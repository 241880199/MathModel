#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从**载体无关样式表** `.claude/skills/mcm-figure-choose/assets/mcm-style.json`
**重放** MATLAB 派生件 `.claude/skills/mcm-plot-matlab/assets/mcmplot.m` 的两处生成区。

用法（cwd = 仓根）：

    python tests/skills/plot-matlab/gen-mcm-style-matlab.py
    python tests/skills/plot-matlab/gen-mcm-style-matlab.py --table <副本>   # 变异/演示用

**重放式**（先例：`tests/skills/plot-python/gen-mcm-style.py`）：本脚本**不自造**
`mcmplot.m` 的散文 —— 它读**在库件**，只把两条生成标记之间的那段**原地换掉**；标记之外
一字不动（函数、help 文本、已知缺口那几段都原样保留）。派生件因此**只能**由本脚本产出。

## 单源机制（为什么必须有个生成器）

`mcmplot.m` 是**唯一会被写手抄进自己脚本**的东西 ⇒ 它一旦自带第二份样式，`m3-style-single-source`
线就白做了（设计 `2026-10-01-m3-plot-matlab-design.md` §4 的纪律：`mcmplot.m` 里零规范字面量）。
⇒ **本模块的每一个样式值都从表取**，**本脚本里不写死任何规范数值**（`H1` 的图宽比、`H14` 的
色序那一批，一个都不在这里出现）。这是本脚本存在的**唯一理由**。

## 逐条锚定 —— 但**不扫文本**（为什么与 python 侧形态不同）

python 侧 `gen-mcm-style.py` 的锚点是**打在 `house-style.md` 正文上的正则**（那边的数在散文里）。
本侧**不同**：要取的每一个值都已在 `mcm-style.json` 里是**结构化的** `entries[].id` / `.value`。
⇒ 本脚本**不用正则扫源文本**，改用 **id 逐条锚定**（`entry()`）：**每个 id 必须在表里恰命中 1 条**，
否则**非零退出、不写任何文件**。

**为什么明令禁止"扫文本"**：表里那些 `how` 串本身含大量数字 —— 实测有 `x2.show=0`（origin 的 how）、
`6.31944` / `455/72`（页盒推算）、版本号一类。**朴素 `\\d+\\.\\d+` 会把它们当样式值抽走**；
本仓先例（plot-python 侦察 §C10）实测同型误抽：`tab10`→`10`、`3D`→`3`、`p90`→`90`、`§7.2`→`7.2`。
⇒ **只认 `id` 精确相等的条目**，其余一律不碰。

## `not-landable` / 空值：**不静默跳过**（与"没抽到"分开）

- **"没抽到"**（表里没有这个 id / 有 2 条 / 值是空） ⇒ **`GeneratorError`**、非零退出、**不写文件**；
- **"表里写着没落地"**（`status == 'not-landable'`） ⇒ **照常处理**：把该行的 `status` 连同表里的
  `how`（"今天为何落不了地"那句）**写进产物的注释**。
两条路**在产物里长得不一样**：前者产物根本没生成，后者产物里有一条显式的 `status=not-landable` 行。

## `H10` 的落地判定（Task 1 的产物级先行实测）

`h10.axes_box` 的 matlab 格今天 `status=not-landable`（"能设、不能验"）。本模块 Task 1 **先做产物级实测**
（量**轴区顶/右带内墨迹**，口径与 python 侧 `tests/skills/plot-python/probe-gap1-hanging-ticks.py` 同型）
⇒ **探到了能落地**（读数见下常量 `H10_PROBE`）。故本生成器**把这些行写进产物**（`H10` 生成区），
同时在注释里如实记下**表今天仍写 not-landable**这件事 —— **表的同步归 Task 2**（见 `docs/superpowers/plans/2026-10-01-m3-plot-matlab.md` 的 T5）。

## 写入

一律 `write_bytes`（全仓禁用 `write_text`：Windows 上会把 LF 写成 CRLF）；产出全 **LF**。
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]        # tests/skills/plot-matlab → 仓根
TABLE = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"
MCM_M = ROOT / ".claude/skills/mcm-plot-matlab/assets/mcmplot.m"

CARRIER = "matlab"                                        # 本脚本读表里的哪一列载体

