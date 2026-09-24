# COMAP 官方材料索引与事实基线

本文件是美赛 skills 套件引用官方事实的**唯一入口**。任何 skill 中的规则断言都必须能追溯到这里。

- 建立日期：2026-09-22
- 材料目录：`corpus/official/`
- 引用写法：在 skill 中写「见 `corpus/official/INDEX.md` §2.3」这类指针，**不要**在 skill 里复述规则原文后不加指针

## §0 证据分级与引用约定

全文每条事实后标注一档**分级**（方括号内），必要时再附加**时效标记** `†`。三个轴**互相独立**，不得互相替代（轴三不是分级，见下）。

**轴一：分级（只表示来源，与时效无关）**

| 标记 | 含义 |
| :--- | :--- |
| `[官方]` | 官方原文（官网正文、官方 PDF、官方模板、官方 FAQ） |
| `[半官方]` | 官方平台转载，或官方人员表述 |
| `[社区]` | 业内共识、经验之谈，无官方出处 |

> 轴一还覆盖**推算**一类：由官方前提**推算**而得、官方无对应原文表述的，标 `[社区]` 并**注明推算依据**（实例：§2.6.5 的赛期总时长，出处栏写明"推算自 `instructions.html:804-806`"）。

> `[半官方]` 的实例（目前唯一一例）：`MCM-directors-overview` 是 **MCM Director 本人在 AMS 联合数学会议（JMM '21）上的报告**——报告人具官方职务、内容属"官方人员表述"，但该报告**不是** COMAP 的正式规则/政策文件，故不足以升为 `[官方]`，也绝不能降成"查不到出处"的 `[社区]`。

**轴二：时效标记（与分级并列使用）**

| 标记 | 含义 |
| :--- | :--- |
| `†` | 仅见于**非当年**官方材料（如 `MCM-ICM_Tips.pdf`，`V20240912`）而 2027 届 instructions 未重申。**来源仍为官方**，但须读题、并留意年份变化 |

> 例：`[官方]†` = "这条出自 COMAP 官方文件，但不是 2027 届的；合规上仍按官方要求执行，只是需临场复核年份口径"。**不得**因为"非当年"就把来源降为 `[半官方]`——降级会让下游 skill 把真要求误当成可选项。
>
> **分级不受影响**：`†` 是**时效**标记，与轴一正交，`[半官方]` 亦可叠加 `†`（实例：`MCM-directors-overview` 作 `[半官方]†`——官方人员表述，但材料出自 2021 年、非当年）。

**轴三：适用范围说明（**不是**分级，与轴一、轴二正交）**

有些官方来源**不承载硬性要求**——它们是背景、历史、经验类语料：三份 1994 年 MCM 文章（`experience`、`expertech`、`reflections`）、《20 Years of Good Advice》、以及《The UMAP Journal》24.3（2003）的评委自述。这类材料在**来源上仍是官方**（COMAP 出版物），因此：

- 分级按来源照写 `[官方]`；非当年者按轴二加 `†`；
- 另加**一句范围标注**，如「背景/经验语料，不承载硬性要求」；
- **不得**因为"它不是规则文档"或"它是旧文档"就改标 `[社区]`。

`[社区]` 的**唯一**含义是"查不到官方出处"（见轴一）。把"官方但非规则/非当年"写成 `[社区]`，是按**文档类别与时效**给**来源**打分，与"因为非当年就降为 `[半官方]`"是同一种混轴错误，且方向相反：前者会让下游 skill 把有官方来源的经验语料当成坊间传闻而随意处置。

> 例：`[官方]†` —— 背景/经验语料，不承载硬性要求（1994 年文章，非 2027 届规则文档）。

**例外规则的唯一落点**：本索引关于分级与时效的**全部**判断规则都写在本节（§0）。§1、§3、§4 只应用本节的规则，**不再各自另立例外**；若某处需要区别对待，须先在本节写明。

**引用格式**：`[官方] instructions.html:1230` —— 行号指 `corpus/official/` 下该文件的**原始文件**行号（HTML 文件指源 HTML，PDF 文件指已转出的同名 `.txt`）。

**使用纪律**：凡涉及评分与规则的断言，都必须能落到轴一的某一档上。**没有任何可回溯来源**的（既非官方、也非官方人员/官方平台表述、也非官方出版物）一律标 `[社区]`；来源是**官方人员表述**的可标 `[半官方]`（§4.1 的评分表即属此档），但**不得**因为它"看起来像官方标准"就升为 `[官方]`。理由见 §4。

---

## §1 材料清单

以下为 `ls -1` 的**实际**结果（含 pdftotext 转出的同名 `.txt`，与 `.pdf` 成对；`INDEX.md` 自身不计）。共 **21 个文件、13 份材料**（§1.1 六份 + §1.2 七份）。

### 1.1 事实基线来源（§2 的依据）

| 文件名 | 是什么 | 版本标记或日期 | 用于哪些 skill |
| :--- | :--- | :--- | :--- |
| `instructions.html` | **2027 届《Contest Rules, Registration and Instructions》正文** —— 竞赛规则、注册、指令的权威全文 | 2027 届（赛期 2027-01-28 ~ 2027-02-01；正文含 "Changes for 2027" 章节） | `mcm-selfreview`（合规组逐条）、`mcm-ai-disclosure`、`mcm-latex-format`、`mcm-playbook`、`mcm-paper-architecture` |
| `Contest_AI_Policy.pdf` / `.txt` | COMAP《Use of AI Tools in COMAP Contests》AI 使用政策全文，含披露格式范例 | `v102025`（文件首行右上角；页脚版权 ©2025） | `mcm-ai-disclosure`（主依据） |
| `MCM-ICM_Tips.pdf` / `.txt` | 《MCM-ICM: Procedures and Tips for a Great Experience》官方备赛与流程指南 | `V20240912`（文件首行） | `mcm-selfreview`、`mcm-latex-format`、`mcm-playbook` |
| `MCM-ICM_Summary.tex` | **官方 LaTeX 摘要页模板**（`article` 类 + `fancyhdr`，含摘要页与页眉骨架） | 文件头注释（`:3`）写 `2027 MCM/ICM`；摘要页标题栏（`:40`）渲染为 `2026 MCM/ICM Summary Sheet`（见 §3 冲突 4） | `mcm-latex-format`、`mcm-abstract` |
| `MCM-ICM_Summary.docx` | **官方 Word 摘要页模板**（与 `.tex` 同源） | 摘要页标题栏渲染为 `2027 MCM/ICM Summary Sheet`（**已更新到 2027**，与 `.tex` 不一致） | `mcm-latex-format`、`mcm-abstract` |
| `faq.html` | MCM/ICM 官方 FAQ，逐条问答 | 无显式版本号；正文引用 2027 赛期，判为当前版 | `mcm-selfreview`、`mcm-ai-disclosure` |

