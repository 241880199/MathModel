#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A3 探针：端到端渲染 —— 同一份数据在 ① matplotlib 默认 ② `science` ③ `science+no-latex`
三个底座下各出 PNG + PDF，并记录 usetex 的 warning/报错。

复跑（仓根）：
  python tests/m3-plot-recon/a3_render_probe.py --site build/m3-plot-recon/site \
      --out build/m3-plot-recon/a3 --dpi 200

产物落在 `--out`（默认 build/，不入库）；判词由报告里的 check-figure-style.py 命令单独跑。
"""
import argparse
import pathlib
import sys
import traceback
import warnings

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--figsize", default="6.31,2.6")
    ap.add_argument("--caption", default="Figure 1: Sample series")
    a = ap.parse_args()

    sys.path.insert(0, str(pathlib.Path(a.site).resolve()))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    import scienceplots                                     # noqa: F401
    from matplotlib import pyplot as plt

    w, h = (float(x) for x in a.figsize.split(","))
    x = np.linspace(0, 10, 50)
    sets = [(lambda t: np.sin(x + t))(t) for t in (0.0, 0.7, 1.4)]

    bases = {"default": [], "science": ["science"], "science+no-latex": ["science", "no-latex"]}
    print(f"python={sys.version.split()[0]}  matplotlib={matplotlib.__version__}")
    print(f"figsize=({w},{h})  dpi={a.dpi}  caption={a.caption!r}")
    print("=" * 78)
    for name, styles in bases.items():
        recs = []
        with warnings.catch_warnings(record=True) as wlist:
            warnings.simplefilter("always")
            err = None
            try:
                with plt.style.context(styles):
                    plt.rcParams["savefig.dpi"] = a.dpi
                    fig, ax = plt.subplots(figsize=(w, h))
                    for i, y in enumerate(sets):
                        ax.plot(x, y, label=f"s{i}")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("Amplitude (a.u.)")
                    ax.legend(loc="upper right")
                    png = out / f"{name.replace('+', '_')}.png"
                    pdf = out / f"{name.replace('+', '_')}.pdf"
                    fig.savefig(png, dpi=a.dpi)
                    fig.savefig(pdf)
                    plt.close(fig)
            except Exception as e:                          # noqa: BLE001（要如实记录报错）
                err = f"{type(e).__name__}: {e}"
        print(f"[{name}] styles={styles}")
        print(f"    savefig 期间 warnings：{len(wlist)} 条")
        for wi in wlist:
            print(f"      - {wi.category.__name__}: {str(wi.message)[:300]}")
        print(f"    渲染异常：{err}")
        if err:
            print(traceback.format_exc())
        if not err:
            for f in (png, pdf):
                print(f"    产物 {f.name}  {f.stat().st_size} 字节")
        print()


if __name__ == "__main__":
    main()
