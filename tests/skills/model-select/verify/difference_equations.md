# 参照记录 · `difference_equations`（差分方程 / 离散动力系统）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/difference_equations.m`
**语料面（P6）**：`[社区]` —— `difference equation` 在 `corpus/papers/MODEL_MAP.md` **0 命中**（2026-10-04 当场复跑）；
离散 ≠ 连续 ⇒ **不能**拿 `differential equation` 那 25 行为它背书。**教科书级常识**。

## ① 参照类型
**第 1 类：解析解 + 收敛阶**。标量线性递推有闭式解；稳定性有解析判据。

## ② 参照来源
- 闭式解：`x_{n+1} = a x_n` ⇒ `x_n = a^n x_0`（一阶线性差分方程标准解，教科书级）。
- 稳定性判据：标量 `|a| < 1`；向量 `x_{n+1} = A x_n` ⇒ 稳定性 ⟺ 谱半径 `rho(A) = max|eig(A)| < 1`。
- **起点素材**（可读、**不可当独立参照** —— 它在 `corpus/algorithms/src/` 里、不在 `fixed/` 六件内，GC6 禁止）：
  `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH15/rsolve.m`（只覆盖线性定常离散系统、用符号 z 变换）。
- 参照与骨架**不同源**：闭式解是纸上解析式，骨架是逐项数值迭代，二者无共享实现。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); difference_equations"
```

## ④ 两边读数
| 量 | 骨架（数值迭代） | 参照（解析） | 差 |
| :--- | :--- | :--- | :--- |
| `x_10`（`a=0.5, x0=1, N=10`） | `0.0009765625` | `a^N*x0 = 0.0009765625` | `0.000e+00` |
| 谱半径 `rho(A)`，`A=[0.8 0.1; 0 -0.5]` | `0.8` | `max|eig(A)| = 0.8` | `0` |
| 稳定性（`rho<1`） | `1`（stable） | `0.8 < 1` ⇒ stable | — |

★ **注**：上表**谱半径 `rho(A)` 行**（及其下的稳定性行）是**符号核对（解析对解析）** —— 两侧同用 `eig`（骨架与参照都调 `eig`）⇒ **本行是符号核对，不是数值验证**；本方法的**数值验证在 `x_10` 行**（逐项数值迭代 vs 闭式解 `a^N x_0`，逐位相同）。

**结论**：数值迭代与闭式解**逐位相同**（误差 0）；谱半径判据与解析一致。
