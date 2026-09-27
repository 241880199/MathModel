#!/usr/bin/env python3
"""Vulnerability composition of six districts (A-F).

The data are three-part compositions: within every district the land-area shares
of the low / medium / high vulnerability tiers sum to 1.00.  The brief asks for
two things, so the figure answers them in two panels:

  (a) 100% stacked bars, one per district, ordered by decreasing low-tier share.
      This is the readout: each district's three shares are labelled directly,
      and because every bar has the same length the internal boundaries can be
      compared across districts at a glance.

  (b) The composition triangle (2-simplex), the canonical display for
      three-part compositions.  A district is a single point whose shares are
      read off the three axes, and *similarity of structure is geometric
      proximity*, so the simplex is exactly the space in which "which two
      districts are most alike?" becomes a question with a visual answer.  The
      pair with the smallest total-variation distance is marked.

Data are the numbers given in the brief, hard-coded below.  The script is
deterministic, offline, and takes no arguments.

Usage:  python make_figure.py
Writes: figure.pdf and figure.png next to this script.
"""

from __future__ import annotations

import itertools
import os

import matplotlib

matplotlib.use("Agg")  # no display needed; keeps the run non-interactive

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

# --------------------------------------------------------------------------
# Data (brief: within every district the three shares sum to 1.00)
# --------------------------------------------------------------------------
TIERS = ("Low", "Medium", "High")

DISTRICTS = {
    "A": (0.42, 0.35, 0.23),
    "B": (0.31, 0.44, 0.25),
    "C": (0.55, 0.30, 0.15),
    "D": (0.28, 0.47, 0.25),
    "E": (0.37, 0.38, 0.25),
    "F": (0.50, 0.33, 0.17),
}

TIER_COLORS = ("#c6dbef", "#6baed6", "#08519c")   # sequential (ColorBrewer Blues)

# --------------------------------------------------------------------------
# Style
# --------------------------------------------------------------------------
H = 3 ** 0.5 / 2.0            # height of a unit equilateral triangle
C_EDGE = "#2b2b2b"
C_GRID = "#e3e3e3"
C_POINT = "#1f3b57"
C_PAIR = "#c0392b"            # the most-similar pair
C_TEXT = "#1a1a1a"

HALO = [pe.withStroke(linewidth=2.6, foreground="white")]


def check_shares() -> None:
    for name, shares in DISTRICTS.items():
        total = sum(shares)
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"shares of district {name} sum to {total}, not 1")


def total_variation(a, b) -> float:
    """Total-variation distance between two compositions (0 = identical)."""
    return 0.5 * sum(abs(x - y) for x, y in zip(a, b))


def closest_pair() -> tuple[str, str, float]:
    """The pair of districts with the smallest structural difference."""
    best = ("", "", float("inf"))
    for i, j in itertools.combinations(sorted(DISTRICTS), 2):
        d = total_variation(DISTRICTS[i], DISTRICTS[j])
        if d < best[2]:
            best = (i, j, d)
    return best


def to_xy(low: float, medium: float, high: float) -> tuple[float, float]:
    """Barycentric composition -> Cartesian point (low=(0,0), med=(1,0), high=(.5,H))."""
    return medium + 0.5 * high, high * H


# --------------------------------------------------------------------------
# Panel (a): 100% stacked bars, ordered by decreasing low-tier share
# --------------------------------------------------------------------------
def draw_composition_bars(ax) -> None:
    order = sorted(DISTRICTS, key=lambda n: -DISTRICTS[n][0])
    y = np.arange(len(order))[::-1]          # first district at the top

    for yi, name in zip(y, order):
        left = 0.0
        for k, share in enumerate(DISTRICTS[name]):
            ax.barh(yi, share, left=left, height=0.66,
                    color=TIER_COLORS[k], edgecolor="white", linewidth=0.9,
                    zorder=3)
            ax.text(left + share / 2.0, yi, f"{share:.2f}",
                    ha="center", va="center", fontsize=7.6,
                    color="white" if k == 2 else "#12324d", zorder=4)
            left += share

    ax.set_yticks(y)
    ax.set_yticklabels(order, fontsize=10)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(np.arange(0.0, 1.01, 0.2))
    ax.set_xticklabels([f"{t:.1f}" for t in np.arange(0.0, 1.01, 0.2)],
                       fontsize=8.5)
    ax.set_xlabel("Share of district land area", fontsize=9)
    ax.xaxis.grid(True, color="#e8e8e8", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#9a9a9a")
        ax.spines[side].set_linewidth(0.8)
    ax.tick_params(length=2.5, color="#9a9a9a")

    handles = [plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor="white")
               for c in TIER_COLORS]
    ax.legend(handles, [f"{t} vulnerability" for t in TIERS],
              loc="upper center", bbox_to_anchor=(0.5, -0.135),
              ncol=3, frameon=False, fontsize=8.5,
              handlelength=1.1, handleheight=0.9, columnspacing=1.4,
              borderpad=0.0)


