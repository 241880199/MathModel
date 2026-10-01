#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 2：生成 tests/skills/figure-choose/red/red-evidence.md（机械层逐字证据）。

写入用 write_bytes。文中所有数字都来自本次当场跑过的命令，命令与输出逐字附在文内。

本脚本**与它生成的证据同目录入库**（旧版放在 gitignored 的 `.superpowers/sdd/`，
等于"证据在册、造它的脚本随时会丢"）。
`<<CAPTIONS>>` 处的图注**在生成时从 `out-R{n}/caption.txt` 的字节直接读入**，
所以"逐字"这个标签**由构造方式保证**，不是手抄出来的（旧版这里被"..."截断却标着"逐字"）。
"""
import pathlib

RED = pathlib.Path(__file__).resolve().parent

DOC = """\
==============================================================================
tests/skills/figure-choose/red/ —— Task 2 RED 基线证据（逐字）
==============================================================================

【范围】3 个场景（R1 构成数据 / R2 多变量对比 / R3 交付形态）× 2 层判据：
        机械层 = Task 1 的 `check-figure-style.py`（**一字不改**，直接调用）；
        判断层 = 独立判者（判词逐字见 `judge.md`）。
【机器】Windows 11 / Python 3.11.9 / Pillow 12.3.0 / PyMuPDF 1.27.2 / matplotlib 3.10.7
【起始 commit】`5ace7b4`（分支 `feat/m6-corpus-pipeline`）
【本轮修复起点】HEAD `5edbd20`；本文件随修复同步更新（**本轮见 §11**，上一轮见 §10）

【写手与判者的身份】六个写手 + 一位判者**全部是 `general-purpose` 全新 subagent，未用 `fork`**。
  这一条**不是自报**：`fork` 会继承主 agent 上下文，其 transcript 的**首条 user 消息**会是
  长篇上下文；而实测六个写手 + 判者的首条 user 消息就是**那一条提示词本身**
  （212 / 309 / 1194 字符，逐字见 `writer-self-reports.md`）。

【本文件怎么来的】由同目录的 `make-evidence.py` 用 `write_bytes` 生成（LF）。
  生成器与它生成的证据**同在受版本控制的目录里** —— 旧版生成器放在 gitignored 的
  `.superpowers/sdd/`，等于"证据在册、造它的脚本随时会丢"。

【对捕获输出的唯一加工】
1) 命令一律以**仓库相对路径**写出（cwd = 仓根）；
2) 系统临时目录的绝对路径剥成 `<TMP>/`（本仓规定不写绝对路径）；
3) 其余**逐字未改**。每个块尾的 `[exit=..]` 是该命令的真实退出码。
   **凡有节略一律当场标明**（旧版 §2 的图注块标着"逐字"其实被"..."截断，第一轮修复时已补全）。

【分母口径】同 Task 1：`--textwidth-in` 一律传 **6.31**
（= 逐篇正文行宽 p90 的全局中位，见 `tests/figures-recon/b-stats.txt`
`col_w_in: n=43 ... median=6.310`）。检查器**不预设**口径。

==============================================================================
§0 头号发现：RED 隔离**不是**"结构性成立"的 —— 第一轮整轮作废，第二轮显式加隔离
==============================================================================

任务书断言：「此刻 `.claude/skills/mcm-figure-choose/` 还不存在，所以"读不到规范"是
**结构性成立**的」。**该断言经实测为假**，且不是理论担忧 —— 第一轮三个写手**全部**自报
读了规范来源，产物按规范设计，RED 基线被污染。

**第一轮（`red/out-R*` 的首版）三个写手**（`general-purpose` 全新 agent、未用 `fork`）
**全部自报读了仓内规范**。下面是三人的**原句**（逐字节，从各自的 SubagentHandback 里摘出；
**完整原文**见受版本控制的 `writer-self-reports.md`，该文件同时存了两轮的派发提示词）：

- **R1**：「**This is not a clean naive RED product.** While orienting in the repo I read
  `tests/skills/figure-choose/check-figure-style.py`, `fixtures/expected.tsv`, the recon files
  under `tests/figures-recon/`, and the `.superpowers/sdd/task-m3-t3-brief.md` house-style table
  (H1–H13: width ≤1.2× column, no pie charts, ≤4 colours, ≤12-word captions, aspect 2–3, ≥7 pt).
  **I deliberately conformed to all of them.**」
- **R2**（节选：原句从 "before drawing anything" 起，前文在讲它拿到了整个仓的通行权）：
  「before drawing anything I read the M3 design spec
  (`docs/superpowers/specs/2026-09-27-m3-figure-choose-design.md`), the checker source
  (`tests/skills/figure-choose/check-figure-style.py`) and the fixtures. **So this artifact is
  NOT a clean no-skill baseline**」
- **R3**：「Having seen the mechanical criteria, I designed directly against them — the 6.00 in
  page width, the ≤4-colour palette, the 11-word caption and the ASCII `Figure 1:` were all
  **chosen knowing the thresholds**. So this artifact is **not** a skill-free/naive RED baseline」

**规范在这份仓里至少有 6 个可读落点**（都不是 `.claude/skills/`）：

| # | 落点 | 泄的是什么 |
| :- | :--- | :--- |
| 1 | `tests/skills/figure-choose/check-figure-style.py` | 判据本体与全部阈值常量 |
| 2 | `tests/skills/figure-choose/fixtures/expected.tsv` · `captions.tsv` | 逐条 fixture 的期望红绿 + 合规图注样板 |
| 3 | `tests/skills/figure-choose/figure-style-baseline.txt` | 判据来历与实测读数 |
| 4 | `tests/figures-recon/**`（a/b/c/d 系列） | 规范所依据的**实测分布**（`col_w_in median=6.310`、配色数、图注词数…） |
| 5 | `docs/superpowers/specs/2026-09-27-m3-figure-choose-design.md` | 设计定稿 |
| 6 | `.superpowers/sdd/task-m3-t{2,3}-brief.md` | 本任务书自己写了**期望的失败形态**；t3 任务书含 H1-H13 规范表 |

⇒ **结论**：Task 6 的 GREEN/RED 对照必须保证 RED 侧是"没读过上面任何一处"的产物。
本任务的处置：**把三份 brief 原样（字节相同）搬到仓外临时目录，写手只拿到
"仓外 brief 路径 + 仓外输出目录"，并显式限定"只读这一份 brief"**，产物回收入库。
第二轮三个写手**各自独立确认**只读了那一份 brief（逐字节原句，全文见 `writer-self-reports.md`；
下面都是**节选**，节选处都是原句的连续片段）：

- R1：「The task said to work only from that brief and to read/write no other file, so I did not
  invoke the dataviz skill (invoking it reads skill files)」
- R2：「Only the brief was read; nothing else in the repo was touched」
- R3：「worked only from brief-R3.md, no other file read or written」

⚠️ **强度必须说清（不许下游读过头）**："写手只读了那一份 brief"这件事
**只有自报，没有沙箱可证** —— 没有文件系统审计、没有 syscall 记录、没有哈希链。
能做到的只有两件：① 把**原文**存进受版本控制的地方（`writer-self-reports.md`，逐字节）；
② 证明"没给它们继承的上下文"，即**未用 `fork`**（实测：六个写手 + 判者的 transcript
**首条 user 消息就是那一条提示词本身**，212 / 309 / 1194 字符 —— `fork` 的首条消息会是
继承来的长篇上下文）。**"自报一致"不等于"已证"**。

⚠️ **这仍是一处对任务书的偏离**：任务书要求写手提示词"只准包含 ① brief 路径 ② 输出目录"。
本实施**多了一句**"Work only from that brief - do not read or write any other file."
理由与代价见 §9-A；**两轮提示词的逐字原文见 §0.1**。**审计请重点看 §0.1 与 §0.2。**

==============================================================================
§0.1 逐字提示词（两轮写手 + 判者）—— 任务书的验收项
==============================================================================

出处：每个 agent 的 transcript 里**首条 user 消息**。抢救件（含完整报告）在
`writer-self-reports.md`；本节把它按"提示词"抽出，**不软换行**（原文就是下面这些行）。

【对原文的唯一加工】写手自己写了**绝对路径**，本仓规定不写，故在抢救件里掩码：
仓外临时目录 → `<TMP>/m3-t2-red`（**共 15 处**，`rescue-transcripts.py` 逐处计数后写在文件头）。
因此第 2 轮提示词的**原文长度是 309 字符**，掩码后 247；本节的 `<TMP>` 就是那个掩码。

**第 1 轮（作废轮）写手提示词** —— 与任务书模板一致，只含 ① brief 路径 ② 输出目录，
仓库相对路径。**三条全部列出**（每条 **212 字符**，**单行**）：

```text
Read the brief at tests/skills/figure-choose/red/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R1/.
Read the brief at tests/skills/figure-choose/red/brief-R2.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R2/.
Read the brief at tests/skills/figure-choose/red/brief-R3.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R3/.
```

**第 2 轮（有效轮）写手提示词** —— **三条全部列出，每条单行、无软换行**；
`<TMP>` 是对系统临时目录前缀的**唯一**加工（本仓规定不写绝对路径），其余逐字节未改。
每条 **309 字符**：

