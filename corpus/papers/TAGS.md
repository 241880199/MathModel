# TAGS — 机读索引（三层）· 2025 美赛 O 奖论文

> 合集：`corpus/历届优秀论文/2025美赛O奖论文/`　·　篇数：**43**
> **奖项注记**：本合集 `2025美赛O奖论文` 内**全部为 O 奖（Outstanding Winner）论文**——奖项在合集内统一，故**不设「奖项」栏**（用户 2026-09-26 定案）。
> 稳定 ID **内容无关**（按到达顺序生成）⇒ `ID → 原件` 推不出来，双射表在 `PROVENANCE.md`。

## 局限（必读）

* 词表匹配抓不到「**用了但没写名字**」的模型，也抓不到词表外的模型。**本文件是检索入口，不是完备清单**——先据此定位候选，再读 md 全文。
* `has_*` 各栏的语义是「**md 的 `## ` 标题行里字面出现了该词**」这个事实，**不等于**「论文确实做了敏感性分析」。
* **零区分力登记**（一边占比 > 90%）：has_contents=42/43 · has_assumptions=42/43 · has_notations=39/43 —— 这几栏在本语料上**区分力低**，**不因为它们算得出来就当判据用**。逐栏分布见 `tests/papers/reports/ids-report.txt`。
* `sections` 是 **md `## ` 标题行逐字**（`;` 连接、去 `## ` 前缀）。本语料把「号」与「题」**常分两行排**（`## 1.1` 一行、`## Problem Background` 下一行），本文件**不做「号/题合并」一类推断**——那会把推断写进事实栏。
* `problem_type` = **该篇题目的题型**（`L1 · L2` 全名，`;` 连接）——**读回**自 `corpus/papers/PROBLEM_TYPES.md`（人工逐题读题面后做的标注），**不在索引侧重算**（「同一份事实不在两处各算一次」）。`核心` 与 `附带` 两种标记的标签**都收**（标记只活在标注文件里，本栏只放题型名）；它是**题的属性、不是篇的属性**（同一题号的所有行取值逐字相同）。
* **标注覆盖边界（机读）**：标注题数=67 · 有论文的题=6 · 未配对的题=61 · 覆盖年份=2025 · 未配对逐题=2016 A、2016 B、2016 C、2016 D、2016 E、2016 F、2017 A、2017 B、2017 C、2017 D、2017 E、2017 F、2018 A、2018 B、2018 C、2018 D、2018 E、2018 F、2019 A、2019 B、2019 C、2019 D、2019 E、2019 F、2020 A、2020 B、2020 C、2020 D、2020 E、2020 F、2021 A、2021 B、2021 C、2021 D、2021 E、2021 F、2022 A、2022 B、2022 C、2022 D、2022 E、2022 F、2023 A、2023 B、2023 C、2023 D、2023 E、2023 F、2023 Z、2024 A、2024 B、2024 C、2024 D、2024 E、2024 F、2026 A、2026 B、2026 C、2026 D、2026 E、2026 F —— 本合集只有 2025 的论文，`corpus/官方原题/` 的其余年份**尚无论文产物**（Task 9 才扩），故这些题**有题型、无配对**。

## 第一层 · 逐篇一行（客观栏）

**每篇一行**，字段以 ` | ` 分隔、列表以 `;` 分隔、空值写 `-`。值内的 `|`、`;`、NUL、CR、LF 与反斜杠**一律转义**（前四者写成「反斜杠 + 原字符 / 反斜杠 + 数字」的形式，反斜杠自身写成两个反斜杠）——实测 md 的标题行里确有 `|`（`p(Θ|·)`）与 `;`，不转义会把一条记录静默切成多列。

字段序：

```
stable_id | year | problem | n_pages | n_figures | n_tables | n_equations | models | sections | has_contents | has_assumptions | has_notations | has_sensitivity | has_extension | keywords | problem_type
```

记录（同一行序，**入库文件里就是这一段**）：

