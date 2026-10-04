# `mcm-model-select`（M4）方法**花名册终版**（Task 0 审定，2026-10-04）

**上位**：`docs/superpowers/specs/2026-10-04-m4-model-select-design.md`（§11 首版花名册是本次要审的对象）·
`docs/superpowers/plans/2026-10-04-m4-model-select.md`（**Global Constraints 19 条**与**质检记录 P1–P7** 全部适用）。
**本件由 `mcm-model-select` Task 0 产出**（基线 commit `3d02d2c`）。**本件取代设计 §11 的"首版"** ——
§11 是**首版**（"**不许当既成事实**"），本件是**逐件核过**的终版。

**路径写法（GC4）**：本件**盘上素材一律写全路径**（`corpus/algorithms/src/…`），**不再用 `src/…` 简写**
（§11 的 `src/…` 是"给人读的范围定义"，不是"给判据核的指针"）。

**总计数 = 66**（`盘` **48** + `补` **18**）。**标记**：`盘` = 盘上已有素材（给全路径）· `补` = 本模块前置批次要补。

---

## 0. 计数算式（**自核；每个类任务开工前先核自己那一行**）

**逐类之和**（设计 §11.9 的算式，本任务逐件核过后**确认成立**）：

| 类 | 总数 | `盘`（＝**新做**） | `补`（＝**引用**，前置批次已做） |
| :--- | ---: | ---: | ---: |
| evaluation | 5 | 3 | 2 |
| prediction | 10 | 9 | 1 |
| optimization | 11 | 11 | 0 |
| mechanism | 10 | 3 | 7 |
| simulation | 4 | 2 | 2 |
| statistics | 7 | 4 | 3 |
| network | 11 | 11 | 0 |
| ml | 8 | 5 | 3 |
| **合计** | **66** | **48** | **18** |

- **新做合计 = 3+9+11+3+2+4+11+5 = 48**（应 == 本花名册的 `盘` 48）✓
- **引用合计 = 2+1+0+7+2+3+0+3 = 18**（应 == 本花名册的 `补` 18）✓
- **48 + 18 = 66** ✓

★ **两个词的定义（照计划 Task 0 硬要求 8）**：**"新做" = 本类的 `盘` 项数**（归档有素材、但我们还没有自己的骨架）·
**"引用" = 本类的 `补` 项数**（骨架已在 T1–T3 做过）。
⇒ **`新做 + 引用 = 本类总数`**（**不是"引用 = 18 − 新做"** —— T5 新做 3 ⇒ 引用 **2**，而 18−3 = 15 ✗）。

---

## 1. 逐件核定结论（**设计 §11 的 66 项，逐件核过**）

**方法**：`盘` 的**核路径存在**（`test -e` / `ls`）；`补` 的**核真的缺**（**词边界 `grep -w`**）。
★ **词边界用 `grep -rwi`（大小写不敏感 + 词边界）**，并**逐条读命中行**——因为 `-w` **挡不住大小写与词形**：
- `SIR` ⇒ 唯一命中 `corpus/algorithms/src/《MATLAB图像处理》源文件/本书源文件/chap2/chap2_07.m` 的 `'good morning, Sir.'`（**非实质**）；
- `partial differential` ⇒ 唯一命中 `corpus/algorithms/src/README.md`（**正是 §4 要订正的那句自述**，非实现）；
- `agent` ⇒ 命中 `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH08/arrow.m`（该行是 `magenta arrows`，**`magenta` 含子串 `agent`**）；
- `heat` ⇒ 会命中 `heatmap`（本归档无，`MODEL_MAP.md` 有），故一律写全 `heat equation`。

**`补` 的 18 项逐条实测（扫描面 = `corpus/algorithms/src/` 全树，`grep -rwi`）**：

