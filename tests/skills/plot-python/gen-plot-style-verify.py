#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 Task 3 的**验收证据**复跑并落盘到 `tests/skills/plot-python/plot-style-verify.txt`。

用法：  python tests/skills/plot-python/gen-plot-style-verify.py

## 为什么必须有个**入库的**生成器

`.superpowers/sdd/**` 被 git 忽略 ⇒ 报告不落盘就没了（本仓通则）。故证据件必须进
`tests/` 下、且**可复跑**（先例：`tests/skills/figure-choose/gen-{house-style,pointer,skill}-verify.py`）。

## 记什么

1. 关键件的 `git hash-object`（证据与哪一版代码/字体绑定，逐字可核）；
2. 每条命令的**原始 stdout + stderr + 退出码**，逐字落盘（不转述、不节选）；
3. 收尾一行合计（命令数 · 非零退出数）——证据件自己也要能被一眼判死。

**只捕获、不改写**：命令的输出原样进文件；本脚本对被测件**不做任何写操作**
（跑 `mutate-plot-style.py` 时它自己会还原，见那份驱动器里的"还原自证"）。
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "tests/skills/plot-python/plot-style-verify.txt"

# 证据绑定的件（逐件 `git hash-object`）—— task 3 的判据与它守的东西
BOUND = [
    "tests/skills/plot-python/check-style-freshness.py",
    "tests/skills/plot-python/mutate-plot-style.py",
    "tests/skills/plot-python/gen-mcm-style.py",
    ".claude/skills/mcm-plot-python/assets/mcm.mplstyle",
    ".claude/skills/mcm-plot-python/assets/mcmplot.py",
    ".claude/skills/mcm-figure-choose/references/house-style.md",
    ".claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-Regular.otf",
    ".claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-Italic.otf",
    ".claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-Bold.otf",
    ".claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-BoldItalic.otf",
    ".claude/skills/mcm-plot-python/assets/fonts/PROVENANCE.md",
]

# 验收命令（逐条真跑；stdout/stderr 全文落盘）
COMMANDS = [
    ("Task 3 的新鲜度守卫 + 字体守卫（干净态）",
     [sys.executable, "tests/skills/plot-python/check-style-freshness.py"], 0),
    ("Task 3 的变异驱动器（6 条必须红 + 2 条对照：射程边界该绿 / 字面形态该被证伪）",
     [sys.executable, "tests/skills/plot-python/mutate-plot-style.py"], 0),
    ("收工三件套 ① 规范数守卫",
     [sys.executable, "tests/skills/figure-choose/check-house-style.py"], 0),
    ("收工三件套 ② 判据变异总驱动器",
     [sys.executable, "tests/skills/figure-choose/mutate-figure-style.py"], 0),
    ("收工三件套 ③ 逐格验收",
     [sys.executable, "tests/skills/figure-choose/fixtures/run-expected.py"], 0),
    ("顺带：引用完整性（`mcm-plot-python` 已建 ⇒ 绘图家族逐份判据应全绿）",
     [sys.executable, "tests/skills/figure-choose/check-spec-pointers.py"], 0),
]


def blob(rel):
    return subprocess.run(["git", "hash-object", rel], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def main():
    lines = ["# Task 3 验收证据 · 新鲜度守卫 + 字体守卫 + 变异（复跑："
             "`python tests/skills/plot-python/gen-plot-style-verify.py`）",
             "# 本文件**一字不改**地记录每条命令的原始 stdout/stderr 与退出码。",
             ""]
    print("=" * 78)
    print("Task 3 验收证据 · 复跑并落盘")
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
