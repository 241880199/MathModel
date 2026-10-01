#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M3 载体无关样式表生成器（重放式）。从规范 house-style.md 抽取/投影出 mcm-style.json。

用法：
  python tests/skills/figure-choose/gen-style-table.py [--doc <路径>] [--check]
退出码：0 成功 · 1 锚点不命中或标记缺失（**不写任何文件**）
末行：`重放 → <产出件>（<N> 条）`

## 为什么是派生件、为什么是重放式

与 python 侧的 `gen-mcm-style.py` 同一套纪律（设计 Global Constraint 2/6）：规范
（`references/house-style.md`）是**唯一权威**，`assets/mcm-style.json` 是它给**实现方**用的
**机器投影**。手写这份 json 就是造第二份权威 ⇒ 它**只能**由本脚本重放产出，并由
`check-style-table-freshness.py` 证明"没被手改"。各载体（`mcm-plot-*`）**只读**它、各自映射，
**不许另起一份抽取**（Global Constraint 2）。

## 两条取值路径

1. **锚点表 `ANCHORS`**：规范里**有数可抽**的量 —— H1 / H3 / H4 / H12 的阈值（**标量**）+
   **H14 的八色序列**（**定长序列**，规范里是八行 markdown 表格）。逐条正则都 fail-closed：
   标量锚点必须**恰命中 1 处**；H14 锚点必须**恰命中 8 行**（不许"抓到几个算几个"）。任一不满足
   ⇒ 非零退出、**不写任何文件**。
2. **常量区 `CONSTS`**：规范里**只有规则没有数**（或规则本身就是文字）的量 + 两条**交付形态**量
   （底色 §0 / 字体族 H12）。**每一条都带 origin**，origin 逐字取自
   Global Constraint 8 的三个枚举值 `measured` / `community` / `as-delivered`，**不许自造**。

H14 的八色是**规定**（〔交付形态/口径〕），不是样本读数。它**不再手抄进常量区**——抄件会漂：
新鲜度守卫只证"表 vs 生成器"一致，**证不了"生成器常量 vs 规范"一致** ⇒ 规范改了色、表不跟着改、
**而且没有任何东西会红**（同 `gen-pointer-verify` 抄 `FAMILY_RE` 那次）。⇒ 值一律由 **H14 锚点**
从规范现取；`CONSTS` 里那一格只留**元数据**（clause / why），值用哨兵 `_H14` 占位、运行时由锚点填。
八个 hex 逐字取自规范 H14 的序号表；**下游（Task 3/4 与各载体生成器）一律读本脚本产出的 json，
不许各抄一份**。

## 写入

一律 `write_bytes`（全仓禁用 `write_text`：Windows 上会把 LF 写成 CRLF）；产出件是 **LF**。
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]     # tests/skills/figure-choose → 仓根
HOUSE = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
OUT   = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"


class GeneratorError(Exception):
    pass


# ── 锚点：从规范抽"有数可抽"的量（仿 gen-mcm-style.py 的 fail-closed）
#    · **标量**锚点 = 3 元组 `(id, 规范里的锚定正则, (json 里的 id, 来源性质))`：逐条必须**恰命中 1 处**。
#    · **定长序列**锚点 = 4 元组（末尾多一个"期望命中数"）：逐条必须**恰命中该数**。
#    任一不满足 ⇒ `GeneratorError`（不写任何文件）。
ANCHORS = (
    ("H1-width-min",       r"\*\*不窄于 ([\d.]+)×\*\*",           ("h1.width_ratio.min", "measured")),
    ("H1-width-max",       r"\*\*不超过 ([\d.]+)×\*\*",           ("h1.width_ratio.max", "measured")),
    # H1 的默认比值（"贴近正文宽 0.95–1.0×"）：F1 的落地默认**取的就是这两个数**，必须在表里（锚点形态
    #   与 `gen-mcm-style.py` 的 `H1-width-default-lo/hi` 一致）。之前只在 mcmplot.py 的镜像里 ⇒ 表里缺项。
    ("H1-width-default-lo", r"（\*\*([\d.]+)–[\d.]+×\*\*）",      ("h1.width_ratio.default_lo", "measured")),
    ("H1-width-default-hi", r"（\*\*[\d.]+–([\d.]+)×\*\*）",      ("h1.width_ratio.default_hi", "measured")),
    ("H3-height",          r"图高按 \*\*([\d.]+) in 量级\*\*",     ("h3.height_in",       "measured")),
    ("H4-max-main-colors", r"彩色\*\*主色 ≤(\d+)\*\*",            ("h4.max_main_colors", "measured")),
    ("H12-font-scale-lo",  r"正文的 \*\*([\d.]+)–[\d.]+×\*\*",    ("h12.font_scale_lo",  "community")),
    ("H12-font-scale-hi",  r"正文的 \*\*[\d.]+–([\d.]+)×\*\*",    ("h12.font_scale_hi",  "community")),
    ("H12-font-min-pt",    r"最小 \*\*≥(\d+) pt\*\*",             ("h12.font_min_pt",    "community")),
    # H14 八色：规范里是**八行 markdown 表格**（`| 一 | `#E69F00` | 橙 |`，一…八逐行）⇒ 定长序列锚点。
    #   ★ fail-closed：命中**行数必须恰 8**（不许"抓到几个算几个"）。值保留带 `#` 的 hex（Task 4 才剥）。
    #   ⚠️ H14 正文里另有一段可复跑的比对命令（含别的 hex，写成 `h14 = [...]`）—— 本正则只锚**表格行**
    #   （行首 `| <序数> |` + 反引号 hex），不会命中那段代码，故行数恒为 8。
    ("H14-series-color",   r"^\| [一二三四五六七八] \| `(#[0-9A-Fa-f]{6})` \|",
                           ("series.color", "as-delivered"), 8),
)


