#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-playbook` 的机械层判据 `T1`–`T5`（设计 `2026-10-03-m1-playbook-design.md` §4.1；计划 Task 2）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/playbook/check-playbook.py
        [--skill-md PATH] [--timeline PATH] [--mistakes PATH] [--index PATH] [--skills-root PATH]

**被判对象**：本 skill 自己的三份文档 —— `SKILL.md` · `references/timeline.md` ·
`references/phase-mistakes.md`；另有两个**现取的读数源** —— `corpus/official/INDEX.md`
（官方事实基线）与 `.claude/skills/`（现存 skill 目录）。

★ **本模块不产任何产物**（无图 / 表 / 代码）⇒ 判据不是"量产物"，而是"**查一致性**"。
它与绘图家族的 `F1–F6` / `A1–A4`（**量产物**的宽度 / 配色 / 字体 / 几何）**无关**，
**不照抄**，也**不**为了"有个像样的判据"去造一个量不到的东西的判据（计划 P2）。

退出码 **0 / 1**（无 2）；末行恒为 `RESULT: …`；每条判词一行，形态 `PASS|FAIL  <id>  <读数>`。
**fail-closed = 判红 + exit 1**（输入读不出 / 承重结构解析不出 ⇒ 红，**不许静默绿**）。

## 五条判据（对应设计 §4.1 的表）

| ID | 判什么 | 现取的读数源 |
| :--- | :--- | :--- |
| `T1` | 时间线里的**硬时刻**与**两个时长**：硬时刻与 `INDEX.md` §2.6.1/§2.6.2 **逐位一致**；时长与 §2.6.5 **且与"由硬时刻现算的差"**一致。★ **期望值现取**，不写死。 | `INDEX.md` §2.6.1/§2.6.2/§2.6.5 |
| `T2` | 每条「失误」都带**分级标注** + **`§id` 出处**，且那个 `§id` **现场解析得到**（`INDEX.md` 表格行真的存在）。★ **解析 `§id`，不比对行号**（计划 P3）。 | `INDEX.md` 表格行 id 全集 |
| `T3` | 凡**点名的 skill** 真的存在（扫 `.claude/skills/`）；**不存在的必须明写「未建」**。 | `.claude/skills/` 目录 |
| `T4` | **北京时间换算可复算**：由 EST 侧**现算**（`zoneinfo`）再与文档的北京侧比对。★ **判据自己算，不写死 +13**（计划 P8）。 | `zoneinfo`（标准库） |
| `T5` | 阶段边界带**「构造」**标注 · 每条失误的**归类**带「构造」· 示例评分表处带官方那条 **"A Sample / 可按题目调整"** 限定。 | 本地文档断言（无外部源） |

## ★ 关于 `T1` 为什么也判「时长」

设计 §4.1 把 `T1` 记作"三个硬时刻逐位一致"。但**两个时长（99 / 100 小时）是从那三个硬时刻推出来的**
（`INDEX.md` §2.6.5 自己就是这么推的）⇒ 它**同属"时间线的现取一致性"**，且是**流传错说法"96 小时"**的落点。
故 `T1` 判三层：**(a)** 硬时刻 vs §2.6.1/§2.6.2；**(b)** 文档时长 vs §2.6.5；
**(c)** 文档时长 vs **由 §2.6.2 硬时刻现算的差** —— 这三层**任一层读不出即红**。
（(`b`) 与 (`c`) 并列：若 `INDEX.md` 内部不自洽，(`c`) 当场变红。）

## 关于 `T2` 的解析面（**不声称穷尽**）

只解析**每条失误的「出处」行**（`- 出处：…`）。这三份文档里另有若干 `§id` 出现在**散文**里、
指的是**设计件**（如 `§0.6` · `§1.1` · `§0.2`）而**不是** `INDEX.md` 的表格行 ⇒ **不在本判据的解析面内**，
**不判**。本器**不**声称覆盖"文档里出现的每一个 `§id`"。

## 覆盖范围（**不声称穷尽**）

