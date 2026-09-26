# AI 披露 skill —— RED 基线记录

- 日期：2026-09-22
- 场景：`tests/scenarios/ai-disclosure-baseline.md`
- 条件：**不加载任何 skill**，subagent 只收到场景正文
- 判定表：见本文末「缺失项清单」（6 项）

本文件记录两次基线。两次派发时，**我方 prompt 均只含场景正文本身**（无简报、无背景、无 `mcm-` 提及、无 COMAP 政策内容、无期望答案、无"这是测试"的暗示），且均用 `general-purpose`（非 `fork`）。

---

## Run A —— 本地基线

第一次派发。subagent 在项目工作目录内运行。**它自行探索了仓库**并读取了 `corpus/official/Contest_AI_Policy.txt`、`tests/scenarios/ai-disclosure-baseline.md`、`docs/superpowers/plans/`，因此在作答时手里已有官方原文。这一污染**不是**我方 prompt 造成的（prompt 只有场景正文），详见文末「偏离与顾虑」§D1。

### A.1 原始输出（首次 hand-back 全文，逐字）

> ## 交付内容
>
> 已按 COMAP 官方政策写成可直接粘贴的披露部分。格式依据是本地官方原文 `D:/Projects/数学建模/corpus/official/Contest_AI_Policy.txt`（v102025《Use of AI Tools in COMAP Contests》），不是二手转述。
>
> ## 三个关键格式事实（已核实原文）
>
> 1. 章节标题必须逐字为 **"Report on Use of AI Tools"**，放在 25 页正文**之后**（含参考文献、附录之后），**不计入 25 页、本身无页数限制**。
> 2. 政策明确把 **mathematics software（数学软件）和 translation software（翻译软件）** 列入需披露的 AI 工具。所以 **DeepL 和 MATLAB 都必须写进去**——队伍把它们记进使用记录是对的。且这两类只接受**陈述式**说明，不需要 query/output。
> 3. 只有 **Claude 和 ChatGPT 需要 "exact wording you input" + "complete output"**。这是全篇唯一必须由队伍自己填的部分。
>
> ## 输出的论文内容（见正文）
>
> - 正文内联引用标记（上标 1–5）
> - 25 页内的参考文献条目（COMAP 要求 AI 工具同时出现在 inline citation 和 reference section，队伍容易漏掉这一条）
> - 完整的 "Report on Use of AI Tools" 段落，5 条：DeepL（翻译，陈述式）、Claude（润色摘要+引言，需 query/output）、ChatGPT（TOPSIS 步骤，需 query/output）、GitHub Copilot（代码补全，陈述式）、MATLAB Optimization Toolbox（数学软件，陈述式）
> - 末尾否定式声明（未用于建模/选参/结论/生成参考文献）——评审友好且政策要求"which model and what for purpose"，故每条都写了 Purpose 与 Verification
>
> ## 必须提醒队伍的两点
>
> 1. **Query/Output 两处不能编。** 政策要求逐字输入与完整输出。编造看似合理的 prompt 文本本身就是披露失实，风险高于留白。若确实未留存原文，应诚实标注 "reconstructed from team notes; exact wording not retained"，而不是伪造引文。
> 2. **版本与日期**按政策示例格式填写（如 "Nov 5, 2023 version, ChatGPT-4"）。
>
> ## 主动发现的一个风险点
>
> 整篇机器翻译 + 摘要/引言 LLM 润色，意味着英文正文基本是机器产出。政策允许（明确许可翻译与语言润色，只要披露），但同页警告 AI 可能复现他人文本，建议提交前把润色过的摘要与引言对照来源再核一遍。
>
> ## 建议后续动作
>
> `docs/superpowers/plans/` 与 `tests/scenarios/ai-disclosure-baseline.md` 显示该仓库正在建设 MCM 技能套件，本场景很可能是一条 baseline 测试用例。若需要，可把上述披露模板固化为技能产物。

### A.2 原始输出（应我方要求补回的逐字披露正文）

首次 hand-back 只说"见正文"而未附正文，故另发消息要求逐字重贴。以下是它回传的披露正文全文，逐字照录。

**【1. Inline citation 写法与插入位置】**

> **Placement:** append after the reference list, as the final section.
>
> ### A. Inline citations (inside the 25 pages)
>
> Add superscript markers at each point of use, e.g. "…the optimisation model was solved with MATLAB's Optimization Toolbox.⁵" and "…the draft was translated from the team's Mandarin manuscript.¹" Use superscript numerals 1–5 (not `[1]`-style) so they don't collide with your numbered references.

**【2. References 章节中的 AI 工具条目】**

```
[1] DeepL SE. DeepL Translator [version]. Accessed [date]. https://www.deepl.com/translator
[2] Anthropic. Claude [model]. Accessed [date]. https://claude.ai
[3] OpenAI. ChatGPT [model]. Accessed [date]. https://chat.openai.com
[4] GitHub. GitHub Copilot [version]. Accessed [date]. https://github.com/features/copilot
[5] The MathWorks, Inc. MATLAB Optimization Toolbox, Release [R20xx]. Natick, MA.
    https://www.mathworks.com/products/optimization.html
```

**【3. 追加章节完整文本】**

