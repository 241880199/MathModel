#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从规范 `house-style.md` **重放**派生件：`assets/mcm.mplstyle` 与 `assets/mcmplot.py` 的常量区。

用法（cwd = 仓根）：

    python tests/skills/plot-python/gen-mcm-style.py                 # 重放真规范
    python tests/skills/plot-python/gen-mcm-style.py --doc <副本>    # 变异/演示用（默认 = 真规范）

**重放式**（先例：`tests/skills/figure-choose/gen-figure-style-baseline.py`）：本脚本**不自造**
派生件的散文 —— 它读**在库件**，只把两条生成标记之间的那段**原地换掉**；标记之外一字不动
（`mcmplot.py` 的函数与散文、`mcm.mplstyle` 的说明性注释都原样保留）。派生件因此**只能**
由本脚本产出，不许手改（Global Constraint 6）。

## 单源机制（为什么必须有个生成器）

`house-style.md` 是唯一权威（本模块的 Global Constraint 1）。手写一份带数值的 `.mplstyle`/`mcmplot.py`
就是造第二份权威；而今天**没有任何守卫会扫非 `SKILL.md` 的载体**（`check-spec-pointers.py` 只 glob
`*/SKILL.md`）。⇒ 样式数值**不手写**，由本脚本用**逐条锚定正则**从规范里取（Global Constraint 7
"本次一个都不许手写"）。取了哪些、没取哪些，逐条写在下面。

## 锚点表：`（id, 正则, 键）` —— fail-closed

每条正则必须在 `house-style.md` 里**恰命中 1 处**（沿用 `check-house-style.py` 的 `GUARDS` 惯用法：
命中 0 处（锚点被删/被改走）或 >1 处（锚点被挤到别处、判据会静默判在错的地方）一律 FAIL 并**非零退出**、
**不写任何文件**）。**绝不"抽不到就默认放行"** —— 那正是本仓栽过六次的"判据恒绿"。

## 可抽性边界（照实写；侦察 §C10 实测，见 `tests/m3-plot-recon/out-c10-extract.txt`）

**只有 H1 / H3 / H4 / H12 四条**的规则行里有能机械抽出的阈值 ⇒ 只有这四条进锚点表。

- **H2 / H6 / H8 / H10 / H11 / H13 六条根本没有数可抽**（H2 是口径、H6/H8/H10/H11 是语义/未覆盖、
  H13 是纪律），**抽不到的绝不硬凑**：它们落实在散文与底座覆盖键里（H10 由 `mcm.mplstyle` 的
  `axes.spines.*` / `*tick.minor.visible` 覆盖键落实）。
- **H9 的可操作数在「依据」段**（正文词数阈值），与同段那一批**分布读数同形** ⇒ 正则分不开
  "阈值"与"读数"（同一段里阈值与百分数读数混在一起）⇒ **本脚本不抽 H9**。出货判据
  （`check-figure-style.py` 的 F3a–d）已守它，本模块不重造。
- **禁止全文档扫数**：实测朴素 `\\d+\\.\\d+` 会**误抽**非阈值 token 里的数字（`tab10`、`3D`、
  `p90`、章节号 `§…` 一类；侦察 §C10）⇒ 一律用**逐条锚定**正则。

## 抽出来的值落在哪

H1 / H3 / H4 / H12 的数**一律落进 `mcmplot.py` 的常量区** `HOUSE_STYLE`（那是"规范在本模块里的镜像"）；
函数消费其中的一部分：`figsize_for()` 用 H1 的默认档上限与 H3 的图高，`fontsize_for()` 用三个 H12 值。
`mcm.mplstyle` 只装**与调用方参数无关**的覆盖键（`savefig.bbox` 是 H1 机制的落地、H10 的语义、
H12 的字体族、H9 之外各条需要的 `mathtext.fontset`），**不含**上述阈值 —— 那些随正文 pt / 栏宽而变，
只能由调用方经函数换算。

## 写入

一律 `write_bytes`（全仓禁用 `write_text`：Windows 上会把 LF 写成 CRLF）；本脚本产出的两个文件
都是 **LF**。
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]     # tests/skills/plot-python → 仓根
DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
MPLSTYLE = ROOT / ".claude/skills/mcm-plot-python/assets/mcm.mplstyle"
MCM_PY = ROOT / ".claude/skills/mcm-plot-python/assets/mcmplot.py"