def extract(text):
    """按 `ANCHORS` 抽值：标量 → 值串；定长序列 → 值串列表。

    返回 `(scalars, seq)`：`scalars = [(json_id, 值串, 来源性质)]`（标量，按 ANCHORS 顺序）；
    `seq = {json_id: [值串, ...]}`（定长序列）。
    任一锚点不满足（标量命中 ≠ 1 / 序列命中 ≠ 声明数）⇒ `GeneratorError`。"""
    scalars, seq = [], {}
    for spec in ANCHORS:
        aid, pat, (key, origin) = spec[0], spec[1], spec[2]
        hits = list(re.finditer(pat, text, re.MULTILINE))
        want = spec[3] if len(spec) == 4 else 1
        if len(hits) != want:
            unit = "行" if len(spec) == 4 else "处"
            raise GeneratorError(f"{aid}：正则命中 {len(hits)} {unit}（必须恰 {want}）—— 锚点被删或挤到"
                                 f"别处，派生件无从取值：{pat}")
        if len(spec) == 4:
            seq[key] = [h.group(1) for h in hits]
        else:
            scalars.append((key, hits[0].group(1), origin))
    return scalars, seq


# ── 常量区：正则抽不到的（规范里只有规则没有数、或来源是交付形态）——
#    ★ 每一条都必须带 origin，且 origin 必须来自 Global Constraint 8 的三个枚举值，不许自造。
#    ★ 这些常量本身也要有守卫（见 check-house-style.py 的 const: 机制；本文件的守卫是
#      check-style-table-freshness.py + 下游判据）。
# 哨兵：该格的值**不手抄**，运行时由锚点填（目前只有 H14 八色，见 `_H14`）。
_H14 = object()

CONSTS = (
    # 底色：来源 = §0「交付形态前提」，不是样本读数
    ("bg",            "#FFFFFF", "as-delivered", "§0",  "论文底色 = 白"),
    # 显式色序：来源 = H14，是**规定**不是读数。★ 值由 **H14 锚点**从规范现取（`_H14` 哨兵），
    #   本行只留元数据 —— 手抄会漂（规范改了色、表不跟着改、且没有东西会红）。
    ("series.color",  _H14,      "as-delivered", "H14", "H14 的八色序列（用户 2026-09-30 二次定稿）"),
    # 字体族：按族等价（Global Constraint 1）
    ("font.family",   "serif", "as-delivered", "H12", "衬线族"),
    ("font.serif",    ["TeXGyreTermesX", "Times New Roman"], "as-delivered", "H12",
                      "各载体取本机可用的 Times 系实现"),
    ("lines.linewidth", 1.0, "community", "H12", "线宽默认值"),
    # H10（坐标轴：去上/右边框线 · 刻度朝内 · 只留主刻度 · 轴标签带单位）—— 规范里**没有数可抽**
    #   （H10 的"依据"段自标"本样本量不到刻度朝向"）⇒ 走常量区，`clause` = H10、`origin` = 规范
    #   H10 自己的来源性质〔社区〕（Global Constraint 8 的枚举值之一，不许自造）。
    #   ★ 补进表的理由（M3-style 终审 **I-5**，Global Constraint 4"全收、逐格标落地状态"）：
    #   H10 **是载体相关的样式规则**（python 侧 `mcm.mplstyle` 已为它落了 6 个键）——GC4 只把 **H11**
    #   排除在外，H10 漏在表外 ⇒ matlab/origin 照表实现时**拿不到 H10** ⇒ 对 H10 而言"单源"不成立。
    #   值是无主的规则（不是数）⇒ 拆成 5 个可人工转述的 token（**值里一个数都没有**，不引入无主数）。
    ("h10.axes_box",
     ["spines.top=off", "spines.right=off", "ticks.dir=in", "ticks.minor=off",
      "axis.label=with-unit"],
     "community", "H10", "去上/右边框线 · 刻度朝内 · 只留主刻度 · 轴标签带单位"),
)


