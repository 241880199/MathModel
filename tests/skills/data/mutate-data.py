#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/data/mutate-data.py` —— `check-data.py` 的**变异驱动器**。

用法：  python tests/skills/data/mutate-data.py

它做什么
--------
逐对跑 `samples/<判据号>/{comply,violate}/` 的夹具（`data-sources.md` + `paper.md`），
断言**三条**（`GC8`，缺一不可）：

* **断言 ① 每条判据至少红过一次**：`violate` 侧必须把**它自己那条**判 `FAIL`
  （**且只红它自己那条** —— 否则"打红"会退化：别的判据连带红也算过）。
* **断言 ② 每条判据的合规侧确实绿**：`comply` 侧必须**全 `PASS`**（防"连好产物也判红"）。
* **断言 ③ 判据总数 == `samples/` 下一级目录数** —— **分母不是常量**：
  左 = 检查器 `--scope artifact` **现取**到的判据号集合；右 = `samples/` 下的**一级目录名**集合；
  两边**集合相等**才算过。删掉检查器里任一条判据声明 ⇒ 左少一个；删掉任一样例目录 ⇒ 右少一个；
  **两边都会当场红**（照本仓 `check-writing-discipline.py` 的 `E0` 口径）。
  ★ 该断言自带一条**自证**（`_ass3_ok` 探针）：喂一对不等集合必须返回 `False` —— 否则断言被架空。

另设**控制项**（不占 `samples/` 分母），压住 `N/A` 三分口径、**第四态**、模板守卫与 `DA2` 的 `N/A` 出口：

| 控制项 | 打的是 | 期望 |
| :--- | :--- | :--- |
| `CTRL-SELF` | 内检 `--scope self` | 三条自检全 `PASS`、`exit=0` |
| `CTRL-NA-MISSING` | **情形 A**：目标文件不存在 | `DA1`–`DA5` 全 `N/A`、`exit=0` |
| `CTRL-NA-NOSECTION` | **情形 B**：两节都不在 | `DA1`–`DA5` 全 `N/A`、`exit=0` |
| `CTRL-EMPTY-ROWS` | **情形 C**：节在但零数据行 | `DA1` 判 `FAIL`（空集不许判绿） |
| `CTRL-HEADER-BAD` | **第四态**：节在但表头不符 | `DA1`–`DA4` 判 `FAIL`（fail-closed） |
| `CTRL-DA2-NOREFS` | `DA2` 的 `N/A` 出口（不给 `--refs`） | `DA2` = `N/A`、其余 `PASS`、`exit=0` |
| `CTRL-TEMPLATE` | **模板守卫**：靶子 = `assets/data-source-table.md` | 出一条 `FAIL TEMPLATE`、`exit≠0` |

★ 内检三条（`SELF1`/`SELF2`/`SELF3`）也要**从失败方向证明**（`GC12`）—— 驱动器把 skill 目录**拷进
`build/`**、逐条改坏副本、再用 `--skill-dir <副本>` 跑内检，断言对位那条真红（**不动入库件**）：

| 变异 | 打的是 | 期望 |
| :--- | :--- | :--- |
| `CTRL-SELF-COPY` | 未改的 skill 副本 | `SELF1`–`SELF3` 全 `PASS`、`exit=0` |
| `MUT-SELF1` | 删掉副本 `SKILL.md` 的通用边界句 | `SELF1` → `FAIL` |
| `MUT-SELF2` | 把副本某 reference 里的指针改成不存在的文件 | `SELF2` → `FAIL` |
| `MUT-SELF3` | 把副本模板表头删一列 | `SELF3` → `FAIL` |

★ 临时件只落仓内 `build/m5dc-mut/`（gitignored），跑完即清。**判据本体与样例一概不动。**
★ 末行打印**可复跑的红/绿计数**。
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]        # tests/skills/data/x.py → 仓根
CHK = ROOT / ".claude/skills/mcm-data/check-data.py"
SKILL = ROOT / ".claude/skills/mcm-data"
SAMPLES = ROOT / "tests/skills/data/samples"
TEMPLATE = ROOT / ".claude/skills/mcm-data/assets/data-source-table.md"
BUILD = ROOT / "build/m5dc-mut"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

STATUS_RE = re.compile(r"^(PASS|FAIL|N/A)\s+(DA\d|SELF\d|TEMPLATE)\b")
SIDES = ("comply", "violate")

# 边界句（`check-data.py` 的 `SELF1` 比对串；此处用于造 `MUT-SELF1`）
GEN_BOUNDARY = "本 skill 给出数据来源与代码规范；最终判断与结论由队员负责。"
# 模板七列表头（用于造 `MUT-SELF3`）
HEADER_LINE = "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 | 确认 |"

