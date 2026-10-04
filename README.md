# MathModel

2027 美赛（MCM/ICM）自用的 **Claude Code skill 套件** 与 **语料流水线**。

把"比赛那四天该怎么走"拆成 **17 个 skill** —— 每个只管一件事、给一套能指着说清的判断；**绝大多数**配**机械判据**与**证据件**（**三个合规 skill 例外**，见「怎么用」一节）。

---

## 目录结构

| 目录 | 内容 |
| :--- | :--- |
| `.claude/skills/` | **17 个 skill**（见下节） |
| `tests/skills/` | **多数 skill**的**逐条正反样例**、**变异驱动器**、**RED/GREEN 证据件**。★ **判据脚本有两种落点**：**各 6 个 skill** 分别把 `check-*.py` 放在 `.claude/skills/<名>/` 与 `tests/skills/<名>/`（后者含一个 skill 自带 4 个检查器的情况，故**文件数多于 skill 数**）；★ **剩下 5 个 skill 在各自名下没有 `check-*.py`** —— 其中 **3 个合规 skill 连共享判据也没有**（见「怎么用」），另 2 个（`mcm-plot-origin` · `mcm-schematic`）是绘图家族成员，**由家族共享判据覆盖** |
| `tests/`（其余） | 各模块的侦察/探针件（MATLAB·Origin·字体·绘图语料） |
| `tools/papers/` | 语料流水线（水印处理 · 正文抽取 · 图表/公式/索引） |
| `docs/` | 设计件与计划件（`docs/superpowers/{specs,plans}/`）· 待办台账 · 写作纪律 |
| `corpus/` | 语料 —— ★ **绝大部分不入远端**（见"这个仓库里没有什么"） |
| `build/` | 临时产物（`.gitignore` 已忽略） |

---

## 17 个 skill

### 绘图家族（5 个）

这五个受**同一条家族规则**约束（互相给指针；家族内不许出现无出处的数字）：

| skill | 干什么 |
| :--- | :--- |
| `mcm-plot-python` | 用 Python 出图、把图型决策落成 matplotlib 代码 |
| `mcm-plot-matlab` | 用 MATLAB 出图、把图型决策落成 MATLAB 代码 |
| `mcm-plot-origin` | 用 Origin 出图、把图型决策落成 Origin 脚本 |
| `mcm-table` | 排版表格、把数据落成可直接粘的 LaTeX 表格代码 |
| `mcm-schematic` | 把"过程 / 结构 / 机理"的描述落成可直接粘的 TikZ 示意图源码 |

### 家族外（12 个）

| skill | 干什么 |
| :--- | :--- |
| `mcm-playbook` | 赛程中回答"**现在该干什么**"——处在哪个阶段、该做哪几件事、该调哪个 skill |
| `mcm-topic-select` | 开赛后从六道题里**挑一道**，并说清"为什么是它" |
| `mcm-data` | **数据侧**：题面没给的数据怎么找、附件怎么读、统一落成一张数据来源表 |
| `mcm-model-select` | 建模阶段从题面特征**选出候选模型**，说清"为什么用它 / 什么时候不该用它" |
| `mcm-code` | **代码侧**：写求解代码、结果落盘、编号与论文对齐、附录里的代码怎么处置 |
| `mcm-figure-choose` | 决定"**这组数据该画成哪种图**"（图型选型，不是画图） |
| `mcm-section-writer` | 写论文的**某一节正文**（不是整篇）——这一节该回答什么、按什么次序组织 |
| `mcm-abstract` | 写或复核**摘要页**——正文与结果完成之后定稿 |
| `mcm-memo` | **题面明确要求 letter/memo 时**起草一页备忘录（★ 题面没要求就绝不产出） |
| `mcm-latex-format` | 搭 LaTeX 骨架、排版初稿、格式合规检查 |
| `mcm-ai-disclosure` | 撰写 / 核查**AI 使用披露**（按 COMAP AI policy） |
| `mcm-selfreview` | 提交前对论文稿做**最后自查**，判断"能不能提交" |

---

## 环境需求

### 必需

**Python 3.11**（本机实测 `3.11.9`；仓内没有声明版本下限的文件，这里只报实测值）。工具链与判据脚本用到的第三方包（逐个实测可 import）：

