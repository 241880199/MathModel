# 连通性 / 中心性（`connectivity_centrality.m`）

> **要描述网络结构属性时用**：连通分量（网络是否分成几块）、以及中心性度量（哪个节点最重要）—— 度、接近、介数、特征向量中心性。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/connectivity_centrality.m` · 参照 `tests/skills/model-select/verify/connectivity_centrality.md`。
★ **与相邻方法的边界**：要找**路径** ⇒ `references/network/shortest_path.md`；要找**最小连边集** ⇒ `references/network/mst.md`。

## ① 适用判据

- **用**：题面问**网络的整体结构**（连通性、割点、脆弱性）或**节点重要性排序**（关键枢纽、影响力）；节点可代表实体、边代表关系。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. ★ **`neural network` / `Bayesian network` 不是本方法** —— 前者是 ML 模型、后者是概率图模型（`corpus/papers/MODEL_MAP.md` 里是独立 tag）。
  2. **要问两点间最优路径** ⇒ 走 `references/network/shortest_path.md`。
  3. **中心性选择不当** ⇒ 度中心性只见局部、介数中心性昂贵，须按题面语义选（凭经验）。
  4. **有权图用无权度中心性** ⇒ 忽略权重会误判"枢纽"（凭经验）。

## ② 标准建模步骤

1. **建图**：顶点 = 实体，边 = 关系（可带权）。
2. **连通性**：BFS/DFS 求连通分量、割点 / 桥（脆弱性）。
3. **选中心性**：度（局部活跃）· 接近（到全体近）· 介数（在路径上关键）· 特征向量（连到大节点）。
4. **计算**：按定义式逐节点求值、归一化。
5. **数值验证**（见 ⑥）：小图**手算**分量数与度中心性。
6. **报告**：分量表 + 中心性排序 + 关键节点。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 邻接矩阵 `A`（无权；带权须另处理） |
| **输出** | `ncomp`（分量数）· `comp`（分量标签）· `degree` · `degree_centrality` |

**显式假设（必须写进论文）**：
1. **无向图**（本骨架）；有向图的连通性分"强 / 弱"，须分别说。
2. **无权**：本骨架给度中心性（无权）；带权中心性须另行定义。
3. **中心性口径**：度中心性归一化为 `deg/(n-1)`，须写明。
4. **静态网络**：结构不随时间变。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把 `neural network` / `Bayesian network` 归入本方法**：同名不同义（凭经验 + 语料实查）。
2. **中心性不归一化就横比**：不同规模网络不可比（凭经验）。本骨架用 `deg/(n-1)`。
3. **有向图强 / 弱连通混淆**：结论可能相反（凭经验）。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/basic/grComp.m`（grTheory）等未净室重写，不作独立参照。参照走**手算小图**（**实测**：分量数 `2`、度中心性 `[0.5 0.5 0.5 0.25 0.25]`）。
5. **孤立点被漏计**：分量数会少数（凭经验）。本骨架逐点遍历，孤立点自成一分量。

## ⑤ 输出模板

- **分量表**（分量号 · 成员）+ **中心性排序表**（节点 · 中心性值）+ 可选**网络图**（大小按中心性）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；网络图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/connectivity_centrality.m`（**零参可跑**，自带手算小图：5 节点，边 1-2,2-3,1-3,4-5 ⇒ 2 分量）。

关键片段（**不整份复制**）：
```matlab
for u = 1:n
    if comp(u) == 0
        ncomp = ncomp + 1; q = u; comp(u) = ncomp;      % BFS 标分量
        while ~isempty(q); x = q(1); q(1) = [];
            for v = find(A(x,:) > 0); if comp(v)==0; comp(v)=ncomp; q(end+1)=v; end; end; end
    end
end
degcent = sum(A > 0, 2)' / (n - 1);                     % 度中心性
```
**独立参照**：`tests/skills/model-select/verify/connectivity_centrality.md`（**第 3 类：手算小图** —— 手算 2 分量、度中心性 `[0.5 0.5 0.5 0.25 0.25]`，与骨架逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grComp.m`（**grTheory**，作者 Sergiy Iglin）· `corpus/algorithms/src/GraphTheory(图论)/detailed/连通图/`（**另一作者**的中文实现）—— 教辅级**起点素材**，**不作独立参照**。
★★ **两条线不许混写（P2）**：`basic/gr*.m`（`grTheory`，Sergiy Iglin）与 `detailed/` 下另一作者的实现**不是一套**，本文件只把二者**并列标源**，**不合成一个**。

## 语料面（P6）

- **带语料指针**：`corpus/papers/MODEL_MAP.md` 里 `centrality` 带锚 **3 行**（当场 `grep -nE "^ +- centrality（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ `:163`（1 篇 P2025-C-14）· `:190`（3 篇 P2025-D-01/D-03/D-04）· `:240`（1 篇 P2025-E-01））；另有 `network analysis` 带锚 **2 行**（`:213` P2025-D-02 · `:280` P2025-F-02）。
  ★ **正对照**：同形态 `genetic algorithm` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grComp.m`（**grTheory**）· `corpus/algorithms/src/GraphTheory(图论)/detailed/连通图/`（**另一作者**）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**：`neural network`（8 篇）· `Bayesian network`（1 篇）**均不并入**（不同方法）。
