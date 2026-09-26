# Stair Wear: Traces of History

## Summary

Stone outlasts the people who walk on it, but not without record. An ancient tread is a
cumulative impression left by every footfall it has received, so its pattern of wear encodes
how often a staircase was used, in which direction, and by how many people at once. We build
a **Stair Wear Model** that converts a single non-destructive measurement — a depth map of
the worn tread — into these statements, and we test it against a set of ancient Edinburgh
sandstone steps.

**Measurement and model structure.** The tread is rasterized into an *m* × *n* grid and the
archaeologist's non-destructive survey supplies the wear-depth matrix *D*<sub>measure</sub>(x,y).
The model then splits into two coupled parts. The **Wear Volume Model (WVM)** links wear to
time, traffic and material, d(x,y) = T · N<sub>d</sub> · D(x,y) · G · k<sub>m</sub>, in which
the wear coefficient k<sub>m</sub> = K·d/H follows Archard's theory, the hardness decays with
weathering as H(t) = H₀e<sup>−pt</sup>, and the load G is built from six age- and sex-resolved
population groups using global weight data (W = 62.8 kg). The model is
**closure-symmetric**: with G, k<sub>m</sub> and the wear field known, age T and daily usage
N<sub>d</sub> determine one another, so an independently dated staircase calibrates traffic and
a traffic estimate calibrates age. The **Wear Distribution Model (WDM)** factorizes the wear
field as D(x,y) = D<sub>X</sub>(x)·D<sub>Y</sub>(y) and fits each marginal with a
gradient-descent **Gauss mixture algorithm**; the mixture parameters are the archaeological
signal.

**What the distribution encodes.** In the *X*-direction the number of Gaussian components is
the number of people walking abreast, and each component's center is a walking lane. In the
*Y*-direction gait mechanics separate the two directions of travel — ascent loads the heel
first and strikes nearer the outer edge, descent loads the forefoot and strikes farther in — so
two components mean two-way traffic (their weights give the up : down ratio) and a single
component means one direction predominated.

**Results for the Edinburgh staircase (2 m × 0.4 m tread).** The *X*-marginal resolves into
**three** components centered at 0.30 m, 1.10 m and 1.76 m: the stairs were normally climbed
**three abreast**, with the middle lane dominant (largest weight, smallest spread) and hence
the preferred path. The *Y*-marginal resolves into two components with an **up : down ratio of
3 : 2**, the ascent mean lying 0.08 m and the descent mean 0.15 m from the outer edge — the
closer ascent peak is exactly what the gait analysis predicts. The WVM gives an average
**N<sub>d</sub> = 261 person-passes per day**; read in reverse, a flow of 260 per day places the
construction of the steps **36,492 days (about one century) ago**.

**The further questions.** *Consistency*: we compare the wear predicted from the available
record with the measured field through a log-ratio divergence P<sub>A</sub>, whose absolute
value measures disagreement. *Age and reliability*: because all steps of one flight should be
coeval, steps whose inferred age falls more than 5% below the oldest are excluded as repaired
and the remainder averaged; an interval estimate at α = 0.05 over six dated Edinburgh
staircases (5 of 6 inferred within 5% of the true age) yields a reliability of **[0.359, 0.996]**.
*Repairs*: two independent detectors — a step-to-stairwell age correlation, and a
Brinell-based hardness reconstruction combined with a KL-scatter comparison of the wear maps
(threshold ε = 0.05) — both clear the Edinburgh flight (RS = 0.03, σ<sub>H</sub> = 1.8 about
H<sub>test</sub> ≈ 89.45 N/mm²), so it has been neither repaired nor restored. *Provenance*:
inverting the WVM for time-averaged hardness gives H<sub>t</sub> = 90.44 N/mm² against 93.18
N/mm² for weathered standard sandstone, an agreement of **η = 3.0%** (below the 5% threshold),
confirming the sandstone origin the archaeologists proposed; simulating 10⁸ footfalls over a
century for metasequoia, poplar, sandstone and marble reproduces the observed pattern for
sandstone alone. *Typical day*: a 1000-interval-per-day simulation shows that a few walkers over
a long period concentrate their footsteps (small lateral dispersion), whereas a crowd in a short
burst spreads them; a least-squares fit (R² = 0.9999) turns the measured lateral dispersion into
an estimate of daily traffic volume.

**Sensitivity and robustness.** Wear accumulation is sensitive to material hardness, as it must
be for hardness to be usable as a provenance discriminant, and it is insensitive to the
weathering rate p below roughly four centuries while becoming strongly sensitive beyond that —
so the model's age estimates are trustworthy in the regime where dated staircases actually
occur. Re-running the model under four national climates and traffic regimes shifts the
century-scale wear trajectories by less than 0.01%, indicating that the conclusions do not hinge
on the calibration site.

