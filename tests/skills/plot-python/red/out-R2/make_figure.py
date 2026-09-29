# -*- coding: utf-8 -*-
"""Regenerate the figure for Brief R2: drivers of historical disaster counts.

Inputs are hard-coded from the brief (six districts x five attributes).
No network access, no manual steps, no randomness: the output is byte-stable
for a fixed matplotlib version.

Outputs (written next to this script):
    figure.pdf, figure.png, caption.txt

Run:  python make_figure.py
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats

# --------------------------------------------------------------------------
# 1. Data (transcribed from the brief, districts in alphabetical order)
# --------------------------------------------------------------------------
DISTRICTS = ["A", "B", "C", "D", "E", "F"]

ATTRS = [
    "Population density",
    "Mean slope",
    "Vegetation cover",
    "Historical disaster count",
    "Infrastructure index",
]

# columns: population density, mean slope, vegetation cover, disasters, infra
DATA = np.array(
    [
        [820.0, 3.2, 0.61, 12.0, 74.0],  # A
        [640.0, 11.5, 0.58, 31.0, 72.0],  # B
        [610.0, 2.4, 0.72, 8.0, 81.0],  # C
        [1210.0, 14.8, 0.41, 38.0, 55.0],  # D
        [990.0, 7.1, 0.49, 16.0, 66.0],  # E
        [1750.0, 5.0, 0.55, 24.0, 70.0],  # F
    ]
)

OUTCOME = 3  # historical disaster count
PREDICTORS = [0, 1, 2, 4]

# --------------------------------------------------------------------------
# 2. Statistics
# --------------------------------------------------------------------------
y = DATA[:, OUTCOME]

rows = []
for j in PREDICTORS:
    x = DATA[:, j]
    r, p = stats.pearsonr(x, y)
    rho, p_rho = stats.spearmanr(x, y)
    rows.append({"name": ATTRS[j], "r": r, "p": p, "rho": rho, "p_rho": p_rho})

# strongest driver first (by |Pearson r|)
rows.sort(key=lambda d: abs(d["r"]), reverse=True)

# standardise all five attributes, then measure district-to-district distance
z = (DATA - DATA.mean(axis=0)) / DATA.std(axis=0, ddof=1)
dist = np.sqrt(((z[:, None, :] - z[None, :, :]) ** 2).sum(axis=-1))

off = dist + np.eye(len(DISTRICTS)) * 1e9
i_min, j_min = np.unravel_index(np.argmin(off), off.shape)
closest_pair = (DISTRICTS[i_min], DISTRICTS[j_min], dist[i_min, j_min])
most_isolated = DISTRICTS[int(np.argmax(off.min(axis=1)))]
isolated_d = off.min(axis=1).max()

# --------------------------------------------------------------------------
# 3. Style
# --------------------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["DejaVu Serif"],
        "mathtext.fontset": "dejavuserif",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "figure.dpi": 300,
        "savefig.bbox": "tight",
        "pdf.fonttype": 42,
    }
)

NEUTRAL = "#4C72B0"  # non-selected bars
ACCENT = "#C44E52"  # strongest driver
INK = "#222222"

sim_cmap = LinearSegmentedColormap.from_list(
    "similarity", ["#F2F6FB", "#9DB8D2", "#4C72B0", "#22384F"]
)

# --------------------------------------------------------------------------
# 4. Figure: (a) correlations with disaster count, (b) district similarity
# --------------------------------------------------------------------------
fig, (ax_a, ax_b) = plt.subplots(
    1,
    2,
    figsize=(9.0, 3.9),
    gridspec_kw={"width_ratios": [1.0, 1.02], "wspace": 0.32},
)

# --- panel (a): correlation of each factor with the disaster count ---------
n = len(rows)
pos = np.arange(n)[::-1]
vals = [d["r"] for d in rows]
names = [d["name"] for d in rows]
colors = [ACCENT if k == 0 else NEUTRAL for k in range(n)]

ax_a.barh(pos, vals, height=0.62, color=colors, edgecolor="white", linewidth=0.6, zorder=3)
ax_a.axvline(0.0, color=INK, linewidth=0.8, zorder=2)

# Spearman rank correlation, drawn as hollow markers on the same scale
ax_a.scatter(
    [d["rho"] for d in rows],
    pos,
    s=22,
    facecolors="white",
    edgecolors=INK,
    linewidths=0.9,
    zorder=4,
    label="Spearman $\\rho$",
)

for k, d in enumerate(rows):
    v = d["r"]
    # start the value label beyond whichever statistic reaches furthest out,
    # so it never lands on the Spearman marker
    reached = max(v, d["rho"]) if v >= 0 else min(v, d["rho"])
    ax_a.text(
        reached + (0.08 if v >= 0 else -0.08),
        pos[k],
        f"{v:+.2f}" + ("*" if d["p"] < 0.05 else ""),
        va="center",
        ha="left" if v >= 0 else "right",
        fontsize=8,
        color=INK,
    )

ax_a.set_yticks(pos)
ax_a.set_yticklabels(names)
ax_a.set_xlim(-1.5, 1.45)
ax_a.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
ax_a.set_ylim(-0.7, n - 0.3)
ax_a.set_xlabel("Correlation with historical disaster count")
ax_a.set_title("(a) Which factor tracks the disaster count?", loc="left")

handles = [
    plt.Rectangle((0, 0), 1, 1, facecolor=ACCENT, edgecolor="white"),
    plt.Rectangle((0, 0), 1, 1, facecolor=NEUTRAL, edgecolor="white"),
    plt.Line2D([], [], marker="o", linestyle="none", markerfacecolor="white",
               markeredgecolor=INK, markersize=4.5),
]
ax_a.legend(handles, ["Pearson $r$ (strongest)", "Pearson $r$", "Spearman $\\rho$"],
            loc="upper left", frameon=False, fontsize=7.5, handlelength=1.0,
            handleheight=0.9, borderaxespad=0.2, labelspacing=0.35)
ax_a.text(0.99, 0.02, "* Pearson $p < 0.05$", transform=ax_a.transAxes,
          fontsize=7.5, color=INK, ha="right", va="bottom")

# --- panel (b): district similarity in standardised attribute space --------
im = ax_b.imshow(dist, cmap=sim_cmap, vmin=0.0, vmax=dist.max())

ax_b.set_xticks(range(len(DISTRICTS)))
ax_b.set_yticks(range(len(DISTRICTS)))
ax_b.set_xticklabels(DISTRICTS)
ax_b.set_yticklabels(DISTRICTS)
ax_b.set_xlabel("District")
ax_b.set_ylabel("District")
ax_b.set_title("(b) Districts that behave alike", loc="left")

for a in range(len(DISTRICTS)):
    for b in range(len(DISTRICTS)):
        if a == b:
            continue
        ax_b.text(
            b,
            a,
            f"{dist[a, b]:.1f}",
            ha="center",
            va="center",
            fontsize=7,
            color="white" if dist[a, b] > 0.55 * dist.max() else INK,
        )

# flag the closest pair with a thin square outline on both cells
for (rr, cc) in [(i_min, j_min), (j_min, i_min)]:
    ax_b.add_patch(
        plt.Rectangle((cc - 0.5, rr - 0.5), 1, 1, fill=False,
                      edgecolor=ACCENT, linewidth=1.2, zorder=5)
    )

cbar = fig.colorbar(im, ax=ax_b, fraction=0.046, pad=0.04)
cbar.set_label("Euclidean distance (standardised)", fontsize=8)
cbar.outline.set_linewidth(0.6)
cbar.ax.tick_params(labelsize=7.5)

ax_b.text(
    0.5,
    -0.245,
    f"Most similar: {closest_pair[0]}-{closest_pair[1]} (d = {closest_pair[2]:.2f})"
    f"    |    most distinct: {most_isolated} (d = {isolated_d:.2f})",
    transform=ax_b.transAxes,
    ha="center",
    va="top",
    fontsize=8,
    color=INK,
)

# --------------------------------------------------------------------------
# 5. Export + caption
# --------------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(here, "figure.pdf"), metadata={"CreationDate": None})
fig.savefig(os.path.join(here, "figure.png"))
plt.close(fig)

top = rows[0]
caption = (
    "Figure 1. Drivers of the historical disaster count and the similarity of the six "
    "districts. (a) Pearson correlation between each measured attribute and the historical "
    "disaster count, ordered by absolute strength; hollow circles mark the Spearman rank "
    "correlation and an asterisk marks p < 0.05. Mean slope is the only factor that is both "
    f"strongly and significantly correlated with the disaster count (r = {top['r']:+.2f}, "
    f"p = {top['p']:.3f}), so terrain steepness rather than exposure or population dominates; "
    f"the infrastructure index (r = {rows[1]['r']:+.2f}) and vegetation cover "
    f"(r = {rows[2]['r']:+.2f}) act as weaker protective factors and population density is "
    f"nearly unrelated (r = {rows[3]['r']:+.2f}). (b) Pairwise Euclidean distance between "
    "districts in the space of all five standardised attributes; darker cells are more "
    "dissimilar and the red outlines mark the closest pair. Districts A and C are the most "
    f"similar (d = {closest_pair[2]:.2f}), both combining gentle slopes, the highest "
    "vegetation cover and the strongest infrastructure, and E is the next nearest to this "
    f"group, whereas D is the most distinct district overall (d = {isolated_d:.2f} to its "
    "nearest neighbour) because it pairs the steepest slopes and the lowest vegetation cover "
    "with the weakest infrastructure and the largest disaster count. With only six districts, "
    "these correlations are indicative rather than conclusive."
)

with open(os.path.join(here, "caption.txt"), "w", encoding="utf-8") as fh:
    fh.write(caption + "\n")

print("[ok] wrote figure.pdf, figure.png, caption.txt")
for d in rows:
    print(f"  {d['name']:<28} r={d['r']:+.3f}  p={d['p']:.4f}  rho={d['rho']:+.3f}")
print(f"  closest pair {closest_pair[0]}-{closest_pair[1]} d={closest_pair[2]:.2f}")
print(f"  most distinct {most_isolated} nn d={isolated_d:.2f}")
