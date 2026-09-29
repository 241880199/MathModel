#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A2 补充探针：候选底座在 `style.library[...]` 里的**原始 dict**（逐键，不是合并后的）、
prop_cycle 与 matplotlib 默认色序的同一性、以及组合用法 `['science','no-latex']` 的落地值。

复跑（仓根）：
  python tests/m3-plot-recon/a2_style_raw_dump.py --site build/m3-plot-recon/site
"""
import argparse
import pathlib
import sys

CANDS = ["science", "no-latex", "grid", "ieee", "nature", "notebook"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(pathlib.Path(a.site).resolve()))

    import matplotlib
    import scienceplots                                     # noqa: F401
    from matplotlib import style, rcParams, rcParamsDefault

    dflt_cyc = rcParamsDefault["axes.prop_cycle"]
    print(f"matplotlib {matplotlib.__version__}")
    print(f"matplotlib 默认 axes.prop_cycle 的颜色数 = {len(dflt_cyc)}")
    print(f"matplotlib 默认色序（前 3）= {list(dflt_cyc)[:3]}")
    print("=" * 78)
    for c in CANDS:
        d = style.library[c]
        print(f"--- style.library[{c!r}] 原始 dict · {len(d)} 键 ---")
        for k in sorted(d):
            print(f"    {k:<26} = {d[k]!r}")
        cyc = d.get("axes.prop_cycle")
        if cyc is None:
            print("    ## 本 style **未设** axes.prop_cycle ⇒ 落回默认")
        else:
            same = list(cyc) == list(dflt_cyc)
            print(f"    ## axes.prop_cycle 与 matplotlib 默认色序**逐项相同**？ {same}")
        print()

    print("=" * 78)
    print("组合用法（SciencePlots 的推荐写法就是列多个 style）在**落地后**的关键键：")
    combos = [["science"], ["science", "no-latex"], ["science", "no-latex", "grid"],
              ["science", "ieee"], ["science", "nature"], ["science", "notebook"]]
    keys = ["text.usetex", "axes.prop_cycle", "font.family", "font.size",
            "lines.linewidth", "axes.spines.top", "axes.spines.right",
            "xtick.direction", "axes.grid", "figure.figsize",
            "text.latex.preamble"]
    for cb in combos:
        with style.context(cb):
            same = list(rcParams["axes.prop_cycle"]) == list(dflt_cyc)
            print(f"[{'+'.join(cb)}]")
            print(f"    axes.prop_cycle ≡ matplotlib 默认色序？ {same}")
            for k in keys:
                if k == "axes.prop_cycle":
                    continue
                print(f"    {k:<22} = {rcParams[k]!r}")
        print()

    print("=" * 78)
    print("`science` 相对 matplotlib 默认**改动的全部键**（合并后逐键 diff）：")
    with style.context(["science"]):
        cur = dict(rcParams)
    changed = sorted(k for k in cur
                     if repr(cur[k]) != repr(rcParamsDefault[k]))
    print(f"改动键数 = {len(changed)}")
    for k in changed:
        print(f"    {k:<26} default={rcParamsDefault[k]!r}")
        print(f"    {'':<26} science={cur[k]!r}")


if __name__ == "__main__":
    main()