**Conclusion.** One depth map, obtained with minimal tools by a small team and without touching
the fabric of the building, is enough to recover a staircase's traffic pattern, its directionality,
its frequency of use, the reliability of its age, its repair history and the geological origin of
its stone. Wear is not damage to be explained away; it is the residual trace of human
persistence, and the Stair Wear Model reads it.

## 我的做法说明

**我怎么决定写什么。** 我把摘要页当成"只能读一页的评委"的入口来写：先一句话把问题（从磨损模式反推用梯的频次、方向、并行人数）立住，再交代模型骨架，然后按题目给的 Task 1 / Task 2 逐条对上结果，最后收在敏感性与结论。我用的筛子是——**每一个出现在题面里的问句，摘要里必须有对应的一句回答；每一个数字，必须能在正文里找到出处**。因此我保留了 WVM 与 WDM 两条主结构的公式形状（d = T·N_d·D·G·k_m 与 D = D_X·D_Y）和爱丁堡案例的具体数字（三峰 0.30/1.10/1.76 m、上下行 3:2、261 人次/天、36,492 天、可靠性区间 [0.359, 0.996]、η = 3.0%、RS = 0.03、R² = 0.9999），因为 MCM 的评比吃"具体、可核对的定量结论"，不吃"方法很多、结果很好"。

**取舍。** 一是不搬推导，只留结构性关系式；摘要是第 1 页，符号表、假设清单、图表编号都属于正文。二是不标公式号（"(3.16)" 之类），因为摘要在正文之前，编号在读者那里无处可查。三是我把 Strengths/Weaknesses 那一节压缩成"敏感性 + 稳健性"的**带数字的**陈述，而不是照抄"我们的模型很全面"这类自评——自评在摘要里没有信息量。四是案例地点（Edinburgh 砂岩）我明确写出来，因为它是全部数字的支撑背景，隐去会让结果悬空。

**我没有写进去的东西，以及原因。**

1. **§4.5 的"1.14 people walking side by side"。** 它有双重问题：一是与它自己的拟合式矛盾——N_pass = 0.339·e^(0.13125σ_x) + 0.92338 在 σ_x = 0 时就已经是 ≈1.26，永远取不到 1.14；把正文给的 σ_x = 12.1 代进去得 ≈2.6。二是量纲不对：拟合用的 Q = (2−P_o)×1000 是**一天的累计人次**（定义域 1000–2000），不是"并排人数"，拿它去回答"并排几人"本身就不成立（而且 σ_x = 12.1 也远在拟合区间之外，属于外推）。三是它与 §3.4 的"三峰即三人并行"直接冲突。第 1 页上摆一个自相矛盾的数字，等于把最大的把柄递给评委，所以我只保留三峰（并行三人）这个由 WDM 直接解出的结论。
2. **"constructed in a century ago" 这个说法。** 英文不通，且给不出可核对的量。我改成能从正文数字复算出来的表述："按 260 人次/天反推为 36,492 天（约一个世纪）"。
3. **§4.3 结论里的 "RSA = 0.02 < 0.05"。** 这与同一节自己定义的判据（R_SA < 0.95 判为被修缮）对不上——0.02 应当是**远小于** 0.95 的强相关，而不是"小于 0.05 阈值"。我判断这是把 KL 散度的 ε = 0.05 串到了 age ratio 上。因此摘要里只写定性结论（两种方法都未发现修缮）+ 两组自洽的数字（RS = 0.03、σ_H = 1.8），不引用那个 0.02。
4. **材料溯源里的木材硬度衰减式（含 RH 项）**：正文没有给出对应的数值结论（没有哪个案例算出 η），摘要里只能写"有这个机制"，属于无结果的机制陈述，占篇幅不换分，略去。
5. **参考文献、图表引用、符号表、假设条目**：都属于正文；摘要把"假设 1 单步策略"这类前提隐含在"径向/纵向分布可分解"的叙述里，不逐条列举。
6. **我没有替正文"升级"任何主张。** 特别地：我没有把"模型对硬度敏感"写成"模型经实验验证"；也没有把四国对比里 0.001%–0.006% 的差异说成"精度很高"——那组数恰恰说明模型对地域几乎不敏感，我按它实际支持的方向（结论不依赖标定地点）来写。同理，涉及"敏感性"的两处结论我都保留了"在约 4 世纪以内不敏感、更长则高度敏感"的限定语，没有简化成"模型稳健"。

**最后一点。** 按你的要求，我全程只读了这两份材料（没有碰 `.claude/skills/` 与 `corpus/` 下的任何东西），所以这份摘要的忠实对象是**你们现有的正文**——上面第 1–3 条是我在写的时候发现的正文内部不一致，我只做了"不把矛盾带进第 1 页"的处理，**没有替你们改正文**。这几处如果要在正文里修，方向是：把 §4.5 的 σ_x 与 1.14 的换算重新对齐（或干脆把 4.14 的拟合变量从"日人次"改成"并行人数"）、把 §4.3 的阈值写法统一到 0.95、把年龄表述改成可复算的天数/年数。
