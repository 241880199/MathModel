# `red/` —— RED 基线（`mcm-schematic` · **无规范**场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（三份并列）**：本 `README.md` / `writer-self-reports.md` / 上一级的 `red-green-evidence.md`。
> 它们写明了**判据**（`F1`–`F6` ＋ `A1`/`A3`/`A4`）与**对照结论**；`writer-self-reports.md` 还写明**派发口径**。
> 任何「写手」agent 读过其中**任何一份**，产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：`out-R{n}/figure.tex` 与 `caption.txt`（别的写手的产物）、
> `out-R{n}/figure.pdf` 与 `figure.png`（渲染/判据证据件）、以及上一级 `neutral-skeleton.tex`
> **也都不给写手**。派写手时提示词只给**场景 brief 的路径** ＋ **中性骨架的路径** ＋ **产物输出目录**
> （外加一件环境事实，见 §4）。

## 1. 这是什么

Task 3 的 RED 侧：**同一份场景、同一把尺**下，**没见过规范**的三位写手产出的**示意图**。
与上一级 `green/` 对照：GREEN 侧是**用本 skill** 产出的同场景图。

- **场景（权威副本）**：`tests/skills/schematic/red/brief.md` —— **唯一一份**，RED 与 GREEN 逐字共用。
- **中性骨架**：`tests/skills/schematic/neutral-skeleton.tex`（§3 讲它为什么长这样；它**自己也入库、也能编译**）。
- **判据**：`tests/skills/figure-choose/check-figure-style.py`，**一字未改**（工作树 blob == `HEAD` blob，
  见 `../red-green-evidence.md` §0）。
- **★ RED 是本任务的「自变量」**：`out-R{n}/figure.tex` 与 `caption.txt` **本轮未改**
  （逐个 blob 与 `HEAD` 比对见 `../red-green-evidence.md` §0）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `brief.md` | **场景正文**（唯一一份；RED 与 GREEN 共用；**这本身不是泄题件** —— 写手要看它） |
| `out-R{n}/figure.tex` | 写手产出的 TikZ 源码（**自包含**、可编译；泄题风险件） |
| `out-R{n}/caption.txt` | 写手产出的图注文本（英文；泄题风险件） |
| `out-R{n}/figure.pdf` | 写手**自己编译**的产物（**非字节可复现**） |
| `out-R{n}/figure.png` | 渲图（150 dpi）；**非字节可复现**，只作「看一眼」的证据 |
| `writer-self-reports.md` | 三个写手的**派发口径与自述**（⚠️ 泄题风险件） |
| `README.md` | 本文件（⚠️ 泄题风险件） |

**对照表与判断层在上一级**：`../red-green-evidence.md`
（RED × GREEN 并列红绿表 · 逐判据判词 · RED 每条红的性质 · 两侧 `.tex` 并排 diff · 亲眼看图）。
**生成器**：`../make-evidence.py`（机器抽取；`write_bytes`、全 LF；判据清单**现取**、不写死）。

## 3. ★ 中性骨架 `neutral-skeleton.tex` —— 为什么长这样（硬要求 1 / P6）

**陷阱（照实说）**：写这份骨架的人**天然会想把它写得好看**；而**「好看」本身就是样式决策**。
它在这里的作用是给写手一个**能用的工具**，**不是**给一个「我们家的样式」的起跑线。
故写完**逐行回读**，对每一行问一句：**「这一行决定了规范也决定的某件事吗？」** 是 ⇒ 删。

**逐行判定（本文下方 §3.1 的清单不声称穷尽，只逐条过一遍当天的每一行）**：

| 行 | 决定了什么 | 规范也决定它吗 | 判定 |
| :--- | :--- | :--- | :--- |
| `\documentclass{article}` | 一个默认页盒 | 规范**钉**页盒宽（`\mcmscfigwidth`）；`article` 默认**不钉** | **留** —— 它没有做出规范的那个决定 |
| `\usepackage{tikz}` ＋ `\usetikzlibrary{positioning}` | 能画 TikZ（**工具**） | 规范用的库是另一套（`arrows.meta,calc,fit,...`，见样式层顶部） | **留** —— 库是工具，不是样式值 |
| `\node[draw] (a) {A};` | 一个**有边框的节点** | 规范决定节点边框的**颜色 / 线宽 / 圆角 / 填充**；`[draw]` 全用 **TikZ 默认** | **留** —— 它只做出「有框」这个**语义**决定，没做出规范的**样式值** |
| `\node[draw, right=of a] (b) {B};` | 用 `positioning` 默认间距摆第二个节点 | 规范有**自己的**间距（`\mcmscgap` 等） | **留** —— 用的是库默认，不是规范的间距纪律 |
| `\draw[->] (a) -- (b);` | 一条**有向箭头** | 规范有**自己的**箭头（`Stealth` 尖、线宽、颜色） | **留** —— 用的是 TikZ 默认箭头，不是样式层的箭头 |
| **没有**：颜色调色板 / 线宽值 / 圆角值 / 间距纪律 / `newtxtext` / 页宽或图宽钉子 / 图注约定 | —— | 规范**全都**决定这些 | **都不写** —— 正是要留给写手自己去（不知道而）决定 |

