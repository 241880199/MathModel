# 第一期：COMAP 官方要求与模板落成 skills — 实现计划

> ⚠️ **环境前提已失效（2026-09-24）**：本计划里「**本机无 LaTeX 工具链**、不得写出依赖本机编译的步骤、不得声称已验证编译」
> （见下方约束表与 Task 1 Step 5）**已不成立**——2026-09-24 本机已装 **TeX Live 2026**。
> 现行纪律见 `docs/mcm-suite-lessons.md` **通则 6**（可真编译，故声称编译结果须附真实命令与输出；
> 但页数/体积仍以用户提交的那次编译为准）与 `docs/mcm-suite-todo.md` §E.1。
> 本文件作为**历史工单保留原样**，不逐句改写——但**不得**再把其中的环境陈述当作现行口径。

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把已抓取的 COMAP 官方要求与模板，落成三个不依赖获奖论文语料的 skill，并建立官方材料索引。

**Architecture:** 每个 skill 走 writing-skills 的 RED→GREEN→REFACTOR 循环——先用 subagent 跑基线场景、记录 agent 在没有 skill 时的**具体错误样子**，再针对那些错误写 SKILL.md，再用同一场景验证。三个 skill 均为**契约型**（钉死输出形状），不是纪律型——因为基线失败是"输出形状不对"，不是"明知故犯"，对此用禁令式措辞会适得其反。

> **基线的有效性取决于「干净」**：跑 RED 的 subagent 只能收到 `tests/scenarios/*.md` 的**正文**——不得附带本计划、不得提及 mcm- skill、不得暗示期望的答案。如果基线 subagent 知道答案，测试就失去意义。每次跑 RED 都要用**新开的** subagent，不能复用跑过 GREEN 的那个。

> **关于本计划中没有预先写出的 skill 正文**：这是刻意的，不是占位符。writing-skills 的铁律要求 skill 内容由 RED 阶段**实测出的具体失败**决定——先写好正文再测试等于先写实现再写测试。每个 skill 任务因此给出的是**完整的输出契约与必需内容要素**（这些是可执行的规格），最终措辞在 GREEN 阶段写定。同理，Task 3 的违规样稿只规定**必须植入的违规项**，具体 LaTeX 由实现者写，但 6 项必须全部植入，否则测试无效。

**Tech Stack:** Markdown `SKILL.md`；测试用 subagent 压力场景；校验用 `PyPDF2`（读页数）与 `pdftotext`（读文本）。

## Global Constraints

