#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样例求解脚本：CD5 违规侧 —— 可执行语句里写死了机器绝对路径。"""
from pathlib import Path

import numpy as np

SEED = 2025


def solve(seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    x = np.load('C:\\Users\\alice\\mcm\\data.npy')
    out_dir = Path("build")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "figure-1-samples.csv"
    np.savetxt(out_file, x, delimiter=",")
    return {"mean": float(x.mean()), "file": str(out_file)}
