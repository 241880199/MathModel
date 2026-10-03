# `green/` —— GREEN 对照件（**用本 skill** 出的示意图）

> ## !! 本目录（连同上一级的证据件）含泄题风险，绝不给写手 !!
>
> **点名**：上一级 `red-green-evidence.md`（对照结论）与 `../red/README.md` / `../red/writer-self-reports.md`
> **都不给写手**。**这个点名不是穷举**：`out-G1/` 下的 `figure.tex` / `caption.txt` / `figure.png`
> 与本 `README.md` 自身**同样不给写手**。

## 1. 这是什么

Task 3 的 GREEN 侧：与 `red/` **同场景、同一把尺**，只换一个自变量 —— **用不用本 skill**
（`.claude/skills/mcm-schematic/` 的 `SKILL.md` / `references/workflow.md` / `references/schematic-style.md`
＋ `assets/schematic-style.tex` ＋ `assets/skeletons/`）。

- **场景**：`tests/skills/schematic/red/brief.md`（**权威副本在 `red/`**，本目录**不重复内联**）。
  RED 与 GREEN **同场景同内容**（唯一场景，见 `../red/README.md` §3）。
- **判据**：`tests/skills/figure-choose/check-figure-style.py`，**一字未改**（工作树 blob == `HEAD` blob，
  见 `../red-green-evidence.md` §0）；两侧都带 `--schematic`、同一分母 `--textwidth-in 6.75`。
- **GREEN 不由干净写手产出**：由本任务**用本 skill 的工作流**产出（分类 → 挑骨架 → 改 → 编译 → 渲图看一眼 → 交付），
  过全部判据。**没有** `green/writer-self-reports.md` —— 这一侧不是隔离写手的产物（对比 `red/` 有那份）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-G1/figure.tex` | 本 skill 产出的 TikZ 源码（完整可编译文档，`\input{../schematic-style.tex}`；泄题风险件） |
| `out-G1/caption.txt` | 英文图注（泄题风险件） |
| `out-G1/figure.pdf` | 编译产物（**非字节可复现**：每次重编带新 `CreationDate`/`ID`） |
| `out-G1/figure.png` | 渲图（150 dpi）；**非字节可复现**，只作「看一眼」的证据 |
| `README.md` | 本文件（泄题风险件） |

**上表不声称穷尽**：本目录内任何文件派写手时都不给。

**对照表在上一层**：`../red-green-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. 本支产物在机械判据上的读数

- **G1 十三条全绿**（`F1`–`F6` ＋ `--schematic` 的 `A1`/`A3`/`A4`）—— 逐字读数见 `../red-green-evidence.md` §3。
- **选型回显**：类别 = **技术路线图**（有先后 / 分支 / 汇合）；骨架 = `assets/skeletons/pipeline-branch.tex`
  **改造**（两路改成三路投影、加一条虚线修订回环）。样式一律走 `../schematic-style.tex`，
  `figure.tex` 自己**不含**颜色 / 线宽 / 圆角 / 字号字面量。

## 4. 亲眼看图逼出来的（照实）

见 `../red-green-evidence.md` §6 的看图记录。**本任务不改判据**。

## 5. 与 RED 的比对口径

同场景、同判据、同一组参数（`--schematic` ＋ `--textwidth-in 6.75`）。
**不许**因为某场景过不了就调判据或换数据。逐条对照与并排 diff 见 `../red-green-evidence.md`。