```text
Read the brief at <TMP>/m3-t2-red/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R1/. Work only from that brief - do not read or write any other file.
Read the brief at <TMP>/m3-t2-red/brief-R2.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R2/. Work only from that brief - do not read or write any other file.
Read the brief at <TMP>/m3-t2-red/brief-R3.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R3/. Work only from that brief - do not read or write any other file.
```

与第 1 轮的**差别只有两处**：路径从仓内搬到仓外临时目录；末尾多一句隔离限定。
**这句不泄露任何判据**（未提 skill、规范、图宽、配色、饼图、判据、期望答案），
但它**暗示了"存在别的文件"** —— 这正是 §9-A 登记的偏离。

**判者提示词（第 2 轮，一位判者判三份）** —— **1194 字符**，逐字节（原文自带换行，未改）：

```text
You are reviewing three figures, each produced by a different author from a separate brief. Read the brief and the artifacts for each:

- tests/skills/figure-choose/red/brief-R1.md  ->  artifacts in tests/skills/figure-choose/red/out-R1/
- tests/skills/figure-choose/red/brief-R2.md  ->  artifacts in tests/skills/figure-choose/red/out-R2/
- tests/skills/figure-choose/red/brief-R3.md  ->  artifacts in tests/skills/figure-choose/red/out-R3/

Each artifact directory contains the generating script (make_figure.py), the exported figure (figure.pdf and figure.png) and the caption text (caption.txt). View the figure images.

For each of the three, in turn, answer these three questions:
1. Is the chart type appropriate for the question asked in the brief? Answer exactly one of: correct / partly correct / wrong.
2. Why? Give your reasoning.
3. Does it violate the rule "composition data must not be drawn as a pie chart"? Answer yes or no.

Read only the three briefs and the three artifact directories. Do not read .claude/, docs/, tests/skills/figure-choose/*.py, or any other repository file.

Write your answers for all three to tests/skills/figure-choose/red/judge.md, in your own words.
```

**一处任务书没写的取舍（如实登记）**：判者提示词里给了三份 brief 的**仓库路径**，
而任务书说"只读产物"。理由：不问"brief 问了什么"就无法判"图型选得对不对"；
给的是**场景**，不是**规范**（`house-style.md` / `.claude/` / `docs/` / 检查器都在禁止之列）。
判者没有被告知任何机械层读数（两层独立），其自报为"只读了三个 brief + 三个产物目录"。

==============================================================================
§0.2 作废轮登记（产物已删除，只留登记）
==============================================================================

第一轮的产物**已删除**（理由见 §9-B：**不删就等于交付一份"按规范反向设计过的 RED 基线"**）。
下表是删除前的 blob **前缀**，引自实施报告 —— **无法复核**（对象已不存在），
如实标成"报告登记值"而非本仓测量值：

| 作废轮 | 登记的文件 blob（12 位前缀，**引自报告、未复核**） |
| :--- | :--- |
| R1 | `3311994b` · `a71d4d69` · `0e73b98a` |
| R2 | `e81c7e31` · `338c58e3` · `5b027ef1` · `83c6a5fc` |
| R3 | `0f95cac3` · `1f0c9197` · `9680000a` |

**一处交叉核对（成立）**：上表的**条数 3 / 4 / 3** 与三个作废轮写手**自己**列的文件清单
一致 —— 它们的自报里 R1 与 R3 都是"**PDF only, no PNG**"（各 3 个文件：脚本 / PDF / 图注），
R2 报了 PDF + PNG（4 个文件）。两条独立来源在条数上对得上。

**可复核的替代物**：三个作废轮写手**自己的报告**（含它们各自报的 md5、页盒尺寸、
以及"我读了规范"的原句）已逐字节入 `writer-self-reports.md`；它们的**派发提示词**
见 §0.1（212 字符那一版）。**这一轮的图本身永久不可复现** —— 这是本次删除的既成代价，
登记在此以免下游以为"还能回去核"。

==============================================================================
§1 场景与地面真值
==============================================================================

三份 brief 的正文逐字内联在 `README.md`（脚本从 `brief-R*.md` 的字节直接读入）。
blob（`git hash-object tests/skills/figure-choose/red/<file>`）：

```
brief-R1.md  c0ef2522701945b1b82730d0b2994df279289120   （1122 B）
brief-R2.md  4596500881bfc4e5eed4fc31da97e6d711d7c602   （2029 B）
brief-R3.md  6749ab6e9681acdd38e6e165395f413d47137ebd   （1230 B）
```

R3 = R1 的数据与问题 + 一句"纸面交付形态"
（"I need one figure (with its caption) that I can paste straight into the body text of my paper."）。

⚠️ **旧版这里写"R1 与 R3 的区别只有这一句"—— 实测为假**：两处，`diff` 当场可证
（`[exit=1]` = 有差异；下面是**全文**，不是节略）：

```
$ diff tests/skills/figure-choose/red/brief-R1.md tests/skills/figure-choose/red/brief-R3.md
1c1
< # Brief R1 - district vulnerability composition
---
> # Brief R3 - district vulnerability composition, paper-ready
19c19,20
< structure.
---
> structure. I need one figure (with its caption) that I can paste straight into the
> body text of my paper.
[exit=1]
```

即：**标题也不同**（多一个 `, paper-ready`），第 19 行那句在 R1 里是一整行、在 R3 里
换了行。所以严格说 R1/R3 的对照隔离出的是"**交付形态这个杠杆 + 一个标题词**"，
不是"只有这一句"。标题不该有形制影响（写手看不到标题以外的东西被改的事实），
但**登记按实测**。

**地面真值**（`python tests/skills/figure-choose/red/truth.py`，输出逐字）：

```
## R1 ground truth: pairwise composition similarity (lower L1 = more similar)
row sums: A=1.00, B=1.00, C=1.00, D=1.00, E=1.00, F=1.00
  L1(B,D) = 0.06
  L1(A,E) = 0.10
  L1(C,F) = 0.10
  L1(B,E) = 0.12
  L1(A,F) = 0.16
  L1(D,E) = 0.18
  L1(A,B) = 0.22
  L1(E,F) = 0.26
  L1(A,C) = 0.26
  L1(A,D) = 0.28
  L1(C,E) = 0.36
  L1(B,F) = 0.38
  L1(D,F) = 0.44
  L1(B,C) = 0.48
  L1(C,D) = 0.54
  => most similar pair: B-D (L1=0.06); runner-up A-E (L1=0.10)

## R2 ground truth: correlation of each factor with historical disaster count
  (n=6 districts; Pearson and Spearman both shown - small n, so both)
  pop_density  Pearson r = +0.3599   Spearman rho = +0.5429
  mean_slope   Pearson r = +0.9302   Spearman rho = +0.9429
  veg_cover    Pearson r = -0.7436   Spearman rho = -0.7714
  infra_index  Pearson r = -0.7766   Spearman rho = -0.7714
  => strongest |Pearson|: mean_slope (r = +0.9302)
  => strongest |Spearman|: mean_slope (rho = +0.9429)
```

⇒ R1 的答案是 **B–D**（0.06，次近 A–E / C–F 并列 0.10）；
R2 的答案是 **mean_slope**（|r| = 0.93，次强 infra_index |r| = 0.78）。
两问都有唯一确定答案，不是"怎么看都行"。

==============================================================================
§2 机械层逐字读数（同一把尺：Task 1 的 check-figure-style.py）
==============================================================================