| 项 | 检索式（`grep -rwi`） | 命中 | 结论 |
| :--- | :--- | ---: | :--- |
| TOPSIS | `TOPSIS` | 0 | 确缺 |
| 熵权法 | `entropy_weight` · `entropy weight` · `熵权` | 0 | 确缺 |
| ARIMA/SARIMA | `ARIMA` · `SARIMA` | 0 | 确缺 |
| 差分方程 | `difference equation` · `差分方程` | 0 | 确缺（★ **但见 §4 反向扫的 `CH15/rsolve.m`**） |
| PDE 数值解 | `PDE` · `finite difference` · `偏微分` | 0（`partial differential` 仅 `README.md` 一句自述） | 确缺 |
| SIR/SEIR | `SIR` · `SEIR` | 0（`SIR` 唯一命中是 `'good morning, Sir.'`） | 确缺 |
| Lotka-Volterra | `Lotka` | 0 | 确缺 |
| 输运（热传导/波动） | `heat equation` · `wave equation` · `热传导` · `波动方程` | 0 | 确缺 |
| 反应扩散 | `reaction diffusion` · `reaction-diffusion` · `反应扩散` | 0 | 确缺 |
| 参数辨识/稳定性 | `parameter identification` · `identifiability` · `参数辨识` · `稳定性分析` | 0 | 确缺 |
| 排队论 | `queueing` · `排队论` | 0 | 确缺 |
| ABM | `agent-based` · `ABM` | 0 | 确缺 |
| 假设检验 | `hypothesis test` · `假设检验` | 0 | 确缺 |
| 方差分析 | `ANOVA` · `方差分析` | 0 | 确缺 |
| 贝叶斯 | `bayesian` · `Bayesian` · `贝叶斯` | 0 | 确缺 |
| 降维（t-SNE/UMAP） | `t-SNE` · `UMAP` | 0 | 确缺 |
| 因子分析 | `factor analysis` · `因子分析` | 0 | 确缺 |
| 判别分析 | `discriminant` · `判别分析` | 0 | 确缺 |

★ **本表不声称穷尽检索式**（只列我逐条实跑过的那些）；**"我没找到" ≠ "它不存在"**（扫描面 = `corpus/algorithms/src/`，不含 `corpus/papers/`）。

**`盘` 的 48 项**：**逐件核路径存在**，**全部成立**（见下面第 2、3 节的逐类清单）。

---

## 2. 花名册终版（66 项，**全路径**）

### 2.1 evaluation（5）—— `盘` 3 · `补` 2

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | AHP 层次分析法 | `ahp.m` | `盘` `corpus/algorithms/src/AHP层次分析法/{ahp.m,sglsortexamine.m,tolsortvec.m}` |
| 2 | 模糊综合评价（多层次） | `multi_level_fuzzy.m` | `盘` `corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/多层次模糊综合评价/` |
| 3 | 模糊综合评价（多目标） | `multi_objective_fuzzy.m` | `盘` `corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/多目标模糊综合评价/` |
| 4 | TOPSIS | `topsis.m` | `补` |
| 5 | 熵权法 | `entropy_weight.m` | `补` |

★ **订正（沿用 §11.1）**：**模糊聚类**不属 evaluation ⇒ 归 ml 的"聚类"（见 2.8 #5）。

