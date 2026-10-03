#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-topic-select` 的机械层判据 `S1`–`S6`（设计 `2026-10-03-m1-topic-select-design.md` §3；
实施计划 `2026-10-03-m1-topic-select.md` 的 Task 2）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/topic-select/check-topic-select.py
        [--problems PATH] [--output PATH] [--corpus PATH] [--skill-md PATH] [--method PATH]

**被判对象分两组**（设计 §3 是唯一权威）：

* **产出侧（`S1`–`S4`）** —— 本 skill 的**当天产出**（一份"选题决策"），由 `--output` 给：
  * `S1` **每个标签的支撑句必须是当天题面的子串**（归一化后）。★★ **心脏**。
  * `S2` **凡引历史，读数与 `PROBLEM_TYPES.md` / `MODEL_MAP.md` 现取一致**。
  * `S3` **四轴逐轴齐备**，且每轴**标明可核性**（读数 / 半可核 / 判断）；**判断型不许写成读数**。
  * `S4` **推荐带推翻条件**。
* **规范侧（`S5`–`S6`）** —— 本 skill 的**规则文档**（`SKILL.md` + `references/method.md`）：
  * `S5` **时间盒声明在位**（`≤2 小时` + **什么时候值得超时**）。
  * `S6` **禁令在位**：**不许拿"历史获奖论文篇数"代理"选它的人数"**，**且"赛期内没有任何可靠办法
    知道某题的选题人数"那句在位**（设计 §2.1.2：「规范里要明写」）。

★ 为什么 `S5`/`S6` 判**文档**而不是产出：`SKILL.md` 的「输出契约」**只列四样**
（分类 / 同型历史 / 四轴证据档 / 推荐 + 推翻条件），**时间盒与禁令不在契约内**
——它们是**本 skill 对使用者的规则**，写在 `SKILL.md`（`≤2 小时` 的契约值）与
`references/method.md`（覆盖机制 + 禁令 + 「赛期内不可回答」那句）。判产出对它们**恒真或恒假**，
不构成判据。设计 §3 的 `S6` 自己就写着「**规范里**明写」。

## 归一化**复用**（计划 P3；设计 §3「一条工程决定」）

`S1` 的归一化**不另写一套**：直接 `import tools.papers.taxonomy`（该模块 + `tools/papers/`
实测可导入）用它的 `normalize_for_locate`（题面侧）与 `normalize_quote`（引文侧）。
★ 两份归一化各写一套，两支的"可核"会有一天对不上。本器**只读**那个模块，**不改**它。

## CLI 输入面（写死；实施计划 Task 2 · 硬要求 2b）

* `--problems` —— 当天题面：**一个目录**（每份一件，文件名里的题号字母见下）**或一个文件**
  （用 `## 题 <字母>` 分节）。
* `--output` —— 本 skill 的产出（默认 = `tests/skills/topic-select/fixtures/good-output.md`，
  即"已知好产出" fixture；真实产出由调用方 `--output` 指明）。
* `--corpus` —— `corpus/papers/` 的根（默认 = 仓内 `corpus/papers`）。
* `--skill-md` / `--method` —— 规范侧两份文档（默认 = 仓内 skill）。

★ **三者任一读不出 ⇒ fail-closed 红**（`--problems` / `--output` / `--corpus`；**不许静默绿**）；
★ `--corpus` **可指向别处**（否则"读不出"的变异没法构造）。

## 产出的形态（**权威不在本文件**）

产出的**逐字形态**（题标题行 / 标签表 / 历史读数两行 / 四轴四行 / 推荐两行）由 skill 自己公布：
`.claude/skills/mcm-topic-select/references/method.md` §5「产出的逐字形态」。
★ **本器不再自带一份格式说明**（两份格式说明 ⇒ 两处各说各话）；下面 `PROB_HEAD` / … / `REC_OVER`
那组承重正则只是**那份形态的机读实现**，改形态请改 `method.md` §5，再回来对正则。

★ **题号读法**（这是 `--problems` 侧的输入规则，**不是产出形态的一部分**）：目录里每份件的文件名里
那个**不被其它 ASCII 字母贴着**的 `[A-F]` 字母（如 `A.md`、`problem_C.txt`）；单文件则用
`## 题 <字母>` 分节。

★ **标签表逐字复用** `taxonomy.py` 的三条正则（`TABLE_HEAD` / `TABLE_SEP` / `TABLE_ROW`）
与 `QUOTED`：本 skill 的"每个标签附题面原句"就是语料**口径 2** 的照搬（设计 §1.1），
所以它的机读形态也照搬 —— 复用的**不止**归一化。

