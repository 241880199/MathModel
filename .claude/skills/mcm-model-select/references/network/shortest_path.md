# 最短路（`shortest_path.m`）

> **要在顶点之间找"走哪条路最省"时用**：给定赋权图（距离 / 时间 / 费用 / 通行代价），求两点或多点间累计权重最小的路径。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/shortest_path.m` · 参照 `tests/skills/model-select/verify/shortest_path.md`。
★ **与相邻方法的边界**：要走遍**所有点各一次**（巡回）⇒ `references/network/tsp.md`；要**遍历所有边**（一笔画）⇒ `references/network/euler_hamilton.md`；要**连接所有点、总代价最小**（不一定两点间最短）⇒ `references/network/mst.md`。

## ① 适用判据

- **用**：题面可抽象成**赋权图**，问"最短 / 最快 / 最省"的**点对间路径**（导航、调度、传输路径、应急疏散）；边权**非负**；可要单源（一到多）或全对（多到多）最短路及其长度。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **含负权边** ⇒ Dijkstra **失效**（贪心前提被破坏）⇒ 走 Bellman-Ford / Floyd（凭经验，本骨架只实现 Dijkstra）。
  2. **要求"经过全部点各一次"** ⇒ 那是 **TSP**（`references/network/tsp.md`），最短路解不出巡回。
  3. **问"总代价最小的连边集"** ⇒ 那是**最小生成树**（`references/network/mst.md`），它**不保证**两点间最短路。
  4. **边权表示"容量"而非"代价"** ⇒ 那是**最大流**（`references/network/maxflow_mincut.md`），与最短路不是一回事。

## ② 标准建模步骤

1. **建图**：顶点 = 对象，边 = 可达关系，**边权 = 代价**（距离 / 时间 / 费用），写清**有向还是无向**。
2. **定邻接表示**：邻接矩阵 `W`（`0` = 无边）或边表。
3. **选手算法**：非负权、单源 ⇒ **Dijkstra**；全对 ⇒ **Floyd-Warshall**；含负权 ⇒ Bellman-Ford。
4. **逐点松弛**：维护已定型集合，每次取未定型中当前距离最小者，松弛其出边。
5. **回溯路径**：用前驱数组 `prev` 还原最短路（不只给长度）。
6. **数值验证**（见 ⑥）：小图**手算**逐位核。
7. **报告**：距离向量 + 路径 + 关键节点/边的灵敏度。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 邻接矩阵 `W`（对称 = 无向；`0` = 无边）· 源点 `src` |
| **输出** | `dist`（到各点最短距离）· `prev`（前驱）· `path`（到目标点的路径） |

**显式假设（必须写进论文）**：
1. **非负边权**：Dijkstra 的前提；若题目含负价差 / 负成本，须改算法并写明。
2. **图为静态**：边权不随时间变化（动态网络需另建模型）。
3. **可加性**：路径代价 = 各边代价之和（无可变的换乘惩罚，若有须并入边权）。
4. **连通性**：不连通时不可达点距离为 `inf`，须在报告里点明。
5. **`0` 表示无边**：若存在合法的零权边，此约定会误判（须改用 `inf` 表无边）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **负权边跑 Dijkstra**：结果可能错且不报错（凭经验）。Dijkstra 要求非负权。
2. **`0` 当"无边"与"零权边"混淆**：本骨架用 `0` 表无边（**实测**：算例权重全为正，无歧义）；实战若有权 0 边须改约定。
3. **无向图邻接矩阵不对称**：只填半个矩阵会让部分边"单向化"（凭经验）。
4. ★ **拿 MATLAB 内置 `shortestpath` 当"独立参照"**：那是**同一台机器的同一套实现**，不构成独立验证（任务书 B）。本骨架**自写 Dijkstra**，参照走**手算小图**；若在论文里用内置，须明写"只验证实现"。
5. **只报长度不报路径**：评委常问"怎么走"，须给 `prev` 还原的路径（凭经验）。

## ⑤ 输出模板

- **最短距离表**（节点 · 距离）+ **路径串**（如 `1→3→2→4→5`）+ 可选**最短路径树 / 网络图**。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；网络图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/shortest_path.m`（**零参可跑**，自带手算小图：5 节点无向图，边 1-2:4 · 1-3:2 · 2-3:1 · 2-4:5 · 3-4:8 · 3-5:10 · 4-5:2；源点 1）。

关键片段（**不整份复制**）：
```matlab
dist = inf(1, n); dist(src) = 0; done = false(1, n);
for it = 1:n
    d = dist; d(done) = inf; [~, u] = min(d);
    done(u) = true;
    for v = find(W(u, :) > 0)
        if dist(u) + W(u, v) < dist(v); dist(v) = dist(u) + W(u, v); prev(v) = u; end
    end
end
```
**独立参照**：`tests/skills/model-select/verify/shortest_path.md`（**第 3 类：手算小图** —— `dist = [0 3 2 8 10]`、路径 `1-3-2-4-5` 与手算逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grShortPath.m`（**grTheory**，作者 Sergiy Iglin，Floyd-Warshall）· `corpus/algorithms/src/GraphTheory(图论)/detailed/最短路/Dijkf.m`（**另一作者**的 Dijkstra 中文实现）· 同目录 `Floyd.m` —— 教辅级**起点素材**，**不作独立参照**（未经净室重写）。
★★ **两条线不许混写**：`basic/gr*.m`（`grTheory`，Sergiy Iglin）与 `detailed/` 下另一作者的中文实现**不是一套**，本文件只把二者并列标源，**不合成一个**。

## 语料面（P6）

- **带语料指针**：`corpus/papers/MODEL_MAP.md` 里 `shortest path` 带锚 **2 行**（当场 `grep -nE "^ +- shortest path（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ `:189` = 2025 D 题 **4 篇**（P2025-D-01..D-04）· `:248` = 2025 E 题 **1 篇**（P2025-E-01））。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：见上（`grShortPath.m` / `Dijkf.m` / `Floyd.m`）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**：邻近 tag（`A-star` · `Wardrop` 等）**不并入**本方法。