```
P2025-A-01 | 2025 | A | 25 | 22 | 6 | 23 | Archard Law;Monte Carlo;Navier-Stokes;correlation coefficient;differential equation;finite difference;partial differential equation;particle swarm optimization;sensitivity analysis;feature selection;hypothesis test;machine learning | Stairs: The Glory of the Ordinary;Summary;Contents;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3  Our Work;2 Assumptions and Justifications;3 Notations;4 Model Preparation;4.1 Data Processing;4.2 Solution of the Wear Depth Distribution;5 Model Ⅰ: Step Wear Analysis Model;5.1 Pedestrian Flow Calculation based on Archard's Law;5.2 Preference Direction Model Based on Wear Depth Distribution;5.3 Walking Patterns Model based on Navier-Stokes Equations;6 Model II: Step Characteristic Analysis Model;6.1 Comparison of Actual and Theoretical Stair Usage Time;6.2 Calculation of Stair Service Life;6.3 Determination of Stair Renovation;6.4 Determination of Material Source;6.5  Research on temporal distribution of the Pedestrian Flow;7 Sensitivity Analysis;7.1  Sensitivity Analysis of 2-D Normal Distribution Model of Wear Depth;7.2 Sensitivity Analysis of Continuity Equation for Simulating Walking Patterns;8 Strengths and Weaknesses;8.1 Strengths;8.2  Weaknesses;9 Conclusion;References;Appendix | 1 | 1 | 1 | 1 | 0 | Wear depth\; Archard\; PSO\; Navier-Stokes\; Mont Carlo method\; | 6 反演与参数估计 · 6.1 由观测反推参数/历史;4 机理建模与仿真 · 4.1 物理/化学机理建模;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-A-02 | 2025 | A | 25 | 12 | 3 | 36 | Archard Law;Bayesian;Gaussian Distribution;Monte Carlo;linear regression | Step Chronicles: A Multiscale Model Linking Wear;Patterns and Temporal Use in Ancient Staircases;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Our Work;Assumptions and Justifications;Notations;Analysis and Modeling;4.1;Data Collection for Staircase Wear;4.2;Fundamental Physical Wear Models;4.3;Walking Frequency Model;4.4;Single-Stage Wear Model;4.5;Consistency of Wear with Available Information;4.6;Stair Durability Prediction;4.7;Repair and Renovation Inspection;4.8;Material Source Identification;4.9;Frequency and Duration Patterns;Model Evaluation and Further Discussion;5.1;Strengths and Limitations of the Model;5.2;Future Directions;Conclusion;References | 1 | 1 | 1 | 0 | 0 | Stair Wear\; Gaussian Distribution\; Monte Carlo Simulation\; Fatigue Damage | 6 反演与参数估计 · 6.1 由观测反推参数/历史;4 机理建模与仿真 · 4.1 物理/化学机理建模;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-A-03 | 2025 | A | 25 | 14 | 8 | 0 | Archard Law;Central Limit Theorem;Gaussian Mixture Algorithm;sensitivity analysis | Stair Wear: Traces of History;Contents;Introduction;1.1;Problem Background;1.2;Our Work;Assumptions and Notations;2.1;Assumptions;2.2;Notations;Stair Wear Model;3.1;Wear Volume Model;W = ∑;3.2;Wear Distribution Model;Dx ∼wi∑;(x) = ∑;(y) = ∑;3.3;Stair Wear Model;G = ∑;Dx ∼wi∑;(x) = ∑;(y) = ∑;3.4;Solution of the Stair Wear Model;Further Problems;4.1;Consistency of Wear Results;PA = Davailable(x,y)∑;x ∑;4.2;The Age of The Stairwell and Reliability;4.3;Repairs or Renovations;RS(d1,d2) = D1(x,y)∑;x ∑;4.4;The Source of The Material;4.5;People Use The Stair on A Typical Day;Sensitivity and Robustness Analysis;5.1;Impact of Material Hardness on Wear Volume;5.2;Impact of Weathering Rate Constant on Wear Volume;5.3;Impact of Reigon on Wear Volume;Strength and Weakness;6.1;Strength;6.2;Weakness;Conclusion;References | 1 | 1 | 1 | 1 | 0 | Stair Wear, Archard Law, Central Limit Theorem, Gaussian Mixture Algorithm | 6 反演与参数估计 · 6.1 由观测反推参数/历史;4 机理建模与仿真 · 4.1 物理/化学机理建模;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-A-04 | 2025 | A | 26 | 14 | 2 | 32 | Archard Law;Bayesian;Markov chain;Markov chain Monte Carlo;Monte Carlo;partial differential equation;particle swarm optimization;sensitivity analysis;correlation coefficient;Gaussian Distribution;differential equation;Credible Intervals;Uncertainty Quantification;system dynamics | Problem Chosen;MCM/ICM;Summary Sheet;Team Control Number;Where Footsteps Collide: A Spatiotemporal;Journey through Staircase Wear;Summary;Stones and other materials in historic building steps undergo continuous, long-;term wear, a process archaeologists examine to uncover valuable insights. To sup-;port archaeological research and long-term maintenance, we propose a wear model;for steps and investigate how measurement data can invert key parameters within;that process.;Several models are established: Model I: Hybrid Wear Model\; Model II: Wear-;parameter Inversion Model, etc.;Before building the models, we identified archaeologists’ data collection method:;using 3D scanners to create point cloud maps, which is cost-effective and non-destructive.;We also gathered data through calculations and set reasonable parameters.;For Model I, we introduced three submodels that form a hybrid wear framework.;Sub-model i, grounded in Archard’s theory and PDEs, provides a probabilistic equa-;tion for archaeological contexts, laying the foundation to describe stair-wear dynam-;ics. Sub-model ii then incorporates a single-parallel hybrid approach, showing how;different single/parallel usage ratios influence final wear through foot traffic\; by ex-;amining how those ratios relate to foot traffic, we determine the influence of stair usage;frequency on final wear. Finally, sub-model iii, based on human dynamics, extends;sub-model ii to produce a 3D wear-depth distribution, applying Gaussian blurring;and random offsets to generate realistic footprints.;For Model II, we devised a comprehensive inversion approach that uses mea-;surement data to estimate optimal wear parameters, taking the hybrid wear equation;from Model I as the forward model. We incorporate stair-material and archaeologi-;cal insights in a Bayesian framework by assigning prior distributions to multiple pa-;rameters. The likelihood function is formed from the residual between measurement;and simulation. After Particle Swarm Optimization (PSO) locates the global optimum,;Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,;capturing parameter uncertainty.;traffic at 30%-40% and usage frequency uncertainty of ±5%-10%.;depth error of ±0.015m and material wear uncertainty of ±10%.;For the advanced tasks 3 & 5, we developed a multi-layer PDE model as well as a;discrete-event simulation model to handle repeated repairs and typical one-day stair;wear. Finally, we performed a sensitivity analysis. The results show that our model;remains stable.;Keywords: PDE, Archard’s theory, PSO, MCMC, Bayesian framework;Contents;Introduciton;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Our Work;Model Preparation;2.1;Assumptions and Justifications;2.2;Notations;Notation;Description;wear height;average pressure;area of application;κ;combined coefficient;β;environment constant;Poisson process arrival rate;α(N);probability of parallel usage of stairs;δ;mean lateral distance between left and right footprints;σ;width of the single-foot peak;Θ;parameter vector;p(Θ);Bayesian prior;p(Θ\|·);Bayesian posterior;2.3;Data Collection and Preparation;Model I: Hybrid Wear PDE Model;3.1;Submodel i: Probabilistic Wear Equation (PWE);3.1.1;Generalized PWE;3.1.2;Bimodal Probability Wear Model;3.2;Submodel ii: Improved PWE Considering Single–Parallel Prob-;ability;3.2.1;Single-File Wear Probability Density;3.2.2;Side-by-Side Wear Probability Density;3.2.3;Single-Parallel Wear Model;3.2.4;Issue of Usage Density;3.3;Submodel iii: Improved PWE considering up-/downstairs pref-;erences;Foot Partitioning in Upstairs and Downstairs;3.3.1;Construction of Foot Distributions and Minor Shifts;Algorithm 1: Build Foot Distribution (Gaussian + Random Offsets);Foot Partition-based Travel Direction Model (FPTDM);Algorithm 2: Explicit Euler Scheme for FPTDM;Model II: Wear Parameter Inversion;4.1;Bayesian inference and smoothing regularization[7];4.2;Improved strategy: Preliminary search via heuristic algorithm;Modeling.;Step A: PSO for Global Optimization;Step B: Local MCMC Sampling;4.3;Application and Solution;1. Simulated Observation Data: True Values and Noise Handling;2. Prior Setup and Objective Function;(a) Priors;(b) Objective Function;3. Numerical Procedure: PSO + MCMC;4. Inversion Results: Table and Comparison;5. Error Distribution and Surface Comparison;6. Discussion and Conclusions;Parameter;True Value;Posterior Mean;± Interval;Rel. Error (%);κ (×10−5);7.2;7.43;±0.32;3.2;T (year);259.4;±2.5;1.0;α(u);0.22;0.21;±0.02;4.5;α(u);0.78;0.80;±0.03;2.6;au;0.13;0.12;±0.01;7.7;bu;53.3;±2.4;3.1;α(d);0.12;0.10;±0.02;16.7;α(d);0.62;0.60;±0.03;3.2;ad;0.11;0.10;±0.01;9.1;bd;43.7;±2.0;4.0;Nup(0∼90);±7;5.0;Nup(90∼180);±5;5.9;Nup(180∼257);±4;3.3;Ndown(0∼90);±6;5.3;Ndown(90∼180);±5;5.3;Ndown(180∼257);±4;2.2;Model III: Refurbishment and Typical One-day Wear;5.1;Multi-layer structural PDE;5.1.1;Worn-out equation;5.1.2;Renovate (add new layer);5.1.3;Penetration conditions;5.1.4;Inverse Problem Solving;5.2;Discrete-Time Simulation Model;Sensitivity Analysis;Strengths and Weaknesses;7.1;Strengths;7.2;Weaknesses;References | 1 | 1 | 1 | 1 | 1 | PDE, Archard’s theory, PSO, MCMC, Bayesian framework | 6 反演与参数估计 · 6.1 由观测反推参数/历史;4 机理建模与仿真 · 4.1 物理/化学机理建模;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-A-05 | 2025 | A | 31 | 15 | 4 | 42 | Archard Law;Bayesian;Weathering Degree Model;sensitivity analysis;CNN;machine learning;Monte Carlo;hypothesis test;cross-validation | Staircase Wear Analysis - Walking Through History;Contents;Introduction;1.1;Problem Background;1.2;Literature Review;1.3;Problem Restatement and Analysis;1.4;Our Work;Preparation;2.1;Notations;2.2;Assumptions;2.3;Detailed Measurement Plan;2.4;Data collection and processing;Analysis and Modeling;3.1;Wear Volume Calculation;Vtotal = ∑;3.2;Model I: Daily foot traffic model based on the Archard equation;3.3;Model II:Wear Distribution Model——solving Problem 2 and 3;Estimate the Age of the Staircase;4.1;Estimate the Age of the Wooden Staircase With C14 Dating Method;4.2;Estimate the Age of the Stone Staircase Using Weathering Degree;4.3;Estimate the Age of the Staircase Using Bayesian Inversion;4.4;Verify the Age Estimate through Confidence Interval Estimation;Further exploration;5.1;Detection of Repairs or Renovations;5.2;Exploring the Consistency Between Wear and Information available;5.3;Analysis of Usage Patterns;Evaluation of Models;6.1;Sensitivity of Model I;6.2;Sensitivity of Model II;6.3;Strength and Weakness;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Stair Wear, Archard Equation, Depth Estimation, Weathering Degree Model, | 6 反演与参数估计 · 6.1 由观测反推参数/历史;4 机理建模与仿真 · 4.1 物理/化学机理建模;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-01 | 2025 | B | 25 | 14 | 1 | 0 | CVM;nonlinear programming;particle swarm optimization;sensitivity analysis;logistic regression;ARIMA;Regression Analysis;linear regression;Monte Carlo | Economy, Ecology, and Social Welfare:A Win-Win;Approach for Sustainable Tourism in Juneau;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Our Work;Model Preparations;2.1;Assumptions and Justifications;2.2;Notations;2.3;Basic components of sustainable tourism;Model Design;3.1;Preprocessing;3.2;Total Economic Profits Section;3.3;Environmental Level Section;3.4;Social Welfare Section;3.5;The Model Results;Sensitivity Analysis;4.1;Policy Variables and Further Discussion;4.2;Reasonably Estimated Parameters Based on CVM;Application of our Model;5.1;Similarities and Differences between Jiuzhaigou and Juneau;5.2;Specific Application in The Tourism Development of Jiuzhaigou;5.3;Policy Analysis and Comparison Based on Model Results;5.4;Advice on Promoting Less-popular Attractions;Model Evaluation;6.1;Strengths;6.2;Weaknesses and Further Discussion;References;MEMORANDUM | 1 | 1 | 1 | 1 | 0 | Sustainable tourism\; CVM\; Multi-objective nonlinear programming | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-02 | 2025 | B | 26 | 14 | 3 | 18 | Pareto;SLSQP;multi-objective optimization;sensitivity analysis;reinforcement learning | Overload Alarm: Pareto Optimization of the;Economic-Social-Environmental Triangle;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Literature Review;1.4;Our Work;Assumptions and Justifications;Notations;Multi-Objective Optimization Model;4.1;Sub-model I: Cost-benefit Analysis Considering Marginal Effects;4.2;Sub-model II: Social Welfare Optimization Model;4.3;Sub-model III: Environmental Carrying Capacity Model;4.4;Pareto Optimal Solution for Total benefit;Results and Extension;5.1;Optimization Objectives;5.2;Constraints Analysis;5.3;Optimization Result Analysis;5.4;Key Parameter Determination;Additional Income and Expenditure Plan;Sensitivity Analysis;7.1;Effect of Changes in Total Tourists and Performance per Tourist;7.2;Effect of Changes in Total benefit;Strengths and Weaknesses;8.1;Strengths;8.2;Weaknesses;Conclusion;References;Memo | 1 | 1 | 1 | 1 | 1 | Sustainable Tourism, Management Measures, Multi-objective Planning Model, Pareto | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-03 | 2025 | B | 26 | 12 | 7 | 24 | AHP;Lotka-Volterra;SIS model;sensitivity analysis;ordinary differential equation;system dynamics;logistic regression;nonlinear regression;cluster analysis | Rebalancing Nature’s Scale: A Model to Tame Overtourism;Memo;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Our Work;Assumptions and Justiﬁcations;Notations;Model Preparation;4.1;Data Collection;4.2;Data Selection Explanation;Model Design;5.1;Sustainable Tourism Dynamics Model (STDM);5.2;Intervention Strategies;Evaluation Model;6.1;Indicators Determination;6.2;Score Calculation Model;6.3;Values of Parameters;6.4;Weights Distribution Outcomes;Analysis of Factors;Results and Discussion;Sensitivity Analysis;9.1;Qualitative analysis: Morris Method;9.2;Quantitative analysis: Local Sensitivity Analysis;Reimagining Big Sur;10.1;Fundamental Information;10.2;Model Validation and Generalization;Strengths and Weaknesses;11.1;Strengths;11.2;Weaknesses;References;Report on Use of AI;OpenAI ChatGPT(Jan 14, 2025 version, ChatGPT-4o);OpenAI ChatGPT(Jan 14, 2025 version, ChatGPT-4o) | 1 | 1 | 1 | 1 | 0 | Overtourism, Sustainable Tourism Dynamic Model, Lotka-Volterra model, SIS model, | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-04 | 2025 | B | 25 | 16 | 5 | 22 | dynamic programming;entropy weight method;multi-objective optimization;sensitivity analysis | Sustainable Tourism Management in Juneau;Contents;Introduction;1.1;Problem Background;1.2;Problem Restatement;1.3;Our Work;Preparation of the Models;2.1;Assumptions;2.2;Notations;2.3;Data Preparation;The Models;3.1;Tourist Demand Model;3.2;Economic Benefit Model;3.3;Environmental Impact Model;Entropy = −∑pi log(pi);3.4;Resident Satisfaction Model;3.5;Model Solving using Dynamic Programming;Sensitivity Analysis;4.1;Average Input of Environmental Index;4.2;Average Input of Resident Satisfaction;4.3;Average Input of Tourist Count;Adaptability of the Model;5.1;Data Collection and Processing;5.2;Adaptation to Miami tourism;5.3;Promotion of Attractions with Fewer Tourists;Strengths and Weaknesses;6.1;Strengths;6.2;Weaknesses;References;Memo: Sustainable Tourism Recommendations for Juneau;Report on use of AI | 1 | 1 | 1 | 1 | 0 | Multi-Objective Model, Dynamic Programming, Sustainable Tourism | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-05 | 2025 | B | 28 | 11 | 2 | 56 | NSGA-II;genetic algorithm;multi-objective optimization;sensitivity analysis;Pareto;deep learning;factor analysis;hypothesis test | Breaking through the Tourism Dilemmas in Juneau: The Road to;Sustainable Development Driven by a Multi - objective Model;Summary;Contents;1 Introduction ...................................................................................................... 3;2 Preparation of the Model ................................................................................ 4;3 Model establishment ........................................................................................ 6;4 Model Solution ................................................................................................ 15;5 Sensitivity Analysis ......................................................................................... 20;6 Model Evaluation and Further Discussion .................................................. 21;7 The Promotion of the Model in Other Regions ........................................... 22;8 Memo ............................................................................................................... 24;References .......................................................................................................... 25;AI Use Report .................................................................................................... 26;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Preparation of the Model;2.1 Assumptions and Explanations;2.2 Notations;3  Model establishment;3.1 Optimization Objectives Setting;3.2 Definition of Decision Variables;3.3 Construction of the Objective Function;3.4 Setting of Constraints;4 Model Solution;4.1 Data Processing and Function fitting;We use the gradient descent method. Based on a set of collected data ;4.2 Model Solution Based on NSGA-II;4.3 Analysis of the solution results and selection of the optimal solution;5 Sensitivity Analysis;6 Model Evaluation and Further Discussion;6.1 Strengths;6.2 Weaknesses;6.3 Further Discussion;7 The Promotion of the Model in Other Regions;8 Memo;References;AI Use Report | 1 | 1 | 1 | 1 | 0 | Sustainable tourism\; Juneau\; Multi - objective optimization\; NSGA - II | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-06 | 2025 | B | 26 | 13 | 3 | 5 | L-BFGS-B algorithm;differential equation;sensitivity analysis;system dynamics | The Triangular Balance of Environment, Economy, and;Society: A System Dynamics-Based Model for;Sustainable Tourism Management;Contents;Introduction;1.1;Background;1.2;Restatement of the Problem;1.3;Our Work;Model Preparation;2.1;Basic Ideas;2.2;Overview of the Model;Assumptions and Justifications;3.1;Tourists Number Dynamics;3.2;Environmental Degradation;3.3;Infrastructure Level;3.4;Resident Satisfaction;3.5;Tax Allocation;3.6;System Dynamics;3.7;Scenario Simulation;3.8;Model Adaptability;Notations;Models;5.1;Dynamic Equation for Tourist Volume;5.2;Infrastructure Level Equation;5.3;Environmental Degradation Equation;5.4;Resident Satisfaction Equation;5.5;Tax Revenue Model;5.6;Dynamic Interactions in Sustainable Tourism Management Framework;5.7;Significance for Achieving Sustainable Tourism Development;The Solution of Juneau;Sensitivity Analysis;7.1;Synergistic Effects of Environmental Investment and Tax Rates on Tourist;Volume;7.2;Gain Mechanism of Infrastructure Investment and Additional Expendi-;tures on Satisfaction;7.3;Coupled Effects of Tax Policies and Environmental Governance;7.4;Phased Policy Strategies for Sustainable Tourism Development;Model extension;8.1;Data Analysis of Sanya;8.2;The Solution of Sanya;8.3;Promoting Undervisited Destinations via Dynamic Models;Model Evaluation and Future Discussion;9.1;Advantages;9.2;Limitations;9.3;Future Directions;Conclusions;References;Memo to the Tourist Council of Juneau;Report on Use of AI | 1 | 1 | 1 | 1 | 1 | System Dynamics\; differential equations\; logistics growth model\; dynamic feedback loops\; | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-B-07 | 2025 | B | 25 | 13 | 3 | 25 | AHP;NSGA-II;Pareto;multi-objective optimization;sensitivity analysis;genetic algorithm;system dynamics;Regression Analysis;nonlinear regression;structural equation modeling;correlation coefficient | From TBMP to TSMP: Juneau’s Tourism Never Ends;Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 5;3 Notations ........................................................................................................... 6;4 Model Preparation ........................................................................................... 7;5 Sustainable Tourism Optimization Model ..................................................... 8;6 Sensitivity Analysis ......................................................................................... 18;7 Expansion of the Model ................................................................................. 20;8 Model Evaluation ........................................................................................... 23;Memo .................................................................................................................. 24;References .......................................................................................................... 25;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Literature Review;1.4 Our Work;2 Assumptions and Justifications;3 Notations;Number of daily visitors to the attraction i;attractioni Visitor Fees;Increase in attractioni Visitor Fees;4 Model Preparation;4.1 Data Overview;4.2 Data Collection;4.3 Description of Tourism in Juneau;5 Sustainable Tourism Optimization Model;5.1 Multi-Objective Optimization Model;Criteria;1.45;3.2;0.69;2.2;0.31;0.45;5.2 NGSA-II for Multi-objective Optimization;5.3 Expenditure-Feedback Model for Additional Revenue;6 Sensitivity Analysis;7 Expansion of the Model;7.1 Expansion Model for the Maldives;7.2 Expansion Model in low-tourist-volume areas;8 Model Evaluation;8.1 Strengths;8.2 Weaknesses;Memo;✓ Tourism Sustainable Management Plan;sion, and should also spend more on environmental protection projects;✓ Optimization suggestions;References | 1 | 1 | 1 | 1 | 0 | Sustainable Tourism\; Multi-Objective Optimization\; NSGA-II Algorithm\; Sensitivity | 3 优化 · 3.3 多目标/权衡;4 机理建模与仿真 · 4.6 反馈结构与动态演化;1 预测 · 1.3 情景与概率预测;5 统计推断与因果 · 5.4 不确定性与敏感性
P2025-C-01 | 2025 | C | 26 | 17 | 5 | 7 | LSTM;SHAP;XGBoost;bootstrap;difference-in-differences;machine learning;principal component analysis;hypothesis test;sensitivity analysis;correlation coefficient;Markov chain;time series analysis;cross-validation;stacking;logistic regression;deep learning;reinforcement learning;Bayesian;cluster analysis;gradient boosting;random forest | Olympic Multi-dimensional Predictive Integrator;Contents;Introduction ·················································;Preparation for Modeling ····································;Problem 1: Medal Prediction ································;Problem 2: The "Great Coach" Effect ······················· 18;Problem 3: New Insights ····································· 19;Sensitivity Analysis ·········································· 21;Model Analysis··············································· 22;Memorandum················································ 24;Reference ···················································· 25;Introduction;1.1;Problem Background;1.2;Clarifications and Restatements;1.3;Our Work;Preparation for Modeling;2.1;Model Assumptions;2.2;Notations;2.3;Data Preprocessing;Problem 1: Medal Prediction;3.1;Medal Ranking;3.2;Breaking the Zero;3.3;Olympic Events and Medal Counts;Problem 2: The "Great Coach" Effect;4.1;DID Modeling;4.2;Hypothesis Testing and Contribution Coefficient Analysis;Problem 3: New Insights;Sensitivity Analysis;6.1;The Number of Principal Components;6.2;Prediction Model Evaluation;Model Analysis;7.1;Strength;7.2;Weekness and Further Discussion;Memorandum;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Prediction Model, PCA, LSTM, XGBoost, SHAP, DID | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-02 | 2025 | C | 25 | 12 | 11 | 12 | Bayesian;Tobit;XGBoost;change-point detection;hurdle model;machine learning;random forest;two-stage least squares;Causal Inference;sensitivity analysis;decision tree;stacking;zero-inflated;principal component analysis;logistic regression;correlation coefficient;difference-in-differences;neural network | Medal Prediction Based on Tobit and Hurdle Models;and Great Coach Effect Insights;Summary;Contents;Introduction;1.1;Background;1.2;Restatement of the Problem;1.3;Literature Overview;1.4;Our Work;Assumptions and Justification;Notations;Data Processing;4.1;Data Cleaning;4.2;Data Overview;Comparative Modeling of Olympic Medal Projections: Hurdle-;Tobit Framework with Host Country Strategy Analysis;5.1;Hurdle and Tobit Models;5.2;Model Selection and Validation;5.3;2028 Los Angeles Olympics Medal Count Projections;5.4;Projecting First-Time Medal Winners and Probability Estimates;5.5;The Influence of Item Selection on the Number of Medals;The Great Coach Effect: A Strategy Optimization Study;Based on Bayesian Change-Point Detection and Causal In-;ference Models;6.1;Discovery of Great Coach Effect Based on Bayesian Change-Point;Detection;6.2;Quantitative Evaluation of Great Coaching Effect on Medal Counts;6.3;Targeted Coaching Investments for Three Nations;Insights: Strategic Resource Allocation and Path Depen-;dency in Olympic Medal Performance;7.1;Dynamic Attenuation of the Host Country Effect and Resource Re-;distribution;7.2;The “Double-Eged Sword Effect” of the Number of Events and Sports;Sensitivity Analysis;Model Evaluation;9.1;Strength;9.2;Weakness;References | 1 | 1 | 1 | 1 | 0 | Tobit, Hurdle, 2SLS, Bayesian Change-Point Detection, Medal Prediction | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-03 | 2025 | C | 26 | 20 | 11 | 0 | Monte Carlo;bootstrap;linear regression;logistic regression;machine learning;principal component analysis;random forest;neural network;sensitivity analysis;regression discontinuity;feature selection;Regression Analysis;decision tree;cross-validation | Olympic Medal Prediction Model Based on;Regression and Machine Learning;Summary;Contents;Introduction;1.1;Background;1.2;Restatement of the Problem;1.3;Our work;Assumptions and Justification;Notations;Data Preprocessing;4.1;Data Cleaning and Adjustments;4.2;Data Exploration;Multiple Linear Regression-Feedforward Neural Network;Bootstrap Ensemble Interval Prediction Model with Host;Effect;5.1;Reasons for Model Selection;5.2;Model Construction and Fusion;5.3;Forecast Results and Insights;5.4;Uncertainty and Evaluation Analysis;Logistic Regression and Random Forest Prediction Model;for First-Time Medalist Countries;6.1;Reasons for Model Selection;6.2;Feature Engineering;6.3;Analysis of Conditions for Countries Winning Medals for the First;Time;6.4;Model Formulation and Prediction Results;6.5;Estimate odds;Strategic Importance Assessment Model for Olympic Sports;(SIAMOS);7.1;Model Development and Evaluation Framework;7.2;Result 1: Relationship Between Events and Medal Counts;7.3;Result 2: Sport-Specific Importance Across Nations;7.4;Result 3: Impact of Host Nation’s Event Selection on Medal Outcomes;Contribution of the Great Coach;8.1;Definition of Great Coach;8.2;Data Processing Framework;8.3;Calculation of Coeﬀicients Based on Breakpoint Regression Model;8.4;Case Study Analysis (Focusing on Three Key Sports);The Practical Application of the ”Great Coach” Effect;9.1;Selection of Sports Needing a Great Coach;9.2;Results;Other Insights: Host Country Spillover Effect on Medal;Rates of Neighboring Countries;10.1;Analysis and Results;10.2;Strategic Recommendation for National Olympic Committees;Sensitivity Analysis;Initial Feature Values and Sensitivity Ranges;Results and Observations;Strengths and Weaknesses;Strengths;Weaknesses;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Olympic medal prediction\;Strategic Importance Assessment Model for Olympic | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-04 | 2025 | C | 31 | 15 | 7 | 0 | Monte Carlo;linear regression;random forest;Uncertainty Quantification;sensitivity analysis;machine learning;Regression Analysis;zero-inflated;feature selection;ARIMA;exponential smoothing;time series analysis | 2028 Olympic Medal Predictions Based on Random;Forest Model;Contents;Introduction;1.1;Background;Faster, Higher, Stronger – Together;-The Olympic Motto;1.2;Problem Analysis;Assumptions;Models;3.1;Task 1: Establishment and Analysis of the Medal Ranking Prediction;Model for the 2028 Olympic Games;3.2;Task 2: Prediction of First-time Medal-winning Countries;3.3;Task 3: Critical Sports/Disciplines;3.4;Task 4: The Great Coach Model;3.5;Our Unique Insights into Olympics Medals And Suggestions for NOC;Conclusions;Report on Use of AI | 1 | 1 | 0 | 0 | 0 | Olympics, Medal Prediction, Random Forest Model, Monte Carlo Simulation | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-05 | 2025 | C | 25 | 21 | 13 | 21 | GSRF;cross-validation;lasso;logistic regression;random forest;sensitivity analysis;ARIMA;moving average;time series analysis;decision tree;machine learning;correlation coefficient;linear regression | Olympic Medals Unveiled:;A Mathematical Exploration of Achievement Trends;Summary;Contents;1 Introduction;1.1 Background;1.2 Clarifications and Restatements;1.3 Our work;2 Basic Assumption; Hypothesis 1: Assume that the number of athletes participating in the 2028;in 2024.;the calculation of the model, it is assumed that the number remains constant.;3 Symbols;4  Data Preprocessing;5 Task 1 Predicting Gold & Total Medals Based on GSRF Model;5.1 GSRF Prediction Model;b)  United States Total Predict;5.2 Predicting the 2028 Gold & Medal Tables;y  represents the predicted value,;and the total prediction interval for the number of medals is ;6 Task 2 Projections for Non-Awarded Countries;6.1 Bicategory Logistic Regression Modeling;6.2;Bicategory Logistic Regression Results;7 Task 3 Relationship Between Sports and Medals;7.1 Relationship of the Sports to gold medals & total medals;7.2 The most Important Sports for the Country;7.3 Impact of Nationally Selected Sports on results;8 Task 4 The Impact of Great Coach;8.1 Lasso Regression Model;8.2 Lasso Regression Results;9 Task 5 Original Opinion;9.1 Host Effect;9.2 Talented Athletes;10 Error Analysis and Sensitivity Analysis;10.1 Definition of Sensitivity;10.2 Impact of Athletes Number, Gold & Total Medals on Predicted Results;11 Evaluation of Model;12 References | 1 | 1 | 0 | 1 | 0 | Olympic；GSRF；Logistic Regression；Lasso Regression | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-06 | 2025 | C | 29 | 26 | 11 | 0 | ARIMA;Monte Carlo;linear regression;moving average;random forest;cluster analysis;sensitivity analysis;K-means;logistic regression;decision tree;time series analysis | 2028 LA Olympics: Who Will Dominate the Medal;Count?;Contents;Introduction;1.1;Background;1.2;Problem Restatement;Notations & Assumputions;Data Processing;3.1;Clustering Analysis;3.2;Country Classiﬁcation;3.3;Event Addition and Removal;Task 1: Olympic Medal Prediction and Analysis;4.1;2028 Medal Table Prediction;4.2;Analysis of the Relationship Between Events and Medals;Task 2: Great Coaches;5.1;Evidence of the Great Coach Eﬀect;5.2;Selection of Three Countries and Speciﬁc Sports;Task 3: Recommendations;Model Evaluation;7.1;Sensitivity Analysis;Model Evaluation;Reference;References;Report on Use of AI;AI Tools Usage Report | 1 | 0 | 1 | 1 | 0 | ARIMA, Random Forest, Linear Regression, Olympic Medal Predic- | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-07 | 2025 | C | 24 | 15 | 14 | 6 | BP neural network;bootstrap;neural network;random forest;sensitivity analysis;cross-validation;SVM;XGBoost;linear regression;decision tree;machine learning | Maximizing Medal Performance: Athlete and Event;Potential Indices;Contents;Introduction;1.1;Background;1.2;Restatement of Problem;1.3;Our work;Preparation for Modeling;2.1;Assumptions;2.2;Notations;2.3;Data Processing;Task 1: Medal Count Prediction Model;3.1;Feature Engineering;3.2;Model Selection;3.3;Task 1.1: 2028 Olympic VMT Prediction;3.4;Task 1.2: The Probability of First Medal;3.5;Task 1.3: The Impact of Events on Medals;Task 2: “Great Coach” Contribution to Medals;4.1;Existence of “Great Coach” Effect;4.2;Contribution of "Great Coach";4.3;Event Investment and Impact;Task 3: Other Original Insights;5.1;Common Traits of No Medal Nations;5.2;Negative Impact Events;5.3;Recommendations of “Great Coach”;Model Analysis;6.1;Sensitivity Analysis;6.2;Strengths and Weaknesses;Conclusions;References | 1 | 1 | 1 | 1 | 0 | Athlete Potential Index\; Event Potential Index\; Random Forest\; BP Neural Network | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-08 | 2025 | C | 25 | 18 | 2 | 15 | K-means;SHAP;bootstrap;cluster analysis;correlation coefficient;cross-validation;difference-in-differences;propensity score matching;sensitivity analysis;stacking;machine learning;SVM;XGBoost;decision tree;gradient boosting;logistic regression;random forest;Regression Analysis | 2028 Olympic Medal Predictions:;Multi-Effect Analysis and Strategic Insights;Contents;Introduction;1.1;Problem background;1.2;Restatement of the problem;1.3;Our work;Assumptions;Notations;Data Pre-processing;Task 1: 2028 Olympics Medal Prediction Model;5.1;Develop a model for medal counts for each country;5.2;Prediction for the Olympics in 2028;Task 2: Multifaceted analysis for Predicting the Next "First-;Medal" Winner;Task 3:Exploration of the Relationship Between Olympic;Events and Medal Wins;7.1;Explore the relationship between the events and how many medals;countries earn;7.2;Most important sports for different countries;7.3;Impact of Host Country’s Event Selection on medal;Task 4: Analysis of the "Great Coach" Effect and Its Im-;pact on Medals’ Performance;8.1;The effect contributes to medal counts;8.2;3 Countries should consider investing "Great Coach";Model Testing;9.1;Tests of the stacking model;9.2;Tests of the PSM-DID model;Letter;References | 1 | 1 | 1 | 0 | 0 | Medal predictions \; Stacking ensemble \; SHAP analysis \; PSM-DID model | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-09 | 2025 | C | 22 | 6 | 9 | 12 | Bayesian;Credible Intervals;Markov chain Monte Carlo;Posterior inference;Regression Analysis;Uncertainty Quantification;sensitivity analysis;deep learning;RNN;machine learning;Markov chain;Monte Carlo;XGBoost;LSTM;random forest | A Glimpse of Olympics Medals through Bayesian Model;Contents;Introduction;1.1;Background;1.2;Problem Restatement;1.3;Our Work;Assumptions and Justifications;Notations;Data Pre-processing;4.1;Data Cleaning;4.2;A glimpse of dataset;Task 1: Predicting Medals of 2028 LA Olympics;5.1;Key Variables Influencing Olympic Medal Success;5.2;Bayesian Hierarchical Dirichlet–Multinomial (BHDM) Model;5.3;Projects of LA 2028;5.4;The country that will achieve a Breakthrough From Zero;5.5;Important Sports and Home Event Impact;Task 2: Dive Into Great Coach Effect;6.1;What is a Great Coach?;6.2;Great Coach Affect the Medals;6.3;Invest in Great Coach and Estimate its Impact;Sensitivity Analysis;7.1;Sensitivity Analysis for 𝜏2 Values;7.2;Sensitivity Analysis of Equal Distribution Assumptions;Strengths and Limitation of the Proposed Model;Task 3: Other Original Insights of Our BHDM Model;9.1;Economic level determines medals;9.2;Home Turf and Aligned Systems Prevail;9.3;Emerging Sports Aid Low-GDP Countries;9.4;A letter to inform NOC;Some insights about Olympics Medal Counts;To: Country Olympics Committees;From: Team #2513314;Data: January 27, 2025;Dear Country Olympics Committees leaders:;References | 1 | 1 | 1 | 1 | 0 | Bayesian Hierarchical Dirichlet-Multinomial, Posterior inference, Uncertainty | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-10 | 2025 | C | 27 | 25 | 5 | 22 | Bayesian;Laplace smoothing;sensitivity analysis;zero-inflated;SHAP;SVR;bootstrap;difference-in-differences;genetic algorithm;neural network;Causal Inference;time series analysis;cross-validation;machine learning;Shannon entropy;decision tree;principal component analysis | Unveiling 2028 Glory: Data-Driven Predictions and;Strategic Insights via Advanced Statistical Models;Contents;Introduction;1.1;Problem Background;1.2;Problem Restatement;1.3;Literature Review;1.4;Data Cleaning;1.5;Our Work;Assumptions and Justiﬁcations;Notations;Multi-level integrated forecasting model;4.1;Mixed effects negative binomial regression model;4.2;Zero expansion negative binomial model (ZINB);4.3;Relationship between the Events and Countries;4.4;Project Selection and its Impact;4.5;Sensitivity Analysis;Entropy model based on Bayesian Modiﬁcation;5.1;Model Selection Background;5.2;The Establishment of the Mathematical Model;5.3;Case Analysis;5.4;The result of the mathematical model;5.5;Sensitivity Analysis;Original Insights;6.1;Analysis of "Potential Medal" in Non-Medal-Winning Nations;6.2;The Multiplier Effect of Elite Coaches;6.3;Dual Nature of Host Effect;6.4;The reference value of Cold War factors;Strengths and weaknesses;7.1;Strengths;7.2;Weaknesses;Conclusion;References;Report on the Use of AI | 1 | 1 | 1 | 1 | 0 | Bayesian entropy analysis, Zero-inﬂated negative binomial regression, Mixed- | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-11 | 2025 | C | 30 | 21 | 7 | 23 | Cox proportional hazards;LSTM;Mann-Kendall;Monte Carlo;SVR;Threshold Method;XGBoost;isolation forest;linear regression;random forest;sensitivity analysis;stacking;SVM;gradient boosting;grey prediction;machine learning;neural network;time series analysis;ARIMA;Regression Analysis;cross-validation;decision tree;survival analysis;cluster analysis | Sketch an Olympic Vision;Summary;Contents;Introduction;1.1;Background;1.2;Literature Review;1.3;Problem Restatement;1.4;Our Work;Assumptions and Justification;Notations;Model I : Event Prediction based on SVR;4.1;Model Overview;4.2;Model Establishment;4.3;Results;4.4;Analysis of the importance of different sports;Model II : Medal Prediction based on LSTM and XGBoost;5.1;Model Overview;5.2;Data Preparation;5.3;Baseline: LSTM model;5.4;Advanced: XGBoost model;5.5;Examining the confidence of the prediction interval;5.6;A Mann-Kendall-based analysis to project significant change in medal;acquisition;Model III: First-time Medalist Prediction based on Cox;Proportional Hazard Model;6.1;Model Overview;6.2;Theoretical Basis;6.3;Key Predictors of First-time Medalists;6.4;Model establishment;6.5;Model Fitting and Prediction;6.6;Monte Carlo Simulation;Model IV: Great Coach Effect;7.1;Model Overview;7.2;Effect Evidence;7.3;GCE contribution to medal counts;7.4;GCE influence on certain sports;7.5;Application and Estimation;Insights;8.1;From Models Above;8.2;Extra Study: Impact of Gender Ratio;Sensitivity Analysis;Strength and Weakness;10.1;Strength;10.2;Weakness;10.3;Room for Improvement;References;Appendices;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Threshold Method, SVR, XGBoost, LSTM, Mann-Kendall, Cox, Isolation Forest, Linear Regression, | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-12 | 2025 | C | 26 | 12 | 5 | 13 | ARIMA;SARIMA;Tobit;correlation coefficient;difference-in-differences;hurdle model;logistic regression;sensitivity analysis;time series analysis;linear regression;particle swarm optimization;cluster analysis;machine learning;propensity score matching | From Models to Medals: The Winning Formula Behind the Data;Summary;Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 4;3 Notations ........................................................................................................... 5;4 Data processing................................................................................................. 5;5 Model 1: Predict Olympic medal counts by TMP-OMP Model. ................. 6;6 Model 2: Analysis “great coach” effect by DRD-CE Model. ..................... 16;7 The Solution of Problem 3 ............................................................................. 21;8 Sensitivity Analysis ......................................................................................... 23;9 Model Evaluation and Further Discussion .................................................. 24;10 References ..................................................................................................... 25;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Assumptions and Justifications;3 Notations;4 Data processing;5 Model 1: Predict Olympic medal counts by TMP-OMP Model.;5.1 Explanation of the Dynamic Country Characteristics and Constant;Country Properties;5.2 The Establishment of Model 1;Inspired by the works of [3,4], we developed the Tobit-Mundlak- Hurdle Olympic;5.3 The Solution of Problem 1 by Model 1.;Countries;Algorithm 1 Calculate the contribution of Sport Contribution Score;6 Model 2: Analysis “great coach” effect by DRD-CE Model.;6.1 The Establishment of Model 2;6.2 The Solution of Problem 2 by Model 2;7 The Solution of Problem 3;7.1 Former host effect and Subsequent host effect.;7.2 Strategies to Enhance Olympic Participation and Global Influence.;8 Sensitivity Analysis;9 Model Evaluation and Further Discussion;9.1 Strengths;9.2 Weaknesses and Further Discussion;10 References | 1 | 1 | 1 | 1 | 0 | Olympic Games\; Tobit regression\; Hurdle model\; Great coach effect\; Doubly ro- | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-13 | 2025 | C | 27 | 14 | 8 | 21 | SHAP;XGBoost;bootstrap;cross-validation;difference-in-differences;sensitivity analysis;Tobit;hurdle model;machine learning;decision tree;Bayesian;feature selection;logistic regression;random forest;time series analysis;linear regression;neural network;hypothesis test;Regression Analysis;gradient boosting;stacking | Revealing the Hidden Forces Shaping Olympic Success;Summary;Table of Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 4;3 Notations ........................................................................................................... 5;4 Model Preparation ........................................................................................... 5;5 Model I: Dual-staged XGBoost Medal Prediction ........................................ 6;6 Evaluation and Application of the Dual-Stage XGBoost Model ............... 12;7 Model II: DID Regression Evaluating the Great Coach Effect ................. 17;8 Novel Insights from SHAP Analysis in Olympic Performance .................. 22;9 Sensitivity Analysis ......................................................................................... 24;10 Model Evaluation ......................................................................................... 24;References .......................................................................................................... 25;Report on Use of AI ........................................................................................... 26;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Assumptions and Justifications;3 Notations;4 Model Preparation;4.1 Data Pre-processing;5 Model I: Dual-staged XGBoost Medal Prediction;5.1 Parameterization of Influencing Factors;5.2 Developing of the XGBoost Classifier;5.3 Developing of the TPE-XGBoost Regressor;6 Evaluation and Application of the Dual-Stage XGBoost Model;6.1 Model Evaluation Metrics;6.2 Evaluation of Model Prediction Accuracy;6.3 Solving Confidence Intervals with the Non-parametric Bootstrap Algo-;rithm;6.4 Application and Analysis of the Model for the 2028 Olympics;6.5 Analysis of the Correlation between China-US Olympic Medals and;Events Based on SHAP Values;7 Model II: DID Regression Evaluating the Great Coach Effect;7.1 Identifying Independent Variables;7.2 DID Model Building;7.3 Solution of the Model;8 Novel Insights from SHAP Analysis in Olympic Performance;9 Sensitivity Analysis;10 Model Evaluation;10.1 Strengths;10.2 Weaknesses;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Dual-stage XGBoost\; Non-parametric Bootstrap algorithm\; DID model\; SHAP model | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-14 | 2025 | C | 26 | 24 | 11 | 16 | Bayesian;Bayesian network;Cox proportional hazards;LSTM;Markov chain Monte Carlo;Monte Carlo;difference-in-differences;sensitivity analysis;spatio-temporal modeling;time series analysis;factor analysis;deep learning;Causal Inference;hypothesis test;centrality;neural network;correlation coefficient;Uncertainty Quantification;CNN;self-organizing map | "Golden Dynamics: Bayesian-AI Olympic Forecasting with;Geopolitics & Coaching";Summary;Contents;Introduction;1.1;Background;1.2;Restatement of the Problem;1.3;Our work;Assumptions and Justifications;Notations;Model Preparation;4.1;Data Overview;4.2;temporal extension of Bayesian networks;4.3;Preparation for the G - Coach Impact Quantifier (GCIQ);(HARMONIE) Hierarchical Adaptive Reasoning Model;5.1;Three - Layer Model Architecture;5.2;Results and Analysis;(CHAMPS)Cox Hazard Analysis and Monte Carlo Pre-;diction Model;6.1;Cox Proportional Hazards Model;6.2;Problem - Solving and Result Analysis;Project Selection Strategy and Quantification of Na-;tional Advantages;7.1;Event Influence and National Dependence Evaluation Model;7.2;Verification and Sensitivity Analysis of Host’s Agenda - Setting;(GCIQ)G-Coach Impact Quantifier Model;8.1;Full - Process Analysis of Cross - National Coaches;Emergent Patterns and Strategic Regulation of Olympic;Medal Distribution;9.1;Conclusions and Recommendations;Sensitivity Analysis;10.1;Univariate and Global Sensitivity Analysis via Sobol’ Indices;10.2;Global Sensitivity Analysis via Sobol’ Indices;10.3;Dynamic Stability and Structural Sensitivity Under Regime Shifts;Evaluation of Strengths and Weaknesses;11.1;Strengths;11.2;Weaknesses and Further Improvements;References;Report on Use of AI | 1 | 1 | 1 | 1 | 1 | Olympic medal prediction\;dynamic Bayesian networks\;Cox-Monte Carlo\;great | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-15 | 2025 | C | 25 | 16 | 12 | 21 | XGBoost;cross-validation;hypothesis test;lasso;logistic regression;machine learning;neural network;random forest;sensitivity analysis;deep learning;linear regression;ridge regression;time series analysis;decision tree;feature selection;grey relational analysis | Who will dominate the 2028 Olympic Games?;Summary;Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 5;3 Notations ........................................................................................................... 5;4 Data Pre-processing and Visual Analytics ..................................................... 6;5 Olympic Medal Prediction Based on Machine Learning ............................. 8;6 The Study of a “Great Coach” Effect ......................................................... 17;7 Predicting Olympic Medals: Insights and Strategies ................................. 21;8 Sensitivity Analysis and Error Analysis ....................................................... 22;9 Strengths and Weaknesses ............................................................................. 24;10 Conclusion ..................................................................................................... 25;References .......................................................................................................... 25;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Literature Review;1.4 Our Work;2 Assumptions and Justifications;3 Notations;4 Data Pre-processing and Visual Analytics;4.1 Data Pre-processing;4.2 Visual Analytics;5 Olympic Medal Prediction Based on Machine Learning;5.1 Medal Table Prediction Model Based on Random Forest;5.2  Prediction of First Medal Wins for Medal-less Countries;5.3 Analysis of Factors Influencing Country Medal Counts;6 The Study of a “Great Coach” Effect;6.1 Analysis of the “great coach” effect;6.2 Contribution of “great coach” Based on the Logistic;(ˆ;6.3 Investment in “great coach”;7 Predicting Olympic Medals: Insights and Strategies;7.1 The Number of Participating Athletes and the Potential to Win Medals;7.2 Medal Distribution of Different Countries in Various Events;7.3 Set Advantageous Events;8 Sensitivity Analysis and Error Analysis;8.1 Sensitivity Analysis;8.2 Error Analysis;9 Strengths and Weaknesses;9.1 Strengths;9.2 Weaknesses;10 Conclusion;References | 1 | 1 | 1 | 1 | 0 | Olympics \; medal prediction \; Machine Learning \;“great coach” effect | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-16 | 2025 | C | 25 | 23 | 3 | 22 | Bayesian;LR-SCAD Model;Residual Analysis;SARIMA;TrueSkill;sensitivity analysis;random forest;Gaussian Distribution;time series analysis;linear regression;moving average;decision tree;stacking;Monte Carlo;deep learning | Beyond Medals: A Predictive Model for Olympic Success and;Identifying Opportunities;Summary;Contents;Introduction;1.1;Problem Background;1.2;Restatement of The Problem;1.3;Our Work;Assumptions;Notations;Data Preprocessing;Medal Projection Model;5.1;TrueSkill Sports Performance Evaluation Model;5.2;SARIMAX-Bayesian Model: Predicting Future Medals;5.3;Random Forest Model: Predicting Medals in New Events;5.4;Model Aggregation;5.5;Model Evaluation;Task 1: Medal Prediction and Analysis for the 2028 Olympics;6.1;Medal Table Projections;6.2;First Ever Medal;6.3;Task 1.3;Task 2: Great Coach Effect;7.1;Residuals Test: Evidence of Changes That Might Be Due to Great Coach;Effect;7.2;LR-SCAD: Estimate Great Coach Effect Contributes To Medal Counts;7.3;Choose three countries and identify sports where they should consider;investing in a “great” coach and estimate that impact;TASK 3: Oringinal Insights;8.1;Insights and Recommendations for Countries That Have Never Won Medals;8.2;Insights and Advice for NOCs on Deploying Experienced Athletes;Model Evaluation;Sensitivity Analysis;Conclusion;References | 1 | 1 | 1 | 1 | 0 | TrueSkill, SARIMAX, Residual Analysis, LR-SCAD Model, Great Coach Effect | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-17 | 2025 | C | 25 | 6 | 18 | 0 | Regression Analysis;Tobit;cluster analysis;moving average;probit;time series analysis;hurdle model;Bayesian;linear regression | The Best of the Best: Olympic Medal Tables;Summary;Contents;Introduction;1.1;Problem Restatement;Data Pre-Processing;Problem 1: Medal Forecasting;3.1;Variable Definitions;3.2;General Assumptions;3.3;Tobit Model;3.4;Mixed Linear Models (MLMs) in a Hierarchical Framework;3.5;Projections for Countries Yet to Earn Medals;3.6;Analyzing Impacts of Events and Sports;Problem 2: Detecting and Utilizing the Great Coach Effect;4.1;Detecting the Great Coach Effect;4.2;Estimating Impacts of Great Coaches;4.3;Identifying Country-Sport Pairs Fit for Great Coaches and Estimating Impacts;Problem 3: Insights into Olympic Medal Counts;Strengths and Weaknesses;6.1;Hierarchical Regression Model;6.2;Time Series Analysis with Moving Average Model;Conclusion;Works Cited | 1 | 1 | 0 | 0 | 0 | - | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-C-18 | 2025 | C | 25 | 13 | 12 | 16 | Bayesian;Markov chain;Markov chain Monte Carlo;Mixed-effects Model;Monte Carlo;association rules;zero-inflated;analysis of variance;machine learning;logistic regression;Cox proportional hazards | From Data to Podiums: A Study for Olympic Medal;Forecasting;Contents;Introduction;1.1;Background;1.2;Problem Restatement;1.3;Our Work;Assumptions and Notations;Data Preprocessing;Who Will Rule the Medal Race at the 2028 LA Olympics?;4.1;Count Regression Model;4.2;Zero-Inflated Model;4.3;Zero-Inflated Negative Binomial Model;4.4;Fitting the Model Using Bayesian Inference and MCMC;4.5;Problem Solutions;4.6;Results;4.7;Model Assessment;How Events of Various Sports Impact the Results?;5.1;Establishment of Indicators;5.2;Events-Medals Association Rule Model Based on GRI Algorithm;5.3;Results Analysis;Could a Great Coach Boost Your Country’s Medal Count?;6.1;Analysis of Variance, Mixed-effects Model;6.2;Definition of the Response Variable;6.3;Problem Solutions;6.4;Fitting the Model;6.5;Results;What Else Is Included in Our Model?;Model Evaluation;8.1;Advantages;8.2;Limitations;References | 1 | 1 | 1 | 0 | 0 | Zero-Inflated Negative Binomial Regression\; Association Rules\; GRI Algo- | 1 预测 · 1.2 回归/相关预测;1 预测 · 1.5 零膨胀/受限计数预测;5 统计推断与因果 · 5.2 回归系数与效应量;7 分类与聚类 · 7.1 监督分类/识别
P2025-D-01 | 2025 | D | 26 | 16 | 3 | 32 | A* and GA;Monte Carlo;centrality;dynamic programming;nonlinear programming;queueing theory;sensitivity analysis;shortest path;A-star;BP neural network;genetic algorithm | Revitalizing Transport: A Safer, Smarter Future for;Baltimore's Network;Contents;1 Introduction............................................................................................ 3;2 Assumptions and Justifications.............................................................4;3 Notations..................................................................................................5;4 Data Processing.......................................................................................5;5 Bridge Collapse Impact Quantification Model...................................6;6 Transit Network Optimization Model................................................14;7 Community Road Availability Optimization Model........................ 19;8 Model Application for Security...........................................................22;9 Sensitivity Analysis...............................................................................23;10 Model Evaluation............................................................................... 24;References................................................................................................ 24;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Assumptions and Justifications;3 Notations;4 Data Processing;5 Bridge Collapse Impact Quantification Model;5.1 Network model building and visualization;5.2 Quantification of impact indicators;5.3 Accessibility definition and solution;5.4 Bridge collapse data processing;5.5 Solution;6 Transit Network Optimization Model;6.1 Urban Bus Network Visualization;6.2 Single-objective Optimization Model;6.3 Solution;7 Community Road Availability Optimization Model;7.1 Supplementary Datasets;7.2 Community transportation availability evaluation;7.3 Traffic Layout Optimization Model;7.4 Solution;8 Model Application for Security;9 Sensitivity Analysis;10 Model Evaluation;10.1 Strengths;10.2 Weaknesses;References | 1 | 1 | 1 | 1 | 0 | Stakeholder\; Queueing Theory\; Accessibility\; A* and GA\; Monte Carlo | 8 网络与图 · 8.2 流量分配/路由;2 评价与排序 · 2.3 排序规则/权重设计;9 决策与博弈 · 9.1 多准则决策;3 优化 · 3.5 调度与配置
P2025-D-02 | 2025 | D | 25 | 29 | 1 | 13 | cluster analysis;graph theory;sensitivity analysis;shortest path;entropy weight method;minimum spanning tree;correlation coefficient;factor analysis;network analysis;machine learning | Optimizing Baltimore Multi-Layer Traffic Network Model Based;on Graph Theory & Clustering Algorithm;Contents;Introduction;1.1;Problem Background;1.2;Problem Restatement;1.3;Our Work;Assumptions and Justifications;Notations;Model I: Adaptive Transportation Network Model Simulation;4.1;Introduction of the Network Model;4.2;Network Model Establishment Based on Graph Theory;4.3;Analysis Based on Entropy Weight Method;4.4;Mathematical Formulation of the Network Model;4.5;Impact of Bridge Collapse in Stakeholders;Model II: Upgraded Bus Network Model Based on Cluster Anal-;ysis;5.1;Introduction of Current Situation;5.2;Establishment of Upgraded Bus Model;5.3;Impact of New Project in Stakeholders;Model III: Integrated Multimodal Transport Model;6.1;Optimized Integration of Bus and Rail Networks;6.2;Influence of Project Based on Model;Insight of Safety Based on Transportation System;Sensitivity Analysis;Model Evaluation;9.1;Strength;9.2;Weakness;Conclusion;Memorandum;References | 1 | 1 | 1 | 1 | 0 | Graph Theory | 8 网络与图 · 8.2 流量分配/路由;2 评价与排序 · 2.3 排序规则/权重设计;9 决策与博弈 · 9.1 多准则决策;3 优化 · 3.5 调度与配置
P2025-D-03 | 2025 | D | 25 | 14 | 4 | 44 | Bayesian;Markov chain;Markov chain Monte Carlo;Monte Carlo;Wardrop;fuzzy comprehensive evaluation;network flow;sensitivity analysis;centrality;shortest path;Pareto;fuzzy logic | A Multi-Methodological Framework for Post-Disaster;Traffic Optimization and Sustainable Mobility Planning;in Baltimore;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Literature Review;1.4;Our Work;Assumptions and Explanations;Notations;Preparation before Solution;4.1;Data Collection;4.2;Data processing;Network-Theoretic Framework for Urban Traffic Flow;Analysis;5.1;Network Representation;5.2;Traffic Flow Modeling;5.3;Analytical Metrics and Data Integration;Quantitative Analysis of the Francis Scott Key Bridge;Accident Impact on Urban Traffic Network Flow;6.1;Impact of the Francis Scott Key Bridge accident on traffic flow;network;6.2;Francis Scott Key Bridge collapse and its impact on residents;6.3;Analysis of the impact of Francis Scott Key Bridge on stakehold-;ers;Multimodal Transportation Network Model for Bus-;Pedestrian System Analysis;7.1;Multimodal Network Representation;7.2;Multimodal Demand Allocation;7.3;Accessibility Impact Metric;7.4;Implementation Scenario: Bus Rapid Transit (BRT) Project;7.5;Stakeholder Impact Analysis;7.6;Sensitivity Analysis;Optimal Transportation Network Intervention Model;for Baltimore;8.1;Project Recommendation: Integrated Mobility Corridor (IMC);8.2;Benefit Quantification Model;8.3;System Disruption Analysis;8.4;Implementation Framework;8.5;Case Study: Baltimore Green Transit Corridor;Model Evaluation;9.1;Strengths;9.2;Weakness;Conlusion;References;STRENGTHEN THE MANAGEMENT OF;BALTIMORE TRANSPORTATION;MEMO;KEY MODEL FEATURES;WHY CHOOSE OUR MODEL?;Project 1： Impacting Bus/Pedestrian;Systems: Bus Rapid Transit (BRT);Project;Multimodal;Network;Model: Integrates;bus;routes,;pedestrian pathways, and transfer links;as a directed graph.;Nested;Logit;Demand;Allocation: Predicts mode shifts (bus;ridership increased by 44% post-BRT).;Gini coefficients to quantify spatial;justice;improvements;(accessibility;inequality reduced by 14.6%);Project 2: Integrated Mobility Corridor;(IMC) System;resident welfare (58% improvement in;quality of life), cost efficiency (phased;funding to minimize upfront burdens), and;environmental sustainability (28,000-ton;annual CO₂ reduction).;marginalized;communities;through;accessibility metrics (Gini coefficient;drops from 0.41 to 0.33) and pedestrian-;friendly zones to reduce spatial inequality.;Dynamic;Simulations:;Accounts;for;phased;disruptions,;stakeholder feedback, and climate risks.;Data-Driven Validation: Matches CMAP traffic counters (R² =;0.89) and Baltimore’s Green Corridor case study.;Equity-Centered Design: Uses accessibility potential metrics to;prioritize underserved communities.;OUR FLAWS;risking suboptimal policy recommendations.;TO THE MAYOR;OF BALTIMORE | 1 | 1 | 1 | 1 | 0 | Traffic Flow Optimization, Fuzzy Comprehensive Evaluation, Wardrop | 8 网络与图 · 8.2 流量分配/路由;2 评价与排序 · 2.3 排序规则/权重设计;9 决策与博弈 · 9.1 多准则决策;3 优化 · 3.5 调度与配置
P2025-D-04 | 2025 | D | 27 | 26 | 5 | 17 | Multi-layer network model;TOPSIS;centrality;sensitivity analysis;three-layer bus network model;shortest path;entropy weight method | Navigating Baltimore’s Growth: A Multi-Layer Network;Approach to Urban Transportation Optimization;Summary;Contents;Introduction;1.1;Background;1.2;Restatement of the Problem;1.3;Our Work;Model Assumptions and Notation;2.1;Assumptions;2.2;Notation;Data Preprocessing;3.1;Imputation of Missing Values;3.2;Outlier Removal;3.3;Handling Cluttered Road Information;3.4;Processing Abbreviation Information;Multi-layer Transportation Network Model;Task 1: Analysis of the Bridge Collapse’s Impact;5.1;Impact Assessment Model(IA);5.2;Model Solution and Results;Task 2: The impact of the project on the bus system;6.1;Three-layer Bus Network Model (TBN);6.2;Model Solution and Results;Task 3: The project best improves the lives of the residents;7.1;Improved Dijkstra Algorithm;7.2;Double Density Fitting Model (DDF);7.3;Model Solution and Results;Sensitivity Analysis;Model Evaluation and Further Discussion;9.1;Strengths;9.2;Weaknesses;9.3;Further Discussion;Memorandum;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Multi-layer network model, three-layer bus network model, Baltimore | 8 网络与图 · 8.2 流量分配/路由;2 评价与排序 · 2.3 排序规则/权重设计;9 决策与博弈 · 9.1 多准则决策;3 优化 · 3.5 调度与配置
P2025-E-01 | 2025 | E | 26 | 16 | 6 | 35 | AHP;Food web model;centrality;differential equation;entropy weight method;graph theory;sensitivity analysis;system dynamics;shortest path | Forests and Agriculture in Harmony: How to Maintain Ecosys-;tem Stability During the Transition to Organic Farming;Summary;Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 4;3 Notations and Data........................................................................................... 5;4 Problem 1: Agricultural Ecosystem Based on Differential Equation ......... 5;5 Problem 2: Ecosystem Assessment ............................................................... 15;6 Problem 3: Towards Green Agriculture ....................................................... 20;7 Sensitivity Analysis ......................................................................................... 24;8 Model Evaluation and Further Discussion .................................................. 25;9 References ....................................................................................................... 25;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Assumptions and Justifications;3 Notations and Data;4 Problem 1: Agricultural Ecosystem Based on Differential Equa-;tion;4.1 Problem analysis;4.2 Model preparation;4.3 Model 1：Dynamic Model of Tri-trophic Food Chain;4.4 Model 2：Dynamic Model of Food Web;4.5 Model 3：Food Web Model Considering Agricultural Cycles;5 Problem 2: Ecosystem Assessment;5.1 Problem analysis;5.2 Model preparation;5.3 Assessment of Food Chain and Food Web;5.4 Assessment of the Food Web After Introducing New Species;5.5 Assessment of the Food Web After Removing Chemicals (Herbicides +;Pesticides);5.6 Assessment of the Food Web After Introducing Bats (or Bees);6 Problem 3: Towards Green Agriculture;6.1 Problem background;6.2 Model preparation;X (C1);g cm;g cm;g cm;g cm;g cm;6.3 EWM-AHP;6.4 Analysis of results;7 Sensitivity Analysis;8 Model Evaluation and Further Discussion;8.1 Advantages;8.2 Limitations and Extension of the model;9 References | 1 | 1 | 1 | 1 | 1 | Differential equation, Food web model, network, EWM-AHP | 4 机理建模与仿真 · 4.2 生态/生物动力学;1 预测 · 1.3 情景与概率预测;3 优化 · 3.3 多目标/权衡;9 决策与博弈 · 9.1 多准则决策
P2025-E-02 | 2025 | E | 27 | 19 | 3 | 29 | COMAP Model;Convex Reformulation;FATE Model;Lotka-Volterra;logistic regression;multi-objective optimization;sensitivity analysis;Food web model;differential equation;partial differential equation;nonlinear programming;system dynamics | Symphony of Eco-Agriculture:;A New Music of Harmonious Coexistence;Summary;Contents;1 Introduction ...................................................................................................... 3;2 Assumptions and Justifications ....................................................................... 4;3 Notations and Data Sources ............................................................................ 5;4 Model Ⅰ: Forest- to-Agriculture Transition Ecosystem ................................ 6;5 Analysis of Species Return Under Multi-Scenario Simulation .................. 13;6 Analysis of Chemical Dependency and Biodiversity Synergy ................... 16;7 Model II: Comprehensive Organic Management and Planning ............... 19;8 Sensitivity Analysis ......................................................................................... 21;9 Strengths and Weaknesses ............................................................................. 22;10 Conclusion ..................................................................................................... 23;References .......................................................................................................... 23;Appendices ......................................................................................................... 24;1 Introduction;1.1 Background;1.2 Restatement of the Problem;1.3 Literature Review;1.4 Our Work;2 Assumptions and Justifications;3 Notations and Data Sources;3.1 Notations;3.2 Data Sources;4 Model Ⅰ: Forest- to-Agriculture Transition Ecosystem;4.1 Model Overview;4.2 Multi-Trophic Food Web;4.3 Results of Model I;5 Analysis of Species Return Under Multi-Scenario Simulation;5.1 Species Distribution Model;5.2 Multi-Scenario Simulations;5.3 Scenario Simulation Results;6 Analysis of Chemical Dependency and Biodiversity Synergy;6.1 Herbicide Dependency Reduction;6.2 Biodiversity Synergy;6.3 Calculated Results;7 Model II: Comprehensive Organic Management and Planning;7.1 Model Preparation;7.2 Model Construction;7.3 Calculated results;8 Sensitivity Analysis;9 Strengths and Weaknesses;9.1 Strengths;9.2 Weaknesses;10 Conclusion;References;Appendices;Proof 1: Mathematical Expression of Spatial Dimensions;Proof 2: Concavity of the COMAP Model;Report on Use of AI;GPT-4o | 1 | 1 | 1 | 1 | 0 | FATE Model\; COMAP Model\; Lotka-Volterra Equation\; Eco-Agriculture； | 4 机理建模与仿真 · 4.2 生态/生物动力学;1 预测 · 1.3 情景与概率预测;3 优化 · 3.3 多目标/权衡;9 决策与博弈 · 9.1 多准则决策
P2025-E-03 | 2025 | E | 25 | 16 | 4 | 26 | Food web model;Lotka-Volterra;Petri net;Petri-Food Web model;entropy weight method;fuzzy comprehensive evaluation;sensitivity analysis;system dynamics;differential equation;Shannon entropy | From Forest to Farm, an Ecosystem’s Charm;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Overview of Our Work;Assumptions and Justifications;Notations;Model Preparation;Petri-Food Web (PFW) Model;5.1;Model Building and Design;5.2;Maturity Assessment of Ecosystems;5.3;Extension of the Model: Species Regression;Herbicide-Removal Prediction (HRP) Model;6.1;Impact Prediction Model Based on Wheat-Weed Competition;6.2;Restoration of Ecological Balance After the Introduction of Bats;6.3;Introduction of Typical Species: Woodpeckers vs. Bats;Organic Agriculture Impacts Evaluation (OAIE) Model;7.1;Indicator Identification and Data Collection;7.2;Multi-level Fuzzy Evaluation Modeling;7.3;The Entropy Weight Method (EWM);7.4;Presentation of Results and Discussion;Sensitivity Analysis;Model Evaluation;9.1;Strengths;9.2;Weaknesses;References | 1 | 1 | 1 | 1 | 1 | Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger- | 4 机理建模与仿真 · 4.2 生态/生物动力学;1 预测 · 1.3 情景与概率预测;3 优化 · 3.3 多目标/权衡;9 决策与博弈 · 9.1 多准则决策
P2025-E-04 | 2025 | E | 26 | 15 | 0 | 43 | Lotka-Volterra;differential evolution;multi-type Holling responses;sensitivity analysis;Food web model;time series analysis;logistic regression | Regenerative, Organic, or Conventional:;A Mathematical Modeling Comparison;Contents;1 Introduction;1.1 Research Background;1.2 Restatement of the Problem;1.3 Literature Review;1.4 Our Work;2 Model Preparation;2.1 Assumption;2.2 Notations;3 Establishment of Models;3.1 Core Model;3.2 BEME Models;3.2.1 Soil Phosphorus dynamics ( P );3.2.2 Ryegrass dynamics ( R );3.2.3 Aphid dynamics ( A );3.2.4 Ladybug dynamics ( L );3.2.5 Exogenous control;3.3 SEAM Models;3.3.1 State Equation;3.3.1.1 Crop biomass dynamics;3.3.1.2 Pest population dynamics;3.3.1.3 Beneficial insect population dynamics;3.3.1.4 Dynamics of soil organic matter;3.3.1.5 Soil microbial activity;3.3.1.6 Natural enemy diversity;3.3.1.7 Farmland ecosystem functions;3.3.2 Control variable;3.3.2.1 Chemical pesticide use;3.3.2.2 Organic input;3.3.3 Economic benefit function;3.3.3.1 Short-term yield;3.3.3.2 Long-term net present value;3.4 System optimization;4 Interpretation of Result;4.1 Establishment of Ecosystem Model;4.2 The Impact of Human Practices on Ecosystems;4.3 Effects of Anthropogenic Introduction of Bats and Sparrows on;Ecosystems;4.4 SEAM Results;4.4.1 Economic Performance Trajectory Analysis;4.4.2 Ecosystem Services Value Assessment;4.4.3 Multi-dimensional Sustainability Performance Analysis;4.4.4 Cost-Benefit Distribution Analysis;4.4.5 Temporal Analysis of Regenerative Agriculture Transition;4.4.6 Risk-Return Distribution Assessment;4.4.7 Economic Efficiency Analysis;4.4.8 Socioeconomic Impact Assessment;5 Sensitivity Analysis;6 A Letter to a Farmer;References;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | differential evolution optimization, ecosystem modeling, multi-type Holling responses, | 4 机理建模与仿真 · 4.2 生态/生物动力学;1 预测 · 1.3 情景与概率预测;3 优化 · 3.3 多目标/权衡;9 决策与博弈 · 9.1 多准则决策
P2025-F-01 | 2025 | F | 25 | 13 | 4 | 25 | Cox proportional hazards;VBGMM;difference-in-differences;sensitivity analysis;structural equation modeling;survival analysis;Bayesian;cluster analysis;hypothesis test;principal component analysis;logistic regression;machine learning;time series analysis;Regression Analysis | Changing rules on the virtual battleﬁeld;Contents;Introduction;1.1;Problem Background;1.2;Restatement of the Problem;1.3;Our Work;Assumptions and Justiﬁcations;Notations;Data Pre-processing;4.1;Data Collection;4.2;Data Cleaning;Task1: Multi-level cybercrime risk assessment and re-;sponse model;5.1;Data Visualization;5.2;Variational Bayesian Gaussian Mixture Clustering;5.3;Multi-level analysis model based on unordered multi-classiﬁcation;logistics regression;Task2:Cybersecurity policy effectiveness evaluation mod-;el;6.1;Multi-period double difference model;6.2;Cox’s time varying proportional hazard model;6.3;principle;6.4;Hypothesis Testing;6.5;Model Building;6.6;Model Analysis;Task3:CyberDemographic Resilience Model;7.1;Principle;7.2;Model establishment;7.3;Fitness test;7.4;Model analysis;Analysis on Model’s Sensitivity;Strengths and Weaknesses;9.1;Strengths;9.2;Weaknessess;References;MEMO | 1 | 1 | 1 | 1 | 0 | VBGMM\; DID Model\; Cox TVPH\; SEM | 5 统计推断与因果 · 5.3 因果/政策评估;2 评价与排序 · 2.1 指标体系构建;7 分类与聚类 · 7.2 无监督聚类/分段
P2025-F-02 | 2025 | F | 25 | 1 | 0 | 0 | Causal Inference;K-means;cluster analysis;difference-in-differences;network analysis;sensitivity analysis;principal component analysis;integer programming;machine learning;Regression Analysis;factor analysis;structural equation modeling | Five Elements Illuminate, Cybersecurity Innovates;Summary;Contents;1 Introduction;1.1 Problem Background;1.2 Problem Restatement and Analysis;2 Assumptions and Justifications;3 Notations;4 Selecting Critical Factors of Cybercrime;4.1 Data Preprocessing;4.2 Cluster Analysis;4.2.1 K-means Clustering;4.2.2 Selection of the Optimal Number of Clusters;4.2.3 Clustering Results Analysis and Visualization;Z=X⋅W;5 The Five Elements Model;5.1 Introduction of Five Elements Theory;5.2 Significance of Five Elements in Cybersecurity;5.3 The Five Elements Model;5.3.1 Data Analysis: Cybercrime Distribution;5.3.2 Combination of Data Analysis and Five Elements Theory;5.3.3 Conclusion and Discussion;6 Model II: Effectiveness Analysis of Cybersecurity;Policies;6.1 Data Acquisition and Cleaning;6.2 Five Elements Classification of Policies;6.3 Impact of Policies vs. Cybercrime;6.3.1 Panel Regression Analysis;6.3.2 Interaction Effect Analysis;6.4 Results Visualization;7 Model III: Impact of National Characteristics on;Cybercrime;7.1 Research Design and Data;7.2 Measurement Model;7.3 Structural Model;7.4 Conclusion;8 Sensitivity Analysis;attention.;9 Model Evaluation;10 Reference;Memo;effectively and close jurisdictional loopholes. | 1 | 1 | 1 | 1 | 0 | Cybersecurity Policy\; Cybercrime\; Five Elements Theory\; Clustering Analysis\; | 5 统计推断与因果 · 5.3 因果/政策评估;2 评价与排序 · 2.1 指标体系构建;7 分类与聚类 · 7.2 无监督聚类/分段
P2025-F-03 | 2025 | F | 33 | 11 | 7 | 0 | K-means;KDMF;MIC;cluster analysis;difference-in-differences;factor analysis;sensitivity analysis;principal component analysis;Regression Analysis;linear regression | Cracking the Cyber - Puzzle: KDMF in Action;Contents;1 Introduction ........................................................................................................... 3;2 Assumptions and Justifications ........................................................................... 5;3 Notations ................................................................................................................ 5;4 K-Means approach: Unveiling the Tapestry of Cybercrime ............................ 6;5 DID Analysis: Assessing Cyber - security Policies ...........................................12;6 MIC & Factor Strategy: Demographics - Cybercrime Correlations.............17;7 Sensitivity Analysis .............................................................................................20;9 Model Evaluation and Further Discussion .......................................................22;10 References ..........................................................................................................24;Memorandum .........................................................................................................25;Report on Use of AI ...............................................................................................26;1 Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Our Work;2 Assumptions and Justifications;3 Notations;4 K-Means approach: Unveiling the Tapestry of Cybercrime;4.1 Introduction;4.2 Indicators Selection;4.3 Data Analysis;4.3.1 Descriptive Analysis of Individual Indicators;4.3.2 Clustering Analysis of Cybercrime Distribution Patterns;4.4 Discussion;4.4.1 Synthesis of Findings;4.4.2 Emergent Patterns and Implications;5 DID Analysis: Assessing Cyber - security Policies;5.1 Cracking the Policy Code: LDA and DID in Action;5.1.1 LDA - based Thematic Analysis;5.1.2 Efficiency Analysis by DID;5.2 Decoding the Policy Efficacy: LDA - DID Results Uncovered;6 MIC & Factor Strategy: Demographics - Cybercrime Cor-;relations;6.1 Analytical Framework: MIC Approach;6.1.1 Data Preparation;6.1.2 MIC Computation;6.2 Factor Analysis for Deeper Understanding;6.3 Results Unveiled: Variable Impact Profiles;6.3.1 Intra - variable Variations across Countries;6.3.2 Inter - variable Comparative Analysis;7 Sensitivity Analysis;9 Model Evaluation and Further Discussion;9.1 Strengths;9.2 Weaknesses;9.3 Further Discussion;10 References;Memorandum;Report on Use of AI | 1 | 1 | 1 | 1 | 0 | Cybercrime, KDMF, K-means, DID, MIC, Policy | 5 统计推断与因果 · 5.3 因果/政策评估;2 评价与排序 · 2.1 指标体系构建;7 分类与聚类 · 7.2 无监督聚类/分段
P2025-F-04 | 2025 | F | 25 | 15 | 0 | 8 | correlation coefficient;time series analysis;machine learning | Data-Driven Policy Effectiveness Evaluation and Country-;Specific Characteristic Based Cybercrime Prediction;Summary;Content;1. Introduction;1.1 Problem Background;1.2 Restatement of the Problem;1.3 Global Cybersecurity Index;1.4 Our Work;Stage I Data Preparation;Stage II High Risk Region Location;Stage III Policy Evaluation;Stage IV Demographic Evaluation;2. Model Preparation;2.1 Assumptions;Assumption 1: When predicting the number of crime occurrences, statistics are;Assumption 2: Data with largely similar content but differing in a small amount;Assumption 3: When conducting demographic properties with monthly precision,;2.2 Notations;2.3 Data Collection and Visualization;3. Model Establishment;3.1 Model I: Define High Targets;3.2 Model II: Define Effective Policies;3.3 Model III: Define Correlative Demographic Parameters;and Make Prediction Accordingly;4. Results and Discussion;4.1 Problem 1;4.2 Problem 2;4.3  Problem 3;5. Model Evaluation;6. Conclusion;7. Reference;8. Memo;Empirical Insights on Cybersecurity: Policy;Effectiveness and Predictive Models for Global;Cybercrime Trends | 0 | 1 | 1 | 0 | 0 | Cybercrime, Policy effectiveness, Correlation coefficient, Cybercrime | 5 统计推断与因果 · 5.3 因果/政策评估;2 评价与排序 · 2.1 指标体系构建;7 分类与聚类 · 7.2 无监督聚类/分段
P2025-F-05 | 2025 | F | 27 | 17 | 5 | 0 | difference-in-differences;linear regression;Regression Analysis;correlation coefficient;cross-validation | The Global Cybersecurity Chessboard: Decoding Crime;Distribution and Policy Effectiveness;Contents;Introduction;1.1;Background of the Issue;1.2;Restatement of the Problem;1.3;Our Work;Assumptions and Justiﬁcations;Interpretation of Symbols;Global Cybercrime Data Analysis;4.1;Data Collection;4.2;Data Processing;4.3;Data Analysis and Visualization;National Security Policies and Global Cybercrime Dis-;tribution;5.1;Preliminary Analysis;5.2;Model1: Hierarchical Interaction Scoring Regression Model(HISR);5.3;Pattern Analysis;5.4;Theoretical Summary;National Demographics and Cybercrime Distribution;6.1;Correlation Analysis;6.2;Model2: Log-Enhanced Quadratic Regression Model(LEQR);6.3;Results Interpretation;Model Evaluation;7.1;Merits;7.2;Limitations;Conclusions;Memorandum;References;Report on Use of AI | 1 | 1 | 0 | 0 | 0 | Cybersecurity\; Hierarchical Interaction Scoring Regression Model\; Log- | 5 统计推断与因果 · 5.3 因果/政策评估;2 评价与排序 · 2.1 指标体系构建;7 分类与聚类 · 7.2 无监督聚类/分段
```

