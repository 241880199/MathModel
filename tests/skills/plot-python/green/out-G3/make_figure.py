#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GREEN G3 - R3 district vulnerability composition, paper-ready

场景 R3（`tests/skills/figure-choose/red/brief-R3.md`）：同上数据，论文正文宽单栏。

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

CAPTION = 'Figure 3: Vulnerability composition by district, paper-ready'


def main():

    mcmplot.apply_style()
    districts = ["A", "B", "C", "D", "E", "F"]
    low = [0.42, 0.31, 0.55, 0.28, 0.37, 0.50]
    medium = [0.35, 0.44, 0.30, 0.47, 0.38, 0.33]
    high = [0.23, 0.25, 0.15, 0.25, 0.25, 0.17]

    fig, ax = plt.subplots(figsize=mcmplot.figsize_for(TEXTWIDTH_IN), layout="constrained")
    # 亲眼看图逼出的一笔：apply_style() 把 xtick.top/ytick.right 打开（science 底座），
    # 而 mcm.mplstyle 关了对应边框线 ⇒ 上/右会留下悬空刻度。这里在轴级关掉。
    ax.tick_params(top=False, right=False)
    y = np.arange(len(districts))
    left = np.zeros(len(districts))
    for vals, label in ((low, "low"), (medium, "medium"), (high, "high")):
        # 不描白边：水平短条的描边抗锯齿会与白底混出浅色，PNG 上把 F2 抬到 5
        # （同一张图的 PDF 读作 3）—— 见 green/README.md 的载体敏感性一节。
        ax.barh(y, vals, left=left, height=0.62, label=label)
        left = left + np.array(vals)
    ax.set_yticks(y)
    ax.set_yticklabels(districts)
    ax.set_xlabel("Share of district area")
    ax.set_xlim(0.0, 1.0)
    ax.legend(loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.14))
    mcmplot.save(fig, OUT / "figure.png", DPI)
    mcmplot.save(fig, OUT / "figure.pdf", DPI)
    plt.close(fig)
    (OUT / "caption.txt").write_bytes(CAPTION.encode("utf-8"))
    print(f"wrote {OUT}/figure.png, figure.pdf, caption.txt")


if __name__ == "__main__":
    main()