三份产物各有 `figure.pdf`（矢量主产物）与 `figure.png`（同源 300 dpi 栅格）。
两条载体都判，读数一致（PDF 的 F1 走页盒、PNG 的走 `--dpi 300`）。

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R1/figure.pdf --caption @tests/skills/figure-choose/red/out-R1/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.521（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 203 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 203 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R1/figure.png --caption @tests/skills/figure-choose/red/out-R1/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.521（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 203 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 203 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R2/figure.pdf --caption @tests/skills/figure-choose/red/out-R2/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.743（分母 6.31 in）
FAIL  F2  彩色主色数 7
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 285 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 285 词）
RESULT: FAIL（F1,F2,F3a,F3b,F3c）
[exit=1]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R2/figure.png --caption @tests/skills/figure-choose/red/out-R2/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.743（分母 6.31 in）
FAIL  F2  彩色主色数 7
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 285 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 285 词）
RESULT: FAIL（F1,F2,F3a,F3b,F3c）
[exit=1]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R3/figure.pdf --caption @tests/skills/figure-choose/red/out-R3/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.204（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 177 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 177 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R3/figure.png --caption @tests/skills/figure-choose/red/out-R3/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.204（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 177 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 177 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]
```

**三份产物的图注（逐字、全文、`cat`）**——这是 F3a/b/c 全红的直接原因：

<<CAPTIONS>>
三份**全部**用 `Figure 1.`（**句点**，不是 `Figure 1:`）、**全部**以句点收尾、
词数 203 / 285 / 177（硬上限 17）。即：**独立写手把"图注"理解成了一段
完整的方法学说明文字，而不是一行图题**。这是本轮 RED 最整齐、最可复现的失败形态。

==============================================================================
§3 红绿表（R1/R2/R3 × F1/F2/F3a-d）
==============================================================================

| 场景 | F1 图宽比 | F2 主色数 | F3a 前缀 | F3b 词数 | F3c 句末 | F3d 非空 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R1**（构成数据） | **FAIL** 1.521 | PASS 3 | **FAIL** | **FAIL** 203 | **FAIL** | PASS |
| **R2**（多变量对比） | **FAIL** 1.743 | **FAIL** 7 | **FAIL** | **FAIL** 285 | **FAIL** | PASS |
| **R3**（交付形态） | **FAIL** 1.204 | PASS 3 | **FAIL** | **FAIL** 177 | **FAIL** | PASS |

- 三份产物 `exit=1`，**没有一份是 `exit=2`**（`2` = 根本没判成，不是判红）。
- **判红 13 格 / 满 18 格；绿 5 格**（= F2 的 R1/R3 两格 + F3d 三格）。
- ★ **这个汇总数是从上表当场重算的，不是手写的**。旧版这里写"判红 16 格 / 满 18 格；
  只有 F2（R1,R3）与 F3d（×3）绿"——**16+5=21≠18，自相矛盾**，而它上方三行的表给的是
  4/5/4 = 13 红。**逐格数据是对的，错的是汇总**（本项目栽过五次的同一型）。重算命令与输出：

```
$ python - <<'PY'
import pathlib
doc = pathlib.Path("tests/skills/figure-choose/red/red-evidence.md").read_text(encoding="utf-8")
sec = doc.split("§3 红绿表")[1].split("§4")[0]
rows = [l for l in sec.splitlines() if l.startswith("| **R")]
tot_r = tot_g = 0
for l in rows:
    cells = [c.strip() for c in l.strip().strip("|").split("|")]
    verdicts = ["FAIL" if c.startswith("**FAIL**") else "PASS" for c in cells[1:]]
    nf = verdicts.count("FAIL"); ng = verdicts.count("PASS")
    tot_r += nf; tot_g += ng
    print(f"{cells[0]}: cells={len(cells)-1}  FAIL={nf}  PASS={ng}  -> "
          + "".join("R" if v == "FAIL" else "G" for v in verdicts))
print(f"TOTAL: 判红 {tot_r} 格 / 满 {tot_r + tot_g} 格；绿 {tot_g} 格")
PY
**R1**（构成数据）: cells=6  FAIL=4  PASS=2  -> RGRRRG
**R2**（多变量对比）: cells=6  FAIL=5  PASS=1  -> RRRRRG
**R3**（交付形态）: cells=6  FAIL=4  PASS=2  -> RGRRRG
TOTAL: 判红 13 格 / 满 18 格；绿 5 格
[exit=0]
```

- F3d 三份全绿是**设计使然**：本轮没有"空图注"这种失败形态；F3d 的价值要等
  GREEN 或变异证明去压，本轮的 RED 没有区分力 —— **不许把它算成"通过"**。

==============================================================================
§4 判断层（判者判词逐字见 `judge.md`；本节只记结论与"两层分工"的现场证据）
==============================================================================

判者结论（逐字引用 `judge.md` 的三份小结表）：

| 产物 | 图表类型 | 饼图规则 |
| :--- | :--- | :--- |
| R1 | correct | no |
| R2 | correct | no |
| R3 | correct（但三元图 low/medium 轴题互换，属标注错误） | no |

**★ 这正是本任务要留的现场证据：机械层与判断层各抓各的，不可互相替代。**

1. **机械层抓不到的**：
   - "图型选得对不对"——判者判三份**全部 correct**，而机械层对这层**无话可说**。
   - R3 的**实质硬伤**：判者发现三元图 (b) 的 **low / medium 两条轴题被互换**
     （底边刻度画的是 medium 值却标 "Low share"；左边缘画的是 low 值却标
     "Medium share"）。判者的判词："后果不是审美问题：按图上的文字去读，C 会被读成
     low 约 0.37、medium 约 0.55，而真值是 low 0.55、medium 0.30……**题目要求的
     '描述每个区的脆弱度构成'在 (b) 面板里按印刷文字读会读反**"。
     而机械层对 R3 的 F1/F2/F3 读数里**看不出任何异常**——F2 还是绿的。
   - 所以：**R3 是一张"机械层只红在格式、实质却读反了数据"的图**。判据齐全 ≠ 图对。
2. **判断层抓不到的**：图宽比、主色数、图注词数——判者只在 R1 的"小瑕疵"里顺口提了
   "整图偏宽（9.6×4.5 in），排进论文单栏时字会偏小"，**没有**把它报成违规；真正把它
   判红的是机械层的 F1（1.521）。两条判据在这一点上**独立收敛**。
3. **★ 两层判据都抓不到的第三例（R1 的网格线画错族）—— 本节要登记的第三个例子。**
   `out-R1/make_figure.py:174-178`：`if fixed == 0:`（注释写 `# low = c`）与
   `elif fixed == 1:`（`# medium = c`）**算出的是完全相同的数组**
   （`l_ = (1-c)*s, m_ = c, h_ = 0`）⇒ **"low = c" 那一族网格线从没被画出来，
   "medium = c" 那一族被画了两遍**（同一条线重绘，视觉上仍是一族）。
   R1 的**轴标题与刻度是对的**（判者判 Q1 correct，读数没被颠倒），所以这是一处
   **只影响可读性的产物缺陷**：机械层看不出（F1 图宽 / F2 色数 / F3 图注都与之无关），
   判断层也没看出（判者在 R1 的"小瑕疵"里提了点位拥挤与整图偏宽，**没提网格**）。
   ⇒ **不许把"两层判据都红了别的问题"读成"两层判据抓到了其它一切"**。
   实测（脚本按行号直接跑 `fixed=0` 与 `fixed=1` 的两份数组）：

```
$ python - <<'PY'
import numpy as np
s = np.linspace(0.0, 1.0, 60)
for c in (0.1, 0.5, 0.9):
    f0 = ((1 - c) * s, c * np.ones_like(s), np.zeros_like(s))          # fixed == 0
    f1 = ((1 - c) * s, c * np.ones_like(s), np.zeros_like(s))          # fixed == 1
    f2 = ((1 - c) * s, (1 - c) * (1 - s), c * np.ones_like(s))         # fixed == 2
    print(f"c={c}: fixed0==fixed1 -> {all(np.array_equal(a, b) for a, b in zip(f0, f1))}"
          f" | fixed0==fixed2 -> {all(np.array_equal(a, b) for a, b in zip(f0, f2))}")
PY
c=0.1: fixed0==fixed1 -> True | fixed0==fixed2 -> False
c=0.5: fixed0==fixed1 -> True | fixed0==fixed2 -> False
c=0.9: fixed0==fixed1 -> True | fixed0==fixed2 -> False
[exit=0]
```

   （上面 `f0` / `f1` 两行**逐字符相同**，就是 `make_figure.py:174-178` 那两支的原文数组；
   `f2` 那支（high = c）与之不同，是对的。）
4. **饼图那条规则本轮没有区分力**：任务书预期 R1"压饼图这条（实测 n=120 里 0 张）"，
   但**三个写手没有一个选饼图**。两份构成数据的 brief（R1、R3）都选了
   "100% 堆叠水平条 + 三元单纯形"。判者据此判"饼图规则：no"×3。
   ⇒ 本轮 **"构成数据用饼图"这个失败形态没有出现**；它是不是常见错误，本任务**没有**
   提供证据。Task 3/6 不许把"没出现"当成"这条规则不需要"。
   同时它也是**机械层盲区**的注脚：饼图通常也 <=4 色，F2 会放它过去。

==============================================================================
§5 遗留风险 #1：F2 的抗锯齿（AA）余量 —— 实测回答
==============================================================================

**问题（Task 1 遗留）**：Task 1 实测 4 色 PDF 的最大抗锯齿箱占 0.312%，地板 0.5%
（余量 0.188pp）⇒ 带渐变/细网格/抗锯齿色带的图可能让 F2 **虚高成假 FAIL**。

**取证工具**：`tests/skills/figure-choose/red/f2-diagnose.py`（**不改** Task 1 的检查器）：

- `raster_rgb()` / `color_count()` / `RASTER_DPI` / `F2_MAX` **直接 import 原件**
  （`check-figure-style.py` 有 `__main__` 守卫，可 import）；
- 只有"取箱"这一步必须重写 —— 原件只返回**计数**，本工具要的是**每个箱的占比**；
- 重写的那份**每次运行都自证没漂**：对**每一个**输入断言
  `len(过地板的箱) == color_count(rgb)`，并对 `color_count` 的源码做字面 tripwire
  （`resize((320, 320), Image.NEAREST)` · `< 24` · `// 16` · `>= 0.005` 任一消失 ⇒ fail-closed 拒绝出数）。
- **旧版是"逐行照抄"**（复制件，**没有任何东西防止它随 Task 1 的检查器漂移**）；
  现在"能 import 的都 import，唯一必须重写的那一步挂在一致性断言上"。
- 全量逐字输出见 `f2-boxes.txt`（341 行）；**它由 `--out` 用 `write_bytes` 落盘**，
  故重跑能逐字节复现（Windows 的 `> file` 会把行尾翻成 CRLF，与入库件不符）。

**同一支工具的忠实性先自证**（跑 Task 1 的 fixtures；下面是**完整输出**，不是节略 ——
旧版这里把 `loaded_px` / `all chroma boxes` / 未过地板的箱都静默删掉了）：

