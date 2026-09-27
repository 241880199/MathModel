#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 2 备料工具：R1 / R2 场景的**地面真值**（供 red-evidence.md 判定「图是否支持该判断」）。

只算不设计：数据逐字取自 brief-R1.md / brief-R2.md 的表格。
输出纯文本，逐字贴进 tests/skills/figure-choose/red/red-evidence.md。
"""
import itertools
import math

# ---- R1：六个分区 × 三档脆弱性面积占比（逐字取自 brief-R1.md） ----
R1 = {
    "A": (0.42, 0.35, 0.23),
    "B": (0.31, 0.44, 0.25),
    "C": (0.55, 0.30, 0.15),
    "D": (0.28, 0.47, 0.25),
    "E": (0.37, 0.38, 0.25),
    "F": (0.50, 0.33, 0.17),
}

# ---- R2：5 列 × 6 行（逐字取自 brief-R2.md） ----
FACTORS = {
    "pop_density":  [820, 640, 610, 1210, 990, 1750],
    "mean_slope":   [3.2, 11.5, 2.4, 14.8, 7.1, 5.0],
    "veg_cover":    [0.61, 0.58, 0.72, 0.41, 0.49, 0.55],
    "infra_index":  [74, 72, 81, 55, 66, 70],
}
DISASTER = [12, 31, 8, 38, 16, 24]
DISTRICTS = ["A", "B", "C", "D", "E", "F"]


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    dx = [v - mx for v in x]
    dy = [v - my for v in y]
    cov = sum(a * b for a, b in zip(dx, dy)) / n
    sx = math.sqrt(sum(a * a for a in dx) / n)
    sy = math.sqrt(sum(b * b for b in dy) / n)
    return cov / (sx * sy)


def ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    for pos, i in enumerate(order):
        r[i] = pos + 1.0
    return r


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def main():
    print("## R1 ground truth: pairwise composition similarity (lower L1 = more similar)")
    print("row sums: " + ", ".join(f"{k}={sum(v):.2f}" for k, v in R1.items()))
    pairs = []
    for a, b in itertools.combinations(sorted(R1), 2):
        l1 = sum(abs(p - q) for p, q in zip(R1[a], R1[b]))
        pairs.append((l1, a, b))
    for l1, a, b in sorted(pairs):
        print(f"  L1({a},{b}) = {l1:.2f}")
    print(f"  => most similar pair: {sorted(pairs)[0][1]}-{sorted(pairs)[0][2]}"
          f" (L1={sorted(pairs)[0][0]:.2f}); runner-up"
          f" {sorted(pairs)[1][1]}-{sorted(pairs)[1][2]} (L1={sorted(pairs)[1][0]:.2f})")

    print()
    print("## R2 ground truth: correlation of each factor with historical disaster count")
    print("  (n=6 districts; Pearson and Spearman both shown - small n, so both)")
    rows = []
    for name, vals in FACTORS.items():
        p, s = pearson(vals, DISASTER), spearman(vals, DISASTER)
        rows.append((abs(p), name, p, s))
        print(f"  {name:12s} Pearson r = {p:+.4f}   Spearman rho = {s:+.4f}")
    rows.sort(reverse=True)
    print(f"  => strongest |Pearson|: {rows[0][1]} (r = {rows[0][2]:+.4f})")
    by_rho = sorted(rows, key=lambda t: -abs(t[3]))
    print(f"  => strongest |Spearman|: {by_rho[0][1]} (rho = {by_rho[0][3]:+.4f})")


if __name__ == "__main__":
    main()
