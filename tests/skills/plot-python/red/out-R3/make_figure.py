#!/usr/bin/env python3
"""Regenerate the district vulnerability-composition figure (Brief R3).

Input: the 6 x 3 table of land-area shares (district x vulnerability tier).
Every district's three shares sum to 1.00.

Output (written next to this script): figure.pdf and figure.png

The script is fully deterministic: no randomness, no network access, no
manual steps.  Run with ``python make_figure.py``.
"""

from __future__ import annotations

import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless, no display needed

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Rectangle

# --------------------------------------------------------------------------
# 1. Data (Brief R3, verbatim)
# --------------------------------------------------------------------------
DISTRICTS = list("ABCDEF")
TIERS = ["Low", "Medium", "High"]

# rows = districts A..F, columns = low / medium / high
SHARES = np.array(
    [
        [0.42, 0.35, 0.23],  # A
        [0.31, 0.44, 0.25],  # B
        [0.55, 0.30, 0.15],  # C
        [0.28, 0.47, 0.25],  # D
        [0.37, 0.38, 0.25],  # E
        [0.50, 0.33, 0.17],  # F
    ],
    dtype=float,
)

# Sanity checks: the figure is only valid for proper compositions.
assert SHARES.shape == (len(DISTRICTS), len(TIERS)), SHARES.shape
assert np.all(SHARES >= 0.0)
assert np.allclose(SHARES.sum(axis=1), 1.0, atol=1e-9), SHARES.sum(axis=1)

# --------------------------------------------------------------------------
# 2. Style
# --------------------------------------------------------------------------
# Ordinal tiers -> one sequential (single-hue) ramp, light = lowest tier.
TIER_COLORS = ["#c6dbef", "#4292c6", "#08306b"]
TIER_TEXT = ["#08519c", "white", "white"]  # label colour per tier
INK = "#1a1a1a"
GRID = "#d9d9d9"
ACCENT = "#d94801"  # single accent used only for the highlighted pair

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "text.color": INK,
        "axes.labelcolor": INK,
        "axes.edgecolor": "#666666",
        "axes.linewidth": 0.8,
        "xtick.color": INK,
        "ytick.color": INK,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "pdf.fonttype": 42,  # embed TrueType, not Type-3
        "ps.fonttype": 42,
        "figure.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    }
)

# --------------------------------------------------------------------------
# 3. Pairwise dissimilarity (total variation distance between share vectors)
# --------------------------------------------------------------------------
# TV(i, j) = 0.5 * sum_t |p_it - p_jt|  in [0, 1]
tv = 0.5 * np.abs(SHARES[:, None, :] - SHARES[None, :, :]).sum(axis=-1)

off_diag = tv.copy()
np.fill_diagonal(off_diag, np.nan)
i_min, j_min = np.unravel_index(np.nanargmin(off_diag), off_diag.shape)
if i_min > j_min:  # report the pair in alphabetical order
    i_min, j_min = j_min, i_min
PAIR = (DISTRICTS[i_min], DISTRICTS[j_min])
PAIR_INDEX = {i_min, j_min}          # for the bar rectangles
PAIR_LETTER = set(PAIR)              # for the tick labels
TV_MIN = float(tv[i_min, j_min])
TV_MAX = float(np.nanmax(off_diag))

# --------------------------------------------------------------------------
# 4. Figure
# --------------------------------------------------------------------------
fig, (ax, axb) = plt.subplots(
    1,
    2,
    figsize=(9.6, 4.2),
    gridspec_kw={"width_ratios": [1.35, 1.0]},
    layout="constrained",
)

# --- (a) 100% stacked composition bars ------------------------------------
x = np.arange(len(DISTRICTS))
bottom = np.zeros(len(DISTRICTS))
for t, (tier, colour, text_colour) in enumerate(zip(TIERS, TIER_COLORS, TIER_TEXT)):
    values = SHARES[:, t]
    ax.bar(
        x,
        values,
        width=0.62,
        bottom=bottom,
        color=colour,
        edgecolor="white",
        linewidth=0.7,
        label=tier,
        zorder=3,
    )
    for xi, (base, value) in enumerate(zip(bottom, values)):
        ax.text(
            xi,
            base + value / 2.0,
            f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=8,
            color=text_colour,
            zorder=4,
        )
    bottom += values

# Highlight the pair with the most similar composition.
for xi in sorted(PAIR_INDEX):
    ax.add_patch(
        Rectangle(
            (xi - 0.335, 0.0),
            0.67,
            1.0,
            fill=False,
            edgecolor=ACCENT,
            linewidth=1.6,
            zorder=5,
            clip_on=False,
        )
    )

