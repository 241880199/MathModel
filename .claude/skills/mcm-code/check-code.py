#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`check-code.py` —— `mcm-code` 机械层判据 `CD1`–`CD6`（外检）+ 三条交付件自洽自检（内检）。

依据
----
* 判据定义：`docs/superpowers/specs/2026-10-04-m5-data-code-design.md` §4.2
  （`CD1`–`CD6` 的定义与依据）。
* 逐字契约：`docs/superpowers/specs/2026-10-04-m5-data-code-conventions.md`
  §1.2（五列列头）· §2.2 / §2.3（文件契约与解析器口径）· §3（判据编号）
  · §4.3（`mcm-code` 的边界句）· §5（`N/A` 与空集三分口径 + 第四态）
  · §6（依据标注分派表）· §8（`--scope` 取值表）。
* 硬约束：`docs/superpowers/plans/2026-10-04-m5-data-code.md` 的
  `GC5`/`GC6`/`GC7`/`GC8`/`GC9`/`GC12` 与质检记录 `P5`/`P6`/`P7`。
* 靶子（本检查器判的就是照着它产出的东西）：`.claude/skills/mcm-code/SKILL.md` ·
  `.claude/skills/mcm-code/assets/result-manifest.md` · 三份 `references/` · 两份 `assets/` 脚手架。

## 两个 `--scope`（**取值写死，见约定件 §8**）

    python .claude/skills/mcm-code/check-code.py --scope self
    python .claude/skills/mcm-code/check-code.py --scope artifact <代码目录> [--appendix <论文文件>]

