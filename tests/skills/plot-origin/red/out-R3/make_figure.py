#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Figure for brief R3 -- vulnerability composition of six districts.

Regenerates ``figure.png`` from the six districts x three vulnerability tiers
share table.  The figure is a 100% stacked column chart drawn with OriginPro
2026 through the ``originpro`` Python package.

Usage:  python make_figure.py

No network access is required and there are no manual steps.  The script always
calls ``op.exit()`` so that no stray ``Origin64.exe`` process is left behind.
"""

from __future__ import annotations

import os
import sys

# --------------------------------------------------------------------------
# OriginPro is installed in a separate "site" directory on this machine.
# --------------------------------------------------------------------------
_ORIGIN_SITE = r"D:\Projects\数学建模\build\m3-origin-probe\site"
if os.path.isdir(_ORIGIN_SITE) and _ORIGIN_SITE not in sys.path:
    sys.path.insert(0, _ORIGIN_SITE)

import originpro as op  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FIGURE_PNG = os.path.join(HERE, "figure.png")
FIGURE_PDF = os.path.join(HERE, "figure.pdf")
FIGURE_WIDTH_PX = 1950  # 6.5 in at 300 dpi

# --------------------------------------------------------------------------
# Data -- straight from the brief.  Within every district the three shares
# sum to 1.00.
# --------------------------------------------------------------------------
DISTRICTS = ["A", "B", "C", "D", "E", "F"]
TIERS = [
    # (long name, shares, fill colour) -- ordered bottom-of-column upwards.
    # Sequential single-hue ramp (light -> dark = low -> high vulnerability).
    ("Low", [0.42, 0.31, 0.55, 0.28, 0.37, 0.50], "#FEE8C8"),
    ("Medium", [0.35, 0.44, 0.30, 0.47, 0.38, 0.33], "#FDBB84"),
    ("High", [0.23, 0.25, 0.15, 0.25, 0.25, 0.17], "#E34A33"),
]

# Graph page width, in Origin page units (1/600 inch) -> 6.5 in wide, i.e. the
# text width of a single-column paper.  Keeping the page at its native ~10.8 in
# would shrink the 9-10 pt labels to ~5.5 pt once the figure is scaled down.
PAGE_W = 3900
# Plot layer inside the page, in percent of page.
LAYER_LEFT, LAYER_TOP, LAYER_W, LAYER_H = 12.0, 12.0, 62.0, 74.0
# Gap between the right edge of the page and the legend, in page units.
LEGEND_MARGIN = 100
# Point sizes: true size at 6.5 in wide, i.e. readable at print scale.
TICK_PT, TITLE_PT, LEGEND_PT = 9, 10, 9


def build_data():
    """Write the brief's table into a worksheet and return it."""
    wks = op.new_sheet("w", "Vulnerability composition")
    wks.from_list(0, DISTRICTS, "District")
    for i, (name, shares, _colour) in enumerate(TIERS, start=1):
        wks.from_list(i, shares, name)
    return wks


def draw(wks):
    """Create the 100% stacked column graph and return its GPage."""
    # Column 1 is the (categorical) X axis, columns 2:4 are the three Y series;
    # plot type 213 is Origin's "100% stacked column".
    script = "plotxy iy:=%(range)s!(1,2:4) plot:=213;" % {"range": wks.lt_range()}
    if not op.lt_exec(script):
        raise RuntimeError("Origin could not create the 100% stacked column plot")

    gp = op.find_graph()
    if gp is None:
        raise RuntimeError("no active graph after plotxy")
    return gp


def style(gp):
    """Apply the paper-ready styling."""
    gl = gp[0]

    # --- page geometry ------------------------------------------------------
    # The graph template keeps a fixed page aspect ratio (sqrt(2), as for A4),
    # so setting the width also fixes the height.
    op.lt_exec("page.width=%d;" % PAGE_W)
    page_w = gp.get_float("width")
    page_h = gp.get_float("height")

    # --- explicit colour order (bottom -> top: Low, Medium, High) ----------
    for plot, (_name, _shares, colour) in zip(gl.plot_list(), TIERS):
        plot.color = colour

    # --- axes ---------------------------------------------------------------
    gl.set_float("width", LAYER_W)
    gl.set_float("height", LAYER_H)
    gl.set_float("left", LAYER_LEFT)
    gl.set_float("top", LAYER_TOP)

    yax = gl.axis("y")
    yax.title = "Share of district area"
    yax.set_limits(0.0, 1.0, 0.2)  # the three shares always sum to 1.00
    gl.axis("x").title = "District"

    # --- fonts --------------------------------------------------------------
    # Only the point sizes are set.  No face is forced: on this machine the
    # Origin page default (SimSun) is what both carriers actually embed -
    # assigning a face name via LabTalk (layer.x.label.font$) leaves the
    # exported PDF unchanged, and the face index (layer.x.label.font) is
    # machine-specific, so forcing either would make the output fragile.
    op.lt_exec(
        "layer.x.label.pt=%(tick)d; layer.y.label.pt=%(tick)d;"
        "layer.x.title.pt=%(title)d; layer.y.title.pt=%(title)d;"
        "legend.pt=%(legend)d;"
        % {"tick": TICK_PT, "title": TITLE_PT, "legend": LEGEND_PT}
    )

    # --- legend: outside the plot frame, to the right -----------------------
    legend = gl.label("legend")
    if legend is not None:
        # Low -> Medium -> High, matching the bottom-to-top stacking order.
        # (\l(n) draws the symbol of the n-th data plot.)
        legend.text = "\r\n".join(
            "\\l(%d) %s" % (i, name) for i, (name, _s, _c) in enumerate(TIERS, 1)
        )
        legend.show = True
        legend_w = legend.get_float("width")
        legend_h = legend.get_float("height")
        legend.set_float("left", page_w - legend_w - LEGEND_MARGIN)
        legend.set_float("top", 0.5 * (page_h - legend_h))


def export(gp):
    """Write the same rendered figure to both carriers: raster PNG and PDF."""
    if not gp.save_fig(FIGURE_PNG, type="png", width=FIGURE_WIDTH_PX):
        raise RuntimeError("Origin could not export the PNG figure")
    if not gp.save_fig(FIGURE_PDF, type="pdf"):
        raise RuntimeError("Origin could not export the PDF figure")


def main():
    op.set_show(False)  # Origin runs hidden
    wks = build_data()
    gp = draw(wks)
    style(gp)
    export(gp)


if __name__ == "__main__":
    try:
        main()
    finally:
        op.exit()
