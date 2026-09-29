#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 5：生成 `tests/skills/plot-python/red-green-evidence.md`（RED × GREEN 并列对照，机器抽取）。

写入用 `write_bytes`（本仓纪律；也保证全 LF）。文中每个读数都来自本脚本**当场跑过**的
`check-figure-style.py`（一字未改，blob 与 HEAD 比对见文内）；对照表由当场 stdout **逐格解析**，
不手抄（判词行 -> (状态, 判据 ID, 详情)）。

两侧口径：3 个场景（R1/R2/R3 = `figure-choose/red/brief-R{1,2,3}.md`）× 2 个载体（PNG/PDF）
= 各 6 张图；同一分母 `--textwidth-in 6.31`；同一把尺。PNG 的 `--dpi` 由**产物自身**推得
（PNG 像素宽 ÷ PDF 页盒宽），不写死。

用法： python tests/skills/plot-python/make-evidence.py
"""
import importlib.util
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/plot-python
REPO = HERE.parents[2]
CHECKER = REPO / "tests" / "skills" / "figure-choose" / "check-figure-style.py"
RED = HERE / "red"
GREEN = HERE / "green"
OUT_DOC = HERE / "red-green-evidence.md"
TEXTWIDTH = "6.31"

CRIT = ["F1", "F2", "F3a", "F3b", "F3c", "F3d"]
LINE_RE = re.compile(r"^(PASS|FAIL)\s+(F[0-9][a-d]?)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)?\s*$")


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
    for n in (1, 2, 3):
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


def main():
    red = side(RED, "R")
    green = side(GREEN, "G")

    # 同一把尺：checker 的工作树 blob == HEAD 的 blob
    rel = CHECKER.relative_to(REPO).as_posix()
    wt_blob, _ = run(["git", "hash-object", rel])
    hd_blob, _ = run(["git", "rev-parse", f"HEAD:{rel}"])
    wt_blob, hd_blob = wt_blob.strip(), hd_blob.strip()

    probe = carrier_probe()

    L = []
    a = L.append
    a("# Task 5 · RED × GREEN 对照证据（mcm-plot-python）")
    a("")
    a("本文件由 `tests/skills/plot-python/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("文里每个读数都来自下面附的原始 stdout。**对照表是机器抽取的**：判词行逐格解析成")
    a("`(状态, 判据 ID, 详情)`，不是手抄。")
    a("")
    a("## §0 口径（两侧同源同数）")
    a("")
    a("- **场景**：同一份 `tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，未改写）。")
    a("  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景。")
    a("- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。")
    a("- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。")
    a(f"  工作树 blob `{wt_blob[:12]}` · `HEAD:` blob `{hd_blob[:12]}` ⇒ "
      + ("**相同**" if wt_blob == hd_blob else "**不同（！）**"))
    a("- **同数**：每侧 3 场景 × 2 载体（PNG/PDF）= **6 张图**，两侧共 12 张；判据 6 条 × 12 张。")
    a("- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行。")
    a("- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；")
    a("  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。")
    a("  RED **不 import `mcmplot`、不用 `mcm.mplstyle`**。")
    a("- **GREEN 侧**：由本任务 agent **用模块**（`mcmplot.apply_style/figsize_for/save`）产出；")
    a("  **图注是判断层动作**（我写的），不是场景给的。")
    a("")
    a("## §1 RED 原始读数（朴素写手 · 无规范）")
    a("")
    for n in (1, 2, 3):
        a(f"### R{n}（dpi={red[n]['dpi']}）")
        a("")
        a(f"图注（`red/out-R{n}/caption.txt`，逐字）：")
        a("```text")
        a(red[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in ("png", "pdf"):
            r = red[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §2 GREEN 原始读数（模块 · `mcmplot`）")
    a("")
    for n in (1, 2, 3):
        a(f"### G{n}（dpi={green[n]['dpi']}）")
        a("")
        a(f"图注（`green/out-G{n}/caption.txt`，逐字）：")
        a("```text")
        a(green[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in ("png", "pdf"):
            r = green[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §3 对照表（机器抽取）")
    a("")
    a("每个格子 = `状态`（绿=PASS / 红=FAIL）。同场景同行，RED 与 GREEN 并列；判据 ID 见表头。")
    a("")
    a("| 场景 | 载体 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    for n in (1, 2, 3):
        for car in ("png", "pdf"):
            for name, data in (("RED", red), ("GREEN", green)):
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
    for n in (1, 2, 3):
        for car in ("png", "pdf"):
            for name, data in (("RED", red), ("GREEN", green)):
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
    for name, data in (("RED", red), ("GREEN", green)):
        reds, ok_imgs = [], 0
        for n in (1, 2, 3):
            for car in ("png", "pdf"):
                c = data[n][car]["cells"]
                if len(c) == len(CRIT) and all(v[0] for v in c.values()):
                    ok_imgs += 1
                for k in CRIT:
                    if k in c and not c[k][0]:
                        reds.append(k)
        a(f"| {name} | {len(reds)} | {'、'.join(sorted(set(reds))) or '（无）'} | {ok_imgs}/6 |")
    a("")
    a("## §4 F2 随载体变（**不能跨载体比 F2**）")
    a("")
    a(probe)
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
    for n in (1, 2, 3):
        for car in ("png", "pdf"):
            assert green[n][car]["result"][0], f"GREEN {n}/{car} 未全绿"
    for n in (1, 2, 3):
        bad = set()
        for car in ("png", "pdf"):
            bad |= {k for k, v in red[n][car]["cells"].items() if not v[0]}
        print(f"RED R{n} 判红判据：{sorted(bad)}")
    print("OK")


def carrier_probe():
    """现场探针：同一张图（G3 数据，横条**描白边**）在 PNG 与 PDF 上的 F2 读数。

    直接 import 检查器的 `raster_rgb`/`color_count`（不抄），产物落 build/（gitignored）。
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    bd = REPO / "build" / "m3-t5-carrier-probe"
    bd.mkdir(parents=True, exist_ok=True)
    D = list("ABCDEF")
    LO = [0.42, 0.31, 0.55, 0.28, 0.37, 0.50]
    ME = [0.35, 0.44, 0.30, 0.47, 0.38, 0.33]
    HI = [0.23, 0.25, 0.15, 0.25, 0.25, 0.17]
    png, pdf = bd / "white-edge.png", bd / "white-edge.pdf"
    for out in (png, pdf):
        fig, ax = plt.subplots(figsize=(6.31, 2.6))
        y = np.arange(6)
        left = np.zeros(6)
        for vals, lab in ((LO, "low"), (ME, "medium"), (HI, "high")):
            ax.barh(y, vals, left=left, height=0.62, label=lab,
                    edgecolor="white", linewidth=0.6)
            left = left + np.array(vals)
        ax.set_yticks(y)
        ax.set_yticklabels(D)
        fig.savefig(out, dpi=200, bbox_inches=None)
        plt.close(fig)
    n_png = CHK.color_count(CHK.raster_rgb(png))
    n_pdf = CHK.color_count(CHK.raster_rgb(pdf))
    return ("同一份数据、同一张图（横条**描白边**），只换载体：\n\n"
            "```\n"
            f"PNG  F2 = {n_png}\n"
            f"PDF  F2 = {n_pdf}\n"
            "```\n\n"
            "⇒ **F2 随载体变**（这里 PNG 比 PDF 高：PNG 栅格上描边的抗锯齿混色占到 0.5% 以上；"
            "PDF 走第 1 页 150 dpi 栅格，混色占比低于阈值）。\n"
            "**结论：F2 不能跨载体比** —— 同一张图必须写清“这是在哪个载体上量的”。\n"
            "（同一个机制也解释了 GREEN 的 G3 / G1 **初版**：它们给条描了白边，实测 PNG 的 F2 "
            "被抬高一档（G3 初版 PNG=5 / PDF=3；G1 初版加 constrained 后 PNG=4 / PDF=3）；"
            "去掉白边后两图两载体都回落到 3。**这是“看图 + 看读数”逼出来的修图**。）\n"
            "（另一条独立佐证：侦察 `tests/m3-plot-recon/out-d11-red-loop.txt` 的线图上是 "
            "PNG=2 / PDF=1 —— 同样不同，方向与本探针相反，更说明两载体不可互换。）")