```
                        Report on Use of AI Tools

This section is appended after the 25-page solution in accordance with COMAP's
policy "Use of AI Tools in COMAP Contests" and is not counted toward the 25-page
limit. AI tools are cited inline in the solution and listed in the reference
section. The complete record of use is given below.

1. DeepL SE, DeepL Translator ([version], [date accessed])
   Purpose: translation.
   Uploaded the entire paper, written in Mandarin, to be translated into English.
   The machine translation was used as a working draft only; all subsequent
   correction of terminology, technical phrasing and final wording was performed
   by the team.

2. Anthropic Claude ([model], [date accessed])
   Purpose: language polishing of the Abstract and the Introduction (grammar,
   clarity, concision). No technical content was requested or used.
   Query: [insert the exact wording you input into the AI tool]
   Output: [insert the complete output from the AI tool]
   Verification: all accepted changes were wording-level. The team confirmed that
   no claim, number, assumption, result or citation was added or altered, and
   reversed [n] suggestions that changed the intended technical meaning.

3. OpenAI ChatGPT ([model], [date accessed])
   Purpose: consultation on the standard computational procedure of the TOPSIS
   method (normalisation, weighting, ideal and anti-ideal solutions, closeness
   coefficient).
   Query: [insert the exact wording you input into the AI tool]
   Output: [insert the complete output from the AI tool]
   Verification: the procedure was checked against [textbook / reference 12], and
   the method was implemented independently by the team and validated against a
   hand-worked numerical example and a published test case.

4. GitHub Copilot ([version], [date accessed])
   Purpose: auto-completion of routine Python code in our solution scripts.
   Auto-completions for code used in preparing our models. All completed
   fragments were read, executed and tested by the team; none were retained
   without the team understanding them, and all reported outputs were reproduced
   by an independent clean run.

5. MATLAB Optimization Toolbox, MathWorks ([release], [date accessed])
   Purpose: conventional numerical solution of our optimisation models via
   linprog and fmincon. This is deterministic mathematics software, disclosed
   here as required by the policy.
   Verification: models were re-solved from a clean script; results were
   cross-checked against [an independent Python implementation / analytic bounds
   / sensitivity re-runs].

No AI tool was used to formulate the problem, select or build the models, choose
parameters, generate or interpret data, draw scientific conclusions, or write the
final solution beyond the uses disclosed above. No reference in this paper was
generated by an AI tool.
```

---

## Run B —— 冷启动基线（远端隔离，无仓库访问）

第二次派发，`isolation: "remote"`，目的：排除 Run A 的仓库污染，取一个真正"手里没有本仓库语料"的无 skill 基线。Prompt 仍只有场景正文。它自行做了网络检索。

### B.1 原始输出（hand-back 全文，逐字）