退出码 **0 / 1**（无 2）；末行恒为 `RESULT: …`；每条判词一行，形态 `PASS|FAIL  <id>  <读数>`。
**fail-closed = 判红 + exit 1**（输入读不出 / 承重结构解析不出 ⇒ 红，**不许静默绿**）。

## 覆盖范围（**不声称穷尽**）

判的是**产出与'当天题面 + 语料现取 + 规范文档'之间的机械一致性**；**判不了**：推荐对不对 /
四轴的判断质量 / 分类打得准不准 / 题面本身是不是那场比赛的真题 / 文字措辞好不好。
`S1` 只判**产出里出现过的标签**（**不要求覆盖全部输入题**：本 skill 允许"只给几道排序"的用法，
且 RED 场景的写手本就只挑一道 ⇒ 强求覆盖会把 S1 的红**归因错**）。
**"看一眼"层不适用**（本支无产物可看）——那层的**替代品**（把"推荐 + 依据"拿给人读）
**不在本器里**（设计 §3.3）。**不声称覆盖全部失败模式。**
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]      # tests/skills/topic-select/x.py → 仓根
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.papers import taxonomy as TX                 # noqa: E402  ★ 归一化与标签表口径的**唯一**来源（P3）

DEFAULT_PROBLEMS = ROOT / "tests/skills/topic-select/fixtures/problems"
DEFAULT_OUTPUT = ROOT / "tests/skills/topic-select/fixtures/good-output.md"
DEFAULT_CORPUS = ROOT / "corpus/papers"
DEFAULT_SKILL_MD = ROOT / ".claude/skills/mcm-topic-select/SKILL.md"
DEFAULT_METHOD = ROOT / ".claude/skills/mcm-topic-select/references/method.md"

# 产出侧的承重形态
PROB_HEAD = re.compile(r"^#{2,}\s*题\s*([A-F])\b")
HIST_COMBO = re.compile(r"^-\s*历史：组合\s*`([^`]+)`\s*×\s*`([^`]+)`[，,]\s*出现\s*(\d+)\s*次")
HIST_MODEL = re.compile(r"^-\s*历史：题\s*`([^`]+)`\s*用过模型\s*`([^`]+)`[，,]\s*(\d+)\s*篇")
AXIS_LINE = re.compile(
    r"^-\s*轴\s*([1-4])\s*·\s*([^【\[（(]+?)\s*[【\[（(]\s*(读数|半可核|部分可核|判断)\s*[】\]）)]")
REC_PICK = re.compile(r"^-\s*推荐：\s*(.+?)\s*$")
REC_OVER = re.compile(r"^-\s*推翻条件：\s*(.+?)\s*$")
HEAD_ANY = re.compile(r"^#{2,}\s*(.*)$")

# 规范侧的承重串
TIMEBOX = re.compile(r"≤\s*2\s*(?:小时|h|hours?)", re.I)
OVERRUN = "值得超时"
NO_COUNT_SENTENCE = "赛期内没有任何可靠办法知道某题的选题人数"
PROHIBITION = re.compile(r"不许拿.{0,50}获奖.{0,50}代理.{0,50}人数")

AXIS_KEY = {1: "数据", 2: "难度", 3: "拥挤", 4: "创新"}
# 设计 §2 表**逐轴**给出的可核性（轴 1/4 = 半可核；轴 2/3 = 判断）
AXIS_EXPECT = {1: "半可核", 2: "判断", 3: "判断", 4: "半可核"}
TAG_CANON = {"部分可核": "半可核"}


def read_text(path):
    """读一个文本文件；读不出 ⇒ `None`（**fail-closed 的入口**，调用方据此判红）。"""
    try:
        return pathlib.Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def letter_from_stem(stem):
    """文件名主干里的题号字母：那个**不被其它 ASCII 字母贴着**的 `[A-F]`（`A` / `problem_C`）。"""
    m = re.search(r"(?:^|[^A-Za-z])([A-Fa-f])(?:[^A-Za-z]|$)", stem)
    return m.group(1).upper() if m else None