# ------------------------------------------------------------------ 生成标记
STYLE_BEGIN = "% >>> BEGIN GENERATED: STYLE（gen-mcm-style-matlab.py 重放，勿手改）>>>"
STYLE_END = "% <<< END GENERATED: STYLE <<<"
H10_BEGIN = "% >>> BEGIN GENERATED: H10（gen-mcm-style-matlab.py 重放，勿手改）>>>"
H10_END = "% <<< END GENERATED: H10 <<<"

# ------------------------------------------------------------------ id 锚点表
# `(行 id, 落进 STYLE 的键 或 None, 值形态)`
#   · 键 = None            ⇒ 只在该行的 status 注释里出现（本模块不落活常量）
#   · 形态 "num"           ⇒ 数值常量
#   · 形态 "hex"           ⇒ 单个 "#RRGGBB" → MATLAB 三元组 `[r g b]/255`
#   · 形态 "hexlist"       ⇒ 一串 "#RRGGBB" → MATLAB N×3 矩阵 `/255`
#   · 形态 "str"           ⇒ 单个字符串 → MATLAB 字符向量
#   · 形态 "strlist"       ⇒ 字符串列表 → MATLAB 元胞
# ⚠️ `h1.width_ratio.default_lo` 落 `None`：本模块的 `figsize_for()` 取**默认档上限**，不消费下限
#   ⇒ 不落活常量（它的值形态是 `0.xx`，落了会在产物里留一个**看起来像手写字面**的数）。表里仍读它、
#   仍为它记 status（见"不静默跳过"）。
ANCHORS = [
    ("h1.width_ratio.min",          "width_ratio_min",        "num"),
    ("h1.width_ratio.max",          "width_ratio_max",        "num"),
    ("h1.width_ratio.default_hi",   "width_ratio_default_hi", "num"),
    ("h1.width_ratio.default_lo",   None,                     "num"),
    ("h3.height_in",                "height_in",              "num"),
    ("h4.max_main_colors",          "max_main_colors",        "num"),
    ("h12.font_scale_lo",           "font_scale_lo",          "num"),
    ("h12.font_scale_hi",           "font_scale_hi",          "num"),
    ("h12.font_min_pt",             "font_min_pt",            "num"),
    ("lines.linewidth",             "line_width",             "num"),
    ("bg",                          "bg",                     "hex"),
    ("series.color",                "series_color",           "hexlist"),
    ("font.family",                 None,                     "str"),
    ("font.serif",                  "font_serif",             "strlist"),
    ("h10.axes_box",                None,                     "strlist"),
]

# ------------------------------------------------------------------ H10 的载体映射
# 把表里 `h10.axes_box.value` 的**需求串**逐条译成 MATLAB 落实行。**键必须与表里的串逐字相等**
# （表里出现未知需求串 ⇒ fail-closed，逼人来补映射，绝不静默跳过）。
H10_MAP = {
    "spines.top=off":
        "box(ax, 'off');                        % H10: 去上/右边框线（MATLAB 的 box 一并管顶与右）",
    "spines.right=off":
        "% H10: 右框线同上（MATLAB 无单独关右框线的设置项，由 box off 一并管）",
    "ticks.dir=in":
        "set(ax, 'TickDir', 'in');              % H10: 刻度朝内",
    "ticks.minor=off":
        "set(ax, 'XMinorTick', 'off', 'YMinorTick', 'off');   % H10: 只留主刻度",
    "axis.label=with-unit":
        "% H10: 轴标签带单位 = **调用方纪律**（MATLAB 侧**无设置项**）：写 xlabel/ylabel 时把单位写进去",
}

# ------------------------------------------------------------------ H10 的产物级实测结论
# Task 1 的**一次性探针**（不入库；入库探针 + 改表归 Task 2）当场跑出的读数。
# 复跑：`d:/Software/Matlab/bin/matlab -batch "run('build/m3-matlab-t1/probe_h10_band_ink.m')"`
# 量的是**轴区顶/右带内墨迹**（非白像素数），口径与 python 侧 probe-gap1-hanging-ticks.py 同型。
# 读数（本机 R2025b Update 5）：落地态(off/in) 顶内 0 右内 0 下外 0；对照态(on/out) 顶内 2900 右内 2337 下外 336。
H10_PROBE = ("landed", "顶内 0 / 右内 0 / 下外 0（落地态） vs 顶内 2900 / 右内 2337 / 下外 336（对照态）")


