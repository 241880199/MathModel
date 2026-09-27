#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Regenerate the district vulnerability-composition figure (brief R1).

Data relationship: composition (one whole -- a district's land area -- split into
three parts that sum back to the whole).  Chart type chosen by the
``mcm-figure-choose`` decision tree, entry 4 (composition): first choice is a
stacked bar chart, because the question is "compare the composition of several
groups" (six districts), not "how is a single whole divided".

Delivery-form targets come from ``house-style.md`` and are cited by H-ID only:

  H1  width close to the body text width (0.95-1.0 x 6.31 in -> 6.0 in)
  H3  landscape, aspect ratio in the usual 2-3 band, height ~2.6 in
  H4  at most 4 main colours (three tiers -> three ordered shades)
  H5  no matplotlib default colour cycle (tab10)
  H6  no pie / donut chart for composition data
  H7  no 3-D
  H9  caption is "Figure N:" + ASCII colon, <= 12 words, no trailing period
  H10 no top/right spines, ticks pointing in, axis labels carry units
  H12 in-figure text 9 pt (>= 7 pt, ~0.8-1.0 x body size)

Deterministic: the numbers are hard-coded below, no network, no manual steps.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# 1. Data (hard-coded, as given in the brief; shares are fractions of a
#    district's land area and each district's three shares sum to 1.00)
# --------------------------------------------------------------------------
TIERS = ["low", "medium", "high"]
# Ordered tiers -> ordered shades of one hue (H4, H5: not the tab10 cycle).
COLOURS = {"low": "#deebf7", "medium": "#9ecae1", "high": "#3182bd"}

DISTRICTS = {
    "A": {"low": 0.42, "medium": 0.35, "high": 0.23},
    "B": {"low": 0.31, "medium": 0.44, "high": 0.25},
    "C": {"low": 0.55, "medium": 0.30, "high": 0.15},
    "D": {"low": 0.28, "medium": 0.47, "high": 0.25},
    "E": {"low": 0.37, "medium": 0.38, "high": 0.25},
    "F": {"low": 0.50, "medium": 0.33, "high": 0.17},
}

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# 2. Checks on the input (fail loudly rather than draw a wrong figure)
# --------------------------------------------------------------------------
for _d, _row in DISTRICTS.items():
    _total = sum(_row[t] for t in TIERS)
    assert abs(_total - 1.0) < 1e-9, "district %s sums to %r, not 1" % (_d, _total)


def pairwise_l1(a, b):
    """L1 (city-block) distance between two composition vectors."""
    return sum(abs(DISTRICTS[a][t] - DISTRICTS[b][t]) for t in TIERS)


# --------------------------------------------------------------------------
# 3. Reading of the data that the figure has to carry
# --------------------------------------------------------------------------
# Order the districts by their low-tier share, descending.  Compositions that
# vary mainly along the low <-> medium axis land next to each other, so the
# closest pairs become neighbours and can be read off by eye.
ORDER = sorted(DISTRICTS, key=lambda d: (-DISTRICTS[d]["low"], d))

# The closest pair under L1 over the three shares.
_names = sorted(DISTRICTS)
PAIRS = [(_names[i], _names[j])
         for i in range(len(_names)) for j in range(i + 1, len(_names))]
CLOSEST = min(PAIRS, key=lambda p: (pairwise_l1(*p), p))

# --------------------------------------------------------------------------
# 4. Figure (H1 / H3 / H12)
# --------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "serif"],
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "figure.dpi": 300,
    "savefig.facecolor": "white",
    "figure.facecolor": "white",
})

FIG_W, FIG_H = 6.0, 2.6          # H1: 6.0 / 6.31 = 0.95; H3: aspect 2.31
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))

x = range(len(ORDER))
BAR_W = 0.62
bottom = [0.0] * len(ORDER)