| 包 | 实测版本 | 用途 |
| :--- | :--- | :--- |
| `numpy` | 2.3.5 | 数值 |
| `scipy` | 1.17.1 | 数值 |
| `pandas` | 3.0.5 | 表格数据 |
| `matplotlib` | 3.10.7 | 出图 |
| `SciencePlots` | 2.2.2 | 绘图样式表 |
| `Pillow` | 12.3.0 | 位图 |
| `PyMuPDF` (`fitz`) | 1.27.2.3 | PDF 处理（语料流水线） |
| `pywin32` | — | 窗口/进程（Origin 探针） |

### 可选，但某些 skill 需要

| 依赖 | 谁需要 | 现状 |
| :--- | :--- | :--- |
| **MATLAB** | `mcm-plot-matlab`；`mcm-model-select` 的 66 个骨架与参照记录 | ★ **版本未实测**（本机跑 MATLAB 会崩，见下）。要求：本机已装且 `matlab -batch` 可用 |
| **TeX Live** | LaTeX 骨架、表格、示意图（`mcm-latex-format` / `mcm-table` / `mcm-schematic`） | 实测 **TeX Live 2026**（pdfTeX 3.141592653-2.6-1.40.29） |
| **Origin** | `mcm-plot-origin` 的自动化路径 | `originpro` 包 **未装**（脚本路径不可用；换成手工导出） |

**随仓入库的字体**：`mcm-plot-python/assets/fonts/` 下 4 个 OTF（TeX Gyre Termes X 的 Regular / Italic / Bold / BoldItalic），同目录有 `PROVENANCE.md` 与 `GFL.txt` / `LPPL.txt` 两份许可原文。

**已知未装的包**（**是有意为之**，不是缺陷）：`statsmodels` · `cvxpy` · `pulp` —— 统计推断 / 凸优化 / 规划这三类的代码骨架**改用 MATLAB 写**，所以不引这三个 Python 依赖。

> ⚠️ **本机 MATLAB 不稳定**：开发期间出现过多次崩溃（含一次在 **MATLAB 退出期**自崩，会把崩溃转储写进正在生成的证据件）。⇒ 跑任何拉 MATLAB 的命令后，**先看 `git status` 再提交**。

---

## 怎么用

### 1. 调用 skill

skill 放在 `.claude/skills/`，**在 Claude Code 里用**。触发方式是**自然语言**：每个 `SKILL.md` 的 frontmatter 写了两段——
`Use when …`（什么条件下该用）与 `Triggers include …`（一批中英文触发短语）。

本仓**没有**自行注册 slash 命令（`.claude/` 下没有 `commands/`）。所以：

- **把需求直接说出来就行** —— 命中 `Triggers` 就自动调用（例：说"这组数据该画成什么图"→ `mcm-figure-choose`；说"现在该干什么"→ `mcm-playbook`）。
- 也能**显式点名**某个 skill。

★ **除下面那三个合规 skill 外**，每个 `SKILL.md` 里都写了"**不用**"（什么时候**不**该用它、该转给谁）——那是这套件的重点之一。
（例外：`mcm-ai-disclosure` · `mcm-latex-format` · `mcm-selfreview` 这三份**没有**这一节。）

★ **这三个 skill 同时也是全库仅有的三份「没有常驻机械门」的**：既没有自己的 `check-*.py`，`tests/skills/` 下也没有对应目录；它们只有一次性的 RED 基线（在 `tests/results/` 下）。这是**设计上的取舍**（当初只要求"造一份违规样稿"验一次），不是遗漏 —— 但**改坏了没有判据会红**，用它们时心里有数。

### 2. 跑判据

判据脚本**多数**以 `RESULT: PASS` 或 `RESULT: FAIL（…）` 收尾，退出码 0 / 1（个别另有 exit 2 = fail-closed 且不打印判词）。
★ **三处已知例外**（FAIL 态末行是 `失败项=…`，`RESULT: FAIL` 在它上一行）：**`check-summary.py` · `check-memo.py` · `check-section.py`** —— 脚本序读 `RESULT:` 时别只认最后一行。三种典型调用：

