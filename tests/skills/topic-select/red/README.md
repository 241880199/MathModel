# `red/` —— RED 基线（`mcm-topic-select` · **无 skill** 场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（三份并列）**：本 `README.md` / `writer-self-reports.md` / 上一级的 `TOPICSELECT-evidence.md`。
> 它们写明了**判据**（`S1`–`S6`）与**对照结论**；`writer-self-reports.md` 还写明**派发口径**。
> 任何「写手」agent 读过其中**任何一份**，产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：`out-R{n}/decision.md` 与 `out-R{n}-shape/decision.md`（**别的**写手的产物）、
> `problems/**`（题面）与上一级 `green/`、`make-evidence.py`、`check-topic-select.py`、`mutate-topic-select.py`
> **也都不给写手**。派写手时提示词只给**brief 的路径** ＋ **题面目录** ＋ **产物输出目录** ＋ 一件环境事实。
>
> ★★ **一个例外（本目录里唯一"给写手看"的件）**：`neutral-shape.md` —— 它是**第二轮 RED 的起跑件**，
> 派写手时**必须**连同 brief 一起给（**它就是给写手看的**）。它不是泄题件：它**只给形状、不给纪律**
> （逐行判定见 §6）。**除它之外**，本目录其余件（含本 `README.md`）**一律不给写手**。

## 1. 这是什么

Task 3 的 RED 侧：**同一件事、同一把尺**下，**没见过本 skill 的正文**的三位写手产出的**选题决策**。
与上一级 `green/` 对照：GREEN 侧 = **用本 skill**（`SKILL.md` 契约 + `references/`）出的同一件事。

- **这件事（权威副本）**：`brief.md` —— **唯一一份**，RED 与 GREEN 逐字共用。
  ★ **它本身不是泄题件** —— 写手要看的就是它。
- **题面**：`problems/A.md` – `F.md` —— **2025 年美赛 A–F 的六份真实题面**，
  由 `tools/papers/taxonomy.extract_text`（`pdftotext -enc UTF-8`）从 `corpus/官方原题/2025/*.pdf` 抽出（**唯一口径**）。
- **判据**：`../check-topic-select.py`，**两侧同一版**（本支**不动**它；见 `../TOPICSELECT-evidence.md` §0）。
- **★ RED 是本任务的「自变量」**：`out-R{n}/decision.md` 是**写手的字节**，本轮未改
  （blob 见 `../TOPICSELECT-evidence.md` §0）。
- ★★ **两轮 RED（同一 brief，一个变量之差）**：
  - **第一轮（无形态）** = `out-R{1,2,3}/decision.md` —— 只给 **brief + 六份题面**。
    **结果**：三位写手**都没产出可比结构**（题小节 / 标签表 / 推荐行全 0）⇒ `S1`–`S4` **全在解析层 fail-closed**，
    **走不到"逐字 vs 改写"那一格** ⇒ **对 `S1` 的判别力提供不了证据**（但它证明了另一件事：**契约外产物一律 fail-closed**）。
  - **第二轮（有中性形态）** = `out-R{1,2,3}-shape/decision.md` —— 在 brief + 六份题面之外，**多给一份 `neutral-shape.md`**
    （**只有形状、不含纪律**的空壳；见 §6）。**目的**：让写手产得出**可比结构**，从而**才可能**走到 `S1` 的逐字那一格。
  - ★ **两轮都是真读数，都留**；各自证明了什么 / 不能证明什么见 `../TOPICSELECT-evidence.md` §10。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `brief.md` | **那件事本身**（唯一一份；RED 与 GREEN 共用；**不是泄题件** —— 写手要看它） |
| `problems/A.md` – `F.md` | 六份**真实题面**（2025 A–F；写手要看它） |
| `neutral-shape.md` | **第二轮的中性形态**（"只有形状、无纪律"的空壳；**不是泄题件** —— **第二轮写手要看它**；逐行判定见 §6） |
| `out-R{n}/decision.md` | **第一轮**写手产出的选题决策（无形态；**泄题风险件**） |
| `out-R{n}-shape/decision.md` | **第二轮**写手产出的选题决策（有中性形态；**泄题风险件**） |
| `writer-self-reports.md` | 写手的**派发口径与自述** + **环境旁路披露**（两轮都在此件；⚠️ 泄题风险件） |
| `README.md` | 本文件（⚠️ 泄题风险件） |

