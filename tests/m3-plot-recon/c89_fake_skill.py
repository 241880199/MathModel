#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C8/C9 探针：造一个**临时的假家族 skill**，测 `check-spec-pointers.py` 是否**立刻生效**；
再把同一个禁止数值放进**非 `SKILL.md`** 的文件，测今天判不判得到。

★ 一律 `write_bytes`（本仓硬纪律：`write_text` 在 Windows 会写 CRLF）。
★ 产物落在 `build/`（gitignore），脚本本身入库 → 可复跑。

复跑（仓根）：
  python tests/m3-plot-recon/c89_fake_skill.py
"""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "build/m3-plot-recon/fake-skills"

# 一处**故意复述规范数值**：`6.31`（H2 的分母，K3 禁止串之一）
SKILL_RESTATE = """---
name: mcm-plot-python
description: 假家族 skill（侦察用，非交付物）
---

# mcm-plot-python

## 什么时候用
临时件。

## 决策树
临时件。

## 输出契约
- **推荐图型**：临时件。
- **理由**：临时件。
- **设计要点**：正文栏宽 6.31 in 时按 6.31 出图。

## 边界
见 `references/house-style.md`。

## 指针
`references/house-style.md`
"""

# 一个**干净**的对照：指针在、数值不复述
SKILL_CLEAN = """---
name: mcm-plot-python
description: 假家族 skill 对照（侦察用）
---

# mcm-plot-python

## 什么时候用
临时件。

## 决策树
临时件。

## 输出契约
- **推荐图型**：临时件。
- **理由**：临时件。
- **设计要点**：宽度按规范那一节走。

## 边界
见 `references/house-style.md`。

## 指针
`references/house-style.md`
"""

# 非 SKILL.md 的三种载体，各含同一个禁止数值（H12 的 0.8）
NON_SKILL = {
    "references/style.md": "# 样式\n\n主色不超过 4，线宽取 0.8。\n",
    "style.mplstyle": "figure.figsize: 6.31, 2.6\nlines.linewidth: 0.8\n",
    "style.py": "FIGSIZE = (6.31, 2.6)\nLINEWIDTH = 0.8\n",
}


def wb(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(s.encode("utf-8"))


def build():
    d = OUT / "mcm-plot-python"
    wb(d / "SKILL.md", SKILL_RESTATE)
    wb(d / "references/style.md", NON_SKILL["references/style.md"])
    wb(d / "style.mplstyle", NON_SKILL["style.mplstyle"])
    wb(d / "style.py", NON_SKILL["style.py"])
    c = OUT / "mcm-plot-clean"
    wb(c / "SKILL.md", SKILL_CLEAN)
    wb(c / "references/house-style.md", "# 假指针目标（空壳）\n")


if __name__ == "__main__":
    build()
    print(f"已生成假 skill 到 {OUT}")
    for p in sorted(OUT.rglob("*")):
        if p.is_file():
            print(f"  {p.relative_to(ROOT).as_posix()}  {p.stat().st_size} 字节  "
                  f"bytes={p.read_bytes()[:24]!r}")
