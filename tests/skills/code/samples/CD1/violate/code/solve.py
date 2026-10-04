#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样例求解脚本：用了随机性却未固定随机源（CD1 违规侧）。"""
from pathlib import Path

import numpy as np


def solve() -> dict:
    x = np.random.rand(1000)
    out_dir = Path("build")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "figure-1-samples.csv"
    np.savetxt(out_file, x, delimiter=",")
    return {"mean": float(x.mean()), "file": str(out_file)}
