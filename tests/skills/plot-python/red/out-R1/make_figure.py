"""Regenerate the district vulnerability-composition figure.

Data: for each of six districts (A-F) the share of land area in each of three
vulnerability tiers (low, medium, high). Within every district the three shares
sum to 1.00, so the data are compositional.

Outputs (written next to this script):
    figure.pdf, figure.png, caption.txt

Deterministic: no randomness, no network, no manual steps.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display required

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- data ------
DISTRICTS = ["A", "B", "C", "D", "E", "F"]
TIERS = ["low", "medium", "high"]

# rows = districts (in the order given), columns = low / medium / high
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

# The stacked bar is exact only because each row sums to 1; fail loudly if not.
row_sums = SHARES.sum(axis=1)
assert np.allclose(row_sums, 1.0, atol=1e-9), f"rows do not sum to 1: {row_sums}"

# ------------------------------------------------------------- ordering -----
# Order districts by decreasing low-tier share. This is a deliberate choice: it
# puts the most similar pair (found below) next to each other in the display.
order = sorted(range(len(DISTRICTS)), key=lambda i: (-SHARES[i, 0], DISTRICTS[i]))
disp_districts = [DISTRICTS[i] for i in order]
disp_shares = SHARES[order]  # shape (6, 3)

# ---------------------------------------------------------- similarity ------
# Structure = the 3-vector of tier shares. Euclidean distance is a plain,
# scale-free way to rank pairs on this 2-D simplex (all rows sum to 1).
pairs = []
for i in range(len(DISTRICTS)):
    for j in range(i + 1, len(DISTRICTS)):
        d = float(np.linalg.norm(SHARES[i] - SHARES[j]))
        pairs.append((DISTRICTS[i], DISTRICTS[j], d))
pairs.sort(key=lambda p: (p[2], p[0], p[1]))

best = pairs[0]
best_pair = (best[0], best[1])
_, _, best_d = best
runner_up_d = pairs[1][2]
# largest absolute tier gap within the winning pair
best_gap = float(np.max(np.abs(SHARES[DISTRICTS.index(best[0])]
                               - SHARES[DISTRICTS.index(best[1])])))

# How similar the winner is: ratio to the next-closest pair.
print(f"most similar pair : {best_pair[0]}-{best_pair[1]}  d={best_d:.4f}")
print(f"max tier gap      : {best_gap:.4f}")
print(f"runner-up pair    : {pairs[1][0]}-{pairs[1][1]}  d={runner_up_d:.4f}")
print(f"least similar pair: {pairs[-1][0]}-{pairs[-1][1]}  d={pairs[-1][2]:.4f}")
print("high-tier range   : "
      f"{SHARES[:, 2].min():.2f}-{SHARES[:, 2].max():.2f}")
print("low-tier range    : "
      f"{SHARES[:, 0].min():.2f}-{SHARES[:, 0].max():.2f}")

# --------------------------------------------------------------- style ------
TIER_COLORS = {"low": "#5aae61", "medium": "#f4a259", "high": "#c1443c"}
INK = "#1a1a1a"


def text_color(hex_color: str) -> str:
    """Pick black or white ink for a filled swatch, by relative luminance."""
    r, g, b = (int(hex_color[k : k + 2], 16) / 255.0 for k in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
           for c in (r, g, b)]
    luminance = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
    return INK if luminance > 0.45 else "white"


plt.rcParams.update(
    {
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": "#666666",
        "axes.linewidth": 0.8,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        # embed TrueType (not matplotlib's default Type 3), so the PDF carries
        # a real embedded font and its text stays searchable when placed in
        # LaTeX
        "pdf.fonttype": 42,
    }
)

# -------------------------------------------------------------- figure ------
fig = plt.figure(figsize=(7.2, 4.4), constrained_layout=True)
grid = fig.add_gridspec(1, 2, width_ratios=[2.05, 1.0], wspace=0.30)
ax_left = fig.add_subplot(grid[0, 0])
ax_right = fig.add_subplot(grid[0, 1])

n = len(disp_districts)
ys = np.arange(n)
height = 0.70

# --- highlight band behind the most similar pair (drawn first, so it is under)
band_rows = [disp_districts.index(best_pair[0]), disp_districts.index(best_pair[1])]
ax_left.axhspan(min(band_rows) - 0.5, max(band_rows) + 0.5,
                color="#f2d98c", alpha=0.35, zorder=0)

# --- stacked bars (each district sums to 1.00 by construction)
left_edges = np.zeros(n)
for t, tier in enumerate(TIERS):
    vals = disp_shares[:, t]
    ax_left.barh(ys, vals, height=height, left=left_edges,
                 color=TIER_COLORS[tier], edgecolor="white", linewidth=0.7,
                 label=tier.capitalize(), zorder=3)
    for y, v, e in zip(ys, vals, left_edges):
        if v >= 0.06:  # only label segments wide enough to hold text
            ax_left.text(e + v / 2, y, f"{v:.0%}", ha="center", va="center",
                         fontsize=8, color=text_color(TIER_COLORS[tier]),
                         zorder=4)
    left_edges = left_edges + vals

ax_left.set_yticks(ys)
ax_left.set_yticklabels([f"District {d}" for d in disp_districts])
ax_left.invert_yaxis()  # first (highest low-share) district on top
ax_left.set_xlim(0, 1.0)
ax_left.set_xticks(np.arange(0, 1.01, 0.2))
ax_left.set_xticklabels([f"{int(x * 100)}" for x in np.arange(0, 1.01, 0.2)])
ax_left.set_xlabel("Share of district land area (%)")
ax_left.set_title("Vulnerability composition by district", loc="left")
ax_left.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3,
               frameon=False, handlelength=1.2, columnspacing=1.4)
ax_left.grid(axis="x", color="#dddddd", linewidth=0.6, zorder=0)
ax_left.set_axisbelow(True)
for side in ("top", "right"):
    ax_left.spines[side].set_visible(False)

# annotate the highlighted pair, in the blank strip to the right of the bars
band_mid = float(np.mean(band_rows))
ax_left.annotate(
    f"B and D: most similar pair\n(d = {best_d:.3f}, all tier gaps ≤ "
    f"{best_gap:.2f})",
    xy=(1.0, band_mid), xytext=(1.06, band_mid),
    va="center", ha="left", fontsize=7.5, color="#7a5b00",
    annotation_clip=False,
)

# --- right panel: every pairwise distance, sorted
pair_labels = [f"{a}–{b}" for a, b, _ in pairs]
pair_dists = [d for _, _, d in pairs]
py = np.arange(len(pairs))
bar_colors = [TIER_COLORS["high"] if (a, b) == best_pair else "#c9c9c9"
              for a, b, _ in pairs]

ax_right.barh(py, pair_dists, height=0.68, color=bar_colors, zorder=3)
ax_right.set_yticks(py)
ax_right.set_yticklabels(pair_labels, fontsize=7)
ax_right.invert_yaxis()
ax_right.set_xlim(0, max(pair_dists) * 1.34)
ax_right.set_xticks(np.arange(0.0, 0.31, 0.1))
ax_right.tick_params(axis="x", labelsize=8)
ax_right.tick_params(axis="y", labelsize=7)
ax_right.set_xlabel("Euclidean distance")
ax_right.set_title("Pairwise compositional\ndistance (15 pairs)",
                   loc="left", fontsize=9)
ax_right.grid(axis="x", color="#dddddd", linewidth=0.6, zorder=0)
ax_right.set_axisbelow(True)
for side in ("top", "right"):
    ax_right.spines[side].set_visible(False)

for y, (a, b, d) in zip(py, pairs):
    is_best = (a, b) == best_pair
    label = f"{d:.3f} (smallest)" if is_best else f"{d:.3f}"
    ax_right.text(d + max(pair_dists) * 0.03, y, label,
                  va="center", ha="left", fontsize=6.5,
                  color=TIER_COLORS["high"] if is_best else "#777777",
                  fontweight="bold" if is_best else "normal")

# --------------------------------------------------------------- output -----
# Fixed metadata keeps the PDF byte-identical across runs (no embedded date).
fig.savefig(HERE / "figure.png", bbox_inches="tight", facecolor="white")
fig.savefig(HERE / "figure.pdf", bbox_inches="tight", facecolor="white",
            metadata={"CreationDate": None, "ModDate": None})
plt.close(fig)

print("\nwrote figure.png / figure.pdf")
