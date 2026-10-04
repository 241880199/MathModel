#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcm-code 最小可复现骨架（Python · 零参可跑）。

★ 三件事一次演示（本 skill 的可复现规范）：
  (1) 固定随机源 —— 入口即 ``numpy.random.default_rng(<固定种子>)``，同样输入必得同样结果；
  (2) 结果落盘   —— 用 csv / json 把结果写到磁盘（**不是只 print**）；
  (3) 编号对齐   —— **进正文的成品**文件名带论文编号（``table-1-*`` / ``figure-1-*``），与正文 表 1 / 图 1 对得上。

用法（**零参可跑**）：
    python .claude/skills/mcm-code/assets/scaffold.py
    python .claude/skills/mcm-code/assets/scaffold.py --outdir build/my-run --seed 2026 --n-samples 100000

★ 不写死机器绝对路径：默认输出目录是**相对**路径（``build/...``，已入 .gitignore），可经 ``--outdir`` 改。
★ 本骨架**不给算法** —— 例中的蒙特卡洛估 pi 只是"可跑的最小例子"，整体替换为你的模型即可。
★ 成品与工作转储**分目录**：带编号的成品（``table-1-*`` / ``figure-1-*``）落 ``out_dir``；**不进正文**的工作转储
  （``run-summary.json``）落 ``out_dir/work/`` —— 即 ``references/numbering.md``「中间产物可以不带编号，
  但别与带编号的成品混在同一目录」的落地。
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import numpy as np

SEED = 2025
N_SAMPLES = 20000


def run(out_dir: Path, seed: int = SEED, n_samples: int = N_SAMPLES) -> dict:
    """跑一遍最小可复现实验并把结果落盘；返回读数与落盘文件路径。"""
    rng = np.random.default_rng(seed)                  # ★ (1) 固定随机源

    # 可跑的最小例子：用蒙特卡洛估 pi（可整体替换为你的模型）
    x = rng.random(n_samples)
    y = rng.random(n_samples)
    in_circle = (x ** 2 + y ** 2) <= 1.0
    p = float(in_circle.mean())
    pi_hat = 4.0 * p

    # 95% 置信区间（正态近似）
    se = 4.0 * float(np.sqrt(p * (1.0 - p) / n_samples))
    ci95 = (pi_hat - 1.96 * se, pi_hat + 1.96 * se)

    # —— (2) 结果落盘 + (3) 文件名带编号 ——
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir / "work"                        # ★ 工作转储单独落，不混成品
    work_dir.mkdir(parents=True, exist_ok=True)

    # 图 1 的原始数据 -> figure-1-samples.csv（对应正文 图 1）
    fig_file = out_dir / "figure-1-samples.csv"        # ★ (3) figure-1 ↔ 正文 图 1
    with fig_file.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["x", "y", "in_circle"])
        w.writerows(zip(x.tolist(), y.tolist(), in_circle.astype(int).tolist()))

    # 表 1 的结果 -> table-1-estimate.csv（对应正文 表 1）
    tbl_file = out_dir / "table-1-estimate.csv"        # ★ (3) table-1 ↔ 正文 表 1
    with tbl_file.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pi_hat", "ci95_lo", "ci95_hi", "n_samples", "seed"])
        w.writerow([f"{pi_hat:.6f}", f"{ci95[0]:.6f}", f"{ci95[1]:.6f}", n_samples, seed])

    # 整包读数 -> work/run-summary.json（`json` / `np.save` 之一例）
    # 不进正文的工作转储：不带编号、另置 work/，别与带编号的成品混放（见 references/numbering.md）
    json_file = work_dir / "run-summary.json"          # ★ (2) 落盘
    payload = {
        "pi_hat": pi_hat,
        "ci95": [ci95[0], ci95[1]],
        "n_samples": int(n_samples),
        "seed": int(seed),
    }
    json_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return {
        "out_dir": str(out_dir),
        "seed": int(seed),
        "pi_hat": pi_hat,
        "ci95": [ci95[0], ci95[1]],
        "files": [str(fig_file), str(tbl_file), str(json_file)],
    }


def main(argv: list[str] | None = None) -> dict:
    ap = argparse.ArgumentParser(description="mcm-code 最小可复现骨架（零参可跑）")
    ap.add_argument("--outdir", default=str(Path("build") / "mcm-code-scaffold" / "python"),
                    help="产物目录（默认相对路径 build/mcm-code-scaffold/python，已入 .gitignore）")
    ap.add_argument("--seed", type=int, default=SEED, help="固定随机源的种子")
    ap.add_argument("--n-samples", type=int, default=N_SAMPLES, help="样本量")
    args = ap.parse_args(argv)

    res = run(Path(args.outdir), args.seed, args.n_samples)
    print(f"[scaffold] (1) 固定随机源 seed = {res['seed']}")
    print(f"[scaffold] (2) 结果落盘 -> {res['out_dir']}")
    print("[scaffold] (3) 编号对齐：figure-1-samples.csv / table-1-estimate.csv")
    print(f"[scaffold]     不进正文的工作转储 -> {res['files'][2]}")
    print(f"[scaffold] pi_hat = {res['pi_hat']:.6f}  (95% CI {res['ci95'][0]:.6f}, {res['ci95'][1]:.6f})")
    return res


if __name__ == "__main__":
    main()
