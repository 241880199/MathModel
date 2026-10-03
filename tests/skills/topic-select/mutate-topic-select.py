#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/topic-select/check-topic-select.py` 的**变异驱动器**（实施计划 Task 2 · 硬要求 2）。

用法：  python tests/skills/topic-select/mutate-topic-select.py

## 它做什么

把**已知好产出**（`fixtures/good-output.md`）与**规范侧两份文档**（`SKILL.md` · `references/method.md`）
各取一份副本**逐条改坏**（**当场改、当场跑、当场判、然后收走**），断言检查器**点名红在那一条判据上**；
另设**必须仍绿**的射程边界对照。**每条判据 `S1`–`S6` 至少一条真红作证**（本仓硬规矩：判据只能从失败方向证明）。

- 每条变异**只碰 `build/` 下的副本**（仓内 gitignored 的临时目录，**不落 C 盘 / `%TEMP%`**），
  **不碰**仓内任何入库件；收尾逐件 `git hash-object` 自证"受保护件逐字节未变"。
- **被判对象由命令行覆盖**（`check-topic-select.py` 的 `--output` / `--skill-md` / `--method`）
  ⇒ 变异**不改入库件**、也**不需要"改回"**；"还原"由 blob 自证兑现。
- **期望集逐条写死**（不是"红了就算数"）：实际红的判据集合必须**恰好等于**该条声明的集合 ⇒
  "一条变异顺手带红别的判据"或"该红没红"都会被抓出来。
- **判据清单现取**（硬要求 3）：先把检查器在**干净输入**上跑一遍、把 `PASS|FAIL  <id>` 行读成 id 集合，
  再拿它当"全部判据"。**没有写死 `S1`–`S6` 的字面**——写死条数会让汇总表在判据增减时**静默归零**。
  变异若点名了**不在现取集合里**的判据 ⇒ 该条直接判失败（防"打错靶子还报绿"）。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望红 |
| :--- | :--- | :--- |
| `MUT-S1a` | 把 A 的一条支撑句**改写成同义句**（`in space and time` → `over space and time`）⇒ 不再是题面子串 | `S1` |
| `MUT-S1b` | 把 A 一条标签的**支撑句单元格清空**（标签行还在，引文没了） | `S1` |
| `MUT-S2a` | 改一个**组合历史数**（A 的组合出现 8 → 9 次） | `S2` |
| `MUT-S2b` | 改一个**模型历史数**（`2025 A` 用过 `Archard Law` 5 → 6 篇） | `S2` |
| `MUT-S3a` | 把 **`轴 3 · 拥挤风险` 的可核性从【判断】改成【读数】** | `S3` |
| `MUT-S4a` | **删掉「- 推翻条件：…」行** | `S4` |
| `MUT-S5a` | `method.md` 的**时间盒**（`默认时间盒：≤2 小时` → 到点为止） | `S5` |
| `MUT-S5b` | `SKILL.md` 的**契约时间盒**（两处 `≤2 小时` 全删） | `S5` |
| `MUT-S6a` | 把**禁令改写成坏推理**（`不许拿…代理…人数` → `获奖论文多的题，选它的人就少`） | `S6` |
| `MUT-FC1` | **fail-closed**：`--output` 指向不存在的文件 | `S1`,`S2`,`S3`,`S4` |
| `MUT-FC2` | **fail-closed**：`--problems` 指向不存在的路径 | `S1` |
| `MUT-FC3` | **fail-closed**：`--corpus` 指向不存在的目录 | `S2` |
| `MUT-FC4` | **fail-closed**：`--method` 指向不存在的文件 | `S5`,`S6` |
| `CTRL-GREEN-a` | 射程边界：只改 A 的**轴 2 依据文字**（不碰轴名 / 可核性标记） | （无） |
| `CTRL-GREEN-b` | 射程边界：改**推荐点名的题号**（A → B，推翻条件不动） | （无） |
| `CTRL-GREEN-c` | 射程边界：**新增一条标签行**且支撑句是题面子串 | （无） |
| `CTRL-GREEN-d` | 射程边界：只改 `method.md` 里**与时间盒/禁令无关**的散文 | （无） |