# ------------------------------------------------------------------ 锚点表
# （id, house-style.md 里的锚定正则, HOUSE_STYLE 里的键）
# 正则形态与 `check-house-style.py` 的 `G-*` 逐条同源（H1 四条、H3 三条、H4 一条、H12 三条）——
# 但不 import 它：那一侧的期望值来源是"现算 metric / 钉死常量"，这一侧是"抽成派生常量"，两端都从
# **同一份文档**取值，改一处即两端一起动（这正是单源的意义）。
ANCHORS = [
    # ---- H1. 图宽：贴近正文宽
    ("H1-width-min", r"\*\*不窄于 ([\d.]+)×\*\*", "h1_width_ratio_min"),
    ("H1-width-max", r"\*\*不超过 ([\d.]+)×\*\*", "h1_width_ratio_max"),
    ("H1-width-default-lo", r"（\*\*([\d.]+)–[\d.]+×\*\*）", "h1_width_ratio_default_lo"),
    ("H1-width-default-hi", r"（\*\*[\d.]+–([\d.]+)×\*\*）", "h1_width_ratio_default_hi"),
    # ---- H3. 取向与图高：默认横向
    ("H3-aspect-lo", r"宽高比常见带 \*\*([\d.]+)–[\d.]+\*\*", "h3_aspect_ratio_lo"),
    ("H3-aspect-hi", r"宽高比常见带 \*\*[\d.]+–([\d.]+)\*\*", "h3_aspect_ratio_hi"),
    ("H3-height", r"图高按 \*\*([\d.]+) in 量级\*\*", "h3_height_in"),
    # ---- H4. 配色密度
    ("H4-max-main-colors", r"彩色\*\*主色 ≤(\d+)\*\*", "h4_max_main_colors"),
    # ---- H12. 字号 / 线宽 / 字体族
    ("H12-font-scale-lo", r"正文的 \*\*([\d.]+)–[\d.]+×\*\*", "h12_font_scale_lo"),
    ("H12-font-scale-hi", r"正文的 \*\*[\d.]+–([\d.]+)×\*\*", "h12_font_scale_hi"),
    ("H12-font-min-pt", r"最小 \*\*≥(\d+) pt\*\*", "h12_font_min_pt"),
]

# ------------------------------------------------------------------ 生成标记
# 「只重写标记之间」—— 标记行**整行**连同其间的正文一起被重放，标记之外的散文原样保留。
MCM_PY_BEGIN = "# >>> BEGIN GENERATED: HOUSE_STYLE（gen-mcm-style.py 重放，勿手改）>>>"
MCM_PY_END = "# <<< END GENERATED: HOUSE_STYLE <<<"
MPLSTYLE_BEGIN = "# >>> BEGIN GENERATED: rcParams（gen-mcm-style.py 重放，勿手改）>>>"
MPLSTYLE_END = "# <<< END GENERATED: rcParams <<<"

# `mcm.mplstyle` 的覆盖键。**与调用方参数无关**的那些放这里（其余的数走 `mcmplot.py` 的函数）。
# `savefig.bbox: standard` 是 H1 机制的落地：底座 `science` 自带 `'tight'`，会把输出宽裁掉、
# 毁掉 `figsize`↔F1 的干净映射（读数与两张载体的对照见设计 §9 的实测表）。
MPLSTYLE_OVERRIDES = [
    ("savefig.bbox", "standard",
     "H1 机制：抵消底座 science 自带的 'tight'（否则输出宽 ≠ figsize 宽）"),
    ("mathtext.fontset", "stix",
     "H12：数学取 stix（与 Times 相容；底座是 dejavuserif/cm，必须显式覆盖）"),
    ("font.family", "serif", "H12：字体族随论文正文（serif）"),
    ("font.serif", "TeX Gyre TermesX, TeX Gyre Termes, DejaVu Serif",
     "H12：入库的 TeX Gyre TermesX 优先（由 apply_style() 注册），后两档是回退"),
    ("axes.spines.top", "False", "H10：去掉上边框线"),
    ("axes.spines.right", "False", "H10：去掉右边框线"),
    ("xtick.minor.visible", "False", "H10：只留主刻度"),
    ("ytick.minor.visible", "False", "H10：只留主刻度"),
]


