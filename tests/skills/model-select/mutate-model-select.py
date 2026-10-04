#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`.claude/skills/mcm-model-select/check-model-select.py` 的**变异驱动器**（实施计划 Task 13 · 硬要求 1）。

用法：  python tests/skills/model-select/mutate-model-select.py

## 它做什么

把**本 skill 的一整套入库件**（`SKILL.md` · `references/**` · `assets/**` · `tests/skills/model-select/verify/*.md`）
各取一份副本**逐条改坏**（**当场改、当场跑、当场判、然后收走**），断言检查器**点名红在那一条判据上**；
另设**必须仍绿**的射程边界对照（`CTRL-GREEN-*`）。**每条判据 `MS1`–`MS6` 至少一条真红作证**
（本仓硬规矩：判据只能从失败方向证明）。

- 每条变异**只碰 `build/` 下的副本**（仓内 gitignored 的临时目录，**不落 C 盘 / `%TEMP%`**），
  **不碰**仓内任何入库件；收尾逐件 `git hash-object` 自证"受保护件逐字节未变"。
- **被判对象由命令行覆盖** —— 检查器有 **`--skill-dir`** 与 **`--verify-dir`** ⇒ 变异**把副本目录喂给它**，
  **不改入库件、也无需"改回"**；"还原"由 blob 自证兑现。
- **期望集逐条写死**（不是"红了就算数"）：实际红的判据集合必须**恰好等于**该条声明的集合 ⇒
  "一条变异顺手带红别的判据"或"该红没红"都会被抓出来。
  ★ **两处例外，如实登记（不是放宽，是这型的语义）**：
  ① `MUT-MS2-shorthand` 打的是 **`MS2` 的"势"少一格**（**不是变红**）⇒ 声明红集 = 空（必须全绿），
     另加断言 `MS2` 的**势恰好少 1**；
  ② `MUT-EMPTY-TREE` / `MUT-EMPTY-LIB` 是**空集反证**（§5.2）⇒ 势=0 时的红集按实测写死；
     见下"空集反证"一节 —— **任务书 §"必查项"第 9 条只列了五行，实测"整树空"是六行**。
- **判据清单现取**（硬要求 3）：先把检查器在**干净输入**上跑一遍、把 `PASS|FAIL  <id>` 行读成 id 集合，
  再拿它当"全部判据"。**没有写死 `MS1`–`MS6` 的字面**——写死条数会让汇总表在判据增减时**静默归零**。
  变异若点名了**不在现取集合里**的判据 ⇒ 该条直接判失败（防"打错靶子还报绿"）。

## 面（`--scope`）的选择

