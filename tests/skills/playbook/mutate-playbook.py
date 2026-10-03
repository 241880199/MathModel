#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/playbook/check-playbook.py` 的**变异驱动器**（计划 Task 2 · 硬要求 2）。

用法：  python tests/skills/playbook/mutate-playbook.py

## 它做什么

把本 skill 的三份文档（`SKILL.md` · `references/timeline.md` · `references/phase-mistakes.md`）
各取一份副本**逐条改坏**（**当场改、当场跑、当场判、然后收走**），断言检查器**点名红在那一条判据上**；
另设**必须仍绿**的射程边界对照。**每条判据 `T1`–`T5` 至少一条真红作证**（本仓硬规矩：判据只能从失败方向证明）。

- 每条变异**只碰 `build/` 下的副本**（仓内 gitignored 的临时目录，**不落 C 盘 / `%TEMP%`**），
  **不碰**仓内任何入库件；收尾逐件 `git hash-object` 自证"受保护件逐字节未变"。
- **被判对象的三份文档由命令行覆盖**（`check-playbook.py` 的 `--timeline` / `--mistakes` / `--skill-md`）
  ⇒ 变异**不改入库件**、也**不需要"改回"**；"还原"由 blob 自证兑现。
- **期望集逐条写死**（不是"红了就算数"）：实际红的判据集合必须**恰好等于**该条声明的集合 ⇒
  "一条变异顺手带红别的判据"或"该红没红"都会被抓出来。
- **判据清单现取**（硬要求 3）：先把检查器在**干净文档**上跑一遍、把 `PASS|FAIL  <id>` 行读成 id 集合，
  再拿它当"全部判据"。**没有写死 `T1`–`T5` 的字面**——写死条数会让汇总表在判据增减时**静默归零**。
  变异若点名了**不在现取集合里**的判据 ⇒ 该条直接判失败（防"打错靶子还报绿"）。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望红 |
| :--- | :--- | :--- |
| `MUT-T1a` | `timeline.md` 的**时长**改成流传的 **96 小时**（99.0 → 96.0） | `T1` |
| `MUT-T1b` | `timeline.md` §1 的**开赛 EST** 改错（17:00 → 18:00）⇒ 硬时刻对不上 §2.6.2，且换算也随即变化 | `T1`,`T4` |
| `MUT-T2a` | 删掉某条失误**出处行里的 `§id`**（`§2.5.3`） | `T2` |
| `MUT-T2b` | 把 `§id` 改成**现场解析不到**的 `§9.9.9`（行号不动） | `T2` |
| `MUT-T3` | 把 `mcm-selfreview` 改成**不存在的名字** `mcm-nosuchskill` | `T3` |
| `MUT-T4` | `timeline.md` 的**北京换算**写成 `07:00`（停止修改 09:00 → 07:00） | `T4` |
| `MUT-T5a` | **抹掉一处「构造」**（阶段边界理由行） | `T5` |
| `MUT-T5b` | 抹掉示例评分表处的官方限定串 `adjusting categories and points as needed` | `T5` |
| `MUT-T5c` | 抹掉某条失误**归类行**的「构造」 | `T5` |
| `MUT-T5d` | 把两条官方限定串**搬出**「`## 关于那份`」节、改放到**其后新增的一个 `## ` 小节**里 ⇒ **专守 `T5` arm C 的「结束标记」** | `T5` |
| `MUT-FC1` | **fail-closed**：`--timeline` 指向不存在的文件 ⇒ 读不出即红（**不许静默绿**） | `T1`,`T3`,`T4`,`T5` |
| `MUT-FC2` | **fail-closed**：`--index` 指向不存在的文件 ⇒ 官方事实基线读不出即红 | `T1`,`T2` |
| `CTRL-GREEN-a` | 射程边界：只改一条失误的**措辞** ⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-b` | 射程边界：新增一个**不存在的名字但明写「未建」** ⇒ **必须仍绿**（`T3` 只抓"未标"） | （无） |
| `CTRL-GREEN-c` | 射程边界：只改阶段表**"在干什么"格**的措辞（不碰边界 / 「构造」） ⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-d` | 射程边界：新增一处**现存** skill 的提及（`mcm-abstract`） ⇒ **必须仍绿** | （无） |