def parse_problems(path):
    """`--problems`（目录或单个文件）⇒ `{字母: 题面文本}`；读不出 ⇒ `None`（fail-closed）。"""
    p = pathlib.Path(path)
    if not p.exists():
        return None
    if p.is_dir():
        out = {}
        try:
            entries = sorted(p.iterdir())
        except OSError:
            return None
        for f in entries:
            if not f.is_file():
                continue
            L = letter_from_stem(f.stem)
            if L is None:
                continue
            t = read_text(f)
            if t is None:
                return None
            out[L] = t
        return out or None
    t = read_text(p)
    if t is None:
        return None
    out, cur, buf = {}, None, []

    def flush():
        if cur is not None:
            out[cur] = "\n".join(buf)
    for ln in t.splitlines():
        m = PROB_HEAD.match(ln)
        if m:
            flush()
            cur, buf = m.group(1), []
            continue
        if cur is not None:
            buf.append(ln)
    flush()
    return out or None


def split_sections(text):
    """产出的 `## 题 <字母>` 小节与 `## 推荐` 小节 ⇒ `([(字母, 小节文本)], 推荐小节文本|None)`。"""
    lines = text.splitlines()
    idx = [i for i, ln in enumerate(lines) if HEAD_ANY.match(ln)]
    probs, rec = [], None
    for k, i in enumerate(idx):
        head = HEAD_ANY.match(lines[i]).group(1).strip()
        j = idx[k + 1] if k + 1 < len(idx) else len(lines)
        body = "\n".join(lines[i + 1:j])
        mp = re.match(r"题\s*([A-F])\b", head)
        if mp:
            probs.append((mp.group(1), body))
        elif re.match(r"推荐\b", head):
            rec = body
    return probs, rec


def labels_in(body):
    """一个小节里的标签行 ⇒ `[(标记, `L1 · L2`, [原句, …]), …]`（**复用** taxonomy 的标签表口径）。"""
    out = []
    for ln in body.splitlines():
        if TX.TABLE_HEAD.match(ln) or TX.TABLE_SEP.match(ln):
            continue
        m = TX.TABLE_ROW.match(ln)
        if m:
            out.append((m.group(1) or "", m.group(2).strip(), TX.QUOTED.findall(m.group(3))))
    return out


# ----------------------------------------------------------------------------- S1
def check_s1(out_text, problems):
    """★★ 心脏：每个标签的支撑句（**按 taxonomy 口径归一化后**）必须是当天题面的子串。"""
    if out_text is None:
        return False, "fail-closed：`--output` 读不出"
    if problems is None:
        return False, "fail-closed：`--problems` 读不出或解析不出任何题"
    probs, _ = split_sections(out_text)
    if not probs:
        return False, "fail-closed：产出里解析不出任何「## 题 <字母>」小节"
    n_lbl = n_q = n_miss = 0
    bad = []
    for letter, body in probs:
        if letter not in problems:
            bad.append(f"题 {letter}：`--problems` 里没有这道题面")
            continue
        npt = TX.normalize_for_locate(problems[letter])          # ★ 复用（P3）
        for _mark, label, quotes in labels_in(body):
            n_lbl += 1
            if not quotes:
                bad.append(f"题 {letter} 标签「{label}」的支撑句单元格里没有引文")
                continue
            for q in quotes:
                n_q += 1
                if TX.normalize_quote(q) not in npt:              # ★ 复用（P3）
                    n_miss += 1
                    bad.append(f"题 {letter} 标签「{label}」：支撑句不是题面子串：{q[:44]!r}")
    if n_lbl == 0:
        return False, "fail-closed：产出里解析不出任何标签行（承重结构缺失）"
    detail = f"题 {len(probs)} 道 · 标签 {n_lbl} 个 · 支撑句 {n_q} 条 · 非子串 {n_miss} 条"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return (not bad), detail


# ----------------------------------------------------------------------------- S2
def _load_annotations(corpus_dir):
    """`PROBLEM_TYPES.md` 的标注（**现取**）；读不出/解析不出 ⇒ `None`（fail-closed）。"""
    p = pathlib.Path(corpus_dir) / "PROBLEM_TYPES.md"
    if not p.is_file():
        return None
    try:
        return TX.load_annotations(p)
    except Exception:                                          # 严格解析器抛错 ⇒ 判红
        return None


def _load_model_counts(corpus_dir):
    """`MODEL_MAP.md` 的逐题模型篇数 ⇒ `{"2025 A": {模型: 篇数}}`；读不出 ⇒ `None`。"""
    p = pathlib.Path(corpus_dir) / "MODEL_MAP.md"
    t = read_text(p)
    if t is None:
        return None
    out, cur = {}, None
    for ln in t.splitlines():
        m = re.match(r"^###\s+(\d{4})\s+([A-Z])\s*—", ln)
        if m:
            cur = f"{m.group(1)} {m.group(2)}"
            out[cur] = {}
            continue
        m2 = re.match(r"^  - (.+?)（(\d+) 篇）", ln)
        if m2 and cur is not None:
            out[cur][m2.group(1)] = int(m2.group(2))
    return out or None


