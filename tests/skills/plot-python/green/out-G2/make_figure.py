#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GREEN G2 - R2 drivers of historical disaster counts

场景 R2（`tests/skills/figure-choose/red/brief-R2.md`）：各属性与灾害数的相关系数条。

由 mcmplot（`.claude/skills/mcm-plot-python/assets/mcmplot.py`）出图：
套样式 -> figsize_for(textwidth_in) -> save()。分母 TEXTWIDTH_IN 与送进
check-figure-style.py 的 --textwidth-in 逐字同值（本仓演示口径）。
产物：figure.png / figure.pdf（两载体同源）；caption.txt 供检查器 --caption @file。
"""

import pathlib
import sys

_REPO = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(_REPO / ".claude" / "skills" / "mcm-plot-python" / "assets"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import mcmplot

OUT = pathlib.Path(__file__).resolve().parent
TEXTWIDTH_IN = 6.31   # 正文栏宽分母（本仓演示口径）；判据侧 --textwidth-in 同值
DPI = 200             # 保存即送检的 dpi（两处逐字一致）

CAPTION = 'Figure 2: Correlation of district attributes with historical disaster count'


def main():

    mcmplot.apply_style()
    factors = {
        "Population density": [820, 640, 610, 1210, 990, 1750],
        "Mean slope": [3.2, 11.5, 2.4, 14.8, 7.1, 5.0],
        "Vegetation cover": [0.61, 0.58, 0.72, 0.41, 0.49, 0.55],
        "Infrastructure index": [74, 72, 81, 55, 66, 70],
    }
    disaster = np.array([12, 31, 8, 38, 16, 24])
    names = list(factors)
    r = [float(np.corrcoef(np.array(factors[k]), disaster)[0, 1]) for k in names]
    order = sorted(range(len(names)), key=lambda i: r[i])
    names_s = [names[i] for i in order]
    r_s = [r[i] for i in order]

    fig, ax = plt.subplots(figsize=mcmplot.figsize_for(TEXTWIDTH_IN), layout="constrained")
    # 底座的 xtick.top / ytick.right 曾让上/右留下悬空刻度（这一笔当初是亲眼看图逼出来的）。
    # 缺口① 已由 mcm.mplstyle 显式置 False 处置 ⇒ 这行现在是**冗余的保底**：本机实测把它删掉
    # 重跑，产出的 PNG 逐字节不变（对产物无影响，留作双保险）。
    ax.tick_params(top=False, right=False)
    bars = ax.barh(names_s, r_s, height=0.62)
    # 判断层的一笔：把最强的那一根挑出来上色（mean slope，r = +0.93，见 truth.py）。
    # 取色**从落地后的显式色序里取**（不手写 hex ⇒ 单源 = H14）：F5 要求图上显著色**精确命中**
    # H14 集合，而这里原先写的是底座**旧**调色板的第 4 色 `#FF2C00` ⇒ 重生成后 F5 判红
    # （Task 4 落地显式色序时暴露；见 task-m3-style-t4-report.md）。
    _h14 = plt.rcParams["axes.prop_cycle"].by_key()["color"]   # apply_style() 已落地的 H14
    strongest = names.index("Mean slope")
    bars[order.index(strongest)].set_color(_h14[5])            # H14 的第 6 色（偏红那一档）
    ax.axvline(0.0, color="0.4", lw=0.6)
    ax.set_xlabel("Pearson r with historical disaster count")
    ax.set_xlim(-1.0, 1.0)
    mcmplot.save(fig, OUT / "figure.png", DPI)
    mcmplot.save(fig, OUT / "figure.pdf", DPI)
    plt.close(fig)
    (OUT / "caption.txt").write_bytes(CAPTION.encode("utf-8"))
    print(f"wrote {OUT}/figure.png, figure.pdf, caption.txt")


if __name__ == "__main__":
    main()
