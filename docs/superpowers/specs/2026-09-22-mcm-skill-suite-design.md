# 美赛（MCM/ICM）自用 Skills 体系 — 设计文档

日期：2026-09-22
状态：设计已确认，待写实现计划

---

## 1. 背景与目标

为参加美国大学生数学建模竞赛（COMAP MCM/ICM）构建一套自用 Claude Code skills，覆盖参赛全流程：赛程编排、论文写作与美化、科研图表、数学模型、数据与代码。

**目标不是"什么都有"，而是在 99 小时的时间压力下"该用的东西能立刻用上"。**

### 已确认的约束

| 约束 | 取值 | 对设计的影响 |
| :--- | :--- | :--- |
| 使用阶段 | **赛中执行优先，兼顾备赛** | skill 短、可执行、少岔路、输出即成品；不做讲解型内容 |
| 论文载体 | **LaTeX** | 写作类 skill 输出 `.tex` 片段，直接进官方摘要页模板（**实际产出见 §9.2：`mcm-latex-format` 只以官方模板的修正副本为基线，不为 `mcmthesis` 等宏包的包内机制背书**） |
| 建模/绘图 | **混合：Python、MATLAB、Origin 视情况** | 图表层必须拆成「语言无关的设计规范」与「语言相关的实现」两半 |
| 获奖论文语料 | **提炼内嵌 + 保留可检索语料库** | skill 内嵌检查清单与范式；同时 corpus/ 保留原文供临场比对文风 |
| 归属 | 自用，非分发 | 无需考虑版本兼容、安装文档、他人上手成本 |

### 非目标

- 不做通用数学建模教学（教科书的活）
- 不做向量检索/知识图谱（对 LaTeX 语料是过度工程）
- 不做自动写完整篇论文的"一键出稿"（见 §2 的官方 AI 政策与学术诚信约束）

---

## 2. 官方规则事实基线

**本章是全套 skill 的依据**，所有「常见失分点」「检查清单」都从这里取，不允许凭印象写。每条按证据分级标注：

`[官方]` 官方原文 · `[半官方]` 官方平台转载或官方人员表述 · `[社区]` 业内共识但无官方出处

> 来源为 2026-09-22 对 COMAP 官方页面的直接抓取：2027 届《Contest Rules, Registration and Instructions》、官方 AI 政策 PDF（`v102025`）、官方 Tips PDF（`V20240912`）、官方摘要页 LaTeX 模板、官方 FAQ。

### 2.1 赛制 [官方]

- **2027 赛期**（EST）：注册截止 1/28 15:00 → 开赛 1/28 17:00 → 停止修改 2/1 20:00 → 提交截止 2/1 21:00。开赛到停止修改 **99 小时**、到提交截止 **100 小时**（由官方时间点推算）。**常被引用的"96 小时"与 2027 日期不符**——COMAP 自己的材料（MCM Director's Overview, JMM '21）用的说法是 **"100-hour"**，与该推算一致
- 六题方向：A *continuous* · B *discrete* · C *data insights* · D *operations research/network science* · E *sustainability* · F *policy*，任选一题
- 队伍 ≤3 名同校在读学生；报名费 $100；开赛后禁止向队外求助

### 2.2 提交硬性要求 [官方]

| 项 | 规定 |
| :--- | :--- |
| **页数上限** | **25 页**，且覆盖整个提交物：Summary Sheet + Solution + References + Table of Contents + Notes + Appendices + Code + 题目特定要求 |
| 页数下限 | **无**。官方明示接受 partial solutions |
| Summary Sheet | 必须是 PDF **第 1 页**，**单页**，字体 ≥12pt |
| 页眉 | **每页**顶部须含队号与页码。官方示例 `Team # 0000000, Page 6 of 25` 由 "for example" 引出，**示例文字本身非强制** |
| 匿名 | 全文**不得出现**学生名、指导老师名、学校名及任何可识别信息 |
| 格式 | Adobe PDF；英文；≥12pt；US Letter 或 A4；附件 **<25MB** |
| 文件名 | 队号，如 `0000000.pdf` |
| 唯一不计页数 | **Report on Use of AI**（置于 25 页之后） |

> 官方模板使用措辞为 "should be used" 而非 "must"。可确证的强制项是**格式与内容要求**，不是模板本身。

### 2.3 Report on Use of AI —— 强制 [官方]

**这一节对本项目有直接约束力：使用本套 skills 即触发披露义务。**

