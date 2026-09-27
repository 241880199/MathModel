#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Figure: vulnerability composition of six districts (A-F).

Two panels:
  (a) 100% stacked horizontal bars - the vulnerability composition of each
      district (shares of land area in the low / medium / high tier; the
      three shares sum to 1.00 within every district).
  (b) The same six districts placed in the low-medium-high simplex (ternary
      diagram) - the natural geometry for a three-part composition. Because
      every district is one point in this triangle, the two districts with
      the most similar structure are simply the two closest points; the
      closest pair is marked explicitly.

Similarity is measured by the Aitchison distance, the standard metric for
compositional data (Euclidean distance between centred log-ratio vectors).
It is reported alongside the plain Euclidean distance on the shares; both
metrics select the same pair, so the judgement does not depend on the metric.

Deterministic: fixed input table, no randomness, no network access,
no external data files, no manual steps.
"""

import datetime
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, Polygon
import numpy as np

# ----------------------------------------------------------------------
# Input data (shares of district land area; each row sums to 1.00)
# ----------------------------------------------------------------------
DISTRICTS = ["A", "B", "C", "D", "E", "F"]
TIERS = ["low", "medium", "high"]
SHARES = np.array([
    # low, medium, high
    [0.42, 0.35, 0.23],   # A
    [0.31, 0.44, 0.25],   # B
    [0.55, 0.30, 0.15],   # C
    [0.28, 0.47, 0.25],   # D
    [0.37, 0.38, 0.25],   # E
    [0.50, 0.33, 0.17],   # F
])

# Ordered severity ramp (low -> high), ColorBrewer YlOrRd 3-class:
# sequential, colour-vision-deficiency safe, light -> dark for rising severity.
TIER_COLORS = ["#ffeda0", "#feb24c", "#f03b20"]
TIER_TEXT = ["#3d3d3d", "#3d3d3d", "#ffffff"]   # label colour for contrast
EDGE = "#5a5a5a"

INK = "#222222"
GRID = "#c9c9c9"
POINT = "#2f3b52"
OUT = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------
# Similarity metrics
# ----------------------------------------------------------------------
def euclidean_matrix(x):
    """Plain Euclidean distance between the share vectors."""
    diff = x[:, None, :] - x[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def aitchison_matrix(x):
    """Aitchison distance: Euclidean distance between centred log-ratios."""
    clr = np.log(x) - np.log(x).mean(axis=1, keepdims=True)
    diff = clr[:, None, :] - clr[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=-1))


def ranked_pairs(dmat, names):
    """All unordered pairs, sorted by distance (closest first)."""
    out = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            out.append((dmat[i, j], names[i], names[j]))
    out.sort(key=lambda t: t[0])
    return out


AIT = aitchison_matrix(SHARES)
EUC = euclidean_matrix(SHARES)
BY_AIT = ranked_pairs(AIT, DISTRICTS)
BY_EUC = ranked_pairs(EUC, DISTRICTS)

D_AIT, P1, P2 = BY_AIT[0]
D_AIT_EUC = [p for p in BY_EUC if {p[1], p[2]} == {P1, P2}][0][0]
# Both metrics must agree, otherwise the figure's headline claim is not safe.
assert (BY_EUC[0][1], BY_EUC[0][2]) == (P1, P2), "metrics disagree on closest pair"


# ----------------------------------------------------------------------
# Ternary geometry: barycentric (low, medium, high) -> cartesian
# ----------------------------------------------------------------------
H = np.sqrt(3.0) / 2.0
V_LOW = np.array([0.0, 0.0])      # low = 1
V_MED = np.array([1.0, 0.0])      # medium = 1
V_HIGH = np.array([0.5, H])       # high = 1


def tern(low, med, high):
    """Map a composition (summing to 1) onto the simplex."""
    low = np.asarray(low, float)
    med = np.asarray(med, float)
    high = np.asarray(high, float)
    return med + 0.5 * high, H * high


# unit vectors pointing outward from each edge (for tick / axis labels)
N_LEFT = np.array([-H, 0.5]) / np.hypot(H, 0.5)     # left edge,  outward
N_RIGHT = np.array([H, 0.5]) / np.hypot(H, 0.5)     # right edge, outward
N_BOTTOM = np.array([0.0, -1.0])                    # bottom edge, outward

TICKS = np.arange(0.1, 0.95, 0.1)


# ----------------------------------------------------------------------
# Figure
# ----------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,      # keep text as TrueType so it stays searchable
    "ps.fonttype": 42,
    "savefig.dpi": 300,
})

fig = plt.figure(figsize=(9.6, 4.5))
ax_a = fig.add_axes([0.065, 0.235, 0.40, 0.66])
ax_b = fig.add_axes([0.545, 0.16, 0.415, 0.76])

# ---------------- panel (a): 100% stacked bars ----------------
ypos = np.arange(len(DISTRICTS))
left = np.zeros(len(DISTRICTS))
for k in range(3):
    vals = SHARES[:, k]
    ax_a.barh(ypos, vals, left=left, height=0.68,
              color=TIER_COLORS[k], edgecolor=EDGE, linewidth=0.7, zorder=3)
    for y, (v, l) in enumerate(zip(vals, left)):
        ax_a.text(l + v / 2.0, y, "{:.2f}".format(v),
                  ha="center", va="center", fontsize=8,
                  color=TIER_TEXT[k], zorder=4)
    left = left + vals

ax_a.set_yticks(ypos)
ax_a.set_yticklabels(DISTRICTS)
ax_a.invert_yaxis()                       # A at the top
ax_a.set_ylim(len(DISTRICTS) - 0.45, -0.75)
ax_a.set_xlim(0, 1)
ax_a.set_xticks(np.arange(0, 1.01, 0.2))
ax_a.set_xlabel("share of district land area")
ax_a.set_ylabel("district")
ax_a.set_title("(a) Vulnerability composition by district", fontsize=10, pad=6)
ax_a.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
ax_a.set_axisbelow(True)
for s in ("top", "right"):
    ax_a.spines[s].set_visible(False)

# ---------------- panel (b): ternary simplex ----------------
# gridlines at each 0.1 of every component
s = np.linspace(0.0, 1.0, 60)
for c in TICKS:
    for fixed in range(3):
        v = np.array([c, c, c])
        if fixed == 0:                       # low = c
            a1, a2 = (1 - c) * s, c * np.ones_like(s)
            l_, m_, h_ = a1, a2, np.zeros_like(s)
        elif fixed == 1:                     # medium = c
            l_, m_, h_ = (1 - c) * s, c * np.ones_like(s), np.zeros_like(s)
        else:                                # high = c
            l_, m_, h_ = (1 - c) * s, (1 - c) * (1 - s), c * np.ones_like(s)
        gx, gy = tern(l_, m_, h_)
        ax_b.plot(gx, gy, color=GRID, linewidth=0.55, zorder=1)

# triangle outline
tri = np.vstack([V_LOW, V_MED, V_HIGH])
ax_b.add_patch(Polygon(tri, closed=True, fill=False,
                       edgecolor="#333333", linewidth=1.1, zorder=2))

# tick marks + tick labels on each edge
for c in TICKS:
    # low, along the left edge: (low, med, high) = (c, 0, 1-c)
    p = np.array(tern(c, 0.0, 1.0 - c))
    p = np.array([p[0], p[1]])
    ax_b.plot(*zip(p, p + 0.018 * N_LEFT), color="#333333", linewidth=0.7, zorder=3)
    q = p + 0.055 * N_LEFT
    ax_b.text(q[0], q[1], "{:.1f}".format(c), fontsize=7,
              ha="center", va="center", color="#444444", rotation=60)
    # medium, along the bottom edge: (0, c, 1-c)
    p = np.array(tern(1.0 - c, c, 0.0))
    p = np.array([p[0], p[1]])
    ax_b.plot(*zip(p, p + 0.018 * N_BOTTOM), color="#333333", linewidth=0.7, zorder=3)
    q = p + 0.055 * N_BOTTOM
    ax_b.text(q[0], q[1], "{:.1f}".format(c), fontsize=7,
              ha="center", va="center", color="#444444")
    # high, along the right edge: (0, 1-c, c)
    p = np.array(tern(0.0, 1.0 - c, c))
    p = np.array([p[0], p[1]])
    ax_b.plot(*zip(p, p + 0.018 * N_RIGHT), color="#333333", linewidth=0.7, zorder=3)
    q = p + 0.055 * N_RIGHT
    ax_b.text(q[0], q[1], "{:.1f}".format(c), fontsize=7,
              ha="center", va="center", color="#444444", rotation=-60)

# axis titles, outside the edge midpoints
ax_b.text(0.5, -0.175, "medium share", fontsize=9, ha="center", va="center", color=INK)
ax_b.text(0.25 + 0.135 * N_LEFT[0], H / 2 + 0.135 * N_LEFT[1], "low share",
          fontsize=9, ha="center", va="center", color=INK, rotation=60)
ax_b.text(0.75 + 0.135 * N_RIGHT[0], H / 2 + 0.135 * N_RIGHT[1], "high share",
          fontsize=9, ha="center", va="center", color=INK, rotation=-60)

# the six districts as points
px, py = tern(SHARES[:, 0], SHARES[:, 1], SHARES[:, 2])
ax_b.scatter(px, py, s=52, facecolor=POINT, edgecolor="white",
             linewidth=0.9, zorder=5)

# label offsets (hand-tuned, deterministic) so the six labels do not collide
LABEL_OFF = {
    "A": (-0.045, 0.042), "B": (-0.018, 0.060), "C": (-0.046, -0.018),
    "D": (0.078, -0.026), "E": (0.002, -0.055), "F": (-0.004, -0.058),
}
for name, x, y in zip(DISTRICTS, px, py):
    dx, dy = LABEL_OFF[name]
    ax_b.text(x + dx, y + dy, name, fontsize=9.5, fontweight="bold",
              ha="center", va="center", color=INK, zorder=6,
              path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])

# highlight the closest pair: one enclosure around the two nearly coincident
# points (plus the segment joining them, which is short because they are close)
i1, i2 = DISTRICTS.index(P1), DISTRICTS.index(P2)
mx, my = (px[i1] + px[i2]) / 2.0, (py[i1] + py[i2]) / 2.0
ax_b.plot([px[i1], px[i2]], [py[i1], py[i2]], color=INK, linewidth=1.0,
          linestyle=(0, (3, 2)), zorder=4)
ax_b.add_patch(Ellipse((mx, my), width=0.135, height=0.090,
                       facecolor="none", edgecolor=INK, linewidth=1.3, zorder=5))

# evidence for the judgement, in the free strip above the triangle
rank_txt = "closest pair: {}–{}  (Aitchison d = {:.2f})".format(P1, P2, D_AIT)
rank_txt += "    next closest: {}".format(
    ", ".join("{}–{} {:.2f}".format(a, b, d) for d, a, b in BY_AIT[1:3]))
rank_txt += "\nall remaining pairs:  d > {:.2f}".format(BY_AIT[3][0] - 0.01)
ax_b.text(1.235, 1.052, rank_txt, fontsize=7.4, ha="right", va="top",
          color="#3d3d3d", linespacing=1.8, zorder=7)

ax_b.set_title("(b) The same districts in the low–medium–high simplex",
               fontsize=10, pad=6)
ax_b.set_aspect("equal")
ax_b.set_xlim(-0.235, 1.235)
ax_b.set_ylim(-0.285, 1.065)
ax_b.axis("off")

# ---------------- shared legend ----------------
handles = [Line2D([], [], marker="s", linestyle="none", markersize=8,
                  markerfacecolor=TIER_COLORS[k], markeredgecolor=EDGE,
                  label="{} vulnerability".format(TIERS[k])) for k in range(3)]
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, 0.005), handletextpad=0.5,
           columnspacing=2.0)

fig.savefig(os.path.join(OUT, "figure.pdf"),
            metadata={"CreationDate": datetime.datetime(2026, 1, 1, 0, 0, 0)})
fig.savefig(os.path.join(OUT, "figure.png"))
plt.close(fig)

# ----------------------------------------------------------------------
# Console report (audit trail for the caption's claims)
# ----------------------------------------------------------------------
print("closest pair by Aitchison distance : {} - {:.4f}".format(
    " - ".join(BY_AIT[0][1:]), BY_AIT[0][0]))
print("same pair by Euclidean distance    : {:.4f} (rank {} of 15)".format(
    D_AIT_EUC, [tuple(sorted((a, b))) for _, a, b in BY_EUC].index(
        tuple(sorted((P1, P2)))) + 1))
print("next closest pairs (Aitchison)     : " + ", ".join(
    "{} - {} {:.4f}".format(a, b, d) for d, a, b in BY_AIT[1:4]))
print("shares per district sum to         : " + ", ".join(
    "{:.2f}".format(v) for v in SHARES.sum(axis=1)))
print("wrote figure.pdf, figure.png in", OUT)