* `--scope self` —— **内检**：本仓交付件自洽。**无目标参数**。三条（进收工门）：
  - `SELF1` `SKILL.md` 的边界**两句在场**（通用句 + `mcm-code` 特有句）；
    ★ 比对前**先剥掉 `**` / `` ` `` 再逐字比**（约定件 §4 末注的 `GC3` 裁定）——
    **不许拿带 Markdown 标记的串直接比**（否则加粗与否会造成假红/假绿）。
  - `SELF2` `references/` 的内部**指针不悬空**（盘检 skill 目录内 `references/` · `assets/` · `SKILL.md`）。
  - `SELF3` `assets/result-manifest.md` 的表头**与约定件 §1.2 逐字一致**（五列 + 五格分隔行）。
* `--scope artifact <代码目录> [--appendix <论文文件>]` —— **外检**：用户赛期真实代码目录。
  ★ **`N/A` 出口是前提**（约定件 §5 —— 用户产物形态未知，查不到不等于违规）。
  ★ **结果清单文件 = `<代码目录>/result-manifest.md`**（不是另开 flag）。
  ★ `--appendix` 不给 ⇒ `CD4` 判 `N/A`（与 `mcm-data` 的 `DA2 --refs` 同型）。

## 六条判据（设计 §4.2；**依据标注**见约定件 §6）

* `CD1` 求解入口固定随机源：MATLAB `rng(` / Python `default_rng`|`seed`。`[社区]`
  ★ **机械判法（per-file 启发式）**：逐个代码文件看 —— **凡用到随机性的文件，必须同处有固定随机源惯用法**；
  用了随机（MATLAB `rand`/`randn`/`randi`/`randperm`；Python `random` / `default_rng`）却找不到固定随机源 ⇒ 红。
  **完全不含随机性的文件不判**（确定性模型没有"随机源"可固定 ⇒ 不强制）。
* `CD2` 结果落盘（`save`|`writetable` / `to_csv`|`np.save`|`savefig` …），且**不只有** `disp`|`print`。`[社区]`
  ★ **机械判法**：逐个代码文件 —— 有打印（`disp`/`fprintf`/`print`）**却无任何落盘惯用法** ⇒ 该文件"只打印"⇒ 红；
  另：整个代码集**无一处落盘惯用法** ⇒ 红（空集不许判绿）。
* `CD3` 结果文件名带论文编号，与正文 图 X / 表 Y / 式 Z 对得上。`[社区]`
  ★ **机械判法（与 `references/numbering.md` 一致）**：结果清单每行 —— 从 `结果文件` 文件名里抽出
  `(类型, 编号)`（`figure-1-*` / `table-2-*` / `eq-3-*`），与 `对应正文编号` 列的 `(类型, 编号)` 必须**相等**
  （类型一致 **且** 编号一致）。**这是"文件名 ↔ 清单编号"的对应检查，不查文件是否真的存在于盘上。**
* `CD4` 论文附录里**不含程序正文**。`[官方]` `corpus/official/instructions.html:1227` 与
  `corpus/official/instructions.html:1305`（★ 按 `GC7` 禁简写：两个锚都写全路径）。
  ★ **机械判法（启发式 · 两层强信号）**：给了 `--appendix` 时 ——
  ① **无歧义信号**（代码块标记 `\\begin{verbatim}` / `\\begin{lstlisting}` / `\\begin{minted}` / Markdown
  围栏 ```；或代码专属语法 `#include <` / `from X import Y` / `import X as Y`）⇒ **单命中即判**；
  ② **定义行**（`function ` / `def ` / `class ` / 整行 `import X`）⇒ **须有代码体佐证**才判
  （定义行不以句尾标点收束 ∧ 其紧邻窗口内出现代码语句）。**不给 `--appendix` ⇒ 判 `N/A`**
  （与 `mcm-data` 的 `DA2 --refs` 同型）。
  ★ **假阳性面**（详见"已知边界"）：本判据是启发式；**以 `class 词:` / `function 词(` 起首的散文行**
  仍有可能被误判为程序正文 —— **命中时请人工确认再改**（不许说"已消除"）。
* `CD5` **可执行语句内**没有写死的机器绝对路径（`C:\\` / `D:\\` / `/Users/`）；**注释内不算**。`[社区]`
  ★ **机械判法（启发式）**：逐行先**剥掉注释**（MATLAB `%`、Python `#`，均按引号态判定）**再**找路径字面量
  `[A-Za-z]:[\\/]` 或 `/Users/`；注释里的路径**不判**（`P5` 的假阳性面）。
* `CD6` **结果清单在场，五列每行非空，且凡 `代码来自=AI` 的行有「跑过人 + 日期 + 已核」**。`[社区]`
  （理由见约定件 §6.1：判据规则本身是本套件自订，**不许写成官方**）。`P6` 的核心。
  ★ `代码来自` 比对前先**规范化**：去首尾空白 + 去反引号 + 大小写不敏感 + **允许 `AI` 前缀**
  （`ai` / `AI写` / `AI 生成` 都算 **AI 行**；否则写成变体会**假绿**）。
  ★ 判"清单列齐"时**一并判 `代码来自` 的取值域**：规范化后**只许** `本人` / `AI` —— 出现第三种取值 ⇒ 红
  （**fail-closed**，不静默放过）。

## `N/A` 与空集的【三分口径 + 第四态】（约定件 §5 · `GC5`/`GC6`/`P7`）—— 分开实现

| 情形 | 触发 | 判 |
| :--- | :--- | :--- |
| A 目标物**不存在** | 代码目录 / 结果清单文件 `<代码目录>/result-manifest.md` / `--appendix` 论文文件不在 | `N/A`（不计入失败） |
| B **节不在** | 结果清单文件在，但 `## 结果清单` 不在 | `N/A` |
| C **节 / 目录在场但零行 / 零文件** | `## 结果清单` 在但表体零数据行；或代码目录在但零代码文件 | `FAIL`（**空集不许判绿**） |
| D **节在、但表头与契约不符** | `## 结果清单` 在，但其下五列表头与 §1.2 逐字不符 | `FAIL`（**第四态** · fail-closed） |

★ 一旦清单表在场（有数据行），**列内取值缺失即判红**，不再走 `N/A`（约定件 §5.1）。

## ★ 模板守卫（`P7` / Task 3 的硬口径，本检查器同族照做）

`--scope artifact` 的**目标目录若落在 `.claude/skills/mcm-code/assets/` 下 ⇒ 直接 `FAIL`**，
打印「那是模板，不是用户产物」。理由：`assets/result-manifest.md` **自己就是空表**、
`assets/scaffold.m` / `assets/scaffold.py` 是**骨架模板**；若被当成合法靶子，会与
「**节在但零行 ⇒ FAIL**」串成一个**自相矛盾的假红/假绿**。★ T4 同族实现了此守卫（见 `TEMPLATE`）。

## 已知边界（**不声称穷尽** · 设计 §4.4）

* **查不到"结果算得对不对"** —— 只查工程规范（可复现 / 落盘 / 编号对齐）是否落地。
* `CD1` / `CD2` 是 **per-file 启发式**：`CD1` 只认常见随机源花名（MATLAB `rand` 族 / Python `random` / `default_rng`），
  **接收外部注入 `rng` 对象的库文件**会被判"用了随机未固定"（**假红可能**）；**完全不含随机性的文件不判**。
  `CD2` 只认常见落盘花名（见 `_SAVE_*`）；用**未列举**的落盘方式会**假红**，用**未列举**的打印方式会**漏判**。
* `CD3` 只判"文件名编号 ↔ 清单 `对应正文编号`"的**对应**；**不查文件是否真的落盘**、**不读正文散文**核对图号。
* `CD4` 是**启发式**（两层强信号：① 代码块标记 / 代码专属语法 ⇒ 单命中即判；② 定义行须有代码体佐证）。
  - **漏判面**：**纯文字描述的伪代码**、**被转义 / 包在自定义环境里的源码**、或**孤立一行、无代码体佐证的定义行**可能漏判。
  - **假阳性面**：**以 `class 词:` / `function 词(` 起首的散文行**仍有可能被误判为程序正文 ——
    **本判据护的是"程序不得随解答提交"这条官方禁令，误判会叫人删合法散文** ⇒ **命中时请人工确认再改**。
* `CODE_EXTS` 只含 `.m` / `.py`：本支语言限在 **MATLAB / Python**（设计 §0.3）；
  **用户代码目录若全是其它语言（如 `.R` / `.jl`），会判"代码目录在场但零代码文件"**（`CD1`/`CD2`/`CD5` 红）
  —— 属**既定取舍**，**非承诺覆盖全语言**。
* `CD5` 的"绝对路径"是**启发式**（`[A-Za-z]:[\\/]` 与 `/Users/`）；**匹配到不一定是违规，没匹配到也不保证没有别的形态**
  （设计 §4.4 承认的假阳性面）。`CD5` 的**注释剥离**按引号态判定，**字符串里的 `%` / `#` 不被当注释**。
* `CD6` 的 `代码来自` 规范化是**前缀式**：归一后凡以 `AI` 起首即算 AI 行；同时判 `代码来自` **只许** `本人` / `AI`。
* `--scope self` 的 `SELF2` **只盘检 skill 目录内的 `*.md`**（`references/` · `assets/` · `SKILL.md`）；
  **`assets/scaffold.m` / `assets/scaffold.py` 不进射程**（只扫 `*.md`，与 `check-data.py` 同族）；
  `corpus/` 起始的指针**不在射程内**。

★ 末行恒为 `RESULT: …`；退出码 **0 / 1**（判红 = 1；用法错 = 2）。每条判词一行，形态 `PASS|FAIL|N/A  <id>  <读数>`。
"""

import argparse
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]                 # …/mcm-code/check-code.py → 仓根
SKILL_DIR = ROOT / ".claude/skills/mcm-code"                       # 默认 skill 根（`--skill-dir` 可改）
ASSETS = SKILL_DIR / "assets"                                      # 模板守卫的默认判据面

# ---- 逐字契约（约定件 §1.2；与设计 §3.2 一致）-----------------------------
HEADER_LINE = "| 结果文件 | 对应正文编号 | 生成脚本 | 代码来自 | 确认 |"
HEADER_COLS = ["结果文件", "对应正文编号", "生成脚本", "代码来自", "确认"]

# 结果清单的节名（约定件 §2.2 / §2.3）
MANIFEST_SECTION = "结果清单"
MANIFEST_NAME = "result-manifest.md"

# 边界两句（约定件 §4.1 / §4.3；比对前先剥 `**` / 反引号 —— 见文件头 `SELF1`）
GEN_BOUNDARY = "本 skill 给出数据来源与代码规范；最终判断与结论由队员负责。"
CODE_BOUNDARY = "凡由 AI 写的代码，队员必须自己跑通并核对结果后方可采信"

# 全仓唯一的判据名册（约定件 §3）；`--scope artifact` **逐条**据此出判词
CRITERIA = ("CD1", "CD2", "CD3", "CD4", "CD5", "CD6")

# 代码文件扩展名（两套语言：MATLAB / Python —— 设计 §0.3）
CODE_EXTS = (".m", ".py")

# ---- `CD1` 固定随机源 / 随机性使用（启发式）-------------------------------
_SEED_M = re.compile(r"\brng\s*\(")                                 # MATLAB rng(...)
_SEED_PY = re.compile(r"default_rng|\bseed\s*\(")                    # default_rng / *.seed(
_RAND_M = re.compile(r"\b(?:randn|randi|randperm|rand)\b")           # MATLAB 随机性使用
_RAND_PY = re.compile(r"\brandom\b|default_rng")                     # Python 随机性使用

# ---- `CD2` 落盘 / 纯打印（启发式）----------------------------------------
_SAVE_M = re.compile(
    r"\b(?:save|writetable|writematrix|writetimetable|writecell|exportgraphics|imwrite|print)\s*\(")
_PRINT_M = re.compile(r"\b(?:disp|fprintf)\s*\(")
_SAVE_PY = re.compile(
    r"\.(?:to_csv|to_excel|to_parquet|to_json|to_pickle|savefig|savetxt|savez|save|write_text|write)\s*\("
    r"|(?:numpy|np)\.save\b|json\.dump\s*\(")
_PRINT_PY = re.compile(r"\bprint\s*\(")

# ---- `CD5` 绝对路径（启发式）---------------------------------------------
_ABS_PATH = re.compile(r"[A-Za-z]:[\\/]|/Users/")

# ---- `CD4` 程序正文特征（启发式 · 两层强信号）-----------------------------
# ★ **收窄以压住散文假阳性**（复核 Important）：只认下列两类强信号。
#   ① **无歧义信号**（代码块标记 / 代码专属语法）—— 单命中即判：
#      LaTeX 代码环境（`\begin{verbatim|lstlisting|minted}`）/ Markdown 围栏 ``` /
#      `#include <` / `from X import Y` / `import X as Y`。
#   ② **定义行**（`function` / `def` / `class` / 整行 `import X`）—— **须有代码体佐证**才判：
#      定义行本身**不以句尾标点（`.!?`）收束**，且其**紧邻窗口内须出现代码语句**
#      （非注释、非句尾、带 `;` / 控制关键字 / 代码运算符）。散文里
#      `Class imbalance: …` / `function g(y) denotes …` 因句尾句号、或后继是散文 ⇒ **不再误判**。
_APPENDIX_BLOCK_RE = re.compile(
    r"\\begin\{(?:verbatim|lstlisting|minted)\}"
    r"|^\s*```"
    r"|^\s*#include\s*<"
    r"|^\s*from\s+[\w.]+\s+import\s+\w+"
    r"|^\s*import\s+[A-Za-z_][\w.]*\s+as\s+\w+\s*$",
    re.IGNORECASE)

# 定义行（**须代码体佐证**才算程序正文）
_APPENDIX_DEF_RE = re.compile(
    r"^\s*(?:function\s+\w+|def\s+\w+\s*\(|class\s+\w+\s*[:(]|import\s+[A-Za-z_][\w.]*\s*$)",
    re.IGNORECASE)

_SENTENCE_END_RE = re.compile(r"[.!?]\s*$")          # 散文句尾 ⇒ 该行按散文看
_DEF_BODY_WINDOW = 3                                 # 定义行向后看几条非空行找代码体

# ---- `CD3` 编号解析 -------------------------------------------------------
_KIND_CN = {"图": "figure", "表": "table", "式": "eq"}
_BODY_REF_RE = re.compile(r"(图|表|式)\s*[（(]?\s*(\d+)\s*[)）]?")
_FNAME_KINDS = (
    ("figure", re.compile(r"(?:figure|fig|图)[-_]?(\d+)", re.IGNORECASE)),
    ("table", re.compile(r"(?:table|表)[-_]?(\d+)", re.IGNORECASE)),
    ("eq", re.compile(r"(?:equation|eq|式)[-_]?(\d+)", re.IGNORECASE)),
)

# 日期串（`CD6` 判"记了日期"用）：YYYY-MM-DD / YYYY/M/D / YYYY年M月D日
_DATE_RE = re.compile(r"(\d{4}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2})")

_HEAD2_RE = re.compile(r"^#{2}\s+(.+?)\s*$")          # 恰好 level-2 标题
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


def _pad(row, n):
    return (list(row) + [""] * n)[:n]


def _clean(cell):
    """清单单元格取值归一：去空白 + 去反引号。"""
    return cell.strip().strip("`").strip()


# ---------------------------------------------------------------- 注释剥离（`CD5`）
def _strip_comment(line, ext):
    """剥掉一行里的注释：MATLAB `%` / Python `#`。

    ★ **按引号态判定** —— 字符串里的 `%` / `#` **不算注释**（否则会把字符串内容当注释剥掉 ⇒ 漏判）。
    MATLAB 字符串用 `'`（连续两个 `''` 表示一个撇号）；Python 用 `'` / `"`（`\\` 转义）。
    """
    out = []
    i, n = 0, len(line)
    if ext == ".m":
        inq = False
        while i < n:
            c = line[i]
            if inq:
                out.append(c)
                if c == "'":
                    if i + 1 < n and line[i + 1] == "'":
                        out.append("'")
                        i += 2
                        continue
                    inq = False
                i += 1
                continue
            if c == "'":
                inq = True
                out.append(c)
                i += 1
                continue
            if c == "%":
                break
            out.append(c)
            i += 1
        return "".join(out)
    # Python
    q = None
    while i < n:
        c = line[i]
        if q:
            out.append(c)
            if c == "\\":
                if i + 1 < n:
                    out.append(line[i + 1])
                    i += 2
                    continue
            elif c == q:
                q = None
            i += 1
            continue
        if c in ("'", '"'):
            q = c
            out.append(c)
            i += 1
            continue
        if c == "#":
            break
        out.append(c)
        i += 1
    return "".join(out)


# ---------------------------------------------------------------- 规范化 / 判值
def _norm_author(v):
    """规范化 `代码来自`：去首尾空白 + 去反引号 + 大小写不敏感 + **允许 `AI` 前缀**。

    返回归一后的取值 `"本人"` / `"AI"`；**第三种取值（含空）⇒ `None`**（`CD6` 据此判红，fail-closed）。
    例：`ai` / `AI写` / `AI 生成` / ` AI ` 一律归 `"AI"`；`本人` 归 `"本人"`。
    """
    v = v.strip().strip("`").strip()
    if not v:
        return None
    if v.upper().startswith("AI"):
        return "AI"
    if v == "本人":
        return "本人"
    return None


def _confirm_ok(v):
    """`确认` 列：含「已核」且记跑过人 + 日期。返回 `(bool, 原因)`。"""
    v = v.strip().strip("`").strip()
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
        return False, "未记跑过人"
    return True, ""


def _parse_body_ref(cell):
    """`对应正文编号` 单元格 ⇒ `(类型, 编号)`；认 `图 X` / `表 Y` / `式 Z`（可带半角/全角括号）。"""
    m = _BODY_REF_RE.search(_clean(cell))
    if not m:
        return None
    return (_KIND_CN[m.group(1)], int(m.group(2)))


def _is_code_stmt(line):
    """一行是否像**代码语句**（`CD4` 判"定义行有无代码体佐证"用）。

    判据：非空、非纯注释行、**不以句尾标点收束**，且满足其一 —— 以 `;` 收束 /
    以代码控制关键字起首 / 含代码运算符（`= ( ) [ ] { }`）。
    散文句（如 `function g(y) denotes the marginal cost in the model.`）因句尾句号 ⇒ 判否。
    """
    s = line.strip()
    if not s:
        return False
    if s.startswith("%") or s.startswith("#"):
        return False
    if _SENTENCE_END_RE.search(s):
        return False
    if s.endswith(";"):
        return True
    if re.match(r"(?:end|return|break|continue|pass|else|elif|except|finally|try|with|"
                r"if|for|while|switch|case|otherwise|do|then|import|from|function|def|class)"
                r"\b", s):
        return True
    return bool(re.search(r"[=()\[\]{}]", s))


def _has_code_body(lines, idx):
    """定义行（0-based `idx`）之后**紧邻窗口**内是否出现代码语句（定义行的佐证）。"""
    seen = 0
    for j in range(idx + 1, len(lines)):
        if not lines[j].strip():
            continue
        if _is_code_stmt(lines[j]):
            return True
        seen += 1
        if seen >= _DEF_BODY_WINDOW:
            break
    return False


def _parse_filename_ref(name):
    """结果文件名 ⇒ `(类型, 编号)`（`figure-1-*` / `table-2-*` / `eq-3-*`；也认中文名）。"""
    cands = []
    for kind, rx in _FNAME_KINDS:
        m = rx.search(name)
        if m:
            cands.append((m.start(), kind, int(m.group(1))))
    if not cands:
        return None
    cands.sort()
    return (cands[0][1], cands[0][2])


# ---------------------------------------------------------------- `--scope artifact` 状态
class State(object):
    def __init__(self, target, appendix):
        self.dir = pathlib.Path(target)
        self.appendix = pathlib.Path(appendix) if appendix else None
        self.dir_missing = not self.dir.exists()
        self.dir_ok = self.dir.is_dir()

        # ---- 代码文件（目录在场时收集）----
        self.code_texts = []            # [(Path, text), ...]（读不出的跳过）
        if self.dir_ok:
            for p in sorted(self.dir.rglob("*")):
                if p.is_file() and p.suffix.lower() in CODE_EXTS:
                    t = read_text(p)
                    if t is not None:
                        self.code_texts.append((p, t))

        # ---- 结果清单（`<代码目录>/result-manifest.md`）----
        self.manifest = self.dir / MANIFEST_NAME
        self.manifest_missing = self.dir_missing or not self.manifest.exists()
        self.manifest_unreadable = False
        self.mf_body = None
        self.mf_header = None
        self.mf_rows = []
        self.mf_colmap = {}

        if not self.manifest_missing and self.manifest.is_file():
            text = read_text(self.manifest)
            if text is None:
                self.manifest_unreadable = True
            else:
                self.mf_body = _section_body(text, MANIFEST_SECTION)
                if self.mf_body is not None:
                    table = _first_table(self.mf_body)
                    if table:
                        header = _cells(table[0])
                        if header == HEADER_COLS:
                            self.mf_header = header
                            self.mf_colmap = {c: i for i, c in enumerate(header)}
                            body_rows = table[1:]
                            if body_rows and _is_sep(_cells(body_rows[0])):
                                body_rows = body_rows[1:]
                            self.mf_rows = [_pad(_cells(r), len(HEADER_COLS)) for r in body_rows]

    # ---- 三情形 / 第四态的公共前置 ----
    def code_pre(self):
        """代码文件类判据（`CD1` / `CD2` / `CD5`）的共同出口。"""
        if self.dir_missing:
            return "N/A", "目标代码目录不存在（情形 A）"
        if not self.dir_ok:
            return "FAIL", "目标路径不是目录（fail-closed）"
        if not self.code_texts:
            return "FAIL", "代码目录在场但零代码文件（情形 C · 空集不许判绿）"
        return None

    def mf_pre(self):
        """结果清单类判据（`CD3` / `CD6`）的共同出口。"""
        if self.dir_missing:
            return "N/A", "目标代码目录不存在 ⇒ 无结果清单（情形 A）"
        if self.manifest_missing:
            return "N/A", "结果清单文件 `<代码目录>/%s` 不存在（情形 A）" % MANIFEST_NAME
        if self.manifest_unreadable:
            return "FAIL", "结果清单文件读不出（fail-closed）"
        if self.mf_body is None:
            return "N/A", "节 `## %s` 不在本文件（情形 B）" % MANIFEST_SECTION
        if self.mf_header is None:
            return "FAIL", "`## %s` 下无五列表 / 表头与 §1.2 不符（第四态 · fail-closed）" % MANIFEST_SECTION
        if not self.mf_rows:
            return "FAIL", "节 `## %s` 在但零数据行（情形 C · 空集不许判绿）" % MANIFEST_SECTION
        return None


# ---------------------------------------------------------------- CD1
def cd1(st):
    r = st.code_pre()
    if r:
        return r
    bad = []
    for p, t in st.code_texts:
        ext = p.suffix.lower()
        if ext == ".m":
            uses, seed = _RAND_M.search(t), _SEED_M.search(t)
        else:
            uses, seed = _RAND_PY.search(t), _SEED_PY.search(t)
        if uses and not seed:
            bad.append(p.name)
    detail = "势=%d（代码文件）· 用随机未固定 %d 个" % (len(st.code_texts), len(bad))
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- CD2
def cd2(st):
    r = st.code_pre()
    if r:
        return r
    offenders = []          # 只打印不落盘的文件
    any_save = False
    for p, t in st.code_texts:
        ext = p.suffix.lower()
        if ext == ".m":
            save, prnt = _SAVE_M.search(t), _PRINT_M.search(t)
        else:
            save, prnt = _SAVE_PY.search(t), _PRINT_PY.search(t)
        if save:
            any_save = True
        elif prnt:
            offenders.append(p.name)
    bad = []
    if offenders:
        bad.append("只打印未落盘：" + "/".join(offenders[:6]) + (" …" if len(offenders) > 6 else ""))
    if not any_save:
        bad.append("整个代码集无任何落盘惯用法（空集不许判绿）")
    detail = "势=%d（代码文件）· 落盘惯用法 %s · 问题 %d 处" % (
        len(st.code_texts), "有" if any_save else "无", len(bad))
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- CD3
def cd3(st):
    r = st.mf_pre()
    if r:
        return r
    bad = []
    i_f, i_b = st.mf_colmap["结果文件"], st.mf_colmap["对应正文编号"]
    for i, row in enumerate(st.mf_rows, 1):
        fname = _clean(row[i_f])
        fref = _parse_filename_ref(fname)
        bref = _parse_body_ref(row[i_b])
        if fref is None:
            bad.append("第%d行 文件名「%s」不带编号" % (i, fname))
        elif bref is None:
            bad.append("第%d行 对应正文编号「%s」不含 图/表/式 编号" % (i, _clean(row[i_b])))
        elif fref != bref:
            bad.append("第%d行 文件名 %s-%d 与正文 %s-%d 对不上"
                       % (i, fref[0], fref[1], bref[0], bref[1]))
    detail = "势=%d（清单行）· 编号对不上/缺编号 %d 处" % (len(st.mf_rows), len(bad))
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- CD4
def cd4(st):
    if st.appendix is None:
        return "N/A", "未给 `--appendix` ⇒ 无附录靶子（约定件 §8；与 `mcm-data` 的 `DA2 --refs` 同型）"
    if not st.appendix.exists():
        return "N/A", "论文文件（`--appendix`）不存在 ⇒ 无附录靶子（情形 A）"
    text = read_text(st.appendix)
    if text is None:
        return "FAIL", "论文文件（`--appendix`）读不出（fail-closed）"
    lines = text.splitlines()
    hits = []
    for i, ln in enumerate(lines, 1):
        m = _APPENDIX_BLOCK_RE.search(ln)               # ① 无歧义信号：单命中即判
        if m:
            hits.append("第%d行「%s」" % (i, m.group(0).strip()))
            continue
        if (_APPENDIX_DEF_RE.match(ln)                 # ② 定义行：须代码体佐证
                and not _SENTENCE_END_RE.search(ln)
                and _has_code_body(lines, i - 1)):
            hits.append("第%d行「%s」" % (i, ln.strip()))
    detail = "势=%d（附录行）· 程序正文命中 %d 处" % (len(lines), len(hits))
    if hits:
        detail += "  <<< " + " ; ".join(hits[:6]) + (" …" if len(hits) > 6 else "")
    return ("PASS" if not hits else "FAIL"), detail


# ---------------------------------------------------------------- CD5
def cd5(st):
    r = st.code_pre()
    if r:
        return r
    hits = []
    for p, t in st.code_texts:
        ext = p.suffix.lower()
        for i, ln in enumerate(t.splitlines(), 1):
            m = _ABS_PATH.search(_strip_comment(ln, ext))
            if m:
                hits.append("%s:%d「%s」" % (p.name, i, m.group(0)))
    detail = "势=%d（代码文件）· 可执行语句内绝对路径 %d 处（注释内不算）" % (len(st.code_texts), len(hits))
    if hits:
        detail += "  <<< " + " ; ".join(hits[:6]) + (" …" if len(hits) > 6 else "")
    return ("PASS" if not hits else "FAIL"), detail


# ---------------------------------------------------------------- CD6
def cd6(st):
    r = st.mf_pre()
    if r:
        return r
    i_author, i_confirm = st.mf_colmap["代码来自"], st.mf_colmap["确认"]
    empty = []
    for i, row in enumerate(st.mf_rows, 1):
        for col in HEADER_COLS:
            if not _clean(row[st.mf_colmap[col]]):
                empty.append("第%d行 `%s` 空" % (i, col))
    ai = []
    for i, row in enumerate(st.mf_rows, 1):
        raw = row[i_author]
        if _norm_author(raw) == "AI":
            ai.append((i, row))
        elif raw and _norm_author(raw) is None:
            empty.append("第%d行 `代码来自`「%s」非法（只许 `本人` / `AI`）" % (i, _clean(raw)))
    bad = []
    for i, row in ai:
        ok, why = _confirm_ok(row[i_confirm])
        if not ok:
            bad.append("第%d行；%s" % (i, why))
    detail = ("势=%d（清单行）· 五列有空/取值非法 %d 处 · `代码来自=AI` 的行 %d，未确认 %d 处"
              % (len(st.mf_rows), len(empty), len(ai), len(bad)))
    if not ai:
        detail += "  ★ 0 条 AI 行 ⇒ 确认闸无从判（若清单本应有 AI 行，请先查 `代码来自` 列）"
    issues = empty + bad
    if issues:
        detail += "  <<< " + " ; ".join(issues[:6]) + (" …" if len(issues) > 6 else "")
    return ("PASS" if not issues else "FAIL"), detail


ARTIFACT_FUNCS = {"CD1": cd1, "CD2": cd2, "CD3": cd3, "CD4": cd4, "CD5": cd5, "CD6": cd6}


# ---------------------------------------------------------------- `--scope self`
def self1(skill_dir):
    """`mcm-code/SKILL.md` 的边界**两句在场**（比对前剥 `**` / 反引号）。"""
    text = read_text(skill_dir / "SKILL.md")
    if text is None:
        return "FAIL", "`SKILL.md` 读不出 ⇒ 无可检对象（fail-closed）"
    norm = _norm(text)
    miss = [s for s in (GEN_BOUNDARY, CODE_BOUNDARY) if _norm(s) not in norm]
    detail = "势=2（边界句）· 缺 %d 句" % len(miss)
    if miss:
        detail += "  <<< " + " ; ".join("「%s」" % m for m in miss)
    return ("PASS" if not miss else "FAIL"), detail


def self2(skill_dir):
    """`references/` 的内部指针不悬空（盘检 skill 目录内的 `references/` · `assets/` · `SKILL.md`）。"""
    scan = []
    skill_md = skill_dir / "SKILL.md"
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
    """`assets/result-manifest.md` 的表头与约定件 §1.2 **逐字一致**（五列 + 五格分隔行）。"""
    text = read_text(skill_dir / "assets" / MANIFEST_NAME)
    if text is None:
        return "FAIL", "`assets/%s` 读不出（fail-closed）" % MANIFEST_NAME
    body = _section_body(text, MANIFEST_SECTION)
    if body is None:
        return "FAIL", "模板缺 `## %s` 节" % MANIFEST_SECTION
    table = _first_table(body)
    if not table:
        return "FAIL", "模板 `## %s` 下无表" % MANIFEST_SECTION
    bad = []
    if table[0].strip() != HEADER_LINE:
        bad.append("表头与 §1.2 逐字不符：%s" % table[0].strip())
    if len(table) < 2 or not _is_sep(_cells(table[1])) or len(_cells(table[1])) != len(HEADER_COLS):
        bad.append("分隔行缺失或非五格")
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
        description="`mcm-code` 机械层判据：外检 `CD1`–`CD6` + 内检（交付件自洽）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "两个 `--scope`（取值写死 · 约定件 §8）：\n"
            "  self                      内检：本仓交付件自洽（SELF1 边界两句 / SELF2 指针不悬空 /\n"
            "                            SELF3 模板表头逐字）。无目标参数。进收工门。\n"
            "  artifact <代码目录>       外检：用户赛期真实代码目录。\n"
            "                            ★ 结果清单文件 = `<代码目录>/result-manifest.md`。\n"
            "                            ★ `N/A` 出口是前提（约定件 §5）。\n"
            "可选：--appendix <论文文件> 给了 ⇒ `CD4` 判「论文附录里不含程序正文」；\n"
            "                            不给 ⇒ `CD4` 判 `N/A`（与 `mcm-data` 的 `CD4`↔`DA2 --refs` 同型）。\n"
            "\n"
            "示例:\n"
            "  python .claude/skills/mcm-code/check-code.py --scope self\n"
            "  python .claude/skills/mcm-code/check-code.py --scope artifact my-code --appendix paper.md\n"))
    ap.add_argument("--scope", required=True, choices=["self", "artifact"],
                    help="self = 内检（本仓交付件自洽，无目标）· artifact = 外检（用户赛期真实代码目录）")
    ap.add_argument("target", nargs="?", default=None,
                    help="--scope artifact 时的代码目录路径（--scope self 时不用给）")
    ap.add_argument("--appendix", default=None,
                    help="--scope artifact 时的论文文件（给了才判 CD4；不给 ⇒ CD4 = N/A）")
    ap.add_argument("--skill-dir", dest="skill_dir", default=None,
                    help="skill 根（默认仓内 `.claude/skills/mcm-code`；变异探针可指到副本，"
                         "只影响 `--scope self`）")
    a = ap.parse_args(argv)

    if a.scope == "self":
        if a.target is not None:
            print("用法错：`--scope self` 不吃目标参数（约定件 §8）。", file=sys.stderr)
            return 2
        skill_dir = pathlib.Path(a.skill_dir) if a.skill_dir else SKILL_DIR
        print("check-code.py · scope=self")
        print("skill-dir = %s" % skill_dir)
        rows = [(rid, fn(skill_dir)) for rid, fn in SELF_FUNCS]
        return _print_rows(rows)

    # ---- scope == artifact ----
    if a.target is None:
        print("用法错：`--scope artifact` 必须给一个代码目录路径（约定件 §8）。", file=sys.stderr)
        return 2

    target = pathlib.Path(a.target).resolve()
    assets = ASSETS.resolve()
    print("check-code.py · scope=artifact")
    print("target   = %s" % target)
    if a.appendix:
        print("appendix = %s" % pathlib.Path(a.appendix))

    # ★ 模板守卫：目标落在 assets/ 下 ⇒ 直接 FAIL（那是模板，不是用户产物）
    try:
        under_assets = os.path.commonpath([str(target), str(assets)]) == str(assets)
    except ValueError:                       # 不同盘符等
        under_assets = False
    if under_assets:
        print("FAIL  TEMPLATE  目标落在 `.claude/skills/mcm-code/assets/` 下 —— "
              "那是模板，不是用户产物（模板清单零数据行 / 脚手架是骨架，不可当靶子）。")
        print("-" * 78)
        print("判据 1 条 · 红 1 条 · N/A 0 条")
        print("RESULT: FAIL（TEMPLATE）")
        return 1

    st = State(a.target, a.appendix)
    rows = [(rid, ARTIFACT_FUNCS[rid](st)) for rid in CRITERIA]
    return _print_rows(rows)


if __name__ == "__main__":
    sys.exit(main())
