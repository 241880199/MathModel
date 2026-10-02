# `red/` —— RED 基线（`mcm-table` · **无规范**场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（三份并列）**：本 `README.md` / `writer-self-reports.md` / 上一级的
> `red-green-evidence.md`。它们写明了**判据**（`C1`–`C8`：编得过 · 三线结构 · 表题位置 · 表宽 ·
> 列数/空格子 · 同列精度 · 缺失值形态 · **来源回显**）与**对照结论**；`writer-self-reports.md`
> 还写明**派发口径**。任何"写手" agent 读过其中**任何一份**，产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：`out-R{n}/table.tex` 与 `caption.txt` 本身（别的写手的产物）、以及
> `out-R{n}/table.png`（判据渲染的证据件）**也不给写手**。派写手时提示词只给**场景 brief 的路径**
> 与**产物输出目录**（外加一件环境事实，见下）。

## 1. 这是什么

Task 3 的 RED 侧：**同一份场景、同一把尺**下，**没见过规范**的写手产出的**表**。
与上一级 `green/` 对照：GREEN 侧是**用本 skill 规范 + 判据**产出的同场景表。

- **场景（权威副本）**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`（本该是**图**的 brief）。
  本目录**不重复内联**那三份 —— 免得造第二份权威。派写手时把它们复制到仓外
  `<TMP>\m3-table-t3-red\` 的**副本**（**只改交付物那一节**：从"出一张图"改成"为论文做一张表
  （LaTeX 表格代码 + 英文表题）"；数据段与问题段**逐字保留** ⇒ 与另两支载体同场景可比），
  并**如实披露**写手看得到/看不到什么（见 `writer-self-reports.md` 文首）。
- **判据**：`tests/skills/table/check-table-style.py`，**一字未改**（工作树 blob == `HEAD` blob，
  见 `../red-green-evidence.md` §0）。
- **★ RED 是本任务的「自变量」**：`out-R{n}/table.tex` 与 `caption.txt` **本轮未改**
  （逐个 blob 与 `HEAD` 比对见 `../red-green-evidence.md` §0）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-R{n}/table.tex` | 写手产出的表片段（**无 preamble**、自包含；泄题风险件） |
| `out-R{n}/caption.txt` | 写手产出的表题文本（泄题风险件） |
| `out-R{n}/table.png` | **判据渲染**的证据件（`--png` · 150dpi 第 1 页）；**非写手产物**、非字节可复现 |
| `writer-self-reports.md` | 三个写手的**派发口径与自述**（⚠️ 泄题风险件，**控制者写的、本支未改**） |
| `README.md` | 本文件（⚠️ 泄题风险件） |

**对照表与判断层在上一级**：`../red-green-evidence.md`
（RED × GREEN 并列红绿表 · 逐判据判词 · `SKEL` 信息行 · RED 每条红的性质 · 两侧 `.tex` 并排 diff ·
亲眼看表）。**生成器**：`../make-evidence.py`（机器抽取；`write_bytes`、全 LF；判据清单**现取**、不写死）。

## 3. RED 之所以是 RED

- 三个写手都是**新起的干净上下文 agent**（**未用 `fork`**）。首条 user 消息 = 一条提示词本身，
  只含**两样 + 一件环境事实**：场景 brief 的路径 · 产物输出目录 · `pdflatex` 在 PATH
  （可选自编验证）。末尾一句**隔离句**（"Work only from that brief - do not read or write any
  other file."）。**未给**规范 / 本 skill / 判据 / 任何先例证据。
- **强度边界（照实）**：写手"只读了那一份 brief"这件事**只有自报、没有沙箱可证**；本支那份
  `writer-self-reports.md` 的提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**，
  **不是**从 transcript 文件里机器摘的 ⇒ **只有转录级忠实度声明**，没有逐字节保证。
- **★ 环境旁路的如实披露（删不掉的，不许省）**：写手是本机 Claude Code 的 agent，
  **会话级共享上下文里另有两处可见面** —— ① 可用 skill 列表里 `mcm-table` 那一行的**类别名**
  （"缺三线结构、表宽溢出、表题位置不对、来源没回显"）；② 项目记忆 `MEMORY.md`（模块名 + 工具面）。
  ★ 它们泄的是**"有这几类判据"**，**不是"判据的边界在哪"** —— 阈值、`T`/`D` 正文、
  **来源回显的注释格式**、表宽上限的来源（编译时的版心宽）、8 条判据 ID 与口径，写手**都看不到**。
  全文见 `writer-self-reports.md` 文首。

## 4. 与 GREEN 的比对口径

同场景（`brief-R{1,2,3}.md` 的数据）、同数据（逐字）、同一把尺（`check-table-style.py` 一字不改）。
**两侧都出编译渲染的 PNG**，证据里都登记；**不许**因为 GREEN 改善就调判据或换数据。
**★ 不许把 RED 的红读成"表烂"** —— 判据修掉两处假红（`bd97fd6`）后，
R1/R3 各只剩 `C8`（缺**来源回显**），R2 的 6 条里 **5 条是级联**自"双 `tabular` 超出单表射程"。
详见 `../red-green-evidence.md` §4。

## 5. ★ `out-R2/table.tex` 是 **CRLF** —— **自变量，永久保留**（2026-10-02 · Task 4 裁定）

**实测**：`out-R2/table.tex` 的**工作树与 `HEAD` blob 都含 56 个 `\r`**（CRLF，3169 B）；
`out-R1`/`out-R3` 是 LF（`\r` = 0）。复跑命令：
`python -c "import pathlib;d=pathlib.Path('tests/skills/table/red/out-R2/table.tex').read_bytes();print(d.count(b'\r'),len(d))"`。

**裁定：保留，不"解冻"**。理由 ① 它是**写手的真实产物**（本支的**自变量**）——
Task 3 已正确**未动**它，Task 4 复判**维持**：改它 = **改自变量 = 造伪**；
② 本仓"全 LF"纪律管的是**我们自己的写入**，管不着**冻结的输入件**；
③ 判据（`check-table-style.py` 用 `splitlines`）与生成器（`make-evidence.py` 用 `decode + splitlines`）
**都换行无关** ⇒ CRLF **不影响任何判据或对照读数**。
⇒ **登记为永久项**（不是"待解冻的作业"）：除非 RED 场景整体重做，**不要动它**。
