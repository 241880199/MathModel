# 参照记录 · `transport`（输运方程 · 平流 / 扩散）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/transport.m`
**语料面（P6）**：**带语料指针（注明"薄"）** —— `corpus/papers/MODEL_MAP.md` 里含 `diffusion` 的**仅 1 行**：
`corpus/papers/MODEL_MAP.md:644`（P2025-E-02 的 "spatial diffusion term"）。
★ **薄**：这是**逐子形态**的读数 —— `heat equation` **0 命中** · `wave equation` **0 命中**（2026-10-04 当场复跑）
⇒ 该方法的**热传导 / 波动子形态无语料背书**，只有"扩散"这一薄支有。

## ① 参照类型
**第 1 类：有闭式解的参数取值**（平流 / 扩散均有闭式解）。

## ② 参照来源
周期域 `(0,1)`、`u0(x)=sin(2 pi x)`，显式有限差分：
- 平流 `u_t + c u_x = 0` ⇒ `u(x,t) = sin(2 pi (x - c t))`；
  ★ 取 **CFL = c·dt/dx = 1** 时迎风格式**精确**（整格平移）。
- 扩散 `u_t = D u_xx` ⇒ `u(x,t) = exp(-D (2 pi)^2 t) sin(2 pi x)`；衰减率解析值 = `D (2 pi)^2`。
- 参照与骨架**不同源**：闭式解是纸上解析式，数值解是显式格式，无共享实现。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); transport"
```

## ④ 两边读数（`c = 1`, `D = 0.1`, `N = 100`, `T = 0.5`）
| 量 | 骨架（数值） | 参照（解析） | 差 |
| :--- | :--- | :--- | :--- |
| 平流 `max|u-u_exact|`（CFL=1） | `7.772e-16` | `0` | 机器精度 |
| 扩散 `max|u-u_exact|` | `1.263e-04` | `0` | `O(dx^2)` |
| 扩散衰减率（数值） | `3.94966147` | `3.94784176`（`D(2pi)^2`） | `1.8e-03` |

**结论**：平流在 CFL=1 时与闭式解**逐位一致**（误差 ~1e-16）；扩散与闭式解同值到二阶，衰减率吻合到 0.05%。
