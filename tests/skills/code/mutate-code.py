#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/code/mutate-code.py` —— `check-code.py` 的**变异驱动器**。

用法：  python tests/skills/code/mutate-code.py

它做什么
--------
逐对跑 `samples/<判据号>/{comply,violate}/` 的夹具（`code/` 代码目录 + `appendix.md` 论文文件），
断言**三条**（`GC8`，缺一不可）：

* **断言 ① 每条判据至少红过一次**：`violate` 侧必须把**它自己那条**判 `FAIL`
  （**且只红它自己那条** —— 否则"打红"会退化：别的判据连带红也算过）。
* **断言 ② 每条判据的合规侧确实绿**：`comply` 侧必须**全 `PASS`**（防"连好产物也判红"）。
* **断言 ③ 判据总数 == `samples/` 下一级目录数** —— **分母不是常量**：
  左 = 检查器 `--scope artifact` **现取**到的判据号集合；右 = `samples/` 下的**一级目录名**集合；
  两边**集合相等**才算过。删掉检查器里任一条判据声明 ⇒ 左少一个；删掉任一样例目录 ⇒ 右少一个；
  **两边都会当场红**（照本仓 `check-writing-discipline.py` 的 `E0` 口径）。
  ★ 该断言自带一条**自证**（`_ass3_ok` 探针）：喂一对不等集合必须返回 `False` —— 否则断言被架空。

另设**控制项**（不占 `samples/` 分母），压住 `N/A` 三分 + 第四态、模板守卫、`CD4` 的 `N/A` 出口与 `CD6` 规范化：

| 控制项 | 打的是 | 期望 |
| :--- | :--- | :--- |
| `CTRL-SELF` | 内检 `--scope self` | 三条自检全 `PASS`、`exit=0` |
| `CTRL-NA-MISSING` | **情形 A**：代码目录不存在 | `CD1`–`CD6` 全 `N/A`、`exit=0` |
| `CTRL-NA-NOSECTION` | **情形 B**：清单在但 `## 结果清单` 不在 | `CD3`/`CD6` = `N/A`，`CD1`/`CD2`/`CD5` = `PASS` |
| `CTRL-EMPTY-ROWS` | **情形 C**：节在但零数据行 | `CD3`/`CD6` 判 `FAIL`（空集不许判绿） |
| `CTRL-HEADER-BAD` | **第四态**：节在但表头不符 | `CD3`/`CD6` 判 `FAIL`（fail-closed） |
| `CTRL-DIR-EMPTY` | **情形 C**：目录在但零代码文件 | `CD1`/`CD2`/`CD5` 判 `FAIL` |
| `CTRL-CD4-NOAPPENDIX` | `CD4` 的 `N/A` 出口（不给 `--appendix`） | `CD4` = `N/A`、其余 `PASS`、`exit=0` |
| `CTRL-TEMPLATE` | **模板守卫**：靶子 = `assets/` 目录 | 出一条 `FAIL TEMPLATE`、`exit≠0` |
| `CTRL-CD6-NORM-PREFIX` | `CD6` 的 `代码来自` **规范化**（`ai生成` 认作 AI 行） | `CD6` = `PASS`（不规范化会假红） |
| `CTRL-CD6-THIRD-VALUE` | `CD6` 的 `代码来自` **取值域**（第三种取值） | `CD6` = `FAIL`（fail-closed） |

★ 内检三条（`SELF1`/`SELF2`/`SELF3`）也要**从失败方向证明**（`GC12`）—— 驱动器把 skill 目录**拷进
`build/`**、逐条改坏副本、再用 `--skill-dir <副本>` 跑内检，断言对位那条真红（**不动入库件**）：

| 变异 | 打的是 | 期望 |
| :--- | :--- | :--- |
| `CTRL-SELF-COPY` | 未改的 skill 副本 | `SELF1`–`SELF3` 全 `PASS`、`exit=0` |
| `MUT-SELF1` | 删掉副本 `SKILL.md` 的通用边界句 | `SELF1` → `FAIL` |
| `MUT-SELF2` | 把副本某 reference 里的指针改成不存在的文件 | `SELF2` → `FAIL` |
| `MUT-SELF3` | 把副本模板表头删一列 | `SELF3` → `FAIL` |

