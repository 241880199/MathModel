# 参照记录 · `lotka_volterra`（生态动力学 Lotka-Volterra）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/lotka_volterra.m`
**语料面（P6）**：**带语料指针** —— `corpus/papers/INDEX.md` 的 **P2025-B-03 / E-02 / E-03 / E-04 四篇**在用 Lotka-Volterra（当场 `grep -nE "^ +- .*Lotka-Volterra（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 2 行、篇数 `1 + 3 = 4`）。★ **订正（2026-10-04 M4 终审 W-2）**：原写的命令**少了 `（[0-9]+ 篇）` 锚** ⇒ 实测 3 行（`:840` 是关键词明细行）；**已补锚**。
★ **口径订正（2026-10-04 Task 8 复核 Q3）**：本行**原写** `grep -c "Lotka"` 的"**19 行**"——裸模式，含聚合表行；**已改带锚形**。
★ 注意（GC15）：**"素材 0" ≠ "语料 0"** —— `corpus/algorithms/src/` 里 LV 素材确为 0，但获奖论文语料里 4 篇在用。

## ① 参照类型
**解析性质**（守恒量 / 平衡点 / 周期解存在性）。

## ② 参照来源
- 模型：`dx/dt = alpha x - beta x y`，`dy/dt = -gamma y + delta x y`。
- 平衡点：`(0,0)` 与 `(gamma/delta, alpha/beta)`（后者为中心型）。
- **第一积分（守恒量）**：`H(x,y) = delta x - gamma ln x + beta y - alpha ln y`，轨线应满足 `H ≡ H0`
  ⇒ 守恒量漂移应 ~ 积分容差量级（**周期解存在的依据**）。
- 周期解时间平均 = 平衡点：`x̄ → gamma/delta`、`ȳ → alpha/beta`。
- 参照与骨架**不同源**：守恒量/时间平均性质是纸上解析式，骨架是 `ode45` 数值积分。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); lotka_volterra"
```

## ④ 两边读数（`alpha=beta=gamma=delta=1`, `(x0,y0)=(0.5,0.75)`, `T=200`）
| 量 | 骨架（ode45） | 参照（解析性质） | 差 |
| :--- | :--- | :--- | :--- |
| 平衡点 `(gamma/delta, alpha/beta)` | — | `(1, 1)` | — |
| 第一积分 `max|H(t)-H0|`（`H0=2.23082925301173`） | `2.813e-10` | `0` | 守恒量漂移 ~1e-10 |
| 时间平均 `x_bar` | `1.00441452` | `1`（`gamma/delta`） | `4.4e-03` |
| 时间平均 `y_bar` | `0.995757613` | `1`（`alpha/beta`） | `4.2e-03` |

**结论**：第一积分守恒到 1e-10 ⇒ 周期解存在性成立；两时间平均与平衡点同值到 ~4e-3（长时窗下的有限时段残差）。
