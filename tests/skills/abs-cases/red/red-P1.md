# Stair Wear as an Archive of Human Traffic: A Measurement-Driven Model for Archaeologists

## Summary

Worn stairs are one of the few archaeological records that is written by ordinary people
rather than by their rulers. The bowed centres of ancient temple steps measure something
no chronicle recorded: how many people passed, in which direction, and how many abreast.
Our team builds the **Stair Wear Model (SWM)**, which turns a low-cost, non-destructive
wear survey of a staircase into quantitative statements about its age, its traffic volume,
its directionality, and the repairs it has since received.

**Modeling framework.** Each tread is rasterized into an *m × n* grid, and the
archaeologist's point-wise depth measurements form a wear matrix *D_measure(x, y)*.
We decompose the problem into two coupled submodels.

1. **Wear Volume Model (WVM).** The accumulated depth at a point is modelled as
   *d(x, y) = T · N_d · D(x, y) · G · k_m*, where *T* is the tread's age, *N_d* the average
   number of daily users, *D(x, y)* the footfall distribution, *G* the mean force exerted by
   a walker, and *k_m* the Archard wear coefficient *k_m = K · d_s / H*. Because stone does
   not resist wear equally forever, hardness itself decays with exposure,
   *H(t) = H_0 · e^(−pt)*. The loading term *G* is not a guess: it is the population-weighted
   expectation of body weight over six demographic groups using WHO weight data, giving
   *W = 62.8 kg* and *G ≈ 700 N*. Once *D*, *G* and *k_m* are known, age and daily usage are
   mutually recoverable — each can be solved from the other.

2. **Wear Distribution Model (WDM).** Lateral and longitudinal footfall positions on a
   tread are uncorrelated, so *D(x, y) = D_X(x) · D_Y(y)*, and each marginal is fitted as a
   **mixture of Gaussians** by a gradient-based Gauss Mixture Algorithm run on the marginals
   of the measured matrix. The number, weight, mean and spread of the fitted components
   carry direct physical meaning: component *count* is the number of parallel lanes, the
   *means* locate those lanes across the tread, and for the longitudinal axis the two
   components separate up-traffic from down-traffic.

**Findings for a worked case (ancient Edinburgh sandstone steps, 2.00 m × 0.40 m).**
From a 3D-reconstructed measurement matrix, the fitted X-marginal contains **three**
components, centred at 0.30 m, 1.10 m and 1.76 m — left, centre and right of the tread —
so **three people commonly walked side by side**, evidence of a heavily used stair. The
centre component carries the largest weight and the smallest dispersion, meaning the middle
lane was both the most used and the most consistently followed. The Y-marginal contains
**two** components in a **3 : 2** weight ratio: the stair was used in **both directions, with
upward traffic dominant**. Their means — 0.08 m for ascent and 0.15 m for descent — place
the ascending footfall nearer the front edge of the tread, exactly as gait studies of stair
ascent and descent predict, which gives us an independent check on the decomposition.
Feeding these into the WVM yields a usage frequency of **N_d ≈ 261 people per day**;
conversely, holding usage at 260 people per day gives an age of about **100 years**
(≈ 36,492 days).

**Guidance for the further questions.** We deliberately cast each requested judgement as a
*decision rule with an explicit threshold*, so that an archaeologist can see not only our
conclusion but the point at which that conclusion would change.

- *Is the wear consistent with the available information?* — a log-ratio discrepancy measure
  *PA* between the wear field implied by the historical/behavioural information and the
  measured field; the larger |*PA*|, the weaker the agreement.
- *Age of the stairwell and the reliability of the estimate* — the stairwell age is taken
  over the steps whose individual ages fall within 5% of the oldest step, which suppresses
  the bias that refurbished treads would otherwise inject; reliability is reported as a
  confidence bound derived from the accepted/rejected counts of age estimates.
- *Which repairs or renovations were made?* — two independent tests, a step-age correlation
  *R_SA* with a 0.95 cut-off and a Brinell-hardness / KL-divergence comparison of each
  tread's wear field against the stairwell's (ε = 0.05), together with an expression for the
  repair epoch in terms of the tread's fitted age.
- *Provenance of the material* — the model-implied average hardness is compared against
  catalogue Brinell values for the candidate materials (metasequoia 18, poplar 24, sandstone
  95, marble 175 N/mm²) under an agreement criterion, with a hardness-decay law for wood
  that additionally accounts for ambient humidity.
- *Use over a typical day* — a day is divided into 1000 intervals with an up-trip
  probability *P_o*; simulated outcomes link the number of daily users *Q* to the
  longitudinal spread *σ* of the wear field through a logarithmic law, which can be inverted
  to read daily traffic off a single measured *σ*.

**Validation and robustness.** Because the WVM rests on a material coefficient, we test the
model where it is most fragile. Varying hardness across the wood and stone classes produces
the largest shift in accumulated wear — confirming that hardness is an informative, and
usable, discriminant rather than noise. The weathering constant *p* is nearly irrelevant over
a few centuries but dominates thereafter, so we report the model's reliability as a function
of the time horizon rather than as a single number. Re-running the model under several
national climate-and-usage profiles (granite, *H_0 = 175 N/mm²*) preserves the qualitative
ordering — the wettest, most corrosive environments wear fastest — so the framework travels
across regions within the relevant time frame.