> 已核实 COMAP 官方 AI 政策（2024 年起施行、2025/2026 赛季沿用），据此写好了可直接放进论文的披露内容。
>
> ## 放置规则（先明确）
> - 正文解答仍 ≤25 页，该页数含参考文献、附录、代码、目录。
> - 标题为 "Report on Use of AI" 的一节附在 25 页之后，**不限页数、不计入 25 页**。
> - 另需正文行内引用 + 把所有 AI 工具列入参考文献区。LaTeX 的 mcmthesis 宏包内置 \AIcite{AI1,...}（与普通 \cite 分开）。文档用英文。
>
> ## 一、正文里的行内引用（放 Introduction 开头，或首页脚注）
> "Certain portions of this solution were prepared with the assistance of the artificial-intelligence tools listed in the References as [AI1]–[AI4]. The nature and extent of that assistance is described in full in the *Report on Use of AI* appended to this paper. All such content was reviewed, verified, and where necessary corrected by the team, which takes sole responsibility for the solution as submitted."
>
> ## 二、参考文献区条目（25 页内）
> [AI1] DeepL SE. *DeepL Translator* (web application, <version>, <date>). Machine translation of the team's Chinese draft into English. https://www.deepl.com
> [AI2] Anthropic. *Claude* (<model and version>, <date>). Language polishing of the Abstract and Introduction.
> [AI3] OpenAI. *ChatGPT* (<model and version>, <date>). Consultation on the computational steps of the TOPSIS method.
> [AI4] GitHub. *GitHub Copilot* (<version>, <date>). Inline code auto-completion in the Python implementation.
>
> ## 三、附录全文（Report on Use of AI）
>
> ### Report on Use of AI
> This report is submitted in accordance with COMAP's policy on the use of large language models and generative AI tools in the MCM/ICM contests. It is appended after the 25-page solution, is not part of that page limit, and is organised by tool.
>
> **1. DeepL SE, *DeepL Translator* (web application, <version>, <date of use>)**
> *Purpose: translation.* The team's draft of this solution was written in Chinese. The complete draft was uploaded to the tool and machine-translated into English; the English text produced in this way was the starting text for the submitted solution. In accordance with COMAP's policy, no input query is reproduced for translation-only use.
> *Team action:* The team edited the translated text manually, line by line, before submission. All terminology, notation, numerical values, equations, results and conclusions were checked against the team's own calculations. The tool performed no computation and originated no technical content; the errors it introduced (terminology and phrasing) were corrected by the team.
>
> **2. Anthropic, *Claude* (<model and version>, <date of use>)**
> *Purpose: language polishing of the Abstract and of the Introduction*, after both sections had been drafted by the team.
> Query 1: <insert the exact wording you input into the AI tool>
> Output 1: <insert the complete output from the AI tool>
> Query 2: <insert the exact wording of any subsequent input into the AI tool>
> Output 2: <insert the complete output from the second query>
> *(repeat for every further input, as the policy requires)*
> *Team action:* Each revised passage was compared sentence by sentence with the team's draft. Only phrasing, grammar and concision were accepted; any change that altered technical meaning, emphasis or claimed results was rejected. The Abstract and Introduction as submitted state the team's own claims.
>
> **3. OpenAI, *ChatGPT* (<model and version>, <date of use>)**
> *Purpose:* to recall the standard computational steps of the TOPSIS method while the team was building its evaluation model.
> Query: <insert the exact wording you input into the AI tool>
> Output: <insert the complete output from the AI tool>
> *Team action and verification:* The response was not used as a source and is not cited. The TOPSIS procedure actually implemented here is taken from the published literature listed in the References, and every step -- normalisation of the decision matrix, weighting, the ideal and anti-ideal solutions, the separation measures, and the closeness coefficient -- was derived and checked by the team before it was coded or used. The tool served only as an orientation aid that prompted the team to consult those references. No sentence, claim or citation from its output appears in the solution.
>
> **4. GitHub, *GitHub Copilot* (<version>, <date of use>)**
> *Purpose:* inline auto-completion while the team wrote the Python code for <model / solver>.
> In the descriptive form of COMAP's Example 4, the tool supplied editor auto-completions of routine code as the team typed -- loop and array constructs, plotting and file-input boilerplate. The team directed the code and reviewed every accepted suggestion against its own formulation of the model, then executed and validated the complete program. The results reported in the solution reproduce the team's own algorithm.
>
> **5. Verification and responsibility.** Every output listed above was read in full by at least two team members. Its accuracy, validity and appropriateness were checked against the team's derivations, against independent computation, or against the original sources cited in the References, and inaccuracies were corrected or discarded. Because generative tools can reproduce text from other sources, all AI-assisted passages were checked against those sources before submission; no sentence was retained unless the team could confirm it as its own expression or trace it to a reference listed in this paper. The team accepts full responsibility for all content of this solution.
>
> **6. Software not covered by this report.** MATLAB and its Optimization Toolbox (used to solve the optimisation models and to cross-check results), the Python scientific stack (NumPy/SciPy/pandas/matplotlib), and LaTeX/TikZ are conventional computational and typesetting software, not generative AI tools, and are therefore not disclosed as AI uses above. Their role is documented in the code appendix of this solution.
>
> ## 四、必须由队伍补齐的三处
> 1. 各工具的准确版本与日期（COMAP 示例体例为"名称（版本，日期）"）。
> 2. Claude 与 ChatGPT 的逐条 query + 完整 output（政策要求贴输入的确切措辞与完整输出；该节不限页数）。若记录已丢失，不要凭空补写，按实际交互如实重构并注明该条为事后重构、完整输出未能保存。
> 3. Copilot 的版本及其补全的具体代码文件/函数。
>
> ## 五、两个真实风险
> - DeepL 整篇翻译适用"翻译例外"（只需一句声明、不必贴 query），但"整篇翻译"必须披露，未披露的 AI 辅助译文 COMAP 明确可按抄袭处理并取消资格。
> - ChatGPT 那条会引来对照检查：既然披露用 AI 查 TOPSIS 步骤，评委可能拿它比对论文里的公式。报送前核对论文中 TOPSIS 的归一化方式、正/负理想解、以及贴近度 C_i = D_i^-/(D_i^+ + D_i^-) 的分子分母方向是否自洽（这类助手回答最常见的出错点）。另外绝不要把 AI 输出里的文献抄进参考文献。
>
> 另注：MATLAB Optimization Toolbox 不属于生成式 AI，不要列为 AI 使用，已用附录第 6 条作说明以免评委误会。
>
> Sources: COMAP AI Policy PDF (stage.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)；SCUT 镜像版 Use of AI Tools in COMAP Contests；mcmthesis 宏包 \AIcite 机制文档。

---

## 缺失项清单

判定口径（我方据简报 6 项表操作化，逐条与 `corpus/official/INDEX.md` §2.4 对齐，分级沿用 §0）：

| # | 应有内容 | 分级 | 判定口径 |
| :--- | :--- | :--- | :--- |
| 1 | 正文内的 inline citation（不只是末尾参考文献） | `[官方]` §2.4.2 | 正文内是否有就地标注的引用（上标/编号），而非仅末尾列表 |
| 2 | 独立章节，位置在 25 页正文**之后** | `[官方]` §2.4.3 | 是否声明置于 25 页正文之后、且不与之混排 |
| 3 | 章节标题用 `Report on Use of AI` | `[官方]` §2.4.4 + §3 冲突 3 | 标题是否**逐字**为 `Report on Use of AI`（`...AI Tools` 判否） |
| 4 | 每个工具注明 工具名 + 版本/日期 + 模型名 | `[官方]` §2.4.5 | **逐工具**核：每一条是否三要素齐全（该工具确有模型者必须给模型名） |
| 5 | 非翻译用途给出 Query 原文与 Output 全文 | `[官方]` §2.4.6 | 文本输入→文本输出的非翻译用途，是否给出 `Query:`/`Output:` 两字段 |
| 6 | 翻译用途只需一句声明（不需 Query） | `[官方]` §2.4.6 | 翻译条目是否以一句陈述了结、且**未**被要求附 Query |

### Run A（本地基线）逐条判定

| # | 判定 | 说明 |
| :--- | :--- | :--- |
| 1 | 有 | 给了上标 1–5 的就地插入写法与示例句 |
| 2 | 有 | "append after the reference list, as the final section"；正文亦声明置于 25 页之后 |
| 3 | **无** | 标题写作 **`Report on Use of AI Tools`** —— 采用了政策 PDF 侧，与 §3 冲突 3 的本项目采用侧相反 |
| 4 | **无** | 三要素不齐：DeepL 与 Copilot 条目只有 `[version]`、**无模型名字段**；且三处把「版本/日期」换成了 `[date accessed]`（**访问日期 ≠ 官方范例的「版本, 模型」体例**）。MATLAB 条目只给 `[release]` |
| 5 | 有 | Claude、ChatGPT 两条均给出 `Query:`/`Output:` 字段 |
| 6 | 有 | DeepL 条目为陈述式，未要求 Query |
| | **4 / 6** | |