- skill 路径：`.claude/skills/mcm-<name>/SKILL.md`（项目级，非全局）
- 每个 `SKILL.md` **< 150 行**
- frontmatter 只含 `name` 与 `description` 两个字段，合计 < 1024 字符
- `description` 规格：以 `Use when` 开头；第三人称；**只写触发条件，绝不概括 skill 流程**；< 500 字符；含中英混合触发词
- `name` 只用字母、数字、连字符
- 所有涉及规则或评分的事实断言，必须标证据分级：`[官方]` / `[半官方]` / `[社区]`
- 事实来源**限于** `corpus/official/` 内的官方文件；不得引用外部二手说法
- **本机无 LaTeX 工具链、无 `pdfinfo`、无 `pandoc`**。用户使用**网页端** LaTeX 编译器（非本机）。因此：skill **不得**写出依赖本机编译的步骤，也**不得**声称已验证编译；页数来源为项目内的 PDF（用 `PyPDF2` 读取）或用户提供的网页端页数；文本提取用 `pdftotext`
- 不得修改 `C:\Users\Shameless\.claude\skills\` 下的任何现有 skill

---

### Task 1: 官方材料索引与验证记录

**Files:**
- Create: `corpus/official/INDEX.md`

**Interfaces:**
- Consumes: 已下载到 `corpus/official/` 的 11 个文件
- Produces: `INDEX.md` —— 后续三个 skill 引用事实时的唯一入口；skill 中以「见 `corpus/official/INDEX.md` §X」形式引用

- [ ] **Step 1: 核对实际文件清单**

Run:
```bash
cd "D:/Projects/数学建模/corpus/official" && ls -1
```
Expected: 出现 `MCM-ICM_Summary.tex`、`MCM-ICM_Summary.docx`、`Contest_AI_Policy.pdf/.txt`、`MCM-ICM_Tips.pdf/.txt`、`instructions.html`、`faq.html`、`resources.html`、`20YearsofGoodAdvice.pdf/.txt`、`experience.pdf/.txt`、`expertech.pdf/.txt`、`reflections.pdf/.txt`。若与下表不符，以实际为准写入。

- [ ] **Step 2: 写 `INDEX.md`**

必须包含四节：

**§1 材料清单** — 表格，每行：文件名 / 是什么 / 版本标记或日期 / 用于哪些 skill
- `instructions.html` 标注为 **2027 届正文**（事实基线的主要来源）
- `Contest_AI_Policy.pdf` 标注版本 `v102025`
- `MCM-ICM_Tips.pdf` 标注版本 `V20240912`
- 其余按实际内容标注

**§2 事实基线** — 逐条列出已核验的硬性要求，每条附 `[官方]` 标记与来源文件。至少覆盖：
- 25 页上限覆盖整个提交物（含 Summary Sheet / Solution / Reference List / Table of Contents / Notes / Appendices / Code / 题目特定要求）
- 无最低页数，接受 partial solutions
- Summary Sheet 必须是第 1 页、单页、字体 ≥12pt
- 每页页眉格式 `Team # 0000000, Page 6 of 25`
- 全文禁止出现学生名、指导老师名、学校名
- PDF、≥12pt、US Letter 或 A4、<25MB、文件名 = 队号
- Report on Use of AI 置于 25 页之后，无页数上限、不计入 25 页

**§3 官方冲突登记** — 表格，每行：冲突项 / 说法 A（来源）/ 说法 B（来源）/ 本项目采用哪侧及理由。至少覆盖已核实的 5 处：附件大小 25MB vs 20MB、MCM A/B 主题、AI 章节标题 `Report on Use of AI Tools` vs `Report on Use of AI`、模板文件头 2027 vs 标题栏 2026、报名截止时间。

**§4 已证伪的流传说法** — 记录那份 100 分制"官方评分权重表"的真实来源（2003 年 UMAP 评委自述，终审轮自行制定），标明 `[社区 · 已证伪]`，并写明 COMAP 从未公布加权 rubric。

- [ ] **Step 3: 核对每条事实都能在本地文件里 grep 到**

Run:
```bash
cd "D:/Projects/数学建模/corpus/official" && for s in "25 page limit" "Team # 0000000, Page 6 of 25" "less than 25MB" "no page limit"; do printf '%s -> ' "$s"; grep -rl "$s" . 2>/dev/null | tr '\n' ' '; echo; done
```
Expected: 每个字符串至少命中一个文件。若有未命中的，删掉 `INDEX.md` 中对应条目或改标 `[半官方]`。

- [ ] **Step 4: Commit**

```bash
cd "D:/Projects/数学建模" && git add corpus/official/INDEX.md && git commit -m "docs: 建立 COMAP 官方材料索引与事实基线"
```

---

### Task 2: `mcm-ai-disclosure`

**Files:**
- Create: `.claude/skills/mcm-ai-disclosure/SKILL.md`
- Create: `tests/scenarios/ai-disclosure-baseline.md`（场景定义）
- Create: `tests/results/ai-disclosure-baseline.md`（RED 记录）

**Interfaces:**
- Consumes: `corpus/official/INDEX.md` §2（AI 章节位置与页数规则）、§3（标题冲突的采用侧）
- Produces: `mcm-ai-disclosure` skill。Task 3 的合规清单会检查其产出是否存在

- [ ] **Step 1: 写基线场景**

