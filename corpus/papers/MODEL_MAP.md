# MODEL_MAP — 题型 → 模型/算法 配对表（2025 美赛 O 奖论文）

> 合集：`corpus/历届优秀论文/2025美赛O奖论文/`　·　篇数：**43**　·　题数：**6**　·　桶数：**19**　·　`(模型, 篇)` 对：**496**
> 生成器：`tools/papers/model_map.py` 的 `build()`（**确定性**：同输入同字节）；判据：`tests/papers/verify_map.py`（M-1…M-16）。

## 口径（读表之前先读这一段）

1. **两个数据源、都读回、都不重算**：题型/数据形态 ← `corpus/papers/PROBLEM_TYPES.md`（人工逐题读题面后的标注）；模型/算法与其**指针** ← `corpus/papers/TAGS.md`（Task 6 的产物：受控词表 `tools/papers/vocab/models.txt` 的**字面命中**）。**本表不自己去 md 里抽模型**——那会让配对的两侧同源，「配对 == 指针」这条判据当场变成恒真。
2. **配对的推理轴只有两条：`(L1,L2)` × `data_regime`**（用户 2026-09-26 定案）。`scenario`（场景，如「考古 / 旅游」）**只作检索标签、不进配对**（原话：*「实际模型的确立并不与场景有关」*）。
3. **`核心` / `附带` 的用法**：`核心` = 题干明确要求做这件事；`附带` = 题面出现但非题干任务。**两类都进桶**（信息不丢），桶的「标记」列写出该桶的标记；**查表时优先看 `核心` 桶**——`附带` 桶说的是「获奖论文在解决题干任务时顺带用到的」。
4. **指针的展开形态（阶段 2b 改过形状，这里说明为什么）**：第二节先给**每个桶一行**的配对总表（8 列），再给**按 `(模型, 篇)` 去重**的指针行——**每条 = 一个对**，末尾多一列**「所属桶」**。**上一版**是「同一个对在每个标签桶里各抄一遍」（1646 行 / 334 KB），同一个对平均重复约 3.8 次；用户 2026-09-26 裁决去重。**判据跟着改了形状**（原 M-3 → 现 M-13）：不再拿「逐桶展开」判两向相等，改成拿**去重后的对集合**判，并**另判**每行的「所属桶」集合 == 由标注推出的桶集合。这不是放宽：**去重后判的是同一个集合**，而「桶归属」这一列在旧形态里**根本没有**（旧形态靠重复隐式携带它，无从单独判）。
5. **`x<次数>` 是「该词在**该篇全篇**出现的次数」**（不是这一行的）；**低置信 = `x1`（全篇只出现一次）**，单列在第三节。
6. **本表是「获奖论文用过什么」的事实登记，不是「这道题该用什么模型」的规范建议**（后者要的是匹配度与效度分析，属阶段 2b）。

## 覆盖边界（**机读**，必须与表同读）

> 覆盖边界：标注题数=67 · 有论文的题=6 · 未配对的题=61 · 覆盖年份=2025 · 未配对逐题=2016 A、2016 B、2016 C、2016 D、2016 E、2016 F、2017 A、2017 B、2017 C、2017 D、2017 E、2017 F、2018 A、2018 B、2018 C、2018 D、2018 E、2018 F、2019 A、2019 B、2019 C、2019 D、2019 E、2019 F、2020 A、2020 B、2020 C、2020 D、2020 E、2020 F、2021 A、2021 B、2021 C、2021 D、2021 E、2021 F、2022 A、2022 B、2022 C、2022 D、2022 E、2022 F、2023 A、2023 B、2023 C、2023 D、2023 E、2023 F、2023 Z、2024 A、2024 B、2024 C、2024 D、2024 E、2024 F、2026 A、2026 B、2026 C、2026 D、2026 E、2026 F

* **本表只覆盖 2025 的 A/B/C/D/E/F 共 6 题**（`corpus/历届优秀论文/` 里**只有 `2025美赛O奖论文` 这 43 篇被建过索引**；其余合集：2022 / 2023 / 2024 三本与 UMAP 两本**未建索引**，Task 9 才做）。
* `corpus/官方原题/` 的题面共 **67** 道，其余 **61** 道**有题型、无配对**（逐题列在上面那一行里）。**不得**拿别的年份的论文来凑——那不是配对、是编造（任务书 §一 产物 3 的明文边界）。
* 等式：**有论文的题 + 未配对的题 == 标注题数**（6 + 61 == 67），两边都与标注文件**逐题**对得上（判据 M-6）。

## 第一节 · 逐题（6 题）

### 2025 A — Testing Time: The Constant Wear On Stairs

- 题型（`核心` / `附带` **全列**）：`核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史**；`核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模**；`核心` **5 统计推断与因果 · 5.4 不确定性与敏感性**
- 数据形态：`无数据(纯机理/假设)`
- 场景（**只作检索标签，不进配对**）：考古 / 材料 / 人因
- 论文数：5
- 该题论文用过的模型/算法（**去重 25 个**，附篇数）：
  - Archard Law（5 篇）：P2025-A-01 P2025-A-02 P2025-A-03 P2025-A-04 P2025-A-05
  - Monte Carlo（4 篇）：P2025-A-01 P2025-A-02 P2025-A-04 P2025-A-05
  - sensitivity analysis（4 篇）：P2025-A-01 P2025-A-03 P2025-A-04 P2025-A-05
  - Bayesian（3 篇）：P2025-A-02 P2025-A-04 P2025-A-05
  - Gaussian Distribution（2 篇）：P2025-A-02 P2025-A-04
  - correlation coefficient（2 篇）：P2025-A-01 P2025-A-04
  - differential equation（2 篇）：P2025-A-01 P2025-A-04
  - hypothesis test（2 篇）：P2025-A-01 P2025-A-05
  - machine learning（2 篇）：P2025-A-01 P2025-A-05
  - partial differential equation（2 篇）：P2025-A-01 P2025-A-04
  - particle swarm optimization（2 篇）：P2025-A-01 P2025-A-04
  - CNN（1 篇）：P2025-A-05
  - Central Limit Theorem（1 篇）：P2025-A-03
  - Credible Intervals（1 篇）：P2025-A-04
  - Gaussian Mixture Algorithm（1 篇）：P2025-A-03
  - Markov chain（1 篇）：P2025-A-04
  - Markov chain Monte Carlo（1 篇）：P2025-A-04
  - Navier-Stokes（1 篇）：P2025-A-01
  - Uncertainty Quantification（1 篇）：P2025-A-04
  - Weathering Degree Model（1 篇）：P2025-A-05
  - cross-validation（1 篇）：P2025-A-05
  - feature selection（1 篇）：P2025-A-01
  - finite difference（1 篇）：P2025-A-01
  - linear regression（1 篇）：P2025-A-02
  - system dynamics（1 篇）：P2025-A-04

### 2025 B — Managing Sustainable Tourism

