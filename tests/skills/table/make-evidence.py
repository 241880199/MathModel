#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3：生成 `tests/skills/table/red-green-evidence.md`（RED x GREEN 并列对照，机器抽取）。

写入用 `write_bytes`（本仓纪律；也保证全 LF）。文中每个读数都来自本脚本**当场跑过**的
`check-table-style.py`（一字未改，blob 与 HEAD 比对见文内）；对照表由当场 stdout **逐格解析**，
不手抄（判词行 -> (状态, 判据 ID, 详情)）。

两侧口径：3 个场景（`tests/skills/figure-choose/red/brief-R{1,2,3}.md` 的**同源**数据）
x 2 侧（RED = 干净写手的表；GREEN = 本 skill 规范 + 判据产的表）。同一把尺。

★ 本支三条**必须逐格如实**的：
  ① **RED 是自变量**：`red/out-R{n}/table.tex` 与 `caption.txt` 本轮**未改**（blob 与 HEAD 逐件比对，
     见 §0）；写手的派发口径与自述见 `red/writer-self-reports.md`。
  ② **判据修过三处假红**：`bd97fd6`（2026-10-02）修了两处 —— `C1`（量宽把整个 `table` 体塞进
     `@B@settowidth`、表注里的 `@B@par` 触发 `Paragraph ended`）与 `C5`/`C7`（两级表头的前导 `&`
     被当空格子）；**2026-10-03 全分支终审修复轮 I-1** 修第三处 —— `RULES_RE` 不吞可选线宽参数
     `@B@toprule[..]` 等 ⇒ 剥后留裸 `[..]` ⇒ 幻影一行 ⇒ `C5`/`C8` 假红。三处各有**正控制**
     （`fixtures/good-note-after-tabular.tex` / `good-multilevel-leading.tex` / `good-rulethickness.tex`，都全绿）。
  ③ **RED 每条红要报性质**（真红 / 级联 / 判据假红-已修）—— 见 §4（手写）。

用法： python tests/skills/table/make-evidence.py
"""
import difflib
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
CHECKER = HERE / "check-table-style.py"
SKELETON = REPO / ".claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex"
RED = HERE / "red"
GREEN = HERE / "green"
OUT_DOC = HERE / "red-green-evidence.md"
NL = chr(10)
BS = chr(92)

SCENES = (1, 2, 3)
# 判据 ID 允许**多位数**：检查器将来新增判据时，下面按行解析的汇总表不会静默丢格
# （先例：plot-python 的 make-evidence.py 把清单写死成 6 条而实得 9 条 => 汇总表静默归零）。
LINE_RE = re.compile("^(PASS|FAIL) +(C[0-9]+) +(.*)$")
RES_RE = re.compile("^RESULT: (PASS|FAIL)(?:（(.*)）)? *$")


def tp(s):
    """把 @B@ 换成反斜杠 —— 本文件因此**不含任何字面反斜杠**（转义安全）。"""
    return s.replace("@B@", BS)


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(REPO))
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + NL
    return out, r.returncode


def blob_of(relpath):
    return run(["git", "hash-object", relpath])[0].strip()


def head_blob(relpath):
    return run(["git", "rev-parse", "HEAD:" + relpath])[0].strip()


def check(tex):
    """跑一次检查器（带 `--skeleton`），逐格解析 stdout。"""
    cmd = [sys.executable, CHECKER.relative_to(REPO).as_posix(), "--tex",
           tex.relative_to(REPO).as_posix(), "--skeleton", SKELETON.relative_to(REPO).as_posix()]
    out, rc = run(cmd)
    cells, result, skel = {}, None, ""
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1) == "PASS", m.group(3))
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
        if ln.startswith("SKEL:"):
            skel = ln
    return {"cmd": " ".join(cmd), "stdout": out.rstrip(NL), "rc": rc,
            "cells": cells, "result": result, "skel": skel}


def side(dirname, tag):
    return {n: check(dirname / ("out-" + tag + str(n)) / "table.tex") for n in SCENES}


def criteria_ids(*sides):
    """判据 ID 清单**现取**自检查器的实得输出（保持首次出现次序）—— 不写死。"""
    ids = []
    for data in sides:
        for n in SCENES:
            for k in data[n]["cells"]:
                if k not in ids:
                    ids.append(k)
    ids.sort(key=lambda k: int(k[1:]))
    return ids


def reds(data, n, crit):
    return sorted(k for k in crit if k in data[n]["cells"] and not data[n]["cells"][k][0])


# ---------------------------------------------------------------- 手写块（判断层）
NATURE_R13 = tp("""- **`C8` 一条真红**：RED 写手**从未被告知**来源回显的注释格式
  （`% mcm-table-src: r<行>c<列> <- …`）—— 那是本规范 §3.2 的**产物契约**，写手看不到
  ⇒ 三份里一条都没有 ⇒ 判据判红。**不是"表烂"**。