# 控制项夹具（只落 build/）
NO_SECTION_MD = "# 一份没有契约节的来源表\n\n这里只有标题，两节都不在。\n"
EMPTY_ROWS_MD = (
    "# 节在但零数据行\n"
    "\n"
    "## 来源表\n"
    "\n"
    "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 | 确认 |\n"
    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    "\n"
    "## 清洗步骤\n"
    "\n"
    "1. 取数：从 `附件/x.csv` 取一列 —— 脚本 `work/s1.py`。\n"
)
NOREFS_MD = (
    "# 有效来源表（控制项：不给 --refs）\n"
    "\n"
    "## 来源表\n"
    "\n"
    "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 | 确认 |\n"
    "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
    "| https://data.worldbank.org/indicator/NY.GDP.MKTP.CD | 现价美元 GDP | 最新年份为估计值 "
    "| 2027-02-15 | 2 国际组织与学术 | AI | 已核（张三,2027-02-15） |\n"
    "\n"
    "## 清洗步骤\n"
    "\n"
    "1. 取数：从 `附件/x.csv` 取一列 —— 脚本 `work/s1.py`。\n"
)
# 第四态控制项夹具：`## 来源表` 在、但表头**缺一列**（少 `确认`）—— 见约定件 §5 情形 D。
# `--refs` 靶子里**含**该行的 `出处` URL ⇒ 若表头正常，`DA2` 本会 `PASS`；这里 `DA2` 判红
# 完全归因于"表头不符 ⇒ 无七列表"这一态，而非"URL 搜不到"。
HEADER_BAD_MD = (
    "# 表头不符（第四态）\n"
    "\n"
    "## 来源表\n"
    "\n"
    "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 |\n"
    "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    "| https://data.worldbank.org/indicator/NY.GDP.MKTP.CD | 现价美元 GDP | 最新年份为估计值 "
    "| 2027-02-15 | 2 国际组织与学术 | AI |\n"
    "\n"
    "## 清洗步骤\n"
    "\n"
    "1. 取数：从 `附件/x.csv` 取一列 —— 脚本 `work/s1.py`。\n"
)
HEADER_BAD_REFS_MD = (
    "# 第四态控制项的 `--refs` 靶子\n"
    "\n"
    "数据取自 https://data.worldbank.org/indicator/NY.GDP.MKTP.CD 。\n"
)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))          # 一律 write_bytes（全 LF）


def git_status():
    return subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                          capture_output=True, text=True).stdout