创建 `tests/scenarios/ai-disclosure-baseline.md`，内容为一段可直接发给 subagent 的 prompt：

```
你是美赛参赛队员。下面是你们队的 AI 工具使用记录：

- 用 DeepL 把中文初稿整篇翻成英文
- 用 Claude 润色了摘要和引言
- 用 ChatGPT 查 TOPSIS 法的计算步骤
- 用 GitHub Copilot 补全了 Python 求解代码
- 用 MATLAB 的优化工具箱跑求解

请按 COMAP 的要求，写好这次比赛需要提交的 AI 使用披露部分。
直接输出你打算放进论文的内容。
```

**故意不给**任何格式说明——这就是要观察的：agent 在没有 skill 时会自己发明格式。

- [ ] **Step 2: 跑基线（RED）**

用一个全新 subagent 执行上述 prompt，**不加载任何 mcm- skill**。

Run: 通过 Agent 工具派发，prompt 为 `tests/scenarios/ai-disclosure-baseline.md` 的正文。

- [ ] **Step 3: 记录基线结果**

把 subagent 的**原始输出**存进 `tests/results/ai-disclosure-baseline.md`，并在末尾列出「缺失项清单」。对照下列 6 项逐条判定有/无：

| # | 应有内容 | 依据 |
| :--- | :--- | :--- |
| 1 | 正文内的 inline citation（不只是末尾参考文献） | `[官方]` |
| 2 | 独立章节，且位置在 25 页正文**之后** | `[官方]` |
| 3 | 章节标题用 `Report on Use of AI` | `[官方]`（年度正文侧） |
| 4 | 每个工具注明 工具名 + 版本/日期 + 模型名 | `[官方]` |
| 5 | 非翻译用途给出 Query 原文与 Output 全文 | `[官方]` |
| 6 | 翻译用途只需一句声明（不需 Query） | `[官方]` |

- [ ] **Step 4: 写 `SKILL.md`（GREEN）**

针对 Step 3 实测出的缺失项写。**契约式**：先钉死输出形状，再给规则。

必须包含：
- frontmatter：`name: mcm-ai-disclosure`；description 以 `Use when` 开头，含中英触发词（`AI 使用声明`、`披露`、`Report on Use of AI`、`AI disclosure`、`COMAP AI policy`），**不得概括流程**
- `## 输出` —— 钉死为三部分，按序：① 正文 inline citation 的插入位置与写法 ② References 中 AI 工具条目 ③ 追加章节的完整文本（标题 + 逐工具条目）
- `## 规则` —— 表格，含 Step 3 那 6 项，每项标证据分级
- 明确写出：该章节**置于 25 页之后、无页数上限、不计入 25 页**，并注明依据 `corpus/official/INDEX.md` §2
- 明确写出标题采用 `Report on Use of AI`（年度正文侧），并注明官方政策 PDF 作 `Report on Use of AI Tools`，两者不一致
- `## 触发范围` —— 列出会触发披露义务的工具类别，**必须包含翻译软件**（政策原文明确适用于翻译）
- `## 常见失分点` —— 每条带证据分级

行数控制在 150 行内。

- [ ] **Step 5: 跑带 skill 场景（验证 GREEN）**

用**全新** subagent，加载 `mcm-ai-disclosure` skill，执行与 Step 1 完全相同的 prompt。

Run: 派发 subagent，prompt 同 `tests/scenarios/ai-disclosure-baseline.md`，但要求先读取 `.claude/skills/mcm-ai-disclosure/SKILL.md`。

- [ ] **Step 6: 判定通过**

对照 Step 3 的 6 项表格逐条核对新输出。**6 项全部命中才算通过。**

把新输出与判定结果追加进 `tests/results/ai-disclosure-baseline.md`。

若有未命中项：回到 Step 4，针对该缺失项补写（**不要加泛泛的强调，要改输出契约的形状**），然后重跑 Step 5。反复直到 6 项全中。

