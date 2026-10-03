# 选题决策 —— 已知好产出（fixture）

> ★ 本文件是 `check-topic-select.py` 的**已知好产出** fixture：供判据自测、变异基线与
> `--output` 默认值使用。**六道题面是构造的**（`fixtures/problems/`，仅用于机械自测）；
> **历史读数取自真实语料**（`corpus/papers/{PROBLEM_TYPES,MODEL_MAP}.md`，现取）。
> ★ 它**不是**一次真实赛事的产物，**不声称**任何题面或推荐的正确性。
> ★ 它的**逐字形态**照 `.claude/skills/mcm-topic-select/references/method.md` §5
> （判据 `S1`–`S4` 读的就是那份形态；本 fixture 与它必须一致）。

## 题 A — Keeping a Coffee Cup Warm

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Develop a model of the temperature of the coffee in space and time as it cools"* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"determine the best strategy the person can adopt to keep the temperature as close as possible to the initial temperature"* |

- 历史：组合 `4 机理建模与仿真 · 4.1 物理/化学机理建模` × `无数据(纯机理/假设)`，出现 8 次
- 历史：题 `2025 A` 用过模型 `Archard Law`，5 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面自设几何与参数；未知具体材料常数；依据 = 题面原句（自设）。
- 轴 2 · 难度【判断】：一维/二维传热方程数值求解属中等难度；依据 = 模型的复杂度与求解代价。
- 轴 3 · 拥挤风险【判断】：题面一眼就懂、场景日常，可能吸引人扎堆；依据 = 题面特征，非任何数据。
- 轴 4 · 创新空间【半可核】：历史上多用守恒律写作；再用标准 PDE 只是跟随。

## 题 B — Managing a National Park

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Recommend a management policy that simultaneously maximizes revenue and minimizes ecological impact"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Your model should include quantitative and/or qualitative estimates of costs, risks, and benefits"* |

- 历史：组合 `3 优化 · 3.3 多目标/权衡` × `无数据(纯机理/假设)`，出现 7 次
- 历史：题 `2025 B` 用过模型 `multi-objective optimization`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面给了权衡对象；未知具体客流与生态数据来源；依据 = 题面原句。
- 轴 2 · 难度【判断】：多目标建模与权衡方式的选择是难点；依据 = 目标冲突的复杂度。
- 轴 3 · 拥挤风险【判断】：多目标 + 旅游题材套路常见，可能吸引人扎堆；依据 = 题面特征。
- 轴 4 · 创新空间【半可核】：历史上多用 Pareto/加权类方法；再用同族方法只是跟随。

## 题 C — Predicting the Medal Table

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"predict the number of medals each country will win in the next Games under several growth scenarios"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"give a range for each estimate"* |

- 历史：组合 `1 预测 · 1.3 情景与概率预测` × `混合`，出现 10 次
- 历史：题 `2025 C` 用过模型 `random forest`，13 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面提到历史记录；未知数据集的完整性与年份范围；依据 = 题面原句。
- 轴 2 · 难度【判断】：面板预测 + 区间估计的难度中等偏高；依据 = 需要的特征工程与验证设计。
- 轴 3 · 拥挤风险【判断】：奖牌预测是经典题材、套路成熟，可能吸引人扎堆；依据 = 题面特征。
- 轴 4 · 创新空间【半可核】：历史上随机森林类方法用得很多；再用同类集成只是跟随。

## 题 D — Rerouting a Delivery Fleet

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.4 动态与随机** | *"Develop a time-dependent model to determine the best alternative or combination of alternatives"* |
| `核心` **3 优化 · 3.5 调度与配置** | *"decide, hour by hour, how many trucks to dispatch and along which routes"* |

- 历史：组合 `3 优化 · 3.4 动态与随机` × `无数据(纯机理/假设)`，出现 7 次
- 历史：题 `2025 D` 用过模型 `shortest path`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面给了不确定需求；未知真实路网与订单数据；依据 = 题面原句。
- 轴 2 · 难度【判断】：动态随机调度做成可交付的一版偏难；依据 = 状态空间与求解代价。
- 轴 3 · 拥挤风险【判断】：路径与调度题材套路常见、易套模板，可能吸引人扎堆；依据 = 题面特征。
- 轴 4 · 创新空间【半可核】：历史上最短路径/网络流类方法很多；再用同族方法只是跟随。

## 题 E — The Cost of Uncertainty

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Quantify the uncertainty of your conclusions and examine how sensitive they are to the assumptions and parameters you chose"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"allocate a fixed budget among several programs whose outcomes are noisy"* |

- 历史：组合 `5 统计推断与因果 · 5.4 不确定性与敏感性` × `无数据(纯机理/假设)`，出现 5 次
- 历史：题 `2025 E` 用过模型 `Lotka-Volterra`，3 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面给了预算约束；未知各项目的产出分布；依据 = 题面原句。
- 轴 2 · 难度【判断】：不确定性量化与敏感性分析的落地难度中等；依据 = 需要多少假设与计算。
- 轴 3 · 拥挤风险【判断】：题材抽象、不易套模板，拥挤风险可能偏低；依据 = 题面特征（**本轴最软**）。
- 轴 4 · 创新空间【半可核】：历史上多用微分方程/生态模型类工具；换一套不确定性框架或可做出不同一版。

## 题 F — Did the Policy Work?

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"Determine whether this policy caused the observed change in outcomes"* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"using past data and a counterfactual argument"* |

- 历史：组合 `5 统计推断与因果 · 5.3 因果/政策评估` × `混合`，出现 7 次
- 历史：题 `2025 F` 用过模型 `difference-in-differences`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知题面提到过去数据；未知对照组的构造方式；依据 = 题面原句。
- 轴 2 · 难度【判断】：反事实论证要立得住偏难；依据 = 识别策略的强度。
- 轴 3 · 拥挤风险【判断】：政策评估题材常见、DID 易套模板，可能吸引人扎堆；依据 = 题面特征。
- 轴 4 · 创新空间【半可核】：历史上 DID/PSM 类方法很多；再用同族方法只是跟随。

## 推荐

- 推荐：题 A
- 推翻条件：若轴 1 的数据来源当场核不清、或轴 2 判定实际做不出可交付的一版，则推翻本推荐；
  ★ 另：轴 3 是四轴里最软的一条（无任何数据、可能整体偏），**不得单独据此推翻或确立推荐**。
