# mechanism —— 类索引（**第二跳**：机理建模）

**上位**：`SKILL.md` 的第一跳决策树把「**要有机理的动力学 / 随时间演化 / 微分方程**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/mechanism/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面能写出**状态随时间（或时空）演化的方程**（微分 / 差分方程），要**求演化轨迹、平衡点、稳定性或参数**。
**类级反面（什么时候不该用这一类）**：**没有机理、只有数据** ⇒ `prediction` / `ml`；**只有个体规则、无方程** ⇒ `simulation`；**要解约束最优** ⇒ `optimization`。
★ **语料面与算法素材面必须分开说**（`"素材 0" ≠ "语料 0"`）：见各方法文件里的两面分派。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：自变量是连续时间还是离散时间步？**
  - **连续时间、给初值** ⇒ **ODE 初值问题（Euler / RK4）** → `references/mechanism/ode_ivp.md`
  - **连续时间、给两端边界条件** ⇒ **ODE 边值问题（打靶法）** → `references/mechanism/ode_bvp_shooting.md`
  - **高阶可降为一阶组 / 有解析解** ⇒ **降阶 / 解析解法** → `references/mechanism/reduce_order.md`
  - **离散时间步（x_{k+1}=f(x_k)）** ⇒ **差分方程（离散动力系统 · 稳定性判据）** → `references/mechanism/difference_equations.md`
- **问 2：是否含空间维度（偏微分方程）？**
  - **抛物 / 椭圆 / 双曲型数值解（含刚性）** ⇒ **PDE 数值解** → `references/mechanism/pde_numerical.md`
  - **热传导 / 扩散 / 波动（输运）** ⇒ **输运方程** → `references/mechanism/transport.md`
  - **反应 + 扩散耦合** ⇒ **反应扩散** → `references/mechanism/reaction_diffusion.md`
- **问 3：是否已定"模型形态"（现成的动力学模型）？**
  - **传染病传播（仓室模型）** ⇒ **传染病模型（SIR / SEIR）** → `references/mechanism/sir_seir.md`
  - **种群 / 生态竞争捕食** ⇒ **生态动力学（Lotka-Volterra）** → `references/mechanism/lotka_volterra.md`
- **问 4：方程已知但参数未知、或要看长期稳定性？**
  - **是** ⇒ **参数辨识 / 稳定性分析** → `references/mechanism/param_id_stability.md`

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| ODE 初值问题（Euler / RK4） | `ode_ivp.m` | `references/mechanism/ode_ivp.md` |
| ODE 边值问题（打靶法） | `ode_bvp_shooting.m` | `references/mechanism/ode_bvp_shooting.md` |
| 降阶 / 解析解法 | `reduce_order.m` | `references/mechanism/reduce_order.md` |
| 差分方程（离散动力系统 · 稳定性判据） | `difference_equations.m` | `references/mechanism/difference_equations.md` |
| PDE 数值解（抛物/椭圆/双曲） | `pde_numerical.m` | `references/mechanism/pde_numerical.md` |
| 传染病模型（SIR / SEIR） | `sir_seir.m` | `references/mechanism/sir_seir.md` |
| 生态动力学（Lotka-Volterra） | `lotka_volterra.m` | `references/mechanism/lotka_volterra.md` |
| 输运方程（热传导 / 扩散 / 波动） | `transport.m` | `references/mechanism/transport.md` |
| 反应扩散 | `reaction_diffusion.m` | `references/mechanism/reaction_diffusion.md` |
| 参数辨识 / 稳定性分析 | `param_id_stability.m` | `references/mechanism/param_id_stability.md` |

★ **行数 = 10 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **与 `statistics` / `optimization` 的边界**：**参数辨识 / 稳定性分析** 保留在本类，但其方法文件要写明它与统计（估计）与优化（拟合）的边界。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