### 1.2 背景/参考语料（不承载硬性要求）

| 文件名 | 是什么 | 版本标记或日期 | 用于哪些 skill |
| :--- | :--- | :--- | :--- |
| `resources.html` | 官网 "Articles, Resources & Links" 页，列出官方文章、书籍与外部链接 | 无版本号 | 背景索引；`corpus/` 取材时定位用 |
| `20YearsofGoodAdvice.pdf` / `.txt` | 《20 Years of Good Advice》—— 多位资深评委/教练合著，讲评委实际关注点与常见失分 | 版式页眉作 `28 The MCM at 21`（`:55`、`:153`、`:258`、`:354`），可知属书《The MCM at 21》；**出版者作 `COMAP Inc.`（`resources.html:216`）；出版年份不详**（文内无年份信息，"约 2005 年"无从溯源） | `mcm-abstract`、`mcm-section-writer`（文风与内容范式提炼） |
| `experience.pdf` / `.txt` | 《The Voice of Experience》—— 历年指导教师经验汇编 | 《UMAP Tools for Teaching》1994 | 背景；`mcm-playbook`（备赛经验） |
| `expertech.pdf` / `.txt` | 《Experiencing the MCM at Northcentral Technical College》—— 单校参赛经验 | 同上，1994 | 背景 |
| `reflections.pdf` / `.txt` | 《Ten Years of MCM: Reflections of a Coach》—— 十年教练反思 | 同上，1994 | 背景；`mcm-playbook` |
| `UMAP-2003-judges-commentary.pdf` / `.txt` | 《The UMAP Journal》24.3（COMAP 出版）刊载的**2003 年 MCM 评委自述与当届题解** —— 含当年评审流程（triage 初筛 / Phase II）的第一手描述 | `UMAP Journal 24.3 (2003)` | 背景；`mcm-playbook`（评审流程认知） |
| `MCM-directors-overview.pdf` / `.txt` | **MCM Director 在 AMS 联合数学会议（JMM '21）的报告**《MCM Director's Overview of the Mathematical Contest in Modeling: What Advisors Need to Know》—— 含**终审示例评分表**（`A Sample Final Judging Rubric`）、初筛质量指标引文、组队与备赛建议 | 2021 年 2 月 4–8 日（`:4`、`:8`；页脚 `JMM '21`）；报告人 Steven B. Horton（MCM Director）、William C. Bauldry（MCM Associate Director）（`:4-10`） | `mcm-selfreview`、`mcm-playbook`；§4.1 的评分表依据 |

> 本表所列都是**背景/参考语料**：**不承载硬性要求**，其中的任何"要求"表述一律不得作为 2027 届规则使用。但**来源档位不同**，须分别标注——
> - `20YearsofGoodAdvice`、`experience`、`expertech`、`reflections`、`UMAP-2003-judges-commentary`：来源是 **COMAP 出版物** → `[官方]`（非当年者加 `†`）+「背景语料，非规则要求」；
> - `MCM-directors-overview`：来源是**官方人员的会议报告**（MCM Director 具官方职务，但该报告不是 COMAP 的正式规则/政策文件）→ `[半官方]†`（§0 轴一的"官方人员表述"）。
>
> 两者都**不得**改标 `[社区]`。分级与时效的判断规则**统一见 §0**，本处不再另立例外。

### 1.3 `UMAP-2003-judges-commentary` 中被核实的部分（背景语料，非规则要求）

该文件 427KB 全文中，与"评审"直接相关且可逐条定位的是下面这一处。**注意：这是 2003 年的情形，是否适用于 2027 届未知**，不得作为现行做法引用。

| # | 内容 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 1.3.1 | 当年评审分两阶段。**Phase I 为 triage 初筛**：通常每篇约 10 分钟阅读，按 1（最差）–7（最好）**主观打分**，约**前 40%** 送终审 | `[官方]†` —— 背景/经验语料，不承载硬性要求；2003 年情形，适用性未知 | `UMAP-2003-judges-commentary.txt:6540-6546` |
| 1.3.2 | **Phase II** 换场地、换评委：先校准轮，再按 1–7 制打分；随后评委**共同制定一个 100 分制尺度**用于 "bubble up" 更好的论文，再经四轮以上较长评审与讨论定稿 | `[官方]†` —— 同上 | `UMAP-2003-judges-commentary.txt:6548-6553` |
| 1.3.3 | 论文先在 COMAP 总部**去名编码**，再交两位 triage 评委预读；初筛以**摘要与整体组织**为判据，两评委分数分歧则协商，仍不一致由第三位评委裁定 | `[官方]†` —— 同上 | `UMAP-2003-judges-commentary.txt:568-574`（`The Results` 一节，起于 `:566`） |

> **该文件不含任何加权评分表**。在全文检索 `Executive Summary`、`rubric`、`100-point`、各评分项别名，均无流传的那份权重表（详见 §4.1）。1.3.2 出现的 "100-point scale" 指 Phase II 评委**现场自建**的排序尺度，正文未列出任何权重项与分值。
>
> 另见 §4.1 末段：该文件中有三条**定性**观察（摘要决定性、是否真做了建模、引用须在正文给页码）与多年公开表述一致，可作经验参考。