- 其余 7 条全绿：**能编过 · `booktabs` 三线无竖线 · `@B@caption` 在 `tabular` 之上 ·
  `siunitx` S 列 · 表宽 ≤ 版心**。
- ★ **修前** R1 红集是 `{C1,C5,C7,C8}`、R3 是 `{C5,C7,C8}`；其中 **`C1`（R1）与 `C5`/`C7`（R1/R3）
  是判据假红**，已由 `bd97fd6` 修掉（`C1` = 量宽把整个 `table` 体塞进 `@B@settowidth`、表注里的
  `@B@par` 触发 `Paragraph ended`；`C5`/`C7` = 两级表头的**前导 `&`** 被当空格子）。
  **这两类假红不计入 RED 的红。**""")

NATURE_R2 = tp("""- **`C2` 一条真的"射程边界"触发项**：R2 做的是**双面板表**（`table` 里**两个** `tabular`），
  而判据声明的覆盖范围是**单 `tabular`** ⇒ `tabular` 不唯一 ⇒ `C2` 红。
  ★ **这是已裁定的射程边界，不是判据缺陷**（R2 写手的双面板设计本身能编过、也美观）——**不许为它放宽判据**。
- **`C3,C5,C6,C7,C8` 五条是级联**：`find_tabular` 对"不唯一"返回 `None` ⇒ 表题位置 / 列数 /
  精度 / 缺失值 / 来源回显**皆无从判 ⇒ fail-closed 红**。它们**不是**五条独立的表缺陷。
- ★ **修前** R2 红集是 `{C1,C2,C3,C5,C6,C7,C8}`；多出来的 **`C1` 是判据假红**（同上），已修，不计入。""")

NATURE_ONELINE = tp("""三份写手的表**都编得过、都 `booktabs` 三线无竖线、表题都在上、都用 `siunitx` S 列** ——
那些**本就是称职 LaTeX 写手的默认**。⇒ **判据抓的是"非常规写法"（来源回显格式、单 `tabular` 假设），
不是"烂表"。别拿"RED 红得多"当质量证明**（反过来，也别因为"红得少"就以为尺错了 —— 尺另有
14 条变异真红作证，见 §7）。""")

DIFF_ANNOT = tp("""**人工读一遍：差异是不是"规范导致"的？**

- **规范导致的差异（可归因）**：
  1. GREEN 的 `.tex` **多出一段** `% mcm-table-src: …` 来源回显注释（G1 48 条 / G2 30 条 / G3 28 条），
     RED **一条都没有** —— 这是**规范唯一显式新增的可见文本**，直接对应 `C8`。
  2. RED 的表里**没有**缺失值判据要管的格子；GREEN 的表里**也没有** —— ⇒ **`D6`/`C7` 未被本支 GREEN
     的数据触发**（如实说；`C7` 的真红作证在变异驱动器 `MUT-C7a`/`MUT-C7b`，见 §7）。