★ `MUT-S1a` 与 `MUT-S1b` 打的是 `S1` 的**两臂**：**句子在不在题面里**（改写）vs **有没有句子**（清空）。
★ `MUT-S2a` 与 `MUT-S2b` 打的是 `S2` 的**两臂**：**组合计数**（现取 `PROBLEM_TYPES.md`） vs
**模型篇数**（现取 `MODEL_MAP.md`）。
★ `MUT-S5a` 与 `MUT-S5b` 打的是 `S5` 的**两臂**：`method.md` 的**默认值** vs `SKILL.md` 的**契约值**
（两处都判 ⇒ 删任一处即红）。
★ `MUT-FC1`–`MUT-FC4` 打的是**读不出即红**（不是"内容不合规"）。
**其它读失败入口**（题面目录里无合法字母 / 承重结构解析空）**本表未逐条覆盖**（**不声称穷尽**）。

## 合计行形态

照 `mutate-playbook.py` / `mutate-table-style.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**
（末行放"运行完整性"读数）。
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]      # tests/skills/topic-select/x.py → 仓根
CHK = ROOT / "tests/skills/topic-select/check-topic-select.py"
GOOD = ROOT / "tests/skills/topic-select/fixtures/good-output.md"
PROBLEMS_DIR = ROOT / "tests/skills/topic-select/fixtures/problems"
PROBLEM_FILES = tuple(sorted(PROBLEMS_DIR.glob("*.md")))
SKILL_MD = ROOT / ".claude/skills/mcm-topic-select/SKILL.md"
METHOD = ROOT / ".claude/skills/mcm-topic-select/references/method.md"
CORPUS = ROOT / "corpus/papers"
BUILD = ROOT / "build/topic-select-mut"                 # ★ 临时目录落仓内 `build/`
# 变异**不许**动的入库件（收尾逐件比对 blob）
GUARDED = (CHK, GOOD, SKILL_MD, METHOD,
           CORPUS / "PROBLEM_TYPES.md", CORPUS / "MODEL_MAP.md") + PROBLEM_FILES

FLAG = {"output": "--output", "skill_md": "--skill-md", "method": "--method",
        "problems": "--problems", "corpus": "--corpus"}
BASE = {"output": GOOD, "skill_md": SKILL_MD, "method": METHOD}
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def run_checker(overrides=None):
    """跑检查器；`overrides` = `{"output": path, …}`。返回 `(rc, stdout, {id: PASS|FAIL})`。"""
    args = [sys.executable, str(CHK)]
    for key, val in (overrides or {}).items():
        args += [FLAG.get(key, key), str(val)]
    pr = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
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


def _drop_line(prefix):
    """删掉**所有**以 `prefix`（剥掉行首空白后）开头的行 ⇒ 缺了承重行。"""
    def f(src):
        lines = src.splitlines(keepends=True)
        out = [l for l in lines if not l.lstrip().startswith(prefix)]
        if len(out) == len(lines):
            raise AssertionError(f"基准里找不到以 {prefix!r} 开头的行")
        return "".join(out)
    return f


def _break_prohibition(src):
    """把**禁令那段**（`不许拿 … 人数`）整段换成坏推理 ⇒ `S6` 的禁令臂红。"""
    m = re.search(r"不许拿.{0,50}人数", src)
    if not m:
        raise AssertionError("基准 `method.md` 里找不到禁令片段（不许拿…人数）")
    return src[:m.start()] + "获奖论文多的题，选它的人就少" + src[m.end():]


def _add_row(src):
    """在某条标签行后**新增一条**合法标签行（支撑句是题面子串）⇒ 必须仍绿。"""
    old = ('| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** '
           '| *"Develop a model of the temperature of the coffee in space and time as it cools"* |')
    if old not in src:
        raise AssertionError("基准产出里找不到要追加在其后的标签行")
    extra = ('\n| `核心` **3 优化 · 3.1 连续/非线性** '
             '| *"keep the temperature as close as possible to the initial temperature"* |')
    return src.replace(old, old + extra, 1)


class Mutation:
    """一条变异：把变换加到**某份文件的副本**上，断言红的判据集合**恰好**是 `expect`。"""

    def __init__(self, mid, desc, target, transform, expect):
        self.mid, self.desc, self.target = mid, desc, target
        self.transform, self.expect = transform, set(expect)

    def run(self, tmpdir):
        src = BASE[self.target].read_bytes().decode("utf-8")
        new = self.transform(src)
        if new == src:
            return False, f"驱动器自己报错：变换没有改变文本（{self.mid}）"
        d = tmpdir / self.mid
        d.mkdir(parents=True, exist_ok=True)
        p = d / BASE[self.target].name
        p.write_bytes(new.encode("utf-8"))                   # 一律 write_bytes（全 LF）
        rc, out, verdict = run_checker({self.target: p})
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == self.expect)
        note = "" if ok else f"   <<< 期望红 {sorted(self.expect)} · 实红 {sorted(actual)}"
        detail = (f"变换：{self.desc}（副本 = {p.name}）\n"
                  f"      期望红 = {sorted(self.expect) or '（无，必须全绿）'} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)} {note}\n"
                  + _raw(f"check-topic-select.py {FLAG[self.target]} {self.mid}/{p.name}", rc, out))
        return ok, detail


class PathMutation:
    """一条 **fail-closed** 变异：把某个输入指向**不存在**的路径 ⇒ 依赖它的判据**必须红**。"""

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
                  + _raw(f"check-topic-select.py {FLAG[self.key]} {missing.name}", rc, out))
        return ok, detail


MUTATIONS = [
    Mutation("MUT-S1a", "把 A 的一条支撑句改写成同义句（in space and time → over space and time）",
             "output", _sub("the coffee in space and time as it cools",
                            "the coffee over space and time as it cools"), {"S1"}),
    Mutation("MUT-S1b", "把 A 一条标签的支撑句单元格清空",
             "output", _sub('*"determine the best strategy the person can adopt to keep the '
                            'temperature as close as possible to the initial temperature"*', ""), {"S1"}),
    Mutation("MUT-S2a", "改一个组合历史数（A 的组合出现 8 → 9 次）",
             "output", _sub("× `无数据(纯机理/假设)`，出现 8 次",
                            "× `无数据(纯机理/假设)`，出现 9 次"), {"S2"}),
    Mutation("MUT-S2b", "改一个模型历史数（2025 A 用过 Archard Law 5 → 6 篇）",
             "output", _sub("用过模型 `Archard Law`，5 篇", "用过模型 `Archard Law`，6 篇"), {"S2"}),
    Mutation("MUT-S3a", "把「轴 3 · 拥挤风险」的可核性从【判断】改成【读数】",
             "output", _sub("轴 3 · 拥挤风险【判断】", "轴 3 · 拥挤风险【读数】"), {"S3"}),
    Mutation("MUT-S4a", "删掉「- 推翻条件：…」行",
             "output", _drop_line("- 推翻条件："), {"S4"}),
    Mutation("MUT-S5a", "method.md 的默认时间盒（默认时间盒：≤2 小时 → 到点为止）",
             "method", _sub("默认时间盒：≤2 小时", "默认时间盒：到点为止"), {"S5"}),
    Mutation("MUT-S5b", "SKILL.md 的契约时间盒（两处 `≤2 小时` 全删 → 两小时）",
             "skill_md", _sub("≤2 小时", "两小时", 99), {"S5"}),
    Mutation("MUT-S6a", "把禁令改写成坏推理（不许拿…代理…人数 → 获奖论文多的题，选它的人就少）",
             "method", _break_prohibition, {"S6"}),
]

FAILCLOSED = [
    PathMutation("MUT-FC1", "`--output` 指向不存在的文件 ⇒ 产出侧四条判据全部读失败即红",
                 "output", {"S1", "S2", "S3", "S4"}),
    PathMutation("MUT-FC2", "`--problems` 指向不存在的路径 ⇒ 题面读不出即红",
                 "problems", {"S1"}),
    PathMutation("MUT-FC3", "`--corpus` 指向不存在的目录 ⇒ 语料现取不出即红",
                 "corpus", {"S2"}),
    PathMutation("MUT-FC4", "`--method` 指向不存在的文件 ⇒ 规范侧两条读失败即红",
                 "method", {"S5", "S6"}),
]

CONTROLS = [
    Mutation("CTRL-GREEN-a", "射程边界：只改 A 的轴 2 依据文字（不碰轴名 / 可核性标记）",
             "output", _sub("一维/二维传热方程数值求解属中等难度", "传热方程数值求解属中等难度"), set()),
    Mutation("CTRL-GREEN-b", "射程边界：改推荐点名的题号 A → B（推翻条件不动）",
             "output", _sub("- 推荐：题 A", "- 推荐：题 B"), set()),
    Mutation("CTRL-GREEN-c", "射程边界：新增一条标签行且支撑句是题面子串",
             "output", _add_row, set()),
    Mutation("CTRL-GREEN-d", "射程边界：只改 method.md 里与时间盒/禁令无关的散文",
             "method", _sub("人多的题会把好答案淹掉。", "人多的题会把好答案淹掉（这是常识）。"), set()),
]


def main():
    print("=" * 78)
    print("变异驱动器 · check-topic-select.py（mcm-topic-select）：判据 S1–S6 逐条打红 + fail-closed 打红 "
          f"+ {len(CONTROLS)} 条对照（必须绿）")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    # 前置：干净输入必须**全绿**，并**现取**判据清单（硬要求 3：不写死 S1–S6）。
    rc0, out0, v0 = run_checker()
    criteria = sorted(v0)
    base_ok = rc0 == 0 and criteria and all(v0.get(i) == "PASS" for i in criteria)
    print(f"\n前置（干净产出 + 规范侧）：exit={rc0} · 现取判据清单 = {criteria} · "
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
        print(f"  {p.relative_to(ROOT).as_posix():<62} blob {now}  "
              f"{'== 变异前' if now == guarded_before[p] else '!= 变异前 <<<'}")
    print(f"  受保护件逐个 blob 还原: {byte_ok}")
    print(f"  变异后复跑（干净输入）：exit={rerun_rc} · "
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
    print(f"MUT: {n_mut}/{len(mut_ids)} 达预期（判据打红：S1 改写+清空 / S2 组合数+模型篇数 / "
          f"S3 判断改读数 / S4 删推翻条件 / S5 method 默认值+SKILL 契约值 / S6 禁令改坏）"
          + ("" if not [x for x in failed if x in mut_ids] else f"（未达预期：{', '.join(x for x in failed if x in mut_ids)}）"))
    print(f"MUT: {n_fc}/{len(fc_ids)} 达预期（fail-closed：output / problems / corpus / method 读不出即红）"
          + ("" if not [x for x in failed if x in fc_ids] else f"（未达预期：{', '.join(x for x in failed if x in fc_ids)}）"))
    print(f"MUT: 对照 {n_ctl}/{len(ctl_ids)} 达预期（必须绿：轴依据措辞 / 推荐题号 / 新增合法标签行 / 规范散文）"
          + ("" if not [x for x in failed if x in ctl_ids] else f"（未达预期：{', '.join(x for x in failed if x in ctl_ids)}）"))
    print(f"MUT: {n_mut + n_fc + n_ctl}/{len(mut_ids) + len(fc_ids) + len(ctl_ids)} 达预期（合计）")
    # ★ 合计行**不是末行**（照先例）：末行放"运行完整性"读数。
    print(f"RUN: 受保护件 blob 逐件还原={byte_ok} · 干净输入复跑 exit={rerun_rc} · "
          f"判据清单现取 {len(criteria)} 条 {criteria} · "
          f"变异点名了清单外的判据 {bad_target or '无'} · "
          f"全仓 `git status --short` {'空' if not dirty else '非空 <<< ' + '; '.join(dirty)}")
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty and not bad_target) else 1


if __name__ == "__main__":
    sys.exit(main())
