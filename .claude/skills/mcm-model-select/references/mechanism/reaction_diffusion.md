# 反应扩散（`reaction_diffusion.m`）

> **给"反应 + 扩散耦合"的空间演化题用**：`u_t = D u_xx + r u(1-u)`（Fisher-KPP）这类方程，反应项让状态增长 / 饱和，扩散项让状态在空间铺开 ⇒ 出现**行波前 / 斑图 / 传播速度**。

**归属**：类索引 `references/mechanism.md` · 骨架 `assets/matlab/mechanism/reaction_diffusion.m` · 参照 `tests/skills/model-select/verify/reaction_diffusion.md`（**Task 1 已交付、已过独立复核**）。
★ **与相邻方法的边界**：**纯扩散 / 热传导 / 波动**（无反应项）⇒ `references/mechanism/transport.md`；**一般抛物型 PDE（含刚性、内置）** ⇒ `references/mechanism/pde_numerical.md`；**空间均匀的仓室传播**（SIR）⇒ `references/mechanism/sir_seir.md`。

## ① 适用判据

- **用**：方程同时含**反应项**（局部增长 / 衰减 / 饱和，如 `r u(1-u)`）与**扩散项**（`D u_xx`）；要**行波前速度、传播、斑图形成**；或生态入侵、化学波、种群空间扩张。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **只有扩散、无反应**（纯热传导）⇒ 走 `references/mechanism/transport.md`。
  2. **空间均匀**（无扩散，只是 ODE / 仓室）⇒ 走 `references/mechanism/ode_ivp.md` 或 `references/mechanism/sir_seir.md`。
  3. **要的是斑图的精细结构（Turing 斑图）**⇒ 需多组分 + 参数区间分析，单组分 Fisher 不够（凭经验）。
  4. **要数值结果、不在乎机理可见性** ⇒ 可直接用内置 `pdepe`（见下 ⑤/⑥ 的设计取舍），不必手写 FTCS。
  5. **硬上显式格式处理刚性强反应** ⇒ 稳定域 `r=D dt/dx² ≤ 0.5` 且反应尺度可能更严 ⇒ 换隐式。

## ② 标准建模步骤

1. **写方程**：`u_t = D u_xx + f(u)`（Fisher：`f(u)=r u(1-u)`）。
2. **定域与边界**：有界域 + 两端边界条件（本骨架 Dirichlet）。
3. **定初值**：本骨架纯扩散检验用 `u0=sin(pi x)`；行波检验用阶跃 `u0≈tanh`。
4. **空间离散 + 时间推进**：显式 FTCS（`u(2:end-1)` 中心差分 + 反应项）。
5. **定时间步**：`dt = 0.4 dx²/D`（稳在 `r=D dt/dx² ≤ 0.5` 以内）。
6. **数值验证**（★ 见 ⑥）：**退化检验** —— 令反应项 `r=0`，退回纯扩散，比闭式解。
7. **报告**：行波前位置 / 速度 + 斑图 / 剖面 + 与解析前速对比。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 扩散系数 `D` · 反应率 `r` · 网格 `N` · 时间区间 `T` · 初值与边界 |
| **输出** | 整场 `u(x,t)` · 行波前速 · 退化检验误差 |

**显式假设（必须写进论文）**：
1. **常系数**（`D`、`r` 定常）。
2. **一维、均匀网格**、显式稳定域满足。
3. **边界条件类型**写清（本骨架 Dirichlet）。
4. **单组分**（Fisher-KPP）；多组分（捕食+扩散等）要扩方程。
5. **行波前速的有限时窗测量有偏差**（本骨架从上方逼近解析 `2 sqrt(D r)`，不声称精确相等）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **行波前速不能"精确等于"解析最小波速**：有限时窗测量有偏差。**实测**（Task 1）：t:60→100 测 `0.618220` vs `2 sqrt(D r)=0.632456`（`-2.2%`）；t:30→60 测 `0.657`（从上方逼近）⇒ **与解析值在有限时窗测量误差（~±3%）内一致，不声称精确相等**。
2. ★ **主参照要靠"退化到纯扩散"**：令 `r=0` 退回闭式解才是本类的**硬核**。**实测**（Task 1）：`r=0` 纯扩散 `max|u-u_exact|=1.765451e-04`（`O(dx²)`）。
3. **显式格式越稳定域**：`r=D dt/dx² > 0.5` 振荡发散（凭经验）。
4. **行波域不够长 / 时间不够**：前未充分发展就测速 ⇒ 偏差大（本骨架用 `L=150`、测 `t=60..100`）（凭经验）。
5. ★ **拿 `pdepe` 当"独立参照"**：`pdepe` 是**同机实现**（真参照是退化闭式解）；本骨架手写 FTCS 是**设计取舍**（机理可见），**不是"内置不可用"** —— Fisher-KPP 本可用 `pdepe` 直接解（Task 1 实测 `u(0.5,1)=0.541374`）。
6. **把"前速随时间变化"当成错**：前速应**收敛于**最小波速，短时窗偏大是正常现象（凭经验）。

## ⑤ 输出模板

- **行波演化图**（多时刻剖面叠加，看前沿推进）+ **前速 vs 解析值表** + **退化检验误差**。
- 图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；读数表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **两条路都给**：要**机理可见性**用本骨架显式 FTCS；**只要数值结果**可用内置 `pdepe`（见参照件 §⑤）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/mechanism/reaction_diffusion.m`（**零参可跑**，自带算例 Fisher-KPP `D=0.1, r=1, N=50`）。

关键片段（**不整份复制**）：
```matlab
% (a) 退化检验：r = 0 纯扩散，对照闭式 exp(-D pi^2 t) sin(pi x)
u(2:end-1) = u(2:end-1) + lam*(u(3:end) - 2*u(2:end-1) + u(1:end-2));   % 扩散
% (b) Fisher 行波：加反应项，测 u=0.5 穿越点算前速
uf(2:end-1) = uf(2:end-1) + rf*(...) + dtf*r*uf(2:end-1).*(1 - uf(2:end-1));
front_speed_analytic = 2*sqrt(D*r);
```
**独立参照**：`tests/skills/model-select/verify/reaction_diffusion.md`（**第 1 类：有闭式解的参数取值（取无反应退化）** —— `r=0` 闭式解 `u=exp(-D pi² t) sin(pi x)`；**实测** 退化误差 `1.765451e-04`；行波前速旁证 `0.618220` vs `0.632456`）。
★ **起点素材**：无（Task 1 已确认 `corpus/algorithms/src/` 里反应扩散为 0；本类为 `补`）。

## 语料面（P6）

- **语料指针（无）**：`corpus/papers/MODEL_MAP.md` 里 `reaction diffusion` / `reaction-diffusion` **0 命中**（承接 Task 1；当场复跑 `grep -inE "reaction[ -]diffusion" corpus/papers/MODEL_MAP.md` ⇒ 0 行）⇒ 标 `[社区]`（教科书级常识）。
- **算法素材面**：**0**（Task 1 已确认）—— 本方法属 `补`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