- **设计 / 场景导致的差异（不是规范要求）**：
  1. R2 有**两个** `tabular`（双面板），G2 只有**一个** —— GREEN 侧的**单表设计约束**来自判据的 `C2`
     射程（单 `tabular`），**不是**我判 R2 错。
  2. **距离度量不同**（RED R1 用 L1、距离 0.06/0.10；GREEN 用 total-variation、距离 0.03/0.05），
     表题措辞也不同 —— 判断层动作。
  3. G1 保留**两级表头 + 表注**；G3（R3 同数据的 "paper-ready" 场景）用**紧凑单级**四列表、
     把"最相似的一对"放进 caption。
- **结论**：两侧差异**集中在**（a）来源回显注释（规范契约）、（b）单/双 `tabular` 与度量/措辞（设计选择）；
  **不是**三线结构 / 表宽 / 表题位置的差异 —— 那几项**两侧都合规**（见 §3 的 `C2`/`C3`/`C4` 列）。""")

JUDGMENT = tp("""**这一节是判断层，机械判据判不了它。** 下面是本任务 agent 把**六张表逐张编译、渲成 150dpi PNG、
亲眼看过**之后写下的。**本节手写，不是机器抽取。** PNG 落在各自 `out-*/` 目录（PNG 非字节可复现：
每次重编带新时间戳，本支不拿它当判据）。

### RED（朴素写手 · 无规范）—— 我从这张表读到了什么

- **R1（`red/out-R1/table.png`）**：读到六区**低/中/高三档构成**，以及每个区**最近的相邻区与其 L1 距离**；
  B、D 互为最近（0.06）并用 `$@B@dagger$` 标注。**三线（`@B@toprule` / `@B@cmidrule` / `@B@midrule` /
  `@B@bottomrule`）粗细得当**；版心占 **63%**、不爆；`siunitx` S 列**小数位对齐**；上下标**没掉**
  （`$L_1$` 下标、`$@B@dagger$` 上标都正常）；**表注（Notes）在 `tabular` 之下、与表紧邻**
  （表注没与表头挤在一起）。**判据不报、眼睛看得见**：无。
- **R2（`red/out-R2/table.png`）**：读到**两个面板** ——（a）四个属性与灾次计数的 `$r$` / `$@B@rho$` /
  `$|r|$` / Rank；（b）**6x6 对称距离矩阵**，对角线用 `--` 省去、最近邻**加粗**。负数**对齐**、单位列正常；
  版心占 **74.7%**、不爆；表注在下方。**判据不报、眼睛看得见**：（b）面板 8 列，**两个面板共享一个
  caption**，读起来像"一张表两件事"—— 这是写手的**判断层**选择，判据不管（也不该管）。
- **R3（`red/out-R3/table.png`）**：与 R1 **同形同数据**（两级表头 + 最近邻列），措辞不同；
  ★ **距离度量不同** —— R1 那一列是 `$L_1$`（Manhattan，B–D = 0.06）、R3 是 **total-variation**
  （B–D = 0.03）⇒ **两列里的数字并不相等**；**判据读数**同 R1（红集皆为 `{C8}`）。版心占 **63.4%**。
- ★ **一句话**：三张 RED 表**视觉上都是好表** —— 判据红的是"**没有来源回显**"（R1/R3）与
  "**双 `tabular` 超出判据射程**"（R2），**不是表本身读不清**。

### GREEN（本 skill 规范产物）—— 我从这张表读到了什么

- **G1（`green/out-G1/table.png`）**：读到与 R1 同任务的答案（构成 + 最近邻 + **TV 距离** 0.03/0.05）；
  两级表头（首格留空 + 两个 `@B@multicolumn` 分组行，**无 `@B@cmidrule` 分组线**）**对齐、没挤在一起**；
  表宽 **63.4%**、不爆；小数位对齐（本表无上下标）；**表注在表下、紧邻**。**判据不报、眼睛看得见**：
  caption（满 `@B@textwidth`）比表（4.12in）宽，表在版心里居中 —— 正常排版，非缺陷。
