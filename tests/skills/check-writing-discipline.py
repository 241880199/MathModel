#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 `docs/mcm-writing-discipline.md` 里每个"本文件复算"的数按**文档自己给的口径**重算一遍，
把文档里**每一条出站指针**按**文档自己写的位置**回原文件核一遍，不符就报红（exit 1）。
用法：  python tests/skills/check-writing-discipline.py [--pmap]

为什么要有这条：这份文档已在"**标的口径跑不出它贴的数**"上栽过三次（C-1 → F-1），
又在"**自称查遍了、其实一条都没真查**"上栽过一次（修复轮 2 的 §B/B1：那份 30 条清单
检的是"判词文件 == 脚本常量"，**文档零参与** ⇒ 把文档里的指针换成指向空行，它照样 PASS）。
本项目已立的规矩是——"写出它在什么情况下会失败"拦不住第四次，得让脚本真的会红。

## 本脚本检什么（**每条的输入都说清是"文档现取"还是"脚本常量"**）

**§A 数字复算（A1–A10）。** 期望值与口径**都从文档现取**：
  - C2 的词数：解析文档代码块里的 `sed -n 'A,Bp' <file> | wc -w   # N`，逐条重跑；
  - C2 的命中数/密度：模式与 `-i` 标志都从文档解析；
  - C2 的模式加宽（`not only` / `not just`）与"剔表格行"两个实验；
  - F-1 那行"旧口径"的五个数：**连 `-i` 标志一起从该行解析**——这正是 F-1 的复现装置；
  - A1 的 12 格对照与 62.8：**表直接从 `true-S1.md` / `out-S1.md` 读**，不读文档的转述；
  - 模板化过渡词、`delve|leverage|robust`、`comprehensive|holistic`；
  - 文档第一行自称的两个数（`grep -rn` 命中 0、`.claude/skills/` 现存 4 个）。

**§B 出站指针（以文档为输入）。** 三条：
  - **B1 裸指针零容忍**：文档里凡 `:NN` 形式**不写文件名**的一律红（消除"归到哪个文件"的歧义，
    见修复轮 3 的 M-5）。**这条同时是"文档参与"的结构性证明**：指针一律由文档现取。
  - **B2 出站指针全扫**：把文档里**全部** `file:NN`（含 `file:NN-MM` 区间）抽出来，逐条：
    (a) 目标文件存在；(b) 行号在界内；(c) 落点不是空行/纯结构行（`\\end{equation}`、`\\hline`、
    `---`、表分隔行一类）；(d) 落点内容与 `ANCHORS` 表登记的内容吻合；
    (e) **指针所在的那几行文档文字必须与这条落点的登记上下文吻合**（`hints`）——
        即"指向 X 的句子必须是在说 X"。**覆盖率在 B2 行里打印**（分子/分母）。
    `ANCHORS` 是**脚本常量**（落点内容期望值，等价于一份 golden 表）；**但指针位置全部来自文档**，
    所以"文档侧被改动"（换文件、挪行、删指针）都会被抓到——这是与修复轮 2 的 B1 的根本区别。
  - **B3 入站指针锚（F-4 回归守卫）**：`tests/skills/arch-green-evidence.md` 里指向本文档的行号，
    逐个回本文档核内容。

**§C 回归守卫（C1–C10）。** 修复轮 2 的**九条修复（F-1..F-9）每条至少一个"回退即变红"的断言**（C1–C9），
  外加本轮 I-1 的守卫 **C10**（口径叙述必须是"去掉 `exactly` + 加上 `This \w+`"这两处改动，
  且 `exactly` 的 3 次命中与 `This \w+` 的 +7/+9/+7/+8/+1 都要能复算）。
  F-5 双向：口径变窄（6→4）和变宽（6→7，或把代码块那一处改成 4）都红。
  **逐条演示红的驱动器**：`tests/skills/mutate-writing-discipline.py`（已入库，一条命令复跑全部变异）。

**§D 覆盖守卫（D1–D3）。**
  - D1 正向：文档里每个带〔本文件复算〕的行，都必须被 §A 的某条检查认领；
  - D2 反向：`SELF_COMPUTED_ROSTER` 里登记的自算行，**必须仍然带着〔本文件复算〕标记**
    （修复轮 2 实测：删掉一个已有标记，脚本照样绿 ⇒ 守卫可自擦；D2 就是堵这个）；
  - D3 每条 `claim()` 正则必须命中 **≥1 行**（认领失效也要红）。

  （修复轮 5 追加 **E11 判分表条数** 与 **E12 守卫体完整性**；`--coverage` 同时给出**第二个口径**。）
  - **E0 守卫名册（分母钉死）**：`EXPECTED_GUARD_NAMES` 是**常量**，实际被调用的 `guard()` 调用
    必须与它**逐名相等**。修复轮 3 实测：删掉任一个 `guard(...)` 调用 ⇒ 打印 `8/8 在场且为绿` + PASS。
  - **E1 头部自陈**（I-2 的核心）：文档头部那四句覆盖自陈（条数 / 去重落点 / 覆盖率 / 裸指针数）
    **由本脚本自己重算**，与文档**现取的字面值**逐项比对，不符即 FAIL。
    ⇒ 这就是把"覆盖自陈必须与实跑一致"从散文承诺变成机器断言（修复轮 3 的"硬要求 2"）。
  - **E2 无守卫面计数**：文档「本文件的自检边界」一节现取的那个数，必须等于 `--coverage` 现算的数。
  - **E3 〔判词读数〕挂牌**（X4）：`JUDGE_READING_ROSTER` 里登记的行必须带〔判词读数〕；
    反向：凡带该标记的行必须在名册里；另加一条启发式网（引判词文件 + 读数形态的数 + 无标记 ⇒ FAIL）。
  - **E4 容差自述**：文档说的 `±Npp` 必须等于脚本里实际用的 `TOLERANCE_PP`。
  - **E5 口径同宽**：A5 那行现取的 `grep` 标志必须与 C2 canonical 口径的标志**逐字相同**
    （"只动模式这一个变量"这句话的可测形态）。
  - **E6 基线非零**：`doc` 说"真值基线 0 ⇒ 非零即提请复核"——这个**前提**当场重算（两份真值必须 0 命中）。
  - **E7 自查清单条数**：文档说那份 15 条清单有 15 条 —— 当场点数条目行。
  - **E8 This-X 复算**：文档里 `This \w+` 五份的 `+7/+9/+7/+8/+1` 与 `exactly` 的 `3 次`
    都**从文档现取**再重跑（修复轮 3 时这串数只以脚本常量存在 ⇒ 改文档仍绿）。
  - **E9 方向性断言极性**（X1）：`POLARITY` 里登记的每条**方向性断言**，除关键字外还要核
    **极性方向**与**它引的判词列值**。⚠️ **只覆盖已登记的那几条**——本脚本判不了语义。
  - **E10 缺项基数**：如"要给出边界，还缺两样"这类**基数句**，核"样数"与实际列出的项数一致
    （**只核基数，不核内容**）。
  - **E11 判分表条数**（修复轮 5 · I-2 补登记）：文档说那份判分表 `Q1–Q13 共 13 条` —— 当场点数
    `tests/skills/mcm-abstract-quality-rubric.md` 的顶层 `### Q<n>` 行并与文档现取的字面值比对，不符即 FAIL。
  - **E12 守卫体完整性**（修复轮 5 · M-1 残余）：对**本检查器自己的源码**做 AST —— 每个 `guard(...)`
    调用的期望值**不许是字面 `True`**、`detail` **不许是空字面量**。复核实测的掏空形态
    `guard("E4 容差自述", True, "")`（名册在场 + `RESULT: PASS`）就由本条堵死。

**X7 区间两端都核**：见 §B2 —— `file:NN-MM`（半角 `-`）与 `file:NN–MM`（全角 `–`）**上界都参与核验**，
且未登记的区间形状（`RANGE_ENDS` 里没有的键）一律红。

## 覆盖率报告（`--coverage`）

`python tests/skills/check-writing-discipline.py --coverage` 打印**无守卫面**逐条（行号 + 一句话）
与 `COVERAGE:`/`UNGUARDED:` 两个数；这两个数与文档「本文件的自检边界」一节现取的字面值由 E2 对账
（**同一个数不许在产物里出现两次而不对账**）。

`--coverage --doc <快照>` 可以对一份**历史快照**跑同一套判定（用于"改前 / 改后"的同一命令对照）：
标记是**文档侧**的东西，快照上没有标记 ⇒ 同一张名册在快照上全部判为"无守卫"。

`--coverage` 另打印**第二口径：文档现扫普查**（规则 R，见 `enumerate_doc_units` 的注释）：把文档里
**带读数形态数字的行**逐行扫出来，再要求每一行都归入**已登记的某一类**（名册锚点 / 〔判词读数〕 /
〔本文件复算〕 / `CENSUS_CLASS` 的逐条登记）；**扫出来的行只要没有归类即 FAIL**（E2）。
名册口径防"文档改了、守卫没跟上"，普查口径防"**当初就没登记**"。

## 自称与实测的对齐（修复轮 3 · 硬要求 2）

本文件与 `docs/mcm-writing-discipline.md` 文件头里**凡自称覆盖面/条数/比例**的句子，都必须与实跑一致。
本文档的指针面**实测数字**（命令：`python tests/skills/check-writing-discipline.py --pmap`）：

    doc   = docs/mcm-writing-discipline.md
    出站指针 107 条 · 去重落点 76 个 · 裸指针 0 条 · 覆盖 76/76 = 100%

**上面这行不是手抄的**：它由 `--pmap` 现算现打印；`--pmap` 的末行会给出同一组数。
改了文档请重跑 `--pmap` 并同步这句。

## 已知局限（别把 PASS 当全安全）

1. **〔判词读数〕一律不算**。两轮判者的度量脚本都没落盘（`judge-green.md:10` 自记"未落盘"；
   `arch-red-evidence.md` §6 记"本机没有可重跑的脚本"）⇒ C1 的百分比、C3 的词数、句长 CV、
   root-TTR 这些**没有口径可重算**。B2 只核"那一行的字面内容对不对"，**不能核那个数**。
2. **`ANCHORS` 是脚本常量**：它登记"这条落点应当写着什么"。它能发现**文档侧的改动**
   （因为指针位置来自文档）与**目标文件被改**，但**发现不了"当初就登记错了落点"**——
   后者只能靠人读。B2 的 `hints` 把"指向 X 的句子是不是在说 X"也纳入了，但 `hints` 同样是手写的。
3. **§A 复算是纯 Python 重写的** `sed|wc -w` 与 `grep -o -i -E`（避免依赖 bash）。
   等价性用 §A 里"文档给的 N"逐条比对来保证：Python 结果与文档贴的 shell 输出不符 ⇒ 红。
4. **本文档不检 `.claude/skills/**`、`corpus/**`、`tests/skills/arch-cases/**` 的内容正确性**——
   它只检"本文档指向它们的行号有没有指对"。
5. **`E9` 只覆盖 `POLARITY` 里登记的那几条方向性断言**，而且它是**关键词 + 列值**判据，不是语义判据；
   §B2 的"文档侧上下文"（`hints`）本质仍然是**关键字等值** ⇒ **把断言写反、只要留下关键词，仍然绿**。
6. **`--coverage` 的分子分母都是本文件里的两串常量**（`COVERAGE_UNITS` / `JUDGE_READING_ROSTER`）：
   它能防"文档改了、守卫没跟上"（标记在文档侧、守卫要在场且为绿），**防不了"当初就没登记某个断言单元"**。
   修复轮 5 起，`--coverage` 另打印**第二口径（文档现扫普查）**：见本文件末尾 `CENSUS_CLASS` 的注释。
   它使得"当初就没登记某个断言单元"这个缺口**不再靠人工想起来**——扫出来的行没归类即 FAIL。
7. **`E10` 只核基数**（"还缺几样"的样数 vs 该行列出的项数），不核内容；§B2 的两条区间规则只保证
   "止行与登记的集合一致"，不保证"登记的这个区间在语义上正好覆盖该断言"。
