# 选题决策 · 2025 六题（A–F）

本次拿到的是六道题的题面（`problems/A.md`–`F.md`，即 2025 MCM/ICM 的 A–F）。
本文件按 `mcm-topic-select` 的输出契约逐题给出：**分类（标签 + 题面原句为证）+ 同型历史 + 四轴证据档**，
最后给**一个带推翻条件的推荐**。四轴**不编 1–5 分**，只交证据档，推荐从证据档里推出来。

**边界（凡引用语料必带）**
- 语料（`corpus/papers/PROBLEM_TYPES.md` 的标签与数据形态、`MODEL_MAP.md` 的模型配对）是**我们的标注件，不是官方口径**。
- `MODEL_MAP.md` **只覆盖 2025 那一年**（`corpus/历届优秀论文/` 里只有 `2025美赛O奖论文` 建过索引）⇒ 模型配对证据**偏薄**，**不得**拿别的年份的论文来凑。
- `场景` 标签**不进配对**；配对的推理轴只有 `数学任务 × 数据形态` 两条。
- 「拥挤风险」是四轴里**最软**的一条，且**可能整体偏**（"看着不挤"未必真不挤）；**不预测选题人数**，赛期内无从知晓。
- **巧合登记（如实）**：本轮拿到的六道题面与语料里的 **2025 A–F 同文**，故本轮现打的标签与语料 2025 的标注一致；这本该是两条独立的线（语料覆盖往年题面），此处如实标出这一巧合，不冒充"语料当年就是这么标的"。

---

## 题 A — Testing Time: The Constant Wear On Stairs

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"Your model should provide some basic predictions given the patterns of wear on a particular set of stairs"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"The stone and other materials used to create steps are subject to constant, long-term wear, and the wear can be uneven."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"What is the age of the stairwell and how reliable is the estimate?"* |
| `附带` **5 统计推断与因果 · 5.5 关联/相关模式** | *"Is the wear consistent with the information available?"* |

- 历史：组合 `6 反演与参数估计 · 6.1 由观测反推参数/历史` × `无数据(纯机理/假设)`，出现 2 次
- 历史：题 `2025 A` 用过模型 `Archard Law`，5 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**不给任何数据集**，测量方案由队伍自定（*"an archaeologist has access to the structure in question and can obtain whatever measurement your team believes is important"*），且限定非破坏、低成本、小团队（*"non-destructive, the cost must be relatively low"*）⇒ 不依赖外部数据即可起步；未知——自定测量方案在真实遗迹上的可行性与精度；依据——题面把「量什么、怎么量」交给队伍，故数据这一轴属"题面自给"部分（可核原句）；外部数据源本支不查。
- 轴 2 · 难度【判断】：已知——这是**逆问题**（由磨损形态反推使用史与年代），映射**不唯一**，还须同时给出年代估计的**可靠性**与材料来源判断；未知——反演的可辨识性（不同使用史能否产生同一磨损形态）；依据（判断）——逆问题 + 非唯一映射 + 测量受"非破坏/低成本"硬约束 ⇒ 难度偏高，但模型自足、题面明写 partial solutions are accepted ⇒ **可交付**（不判"否"）。★ 这是判断，不是读数。
- 轴 3 · 拥挤风险【判断】：已知（题面特征逐条比对）——"一眼就懂"有（考古/台阶，易懂）、"趣味性强"有（考古题材）；"套路常见（能套模板）"**弱**（逆问题不像回归/优化那样有现成模板）、"自带数据（省事）"**无**；未知——今年真实的选题分布（赛期内不可知）；依据（判断）——缺"自带数据"与"现成模板"这两个吸人特征 ⇒ 相对 C/D/B 不易扎堆；仅"趣味性"会吸一部分人 ⇒ 只能**当软证据**。
- 轴 4 · 创新空间【半可核】：已知——语料同型组合 `6 反演与参数估计 · 6.1 由观测反推参数/历史` × `无数据(纯机理/假设)` 共 2 道（2018 A 附带、2025 A 核心），2025 A 的 O 奖论文**全部 5 篇**都用了 `Archard Law`（↔ `MODEL_MAP.md`，只覆盖 2025）；未知——"你这一版算不算新"仍是判断；依据——语料读数（可核）+ 判断 ⇒ 直接套 Archard 磨损律 = 落进那 5 篇同一堆；差异化空间在**把频次/方向/并行人数的异质使用史与测量不确定性一起反演**。

