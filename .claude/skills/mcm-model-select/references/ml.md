# ml —— 类索引（**第二跳**：机器学习）

**上位**：`SKILL.md` 的第一跳决策树把「**要从数据学出分类 / 回归 / 降维 / 判别关系**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/ml/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面有**特征矩阵**，要**从数据学出一个映射 / 结构**（分类、判别、无监督分组、潜在因子、降维可视化）。
**类级反面（什么时候不该用这一类）**：数据是**序列 / 时空型**、要外推未来 ⇒ `prediction`；**样本极少**、要保守推断 ⇒ `statistics`；**有机理** ⇒ `mechanism`。
★ **低使用度提示**：`dim_reduction` 属**低使用度**（见 `SKILL.md` 的口径与不做表）—— 照补是为**覆盖面**，**不许写成"常用"**。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：有标签吗（监督）？**
  - **有，且是分类问题** ⇒
    - **快速前馈、单隐层、训练快** ⇒ **极限学习机 ELM** → `references/ml/elm.md`
    - **要神经网络的强非线性（BP / LVQ / PNN）** ⇒ **神经网络分类** → `references/ml/nn_classify.md`
    - **要最大间隔 / 核方法** ⇒ **SVM 分类** → `references/ml/svm_classify.md`
  - **有，且因变量是连续值（回归）** ⇒ **SVM 回归** → `references/ml/svm_regress.md`
  - **有，且要给已知类别做判别 / 归类规则** ⇒ **判别分析** → `references/ml/discriminant.md`
- **问 2：无标签（无监督）？**
  - **要分成若干簇** ⇒ **聚类（K-means / 模糊 C-means）** → `references/ml/clustering.md`
  - **要压缩到低维、便于可视化（t-SNE / UMAP）** ⇒ **降维：t-SNE / UMAP** → `references/ml/dim_reduction.md`
  - **要找观测变量背后的潜在因子** ⇒ **因子分析** → `references/ml/factor_analysis.md`

★ **参照口径**：本类用**合成数据**（已知类别 / 已知因子载荷 / 已知簇结构 + 邻域保持率）；`dim_reduction` 属**人工兜底**，**不许写成"已验证"**。
★ **与 `prediction` 的边界**：本类的**神经网络分类**管「**类别判别**」；`prediction` 的**神经网络预测**管「**序列预测**」—— 边界在各方法文件里写明。
★ **去重口径**：**层次聚类**不列本类（正条目在 `statistics` 的 `hierarchical_cluster`）；本类「聚类」行 = **K-means / 模糊 C-means**。

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 神经网络分类（BP / LVQ / PNN） | `nn_classify.m` | `references/ml/nn_classify.md` |
| SVM 分类 | `svm_classify.m` | `references/ml/svm_classify.md` |
| SVM 回归 | `svm_regress.m` | `references/ml/svm_regress.md` |
| 极限学习机 ELM | `elm.m` | `references/ml/elm.md` |
| 聚类（K-means / 模糊 C-means） | `clustering.m` | `references/ml/clustering.md` |
| 降维：t-SNE / UMAP | `dim_reduction.m` | `references/ml/dim_reduction.md` |
| 因子分析 | `factor_analysis.m` | `references/ml/factor_analysis.md` |
| 判别分析 | `discriminant.m` | `references/ml/discriminant.md` |

★ **行数 = 8 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