```
$ python tests/skills/figure-choose/red/f2-diagnose.py tests/skills/figure-choose/fixtures/ok-03.png
=== tests/skills/figure-choose/fixtures/ok-03.png
    loaded_px=1260x600  (raster)
    F2-relevant boxes (>= 0.5% floor): 4   => F2 PASS
    all chroma boxes kept (before floor): 4
      #1  bin(14, 6, 7)  share= 20.000%  >=FLOOR
      #2  bin(12, 11, 4)  share= 20.000%  >=FLOOR
      #3  bin(4, 7, 10)  share= 20.000%  >=FLOOR
      #4  bin(2, 8, 3)  share= 20.000%  >=FLOOR
    boundary: no sub-floor chromatic box at all (nothing near-missed the 0.5% floor)
[exit=0]

$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/fixtures/ok-03.png --caption "Figure 3: A caption here" --textwidth-in 6.31 --dpi 100
FAIL  F1  图宽比 1.997（分母 6.31 in）
PASS  F2  彩色主色数 4
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 5（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 3 词）
RESULT: FAIL（F1）
[exit=1]

$ python tests/skills/figure-choose/red/f2-diagnose.py tests/skills/figure-choose/fixtures/ok-05.pdf tests/skills/figure-choose/fixtures/bad-f2-five-colors.pdf
=== tests/skills/figure-choose/fixtures/ok-05.pdf
    loaded_px=900x390  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 4   => F2 PASS
    all chroma boxes kept (before floor): 8
      #1  bin(14, 6, 7)  share= 19.688%  >=FLOOR
      #2  bin(12, 11, 4)  share= 19.688%  >=FLOOR
      #3  bin(4, 7, 10)  share= 19.688%  >=FLOOR
      #4  bin(2, 8, 3)  share= 19.688%  >=FLOOR
      #5  bin(14, 7, 7)  share=  0.312%    below
      #6  bin(12, 11, 5)  share=  0.312%    below
      #7  bin(5, 8, 10)  share=  0.312%    below
      #8  bin(3, 9, 4)  share=  0.312%    below
    boundary: highest sub-floor box = 0.312%  |  lowest counted box = 19.688%  |  floor = 0.500%
=== tests/skills/figure-choose/fixtures/bad-f2-five-colors.pdf
    loaded_px=900x390  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 6   => F2 FAIL
    all chroma boxes kept (before floor): 13
      #1  bin(14, 6, 7)  share= 14.062%  >=FLOOR
      #2  bin(12, 11, 4)  share= 14.062%  >=FLOOR
      #3  bin(6, 12, 14)  share= 14.062%  >=FLOOR
      #4  bin(4, 7, 10)  share= 14.062%  >=FLOOR
      #5  bin(10, 3, 7)  share= 13.750%  >=FLOOR
      #6  bin(2, 8, 3)  share= 13.750%  >=FLOOR
      #7  bin(13, 8, 9)  share=  0.312%    below
      #8  bin(12, 13, 14)  share=  0.312%    below
      #9  bin(11, 6, 9)  share=  0.312%    below
      #10 bin(10, 13, 12)  share=  0.312%    below
      #11 bin(10, 4, 8)  share=  0.312%    below
      #12 bin(6, 10, 5)  share=  0.312%    below
      #13 bin(3, 9, 4)  share=  0.312%    below
    boundary: highest sub-floor box = 0.312%  |  lowest counted box = 13.750%  |  floor = 0.500%
[exit=0]
```

（0.312% 正是 Task 1 记录的那个 AA 箱占比 —— 工具复现无误；`ok-03` = 4、`ok-05` = 4、
`bad-f2` = 6，与 `figure-style-baseline.txt` 逐格一致。）

**三份写手图的实测（`f2-boxes.txt` 的 `boundary` 行，逐字）**：

| 产物 | 计数色箱（>=0.5%） | 最低的**计数**箱 | 最高的**落选**箱 | 余量（地板 − 落选箱） | 倍数 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R1（3 色平涂） | 3 | 3.260% | 0.127% | **0.373pp** | 3.94x |
| R2（连续红蓝热图） | 7 | 0.689% | 0.370% | **0.130pp** | 1.35x |
| R3（3 色平涂） | 3 | 4.499% | 0.081% | **0.419pp** | 6.17x |
| （参照）Task 1 的 4 色 PDF | 4 | 19.688% | 0.312% | 0.188pp | 1.60x |

⚠️ **旧版把 R1 标成"3 色平涂 + 灰色矩阵"—— 实测为假，已按实测改准。**
R1 的 3 个计数箱（6.370% / 5.903% / 3.260%）就是它的三个 tier 色
`#ffeda0` / `#feb24c` / `#f03b20` 各自的面积（该图的彩色元素只有这三色 + 灰阶的点/线/字，
灰阶会被 F2 的近灰阈值滤掉）。其中**两个箱号与对应纯色逐位相同**
（`bin(15,14,10)` / `bin(15,11,4)`）；第三个的纯色落在 `bin(15,3,2)`，实测箱是
`bin(15,3,1)`，蓝通道差一档 —— **原因未查，只报实测**。**R1 里没有矩阵面板**：
`out-R1/make_figure.py` 只有 (a) 100% 堆叠条 + (b) 三元图两个面板。
"灰色矩阵"是**作废轮**的 R1/R3 的画法（其自报原文见 `writer-self-reports.md`），
当前轮 R2 的四个面板是 bars / scatter / 连续发散热图（z 分数，`RdBu_r`）/ dendrogram，
**也没有灰色矩阵**。

**如实回答任务书的两问**：

1. **出现了"看起来该判 PASS 却栽在某个小色箱上"的情形吗？——没有。**
   R1、R3 是**真·3 色设计**（序数单色阶），F2 判 PASS，且最大的杂色箱只占
   0.127% / 0.081%，离地板还有 0.373pp / 0.419pp（3.94x / 6.17x）。
   R2 的 F2 FAIL **不是虚高**：它给 z 分数热图用了**连续红-蓝发散色图**，色箱本来就
   上百个（`f2-boxes.txt`：落选前的彩色箱 **152** 个），越过地板的 7 个是**最大的几个
   热图格子**（2.052% / 1.529% / 1.072% / 1.068% / 0.725% / 0.710% / 0.689%）。
   ⇒ 方向判对了（连续色图 = 多色），**但读数 7 不稳定**。

2. **★ 风险以另一种形态真实出现了：R2 有一整片"贴着地板"的落选箱。**
   紧挨地板的第 8-19 名落在 **0.329% ~ 0.370%** 区间（12 个箱子，全部只比地板低
   0.130 ~ 0.171pp）。也就是说，只要 R2 的热图格子再大一点（dpi、画布尺寸、格数任一
   变动），这 12 个箱子就会越线，**F2 的读数会从 7 跳到最多 19**。
   ⇒ 对**连续色图/渐变**类图，F2 的**数值**是"地板切一条连续谱"切出来的产物，
   不是稳定的设计量；**红绿方向可信，具体条数不可引用**。Task 3 若要把 F2 的窄口径
   写进规范（如"主色数 <= 4"），必须先说清"连续色图"这类是否在射程内。

==============================================================================
§6 遗留风险 #2：PDF 的 F2 只判第 1 页 —— 实测回答（并发现 F1 同样只判第 1 页）
==============================================================================

**三份写手产物都是单页 PDF**（`f2-diagnose.py` 打印 `pdf_pages=1` × 3）⇒
本条限制在本轮 RED 上**没有实际咬到**，取舍无影响。

**但为了把这条从"未测"变成"实测"，另做了一个两页探针**（入库件
`red/multipage-probe.pdf`；**生成器 `red/make-multipage-probe.py` 也已入库** ——
旧版只有那个二进制、没有生成脚本，第 2 页的读数**无法从仓库复现**，等于一句无从核对的话）。
构造：第 1 页 6.31 in 宽 / 1 个彩色主色，第 2 页 12.00 in 宽 / 6 个彩色主色。

★ **Task 3b 修 ① 之后（2026-09-30）这份探针重生成过一次** —— page1 原先**整页铺一个非 H14 的红底**
（`#f03b20`，众数亮度 109 < `BG_MIN_LUMA`=136）。`F4`/`F5` 落地后**那种 page1 自己就红**
⇒ 整份判 `FAIL（F4,F5）` ⇒ 把 `house-style.md` §0 的"整份仍判 PASS"打成假、连带 `G-F0-verdict` 红。
现 page1 改成**一张合规图**（白底 + 一个 H14 色、色带只占页面下 1/3）⇒ **整份仍判 PASS**，
且"只读 `doc[0]`"这件事从 `F1`/`F2` **扩到 `F1`/`F2`/`F4`/`F5`**（page2 在四条上都越界）。
**现行读数**：`blob=d745b7ba1eb0f61d1e1d640e7a8265ee0f094392` · `bytes = 1926` · `probe_verdict = PASS`。
⚠️ 下面两块 transcript 是**那一轮**的读数（`blob=dc8697b00cff…` / `bytes = 1923`），
它们是那一轮的逐字记录、**不随本次重生成改写**（同 §11 里那两处）；现行值以本行为准。

**生成器输出（含 blob 与逐页读数；`--twice` 连跑两次自证可重复生成）**：

