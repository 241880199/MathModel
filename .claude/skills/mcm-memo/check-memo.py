#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-memo.py —— MCM/ICM letter / memo 自检（`mcm-memo` skill 随附）

用途
----
对**一份备忘录 `.tex`**（题面明确要求 letter/memo 时的产物）跑一组检查，逐条报告
`PASS` / `FAIL` / `SKIP`：

  MO1  触发条件在场（硬失败 · 出处 `corpus/official/MCM-ICM_Tips.txt:160-162`）
  MO2  匿名落款（硬失败 · 出处 `corpus/official/MCM-ICM_Tips.txt:239-241`）
  MO3  恰好一页（硬失败 · 本项目 [社区] 口径：一页备忘录）
  MO4  受众在文首点名（硬失败 · 本项目 [社区] 口径，燃料 = 题面）

★ **四条都是硬失败（`FAIL`）** —— 与 `check-section.py` 不同，本工具**没有 `WARN` 档**
  （memo 的四项都可机判，且 MO1/MO2 直接对应官方规则）。
★ **`SKIP` = 无法判定**（既不是 `PASS` 也不是 `FAIL`）：缺 `--problem` ⇒ `MO1`/`MO4` `SKIP`；
  PATH 里没有 `pdflatex` ⇒ `MO3` `SKIP`。**缺燃料一律报"无法判定"，不许报 `PASS`**（fail-closed）。
★ **本工具只判这四项**：**"检查器 PASS" ≠ "这份备忘录写好了"** ——
  措辞 / 受众适配 / 内容覆盖**仍靠人工**（同 `mcm-abstract` 的口径：工具只判形式）。
★ **自查侧是 `mcm-selfreview` 的 `自查 A14`（题目特定要求）** —— 本工具**只给指针、不复述它的判据**。

## 两条官方规则（本工具 `MO1`/`MO2` 的判据源头；★ 仅见于 `MCM-ICM_Tips.txt`）

- **① 触发**（`MCM-ICM_Tips.txt:160-162`）：官方**只陈述**"每题有**各自**的要求"——
  *"Each problem will have different and specific requirements, such as **required memos or letters**,
  specific solution format, and/or page limits."*
  ★ **官方原文并未说"不要求就不许写"**；"题面没要求就绝不产出"是本项目据此推出的**更严操作纪律**，
  标 **`[社区]`**（见下节 `MO1` 口径）。`MO1` 判的是这条 `[社区]` 纪律。
- **② 匿名落款**（`MCM-ICM_Tips.txt:239-241`，**一票否决类**）：
  *"Do not include any type of team identification such as student names, institution name or
  geographical region. If you are required to include a letter with your submission, be sure not to
  sign the letter with your name. If you feel as though you need to have a formal closing to such a
  letter we suggest using: **Sincerely, Team #2000000**."*
  ⇒ **不得署真名 / 校名 / 机构名**；要正式收尾就用官方建议写法 `Sincerely, Team #<队号>`。`MO2` 判它。

## 判据口径（★ 自订项一律标 `[社区]`）

- `MO1` **触发条件在场**：读 `--problem`（题面）判**题面有没有要求 memo/letter**。
  ★ **`[社区]` 操作纪律（由官方① 推出的推论）** —— 官方① **只**说"每题有各自要求（如 required
  memos or letters）"，**未**禁止主动写 memo；本项目据此采取**更严**处置：**题面没要求就绝不产出**
  （产物不该存在 ⇒ `FAIL`；这是它最容易误触发的地方）。
  ★ 燃料 `--problem` **缺失 ⇒ `SKIP`（无法判定）**，**不许报 `PASS`**。
  ★ "要求"的识别：`[社区]` 口径 —— `memo`/`memorandum` 一律算要求；
  `letter` 需**动作上下文**（`write/prepare/include/... letter` 或 `letter ... to/for`），
  以排除 "US **Letter** or A4 page size" 这类**纸张尺寸**误命中。
- `MO2` **匿名落款**：取**落款块**（最后一个正式收尾词起），**须为 `Sincerely, Team #<队号>` 一类形态**；
  **出现真名 / 校名 / 机构名 / 任何非匿名标识 ⇒ `FAIL`**（**官方硬规则 ②**）。
  ★ **无落款**不算违规（官方只在"需要正式收尾"时给建议写法）⇒ `PASS`（带说明）。
  ★ 机构名清单与"残余标识"判法是 [社区] 口径（官方只列举"student names, institution name or
  geographical region"，未给词表）。
