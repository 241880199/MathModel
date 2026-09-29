#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A1–A2 探针：SciencePlots 提供的 style 名清单 + 候选底座的 rcParams 全量转储。

复跑（仓根）：
  python tests/m3-plot-recon/a1_style_census.py --site build/m3-plot-recon/site

★ 只读：不改任何既有文件；输出只到 stdout。
★ 隔离：`--site` 指向 `pip install --target` 的目录，脚本自己 sys.path.insert(0, site)，
  绝不把 SciencePlots 装进本机 site-packages（红线）。
"""
import argparse
import pathlib
import sys

CANDIDATES = ["science", "no-latex", "grid", "ieee", "nature", "notebook"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="pip --target 目录")
    ap.add_argument("--dump-keys", default=None,
                    help="若给出，只转储这些 rcParams 键（逗号分隔）；默认全量")
    a = ap.parse_args()

    site = pathlib.Path(a.site).resolve()
    sys.path.insert(0, str(site))

    import matplotlib
    import scienceplots                                     # noqa: F401（注册 style）
    from matplotlib import style, rcParams

    print(f"python          = {sys.version.split()[0]}")
    print(f"matplotlib      = {matplotlib.__version__}  （__file__ = {matplotlib.__file__}）")
    print(f"site inserted   = {site}")
    print(f"style.library 里 SciencePlots 的 style 名 = {len(style.library)} 个条目")
    print("-" * 78)
    for name in sorted(style.library):
        print(f"  {name}")
    print("-" * 78)

    # 候选底座的存在性 + 关键 rcParams
    keys_of_interest = ["text.usetex", "axes.prop_cycle", "font.family", "font.size",
                        "axes.titlesize", "axes.labelsize", "xtick.labelsize",
                        "ytick.labelsize", "legend.fontsize", "lines.linewidth",
                        "lines.markersize", "axes.linewidth", "axes.grid",
                        "axes.spines.top", "axes.spines.right", "xtick.direction",
                        "ytick.direction", "figure.dpi", "savefig.dpi",
                        "figure.figsize", "legend.frameon", "text.latex.preamble"]
    print("候选底座的存在性与关键 rcParams（未列出的 = 该 style 没设，落回 matplotlib 默认）")
    print("-" * 78)
    for cand in CANDIDATES:
        present = cand in style.library
        print(f"[{cand}]  在 style.library 里：{'是' if present else '**否**'}")
        if not present:
            continue
        with style.context(cand):
            for k in keys_of_interest:
                print(f"    {k:<24} = {rcParams[k]!r}")
        print()

    if a.dump_keys:
        want = [k.strip() for k in a.dump_keys.split(",")]
        print("=" * 78)
        print("指定键的默认值 vs 各候选底座的值")
        print("=" * 78)
        for k in want:
            line = [f"{k:<24}", f"default={rcParams_default(k)!r}"]
            for cand in CANDIDATES:
                if cand in style.library:
                    with style.context(cand):
                        line.append(f"{cand}={rcParams[k]!r}")
            print("  ".join(line))


def rcParams_default(k):
    """matplotlib 默认值（不经任何 style）。"""
    import matplotlib
    return matplotlib.rcParamsDefault[k]


if __name__ == "__main__":
    main()