**对照表与判断层在上一级**：`../TOPICSELECT-evidence.md`
（RED × GREEN 并列红绿表 · 逐判据判词 · RED 每条红的性质 · 内容探针 · 「看一眼」替代品）。
**生成器**：`../make-evidence.py`（机器抽取；`write_bytes`、全 LF；判据清单**现取**、不写死）。

## 3. 三位写手是谁（派发口径见 `writer-self-reports.md` §0）

- 三个**新起的干净上下文** `general-purpose` agent，**未用 `fork`**。
- 首条 user 消息 = 一条**逐字相同**的提示词（只有 `out-R{n}` 不同）：只给 **brief 路径 + 题面目录 + 输出目录**，
  外加一件**环境事实**（"不需要联网"）；末尾一句**隔离句**（"Work only from that brief file and those six problem files"）。
- **未给**：本 skill 的**正文**（`SKILL.md` / `references/`）、`corpus/**`、判据、本任务书。
- **强度边界（照实）**：写手"只读了 brief + 六份题面"**只有自报、没有沙箱可证**
  （自报件是**转录级**、非机器抽取）。
- ★★ **环境旁路的如实披露**：写手是本机 Claude Code 的 agent，会话级共享上下文里**另有三处可见面** ——
  ① skill 列表里 `mcm-topic-select` 那一行的**描述**（**它点了名"分类 / 同型历史 / 四轴 / 推翻条件"**）；
  ② `git status` 快照（含 `.claude/skills/mcm-topic-select/references/method.md` 之类路径）；
  ③ **Recent commits**（五条 `m1-topic-select` 提交，其一标题提到「判据 `S1–S6` + 变异驱动器」）。
  ★ **本次这不是"没泄漏"**：旁路**实打实漏了**"要做哪几样"。当场用干净上下文探针查过、全文与**探针自身的边界**
  见 `writer-self-reports.md` §4。**登记在案**：本轮 RED **不是**"完全没见过本 skill"的基线。

## 4. ★ RED 的诚实边界（硬要求 6 / 设计 §3.2）

中性 brief **已经限定**"要**从六道题里挑一道，并说明为什么**"（必答项：挑一道 + 理由）
⇒ 这轮 RED **测不到"连推荐都给不出"那一类失败**（写不出任何选择、给不出理由）。**不声称覆盖全部失败模式。**

★ **不许把 RED 的红读成"选题决策做得差"**：三份 RED **都读得懂、都自洽、内容还都像样**
（都推荐了题 C，都给了理由、都在诚实清单里列了不确定处）。判据红的是**"没按本 skill 的契约产出"**
（缺机器可核的承重结构：`## 题 <字母>` 小节 · 标签表 · `- 历史：…` 行 · 四轴行 · `## 推荐` 节）。
详见 `../TOPICSELECT-evidence.md` §6、§7。

★★ **一条本轮特有的边界**：**2027 的题尚不存在**，而**任何真实可得的 MCM 题集（2016–2026）都已在语料里** ⇒
本轮选**真实旧题集 2025 A–F** ⇒ **复现不了**"当天新题刚放出、尚不在语料里"那一情形。
**本轮测的是形态/逐字纪律（`S1`）与判据本身，不是"新题不在语料里"那一情形。不声称覆盖真实赛期情形。**


---

## 5. 第二轮（有中性形态）—— 一个变量之差

- **同一件事（`brief.md` 逐字）、同一把尺（`../check-topic-select.py`）、同一组题面** ⇒ **唯一变量** =
  多给一份 `neutral-shape.md`（逐行判定见 §6）。
- 三个写手都是**新起的干净上下文** `general-purpose` agent（**未用 `fork`**）；首条 user 消息 = 下面这条提示词，
  **只有 `out-R{n}` 一个 token 不同**：

```text
Read the brief at <WS>/brief.md, the six problem statements in <WS>/problems/ (A.md, B.md, C.md, D.md, E.md, F.md), and the neutral shape (an empty shell) at <WS>/neutral-shape.md. Produce the deliverable the brief asks for, using that neutral shape as the shape for your document. Write your deliverable into <WS>/out-R{n}/. Work only from that brief file, those six problem files, and that neutral-shape file - do not read or write any other file.

Environment fact (not part of the brief): you do not need network access; work offline from your own knowledge and judgement.

When you are done, reply with a short self-report: which files you read, what you produced (file names and sizes), why you chose the problem you chose, and any issues you hit.
```

（实际派发用**绝对 Windows 路径**，`<WS>` = 仓内 `build/topic-select-red2/`（gitignore、**不落盘根**）；
三份件是仓内权威件的**副本**，派发前逐字节比对过；提示词原文与三份自述见 `writer-self-reports.md` §5。）

