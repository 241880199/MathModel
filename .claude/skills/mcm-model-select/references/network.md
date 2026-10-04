# network —— 类索引（**第二跳**：图与网络）

**上位**：`SKILL.md` 的第一跳决策树把「**要处理图 / 网络：路径、流、连通、遍历、匹配**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/network/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面可抽象成**顶点 + 边的图**，要在图上求**路径 / 连通 / 流 / 覆盖 / 遍历 / 中心性**。
**类级反面（什么时候不该用这一类）**：问题不是图结构（无顶点-边关系）⇒ 去别的类；**要连续优化** ⇒ `optimization`。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：要给两（多）点间找路径吗？**
  - **求最短路径** ⇒ **最短路** → `references/network/shortest_path.md`
  - **求经过所有点一次的巡回（旅行商）** ⇒ **旅行商 TSP** → `references/network/tsp.md`
  - **求一笔画遍历所有边（欧拉）/ 哈密顿回路** ⇒ **欧拉图 / Hamilton 图** → `references/network/euler_hamilton.md`
- **问 2：要连接 / 输送吗？**
  - **连接所有点、总代价最小（树）** ⇒ **最小生成树** → `references/network/mst.md`
  - **求最大吞吐量 / 最小割** ⇒ **最大流 / 最小割** → `references/network/maxflow_mincut.md`
  - **在流上还带单位费用、求最小费用** ⇒ **最小费用流** → `references/network/min_cost_flow.md`
  - **工期 / 关键路径（计划评审）** ⇒ **计划评审 PERT** → `references/network/pert.md`
- **问 3：要选顶点 / 边的一个子集满足某种约束吗？**
  - **配对 / 点覆盖 / 边覆盖 / 独立集 / 团 / 支配集** ⇒ **匹配与覆盖** → `references/network/matching.md`
  - **给边或点着色、相邻不同色** ⇒ **染色（边 / 点 / 图）** → `references/network/coloring.md`
- **问 4：要描述结构属性吗？**
  - **层级遍历 / 前缀编码** ⇒ **树 / 遍历 / Huffman** → `references/network/tree_traversal.md`
  - **连通分量 / 中心性度量** ⇒ **连通性 / 中心性** → `references/network/connectivity_centrality.md`

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 最短路 | `shortest_path.m` | `references/network/shortest_path.md` |
| 最小生成树 | `mst.m` | `references/network/mst.md` |
| 最大流 / 最小割 | `maxflow_mincut.m` | `references/network/maxflow_mincut.md` |
| 最小费用流 | `min_cost_flow.m` | `references/network/min_cost_flow.md` |
| 匹配与覆盖 | `matching.m` | `references/network/matching.md` |
| 染色（边 / 点 / 图） | `coloring.m` | `references/network/coloring.md` |
| 树 / 遍历 / Huffman | `tree_traversal.m` | `references/network/tree_traversal.md` |
| 欧拉图 / Hamilton 图 | `euler_hamilton.m` | `references/network/euler_hamilton.md` |
| 连通性 / 中心性 | `connectivity_centrality.m` | `references/network/connectivity_centrality.md` |
| 计划评审 PERT | `pert.m` | `references/network/pert.md` |
| 旅行商 TSP | `tsp.m` | `references/network/tsp.md` |

★ **行数 = 11 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **参照口径**：本类用**手算小图**（5 节点可手算）；**第 2 类（盘上实现）默认不用**，只在必要时取净室重写版。
★ **两条线不许混写**：`grTheory`（`basic/gr*.m`，作者 Sergiy Iglin）与 `detailed/` 下另一作者的中文实现**不是一套**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