- [ ] **Step 7: 检查 frontmatter 规格**

Run:
```bash
cd "D:/Projects/数学建模" && awk '/^---$/{n++} n==1' .claude/skills/mcm-ai-disclosure/SKILL.md | head -5; echo "--- 行数 ---"; wc -l < .claude/skills/mcm-ai-disclosure/SKILL.md
```
Expected: 能看到 `name:` 与 `description:` 两行；行数 < 150。

- [ ] **Step 8: Commit**

```bash
cd "D:/Projects/数学建模" && git add .claude/skills/mcm-ai-disclosure tests/ && git commit -m "feat: 新增 mcm-ai-disclosure skill（RED 基线已记录）"
```

---

### Task 3: `mcm-selfreview` 合规组

**Files:**
- Create: `.claude/skills/mcm-selfreview/SKILL.md`
- Create: `tests/fixtures/violating-paper.tex`（故意违规样稿）
- Create: `tests/fixtures/clean-paper.tex`（对照样稿）
- Create: `tests/scenarios/selfreview-baseline.md`
- Create: `tests/results/selfreview-baseline.md`

**Interfaces:**
- Consumes: `corpus/official/INDEX.md` §2
- Produces: `mcm-selfreview` skill，含 A 组合规清单与 B 组内容清单

- [ ] **Step 1: 造违规样稿 `tests/fixtures/violating-paper.tex`**

一份最小可读的 LaTeX 论文源码，**植入下列 6 处违规**（全部可从源码检出，不需要编译）：

| # | 植入的违规 | 分级 |
| :--- | :--- | :--- |
| 1 | 页眉缺失队号：只用 `\rhead{Page \thepage}`，无 `Team #` | `[官方]` |
| 2 | 正文出现学校名：`We thank the faculty of Example University for support.` | `[官方]` |
| 3 | 摘要页未用 `\Team` 宏，队号写死为空 | `[官方]` |
| 4 | 文档类选项为 `\documentclass[10pt]{article}`，低于 12pt 下限 | `[官方]` |
| 5 | 正文有 AI 辅助痕迹（`The TOPSIS weights were computed with the assistance of ChatGPT.`）但**无** `Report on Use of AI` 章节 | `[官方]` |
| 6 | 提交文件名未用队号：源码顶部注释 `% filename: final_paper_v3.pdf` | `[官方]` |

**同时植入两处「陷阱」，用来检验 skill 的判据既不漏也不滥**：

- 参考文献混入一条 CSDN 链接（`https://blog.csdn.net/...`）。这是**质量问题，不是规则违规**——官方从未禁止 CSDN。skill 应把它归入 B 组内容清单，**不得**报成合规否决项。
- 全文**没有** `Table of Contents`。官方措辞是 "is encouraged"，**非强制**。skill **不得**因缺目录而判合规失败。

这两处是有意设计的假阳性诱饵：若 skill 把它们当违规，说明清单过激，需收窄判据（见 Step 9）。

- [ ] **Step 2: 造对照样稿 `tests/fixtures/clean-paper.tex`**

同一份内容的修正版：页眉含 `Team # 1234567`、无学校名、用官方 `\Problem`/`\Team` 宏、有目录、有 `Report on Use of AI` 章节、参考文献无 CSDN。

- [ ] **Step 3: 写基线场景**

`tests/scenarios/selfreview-baseline.md`：

```
请审查 tests/fixtures/violating-paper.tex 这份美赛论文稿，
告诉我它能不能直接提交。给出你发现的问题清单。
```

- [ ] **Step 4: 跑基线（RED）**

用全新 subagent 执行该 prompt，**不加载任何 mcm- skill**。把原始输出存进 `tests/results/selfreview-baseline.md`。

- [ ] **Step 5: 记录基线漏检**

