# 参照记录 · `ode_ivp`（ODE 初值问题 Euler / RK4）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/ode_ivp.m`
**语料面（P6）**：**有语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `ordinary differential equation` 命中 **1 行**（`P2025-B-03`；2026-10-04 当场复跑 `grep -nE "^ +- .*ordinary differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行）；泛称 `differential equation` 另命中 **6 行**（`grep -nE "^ +- .*differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 6 行）。
★ **不许与 PDE 面相加**：那 6 行里含 `partial differential equation`（与 `pde_numerical` 重叠）⇒ 两数**不相交**的假设不成立。
**算法素材面**：`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/{Explicit_Euler.m,Classical_RK4.m,Classical_RK4s.m}` —— 教辅级**起点素材**，**不作独立参照**（GC6）。

## ① 参照类型
**第 1 类：解析解 + 收敛阶**（GC6）—— 取有闭式解的算例，比逐点误差 + **步长减半看误差按阶下降**。
★ **不许拿 MATLAB 内置 `ode45` 当"独立参照"**（同机同实现，不独立）—— 本方法的参照是**闭式解 + 收敛阶**。

## ② 参照来源
- **算例**：`dy/dt = lambda*y`，`y(0)=1` ⇒ **闭式解 `y(t) = exp(lambda*t)`**（教科书级）。
- **收敛阶**：显式 Euler 是 **1 阶**（全球误差 `O(h)`，步长减半误差比 ~ `2`）；经典 RK4 是 **4 阶**（`O(h^4)`，比 ~ `16`）。
- **参照与骨架不同源**：闭式解是纸上解析式；骨架是手写 Euler / RK4 数值迭代；`ode45` 是同机实现（只作交叉核对）。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); ode_ivp"
```

## ④ 两边读数（默认 `lambda = -2`, `T = 1`, `h = 0.1`）
| 量 | 骨架（数值） | 参照（解析） | 差 |
| :--- | :--- | :--- | :--- |
| `y_exact = exp(lambda*T)` | `0.135335283236613` | `0.135335283236613` | `0` |
| Euler 误差（`h`, `h/2`） | `2.796110e-02`, `1.375863e-02` | `0` | — |
| **Euler 误差比（h vs h/2）** | **`2.032259`** | 1 阶 ⇒ 约 `2` | — |
| RK4 误差（`h`, `h/2`） | `4.265194e-06`, `2.451852e-07` | `0` | — |
| **RK4 误差比（h vs h/2）** | **`17.395806`** | 4 阶 ⇒ 约 `16` | — |
| `ode45` 误差（交叉核对，非独立参照） | `3.105849e-14` | `0` | 机器精度 |

**更细档（当场复跑，证 4 阶）**：RK4 误差比 `h=0.1/0.05` ⇒ `17.396`、`h=0.05/0.025` ⇒ `16.682`、`h=0.025/0.0125` ⇒ `16.337`；
Euler 误差比 `h=0.1/0.05` ⇒ `2.032`、`h=0.05/0.025` ⇒ `2.016` ⇒ **分别收敛于 16 与 2**。

**结论**：Euler 误差比收敛于 `2`（1 阶）、RK4 收敛于 `16`（4 阶）⇒ **数值解与解析解同公式、且误差按正确阶下降** ⇒ "算得对"成立。
★ **诚实说明**：该参照验证的是**数值格式算得对不对**，**不验证"该不该用 ODE 初值问题建模"**（那是建模判断）。
★ **`ode45` 只验证实现**（误差 `3.1e-14` 说明自适应实现与我们算的是同一解），**不作独立参照**。
