# 参照记录 · `sir_seir`（传染病模型 SIR / SEIR）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/mechanism/sir_seir.m`
**语料面（P6）**：`[社区]` —— `SIR model` / `SEIR` 在 `corpus/papers/MODEL_MAP.md` **0 命中**（2026-10-04 当场复跑；
全库 `corpus/papers/` 检索 `seir` 唯一命中是一个 PNG 的**二进制假匹配**，非文本）⇒ **教科书级常识**。

## ① 参照类型
**解析性质**（守恒量 / `R0` 阈值 / 平衡点 / 最终规模），不是"跟另一段代码对"。

## ② 参照来源
- 守恒量：归一化分数下 `S+I+R = 1`（SIR）、`S+E+I+R = 1`（SEIR）。
- 基本再生数：`R0 = beta / gamma`。
- 最终规模关系（SIR）：`ln(s0 / s_inf) = R0 (1 - s_inf)` ⇒ 用 `fzero` 解出 `s_inf`，应与 `ode45` 末值一致。
- 参照与骨架**不同源**：守恒律与最终规模方程是模型不变量/解析关系，骨架是 `ode45` 数值积分。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/mechanism'); sir_seir"
```

## ④ 两边读数（`beta = 0.6`, `gamma = 0.2`, `I0 = 1e-3`）
| 量 | 骨架（ode45） | 参照（解析性质） | 差 |
| :--- | :--- | :--- | :--- |
| `R0 = beta/gamma` | `3` | `3`（>1 ⇒ 疫情扩散） | — |
| SIR `max|S+I+R-1|` | `1.554e-15` | `0` | 机器精度 |
| SEIR `max|S+E+I+R-1|` | `1.332e-15` | `0` | 机器精度 |
| 最终规模 `s_inf`（末值） | `0.0594477683271942` | `0.0594477683162695`（`fzero` 解最终规模方程） | `1.092e-11` |

**结论**：守恒量守恒到机器精度;数值末态 `s_inf` 与解析最终规模方程的根**同值到 1e-11** ⇒ 强独立佐证。
