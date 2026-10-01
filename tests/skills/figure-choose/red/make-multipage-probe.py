#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§6 遗留风险 #2 的探针生成器：一张**两页** PDF，用来实测"检查器只判第 1 页"。

产物 `multipage-probe.pdf` 的构造（数字全部打印出来，可当场复核）：
  · page 1：**一张合规图** —— 6.31 in 宽（= 本仓 `--textwidth-in 6.31` 的分母 ⇒ F1 比值恰 1.000）、
            **白底**（F4 过）、**一个 H14 色**（F5 过）、彩色主色数 1（F2 过）、
            无字体（F6 走"未引用任何字体 ⇒ 不适用"那一支）；色带只占页面**下 1/3**
            ⇒ 白底是**明确众数**（不靠平票的运气，见下面 ⚠️）。
  · page 2：**一张越界图** —— 12.00 in 宽 ⇒ F1 比值 1.902（> 1.20，本该红）、
            6 个彩色主色铺满整页 ⇒ F2 = 6（> 4，本该红）；底色非白、色序非 H14
            ⇒ F4/F5 在它上面也该红。
⇒ 若检查器报 `RESULT: PASS`，就证明它只读了 `doc[0]`
  （**F1 / F2 / F4 / F5 都只读第 1 页**，page2 及以后整页在射程外）。

★ **Task 3b 修 ① 的由来**（为什么 page1 必须是合规图）：
  page1 原先**整页铺一个非 H14 的红底**（`#f03b20`，众数亮度 109 < `BG_MIN_LUMA`=136）。
  `F4`/`F5` 落地后，**那种 page1 自己就红** ⇒ 整份判 `FAIL（F4,F5）` ⇒
  `house-style.md` §0 的"整份仍判 PASS（`probe_verdict` = PASS）"**成假**，
  把 `G-F0-verdict`（那个"文档 vs 实测"的钉）连带打红，并连带 `C1`/`C2` 双双 RED-BAD。
  现把 page1 改成**合规图**：§0 那句恢复为真，而且"只读 `doc[0]`"这件事
  从 `F1`/`F2` **扩到 `F1`/`F2`/`F4`/`F5`**（page2 在四条判据上都越界）。
  ⇒ **改这个脚本时必须让 page1 继续六条全过**，否则 §0 与 `G-F0-verdict` 会再次翻转。

色块用满幅矩形铺，故每个颜色在 `check-figure-style.py` 的 320x320 采样上都远大于
0.5% 地板（不会被地板刷掉），色数即矩形个数。

写入用 `savefig`（二进制输出，非 `write_text`）；PDF 的 `CreationDate` 固定，
故本脚本可重复跑出**逐字节相同**的探针（自带自证：跑两次比 blob）。
用法：python tests/skills/figure-choose/red/make-multipage-probe.py
      自带自证：--twice 会连跑两次并比对 git blob。
"""
import datetime
import pathlib
import subprocess
import sys

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle

RED = pathlib.Path(__file__).resolve().parent
OUT = RED / "multipage-probe.pdf"
REL = "tests/skills/figure-choose/red/multipage-probe.pdf"   # 输出里只写仓库相对路径

PAGE1_IN, PAGE2_IN = 6.31, 12.00            # 两页宽度（英寸）：第 1 页合规格、第 2 页越界
# 每页 = (宽度 in, 色带列表, 色带占页面高度的比例)
#   page1：**1 个 H14 色**（`#0072B2`）只占下 1/3 高 ⇒ 白底是明确众数、F4 过；
#          `#0072B2` 的选法有实测依据：八色逐个过一遍 matplotlib→PDF→栅格化，
#          只有这一族的 7 个（除 `#4D4D4D`）回来仍是**同一个 hex**（F5 是精确比对）。
#   page2：6 个非 H14 色、**铺满整页**（与修 ① 之前逐字相同 ⇒ page2 的两项读数不变）。
PAGES = ((PAGE1_IN, ["#0072B2"], 1 / 3),
         (PAGE2_IN, ["#f03b20", "#31a354", "#3182bd", "#756bb1", "#e6550d", "#c51b8a"], 1.0))
CHECKER = RED.parent / "check-figure-style.py"
CAPTION = "Figure 1: A two page probe"      # 与 `house-metrics.py::_probe_verdict` 传的**逐字相同**
ROOT = RED.resolve().parents[3]


def build(path):
    """两页 PDF。每页一个色带图，页盒 = figsize（matplotlib 不用 bbox_inches）。"""
    with PdfPages(
            path, metadata={"CreationDate": datetime.datetime(2026, 1, 1, 0, 0, 0)}) as pdf:
        for width, colors, cover in PAGES:
            fig = plt.figure(figsize=(width, 2.0))          # 底色白（matplotlib 默认）
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis("off")
            n = len(colors)
            for i, c in enumerate(colors):
                ax.add_patch(Rectangle((i / n, 0), 1 / n, cover, facecolor=c,
                                       edgecolor="none"))
            pdf.savefig(fig)
            plt.close(fig)


def blob(path):
    return subprocess.run(["git", "hash-object", str(path)], cwd=RED,
                          capture_output=True, text=True, check=True).stdout.strip()


def report(path):
    """逐页实测：页盒宽（英寸）、F1 比值、彩色主色数（用检查器本体的函数）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "check_figure_style", RED.parent / "check-figure-style.py")
    cs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cs)
    from PIL import Image
    with fitz.open(path) as doc:
        print(f"pages = {doc.page_count}   file = {path.name}   bytes = {path.stat().st_size}")
        for i in range(doc.page_count):
            w = doc[i].rect.width / 72.0
            pm = doc[i].get_pixmap(dpi=cs.RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
            im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
            print(f"  page{i + 1}: width={w:.3f} in -> ratio {w / PAGE1_IN:.3f}"
                  f"  |  彩色主色数 = {cs.color_count(im)}")


def verdict_check(path):
    """整份探针在**出货检查器**下判 PASS 吗 —— 这是 `house-style.md` §0 那句"整份仍判 PASS"
    与守卫 `G-F0-verdict` 的**同一支仪器**（`house-metrics.py --metric probe_verdict` 内部
    跑的就是这条命令、传的就是下面这个图注）。**这里只印一行结论**，逐条判词见 §6 的第二块。
    """
    p = subprocess.run([sys.executable, str(CHECKER), "--fig", str(path),
                        "--caption", CAPTION, "--textwidth-in", str(PAGE1_IN)],
                       capture_output=True, text=True, cwd=str(ROOT))
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "(无判词)"
    print(f"verdict(probe_verdict) = {last.replace('RESULT: ', '')}")


def main():
    build(OUT)
    print(f"wrote {REL}  blob={blob(OUT)}")
    report(OUT)
    verdict_check(OUT)
    if "--twice" in sys.argv:
        first = blob(OUT)
        build(OUT)
        print(f"rerun  blob={blob(OUT)}  identical={first == blob(OUT)}")


if __name__ == "__main__":
    main()