- **仍不给**：本 skill 正文（`SKILL.md` / `references/`）、`corpus/**`、判据、本任务书。
- **结果（机器抽取，见 `../TOPICSELECT-evidence.md` §3、§7.1）**：三位写手**都产出了可比结构**
  （每题一节 `## 题 <字母>`、标签表 12 行都填），`S1` **逐条判红 36 条支撑句**（**非子串 12 / 12 / 12**）
  ⇒ **第一次在 RED 里行使了 `S1` 的逐字判别力**。R1s/R2s 红 `S1,S2,S3,S4`；R3s 红 `S1,S2,S3`。
  ★ **第二轮的红与第一轮不是同一型**（第一轮全在"结构缺失"上读空；第二轮结构在、红的是内容与形态）。
- ★ **环境旁路**：与第一轮同型、**更重**（Recent commits 里多了点名「判据 `S1–S6` + 变异驱动器」的提交），
  **照实披露**见 `writer-self-reports.md` §5.4。

## 6. ★ 中性形态 `neutral-shape.md` —— 为什么长这样（逐行判定）

**它是第二轮 RED 的起跑件**（口径照 `mcm-schematic` 的 `neutral-skeleton.tex`：给写手一份"能用"的容器）。
**陷阱（照实说）**：写这份空壳的人**天然会想把它写成一份"模板"**；可模板里的**每一句提示都可能变成纪律**。
它在这里的作用是给写手一个**能填出可比结构的容器**，**不是**给一份"我们家的规矩"。故写完**逐行回读**，
对每一行问一句：**「这一行给出的是"长什么样"，还是"内容该怎么写"？」** 后者 ⇒ 删。

**逐行判定（下面这张表不声称穷尽，只逐条过一遍当天的每一行；表里的行只写"前缀/位置"，不内联竖线以免与表格本身打架）**：

| 行（只说形状，不抄全文） | 给出了什么 | 是"形状"还是"纪律" | 判定 |
| :--- | :--- | :--- | :--- |
| 题标题行（`## 题 <字母> — <题干词>`） | 一节一题的**标题形态** | **形状**（容器：让每道题各成一节） | **留** |
| 标签表**表头**（两列：`L1 · L2` 与 `支撑句`） | 两列表的**列名** | **形状**（只说有两列，不说列里写什么） | **留** |
| 标签表**数据行**（标记位 `核心`/`附带` + 粗体 `L1 · L2` + 引号句位） | 一行的**两格形态**（标记位 / 粗体位 / 引号位） | **形状**（给竖线两格的**骨架**，**不说这句从哪来**） | **留** |
| **组合历史行**（前缀 `- 历史：组合`；值全空） | 历史行的**格式** | **形状** | **留** |
| **模型历史行**（前缀 `- 历史：题`；值全空） | 历史行的**格式** | **形状** | **留** |
| **四轴行 ×4**（前缀 `- 轴 N ·` + `【<可核性>】`；内容空） | 四轴行的**格式**（四个、带方括号位；轴名与可核性**都空着**） | **形状**（只给"有四条这种行"，不给"是哪四轴 / 各标什么"） | **留** |
| **推荐节**（`## 推荐` + `- 推荐：` + `- 推翻条件：`） | 推荐节的**格式**（值空） | **形状** | **留** |
| **没有**：支撑句必须逐字来自当天题面 | —— | ★★ **纪律**（**正是 `S1` 要测的靶子**） | **不写** |
| **没有**：`核心` / `附带` 怎么分 | —— | **纪律**（`corpus-lookup.md` §1 口径） | **不写** |
| **没有**：`N` 怎么数（含不含 `附带` / 当天题） | —— | **纪律**（语料口径） | **不写** |
| **没有**：四轴各是哪四轴 / 各标哪种可核性（半可核 / 判断） | —— | **纪律**（`method.md` §1 / §5） | **不写** |

★ **一句话**：`neutral-shape.md` 里**有形状、无纪律** —— 它让写手**产得出可比结构**（第二轮实测：
六题各一节、标签表 12 行都填了），却**不告诉写手**"支撑句得逐字抄题面"（`S1` 的靶子）。
★★ **一处如实登记**：给写手的那份里**没有**"逐字"这条纪律 —— 这**不是疏忽，是本轮要测的东西**
（若给了，测的就不是"写手会不会自发逐字"，而是"写手听不听指令"）。
