# 欧拉图 / Hamilton 图（`euler_hamilton.m`）

> **要判"能否一笔画走遍所有边"或"能否走遍所有点一次"时用**：欧拉回路（每边恰一次、回到起点）与哈密顿回路（每点恰一次）。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/euler_hamilton.m` · 参照 `tests/skills/model-select/verify/euler_hamilton.md`。
★ **与相邻方法的边界**：要**两点间最短路** ⇒ `references/network/shortest_path.md`；要**经过所有点的最小巡回**（带权、求最优）⇒ `references/network/tsp.md`。

## ① 适用判据

- **用**：题面问**遍历边**（路线巡检、一笔画、邮递员）或**遍历点**（巡回访问、坐席轮转）；要判**存在性**或**求一条回路**。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **要带权最优巡回** ⇒ 那是 **TSP**（`references/network/tsp.md`），欧拉/Hamilton 只判存在与给一条。
  2. **只求两点最短** ⇒ 走 `references/network/shortest_path.md`。
  3. **奇度顶点 > 2** ⇒ 欧拉**回路不存在**（至多 2 个奇度点才有欧拉**路径**）—— 须判存在性，别硬找（凭经验）。
  4. **Hamilton 回路是 NP-hard** ⇒ 大图别指望多项式算法，须回溯 + 剪枝或说明只做小规模（凭经验）。

## ② 标准建模步骤

1. **建图**：顶点、边（无向 / 有向）。
2. **判欧拉**：连通 + **所有顶点度为偶数** ⇒ 欧拉回路存在；恰 2 个奇度 ⇒ 欧拉路径。
3. **求欧拉回路**：**Hierholzer**（走圈、回溯拼接）。
4. **判 / 求 Hamilton**：回溯（DFS）+ 剪枝，小规模可行。
5. **数值验证**（见 ⑥）：小图**手算**存在性 + 回路合法性（每边一次、闭合）。
6. **报告**：存在性结论 + 一条回路 + 合法性校核。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 欧拉图邻接 `AE` · Hamilton 图邻接 `AH` |
| **输出** | `euler`（回路序列）· `hamilton`（回路序列，无则空） |

**显式假设（必须写进论文）**：
1. **无向图**（本骨架）；有向图判据改为入度 = 出度。
2. **连通性**：非连通图谈不上欧拉回路。
3. **简单图**：本骨架用邻接矩阵，多重边须另表示。
4. **Hamilton 只在小规模求存在性**（NP-hard）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★★ **上游 `corpus/algorithms/src/GraphTheory(图论)/detailed/Euler图和Hamilton图/Fleuf1.m` 有确证的算法性缺陷 —— 给出非法欧拉回路**（K5 上重复用边、漏边，且序列首尾不相接）。**实测**（`corpus/algorithms/INDEX.md` §10.1 登记）。**净室重写版**在 `corpus/algorithms/fixed/euler_circuit.m`；本骨架**自写 Hierholzer**，**不拿 `Fleuf1.m` 当参照**。
2. **不判连通性就找欧拉回路**：非连通图会漏掉另一分量（凭经验）。
3. **Hamilton 当多项式问题解**：NP-hard，大图会指数爆炸（凭经验）。
4. **欧拉回路不校核**：须验"每边恰一次 + 首尾相接"（凭经验）。本骨架给出回路后由参照件手算核合法性。
5. **有向图沿用无向判据**：忘改"入度 = 出度"（凭经验）。

## ⑤ 输出模板

- **存在性结论**（欧拉回路 / 路径 / Hamilton 是否存在）+ **一条回路串** + **合法性校核**。
- 文本 / 表 → `mcm-table`（`.claude/skills/mcm-table/`）；路线图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/euler_hamilton.m`（**零参可跑**，自带手算小图：欧拉图边 1-2,2-3,3-1,3-4,4-5,5-3（度全偶）；Hamilton 图 = 5 环 C5）。

关键片段（**不整份复制**）：
```matlab
% Hierholzer
while ~isempty(stack)
    u = stack(end); nbrs = find(A(u, :) > 0);
    if isempty(nbrs); circ(end+1) = u; stack(end) = [];      % 回溯拼接
    else; v = nbrs(1); A(u,v)=A(u,v)-1; A(v,u)=A(v,u)-1; stack(end+1) = v; end
end
```
**独立参照**：`tests/skills/model-select/verify/euler_hamilton.md`（**第 3 类：手算小图** —— 欧拉回路 `1 2 3 4 5 3 1`（每边一次、闭合）· Hamilton `1 2 3 4 5 1`，与手算一致）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/detailed/Euler图和Hamilton图/`（含 **有缺陷的** `Fleuf1.m`）—— 教辅级**起点素材**，**不作独立参照**。★ 该目录的净室重写版 `corpus/algorithms/fixed/euler_circuit.m` 是 11 项里**唯一**对得上的第 2 类参照候选，但本算例**首选手算**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `Euler` 与 `Hamilton` 带锚 **均 0 行**（当场 `grep -cE "^ +- (Euler|Hamilton)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：见上（`Fleuf1.m` 等，**含已登记缺陷**）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