## 题 B — Managing Sustainable Tourism

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"State clearly which factors you are optimizing, and which factors serve as constraints"* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"show how these expenditures feed back into your model to promote sustainable tourism"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"your predictions, the effects of various measures"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Include a sensitivity analysis and discuss which factors are most important"* |
| `附带` **2 评价与排序 · 2.4 方案比较** | *"Various measures have been enacted to attempt to ease the burden, including increased hotel taxes, visitor fees, caps on the number of daily visitors"* |

- 历史：组合 `3 优化 · 3.3 多目标/权衡` × `无数据(纯机理/假设)`，出现 7 次
- 历史：题 `2025 B` 用过模型 `sensitivity analysis`，7 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**不给数据集**，只给 Juneau 案例事实（2023 年 160 万邮轮乘客、约 3.75 亿美元收益、冰川退却、已实施的税费/每日上限）与 4 条参考链接；未知——自采的旅游/承载力数据的可得性；依据——题面（案例背景 + 链接，题面提到 ≠ 附件里有）。
- 轴 2 · 难度【判断】：已知——需自建"游客—收益—承载力—措施"系统模型，明确优化目标与约束、并让支出**反馈**进模型，还要做敏感性；未知——自设因素的合理性边界；依据（判断）——系统动力学/多目标优化是标准方法，难度中等。
- 轴 3 · 拥挤风险【判断】：已知——"一眼就懂"有（旅游）、"套路常见"有（优化 + 敏感性模板）、"趣味性强"有；未知——真实选题分布；依据（判断）——三个吸人特征里中两个 ⇒ 偏挤（**软证据**）。
- 轴 4 · 创新空间【半可核】：已知——同型组合出现 7 次（2016 B、2017 B、2022 B、2023 Z、2025 B、2025 E、2026 B）；2025 B 论文 7 篇，`sensitivity analysis` 7 篇、`multi-objective optimization` 4 篇、`system dynamics` 3 篇（↔ `MODEL_MAP.md`）；未知——你这版算不算新；依据——读数 + 判断 ⇒ 用"多目标 + 敏感性"会落进主流那一堆。

## 题 C — Models for Olympic Medal Tables

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"Develop a model for medal counts for each country"* |
| `核心` **1 预测 · 1.5 零膨胀/受限计数预测** | *"countries that have yet to earn medals"* |
| `核心` **5 统计推断与因果 · 5.2 回归系数与效应量** | *"How much do you estimate such an effect contributes to medal counts?"* |
| `核心` **7 分类与聚类 · 7.1 监督分类/识别** | *"Which countries do you believe are most likely to improve?"* |
| `附带` **5 统计推断与因果 · 5.3 因果/政策评估** | *"How do the events chosen by the home country impact results?"* |

- 历史：组合 `1 预测 · 1.2 回归/相关预测` × `面板`，出现 2 次
- 历史：题 `2025 C` 用过模型 `sensitivity analysis`，16 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**提供 5 个数据文件**（奖牌榜、主办国、项目数、运动员明细），并明令 *"Your models and data analysis must ONLY use the provided data sets"* ⇒ 数据可得性最强的一档（无需自采）；未知——数据清洗口径（IOC 国名变更、Team 细分、记录异常）；依据——题面数据清单 + 原句。
- 轴 2 · 难度【判断】：已知——要预测奖牌数、给预测区间、含尚未得牌国家的首金概率、估"名帅"效应量；未知——小样本（届次少）+ 大量零计数下模型的表现；依据（判断）——方法成熟（回归/计数模型），难度中等。
- 轴 3 · 拥挤风险【判断】：已知——"自带数据（省事）"有、"一眼就懂"有（奥运奖牌）、"套路常见（能套模板）"有（回归/ML）；未知——真实选题分布；依据（判断）——**三个吸人特征全中** ⇒ 最可能挤（**软证据**，也可能是四题里最挤的）。
- 轴 4 · 创新空间【半可核】：已知——同型组合 `1 预测 · 1.2 回归/相关预测` × `面板` 出现 2 次（2019 C、2025 C）；2025 C 论文 18 篇，`sensitivity analysis` 16 篇、`machine learning` 14 篇、`random forest` 13 篇（↔ `MODEL_MAP.md`）；未知——你这版算不算新；依据——读数 + 判断 ⇒ 常规做法**极度饱和**，难出彩。