`check-model-select.py` **必须**用 `--scope` 指名一个面。本驱动一律用 **`--scope class --class simulation`**：
`simulation` 是全库最小的一类（**4 个方法**）⇒ `MS1`/`MS3`/`MS4` 的**势 = 4**、跑得快（MATLAB 只 feval 4 个骨架）；
★ 而 **`MS2` 的扫描面与 `MS6` 的自洽面与 `--scope` 无关**（`MS2` 递归扫全库、`MS6` 逐类核索引↔`MAP.md`），
⇒ 拿这一类当探针**不影响** `MS2`/`MS6` 的读数（本驱动实测：`MS2` 势=53 · `MS6` 势=8 类）。
★ **`--scope all` 的判据集合与 `class` 面相同**（都是 `MS1`–`MS6`），本驱动不重复跑 `all`（那是收工门的事）。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望红 |
| :--- | :--- | :--- |
| `MUT-MS1-drop-cell` | 删掉一个方法文件的**六格之一**（`## ② 标准建模步骤` 标题） | `MS1` |
| `MUT-MS2-wrong-path` | 把一个**素材路径改错**（骨架 `.m` 里 `monte_carro.m` → `monte_carro_MISSING.m`） | `MS2` |
| `MUT-MS3-missing-ref` | **删掉一份参照记录**（`verify/monte_carlo.md` 整份删） | `MS3` |
| `MUT-MS3-drop-element` | 删掉**四要素里的一项**（`## ② 参照来源` 标题） | `MS3` |
| `MUT-MS4-broken-skeleton` | 把骨架改成**跑不通**（首行换成 `error(...)`；跑 MATLAB，慢） | `MS4` |
| `MUT-MS5-drop-boundary` | 删掉**边界声明**句（`…最终选择与结论由队员负责` → `…由用户负责`） | `MS5` |
| `MUT-MS6-ghost-method` | 索引里**加一个不存在的方法**行 | `MS6` |
| `MUT-MS2-shorthand` | 把一条引用的**全路径改回 `src/…` 简写** ⇒ **不在抽取面上**（**不是变红**） | （无红）· **`MS2` 势 −1** |
| `MUT-EMPTY-TREE` | **整个 skill-dir 副本清空**（空集反证 · §5.2） | `MS1`,`MS2`,`MS3`,`MS4`,`MS5`,`MS6` |
| `MUT-EMPTY-LIB` | **只清空方法库**（`references/` + `assets/`，留 `SKILL.md`）⇒ 诊断子例 | `MS1`,`MS3`,`MS4`,`MS6`（**`MS2` 仍绿**） |
| `CTRL-GREEN-a` | 射程边界：只改方法文件正文散文（不碰六格标题 / 路径） | （无） |
| `CTRL-GREEN-b` | 射程边界：只改参照记录里的**数值读数**（四要素标题不动） | （无） |
| `CTRL-GREEN-c` | 射程边界：只改骨架里的**数值参数**（骨架仍跑通） | （无） |
| `CTRL-GREEN-d` | 射程边界：只改 `SKILL.md` 里**与边界句 / `[官方]` 无关**的散文 | （无） |

## ★ 一处实测发现：方法文件里的 `corpus/` 串**未必落在 `MS2` 抽取面上**

`MS2` 的抽取语法是「**反引号内**、以 `corpus/` 或 `.claude/` 起始」。**实测**：`references/simulation/monte_carlo.md`
里两条 `corpus/algorithms/src/…/monte_carro.m` **没有被抽取到**（该文件的**反引号配对**被正文里的代码围栏
```` ```matlab ```` 打断 ⇒ 那些串落进"跨段"配对里）—— 该文件**只抽出 `.claude/skills/mcm-table/` 与
`.claude/skills/mcm-figure-choose/` 两条**（驱动器首跑 `MUT-MS2-wrong-path` 打在 `.md` 上时**实测红了 0 条**，
据此改为打在骨架 `.m` 上才真红）。⇒ 打 `MS2` 的变异**必须挑一条真的在抽取面上的串**
（本驱动改的是**骨架 `.m`** 里的 `monte_carro.m`，那条**确实被抽取**）。
★ 这不改判据 —— 是 `MS2` 的抽取面**比"人眼看反引号"要小**这一事实的登记（设计 §5.1 已有"不声称穷尽"的边界）。

## ★ 空集反证：**任务书第 9 条只列了五行，实测"整树空"是六行**（以实测为准，当场报告）

任务书 §"必查项"第 9 条写：**"把方法目录清空 ⇒ `MS1`/`MS2`/`MS3`/`MS4`/`MS6` 必须全红"**。
**实测（本驱动先跑的两个探针，读数照贴）**：
- **只清空方法库**（`references/` + `assets/`，**留 `SKILL.md`**） ⇒ 红集 = **{`MS1`,`MS3`,`MS4`,`MS6`}**，
  **`MS2` 仍绿**（势=3）—— 因为 `SKILL.md` 自身带 3 条 `corpus/` 反引号路径（`corpus/papers/MODEL_MAP.md`
  · `corpus/algorithms/src/` · `corpus/papers/`），**`MS2` 的抽取面非空**。
- **把整个 skill-dir 清空**（`SKILL.md` 也没了） ⇒ 红集 = **全六条** `{MS1,MS2,MS3,MS4,MS5,MS6}`。
⇒ 设计 §5.2 的口径是"**空树**（零文件 / 零路径 / 零参照 / 零骨架）⇒ 这几条必须真的红" —— 它在"**整树清空**"下成立；
**第 9 条列五行是因为它列的是"原本平凡真的那五条"**（`MS5` 在空树下**本来就会红**，不在"待修"名单里）。
★ 本驱动把**两种切法都跑了**：`MUT-EMPTY-TREE`（整树空 · 六行全红 · **满足第 9 条的"`MS2` 必须红"**）与
`MUT-EMPTY-LIB`（只清库 · 四行红 · 登记"`MS2` 仍绿"这一**真读数**）。

## 合计行形态

照 `mutate-topic-select.py` / `mutate-playbook.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**
（末行放"运行完整性"读数）。
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]      # tests/skills/model-select/x.py → 仓根
SKILL = ROOT / ".claude/skills/mcm-model-select"
CHK = SKILL / "check-model-select.py"
VERIFY = ROOT / "tests/skills/model-select/verify"
BUILD = ROOT / "build/model-select-mut"                 # ★ 临时目录落仓内 `build/`

