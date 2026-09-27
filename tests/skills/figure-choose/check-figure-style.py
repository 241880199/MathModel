#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcm-figure-choose 产物判据。只读被测图，不改任何东西。fail-closed。

用法：
  python tests/skills/figure-choose/check-figure-style.py \
      --fig <path> --caption <text|@file> --textwidth-in <float> [--dpi <int>] [--json]

退出码：0 全 PASS · 1 有 FAIL · 2 参数/参照缺失（fail-closed：**不产生判词**，只管报错退出）
末行：`RESULT: PASS` 或 `RESULT: FAIL（...）`，**恒定是最后一行**（`--json` 的 JSON 打在它**之前**）；
     exit 2 的路径不打印任何判词，也不打印 `RESULT:`。

判据 ID：F1 图宽比 ∈[0.80,1.20] · F2 彩色主色数 ≤4 · F3a 图注以 `Figure <n>:` 起 ·
F3b **正文**词数 ≤12（>17 硬失败）· F3c 句末无句号 · F3d 图注正文非空。

**两种载体都判**：PNG（本 Task 的 fixture）与 **PDF**（M3 的载体定为 TikZ，主要产物格式）。
  · F1：PDF 走页盒 `doc[0].rect.width/72`（矢量、精确，**不用 --dpi**）；PNG 走 `--dpi`（必须显式给）。
  · F2：PDF 第 1 页按 `RASTER_DPI` 栅格化成 RGB 再数色（`get_pixmap` → `Image.frombytes`）；
        PNG 直接 `Image.open`。**两条载体走同一条 `raster_rgb()`**，保证 F2 口径一致。

**fail-closed 的覆盖面**（拿到不参照就不判，一律 exit 2、且不打印判词）：
  `--textwidth-in ≤ 0` · `--dpi ≤ 0` · `--fig` 不存在／是目录 · `--fig` 不是图像（含 PDF 解析不了） ·
  `--caption @file` 读不出 · PNG 未给 `--dpi`。实现上：所有 I/O 与形参校验都在 `fail_closed()` 里出口，
  **不许**让 `FileNotFoundError` / `UnidentifiedImageError` / `ZeroDivisionError` 之类裸异常漏出去
  ——裸异常的退出码也是 1，会与「判过且红」撞号（那正是本 Task 要消灭的盲区）。

**分母口径**：`--textwidth-in` 由调用方传入，本脚本**不预设**。本仓 2026-09-27 的演示一律传
`6.31`（= 逐篇正文行宽 p90 的全局中位，侦察读数；见 tests/figures-recon/b-stats.txt
`col_w_in: ... median=6.310`）。换口径（如逐篇 p90）会给出不同的比值，**结论可能不同**。

---
**与派发任务书（`.superpowers/sdd/task-m3-t1-brief.md` Step 3）的代码差异 —— 六处，均为实测逼出**

D1（F2 算法）：`resize((320,320))` → `resize((320,320), Image.NEAREST)`。
  任务书用默认重采样（Pillow 12 = BICUBIC），重采样在色带交界处**造出新颜色**，再经
  `//16` 分箱时把**同一个真色劈成两个箱**。实测（命令与输出见
  `tests/skills/figure-choose/figure-style-baseline.txt`）：ok-01 只有 3 色却读成 **4**、
  ok-03 只有 4 色却读成 **5** ⇒ 任务书自带的期望表（ok-01 F2 PASS / ok-03 F2 PASS）
  **当场对不上**。改 NEAREST 后 6 个 fixture 的读数与任务书期望表逐格一致
  （ok-01=3 · ok-02=1 · ok-03=4 · bad-f2=6）。
  **阈值 320/16/24/0.005/≤4 一个没动** —— 动的只是"怎么采到像素"。
  ⚠️ 口径提醒：本函数与侦察用的 `quantize(32, MEDIANCUT)` **不是同一支仪器**（166 张抽样上
  中位 2 vs 4），故 spec 里"实测中位 3"这个数**不能直接用本函数复算**（Task 3 须二选一并写明）。

D2（F3d）：任务书写 `words > 0`，但样本里的空图注形态是 `Figure 13:`（只有前缀没正文，
  17/662）——`"Figure 13:".split()` 有 2 个词，`words > 0` 恒真，**这条判据抓不到它要抓的东西**。
  且任务书自己的 fixture `caption:4 = Figure 4:` 标的是 F3d FAIL，用 `words > 0` 只能得 PASS。
  故 F3d 改为"**去掉 `Figure N:` 前缀后的正文非空**"（F3a 已单独判前缀形态）。

D3（退出码）：任务书写 `sys.exit("...")`（= exit 1），但同一份任务书的 Interfaces 段与
  spec 都写死 `2 = 参数/参照缺失（fail-closed）`。两者冲突时取 **exit 2**，理由：`1` 已被
  "有 FAIL" 占用，若 fail-closed 也退 1，"判过且红"与"根本没判成"就分不开——这正是本任务
  M3 变异要证的那件事。

