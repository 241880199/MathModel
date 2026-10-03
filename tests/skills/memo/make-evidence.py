#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 4（`mcm-memo`）：生成 `tests/skills/memo/MEMO-evidence.md`。

用法：  python tests/skills/memo/make-evidence.py

## 它做什么

用**同一把尺** = `.claude/skills/mcm-memo/check-memo.py`（判据 `MO1–MO4`），
对**若干份备忘录 × 题面组合**逐件跑同一条命令形态，把机器读数摆成一张可读的表，
并登记**两条官方规则**的出处与**本工具的边界**。

- 夹具写在 `build/memo-ev/`（仓内 gitignored；**不落 C 盘 / `%TEMP%` / 盘根**），
  由本生成器**当场写出**，故证据是（夹具字节 + 检查器字节 + 本文件源码）的**纯函数**。
- ★ **本生成器不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`），锚点一律用
  固定基线 `BASE_REF` ⇒ 在**已提交的树**上重跑本生成器 ⇒ 本文件**逐字节不变**（通则 14）。

## 可重放（通则 14）

**先干净 → 再捕获 → 再提交 → 再跑一次证不动点**：本生成器只读检查器与自造夹具、
不碰工作树 ⇒ 提交后在干净树上重跑，`git diff` 对本文件为空即证。
"""

import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/memo
REPO = HERE.parents[2]                                   # 仓根
CHK = REPO / ".claude/skills/mcm-memo/check-memo.py"
BUILD = REPO / "build/memo-ev"
OUT_DOC = HERE / "MEMO-evidence.md"

# ★ 本任务的**基线 commit**（Task 4 的基线；不随提交变动 —— 用固定基线，不用 `HEAD`）。
BASE_REF = "eb43b39"

NL = chr(10)
STATUS_RE = re.compile(r"^(PASS|FAIL|SKIP)\s+(MO\d)\b")
RESULT_RE = re.compile(r"^RESULT:\s*(PASS|FAIL)")
IDS = ["MO1", "MO2", "MO3", "MO4"]

# --------------------------------------------------------------------------
# 夹具（与变异驱动器同构；由本生成器当场写出）
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
WMA_TEX = GOOD_TEX.replace("To:} the group of Governors", "To:} the World Medical Association")
LONG_TEX = GOOD_TEX.replace("Sincerely, Team \\#2000000",
                            (BODY_PARAS[0] + "\n\n") * 24 + "Sincerely, Team \\#2000000")
NAME_TEX = GOOD_TEX.replace("Sincerely, Team \\#2000000", "Sincerely, John Smith")
INST_TEX = GOOD_TEX.replace("Sincerely, Team \\#2000000", "Sincerely, Nanjing University")
AUDMISS_TEX = GOOD_TEX.replace("To:} the group of Governors", "To:} the relevant authority")

PROBLEM_MEMO = (
    "Prepare a one-page memo to the group of Governors summarizing the recommended\n"
    "inspection interval for the campus stair, based on your model of its wear.\n")
PROBLEM_NOMEMO = (
    "Model the wear of the campus stair and report your estimate of its age and of the\n"
    "number of daily users. State the assumptions your model rests on.\n")
PROBLEM_WMA = (
    "Prepare a 1-2 page non-technical letter for the World Medical Association to use.\n")

# (tag, 备忘录, 题面, 说明)
SCENARIOS = [
    ("SKL-good",       GOOD_TEX,   PROBLEM_MEMO,   "干净的一页备忘录 + **要求 memo** 的题面（应全 `PASS`）"),
    ("SKL-nomemo",     GOOD_TEX,   PROBLEM_NOMEMO, "题面**不要求** memo ⇒ 产物不该存在（`MO1` → `FAIL`）"),
    ("SKL-noproblem",  GOOD_TEX,   None,           "**不给 `--problem`** ⇒ `MO1`/`MO4` = `SKIP`（不是 `PASS`）"),
    ("SKL-name",       NAME_TEX,   PROBLEM_MEMO,   "★ 落款**署真名** ⇒ 违反官方②（`MO2` → `FAIL`）"),
    ("SKL-inst",       INST_TEX,   PROBLEM_MEMO,   "落款**署校名** ⇒ 违反官方②（`MO2` → `FAIL`）"),
    ("SKL-twopage",    LONG_TEX,   PROBLEM_MEMO,   "灌水成**两页** ⇒ 不是一页（`MO3` → `FAIL`）"),
    ("SKL-audmiss",    AUDMISS_TEX, PROBLEM_MEMO,  "`To:` 行不再点名题面受众（`MO4` → `FAIL`）"),
    ("SKL-wma",        WMA_TEX,    PROBLEM_WMA,    "另一受众（`World Medical Association`）+ 对应题面（`MO4` = `PASS`）"),
]


def rel(p):
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return str(p)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def git_blob(path):
    r = subprocess.run(["git", "hash-object", str(path)], cwd=str(REPO),
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def run_check(memo, problem):
    args = [sys.executable, str(CHK), str(memo)]
    if problem is not None:
        args += ["--problem", str(problem)]
    p = subprocess.run(args, cwd=str(REPO), capture_output=True, text=True, encoding="utf-8")
    return p.stdout, p.returncode


def parse(out):
    st, result = {}, None
    for line in out.splitlines():
        m = STATUS_RE.match(line)
        if m:
            st[m.group(2)] = m.group(1)
            continue
        m = RESULT_RE.match(line)
        if m:
            result = m.group(1)
    return st, result


def main():
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True, exist_ok=True)

    fixtures = {
        "good.tex": GOOD_TEX, "wma.tex": WMA_TEX, "long.tex": LONG_TEX,
        "name.tex": NAME_TEX, "inst.tex": INST_TEX, "audmiss.tex": AUDMISS_TEX,
        "problem-memo.txt": PROBLEM_MEMO, "problem-nomemo.txt": PROBLEM_NOMEMO,
        "problem-wma.txt": PROBLEM_WMA,
    }
    for name, text in fixtures.items():
        write(BUILD / name, text)

    rows = []
    for tag, memo_text, problem_text, note in SCENARIOS:
        memo = BUILD / {GOOD_TEX: "good.tex", WMA_TEX: "wma.tex", LONG_TEX: "long.tex",
                        NAME_TEX: "name.tex", INST_TEX: "inst.tex",
                        AUDMISS_TEX: "audmiss.tex"}[memo_text]
        prob = None
        if problem_text is not None:
            prob = BUILD / {PROBLEM_MEMO: "problem-memo.txt",
                            PROBLEM_NOMEMO: "problem-nomemo.txt",
                            PROBLEM_WMA: "problem-wma.txt"}[problem_text]
        out, code = run_check(memo, prob)
        st, result = parse(out)
        rows.append(dict(tag=tag, memo=memo, prob=prob, note=note, st=st, result=result,
                         code=code, blob=git_blob(memo),
                         nbytes=len(memo.read_bytes()), nlines=memo.read_bytes().count(b"\n")))

    chk_blob = git_blob(CHK)
    doc = []
    a = doc.append

    a('# `MEMO-evidence.md` —— `mcm-memo` 的证据（同一把尺：`check-memo.py` 的 `MO1–MO4`）')
    a('')
    a('**本文件由 `tests/skills/memo/make-evidence.py` 当场跑命令生成**（`write_bytes`、全 LF）。')
    a('**不许手改** —— 改读数请改生成器或夹具，然后重跑。')
    a('')
    a('> 生成命令：`python tests/skills/memo/make-evidence.py`')
    a('> 复现：在**已提交的树**上重跑本生成器 ⇒ 本文件**逐字节不变**（证法见 §6）。')
    a('')
    a('**同一把尺** = `.claude/skills/mcm-memo/check-memo.py`，对**每份备忘录 × 题面组合**')
    a('跑同一条命令形态：`python check-memo.py <memo.tex> [--problem <题面>]`。')
    a('★ **判据清单现取**（从检查器 stdout 的 `PASS|FAIL|SKIP` 行里读 id），**不写死条数**。')
    a('')

    # ---- §1 两条官方规则 ----
    a('## §1 两条官方规则（本 skill 的判据源头；★ 仅见于 `corpus/official/MCM-ICM_Tips.txt`）')
    a('')
    a('| # | 规则 | 出处 | 原文（节录） |')
    a('| :-- | :-- | :-- | :-- |')
    a('| ① | **触发**（每题有**各自**要求，如 required memos or letters） | `MCM-ICM_Tips.txt:160-162` | '
      '*"Each problem will have different and specific requirements, such as **required memos or letters**, '
      'specific solution format, and/or page limits."* |')
    a('| ② | ★★ **匿名落款**（一票否决类） | `MCM-ICM_Tips.txt:239-241` | '
      '*"Do not include any type of team identification such as student names, institution name or '
      'geographical region. If you are required to include a letter with your submission, be sure not to '
      'sign the letter with your name. If you feel as though you need to have a formal closing to such a '
      'letter we suggest using: **Sincerely, Team #2000000**."* |')
    a('')
    a('★ **② 最要紧**：漏了它，skill 会把队伍引向**在 letter 上署真名**。两条均标 `[官方]†`（**仅见于 Tips**）。')
    a('★ **题面没要求就绝不产出**（★ `[社区]` **操作纪律**；由官方① 推出的**更严推论** —— 官方① *只*说'
      '"每题有各自要求（如 required memos or letters）"，**未**禁止主动写 memo）—— memo/letter 是'
      '**题目特定要求**，不是通用交付物（`MO1` 判它）。')
    a('')

    # ---- §2 判据 ----
    a('## §2 判据 `MO1–MO4`（★ 四条都是硬失败 `FAIL`）')
    a('')
    a('| id | 判据 | 出处 | 燃料 / 缺燃料时 |')
    a('| :-- | :-- | :-- | :-- |')
    a('| `MO1` | 触发条件在场（题面**未**要求 memo/letter ⇒ 不得产出该文件） | `[社区]` 操作纪律（由 `[官方]†` ① `Tips:160-162` 推出） | '
      '`--problem`；**缺 ⇒ `SKIP`（不报 `PASS`）** |')
    a('| `MO2` | 匿名落款（须为 `Sincerely, Team #<队号>` 一类；真名/校名/机构名 ⇒ 红） | `[官方]†` ② `Tips:239-241` | '
      '备忘录本体；机构词表与"残余标识"判法是 `[社区]` |')
    a('| `MO3` | 恰好一页（`pdfLaTeX` 编两遍 + `fitz` 读页数） | `[社区]` 口径（官方只说题面可能有页数要求） | '
      'PATH 里 `pdflatex`；**缺 ⇒ `SKIP`** |')
    a('| `MO4` | 受众在文首点名（题面点名的受众出现在前 15 非空行） | `[社区]` 口径 | '
      '`--problem` 提受众；**缺/提不出 ⇒ `SKIP`** |')
    a('')
    a('★ **"检查器 PASS" ≠ "这份备忘录写好了"** —— 措辞 / 受众适配 / 内容覆盖**仍靠人工**；')
    a('  `自查 A14`（题目特定要求）是 `mcm-selfreview` 的**检查侧**，本 skill **只给指针、不复述**。')
    a('')

    # ---- §3 夹具身份 ----
    a('## §3 夹具身份（逐件当场 `git hash-object`）')
    a('')
    a('| 场景 | 备忘录 | 形态 | 字节 | 行数 | git blob |')
    a('| :-- | :-- | :-- | ---: | ---: | :-- |')
    for r in rows:
        a("| `%s` | `%s` | `.tex` | %d | %d | `%s` |"
          % (r["tag"], r["memo"].name, r["nbytes"], r["nlines"], r["blob"]))
    a('')
    a('★ 夹具由本生成器**当场写出**（`build/memo-ev/`，仓内 gitignored）⇒ 上面每个 blob 是**纯函数**读数。')
    a('')

    # ---- §4 对照表 ----
    a('## §4 ★ 读数表（机器读数；同一把尺、逐件跑）')
    a('')
    a('命令形态：`python .claude/skills/mcm-memo/check-memo.py <memo.tex> [--problem <题面>]`')
    a('')
    a('| 场景 | 题面 | 说明 | ' + ' | '.join('`%s`' % i for i in IDS) + ' | `RESULT` | exit |')
    a('| :-- | :-- | :-- | ' + ' | '.join(':--' for _ in IDS) + ' | :-- | ---: |')
    for r in rows:
        prob = "（无）" if r["prob"] is None else "`%s`" % r["prob"].name
        a("| `%s` | %s | %s | " % (r["tag"], prob, r["note"])
          + " | ".join(r["st"].get(i, "—") for i in IDS)
          + " | **%s** | %d |" % (r["result"], r["code"]))
    a('')
    a('★ **状态语义**：`FAIL` = 硬失败（退出码非 0）；`PASS` = 过；')
    a('  `SKIP` = **无法判定**（缺燃料；**既不是 `PASS` 也不是 `FAIL`**，退出码不受影响）。')
    a('★ `SKL-noproblem` 一行证明：**缺 `--problem` 时 `MO1`/`MO4` 报 `SKIP` 而不报 `PASS`**（fail-closed）。')
    a('')

    # ---- §5 边界 ----
    a('## §5 边界（**如实登记，不放大**）')
    a('')
    a('- **只判形式**：`MO1–MO4` 覆盖不了**措辞 / 受众适配 / 内容覆盖** —— "检查器 PASS" ≠ "写好了"。')
    a('- **`MO2` 的机构词表与"残余标识"判法是 `[社区]` 口径**：官方只列举 *"student names, institution name or '
      'geographical region"*，**未给词表**。⇒ 词表**不声称穷尽**；落款块**之外**的团队标识（如正文或')
    a('  `From:` 行里的真名）**本工具不查** —— 那属于 `自查 A14` / 人工。')
    a('- **`MO4` 的受众靠题面里的固定句式**（`memo/letter ... to/for the <受众>`）提取：**提不出 ⇒ `SKIP`**，')
    a('  **不猜**；作者换一种措辞写题面就可能提不出 ⇒ 该行**不是**"受众写错"，而是"无法判定"。')
    a('- **`MO3` 要能编译**：备忘录须是**可编译的完整 `.tex`**（含 `\\documentclass`）；**非 `.tex` ⇒ fail-closed 红**。')
    a('- **不判"这段是不是 AI 生成的"**；**不做**全稿提交前合规（那是 `mcm-selfreview`）。')
    a('- ★ **本文件不声称穷尽**：以上是**已知**边界，不是"工具的全部局限清单"。')
    a('')

    # ---- §6 自证 ----
    a('## §6 自证（可重放 / 不动点）')
    a('')
    # ★★ 取基线路径的 blob：`git rev-parse <ref>:<path>` 在**该路径不在基线里**时 **rc=128**，
    #    但 **stdout 仍会把参数本身回显出来**（实测：`eb43b39:...check-memo.py` 照打一行）。
    #    ⇒ 拿 stdout 前**必须先判 `returncode`**：rc≠0 ⇒ 走回退串，绝不把"参数回显"当成 blob
    #    （否则 `[:12]` 会切出 `eb43b39:.cla` 这种垃圾值）。这条纪律对**所有**会回显参数的 git 调用成立。
    base_run = subprocess.run(["git", "rev-parse", BASE_REF + ":" + rel(CHK)],
                              cwd=str(REPO), capture_output=True, text=True, encoding="utf-8")
    base_blob = base_run.stdout.strip() if base_run.returncode == 0 else ""
    a("- **检查器 blob**：工作树 `%s` · 基线 `%s` blob `%s`" % (chk_blob[:12], BASE_REF,
                                                                 (base_blob[:12] or "(基线里无此件)")))
    a("- **夹具自证（逐件 blob）**：" + " · ".join("`%s`=`%s`" % (r["tag"], r["blob"][:12]) for r in rows))
    a("- **本生成器不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`，锚点一律用固定基线 `%s`）" % BASE_REF)
    a('  ⇒ 本文件是（夹具字节 + 检查器字节 + 生成器源码）的**纯函数**。')
    a('- ★ **不动点证法（通则 14）**：**先干净 → 再捕获 → 再提交 → 再跑一次证不动点** ——')
    a('  在**已提交**的树上重跑本生成器，然后 `git status --short` 仍为空、`git diff` 对本文件为空 ⇒ **逐字节不变**。')
    a('  （本支执行记录见 `.superpowers/sdd/task-m2-sw-t4-report.md`。）')
    a('- ★ **判据逻辑全仓只许一份**：判据本体在 `.claude/skills/mcm-memo/check-memo.py`；')
    a('  `tests/` 下**无**镜像版（变异驱动器的 `RUN:` 行盯着这件事）。')
    a('')

    OUT_DOC.write_bytes((NL.join(doc) + NL).encode("utf-8"))
    shutil.rmtree(BUILD, ignore_errors=True)
    print("WROTE %s (%d 字节)" % (rel(OUT_DOC), OUT_DOC.stat().st_size))
    for r in rows:
        print("  %-14s RESULT=%-4s exit=%d  %s" % (r["tag"], r["result"], r["code"],
                                                   {i: r["st"].get(i) for i in IDS}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