## 第二层 · 受控词表命中（**指针：词 + md 文件 + 页码 + 片段**）

本层收**有命中**的 **43** 篇；第三层收零命中的 **0** 篇；两层之和 = **43** = 篇数（**每篇恰好进一层**）。

指针格式（每行一条，**刻意不用反引号包裹**——md 整行里可能有反引号）：

```
- <规范词>;p<页码>;x<出现次数>;<md 整行逐字>
```

解析式：`^- (.*); p(\d+); x(\d+); (.*)$`（`;` 是转义过的分隔符，片段按 `_esc` 的规则转义）。页码由该行之前最近的 `<!-- page N -->` 锚数出；**片段是 md 的整行逐字**（可用 `grep -F` 直接在该 md 里定位）；`x<N>` 是**全篇**出现次数，**不是**这一行的。**md 文件**列在每篇小标题下的 `md: ` 一行。

### P2025-A-01 · 题 A · 2025美赛O奖论文/A/2500836.pdf
md: corpus/papers/md/2025美赛O奖论文/A/2500836.md
- Archard Law; p1; x9; stair usage frequency. Given the known distribution of wear depth, and based on Archard's Law, we
- Monte Carlo; p1; x5; the Monte Carlo method to estimate the stair age, yielding a range of approximately (282.1984,
- Navier-Stokes; p1; x8; continuity equation for simulating pedestrian flow was established based on Navier-Stokes Equations.
- correlation coefficient; p1; x10; then used the Person correlation coefficient to analyze their relationship. Finally, to analyze the
- differential equation; p1; x2; number of stair users on a specific day, we established a partial differential equation to
- finite difference; p1; x2; Then we used the finite difference method to calculate the pedestrian density during stair usage and
- partial differential equation; p1; x2; number of stair users on a specific day, we established a partial differential equation to
- particle swarm optimization; p1; x9; Swarm Optimization algorithm(PSO).
- sensitivity analysis; p1; x11; Furthermore, we conduct a sensitivity analysis on the two-dimensional normal distribution
- feature selection; p7; x1; **Step 2: Feature extraction**
- hypothesis test; p16; x2; Finally, a Monte Carlo simulation was used for reliability assessment, with hypothesis testing:
- machine learning; p22; x1; the advanced machine learning algorithm, particle swarm optimization algorithm (PSO), which

### P2025-A-02 · 题 A · 2025美赛O奖论文/A/2501567.pdf
md: corpus/papers/md/2025美赛O奖论文/A/2501567.md
- Archard Law; p1; x9; **In Task 1, we establish a model based on Archard’s Wear Law and Human Behavior**
- Bayesian; p1; x4; and Bayesian Information Criterion to analyze the direction and usage pattern of stair-
- Gaussian Distribution; p1; x5; number of mixture Gaussian distribution, can be accessed by minimizing Bayesian Infor-
- Monte Carlo; p1; x11; **In Task 3, we develop a model combining Monte Carlo simulations and Smooth-**
- linear regression; p4; x1; Linear Regression

### P2025-A-03 · 题 A · 2025美赛O奖论文/A/2501909.pdf
md: corpus/papers/md/2025美赛O奖论文/A/2501909.md
- Archard Law; p1; x6; matrix. Based on this matrix and Archard Wear Law, we develop the WVM. We introducing
- Central Limit Theorem; p1; x3; WDM based on the Central Limit Theorem. It calculate the marginal distribution of the wear
- Gaussian Mixture Algorithm; p1; x1; Keywords: Stair Wear, Archard Law, Central Limit Theorem, Gaussian Mixture Algorithm
- sensitivity analysis; p1; x7; Material hardness demonstrates a high sensitivity in our model. The model shows low

### P2025-A-04 · 题 A · 2025美赛O奖论文/A/2504218.pdf
md: corpus/papers/md/2025美赛O奖论文/A/2504218.md
- Archard Law; p1; x6; ## Sub-model i, grounded in Archard’s theory and PDEs, provides a probabilistic equa-
- Bayesian; p1; x21; ## cal insights in a Bayesian framework by assigning prior distributions to multiple pa-
- Markov chain; p1; x2; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,
- Markov chain Monte Carlo; p1; x19; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,
- Monte Carlo; p1; x2; ## Markov Chain Monte Carlo (MCMC) refines the posterior distribution in its vicinity,
- partial differential equation; p1; x19; ## For the advanced tasks 3 & 5, we developed a multi-layer PDE model as well as a
- particle swarm optimization; p1; x15; ## and simulation. After Particle Swarm Optimization (PSO) locates the global optimum,
- sensitivity analysis; p1; x6; ## wear. Finally, we performed a sensitivity analysis. The results show that our model
- correlation coefficient; p3; x1; materials after a certain amount of wear by changing the correlation coefficient, and obtain the
- Gaussian Distribution; p13; x1; Here, (δx, δy) can be drawn from a Gaussian distribution N((x0, y0), Σ) to reflect that each footstep
- differential equation; p14; x1; flow rates of people going upstairs and downstairs, we can formulate a partial differential equation that
- Credible Intervals; p17; x4; Finally, we use a Quantile-based Method to construct credible intervals. Specifically, we sort the
- Uncertainty Quantification; p19; x1; posterior uncertainty quantification” under limited computational overhead. It aligns the simulated
- system dynamics; p26; x1; tion: a literature review. Vehicle System Dynamics, 47(6): 661–700, 2007.

### P2025-A-05 · 题 A · 2025美赛O奖论文/A/2511565.pdf
md: corpus/papers/md/2025美赛O奖论文/A/2511565.md
- Archard Law; p1; x15; Second, we build a Daily Foot Traffic Model based on the Archard equation. We take Ar-
- Bayesian; p1; x10; use Bayesian Inversion Framework to calculate the construction time to provide essential param-
- Weathering Degree Model; p1; x3; Key Words: Stair Wear, Archard Equation, Depth Estimation, Weathering Degree Model,
- sensitivity analysis; p1; x15; Finally, we perform a sensitivity analysis on the key parameters of our model to evaluate its
- CNN; p3; x1; machine learning, specifically CNN models [5], to train data and obtain rail wear amounts have
- machine learning; p3; x2; machine learning, specifically CNN models [5], to train data and obtain rail wear amounts have
- Monte Carlo; p14; x1; After considering all the above factors, we wrote a Python program using the Monte Carlo
- hypothesis test; p14; x5; 3.4 Hypothesis Testing
- cross-validation; p24; x1; the staircase, employing cross-validation with multiple data sources to boost reliability.

### P2025-B-01 · 题 B · 2025美赛O奖论文/B/2501687.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2501687.md
- CVM; p1; x17; **gramming Model based on Contingent Valuation Method(CVM) and Particle Swarm**
- nonlinear programming; p1; x4; **Keywords: Sustainable tourism\; CVM\; Multi-objective nonlinear programming**
- particle swarm optimization; p1; x7; **gramming Model based on Contingent Valuation Method(CVM) and Particle Swarm**
- sensitivity analysis; p1; x9; Sensitivity analysis confirmed model stability, highlighting peak-season tourist limits as
- logistic regression; p11; x2; **can employ the Logistic Model:**
- ARIMA; p12; x3; The estimation of the unemployment rate growth utilized the ARIMA (p, d, q) model.
- Regression Analysis; p12; x1; *Figure 6: Linear regression analysis of the population and median income in Juneau*
- linear regression; p12; x2; Juneau[8][9][10], and perform a linear regression fit to obtain the following results:
- Monte Carlo; p17; x1; we use the Monte Carlo Method to select 101 values at equal intervals with a step size of

### P2025-B-02 · 题 B · 2025美赛O奖论文/B/2502617.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2502617.md
- Pareto; p1; x26; ## Overload Alarm: Pareto Optimization of the
- SLSQP; p1; x3; among them. Using the SLSQP method, we determine the global Pareto-optimal solution for
- multi-objective optimization; p1; x9; develops a multi-objective planning model that integrates economic, social, and environmental
- sensitivity analysis; p1; x11; Finally, we analyze the sensitivity of key model parameters, as well as the sources of additional
- reinforcement learning; p23; x1; Safe Urban Bus Routes for Tourism Promotion Using a Hybrid Reinforcement Learning

### P2025-B-03 · 题 B · 2025美赛O奖论文/B/2503268.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2503268.md
- AHP; p1; x9; for each main factor combined with Analytic Hierarchy Process (AHP) to attain the comprehen-
- Lotka-Volterra; p1; x2; and economy, respectively. Inspired by the Lotka-Volterra model, logistic population model, and
- SIS model; p1; x2; SIS model, we developed the Sustainable Tourism Dynamics Model (STDM). This system uses
- sensitivity analysis; p1; x20; We assessed our model’s sensitivity using two methods. The Morris method identiﬁed key factors
- ordinary differential equation; p4; x5; gies. The SDTM, formulated with ordinary diﬀerential equations (ODE), establishes the relationships
- system dynamics; p5; x2; essential system dynamics.
- logistic regression; p9; x1; teraction with the glacier environment. According to Verhulst’s logistic model [3], population growth
- nonlinear regression; p9; x2; the parameters ki and ri through nonlinear regression. Due to the complexity of real-world systems,
- cluster analysis; p11; x1; cated by the tight clustering of observed data along the model trajectories in the (NJuneau, TJuneau)

### P2025-B-04 · 题 B · 2025美赛O奖论文/B/2504448.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2504448.md
- dynamic programming; p1; x11; frastructure. To address this issue, we develop a multi-objective dynamic programming
- entropy weight method; p1; x2; ature, snowfall, and ocean pH using entropy weight method. This environment model
- multi-objective optimization; p1; x1; **Keywords: Multi-Objective Model, Dynamic Programming, Sustainable Tourism**
- sensitivity analysis; p1; x10; ommended policies. Additionally, we perform a sensitivity analysis to identify the most

### P2025-B-05 · 题 B · 2025美赛O奖论文/B/2505199.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2505199.md
- NSGA-II; p1; x11; the Non - dominated Sorting Genetic Algorithm II (NSGA - II) is employed to solve the
- genetic algorithm; p1; x3; the Non - dominated Sorting Genetic Algorithm II (NSGA - II) is employed to solve the
- multi-objective optimization; p1; x10; Keywords: Sustainable tourism\; Juneau\; Multi - objective optimization\; NSGA - II
- sensitivity analysis; p1; x13; opment of the tourism industry. Sensitivity analysis indicates that the number of tourists, alco-
- Pareto; p4; x7; for hierarchical search, gets Pareto optimal solutions, maintains population diversity with
- deep learning; p21; x1; ·Adopt advanced algorithms like deep learning to boost efficiency and accuracy for de-
- factor analysis; p26; x1; techniques, like time - series analysis for predicting tourist flow trends and factor analysis for
- hypothesis test; p27; x2; Hypothesis Testing: We used Kimi to assist in hypothesis testing during the model -

### P2025-B-06 · 题 B · 2025美赛O奖论文/B/2509557.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2509557.md
- L-BFGS-B algorithm; p1; x2; on tourism sustainability and identify optimal strategies. Using the L-BFGS-B algorithm, we de-
- differential equation; p1; x2; System Dynamics\; differential equations\; logistics growth model\; dynamic feedback loops\;
- sensitivity analysis; p1; x11; plicability. Through sensitivity analysis and scenario simulations, we reveal the critical importance
- system dynamics; p1; x10; ## Society: A System Dynamics-Based Model for

### P2025-B-07 · 题 B · 2025美赛O奖论文/B/2517929.pdf
md: corpus/papers/md/2025美赛O奖论文/B/2517929.md
- AHP; p1; x6; analysis, the analytic hierarchy process (AHP) were used to construct the objective functions.
- NSGA-II; p1; x9; The NSGA-II Algorithm was applied to search for the Pareto-optimal solution set. Taking the
- Pareto; p1; x6; The NSGA-II Algorithm was applied to search for the Pareto-optimal solution set. Taking the
- multi-objective optimization; p1; x14; Several models are established: Model I: Multi-Objective Optimization Model for Sustain-
- sensitivity analysis; p1; x12; Before promoting the model, we conducted a sensitivity analysis using the local pertur-
- genetic algorithm; p4; x3; and multi-objective genetic algorithms. Based on this, we finally choose the NSGA-II al-
- system dynamics; p4; x1; ➢ Regarding the modeling methods, system dynamics[4], and multi-objective optimization
- Regression Analysis; p6; x4; at the same time, a stable tourist count provides reliable inputs to the regression analysis
- nonlinear regression; p10; x1; **2) Nonlinear regression analysis of average temperature and carbon footprint**
- structural equation modeling; p12; x2; When developing a structural equation model of residents' attitudes towards tourism de-
- correlation coefficient; p18; x1; tion indicates the magnitude of the correlation coefficient. The closer the absolute value is to

