#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GREEN G3 - R3 district vulnerability composition, paper-ready (horizontal stacked bars).

Scene: tests/skills/figure-choose/red/brief-R3.md (the authoritative copy of the
numbers; the three tiers of each district sum to one).  The chart type matches the
same-scene products of the other two carriers (plot-python / plot-matlab out-G3): a
horizontal stacked bar.

Produced THROUGH the mcm-plot-origin helper
(.claude/skills/mcm-plot-origin/assets/mcmplot_origin.py) for styling / sizing /
export; this script types no style number.

Run:  python tests/skills/plot-origin/green/out-G3/scenario.py
"""
import pathlib
import sys

_REPO = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(_REPO / "build" / "m3-origin-probe" / "site"))
sys.path.insert(0, str(_REPO / ".claude" / "skills" / "mcm-plot-origin" / "assets"))

import originpro as op                                   # noqa: E402
from mcmplot_origin import apply_style, figsize_for, save  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent
TEXTWIDTH_IN = 6.31
DPI = 300

# --- scene numbers, verbatim from brief-R3.md ---
DISTRICTS = ["A", "B", "C", "D", "E", "F"]
LOW = [0.42, 0.31, 0.55, 0.28, 0.37, 0.50]
MEDIUM = [0.35, 0.44, 0.30, 0.47, 0.38, 0.33]
HIGH = [0.23, 0.25, 0.15, 0.25, 0.25, 0.17]

CAPTION = "Figure 3: District vulnerability composition, low to high tiers"

# --- layout constants (judgement layer, NOT style values) ---------------------
LEGEND_GAP_PX = 20.0
LAYER_LEFT, LAYER_WIDTH = 14.0, 82.0
LAYER_TOP, LAYER_HEIGHT = 9.0, 66.0


def _lt_num(expr):
    """Read a LabTalk numeric expression back into Python (page/object geometry)."""
    op.po.LT_execute(f"double __mcm_tmp = {expr};")
    return op.po.LT_get_var("__mcm_tmp")


def legend_above_layer(gap_px=LEGEND_GAP_PX):
    """Lay the legend out as a single row ABOVE the plot box, clear of the data.

    Two separate things, both needed:

    1. **Single row.**  Rewrite ``legend.text$`` with every ``\\l(n)`` swatch and its
       ``%(n)`` name on ONE line.  This build of Origin exposes **no** column /
       direction property on the legend object (probed: every ``numCols`` /
       ``multiCol`` / ``direction`` style name is either rejected or a silent
       no-op), so writing the text is the way to get a horizontal legend.
       The swatches still come from ``\\l(n)`` -- i.e. from each plot's own colour,
       which is the H14 series colour the helper set.  No colour is typed here.
    2. **Position.**  With a stacked bar every in-layer position overlaps a bar, so
       the legend has to sit outside the box.  ``legend.x`` / ``legend.y`` are in
       *axis units* (probed by reading back ``legend.left`` / ``legend.top`` while
       varying them); ``legend.left`` / ``legend.top`` are in page pixels, which is
       far easier to reason about -- so park the box in the top margin with those.
    """
    op.po.LT_execute('legend.text$ = "\\l(1) %(1)   \\l(2) %(2)   \\l(3) %(3)";')
    op.po.LT_execute("legend.showframe = 0;")      # frameless, like the sibling carriers
    page_w, page_h = _lt_num("page.width"), _lt_num("page.height")
    legend_w, legend_h = _lt_num("legend.width"), _lt_num("legend.height")
    box_left = _lt_num("layer.left") / 100.0 * page_w
    box_width = _lt_num("layer.width") / 100.0 * page_w
    box_top = _lt_num("layer.top") / 100.0 * page_h
    op.po.LT_execute(f"legend.left = {box_left + (box_width - legend_w) / 2.0};")
    op.po.LT_execute(f"legend.top = {box_top - gap_px - legend_h};")


def main():
    op.set_show(False)
    try:
        wb = op.new_book("w", "Data")
        ws = wb[0]
        ws.from_list(0, DISTRICTS)
        ws.from_list(1, LOW)
        ws.from_list(2, MEDIUM)
        ws.from_list(3, HIGH)
        op.po.LT_execute(f"win -a {wb};")
        op.po.LT_execute('wks.col2.lname$="low";wks.col3.lname$="medium";wks.col4.lname$="high";')

        # Horizontal stacked bar = plot type "StackBar" (Plot.ogs names it 216).
        page = op.new_graph("G3", template="bar")
        layer = page[0]
        layer.obj.AddPlotFromString(f"{ws.lt_range()}!(1,2:4)", 216)
        layer.group(True, 0, 2)          # group the three tiers so they stack
        layer.rescale()
        layer.axis("x").title = "District"
        layer.axis("y").title = "Share of district area (fraction)"
        layer.set_float("left", LAYER_LEFT)
        layer.set_float("width", LAYER_WIDTH)
        layer.set_float("top", LAYER_TOP)
        layer.set_float("height", LAYER_HEIGHT)

        # `-k 0` on every series, BEFORE apply_style.  Measured on this module's scenes:
        #  * the ORDER is load-bearing -- applied AFTER apply_style the fill comes out
        #    black (first seen on the single-series Bar in G2);
        #  * the CALL is load-bearing -- dropping it HERE takes F2 from 3 to 6 and puts
        #    three out-of-set tints into F5 (both sides measured 2026-10-02, from the
        #    same script).
        for p in layer.plot_list():
            p.set_cmd("-k 0")
        apply_style(page)

        # Pin the page's physical width BEFORE placing the legend: the layer box is
        # positioned in percent of the page, so a later width change moves the box out
        # from under a legend that was parked using its old page-pixel geometry.
        w = figsize_for(TEXTWIDTH_IN)
        page.set_float("width", round(w * page.get_float("resx")))
        legend_above_layer()

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