★ 上列**控制项与内检变异清单不声称穷尽** —— 各只钉一种已列出的失效；覆盖口径与边界见
`tests/skills/code/samples/README.md` 的"驱动器覆盖"节与 `check-code.py` 的"已知边界"节。
★ 临时件只落仓内 `build/m5dc-mut-code/`（gitignored），跑完即清。**判据本体与样例一概不动。**
★ 末行打印**可复跑的红/绿计数**。
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]        # tests/skills/code/x.py → 仓根
CHK = ROOT / ".claude/skills/mcm-code/check-code.py"
SKILL = ROOT / ".claude/skills/mcm-code"
SAMPLES = ROOT / "tests/skills/code/samples"
ASSETS = ROOT / ".claude/skills/mcm-code/assets"
BUILD = ROOT / "build/m5dc-mut-code"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

STATUS_RE = re.compile(r"^(PASS|FAIL|N/A)\s+(CD\d|SELF\d|TEMPLATE)\b")
SIDES = ("comply", "violate")

# 边界句（`check-code.py` 的 `SELF1` 比对串；此处用于造 `MUT-SELF1`）
GEN_BOUNDARY = "本 skill 给出数据来源与代码规范；最终判断与结论由队员负责。"
# 模板五列表头（用于造 `MUT-SELF3`）
HEADER_LINE = "| 结果文件 | 对应正文编号 | 生成脚本 | 代码来自 | 确认 |"

