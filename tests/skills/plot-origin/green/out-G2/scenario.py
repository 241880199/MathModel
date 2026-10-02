#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GREEN G2 - R2 drivers of historical disaster counts (horizontal bars).

Scene: tests/skills/figure-choose/red/brief-R2.md (the authoritative copy of the
numbers).  The chart type matches the same-scene products of the other two carriers
(plot-python / plot-matlab out-G2): one horizontal bar per attribute, showing its
Pearson r with the historical disaster count, ordered by r.

Produced THROUGH the mcm-plot-origin helper
(.claude/skills/mcm-plot-origin/assets/mcmplot_origin.py) for styling / sizing /
export; this script types no style number.

Run:  python tests/skills/plot-origin/green/out-G2/scenario.py
"""
import pathlib
import sys

import numpy as np

_REPO = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(_REPO / "build" / "m3-origin-probe" / "site"))
sys.path.insert(0, str(_REPO / ".claude" / "skills" / "mcm-plot-origin" / "assets"))

import originpro as op                                   # noqa: E402
from mcmplot_origin import apply_style, figsize_for, save  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent
TEXTWIDTH_IN = 6.31
DPI = 300

# --- scene numbers, verbatim from brief-R2.md (rows A-F) ---
ATTRIBUTES = [
    ("Population density", [820, 640, 610, 1210, 990, 1750]),
    ("Mean slope", [3.2, 11.5, 2.4, 14.8, 7.1, 5.0]),
    ("Vegetation cover", [0.61, 0.58, 0.72, 0.41, 0.49, 0.55]),
    ("Infrastructure index", [74, 72, 81, 55, 66, 70]),
]
DISASTER = np.array([12, 31, 8, 38, 16, 24])

CAPTION = "Figure 2: Attribute correlations with historical disaster count"


def main():
    # Pearson r of each attribute with the disaster count, ascending (as in the
    # same-scene products of the other carriers).
    r = {name: float(np.corrcoef(np.array(vals), DISASTER)[0, 1]) for name, vals in ATTRIBUTES}
    order = sorted(r, key=lambda k: r[k])
    names = order
    values = [r[k] for k in order]

    op.set_show(False)
    try:
        wb = op.new_book("w", "Data")
        ws = wb[0]
        ws.from_list(0, names)
        ws.from_list(1, values)
        op.po.LT_execute(f"win -a {wb};")

        # Horizontal bar = plot type "Bar" (Plot.ogs names it 215); the bar template
        # gives the standard layout (value axis along the bottom).
        page = op.new_graph("G2", template="bar")
        layer = page[0]
        layer.obj.AddPlotFromString(f"{ws.lt_range()}!(1,2)", 215)
        layer.rescale()
        layer.axis("y").title = "Pearson r with historical disaster count"
        # widen the left margin so the attribute names are not clipped
        layer.set_float("left", 28.0)
        layer.set_float("width", 60.0)
        layer.set_float("top", 9.0)
        layer.set_float("height", 66.0)
        # a single-series bar needs no legend
        op.po.LT_execute("legend -d;")
        op.po.LT_execute("label -r legend;")

        # `-k 0` on every series, BEFORE apply_style.  Measured on this module's scenes:
        #  * the ORDER is load-bearing -- applied AFTER apply_style the fill comes out
        #    black (first seen on this single-series Bar);
        #  * the CALL is load-bearing -- dropping it on the G3 bar scene takes F2 from
        #    3 to 6 and puts three out-of-set tints into F5 (both sides measured
        #    2026-10-02, from the same script).
        for p in layer.plot_list():
            p.set_cmd("-k 0")
        apply_style(page)

        w = figsize_for(TEXTWIDTH_IN)
        page.set_float("width", round(w * page.get_float("resx")))

        png = save(page, OUT / "figure.png", DPI)
        pdf = save(page, OUT / "figure.pdf")
        print("png actual width in:", png["actual_width_in"])
        print("pdf actual width in:", pdf["actual_width_in"])

        (OUT / "caption.txt").write_bytes(CAPTION.encode("utf-8"))
        print(f"wrote {OUT}/figure.png, figure.pdf, caption.txt")
    finally:
        op.exit()


if __name__ == "__main__":
    main()