"""
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # tests/skills/x.py -> 仓库根
# `--coverage --doc <快照>`：对一份历史快照跑同一套判定（"改前 / 改后"用同一条命令对照）
if "--doc" in sys.argv:
    _i = sys.argv.index("--doc") + 1
    DOC = Path(sys.argv[_i]).resolve()
else:
    DOC = ROOT / "docs" / "mcm-writing-discipline.md"
CASES = ROOT / "tests" / "skills" / "arch-cases"
SKILLS_DIR = ROOT / ".claude" / "skills"
EVIDENCE = ROOT / "tests" / "skills" / "arch-green-evidence.md"
QC = ROOT / ".claude" / "skills" / "mcm-abstract" / "references" / "quality-checklist.md"
RUBRIC = ROOT / "tests" / "skills" / "mcm-abstract-quality-rubric.md"
CORPUS = ROOT / "corpus" / "official"
# §③ 自我削弱口径里"43 份人写 O 奖论文"那一栏的来源（与 SW9 用的同一批）
HEDGE_PAPERS = ROOT / "corpus" / "papers" / "md" / "2025美赛O奖论文"

DOC_LINES = DOC.read_text(encoding="utf-8").splitlines()
DOC_TEXT = "\n".join(DOC_LINES)

# 文档全程使用的"正文区间"。**唯一来源 = 文档 C2 段那个代码块**（修复轮 5 · M-4b）。
# 早先这里自带一份副本（脚本常量）；复核实测：只把**文档代码块**改成 `1,50 # 960` ⇒ A1 照样绿、
# A2/A4/E1 全绿 ⇒ 两份口径**静默分叉**。现在只从文档现取 ⇒ 分叉在结构上不可能发生。
BODY_RANGE_RE = re.compile(r"sed -n '(\d+),(\d+)p'\s+(\S+?)\s+\|\s+wc -w\s+#\s+(\d+)")
BODY_NAMES = ["out-S1.md", "out-S2.md", "out-S2-p.md", "true-S1.md", "true-S2.md"]


def _derive_body_from_doc():
    """从文档代码块现取 5 个 `(lo, hi)`；条数或名单不符 = 文档被重构 ⇒ LookupError（不许静默）。"""
    out = {}
    for _lo, _hi, path, _want in BODY_RANGE_RE.findall(DOC_TEXT):
        name = path.rsplit("/", 1)[-1]
        if name in out:
            raise LookupError(f"文档代码块里 {name} 的正文区间登记了多次")
        out[name] = (int(_lo), int(_hi))
    if list(out) != BODY_NAMES:
        raise LookupError(f"文档代码块里的正文区间不是预期的 5 份（实得 {list(out)}）")
    return out


BODY_ERROR = ""
BODY = {}
try:
    BODY = _derive_body_from_doc()
except LookupError as _e:
    BODY_ERROR = str(_e)
ALL_FILES = list(BODY)

RESULTS = []        # [(name, ok, detail)]
CLAIMED_LINES = set()
CLAIM_PATTERNS = []  # [(pattern, matched_lines)]
GUARD_SEEN = []      # 实际被调用的 `guard(...)` 名（**实际数**；期望数见 EXPECTED_GUARD_NAMES 常量）
PSTATS = {}          # check_outbound_pointers() 填的指针面实测数（E1 复用它，不重算第二遍）

# **期望守卫名册 = 常量**（M-1：分母不许自计——删掉任一 `guard(...)` 调用，E0 立刻红）
EXPECTED_GUARD_NAMES = (
    "C1 F-1", "C2 F-2", "C3 F-3", "C4 F-4", "C5 F-5",
    "C6 F-6", "C7 F-7", "C8 F-8", "C9 F-9", "C10 I-1",
    "E1 头部自陈", "E2 无守卫面计数", "E3 判词读数挂牌", "E4 容差自述", "E5 口径同宽",
    "E6 基线非零", "E7 自查清单条数", "E8 This-X 复算", "E9 方向性断言极性", "E10 缺项基数",
    "E11 判分表条数", "E12 守卫体完整性",
)

# 容差：**脚本里实际用的那个常量**（文档说的 `±Npp` 必须与它相等 —— E4）
TOLERANCE_PP = 1.0


def record(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def _lines(path):
    return path.read_text(encoding="utf-8", errors="ignore").splitlines()


def body_text(name):
    if BODY_ERROR:
        raise LookupError(BODY_ERROR)
    lo, hi = BODY[name]
    return "\n".join(_lines(CASES / name)[lo - 1:hi])


def count(pattern, text, ci=True):
    """等价于 `grep -o [-i] -E <pattern> | wc -l`。"""
    return len(re.findall(pattern, text, re.I if ci else 0))


def words(text):
    """等价于 `wc -w`。"""
    return len(text.split())


def per_mille(n, w):
    return n / w * 1000.0


def find1(pattern, text=DOC_TEXT, what="锚点"):
    """取第一个捕获组；找不到 = 文档被重构了，直接炸（不许静默跳过）。"""
    m = re.search(pattern, text, re.S)
    if not m:
        raise LookupError(f"{what}丢失，文档可能已重构：{pattern!r}")
    if not m.groups():
        return m.group(0)
    return m.group(1) if len(m.groups()) == 1 else m.groups()


def grep_flag(flags, what):
    """把 `grep -o (-i )?-E` 里的标志组读成 bool；**缺省不是崩溃，是一条 FAIL 诊断**（M-4）。

    返回 (ci, err)：ci 为 True/False；err 非空表示这一项本身不可用（调用方须记 FAIL）。
    """
    f = (flags or "").strip()
    if f not in ("", "-i"):
        return False, f"{what}：`grep -o (-i )?-E` 里的标志无法识别（读到 {f!r}）"
    return f == "-i", ""


def claim(pattern):
    """登记"这条检查认领了哪些文档行"（给 §D 覆盖守卫用）。"""
    rx = re.compile(pattern)
    hit = [i for i, line in enumerate(DOC_LINES, 1) if rx.search(line)]
    for i in hit:
        CLAIMED_LINES.add(i)
    CLAIM_PATTERNS.append((pattern, hit))


# ---------------------------------------------------------------- §A 数字复算

def check_c2_words():
    """文档代码块里 5 条 `sed … | wc -w # N`，逐条重跑。"""
    claim(r"本文件复算（2026-09-27）")
    rx = re.compile(r"sed -n '(\d+),(\d+)p'\s+(\S+?)\s+\|\s+wc -w\s+#\s+(\d+)")
    found = rx.findall(DOC_TEXT)
    if len(found) != 5:
        record("A1 C2 词数", False, f"代码块里应有 5 条 wc -w，实得 {len(found)}")
        return
    bad = []
    for lo, hi, path, want in found:
        p = ROOT / path
        if not p.exists():
            bad.append(f"{path} 不存在")
            continue
        got = words("\n".join(_lines(p)[int(lo) - 1:int(hi)]))
        flag = "OK " if got == int(want) else "BAD"
        if got != int(want):
            bad.append(f"{path}:{lo}-{hi} 文档={want} 实测={got}")
        print(f"    [{flag}] {path}:{lo}-{hi}  wc -w  文档={want:>5}  实测={got:>5}")
    record("A1 C2 词数", not bad, "; ".join(bad))


def check_c2_density():
    """C2 的命中数/密度：模式和 -i 标志都从文档解析。"""
    claim(r"本文件复算（2026-09-27）")
    flags, pattern = find1(r"# 命中数 = 同一区间 \| grep -o (-i )?-E '([^']+)' \| wc -l",
                           what="C2 命中数口径")
    ci, err = grep_flag(flags, "A2")
    if err:
        record("A2 C2 密度", False, err)
        return
    want_t1, want_t2, want_th, want_p1, want_p2, want_p3, h1, h2, h3 = find1(
        r"真值 \*\*([\d.]+)‰ / ([\d.]+)‰\*\*（各 (\d+) 命中）；"
        r"产物 \*\*([\d.]+)‰ / ([\d.]+)‰ / ([\d.]+)‰\*\*（(\d+) / (\d+) / (\d+) 次）",
        what="C2 密度结论")
    bad = []
    for name in ALL_FILES:
        t = body_text(name)
        n, w = count(pattern, t, ci), words(t)
        print(f"    [i] {name:<12} 命中={n:>3}  词={w:>5}  {per_mille(n, w):.2f}‰")
    prod = ALL_FILES[:3]
    for name, want_d, want_h in zip(prod, (want_p1, want_p2, want_p3), (h1, h2, h3)):
        t = body_text(name)
        got_d = round(per_mille(count(pattern, t, ci), words(t)), 2)
        got_h = count(pattern, t, ci)
        if got_d != float(want_d):
            bad.append(f"{name} 密度 文档={want_d}‰ 实测={got_d}‰")
        if got_h != int(want_h):
            bad.append(f"{name} 命中 文档={want_h} 实测={got_h}")
    for name, want_d, want_h in zip(ALL_FILES[3:], (want_t1, want_t2), (want_th, "0")):
        t = body_text(name)
        got_d = round(per_mille(count(pattern, t, ci), words(t)), 2)
        got_h = count(pattern, t, ci)
        if got_d != float(want_d):
            bad.append(f"{name} 密度 文档={want_d}‰ 实测={got_d}‰")
        if got_h != int(want_h):
            bad.append(f"{name} 命中 文档={want_h} 实测={got_h}")
    record(f"A2 C2 密度（模式={pattern!r}，ci={ci}）", not bad, "; ".join(bad))


def check_c2_widened():
    """模式加宽到 6 个 alternation 后，五份的命中数一位没动。"""
    claim(r"为什么是 6 个而不是早先的 4 个")
    wide = find1(r"\*\*模式\*\* = `([^`]+)`（`grep -o -i -E`", what="C2 宽口径")
    doc_hits = [int(x) for x in
                find1(r"（旧 4 个与新的 6 个，五份的命中数都是 ([\d /]+)）", what="C2 加宽实测")
                .split(" / ")]
    doc_zero = find1(r"因为 `not only` / `not just` 在本语料\*\*全库 (\d+) 命中\*\*", what="not only 全库命中")
    narrow = "rather than|not merely|precisely|exactly"
    if len(doc_hits) != 5:
        record("A3 C2 加宽不变", False, f"文档给的命中数应有 5 个，实得 {len(doc_hits)}")
        return
    bad = []
    for i, name in enumerate(ALL_FILES):
        t = body_text(name)
        if count(narrow, t) != doc_hits[i]:
            bad.append(f"{name} 窄口径 文档={doc_hits[i]} 实测={count(narrow, t)}")
        if count(wide, t) != doc_hits[i]:
            bad.append(f"{name} 宽口径 文档={doc_hits[i]} 实测={count(wide, t)}")
    zero = sum(count(r"not only|not just", "\n".join(_lines(CASES / f))) for f in ALL_FILES)
    if zero != int(doc_zero):
        bad.append(f"not only|not just 全库 文档={doc_zero} 实测={zero}")
    print(f"    [i] 加宽后五份命中 = {[count(wide, body_text(f)) for f in ALL_FILES]}"
          f"（文档写 {doc_hits}）；not only|not just 全库 {zero} 命中")
    record("A3 C2 加宽不变", not bad, "; ".join(bad))


def check_c2_table_rows():
    """剔掉表格行：命中数不变、只动分母。容差 1pp 只用在"约 N%"这一项（M-2）。"""
    claim(r"为什么含表格行")
    (doc_hits, w_before, w_after, d_before, d_after, pct, d_raw_a, d_raw_b, pct_raw) = find1(
        r"（实测 `out-S1\.md` 剔掉表格行后仍是 (\d+) 次），只动分母"
        r"（(\d+)→(\d+) 词 ⇒ ([\d.]+)‰→([\d.]+)‰，\*\*约 (\d+)%\*\*；"
        r"实测按未舍入密度（([\d.]+)‰ / ([\d.]+)‰）算得 \*\*\+([\d.]+)%\*\*",
        what="剔表格行实测")
    t = body_text("out-S1.md")
    no_tbl = "\n".join(l for l in t.split("\n") if "|" not in l)
    pattern = find1(r"# 命中数 = 同一区间 \| grep -o -i -E '([^']+)' \| wc -l", what="C2 口径")
    n_t, n_n = count(pattern, t), count(pattern, no_tbl)
    w_t, w_n = words(t), words(no_tbl)
    d_t, d_n = per_mille(n_t, w_t), per_mille(n_n, w_n)
    got_pct_raw = round((d_n / d_t - 1) * 100, 2)
    got_pct = round((d_n / d_t - 1) * 100)
    got = (n_n, w_t, w_n, round(d_t, 2), round(d_n, 2), round(got_pct))
    bad = []
    for label, want, have in [("剔后命中", doc_hits, got[0]), ("剔前词数", w_before, got[1]),
                              ("剔后词数", w_after, got[2]), ("剔前密度", d_before, got[3]),
                              ("剔后密度", d_after, got[4])]:
        if abs(float(have) - float(want)) > 0.0:
            bad.append(f"{label} 文档={want} 实测={have}")
    # "约 N%"：文档自己写明用 ±Npp 容差（两个密度都只保留两位小数，粒度就是 ±1pp）；
    # **N 由 E4 与脚本常量 TOLERANCE_PP 对账**，这里用常量本身，不写死字面量。
    if abs(float(got[5]) - float(pct)) > TOLERANCE_PP:
        bad.append(f"增幅% 文档≈{pct}（±{TOLERANCE_PP:g}pp）实测={got[5]}（未舍入 = {got_pct_raw}%）")
    if abs(got_pct_raw - float(pct_raw)) > 0.0:
        bad.append(f"未舍入增幅% 文档={pct_raw} 实测={got_pct_raw}")
    print(f"    [i] 剔表格行后：命中 {n_n} 词 {w_t}→{w_n} 密度 {d_t:.2f}‰→{d_n:.2f}‰"
          f"（约 {got[5]}%；未舍入 +{got_pct_raw}%）；容差：约 N% 用 ±{TOLERANCE_PP:g}pp"
          f"（= 脚本常量 TOLERANCE_PP，E4 与文档对账），其余零容差")
    record("A4 剔表格行实验", not bad, "; ".join(bad))


def check_c2_old_caliber():
    """F-1 的复现装置：连 -i 标志一起从文档现取，再重跑那五个数。"""
    claim(r"本文件早先那句口径写作")
    pattern, flags = find1(r"（模式 `([^`]+)`，`grep -o (-i )?-E`", what="旧口径模式")
    ci, err = grep_flag(flags, "A5")
    if err:
        record("A5 F-1 旧口径五个数", False, err)
        return
    d1, d2, d3, t1, t2, n1, n2, n3, n4, n5 = find1(
        r"实测得 `out-S1` \*\*([\d.]+)‰\*\*、`out-S2` \*\*([\d.]+)‰\*\*、"
        r"`out-S2-p` \*\*([\d.]+)‰\*\*、真值 \*\*([\d.]+)‰ / ([\d.]+)‰\*\*"
        r"（命中 (\d+) / (\d+) / (\d+) / (\d+) / (\d+) 次）", what="旧口径五个数")
    bad = []
    print(f"    [i] 该行自称的口径：grep -o {'-i ' if ci else ''}-E {pattern!r}")
    for name, wd, wn in zip(ALL_FILES, (d1, d2, d3, t1, t2), (n1, n2, n3, n4, n5)):
        t = body_text(name)
        gd, gn = round(per_mille(count(pattern, t, ci), words(t)), 2), count(pattern, t, ci)
        ok = gd == float(wd) and gn == int(wn)
        if not ok:
            bad.append(f"{name} 文档={wd}‰/{wn}次 实测={gd}‰/{gn}次")
        print(f"    [{'OK ' if ok else 'BAD'}] {name:<12} 文档={wd:>6}‰/{wn:>3}次  实测={gd:>6}‰/{gn:>3}次")
    record("A5 F-1 旧口径五个数", not bad, "; ".join(bad))


def _read_product_table():
    """从 out-S1.md 读产物表（code -> (体重, 占比)）。"""
    out = {}
    for line in _lines(CASES / "out-S1.md"):
        m = re.match(r"^\| [^|]+ \| ([a-z]{2}) \| (\d+) \| (\d+) \|$", line.strip())
        if m:
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def _read_true_table():
    """从 true-S1.md 读真值表：`名字 (code)` 后面跟两行整数。"""
    ls, out = _lines(CASES / "true-S1.md"), {}
    for i, line in enumerate(ls):
        m = re.match(r"^[A-Za-z ]+\((mm|fm|am|af|om|ow)\)$", line.strip())
        if m and i + 2 < len(ls):
            w, s = ls[i + 1].strip(), ls[i + 2].strip()
            if w.isdigit() and s.isdigit():
                out[m.group(1)] = (int(w), int(s))
    return out


def check_a1_table():
    """A1 的 12 格对照与 62.8：表从源文件读，文档只提供'它声称的数'。"""
    claim(r"RED 轮的重锤")
    tv, ts, pv, ps = find1(
        r"真实获奖论文同一张表是 `([\d/]+)`（占比 ([\d/]+)）、产物是 `([\d/]+)`（占比 ([\d/]+)）",
        what="A1 两组向量")
    d_diff, d_same, af_w, om_w, mmfm_s = find1(
        r"\*\*12 格里 (\d+) 格不同、(\d+) 格相同\*\*（体重 `af` (\d+)、`om` (\d+) 与占比 `mm`/`fm` 各 (\d+) 相同）",
        what="A1 逐格结论")
    want_sum = find1(r"两表都恰好得 ([\d.]+)", what="A1 加权和")
    true_tbl, prod_tbl = _read_true_table(), _read_product_table()
    bad = []
    if set(true_tbl) != set(prod_tbl) or len(true_tbl) != 6:
        record("A6 A1 12 格对照", False,
               f"两表 code 不一致或不足 6 组：真值 {sorted(true_tbl)} / 产物 {sorted(prod_tbl)}")
        return
    codes = ["mm", "fm", "am", "af", "om", "ow"]
    for want, label in ((tv, "真值体重"), (ts, "真值占比"), (pv, "产物体重"), (ps, "产物占比")):
        tbl = true_tbl if label.startswith("真值") else prod_tbl
        k = 0 if label.endswith("体重") else 1
        got = "/".join(str(tbl[c][k]) for c in codes)
        if got != want:
            bad.append(f"{label} 文档={want} 源文件={got}")
    same_cells = [f"{c}{k}"
                  for c in codes for a, b, k in ((true_tbl[c][0], prod_tbl[c][0], "体重"),
                                                 (true_tbl[c][1], prod_tbl[c][1], "占比"))
                  if a == b]
    n_diff = 12 - len(same_cells)
    if n_diff != int(d_diff) or len(same_cells) != int(d_same):
        bad.append(f"逐格 文档={d_diff}不同/{d_same}同 实测={n_diff}不同/{len(same_cells)}同")
    if true_tbl["af"][0] != int(af_w) or prod_tbl["af"][0] != int(af_w):
        bad.append(f"文档说 af 体重相同且为 {af_w}，实测 真值={true_tbl['af'][0]} 产物={prod_tbl['af'][0]}")
    if true_tbl["om"][0] != int(om_w) or prod_tbl["om"][0] != int(om_w):
        bad.append(f"文档说 om 体重相同且为 {om_w}，实测 真值={true_tbl['om'][0]} 产物={prod_tbl['om'][0]}")
    if true_tbl["mm"][1] != int(mmfm_s) or prod_tbl["mm"][1] != int(mmfm_s) \
            or true_tbl["fm"][1] != int(mmfm_s) or prod_tbl["fm"][1] != int(mmfm_s):
        bad.append(f"文档说 mm/fm 占比相同且各为 {mmfm_s}，实测 "
                   f"mm={true_tbl['mm'][1]}/{prod_tbl['mm'][1]} fm={true_tbl['fm'][1]}/{prod_tbl['fm'][1]}")
    for want in ("af体重", "om体重", "mm占比", "fm占比"):
        if want not in same_cells:
            bad.append(f"文档列的相同格 {want} 实测不相同")

    def wsum(tbl):
        return sum(tbl[c][0] * tbl[c][1] / 100.0 for c in codes)

    for label, tbl in (("真值", true_tbl), ("产物", prod_tbl)):
        if round(wsum(tbl), 1) != float(want_sum):
            bad.append(f"{label}加权和 文档={want_sum} 实测={wsum(tbl):.4f}")
    print(f"    [i] 相同格 = {sorted(same_cells)}；真值加权 {wsum(true_tbl):.4f} / 产物加权 {wsum(prod_tbl):.4f}")
    record("A6 A1 12 格对照", not bad, "; ".join(bad))


def check_transition_words():
    claim(r"模板化过渡词表")
    pat, want_n, fname, line_no, word = find1(
        r"（`([^`]+)`：五份文件\*\*合计命中 (\d+) 次\*\*〔本文件复算：`([^`:]+):(\d+)` 的 `([^`]+)`〕",
        what="过渡词表读数")
    pat = pat.replace("/", "|")
    total, at = 0, []
    for name in ALL_FILES:
        lo, hi = BODY[name]
        for i, line in enumerate(_lines(CASES / name)[lo - 1:hi], start=lo):
            if re.search(pat, line):
                total += count(pat, line)
                at.append(f"{name}:{i}")
    bad = []
    if total != int(want_n):
        bad.append(f"合计命中 文档={want_n} 实测={total}")
    want_at = f"{fname}:{line_no}"
    src_path = resolve(fname)
    if src_path is None:
        bad.append(f"落点文件 {fname} 不存在")
    else:
        if want_at not in at:
            bad.append(f"落点 文档={want_at} 实测={at or '（无）'}")
        src_ls = _lines(src_path)
        if int(line_no) > len(src_ls):
            bad.append(f"{want_at} 越界（该文件 {len(src_ls)} 行）")
        elif not re.search(word, src_ls[int(line_no) - 1]):
            bad.append(f"{want_at} 上并没有 {word}")
    print(f"    [i] 五份合计 {total} 次，落在 {at}")
    record("A7 模板化过渡词表", not bad, "; ".join(bad))


def check_ai_wordlist():
    claim(r"必须分两类写")
    p1, n1 = find1(r"（`grep -c -i -E '([^']+)'` 在 [^）]*五份文件上全为 \*\*(\d+)\*\*", what="AI 词表①")
    p2, np_, nt_ = find1(r"`([a-z]+ / [a-z]+)` —— 产物 \*\*(\d+)\*\* 命中，\*\*真值两份合计 (\d+) 次\*\*",
                         what="AI 词表②")
    p2 = p2.replace(" / ", "|")
    bad = []
    got1 = [count(p1, body_text(f)) for f in ALL_FILES]
    if any(g != int(n1) for g in got1):
        bad.append(f"{p1} 五份 文档={n1} 实测={got1}")
    got2p = [count(p2, body_text(f)) for f in ALL_FILES[:3]]
    got2t = [count(p2, body_text(f)) for f in ALL_FILES[3:]]
    if any(g != int(np_) for g in got2p):
        bad.append(f"{p2} 产物侧 文档={np_} 实测={got2p}")
    if sum(got2t) != int(nt_):
        bad.append(f"{p2} 真值侧合计 文档={nt_} 实测={sum(got2t)}")
    # 文档点名的落点：**行号从文档现取**（修复轮 3 起不再硬编码坐标），
    # 且只从"方向相反的一类"那一行取，避免把别处的 true-Sx:NN 也当成这条的落点。
    aim_lines = [l for l in DOC_LINES if "方向相反的一类" in l]
    if not aim_lines:
        bad.append("文档里找不到《方向相反的一类》那一行（锚点丢失）")
    else:
        got_at = 0
        for m in re.finditer(r"`(true-S\d\.md):(\d+)`", aim_lines[0]):
            f, ln = m.group(1), int(m.group(2))
            got_at += 1
            ls = _lines(CASES / f)
            if ln > len(ls):
                bad.append(f"落点 {f}:{ln} 越界")
                continue
            if not re.search(p2, ls[ln - 1], re.I):
                bad.append(f"落点 {f}:{ln} 上没有 {p2}")
        if got_at == 0:
            bad.append("《方向相反的一类》那一行上一个落点都没抽到")
    print(f"    [i] {p1} → {got1}；{p2} → 产物 {got2p}，真值 {got2t}（合计 {sum(got2t)}）")
    record("A8 AI 词表两类", not bad, "; ".join(bad))


def check_hedge_diminish():
    """§③ 自我削弱口径：显式自我削弱词两侧为 0（没量 ⇒ 不设机判）；弱化词方向相反（明令别用）。

    口径（模式）从文档现取；读数在 5 份 canonical 正文 + 43 份人写 O 奖论文上重算。
    """
    claim(r"自我削弱口径|显式自我削弱词（模式|这一族在本语料")
    hp = find1(r"显式自我削弱词（模式 `([^`]+)`，`grep -o -i -E`）", what="hedge 模式")
    dp = find1(r"模式 `([^`]+)` 这一族在本语料", what="弱化词模式")
    n_red_h, n_true_h, n_paper_h = find1(
        r"\*\*RED 三份合计 (\d+) 次\*\*、\*\*真值两份合计 (\d+) 次\*\*〔本文件复算〕、"
        r"\*\*43 份人写 O 奖论文合计 (\d+) 次\*\*", what="hedge 三处读数")
    want_dt, want_dr = find1(
        r"\*\*真值两份 ([\d.]+)‰\*\* > \*\*RED 三份 ([\d.]+)‰\*\*", what="弱化词两侧密度")
    want_med, want_max = find1(
        r"\*\*43 份人写 43/43 份有\*\*（中位 \*\*(\d+)\*\* 次 / 件，最大 (\d+) 次）", what="弱化词人写分布")

    red, truth = ALL_FILES[:3], ALL_FILES[3:]
    got_red_h = sum(count(hp, body_text(f)) for f in red)
    got_true_h = sum(count(hp, body_text(f)) for f in truth)
    w_red = sum(words(body_text(f)) for f in red)
    w_true = sum(words(body_text(f)) for f in truth)
    got_red_d = sum(count(dp, body_text(f)) for f in red)
    got_true_d = sum(count(dp, body_text(f)) for f in truth)

    texts = [p.read_text(encoding="utf-8", errors="ignore") for p in sorted(HEDGE_PAPERS.rglob("*.md"))]
    got_paper_h = sum(count(hp, t) for t in texts)
    p_d = [count(dp, t) for t in texts]
    got_med = sorted(p_d)[len(p_d) // 2] if p_d else 0
    got_max = max(p_d) if p_d else 0

    bad = []
    for label, want, got in (("RED hedge", n_red_h, got_red_h), ("真值 hedge", n_true_h, got_true_h),
                             ("人写 hedge", n_paper_h, got_paper_h)):
        if int(want) != got:
            bad.append(f"{label} 文档={want} 实测={got}")
    for label, want, got, wd in (("真值弱化词密度", want_dt, got_true_d, w_true),
                                 ("RED 弱化词密度", want_dr, got_red_d, w_red)):
        if round(per_mille(got, wd), 2) != float(want):
            bad.append(f"{label} 文档={want} 实测={per_mille(got, wd):.4f}")
    if int(want_med) != got_med or int(want_max) != got_max:
        bad.append(f"人写弱化词分布 文档中位/最大={want_med}/{want_max} 实测={got_med}/{got_max}")
    if per_mille(got_true_d, w_true) <= per_mille(got_red_d, w_red):
        bad.append("弱化词密度方向不再相反（真值应 > RED）——『明令别用』的理由已变")
    print(f"    [i] hedge RED {got_red_h} / 真值 {got_true_h} / 人写 {got_paper_h}；"
          f"弱化词 真值 {per_mille(got_true_d, w_true):.2f}‰ vs RED {per_mille(got_red_d, w_red):.2f}‰")
    record("A11 自我削弱口径·文档读数自证", not bad, "; ".join(bad))


def check_doc_selfclaim():
    """文档第一行自称的两个数：grep -rn 命中 0、.claude/skills/ 现存 4 个。"""
    want_zero = find1(r"`grep -rn \"mcm-writing-discipline\" \.claude/` 命中 \*\*(\d+)\*\*", what="自称命中数")
    want_dirs = find1(r"`\.claude/skills/` 下现存 (\d+) 个", what="skill 个数")
    n = 0
    for p in SKILLS_DIR.rglob("*"):
        if p.is_file():
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            n += sum(1 for l in txt.splitlines() if "mcm-writing-discipline" in l)
    dirs = sorted(d.name for d in SKILLS_DIR.iterdir() if d.is_dir())
    bad = []
    if n != int(want_zero):
        bad.append(f"grep -rn 命中 文档={want_zero} 实测={n}")
    if len(dirs) != int(want_dirs):
        bad.append(f".claude/skills/ 目录数 文档={want_dirs} 实测={len(dirs)} {dirs}")
    print(f"    [i] grep -rn 命中 {n}；.claude/skills/ = {dirs}")
    record("A9 文档自称的两个数", not bad, "; ".join(bad))


def check_threshold_range():
    """文末「阈值与边界」引的产物密度区间，须与 C2 段算出的极值一致。"""
    claim(r"第三层里只有两个量是")
    t_zero, lo, hi = find1(r"C2\*\*（真值 \*\*([\d.]+)‰\*\* vs 产物 ([\d.]+)–([\d.]+)‰〔本文件复算〕）",
                           what="阈值段区间")
    pattern = find1(r"# 命中数 = 同一区间 \| grep -o -i -E '([^']+)' \| wc -l", what="C2 口径")
    ds = [round(per_mille(count(pattern, body_text(f)), words(body_text(f))), 1) for f in ALL_FILES[:3]]
    bad = []
    if min(ds) != float(lo) or max(ds) != float(hi):
        bad.append(f"产物密度区间 文档={lo}–{hi} 实测={min(ds)}–{max(ds)}")
    tz = [round(per_mille(count(pattern, body_text(f)), words(body_text(f))), 2) for f in ALL_FILES[3:]]
    if any(d != float(t_zero) for d in tz):
        bad.append(f"真值密度 文档={t_zero} 实测={tz}")
    print(f"    [i] 产物密度（一位小数）= {ds}；真值 = {tz}")
    record("A10 文末区间", not bad, "; ".join(bad))


# ---------------------------------------------------------------- §B 出站指针（以文档为输入）

POINTER_RE = re.compile(r"([A-Za-z0-9_.][A-Za-z0-9_./\-]*\.(?:md|html|py|json)):(\d+)(?:[-\u2013](\d+))?")
BARE_RE = re.compile(r"(?<![A-Za-z0-9_./\-:]):(\d+)(?:[-\u2013](\d+))?")

# 落点的"内容期望值"表（脚本常量 = golden）。**指针位置全部来自文档**。
# 键 = 仓库相对路径（POSIX 风格）。值 = (落点内容正则, (文档侧上下文正则, ...), 是否允许空/结构行)
J = "tests/skills/arch-cases/judge.md"
JG = "tests/skills/arch-cases/judge-green.md"
OS1 = "tests/skills/arch-cases/out-S1.md"
OS2 = "tests/skills/arch-cases/out-S2.md"
OS1G = "tests/skills/arch-cases/out-S1-g.md"
OS2G = "tests/skills/arch-cases/out-S2-g.md"
TS1 = "tests/skills/arch-cases/true-S1.md"
TS2 = "tests/skills/arch-cases/true-S2.md"
QCK = ".claude/skills/mcm-abstract/references/quality-checklist.md"
RUB = "tests/skills/mcm-abstract-quality-rubric.md"
INS = "corpus/official/instructions.html"

ANCHORS = {
    (INS, 952): (r"must document any outside sources of information", (r"引用义务",), False),
    (INS, 1162): (r"Discuss any apparent strengths or weaknesses", (r"官方硬要求",), False),
    (JG, 10): (r"未落盘", (r"未落盘",), False),
    (JG, 48): (r"WHO global body-weight references", (r"out-S1-g\.md:75",), False),
    (JG, 69): (r"两侧都恰好命中 62\.8", (r"出处声明",), False),
    (JG, 78): (r"The previous sections have developed the Stair Wear Model", (r"断言了前文的实况",), False),
    (JG, 82): (r"Simulation was used extensively", (r"未读章节实况",), False),
    (JG, 89): (r"Figure 3\.1 about here", (r"LaTeX 注释分隔线",), False),
    (JG, 101): (r"指代错位", (r"正面写明为简并",), False),
    (JG, 103): (r"A5/B3 家族，低", (r"three coefficients",), False),
    (JG, 113): (r"正文全篇零引用", (r"参考文献表两侧都无从判",), False),
    (JG, 131): (r"跨节符号不一致（新产生）", (r"three coefficients",), False),
    (JG, 132): (r"跨节符号不一致（新产生）", (r"产物层可证的事实",), False),
    (JG, 136): (r"### B5 — 时态一致", (r"时态一致", r"本来就好"), False),
    (JG, 138): (r"两侧均 0 —— 该条本次无区分力", (r"本次交付了什么",), False),
    (JG, 140): (r"全部在从句里", (r"从句/完成体",), False),
    (JG, 141): (r"本次交付了什么", (r"本次交付了什么",), False),
    (JG, 142): (r"均不构成跳时态", (r"即结论",), False),
    (JG, 164): (r"任务书给定的下限", (r"天花板",), False),
    (JG, 168): (r"not only\|not just", (r"逐字同宽",), False),
    (JG, 172): (r"10 次 / 6\.4‰", (r"6\.4‰",), False),
    (JG, 183): (r"We therefore discretise", (r"两个来源别混", r"基线订正"), False),
    (JG, 185): (r"The model has two components", (r"两个来源别混", r"极短断言"), False),
    (JG, 189): (r"复现不出来", (r"基线订正",), False),
    (JG, 195): (r"0\.601", (r"0\.601",), False),
    (JG, 196): (r"10\.55", (r"root-TTR",), False),
    (JG, 202): (r"0\.459", (r"0\.601", r"0\.691"), False),
    (JG, 203): (r"10\.55/11\.11", (r"root-TTR",), False),
    (JG, 250): (r"out-S1-g\.md:48", (r"产物层可证的事实",), False),
    (JG, 251): (r"out-S1-g\.md:41", (r"参考文献表两侧都无从判",), False),
    (JG, 257): (r"修一条、退一条", (r"COP",), False),
    (JG, 263): (r"无从核实", (r"同一写手",), False),
    (JG, 264): (r"S1 这一对混了两个变量", (r"同时换了两个变量",), False),
    (JG, 267): (r"本设计给不出", (r"本设计给不出", r"合稿后是否一致"), False),
    (JG, 270): (r"0 与 0 之间无法定阈", (r"0 与 0 之间无法定阈",), False),
    (JG, 277): (r"无从判", (r"同一写手",), False),
    (J, 50): (r"delve / leverage / robust", (r"必须分两类写",), False),
    (J, 101): (r"逐格不同", (r"逐格不同",), False),
    (J, 102): (r"过度声明与同段让步自相矛盾", (r"同段下一句",), False),
    (J, 103): (r"跨节术语漂移", (r"别拿",), False),
    (J, 177): (r"九格不同", (r"九格不同",), False),
    (J, 224): (r"若数据确实不可得", (r"数据确实不可得", r"判据 1"), False),
    (J, 236): (r"not only\|not just", (r"逐字同宽", r"判据"), False),
    (J, 238): (r"强制条款", (r"必须分两类写", r"整体禁用"), False),
    (J, 250): (r"没有对照组", (r"第 7 条",), False),
    (J, 285): (r"0\.691", (r"0\.691", r"区间重叠", r"实测读数"), False),
    (J, 286): (r"最短句", (r"P1b", r"实测读数"), False),
    (J, 290): (r"10\.2%", (r"10\.2%", r"0/50", r"实测读数", r"拆分口径"), False),
    (J, 311): (r"体裁", (r"体裁",), False),
    (RUB, 3): (r"Q1–Q13", (r"Q1–Q13",), False),
    (OS1G, 9): (r"the abbreviation COP", (r"首现不展开",), False),
    (OS1G, 34): (r"archard1953", (r"正文明标补上了",), False),
    (OS1G, 41): (r"published data", (r"仍无引文", r"published data", r"three coefficients"), False),
    (OS1G, 48): (r"\\end\{equation\}", (r"out-S1-g\.md:48",), True),
    (OS1G, 50): (r"\\lambda\$ is the weathering rate constant", (r"定义句在", r"实测\*\*写"), False),
    (OS1G, 75): (r"placeholders", (r"三重标注",), False),
    (OS1G, 79): (r"illustrative values", (r"out-S1-g\.md:79",), False),
    (OS1G, 131): (r"fixes the product", (r"正面写明为简并",), False),
    (OS1, 22): (r"horizontal distance \$p\$", (r"水平距离坐标",), False),
    (OS1, 28): (r"Figure 3\.1 about here", (r"残留一条",), False),
    (OS1, 55): (r"weathering rate constant", (r"风化速率常数",), False),
    (OS1, 65): (r"WHO global body-weight references", (r"反推",), False),
    (OS1, 107): (r"payoff of this section", (r"同段下一句",), False),
    (OS2G, 7): (r"not treated as fixed", (r"仍无引文",), False),
    (OS2G, 15): (r"single rate constant", (r"仍无引文", r"仍在用"), False),
    (OS2G, 19): (r"Stair Wear Model was developed", (r"正文明标补上了",), False),
    (OS2G, 21): (r"Indices of consistency", (r"未读章节实况",), False),
    (OS2, 3): (r"The previous sections have developed", (r"断言了前文的实况",), False),
    (OS2, 23): (r"we set out to give archaeologists", (r"断言了前文的实况",), False),
    (QCK, 30): (r"Q7 家族「结果没出来就显式标缺」（共同项 = `纪律 A1`）", (r"Q7 家族",), False),
    (QCK, 44): (r"Q12 措辞克制（共同项 = `纪律 C1`）", (r"Q12",), False),
    (QCK, 54): (r"Q9 数字必须自洽（共同项 = `纪律 A5`）", (r"Q9",), False),
    (QCK, 65): (r"摘要自身不许前后打架", (r"摘要自身不许前后打架",), False),
    (QCK, 80): (r"Q8 数字与具名归属都要能回指正文（共同项 = `纪律 A2`）", (r"Q8",), False),
    (TS1, 46): (r"comprehensive Wear Volume Model", (r"漏了",), False),
    (TS1, 80): (r"Moreover", (r"模板化过渡词表",), False),
    (TS2, 18): (r"Comprehensive Integration of Factors", (r"漏了",), False),
}

# **区间落点的止行登记表（X7）**。键 = `(仓库相对路径, 起行)`；值 = 文档**允许写的止行集合**。
# 修复轮 3 实测：改 `judge-green.md:183-186` → `:183-185` **仍然绿**——因为旧实现只拿止行
# **放宽搜索窗口**（`hi = max(ends)`），止行本身**从不参与核验**。
# 现在两条硬规则：
#   ① 登记在表的键：文档现取的每一个止行都必须落在允许集合里，否则红；
#   ② **没**登记在表的键：文档不许写成区间（现取的止行必须等于起行），否则红
#      ⇒ 新引入的区间形状会立刻暴露，不必等有人想起来登记。
RANGE_ENDS = {
    (J, 50): (51,),
    (JG, 48): (51,), (JG, 78): (81,), (JG, 82): (83,), (JG, 89): (92,), (JG, 101): (103,),
    (JG, 113): (123,), (JG, 131): (134,), (JG, 136): (142,),
    (JG, 138): (138, 140, 141),          # 同一处被引三次：`:138-141` / `:138-140` / `:138`
    (JG, 183): (183, 186), (JG, 203): (203, 206), (JG, 264): (265,),
    (OS1, 65): (77,), (TS2, 18): (19,),
    (QCK, 30): (34,), (QCK, 44): (52,), (QCK, 54): (57,), (QCK, 65): (67, 72),
}

# 空行/纯结构行的判定：这些不是"内容"，指针落在这里等于没落
STRUCTURAL_RE = re.compile(
    r"^\s*(?:\\end\{[A-Za-z*]+\}|\\begin\{[A-Za-z*]+\}|\\hline\b[^\n]*|-{3,}|\|[\s|:.\\-]*\||`{3,})\s*$")


def resolve(name):
    """把文档里写的文件名解析成真实路径；解析不了返回 None（**不抛异常**）。"""
    if "/" in name:
        p = ROOT / name.replace("\\", "/")
        return p if p.exists() else None
    if name == "quality-checklist.md":
        return QCK_PATH if QCK_PATH.exists() else None
    if name == "mcm-abstract-quality-rubric.md":
        return RUBRIC if RUBRIC.exists() else None
    p = CASES / name
    return p if p.exists() else None


def relkey(path):
    """解析成"仓库相对路径"作为锚点键（文档里写短名还是全路径都能对上同一把钥匙）。"""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


QCK_PATH = ROOT / QCK


def extract_pointers(text_lines=None):
    """**从文档里**抽出全部出站指针。返回 (doc_line, 文件串, 起行, 止行)。"""
    ls = DOC_LINES if text_lines is None else text_lines
    out = []
    for i, line in enumerate(ls, 1):
        for m in POINTER_RE.finditer(line):
            out.append((i, m.group(1), int(m.group(2)),
                        int(m.group(3)) if m.group(3) else int(m.group(2))))
    return out


def check_bare_pointers():
    """B1：文档里不许有裸 `:NN`（不写文件名的指针）。"""
    bad = []
    for i, line in enumerate(DOC_LINES, 1):
        # ⚠️ 不要剥反引号：裸指针本来就写在反引号里（`` `:257` ``），剥掉就永远抓不到。
        stripped = POINTER_RE.sub(" ", line)
        for m in BARE_RE.finditer(stripped):
            bad.append(f"doc:{i} 裸指针 :{m.group(1)}")
    if bad:
        print("    " + "\n    ".join(bad[:20]))
    record("B1 裸指针零容忍", not bad,
           ("文档里有裸 `:NN` 指针（无法判定归哪个文件，M-5 明令补全文件名）：" + "; ".join(bad[:8]))
           if bad else "")


def check_outbound_pointers(verbose=False):
    """B2：文档里**每一条**出站指针，回原文件逐条核（结构 + 内容 + 文档侧上下文）。"""
    ptrs = extract_pointers()
    # **按解析后的（文件, 起行）归并**：同一个文件在文档里既写短名又写全路径，算**一个**落点。
    by_key = {}
    for dl, name, a, b in ptrs:
        path = resolve(name)
        k = (relkey(path) if path else name, a)
        by_key.setdefault(k, {"lines": set(), "ends": [], "names": set()})
        by_key[k]["lines"].add(dl)
        by_key[k]["ends"].append(b)
        by_key[k]["names"].add(name)

    n_err = n_oob = n_bad = n_unreg = n_blank = n_end = 0
    bad = []
    rows = []
    for key, meta in sorted(by_key.items()):
        a = key[1]
        doc_lines = sorted(meta["lines"])
        # X7：**区间两端都核**（含 `NN-MM` 与 `NN–MM` 两种破折号——POINTER_RE 已同时认两种）
        ends = sorted(set(meta["ends"]))
        allowed = RANGE_ENDS.get(key, (a,))
        off = [e for e in ends if e not in allowed]
        if off:
            n_end += 1
            bad.append(f"{key[0]}:{a}-{off[0]} **区间止行**未登记（该键登记的止行 = {allowed}"
                       f"，其余 {ends}；doc:{doc_lines}）")
        anchor = ANCHORS.get(key)
        path = ROOT / key[0]
        ls = _lines(path)
        # 诊断顺序：**越界 → 空/结构行 → 未登记 → 内容 → 上下文**（先报最硬的事实）
        if a > len(ls) or a < 1:
            n_oob += 1
            bad.append(f"{key[0]}:{a} 行号越界（该文件 {len(ls)} 行，doc:{doc_lines}）")
            rows.append((key[0], a, doc_lines, "越界"))
            continue
        allow_struct = anchor[2] if anchor else False
        first = ls[a - 1]
        if (not first.strip() or STRUCTURAL_RE.match(first)) and not allow_struct:
            n_blank += 1
            bad.append(f"{key[0]}:{a} 落点是空行/纯结构行（doc:{doc_lines}）：{first.strip()[:40]!r}")
            rows.append((key[0], a, doc_lines, "空/结构行"))
            continue
        if anchor is None:
            n_unreg += 1
            bad.append(f"{key[0]}:{a} 未登记的落点（doc:{doc_lines}）——ANCHORS 表里没有它")
            rows.append((key[0], a, doc_lines, "未登记"))
            continue
        want_text, hints, _ = anchor
        hi = max(min(e, len(ls)) for e in meta["ends"])
        text = "\n".join(ls[a - 1:hi])
        if not re.search(want_text, text):
            n_bad += 1
            bad.append(f"{key[0]}:{a} 内容不符（doc:{doc_lines}）：要 {want_text!r}")
            rows.append((key[0], a, doc_lines, "内容不符"))
            continue
        ctx_bad = [dl for dl in doc_lines
                   if not any(re.search(h, DOC_LINES[dl - 1]) for h in hints)]
        if ctx_bad:
            n_bad += 1
            bad.append(f"{key[0]}:{a} 文档侧上下文不符（doc:{ctx_bad} 那几行不是在说这条落点）")
            rows.append((key[0], a, doc_lines, "文档上下文不符"))
            continue
        rows.append((key[0], a, doc_lines, "区间止行" if off else "OK"))

    # 反向：登记但文档里没人指向的落点 = 指针被删了
    orphans = sorted(set(ANCHORS) - set(by_key))
    for k in orphans:
        bad.append(f"{k[0]}:{k[1]} 登记了却没有任何文档指针指向它（指针被删？）")

    n_land = len(by_key)
    n_ok = sum(1 for r in rows if r[3] == "OK")
    n_bare = sum(len(list(BARE_RE.finditer(POINTER_RE.sub(" ", l)))) for l in DOC_LINES)
    PSTATS.clear()
    PSTATS.update(ptrs=len(ptrs), land=n_land, ok=n_ok, bare=n_bare, oob=n_oob,
                  blank=n_blank, unreg=n_unreg, bad=n_bad, end=n_end, orphans=len(orphans))
    print(f"    [i] 出站指针 {len(ptrs)} 条 · 去重落点 {n_land} 个 · 覆盖 {n_ok}/{n_land}"
          f"（{n_ok / n_land * 100:.0f}%）"
          f" · 解析失败 {n_err} · 越界 {n_oob} · 空/结构行 {n_blank} · 未登记 {n_unreg}"
          f" · 内容或上下文不符 {n_bad} · **区间止行不符 {n_end}** · 孤儿 {len(orphans)}")
    if verbose:
        for k, a, dl, st in rows:
            print(f"      [{st:<8}] doc:{str(dl):<14} {k}:{a}")
    record(f"B2 出站指针全扫（{len(ptrs)} 条 / {n_land} 落点）", not bad, "; ".join(bad[:12]))


def check_inbound_pointers():
    """B3：`arch-green-evidence.md` 指向本文档的入站行号，回本文档核内容（F-4 回归守卫）。

    入站指针从**证据文件**里现取（`docs/mcm-writing-discipline.md` 之后同一行的裸 `:NN`），
    不写死行号；每条入站指针都要在 `INBOUND_ANCHORS` 里有登记内容期望。
    """
    bad = []
    ev_lines = _lines(EVIDENCE)
    ev_key = relkey(EVIDENCE)
    found = 0
    for ev_re, expects, label in INBOUND_TABLE:
        ev_no = next((i for i, l in enumerate(ev_lines, 1) if re.search(ev_re, l)), None)
        if ev_no is None:
            bad.append(f"入站锚点行的文字丢了（应在证据文件里出现 {ev_re!r}）")
            continue
        line = ev_lines[ev_no - 1]
        tail = line[line.rindex("mcm-writing-discipline.md"):]
        ptrs = [(int(m.group(1)), int(m.group(2)) if m.group(2) else int(m.group(1)))
                for m in BARE_RE.finditer(tail)]
        found += len(ptrs)
        if len(ptrs) != len(expects):
            bad.append(f"{ev_key}:{ev_no} 那条 {label} 上抽到 {len(ptrs)} 个入站指针，"
                       f"登记表里写了 {len(expects)} 个（改证据文件时须同步）")
            continue
        for (a, b), (want, what) in zip(ptrs, expects):
            if a > len(DOC_LINES) or b > len(DOC_LINES) or a < 1:
                bad.append(f"{ev_key}:{ev_no} → doc:{a}-{b} 越界（本文档 {len(DOC_LINES)} 行）")
                continue
            if want is None:      # 历史行号：只核界内，不核内容（它记的是旧 commit 的位置）
                print(f"    [i  ] {ev_key}:{ev_no} → doc:{a}-{b}  {what}")
                continue
            if re.search(want, "\n".join(DOC_LINES[a - 1:b])):
                print(f"    [OK ] {ev_key}:{ev_no} → doc:{a}-{b}  {what}")
            else:
                bad.append(f"{ev_key}:{ev_no} → doc:{a}-{b} 内容不符：要 {want!r}（{what}）")
    if found == 0:
        bad.append("从证据文件里一条指向本文档的入站行号都没抽到（锚点丢失）")
    record("B3 入站指针锚（F-4 回归守卫）", not bad, "; ".join(bad))


# 入站指针的内容期望。**键是"证据文件里那一行的文字"**（不是行号，免得行号抄成常量）；
# 值是按**出现顺序**排列的期望表：`(本文档里的内容正则, 标签)`；`None` = 历史行号（只核界内）。
INBOUND_TABLE = [
    (r"见 `docs/mcm-writing-discipline\.md` §③ C3",
     [(r"基线订正（2026-09-27 由 GREEN 轮复量）", "§③ C3 基线订正（活动指针）")],
     "C3 基线订正"),
    (r"→ `B6 · 跨节一致性",
     [(r"B6 · 跨节一致性", "B6 整条（活动指针）"),
      (None, "历史行号 :61–64（`c6f77f7` 时的位置，只核界内）")],
     "B6"),
    (r"→ `A3` 下的「规则边界（必须写清）」",
     [(r"规则边界（必须写清）", "A3 规则边界（活动指针）"),
      (None, "历史行号 :37–38（`c6f77f7` 时的位置，只核界内）")],
     "A3 规则边界"),
]
INBOUND_ANCHORS = {}       # 由 _load_inbound_anchors() 填充，供 C4 守卫计数


def _load_inbound_anchors():
    ev = _lines(EVIDENCE)
    for ev_re, expects, label in INBOUND_TABLE:
        for i, line in enumerate(ev, 1):
            if re.search(ev_re, line):
                INBOUND_ANCHORS[(relkey(EVIDENCE), i)] = (expects, label)
                break


# ---------------------------------------------------------------- §C 九条修复的回归守卫

def _doc_has(pattern):
    return bool(re.search(pattern, DOC_TEXT, re.S))


def guard(fix, ok, detail):
    """守卫登记口；**绿的时候不打印 detail**（detail 是失败诊断）。

    每次调用都把 `fix` 记进 `GUARD_SEEN`：E0 拿它和**常量** `EXPECTED_GUARD_NAMES` 对账
    —— 修复轮 3 的 `GUARDS: 8/8 在场且为绿` 就是"分母自计"（删了调用它自己把分母也减 1）。
    """
    GUARD_SEEN.append(fix)
    record(f"{fix} 回归守卫", ok, detail if not ok else "")


def check_guards():
    # F-1：五个数（连 -i 一起）—— A5 就是它的守卫，这里只做存在性交叉断言
    five = re.findall(r"`out-S1` \*\*7\.96‰\*\*、`out-S2` \*\*13\.27‰\*\*、`out-S2-p` \*\*13\.72‰\*\*、"
                      r"真值 \*\*7\.80‰ / 2\.82‰\*\*", DOC_TEXT)
    off = re.search(r"`4\.55 / 8\.29 / 7\.48 / 2\.93 / 0\.00‰` 是\*\*大小写敏感\*\*", DOC_TEXT)
    guard("C1 F-1", len(five) == 1 and bool(off),
          "doc 里找不到带 -i 口径的 7.96/13.27/13.72/7.80/2.82 与《4.55…是大小写敏感》的登记")

    # F-2：别拿 judge.md:103 当出处（判词那一行的 S1 列确记 0）
    j103 = _lines(CASES / "judge.md")[102]
    guard("C2 F-2", _doc_has(r"别拿 `judge\.md:103` 当这条的出处") and "跨节术语漂移" in j103
          and re.search(r"\|\s*跨节术语漂移（`p` 的语义）\s*\|\s*0\s*\|", j103) is not None,
          "doc 少了《别拿 judge.md:103 当出处》的登记，或 judge.md:103 的 S1 列不再是 0")

    # F-3：root-TTR 的四个读数/GREEN 落在真值一带
    j196 = _lines(CASES / "judge-green.md")[195]
    j203 = _lines(CASES / "judge-green.md")[202]
    guard("C3 F-3",
          _doc_has(r"GREEN 两份是 10\.55 / 11\.11——就落在真值那一带里")
          and "10.55" in j196 and "11.11" in j196 and "10.55/11.11 ≈ 真值 10.71/11.13" in j203
          and _doc_has(r"等长对照后更是直接翻掉")
          and _doc_has(r"（旧结论说它\"反向指标\"，现改判）"),
          "doc 少了 root-TTR 的《GREEN 落在真值一带 + 等长对照》读法，或判词 :196/:203 的两处原文变了")

    # F-4 由 B3 守；这里断言"三处入站指针都在盘上"
    guard("C4 F-4", len(INBOUND_ANCHORS) >= 3,
          f"入站锚点只找到 {len(INBOUND_ANCHORS)} 条（应 3 条）")

    # F-5：口径双向守卫 —— 6 个 alternation，且与两份源判词逐字同宽；窄口径必须仍是 4 个
    wide = find1(r"\*\*模式\*\* = `([^`]+)`（`grep -o -i -E`", what="C2 宽口径")
    code = find1(r"# 命中数 = 同一区间 \| grep -o -i -E '([^']+)' \| wc -l", what="C2 口径")
    j236 = _lines(CASES / "judge.md")[235]
    jg168 = _lines(CASES / "judge-green.md")[167]
    six = ["rather than", "not merely", "not only", "not just", "precisely", "exactly"]
    narrow = "rather than|not merely|precisely|exactly"
    parts_wide = wide.split("|")
    parts_code = code.split("|")
    m236 = re.search(r"`\(([^)]+)\)`", j236)
    m168 = re.search(r"正则 `([^`]+)`", jg168)
    bad5 = []
    if parts_wide != six:
        bad5.append(f"doc:107 的口径 = {parts_wide}，应恰为 6 个 {six}")
    if parts_code != six:
        bad5.append(f"doc:116 代码块口径 = {parts_code}，应恰为 6 个 {six}")
    if not (m236 and m236.group(1).split("|") == six):
        bad5.append(f"judge.md:236 公式 = {m236.group(1).split('|') if m236 else None}，应恰为 6 个")
    if not (m168 and m168.group(1).split("|") == six):
        bad5.append(f"judge-green.md:168 正则 = {m168.group(1).split('|') if m168 else None}，应恰为 6 个")
    if wide == narrow:
        bad5.append("doc:107 的口径与 A3 里的窄口径（4 个）相同——加宽被回退了")
    guard("C5 F-5", not bad5,
          "; ".join(bad5) or "")

    # F-6：两个来源别混 + 三条极短断言逐字
    jg185 = _lines(CASES / "judge-green.md")[184]
    three = ["The model has two components.", "Real use is rarely so steady.",
             "Wear on a staircase is unavoidable."]
    bad6 = []
    if not _doc_has(r"⚠️ \*\*两个来源别混\*\*"):
        bad6.append("doc 少了《两个来源别混》的分列句")
    if not _doc_has(r"3 与 5 是 \*\*GREEN 轮\*\*判者复量 RED 产物得的"):
        bad6.append("doc 少了《3 与 5 出自 GREEN 轮》的来源分列")
    if not _doc_has(r"6 是 \*\*RED 轮\*\*的读数"):
        bad6.append("doc 少了《6 出自 RED 轮》的来源分列")
    for s in three:
        if s not in jg185:
            bad6.append(f"judge-green.md:185 上不再有 {s!r}")
        elif s not in DOC_TEXT:
            bad6.append(f"doc 上没有逐字引 {s!r}")
    guard("C6 F-6", not bad6, "; ".join(bad6))

    # F-7：§6.2 / 不在 §5
    j = _lines(CASES / "judge.md")
    def section_of(n):
        for i in range(n - 1, -1, -1):
            m = re.match(r"^#{2,3}\s+([\d.]+)", j[i])
            if m:
                return m.group(1)
        return None
    bad7 = []
    for n in (285, 286, 290):
        sec = section_of(n)
        if sec != "6.2":
            bad7.append(f"judge.md:{n} 现在落在 §{sec}（文档说是 §6.2）")
    if section_of(236) != "5.2":
        bad7.append(f"judge.md:236 现在落在 §{section_of(236)}（文档说它在 §5.2）")
    if not _doc_has(r"\*\*§6\.2\*\*——`### 6\.2 七个候选代理量的实测分布`，`judge\.md:285`"):
        bad7.append("doc 的 §6.2 落点句被改掉了")
    if not _doc_has(r"⚠️ \*\*不在 §5\*\*"):
        bad7.append("doc 少了《不在 §5》的更正")
    guard("C7 F-7", not bad7, "; ".join(bad7))

    # F-8：B5 的最小可执行读法 + 强度来源如实
    jg138 = _lines(CASES / "judge-green.md")[137]
    bad8 = []
    if not _doc_has(r"\*\*最小可执行读法\*\*（落点 = `judge-green\.md:138-141`"):
        bad8.append("doc 的 B5《最小可执行读法》被删/被改回 138-140")
    if "两侧均 0 —— 该条本次无区分力" not in jg138:
        bad8.append("judge-green.md:138 不再是《两侧均 0 —— 该条本次无区分力》")
    if not _doc_has(r"强度读法：上面这条\"必须统一时态\"是〔本文件自定〕的强度"):
        bad8.append("doc 少了《强度是〔本文件自定〕》的来源如实标注")
    if not _doc_has(r"本节的叙述主动词必须统一时态"):
        bad8.append("doc 少了 B5 的最小可执行读法正文")
    guard("C8 F-8", not bad8, "; ".join(bad8))

    # I-1（本轮的 Important）：口径叙述必须是**准确的两处改动**，且两处改动各动多少要可复算
    badI1 = []
    LIT_THIS = "This " + chr(92) + "w+"      # 文档与 grep 口径里那个"反斜杠 w 加号"的字面串
    ex = [count("exactly", body_text(f)) for f in ALL_FILES]
    th = [count(r"This \w+", body_text(f)) for f in ALL_FILES]
    LIT_PAIR = "**① 去掉 `exactly`、② 加上 `This " + chr(92) + "w+`**"
    LIT_TWO = "**相对当时那条 canonical 四 alternation（`rather than|not merely|precisely|exactly`）是两处改动**"
    if LIT_PAIR not in DOC_TEXT or LIT_TWO not in DOC_TEXT or LIT_THIS not in DOC_TEXT:
        badI1.append("doc 少了《① 去掉 exactly、② 加上 This \w+》这条**两处改动**的准确叙述"
                     "（三个字面串都要在：改动清单 / 相对四 alternation / This \w+ 本身）")
    if not _doc_has(r"有 \*\*3 次\*\*命中、\*\*其余四份各 0 次\*\*"):
        badI1.append("doc 少了《exactly 有 3 次命中、其余四份各 0 次》这个可测事实")
    if ex != [3, 0, 0, 0, 0]:
        badI1.append(f"exactly 五份实测 {ex}，文档说的 3/0/0/0/0 对不上")
    if th != [7, 9, 7, 8, 1]:
        badI1.append(f"This-\w+ 五份实测 {th}，文档说的 +7/+9/+7/+8/+1 对不上")
    guard("C10 I-1", not badI1, "; ".join(badI1))

    # F-9：定义句实测在 :50；判词的 :48 只作"错值登记"出现
    os1g = _lines(CASES / "out-S1-g.md")
    bad9 = []
    if r"\end{equation}" != os1g[47].strip():
        bad9.append("out-S1-g.md:48 不再是 \\end{equation}（判词那处 off-by-2 的另一半变了）")
    if "is the weathering rate constant" not in os1g[49]:
        bad9.append("out-S1-g.md:50 上不再是 λ 的定义句")
    if not _doc_has(r"（定义句在 `out-S1-g\.md:50`）"):
        bad9.append("doc 的 B6 事实句被改回去了（应写 out-S1-g.md:50）")
    if not _doc_has(r"本行按\*\*实测\*\*写 `out-S1-g\.md:50`"):
        bad9.append("doc 少了《本行按实测写 :50》的登记")
    if not _doc_has(r"off-by-2，\*\*已登记\*\*在 `tests/skills/arch-green-evidence\.md` 的编者按"):
        bad9.append("doc 少了 off-by-2 已登记的说明")
    guard("C9 F-9", not bad9, "; ".join(bad9))


# ---------------------------------------------------------------- §E 机器守卫（修复轮 4）

def _guard_green(name):
    """该守卫**在场且为绿**吗（E1/coverage 都用它判"标记所指的守卫真的在跑"）。"""
    return any(n == f"{name} 回归守卫" and ok for n, ok, _ in RESULTS)


def check_guard_roster():
    """E0（M-1）：**分母钉死** —— 实际被调用的 guard() 名册必须与**常量**逐名相等。

    修复轮 3 实测：删掉自检件里任一个 `guard(...)` 调用 ⇒ 它打印 `GUARDS: 8/8 在场且为绿`
    + `RESULT: PASS`（分母也跟着减 1 了）。现在期望数是常量，删了谁立刻红。
    """
    want, got = list(EXPECTED_GUARD_NAMES), list(GUARD_SEEN)
    missing = [n for n in want if n not in got]
    extra = [n for n in got if n not in want]
    dup = sorted({n for n in got if got.count(n) > 1})
    bad = []
    if missing:
        bad.append("名册里的守卫**没有被调用**（guard(...) 调用被删？）：" + ", ".join(missing))
    if extra:
        bad.append("有守卫没登记进 EXPECTED_GUARD_NAMES：" + ", ".join(extra))
    if dup:
        bad.append("守卫被登记了多次：" + ", ".join(dup))
    if len(want) != len(got):
        bad.append(f"期望 {len(want)} 条，实际调用了 {len(got)} 条")
    record(f"E0 守卫名册（期望 = 常量 {len(want)} 条 / 实际 {len(got)} 条）", not bad, "; ".join(bad))


def check_e1_header_selfclaim():
    """E1（I-2 核心）：文档头部那**四句覆盖自陈**，由本脚本自己重算并与文档**现取的字面值**比对。"""
    claim(r"覆盖自陈（必须与实跑一致")
    w_ptr, w_land = find1(r"本文件共 \*\*(\d+) 条\*\*出站指针、去重 \*\*(\d+) 个\*\*",
                          what="头部自陈·条数/落点")
    w_ok, w_den, w_pct = find1(r"逐条回原文件核过 (\d+)/(\d+) = (\d+)%", what="头部自陈·覆盖率")
    w_bare = find1(r"裸 `:NN` 指针 (\d+) 条", what="头部自陈·裸指针")
    bad = []
    if not PSTATS:
        bad.append("B2 没有先跑，拿不到指针面实测数")
    else:
        g = PSTATS
        for label, want, have in (("出站指针条数", w_ptr, g["ptrs"]), ("去重落点数", w_land, g["land"]),
                                  ("覆盖率分子", w_ok, g["ok"]), ("覆盖率分母", w_den, g["land"]),
                                  ("裸 `:NN` 指针数", w_bare, g["bare"])):
            if int(want) != have:
                bad.append(f"{label} 文档={want} 实测={have}")
        pct = round(g["ok"] / g["land"] * 100) if g["land"] else 0
        if pct != int(w_pct):
            bad.append(f"覆盖率百分数 文档={w_pct}% 实测={pct}%")
        print(f"    [i] 头部自陈逐项复算：指针 {g['ptrs']} 条 · 落点 {g['land']} 个 · "
              f"覆盖 {g['ok']}/{g['land']} = {pct}% · 裸 {g['bare']} 条 · 越界 {g['oob']} · "
              f"未登记 {g['unreg']} · 内容/上下文不符 {g['bad']} · 区间止行 {g['end']} · 孤儿 {g['orphans']}")
    guard("E1 头部自陈", not bad, "; ".join(bad))


def check_e4_tolerance():
    """E4：文档说的 `±Npp` 必须等于**脚本里实际用的** `TOLERANCE_PP`。"""
    w = find1(r"这一项带 \*\*±(\d+(?:\.\d+)?)pp\*\* 容差", what="±Npp 容差自述")
    bad = []
    if float(w) != TOLERANCE_PP:
        bad.append(f"文档说 ±{w}pp，脚本常量 TOLERANCE_PP = ±{TOLERANCE_PP:g}pp")
    guard("E4 容差自述", not bad, "; ".join(bad))


def check_e5_caliber_flags():
    """E5：「**只动模式这一个变量**」的可测形态 —— A5 那行现取的 `grep` 标志必须与 canonical 逐字相同。"""
    canon = find1(r"# 命中数 = 同一区间 \| grep -o (-i )?-E", what="C2 口径标志")
    a5 = find1(r"（模式 `[^`]+`，`grep -o (-i )?-E`", what="A5 标志")
    bad = []
    if (canon or "").strip() != (a5 or "").strip():
        bad.append(f"A5 那行的 grep 标志 = {(a5 or '').strip()!r}，canonical 口径 = "
                   f"{(canon or '').strip()!r} —— 已经不是《只动模式这一个变量》")
    if "只动模式这一个变量" not in DOC_TEXT:
        bad.append("doc 少了《只动模式这一个变量》那句")
    guard("E5 口径同宽", not bad, "; ".join(bad))


def check_e6_truth_zero():
    """E6：「真值基线 0 ⇒ 非零即提请复核」的**前提**当场重算。"""
    pattern = find1(r"# 命中数 = 同一区间 \| grep -o -i -E '([^']+)' \| wc -l", what="C2 口径")
    hits = [count(pattern, body_text(f)) for f in ALL_FILES[3:]]
    bad = []
    if any(h != 0 for h in hits):
        bad.append(f"两份真值实测命中 {hits}，不再全为 0 ⇒《真值基线 0 ⇒ 非零即提请复核》的前提失效")
    if "真值基线 0 ⇒ 非零即提请复核" not in DOC_TEXT:
        bad.append("doc 少了《非零即提请复核》那句")
    guard("E6 基线非零", not bad, "; ".join(bad))


CHECKLIST_ITEM_RE = re.compile(r"^(?:★ |- )\*\*(?!配方|怎么查|依据|附注)")


def check_e7_checklist_rows():
    """E7：文档说那份自查清单有 15 条 —— 当场点数它的顶层条目行。"""
    w = int(find1(r"逐条自查清单\*\* = `[^`]+`，\*\*(\d+) 条\*\*", what="自查清单条数"))
    rows = [l for l in _lines(QCK_PATH) if CHECKLIST_ITEM_RE.match(l)]
    bad = [] if len(rows) == w else [f"文档说 {w} 条，实测顶层条目行 {len(rows)} 条"]
    print(f"    [i] {QCK} 顶层条目行 = {len(rows)} 条（文档说 {w} 条）")
    guard("E7 自查清单条数", not bad, "; ".join(bad))


def check_e8_thisx():
    """E8：`This \\w+` 五份的 `+7/+9/+7/+8/+1` 与 `exactly` 的 `3 次` —— **从文档现取**再重跑。"""
    five = [int(x) for x in find1(
        r"⇒ 五份各 \*\*\+(\d+) / \+(\d+) / \+(\d+) / \+(\d+) / \+(\d+)\*\*", what="This \\w+ 五份")]
    ex_n = int(find1(r"有 \*\*(\d+) 次\*\*命中、\*\*其余四份各 0 次\*\*", what="exactly 命中数"))
    got_th = [count(r"This \w+", body_text(f)) for f in ALL_FILES]
    got_ex = [count("exactly", body_text(f)) for f in ALL_FILES]
    bad = []
    if got_th != five:
        bad.append(f"This \\w+ 五份 文档={five} 实测={got_th}")
    if got_ex != [ex_n, 0, 0, 0, 0]:
        bad.append(f"exactly 五份 文档={[ex_n, 0, 0, 0, 0]} 实测={got_ex}")
    guard("E8 This-X 复算", not bad, "; ".join(bad))


# **已登记的方向性断言**（X1）。⚠️ 只覆盖这几条 —— 本脚本判不了语义。
# 每条：锚点（在哪一行）+ 方向词（必须出现）+ 反义词（**不得**出现）
#       + 可选：把这行引的判词列值当场重算（比关键词强）。
POLARITY = [
    {"label": "P1 `judge.md:103` 的引用方向（复核 X1 的原案）",
     "anchor": r"别拿 `judge\.md:103` 当这条的出处",
     "must": r"反证", "forbid": r"支撑",
     "doc_num": r"其 S1 列记 \*\*(\d+)\*\*",
     "src": ("judge.md", 103, r"\|\s*跨节术语漂移（`p` 的语义）\s*\|\s*(\d+)\s*\|"),
     "why": "该行说 judge.md:103 的 S1 列记 0、引它反而**反证**本条；把 0 改成 1、「反证」改成「支撑」即 FAIL"},
    {"label": "P2 B6 的跨节不一致断言",
     "anchor": r"不一致换了个形态",
     "must": r"仍然存在", "forbid": r"已消除|已经一致|不再存在",
     "doc_num": None, "src": None,
     "why": "该行断言跨节不一致**仍然存在**；改成「已消除/已经一致」即 FAIL"},
]


def check_e9_polarity():
    """E9（X1）：对**已登记的方向性断言**核极性方向（并尽量把它引的判词列值当场重算）。"""
    bad, n = [], 0
    for p in POLARITY:
        lines = [l for l in DOC_LINES if re.search(p["anchor"], l)]
        if not lines:
            bad.append(f"极性断言锚点丢失（{p['label']}）：{p['anchor']!r}")
            continue
        n += 1
        for l in lines:
            if not re.search(p["must"], l):
                bad.append(f"{p['label']}：那行上找不到方向词 {p['must']!r}（{p['why']}）")
            if p["forbid"] and re.search(p["forbid"], l):
                bad.append(f"{p['label']}：那行上出现了**反向**词 {p['forbid']!r} —— 断言被写反了")
            if p["doc_num"] and p["src"]:
                f, ln, rx = p["src"]
                m = re.search(p["doc_num"], l)
                s = re.search(rx, _lines(CASES / f)[ln - 1])
                if not m or not s:
                    bad.append(f"{p['label']}：列值解析不出来（doc 侧 {p['doc_num']!r} / "
                               f"源 {f}:{ln} 侧 {rx!r}）")
                elif m.group(1) != s.group(1):
                    bad.append(f"{p['label']}：doc 说该行记 {m.group(1)}，{f}:{ln} 实测 "
                               f"{s.group(1)} —— 数字与方向一起错了")
    print(f"    [i] 已登记的方向性断言 {n}/{len(POLARITY)} 条核过极性（**只覆盖登记的这几条**）")
    guard("E9 方向性断言极性", not bad, "; ".join(bad))


CN_NUM = {"两": 2, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6}


def check_e10_missing_count():
    """E10：**基数句**（如"要给出边界，还缺两样"）—— 核"样数"与实际列出的项数一致。**只核基数。**"""
    hits = [(i, l) for i, l in enumerate(DOC_LINES, 1) if "要给出边界，还缺" in l]
    bad = []
    if len(hits) != 1:
        bad.append(f"《要给出边界，还缺 N 样》那句出现 {len(hits)} 次（应恰 1 次）")
    for i, l in hits:
        m = re.search(r"还缺(两|二|三|四|五|六|\d+)\s*(?:样|项|条)", l)
        if not m:
            bad.append(f"doc:{i} 的“还缺 N 样”解析不出来")
            continue
        want = CN_NUM.get(m.group(1), None)
        want = int(m.group(1)) if want is None else want
        got = len(re.findall(r"[①②③④⑤⑥]", l))
        if want != got:
            bad.append(f"doc:{i} 说“还缺 {want} 样”，该行实际列了 {got} 项")
        print(f"    [i] doc:{i} 缺项基数：declared={want} · listed={got}（**只核基数，不核内容**）")
    guard("E10 缺项基数", not bad, "; ".join(bad))


RUBRIC_Q_RE = re.compile(r"^### Q(\d+)\b")


def check_e11_rubric_count():
    """E11（修复轮 5 · I-2 补登记）：文档说那份判分表 `Q1–Q13 共 13 条` —— 当场点数它的顶层 `### Q<n>` 行。

    这条是复核 §4.3 点名的"**名册外的单元**"之一（`doc:166`；复核实测：把 13 改成 14 ⇒ 全绿，无人守）。
    """
    ws = [int(x) for x in re.findall(r"\*\*Q1\u2013Q13 共 (\d+) 条\*\*", DOC_TEXT)]
    if not ws:
        raise LookupError("文档里找不到《Q1–Q13 共 N 条》那句")
    qs = [int(m.group(1)) for m in (RUBRIC_Q_RE.match(l) for l in _lines(RUBRIC)) if m]
    bad = []
    if len(set(ws)) != 1:
        bad.append(f"文档里《Q1–Q13 共 N 条》出现 {len(ws)} 处、值不一致：{ws}（同一个数不许有两份）")
    if ws[0] != len(qs):
        bad.append(f"文档说判分表 {ws[0]} 条，实测顶层 `### Q<n>` 行 {len(qs)} 条")
    elif qs != list(range(1, ws[0] + 1)):
        bad.append(f"判分表的 Q 编号不是 1..{ws[0]} 连续：{qs}")
    print(f"    [i] {RUBRIC.relative_to(ROOT)} 顶层 `### Q<n>` 行 = {len(qs)} 条（Q1–Q{max(qs) if qs else 0}）")
    guard("E11 判分表条数", not bad, "; ".join(bad))


def check_e12_guard_bodies():
    """E12（修复轮 5 · M-1 残余）：守卫**体**不许被掏空 —— 对**本检查器自己的源码**做 AST。

    机械约束（三条都要成立）：
      ① 每个 `guard(...)` 调用的实参 ≥ 3 个；
      ② 第 2 个实参（期望值 `ok`）**不许是字面 `True`** —— 恒真 ⇒ 名册还在、断言没了；
      ③ 第 3 个实参（失败诊断 `detail`）**不许是空字面量**（`""` / `f""` / `None`）。
    复核 M-1（`G5d`）实测的那一手 `guard("E4 容差自述", True, "")`（名册 20/20 + `RESULT: PASS`）由本条堵死。
    ⚠️ 为什么必须是 AST、不能是运行时检查：`not bad`（`bad == []`）返回的就是**字面 True 单例**，
    运行时分不出"合法的 `not bad`"与"掏空的 `True`"——只有看**源码文本**才分得出。
    """
    with open(__file__, "r", encoding="utf-8") as fh:
        src = fh.read()
    calls = [n for n in ast.walk(ast.parse(src))
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "guard"]
    bad = []
    for n in calls:
        if len(n.args) < 3:
            bad.append(f"自检件:{n.lineno} 的 guard(...) 实参少于 3 个")
            continue
        if isinstance(n.args[1], ast.Constant) and n.args[1].value is True:
            bad.append(f"自检件:{n.lineno} 的 guard(...) 期望值是**字面 True**（恒真 ⇒ 掏空）")
        d = n.args[2]
        if isinstance(d, ast.Constant) and not d.value:
            bad.append(f"自检件:{n.lineno} 的 guard(...) detail 是空字面量（掏空形态）")
    if len(calls) != len(EXPECTED_GUARD_NAMES):
        bad.append(f"AST 看到的 guard(...) 调用 {len(calls)} 个，名册 {len(EXPECTED_GUARD_NAMES)} 个")
    print(f"    [i] AST：guard(...) 调用 {len(calls)} 个（名册 {len(EXPECTED_GUARD_NAMES)} 个）；"
          f"期望值均非字面 True，detail 均非空字面量")
    guard("E12 守卫体完整性", not bad, "; ".join(bad[:6]))
# ---------------------------------------------------------------- 无守卫面名册 + 覆盖率报告
#
# 修复轮 5 起，名册是**两个口径**里的第一个（**已登记名册口径**）：
#   · 口径一（本名册）：逐条登记"可判定断言单元" + 它的守卫名；覆盖 % 的分母 = 本名册条数。
#   · 口径二（`enumerate_doc_units` 的**普查**）：从文档现扫所有"带读数形态数字的行"，
#     要求每行都归入已登记的某一类 ⇒ 防"**当初就没登记**某个单元"。两个口径的差，`--coverage` 现场打印。
# 判定一个单元"有守卫"的**两个条件都必须成立**：
#   ① 文档里那一行带 `〔机器守卫：<守卫名>〕`（**标记在文档侧** ⇒ `--doc <快照>` 上必然全判为无守卫）；
#   ② 该守卫**在场且为绿**（`_guard_green`）。
# 只有标记、守卫不在场 ⇒ **FAIL**（E2 报），不许"挂个牌子就算有守卫"。
# U12–U14 是修复轮 5 按复核 §4.3 补登记的**三条名册外单元**（改错值即 FAIL）。
COVERAGE_UNITS = [
    ("U01", "头部覆盖自陈·出站指针条数（`107 条`）", r"覆盖自陈（必须与实跑一致", "E1 头部自陈"),
    ("U02", "头部覆盖自陈·去重落点数（`76 个`）", r"覆盖自陈（必须与实跑一致", "E1 头部自陈"),
    ("U03", "头部覆盖自陈·覆盖率（`76/76 = 100%`）", r"覆盖自陈（必须与实跑一致", "E1 头部自陈"),
    ("U04", "头部覆盖自陈·裸 `:NN` 指针数（`0 条`）", r"覆盖自陈（必须与实跑一致", "E1 头部自陈"),
    ("U05", "口径句「只动模式这一个变量」（`-i` 同宽）", r"这一行要证明的是", "E5 口径同宽"),
    ("U06", "口径句「真值基线 0 ⇒ 非零即提请复核」", r"非零即提请复核", "E6 基线非零"),
    ("U07", "C3 读法「最短句 < 8 词 且全节 ≥ 3 处」（阈值出自判词）", r"它的读法是", None),
    ("U08", "自查清单「15 条」", r"逐条自查清单\*\* = ", "E7 自查清单条数"),
    ("U09", "B5 边界「要给出边界，还缺两样」的**基数**", r"要给出边界，还缺", "E10 缺项基数"),
    ("U10", "`±1pp` 容差自述（脚本自定）", r"这一项带 \*\*±\d+pp\*\* 容差", "E4 容差自述"),
    ("U11", "`This \\w+` 五份 `+7/+9/+7/+8/+1`", r"五份各 \*\*\+7", "E8 This-X 复算"),
    ("U12", "判分表「Q1–Q13 共 13 条」", r"\*\*判分表\*\* = ", "E11 判分表条数"),
    ("U13", "本文件的自检边界·「降掉的 N 条」", r"\*\*降掉的 ", "E2 无守卫面计数"),
    ("U14", "本文件的自检边界·「剩下的 N 条」", r"\*\*剩下的 ", "E2 无守卫面计数"),
]

# ---- 修复轮 5 · 第二口径：文档现扫普查（防"当初没登记某单元"）----
#
# **规则 R**（机械、纯文档侧，`enumerate_doc_units`）：
#   ① 跳过代码围栏内的行、表格分隔行、空行、标题行；
#   ② 从行里去掉 **指针**（`file.md:NN` / `:NN–MM`）、**日期**（YYYY-MM-DD）、**节号**（`§N.M`）；
#   ③ 剩下的文本里若还有**读数形态的数**（`数字+量词/单位`、`带小数点的数`、`**加粗整数**`）⇒ 记一行。
#
# **只做到这一步就停**：规则 R 给的是**行粒度**的候选面，不是"断言单元"本身。
# 名册是**断言粒度**（同一行可以含多条自陈 —— 头部那句一行含四句），且把候选行分成
# "复述型（同一数在别处有守卫）/ 非独立单元（节号、标题引文）/ 真无守卫"需要**人读语义**。
# ⇒ **全派生做不到**；能机械做到的是"**不许有未归类的新行**"：
#   普查扫出来的每一行，必须落在 {名册锚点 · 〔判词读数〕 · 〔本文件复算〕 · `CENSUS_CLASS` 逐条登记}
#   之一，否则 **E2 FAIL**。这就是把"当初没登记"从**静默缺口**变成**显式登记 + 缺失即红**。
CENSUS_PTR_RE = re.compile(
    r"[\w`./\\-]*[\w-]\.(?:md|py|html|txt|json|yml|yaml|tex):\d+(?:[\u2013-]\d+)?"
    r"|`:\d+(?:[\u2013-]\d+)?`")
CENSUS_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
CENSUS_SEC_RE = re.compile(r"\u00a7\d+(?:\.\d+)*")
CENSUS_READ_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:\u2030|%|pp|词|字|次|处|句|行|条|个|格|份)"
    r"|\d+\.\d+|\*\*\d+\*\*")
CENSUS_SEP_RE = re.compile(r"^\s*\|?[\s:|\-]+\|?\s*$")

# 逐条登记的分类表：(行内锚点, 类别, 一句性质)。锚点必须**恰好命中一条普查行**。
# 类别 ∈ {已覆盖, 复述型, 非独立单元, 无守卫}。
CENSUS_CLASS = [
    (r"唯一权威表述", "已覆盖", "A9 现场重算本行的两个数（grep -rn 命中数 / .claude/skills 目录数）"),
    (r"将来的写作类 skill", "已覆盖", "A9 现场重算本行的两个数（同一个 A9）"),
    (r"格不同、", "已覆盖", "A6 从本行现取逐格结论并回源文件重算（12 格里 N 格不同）"),
    (r"两表都恰好得", "已覆盖", "A6 从本行现取加权和并重算"),
    (r"漏数的那", "复述型", "同一组数由 A6 守卫（它就从那一行现取）；本行是复述"),
    (r"修的是", "复述型", "同一个 62.8 由 A6 守卫；本行是复述"),
    (r"同族但不在判分表里", "复述型", "「15 条」由 E7、「Q1–Q13 共 13 条」由 E11 守卫；本行是复述"),
    (r"别拿 `judge\.md:103` 当这条的出处", "已覆盖", "E9·P1 从本行现取 S1 列值并回 judge.md:103 重算"),
    (r"七个候选代理量的实测分布", "非独立单元", "引的是判词原文里的节标题 `### 6.2`（那 6.2 不是本文件的读数）"),
    (r"个 alternation", "已覆盖", "C5 从本行现取 6 个 alternation 并与两份源判词逐字比对"),
    (r"各 0 命中）；产物", "已覆盖", "A2 从本行现取密度结论并重跑五份"),
    (r"以本文件这条口径为准", "复述型", "同一组密度由 A2 守卫；本行是复述"),
    (r"无判别力的一类", "已覆盖", "A8 从本行现取词表口径与命中数并重跑五份"),
    (r"方向相反的一类", "已覆盖", "A8 从本行现取词表口径、命中数与两个落点并重跑"),
    (r"A5\*\*（同处不许自相矛盾）", "复述型", "「15 条清单第 15 条」由 E7 守卫；本行是复述"),
    (r"容差自述（`E4`）", "复述型", "`This \w+` 五份由 E8、`±1pp` 由 E4 守卫；本行是清单复述"),
    (r"明确的局限", "复述型", "「覆盖不到 1 条」由 E2 守卫；本行是它的复述"),
    (r"占 4 条", "复述型", "E1 的四句由 E1 守卫（名册 U01–U04）；本行只是复述「四句各算一条」"),
    (r"判分表「Q1–Q13 共 13 条」", "复述型", "同一个数由 E11 守卫；本行是本节的清单复述"),
    (r"本节自己的两个记账数", "复述型", "「降掉」数与「剩下」数由 E2 守卫（名册 U13/U14 的载体行）；本行是复述"),
]


def enumerate_doc_units():
    """规则 R（见上方注释）：返回文档里"带读数形态数字"的行 `[(行号, 行文本)]`。**纯文档侧、无常量**。"""
    rows, in_fence = [], False
    for i, l in enumerate(DOC_LINES, 1):
        if l.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not l.strip() or l.lstrip().startswith("#") or CENSUS_SEP_RE.match(l):
            continue
        s = CENSUS_SEC_RE.sub(" ", l)
        s = CENSUS_PTR_RE.sub(" ", s)
        s = CENSUS_DATE_RE.sub(" ", s)
        if CENSUS_READ_RE.search(s):
            rows.append((i, l))
    return rows


def census_status():
    """把普查行归类。**未归类 = FAIL**（E2）：类别表锚点丢失也报。"""
    rows = enumerate_doc_units()
    roster_lines = set()
    for _uid, _label, anchor, _g in COVERAGE_UNITS:
        roster_lines |= {i for i, l in enumerate(DOC_LINES, 1) if re.search(anchor, l)}
    classified, unclassified, used = set(), [], set()
    ok_covered = rep = nonunit = unguarded = judge_self = 0
    detail = []
    for i, l in rows:
        if i in roster_lines:
            continue
        if "判词读数" in l or "本文件复算" in l:
            judge_self += 1
            continue
        hit = None
        for k, (pat, cat, _why) in enumerate(CENSUS_CLASS):
            if re.search(pat, l):
                hit = k
                break
        if hit is None:
            unclassified.append(i)
            continue
        used.add(hit)
        classified.add(i)
        cat, why = CENSUS_CLASS[hit][1], CENSUS_CLASS[hit][2]
        detail.append((i, cat, why))
        if cat == "已覆盖":
            ok_covered += 1
        elif cat == "复述型":
            rep += 1
        elif cat == "非独立单元":
            nonunit += 1
        else:
            unguarded += 1
    dangling = [CENSUS_CLASS[k][0] for k in range(len(CENSUS_CLASS)) if k not in used]
    return {"rows": rows, "roster": len(roster_lines), "classified": len(classified),
            "unclassified": unclassified, "dangling": dangling, "judge_self": judge_self,
            "detail": detail,
            "ok_covered": ok_covered, "rep": rep, "nonunit": nonunit, "unguarded": unguarded}


def coverage_units_status(assume_green=()):
    """逐个单元判：有守卫 / 无守卫 / 改归〔判词读数〕（不可重算）。

    `assume_green`：**自指守卫**用。U13/U14 的守卫就是 E2 本身 ⇒ E2 在自己运行时把"本检查在场"
    按在场计（否则它永远算不到自己）；它真正的约束是**数值比对本身**。其它调用方（`--coverage`）
    不传这个参数，此时 E2 已登记，绿否是真实读数。
    """
    rows, guarded, unguarded, judge, stale = [], 0, 0, 0, []
    for uid, label, anchor, gname in COVERAGE_UNITS:
        lines = [i for i, l in enumerate(DOC_LINES, 1) if re.search(anchor, l)]
        marked_j = any("判词读数" in DOC_LINES[i - 1] for i in lines)
        marked_g = bool(gname) and any(f"〔机器守卫：{gname}〕" in DOC_LINES[i - 1] for i in lines)
        if marked_g and (_guard_green(gname) or gname in assume_green):
            st, guarded = f"有守卫（{gname}）", guarded + 1
        elif marked_j and not gname:
            st, judge = "已改归〔判词读数〕（无口径可重算）", judge + 1
        else:
            st, unguarded = "**无守卫**", unguarded + 1
            if marked_g or (gname and gname in GUARD_SEEN):
                stale.append(f"{uid}({gname or '判词读数'} 标记与守卫状态不一致)")
        rows.append((uid, lines, label, st))
    return {"rows": rows, "total": len(COVERAGE_UNITS), "guarded": guarded,
            "unguarded": unguarded, "judge": judge, "stale": stale,
            "named_guards": sum(1 for u in COVERAGE_UNITS if u[3]),
            "nameless": sum(1 for u in COVERAGE_UNITS if not u[3])}


def check_e2_unguarded_count():
    """E2：文档「本文件的自检边界」那一节的**四个数** = `--coverage` 现算的四个数（修复轮 5 扩）。

    修复轮 5 之前只对账两个（覆盖不到 / 改前）⇒ 复核 I-1 实证：同节的「降掉的 N 条」写错（9 实为 10）
    也**全绿**。现在四个数（覆盖不到 / 改前 / 降掉 / 剩下）逐项对账，并当核"降掉 + 剩下 = 改前"的闭合。
    另加两条结构约束：**每个〔机器守卫：X〕标记必须落在名册行上**；**普查行必须全部归类**。
    """
    w_now = find1(r"机器守卫覆盖不到的：`(\d+)` 条", what="自检边界·无守卫数")
    w_before = find1(r"改前是 `(\d+)` 条", what="自检边界·改前数")
    w_drop = find1(r"\*\*降掉的 (\d+) 条\*\*", what="自检边界·降掉数")
    w_left = find1(r"\*\*剩下的 (\d+) 条\*\*", what="自检边界·剩余数")
    st = coverage_units_status(assume_green=("E2 无守卫面计数",))
    bad = []
    if int(w_now) != st["unguarded"] + st["judge"]:
        bad.append(f"文档说《覆盖不到的 {w_now} 条》，--coverage 现算 {st['unguarded'] + st['judge']} 条"
                   f"（断言面 {st['unguarded']} + 判词读数 {st['judge']}）")
    if int(w_before) != st["total"]:
        bad.append(f"文档说《改前是 {w_before} 条》，名册常量是 {st['total']} 条")
    if int(w_drop) != st["guarded"]:
        bad.append(f"文档说《降掉的 {w_drop} 条》，--coverage 现算有守卫 {st['guarded']} 条")
    if int(w_left) != st["judge"]:
        bad.append(f"文档说《剩下的 {w_left} 条》，--coverage 现算判词读数类 {st['judge']} 条")
    if int(w_drop) + int(w_left) != int(w_before):
        bad.append(f"本节算术不闭合：降掉 {w_drop} + 剩下 {w_left} != 改前 {w_before}")
    if st["stale"]:
        bad.append("挂了〔机器守卫：…〕牌子但守卫不在场/不是绿的：" + ", ".join(st["stale"]))
    # 结构约束①：**标记不许挂在名册外的行上**（防"到处挂牌子冒充覆盖"）
    roster_lines = set()
    for _uid, _label, anchor, _g in COVERAGE_UNITS:
        roster_lines |= {i for i, l in enumerate(DOC_LINES, 1) if re.search(anchor, l)}
    # （doc:10 那句**下定义**的话本身就含这个字样，它不是"挂牌"——与 E3 的豁免同源。）
    stray = sorted(i for i, l in enumerate(DOC_LINES, 1)
                   if "〔机器守卫：" in l and i not in roster_lines
                   and not EXEMPT_MARKER_DEF.search(l))
    if stray:
        bad.append("这些行的〔机器守卫：…〕标记**不在名册行上**（名册漏登记？）："
                   + ", ".join(f"doc:{i}" for i in stray))
    # 结构约束②：普查行必须全部归类（"当初没登记"不许静默存在）
    cs = census_status()
    if cs["unclassified"]:
        bad.append("**普查扫出来的行没有归类**（新出现的读数行？补 `CENSUS_CLASS` 或补守卫）："
                   + ", ".join(f"doc:{i}" for i in cs["unclassified"]))
    if cs["dangling"]:
        bad.append("`CENSUS_CLASS` 的锚点一条都没命中普查行（锚点失效）："
                   + ", ".join(repr(p) for p in cs["dangling"][:4]))
    print(f"    [i] 无守卫面复算：覆盖不到 {st['unguarded'] + st['judge']} 条"
          f"（断言面 {st['unguarded']} · 判词读数 {st['judge']}）· 有守卫 {st['guarded']}/{st['total']}")
    print(f"    [i] 普查（第二口径）：扫得 {len(cs['rows'])} 行 · 名册锚点 {cs['roster']} 行 · "
          f"已归类 {cs['classified']} 行（已覆盖{cs['ok_covered']}/复述{cs['rep']}/"
          f"非单元{cs['nonunit']}/真无守卫{cs['unguarded']}）· 未归类 {len(cs['unclassified'])} 行")
    guard("E2 无守卫面计数", not bad, "; ".join(bad))


# 〔判词读数〕名册：**引判词读数、又没有可重跑口径**的文档行。
# X4：漏标即 FAIL；反向：带标记却没登记也 FAIL。
JUDGE_READING_ROSTER = [
    (r"GREEN 轮复核：修好了\*\*〔判词读数〕", "A1 RED→GREEN 的机构名/reference 读数"),
    (r"`out-S1-g\.md:34` `\\cite\{archard1953\}` 1 处", "B1 正文明标补上的处数"),
    (r"两侧都是\"同一段里过去时陈述交付动作", "B5 时态：两侧都是常规"),
    (r"\*\*最小可执行读法\*\*（落点 = `judge-green\.md:138-141`", "B5 最小可执行读法的 4 处 / 3 处"),
    (r"要给出边界，还缺", "B5 边界：GREEN S1 3 处 / RED S1 4 行 / GREEN S2 10 处"),
    (r"真值 \*\*0/50 句\*\*", "C1 套话比 0/50 vs 10.2%/21.3%/9.1%"),
    (r"可比性主要在 `true-S1` 这一半", "C1 偏置：0/34 与 0/16"),
    (r"是任务书给定的下限", "C1 天花板：8%"),
    (r"同一量在另一份判词里是 6\.4‰", "C2 的 6.4‰ 与 10 次"),
    (r"极短断言句\*\*〔RED \+ GREEN〕〔判词读数", "C3 的 3 / 5 / 6 词与 7–8 词基线"),
    (r"加粗小标签被分句器切开", "C3 的 2 词与真正的 3 条"),
    (r"基线订正（2026-09-27 由 GREEN 轮复量）", "C3 基线订正 11 词→7–8 词"),
    (r"句长 CV\*\*〔RED \+ GREEN〕", "句长 CV 0.601 / 0.691"),
    (r"本文件早先写的理由", "句长 CV 旧理由的两组区间"),
    (r"root-TTR 词汇多样性\*\*〔RED \+ GREEN〕〔判词读数", "root-TTR 的六个读数与等长对照"),
    (r"第三层里只有两个量是", "文末阈值段引的 C1 百分比"),
    (r"它的读法是", "C3 读法引的 8 词 / 3 处 阈值"),
    (r"命中数为 0 即判失败", "判词里的阈值式写法"),
]
JUDGE_PTR_RE = re.compile(r"(?:judge\.md|judge-green\.md):\d+")
READING_NUM_RE = re.compile(r"\d+(?:\.\d+)?\s*(?:‰|%|词|次|处|句|行|条)")
EXEMPT_MARKER_DEF = re.compile(r"本文件自带可跑命令的数")   # doc:10 是〔判词读数〕的定义行，不是读数
# 「本文件的自检边界」一节**全程在讨论这两套标记的词汇** ⇒ 它里面的标记字样不算"挂牌"。
# （**只豁免这一节的"反向"判定**；正向判定与启发式网照扫全篇。）
SELF_BOUNDARY_RE = re.compile(r"^##\s*本文件的自检边界")


def _self_boundary_start():
    for i, l in enumerate(DOC_LINES, 1):
        if SELF_BOUNDARY_RE.match(l):
            return i
    return None


def check_e3_judge_reading_roster():
    """E3（X4）：〔判词读数〕**挂牌与名册一致** + 一条启发式网兜"新出现的漏标行"。"""
    bad = []
    bs = _self_boundary_start()
    marked = {i for i, l in enumerate(DOC_LINES, 1)
              if "判词读数" in l and not EXEMPT_MARKER_DEF.search(l)
              and not (bs and i >= bs)}
    registered = set()
    for pat, label in JUDGE_READING_ROSTER:
        hits = [i for i, l in enumerate(DOC_LINES, 1) if re.search(pat, l)]
        if not hits:
            bad.append(f"名册锚点丢失（{label}）：{pat!r}")
            continue
        registered |= set(hits)
        for i in hits:
            if "判词读数" not in DOC_LINES[i - 1]:
                bad.append(f"doc:{i}（{label}）引判词读数却**没有**〔判词读数〕标记")
    for i in sorted(marked - registered):
        bad.append(f"doc:{i} 带〔判词读数〕却没进名册（标记与名册不一致）")
    for i, l in enumerate(DOC_LINES, 1):
        if i in registered or i in marked:
            continue
        if JUDGE_PTR_RE.search(l) and READING_NUM_RE.search(l) and "机器守卫" not in l:
            bad.append(f"doc:{i} 引判词文件又带读数形态的数，却既没〔判词读数〕也没〔机器守卫〕"
                       f"（疑似漏标 —— 补标记或补守卫）")
    print(f"    [i] 〔判词读数〕行 {len(marked)} 行 · 名册锚点 {len(JUDGE_READING_ROSTER)} 条")
    guard("E3 判词读数挂牌", not bad, "; ".join(bad[:8]))


def coverage_report():
    """`--coverage`：逐条打印无守卫面（行号 + 一句话）+ `COVERAGE:` / `UNGUARDED:` + **第二口径普查**。"""
    st = coverage_units_status()
    print("== 口径一：已登记名册（--coverage）——有守卫 = 文档侧有〔机器守卫：<名>〕**且**该守卫在场且为绿 ==")
    for uid, lines, label, s in st["rows"]:
        where = ",".join(f"doc:{i}" for i in lines) if lines else "**锚点丢失**"
        print(f"  {uid}  {where:<14} {label:<52} → {s}")
    n_un = st["unguarded"] + st["judge"]
    print()
    print(f"  可判定断言单元 {st['total']} 条 · 有守卫 {st['guarded']} · 覆盖不到 {n_un}"
          f"（断言面 {st['unguarded']} + 已改归〔判词读数〕{st['judge']}）")
    print(f"  已登记的方向性断言（X1 极性断言，**只覆盖这些**）：{len(POLARITY)} 条 —— "
          + "；".join(p["label"] for p in POLARITY))
    print(f"COVERAGE: 有守卫 {st['guarded']}/{st['total']} = "
          f"{st['guarded'] / st['total'] * 100:.0f}%")
    print(f"UNGUARDED: {n_un} 条（断言面 {st['unguarded']} + 判词读数 {st['judge']}）")
    cs = census_status()
    print()
    print("== 口径二：文档现扫普查（规则 R：带读数形态数字的行；**行粒度**，只用来防"
          "「当初没登记」）==")
    print(f"  扫得 {len(cs['rows'])} 行 · 其中名册锚点 {cs['roster']} 行 · "
          f"〔判词读数〕/〔本文件复算〕行（设计上不可重算）{cs['judge_self']} 行 · "
          f"名册外已归类 {cs['classified']} 行 · 未归类 {len(cs['unclassified'])} 行")
    print(f"  名册外已归类的 {cs['classified']} 行：已覆盖（守卫在名册外的某条检查）{cs['ok_covered']} · "
          f"复述型 {cs['rep']} · 非独立单元 {cs['nonunit']} · **真无守卫 {cs['unguarded']}**")
    for i, cat, why in cs["detail"]:
        print(f"    doc:{i:<4} [{cat}] {why}")
    if cs["unclassified"]:
        print("  **未归类**（E2 会 FAIL）：" + ", ".join(f"doc:{i}" for i in cs["unclassified"]))
    print(f"CENSUS: 扫得 {len(cs['rows'])} 行 · 名册 {st['total']} 条 · 名册外已归类 {cs['classified']} 行 · "
          f"未归类 {len(cs['unclassified'])} 行 · 真无守卫 {cs['unguarded']} 行")
    return st


# ---------------------------------------------------------------- §D 覆盖守卫

# 文档第一段里给两个标记下定义的那一行（它自己带"本文件复算"四个字，但不是自算行）
EXEMPT_LINE = re.compile(r"本文件自带可跑命令的数")

# 反向名册：这些**自算行**必须仍然带着〔本文件复算〕标记。
# （修复轮 2 实测：删掉一个已有标记，脚本照样绿 ⇒ 守卫可自擦。D2 堵这个方向。）
SELF_COMPUTED_ROSTER = [
    (r"RED 轮的重锤", "A1 的 12 格对照"),
    (r"为什么是 6 个而不是早先的 4 个", "C2 口径加宽"),
    (r"本文件复算（2026-09-27）", "C2 的 5 条 wc -w 代码块"),
    (r"为什么含表格行", "C2 剔表格行实验"),
    (r"本文件早先那句口径写作", "F-1 旧口径五个数"),
    (r"模板化过渡词表", "过渡词表合计 1 次"),
    (r"必须分两类写，不能并成一句", "AI 词表两类的分列"),
    (r"第三层里只有两个量是", "文末密度区间"),
    (r"显式自我削弱词（模式|这一族在本语料", "自我削弱口径的两处实测"),
]


def check_coverage_forward():
    tagged = {i for i, l in enumerate(DOC_LINES, 1)
              if "本文件复算" in l and not EXEMPT_LINE.search(l)}
    missed = sorted(tagged - CLAIMED_LINES)
    for i in sorted(tagged & CLAIMED_LINES):
        print(f"    [OK ] doc:{i} 已被 §A 认领")
    record("D1 覆盖守卫·正向（〔本文件复算〕行必须被认领）", not missed,
           ("这些自算行没有任何 §A 检查认领：" + ", ".join(f"doc:{i}" for i in missed)) if missed else "")


def check_coverage_reverse():
    """反向：名册里的自算行必须仍带〔本文件复算〕标记（防"删掉标记即逃逸"）。"""
    bad = []
    for pat, label in SELF_COMPUTED_ROSTER:
        hits = [i for i, l in enumerate(DOC_LINES, 1) if re.search(pat, l)]
        if not hits:
            bad.append(f"名册锚点丢失（{label}）：{pat!r}")
            continue
        for i in hits:
            if "本文件复算" not in DOC_LINES[i - 1]:
                bad.append(f"doc:{i}（{label}）是自算行却**没有**〔本文件复算〕标记")
            else:
                print(f"    [OK ] doc:{i} 仍带〔本文件复算〕（{label}）")
    record("D2 覆盖守卫·反向（自算行必须仍挂牌）", not bad, "; ".join(bad))


def check_claims_alive():
    """D3：每条 claim() 正则必须命中 ≥1 行——认领本身失效也要红。"""
    bad = []
    for pat, hit in CLAIM_PATTERNS:
        if not hit:
            bad.append(f"claim 正则 {pat!r} 一行都没命中（认领已失效）")
    record(f"D3 覆盖守卫·认领存活（{len(CLAIM_PATTERNS)} 条 claim 正则）", not bad, "; ".join(bad))


# ---------------------------------------------------------------- 主流程

def pmap():
    """打印出站指针全表 + 自陈计数（供报告与"自称对齐"用）。"""
    ptrs = extract_pointers()
    by_key = {}
    for dl, name, a, b in ptrs:
        path = resolve(name)
        k = (relkey(path) if path else name, a)
        by_key.setdefault(k, set()).add(dl)
    for (key, a), dls in sorted(by_key.items()):
        path = ROOT / key
        ls = _lines(path) if path.exists() else []
        body = ls[a - 1].strip()[:80] if path.exists() and a <= len(ls) else "<MISSING/OOB>"
        print(f"  doc:{','.join(str(x) for x in sorted(dls)):<16} {key}:{a:<5} {body}")
    print()
    n_bare = sum(len(list(BARE_RE.finditer(POINTER_RE.sub(" ", l)))) for l in DOC_LINES)
    print(f"出站指针 {len(ptrs)} 条 · 去重落点 {len(by_key)} 个 · 覆盖 {len(by_key)}/{len(by_key)}"
          f" · 裸指针 {n_bare}")
    return 0


def main():
    if "--pmap" in sys.argv:
        return pmap()
    if BODY_ERROR:
        print(f"FAIL  §A 正文区间（M-4b）：{BODY_ERROR}")
        print("RESULT: FAIL（1 条）")
        return 1
    _load_inbound_anchors()
    print(f"doc   = {DOC.relative_to(ROOT)}（{len(DOC_LINES)} 行）")
    print(f"cases = {CASES.relative_to(ROOT)}\n")
    for label, fn in [
        ("§A 数字复算", None),
        ("  A1", check_c2_words), ("  A2", check_c2_density), ("  A3", check_c2_widened),
        ("  A4", check_c2_table_rows), ("  A5", check_c2_old_caliber), ("  A6", check_a1_table),
        ("  A7", check_transition_words), ("  A8", check_ai_wordlist),
        ("  A9", check_doc_selfclaim), ("  A10", check_threshold_range),
        ("  A11", check_hedge_diminish),
        ("§B 出站指针（以文档为输入）", None),
        ("  B1", check_bare_pointers),
        ("  B2", lambda: check_outbound_pointers(verbose=("--rows" in sys.argv))),
        ("  B3", check_inbound_pointers),
        ("§C 回归守卫（F-1..F-9 / I-1）", None),
        ("  C1..C10", check_guards),
        ("§E 机器守卫（修复轮 4 立；修复轮 5 追加 E11/E12）", None),
        # 顺序有讲究：E2（无守卫面）要读其它 E 守卫的**绿否**，E0（名册）要读**全部** guard() 调用
        ("  E1", check_e1_header_selfclaim), ("  E4", check_e4_tolerance),
        ("  E5", check_e5_caliber_flags), ("  E6", check_e6_truth_zero),
        ("  E7", check_e7_checklist_rows), ("  E8", check_e8_thisx),
        ("  E9", check_e9_polarity), ("  E10", check_e10_missing_count),
        ("  E11", check_e11_rubric_count),
        ("  E3", check_e3_judge_reading_roster), ("  E2", check_e2_unguarded_count),
        ("  E12", check_e12_guard_bodies),
        ("  E0", check_guard_roster),
        ("§D 覆盖守卫", None),
        ("  D1", check_coverage_forward), ("  D2", check_coverage_reverse),
        ("  D3", check_claims_alive),
    ]:
        if fn is None:
            print(label)
            continue
        print(f"{label} ...")
        try:
            fn()
        except LookupError as e:
            record(label.strip(), False, f"锚点丢失（文档已重构，检查器需同步）：{e}")
        except Exception as e:  # noqa: BLE001 —— 检查器自己炸也要红，不许静默通过
            record(label.strip(), False, f"检查器异常 {type(e).__name__}: {e}")

    if "--coverage" in sys.argv:
        print()
        coverage_report()

    print()
    bad = [(n, d) for n, ok, d in RESULTS if not ok]
    for name, ok, detail in RESULTS:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  —— {detail}" if detail else ""))
    print()
    gnames = {f"{n} 回归守卫" for n in EXPECTED_GUARD_NAMES}
    n_ok_g = sum(1 for n, ok, _ in RESULTS if n in gnames and ok)
    print(f"GUARDS: 名册（**常量**）{len(EXPECTED_GUARD_NAMES)} 条 · 实际调用 {len(GUARD_SEEN)} 条"
          f" · 绿 {n_ok_g} 条  ← 分母是常量，删掉任一个 guard(...) 调用即 FAIL（E0）")
    print("RESULT: " + ("PASS" if not bad else f"FAIL（{len(bad)} 条）"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