# 控制项夹具（只落 build/）：一份可过 CD1/CD2/CD5 的最小 MATLAB 代码
CTRL_CODE_M = (
    "function out = solve(seed)\n"
    "% 控制项夹具：入口固定随机源 + 结果落盘。\n"
    "if nargin < 1 || isempty(seed); seed = 2025; end\n"
    "rng(seed, 'twister');\n"
    "x = rand(100, 1);\n"
    "out.mean = mean(x);\n"
    "writetable(table(out.mean), fullfile('build', 'table-1-estimate.csv'));\n"
    "end\n"
)
_MF_HEAD = (
    "## 结果清单\n"
    "\n"
    "| 结果文件 | 对应正文编号 | 生成脚本 | 代码来自 | 确认 |\n"
    "| :--- | :--- | :--- | :--- | :--- |\n"
)
NO_SECTION_MANIFEST = "# 一份没有契约节的清单\n\n这里只有标题，`## 结果清单` 不在。\n"
EMPTY_ROWS_MANIFEST = "# 节在但零数据行\n\n" + _MF_HEAD
HEADER_BAD_MANIFEST = (
    "# 表头不符（第四态）\n\n"
    "## 结果清单\n\n"
    "| 结果文件 | 对应正文编号 | 生成脚本 | 代码来自 |\n"
    "| :--- | :--- | :--- | :--- |\n"
    "| build/figure-1-samples.csv | 图 1 | build/solve.py | AI |\n"
)
NORM_PREFIX_MANIFEST = (
    "# 代码来自 取值变体（小写 + 前缀）\n\n" + _MF_HEAD +
    "| build/figure-1-samples.csv | 图 1 | build/solve.py | ai生成 | 已核（李四,2027-02-16） |\n"
)
THIRD_VALUE_MANIFEST = (
    "# 代码来自 第三种取值（fail-closed）\n\n" + _MF_HEAD +
    "| build/figure-1-samples.csv | 图 1 | build/solve.py | 助手 | 待核 |\n"
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
    """跑一对；返回 `{side: (ok, rc, verdict, want, out, args)}`。"""
    res = {}
    for side in SIDES:
        d = SAMPLES / cid / side
        args = ["--scope", "artifact", str(d / "code"), "--appendix", str(d / "appendix.md")]
        rc, out, v = run_checker(args)
        if side == "comply":
            ok = (rc == 0) and all(v.get(i) == "PASS" for i in criteria)
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

def _make_dir(name, manifest_text, code_text=CTRL_CODE_M):
    """在 `build/` 下造一个控制项代码目录：一个 `.m` 代码文件 + 指定清单。"""
    d = BUILD / name
    write(d / "solve.m", code_text)
    if manifest_text is not None:
        write(d / "result-manifest.md", manifest_text)
    return d


def run_controls(base_verdict):
    """返回 `[(cid, desc, ok, detail), ...]`。"""
    out = []

    # CTRL-SELF
    rc, text, v = run_checker(["--scope", "self"])
    ok = (rc == 0) and all(v.get("SELF%d" % i) == "PASS" for i in (1, 2, 3))
    out.append(("CTRL-SELF", "内检 --scope self ⇒ 三条自检全 PASS、exit=0", ok,
                _raw("check-code.py --scope self", rc, text)))

    # CTRL-NA-MISSING（情形 A：整个代码目录不存在）
    missing = BUILD / "does-not-exist-dir"
    rc, text, v = run_checker(["--scope", "artifact", str(missing)])
    ok = (rc == 0) and all(v.get(i) == "N/A" for i in base_verdict)
    out.append(("CTRL-NA-MISSING", "情形 A：代码目录不存在 ⇒ CD1–CD6 全 N/A、exit=0", ok,
                _raw("check-code.py --scope artifact %s" % missing.name, rc, text)))

    # CTRL-NA-NOSECTION（情形 B：清单在但节不在）
    d = _make_dir("nosection", NO_SECTION_MANIFEST)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (rc == 0) and (v.get("CD3") == "N/A") and (v.get("CD6") == "N/A") \
        and all(v.get(i) == "PASS" for i in ("CD1", "CD2", "CD5"))
    out.append(("CTRL-NA-NOSECTION", "情形 B：清单在但 `## 结果清单` 不在 ⇒ CD3/CD6=N/A、CD1/CD2/CD5=PASS", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

    # CTRL-EMPTY-ROWS（情形 C：节在但零数据行）
    d = _make_dir("emptyrows", EMPTY_ROWS_MANIFEST)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (rc != 0) and (v.get("CD3") == "FAIL") and (v.get("CD6") == "FAIL")
    out.append(("CTRL-EMPTY-ROWS", "情形 C：节在但零数据行 ⇒ CD3/CD6 判 FAIL（空集不许判绿）", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

    # CTRL-HEADER-BAD（第四态：节在但表头不符）
    d = _make_dir("headerbad", HEADER_BAD_MANIFEST)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (rc != 0) and (v.get("CD3") == "FAIL") and (v.get("CD6") == "FAIL")
    out.append(("CTRL-HEADER-BAD", "第四态：节在但表头不符 ⇒ CD3/CD6 判 FAIL（fail-closed）", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

    # CTRL-DIR-EMPTY（情形 C：目录在但零代码文件）
    d = BUILD / "emptydir"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True, exist_ok=True)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (rc != 0) and (v.get("CD1") == "FAIL") and (v.get("CD2") == "FAIL") and (v.get("CD5") == "FAIL")
    out.append(("CTRL-DIR-EMPTY", "情形 C：目录在但零代码文件 ⇒ CD1/CD2/CD5 判 FAIL", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

    # CTRL-CD4-NOAPPENDIX（CD4 的 N/A 出口）
    okdir = SAMPLES / "CD6/comply/code"
    rc, text, v = run_checker(["--scope", "artifact", str(okdir)])
    ok = (rc == 0) and (v.get("CD4") == "N/A") \
        and all(v.get(i) == "PASS" for i in base_verdict if i != "CD4")
    out.append(("CTRL-CD4-NOAPPENDIX", "不给 --appendix ⇒ CD4 = N/A、其余 PASS、exit=0", ok,
                _raw("check-code.py --scope artifact %s" % okdir.relative_to(ROOT).as_posix(), rc, text)))

    # CTRL-TEMPLATE（模板守卫）
    rc, text, v = run_checker(["--scope", "artifact", str(ASSETS)])
    ok = (rc != 0) and (v.get("TEMPLATE") == "FAIL")
    out.append(("CTRL-TEMPLATE", "模板守卫：靶子 = assets/ 目录 ⇒ FAIL TEMPLATE、exit≠0", ok,
                _raw("check-code.py --scope artifact %s" % ASSETS.relative_to(ROOT).as_posix(), rc, text)))

    # CTRL-CD6-NORM-PREFIX（代码来自 规范化）
    d = _make_dir("norm-prefix", NORM_PREFIX_MANIFEST)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (v.get("CD6") == "PASS")
    out.append(("CTRL-CD6-NORM-PREFIX", "`代码来自 = ai生成` 认作 AI 行且已确认 ⇒ CD6 = PASS（证明规范化）", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

    # CTRL-CD6-THIRD-VALUE（代码来自 取值域 fail-closed）
    d = _make_dir("third-value", THIRD_VALUE_MANIFEST)
    rc, text, v = run_checker(["--scope", "artifact", str(d)])
    ok = (rc != 0) and (v.get("CD6") == "FAIL")
    out.append(("CTRL-CD6-THIRD-VALUE", "`代码来自 = 助手`（第三种取值）⇒ CD6 = FAIL（fail-closed）", ok,
                _raw("check-code.py --scope artifact %s" % d.name, rc, text)))

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
                _raw("check-code.py --scope self --skill-dir <副本>", rc, text)))

    # MUT-SELF1：删通用边界句
    d = _fresh_skill_copy()
    _mutate(d / "SKILL.md", GEN_BOUNDARY, "")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF1") == "FAIL")
    out.append(("MUT-SELF1", "删掉副本 SKILL.md 的通用边界句 ⇒ SELF1 = FAIL", ok,
                _raw("check-code.py --scope self --skill-dir <副本·去掉边界句>", rc, text)))

    # MUT-SELF2：把某 reference 的指针改成不存在的文件
    d = _fresh_skill_copy()
    _mutate(d / "references/reproducibility.md", "references/numbering.md", "references/does-not-exist.md")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF2") == "FAIL")
    out.append(("MUT-SELF2", "把副本某 reference 的指针改成不存在的文件 ⇒ SELF2 = FAIL", ok,
                _raw("check-code.py --scope self --skill-dir <副本·断指针>", rc, text)))

    # MUT-SELF3：把模板表头删一列
    d = _fresh_skill_copy()
    _mutate(d / "assets/result-manifest.md", HEADER_LINE,
            "| 结果文件 | 对应正文编号 | 生成脚本 | 代码来自 |")
    rc, text, v = run_checker(["--scope", "self", "--skill-dir", str(d)])
    ok = (rc != 0) and (v.get("SELF3") == "FAIL")
    out.append(("MUT-SELF3", "把副本模板表头删一列 ⇒ SELF3 = FAIL", ok,
                _raw("check-code.py --scope self --skill-dir <副本·缺一列>", rc, text)))

    return out


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("变异驱动器 · check-code.py（mcm-code）：判据 CD1–CD6 逐对打红 / 打绿 + 控制项")
    print("=" * 78)
    print("检查器 = %s" % CHK.relative_to(ROOT).as_posix())

    if not CHK.exists():
        print("RUN: 找不到检查器 %s ⇒ fail-closed" % CHK)
        return 1

    # ★ 驱动器自证（强口径）：自己建的容器 `build/m5dc-mut-code` —— 开工前不该在场、
    #    跑期间必须真的建过、跑完（清完）必须仍不在场；另看 `git status` 有无差值。
    status_before = git_status()
    container_pre = BUILD.exists()          # 开工前：本驱动器建的容器不该在场

    # ---- 现取判据清单（干净合规侧）+ 现取 samples 一级目录 ----
    rc0, out0, base = run_checker(
        ["--scope", "artifact",
         str(SAMPLES / "CD1/comply/code"),
         "--appendix", str(SAMPLES / "CD1/comply/appendix.md")])
    criteria = sorted(k for k in base if k.startswith("CD"))
    sample_ids = _sample_ids()
    print("\n现取判据清单（合规侧 CD1/comply 上读到）= %s" % criteria)
    print("样本一级目录（samples/ 下）= %s" % sample_ids)

    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ fail-closed（检查器没出 CD* 行？）")
        return 1

    # ---- 断言 ③（含自证探针）----
    ass3 = _ass3_ok(criteria, sample_ids)
    probe_ok = (_ass3_ok(criteria, sample_ids + ["CD9"]) is False) and \
               (_ass3_ok(criteria + ["CD9"], sample_ids) is False)
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
            cmd = "check-code.py " + " ".join(args)
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
    print("控制项（N/A 三分 + 第四态 · 模板守卫 · CD4 的 N/A 出口 · CD6 规范化 · 内检）")
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
    print("驱动器自证：容器 build/m5dc-mut-code 跑前=%s · 跑期间=%s · 清完=%s · git status(非 ignored 面)差值=%s ⇒ %s"
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