### 2.2 prediction（10）—— `盘` 9 · `补` 1

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 灰色预测 GM(1,1) | `gm11.m` | `盘` `corpus/algorithms/src/GreySystem灰色系统/{GM_1_1.m,GM_1_1_full_procession.m}` |
| 2 | 灰色 GM(2,1) / Verhulst | `gm21_verhulst.m` | `盘` `corpus/algorithms/src/GreySystem灰色系统/{GM_2_1.m,GM_Verhulst.m}` |
| 3 | 指数平滑 | `exp_smoothing.m` | `盘` `corpus/algorithms/src/TimeSeries时间序列函数/指数平滑法/` |
| 4 | 移动平均 | `moving_average.m` | `盘` `corpus/algorithms/src/TimeSeries时间序列函数/移动平均法/` |
| 5 | 趋势外推 | `trend_extrapolation.m` | `盘` `corpus/algorithms/src/TimeSeries时间序列函数/趋势外推预测法/` |
| 6 | 自适应滤波 | `adaptive_filtering.m` | `盘` `corpus/algorithms/src/TimeSeries时间序列函数/自适应滤波法/` |
| 7 | 回归预测 | `regression.m` | `盘` `corpus/algorithms/src/RegressionAnalysis回归分析/`（6 件） |
| 8 | 神经网络预测 | `nn_forecast.m` | `盘` `corpus/algorithms/src/HeuristicAlgorithm（补分启发式算法，包括神经网络、模拟退火、遗传算法）/神经网络算法/` + 二级层两本书（见 §3.3） |
| 9 | 插值（数据补全 / 网格化） | `interpolation.m` | `盘` `corpus/algorithms/src/Interpolation（目标规划、多元分析与插值的相关例子）/{interp_1D.m,interp_2D.m,interp_2D_compare.m,interp_grid.m}` |
| 10 | ARIMA / SARIMA | `arima_forecast.m` | `补` ★ **订正（2026-10-04 Task 3 实测）**：ASCII 名原定 `arima.m`，因 MATLAB 的 `arima` 是**类构造器**（class-folder 优先于同名路径函数）⇒ `arima.m` 不可调用、不可 `run` ⇒ 改名 `arima_forecast.m`（详见 `MAP.md` 该表下的订正注） |

### 2.3 optimization（11）—— `盘` 11 · `补` 0

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 线性规划 | `lp.m` | `盘` `corpus/algorithms/src/LinearProgramming（添加了线性规划、整数规划等内容的使用案例）/` |
| 2 | 整数规划 / 指派问题 | `ilp_assignment.m` | `盘` `corpus/algorithms/src/IntegerProgramming（线性规划、整数规划等内容的使用案例）/assgin_integer_prog.m` |
| 3 | 非线性规划 | `nlp.m` | `盘` `corpus/algorithms/src/NonLinearProgramming非线性规划/` |
| 4 | 目标规划 | `goal_programming.m` | `盘` `corpus/algorithms/src/GoalProgramming(目标规划、多元分析与插值的相关例子)/` |
| 5 | 遗传算法 | `ga.m` | `盘` `corpus/algorithms/src/HeuristicAlgorithm（补分启发式算法，包括神经网络、模拟退火、遗传算法）/遗传算法/` + `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter{1,2,4,6,9,11}…` |
| 6 | 模拟退火 | `sa.m` | `盘` `corpus/algorithms/src/HeuristicAlgorithm（…）/模拟退火算法/` + `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter{19,21}…` |
| 7 | 粒子群 PSO | `pso.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter{10,13,14,15,16,17}…` |
| 8 | 免疫优化 | `immune.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter12…` |
| 9 | 蚁群 ACO | `aco.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter{22,23,24}…`（TSP / 二维路径 / 三维路径） |
| 10 | 人工鱼群 | `afsa.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter18…`（函数寻优） |
| 11 | 遗传算法变体（多种群 / 量子 / 混合） | `ga_variants.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter{7,8}…` |

### 2.4 mechanism（10）—— `盘` 3 · `补` 7

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | ODE 初值问题（Euler / RK4） | `ode_ivp.m` | `盘` `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/{Explicit_Euler.m,Classical_RK4.m,Classical_RK4s.m}` |
| 2 | ODE 边值问题（打靶法） | `ode_bvp_shooting.m` | `盘` `…/CH14/{lineshoot.m,nlshoot.m}` |
| 3 | 降阶 / 解析解法 | `reduce_order.m` | `盘` `…/CH14/{ReduceDE1.m,SeparableVarsDE.m,HomogenDE.m}` |
| 4 | 差分方程（离散动力系统 · 稳定性判据） | `difference_equations.m` | `补` ★ **起点素材：`corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH15/rsolve.m`（z 变换解线性定常离散系统）—— 见 §4** |
| 5 | PDE 数值解（抛物/椭圆/双曲；有限差分/有限元；刚性） | `pde_numerical.m` | `补`（MATLAB `pdepe`/`ode15s` 内置） |
| 6 | 传染病模型（SIR / SEIR） | `sir_seir.m` | `补` |
| 7 | 生态动力学（Lotka-Volterra） | `lotka_volterra.m` | `补` |
| 8 | 输运方程（热传导 / 扩散 / 波动） | `transport.m` | `补` |
| 9 | 反应扩散 | `reaction_diffusion.m` | `补` |
| 10 | 参数辨识 / 稳定性分析 | `param_id_stability.m` | `补` |