SCOPE = "class"                                          # ★ 探针面：最小的一类
CLS = "simulation"

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def _guarded_files():
    """变异**不许**动的入库件：整棵 skill 树（去掉 `__pycache__`）+ 全部参照记录。"""
    out = [CHK]
    for base in (SKILL, VERIFY):
        for p in sorted(base.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                out.append(p)
    seen, res = set(), []
    for p in out:
        if p not in seen:
            seen.add(p)
            res.append(p)
    return tuple(res)


GUARDED = _guarded_files()


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def run_checker(skill_dir, verify_dir):
    """跑检查器（`--scope class --class simulation`）。返回 `(rc, stdout, {id: PASS|FAIL}, ms2_pot)`。"""
    args = [sys.executable, str(CHK), "--scope", SCOPE, "--class", CLS,
            "--skill-dir", str(skill_dir), "--verify-dir", str(verify_dir)]
    pr = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(\S+)\s", line)
        if m:
            verdict[m.group(2)] = m.group(1)
    mp = re.search(r"MS2\s+势=(\d+)", pr.stdout)
    ms2_pot = int(mp.group(1)) if mp else None
    return pr.returncode, pr.stdout, verdict, ms2_pot


def _raw(mid, rc, out):
    cmd = ("check-model-select.py --scope class --class simulation "
           f"--skill-dir {mid}/skill --verify-dir {mid}/verify")
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return f"$ {cmd}   → exit={rc}\n{body}"


def _sub(old, new, count=1):
    def f(src):
        if old not in src:
            raise AssertionError(f"基准里找不到待改片段：{old!r}")
        return src.replace(old, new, count)
    return f


def _copy_tree(src, dst):
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


# ---------------------------------------------------------------- 变异对象
class _Case:
    mid = ""
    desc = ""
    expect = set()
    kind = "RED"

    def _prep(self, tmpdir):
        d = tmpdir / self.mid
        sk, vf = d / "skill", d / "verify"
        _copy_tree(SKILL, sk)
        _copy_tree(VERIFY, vf)
        return d, sk, vf

    def _judge(self, mid, rc, out, verdict, expect, extra_ok=True, extra_note=""):
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == set(expect)) and extra_ok
        if ok:
            note = ""
        elif actual != set(expect):
            note = f"   <<< 期望红 {sorted(expect) or '（无，必须全绿）'} · 实红 {sorted(actual)}"
        else:
            note = "   <<< 红集符合期望，但附加断言未过"
        detail = (f"变换：{self.desc}\n"
                  f"      期望红 = {sorted(expect) or '（无，必须全绿）'} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)}{extra_note}{note}\n"
                  + _raw(mid, rc, out))
        return ok, detail


