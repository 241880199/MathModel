#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-section.py —— MCM/ICM 逐节写作自检（`mcm-section-writer` skill 随附）

用途
----
对**一份节文本**（`.tex` 或 `.md`）跑一组检查，逐条报告 `PASS` / `WARN` / `FAIL` / `SKIP`：

  SW1  数字与出处成对（硬失败 · 出处 `judge.md:222-225`）
  SW2  无出处数字须带标注（硬失败 · 出处 `judge.md:224`；★ 只在"有具名外源"时判死）
  SW3  段末总结率（提请复核 · 出处 `judge.md:309`）
  SW4  膨胀比（提请复核 · 读数出 `judge.md:235`；阈值 4.0 = 本项目 `[社区]` 口径）
  SW5  对比式 + 强调式构造密度（提请复核 · 出处 `judge.md:315`）
  SW6  自评式元话语数（提请复核 · 读数出 `judge.md:237`；阈值 2 = 本项目 `[社区]` 口径）
  SW7  极短断言句（提请复核 · 出处 `judge.md:308`）
  SW8  可整体删除而信息量不变的句比（提请复核 · 出处 `judge.md:311`）

★ **硬失败（`FAIL`）只有三处：`SW1`、`SW2`（★ 与 `SW1` 同一合取口径）、`EMPTY`（无正文）**；
  `SW3`–`SW8` **一律只出"提请复核"（`WARN`）**，**绝不判死**。
★ **"检查器 PASS" ≠ "这一节写好了"** —— 它只判形式与可机判的那几项；
  `纪律 A3/A4/A5/B2/B4/B5/B6` 等条目**仍靠人工逐条**（同 `mcm-abstract` 的口径：工具只判形式）。
★ **本工具不判"这段是不是 AI 生成的"**（`judge.md:133` / `:244` / `:240`）。

★ **`SW2` 的硬失败射程与 `SW1` 同一合取口径**（`judge.md:223(d)`）：
  **有具名外源 ∧ 数字搜不到 ∧ 无标注串 ⇒ `FAIL`**（判死）。
  **无具名外源**（一张**自算结果表**的常见形态）∧ 数字搜不到 ∧ 无标注串 ⇒ **只提请复核（`WARN`，退出码 0）**，
  文案点明两条可能原因与各自的补救。**不许把判词该"提请复核"的情形做成"判死"。**

★ **没有可检正文**（**无散文行、无表**）⇒ **`FAIL  EMPTY`**（fail-closed，退出码非 0）——
  **对"什么都没写"判 `PASS` 是恒真型失效**（`SW1`/`SW2` 报"无适用对象"不算数）。
  ★ **触发线**：本节**没有任何"非空 ∧ 非标题 ∧ 非公式（数学行）"的行** **且无表** ——
  ⇒ **"只有公式、没有散文、也没有表"同样触发 `EMPTY`**：那种形态下 `SW1`/`SW2` 无表、
  `SW3`–`SW8` 无可切句 ⇒ **八条判据一条都检不了**，判 `PASS` 就是"判据在什么都没验时报绿"。
  「散文段 `<5` 词不进 `SW3`/`SW7` 统计」是**解析门**（那两条判据的射程），
  **与"本节有没有正文"是两件事** —— **一句 4 词的散文（`We use the following.`）仍算正文**（见 `content_lines()`）。
  ★ **"纯公式行"的判法（判据 = 残留里有没有 ≥1 个字母，中英文均可）**：该行掩掉**块级数学**、
    再抹掉**行内公式**后，**残留里没有一个字母** ⇒ 判公式行（不算正文）。
    ⇒ `$$ E=mc^2 $$.` 的残留只有 `.`（无字母）**仍判公式行**；
    而 `We obtain $T = 18743$ from the fit.` 残留含字母 ⇒ **仍是正文**（不许误伤）。
  ★ **数学环境清单不声称穷尽**：只认工具列出的那些（`equation`/`align`/`alignat`/`flalign`/`gather`/`multline`/
    `eqnarray`/`displaymath`/`math`/`split`/`cases`/`array`，及 `$$…$$` / `\[…\]`）；
    **自定义 / 未列出的环境可能不被识别** ⇒ 那一行可能被当成正文（漏判 `EMPTY`）。
    见 `metrics.md` 与 `README` 的 `EMPTY` 条目"已知局限"。

★ **自订阈值一律标 `[社区]`**：判词只给**读数**、**不含**下面这几条线，是本项目自订
  （先例：`figure-choose/check-house-style.py`、`playbook/check-playbook.py`）——
  `SW4` 的 `4.0×`（`judge.md:235` 只给 1.7 / 3.3 / 2.2）、`SW6` 的 `≥2`（`:237` 只给读数 2 / 3 / 1）、
  `SW1`/`SW2` 的 `0.5`（"过半搜不到"这一档；判词只有"一个都搜不到"）。
  **工具输出里凡自订阈值一律带 `[社区]` 字样**，使用者一眼能看出哪条线不是判词的。

用法
----
    python check-section.py <节文件> --section <节名> [--input <要点清单>]
    python check-section.py --selfcheck        # 只跑两条"关于本工具自己"的静态自检
    python check-section.py --help

- `--section` 的取值 = `references/sections.md` 里那 8 个 `##` 标题的节名（本工具**现场从该文件取**）；
  **给不认识的值 ⇒ fail-closed 红**（不许静默绿、不许猜）。
- `--input` = 写手输入里**要点清单 + 已定稿的图表与结果**（★ **设计 §1 的输入契约**：
  **题面 + 哪一节 + 该节要点清单 + 已定稿的图表与结果** —— 本 CLI 的 `--input` 收其中后两项；
  `--section` 收"哪一节"、节文件本体即"题面下的产物"）；
  `SW1`/`SW2` 要回它搜数字；**缺失时 `SW1`/`SW2` 报"无法判定"（`SKIP`）**，**不许报 `PASS`**。
- 退出码：**有 `FAIL` ⇒ 非 0**；只有 `WARN` / `SKIP` ⇒ 0（`WARN` 会在输出里显眼列出）。