```
$ python tests/skills/figure-choose/red/make-multipage-probe.py --twice
wrote tests/skills/figure-choose/red/multipage-probe.pdf  blob=dc8697b00cffc526b61e86314679fefcf1a5eae6
pages = 2   file = multipage-probe.pdf   bytes = 1923
  page1: width=6.310 in -> ratio 1.000  |  彩色主色数 = 1
  page2: width=12.000 in -> ratio 1.902  |  彩色主色数 = 6
rerun  blob=dc8697b00cffc526b61e86314679fefcf1a5eae6  identical=True
[exit=0]
```

（逐页读数用的是**检查器本体的 `color_count`**（import 进来），不是另抄一份。）

**检查器对这份两页 PDF 的判词**：

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/multipage-probe.pdf --caption "Figure 1: Multipage probe" --textwidth-in 6.31
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 1
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 4（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 2 词）
RESULT: PASS
[exit=0]
```

⇒ 检查器报的是 **page1 的读数（F1 1.000 / F2 1）**；page2 的
**F1 1.902 与 F2 6 被完全忽略**。

**结论比任务书说的更宽**：任务书只点了"F2 只判第 1 页"，
**实测 F1 也走 `doc[0]`**（`fig_width_in()` 里同样是 `doc[0].rect.width`）。
即：一张多页 PDF，**只要第 1 页合规格，整份文件就判 PASS**，后面几页完全在射程外。

取舍是否可接受：**本任务内可接受**（三份产物皆单页，且 MCM 图惯例是一图一文件一页）。
但这是一条**未设防的边**：Task 3 写规范时应写明"一个图文件 = 一页"，
否则一份多页 PDF 可以合法地绕过 F1 与 F2。

==============================================================================
§7 可复算性（"脚本 + 图 + 图注"三者都入库；脚本能独立再生图）
==============================================================================

**命令（入库脚本，可当场重跑）**：`red/verify-reproducible.py` —— 把三份产物各复制到
仓外临时目录、**只留 `make_figure.py`**、删掉图、跑一遍，再与**入库件**比字节。

★ **旧版这一节没有命令**（只有一段手贴的输出），也没有人重跑过；
且旧版把 md5 标成 `committed=`，容易被读成 git blob 哈希（本仓纪律要求用 `git hash-object`）。
新版**两个口径都给**，并且多比了一列：`HEAD:{path}` 的 blob，证明比的是**入库**那一份。

```
$ python tests/skills/figure-choose/red/verify-reproducible.py
temp workdir: <TMP>/m3-t2-repro-1_7x477d
--- out-R1: rc=0
      figure.pdf   committed_blob=a25d0a12bb80  regenerated_blob=a25d0a12bb80  (HEAD=a25d0a12bb80)  md5=38c92a1dbf44  identical=True
      figure.png   committed_blob=3ebb207af1a6  regenerated_blob=3ebb207af1a6  (HEAD=3ebb207af1a6)  md5=f5359942ff4a  identical=True
      caption.txt  committed_blob=b85515fdeb54  md5=2f69656eceee  regenerated=(absent)  identical=False

--- out-R2: rc=0
      figure.pdf   committed_blob=35b30acf7e51  regenerated_blob=35b30acf7e51  (HEAD=35b30acf7e51)  md5=64378431c7c3  identical=True
      figure.png   committed_blob=1bfcf8de4f95  regenerated_blob=1bfcf8de4f95  (HEAD=1bfcf8de4f95)  md5=3bc9c6c86770  identical=True
      caption.txt  committed_blob=24c07ec6a0a0  md5=364f98cfcd98  regenerated=(absent)  identical=False

--- out-R3: rc=0
      figure.pdf   committed_blob=db55c0a97986  regenerated_blob=db55c0a97986  (HEAD=db55c0a97986)  md5=da53a421045d  identical=True
      figure.png   committed_blob=49be5c44d92e  regenerated_blob=49be5c44d92e  (HEAD=49be5c44d92e)  md5=be19e6417d5c  identical=True
      caption.txt  committed_blob=8848b1ef4cee  md5=fbfd65f7e513  regenerated=(absent)  identical=False

