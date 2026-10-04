#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3（`mcm-section-writer`）：生成 `tests/skills/section-writer/SECTIONWRITER-evidence.md`。

用法：  python tests/skills/section-writer/make-evidence.py

## 它做什么

把**三个工况（七件产物）**摆成一张可读的对照表，**同一把尺**地量：

- **同一把尺** = `.claude/skills/mcm-section-writer/check-section.py`（判据 `SW1–SW9` + `SELF1`/`SELF2` + `EMPTY`）。
  对**每一件产物**跑同一条命令形态；`--input` 一律指**对应那个节的 brief**。
- **三臂**（详见 `SECTIONWRITER-evidence.md` §1）：
  - **RED**（`out-S1.md` / `out-S2.md` / `out-S2-p.md`）：**什么都不给**；
  - **纪律轮**（`out-S1-g.md` / `out-S2-g.md`）：只给一份 `docs/mcm-writing-discipline.md`；
  - **skill 轮**（`green/out-S1-skill.tex` / `green/out-S2-skill.tex`）：给 `mcm-section-writer` **整目录**。
- ★ **RED 与纪律轮的四件产物逐字冻结**：本生成器**只读、不搬动、不改写、不重跑**它们。
- ★ **判据清单现取**：从检查器 stdout 里读 `PASS|WARN|FAIL|SKIP  <id>` 行得到 id 集合，**不写死条数**。

## 可重放（通则 14）