- **触发范围**：LLM、生成式 AI、数学软件、**翻译软件**、代码补全等一切 AI 辅助技术。政策原文明确适用于"从研究到模型开发（含写代码）到书面报告，**甚至包括从队伍母语翻译成英文**"
- **双位置披露**：
  1. 正文内 **inline citation** + References 章节列出所用工具
  2. 在 25 页正文**之后**追加独立章节（同 PDF 文件内），**无页数上限，不计入 25 页**
- **披露格式**：工具名 + 版本/日期 + 模型名。非翻译用途须给出 **Query 原文**与 **Output 全文**；翻译用途只需一句声明
- **未披露后果**：官方原文"COMAP will take appropriate action when we identify submissions likely prepared with undisclosed use of such tools"；未标注的段落易被判为抄袭并取消资格
- **标题版本冲突**：AI 政策 PDF 作 `Report on Use of AI Tools`，2027 届 instructions 正文作 `Report on Use of AI` → **采用后者**（更新的年度正文）

### 2.4 官方对 AI 的分区建议 [官方]

政策原文把 AI 用途分成两侧，这直接决定本套 skill 的定位：

| 官方认可（productivity tools） | 官方建议谨慎（human creativity essential） |
| :--- | :--- |
| 生成结构初始想法 | **模型选择与构建** |
| summarizing、paraphrasing | **辅助写代码** |
| language polishing | **解释数据与模型结果** |
| | **得出科学结论** |

**对设计的直接影响**：M4（模型库）与 M5（代码）落在"建议谨慎"一侧。这不是禁止，但 skill 必须在使用时**显式提示边界**——给出的是候选与判据，最终选择与结论必须由队员判断。此约束写入 M4/M5 的 skill 契约。

### 2.5 评审导向 [官方]

- **官方不把加权 rubric 作为评审标准公布**。官方 FAQ 把"评审标准是什么"指向 instructions 中的内容清单，而非评分表。**但这不等于 COMAP 从未公开过任何评分表**——见 §2.7
- **官方明示评委关注点**：原文"judges are primarily interested in the team's **thought processes, analysis of the problem, modeling approaches, and mathematical methods**"
- **摘要权重**：原文"judges place considerable weight on the summary, and winning papers are often distinguished from other papers based on the quality of the summary"；"It is unlikely the judges will read much beyond a poorly constructed summary"
- **官方认定的弱摘要**：重述题目，或从 Introduction 复制粘贴的套话
- **官方要求的论文内容清单**（10 条）：目录 → 问题重述 → 变量与假设的清晰陈述 → 假设的合理性与论证 → 问题的分析（论证模型动机）→ 正文只放推导摘要（冗长部分入附录）→ **模型设计，并讨论如何检验：误差分析、灵敏度、稳定性** → **优缺点的讨论** → 结论并明确报告结果 → 参考文献
- 官方对优秀论文的描述：包含 assumptions with justifications、modeling process、results、strengths and weaknesses、sensitivity、conclusions 等章节

### 2.6 官方材料自相矛盾处 [官方]

同一官方渠道内部不自洽，skill 引用时须选定一侧并注明：

| # | 冲突项 | 说法 A | 说法 B | 本设计采用 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | PDF 附件大小 | 2027 instructions：<25MB | Tips V20240912：<20MB | **A**（更新的年度正文） |
| 2 | MCM A/B 主题 | **同一份文件内部即矛盾**：`MCM-ICM_Tips.txt:152-154`（逐条分类的正式列表）：A=continuous, B=discrete | `MCM-ICM_Tips.txt:61`（正文顺带举例）：A=discrete, B=continuous。comap.org 主页与 A 侧一致 | **A** |
| 3 | AI 章节标题 | AI 政策 PDF：Report on Use of AI **Tools** | 2027 instructions：Report on Use of **AI** | **B** |
| 4 | 官方 LaTeX 模板年份 | 文件头注释：2027 | 摘要页标题栏渲染：2026 | 用模板但**手工改年份** |
| 5 | ~~报名截止~~ **（已修正：非冲突）** | 15:00 是**报名与缴费**截止（`instructions.html`：`Registration Deadline: Before 3:00 p.m. EST on Thursday, January 28, 2027`） | 17:00 是**开赛**时刻（`Contest Starts: 5:00 p.m.`），亦是队员名单录入截止 | 两件不同的事，**不存在冲突**。原表述有误，已修正 |