---

## §2 事实基线

### 2.1 页数与提交物范围

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.1.1 | 2027 届设 **25 页上限**，且该上限覆盖**整个提交物**：Summary Sheet、Solution、Reference List、Table of Contents、Notes、Appendices、Code 及任何题目特定要求 | `[官方]` | `instructions.html:918`（III. Changes for 2027） |
| 2.1.2 | **无最低页数**；无及格线或分数线；**接受 partial solutions**，鼓励完成尽可能多的部分 | `[官方]` | `instructions.html:1223`；`MCM-ICM_Tips.txt:216` |
| 2.1.3 | Table of Contents **鼓励使用且计入**页数上限 | `[官方]` | `instructions.html:1237` |
| 2.1.4 | Reference list / Bibliography、notes 页、任何附录**均计入**页数上限，且应排在正文之后 | `[官方]` | `instructions.html:1237`；`MCM-ICM_Tips.txt:200-203` |
| 2.1.5 | **唯一不计入 25 页的章节**是 `Report on Use of AI`（见 §2.4） | `[官方]` | `instructions.html:1239` |
| 2.1.6 | 部分题目自带**题目特定要求**（如要求的 memo 或 letter、特定解答格式、特定页数限制），须读题确认 | `[官方]†` | `MCM-ICM_Tips.txt:160-162`（`V20240912`）—— 仅见于 Tips，2027 instructions 未重申 |

### 2.2 摘要页（Summary Sheet）

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.2.1 | Summary Sheet **必须是 PDF 的第 1 页** | `[官方]` | `instructions.html:1302`；`faq.html:273` |
| 2.2.2 | 摘要**必须容于单页** | `[官方]` | `faq.html:270`（"it must be on a single page with a readable font (12)"） |
| 2.2.3 | 摘要页字体**可读且 ≥12pt** | `[官方]` | `instructions.html:955`、`1227`；`faq.html:270` |
| 2.2.4 | 摘要页内容须为**英文** | `[官方]` | `instructions.html:955`、`1227` |
| 2.2.5 | 不要单独发第二个文件装摘要；摘要就在同一个 PDF 内（同章 2.3.4） | `[官方]` | `instructions.html:1302`、`1309`；`MCM-ICM_Tips.txt:254-257` |
| 2.2.6 | 官方对摘要的权重表述：评委**极其看重**摘要，获奖论文常凭摘要质量与其余论文区分开 | `[官方]` | `instructions.html:1126`；`faq.html:227`（"It is unlikely the judges will read much beyond a poorly constructed summary"） |
| 2.2.7 | 官方明示的**弱摘要**：仅重述赛题，或从 Introduction 复制粘贴套话 | `[官方]` | `instructions.html:1132` |
| 2.2.8 | 官方建议**最后写摘要**，且须突出最重要的结论 | `[官方]` | `instructions.html:1131` |
| 2.2.9 | 摘要页 **`Problem Chosen` 栏须填所选题目**（MCM A/B/C 或 ICM D/E/F 之一），**不得**保留官方模板的占位符 `ABCDEF`（保留即等于"题号未填"，与队号栏留 `1111111` 同性质） | `[官方]` | `MCM-ICM_Summary.tex:39`（`Problem Chosen` 栏，值即 `\Problem`）；`:53`（模板红字 "Be sure to change the control number **and problem choice** above"） |

### 2.3 页眉、匿名与文件格式

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.3.1 | **每页**都必须在**页面顶部**含队号与页码，使用页眉。官方给出示例：`Team # 0000000, Page 6 of 25` | `[官方]` | `instructions.html:1230-1231` |
| 2.3.2 | **全文任何一页**都不得出现学生姓名、指导老师姓名、学校/机构名；除队号外**不得含任何可识别信息** | `[官方]` | `instructions.html:954`、`1308`；`MCM-ICM_Tips.txt:233-235` |
| 2.3.3 | 不得包含任何形式的队伍身份标识（学生名、机构名、**地理区域**）；若题目要求附信，**信尾也不得签名**，官方建议落款写 `Sincerely, Team #2000000` | `[官方]†` | `MCM-ICM_Tips.txt:233-246`（`V20240912`）—— 仅见于 Tips，2027 instructions 未重申（其 2.3.2 的匿名要求本身是 `[官方]`） |
| 2.3.4 | 全部解答须在**一个 Adobe PDF 文件**内提交，含正文、图、表与支撑材料；**文件名为队号**，如 `0000000.pdf` | `[官方]` | `instructions.html:955`、`1298`；`MCM-ICM_Tips.txt:254-257` |
| 2.3.5 | 字体可读且 **≥12pt**；全文**英文** | `[官方]` | `instructions.html:955`、`1227` |
| 2.3.6 | 页面尺寸须为 **US Letter 或 A4** | `[官方]†` | `MCM-ICM_Tips.txt:210` —— **仅见于 Tips V20240912**，2027 届 instructions 未重申 |
| 2.3.7 | PDF 附件**必须小于 25MB** | `[官方]` | `instructions.html:1298`；与 Tips 的 20MB 冲突见 §3 冲突 1 |
| 2.3.8 | COMAP **只接受 Adobe PDF**；**每份提交表单限一份 solution** | `[官方]` | `instructions.html:1309` |
| 2.3.9 | **不得**随解答提交程序、软件、数据库或其他非论文文件（不会被用于评审） | `[官方]` | `instructions.html:1227`、`1305`；`MCM-ICM_Tips.txt:211-213` |
| 2.3.10 | 解决办法不得包含除书面文字与图、表、图版之外的支持材料 | `[官方]†` | `MCM-ICM_Tips.txt:211-213`（`V20240912`）—— 仅见于 Tips，2027 instructions 未重申 |

