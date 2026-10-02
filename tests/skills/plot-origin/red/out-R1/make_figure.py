# -*- coding: utf-8 -*-
"""Regenerate the R1 figure: vulnerability composition of six districts.

A 100% stacked column chart is built in Origin: one column per district, split
into the low / medium / high vulnerability tiers, with the three shares of
every district summing to 100 %.

Deterministic, offline, no manual steps:
    python make_figure.py

Outputs (next to this script):
    figure.pdf, figure.png
"""

import os
import sys

# --- environment: locate the locally installed originpro package ----------
SITE = r"D:\Projects\数学建模\build\m3-origin-probe\site"
if os.path.isdir(SITE) and SITE not in sys.path:
    sys.path.insert(0, SITE)

import originpro as op  # noqa: E402

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PDF = os.path.join(OUT_DIR, "figure.pdf")
OUT_PNG = os.path.join(OUT_DIR, "figure.png")

# --- data, exactly as given in the brief ---------------------------------
# Every district's three shares sum to 1.00; plotted as percentages.
TIERS = ["low", "medium", "high"]
SHARES = {
    "A": [0.42, 0.35, 0.23],
    "B": [0.31, 0.44, 0.25],
    "C": [0.55, 0.30, 0.15],
    "D": [0.28, 0.47, 0.25],
    "E": [0.37, 0.38, 0.25],
    "F": [0.50, 0.33, 0.17],
}

# One stated ordering rule: districts sorted by low-tier share, descending, so
# that districts with a similar composition sit next to each other.
ORDER = sorted(SHARES, key=lambda d: -SHARES[d][0])

# Sequential single-hue ramp (light -> dark) for the ordinal tiers.
TIER_COLORS = ["#c6dbef", "#6baed6", "#2171b5"]

PERCENT = {d: [round(100.0 * s, 1) for s in SHARES[d]] for d in ORDER}

WKS_NAME = "vuln"


def build_graph():
    wks = op.new_sheet("w", WKS_NAME)
    wks.from_list(0, ORDER, lname="District")
    for j, tier in enumerate(TIERS):
        wks.from_list(j + 1, [PERCENT[d][j] for d in ORDER], lname=tier)
    wks.cols_axis("x", 0)                       # district labels on X
    for j in range(3):
        wks.cols_axis("y", j + 1)               # three Y columns
    wks.activate()

    existing = set(op.graph_list())
    # Plot the three Y columns against the label column as a stacked group.
    # Plot id 213 = stacked column; Origin groups + applies the template.
    op.lt_exec("plotxy iy:=((1,2),(1,3),(1,4)) plot:=213 legend:=1;")
    new_pages = [g for g in op.graph_list() if g not in existing]
    if not new_pages:
        raise RuntimeError("Origin did not create a graph")
    gp = new_pages[0]
    gl = gp[0]

    for i, plot in enumerate(gl.plot_list()):
        plot.color = TIER_COLORS[i]             # fill colour of each tier

    gl.set_int("width", 68)                     # leave a gap between columns
    gl.rescale()
    gl.set_ylim(0, 100)                         # shares sum to 100 %
    gl.axis("x").title = "District"
    gl.axis("y").title = "Share of district area (%)"
    return gp


def main():
    op.set_show(False)
    try:
        gp = build_graph()
        pdf = gp.save_fig(OUT_PDF, type="pdf")
        png = gp.save_fig(OUT_PNG, type="png", width=1200)
        print("pdf:", pdf)
        print("png:", png)
    finally:
        op.exit()


if __name__ == "__main__":
    main()
