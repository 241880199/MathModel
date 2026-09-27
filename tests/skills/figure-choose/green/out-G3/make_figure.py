# -*- coding: utf-8 -*-
"""
make_figure.py - figure for brief R3 (district vulnerability composition).

Regenerates figure.pdf / figure.png from the six-district, three-tier shares in
the brief. Deterministic: fixed data, no randomness, no network, no manual steps.

    python make_figure.py

--------------------------------------------------------------------------
Chart choice (skill `mcm-figure-choose`, decision tree in
references/chart-types.md, entry 4 = composition / 构成)

  Data relationship: one whole (a district's land area) split into three parts
  whose shares sum to 1 -> entry 4 (composition).  Entry 4's first choice is
  `stacked bar chart` for comparing the composition of several groups; it holds
  here (6 groups, one part-of-whole layer), so no fallback is taken.
  (The entry's fallbacks are treemap / ternary plot / radar chart; the ternary
  plot was checked and rejected on the data itself - the six compositions occupy
  only a small central patch of the simplex (low 0.28-0.55, high 0.15-0.25), so
  the three closest pairs would land within ~0.04 simplex units of each other
  and their markers would overlap at any readable size.)

  Why this plot type: the part-of-whole share is carried by *length along a
  common baseline* - every segment of every bar is read off the same 0-100%
  scale, which is exactly the channel that makes shares comparable between
  districts.  The judgement asked for by the brief (which two districts have the
  most similar structure) is supported by two design decisions:
    (1) bars are ordered by high-vulnerability share (descending), which places
        the closest pair B and D side by side;
    (2) the closest pair is picked from the data (smallest Euclidean distance
        between share vectors) and highlighted with a neutral band + bracket,
        so the reader sees both the aligned 75% boundary of B and D and the
        printed values behind the call.

  Taboos read before drawing (chart-types.md, entry 4): no pie/donut chart
  (the one rule with a judge layer), no stacked-area-for-shares, no 3-D.

Design points, mapped to the house style by ID (references/house-style.md):
  H1  figure width == text-width default (6.31 in)      -> not narrower/wider
  H3  landscape, aspect in the 2-3 band, height ~2.6 in
  H4  three chromatic colours (<= 4); the highlight band is near-grey
  H5  explicit palette, not the matplotlib default colour cycle
  H6  composition data is NOT drawn as a pie/donut
  H7  no 3-D
  H9  caption (caption.txt) is `Figure 1:` + ASCII colon, <= 12 words, no
      closing period
  H10 no top/right spines, inward major ticks only, axis label carries the unit
  H12 in-figure type 7.5-9 pt, no line/font clash with the body text
  (H11 is not covered by the style: no gridlines are drawn; the legend is kept,
  it is a 3-entry tier key and there is no alternative that is less ambiguous.)
--------------------------------------------------------------------------
"""

import os

# Pin the PDF creation timestamp so re-running yields a byte-identical file
# (matplotlib honours SOURCE_DATE_EPOCH for reproducible output). Set before
# importing matplotlib.
os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

# in-figure type: 8 pt body-relative, axis labels 9 pt, never below 7.5 pt (H12)
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 8,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

# --- data, exactly as in brief R3 (table order A-F) -----------------------
# (district, low, medium, high) - shares of the district's land area
DATA = [
    ("A", 0.42, 0.35, 0.23),
    ("B", 0.31, 0.44, 0.25),
    ("C", 0.55, 0.30, 0.15),
    ("D", 0.28, 0.47, 0.25),
    ("E", 0.37, 0.38, 0.25),
    ("F", 0.50, 0.33, 0.17),
]

TIERS = ("Low", "Medium", "High")

# Palette: single-hue sequential ramp (ordered tiers -> ordered lightness),
# deliberately not the matplotlib default colour cycle (H5).
COLORS = {"Low": "#A9C7E0", "Medium": "#4E86B4", "High": "#1D4E73"}
LABEL_INK = {"Low": "#1A1A1A", "Medium": "#FFFFFF", "High": "#FFFFFF"}

BAND_COLOR = "#EFEFEF"   # near-grey highlight band (not a chromatic colour, H4)
INK = "#333333"