- `MO3` **恰好一页**：`pdfLaTeX` **编两遍**，用 `fitz`(PyMuPDF) 读页数（★ 本机有 `pdflatex`、
  无 `pdfinfo`/`pandoc`；口径同 `.claude/skills/mcm-abstract/check-summary.py`）。
  页数 `>1` ⇒ `FAIL`。★ 无 `pdflatex` ⇒ `SKIP`；**非 `.tex` ⇒ fail-closed `FAIL`**。
  ★ "一页"是 [社区] 口径（官方只说"题面可能有页数要求 / 例题是 one-page memo"）。
- `MO4` **受众在文首点名**：从 `--problem` 提取**题面点名的受众**，判它**在备忘录文首出现**。
  ★ 题面里提不出受众、或 `--problem` 缺失 ⇒ `SKIP`。★ "文首 = 前 15 个非空行"是 [社区] 口径。

用法
----
    python check-memo.py <memo.tex> [--problem <题面>] [--keep-temp]
    python check-memo.py --help

- 退出码：**有 `FAIL` ⇒ 非 0**；只有 `PASS`/`SKIP` ⇒ 0。
- **临时件只落仓内 `build/`**（gitignored；**不落 C 盘 / `%TEMP%` / 盘根**），跑完即清
  （`--keep-temp` 可留）。

判据只从失败方向证明：每条 `MO*` 都由 `tests/skills/memo/mutate-memo.py` 的变异体证红。
本工具只读输入、不写仓内文件（编译中间件落在 `build/` 的临时目录、跑完清掉）。
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# --------------------------------------------------------------------------
# 路径
# --------------------------------------------------------------------------

REPO = Path(__file__).resolve().parents[3]      # .claude/skills/mcm-memo/check-memo.py → 仓根

# --------------------------------------------------------------------------
# [社区] 口径常量（自订项；判据源头不含这些线，故一律标 [社区]）
# --------------------------------------------------------------------------

MO4_HEAD_LINES = 15          # [社区]："文首" = 前 15 个非空行
MO3_PAGES_MAX = 1            # [社区]："恰好一页"（>1 即 FAIL）

# --------------------------------------------------------------------------
# 词表 / 正则
# --------------------------------------------------------------------------

# MO1：`[社区]` 识别口径（官方① 举例 "required memos or letters"）—— memo/memorandum 一律算要求。
RE_REQ_MEMO = re.compile(r"\b(?:memo|memorandum)\b", re.I)
# MO1：`letter` 需**动作上下文**，以排除 "US Letter or A4 page size" 的纸张尺寸误命中。
RE_REQ_LETTER = re.compile(
    r"\b(?:write|writing|prepare|preparing|include|including|provide|providing|"
    r"draft|drafting|submit|submitting|compose|composing|attach|attaching|"
    r"require[sd]?|requiring)\b[^.\n]{0,40}?\bletter\b|"
    r"\bletter\b[^.\n]{0,40}?\b(?:to|for)\b", re.I)
# ★ 已知边界（K3 登记；本工具**不修**它 —— 修它属改判据面；★ 本清单**不声称穷尽**）：
#   上述两条正则会**误报**"题面要求 memo/letter"，已登记的成因有：
#   · ① 裸 `memo`/`memorandum` 的**任意**出现（如 "memorandum of understanding"、"the word memo ..."）；
#   · ② `letter` 的**否定式无处理**（如 "Do not write a letter to the editor" 也会被判"要求"）；
#   · ③ RE_REQ_LETTER 在**非交付语境**下也命中（**两个分支都会**）：
#       - `\bletter\b[^.\n]{0,40}?\b(?:to|for)\b` 分支**无动作动词也命中** ——
#         实测 "The letter to the editor was already published."（命中 `letter to`）⇒ 被判"要求"；
#       - **动作动词分支**（`write/prepare/include/… … letter`）**过宽** ——
#         实测 "Please write a letter of recommendation for the dean."（命中 `write a letter`，
#         是"写推荐信"、**非**"题面要求交付 memo/letter"）⇒ 被判"要求"。
#   ★ **方向一律 = 宁可漏、不误红**（宁可不报这类红）；实测登记见 `tests/skills/memo/README.md` §4。