class FileMutation(_Case):
    """把变换加到**某份文件在副本里的那份**上；断言红的判据集合**恰好**是 `expect`。"""

    def __init__(self, mid, desc, where, rel, transform, expect):
        self.mid, self.desc, self.where, self.rel = mid, desc, where, rel
        self.transform, self.expect = transform, set(expect)

    def _target(self, sk, vf):
        return (sk if self.where == "skill" else vf) / self.rel

    def run(self, tmpdir):
        _d, sk, vf = self._prep(tmpdir)
        t = self._target(sk, vf)
        src = t.read_bytes().decode("utf-8")
        new = self.transform(src)
        if new == src:
            return False, f"驱动器自己报错：变换没有改变文本（{self.mid}）"
        t.write_bytes(new.encode("utf-8"))               # 一律 write_bytes（全 LF）
        rc, out, verdict, _pot = run_checker(sk, vf)
        return self._judge(self.mid, rc, out, verdict, self.expect)


class DeleteMutation(_Case):
    """**删掉一份文件**（整份）—— 打 `MS3` 的"缺参照记录"臂。"""

    def __init__(self, mid, desc, where, rel, expect):
        self.mid, self.desc, self.where, self.rel = mid, desc, where, rel
        self.expect = set(expect)

    def run(self, tmpdir):
        _d, sk, vf = self._prep(tmpdir)
        t = (sk if self.where == "skill" else vf) / self.rel
        if not t.exists():
            return False, f"驱动器自己报错：待删文件不存在（{self.mid}）"
        t.unlink()
        rc, out, verdict, _pot = run_checker(sk, vf)
        return self._judge(self.mid, rc, out, verdict, self.expect)


class PotentialMutation(FileMutation):
    """**不是变红**：改一条引用的**全路径 → `src/…` 简写** ⇒ 该条**退出抽取面** ⇒
    红集必须为空、且 **`MS2` 的势恰好少 `delta`**（证明这个洞被"计数变化"暴露、不是静默的 · §2.2 规则 3 / §5.1）。"""
    kind = "POT"

    def __init__(self, mid, desc, where, rel, transform, base_pot, delta=-1):
        super().__init__(mid, desc, where, rel, transform, set())
        self.base_pot, self.delta = base_pot, delta

    def run(self, tmpdir):
        _d, sk, vf = self._prep(tmpdir)
        t = self._target(sk, vf)
        src = t.read_bytes().decode("utf-8")
        new = self.transform(src)
        if new == src:
            return False, f"驱动器自己报错：变换没有改变文本（{self.mid}）"
        t.write_bytes(new.encode("utf-8"))
        rc, out, verdict, ms2_pot = run_checker(sk, vf)
        if ms2_pot is None:
            extra_ok, extra_note = False, "   <<< 读不出 `MS2` 的势"
        else:
            got = ms2_pot - self.base_pot
            extra_ok = (got == self.delta)
            extra_note = f" · `MS2` 势 {self.base_pot} → {ms2_pot}（Δ={got}，期望 Δ={self.delta}）"
            if not extra_ok:
                extra_note += "   <<< 势的变化与期望不符"
        return self._judge(self.mid, rc, out, verdict, self.expect, extra_ok, extra_note)


class EmptyMutation(_Case):
    """**空集反证**：`mode="tree"` ⇒ 整棵 skill-dir 副本清空；`mode="lib"` ⇒ 只清 `references/` + `assets/`。"""
    kind = "EMPTY"

    def __init__(self, mid, desc, mode, expect):
        self.mid, self.desc, self.mode = mid, desc, mode
        self.expect = set(expect)

    def run(self, tmpdir):
        if self.mode == "tree":
            d = tmpdir / self.mid
            sk = d / "skill"
            if sk.exists():
                shutil.rmtree(sk)
            sk.mkdir(parents=True, exist_ok=True)         # ★ 空目录
            vf = d / "verify"
            _copy_tree(VERIFY, vf)
        else:
            _d, sk, vf = self._prep(tmpdir)
            for sub in ("references", "assets"):
                p = sk / sub
                if p.exists():
                    shutil.rmtree(p)
        rc, out, verdict, _pot = run_checker(sk, vf)
        return self._judge(self.mid, rc, out, verdict, self.expect)