★ `SW1`/`SW2` 里"数字**无出处**"的判法有**两档**（**都只会更严，不是放松**）：
  ① **一个都搜不到** —— 判词原文口径（`judge.md:223(d)`：「数字在输入里一个都搜不到」）；
  ② **过半搜不到** —— 本工具的加固（`[社区]` 本项目口径，阈值 `0.5`）：单个数字**偶合**会把①整条判据架空。
  **实测依据（别凭感觉改）**：`tests/skills/arch-cases/out-S1.md` 那张 WHO 表 10 个数字里，
  只有 `12` 能在 `brief-S1.md` 里被搜到 —— 而它来自清单标题「要点（**12** 条）」，**不是数据**。
  若只按①，这张"编造数据 + 借权威署名"的表会**判绿**（本仓最恨的那种失效）。

★ **`SW4`（膨胀比）的分母与判词不同源** —— 判词的分母是 `true-*` 同内容词数
（实测真值上 `true-S1 = 0.92×`、`true-S2 = 0.46×`），本工具 CLI 只能拿到**写手输入（要点清单）**
⇒ 两数**不同源、不可对齐**（判词的 1.7 / 3.3 / 2.2 与本工具的比值不同量级）；
本工具只给"同一写手输入下横比"的量。★ 阈值 `4.0` 为 `[社区]` 软线，不是达标线。

★ 边界 1（阈值不可复算）—— `SW3`–`SW8` 的阈值**全部出自判词读数**，而两轮的度量脚本**都没落盘**
⇒ **不可重跑、不可复算** ⇒ 一律只出"提请复核"，**绝不判死**；
**不许**读成"达标线"（`judge-green.md:270`：*"0 与 0 之间无法定阈"*）。

★ 边界 2（词表先自测）—— `judge.md:238` 明令：任何词表判据**使用前必须先在 `true-*` 上跑一遍**。
本工具**每次运行**都先拿 `tests/skills/arch-cases/true-S1.md` / `true-S2.md` 跑一遍；
**命中 ⇒ 输出"词表不可用：真值命中 N 处"，把该项降级为"不可判"（`SKIP`）**，**不得**据此判产物有罪。
（真值取不到 ⇒ 同样降级为不可判：**没有自测就不许用词表**。）

★ 边界 3（压力臂）—— 压力臂与自由臂必须分别设阈：**本工具做不到** —— 节片段里没有"压力臂"这个概念。
RED 轮是分臂测的（`out-S2.md` 自由臂 vs `out-S2-p.md` 压力臂），
**本工具放弃的正是 RED 那一半控制手段**。**这是明确局限，不是"已覆盖"。**

★ 边界 4（四项不用）—— 判词明令**不用**的四项判据（清单与理由见 `references/metrics.md` §边界 4）
**一律不出现在本工具里**；工具自带一条盯着自己的静态自检（`SELF1`），源码里出现其中任一项的字面即 `FAIL`。
（本工具源码里连它们的**字面**都不留：那张清单按字元在运行时拼出，见 `_forbidden_tokens()`。）

两条"关于本工具自己"的静态自检（`--selfcheck`；正常运行时也一并跑）
------------------------------------------------------------------
  SELF1  源码里不得出现那四项明令不用的判据（字面即红）。
  SELF2  "压力臂与自由臂必须分别设阈：本工具做不到"这一段**局限文字必须在场**（缺即红）。