> **冲突登记以 `corpus/official/INDEX.md` §3 为准**——那里的条目更完整（含页眉示例写法一处），并且每条都带 `文件:行号` 引用。本表仅保留影响架构判断的项。

### 2.7 关于流传的"官方评分权重表" [半官方]

网上广泛流传一份 100 分制 rubric（Executive Summary 10 / Assumptions 15 / Model 40 / Sensitivity 15 / Documents 10 / Clarity 10），常被传成"COMAP 官方评分标准"。

**已找到出处——它确实来自 COMAP。** 原始材料是 MCM Director 在 AMS 联合数学会议（JMM '21）的报告，已收入 `corpus/official/MCM-directors-overview.pdf`。原文：

> Final Judging: The Final Judging Rubric — **A Sample Final Judging Rubric**
> The panel of Final Judges creates a rubric to fit their particular problem adjusting categories and points as needed. **A starting rubric appears below.**

| 类别 | 分值 |
| :--- | ---: |
| Executive Summary | 10 |
| Assumptions & Justification | 15 |
| **Model / Value Added** | **40** |
| Sensitivity / Strengths & Weaknesses | 15 |
| Required Documents | 10 |
| Clarity of Writing | 10 |
| **合计** | **100** |

**三条限定，缺一不可**：

1. 官方明写这是 **"A Sample" / "A starting rubric"**，且"终审评委团会针对具体题目**调整类别与分值**"——所以它**不是固定权重公式**，不能表述为"模型占 40%"
2. 它管的是 **Final Judging（终审轮）**，不是初筛。只有极少数论文走到终审
3. 材料出自 2021 年，是否逐字沿用至 2027 届未经确认

**用途**：可作为**相对重要性**的参考信号——Model / Value Added 一项独大（40），Assumptions 与 Sensitivity / Strengths & Weaknesses 次之（各 15）。这与 §2.5 官方内容清单的侧重方向一致。

**这是 §4 证据分级制度存在的直接理由**：这份表格在网上被传成"COMAP 官方评分标准"与"伪造的假 rubric"两种极端，**两种说法都不准确**。分级标注逼人去找原文，而原文给出的限定条件恰恰是使用时最要紧的部分。

任何 skill 中出现的评分相关内容都必须标级；无权重依据的一律标 `[社区]`。

### 2.8 评委实际阅读行为 [官方†]

`The UMAP Journal` **由 COMAP 出版**（该刊版权页、订阅说明、作者单位均为 COMAP, Inc.，可证），故其评委评述来源上属 `[官方]`；因是 2003 年材料，加 `†`。文件已收入 `corpus/official/UMAP-2003-judges-commentary.pdf`。

**原文（该文件 `:570-575`）**：

> The judging is accomplished in two phases. Phase I is "triage judging." These are generally only **10-min reads** with a subjective scoring from **1 (worst) to 7 (best)**. Approximately the **top 40%** of papers are sent on to the final judging. Phase II, at a different site, is done with different judges...

**两条对设计有直接指导的原文**：

> At the triage stage, **the summary and overall organization are the basis for judging a paper**.

> The solution papers were coded at COMAP headquarters so that **names and affiliations of the authors would be unknown to the judges**.

**未确认该流程是否适用于 2027 届**，仅作背景。但其中三条观察与其他年份的公开表述一致，可作为设计参考：
- 摘要决定性极大，"a majority of the summaries were poor and did not tell the reader the results obtained"
- 评委最先找的是**是否真的做了建模**，还是"查了几条公式硬套"
- 引用须在**正文中**给出具体页码，仅末尾参考文献表不足

---

## 3. 模块地图

六个模块，M1–M5 是 skills，M6 是语料库（非 skill）。

```
M1 赛程编排层 ── 回答"现在该干什么"
M2 论文写作层 ── 回答"这一节怎么写"
M3 科研图表层 ── 回答"这个数据画成什么图、怎么画"
M4 数学模型层 ── 回答"这个问题该用哪类模型、怎么建"
M5 数据与代码层 ─ 回答"数据哪来、代码怎么写得可复现"
M6 语料库     ── 供 M2/M3 检索获奖论文原文
```

### M1 · 赛程编排层

