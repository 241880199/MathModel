# PDE 数值解（抛物/椭圆/双曲）（`pde_numerical.m`）

> **给"含空间维度"的机理题用**：状态既随时间又随空间变化（`u_t = D u_xx + ...`），要把**整场** `u(x,t)` 求出来 ⇒ 有限差分 / 线方法 / 有限元。

**归属**：类索引 `references/mechanism.md` · 骨架 `assets/matlab/mechanism/pde_numerical.m` · 参照 `tests/skills/model-select/verify/pde_numerical.md`（**Task 1 已交付、已过独立复核**）。
★ **与相邻方法的边界**：**只与时间有关**（无空间）⇒ `references/mechanism/ode_ivp.md`；**一维输运**（平流 / 扩散 / 波动）⇒ `references/mechanism/transport.md`；**反应 + 扩散耦合** ⇒ `references/mechanism/reaction_diffusion.md`；**参数未知** ⇒ `references/mechanism/param_id_stability.md`。

## ① 适用判据

- **用**：方程含**空间导数**（`u_xx`、`∇²u`、`u_x`），按类型分——**抛物型**（`u_t = D u_xx`，扩散/热传导）· **椭圆型**（`∇²u = f`，稳态）· **双曲型**（`u_tt = c² u_xx`，波动）；要**整场分布**（空间剖面随时间的演化，或稳态场）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **只有一个自变量**（纯时间 ODE）⇒ 别硬写成 PDE，走 `references/mechanism/ode_ivp.md`。
  2. **只有平流 / 简单一维输运**，格式选型（迎风 / 中心 / Lax-Wendroff）是重点 ⇒ 走 `references/mechanism/transport.md`。
  3. **反应项是主角**（反应扩散耦合、行波）⇒ 走 `references/mechanism/reaction_diffusion.md`。
  4. **要的是空间某个量的最优布点**（不是求场）⇒ 属 `optimization` 类。
  5. **硬上显式格式处理刚性抛物型**（`D` 大 / 网格细）⇒ 稳定域 `r=D dt/dx² ≤ 0.5` 会把 `dt` 逼到极小 ⇒ 换**隐式**（`ode15s` 线方法 / Crank-Nicolson）。

## ② 标准建模步骤

1. **定方程类型与边界/初值**：抛物型给初值 + 边界；椭圆型给纯边界；双曲型给两个初值（`u` 与 `u_t`）。
2. **空间离散**：有限差分离散 `u_xx`（中心差分）、`u_x`（迎风 / 中心）；得 ODE 组（**线方法 MOL**）。
3. **选积分器**：抛物型刚性 ⇒ `ode15s`；或用 `pdepe`（一维抛物/椭圆，内置）；显式差分则**先核稳定域**。
4. **时间推进 / 求稳态**：双曲型注意 CFL；椭圆型直接解线性系统。
5. **求数值解整场**。
6. **数值验证**（★ 见 ⑥）：对本**有分离变量闭式解**的算例比逐点误差 + **步长减半看误差按阶下降**（空间二阶 ⇒ 比值 ~4）。
7. **报告**：时空演化图 / 空间剖面图 + 边界条件 + 网格与容差。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 方程系数（`D`、`c`…）· 空间域与网格 `N` · 时间区间 `T` · 初值 / 边界条件 · 积分容差 |
| **输出** | 整场 `u(x,t)` · 剖面 / 时空图 · 收敛阶读数 |

