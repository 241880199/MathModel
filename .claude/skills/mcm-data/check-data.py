#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`check-data.py` —— `mcm-data` 机械层判据 `DA1`–`DA5`（外检）+ 三条交付件自洽自检（内检）。

依据
----
* 判据定义：`docs/superpowers/specs/2026-10-04-m5-data-code-design.md` §4.1
  （`DA1`–`DA5` 的定义与依据）。
* 逐字契约：`docs/superpowers/specs/2026-10-04-m5-data-code-conventions.md`
  §1.1（七列列头）· §2（文件契约）· §5（`N/A` 与空集三分口径）· §6（依据标注分派表）
  · §8（`--scope` 取值表）。
* 硬约束：`docs/superpowers/plans/2026-10-04-m5-data-code.md` 的 `GC5`/`GC6`/`GC7`/`GC8`/`GC9`
  与质检记录 `P5`/`P6`/`P7`。
* 靶子（本检查器判的就是照着它产出的东西）：`.claude/skills/mcm-data/SKILL.md` ·
  `.claude/skills/mcm-data/assets/data-source-table.md` · 四份 `references/`。

## 两个 `--scope`（**取值写死，见约定件 §8**）

    python .claude/skills/mcm-data/check-data.py --scope self
    python .claude/skills/mcm-data/check-data.py --scope artifact <表文件> [--refs <论文文件>]

* `--scope self` —— **内检**：本仓交付件自洽。**无目标参数**。三条（进收工门）：
  - `SELF1` `SKILL.md` 的 §4 边界**两句在场**（通用句 + `mcm-data` 特有句）；
    ★ 比对前**先剥掉 `**` / `` ` `` 再逐字比**（约定件 §4 末注的 `GC3` 裁定）——
    **不许拿带 Markdown 标记的串直接比**（否则加粗与否会造成假红/假绿）。
  - `SELF2` `references/` 的内部**指针不悬空**（盘检 skill 目录内 `references/` · `assets/` · `SKILL.md`）。
  - `SELF3` `assets/data-source-table.md` 的表头**与约定件 §1.1 逐字一致**（七列 + 七格分隔行）。
* `--scope artifact <表文件> [--refs <论文文件>]` —— **外检**：用户赛期真实来源表文件。
  ★ **`N/A` 出口是前提**（约定件 §5 —— 用户产物形态未知，查不到不等于违规）。
  `--refs` 不给 ⇒ `DA2` 判 `N/A`（与 `mcm-code` 的 `CD4 --appendix` 同型）。

## 五条判据（设计 §4.1；**依据标注**见约定件 §6）

* `DA1` 来源表在场，且 `出处` / `口径` / `局限` / `获取日期` / `取数方` 五列每行非空。`[社区]`
  ★ 另判 `取数方` 的**取值**（规范化后）**只许** `本人` / `AI` —— 出现第三种取值 ⇒ 红（**fail-closed**）。
* `DA2` **每个非自主来源**都有对应引用。`[官方]` `corpus/official/instructions.html:1121`
  ★ **机械判法（约定件 §8 · 计划件硬要求 2 写死）**：**给了 `--refs`** ⇒ `出处` 列的**每个非自主值
  都必须能在 `--refs` 文件里被搜到**（**没搜到 ⇒ 红**）；**不给 `--refs`** ⇒ 判 `N/A`。
  ★ **保留值豁免（设计 §3.1 · 2026-10-04 裁定）**：`出处` 取**保留值 `本队自产`** 的行是**自产来源**，
  **不参与**这条搜索（该行仍须满足 `DA1` 非空 / `DA4` 确认闸）。
* `DA3` `可信度层级` 列每行非空，且取值在五级内（设计 §3.3）。`[社区]`
  ★ **保留值豁免（设计 §3.3 · 2026-10-04 裁定）**：`出处` 取**保留值 `本队自产`** 的行**豁免本判据**
  —— 自产数据没有"外部可信度层级"；该行 `可信度层级` 列填保留记号 `—`，本判据不查该列。
* `DA4` **凡 `取数方=AI` 的行，`确认` 必须为「已核」且记确认人 + 日期**。`[社区]`
  ★ `取数方` 比对前先**规范化**：去首尾空白 + 去反引号 + 大小写不敏感 + **允许 `AI` 前缀**
  （`ai` / `AI检索` / `AI 检索` 都算 **AI 行**；否则写成变体会**假绿**）。
  ★ 它是设计 §1.2 那句边界话的机械落地（质检记录 `P6`）；**不是官方要求**
  （官方只把「解释数据与模型结果」列在建议谨慎侧 `[官方]`，判据规则本身是本套件自订）。
* `DA5` 清洗与口径对齐步骤有记录，且每步可重跑。`[社区]`

## `N/A` 与空集的【三分口径】（约定件 §5 · `GC5`/`GC6`/`P7`）—— 三情形分开实现

| 情形 | 触发 | 判 |
| :--- | :--- | :--- |
| A 目标物/文件**不存在** | `--scope artifact` 的表文件 / `--refs` 的论文文件不在 | `N/A`（不计入失败） |
| B **节不在** | 表文件在，但 `## 来源表` / `## 清洗步骤` 不在 | `N/A` |
| C **节 / 表在场但零行** | 该节在，但表体零数据行 / 有序列表零项 | `FAIL`（**空集不许判绿**） |