FIGSIZE = (6.31, 2.90)   # H1 width = text-width default, H3 aspect 2.18
OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def check_shares(rows):
    """Every district's three shares must sum to 1.00 (brief R3)."""
    for name, low, medium, high in rows:
        total = low + medium + high
        assert abs(total - 1.0) < 1e-9, "district %s sums to %r" % (name, total)


def closest_pair(rows):
    """Pair of districts with the smallest Euclidean distance between their
    share vectors - i.e. the most similar composition."""
    d2 = {}
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            dist = sum((a[k] - b[k]) ** 2 for k in (1, 2, 3)) ** 0.5
            d2[tuple(sorted((a[0], b[0])))] = dist
    pair = min(d2, key=d2.get)
    return pair, d2[pair]


def draw_bracket(ax, x0, x1, y, drop, color):
    """Horizontal bracket in axes-fraction coordinates, above the bars."""
    ax.plot([x0, x0, x1, x1], [y - drop, y, y, y - drop],
            color=color, linewidth=0.8, clip_on=False, solid_capstyle="butt",
            transform=ax.transAxes)


def main():
    check_shares(DATA)

    # order bars by high-vulnerability share (desc), then low share (asc):
    # this puts the closest pair side by side.
    rows = sorted(DATA, key=lambda r: (-r[3], r[1]))
    (pair_lo, pair_hi), pair_dist = closest_pair(DATA)

    fig = plt.figure(figsize=FIGSIZE)
    ax = fig.add_axes([0.085, 0.16, 0.745, 0.70])

    xpos = range(len(rows))

    # highlight band behind the closest pair (neutral, drawn under the bars)
    idx = [i for i, r in enumerate(rows) if r[0] in (pair_lo, pair_hi)]
    ax.axvspan(min(idx) - 0.44, max(idx) + 0.44, color=BAND_COLOR, zorder=0)

    bottoms = [0.0] * len(rows)
    for tier, slot in zip(TIERS, (1, 2, 3)):
        vals = [r[slot] for r in rows]
        ax.bar(xpos, vals, width=0.72, bottom=bottoms, label=tier,
               color=COLORS[tier], edgecolor="white", linewidth=0.6, zorder=2)
        for x, v, b in zip(xpos, vals, bottoms):
            ax.text(x, b + v / 2.0, "%.0f" % round(v * 100), ha="center",
                    va="center", fontsize=7.5, color=LABEL_INK[tier], zorder=3)
        bottoms = [b + v for b, v in zip(bottoms, vals)]

    # axes (H10)
    ax.set_ylim(0.0, 1.0)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0", "20", "40", "60", "80", "100"])
    ax.set_ylabel("Share of district land area (%)", color=INK)
    ax.set_xticks(list(xpos))
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_xlabel("District", color=INK)
    ax.tick_params(axis="both", which="major", direction="in", color=INK,
                   labelcolor=INK, top=False, right=False)
    ax.tick_params(axis="x", pad=3)
    ax.tick_params(axis="y", pad=3)
    ax.set_xlim(-0.6, len(rows) - 0.4)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.8)

    # legend: tier key, to the right of the plot (H11 not covered by the style)
    leg = ax.legend(loc="center left", bbox_to_anchor=(1.03, 0.5),
                    frameon=False, fontsize=8, handlelength=1.1,
                    handleheight=0.9, labelspacing=0.9, borderaxespad=0.0)
    for text in leg.get_texts():
        text.set_color(INK)

    # the judgement the brief asks for: mark the closest pair
    x0 = (min(idx) - 0.44 - (-0.6)) / (len(rows) + 0.2)
    x1 = (max(idx) + 0.44 - (-0.6)) / (len(rows) + 0.2)
    draw_bracket(ax, x0, x1, 1.035, 0.035, INK)
    ax.text((x0 + x1) / 2.0, 1.075,
            "most similar pair (%s, %s)" % (pair_lo, pair_hi),
            transform=ax.transAxes, ha="center", va="bottom", fontsize=8,
            color=INK)

    fig.savefig(os.path.join(OUT_DIR, "figure.pdf"))
    fig.savefig(os.path.join(OUT_DIR, "figure.png"), dpi=200)
    plt.close(fig)

    print("closest pair: %s-%s, distance %.4f" % (pair_lo, pair_hi, pair_dist))
    print("bar order:", ", ".join(r[0] for r in rows))
    print("wrote figure.pdf and figure.png to", OUT_DIR)


if __name__ == "__main__":
    main()
