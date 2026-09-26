#!/usr/bin/env python3
"""Categorise execution failures from run-report.txt.

Separates genuine defects from harness/environment artefacts:

  MY-FAULT  the script needs data this archive deliberately excluded
            (e.g. the 0.87 MB china.mat binaries), or waits for a human
  DEPRECATED the code calls a MATLAB API that has since been removed
  SHADOWING  the archive ships a file whose name collides with a built-in
  BUG        the code itself is wrong (parse error, index error, wrong maths)

Usage:  python tests/algorithms/analyze_runs.py [report.txt]
"""
import collections
import io
import os
import sys

REPORT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "run-report.txt")


def classify(msg):
    if "找不到文件或目录" in msg or "china" in msg:
        return "MY-FAULT 需要本归档剔除的数据文件"
    if "需要支持用户输入" in msg or "此平台上未提供此支持" in msg:
        return "MY-FAULT 需要交互输入（-batch 不支持）"
    if "不再支持" in msg or "已删除" in msg or "无法识别" in msg and "属性" in msg:
        return "DEPRECATED 用了已被移除的 MATLAB API"
    if "脚本" in msg and "作为函数执行" in msg:
        return "SHADOWING 文件名遮蔽了内置函数"
    if "无效表达式" in msg or "表达式无效" in msg or "解析错误" in msg:
        return "BUG 语法/解析错误"
    if "索引超出数组边界" in msg or "索引必须为正整数" in msg:
        return "BUG 数组索引越界"
    if "维度" in msg or "维度不一致" in msg:
        return "BUG 维度不匹配"
    return "OTHER 待判"


def main():
    rows = []
    for line in io.open(REPORT, encoding="utf-8"):
        if line.startswith("#"):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) >= 4:
            rows.append(p)

    fails = [r for r in rows if r[0] == "fail"]
    print(f"失败 {len(fails)} / 总计 {len(rows)}\n")

    groups = collections.defaultdict(list)
    for _st, rel, sec, msg in fails:
        groups[classify(msg)].append((rel, sec, msg))

    for kind in sorted(groups):
        print(f"=== {kind}  ({len(groups[kind])}) ===")
        for rel, sec, msg in groups[kind]:
            print(f"  [{sec:>7}s] {rel}")
            print(f"            {msg[:150]}")
        print()

    print("=== 通过的 ===")
    oks = [r for r in rows if r[0] == "ok"]
    print(f"  {len(oks)} 个通过")


if __name__ == "__main__":
    main()