for tier in TIERS:
    vals = [DISTRICTS[d][tier] for d in ORDER]
    ax.bar(x, vals, BAR_W, bottom=bottom,
           color=COLOURS[tier], edgecolor="white", linewidth=0.6,
           label=tier.capitalize(), zorder=3)
    # Direct value labels: the shares are the point of the figure, so put the
    # numbers on the figure instead of making the reader measure the segments.
    for xi, v, b0 in zip(x, vals, bottom):
        # Dark text on the light shades, white text on the dark shade.
        lum = int(COLOURS[tier][1:3], 16) * 0.299 \
            + int(COLOURS[tier][3:5], 16) * 0.587 \
            + int(COLOURS[tier][5:7], 16) * 0.114
        ax.text(xi, b0 + v / 2.0, "%.2f" % v,
                ha="center", va="center", fontsize=7,
                color="#1a1a1a" if lum > 150 else "white", zorder=4)
    bottom = [b + v for b, v in zip(bottom, vals)]

# --------------------------------------------------------------------------
# 5. Axes (H10)
# --------------------------------------------------------------------------
ax.set_ylim(0.0, 1.0)
ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(["0.00", "0.20", "0.40", "0.60", "0.80", "1.00"])
ax.set_ylabel("Share of land area (fraction)")
ax.set_xticks(list(x))
ax.set_xticklabels(ORDER)
ax.set_xlim(-0.55, len(ORDER) - 0.45)
ax.tick_params(axis="both", which="both", top=False, right=False)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

# --------------------------------------------------------------------------
# 6. Point at the answer: the closest pair, which the sorting made adjacent.
#    The bracket sits below the tick labels; the x-axis title and the pair
#    note share the bottom row (they are far apart horizontally).
# --------------------------------------------------------------------------
i, j = ORDER.index(CLOSEST[0]), ORDER.index(CLOSEST[1])
x_lo, x_hi = min(i, j) - BAR_W / 2.0, max(i, j) + BAR_W / 2.0
BRACKET_Y, TEXT_Y = -0.150, -0.175
ax.plot([x_lo, x_hi], [BRACKET_Y, BRACKET_Y],
        transform=ax.get_xaxis_transform(), color="#555555",
        linewidth=0.8, clip_on=False, zorder=5)
for xi in (x_lo, x_hi):
    ax.plot([xi, xi], [BRACKET_Y, BRACKET_Y + 0.030],
            transform=ax.get_xaxis_transform(), color="#555555",
            linewidth=0.8, clip_on=False, zorder=5)
ax.text((i + j) / 2.0, TEXT_Y,
        "%s and %s: closest pair" % CLOSEST,
        transform=ax.get_xaxis_transform(), ha="center", va="top",
        fontsize=8, color="#555555")

# x-axis title, written on the same row as the pair note (H10)
ax.text(2.5, TEXT_Y, "District", transform=ax.get_xaxis_transform(),
        ha="center", va="top", fontsize=9, color="black")

# --------------------------------------------------------------------------
# 7. Legend (one row, above the plot, no frame)
# --------------------------------------------------------------------------
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3,
          frameon=False, handlelength=1.2, handleheight=0.9,
          columnspacing=1.6, borderaxespad=0.0,
          title="Vulnerability tier")
ax.get_legend().get_title().set_fontsize(8)

fig.subplots_adjust(left=0.10, right=0.99, top=0.80, bottom=0.26)

# --------------------------------------------------------------------------
# 8. Export (H1: no tight bbox, so the page keeps the intended 6.0 x 2.6 in)
# --------------------------------------------------------------------------
png_path = os.path.join(OUT_DIR, "figure.png")
pdf_path = os.path.join(OUT_DIR, "figure.pdf")
fig.savefig(png_path, dpi=300)
# CreationDate is dropped so that two runs give byte-identical files.
fig.savefig(pdf_path, metadata={"CreationDate": None})
plt.close(fig)

print("wrote %s" % png_path)
print("wrote %s" % pdf_path)
print("closest pair under L1: %s-%s (distance %.2f)"
      % (CLOSEST[0], CLOSEST[1], pairwise_l1(*CLOSEST)))
