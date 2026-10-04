# MathModel

2027 美赛（MCM/ICM）自用的 Claude Code skill 套件与语料流水线。

套件把比赛四天的流程拆成 **17 个 skill**：每个只负责一件事，给出一套能照着执行的判断，并配机械判据与验证证据。

---

## 目录结构

```
.claude/skills/     17 个 skill（每个含 SKILL.md，多数还带 references/ 与 assets/）
tests/skills/       判据脚本、逐条正反样例、变异驱动器、RED/GREEN 证据件
tests/              其余模块的侦察与探针件（MATLAB、Origin、字体、绘图语料）
tools/papers/       语料流水线（水印处理、正文抽取、图表、公式、索引）
docs/               设计件与计划件（docs/superpowers/）、待办台账、写作纪律
corpus/             语料（绝大部分不入远端，见「仓库边界」）
build/              临时产物（已 gitignore）
```

判据脚本有两种落点：6 个 skill 放在 `.claude/skills/<名>/`，6 个放在 `tests/skills/<名>/`。剩下的 5 个 skill 在各自名下没有判据脚本，其中 3 个（`mcm-ai-disclosure`、`mcm-latex-format`、`mcm-selfreview`）也没有共享判据，另 2 个（`mcm-plot-origin`、`mcm-schematic`）由绘图家族的共享判据覆盖。

---

## 17 个 skill

### 绘图家族

这五个 skill 受同一条家族规则约束：互相给出指针，家族内不出现没有出处的数字。

| skill | 用途 |
| :--- | :--- |
| `mcm-plot-python` | 用 Python 出图，把图型决策落成 matplotlib 代码 |
| `mcm-plot-matlab` | 用 MATLAB 出图，把图型决策落成 MATLAB 代码 |
| `mcm-plot-origin` | 用 Origin 出图，把图型决策落成 Origin 脚本 |
| `mcm-table` | 排版表格，把数据落成可直接粘贴的 LaTeX 表格代码 |
| `mcm-schematic` | 把过程、结构、机理的描述落成可直接粘贴的 TikZ 示意图源码 |

### 家族外

| skill | 用途 |
| :--- | :--- |
| `mcm-playbook` | 赛程中回答"现在该干什么"——处在哪个阶段、该做哪几件事、该调哪个 skill |
| `mcm-topic-select` | 开赛后从六道题里挑一道，并说清为什么是它 |
| `mcm-data` | 数据侧：题面没给的数据怎么找、附件怎么读、统一落成一张数据来源表 |
| `mcm-model-select` | 建模阶段从题面特征选出候选模型，说清为什么用它、什么时候不该用它 |
| `mcm-code` | 代码侧：求解代码怎么写、结果怎么落盘、编号怎么与论文对齐、附录里的代码怎么处置 |
| `mcm-figure-choose` | 决定这组数据该画成哪种图（图型选型） |
| `mcm-section-writer` | 写论文的某一节正文——这一节该回答什么、按什么次序组织 |
| `mcm-abstract` | 写或复核摘要页，在正文与结果完成之后定稿 |
| `mcm-memo` | 题面明确要求 letter 或 memo 时，起草一页备忘录 |
| `mcm-latex-format` | 搭 LaTeX 骨架、排版初稿、格式合规检查 |
| `mcm-ai-disclosure` | 撰写或核查 AI 使用披露（按 COMAP AI policy） |
| `mcm-selfreview` | 提交前对论文稿做最后自查，判断能不能提交 |

除 `mcm-ai-disclosure`、`mcm-latex-format`、`mcm-selfreview` 外，每个 `SKILL.md` 都写明了"什么时候不该用它、该转给谁"。

---

## 环境需求

### 必需

Python 3.11（开发环境为 3.11.9）。工具链与判据脚本用到的第三方包：

| 包 | 版本 | 用途 |
| :--- | :--- | :--- |
| `numpy` | 2.3.5 | 数值 |
| `scipy` | 1.17.1 | 数值 |
| `pandas` | 3.0.5 | 表格数据 |
| `matplotlib` | 3.10.7 | 出图 |
| `SciencePlots` | 2.2.2 | 绘图样式表 |
| `Pillow` | 12.3.0 | 位图 |
| `PyMuPDF` | 1.27.2.3 | PDF 处理 |
| `pywin32` | — | 窗口与进程（Origin 探针） |

