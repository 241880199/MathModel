---
name: mcm-plot-python
description: Use when 美赛 MCM/ICM 论文要用 Python 出图、把图型决策落成 matplotlib 代码，或已画出的图被出货检查器打回（图宽比不合、彩色主色太多、图注不合规）需要按规范重画时。Triggers include 画图、出图、matplotlib、Python 出图、按规范画图、图宽不对、图注不合规、配色太多、套用期刊样式、scienceplots、plot the figure。
---

# mcm-plot-python —— 把图型决策落成 python 代码

**只回答一件事**：图型定了、数据在手，**怎么用 Python 把它画成规范里的那张图** —— 套哪套样式、
图幅怎么定、字号怎么取、图注怎么写、画完怎么验。

**不回答**：**该画成哪种图**（那是 `mcm-figure-choose` 的活）；**规范里每条规则的数值**
（规范在 `references/house-style.md`，本 skill **只给指针、不重述**）。
**不产** MATLAB / Origin / TikZ 代码，也不出"这张图合规吗"的判词（判词在出货检查器的出口）。

## 什么时候用

- 图型已经定了（自己定的，或 `mcm-figure-choose` 给的），要把数据落成 matplotlib 代码；
- 已经画出来了，但出货检查器的几条（图宽比 / 彩色主色数 / 图注形态）判红，要按规范重画；
- 要统一一篇论文里所有图的外观（字体、线宽、刻度那些细节）。

**不用**：

- 只问"这组数据该画哪种图" ⇒ 走 `mcm-figure-choose`；
- 只问某条规范的具体数值或口径 ⇒ 直接读 `references/house-style.md` 与它旁边的 `provenance.md`
  （本 skill 不重述数值）。

## 怎么用

**前置条件（照实）**：本 skill 依赖 **SciencePlots** 这个第三方样式包（底座 = `science` 与 `no-latex`
两套样式叠加）。**本 skill 不自动安装它** —— 运行前请自行确保它已能在当前 Python 环境里导入
（`import scienceplots` 不报错）。字体**随本 skill 入库**，由 `apply_style()` 注册，
**不依赖 TeX Live 的字体路径**。

入口（薄封装，实现在 `assets/mcmplot.py`；本文件只讲怎么用）：

- `apply_style()`：注册入库字体 + 叠底座 + 叠本 skill 的 rcParams。**先调它，再建图**。
- `figsize_for(textwidth_in)`：把**正文栏宽分母**换算成 `figsize`。分母由**调用方**传入 ——
  它是论文的属性，本 skill 与检查器都**不预设**默认值。
- `fontsize_for(body_pt)`：给出图内字号的允许区间；`body_pt` 同样由调用方传（正文 pt 是论文的属性）。
- `save(fig, path, dpi)`：保存。`dpi` 由调用方传，且必须与送进检查器时的 `--dpi` **一致**。

完整流程（读规范 → 套样式 → 出图 → 机械层验 → **亲眼看图**）见 `references/workflow.md`。

## 输出契约（每次都交齐这几样）

- **一份可复跑的 python 脚本**：调上面那几个入口，不手抄任何样式数值。
- **产物图**：PNG 与 PDF 两种载体都出（两条载体上检查器的读数**不保证相同**）。
- **图注文本**：按规范写（图注形态由检查器那几条守）。
- **机械层读数**：产物送进出货检查器后的原始输出，判词逐条贴。
- **亲眼看图的一句话**：从这张图上读到了什么 —— 见 `references/workflow.md` 那一节。

## 边界

- **不重述任何规范数值**：阈值 / 占比 / 样本读数一律在 `references/house-style.md`。
  本文件与 `references/workflow.md` 都**不复述规范数值**（含用中文数词写的规范值），也都**一个阿拉伯数字都没有**。要说的数回规范去说。
- **不手改派生件**：`assets/mcm.mplstyle` 与 `assets/mcmplot.py` 的常量区都是**派生件**
  （由入库的生成器从规范重放产出）。要改，请改规范里那条，再重放。
- **不判"图讲没讲清"**：机械层判不了这一层，它是判断层的事；这一层的入口写在
  `references/workflow.md` 的固定一节里。
- **不产别的载体**：MATLAB / Origin / TikZ 是同层其余 skill 的事。
- **不自动装依赖**：见「怎么用」的前置条件。

## 指针（唯一权威）

- **规范正文**（图通常长什么样、每条规则的数值与验证状态）：`references/house-style.md`
- **口径与复跑命令**（每个数的分母、样本范围、已知偏差）：`references/provenance.md`
- **图型决策**（该画哪种图）：`mcm-figure-choose` 那个 skill
- **出货检查器**（机械层判词）：`tests/skills/figure-choose/check-figure-style.py`
- **本 skill 的流程正文**：`references/workflow.md`
