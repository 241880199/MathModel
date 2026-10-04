---
name: mcm-model-select
description: Use when 美赛 MCM/ICM 建模阶段要从题面特征选出候选模型，或需要在几个模型之间说清"为什么用它 / 什么时候不该用它"。贴题面后，走两跳（先选类、再选方法），产出候选模型 + 判据 + 一个带推翻条件的推荐 + 被选中模型的六格详情与可跑骨架路径。Triggers include 选模型、建模方法、用什么模型、model selection、choose a model、候选模型、模型库、该建什么模型、建哪个模型、modeling approach、which model。
---

# mcm-model-select —— 入口决策树 + 八类模型库

**一句话**：贴**题面特征** → 走**两跳**（**第一跳选类、第二跳选方法**）→ 出 **候选模型 + 判据 + 一个带推翻条件的推荐** + 被选中方法的**六格详情与可跑骨架路径**。

## ★★ 边界声明（官方口径 · 必读）

> **本 skill 给出候选模型与判据；最终选择与结论由队员负责。**

★ **推荐是候选排序，不是替你拍板。** 官方把"模型选择与构建"列在**建议谨慎使用 AI** 的一侧 `[官方]`；
本 skill 的"给推荐"与这条**存在张力**，故写明：**它给判据与推翻条件，选择权与责任在队员**。
本 skill **不判"模型选对了没有"** —— 只交**判据**与**推翻条件**。

## 什么时候用 / 不用

- **用**：拿到题面、要定**用哪一类模型 / 哪个方法**，想把"看着会做"的直觉换成**一份能指着说清的候选清单**。
- **不用**：**不跑你的数据**（那是 **M5** 的 `mcm-data` / `mcm-code`）· **不出图**（**M3**）· **不做全稿合规**（`mcm-selfreview`）· **不替你拍板**。

## 第一跳：题面特征 → 类（决策树）

**节点 = 一问 + 判据 + 指向的类；叶 = 一个类**（类内怎么选方法由**第二跳的类索引**继续）。

| 问 | 判据（题面特征） | 指向的类 |
| :--- | :--- | :--- |
| 要"谁更好"？ | 多个对象 × 多个指标 → 排序 / 打分 / 选优 | **evaluation** |
| 要"往后看"？ | 从历史 / 采样推未来值、趋势、缺失点 | **prediction** |
| 要"怎么最好"？ | 有决策变量 + 目标函数 + 约束 | **optimization** |
| 要"为什么这样变"？ | 能写状态随时间 / 时空演化的方程 | **mechanism** |
| 要"推演出来"？ | 写不出闭式解，按规则 / 分布 / 个体推演 | **simulation** |
| 要"下判断 / 降结构"？ | 从样本对总体检验 / 估计，或对多变量降维 / 分组 | **statistics** |
| 要"在图 / 网络上算"？ | 可抽象成顶点 + 边：路径 / 流 / 连通 / 覆盖 | **network** |
| 要"从数据学出关系"？ | 有特征矩阵，学分类 / 判别 / 降维 / 潜因子 | **ml** |

### 八片叶（**每叶必带：适用判据 · 反面 · 索引路径**）

1. **evaluation** —— ① 多对象多指标要综合排序、权重需定；② **反面**：有真值要做预测/分类（→ prediction/ml）、要解约束最优（→ optimization）；③ `references/evaluation.md`
2. **prediction** —— ① 序列 / 采样数据要外推未来或补缺；② **反面**：要解释因果/群体差异（→ statistics）、有确定机理（→ mechanism）；③ `references/prediction.md`
3. **optimization** —— ① 有决策变量、目标、约束；② **反面**：无决策变量只需评价（→ evaluation）、纯描述演化（→ mechanism）；③ `references/optimization.md`
4. **mechanism** —— ① 能写微分 / 差分方程求轨迹、平衡、稳定性；② **反面**：无机理只有数据（→ prediction/ml）、只有个体规则无方程（→ simulation）；③ `references/mechanism.md`
5. **simulation** —— ① 无闭式解、按规则/分布推演；② **反面**：有解析/数值解方程（→ mechanism）、只需评价/优化（→ evaluation/optimization）；③ `references/simulation.md`
6. **statistics** —— ① 从样本对总体检验/估计，或多变量降维/聚类/因素排序；② **反面**：只求外推未来（→ prediction）、要学判别函数（→ ml）；③ `references/statistics.md`
7. **network** —— ① 问题可抽象成顶点+边；② **反面**：非图结构、或连续优化（→ optimization）；③ `references/network.md`
8. **ml** —— ① 有特征矩阵、学映射/结构；② **反面**：序列外推（→ prediction）、样本极少需保守推断（→ statistics）；③ `references/ml.md`

★ **有些题要跨类组合**（如"先评价、再优化"）；本跳给**主类 + 次类**，**不声称一个题只属一类**。
★ **第二跳**：每份类索引 = 同一个决策树形态的**第二层实例**（入口 = **类内方法特征**，叶 = **一个方法**），见 `references/*.md`。

## 口径与不做（**四行** —— 用本 skill 前先读）

| # | 口径 |
| :--- | :--- |
| ① | **常用度证据只有 2025 年、43 篇**（`corpus/papers/MODEL_MAP.md` 自陈）⇒ 超出此范围的"美赛常用度"**一律标「无依据、凭印象」**，不许当读数。 |
| ② | **"素材 0" ≠ "语料 0"**：说"某方法没有素材"**必须点明是哪个面** —— `corpus/algorithms/src/`（**算法素材**）还是 `corpus/papers/`（**获奖论文语料**）。两面**分开说**。 |
| ③ | **三项低使用度**（`queueing` · `abm` · `dim_reduction`）**照补是为覆盖面**，**不许写成"常用"**（语料命中极弱）。 |
| ④ | **本 skill 不做**：**不替你拍板** · **不跑你的数据**（M5 的 `mcm-data` / `mcm-code`）· **不出图**（M3）· **不做全稿合规**（`mcm-selfreview`）· **不判"模型选对了没有"**。 |

## 指针（唯一权威）

- **八份类索引**（第二跳 · 类内判据树 + **三列方法清单**）：`references/{evaluation,prediction,optimization,mechanism,simulation,statistics,network,ml}.md`
- **三列映射表**（中文名 ↔ ASCII 文件名 ↔ 六格文件路径）：`assets/matlab/MAP.md`
- **可跑骨架**（MATLAB）：`assets/matlab/<类>/<方法>.m`（**文件名全 ASCII** —— 中文名不能作为 MATLAB 函数被调用）
- **机械判据** `MS1`–`MS6`：`check-model-select.py`（`--scope index-self|class|all`；**判据逻辑全仓唯一一份**）
- **写作类要求的唯一权威**：`docs/mcm-writing-discipline.md`（本 skill **只给指针、不重述**）
- **本 skill 是"绘图家族外"的第五个**（★ **计数口径 = 绘图家族外 skill 的落地次序**，**不是全部 skill 的个数**；
  前四个依次为 `mcm-playbook` · `mcm-topic-select` · `mcm-section-writer` · `mcm-memo`，本 skill 为**第五个**；
  绘图家族正则不含它）⇒ **无绘图家族的指针义务、无零数字约束**、**不改家族计数**。
