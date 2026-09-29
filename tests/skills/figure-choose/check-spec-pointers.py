#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""引用完整性检查器（Task 7）：**绘图家族的每个 skill 必须指向规范，且不许重述规范数值**。

用法：
  python tests/skills/figure-choose/check-spec-pointers.py
  python tests/skills/figure-choose/check-spec-pointers.py --skills-dir tests/skills/figure-choose/fixtures/fake-skills
  python tests/skills/figure-choose/check-spec-pointers.py --checker <改坏的 check-house-style.py 副本>   # 变异探针用

末行恒为 `RESULT: PASS` / `RESULT: PASS (…)` / `RESULT: FAIL（…）`；退出码 0 / 1。
每条判词一行，形态 `PASS|FAIL  <规则号>  <skill 名>  <读数>`（两条空格作分隔，不许靠列宽对齐 ——
变异驱动器要能**逐字**断言"哪条规则打中了哪个 skill"）。

## 两条判据**一条都不在这里实现**

它们已经在 `check-house-style.py` 里（`K2` 管指针、`K3` 管"不复述规范数值" + 中文数词臂），
本文件**import 复用**（`_load()` 惯用法，同 `check-house-style.py:77-80` / `house-metrics.py:81-82`），
**绝不抄一份实现**——抄件会随检查器漂移（本仓通则，见 `house-metrics.py` 头部"三支仪器"）。
本文件新增的只是**把 `_k2`/`_k3` 从「`--skill <单个文件>`」扩成「对一族 skill 的全扫」**。

复用之所以不用装配：`check-house-style.py` 靠**模块级全局** `DOC` / `SKILLS_ROOT` 等，默认值就是真件；
`_k2(txt)` / `_k3(txt)` **都只吃一个 `txt`**（`_k3` 自己读 `mod.DOC`）⇒ 逐份 skill 读成文本喂进去即可。

## 射程（**写实，别读成"覆盖了所有 skill"**）

- **规则①（`K2`）与规则②（`K3`）的作用域 = 绘图家族**，名字用 `FAMILY_RE` 现匹配：
  `mcm-plot-*` / `mcm-table` / `mcm-schematic`。将来真建出这些 skill 时**自动纳入**。
- **为什么不写"任何 skill"**（本任务书差异 2）：`K3` 的禁止串**只从 `house-style.md` 现取**，
  它假设被验文本是那份规范的**消费者**。把别人的 `§` 章节引用（`mcm-abstract` 的 "§7.2"、
  `mcm-selfreview` 的 "§1.1"）当规范数值是**口径偶合**，不是重述 —— 实测那样写会在**5 份里的 4 份上假红**。
  ★ **不许用"排除 `§` 前缀"来打补丁**：那等于给真正的重述开一个藏身处（把 `0.951` 写成 `§0.951` 即转绿）。
- `mcm-figure-choose`（规范的主人）不在家族里，故天然不受这两条约束。

## fail-closed（③）——锚在"扫到的 skill 总数"，**不锚在家族数**

- `--skills-dir` 不存在 / 不是目录 ⇒ **FAIL**（exit 1）；
- 目录存在但扫到 **0 个** `*/SKILL.md` ⇒ **FAIL**；
- **仪器探针**：把**空串**喂给 `K3`（`PASS  INSTR  K3@空串`）。空串什么都没重述 ⇒ 一个健康的仪器必须判绿；
  它若判红，只有三类可能：**参照物抽不齐**（`house-style.md` 抽不出小数、或抽不出上界 / 下界
  任一族的阈值、或标记表里出现认不出方向的形态），或 `K3` 中文数词臂的
  出处锚验失败 —— 都是"仪器取不到参照物"⇒ **FAIL**。（不证这一臂，"抽不到即 FAIL"就只是注释里的一句话。）
- 扫到 N ≥ 1 个 skill 而**绘图家族 0 个** ⇒ **PASS**，但末行**显式披露**且**逐行打印普查**
  （例：`RESULT: PASS (无对象：扫到 N 个 skill，绘图家族 0 个)`）—— 这是**家族还没建出来**时的形态；
  家族 ≥ 1 个之后走的是下一条（逐份跑判据），这一支不再触发。
  ★ 为什么不照 `_k6` 那条先例（"一个绘图 skill 都不点名 = 红"）：照搬会让本器在真仓**恒红**，
  那正是本任务要防的"恒真"的**镜像**。
- 家族 ≥ 1 个 ⇒ 逐个跑 `K2` + `K3`，任一红 ⇒ **FAIL**，且**逐条点名**是哪个 skill 的哪条规则。

## 本文件自己验不到的事（写实）

- **`K2`/`K3` 的口径本身**（判得对不对）不在这里验 —— 它们由 `check-house-style.py` 那一侧守
  （`M29`–`M41`）。本器只验"这两条在**一族 skill** 上真的会被触发、且不是恒真/恒红"。
- 真仓**已有绘图家族 skill**（`mcm-plot-python`）⇒ 只跑真仓时，逐份判据路径**会**执行。
  要证"缺指针 / 重述数值**分别**点名"，仍得靠 `--skills-dir` 指到假 skill 上
  （见 `mutate-figure-style.py` 的 `M43`–`M46`）。
