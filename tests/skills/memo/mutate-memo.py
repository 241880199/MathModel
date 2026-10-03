#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/memo/mutate-memo.py` —— `check-memo.py` 的**变异驱动器**。

用法：  python tests/skills/memo/mutate-memo.py

## 它做什么

把**已知好的一份一页备忘录 `.tex`**（`build/memo-mut/` 下的夹具）逐条改坏（当场改、当场跑、
当场判、然后收走），断言检查器**点名红在该条判据上**；另设**必须仍绿**的射程边界对照。

**`MO1–MO4` 每项至少一条真红作证**（本仓硬规矩：判据只能从失败方向证明）。
★ **必查的一条**：**把落款改成署真名 ⇒ `MO2` 真红**（它对应**官方硬规则** ②
`corpus/official/MCM-ICM_Tips.txt:239-241`）。

- **判据本体不动**：驱动器**调 skill 目录那一份**（`.claude/skills/mcm-memo/check-memo.py`），
  **不在 `tests/` 下再写一份镜像版**；变异只碰 `build/` 下的副本（仓内 gitignored，
  **不落 C 盘 / `%TEMP%` / 盘根**）。
- 收尾逐件 `git hash-object` 自证"受保护件逐字节未变"，并核 `git status --short` 为空。
- **期望集逐条写死**：每条变异断言"**与基准逐条相比，恰好这些判据的状态变了、且变成什么**"。
  "该红没红"或"顺手带红了别的判据"都会被当场抓出来。
- **判据清单现取**：先把检查器在**干净夹具**上跑一遍、把 `PASS|FAIL|SKIP  <id>` 行读成 id 集合，
  拿它当"全部判据"。变异若点名了**不在现取集合里**的判据 ⇒ 该条直接判失败（防"打错靶子还报绿"）。
  ★ **这条断言不恒真**：驱动器自带一条**自证** —— 造一个点名**清单外**判据（`MO5`）的假 Case，
  断言它**必被** `_bad_target_ids()` 抓到；抓不到即 `rc≠0`。
- ★ **`SKIP` 不许做成"判死"**：`CTRL-no-problem` 断言 `MO1`/`MO4` = `SKIP` **且退出码 = 0**。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望 |
| :--- | :--- | :--- |
| `MUT-MO1` | 题面**不要求** memo/letter，却产出该文件 | `MO1` → `FAIL` |
| `MUT-MO1-PAPER` | 题面出现 `US Letter or A4`（**纸张尺寸**，不是要求 memo） | `MO1` → `FAIL`（**不误判为"要求"**） |
| `MUT-MO2-NAME` | ★ **落款改成署真名**（`Sincerely, John Smith`） | `MO2` → `FAIL` |
| `MUT-MO2-INST` | 落款改成署**校名**（`Sincerely, Nanjing University`） | `MO2` → `FAIL` |
| `MUT-MO3` | 灌水成**两页** | `MO3` → `FAIL` |
| `MUT-MO4` | 把 `To:` 行的**点名受众**换成别的 | `MO4` → `FAIL` |
| `CTRL-good` | 干净的一页备忘录 + 要求 memo 的题面 | 全 `PASS`、`exit=0` |
| `CTRL-no-sig` | **删掉整个落款**（无正式收尾） | `MO2` **不得** `FAIL`（无落款不违规） |
| `CTRL-other-audience` | 另一份备忘录（`To: the World Medical Association`）+ 对应题面 | `MO4` = `PASS`（不写死某一受众） |
| `CTRL-no-problem` | 不给 `--problem` | `MO1`/`MO4` = `SKIP`（**不是 `PASS`**）、`exit=0` |

## 合计行形态