def check_s2(out_text, corpus_dir):
    """凡引历史（组合出现 N 次 / 某题的 O 奖论文用过某模型 N 篇），读数与语料**现取**一致。"""
    if out_text is None:
        return False, "fail-closed：`--output` 读不出"
    anns = _load_annotations(corpus_dir)
    if anns is None:
        return False, f"fail-closed：`{pathlib.Path(corpus_dir) / 'PROBLEM_TYPES.md'}` 读不出或解析不出"
    models = _load_model_counts(corpus_dir)
    if models is None:
        return False, f"fail-closed：`{pathlib.Path(corpus_dir) / 'MODEL_MAP.md'}` 读不出"
    probs, _ = split_sections(out_text)
    if not probs:
        return False, "fail-closed：产出里解析不出任何题目小节"
    n_c = n_m = 0
    bad = []
    for letter, body in probs:
        for ln in body.splitlines():
            mc = HIST_COMBO.match(ln.strip())
            if mc:
                n_c += 1
                lab, regime, want = mc.group(1), mc.group(2), int(mc.group(3))
                if " · " not in lab:
                    bad.append(f"题 {letter}：组合标签不合 `L1 · L2` 形态：{lab!r}")
                    continue
                l1, l2 = [x.strip() for x in lab.split(" · ", 1)]
                real = sum(1 for x in anns
                           if any((a, b) == (l1, l2) for (a, b, _m) in x.labels)
                           and x.data_regime == regime)
                if real != want:
                    bad.append(f"题 {letter}：组合「{lab}」×「{regime}」现取 {real} 次 · 产出写 {want} 次")
                continue
            mm = HIST_MODEL.match(ln.strip())
            if mm:
                n_m += 1
                prob, model, want = mm.group(1).strip(), mm.group(2).strip(), int(mm.group(3))
                tbl = models.get(prob)
                if tbl is None:
                    bad.append(f"题 {letter}：`MODEL_MAP.md` 里没有题「{prob}」")
                elif model not in tbl:
                    bad.append(f"题 {letter}：「{prob}」的 O 奖论文里没有模型「{model}」")
                elif tbl[model] != want:
                    bad.append(f"题 {letter}：「{prob}」用过「{model}」现取 {tbl[model]} 篇 · 产出写 {want} 篇")
    if n_c + n_m == 0:
        return False, "fail-closed：产出里解析不出任何「- 历史：…」读数行（同型历史是输出契约的一项）"
    detail = f"历史读数 {n_c + n_m} 条（组合 {n_c} · 模型 {n_m}）· 与语料现取不符 {len(bad)} 条"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return (not bad), detail


# ----------------------------------------------------------------------------- S3
def check_s3(out_text):
    """四轴逐轴齐备，且每轴**标明可核性**；**判断型不许写成读数**（设计 §2 的逐轴表）。"""
    if out_text is None:
        return False, "fail-closed：`--output` 读不出"
    probs, _ = split_sections(out_text)
    if not probs:
        return False, "fail-closed：产出里解析不出任何题目小节"
    n_axis = 0
    bad = []
    for letter, body in probs:
        found = {}
        for ln in body.splitlines():
            m = AXIS_LINE.match(ln.strip())
            if m:
                found[int(m.group(1))] = (m.group(2).strip(), TAG_CANON.get(m.group(3), m.group(3)))
        for no in (1, 2, 3, 4):
            if no not in found:
                bad.append(f"题 {letter}：缺轴 {no}")
                continue
            name, tag = found[no]
            n_axis += 1
            if AXIS_KEY[no] not in name:
                bad.append(f"题 {letter}：轴 {no} 的名字里没有「{AXIS_KEY[no]}」（读到 {name!r}）")
            if tag != AXIS_EXPECT[no]:
                bad.append(f"题 {letter}：轴 {no}「{name}」的可核性标成「{tag}」· 应为「{AXIS_EXPECT[no]}」")
    detail = f"题 {len(probs)} 道 · 四轴读数 {n_axis} 处（应 {len(probs) * 4}）· 不符 {len(bad)} 处"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return (not bad), detail


