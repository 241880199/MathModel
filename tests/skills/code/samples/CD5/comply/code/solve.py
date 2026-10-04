#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样例求解脚本：CD5 合规侧 —— 绝对路径只出现在注释里。"""
from pathlib import Path

import numpy as np

SEED = 2025


def solve(seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    # 说明（注释，不算违规）：旧机器路径 /Users/alice/mcm/table1.csv，现已改为相对路径。
    x = rng.random(1000)
    out_dir = Path("build")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "figure-1-samples.csv"
    np.savetxt(out_file, x, delimiter=",")
    return {"mean": float(x.mean()), "file": str(out_file)}
