# ODE 初值问题（Euler / RK4）（`ode_ivp.m`）

> **给"状态随时间演化、且已知初始状态"的连续时间系统用**：题面能写成 `dy/dt = f(t, y)`、并给出 `y(t0) = y0` ⇒ 用数值积分（Euler / RK4 / 自适应）求出轨迹。

**归属**：类索引 `references/mechanism.md` · 骨架 `assets/matlab/mechanism/ode_ivp.m` · 参照 `tests/skills/model-select/verify/ode_ivp.md`。
★ **与相邻方法的边界**：**两端给边界条件（不是初值）** ⇒ `references/mechanism/ode_bvp_shooting.md`；**自变量是离散时间步**（`x_{k+1}=f(x_k)`）⇒ `references/mechanism/difference_equations.md`；**含空间维度 / 刚性 PDE** ⇒ `references/mechanism/pde_numerical.md`；**方程形态已知、参数未知** ⇒ `references/mechanism/param_id_stability.md`。

## ① 适用判据

- **用**：题面给出**连续时间**的状态方程 `dy/dt = f(t, y)`（一阶，或高阶化成一阶组）**加初始条件** `y(t0)=y0`；要**轨迹 / 终态 / 峰时 / 稳定时间**这类**向前演化**的量；`f` 可只给到"能算函数值"的粒度（黑箱也行）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **边界条件在两端**（如 `y(0)=0`、`y(1)=1`）——初值积分**给不出**满足右端条件的轨线 ⇒ 走打靶 / 边值问题（`references/mechanism/ode_bvp_shooting.md`）。
  2. **自变量是离散步**（`x_{k+1}=a x_k`），写成微分方程会**改掉原系统** ⇒ 走 `references/mechanism/difference_equations.md`。
  3. **方程本有闭式解且只要解析式**（求通解、看解的族结构）⇒ 走 `references/mechanism/reduce_order.md`，别拿数值解当解析解。
  4. **刚性系统**（快慢尺度悬殊）用显式 Euler / RK4 会**要求极小步长**才能稳定 ⇒ 换 `ode15s`（隐式），或按 `pde_numerical` 的线方法处置。
  5. **参数未知、要从数据里反推** ⇒ 那是参数辨识（`references/mechanism/param_id_stability.md`），不是"给定参数算轨迹"。

## ② 标准建模步骤

1. **把高阶化成一阶组**：`y'' = g(t,y,y')` ⇒ 令 `y1=y, y2=y'`，得 `[y1;y2]' = [y2; g]`（本类的降阶，见 `references/mechanism/reduce_order.md`）。
2. **写清右端函数 `f(t,y)` 与初值 `y0`**：这是题面直接给 / 由守恒律、速率假设推出的。
3. **选格式**：Euler（1 阶、最省、仅作教学 / 粗算）· RK4（4 阶，定步长通用）· 自适应法（`ode45` 非刚性 / `ode15s` 刚性）。
4. **定步长 / 容差**：定步长按"解的时间尺度"选（走过特征时间要几十步以上）；自适应给 `RelTol/AbsTol`。
5. **求解并记录轨迹**：`[t, y]`。
6. **做数值验证**（★ 见 ⑥）：对**有闭式解的算例**比逐点误差 + **步长减半看误差按阶下降**（Euler ~2、RK4 ~16）。
7. **报告**：轨迹图 + 关键读数（终态 / 峰时 / 最大浓度等）。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 右端函数 `f(t,y)` · 初值 `y0` · 时间区间 `[t0,T]` · 步长 `h` 或容差 `RelTol/AbsTol` |
| **输出** | 时间网格 `t` · 状态轨迹 `y(t)` · （定步长）收敛阶读数 |

