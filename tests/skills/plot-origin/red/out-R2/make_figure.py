#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Regenerate the figure for brief R2 (drivers of historical disaster counts).

The two panels answer the two questions in the brief:

  (a) mean slope vs. historical disaster count, one labelled point per district,
      with the ordinary least-squares line -> shows the single strongest driver
      and which districts behave alike;
  (b) Pearson r of every candidate attribute against the disaster count, ranked
      by |r| -> shows that slope dominates and by how much.

Deterministic: the data are hard-coded below, nothing is downloaded, and no
manual step is needed.  Run:  python make_figure.py
Outputs (written next to this script): figure.png, figure.pdf, caption.txt
"""

import os
import sys

import numpy as np

# ---------------------------------------------------------------- environment
try:
    import originpro as op
except ImportError:  # pragma: no cover - machine specific
    sys.path.insert(0, r"D:\Projects\数学建模\build\m3-origin-probe\site")
    import originpro as op

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "figure.png")
PDF = os.path.join(HERE, "figure.pdf")
CAPTION = os.path.join(HERE, "caption.txt")

# ---------------------------------------------------------------------- data
# District, population density (people/km2), mean slope (deg),
# vegetation cover (fraction), historical disaster count, infrastructure index
DATA = [
    ("A", 820, 3.2, 0.61, 12, 74),
    ("B", 640, 11.5, 0.58, 31, 72),
    ("C", 610, 2.4, 0.72, 8, 81),
    ("D", 1210, 14.8, 0.41, 38, 55),
    ("E", 990, 7.1, 0.49, 16, 66),
    ("F", 1750, 5.0, 0.55, 24, 70),
]

DISTRICTS = [row[0] for row in DATA]
POPDENS = np.array([row[1] for row in DATA], dtype=float)
SLOPE = np.array([row[2] for row in DATA], dtype=float)
VEG = np.array([row[3] for row in DATA], dtype=float)
COUNT = np.array([row[4] for row in DATA], dtype=float)
INFRA = np.array([row[5] for row in DATA], dtype=float)

# --------------------------------------------------------------- statistics
def pearson(x, y):
    return float(np.corrcoef(x, y)[0, 1])


# ranked by |r|: the point of panel (b)
CANDIDATES = [
    ("Mean slope", SLOPE),
    ("Infrastructure", INFRA),      # index, 0-100
    ("Vegetation", VEG),            # cover, fraction of area
    ("Pop. density", POPDENS),      # people/km2
]
CANDIDATES.sort(key=lambda kv: abs(pearson(kv[1], COUNT)), reverse=True)
R_VALUES = [pearson(vals, COUNT) for _, vals in CANDIDATES]
ATTR_LABELS = [name for name, _ in CANDIDATES]

R_SLOPE = pearson(SLOPE, COUNT)
FIT_B, FIT_A = np.polyfit(SLOPE, COUNT, 1)          # y = a + b x
FIT_X = np.array([SLOPE.min() - 0.6, SLOPE.max() + 0.6])
FIT_Y = FIT_A + FIT_B * FIT_X

# ----------------------------------------------------------------- palette
BLUE = "#2E5C8A"      # primary series / positive direction
ORANGE = "#C1663D"    # secondary series / negative direction

FS_TICK, FS_TITLE = 10, 11


def try_set(obj, setter, prop, value):
    """Apply a cosmetic LabTalk property; warn instead of aborting if unknown."""
    try:
        getattr(obj, setter)(prop, value)
    except Exception as exc:  # pragma: no cover - depends on Origin build
        print("  [warn] %s.%s = %r not applied (%s)" % (obj, prop, value, exc))


def main():
    op.set_show(False)

    # -------------------------------------------------- worksheet for panel (a)
    wks_a = op.new_sheet("w", lname="Districts")
    wks_a.from_list(0, DISTRICTS, lname="District", axis="L")
    wks_a.from_list(1, list(SLOPE), lname="Mean slope", units="deg", axis="X")
    wks_a.from_list(2, list(COUNT), lname="Disaster count", axis="Y")
    wks_a.from_list(3, list(FIT_X), lname="Fit slope", axis="X")
    wks_a.from_list(4, list(FIT_Y), lname="Fit count", axis="Y")

    # -------------------------------------------------- worksheet for panel (b)
    wks_b = op.new_sheet("w", lname="Correlations")
    wks_b.from_list(0, ATTR_LABELS, lname="Attribute", axis="X")
    pos = [r if r > 0 else float("nan") for r in R_VALUES]
    neg = [r if r < 0 else float("nan") for r in R_VALUES]
    wks_b.from_list(1, pos, lname="Positive", axis="Y")
    wks_b.from_list(2, neg, lname="Negative", axis="Y")

    # ------------------------------------------------------------- graph page
    gp = op.new_graph(lname="Drivers of disaster counts")

    gl = gp[0]                                    # panel (a)
    pts = gl.add_plot(wks_a, "Disaster count", "Mean slope", type="s")
    line = gl.add_plot(wks_a, "Fit count", "Fit slope", type="l")
    pts.color = BLUE
    pts.symbol_kind = 2
    pts.symbol_size = 10
    line.color = ORANGE
    try_set(line, "set_float", "line.width", 2.5)

    gl.axis("x").title = "Mean slope (degrees)"
    gl.axis("y").title = "Historical disaster count"
    try_set(gl, "set_int", "x.label.font", FS_TICK)
    try_set(gl, "set_int", "y.label.font", FS_TICK)
    try_set(gl, "set_int", "x.title.font", FS_TITLE)
    try_set(gl, "set_int", "y.title.font", FS_TITLE)
    gl.set_xlim(0.0, 17.5)
    gl.set_ylim(-2.0, 47.0, 10.0)

    leg = gl.label("legend")
    leg.text = "\\l(1) Districts\n\\l(2) Linear fit (r = %.2f)" % R_SLOPE

    # district letters next to the markers (hand-placed to clear markers/line)
    LABEL_AT = {
        "A": (3.9, 12.6),
        "B": (11.2, 29.2),
        "C": (2.75, 8.4),
        "D": (15.15, 36.3),
        "E": (7.45, 16.5),
        "F": (5.35, 24.5),
    }
    for name in DISTRICTS:
        x, y = LABEL_AT[name]
        gl.add_label(name, x, y)
    gl.add_label("(a)", 0.5, 44.0)

    # -------------------------------------------------------- panel (b) layer
    gl2 = gp.add_layer(0)   # plain layer; type 2 ("righty") ties it to layer 1
    bars_p = gl2.add_plot(wks_b, "Positive", "Attribute", type="c")
    bars_n = gl2.add_plot(wks_b, "Negative", "Attribute", type="c")
    bars_p.color = BLUE
    bars_n.color = ORANGE

    gl2.axis("y").title = "Pearson r with disaster count"
    gl2.axis("x").title = ""            # the tick labels are self-explanatory
    try_set(gl2, "set_int", "y.label.font", FS_TICK)
    try_set(gl2, "set_int", "y.title.font", FS_TITLE)
    try_set(gl2, "set_int", "x.label.font", 9)
    gl2.set_xlim(0.4, 4.75)
    gl2.set_ylim(-1.0, 1.2, 0.5)

    gl2.lt_exec("legendupdate;")           # a freshly added layer has no legend yet
    leg2 = gl2.label("legend")
    leg2.text = "\\l(1) Positive (r > 0)\n\\l(2) Negative (r < 0)"
    gl2.add_label("(b)", 0.5, 1.05)

    # ---------------------------------------------------------------- layout
    # NB: Origin keeps the graph page at its template aspect ratio (6.43 x 4.56
    # in here) - setting page width or height alone rescales the other one, so
    # the two panels are laid out inside that page rather than on a wider one.
    gl.set_float("left", 9.0)
    gl.set_float("top", 14.0)
    gl.set_float("width", 38.0)
    gl.set_float("height", 68.0)     # leaves room under panel (b) for the rotated labels
    gl2.set_float("left", 58.0)
    gl2.set_float("top", 14.0)
    gl2.set_float("width", 37.0)
    gl2.set_float("height", 68.0)

    # re-applied after the geometry: resizing a layer redraws the axes and can
    # drop an earlier tick-label rotation
    try_set(gl2, "set_int", "x.label.rotate", 45)

    gp.save_fig(PNG, type="png", width=2100)
    gp.save_fig(PDF, type="pdf")

    # ------------------------------------------------------------- caption
    FULL_NAME = {
        "Mean slope": "mean slope",
        "Infrastructure": "the infrastructure index",
        "Vegetation": "vegetation cover",
        "Pop. density": "population density",
    }
    order = ", ".join(
        "%s (r = %+.2f)" % (FULL_NAME[name], r)
        for name, r in zip(ATTR_LABELS, R_VALUES)
    )
    caption = (
        "Figure 1. Drivers of the historical disaster count across the six study "
        "districts. (a) Mean slope against the historical disaster count; each point "
        "is one district (A-F) and the solid line is the ordinary least-squares fit "
        "(r = %.2f, n = 6). (b) Pearson correlation of each candidate attribute with "
        "the historical disaster count, ranked by absolute value: %s. Mean slope is by "
        "far the strongest driver; the infrastructure index and vegetation cover are "
        "moderately negative and population density is weak. The district letters in "
        "(a) also show how the districts group: A and C (gentle slopes, dense "
        "vegetation, few disasters) resemble each other, as do B and D (steep slopes, "
        "sparse vegetation, many disasters), while E and F lie between the two pairs."
        % (R_SLOPE, order)
    )
    with open(CAPTION, "w", encoding="utf-8") as fh:
        fh.write(caption + "\n")

    return PNG, PDF, CAPTION


if __name__ == "__main__":
    try:
        for path in main():
            print("wrote %s (%d bytes)" % (path, os.path.getsize(path)))
    finally:
        op.exit()