# MO2：正式收尾词（官方举例 `Sincerely`）
RE_SIGNOFF = re.compile(
    r"(?:sincerely|respectfully|yours\s+(?:sincerely|truly|faithfully)|"
    r"best\s+regards|with\s+regards|kind\s+regards|warm\s+regards|regards)\b", re.I)
# MO2：官方建议的匿名落款形态 `Sincerely, Team #2000000`（源码里 `#` 写作 `\#`，故 `\\?#`）
RE_TEAM_SIG = re.compile(r"Team\s*\\?#\s*\d+", re.I)
# MO2：[社区] 机构名清单（官方列举 "institution name" 但未给词表）
RE_INSTITUTION = re.compile(
    r"\b(?:university|universit[aä]t|college|school|institute|institution|academy|"
    r"polytechnic|department|dept|laboratory|laboratories|faculty|campus|high\s+school)\b",
    re.I)
# MO2：[社区] 落款块里"残余标识"的判法 —— 去掉收尾词与 `Team #<n>` 后，还有 ≥2 字母的词即标识。
RE_IDENTIFIER_WORD = re.compile(r"[A-Za-z\u4e00-\u9fff]{2,}")

# MO4：从题面提取"需要 memo/letter ... to/for the <受众>"的受众短语
RE_AUDIENCE = re.compile(
    r"\b(?:memo|memorandum|letter)\b[^.\n]{0,30}?\b(?:to|for)\s+(the\b.+)$", re.I)
# MO4：受众短语的截断词（[社区] 口径）
AUD_STOP = frozenset((
    "summarizing", "summarising", "that", "which", "describing", "outlining",
    "about", "on", "regarding", "detailing", "to", "for", "using", "in", "with",
))
# MO4：匹配时忽略的功能词（不参与"文首点名"的 token 校验）
AUD_SKIP_TOKENS = frozenset(("the", "of", "a", "an", "and", "to", "for", "in", "with", "on"))

RE_END_DOC = re.compile(r"\\end\s*\{document\}")


# --------------------------------------------------------------------------
# 读文本
# --------------------------------------------------------------------------

def read_text(path):
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1(replace)"


# --------------------------------------------------------------------------
# MO1：触发条件在场
# --------------------------------------------------------------------------

def problem_requires_memo(problem_text):
    """题面是否**明确要求** memo/letter（官方 ①）。"""
    m = RE_REQ_MEMO.search(problem_text)
    if m:
        return m.group(0)
    m = RE_REQ_LETTER.search(problem_text)
    if m:
        return m.group(0)
    return None


def check_mo1(problem_text):
    if problem_text is None:
        return ("SKIP", "MO1 触发条件在场",
                "缺 --problem ⇒ 无法判定题面是否要求 memo/letter（fail-closed：不报 PASS）")
    hit = problem_requires_memo(problem_text)
    if hit:
        return ("PASS", "MO1 触发条件在场",
                "题面明确要求 memo/letter（命中 %r）—— 官方①（Tips:160-162）" % hit)
    return ("FAIL", "MO1 触发条件在场",
            "题面**未**要求 memo/letter ⇒ **不得产出该文件**（`[社区]` 操作纪律：由官方① 推出的更严处置；"
            "官方① 只说每题有各自要求、**未**禁止主动写）")


# --------------------------------------------------------------------------
# MO2：匿名落款
# --------------------------------------------------------------------------

def signature_block(text):
    """落款块 = 从**最后一个正式收尾词**到文末（去掉 `\\end{document}`）。无收尾词 ⇒ None。"""
    t = RE_END_DOC.sub("", text)
    ms = list(RE_SIGNOFF.finditer(t))
    if not ms:
        return None
    return t[ms[-1].start():]


def check_mo2(memo_text):
    block = signature_block(memo_text)
    if block is None:
        return ("PASS", "MO2 匿名落款",
                "无正式落款（不违反匿名规则 —— 官方②只在『需要正式收尾』时建议 "
                "Sincerely, Team #<队号>）")
    inst = RE_INSTITUTION.search(block)
    if inst:
        return ("FAIL", "MO2 匿名落款",
                "落款含**机构名** %r ⇒ 违反官方②（不得署 institution name；"
                "建议 Sincerely, Team #<队号>）" % inst.group(0))
    residual = RE_TEAM_SIG.sub(" ", block)
    residual = RE_SIGNOFF.sub(" ", residual)
    words = RE_IDENTIFIER_WORD.findall(residual)
    if words:
        return ("FAIL", "MO2 匿名落款",
                "落款含**非匿名标识** %s ⇒ 违反官方②（不得署真名/标识；"
                "建议 Sincerely, Team #<队号>）" % ", ".join(repr(w) for w in words[:6]))
    if RE_TEAM_SIG.search(block):
        return ("PASS", "MO2 匿名落款",
                "落款为官方建议形态 `Sincerely, Team #<队号>`（官方②；Tips:239-241）")
    return ("PASS", "MO2 匿名落款", "落款无任何标识（不违反官方②）")