### Run B（冷启动基线）逐条判定

| # | 判定 | 说明 |
| :--- | :--- | :--- |
| 1 | 有 | 给了行内引用段（含 `[AI1]–[AI4]`） |
| 2 | 有 | "附在 25 页之后，不限页数、不计入 25 页" |
| 3 | 有 | 标题逐字为 `Report on Use of AI` |
| 4 | **无** | 三要素不齐：Copilot 条目只有 `<version>`、**无模型名**；MATLAB **被整条排除**（见下） |
| 5 | 有 | Claude（Query 1/Output 1 + 续问）、ChatGPT 两条均给出 `Query:`/`Output:` 字段 |
| 6 | 有 | DeepL 条目陈述式，并写明"no input query is reproduced for translation-only use" |
| | **5 / 6** | |

### 两次基线共同暴露的缺失项（skill 必须补掉）

除上表 6 项外，两次基线还暴露了下列**不在 6 项表内、但确属错误**的行为。这些是 skill 正文的直接取材来源：

| 编号 | 实测失败 | 依据 | 涉及基线 |
| :--- | :--- | :--- | :--- |
| F1 | **标题不稳定**：Run A 写 `Report on Use of AI Tools`（错），Run B 写 `Report on Use of AI`（对）。无 skill 时标题是掷硬币 | `[官方]` §2.4.4、§3 冲突 3 | A、B |
| F2 | **「工具名 + 版本/日期 + 模型名」体例不成立**：把「版本/日期」写成「访问日期」；多个工具缺模型名字段 | `[官方]` §2.4.5 | A、B |
| F3 | **数学软件被误排除**：Run B 专设第 6 条「Software not covered by this report」，把 MATLAB Optimization Toolbox 明确排除在披露之外，并叮嘱"不要列为 AI 使用"。这与 §2.4.1（`[官方]`，数学软件在披露范围内）**直接冲突**，且与队伍自己的使用记录相悖 | `[官方]` §2.4.1 | B（Run A 正确地保留了 MATLAB） |
| F4 | **自创引用体系**：Run B 凭空引入 `[AI1]–[AI4]` 平行编号与"首页脚注亦可"的写法，无官方出处 | `[官方]` §2.4.2（只要求 inline citation + reference section，未规定编号体系） | B |
| F5 | **杜撰 LaTeX 机制**：Run B 声称 `mcmthesis` 宏包内置 `\AIcite{AI1,...}`。本项目语料只能证到 `mcmthesis` 有名为 `ReportAiUse` 的**环境**（`INDEX.md` §3 冲突 3），**没有**任何 `\AIcite` 命令的依据 | §3 冲突 3 | B |
| F6 | **输出形状是三段还是四段不确定**：两次基线都把「给队伍的行动建议」（Run A 的"必须提醒队伍的两点"、Run B 的"必须由队伍补齐的三处"）与「要放进论文的内容」混在同一份输出里，没有先钉死"论文成品"的形状 | `[官方]` §2.4.2（要求的是**论文内的**三处内容） | A、B |

### 结论

两次基线在 6 项表上分别是 **4/6** 与 **5/6**，**没有一次全中**；且两次的失分点不同（A 错标题 + 错体例，B 错体例 + 错排除数学软件），说明**无 skill 时格式是随机的**。此外 F1–F6 六项系统性失败中，F1、F3 属于会直接影响合规与评分的实质性错误。

因此 skill 正文必须**先钉死输出形状**（三段、逐工具的字段清单、标题逐字），再给规则——这正是 Step 4 的契约式写法的依据。

---

## 偏离与顾虑

**D1（重要）：Run A 被 subagent 自行污染。** 我方派发 prompt 只含场景正文（已按要求执行），但该 subagent 具备工具权限，**自行决定**探索仓库并读取了 `corpus/official/Contest_AI_Policy.txt`。因此 Run A 是「**手里已有官方原文**的无 skill 基线」，而非冷启动基线。它仍失分 2 项，恰说明官方 PDF 单独存在时并不足以定对格式（尤以标题为然——PDF 侧恰是 §3 冲突 3 的**错误侧**）。为补足冷启动证据，追加了 Run B（远端隔离，无本仓库语料）。**若项目要求基线必须完全冷启动，则应以 Run B 为准，Run A 作旁证。**

**D2：第 4、5 项的口径张力。** §2.4.6（`[官方]`）说"非翻译用途须给出 Query 原文与 Output 全文"，但政策自身范例 4（GitHub CoPilot，`Contest_AI_Policy.txt:101-102`）对**代码补全**只给了一句陈述、并无 Query/Output。两条官方材料在此不完全齐平，而 §3 冲突登记**未**收录这一处。本次判定采用的口径是：**文本输入→文本输出的非翻译用途（润色、咨询）必须给 Query/Output；代码补全类按官方范例 4 以陈述式说明即为合格**。若项目认为应对代码补全也强制 Query/Output，则两次基线的第 5 项都应改判为"无"，且 skill 需相应改写。