### P2025-C-01 · 题 C · 2025美赛O奖论文/C/2500759.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2500759.md
- LSTM; p1; x20; ory (LSTM) networks to mine temporal features and integrate home advantage effects.
- SHAP; p1; x33; athletics, and medal counts, while SHapley Additive exPlanations (SHAP) quantifies
- XGBoost; p1; x24; A dual-channel XGBoost-Bootstrap model is established to generate predictions with
- bootstrap; p1; x16; A dual-channel XGBoost-Bootstrap model is established to generate predictions with
- difference-in-differences; p1; x15; Subsequently, we develop a Difference-in-Differences (DID) model to quantify the
- machine learning; p1; x2; machine learning integration methods, we achieve an in-depth analysis and reliable pre-
- principal component analysis; p1; x28; patterns. Utilizing Principal Component Analysis (PCA) for dimensionality reduction
- hypothesis test; p2; x7; Hypothesis Testing and Contribution Coefficient Analysis · · · · · · · · · · ·
- sensitivity analysis; p2; x2; ## Sensitivity Analysis ·········································· 21
- correlation coefficient; p3; x14; responding probabilities. Furthermore, Spearman correlation coefficients and SHAP are
- Markov chain; p5; x1; memoryless characteristic of Olympic medal trends akin to Markov chains, we employ an
- time series analysis; p6; x4; Predicting the Olympic medal tally can be framed as a time series forecasting prob-
- cross-validation; p9; x4; through 10-fold cross-validation grid parameter tuning, along with the estimation of con-
- stacking; p9; x2; XGBoost is an ensemble learning algorithm based on gradient-boosted trees, which
- logistic regression; p11; x1; or defining a binary variable for "having won a gold medal" to apply logistic regression
- deep learning; p23; x1; pact analysis with deep learning techniques to refine medal predictions. By incorporating
- reinforcement learning; p23; x1; robust real-time data update mechanism. The use of reinforcement learning will further
- Bayesian; p25; x2; [8] Tui H Nolan, Jeff Goldsmith, and David Ruppert. Bayesian functional principal
- cluster analysis; p25; x1; autoencoder-based arithmetic optimization clustering algorithm to enhance principal
- gradient boosting; p25; x1; region, northwest china: Research using the extreme gradient boosting (xgboost)
- random forest; p26; x2; random forest model and then use SHAP to interpret its predictions. The steps might

