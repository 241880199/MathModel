#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figure for Brief R2 - drivers of historical disaster counts.

Data relationship (figure-choose decision tree, entry 3 "correlation"):
five continuous attributes observed on the same six districts, and the
question has two layers that the same data relationship carries --

  (a) which factor moves together with the historical disaster count
      -> the disaster-count column of the scatter matrix, drawn as four
         scatter panels (one per predictor) on a shared disaster-count axis,
         ordered by |r| so the ranking is read left to right;
  (b) how similar the districts are to each other
      -> parallel coordinates: the same six individuals traced across all
         five standardised axes (the alternative listed for this entry when
         the multi-dimensional layer matters, not only the pairwise one).

Deterministic: numbers typed in below, no randomness, no network, no
manual steps.  Run ``python make_figure.py`` -- it rewrites figure.png,
figure.pdf and caption.txt next to this file.
"""

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "figure.png")
OUT_PDF = os.path.join(HERE, "figure.pdf")
OUT_TXT = os.path.join(HERE, "caption.txt")

# --------------------------------------------------------------------------
# Data (Brief R2 table, in the brief's column order)
# --------------------------------------------------------------------------
DISTRICTS = ["A", "B", "C", "D", "E", "F"]
POP, SLOPE, VEG, DIS, INFRA = range(5)

DATA = np.array(
    [
        # population density, mean slope, vegetation cover, disaster count, infrastructure
        [820.0, 3.2, 0.61, 12.0, 74.0],  # A
        [640.0, 11.5, 0.58, 31.0, 72.0],  # B
        [610.0, 2.4, 0.72, 8.0, 81.0],  # C
        [1210.0, 14.8, 0.41, 38.0, 55.0],  # D
        [990.0, 7.1, 0.49, 16.0, 66.0],  # E
        [1750.0, 5.0, 0.55, 24.0, 70.0],  # F
    ],
    dtype=float,
)

# predictor panels: (column, title, x-axis unit)
PREDICTORS = [
    (SLOPE, "Mean slope", "degrees"),
    (INFRA, "Infrastructure index", "index (0-100)"),
    (VEG, "Vegetation cover", "fraction of area"),
    (POP, "Population density", "people/km$^2$"),
]

# parallel-coordinate axes, in the brief's column order
PC_AXES = [
    (POP, "Population density\n(people/km$^2$)"),
    (SLOPE, "Mean slope\n(degrees)"),
    (VEG, "Vegetation cover\n(fraction of area)"),
    (DIS, "Historical\ndisaster count"),
    (INFRA, "Infrastructure\nindex (0-100)"),
]

CAPTION = "Figure 1: Scatter panels rank slope first; A and C share a profile"

# --------------------------------------------------------------------------
# House style: <=4 main colours, no matplotlib default colour order, grey is
# a normal choice, no top/right spines, ticks inward, unit-bearing labels.
# --------------------------------------------------------------------------
C_HI = "#C1440E"  # accent: the district that stands apart
C_PAIR = "#16697A"  # accent: the two most alike districts
C_GRAY = "#8C8C8C"  # the rest
C_INK = "#333333"  # text / markers
C_SOFT = "#B0B0B0"  # axes of the profile panel, light rules

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.linewidth": 0.8,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "axes.unicode_minus": False,
        "figure.dpi": 200,
        "savefig.dpi": 200,
        "lines.solid_capstyle": "round",
    }
)


# --------------------------------------------------------------------------
# Statistics (plain numpy -- no scipy, nothing random)
# --------------------------------------------------------------------------
def pearson(a, b):
    """Pearson product-moment correlation of two 1-D arrays."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    a = a - a.mean()
    b = b - b.mean()
    return float(a @ b / np.sqrt((a @ a) * (b @ b)))


TARGET = DATA[:, DIS]
R_BY_COL = {col: pearson(DATA[:, col], TARGET) for col, _, _ in PREDICTORS}

