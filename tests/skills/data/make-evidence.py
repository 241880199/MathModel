#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 5（`mcm-data`）：生成 `tests/skills/data/DATA-evidence.md`（RED × GREEN 对照证据）。

用法：  python tests/skills/data/make-evidence.py

## 它做什么（口径 = 设计 §5）

**RED / GREEN 是「样例驱动」的**（**不是**另起写手 agent 作对照 —— 那是 M4 的口径，本支不用）：

* **RED 侧** = 逐条判据的**违规样例**（`samples/<判据号>/violate/`）跑一遍 `check-data.py --scope artifact`
  的**实测读数** —— 每条确实红，且**红的是它自己那条**（其余判据仍 `PASS`）。
* **GREEN 侧** = 逐条判据的**合规样例**（`samples/<判据号>/comply/`）跑一遍的**实测读数** —— 每条确实绿。
* **对照口径**：**只评「判据红没红」**，不评别的（设计 §5）。

## 两条不变式（写进证据件 · 任务书口径 3）

* **① 判据总数 == `samples/` 下一级目录数**：左 = 检查器 `--scope artifact` **现取**到的判据号集合，
  右 = `samples/` 的**一级目录名**集合，**集合相等**。
* **② `DA4`（人机确认闸）的红，来自「确认缺失」那一行本身**（质检记录 `P6` 的核心）：
  **机器交叉核** —— 检查器判词里**报出的行号**，必须**恰好等于**从样例里**独立读出**的
  「`取数方=AI` 且 `确认` 未「已核」」的**行号**。

## 不动点（硬要求）

**先干净 → 捕获 → 提交 → 再跑一次**，重新生成**字节级一致**。故本器**不含任何非确定性**：
无时间戳 / 无随机序 / **无绝对路径**（检查器 stdout 里的仓根前缀一律**脱敏成 `<REPO>/…`**）/
遍历一律 `sorted()`。★ 证据件里**不写「生成日期」**这类会漂的字段。

## 诚实边界（**不声称穷尽**）