**D3：Run B 的远端基线无法复用本地语料。** 它引用的是网络来源（含第三方镜像），其中 `\AIcite` 一说与本项目语料不符（见 F5）。本记录只把 Run B 当作**无 skill 时的行为样本**使用，**不**采纳其任何事实主张。

---

# GREEN 记录（Step 5–6）

- 条件：**全新 subagent**，prompt = 场景正文 + 一句「动手前先读取 `.claude/skills/mcm-ai-disclosure/SKILL.md` 并遵循」+ 一句「全文逐字贴出、不要省略」
- skill 版本：本次 GREEN 所跑的即本文「SKILL.md 最终内容」一节所载版本（105 行）

## GREEN 原始输出（hand-back 全文，逐字）

> 已按 `D:\Projects\数学建模\.claude\skills\mcm-ai-disclosure\SKILL.md` 产出，事实依据追溯到 `D:\Projects\数学建模\corpus\official\INDEX.md` §2.4、§3.1 冲突 3，并核对官方原文 `D:\Projects\数学建模\corpus\official\Contest_AI_Policy.txt`（v102025）行 54-58、81-86、88-102。
>
> 以下为拟放进论文的内容全文（逐字，无省略）。
>
> ## ① Inline citations — 在 25 页正文内，插在每个实际使用点（编号与 ② 一致）
>
> 置于 Introduction 开头（首次提到译文来源处）：
>
> > The present report was translated from the team's Mandarin manuscript.[1]
>
> 置于 Introduction 末尾（或摘要之后、正文首次出现润色说明处）：
>
> > The language of the Abstract and of this Introduction was polished with the assistance of an AI tool listed in the References.[2]
>
> 置于 TOPSIS 评价模型建模一节：
>
> > The computational steps of the TOPSIS method were verified against <ref. X>; the team also consulted ChatGPT on these steps while developing the evaluation model.[3]
>
> 置于数值求解／代码实现一节：
>
> > The Python code used to solve the model was written by the team, with inline auto-completions from GitHub Copilot.[4]
>
> 置于数值结果一节：
>
> > The optimization model was solved with MATLAB's Optimization Toolbox.[5]
>
> ## ② References 章节中的条目 — 在 25 页正文内
>
> ```
> [1] DeepL SE, DeepL Translator (<version>). Used to translate the team's Mandarin manuscript into English.
> [2] Anthropic Claude (<version>, <model>). Used to polish the language of the Abstract and of the Introduction.
> [3] OpenAI ChatGPT (<version>, <model>). Consulted on the computational steps of the TOPSIS method.
> [4] GitHub Copilot (<version>, <model>). Auto-completions for the Python code used in preparing our models.
> [5] The MathWorks, MATLAB with Optimization Toolbox (<version>). Used to solve the optimization model reported in this paper.
> ```
>
> ## ③ 追加章节 — 位于 25 页正文之后
>
> ```
> Report on Use of AI
>
> This section is appended after the 25-page solution in accordance with COMAP's policy on the use of AI tools. It has no page limit and is not counted as part of the 25-page solution.
>
> 1. DeepL SE, DeepL Translator (<version>)
>    Uploaded the entire paper, written in Mandarin, to be translated into English.
>
> 2. Anthropic Claude (<version>, <model>)
>    Language polishing of the Abstract and of the Introduction.
>    Query: <insert the exact wording you input into the AI tool> (reconstructed from team notes; exact wording not retained)
>    Output: <insert the complete output from the AI tool> (reconstructed from team notes; complete output not retained)
>
> 3. OpenAI ChatGPT (<version>, <model>)
>    Consultation on the computational steps of the TOPSIS method.
>    Query: <insert the exact wording you input into the AI tool> (reconstructed from team notes; exact wording not retained)
>    Output: <insert the complete output from the AI tool> (reconstructed from team notes; complete output not retained)
>
> 4. GitHub Copilot (<version>, <model>)
>    Auto-completions for the Python code used in preparing our models.
>
> 5. The MathWorks, MATLAB with Optimization Toolbox (<version>)
>    Used to solve the optimization model reported in this paper.
> ```
>
> ## 以下内容不属于论文（成品之外另附）
>
> 1. 尖括号处填实际值，体例照官方范例 `(Nov 5, 2023 version, ChatGPT-4)`，即「版本 + 模型」；**不是** `Accessed [date]`。DeepL 为纯翻译软件、无独立模型名，以版本/日期充该字段（官方范例 1 即 `Baidu Fanyi, Baidu Translate (Sep 10, 2025 version)`）；MATLAB 写版本号如 `R2024b`；Copilot 与 Claude、ChatGPT 均须写出模型名。
> 2. `[1]`–`[5]` 若与论文既有参考文献表编号冲突，按实际位次重编号，并同步改 ① 的正文标记。
> 3. Claude 与 ChatGPT 两条的 Query/Output：若当时留了逐字记录，把原文与完整输出填入；若确未留存，保留上文的如实标注，**不要**补写看似合理的 prompt——编造 prompt 本身即披露失实。
>
> ## 关键取舍（相对无 skill 基线易错处）
>
> - 标题逐字用 `Report on Use of AI`，不写 `Report on Use of AI Tools`（政策 PDF 侧是被否的一侧，`INDEX.md` §3.1 冲突 3：年度 instructions + Tips 2 票对 1 票）。
> - 翻译类（DeepL，含整篇中译英）为一句陈述、不附 Query；润色（Claude）与咨询（ChatGPT）两类必须给 Query + Output；代码补全（Copilot）按官方范例 4 用陈述式。
> - MATLAB 作为数学软件保留在披露内，未以"不是生成式 AI"为由排除（政策把 mathematics software 与 translation software 并列为在内）。
> - 三处内容同处一稿：正文 inline citation、25 页内 References 条目、25 页之后追加章节，缺一不可。
> - 未编造版本号、模型名与 Query/Output 原文，一律用尖括号占位并加如实标注。

