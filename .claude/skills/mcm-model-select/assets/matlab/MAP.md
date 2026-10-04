# `mcm-model-select` 三列映射表（中文名 ↔ ASCII 文件名 ↔ 六格文件路径）

**本表由 Task 0 产出**（基线 `3d02d2c`），**随 skill 入库**。**扫描面 = 66 项**（= 花名册终版 `docs/superpowers/specs/2026-10-04-m4-model-select-roster.md`）。

**约定（设计 §2.1 · GC5）**：**MATLAB 文件名必须合法 ASCII** —— **中文名不能作为 MATLAB 函数被调用** ⇒ 骨架一律 **ASCII 蛇形**。
**列义**：① **中文名**（方法名，给人读）· ② **ASCII 文件名**（`assets/matlab/<类>/<ASCII>.m` 的文件名）· ③ **六格文件路径**（`references/<类>/<ASCII>.md`，相对 `.claude/skills/mcm-model-select/`）。
★ **它是 `MS6` 的前提** —— 没有这张表，"最短路" ↔ `shortest_path.m` 无法机械对齐（设计 §2.1）。

**合计 = 66**（evaluation 5 · prediction 10 · optimization 11 · mechanism 10 · simulation 4 · statistics 7 · network 11 · ml 8）。
**本表不声称穷尽**：它只列花名册终版里的 66 个方法。

---

## evaluation（5）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| AHP 层次分析法 | `ahp.m` | `references/evaluation/ahp.md` |
| 模糊综合评价（多层次） | `multi_level_fuzzy.m` | `references/evaluation/multi_level_fuzzy.md` |
| 模糊综合评价（多目标） | `multi_objective_fuzzy.m` | `references/evaluation/multi_objective_fuzzy.md` |
| TOPSIS | `topsis.m` | `references/evaluation/topsis.md` |
| 熵权法 | `entropy_weight.m` | `references/evaluation/entropy_weight.md` |

## prediction（10）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 灰色预测 GM(1,1) | `gm11.m` | `references/prediction/gm11.md` |
| 灰色 GM(2,1) / Verhulst | `gm21_verhulst.m` | `references/prediction/gm21_verhulst.md` |
| 指数平滑 | `exp_smoothing.m` | `references/prediction/exp_smoothing.md` |
| 移动平均 | `moving_average.m` | `references/prediction/moving_average.md` |
| 趋势外推 | `trend_extrapolation.m` | `references/prediction/trend_extrapolation.md` |
| 自适应滤波 | `adaptive_filtering.m` | `references/prediction/adaptive_filtering.md` |
| 回归预测 | `regression.m` | `references/prediction/regression.md` |
| 神经网络预测 | `nn_forecast.m` | `references/prediction/nn_forecast.md` |
| 插值（数据补全 / 网格化） | `interpolation.m` | `references/prediction/interpolation.md` |
| ARIMA / SARIMA | `arima_forecast.m` | `references/prediction/arima_forecast.md` |

★ **订正（2026-10-04，Task 3 实测）**：ARIMA 的 ASCII 名原定 `arima.m`，**实测不可用** ——
MATLAB 的 `arima` 是**类文件夹里的构造器**（`...\toolbox\econ\econ\@arima\arima.m`），在 R2025b 上
**class-folder 优先于 MATLAB 路径里的同名函数** ⇒ 名为 `arima.m` 的骨架**既不能被按名调用、也不能被 `run` 执行**
（`run('.../arima.m')` ⇒ `未找到`）⇒ 会让 `MS4`（骨架可跑）判出**假绿**。故改名为 `arima_forecast.m`。
（★ **本表 66 个 ASCII 名已逐名实跑**（2026-10-04 复核），**判据 = 顶层类目录撞名**：
`find /d/Software/Matlab/toolbox -type d -name "@<名>" -printf '%h\n'` —— **命中且父目录不以 `+` 开头** ⇒ 真撞名；
父目录以 `+` 开头 ⇒ **包内类目录**、类名带包前缀、**不遮蔽**顶层同名函数、**不算**。
**全量 66 名实测：真顶层 `@<名>` 类目录命中 = 0**；唯一命中是**包内假阳**
`toolbox/matlab/timeseries/+tsdata/@interpolation`（父目录 `+tsdata` ⇒ 类名 `tsdata.interpolation`；
实测 `exist('interpolation') = 0`，**不遮蔽**顶层 `interpolation.m`）。
★ **改名前的原名 `arima` 是唯一的真撞名**（`toolbox/econ/econ/@arima`，父目录 `econ` 非包）—— 故已改名 `arima_forecast.m`。
★ 但 `anova` 等**函数**级撞名不在此列 —— 函数被路径文件遮蔽时是**路径文件胜出**、可正常调用。）