# --------------------------------------------------------------------------
# Panel (b): the composition triangle
# --------------------------------------------------------------------------
def draw_composition_triangle(ax, pair_a: str, pair_b: str, pair_d: float) -> None:
    # 0.1 gridlines, each parallel to one edge
    for k in range(1, 10):
        t = k / 10.0
        for p, q in (
            (to_xy(1 - t, 0.0, t), to_xy(0.0, 1 - t, t)),   # constant high
            (to_xy(t, 1 - t, 0.0), to_xy(t, 0.0, 1 - t)),   # constant low
            (to_xy(1 - t, t, 0.0), to_xy(0.0, t, 1 - t)),   # constant medium
        ):
            ax.plot([p[0], q[0]], [p[1], q[1]], color=C_GRID, lw=0.55, zorder=1)

    # the closest pair: connector first so the markers sit on top of it
    ca, cb = to_xy(*DISTRICTS[pair_a]), to_xy(*DISTRICTS[pair_b])
    mid = ((ca[0] + cb[0]) / 2.0, (ca[1] + cb[1]) / 2.0)
    ax.plot([ca[0], cb[0]], [ca[1], cb[1]], color=C_PAIR, lw=2.4,
            solid_capstyle="round", zorder=3)

    # every district
    for name, shares in DISTRICTS.items():
        x, y = to_xy(*shares)
        is_pair = name in (pair_a, pair_b)
        ax.plot(x, y, marker="o", ms=6.6 if is_pair else 6.0,
                mfc=C_PAIR if is_pair else C_POINT, mec="white", mew=1.0,
                ls="none", zorder=4)

    # callout for the closest pair, floating directly above the red connector
    ax.text(mid[0], 0.325,
            f"most similar pair\n{pair_a}–{pair_b}: {pair_d:.2f} apart",
            ha="center", va="bottom", fontsize=7.8, color=C_PAIR,
            linespacing=1.4, path_effects=HALO, zorder=6)

    # District labels.  The six points sit in a tight cluster in the middle of
    # the simplex, so the labels are pushed out into the free space around it
    # and tied to their own marker with a visible leader line -- proximity
    # alone would leave A/E and C/F ambiguous.
    offsets = {
        "A": (-0.103, 0.039),
        "B": (-0.045, 0.052),
        "C": (-0.120, -0.032),
        "D": (0.077, 0.000),
        "E": (0.015, -0.124),
        "F": (-0.043, -0.099),
    }
    for name, shares in DISTRICTS.items():
        x, y = to_xy(*shares)
        dx, dy = offsets[name]
        is_pair = name in (pair_a, pair_b)
        ax.annotate(name, xy=(x, y), xytext=(x + dx, y + dy),
                    ha="center", va="center", fontsize=9.5,
                    fontweight="bold" if is_pair else "normal",
                    color=C_PAIR if is_pair else C_TEXT,
                    path_effects=HALO, zorder=6,
                    arrowprops=dict(arrowstyle="-", lw=0.6, color="#8c8c8c",
                                    shrinkA=3.0, shrinkB=2.0))

    # triangle outline, ticks and axis titles
    ax.plot([0.0, 1.0, 0.5, 0.0], [0.0, 0.0, H, 0.0],
            color=C_EDGE, lw=1.1, solid_joinstyle="miter", zorder=2)

    n_left, n_right, n_bottom = (-H, 0.5), (H, 0.5), (0.0, -1.0)
    for k in range(1, 10):
        t = k / 10.0
        for p, n, ha in (
            ((t, 0.0), n_bottom, "center"),
            (to_xy(t, 0.0, 1 - t), n_left, "right"),
            (to_xy(0.0, 1 - t, t), n_right, "left"),
        ):
            ax.plot([p[0], p[0] + 0.014 * n[0]], [p[1], p[1] + 0.014 * n[1]],
                    color=C_EDGE, lw=0.8, zorder=2)
            ax.text(p[0] + 0.044 * n[0], p[1] + 0.044 * n[1], f"{t:.1f}",
                    ha=ha, va="top" if n is n_bottom else "center",
                    fontsize=8, color=C_TEXT, path_effects=HALO, zorder=5)

    ax.text(0.5, -0.105, "Low share", ha="center", va="top",
            fontsize=9, color=C_TEXT)
    ax.text(0.25 + 0.185 * n_left[0], H / 2 + 0.185 * n_left[1],
            "Medium share", ha="center", va="center",
            fontsize=9, color=C_TEXT, rotation=60, rotation_mode="anchor")
    ax.text(0.75 + 0.185 * n_right[0], H / 2 + 0.185 * n_right[1],
            "High share", ha="center", va="center",
            fontsize=9, color=C_TEXT, rotation=-60, rotation_mode="anchor")

    ax.set_xlim(-0.19, 1.21)
    ax.set_ylim(-0.175, 0.98)
    ax.set_aspect("equal", adjustable="box")
    ax.set_anchor("N")
    ax.axis("off")


# --------------------------------------------------------------------------
def main() -> None:
    check_shares()
    pair_a, pair_b, pair_d = closest_pair()

    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "pdf.fonttype": 42,   # embed as TrueType so the text stays selectable
        "ps.fonttype": 42,
    })

    fig, (ax_a, ax_b) = plt.subplots(
        1, 2, figsize=(7.6, 4.0), gridspec_kw={"width_ratios": [0.98, 1.0]}
    )
    draw_composition_bars(ax_a)
    draw_composition_triangle(ax_b, pair_a, pair_b, pair_d)

    for ax, tag in ((ax_a, "(a)"), (ax_b, "(b)")):
        ax.text(0.0, 1.02, tag, transform=ax.transAxes, fontsize=9.5,
                fontweight="bold", color=C_TEXT, ha="left", va="bottom")

    fig.subplots_adjust(left=0.052, right=0.995, top=0.955, bottom=0.16,
                        wspace=0.08)

    here = os.path.dirname(os.path.abspath(__file__))
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(here, f"figure.{ext}"), dpi=300,
                    facecolor="white",
                    # drop the embedded timestamps so re-running the script
                    # reproduces the same file byte for byte
                    metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)

    print(f"wrote figure.pdf / figure.png in {here}")
    print(f"closest pair: {pair_a}-{pair_b}, total variation {pair_d:.3f}")


if __name__ == "__main__":
    main()