### 2.5 simulation（4）—— `盘` 2 · `补` 2

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 元胞自动机（9 种规则） | `cellular_automata.m` | `盘` `corpus/algorithms/src/CellularAutomata元胞向量机/`（11 件） |
| 2 | 蒙特卡洛 | `monte_carlo.m` | `盘` `corpus/algorithms/src/IntegerProgramming（线性规划、整数规划等内容的使用案例）/monte_carro.m` |
| 3 | 排队论 | `queueing.m` | `补` ★ **低使用度，见 §5 口径** |
| 4 | ABM（多智能体） | `abm.m` | `补` ★ **参照口径有缺口（设计 §4.1）· 低使用度** |

### 2.6 statistics（7）—— `盘` 4 · `补` 3

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 主成分分析 PCA | `pca.m` | `盘` `corpus/algorithms/src/MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/主成分分析/` |
| 2 | 系统聚类（层次聚类） | `hierarchical_cluster.m` | `盘` `corpus/algorithms/src/MultivariateAnalysis（…）/聚类分析/{system_cluster.m,main.m}` |
| 3 | 变量聚类 | `var_cluster.m` | `盘` `corpus/algorithms/src/MultivariateAnalysis（…）/聚类分析/var_cluster.m` |
| 4 | 灰色关联 / 优势分析（因素排序） | `grey_relational.m` | `盘` `corpus/algorithms/src/GreySystem灰色系统/{association_analysis.m,strength_analysis.m}` |
| 5 | 假设检验 | `hypothesis_test.m` | `补` |
| 6 | 方差分析 | `anova.m` | `补` |
| 7 | 贝叶斯推断 | `bayesian.m` | `补` ★ **语料里数得出的最高频缺口（`Bayesian` 14 篇）** |

### 2.7 network（11）—— `盘` 11 · `补` 0

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/GraphTheory(图论)/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 最短路 | `shortest_path.m` | `basic/grShortPath.m`（**`grTheory`，Floyd-Warshall**）· `detailed/最短路/{Dijkf.m,Floyd.m}` · `dijkstra求解最短路径/dijkstra.cpp` · `floyd求解最短路径/floyd.cpp` |
| 2 | 最小生成树 | `mst.m` | `basic/grMinSpanTree.m` |
| 3 | 最大流 / 最小割 | `maxflow_mincut.m` | `basic/{grMaxFlows.m,grMinCutSet.m}` + ★ **反向扫补入** `detailed/网络流/{fofuf.m,boundnetf.m,restrf.m}`（见 §4） |
| 4 | 最小费用流 | `min_cost_flow.m` | `detailed/最小费用流/BGf.m`（★ **`INDEX.md` §10.1 登记的算法性缺陷：不终止**） |
| 5 | 匹配与覆盖 | `matching.m` | `basic/{grMaxMatch.m,grMinVerCover.m,grMinEdgeCover.m,grMaxStabSet.m,grMaxComSu.m,grMinAbsVerSet.m}` + `detailed/匹配问题/`（★ **反向扫补入，见 §4**） |
| 6 | 染色（边 / 点 / 图） | `coloring.m` | `basic/{grColEdge.m,grColVer.m}` + `detailed/图的染色/` |
| 7 | 树 / 遍历 / Huffman | `tree_traversal.m` | `detailed/树/{BFS.m,DFS.m,Huffman.m}` |
| 8 | 欧拉图 / Hamilton 图 | `euler_hamilton.m` | `detailed/Euler图和Hamilton图/` |
| 9 | 连通性 / 中心性 | `connectivity_centrality.m` | `basic/grComp.m` + `detailed/连通图/` |
| 10 | 计划评审 PERT | `pert.m` | `basic/grPERT.m` |
| 11 | 旅行商 TSP | `tsp.m` | `basic/grTravSale.m`（另 GA/SA/PSO/ACO 各有一版，见 §2.3） |

