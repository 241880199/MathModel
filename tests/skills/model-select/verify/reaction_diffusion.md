# 参照记录 · `reaction_diffusion`（反应扩散 · Fisher-KPP）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/reaction_diffusion.m`
**语料面（P6）**：`[社区]` —— `reaction diffusion` / `reaction-diffusion` 在 `corpus/papers/MODEL_MAP.md` **0 命中**（2026-10-04 当场复跑）
⇒ **教科书级常识**。

## ① 参照类型
**第 1 类：有闭式解的参数取值**（取无反应的纯扩散退化）。

## ② 参照来源
- 模型：`u_t = D u_xx + r u (1 - u)`（Fisher-KPP）。
- **退化检验（主参照）**：令 `r = 0`（纯扩散），`u0 = sin(pi x)`、两端 0 ⇒ 分离变量闭式
  `u(x,t) = exp(-D pi^2 t) sin(pi x)`。
- **附解析性质（旁证）**：Fisher 行波最小前速 `v* = 2 sqrt(D r)`。
- 参照与骨架**不同源**：闭式解/行波速度是纸上解析式，数值解是显式 FTCS，无共享实现。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); reaction_diffusion"
```

## ④ 两边读数（`D = 0.1`, `r = 1`, `N = 50`, 纯扩散 `T = 1`）
| 量 | 骨架（数值） | 参照（解析） | 差 |
| :--- | :--- | :--- | :--- |
| (a) `r=0` 纯扩散 `max|u-u_exact|` | `1.765451e-04` | `0` | `O(dx^2)` |
| (b) Fisher 前速（t: 60→100） | `0.618220` | `0.632456`（`2 sqrt(D r)`） | `-2.2%` |

**结论**：主参照（`r=0` 退化到纯扩散）与闭式解同值到二阶 ⇒ "算得对"的硬核成立。
★ (b) 为**旁证**、非本类硬核：有限时间测量前速**收敛于**解析值（另测 t: 30→60 得 `0.657`，即从上方逼近）
⇒ 与 `2 sqrt(D r)` 在**有限时窗测量误差（~±3%）**内一致，**不声称精确相等**。

## ⑤ 为什么用显式 FTCS 而不是 `pdepe`（★ 设计取舍，非"内置不可用"）

Fisher-KPP **本可用 MATLAB 内置的 `pdepe` 直接求解**（无需手写差分）—— 2026-10-04 本机复跑证实：
同本类问题设置（域 `(0,1)`、`u0=sin(pi x)`、`u(0)=u(1)=0`、`D=0.1`、`r=1`、`T=1`），`pdepe` 跑通并给 `u(0.5,1)=0.541374`。
```
matlab -batch "sol=pdepe(0,@(x,t,u,d)deal(1,0.1*d,u*(1-u)),@(x)sin(pi*x),@(xl,ul,xr,ur,t)deal(ul,0,ur,0),linspace(0,1,200),linspace(0,1,41),odeset('RelTol',1e-9,'AbsTol',1e-11)); fprintf('pdepe Fisher-KPP u(0.5,1) = %.6f\n', interp1(linspace(0,1,200),sol(end,:),0.5))"
```

**本骨架仍选显式 FTCS**，是**设计取舍**，**不是"没有内置可用"**：
- 显式格式把**反应项 + 扩散项逐拍显现** ⇒ **机理可见**（`mechanism` 类方法文件要教的正是这个）；
- 该显式格式**已过独立参照**（上表 (a)：`r=0` 退化到纯扩散，与闭式解同值到二阶）。

⇒ **两条路都给**：要**机理可见性**（教学 / 建模演示）用本骨架的显式 FTCS；**只要数值结果**、不在乎机理可见性时，**`pdepe` 可直接解 Fisher-KPP**。