# profiles live on a comparable scale only after standardising each attribute
Z = (DATA - DATA.mean(axis=0)) / DATA.std(axis=0, ddof=1)

# the most alike pair = smallest Euclidean distance in standardised space
_pair = None
for _i in range(len(DISTRICTS)):
    for _j in range(_i + 1, len(DISTRICTS)):
        _d = float(np.linalg.norm(Z[_i] - Z[_j]))
        if _pair is None or _d < _pair[0] - 1e-12:
            _pair = (_d, _i, _j)
PAIR = (DISTRICTS[_pair[1]], DISTRICTS[_pair[2]])

# the district that stands apart = largest mean distance to the others
_meand = {
    d: float(np.mean([np.linalg.norm(Z[i] - Z[j]) for j in range(len(DISTRICTS)) if j != i]))
    for i, d in enumerate(DISTRICTS)
}
OUTLIER = max(DISTRICTS, key=lambda d: _meand[d])

COLOR = {d: C_GRAY for d in DISTRICTS}
COLOR[PAIR[0]] = COLOR[PAIR[1]] = C_PAIR
COLOR[OUTLIER] = C_HI


def num(v):
    """Compact axis label: 610 / 2.4 / 0.61."""
    return f"{int(round(v))}" if abs(v - round(v)) < 1e-9 else f"{v:g}"


# --------------------------------------------------------------------------
# Label placement: pick, per point, the first free slot from a fixed list
# --------------------------------------------------------------------------
_OFFSETS = [
    (4.0, 0.0, "left", "center"),
    (-4.0, 0.0, "right", "center"),
    (0.0, 5.0, "center", "bottom"),
    (0.0, -5.0, "center", "top"),
    (4.0, 4.0, "left", "bottom"),
    (-4.0, 4.0, "right", "bottom"),
    (4.0, -4.0, "left", "top"),
    (-4.0, -4.0, "right", "top"),
]


def pick_corner(ax, xs, ys, txt, fontsize=8.0):
    """Pick the corner of the panel that no point occupies, and box it.

    Returns (anchor, reserved_box) where ``anchor`` is (x, y, ha, va) in axes
    fractions and ``reserved_box`` is (x0, x1, y0, y1) in display pixels, so
    that the point labels placed afterwards keep clear of the readout.
    """
    pp = ax.figure.dpi / 72.0
    w = 0.68 * fontsize * len(txt) * pp + 4.0 * pp
    h = 1.10 * fontsize * pp + 4.0 * pp
    bw, bh = ax.bbox.width, ax.bbox.height
    frac_w, frac_h = w / bw, h / bh
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    fx = (np.asarray(xs) - x0) / (x1 - x0)
    fy = (np.asarray(ys) - y0) / (y1 - y0)

    best = None
    for ax_x, ax_y, ha, va in [
        (0.045, 0.935, "left", "top"),
        (0.955, 0.935, "right", "top"),
        (0.045, 0.065, "left", "bottom"),
        (0.955, 0.065, "right", "bottom"),
    ]:
        bx0 = ax_x if ha == "left" else ax_x - frac_w
        by1 = ax_y if va == "top" else ax_y + frac_h
        bx1, by0 = bx0 + frac_w, by1 - frac_h
        pad = 0.025
        hits = int(
            np.sum(
                (fx > bx0 - pad)
                & (fx < bx1 + pad)
                & (fy > by0 - pad)
                & (fy < by1 + pad)
            )
        )
        box_px = (bx0 * bw, bx1 * bw, by0 * bh, by1 * bh)
        if best is None or hits < best[0]:
            best = (hits, (ax_x, ax_y, ha, va), box_px)
    return best[1], best[2]