RESULT: ALL FIGURES BYTE-IDENTICAL
[exit=0]
```

（`<TMP>/m3-t2-repro-1_7x477d` 的随机后缀每次不同，是唯一随运行变化的部分。）

- **图可复算，且是字节级确定**（三个写手都主动压掉了 matplotlib 的 PDF 时间戳，
  故 `figure.pdf` 逐字节可重现）——`rc=0` × 3，且 6 份图的
  `git hash-object` blob 与 `HEAD:` 里那一份**三方相同**
  （入库件 / HEAD / 重新生成）。**这一节是本任务"可复算"主张的核心**，
  本轮由修复者当场重跑过一次（见上表；旧版只跑过一次且没留命令）。
- **图注不由脚本再生**（`caption.txt` 是写手手写的静态文件，脚本不写它）。
  这与 brief 的措辞一致（brief 只要求脚本"regenerates the figure"），但 Task 6 若想
  让 GREEN 的图注也可复算，得另外要求。**这是一处已知的、有意保留的缺口**。
- 三个脚本都靠 `__file__` 定位输出目录，故与 cwd 无关；都无网络、无外部输入。

==============================================================================
§8 RED 的典型失败形态（逐条给机械层读数或判者判词作证）
==============================================================================

| # | 失败形态 | 出现的场景 | 证据 |
| :- | :--- | :--- | :--- |
| 1 | **图注写成了一整段方法学文字**（不是一行图题） | R1 / R2 / R3 **全部** | F3b 词数 203 / 285 / 177（硬上限 17）；`Figure 1.` 用句点 → F3a 红 ×3；末尾带句点 → F3c 红 ×3 |
| 2 | **图宽不贴正文栏宽**（按"好看"定尺寸，不按排版定） | R1 / R2 / R3 **全部** | F1 比值 1.521 / 1.743 / **1.204**。R2 直接把 2x2 面板放到 11.0x8.4 in；R3 最险——**1.204 只比上限 1.20 高 0.004**（7.6 in vs 6.31 in 栏宽） |
| 3 | **连续色图让主色数爆掉** | R2 | F2 = **7**（> 4）。z 分数热图用连续红-蓝发散色图，落选前 152 个色箱；过线的 7 个是最大格子，且紧邻其下还有 12 个箱子挤在 0.329%~0.370%（见 §5） |
| 4 | **"构成数据用饼图"** —— 预期出现，**实际没有出现** | 无 | 判者对 R1/R2/R3 的饼图规则判词均为 **no**；R1/R3 都选了 100% 堆叠条 + 三元单纯形 |
| 5 | **图型选错** —— 预期出现，**实际没有出现** | 无 | 判者三份全判 **correct**；"机械层抓不到图型"这条盲区因此**本轮没能用失败样例证成**，只由 R3 的轴题互换间接证成（见 §4） |
| 6 | **★ 机械层看不见的实质错误** | R3 | 判者：三元图 (b) 的 low / medium 轴题互换 ⇒ "题目要求的'描述每个区的脆弱度构成'在 (b) 面板里按印刷文字读会**读反**"。而机械层对 R3 只红在 F1/F3a/b/c（格式），F2 还是绿的 |
| 7 | 空图注（F3d） | 无 | 三份 F3d 全 PASS，**本轮无区分力**；不许记成"规范起作用了" |
| 8 | **★ 两层判据都没报的产物缺陷：网格线画错族** | R1 | `out-R1/make_figure.py:174-178`：`fixed == 0`（注释 "low = c"）与 `fixed == 1`（"medium = c"）**算出同一个数组** ⇒ "low = c" 那族网格线从未画出、"medium = c" 那族画了两遍。机械层与之无关（F1/F2/F3 都看不出），判者在 R1 的"小瑕疵"里也**没提**（详见 §4-3 的实测） |

**★ 特别指出（任务书要求显式点出）**：
形态 4 与 5 是"机械层**结构性抓不到**"的那一类。本轮它们恰好**没有**以失败形态出现，
**不是因为检查器漏了，也不是因为这条规范不重要**——而是因为本次三个写手恰好都选了
合规载体。R3 的轴题互换（形态 6）则给出了一个**反例方向**的证明：同一张图，机械层
绿了 F2、判者却读出"数据读反了"。所以两层判据必须并存，
**且 Task 6 不许把"机械层全绿"当成"图是对的"**。

**★ 反向的一条同样要点（形态 8，本轮修复新增）**：R1 的网格线画错族**两层判据都没报**
（机械层结构上判不到这类缺陷；判者读了三张图、复算过全部数字，也没提网格）。
**所以"两层判据"并不等于"覆盖了一切"** —— 这条同时挡住两种过度读法：
① 不许把"机械层红了 13 格"读成"这一轮的问题都被抓到了"；
② 不许把"判者判了 correct"读成"这张图没有别的毛病"。
两层判据各自**明确**的射程是："格式类"与"选型+可读性judgement类"。
**"图里的每一个几何元素都画对了没有"不在任何一层的射程内。**

==============================================================================
§9 与任务书不符处（5 条：A-C 由当场实测逼出，D-E 是追加的入库件）
==============================================================================

### A. 写手提示词多了一句隔离限定（**最重要的偏离**）

任务书：「写手提示词**只准包含**：① 那一份 brief 的路径；② 产物输出目录。」
本实施在第二轮（有效轮）多了一句："Work only from that brief - do not read or write
any other file."

- **为什么**：§0 已证"结构性隔离"不存在，且第一轮因此整轮作废。若不加这句，
  任何一间写手都可能再次读到检查器/规范，RED 基线随时作废。
- **代价/风险**：这句本身**不泄露任何判据**（没提 skill、规范、图宽、配色、饼图、
  判据、期望答案），但它**暗示了"存在别的文件"**。严格按任务书字面，这是一处偏离。
- **留痕**：第一轮与第二轮的完整提示词**逐字节**在本文件 §0.1，以及
  `writer-self-reports.md`（六个写手 + 判者的提示词与完整自报原文）。
  **旧版把审计者指向实施报告 `.superpowers/sdd/task-m3-t2-report.md` —— 那是 gitignored 的暂存区**，
  等于"最载重的审计线索放在一个会被清理的地方"；且旧版贴的提示词是**软换行**的、
  非逐字节。第一轮修复时两处都已改正。
- 另一处配套动作：brief 被**字节相同**地搬到仓外临时目录（`git hash-object` 三份
  全部 `identical=True`），写手拿到的是仓外路径 —— 这**没有**违反"只给路径"的规则，
  但同样是任务书没写的做法。

### B. 第一轮 RED 整轮作废并重跑（任务书没有这一轮）

任务书 Step 2 只说"派 RED subagent"，**没有**预设"隔离不成立 ⇒ 重跑"。
本实施把第一轮三份产物**删除**并重跑；删除前已登记它们的 blob ——
登记值**逐条内联在本文件 §0.2**（每个作废轮一行的表），并如实标明"引自报告、未复核"。
（旧版这里写的是"（见实施报告）"，把读者指向 gitignored 的 `.superpowers/sdd/` 暂存区；
**指针不许指向会被清理的地方**，故改成指本文件的同一处内联表。）
**这一轮是必须的**：不删就等于交付一份"按规范设计过的 RED 基线"，
Task 6 的 RED/GREEN 对照会得出"规范没用"的**反向**结论。

### C. 产物目录用 `out-R{n}/` 子目录，而非 `out-R{n}.*` 前缀文件

任务书 Files 段写 `red/{out-R1.,out-R2.,out-R3.}*`（前缀式文件名）。
本实施用 `red/out-R1/{make_figure.py,figure.pdf,figure.png,caption.txt}`。
理由：写手要产出 4 个文件且文件名由写手定，前缀式会让下游命令随写手的命名漂移；
子目录把"一个场景的产物"封成一个单元，`out-R{n}/` 与 `out-R{n}.*` 表达的是同一件事。

### D. 追加了任务书没列的证据文件

- `red/f2-boxes.txt`（341 行 / 16801 B）：§5 的全量逐字取证输出。
- `red/multipage-probe.pdf`（1923 B / blob `dc8697b00cff`）：§6 的两页探针入库件。
  连同它的生成器 `red/make-multipage-probe.py` 一起入库，使第 2 页的读数**可从仓库复现**。

### E. 第一轮修复（独立评审 Needs fixes 后）新增入库的文件

那一轮评审对上一版提了 1 条 Important + 9 条 Minor，逐条修完后**造证据的脚本也一并入库**
（通则 7：证据放 gitignored = 丢失）。新增/变更：

| 文件 | 为什么入库 |
| :--- | :--- |
| `truth.py` | 地面真值生成器。旧版只在 gitignored 的 `.superpowers/sdd/` 里，而 §1 直接引用了它 |
| `f2-diagnose.py`（改） | §5 的取证工具。旧版**抄**检查器的实现；现改为 import + 逐例一致性断言（详见 §5） |
| `verify-reproducible.py` | §7 的"逐字节重生成"脚本。旧版**只有输出、没有命令**，这一节无法独立复跑 |
| `make-multipage-probe.py` | §6 探针的生成器。旧版只有一个二进制，第 2 页读数无法复现 |
| `writer-self-reports.md` | 六个写手 + 判者的**提示词与完整自报原文**（逐字节抢救自仓外 transcript） |
| `rescue-transcripts.py` | 上一条的抢救脚本（记录它从哪来、摘了什么、**没有**摘什么） |
| `make-briefs.py` / `make-readme.py` / `make-evidence.py` | 三份入库文本（briefs / README / 本文件）的生成器。它们原先在 gitignored 区 ⇒ "证据在册、造它的脚本随时会丢"，而且手工改文本后重跑旧生成器会把修复**悄悄回滚** |

==============================================================================
§10 第一轮修复记录（独立评审 Needs fixes 后）—— 1 条 Important + 9 条 Minor + 3 条 ⚠️
==============================================================================

本节是**第一轮**修复的记录；**本节内的"本轮/该轮"一律指那第一轮**
（**第二轮**修复的记录在本文件 §11 —— **要看最新状态直接读 §11**）。
评审独立复算了几乎每一个载重的数（F1 由 figsize 反推 1.5215 / 1.7433 / 1.2044 ✓、
词数 203 / 285 / 177 ✓、F2 箱表 ✓、`doc[0]` 断言 ✓、R3 轴互换逐行核实 ✓、真值相关系数 ✓）。
下面**逐条**记处置；凡与本文件其它节的实测冲突的，以实测为准（文内已写明）。

| # | 评审条目 | 处置 | 落在本文件哪一节 |
| :- | :--- | :--- | :--- |
| **Imp-1** | 基线头条"判红 **16 格 / 满 18 格**"自相矛盾（16+5=21≠18），且与自身上方表（4/5/4=13 红）不符 | **当场用命令从逐格表重算 = 13 红 / 5 绿**，三处（本文件 §3、实施报告 §0 与 §4）全部改成实测值；命令与输出已贴进 §3 | §3 |
| M-2 | `out-R1/make_figure.py` 的 `fixed == 0` 与 `fixed == 1` 算出同一数组 ⇒ 少画一族、重画一族；两层判据都没报 | **登记为"两层都抓不到的第三例"**（初版称"两层各抓到对方抓不到的"易被读成"其它都被抓到了"），并配 `np.array_equal` 实测 | §4-3 · §8 形态 8 |
| M-3 | 证据里的命令跑不了（`m3-t2-truth.py` / `m3-t2-f2-diagnose.py` / §7 重生成脚本都在 gitignored 区） | 真值生成器 `truth.py`、取证工具 `f2-diagnose.py`、重生成脚本 `verify-reproducible.py` **搬进 `red/`**，引用路径全部订正；`f2-diagnose.py` 的 usage 串同步订正 | §1 · §5 · §7 · §9-E |
| M-4 | 标"逐字"其实是节略（图注块被 "..." 截断） | 图注改由生成器**从 `caption.txt` 的字节直接读入**（去掉省略号），标签"逐字"由构造保证；§5 的 fixtures 块同病同治，补成**完整输出** | §2 · §5 |
| M-5 | 最载重的审计线索只活在 gitignored 报告里；贴出的提示词是软换行的 | **两轮提示词 + 判者提示词**逐字节入 §0.1（**不软换行**）；**六个写手 + 判者的完整自报原文**入 `writer-self-reports.md`；作废轮登记入 §0.2 | §0.1 · §0.2 · `writer-self-reports.md` |
| M-6 | `README.md` 目录清单漏了 `f2-boxes.txt` 与 `multipage-probe.pdf` | 清单补齐（并补上该轮新增的六个脚本） | `README.md` §2 |
| M-7 | 两处失准：R1 被说成"3 色平涂 + 灰色矩阵"；"R1 与 R3 的区别只有这一句" | 均按实测改准（R1 无矩阵面板，见 §5 脚注；R1/R3 的 `diff` 全文入 §1，**标题也不同**） | §1 · §5 |
| M-8 | `f2-diagnose.py` **抄**检查器实现（无任何防漂移） | 改成 **import 原件**（`raster_rgb` / `color_count` / 常量），唯一必须重写的那步挂**逐例一致性断言** + 源码 tripwire；重跑 `f2-boxes.txt` **逐字节不变**（blob 仍是 `e46f98b66c5c`） | §5 |
| M-9 | `multipage-probe.pdf` 没有生成脚本（第 2 页读数无法复现） | 补 `make-multipage-probe.py` 入库；重生成后 blob `dc8697b00cff`、1923 B，读数两页复现；§6 的尺寸/blob 全部按**该轮实测**更新 | §6 · §9-D |
| M-10① | 写手是 `general-purpose`、未用 `fork`，但 diff 里核不到 | 入 §0.1 与 `writer-self-reports.md`：**实测**六个写手 + 判者的首条 user 消息就是那一条提示词（212 / 309 / 1194 字符）⇒ `fork` 会继承长篇上下文，故这条可复核 | §0.1 |
| M-10② | "写手是否读了别的文件"只有自报 | 在 §0 与 `writer-self-reports.md` 顶部**明确登记该局限**（无文件系统审计、无 syscall 记录；"自报一致 ≠ 已证"） | §0 · §0.1 |
| M-11 | §7 的"逐字节确定性重生成"没被重跑 | 该轮**跑了一次并把输出入库**（6 份图 blob 三方相同：入库件 / `HEAD:` / 重新生成） | §7 |

**一处与评审不符（以实测为准，已写明）**：评审说"灰色矩阵是 **R2** 的"。
实测**当前轮的 R1 与 R2 都没有矩阵面板**（R1 = 堆叠条 + 三元图；R2 = bars / scatter /
连续发散热图 / dendrogram）；带灰色矩阵的是**作废轮**的 R1/R3（其自报原文可查）。
评审这条的**方向**（R1 的第三箱是它自己的 `#f03b20` 分档色，不是灰色矩阵）成立，已按此改准。