★ **订正（沿用 §11.7）**：`grTheory` 是 `basic/` 下的 `gr*.m`（作者 **Sergiy Iglin**）；`Dijkf.m`/`Floyd.m` 在 `detailed/最短路/`，**是另一个作者的中文实现**。**两条线不是同一套**（P2）。

### 2.8 ml（8）—— `盘` 5 · `补` 3

| # | 方法（中文） | ASCII | 证据（`corpus/algorithms/src/…`） |
| ---: | :--- | :--- | :--- |
| 1 | 神经网络分类（BP / LVQ / PNN） | `nn_classify.m` | `盘` `corpus/algorithms/src/NeuralNetwork神经网络工具箱的调用案例/` + `corpus/algorithms/src/HeuristicAlgorithm（…）/神经网络算法/` + 二级层两本书（见 §3.3） |
| 2 | SVM 分类 | `svm_classify.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter28…` + `corpus/algorithms/src/HeuristicAlgorithm（…）/神经网络算法/MATLAB神经网络30个案例分析/案例{12,13}…` |
| 3 | SVM 回归 | `svm_regress.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter29…` + `…/案例{14,15}…` |
| 4 | 极限学习机 ELM | `elm.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter30…`（`elmtrain.m` · `elmpredict.m`） |
| 5 | 聚类（K-means / 模糊 C-means） | `clustering.m` | `盘` `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter20…`（FCM） + `corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/模糊聚类/`（★ **去重裁定见 §6① ② ③**） |
| 6 | 降维：t-SNE / UMAP | `dim_reduction.m` | `补` ★ **参照口径有缺口（设计 §4.1）· 低使用度**（MATLAB 有 `tsne`；UMAP 无内置） |
| 7 | 因子分析 | `factor_analysis.m` | `补`（MATLAB `factoran` 内置） |
| 8 | 判别分析 | `discriminant.m` | `补`（MATLAB `classify` 内置） |

★ **订正（沿用 §11.8）**：**"神经网络"**在 prediction（#8 神经网络预测）与 ml（#1 神经网络分类）**各一次** ⇒ **两条的边界在各自方法文件里写明**（预测侧管"序列预测"、ml 侧管"类别判别"）。

---

## 3. 命名约定（GC5）与三列映射表

### 3.1 ★★ MATLAB 文件名一律合法 ASCII（GC5）

**中文名不能作为 MATLAB 函数被调用** ⇒ 骨架一律 **ASCII 蛇形**（`shortest_path.m` · `topsis.m` · `sir_seir.m`）。
**本件第 2 节每行都给了 ASCII 名**；**核过：66 个 ASCII 名全为 `[a-z0-9_]+\.m`，无中文、无空格、无大写**。
**中文名 ↔ ASCII 名 ↔ 六格文件路径**的**三列映射表**见 `.claude/skills/mcm-model-select/assets/matlab/MAP.md`（本次产出）。

### 3.2 六格文件路径

`references/<类>/<方法>.md`（相对 `.claude/skills/mcm-model-select/`）。**一方法一文件**（设计 §2）。
`MAP.md` 的第三列写的就是这个相对路径 —— **它是 `MS6`（类索引清单 ↔ 实际方法文件，双向一致）的前提**。

### 3.3 二级层"两本书"的确切路径（供 prediction #8 · ml #1 引用）

