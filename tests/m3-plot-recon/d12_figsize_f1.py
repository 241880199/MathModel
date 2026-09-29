#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D12 探针：`figsize` 与 F1 读数的对应关系。

固定 figsize / dpi，扫 `bbox_inches ∈ {None(默认), 'tight'}` × `pad_inches ∈ {默认, 0.05, 0.1, 0.0}`，
量 **PNG 像素宽 ÷ dpi** 与 **PDF 页盒宽**，并与 `--textwidth-in`（本项目惯例 6.31）比对 ⇒ 复算 F1 比值。

复跑（仓根）：
  python tests/m3-plot-recon/d12_figsize_f1.py --site build/m3-plot-recon/site \
      --out build/m3-plot-recon/d12 --dpi 200 --textwidth 6.31 --figsize 6.31,2.6
  python tests/m3-plot-recon/d12_figsize_f1.py --site build/m3-plot-recon/site \
      --out build/m3-plot-recon/d12 --styles science,no-latex --figsize 7.2,2.6
"""
import argparse
import pathlib
import sys

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--textwidth", type=float, default=6.31)
    ap.add_argument("--figsize", default="6.31,2.6")
    ap.add_argument("--styles", default="", help="逗号分隔的 style 名（空 = matplotlib 默认）")
    a = ap.parse_args()
    sys.path.insert(0, str(pathlib.Path(a.site).resolve()))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    import scienceplots                                     # noqa: F401（注册 style 名）
    from matplotlib import pyplot as plt

    styles = [s for s in a.styles.split(",") if s]
    with plt.style.context(styles):
        _sweep(a, out, styles)


def _sweep(a, out, styles):
    import matplotlib
    from matplotlib import pyplot as plt
    from PIL import Image
    import fitz

    w, h = (float(s) for s in a.figsize.split(","))
    x = np.linspace(0, 10, 60)
    print(f"matplotlib={matplotlib.__version__}  styles={styles or '(默认)'}  "
          f"目标 figsize=({w},{h})  dpi={a.dpi}  textwidth={a.textwidth} in")
    hdr = (f"{'bbox_inches':<12} {'pad_inches':<11} {'PNG px宽':>9} {'PNG宽/dpi':>10} "
           f"{'F1(PNG)':>8} {'PDF页盒宽':>10} {'F1(PDF)':>8}")
    print(hdr)
    print("-" * len(hdr))
    for bname, bbox in (("default", None), ("tight", "tight")):
        for pname, pad in (("default", None), (0.05, 0.05), (0.1, 0.1), (0.0, 0.0)):
            kw = {}
            if bbox is not None:
                kw["bbox_inches"] = bbox
            if pad is not None:
                kw["pad_inches"] = pad
            fig, ax = plt.subplots(figsize=(w, h))
            ax.plot(x, np.sin(x), label="s0")
            ax.plot(x, np.cos(x), label="s1")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude (a.u.)")
            ax.legend(loc="upper right")
            tag = f"{bname}_{pname}"
            png, pdf = out / f"{tag}.png", out / f"{tag}.pdf"
            fig.savefig(png, dpi=a.dpi, **kw)
            fig.savefig(pdf, **kw)
            plt.close(fig)
            with Image.open(png) as im:
                pxw = im.size[0]
            with fitz.open(pdf) as doc:
                pdfw = doc[0].rect.width / 72.0
            pngin = pxw / a.dpi
            print(f"{bname:<12} {str(pname):<11} {pxw:>9} {pngin:>10.3f} "
                  f"{pngin / a.textwidth:>8.3f} {pdfw:>10.3f} {pdfw / a.textwidth:>8.3f}")
    print()
    print(f"F1 绿区（分母 {a.textwidth}）: "
          f"{0.80 * a.textwidth:.3f} <= 输出宽 <= {1.20 * a.textwidth:.3f} in")


if __name__ == "__main__":
    main()