### P2025-C-02 · 题 C · 2025美赛O奖论文/C/2501869.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2501869.md
- Bayesian; p1; x17; In Question 2, the Bayesian Change-point Detection method is used to identify significant
- Tobit; p1; x50; ## Medal Prediction Based on Tobit and Hurdle Models
- XGBoost; p1; x13; were significantly better than the machine learning methods (random forest and XGboost) in
- change-point detection; p1; x13; In Question 2, the Bayesian Change-point Detection method is used to identify significant
- hurdle model; p1; x58; ## Medal Prediction Based on Tobit and Hurdle Models
- machine learning; p1; x5; were significantly better than the machine learning methods (random forest and XGboost) in
- random forest; p1; x14; were significantly better than the machine learning methods (random forest and XGboost) in
- two-stage least squares; p1; x11; stage least squares (2SLS) method is used to construct a causal regression model to quantify
- Causal Inference; p2; x1; **Change-Point Detection and Causal Inference Models**
- sensitivity analysis; p2; x3; **Sensitivity Analysis**
- decision tree; p3; x3; ensemble learning methods based on decision trees, excel at handling non-linear relationships
- stacking; p3; x1; ensemble learning methods based on decision trees, excel at handling non-linear relationships
- zero-inflated; p3; x4; and feature interactions, but they lack the ability to explicitly model truncation and zero-inflated
- principal component analysis; p5; x10; Medal_PCA
- logistic regression; p9; x3; We use the Logit model to calculate the probability that the i country will get at least one
- correlation coefficient; p14; x4; Subsequently, the Pearson correlation coefficients of these countries regarding the two covari-
- difference-in-differences; p20; x1; methods (such as OLS, DID, and IV) and develop a parameter estimation method that eliminates
- neural network; p24; x1; the summer Olympics using neural networks. Computers & Operations Research, 26(13),

