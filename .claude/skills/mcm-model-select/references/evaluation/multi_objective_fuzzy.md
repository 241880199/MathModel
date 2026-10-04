# 模糊综合评价（多目标）（`multi_objective_fuzzy.m`）

> **并列多目标下的相对隶属度排序**：没有层级，只有若干**量纲不同、方向不同**的目标；先把每个目标化成"越接近最优越好"的**相对隶属度**（min-max），再加权合成、排序。

**归属**：类索引 `references/evaluation.md` · 骨架 `assets/matlab/evaluation/multi_objective_fuzzy.m` · 参照 `tests/skills/model-select/verify/multi_objective_fuzzy.md`。

## ① 适用判据

- **用**：有**多个并列目标**（不是一个层次体系），各目标**量纲/单位不同**、且**方向不同（效益型 / 成本型）**；要把方案在各目标下的表现统一成**相对隶属度**再合成排序。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **目标其实分层**（准则→子准则）⇒ 用 **多层次** `references/evaluation/multi_level_fuzzy.md`。
  2. **目标是可测数值、且要客观权重** ⇒ 熵权 + TOPSIS（`references/evaluation/entropy_weight.md` · `references/evaluation/topsis.md`）。
  3. **目标间强冲突、要的是 Pareto 前沿而不是单一排序** ⇒ 去 `optimization`（多目标规划）。
  4. **样本极少**：min-max 被**极值绑架**，个别离群点会让相对隶属度全变（凭经验）。

## ② 标准建模步骤

1. 定**方案集**（m 个）与**目标集**（n 个），逐目标标 **benefit / cost**。
2. 建**原始决策矩阵 `X`**（m×n）。
3. 逐列 **min-max** 求**相对隶属度** `R`：
   `benefit: r = (x − min)/(max − min)`；`cost: r = (max − x)/(max − min)`。
4. 定**权重 `w`**（归一）。
5. 合成：`B = R · wᵀ`；`B` 越大越优 ⇒ 排序。
6. 结论：排序 + 各方案相对隶属度。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 原始矩阵 `X`（m×n）· 权重 `w`（1×n）· 各目标类型 `benefit` |
| **输出** | 相对隶属度 `R` · 综合隶属度 `B` · 排序 |

**显式假设（必须写进论文）**：
1. 各目标可**独立评价**、可**加性合成**。
2. min-max 的相对隶属度**线性**刻画"越接近最优越好"。
3. 数据中**无极端离群值**（否则 min-max 失真）。
4. 权重 `Σw = 1`。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **成本型目标忘取反**：用 benefit 公式会**把排序弄反**。本骨架对每个目标读 `benefit(j)` 分支处理（避免此坑）。
2. ★ **常量目标列**（`max == min`）⇒ 分母为 0。**实测**（本骨架）：对该列**相对隶属度置 0 并打印注记**（`multi_objective_fuzzy.m` 的 `const_col`），而不是产生 `NaN`。
3. **min-max 对离群值敏感**：数据更新后相对隶属度**全变** ⇒ 报告里给的"综合隶属度"是**相对量**，**不可跨数据集比较**（凭经验）。
4. **把归一化隶属度当原始分**：`B` 是 0–1 的相对量，**不是**某种"百分制得分"，别误读（凭经验）。
5. **与 TOPSIS 混淆**：两者都做归一化 + 排序，但 TOPSIS 用**离理想解的距离**、本方法用**加权相对隶属度**；换了方法结果不同，**须写明用了哪个**（凭经验）。

## ⑤ 输出模板

- **相对隶属度矩阵 `R`** + **综合隶属度 `B`** + **排序**。
- 排序表 / 隶属度表 → `mcm-table`（`.claude/skills/mcm-table/`）；结果对比图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/evaluation/multi_objective_fuzzy.m`（**零参可跑**，自带 3 方案 × 3 目标全效益型算例）。

关键片段（**不整份复制**）：
```matlab
% 相对隶属度（逐列 min-max；常量列置 0）
if benefit(j); R(:, j) = (X(:, j) - lo) / (hi - lo);
else;          R(:, j) = (hi - X(:, j)) / (hi - lo); end
B = R * w.';                    % 加权综合
[~, rank] = sort(B, 'descend'); % 排序
```
**独立参照**：`tests/skills/model-select/verify/multi_objective_fuzzy.md`（第 3 类：手算标准算例）。

## 语料面（P6）

- **语料指针（带 · 类级）**：`corpus/papers/MODEL_MAP.md` 里 `fuzzy comprehensive evaluation` 命中 **2 篇**（`P2025-D-03` · `P2025-E-03`；当场 `grep -nE "^ +- .*fuzzy comprehensive evaluation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 2 行，各 1 篇）—— **类级指针**（与"多层次"共用；该 tag 不区分两种形态）。
- **算法素材面**：`corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/多目标模糊综合评价/`（含 `main.m` + `muti_objective_fuzzy_analysis.m`）—— 教辅级**起点素材**，**不作独立参照**。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