★ `MUT-T1a` 与 `MUT-T1b` 打的是 `T1` 的**两层**：前者是**推算时长**（须与 §2.6.5 且与"由硬时刻现算的差"一致），
后者是**硬时刻逐位**（§1 表 vs §2.6.2 现取）。后者**连带** `T4` 真红 —— 这**不是驱动器出错**：
硬时刻的 EST 改了，同一行文档里的北京侧就不再是它的换算结果 ⇒ `T4` 本就该红（`expect` 里如实写死）。
★ `MUT-T2b` 与 `MUT-T2a` 打的是 `T2` 的**两臂**：`§id` **有没有** vs `§id` **解不解得出**；
两条都**不动任何行号** ⇒ 正面兑现"解析 `§id`，不比对行号"（计划 P3）。
★ `MUT-FC1`/`MUT-FC2` 打的是**读不出即红**（不是"内容不合规"）—— 本支无产物，fail-closed 就是"读不出"这一类。
**其它读失败入口（`--skill-md` / `--skills-root` / 承重表解析空）本表未逐条覆盖**（**不声称穷尽**）。

★ `MUT-T5d` 与其余 `T5` 变异**不同型**：它不是"抹掉某处的限定串"，而是把两条限定串**搬到目标小节之外**
（节内搬空、节外复述）。它**专为守住 `T5` arm C 的结束标记**而设：
**有结束标记 ⇒ 搜索面收在小节内、够不到节外那段 ⇒ `T5` 红**；
**若把结束标记去掉（改回扫到文件尾）⇒ 搜索面盖住节外那段 ⇒ 该串又被找到 ⇒ `T5` 不红 ⇒ 本条转 RED-BAD**。
⇒ 它让"把那个修复改回去"这件事**能被本驱动器抓到**（旧 `MUT-T5b` 抓不到：它删的是**节内**的串，
有没有结束标记**都红**，所以守不住结束标记本身）。

## 合计行形态