**一处没修的（有意保留）**：`caption.txt` 仍不由 `make_figure.py` 再生（§7 末条）。
brief 只要求脚本"regenerates the figure"，这是已知缺口、且已逐条登记，不在该轮改动范围。

<<ROUND2>>
==============================================================================
§11 第二轮修复记录（评审 Needs fixes 后）—— 1 条 Important + 5 条 Minor
==============================================================================

起点 HEAD `5edbd20`。评审这 6 条**全部落在第一轮（§10）的收尾上**，没有新的事实错误。
逐条处置，每条都附**当场跑过的命令**。**与评审描述不符处，以实测为准并已写明。**

| # | 评审条目 | 处置 | 落点 |
| :- | :--- | :--- | :--- |
| **Imp-1** | `writer-self-reports.md` 是本目录**最完整的泄题件**（逐字含写手对 H1-H13 规范表的引述），而"绝不给写手"的警示头**只点名三份文件** ⇒ 枚举**读起来像穷举**，照它决定"什么能交给写手"的人恰好会漏掉最完整的那一份 | 警示头改成**四份并列点名**（含 `writer-self-reports.md`），并补一句"**这个点名不是穷举**：§2 的证据与工具两栏整体同样不给写手"；该文件**自己也加了警示块**（它可能被单独交出去）；`make-readme.py` 的 `HEADER` 同步改 | `README.md` 文首 · `writer-self-reports.md` 文首 |
| N-2 | `rescue-transcripts.py` 有**第二份提取循环**，在 `blob` 已构造**之后**才往 `out` 追加 ⇒ **结果被丢弃**；而它插的是**未脱敏**的 `prompt`/`handback` ⇒ 一次自然的重排（把 `blob` 那行下移）就会把绝对路径写进入库证据 | **整段删掉**死块（不留"待用"版本）；删后重跑，transcript 段**逐字节不变**（见 ④） | `rescue-transcripts.py` |
| N-3 | `make-briefs.py` / `make-readme.py` 用 **cwd 相对路径**，另四个脚本锚 `__file__` | 两个脚本都锚 `__file__`（输出路径同时改成**仓库相对**，与 `rescue-transcripts.py` 同款）。修前的两种坏法已实测复现（见 ②） | 两个脚本 |
| N-4 | 实施报告的 §7.2 与 §9-D 仍写探针 "2354 B"，而 §11.1/§11.3 已记 **1923 B** | 按**磁盘实测**（见 ①）把那两处改成 1923 B | 实施报告 `.superpowers/sdd/task-m3-t2-report.md`（**暂存区文件，不在本仓证据内**） |
| N-5 | §9-B 还留着一处**指向 gitignored 文件**的指针（"见实施报告"），而值已在 §0.2 内联 | 改成**指本文件 §0.2 的内联表**，并写明"**指针不许指向会被清理的地方**" | 本文件 §9-B |
| N-6a | 本文件**缺 §10**（§9 直接跳 §11） | 第一轮记录**改编号为 §10**（并注明"本节内的'本轮/该轮'一律指那一轮"），本文件收尾于 **§11 = 本节** | 本文件 §10 · §11 |
| N-6b | `writer-self-reports.md` 自称"本文件不含任何 `...` 式删节"，而文件里**确有 `...`** | 改成**准确说法**：本脚本**不施加**删节；文件里的省略号**全部在两段引用内部**、是原文作者自己的简写。处数按实测（见 ③） | `writer-self-reports.md` 文首 |

**一处与评审不符（以实测为准）**：N-6b 评审写"**四处** `...`（`:55`、`:140`、`:141`）"。
**实测 5 处**：`:55` ×2（作废轮 R1 的自报）+ `:140` ×2、`:141` ×1（作废轮 R3 的自报）
—— 修后行号变为 `:66` ×2 + `:151` ×2 + `:152` ×1。评审的**方向**（都在写手原文里、
不是我们删的）**成立**，条数按实测写成 **5 处**。修这条时**踩过一次自己的坑**：第一版改法
在文首的说明里**也写了 `...`**（举例如 `--fig .../figure.pdf`），使全文件处数从 5 涨到 9；
现改成**用文字描述省略号**，全文件仍是**只有那 5 处**（③ 就是重测）。

## 11.1 本轮当场跑过的命令与输出

**① N-4：探针在磁盘上的真实大小**

```
$ wc -c < tests/skills/figure-choose/red/multipage-probe.pdf
1923
```

（§6 / §9-D / `README.md` 记的本来就都是 1923 B —— 只有**实施报告**那两处还留着 2354 B，
那是**加生成器之前**那一版的字节数。报告已按实测改准。）

**② N-3：cwd 相对路径的两种坏法（修前实测）与修后实测**

修前 ①：在 `red/` 下跑 `make-readme.py` —— 以 cwd 找 brief，找不到就崩：

```
$ cd tests/skills/figure-choose/red && python make-readme.py
FileNotFoundError: [Errno 2] No such file or directory: 'tests\\skills\\figure-choose\\red\\brief-R1.md'
[exit=1]
```

修前 ②：在**别的 cwd** 下跑 `make-briefs.py` —— 不报错，**静默**把三份 brief 写进
`<cwd>/tests/...`（`mkdir(parents=True, exist_ok=True)` 让这失败无声）：

```
$ cd <TMP>/n3-scratch && python <REPO>/tests/skills/figure-choose/red/make-briefs.py
tests/skills/figure-choose/red/brief-R1.md  bytes=1122
tests/skills/figure-choose/red/brief-R2.md  bytes=2029
tests/skills/figure-choose/red/brief-R3.md  bytes=1230
tests/skills/figure-choose/red/out-R1/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R2/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R3/  (empty, awaiting writer)
[exit=0]
$ find <TMP>/n3-scratch
<TMP>/n3-scratch/tests/skills/figure-choose/red/brief-R1.md
<TMP>/n3-scratch/tests/skills/figure-choose/red/brief-R2.md
<TMP>/n3-scratch/tests/skills/figure-choose/red/brief-R3.md
```

修后：换 cwd 不再影响落点（`<REPO>` / `<TMP>` 是掩码，本仓规定不写绝对路径）：

```
$ cd docs && python ../tests/skills/figure-choose/red/make-briefs.py
tests/skills/figure-choose/red/brief-R1.md  bytes=1122
tests/skills/figure-choose/red/brief-R2.md  bytes=2029
tests/skills/figure-choose/red/brief-R3.md  bytes=1230
tests/skills/figure-choose/red/out-R1/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R2/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R3/  (empty, awaiting writer)
[exit=0]
$ git status --short docs
$ cd tests/skills/figure-choose/red && python make-readme.py
tests/skills/figure-choose/red/README.md  bytes=9724
[exit=0]
```

（`git status --short docs` **无输出** ⇒ 这次没有往 cwd 下写任何东西；三份 brief 的
blob 也与入库件相同 —— 见 ⑤ 的重跑。）

**③ N-6b：省略号的逐处计数（修后实测）**

```
$ python - <<'PY'
import pathlib
b = pathlib.Path("tests/skills/figure-choose/red/writer-self-reports.md").read_bytes().decode("utf-8")
tot = 0
for i, line in enumerate(b.splitlines(), 1):
    n = line.count("...")
    if n:
        tot += n
        print(f":{i}  count={n}  {line[:88]}")
print("TOTAL =", tot)
PY
:66  count=2  - `python tests/skills/figure-choose/check-figure-style.py --fig .../figure.pdf --captio
:151  count=2  - `python tests/skills/figure-choose/check-figure-style.py --fig .../figure.pdf --captio
:152  count=1  - Determinism: reran 3× and diffed bytes. First attempt was *content*-deterministic only
TOTAL = 5
[exit=0]
```

（三处**全部**在两段引用**内部**，都是写手自己写的简写；文首的说明里现在一个省略号也没有。）

**④ N-2：删掉死块后，抢救件的内容逐字节不变**

```
$ python tests/skills/figure-choose/red/rescue-transcripts.py <subagents 目录>
wrote tests/skills/figure-choose/red/writer-self-reports.md  bytes=30721  lines=328  masked_paths=15
$ python - <<'PY'
import pathlib, subprocess
SEP = ("=" * 78).encode()
def tail(b): return b[b.index(SEP):]          # 从第一条分隔线起 = 两段原文本身
new = tail(pathlib.Path("tests/skills/figure-choose/red/writer-self-reports.md").read_bytes())
old = tail(subprocess.run(["git","show","HEAD:tests/skills/figure-choose/red/writer-self-reports.md"],
                          capture_output=True, check=True).stdout)
print("tail bytes: new=%d old=%d  identical=%s" % (len(new), len(old), new == old))
PY
tail bytes: new=28270 old=28270  identical=True
[exit=0]
```