| skill | 职责 | 输出形状 |
| :--- | :--- | :--- |
| `mcm-playbook` | 99h 时间线、阶段 checkpoint、任务切换时机。**体系入口** | 当前阶段的动作清单 + 该阶段典型失误 |
| `mcm-topic-select` | 六题（A–F）选题决策 | 选题对比表（数据可得性 / 建模难度 / 创新空间 / 队伍匹配度）+ 一个明确推荐 |
| `mcm-selfreview` | 交稿前自查，**分两组**：① 机械合规（§2.2 逐条）② 内容质量（§2.5 官方清单逐条） | 按严重度排序的失分点清单，每条带证据分级 |

`mcm-selfreview` 的合规组是**一票否决**性质（页数、页眉、匿名、文件名、25MB），必须与内容组分开呈现——未过合规的论文，内容再好也无效。

### M2 · 论文写作层

| skill | 职责 | 输出形状 |
| :--- | :--- | :--- |
| `mcm-paper-architecture` | 全文骨架 + **25 页预算分配**（含摘要/TOC/参考文献/附录的占页） | 章节大纲 + 每节必须回答的问题 + 页数预算表 |
| `mcm-abstract` | 摘要页专项（评委在此决定论文生死） | 单页英文摘要，无公式、无图表、无引用 |
| `mcm-section-writer` | 单章节写作范式 | 该章节 `.tex` 片段 |
| `mcm-memo` | **当题目要求 letter/memo 时的写作范式**。注意：Memo 并非通用交付物，是题目特定要求 | 面向指定受众的一页备忘录 |
| `mcm-ai-disclosure` | 生成符合 §2.3 的 `Report on Use of AI` 章节 + 正文 inline citation | 可直接追加到 PDF 末尾的章节文本 |
| `mcm-latex-format` | 排版合规与美化；**基于官方摘要页模板的修正副本** `assets/mcm-2027-summary.tex`（**不**以 `mcmthesis` 为基线——该宏包的包内机制本项目不背书，见 §9.2） | 可编译的 `.tex` 修改 + 格式问题清单 |

**复用现有 skills，不重造**：`academic-polish` / `academic-proofread` / `references-to-bibtex` 作为下游被引用。

**例外**：`mcm-abstract` 不委托给 `academic-polish`——摘要有硬性套路与篇幅纪律，通用润色覆盖不了。

### M3 · 科研图表层

因工具链混合，此层严格分为**设计**（语言无关）与**实现**（语言相关）两半。

| skill | 职责 | 输出形状 |
| :--- | :--- | :--- |
| `mcm-figure-choose` | **核心**。图型决策树 + 设计规范（配色 / 字号 / 坐标轴 / 图例 / 信息密度） | 推荐图型 + 设计要点，语言无关 |
| `mcm-plot-python` | matplotlib 实现；底层用 SciencePlots（9.2k★ 期刊样式库，MIT）叠加美赛 house style，不自造 | 可直接运行的脚本 |
| `mcm-plot-matlab` | MATLAB 实现，同一套规范 | 可直接运行的 `.m` 脚本 |
| `mcm-plot-origin` | Origin 实现，同一套规范 | 操作步骤 + 参数取值（GUI 软件，不产出脚本） |
| `mcm-table` | 三线表、结果表、灵敏度表 | LaTeX 表格代码 |
| `mcm-schematic` | 技术路线图 / 机理示意图 / 模型结构图 | TikZ 或 Mermaid 源码 |

三个 `mcm-plot-*` 必须与 `mcm-figure-choose` 共用同一份规范来源，不允许各自收敛出不同视觉标准。

### M4 · 数学模型层

架构：**单个入口 skill + `references/` 模型库**（已确认）。

```
mcm-model-select/
├─ SKILL.md          # 「问题特征 → 哪类模型」决策树 + references 索引 + 官方 AI 边界提示
└─ references/
   ├─ evaluation.md     # 评价类：AHP、TOPSIS、熵权法、模糊综合
   ├─ prediction.md     # 预测类：ARIMA、灰色 GM(1,1)、回归、时序
   ├─ optimization.md   # 优化类：LP/ILP、多目标、GA、PSO、模拟退火
   ├─ mechanism.md      # 机理类：ODE/PDE、差分方程
   ├─ simulation.md     # 仿真类：Monte Carlo、元胞自动机、排队论、ABM
   ├─ statistics.md     # 统计类：假设检验、回归、贝叶斯
   ├─ network.md        # 网络与图论：最短路、最大流、网络优化
   └─ ml.md             # 机器学习：分类、聚类、降维
```

每个 reference 文件内部结构**统一**：`适用判据 → 标准建模步骤 → 参数与假设 → 常见坑 → 输出模板 → 代码骨架`

