#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""样例求解脚本：只打印不落盘（CD2 违规侧）。"""
import numpy as np

SEED = 2025


def solve(seed: int = SEED) -> float:
    rng = np.random.default_rng(seed)
    x = rng.random(1000)
    print(float(x.mean()))
    return float(x.mean())