# ── 载体落地 `status` 的**唯一声明**（设计 §6.3）——
#    ★ 这 5 个值是全表唯一权威；`carrier_map()` 里任何格子的 status 不在其中 ⇒ `GeneratorError`
#      （fail-closed）。防的是手滑成 `"samevalue"` 之类**静默通过**（没有守卫兜底）。
STATUSES = ("same-value", "family-equivalent", "not-landable", "scriptable", "not-embedded")

# ── `status` 的**正面定义**（2026-10-01，M3-plot-matlab Task 2 补；随 `_status_defs` 写进表头）——
#    ★ 为什么必须补（Task 1 独立复核 Findings-M4 / 计划 Task 2 硬要求 6）：旧稿只列了 5 个**值**，
#      **没有给任何一个正面定义** ⇒ 它接不住"**载体有能力设、但产物里不落活常量**"这一类
#      （实况：`h1.width_ratio.default_lo` 的 matlab 格写 `same-value`，而 `mcmplot.m` 只把它落成注释）。
#    ★ 定义取"**能力**"口径（而非"产物已落"口径）——与设计 §1.1"一致性目标 = 同规范 / 按族等价、
#      不追求逐字同值"同一取向：`same-value` 说的是"**载体侧能设成与表内逐字相同的值**"，
#      **不保证**该值一定落成产物里的活常量。⇒ **`how` 一栏必须写明这个值在本模块产物里的落点**
#      （活常量 / 产物像素 / 调用方参数 / 只登记不消费）—— 这条**新增的 how 义务**才是这次补定义的重点：
#      单个 status 词承载不了"落点在哪"，落到 `how` 里说清、不许留一句笼统的"能同值"。
STATUS_DEFS = {
    "same-value": "载体侧**有能力**把该量设成与表内**逐字相同的值**（区别于 'family-equivalent' 的按族等价）；"
                  "该格 `how` **必须写明这个值在本模块产物里的落点**（活常量 / 产物像素 / 调用方参数 / "
                  "只登记不消费）。**不声称**产物一定落活常量。",
    "family-equivalent": "载体只能按**族**等价（如字体：同族不同实现 —— python 入库 OTF 与系统 Times 系）；"
                         "`how` 写明各载体取的族。",
    "not-landable": "本模块**今天确实没有**能落到产物上的方式（载体可能连设置项都没有）；"
                    "`how` 写清原因，**不许**既不测也不改、留一句'能设不能验'当结论。",
    "scriptable": "（origin 专用）本支**能脚本化**落地，`F1`/`F4`/`F5` 在它上有承重；`how` 给出脚本命令。",
    "not-embedded": "（origin 字体两格专用）产物**不内嵌**字体 ⇒ 字体族判据（`F6`）对它只能判 `N/A`。",
}


# ── origin 列的契约（设计 §6.3，2026-09-30 更新：脚本为权威、值已实测）——
#    每个 id 的 `carriers.origin` 填**实测到的脚本命令 + 操作步骤 + 版本**，不再是 `null`。
#    下面三条常量是 Task 2 **当场复跑**（probe_b/d/e/g/i + probe_origin_font5）后落表的：
#    逐份 stdout 与本目录入库的 `out-*.txt` **逐字节相同**（见 task-m3-style-t2-report.md）。
ORIGIN_VERSION = "10.300197（OriginPro 2026 / 教育版）"   # 实测 `LT_get_var('@V')` + 窗口标题
# ★ 设计 §6.3③ 要的「菜单路径 + 控件名」辅路：本表**不写** origin 的操作步骤（菜单路径 + 控件名）——
#   本轮**没有对 GUI 做过独立取证**，故留待补。**不编造**（本项目第一号病灶 = 声明比事实大）
#   ⇒ 如实标缺口，待补。（旧稿那句"两个 probe README 都写明全程无任何 GUI 交互"在入库件里
#   grep 不到 ⇒ 改为**只述事实、不指任何路径**：`origin-font-probe` 只写"全程无交互"、
#   `origin-probe` 只字未提。）
ORIGIN_STEPS_UNPROBED = ("本表不写 origin 的操作步骤（菜单路径 + 控件名）：本轮没有对 GUI 做过独立取证，"
                         "故留待补（设计 §6.3③ 待补）")


