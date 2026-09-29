#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""E15 探针：`mutate-figure-style.py` 的 `M43` **前置锚**在"真家族 ≥1"时是否仍成立。

★ 覆盖不到的部分写实：`M43` 的前置锚跑的是**真 `.claude/skills`**（`pointer_run()` 不给
  `--skills-dir`），所以我**不能**往那儿放一个真家族 skill（会脏树）。本探针改用
  `--skills-dir` 指向**.claude/skills 的临时拷贝 + 一个家族 skill**，跑的是
  **`M43` 里那条 `pre_ok` 断言表达式的逐字复刻**，不是驱动器本身。
  ⇒ 它证明的是"那条断言在家族落地时成立/不成立"，不是"驱动器跑了"。

复跑（仓根）：
  python tests/m3-plot-recon/e15_m43_preanchor.py
"""
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
COPY = ROOT / "build/m3-plot-recon/skills-copy"

GOOD = """---
name: mcm-plot-python
description: 家族成员（模拟：合规）
---
# mcm-plot-python
见 `references/house-style.md`。
"""
BAD = GOOD.replace("见 `references/house-style.md`。", "宽度按 6.31 in 走。")


def pointer_run(skills_dir):
    cmd = [sys.executable, "tests/skills/figure-choose/check-spec-pointers.py",
           "--skills-dir", str(skills_dir)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def pre_ok(rc, out):
    """逐字复刻 `mutate-figure-style.py:902-904` 的 `pre_ok`（M43 前置锚）。"""
    res = next((l for l in out.splitlines() if l.startswith("RESULT")), "（缺 RESULT 行）")
    return (rc == 0 and res.startswith("RESULT: PASS")
            and not [l for l in out.splitlines() if l.startswith("FAIL")]), res


def main():
    if COPY.exists():
        shutil.rmtree(COPY)
    shutil.copytree(ROOT / ".claude/skills", COPY)
    print(f"拷贝真 skills 根 -> {COPY.relative_to(ROOT)} · 成员 "
          f"{sorted(p.name for p in COPY.iterdir())}")
    d = COPY / "mcm-plot-python"
    d.mkdir()
    for label, txt in (("A 合规家族 skill", GOOD), ("B 不合规家族 skill", BAD)):
        (d / "SKILL.md").write_bytes(txt.encode("utf-8"))   # write_bytes：本仓硬纪律
        rc, out = pointer_run(COPY)
        ok, res = pre_ok(rc, out)
        print("=" * 78)
        print(f"### {label} ###")
        print(f"  M43 前置锚 pre_ok = {ok}   （rc={rc} · 末行『{res}』）")
        for l in out.splitlines():
            if l.startswith(("RESULT", "FAIL", "PASS  K2", "PASS  K3")):
                print("    " + l)
    shutil.rmtree(COPY)
    print("\n临时拷贝已删：", not COPY.exists())
    print("\n★ 驱动器本身今天跑过：见 out-m43-m46-today.txt（46/46 红，M43 RED-OK，"
          "前置锚读数『真仓扫到 5 个 skill』由 `_ptr_scanned()` 现读，不写死字面量）")


if __name__ == "__main__":
    main()