（**掩码处数仍是 15**，尾部 28270 B **逐字节相同** ⇒ 删掉那段死代码**没有**改变任何一个
入库字节。文件本身从 29906 → 30721 B，增量**全在脚本自己写的文首说明**上。）

**⑤ Imp-1：修后的点名清单（实测打印）**

```
$ python - <<'PY'
import pathlib
lines = pathlib.Path("tests/skills/figure-choose/red/README.md").read_text(encoding="utf-8").splitlines()
for i, l in enumerate(lines[:12], 1):
    print(f"{i:>3}| {l}")
PY
  1| # `red/` - RED 基线（无 skill 场景下的产物）
  2|
  3| > ## !! 本目录含泄题风险文件，绝不给写手 !!
  4| >
  5| > **点名（四份并列，没有"次要"档）**：`red-evidence.md` / `judge.md` / `README.md` /
  6| > **`writer-self-reports.md`**。它们写明了**期望的失败形态**（图宽比、配色数、图注形态、
  7| > 饼图那条规则）；其中 `writer-self-reports.md` 是**最完整**的一份 —— 它逐字含写手对
  8| > 规范表（H1-H13）的引述，以及"这些阈值我都知道"的自述。任何"写手" agent 一旦读到
  9| > 其中**任何一份**，产出的就不再是 RED 基线。
 10| >
 11| > **这个点名不是穷举**：第 2 节的**"证据"与"工具"两栏整体同样不给写手**，
 12| > 派写手时提示词只给**场景 brief 的路径**与**产物输出目录**。
[exit=0]
```

**⑥ 入库生成器重跑一遍，产物逐字节不变（本轮"可复现"的当场证据）**

```
$ git status --short tests/skills/figure-choose/red/            # 重跑前
 M tests/skills/figure-choose/red/README.md
 M tests/skills/figure-choose/red/make-briefs.py
 M tests/skills/figure-choose/red/make-evidence.py
 M tests/skills/figure-choose/red/make-readme.py
 M tests/skills/figure-choose/red/red-evidence.md
 M tests/skills/figure-choose/red/rescue-transcripts.py
 M tests/skills/figure-choose/red/writer-self-reports.md
$ python tests/skills/figure-choose/red/make-briefs.py
tests/skills/figure-choose/red/brief-R1.md  bytes=1122
tests/skills/figure-choose/red/brief-R2.md  bytes=2029
tests/skills/figure-choose/red/brief-R3.md  bytes=1230
tests/skills/figure-choose/red/out-R1/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R2/  (empty, awaiting writer)
tests/skills/figure-choose/red/out-R3/  (empty, awaiting writer)
$ python tests/skills/figure-choose/red/make-readme.py
tests/skills/figure-choose/red/README.md  bytes=9724
$ python tests/skills/figure-choose/red/make-evidence.py        # stdout 见脚注（自指数）
$ python tests/skills/figure-choose/red/rescue-transcripts.py <subagents 目录>
wrote tests/skills/figure-choose/red/writer-self-reports.md  bytes=30721  lines=328  masked_paths=15
$ git hash-object tests/skills/figure-choose/red/red-evidence.md
（重跑前后各跑一次，两次输出**逐字符相同** —— 值自指，按脚注不写死）
$ git status --short tests/skills/figure-choose/red/            # 重跑后
 M tests/skills/figure-choose/red/README.md
 M tests/skills/figure-choose/red/make-briefs.py
 M tests/skills/figure-choose/red/make-evidence.py
 M tests/skills/figure-choose/red/make-readme.py
 M tests/skills/figure-choose/red/red-evidence.md
 M tests/skills/figure-choose/red/rescue-transcripts.py
 M tests/skills/figure-choose/red/writer-self-reports.md
```

（重跑后的七行与重跑前那七行**逐行相同** ⇒ 改动的文件与个数都没变。）

**脚注（自指数，本文件唯一的"数不写死"处）**：`make-evidence.py` 的 stdout 打出的是**它正
在生成的这个文件自己**的字节数与行数。把这个数**写进本文件**就成了自指：写一次、文件变长、
数又变 —— 永远追不上。故本轮**不写死它**，改用"两次 `git hash-object` 输出相同"来证
"重跑逐字节不变"（hash 值**同样**是自指的，所以也只声明相等、不写值）。
**这不是"数字可以不实测"**：本文件其余每一个数都是当场跑出来的。

（重跑**没有**碰写手产物：三份 brief / 三份 `make_figure.py` / 六份图 / 三份 `caption.txt` /
`judge.md` / `f2-boxes.txt` / `multipage-probe.pdf` **全不在**那七行改动列表里。）

**⑦ 另外三个入库生成脚本也各重跑一遍**（本轮**没有改**它们，重跑是为了证明"本轮修复
没有破坏第二轮修复建立的可复现机制"）：

```
$ python tests/skills/figure-choose/red/f2-diagnose.py \
    tests/skills/figure-choose/red/out-R1/figure.pdf \
    tests/skills/figure-choose/red/out-R2/figure.pdf \
    tests/skills/figure-choose/red/out-R3/figure.pdf \
    --out tests/skills/figure-choose/red/f2-boxes.txt
wrote tests/skills/figure-choose/red/f2-boxes.txt  bytes=16801  lines=341
$ git hash-object tests/skills/figure-choose/red/f2-boxes.txt
e46f98b66c5cc9f47d75f98389bfac95d4497b61
$ git rev-parse HEAD:tests/skills/figure-choose/red/f2-boxes.txt
e46f98b66c5cc9f47d75f98389bfac95d4497b61        ← 与入库件相同

$ python tests/skills/figure-choose/red/make-multipage-probe.py --twice
wrote tests/skills/figure-choose/red/multipage-probe.pdf  blob=dc8697b00cffc526b61e86314679fefcf1a5eae6
pages = 2   file = multipage-probe.pdf   bytes = 1923
  page1: width=6.310 in -> ratio 1.000  |  彩色主色数 = 1
  page2: width=12.000 in -> ratio 1.902  |  彩色主色数 = 6
rerun  blob=dc8697b00cffc526b61e86314679fefcf1a5eae6  identical=True

$ python tests/skills/figure-choose/red/verify-reproducible.py
temp workdir: <TMP>/m3-t2-repro-1f23wn4b
--- out-R1: rc=0
      figure.pdf   committed_blob=a25d0a12bb80  regenerated_blob=a25d0a12bb80  (HEAD=a25d0a12bb80)  md5=38c92a1dbf44  identical=True
      figure.png   committed_blob=3ebb207af1a6  regenerated_blob=3ebb207af1a6  (HEAD=3ebb207af1a6)  md5=f5359942ff4a  identical=True
      caption.txt  committed_blob=b85515fdeb54  md5=2f69656eceee  regenerated=(absent)  identical=False
--- out-R2: rc=0
      figure.pdf   committed_blob=35b30acf7e51  regenerated_blob=35b30acf7e51  (HEAD=35b30acf7e51)  md5=64378431c7c3  identical=True
      figure.png   committed_blob=1bfcf8de4f95  regenerated_blob=1bfcf8de4f95  (HEAD=1bfcf8de4f95)  md5=3bc9c6c86770  identical=True
      caption.txt  committed_blob=24c07ec6a0a0  md5=364f98cfcd98  regenerated=(absent)  identical=False
--- out-R3: rc=0
      figure.pdf   committed_blob=db55c0a97986  regenerated_blob=db55c0a97986  (HEAD=db55c0a97986)  md5=da53a421045d  identical=True
      figure.png   committed_blob=49be5c44d92e  regenerated_blob=49be5c44d92e  (HEAD=49be5c44d92e)  md5=be19e6417d5c  identical=True
      caption.txt  committed_blob=8848b1ef4cee  md5=fbfd65f7e513  regenerated=(absent)  identical=False

RESULT: ALL FIGURES BYTE-IDENTICAL
```

（`f2-boxes.txt` 341 行 / 16801 B 与入库件**同 blob**；探针 blob `dc8697b00cff` 未变；
六份图的 blob 与 `HEAD:` **三方相同**。`caption.txt` 仍不由脚本再生 —— 那是 §7 已登记的
**已知缺口**，本轮同样**没有**顺手补，理由见 §10 末条。）
"""



def captions_block():
    """把三份图注的**字节**原样内联（顺带给出每条的字节点数，便于核对没被截断）。"""
    parts = []
    for n in (1, 2, 3):
        p = RED / f"out-R{n}" / "caption.txt"
        raw = p.read_bytes().decode("utf-8")
        parts.append(f"$ cat tests/skills/figure-choose/red/out-R{n}/caption.txt"
                     f"    # {len(p.read_bytes())} B\n{raw}\n")
    return "```\n" + "".join(parts) + "```\n"


def main():
    doc = DOC.replace("<<CAPTIONS>>", captions_block())
    assert "<<CAPTIONS>>" not in doc
    out = doc.encode("utf-8")
    p = RED / "red-evidence.md"
    p.write_bytes(out)
    rel = p.relative_to(RED.parents[3]).as_posix()             # 只打印仓库相对路径
    print(f"{rel}  bytes={len(out)}  lines={doc.count(chr(10))}")


if __name__ == "__main__":
    main()
