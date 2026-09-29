#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D11 探针：**端到端最小回路** —— 一份**朴素 matplotlib 出图脚本**（RED 候选：
默认色序 · 图偏宽 · 图注很长且以句号结尾）→ 出 PNG + PDF → 跑 `check-figure-style.py`。

不 import 任何 SciencePlots（这是"朴素写手"那一态），用本机默认 matplotlib。

复跑（仓根）：
  python tests/m3-plot-recon/d11_red_loop.py --out build/m3-plot-recon/d11
  python tests/skills/figure-choose/check-figure-style.py \
      --fig build/m3-plot-recon/d11/naive.pdf \
      --caption "Figure 1. This figure shows the simulated concentration of the species over time for all six parameter settings under baseline conditions." \
      --textwidth-in 6.31
"""
import argparse
import pathlib
import subprocess
import sys

import numpy as np

# 朴素写手的图注：**没有 ASCII 冒号**（用句点）、**很长**、**句末有句号**
CAPTION = ("Figure 1. This figure shows the simulated concentration of the species over time "
           "for all six parameter settings under baseline conditions.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--textwidth", type=float, default=6.31)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    x = np.linspace(0, 10, 80)
    fig, ax = plt.subplots(figsize=(9.0, 3.0))            # 图偏宽
    for i in range(6):                                   # 6 条序列 ⇒ 默认色序 6 色
        ax.plot(x, np.sin(x + i / 3) * (1 + i / 10), label=f"run {i + 1}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Concentration (mol/L)")
    ax.legend(loc="upper right", ncol=3, fontsize=7)
    png, pdf = out / "naive.png", out / "naive.pdf"
    fig.savefig(png, dpi=a.dpi)
    fig.savefig(pdf)
    plt.close(fig)
    (out / "caption.txt").write_bytes(CAPTION.encode("utf-8"))

    print(f"matplotlib = {matplotlib.__version__}（本机默认，未插 site 路径）")
    print(f"figsize = (9.0, 3.0)  dpi = {a.dpi}")
    print(f"产物：{png}（{png.stat().st_size} B）· {pdf}（{pdf.stat().st_size} B）")
    print(f"图注：{CAPTION!r}")
    print("=" * 78)
    base = ["python", "tests/skills/figure-choose/check-figure-style.py"]
    common = ["--caption", CAPTION, "--textwidth-in", str(a.textwidth)]
    for label, cmd in (("PNG", base + ["--fig", str(png), "--dpi", str(a.dpi)] + common),
                       ("PDF", base + ["--fig", str(pdf)] + common)):
        print(f"$ {' '.join(cmd)}")
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(pathlib.Path.cwd()))
        print(p.stdout.rstrip() or p.stderr.rstrip())
        print(f"  ⇒ exit = {p.returncode}\n")


if __name__ == "__main__":
    sys.exit(main())