★ 一旦表在场（有数据行），**列内取值缺失即判红**，不再走 `N/A`（约定件 §5.1）。

## ★ 模板守卫（Task 1 复核的硬口径）

`--scope artifact` 的**目标路径若落在 `.claude/skills/mcm-data/assets/` 下 ⇒ 直接 `FAIL`**，
打印「那是模板，不是用户产物」。理由：`assets/data-source-table.md` **自己就是空表**
（表头 + 分隔行、零数据行）；若被当成合法靶子，会与「**节在但零行 ⇒ FAIL**」串成一个
**自相矛盾的假红/假绿**。

## 已知边界（**不声称穷尽** · 设计 §4.4）

* **查不到"数据是不是真的"** —— 只查来源表与确认记录**是否在场**，不查 URL 里是否真有那个数。
* **查不到"口径选得对不对"** —— 只查 `口径` 列非空，不判内容。
* `DA3` 的"五级内"是**启发式**：认**层级号 `1`–`5` 起首**或**含五级名之一**；缩写/别名可能漏判。
  ★ **保留值豁免（设计 §3.3 · 2026-10-04 裁定）**：`出处` 取**保留值 `本队自产`** 的行**豁免本判据**
  —— 自产数据没有"外部可信度层级"；该行 `可信度层级` 填保留记号 `—`，本判据不查该列。
  ★ 与 `DA2` 的豁免**同一保留值、同一裁定出处**（设计 §3.1 / §3.3）⇒ 两条判据**一致地**放行自产行。
* `DA5` 的"可重跑"是**启发式**：认**脚本/命令标记**（见 `_RERUN_RE`）；手写步骤若措辞不含这些
  字面，会被判"不可重跑"（**假红可能**）。
* `DA2` 的"出处"是**全列搜子串**；`出处` 写成题面附件名时**同样要求它在 `--refs` 里出现**。
  ★ **保留值豁免**：`出处` 取**保留值 `本队自产`** 的行 = **自产来源**，**不参与**这条搜索；
  一旦某表的 `出处` **全部**是保留值 ⇒ 无非自主来源 ⇒ 判 `PASS`（势=0）。
* `取数方` 的规范化是**前缀式**：归一后凡以 `AI` 起首即算 AI 行（`AI检索` / `ai` / `AI 检索` 等）；
  同时 `DA1` 判 `取数方` **只许** `本人` / `AI`（规范化后），第三种取值 ⇒ 红（fail-closed，不静默放过）。
* `--scope self` 的 `SELF2` **只盘检 skill 目录内**（`references/` · `assets/` · `SKILL.md`）；
  `corpus/` 起始的指针**不在射程内**（`references/cleaning.md` 里就有一条**故意指向不存在的
  `corpus/官方原题/INDEX.md`** 的说明，收进来会恒红）。