D4（PDF 的 F2，**独立复审判定 Important-1 逼出**）：任务书的 Step 3 代码把 `Image.open(fig)`
  无条件用在 F2 上，而 PDF 是本设计的**主要产物格式**（载体已定为 TikZ）。实测一张
  6.0×2.6 in 的 PDF：rc=1、**stdout 空**、`PIL.UnidentifiedImageError` —— 即"F1 用 fitz、
  F2 用 Pillow"这个半吊子状态让 PDF **根本判不完整**。本实现的取法：**F2 也吃 PDF**——
  第 1 页 `get_pixmap(dpi=RASTER_DPI, colorspace=csRGB, alpha=False)` → `Image.frombytes`
  → 与 PNG 走同一条 `color_count`。因此文件头"两种载体都判"的自称与本实现一致。
  （另一条路是删掉 fitz 分支、写死"仅 PNG"，但那会与本设计的载体选择直接冲突。）

D5（fail-closed 覆盖面，**独立复审判定 Important-2 逼出**）：任务书的 Step 3 只对
  `--textwidth-in ≤ 0` 与"图不存在"做了守卫，其余全部裸异常漏出（实测：`@不存在` →
  `FileNotFoundError` rc=1；图不是图像 → `UnidentifiedImageError` rc=1；`--fig <目录>` →
  `PermissionError` rc=1；`--dpi 0` → `ZeroDivisionError` rc=1；**`--dpi -200` 竟然打印判词**
  `FAIL F1 图宽比 -0.951`）。本实现把这五条全并进 `fail_closed()`，并**把 `--dpi ≤ 0` 与
  `--textwidth-in ≤ 0` 同等拒绝**。

D6（`--json` 的位置，**独立复审判定 R-4 逼出**）：任务书把 JSON 打在 `RESULT:` **之后**，
  于是"末行固定为 `RESULT:`"这条接口契约在 `--json` 下**不成立**。本实现把 JSON 挪到
  `RESULT:` 之前：末行恒为判词行，JSON 是它的机器可读副本。

D7（F3b 的词数口径，**Task 6 GREEN 对照的 Important-2 逼出**）：F3b 原先数**整条图注**
  （`cap.split()`，含 `Figure N:` 这 2 个词），而规范 H9 与它的复跑仪器 `house-metrics.py`
  的 `cap_words_*` 用的是**去掉 `Figure N:` 前缀后的正文**（口径原文见
  `references/provenance.md` 的 P-D-c1）。同一批 662 条图上两口径**相差恰好 2 词**、
  **不可互换** ⇒ 出货检查器与规范在当时是**两个口径**。本轮收敛到**规范侧**：
  `words = len(caption_body(cap).split())`（`caption_body` 见下，F3d 本就在用）。
  **常量 `CAP_MAX` 12 / `CAP_HARD` 17 与 `G-H9-*` 守卫一个没动**——12/17 本来就是
  **正文口径**的 p95/max（`c8-caption.tsv:913`：正文 p95=12 / max=17；含标签口径是 14/19）。
  影响面（实测）：GREEN 三份由"整条 13 词"变为"正文 11 词"⇒ F3b 转绿；RED 三份的图注以
  `Figure 1.`（句点、无冒号）起，`caption_body` 切不出前缀 ⇒ 整条算正文 ⇒ 读数一字不变
  （203/285/177，仍红）。
