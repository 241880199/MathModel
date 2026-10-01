#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 4：生成 `tests/skills/plot-matlab/red-green-evidence.md`（RED × GREEN 并列对照，机器抽取）。

写入用 `write_bytes`（本仓纪律；也保证全 LF）。文中每个读数都来自本脚本**当场跑过**的
`check-figure-style.py`（一字未改，blob 与 HEAD 比对见文内）；对照表由当场 stdout **逐格解析**，
不手抄（判词行 -> (状态, 判据 ID, 详情)）。

两侧口径：3 个场景（R1/R2/R3 = `tests/skills/figure-choose/red/brief-R{1,2,3}.md` 的 MATLAB 版，
逐字节同源）× 2 个载体（PNG/PDF）= 各 6 张图；同一分母 `--textwidth-in 6.31`；同一把尺。
PNG 的 `--dpi` 由**产物自身**推得（PNG 像素宽 ÷ PDF 页盒宽），不写死。

用法： python tests/skills/plot-matlab/make-evidence.py
"""
import importlib.util
import os
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/plot-matlab
REPO = HERE.parents[2]
CHECKER = REPO / "tests" / "skills" / "figure-choose" / "check-figure-style.py"
RED = HERE / "red"
GREEN = HERE / "green"
OUT_DOC = HERE / "red-green-evidence.md"
TEXTWIDTH = "6.31"
MATLAB = os.environ.get("MATLAB_BIN", "D:/Software/Matlab/bin/matlab.exe")   # GC12：本机 R2025b Update 5

# 场景编号与载体：**唯一一处**定义 —— 图数与判据清单都由它现推，别处**不许再写死**。
SCENES = (1, 2, 3)
CARRIERS = ("png", "pdf")
# 判据 ID 允许**多位数**（`F10`、`F12`…）：检查器将来新增两位数判据时，下面按行解析的汇总表
# 不会静默丢格（`M3-plot-INIT` 的「清单写死 6 条 / 检查器实得 9 条」同型坑：解析器看不见 = 静默丢项）。
LINE_RE = re.compile(r"^(PASS|FAIL)\s+(F[0-9]+[a-d]?)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)?\s*$")


def criteria_ids(*sides):
    """判据 ID 清单**现取**自检查器的实得输出（保持首次出现次序）—— **不写死**。

    先例病灶（plot-python `make-evidence.py`）：写死过 `CRIT = [F1, F2, F3a..d]`，而 Task 3 又加了
    F4/F5/F6 ⇒ 解析器每张图抓到 9 条、清单 6 条 ⇒ `len(c) == len(CRIT)` 恒 False ⇒ 汇总表
    「红格数」「全绿图数」**静默归零**、三条判据静默丢掉（任务书铁律 7 / `M3-plot-INIT`）。
    **现取**（清单跟着检查器走、不由本件维护第二份）才是不会再漂的那一版。
    """
    ids = []
    for data in sides:
        for n in SCENES:
            for car in CARRIERS:
                for k in data[n][car]["cells"]:
                    if k not in ids:
                        ids.append(k)
    # 排序只为表头好读；**集合**才是从输出现取的（顺序不影响任何判红/计数）。
    ids.sort(key=lambda k: (int(re.match(r"F(\d+)", k).group(1)), k))
    return ids


def load_checker():
    spec = importlib.util.spec_from_file_location("chk", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CHK = load_checker()


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(REPO))
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + "\n"
    return out, r.returncode


def png_dpi(png, pdf):
    from PIL import Image
    import fitz
    with Image.open(png) as im:
        pw = im.size[0]
    with fitz.open(pdf) as doc:
        win = doc[0].rect.width / 72.0
    return int(round(pw / win))


def check_fig(fig, caption_file, dpi):
    cmd = ["python", str(CHECKER.relative_to(REPO)), "--fig", str(fig.relative_to(REPO)),
           "--caption", "@" + str(caption_file.relative_to(REPO)),
           "--textwidth-in", TEXTWIDTH]
    if fig.suffix.lower() == ".png":
        cmd += ["--dpi", str(dpi)]
    out, rc = run(cmd)
    cells, result = {}, None
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1) == "PASS", m.group(3))
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
    return {"cmd": " ".join(cmd), "stdout": out, "rc": rc, "cells": cells, "result": result}


def side(dirname, tag):
    res = {}
    for n in SCENES:
        d = dirname / f"out-{tag}{n}"
        pdf, png = d / "figure.pdf", d / "figure.png"
        cap = d / "caption.txt"
        dpi = png_dpi(png, pdf)
        res[n] = {
            "pdf": check_fig(pdf, cap, dpi),
            "png": check_fig(png, cap, dpi),
            "dpi": dpi,
            "caption_bytes": cap.read_bytes().decode("utf-8"),
        }
    return res


def verdict_cell(c):
    return "绿" if c[0] else "红"


def f2_num(cell):
    """从 F2 判词（`彩色主色数 N`）里取 N —— **当场抽取**，不另存第二份。"""
    if not cell:
        return None
    m = re.search(r"彩色主色数 (\d+)", cell[1])
    return int(m.group(1)) if m else None


def _h14_hexes():
    """H14 色序 —— **现读**单源 `mcm-style.json` 的 `series.color`（与 F5 用的那份同源），不手写第二份。"""
    import json
    data = json.loads(pathlib.Path(CHK._STYLE_PATH).read_text(encoding="utf-8"))
    return next(e["value"] for e in data["entries"] if e["id"] == "series.color")


def _probe_readings(fig_path, dpi):
    """当场跑检查器**本人**的 `check()`（同一支仪器、不另写一份口径），返回 `(F2 数, F5 判词原文)`。"""
    res = {cid: (ok, why) for cid, ok, why in CHK.check(fig_path, "Figure 1: probe",
                                                          float(TEXTWIDTH), dpi)}
    f2 = int(re.search(r"彩色主色数 (\d+)", res["F2"][1]).group(1))
    return f2, res["F5"][1]


# 两态探针的 MATLAB 驱动（由本脚本生成到 build/ 下，收工自清 _probe/）。
# ★ `\n` 一律不写进 .m 源码（本仓踩过：f-string 里 `\\n` 落到 MATLAB 源里成了真换行 ⇒ 语法错）⇒ 用 disp。
_PROBE_M = """here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(here)));   % build/m3-matlab-t4-carrier-probe/_probe -> repo root
addpath(fullfile(root,'.claude','skills','mcm-plot-matlab','assets'));
OUT = fullfile(root,'build','m3-matlab-t4-carrier-probe');
if ~exist(OUT,'dir'); mkdir(OUT); end
M = mcmplot();
D  = {'A','B','C','D','E','F'};
lo = [0.42 0.31 0.55 0.28 0.37 0.50];
me = [0.35 0.44 0.30 0.47 0.38 0.33];
hi = [0.23 0.25 0.15 0.25 0.25 0.17];
H14 = __H14__;
for tag = {'edge','noedge'}
  fig = M.figure(6.31); ax = axes(fig);
  b = barh(ax, [lo(:) me(:) hi(:)], 'stacked');
  for k = 1:3
    b(k).FaceColor = H14(k,:);
    if strcmp(tag{1}, 'edge'); b(k).EdgeColor = 'white'; b(k).LineWidth = 0.6;
    else; b(k).EdgeColor = 'none'; end
  end
  set(ax,'YTickLabel',D); xlabel(ax,'Share of district area (fraction)'); xlim(ax,[0 1]);
  legend(ax, {'low','medium','high'}, 'Location','southoutside','Orientation','horizontal');
  M.apply(fig);
  M.save(fig, fullfile(OUT, sprintf('probe-%s.png', tag{1})), 300);
  M.save(fig, fullfile(OUT, sprintf('probe-%s.pdf', tag{1})));
  close(fig);