class GeneratorError(RuntimeError):
    """id 命中 ≠ 1 / 值为空 / 目标件缺生成标记 / 表里出现未知 H10 需求串 —— 一律 fail-closed。"""


def load_table(path):
    """读表（结构化）。读不出 ⇒ `GeneratorError`（绝不"读不到就默认放行"）。"""
    try:
        return json.loads(path.read_bytes().decode("utf-8"))
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        raise GeneratorError(f"读不出 {path.name}（{type(e).__name__}: {e}）")


def entry(tbl, eid):
    """**逐条锚定**：`eid` 必须在 `entries[]` 里**恰命中 1 条**，且它的值非空。否则 `GeneratorError`。

    这里**不看** `how`/`why` 那类散文（它们含大量数字），只认 `id` 精确相等 —— 见模块头"禁止扫文本"。
    """
    hits = [e for e in tbl.get("entries", []) if e.get("id") == eid]
    if len(hits) != 1:
        raise GeneratorError(f"锚点 {eid!r} 在表里命中 {len(hits)} 条（必须恰 1）—— "
                             f"锚点被删/被改名/被复制，派生件无从取值")
    e = hits[0]
    val = e.get("value")
    if val is None or val == "" or val == []:
        raise GeneratorError(f"锚点 {eid!r} 的 value 是空（{val!r}）—— 空值不许静默跳过")
    if CARRIER not in e.get("carriers", {}):
        raise GeneratorError(f"锚点 {eid!r} 的表里没有 {CARRIER!r} 这一列")
    return e


def carrier_status(e):
    """该行在 `CARRIER` 列的 `status`；缺 ⇒ fail-closed。"""
    c = e["carriers"][CARRIER]
    st = c.get("status")
    if not st:
        raise GeneratorError(f"锚点 {e['id']!r} 的 {CARRIER} 列没有 status")
    return st


def carrier_how(e):
    """该行在 `CARRIER` 列的 `how`（"为何落不了地"那句的来源）；缺 ⇒ fail-closed。"""
    c = e["carriers"][CARRIER]
    how = c.get("how")
    if not how:
        raise GeneratorError(f"锚点 {e['id']!r} 的 {CARRIER} 列没有 how")
    return " ".join(how.split())                               # 折成单行（MATLAB 注释不能跨行）


def matlab_literal(kind, val):
    """把表里的值渲染成 MATLAB 字面量。**颜色一律整数三元组 `/255`** —— 不带 `#`（见模块头单源纪律）。"""
    if kind == "num":
        return repr(val)
    if kind == "hex":
        h = str(val).lstrip("#")
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        return f"[{r} {g} {b}]/255"
    if kind == "hexlist":
        rows = "; ".join(
            "[{} {} {}]".format(*(int(str(c).lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)))
            for c in val)
        return f"[{rows}]/255"
    if kind == "str":
        return "'{}'".format(str(val).replace("'", "''"))
    if kind == "strlist":
        items = ", ".join("'{}'".format(s.replace("'", "''")) for s in val)
        return "{" + items + "}"
    raise GeneratorError(f"未知的值形态 {kind!r}")


def render_style(pairs, statuses, notlandable):
    """STYLE 生成区的正文：逐行 `STYLE.<键> = <字面量>;` + 每行的 status 注释 + not-landable 行说明。"""
    out = [
        "% 唯一样式来源：.claude/skills/mcm-figure-choose/assets/mcm-style.json（由生成器**按 id 逐条锚定**重放）。",
        "% 下列 id **不声称穷尽**：只列本模块读到的那些行；表里别的行本模块不消费。",
    ]
    for eid, key, kind, val in pairs:
        st = statuses[eid]
        if key is None:
            out.append(f"% {eid:<30} status={st}  （本模块不落活常量）")
        else:
            out.append(f"STYLE.{key} = {matlab_literal(kind, val)};"
                       f"{' ' * max(1, 34 - len(key) - len(matlab_literal(kind, val)))}% {eid} · status={st}")
    if notlandable:
        out.append("%")
        out.append("% ---- status=not-landable 的行（**不静默跳过**：下面逐行给『为何落不了地』，原句取自表）----")
        for eid, st, how in notlandable:
            out.append(f"% [{eid}] status={st}")
            out.append(f"%     {how}")
    return "\n".join(out)


