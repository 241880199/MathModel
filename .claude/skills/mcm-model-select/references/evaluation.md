# evaluation —— 类索引（**第二跳**：评价与排序）

**上位**：`SKILL.md` 的第一跳决策树把「**要给若干对象在多指标下排序 / 打分 / 选优**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/evaluation/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面有**多个候选对象**、**多个指标**，要综合成一个**排序 / 得分 / 优劣判断**，且**指标权重需要确定**。
**类级反面（什么时候不该用这一类）**：有**真值的监督数据**要做**预测 / 分类** ⇒ 去 `prediction` / `ml`；
**要在约束下解出最优决策变量** ⇒ `optimization`；**只需描述机理演化** ⇒ `mechanism`。
**边界**：本类只排「谁更好」；**不判"排得对不对"**（那要题目给真值或外部标准）。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：权重从哪来？**
  - **靠专家两两比较、主观定权（含一致性检验）** ⇒ **AHP 层次分析法** → `references/evaluation/ahp.md`
  - **靠数据自身的离散度、客观定权** ⇒ **熵权法** → `references/evaluation/entropy_weight.md`
  - **不显式定权，按"离理想解的距离"排序** ⇒ **TOPSIS** → `references/evaluation/topsis.md`
- **问 2：指标边界是否模糊、等级是否分不清？**
  - **是，且**评价体系**分层** ⇒ **模糊综合评价（多层次）** → `references/evaluation/multi_level_fuzzy.md`
  - **是，且**要同时看**多个目标** ⇒ **模糊综合评价（多目标）** → `references/evaluation/multi_objective_fuzzy.md`
- **常见连用**：**熵权法（客观权重）+ TOPSIS（逼近理想解排序）** = EWM-TOPSIS；AHP 给出主观权重后也可接 TOPSIS。

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| AHP 层次分析法 | `ahp.m` | `references/evaluation/ahp.md` |
| 模糊综合评价（多层次） | `multi_level_fuzzy.m` | `references/evaluation/multi_level_fuzzy.md` |
| 模糊综合评价（多目标） | `multi_objective_fuzzy.m` | `references/evaluation/multi_objective_fuzzy.md` |
| TOPSIS | `topsis.m` | `references/evaluation/topsis.md` |
| 熵权法 | `entropy_weight.m` | `references/evaluation/entropy_weight.md` |

★ **行数 = 5 = 本类花名册项数**（`docs/superpowers/specs/2026-10-04-m4-model-select-roster.md` §2.1）。
★ **本清单不声称穷尽**：它只列花名册终版里本类的 5 个方法。
★ **第二跳与第一跳同构**：本文件也是「入口 → 一问 + 判据 → 叶（一个方法）」的决策树，只是入口换成**类内方法特征**。
★ **每个方法文件的六格形态**（适用判据含反面 · 标准建模步骤 · 参数与假设 · 常见坑 · 输出模板 · 代码骨架）与语料指针口径，
**以各方法文件为准**；本索引**不复述**其具体步骤 / 参数。