- `corpus/algorithms/src/《MATLAB 神经网络30个案例分析》源程序 数据/`（29 个 `chapter*/`）
- `corpus/algorithms/src/《MATLAB神经网络原理与实例精解》随书附带源程序/`（`第2/4–11/13章 …`）

---

## 4. ★ 反向扫（**不声称穷尽**；候选**逐条给去向**）

**扫描面**：`corpus/algorithms/src/` 的**全部 20 个顶层目录** —— **一级 15 个作者目录 + 二级 3 个 + 三级 2 个**（见 §7 口径）。
★ **本节的"扫过"不声称穷尽**：我按**目录结构 + 文件名 + `grep -rwi` 关键词**扫，**判不了的（语义级方法）不在射程内**。

### 4.1 P1 列的 10 项（**去向 = 已在册**，首版 §11 已并入）

插值（§2.2 #9）· 蚁群 ACO（§2.3 #9）· 人工鱼群（§2.3 #10）· GA 变体（§2.3 #11）· PERT（§2.7 #10）·
TSP（§2.7 #11）· SVM 分类（§2.8 #2）· SVM 回归（§2.8 #3）· ELM（§2.8 #4）· **灰色关联/优势分析（**移类**：§2.6 #4）**。
⇒ **10 项全部在册，无新增**（第 10 项是"移类"而非"新增"）。

### 4.2 复核扫出的候选（**逐条给去向**）

| 候选（全路径） | 是什么（实测） | **去向** |
| :--- | :--- | :--- |
| `corpus/algorithms/src/GraphTheory(图论)/detailed/网络流/{fofuf.m,boundnetf.m,restrf.m}` | 最大流变体：`fofuf` 最大流 · `boundnetf` **带上下界的最大流（该目录 `readme.txt` 自记"有问题"）** · `restrf` 带需求的最大流 | **归入 network #3「最大流/最小割」**（同一问题族，不新立行；`boundnetf` 的已知问题写进方法文件的"常见坑"） |
| `corpus/algorithms/src/GraphTheory(图论)/basic/grMinVerCover.m`（最小点覆盖）· `grMinEdgeCover.m`（最小边覆盖）· `grMaxStabSet.m`（最大独立集） | 图覆盖/独立集家族（NP-hard 组合优化） | **归入 network #5，并把该行改名为「匹配与覆盖」**（★ 理由见 §6④） |
| `corpus/algorithms/src/GraphTheory(图论)/basic/{grMaxComSu.m,grMinAbsVerSet.m}`（最大团 / 最小支配集） | 同上家族（团 = 独立集的补图；支配集 = 覆盖的对偶） | **同上，归 network #5「匹配与覆盖」**（**一并登记，不声称穷尽该家族**） |
| `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH15/rsolve.m` | **z 变换解线性定常离散系统** `X(k+1)=F X(k)+G U(k)`（**中文注释**，故 `difference equation` 检索不到） | **登记为 mechanism #4「差分方程」的"起点素材"**（**#4 仍判 `补`** —— 见下） |
| `…/CH15/{fouriern.m,dft.m,Laplace_Define.m}` | 积分变换（多重傅里叶 / DFT / 拉普拉斯，`见 also ztrans,iztrans,int`） | **不入库**（**数学工具层，非建模方法层**；它们是解 ODE/PDE 的工具，不是可选的"模型"） |
| `corpus/algorithms/src/MATLAB智能算法30个案例分析/chapter5…`（基于遗传算法的 LQR 控制器优化）· `chapter14…`（PSO-PID 控制器优化） | 控制论（控制器参数优化） | **不入库**（**超出八类模型库范围** —— MCM 八类不含控制；其优化内核已被 GA/PSO 行覆盖） |
| `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH02–CH13`（导数/积分/级数/多重积分/数值积分）· `CH07/{bisect.m,newton.m}` · `CH08/{Gauss_legendre.m,InterpolatoryQuad.m}` | 微积分与数值积分 | **不入库**（**工具层**；数值积分/求根不是八类里的"模型"） |
| `corpus/algorithms/src/《MATLAB图像处理》源文件/`（339 个 `.m`） | 图像处理 | **不入库**（与八类模型无关） |

