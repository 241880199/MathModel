#!/usr/bin/env python3
"""Summarise checkcode-report.txt: separate fatal parse errors from style noise.

Usage:  python tests/algorithms/analyze_checkcode.py [report.txt]
"""
import collections
import io
import os
import sys

REPORT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "checkcode-report.txt")

# Directories authored by the repo owner (tier 1 = "directly usable" in INDEX.md).
# Everything else is book companion code (tier 2/3).
TIER1_PREFIXES = (
    "AHP", "CellularAutomata", "FuzzyMathematicalModel", "GoalProgramming",
    "GraphTheory", "GreySystem", "HeuristicAlgorithm", "IntegerProgramming",
    "Interpolation", "LinearProgramming", "MultivariateAnalysis",
    "NeuralNetwork", "NonLinearProgramming", "RegressionAnalysis", "TimeSeries",
)

# IDs that indicate the file does not parse -- a real defect, not a style nit.
FATAL_IDS = {"SYNER"}


def relpath(path):
    """Strip everything up to and including 'src/'."""
    marker = "src" + os.sep
    idx = path.rfind(marker)
    return path[idx + len(marker):] if idx >= 0 else path


def tier(path):
    return 1 if relpath(path).startswith(TIER1_PREFIXES) else 2


def main():
    rows = []
    for line in io.open(REPORT, encoding="utf-8"):
        if line.startswith("#"):
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) >= 4:
            rows.append(parts)

    by_id = collections.Counter(r[2] for r in rows)
    sample = {}
    for r in rows:
        sample.setdefault(r[2], r[3])

    print("消息总数:", len(rows))
    print("\n=== 按 ID 排序，附典型文本 ===")
    for k, v in by_id.most_common():
        print(f"{v:>6}  {k:<10} {sample[k][:76]}")

    files_with_issues = {r[0] for r in rows}
    fatal_files = collections.Counter(r[0] for r in rows if r[2] in FATAL_IDS)

    print("\n=== 解析错误（SYNER）文件 ===")
    print(f"共 {len(fatal_files)} 个文件；其中一级层 "
          f"{sum(1 for f in fatal_files if tier(f) == 1)} 个")
    for f, c in fatal_files.most_common():
        print(f"  {c:>3} 处  [T{tier(f)}]  {relpath(f)}")

    print("\n=== 分级对比 ===")
    for t in (1, 2):
        files = {r[0] for r in rows if tier(r[0]) == t}
        msgs = sum(1 for r in rows if tier(r[0]) == t)
        fat = sum(1 for f in files if f in fatal_files)
        print(f"  T{t}: 有提示的文件 {len(files):>4}，消息 {msgs:>5}，含解析错误 {fat:>3}")

    print("\n=== 提示最多的 15 个文件 ===")
    per_file = collections.Counter(r[0] for r in rows)
    for f, c in per_file.most_common(15):
        print(f"  {c:>3} 提示  [T{tier(f)}]  {relpath(f)}")


if __name__ == "__main__":
    main()
