# 树 / 遍历 / Huffman（`tree_traversal.m`）

> **要描述层级结构 / 遍历序 / 前缀编码时用**：树上的 BFS（层序）、DFS（深度序），以及 Huffman 最优前缀编码。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/tree_traversal.m` · 参照 `tests/skills/model-select/verify/tree_traversal.md`。
★ **与相邻方法的边界**：要**最小生成树**（在图上选边）⇒ `references/network/mst.md`；要**连通分量 / 中心性** ⇒ `references/network/connectivity_centrality.md`；要做**分类决策树** ⇒ 那是 ML 方法（`references/ml/`），**不是本类的树遍历**。

## ① 适用判据

- **用**：题面有**天然层级 / 树状依赖**（组织、目录、溯源、决策层级）；要**层序 / 深度序**；要做**变长前缀编码**（压缩 / 频率编码）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. ★ **`decision tree`（决策树）不是本类的树遍历** —— 那是**分类 / 回归模型**（`corpus/papers/MODEL_MAP.md` 里是独立 tag）。
  2. **图不是树（有环）** ⇒ BFS/DFS 仍可跑，但"遍历序"非唯一，须先定根与判据（凭经验）。
  3. **要最小生成树** ⇒ 走 `references/network/mst.md`。
  4. **固定长度编码** ⇒ 不需 Huffman（凭经验）。

## ② 标准建模步骤

1. **建树**：定义根、父子关系（邻接表）。
2. **BFS**：队列层序扩张，得层序遍历与层数。
3. **DFS**：栈 / 递归深度优先，得先序（本骨架升序邻接）。
4. **Huffman**：反复合并**两个最小权**叶，建树，读各叶深度 = 码长，加权路径长 = Σ 权×码长。
5. **数值验证**（见 ⑥）：小树**手算** BFS/DFS 序；Huffman **手算**合并序。
6. **报告**：遍历序 + 层数 / 码长表 + 加权路径长。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 邻接表 `adj`（无向树）· 根 `root` · 频率 `w`（Huffman） |
| **输出** | `bfs` · `dfs`（遍历序）· `lens`（码长）· `wpl`（加权路径长） |

**显式假设（必须写进论文）**：
1. **树结构**：`n` 顶点、`n-1` 边、无环（若含环须先说明）。
2. **根已定**：BFS/DFS 依赖根的选取。
3. **遍历序约定**：本骨架 DFS 按邻接**升序**（序不唯一，须写明约定）。
4. **Huffman 权非负**：频率 / 权重 ≥ 0。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把决策树当树遍历**：同名不同义（凭经验 + 语料实查）。
2. **遍历序不写明邻接顺序**：同一棵树不同输出会被误判"算错"（凭经验）。本骨架显式用升序。
3. **DFS 递归深度爆栈**：大树须改迭代（凭经验）。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/detailed/树/` 下代码未净室重写，不作独立参照。参照走**手算小图**（**实测**：BFS `[1 2 3 4 5 6]` · DFS `[1 2 4 5 3 6]` · Huffman WPL `224`）。
5. **Huffman 合并并列最小权时次序**：会影响具体码字、但**加权路径长唯一**（凭经验）。

## ⑤ 输出模板

- **遍历序**（BFS / DFS）+ **Huffman 码长表**（符号 · 频率 · 码长）+ **加权路径长** + 可选**树 / 编码树图**。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；树图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/tree_traversal.m`（**零参可跑**，自带手算小树：边 1-2,1-3,2-4,2-5,3-6，根 1；Huffman 权 `[5 9 12 13 16 45]`）。

关键片段（**不整份复制**）：
```matlab
% BFS
while ~isempty(q); u = q(1); q(1) = []; bfs(end+1) = u;
    for v = adj{u}; if ~visited(v); visited(v)=true; q(end+1)=v; end; end; end
% Huffman：反复合并两个最小权，读叶深度 = 码长
while numel(activeIdx) > 1
    [~, o] = sort(activeW); a = activeIdx(o(1)); b = activeIdx(o(2));
    ...
end
```
**独立参照**：`tests/skills/model-select/verify/tree_traversal.md`（**第 3 类：手算小图** —— BFS `1 2 3 4 5 6` · DFS `1 2 4 5 3 6` · Huffman 码长 `[4 4 3 3 3 1]` · WPL `224`，与手算逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/detailed/树/BFS.m` · `corpus/algorithms/src/GraphTheory(图论)/detailed/树/DFS.m` · `corpus/algorithms/src/GraphTheory(图论)/detailed/树/Huffman.m` —— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `tree traversal` 与 `Huffman` 带锚 **均 0 行**（当场 `grep -cE "^ +- (tree traversal|Huffman)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。★ **陷阱**：`decision tree` 带锚 **1 行（11 篇）** —— 那是**分类模型**、**不是本类树遍历**，**不并入**（★ **订正**：原写"带锚 11 行"，**把篇数当成了行数**；实测 `grep -nE "^ +- .*decision tree（[0-9]+ 篇）"` ⇒ **1 行**、11 是篇数 —— 同 Task 11 复核 M2）。
- **算法素材面**：见上（`BFS.m` · `DFS.m` · `Huffman.m`）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