def place_point_labels(ax, xs, ys, labels, colors, reserved=(), fontsize=8.0):
    """Put one short label next to each point, in the first slot that is free.

    Slots are tried in a fixed order, collisions are checked against the
    markers, against anything already reserved, and against labels already
    placed, so the result is deterministic.
    """
    fig = ax.figure
    pp = fig.dpi / 72.0
    pts = ax.transData.transform(np.column_stack([xs, ys]))
    taken = list(reserved) + [
        (px - 4.0, px + 4.0, py - 4.0, py + 4.0) for px, py in pts
    ]
    for (px, py), lab, col, x, y in zip(pts, labels, colors, xs, ys):
        w = 0.68 * fontsize * len(lab) * pp
        h = 1.10 * fontsize * pp
        for dx, dy, ha, va in _OFFSETS:
            cx, cy = px + dx * pp, py + dy * pp
            x0 = cx if ha == "left" else (cx - w if ha == "right" else cx - w / 2.0)
            y0 = cy - h / 2.0 if va == "center" else (cy if va == "bottom" else cy - h)
            box = (x0, x0 + w, y0, y0 + h)
            if any(
                box[0] < t[1] and t[0] < box[1] and box[2] < t[3] and t[2] < box[3]
                for t in taken
            ):
                continue
            taken.append(box)
            ax.annotate(
                lab,
                (x, y),
                textcoords="offset points",
                xytext=(dx, dy),
                ha=ha,
                va=va,
                fontsize=fontsize,
                color=col,
                zorder=5,
            )
            break