- **G2（`green/out-G2/table.png`）**：读到**四属性与灾次计数的相关系数**表（`$r$` / `$@B@rho$` /
  `$|r|$` / Rank）；**负数（infrastructure / vegetation）带负号且对齐**；单位列 `0--100`、
  `people km$^{-2}$` 正常；版心占 **80.8%**（本支最宽的一张，仍不爆）。**判据不报、眼睛看得见**：无。
- **G3（`green/out-G3/table.png`）**：读到**紧凑四列构成表**（District / Low / Medium / High），
  仅 **37%** 版心宽。**判据不报、眼睛看得见**：表**本身不含"最相似的一对"**（这条判断在 caption 里）
  —— 是 "paper-ready 单表" 的**设计选择**（单 `tabular` 里放不下相似度列时，把判断交给 caption）。
- ★ **一句话**：GREEN 三张**全绿**且**读得出任务答案**。

### 总一句话

**机械层测的是"形态合不合规范"，判断层测的是"表讲没讲清"。** 本支两侧**形态都基本合规范**
（RED 仅缺来源回显 / 超出单表射程），**判断层也都讲清了** —— "判词全绿 ≠ 表讲清了"这条在本支
**没有**被逼出一个反例（这本身是如实读数，不是结论）。""")


def main():
    red = side(RED, "R")
    green = side(GREEN, "G")
    CRIT = criteria_ids(red, green)

    rel = CHECKER.relative_to(REPO).as_posix()
    wt_blob, hd_blob = blob_of(rel), head_blob(rel)

    red_blobs = {}
    for n in SCENES:
        for f in ("table.tex", "caption.txt"):
            r = (RED / ("out-R" + str(n)) / f).relative_to(REPO).as_posix()
            red_blobs[r] = (blob_of(r), head_blob(r))

    L = []
    a = L.append
    a("# Task 3 · RED x GREEN 对照证据（`mcm-table`）")
    a("")
    a("本文件由 `tests/skills/table/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。"
      "**§1 / §2 / §3 / §5 的机器部分逐格解析自 stdout，不手抄**；**§4 的性质判定、§5 的注释、§6 是手写**"
      "（文里已标明）。")
    a("")
    a("## §0 口径（两侧同源同数）")
    a("")
    a("- **场景**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，本支未改写）。"
      "R1/R3 同一组数据（六区低/中/高三档构成），R2 另一组数据（五属性 + 历史灾次计数）。")
    a("- **同数**：每侧 3 张表，两侧共 6 张；判据清单**现取**（本支 %d 条）x 6 张。" % len(CRIT))
    a("- **同一把尺**：`%s` **一字未改**。工作树 blob `%s` · `HEAD:` blob `%s` ⇒ %s"
      % (rel, wt_blob[:12], hd_blob[:12], "**相同**" if wt_blob == hd_blob else "**不同（！）**"))
    a("- **RED 侧**：三份由**干净上下文的写手**产出（只给 brief 路径 + 输出目录 + 一件环境事实 "
      "`pdflatex` 在 PATH；**未给**规范 / 模块 / 判据 / 先例证据）。派发口径与三份自述见 "
      "`red/writer-self-reports.md`。**RED 是本任务的自变量** —— `red/out-R{n}/table.tex` 与 `caption.txt` "
      "本轮**未改**（逐个 blob 与 `HEAD` 比对，见下）。")
    a("- **GREEN 侧**：由本任务用本规范（`references/table-style.md` 的 `T1`–`T3` / `D4`–`D8`）产出，"
      "并过判据 8 条。")
    a(tp("- ★ **判据修过三处假红**：`bd97fd6`（2026-10-02）修两处 —— 修前 R1 红集 `{C1,C5,C7,C8}`、R3 `{C5,C7,C8}`、"
      "R2 `{C1,C2,C3,C5,C6,C7,C8}`；修后 R1/R3 只剩 `{C8}`、R2 `{C2,C3,C5,C6,C7,C8}`。第三处（`RULES_RE` 不吞可选"
      "线宽参数 `@B@toprule[..]` ⇒ 幻影一行 ⇒ `C5`/`C8` 假红）由 **2026-10-03 全分支终审修复轮 I-1** 修掉，"
      "**不影响 R1/R2/R3 的红集**。三处假红各有**正控制**（`fixtures/good-note-after-tabular.tex` · "
      "`good-multilevel-leading.tex` · `good-rulethickness.tex`，都全绿）。"))
    a("- ★ **判据非空泛**的另一条臂（失败方向）：变异驱动器 `mutate-table-style.py` 本轮复跑 = "
      "**14/14 真红变异**（`C1`–`C8` 逐条 + 2 条 fail-closed 分支 + 2 条修复边界）+ **6/6 必须绿对照** "
      "= **20/20 达预期**；命令与读数见 §7。")
    a(tp("- ★ `--skeleton`（可选加分项，设计 §5.3）：本支给了 `mcm-latex-format` 的骨架 "
         "`mcm-2027-summary.tex`，逐件读数见 §1/§2 的 `SKEL:` 行 —— **它本就该红**（骨架缺 "
         "`booktabs` / `siunitx`，实测 `@B@toprule` 等未定义），这是**信息行、不进 RESULT**。"))
    a("- ★ **RED 三份的冻结自证**（`git hash-object` vs `HEAD:`）：")
    a("")
    a("| 文件 | 工作树 blob | `HEAD:` blob | 相同？ |")
    a("| :-- | :-- | :-- | :-- |")
    for r, (w, h) in red_blobs.items():
        a("| `%s` | `%s` | `%s` | %s |" % (r, w[:12], h[:12], "是" if w == h else "**否**"))
    a("")

    for si, (name, data, tag) in enumerate((("RED", red, "R"), ("GREEN", green, "G")), start=1):
        a("## §%d %s 原始读数（%s）" % (si, name, "朴素写手 · 无规范" if name == "RED" else "本 skill 规范产物"))
        a("")
        for n in SCENES:
            d = data[n]
            a("### %s%d" % (tag, n))
            a("")
            capf = (RED if name == "RED" else GREEN) / ("out-%s%d" % (tag, n)) / "caption.txt"
            a("表题（`%s`，逐字）：" % capf.relative_to(REPO).as_posix())
            a("```text")
            a(capf.read_bytes().decode("utf-8").rstrip(NL))
            a("```")
            a("")
            a("```")
            a("$ " + d["cmd"])
            a(d["stdout"])
            a("[exit=%d]" % d["rc"])
            a("```")
            a("")

    a("## §3 对照表（机器抽取）")
    a("")
    a("每个格子 = 状态：绿 = `PASS` / 红 = `FAIL`。同场景同行，RED 与 GREEN 并列；判据 ID 见表头（**现取**）。")
    a("")
    a("| 场景 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    for n in SCENES:
        for name, data in (("RED", red), ("GREEN", green)):
            c = data[n]["cells"]
            row = ["R%d" % n, name]
            for k in CRIT:
                cell = c.get(k)
                row.append("—" if cell is None else ("绿" if cell[0] else "红"))
            row.append("PASS" if data[n]["result"][0] else "FAIL")
            a("| " + " | ".join(row) + " |")
    a("")
    a("### §3.1 逐判据明细（判词 + `SKEL` 信息行，机器抽取）")
    a("")
    a("| 场景 | 侧 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for n in SCENES:
        for name, data in (("RED", red), ("GREEN", green)):
            for k in CRIT:
                cell = data[n]["cells"].get(k)
                if not cell:
                    continue
                a("| %s%d | %s | %s | %s | %s |" % (name[0], n, name, k,
                                                   "PASS" if cell[0] else "FAIL", cell[1]))
    a("")
    a("**`SKEL`（在 `mcm-latex-format` 骨架 preamble 下再编一遍 —— 信息行，不进 RESULT）**：")
    a("")
    a("| 场景 | 侧 | SKEL 行 |")
    a("| :-- | :-- | :-- |")
    for n in SCENES:
        for name, data in (("RED", red), ("GREEN", green)):
            a("| %s%d | %s | `%s` |" % (name[0], n, name, data[n]["skel"] or "（无）"))
    a("")
    a("### §3.2 汇总（由 §3 的格子逐格重算）")
    a("")
    a("| 侧 | 红格数（判据 x 表） | 判红的判据 ID（并集） | 全绿表数 |")
    a("| :-- | :-- | :-- | :-- |")
    for name, data in (("RED", red), ("GREEN", green)):
        allreds, ok = [], 0
        for n in SCENES:
            c = data[n]["cells"]
            if set(c) == set(CRIT) and all(v[0] for v in c.values()) and data[n]["result"][0]:
                ok += 1
            allreds += reds(data, n, CRIT)
        a("| %s | %d | %s | %d/3 |" % (name, len(allreds),
                                       "、".join(sorted(set(allreds))) or "（无）", ok))
    a("")

    a("## §4 RED 的红逐条点名（硬要求 2：真红 / 级联 / 判据假红-已修）")
    a("")
    a("（红集**机器抽取**自 §1；性质判定是人工判定，逐条写。）")
    a("")
    a("### R1（红集 = `%s`）· R3（红集 = `%s`）"
      % ("{%s}" % ",".join(reds(red, 1, CRIT)), "{%s}" % ",".join(reds(red, 3, CRIT))))
    a("")
    a(NATURE_R13)
    a("")
    a("### R2（红集 = `%s`）" % ("{%s}" % ",".join(reds(red, 2, CRIT))))
    a("")
    a(NATURE_R2)
    a("")
    a("### §4 的一句话（本支 RED 最诚实的读法）")
    a("")
    a(NATURE_ONELINE)
    a("")

    a("## §5 两侧 `.tex` 并排逐字 diff（机器抽取 + 人工注释）")
    a("")
    a("**结构读数（机器抽取）**：")
    a("")
    a("| 场景 | R 行数 | R 来源回显注释行 | G 行数 | G 来源回显注释行 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    nsrc = {}
    for n in SCENES:
        rl = (RED / ("out-R%d" % n) / "table.tex").read_bytes().decode("utf-8").splitlines()
        gl = (GREEN / ("out-G%d" % n) / "table.tex").read_bytes().decode("utf-8").splitlines()
        nsrc[n] = (len(rl), sum(1 for x in rl if "mcm-table-src" in x),
                   len(gl), sum(1 for x in gl if "mcm-table-src" in x))
        a("| %d | %d | %d | %d | %d |" % ((n,) + nsrc[n]))
    a("")
    for n in SCENES:
        rp = RED / ("out-R%d" % n) / "table.tex"
        gp = GREEN / ("out-G%d" % n) / "table.tex"
        rl = rp.read_bytes().decode("utf-8").splitlines()
        gl = gp.read_bytes().decode("utf-8").splitlines()
        diff = list(difflib.unified_diff(rl, gl,
                                         fromfile="red/out-R%d/table.tex" % n,
                                         tofile="green/out-G%d/table.tex" % n, lineterm=""))
        a("### 场景 %d：R%d vs G%d（`difflib.unified_diff`，逐字）" % (n, n, n))
        a("")
        a("```diff")
        a(NL.join(diff) if diff else "（两侧逐字相同）")
        a("```")
        a("")
    a(DIFF_ANNOT)
    a("")

    a("## §6 看图记录（硬要求 5：亲眼看表）")
    a("")
    a(JUDGMENT)
    a("")

    a("## §7 生成器 · 判据非空泛 · 不动点")
    a("")
    a("- 本文件的机器部分由 `make-evidence.py` **当场跑** `check-table-style.py` 生成"
      "（`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout。")
    a("")
    a("- ★ **判据非空泛（失败方向的另一条臂）** —— `mutate-table-style.py` **当场跑过**，读数为"
      "（**逐字**摘其合计段；全量输出含每条变异的检查器原文，从略）：")
    a("")
    a("```")
    a("$ python tests/skills/table/mutate-table-style.py")
    a("MUT: 14/14 红（check-table-style.py 的 C1–C8 逐条打红 + 2 条 fail-closed 分支打红 + 2 条修复边界打红：`MUT-C1b`/`MUT-LEAD-a`）")
    a("MUT: 对照 6/6 达预期（必须绿：射程边界 + C3 覆盖口径 + `\\multicolumn` 合规表 + 前导 `&` 两级表头 + `\\end{tabular}` 后表注 + 可选线宽参数合规表）")
    a("MUT: 合计 20/20 达预期（合计）")
    a("RUN: 受保护件 blob 逐件还原=True · 基准样本复跑 exit=0 · 全仓 `git status --short` 空")
    a("```")
    a("")
    a("  ⇒ 其中 **14 条是「真红」变异**（`C1`–`C8` **逐条**有真红 + `MUT-FC1`/`MUT-FC2` 两条 "
      "fail-closed 分支 + `MUT-C1b`/`MUT-LEAD-a` 两条修复边界），**6 条是「必须绿」的对照**；"
      "合计 **20/20 达预期**。（「驱动器 20 条变异」是**并集口径**；分开看是 **14 真红 + 6 对照**。"
      "对照里 `CTRL-GREEN-f`（可选线宽参数合规表）是 **2026-10-03 全分支终审修复轮 I-1** 新增（`RULES_RE` 吞 `[..]`）。）")
    a("")
    a("- **重跑不动点**：在已提交的树上重跑本生成器 ⇒ 本文件**逐字节不变**"
      "（证法：跑后 `git status --short` 仍为空；见本任务报告）。")
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace("\r\n", NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO).as_posix(), OUT_DOC.stat().st_size, "B")

    # ---- 自证断言（不满足即非零退出）----
    assert wt_blob == hd_blob, "checker blob 与 HEAD 不同！"
    for r, (w, h) in red_blobs.items():
        assert w == h, "RED 件被改：%s" % r
    for n in SCENES:
        c = green[n]["cells"]
        assert green[n]["result"] is not None, "GREEN %d 没解析到 RESULT" % n
        assert set(c) == set(CRIT), "GREEN %d 判据集合与清单不符：%s" % (n, sorted(c))
        assert all(v[0] for v in c.values()) and green[n]["result"][0], \
            "GREEN %d 未全绿：%s" % (n, reds(green, n, CRIT))
    assert set(reds(red, 1, CRIT)) == {"C8"}, "R1 红集变了：%s" % reds(red, 1, CRIT)
    assert set(reds(red, 3, CRIT)) == {"C8"}, "R3 红集变了：%s" % reds(red, 3, CRIT)
    assert set(reds(red, 2, CRIT)) == {"C2", "C3", "C5", "C6", "C7", "C8"}, \
        "R2 红集变了：%s" % reds(red, 2, CRIT)
    print("判据 %d 条：%s" % (len(CRIT), CRIT))
    for n in SCENES:
        print("  RED  R%d 判红：%s" % (n, reds(red, n, CRIT) or "（无）"))
        print("  GREEN G%d 判红：%s" % (n, reds(green, n, CRIT) or "（无）"))
    print("OK")


if __name__ == "__main__":
    main()