照 `mutate-section-writer.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**
（末行放"运行完整性"读数）。
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]     # tests/skills/memo/x.py → 仓根
CHK = ROOT / ".claude/skills/mcm-memo/check-memo.py"
SKILL = ROOT / ".claude/skills/mcm-memo"
BUILD = ROOT / "build/memo-mut"                        # ★ 临时件只落仓内 `build/`
GUARDED = (CHK, SKILL / "SKILL.md", SKILL / "references/format.md")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
STATUS_RE = re.compile(r"^(PASS|FAIL|SKIP)\s+(MO\d)\s")
IDS = ["MO1", "MO2", "MO3", "MO4"]

# --------------------------------------------------------------------------
# 夹具（**不落入库件**，只写 build/）
# --------------------------------------------------------------------------

BODY_PARAS = (
    "The model estimates the wear depth at every control point of the stair and turns it "
    "into a single number for the whole tread. That number is compared with the depth the "
    "survey team measured, and the two agree to within the resolution of the instrument.",
    "The fitted age and the number of daily users trade off against each other, so this memo "
    "reports a range rather than a single pair. Over that range the predicted wear depth stays "
    "within ten per cent of the measured value.",
    "On that basis we recommend an inspection interval of two years for the walking line and "
    "five years for the edge beside the handrail.",
)

GOOD_TEX = (
    "\\documentclass[11pt]{article}\n"
    "\\usepackage[margin=1in]{geometry}\n"
    "\\begin{document}\n\n"
    "\\begin{center}\\textbf{MEMORANDUM}\\end{center}\n\n"
    "\\noindent\\textbf{To:} the group of Governors\\\\\n"
    "\\textbf{From:} Team \\#2000000\\\\\n"
    "\\textbf{Date:} 1 February 2027\\\\\n"
    "\\textbf{Subject:} A recommended inspection interval for the campus stair\n\n"
    "\\medskip\n"
    + BODY_PARAS[0] + "\n\n" + BODY_PARAS[1] + "\n\n" + BODY_PARAS[2] + "\n\n"
    "Sincerely, Team \\#2000000\n\n"
    "\\end{document}\n"
)

# 另一受众（证明 MO4 不写死某一受众）：正文同构，只换 `To:` 行。
GOOD_WMA_TEX = GOOD_TEX.replace("To:} the group of Governors", "To:} the World Medical Association")

# 两页件（灌水；`MO3` 该红）
LONG_TEX = GOOD_TEX.replace(
    "Sincerely, Team \\#2000000",
    (BODY_PARAS[0] + "\n\n") * 24 + "Sincerely, Team \\#2000000")

PROBLEM_MEMO = (
    "Prepare a one-page memo to the group of Governors summarizing the recommended\n"
    "inspection interval for the campus stair, based on your model of its wear.\n")

PROBLEM_NOMEMO = (
    "Model the wear of the campus stair and report your estimate of its age and of the\n"
    "number of daily users. State the assumptions your model rests on.\n")

# ★ 纸张尺寸提及（`US Letter or A4`）—— 不是要求 memo ⇒ `MO1` 应 `FAIL`（不许误判为"要求"）
PROBLEM_PAPER = (
    "Format your solution on US Letter or A4 page size. Report the model results and the\n"
    "assumptions behind them.\n")

PROBLEM_WMA = (
    "Prepare a 1-2 page non-technical letter for the World Medical Association to use.\n")


def _sign_real_name(src):
    return src.replace("Sincerely, Team \\#2000000", "Sincerely, John Smith")


def _sign_institution(src):
    return src.replace("Sincerely, Team \\#2000000", "Sincerely, Nanjing University")


def _drop_signature(src):
    return src.replace("\n\nSincerely, Team \\#2000000\n", "\n")


def _retarget_audience(src):
    return src.replace("To:} the group of Governors", "To:} the relevant authority")


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------

def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))          # 一律 write_bytes（全 LF）


def run_checker(memo_path, problem_path=None):
    args = [sys.executable, str(CHK), str(memo_path)]
    if problem_path is not None:
        args += ["--problem", str(problem_path)]
    pr = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = STATUS_RE.match(line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def _raw(cmdline, rc, out):
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return "$ %s   → exit=%d\n%s" % (cmdline, rc, body)


class Case(object):
    def __init__(self, cid, desc, memo_target, problem_target=None, transform=None,
                 expect=None, expect_rc="zero", kind="red"):
        self.cid, self.desc = cid, desc
        self.memo_target, self.problem_target = memo_target, problem_target
        self.transform = transform
        self.expect = expect or {}
        self.expect_rc = expect_rc
        self.kind = kind


def _bad_target_ids(case_list, criteria):
    """点名了**现取判据清单之外**的判据的变异 id。"""
    return [c.cid for c in case_list if not (set(c.expect) <= set(criteria))]


def cases():
    R = []
    # ---- MO1：触发条件在场 ----
    R.append(Case("MUT-MO1", "题面**不要求** memo/letter，却产出该文件 ⇒ 产物不该存在",
                  "good.tex", "nomemo", None, {"MO1": "FAIL", "MO4": "SKIP"}, "nonzero"))
    R.append(Case("MUT-MO1-PAPER",
                  "题面出现 `US Letter or A4`（**纸张尺寸**）⇒ **不误判为**要求 memo ⇒ `MO1` 仍 `FAIL`",
                  "good.tex", "paper", None, {"MO1": "FAIL", "MO4": "SKIP"}, "nonzero"))
    # ---- MO2：匿名落款（★ 必查：署真名）----
    R.append(Case("MUT-MO2-NAME", "★ 落款改成**署真名**（`Sincerely, John Smith`）—— 官方硬规则 ②",
                  "good.tex", "memo", _sign_real_name, {"MO2": "FAIL"}, "nonzero"))
    R.append(Case("MUT-MO2-INST", "落款改成**署校名**（`Sincerely, Nanjing University`）",
                  "good.tex", "memo", _sign_institution, {"MO2": "FAIL"}, "nonzero"))
    # ---- MO3：恰好一页 ----
    R.append(Case("MUT-MO3", "灌水成**两页** ⇒ 不是一页", "long.tex", "memo", None,
                  {"MO3": "FAIL"}, "nonzero"))
    # ---- MO4：受众在文首点名 ----
    R.append(Case("MUT-MO4", "把 `To:` 行的**点名受众**换成别的 ⇒ 文首不再点名该受众",
                  "good.tex", "memo", _retarget_audience, {"MO4": "FAIL"}, "nonzero"))
    return R


def controls():
    C = []
    C.append(Case("CTRL-good", "射程边界：干净的一页备忘录 + 要求 memo 的题面",
                  "good.tex", "memo", None, {}, "zero", kind="green"))
    C.append(Case("CTRL-no-sig", "射程边界：**删掉整个落款**（无正式收尾）⇒ `MO2` 不得 FAIL",
                  "good.tex", "memo", _drop_signature, {}, "zero", kind="green"))
    C.append(Case("CTRL-other-audience",
                  "★ 另一份备忘录（`To: the World Medical Association`）+ 对应题面 ⇒ `MO4` = PASS"
                  "（不写死某一受众）",
                  "wma.tex", "wma", None, {}, "zero", kind="green"))
    C.append(Case("CTRL-no-problem", "不给 `--problem` ⇒ `MO1`/`MO4` = `SKIP`（不是 `PASS`）、exit=0",
                  "good.tex", None, None, {"MO1": "SKIP", "MO4": "SKIP"}, "zero", kind="green"))
    return C


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("变异驱动器 · check-memo.py（mcm-memo）：判据 MO1–MO4 逐条打红 + %d 条对照"
          % len(controls()))
    print("=" * 78)
    print("检查器 = %s  blob %s" % (CHK.relative_to(ROOT).as_posix(), git_hash_object(CHK)))
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    # ---- 夹具 ----
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    write(BUILD / "good.tex", GOOD_TEX)
    write(BUILD / "wma.tex", GOOD_WMA_TEX)
    write(BUILD / "long.tex", LONG_TEX)
    write(BUILD / "problem-memo.txt", PROBLEM_MEMO)
    write(BUILD / "problem-nomemo.txt", PROBLEM_NOMEMO)
    write(BUILD / "problem-paper.txt", PROBLEM_PAPER)
    write(BUILD / "problem-wma.txt", PROBLEM_WMA)

    targets = {"good.tex": BUILD / "good.tex", "wma.tex": BUILD / "wma.tex",
               "long.tex": BUILD / "long.tex"}
    problems = {"memo": BUILD / "problem-memo.txt",
                "nomemo": BUILD / "problem-nomemo.txt",
                "paper": BUILD / "problem-paper.txt",
                "wma": BUILD / "problem-wma.txt"}

    # ---- 前置：干净夹具必须全绿；并现取判据清单 ----
    rc0, out0, base = run_checker(targets["good.tex"], problems["memo"])
    criteria = [i for i in IDS if i in base]
    base_ok = (rc0 == 0 and criteria == IDS and all(base.get(i) == "PASS" for i in IDS))
    print("\n前置（干净夹具 good.tex + 要求 memo 的题面 + 现取判据清单）: exit=%d · 现取 = %s"
          % (rc0, criteria))
    print("  good.tex = %s" % sorted(base.items()))
    print("  %s" % ("全 PASS" if base_ok else "未全绿 <<< 夹具或判据有问题"))
    if criteria != IDS:
        print("RUN: 现取不到全部四条判据 ⇒ 无法变异（fail-closed）")
        return 1

    rows, failed = [], []
    bad_target = _bad_target_ids(cases() + controls(), criteria)
    _probe = Case("__PROBE_OUT_OF_LIST__", "(自证) 点名清单外的判据 MO5",
                  "good.tex", "memo", None, {"MO5": "FAIL"}, "zero")
    bad_target_probe = _bad_target_ids([_probe], criteria)
    bad_target_probe_ok = (bad_target_probe == ["__PROBE_OUT_OF_LIST__"])

    for c in cases():
        rows.append(run_case(c, targets, problems, base, criteria))
    for c in controls():
        rows.append(run_case(c, targets, problems, base, criteria))

    for st, cid, desc, detail in rows:
        if st.endswith("BAD"):
            failed.append(cid)

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    for st, cid, desc, detail in rows:
        print("%-11s %-16s %s" % (st, cid, desc))
        print(detail)

    # ---- 还原自证 ----
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    stx = subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                         capture_output=True, text=True).stdout
    dirty = sorted(l for l in stx.splitlines() if l.strip())
    rerun_rc, _, rerun_v = run_checker(targets["good.tex"], problems["memo"])

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print("  %-62s blob %s  %s" % (p.relative_to(ROOT).as_posix(), now,
                                       "== 变异前" if now == guarded_before[p] else "!= 变异前 <<<"))
    print("  受保护件逐个 blob 还原: %s" % byte_ok)
    print("  变异后复跑（干净夹具）：exit=%d · %s"
          % (rerun_rc, "全 PASS" if all(rerun_v.get(i) == "PASS" for i in IDS)
             else sorted(rerun_v.items())))
    print("  全仓 `git status --short`:\n%s" % (stx if stx.strip() else "      （空）"))

    n_red = len(cases())
    n_ctl = len(controls())
    fail_red = [c.cid for c in cases() if c.cid in failed]
    fail_ctl = [c.cid for c in controls() if c.cid in failed]
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print("MUT: %d/%d 达预期（判据打红：MO1 触发 / MO2 匿名落款 / MO3 一页 / MO4 受众）%s"
          % (n_red - len(fail_red), n_red,
             "" if not fail_red else "（未达预期：%s）" % ", ".join(fail_red)))
    print("MUT: 对照 %d/%d 达预期（必须绿：干净件全 PASS / 无落款不违规 / 另一受众 MO4 PASS / "
          "缺 --problem 报不可判）%s"
          % (n_ctl - len(fail_ctl), n_ctl,
             "" if not fail_ctl else "（未达预期：%s）" % ", ".join(fail_ctl)))
    total = n_red + n_ctl
    print("MUT: %d/%d 达预期（合计）" % (total - len(failed), total))
    dups = sorted(p.relative_to(ROOT).as_posix()
                  for p in (ROOT / "tests").rglob("check-memo.py"))
    print("RUN: 受保护件 blob 逐件还原=%s · 干净夹具复跑 exit=%d · 判据清单现取 %d 条 %s · "
          "变异点名了清单外的判据 %s · bad_target 自证（点名清单外判据必被抓）%s · "
          "`tests/` 下的 check-memo.py 镜像 %s · "
          "全仓 `git status --short` %s"
          % (byte_ok, rerun_rc, len(criteria), criteria, bad_target or "无",
             "OK" if bad_target_probe_ok else "失败 <<<（断言已被架空）",
             dups or "无（唯一一份在 skill 目录）",
             "空" if not dirty else "非空 <<< " + "; ".join(dirty)))
    rc_all = 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty
                   and not bad_target and not dups and bad_target_probe_ok) else 1
    shutil.rmtree(BUILD, ignore_errors=True)      # ★ 自己造的临时件当场清（build/ 下）
    return rc_all


def run_case(c, targets, problems, base, criteria):
    cid = c.cid
    try:
        tgt = targets[c.memo_target]
        memo = tgt
        if c.transform is not None:
            new = c.transform(tgt.read_bytes().decode("utf-8"))
            if new == tgt.read_bytes().decode("utf-8"):
                return ("RED-BAD" if c.kind == "red" else "GREEN-BAD", cid, c.desc,
                        "驱动器自己报错：变换没有改变文本")
            memo = BUILD / cid / tgt.name
            write(memo, new)
        inp = None if c.problem_target is None else problems.get(c.problem_target)
        rc, out, verdict = run_checker(memo, inp)
        actual = {i: verdict.get(i) for i in criteria}
        want = dict(base)
        want.update(c.expect)
        ok = all(actual.get(i) == want.get(i) for i in criteria)
        if c.expect_rc == "zero":
            ok = ok and rc == 0
        else:
            ok = ok and rc != 0
        note = "" if ok else "   <<< 期望 %s · 实得 %s（exit=%d）" % (want, actual, rc)
        st = ("RED-OK" if c.kind == "red" else "GREEN-OK") if ok else \
             ("RED-BAD" if c.kind == "red" else "GREEN-BAD")
        detail = ("变换：%s\n      期望 = %s · 实得 = %s · exit=%d %s\n"
                  % (c.desc, want, actual, rc, note)
                  + _raw("check-memo.py %s%s" % (tgt.name,
                                                 "" if inp is None else " --problem " + inp.name),
                         rc, out))
        return (st, cid, c.desc, detail)
    except AssertionError as e:
        return ("RED-BAD" if c.kind == "red" else "GREEN-BAD", cid, c.desc,
                "驱动器自己报错：%s" % e)


if __name__ == "__main__":
    sys.exit(main())