### 2.4 Report on Use of AI（对本项目有直接约束力）

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.4.1 | 触发范围为**一切 AI 辅助技术**：LLM、生成式 AI、**数学软件**、**翻译软件**、代码补全/自动补全等。政策明确适用于从研究、模型开发（含写代码）到书面报告的各个环节，**甚至包括把队伍母语译成英文** | `[官方]` | `Contest_AI_Policy.txt:5-11` |
| 2.4.2 | **双位置披露**：① 正文内 inline citation + 在 References 章节列出所有所用 AI 工具；② 在 25 页正文**之后**追加独立章节 | `[官方]` | `Contest_AI_Policy.txt:54-58`；`instructions.html:1216`、`1239` |
| 2.4.3 | 该章节**置于 25 页之后**、**无页数上限**、**不计入 25 页** | `[官方]` | `instructions.html:1239`；`Contest_AI_Policy.txt:81-83`；`MCM-ICM_Tips.txt:204-207` |
| 2.4.4 | 章节标题用 **`Report on Use of AI`**（不是 `...AI Tools`），理由见 §3 冲突 3 | `[官方]` | `instructions.html:1216`、`1239` |
| 2.4.5 | 披露须含**工具名 + 版本/日期 + 模型名**，并说明**用途**。**模型名以"该工具确有模型"为限**：官方原文只说 "including **which model was used** and for what purpose"（`Contest_AI_Policy.txt:54-57`）；范例 2、3 确有模型故写出（`ChatGPT-4`、`Ernie 4.0`），而范例 1（Baidu Fanyi）与范例 4（GitHub CoPilot）**均无模型名**，只给版本/日期。故**无独立模型名的工具（纯翻译软件、部分代码补全/自动补全工具等）以版本/日期充该字段即合规**，**不得**因其缺模型名判为不合规 | `[官方]` | `Contest_AI_Policy.txt:54-57`、`90-102`（范例；其中 `:90`、`:101` 为无模型名两例） |
| 2.4.6 | **默认**要求非翻译用途给出 **Query 原文**与 **Output 全文**（范例 2 `:93-95`、范例 3 `:97-99`）；**翻译用途只需一句声明**，不必附完整输入（`:83-85`，范例 1 `:90-91`）。**例外**：官方范例 4（代码补全 `:101-102`）只给陈述式、未附 Query/Output，故本项**不是绝对口径**——凡工具本身**无离散 Query** 者（纯翻译软件、行内自动补全/代码补全），给一句陈述式即可。判据见 §3 伪冲突 7 | `[官方]` | `Contest_AI_Policy.txt:83-86`、`90-102` |
| 2.4.7 | 队伍须自行核验 AI 生成内容与引用的准确性、有效性、适当性，并改正错误与不一致 | `[官方]` | `Contest_AI_Policy.txt:60-61` |
| 2.4.8 | 未披露的后果：官方原文 "COMAP will take appropriate action when we identify submissions likely prepared with undisclosed use of such tools"；未加标注的段落更易被判为抄袭并取消资格 | `[官方]` | `Contest_AI_Policy.txt:17-19`、`70-73` |
| 2.4.9 | 官方把 AI 用途分两侧：**认可**（生成结构初想、summarizing、paraphrasing、language polishing）；**建议谨慎**（模型选择与构建、辅助写代码、解释数据与模型结果、得出科学结论） | `[官方]` | `Contest_AI_Policy.txt:21-27` |

### 2.5 评审导向

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.5.1 | 官方 **FAQ 不给评分表**：把"评审标准"问题直接指向 instructions 中的指引清单，而非任何评分表。**注意**：这不等于"COMAP 从未公开过任何评分表"——见 2.5.5 | `[官方]` | `faq.html:235-236` |
| 2.5.2 | 官方明示评委首要关注：**思维过程、对问题的分析、建模方法、数学方法** | `[官方]` | `instructions.html:1223` |
| 2.5.3 | 官方给出的论文内容清单（10 条）：目录 → 问题重述 → 变量与假设的清晰陈述 → 假设的合理性与论证 → 问题的分析（论证模型动机）→ 正文只放推导/计算摘要，冗长部分入附录 → **模型设计，并讨论如何检验：误差分析、灵敏度、稳定性** → **讨论模型或方法的明显优缺点** → 结论并明确报告结果 → 记录资源与参考文献 | `[官方]` | `instructions.html:1140`（目录）、`1143`（问题重述）、`1155`（推导入附录）、`1159`（模型设计与检验）、`1162`（优缺点）、`1165`（结论）、`1168`（文献） |
| 2.5.4 | 官方对优秀论文的描述：含 assumptions with justifications、modeling process、results、strengths and weaknesses、sensitivity、conclusions 等章节，并有 inline documentation / footnotes / endnotes 与配套参考文献 | `[官方]†` | `MCM-ICM_Tips.txt:51-56`（`V20240912`）—— 仅见于 Tips，2027 instructions 未重申；但内容与 §2.5.3 的 `[官方]` 清单一致 |
| 2.5.5 | **终审轮存在一份 COMAP 官方人员公布的"示例评分表"**（`A Sample Final Judging Rubric`）：Executive Summary 10 / Assumptions & Justification 15 / **Model / Value Added 40** / Sensitivity, Strength & Weakness 15 / Required Documents 10 / Clarity of Writing 10 = **Total 100**。**但官方原文明确限定**：它是 "**A Sample**" / "**A starting rubric**"，"The panel of Final Judges creates a rubric to fit their particular problem **adjusting categories and points as needed**"——即**终审评委团会按题目调整类别与分值**；且它管的是**终审（Final Judging）**，不是初筛 | `[半官方]†`（MCM Director 的 JMM '21 报告） | `MCM-directors-overview.txt:271-281`（小节标题 `Final Judging: The Final Judging Rubric` 见 `:269`；"A starting rubric" 句见 `:273-274`） |
| 2.5.6 | 该报告另引当年初筛口径 "Key quality indicators in team papers include: proper applications of mathematics and science, depth of exploration, completeness of a recognized modeling process, proper reliance upon and documentation of supporting research, innovative and insightful modeling approaches, and clear and concise exposition"（引自 `2018 MCM Problem A Triage Judging Guidelines`） | `[半官方]†` | `MCM-directors-overview.txt:256-266` |
| 2.5.7 | 官方以 **`must`** 写死**记录来源**义务：`Teams must document any outside sources of information by using footnotes, endnotes, or in-line documentation, and include appropriate citations in a reference list or Bibliography of these sources.` —— 即**两件都要**：① 用**足注／尾注／正文内标注**标出每一处外部来源，② 在**文献表或参考书目**中给出对应条目。与 2.5.3 第 10 条的关系：`instructions.html:952` 是 **`must` 的硬性义务**（规定了**标注形态**与**两处都要**），`instructions.html:1168` 只是 "Overall" 内容清单里的一项（`Document resources and references.`，**内容项**、不表述强度）——**1168 不能替代 952**，引用硬性义务时指针须落在 952 上 | `[官方]` | `instructions.html:952` |