## GREEN 逐项判定（对照上文同一张 6 项表与同一套判定口径）

| # | 判定 | 依据（GREEN 输出中的对应处） |
| :--- | :--- | :--- |
| 1 | **有** | ① 给出 5 条**就地**插入的正文引用句（Introduction 开头/末尾、TOPSIS 节、代码节、数值结果节），编号与 ② 一致 |
| 2 | **有** | ③ 标题独立成节，正文写明 "appended after the 25-page solution … has no page limit and is not counted as part of the 25-page solution" |
| 3 | **有** | 标题逐字为 `Report on Use of AI`（未写 `...AI Tools`） |
| 4 | **有** | 逐工具齐三要素：[2] Claude `(<version>, <model>)`、[3] ChatGPT 同、[4] Copilot `(<version>, <model>)`（基线里 Copilot 缺模型名，此处已补）；[1] DeepL 与 [5] MATLAB 为无独立模型名的工具，以版本充该字段（符合本记录「判定口径」栏） |
| 5 | **有** | [2] Claude 与 [3] ChatGPT 两条均给出 `Query:` 与 `Output:` 两字段，且未编造、加如实标注；[4] Copilot 按官方范例 4 用陈述式（符合判定口径） |
| 6 | **有** | [1] DeepL 为一句陈述 "Uploaded the entire paper, written in Mandarin, to be translated into English."，**未**附 Query |
| | **6 / 6** | **通过** |

## 对 RED 暴露的 F1–F6 的复验

| 编号 | 基线失败 | GREEN 复验 |
| :--- | :--- | :--- |
| F1 | 标题不稳定（A 错 / B 对） | 已消除：逐字 `Report on Use of AI` |
| F2 | 「版本/日期」写成「访问日期」、缺模型名 | 已消除：体例改为 `(<version>, <model>)`，并显式说明"**不是** `Accessed [date]`" |
| F3 | 数学软件被整条排除 | 已消除：MATLAB 作为数学软件保留在 ③ 第 5 条，并说明不得以"非生成式 AI"排除 |
| F4 | 自创 `[AI1]–[AI4]` 平行编号体系 | 已消除：`[1]`–`[5]` 与参考文献表同体系 |
| F5 | 杜撰 `\AIcite` 宏包命令 | 已消除：未出现任何宏包命令 |
| F6 | 成品与"行动建议"混作一稿 | 已消除：①②③ 为论文成品；建议另立「以下内容不属于论文（成品之外另附）」一节 |

## GREEN 阶段结论

**6 项全中，通过（Step 6）。** 无需回到 Step 4 补写，未做迭代。

---

# SKILL.md 最终内容

即 `.claude/skills/mcm-ai-disclosure/SKILL.md` 当前内容，105 行。frontmatter 与正文全文见该文件本身（本记录不复制，避免两处内容漂移）。

# 实测命令输出（Step 7）

```
$ cd "D:/Projects/数学建模" && awk '/^---$/{n++} n==1' .claude/skills/mcm-ai-disclosure/SKILL.md | head -5; echo "--- 行数 ---"; wc -l < .claude/skills/mcm-ai-disclosure/SKILL.md
=== frontmatter ===
---
name: mcm-ai-disclosure
description: Use when 需要撰写、补写或核查美赛 MCM/ICM 的 AI 使用披露（AI 使用声明、披露章节、AI disclosure），或按 COMAP AI policy 检查论文是否已正确声明 AI 工具使用。Triggers include AI 使用声明、披露、Report on Use of AI、AI disclosure、COMAP AI policy、AI 工具声明、翻译软件披露、数学软件披露。
--- 行数 ---
105
```

```
$ desc=$(awk '/^description: /{sub(/^description: /,""); print}' .claude/skills/mcm-ai-disclosure/SKILL.md) && echo "$desc" | wc -c; case "$desc" in "Use when"*) echo YES;; *) echo NO;; esac
364
YES
```

判定：frontmatter 仅含 `name` 与 `description` 两项；`description` 以 `Use when` 开头、长度 **364 字符 < 500**、含中英触发词；正文 **105 行 < 150**。**全部达标。**

---

# GREEN 复跑（修复轮次 1）

- 日期：2026-09-22
- 触发原因：`SKILL.md` 经独立审查判定 **Needs fixes**（输出契约的"括号例外"与规则表、检查清单三处互相打架，③ 缺页数声明句，mcmthesis 段越出语料，若干措辞与出处问题）。修复后按简报 Step 5 复跑 GREEN。
- 所跑版本：sha1 `7a1cbe7923ce340a0007671da274c7c1c6f31794`，**108 行**（上节记录的 105 行系修复前版本）
- 派发方式：**全新** `general-purpose` subagent（**非** `fork`）。prompt = `tests/scenarios/ai-disclosure-baseline.md` 的**场景正文（与 Step 1 完全相同的正文，逐字）** + 一句「动手前先读取 `.claude/skills/mcm-ai-disclosure/SKILL.md` 并严格遵循该 skill」。按简报 Step 5 要求，**未**加"全文逐字贴出、不要省略"之类的话。
- **所跑即冻结版**：本轮 GREEN 只认上列 sha1 的文件。此前另跑过一次**试点**，其时所读 SKILL.md 与冻结版只差规则 5b 出处栏的一处指针（试点版写"`INDEX.md` §3 未收录此冲突"；冻结前已改为指向 `INDEX.md` §3 伪冲突 7，因为审查期间 `INDEX.md` 被同步修订、§3.2 新增伪冲突 7，原句已不成立）。试点输出同为 6/6，本记录不重复收录其全文。