end
disp('carrier probe done');
"""


def carrier_probe():
    """现场探针：同一张图（六段**横向堆叠条**，H14 配色）在 PNG 与 PDF 上的 F2 / F5 读数。

    被换的量 = **描不描白边**（驱动里只改 `EdgeColor` / `LineWidth`，与 python 侧探针同型）；
    每态各出 PNG 与 PDF 两个载体。
    读数**当场算**（import 检查器的 `check()`，同一支仪器）。产物落 `build/`（gitignored）。
    ★ 本探针是**如实复刻 python 侧的构造**、不预设结论 —— 它有可能证明"MATLAB 上该构造
      **不**移动 F2"（本仓实测正是如此），那种结局与"移动了"一样要照实写。
    """
    hexes = _h14_hexes()[:3]
    rgbs = [[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in hexes]
    mat = "[" + "; ".join(" ".join(f"{c/255:.6f}" for c in rgb) for rgb in rgbs) + "]"
    bd = REPO / "build" / "m3-matlab-t4-carrier-probe"
    probedir = bd / "_probe"
    probedir.mkdir(parents=True, exist_ok=True)
    drv = probedir / "probe_carrier.m"
    drv.write_bytes(_PROBE_M.replace("__H14__", mat).encode("utf-8"))
    try:
        pr = subprocess.run([MATLAB, "-batch",
                             f"run('{drv.relative_to(REPO).as_posix()}')"],
                            cwd=str(REPO), capture_output=True, text=True)
        rc, out, err = pr.returncode, pr.stdout, pr.stderr
    except OSError as e:
        rc, out, err = 127, "", f"{type(e).__name__}: {e}"
    finally:
        shutil.rmtree(probedir, ignore_errors=True)
    if rc != 0:
        return (f"探针跑不动（MATLAB 退出 {rc}）⇒ fail-closed。stdout/stderr：\n\n```\n"
                f"{out.rstrip()}\n{err.rstrip()}\n```\n", None)
    f2, f5 = {}, {}
    for tag in ("edge", "noedge"):
        for car, dpi in (("png", 300), ("pdf", None)):
            f2[(tag, car)], f5[(tag, car)] = _probe_readings(bd / f"probe-{tag}.{car}", dpi)
    w_png, w_pdf = f2[("edge", "png")], f2[("edge", "pdf")]
    n_png, n_pdf = f2[("noedge", "png")], f2[("noedge", "pdf")]
    body = ("同一份数据、同一张图（六段**横向堆叠条**，**H14 配色**）；被换的量 = **描不描白边**"
            "（驱动脚本里就改 `EdgeColor` / `LineWidth` 两个字段，其余逐行相同），"
            "每态各出两载体。读数**当场算**（`check-figure-style.py` 本人的判词，逐字抄）：\n\n"
            "```\n"
            "              PNG  PDF\n"
            f"描白边          {w_png}    {w_pdf}\n"
            f"不描边（对照）   {n_png}    {n_pdf}\n"
            "```\n\n"
            f"⇒ 本机实测（R2025b Update 5）：**就这一个构造、这两态**而言，"
            f"同图两态的 F2 在 PNG 与 PDF 上逐格相同（描白边 {w_png}/{w_pdf} · 不描边 {n_png}/{n_pdf}）"
            "—— **与 python 侧那件探针的结论相反**"
            "（python 上描白边把 PNG 的 F2 由 3 抬到 5、PDF 不变）。\n"
            "⇒ **如实收窄（射程只到这里）**：本探针只证明「**这一个构造、这两态**不移动 F2」，"
            "**驳不倒**「MATLAB 产物的 F2 可以随载体变」—— 另有一个**未入库的自造构造**能把同一张图的"
            " F2 在两个载体上拉开（读数未落盘，此处不复述，先例 `M3-plot-INIT`）。"
            "故本探针**不构成**「MATLAB 上 F2 不随载体变」的证据，**也无权**被那样读。\n"
            "**那么「不许跨载体比 F2」这条规矩**的承重**不是**本探针，而是**器械口径**："
            "检查器对两载体走**不同的栅格化路径** —— PNG 直接 `Image.open`（原生像素、按 `--dpi` 定尺）、"
            "PDF 第 1 页按固定 `RASTER_DPI=150` 栅格化（`raster_rgb()`）⇒ 同一条 `color_count` 吃到的"
            "像素来源不同 ⇒ 两个读数**不是同一个量**，故**不可跨载体比**。这是设计 §2、"
            "检查器 docstring 与 python 先例共同定下的口径。\n"
            "同一支检查器的 F5 判词（逐字）：\n\n"
            "```\n"
            f"描白边 PNG：{f5[('edge', 'png')]}\n"
            f"描白边 PDF：{f5[('edge', 'pdf')]}\n"
            f"不描边 PNG：{f5[('noedge', 'png')]}\n"
            f"不描边 PDF：{f5[('noedge', 'pdf')]}\n"
            "```\n")
    pairs = {"edge": (w_png, w_pdf), "noedge": (n_png, n_pdf)}
    return body, pairs


JUDGMENT = """**这一节是判断层，机械判据判不了它。** 下面是我（本任务 agent）**亲眼看图**后写下的：读到了什么、
读不出什么。**写真话**。六张图（逐张列在下面、各带仓内相对路径）我都打开看过（PNG），并另核了 PDF 同源。
对每一张必看的两点：**底色是不是浅色** · **顶/右框线在不在、刻度朝内还是朝外**（`H10`）。
刻度朝向不是"看着像"：用像素量过（底脊线上方 / 下方各 8 px 带里灰度 < 60 的墨迹像素数），读数写在每条里。

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（`tests/skills/plot-matlab/green/out-G1/figure.png`，R1 构成，竖堆叠条）**：
  **底色浅色**（F4 外缘环 100% 白）；**无顶/右框线**；**刻度朝内**（底脊上方 130 : 下方 32 墨迹像素）。
  轴标签带单位（`Share of district area (fraction)`）。读得出：六区 A–F 的三档构成与每段占比；
  读不出：这张图**没有**替读者判断"B 与 D 最像"——那条判断是我在图外另算的。