```bash
# 不带参数
python tests/skills/check-writing-discipline.py
python tests/skills/figure-choose/check-spec-pointers.py

# 带 --scope（内检 / 外检）
python .claude/skills/mcm-data/check-data.py --scope self
python .claude/skills/mcm-data/check-data.py --scope artifact <数据来源表.md> --refs <论文.md>

# 带文件与其它参数
python .claude/skills/mcm-section-writer/check-section.py <产出.md> --section 模型建立 --input <题面简报.md>
```

### 3. 跑变异驱动器

驱动器的作用是**证明判据真的会红**（而不只是"看起来能失败"）：它逐条把样例改坏、要求对应判据翻红，再断言**合规侧确实绿**。

```bash
python tests/skills/data/mutate-data.py
python tests/skills/code/mutate-code.py
```

末行同样是 `RESULT: PASS` / `RESULT: FAIL`；上面一行是 `RUN: 判据 … · 违规侧红 … · 合规侧绿 … · 控制项 …` 的汇总。

### 4. 全仓检查一次跑完

**没有一键脚本** —— 是一串命令，登记在各模块计划的「**收工门**」里，可直接复制粘贴执行。
最新、且收工门清单最完整的一份（**自成一块、可整段复制**的 32 条命令）在：**`docs/superpowers/plans/2026-10-04-m5-data-code.md`** 的 `## Global Constraints` 第 16 条。

★ 那份清单**自称不声称穷尽全仓脚本**，并明列**两个不在表内的真实驱动器**（`tests/skills/plot-python/mutate-plot-style.py` · `tests/skills/plot-matlab/mutate-plot-style.py`）——属**已知缺口**，不是遗漏。

### 5. 移植到别的 agent（Codex / Cursor / Gemini CLI …）

★ **先说结论**：**内容可移植，触发方式不可移植。**

**它为什么可移植**：这套 skill 的 `SKILL.md` frontmatter **只有 `name` 与 `description` 两个字段**，没有 `model` / `hooks` / `allowed-tools` 这类 harness 专有字段 —— 也就是说它**符合跨工具的 `SKILL.md` 约定**（`Agent Skills` 开放标准），正文全是纯 Markdown + 仓内相对路径。**判据与驱动器更是 29 个纯 Python 脚本，跟哪个 agent 无关。**

**它为什么不可移植**：skill 放在 **`.claude/skills/`** —— 那是 **Claude Code 的目录约定**，别的工具**不扫这个路径**，所以**不会自动触发**。

**三条移植路径**（按成本从低到高）：

| 做法 | 怎么做 | 效果 |
| :--- | :--- | :--- |
| **① 借用标准位置** | 让 `.agents/skills/` 指向 `../.claude/skills`（符号链接或复制） —— `.agents/skills/` 是这套 `SKILL.md` 标准**跨工具的可移植位置** | 认该标准的工具（Gemini CLI 等）能**自动发现**这些 skill |
| **② 写一份 `AGENTS.md` 指路** | 在仓根放 `AGENTS.md`，把"要做什么 → 去读哪个 `.claude/skills/<名>/SKILL.md`"列成一张表 —— `AGENTS.md` 是**当前跨工具的事实标准**，Codex / Cursor / Gemini CLI / Windsurf / Copilot / Aider / Zed / Warp / Roo / Junie / Amp 等都读它 | 把"**自动触发**"降级成"**显式指路**"，但**覆盖面最广** |
| **③ 各 harness 自己的入口** | `GEMINI.md` 等 —— 常见做法是里面只写一行 `@AGENTS.md`（导入）或做成符号链接，让**共享内容只有一份** | 与 ② 配合用，避免同一套规则抄 N 遍 |

★★ **两个必须知道的坑**：

- **Codex 不读 `.claude/` 目录**（也不读 `.cursor/`）⇒ 路径 ① 对它未必生效，**路径 ② 才是对 Codex 的正解**。
- `AGENTS.md` 默认有 **32 KiB 的加载上限**（超出会被静默截断）⇒ **别把整套内容抄进去**，写成**指路的索引**就好。

★★ **诚实边界**：**以上三条我们【没有实测过】** —— 本仓从没在 Claude Code 之外的 agent 上跑过这套 skill（`find . -iname "*AGENTS*" -o -iname "*codex*"` 为空）。这一节是**按各工具公开的约定写出的配方**，不是"我们验证过能用"。