对照 Step 1 的 6 处违规，逐条判定基线**是否发现**。预期基线会发现内容层面的问题，但**漏掉机械合规项**（页眉、匿名、文件名、12pt、AI 章节缺失）。把实际漏检项写进结果文件。

- [ ] **Step 6: 写 `SKILL.md`（GREEN）**

针对 Step 5 实测的漏检写。**结构式**——合规组必须是**逐项必填的清单**，不许 agent 自由裁量跳过。

必须包含：
- frontmatter：`name: mcm-selfreview`；description 含中英触发词（`论文自查`、`投稿前检查`、`能不能提交`、`final check`、`paper review before submission`），不概括流程
- `## 输出` —— 钉死为**两组分开**呈现：
  - **A 组合规（一票否决）** —— 逐项列，每项必填「检查值 / 是否通过 / 证据位置」。**未过合规的论文，内容再好也无效**，这句话要写进输出契约
  - **B 组内容质量** —— 按官方 10 条内容清单逐条
- `## 合规检查清单` —— 表格，至少含：总页数（含摘要/目录/参考文献/附录/代码）、Summary Sheet 是否第 1 页且单页、每页页眉是否含队号、是否出现校名/姓名/指导老师、文件名是否 = 队号、PDF 是否 <25MB、是否 ≥12pt、Report on Use of AI 是否存在且在 25 页之后。每条标 `[官方]` 并指向 `corpus/official/INDEX.md` 对应节
- `## 内容检查清单` —— 官方 10 条内容要求逐条
- **页数检查的具体方法**（本机无 `pdfinfo`，用户用网页端编译器）：若项目内有编译好的 PDF，用 `python -c "from PyPDF2 import PdfReader; print(len(PdfReader('x.pdf').pages))"` 读**实际**页数；若只有 `.tex` 源码，**要求用户提供网页端显示的页数**——不得猜测、不得按源码行数估算
- `## 常见失分点` —— 每条带证据分级

- [ ] **Step 7: 跑带 skill 场景（验证 GREEN）**

用全新 subagent，加载 `mcm-selfreview`，执行与 Step 3 相同的 prompt。要求先读取该 SKILL.md。

- [ ] **Step 8: 判定通过**

两件事都要核对，**缺一不可**：

1. **6 处违规全部命中**
2. **2 处陷阱未被误报为合规违规**——CSDN 链接应落在 B 组内容提示，缺目录**不得**出现在 A 组合规否决项里

结果追加进 `tests/results/selfreview-baseline.md`。

未命中则回 Step 6 补，再重跑。反复直到两项全过。

- [ ] **Step 9: 反向验证（防误报）**

用同一 skill 审查 `tests/fixtures/clean-paper.tex`。

Expected: **合规组零告警**。若把对照样稿判为违规，说明清单过于激进，需收窄判据。

- [ ] **Step 10: 检查 frontmatter 与行数，Commit**

```bash
cd "D:/Projects/数学建模" && wc -l < .claude/skills/mcm-selfreview/SKILL.md && git add .claude/skills/mcm-selfreview tests/ && git commit -m "feat: 新增 mcm-selfreview skill（含违规样稿反向验证）"
```

---

### Task 4: `mcm-latex-format`

**Files:**
- Create: `.claude/skills/mcm-latex-format/SKILL.md`
- Create: `.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex`（官方模板副本，去掉 2026 标题错误）
- Create: `tests/scenarios/latex-format-baseline.md`
- Create: `tests/results/latex-format-baseline.md`

**Interfaces:**
- Consumes: `corpus/official/MCM-ICM_Summary.tex`、`INDEX.md` §3
- Produces: 一个 skill，产出可编译的 `.tex` 骨架

- [ ] **Step 1: 写基线场景**

`tests/scenarios/latex-format-baseline.md`：

```
我要开始写美赛论文了。请给我一份可以直接开始写的 LaTeX 论文骨架，
要符合 COMAP 的格式要求。
```

- [ ] **Step 2: 跑基线（RED）**