**验证它真的「能用」**：`neutral-skeleton.tex` **自己编得过**（`pdflatex rc=0`，§3.1 有当场读数）；
它**能放节点与箭头**（上面三行）。★ 但它在判据上的读数**本来就带红**（默认页盒 ⇒ `F1` 红、
默认 CM 字体 ⇒ `F6` 红、默认线宽 ⇒ `A4` 红）—— 这不是缺陷，是「**零美赛样式决策**」的必然结果，
也正是 RED 要暴露的东西。

### 3.1 `neutral-skeleton.tex` 自己的编译读数（当场跑过）

```text
$ pdflatex -interaction=nonstopmode -halt-on-error neutral-skeleton.tex
rc=0 · Overfull \hbox=0 · Output written on neutral-skeleton.pdf (1 page, 10736 bytes)
```

它随附的判据读数（`--schematic`，信息行）—— ★ **本块是手写摘录，不是机器生成**（无生成器、无不动点保证）；读数本身与当日 `neutral-skeleton.pdf` 相符，但**以当场命令的输出为准**（复跑命令即本块首行；`<...>` 处填骨架 PDF 的实际路径）：

```text
$ python tests/skills/figure-choose/check-figure-style.py --fig <...>/neutral-skeleton.pdf \
    --caption "Figure 1: a minimal test" --textwidth-in 6.75 --schematic
FAIL  F1  图宽比 1.259（分母 6.75 in）
FAIL  F6  内嵌字体 ['CMR10']
FAIL  A4  越界线宽 2 种：[0.319, 0.399]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
RESULT: FAIL（F1,F6,A4）   # 其余 F2/F3a-d/F4/F5/A1/A3 全 PASS
```

## 4. RED 之所以是 RED

- 三个写手都是**新起的干净上下文 agent**（`general-purpose`，**未用 `fork`**）。首条 user 消息 = 一条提示词本身，
  只含**三样 + 一件环境事实**：场景 brief 的路径 · 中性骨架的路径 · 产物输出目录 · `pdflatex` 在 PATH
  （可选自编验证）。末尾一句**隔离句**（"Work only from those two files - do not read or write any other file."）。
  **未给**：本 skill / `schematic-style.md` / 判据 / 侦察读数 / 本任务书。
- **强度边界（照实）**：写手「只读了那两个文件」这件事**只有自报、没有沙箱可证**；本支那份
  `writer-self-reports.md` 的提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**，
  **不是**从 transcript 文件里机器摘的 ⇒ **只有转录级忠实度声明**，没有逐字节保证。
- **★ 环境旁路的如实披露（删不掉的，不许省）**：写手是本机 Claude Code 的 agent，
  **会话级共享上下文里另有两处可见面** —— ① 可用 skill 列表里 `mcm-schematic` 那一行的**类别名**
  （"图宽不合、底色不是白、显著色不在允许色序、图注不合规、字体族不对"）；② 项目记忆 `MEMORY.md`
  （模块名 + 工具面）。★ 它们泄的是**「有这几类要求」**，**不是「判据的边界在哪」** —— 阈值、线宽集合、
  `newtxtext`、`\mcmscfigwidth` 的算法、`A` 族判据 ID 与口径，写手**都看不到**。
  全文见 `writer-self-reports.md` 文首。
- **★ 一处设计选择（如实记）**：本支是**同一场景 × 3 位隔离写手**（看**写手间的离散度**），
  **不是**另三支载体的 **3 场景 × 1 位**。依据 = Task 3 任务书与设计 §5.3 原文
  （「三个隔离写手各拿**同一份**场景描述 + 一份中性最小骨架」）。代价照实说：场景只有一份，
  **判据覆盖的形态因此比「3 场景」窄**。

## 5. 与 GREEN 的比对口径

同场景（`brief.md`，逐字）、同一把尺（`check-figure-style.py` 一字不改、两侧同一组参数
`--schematic` ＋ `--textwidth-in 6.75`）。**两侧都出编译渲染的 PNG**，证据里都登记；
**不许**因为 GREEN 改善就调判据或换数据。
**★ 不许把 RED 的红读成「图烂」** —— 三份 RED **都编得过、拓扑都对、图都读得清**；
判据红的是**没被告知的约定**（图宽怎么钉 · 图注怎么写 · 字体跟谁同源 · 线宽取哪一档）。
详见 `../red-green-evidence.md` §5。