**这些说法的出处**（外部工具的约定，非本仓事实）：
[Codex CLI · Custom Instructions](https://mintlify.wiki/openai/codex/advanced/custom-instructions) ·
[AGENTS.md 的跨工具采用面](https://docs.crewai.com/v1.15.22/en/guides/coding-tools/agents-md) ·
[Gemini CLI 配置](https://opensource.adobe.com/mysticat-ai-native-guidelines/04-configuration/ai-tools/gemini-cli/) ·
[跨 harness 的 skill 兼容性矩阵](https://raw.githubusercontent.com/speclabs/devspec/main/devspec/adapters/compatibility-matrix.md)

**换 agent 会丢什么、不会丢什么**：

| | 换 agent 后 |
| :--- | :--- |
| **判据 / 变异驱动器 / 证据件** | ★ **不丢** —— 纯 Python，任何终端都能跑 |
| **内容准确度**（那两条硬约束守的东西） | ★ **不丢** |
| **"喊一声它自己找上门"**（自然语言自动触发） | ✗ **丢** —— 得靠上面的 ① 或 ② 补回来 |

---

## 这个仓库里**没有**什么（有意为之）

**第三方语料绝大部分不上传。** 远端 `corpus/` 只保留**索引、净室件与论文正文抽取**这三类派生件，外加来源/许可说明（含净室件自己的一份 `README.md`）与一份转码表
（实测：`corpus/` 下共 59 个文件，其中非 `INDEX.md` 的 56 件 = 算法 9 + 论文 47）。

| 未上传 | 本地体量 | 原因 |
| :--- | ---: | :--- |
| COMAP 获奖论文 201 份（2022–2025 O 奖 + UMAP 期刊） | 约 **1.7 GB** | 第三方版权 |
| COMAP 官方赛题与数据附件（2016–2026） | 约 **108 MB** | 第三方版权 |
| 获奖论文的**整页渲染图** | 约 **164 MB** | 派生复制品 |
| 第三方算法源码（`corpus/algorithms/src/`） | 约 **4.7 MB**（连同索引与净室件，整个 `corpus/algorithms/` 是 **4.9 MB**） | 上游未声明许可（默认保留所有权利） |

**已经上传的派生件**（与旧版 README 的说法不同，这里如实更正）：

- **获奖论文的正文抽取**（43 份 `.md`）**已入库** —— 渲染图仍不入库；
- **净室重写版算法**（`corpus/algorithms/fixed/` 下 6 个 `.m`）**已入库** —— 原始 `src/` 不入库。

★ 各语料的**来源、许可状态与可复现步骤**见对应目录下**若有**的 `PROVENANCE.md`。
★ **不声称穷尽**：本地 5 堆语料里，`algorithms` / `papers` / `官方原题` 三堆有 `PROVENANCE.md`，另两堆（`official` · `历届优秀论文`）**没有**。

---

## 两条贯穿全项目的硬约束

**① 语料产物一律字节级写入**（`write_bytes`），并配 `.gitattributes` 的 `-text`。

> 起因：本项目踩过 `core.autocrlf` 把 883 个文件写成 `\r\r\n` 的事故，一度误判为上游代码问题。

**② 判据不得"看起来能失败"就算数** —— 每条新增判据都必须用一次**变异**证明它真的会红（把被测对象改坏 → 跑一次 → 看它红不红）。

> 本项目已出现多次「判据在什么都没验的情况下报绿」。这条规矩立下**之后**仍然复发过，
> 所以现在**绝大多数模块**都配一个**变异驱动器**（`tests/skills/` 下 11 个），并要求它的判据总数**现取**（删掉一条即 FAIL）。
> ★ **例外**：**连共享驱动也没有的**只有 `mcm-abstract` 与上面那三个合规 skill（共 4 个）；另有 `mcm-plot-origin` / `mcm-schematic` 名下无专属驱动器，但其变异**由家族共享的 `mutate-figure-style.py` 覆盖**。属已知缺口。

---

## 文档去哪找

| 想找 | 去 |
| :--- | :--- |
| 这个套件怎么设计的 | `docs/superpowers/specs/` |
| 各模块怎么实施的 | `docs/superpowers/plans/` |
| **还欠什么、哪些是刻意不动的** | `docs/mcm-suite-todo.md`（**权威台账**） |
| 写作类要求以哪份为准 | `docs/mcm-writing-discipline.md` |
| 踩过的坑 | `docs/mcm-suite-lessons.md` |
