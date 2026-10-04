# 参照记录 · `euler_hamilton`（欧拉图 / Hamilton 图）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/network/euler_hamilton.m`
**语料面（P6）**：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `Euler` 与 `Hamilton` 带锚 **均 0 行**（2026-10-04 当场复跑 `grep -cE "^ +- (Euler|Hamilton)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
★ **正对照**：同形态 `centrality` 带锚 ⇒ `3 行`。
★★ **上游缺陷**：`corpus/algorithms/src/GraphTheory(图论)/detailed/Euler图和Hamilton图/Fleuf1.m` 被 `corpus/algorithms/INDEX.md` §10.1 登记为**给出非法欧拉回路**（确证算法性缺陷）⇒ **不拿它当参照**；净室重写版在 `corpus/algorithms/fixed/euler_circuit.m`。

## ① 参照类型
**第 3 类：手算小图**（GC6）—— 小图欧拉回路**合法性**、`C5` 的 Hamilton 回路，**手算**，与骨架逐位比。
★ 归档净室重写版 `corpus/algorithms/fixed/euler_circuit.m`（第 2 类候选，11 项里唯一对得上）**本算例未用** —— 首选手算。

## ② 参照来源（算式 + 手算）
- **欧拉图**：边 1-2, 2-3, 3-1, 3-4, 4-5, 5-3。度：`deg(1)=2, deg(2)=2, deg(3)=4, deg(4)=2, deg(5)=2` ⇒ **全偶 + 连通 ⇒ 欧拉回路存在**。
  **合法性手算**（对骨架给出的回路 `1 2 3 4 5 3 1`）：逐边 = `1-2, 2-3, 3-4, 4-5, 5-3, 3-1` ⇒ **恰为全部 6 条边各一次**，且**首尾相接**（回到 1）✓。
- **Hamilton 图**：`C5`（顶点 1-2-3-4-5-1）。手算回路 `1 2 3 4 5 1`：每点恰一次、闭合 ✓。
- **参照与骨架不同源**：手算走**度判据 + 逐边核对**；骨架是 Hierholzer + 回溯实现。
  ★ **诚实说明**：本算例验证的是**回路合法性**（结构性质），与骨架**同源算法**；独立性来自"手算是人按度判据与边集核对、与代码无关"。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/network'); euler_hamilton"
```

## ④ 两边读数
| 量 | 骨架 | 参照（手算） | 是否一致 |
| :--- | :--- | :--- | :--- |
| 欧拉回路存在 | `1`（度全偶） | 存在（6 边、度全偶） | 一致 |
| 欧拉回路 | `1 2 3 4 5 3 1` | 合法（6 边各一次、闭合） | 一致 |
| Hamilton 回路 | `1 2 3 4 5 1` | `1-2-3-4-5-1` | **逐位相同** |

（骨架内置 `hand-computed ... => MATCH` 自检行；本方法**确定性**，故无需多运行分布。）

**结论**：欧拉回路 `1 2 3 4 5 3 1`（6 边各一次、首尾相接）与 Hamilton 回路 `1 2 3 4 5 1`，与**手算合法性核对一致**。
★ **本记录验证**"回路存在性与合法性算得对"；**不验证**"该不该用欧拉 / Hamilton 建模"（建模判断）。
