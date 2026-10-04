# 最大流 / 最小割（`maxflow_mincut.m`）

> **要问"一个网络最多能输送多少 / 瓶颈在哪"时用**：在有向容量网络上求源到汇的最大可行流量，其等值于最小割容量（最大流最小割定理）。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/maxflow_mincut.m` · 参照 `tests/skills/model-select/verify/maxflow_mincut.md`。
★ **与相邻方法的边界**：弧上还带**单位费用**、要求**最小费用** ⇒ `references/network/min_cost_flow.md`；只求**两点最短路**（代价）⇒ `references/network/shortest_path.md`。

## ① 适用判据

- **用**：题面有**容量约束**的网络（管道 / 通信 / 交通 / 任务分配），问**最大吞吐**或**瓶颈割**；要**整数 / 流量守恒**解；`max flow = min cut` 可做校核。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **弧上有单位费用** ⇒ 单求最大流不含费用目标 ⇒ 走 `references/network/min_cost_flow.md`。
  2. **边权是"距离 / 代价"而非"容量"** ⇒ 那是最短路（`references/network/shortest_path.md`），不是流。
  3. **要连接所有点、无源汇** ⇒ 那是 MST（`references/network/mst.md`）。
  4. **多源多汇** ⇒ 须先**加超级源 / 超级汇**再建模，不能直接套单源单汇（凭经验）。

## ② 标准建模步骤

1. **建图**：顶点 = 节点，**有向弧** = 传输关系，**弧容量** `c(u,v)`。
2. **定源汇**：指定源 `s`、汇 `t`（多源多汇 → 加超级源 / 汇）。
3. **求最大流**：标号法 / Ford-Fulkerson（本骨架用 **Edmonds-Karp**：BFS 找增广路）。
4. **取最小割**：由残量网络从 `s` 可达集给出割 `(S, T)`。
5. **校核**：`max flow == min cut`。
6. **数值验证**（见 ⑥）：小网络**手算**增广 + 割容量。
7. **报告**：最大流量 + 各弧流量 + 最小割集。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 容量矩阵 `C`（`C(i,j)` = 弧 i→j 容量，`0` = 无弧）· 源 `s` · 汇 `t` |
| **输出** | `maxflow` · `mincut` · `flow`（流量矩阵） |

**显式假设（必须写进论文）**：
1. **容量守恒**：除源汇外，流入 = 流出。
2. **容量约束**：`0 ≤ f(u,v) ≤ c(u,v)`，反对称 `f(v,u) = -f(u,v)`。
3. **静态容量**：容量不随时间变。
4. **单源单汇**：多源多汇须先归一化（见 ①反面 4）。
5. **容量非负**。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. **把"最大流"当"最短路 / MST"**：三者目标不同，误配会答非所问（凭经验）。
2. **多源多汇不加超级源汇**：直接套会漏解（凭经验）。
3. ★ **拿 MATLAB 内置 `maxflow` 当"独立参照"**：同机同实现，不构成独立验证（任务书 B）。本骨架**自写 Edmonds-Karp**，参照走**手算小图**（**实测**：max flow = 5 = min cut）。
4. ★ **归档里 `corpus/algorithms/src/GraphTheory(图论)/basic/grMaxFlows.m`（grTheory）在 R2025b 上不可用**（`corpus/algorithms/INDEX.md` §10.5 第 1 批登记）——用前须实测，**不拿它当参照**。
5. **残量网络的反对称弧漏建**：无法正确"退流"⇒ 会停在次优流（凭经验）。

## ⑤ 输出模板

- **最大流量** + **最小割容量**（两者相等做校核）+ **各弧流量表** + 可选**网络流图**（标流量/容量）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；网络图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/maxflow_mincut.m`（**零参可跑**，自带手算小网络：5 节点有向、源 1 汇 4，容量 1→2:3 · 1→3:2 · 2→3:1 · 2→4:2 · 3→4:4）。

关键片段（**不整份复制**）：
```matlab
while true
    [parent, ok] = bfs_path(C - F, s, t, n);   % 残量网络 BFS 增广路
    if ~ok; break; end
    % 沿路径取瓶颈、更新残量流量
    ...
    maxflow = maxflow + bottleneck;
end
```
**独立参照**：`tests/skills/model-select/verify/maxflow_mincut.md`（**第 3 类：手算小图** —— 手算最小割 `S={1,2}` 割容量 5 ⇒ max flow = 5 = min cut，与骨架一致）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMaxFlows.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinCutSet.m`（**grTheory**）—— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **带语料指针（薄）**：`corpus/papers/MODEL_MAP.md` 里 `network flow` 带锚 **1 行 / 1 篇**（当场 `grep -nE "^ +- network flow（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ `:214` = P2025-D-03）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行。
- **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMaxFlows.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinCutSet.m`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**：`network` 带锚 **0 行**（真 tag 是整串 `network flow`）。
