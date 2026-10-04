#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样例求解脚本：入口固定随机源（Python）。"""
from pathlib import Path

import numpy as np

SEED = 2025


def solve(seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    x = rng.random(1000)
    out_dir = Path("build")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "figure-1-samples.csv"
    np.savetxt(out_file, x, delimiter=",")
    return {"mean": float(x.mean()), "file": str(out_file)}


if __name__ == "__main__":
    print(solve())