- 题型（`核心` / `附带` **全列**）：`核心` **3 优化 · 3.3 多目标/权衡**；`核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化**；`核心` **1 预测 · 1.3 情景与概率预测**；`核心` **5 统计推断与因果 · 5.4 不确定性与敏感性**
- 数据形态：`无数据(纯机理/假设)`
- 场景（**只作检索标签，不进配对**）：旅游 / 公共政策
- 论文数：7
- 该题论文用过的模型/算法（**去重 31 个**，附篇数）：
  - sensitivity analysis（7 篇）：P2025-B-01 P2025-B-02 P2025-B-03 P2025-B-04 P2025-B-05 P2025-B-06 P2025-B-07
  - multi-objective optimization（4 篇）：P2025-B-02 P2025-B-04 P2025-B-05 P2025-B-07
  - Pareto（3 篇）：P2025-B-02 P2025-B-05 P2025-B-07
  - system dynamics（3 篇）：P2025-B-03 P2025-B-06 P2025-B-07
  - AHP（2 篇）：P2025-B-03 P2025-B-07
  - NSGA-II（2 篇）：P2025-B-05 P2025-B-07
  - Regression Analysis（2 篇）：P2025-B-01 P2025-B-07
  - genetic algorithm（2 篇）：P2025-B-05 P2025-B-07
  - logistic regression（2 篇）：P2025-B-01 P2025-B-03
  - nonlinear regression（2 篇）：P2025-B-03 P2025-B-07
  - ARIMA（1 篇）：P2025-B-01
  - CVM（1 篇）：P2025-B-01
  - L-BFGS-B algorithm（1 篇）：P2025-B-06
  - Lotka-Volterra（1 篇）：P2025-B-03
  - Monte Carlo（1 篇）：P2025-B-01
  - SIS model（1 篇）：P2025-B-03
  - SLSQP（1 篇）：P2025-B-02
  - cluster analysis（1 篇）：P2025-B-03
  - correlation coefficient（1 篇）：P2025-B-07
  - deep learning（1 篇）：P2025-B-05
  - differential equation（1 篇）：P2025-B-06
  - dynamic programming（1 篇）：P2025-B-04
  - entropy weight method（1 篇）：P2025-B-04
  - factor analysis（1 篇）：P2025-B-05
  - hypothesis test（1 篇）：P2025-B-05
  - linear regression（1 篇）：P2025-B-01
  - nonlinear programming（1 篇）：P2025-B-01
  - ordinary differential equation（1 篇）：P2025-B-03
  - particle swarm optimization（1 篇）：P2025-B-01
  - reinforcement learning（1 篇）：P2025-B-02
  - structural equation modeling（1 篇）：P2025-B-07

### 2025 C — Models for Olympic Medal Tables

- 题型（`核心` / `附带` **全列**）：`核心` **1 预测 · 1.2 回归/相关预测**；`核心` **1 预测 · 1.5 零膨胀/受限计数预测**；`核心` **5 统计推断与因果 · 5.2 回归系数与效应量**；`核心` **7 分类与聚类 · 7.1 监督分类/识别**
- 数据形态：`面板`
- 场景（**只作检索标签，不进配对**）：体育
- 论文数：18
- 该题论文用过的模型/算法（**去重 76 个**，附篇数）：
  - sensitivity analysis（16 篇）：P2025-C-01 P2025-C-02 P2025-C-03 P2025-C-04 P2025-C-05 P2025-C-06 P2025-C-07 P2025-C-08 P2025-C-09 P2025-C-10 P2025-C-11 P2025-C-12 P2025-C-13 P2025-C-14 P2025-C-15 P2025-C-16
  - machine learning（14 篇）：P2025-C-01 P2025-C-02 P2025-C-03 P2025-C-04 P2025-C-05 P2025-C-07 P2025-C-08 P2025-C-09 P2025-C-10 P2025-C-11 P2025-C-12 P2025-C-13 P2025-C-15 P2025-C-18
  - random forest（13 篇）：P2025-C-01 P2025-C-02 P2025-C-03 P2025-C-04 P2025-C-05 P2025-C-06 P2025-C-07 P2025-C-08 P2025-C-09 P2025-C-11 P2025-C-13 P2025-C-15 P2025-C-16
  - time series analysis（12 篇）：P2025-C-01 P2025-C-04 P2025-C-05 P2025-C-06 P2025-C-10 P2025-C-11 P2025-C-12 P2025-C-13 P2025-C-14 P2025-C-15 P2025-C-16 P2025-C-17
  - decision tree（11 篇）：P2025-C-02 P2025-C-03 P2025-C-05 P2025-C-06 P2025-C-07 P2025-C-08 P2025-C-10 P2025-C-11 P2025-C-13 P2025-C-15 P2025-C-16
  - linear regression（11 篇）：P2025-C-03 P2025-C-04 P2025-C-05 P2025-C-06 P2025-C-07 P2025-C-11 P2025-C-12 P2025-C-13 P2025-C-15 P2025-C-16 P2025-C-17
  - logistic regression（10 篇）：P2025-C-01 P2025-C-02 P2025-C-03 P2025-C-05 P2025-C-06 P2025-C-08 P2025-C-12 P2025-C-13 P2025-C-15 P2025-C-18
  - Bayesian（9 篇）：P2025-C-01 P2025-C-02 P2025-C-09 P2025-C-10 P2025-C-13 P2025-C-14 P2025-C-16 P2025-C-17 P2025-C-18
  - cross-validation（9 篇）：P2025-C-01 P2025-C-03 P2025-C-05 P2025-C-07 P2025-C-08 P2025-C-10 P2025-C-11 P2025-C-13 P2025-C-15
  - Monte Carlo（8 篇）：P2025-C-03 P2025-C-04 P2025-C-06 P2025-C-09 P2025-C-11 P2025-C-14 P2025-C-16 P2025-C-18
  - XGBoost（8 篇）：P2025-C-01 P2025-C-02 P2025-C-07 P2025-C-08 P2025-C-09 P2025-C-11 P2025-C-13 P2025-C-15
  - neural network（8 篇）：P2025-C-02 P2025-C-03 P2025-C-07 P2025-C-10 P2025-C-11 P2025-C-13 P2025-C-14 P2025-C-15
  - Regression Analysis（7 篇）：P2025-C-03 P2025-C-04 P2025-C-08 P2025-C-09 P2025-C-11 P2025-C-13 P2025-C-17
  - difference-in-differences（7 篇）：P2025-C-01 P2025-C-02 P2025-C-08 P2025-C-10 P2025-C-12 P2025-C-13 P2025-C-14
  - bootstrap（6 篇）：P2025-C-01 P2025-C-03 P2025-C-07 P2025-C-08 P2025-C-10 P2025-C-13
  - cluster analysis（6 篇）：P2025-C-01 P2025-C-06 P2025-C-08 P2025-C-11 P2025-C-12 P2025-C-17
  - correlation coefficient（6 篇）：P2025-C-01 P2025-C-02 P2025-C-05 P2025-C-08 P2025-C-12 P2025-C-14
  - stacking（6 篇）：P2025-C-01 P2025-C-02 P2025-C-08 P2025-C-11 P2025-C-13 P2025-C-16
  - ARIMA（5 篇）：P2025-C-04 P2025-C-05 P2025-C-06 P2025-C-11 P2025-C-12
  - deep learning（5 篇）：P2025-C-01 P2025-C-09 P2025-C-14 P2025-C-15 P2025-C-16
  - LSTM（4 篇）：P2025-C-01 P2025-C-09 P2025-C-11 P2025-C-14
  - SHAP（4 篇）：P2025-C-01 P2025-C-08 P2025-C-10 P2025-C-13
  - Tobit（4 篇）：P2025-C-02 P2025-C-12 P2025-C-13 P2025-C-17
  - feature selection（4 篇）：P2025-C-03 P2025-C-04 P2025-C-13 P2025-C-15
  - gradient boosting（4 篇）：P2025-C-01 P2025-C-08 P2025-C-11 P2025-C-13
  - hurdle model（4 篇）：P2025-C-02 P2025-C-12 P2025-C-13 P2025-C-17
  - hypothesis test（4 篇）：P2025-C-01 P2025-C-13 P2025-C-14 P2025-C-15
  - moving average（4 篇）：P2025-C-05 P2025-C-06 P2025-C-16 P2025-C-17
  - principal component analysis（4 篇）：P2025-C-01 P2025-C-02 P2025-C-03 P2025-C-10
  - zero-inflated（4 篇）：P2025-C-02 P2025-C-04 P2025-C-10 P2025-C-18
  - Causal Inference（3 篇）：P2025-C-02 P2025-C-10 P2025-C-14
  - Cox proportional hazards（3 篇）：P2025-C-11 P2025-C-14 P2025-C-18
  - Markov chain（3 篇）：P2025-C-01 P2025-C-09 P2025-C-18
  - Markov chain Monte Carlo（3 篇）：P2025-C-09 P2025-C-14 P2025-C-18
  - SVM（3 篇）：P2025-C-07 P2025-C-08 P2025-C-11
  - Uncertainty Quantification（3 篇）：P2025-C-04 P2025-C-09 P2025-C-14
  - K-means（2 篇）：P2025-C-06 P2025-C-08
  - SARIMA（2 篇）：P2025-C-12 P2025-C-16
  - SVR（2 篇）：P2025-C-10 P2025-C-11
  - lasso（2 篇）：P2025-C-05 P2025-C-15
  - propensity score matching（2 篇）：P2025-C-08 P2025-C-12
  - BP neural network（1 篇）：P2025-C-07
  - Bayesian network（1 篇）：P2025-C-14
  - CNN（1 篇）：P2025-C-14
  - Credible Intervals（1 篇）：P2025-C-09
  - GSRF（1 篇）：P2025-C-05
  - Gaussian Distribution（1 篇）：P2025-C-16
  - LR-SCAD Model（1 篇）：P2025-C-16
  - Laplace smoothing（1 篇）：P2025-C-10
  - Mann-Kendall（1 篇）：P2025-C-11
  - Mixed-effects Model（1 篇）：P2025-C-18
  - Posterior inference（1 篇）：P2025-C-09
  - RNN（1 篇）：P2025-C-09
  - Residual Analysis（1 篇）：P2025-C-16
  - Shannon entropy（1 篇）：P2025-C-10
  - Threshold Method（1 篇）：P2025-C-11
  - TrueSkill（1 篇）：P2025-C-16
  - analysis of variance（1 篇）：P2025-C-18
  - association rules（1 篇）：P2025-C-18
  - centrality（1 篇）：P2025-C-14
  - change-point detection（1 篇）：P2025-C-02
  - exponential smoothing（1 篇）：P2025-C-04
  - factor analysis（1 篇）：P2025-C-14
  - genetic algorithm（1 篇）：P2025-C-10
  - grey prediction（1 篇）：P2025-C-11
  - grey relational analysis（1 篇）：P2025-C-15
  - isolation forest（1 篇）：P2025-C-11
  - particle swarm optimization（1 篇）：P2025-C-12
  - probit（1 篇）：P2025-C-17
  - regression discontinuity（1 篇）：P2025-C-03
  - reinforcement learning（1 篇）：P2025-C-01
  - ridge regression（1 篇）：P2025-C-15
  - self-organizing map（1 篇）：P2025-C-14
  - spatio-temporal modeling（1 篇）：P2025-C-14
  - survival analysis（1 篇）：P2025-C-11
  - two-stage least squares（1 篇）：P2025-C-02

### 2025 D — A Roadmap to a Better City

- 题型（`核心` / `附带` **全列**）：`核心` **8 网络与图 · 8.2 流量分配/路由**；`核心` **2 评价与排序 · 2.3 排序规则/权重设计**；`核心` **9 决策与博弈 · 9.1 多准则决策**；`附带` **3 优化 · 3.5 调度与配置**
- 数据形态：`网络`
- 场景（**只作检索标签，不进配对**）：城市交通 / 基础设施
- 论文数：4
- 该题论文用过的模型/算法（**去重 30 个**，附篇数）：
  - sensitivity analysis（4 篇）：P2025-D-01 P2025-D-02 P2025-D-03 P2025-D-04
  - shortest path（4 篇）：P2025-D-01 P2025-D-02 P2025-D-03 P2025-D-04
  - centrality（3 篇）：P2025-D-01 P2025-D-03 P2025-D-04
  - Monte Carlo（2 篇）：P2025-D-01 P2025-D-03
  - entropy weight method（2 篇）：P2025-D-02 P2025-D-04
  - A* and GA（1 篇）：P2025-D-01
  - A-star（1 篇）：P2025-D-01
  - BP neural network（1 篇）：P2025-D-01
  - Bayesian（1 篇）：P2025-D-03
  - Markov chain（1 篇）：P2025-D-03
  - Markov chain Monte Carlo（1 篇）：P2025-D-03
  - Multi-layer network model（1 篇）：P2025-D-04
  - Pareto（1 篇）：P2025-D-03
  - TOPSIS（1 篇）：P2025-D-04
  - Wardrop（1 篇）：P2025-D-03
  - cluster analysis（1 篇）：P2025-D-02
  - correlation coefficient（1 篇）：P2025-D-02
  - dynamic programming（1 篇）：P2025-D-01
  - factor analysis（1 篇）：P2025-D-02
  - fuzzy comprehensive evaluation（1 篇）：P2025-D-03
  - fuzzy logic（1 篇）：P2025-D-03
  - genetic algorithm（1 篇）：P2025-D-01
  - graph theory（1 篇）：P2025-D-02
  - machine learning（1 篇）：P2025-D-02
  - minimum spanning tree（1 篇）：P2025-D-02
  - network analysis（1 篇）：P2025-D-02
  - network flow（1 篇）：P2025-D-03
  - nonlinear programming（1 篇）：P2025-D-01
  - queueing theory（1 篇）：P2025-D-01
  - three-layer bus network model（1 篇）：P2025-D-04

### 2025 E — Making Room for Agriculture

- 题型（`核心` / `附带` **全列**）：`核心` **4 机理建模与仿真 · 4.2 生态/生物动力学**；`核心` **1 预测 · 1.3 情景与概率预测**；`核心` **3 优化 · 3.3 多目标/权衡**；`附带` **9 决策与博弈 · 9.1 多准则决策**
- 数据形态：`无数据(纯机理/假设)`
- 场景（**只作检索标签，不进配对**）：农业 / 生态
- 论文数：4
- 该题论文用过的模型/算法（**去重 24 个**，附篇数）：
  - Food web model（4 篇）：P2025-E-01 P2025-E-02 P2025-E-03 P2025-E-04
  - sensitivity analysis（4 篇）：P2025-E-01 P2025-E-02 P2025-E-03 P2025-E-04
  - Lotka-Volterra（3 篇）：P2025-E-02 P2025-E-03 P2025-E-04
  - differential equation（3 篇）：P2025-E-01 P2025-E-02 P2025-E-03
  - system dynamics（3 篇）：P2025-E-01 P2025-E-02 P2025-E-03
  - entropy weight method（2 篇）：P2025-E-01 P2025-E-03
  - logistic regression（2 篇）：P2025-E-02 P2025-E-04
  - AHP（1 篇）：P2025-E-01
  - COMAP Model（1 篇）：P2025-E-02
  - Convex Reformulation（1 篇）：P2025-E-02
  - FATE Model（1 篇）：P2025-E-02
  - Petri net（1 篇）：P2025-E-03
  - Petri-Food Web model（1 篇）：P2025-E-03
  - Shannon entropy（1 篇）：P2025-E-03
  - centrality（1 篇）：P2025-E-01
  - differential evolution（1 篇）：P2025-E-04
  - fuzzy comprehensive evaluation（1 篇）：P2025-E-03
  - graph theory（1 篇）：P2025-E-01
  - multi-objective optimization（1 篇）：P2025-E-02
  - multi-type Holling responses（1 篇）：P2025-E-04
  - nonlinear programming（1 篇）：P2025-E-02
  - partial differential equation（1 篇）：P2025-E-02
  - shortest path（1 篇）：P2025-E-01
  - time series analysis（1 篇）：P2025-E-04

### 2025 F — Cyber Strong?

- 题型（`核心` / `附带` **全列**）：`核心` **5 统计推断与因果 · 5.3 因果/政策评估**；`核心` **2 评价与排序 · 2.1 指标体系构建**；`核心` **7 分类与聚类 · 7.2 无监督聚类/分段**
- 数据形态：`混合`
- 场景（**只作检索标签，不进配对**）：网络安全 / 公共政策
- 论文数：5
- 该题论文用过的模型/算法（**去重 24 个**，附篇数）：
  - Regression Analysis（4 篇）：P2025-F-01 P2025-F-02 P2025-F-03 P2025-F-05
  - difference-in-differences（4 篇）：P2025-F-01 P2025-F-02 P2025-F-03 P2025-F-05
  - cluster analysis（3 篇）：P2025-F-01 P2025-F-02 P2025-F-03
  - machine learning（3 篇）：P2025-F-01 P2025-F-02 P2025-F-04
  - principal component analysis（3 篇）：P2025-F-01 P2025-F-02 P2025-F-03
  - sensitivity analysis（3 篇）：P2025-F-01 P2025-F-02 P2025-F-03
  - K-means（2 篇）：P2025-F-02 P2025-F-03
  - correlation coefficient（2 篇）：P2025-F-04 P2025-F-05
  - factor analysis（2 篇）：P2025-F-02 P2025-F-03
  - linear regression（2 篇）：P2025-F-03 P2025-F-05
  - structural equation modeling（2 篇）：P2025-F-01 P2025-F-02
  - time series analysis（2 篇）：P2025-F-01 P2025-F-04
  - Bayesian（1 篇）：P2025-F-01
  - Causal Inference（1 篇）：P2025-F-02
  - Cox proportional hazards（1 篇）：P2025-F-01
  - KDMF（1 篇）：P2025-F-03
  - MIC（1 篇）：P2025-F-03
  - VBGMM（1 篇）：P2025-F-01
  - cross-validation（1 篇）：P2025-F-05
  - hypothesis test（1 篇）：P2025-F-01
  - integer programming（1 篇）：P2025-F-02
  - logistic regression（1 篇）：P2025-F-01
  - network analysis（1 篇）：P2025-F-02
  - survival analysis（1 篇）：P2025-F-01

## 第二节 · 按 `(L1,L2)` × `data_regime` 聚合（**每个桶一行**）

共 **19** 个桶。列序：`桶 | (L1,L2) | data_regime | 标记 | 来源题 | 论文数 | (模型,篇) 对 | 模型/算法（篇数）`。

| 桶 | `(L1,L2)` | `data_regime` | 标记 | 来源题 | 论文数 | (模型,篇) 对 | 模型/算法（篇数） |
| :-- | :-- | :-- | :-: | :-- | ---: | ---: | :-- |
| 1 | 1 预测 · 1.2 回归/相关预测 | 面板 | 核心 | 2025 C | 18 | 280 | sensitivity analysis（16 篇） · machine learning（14 篇） · random forest（13 篇） · time series analysis（12 篇） · decision tree（11 篇） · linear regression（11 篇） · logistic regression（10 篇） · Bayesian（9 篇） · cross-validation（9 篇） · Monte Carlo（8 篇） · XGBoost（8 篇） · neural network（8 篇） · Regression Analysis（7 篇） · difference-in-differences（7 篇） · bootstrap（6 篇） · cluster analysis（6 篇） · correlation coefficient（6 篇） · stacking（6 篇） · ARIMA（5 篇） · deep learning（5 篇） · LSTM（4 篇） · SHAP（4 篇） · Tobit（4 篇） · feature selection（4 篇） · gradient boosting（4 篇） · hurdle model（4 篇） · hypothesis test（4 篇） · moving average（4 篇） · principal component analysis（4 篇） · zero-inflated（4 篇） · Causal Inference（3 篇） · Cox proportional hazards（3 篇） · Markov chain（3 篇） · Markov chain Monte Carlo（3 篇） · SVM（3 篇） · Uncertainty Quantification（3 篇） · K-means（2 篇） · SARIMA（2 篇） · SVR（2 篇） · lasso（2 篇） · propensity score matching（2 篇） · BP neural network（1 篇） · Bayesian network（1 篇） · CNN（1 篇） · Credible Intervals（1 篇） · GSRF（1 篇） · Gaussian Distribution（1 篇） · LR-SCAD Model（1 篇） · Laplace smoothing（1 篇） · Mann-Kendall（1 篇） · Mixed-effects Model（1 篇） · Posterior inference（1 篇） · RNN（1 篇） · Residual Analysis（1 篇） · Shannon entropy（1 篇） · Threshold Method（1 篇） · TrueSkill（1 篇） · analysis of variance（1 篇） · association rules（1 篇） · centrality（1 篇） · change-point detection（1 篇） · exponential smoothing（1 篇） · factor analysis（1 篇） · genetic algorithm（1 篇） · grey prediction（1 篇） · grey relational analysis（1 篇） · isolation forest（1 篇） · particle swarm optimization（1 篇） · probit（1 篇） · regression discontinuity（1 篇） · reinforcement learning（1 篇） · ridge regression（1 篇） · self-organizing map（1 篇） · spatio-temporal modeling（1 篇） · survival analysis（1 篇） · two-stage least squares（1 篇） |
| 2 | 1 预测 · 1.3 情景与概率预测 | 无数据(纯机理/假设) | 核心 | 2025 B、2025 E | 11 | 88 | sensitivity analysis（11 篇） · system dynamics（6 篇） · multi-objective optimization（5 篇） · Food web model（4 篇） · Lotka-Volterra（4 篇） · differential equation（4 篇） · logistic regression（4 篇） · AHP（3 篇） · Pareto（3 篇） · entropy weight method（3 篇） · NSGA-II（2 篇） · Regression Analysis（2 篇） · genetic algorithm（2 篇） · nonlinear programming（2 篇） · nonlinear regression（2 篇） · ARIMA（1 篇） · COMAP Model（1 篇） · CVM（1 篇） · Convex Reformulation（1 篇） · FATE Model（1 篇） · L-BFGS-B algorithm（1 篇） · Monte Carlo（1 篇） · Petri net（1 篇） · Petri-Food Web model（1 篇） · SIS model（1 篇） · SLSQP（1 篇） · Shannon entropy（1 篇） · centrality（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · deep learning（1 篇） · differential evolution（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · graph theory（1 篇） · hypothesis test（1 篇） · linear regression（1 篇） · multi-type Holling responses（1 篇） · ordinary differential equation（1 篇） · partial differential equation（1 篇） · particle swarm optimization（1 篇） · reinforcement learning（1 篇） · shortest path（1 篇） · structural equation modeling（1 篇） · time series analysis（1 篇） |
| 3 | 1 预测 · 1.5 零膨胀/受限计数预测 | 面板 | 核心 | 2025 C | 18 | 280 | sensitivity analysis（16 篇） · machine learning（14 篇） · random forest（13 篇） · time series analysis（12 篇） · decision tree（11 篇） · linear regression（11 篇） · logistic regression（10 篇） · Bayesian（9 篇） · cross-validation（9 篇） · Monte Carlo（8 篇） · XGBoost（8 篇） · neural network（8 篇） · Regression Analysis（7 篇） · difference-in-differences（7 篇） · bootstrap（6 篇） · cluster analysis（6 篇） · correlation coefficient（6 篇） · stacking（6 篇） · ARIMA（5 篇） · deep learning（5 篇） · LSTM（4 篇） · SHAP（4 篇） · Tobit（4 篇） · feature selection（4 篇） · gradient boosting（4 篇） · hurdle model（4 篇） · hypothesis test（4 篇） · moving average（4 篇） · principal component analysis（4 篇） · zero-inflated（4 篇） · Causal Inference（3 篇） · Cox proportional hazards（3 篇） · Markov chain（3 篇） · Markov chain Monte Carlo（3 篇） · SVM（3 篇） · Uncertainty Quantification（3 篇） · K-means（2 篇） · SARIMA（2 篇） · SVR（2 篇） · lasso（2 篇） · propensity score matching（2 篇） · BP neural network（1 篇） · Bayesian network（1 篇） · CNN（1 篇） · Credible Intervals（1 篇） · GSRF（1 篇） · Gaussian Distribution（1 篇） · LR-SCAD Model（1 篇） · Laplace smoothing（1 篇） · Mann-Kendall（1 篇） · Mixed-effects Model（1 篇） · Posterior inference（1 篇） · RNN（1 篇） · Residual Analysis（1 篇） · Shannon entropy（1 篇） · Threshold Method（1 篇） · TrueSkill（1 篇） · analysis of variance（1 篇） · association rules（1 篇） · centrality（1 篇） · change-point detection（1 篇） · exponential smoothing（1 篇） · factor analysis（1 篇） · genetic algorithm（1 篇） · grey prediction（1 篇） · grey relational analysis（1 篇） · isolation forest（1 篇） · particle swarm optimization（1 篇） · probit（1 篇） · regression discontinuity（1 篇） · reinforcement learning（1 篇） · ridge regression（1 篇） · self-organizing map（1 篇） · spatio-temporal modeling（1 篇） · survival analysis（1 篇） · two-stage least squares（1 篇） |
| 4 | 2 评价与排序 · 2.1 指标体系构建 | 混合 | 核心 | 2025 F | 5 | 44 | Regression Analysis（4 篇） · difference-in-differences（4 篇） · cluster analysis（3 篇） · machine learning（3 篇） · principal component analysis（3 篇） · sensitivity analysis（3 篇） · K-means（2 篇） · correlation coefficient（2 篇） · factor analysis（2 篇） · linear regression（2 篇） · structural equation modeling（2 篇） · time series analysis（2 篇） · Bayesian（1 篇） · Causal Inference（1 篇） · Cox proportional hazards（1 篇） · KDMF（1 篇） · MIC（1 篇） · VBGMM（1 篇） · cross-validation（1 篇） · hypothesis test（1 篇） · integer programming（1 篇） · logistic regression（1 篇） · network analysis（1 篇） · survival analysis（1 篇） |
| 5 | 2 评价与排序 · 2.3 排序规则/权重设计 | 网络 | 核心 | 2025 D | 4 | 40 | sensitivity analysis（4 篇） · shortest path（4 篇） · centrality（3 篇） · Monte Carlo（2 篇） · entropy weight method（2 篇） · A* and GA（1 篇） · A-star（1 篇） · BP neural network（1 篇） · Bayesian（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Multi-layer network model（1 篇） · Pareto（1 篇） · TOPSIS（1 篇） · Wardrop（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · fuzzy logic（1 篇） · genetic algorithm（1 篇） · graph theory（1 篇） · machine learning（1 篇） · minimum spanning tree（1 篇） · network analysis（1 篇） · network flow（1 篇） · nonlinear programming（1 篇） · queueing theory（1 篇） · three-layer bus network model（1 篇） |
| 6 | 3 优化 · 3.3 多目标/权衡 | 无数据(纯机理/假设) | 核心 | 2025 B、2025 E | 11 | 88 | sensitivity analysis（11 篇） · system dynamics（6 篇） · multi-objective optimization（5 篇） · Food web model（4 篇） · Lotka-Volterra（4 篇） · differential equation（4 篇） · logistic regression（4 篇） · AHP（3 篇） · Pareto（3 篇） · entropy weight method（3 篇） · NSGA-II（2 篇） · Regression Analysis（2 篇） · genetic algorithm（2 篇） · nonlinear programming（2 篇） · nonlinear regression（2 篇） · ARIMA（1 篇） · COMAP Model（1 篇） · CVM（1 篇） · Convex Reformulation（1 篇） · FATE Model（1 篇） · L-BFGS-B algorithm（1 篇） · Monte Carlo（1 篇） · Petri net（1 篇） · Petri-Food Web model（1 篇） · SIS model（1 篇） · SLSQP（1 篇） · Shannon entropy（1 篇） · centrality（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · deep learning（1 篇） · differential evolution（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · graph theory（1 篇） · hypothesis test（1 篇） · linear regression（1 篇） · multi-type Holling responses（1 篇） · ordinary differential equation（1 篇） · partial differential equation（1 篇） · particle swarm optimization（1 篇） · reinforcement learning（1 篇） · shortest path（1 篇） · structural equation modeling（1 篇） · time series analysis（1 篇） |
| 7 | 3 优化 · 3.5 调度与配置 | 网络 | 附带 | 2025 D | 4 | 40 | sensitivity analysis（4 篇） · shortest path（4 篇） · centrality（3 篇） · Monte Carlo（2 篇） · entropy weight method（2 篇） · A* and GA（1 篇） · A-star（1 篇） · BP neural network（1 篇） · Bayesian（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Multi-layer network model（1 篇） · Pareto（1 篇） · TOPSIS（1 篇） · Wardrop（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · fuzzy logic（1 篇） · genetic algorithm（1 篇） · graph theory（1 篇） · machine learning（1 篇） · minimum spanning tree（1 篇） · network analysis（1 篇） · network flow（1 篇） · nonlinear programming（1 篇） · queueing theory（1 篇） · three-layer bus network model（1 篇） |
| 8 | 4 机理建模与仿真 · 4.1 物理/化学机理建模 | 无数据(纯机理/假设) | 核心 | 2025 A | 5 | 44 | Archard Law（5 篇） · Monte Carlo（4 篇） · sensitivity analysis（4 篇） · Bayesian（3 篇） · Gaussian Distribution（2 篇） · correlation coefficient（2 篇） · differential equation（2 篇） · hypothesis test（2 篇） · machine learning（2 篇） · partial differential equation（2 篇） · particle swarm optimization（2 篇） · CNN（1 篇） · Central Limit Theorem（1 篇） · Credible Intervals（1 篇） · Gaussian Mixture Algorithm（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Navier-Stokes（1 篇） · Uncertainty Quantification（1 篇） · Weathering Degree Model（1 篇） · cross-validation（1 篇） · feature selection（1 篇） · finite difference（1 篇） · linear regression（1 篇） · system dynamics（1 篇） |
| 9 | 4 机理建模与仿真 · 4.2 生态/生物动力学 | 无数据(纯机理/假设) | 核心 | 2025 E | 4 | 38 | Food web model（4 篇） · sensitivity analysis（4 篇） · Lotka-Volterra（3 篇） · differential equation（3 篇） · system dynamics（3 篇） · entropy weight method（2 篇） · logistic regression（2 篇） · AHP（1 篇） · COMAP Model（1 篇） · Convex Reformulation（1 篇） · FATE Model（1 篇） · Petri net（1 篇） · Petri-Food Web model（1 篇） · Shannon entropy（1 篇） · centrality（1 篇） · differential evolution（1 篇） · fuzzy comprehensive evaluation（1 篇） · graph theory（1 篇） · multi-objective optimization（1 篇） · multi-type Holling responses（1 篇） · nonlinear programming（1 篇） · partial differential equation（1 篇） · shortest path（1 篇） · time series analysis（1 篇） |
| 10 | 4 机理建模与仿真 · 4.6 反馈结构与动态演化 | 无数据(纯机理/假设) | 核心 | 2025 B | 7 | 50 | sensitivity analysis（7 篇） · multi-objective optimization（4 篇） · Pareto（3 篇） · system dynamics（3 篇） · AHP（2 篇） · NSGA-II（2 篇） · Regression Analysis（2 篇） · genetic algorithm（2 篇） · logistic regression（2 篇） · nonlinear regression（2 篇） · ARIMA（1 篇） · CVM（1 篇） · L-BFGS-B algorithm（1 篇） · Lotka-Volterra（1 篇） · Monte Carlo（1 篇） · SIS model（1 篇） · SLSQP（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · deep learning（1 篇） · differential equation（1 篇） · dynamic programming（1 篇） · entropy weight method（1 篇） · factor analysis（1 篇） · hypothesis test（1 篇） · linear regression（1 篇） · nonlinear programming（1 篇） · ordinary differential equation（1 篇） · particle swarm optimization（1 篇） · reinforcement learning（1 篇） · structural equation modeling（1 篇） |
| 11 | 5 统计推断与因果 · 5.2 回归系数与效应量 | 面板 | 核心 | 2025 C | 18 | 280 | sensitivity analysis（16 篇） · machine learning（14 篇） · random forest（13 篇） · time series analysis（12 篇） · decision tree（11 篇） · linear regression（11 篇） · logistic regression（10 篇） · Bayesian（9 篇） · cross-validation（9 篇） · Monte Carlo（8 篇） · XGBoost（8 篇） · neural network（8 篇） · Regression Analysis（7 篇） · difference-in-differences（7 篇） · bootstrap（6 篇） · cluster analysis（6 篇） · correlation coefficient（6 篇） · stacking（6 篇） · ARIMA（5 篇） · deep learning（5 篇） · LSTM（4 篇） · SHAP（4 篇） · Tobit（4 篇） · feature selection（4 篇） · gradient boosting（4 篇） · hurdle model（4 篇） · hypothesis test（4 篇） · moving average（4 篇） · principal component analysis（4 篇） · zero-inflated（4 篇） · Causal Inference（3 篇） · Cox proportional hazards（3 篇） · Markov chain（3 篇） · Markov chain Monte Carlo（3 篇） · SVM（3 篇） · Uncertainty Quantification（3 篇） · K-means（2 篇） · SARIMA（2 篇） · SVR（2 篇） · lasso（2 篇） · propensity score matching（2 篇） · BP neural network（1 篇） · Bayesian network（1 篇） · CNN（1 篇） · Credible Intervals（1 篇） · GSRF（1 篇） · Gaussian Distribution（1 篇） · LR-SCAD Model（1 篇） · Laplace smoothing（1 篇） · Mann-Kendall（1 篇） · Mixed-effects Model（1 篇） · Posterior inference（1 篇） · RNN（1 篇） · Residual Analysis（1 篇） · Shannon entropy（1 篇） · Threshold Method（1 篇） · TrueSkill（1 篇） · analysis of variance（1 篇） · association rules（1 篇） · centrality（1 篇） · change-point detection（1 篇） · exponential smoothing（1 篇） · factor analysis（1 篇） · genetic algorithm（1 篇） · grey prediction（1 篇） · grey relational analysis（1 篇） · isolation forest（1 篇） · particle swarm optimization（1 篇） · probit（1 篇） · regression discontinuity（1 篇） · reinforcement learning（1 篇） · ridge regression（1 篇） · self-organizing map（1 篇） · spatio-temporal modeling（1 篇） · survival analysis（1 篇） · two-stage least squares（1 篇） |
| 12 | 5 统计推断与因果 · 5.3 因果/政策评估 | 混合 | 核心 | 2025 F | 5 | 44 | Regression Analysis（4 篇） · difference-in-differences（4 篇） · cluster analysis（3 篇） · machine learning（3 篇） · principal component analysis（3 篇） · sensitivity analysis（3 篇） · K-means（2 篇） · correlation coefficient（2 篇） · factor analysis（2 篇） · linear regression（2 篇） · structural equation modeling（2 篇） · time series analysis（2 篇） · Bayesian（1 篇） · Causal Inference（1 篇） · Cox proportional hazards（1 篇） · KDMF（1 篇） · MIC（1 篇） · VBGMM（1 篇） · cross-validation（1 篇） · hypothesis test（1 篇） · integer programming（1 篇） · logistic regression（1 篇） · network analysis（1 篇） · survival analysis（1 篇） |
| 13 | 5 统计推断与因果 · 5.4 不确定性与敏感性 | 无数据(纯机理/假设) | 核心 | 2025 A、2025 B | 12 | 94 | sensitivity analysis（11 篇） · Archard Law（5 篇） · Monte Carlo（5 篇） · multi-objective optimization（4 篇） · system dynamics（4 篇） · Bayesian（3 篇） · Pareto（3 篇） · correlation coefficient（3 篇） · differential equation（3 篇） · hypothesis test（3 篇） · particle swarm optimization（3 篇） · AHP（2 篇） · Gaussian Distribution（2 篇） · NSGA-II（2 篇） · Regression Analysis（2 篇） · genetic algorithm（2 篇） · linear regression（2 篇） · logistic regression（2 篇） · machine learning（2 篇） · nonlinear regression（2 篇） · partial differential equation（2 篇） · ARIMA（1 篇） · CNN（1 篇） · CVM（1 篇） · Central Limit Theorem（1 篇） · Credible Intervals（1 篇） · Gaussian Mixture Algorithm（1 篇） · L-BFGS-B algorithm（1 篇） · Lotka-Volterra（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Navier-Stokes（1 篇） · SIS model（1 篇） · SLSQP（1 篇） · Uncertainty Quantification（1 篇） · Weathering Degree Model（1 篇） · cluster analysis（1 篇） · cross-validation（1 篇） · deep learning（1 篇） · dynamic programming（1 篇） · entropy weight method（1 篇） · factor analysis（1 篇） · feature selection（1 篇） · finite difference（1 篇） · nonlinear programming（1 篇） · ordinary differential equation（1 篇） · reinforcement learning（1 篇） · structural equation modeling（1 篇） |
| 14 | 6 反演与参数估计 · 6.1 由观测反推参数/历史 | 无数据(纯机理/假设) | 核心 | 2025 A | 5 | 44 | Archard Law（5 篇） · Monte Carlo（4 篇） · sensitivity analysis（4 篇） · Bayesian（3 篇） · Gaussian Distribution（2 篇） · correlation coefficient（2 篇） · differential equation（2 篇） · hypothesis test（2 篇） · machine learning（2 篇） · partial differential equation（2 篇） · particle swarm optimization（2 篇） · CNN（1 篇） · Central Limit Theorem（1 篇） · Credible Intervals（1 篇） · Gaussian Mixture Algorithm（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Navier-Stokes（1 篇） · Uncertainty Quantification（1 篇） · Weathering Degree Model（1 篇） · cross-validation（1 篇） · feature selection（1 篇） · finite difference（1 篇） · linear regression（1 篇） · system dynamics（1 篇） |
| 15 | 7 分类与聚类 · 7.1 监督分类/识别 | 面板 | 核心 | 2025 C | 18 | 280 | sensitivity analysis（16 篇） · machine learning（14 篇） · random forest（13 篇） · time series analysis（12 篇） · decision tree（11 篇） · linear regression（11 篇） · logistic regression（10 篇） · Bayesian（9 篇） · cross-validation（9 篇） · Monte Carlo（8 篇） · XGBoost（8 篇） · neural network（8 篇） · Regression Analysis（7 篇） · difference-in-differences（7 篇） · bootstrap（6 篇） · cluster analysis（6 篇） · correlation coefficient（6 篇） · stacking（6 篇） · ARIMA（5 篇） · deep learning（5 篇） · LSTM（4 篇） · SHAP（4 篇） · Tobit（4 篇） · feature selection（4 篇） · gradient boosting（4 篇） · hurdle model（4 篇） · hypothesis test（4 篇） · moving average（4 篇） · principal component analysis（4 篇） · zero-inflated（4 篇） · Causal Inference（3 篇） · Cox proportional hazards（3 篇） · Markov chain（3 篇） · Markov chain Monte Carlo（3 篇） · SVM（3 篇） · Uncertainty Quantification（3 篇） · K-means（2 篇） · SARIMA（2 篇） · SVR（2 篇） · lasso（2 篇） · propensity score matching（2 篇） · BP neural network（1 篇） · Bayesian network（1 篇） · CNN（1 篇） · Credible Intervals（1 篇） · GSRF（1 篇） · Gaussian Distribution（1 篇） · LR-SCAD Model（1 篇） · Laplace smoothing（1 篇） · Mann-Kendall（1 篇） · Mixed-effects Model（1 篇） · Posterior inference（1 篇） · RNN（1 篇） · Residual Analysis（1 篇） · Shannon entropy（1 篇） · Threshold Method（1 篇） · TrueSkill（1 篇） · analysis of variance（1 篇） · association rules（1 篇） · centrality（1 篇） · change-point detection（1 篇） · exponential smoothing（1 篇） · factor analysis（1 篇） · genetic algorithm（1 篇） · grey prediction（1 篇） · grey relational analysis（1 篇） · isolation forest（1 篇） · particle swarm optimization（1 篇） · probit（1 篇） · regression discontinuity（1 篇） · reinforcement learning（1 篇） · ridge regression（1 篇） · self-organizing map（1 篇） · spatio-temporal modeling（1 篇） · survival analysis（1 篇） · two-stage least squares（1 篇） |
| 16 | 7 分类与聚类 · 7.2 无监督聚类/分段 | 混合 | 核心 | 2025 F | 5 | 44 | Regression Analysis（4 篇） · difference-in-differences（4 篇） · cluster analysis（3 篇） · machine learning（3 篇） · principal component analysis（3 篇） · sensitivity analysis（3 篇） · K-means（2 篇） · correlation coefficient（2 篇） · factor analysis（2 篇） · linear regression（2 篇） · structural equation modeling（2 篇） · time series analysis（2 篇） · Bayesian（1 篇） · Causal Inference（1 篇） · Cox proportional hazards（1 篇） · KDMF（1 篇） · MIC（1 篇） · VBGMM（1 篇） · cross-validation（1 篇） · hypothesis test（1 篇） · integer programming（1 篇） · logistic regression（1 篇） · network analysis（1 篇） · survival analysis（1 篇） |
| 17 | 8 网络与图 · 8.2 流量分配/路由 | 网络 | 核心 | 2025 D | 4 | 40 | sensitivity analysis（4 篇） · shortest path（4 篇） · centrality（3 篇） · Monte Carlo（2 篇） · entropy weight method（2 篇） · A* and GA（1 篇） · A-star（1 篇） · BP neural network（1 篇） · Bayesian（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Multi-layer network model（1 篇） · Pareto（1 篇） · TOPSIS（1 篇） · Wardrop（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · fuzzy logic（1 篇） · genetic algorithm（1 篇） · graph theory（1 篇） · machine learning（1 篇） · minimum spanning tree（1 篇） · network analysis（1 篇） · network flow（1 篇） · nonlinear programming（1 篇） · queueing theory（1 篇） · three-layer bus network model（1 篇） |
| 18 | 9 决策与博弈 · 9.1 多准则决策 | 无数据(纯机理/假设) | 附带 | 2025 E | 4 | 38 | Food web model（4 篇） · sensitivity analysis（4 篇） · Lotka-Volterra（3 篇） · differential equation（3 篇） · system dynamics（3 篇） · entropy weight method（2 篇） · logistic regression（2 篇） · AHP（1 篇） · COMAP Model（1 篇） · Convex Reformulation（1 篇） · FATE Model（1 篇） · Petri net（1 篇） · Petri-Food Web model（1 篇） · Shannon entropy（1 篇） · centrality（1 篇） · differential evolution（1 篇） · fuzzy comprehensive evaluation（1 篇） · graph theory（1 篇） · multi-objective optimization（1 篇） · multi-type Holling responses（1 篇） · nonlinear programming（1 篇） · partial differential equation（1 篇） · shortest path（1 篇） · time series analysis（1 篇） |
| 19 | 9 决策与博弈 · 9.1 多准则决策 | 网络 | 核心 | 2025 D | 4 | 40 | sensitivity analysis（4 篇） · shortest path（4 篇） · centrality（3 篇） · Monte Carlo（2 篇） · entropy weight method（2 篇） · A* and GA（1 篇） · A-star（1 篇） · BP neural network（1 篇） · Bayesian（1 篇） · Markov chain（1 篇） · Markov chain Monte Carlo（1 篇） · Multi-layer network model（1 篇） · Pareto（1 篇） · TOPSIS（1 篇） · Wardrop（1 篇） · cluster analysis（1 篇） · correlation coefficient（1 篇） · dynamic programming（1 篇） · factor analysis（1 篇） · fuzzy comprehensive evaluation（1 篇） · fuzzy logic（1 篇） · genetic algorithm（1 篇） · graph theory（1 篇） · machine learning（1 篇） · minimum spanning tree（1 篇） · network analysis（1 篇） · network flow（1 篇） · nonlinear programming（1 篇） · queueing theory（1 篇） · three-layer bus network model（1 篇） |

> **读法**：「论文数」= 该桶里出现过的**不同论文**数；「(模型,篇) 对」= 该桶里**不同 `(模型, 篇)` 对**的条数。后者 ≥ 前者（一篇在一个桶里可以用多个模型）；两者都由下一小节的**去重指针行**按「所属桶」列**反推**得出（判据 M-2 两向判）。

### 第二节 · 指针（**按 `(模型, 篇)` 去重**，每条一行）

**这一小节就是「配对」的全集**：**496** 行，每行 = 一个 `(模型, 篇)` 对。同一个对**只出现一次**；它落在哪几个桶由**末列「所属桶」**给出（桶号 = 上一节表里的「桶」列，逗号分隔、升序）。**上一版把同一个对在每个桶里各抄一遍（1644 行），去重后是这一版**——判据 M-13 判的就是「去重后的对集合 ↔ `TAGS.md` 二层的对集合」两向相等，以及每行的「所属桶」与标注推出的桶集合相等。

格式：末列之前与 `TAGS.md` 二层**逐字相同**，前面多一个 `篇` 字段，末尾多一个桶号列：
`- <模型>; <稳定 ID>; p<页>; <md 文件（仓库相对）>; <md 整行逐字>; <桶号,桶号,…>`（`; ` 是分隔符，值内的 `;`/`|`/反斜杠/NUL/CR/LF 按 `TAGS.md` 同一套规则转义）。

- A* and GA; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; of accessibility considered for each stakeholder. We used a method combining A* and GA to; 5,7,17,19
- A-star; P2025-D-01; p10; corpus/papers/md/2025美赛O奖论文/D/2504188.md; **specific calculation process, we innovatively combine the A* algorithm with the**; 5,7,17,19
- AHP; P2025-B-03; p1; corpus/papers/md/2025美赛O奖论文/B/2503268.md; for each main factor combined with Analytic Hierarchy Process (AHP) to attain the comprehen-; 2,6,10,13
- AHP; P2025-B-07; p1; corpus/papers/md/2025美赛O奖论文/B/2517929.md; analysis, the analytic hierarchy process (AHP) were used to construct the objective functions.; 2,6,10,13
- AHP; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; benefits. An EWM-AHP model is developed to assess these schemes for organic farming.; 2,6,9,18
- ARIMA; P2025-B-01; p12; corpus/papers/md/2025美赛O奖论文/B/2501687.md; The estimation of the unemployment rate growth utilized the ARIMA (p, d, q) model.; 2,6,10,13
- ARIMA; P2025-C-04; p28; corpus/papers/md/2025美赛O奖论文/C/2505964.md; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal; 1,3,11,15
- ARIMA; P2025-C-05; p6; corpus/papers/md/2025美赛O奖论文/C/2507817.md; 5.1.1 ARIMA Model Initial Prediction; 1,3,11,15
- ARIMA; P2025-C-06; p1; corpus/papers/md/2025美赛O奖论文/C/2510006.md; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**; 1,3,11,15
- ARIMA; P2025-C-11; p7; corpus/papers/md/2025美赛O奖论文/C/2514461.md; methods can be employed to forecast the number of events in the 2028 Games. While ARIMA; 1,3,11,15
- ARIMA; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; SARIMAX and ARIMA to predict future trends in the number of events. Secondly, to handle; 1,3,11,15
- Archard Law; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; stair usage frequency. Given the known distribution of wear depth, and based on Archard's Law, we; 8,13,14
- Archard Law; P2025-A-02; p1; corpus/papers/md/2025美赛O奖论文/A/2501567.md; **In Task 1, we establish a model based on Archard’s Wear Law and Human Behavior**; 8,13,14
- Archard Law; P2025-A-03; p1; corpus/papers/md/2025美赛O奖论文/A/2501909.md; matrix. Based on this matrix and Archard Wear Law, we develop the WVM. We introducing; 8,13,14
- Archard Law; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## Sub-model i, grounded in Archard’s theory and PDEs, provides a probabilistic equa-; 8,13,14
- Archard Law; P2025-A-05; p1; corpus/papers/md/2025美赛O奖论文/A/2511565.md; Second, we build a Daily Foot Traffic Model based on the Archard equation. We take Ar-; 8,13,14
- BP neural network; P2025-C-07; p1; corpus/papers/md/2025美赛O奖论文/C/2510185.md; Then, to predict medal acquisition by medal-less nations/regions, we employ a BP neural; 1,3,11,15
- BP neural network; P2025-D-01; p10; corpus/papers/md/2025美赛O奖论文/D/2504188.md; BP; 5,7,17,19
- Bayesian; P2025-A-02; p1; corpus/papers/md/2025美赛O奖论文/A/2501567.md; and Bayesian Information Criterion to analyze the direction and usage pattern of stair-; 8,13,14
- Bayesian; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## cal insights in a Bayesian framework by assigning prior distributions to multiple pa-; 8,13,14
- Bayesian; P2025-A-05; p1; corpus/papers/md/2025美赛O奖论文/A/2511565.md; use Bayesian Inversion Framework to calculate the construction time to provide essential param-; 8,13,14
- Bayesian; P2025-C-01; p25; corpus/papers/md/2025美赛O奖论文/C/2500759.md; [8] Tui H Nolan, Jeff Goldsmith, and David Ruppert. Bayesian functional principal; 1,3,11,15
- Bayesian; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; In Question 2, the Bayesian Change-point Detection method is used to identify significant; 1,3,11,15
- Bayesian; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; ## A Glimpse of Olympics Medals through Bayesian Model; 1,3,11,15
- Bayesian; P2025-C-10; p1; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Bayesian modiﬁed entropy. By introducing the Laplace smoothing technique to recon-; 1,3,11,15
- Bayesian; P2025-C-13; p9; corpus/papers/md/2025美赛O奖论文/C/2516178.md; ploy the Bayesian algorithm, specifically the Tree-structured Parzen Estimator (TPE), to de-; 1,3,11,15
- Bayesian; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; ## "Golden Dynamics: Bayesian-AI Olympic Forecasting with; 1,3,11,15
- Bayesian; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; 2028. The host country factor was considered in this step. To account for potential errors, a Bayesian; 1,3,11,15
- Bayesian; P2025-C-17; p10; corpus/papers/md/2025美赛O奖论文/C/2522820.md; We decided to use Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) as; 1,3,11,15
- Bayesian; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; **regression model (ZINB). Adopting a Bayesian framework, we employ the Markov**; 1,3,11,15
- Bayesian; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; trian infrastructure (xp), and micro-mobility hubs (xm). The model employs Bayesian; 5,7,17,19
- Bayesian; P2025-F-01; p2; corpus/papers/md/2025美赛O奖论文/F/2504223.md; Variational Bayesian Gaussian Mixture Clustering . . . . . . . . . . . . .; 4,12,16
- Bayesian network; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; coaches critically influence outcomes. We propose SBN-DBN, a Bayesian model inte-; 1,3,11,15
- CNN; P2025-A-05; p3; corpus/papers/md/2025美赛O奖论文/A/2511565.md; machine learning, specifically CNN models [5], to train data and obtain rail wear amounts have; 8,13,14
- CNN; P2025-C-14; p25; corpus/papers/md/2025美赛O奖论文/C/2516695.md; monthly gas field production based on the CNN - LSTM model. Energy, 260,; 1,3,11,15
- COMAP Model; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; Keywords: FATE Model\; COMAP Model\; Lotka-Volterra Equation\; Eco-Agriculture；; 2,6,9,18
- CVM; P2025-B-01; p1; corpus/papers/md/2025美赛O奖论文/B/2501687.md; **gramming Model based on Contingent Valuation Method(CVM) and Particle Swarm**; 2,6,10,13
- Causal Inference; P2025-C-02; p2; corpus/papers/md/2025美赛O奖论文/C/2501869.md; **Change-Point Detection and Causal Inference Models**; 1,3,11,15
- Causal Inference; P2025-C-10; p6; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Difference-in-Differences (causal inference method); 1,3,11,15
- Causal Inference; P2025-C-14; p15; corpus/papers/md/2025美赛O奖论文/C/2516695.md; G-Coach Impact Quantifier (GCIQ), a hybrid causal inference framework integrating; 1,3,11,15
- Causal Inference; P2025-F-02; p1; corpus/papers/md/2025美赛O奖论文/F/2507789.md; governance. By integrating clustering analysis, causal inference, and network analysis, this; 4,12,16
- Central Limit Theorem; P2025-A-03; p1; corpus/papers/md/2025美赛O奖论文/A/2501909.md; WDM based on the Central Limit Theorem. It calculate the marginal distribution of the wear; 8,13,14
- Convex Reformulation; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; by using the Convex Reformulation Method to trade-off the ecological benefits (biodiversity; 2,6,9,18
- Cox proportional hazards; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; 2028. We employed the Cox Proportional Hazard Model, with its risk function representing the possibility that a; 1,3,11,15
- Cox proportional hazards; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; Model I: Hierarchical Adaptive Reasoning Model (HARMONIE) Model II: Cox Haz-; 1,3,11,15
- Cox proportional hazards; P2025-C-18; p22; corpus/papers/md/2025美赛O奖论文/C/2524070.md; reveals a noticeable trend. To address this issue, we apply the Box-Cox transformation in an effort to; 1,3,11,15
- Cox proportional hazards; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; **Keywords: VBGMM\; DID Model\; Cox TVPH\; SEM**; 4,12,16
- Credible Intervals; P2025-A-04; p17; corpus/papers/md/2025美赛O奖论文/A/2504218.md; Finally, we use a Quantile-based Method to construct credible intervals. Specifically, we sort the; 8,13,14
- Credible Intervals; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; based posterior inference provides 95% credible intervals, assessing both medal forecasts; 1,3,11,15
- FATE Model; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; Keywords: FATE Model\; COMAP Model\; Lotka-Volterra Equation\; Eco-Agriculture；; 2,6,9,18
- Food web model; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; complex food web model. This includes the introduction of pesticide and herbicide, followed; 2,6,9,18
- Food web model; P2025-E-02; p4; corpus/papers/md/2025美赛O奖论文/E/2508861.md; model, and food web model, with their respective strengths and limitations shown in Figure 2.; 2,6,9,18
- Food web model; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; Keywords: Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger-; 2,6,9,18
- Food web model; P2025-E-04; p6; corpus/papers/md/2025美赛O奖论文/E/2517273.md; Assumption2: In this food web model, we assume that sparrows and bats exclusively feed on; 2,6,9,18
- GSRF; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; For Task 1, we developed a Grid-Search Random Forest (GSRF) prediction model; 1,3,11,15
- Gaussian Distribution; P2025-A-02; p1; corpus/papers/md/2025美赛O奖论文/A/2501567.md; number of mixture Gaussian distribution, can be accessed by minimizing Bayesian Infor-; 8,13,14
- Gaussian Distribution; P2025-A-04; p13; corpus/papers/md/2025美赛O奖论文/A/2504218.md; Here, (δx, δy) can be drawn from a Gaussian distribution N((x0, y0), Σ) to reflect that each footstep; 8,13,14
- Gaussian Distribution; P2025-C-16; p7; corpus/papers/md/2025美赛O奖论文/C/2521556.md; 𝑖. The initial Skill is drawn from a Gaussian distribution with mean 𝑚0; 1,3,11,15
- Gaussian Mixture Algorithm; P2025-A-03; p1; corpus/papers/md/2025美赛O奖论文/A/2501909.md; Keywords: Stair Wear, Archard Law, Central Limit Theorem, Gaussian Mixture Algorithm; 8,13,14
- K-means; P2025-C-06; p6; corpus/papers/md/2025美赛O奖论文/C/2510006.md; **K-means clustering uses these rates to group similar**; 1,3,11,15
- K-means; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; significant at the 2% level. K-Means clustering identified Spain, Japan, and Canada as na-; 1,3,11,15
- K-means; P2025-F-02; p1; corpus/papers/md/2025美赛O奖论文/F/2507789.md; The first model employs K-means clustering to categorize nations based on cybersecurity; 4,12,16
- K-means; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; **Key words: Cybercrime, KDMF, K-means, DID, MIC, Policy**; 4,12,16
- KDMF; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; ## Cracking the Cyber - Puzzle: KDMF in Action; 4,12,16
- L-BFGS-B algorithm; P2025-B-06; p1; corpus/papers/md/2025美赛O奖论文/B/2509557.md; on tourism sustainability and identify optimal strategies. Using the L-BFGS-B algorithm, we de-; 2,6,10,13
- LR-SCAD Model; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; we introduced LR-SCAD model to study how the “great coach” effect contributed to changes in the; 1,3,11,15
- LSTM; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; ory (LSTM) networks to mine temporal features and integrate home advantage effects.; 1,3,11,15
- LSTM; P2025-C-09; p22; corpus/papers/md/2025美赛O奖论文/C/2513314.md; [3] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural Computation,; 1,3,11,15
- LSTM; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; We first attempted at a plain Long Short Term Memory (LSTM) model. We employed the technique of the; 1,3,11,15
- LSTM; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; scenarios show asymmetric US-China declines (-12.7% vs. -9.3%). Extending LSTM; 1,3,11,15
- Laplace smoothing; P2025-C-10; p1; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Bayesian modiﬁed entropy. By introducing the Laplace smoothing technique to recon-; 1,3,11,15
- Lotka-Volterra; P2025-B-03; p1; corpus/papers/md/2025美赛O奖论文/B/2503268.md; and economy, respectively. Inspired by the Lotka-Volterra model, logistic population model, and; 2,6,10,13
- Lotka-Volterra; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; In Model I, the biggest innovation is the combination of the Lotka-Volterra model with; 2,6,9,18
- Lotka-Volterra; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; (PFW) Model, drawing upon the principles of Petri nets, Lotka-Volterra theory, and energy; 2,6,9,18
- Lotka-Volterra; P2025-E-04; p1; corpus/papers/md/2025美赛O奖论文/E/2517273.md; capturing saturation effects, Holling Type III for predator-prey dynamics between ladybugs and aphids; 2,6,9,18
- MIC; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; we used the Maximal Information Coefficient (MIC) method and factor analysis. The results; 4,12,16
- Mann-Kendall; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Keywords: Threshold Method, SVR, XGBoost, LSTM, Mann-Kendall, Cox, Isolation Forest, Linear Regression,; 1,3,11,15
- Markov chain; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,; 8,13,14
- Markov chain; P2025-C-01; p5; corpus/papers/md/2025美赛O奖论文/C/2500759.md; memoryless characteristic of Olympic medal trends akin to Markov chains, we employ an; 1,3,11,15
- Markov chain; P2025-C-09; p9; corpus/papers/md/2025美赛O奖论文/C/2513314.md; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,; 1,3,11,15
- Markov chain; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; **regression model (ZINB). Adopting a Bayesian framework, we employ the Markov**; 1,3,11,15
- Markov chain; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**; 5,7,17,19
- Markov chain Monte Carlo; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,; 8,13,14
- Markov chain Monte Carlo; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; specific regression coefficients and a Gamma-distributed concentration parameter. MCMC-; 1,3,11,15
- Markov chain Monte Carlo; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; MCMC sampling, we forecasted the 2028 LA Olympics medal distribution with pre-; 1,3,11,15
- Markov chain Monte Carlo; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; Chain Monte Carlo (MCMC) method to derive the posterior distribution of the model; 1,3,11,15
- Markov chain Monte Carlo; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**; 5,7,17,19
- Mixed-effects Model; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; a mixed-effects model. In this model, the pairing of coach and country is treated as a; 1,3,11,15
- Monte Carlo; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; the Monte Carlo method to estimate the stair age, yielding a range of approximately (282.1984,; 8,13,14
- Monte Carlo; P2025-A-02; p1; corpus/papers/md/2025美赛O奖论文/A/2501567.md; **In Task 3, we develop a model combining Monte Carlo simulations and Smooth-**; 8,13,14
- Monte Carlo; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,; 8,13,14
- Monte Carlo; P2025-A-05; p14; corpus/papers/md/2025美赛O奖论文/A/2511565.md; After considering all the above factors, we wrote a Python program using the Monte Carlo; 8,13,14
- Monte Carlo; P2025-B-01; p17; corpus/papers/md/2025美赛O奖论文/B/2501687.md; we use the Monte Carlo Method to select 101 values at equal intervals with a step size of; 2,6,10,13
- Monte Carlo; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; validated by Monte Carlo simulations, with a 95% confidence interval of 1.00–8.00.; 1,3,11,15
- Monte Carlo; P2025-C-04; p1; corpus/papers/md/2025美赛O奖论文/C/2505964.md; athlete data and various models, including random forest, Monte Carlo simulation,; 1,3,11,15
- Monte Carlo; P2025-C-06; p1; corpus/papers/md/2025美赛O奖论文/C/2510006.md; and new events. For new events, we used Monte Carlo simulations to estimate medal; 1,3,11,15
- Monte Carlo; P2025-C-09; p9; corpus/papers/md/2025美赛O奖论文/C/2513314.md; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,; 1,3,11,15
- Monte Carlo; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Monte-Carlo simulations, we predicted the potential number of first-time medalists by 2028. 3 is the most likely; 1,3,11,15
- Monte Carlo; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; ard Analysis and Monte Carlo Prediction Model (CHAMPS) Model III: G - Coach Im-; 1,3,11,15
- Monte Carlo; P2025-C-16; p13; corpus/papers/md/2025美赛O奖论文/C/2521556.md; So, how many countries are most likely to win medals in 2028? We conducted a Monte Carlo; 1,3,11,15
- Monte Carlo; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; Chain Monte Carlo (MCMC) method to derive the posterior distribution of the model; 1,3,11,15
- Monte Carlo; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; and original stations. Since the area is irregular, we used Monte Carlo Simulations to calculate; 5,7,17,19
- Monte Carlo; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**; 5,7,17,19
- Multi-layer network model; P2025-D-04; p1; corpus/papers/md/2025美赛O奖论文/D/2519935.md; The proposed multi-layer network model exhibited strong robustness and stability, as con-; 5,7,17,19
- NSGA-II; P2025-B-05; p1; corpus/papers/md/2025美赛O奖论文/B/2505199.md; the Non - dominated Sorting Genetic Algorithm II (NSGA - II) is employed to solve the; 2,6,10,13
- NSGA-II; P2025-B-07; p1; corpus/papers/md/2025美赛O奖论文/B/2517929.md; The NSGA-II Algorithm was applied to search for the Pareto-optimal solution set. Taking the; 2,6,10,13
- Navier-Stokes; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; continuity equation for simulating pedestrian flow was established based on Navier-Stokes Equations.; 8,13,14
- Pareto; P2025-B-02; p1; corpus/papers/md/2025美赛O奖论文/B/2502617.md; ## Overload Alarm: Pareto Optimization of the; 2,6,10,13
- Pareto; P2025-B-05; p4; corpus/papers/md/2025美赛O奖论文/B/2505199.md; for hierarchical search, gets Pareto optimal solutions, maintains population diversity with; 2,6,10,13
- Pareto; P2025-B-07; p1; corpus/papers/md/2025美赛O奖论文/B/2517929.md; The NSGA-II Algorithm was applied to search for the Pareto-optimal solution set. Taking the; 2,6,10,13
- Pareto; P2025-D-03; p22; corpus/papers/md/2025美赛O奖论文/D/2516219.md; methods: Pareto frontier analysis of (f1, f2, f3); 5,7,17,19
- Petri net; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; (PFW) Model, drawing upon the principles of Petri nets, Lotka-Volterra theory, and energy; 2,6,9,18
- Petri-Food Web model; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; Keywords: Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger-; 2,6,9,18
- Posterior inference; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; based posterior inference provides 95% credible intervals, assessing both medal forecasts; 1,3,11,15
- RNN; P2025-C-09; p7; corpus/papers/md/2025美赛O奖论文/C/2513314.md; machine learning methods (e.g., RNN and two-stage RF) are clearly unsuitable, as they fail; 1,3,11,15
- Regression Analysis; P2025-B-01; p12; corpus/papers/md/2025美赛O奖论文/B/2501687.md; *Figure 6: Linear regression analysis of the population and median income in Juneau*; 2,6,10,13
- Regression Analysis; P2025-B-07; p6; corpus/papers/md/2025美赛O奖论文/B/2517929.md; at the same time, a stable tourist count provides reliable inputs to the regression analysis; 2,6,10,13
- Regression Analysis; P2025-C-03; p11; corpus/papers/md/2025美赛O奖论文/C/2503389.md; *Table 5: Key Metrics and Results of Regression Analysis*; 1,3,11,15
- Regression Analysis; P2025-C-04; p16; corpus/papers/md/2025美赛O奖论文/C/2505964.md; Using regression analysis on data from 1896 to 2024, the study addresses two key questions: 1.; 1,3,11,15
- Regression Analysis; P2025-C-08; p21; corpus/papers/md/2025美赛O奖论文/C/2510862.md; *Table 2: DID regression analysis results*; 1,3,11,15
- Regression Analysis; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; Quantification, Regression Analysis, Credible Intervals; 1,3,11,15
- Regression Analysis; P2025-C-11; p8; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Weconducted regression analysis on the number of past events insummerOly_programs.csv; 1,3,11,15
- Regression Analysis; P2025-C-13; p20; corpus/papers/md/2025美赛O奖论文/C/2516178.md; Based on the results of the Ordinary Least Squares (OLS) regression analysis, the model; 1,3,11,15
- Regression Analysis; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; Maximum Likelihood Estimate. From regression analysis on the Tobit Model, we discovered it suffered from; 1,3,11,15
- Regression Analysis; P2025-F-01; p24; corpus/papers/md/2025美赛O奖论文/F/2504223.md; ative Infection Based on Logistic Multiple Regression Analysis in the Assess-; 4,12,16
- Regression Analysis; P2025-F-02; p19; corpus/papers/md/2025美赛O奖论文/F/2507789.md; ## 6.3.1 Panel Regression Analysis; 4,12,16
- Regression Analysis; P2025-F-03; p16; corpus/papers/md/2025美赛O奖论文/F/2513705.md; Table 3 Results of OLS Regression Analysis of Data Protection and Privacy Regulations; 4,12,16
- Regression Analysis; P2025-F-05; p12; corpus/papers/md/2025美赛O奖论文/F/2521039.md; merged into a complete analytical sample. In the regression analysis, the model treated; 4,12,16
- Residual Analysis; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; For Task 2, we performed residual analysis to find evidence of how coaches influence athletes’; 1,3,11,15
- SARIMA; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; SARIMAX and ARIMA to predict future trends in the number of events. Secondly, to handle; 1,3,11,15
- SARIMA; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; counts. We built a bottom-up medal analysis and prediction model using the TrueSkill-SARIMAX-; 1,3,11,15
- SHAP; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; athletics, and medal counts, while SHapley Additive exPlanations (SHAP) quantifies; 1,3,11,15
- SHAP; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; SHAP analysis revealed that for the U.S., Athletics and Rugby-related events contributed; 1,3,11,15
- SHAP; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; event dynamics, and the inﬂuence of elite coaching. Shi et al.(2024) used SHAP method to; 1,3,11,15
- SHAP; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; small Olympic countries. Simultaneously, SHAP value analysis was utilized to uncover the; 1,3,11,15
- SIS model; P2025-B-03; p1; corpus/papers/md/2025美赛O奖论文/B/2503268.md; SIS model, we developed the Sustainable Tourism Dynamics Model (STDM). This system uses; 2,6,10,13
- SLSQP; P2025-B-02; p1; corpus/papers/md/2025美赛O奖论文/B/2502617.md; among them. Using the SLSQP method, we determine the global Pareto-optimal solution for; 2,6,10,13
- SVM; P2025-C-07; p7; corpus/papers/md/2025美赛O奖论文/C/2510185.md; **SVM**; 1,3,11,15
- SVM; P2025-C-08; p7; corpus/papers/md/2025美赛O奖论文/C/2510862.md; (LGBM, SVM, XGBoost, and RF) into a final prediction model. Each base learner; 1,3,11,15
- SVM; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Linear Regression, Random Forest, Support Vector Machines and Neural Networks. They are; 1,3,11,15
- SVR; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; ﬂuctuations. Zhao et al.(2012) improved accuracy by optimizing v-SVR parameters with; 1,3,11,15
- SVR; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; avoiding overgeneralizing to the level of sports. We employed Support Vector Regression (SVR) instead of Linear; 1,3,11,15
- Shannon entropy; P2025-C-10; p26; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Query2:Explain information entropy.; 1,3,11,15
- Shannon entropy; P2025-E-03; p21; corpus/papers/md/2025美赛O奖论文/E/2515136.md; Then, the information entropy of the jth indicator is calculated by the following formula.; 2,6,9,18
- TOPSIS; P2025-D-04; p1; corpus/papers/md/2025美赛O奖论文/D/2519935.md; ment of new bus lines. Firstly we use the entropy-weight-TOPSIS method incorporating both; 5,7,17,19
- Threshold Method; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; In Model IV, we addressed the Great Coach Effect (GCE). We developed a Threshold Method, filtering first-; 1,3,11,15
- Tobit; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; ## Medal Prediction Based on Tobit and Hurdle Models; 1,3,11,15
- Tobit; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; model, which combines the Mundlak-modified Tobit regression model with the Hurdle; 1,3,11,15
- Tobit; P2025-C-13; p3; corpus/papers/md/2025美赛O奖论文/C/2516178.md; transformation of the Tobit model and the Hurdle model are the most emblematic. Simultane-; 1,3,11,15
- Tobit; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; first consider a Tobit Model that considers random noise and unobserved random effects, optimized with a; 1,3,11,15
- TrueSkill; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; counts. We built a bottom-up medal analysis and prediction model using the TrueSkill-SARIMAX-; 1,3,11,15
- Uncertainty Quantification; P2025-A-04; p19; corpus/papers/md/2025美赛O奖论文/A/2504218.md; posterior uncertainty quantification” under limited computational overhead. It aligns the simulated; 8,13,14
- Uncertainty Quantification; P2025-C-04; p2; corpus/papers/md/2025美赛O奖论文/C/2505964.md; Monte Carlo Simulation and Uncertainty Quantification; 1,3,11,15
- Uncertainty Quantification; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; A key strength of this model is its robust uncertainty quantification. Each country’s; 1,3,11,15
- Uncertainty Quantification; P2025-C-14; p24; corpus/papers/md/2025美赛O奖论文/C/2516695.md; Probabilistic calibration is validated by uncertainty quantification achieving 93.2%; 1,3,11,15
- VBGMM; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; areas with low GCI scores. Then, a VBGMM model is established to cluster countries; 4,12,16
- Wardrop; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **dynamics are analyzed through Wardrop equilibrium-based traffic assignment and**; 5,7,17,19
- Weathering Degree Model; P2025-A-05; p1; corpus/papers/md/2025美赛O奖论文/A/2511565.md; Key Words: Stair Wear, Archard Equation, Depth Estimation, Weathering Degree Model,; 8,13,14
- XGBoost; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; A dual-channel XGBoost-Bootstrap model is established to generate predictions with; 1,3,11,15
- XGBoost; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; were significantly better than the machine learning methods (random forest and XGboost) in; 1,3,11,15
- XGBoost; P2025-C-07; p7; corpus/papers/md/2025美赛O奖论文/C/2510185.md; **XGBoost**; 1,3,11,15
- XGBoost; P2025-C-08; p7; corpus/papers/md/2025美赛O奖论文/C/2510862.md; (LGBM, SVM, XGBoost, and RF) into a final prediction model. Each base learner; 1,3,11,15
- XGBoost; P2025-C-09; p10; corpus/papers/md/2025美赛O奖论文/C/2513314.md; **XGBoost[1]**; 1,3,11,15
- XGBoost; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; turned to an advanced XGBoost model. In this model, we predicted fractions instead of numbers, and multiplied; 1,3,11,15
- XGBoost; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; First, following model screening, we developed a dual-stage XGBoost model for pre-; 1,3,11,15
- XGBoost; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; Regression, XGBoost Regression and Neural Network Regression models respectively, and; 1,3,11,15
- analysis of variance; P2025-C-18; p2; corpus/papers/md/2025美赛O奖论文/C/2524070.md; Analysis of Variance, Mixed-effects Model . . . . . . . . . . . . . . . . . . . . . . .; 1,3,11,15
- association rules; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; consequent, which led to the identification of five strong association rules. Furthermore,; 1,3,11,15
- bootstrap; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; A dual-channel XGBoost-Bootstrap model is established to generate predictions with; 1,3,11,15
- bootstrap; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; Network Bootstrap Ensemble Interval Model incorporating features such as the host boost,; 1,3,11,15
- bootstrap; P2025-C-07; p1; corpus/papers/md/2025美赛O奖论文/C/2510185.md; quently, we employ the RF model with bootstrapping to generate 95% confidence intervals for; 1,3,11,15
- bootstrap; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; We also calculated 95% confidence intervals using the Bootstrap method. The findings; 1,3,11,15
- bootstrap; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; tainty quantiﬁcation through asymmetric bootstrap intervals and actionable insights into; 1,3,11,15
- bootstrap; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; estimation was conducted using the non-parametric Bootstrap method. After 1000 iterative ver-; 1,3,11,15
- centrality; P2025-C-14; p18; corpus/papers/md/2025美赛O奖论文/C/2516695.md; ployed to identify key paths. The results show that Russia (node degree centrality; 1,3,11,15
- centrality; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; Centrality and Degree Centrality, identifying areas in need of optimization. We then created a; 5,7,17,19
- centrality; P2025-D-03; p9; corpus/papers/md/2025美赛O奖论文/D/2516219.md; resilience through topological-flow synthesis. Edge betweenness centrality quantifies; 5,7,17,19
- centrality; P2025-D-04; p1; corpus/papers/md/2025美赛O奖论文/D/2519935.md; subnetwork using critical nodes of the highway network, and compute the proximity centrality; 5,7,17,19
- centrality; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; icides, and the inclusion of bats and bees. The stability, biodiversity, and centrality indicators; 2,6,9,18
- change-point detection; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; In Question 2, the Bayesian Change-point Detection method is used to identify significant; 1,3,11,15
- cluster analysis; P2025-B-03; p11; corpus/papers/md/2025美赛O奖论文/B/2503268.md; cated by the tight clustering of observed data along the model trajectories in the (NJuneau, TJuneau); 2,6,10,13
- cluster analysis; P2025-C-01; p25; corpus/papers/md/2025美赛O奖论文/C/2500759.md; autoencoder-based arithmetic optimization clustering algorithm to enhance principal; 1,3,11,15
- cluster analysis; P2025-C-06; p2; corpus/papers/md/2025美赛O奖论文/C/2510006.md; Clustering Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 1,3,11,15
- cluster analysis; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; significant at the 2% level. K-Means clustering identified Spain, Japan, and Canada as na-; 1,3,11,15
- cluster analysis; P2025-C-11; p28; corpus/papers/md/2025美赛O奖论文/C/2514461.md; models like group or cluster analysis methods to account for these dependencies.; 1,3,11,15
- cluster analysis; P2025-C-12; p14; corpus/papers/md/2025美赛O奖论文/C/2515235.md; continents is more scattered, with no clear regional clustering of improvements.5.3.3：Ana-; 1,3,11,15
- cluster analysis; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; Country performance was split into clusters using Density-Based Spatial Clustering of Applications with; 1,3,11,15
- cluster analysis; P2025-D-02; p1; corpus/papers/md/2025美赛O奖论文/D/2507692.md; ## on Graph Theory & Clustering Algorithm; 5,7,17,19
- cluster analysis; P2025-F-01; p2; corpus/papers/md/2025美赛O奖论文/F/2504223.md; Variational Bayesian Gaussian Mixture Clustering . . . . . . . . . . . . .; 4,12,16
- cluster analysis; P2025-F-02; p1; corpus/papers/md/2025美赛O奖论文/F/2507789.md; governance. By integrating clustering analysis, causal inference, and network analysis, this; 4,12,16
- cluster analysis; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; Cybercrime Reporting Rate. Through descriptive analysis and K - means clustering, we found; 4,12,16
- correlation coefficient; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; then used the Person correlation coefficient to analyze their relationship. Finally, to analyze the; 8,13,14
- correlation coefficient; P2025-A-04; p3; corpus/papers/md/2025美赛O奖论文/A/2504218.md; materials after a certain amount of wear by changing the correlation coefficient, and obtain the; 8,13,14
- correlation coefficient; P2025-B-07; p18; corpus/papers/md/2025美赛O奖论文/B/2517929.md; tion indicates the magnitude of the correlation coefficient. The closer the absolute value is to; 2,6,10,13
- correlation coefficient; P2025-C-01; p3; corpus/papers/md/2025美赛O奖论文/C/2500759.md; responding probabilities. Furthermore, Spearman correlation coefficients and SHAP are; 1,3,11,15
- correlation coefficient; P2025-C-02; p14; corpus/papers/md/2025美赛O奖论文/C/2501869.md; Subsequently, the Pearson correlation coefficients of these countries regarding the two covari-; 1,3,11,15
- correlation coefficient; P2025-C-05; p10; corpus/papers/md/2025美赛O奖论文/C/2507817.md; Correlation coefficient R2: comparing the predictions obtained using the model with the; 1,3,11,15
- correlation coefficient; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; In Task 3: We calculated Pearson correlation coefficients and used a heatmap to ana-; 1,3,11,15
- correlation coefficient; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; (participation rate) reveals a Pearson correlation coefficient of 0.416.; 1,3,11,15
- correlation coefficient; P2025-C-14; p20; corpus/papers/md/2025美赛O奖论文/C/2516695.md; events. In Figure 16, the Pearson correlation coefficient r = 0.87 (p < 0.001) vali-; 1,3,11,15
- correlation coefficient; P2025-D-02; p16; corpus/papers/md/2025美赛O奖论文/D/2507692.md; correlation coefficient to precisely measure the strength and direction of this relationship and visualized; 5,7,17,19
- correlation coefficient; P2025-F-04; p1; corpus/papers/md/2025美赛O奖论文/F/2517199.md; After that, Pearson correlation coefficient, Spearman rank correlation coefficient and; 4,12,16
- correlation coefficient; P2025-F-05; p19; corpus/papers/md/2025美赛O奖论文/F/2521039.md; tion analysis on the data, generating a Spearman correlation coefﬁcient matrix. The; 4,12,16
- cross-validation; P2025-A-05; p24; corpus/papers/md/2025美赛O奖论文/A/2511565.md; the staircase, employing cross-validation with multiple data sources to boost reliability.; 8,13,14
- cross-validation; P2025-C-01; p9; corpus/papers/md/2025美赛O奖论文/C/2500759.md; through 10-fold cross-validation grid parameter tuning, along with the estimation of con-; 1,3,11,15
- cross-validation; P2025-C-03; p14; corpus/papers/md/2025美赛O奖论文/C/2503389.md; estimated using their respective cross-validation accuracies. The table below summarizes the; 1,3,11,15
- cross-validation; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; using preprocessed data. Through Cross-Validation, we obtained correlation coefficients for; 1,3,11,15
- cross-validation; P2025-C-07; p4; corpus/papers/md/2025美赛O奖论文/C/2510185.md; **50% cross validation**; 1,3,11,15
- cross-validation; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; Finally, 10-fold cross-validation confirmed the Stacking model’s stability, while bal-; 1,3,11,15
- cross-validation; P2025-C-10; p20; corpus/papers/md/2025美赛O奖论文/C/2514362.md; †All metrics derived from 10-fold cross-validation (N=11,234 samples\; stratiﬁed sampling); 1,3,11,15
- cross-validation; P2025-C-11; p8; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Grid Search coupled with 5-fold Cross-Validation. The trained model was then employed to; 1,3,11,15
- cross-validation; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; the last-block cross-validation approach, a type of time-series cross-validation.; 1,3,11,15
- cross-validation; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; country. Through ten-fold cross-validation, we compared Random Forest Regression, Lasso; 1,3,11,15
- cross-validation; P2025-F-05; p26; corpus/papers/md/2025美赛O奖论文/F/2521039.md; **Cross-validation: Use multiple sources like OECD and national government**; 4,12,16
- decision tree; P2025-C-02; p3; corpus/papers/md/2025美赛O奖论文/C/2501869.md; ensemble learning methods based on decision trees, excel at handling non-linear relationships; 1,3,11,15
- decision tree; P2025-C-03; p13; corpus/papers/md/2025美赛O奖论文/C/2503389.md; The Random Forest model aggregates the predictions of multiple decision trees. The final pre-; 1,3,11,15
- decision tree; P2025-C-05; p8; corpus/papers/md/2025美赛O奖论文/C/2507817.md; Random forests are machine learning algorithms trained using multiple decision trees,; 1,3,11,15
- decision tree; P2025-C-06; p12; corpus/papers/md/2025美赛O奖论文/C/2510006.md; of countries winning ﬁrst medals. The ensemble of decision trees helps reduce overﬁtting, and; 1,3,11,15
- decision tree; P2025-C-07; p11; corpus/papers/md/2025美赛O奖论文/C/2510185.md; **DECISION TREE 1**; 1,3,11,15
- decision tree; P2025-C-08; p7; corpus/papers/md/2025美赛O奖论文/C/2510862.md; LightGBM is a gradient boosting algorithm based on decision trees. It gradually; 1,3,11,15
- decision tree; P2025-C-10; p26; corpus/papers/md/2025美赛O奖论文/C/2514362.md; chine learning. In ML, entropy guides decision-making: decision trees split features to min-; 1,3,11,15
- decision tree; P2025-C-11; p12; corpus/papers/md/2025美赛O奖论文/C/2514461.md; adds decision trees to optimize an objective function composed of a loss function for prediction; 1,3,11,15
- decision tree; P2025-C-13; p8; corpus/papers/md/2025美赛O奖论文/C/2516178.md; model's predicted value is the sum of the predictions from 𝐾 decision trees:; 1,3,11,15
- decision tree; P2025-C-15; p10; corpus/papers/md/2025美赛O奖论文/C/2517690.md; diction by integrating multiple decision trees; 1,3,11,15
- decision tree; P2025-C-16; p10; corpus/papers/md/2025美赛O奖论文/C/2521556.md; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for; 1,3,11,15
- deep learning; P2025-B-05; p21; corpus/papers/md/2025美赛O奖论文/B/2505199.md; ·Adopt advanced algorithms like deep learning to boost efficiency and accuracy for de-; 2,6,10,13
- deep learning; P2025-C-01; p23; corpus/papers/md/2025美赛O奖论文/C/2500759.md; pact analysis with deep learning techniques to refine medal predictions. By incorporating; 1,3,11,15
- deep learning; P2025-C-09; p4; corpus/papers/md/2025美赛O奖论文/C/2513314.md; **Deep Learning**; 1,3,11,15
- deep learning; P2025-C-14; p13; corpus/papers/md/2025美赛O奖论文/C/2516695.md; Based on a hybrid architecture of Bayesian learning and deep learning, we con-; 1,3,11,15
- deep learning; P2025-C-15; p4; corpus/papers/md/2025美赛O奖论文/C/2517690.md; deep learning in dealing with complex non-linear relationships. [3]J. Moolchandani, V. Chole,; 1,3,11,15
- deep learning; P2025-C-16; p25; corpus/papers/md/2025美赛O奖论文/C/2521556.md; [6] Deepvarma: A hybrid deep learning and varma model for chemical industry index forecasting. No; 1,3,11,15
- difference-in-differences; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; Subsequently, we develop a Difference-in-Differences (DID) model to quantify the; 1,3,11,15
- difference-in-differences; P2025-C-02; p20; corpus/papers/md/2025美赛O奖论文/C/2501869.md; methods (such as OLS, DID, and IV) and develop a parameter estimation method that eliminates; 1,3,11,15
- difference-in-differences; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; **women’s gymnastics team, focusing on coach Béla Károlyi. Using a PSM-DID model**; 1,3,11,15
- difference-in-differences; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; requires advanced methods like DID or SHAP decomposition.; 1,3,11,15
- difference-in-differences; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; ferences (DID) approach to design a dynamic DID method capable of effectively estimating; 1,3,11,15
- difference-in-differences; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; Keywords: Dual-stage XGBoost\; Non-parametric Bootstrap algorithm\; DID model\; SHAP model; 1,3,11,15
- difference-in-differences; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; Model III: We developed a DID-GAN hybrid model to quantify the "great coach"; 1,3,11,15
- difference-in-differences; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; **Keywords: VBGMM\; DID Model\; Cox TVPH\; SEM**; 4,12,16
- difference-in-differences; P2025-F-02; p1; corpus/papers/md/2025美赛O奖论文/F/2507789.md; cybercrime. The second model utilizes Difference-in-Differences (DID) analysis to establish a; 4,12,16
- difference-in-differences; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; richlet Allocation (LDA) and the Difference - in - Differences (DID) model. LDA categorized; 4,12,16
- difference-in-differences; P2025-F-05; p5; corpus/papers/md/2025美赛O奖论文/F/2521039.md; DID; 4,12,16
- differential equation; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; number of stair users on a specific day, we established a partial differential equation to; 8,13,14
- differential equation; P2025-A-04; p14; corpus/papers/md/2025美赛O奖论文/A/2504218.md; flow rates of people going upstairs and downstairs, we can formulate a partial differential equation that; 8,13,14
- differential equation; P2025-B-06; p1; corpus/papers/md/2025美赛O奖论文/B/2509557.md; System Dynamics\; differential equations\; logistics growth model\; dynamic feedback loops\;; 2,6,10,13
- differential equation; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; For Problem 1, we mainly employ differential equations and develop the equations pro-; 2,6,9,18
- differential equation; P2025-E-02; p8; corpus/papers/md/2025美赛O奖论文/E/2508861.md; are modeled using partial differential equations, expressed as follows:; 2,6,9,18
- differential equation; P2025-E-03; p12; corpus/papers/md/2025美赛O奖论文/E/2515136.md; Pi ←Runge-Kutta Method(Producer energy differential equation, P0, ti); 2,6,9,18
- differential evolution; P2025-E-04; p1; corpus/papers/md/2025美赛O奖论文/E/2517273.md; differential evolution algorithms, we successfully fine-tuned 27 key parameters across three distinct phases; 2,6,9,18
- dynamic programming; P2025-B-04; p1; corpus/papers/md/2025美赛O奖论文/B/2504448.md; frastructure. To address this issue, we develop a multi-objective dynamic programming; 2,6,10,13
- dynamic programming; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; **Availability. We used Approximate Dynamic Programming(ADP) to optimize paths in**; 5,7,17,19
- entropy weight method; P2025-B-04; p1; corpus/papers/md/2025美赛O奖论文/B/2504448.md; ature, snowfall, and ocean pH using entropy weight method. This environment model; 2,6,10,13
- entropy weight method; P2025-D-02; p2; corpus/papers/md/2025美赛O奖论文/D/2507692.md; Analysis Based on Entropy Weight Method; 5,7,17,19
- entropy weight method; P2025-D-04; p13; corpus/papers/md/2025美赛O奖论文/D/2519935.md; Next, we employ the entropy weight method (TOPSIS) to compute the weight of the two; 5,7,17,19
- entropy weight method; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; benefits. An EWM-AHP model is developed to assess these schemes for organic farming.; 2,6,9,18
- entropy weight method; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; ods, incorporating four primary and ten secondary indicators. The EWM was used to calculate; 2,6,9,18
- exponential smoothing; P2025-C-04; p28; corpus/papers/md/2025美赛O奖论文/C/2505964.md; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal; 1,3,11,15
- factor analysis; P2025-B-05; p26; corpus/papers/md/2025美赛O奖论文/B/2505199.md; techniques, like time - series analysis for predicting tourist flow trends and factor analysis for; 2,6,10,13
- factor analysis; P2025-C-14; p11; corpus/papers/md/2025美赛O奖论文/C/2516695.md; *Figure 8: Olympic Medal Risk Factor Analysis*; 1,3,11,15
- factor analysis; P2025-D-02; p23; corpus/papers/md/2025美赛O奖论文/D/2507692.md; 2. Inadequate Complex-Factor Analysis: Despite considering multiple factors, the study of; 5,7,17,19
- factor analysis; P2025-F-02; p21; corpus/papers/md/2025美赛O奖论文/F/2507789.md; and effective." Based on Confirmatory Factor Analysis (CFA) results, the following; 4,12,16
- factor analysis; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; we used the Maximal Information Coefficient (MIC) method and factor analysis. The results; 4,12,16
- feature selection; P2025-A-01; p7; corpus/papers/md/2025美赛O奖论文/A/2500836.md; **Step 2: Feature extraction**; 8,13,14
- feature selection; P2025-C-03; p6; corpus/papers/md/2025美赛O奖论文/C/2503389.md; **Feature Selection**; 1,3,11,15
- feature selection; P2025-C-04; p22; corpus/papers/md/2025美赛O奖论文/C/2505964.md; gesting potential issues in feature selection or; 1,3,11,15
- feature selection; P2025-C-13; p9; corpus/papers/md/2025美赛O奖论文/C/2516178.md; velop a TPE-XGBoost model for optimizing XGBoost's feature selection and hyperparameter; 1,3,11,15
- feature selection; P2025-C-15; p10; corpus/papers/md/2025美赛O奖论文/C/2517690.md; strong feature selection ability, low risk of over-; 1,3,11,15
- finite difference; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; Then we used the finite difference method to calculate the pedestrian density during stair usage and; 8,13,14
- fuzzy comprehensive evaluation; P2025-D-03; p1; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **Keywords: Traffic Flow Optimization, Fuzzy Comprehensive Evaluation, Wardrop**; 5,7,17,19
- fuzzy comprehensive evaluation; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; ponents, we establish OAIE Model based on a fuzzy comprehensive evaluation of the impacts of; 2,6,9,18
- fuzzy logic; P2025-D-03; p24; corpus/papers/md/2025美赛O奖论文/D/2516219.md; [4] Goguen, Joseph A. "LA Zadeh. Fuzzy sets. Information and control, vol. 8 (1965),; 5,7,17,19
- genetic algorithm; P2025-B-05; p1; corpus/papers/md/2025美赛O奖论文/B/2505199.md; the Non - dominated Sorting Genetic Algorithm II (NSGA - II) is employed to solve the; 2,6,10,13
- genetic algorithm; P2025-B-07; p4; corpus/papers/md/2025美赛O奖论文/B/2517929.md; and multi-objective genetic algorithms. Based on this, we finally choose the NSGA-II al-; 2,6,10,13
- genetic algorithm; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; genetic algorithms and incorporating home advantage adjustments.; 1,3,11,15
- genetic algorithm; P2025-D-01; p10; corpus/papers/md/2025美赛O奖论文/D/2504188.md; **genetic algorithm to improve both efficiency and accuracy. The improved A***; 5,7,17,19
- gradient boosting; P2025-C-01; p25; corpus/papers/md/2025美赛O奖论文/C/2500759.md; region, northwest china: Research using the extreme gradient boosting (xgboost); 1,3,11,15
- gradient boosting; P2025-C-08; p7; corpus/papers/md/2025美赛O奖论文/C/2510862.md; **1. LightGBM (LGBM)**; 1,3,11,15
- gradient boosting; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Muhammad Amien Ibrahim compared XGBoost, LightGBM and CatBoost and found that; 1,3,11,15
- gradient boosting; P2025-C-13; p25; corpus/papers/md/2025美赛O奖论文/C/2516178.md; 4. Ibrahem Ahmed Osman, A., et al., Extreme gradient boosting (Xgboost) model to; 1,3,11,15
- graph theory; P2025-D-02; p1; corpus/papers/md/2025美赛O奖论文/D/2507692.md; ## on Graph Theory & Clustering Algorithm; 5,7,17,19
- graph theory; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; For Problem 2, a network is established using graph theory, with populations as nodes.; 2,6,9,18
- grey prediction; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; result of women’s shot put in 2012 based on GM(1,1) prediction model in Gray System Theory,; 1,3,11,15
- grey relational analysis; P2025-C-15; p15; corpus/papers/md/2025美赛O奖论文/C/2517690.md; **(2) Grey Relational Analysis**; 1,3,11,15
- hurdle model; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; ## Medal Prediction Based on Tobit and Hurdle Models; 1,3,11,15
- hurdle model; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; model, which combines the Mundlak-modified Tobit regression model with the Hurdle; 1,3,11,15
- hurdle model; P2025-C-13; p3; corpus/papers/md/2025美赛O奖论文/C/2516178.md; transformation of the Tobit model and the Hurdle model are the most emblematic. Simultane-; 1,3,11,15
- hurdle model; P2025-C-17; p2; corpus/papers/md/2025美赛O奖论文/C/2522820.md; Mixed Linear Models and Hurdle Model; 1,3,11,15
- hypothesis test; P2025-A-01; p16; corpus/papers/md/2025美赛O奖论文/A/2500836.md; Finally, a Monte Carlo simulation was used for reliability assessment, with hypothesis testing:; 8,13,14
- hypothesis test; P2025-A-05; p14; corpus/papers/md/2025美赛O奖论文/A/2511565.md; 3.4 Hypothesis Testing; 8,13,14
- hypothesis test; P2025-B-05; p27; corpus/papers/md/2025美赛O奖论文/B/2505199.md; Hypothesis Testing: We used Kimi to assist in hypothesis testing during the model -; 2,6,10,13
- hypothesis test; P2025-C-01; p2; corpus/papers/md/2025美赛O奖论文/C/2500759.md; Hypothesis Testing and Contribution Coefficient Analysis · · · · · · · · · · ·; 1,3,11,15
- hypothesis test; P2025-C-13; p18; corpus/papers/md/2025美赛O奖论文/C/2516178.md; ments, which will serve as the basis for subsequent hypothesis testing.; 1,3,11,15
- hypothesis test; P2025-C-14; p17; corpus/papers/md/2025美赛O奖论文/C/2516695.md; • Statistical Significance Test; 1,3,11,15
- hypothesis test; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; comes, we conducted the Two-sample mean hypothesis testing and the Chi-square test to; 1,3,11,15
- hypothesis test; P2025-F-01; p2; corpus/papers/md/2025美赛O奖论文/F/2504223.md; Hypothesis Testing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 4,12,16
- integer programming; P2025-F-02; p14; corpus/papers/md/2025美赛O奖论文/F/2507789.md; established an integer programming model:; 4,12,16
- isolation forest; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; ensemble-learning anomaly detection method, Isolation Forest, was also employed to cross-validate the choice of; 1,3,11,15
- lasso; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; building the model by using the Lasso Regression, we selected three countries and identify; 1,3,11,15
- lasso; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; country. Through ten-fold cross-validation, we compared Random Forest Regression, Lasso; 1,3,11,15
- linear regression; P2025-A-02; p4; corpus/papers/md/2025美赛O奖论文/A/2501567.md; Linear Regression; 8,13,14
- linear regression; P2025-B-01; p12; corpus/papers/md/2025美赛O奖论文/B/2501687.md; Juneau[8][9][10], and perform a linear regression fit to obtain the following results:; 2,6,10,13
- linear regression; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; **Medal Forecasting: We developed a Multiple Linear Regression–Feedforward Neural**; 1,3,11,15
- linear regression; P2025-C-04; p1; corpus/papers/md/2025美赛O奖论文/C/2505964.md; Poisson regression, and linear regression.; 1,3,11,15
- linear regression; P2025-C-05; p13; corpus/papers/md/2025美赛O奖论文/C/2507817.md; Logistic regression is a generalized linear regression that combines a nonlinear function; 1,3,11,15
- linear regression; P2025-C-06; p1; corpus/papers/md/2025美赛O奖论文/C/2510006.md; Olympics, linear regression, and average values to predict medal outcomes for both returning; 1,3,11,15
- linear regression; P2025-C-07; p9; corpus/papers/md/2025美赛O奖论文/C/2510185.md; We evaluated multiple models to select the best for prediction. Linear regression is chosen for; 1,3,11,15
- linear regression; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; the prediction results of Linear Regression and Random Forest. The data for fitting are all the threshold-activated; 1,3,11,15
- linear regression; P2025-C-12; p9; corpus/papers/md/2025美赛O奖论文/C/2515235.md; This leads to truncation issues in traditional regression models. A simple linear regression; 1,3,11,15
- linear regression; P2025-C-13; p11; corpus/papers/md/2025美赛O奖论文/C/2516178.md; the linear regression model only reaches 0.570, indicating a significant performance disparity.; 1,3,11,15
- linear regression; P2025-C-15; p4; corpus/papers/md/2025美赛O奖论文/C/2517690.md; various regression methods (such as linear regression, polynomial regression, ridge regression,; 1,3,11,15
- linear regression; P2025-C-16; p9; corpus/papers/md/2025美赛O奖论文/C/2521556.md; shorter time spans, we used simple linear regression.; 1,3,11,15
- linear regression; P2025-C-17; p10; corpus/papers/md/2025美赛O奖论文/C/2522820.md; issues). To predict the number of athletes for each country in 2028, we used a simple linear regression. Finally,; 1,3,11,15
- linear regression; P2025-F-03; p19; corpus/papers/md/2025美赛O奖论文/F/2513705.md; Subsequently, step - by - step linear regression analysis was conducted using Factor 1, Factor; 4,12,16
- linear regression; P2025-F-05; p5; corpus/papers/md/2025美赛O奖论文/F/2521039.md; Intercept in the baseline linear regression model; 4,12,16
- logistic regression; P2025-B-01; p11; corpus/papers/md/2025美赛O奖论文/B/2501687.md; **can employ the Logistic Model:**; 2,6,10,13
- logistic regression; P2025-B-03; p9; corpus/papers/md/2025美赛O奖论文/B/2503268.md; teraction with the glacier environment. According to Verhulst’s logistic model [3], population growth; 2,6,10,13
- logistic regression; P2025-C-01; p11; corpus/papers/md/2025美赛O奖论文/C/2500759.md; or defining a binary variable for "having won a gold medal" to apply logistic regression; 1,3,11,15
- logistic regression; P2025-C-02; p9; corpus/papers/md/2025美赛O奖论文/C/2501869.md; We use the Logit model to calculate the probability that the i country will get at least one; 1,3,11,15
- logistic regression; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; First-Time Medalists: We developed a hybrid Logistic Regression–Random Forest model; 1,3,11,15
- logistic regression; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; For Task 2, we established a Logistic Regression Model to classify countries that have; 1,3,11,15
- logistic regression; P2025-C-06; p9; corpus/papers/md/2025美赛O奖论文/C/2510006.md; world rankings are available, we use logistic regression to assess the performance gaps; 1,3,11,15
- logistic regression; P2025-C-08; p7; corpus/papers/md/2025美赛O奖论文/C/2510862.md; learner (logistic regression) to generate the final prediction. The core advantage of; 1,3,11,15
- logistic regression; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; In order to analyze the "Great Coach" effect, we constructed a logistic regression model; 1,3,11,15
- logistic regression; P2025-C-13; p9; corpus/papers/md/2025美赛O奖论文/C/2516178.md; an example and compare three models: XGBoost, binary logistic regression, and random forest.; 1,3,11,15
- logistic regression; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; the Logistic Regression Model to predict their probability of winning, and the results show; 1,3,11,15
- logistic regression; P2025-C-18; p8; corpus/papers/md/2025美赛O奖论文/C/2524070.md; as a Bernoulli distribution process, which will be executed through logistic regression, as follows:; 1,3,11,15
- logistic regression; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; a generalized Logistic model, incorporating a spatial diffusion term to describe population; 2,6,9,18
- logistic regression; P2025-E-04; p11; corpus/papers/md/2025美赛O奖论文/E/2517273.md; the ladybug predation efficiency will become saturated. We did not use a Logistic model to describe aphid; 2,6,9,18
- logistic regression; P2025-F-01; p3; corpus/papers/md/2025美赛O奖论文/F/2504223.md; classiﬁcation logistic regression to analyze the law of cybercrime.; 4,12,16
- machine learning; P2025-A-01; p22; corpus/papers/md/2025美赛O奖论文/A/2500836.md; the advanced machine learning algorithm, particle swarm optimization algorithm (PSO), which; 8,13,14
- machine learning; P2025-A-05; p3; corpus/papers/md/2025美赛O奖论文/A/2511565.md; machine learning, specifically CNN models [5], to train data and obtain rail wear amounts have; 8,13,14
- machine learning; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; machine learning integration methods, we achieve an in-depth analysis and reliable pre-; 1,3,11,15
- machine learning; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; were significantly better than the machine learning methods (random forest and XGboost) in; 1,3,11,15
- machine learning; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; ## Regression and Machine Learning; 1,3,11,15
- machine learning; P2025-C-04; p7; corpus/papers/md/2025美赛O奖论文/C/2505964.md; 3 One-hot encoding utilized to facilitate processing by machine learning models, for NOC and; 1,3,11,15
- machine learning; P2025-C-05; p8; corpus/papers/md/2025美赛O奖论文/C/2507817.md; Random forests are machine learning algorithms trained using multiple decision trees,; 1,3,11,15
- machine learning; P2025-C-07; p24; corpus/papers/md/2025美赛O奖论文/C/2510185.md; medal distribution – a socioeconomic machine learning model,” Technological Forecasting; 1,3,11,15
- machine learning; P2025-C-08; p6; corpus/papers/md/2025美赛O奖论文/C/2510862.md; the first step is to construct a machine learning regression prediction model that can make; 1,3,11,15
- machine learning; P2025-C-09; p7; corpus/papers/md/2025美赛O奖论文/C/2513314.md; machine learning methods (e.g., RNN and two-stage RF) are clearly unsuitable, as they fail; 1,3,11,15
- machine learning; P2025-C-10; p25; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Perspective from Explainable Machine Learning. Journal of Shanghai University of Sport, 48(4),; 1,3,11,15
- machine learning; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; machine learning algorithms were provided by Jhankar Moolchandani et al. [2] including; 1,3,11,15
- machine learning; P2025-C-12; p25; corpus/papers/md/2025美赛O奖论文/C/2515235.md; tribution–a socioeconomic machine learning model," Technol. Forecast. Soc. Change,; 1,3,11,15
- machine learning; P2025-C-13; p6; corpus/papers/md/2025美赛O奖论文/C/2516178.md; proposes an innovative dual-stage machine learning approach [2].; 1,3,11,15
- machine learning; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; **Keywords: Olympics \; medal prediction \; Machine Learning \;“great coach” effect**; 1,3,11,15
- machine learning; P2025-C-18; p6; corpus/papers/md/2025美赛O奖论文/C/2524070.md; general regression or machine learning model.; 1,3,11,15
- machine learning; P2025-D-02; p25; corpus/papers/md/2025美赛O奖论文/D/2507692.md; models, exact and heuristic algorithms, and machine learning. Expert Systems with Applica-; 5,7,17,19
- machine learning; P2025-F-01; p5; corpus/papers/md/2025美赛O奖论文/F/2504223.md; encoding method helps machine learning algorithms better process and understand; 4,12,16
- machine learning; P2025-F-02; p18; corpus/papers/md/2025美赛O奖论文/F/2507789.md; cybercrime across different countries using statistical modeling, machine learning,; 4,12,16
- machine learning; P2025-F-04; p23; corpus/papers/md/2025美赛O奖论文/F/2517199.md; Using a combination of statistical methods and advanced machine learning; 4,12,16
- minimum spanning tree; P2025-D-02; p14; corpus/papers/md/2025美赛O奖论文/D/2507692.md; For each cluster, we further solved the minimum spanning tree. The construction principle of the; 5,7,17,19
- moving average; P2025-C-05; p6; corpus/papers/md/2025美赛O奖论文/C/2507817.md; predictions.The ARIMA model integrates autoregressive (AR) and moving average (MA); 1,3,11,15
- moving average; P2025-C-06; p1; corpus/papers/md/2025美赛O奖论文/C/2510006.md; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**; 1,3,11,15
- moving average; P2025-C-16; p9; corpus/papers/md/2025美赛O奖论文/C/2521556.md; The SARIMAX model combines autoregression AR, moving average MA, seasonal patterns S,; 1,3,11,15
- moving average; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; performances at the Games are time series, so we used a time series analysis incorporating a moving average.; 1,3,11,15
- multi-objective optimization; P2025-B-02; p1; corpus/papers/md/2025美赛O奖论文/B/2502617.md; develops a multi-objective planning model that integrates economic, social, and environmental; 2,6,10,13
- multi-objective optimization; P2025-B-04; p1; corpus/papers/md/2025美赛O奖论文/B/2504448.md; **Keywords: Multi-Objective Model, Dynamic Programming, Sustainable Tourism**; 2,6,10,13
- multi-objective optimization; P2025-B-05; p1; corpus/papers/md/2025美赛O奖论文/B/2505199.md; Keywords: Sustainable tourism\; Juneau\; Multi - objective optimization\; NSGA - II; 2,6,10,13
- multi-objective optimization; P2025-B-07; p1; corpus/papers/md/2025美赛O奖论文/B/2517929.md; Several models are established: Model I: Multi-Objective Optimization Model for Sustain-; 2,6,10,13
- multi-objective optimization; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; For Model II, our greatest highlight is to solve the multi-objective optimization problem; 2,6,9,18
- multi-type Holling responses; P2025-E-04; p1; corpus/papers/md/2025美赛O奖论文/E/2517273.md; Keywords: differential evolution optimization, ecosystem modeling, multi-type Holling responses,; 2,6,9,18
- network analysis; P2025-D-02; p23; corpus/papers/md/2025美赛O奖论文/D/2507692.md; some complex elements is incomplete. For instance, bus network analysis mainly focuses on; 5,7,17,19
- network analysis; P2025-F-02; p1; corpus/papers/md/2025美赛O奖论文/F/2507789.md; governance. By integrating clustering analysis, causal inference, and network analysis, this; 4,12,16
- network flow; P2025-D-03; p2; corpus/papers/md/2025美赛O奖论文/D/2516219.md; **Urban Traffic Network Flow**; 5,7,17,19
- neural network; P2025-C-02; p24; corpus/papers/md/2025美赛O奖论文/C/2501869.md; the summer Olympics using neural networks. Computers & Operations Research, 26(13),; 1,3,11,15
- neural network; P2025-C-03; p2; corpus/papers/md/2025美赛O奖论文/C/2503389.md; **Multiple Linear Regression-Feedforward Neural Network Bootstrap Ensemble**; 1,3,11,15
- neural network; P2025-C-07; p1; corpus/papers/md/2025美赛O奖论文/C/2510185.md; Keywords: Athlete Potential Index\; Event Potential Index\; Random Forest\; BP Neural Network; 1,3,11,15
- neural network; P2025-C-10; p4; corpus/papers/md/2025美赛O奖论文/C/2514362.md; advantages, and historical performance using neural networks and a Cobb-Douglas frame-; 1,3,11,15
- neural network; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Linear Regression, Random Forest, Support Vector Machines and Neural Networks. They are; 1,3,11,15
- neural network; P2025-C-13; p13; corpus/papers/md/2025美赛O奖论文/C/2516178.md; When evaluating the confidence intervals of neural network models, traditional ap-; 1,3,11,15
- neural network; P2025-C-14; p18; corpus/papers/md/2025美赛O奖论文/C/2516695.md; Figure 14 models the global coach - flow network using a graph neural network; 1,3,11,15
- neural network; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; Regression, XGBoost Regression and Neural Network Regression models respectively, and; 1,3,11,15
- nonlinear programming; P2025-B-01; p1; corpus/papers/md/2025美赛O奖论文/B/2501687.md; **Keywords: Sustainable tourism\; CVM\; Multi-objective nonlinear programming**; 2,6,10,13
- nonlinear programming; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; nonlinear programming model with the objective of maximizing bus coverage, subject to; 5,7,17,19
- nonlinear programming; P2025-E-02; p19; corpus/papers/md/2025美赛O奖论文/E/2508861.md; Planning (COMAP) model, employing multi-objective nonlinear programming to analyze the; 2,6,9,18
- nonlinear regression; P2025-B-03; p9; corpus/papers/md/2025美赛O奖论文/B/2503268.md; the parameters ki and ri through nonlinear regression. Due to the complexity of real-world systems,; 2,6,10,13
- nonlinear regression; P2025-B-07; p10; corpus/papers/md/2025美赛O奖论文/B/2517929.md; **2) Nonlinear regression analysis of average temperature and carbon footprint**; 2,6,10,13
- ordinary differential equation; P2025-B-03; p4; corpus/papers/md/2025美赛O奖论文/B/2503268.md; gies. The SDTM, formulated with ordinary diﬀerential equations (ODE), establishes the relationships; 2,6,10,13
- partial differential equation; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; number of stair users on a specific day, we established a partial differential equation to; 8,13,14
- partial differential equation; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## For the advanced tasks 3 & 5, we developed a multi-layer PDE model as well as a; 8,13,14
- partial differential equation; P2025-E-02; p8; corpus/papers/md/2025美赛O奖论文/E/2508861.md; are modeled using partial differential equations, expressed as follows:; 2,6,9,18
- particle swarm optimization; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; Swarm Optimization algorithm(PSO).; 8,13,14
- particle swarm optimization; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## and simulation. After Particle Swarm Optimization (PSO) locates the global optimum,; 8,13,14
- particle swarm optimization; P2025-B-01; p1; corpus/papers/md/2025美赛O奖论文/B/2501687.md; **gramming Model based on Contingent Valuation Method(CVM) and Particle Swarm**; 2,6,10,13
- particle swarm optimization; P2025-C-12; p11; corpus/papers/md/2025美赛O奖论文/C/2515235.md; emerging countries. Finally, Particle Swarm Optimization (PSO) is used to optimize pre-; 1,3,11,15
- principal component analysis; P2025-C-01; p1; corpus/papers/md/2025美赛O奖论文/C/2500759.md; patterns. Utilizing Principal Component Analysis (PCA) for dimensionality reduction; 1,3,11,15
- principal component analysis; P2025-C-02; p5; corpus/papers/md/2025美赛O奖论文/C/2501869.md; Medal_PCA; 1,3,11,15
- principal component analysis; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; via Principal Component Analysis. Results identified swimming (USA, IS = 39.8) and diving; 1,3,11,15
- principal component analysis; P2025-C-10; p26; corpus/papers/md/2025美赛O奖论文/C/2514362.md; eration (e.g., GANs, SMOTE). Feature engineering and dimensionality reduction (PCA, t-; 1,3,11,15
- principal component analysis; P2025-F-01; p2; corpus/papers/md/2025美赛O奖论文/F/2504223.md; Principal component analysis dimensionality reduction . . . . . .; 4,12,16
- principal component analysis; P2025-F-02; p9; corpus/papers/md/2025美赛O奖论文/F/2507789.md; **To further analyze and demonstrate the clustering result, we used the PCA**; 4,12,16
- principal component analysis; P2025-F-03; p10; corpus/papers/md/2025美赛O奖论文/F/2513705.md; principal component analysis (PCA) to project high - dimensional data onto a 2D plane helped; 4,12,16
- probit; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; to perform a Negative Binomial Regression based on the predictors, as well as a Probit Regression in the; 1,3,11,15
- propensity score matching; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; **women’s gymnastics team, focusing on coach Béla Károlyi. Using a PSM-DID model**; 1,3,11,15
- propensity score matching; P2025-C-12; p25; corpus/papers/md/2025美赛O奖论文/C/2515235.md; [4]. F. Fan and X. Zhang, "Transformation effect of resource-based cities based on PSM-DID; 1,3,11,15
- queueing theory; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; traffic conditions, we used Queueing Theory to calculate the congestion index. For each; 5,7,17,19
- random forest; P2025-C-01; p26; corpus/papers/md/2025美赛O奖论文/C/2500759.md; random forest model and then use SHAP to interpret its predictions. The steps might; 1,3,11,15
- random forest; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; were significantly better than the machine learning methods (random forest and XGboost) in; 1,3,11,15
- random forest; P2025-C-03; p1; corpus/papers/md/2025美赛O奖论文/C/2503389.md; First-Time Medalists: We developed a hybrid Logistic Regression–Random Forest model; 1,3,11,15
- random forest; P2025-C-04; p1; corpus/papers/md/2025美赛O奖论文/C/2505964.md; athlete data and various models, including random forest, Monte Carlo simulation,; 1,3,11,15
- random forest; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; For Task 1, we developed a Grid-Search Random Forest (GSRF) prediction model; 1,3,11,15
- random forest; P2025-C-06; p1; corpus/papers/md/2025美赛O奖论文/C/2510006.md; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**; 1,3,11,15
- random forest; P2025-C-07; p1; corpus/papers/md/2025美赛O奖论文/C/2510185.md; ver, and Bronze medals. Following a comparison of various models, we select a Random Forest; 1,3,11,15
- random forest; P2025-C-08; p8; corpus/papers/md/2025美赛O奖论文/C/2510862.md; **4. Random Forest (RF)**; 1,3,11,15
- random forest; P2025-C-09; p22; corpus/papers/md/2025美赛O奖论文/C/2513314.md; [5] Congjun Rao, Ming Liu, Mark Goh, and Jianghui Wen. 2-stage modified random forest; 1,3,11,15
- random forest; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; the prediction results of Linear Regression and Random Forest. The data for fitting are all the threshold-activated; 1,3,11,15
- random forest; P2025-C-13; p9; corpus/papers/md/2025美赛O奖论文/C/2516178.md; an example and compare three models: XGBoost, binary logistic regression, and random forest.; 1,3,11,15
- random forest; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; previous Olympic Games, we constructed a Random Forest regression model for predicting; 1,3,11,15
- random forest; P2025-C-16; p2; corpus/papers/md/2025美赛O奖论文/C/2521556.md; Random Forest Model: Predicting Medals in New Events . . . . . . . . . . . . . . . .; 1,3,11,15
- regression discontinuity; P2025-C-03; p4; corpus/papers/md/2025美赛O奖论文/C/2503389.md; • The disturbance terms in both the multiple regression and regression discontinuity; 1,3,11,15
- reinforcement learning; P2025-B-02; p23; corpus/papers/md/2025美赛O奖论文/B/2502617.md; Safe Urban Bus Routes for Tourism Promotion Using a Hybrid Reinforcement Learning; 2,6,10,13
- reinforcement learning; P2025-C-01; p23; corpus/papers/md/2025美赛O奖论文/C/2500759.md; robust real-time data update mechanism. The use of reinforcement learning will further; 1,3,11,15
- ridge regression; P2025-C-15; p4; corpus/papers/md/2025美赛O奖论文/C/2517690.md; various regression methods (such as linear regression, polynomial regression, ridge regression,; 1,3,11,15
- self-organizing map; P2025-C-14; p25; corpus/papers/md/2025美赛O奖论文/C/2516695.md; deep learning algorithms used in deep neural nets: MLP SOM and DBN. Wireless; 1,3,11,15
- sensitivity analysis; P2025-A-01; p1; corpus/papers/md/2025美赛O奖论文/A/2500836.md; Furthermore, we conduct a sensitivity analysis on the two-dimensional normal distribution; 8,13,14
- sensitivity analysis; P2025-A-03; p1; corpus/papers/md/2025美赛O奖论文/A/2501909.md; Material hardness demonstrates a high sensitivity in our model. The model shows low; 8,13,14
- sensitivity analysis; P2025-A-04; p1; corpus/papers/md/2025美赛O奖论文/A/2504218.md; ## wear. Finally, we performed a sensitivity analysis. The results show that our model; 8,13,14
- sensitivity analysis; P2025-A-05; p1; corpus/papers/md/2025美赛O奖论文/A/2511565.md; Finally, we perform a sensitivity analysis on the key parameters of our model to evaluate its; 8,13,14
- sensitivity analysis; P2025-B-01; p1; corpus/papers/md/2025美赛O奖论文/B/2501687.md; Sensitivity analysis confirmed model stability, highlighting peak-season tourist limits as; 2,6,10,13
- sensitivity analysis; P2025-B-02; p1; corpus/papers/md/2025美赛O奖论文/B/2502617.md; Finally, we analyze the sensitivity of key model parameters, as well as the sources of additional; 2,6,10,13
- sensitivity analysis; P2025-B-03; p1; corpus/papers/md/2025美赛O奖论文/B/2503268.md; We assessed our model’s sensitivity using two methods. The Morris method identiﬁed key factors; 2,6,10,13
- sensitivity analysis; P2025-B-04; p1; corpus/papers/md/2025美赛O奖论文/B/2504448.md; ommended policies. Additionally, we perform a sensitivity analysis to identify the most; 2,6,10,13
- sensitivity analysis; P2025-B-05; p1; corpus/papers/md/2025美赛O奖论文/B/2505199.md; opment of the tourism industry. Sensitivity analysis indicates that the number of tourists, alco-; 2,6,10,13
- sensitivity analysis; P2025-B-06; p1; corpus/papers/md/2025美赛O奖论文/B/2509557.md; plicability. Through sensitivity analysis and scenario simulations, we reveal the critical importance; 2,6,10,13
- sensitivity analysis; P2025-B-07; p1; corpus/papers/md/2025美赛O奖论文/B/2517929.md; Before promoting the model, we conducted a sensitivity analysis using the local pertur-; 2,6,10,13
- sensitivity analysis; P2025-C-01; p2; corpus/papers/md/2025美赛O奖论文/C/2500759.md; ## Sensitivity Analysis ·········································· 21; 1,3,11,15
- sensitivity analysis; P2025-C-02; p2; corpus/papers/md/2025美赛O奖论文/C/2501869.md; **Sensitivity Analysis**; 1,3,11,15
- sensitivity analysis; P2025-C-03; p2; corpus/papers/md/2025美赛O奖论文/C/2503389.md; **11 Sensitivity Analysis**; 1,3,11,15
- sensitivity analysis; P2025-C-04; p2; corpus/papers/md/2025美赛O奖论文/C/2505964.md; Sensitivity Analysis; 1,3,11,15
- sensitivity analysis; P2025-C-05; p1; corpus/papers/md/2025美赛O奖论文/C/2507817.md; talented athletes. Additionally, we performed a sensitivity analysis that demonstrated the; 1,3,11,15
- sensitivity analysis; P2025-C-06; p2; corpus/papers/md/2025美赛O奖论文/C/2510006.md; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 1,3,11,15
- sensitivity analysis; P2025-C-07; p2; corpus/papers/md/2025美赛O奖论文/C/2510185.md; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 1,3,11,15
- sensitivity analysis; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; ance and sensitivity tests supported the robustness of the PSM-DID model. These find-; 1,3,11,15
- sensitivity analysis; P2025-C-09; p1; corpus/papers/md/2025美赛O奖论文/C/2513314.md; To test the robustness of our model, we conducted sensitivity analyses on both the weakly; 1,3,11,15
- sensitivity analysis; P2025-C-10; p2; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 1,3,11,15
- sensitivity analysis; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; insights were visualized and discussed, and sensitivity analysis was done.; 1,3,11,15
- sensitivity analysis; P2025-C-12; p1; corpus/papers/md/2025美赛O奖论文/C/2515235.md; lyzed its sensitivity. By conducting error analysis between the total medal count derived from; 1,3,11,15
- sensitivity analysis; P2025-C-13; p1; corpus/papers/md/2025美赛O奖论文/C/2516178.md; In addition, a sensitivity analysis was conducted to assess the model's responsiveness to; 1,3,11,15
- sensitivity analysis; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; two-dimensional event-country framework (Figure 9) and sensitivity analysis (Section; 1,3,11,15
- sensitivity analysis; P2025-C-15; p1; corpus/papers/md/2025美赛O奖论文/C/2517690.md; Finally, we performed error evaluation and sensitivity analysis of the Cross-validation; 1,3,11,15
- sensitivity analysis; P2025-C-16; p1; corpus/papers/md/2025美赛O奖论文/C/2521556.md; Lastly, we conducted sensitivity analysis on our model, finding that it demonstrates strong gener-; 1,3,11,15
- sensitivity analysis; P2025-D-01; p1; corpus/papers/md/2025美赛O奖论文/D/2504188.md; Lastly, we conducted sensitivity analysis to prove the robustness of the models and the; 5,7,17,19
- sensitivity analysis; P2025-D-02; p1; corpus/papers/md/2025美赛O奖论文/D/2507692.md; Eventually, the sensitivity analysis is carried out to ensure the accuracy of the model. However,; 5,7,17,19
- sensitivity analysis; P2025-D-03; p2; corpus/papers/md/2025美赛O奖论文/D/2516219.md; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .; 5,7,17,19
- sensitivity analysis; P2025-D-04; p1; corpus/papers/md/2025美赛O奖论文/D/2519935.md; firmed through sensitivity analysis, highlighting its considerable practical utility. The approach; 5,7,17,19
- sensitivity analysis; P2025-E-01; p1; corpus/papers/md/2025美赛O奖论文/E/2502355.md; Finally, a sensitivity analysis of the herbicide power (alpha value) in our Problem 1 food; 2,6,9,18
- sensitivity analysis; P2025-E-02; p1; corpus/papers/md/2025美赛O奖论文/E/2508861.md; Finally, sensitivity analyses on Model I revealed that species mortality had a small influ-; 2,6,9,18
- sensitivity analysis; P2025-E-03; p1; corpus/papers/md/2025美赛O奖论文/E/2515136.md; Consequently, a sensitivity analysis was conducted on the model to ascertain its robustness.; 2,6,9,18
- sensitivity analysis; P2025-E-04; p1; corpus/papers/md/2025美赛O奖论文/E/2517273.md; Sensitivity analysis confirms the model's critical parameter dependencies, revealing that even minor; 2,6,9,18
- sensitivity analysis; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; Finally, a sensitivity analysis was performed on the multi-level regression model of; 4,12,16
- sensitivity analysis; P2025-F-02; p3; corpus/papers/md/2025美赛O奖论文/F/2507789.md; 8 Sensitivity Analysis..................................................................................................23; 4,12,16
- sensitivity analysis; P2025-F-03; p1; corpus/papers/md/2025美赛O奖论文/F/2513705.md; Sensitivity analysis on the DID and MIC models indicates the models' stability and reliability.; 4,12,16
- shortest path; P2025-D-01; p7; corpus/papers/md/2025美赛O奖论文/D/2504188.md; the detour’s shortest path varies depending on factors such as travel mode, destination,; 5,7,17,19
- shortest path; P2025-D-02; p1; corpus/papers/md/2025美赛O奖论文/D/2507692.md; application of Flow Balance Equation and Dijkstra Algorithm, the influence of the bridge collapse; 5,7,17,19
- shortest path; P2025-D-03; p10; corpus/papers/md/2025美赛O奖论文/D/2516219.md; where d(vi, vj) represents shortest-path distance between nodes. This formulation; 5,7,17,19
- shortest path; P2025-D-04; p2; corpus/papers/md/2025美赛O奖论文/D/2519935.md; Improved Dijkstra Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . .; 5,7,17,19
- shortest path; P2025-E-01; p18; corpus/papers/md/2025美赛O奖论文/E/2502355.md; d i j is the shortest path distance between speciesi and species j . High closeness; 2,6,9,18
- spatio-temporal modeling; P2025-C-14; p1; corpus/papers/md/2025美赛O奖论文/C/2516695.md; coach effect\;spatio-temporal modeling\;economics\;Sensitivity Analysis; 1,3,11,15
- stacking; P2025-C-01; p9; corpus/papers/md/2025美赛O奖论文/C/2500759.md; XGBoost is an ensemble learning algorithm based on gradient-boosted trees, which; 1,3,11,15
- stacking; P2025-C-02; p3; corpus/papers/md/2025美赛O奖论文/C/2501869.md; ensemble learning methods based on decision trees, excel at handling non-linear relationships; 1,3,11,15
- stacking; P2025-C-08; p1; corpus/papers/md/2025美赛O奖论文/C/2510862.md; puts for a Stacking ensemble model, which outperformed individual algorithms with; 1,3,11,15
- stacking; P2025-C-11; p1; corpus/papers/md/2025美赛O奖论文/C/2514461.md; Swimming for TPE, are their most coach-needing sports. We then used our own ensemble learning by averaging; 1,3,11,15
- stacking; P2025-C-13; p25; corpus/papers/md/2025美赛O奖论文/C/2516178.md; Alberta’s hydrothermal system using boosting-based ensemble learning incorporating Shapley; 1,3,11,15
- stacking; P2025-C-16; p10; corpus/papers/md/2025美赛O奖论文/C/2521556.md; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for; 1,3,11,15
- structural equation modeling; P2025-B-07; p12; corpus/papers/md/2025美赛O奖论文/B/2517929.md; When developing a structural equation model of residents' attitudes towards tourism de-; 2,6,10,13
- structural equation modeling; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; data of different countries and cybercrime, a structural equation model was established; 4,12,16
- structural equation modeling; P2025-F-02; p22; corpus/papers/md/2025美赛O奖论文/F/2507789.md; Structural Equation Model (SEM) Schematic Diagram; 4,12,16
- survival analysis; P2025-C-11; p17; corpus/papers/md/2025美赛O奖论文/C/2514461.md; conduct a survival analysis, treating Year as duration time and winning as the event. After; 1,3,11,15
- survival analysis; P2025-F-01; p1; corpus/papers/md/2025美赛O奖论文/F/2504223.md; namics of their impact on cybercrime, a survival analysis model was established, and it; 4,12,16
- system dynamics; P2025-A-04; p26; corpus/papers/md/2025美赛O奖论文/A/2504218.md; tion: a literature review. Vehicle System Dynamics, 47(6): 661–700, 2007.; 8,13,14
- system dynamics; P2025-B-03; p5; corpus/papers/md/2025美赛O奖论文/B/2503268.md; essential system dynamics.; 2,6,10,13
- system dynamics; P2025-B-06; p1; corpus/papers/md/2025美赛O奖论文/B/2509557.md; ## Society: A System Dynamics-Based Model for; 2,6,10,13
- system dynamics; P2025-B-07; p4; corpus/papers/md/2025美赛O奖论文/B/2517929.md; ➢ Regarding the modeling methods, system dynamics[4], and multi-objective optimization; 2,6,10,13
- system dynamics; P2025-E-01; p3; corpus/papers/md/2025美赛O奖论文/E/2502355.md; system dynamics. Also, account for the changes on herbicides and pesticides on plants, insects,; 2,6,9,18
- system dynamics; P2025-E-02; p22; corpus/papers/md/2025美赛O奖论文/E/2508861.md; fluence system dynamics, highlighting the need to focus on their interactions to optimize eco-; 2,6,9,18
- system dynamics; P2025-E-03; p6; corpus/papers/md/2025美赛O奖论文/E/2515136.md; to model the network and use system dynamics to analyze changes in energy flow. Consequently,; 2,6,9,18
- three-layer bus network model; P2025-D-04; p1; corpus/papers/md/2025美赛O奖论文/D/2519935.md; For task 2, we develop a three-layer bus network model to determine the optimal place-; 5,7,17,19
- time series analysis; P2025-C-01; p6; corpus/papers/md/2025美赛O奖论文/C/2500759.md; Predicting the Olympic medal tally can be framed as a time series forecasting prob-; 1,3,11,15
- time series analysis; P2025-C-04; p28; corpus/papers/md/2025美赛O奖论文/C/2505964.md; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal; 1,3,11,15
- time series analysis; P2025-C-05; p6; corpus/papers/md/2025美赛O奖论文/C/2507817.md; The ARIMA model is widely used in time series analysis for its flexibility and powerful; 1,3,11,15
- time series analysis; P2025-C-06; p12; corpus/papers/md/2025美赛O奖论文/C/2510006.md; ARIMA model and Random Forest model, using time series data and feature engineering to; 1,3,11,15
- time series analysis; P2025-C-10; p6; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Time series analysis can capture long-term trends in a country’s performance. If the data; 1,3,11,15
- time series analysis; P2025-C-11; p4; corpus/papers/md/2025美赛O奖论文/C/2514461.md; calculation methods to do so when handling time series data [5]. Yu Qin and YuanSheng Lou; 1,3,11,15
- time series analysis; P2025-C-12; p3; corpus/papers/md/2025美赛O奖论文/C/2515235.md; Time series forecasting, a common prediction method, uses historical medal counts to; 1,3,11,15
- time series analysis; P2025-C-13; p10; corpus/papers/md/2025美赛O奖论文/C/2516178.md; adopt the last block cross-validation method, which takes the time series into account by using; 1,3,11,15
- time series analysis; P2025-C-14; p8; corpus/papers/md/2025美赛O奖论文/C/2516695.md; **Layer 3: LSTM time series model[4]**; 1,3,11,15
- time series analysis; P2025-C-15; p7; corpus/papers/md/2025美赛O奖论文/C/2517690.md; **◆ Time series chart of the number of medals in each event**; 1,3,11,15
- time series analysis; P2025-C-16; p8; corpus/papers/md/2025美赛O奖论文/C/2521556.md; is directly related to the Olympic host country, we innovatively introduced the SARIMAX time series; 1,3,11,15
- time series analysis; P2025-C-17; p1; corpus/papers/md/2025美赛O奖论文/C/2522820.md; performances at the Games are time series, so we used a time series analysis incorporating a moving average.; 1,3,11,15
- time series analysis; P2025-E-04; p8; corpus/papers/md/2025美赛O奖论文/E/2517273.md; However, for this modeling task, the traditional soil network model cannot perform time series analysis,; 2,6,9,18
- time series analysis; P2025-F-01; p22; corpus/papers/md/2025美赛O奖论文/F/2504223.md; s of policy evaluation and intervention analysis and can handle different time series; 4,12,16
- time series analysis; P2025-F-04; p1; corpus/papers/md/2025美赛O奖论文/F/2517199.md; handling of endogenous and exogenous variables in time series data. Endogenous; 4,12,16
- two-stage least squares; P2025-C-02; p1; corpus/papers/md/2025美赛O奖论文/C/2501869.md; stage least squares (2SLS) method is used to construct a causal regression model to quantify; 1,3,11,15
- zero-inflated; P2025-C-02; p3; corpus/papers/md/2025美赛O奖论文/C/2501869.md; and feature interactions, but they lack the ability to explicitly model truncation and zero-inflated; 1,3,11,15
- zero-inflated; P2025-C-04; p19; corpus/papers/md/2025美赛O奖论文/C/2505964.md; Model Specification Sensitivity: Negative Binomial and Zero-Inflated Poisson; 1,3,11,15
- zero-inflated; P2025-C-10; p2; corpus/papers/md/2025美赛O奖论文/C/2514362.md; Zero expansion negative binomial model (ZINB); 1,3,11,15
- zero-inflated; P2025-C-18; p1; corpus/papers/md/2025美赛O奖论文/C/2524070.md; number of medals awarded to countries, we propose a zero-inflated negative binomial; 1,3,11,15
## 第三节 · 诚实栏（**不藏**）

* **`models` 栏零命中的篇**：条数=0 · TAGS第三层=0 · 逐篇=（无）
  零命中**不等于**「这篇没用模型」，只等于「词表里的模型名一个都没出现」——词表外与「用了但没写名字」的模型**抓不到**（`TAGS.md` 头部的已知漏检，此处照印）。本条的两个数**都要报**（本表逐篇数 = `TAGS.md` 第三层的篇数）——只报一个数会让「本表漏列了零命中的篇」看不出来。
* **低置信条目**：条数=115 · 总指针=496 · 口径=`x1`（该模型名在**该篇全篇**只出现 1 次）
  **这是可机读的形式标记，不是质量判断**——单次提及不等于用得不重要；它们的片段仍逐条列在第二节。逐条（`模型; 篇; p页; 片段`）：

  - ARIMA; P2025-C-04; p28; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal
  - ARIMA; P2025-C-11; p7; methods can be employed to forecast the number of events in the 2028 Games. While ARIMA
  - BP neural network; P2025-D-01; p10; BP
  - Bayesian; P2025-C-17; p10; We decided to use Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) as
  - CNN; P2025-A-05; p3; machine learning, specifically CNN models [5], to train data and obtain rail wear amounts have
  - CNN; P2025-C-14; p25; monthly gas field production based on the CNN - LSTM model. Energy, 260,
  - Causal Inference; P2025-C-02; p2; **Change-Point Detection and Causal Inference Models**
  - Causal Inference; P2025-C-10; p6; Difference-in-Differences (causal inference method)
  - Food web model; P2025-E-02; p4; model, and food web model, with their respective strengths and limitations shown in Figure 2.
  - Food web model; P2025-E-04; p6; Assumption2: In this food web model, we assume that sparrows and bats exclusively feed on
  - Gaussian Distribution; P2025-A-04; p13; Here, (δx, δy) can be drawn from a Gaussian distribution N((x0, y0), Σ) to reflect that each footstep
  - Gaussian Mixture Algorithm; P2025-A-03; p1; Keywords: Stair Wear, Archard Law, Central Limit Theorem, Gaussian Mixture Algorithm
  - LSTM; P2025-C-09; p22; [3] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural Computation,
  - Markov chain; P2025-C-01; p5; memoryless characteristic of Olympic medal trends akin to Markov chains, we employ an
  - Markov chain; P2025-C-09; p9; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,
  - Monte Carlo; P2025-A-05; p14; After considering all the above factors, we wrote a Python program using the Monte Carlo
  - Monte Carlo; P2025-B-01; p17; we use the Monte Carlo Method to select 101 values at equal intervals with a step size of
  - Monte Carlo; P2025-C-09; p9; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,
  - Monte Carlo; P2025-C-16; p13; So, how many countries are most likely to win medals in 2028? We conducted a Monte Carlo
  - Petri-Food Web model; P2025-E-03; p1; Keywords: Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger-
  - Regression Analysis; P2025-B-01; p12; *Figure 6: Linear regression analysis of the population and median income in Juneau*
  - Regression Analysis; P2025-C-03; p11; *Table 5: Key Metrics and Results of Regression Analysis*
  - Regression Analysis; P2025-C-08; p21; *Table 2: DID regression analysis results*
  - Regression Analysis; P2025-C-09; p1; Quantification, Regression Analysis, Credible Intervals
  - Regression Analysis; P2025-F-01; p24; ative Infection Based on Logistic Multiple Regression Analysis in the Assess-
  - Regression Analysis; P2025-F-02; p19; ## 6.3.1 Panel Regression Analysis
  - Regression Analysis; P2025-F-05; p12; merged into a complete analytical sample. In the regression analysis, the model treated
  - Uncertainty Quantification; P2025-A-04; p19; posterior uncertainty quantification” under limited computational overhead. It aligns the simulated
  - Uncertainty Quantification; P2025-C-09; p1; A key strength of this model is its robust uncertainty quantification. Each country’s
  - Uncertainty Quantification; P2025-C-14; p24; Probabilistic calibration is validated by uncertainty quantification achieving 93.2%
  - cluster analysis; P2025-B-03; p11; cated by the tight clustering of observed data along the model trajectories in the (NJuneau, TJuneau)
  - cluster analysis; P2025-C-01; p25; autoencoder-based arithmetic optimization clustering algorithm to enhance principal
  - cluster analysis; P2025-C-11; p28; models like group or cluster analysis methods to account for these dependencies.
  - cluster analysis; P2025-C-12; p14; continents is more scattered, with no clear regional clustering of improvements.5.3.3：Ana-
  - correlation coefficient; P2025-A-04; p3; materials after a certain amount of wear by changing the correlation coefficient, and obtain the
  - correlation coefficient; P2025-B-07; p18; tion indicates the magnitude of the correlation coefficient. The closer the absolute value is to
  - correlation coefficient; P2025-D-02; p16; correlation coefficient to precisely measure the strength and direction of this relationship and visualized
  - cross-validation; P2025-A-05; p24; the staircase, employing cross-validation with multiple data sources to boost reliability.
  - cross-validation; P2025-F-05; p26; **Cross-validation: Use multiple sources like OECD and national government**
  - decision tree; P2025-C-03; p13; The Random Forest model aggregates the predictions of multiple decision trees. The final pre-
  - decision tree; P2025-C-05; p8; Random forests are machine learning algorithms trained using multiple decision trees,
  - decision tree; P2025-C-06; p12; of countries winning ﬁrst medals. The ensemble of decision trees helps reduce overﬁtting, and
  - decision tree; P2025-C-10; p26; chine learning. In ML, entropy guides decision-making: decision trees split features to min-
  - decision tree; P2025-C-16; p10; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for
  - deep learning; P2025-B-05; p21; ·Adopt advanced algorithms like deep learning to boost efficiency and accuracy for de-
  - deep learning; P2025-C-01; p23; pact analysis with deep learning techniques to refine medal predictions. By incorporating
  - deep learning; P2025-C-15; p4; deep learning in dealing with complex non-linear relationships. [3]J. Moolchandani, V. Chole,
  - deep learning; P2025-C-16; p25; [6] Deepvarma: A hybrid deep learning and varma model for chemical industry index forecasting. No
  - difference-in-differences; P2025-C-02; p20; methods (such as OLS, DID, and IV) and develop a parameter estimation method that eliminates
  - differential equation; P2025-A-04; p14; flow rates of people going upstairs and downstairs, we can formulate a partial differential equation that
  - exponential smoothing; P2025-C-04; p28; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal
  - factor analysis; P2025-B-05; p26; techniques, like time - series analysis for predicting tourist flow trends and factor analysis for
  - factor analysis; P2025-C-14; p11; *Figure 8: Olympic Medal Risk Factor Analysis*
  - factor analysis; P2025-D-02; p23; 2. Inadequate Complex-Factor Analysis: Despite considering multiple factors, the study of
  - factor analysis; P2025-F-02; p21; and effective." Based on Confirmatory Factor Analysis (CFA) results, the following
  - feature selection; P2025-A-01; p7; **Step 2: Feature extraction**
  - feature selection; P2025-C-04; p22; gesting potential issues in feature selection or
  - feature selection; P2025-C-13; p9; velop a TPE-XGBoost model for optimizing XGBoost's feature selection and hyperparameter
  - feature selection; P2025-C-15; p10; strong feature selection ability, low risk of over-
  - fuzzy logic; P2025-D-03; p24; [4] Goguen, Joseph A. "LA Zadeh. Fuzzy sets. Information and control, vol. 8 (1965),
  - genetic algorithm; P2025-C-10; p4; genetic algorithms and incorporating home advantage adjustments.
  - gradient boosting; P2025-C-01; p25; region, northwest china: Research using the extreme gradient boosting (xgboost)
  - gradient boosting; P2025-C-13; p25; 4. Ibrahem Ahmed Osman, A., et al., Extreme gradient boosting (Xgboost) model to
  - graph theory; P2025-E-01; p1; For Problem 2, a network is established using graph theory, with populations as nodes.
  - hypothesis test; P2025-C-13; p18; ments, which will serve as the basis for subsequent hypothesis testing.
  - integer programming; P2025-F-02; p14; established an integer programming model:
  - linear regression; P2025-A-02; p4; Linear Regression
  - linear regression; P2025-C-12; p9; This leads to truncation issues in traditional regression models. A simple linear regression
  - linear regression; P2025-C-17; p10; issues). To predict the number of athletes for each country in 2028, we used a simple linear regression. Finally,
  - linear regression; P2025-F-03; p19; Subsequently, step - by - step linear regression analysis was conducted using Factor 1, Factor
  - logistic regression; P2025-B-03; p9; teraction with the glacier environment. According to Verhulst’s logistic model [3], population growth
  - logistic regression; P2025-C-01; p11; or defining a binary variable for "having won a gold medal" to apply logistic regression
  - logistic regression; P2025-C-06; p9; world rankings are available, we use logistic regression to assess the performance gaps
  - logistic regression; P2025-C-18; p8; as a Bernoulli distribution process, which will be executed through logistic regression, as follows:
  - logistic regression; P2025-E-04; p11; the ladybug predation efficiency will become saturated. We did not use a Logistic model to describe aphid
  - machine learning; P2025-A-01; p22; the advanced machine learning algorithm, particle swarm optimization algorithm (PSO), which
  - machine learning; P2025-C-03; p1; ## Regression and Machine Learning
  - machine learning; P2025-C-04; p7; 3 One-hot encoding utilized to facilitate processing by machine learning models, for NOC and
  - machine learning; P2025-C-07; p24; medal distribution – a socioeconomic machine learning model,” Technological Forecasting
  - machine learning; P2025-C-12; p25; tribution–a socioeconomic machine learning model," Technol. Forecast. Soc. Change,
  - machine learning; P2025-D-02; p25; models, exact and heuristic algorithms, and machine learning. Expert Systems with Applica-
  - machine learning; P2025-F-01; p5; encoding method helps machine learning algorithms better process and understand
  - machine learning; P2025-F-02; p18; cybercrime across different countries using statistical modeling, machine learning,
  - machine learning; P2025-F-04; p23; Using a combination of statistical methods and advanced machine learning
  - moving average; P2025-C-05; p6; predictions.The ARIMA model integrates autoregressive (AR) and moving average (MA)
  - multi-objective optimization; P2025-B-04; p1; **Keywords: Multi-Objective Model, Dynamic Programming, Sustainable Tourism**
  - multi-type Holling responses; P2025-E-04; p1; Keywords: differential evolution optimization, ecosystem modeling, multi-type Holling responses,
  - network analysis; P2025-D-02; p23; some complex elements is incomplete. For instance, bus network analysis mainly focuses on
  - neural network; P2025-C-02; p24; the summer Olympics using neural networks. Computers & Operations Research, 26(13),
  - neural network; P2025-C-11; p4; Linear Regression, Random Forest, Support Vector Machines and Neural Networks. They are
  - neural network; P2025-C-13; p13; When evaluating the confidence intervals of neural network models, traditional ap-
  - neural network; P2025-C-14; p18; Figure 14 models the global coach - flow network using a graph neural network
  - nonlinear programming; P2025-D-01; p1; nonlinear programming model with the objective of maximizing bus coverage, subject to
  - nonlinear regression; P2025-B-07; p10; **2) Nonlinear regression analysis of average temperature and carbon footprint**
  - principal component analysis; P2025-C-10; p26; eration (e.g., GANs, SMOTE). Feature engineering and dimensionality reduction (PCA, t-
  - random forest; P2025-C-09; p22; [5] Congjun Rao, Ming Liu, Mark Goh, and Jianghui Wen. 2-stage modified random forest
  - reinforcement learning; P2025-B-02; p23; Safe Urban Bus Routes for Tourism Promotion Using a Hybrid Reinforcement Learning
  - reinforcement learning; P2025-C-01; p23; robust real-time data update mechanism. The use of reinforcement learning will further
  - ridge regression; P2025-C-15; p4; various regression methods (such as linear regression, polynomial regression, ridge regression,
  - self-organizing map; P2025-C-14; p25; deep learning algorithms used in deep neural nets: MLP SOM and DBN. Wireless
  - shortest path; P2025-E-01; p18; d i j is the shortest path distance between speciesi and species j . High closeness
  - spatio-temporal modeling; P2025-C-14; p1; coach effect\;spatio-temporal modeling\;economics\;Sensitivity Analysis
  - stacking; P2025-C-02; p3; ensemble learning methods based on decision trees, excel at handling non-linear relationships
  - stacking; P2025-C-13; p25; Alberta’s hydrothermal system using boosting-based ensemble learning incorporating Shapley
  - stacking; P2025-C-16; p10; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for
  - survival analysis; P2025-C-11; p17; conduct a survival analysis, treating Year as duration time and winning as the event. After
  - system dynamics; P2025-A-04; p26; tion: a literature review. Vehicle System Dynamics, 47(6): 661–700, 2007.
  - system dynamics; P2025-B-07; p4; ➢ Regarding the modeling methods, system dynamics[4], and multi-objective optimization
  - system dynamics; P2025-E-01; p3; system dynamics. Also, account for the changes on herbicides and pesticides on plants, insects,
  - system dynamics; P2025-E-02; p22; fluence system dynamics, highlighting the need to focus on their interactions to optimize eco-
  - time series analysis; P2025-C-04; p28; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal
  - time series analysis; P2025-C-10; p6; Time series analysis can capture long-term trends in a country’s performance. If the data
  - time series analysis; P2025-C-12; p3; Time series forecasting, a common prediction method, uses historical medal counts to
  - time series analysis; P2025-E-04; p8; However, for this modeling task, the traditional soil network model cannot perform time series analysis,
  - time series analysis; P2025-F-01; p22; s of policy evaluation and intervention analysis and can handle different time series

* **本表证明不了的事**（与表同读）：① 「题型 → 模型」这条配对的**效度**（「给定题型 X，用模型 Y 合不合适」）本表回答不了——第四节量的是**匹配度**（召回 + 精确性），那是**度量**不是**效度**；② 配对的两侧都是**已有产物的读回**——题型来自人工标注、模型来自词表字面命中，本表**不新增任何判断**；③ 场景（`scenario`）不进配对，故本表**不能**回答「考古类题目该用什么模型」这类问题。


## 第四节 · 匹配度（召回 @ 作者 Keywords + 精确性）

**用户 2026-09-26 的那句验收口**：*「为了建模的准确性…要求最终匹配度较高」*。这一节把「匹配度」变成**可量**的：**召回**（作者点名的模型，我们的词表覆盖了几个）+ **精确性**（我们的每条命中能不能在正文定位）。**没有阈值**——比值如实报出交用户判；判据守的是**「未解释为 0」**（每个未覆盖条目都有三态处置与理由）。

> **机读**（判据 M-14 按这一行对账；键与 `tests/papers/reports/coverage-evidence.txt` 的同名键**逐字相等**）：
> 匹配度：参照篇=42 · 参照不存在=P2025-C-17 · 参照存在但没解析出来=（无） · 召回分子前=68 · 召回分子后=105 · 召回分母=115 · 宽参照分子=76 · 宽参照分母=133 · 未覆盖模型条目=47 · 未覆盖不收录=10 · 未解释=0 · 收录条数=37 · 精确性可定位=496 · 精确性总数=496 · 低置信条数=115 · 分流表行数=112 · 分流表收录行数=48

* **参照（主体口径）**：`corpus/papers/TAGS.md` 一层的 **`keywords` 栏**（**作者自己写的** Key words 行，Task 6 原样抄入、**不是我们算的**）。非空 **42** 篇。**参照不存在 1 篇**：P2025-C-17——该篇 md 里 `key.?words?` 一次都不出现（**「参照不存在」与「参照存在但没解析出来」是两件事**；后者实测 0 篇：（无））。
* **命中（受控口径）**：`tools/papers/vocab/models.txt` 的**字面命中**（词边界口径），指针在 `TAGS.md` 第二层。**两侧不共用任何抽取代码**（作者那侧只按分隔符拆词，我们这侧走词表匹配）——否则召回就是「函数跟自己对答案」。

| 量 | 值 | 读法 |
| :-- | ---: | :-- |
| 召回 @**增长前**词表 | **68/115 = 0.5913** | 作者点名的「模型/算法」条目里，**增长前**的词表覆盖了几个 |
| 召回 @**增长后**词表（现行） | **105/115 = 0.9130** | 本轮按三态表**收录**了 37 条后的覆盖 |
| 召回 @**宽参照**（Keywords 段含续行） | 76/133 = 0.5714 | **登记为边界**（见下） |
| 精确性：命中可定位 | **496/496** | `TAGS.md` 二层每条指针的 `(md, 页, 片段)` **复核**（不重算） |
| 低置信条目（`x1`） | **115** 条 | 单列在 `MODEL_MAP.md` 第三节 |

* **分母的口径**：分母 = 「被覆盖的片」+「未覆盖、且分流表判`模型`的片」。**未覆盖的 `场景` 片不进分母**（`Cybercrime`/`Olympics`/`Juneau` 一类——用户 2026-09-26 定案「场景不进模型词表」），它们逐条处置为 `不收` 并记理由。全 43 篇的片共 **164** 个。
* **未解释（分流表里没有这一片的未覆盖片）**：**0** 条——这一格**必须为 0**（「每个未覆盖条目都要有三态处置、不许沉默」）；不为 0 时逐条列在证据文件里（判据 M-10 判它）。
* **未覆盖的作者模型条目**：**47** 条（逐篇之和），三态处置 **收录 37 条 / 不收 10 条 / 待定 0 条**；**未解释 = 0**。分流表：`tools/papers/vocab/growth_triage.txt`（**112** 行）。

### 第四节 · 逐篇（43 篇）

列序：`稳定 ID | 参照 | 片数 | 覆盖@前 | 未覆盖(模型) | 其中收录 | 召回@前 | 召回@后`。**`参照不存在` 的篇单列**，不记「不适用」。

| 稳定 ID | 参照 | 片数 | 覆盖@前 | 未覆盖(模型) | 其中收录 | 召回@前 | 召回@后 |
| :-- | :-- | ---: | ---: | ---: | ---: | ---: | ---: |
| P2025-A-01（2025 A） | 有参照 | 5 | 2 | 2 | 2 | 2/4 | 4/4 |
| P2025-A-02（2025 A） | 有参照 | 4 | 1 | 1 | 1 | 1/2 | 2/2 |
| P2025-A-03（2025 A） | 有参照 | 4 | 0 | 3 | 3 | 0/3 | 3/3 |
| P2025-A-04（2025 A） | 有参照 | 5 | 4 | 1 | 1 | 4/5 | 5/5 |
| P2025-A-05（2025 A） | 有参照 | 4 | 0 | 3 | 2 | 0/3 | 2/3 |
| P2025-B-01（2025 B） | 有参照 | 3 | 1 | 1 | 1 | 1/2 | 2/2 |
| P2025-B-02（2025 B） | 有参照 | 4 | 0 | 2 | 2 | 0/2 | 2/2 |
| P2025-B-03（2025 B） | 有参照 | 4 | 1 | 2 | 1 | 1/3 | 2/3 |
| P2025-B-04（2025 B） | 有参照 | 3 | 1 | 1 | 1 | 1/2 | 2/2 |
| P2025-B-05（2025 B） | 有参照 | 4 | 0 | 2 | 2 | 0/2 | 2/2 |
| P2025-B-06（2025 B） | 有参照 | 4 | 2 | 1 | 0 | 2/3 | 2/3 |
| P2025-B-07（2025 B） | 有参照 | 4 | 2 | 1 | 1 | 2/3 | 3/3 |
| P2025-C-01（2025 C） | 有参照 | 6 | 5 | 0 | 0 | 5/5 | 5/5 |
| P2025-C-02（2025 C） | 有参照 | 5 | 3 | 1 | 1 | 3/4 | 4/4 |
| P2025-C-03（2025 C） | 有参照 | 1 | 0 | 0 | 0 | - | - |
| P2025-C-04（2025 C） | 有参照 | 4 | 2 | 0 | 0 | 2/2 | 2/2 |
| P2025-C-05（2025 C） | 有参照 | 4 | 2 | 1 | 1 | 2/3 | 3/3 |
| P2025-C-06（2025 C） | 有参照 | 4 | 3 | 0 | 0 | 3/3 | 3/3 |
| P2025-C-07（2025 C） | 有参照 | 4 | 2 | 2 | 0 | 2/4 | 2/4 |
| P2025-C-08（2025 C） | 有参照 | 4 | 3 | 0 | 0 | 3/3 | 3/3 |
| P2025-C-09（2025 C） | 有参照 | 2 | 0 | 1 | 1 | 0/1 | 1/1 |
| P2025-C-10（2025 C） | 有参照 | 2 | 1 | 1 | 0 | 1/2 | 1/2 |
| P2025-C-11（2025 C） | 有参照 | 8 | 6 | 2 | 2 | 6/8 | 8/8 |
| P2025-C-12（2025 C） | 有参照 | 5 | 2 | 1 | 0 | 2/3 | 2/3 |
| P2025-C-13（2025 C） | 有参照 | 4 | 4 | 0 | 0 | 4/4 | 4/4 |
| P2025-C-14（2025 C） | 有参照 | 4 | 2 | 0 | 0 | 2/2 | 2/2 |
| P2025-C-15（2025 C） | 有参照 | 4 | 1 | 0 | 0 | 1/1 | 1/1 |
| P2025-C-16（2025 C） | 有参照 | 5 | 1 | 3 | 3 | 1/4 | 4/4 |
| P2025-C-17（2025 C） | 参照不存在 | 0 | 0 | 0 | 0 | - | - |
| P2025-C-18（2025 C） | 有参照 | 2 | 1 | 1 | 0 | 1/2 | 1/2 |
| P2025-D-01（2025 D） | 有参照 | 5 | 2 | 1 | 1 | 2/3 | 3/3 |
| P2025-D-02（2025 D） | 有参照 | 1 | 1 | 0 | 0 | 1/1 | 1/1 |
| P2025-D-03（2025 D） | 有参照 | 3 | 2 | 0 | 0 | 2/2 | 2/2 |
| P2025-D-04（2025 D） | 有参照 | 3 | 0 | 2 | 2 | 0/2 | 2/2 |
| P2025-E-01（2025 E） | 有参照 | 4 | 2 | 1 | 1 | 2/3 | 3/3 |
| P2025-E-02（2025 E） | 有参照 | 4 | 1 | 2 | 2 | 1/3 | 3/3 |
| P2025-E-03（2025 E） | 有参照 | 5 | 1 | 2 | 1 | 1/3 | 2/3 |
| P2025-E-04（2025 E） | 有参照 | 3 | 1 | 1 | 1 | 1/2 | 2/2 |
| P2025-F-01（2025 F） | 有参照 | 4 | 2 | 2 | 2 | 2/4 | 4/4 |
| P2025-F-02（2025 F） | 有参照 | 4 | 1 | 0 | 0 | 1/1 | 1/1 |
| P2025-F-03（2025 F） | 有参照 | 6 | 2 | 2 | 2 | 2/4 | 4/4 |
| P2025-F-04（2025 F） | 有参照 | 4 | 1 | 0 | 0 | 1/1 | 1/1 |
| P2025-F-05（2025 F） | 有参照 | 2 | 0 | 1 | 0 | 0/1 | 0/1 |

* **参照存在、但模型类条目为 0 的篇**（**单列**，同样不记「不适用」）：P2025-C-03。

### 第四节 · 仍未覆盖的作者模型条目（**逐条**）

共 **10** 条。每条都有一条三态处置 + 理由（分流表里逐条可核）。

| 篇 | 词形 | 处置 | 理由（摘要） |
| :-- | :-- | :-: | :-- |
| P2025-A-05 | `Depth Estimation` | 不收 | 正文 p6 的完整形态是「Depth Measurement of Stairs with Monocular Depth Estimation」⇒ 通行名是 **Monocular Depth Estimation**；`Depth Estimation` 是它的**截短**，收它会让词表命中任何 |
| P2025-B-03 | `Sustainable Tourism Dynamic Model` | 不收 | **复合名（场景词 `sustainable tourism` + 通用模型名 `system dynamics`）**（正文 p1 给了展开：`Sustainable Tourism Dynamics Model (STDM)`）。**其通用模型名 `system dynamics` 已在词表** |
| P2025-B-06 | `logistics growth model` | 不收 | **疑似笔误**：通行名是 `logistic growth model`（正文同篇只出现 `logistics growth model` 这一形态，故无法用正文证伪）。不收录的理由：收它会把笔误固化成词表词条；而正确形态 `logistic growth model` 不在作者的 Keyword |
| P2025-C-07 | `Athlete Potential Index` | 不收 | 它是**评价指标**不是方法（正文 p4 有定义块「**Athlete Potential Index(API)**」）。本表的两条推理轴是「数学任务 × 数据形态」，指标名不在轴内；且它是**该篇自建**的指标。**登记为后选项**：若将来要为「自建指标体系」建轴，再收。 |
| P2025-C-07 | `Event Potential Index` | 不收 | 同 `Athlete Potential Index`（自建评价指标；正文 p1「we introduce the Event Potential Index (EPI) to quantify」）。**登记为后选项**。 |
| P2025-C-10 | `Mixed-` | 不收 | **关键词行的断词伪影**。原文逐字：`Bayesian entropy analysis, Zero-inflated negative binomial regression, Mixed-`（md 下一行是 `effect negative binomial regression, Lapla |
| P2025-C-12 | `Doubly ro-` | 不收 | **关键词行的断词伪影**。原文逐字：`Keywords: Olympic Games; Tobit regression; Hurdle model; Great coach effect; Doubly ro-`（md 下一行是 `**bust estimator; Host country e |
| P2025-C-18 | `GRI Algo-` | 不收 | **关键词行的断词伪影**。原文逐字：`Zero-Inflated Negative Binomial Regression; Association Rules; GRI Algo-`（md 下一行是 `rithm; Mixed-effects Model; Prediction of the L |
| P2025-E-03 | `Lunger-` | 不收 | **关键词行的断词伪影 + 笔误**。原文逐字：`Agroecosystems; Organic agriculture; Lotka-Volterra; Petri-Food Web model; Lunger-`（md 下一行是 `Kutta algorithm`）。**正文实证它是笔误**：同 |
| P2025-F-05 | `Log-` | 不收 | **关键词行的断词伪影**。原文逐字：`Cybersecurity; Hierarchical Interaction Scoring Regression Model; Log-`（md 下一行是 `Enhanced Quadratic Regression Model`）⇒ 原形 `Log-En |

### 第四节 · 口径与边界（**与比值同读**）

1. **`keywords` 栏是行内截取**：实测 **17** 篇的作者 Keywords 段**跨行**（栏里少一截）⇒ **宽参照**那一行的分母把它们补了回来。逐篇与差额见 `tests/papers/recon/coverage-recon.txt`。**主体口径的比值对那 17 篇是下界**（漏掉的尾部条目没进分母）。
2. **「覆盖」是方法族级、不是短语级**：判据是「片里**含**词表词」。实测有若干片是这种情形（例 `PSM-DID model` 由 `PSM`+`DID` 判为覆盖）——**语义上正确**（那两个方法确实在词表里），但读比值时要按这个口径读。逐条在证据文件里。
3. **精确性只复核「可定位」**：`TAGS.md` 二层指针的 `(md, 页, 片段)` 三条同时成立才算可定位。它**证明不了**「这个词在那一处确实被用作模型名」——那是语义判断，本表不出具。
4. **低置信 = `x1` 是形式标记、不是质量判断**（第三节已逐条声明）。
5. **本节的数字与 `tests/papers/reports/coverage-evidence.txt` 同源**（同一次 `compute()`），判据 M-14 **各自解析两份文件**再对账。