def run_checker(args):
    """跑检查器；返回 `(rc, stdout, {id: status})`。"""
    pr = subprocess.run([sys.executable, str(CHK)] + list(args), cwd=str(ROOT),
                        capture_output=True, text=True, encoding="utf-8",
                        errors="replace", env=ENV)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = STATUS_RE.match(line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def _raw(cmdline, rc, out):
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return "$ %s   → exit=%d\n%s" % (cmdline, rc, body)


def _sample_ids():
    """`samples/` 下的**一级目录名**（不筛 —— 多一个目录就该让断言 ③ 红）。"""
    return sorted(d.name for d in SAMPLES.iterdir() if d.is_dir())


def _ass3_ok(criteria, sample_ids):
    """断言 ③ 本体：两边**集合相等**。"""
    return set(criteria) == set(sample_ids) and len(criteria) == len(sample_ids)


# --------------------------------------------------------------------------
# 断言 ①②：逐对跑
# --------------------------------------------------------------------------

def run_pair(cid, criteria):
    """跑一对；返回 `(st, detail)`。`st ∈ {RED-OK, RED-BAD, GREEN-OK, GREEN-BAD}` 拼接后的两段。"""
    res = {}
    for side in SIDES:
        d = SAMPLES / cid / side
        args = ["--scope", "artifact", str(d / "data-sources.md"), "--refs", str(d / "paper.md")]
        rc, out, v = run_checker(args)
        if side == "comply":
            others = criteria
            ok = (rc == 0) and all(v.get(i) == "PASS" for i in others)
            want = {i: "PASS" for i in criteria}
        else:
            ok = (rc != 0) and (v.get(cid) == "FAIL") \
                and all(v.get(i) == "PASS" for i in criteria if i != cid)
            want = {i: ("FAIL" if i == cid else "PASS") for i in criteria}
        res[side] = (ok, rc, v, want, out, args)
    return res


# --------------------------------------------------------------------------
# 控制项
# --------------------------------------------------------------------------

def run_controls(base_verdict):
    """返回 `[(cid, desc, ok, detail), ...]`。"""
    out = []

    # CTRL-SELF
    rc, text, v = run_checker(["--scope", "self"])
    ok = (rc == 0) and all(v.get("SELF%d" % i) == "PASS" for i in (1, 2, 3))
    out.append(("CTRL-SELF", "内检 --scope self ⇒ 三条自检全 PASS、exit=0", ok,
                _raw("check-data.py --scope self", rc, text)))

    # CTRL-NA-MISSING（情形 A）
    missing = BUILD / "does-not-exist.md"
    rc, text, v = run_checker(["--scope", "artifact", str(missing)])
    ok = (rc == 0) and all(v.get(i) == "N/A" for i in base_verdict)
    out.append(("CTRL-NA-MISSING", "情形 A：目标文件不存在 ⇒ DA1–DA5 全 N/A、exit=0", ok,
                _raw("check-data.py --scope artifact %s" % missing.name, rc, text)))

    # CTRL-NA-NOSECTION（情形 B）
    nos = BUILD / "no-section.md"
    write(nos, NO_SECTION_MD)
    rc, text, v = run_checker(["--scope", "artifact", str(nos)])
    ok = (rc == 0) and all(v.get(i) == "N/A" for i in base_verdict)
    out.append(("CTRL-NA-NOSECTION", "情形 B：两节都不在 ⇒ DA1–DA5 全 N/A、exit=0", ok,
                _raw("check-data.py --scope artifact %s" % nos.name, rc, text)))

    # CTRL-EMPTY-ROWS（情形 C）
    emp = BUILD / "empty-rows.md"
    write(emp, EMPTY_ROWS_MD)
    rc, text, v = run_checker(["--scope", "artifact", str(emp)])
    ok = (rc != 0) and (v.get("DA1") == "FAIL")
    out.append(("CTRL-EMPTY-ROWS", "情形 C：节在但零数据行 ⇒ DA1 判 FAIL（空集不许判绿）", ok,
                _raw("check-data.py --scope artifact %s" % emp.name, rc, text)))

    # CTRL-HEADER-BAD（第四态：`## 来源表` 在场、但表头与 §1.1 不符）
    # ★ 断言的是**读 `## 来源表` 的那四条**（DA1–DA4）判 FAIL —— 与姊妺侧 `mutate-code.py` 的
    #   `CTRL-HEADER-BAD`（只断言读清单的 `CD3`/`CD6`）同族同形：**只钉被本态影响到的那几条**。
    #   `DA5` 读的是 `## 清洗步骤`、与本态无关 ⇒ 此处**断言它仍 PASS**（证明红是表头引起的、非整体崩）。
    # ★ 另断言判词里带**第四态特有的理由串**（`表头与 §1.1 不符`）—— 以把它与**情形 C**（"零数据行"，
    #   另一条也会判红的路径）**区分开**：若 D 分支失效而落到 C，理由串会变、本条即红。
    hb = BUILD / "headerbad"
    write(hb / "data-sources.md", HEADER_BAD_MD)
    write(hb / "paper.md", HEADER_BAD_REFS_MD)
    rc, text, v = run_checker(["--scope", "artifact", str(hb / "data-sources.md"),
                              "--refs", str(hb / "paper.md")])
    ok = (rc != 0) and all(v.get(i) == "FAIL" for i in ("DA1", "DA2", "DA3", "DA4")) \
        and (v.get("DA5") == "PASS") and ("表头与 §1.1 不符" in text)
    out.append(("CTRL-HEADER-BAD",
                "第四态：`## 来源表` 在但表头不符（缺一列）⇒ DA1–DA4 判 FAIL（理由串 `表头与 §1.1 不符`，"
                "与情形 C 的`零数据行`分开）；DA5 读的是 `## 清洗步骤`、仍 PASS（红只归于表头那一态）",
                ok,
                _raw("check-data.py --scope artifact %s --refs %s"
                     % ((hb / "data-sources.md").relative_to(ROOT).as_posix(),
                        (hb / "paper.md").relative_to(ROOT).as_posix()),
                     rc, text)))

    # CTRL-DA2-NOREFS（DA2 的 N/A 出口）
    nrf = BUILD / "norefs.md"
    write(nrf, NOREFS_MD)
    rc, text, v = run_checker(["--scope", "artifact", str(nrf)])
    ok = (rc == 0) and (v.get("DA2") == "N/A") \
        and all(v.get(i) == "PASS" for i in base_verdict if i != "DA2")
    out.append(("CTRL-DA2-NOREFS", "不给 --refs ⇒ DA2 = N/A、其余 PASS、exit=0", ok,
                _raw("check-data.py --scope artifact %s" % nrf.name, rc, text)))

    # CTRL-TEMPLATE（模板守卫）
    rc, text, v = run_checker(["--scope", "artifact", str(TEMPLATE)])
    ok = (rc != 0) and (v.get("TEMPLATE") == "FAIL")
    out.append(("CTRL-TEMPLATE", "模板守卫：靶子 = assets/data-source-table.md ⇒ FAIL TEMPLATE、exit≠0", ok,
                _raw("check-data.py --scope artifact %s" % TEMPLATE.relative_to(ROOT).as_posix(), rc, text)))

    # ---- 内检三条：拷副本、改坏、证明它真红（GC12）----
    out.extend(run_self_mutations())
    return out


def _fresh_skill_copy():
    dst = BUILD / "skill-copy"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(SKILL, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def _mutate(path, old, new):
    t = path.read_bytes().decode("utf-8")
    assert old in t, "驱动器自己报错：副本里找不到要改的串 %r" % old
    path.write_bytes(t.replace(old, new).encode("utf-8"))
    return t


def run_self_mutations():
    """把 skill 目录拷进 `build/` 改坏，逐条证明 `SELF1`/`SELF2`/`SELF3` 会红。返回结果列表。"""
    out = []

    # CTRL-SELF-COPY：未改副本 ⇒ 全 PASS
    d = _fresh_skill_copy()
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc == 0) and all(v.get("SELF%d" % i) == "PASS" for i in (1, 2, 3))
    out.append(("CTRL-SELF-COPY", "未改的 skill 副本 ⇒ SELF1–SELF3 全 PASS、exit=0", ok,
                _raw("check-data.py --scope self --skill-dir <副本>", rc, text)))

    # MUT-SELF1：删通用边界句
    d = _fresh_skill_copy()
    _mutate(d / "SKILL.md", GEN_BOUNDARY, "")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF1") == "FAIL")
    out.append(("MUT-SELF1", "删掉副本 SKILL.md 的通用边界句 ⇒ SELF1 = FAIL", ok,
                _raw("check-data.py --scope self --skill-dir <副本·去掉边界句>", rc, text)))

    # MUT-SELF2：把某 reference 的指针改成不存在的文件
    d = _fresh_skill_copy()
    _mutate(d / "references/finding-data.md", "references/citation.md", "references/does-not-exist.md")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF2") == "FAIL")
    out.append(("MUT-SELF2", "把副本某 reference 的指针改成不存在的文件 ⇒ SELF2 = FAIL", ok,
                _raw("check-data.py --scope self --skill-dir <副本·断指针>", rc, text)))

    # MUT-SELF3：把模板表头删一列
    d = _fresh_skill_copy()
    _mutate(d / "assets/data-source-table.md", HEADER_LINE,
            "| 出处 | 口径 | 局限 | 获取日期 | 可信度层级 | 取数方 |")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF3") == "FAIL")
    out.append(("MUT-SELF3", "把副本模板表头删一列 ⇒ SELF3 = FAIL", ok,
                _raw("check-data.py --scope self --skill-dir <副本·缺一列>", rc, text)))

    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("变异驱动器 · check-data.py（mcm-data）：判据 DA1–DA5 逐对打红 / 打绿 + 控制项")
    print("=" * 78)
    print("检查器 = %s" % CHK.relative_to(ROOT).as_posix())

    if not CHK.exists():
        print("RUN: 找不到检查器 %s ⇒ fail-closed" % CHK)
        return 1

    # ★ 驱动器自证（强口径）：自己建的容器 `build/m5dc-mut` —— 开工前不该在场、
    #    跑期间必须真的建过、跑完（清完）必须仍不在场；另看 `git status` 有无差值。
    status_before = git_status()
    container_pre = BUILD.exists()          # 开工前：本驱动器建的容器不该在场

    # ---- 现取判据清单（干净合规侧）+ 现取 samples 一级目录 ----
    rc0, out0, base = run_checker(
        ["--scope", "artifact",
         str(SAMPLES / "DA1/comply/data-sources.md"),
         "--refs", str(SAMPLES / "DA1/comply/paper.md")])
    criteria = sorted(k for k in base if k.startswith("DA"))
    sample_ids = _sample_ids()
    print("\n现取判据清单（合规侧 DA1/comply 上读到）= %s" % criteria)
    print("样本一级目录（samples/ 下）= %s" % sample_ids)

    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ fail-closed（检查器没出 DA* 行？）")
        return 1

    # ---- 断言 ③（含自证探针）----
    ass3 = _ass3_ok(criteria, sample_ids)
    probe_ok = (_ass3_ok(criteria, sample_ids + ["DA9"]) is False) and \
               (_ass3_ok(criteria + ["DA9"], sample_ids) is False)
    print("断言 ③（判据总数 == samples 一级目录数）：criteria=%d · sample_dirs=%d · %s"
          % (len(criteria), len(sample_ids), "OK" if ass3 else "FAIL <<<"))
    print("  自证探针（喂不等集合必返回 False）：%s" % ("OK" if probe_ok else "失败 <<<（断言被架空）"))

    # ---- 断言 ①②：逐对跑 ----
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 78)
    print("逐对结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    rows = []           # (cid, side, ok, detail)
    for cid in sample_ids:
        res = run_pair(cid, criteria)
        for side in SIDES:
            ok, rc, v, want, out, args = res[side]
            cmd = "check-data.py " + " ".join(args)
            tag = ("GREEN-" if side == "comply" else "RED-") + ("OK" if ok else "BAD")
            note = "" if ok else "   <<< 期望 %s · 实得 %s（exit=%d）" % (want, v, rc)
            print("%-9s %s/%s%s" % (tag, cid, side, note))
            print(_raw(cmd, rc, out))
            rows.append((cid, side, ok))

    # ---- 断言统计 ----
    red_ok = [cid for (cid, side, ok) in rows if side == "violate" and ok]
    green_ok = [cid for (cid, side, ok) in rows if side == "comply" and ok]
    red_bad = [cid for (cid, side, ok) in rows if side == "violate" and not ok]
    green_bad = [cid for (cid, side, ok) in rows if side == "comply" and not ok]
    ass1 = not red_bad and len(red_ok) == len(sample_ids)
    ass2 = not green_bad and len(green_ok) == len(sample_ids)

    # ---- 控制项 ----
    print("\n" + "=" * 78)
    print("控制项（N/A 三分 · 第四态 · 模板守卫 · DA2 的 N/A 出口 · 内检）")
    print("=" * 78)
    ctrls = run_controls(criteria)
    for cid, desc, ok, detail in ctrls:
        print("%-9s %s" % ("CTRL-OK" if ok else "CTRL-BAD", cid))
        print("       %s" % desc)
        print(detail)
    ctrl_bad = [c[0] for c in ctrls if not c[2]]

    # ---- 驱动器自证（强口径）：自建容器三态 + `git status` 差值 ----
    status_after = git_status()
    container_during = BUILD.exists()       # 清之前：必须为 True（否则"清了个不存在的东西"，自证被架空）
    shutil.rmtree(BUILD, ignore_errors=True)          # ★ 自己造的临时件当场清
    container_post = BUILD.exists()         # 清之后：必须为 False
    no_trace = (status_after == status_before) and (not container_pre) \
               and container_during and (not container_post)

    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print("断言 ① 每条判据至少红过一次：违规侧红 %d/%d %s"
          % (len(red_ok), len(sample_ids), "OK" if ass1 else "FAIL <<< " + ",".join(red_bad)))
    print("断言 ② 每条判据的合规侧确实绿：合规侧绿 %d/%d %s"
          % (len(green_ok), len(sample_ids), "OK" if ass2 else "FAIL <<< " + ",".join(green_bad)))
    print("断言 ③ 判据总数 == samples 一级目录数：%d == %d %s"
          % (len(criteria), len(sample_ids), "OK" if ass3 else "FAIL <<<"))
    print("控制项 %d/%d 达预期 %s"
          % (len(ctrls) - len(ctrl_bad), len(ctrls),
             "OK" if not ctrl_bad else "FAIL <<< " + ",".join(ctrl_bad)))
    print("驱动器自证：容器 build/m5dc-mut 跑前=%s · 跑期间=%s · 清完=%s · git status(非 ignored 面)差值=%s ⇒ %s"
          % (container_pre, container_during, container_post, status_after != status_before,
             "OK" if no_trace else "FAIL <<<（容器三态不符 或 git status 有差值）"))

    all_ok = ass1 and ass2 and ass3 and probe_ok and not ctrl_bad and no_trace
    print("-" * 78)
    print("RUN: 判据 %d 条 · 违规侧红 %d/%d · 合规侧绿 %d/%d · 分母(samples 一级目录)=%d · "
          "控制项 %d/%d · 断言③自证 %s · 驱动器自证 %s"
          % (len(criteria), len(red_ok), len(sample_ids),
             len(green_ok), len(sample_ids), len(sample_ids),
             len(ctrls) - len(ctrl_bad), len(ctrls),
             "OK" if probe_ok else "FAIL", "OK" if no_trace else "FAIL"))
    print("RESULT: %s" % ("PASS" if all_ok else "FAIL"))

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