## 题 D — A Roadmap to a Better City

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"A file with vehicle counts on street segments is provided"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"identifying, prioritizing, and implementing initiatives"* |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"All of Baltimore's transportation plans affect multiple stakeholders with differing perspectives"* |
| `附带` **3 优化 · 3.5 调度与配置** | *"recommending ways to improve"* |

- 历史：组合 `8 网络与图 · 8.2 流量分配/路由` × `网络`，出现 1 次
- 历史：题 `2025 D` 用过模型 `sensitivity analysis`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**提供 9 个数据文件**（路网节点/边、公交线路与站点、AADT 车流量等），并明说 *"teams are not limited to these data"* ⇒ 数据充裕；未知——数据清洗（路名分段变化、坐标接边）；依据——题面文件清单。
- 轴 2 · 难度【判断】：已知——要建网络模型、评桥塌/重建与公交/步行的项目影响、在多利益相关者间做优先级；未知——数据清洗工作量对交付的挤压；依据（判断）——网络方法成熟，但工程量大，难度中。
- 轴 3 · 拥挤风险【判断】：已知——"自带数据（省事）"有、"一眼就懂"有（城市交通）、"套路常见"有（最短路/中心性）；未知——真实选题分布；依据（判断）——吸人特征多 ⇒ 偏挤（**软证据**）。
- 轴 4 · 创新空间【半可核】：已知——同型组合 `8 网络与图 · 8.2 流量分配/路由` × `网络` 只出现 1 次（2025 D）；2025 D 论文 4 篇，`shortest path` 4 篇、`centrality` 3 篇（↔ `MODEL_MAP.md`）；未知——你这版算不算新；依据——读数 + 判断 ⇒ 主流是最短路/中心性；差异化空间在**多利益相关者权衡 + 桥塌中断情景**这一层。

## 题 E — Making Room for Agriculture

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Build a basic food web model for this new agricultural ecosystem"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Consideration should be given to different scenarios with varying components of organic farming"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"economic trade-offs as well as sustainability"* |
| `附带` **9 决策与博弈 · 9.1 多准则决策** | *"Advise the farmer on what methods should be employed"* |

- 历史：组合 `4 机理建模与仿真 · 4.2 生态/生物动力学` × `无数据(纯机理/假设)`，出现 4 次
- 历史：题 `2025 E` 用过模型 `Food web model`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**不给数据集**，允许自设假设（*"You can make assumptions"*）或用 *"a real historic sample of this kind of evolution"* ⇒ 不依赖外部数据即可起步；未知——若选真实样本，样本的可得性；依据——题面原句。
- 轴 2 · 难度【判断】：已知——要建森林→农田演替的食物网动力学（含季节性、农药/除草剂影响），再比较化学/有机路径；未知——物种与参数众多时模型的稳定性与可解释性；依据（判断）——食物网/洛特卡–沃尔泰拉类方法经典，难度中偏易。
- 轴 3 · 拥挤风险【判断】：已知——"一眼就懂"有（森林变农田）、"套路常见"有（食物网/LV 模型现成模板）、"趣味性"中；未知——真实选题分布；依据（判断）——"套路常见"明显 ⇒ 偏挤（**软证据**）。
- 轴 4 · 创新空间【半可核】：已知——同型组合 `4 机理建模与仿真 · 4.2 生态/生物动力学` × `无数据(纯机理/假设)` 出现 4 次（2019 A、2023 A、2024 A、2025 E）；2025 E 论文 4 篇**全部**用 `Food web model`、3 篇用 `Lotka-Volterra`（↔ `MODEL_MAP.md`）；未知——你这版算不算新；依据——读数 + 判断 ⇒ 用标准食物网会落进那 4 篇同一堆。