**显式假设（必须写进论文）**：
1. **方程类型与边界条件类型**（Dirichlet / Neumann / 周期）写清 —— **边界写错会把解整体带偏**（实测：Task 1 初版把 Dirichlet 误写成 Neumann，`u(0.5,1)` 偏到 `6.3e-1`）。
2. **网格足够细**（空间分辨率要能解析解的最小尺度）。
3. **显式格式的稳定域**满足（`r ≤ 0.5` 等），或改用隐式。
4. **物性系数定常**（`D`、`c` 不随 `x,t` 变；变系数另论）。
5. **容差与网格匹配**：核空间阶时 ODE 积分容差要收紧，否则**掩盖空间阶**（见 ④）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **边界条件写错**：`pdepe` 的 `q=1` 是 Neumann（绝热），Dirichlet 要 `p=u, q=0`。**实测**（Task 1）：写成 `q=1` 时 `u(0.5,1)` 偏到 `6.3e-1`，改成 Dirichlet 后 `pdepe` 与解析同值到 `O(h²)`（`max|u-u_exact|=8.354e-4`）。
2. ★ **默认积分容差掩盖空间阶**：同一 `pdepe`、同网格，**只改 ODE 容差**，收敛比大不同。**实测**（Task 1）：默认容差比 `2.9080 / 1.8196`（看不出二阶），收紧到 `RelTol=1e-9, AbsTol=1e-11` 后 `4.2030 / 4.1007`（干净二阶）⇒ 核空间阶**必须收紧容差**。
3. **显式格式越稳定域**：`D dt/dx² > 0.5` 时显式 FTCS **振荡发散**（凭经验 + 教材级 von Neumann 分析）。
4. **双曲型不看 CFL**：`c dt/dx > 1` 时迎风格式失真（见 `references/mechanism/transport.md`）。
5. ★ **拿 `pdepe` / `ode15s` 当"独立参照"**：它们是**实现**（同机同实现不独立，任务书 B）——真参照是**分离变量闭式解 + 收敛阶**。
6. **网格与容差都不报**：论文里必须写 $N$、$\Delta t$、容差，否则不可复现（凭经验）。

## ⑤ 输出模板

- **时空演化图**（`u(x,t)` 的等高线 / 瀑布图）或**多时刻剖面图**（同一张图上若干 `t` 的 `u(x)`）+ 边界条件表。
- 图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；网格 / 容差表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/mechanism/pde_numerical.m`（**零参可跑**，自带算例 `u_t = D u_xx`，`u(0,t)=u(1,t)=0`，`u(x,0)=sin(pi x)`）。

关键片段（**不整份复制**）：
```matlab
% 做法① pdepe（空间二阶）：Dirichlet 边界 p=u, q=0；★ 显式收紧容差
sol = pdepe(0, @(x,t,u,DuDx) deal(1, D*DuDx, 0), ...
            @(x) sin(pi*x), @(xl,ul,xr,ur,t) deal(ul,0,ur,0), ...
            xmesh, tmesh, odeset('RelTol',1e-9,'AbsTol',1e-11));
% 做法② 线方法 MOL + ode15s（刚性）
```
**独立参照**：`tests/skills/model-select/verify/pde_numerical.md`（**第 1 类：解析解 + 收敛阶** —— 分离变量 `u=exp(-D pi² t) sin(pi x)`；**实测** N=20/40 误差比 `4.202961`、`u(0.5,1)` 数值与解析差 `4.376e-4`）。
★ **起点素材**：无（Task 1 已确认 `corpus/algorithms/src/` 里 PDE 数值解为 0；本类为 `补`）——内置 `pdepe` / `ode15s` **只作实现，非独立参照**。

## 语料面（P6）

- **语料指针（带）**：`corpus/papers/MODEL_MAP.md` 里 `partial differential equation` 命中 **3 篇**（`P2025-A-01` · `P2025-A-04` · `P2025-E-02`；当场 `grep -nE "^ +- .*partial differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ **2 行**，篇数 `2 + 1 = 3`）。
  ★ **不许与 `differential equation` 的篇数相加**：PDE 那 **3 篇**是 `differential equation` 那 **6 篇**的子集（该 tag 带锚 **3 行**、篇数 `2 + 1 + 3 = 6`；`{A-01,A-04,E-02} ⊆ {A-01,A-04,B-06,E-01,E-02,E-03}`）⇒ PDE **不是额外的 3 篇**。
  ★ **口径说明**：本行**原写** `grep -c "partial differential equation"` 的"**16 行**"（承接 Task 1）—— 那是**裸模式**，把 `MODEL_MAP.md` 的聚合表行一并计入（T5/T6/T7 已定"不许用裸模式"是同一型）。**2026-10-04 依 Task 8 复核 Q3 改为带锚形**（全库唯一两处裸 `grep -c` 之一，见 `docs/mcm-suite-todo.md` §H.2.2「语料计数口径」条）。
- **算法素材面**：**0**（Task 1 已确认）—— 本方法属 `补`，**内置 `pdepe`/`ode15s` 只作实现**。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
