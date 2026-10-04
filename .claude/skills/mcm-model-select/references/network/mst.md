# 最小生成树（`mst.m`）

> **要用最小总代价把所有点连成一个连通网时用**：在赋权无向图上选 `n-1` 条边，使全图连通且**总权最小**（布线 / 管网 / 通信骨干）。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/mst.m` · 参照 `tests/skills/model-select/verify/mst.md`。
★ **与相邻方法的边界**：要**两点间最短路径**（不是全连通）⇒ `references/network/shortest_path.md`；要**最大吞吐量**⇒ `references/network/maxflow_mincut.md`。

## ① 适用判据

- **用**：题面要给一组点**铺最小代价的连通网**（电网、光缆、管道、道路骨架）；图**无向、连通、边权非负**；要**最小总权**而非"两点间最短"。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **要求特定两点间路径最短** ⇒ 最小生成树**不保证**（它在树上两点间唯一路径可能很长）⇒ 走 `references/network/shortest_path.md`。
  2. **图有向** ⇒ 应走**最小树形图**（有向 MST / arborescence），无向 MST 不适用（凭经验）。
  3. **图不连通** ⇒ 得到的是**最小生成森林**，须点明。
  4. **目标是"容量 / 吞吐"** ⇒ 那是流问题（`references/network/maxflow_mincut.md`）。

## ② 标准建模步骤

1. **建图**：顶点 = 需连通的点，边权 = 连接代价（建设 / 长度）。
2. **选算法**：**Kruskal**（按权升序 + 并查集避环）或 **Prim**（从一点扩张取最廉边）。
3. **避环合并**：逐条取最廉边，若两端已连通则跳过。
4. **终止**：选满 `n-1` 条边。
5. **数值验证**（见 ⑥）：小图**手算**合并序与总权。
6. **报告**：MST 边集 + 总权 + 可选次小生成树做灵敏度。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 边表 `E`（`[u v w]` 三列）· 顶点数 `n` |
| **输出** | `weight`（MST 总权）· `edges`（选中的边，按加入序） |

**显式假设（必须写进论文）**：
1. **无向连通图**：MST 存在且唯一边数 `n-1`（权并列时可能多解，总权仍唯一）。
2. **边权非负**：负权也可用 Kruskal，但须说明其物理意义。
3. **静态权重**：边权不随时间变。
4. **可加性**：总代价 = 选中边权之和。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. **图不连通不检查**：会静默给出"生成森林"，边数 < `n-1`（凭经验）。
2. **权并列时漏声明多解**：MST **总权唯一、边集可能不唯一**（凭经验）。
3. ★ **拿 MATLAB 内置 `minspantree` 当"独立参照"**：同机同实现，不构成独立验证（任务书 B）。本骨架**自写 Kruskal**，参照走**手算小图**（**实测**：合并序 3-4(1) → 1-2(2) → 2-3(3) → 4-5(5)，总权 11）。
4. **把 MST 当"最短路"**：`references/network/shortest_path.md` 是本方法最常见误配（凭经验）。
5. **顶点编号不连续 / 从 0 起**：并查集越界（凭经验）。

## ⑤ 输出模板

- **MST 边表**（u-v · 权重）+ **总权** + 可选**网络图**（标出选中边）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；网络图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/mst.m`（**零参可跑**，自带手算小图：5 节点 7 边，边 1-2:2 · 2-3:3 · 3-4:1 · 4-5:5 · 1-3:4 · 2-4:6 · 3-5:7）。

关键片段（**不整份复制**）：
```matlab
[~, idx] = sort(E(:, 3)); E = E(idx, :);     % Kruskal：按权升序
for k = 1:size(E, 1)
    a = findroot(parent, E(k, 1)); b = findroot(parent, E(k, 2));
    if a ~= b; parent(a) = b; sel(end+1, :) = E(k, :); end   % 避环合并
end
```
**独立参照**：`tests/skills/model-select/verify/mst.md`（**第 3 类：手算小图** —— MST 总权 `11`、边 {3-4(1), 1-2(2), 2-3(3), 4-5(5)} 与手算合并序逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMinSpanTree.m`（**grTheory**）—— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **带语料指针（薄）**：`corpus/papers/MODEL_MAP.md` 里 `minimum spanning tree` 带锚 **1 行 / 1 篇**（当场 `grep -nE "^ +- minimum spanning tree（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ `:212` = P2025-D-02）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行。
- **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMinSpanTree.m`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**：`spanning tree` 带锚 **0 行**（真 tag 是整串 `minimum spanning tree`）。
