# 系统聚类 / 层次聚类（`hierarchical_cluster.m`）

> **要把样本分群、且想看层次结构时用**：自底向上逐层合并最相似的两群，得到一棵**树状图**；割树的高度决定群数，不必预设 `k`。

**归属**：类索引 `references/statistics.md` · 骨架 `assets/matlab/statistics/hierarchical_cluster.m` · 参照 `tests/skills/model-select/verify/hierarchical_cluster.md`。
★ **与相邻方法的边界（★ 类索引去重口径）**：**本方法是「聚类」在 statistics 的正条目**；`references/ml/clustering.md` 讲 **K-means / 模糊 C-means**（要**预设 `k`、迭代重心**）。
★ **另一条边界**：本方法聚的是**样本**（Q 型聚类，输入 n×p 数据）；`references/statistics/var_cluster.md` 聚的是**变量**（R 型聚类，输入相关阵）。

## ① 适用判据

- **用**：要**把样本分成若干群**、且**不预设群数**；要看**层次 / 嵌套结构**（树状图）；样本量中小、距离度量明确。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **样本量很大**（上万）⇒ O(n²) 距离矩阵内存/时间爆炸，改 K-means / 先抽稀（凭经验）。
  2. **已知该分几群、只要快** ⇒ 走 `ml/clustering` 的 K-means（层次聚类不必预设 `k`，但代价高）。
  3. **要聚的是变量**（看指标间相关结构）⇒ 走 `var_cluster`（R 型）。
  4. **距离度量 / 链接方式乱选** ⇒ 结果大不同（本骨架实测：`single`/`complete`/`average` 的**组内**合并距离不同，见 ⑥）。
  5. **非凸、环状簇** ⇒ 基于距离的层次聚类切成凸块，效果差（凭经验）。

## ② 标准建模步骤

1. **建相似 / 距离矩阵**：对样本选度量（欧氏 / 曼哈顿 / 相关系数…）；★ 变量先标准化。
2. **选链接方式**：`single`（最近邻 · 易"链式"）/ `complete`（最远邻 · 紧致）/ `average`（UPGMA · 折中）—— ★ **显式声明**。
3. **自底向上合并**：每次并最近的两群，得到树 `Z`（每行 = 一次合并：被并两群 + 距离）。
4. **定群数 / 割树**：按树高（或业务）割成 `k` 群 ⇒ `cluster(Z,k)`。
5. **核拓扑**：检查**合并次序 / 树状图拓扑**是否合理（本骨架对**已知分组**核割树还原、对**4 点直线**核合并距离）。
6. **报告**：树状图 + 群成员表 + 各群特征。
7. **数值验证**（★ 见 ⑥）：对**已知簇结构**的合成数据核割树还原。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 样本矩阵 `X`（n×p）· 距离度量 · **链接方式** · 割树高度 / 群数 `k` |
| **输出** | 树 `Z`（合并记录）· 树状图 · 群标签 |

**显式假设（必须写进论文）**：
1. **距离能代表"相似"**：选错度量则分群无意义。
2. **链接方式**：`single`/`complete`/`average` **会改变结果**，须写清并说明选择理由。
3. **变量已标准化**（量纲不同时），否则量纲大的变量主导距离。
4. **样本独立同分布**（同一样本不重复计）。
5. **割树高度是外生选择**：群数由人定或按树高定，不是模型自动给。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **链接方式不写明**：同一数据 `single`/`complete`/`average` 结果不同。**实测**（本骨架，6 点 2 群）：三者**顶层分组一致**（都 `6/6` 还原），但**组内合并距离不同** —— `single` 全 `1`、`complete` `1.414`、`average` `1.207`；见 `verify/hierarchical_cluster.md`。
2. ★ **拿 MATLAB 内置当"独立参照"**：`linkage`/`cluster` 同为内置、**不独立**（任务书 B）—— 本骨架参照是**已知分组 + 手算合并次序**。
3. `single` 链接的**链式效应**：容易把"桥"连成一大簇（凭经验）。
4. **不标准化**：量纲大的变量主导欧氏距离（凭经验）。
5. **树状图过度解读**：割树高度是主观选择，群数不同结论可能不同（凭经验）。

## ⑤ 输出模板

- **树状图**（横轴样本、纵轴合并距离）+ **割树后的群成员表** + 各群中心 / 特征表。
- 树状图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；群成员表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/statistics/hierarchical_cluster.m`（**零参可跑**，自带算例：6 点 2 群 · 三种链接 · 4 点直线手算核对）。

关键片段（**不整份复制**）：
```matlab
Z = linkage(X, method);       % method ∈ {single, complete, average} —— ★ 显式
lab = cluster(Z, 2);          % 割树成 2 群
% 簇标签可置换 ⇒ 还原率取两种标号的较大者
a = max(mean(lab == truth), mean(lab == (3 - truth)));
```
★ **撞名提醒**：本名字**无**顶层 `@hierarchical_cluster` 类目录撞名；`linkage`/`cluster` 是**内置函数**（路径文件不同名，无遮蔽问题）。
**独立参照**：`tests/skills/model-select/verify/hierarchical_cluster.md`（**第 3/4 类：已知簇结构的合成数据 + 4 点直线手算合并次序 `[1 2 4]`**）。
★ **起点素材**：`corpus/algorithms/src/MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/system_cluster.m` —— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **带语料指针（薄 · 口径见下）**：`corpus/papers/MODEL_MAP.md` 里 `hierarchical cluster` 带锚 **0 行**（tag 不存在）；
  **泛指词** `cluster analysis` 带锚 **4 行 / 11 篇**（`:82` 1 · `:119` 6 · `:203` 1 · `:260` 3）。
  ★★ **`cluster analysis` 是泛指、归属存疑**：它**同时覆盖**层次聚类与 K-means（`MODEL_MAP.md` **另立** `K-means` tag：带锚 2 行 / 4 篇、与本 tag **有重叠**）。
  ⇒ **本方法专属语料指针 = 无**；引用时**只许说"泛指词 11 篇、归属存疑"**，**不许说"层次聚类有 11 篇语料"**。
- **算法素材面（有）**：`corpus/algorithms/src/MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/system_cluster.m` · `corpus/algorithms/src/MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/var_cluster.m` · `corpus/algorithms/src/MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/main.m`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**："层次聚类还有哪些写法"不声称覆盖（`hierarchical clustering` / `dendrogram` 带锚均 0 行）。