### 4.3 ★ CH15/`rsolve.m` 与 mechanism #4 的边界（**必须写清，防"说大了"**）

- `rsolve.m` **确是**一个"差分方程/离散系统"实现 —— 但**只覆盖线性定常系统**、且**用符号 z 变换**（`ztrans`/`iztrans`），
  **不是**通用的离散动力系统迭代/稳定性判据实现。
- ⇒ **口径写死**：**#4 仍判 `补`**（本模块前置批次照 Task 1 自建 `difference_equations.m`），
  **但把 `rsolve.m` 登记为起点素材**；**不许**再写"差分方程 —— 本归档全 0"这种**说大了的反向话**
  （正确写法：**"本归档无通用差分方程/离散动力系统实现；CH15/`rsolve.m` 覆盖线性定常离散系统（z 变换法），可作起点素材"**）。
- ★ 这条同时**修正设计 §7 第 2 行**"只有 ODE（Euler 可改造）"的隐含范围 —— **Euler 之外还有 z 变换法一条**。

---

## 5. 两组口径（P3 / recon §C⑤）

### 5.1 二级层计数（`510` vs `1,028`）

**实测（当场跑）**：

| 层 | 目录 | 文件数（`find -type f | wc -l`） | `.m` 数 |
| :--- | :--- | ---: | ---: |
| **二级层** | `corpus/algorithms/src/MATLAB智能算法30个案例分析/` | 232 | 215 |
| | `corpus/algorithms/src/《MATLAB 神经网络30个案例分析》源程序 数据/` | 149 | 137 |
| | `corpus/algorithms/src/《MATLAB神经网络原理与实例精解》随书附带源程序/` | 130 | 127 |
| | **二级层 3 目录小计** | **511** | 479 |
| **三级层** | `corpus/algorithms/src/《MATLAB图像处理》源文件/` | 342 | 339 |
| | `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/` | 123 | 123 |
| | **三级层 2 目录小计** | **465** | 462 |

- ⇒ **实测二级层（3 目录） = 511**（`INDEX.md` §1 记 `510` ⇒ **差 1**，**可能是 INDEX 写成时的读数**）；
  **实测三级层（2 目录） = 465**（**与 `INDEX.md` §1 的 `465` 一致**）。
- ★ **`1,028` 复现不出**（`INDEX.md` 的 §12「下一步」与 §10.6 尾注各记一次）：**511 / 465 / 511+465=976 / 255+479=734 都不是 1,028**；
  **无可用口径能锚出它**（**不声称穷尽尝试**：我试了分层求和、`.m` 求和、含/不含三级层等几种读法）。
  ⇒ **口径（写死）**：**凡引用本归档的层级文件数，一律引"二级 511 / 三级 465（实测 2026-10-04）"**，
  **`1,028` 一律不再引用**（`INDEX.md` 的两处订正见 §8）。

### 5.2 层级口径（一级 = ?）

**以 `INDEX.md` 的分层为准（写死）**：

- **一级层 = 15 个作者自有目录**（`AHP层次分析法` … `TimeSeries时间序列函数`）—— **实测 285 文件 / 255 `.m`**
  （`INDEX.md` §1 记 `282` ⇒ **差 3**，登记为 INDEX 陈旧读数）；
- **二级层 = 3 个随书/案例目录**（`MATLAB智能算法30个案例分析` + 两本神经网络书）—— 实测 511；
- **三级层 = 2 个随书目录**（`《MATLAB图像处理》源文件` · `《基于MATLAB的高等数学问题求解》 随书附带源程序`）—— 实测 465；
- 另有 **`corpus/algorithms/src/README.md` 1 个游离文件**（285+511+465+1 = **1262** = 全树文件数 ✓）。
- ★★ **任务书那句"`src/` 一级 15 目录 + 三个三级层 + 二级层两个大目录"是标签互换的笔误**：
  **实测是"二级层 3 个、三级层 2 个"**（以 `INDEX.md` 与实测为准）。**本节不采用任务书的那个标签**。

