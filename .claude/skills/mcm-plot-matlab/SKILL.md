---
name: mcm-plot-matlab
description: Use when 美赛 MCM/ICM 论文要用 MATLAB 出图、把图型决策落成 MATLAB 代码，或已画出的图被出货检查器打回（图宽比不合、底色是深色、字体族不对）需要按规范重画时。Triggers include MATLAB 画图、matlab 出图、MATLAB 代码出图、按规范画图、figure 出图、print 导出、底色太深、图宽不对、字体不对、plot the figure in MATLAB。
---

# mcm-plot-matlab —— 把图型决策落成 MATLAB 代码

**只回答一件事**：图型定了、数据在手，**怎么用 MATLAB 把它画成规范里的那张图** —— 怎么建 figure、
主题怎么上、图幅怎么定、色序怎么套、坐标轴怎么收拾、怎么导出、画完怎么验。

**不回答**：**该画成哪种图**（那是 `mcm-figure-choose` 的活）；**规范里每条规则的数值**
（规范在 `references/house-style.md`，本 skill **只给指针、不重述**）。
**不产** Python / Origin / TikZ 代码，也不出"这张图合规吗"的判词（判词在出货检查器的出口）。

## 什么时候用

- 图型已经定了（自己定的，或 `mcm-figure-choose` 给的），要把数据落成 MATLAB 代码；
- 已经画出来了，但出货检查器的几条（图宽比 / 底色 / 字体族）判红，要按规范重画；
- 要把一篇论文里的图统一到同一套外观（底色、线宽、色序、框线与刻度那些细节）。

**不用**：

- 只问"这组数据该画哪种图" ⇒ 走 `mcm-figure-choose`；
- 只问某条规范的具体数值或口径 ⇒ 直接读 `references/house-style.md` 与它旁边的 `provenance.md`
  （本 skill 不重述数值）。

## 怎么用

**前置条件（照实）**：本 skill 要跑 MATLAB —— **需要本机已装 MATLAB**，且 `matlab -batch` 可用。
**本 skill 不自动安装它**，也不代管许可证。字体走**系统 `Times New Roman`**（点名即内嵌；
**不装任何字体**、**不复制入库字体**）。**跨版本 / 跨机未验**：本封装只在本机的一版 MATLAB 上验过，
换版本或换机器请自行重跑一遍产物级判据。

入口（薄封装，实现在 `assets/mcmplot.m`；本文件只讲怎么用）：

- `M = mcmplot()`：拿到封装句柄；样式值放在 `M.style`（派生件，勿手改）。
- `fig = M.figure(tw_in)`：建一张**浅色主题**的 figure，并把图幅钉进 `PaperPosition` / `PaperSize`。
  `tw_in` = **正文栏宽分母**（英寸），由**调用方**传入 —— 它是论文的属性，本 skill 与检查器都不预设默认值。
- `M.apply(fig)`：给 `fig` 及其下每个 axes 上 house style（白底 / 色序 / 字体 / 框线刻度）。
  **建图后、导出前**调它。
- `M.size(tw_in)`：给出**该用哪个图幅**（宽 × 高，英寸）—— 宽取自表里图宽比那条规则的默认档，**是个确定值**。
- `M.fontsize(body_pt)`：给出图内字号的**允许带**（下限 ~ 上限）—— 落在带里哪个绝对值由调用方按论文正文定。
- `M.save(fig, path, [dpi])`：导出。走 `print` 家族（`.png` 跟 `PaperPosition`、`.pdf` 跟 `PaperSize`）。
  `dpi` 只对 PNG 有意义，且必须与送进检查器时的 `--dpi` **一致**。
- `M.style.line_width`：线宽是**逐对象**属性，本封装只把值放在这里，**不替你套到每条线上**。

完整流程（读规范 → 套样式 → 出图 → 机械层验 → **亲眼看图**）见 `references/workflow.md`。

## 输出契约

- **一份可复跑的 `.m` 脚本**：调上面那几个入口，不手抄样式数值；用 `mfilename('fullpath')` 反推仓根，
  别用相对路径（`run()` 会把 cwd 切到脚本所在目录）。
- **产物图**：PNG 与 PDF 两种载体都出（`save` 只认这两种，别的不认）。
- **图注文本**：按规范写（图注形态由检查器那几条守）。
- **机械层读数**：产物送进出货检查器后的原始输出，判词逐条贴。
- **亲眼看图的一句话**：从这张图上读到了什么 —— 见 `references/workflow.md` 那一节。

## 边界

- **不重述任何规范数值**：阈值 / 占比 / 样本读数回 `references/house-style.md` 去说。
  本文件**一个阿拉伯数字都没有**；`references/workflow.md` 里出现的数字**只有规则编号**
  （`H<n>` 这类指针型 ID，**不是数值**）。要说的数回规范去说。
- **不手改派生件**：`assets/mcmplot.m` 的 `BEGIN/END GENERATED` 之间是**派生件**
  （由入库的生成器从 `mcm-style.json` 重放产出）。要改样式值，请改那张表（或其上游规范），再重放。
- **不判"图讲没讲清"**：机械层判不了这一层，它是判断层的事；这一层的入口写在
  `references/workflow.md` 的固定一节里。
- **不产别的载体**：Python / Origin / TikZ 是同层其余 skill 的事。
- **不自动装依赖**：见「怎么用」的前置条件。

## 指针

- **规范正文**（图通常长什么样、每条规则的数值与验证状态）：`references/house-style.md`
  —— 本 skill 对样式的主张以它为准，本文件不复述其中任何一个数。
- **口径与复跑命令**（每个数的分母、样本范围、已知偏差）：`provenance.md`
- **图型决策**（该画哪种图）：`mcm-figure-choose` 那个 skill
- **出货检查器**（机械层判词）：`tests/skills/figure-choose/check-figure-style.py`
- **本 skill 的流程正文**：`references/workflow.md`