判据只从失败方向证明：每条 `SW*` 都由 `tests/skills/section-writer/mutate-section-writer.py` 的变异体证红。
本工具只读输入、不写任何文件；输出中文、机读友好（每行形如 `<STATUS> <ID> <标题>  # <说明>`）。
"""

import argparse
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# 阈值（★ 全是〔判词读数〕软线，不是"达标线"；只驱动 WARN，绝不判死）
# --------------------------------------------------------------------------

SW3_RATIO_WARN = 0.90     # judge.md:309 —— 段末总结率 ≥90% 且段数 ≥6 ⇒ 提请复核
SW3_MIN_PARAS = 6         # judge.md:309
SW4_RATIO_WARN = 4.0      # ★ [社区] 本项目自订阈值（judge.md:235 只给读数 1.7 / 3.3 / 2.2，无 4.0）
                          #   分母与判词不同源，见 metrics.md
SW5_DENSITY_WARN = 3.0    # judge.md:315（§6.3 P8）—— 密度 > 3‰ 且真值基线为 0 ⇒ 提请复核
SW6_COUNT_WARN = 2        # ★ [社区] 本项目自订阈值（judge.md:237 只给读数 2 / 3 / 1，无 2 这条线）
SW7_SHORT_WORDS = 8       # judge.md:308 —— 最短句 < 8 词
SW7_SHORT_LOW = 2         # ★ [社区] 本项目自订阈值：判词 judge.md:308 只给"<8 词且 ≥3 处"，
                          #   "极短断言句"的**下界 2 词**判词未给 ⇒ 本项目自订、**直接参与 SW7 判定**
SW7_SHORT_MIN = 3         # judge.md:308 —— 且全节 ≥ 3 处
SW8_RATIO_WARN = 0.15     # judge.md:311 —— ≥15% 的句子可整体删除而信息量不变 ⇒ 提请复核
SW1_SW2_TRACE_MIN = 0.5   # ★ [社区] 本项目自订阈值："过半搜不到"（判词只有"一个都搜不到"）

# ★ 以下三条是**解析门**（决定"哪些内容进统计"），**不是判据线**（不判谁死谁活）——
#   写成具名常量，免得被当成阈值读（本仓"编辑的涟漪必须与编辑同批处置"）：
PARSE_MIN_PARA_WORDS = 5  # 散文段 <5 词 ⇒ 不进 SW3/SW7 统计（解析门、非判据线）
FLAT_TABLE_MAX_WORDS = 7  # 扁平表体行的词数上界；≥ 该值视作散文、不认表体（解析门、非判据线）
CTX_WINDOW = 600          # 表题 + 表前句的取窗 = 末 600 字符（解析门、非判据线）
TEX_CAP_WINDOW = 300      # .tex `\caption` 的取窗 = caption 起 300 字符（解析门、非判据线）

# --------------------------------------------------------------------------
# 词表（★ 每一个都要先过"真值自测"，见 truth_lexicon_hits()）
# --------------------------------------------------------------------------

# SW5：judge.md:236 的原表，逐字不改
RE_SW5 = re.compile(r"rather than|not merely|not only|not just|precisely|exactly", re.I)
# SW6：judge.md:237 的原表，逐字不改
RE_SW6 = re.compile(r"this section|the purpose of this section|the payoff|"
                    r"is the subject of|worth stating", re.I)
# SW3：段末"判断/评价/格言"的判据线索（只用于**段末句**；不是判词原表，故须自测）
RE_SW3 = re.compile(r"\bis what\b|\bwhat matters\b|\bthe deeper\b|\bunavoidable\b|"
                    r"\bthe key (?:point|insight|idea)\b|\bin effect\b|\bthe lesson\b|"
                    r"\bthis is why\b|\bmatters most\b", re.I)
# SW8：整句"纯元话语/过渡"（可整体删除而信息量不变）——**匹配句首**
RE_SW8 = re.compile(r"^(?:Taken together|We now|We close|It is worth noting|Put differently|"
                    r"In what follows|As noted above|Suffice it to say)\b", re.I)

LEXICONS = (("SW3", RE_SW3), ("SW5", RE_SW5), ("SW6", RE_SW6), ("SW8", RE_SW8))

# SW2：judge.md:224 给的标注串，逐字不改
RE_MARKER = re.compile(r"assum|illustrat|placeholder|to be (?:replaced|supplied)", re.I)
# SW1：具名外部来源（"具名"——机构名 / 具名文献 / 引用标注 / 明说 published）
RE_ATTRIB = re.compile(
    r"World\s+Health\s+Organization|"
    r"\b(?:Organization|Organisation|Institute|Bureau|Agency|Association|Foundation|"
    r"Ministry|Department)\b|"
    r"\bpublished\b|\baccording to\b|\bdata (?:from|by)\b|"
    r"\[\d+\]|\\cite[a-zA-Z]*\{", re.I)
# ★ 缩写必须**大小写敏感**：`re.I` 会让 `\bWHO\b` 命中 "who"（实测栽过：表前句里的
#   "the people who actually use the stair" 被当成世界卫生组织）。
RE_ATTRIB_ACRONYM = re.compile(r"\bWHO\b")


def has_attribution(text):
    m = RE_ATTRIB_ACRONYM.search(text) or RE_ATTRIB.search(text)
    return m.group(0) if m else None

RE_NUM = re.compile(r"\d+(?:\.\d+)?")

# --------------------------------------------------------------------------
# 结构正则
# --------------------------------------------------------------------------

RE_HEADING = re.compile(r"^\s*#{1,6}\s")
RE_TEX_HEADING = re.compile(r"^\s*\\(?:section|subsection|subsubsection|paragraph|chapter)\*?\{")
RE_PIPE_ROW = re.compile(r"^\s*\|.*\|\s*$")
RE_TABLE_CAP = re.compile(r"^\s*\*{0,2}(?:Table|Figure|Fig\.?)\s*\d", re.I)
RE_TEX_CAPTION = re.compile(r"\\caption\s*\{")
RE_TEX_TABLE_BEGIN = re.compile(r"\\begin\{(table|tabular)\*?\}")
RE_TEX_TABLE_END = re.compile(r"\\end\{(table|tabular)\*?\}")
RE_DOLLAR_BLOCK = re.compile(r"\$\$.*?\$\$", re.S)
RE_BRACKET_MATH = re.compile(r"\\\[.*?\\\]", re.S)
# ★ 常见数学环境的清单**不声称穷尽** —— 自定义 / 未列出的环境可能不被识别（见 metrics.md 与 README 的
#   `EMPTY` 条目"已知局限"）。判"纯公式行"时用它对块级数学做掩码（`_mask_block_math`）。
RE_TEX_MATH_ENV = re.compile(
    r"\\begin\{(?:equation|align|alignat|flalign|gather|multline|eqnarray|"
    r"displaymath|math|split|cases|array)\*?\}.*?"
    r"\\end\{(?:equation|align|alignat|flalign|gather|multline|eqnarray|"
    r"displaymath|math|split|cases|array)\*?\}", re.S)
RE_INLINE_MATH = re.compile(r"\$[^$\n]*\$")
RE_ABBR = re.compile(r"\b(?:e\.g|i\.e|vs|Eq|Eqs|Fig|fig|et al|cf|No|Mr|Ms|Dr|Prof|"
                     r"pp|approx|etc|Ref|Sec|Ch|Vol|al)\.", re.I)

VERBATIM_MARK = re.compile(r"^=+\s*BEGIN VERBATIM.*$", re.M)
RE_CJK = re.compile(r"[\u4e00-\u9fff]")
RE_LATIN_WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")
# RE_LETTER: residual still has >=1 letter (Latin or CJK)? Used to judge a pure formula line.
# Digits and punctuation do NOT count, so `$$ E=mc^2 $$.` leaves only `.` => still a formula line.
RE_LETTER = re.compile(r"[A-Za-z\u4e00-\u9fff]")

# --------------------------------------------------------------------------
# "关于本工具自己"的两条静态自检所需的常量
# --------------------------------------------------------------------------

# SELF2：这段局限文字**必须在工具头部（模块 docstring）里在场**。缺即 FAIL。
REQUIRED_DOC_PHRASES = (
    "压力臂与自由臂必须分别设阈",
    "本工具做不到",
    "本工具放弃的正是 RED 那一半控制手段",
)


def _forbidden_tokens():
    """四项明令不用的判据（`judge-green.md:202-208`；清单见 `references/metrics.md` §边界 4）。

    ★ 为什么按字元拼出来：本自检要判"源码里有没有出现它们的**字面**"，
    若这里直接写整词，自检会**命中它自己**。按字元拼 ⇒ 源码里不留下那四个字面。
    """
    j = "".join
    return (
        j(("C", "V")),                                        # ① 句长变异度
        j(("root", "-", "T", "T", "R")),                      # ② 词汇多样性（长名）
        j(("T", "T", "R")),                                   # ② 词汇多样性（短名）
        j(("F", "l", "e", "s", "c", "h")),                    # ③ 可读性指数
        j(("M", "o", "r", "e", "o", "v", "e", "r")),          # ④ 模板化过渡词表
        j(("F", "u", "r", "t", "h", "e", "r", "m", "o", "r", "e")),
        j(("A", "d", "d", "i", "t", "i", "o", "n", "a", "l", "l", "y")),
        j(("In", " ", "conclusion")),
    )


def selfcheck_source(src_text, doc_text):
    """返回 `[(id, ok, detail), ...]` —— 两条"关于本工具自己"的静态自检。"""
    res = []

    # ---- SELF1：四项明令不用的判据不得出现在源码里 --------------------
    hits = []
    for tok in _forbidden_tokens():
        pat = r"(?<![A-Za-z0-9])" + re.escape(tok) + r"(?![A-Za-z0-9])"
        if re.search(pat, src_text, re.I):
            hits.append(tok)
    if hits:
        res.append(("SELF1", False,
                    "源码里出现明令不用的判据共 %d 项（name=已隐去）：%s"
                    % (len(hits), ", ".join("<%d 字元>" % len(h) for h in hits))))
    else:
        res.append(("SELF1", True, "四项明令不用的判据均未出现在源码里"))

    # ---- SELF2：压力臂那一段局限文字必须在场 --------------------------
    doc = doc_text or ""
    missing = [p for p in REQUIRED_DOC_PHRASES if p not in doc]
    if missing:
        res.append(("SELF2", False,
                    "工具头部的『压力臂局限』文字缺失（缺 %d 句，例：%r）"
                    % (len(missing), missing[0][:24])))
    else:
        res.append(("SELF2", True,
                    "工具头部的『压力臂局限』文字在场（%d 句全在）" % len(REQUIRED_DOC_PHRASES)))
    return res


# --------------------------------------------------------------------------
# 文本工具
# --------------------------------------------------------------------------

def read_text(path):
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1(replace)"


def strip_reference_preamble(text):
    """参考件（`true-*.md`）有 `===== BEGIN VERBATIM` 包壳；只分析标记之后的部分。

    同 `judge.md:9` 的口径：说明段不计入"论文措辞"的统计。普通节文件没有该标记 ⇒ 原样返回。
    """
    marks = list(VERBATIM_MARK.finditer(text))
    if not marks:
        return text
    return text[marks[-1].end():]


def clean_math(text):
    t = RE_DOLLAR_BLOCK.sub(" ", text)
    t = RE_BRACKET_MATH.sub(" ", t)
    t = RE_TEX_MATH_ENV.sub(" ", t)
    t = RE_INLINE_MATH.sub(" ", t)
    return t


def count_words(s):
    return len(RE_LATIN_WORD.findall(s)) + len(RE_CJK.findall(s))


def split_sentences(para):
    t = RE_ABBR.sub(lambda m: m.group(0)[:-1] + "\x01", para)
    t = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "\x01" + m.group(2), t)
    parts = re.split(r"(?<=[.!?])\s+", t)
    return [p.replace("\x01", ".").strip() for p in parts if p.strip()]


def is_caption(txt):
    s = txt.strip()
    if not s:
        return False
    if s.startswith("*") and s.endswith("*") and len(s) > 2:
        return True
    return bool(RE_TABLE_CAP.match(s))


def line_of_offset(text, off):
    return text.count("\n", 0, off)


# --------------------------------------------------------------------------
# 表格抽取（`.md` 管道表 / 扁平表 · `.tex` 的 table|tabular 环境）
# --------------------------------------------------------------------------

def _ctx_above(lines, start, end_of_caption):
    """表题 + 表前一句（判词取的口径）。"""
    parts = []
    if end_of_caption is not None:
        parts.append(lines[end_of_caption])
    j = (end_of_caption - 1) if end_of_caption is not None else (start - 1)
    while j >= 0 and not lines[j].strip():
        j -= 1
    prev = []
    while j >= 0 and lines[j].strip() and not RE_PIPE_ROW.match(lines[j]):
        prev.insert(0, lines[j])
        j -= 1
    if prev:
        parts.append(" ".join(prev))
    return " ".join(parts)[-CTX_WINDOW:]


def find_tables(lines):
    """返回 `[{"start","end","ctx"}]`（行号为 0-based，闭区间；`ctx` = 表题 + 表前一句）。"""
    n = len(lines)
    out = []
    covered = set()

    # ① markdown 管道表
    i = 0
    while i < n:
        if RE_PIPE_ROW.match(lines[i]):
            s = i
            while i < n and RE_PIPE_ROW.match(lines[i]):
                i += 1
            e = i - 1
            cap_line = None
            k = s - 1
            while k >= 0 and not lines[k].strip():
                k -= 1
            if k >= 0 and (RE_TABLE_CAP.match(lines[k]) or lines[k].lstrip().startswith("*")):
                cap_line = k
            out.append({"start": (cap_line if cap_line is not None else s),
                        "end": e, "ctx": _ctx_above(lines, s, cap_line)})
            covered.update(range(s, e + 1))
            if cap_line is not None:
                covered.add(cap_line)
        else:
            i += 1

    # ② 表题领起的扁平表（PDF 转换件的常见形态：表题一行 + 其后一块数字）
    for idx, ln in enumerate(lines):
        if idx in covered:
            continue
        if not RE_TABLE_CAP.match(ln):
            continue
        j = idx + 1
        while j < n and not lines[j].strip():
            j += 1
        if j >= n or RE_PIPE_ROW.match(lines[j]):
            continue
        s = j
        # 表题后面紧跟的是散文 ⇒ 这不是表（防 `*Figure 3: …*` 后面那一段正文被当成表体）
        if count_words(lines[s]) >= FLAT_TABLE_MAX_WORDS:
            continue
        while j < n and lines[j].strip() and count_words(lines[j]) < FLAT_TABLE_MAX_WORDS:
            j += 1
        e = j - 1
        if e < s:
            continue
        out.append({"start": idx, "end": e, "ctx": _ctx_above(lines, idx, idx)})
        covered.update(range(idx, e + 1))

    # ③ .tex 的 table 环境（含其中的 tabular）
    tex = "\n".join(lines)
    for m in re.finditer(r"\\begin\{table\*?\}.*?\\end\{table\*?\}", tex, re.S):
        s = line_of_offset(tex, m.start())
        e = line_of_offset(tex, m.end())
        if s in covered:
            continue
        cap = ""
        cm = RE_TEX_CAPTION.search(m.group(0))
        if cm:
            cap = m.group(0)[cm.start():cm.start() + TEX_CAP_WINDOW]
        out.append({"start": s, "end": e,
                    "ctx": (cap + " " + _ctx_above(lines, s, None))[-CTX_WINDOW:]})
        covered.update(range(s, e + 1))

    # ④ .tex 里裸的 tabular（不在 table 环境内）
    for m in re.finditer(r"\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}", tex, re.S):
        s = line_of_offset(tex, m.start())
        if s in covered:
            continue
        e = line_of_offset(tex, m.end())
        out.append({"start": s, "end": e, "ctx": _ctx_above(lines, s, None)})
        covered.update(range(s, e + 1))

    out.sort(key=lambda t: (t["start"], t["end"]))
    return out


def num_in_input(token, input_text):
    """数字 token 是否出现在写手输入里（★ 只认"成词"的出现）。

    必须排除列表序号（`10.`）这类噪声：否则要点清单里的 `1.`…`12.` 会让小数字
    永远"可回溯"，`SW1` 形同虚设。故要求：左右都不是数字/小数点。
    """
    pat = r"(?<![0-9.])" + re.escape(token) + r"(?![0-9.])"
    return re.search(pat, input_text) is not None


def table_numbers(lines, t):
    """表体（表题之后的表格行）里的数字 token 集合。"""
    body = []
    for k in range(t["start"], t["end"] + 1):
        if RE_TABLE_CAP.match(lines[k]) and not RE_PIPE_ROW.match(lines[k]):
            continue          # 表题行不算"表内数字"
        body.append(lines[k])
    return set(RE_NUM.findall("\n".join(body)))


# --------------------------------------------------------------------------
# 正文（散文）切块
# --------------------------------------------------------------------------

def prose_paragraphs(raw, tables):
    tbl_lines = set()
    for t in tables:
        tbl_lines.update(range(t["start"], t["end"] + 1))
    clines = clean_math(raw).split("\n")
    blocks = []
    cur = []
    for i, ln in enumerate(clines):
        head = RE_HEADING.match(ln) or RE_TEX_HEADING.match(ln)
        if i in tbl_lines or not ln.strip() or head:
            if cur:
                blocks.append(cur)
                cur = []
            continue
        cur.append(ln)
    if cur:
        blocks.append(cur)
    paras = []
    for b in blocks:
        txt = " ".join(b).strip()
        if count_words(txt) < PARSE_MIN_PARA_WORDS:    # ★ 解析门、非判据线（见常量区）
            continue
        if is_caption(txt):
            continue
        paras.append(txt)
    return paras


def _mask_block_math(text):
    """把**块级数学**（`$$…$$` / `\\[…\\]` / 数学环境）的每个非换行字元替换成空格（**保留 `\\n`**）。

    ★ 为什么掩码、不直接 `sub` 掉：块级公式**可能跨行**，直接删会打乱行界 / 行号，
      逐行判"这一行是不是纯公式行"就无从谈起。掩码成空格（换行保留）⇒ 行界与原文一一对应。
    """
    chars = list(text)
    for rx in (RE_DOLLAR_BLOCK, RE_BRACKET_MATH, RE_TEX_MATH_ENV):
        for m in rx.finditer(text):
            for i in range(m.start(), m.end()):
                if chars[i] != "\n":
                    chars[i] = " "
    return "".join(chars)


def content_lines(raw_text):
    """本节里"可检对象"的**行**：非空 ∧ 非标题 ∧ **非公式（数学行）**。

    ★ 口径：**只把"非空 ∧ 非标题 ∧ 非公式"的行算作正文** ⇒
      **"只有公式、没有散文、也没有表" ⇒ 无正文 ⇒ `EMPTY` 触发**（fail-closed）：
      那种形态下 `SW1`/`SW2` 无表、`SW3`–`SW8` 无可切句 ⇒ **八条判据一条都检不了**，
      判 `PASS` 就是"判据在什么都没验时报绿"（本仓最恨的恒真型失效）。
    ★ **与 `prose_paragraphs()` 的 `<5` 词下限是两件事**：
      「散文段 `<5` 词不进 `SW3`/`SW7` 统计」是**解析门**（那两条判据的射程）；
      「本节有没有可检正文」看的是**有没有任何一行"非空 ∧ 非标题 ∧ 非纯公式"的行**
      —— **一句 4 词的散文（`We use the following.`）也算正文** ⇒ **不判 `EMPTY`**。
    ★ **"纯公式行"的判法（判据 = 残留里有没有 ≥1 个字母，中英文均可）**：
      该行经 `_mask_block_math` 掩掉**块级数学**（`$$…$$` / `\\[…\\]` / 列出的数学环境）后，
      再经 `RE_INLINE_MATH` 抹掉**行内公式**；若**残留里没有一个字母** ⇒ 判纯公式行、不算正文。
      ⇒ `$$ E=mc^2 $$.` 的残留只有 `.`（无字母）⇒ **仍判公式行**；
      而 `We obtain $T = 18743$ from the fit.` 残留含字母 ⇒ **仍是正文**。
    ★ **环境清单不声称穷尽**：**自定义 / 未列出的环境可能不被识别**（见 `metrics.md` 与 `README` 的
      `EMPTY` 条目"已知局限"）。
    """
    masked = _mask_block_math(raw_text).split("\n")
    out = []
    for i, ln in enumerate(raw_text.split("\n")):
        if not ln.strip():
            continue
        if RE_HEADING.match(ln) or RE_TEX_HEADING.match(ln):
            continue
        # 掩码后（块级公式已变空格）再抹掉行内公式；残留里**没有一个字母（中英文）** ⇒ 这一行是纯公式行，不算正文。
        if not RE_LETTER.search(RE_INLINE_MATH.sub(" ", masked[i])):
            continue
        out.append(ln)
    return out


# --------------------------------------------------------------------------
# 真值自测（边界 2）
# --------------------------------------------------------------------------

def find_truth_dir(start):
    p = start.resolve()
    for cand in [p] + list(p.parents):
        d = cand / "tests" / "skills" / "arch-cases"
        if (d / "true-S1.md").is_file() and (d / "true-S2.md").is_file():
            return d
    return None


def truth_text(truth_dir):
    if truth_dir is None:
        return None
    parts = []
    for nm in ("true-S1.md", "true-S2.md"):
        p = truth_dir / nm
        if not p.is_file():
            return None
        txt, _ = read_text(p)
        parts.append(strip_reference_preamble(txt))
    return "\n".join(parts)


def truth_lexicon_hits(truth):
    """每个词表在真值上的命中数；真值不可用 ⇒ 返回 None（⇒ 全部降级为不可判）。"""
    if truth is None:
        return None
    return {cid: len(rx.findall(truth)) for cid, rx in LEXICONS}


# --------------------------------------------------------------------------
# 八条判据
# --------------------------------------------------------------------------

def judge(text, raw_lines, tables, paras, input_text, lex_hits):
    """返回 `[(id, status, detail), ...]`；status ∈ {PASS, WARN, FAIL, SKIP}。"""
    out = []
    sents = [s for p in paras for s in split_sentences(p)]
    prose = "\n".join(paras)
    prose_words = count_words(prose)

    def lex_ok(cid):
        return lex_hits is not None and lex_hits.get(cid, 1) == 0

    # ---------------- SW1 / SW2 ----------------
    if input_text is None:
        out.append(("SW1", "SKIP", "'无法判定'：--input 缺失，数字无从回写手输入搜"))
        out.append(("SW2", "SKIP", "'无法判定'：--input 缺失，无从判断哪些数字属于『无出处』"))
    elif not tables:
        out.append(("SW1", "PASS", "本节未检出表格 ⇒ 本判据无适用对象"))
        out.append(("SW2", "PASS", "本节未检出表格 ⇒ 本判据无适用对象"))
    else:
        sw1_bad, sw2_bad, sw2_warn = [], [], []
        for t in tables:
            nums = table_numbers(raw_lines, t)
            if not nums:
                continue
            provable = [x for x in sorted(nums) if num_in_input(x, input_text)]
            region = "\n".join(raw_lines[t["start"]:t["end"] + 1])
            attrib = has_attribution(t["ctx"])
            # ★ "数字搜不到"的判法（两档，**都是判据原文的加固、只会更严**）：
            #   ① 一个都搜不到 —— 判词原文口径（`judge.md:223(d)`：「数字一个都搜不到」）；
            #   ② 过半搜不到 —— 本工具的加固（`[社区]` 阈值 `SW1_SW2_TRACE_MIN`）：单个数字**偶合**
            #      （实测 `out-S1.md` 的 WHO 表 10 个数里只有 "12" 与 `brief-S1.md` 的「（12 条）」偶合）
            #      会把①整条判据架空。
            untraceable = (not provable) or (len(provable) / len(nums) < SW1_SW2_TRACE_MIN)
            marker = RE_MARKER.search(region)
            # ★ 判词（`:223(d)`）只有"一个都搜不到"；"过半搜不到"是本工具的**加固**（`[社区]` 阈值）。
            #   输出纪律（工具头 :41）：**凡自订阈值一律带 `[社区]`**，且要**说清是哪一档把这张表判成"搜不到"** ——
            #   否则使用者只看到"只有 %d 个能搜到"这句读数，看不出那条 `0.5` 的线在起作用。
            if not provable:
                trace_note = "（『搜不到』取判词原文口径：数字一个都搜不到）"
            else:
                trace_note = ("（『搜不到』取『过半搜不到』这一档 = [社区] 本项目自订阈值 %.1f；"
                              "判词 :223(d) 只有『一个都搜不到』）" % SW1_SW2_TRACE_MIN)
            if attrib and untraceable:
                # SW1（硬失败）：判词 :223(d) 的**合取** —— "来源名出现 ∧ 数字一个都搜不到"。
                sw1_bad.append(
                    "行%d-%d：表题/表前句含具名外源(%r)，表内 %d 个数字里只有 %d 个能在 --input 里搜到%s"
                    % (t["start"] + 1, t["end"] + 1, attrib, len(nums), len(provable), trace_note))
            if untraceable and not marker:
                if attrib:
                    # SW2（硬失败）：与 SW1 同一合取口径，只在"有具名外源"时判死。
                    sw2_bad.append("行%d-%d：表题/表前句含具名外源(%r)，"
                                   "表内 %d 个数字里只有 %d 个能在 --input 里搜到%s，"
                                   "且该表行号区间里 "
                                   "`assum|illustrat|placeholder|to be (replaced|supplied)` 命中 0"
                                   % (t["start"] + 1, t["end"] + 1, attrib, len(nums), len(provable),
                                      trace_note))
                else:
                    # ★ 无具名外源（一张**自算结果表**的常见形态）⇒ 只提请复核（`WARN`，退出码 0）。
                    sw2_warn.append(
                        "行%d-%d：表内 %d 个数字里只有 %d 个能在 --input 里搜到，"
                        "且该表既无具名外源、也无标注串 ⇒ 只提请复核："
                        "若是**自算结果**，请把定稿结果放进 --input；"
                        "若是**外部数据**，请补来源名或标注 assumed/illustrative"
                        "（[社区] 此档不判死）"
                        % (t["start"] + 1, t["end"] + 1, len(nums), len(provable)))
        out.append(("SW1", "FAIL" if sw1_bad else "PASS",
                    "；".join(sw1_bad) if sw1_bad else
                    "共 %d 张表，均有出处或数字可回溯到 --input" % len(tables)))
        if sw2_bad:
            out.append(("SW2", "FAIL", "；".join(sw2_bad)))
        elif sw2_warn:
            out.append(("SW2", "WARN", "；".join(sw2_warn)))
        else:
            out.append(("SW2", "PASS", "无出处数字均已带显式标注（或无此情形）"))

    # ---------------- SW3 ----------------
    if not lex_ok("SW3"):
        out.append(("SW3", "SKIP", "词表不可用：真值命中 %s 处"
                    % (lex_hits.get("SW3") if lex_hits else "N/A（真值取不到）")))
    elif len(paras) < SW3_MIN_PARAS:
        out.append(("SW3", "PASS", "散文段数 %d < %d ⇒ 本判据不适用"
                    % (len(paras), SW3_MIN_PARAS)))
    else:
        ends = [split_sentences(p)[-1] for p in paras if split_sentences(p)]
        hit = [s for s in ends if RE_SW3.search(s)]
        ratio = len(hit) / len(paras)
        warn = ratio >= SW3_RATIO_WARN
        out.append(("SW3", "WARN" if warn else "PASS",
                    "段末为评价/格言/判断句的段落 %d/%d = %.0f%%（提请复核线 ≥90%% 且段数 ≥6）"
                    % (len(hit), len(paras), ratio * 100)))

    # ---------------- SW4 ----------------
    if input_text is None:
        out.append(("SW4", "SKIP", "'无法判定'：--input 缺失，膨胀比的分母取不到"))
    else:
        iw = count_words(input_text)
        if iw <= 0:
            out.append(("SW4", "SKIP", "'无法判定'：--input 词数为 0"))
        else:
            ratio = prose_words / iw
            out.append(("SW4", "WARN" if ratio > SW4_RATIO_WARN else "PASS",
                        "膨胀比 = 节正文 %d 词 ÷ 写手输入 %d 词 = %.2f×"
                        "（提请复核线 > %.1f× [社区] 本项目自订；★ 分母与判词不同源，见 metrics.md）"
                        % (prose_words, iw, ratio, SW4_RATIO_WARN)))

    # ---------------- SW5 ----------------
    if not lex_ok("SW5"):
        out.append(("SW5", "SKIP", "词表不可用：真值命中 %s 处"
                    % (lex_hits.get("SW5") if lex_hits else "N/A（真值取不到）")))
    elif prose_words <= 0:
        out.append(("SW5", "SKIP", "'无法判定'：节正文词数为 0"))
    else:
        n = len(RE_SW5.findall(prose))
        dens = n / prose_words * 1000.0
        out.append(("SW5", "WARN" if dens > SW5_DENSITY_WARN else "PASS",
                    "对比式+强调式构造 %d 处 / %d 词 = %.1f‰（提请复核线 > %.1f‰）"
                    % (n, prose_words, dens, SW5_DENSITY_WARN)))

    # ---------------- SW6 ----------------
    if not lex_ok("SW6"):
        out.append(("SW6", "SKIP", "词表不可用：真值命中 %s 处"
                    % (lex_hits.get("SW6") if lex_hits else "N/A（真值取不到）")))
    else:
        n = len(RE_SW6.findall(prose))
        out.append(("SW6", "WARN" if n >= SW6_COUNT_WARN else "PASS",
                    "自评式元话语 %d 处（提请复核线 ≥%d 处 [社区] 本项目自订）" % (n, SW6_COUNT_WARN)))

    # ---------------- SW7 ----------------
    cands = [s for s in sents
             if SW7_SHORT_LOW <= count_words(s) < SW7_SHORT_WORDS
             and not is_caption(s)
             and "=" not in s and "\\" not in s and "$" not in s]
    lens = [count_words(s) for s in sents if count_words(s) > 0]
    minlen = min(lens) if lens else 0
    warn = (minlen < SW7_SHORT_WORDS and len(cands) >= SW7_SHORT_MIN)
    out.append(("SW7", "WARN" if warn else "PASS",
                "最短句 %d 词 · 极短断言句（%d–%d 词）%d 处"
                "（提请复核线：最短句 <8 词且 ≥%d 处；★ 极短句**下界 %d 词** = [社区] 本项目自订，"
                "判词 :308 只给 <8 词）"
                % (minlen, SW7_SHORT_LOW, SW7_SHORT_WORDS - 1, len(cands),
                   SW7_SHORT_MIN, SW7_SHORT_LOW)))

    # ---------------- SW8 ----------------
    if not lex_ok("SW8"):
        out.append(("SW8", "SKIP", "词表不可用：真值命中 %s 处"
                    % (lex_hits.get("SW8") if lex_hits else "N/A（真值取不到）")))
    elif not sents:
        out.append(("SW8", "SKIP", "'无法判定'：本节无可切分的句子"))
    else:
        rm = [s for s in sents if RE_SW8.match(s.strip())]
        ratio = len(rm) / len(sents)
        out.append(("SW8", "WARN" if ratio >= SW8_RATIO_WARN else "PASS",
                    "可整体删除句 %d/%d = %.1f%%（提请复核线 ≥%.0f%%）"
                    % (len(rm), len(sents), ratio * 100, SW8_RATIO_WARN * 100)))
    return out


# --------------------------------------------------------------------------
# 节名（★ 现场从 references/sections.md 的 8 个 `##` 标题里取）
# --------------------------------------------------------------------------

def load_sections():
    ref = Path(__file__).resolve().parent / "references" / "sections.md"
    if not ref.is_file():
        return None
    names = []
    for ln in read_text(ref)[0].splitlines():
        m = re.match(r"^##\s*§([1-8])\s+(.*)$", ln)
        if not m:
            continue
        rest = m.group(2)
        name = re.split(r"[　\[]", rest, 1)[0].strip()
        if name:
            names.append((int(m.group(1)), name))
    names.sort()
    return names if len(names) == 8 else None


# --------------------------------------------------------------------------
# 输出
# --------------------------------------------------------------------------

RULE = "=" * 78
STATUS_LINE = re.compile(r"^(PASS|WARN|FAIL|SKIP)$")


def emit(rows):
    mark = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL", "SKIP": "SKIP"}
    for cid, st, detail in rows:
        print("%-4s %-5s  # %s" % (mark[st], cid, detail))


def print_boundaries():
    print()
    print("== 四条边界（与工具头部同文；必须与上面的读数同读）==")
    print("边界 1（阈值不可复算）: SW3–SW8 的阈值全部出自判词读数，两轮度量脚本未落盘 "
          "⇒ 不可重跑、不可复算 ⇒ 一律只出『提请复核』，绝不判死；不许读成『达标线』"
          "（judge-green.md:270：『0 与 0 之间无法定阈』）。")
    print("边界 2（词表先自测）: 见上方『词表自测』行；真值命中 ⇒ 该项降级为不可判，"
          "不得据此判产物有罪（judge.md:238）。")
    print("边界 3（压力臂）: 压力臂与自由臂必须分别设阈 —— 本工具做不到"
          "（节片段里没有『压力臂』这个概念）；本工具放弃的正是 RED 那一半控制手段。这是明确局限。")
    print("边界 4（四项不用）: 判词明令不用的四项判据一律不出现（清单见 references/metrics.md §边界 4）；"
          "源码里出现即 SELF1 红。")


def do_selfcheck():
    src = Path(__file__).read_text(encoding="utf-8", errors="replace")
    rows = selfcheck_source(src, __doc__ or "")
    print(RULE)
    print("check-section.py · 静态自检（关于本工具自己）")
    print(RULE)
    print("源码=%s" % Path(__file__).resolve())
    for cid, ok, detail in rows:
        print("%-4s %-5s  # %s" % ("PASS" if ok else "FAIL", cid, detail))
    bad = [cid for cid, ok, _ in rows if not ok]
    print()
    print("RESULT: %s" % ("FAIL" if bad else "PASS"))
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="MCM/ICM 逐节写作自检：SW1–SW8（SW1/SW2 硬失败；SW3–SW8 只出提请复核）"
                    "；硬失败另含 EMPTY（本节无可检正文）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python check-section.py section.tex --section 模型建立 --input brief.md\n"
               "  python check-section.py section.md --section 结论\n"
               "  python check-section.py --selfcheck\n")
    ap.add_argument("section_file", nargs="?", help="节文件（.tex 或 .md）")
    ap.add_argument("--section", default=None,
                    help="节名（取值 = references/sections.md 的 8 个 `##` 标题；不认识 ⇒ fail-closed 红）")
    ap.add_argument("--input", default=None,
                    help="写手输入（要点清单 + 已定稿的图表与结果；★ 设计 §1 的输入契约）"
                         "—— SW1/SW2 的燃料")
    ap.add_argument("--selfcheck", action="store_true",
                    help="只跑两条『关于本工具自己』的静态自检，不读节文件")
    args = ap.parse_args(argv)

    if args.selfcheck:
        return do_selfcheck()

    # ---- 源码自检：始终先跑（源码里出现禁用项 ⇒ 本工具自身 FAIL）----
    src = Path(__file__).read_text(encoding="utf-8", errors="replace")
    self_rows = selfcheck_source(src, __doc__ or "")

    if not args.section_file or not args.section:
        sys.stderr.write("错误: 需要 <节文件> 与 --section（或使用 --selfcheck）。"
                         "见 --help\n")
        return 2

    sections = load_sections()
    if sections is None:
        print("FAIL  SECTION  # 取不到 references/sections.md 的 8 个节名 ⇒ 无法校验 --section（fail-closed）")
        print("RESULT: FAIL")
        return 1
    name_of = {n: i for i, n in sections}
    if args.section not in name_of:
        print("FAIL  SECTION  # 不认识的 --section 值 %r（fail-closed；可用值 = %s）"
              % (args.section, " / ".join(n for _, n in sections)))
        print("RESULT: FAIL")
        return 1

    sec_path = Path(args.section_file)
    if not sec_path.is_file():
        print("FAIL  FILE     # 找不到节文件 %s（fail-closed）" % sec_path)
        print("RESULT: FAIL")
        return 1

    raw_text, enc = read_text(sec_path)
    raw_text = strip_reference_preamble(raw_text)
    raw_lines = raw_text.split("\n")
    tables = find_tables(raw_lines)
    paras = prose_paragraphs(raw_text, tables)

    # ---- F5 / H1：没有可检正文（无散文行、无表）⇒ fail-closed 红 ------------------
    # ★ 不许对"什么都没写"判 `PASS` —— 那会让"判据在无对象时不算失败"变成恒真。
    # ★ 触发线看的是**行**（`content_lines()`）：**非空 ∧ 非标题 ∧ 非公式** 的行才算正文。
    #   ⇒ "只有公式、无散文、无表" 也判 EMPTY（那种形态八条判据一条都检不了）；
    #   而一句 4 词的散文（`We use the following.`）**算正文** ⇒ 不判 EMPTY（`<5` 词只是解析门）。
    body = content_lines(raw_text)
    if not body and not tables:
        print("FAIL  EMPTY    # 本节没有可检正文（无散文行、无表；只有公式行也不够）⇒ 无从判定，"
              "fail-closed 红（对『什么都没写』判 PASS 是恒真型失效）")
        print("RESULT: FAIL")
        return 1

    input_text = None
    if args.input is not None:
        ip = Path(args.input)
        if not ip.is_file():
            print("FAIL  INPUT    # 找不到 --input 文件 %s（fail-closed）" % ip)
            print("RESULT: FAIL")
            return 1
        input_text = strip_reference_preamble(read_text(ip)[0])

    truth = truth_text(find_truth_dir(Path(__file__).resolve().parent))
    lex_hits = truth_lexicon_hits(truth)

    # ---- 抬头 ----
    print(RULE)
    print("check-section.py · mcm-section-writer · SW1–SW8")
    print(RULE)
    print("文件=%s" % sec_path.resolve())
    print("编码=%s" % enc)
    print("节=%s（§%d）" % (args.section, name_of[args.section]))
    print("输入=%s" % ("（未给 --input ⇒ SW1/SW2 报『无法判定』）" if input_text is None
                       else Path(args.input).resolve()))
    print("散文段数=%d · 句子数=%d · 正文词数=%d · 检出表格=%d"
          % (len(paras), sum(len(split_sentences(p)) for p in paras),
             count_words("\n".join(paras)), len(tables)))
    if lex_hits is None:
        print("词表自测（真值 true-S1.md/true-S2.md）: 真值取不到 ⇒ 词表判据全部降级为『不可判』")
    else:
        print("词表自测（真值 true-S1.md/true-S2.md 的命中数；★ 命中 0 才可用）: "
              + " ".join("%s=%d" % (c, lex_hits[c]) for c, _ in LEXICONS))

    rows = judge(raw_text, raw_lines, tables, paras, input_text, lex_hits)
    print()
    emit(rows)
    for cid, ok, detail in self_rows:
        print("%-4s %-5s  # %s" % ("PASS" if ok else "FAIL", cid, detail))

    fails = [c for c, st, _ in rows if st == "FAIL"] + [c for c, ok, _ in self_rows if not ok]
    warns = [c for c, st, _ in rows if st == "WARN"]
    skips = [c for c, st, _ in rows if st == "SKIP"]
    passes = [c for c, st, _ in rows if st == "PASS"]

    print_boundaries()
    print()
    print("汇总: PASS=%d WARN=%d FAIL=%d SKIP=%d" % (len(passes), len(warns), len(fails), len(skips)))
    if warns:
        print("WARN（提请复核，不是判死；退出码不受影响）: %s" % ", ".join(warns))
    if skips:
        print("SKIP（无法判定；退出码不受影响）: %s" % ", ".join(skips))
    if fails:
        print("RESULT: FAIL")
        print("失败项=%s" % ",".join(fails))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
