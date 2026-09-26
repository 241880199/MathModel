---
name: mcm-ai-disclosure
description: Use when 需要撰写、补写或核查美赛 MCM/ICM 的 AI 使用披露（AI 使用声明、披露章节、AI disclosure），或按 COMAP AI policy 检查论文是否已正确声明 AI 工具使用。Triggers include AI 使用声明、披露、Report on Use of AI、AI disclosure、COMAP AI policy、AI 工具声明、翻译软件披露、数学软件披露。
---

产出美赛论文的 AI 使用披露：**正文内引用标记 + 参考文献条目 + 25 页之后追加的披露章节**，三者必须同时存在、缺一不可。

本节所有事实的出处行号与分级见 `corpus/official/INDEX.md` §2.4（该节全部为 `[官方]`）；引用时写指针，不要另立说法。

## 输出

按序产出以下三部分。**先钉死形状再填内容**——形状不对，内容再对也不合格。

**① 正文 inline citation（在 25 页正文内）**

在**每个实际使用点**就地插入标注，不是只在开头写一句总声明。编号与 ② 的参考文献条目一致。

```
…the draft was translated from the team's Mandarin manuscript.[1]
…the optimisation model was solved with MATLAB's Optimization Toolbox.[5]
```

**② References / 参考文献章节中的 AI 工具条目（在 25 页正文内）**

每件工具**一条**，体例照官方范例 = `名称 (版本/日期, 模型名)` + 用途。三要素口径与 ③ 同：**该工具确有模型者必须写出模型名**；无独立模型名者（纯翻译软件、部分代码补全/自动补全工具等）以版本/日期充该字段；数学软件写版本号如 `R2024b`（见 `规则` 第 4 条）：

```
[3] OpenAI ChatGPT (Nov 5, 2023 version, ChatGPT-4). Consulted on the computational steps of the TOPSIS method.
```

**③ 追加章节（排在所有计入 25 页的材料之后——含参考文献与附录；作为论文最后一节）**

标题**逐字**为下面这一行，不加 `Tools`、不加任何前后缀；**标题之下先写一句页数声明**，再逐工具列条目：

```
Report on Use of AI

This section has no page limit and is not counted as part of the 25-page solution.
```

其下逐工具一条，**每条必须齐三要素：工具名 + 版本/日期 + 模型名**（该工具确有模型者必须写出模型名；无独立模型名者（纯翻译软件、部分代码补全/自动补全工具等）以版本/日期充该字段；数学软件写版本号如 `R2024b`）。然后按用途二选一：

- **翻译用途**（含整篇中译英）：**一句陈述即可**；官方**不要求**附 Query（**非禁止**，政策原文 `you are not required to include your full input query`）。
- **非翻译用途**（润色、咨询等文本输入→文本输出）：必须给两个字段——`Query:` 为**逐字输入原文**，`Output:` 为**完整输出**。**代码补全类除外**，照官方范例 4 用陈述式（见规则 5b 与 `常见失分点` 第 4 条）。

```
1. DeepL SE, DeepL Translator (Sep 10, 2025 version)
   Uploaded entire paper written in Mandarin to be translated into English.

2. OpenAI ChatGPT (Nov 5, 2023 version, ChatGPT-4)
   Query: <insert the exact wording you input into the AI tool>
   Output: <insert the complete output from the AI tool>
```

上两例的形态取自官方范例（`corpus/official/Contest_AI_Policy.txt:88-102`）。

**输出只含这三部分。** 给队伍的行动建议、留存提醒、风险提示一律不要在成品里出现——需要时在成品之外另附。

## 规则

| # | 规则 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 1 | **双位置披露**：正文内 inline citation + References 列出全部 AI 工具；两者缺一不可，只在末尾列参考文献**不算**完成 | `[官方]` | `INDEX.md` §2.4.2 |
| 2 | 追加章节**置于 25 页正文之后**——即排在**所有计入 25 页的材料（含参考文献与附录）之后**、作为论文**最后一节**；**无页数上限**；**不计入 25 页**。它是唯一不计入 25 页的章节 | `[官方]` | `INDEX.md` §2.4.3、§2.1.5 |
| 3 | 章节标题用 **`Report on Use of AI`** | `[官方]` | `INDEX.md` §2.4.4 |
| 4 | 披露须含**工具名 + 版本/日期 + 模型名**，并说明**用途** | `[官方]` | `INDEX.md` §2.4.5 |
| 5a | 非翻译用途须给 **Query 原文 + Output 全文**；翻译用途**只需一句声明**，官方**不要求**附 Query（**非禁止**） | `[官方]` | `INDEX.md` §2.4.6；`Contest_AI_Policy.txt:83-86` |
| 5b | **代码补全类除外**：官方范例 4（GitHub CoPilot）对代码补全只给陈述式，无须 Query/Output | `[官方]` | `Contest_AI_Policy.txt:101-102`；`:85-86`（`Examples … this is not exhaustive — adapt these examples to your situation`）。该例外与 5a 默认口径的关系见 `INDEX.md` §3 伪冲突 7：**有离散 prompt + 文本输出者必须给 Query/Output；工具本身无离散 Query 者给陈述式** |
| 6 | 队伍须自行核验 AI 生成内容与引用的准确性、有效性、适当性，并改正错误与不一致 | `[官方]` | `INDEX.md` §2.4.7 |