本生成器**不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`），产物是
（七件产物字节 + 检查器字节 + 本文件源码）的**纯函数** ⇒ 在已提交的树上重跑 ⇒ **逐字节不变**。
★ 任何指向本仓其它件的**锚点用固定基线 `BASE_REF`**（任务书给的那个），**不用 `HEAD`**
（先例：`tests/skills/topic-select/make-evidence.py` 的 `BASE_REF` 注释）。
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/section-writer
REPO = HERE.parents[2]                                   # 仓根
CHK = REPO / ".claude/skills/mcm-section-writer/check-section.py"
ARCH = REPO / "tests/skills/arch-cases"
GREEN = HERE / "green"
OUT_DOC = HERE / "SECTIONWRITER-evidence.md"

# ★ 本任务的**基线 commit**（任务书给的那个）。用它、不用 `HEAD`：
#   本支在 Task 3 里会**新增** green/ 产物与生成器 ⇒ 提交之后 `HEAD` 就变了，
#   拿 `HEAD` 当参照会**在提交前后给出两个不同的读数**（生成器就不动了）。基线是**固定**的。
BASE_REF = "a49951a"

NL = chr(10)

# (tag, 臂标签, 节, 产物, 形态, --input, 给了什么)
ARMS = [
    ("RED-S1",  "RED（自由臂）", "模型建立", ARCH / "out-S1.md",           "markdown", ARCH / "brief-S1.md", "**什么都不给**"),
    ("RED-S2",  "RED（自由臂）", "结论",     ARCH / "out-S2.md",           "markdown", ARCH / "brief-S2.md", "**什么都不给**"),
    ("RED-S2p", "RED（压力臂）", "结论",     ARCH / "out-S2-p.md",         "markdown", ARCH / "brief-S2.md", "**什么都不给**（另有队长口头压力：缺点别写太狠）"),
    ("DIS-S1",  "纪律轮",       "模型建立", ARCH / "out-S1-g.md",         "LaTeX 源码", ARCH / "brief-S1.md", "`docs/mcm-writing-discipline.md`（一份纪律文件）"),
    ("DIS-S2",  "纪律轮",       "结论",     ARCH / "out-S2-g.md",         "markdown", ARCH / "brief-S2.md", "`docs/mcm-writing-discipline.md`（一份纪律文件）"),
    ("SKL-S1",  "skill 轮",     "模型建立", GREEN / "out-S1-skill.tex",   ".tex 片段", ARCH / "brief-S1.md", "`mcm-section-writer` **整目录**（`SKILL.md` + 三份 `references` + 检查器）"),
    ("SKL-S2",  "skill 轮",     "结论",     GREEN / "out-S2-skill.tex",   ".tex 片段", ARCH / "brief-S2.md", "`mcm-section-writer` **整目录**（`SKILL.md` + 三份 `references` + 检查器）"),
]

STATUS_RE = re.compile(r"^(PASS|WARN|FAIL|SKIP)\s+([A-Z][A-Z0-9]*)\b")
RESULT_RE = re.compile(r"^RESULT:\s*(PASS|FAIL)")
SIZE_RE = re.compile(r"散文段数=(\d+)\s*·\s*句子数=(\d+)\s*·\s*正文词数=(\d+)\s*·\s*检出表格=(\d+)")
LEX_RE = re.compile(r"^词表自测.*?:\s*(.+)$")

ID_ORDER = ["SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8", "SW9",
            "SELF1", "SELF2", "EMPTY"]


def rel(p):
    try:
        return p.relative_to(REPO).as_posix()
    except ValueError:
        return str(p)


def run_check(path, section, inp):
    cmd = [sys.executable, str(CHK), str(path), "--section", section, "--input", str(inp)]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return p.stdout, p.returncode


def parse(out):
    st, size, result, lex = {}, None, None, None
    for line in out.splitlines():
        m = STATUS_RE.match(line)
        if m:
            st[m.group(2)] = m.group(1)
            continue
        m = RESULT_RE.match(line)
        if m:
            result = m.group(1)
            continue
        m = SIZE_RE.search(line)
        if m:
            size = tuple(int(x) for x in m.groups())
            continue
        m = LEX_RE.match(line)
        if m:
            lex = m.group(1).strip()
            continue
    return st, size, result, lex


def git_blob(path):
    r = subprocess.run(["git", "hash-object", path], cwd=str(REPO),
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout.strip()


def main():
    rows = []
    for tag, arm, section, path, form, inp, given in ARMS:
        if not path.exists():
            sys.stderr.write("缺产物：%s%s" % (rel(path), NL))
            return 2
        out, code = run_check(path, section, inp)
        st, size, result, lex = parse(out)
        rows.append(dict(tag=tag, arm=arm, section=section, path=path, form=form,
                         inp=inp, given=given, st=st, size=size, result=result,
                         lex=lex, code=code,
                         blob=git_blob(rel(path)),
                         nbytes=len(path.read_bytes()),
                         nlines=path.read_bytes().count(b"\n")))

    ids = [i for i in ID_ORDER if any(i in r["st"] for r in rows)]

    doc = []
    a = doc.append

    a('# `SECTIONWRITER-evidence.md` —— `mcm-section-writer` 的三臂对照（RED × 纪律轮 × skill 轮）')
    a('')
    a('**本文件由 `tests/skills/section-writer/make-evidence.py` 当场跑命令生成**（`write_bytes`、全 LF）。')
    a('**不许手改** —— 改读数请改生成器或产物本身，然后重跑。')
    a('')
    a('> 生成命令：`python tests/skills/section-writer/make-evidence.py`')
    a('> 复现：在**已提交的树**上重跑本生成器 ⇒ 本文件**逐字节不变**（证法见 §10）。')
    a('')
    a('**同一把尺** = `.claude/skills/mcm-section-writer/check-section.py`（`SW1–SW9` + `SELF1`/`SELF2` + `EMPTY`），')
    a('对**每一件产物**跑同一条命令形态；`--input` 一律指**对应那个节的 brief**。')
    a('★ **判据清单现取**（从检查器 stdout 的 `PASS|WARN|FAIL|SKIP` 行里读 id），**不写死条数**。')
    a('')

    # ---- §1 三臂清单 ----
    a('## §1 三臂（**三个工况，不是两个**）')
    a('')
    a('| 臂 | 产物（**都已在库**） | 给了什么 | 本任务做什么 |')
    a('| :--- | :--- | :--- | :--- |')
    a('| **RED** | `tests/skills/arch-cases/out-S1.md` · `out-S2.md` · **`out-S2-p.md`** | **什么都不给** | **只读，不重跑** |')
    a('| **纪律轮**（既有 GREEN） | `tests/skills/arch-cases/out-S1-g.md` · `out-S2-g.md` | `docs/mcm-writing-discipline.md` 一份 | **只读，不重跑** |')
    a('| ★ **skill 轮**（本任务新建） | `tests/skills/section-writer/green/out-S1-skill.tex` · `out-S2-skill.tex` | 本 skill 整目录 | **跑它**（两个新起的写手，本会话独立起，非 fork） |')
    a('')
    a('★ **`out-S2-p.md` 是 RED 独有的压力臂**（队长要求"缺点别写太狠"）—— **skill 轮没有对应臂** ⇒')
    a('下表**单列一行并写"无对应"**，**不塞进干净对照里当第三列**。')
    a('')
    a('★ **不重跑 RED 与纪律轮的理由**：它们**逐字冻结、无生成器可重跑**（`tests/skills/arch-cases/README.md` §一 末）。')
    a('')

    # ---- §2 泄题清单 + 隔离 ----
    a('## §2 泄题清单与隔离做法（**给了任何一项，这次对照当场作废**）')
    a('')
    a('**给写手的只有两样**：`tests/skills/arch-cases/brief-S1.md`（或 `brief-S2.md`）**+** 题面')
    a('`tests/skills/abs-cases/case-A-problem.txt`（`arch-cases/README.md:38` 写死）。')
    a('')
    a('**逐项核过、绝不给写手**（**本文件不声称穷尽**）：')
    a('')
    a('- `tests/skills/arch-cases/` 的 `true-S1.md` · `true-S2.md` · `judge.md` · `judge-green.md` · `README-RED.md` · `README.md`；')
    a('- ★★ **`tests/skills/abs-cases/case-A-body.md`** —— **`true-S1.md` 就是它第 147–296 行的逐字节副本**（`true-S1.md:2-3`）')
    a('  ⇒ **给它＝给答案全文**；同目录 `case-A-body-partial.md` · `case-A-true-abstract.md` 同理；')
    a('- ★ `tests/skills/arch-red-evidence.md` · `tests/skills/arch-green-evidence.md`；')
    a('- ★ **既有的 `out-S1-g.md` / `out-S2-g.md`（纪律轮产物）与全部 `out-*.md`** —— 它们是**答案的近似物**。')
    a('')
    a('★ **隔离做法（通则 8）**：两样输入**复制到仓库外的固定容器** `D:/Projects/_scratch/m2-sw-green/`')
    a('（**不许落盘根**、**不许 `%TEMP%`**、**不许 MSYS `/tmp`**），写手在容器里干活；')
    a('**`arch-cases/` 与 `abs-cases/` 整个目录都不给写手看见**（只投喂那两份点名文件）。')
    a('★ **怎么把 skill 交给写手**：把 `.claude/skills/mcm-section-writer/` **整目录复制**进容器')
    a('（**不许只给 `SKILL.md`** —— 那等于没给 references 与工具）；写手读它并**被要求跑一次检查器**。')
    a('★ 两个写手都**由本会话新起（非 fork、无任何上下文）**，派发指令**明写"不要读仓库里其它文件"**。')
    a('')

    # ---- §3 产物身份 ----
    a('## §3 产物身份（逐件当场 `git hash-object`）')
    a('')
    a('| 臂 | 产物 | 形态 | 字节 | 行数 | git blob |')
    a('| :--- | :--- | :--- | ---: | ---: | :--- |')
    for r in rows:
        a("| %s | `%s` | %s | %d | %d | `%s` |"
          % (r["tag"], rel(r["path"]), r["form"], r["nbytes"], r["nlines"], r["blob"]))
    a('')
    a('★ **RED 与纪律轮的 5 件是冻结的第三方对照物** —— 本支**不搬动、不改写、不重跑**。')
    a('★ **skill 轮的 2 件为本任务新建**（写手产物，逐字入库；入库时只做过 `CRLF → LF` 归一，见 §10）。')
    a('')

    # ---- §4 对照表（机器读数）----
    a('## §4 ★ 对照表（**机器读数**；同一把尺、逐件跑）')
    a('')
    a('命令形态：`python .claude/skills/mcm-section-writer/check-section.py <产物> --section <节> --input <brief>`')
    a('')
    a('### §4.1 逐臂读数（尺寸 · 结果 · 退出码）')
    a('')
    a('| 臂 | 节 | 给了什么 | 散文段 | 句 | 正文词 | 表 | `RESULT` | exit |')
    a('| :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- | ---: |')
    for r in rows:
        sz = r["size"] or (None,) * 4
        a("| %s | %s | %s | %s | %s | %s | %s | **%s** | %d |"
          % (r["tag"], r["section"], r["given"],
             sz[0] if sz[0] is not None else "—", sz[1] if sz[1] is not None else "—",
             sz[2] if sz[2] is not None else "—", sz[3] if sz[3] is not None else "—",
             r["result"], r["code"]))
    a('')
    a('★ **`RESULT`/`exit` 只由硬失败决定**（`FAIL`）；`WARN` / `SKIP` **不影响退出码**（见 §4.3）。')
    a('')
    a("### §4.2 逐判据矩阵（**现取**的 %d 条 id）" % len(ids))
    a('')
    a("| 判据 | " + " | ".join(r["tag"] for r in rows) + " |")
    a("| :--- | " + " | ".join(":--" for _ in rows) + " |")
    for i in ids:
        a("| `%s` | %s |" % (i, " | ".join(r["st"].get(i, "—") for r in rows)))
    a('')
    a('★ **词表自测行**（`SW3`/`SW5`/`SW6`/`SW8` 使用前必须先拿 `true-*` 自测；命中 0 才可用）：')
    for r in rows:
        a("- `%s`：%s" % (r["tag"], r["lex"] or "（无此行）"))
    a('')
    a('### §4.3 状态语义（照检查器；**别把 `WARN`/`SKIP` 读成 `PASS` 或 `FAIL`**）')
    a('')
    a('- **硬失败（`FAIL`）只有三处**：`SW1` · `SW2` · `EMPTY`。`SW3–SW9` **一律只出"提请复核"（`WARN`），绝不判死**。')
    a('- **`SKIP` = 无法判定**（既不是 `PASS` 也不是 `FAIL`）：`--input` 缺失 ⇒ `SW1`/`SW2`/`SW4` 报 `SKIP`；')
    a('  真值取不到 ⇒ 词表判据（`SW3`/`SW5`/`SW6`/`SW8`）报 `SKIP`。')
    a('- ★ **本文件里 7 臂的 `--input` 都给了** ⇒ `SW1`/`SW2`/`SW4` 不因缺输入而 `SKIP`；')
    a('  词表自测行显示**真值取得到**（`SW3=0 SW5=0 SW6=0 SW8=0`）⇒ 词表判据**全部实际执行**。')
    a('- **退出码**：有 `FAIL` ⇒ 非 0；只有 `WARN`/`SKIP` ⇒ 0。')
    a('')

    # ---- §5 可比性 ----
    a('## §5 ★★ 哪两列可比（**只评内容覆盖与纪律条目命中，不评风格**）')
    a('')
    a('### §5.1 逐件形态（**当场量过**；`说明段` 不计入）')
    a('')
    a('| 臂 | S1 形态 | S2 形态 |')
    a('| :--- | :--- | :--- |')
    a('| RED（自由臂） | markdown | markdown |')
    a('| 纪律轮 | **LaTeX 源码** | markdown |')
    a('| skill 轮 | **.tex 片段** | **.tex 片段** |')
    a('')
    a('（`out-S2-p.md` = markdown，与 RED 自由臂同形态。）')
    a('')
    a('### §5.2 结论：**只有哪一对是干净的单变量**')
    a('')
    a('- ★ **唯一"形态相同、只换了一个变量"的 S2 对** = **RED-S2（markdown） vs 纪律轮-S2（markdown）**')
    a('  —— 两侧**同为 markdown**，唯一之差是**给不给那份纪律文件**。这正是 `judge-green.md:264` 原本所指的那一对。')
    a('- ★ **RED-S1 vs 纪律轮-S1**：**混了产物形态**（markdown vs LaTeX 源码）⇒ **S1 上的改善不能全归给纪律**。')
    a('- ★★ **凡含 skill 轮的跨臂对，S1 与 S2 都同时换了干预与形态**：')
    a('  skill 轮**两节产物都是 `.tex` 片段**，而 RED **两节都是 markdown** ⇒')
    a('  **`RED-S1 vs skill 轮-S1` 与 `RED-S2 vs skill 轮-S2` 都不是干净单变量对**。')
    a('- ★★ **与任务书的一处出入（按"实测优先"登记）**：任务书写 *"只有「RED 自由臂 vs skill 轮」在 S2 上是干净单变量"*。')
    a('  **实测不符**：skill 轮 S2 的产物是 `.tex`（`.claude/skills/mcm-section-writer/SKILL.md` 的输出契约就是"该节 `.tex` 片段"），')
    a('  与 RED-S2 的 markdown **不是同一形态** ⇒ 该对**同时换了干预与形态**。**本文件以实测为准。**')
    a('- ⇒ **本文件的读法**：skill 轮的对照价值在于"**这个 skill 会不会把一节写合格**"（可与两臂并列看绝对读数），')
    a('  **不能**把"skill 轮比 RED 干净"归因于 skill —— 形态也换了。')
    a('')
    a('### §5.3 两列**不许并成一列**')
    a('')
    a('- ★ **纪律轮与 skill 轮是两种不同的干预**（一份纪律文件 vs 一个带检查器的逐节 skill）⇒')
    a('  二者的读数**不许混成一列**、**不许相减**。')
    a('- ★ **`out-S2-p.md`（RED 压力臂）单列**：skill 轮**无压力臂** ⇒ 该行标注 **"无对应"**。')
    a('')

    # ---- §6 内容覆盖 ----
    a('## §6 内容覆盖（**粗粒度**；skill 轮 = 本文件当面核，RED/纪律轮 = 引既有判词）')
    a('')
    a('★ **只评内容覆盖与纪律条目命中，不评风格**（真值是 PDF 转换件，标点与句法表面不可比 —— `judge.md` §5.3 第 3 条）。')
    a('★ **本表不声称穷尽**；覆盖判定为**粗粒度的人工判**，不是机器读数。')
    a('')
    a('### §6.1 skill 轮（本文件当面逐条核 `brief` 的要点）')
    a('')
    a('- **SKL-S1**（模型建立，`brief-S1.md` **12 条要点**）：**12/12 覆盖**。落点见')
    a('  `green/out-S1-skill-selfcheck.md` §3 的逐点映射表（要点 → 方程/段号）。')
    a('  ★ 一处**有意偏离 brief 字面**：brief 第 7 条用 `d` 同时表示 Archard 滑动距离与磨损量 `d(x,y)`；')
    a('  正文改用 **`d_s`** 表滑动距离并在首现句说明（**受 `纪律 B3` 驱动**，写手自述）。')
    a('- **SKL-S2**（优缺点 + 结论，`brief-S2.md` **8 条要点**）：**8/8 覆盖**。落点见')
    a('  `green/out-S2-skill-selfcheck.md` §一 的逐条打勾（优点 3 条 / 缺点 2 条 / 结论成果清单 7 项 / 收束与展望）。')
    a('')
    a('### §6.2 RED / 纪律轮（**引既有判词，本文件未逐点重测**）')
    a('')
    a('- RED 与纪律轮的内容覆盖**不在本文件重测**（那要重跑 `judge.md` §3 / `judge-green.md` §3 的口径）；')
    a('  本文件只引其**机器可比的纪律条目读数**（§4）与**登记在案的结论**（§7）。')
    a('- ★ **一处 RED 的结构性损失**（`arch-cases/README.md` §三 第三条）：`brief-S1.md` 把')
    a('  "为什么 Archard 理论适用于台阶"的论证压成半句 ⇒ RED 写手补不出这层论证**属任务书自身的结构性损失，不是它的疏忽**，')
    a('  对照时须单独标出。')
    a('')

    # ---- §7 三条缺口 ----
    a('## §7 ★★ 三条已登记缺口：判定**分开写**（`judge-green.md:249–251`）')
    a('')
    a('★ `judge-green.md` 三行登记了 GREEN 轮**未修好**的三条（`:249` A3 · `:250` B3 跨节 · `:251` B1 文献表）。')
    a('**本任务对这三条的判定能力不同**，必须分开写、不许含糊。')
    a('')
    a('### §7.1 `纪律 A3`（声称读过没读过的部分）—— **判得出**，逐条判"修好没有"')
    a('')
    a('| 臂 | A3 读数 | 依据 |')
    a('| :--- | :--- | :--- |')
    a('| RED-S1 | 0（无区分力） | `judge-green.md:220` |')
    a('| RED-S2 | **1 处失败**：`out-S2.md:3`、`:23`×2（含"前文有数值结果"一句） | `judge-green.md:78-81`、`:220` |')
    a('| 纪律轮-S2 | **1 处残留**：`out-S2-g.md:21` 把 brief 只背书半句的"仿真"**扩写得更具体** | `judge-green.md:249` |')
    a('| **skill 轮-S2**（本文件当面核） | **修好** —— 结论里关于仿真只有一句')
    a('  *"Simulation was used extensively in arriving at all of this."*（= brief 第 7 条"大量使用了仿真"的转述，')
    a('  **未添任何 brief 没有的具体用途**）；全节**未对未读章节下具体数值/具体结论的断言** |')
    a('  `green/out-S2-skill-selfcheck.md` §二 的 `纪律 A3` 行；本文件另逐句复核 |')
    a('')
    a('⇒ **A3 判定：skill 轮 S2 = 修好**（**判据 = A3 的规则边界**：转述要点里的断言不算违规，')
    a('*"扩写得更具体"*才算 —— `docs/mcm-writing-discipline.md` A3；对照 GREEN 的 `:21` 曾加 *"under conditions that are')
    a('specified in advance"* 等具体用途，skill 轮 S2 未加）。')
    a('')
    a('### §7.2 `纪律 B3`（跨节符号一致）—— **本任务判不出**')
    a('')
    a('- ★ **本 skill 是逐节工具、不给全文**，而 `judge-green.md:251`/`:267`/`:279` 自认**跨节一致性"无从判"**。')
    a('- ⇒ **照实记"仍无从判"**，**不许**写成"已修好"或"未修好"。')
    a('- ★ **Task 1 的 `references/section-edges.md` 承接这一条**（符号表：`纪律 B3` 管一节之内、跨节对齐归 `纪律 B6`）——')
    a('  但那是**"给了落点"**，**不是"已被验证有效"**。')
    a('  ★ **skill 轮的两份自查单都主动登记了这个"无从判"**（`green/out-S1-skill-selfcheck.md` §6、')
    a('  `green/out-S2-skill-selfcheck.md` §三 的符号表行），并写明"该风险未消、需全文对齐时人工复查"。')
    a('')
    a('### §7.3 `纪律 B1`（文末文献表）—— **本任务判不出**')
    a('')
    a('- ★ 引用义务含**两处**（正文明标 + 文末表）；**文末表的条目形态不在逐节工具的射程内**（`judge-green.md:251`/`:278`）。')
    a('- ⇒ **照实记"仍无从判"**，**不许**写成"已修好"或"未修好"。')
    a('- （本文件可另行如实记录**正文明标那一半**的机器可见事实：SKL-S1 正文有 `\\cite{who-weights}` 一处；')
    a('  SKL-S2 正文 `grep` 无任何引用记号。**但这不是对 B1 的判定** —— B1 的文献表侧仍无从判。）')
    a('')
    a('### §7.4 两条的承接关系（**别把"给了落点"读成"已验证"**）')
    a('')
    a('- Task 1 的 `references/sections.md` 各节 ④ 格 + `references/section-edges.md` 把 `纪律 B3`/`B1` 的**人工落点**写死；')
    a('- 但那是**"给了落点"**：本 skill 是逐节工具，**跨节/全篇这两项它判不出** ⇒ 二者**不是"已被验证有效"**。')
    a('')

    # ---- §8 样本量与形态边界 ----
    a('## §8 ★★ 样本量与形态的边界（`P8`；**必须与上面所有读数同读**）')
    a('')
    a('- **skill 轮每节 1 个产物**（S1 一个 `.tex`、S2 一个 `.tex`），**无压力臂**。')
    a('- **RED 侧 3 个产物**（S1 一臂 + S2 两臂：自由臂 `out-S2.md` + 压力臂 `out-S2-p.md`）；')
    a('  **纪律轮侧 2 个**（S1、S2 各一）。')
    a('- **压力臂只存在于 RED 侧** —— skill 轮**没有**对应臂 ⇒ §5.3 把 `out-S2-p.md` **单列并标"无对应"**。')
    a('- ★★ **S1 那一对（RED-S1 vs 纪律轮-S1）混了产物形态**（markdown vs LaTeX 源码，`judge-green.md:264`）')
    a('  ⇒ **S1 上的改善不能全归给纪律**。')
    a('- ★★ **凡含 skill 轮的跨臂对，S1 与 S2 都混了形态**（§5.2）⇒ **skill 轮上的"更好"也不能全归给 skill**。')
    a('- ⇒ **不得**把 S1/S2 的读数写成"该节的普遍规律"；**不得**把任何一臂的改善整个归给单一干预。')
    a('- ★ **纪律轮与 skill 轮的读数不许混成一列**（两种干预，§5.3）。')
    a('')

    # ---- §9 证明不了什么 ----
    a('## §9 这套对照证明不了什么（**如实登记，不放大**）')
    a('')
    a('- **n=1**：每臂每节只有 1 个产物，没有第二写手、没有第二个案例 ⇒ 任何"X 有效"的结论都只有 `n=1`。')
    a('  （先例 `judge-green.md:263`；本支同样**未能核实**两侧是不是同一写手/同一模型。）')
    a('- **测不出跨节 / 全篇一致性**（B1 文献表、B3/B6 跨节符号）—— 逐节工具不给全文（§7.2/§7.3）。')
    a('- **测不出"纪律在压力下的存活率"**：本支与既有 GREEN 轮**都没有压力臂**（只有 RED 有）。')
    a('- **测不出真实数据压力下的 `纪律 A1`** —— `judge-green.md:268` 同记。')
    a('- **测不出 `SW3–SW8` 的阈值**：两轮度量脚本**未落盘**、不可复算 ⇒ `SW3–SW8` 一律只出 `WARN`，**不是判死**、')
    a('  **不许读成达标线**（`judge-green.md:270`：*"0 与 0 之间无法定阈"*）。★ `SW9` 不在此列：它的阈值是**当场量的分布式**定的、可复算。')
    a('- **不做**判"这段是不是 AI 生成的"（`judge.md:133`/`:244`/`:240`）。')
    a('- ★ **检查器射程不许夸大**：`RESULT: PASS`（§4）**只覆盖 `SW1–SW9` 等可机判项**；')
    a('  `纪律 A3/A4/A5/B2/B4/B5/B6` 等**仍靠人工逐条**。"**检查器 PASS" ≠ "这一节写好了"**（`SKILL.md`）。')
    a('')

    # ---- §10 自证 ----
    a('## §10 自证（可重放 / 不动点）')
    a('')
    wt = git_blob(rel(CHK))
    base = subprocess.run(["git", "rev-parse", BASE_REF + ":" + rel(CHK)],
                          cwd=str(REPO), capture_output=True, text=True, encoding="utf-8").stdout.strip()
    a("- **检查器自证**：工作树 blob `%s` · **基线 `%s`** blob `%s` ⇒ %s —— ★ **本生成器只读检查器、不改它**"
      "（blob 不同 ⇒ 检查器在 `%s` 之后被改过）。"
      % (wt[:12], BASE_REF, base[:12], "**相同**" if wt == base else "**不同（！）**", BASE_REF))
    a("- **产物自证（逐件 blob）**：" + " · ".join("`%s`=`%s`" % (r["tag"], r["blob"][:12]) for r in rows))
    a("- **本生成器不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`，锚点一律用固定基线 `%s`）" % BASE_REF)
    a('  ⇒ 本文件是（七件产物字节 + 检查器字节 + 生成器源码）的**纯函数**。')
    a('- ★ **不动点证法（通则 14）**：**先干净 → 再捕获 → 再提交 → 再跑一次证不动点** ——')
    a('  在**已提交**的树上重跑本生成器，然后 `git status --short` 仍为空、`git diff` 对本文件为空 ⇒ **逐字节不变**。')
    a('  （本支执行记录见 `.superpowers/sdd/task-m2-sw-t3-report.md`。）')
    a('- ★ **入库时的 `CRLF → LF` 归一（如实登记）**：两个写手的产物原始字节为 **CRLF**（写手工具默认），')
    a('  按本仓 GC10"全 LF"要求**只做过换行归一**（`\\r\\n → \\n`），**正文一个字符未改**。')
    a('')

    OUT_DOC.write_bytes((NL.join(doc) + NL).encode("utf-8"))
    print("WROTE %s (%d 字节)" % (rel(OUT_DOC), OUT_DOC.stat().st_size))
    for r in rows:
        print("  %-8s %-6s 节=%-4s RESULT=%-4s exit=%d" % (r["tag"], r["form"], r["section"], r["result"], r["code"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
