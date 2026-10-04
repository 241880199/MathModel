# 参照记录 · `maxflow_mincut`（最大流 / 最小割）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/network/maxflow_mincut.m`
**语料面（P6）**：**带语料指针（薄）** —— `corpus/papers/MODEL_MAP.md` 里 `network flow` 带锚 **1 行 / 1 篇**（2026-10-04 当场复跑 `grep -nE "^ +- network flow（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ `:214` = P2025-D-03）。
★ **正对照**：同形态 `centrality` 带锚 ⇒ `3 行`。★ 截断模式 `network` 带锚 ⇒ **0 行**（真 tag 是整串 `network flow`）。
★ **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMaxFlows.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinCutSet.m` —— 教辅级**起点素材**，**不作独立参照**（且 `grMaxFlows` 在 R2025b 不可用，见 §10.5）。

## ① 参照类型
**第 3 类：手算小图**（GC6）—— 5 节点有向网络，**手算最小割 ⇒ 最大流**，与骨架的 `maxflow`、`mincut`**逐位比**。
★ **不许拿 MATLAB 内置 `maxflow` 当"独立参照"**（同机同实现）；本骨架**自写 Edmonds-Karp**，参照是**手算**。

## ② 参照来源（算式 + 手算）
- **网络**：源 1、汇 4；容量 1→2:3 · 1→3:2 · 2→3:1 · 2→4:2 · 3→4:4。
- **手算最小割**（枚举割 `S`），割容量 = 从 `S` 指向 `T` 的弧容量之和：
  - `S={1}`：`1→2(3) + 1→3(2) = 5`。
  - `S={1,2}`：`1→3(2) + 2→3(1) + 2→4(2) = 5`。
  - `S={1,3}`：`1→2(3) + 3→4(4) = 7`。
  - `S={1,2,3}`：`2→4(2) + 3→4(4) = 6`。
  ⇒ 最小割容量 = `5`（取 `S={1}` 或 `{1,2}`）。
- **由最大流最小割定理** ⇒ 最大流 = `5`。
- **手算可行流校核**：1→2 送 3、1→3 送 2；2→4 送 2、2→3 送 1；3→4 送出 3（收 1+2）⇒ 汇 4 收到 `2+3 = 5` ✓，且不超容量。
- **参照与骨架不同源**：手算走**割枚举 + 可行流校核**；骨架是 Edmonds-Karp 残量增广实现。
  ★ **诚实说明**：手算与骨架不同路径（割枚举 vs 增广路），但**同结论**；独立性来自"手算是人按割容量定义枚举、与代码无关"。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/network'); maxflow_mincut"
```

## ④ 两边读数
| 量 | 骨架 | 参照（手算） | 是否一致 |
| :--- | :--- | :--- | :--- |
| 最大流 `maxflow` | `5` | `5` | **相同** |
| 最小割容量 `mincut` | `5` | `5`（`S={1}` 或 `{1,2}`） | **相同** |

（骨架内置 `hand-computed ... => MATCH` 自检行；本方法**确定性、无随机**，故无需多运行分布。）

**结论**：`max flow = 5 = min cut`，与**手算割枚举 + 可行流校核一致**。
★ **本记录验证**"最大流 / 最小割数值算得对"；**不验证**"网络模型建得对"（建模判断）。
