# 参照记录 · `pde_numerical`（PDE 数值解 · 抛物型热方程）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/pde_numerical.m`
**语料面（P6）**：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `partial differential equation` 命中 **3 篇**（`P2025-A-01` · `P2025-A-04` · `P2025-E-02`；当场 `grep -nE "^ +- .*partial differential equation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 2 行：`:41` 2 篇 · `:247` 1 篇）。
★ 该 **3 篇是 `differential equation` 那 6 篇的子集**（`differential equation` 带锚 3 行、篇数 `2 + 1 + 3 = 6`）⇒ **不许并列相加**（PDE 不是额外的 3 篇）。
★ **口径订正（2026-10-04 Task 8 复核 Q3）**：本行**原写** `grep -c "partial differential equation"` 的"**16 行**"——那是**裸模式**，含 `MODEL_MAP.md` 聚合表行（同 T5/T6/T7 已定的"裸模式会多计"型）。**已改带锚形**（全库唯一两处裸 `grep -c` 之一）。

## ① 参照类型
**第 1 类：解析解 + 收敛阶**（分离变量解 + 步长减半误差按阶下降）。

## ② 参照来源
- 问题：`u_t = D u_xx`，`x∈(0,1)`，`u(0,t)=u(1,t)=0`，`u(x,0)=sin(pi x)`。
- 解析解（分离变量，教科书级）：`u(x,t) = exp(-D pi^2 t) sin(pi x)`。
- 两种数值做法**均用 MATLAB 内置**：① `pdepe`（空间二阶）；② 线方法（MOL）+ `ode15s`（刚性）。
- 参照与骨架**不同源**：解析解是纸上表达式，数值解是有限差分/自适应积分，无共享实现。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); pde_numerical"
```

## ④ 两边读数（`D = 0.1`, `T = 1`）
| 量 | 骨架（数值） | 参照（解析） | 差 |
| :--- | :--- | :--- | :--- |
| `u(x=0.5,t=1)`，`pdepe`，N=20 | `0.372270238013839` | `0.372707838853438` | `4.376e-04` |
| `max|u-u_exact|`，N=20 | `8.353854e-04` | `0` | — |
| `max|u-u_exact|`，N=40（步长减半） | `1.987611e-04` | `0` | — |
| **收敛阶比（N vs 2N）** | **`4.202961`** | 2 阶 ⇒ 约 `4` | — |
| `max|u-u_exact|`，MOL+`ode15s`，N=20 | `1.264428e-03` | `0` | — |

**结论**：`u(0.5,1)` 数值与解析同值到 `O(h^2)`；步长减半误差比 **4.20**（另测 N=40/80 为 **4.10**）⇒ 确为二阶收敛。
（初版曾因 `pdepe` 边界条件写成 `q=1`（Neumann/绝热）而偏到 `6.3e-01`，已修正为 Dirichlet `p=u,q=0`。）

## ⑤ 容差敏感性（★ 默认积分容差会掩盖空间阶）

同一 `pdepe`、同一网格，**只改 ODE 积分容差**，误差与收敛比大不相同（2026-10-04 本机复跑）：

| 容差 | `err N=20` | `err N=40` | `err N=80` | 比 `N20/N40` | 比 `N40/N80` |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **默认**（不传 `options`） | `9.716361e-04` | `3.341218e-04` | `1.836196e-04` | **`2.9080`** | **`1.8196`** |
| **紧**（`RelTol=1e-9, AbsTol=1e-11`，本骨架所用） | `8.353854e-04` | `1.987611e-04` | `4.846966e-05` | **`4.2030`** | **`4.1007`** |

**结论**：**默认积分容差会掩盖空间离散阶** —— 比值 `2.91 / 1.82` 既不为 2 也不为 4，看不出二阶；**收紧容差后才恢复干净二阶**（`4.20 / 4.10`）。本骨架 `pdepe_heat` 因此**显式传入** `odeset('RelTol',1e-9,'AbsTol',1e-11)`（见 `.m` 的 `pdepe_heat`）。⇒ 用 `pdepe` 核空间阶时**必须**收紧 ODE 容差。

**复跑命令**（复现上表两行读数）：
```
matlab -batch "D=0.1;T=1;Nv=[20 40 80]; for t=1:2; if t==1; oo=[]; nm='default'; else; oo=odeset('RelTol',1e-9,'AbsTol',1e-11); nm='tight  '; end; e=zeros(1,3); for k=1:3; N=Nv(k); s=pdepe(0,@(x,t,u,d)deal(1,D*d,0),@(x)sin(pi*x),@(xl,ul,xr,ur,t)deal(ul,0,ur,0),linspace(0,1,N),linspace(0,1,11),oo); e(k)=max(abs(s(end,:)-exp(-D*pi^2*T)*sin(pi*linspace(0,1,N)))); end; fprintf('%s N20/N40=%.4f  N40/N80=%.4f\n',nm,e(1)/e(2),e(2)/e(3)); end"
```
⇒ 输出 `default N20/N40=2.9080  N40/N80=1.8196` 与 `tight   N20/N40=4.2030  N40/N80=4.1007`。