判的是**文档与来源之间的机械一致性**；**判不了**：这张时刻表讲不讲得清 / 动作清单照做做不做得出来 /
阶段切分合不合理 / 文字措辞好不好。**"看一眼"层不适用**（本支无产物）—— 那层的**替代品**
（把动作清单拿给人读一遍）**不在本器里**（计划 P6）。**不声称覆盖全部失败模式。**
"""
import argparse
import pathlib
import re
import sys
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[3]          # tests/skills/playbook/x.py → 仓根
DEFAULT_SKILL_MD = ROOT / ".claude/skills/mcm-playbook/SKILL.md"
DEFAULT_TIMELINE = ROOT / ".claude/skills/mcm-playbook/references/timeline.md"
DEFAULT_MISTAKES = ROOT / ".claude/skills/mcm-playbook/references/phase-mistakes.md"
DEFAULT_INDEX = ROOT / "corpus/official/INDEX.md"
DEFAULT_SKILLS_ROOT = ROOT / ".claude/skills"

# 三个**硬时刻**（其实是四个：§2.6.2 的三个 + §2.6.1 的报名截止）—— 逐条写明它该由哪个 §id 供值。
# ★ 这里写的是"**去哪取**"，**不是**期望值（期望值一律现取）。
HARD_MOMENTS = [
    ("报名/缴费截止", "2.6.1"),
    ("开赛", "2.6.2"),
    ("停止修改", "2.6.2"),
    ("提交截止", "2.6.2"),
]
# 两个**推算时长**：`(标签, 起点 label, 终点 label)`
DURATIONS = [
    ("开赛→停止修改", "开赛", "停止修改"),
    ("开赛→提交截止", "开赛", "提交截止"),
]
DT = r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}"
GRADES = ("官方", "半官方", "社区")          # `[官方]` / `[半官方]†` / `[社区]`
BUILT = "未建"                              # 尚未建的 skill 的**明写**标记


def read_text(path):
    """读一个文本文件；读不出 ⇒ `None`（**fail-closed 的入口**，调用方据此判红）。"""
    try:
        return pathlib.Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def norm_label(s):
    """把标签归一：去空白与强调星号（`**开赛**` 与 `报名 / 缴费截止` 与官方写法对齐）。"""
    return re.sub(r"[\s*]", "", s)


def _flat_dt(s):
    return re.sub(r"\s+", " ", s.replace("*", "")).strip()


def section(text, start_marker, end_marker=None):
    """取 `start_marker` 那一行起、到 `end_marker`（不含）或文末为止的片段。找不到起点 ⇒ `""`。"""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith(start_marker):
            start = i
            break
    if start is None:
        return ""
    if end_marker is None:
        return "\n".join(lines[start:])
    for j in range(start + 1, len(lines)):
        if lines[j].startswith(end_marker):
            return "\n".join(lines[start:j])
    return "\n".join(lines[start:])


def index_rows(text):
    """`INDEX.md` 的表格行 ⇒ `{§id: 事实单元格文本}`（只有**表格行**，不取标题 / 散文）。"""
    rows = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(\d+\.\d+(?:\.\d+)*)\s*\|", line)
        if not m:
            continue
        parts = line.split("|")
        if len(parts) >= 3:
            rows[m.group(1)] = parts[2].strip()
    return rows


def index_moments(fact):
    """从一行事实里抽出 `{归一标签: 日期时刻}`（用于 §2.6.1 / §2.6.2）。"""
    out = {}
    for m in re.finditer(r"([^；;：:|]+?)\s*[：:]\s*\**\s*(" + DT + r")", fact):
        out[norm_label(m.group(1))] = _flat_dt(m.group(2))
    return out


def timeline_hard_moments(text):
    """`timeline.md` §1 的硬时刻表 ⇒ `{归一标签: (EST, 北京)}`。"""
    seg = section(text, "## 1.", "## 2.")
    out = {}
    for line in seg.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        est = _flat_dt(cells[1])
        if not re.fullmatch(DT, est):
            continue                                  # 表头行 / 分隔行 / 说明行
        out[norm_label(cells[0])] = (est, _flat_dt(cells[2]))
    return out


def parse_two_durations(text):
    """在两个文档里抽 `开赛→停止修改 = N 小时` / `开赛→提交截止 = N 小时`（末尾单位"小时"）。"""
    out = {}
    for name, a, b in DURATIONS:
        pat = re.escape(a) + r"\s*→\s*" + re.escape(b) + r"\s*=\s*\**\s*(\d+(?:\.\d+)?)\s*小时"
        m = re.search(pat, text)
        if m:
            out[name] = float(m.group(1))
    return out


def hours_between(a, b):
    fa = datetime.strptime(a, "%Y-%m-%d %H:%M")
    fb = datetime.strptime(b, "%Y-%m-%d %H:%M")
    return (fb - fa).total_seconds() / 3600.0


# ----------------------------------------------------------------------------- T1
def check_t1(idx_text, tl_text):
    problems, notes = [], []
    if idx_text is None:
        return False, "fail-closed：`INDEX.md` 读不出"
    if tl_text is None:
        return False, "fail-closed：`timeline.md` 读不出"
    rows = index_rows(idx_text)
    tl_moments = timeline_hard_moments(tl_text)
    if not tl_moments:
        return False, "fail-closed：`timeline.md` §1 硬时刻表解析不出任何行"

    # (a) 硬时刻：现取 INDEX 的值，再与文档逐位比。
    for label, sid in HARD_MOMENTS:
        if sid not in rows:
            problems.append(f"`INDEX.md` §{sid} 行不存在")
            continue
        want = index_moments(rows[sid]).get(norm_label(label))
        if want is None:
            problems.append(f"§{sid} 里解析不出「{label}」的时刻")
            continue
        got = tl_moments.get(norm_label(label))
        if got is None:
            problems.append(f"文档漏了硬时刻「{label}」")
            continue
        if got[0] != want:
            problems.append(f"硬时刻「{label}」EST：文档={got[0]} · 现取§{sid}={want}")
    notes.append(f"硬时刻 {len(HARD_MOMENTS)} 项 vs §2.6.1/§2.6.2 现取")

    # (b) 时长：文档 vs §2.6.5 现取。
    if "2.6.5" not in rows:
        problems.append("`INDEX.md` §2.6.5 行不存在")
        doc_dur = {}
    else:
        idx_dur = parse_two_durations(rows["2.6.5"])
        doc_dur = parse_two_durations(tl_text)
        for name, _a, _b in DURATIONS:
            if name not in idx_dur:
                problems.append(f"§2.6.5 里解析不出时长「{name}」")
            elif name not in doc_dur:
                problems.append(f"文档里解析不出时长「{name}」")
            elif abs(doc_dur[name] - idx_dur[name]) > 1e-6:
                problems.append(f"时长「{name}」：文档={doc_dur[name]} · 现取§2.6.5={idx_dur[name]}")

    # (c) 时长：再拿"由硬时刻现算的差"核一遍（INDEX 内部自洽性）。
    for name, a, b in DURATIONS:
        wa = tl_moments.get(norm_label(a))
        wb = tl_moments.get(norm_label(b))
        if not (wa and wb):
            problems.append(f"现算时长「{name}」缺端点")
            continue
        calc = hours_between(wa[0], wb[0])
        if name not in doc_dur:
            problems.append(f"现算时长「{name}」无法与文档比（文档那项没解析出）")
        elif abs(doc_dur[name] - calc) > 1e-6:
            problems.append(f"时长「{name}」：文档={doc_dur[name]} · 由硬时刻现算={calc:g}")
        notes.append(f"{name} 现算 {calc:g}h")
    detail = " · ".join(notes) + ("" if not problems else "  <<< " + " ; ".join(problems))
    return (not problems), detail


# ----------------------------------------------------------------------------- T2
def mistake_blocks(text):
    """按 `**失误 …**` 头切成块 ⇒ `[(头行, 块文本)]`。"""
    lines = text.splitlines()
    heads = [i for i, ln in enumerate(lines) if re.match(r"^\*\*失误\s", ln)]
    out = []
    for k, i in enumerate(heads):
        j = heads[k + 1] if k + 1 < len(heads) else len(lines)
        out.append((lines[i], "\n".join(lines[i:j])))
    return out


def check_t2(ms_text, idx_text):
    if ms_text is None:
        return False, "fail-closed：`phase-mistakes.md` 读不出"
    if idx_text is None:
        return False, "fail-closed：`INDEX.md` 读不出"
    valid_ids = set(index_rows(idx_text))
    if not valid_ids:
        return False, "fail-closed：`INDEX.md` 解析不出任何表格行 id"
    blocks = mistake_blocks(ms_text)
    if not blocks:
        return False, "fail-closed：`phase-mistakes.md` 解析不出任何「失误」块"
    problems, n_ref = [], 0
    for head, body in blocks:
        name = head.strip("*").split("：")[0]
        src_lines = [ln for ln in body.splitlines() if ln.strip().startswith("- 出处")]
        ids = []
        for ln in src_lines:
            ids += re.findall(r"§(\d+\.\d+(?:\.\d+)*)", ln)
        if not src_lines or not ids:
            problems.append(f"{name}：没有 `§id` 出处")
        if not re.search(r"\[(?:" + "|".join(GRADES) + r")\]", body):
            problems.append(f"{name}：没有分级标注")
        for i in ids:
            n_ref += 1
            if i not in valid_ids:
                problems.append(f"{name}：`§{i}` 在 `INDEX.md` 里现场解析不到")
    detail = (f"{len(blocks)} 条失误 · 出处 §id {n_ref} 处 · `INDEX.md` 表格行 {len(valid_ids)} 个"
              + ("" if not problems else "  <<< " + " ; ".join(problems)))
    return (not problems), detail


# ----------------------------------------------------------------------------- T3
def skill_tokens(text):
    """抽形如 `mcm-xxx` 的 token ⇒ `[(token, 行号, 行文本)]`。★ **排除路径片段**（`docs/mcm-…`）。"""
    out = []
    for ln_no, ln in enumerate(text.splitlines(), 1):
        for m in re.finditer(r"mcm-[a-z0-9]+(?:-[a-z0-9]+)*", ln):
            if m.start() > 0 and ln[m.start() - 1] in "/-\\":
                continue                              # 属路径（`docs/mcm-writing-discipline.md`）或长名片段
            out.append((m.group(0), ln_no, ln))
    return out


def check_t3(skill_md, tl_text, ms_text, skills_root):
    docs = [("SKILL.md", skill_md), ("timeline.md", tl_text), ("phase-mistakes.md", ms_text)]
    missing_docs = [n for n, t in docs if t is None]
    if missing_docs:
        return False, f"fail-closed：读不出 {missing_docs}"
    try:
        existing = {p.name for p in pathlib.Path(skills_root).iterdir() if p.is_dir()}
    except OSError as e:
        return False, f"fail-closed：`{skills_root}` 列不出（{type(e).__name__}）"
    if not existing:
        return False, f"fail-closed：`{skills_root}` 下没有任何目录"
    occ, unmarked, unseen = [], set(), set()
    for name, text in docs:
        for tok, ln_no, ln in skill_tokens(text):
            occ.append(tok)
            if tok in existing:
                continue
            unseen.add(tok)
            if BUILT not in ln:
                unmarked.add(f"{name}:{ln_no} `{tok}`（该行无「{BUILT}」）")
    if not occ:
        return False, "fail-closed：三份文档里一个 `mcm-*` skill 名都没抽到"
    detail = (f"点名 {len(occ)} 处 · 现存 skill 目录 {len(existing)} 个 · "
              f"不存在的名字 {len(unseen)} 个 {sorted(unseen)}"
              + ("" if not unmarked else "  <<< 未标「" + BUILT + "」：" + " ; ".join(sorted(unmarked))))
    return (not unmarked), detail


# ----------------------------------------------------------------------------- T4
def check_t4(tl_text):
    if tl_text is None:
        return False, "fail-closed：`timeline.md` 读不出"
    try:
        from zoneinfo import ZoneInfo
        est = ZoneInfo("America/New_York")
        bj = ZoneInfo("Asia/Shanghai")
    except Exception as e:                            # ImportError / ZoneInfoNotFoundError
        return False, f"fail-closed：`zoneinfo` 取不到时区库（{type(e).__name__}: {e}）"
    moments = timeline_hard_moments(tl_text)
    if not moments:
        return False, "fail-closed：`timeline.md` §1 硬时刻表解析不出任何行"
    problems, n = [], 0
    for label, (est_s, bj_s) in moments.items():
        if not re.fullmatch(DT, est_s) or not re.fullmatch(DT, bj_s):
            problems.append(f"「{label}」EST 或北京侧不是 `YYYY-MM-DD HH:MM` 形态")
            continue
        n += 1
        calc = (datetime.strptime(est_s, "%Y-%m-%d %H:%M").replace(tzinfo=est)
                .astimezone(bj).strftime("%Y-%m-%d %H:%M"))
        if calc != bj_s:
            problems.append(f"「{label}」EST {est_s} 现算→{calc} · 文档写 {bj_s}")
    detail = (f"{n} 行换算由 `zoneinfo` 现算比对（EST→Asia/Shanghai）"
              + ("" if not problems else "  <<< " + " ; ".join(problems)))
    return (not problems), detail


# ----------------------------------------------------------------------------- T5
def check_t5(tl_text, ms_text):
    if tl_text is None:
        return False, "fail-closed：`timeline.md` 读不出"
    if ms_text is None:
        return False, "fail-closed：`phase-mistakes.md` 读不出"
    problems, notes = [], []

    # A. 阶段边界：§4 声明"全是构造" + 每一条"为何切在…"的理由都带「构造」。
    seg4 = section(tl_text, "## 4.", "## 5.")
    if not seg4:
        problems.append("`timeline.md` 取不到 §4 阶段表段")
    else:
        if "全是构造" not in seg4:
            problems.append("§4 未声明阶段表「全是构造」")
        bullets = [ln for ln in seg4.splitlines() if re.match(r"^\s*-\s*\*\*为何", ln)]
        if not bullets:
            problems.append("fail-closed：§4 解析不出任何「为何切在…」的理由行")
        bad = [b[:24] for b in bullets if "「构造」" not in b]
        if bad:
            problems.append(f"这些阶段边界理由未带「构造」：{bad}")
        notes.append(f"§4 阶段边界理由 {len(bullets)} 条逐条带「构造」")

    # B. 每条失误的**归类**带「构造」：判**那一条「为什么归这个阶段」行**自己带没带，
    #    不判"整个块里有「构造」字样"——否则块内别处的一句「构造」会把漏标的那行掩盖过去。
    blocks = mistake_blocks(ms_text)
    if not blocks:
        problems.append("fail-closed：`phase-mistakes.md` 解析不出任何「失误」块")
    else:
        bad = []
        for h, b in blocks:
            rl = [ln for ln in b.splitlines() if ln.strip().startswith("- 为什么归这个阶段")]
            if not rl or "构造" not in rl[0]:
                bad.append(h.strip("*").split("：")[0])
        if bad:
            problems.append(f"这些失误块的「为什么归这个阶段」行未带「构造」：{bad}")
        notes.append(f"失误 {len(blocks)} 条的归类行逐条带「构造」")

    # C. 示例评分表处：官方那条"A Sample / 可按题目调整"限定。
    #    ★ **给结束标记**（= 下一个 `## ` 顶层小节）：本段原先扫到**文件尾**（无结束标记），
    #    那两条限定串就会在**小节之外**也被搜到 ⇒ 若将来在后面某个小节里复述它们，
    #    这里会**为错误的理由通过**（Task 2 复核登记的 Minor，Task 3 并入）。当前该小节是**最后一节**
    #    ⇒ 干净文档上的读数**不变**；改动只把搜索面收进小节内。
    rub = section(ms_text, "## 关于那份", "## ")
    if not rub:
        problems.append("fail-closed：`phase-mistakes.md` 取不到示例评分表那一节")
    else:
        for need in ("A Sample", "adjusting categories and points as needed"):
            if need not in rub:
                problems.append(f"示例评分表节缺官方限定串：{need!r}")
        notes.append("示例评分表节带 \"A Sample\" + \"adjusting categories and points as needed\"")
    detail = " · ".join(notes) + ("" if not problems else "  <<< " + " ; ".join(problems))
    return (not problems), detail


def main(argv=None):
    ap = argparse.ArgumentParser(description="`mcm-playbook` 机械层判据 T1–T5")
    ap.add_argument("--skill-md", default=str(DEFAULT_SKILL_MD))
    ap.add_argument("--timeline", default=str(DEFAULT_TIMELINE))
    ap.add_argument("--mistakes", default=str(DEFAULT_MISTAKES))
    ap.add_argument("--index", default=str(DEFAULT_INDEX))
    ap.add_argument("--skills-root", default=str(DEFAULT_SKILLS_ROOT))
    a = ap.parse_args(argv)

    idx_text = read_text(a.index)
    tl_text = read_text(a.timeline)
    ms_text = read_text(a.mistakes)
    skill_md = read_text(a.skill_md)

    rows = [
        ("T1", check_t1(idx_text, tl_text)),
        ("T2", check_t2(ms_text, idx_text)),
        ("T3", check_t3(skill_md, tl_text, ms_text, a.skills_root)),
        ("T4", check_t4(tl_text)),
        ("T5", check_t5(tl_text, ms_text)),
    ]
    print(f"判据对象：{pathlib.Path(a.timeline).parent.parent.name}/（SKILL.md + 2 references）")
    for rid, (ok, detail) in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {rid}  {detail}")
    bad = [rid for rid, (ok, _d) in rows if not ok]
    print("-" * 78)
    print(f"判据 {len(rows)} 条 · 红 {len(bad)} 条")
    print("RESULT: PASS" if not bad else f"RESULT: FAIL（{','.join(bad)}）")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