# --------------------------------------------------------------------------
# Figure
# --------------------------------------------------------------------------
def build_figure():
    fig = plt.figure(figsize=(6.31, 4.75))
    fig.patch.set_facecolor("white")

    # ---- (a) one scatter panel per predictor, shared disaster-count axis ----
    panels = sorted(PREDICTORS, key=lambda t: -abs(R_BY_COL[t[0]]))
    n = len(panels)
    left, right, gap = 0.085, 0.985, 0.055
    w = (right - left - (n - 1) * gap) / n
    y_bottom, y_height = 0.600, 0.300

    y_lo, y_hi = 0.0, 42.0
    first = None
    for i, (col, title, unit) in enumerate(panels):
        ax = fig.add_axes([left + i * (w + gap), y_bottom, w, y_height])
        if first is None:
            first = ax
        xs = DATA[:, col]
        ys = TARGET
        colors = [COLOR[d] for d in DISTRICTS]

        pad = 0.10 * (xs.max() - xs.min())
        ax.set_xlim(xs.min() - pad, xs.max() + pad)
        ax.set_ylim(y_lo, y_hi)

        # correlation readout first: it claims the corner that holds no point,
        # and the district letters are then placed around it
        txt = f"r = {R_BY_COL[col]:+.2f}"
        (ax_x, ax_y, ha, va), reserved = pick_corner(ax, xs, ys, txt)
        ax.text(
            ax_x,
            ax_y,
            txt,
            transform=ax.transAxes,
            ha=ha,
            va=va,
            fontsize=8,
            color=C_INK,
            fontweight="bold" if i == 0 else "normal",
            zorder=6,
        )

        ax.scatter(
            xs,
            ys,
            s=18,
            facecolors=colors,
            edgecolors="white",
            linewidths=0.5,
            zorder=4,
        )
        place_point_labels(ax, xs, ys, DISTRICTS, colors, reserved=(reserved,))

        ax.set_title(title, pad=5.0, color=C_INK, fontweight="bold" if i == 0 else "normal")
        ax.set_xlabel(unit, labelpad=2.0, color=C_INK)
        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.xaxis.set_major_formatter(lambda v, _p: num(v))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
        ax.yaxis.set_major_formatter(lambda v, _p: num(v))
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(C_INK)
        ax.tick_params(colors=C_INK)
        if i == 0:
            ax.set_ylabel("Historical disaster count", labelpad=2.0, color=C_INK)
        else:
            ax.tick_params(labelleft=False)

    # ---- (b) parallel coordinates: the six districts across all attributes --
    axp = fig.add_axes([left, 0.075, right - left, 0.395])
    axp.set_axis_off()
    axp.set_xlim(-0.30, 4.62)
    axp.set_ylim(-0.30, 1.32)

    n_ax = len(PC_AXES)
    for j, (col, name) in enumerate(PC_AXES):
        vals = DATA[:, col]
        lo, hi = float(vals.min()), float(vals.max())
        axp.plot([j, j], [0.0, 1.0], color=C_SOFT, lw=0.8, zorder=1)
        axp.plot([j - 0.03, j + 0.03], [0.0, 0.0], color=C_SOFT, lw=0.8, zorder=1)
        axp.plot([j - 0.03, j + 0.03], [1.0, 1.0], color=C_SOFT, lw=0.8, zorder=1)
        axp.text(
            j,
            1.045,
            name,
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=C_INK,
            linespacing=1.2,
        )
        axp.text(j - 0.045, -0.045, num(lo), ha="right", va="top", fontsize=7.5, color=C_INK)
        axp.text(j + 0.045, -0.045, num(hi), ha="left", va="top", fontsize=7.5, color=C_INK)

    # min-max scaled so that profiles are comparable across attributes
    scaled = (DATA - DATA.min(axis=0)) / (DATA.max(axis=0) - DATA.min(axis=0))
    for i, d in enumerate(DISTRICTS):
        axp.plot(
            range(n_ax),
            scaled[i],
            color=COLOR[d],
            lw=1.1,
            marker="o",
            markersize=2.6,
            markeredgecolor="white",
            markeredgewidth=0.4,
            zorder=3,
        )

    # district letters at the right edge, nudged apart if they collide
    ends = [float(scaled[i, n_ax - 1]) for i in range(len(DISTRICTS))]
    order = sorted(range(len(ends)), key=lambda i: ends[i])
    min_gap = 0.10
    placed = list(ends)
    for k in range(1, len(order)):
        i_prev, i_cur = order[k - 1], order[k]
        if placed[i_cur] - placed[i_prev] < min_gap:
            placed[i_cur] = placed[i_prev] + min_gap
    shift = 0.5 * (sum(ends) / len(ends) - sum(placed) / len(placed))
    placed = [v + shift for v in placed]
    for i, d in enumerate(DISTRICTS):
        if abs(placed[i] - ends[i]) > 0.012:
            axp.plot(
                [n_ax - 1 + 0.02, n_ax - 1 + 0.10],
                [ends[i], placed[i]],
                color=C_SOFT,
                lw=0.6,
                zorder=2,
            )
        axp.text(
            n_ax - 1 + 0.12,
            placed[i],
            d,
            ha="left",
            va="center",
            fontsize=8,
            color=COLOR[d],
            fontweight="bold",
            zorder=5,
        )

    # the near-duplicate pair of predictors the ranking cannot separate
    r_veg_infra = pearson(DATA[:, VEG], DATA[:, INFRA])
    axp.text(
        -0.30,
        -0.235,
        "Vegetation cover and infrastructure index co-vary "
        f"(r = {r_veg_infra:+.2f}): treat them as one effect",
        ha="left",
        va="center",
        fontsize=7.5,
        color=C_INK,
    )

    return fig


def main():
    fig = build_figure()
    fig.savefig(OUT_PNG, dpi=200, facecolor="white")
    # drop the two wall-clock fields so that regenerating gives the same bytes
    fig.savefig(
        OUT_PDF,
        facecolor="white",
        metadata={"CreationDate": None, "ModDate": None},
    )
    plt.close(fig)

    with open(OUT_TXT, "w", encoding="utf-8") as fh:
        fh.write(CAPTION + "\n")

    print(f"districts closest in profile: {PAIR[0]}-{PAIR[1]}")
    print(f"district that stands apart:   {OUTLIER}")
    for col, title, _unit in PREDICTORS:
        print(f"r(disaster count, {title:<22}) = {R_BY_COL[col]:+.3f}")
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")
    print(f"wrote {OUT_TXT}")


if __name__ == "__main__":
    main()