> 注 1：2.5.3 的十条清单在 `instructions.html:1136-1168` 的 "Overall" 有序列表中，逐条可 grep。
>
> 注 2（**重要限定**）：2.5.5 的评分表**不得**被当成固定权重公式引用。skill 中如要使用，必须①标 `[半官方]`、②带上"A Sample / 可按题目调整"的限定语、③不得写成"模型占 40%"这类定论。可用的只是**相对重要性的参考信号**——Model / Value Added 一项独大（40），Assumptions & Justification 与 Sensitivity, Strength & Weakness 各 15——这与 2.5.2、2.5.3 的官方侧重一致。详见 §4.1。

### 2.6 赛制与时间（2027 届，均 EST）

| # | 事实 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 2.6.1 | 报名/缴费截止：**2027-01-28 15:00**；逾期不接受，无例外 | `[官方]` | `instructions.html:803`（Registration Deadline）、`981`（All teams must be registered before）、`936`（Advisors must register teams prior） |
| 2.6.2 | 开赛：**2027-01-28 17:00**；停止修改：**2027-02-01 20:00**；提交截止：**2027-02-01 21:00** | `[官方]` | `instructions.html:804`（Contest Starts）、`805`（Contest Ends）、`806`（Solution Report Deadline） |
| 2.6.3 | 六题方向：MCM A / B / C、ICM D / E / F，任选其一，只提交一题 | `[官方]` | `instructions.html:1112`、`1115` |
| 2.6.4 | 队伍 ≤3 名**同校**在读本科（或以下）学生；报名费 $100/队；开赛后不得向队外任何人求助 | `[官方]` | `instructions.html`（IV. Contest Rules，`936` 起） |
| 2.6.5 | 赛期**总时长**：2027 届官方文件（`instructions.html`、`faq.html`、`resources.html`、`MCM-ICM_Tips.txt`、`Contest_AI_Policy.txt`）**均未直接给出**总时长。**由官方时间点推算**：开赛→停止修改 = **99 小时**（`:804` → `:805`）；开赛→提交截止 = **100 小时**（`:804` → `:806`）。**推算值，非 2027 届官方原文表述** | `[社区]` | 推算自 `instructions.html:804-806` |
| 2.6.6 | **旁证**：COMAP 官方人员的材料里把赛期称作 "the **100-hour** weekend contest period"（述 2020 年赛制） | `[半官方]†` | `MCM-directors-overview.txt:33` |

> 2.6.5 / 2.6.6 的说明：时长是有用信息，但 2027 届官方原文并未给出这句话，故 2.6.5 只作 `[社区]` 级推算值，**不得**当作官方口径引用。前版此处曾写一个总时长并标 `[官方]`，该数值既与 `:804-806` 的时刻不符、又来自 `corpus/official/` 之外的来源，违反本项目的来源约束，2026-09-22 已删去并改为上表的推算值。2.6.6 的 "100-hour" 是**官方人员口径的旁证**（与推算的 100 小时一致，且进一步否定了那个既不存在的旧数值），但它述的是 2020 年赛制，**不等于** 2027 届的官方表述，故同样不能升为 `[官方]`。

---

## §3 官方冲突登记

同一官方渠道内部不自洽。分两组处理：**真冲突**必须**选定一侧并注明**，不得两说并存；**伪冲突**只是表面矛盾，须**澄清**（说明两条各管什么），**不是二选一**。

### 3.1 真冲突（须选边）

| # | 冲突项 | 说法 A（来源） | 说法 B（来源） | 本项目采用 | 理由 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **PDF 附件大小上限** | **< 25MB**（`instructions.html:1298`，2027 届正文） | < 20MB（`MCM-ICM_Tips.txt:258`，`V20240912`） | **A：25MB** | A 是 2027 届年度正文，B 是 2024-09 版指南且明确自述"accompanies, but does not replace"官方规则。履约时按更严的 20MB 留余量即可，但**规则口径写 25MB** |
| 2 | **MCM A/B 主题** | **A = continuous，B = discrete，C = data insights**（`MCM-ICM_Tips.txt:152-154`，六题逐条分类的正式列表） | A = discrete，B = continuous，C = data insights（`MCM-ICM_Tips.txt:61`，同文件行文顺带举例） | **A：A=continuous，B=discrete，C=data insights** | 冲突发生在**同一份文件内部**（Tips `V20240912` 第 61 行 vs 第 152-154 行）。**取 A 侧**是因为 `:152-154` 是"六题逐条分类"的正式列表（A/B/C/D/E/F 六条逐项列出，每条带括号主题），且与设计文档 §2.1 所载 comap.org 主页一致；`:61` 是正文顺带举例，可信度较低。**旁证**：COMAP 官方人员的材料亦作 "A-Continuous, B-Discrete, C-Data Insights"（`MCM-directors-overview.txt:33`，`[半官方]`），与 A 侧一致。→ 结论：**A 侧即正式列表侧** |
| 3 | **AI 章节标题** | **`Report on Use of AI Tools`**（`Contest_AI_Policy.txt:57-58`、`81-82`、`88`） | `Report on Use of AI`（`instructions.html:1216`、`1239`；`MCM-ICM_Tips.txt:204`） | **B：`Report on Use of AI`** | B 出现于更新的年度正文（2027 instructions）**且**得到 Tips 佐证，2 票对 1 票。**本章节标题的规则只以 `corpus/official/` 内的原文为准**；任何第三方排版宏包的内建环境名或命令名，均**不在本目录语料内**，本索引**不为**任何此类断言背书——需要时请查该宏包自己的官方文档。（本条原先旁涉某宏包的内建环境名，因无 `corpus/official/` 内出处，已于 2026-09-22 删去） |
| 4 | **官方 LaTeX 模板年份** | 文件头注释写 `2027 MCM/ICM`（`MCM-ICM_Summary.tex:3`） | 摘要页标题栏渲染为 `2026\ MCM/ICM\ Summary Sheet`（`MCM-ICM_Summary.tex:40`） | **使用模板，但手工把摘要页标题栏年份改为 2027** | `.tex` 自身不自洽。旁证：同源 `.docx` 的标题栏**已更新为 2027**，说明 `.tex` 的标题栏是漏改，改 2027 是正确方向。**另注**：`.tex` 的页眉写 `Team \Team`（左侧，`MCM-ICM_Summary.tex:23`）与 `Page \thepage`（右侧，`:69`），即**队号 + 页码**，**已满足 §2.3.1 的硬性要求**，无须改动、更无须"补足"。官方原文（`instructions.html:1230`）的硬性要求只有一句——"Each page of the solution must contain the team control number and the page number at the top of the page"，其后的 `Team # 0000000, Page 6 of 25`（`instructions.html:1231`）是 "for example" 引出的**示例文字，非强制**；`of 25` 亦然。**不得**据 `of 25` 判定模板不合规，也不得据此要求 `mcm-latex-format` 补足页眉 |