**标题不一致的已知冲突（必须按采用侧写）**：官方政策 PDF 作 `Report on Use of AI Tools`（`Contest_AI_Policy.txt:57-58`、`81-83`、`88`），年度正文与 Tips 作 `Report on Use of AI`（`instructions.html:1216`、`1239`；`MCM-ICM_Tips.txt:204`）。**本项目采用 `Report on Use of AI`**，理由与票数见 `INDEX.md` §3 冲突 3。不要因为政策 PDF 里写的是 `...Tools` 就跟着写——那是被否的一侧。

**全局约束（环境与来源）**：本机**已有** TeX Live 2026（2026-09-24 装，可本地编译自检）；凡声称编译结果须附真实命令与输出。用户**提交仍以网页端编译器为准**。**不得**引用任何未见于本项目语料的宏包命令（例如 `\AIcite` 之类）；`mcmthesis` 等宏包的 AI 披露环境与引用命令**以该宏包官方文档为准**，本 skill 不为 `ReportAiUse` / `\AIcite` 之类的包内机制背书。

## 触发范围

下列**每一类**只要用过，都触发披露义务，逐条写进 ③（依据 `INDEX.md` §2.4.1，`[官方]`）：

- **LLM / 生成式 AI**：ChatGPT、Claude、Gemini 等
- **翻译软件**：DeepL、百度翻译、Google 翻译等——**整篇中译英也在内**，政策原文明确适用于"把队伍母语译成英文"
- **数学软件**：**MATLAB 及其工具箱、Mathematica 等专用数学软件**——**属披露范围，不得以"不是生成式 AI"为由排除**。（产品名系本 skill 举例：**官方原文只列类别 "mathematics software"，未列举任何产品名**。）**边界说明**：官方列举 "mathematics software" 但**未澄清该边界**，故 Python / NumPy / SciPy 这类**通用语言与库**是否在内官方未表态（`INDEX.md` §2.4.1）——**不据此判不合规**，但建议队伍为避免风险一并披露
- **代码补全 / 自动补全**：GitHub Copilot、各类 IDE auto-complete
- **其它 AI 辅助技术**：含内嵌于上述软件的 AI 功能

范围覆盖从**研究、模型开发（含写代码）到书面报告**的各个环节（`INDEX.md` §2.4.1，`[官方]`）。队伍**自行记录**的工具清单是下限，不是上限：只要实际用过就写。

## 检查清单

- [ ] ③ 的标题**逐字**为 `Report on Use of AI`（不是 `...AI Tools`）
- [ ] ③ 排在**所有计入 25 页的材料（含参考文献与附录）之后**、作为论文**最后一节**，且已写明"不计入 25 页、无页数上限"
- [ ] ① 正文内有**就地**引用标记，且与 ② 的编号对应
- [ ] ② References 内每件工具有独立条目
- [ ] ③ 每条齐**工具名 + 版本/日期 + 模型名**三要素
- [ ] ③ 每条有明确的**用途**说明
- [ ] 翻译类条目为一句陈述，官方**不要求**附 Query（**非禁止**）；非翻译类条目有 Query + Output（**代码补全类除外**，照官方范例 4 用陈述式）
- [ ] 数学软件与翻译软件**未被漏掉或排除**
- [ ] Query/Output 处若队伍未留存原文，如实标注（如 `reconstructed from team notes; exact wording not retained`），**不得**编造
- [ ] 输出只含①②③，未混入行动建议

## 常见失分点

1. **标题写成 `Report on Use of AI Tools`。** 政策 PDF 就是这么写的，照抄 PDF 就会踩中；年度正文侧才是采用侧。`[官方]`（`INDEX.md` §2.4.4、§3 冲突 3）
2. **只在末尾列参考文献，正文内没有 inline citation。** 政策要的是"双位置"，两处都要。`[官方]`（`INDEX.md` §2.4.2）
3. **把「版本/日期」写成「访问日期」。** 官方范例的体例是 `(Nov 5, 2023 version, ChatGPT-4)`，即**版本 + 模型**；`Accessed [date]` 不是该字段。`[官方]`（范例体例：`INDEX.md` §2.4.5、`Contest_AI_Policy.txt:90-102`）／`[社区]`（"`Accessed [date]` 不是该字段"是**由范例体例推出的否定命题**，官方无对应原文表述，推算依据同前）
4. **给翻译类硬加 Query、或把润色/咨询类写成陈述式。** 官方范例 1 与范例 4 都是陈述式（翻译、代码补全亦然）；但**润色、咨询**这类文本输入→文本输出的用途必须给 Query + Output。反之，给翻译类**硬加** Query **并无必要，但不构成违规**（官方原文 `you are not required to include your full input query`）。`[官方]`（`INDEX.md` §2.4.6、§3 伪冲突 7；`Contest_AI_Policy.txt:83-86`、`90-102`）
5. **以"不是生成式 AI"为由排除数学软件。** 政策原文把 mathematics software 与 translation software 并列为在内；排除即漏披露，而漏披露的后果是官方明示的"appropriate action"、相关段落更易被判抄袭并取消资格。`[官方]`（`INDEX.md` §2.4.1、§2.4.8）
6. **整篇机器翻译当作"润色"一笔带过。** 翻译用途虽只需一句声明，但**必须披露**，且要写明是整篇译自母语。`[官方]`（`INDEX.md` §2.4.1、§2.4.6）
7. **凭空补写 Query/Output。** 政策要的是逐字输入与完整输出；编造 prompt 文本本身即属披露失实，风险高于如实留白。`[社区]`（推算自 `INDEX.md` §2.4.6 的"逐字原文"要求；官方无对应原文表述）