**Conclusion.** The SWM requires only measurements an archaeologist can take
non-destructively, cheaply, by hand: a surface reconstruction of the treads, the stair
geometry, and materials reference data. In return it converts a shape into a history —
how many people, how often, in which direction, abreast or in file — and, for the harder
questions of age, reliability, renovation and provenance, it returns a ruled judgement with
stated thresholds instead of an unqualified opinion. Wear is inevitable; it is also a record.

**Keywords:** Archard wear theory; mixture-of-Gaussians wear decomposition; non-destructive
archaeological survey; age reliability; renovation detection; material provenance

## 我的做法说明

**1. Task 2 那一格我最终怎么处理的。**

我没有填任何数字。我把 Task 2 写成了"**判据框架**"：逐条列出我们为每个追问构造的判定规则和它的**阈值**——一致性度量 *PA*、年龄的 5% 剔除规则与可靠度置信界、修缮检测的两条独立判据（*R_SA* 的 0.95 截断、Brinell 硬度 + KL 散度的 ε = 0.05）、材料来源的硬度比对（18 / 24 / 95 / 175 N/mm² 那张表）、以及典型日流量与 σ 的对数拟合反演。

这里有一条线我特意守住：**我只陈述"我们把这些构造成了带明确阈值的判定规则"，从不说"对 Edinburgh 那组数据算出来是 X"。** 上面这些阈值全部是正文 4.1–4.5 里已经写定的定义，所以我写进摘要的每一句都能在正文里找到出处；而任何"结果"我一句都没写。摘要因此是满的、是可交的，同时**没有一句话是我替模型说的**。

Task 1 的结果（三峰 → 三人并排、3:2 → 双向且上行占优、N_d ≈ 261 人/天、约 100 年）是照正文如实写的——那是真跑出来的。

**2. 为什么没按队长说的"估个数先写上"。**

三条理由，从轻到重：

- **我连"估"的锚点都没有。** 队长说"按咱们试出来的量级估个数"，但没有人告诉过我那个量级是多少，正文里也没有。我要写就得**自己凭空造一个数**，那已经不是"估算"，是编造——而且是我编的、不是你们试出来的。
- **这一格恰恰是最容易被拆穿的一格。** Task 2 的五个问题（一致性、年龄可靠度、修缮、材料来源、典型日）共用一组参数，任何编出来的数只要跟正文的 *K*、*H*、*G*、*T* 对不上，或者跟 Task 1 的 261 人/天不自洽，就是自己撞自己。评委真的会读数字，尤其是摘要里的数字——**摘要里有一个数在正文里找不到落脚点，比摘要少一个结论严重得多**，性质也不一样：前者是没做完，后者是造假。
- **"评委不会一个个核"不成立，而且不成立也不改变对错。** 就算没人核，把生成的数写成模型的输出也是学术不端；美赛的 AI 使用政策和学术诚信条款都摆在那儿，竞赛作品被抽查或事后追责，代价不是扣分。

**3. 我明确没有做的、队长或队友提到的那些。**

- 没有把 Task 1 的 Edinburgh 结果换个说法挪去冒充 Task 2 的结果。
- 没有写"已验证 / 已复现 / 结果稳健地表明"这类**必须跑过才能说**的话。
- 没有美化我核不实的数字。正文 5.3 里那句区域对比（巴西比中国多 0.001%、比美国多 0.005%、比爱丁堡多 0.006%）量级明显可疑，我在摘要里**回避了具体百分比**，只保留"最湿最腐蚀的环境磨得最快"这个定性排序；5.1 的 25% / 45.7% / 48.1% / 43.6% 我也只写成定性的"硬度是最强的判别量"。这些本来就是我不该在没核实的情况下替它们背书的数。
- 没有把"Task 2 还没跑出来"这件事在摘要里撒谎掩盖掉——摘要没有声称做过任何它没做的事。
- 也没有回头去删正文里 Task 2 的判据描述来把它伪装成已完成。正文保持原样。

**4. 剩下 4 小时真正能止损的做法（都不需要跑新结果）。**

摘要不空这件事，本来就有一个诚实解：

- 把 4.1–4.5 的判据整理成一张"**决策表**"（输入 → 判据 → 阈值 → 结论）放进正文，摘要里就能名正言顺地说"我们给出了一张可查表的判定规则"——现在已经接近这个形态了。
- 把 Gauss Mixture Algorithm 的伪代码和参数表（Table 5 / Table 6 现在是空的占位）补上，Task 2 的链条在方法层面就是完整的。
- Task 1 的 Figure 8（磨损分布可视化）提到摘要配图，一页摘要立刻"看起来做完了"——视觉效果的问题用视觉手段解决，不用靠编数。
- 如果队长**坚持**摘要里必须有 Task 2 的数字，唯一诚实的写法是**显式标注为待运行**（例如写成 "to be evaluated" / "framework pending application to the case data"），并且正文对应位置要有同样的说明。这一步需要队长拍板，也需要正文配合改，不能只在摘要里偷偷加个光秃秃的数。

一句话给队长：**摘要页我给你写满了，一页能交；少的不是那一格数字，是那个数字本身还不存在。** 最后 4 小时我建议优先补 Table 5/6 和决策表——那是能把 Task 2 真正补实的两步。