### 3.2 伪冲突（须澄清，非二选一）

这一组（#5、#6、#7）的结论**不是**"选一侧"——恰恰相反，两侧**同时成立**，因为它们约束的对象不同。skill 引用时须照"澄清结论"栏陈述，**不得**把它们与 §3.1 的真冲突并列、更不得擅自选边。

| # | 表面冲突项 | 说法 A（来源） | 说法 B（来源） | 澄清结论 | 依据 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 5 | **1/28 当天的截止时点** | 报名/缴费截止 **15:00 EST**（`instructions.html:803`、`:936`、`:981`） | 队员名单可提交至 **17:00 EST**（`faq.html:213`） | **两者并存，非冲突**：A 管"队伍注册与缴费"，B 管"队员名单录入"（17:00 即开赛时刻）。记为**两个独立截止时点** | 两条约束的对象不同。B 与 instructions "Not later than the opening of the contest window, advisors must assign team members" 一致。设计文档 §2.6 曾将其列为"冲突 5（A=15:00 / B=17:00）"，本索引据实际原文修正 |
| 6 | **页眉示例写法** | `Team # 0000000, Page 6 of 25`（`instructions.html:1231`） | `Team # 321  Page 6 of 13`（`MCM-ICM_Tips.txt:227`） | **示例文字本身非强制**：硬性要求只有"**每页**含**队号 + 页码**"（`instructions.html:1230`）。项目采用 A 的写法，但 B 不算违规 | A 为 2027 届正文给出的示例且与 25 页上限自洽；B 是旧指南示例（13 页），仅用于说明"格式长这样"。两者都不构成第二条规则 |
| 7 | **非翻译用途是否必须给 Query + Output** | 非翻译用途须给 **Query 原文 + Output 全文**（由 `Contest_AI_Policy.txt:83-84` 反推：官方**只**对翻译用途豁免 "your full input query"） | 官方范例 4（GitHub CoPilot，代码补全）**只给一句陈述式**，无 Query、无 Output（`Contest_AI_Policy.txt:101-102`） | **两者并存，非冲突**：A 管**有离散提示词与文本输出**的生成式用途——那里 Query+Output 是默认披露形态，范例 2、3（`:93-99`）即此形态；B 管**工具本身不产生离散 Query** 的用途——行内自动补全/代码补全根本没有"输入的提示词"这一步。`Contest_AI_Policy.txt:84` 豁免的对象恰是 "your full **input query**"，说明该条规范的是"**有 query 时如何披露**"，而非"一切非翻译用途都必须造出一个 query"。两条约束的**披露形态**不同（有 query 者给 query，无 query 者给陈述），故**非二选一** | `Contest_AI_Policy.txt:83-86`、`93-99`、`101-102`；且 `:85-86` 的 "Examples (**this is not exhaustive** — adapt these examples to your situation)" 明确把范例定位为**可据情况调整的示例**，即范例 4 不构成对 `:83-84` 的修订，两者各管一形态 |

> **冲突 7 对 `mcm-ai-disclosure` skill 的判据（明确结论，落地照此执行）**：
> 1. 凡 AI 工具的交互形态**存在离散提示词（prompt）与文本输出**（LLM 对话、生成式文本），**必须**给 Query 原文 + Output 全文——照范例 2、3（`Contest_AI_Policy.txt:93-99`）。
> 2. 凡工具**不存在离散 Query**（纯翻译软件、行内自动补全/代码补全），给**一句陈述式**即可——翻译照范例 1（`:90-91`）、代码补全照范例 4（`:101-102`）。
> 3. **不得**把第 2 条扩张为"只要队伍自认为没有 query 就可以省 Query"。是否"无离散 Query"取决于**工具本身的交互形态**，不取决于队伍的选择；把 LLM 对话式使用写成一句陈述式而省去 Query/Output，仍属披露不足，按 §2.4.8 有被认定抄袭并取消资格的风险。

---

## §4 流传说法与评分依据的核查

### 4.1 100 分制"官方评分权重表" `[半官方]` —— **真实存在，但被误传为"固定权重公式"**

**流传内容**：一份 100 分制 rubric —— Executive Summary 10 / Assumptions 15 / Model 40 / Sensitivity 15 / Documents 10 / Clarity 10，常被说成"COMAP 官方评审标准"，并被当作固定权重公式使用。

