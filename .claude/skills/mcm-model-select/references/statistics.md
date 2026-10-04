# statistics —— 类索引（**第二跳**：统计与推断）

**上位**：`SKILL.md` 的第一跳决策树把「**要检验 / 推断 / 降维 / 聚类 / 因素分析**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/statistics/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面要**从样本对总体下判断**（检验 / 估计 / 区间）或**对多变量做结构简化 / 分组 / 排序**。
**类级反面（什么时候不该用这一类）**：**只求外推未来值** ⇒ `prediction`；**要学出分类/判别函数** ⇒ `ml`；**有机理方程** ⇒ `mechanism`。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：要"对总体下判断"还是"给数据降结构"？**
  - **要检验一个 / 多个假设（显著性、拟合优度、非参数）** ⇒ **假设检验** → `references/statistics/hypothesis_test.md`
  - **要比较三个以上组的均值是否有差异** ⇒ **方差分析** → `references/statistics/anova.md`
  - **有先验、要用数据更新为后验 / 可信区间** ⇒ **贝叶斯推断** → `references/statistics/bayesian.md`
  - **要压缩维度、看主要变异方向** ⇒ **主成分分析 PCA** → `references/statistics/pca.md`
  - **要把样本分群（层次结构 / 树状图）** ⇒ **系统聚类（层次聚类）** → `references/statistics/hierarchical_cluster.md`
  - **要把变量分群（变量间相关结构）** ⇒ **变量聚类** → `references/statistics/var_cluster.md`
  - **要排"哪个因素影响大"（小样本、灰信息）** ⇒ **灰色关联 / 优势分析（因素排序）** → `references/statistics/grey_relational.md`

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 主成分分析 PCA | `pca.m` | `references/statistics/pca.md` |
| 系统聚类（层次聚类） | `hierarchical_cluster.m` | `references/statistics/hierarchical_cluster.md` |
| 变量聚类 | `var_cluster.m` | `references/statistics/var_cluster.md` |
| 灰色关联 / 优势分析（因素排序） | `grey_relational.m` | `references/statistics/grey_relational.md` |
| 假设检验 | `hypothesis_test.m` | `references/statistics/hypothesis_test.md` |
| 方差分析 | `anova.m` | `references/statistics/anova.md` |
| 贝叶斯推断 | `bayesian.m` | `references/statistics/bayesian.md` |

★ **行数 = 7 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **去重口径**：**层次聚类**的正条目在本类（`hierarchical_cluster`）；`ml` 的「聚类」行**不再列层次**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