照 `mutate-table-style.py` / `mutate-figure-style.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**
（末行放"运行完整性"读数）。
"""
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]                 # tests/skills/playbook/x.py → 仓根
CHK = ROOT / "tests/skills/playbook/check-playbook.py"
SKILL_MD = ROOT / ".claude/skills/mcm-playbook/SKILL.md"
TIMELINE = ROOT / ".claude/skills/mcm-playbook/references/timeline.md"
MISTAKES = ROOT / ".claude/skills/mcm-playbook/references/phase-mistakes.md"
INDEX = ROOT / "corpus/official/INDEX.md"
BUILD = ROOT / "build/playbook-mut"                                # ★ 临时目录落仓内 `build/`
# 变异**不许**动的入库件（收尾逐件比对 blob）
GUARDED = (CHK, SKILL_MD, TIMELINE, MISTAKES, INDEX)

FLAG_FOR = {"timeline": "--timeline", "mistakes": "--mistakes", "skill_md": "--skill-md",
            "index": "--index", "skills_root": "--skills-root"}
PATH_FOR = {"timeline": TIMELINE, "mistakes": MISTAKES, "skill_md": SKILL_MD}


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def run_checker(overrides=None):
    """跑检查器；`overrides` = `{"timeline": path, …}`。返回 `(rc, stdout, {id: PASS|FAIL})`。"""
    args = [sys.executable, str(CHK)]
    for key, val in (overrides or {}).items():
        args += [FLAG_FOR[key] if key in FLAG_FOR else key, str(val)]
    pr = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(\S+)\s", line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def _raw(cmdline, rc, out):
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return f"$ {cmdline}   → exit={rc}\n{body}"


def _sub(old, new, count=1):
    def f(src):
        if old not in src:
            raise AssertionError(f"基准里找不到待改片段：{old!r}")
        return src.replace(old, new, count)
    return f


def _drop_word_on_class_line(src):
    """删掉**第一条**「- 为什么归这个阶段」行里的「构造」（其余块不动）⇒ `T5` 的归类臂红。"""
    lines = src.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("- 为什么归这个阶段") and "构造" in ln:
            lines[i] = ln.replace("构造", "判断", 1)
            return "\n".join(lines) + ("\n" if src.endswith("\n") else "")
    raise AssertionError("找不到带「构造」的「- 为什么归这个阶段」行")


def _rubric_limits_moved_out(src):
    """把两条官方限定串从「`## 关于那份`」**节内搬空**、改放到**其后新增的一个 `## ` 顶级小节**里。

    ★ 这条变换**专守 `T5` arm C 的结束标记**（Task 3 修复轮 · Minor 2）：
    - **有结束标记**（`section(ms_text, "## 关于那份", "## ")`）⇒ 搜索面收在小节内 ⇒ 节内已无该串 ⇒ `T5` 红。
    - **去掉结束标记**（改回扫到文件尾）⇒ 搜索面盖住节外那段 ⇒ 该串又被找到 ⇒ `T5` 不红。
    ⇒ 变换只产一份**副本文本**供驱动器变异，**不碰入库件**。
    """
    needles = (("A Sample", "示例评分表"),
               ("adjusting categories and points as needed", "按题目调整类别与分值"))
    lines = src.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.startswith("## 关于那份")), None)
    if start is None:
        raise AssertionError("找不到「## 关于那份」小节起点")
    head, body = lines[:start], list(lines[start:])
    for old, new in needles:
        if not any(old in ln for ln in body):
            raise AssertionError(f"节内找不到待搬走的限定串：{old!r}")
        body = [ln.replace(old, new) for ln in body]
    tail = ["",
            "## 附：那份示例评分表的官方限定（★ 只在节外复述；节内已搬空）",
            "",
            "官方原文写它是 \"A Sample\"，终审评委会 \"adjusting categories and points as needed\""
            "（按题目调整类别与分值）。"]
    return "\n".join(head + body + tail) + "\n"


class Mutation:
    """一条变异：把变换加到**某份文档的副本**上，断言红的判据集合**恰好**是 `expect`。"""

    def __init__(self, mid, desc, target, transform, expect):
        self.mid, self.desc, self.target = mid, desc, target
        self.transform, self.expect = transform, set(expect)

    def run(self, tmpdir):
        src = PATH_FOR[self.target].read_bytes().decode("utf-8")
        new = self.transform(src)
        if new == src:
            return False, f"驱动器自己报错：变换没有改变文本（{self.mid}）"
        d = tmpdir / self.mid
        d.mkdir(parents=True, exist_ok=True)
        p = d / PATH_FOR[self.target].name
        p.write_bytes(new.encode("utf-8"))                       # 一律 write_bytes（全 LF）
        rc, out, verdict = run_checker({self.target: p})
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == self.expect)
        note = "" if ok else f"   <<< 期望红 {sorted(self.expect)} · 实红 {sorted(actual)}"
        detail = (f"变换：{self.desc}\n"
                  f"      期望红 = {sorted(self.expect) or '（无，必须全绿）'} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)} {note}\n"
                  + _raw(f"check-playbook.py {FLAG_FOR[self.target]} {self.mid}/{p.name}", rc, out))
        return ok, detail


class PathMutation:
    """一条 **fail-closed** 变异：把某个读数源指向**不存在**的文件 ⇒ 依赖它的判据**必须红**。"""

    def __init__(self, mid, desc, key, expect):
        self.mid, self.desc, self.key = mid, desc, key
        self.expect = set(expect)

    def run(self, tmpdir):
        missing = tmpdir / f"{self.mid}-does-not-exist.md"
        rc, out, verdict = run_checker({self.key: missing})
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == self.expect)
        note = "" if ok else f"   <<< 期望红 {sorted(self.expect)} · 实红 {sorted(actual)}"
        detail = (f"变换：{self.desc}\n"
                  f"      期望红 = {sorted(self.expect)} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)} {note}\n"
                  + _raw(f"check-playbook.py {FLAG_FOR[self.key]} {missing.name}", rc, out))
        return ok, detail


MUTATIONS = [
    Mutation("MUT-T1a", "`timeline.md` 推算时长改成流传的 96 小时（99.0 → 96.0）",
             "timeline", _sub("= 99.0 小时", "= 96.0 小时"), {"T1"}),
    Mutation("MUT-T1b", "`timeline.md` §1 开赛 EST 改错（17:00 → 18:00）⇒ 对不上 §2.6.2，且换算随即变化",
             "timeline", _sub("| **开赛** | 2027-01-28 17:00 |", "| **开赛** | 2027-01-28 18:00 |"), {"T1", "T4"}),
    Mutation("MUT-T2a", "删掉某条失误**出处行的 `§id`**（`§2.5.3`）",
             "mistakes", _sub("§2.5.3〔`[官方]`〕（官方 10 条内容清单的", "〔`[官方]`〕（官方 10 条内容清单的"), {"T2"}),
    Mutation("MUT-T2b", "把一处 `§id` 改成**现场解析不到**的 `§9.9.9`（行号不动）",
             "mistakes", _sub("§2.5.3", "§9.9.9"), {"T2"}),
    Mutation("MUT-T3", "把 `mcm-selfreview` 改成**不存在的名字** `mcm-nosuchskill`",
             "timeline", _sub("mcm-selfreview", "mcm-nosuchskill", 99), {"T3"}),
    Mutation("MUT-T4", "`timeline.md` 北京换算写成 `07:00`（停止修改 09:00 → 07:00）",
             "timeline", _sub("| **停止修改** | 2027-02-01 20:00 | **2027-02-02 09:00** |",
                              "| **停止修改** | 2027-02-01 20:00 | **2027-02-02 07:00** |"), {"T4"}),
    Mutation("MUT-T5a", "**抹掉一处「构造」**（阶段边界理由行）",
             "timeline", _sub("★「构造」——建模与求解是**主体**", "★——建模与求解是**主体**"), {"T5"}),
    Mutation("MUT-T5b", "抹掉示例评分表处的官方限定串 `adjusting categories and points as needed`",
             "mistakes", _sub("adjusting categories and points as needed", "按题目自行调整"), {"T5"}),
    Mutation("MUT-T5c", "抹掉某条失误**归类行**的「构造」",
             "mistakes", _drop_word_on_class_line, {"T5"}),
    Mutation("MUT-T5d", "把两条官方限定串**搬出**「## 关于那份」节、改放到其后新增的 `## ` 小节里"
             "（守 `T5` arm C 的结束标记：去掉标记本条即转 RED-BAD）",
             "mistakes", _rubric_limits_moved_out, {"T5"}),
]

FAILCLOSED = [
    PathMutation("MUT-FC1", "`--timeline` 指向不存在的文件 ⇒ 读失败即红（不许静默绿）",
                 "timeline", {"T1", "T3", "T4", "T5"}),
    PathMutation("MUT-FC2", "`--index` 指向不存在的文件 ⇒ 官方事实基线读不出即红",
                 "index", {"T1", "T2"}),
]

CONTROLS = [
    Mutation("CTRL-GREEN-a", "射程边界：只改一条失误的**措辞**（不碰 `§id` / 分级 / 「构造」）",
             "mistakes", _sub("不评估可行性", "不评估其可行性"), set()),
    Mutation("CTRL-GREEN-b", "射程边界：新增一个**不存在但明写「未建」**的名字 ⇒ 必须仍绿（`T3` 只抓未标）",
             "timeline",
             _sub("别的时区要自己推，**本 skill 不替别的时区推**。",
                  "别的时区要自己推，**本 skill 不替别的时区推**（未来的 `mcm-future-thing` **未建**）。"),
             set()),
    Mutation("CTRL-GREEN-c", "射程边界：只改阶段表**“在干什么”格**的措辞（不碰边界 / 「构造」）",
             "timeline", _sub("通读六题、定题；", "通读六题并定题；"), set()),
    Mutation("CTRL-GREEN-d", "射程边界：新增一处**现存** skill 的提及（`mcm-abstract`）",
             "timeline",
             _sub("`mcm-selfreview` · `mcm-ai-disclosure` · `mcm-latex-format` |",
                  "`mcm-selfreview` · `mcm-ai-disclosure` · `mcm-latex-format` · `mcm-abstract` |"),
             set()),
]


def main():
    print("=" * 78)
    print("变异驱动器 · check-playbook.py（mcm-playbook）：判据 T1–T5 逐条打红 + fail-closed 打红 "
          f"+ {len(CONTROLS)} 条对照（必须绿）")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    # 前置：干净文档必须**全绿**，并**现取**判据清单（硬要求 3：不写死 T1–T5）。
    rc0, out0, v0 = run_checker()
    criteria = sorted(v0)
    base_ok = rc0 == 0 and criteria and all(v0.get(i) == "PASS" for i in criteria)
    print(f"\n前置（干净文档）：exit={rc0} · 现取判据清单 = {criteria} · "
          f"{'全 PASS' if base_ok else '未全绿 <<< ' + str(sorted(v0.items()))}")
    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ 无法变异（fail-closed）")
        return 1

    tmpdir = BUILD
    shutil.rmtree(tmpdir, ignore_errors=True)
    tmpdir.mkdir(parents=True, exist_ok=True)
    rows, ctrl_rows, failed = [], [], []
    bad_target = [mu.mid for mu in (MUTATIONS + FAILCLOSED + CONTROLS)
                  if not mu.expect <= set(criteria)]
    try:
        for mu in MUTATIONS + FAILCLOSED:
            try:
                ok, detail = mu.run(tmpdir)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            rows.append(("RED-OK" if ok else "RED-BAD", mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)
        for mu in CONTROLS:
            try:
                ok, detail = mu.run(tmpdir)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            ctrl_rows.append(("GREEN-OK" if ok else "GREEN-BAD", mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<11} {mid:<10} {desc}")
        print(detail)
    print("-" * 78)
    print("对照（不是判据变异：`GREEN` = 该绿）")
    for st, mid, desc, detail in ctrl_rows:
        print(f"{st:<11} {mid:<10} {desc}")
        print(detail)

    # ---------------------------------------------------------------- 还原自证
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    st = subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                        capture_output=True, text=True).stdout
    dirty = sorted(l for l in st.splitlines() if l.strip())
    rerun_rc, rerun_out, rerun_v = run_checker()

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print(f"  {p.relative_to(ROOT).as_posix():<58} blob {now}  "
              f"{'== 变异前' if now == guarded_before[p] else '!= 变异前 <<<'}")
    print(f"  受保护件逐个 blob 还原: {byte_ok}")
    print(f"  变异后复跑（干净文档）：exit={rerun_rc} · "
          f"{'全 PASS' if all(rerun_v.get(i) == 'PASS' for i in criteria) else sorted(rerun_v.items())}")
    print(f"  全仓 `git status --short`:\n{st if st.strip() else '      （空）'}")

    mut_ids = {m.mid for m in MUTATIONS}
    fc_ids = {m.mid for m in FAILCLOSED}
    ctl_ids = {m.mid for m in CONTROLS}
    n_mut = len(mut_ids) - len([x for x in failed if x in mut_ids])
    n_fc = len(fc_ids) - len([x for x in failed if x in fc_ids])
    n_ctl = len(ctl_ids) - len([x for x in failed if x in ctl_ids])
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {n_mut}/{len(mut_ids)} 红（判据 T1–T5 逐条打红：T1 时长+硬时刻 / T2 缺 §id + §id 解析不到 / "
          f"T3 名字不存在 / T4 换算错 / T5 抹「构造」×2 + 抹评分表限定 + 搬评分表限定出节（守结束标记））"
          + ("" if not [x for x in failed if x in mut_ids] else f"（未达预期：{', '.join(x for x in failed if x in mut_ids)}）"))
    print(f"MUT: {n_fc}/{len(fc_ids)} 红（fail-closed：读不出即红，不许静默绿）"
          + ("" if not [x for x in failed if x in fc_ids] else f"（未达预期：{', '.join(x for x in failed if x in fc_ids)}）"))
    print(f"MUT: 对照 {n_ctl}/{len(ctl_ids)} 达预期（必须绿：措辞 / 已标「未建」的名字 / 阶段表格 / 现存 skill 提及）"
          + ("" if not [x for x in failed if x in ctl_ids] else f"（未达预期：{', '.join(x for x in failed if x in ctl_ids)}）"))
    print(f"MUT: {n_mut + n_fc + n_ctl}/{len(mut_ids) + len(fc_ids) + len(ctl_ids)} 达预期（合计）")
    # ★ 合计行**不是末行**（照先例）：末行放"运行完整性"读数。
    print(f"RUN: 受保护件 blob 逐件还原={byte_ok} · 干净文档复跑 exit={rerun_rc} · "
          f"判据清单现取 {len(criteria)} 条 {criteria} · "
          f"变异点名了清单外的判据 {bad_target or '无'} · "
          f"全仓 `git status --short` {'空' if not dirty else '非空 <<< ' + '; '.join(dirty)}")
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty and not bad_target) else 1


if __name__ == "__main__":
    sys.exit(main())
