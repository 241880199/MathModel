#!/usr/bin/env python3
"""Classify archived .m files as script vs function, and by tier.

Scripts can be executed standalone; functions cannot (they need arguments).

Usage:  python tests/algorithms/classify_mfiles.py
"""
import collections
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "corpus", "algorithms", "src"))

TIER1_PREFIXES = (
    "AHP", "CellularAutomata", "FuzzyMathematicalModel", "GoalProgramming",
    "GraphTheory", "GreySystem", "HeuristicAlgorithm", "IntegerProgramming",
    "Interpolation", "LinearProgramming", "MultivariateAnalysis",
    "NeuralNetwork", "NonLinearProgramming", "RegressionAnalysis", "TimeSeries",
)

FUNC_RE = re.compile(r"^\s*function\b")
COMMENT_RE = re.compile(r"^\s*(%.*)?$")

# Scripts that wait for a human (GUI callbacks, blocking prompts) or loop
# forever by construction cannot be run unattended. They are reported as
# skipped-with-reason rather than counted as failures.
INTERACTIVE_RE = re.compile(
    r"uicontrol|waitfor|waitbar|ginput|keyboard|questdlg|msgbox|"
    r"\binput\s*\(|\bmenu\s*\(|\bpause\b|"
    r"while\s+(1|true)\b",
    re.IGNORECASE,
)


def strip_comments(text):
    """Drop %-comments and string literals so markers are only matched in code."""
    out = []
    for line in text.splitlines():
        # cut at the first % that is not inside a quoted string
        res, in_str = [], False
        for ch in line:
            if ch == "'":
                in_str = not in_str
            if ch == "%" and not in_str:
                break
            res.append(ch)
        out.append("".join(res))
    return "\n".join(out)


def first_code_line(path):
    """First non-blank, non-comment line (continuation lines joined)."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    buf = ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.endswith("..."):
            buf += line[:-3]
            continue
        line = buf + line
        buf = ""
        if not line or line.startswith("%"):
            continue
        return line
    return None


def tier_of(rel):
    """1 = repo owner's own algorithms; 2 = book companion code.

    A TIER1_PREFIX alone is not enough: HeuristicAlgorithm/ contains a nested
    copy of the 《MATLAB神经网络30个案例分析》 book tree, which is NOT the
    owner's own work and must not be counted as tier 1.
    """
    if not rel.startswith(TIER1_PREFIXES):
        return 2
    if "MATLAB神经网络30个案例分析" in rel:
        return 2
    return 1


def main():
    rows = []
    for dirpath, _dirs, names in os.walk(SRC):
        for n in names:
            if not n.lower().endswith(".m"):
                continue
            full = os.path.join(dirpath, n)
            rel = os.path.relpath(full, SRC)
            fl = first_code_line(full)
            kind = "function" if (fl and FUNC_RE.match(fl)) else "script"
            rows.append((tier_of(rel), kind, rel))

    for t in (1, 2):
        sub = [r for r in rows if r[0] == t]
        c = collections.Counter(r[1] for r in sub)
        print(f"T{t}: 共 {len(sub)} 个 .m  ->  script {c['script']}, function {c['function']}")

    print("\n=== 一级层可执行脚本（按目录）===")
    bydir = collections.defaultdict(list)
    for t, kind, rel in rows:
        if t == 1 and kind == "script":
            bydir[rel.split(os.sep)[0]].append(rel)
    for d in sorted(bydir):
        print(f"  {len(bydir[d]):>3}  {d}")
        for r in sorted(bydir[d]):
            print(f"        {os.sep.join(r.split(os.sep)[1:])}")
    print(f"\n一级层脚本合计: {sum(len(v) for v in bydir.values())}")

    out = os.path.join(HERE, "mfile-classification.txt")
    with open(out, "w", encoding="utf-8") as f:
        for t, kind, rel in sorted(rows):
            f.write(f"T{t}\t{kind}\t{rel}\n")
    print(f"\n清单已写入 {os.path.basename(out)}")

    t1scripts = [rel for t, kind, rel in rows if t == 1 and kind == "script"]
    interactive, runnable = [], []
    for rel in t1scripts:
        text = open(os.path.join(SRC, rel), encoding="utf-8", errors="replace").read()
        (interactive if INTERACTIVE_RE.search(strip_comments(text)) else runnable).append(rel)

    manifest = os.path.join(HERE, "run-manifest.txt")
    with open(manifest, "w", encoding="utf-8") as f:
        for rel in sorted(runnable):
            f.write(rel + "\n")
    skipped = os.path.join(HERE, "interactive-manifest.txt")
    with open(skipped, "w", encoding="utf-8") as f:
        for rel in sorted(interactive):
            f.write(rel + "\n")
    print(f"待执行清单已写入 {os.path.basename(manifest)}（{len(runnable)} 个可无人值守脚本）")
    print(f"交互式脚本已单列 {os.path.basename(skipped)}（{len(interactive)} 个，不自动执行）")
    for rel in sorted(interactive):
        print(f"      {rel}")


if __name__ == "__main__":
    main()
