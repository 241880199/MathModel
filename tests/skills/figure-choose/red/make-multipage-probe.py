#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§6 遗留风险 #2 的探针生成器：一张**两页** PDF，用来实测"检查器只判第 1 页"。

产物 `multipage-probe.pdf` 的构造（数字全部打印出来，可当场复核）：
  · page 1：6.31 in 宽（= 本仓 `--textwidth-in 6.31` 的分母 ⇒ F1 比值恰 1.000），
            整页 1 个彩色主色 ⇒ F2 应为 1
  · page 2：12.00 in 宽 ⇒ F1 比值 1.902（> 1.20，本该红），
            6 个彩色主色 ⇒ F2 应为 6（> 4，本该红）
⇒ 若检查器报 `RESULT: PASS`，就证明它只读了 `doc[0]`（**F1 与 F2 都只读第 1 页**）。

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
PAGES = ((PAGE1_IN, ["#f03b20"]),           # page 1: 1 个彩色主色
         (PAGE2_IN, ["#f03b20", "#31a354", "#3182bd", "#756bb1", "#e6550d", "#c51b8a"]))


def build(path):
    """两页 PDF。每页一个满幅色带图，页盒 = figsize（matplotlib 不用 bbox_inches）。"""
    with PdfPages(
            path, metadata={"CreationDate": datetime.datetime(2026, 1, 1, 0, 0, 0)}) as pdf:
        for width, colors in PAGES:
            fig = plt.figure(figsize=(width, 2.0))
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis("off")
            n = len(colors)
            for i, c in enumerate(colors):
                ax.add_patch(Rectangle((i / n, 0), 1 / n, 1, facecolor=c,
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


def main():
    build(OUT)
    print(f"wrote {REL}  blob={blob(OUT)}")
    report(OUT)
    if "--twice" in sys.argv:
        first = blob(OUT)
        build(OUT)
        print(f"rerun  blob={blob(OUT)}  identical={first == blob(OUT)}")


if __name__ == "__main__":
    main()