MUTATIONS = [
    FileMutation("MUT-MS1-drop-cell",
                 "删掉六格之一：`references/simulation/monte_carlo.md` 的 `## ② 标准建模步骤` 标题",
                 "skill", "references/simulation/monte_carlo.md",
                 _sub("## ② 标准建模步骤", "## ② 建模步骤"), {"MS1"}),
    FileMutation("MUT-MS2-wrong-path",
                 "把一个素材路径改错：骨架 `assets/matlab/simulation/monte_carlo.m` 里的 `monte_carro.m` → "
                 "`monte_carro_MISSING.m`（该文件不在 HEAD）",
                 "skill", "assets/matlab/simulation/monte_carlo.m",
                 _sub("monte_carro.m", "monte_carro_MISSING.m"), {"MS2"}),
    DeleteMutation("MUT-MS3-missing-ref",
                   "删掉一份参照记录：整份去掉 `verify/monte_carlo.md`",
                   "verify", "monte_carlo.md", {"MS3"}),
    FileMutation("MUT-MS3-drop-element",
                 "删掉四要素里的一项：`verify/monte_carlo.md` 的 `## ② 参照来源` 标题（键仍在正文、标题去字）",
                 "verify", "monte_carlo.md",
                 _sub("## ② 参照来源", "## ② 来源"), {"MS3"}),
    FileMutation("MUT-MS4-broken-skeleton",
                 "把骨架改成跑不通：`assets/matlab/simulation/monte_carlo.m` 首行换成 `error(...)`",
                 "skill", "assets/matlab/simulation/monte_carlo.m",
                 _sub("if nargin < 1 || isempty(opts); opts = struct(); end",
                      "error('MUT-DRIVER: deliberate skeleton failure');"), {"MS4"}),
    FileMutation("MUT-MS5-drop-boundary",
                 "删掉边界声明：`SKILL.md` 的「…最终选择与结论由队员负责」→「…由用户负责」",
                 "skill", "SKILL.md",
                 _sub("最终选择与结论由队员负责", "最终选择与结论由用户负责"), {"MS5"}),
    FileMutation("MUT-MS6-ghost-method",
                 "索引里加一个不存在的方法：`references/simulation.md` 的方法清单加一行 `ghost.md`",
                 "skill", "references/simulation.md",
                 _sub("| ABM（多智能体） | `abm.m` | `references/simulation/abm.md` |",
                      "| ABM（多智能体） | `abm.m` | `references/simulation/abm.md` |\n"
                      "| 鬼方法 | `ghost.m` | `references/simulation/ghost.md` |"), {"MS6"}),
]

CONTROLS = [
    FileMutation("CTRL-GREEN-a",
                 "射程边界：只改方法文件正文散文（`monte_carlo.md`「（本方法最常犯的错）」→「（本方法最常犯的一个错）」）",
                 "skill", "references/simulation/monte_carlo.md",
                 _sub("（本方法最常犯的错）", "（本方法最常犯的一个错）"), set()),
    FileMutation("CTRL-GREEN-b",
                 "射程边界：只改参照记录的数值读数（`verify/monte_carlo.md` `7.784` → `7.780`，四要素标题不动）",
                 "verify", "monte_carlo.md",
                 _sub("7.784", "7.780"), set()),
    FileMutation("CTRL-GREEN-c",
                 "射程边界：只改骨架数值参数（`monte_carlo.m` 的 `ns` 末档 `64000` → `25600`，仍跑通）",
                 "skill", "assets/matlab/simulation/monte_carlo.m",
                 _sub("[1000 4000 16000 64000]", "[1000 4000 16000 25600]"), set()),
    FileMutation("CTRL-GREEN-d",
                 "射程边界：只改 `SKILL.md` 里与边界句 / `[官方]` 无关的散文（「## 什么时候用 / 不用」→「## 什么时候用、什么时候不用」）",
                 "skill", "SKILL.md",
                 _sub("## 什么时候用 / 不用", "## 什么时候用、什么时候不用"), set()),
]