## 题 F — Cyber Strong?

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"identify parts of a policy or law that are particularly effective (or particularly ineffective) in addressing cybercrime"* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Develop a theory for what makes a strong national cybersecurity policy and present a data-driven analysis to support your theory"* |
| `核心` **7 分类与聚类 · 7.2 无监督聚类/分段** | *"How is cybercrime distributed across the globe?"* |
| `附带` **10 文本与语义处理 · 10.2 主题与语义归类** | *"As you explore the published national security policies of various countries and compare these with the distribution of cybercrimes"* |

- 历史：组合 `5 统计推断与因果 · 5.3 因果/政策评估` × `混合`，出现 7 次
- 历史：题 `2025 F` 用过模型 `Regression Analysis`，4 篇
- 轴 1 · 数据可得性 + 可信度【半可核】：已知——题面**不给数据集**，只给线索（ITU GCI、VERIS/VCDB），并明说 *"be mindful of the veracity and completeness of those sources"*、要求讨论数据局限；未知——跨国网络犯罪/政策数据的可得性、可比性与完整性（题面自陈大量未报案/瞒报）⇒ **数据风险最高的题**；依据——题面原句（数据须自采 + 自陈不可靠）。
- 轴 2 · 难度【判断】：已知——要先立"什么算强的政策"的**理论**再做数据驱动验证，任务开放、缺少现成模板；未知——理论与数据能否自洽；依据（判断）——数据与理论双难，难度高。
- 轴 3 · 拥挤风险【判断】：已知——"一眼就懂"有（网络安全）、"趣味性强"有；"套路常见"**弱**（无现成模板）、"自带数据"**无**；未知——真实选题分布；依据（判断）——吸人特征少于 C/D/B，但"叙事性强"仍会吸人 ⇒ **软证据**。
- 轴 4 · 创新空间【半可核】：已知——同型组合 `5 统计推断与因果 · 5.3 因果/政策评估` × `混合` 出现 7 次（2016 D、2020 C、2021 D、2023 F、2024 F、2025 F、2026 F）；2025 F 论文 4 篇用 `Regression Analysis` 与 `difference-in-differences`（↔ `MODEL_MAP.md`）；未知——你这版算不算新；依据——读数 + 判断 ⇒ 主流是"回归 + 双重差分"；**理论原创空间大**，但被数据可得性拖累。

---

## 推荐

- 推荐：题 A
- 推翻条件：**① 若队伍在轴 2（判断）上认定"这套逆问题做不出一版可交付的东西"**（例如给不出自洽的「磨损形态→使用史/年代」映射，或测量方案在"非破坏、低成本、小团队"约束下讲不圆）⇒ 推翻，改选轴 1/2 更稳的题（C 或 D：数据由题面提供、方法成熟）。**② 若"自定测量方案"在真实遗迹上被证否**（轴 1 的未知项被证否：拿不到可用的磨损剖面）⇒ 推翻——注意本支核不了任何数据源的真伪，这条只能由队伍核实。**③ 若队伍的唯一目标就是"绝对做得完"而非"做得不同"** ⇒ 让位于题 C（数据最强、交付最稳）；这是"用软证据换确定性"的取舍，属允许的覆盖。**④ 轴 3 是四轴里最软、且可能整体偏**（"看着不挤"未必真不挤）⇒ 若实际开赛热度与本题面特征相反，本推荐的相对排序会被轴 3 拉偏，须并入重估。**⑤ 时间盒到点仍分不开**（轴 1/2 上两题难分）⇒ 保留"分不开"这一事实写进本行的推翻条件，不要再拖过时间盒。