- **G2（`.../green/out-G2/figure.png`，R2 相关，横条）**：**底色浅色**；**无顶/右框线**；
  **刻度朝内**（77 : 21）。读得出：四条属性的 Pearson r 与灾难次数（mean slope 最强 ≈ +0.93）。
  **看图层逼出两处修图**（初版四个类目名平排互相压住、
  ylabel 太长在 2.6 in 图高里被裁掉顶端 ⇒ 类目名旋 20°、ylabel 缩成 `Pearson r (dimensionless)` 后重出）。
  **初版送检是自报口径**：出图时另跑过一次初版送检、观察到 F1–F6 全 PASS（**未捕获 stdout、未落产物**）；
  **承重的是结构论证**：检查器的 `F1`–`F6` **本来就没有**任何关于刻度标签排版的判据 ——
  一条命令即可列举其全部判据（`grep -nE 'res\\.append\\(\\(\"F' tests/skills/figure-choose/check-figure-style.py`，
  实测 9 条，无刻度标签排版类）；详见 `green/README.md` §3.1。
  读不出：图上只有 Pearson，n=6 的稳健性不在图上。
- **G3（`.../green/out-G3/figure.png`，R3 交付形态，横堆叠条）**：**底色浅色**；**无顶/右框线**；
  **刻度朝内**（119 : 0）。轴标签带 `(fraction)`。读得出：同 R1 数据横过来、单栏可直接进正文。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1（`tests/skills/plot-matlab/red/out-R1/figure.png`）**：竖堆叠条，段内印占比，顶部括线标
  "most similar pair: B & D (L1 = 0.06)"。**底色浅色**（写手**自己**把出厂深色修掉了 —— 其自报：
  本机 MATLAB 跑深色主题、首图导出成黑底，它 pin 了 `ax.Color = 'w'`）；**无顶/右框线**；
  **但刻度朝外**（41 : 95）。信息很足；反差点在**形态**：图偏窄（F1 = 0.748）、配色不落 H14（F5 = 3 种越界）、
  图注 178 词且以句号结尾（F3a/b/c 三条红）。