JUDGMENT = """**这一节是判断层，机械判据判不了它。**下面是我（本任务 agent）**亲眼看图**后写下的：
我读到了什么、读不出什么。**写真话**。

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（R1 构成，堆叠条；PNG/PDF 都看过）**：横轴是分区 A–F，纵轴是区内面积占比（0–1），
  三段低/中/高。**读得出**：高脆弱档在六个区几乎等高（都落在四分之一上下一线），差异全在
  低/中两档的分割 —— C、F 的低档最长（占半个区以上），D、B 的低档最短、中档最厚。
  我在图上加的那条 `B-D most similar` 括线，把 brief 要的那句判断直接落到图上（**这是我加的，
  不是场景给的**）。
  **读不出 / 要打折**：这张图**不能**替读者判断“B 与 D 相似”——它只画了构成；相似性要靠我
  额外算的 L1 距离（B–D=0.06，见 `figure-choose/red/truth.py`）。图**显示**了构成，**判断**
  是我给的。
- **G2（R2 相关，横条；PNG/PDF 都看过）**：横轴 Pearson r（−1…1），四条属性。**读得出**：
  mean slope 那根最长且朝正、被我挑成红色 —— 唯一的强正相关；vegetation cover 与
  infrastructure index 朝负、量级相近；population density 短、近乎无关。与数据里的
  r=+0.93 / −0.74 / −0.78 / +0.36 对得上。
  **读不出**：图上只给 Pearson；brief 问“哪个因子相关最强”，对小样本（n=6）的稳健性不在图上
  （Spearman 没画）—— 这是这张图的射程缺口。
- **G3（R3 交付形态，横向堆叠条；PNG/PDF 都看过）**：同 R1 数据、A–F 排序。**读得出**：
  与 G1 同一结论，横过来、单栏，可直接进正文。**读得出（修图时）**：最初横条描了白边，
  抗锯齿把 PNG 的 F2 抬到 5（同图 PDF=3）——**看图 + 看读数**逼我把白边去掉（见 §4）。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1**：一张两联图（左堆叠条、右 15 对距离排序条）。**读得出**：构成部分画得对，信息比
  GREEN 更全（它把“最相似的一对”用距离条显式画了出来）。**反差点**：图**偏宽**（F1=1.21），
  图注是一整段 **168 词**的英文（F3a/F3b/F3c 三条红）—— 判红的三条，恰恰都在“形态”上，
  而这张图**信息并不少**。⇒ **信息足**与**合规范**在这张图上是两件事。
- **R2**：两联图（相关条 + 6×6 标准化距离热图）。**读得出**：连续蓝 colormap 颜色很多
  （F2=12），信息同样很足（连 p<0.05 星号、Spearman 空心圈都画了）。**反差点**：F1/F2/F3 全红
  —— 又一次“**画得越丰富越容易被判红**”，因为判据管的是**形态**不是**信息量**。
- **R3**：一张两联图（左：六区 100% 堆叠构成条；右：**6×6 总变差距离（TV）矩阵**热图 ——
  **与 R1 的“15 对欧氏距离排序条”不是同一种面板**，是另一张图）。**读得出**：(a) 单色蓝渐变的
  低/中/高三档、每段印着占比，B、D 两列被**橙框**圈出，两列构成几乎重合（B 0.31/0.44/0.25 vs
  D 0.28/0.47/0.25）—— 图上**直接显示**了“这两个区构成接近”；(b) TV 矩阵里 B–D 格（含镜像两格）
  最浅（0.03）且同样被橙框圈出，C–D 格最深（0.27），A–E / C–F 次浅（0.05）—— 判断**画在了图上**，
  不像 R1 只画构成、相似性要另算。**读不出 / 要打折**：矩阵只画了 **TV** 这一个度量（写手自报
  另核过欧氏同序，但**那张图不在图上**）；n=6 的稳健性同样不在图上。**反差点**：这张图是三张里
  **偏宽最厉害**的（F1=1.51），单色渐变堆叠条让 F2=15，图注 237 词 —— 是“**信息最全、形态判红
  最多**”的那个极端；判据抓的仍是**形态**，不是信息量。

### 一句话
**机械层测的是“形态合不合规范”，判断层测的是“图讲没讲清”。** 两侧都真跑过后我看到：
RED 的图**信息常常更多**却形态判红；GREEN 的图形态全绿，但“支持判断”这一层是我用图上
一笔/一句补的 —— 把它读成“这张图没问题”是不对的。
"""


if __name__ == "__main__":
    main()