★ 末行恒为 `RESULT: …`；退出码 **0 / 1**（判红 = 1；用法错 = 2）。每条判词一行，形态 `PASS|FAIL|N/A  <id>  <读数>`。
"""

import argparse
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]                 # …/mcm-data/check-data.py → 仓根
SKILL_DIR = ROOT / ".claude/skills/mcm-data"                       # 默认 skill 根（`--skill-dir` 可改）
ASSETS = SKILL_DIR / "assets"                                      # 模板守卫的默认判据面

# ---- 逐字契约（约定件 §1.1；与设计 §3.1 一致）-----------------------------
HEADER_LINE = "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 | 确认 |"
HEADER_COLS = ["出处", "口径", "局限", "获取日期", "可信度层级", "取数方", "确认"]

# `DA1` 判的五列（`可信度层级` 归 `DA3`、`确认` 归 `DA4`）
DA1_COLS = ["出处", "口径", "局限", "获取日期", "取数方"]

# ★ `出处` 的**保留值**：取该值的行 = 自产来源，豁免 `DA2` 的引用搜索（设计 §3.1 · 2026-10-04 裁定）
SELF_SOURCED = "本队自产"

# 可信度五级（设计 §3.3 · `references/source-credibility.md`）
LEVELS = ["官方统计口", "国际组织与学术", "开放数据平台", "商业与行业报告", "媒体与转引"]

# 边界两句（约定件 §4.1 / §4.2；比对前先剥 `**` / 反引号 —— 见文件头 `SELF1`）
GEN_BOUNDARY = "本 skill 给出数据来源与代码规范；最终判断与结论由队员负责。"
DATA_BOUNDARY = "凡由 AI 检索到的数据，队员必须逐条确认可靠性后方可引用"

# 全仓唯一的判据名册（约定件 §3）；`--scope artifact` **逐条**据此出判词
CRITERIA = ("DA1", "DA2", "DA3", "DA4", "DA5")

# `DA5` 的"可重跑"标记（启发式，见"已知边界"）：脚本/命令/解释器/代码文件扩展名
_RERUN_RE = re.compile(
    r"脚本|命令|运行|reproduce|rerun|python\s|matlab\s|Rscript|"
    r"\.(?:py|m|sh|ipynb|R)\b",
    re.IGNORECASE)

# 日期串（`DA4` 判"记了日期"用）：YYYY-MM-DD / YYYY/M/D / YYYY年M月D日
_DATE_RE = re.compile(r"(\d{4}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2})")

_HEAD2_RE = re.compile(r"^#{2}\s+(.+?)\s*$")          # 恰好 level-2 标题
_NUM_ITEM_RE = re.compile(r"^\s*\d+[.)]\s+(.+?)\s*$")  # 有序列表项
_BACKTICK_RE = re.compile(r"`([^`]+)`")


# ---------------------------------------------------------------- 基础 IO / 解析
def read_text(path):
    """读一个文本文件；读不出 ⇒ `None`（fail-closed 的入口）。"""
    try:
        return pathlib.Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _norm(s):
    """剥掉 `**` / 反引号，再把空白折叠成单空格 —— `GC3` 裁定的比对前归一。"""
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", " ", s)


def _section_body(text, name):
    """取 level-2 标题 `## <name>` 的正文（到下一个 `## ` 标题为止）；找不到 ⇒ `None`。"""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        m = _HEAD2_RE.match(ln)
        if m:
            if start is not None:
                return "\n".join(lines[start:i])
            if m.group(1).strip() == name:
                start = i + 1
    return "\n".join(lines[start:]) if start is not None else None


def _first_table(body):
    """从节正文里取**第一段连续的 `|` 行**（表块）；没有 ⇒ `[]`。"""
    cur = []
    for ln in body.splitlines():
        if ln.lstrip().startswith("|"):
            cur.append(ln)
        elif cur:
            return cur
    return cur


def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _is_sep(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells)


def _ordered_items(body):
    """节正文里的有序列表项文本（每项一行）—— `DA5` 的对象集合。"""
    items = []
    for ln in body.splitlines():
        m = _NUM_ITEM_RE.match(ln)
        if m:
            items.append(m.group(1))
    return items


def _pad(row, n):
    return (list(row) + [""] * n)[:n]


def _norm_party(v):
    """规范化 `取数方`：去首尾空白 + 去反引号 + 大小写不敏感 + **允许 `AI` 前缀**。

    返回归一后的取值 `"本人"` / `"AI"`；**第三种取值（含空）⇒ `None`**（`DA1` 据此判红，fail-closed）。
    例：`ai` / `AI检索` / `AI 检索` / ` AI ` 一律归 `"AI"`；`本人` 归 `"本人"`。
    """
    v = v.strip().strip("`").strip()
    if not v:
        return None
    if v.upper().startswith("AI"):
        return "AI"
    if v == "本人":
        return "本人"
    return None


# ---------------------------------------------------------------- `--scope artifact` 状态
class State(object):
    def __init__(self, target, refs):
        self.target = pathlib.Path(target)
        self.refs = pathlib.Path(refs) if refs else None
        self.missing = not self.target.exists()
        self.unreadable = False
        self.src_body = None
        self.clean_body = None
        self.header = None
        self.colmap = {}
        self.data_rows = []

        text = None if self.missing else read_text(self.target)
        if not self.missing and text is None:
            self.unreadable = True
            return
        if text is None:
            return

        self.src_body = _section_body(text, "来源表")
        self.clean_body = _section_body(text, "清洗步骤")

        if self.src_body is not None:
            table = _first_table(self.src_body)
            if table:
                self.header = _cells(table[0])
                if self.header == HEADER_COLS:
                    self.colmap = {c: i for i, c in enumerate(self.header)}
                    body_rows = table[1:]
                    if body_rows and _is_sep(_cells(body_rows[0])):
                        body_rows = body_rows[1:]
                    self.data_rows = [_pad(_cells(r), len(HEADER_COLS)) for r in body_rows]
                else:
                    self.header = None      # 表头与契约不符 ⇒ 视作"无七列表"
                    self.data_rows = []

    # ---- 三情形判定（A 目标缺失 / B 节缺失 / C 零行）的公共前置 ----
    def pre(self):
        """返回 `(status, reason)`：判定前的共同出口；`None` ⇒ 继续往下按列判。"""
        if self.missing:
            return "N/A", "目标文件不存在（情形 A）"
        if self.unreadable:
            return "FAIL", "目标文件读不出（fail-closed）"
        return None

    def src_pre(self):
        r = self.pre()
        if r:
            return r
        if self.src_body is None:
            return "N/A", "节 `## 来源表` 不在本文件（情形 B）"
        if not self.header:
            return "FAIL", "`## 来源表` 下无七列表（表头与 §1.1 不符）"
        if not self.data_rows:
            return "FAIL", "节 `## 来源表` 在但零数据行（情形 C · 空集不许判绿）"
        return None


# ---------------------------------------------------------------- DA1
def da1(st):
    r = st.src_pre()
    if r:
        return r
    bad = []
    for i, row in enumerate(st.data_rows, 1):
        for col in DA1_COLS:
            if not row[st.colmap[col]]:
                bad.append("第%d行 `%s` 空" % (i, col))
        party = row[st.colmap["取数方"]]
        if party and _norm_party(party) is None:
            bad.append("第%d行 `取数方`「%s」非法（只许 `本人` / `AI`）" % (i, party))
    detail = "势=%d（数据行）· 五列有空 / 取值非法 %d 处" % (len(st.data_rows), len(bad))
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- DA2
def _is_self_sourced(row, colmap):
    """`出处` 取**保留值 `本队自产`** 的行 = 自产来源（设计 §3.1 / §3.3 · 2026-10-04 裁定）。

    该行**豁免 `DA2`**（不必在 `--refs` 里被搜到）**与 `DA3`**（`可信度层级` 填保留记号 `—`）。
    """
    return row[colmap["出处"]].strip().strip("`").strip() == SELF_SOURCED


def da2(st):
    """非自主来源须引用（`[官方]` `corpus/official/instructions.html:1121`）。"""
    if st.refs is None:
        return "N/A", "未给 `--refs` ⇒ 无引用靶子（约定件 §8；与 `CD4 --appendix` 同型）"
    r = st.pre()
    if r:
        return r
    if not st.refs.exists():
        return "N/A", "论文文件（`--refs`）不存在 ⇒ 无引用靶子（情形 A）"
    refs_text = read_text(st.refs)
    if refs_text is None:
        return "FAIL", "论文文件（`--refs`）读不出（fail-closed）"
    if st.src_body is None:
        return "N/A", "节 `## 来源表` 不在本文件（情形 B）"
    if not st.header or not st.data_rows:
        return "FAIL", "`## 来源表` 无七列表 / 零数据行 ⇒ 出处集合为空（空集不许判绿）"

    vals = []
    exempt = 0
    for row in st.data_rows:
        v = row[st.colmap["出处"]].strip().strip("`").strip()
        if _is_self_sourced(row, st.colmap):   # ★ 保留值：自产来源，豁免引用要求（设计 §3.1 裁定）
            exempt += 1
            continue
        if v and v not in vals:
            vals.append(v)
    if not vals:
        if exempt:
            return "PASS", ("势=0（不同非自主 `出处` 值）· %d 行标为保留值 `%s` ⇒ 无引用要求"
                             % (exempt, SELF_SOURCED))
        return "FAIL", "`出处` 列每行皆空 ⇒ 非自主出处集合为空（空集不许判绿）"
    miss = [v for v in vals if v not in refs_text]
    detail = "势=%d（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 %d 条" % (len(vals), len(miss))
    if exempt:
        detail += "  · 自产豁免 %d 行" % exempt
    if miss:
        detail += "  <<< " + " ; ".join("「%s」" % m for m in miss[:4]) + (" …" if len(miss) > 4 else "")
    return ("PASS" if not miss else "FAIL"), detail


# ---------------------------------------------------------------- DA3
def _level_ok(v):
    """`可信度层级` 取值在五级内（启发式）：层级号 `1`–`5` 起首，或含五级名之一。"""
    v = v.strip()
    if not v:
        return False
    if re.match(r"^[1-5](\D|$)", v):
        return True
    return any(name in v for name in LEVELS)


def da3(st):
    r = st.src_pre()
    if r:
        return r
    bad = []
    exempt = 0
    for i, row in enumerate(st.data_rows, 1):
        if _is_self_sourced(row, st.colmap):   # ★ 自产行豁免本判据（设计 §3.3 裁定）
            exempt += 1
            continue
        v = row[st.colmap["可信度层级"]]
        if not v:
            bad.append("第%d行 空" % i)
        elif not _level_ok(v):
            bad.append("第%d行「%s」不在五级内" % (i, v))
    detail = "势=%d（数据行）· 空缺/越级 %d 处" % (len(st.data_rows), len(bad))
    if exempt:
        detail += "  · 自产豁免 %d 行" % exempt
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- DA4
def _confirm_ok(v):
    """`确认` 列：含「已核」且记确认人 + 日期。返回 `(bool, 原因)`。"""
    v = v.strip()
    if not v:
        return False, "空"
    if "待核" in v:
        return False, "仍为「待核」"
    if "已核" not in v:
        return False, "既非「已核」也非「待核」"
    inner = v
    m = re.search(r"[（(]([^）)]*)[）)]", v)
    if m:
        inner = m.group(1)
    if not _DATE_RE.search(inner):
        return False, "未记日期"
    parts = [p.strip() for p in re.split(r"[,，]", inner) if p.strip()]
    named = [p for p in parts if not _DATE_RE.fullmatch(p)]
    if not named:
        return False, "未记确认人"
    return True, ""


def da4(st):
    """★ 核心：凡 `取数方=AI` 的行，`确认` 必须为「已核」+ 确认人 + 日期（`P6`）。"""
    r = st.src_pre()
    if r:
        return r
    ai = [(i, row) for i, row in enumerate(st.data_rows, 1)
          if _norm_party(row[st.colmap["取数方"]]) == "AI"]
    bad = []
    for i, row in ai:
        ok, why = _confirm_ok(row[st.colmap["确认"]])
        if not ok:
            bad.append("第%d行；%s" % (i, why))
    detail = ("势=%d（`取数方=AI` 的行）· 未确认 %d 处"
              % (len(ai), len(bad))
              + ("  ★ 0 条 AI 行 ⇒ 无从判（若来源表本应有 AI 行，请先查 `取数方` 列）"
                 if not ai else ""))
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- DA5
def da5(st):
    r = st.pre()
    if r:
        return r
    if st.clean_body is None:
        return "N/A", "节 `## 清洗步骤` 不在本文件（情形 B）"
    items = _ordered_items(st.clean_body)
    if not items:
        return "FAIL", "节 `## 清洗步骤` 在但零步骤项（情形 C · 空集不许判绿）"
    bad = [i for i, it in enumerate(items, 1) if not _RERUN_RE.search(it)]
    detail = "势=%d（清洗步骤项）· 不可重跑 %d 项" % (len(items), len(bad))
    if bad:
        detail += "  <<< 第 %s 项无脚本/命令标记" % "/".join(str(b) for b in bad[:6])
    return ("PASS" if not bad else "FAIL"), detail


ARTIFACT_FUNCS = {"DA1": da1, "DA2": da2, "DA3": da3, "DA4": da4, "DA5": da5}


# ---------------------------------------------------------------- `--scope self`
def self1(skill_dir):
    """`mcm-data/SKILL.md` 的 §4 边界**两句在场**（比对前剥 `**` / 反引号）。"""
    skill_md = skill_dir / "SKILL.md"
    text = read_text(skill_md)
    if text is None:
        return "FAIL", "`SKILL.md` 读不出 ⇒ 无可检对象（fail-closed）"
    norm = _norm(text)
    miss = [s for s in (GEN_BOUNDARY, DATA_BOUNDARY) if _norm(s) not in norm]
    detail = "势=2（边界句）· 缺 %d 句" % len(miss)
    if miss:
        detail += "  <<< " + " ; ".join("「%s」" % m for m in miss)
    return ("PASS" if not miss else "FAIL"), detail


def self2(skill_dir):
    """`references/` 的内部指针不悬空（盘检 skill 目录内的 `references/` · `assets/` · `SKILL.md`）。"""
    skill_md = skill_dir / "SKILL.md"
    scan = []
    if skill_md.exists():
        scan.append(skill_md)
    for d in (skill_dir / "references", skill_dir / "assets"):
        if d.is_dir():
            scan.extend(sorted(d.rglob("*.md")))
    seen = {}
    for f in scan:
        txt = read_text(f)
        if txt is None:
            continue
        for tok in _BACKTICK_RE.findall(txt):
            tok = tok.strip()
            if tok.startswith("references/") or tok.startswith("assets/") or tok == "SKILL.md":
                seen.setdefault(tok, f)
    if not seen:
        return "FAIL", "势=0：skill 目录内没有 `references/` / `assets/` / `SKILL.md` 内部指针（fail-closed）"
    bad = []
    for tok, f in sorted(seen.items()):
        if not (skill_dir / tok).exists():
            bad.append("悬空 `%s`（于 %s）" % (tok, f.relative_to(skill_dir).as_posix()))
    detail = "势=%d（内部指针）· 悬空 %d 条" % (len(seen), len(bad))
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


def self3(skill_dir):
    """`assets/data-source-table.md` 的表头与约定件 §1.1 **逐字一致**（七列 + 七格分隔行）。"""
    text = read_text(skill_dir / "assets/data-source-table.md")
    if text is None:
        return "FAIL", "`assets/data-source-table.md` 读不出（fail-closed）"
    body = _section_body(text, "来源表")
    if body is None:
        return "FAIL", "模板缺 `## 来源表` 节"
    table = _first_table(body)
    if not table:
        return "FAIL", "模板 `## 来源表` 下无表"
    bad = []
    if table[0].strip() != HEADER_LINE:
        bad.append("表头与 §1.1 逐字不符：%s" % table[0].strip())
    if len(table) < 2 or not _is_sep(_cells(table[1])) or len(_cells(table[1])) != len(HEADER_COLS):
        bad.append("分隔行缺失或非七格")
    detail = "势=1（模板表头）· 不符 %d 处" % len(bad)
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return ("PASS" if not bad else "FAIL"), detail


SELF_FUNCS = (("SELF1", self1), ("SELF2", self2), ("SELF3", self3))


# ---------------------------------------------------------------- main
def _print_rows(rows):
    for rid, (st, detail) in rows:
        print("%-4s  %s  %s" % (st, rid, detail))
    fails = [rid for rid, (st, _d) in rows if st == "FAIL"]
    nas = [rid for rid, (st, _d) in rows if st == "N/A"]
    print("-" * 78)
    print("判据 %d 条 · 红 %d 条 · N/A %d 条" % (len(rows), len(fails), len(nas)))
    if not fails:
        print("RESULT: PASS" + ("  [N/A %s]" % ",".join(nas) if nas else ""))
    else:
        print("RESULT: FAIL（%s）" % ",".join(fails))
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="`mcm-data` 机械层判据：外检 `DA1`–`DA5` + 内检（交付件自洽）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "两个 `--scope`（取值写死 · 约定件 §8）：\n"
            "  self                      内检：本仓交付件自洽（SELF1 边界两句 / SELF2 指针不悬空 /\n"
            "                            SELF3 模板表头逐字）。无目标参数。进收工门。\n"
            "  artifact <表文件>         外检：用户赛期真实来源表文件。\n"
            "                            ★ `N/A` 出口是前提（约定件 §5）。\n"
            "可选：--refs <论文文件>     给了 ⇒ `DA2` 判「每个**非自主** `出处` 都要能在该文件里搜到」；\n"
            "                            不给 ⇒ `DA2` 判 `N/A`（与 `mcm-code` 的 `CD4 --appendix` 同型）。\n"
            "                            ★ 自产来源用保留值 `本队自产` 标记 ⇒ 该行豁免引用（`DA2`）与层级（`DA3`）要求。\n"
            "\n"
            "示例:\n"
            "  python .claude/skills/mcm-data/check-data.py --scope self\n"
            "  python .claude/skills/mcm-data/check-data.py --scope artifact data-sources.md --refs paper.md\n"))
    ap.add_argument("--scope", required=True, choices=["self", "artifact"],
                    help="self = 内检（本仓交付件自洽，无目标）· artifact = 外检（用户赛期真实来源表文件）")
    ap.add_argument("target", nargs="?", default=None,
                    help="--scope artifact 时的来源表文件路径（--scope self 时不用给）")
    ap.add_argument("--refs", default=None,
                    help="--scope artifact 时的论文文件（给了才判 DA2；不给 ⇒ DA2 = N/A）")
    ap.add_argument("--skill-dir", dest="skill_dir", default=None,
                    help="skill 根（默认仓内 `.claude/skills/mcm-data`；变异探针可指到副本，"
                         "只影响 `--scope self`）")
    a = ap.parse_args(argv)

    if a.scope == "self":
        if a.target is not None:
            print("用法错：`--scope self` 不吃目标参数（约定件 §8）。", file=sys.stderr)
            return 2
        skill_dir = pathlib.Path(a.skill_dir) if a.skill_dir else SKILL_DIR
        print("check-data.py · scope=self")
        print("skill-dir = %s" % skill_dir)
        rows = [(rid, fn(skill_dir)) for rid, fn in SELF_FUNCS]
        return _print_rows(rows)

    # ---- scope == artifact ----
    if a.target is None:
        print("用法错：`--scope artifact` 必须给一个表文件路径（约定件 §8）。", file=sys.stderr)
        return 2

    target = pathlib.Path(a.target).resolve()
    assets = ASSETS.resolve()
    print("check-data.py · scope=artifact")
    print("target = %s" % target)
    if a.refs:
        print("refs   = %s" % pathlib.Path(a.refs))

    # ★ 模板守卫：目标落在 assets/ 下 ⇒ 直接 FAIL（那是模板，不是用户产物）
    try:
        under_assets = os.path.commonpath([str(target), str(assets)]) == str(assets)
    except ValueError:                       # 不同盘符等
        under_assets = False
    if under_assets:
        print("FAIL  TEMPLATE  目标落在 `.claude/skills/mcm-data/assets/` 下 —— "
              "那是模板，不是用户产物（模板表本身零数据行，不可当靶子）。")
        print("-" * 78)
        print("判据 1 条 · 红 1 条 · N/A 0 条")
        print("RESULT: FAIL（TEMPLATE）")
        return 1

    st = State(a.target, a.refs)
    rows = [(rid, ARTIFACT_FUNCS[rid](st)) for rid in CRITERIA]
    return _print_rows(rows)


if __name__ == "__main__":
    sys.exit(main())