**显式假设（必须写进论文）**：
1. **确定性**：`f` 与 `y0` 已知且无随机项（有随机 ⇒ 随机微分方程，超出本骨架）。
2. **解存在唯一且足够光滑**：区间上 `f` 对 `y` Lipschitz（保证初值问题良定、格式收敛）。
3. **初值即真实初始状态**：`y0` 是被给定/测量来的，其误差会随演化传播（要写清来源与不确定度）。
4. **定步长格式的稳定性限制**：显式 Euler 对 `y'=λy` 需 `|1+hλ|≤1`（`λ<0` 时 `h ≤ 2/|λ|`）；RK4 稳定域更大但**仍有界**。
5. **单位与量纲自洽**（物理机理类必备）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把"跑通"当"算对"**：`ode45` 退出码 0 只说明"不崩"，**不说明步长够到收敛**。**实测**（本骨架）：`y'=-2y, y(0)=1` 上 Euler 全球误差 `O(h)`、RK4 `O(h^4)`，必须**步长减半比一比**才见阶（Euler 比值 `2.032`、RK4 `17.396`，见参照件）。
2. **高阶方程忘记降阶 / 降错**：`y''=g` 写成 `[y1;y2]'=[y2;g]`，**二阶导不能直接塞回一阶**（凭经验，最常见的写法错）。
3. ★ **拿 `ode45` 当"独立参照"**：它只是**实现**；同机同实现**不构成独立验证**（任务书 B / GC6）。本方法的**真参照是有闭式解的算例 + 收敛阶**（见 ⑥ 与参照件）。
4. **步长与解的时间尺度不匹配**：`h` 比特征时间还大 ⇒ 结果完全失真；`h` 太小 ⇒ 白费算力（凭经验）。
5. **刚性硬上显式格式**：显式 Euler/RK4 在刚性系统上要极小步长 ⇒ 直接换 `ode15s`（凭经验 + 教材级稳定域分析）。
6. **只给一条曲线、不给步长**：论文里必须写**用的什么格式、步长/容差多少**，否则结果不可复现（凭经验，对应 `mcm-selfreview` 的可复现性检查）。

## ⑤ 输出模板

- **轨迹图**（`y` vs `t`，多状态多条线）+ **关键读数表**（终态、峰时/峰值、达到稳态的时间）。
- 图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；读数 / 参数表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **可选**：把"步长 vs 对数误差"画成收敛阶图（论文里加分，能一眼看出格式阶数）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/mechanism/ode_ivp.m`（**零参可跑**，自带算例 `dy/dt = lambda*y`, `y(0)=1`，`lambda=-2`）。

关键片段（**不整份复制**）：
```matlab
odefun = @(t, y) lambda * y;         % 一阶化：高阶系统这里换成 [y2; g]
y_exact = exp(lambda * T);           % ★ 有闭式解的算例 ⇒ 真参照
% Euler（1 阶）与 RK4（4 阶）：各跑 h 与 h/2，比误差比
euler_ratio = euler_err_h  / euler_err_h2;   % ~ 2
rk4_ratio   = rk4_err_h    / rk4_err_h2;     % ~ 16
```
**独立参照**：`tests/skills/model-select/verify/ode_ivp.md`（**第 1 类：解析解 + 收敛阶** —— 闭式解 `y=exp(lambda*t)`、步长减半误差比实测 `Euler 2.032` / `RK4 17.396`）。
★ **起点素材**（**`盘` 上、可读、不作独立参照** —— 未经净室重写）：
`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Explicit_Euler.m` ·
`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Classical_RK4.m` ·
`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Classical_RK4s.m`。

## 语料面（P6）

- **语料指针（有）**：`corpus/papers/MODEL_MAP.md` 里 `ordinary differential equation` 命中 **1 行**（`P2025-B-03`；当场 `grep -nE "^ +- .*ordinary differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行）；泛称 `differential equation` 另命中 **6 行**（含 `partial` / `ordinary` 一并命中；当场 `grep -nE "^ +- .*differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 6 行）。
  ★ **不许与 PDE 面相加**：那 6 行里含 `partial differential equation`（与 `pde_numerical` 的重叠），两数**不是**不相交的（同 GC/P6 的"重叠不算额外行"口径）。
  ⇒ **ODE 初值问题在获奖语料里有实例**（2025 A / B / E 题的机理方程），**带指针**。
- **算法素材面**：`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/`（`Explicit_Euler.m` · `Classical_RK4.m` · `Classical_RK4s.m`）—— 教辅级**起点素材**，**不作独立参照**。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
