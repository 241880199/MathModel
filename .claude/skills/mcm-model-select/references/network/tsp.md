# 旅行商 TSP（`tsp.m`）

> **要求"走遍所有点各一次、回到起点、总行程最短"时用**：旅行商问题的精确（小规模穷举）或启发式求解。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/tsp.m` · 参照 `tests/skills/model-select/verify/tsp.md`。
★ **与相邻方法的边界**：只求**两点最短路** ⇒ `references/network/shortest_path.md`；求**一笔画走遍边** ⇒ `references/network/euler_hamilton.md`；大规模走**启发式** ⇒ `references/optimization/aco.md` / `sa.md` / `ga.md`。

## ① 适用判据

- **用**：题面是**巡回路径优化**（配送、巡检、路径规划）；点集规模**小**（如 ≤ 10）时可用**精确穷举**，规模大改用启发式。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **TSP 是 NP-hard** ⇒ 大规模**不能穷举**（`O(n!)` 爆炸），须启发式（`references/optimization/aco.md` 等）（凭经验）。
  2. **不要求"回到起点"** ⇒ 那是哈密顿**路径**问题（`references/network/euler_hamilton.md` 的 Hamilton 支）。
  3. **只求两点最短路** ⇒ 走 `references/network/shortest_path.md`。
  4. **距离非对称 / 有时间窗 / 容量约束** ⇒ 是 TSP 变体（ATSP / VRPTW），标准 TSP 模型不够（凭经验）。

## ② 标准建模步骤

1. **建距离矩阵**：点间代价（距离 / 时间 / 费用）。
2. **选算法**：小 n ⇒ **全排列穷举**（精确最优）；大 n ⇒ 最近邻 + 2-opt / 蚁群 / 退火。
3. **枚举 / 搜索**：穷举时固定起点、枚举其余排列。
4. **取最优**：保留最小总代价巡回。
5. **数值验证**（见 ⑥）：小实例**手算**枚举全部巡回取最优。
6. **报告**：最优巡回 + 总代价 + 规模说明（为何可行 / 为何用启发式）。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 距离矩阵 `D`（对称） |
| **输出** | `best`（最优总代价）· `tour`（巡回序列，回到起点） |

**显式假设（必须写进论文）**：
1. **对称距离**（`D(i,j)=D(j,i)`）；非对称须改算法。
2. **满足三角不等式**（度量 TSP）—— 启发式质量依赖此假设。
3. **小规模可穷举**：本骨架穷举仅适用小 n，规模上限须写明。
4. **每点恰访问一次**且**回到起点**。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★★ **大规模穷举**：`n!` 爆炸（n=12 已 ~4.8×10⁸），必须换启发式（凭经验）。
2. **最优巡回方向对称**：`1-2-4-3-5-1` 与反向等价，报一条即可（**实测**：本算例最优 22，两条对称解）。
3. **最近邻 ≠ 最优**：贪心最近邻可能陷入局部最优（凭经验）。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/basic/grTravSale.m`（grTheory）**在 R2025b 上不可用**（`corpus/algorithms/INDEX.md` §10.5 第 1 批登记）——**不拿它当参照**。参照走**手算小图**（**实测**：最优 `22`）。
5. **距离矩阵不满足三角不等式**：旅行商最优可能"绕远"，且启发式失效（凭经验）。

## ⑤ 输出模板

- **最优巡回串**（如 `1→2→4→3→5→1`）+ **总代价** + 可选**路线图**（按顺序连线）。
- 文本 / 表 → `mcm-table`（`.claude/skills/mcm-table/`）；路线图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/tsp.m`（**零参可跑**，自带手算小实例：5 城市对称距离矩阵；最优巡回总代价 `22`）。

关键片段（**不整份复制**）：
```matlab
P = perms(2:n);                         % 固定起点 1，枚举其余排列
for i = 1:size(P, 1)
    tour = [1 P(i, :) 1]; c = 0;
    for k = 1:n; c = c + D(tour(k), tour(k+1)); end
    if c < best; best = c; bestTour = tour; end
end
```
**独立参照**：`tests/skills/model-select/verify/tsp.md`（**第 3 类：手算小图** —— 手算枚举 12 条不同巡回，最优 `22`；两条对称最优巡回 `1-2-4-3-5-1` 与反向，与骨架一致）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grTravSale.m`（**grTheory**，**R2025b 不可用**）—— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `TSP` / `traveling salesman` / `travelling salesman` 带锚 **均 0 行**（当场 `grep -cE "^ +- (TSP|traveling salesman|travelling salesman)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grTravSale.m`（**R2025b 不可用**）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