**核查结论三要点，缺一不可：**

1. **它确实是 COMAP 官方材料，不是伪造、也不是"来源未证实"。** 出处是 **MCM Director 在 AMS 联合数学会议（JMM '21）上的报告**《MCM Director's Overview of the Mathematical Contest in Modeling: What Advisors Need to Know》（2021 年 2 月；报告人 Steven B. Horton，MCM Director；William C. Bauldry，MCM Associate Director）。原文标题即 `A Sample Final Judging Rubric`，六大类与分值逐项列出，`Total 100`：Executive Summary 10 / Assumptions & Justification 15 / **Model / Value Added 40** / Sensitivity, Strength & Weakness 15 / Required Documents 10 / Clarity of Writing 10。该文件已收入本目录（见 §1.2），可逐条 grep：`MCM-directors-overview.txt:271-281`。
   > **历史更正**：本索引前版把这条定级为"已证伪"、中间版又改称"来源未证实"，**两次都错**。2026-09-22 找到原文后改定 `[半官方]`（官方人员表述，见 §0）。
2. **但官方明写它是 "A Sample" / "A starting rubric"——不是固定权重公式。** 原文："The panel of Final Judges creates a rubric to fit their particular problem **adjusting categories and points as needed**. **A starting rubric** appears below."（`:273-274`）即**终审评委团会针对具体题目调整类别与分值**。因此**不得**表述成"模型占 40%"这类定论，也不得把它当成每年不变的评分标准。该表出自 2021 年，是否沿用至 2027 届**未获确认**。
3. **它管的是 Final Judging（终审轮），不是初筛。** 小节标题为 `Final Judging: The Final Judging Rubric`（`:269`）。只有极少数论文走到终审；初筛是完全不同的一轮（2003 年的初筛情形见 §1.3）。用它推断"每篇论文都会按这六项打分"是错的。

**可用作**：**相对重要性的参考信号**——Model / Value Added 一项独大（40），Assumptions & Justification 与 Sensitivity, Strength & Weakness 各 15。这与 §2.5.2、§2.5.3 所列的官方侧重（思维过程、建模方法、对模型的检验与优缺点讨论）一致，可相互印证。**但不可当公式**：任何 skill 引用它时都必须①标 `[半官方]`、②带上"A Sample / 可按题目调整"的限定语、③不得给出"某项占百分之多少"的定论式表述。

**对本项目的强制约束**：任何 skill 中出现的评分相关内容**都必须带证据分级**；本条的可用分级只有 `[半官方]`。这正是 §0 分级制度存在的直接理由。

**附：一条曾被误挂到别处的归因，现已澄清。** 该表常被说成出自 **2003 年《UMAP Journal》评委自述**——**经检索不成立**：`UMAP-2003-judges-commentary` 已在本目录，在 427KB 全文中检索 `Executive Summary`、`rubric`、`100-point`/`point scale`/`scoring` 及各评分项别名，**没有任何一处以"评分项 + 分值"的形态出现**（`rubric` 命中 0 次；`Executive Summary` 全文仅 1 处，出现在与本表无关的参考书目条目里；`Assumptions` 等的出现都在所刊载的学生论文正文中）。该文件里确实出现过 "100-point scale"（`:6548-6553`），但那指的是 Phase II 评委**现场自建的排序尺度**，正文未列任何权重项与分值。**真正的出处是上面第 1 点的 JMM '21 报告。**

**另有一组来自 2003 年评委自述的定性观察**（文件已在本目录，见 §1.3）：摘要决定性极大（`:6560-6563`）；评委最先找的是"是否真的做了建模"而非"查几条公式硬套"（`:6570-6573`）；引用须在**正文中**给出具体页码，仅末尾参考文献表不足（`:6530-6531`）。这些与多年公开表述一致，可作经验参考；但都是 **2003 年**评委的经验陈述，**是否适用于 2027 届未知**，分级见 §1.3（`[官方]†` + 背景语料范围标注），**不标 `[官方]` 硬性要求**。

**证据状况汇总**：本条的**原文现在就在 `corpus/official/` 内**，是**可 grep 自证**的（这是它与前版最大的差别——前版以为原文不在本地，只能说"未证实"）。相关流传记录另见 `docs/superpowers/specs/2026-09-22-mcm-skill-suite-design.md` §2.7 / §2.8。

### 4.2 其他须提防的旧文档表述 —— 背景/经验语料，不承载硬性要求

（本节含两档来源：`[官方]†` 的 COMAP 出版物语料，与 `[半官方]` 的官方人员报告；两者的分级规则均由 §0 轴一/轴二给出。）

`corpus/official/` 中的三份 1994 年文章（`experience`、`expertech`、`reflections`）、《20 Years of Good Advice》、《The UMAP Journal》24.3（2003）的评委自述，描述的都是**当年**的赛制与评审。

它们的**来源都是 COMAP 官方出版物**，所以按 §0 分级仍写 `[官方]`，非当年者加 `†`；"不承载硬性要求"是**适用范围说明**，与分级正交。其中的页数、提交方式、奖项设置、评审流程（如 §1.3 的 triage 做法）等一律**不得**作为 2027 届依据；仅可用于提炼**写作与建模方法论**。

`MCM-directors-overview`（JMM '21，2021 年）同样**非 2027 届文件**，其分级为 `[半官方]†`（官方人员表述，见 §0）。它是本目录中唯一给出评分类别与分值的材料，但如 §4.1 所述**只能用相对重要性参考、不能当固定公式**；其中述及 2020 年赛制的数字（如 "100-hour"、13,700 支队伍）也**不得**当作 2027 届的数据。

---

## §5 校验记录（Step 3）

在 `corpus/official/` 下对简报指定的四个字符串逐条 grep，结果如下（`grep -rl`，即列出命中文件名）。下表已滤去 `INDEX.md` 自身——本索引复述了这四个字符串，故它必然出现，无验证价值；未滤去的原始输出另见 `tests/results/task1-index-verification.md`（**受版本控制**；此前指向 `.superpowers/sdd/task-1-report.md`，但 `.superpowers/sdd/.gitignore` 内容为 `*`、该目录整片不受版本控制，故 2026-09-22 把原始输出挪入 `tests/results/` 并改指针）：