def carrier_map(vals):
    """每个 id 的载体落地表（**每个 id** 都有 python / matlab / origin 三列 —— Global Constraint 4）。

    ★ 这里**不写死 id 计数**（原先写「12 个 id 全有」，实际早已是 14、补 H10 后 15 ⇒ 声明比事实大）：
    该不变量由 `carriers_for()` **逐 id 强制**（缺该 id 的格 ⇒ `GeneratorError`），计数自己会漂。

    `vals`：`{json_id: 规范里的原值串}`（如 `"h1.width_ratio.min" -> "0.80"`）—— 供 `h1.width_ratio.*`
    各格的 `how` **现取本格自己的键名与值**。防的是"一格引用了别行的值"：旧稿把四格共用一段文字、
    里面写死 `h1_width_ratio_default_hi`（1.0）⇒ min / max / default_lo 三格成了"文本说 1.0、
    值是 0.80 / 1.20 / 0.95"（**同一格里文本与值互相矛盾**）。值由 `ANCHORS` 现取 ⇒ 规范改数、
    `how` 跟着改（不手抄、不漂）。

    `status` 的枚举见模块级 `STATUSES`（**唯一声明**，越界即 `GeneratorError`）：
      · python / matlab：`same-value` / `family-equivalent` / `not-landable`；
      · origin：`scriptable`（本支能脚本化、`F1`/`F4`/`F5` 在它上有承重）、
        `not-embedded`（**字体两格**：产出的 PDF 不内嵌字体 ⇒ `F6` 只能判 `N/A`），
        或 `not-landable`（本支**今天确实没有**对应的落地方式，`how` 里写原因 —— 不编造）。

    `h4.*` / `h12.*` 是**数值判据**（判据、不是设置）⇒ 三支都 `not-landable`，如实写"无设置项"。
    """
    def origin(how, status="scriptable"):
        return {"how": how, "steps": ORIGIN_STEPS_UNPROBED,
                "version": ORIGIN_VERSION, "status": status}

    def width_py(key):
        """H1 图宽（python）那格的 `how`：**本格**的键名与值由 `vals` 现取，不写别行的值。

        ★ 订正（2026-10-01 M3-plot-matlab Task 2，Task 1 独立复核 Findings-M4）：旧稿对四格**一律**
        写「python 侧令宽 = 正文栏宽 × 表内 `<该键>`（…）… ⇒ F1 = …」，**而 `figsize_for()` 只乘
        `default_hi`** ⇒ min / max / default_lo 三格描述的**动作在代码里都不发生**（只有 `default_hi`
        那格与代码一致）。⇒ 现按代码实况**分写**：只有 `default_hi` 是 `figsize_for()` 现取的乘数；
        其余三格**落了活常量但无人消费**（min / max 是 F1 验收带的边界、default_lo 是默认档下限），
        `how` 如实写"不被消费"，不再声称那个不发生的乘法。
        """
        name, val = key.replace(".", "_"), vals[key]
        loc = (".claude/skills/mcm-plot-python/assets/mcmplot.py figsize_for / "
               ".claude/skills/mcm-plot-python/assets/mcm.mplstyle")
        if key == "h1.width_ratio.default_hi":
            return (f"python 侧令宽 = 正文栏宽 × 表内 `{name}`（{val}）—— `figsize_for(textwidth_in)` "
                    f"**取的就是本键**（默认档的上限）；`savefig.bbox: standard` 保证输出宽 == figsize 宽 "
                    f"⇒ F1 = {val}（⇐ {loc}）")
        role = {"h1.width_ratio.min": "**F1 验收带的下界**（判据侧 `check-figure-style.py` 的 `F1_LO` "
                                      "**独立写死**为同值）",
                "h1.width_ratio.max": "**F1 验收带的上界**（判据侧 `check-figure-style.py` 的 `F1_HI` "
                                      "**独立写死**为同值）",
                "h1.width_ratio.default_lo": "**默认档的下限**"}[key]
        return (f"python 侧本键（{val}）= {role}；`figsize_for(textwidth_in)` **只取 `default_hi`、"
                f"不消费本键**，`HOUSE_STYLE['{name}']` 落了活常量但**无人消费**（⇐ {loc}）")

    # 宽度（matlab / origin）：三支都能把"图宽"设成正文栏宽的**指定倍**（F1 = 输出宽 / 正文栏宽）。
    #   ★ 下面两段**一个"某行比值的具体数"都不写**——只述实测的**绝对宽**（6.31 / 6.31944 in），
    #     故四格通用、且不会与所在行的值打架（旧稿在这段里写死 `F1 = 1.000` / `F1 = 1.001`，
    #     那正是"别行的输出比值"，在 min/max/default_lo 格里与值互相矛盾）。
    _W_ML = ("`print -dpng` 跟 `PaperPosition`、`print -dpdf` 跟 `PaperSize`（**显式设宽、不写死**）"
             "⇒ 实测输出宽 == 设定宽（pr.png in = 6.3100 ⇐ out-size-law.txt；设计 §6.2）。⚠️ `exportgraphics` "
             "的宽 = **内容包围盒**、与 figsize/PaperPosition 无关（**完全忽略** `PaperPosition`/"
             "`PaperSize`、按轴内容 bbox 裁剪 ⇐ out-size-law.txt）⇒ **不作权威交付载体**")
    # 宽度（matlab）**default_lo 专用**：本键是四格里唯一"**载体能设、但本模块产物不落活常量**"的一格
    #   （`mcmplot.m` 的 `figsize_for()` 只取 `default_hi`）⇒ 按 Task 2 补的 `same-value` 正面定义
    #   （`STATUS_DEFS`），`how` **必须写明落点**：这里落点是"**只登记、不消费、不落活常量**"。
    #   ★ 为什么不落活常量：其值 `0.95` 是表里**唯一**形如 `0.xx` 的规范值，落进产物会与
    #     `mcmplot.m` 的"产物里零手写规范字面"验收 tripwire（`git grep -nE "0\.[0-9]{2}"`）撞上
    #     —— **该项裁决见 task-m3-matlab-t2-report.md**（本任务把它显式记账，未偷偷放宽 tripwire）。
    _W_ML_DEFAULT_LO = (
        "**本模块产物里不落活常量、也不消费**：`mcmplot.m` 的 `figsize_for()` **只取 `default_hi`**，"
        "本键（`0.95`）仅登记在表里（H1 默认档的下限）。载体（`print` 家族）**有能力**把宽设成 0.95×"
        "（`-dpng` 跟 `PaperPosition`、`-dpdf` 跟 `PaperSize`）⇒ `status=same-value` 指『**载体能同值**』，"
        "**不指**『本模块产物已落该值』（口径见本表 `_status_defs.same-value`）。**不落活常量的理由**："
        "其值 `0.95` 是表里唯一形如 `0.xx` 的规范值，落进产物会与『产物里零手写规范字面』的验收 tripwire "
        "撞上（裁决见 `task-m3-matlab-t2-report.md`）。")

    _W_OG = ("`GPage.save_fig(width=N)` → 发 `expGraph … tr1.Unit:=2 tr1.Width:=N`；裸 LabTalk 用 "
             "`tr1.Unit:=0 tr1.Width:=<in>`。实测输出宽 ≈ 设定宽（green.pdf 页盒 **6.31944 in** / "
             "设定 6.31 ⇐ out-g-e2e-scenarios.txt）；**「PDF 页盒按 1/72 in 网格量化」与「6.31944 ≈ "
             "455/72」均为据实测页盒推算**（`tr1.Width:=6.31` → 页盒 6.31944 in ⇐ "
             "out-g-e2e-scenarios.txt / probe_g_e2e.py）")

    return {
        "h1.width_ratio.min": {
            "python": {"how": width_py("h1.width_ratio.min"), "status": "same-value"},
            "matlab": {"how": _W_ML, "status": "same-value"},
            "origin": origin(_W_OG),
        },
        "h1.width_ratio.max": {
            "python": {"how": width_py("h1.width_ratio.max"), "status": "same-value"},
            "matlab": {"how": _W_ML, "status": "same-value"},
            "origin": origin(_W_OG),
        },
        # H1 的默认比值 lo/hi（0.95 / 1.0）：F1 的**落地默认** = 上限（`default_hi`）；`default_lo`
        #   是默认档下限、**不被 `figsize_for()` 消费**（matlab 格专用 how：见 `_W_ML_DEFAULT_LO`）。
        "h1.width_ratio.default_lo": {
            "python": {"how": width_py("h1.width_ratio.default_lo"), "status": "same-value"},
            "matlab": {"how": _W_ML_DEFAULT_LO, "status": "same-value"},
            "origin": origin(_W_OG),
        },
        "h1.width_ratio.default_hi": {
            "python": {"how": width_py("h1.width_ratio.default_hi"), "status": "same-value"},
            "matlab": {"how": _W_ML, "status": "same-value"},
            "origin": origin(_W_OG),
        },
        "h3.height_in": {
            "python": {"how": "`figsize_for(textwidth_in)` 的高 = 表内 `h3_height_in`（2.6 in，直取）"
                               "（⇐ .claude/skills/mcm-plot-python/assets/mcmplot.py）", "status": "same-value"},
            "matlab": {"how": "`PaperPosition` 第 4 元（`print -dpng`）/ `PaperSize` 的高（`print -dpdf`）"
                               "⇒ 实测 `PaperPosition=[0 0 6.31 2.6]`（⇐ out-b-size-single-variable.txt）",
                       "status": "same-value"},
            "origin": origin(
                "**今天无实测的独立设高方式**：`GPage.save_fig` 签名无 height 参数"
                "（`save_fig(path, type, replace, width, ratio)` ⇐ probe_b_size.py）；裸 "
                "`expgraph … tr1.Height:=500` 实测**未生效**（与 `tr1.Width:=1000` 同发，产物却是 "
                "1000×708 = 按页面长宽比锁高 ⇐ out-b-export-size.txt 第 4 段）⇒ **今天没有实测到的"
                "独立设高方式**，高度随宽度按页面长宽比带出，**无独立落地**", status="not-landable"),
        },
        "h4.max_main_colors": {
            "python": {"how": "**数值判据，无设置项**：F2『彩色主色 ≤4』在 check-figure-style.py 判；"
                               "载体侧没有『限制主色数』的 rcParam/属性，一致性靠『按 H14 取色 + 控制"
                               "系列数』的调用纪律", "status": "not-landable"},
            "matlab": {"how": "**数值判据，无设置项**：同上；F2 本就按像素占比数色、不数系列"
                               "（只数占比 ≥0.5% 的颜色 ⇐ check-figure-style.py）—— 实测 MATLAB 侧同一张 "
                               "7 系列默认图读 3（png）/ 0（pdf）（⇐ out-checks-figure-style.txt 的 "
                               "`C default-N7` 段），更无『主色数上限』设置",
                       "status": "not-landable"},
            "origin": origin(
                "**数值判据，无设置项**：同上；默认模板连画 6 条线 `Plot.color` 6 条**全同色**"
                "（`(81,81,81)`、`colorinc` 恒 0 ⇐ Origin 侦察 §C④）⇒ 颜色数由调用方逐色设定，"
                "无『主色数上限』设置", status="not-landable"),
        },
        "h12.font_scale_lo": {
            "python": {"how": "**数值判据，无设置项**：图内字号 = 正文 pt 的 `[0.8, 1.0]×`、且 `≥7 pt`；"
                               "载体侧设的是**绝对 pt**，无『倍数/下限』设置项。`mcmplot.fontsize_for"
                               "(body_pt)` 只**产这个允许带**、不设值（⇐ .claude/skills/mcm-plot-python/assets/mcmplot.py）",
                       "status": "not-landable"},
            "matlab": {"how": "**数值判据，无设置项**：同上；MATLAB 侧可设绝对 `FontSize`，但判据是比值/"
                               "下限、无对应设置；且 H12 **无机械判据**（⇐ task-m3-matlab-recon-report.md"
                               "『H12 落不了地』）", "status": "not-landable"},
            "origin": origin(
                "**数值判据，无设置项**：同上；`layer.x.label.pt` 可直接设**绝对 pt**（实测可写、"
                "默认 14 ⇐ Origin 侦察 §C③），但表内值是比值/下限、无对应设置项",
                status="not-landable"),
        },
        "h12.font_scale_hi": {
            "python": {"how": "**数值判据，无设置项**：house-style H12 的『落地默认』= 取上限（正文 pt 的 "
                               "`1.0×`）；载体侧设的是**绝对 pt**，无『倍数』设置项。`fontsize_for(body_pt)` "
                               "的上界 = `max(body_pt×1.0, 7)`，调用方在其中取一档（⇐ .claude/skills/mcm-plot-python/assets/mcmplot.py）",
                       "status": "not-landable"},
            "matlab": {"how": "**数值判据，无设置项**：同上；MATLAB 侧可设绝对 `FontSize`，但无『倍数』"
                               "设置项；且 H12 无机械判据（⇐ task-m3-matlab-recon-report.md）",
                       "status": "not-landable"},
            "origin": origin(
                "**数值判据，无设置项**：同上；`layer.x.label.pt` 可设绝对 pt，但无『倍数』设置项",
                status="not-landable"),
        },
        "h12.font_min_pt": {
            "python": {"how": "**数值判据，无设置项**：下限 `≥7 pt`；无『最小字号』设置项。`fontsize_for"
                               "()` 把该下限取进允许带（`max(body×倍, 7)`）但不设值（⇐ .claude/skills/mcm-plot-python/assets/mcmplot.py）",
                       "status": "not-landable"},
            "matlab": {"how": "**数值判据，无设置项**：同上；无对应设置项；且 H12 无机械判据（⇐ "
                               "task-m3-matlab-recon-report.md）", "status": "not-landable"},
            "origin": origin(
                "**数值判据，无设置项**：同上；`layer.x.label.pt` 可设绝对 pt，但无『最小字号』设置项；"
                "本轮未逐档测最小步长（⇐ Origin 侦察 §C③）", status="not-landable"),
        },
        "bg": {
            "python": {"how": "rcParams: figure.facecolor / axes.facecolor / savefig.facecolor", "status": "same-value"},
            "matlab": {"how": "figure(...,'Theme','light') + set(gcf,'Color','w') + set(gca,'Color','w')", "status": "same-value"},
            "origin": origin(
                "默认导出即白底（实测产物四角/中心像素均 255,255,255 ⇐ out-d-appearance.txt，"
                "Task 2 复跑逐字节复现）⇒ 无需设置。⚠️ 实测 `page.color=15;` / `layer.color=15;` / "
                "`layer.background=15;` 均返 OK 而产物底色不变（**静默失败**）⇒ 底色只能由产物证明，"
                "返回值不算数。"),
        },
        "series.color": {
            "python": {"how": "rcParams: axes.prop_cycle（⚠️ 表内值是带 `#` 的 hex；写进 mplstyle 的 "
                               "`axes.prop_cycle` 时**值必须不带 `#`** —— mplstyle 把 `#` 当注释 ⇒ 剥去）",
                       "status": "same-value"},
            "matlab": {"how": "set(gca,'ColorOrder',[...])", "status": "same-value"},
            "origin": origin(
                "逐色设色 = originpro `plot.color = \"#RRGGBB\"`（LabTalk 等价 `layer.plotN.color = "
                "<Origin 颜色值>`）。实测六色 hex 逐色设、读回 Plot.color 逐值命中（⇐ out-e-font-palette-axis.txt "
                "B 段）；**同一会话内不翻转**（同模板连建两图读数一致 ⇐ out-i-dpi-pagesize-frame.txt ③ 段）。"
                "本轮 Task 2 复跑逐字节复现。"),
        },
        "font.family": {
            "python": {"how": "font.family: serif", "status": "family-equivalent"},
            "matlab": {"how": "set(gca,'FontName','Times New Roman')", "status": "family-equivalent"},
            "origin": origin(
                "导出那一刻施加主题：`expGraph type:=pdf … theme:=\"Times New Roman Font\";`"
                "（实测产物字体名 SimSun → TimesNewRomanPSMT ⇐ out-origin-5-round5.txt J1，本轮复跑逐字节复现）。"
                "⚠️ **次序坑**：主题必须在导出时施加，否则新建的文本注释回 SimSun（半张图两种字体 ⇐ J4）；"
                "⚠️ 给不存在的主题名**静默成功**（exec_ok=True、产物不变 ⇐ J3）⇒「设上了」只能由产物证明。"
                "⚠️ 本格标 `not-embedded` 的理由：Origin 导出的 PDF **不内嵌字体**（34/34 个产物 "
                "`/FontFile*` = 0 ⇐ out-pdf-embedding-scan.txt）⇒ 字体族判据（`F6`）对它只能判 `N/A`。",
                status="not-embedded"),
        },
        "font.serif": {
            "python": {"how": "入库 OTF TeXGyreTermesX（随 skill，干净检出可用）", "status": "family-equivalent"},
            "matlab": {"how": "系统 Times New Roman（点名即内嵌，非静默回退）", "status": "family-equivalent"},
            "origin": origin(
                "同 `font.family`：Origin 侧取系统 Times New Roman（衬线族的一员），落地命令 = 导出时 "
                "`theme:=\"Times New Roman Font\"`。⚠️ Origin 导出的 PDF **不内嵌**该字体"
                "（/FontFile*=0 ⇐ out-pdf-embedding-scan.txt）⇒ 最终呈现取决于打开它的机器；"
                "本格标 `not-embedded`：字体族判据（`F6`）对它只能判 `N/A`。",
                status="not-embedded"),
        },
        "lines.linewidth": {
            "python": {"how": "lines.linewidth", "status": "same-value"},
            "matlab": {"how": "set(h,'LineWidth',v)", "status": "same-value"},
            "origin": origin(
                "`layer.plotN.line.width = <pt>`（LabTalk；实测默认 0.5、可写，改后产物**差分像素非零** ⇒ "
                "真的落到产物上 ⇐ out-d-appearance.txt / out-f-axis-candidates.txt，本轮复跑复现）。"),
        },
        # H10（M3-style 终审 I-5 补进表）：载体相关规则。python 侧已落地（6 键 + 入库探针）；
        #   matlab 侧由 M3-plot-matlab Task 2 的**入库探针**补齐产物级实测 ⇒ 由 not-landable 转 same-value
        #   （2026-10-01）；origin 侧仍是 not-landable（侦察逐条试过、差分像素全 0）。
        "h10.axes_box": {
            "python": {
                "how": "`mcm.mplstyle` 的生成区为它落了 **6 个键**：`axes.spines.top: False` / "
                       "`axes.spines.right: False`（去上/右边框线）· `xtick.top: False` / "
                       "`ytick.right: False`（底座 `science` 自带 `xtick.top/ytick.right=True` ⇒ 只关 "
                       "spines 会留**悬空刻度**）· `xtick.minor.visible: False` / "
                       "`ytick.minor.visible: False`（只留主刻度）。**刻度朝内**由底座 `science` 的 "
                       "`xtick.direction='in'` 带出（入库探针 `probe-gap1-hanging-ticks.py` 的"
                       "带内墨迹读数即据它算：落地态顶/右带均 0、旧态对照 234/120）；**轴标签带单位**"
                       "是调用方纪律（GREEN 写手在 `make_figure.py` 里写 `Slope (deg)` 一类），"
                       "载体侧无设置项。（⇐ .claude/skills/mcm-plot-python/assets/mcm.mplstyle / "
                       "tests/skills/plot-python/probe-gap1-hanging-ticks.py）",
                "status": "same-value"},
            "matlab": {
                "how": "**产物级实测能落地**（2026-10-01 M3-plot-matlab Task 2 回读，取代旧稿的"
                       "「能设、不能验」）：`mcmplot.m` 的 H10 生成区落 `box(ax,'off')`（去上/右边框线；"
                       "MATLAB 的 `box` 一并管顶与右）+ `set(ax,'TickDir','in')`（刻度朝内）+ "
                       "`XMinorTick`/`YMinorTick` off（只留主刻度）。**入库探针** "
                       "`tests/skills/plot-matlab/probe-h10-band-ink.py` 量**轴区顶/右带内非白像素**"
                       "（灰度 < 200；带宽 = 刻度长换算 px + 2 余量，现算；口径同 python 侧 "
                       "`probe-gap1-hanging-ticks.py`）：**落地态**（`M.apply()`）顶内 0 / 右内 0 / 下外 0，"
                       "**对照态**（`apply` 之后把 `box` 打开、`TickDir` 改回 out）顶内 2902 / 右内 2346 / "
                       "下外 349（本机 R2025b Update 5）⇒ 框线与刻度朝向**真的从产物上消失**（对照非 0 "
                       "同时证探针不是恒零）。**轴标签带单位**是**调用方纪律**（MATLAB 侧**无设置项**）。",
                "status": "same-value"},
            "origin": origin(
                "**去上/右框线与刻度朝内：侦察**未找到**能落到产物上的命令** —— 逐条试过 "
                "`layer.frame=0` / `layer.x2.show=0; layer.y2.show=0` / `layer.x.opposite=0|1` / "
                "`layer.x.tickDir=1` / `layer.x.tickdir=1` / `layer.x.tick.direction=1`，"
                "**改前后图像差分像素全为 0**（⇐ tests/m3-origin-probe/out-f-axis-candidates.txt / "
                "out-i-dpi-pagesize-frame.txt）。只有 `layer.x.minorTicks=0` 有非零差分（15 px，"
                "「只留主刻度」或有路）⇒ 整条规则**今天无落地**，如实记 `not-landable`。",
                status="not-landable"),
        },
    }