---

## 6. 三处粒度/去重裁定的结论（§11.9 末"Task 0 一并裁"）

| # | 瑕疵 | **裁定** |
| :--- | :--- | :--- |
| ① | **模糊聚类归哪条** | **归 ml 的"聚类"行（§2.8 #5）**，**正条目**；**从 evaluation 移出**（沿用 §11.1 的订正）。`盘` 素材 = `corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/模糊聚类/`。 |
| ② | **层次聚类被算两次**（§11.6 #2 与 §11.8 #5） | **正条目 = statistics #2「系统聚类（层次聚类）」（§2.6 #2）**，`盘` 素材 = `corpus/algorithms/src/MultivariateAnalysis（…）/聚类分析/{system_cluster.m,main.m}`（`main.m` 用 `linkage/dendrogram`，**实测确为层次聚类**）。**§2.8 #5 不再列"层次"**。 |
| ③ | **§11.8 #5 一行并列三种聚类**（与"SVM 分类/回归分行"粒度不一致） | **收敛为一行「聚类（K-means / 模糊 C-means）」**：**层次聚类**归 ②（statistics #2）；**模糊聚类**归 ①；**K-means 无归档实现**（`grep -rli kmeans`/`k-means`/`k均值` 实测 **0 命中**，MATLAB 侧走内置 `kmeans`）。⇒ 该行 `盘` 依据 = `chapter20`（GA-SA 模糊 C-means）+ `模糊聚类/`。 |
| ④ | **network #5 反向扫扩范围**（§4.2，**本次反向扫新增的裁定**） | **把 #5 由「匹配」改名为「匹配与覆盖」**，把 `basic/{grMinVerCover,grMinEdgeCover,grMaxStabSet,grMaxComSu,grMinAbsVerSet}.m` 归入该行。**理由**：匹配–点覆盖（König）、独立集–点覆盖（互补）、团–独立集（补图）**同属一个组合优化家族**，且**该族此前完全缺席**；**不新立行**是为**守住 66 的计数**（hint #6 / 硬要求 8）。**ASCII 名仍取 `matching.m`**（沿用计划的文件结构）。 |

★ **每一条都不改总数** —— 裁定后仍 **66**（**逐类见 §0 表**）。

---

## 7. 边界与不做（本花名册的诚实声明）

- ★ **本表不声称穷尽**（沿用 §11.9）：二级层 30 章里**还有未点名的 GA 变体与神经网络变体**；反向扫（§4）按"目录 + 文件名 + 关键词"扫，**语义级方法不在射程内**。
- ★ **本件只裁 66 项的范围与命名**；**方法文件本体（六格）归 Task 4–12**。
- ★ **"素材 0" ≠ "语料 0"**（GC15）：本件的 `补` 判定**只针对 `corpus/algorithms/src/`（算法素材面）**；
  **语料面（`corpus/papers/`）另算**（如 Lotka-Volterra 素材 0、语料 4 篇在用）。
- ★ **低使用度的三项**（`queueing` · `abm` · `dim_reduction`）**照补是为覆盖面，不许写成"常用"**（P5）。
- ★ **常用度证据只有 2025 一年、43 篇**（P7）⇒ 超出该范围的一律标「无依据、凭印象」。

---

## 8. `corpus/algorithms/INDEX.md` 的订正（与花名册同批处置）

**按「改时点标注 + 追加现值、不覆盖旧值」订正 `INDEX.md` §4 + 连带 4 处**（**按节名定位**）：
§4 的「本归档无」原句**改掉**（GC14："加订正注" ≠ "改原句"）· 本台账自身 2 处（§C「两处已知缺口」引注 + §G.2 表第 4 行）· `INDEX.md` §9 对照表「❌ 空」格与 §12。
**改法的完整文本见**：`.superpowers/sdd/task-m4-ms-t0-report.md` 与本批提交。