def main():
    print("=" * 78)
    print("变异驱动器 · check-model-select.py（mcm-model-select）：判据 MS1–MS6 逐条打红 "
          f"+ 空集反证 + {len(CONTROLS)} 条对照（必须绿）")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    print(f"探针面 = --scope {SCOPE} --class {CLS}（全库最小的一类，4 个方法）")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True, exist_ok=True)

    # 前置：干净输入必须**全绿**，并**现取**判据清单（硬要求 3：不写死 MS1–MS6）。
    rc0, out0, v0, pot0 = run_checker(SKILL, VERIFY)
    criteria = sorted(v0)
    base_ok = rc0 == 0 and bool(criteria) and all(v0.get(i) == "PASS" for i in criteria)
    print(f"\n前置（干净输入 = 真仓）：exit={rc0} · 现取判据清单 = {criteria} · "
          f"{'全 PASS' if base_ok else '未全绿 <<< ' + str(sorted(v0.items()))}")
    print(f"       `MS2` 势（基准）= {pot0}")
    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ 无法变异（fail-closed）")
        return 1

    potential = [PotentialMutation(
        "MUT-MS2-shorthand",
        "把一条引用的全路径改回 `src/…` 简写（`assets/matlab/simulation/cellular_automata.m` 的 "
        "`corpus/algorithms/src/CellularAutomata元胞向量机/生命游戏/game_of_life.m` → `src/…`）"
        " ⇒ 该条**退出 `MS2` 抽取面**（不是变红，是**势少一格**）",
        "skill", "assets/matlab/simulation/cellular_automata.m",
        _sub("corpus/algorithms/src/CellularAutomata元胞向量机/生命游戏/game_of_life.m",
             "src/CellularAutomata元胞向量机/生命游戏/game_of_life.m"),
        pot0, delta=-1)]

    empty = [
        EmptyMutation("MUT-EMPTY-TREE",
                      "空集反证（整树空）：整个 skill-dir 副本清空（`SKILL.md` 也没了）⇒ "
                      "`MS1`–`MS6` 势全 0、**六行全红**",
                      "tree", {"MS1", "MS2", "MS3", "MS4", "MS5", "MS6"}),
        EmptyMutation("MUT-EMPTY-LIB",
                      "诊断子例（只清库）：清 `references/` + `assets/`、**留 `SKILL.md`** ⇒ "
                      "`MS2` 因 `SKILL.md` 自带 `corpus/` 指针**仍绿**（如实登记）",
                      "lib", {"MS1", "MS3", "MS4", "MS6"}),
    ]

    all_subs = MUTATIONS + potential
    bad_target = [mu.mid for mu in (all_subs + empty + CONTROLS)
                  if not mu.expect <= set(criteria)]

    rows, ctrl_rows, empty_rows, failed = [], [], [], []
    try:
        for mu in all_subs:
            try:
                ok, detail = mu.run(BUILD)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            tag = ("POT-OK" if ok else "POT-BAD") if mu.kind == "POT" else \
                  ("RED-OK" if ok else "RED-BAD")
            rows.append((tag, mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)
        for mu in empty:
            try:
                ok, detail = mu.run(BUILD)
            except (AssertionError, OSError) as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            empty_rows.append(("EMPTY-OK" if ok else "EMPTY-BAD", mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)
        for mu in CONTROLS:
            try:
                ok, detail = mu.run(BUILD)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            ctrl_rows.append(("GREEN-OK" if ok else "GREEN-BAD", mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)
    finally:
        shutil.rmtree(BUILD, ignore_errors=True)

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<11} {mid:<22} {desc}")
        print(detail)
    print("-" * 78)
    print("空集反证（势=0 ⇒ 必须红；不是「变红一条判据」、是整组 fail-closed）")
    for st, mid, desc, detail in empty_rows:
        print(f"{st:<11} {mid:<22} {desc}")
        print(detail)
    print("-" * 78)
    print("对照（不是判据变异：`GREEN` = 该绿）")
    for st, mid, desc, detail in ctrl_rows:
        print(f"{st:<11} {mid:<22} {desc}")
        print(detail)

    # ---------------------------------------------------------------- 还原自证
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    st = subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                        capture_output=True, text=True).stdout
    dirty = sorted(l for l in st.splitlines() if l.strip())
    rerun_rc, rerun_out, rerun_v, rerun_pot = run_checker(SKILL, VERIFY)

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    n_chg = 0
    for p in GUARDED:
        if guarded_after[p] != guarded_before[p]:
            print(f"  {p.relative_to(ROOT).as_posix():<62} blob {guarded_after[p]}  != 变异前 <<<")
            n_chg += 1
    print(f"  受保护件 {len(GUARDED)} 件逐个 blob 还原: {byte_ok}"
          + ("" if byte_ok else f"（{n_chg} 件不符）"))
    print(f"  变异后复跑（干净输入）：exit={rerun_rc} · "
          f"{'全 PASS' if all(rerun_v.get(i) == 'PASS' for i in criteria) else sorted(rerun_v.items())}")
    print(f"  全仓 `git status --short`:\n{st if st.strip() else '      （空）'}")

    red_ids = {m.mid for m in MUTATIONS}
    pot_ids = {m.mid for m in potential}
    emp_ids = {m.mid for m in empty}
    ctl_ids = {m.mid for m in CONTROLS}
    n_red = len(red_ids) - len([x for x in failed if x in red_ids])
    n_pot = len(pot_ids) - len([x for x in failed if x in pot_ids])
    n_emp = len(emp_ids) - len([x for x in failed if x in emp_ids])
    n_ctl = len(ctl_ids) - len([x for x in failed if x in ctl_ids])
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {n_red}/{len(red_ids)} 达预期（判据打红：MS1 删格 / MS2 路径错 / MS3 缺参照+缺要素 / "
          f"MS4 骨架跑不通 / MS5 删边界 / MS6 索引幽灵方法）"
          + ("" if not [x for x in failed if x in red_ids] else f"（未达预期：{', '.join(x for x in failed if x in red_ids)}）"))
    print(f"MUT: {n_pot}/{len(pot_ids)} 达预期（势变化：全路径→`src/…` 简写 ⇒ MS2 势 −1、红集空）"
          + ("" if not [x for x in failed if x in pot_ids] else f"（未达预期：{', '.join(x for x in failed if x in pot_ids)}）"))
    print(f"MUT: {n_emp}/{len(emp_ids)} 达预期（空集反证：整树空 ⇒ 六行全红；只清库 ⇒ 四行红、MS2 仍绿）"
          + ("" if not [x for x in failed if x in emp_ids] else f"（未达预期：{', '.join(x for x in failed if x in emp_ids)}）"))
    print(f"MUT: 对照 {n_ctl}/{len(ctl_ids)} 达预期（必须绿：方法正文 / 参照数值 / 骨架参数 / SKILL 散文）"
          + ("" if not [x for x in failed if x in ctl_ids] else f"（未达预期：{', '.join(x for x in failed if x in ctl_ids)}）"))
    print(f"MUT: {n_red + n_pot + n_emp + n_ctl}/{len(red_ids) + len(pot_ids) + len(emp_ids) + len(ctl_ids)} 达预期（合计）")
    # ★ 合计行**不是末行**（照先例）：末行放"运行完整性"读数。
    print(f"RUN: 受保护件 {len(GUARDED)} 件 blob 逐件还原={byte_ok} · 干净输入复跑 exit={rerun_rc} · "
          f"判据清单现取 {len(criteria)} 条 {criteria} · "
          f"变异点名了清单外的判据 {bad_target or '无'} · "
          f"全仓 `git status --short` {'空' if not dirty else '非空 <<< ' + '; '.join(dirty)}")
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty and not bad_target) else 1


if __name__ == "__main__":
    sys.exit(main())