# --------------------------------------------------------------------------
# MO3：恰好一页（pdfLaTeX 两遍 + fitz 读页数）
# --------------------------------------------------------------------------

def make_workdir():
    """建一个临时编译目录（★ 优先落仓内 `build/`；不落 %TEMP% / 盘根）。"""
    base = REPO / "build"
    try:
        base.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix="memo-check-", dir=str(base)))
    except OSError:
        return Path(tempfile.mkdtemp(prefix=".memo-check-", dir=os.getcwd()))


def compile_pages(tex_path, workdir):
    """返回 `(pages, err)`；`pages` 为 None 表示读不到（err 说明原因）。"""
    exe = shutil.which("pdflatex")
    if exe is None:
        return None, "PATH 里找不到 pdflatex"
    job = "memo"
    work_tex = workdir / (job + ".tex")
    shutil.copyfile(tex_path, work_tex)
    for _ in range(2):                                   # ★ 编两遍
        subprocess.run([exe, "-interaction=nonstopmode",
                        "-output-directory", str(workdir), str(work_tex)],
                       cwd=str(workdir), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    produced = workdir / (job + ".pdf")
    if not produced.is_file():
        return None, "编译未产出 PDF（pdfLaTeX 失败）"
    try:
        import fitz                                    # PyMuPDF
    except ImportError:
        return None, "需要 PyMuPDF(fitz)"
    try:
        doc = fitz.open(str(produced))
        n = doc.page_count
        doc.close()
        return n, None
    except Exception as e:                              # noqa: BLE001
        return None, "读 PDF 失败: %s" % e


def check_mo3(memo_path, memo_text, keep_temp=False):
    if memo_path.suffix.lower() != ".tex":
        return ("FAIL", "MO3 恰好一页",
                "非 `.tex`（%s）⇒ 无法编译、fail-closed 红" % memo_path.suffix)
    if shutil.which("pdflatex") is None:
        return ("SKIP", "MO3 恰好一页", "PATH 里找不到 pdflatex ⇒ 无法判定页数（fail-closed）")
    workdir = make_workdir()
    try:
        pages, err = compile_pages(memo_path, workdir)
    finally:
        if not keep_temp:
            shutil.rmtree(workdir, ignore_errors=True)
    if pages is None:
        return ("FAIL", "MO3 恰好一页", "无法得到页数：%s" % err)
    if pages > MO3_PAGES_MAX:
        return ("FAIL", "MO3 恰好一页",
                "页数=%d（>%d）⇒ 不是一页（[社区] 口径）" % (pages, MO3_PAGES_MAX))
    return ("PASS", "MO3 恰好一页", "页数=%d（pdfLaTeX 编两遍 + fitz 读）" % pages)


# --------------------------------------------------------------------------
# MO4：受众在文首点名
# --------------------------------------------------------------------------

def extract_audience(problem_text):
    """从题面提取受众短语（`memo/letter ... to/for the <受众>`）。提不出 ⇒ None。"""
    m = RE_AUDIENCE.search(problem_text)
    if not m:
        return None
    phrase = m.group(1).strip()
    toks = re.split(r"\s+", phrase)
    out = []
    for t in toks:
        w = t.strip(",. ;:")
        if w.lower() in AUD_STOP:
            break
        out.append(w)
        if t[-1:] in ".,;:":
            break
    phrase = " ".join(out).strip()
    return phrase or None


def head_text(memo_text, n=MO4_HEAD_LINES):
    lines = [l for l in memo_text.splitlines() if l.strip()]
    return "\n".join(lines[:n])


def check_mo4(memo_text, problem_text):
    if problem_text is None:
        return ("SKIP", "MO4 受众在文首点名",
                "缺 --problem ⇒ 无法判定题面点名的受众（fail-closed：不报 PASS）")
    aud = extract_audience(problem_text)
    if not aud:
        return ("SKIP", "MO4 受众在文首点名",
                "题面里提取不到受众（无 `memo/letter ... to/for the <受众>` 形态）⇒ 无法判定")
    keys = [w for w in re.split(r"\s+", aud)
            if w.strip(",. ;:").lower() not in AUD_SKIP_TOKENS]
    head = head_text(memo_text).lower()
    missing = [k for k in keys if k.lower() not in head]
    if missing:
        return ("FAIL", "MO4 受众在文首点名",
                "题面点名的受众 %r 未在文首点名（前 %d 非空行里缺 %s）"
                % (aud, MO4_HEAD_LINES, ", ".join(repr(w) for w in missing)))
    return ("PASS", "MO4 受众在文首点名",
            "受众 %r 已在文首点名（前 %d 非空行命中全部 token；[社区] 口径）"
            % (aud, MO4_HEAD_LINES))


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

RULE = "=" * 78


def emit(rows):
    for st, cid, detail in rows:
        print("%-4s %-24s # %s" % (st, cid, detail))


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="MCM/ICM letter/memo 自检：MO1 触发条件 / MO2 匿名落款 / MO3 恰好一页 / MO4 受众",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python check-memo.py memo.tex --problem problem.txt\n"
               "  python check-memo.py memo.tex --problem problem.txt --keep-temp\n")
    ap.add_argument("memo_file", nargs="?", help="备忘录 .tex（题面明确要求 letter/memo 时的产物）")
    ap.add_argument("--problem", default=None,
                    help="题面文件（MO1 判『题面是否要求 memo/letter』、MO4 提取受众的燃料）")
    ap.add_argument("--keep-temp", action="store_true",
                    help="保留编译临时目录（默认跑完清掉；★ 临时目录只落仓内 build/）")
    args = ap.parse_args(argv)

    if not args.memo_file:
        sys.stderr.write("错误: 需要 <memo.tex>。见 --help\n")
        return 2

    memo_path = Path(args.memo_file)
    if not memo_path.is_file():
        print("FAIL  FILE                     # 找不到备忘录文件 %s（fail-closed）" % memo_path)
        print("RESULT: FAIL")
        return 1

    memo_text, enc = read_text(memo_path)
    problem_text = None
    if args.problem is not None:
        pp = Path(args.problem)
        if not pp.is_file():
            print("FAIL  PROBLEM                  # 找不到 --problem 文件 %s（fail-closed）" % pp)
            print("RESULT: FAIL")
            return 1
        # ★ 题面先归一空白：`RE_REQ_LETTER` / `RE_AUDIENCE` 的 `[^.\n]` / `$` 不跨行，
        #   不归一的话"受众在题面下一行"就永远提不出来。
        problem_text = re.sub(r"\s+", " ", read_text(pp)[0]).strip()

    rows = [
        check_mo1(problem_text),
        check_mo2(memo_text),
        check_mo3(memo_path, memo_text, keep_temp=args.keep_temp),
        check_mo4(memo_text, problem_text),
    ]

    print(RULE)
    print("check-memo.py · mcm-memo · MO1–MO4")
    print(RULE)
    print("文件=%s" % memo_path.resolve())
    print("编码=%s" % enc)
    print("题面=%s" % ("（未给 --problem ⇒ MO1/MO4 报『无法判定』）" if problem_text is None
                       else Path(args.problem).resolve()))
    print("官方判据源头: ① 触发 MCM-ICM_Tips.txt:160-162 · "
          "② 匿名落款 MCM-ICM_Tips.txt:239-241")
    print()
    emit(rows)

    fails = [cid for st, cid, _ in rows if st == "FAIL"]
    skips = [cid for st, cid, _ in rows if st == "SKIP"]
    passes = [cid for st, cid, _ in rows if st == "PASS"]
    print()
    print("自订阈值均标 [社区]：MO3 一页=%d · MO4 文首=%d 非空行"
          % (MO3_PAGES_MAX, MO4_HEAD_LINES))
    print("汇总: PASS=%d FAIL=%d SKIP=%d" % (len(passes), len(fails), len(skips)))
    if skips:
        print("SKIP（无法判定；退出码不受影响）: %s" % ", ".join(skips))
    if fails:
        print("RESULT: FAIL")
        print("失败项=%s" % ",".join(fails))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