"""
import argparse
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(__file__).resolve().parents[3]
SKILLS_ROOT = ROOT / ".claude/skills"          # 默认被扫的根（`--skills-dir` 可换）
DEFAULT_CHECKER = HERE / "check-house-style.py"
SKILL_FILE = "SKILL.md"
# 绘图家族的名字（与 `mcm-figure-choose/SKILL.md` 边界段点名的三个前缀同一集合）
FAMILY_RE = re.compile(r"^(?:mcm-plot-.+|mcm-table|mcm-schematic)$")
K2, K3 = "K2", "K3"


def _load(path, name):
    """本仓既有惯用法（带连字符的脚本名不能 `import`）：`spec_from_file_location` + `exec_module`。"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _shown(p):
    """证据里不写绝对路径：仓内的写相对路径，仓外的照原样。"""
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def census(skills_root):
    """扫 `*/SKILL.md`（**只一层**）⇒ `[(名字, 路径, 是否绘图家族)]`，按名字排序。"""
    return [(p.parent.name, p, bool(FAMILY_RE.match(p.parent.name)))
            for p in sorted(skills_root.glob("*/" + SKILL_FILE))]


def main():
    ap = argparse.ArgumentParser(description="引用完整性：绘图家族 skill 必须指向规范、且不许重述规范数值")
    ap.add_argument("--skills-dir", default=None,
                    help="被扫的 skill 根（默认 = 仓内 .claude/skills；相对路径按**仓根**解析）")
    ap.add_argument("--checker", default=None,
                    help="提供 `K2`/`K3` 的检查器（默认 = 同目录的 check-house-style.py；变异探针用）")
    a = ap.parse_args()
    root = pathlib.Path(a.skills_dir) if a.skills_dir else SKILLS_ROOT
    if not root.is_absolute():
        root = ROOT / root
    ck = pathlib.Path(a.checker) if a.checker else DEFAULT_CHECKER
    if not ck.is_absolute():
        ck = ROOT / ck

    bad = []
    print("引用完整性检查器（Task 7）· 判据 K2（指针）/ K3（不复述规范数值）**从 check-house-style.py "
          "import 复用**，本文件不重写")
    print(f"skills-dir = {_shown(root)} · checker = {_shown(ck)}")

    # ---------------- ③a fail-closed：目录不存在
    if not root.is_dir():
        print(f"FAIL  DIR       `--skills-dir` 不存在或不是目录：{_shown(root)}（fail-closed）")
        print("RESULT: FAIL（DIR:skills-dir）")
        return 1

    # ---------------- ③b fail-closed：仪器取不到参照物（空串探针）
    host = _load(ck.resolve(), "check_house_style")
    iok, idetail = host._k3("")          # 空串：什么都没重述 ⇒ 健康仪器必须判绿
    print(f"{'PASS' if iok else 'FAIL'}  INSTR  K3@空串  {idetail}")
    if not iok:
        bad.append("INSTR:K3")

    # ---------------- 普查（逐行打印；"当前无对象"必须由**本器自己**印出来，不是报告里声称）
    rows = census(root)
    fam = [r for r in rows if r[2]]
    print("-" * 78)
    print(f"普查：扫到 {len(rows)} 个 skill（{_shown(root)}/*/{SKILL_FILE}）· 绘图家族 {len(fam)} 个"
          f"（判据射程 = {FAMILY_RE.pattern}）")
    for name, _p, is_fam in rows:
        print(f"      {'家族  ' if is_fam else '非家族'}  {name}")
    if not rows:
        print(f"FAIL  CENSUS    一个 skill 都没扫到（目录里没有 `*/{SKILL_FILE}`）⇒ fail-closed")
        bad.append("CENSUS:0")

    # ---------------- 家族逐个跑 K2 + K3
    print("-" * 78)
    for name, path, _is_fam in fam:
        try:
            txt = path.read_bytes().decode("utf-8")
        except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
            print(f"FAIL  {K2}  {name}  读不出：{type(e).__name__}: {e}（fail-closed）")
            print(f"FAIL  {K3}  {name}  读不出：同上（fail-closed）")
            bad += [f"{K2}@{name}", f"{K3}@{name}"]
            continue
        for rid, fn in ((K2, host._k2), (K3, host._k3)):
            ok, detail = fn(txt)
            print(f"{'PASS' if ok else 'FAIL'}  {rid}  {name}  {detail}")
            if not ok:
                bad.append(f"{rid}@{name}")

    # ---------------- 判词
    # 「无对象」的解释只能印在 RESULT **之前**（末行恒为 RESULT 那一条），且只在真判绿时印：
    # 判红时印它会把"没判到"读成"没事"。
    if not bad and not fam:
        print("（规则①/②**本用例无对象**：逐份判据不执行 —— 这不是「通过」，是「没判到」；"
              "`mcm-plot-*` 真建出来那天，本器即生效）")
    print("-" * 78)
    print(f"扫到 {len(rows)} 个 skill（绘图家族 {len(fam)} 个）· 判据 {K2}/{K3} · 红 {len(bad)} 条")
    if bad:
        print(f"RESULT: FAIL（{','.join(sorted(set(bad)))}）")
    elif not fam:
        print(f"RESULT: PASS (无对象：扫到 {len(rows)} 个 skill，绘图家族 0 个)")
    else:
        print(f"RESULT: PASS (绘图家族 {len(fam)} 个，{K2}/{K3} 全绿)")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