选此架构的理由：skill 列表不被 30+ 个模型挤爆；模型库可无上限扩张；**"选错模型"是美赛最大失分点，把选择决策压在入口比分散在多个 skill 里更有效**。

**必须内建的边界提示**：官方将"模型选择与构建"列在建议谨慎用 AI 的一侧（§2.4）。入口 SKILL.md 须显式声明：本 skill 给出候选模型与判据，**最终选择与结论由队员负责**。

### M5 · 数据与代码层

| skill | 职责 | 输出形状 |
| :--- | :--- | :--- |
| `mcm-data` | 数据源检索策略 + 清洗与可信度说明规范 | 数据来源表（出处/口径/局限）+ 清洗步骤 |
| `mcm-code` | 求解代码规范：可复现、随机种子、结果落盘、编号与论文对齐 | 符合规范的求解代码 + 结果输出文件 |

同样受 §2.4 约束：官方将"辅助写代码"与"解释数据与模型结果"列在谨慎侧，skill 须提示边界。

### M6 · 语料库（非 skill）

```
D:\Projects\数学建模\
├─ .claude/skills/            # 项目级，非全局：语料库和 skill 一起走
├─ corpus/
│  ├─ papers/                 # 获奖论文（PDF + 转出的 md）
│  ├─ templates/              # 论文模板、绘图模板
│  ├─ official/               # 官方材料（规则、AI 政策、摘要页模板）——§2 的来源
│  ├─ INDEX.md                # 人读索引：年份 / 题号 / 奖项 / 主题 / 亮点
│  └─ TAGS.md                 # 机读索引：标签 → 路径
└─ docs/superpowers/specs/    # 本目录
```

**检索协议**（写入相关 skill）：先读 `TAGS.md` 定位候选文件 → 再按需读全文。不引入向量库。

---

## 4. skill 形态契约

每个 MCM skill 沿用现有 `academic-polish` 的契约式骨架：

```markdown
---
name: mcm-xxx
description: Use when ... 触发词中英混合（"摘要怎么写" / "write the abstract" / "Summary Sheet"）
---

# 标题

一句 scope：管什么、明确不管什么

## 输出
钉死产出形状（.tex 片段？markdown 表？决策结论？）

## 规则
表格或决策树，正文主体

## 检查清单
可勾选，自查类 skill 用

## 常见失分点
每条必须带证据分级标注：
[官方] 官方原文 / [半官方] 官方平台转载或官方人员表述 / [社区] 业内共识但无官方出处
```

**证据分级不是洁癖。** 见 §2.7：本领域流传最广的"官方评分权重表"**真实存在且已找到出处**（出自 MCM Director 在 JMM '21 的报告，定级 `[半官方]`，登记见 `corpus/official/INDEX.md` §4.1），却被说成"COMAP 官方评分标准"与"伪造的假 rubric"两种极端——**两种说法都不准确**。分级标注是为了让人一眼看出哪条能信、哪条只是经验。凡涉及评分与规则的断言，无 `[官方]` 依据的一律标 `[社区]`。

**硬约束**：每个 SKILL.md 目标 **< 150 行**。深度内容一律下沉 `references/`。主文件只留「决策 + 输出契约 + 指针」。

---

## 5. 命名与冲突

- 全部 `mcm-` 前缀，不与现有 40 个 skill 抢触发词
- 项目级安装（`.claude/skills/`），仅在本项目目录下生效

---

## 6. 建设顺序

```
M6 语料索引 → M2 论文写作 → M3 科研图表 → M1 赛程编排 → M4 模型库 → M5 数据与代码
```

理由：语料库最先，因为它喂给 M2/M3 做提炼。**论文与图表是"肌肉"，现场练不出来；模型库是"查得到的"，边际价值最低。** 所以力气压在 M2/M3。

**实现计划按模块分期**，不是一个覆盖 16 个 skill 的大计划。每个模块走完整的「计划 → 实现 → 验证」闭环后再进下一个。这样任何一个模块完成都立刻可用。

> **一个例外可以提前**：`mcm-ai-disclosure` 与 `mcm-selfreview` 的合规组**不依赖语料库**（依据是 §2 的官方事实），可以在 M6 之前单独先建，成本很低。

---

## 7. 验证方式

不靠自说自话，用真实材料验：

