# `green/` —— GREEN 对照件（**用本模块** `mcmplot_origin` 产的图）

> ## !! 本目录同样含泄题风险文件，绝不给写手 !!
>
> `out-G{n}/scenario.py`（它 import `mcmplot_origin`、引着模块口径）与上一层
> `red-green-evidence.md`（对照结论）都**不给写手**。

## 1. 这是什么

Task 3 的 GREEN 侧：与 `red/` **同场景、同数据、同分母、同一把尺**，
只换一个自变量 —— **用不用本模块**（`.claude/skills/mcm-plot-origin/assets/mcmplot_origin.py`）。

- **场景**：逐字用 `figure-choose/red/brief-R{1,2,3}.md`（**权威副本在 `red/`**，
  本目录**不重复内联**，免得造第二份权威）。G1↔R1、G2↔R2、G3↔R3 一一对应。
- **判据**：`check-figure-style.py` 一字未改；`--textwidth-in 6.31`。
- **图注是判断层动作**：**由 Task 2 的 agent 写**（场景 brief 只要求"英文图注"，
  没给合规形态），**不是**场景给的。见 `../red-green-evidence.md` §5。
- **GREEN 不由干净写手产出**：它是"模块能不能把图做合规"的对照侧，由 agent 用模块直接产，
  已过独立复核（`Approved`）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-G{n}/scenario.py` | 用 `mcmplot_origin`（`apply_style`/`figsize_for`/`save`）出图的场景脚本 |
| `out-G{n}/figure.png` · `figure.pdf` | 两载体产物（同源；PNG 300 dpi） |
| `out-G{n}/caption.txt` | 图注（判断层动作，Task 2 写） |

**对照表在上一层**：`../red-green-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. 本支产物在机械判据上的两处**载体事实**（如实记）

1. **`F6` 三态**（落哪一态**依产物而定**，`../red-green-evidence.md` §3.3）：本支 GREEN 的
   `out-G2/figure.pdf` 内嵌了一个 `TimesNewRomanPSMT` 子集 ⇒ `F6` 判 **`PASS`**；
   `out-G1`/`out-G3` 的 PDF **只引用、未内嵌**任何字体 ⇒ `F6` 落 **`N/A`**；三张 PNG 载体
   本判据不适用 ⇒ 也 `N/A`。**不许把 `N/A` 当 `PASS` 或写成硬门。**
2. **PDF 侧 `F5` 判红 = 载体限制**：Origin 的 PDF 内容流把填色量化到**两位小数**
   （实测 `0.9 0.62 0`，而 `#E69F00` 的满精度是 `0.9019607843 0.6235294118`）⇒ 栅格化后每通道
   差 1 LSB ⇒ `F5`（容差 0 的精确命中）判红。**同场景 `F5` 在 PNG 侧是绿的**，且 python/matlab 的
   PDF 走满精度、`F5` 也绿 ⇒ **这不是"Origin 画的图颜色不对"**。登记
   `docs/mcm-suite-todo.md` §H.2 `M3-origin-T2a`。

## 4. 亲眼看图逼出来的 / 眼睛看得见但判据不报的（照实，本任务**不改模块**）

- **段间的黑细边**（内建 `column` 模板 + group 的统一构造路线的产物）：判据 `F2`/`F5` 都不报它
  （覆盖率在阈值之下）—— 只有眼睛看得见。见 `../red-green-evidence.md` §5。
- **坐标轴四边全框、图高 1.41**：`H10`（框线/刻度朝向）与 `H3`（图高）在本支 **not-landable**
  —— 依据是**单源表 `assets/mcm-style.json` 里这两格的 origin 状态**（`h3.height_in` / `h10.axes_box` 均为
  `not-landable`），**不是**「调用方纪律」那一节（那一节三条 = 图例位置 / 次序约束 / 边色）。
  ⇒ **不算缺陷**，但跨载体与 python/matlab 明显不同。
- **图例摆框外（上方）**：这是"调用方纪律"第 1 条（Origin 默认把图例放进绘图区 ⇒ 压数据），
  本支产物已挪出。

## 5. 与 RED 的比对口径

同场景、同数据（逐字）、同分母（`--textwidth-in 6.31`）、同一把尺（判据脚本一字不改）。
**两载体都出**，证据里两个都有；**不许**因为某场景过不了就调判据或换数据。
