# optimization —— 类索引（**第二跳**：优化与决策）

**上位**：`SKILL.md` 的第一跳决策树把「**要在约束下求最优 / 分配 / 调度 / 选址 / 路径规划**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/optimization/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面有**可调决策变量** + **目标函数**（最大化/最小化）+ **约束**（资源、容量、平衡、整数性）。
**类级反面（什么时候不该用这一类）**：没有决策变量、只需**评价** ⇒ `evaluation`；只需**描述演化** ⇒ `mechanism` / `simulation`；目标是**纯预测** ⇒ `prediction`。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：模型是"标准数学规划"还是"黑箱启发式"？**
  - **目标与约束都是线性的** ⇒ **线性规划** → `references/optimization/lp.md`
  - **含整数 / 0-1 变量或指派结构** ⇒ **整数规划 / 指派问题** → `references/optimization/ilp_assignment.md`
  - **目标或约束非线性** ⇒ **非线性规划** → `references/optimization/nlp.md`
  - **多个目标需权衡 / 分层让步** ⇒ **目标规划** → `references/optimization/goal_programming.md`
- **问 2：问题不可微、组合爆炸、或目标为黑箱？**（**启发式 / 元启发式**）
  - **要通用全局搜索（编码 + 选择交叉变异）** ⇒ **遗传算法** → `references/optimization/ga.md`（**变体**：多种群 / 量子 / 混合 → `references/optimization/ga_variants.md`）
  - **要按温度退火的概率接受** ⇒ **模拟退火** → `references/optimization/sa.md`
  - **要群体协作、连续搜索** ⇒ **粒子群 PSO** → `references/optimization/pso.md`
  - **要免疫记忆 / 浓度抑制** ⇒ **免疫优化** → `references/optimization/immune.md`
  - **要信息素正反馈（路径类）** ⇒ **蚁群 ACO** → `references/optimization/aco.md`
  - **要鱼群聚群 / 追尾 / 觅食** ⇒ **人工鱼群** → `references/optimization/afsa.md`
- **启发式参照口径**：随机 / 进化算法要**已知最优解的小算例 + 固定种子 + 多次运行的分布**（不拿"跑通"当"算对"）。

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 线性规划 | `lp.m` | `references/optimization/lp.md` |
| 整数规划 / 指派问题 | `ilp_assignment.m` | `references/optimization/ilp_assignment.md` |
| 非线性规划 | `nlp.m` | `references/optimization/nlp.md` |
| 目标规划 | `goal_programming.m` | `references/optimization/goal_programming.md` |
| 遗传算法 | `ga.m` | `references/optimization/ga.md` |
| 模拟退火 | `sa.m` | `references/optimization/sa.md` |
| 粒子群 PSO | `pso.m` | `references/optimization/pso.md` |
| 免疫优化 | `immune.m` | `references/optimization/immune.md` |
| 蚁群 ACO | `aco.m` | `references/optimization/aco.md` |
| 人工鱼群 | `afsa.m` | `references/optimization/afsa.md` |
| 遗传算法变体（多种群 / 量子 / 混合） | `ga_variants.m` | `references/optimization/ga_variants.md` |

★ **行数 = 11 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