样例是**构造的**、每判据仅**一对**（`n` 小）⇒ **只证明「判据真的会红 / 会绿」，不代表真实赛期表现、也不覆盖全部失效形态**。
"""

import os
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/data
REPO = HERE.parents[2]                                   # 仓根
CHK = REPO / ".claude/skills/mcm-data/check-data.py"
SAMPLES = HERE / "samples"
OUT_DOC = HERE / "DATA-evidence.md"
SELF_MAKE = HERE / "make-evidence.py"
NL = chr(10)
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

STATUS_RE = re.compile(r"^(PASS|FAIL|N/A)\s+(DA\d|SELF\d|TEMPLATE)\b(.*)$")
CRIT_RE = re.compile(r"^DA\d$")
_DATE_RE = re.compile(r"(\d{4}\s*[-/.年]\s*\d{1,2}\s*[-/.月]\s*\d{1,2})")
_HEAD2_RE = re.compile(r"^#{2}\s+(.+?)\s*$")
SIDES = ("comply", "violate")

# 每条判据「打的是什么」—— 一句话命名（信息性，**不是**计数 / 不声称穷尽；源：设计 §4.1 与 `samples/README.md`）
LABELS = {
    "DA1": "来源表在场 + `出处`/`口径`/`局限`/`获取日期`/`取数方` 五列每行非空（`取数方` 取值域 fail-closed）",
    "DA2": "每个**非自主**来源都有对应引用（`[官方]` `corpus/official/instructions.html:1121`）；保留值 `本队自产` 的行豁免",
    "DA3": "`可信度层级` 每行非空且在五级内；保留值 `本队自产` 的行豁免（填 `—`）",
    "DA4": "★ 人机确认闸：凡 `取数方=AI` 的行，`确认` 须「已核」+ 确认人 + 日期（`P6`）",
    "DA5": "清洗与口径对齐步骤有记录、且每步可重跑（启发式：认脚本/命令标记）",
}


def criteria_span(cids):
    """把**现取**到的判据号渲染成标题里的范围说明（**不写死条数**）。

    连续编号（如 `DA1`…`DA5`）⇒ `` `DA1`–`DA5` ``（紧凑）；**一旦不连续**（如缺 `DA3`）
    ⇒ **逐个列出**（`` `DA1`、`DA4` ``）—— **绝不谎报中间项**（不写 `DA1`–`DA4` 以免暗示一个不存在的 `DA3`）。
    """
    if not cids:
        return "（无判据）"
    pre = re.sub(r"\d+$", "", cids[0])
    nums = [int(re.sub(r"^\D+", "", c)) for c in cids]
    contiguous = all(re.sub(r"\d+$", "", c) == pre for c in cids) \
        and nums == list(range(nums[0], nums[0] + len(nums)))
    if contiguous:
        return "`%s`–`%s`" % (cids[0], cids[-1])
    return "、".join("`%s`" % c for c in cids)


# ---------------------------------------------------------------- 基础设施
def rel(p):
    return pathlib.Path(p).relative_to(REPO).as_posix()


def git_blob(p):
    r = subprocess.run(["git", "hash-object", rel(p)], cwd=str(REPO),
                       capture_output=True, text=True)
    return (r.stdout or "").strip()


def _sanitize(text):
    """把检查器 stdout 里的**仓根绝对路径**脱敏成 `<REPO>/…`（去掉绝对路径这一非确定源）。"""
    out = text
    for base in sorted({str(REPO), REPO.as_posix()}, key=len, reverse=True):
        pat = re.compile(re.escape(base) + r"[\\/]([^\s]*)")
        out = pat.sub(lambda m: "<REPO>/" + m.group(1).replace("\\", "/"), out)
        out = out.replace(base, "<REPO>")
    return out


def run_checker(args):
    """跑检查器；返回 `(rc, sanitized_stdout)`。"""
    pr = subprocess.run([sys.executable, str(CHK)] + [str(a) for a in args],
                        cwd=str(REPO), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    return pr.returncode, _sanitize(pr.stdout or "")


def parse_verdict(out):
    v = {}
    for ln in out.splitlines():
        m = STATUS_RE.match(ln)
        if m:
            v[m.group(2)] = (m.group(1), m.group(3).strip())
    return v


def _raw(cmdline, rc, out):
    body = NL.join("      | " + l for l in out.rstrip(NL).splitlines())
    return "$ %s   → exit=%d%s%s" % (cmdline, rc, NL, body)


# ---------------------------------------------------------------- 样例解析（供不变式 ② 独立读数）
def _section_body(text, name):
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        m = _HEAD2_RE.match(ln)
        if m:
            if start is not None:
                return NL.join(lines[start:i])
            if m.group(1).strip() == name:
                start = i + 1
    return NL.join(lines[start:]) if start is not None else None


def _first_table(body):
    cur = []
    for ln in body.splitlines():
        if ln.lstrip().startswith("|"):
            cur.append(ln)
        elif cur:
            return cur
    return cur


def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _is_sep(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells)


def parse_table(path, section):
    """读一个 `## <section>` 下的**第一张表**；返回 `(header, rows)`（无表 ⇒ `(None, [])`）。"""
    text = path.read_bytes().decode("utf-8")
    body = _section_body(text, section)
    if body is None:
        return None, []
    table = _first_table(body)
    if not table:
        return None, []
    header = _cells(table[0])
    body_rows = table[1:]
    if body_rows and _is_sep(_cells(body_rows[0])):
        body_rows = body_rows[1:]
    return header, [_cells(r) for r in body_rows]


def _norm_party(s):
    """规范化 `取数方`（与 `check-data.py` 同口径）：去空白/反引号、大小写不敏感、允许 `AI` 前缀。"""
    v = s.strip().strip("`").strip()
    if not v:
        return None
    if v.upper().startswith("AI"):
        return "AI"
    if v == "本人":
        return "本人"
    return None


def _confirm_present(cell):
    """`确认` 列是否已核（含「已核」且记日期）—— **独立于检查器**的轻量读数。"""
    c = cell.strip().strip("`").strip()
    return ("已核" in c) and bool(_DATE_RE.search(c))


# ---------------------------------------------------------------- 逐对跑
def pair_run(cid, side):
    d = SAMPLES / cid / side
    args = ["--scope", "artifact", rel(d / "data-sources.md"), "--refs", rel(d / "paper.md")]
    rc, out = run_checker(args)
    return {"cmd": "check-data.py " + " ".join(args), "rc": rc, "out": out, "v": parse_verdict(out)}


# ---------------------------------------------------------------- main
def main():
    sample_ids = sorted(d.name for d in SAMPLES.iterdir() if d.is_dir())

    # ---- 现取判据清单（在干净合规侧上读）----
    _rc0, _out0 = run_checker(["--scope", "artifact",
                               rel(SAMPLES / "DA1/comply/data-sources.md"),
                               "--refs", rel(SAMPLES / "DA1/comply/paper.md")])
    base = parse_verdict(_out0)
    criteria = sorted(k for k in base if CRIT_RE.match(k))
    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ fail-closed（检查器没出 DA* 行？）")
        return 1

    # ---- 不变式 ①（含自证探针）----
    inv1 = (set(criteria) == set(sample_ids)) and (len(criteria) == len(sample_ids))
    probe1 = (not ((set(criteria) == set(sample_ids + ["DA9"])) and
                   (len(criteria) == len(sample_ids + ["DA9"])))) and \
             (not ((set(criteria + ["DA9"]) == set(sample_ids)) and
                   (len(criteria + ["DA9"]) == len(sample_ids))))
    if not (inv1 and probe1):
        print("RUN: 不变式 ① 不成立（判据 %s vs 样例目录 %s）⇒ fail-closed" % (criteria, sample_ids))
        return 1

    # ---- RED / GREEN 逐对跑 ----
    runs = {}
    for cid in sample_ids:
        runs[cid] = {side: pair_run(cid, side) for side in SIDES}

    # RED 侧断言：violate 把**它自己那条**判 FAIL、其余全 PASS
    red_ok = {}
    for cid in criteria:
        r = runs[cid]["violate"]
        others = [i for i in criteria if i != cid]
        ok = (r["rc"] != 0) and (r["v"].get(cid, ("",))[0] == "FAIL") \
            and all(r["v"].get(i, ("",))[0] == "PASS" for i in others)
        red_ok[cid] = ok
    # GREEN 侧断言：comply 全 PASS
    green_ok = {}
    for cid in criteria:
        r = runs[cid]["comply"]
        ok = (r["rc"] == 0) and all(r["v"].get(i, ("",))[0] == "PASS" for i in criteria)
        green_ok[cid] = ok

    if not (all(red_ok.values()) and all(green_ok.values())):
        print("RUN: RED/GREEN 未全部达预期 ⇒ fail-closed")
        print("  red_ok =", red_ok)
        print("  green_ok =", green_ok)
        return 1

    # ---- 不变式 ②（DA4 人机确认闸）----
    h_v, rows_v = parse_table(SAMPLES / "DA4/violate/data-sources.md", "来源表")
    h_c, rows_c = parse_table(SAMPLES / "DA4/comply/data-sources.md", "来源表")
    ip, ic = h_v.index("取数方"), h_v.index("确认")
    ai_rows_v = [i for i, row in enumerate(rows_v, 1) if _norm_party(row[ip]) == "AI"]
    miss_rows_v = [i for i in ai_rows_v if not _confirm_present(rows_v[i - 1][ic])]
    ai_rows_c = [i for i, row in enumerate(rows_c, 1) if _norm_party(row[ip]) == "AI"]
    miss_rows_c = [i for i in ai_rows_c if not _confirm_present(rows_c[i - 1][ic])]
    _rcv, out_v = run_checker(["--scope", "artifact",
                               rel(SAMPLES / "DA4/violate/data-sources.md"),
                               "--refs", rel(SAMPLES / "DA4/violate/paper.md")])
    vv = parse_verdict(out_v)
    reported_v = sorted(int(x) for x in re.findall(r"第(\d+)行；", vv.get("DA4", ("", ""))[1]))
    # violate 侧：DA4 判 FAIL · 有确认缺失行 · 检查器报出的行 == 独立读出的确认缺失行
    inv2 = (vv.get("DA4", ("",))[0] == "FAIL") and bool(miss_rows_v) \
        and (reported_v == sorted(miss_rows_v))
    # comply 侧：AI 行存在、确认齐 ⇒ DA4 PASS
    rc_c, out_c = run_checker(["--scope", "artifact",
                               rel(SAMPLES / "DA4/comply/data-sources.md"),
                               "--refs", rel(SAMPLES / "DA4/comply/paper.md")])
    vc = parse_verdict(out_c)
    inv2_c = (bool(ai_rows_c) and not miss_rows_c) and (vc.get("DA4", ("",))[0] == "PASS")
    inv2 = inv2 and inv2_c
    if not inv2:
        print("RUN: 不变式 ② 不成立（报出行 %s vs 独立读出确认缺失行 %s）⇒ fail-closed"
              % (reported_v, miss_rows_v))
        return 1

    # ---- 内检（`--scope self`）读数（补充证据，非 RED/GREEN）----
    scr, sout = run_checker(["--scope", "self"])
    self_v = parse_verdict(sout)

    # ---- blob 自证 ----
    chk_blob = git_blob(CHK)
    mk_blob = git_blob(SELF_MAKE)
    fixture_blobs = []
    for cid in sample_ids:
        for side in SIDES:
            for p in sorted((SAMPLES / cid / side).rglob("*")):
                if p.is_file():
                    fixture_blobs.append((p, git_blob(p)))

    # ================================================================ 生成文档
    L = []
    a = L.append
    a("# Task 5 · RED × GREEN 对照证据（`mcm-data` · %s）" % criteria_span(criteria))
    a("")
    a("本文件由 `tests/skills/data/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("**它不含**时间戳 / 随机序 / 绝对路径（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`）"
      "⇒ **重新生成字节级一致**（不动点，见 §6）。**§1–§4 是机器抽取**（逐字解析检查器 stdout、"
      "逐条跑样例）；**§5 的边界是手写**（文里已标明）。")
    a("")

    # ---- §0
    a("## §0 口径（样例驱动 · 只评「判据红没红」 · 现取判据清单）")
    a("")
    a("- **RED / GREEN 是「样例驱动」的**（设计 §5；**不是**另起写手 agent 作对照）：")
    a("  - **RED 侧** = 逐条判据的**违规样例**（`tests/skills/data/samples/<判据号>/violate/`）跑"
      "`check-data.py --scope artifact` 的**实测读数** —— 每条确实红，**且红的是它自己那条**。")
    a("  - **GREEN 侧** = 逐条判据的**合规样例**（`…/comply/`）跑一遍的**实测读数** —— 每条确实绿。")
    a("- **对照口径**：**只评「判据红没红」**，不评别的（设计 §5）。")
    a("- **判据清单现取**（**不写死条数**）：从检查器 stdout 现取 `DA*` 行 ⇒ 本次 **%d 条**（`%s`）。"
      % (len(criteria), "、".join(criteria)))
    a("- **检查器自证**：`.claude/skills/mcm-data/check-data.py` worktree blob `%s`（本支不动它；两侧同一版）。"
      % chk_blob[:12])
    a("- **样本量边界**：样例是**构造的**、每判据仅**一对**（`n` 小）⇒ 见 §5 —— **不声称穷尽**失效形态。")
    a("")

    # ---- §1 不变式 ①
    a("## §1 不变式 ①：判据总数 == `samples/` 下一级目录数")
    a("")
    a("| 现取到的判据（左） | 条数 | `samples/` 一级目录（右） | 个数 | 集合相等 |")
    a("| :-- | --: | :-- | --: | :-- |")
    a("| %s | %d | %s | %d | **%s** |"
      % ("、".join(criteria), len(criteria), "、".join(sample_ids), len(sample_ids),
         "是" if inv1 else "否"))
    a("")
    a("★ 两边**现取**：删掉检查器里任一条判据 ⇒ 左少一个；删掉任一样例目录 ⇒ 右少一个；**两边都会当场红**。")
    a("★ 该不变式**自带一条自证探针**：喂一对不等集合必判否 ⇒ **%s**（断言没被架空）。"
      % ("OK" if probe1 else "失败 <<<"))
    a("")

    # ---- §2 RED
    a("## §2 RED 侧：逐条判据的**违规样例**实测读数（`violate/`）")
    a("")
    a("### §2.1 汇总（机器抽取：逐条 status）")
    a("")
    a("| 判据 | 它自己这条 | 同侧其余判据 | 该侧 `exit` | 只红它自己 |")
    a("| :-- | :-- | :-- | --: | :-- |")
    for cid in criteria:
        r = runs[cid]["violate"]
        others = [i for i in criteria if i != cid]
        ost = all(r["v"].get(i, ("",))[0] == "PASS" for i in others)
        a("| `%s` | **%s** | 其余 %d 条 = %s | %d | %s |"
          % (cid, r["v"].get(cid, ("",))[0], len(others),
             "PASS" if ost else "（有非 PASS）", r["rc"], "**是**" if red_ok[cid] else "否 <<<"))
    a("")
    a("★ 每行**只评「它自己那条」红没红**（设计 §5 的对照口径）；**不评别的**。")
    a("")

    # ---- §2.2 RED raw stdout
    a("### §2.2 RED 原始 stdout（逐条判据的 `violate/` 跑一遍 · **逐字**贴检查器输出）")
    a("")
    for cid in criteria:
        r = runs[cid]["violate"]
        a("**`%s`** —— 打的是：%s" % (cid, LABELS.get(cid, "")))
        a("")
        a("```")
        a(_raw(r["cmd"], r["rc"], r["out"]))
        a("```")
        a("")

    # ---- §3 GREEN
    a("## §3 GREEN 侧：逐条判据的**合规样例**实测读数（`comply/`）")
    a("")
    a("### §3.1 汇总（机器抽取：逐条 status）")
    a("")
    a("| 判据 | `comply/` 全员 status | 该侧 `exit` | 全绿 |")
    a("| :-- | :-- | --: | :-- |")
    for cid in criteria:
        r = runs[cid]["comply"]
        allp = all(r["v"].get(i, ("",))[0] == "PASS" for i in criteria)
        a("| `%s` | %s | %d | %s |"
          % (cid, "全 PASS" if allp else "（有非 PASS）", r["rc"], "**是**" if green_ok[cid] else "否 <<<"))
    a("")
    a("### §3.2 GREEN 原始 stdout（逐条判据的 `comply/` 跑一遍 · **逐字**贴检查器输出）")
    a("")
    for cid in criteria:
        r = runs[cid]["comply"]
        a("**`%s`** —— 打的是：%s" % (cid, LABELS.get(cid, "")))
        a("")
        a("```")
        a(_raw(r["cmd"], r["rc"], r["out"]))
        a("```")
        a("")

    # ---- §4 不变式 ②
    a("## §4 不变式 ②：`DA4`（人机确认闸）的红来自「确认缺失」那一行本身（`P6` 的核心）")
    a("")
    a("**机器交叉核**（两条独立路径对齐）—— 路径 1 = 检查器判词里**报出的行号**；"
      "路径 2 = 从样例表里**独立读出**的「`取数方=AI` 且 `确认` 未「已核」」的**行号**。")
    a("")
    a("| 侧 | `取数方=AI` 的行（路径 2） | 其中「确认缺失」的行（路径 2） | 检查器**报出**的行（路径 1） | `DA4` status | 对齐 |")
    a("| :-- | :-- | :-- | :-- | :-- | :-- |")
    a("| `DA4/violate` | %s | %s | %s | %s | **%s** |"
      % (ai_rows_v, miss_rows_v, reported_v, vv.get("DA4", ("",))[0],
         "是" if reported_v == sorted(miss_rows_v) else "否 <<<"))
    a("| `DA4/comply` | %s | %s | （空） | %s | **是** |"
      % (ai_rows_c, miss_rows_c, vc.get("DA4", ("",))[0]))
    a("")
    a("★ **读法**：`violate/` 侧把**确认那格**从「已核（…）」改成「待核」—— **只动这一格**；"
      "`DA4` 的 `FAIL` 判词 **`<<< 第%d行；仍为「待核」`** 报的正是**那条 AI 行本身**"
      "（不是别行、不是别的判据连坐）⇒ 这就是设计 §1.2 那句边界话的**机械落地**。"
      % (miss_rows_v[0] if miss_rows_v else 0))
    a("★ **`comply/` 侧**同一行填「已核（…, 日期）」⇒ `DA4` 判 `PASS` ⇒ **正反真的分得开**。")
    a("★ 该不变式**不靠手抄行号**：行号由**样例表当场读出**、再与**检查器报出**的行号**集合比对**。")
    a("")

    # ---- §5 边界
    a("## §5 诚实边界（**不声称穷尽** · 手写）")
    a("")
    a("- ★★ **样本量边界（原话）**：**样例是构造的** —— 每条判据**只钉一对**（`comply` + `violate`），"
      "`n` 小 ⇒ **本文只证明「判据真的会红 / 会绿」，不代表真实赛期表现、也不覆盖全部失效形态**。"
      "**凡本文列的清单都不声称穷尽。**")
    a("- ★ **RED / GREEN 是「样例驱动」的**（设计 §5）：**不另起写手 agent 作对照** ⇒ 它**证明不了**"
      "「一个不看 skill 的写手会不会踩同样的坑」——**那是另一支（M4）的口径，本支不做**。")
    a("- ★ **外检是启发式**（设计 §4.4）：`DA2`（出处全列搜子串）、`DA3`（五级启发式）、"
      "`DA5`（可重跑认脚本/命令标记）**都有假阳性 / 假阴性面**；本文只如实贴某一次读数，**不背书内容对错**。")
    a("- ★ **只评「判据红没红」**：本文不对样例产物的**质量**下任何判断（设计 §5 的对照口径）。")
    a("")

    # ---- §6 可重放性
    a("## §6 可重放性（**不动点**：先干净 → 捕获 → 提交 → 再跑一次）")
    a("")
    a("- **本文件完全由生成器当场产出**：`python tests/skills/data/make-evidence.py`（跑完 `git status --short` 应为空）。")
    a("- **不动点的证法**：在**已提交的树上**、**同一操作系统内**重跑本生成器 ⇒ **本文件逐字节不变**"
      "（跑后 `git status --short` 仍为空）；**平台边界见下条**。")
    a("- **非确定性被逐项堵住**：无时间戳 / 无 `random` / 无 `set` 遍历序（一律 `sorted()`）/"
      "**无绝对路径**（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`）⇒ **不写「生成日期」这类会漂的字段**。")
    a("- ★ **平台边界（非跨平台规范形）**：本件内含**检查器 stdout 逐字捕获的 Windows 反斜杠相对路径**"
      "（如 `refs   = tests\\…` —— `pathlib` 在 Windows 上按 `os.sep` 渲染）⇒ **不动点只在同一操作系统内成立**；"
      "换 Linux/macOS 重跑**不再逐字节一致**。")
    a("- **它实跑**：`check-data.py`（逐对 ×2 侧 + 一次 `--scope artifact` 现取判据 + 不变式 ② 的两次 + 一次 `--scope self`）。")
    a("")

    # ---- §7 生成器口径 / blob
    a("## §7 生成器口径与数据来源（机器抽取 · blob 当场跑 `git hash-object`）")
    a("")
    a("- 生成器 `tests/skills/data/make-evidence.py` blob `%s`。" % mk_blob[:12])
    a("- 检查器 `.claude/skills/mcm-data/check-data.py` blob `%s`（本支不动它）。" % chk_blob[:12])
    a("- 样例夹具逐件 blob：")
    a("")
    a("| 夹具 | blob |")
    a("| :-- | :-- |")
    for p, bl in fixture_blobs:
        a("| `%s` | `%s` |" % (rel(p), bl[:12]))
    a("")
    a("- **内检 `--scope self`（补充读数，非 RED/GREEN）**：")
    a("")
    a("```")
    a(_raw("check-data.py --scope self", scr, sout))
    a("```")
    a("")
    a("- ★ **本文不声称穷尽**：只覆盖 `samples/` 里**现存的**那一对一夹具 + 检查器判的那几条判据。")
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace(chr(13) + chr(10), NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", rel(OUT_DOC), OUT_DOC.stat().st_size, "B")
    print("criteria %d: %s" % (len(criteria), criteria))
    print("GREEN all-PASS = %s · RED only-own = %s"
          % (all(green_ok.values()), all(red_ok.values())))
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