class GeneratorError(RuntimeError):
    """锚点不命中 / 命中 >1 / 目标件缺生成标记 —— 一律 fail-closed（非零退出、不写文件）。"""


def extract(text):
    """按 `ANCHORS` 逐条抽值 ⇒ `[(键, 值)]`。任一条命中数 ≠ 1 ⇒ `GeneratorError`。"""
    out = []
    for aid, pat, key in ANCHORS:
        hits = list(re.finditer(pat, text))
        if len(hits) != 1:
            raise GeneratorError(f"{aid}：正则命中 {len(hits)} 处（必须恰 1）—— 锚点被删或挤到别处，"
                                 f"派生件无从取值：{pat}")
        out.append((key, hits[0].group(1)))
    return out


def _num(s):
    """把抽到的数值串按其**字面形态**转成 int / float（带小数点的转 float，否则转 int）。"""
    return float(s) if "." in s else int(s)


def render_mcm_py_values(pairs):
    """`HOUSE_STYLE` 常量区的生成体（逐行 `键: 值,`，注释标出它出自哪条规范）。"""
    lines = [
        "# 规范（.claude/skills/mcm-figure-choose/references/house-style.md）在本模块里的镜像。",
        "# 本区由 tests/skills/plot-python/gen-mcm-style.py 从规范**逐条锚定**重放产出 ——",
        "# **勿手改**（改了下一次重放就没了；要改请改规范里那条，再重放）。",
        "HOUSE_STYLE = {",
    ]
    for key, val in pairs:
        lines.append(f"    {key!r}: {_num(val)!r},")
    lines.append("}")
    return "\n".join(lines)


def render_mplstyle_body():
    """`mcm.mplstyle` 生成区的 rcParams 体。"""
    lines = ["# 底座 = ['science', 'no-latex'] 叠加本文件（apply_style() 里顺序固定：本文件最后 ⇒ 覆盖前者）。"]
    for key, val, why in MPLSTYLE_OVERRIDES:
        lines.append(f"{key}: {val}   # {why}")
    return "\n".join(lines)


def replace_region(text, begin, end, body, path):
    """把 `begin` 行与 `end` 行**之间**（不含两行本身）换成 `body`；标记缺一即 `GeneratorError`。"""
    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        raise GeneratorError(f"{path}：找不到生成标记（begin={begin[:40]!r} end={end[:40]!r}）"
                             f"—— 派生件必须由本脚本重放，不许手改")
    return text[:i + len(begin)] + "\n" + body + "\n" + text[j:]


def main():
    ap = argparse.ArgumentParser(description="从 house-style.md 重放派生件（mcm.mplstyle + mcmplot.py 常量区）")
    ap.add_argument("--doc", default=None, help="被抽的规范（默认 = 仓内 house-style.md；变异/演示用）")
    a = ap.parse_args()
    doc = pathlib.Path(a.doc) if a.doc else DOC

    text = doc.read_bytes().decode("utf-8")
    try:
        pairs = extract(text)
    except GeneratorError as e:
        print(f"FAIL  ANCHOR  {e}", file=sys.stderr)
        return 1

    # ---- 先全部渲染（fail-closed 之后再写：任一环失败都不留半成品）
    mcm_text = MCM_PY.read_bytes().decode("utf-8")
    style_text = MPLSTYLE.read_bytes().decode("utf-8")
    try:
        new_mcm = replace_region(mcm_text, MCM_PY_BEGIN, MCM_PY_END,
                                 render_mcm_py_values(pairs), MCM_PY)
        new_style = replace_region(style_text, MPLSTYLE_BEGIN, MPLSTYLE_END,
                                   render_mplstyle_body(), MPLSTYLE)
    except GeneratorError as e:
        print(f"FAIL  MARKER  {e}", file=sys.stderr)
        return 1

    MCM_PY.write_bytes(new_mcm.encode("utf-8"))
    MPLSTYLE.write_bytes(new_style.encode("utf-8"))

    print(f"规范 = {doc}")
    print(f"锚点 {len(ANCHORS)} 条，逐条命中 1 处：")
    for aid, _pat, key in ANCHORS:
        val = dict(pairs)[key]
        print(f"    {aid:<22} {key:<26} = {val}")
    print(f"重放 → {MCM_PY.relative_to(ROOT).as_posix()}（常量区）")
    print(f"重放 → {MPLSTYLE.relative_to(ROOT).as_posix()}（rcParams）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