## optimization（11）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 线性规划 | `lp.m` | `references/optimization/lp.md` |
| 整数规划 / 指派问题 | `ilp_assignment.m` | `references/optimization/ilp_assignment.md` |
| 非线性规划 | `nlp.m` | `references/optimization/nlp.md` |
| 目标规划 | `goal_programming.m` | `references/optimization/goal_programming.md` |
| 遗传算法 | `ga.m` | `references/optimization/ga.md` |
| 模拟退火 | `sa.m` | `references/optimization/sa.md` |
| 粒子群 PSO | `pso.m` | `references/optimization/pso.md` |
| 免疫优化 | `immune.m` | `references/optimization/immune.md` |
| 蚁群 ACO | `aco.m` | `references/optimization/aco.md` |
| 人工鱼群 | `afsa.m` | `references/optimization/afsa.md` |
| 遗传算法变体（多种群 / 量子 / 混合） | `ga_variants.m` | `references/optimization/ga_variants.md` |

## mechanism（10）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| ODE 初值问题（Euler / RK4） | `ode_ivp.m` | `references/mechanism/ode_ivp.md` |
| ODE 边值问题（打靶法） | `ode_bvp_shooting.m` | `references/mechanism/ode_bvp_shooting.md` |
| 降阶 / 解析解法 | `reduce_order.m` | `references/mechanism/reduce_order.md` |
| 差分方程（离散动力系统 · 稳定性判据） | `difference_equations.m` | `references/mechanism/difference_equations.md` |
| PDE 数值解（抛物/椭圆/双曲） | `pde_numerical.m` | `references/mechanism/pde_numerical.md` |
| 传染病模型（SIR / SEIR） | `sir_seir.m` | `references/mechanism/sir_seir.md` |
| 生态动力学（Lotka-Volterra） | `lotka_volterra.m` | `references/mechanism/lotka_volterra.md` |
| 输运方程（热传导 / 扩散 / 波动） | `transport.m` | `references/mechanism/transport.md` |
| 反应扩散 | `reaction_diffusion.m` | `references/mechanism/reaction_diffusion.md` |
| 参数辨识 / 稳定性分析 | `param_id_stability.m` | `references/mechanism/param_id_stability.md` |

## simulation（4）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 元胞自动机（9 种规则） | `cellular_automata.m` | `references/simulation/cellular_automata.md` |
| 蒙特卡洛 | `monte_carlo.m` | `references/simulation/monte_carlo.md` |
| 排队论 | `queueing.m` | `references/simulation/queueing.md` |
| ABM（多智能体） | `abm.m` | `references/simulation/abm.md` |

## statistics（7）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 主成分分析 PCA | `pca.m` | `references/statistics/pca.md` |
| 系统聚类（层次聚类） | `hierarchical_cluster.m` | `references/statistics/hierarchical_cluster.md` |
| 变量聚类 | `var_cluster.m` | `references/statistics/var_cluster.md` |
| 灰色关联 / 优势分析（因素排序） | `grey_relational.m` | `references/statistics/grey_relational.md` |
| 假设检验 | `hypothesis_test.m` | `references/statistics/hypothesis_test.md` |
| 方差分析 | `anova.m` | `references/statistics/anova.md` |
| 贝叶斯推断 | `bayesian.m` | `references/statistics/bayesian.md` |

## network（11）

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

## ml（8）

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