### P2025-C-03 · 题 C · 2025美赛O奖论文/C/2503389.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2503389.md
- Monte Carlo; p1; x4; validated by Monte Carlo simulations, with a 95% confidence interval of 1.00–8.00.
- bootstrap; p1; x5; Network Bootstrap Ensemble Interval Model incorporating features such as the host boost,
- linear regression; p1; x7; **Medal Forecasting: We developed a Multiple Linear Regression–Feedforward Neural**
- logistic regression; p1; x10; First-Time Medalists: We developed a hybrid Logistic Regression–Random Forest model
- machine learning; p1; x1; ## Regression and Machine Learning
- principal component analysis; p1; x3; via Principal Component Analysis. Results identified swimming (USA, IS = 39.8) and diving
- random forest; p1; x11; First-Time Medalists: We developed a hybrid Logistic Regression–Random Forest model
- neural network; p2; x8; **Multiple Linear Regression-Feedforward Neural Network Bootstrap Ensemble**
- sensitivity analysis; p2; x6; **11 Sensitivity Analysis**
- regression discontinuity; p4; x3; • The disturbance terms in both the multiple regression and regression discontinuity
- feature selection; p6; x2; **Feature Selection**
- Regression Analysis; p11; x1; *Table 5: Key Metrics and Results of Regression Analysis*
- decision tree; p13; x1; The Random Forest model aggregates the predictions of multiple decision trees. The final pre-
- cross-validation; p14; x2; estimated using their respective cross-validation accuracies. The table below summarizes the

### P2025-C-04 · 题 C · 2025美赛O奖论文/C/2505964.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2505964.md
- Monte Carlo; p1; x15; athlete data and various models, including random forest, Monte Carlo simulation,
- linear regression; p1; x4; Poisson regression, and linear regression.
- random forest; p1; x19; athlete data and various models, including random forest, Monte Carlo simulation,
- Uncertainty Quantification; p2; x3; Monte Carlo Simulation and Uncertainty Quantification
- sensitivity analysis; p2; x21; Sensitivity Analysis
- machine learning; p7; x1; 3 One-hot encoding utilized to facilitate processing by machine learning models, for NOC and
- Regression Analysis; p16; x3; Using regression analysis on data from 1896 to 2024, the study addresses two key questions: 1.
- zero-inflated; p19; x3; Model Specification Sensitivity: Negative Binomial and Zero-Inflated Poisson
- feature selection; p22; x1; gesting potential issues in feature selection or
- ARIMA; p28; x1; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal
- exponential smoothing; p28; x1; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal
- time series analysis; p28; x1; velop a time series forecasting model (e.g., ARIMA, exponential smoothing) to project medal

### P2025-C-05 · 题 C · 2025美赛O奖论文/C/2507817.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2507817.md
- GSRF; p1; x21; For Task 1, we developed a Grid-Search Random Forest (GSRF) prediction model
- cross-validation; p1; x6; using preprocessed data. Through Cross-Validation, we obtained correlation coefficients for
- lasso; p1; x12; building the model by using the Lasso Regression, we selected three countries and identify
- logistic regression; p1; x11; For Task 2, we established a Logistic Regression Model to classify countries that have
- random forest; p1; x9; For Task 1, we developed a Grid-Search Random Forest (GSRF) prediction model
- sensitivity analysis; p1; x13; talented athletes. Additionally, we performed a sensitivity analysis that demonstrated the
- ARIMA; p6; x12; 5.1.1 ARIMA Model Initial Prediction
- moving average; p6; x1; predictions.The ARIMA model integrates autoregressive (AR) and moving average (MA)
- time series analysis; p6; x2; The ARIMA model is widely used in time series analysis for its flexibility and powerful
- decision tree; p8; x1; Random forests are machine learning algorithms trained using multiple decision trees,
- machine learning; p8; x3; Random forests are machine learning algorithms trained using multiple decision trees,
- correlation coefficient; p10; x4; Correlation coefficient R2: comparing the predictions obtained using the model with the
- linear regression; p13; x4; Logistic regression is a generalized linear regression that combines a nonlinear function

### P2025-C-06 · 题 C · 2025美赛O奖论文/C/2510006.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2510006.md
- ARIMA; p1; x43; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**
- Monte Carlo; p1; x6; and new events. For new events, we used Monte Carlo simulations to estimate medal
- linear regression; p1; x9; Olympics, linear regression, and average values to predict medal outcomes for both returning
- moving average; p1; x7; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**
- random forest; p1; x10; **regression, ARIMA (AutoRegressive Integrated Moving Average), and random forest**
- cluster analysis; p2; x6; Clustering Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- sensitivity analysis; p2; x5; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- K-means; p6; x4; **K-means clustering uses these rates to group similar**
- logistic regression; p9; x1; world rankings are available, we use logistic regression to assess the performance gaps
- decision tree; p12; x1; of countries winning ﬁrst medals. The ensemble of decision trees helps reduce overﬁtting, and
- time series analysis; p12; x7; ARIMA model and Random Forest model, using time series data and feature engineering to

### P2025-C-07 · 题 C · 2025美赛O奖论文/C/2510185.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2510185.md
- BP neural network; p1; x12; Then, to predict medal acquisition by medal-less nations/regions, we employ a BP neural
- bootstrap; p1; x5; quently, we employ the RF model with bootstrapping to generate 95% confidence intervals for
- neural network; p1; x10; Keywords: Athlete Potential Index\; Event Potential Index\; Random Forest\; BP Neural Network
- random forest; p1; x31; ver, and Bronze medals. Following a comparison of various models, we select a Random Forest
- sensitivity analysis; p2; x5; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- cross-validation; p4; x6; **50% cross validation**
- SVM; p7; x2; **SVM**
- XGBoost; p7; x12; **XGBoost**
- linear regression; p9; x6; We evaluated multiple models to select the best for prediction. Linear regression is chosen for
- decision tree; p11; x3; **DECISION TREE 1**
- machine learning; p24; x1; medal distribution – a socioeconomic machine learning model,” Technological Forecasting

