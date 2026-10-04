# 染色（`coloring.m`）

> **要给"相冲突的对象"分组、使同组内无冲突时用**：给顶点（或边）着色，相邻（冲突）者不同色，求最少色数（频率分配 / 排课 / 时间表 / 寄存器分配）。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/coloring.m` · 参照 `tests/skills/model-select/verify/coloring.md`。
★ **与相邻方法的边界**：要**选点边子集**（匹配 / 覆盖）⇒ `references/network/matching.md`；要**最短路径** ⇒ `references/network/shortest_path.md`。

## ① 适用判据

- **用**：题面是**冲突分组**（同一资源不能同时服务两个冲突对象）；要**最少组数 / 最少色数**；常用近似（贪心）即可给出可施工方案。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **色数（chromatic number）是 NP-hard** ⇒ 别声称"贪心一定得最优"；贪心只给**上界**（凭经验）。
  2. **冲突关系不是两两（成对）的** ⇒ 若是群体约束，图染色表达不了（凭经验）。
  3. **要精确最优且规模大** ⇒ 须 ILP / 精确回溯，贪心只当启发式起点（凭经验）。
  4. **问题其实是匹配 / 覆盖** ⇒ 走 `references/network/matching.md`。

## ② 标准建模步骤

1. **建冲突图**：顶点 = 对象，**边 = 冲突关系**。
2. **选算法**：贪心（**Welsh-Powell**：按度降序着色）给上界；小图可回溯求精确色数。
3. **逐个着色**：取当前顶点**可用最小色**（未被已着色邻居占用）。
4. **计数**：色数 = 用到的最大色号。
5. **数值验证**（见 ⑥）：小图**手算**色数（奇环 χ=3 等）。
6. **报告**：分组表 + 色数 + 是否为最优的说明。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 邻接矩阵 `A`（无向） |
| **输出** | `colors`（每点色号）· `ncolors`（用到的色数） |

**显式假设（必须写进论文）**：
1. **冲突成对**：冲突可表示为两点一条边。
2. **同色可共存**：同色内两两不冲突（即无相邻顶点同色）。
3. **贪心给上界**：须说明"结果是可行方案，未必最优"。
4. **无向图**：着色基于无向冲突关系。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把贪心上界当最优色数**：只有部分图（如奇环、完全图）贪心能达标（**实测**：C5 贪心得 3 = χ(C5)）；一般图须点明"上界"（凭经验）。
2. **着色顺序影响结果**：不同顶点序会得到不同色数（凭经验）；Welsh-Powell 按度降序可改善。
3. **奇环需要 3 色**：C5 不能 2 色（凭经验）；这是"色数 ≥ 3"的典型判据。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/basic/grColEdge.m`（grTheory）等未净室重写，不作独立参照。参照走**手算小图**（**实测**：C5 ⇒ 3 色、`[1 2 1 2 3]`）。
5. **完全图 K_n 需 n 色**：别误以为贪心总能压到少数（凭经验）。

## ⑤ 输出模板

- **分组表**（色号 · 该色顶点）+ **色数** + 可选**冲突图**（按色分组标色）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；冲突图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/coloring.m`（**零参可跑**，自带手算小图：5 环 C5，顶点 1-2-3-4-5-1）。

关键片段（**不整份复制**）：
```matlab
[~, order] = sort(deg, 'descend');          % Welsh-Powell 序
for u = order(:)'
    used = colors(A(u, :) > 0);
    c = 1; while any(used == c); c = c + 1; end
    colors(u) = c;
end
ncolors = max(colors);
```
**独立参照**：`tests/skills/model-select/verify/coloring.md`（**第 3 类：手算小图** —— 手算 χ(C5) = `3`、`colors = [1 2 1 2 3]`，与骨架逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grColEdge.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grColVer.m`（**grTheory**，作者 Sergiy Iglin）· `corpus/algorithms/src/GraphTheory(图论)/detailed/图的染色/`（**另一作者**的中文实现）—— 教辅级**起点素材**，**不作独立参照**。
★★ **两条线不许混写（P2）**：`basic/gr*.m`（`grTheory`，Sergiy Iglin）与 `detailed/` 下另一作者的实现**不是一套**，本文件只把二者**并列标源**，**不合成一个**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `coloring` 与 `graph coloring` 带锚 **均 0 行**（当场 `grep -cE "^ +- (coloring|graph coloring)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：见上（`grColEdge.m` · `grColVer.m`）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
