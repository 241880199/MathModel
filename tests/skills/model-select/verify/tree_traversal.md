# 参照记录 · `tree_traversal`（树 / 遍历 / Huffman）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/network/tree_traversal.m`
**语料面（P6）**：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `tree traversal` 与 `Huffman` 带锚 **均 0 行**（2026-10-04 当场复跑 `grep -cE "^ +- (tree traversal|Huffman)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
★ **正对照**：同形态 `centrality` 带锚 ⇒ `3 行`。★ **陷阱**：`decision tree` 带锚 **1 行（11 篇）** —— 那是**分类模型**，**不是本类树遍历**，**不并入**（★ **订正**：原写"带锚 11 行"是**把篇数当行数**、同 Task 11 复核 M2）。
★ **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/detailed/树/BFS.m` · `corpus/algorithms/src/GraphTheory(图论)/detailed/树/DFS.m` · `corpus/algorithms/src/GraphTheory(图论)/detailed/树/Huffman.m` —— 教辅级**起点素材**，**不作独立参照**。

## ① 参照类型
**第 3 类：手算小图**（GC6）—— 小树的 BFS / DFS 序 + Huffman 码长，**手算**，与骨架逐位比。

## ② 参照来源（算式 + 手算）
- **树**：边 1-2 · 1-3 · 2-4 · 2-5 · 3-6，根 1。
- **BFS 手算**（队列层序）：1 → 邻 2,3 → 2 的邻 4,5 → 3 的邻 6 ⇒ `1 2 3 4 5 6`。
- **DFS 手算**（升序邻接、递归）：1 → 2 → 4 → 回溯 → 5 → 回溯 → 3 → 6 ⇒ `1 2 4 5 3 6`。
- **Huffman 手算**（权 `[5 9 12 13 16 45]`，反复合并两个最小权）：
  - `5+9 = 14`
  - `12+13 = 25`
  - `14+16 = 30`
  - `25+30 = 55`
  - `45+55 = 100`
  码长（合并次数）：`5→4, 9→4, 12→3, 13→3, 16→3, 45→1`；加权路径长 `5·4 + 9·4 + 12·3 + 13·3 + 16·3 + 45·1 = 20+36+36+39+48+45 = 224`。
- **参照与骨架不同源**：手算走**逐层 / 逐次合并算术**；骨架是 BFS 队列、DFS 递归、Huffman 建树实现。
  ★ **诚实说明**：手算与骨架同一算法 ⇒ **符号核对 + 逐位数值核对**；独立性来自"手算按定义逐点/逐次推、与代码无关"。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/network'); tree_traversal"
```

## ④ 两边读数
| 量 | 骨架 | 参照（手算） | 是否一致 |
| :--- | :--- | :--- | :--- |
| BFS 序 | `1 2 3 4 5 6` | `1 2 3 4 5 6` | **逐位相同** |
| DFS 序 | `1 2 4 5 3 6` | `1 2 4 5 3 6` | **逐位相同** |
| Huffman 码长 | `[4 4 3 3 3 1]` | `[4 4 3 3 3 1]` | **逐位相同** |
| Huffman 加权路径长 | `224` | `20+36+36+39+48+45 = 224` | **相同** |

（骨架内置 `hand-computed ... => MATCH` 自检行；本方法**确定性**（DFS 按升序邻接），故无需多运行分布。）

**结论**：BFS `1 2 3 4 5 6` · DFS `1 2 4 5 3 6` · Huffman 码长 `[4 4 3 3 3 1]` · WPL `224`，与**手算逐位相同**。
★ **本记录验证**"遍历序与 Huffman 码长算得对"；**不验证**"该不该用树 / Huffman 建模"（建模判断）。