ax.set_xticks(x)
ax.set_xticklabels(DISTRICTS)
for tick, district in zip(ax.get_xticklabels(), DISTRICTS):
    if district in PAIR_LETTER:
        tick.set_color(ACCENT)
        tick.set_fontweight("bold")

ax.set_ylim(0.0, 1.0)
ax.set_yticks(np.arange(0.0, 1.01, 0.25))
ax.set_yticklabels([f"{v:.0%}" for v in np.arange(0.0, 1.01, 0.25)])
ax.set_xlabel("District")
ax.set_ylabel("Share of district land area")
ax.set_title("(a) Vulnerability composition by district", loc="left", pad=8)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

# Shared legend: the three tiers plus the cue for the highlighted pair.
legend_handles = [
    Patch(facecolor=colour, edgecolor="white", linewidth=0.7, label=tier)
    for tier, colour in zip(TIERS, TIER_COLORS)
]
legend_handles.append(
    Patch(
        facecolor="none",
        edgecolor=ACCENT,
        linewidth=1.6,
        label=f"{PAIR[0]} and {PAIR[1]}: most similar pair (TV = {TV_MIN:.2f})",
    )
)
fig.legend(
    handles=legend_handles,
    loc="outside lower center",
    ncol=4,
    frameon=False,
    handlelength=1.6,
    handleheight=1.0,
    columnspacing=1.6,
    handletextpad=0.6,
)

# --- (b) pairwise dissimilarity matrix ------------------------------------
display = np.ma.masked_array(tv, mask=np.eye(len(DISTRICTS), dtype=bool))
cmap = plt.get_cmap("Blues").copy()
cmap.set_bad("#f2f2f2")

im = axb.imshow(display, cmap=cmap, vmin=0.0, vmax=TV_MAX, aspect="equal")
axb.set_xticks(np.arange(len(DISTRICTS)))
axb.set_yticks(np.arange(len(DISTRICTS)))
axb.set_xticklabels(DISTRICTS)
axb.set_yticklabels(DISTRICTS)
for axis, labels in ((axb.xaxis, DISTRICTS), (axb.yaxis, DISTRICTS)):
    for tick, district in zip(axis.get_ticklabels(), labels):
        if district in PAIR_LETTER:
            tick.set_color(ACCENT)
            tick.set_fontweight("bold")

axb.set_xticks(np.arange(-0.5, len(DISTRICTS), 1), minor=True)
axb.set_yticks(np.arange(-0.5, len(DISTRICTS), 1), minor=True)
axb.grid(which="minor", color="white", linewidth=1.0)
axb.tick_params(which="minor", length=0)

for a in range(len(DISTRICTS)):
    for b in range(len(DISTRICTS)):
        if a == b:
            continue
        value = tv[a, b]
        axb.text(
            b,
            a,
            f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=7.5,
            color="white" if value > 0.55 * TV_MAX else "#08306b",
        )

for a, b in ((i_min, j_min), (j_min, i_min)):
    axb.add_patch(
        Rectangle(
            (b - 0.5, a - 0.5),
            1.0,
            1.0,
            fill=False,
            edgecolor=ACCENT,
            linewidth=1.8,
            zorder=5,
        )
    )

axb.set_xlabel("District")
axb.set_ylabel("District")
axb.set_title("(b) Pairwise dissimilarity of composition", loc="left", pad=8)

cbar = fig.colorbar(im, ax=axb, fraction=0.046, pad=0.03)
cbar.set_label("Total variation distance", fontsize=8.5)
cbar.ax.tick_params(labelsize=7.5)
cbar.outline.set_edgecolor("#666666")
cbar.outline.set_linewidth(0.6)

# --------------------------------------------------------------------------
# 5. Export
# --------------------------------------------------------------------------
here = Path(__file__).resolve().parent

# Pin the PDF timestamps so repeated runs give a byte-identical file
# (matplotlib would otherwise stamp the current time into the metadata).
FIXED_DATE = datetime.datetime(2000, 1, 1, 0, 0, 0)
pdf_metadata = {"CreationDate": FIXED_DATE, "ModDate": FIXED_DATE}

fig.savefig(here / "figure.pdf", metadata=pdf_metadata)
fig.savefig(here / "figure.png", dpi=300)
plt.close(fig)

print(f"wrote {here / 'figure.pdf'}")
print(f"wrote {here / 'figure.png'}")
print(f"most similar pair: {PAIR[0]}-{PAIR[1]}, TV distance = {TV_MIN:.2f}")