### 部分 skill 需要

| 依赖 | 谁需要 | 说明 |
| :--- | :--- | :--- |
| MATLAB | `mcm-plot-matlab`；`mcm-model-select` 的 66 个骨架与参照记录 | 要求本机已装且 `matlab -batch` 可用 |
| TeX Live | `mcm-latex-format`、`mcm-table`、`mcm-schematic` | 开发环境为 TeX Live 2026 |
| Origin | `mcm-plot-origin` 的自动化路径 | `originpro` 包未安装，该路径不可用；改用手工导出 |

随仓库入库的字体：`mcm-plot-python/assets/fonts/` 下有 4 个 OTF（TeX Gyre Termes X 的常规、斜体、粗体、粗斜体），同目录附来源说明与 GFL、LPPL 两份许可原文。

`statsmodels`、`cvxpy`、`pulp` 三个包没有安装，这是有意的：统计推断、凸优化、规划这三类问题的代码骨架改用 MATLAB 写，因此不引入这三个 Python 依赖。

MATLAB 在本机不稳定，开发期间出现过崩溃，其中一次发生在 MATLAB 退出期，崩溃转储会被写进当时正在生成的证据件。跑完任何调用 MATLAB 的命令之后，先看 `git status` 再提交。

---

## 使用方法

### 调用 skill

skill 放在 `.claude/skills/`，在 Claude Code 里使用。触发方式是自然语言：每个 `SKILL.md` 的 frontmatter 写了 `Use when`（什么条件下该用）与 `Triggers include`（一批中英文触发短语）。仓库没有注册 slash 命令，把需求直接说出来即可；也可以显式点名某个 skill。

### 跑判据

判据脚本多数以 `RESULT: PASS` 或 `RESULT: FAIL（…）` 收尾，退出码 0 或 1（个别另有 exit 2，表示 fail-closed 且不打印判词）。三种典型调用：

```bash
# 不带参数
python tests/skills/check-writing-discipline.py
python tests/skills/figure-choose/check-spec-pointers.py

# 带 --scope，区分内检与外检
python .claude/skills/mcm-data/check-data.py --scope self
python .claude/skills/mcm-data/check-data.py --scope artifact <数据来源表.md> --refs <论文.md>

# 带文件与其它参数
python .claude/skills/mcm-section-writer/check-section.py <产出.md> --section 模型建立 --input <题面简报.md>
```

有例外：`check-summary.py`、`check-memo.py`、`check-section.py` 在 FAIL 时末行是 `失败项=…`，`RESULT: FAIL` 在它上一行。按末行判断结果的调用方需要注意这三点。

### 跑变异驱动器

驱动器的作用是证明判据真的会红：它逐条把样例改坏，要求对应判据翻红，再断言合规侧确实绿。

```bash
python tests/skills/data/mutate-data.py
python tests/skills/code/mutate-code.py
```

末行同样是 `RESULT: PASS` 或 `RESULT: FAIL`，上一行是 `RUN: 判据 … · 违规侧红 … · 合规侧绿 … · 控制项 …` 的汇总。

### 全仓检查

没有一键脚本，是一串命令，登记在各模块计划的「收工门」一节，可以直接复制执行。最新且最完整的一份在 `docs/superpowers/plans/2026-10-04-m5-data-code.md` 的 `## Global Constraints` 第 16 条，共 32 条命令。

其中列了两个不在表内的驱动器（`tests/skills/plot-python/mutate-plot-style.py` 与 `tests/skills/plot-matlab/mutate-plot-style.py`），它们是已知缺口。

### 移植到其它 agent

这套 skill 的内容可以移植，触发方式不行。

可以移植，是因为它的 `SKILL.md` frontmatter 只有 `name` 与 `description` 两个字段，没有 `model`、`hooks`、`allowed-tools` 这类跟 harness 绑定的字段，符合跨工具的 `SKILL.md` 约定；正文全是 Markdown 加仓内相对路径。判据与驱动器更是 29 个纯 Python 脚本，与用什么 agent 无关。