全新 subagent，不加载任何 mcm- skill。原始输出存 `tests/results/latex-format-baseline.md`。

- [ ] **Step 3: 记录基线缺口**

对照下列项判定有/无：

| # | 应有 |
| :--- | :--- |
| 1 | 用官方摘要页模板结构（三栏 Problem Chosen / Summary Sheet / Team Control Number） |
| 2 | 页眉 `\lhead{Team \Team}` 与 `\rhead{Page \thepage}` |
| 3 | 摘要页 `\thispagestyle{empty}` + `\vspace*{-16ex}` |
| 4 | `\setcounter{page}{1}` 让正文从第 1 页起 |
| 5 | 不含校名/姓名占位符 |
| 6 | 25 页预算提示 |

预期基线会给出一个**通用 LaTeX 论文模板**，上述多数缺失。记录实测。

- [ ] **Step 4: 准备模板副本**

复制 `corpus/official/MCM-ICM_Summary.tex` 到 `.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex`，并**修正官方未同步的错误**：把摘要页标题栏的 `2026\\ MCM/ICM\\ Summary Sheet` 改为 `2027\\ MCM/ICM\\ Summary Sheet`。在文件头加注释说明这是官方模板的修正副本及修正点。

- [ ] **Step 5: 写 `SKILL.md`（GREEN）**

- frontmatter：`name: mcm-latex-format`；description 含中英触发词（`论文排版`、`LaTeX 格式`、`格式合规`、`format the paper`、`LaTeX skeleton`），不概括流程
- `## 输出` —— 钉死为：① 完整可编译的 `.tex` 骨架（引用 assets 模板）② 格式合规问题清单
- `## 规则` —— 表格，含 Step 3 的 6 项，每条标证据分级并指向 `INDEX.md`
- 写入官方模板的三个关键事实：`\documentclass[12pt]{article}`、`\geometry{left=1in,right=0.75in,top=1in,bottom=1in}`、两个待替换宏 `\Problem` 与 `\Team`
- **明确写出编译方式**：用户使用**网页端** LaTeX 编译器，本机无 TeX 发行版。skill 输出 `.tex` 后**不承诺**编译验证；提示若网页端报错，把报错原文贴回来定位
- 写入官方冲突：模板文件头写 2027 但标题栏渲染 2026，本项目用修正副本
- `## 常见失分点` —— 每条带证据分级

- [ ] **Step 6: 跑带 skill 场景并判定**

全新 subagent 加载该 skill，执行 Step 1 同一 prompt。对照 Step 3 的 6 项：**全中才通过**。结果追加进 `tests/results/latex-format-baseline.md`。未中则回 Step 5 补，再重跑。

- [ ] **Step 7: 检查行数与 assets 完整性，Commit**

```bash
cd "D:/Projects/数学建模" && wc -l < .claude/skills/mcm-latex-format/SKILL.md && ls .claude/skills/mcm-latex-format/assets/ && git add .claude/skills/mcm-latex-format tests/ && git commit -m "feat: 新增 mcm-latex-format skill 与官方模板修正副本"
```

---

## 完成标准

- [ ] `corpus/official/INDEX.md` 存在，四节齐全，每条事实可在本地文件 grep 到
- [ ] 三个 skill 的 `SKILL.md` 均存在，行数 < 150，frontmatter 合规
- [ ] 三份 `tests/results/*-baseline.md` 均含**真实 subagent 输出**与逐项判定，且 GREEN 阶段全部命中
- [ ] `mcm-selfreview` 在对照样稿上零误报
- [ ] 四次 commit 完成

## 已知待决

- ~~LaTeX 工作流未确认~~ → **已确认**：用户使用网页端编译器，本机不装 TeX 发行版。影响已折入 Global Constraints 与 Task 3 Step 6、Task 4 Step 5。
- 本期的三个 skill 均**不依赖**获奖论文语料。M6 语料索引与 M2/M3 主线待素材就位后另立计划。