### P2025-C-08 · 题 C · 2025美赛O奖论文/C/2510862.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2510862.md
- K-means; p1; x5; significant at the 2% level. K-Means clustering identified Spain, Japan, and Canada as na-
- SHAP; p1; x17; SHAP analysis revealed that for the U.S., Athletics and Rugby-related events contributed
- bootstrap; p1; x2; We also calculated 95% confidence intervals using the Bootstrap method. The findings
- cluster analysis; p1; x3; significant at the 2% level. K-Means clustering identified Spain, Japan, and Canada as na-
- correlation coefficient; p1; x7; In Task 3: We calculated Pearson correlation coefficients and used a heatmap to ana-
- cross-validation; p1; x5; Finally, 10-fold cross-validation confirmed the Stacking model’s stability, while bal-
- difference-in-differences; p1; x23; **women’s gymnastics team, focusing on coach Béla Károlyi. Using a PSM-DID model**
- propensity score matching; p1; x20; **women’s gymnastics team, focusing on coach Béla Károlyi. Using a PSM-DID model**
- sensitivity analysis; p1; x4; ance and sensitivity tests supported the robustness of the PSM-DID model. These find-
- stacking; p1; x18; puts for a Stacking ensemble model, which outperformed individual algorithms with
- machine learning; p6; x3; the first step is to construct a machine learning regression prediction model that can make
- SVM; p7; x9; (LGBM, SVM, XGBoost, and RF) into a final prediction model. Each base learner
- XGBoost; p7; x10; (LGBM, SVM, XGBoost, and RF) into a final prediction model. Each base learner
- decision tree; p7; x4; LightGBM is a gradient boosting algorithm based on decision trees. It gradually
- gradient boosting; p7; x5; **1. LightGBM (LGBM)**
- logistic regression; p7; x3; learner (logistic regression) to generate the final prediction. The core advantage of
- random forest; p8; x3; **4. Random Forest (RF)**
- Regression Analysis; p21; x1; *Table 2: DID regression analysis results*

### P2025-C-09 · 题 C · 2025美赛O奖论文/C/2513314.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2513314.md
- Bayesian; p1; x13; ## A Glimpse of Olympics Medals through Bayesian Model
- Credible Intervals; p1; x9; based posterior inference provides 95% credible intervals, assessing both medal forecasts
- Markov chain Monte Carlo; p1; x2; specific regression coefficients and a Gamma-distributed concentration parameter. MCMC-
- Posterior inference; p1; x2; based posterior inference provides 95% credible intervals, assessing both medal forecasts
- Regression Analysis; p1; x1; Quantification, Regression Analysis, Credible Intervals
- Uncertainty Quantification; p1; x1; A key strength of this model is its robust uncertainty quantification. Each country’s
- sensitivity analysis; p1; x15; To test the robustness of our model, we conducted sensitivity analyses on both the weakly
- deep learning; p4; x4; **Deep Learning**
- RNN; p7; x3; machine learning methods (e.g., RNN and two-stage RF) are clearly unsuitable, as they fail
- machine learning; p7; x3; machine learning methods (e.g., RNN and two-stage RF) are clearly unsuitable, as they fail
- Markov chain; p9; x1; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,
- Monte Carlo; p9; x1; from this posterior distribution via Markov chain Monte Carlo or other approximate methods,
- XGBoost; p10; x3; **XGBoost[1]**
- LSTM; p22; x1; [3] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural Computation,
- random forest; p22; x1; [5] Congjun Rao, Ming Liu, Mark Goh, and Jianghui Wen. 2-stage modified random forest