def carriers_for(key, vals):
    """取某 id 的载体落地表；缺 ⇒ `GeneratorError`（Global Constraint 4：全收条目**逐格**标落地状态）。

    `vals` 透传给 `carrier_map()`（`h1.width_ratio.*` 的 `how` 要用它取**本格**键名与值）。
    另守：每格的 `status` 必须 ∈ 模块级 `STATUSES`（唯一声明）—— 越界 ⇒ `GeneratorError`（fail-closed）。"""
    c = carrier_map(vals).get(key)
    if not c:
        raise GeneratorError(f"{key}：carrier_map() 缺该 id 的载体落地表（Global Constraint 4 要求逐格标）")
    for carrier, cell in c.items():
        st = cell.get("status")
        if st not in STATUSES:
            raise GeneratorError(f"{key}.{carrier}：status={st!r} 不在 STATUSES {STATUSES} 里"
                                 f" —— 状态值必须取自唯一声明（fail-closed）")
    return c


def build(doc_path):
    text = pathlib.Path(doc_path).read_bytes().decode("utf-8")
    scalars, seq = extract(text)
    vals = {k: v for k, v, _ in scalars}        # {json_id: 规范原值串}，供 width 各格的 how 现取
    entries = []
    for key, raw, origin in scalars:
        entries.append({"id": key, "clause": key.split(".")[0].upper(),
                        "value": (float(raw) if "." in raw else int(raw)),
                        "origin": origin, "carriers": carriers_for(key, vals)})
    for key, val, origin, clause, why in CONSTS:
        if val is _H14:
            val = seq["series.color"]          # ★ 从 H14 锚点现取（不手抄）
        entries.append({"id": key, "clause": clause, "value": val, "origin": origin,
                        "why": why, "carriers": carriers_for(key, vals)})
    return {"_generated_by": "tests/skills/figure-choose/gen-style-table.py",
            "_source": str(HOUSE.relative_to(ROOT)).replace("\\", "/"),
            # ★ 表头（2026-10-01 补）：`status` 的**正面定义**（`STATUS_DEFS`）。写进表头是为了让
            #   **表自身**带上"每个 status 是什么意思"，而不是只在下游生成器的注释里 —— 下游
            #   （`mcm-plot-*`）读表时能直接看到口径，无需回读生成器。（Task 2 硬要求 6(a)：写进生成器与表头）
            "_status_defs": STATUS_DEFS,
            "entries": entries}


def main():
    ap = argparse.ArgumentParser(description="从 house-style.md 重放 mcm-style.json（载体无关样式表）")
    ap.add_argument("--doc", default=None, help="被抽的规范（默认 = 仓内 house-style.md；变异/演示用）")
    ap.add_argument("--check", action="store_true", help="只比对派生件是否与重放结果一致（不写文件）")
    a = ap.parse_args()
    doc = a.doc or HOUSE
    try:
        data = build(doc)
    except GeneratorError as e:
        print(f"FAIL  ANCHOR  {e}", file=sys.stderr)
        return 1
    body = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if a.check:
        cur = OUT.read_bytes().decode("utf-8") if OUT.is_file() else None
        if cur != body:
            print("FAIL  STALE  派生件与重放结果不一致", file=sys.stderr)
            return 1
        print(f"重放 → {OUT.relative_to(ROOT).as_posix()}（{len(data['entries'])} 条）· 一致")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(body.encode("utf-8"))          # ★ write_bytes，全仓禁 write_text
    print(f"重放 → {OUT.relative_to(ROOT).as_posix()}（{len(data['entries'])} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
