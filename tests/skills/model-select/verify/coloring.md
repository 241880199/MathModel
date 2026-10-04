# 参照记录 · `coloring`（染色）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/network/coloring.m`
**语料面（P6）**：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `coloring` 与 `graph coloring` 带锚 **均 0 行**（2026-10-04 当场复跑 `grep -cE "^ +- (coloring|graph coloring)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
★ **正对照**：同形态 `centrality` 带锚 ⇒ `3 行`。
★ **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grColEdge.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grColVer.m` · `corpus/algorithms/src/GraphTheory(图论)/detailed/图的染色/` —— 教辅级**起点素材**，**不作独立参照**。

## ① 参照类型
**第 3 类：手算小图**（GC6）—— 5 环 `C5`，**手算色数 + 贪心着色序**，与骨架的 `colors`、`ncolors`**逐位比**。

## ② 参照来源（算式 + 手算）
- **图**：5 环 `C5`（顶点 1-2-3-4-5-1 首尾相接）。
- **手算色数**：`C5` 是**奇环** ⇒ 不能 2 色（2 色只能着偶环 / 二分图）⇒ `χ(C5) = 3`。
- **手算贪心（Welsh-Powell，度全为 2、按原序）**：
  - 节点 1 ⇒ 色 1。
  - 节点 2（邻 1、3）⇒ 色 2。
  - 节点 3（邻 2、4；不与 1 相邻）⇒ 可取 **色 1**。
  - 节点 4（邻 3、5）⇒ 色 2。
  - 节点 5（邻 4、1，色 1、2 都占）⇒ 色 3。
  ⇒ `colors = [1 2 1 2 3]`，`ncolors = 3`（= χ(C5)）。
- **参照与骨架不同源**：手算走**逐点取最廉色**；骨架是 Welsh-Powell 排序 + 贪心实现。
  ★ **诚实说明**：手算与骨架同一贪心算法 ⇒ **符号核对 + 逐位数值核对**；独立性来自"手算按冲突定义逐点推、与代码无关"。★ 本算例贪心恰达最优；**一般图贪心只给上界**。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/network'); coloring"
```

## ④ 两边读数
| 量 | 骨架 | 参照（手算） | 是否一致 |
| :--- | :--- | :--- | :--- |
| `colors` | `[1 2 1 2 3]` | `[1 2 1 2 3]` | **逐位相同** |
| 色数 `ncolors` | `3` | `3`（= χ(C5)） | **相同** |

（骨架内置 `hand-computed ... => MATCH` 自检行；本方法**确定性**，故无需多运行分布。）

**结论**：色数 `3`、着色 `[1 2 1 2 3]`，与**手算色数 + 贪心序逐位相同**。
★ **本记录验证**"色数与着色算得对（本算例贪心达最优）"；**不验证**"该不该用染色建模"（建模判断）。