### P2025-C-10 · 题 C · 2025美赛O奖论文/C/2514362.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2514362.md
- Bayesian; p1; x20; Bayesian modiﬁed entropy. By introducing the Laplace smoothing technique to recon-
- Laplace smoothing; p1; x6; Bayesian modiﬁed entropy. By introducing the Laplace smoothing technique to recon-
- sensitivity analysis; p2; x16; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- zero-inflated; p2; x3; Zero expansion negative binomial model (ZINB)
- SHAP; p4; x4; event dynamics, and the inﬂuence of elite coaching. Shi et al.(2024) used SHAP method to
- SVR; p4; x2; ﬂuctuations. Zhao et al.(2012) improved accuracy by optimizing v-SVR parameters with
- bootstrap; p4; x3; tainty quantiﬁcation through asymmetric bootstrap intervals and actionable insights into
- difference-in-differences; p4; x3; requires advanced methods like DID or SHAP decomposition.
- genetic algorithm; p4; x1; genetic algorithms and incorporating home advantage adjustments.
- neural network; p4; x3; advantages, and historical performance using neural networks and a Cobb-Douglas frame-
- Causal Inference; p6; x1; Difference-in-Differences (causal inference method)
- time series analysis; p6; x1; Time series analysis can capture long-term trends in a country’s performance. If the data
- cross-validation; p20; x2; †All metrics derived from 10-fold cross-validation (N=11,234 samples\; stratiﬁed sampling)
- machine learning; p25; x2; Perspective from Explainable Machine Learning. Journal of Shanghai University of Sport, 48(4),
- Shannon entropy; p26; x2; Query2:Explain information entropy.
- decision tree; p26; x1; chine learning. In ML, entropy guides decision-making: decision trees split features to min-
- principal component analysis; p26; x1; eration (e.g., GANs, SMOTE). Feature engineering and dimensionality reduction (PCA, t-

### P2025-C-11 · 题 C · 2025美赛O奖论文/C/2514461.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2514461.md
- Cox proportional hazards; p1; x15; 2028. We employed the Cox Proportional Hazard Model, with its risk function representing the possibility that a
- LSTM; p1; x11; We first attempted at a plain Long Short Term Memory (LSTM) model. We employed the technique of the
- Mann-Kendall; p1; x8; Keywords: Threshold Method, SVR, XGBoost, LSTM, Mann-Kendall, Cox, Isolation Forest, Linear Regression,
- Monte Carlo; p1; x16; Monte-Carlo simulations, we predicted the potential number of first-time medalists by 2028. 3 is the most likely
- SVR; p1; x18; avoiding overgeneralizing to the level of sports. We employed Support Vector Regression (SVR) instead of Linear
- Threshold Method; p1; x6; In Model IV, we addressed the Great Coach Effect (GCE). We developed a Threshold Method, filtering first-
- XGBoost; p1; x29; turned to an advanced XGBoost model. In this model, we predicted fractions instead of numbers, and multiplied
- isolation forest; p1; x10; ensemble-learning anomaly detection method, Isolation Forest, was also employed to cross-validate the choice of
- linear regression; p1; x10; the prediction results of Linear Regression and Random Forest. The data for fitting are all the threshold-activated
- random forest; p1; x13; the prediction results of Linear Regression and Random Forest. The data for fitting are all the threshold-activated
- sensitivity analysis; p1; x8; insights were visualized and discussed, and sensitivity analysis was done.
- stacking; p1; x2; Swimming for TPE, are their most coach-needing sports. We then used our own ensemble learning by averaging
- SVM; p4; x5; Linear Regression, Random Forest, Support Vector Machines and Neural Networks. They are
- gradient boosting; p4; x5; Muhammad Amien Ibrahim compared XGBoost, LightGBM and CatBoost and found that
- grey prediction; p4; x2; result of women’s shot put in 2012 based on GM(1,1) prediction model in Gray System Theory,
- machine learning; p4; x3; machine learning algorithms were provided by Jhankar Moolchandani et al. [2] including
- neural network; p4; x1; Linear Regression, Random Forest, Support Vector Machines and Neural Networks. They are
- time series analysis; p4; x11; calculation methods to do so when handling time series data [5]. Yu Qin and YuanSheng Lou
- ARIMA; p7; x1; methods can be employed to forecast the number of events in the 2028 Games. While ARIMA
- Regression Analysis; p8; x3; Weconducted regression analysis on the number of past events insummerOly_programs.csv
- cross-validation; p8; x4; Grid Search coupled with 5-fold Cross-Validation. The trained model was then employed to
- decision tree; p12; x2; adds decision trees to optimize an objective function composed of a loss function for prediction
- survival analysis; p17; x1; conduct a survival analysis, treating Year as duration time and winning as the event. After
- cluster analysis; p28; x1; models like group or cluster analysis methods to account for these dependencies.

### P2025-C-12 · 题 C · 2025美赛O奖论文/C/2515235.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2515235.md
- ARIMA; p1; x2; SARIMAX and ARIMA to predict future trends in the number of events. Secondly, to handle
- SARIMA; p1; x2; SARIMAX and ARIMA to predict future trends in the number of events. Secondly, to handle
- Tobit; p1; x20; model, which combines the Mundlak-modified Tobit regression model with the Hurdle
- correlation coefficient; p1; x9; (participation rate) reveals a Pearson correlation coefficient of 0.416.
- difference-in-differences; p1; x18; ferences (DID) approach to design a dynamic DID method capable of effectively estimating
- hurdle model; p1; x17; model, which combines the Mundlak-modified Tobit regression model with the Hurdle
- logistic regression; p1; x2; In order to analyze the "Great Coach" effect, we constructed a logistic regression model
- sensitivity analysis; p1; x12; lyzed its sensitivity. By conducting error analysis between the total medal count derived from
- time series analysis; p3; x1; Time series forecasting, a common prediction method, uses historical medal counts to
- linear regression; p9; x1; This leads to truncation issues in traditional regression models. A simple linear regression
- particle swarm optimization; p11; x2; emerging countries. Finally, Particle Swarm Optimization (PSO) is used to optimize pre-
- cluster analysis; p14; x1; continents is more scattered, with no clear regional clustering of improvements.5.3.3：Ana-
- machine learning; p25; x1; tribution–a socioeconomic machine learning model," Technol. Forecast. Soc. Change,
- propensity score matching; p25; x2; [4]. F. Fan and X. Zhang, "Transformation effect of resource-based cities based on PSM-DID

### P2025-C-13 · 题 C · 2025美赛O奖论文/C/2516178.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2516178.md
- SHAP; p1; x35; small Olympic countries. Simultaneously, SHAP value analysis was utilized to uncover the
- XGBoost; p1; x59; First, following model screening, we developed a dual-stage XGBoost model for pre-
- bootstrap; p1; x10; estimation was conducted using the non-parametric Bootstrap method. After 1000 iterative ver-
- cross-validation; p1; x6; the last-block cross-validation approach, a type of time-series cross-validation.
- difference-in-differences; p1; x9; Keywords: Dual-stage XGBoost\; Non-parametric Bootstrap algorithm\; DID model\; SHAP model
- sensitivity analysis; p1; x5; In addition, a sensitivity analysis was conducted to assess the model's responsiveness to
- Tobit; p3; x4; transformation of the Tobit model and the Hurdle model are the most emblematic. Simultane-
- hurdle model; p3; x2; transformation of the Tobit model and the Hurdle model are the most emblematic. Simultane-
- machine learning; p6; x3; proposes an innovative dual-stage machine learning approach [2].
- decision tree; p8; x4; model's predicted value is the sum of the predictions from 𝐾 decision trees:
- Bayesian; p9; x2; ploy the Bayesian algorithm, specifically the Tree-structured Parzen Estimator (TPE), to de-
- feature selection; p9; x1; velop a TPE-XGBoost model for optimizing XGBoost's feature selection and hyperparameter
- logistic regression; p9; x4; an example and compare three models: XGBoost, binary logistic regression, and random forest.
- random forest; p9; x10; an example and compare three models: XGBoost, binary logistic regression, and random forest.
- time series analysis; p10; x2; adopt the last block cross-validation method, which takes the time series into account by using
- linear regression; p11; x3; the linear regression model only reaches 0.570, indicating a significant performance disparity.
- neural network; p13; x1; When evaluating the confidence intervals of neural network models, traditional ap-
- hypothesis test; p18; x1; ments, which will serve as the basis for subsequent hypothesis testing.
- Regression Analysis; p20; x3; Based on the results of the Ordinary Least Squares (OLS) regression analysis, the model
- gradient boosting; p25; x1; 4. Ibrahem Ahmed Osman, A., et al., Extreme gradient boosting (Xgboost) model to
- stacking; p25; x1; Alberta’s hydrothermal system using boosting-based ensemble learning incorporating Shapley

### P2025-C-14 · 题 C · 2025美赛O奖论文/C/2516695.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2516695.md
- Bayesian; p1; x19; ## "Golden Dynamics: Bayesian-AI Olympic Forecasting with
- Bayesian network; p1; x22; coaches critically influence outcomes. We propose SBN-DBN, a Bayesian model inte-
- Cox proportional hazards; p1; x11; Model I: Hierarchical Adaptive Reasoning Model (HARMONIE) Model II: Cox Haz-
- LSTM; p1; x12; scenarios show asymmetric US-China declines (-12.7% vs. -9.3%). Extending LSTM
- Markov chain Monte Carlo; p1; x2; MCMC sampling, we forecasted the 2028 LA Olympics medal distribution with pre-
- Monte Carlo; p1; x15; ard Analysis and Monte Carlo Prediction Model (CHAMPS) Model III: G - Coach Im-
- difference-in-differences; p1; x13; Model III: We developed a DID-GAN hybrid model to quantify the "great coach"
- sensitivity analysis; p1; x25; two-dimensional event-country framework (Figure 9) and sensitivity analysis (Section
- spatio-temporal modeling; p1; x1; coach effect\;spatio-temporal modeling\;economics\;Sensitivity Analysis
- time series analysis; p8; x2; **Layer 3: LSTM time series model[4]**
- factor analysis; p11; x1; *Figure 8: Olympic Medal Risk Factor Analysis*
- deep learning; p13; x2; Based on a hybrid architecture of Bayesian learning and deep learning, we con-
- Causal Inference; p15; x3; G-Coach Impact Quantifier (GCIQ), a hybrid causal inference framework integrating
- hypothesis test; p17; x2; • Statistical Significance Test
- centrality; p18; x6; ployed to identify key paths. The results show that Russia (node degree centrality
- neural network; p18; x1; Figure 14 models the global coach - flow network using a graph neural network
- correlation coefficient; p20; x2; events. In Figure 16, the Pearson correlation coefficient r = 0.87 (p < 0.001) vali-
- Uncertainty Quantification; p24; x1; Probabilistic calibration is validated by uncertainty quantification achieving 93.2%
- CNN; p25; x1; monthly gas field production based on the CNN - LSTM model. Energy, 260,
- self-organizing map; p25; x1; deep learning algorithms used in deep neural nets: MLP SOM and DBN. Wireless

### P2025-C-15 · 题 C · 2025美赛O奖论文/C/2517690.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2517690.md
- XGBoost; p1; x2; Regression, XGBoost Regression and Neural Network Regression models respectively, and
- cross-validation; p1; x5; country. Through ten-fold cross-validation, we compared Random Forest Regression, Lasso
- hypothesis test; p1; x7; comes, we conducted the Two-sample mean hypothesis testing and the Chi-square test to
- lasso; p1; x2; country. Through ten-fold cross-validation, we compared Random Forest Regression, Lasso
- logistic regression; p1; x14; the Logistic Regression Model to predict their probability of winning, and the results show
- machine learning; p1; x7; **Keywords: Olympics \; medal prediction \; Machine Learning \;“great coach” effect**
- neural network; p1; x4; Regression, XGBoost Regression and Neural Network Regression models respectively, and
- random forest; p1; x18; previous Olympic Games, we constructed a Random Forest regression model for predicting
- sensitivity analysis; p1; x6; Finally, we performed error evaluation and sensitivity analysis of the Cross-validation
- deep learning; p4; x1; deep learning in dealing with complex non-linear relationships. [3]J. Moolchandani, V. Chole,
- linear regression; p4; x2; various regression methods (such as linear regression, polynomial regression, ridge regression,
- ridge regression; p4; x1; various regression methods (such as linear regression, polynomial regression, ridge regression,
- time series analysis; p7; x2; **◆ Time series chart of the number of medals in each event**
- decision tree; p10; x8; diction by integrating multiple decision trees
- feature selection; p10; x1; strong feature selection ability, low risk of over-
- grey relational analysis; p15; x8; **(2) Grey Relational Analysis**

### P2025-C-16 · 题 C · 2025美赛O奖论文/C/2521556.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2521556.md
- Bayesian; p1; x10; 2028. The host country factor was considered in this step. To account for potential errors, a Bayesian
- LR-SCAD Model; p1; x5; we introduced LR-SCAD model to study how the “great coach” effect contributed to changes in the
- Residual Analysis; p1; x5; For Task 2, we performed residual analysis to find evidence of how coaches influence athletes’
- SARIMA; p1; x22; counts. We built a bottom-up medal analysis and prediction model using the TrueSkill-SARIMAX-
- TrueSkill; p1; x20; counts. We built a bottom-up medal analysis and prediction model using the TrueSkill-SARIMAX-
- sensitivity analysis; p1; x4; Lastly, we conducted sensitivity analysis on our model, finding that it demonstrates strong gener-
- random forest; p2; x10; Random Forest Model: Predicting Medals in New Events . . . . . . . . . . . . . . . .
- Gaussian Distribution; p7; x2; 𝑖. The initial Skill is drawn from a Gaussian distribution with mean 𝑚0
- time series analysis; p8; x6; is directly related to the Olympic host country, we innovatively introduced the SARIMAX time series
- linear regression; p9; x2; shorter time spans, we used simple linear regression.
- moving average; p9; x2; The SARIMAX model combines autoregression AR, moving average MA, seasonal patterns S,
- decision tree; p10; x1; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for
- stacking; p10; x1; Random Forest regression[5] is an ensemble learning method that builds multiple decision trees for
- Monte Carlo; p13; x1; So, how many countries are most likely to win medals in 2028? We conducted a Monte Carlo
- deep learning; p25; x1; [6] Deepvarma: A hybrid deep learning and varma model for chemical industry index forecasting. No

### P2025-C-17 · 题 C · 2025美赛O奖论文/C/2522820.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2522820.md
- Regression Analysis; p1; x4; Maximum Likelihood Estimate. From regression analysis on the Tobit Model, we discovered it suffered from
- Tobit; p1; x25; first consider a Tobit Model that considers random noise and unobserved random effects, optimized with a
- cluster analysis; p1; x3; Country performance was split into clusters using Density-Based Spatial Clustering of Applications with
- moving average; p1; x4; performances at the Games are time series, so we used a time series analysis incorporating a moving average.
- probit; p1; x7; to perform a Negative Binomial Regression based on the predictors, as well as a Probit Regression in the
- time series analysis; p1; x9; performances at the Games are time series, so we used a time series analysis incorporating a moving average.
- hurdle model; p2; x4; Mixed Linear Models and Hurdle Model
- Bayesian; p10; x1; We decided to use Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) as
- linear regression; p10; x1; issues). To predict the number of athletes for each country in 2028, we used a simple linear regression. Finally,

### P2025-C-18 · 题 C · 2025美赛O奖论文/C/2524070.pdf
md: corpus/papers/md/2025美赛O奖论文/C/2524070.md
- Bayesian; p1; x10; **regression model (ZINB). Adopting a Bayesian framework, we employ the Markov**
- Markov chain; p1; x4; **regression model (ZINB). Adopting a Bayesian framework, we employ the Markov**
- Markov chain Monte Carlo; p1; x11; Chain Monte Carlo (MCMC) method to derive the posterior distribution of the model
- Mixed-effects Model; p1; x7; a mixed-effects model. In this model, the pairing of coach and country is treated as a
- Monte Carlo; p1; x2; Chain Monte Carlo (MCMC) method to derive the posterior distribution of the model
- association rules; p1; x15; consequent, which led to the identification of five strong association rules. Furthermore,
- zero-inflated; p1; x18; number of medals awarded to countries, we propose a zero-inflated negative binomial
- analysis of variance; p2; x2; Analysis of Variance, Mixed-effects Model . . . . . . . . . . . . . . . . . . . . . . .
- machine learning; p6; x2; general regression or machine learning model.
- logistic regression; p8; x1; as a Bernoulli distribution process, which will be executed through logistic regression, as follows:
- Cox proportional hazards; p22; x6; reveals a noticeable trend. To address this issue, we apply the Box-Cox transformation in an effort to

### P2025-D-01 · 题 D · 2025美赛O奖论文/D/2504188.pdf
md: corpus/papers/md/2025美赛O奖论文/D/2504188.md
- A* and GA; p1; x2; of accessibility considered for each stakeholder. We used a method combining A* and GA to
- Monte Carlo; p1; x5; and original stations. Since the area is irregular, we used Monte Carlo Simulations to calculate
- centrality; p1; x11; Centrality and Degree Centrality, identifying areas in need of optimization. We then created a
- dynamic programming; p1; x6; **Availability. We used Approximate Dynamic Programming(ADP) to optimize paths in**
- nonlinear programming; p1; x1; nonlinear programming model with the objective of maximizing bus coverage, subject to
- queueing theory; p1; x6; traffic conditions, we used Queueing Theory to calculate the congestion index. For each
- sensitivity analysis; p1; x6; Lastly, we conducted sensitivity analysis to prove the robustness of the models and the
- shortest path; p7; x6; the detour’s shortest path varies depending on factors such as travel mode, destination,
- A-star; p10; x3; **specific calculation process, we innovatively combine the A* algorithm with the**
- BP neural network; p10; x1; BP
- genetic algorithm; p10; x3; **genetic algorithm to improve both efficiency and accuracy. The improved A***

### P2025-D-02 · 题 D · 2025美赛O奖论文/D/2507692.pdf
md: corpus/papers/md/2025美赛O奖论文/D/2507692.md
- cluster analysis; p1; x9; ## on Graph Theory & Clustering Algorithm
- graph theory; p1; x8; ## on Graph Theory & Clustering Algorithm
- sensitivity analysis; p1; x4; Eventually, the sensitivity analysis is carried out to ensure the accuracy of the model. However,
- shortest path; p1; x12; application of Flow Balance Equation and Dijkstra Algorithm, the influence of the bridge collapse
- entropy weight method; p2; x6; Analysis Based on Entropy Weight Method
- minimum spanning tree; p14; x5; For each cluster, we further solved the minimum spanning tree. The construction principle of the
- correlation coefficient; p16; x1; correlation coefficient to precisely measure the strength and direction of this relationship and visualized
- factor analysis; p23; x1; 2. Inadequate Complex-Factor Analysis: Despite considering multiple factors, the study of
- network analysis; p23; x1; some complex elements is incomplete. For instance, bus network analysis mainly focuses on
- machine learning; p25; x1; models, exact and heuristic algorithms, and machine learning. Expert Systems with Applica-

### P2025-D-03 · 题 D · 2025美赛O奖论文/D/2516219.pdf
md: corpus/papers/md/2025美赛O奖论文/D/2516219.md
- Bayesian; p1; x4; trian infrastructure (xp), and micro-mobility hubs (xm). The model employs Bayesian
- Markov chain; p1; x3; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**
- Markov chain Monte Carlo; p1; x4; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**
- Monte Carlo; p1; x2; **calibration with Markov Chain Monte Carlo (MCMC) to assimilate cross-city data,**
- Wardrop; p1; x11; **dynamics are analyzed through Wardrop equilibrium-based traffic assignment and**
- fuzzy comprehensive evaluation; p1; x5; **Keywords: Traffic Flow Optimization, Fuzzy Comprehensive Evaluation, Wardrop**
- network flow; p2; x2; **Urban Traffic Network Flow**
- sensitivity analysis; p2; x6; Sensitivity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- centrality; p9; x3; resilience through topological-flow synthesis. Edge betweenness centrality quantifies
- shortest path; p10; x2; where d(vi, vj) represents shortest-path distance between nodes. This formulation
- Pareto; p22; x2; methods: Pareto frontier analysis of (f1, f2, f3)
- fuzzy logic; p24; x1; [4] Goguen, Joseph A. "LA Zadeh. Fuzzy sets. Information and control, vol. 8 (1965),

### P2025-D-04 · 题 D · 2025美赛O奖论文/D/2519935.pdf
md: corpus/papers/md/2025美赛O奖论文/D/2519935.md
- Multi-layer network model; p1; x2; The proposed multi-layer network model exhibited strong robustness and stability, as con-
- TOPSIS; p1; x19; ment of new bus lines. Firstly we use the entropy-weight-TOPSIS method incorporating both
- centrality; p1; x8; subnetwork using critical nodes of the highway network, and compute the proximity centrality
- sensitivity analysis; p1; x5; firmed through sensitivity analysis, highlighting its considerable practical utility. The approach
- three-layer bus network model; p1; x5; For task 2, we develop a three-layer bus network model to determine the optimal place-
- shortest path; p2; x9; Improved Dijkstra Algorithm . . . . . . . . . . . . . . . . . . . . . . . . . . .
- entropy weight method; p13; x11; Next, we employ the entropy weight method (TOPSIS) to compute the weight of the two

### P2025-E-01 · 题 E · 2025美赛O奖论文/E/2502355.pdf
md: corpus/papers/md/2025美赛O奖论文/E/2502355.md
- AHP; p1; x9; benefits. An EWM-AHP model is developed to assess these schemes for organic farming.
- Food web model; p1; x22; complex food web model. This includes the introduction of pesticide and herbicide, followed
- centrality; p1; x39; icides, and the inclusion of bats and bees. The stability, biodiversity, and centrality indicators
- differential equation; p1; x8; For Problem 1, we mainly employ differential equations and develop the equations pro-
- entropy weight method; p1; x9; benefits. An EWM-AHP model is developed to assess these schemes for organic farming.
- graph theory; p1; x1; For Problem 2, a network is established using graph theory, with populations as nodes.
- sensitivity analysis; p1; x8; Finally, a sensitivity analysis of the herbicide power (alpha value) in our Problem 1 food
- system dynamics; p3; x1; system dynamics. Also, account for the changes on herbicides and pesticides on plants, insects,
- shortest path; p18; x1; d i j is the shortest path distance between speciesi and species j . High closeness

### P2025-E-02 · 题 E · 2025美赛O奖论文/E/2508861.pdf
md: corpus/papers/md/2025美赛O奖论文/E/2508861.md
- COMAP Model; p1; x11; Keywords: FATE Model\; COMAP Model\; Lotka-Volterra Equation\; Eco-Agriculture；
- Convex Reformulation; p1; x2; by using the Convex Reformulation Method to trade-off the ecological benefits (biodiversity
- FATE Model; p1; x7; Keywords: FATE Model\; COMAP Model\; Lotka-Volterra Equation\; Eco-Agriculture；
- Lotka-Volterra; p1; x4; In Model I, the biggest innovation is the combination of the Lotka-Volterra model with
- logistic regression; p1; x3; a generalized Logistic model, incorporating a spatial diffusion term to describe population
- multi-objective optimization; p1; x2; For Model II, our greatest highlight is to solve the multi-objective optimization problem
- sensitivity analysis; p1; x12; Finally, sensitivity analyses on Model I revealed that species mortality had a small influ-
- Food web model; p4; x1; model, and food web model, with their respective strengths and limitations shown in Figure 2.
- differential equation; p8; x2; are modeled using partial differential equations, expressed as follows:
- partial differential equation; p8; x4; are modeled using partial differential equations, expressed as follows:
- nonlinear programming; p19; x2; Planning (COMAP) model, employing multi-objective nonlinear programming to analyze the
- system dynamics; p22; x1; fluence system dynamics, highlighting the need to focus on their interactions to optimize eco-

### P2025-E-03 · 题 E · 2025美赛O奖论文/E/2515136.pdf
md: corpus/papers/md/2025美赛O奖论文/E/2515136.md
- Food web model; p1; x12; Keywords: Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger-
- Lotka-Volterra; p1; x14; (PFW) Model, drawing upon the principles of Petri nets, Lotka-Volterra theory, and energy
- Petri net; p1; x12; (PFW) Model, drawing upon the principles of Petri nets, Lotka-Volterra theory, and energy
- Petri-Food Web model; p1; x1; Keywords: Agroecosystems\; Organic agriculture\; Lotka-Volterra\; Petri-Food Web model\; Lunger-
- entropy weight method; p1; x5; ods, incorporating four primary and ten secondary indicators. The EWM was used to calculate
- fuzzy comprehensive evaluation; p1; x3; ponents, we establish OAIE Model based on a fuzzy comprehensive evaluation of the impacts of
- sensitivity analysis; p1; x9; Consequently, a sensitivity analysis was conducted on the model to ascertain its robustness.
- system dynamics; p6; x2; to model the network and use system dynamics to analyze changes in energy flow. Consequently,
- differential equation; p12; x2; Pi ←Runge-Kutta Method(Producer energy differential equation, P0, ti)
- Shannon entropy; p21; x2; Then, the information entropy of the jth indicator is calculated by the following formula.

### P2025-E-04 · 题 E · 2025美赛O奖论文/E/2517273.pdf
md: corpus/papers/md/2025美赛O奖论文/E/2517273.md
- Lotka-Volterra; p1; x6; capturing saturation effects, Holling Type III for predator-prey dynamics between ladybugs and aphids
- differential evolution; p1; x6; differential evolution algorithms, we successfully fine-tuned 27 key parameters across three distinct phases
- multi-type Holling responses; p1; x1; Keywords: differential evolution optimization, ecosystem modeling, multi-type Holling responses,
- sensitivity analysis; p1; x8; Sensitivity analysis confirms the model's critical parameter dependencies, revealing that even minor
- Food web model; p6; x1; Assumption2: In this food web model, we assume that sparrows and bats exclusively feed on
- time series analysis; p8; x1; However, for this modeling task, the traditional soil network model cannot perform time series analysis,
- logistic regression; p11; x1; the ladybug predation efficiency will become saturated. We did not use a Logistic model to describe aphid

### P2025-F-01 · 题 F · 2025美赛O奖论文/F/2504223.pdf
md: corpus/papers/md/2025美赛O奖论文/F/2504223.md
- Cox proportional hazards; p1; x7; **Keywords: VBGMM\; DID Model\; Cox TVPH\; SEM**
- VBGMM; p1; x9; areas with low GCI scores. Then, a VBGMM model is established to cluster countries
- difference-in-differences; p1; x9; **Keywords: VBGMM\; DID Model\; Cox TVPH\; SEM**
- sensitivity analysis; p1; x7; Finally, a sensitivity analysis was performed on the multi-level regression model of
- structural equation modeling; p1; x9; data of different countries and cybercrime, a structural equation model was established
- survival analysis; p1; x2; namics of their impact on cybercrime, a survival analysis model was established, and it
- Bayesian; p2; x4; Variational Bayesian Gaussian Mixture Clustering . . . . . . . . . . . . .
- cluster analysis; p2; x12; Variational Bayesian Gaussian Mixture Clustering . . . . . . . . . . . . .
- hypothesis test; p2; x2; Hypothesis Testing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
- principal component analysis; p2; x3; Principal component analysis dimensionality reduction . . . . . .
- logistic regression; p3; x2; classiﬁcation logistic regression to analyze the law of cybercrime.
- machine learning; p5; x1; encoding method helps machine learning algorithms better process and understand
- time series analysis; p22; x1; s of policy evaluation and intervention analysis and can handle different time series
- Regression Analysis; p24; x1; ative Infection Based on Logistic Multiple Regression Analysis in the Assess-

### P2025-F-02 · 题 F · 2025美赛O奖论文/F/2507789.pdf
md: corpus/papers/md/2025美赛O奖论文/F/2507789.md
- Causal Inference; p1; x6; governance. By integrating clustering analysis, causal inference, and network analysis, this
- K-means; p1; x6; The first model employs K-means clustering to categorize nations based on cybersecurity
- cluster analysis; p1; x28; governance. By integrating clustering analysis, causal inference, and network analysis, this
- difference-in-differences; p1; x5; cybercrime. The second model utilizes Difference-in-Differences (DID) analysis to establish a
- network analysis; p1; x4; governance. By integrating clustering analysis, causal inference, and network analysis, this
- sensitivity analysis; p3; x4; 8 Sensitivity Analysis..................................................................................................23
- principal component analysis; p9; x4; **To further analyze and demonstrate the clustering result, we used the PCA**
- integer programming; p14; x1; established an integer programming model:
- machine learning; p18; x1; cybercrime across different countries using statistical modeling, machine learning,
- Regression Analysis; p19; x1; ## 6.3.1 Panel Regression Analysis
- factor analysis; p21; x1; and effective." Based on Confirmatory Factor Analysis (CFA) results, the following
- structural equation modeling; p22; x2; Structural Equation Model (SEM) Schematic Diagram

### P2025-F-03 · 题 F · 2025美赛O奖论文/F/2513705.pdf
md: corpus/papers/md/2025美赛O奖论文/F/2513705.md
- K-means; p1; x6; **Key words: Cybercrime, KDMF, K-means, DID, MIC, Policy**
- KDMF; p1; x6; ## Cracking the Cyber - Puzzle: KDMF in Action
- MIC; p1; x43; we used the Maximal Information Coefficient (MIC) method and factor analysis. The results
- cluster analysis; p1; x15; Cybercrime Reporting Rate. Through descriptive analysis and K - means clustering, we found
- difference-in-differences; p1; x31; richlet Allocation (LDA) and the Difference - in - Differences (DID) model. LDA categorized
- factor analysis; p1; x14; we used the Maximal Information Coefficient (MIC) method and factor analysis. The results
- sensitivity analysis; p1; x5; Sensitivity analysis on the DID and MIC models indicates the models' stability and reliability.
- principal component analysis; p10; x3; principal component analysis (PCA) to project high - dimensional data onto a 2D plane helped
- Regression Analysis; p16; x4; Table 3 Results of OLS Regression Analysis of Data Protection and Privacy Regulations
- linear regression; p19; x1; Subsequently, step - by - step linear regression analysis was conducted using Factor 1, Factor

### P2025-F-04 · 题 F · 2025美赛O奖论文/F/2517199.pdf
md: corpus/papers/md/2025美赛O奖论文/F/2517199.md
- correlation coefficient; p1; x25; After that, Pearson correlation coefficient, Spearman rank correlation coefficient and
- time series analysis; p1; x5; handling of endogenous and exogenous variables in time series data. Endogenous
- machine learning; p23; x1; Using a combination of statistical methods and advanced machine learning

### P2025-F-05 · 题 F · 2025美赛O奖论文/F/2521039.pdf
md: corpus/papers/md/2025美赛O奖论文/F/2521039.md
- difference-in-differences; p5; x8; DID
- linear regression; p5; x8; Intercept in the baseline linear regression model
- Regression Analysis; p12; x1; merged into a complete analytical sample. In the regression analysis, the model treated
- correlation coefficient; p19; x3; tion analysis on the data, generating a Spearman correlation coefﬁcient matrix. The
- cross-validation; p26; x1; **Cross-validation: Use multiple sources like OECD and national government**

## 第三层 · 词表缺口自曝（受控词表**零命中**的篇）

本层 **0** 篇（= 43 − 第二层 43）。如为零也**照印**：这一层必须存在，空与「没写」不是一回事。这些篇要么真没用词表里的模型，要么用了词表外的模型——**这是已知漏检，登记而非掩盖**。


### 词表本身

`tools/papers/vocab/models.txt`：**150** 个词条、**415** 个变体；**一行一詞条、可追加**（用户 2026-09-26：「新遇到的模型/算法可以加入语料库」）。零命中词条与「论文里出现但词表没有」的增长候选清单在 `tests/papers/reports/ids-report.txt`。

