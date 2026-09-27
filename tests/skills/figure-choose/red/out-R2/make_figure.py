#!/usr/bin/env python3
"""Brief R2 - drivers of historical disaster counts.

Regenerates, from the six-district table in the brief, the figure used to answer
two questions:

  (i)  which measured factor is most strongly correlated with the historical
       disaster count, and
  (ii) how similar the six districts are to one another.

The script is self-contained and deterministic: the numbers are typed in below,
nothing is downloaded, and no manual post-processing step is required.

Outputs written next to this script:
    figure.pdf
    figure.png

Run:  python make_figure.py
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from scipy.cluster.hierarchy import dendrogram, leaves_list, linkage
from scipy.stats import pearsonr, spearmanr

# --------------------------------------------------------------------------
# 1. Data (typed verbatim from the brief)
# --------------------------------------------------------------------------

DISTRICTS = ["A", "B", "C", "D", "E", "F"]

# Column order used throughout the figure.
ATTRS = [
    "Mean slope",
    "Infrastructure index",
    "Vegetation cover",
    "Population density",
]
ATTR_UNITS = {
    "Mean slope": "deg",
    "Infrastructure index": "0-100",
    "Vegetation cover": "fraction of area",
    "Population density": "people/km2",
}

RESPONSE = "Historical disaster count"

# Rows are districts A..F, columns are ATTRS in the order above, then RESPONSE.
RAW = {
    "A": dict(zip(ATTRS, [3.2, 74, 0.61, 820])) | {RESPONSE: 12},
    "B": dict(zip(ATTRS, [11.5, 72, 0.58, 640])) | {RESPONSE: 31},
    "C": dict(zip(ATTRS, [2.4, 81, 0.72, 610])) | {RESPONSE: 8},
    "D": dict(zip(ATTRS, [14.8, 55, 0.41, 1210])) | {RESPONSE: 38},
    "E": dict(zip(ATTRS, [7.1, 66, 0.49, 990])) | {RESPONSE: 16},
    "F": dict(zip(ATTRS, [5.0, 70, 0.55, 1750])) | {RESPONSE: 24},
}

COLUMNS = ATTRS + [RESPONSE]
M = np.array([[RAW[d][c] for c in COLUMNS] for d in DISTRICTS], dtype=float)
y = M[:, -1]
X = M[:, :-1]

# --------------------------------------------------------------------------
# 2. Analysis
# --------------------------------------------------------------------------

# Standardise each attribute across districts (z-scores, population sd) so that
# the mixed units (people/km2, degrees, fractions, counts, index points) can be
# compared and combined in a single distance / colour scale.
Z = (M - M.mean(axis=0)) / M.std(axis=0)

# Univariate association between each driver and the disaster count. Both a
# linear (Pearson) and a rank-based (Spearman) measure are reported: with only
# six districts, a conclusion that survives both is the safer one.
pearson = {}
spearman = {}
for j, name in enumerate(ATTRS):
    pearson[name] = pearsonr(X[:, j], y)[0]
    spearman[name] = spearmanr(X[:, j], y)[0]

# Drivers ordered by absolute Pearson correlation, strongest first.
ranked = sorted(ATTRS, key=lambda n: -abs(pearson[n]))

# Similarity structure: average-linkage agglomerative clustering on Euclidean
# distances between standardised attribute vectors.
Zlink = linkage(Z[:, :-1], method="average", metric="euclidean")
leaf_order = leaves_list(Zlink)
ordered_districts = [DISTRICTS[i] for i in leaf_order]

# --------------------------------------------------------------------------
# 3. Figure
# --------------------------------------------------------------------------

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman", "serif"],
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.linewidth": 0.8,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "legend.fontsize": 8.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

C_PEAR = "#2f4b7c"     # Pearson
C_SPEAR = "#c9d6e8"    # Spearman (same family, lighter)
C_FIT = "#b3442f"      # regression line / accent
C_HI = "#b3442f"       # highlighted district
CMAP = "RdBu_r"

fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.4))
fig.subplots_adjust(left=0.155, right=0.975, bottom=0.06, top=0.90,
                    hspace=0.42, wspace=0.32)

# --- (a) association of each driver with the disaster count -----------------
ax = axes[0, 0]
pos = np.arange(len(ranked))
h = 0.36
ax.barh(pos + h / 2, [pearson[n] for n in ranked], height=h,
        color=C_PEAR, edgecolor="white", linewidth=0.6, label="Pearson $r$")
ax.barh(pos - h / 2, [spearman[n] for n in ranked], height=h,
        color=C_SPEAR, edgecolor=C_PEAR, linewidth=0.6,
        label="Spearman $\\rho$")
for i, n in enumerate(ranked):
    for val, off in ((pearson[n], h / 2), (spearman[n], -h / 2)):
        ha = "left" if val >= 0 else "right"
        pad = 0.02 if val >= 0 else -0.02
        ax.text(val + pad, i + off, f"{val:+.2f}", va="center", ha=ha,
                fontsize=8, color="#333333")
ax.axvline(0.0, color="#666666", linewidth=0.8)
ax.set_yticks(pos)
ax.set_yticklabels(ranked)
ax.invert_yaxis()
ax.set_xlim(-1.15, 1.15)
ax.set_xlabel(f"Correlation with {RESPONSE.lower()}  ($n$ = 6)")
ax.set_title("(a) Association of each measured factor\nwith the disaster count")
ax.legend(loc="upper left", frameon=False)

# --- (b) the strongest driver, district by district -------------------------
ax = axes[0, 1]
xs = X[:, ATTRS.index("Mean slope")]
ax.scatter(xs, y, s=52, color=C_PEAR, edgecolor="white", linewidth=0.9,
           zorder=3)
# Hand-tuned label offsets so that no district label collides with a marker,
# with the fitted line, or with another label.
LABEL_OFFSET = {
    "A": (8, -13), "B": (8, -13), "C": (8, -3),
    "D": (8, -13), "E": (8, -3), "F": (8, 6),
}
for xi, yi, d in zip(xs, y, DISTRICTS):
    ax.annotate(d, (xi, yi), textcoords="offset points",
                xytext=LABEL_OFFSET[d], fontsize=9, fontweight="bold",
                color=C_HI if d in ("C", "D") else "#1a1a1a")
slope_fit, intercept = np.polyfit(xs, y, 1)
xline = np.linspace(xs.min() - 1.0, xs.max() + 1.0, 100)
ax.plot(xline, slope_fit * xline + intercept, color=C_FIT, linewidth=1.4,
        linestyle="--", zorder=2,
        label=f"least squares: $y$ = {slope_fit:.2f}$x$ + {intercept:.2f}")
r_slope = pearson["Mean slope"]
ax.text(0.03, 0.96, f"Pearson $r$ = {r_slope:+.2f}   ($R^2$ = {r_slope ** 2:.2f})",
        transform=ax.transAxes, va="top", ha="left", fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor="#cccccc", linewidth=0.6))
ax.set_xlabel("Mean slope (degrees)")
ax.set_ylabel(RESPONSE.capitalize())
ax.margins(x=0.10)
ax.set_title("(b) Strongest correlate: mean slope\n(the two extremes, C and D, highlighted)")
ax.legend(loc="lower right", frameon=False)

# --- (c) standardised attribute profiles, districts in cluster order --------
ax = axes[1, 0]
Zord = Z[leaf_order]   # rows reordered to match the dendrogram in panel (d)
im = ax.imshow(Zord, cmap=CMAP, norm=TwoSlopeNorm(vcenter=0.0, vmin=-2.0, vmax=2.0),
               aspect="auto")
for i in range(Zord.shape[0]):
    for j in range(Zord.shape[1]):
        val = Zord[i, j]
        ax.text(j, i, f"{val:+.2f}", ha="center", va="center", fontsize=7.5,
                color="white" if abs(val) > 1.3 else "#1a1a1a")
ax.set_xticks(np.arange(len(COLUMNS)))
ax.set_xticklabels(["Mean\nslope", "Infra-\nstructure", "Vege-\ntation",
                    "Pop.\ndensity", "Disaster\ncount"], fontsize=8)
ax.set_yticks(np.arange(len(ordered_districts)))
ax.set_yticklabels(ordered_districts)
ax.set_ylabel("District (cluster order)")
ax.set_title("(c) Standardised profiles\n(red = above average, blue = below)")
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_xticks(np.arange(len(COLUMNS) + 1) - 0.5, minor=True)
ax.set_yticks(np.arange(len(ordered_districts) + 1) - 0.5, minor=True)
ax.grid(which="minor", color="white", linewidth=1.2)
ax.tick_params(which="minor", length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.036, pad=0.03)
cb.set_label("z-score", fontsize=8)
cb.ax.tick_params(labelsize=7.5)

# --- (d) similarity structure: dendrogram ----------------------------------
ax = axes[1, 1]
dendrogram(Zlink, labels=DISTRICTS, ax=ax, color_threshold=0.0,
           above_threshold_color="#1a1a1a", link_color_func=lambda _: "#2f4b7c")
ax.set_ylabel("Euclidean distance\n(standardised attributes)")
ax.set_xlabel("District")
ax.set_title("(d) Similarity of districts\n(average linkage on the standardised drivers)")
ax.spines["bottom"].set_visible(True)
ax.tick_params(axis="x", length=0)

fig.suptitle("Drivers of historical disaster counts and similarity of the six districts",
             fontsize=11.5, y=0.965)

# --------------------------------------------------------------------------
# 4. Export
# --------------------------------------------------------------------------

outdir = os.path.dirname(os.path.abspath(__file__))
# CreationDate is suppressed so that repeated runs produce a byte-identical PDF
# rather than one that differs only by an embedded timestamp.
fig.savefig(os.path.join(outdir, "figure.pdf"), metadata={"CreationDate": None})
fig.savefig(os.path.join(outdir, "figure.png"), dpi=300)
plt.close(fig)

# --------------------------------------------------------------------------
# 5. Console summary (the numbers quoted in caption.txt)
# --------------------------------------------------------------------------

print("Correlation with", RESPONSE, "(n = 6)")
for n in ranked:
    print(f"  {n:<22} Pearson r = {pearson[n]:+.3f}   Spearman rho = {spearman[n]:+.3f}")
print()
print("Average-linkage merges (standardised drivers):")
for row in Zlink:
    a = DISTRICTS[int(row[0])] if row[0] < len(DISTRICTS) else f"cluster{int(row[0])}"
    b = DISTRICTS[int(row[1])] if row[1] < len(DISTRICTS) else f"cluster{int(row[1])}"
    print(f"  {a:>9} + {b:<9} at height {row[2]:.3f}")
print()
print("Cluster leaf order:", " ".join(ordered_districts))