| 类型 | 验证方法 |
| :--- | :--- |
| 写作类 | 拿一篇获奖论文，只给标题 + 我们的模型结果，让 skill 重写某一节，与原文逐段对比 |
| 图表类 | 用真实数据出图，逐条核对设计规范 + **视觉复核**（读图找错，不能只靠程序化自检） |
| 触发类 | 用 subagent 测 description 触发准确率（该触发的触发、不该触发的不触发） |
| 编排类 | 走一遍模拟赛程，检查每个 checkpoint 的产出是否真的能推进下一步 |
| 合规类 | 造一份**故意违规**的样稿（超页、缺页眉、含校名、文件名错），验证 `mcm-selfreview` 能否全部揪出 |

---

## 8. 已有生态与差异化（调研结论，2026-09-22）

调研核验了 30+ 个 GitHub 仓库的 API 元数据与关键文件。

**这个领域已经很拥挤**：`XiaoMaColtAI/math-modeling-skill` 1727★、`MathModeling-skills` 1004★、`Mrite` 524★、`mathodology` 284★；绘图侧 `scipilot-figure-skill` 2446★、样式库 `SciencePlots` 9247★。

但现成项目清一色是**"全程流水线"取向**（读题→建模→求解→成稿一键贯通），与本项目「自用、贴合自身的混合工具链与短板」的定位不是一回事。**更重要的是，已查证的三处空白正是本设计的落点：**

| 空白 | 调研到的表现 | 本设计对应 |
| :--- | :--- | :--- |
| 期刊级制图规范未进入数模工具链 | 通用绘图 skill 与建模流程完全解耦；数模 skill 内部普遍只是"matplotlib 出图 + 300dpi" | **M3** 的「设计 / 实现」分层 |
| 评审维度 → 论文结构 → 可执行检查项，三者未贯通 | 做得最好的两份材料分属两个 6–32★ 仓库、互不引用；高星项目在此维度是空白 | **M2** + `mcm-selfreview` |
| 效果验证严重缺失 | 除一篇 NeurIPS 论文（`LLM-MM-Agent`）外，无任何项目提供可复现评测 | **§7** 以真实材料自证 |

**一条来自他人自曝的一手教训**：`AutoMCM-Pro` 作者披露，其全自动流程产出的图质量不达标；改用有视觉能力的模型复核 21 张图后，**发现 2 处实质 bug 与 1 处配色误用**。该结论已折入 §7：图表验证必须包含视觉复核。

**一个必须警惕的现状**：本领域"工具极多、验证极少"，且讨论几乎全部发生在中文 GitHub 生态（Reddit 零结果、知乎三次检索零结果）。star 数应理解为**关注度，不是有效性**。凡引用他人做法，一律按 §4 证据分级标注。

**可复用的外部依赖**：`SciencePlots`（MIT）作为 `mcm-plot-python` 的样式底座，不自造。

**关于借用他人内容**：多数项目无 License，`vivid-figures-skill` 明确禁止二次开发。本项目的做法是**只借方法论与结构，内容从自己提供的语料重新提炼**。

> ⚠️ **上句政策已作废（2026-09-23）**：现行政策 = **第三方素材不因许可证排除，按价值判断收录**，仍须逐份留 `PROVENANCE`（来源、commit、许可状态）。
> 见 `docs/mcm-suite-todo.md` §E 最后一条。上句作为**当时的调研结论保留原样**，**不得**再作为取舍依据。

---

## 9. 待办与已知风险

**已解决**：COMAP 官方规则与 AI 政策已查证，见 §2。

**已知风险**：

1. **官方材料自身存在版本冲突**（§2.6 的表列 5 项，其中 #5 已改判"非冲突"，**实为 4 处真冲突**；`corpus/official/INDEX.md` §3 现登记 **7 条 = 4 条真冲突（§3.1）+ 3 条伪冲突（§3.2）**）。skill 内已选定一侧并注明依据；但若 COMAP 在 2027 赛前再次修订，需重新核对。
2. **社区模板 mcmthesis 的兼容性未核实**。CTAN 版本 6.3.3（2024-01），是否适配 2027 届的 25 页与提交流程**未经确认**。关于其内建 AI 披露环境与引用命令的具体说法**来自 `corpus/official/` 之外**（调研时查阅 CTAN 文档所得），本项目**不为其正确性背书**——使用时以该宏包官方文档为准。编译方式为 **xelatex**（同源，亦未核实）。
3. **`corpus/` 仍是空的**。M6 与依赖它的 M2/M3 需要获奖论文与模板就位才能开始。