不行，是因为 skill 放在 `.claude/skills/`，这是 Claude Code 的目录约定，其它工具不扫这个路径，因此不会自动触发。

三条移植路径，成本从低到高：

**借用标准位置。** 让 `.agents/skills/` 指向 `../.claude/skills`（符号链接或复制）。`.agents/skills/` 是这套 `SKILL.md` 约定在跨工具场景下的位置，认这个约定的工具能自动发现这些 skill。

**写一份 `AGENTS.md` 指路。** 在仓库根放 `AGENTS.md`，把"要做什么、去读哪个 `.claude/skills/<名>/SKILL.md`"列成一张表。`AGENTS.md` 是当前跨工具的事实标准，Codex、Cursor、Gemini CLI、Windsurf、Copilot、Aider、Zed、Warp、Roo、Junie 等都会读它。这样会把自动触发降级为显式指路，但覆盖面最广。

**各 harness 自己的入口文件。** `GEMINI.md` 等，常见做法是里面只写一行 `@AGENTS.md` 或者做成符号链接，让共享内容只有一份。

有两点需要注意：Codex 不读 `.claude/` 目录，所以第一条路对它未必生效，第二条才是对它的正解；`AGENTS.md` 默认有 32 KiB 的加载上限，超出会被静默截断，所以不要抄全文，写成索引即可。

以上三条按各工具公开的约定整理，本仓库没有在 Claude Code 之外的 agent 上实测过。参考来源：[Codex CLI Custom Instructions](https://mintlify.wiki/openai/codex/advanced/custom-instructions)、[AGENTS.md 的跨工具采用](https://docs.crewai.com/v1.15.22/en/guides/coding-tools/agents-md)、[Gemini CLI 配置](https://opensource.adobe.com/mysticat-ai-native-guidelines/04-configuration/ai-tools/gemini-cli/)、[跨 harness 的 skill 兼容性](https://raw.githubusercontent.com/speclabs/devspec/main/devspec/adapters/compatibility-matrix.md)。

---

## 仓库边界

第三方语料绝大部分不上传。远端 `corpus/` 只保留索引、净室件与论文正文抽取这三类派生件，外加来源与许可说明、一份转码表，共 59 个文件。

| 未上传 | 本地体量 | 原因 |
| :--- | ---: | :--- |
| COMAP 获奖论文 201 份（2022–2025 O 奖与 UMAP 期刊） | 1.7 GB | 第三方版权 |
| COMAP 官方赛题与数据附件（2016–2026） | 108 MB | 第三方版权 |
| 获奖论文的整页渲染图 | 164 MB | 派生复制品 |
| 第三方算法源码（`corpus/algorithms/src/`） | 4.7 MB | 上游未声明许可 |

获奖论文的正文抽取（43 份 Markdown）与净室重写版算法（`corpus/algorithms/fixed/` 下的 6 个 `.m`）已经入库。

各语料的来源、许可状态与复现步骤见对应目录下的 `PROVENANCE.md`。本地五堆语料中，`algorithms`、`papers`、`官方原题` 三堆有这份文件，`official` 与 `历届优秀论文` 两堆没有。

---

## 两条全局约定

**语料产物一律字节级写入**，写文件用 `write_bytes`，并配 `.gitattributes` 的 `-text`。

这条约定来自一次事故：`core.autocrlf` 把 883 个文件写成了 `\r\r\n`，当时误判为上游代码有问题。

**判据不得"看起来能失败"就算数。** 每条新增判据都要用一次变异证明它真的会红：把被测对象改坏，跑一次，看它红不红。

这条约定来自反复出现的同类问题：判据在什么都没验的情况下报绿。规矩立下之后仍然复发过，所以现在多数模块都配一个变异驱动器，并要求它的判据总数现取，删掉一条即 FAIL。

---

## 文档索引

| 想找 | 位置 |
| :--- | :--- |
| 套件的设计 | `docs/superpowers/specs/` |
| 各模块的实施过程 | `docs/superpowers/plans/` |
| 还欠什么、哪些是刻意不动的 | `docs/mcm-suite-todo.md` |
| 写作类要求以哪份为准 | `docs/mcm-writing-discipline.md` |
| 踩过的坑 | `docs/mcm-suite-lessons.md` |
