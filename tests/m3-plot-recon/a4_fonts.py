#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A4 探针：字体回退 + 缺字 warning + 中文字符（只报事实）。

复跑（仓根）：
  python tests/m3-plot-recon/a4_fonts.py --site build/m3-plot-recon/site \
      --out build/m3-plot-recon/a4
"""
import argparse
import pathlib
import sys
import warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(pathlib.Path(a.site).resolve()))
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    import scienceplots                                     # noqa: F401（注册 style 名）
    from matplotlib import font_manager as fm
    import matplotlib.pyplot as plt
    from matplotlib import rcParams

    print(f"matplotlib={matplotlib.__version__}")
    print(f"font_manager 扫到的字体族数 = {len(fm.fontManager.ttflist)}")
    fams = sorted({f.name for f in fm.fontManager.ttflist})
    print(f"不同字体族名 {len(fams)} 个：")
    for n in fams:
        print(f"  {n}")

    print("-" * 78)
    print("与 newtx（Times 系正文）可能对齐的候选：")
    for probe in ["Times New Roman", "Times", "Nimbus Roman", "Liberation Serif",
                  "STIXGeneral", "STIX Two Text", "TeX Gyre Termes", "DejaVu Serif",
                  "DejaVu Sans", "Cambria", "SimSun", "Microsoft YaHei", "SimHei",
                  "Arial", "Helvetica"]:
        try:
            p = fm.findfont(fm.FontProperties(family=probe), fallback_to_default=False)
            print(f"  {probe:<20} 命中 {p}")
        except Exception as e:                              # noqa: BLE001
            print(f"  {probe:<20} **未命中**（{type(e).__name__}）")

    print("-" * 78)
    print("中文 / CJK 缺失字符的 warning 实测（默认字体族下画中文轴标签）：")
    for styles, tag in (([], "default"), (["science", "no-latex"], "science+no-latex")):
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            with plt.style.context(styles):
                fig, ax = plt.subplots(figsize=(4, 2.5))
                ax.plot([0, 1], [0, 1])
                ax.set_xlabel("时间 (秒)")
                ax.set_ylabel("振幅")
                ax.set_title("中文标题")
                p = out / f"cjk_{tag.replace('+', '_')}.png"
                fig.savefig(p, dpi=150)
                plt.close(fig)
        miss = [str(w.message) for w in wl if "missing from font" in str(w.message).lower()
                or "Glyph" in str(w.message)]
        print(f"  [{tag}] warnings 共 {len(wl)} 条 · 缺字相关 {len(miss)} 条")
        for m in miss[:3]:
            print(f"      {m[:160]}")


if __name__ == "__main__":
    main()