# ----------------------------------------------------------------------------- S4
def check_s4(out_text, problems):
    """推荐**带推翻条件**（并点名一道题）。"""
    if out_text is None:
        return False, "fail-closed：`--output` 读不出"
    _, rec = split_sections(out_text)
    if rec is None:
        return False, "fail-closed：产出里没有「## 推荐」小节"
    pick = over = None
    for ln in rec.splitlines():
        m = REC_PICK.match(ln.strip())
        if m and pick is None:
            pick = m.group(1).strip()
        m = REC_OVER.match(ln.strip())
        if m and over is None:
            over = m.group(1).strip()
    bad = []
    if not pick:
        bad.append("推荐小节里没有「- 推荐：…」行")
    else:
        letters = set(re.findall(r"[A-F]", pick))
        if problems is not None:
            letters &= set(problems)
        if not letters:
            bad.append(f"推荐没有点名一个在场的题号（读到 {pick!r}）")
    if not over:
        bad.append("推荐小节里没有「- 推翻条件：…」行")
    elif len(over) < 5:
        bad.append(f"推翻条件内容过短（{over!r}）")
    shown = (over[:40] + "…") if over and len(over) > 40 else over
    detail = f"推荐 = {pick!r} · 推翻条件 = {shown!r}"
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return (not bad), detail


# ----------------------------------------------------------------------------- S5
def check_s5(skill_md, method):
    """时间盒声明在位：`≤2 小时`（契约值在 SKILL.md）+「什么时候值得超时」（在 method.md）。"""
    if skill_md is None:
        return False, "fail-closed：`--skill-md`（SKILL.md）读不出"
    if method is None:
        return False, "fail-closed：`--method`（method.md）读不出"
    bad = []
    if not TIMEBOX.search(skill_md):
        bad.append("`SKILL.md` 里没有 ≤2 小时的时间盒声明（契约值）")
    if not TIMEBOX.search(method):
        bad.append("`method.md` 里没有 ≤2 小时的时间盒声明")
    if OVERRUN not in method:
        bad.append("`method.md` 里没有「什么时候值得超时」的判据")
    detail = "时间盒（≤2 小时）声明 + 「值得超时」判据"
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return (not bad), detail


# ----------------------------------------------------------------------------- S6
def check_s6(method):
    """禁令在位 + 「赛期内没有任何可靠办法知道某题的选题人数」那句在位（设计 §2.1.2）。"""
    if method is None:
        return False, "fail-closed：`--method`（method.md）读不出"
    norm = re.sub(r"\s+", " ", re.sub(r"[*`]", "", method))
    bad = []
    if NO_COUNT_SENTENCE not in norm:
        bad.append("缺那句「赛期内没有任何可靠办法知道某题的选题人数」")
    if not PROHIBITION.search(norm):
        bad.append("缺禁令「不许拿…历史获奖论文篇数…代理…选它的人数」")
    detail = "禁令 + 「赛期内不可回答」句（规范侧）"
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return (not bad), detail


def main(argv=None):
    ap = argparse.ArgumentParser(description="`mcm-topic-select` 机械层判据 S1–S6")
    ap.add_argument("--problems", default=str(DEFAULT_PROBLEMS))
    ap.add_argument("--output", default=str(DEFAULT_OUTPUT))
    ap.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    ap.add_argument("--skill-md", default=str(DEFAULT_SKILL_MD))
    ap.add_argument("--method", default=str(DEFAULT_METHOD))
    a = ap.parse_args(argv)

    out_text = read_text(a.output)
    problems = parse_problems(a.problems)

    rows = [
        ("S1", check_s1(out_text, problems)),
        ("S2", check_s2(out_text, a.corpus)),
        ("S3", check_s3(out_text)),
        ("S4", check_s4(out_text, problems)),
        ("S5", check_s5(read_text(a.skill_md), read_text(a.method))),
        ("S6", check_s6(read_text(a.method))),
    ]
    print(f"判据对象（产出侧）：产出 = {a.output}")
    print(f"                    题面 = {a.problems} · 语料 = {a.corpus}")
    print(f"判据对象（规范侧）：规范 = {a.skill_md} + {a.method}")
    for rid, (ok, detail) in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {rid}  {detail}")
    bad = [rid for rid, (ok, _d) in rows if not ok]
    print("-" * 78)
    print(f"判据 {len(rows)} 条 · 红 {len(bad)} 条")
    print("RESULT: PASS" if not bad else f"RESULT: FAIL（{','.join(bad)}）")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
