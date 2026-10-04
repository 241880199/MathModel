# simulation —— 类索引（**第二跳**：仿真与随机）

**上位**：`SKILL.md` 的第一跳决策树把「**要模拟随机过程 / 离散事件 / 个体互动的演化**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/simulation/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面**写不出闭式解**，只能**按规则 / 分布推演**出结果（随机抽样、事件排队、个体互动、网格演化）。
**类级反面（什么时候不该用这一类）**：**有解析解或可数值解方程** ⇒ `mechanism`；**只需评价 / 优化** ⇒ `evaluation` / `optimization`；**只要预测序列** ⇒ `prediction`。
★ **本类里 `queueing` / `abm` 属低使用度**（见 `SKILL.md` 的口径与不做表）—— 照补是为**覆盖面**，**不许写成"常用"**。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：演化发生在固定网格上、规则是局部确定的吗？**
  - **是（元胞自动机）** ⇒ **元胞自动机（9 种规则）** → `references/simulation/cellular_automata.md`
- **问 2：核心是"对随机量做大量抽样 / 估计积分"？**
  - **是** ⇒ **蒙特卡洛** → `references/simulation/monte_carlo.md`
- **问 3：有"随机到达 + 排队 + 服务"的结构吗？**
  - **是（M/M/1、M/M/c 等）** ⇒ **排队论** → `references/simulation/queueing.md`
- **问 4：由大量异构个体按各自规则互动、涌现宏观行为？**
  - **是（agent-based）** ⇒ **ABM（多智能体）** → `references/simulation/abm.md`

★ **参照口径**：`cellular_automata` / `abm` 属**三类参照套不上**的情形 → **人工兜底**（已知规则标准图案 / 2–3 agent 手算小例）；
`monte_carlo` → 合成分布 + 收敛率；`queueing` → **有闭式 ⇒ 可用第 1 类**（M/M/1 的 L/W/ρ）。**不许写成"已验证"**。

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 元胞自动机（9 种规则） | `cellular_automata.m` | `references/simulation/cellular_automata.md` |
| 蒙特卡洛 | `monte_carlo.m` | `references/simulation/monte_carlo.md` |
| 排队论 | `queueing.m` | `references/simulation/queueing.md` |
| ABM（多智能体） | `abm.m` | `references/simulation/abm.md` |

★ **行数 = 4 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