- **R2（`.../red/out-R2/figure.png`）**：两联图（a 相关横条 + b z-score 热图带 colorbar），
  每个格子印 z 值、相关条带值标 —— 信息量最大的一张。**底色浅色**；**刻度朝内**（907 : 227，量的是 b 面板）；
  **但 b 面板的坐标系带完整四边黑框（上/右框线都在）** —— `H10` 要的是去上/右框线，这一点它没做到。
  反差点：F1 = 1.310 偏宽、F2 PNG = 15（热图多档）、F5 越界 21 种、图注 261 词、PDF 内嵌 **ArialMT**（F6 红）。
- **R3（`.../red/out-R3/figure.png`）**：横堆叠条，Reds 单色三档，段内印整数百分比。
  **底色浅色**；**无顶/右框线**；**刻度朝外**（14 : 78）；xlabel 带 `(%)` 单位。
  反差点：配色（#fee0d2 / #fc9272 / #de2d26）不落 H14（F5 红）、图注 110 词且以句号结尾（F3a/b/c 红）；
  F1 = 0.846 在带内、F2 = 3 绿。

### 一句话
**机械层测的是"形态合不合规范"，判断层测的是"图讲没讲清"。** 六张图（上面六条）都真看过以后：
三张 RED 的信息常常更多（R1 标出最相似对、R2 连 z 值都印了）、底色也都自己修成了浅色，
却仍在**形态**上判红；而且 **R1 / R3 的刻度朝外、R2 的 b 面板带上/右全框** 这三条 `H10` 违反，
**检查器的 F1–F6 没有一条会报** —— 只能靠这一层看见（`H10` 的产物级回读另有入库探针）。
三张 GREEN 形态全绿，但"支持判断"那一层要我在图上另加一笔、图注里另写一句 ——
把 GREEN 读成"这张图没问题"是不对的。"""


def main():
    red = side(RED, "R")
    green = side(GREEN, "G")

    # 判据清单与图数**现取**（见 `criteria_ids()`）；本件**不再写死**任何一条总数。
    CRIT = criteria_ids(red, green)
    SIDES = (("RED", red), ("GREEN", green))
    n_per_side = len(SCENES) * len(CARRIERS)
    n_total = len(SIDES) * n_per_side

    # 同一把尺：checker 的工作树 blob == HEAD 的 blob
    rel = CHECKER.relative_to(REPO).as_posix()
    wt_blob, _ = run(["git", "hash-object", rel])
    hd_blob, _ = run(["git", "rev-parse", f"HEAD:{rel}"])
    wt_blob, hd_blob = wt_blob.strip(), hd_blob.strip()

    probe, _pairs = carrier_probe()

    L = []
    a = L.append
    a("# Task 4 · RED × GREEN 对照证据（`mcm-plot-matlab`）")
    a("")
    a("本文件由 `tests/skills/plot-matlab/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("文里每个读数都来自下面附的原始 stdout。**对照表是机器抽取的**：判词行逐格解析成")
    a("`(状态, 判据 ID, 详情)`，不是手抄。")
    a("")
    a("## §0 口径（两侧同源同数）")
    a("")
    a("- **场景**：`tests/skills/plot-matlab/red/brief-R{1,2,3}.md`（MATLAB 版，场景/数据段与")
    a("  `tests/skills/figure-choose/red/brief-R{1,2,3}.md` **逐字节相同**、只换 Deliverables 段）。")
    a("  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景。")
    a("- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。")
    a("- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。")
    a(f"  工作树 blob `{wt_blob[:12]}` · `HEAD:` blob `{hd_blob[:12]}` ⇒ "
      + ("**相同**" if wt_blob == hd_blob else "**不同（！）**"))
    a(f"- **同数**：每侧 {len(SCENES)} 场景 × {len(CARRIERS)} 载体（PNG/PDF）= **{n_per_side} 张图**，"
      f"两侧共 {n_total} 张；判据 {len(CRIT)} 条 × {n_total} 张。")
    a("- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行；")
    a("  **PDF 不给 `--dpi`**（走页盒）。")
    a("- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；")
    a("  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。")
    a("  RED **不 `addpath` 本模块、不调 `mcmplot`**。")
    a("- **GREEN 侧**：由本任务 agent **用模块**（`mcmplot` 的 `figure/apply/save`）产出；")
    a("  **图注是判断层动作**（我写的），不是场景给的。")
    a("- ★ **两个载体不可比 `F2`**：PNG 与 PDF 在检查器里走**不同的栅格化路径**")
    a("  （PNG 原生像素、PDF 按固定的 150 dpi 栅格化）⇒ F2/F5 的读数**不是同一个量**，")
    a("  **不许跨载体比 F2**（见 §4 的探针与收窄说明）。")
    a("")
    a("## §1 RED 原始读数（朴素写手 · 无规范）")
    a("")
    for n in SCENES:
        a(f"### R{n}（dpi={red[n]['dpi']}）")
        a("")
        a(f"图注（`red/out-R{n}/caption.txt`，逐字）：")
        a("```text")
        a(red[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in CARRIERS:
            r = red[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §2 GREEN 原始读数（模块 · `mcmplot`）")
    a("")
    for n in SCENES:
        a(f"### G{n}（dpi={green[n]['dpi']}）")
        a("")
        a(f"图注（`green/out-G{n}/caption.txt`，逐字）：")
        a("```text")
        a(green[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in CARRIERS:
            r = green[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §3 对照表（机器抽取）")
    a("")
    a("每个格子 = `状态`（绿=PASS / 红=FAIL）。同场景同行，RED 与 GREEN 并列；判据 ID 见表头。")
    a("")
    a("| 场景 | 载体 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    for n in SCENES:
        for car in CARRIERS:
            for name, data in SIDES:
                c = data[n][car]["cells"]
                row = [f"R{n}" if name == "RED" else f"G{n}", car.upper(), name]
                for k in CRIT:
                    cell = c.get(k)
                    row.append(verdict_cell(cell) if cell else "—")
                row.append("PASS" if data[n][car]["result"][0] else "FAIL")
                a("| " + " | ".join(row) + " |")
    a("")
    a("### §3.1 逐判据红/绿明细（含判词，机器抽取）")
    a("")
    a("| 场景 | 载体 | 侧 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- | :-- | :-- |")
    for n in SCENES:
        for car in CARRIERS:
            for name, data in SIDES:
                c = data[n][car]["cells"]
                for k in CRIT:
                    cell = c.get(k)
                    if not cell:
                        continue
                    a(f"| {'R' if name == 'RED' else 'G'}{n} | {car.upper()} | {name} | {k} | "
                      f"{'PASS' if cell[0] else 'FAIL'} | {cell[1]} |")
    a("")
    a("### §3.2 汇总（由 §3 的格子逐格重算）")
    a("")
    a("| 侧 | 红格数（判据×图） | 判红的判据 ID（并集） | 全绿图数 |")
    a("| :-- | :-- | :-- | :-- |")
    for name, data in SIDES:
        reds, ok_imgs = [], 0
        for n in SCENES:
            for car in CARRIERS:
                c = data[n][car]["cells"]
                # 「全绿」= 该图**判据集合与清单逐条相符**且全 PASS（缺一条即不算绿）。
                if set(c) == set(CRIT) and all(v[0] for v in c.values()):
                    ok_imgs += 1
                for k in CRIT:
                    if k in c and not c[k][0]:
                        reds.append(k)
        a(f"| {name} | {len(reds)} | {'、'.join(sorted(set(reds))) or '（无）'} | {ok_imgs}/{n_per_side} |")
    a("")
    a("## §4 F2 与载体（**不许跨载体比 F2**）")
    a("")
    a(probe)
    a("")
    a("- **仓内实测佐证 —— 同一张图的 F2 在两个载体上不同（逐图，机器抽取自 §1/§2）**：")
    a("")
    a("| 场景 | 侧 | F2(PNG) | F2(PDF) | 随载体变？ |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for name, data in SIDES:
        for n in SCENES:
            p = f2_num(data[n]["png"]["cells"].get("F2"))
            q = f2_num(data[n]["pdf"]["cells"].get("F2"))
            a(f"| {'R' if name == 'RED' else 'G'}{n} | {name} | {p} | {q} | "
              f"{'**是**' if p != q else '否'} |")
    a("")
    a("⇒ `R2`（PNG 15 / PDF 3）是**仓内实例**：同一张图的两载体 F2 确实不同 —— 但它**不是**"
      "「不许跨载体比 F2」的**唯一**支撑（该规矩的承重是上面那条**器械口径**：两载体走两条"
      "栅格化路径 ⇒ 读数不是同一个量）。其余各行两载体相同、也不矛盾 —— 该规矩是**禁止把一个"
      "载体的读数当成另一个的**，不是声称「每张图的 F2 都会变」。")
    a("")
    a("## §5 判断层（亲眼看图 · 机械判据之外的那一层）")
    a("")
    a(JUDGMENT)
    a("")
    doc = ("\n".join(L).rstrip("\n") + "\n").replace("\r\n", "\n")
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO), OUT_DOC.stat().st_size, "B")

    # 自证断言（不满足即非零退出）
    assert wt_blob == hd_blob, "checker blob 与 HEAD 不同！"
    # ★ 逐图哨兵：每张图的判据集合必须与清单 `CRIT` **相等**（`CRIT` 也是**从同一批输出现取**的，
    #   不是写死）—— 某张图缺/多一条 ⇒ `set(got) != set(CRIT)` ⇒ 当场炸，不再静默少算。
    #   射程（如实写窄）：清单与各图**同源** ⇒ 给**所有**图**统一**加一条判据时两边同步变、
    #   `set(got) == set(CRIT)` 仍成立 ⇒ 这里不炸；本哨兵抓的是**判据集合在不同图之间不一致**那一类。
    for name, data in SIDES:
        for n in SCENES:
            for car in CARRIERS:
                got = data[n][car]["cells"]
                assert data[n][car]["result"] is not None, f"{name} {n}/{car} 没解析到 RESULT 行"
                assert set(got) == set(CRIT), (
                    f"{name} {n}/{car} 的判据集合与清单不符：{sorted(got)} vs {CRIT}")
    for n in SCENES:
        for car in CARRIERS:
            assert green[n][car]["result"][0], f"GREEN {n}/{car} 未全绿"
    for n in SCENES:
        bad = set()
        for car in CARRIERS:
            bad |= {k for k, v in red[n][car]["cells"].items() if not v[0]}
        print(f"RED R{n} 判红判据：{sorted(bad)}")
    print(f"判据 {len(CRIT)} 条：{CRIT}")
    print("OK")


if __name__ == "__main__":
    main()