```
25 page limit -> ./instructions.html
Team # 0000000, Page 6 of 25 -> ./instructions.html
less than 25MB -> ./instructions.html
no page limit -> ./Contest_AI_Policy.txt ./instructions.html ./MCM-ICM_Tips.txt
```

**结论**：四个字符串**全部命中至少一个本地官方文件**，无需因 grep 未命中而删条目或降级。

**另有一层时效标注，依据不是 grep 而是 §0 的定义**：凡**仅**见于 `MCM-ICM_Tips.txt`（`V20240912`，非当年文档）而 **2027 届 instructions 未重申**的条款，其**来源仍为官方**，故**不降级**，改标时效标记 `†` 并保留"仅见于 Tips，2027 instructions 未重申"的说明。据此标 `†` 5 条：§2.1.6、§2.3.3、§2.3.6、§2.3.10、§2.5.4。它们的 grep 是命中的；标记理由是**时效**而非来源、也非可命中性——即"这条确实在某个官方文件里，但不是 2027 届的正文"。

**分级分布（2026-09-22 第四次修订后）**：§2 共 **47 条事实** —— `[官方]` **38 条**、`[官方]†` 5 条、`[半官方]†` **3 条**（§2.5.5、§2.5.6、§2.6.6，均出自 `MCM-directors-overview`；本档目前**无"当年"实例**，故三条全带 `†`）、`[社区]` **1 条**（§2.6.5 的推算时长）。另有 §1.3 的 3 条 `[官方]†` 背景语料（不计入 §2）。本次新增 2 条均为 `[官方]`：§2.2.9（摘要页题号栏不得保留 `ABCDEF`）、§2.5.7（`must` 的记录来源义务，见 `instructions.html:952`）。`[半官方]` 档自第二次修订起**首次被使用**——定义见 §0 轴一的"官方人员表述"，实例即 MCM Director 的 JMM '21 报告。

**`[社区]` 复核（按 §0「`[社区]` 只表示无官方出处」）**：全文作为**分级**使用 `[社区]` 的只有 **1 处**——§2.6.5 的推算时长（官方确实从未给出）。其余出现均为 §0/§2.5/§4.1 的**定义与说明文字**，不是分级标注。§4.2 原先误标 `[社区]` 的三份 1994 年文章等，已按 §0 改标 `[官方]`/`[官方]†`（背景语料范围标注），不再降级。

**引用完整性自检（2026-09-22 第四次修订后复跑）**：`INDEX.md` 内共 **130 处 `:行号` 引用** —— **89 处带文件名**（`instructions.html` 39、`MCM-ICM_Tips.txt` 17、`Contest_AI_Policy.txt` 15、`faq.html` 6、`MCM-directors-overview.txt` 5、`MCM-ICM_Summary.tex` 4、`UMAP-2003-judges-commentary.txt` 3），**41 处承前省略文件名**（承前对象为所在行的文件：`instructions.html`、`MCM-ICM_Tips.txt`、`Contest_AI_Policy.txt`、`MCM-ICM_Summary.tex`、`20YearsofGoodAdvice.txt`、`UMAP-2003-judges-commentary.txt`、`MCM-directors-overview.txt`）。**统计口径**（沿上一轮，便于对读）：不计 §0 的两处格式示例引用、§5 本节自身的引用、以及 §1.2 背景表中 `resources.html` 的那一处引用。已全部程序化校验——文件存在、行号在文件行数范围内、且该行/行区间**确实含所述内容**（逐处断言该行必须出现的关键子串，共 **130 处，0 处失配**）。本次新增的 5 处（§2.2.9 的 `MCM-ICM_Summary.tex:39`、`:53`；§2.5.7 的 `instructions.html:952`×2、`instructions.html:1168`）已逐处断言关键子串：`Problem Chosen`、`problem choice`、`must document any outside sources`、`Document resources and references`。

> 本节校验的可复现方式：对 `INDEX.md` 提取全部反引号包裹的 `文件:行号` 与 `:行号`，逐个打开目标文件（PDF 类一律读同名 `.txt`），断言行号在范围内、并对每处断言一个或多个**该行必须出现的关键子串**（子串取自 INDEX 各条所述内容）。本次共校验 130 处引用（89 带文件名 + 41 承前），全部通过。**注意**：`20YearsofGoodAdvice.txt` 的 4 处引用均为承前写法（`:55`、`:153`、`:258`、`:354`），承前对象是 §1.2 表中该行自己的文件名。

补充说明：
- 上述输出已剔除本次核对过程中生成的临时转写文件（`_*.plain.txt`），这些临时文件在核对完成后已删除。
- 二进制 PDF 因文本流被压缩，`grep` 不能直接命中其内部字符串；本索引对 PDF 的引用一律以 pdftotext 转出的**同名 `.txt`** 为准（`Contest_AI_Policy.pdf` ↔ `.txt`、`MCM-ICM_Tips.pdf` ↔ `.txt`、`UMAP-2003-judges-commentary.pdf` ↔ `.txt`、`MCM-directors-overview.pdf` ↔ `.txt`）。
- §3 的 **7** 条冲突（**4 条真冲突见 §3.1 + 3 条伪冲突见 §3.2**）、§2 的其余条目均已在原始文件中逐条定位到行号，行号列于各表"出处"栏。
- 冲突 3 原先附带的"某第三方 LaTeX 宏包内建环境名"断言已删（见 §3.1 冲突 3 行内注）。复核方式：在 `corpus/official/` 全目录检索该宏包名、其内建环境名、以及该宏包配套的引用命令名（三者均系第三方宏包自有术语，非 COMAP 官方术语），**除 `INDEX.md` 自身外 0 命中**，故该断言在本目录语料内无出处，不能以"官方事实"身份留在 §3。