"""
import argparse
import json
import pathlib
import re
import sys

import fitz                      # PyMuPDF
from PIL import Image

F1_LO, F1_HI = 0.80, 1.20        # spec house-style #1（实测 p25 / max）
F2_MAX = 4                       # spec #4（实测中位 3）
CAP_MAX, CAP_HARD = 12, 17       # spec #9（实测 p95 / 全样本上界）
RASTER_DPI = 150                 # PDF 栅格化密度（只影响 F2 采样，与 F1 无关；见 D4）
EXIT_FIG_FAIL = 1                # 判过，且至少一条判据红
EXIT_FAIL_CLOSED = 2             # 拿不到参照：不产生判词，只报错退出


def fail_closed(msg):
    """拿不到参照时的唯一出口：非零退出，**不得**返回空结果静默通过。"""
    print(msg, file=sys.stderr)
    sys.exit(EXIT_FAIL_CLOSED)


def read_caption(spec):
    """`--caption` 原样返回；`@file` 读文件。读不出 ⇒ fail_closed（不裸抛 FileNotFoundError）。"""
    if not spec.startswith("@"):
        return spec
    path = pathlib.Path(spec[1:])
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图注文件 {path}（{type(e).__name__}: {e}）（fail-closed）")


def raster_rgb(path):
    """把图变成 RGB 像素供 F2 数色：PDF 走第 1 页栅格化，PNG/JPG 走 Pillow。

    两个载体的像素都经同一条 `color_count`，故 F2 口径一致。读不出 ⇒ fail_closed。
    """
    try:
        if path.suffix.lower() == ".pdf":
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                pm = doc[0].get_pixmap(dpi=RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
                return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        with Image.open(path) as im:
            return im.convert("RGB")       # 立刻取像素，脱离文件句柄；坏文件在这里就报
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图 {path}（{type(e).__name__}: {e}）（fail-closed）")


def color_count(im):
    """彩色主色数：去掉近黑/近白/近灰，只数占比 >=0.5% 的颜色。

    采样用 NEAREST：重采样（BICUBIC 等）会在色带交界造出新色，`//16` 分箱随即把同一真色
    劈成两箱 ⇒ 系统性**多**数（见文件头 D1）。
    """
    im = im.convert("RGB").resize((320, 320), Image.NEAREST)   # 与分辨率无关；不重采样造色
    tot, keep = 320 * 320, {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24:           # 近灰（含黑/白）
            continue
        keep[(r // 16, g // 16, b // 16)] = keep.get((r // 16, g // 16, b // 16), 0) + cnt
    return sum(1 for c in keep.values() if c / tot >= 0.005)


def fig_width_in(path, dpi):
    """图宽（英寸）。PDF 用页盒（矢量、精确，不用 --dpi）；PNG 走 --dpi（必须显式给）。"""
    if path.suffix.lower() == ".pdf":
        try:
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                return doc[0].rect.width / 72.0
        except Exception as e:                                 # noqa: BLE001（fail-closed 出口）
            fail_closed(f"FAIL: 读不出 PDF 页盒 {path}（{type(e).__name__}: {e}）（fail-closed）")
    if dpi is None:
        fail_closed("FAIL F1: PNG 需要显式 --dpi（PNG 的 dpi 元信息不可信，见 provenance）")
    try:
        with Image.open(path) as im:
            return im.size[0] / dpi
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图 {path}（{type(e).__name__}: {e}）（fail-closed）")


def caption_body(cap):
    """图注正文 = 去掉 `Figure N:` 前缀之后的部分；切不出前缀时整条算正文（F3a 会另外报红）。"""
    m = re.match(r"^Figure\s+\d+\s*:", cap)
    return cap[m.end():].strip() if m else cap


def check(fig, caption, textwidth_in, dpi):
    res = []
    if textwidth_in <= 0:
        fail_closed("FAIL: --textwidth-in 必须为正（fail-closed）")
    if dpi is not None and dpi <= 0:          # 与 --textwidth-in 同等拒绝（见文件头 D5）
        fail_closed(f"FAIL: --dpi 必须为正（收到 {dpi}）（fail-closed）")
    ratio = fig_width_in(fig, dpi) / textwidth_in
    res.append(("F1", F1_LO <= ratio <= F1_HI, f"图宽比 {ratio:.3f}（分母 {textwidth_in:.2f} in）"))
    n = color_count(raster_rgb(fig))
    res.append(("F2", n <= F2_MAX, f"彩色主色数 {n}"))
    cap = caption.strip()
    res.append(("F3a", bool(re.match(r"^Figure\s+\d+\s*:", cap)), "图注以 `Figure N:` 起"))
    body = caption_body(cap)                              # 正文口径：见文件头 D7（口径与 H9 收敛）
    words = len(body.split())
    res.append(("F3b", words <= CAP_MAX, f"图注词数 {words}（上限 {CAP_MAX}，硬上限 {CAP_HARD}）"))
    if words > CAP_HARD:
        res[-1] = ("F3b", False, f"图注词数 {words} 超硬上限 {CAP_HARD}")
    res.append(("F3c", not cap.endswith("."), "句末不加句号"))
    res.append(("F3d", bool(body), f"图注正文非空（正文 {len(body.split())} 词）"))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fig", required=True)
    ap.add_argument("--caption", required=True)
    ap.add_argument("--textwidth-in", type=float, required=True)
    ap.add_argument("--dpi", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.fig)
    if not p.is_file():                       # 不存在 / 是目录 / 是设备文件，一律 fail-closed
        fail_closed(f"FAIL: 图不存在或不是普通文件 {a.fig}（fail-closed）")
    cap = read_caption(a.caption)
    res = check(p, cap, a.textwidth_in, a.dpi)
    for cid, ok, why in res:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {why}")
    if a.json:                                # JSON 在判词行**之前**（见文件头 D6）
        print(json.dumps({c: ok for c, ok, _ in res}, ensure_ascii=False))
    bad = [c for c, ok, _ in res if not ok]
    print(f"RESULT: {'PASS' if not bad else 'FAIL'}" + ("" if not bad else f"（{','.join(bad)}）"))
    sys.exit(0 if not bad else EXIT_FIG_FAIL)


if __name__ == "__main__":
    main()
