# 灰色关联 / 优势分析（`grey_relational.m`）

> **小样本、信息灰（一列参考序列 + 若干比较因素）时，排"哪个因素影响大"**：用关联系数衡量各比较序列与参考序列的**几何形状接近程度**，得到关联度并排序。

**归属**：类索引 `references/statistics.md` · 骨架 `assets/matlab/statistics/grey_relational.m` · 参照 `tests/skills/model-select/verify/grey_relational.md`。
★ **与相邻方法的边界**：要**预测未来值**（灰预测 GM(1,1)）⇒ `references/prediction/gm11.md`；要**按样本 / 变量分组**⇒ `references/statistics/hierarchical_cluster.md` / `var_cluster.md`；要**回归系数**（可解释的边际效应）⇒ `references/prediction/regression.md`。

## ① 适用判据

- **用**：**样本少（灰信息）**、要**排因素影响力 / 优势**；因素与参考序列的量纲可能不同；想要**无量纲、形状导向**的接近度；做**优势分析**（哪个因素对目标更敏感）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **要估计系数 / 边际效应** ⇒ 走 `regression`（关联度是"接近度排序"，不是系数）。
  2. **要预测未来值** ⇒ 走 `gm11`（灰关联不预测）。
  3. **样本量充足、可做统计推断** ⇒ 走 `hypothesis_test` / `regression`（灰关联是**小样本**的补救工具）。
  4. **分辨系数 `ρ` / 归一化方式不写明** ⇒ 关联度不可复现（本骨架 `ρ = 0.5` 显式）。
  5. **序列间是强非线性关系** ⇒ 几何接近度未必反映真实影响（凭经验）。

## ② 标准建模步骤

1. **定参考序列 `x0`**（目标 / 母序列）与**比较序列 `xi`**（各因素）。
2. **归一化**（★ 量纲不同时）：初值化（除以首值）/ 均值化 / min-max —— **写清用哪种**（本算例用**原始差**以保持手算可核）。
3. **算差序列** `Δ_i(k) = |x0(k) − xi(k)|`，取 `min`、`max`。
4. **定分辨系数 `ρ`**（惯例 `0.5`）。
5. **算关联系数** `ξ_i(k) = (min + ρ·max) / (Δ_i(k) + ρ·max)`。
6. **算关联度** `r_i = mean_k ξ_i(k)`（沿样本取均值），**降序排序**。
7. **数值验证**（★ 见 ⑥）：对小规模算例**手算**逐位核对。
8. **报告**：关联系数矩阵 + 关联度表 + 排序。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 参考序列 `x0`（1×n）· 比较序列矩阵 `X`（m×n）· **分辨系数 `ρ`** · 归一化方式 |
| **输出** | 差序列 `Δ` · 关联系数 `ξ`（m×n）· 关联度 `r`（m×1）· 排序 |

**显式假设（必须写进论文）**：
1. **几何接近 = 影响大**：两序列形状越接近，关联度越高（这是灰关联的核心假设，可被质疑）。
2. **分辨系数 `ρ`**：惯例 `0.5`；`ρ` 越小越放大差异 —— ★ **必须写明取值**（本骨架默认 `0.5`）。
3. **归一化方式**：影响结果，须写明（本算例用原始差）。
4. **样本数 `n`**：小样本工具，`n` 太小则关联度不稳。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **`ρ` 与归一化方式不写明** ⇒ 关联度不可复现（本骨架把 `ρ = 0.5` 与"原始差"都显式）。
2. ★ **拿"跑通"当"算对"**：必出关联度，对不对要手算核。**实测**（本骨架，3 因素 × 4 样本）：`r = [0.475000 0.916667 0.533333]` 与**手算逐位相同**；见 `verify/grey_relational.md`。
3. **不归一化就跨量纲比较**：量纲大的因素主导差序列（凭经验；本算例用同量纲原始差，实战常需先归一化）。
4. **把关联度当"系数"**：关联度只给**排序**，**不是**回归系数、不能说"每增 1 单位目标增 `r`"（凭经验）。
5. **参考序列选错**：参考序列应是**目标 / 母序列**，不是随便一列（凭经验）。

## ⑤ 输出模板

- **关联系数矩阵**（因素 × 样本）+ **关联度表**（因素 · 关联度 · **排序**）+ 可选**关联度条形图**（降序）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；排序条形图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/statistics/grey_relational.m`（**零参可跑**，自带手算算例：`x0 = [1 2 3 4]`、3 因素 × 4 样本、`ρ = 0.5`）。

关键片段（**不整份复制**）：
```matlab
Delta = abs(X - x0);                       % 差序列 m x n
minv = min(Delta(:));  maxv = max(Delta(:));
xi = (minv + rho*maxv) ./ (Delta + rho*maxv);   % 关联系数（rho = 0.5）
r  = mean(xi, 2);                          % 关联度
[rs, order] = sort(r, 'descend');          % 因素影响力排序
```
★ **撞名提醒**：本名字**无**顶层 `@grey_relational` 类目录撞名（灰关联无 MATLAB 内置）。
**独立参照**：`tests/skills/model-select/verify/grey_relational.md`（**第 3 类：手算算例** —— `r = [0.475000 0.916667 0.533333]`、排序 `[2 3 1]` 与手算逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GreySystem灰色系统/association_analysis.m` · `corpus/algorithms/src/GreySystem灰色系统/strength_analysis.m` —— 教辅级**起点素材**，**不作独立参照**（未经净室重写）。

## 语料面（P6）

- **带语料指针（薄）**：`corpus/papers/MODEL_MAP.md` 里 `grey relational analysis` 带锚 **1 行 / 1 篇**（`:169` `P2025-C-15`）
  （当场 `grep -nE "^ +- .*grey relational analysis（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` —— **必须用整串**：裸 / 截断模式 `grey relational` 带锚 ⇒ **0 行**、`grey correlation` / 裸 `grey` 亦 0）。
  ★ **正对照**：同形态 `genetic algorithm` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面（有）**：`corpus/algorithms/src/GreySystem灰色系统/association_analysis.m` · `corpus/algorithms/src/GreySystem灰色系统/strength_analysis.m`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**："灰关联还有哪些写法"不声称覆盖（`grey correlation` 带锚 0 行；邻近 `grey prediction` 1 篇是**灰预测**、不并入）。