def render_h10(requirements):
    """H10 生成区：按**表里的顺序**逐条译成 MATLAB 落实行。未知需求串 ⇒ fail-closed。"""
    lines = []
    unknown = [r for r in requirements if r not in H10_MAP]
    if unknown:
        raise GeneratorError(f"表里的 h10.axes_box 出现未知需求串 {unknown!r} —— 补 H10_MAP 映射，"
                             f"不许静默跳过（本生成器只认结对的载体落实）")
    for r in requirements:
        lines.append(H10_MAP[r])
    return "\n".join(lines)


def replace_region(text, begin, end, body, path):
    """把 `begin` 行与 `end` 行**之间**（不含两行本身）换成 `body`；标记缺一即 `GeneratorError`。"""
    i, j = text.find(begin), text.find(end)
    if i < 0 or j < 0 or j < i:
        raise GeneratorError(f"{path}：找不到生成标记（begin={begin[:44]!r} end={end[:44]!r}）"
                             f"—— 派生件必须由本脚本重放，不许手改")
    return text[:i + len(begin)] + "\n" + body + "\n" + text[j:]


def main():
    ap = argparse.ArgumentParser(description="从 mcm-style.json 重放 mcmplot.m 的两处生成区")
    ap.add_argument("--table", default=None, help="被读的样式表（默认 = 仓内 mcm-style.json；变异/演示用）")
    a = ap.parse_args()
    table = pathlib.Path(a.table) if a.table else TABLE

    try:
        tbl = load_table(table)

        pairs, statuses, notlandable = [], {}, []
        for eid, key, kind in ANCHORS:
            e = entry(tbl, eid)
            st = carrier_status(e)
            statuses[eid] = st
            pairs.append((eid, key, kind, e["value"]))
            if st == "not-landable":
                notlandable.append((eid, st, carrier_how(e)))

        # H10：先取需求串（fail-closed：空/缺一律抛），再逐条映射
        h10_reqs = entry(tbl, "h10.axes_box")["value"]
        h10_body = render_h10(h10_reqs)

        # ★ H10 的落地判定：表 status != not-landable ⇒ 表已认；今天表仍写 not-landable，
        # 但 Task 1 的**产物级探针**已证能落地 ⇒ 据实测写进产物。表同步归 Task 2。
        h10_note = [
            f"% 表 status（今天）= {statuses['h10.axes_box']!r}；"
            f"Task 1 产物级实测 = {H10_PROBE[0]}（{H10_PROBE[1]}）。",
            "% ⇒ 按**实测**把这些行落进产物；表 status 的同步（not-landable → 实测口径）归 Task 2。",
        ]
        h10_body = "\n".join(h10_note) + "\n" + h10_body
    except GeneratorError as e:
        print(f"FAIL  {e}", file=sys.stderr)
        return 1

    try:
        src = MCM_M.read_bytes().decode("utf-8")
        new = replace_region(src, STYLE_BEGIN, STYLE_END,
                             render_style(pairs, statuses, notlandable), MCM_M)
        new = replace_region(new, H10_BEGIN, H10_END, h10_body, MCM_M)
    except GeneratorError as e:
        print(f"FAIL  MARKER  {e}", file=sys.stderr)
        return 1

    MCM_M.write_bytes(new.encode("utf-8"))

    print(f"表 = {table}")
    print(f"锚点 {len(ANCHORS)} 条，按 id 逐条命中 1 处：")
    for eid, key, kind, val in pairs:
        shown = val if kind == "num" else matlab_literal(kind, val)
        print(f"    {eid:<30} {str(key or '(注释)'):<22} = {shown}   [{statuses[eid]}]")
    print(f"H10 需求串 {len(h10_reqs)} 条 → {h10_reqs}")
    print(f"重放 → {MCM_M.relative_to(ROOT).as_posix()}（STYLE 区 {len(pairs)} 行 + H10 区 {len(h10_reqs)} 行）")
    print(f"not-landable 行 {len(notlandable)} 条（已写进产物注释）：{[n[0] for n in notlandable]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