## 复跑原始输出（hand-back 全文，逐字；hand-back 框架统一缩进两格，此处已还原）

```
已按 mcm-ai-disclosure skill 产出，三部分齐全（正文 inline citation + References 条目 + 25 页后追加章节）。以下为论文内容。

════════════════════════════════════
① 正文内 inline citation（置于 25 页正文内，就地插入）
════════════════════════════════════
编号与 ② 一致；下面每句插在对应使用点所在句末。

[Introduction，末尾关于本稿写作过程的一句]
…this report was first drafted in the team's native Mandarin and was translated into English with DeepL.[9] The Summary and the Introduction were subsequently polished for language and clarity with Claude.[10]

[Methodology / TOPSIS 小节]
…the computational steps of the TOPSIS method were confirmed against a procedural description consulted via ChatGPT.[11]

[Model Solution / 求解小节]
…the Python solver was written by the team, with inline auto-completions provided by GitHub Copilot.[12]

[Model Solution / 结果小节]
…the optimization model was solved with MATLAB's Optimization Toolbox.[13]

════════════════════════════════════
② References 章节内的 AI 工具条目（置于 25 页正文内）
════════════════════════════════════
每件工具一条，续排在现有参考文献之后：

[9] DeepL SE, DeepL Translator (<version/date>). Uploaded the entire paper written in Mandarin to be translated into English.
[10] Anthropic Claude (<version/date>, <model name>). Polished the language of the Summary and Introduction.
[11] OpenAI ChatGPT (<version/date>, <model name>). Consulted on the computational steps of the TOPSIS method.
[12] GitHub Copilot (<version/date>). Auto-completions for the Python code used in preparing our models.
[13] MathWorks MATLAB (R2024b). Solved the optimization model with the Optimization Toolbox.

════════════════════════════════════
③ 追加章节（排在参考文献与附录之后，作为论文最后一节）
════════════════════════════════════
Report on Use of AI

This section has no page limit and is not counted as part of the 25-page solution.

1. DeepL SE, DeepL Translator (<version/date>)
   Uploaded the entire paper written in Mandarin to be translated into English.

2. Anthropic Claude (<version/date>, <model name>)
   Query: reconstructed from team notes; exact wording not retained. The team's input asked the tool to polish the English of the Summary and Introduction.
   Output: reconstructed from team notes; complete output not retained.

3. OpenAI ChatGPT (<version/date>, <model name>)
   Query: reconstructed from team notes; exact wording not retained. The team's input asked the tool to explain the computational steps of the TOPSIS method.
   Output: reconstructed from team notes; complete output not retained.

4. GitHub Copilot (<version/date>)
   Auto-completions for the Python code used in preparing our models.

5. MathWorks MATLAB (R2024b)
   Solved the optimization model using the Optimization Toolbox.

════════════════════════════════════
以下不属于论文内容 —— 仅供队伍使用的填写与核查说明
════════════════════════════════════
1. 尖括号占位符必须替换，不得原样交稿：`<version/date>` 按官方体例填 `Sep 10, 2025 version` 这类版本/日期（**不是访问日期**，`Accessed [date]` 不是该字段）；`<model name>` 填实际所用模型（如 `ChatGPT-4`、`Claude Sonnet 4.5` 的写法）。MATLAB 一行的 `R2024b` 是我按 skill 给的形式填的示例，请改成你们实际用的版本号。
2. 编号：② 的 [9]–[13] 是接着"现有参考文献最后一条为 [8]"写的；实际按你们文献表末号续排，并**同步改 ① 的编号**，两处必须一致。
3. Query/Output：Claude（润色）与 ChatGPT（咨询）属**非翻译用途**，官方默认要求**逐字 Query + 完整 Output**。你们未留存原文，我按 skill 允许的形态如实标注 `reconstructed from team notes; exact wording not retained`——**没有编造 prompt**。若还能从聊天记录里取回逐字原文与完整输出，务必替换为真实文本；编造 prompt 属披露失实，风险高于如实留白。
4. 翻译（DeepL）与代码补全（Copilot）：按官方范例 1 与范例 4，**只给陈述式，不需要 Query/Output**；不必给翻译硬加 Query。MATLAB 属数学软件，官方明确在披露范围内，**不得**以"不是生成式 AI"为由删去。
5. 若你们知道 Copilot 背后的具体模型，可在 [12] 与 ③ 第 4 条补上模型名（官方范例 4 未写，故不写也合规）。
6. 章节标题只能是 `Report on Use of AI`，**不要**写成政策 PDF 里的 `Report on Use of AI Tools`（年度正文与 Tips 是采用侧，2 票对 1 票）；标题下必须保留那句页数声明。
7. 队伍仍需按官方要求核验 AI 生成内容与引用的准确性（`Contest_AI_Policy.txt:60-61`）；本机无 LaTeX 工具链，编译验证请在你们使用的网页端编译器上完成。
```

## 复跑逐项判定（对照上文同一张 6 项表；第 4 项口径见本节末「裁定点」）

