#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Task 2 的**验收证据**复跑并落盘到 `tests/skills/plot-matlab/plot-matlab-verify.txt`。

用法：  python tests/skills/plot-matlab/gen-plot-matlab-verify.py

## 为什么必须有个**入库的**生成器

`.superpowers/sdd/**` 被 git 忽略 ⇒ 报告不落盘就没了（本仓通则）。故证据件必须进 `tests/` 下、且**可复跑**
（先例：`tests/skills/plot-python/gen-plot-style-verify.py`、`tests/skills/figure-choose/gen-*.py`）。

## 记什么

1. 关键件的 `git hash-object`（证据与哪一版代码/表绑定，逐字可核）；
2. 每条命令的**原始 stdout + stderr + 退出码**，逐字落盘（不转述、不节选）；
3. 收尾一行合计（命令数 · 非零退出数）——证据件自己也要能被一眼判死。

**只捕获、不改写**：命令的输出原样进文件；本脚本对被测件**不做任何写操作**
（跑 `mutate-plot-style.py` 时它自己会还原，见那份驱动器里的"还原自证"）。

⚠️ **排期**：本器会跑 `mutate-figure-style.py`（约 225 s）。**别**与
`tests/skills/plot-python/gen-plot-style-verify.py` 并发（两者都会碰 `mutate-*` 的临时根）。
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "tests/skills/plot-matlab/plot-matlab-verify.txt"

# 证据绑定的件（逐件 `git hash-object`）—— Task 2 的判据 / 生成器 / 表 / 派生件 / 上游判据 / 规范
BOUND = [
    "tests/skills/plot-matlab/check-style-freshness.py",
    "tests/skills/plot-matlab/mutate-plot-style.py",
    "tests/skills/plot-matlab/probe-h10-band-ink.py",
    "tests/skills/plot-matlab/gen-mcm-style-matlab.py",
    "tests/skills/figure-choose/gen-style-table.py",
    "tests/skills/figure-choose/check-figure-style.py",
    ".claude/skills/mcm-figure-choose/assets/mcm-style.json",
    ".claude/skills/mcm-plot-matlab/assets/mcmplot.m",
    ".claude/skills/mcm-figure-choose/references/house-style.md",
]

# 验收命令（逐条真跑；stdout/stderr 全文落盘）
COMMANDS = [
    ("Task 2 的新鲜度守卫（干净态：两臂 + G0）",
     [sys.executable, "tests/skills/plot-matlab/check-style-freshness.py"], 0),
    ("Task 2 的变异驱动器（6 条必须红：两臂专属 / fail-closed / F4 / F6 + 2 条对照：射程边界该绿 / 字面形态该被证伪）",
     [sys.executable, "tests/skills/plot-matlab/mutate-plot-style.py"], 0),
    ("Task 2 的 H10 产物级回读探针（落地态 0/0/0 vs 对照态非 0）",
     [sys.executable, "tests/skills/plot-matlab/probe-h10-band-ink.py"], 0),
    ("收工门 ① 规范数守卫",
     [sys.executable, "tests/skills/figure-choose/check-house-style.py"], 0),
    ("收工门 ② 判据变异总驱动器（约 225 s）",
     [sys.executable, "tests/skills/figure-choose/mutate-figure-style.py"], 0),
    ("收工门 ③ 逐格验收",
     [sys.executable, "tests/skills/figure-choose/fixtures/run-expected.py"], 0),
    ("收工门 ④ 样式表新鲜度守卫（figure-choose 侧）",
     [sys.executable, "tests/skills/figure-choose/check-style-table-freshness.py"], 0),
    ("收工门 ⑤ 样式表新鲜度守卫（plot-python 侧）",
     [sys.executable, "tests/skills/plot-python/check-style-freshness.py"], 0),
    ("收工门 ⑥ 表重放一致性（15 条一致）",
     [sys.executable, "tests/skills/figure-choose/gen-style-table.py", "--check"], 0),
]


def blob(rel):
    return subprocess.run(["git", "hash-object", rel], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def main():
    lines = ["# Task 2 验收证据 · 新鲜度两臂 + 变异驱动器 + H10 回读（复跑："
             "`python tests/skills/plot-matlab/gen-plot-matlab-verify.py`）",
             "# 本文件**一字不改**地记录每条命令的原始 stdout/stderr 与退出码。",
             ""]
    print("=" * 78)
    print("Task 2 验收证据 · 复跑并落盘")
    print("=" * 78)

    lines.append("## 0. 证据绑定的件（`git hash-object`）")
    lines.append("")
    lines.append("| 件（仓相对） | `git hash-object` |")
    lines.append("| :--- | :--- |")
    for rel in BOUND:
        h = blob(rel)
        lines.append(f"| `{rel}` | `{h}` |")
        print(f"  {rel:<70} {h}")
    lines.append("")

    n_bad = 0
    for i, (title, cmd, want) in enumerate(COMMANDS, 1):
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
        cmdline = "python " + " ".join(cmd[1:])
        ok = (p.returncode == want)
        n_bad += 0 if ok else 1
        print(f"  [{i}/{len(COMMANDS)}] {title}\n      $ {cmdline}  → exit={p.returncode}"
              f"  {'OK' if ok else '未达预期 <<<'}")
        lines += [f"## {i}. {title}", "", f"    $ {cmdline}", f"    exit={p.returncode}",
                  "", "```text", p.stdout.rstrip("\n"), "```"]
        if p.stderr.strip():
            lines += ["", "stderr：", "```text", p.stderr.rstrip("\n"), "```"]
        lines.append("")

    lines += ["## 合计", "",
              f"命令 {len(COMMANDS)} 条 · 非零退出/未达预期 **{n_bad}** 条", ""]
    OUT.write_bytes(("\n".join(lines)).encode("utf-8"))       # write_bytes：不用 write_text（CRLF）
    print("-" * 78)
    print(f"命令 {len(COMMANDS)} 条 · 非零退出/未达预期 {n_bad} 条")
    print(f"证据 → {OUT.relative_to(ROOT).as_posix()}（{len(OUT.read_bytes())} 字节）")
    return 0 if n_bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
