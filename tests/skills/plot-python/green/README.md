# `green/` —— GREEN 对照件（**用模块** `mcmplot` 产的图）

> ## !! 本目录同样含泄题风险文件，绝不给写手 !!
>
> `out-G{n}/make_figure.py`（它 import `mcmplot`、引着模块口径）与上一层
> `red-green-evidence.md`（对照结论）都**不给写手**。

## 1. 这是什么

Task 5 的 GREEN 侧：与 `red/` **同场景、同数据、同分母、同一把尺**，
只换一个自变量 —— **用不用本模块**（`.claude/skills/mcm-plot-python/assets/mcmplot.py`）。

- **场景**：逐字用 `figure-choose/red/brief-R{1,2,3}.md`（**权威副本在 `red/`**，
  本目录**不重复内联**，免得造第二份权威）。G1↔R1、G2↔R2、G3↔R3 一一对应。
- **判据**：`check-figure-style.py` 一字未改；`--textwidth-in 6.31`。
- **图注是判断层动作**：**由本任务 agent 写**（场景 brief 只要求"英文图注"，
  没给合规形态），**不是**场景给的。见 `red-green-evidence.md` §5。
- **GREEN 不由干净写手产出**：它是"模块能不能把图做合规"的对照侧，由 agent 用模块直接产。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-G{n}/make_figure.py` | 用 `mcmplot` 出图的生成脚本 |
| `out-G{n}/figure.png` · `figure.pdf` | 两载体产物（同源；PNG 200 dpi） |
| `out-G{n}/caption.txt` | 图注（判断层动作） |

**对照表在上一层**：`../red-green-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. 亲眼看图逼出来的两件事（模块层缺口，如实记，本任务**不改模块**）

1. **上/右悬空刻度**：`mcmplot.apply_style()` 叠的 `science` 底座把 `xtick.top` / `ytick.right`
   打开，而 `mcm.mplstyle` 只关了对应**边框线** ⇒ 图上/右会留下**没有脊线的悬空刻度**。
   GREEN 的生成脚本在**轴级** `ax.tick_params(top=False, right=False)` 关掉。
   **这是 G1/G2/G3 生成器里的动作，不是模块的**（改模块要动派生的 `mcm.mplstyle`，
   本任务不做）。
2. **描边把 PNG 的 F2 抬高一档**：给条描白边时，抗锯齿与白底混出的浅色在 **PNG** 栅格上
   占比超过阈值 ⇒ 同一张图 PNG 的 F2 比 PDF 高（G3 初版 PNG=5 / PDF=3）。
   去掉白边后两载体都回落。**证据见 `../red-green-evidence.md` §4 的载体探针。**

## 4. 与 RED 的比对口径

同场景、同数据（逐字）、同分母（`--textwidth-in 6.31`）、同一把尺（判据脚本一字不改）。
**两载体都出**，证据里两个都有；**不许**因为某场景过不了就调判据或换数据。