| # | 判定 | 依据（复跑输出中的对应处） |
| :--- | :--- | :--- |
| 1 | **有** | ① 给出 5 条**就地**插在句末的引用标记（Introduction、TOPSIS 节、求解节、结果节），编号 [9]–[13] 与 ② 一致 |
| 2 | **有** | ③ 标题栏写明"排在参考文献与附录之后，作为论文最后一节"，且正文首句即页数声明 "This section has no page limit and is not counted as part of the 25-page solution." |
| 3 | **有** | 标题逐字为 `Report on Use of AI`（未写 `...AI Tools`），① 与 ③ 两处一致 |
| 4 | **有**（按 `INDEX.md` §2.4.5 口径） | 逐工具：[10] Claude `(<version/date>, <model name>)`、[11] ChatGPT 同——有模型者已留模型名字段；[9] DeepL、[13] MATLAB 无独立模型名，以版本/日期充该字段；[12] Copilot 只给 `<version/date>`——官方范例 4（`Contest_AI_Policy.txt:101`）本身即无模型名，`INDEX.md` §2.4.5 明示"部分代码补全/自动补全工具…以版本/日期充该字段即合规，**不得**因其缺模型名判为不合规"，故按现行 INDEX 判**有**。**但冻结版 SKILL.md `:41`/`:93` 的措辞严于 §2.4.5**，见本节末裁定点 |
| 5 | **有** | [10] Claude 与 [11] ChatGPT 两条均给出 `Query:` 与 `Output:` 两字段；[12] Copilot 按官方范例 4 用陈述式 |
| 6 | **有** | [9] DeepL 为一句陈述 "Uploaded the entire paper written in Mandarin to be translated into English."，**未**附 Query |
| | **6 / 6** | **通过** |

## 复跑对**修正后**检查清单的自检（逐条）

| 检查项 | 结果 | 说明 |
| :--- | :--- | :--- |
| ③ 标题逐字 `Report on Use of AI` | 过 | ① 与 ③ 均为 `Report on Use of AI` |
| ③ 排在所有计入 25 页材料之后、最后一节，且写明"不计入 25 页、无页数上限" | 过 | "排在参考文献与附录之后，作为论文最后一节" + "This section has no page limit and is not counted as part of the 25-page solution."（**修正 2 的声明句已由契约本身产出**，不再依赖 subagent 临场补写） |
| ① 就地引用标记、与 ② 编号对应 | 过 | [9]–[13] 两处一致 |
| ② 每件工具有独立条目 | 过 | 5 条 |
| ③ 每条齐 工具名 + 版本/日期 + 模型名 三要素 | **过（按 §2.4.5 口径）** | [12] Copilot 无模型名字段；理由同上表第 4 项。若按 `:41`/`:93` 的字面（"该工具确有模型者必须写出模型名"）判，则此项**不过**——见裁定点 |
| ③ 每条有明确用途说明 | 过 | 5 条均有 |
| 翻译类一句陈述、不要求 Query（非禁止）；非翻译类有 Query + Output（**代码补全类除外**） | 过 | DeepL 一句陈述无 Query；Claude/ChatGPT 有 Query+Output；Copilot 陈述式——**这正是修正 1 要验的一点**：修复前的 `:92` 会否证这一条，修复后不再 |
| 数学软件与翻译软件未被漏掉或排除 | 过 | MATLAB（[13]）与 DeepL（[9]）均在披露内 |
| Query/Output 未留存时如实标注、不得编造 | 过 | 两条均标 `reconstructed from team notes; exact wording not retained` |
| 输出只含①②③，未混入行动建议 | 过 | 行动建议另立于"以下不属于论文内容"一节（与上一轮 GREEN 同一处理口径） |

**结论：6 项全中，且通过修正后检查清单自检。**

## 复跑暴露的两个**未**由本轮修复触及的点（提交裁定，本轮**未**改）

**R1（与第 4 项及检查清单第 5 条直接相关）——SKILL.md 的模型名口径已严于现行 `INDEX.md` §2.4.5。** 审查期间 `INDEX.md` 被同步修订：§2.4.5 新增"**无独立模型名的工具（纯翻译软件、部分代码补全/自动补全工具等）以版本/日期充该字段即合规**，**不得**因其缺模型名判为不合规"，并明示范例 4（GitHub CoPilot）无模型名。冻结版 SKILL.md 的 `:41`（"该工具确有模型者必须写出模型名；**纯翻译软件**无独立模型名者…"）与 `:93`（"③ 每条齐 工具名 + 版本/日期 + 模型名 三要素"）**未**包含"部分代码补全/自动补全工具"这一档，故按字面会否证一个合规的 Copilot 条目。本轮**只**按简报列出的条目改，未擅自扩到此处。一行即可对齐：把 `:41` 的"纯翻译软件无独立模型名者"改为"无独立模型名者（纯翻译软件、部分代码补全/自动补全工具等）"，并在 `:93` 后加"（无独立模型名者以版本/日期充该字段）"。

**R2——同一 mcmthesis 断言仍留在另两份非 skill 文件中。** `corpus/official/INDEX.md:199` 已由你方删去该断言；但 `docs/superpowers/specs/2026-09-22-mcm-skill-suite-design.md:365`（"其内建的 `ReportAiUse` 环境与 `\AIcite` 命令…可用"）与 `tests/results/ai-disclosure-baseline.md:246`（本文件 F5 行，称"本项目语料只能证到 `ReportAiUse` 环境"）仍作同样断言，来源均落在 `corpus/official/` 之外。本轮未动（不在清单内）。

**另记（不构成失分）**：复跑把 MATLAB 版本写成实值 `R2024b` 而非占位符，它在成品之外如实说明"是我按 skill 给的形式填的示例，请改成你们实际用的版本号"，未充当已验证事实。
