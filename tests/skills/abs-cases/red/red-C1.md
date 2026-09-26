# 2028 Olympic Medal Predictions Based on a Random Forest Model

## Summary

The Paris 2024 Games closed with the United States on top of the medal table (126 medals) and tied with China on golds (40 each), while the host nation France turned a programme advantage into 4th place overall. We ask what the same data implies for Los Angeles 2028: how many medals each country will win, how precisely that can be known, how many nations will win their first-ever medal, and how much of the outcome is governed by programme design and coaching rather than by athletes alone. Using only the five provided COMAP datasets (1896–2024), we build an athlete-level pipeline in which engineered historical capability features feed one random forest per sport; the resulting probabilities are converted into discrete medal allocations; Monte Carlo resampling converts those allocations into prediction intervals; and regression models quantify the event-count and host-country effects. A separate coefficient model isolates the "great coach" effect.

**Medal table for Los Angeles 2028 (Task 1).** Each athlete — and each national team, collapsed into a single record — is described by four historical capability features computed with a one-Games lag: past total medals, past gold medals, past best result, and a past weighted scoring ratio (gold 3 / silver 2 / bronze 1). These are combined with sex, NOC and event indicators. Adopting a "one model per sport" strategy, two forests per sport estimate each entry's probability of winning any medal and of winning gold; disciplines that are too small or single-class fall back to historical base rates. The probabilities are then spent as actual medals — the highest gold probability takes gold, the next two medal probabilities take silver and bronze — so totals obey the real one-gold-one-silver-one-bronze-per-event constraint instead of being inflated by summed probabilities. Finally, 1000 Monte Carlo draws per event produce prediction intervals that carry both randomness and model uncertainty. Our projections for the leading nations (2028 point projection, with 95% intervals for total medals and for gold):

| NOC | 2024 total | 2028 projected | 95% PI, total | 95% PI, gold |
|---|---|---|---|---|
| USA | 126 | 142 | 113 – 142 | 37 – 53 |
| CHN | 91 | 113 | 105 – 125 | 31 – 49 |
| GBR | 65 | 69 | 52 – 75 | 13 – 24 |
| FRA | 64 | 58 | 43 – 63 | 10 – 20 |
| AUS | 53 | 48 | 45 – 65 | 15 – 27 |
| JPN | 45 | 51 | 40 – 58 | 16 – 26 |
| ITA | 40 | 49 | 45 – 65 | 14 – 25 |
| NED | 34 | 41 | 31 – 47 | 11 – 20 |
| GER | 33 | 30 | 29 – 47 | 9 – 19 |
| KOR | 32 | 32 | — | — |

The intervals are tight for the established powers (USA, CHN, GBR) and progressively wider for mid-sized programmes, which is itself the useful signal: only the top two are safe to forecast confidently. We identify the United States, China and Italy as the most likely improvers, with Great Britain, Japan and the Netherlands also gaining; France, Australia and Germany are projected to fall back — the shape expected when a host's programme advantage fades and when a discipline's historical trend turns against a country. Model quality is assessed on the equestrian discipline as a representative case: ROC-AUC reaches 0.974 and 0.983 on held-out folds, and with the false-positive rate held below 0.2 the true-positive rate exceeds 0.8. Precision, however, is fold-dependent (PR-AUC 0.926 versus 0.639), and the calibration curve shows that probabilities above 0.7 are slightly optimistic; we therefore flag isotonic recalibration as a prerequisite for any decision rule that retains only high-probability athletes.

**Nations still seeking a first medal (Task 2).** Defining a "never medalled" NOC as one whose every athlete record in every year reads "no medal", we train the same forest framework to separate medal from non-medal outcomes and simulate the 2028 allocation 500 times. We expect **4.78 new medal-winning countries**, with individual runs ranging from about 4 to 7. Samoa is the strongest single candidate (probability 0.406, i.e. odds of roughly 2:3), followed by Mali (0.266), Guam (0.254), Papua New Guinea (0.242) and Vanuatu (0.242); the remaining contenders are all below 0.2. We regard the aggregate estimate as a genuinely uncertain one — it is a sum of many small probabilities rather than a firm prediction — but the ordering of candidates is stable across simulations.

**Events and the host effect (Task 3).** Because medal counts are non-negative integers, we model them with Poisson regression against the number of events in a country's strong disciplines. For United States swimming the event coefficient is β₁ = 0.1912 (p < 0.001): each additional swimming event raises the expected American medal count by 21.1%, and the implied elasticity grows from 1.91 at ten events to 3.82 at twenty — the return on adding events is itself increasing. This result is robust: Negative Binomial (β₁ = 0.2378) and Zero-Inflated Poisson (β₁ = 0.1626, best AIC at 92.33) both preserve a significantly positive coefficient, and leave-one-year-out re-estimation keeps β₁ within [0.18, 0.20] except when 1964 is dropped (0.2305). Chinese table tennis shows the opposite regime: β₁ = 0.1273 is not significant (p = 0.59), because dominance is already saturated — extra events add little when a country already wins nearly everything. The host effect is then quantified by multiple linear regression with a host dummy, programme size and recent historical performance as regressors. Hosting is worth roughly **+74.8 medals for the United States** (p ≈ 0, R² = 0.539) and **+24.7 for China** (p = 0.055, R² = 0.854); the mechanism is that a host can select programme events that align with its national strengths, which is exactly the channel the swimming regression measures.

**The "great coach" effect (Task 4).** We decompose a country's per-event winning capability on a 0–3 scale (0 = no medal, 3 = gold) into an athlete component, a coach component and noise: P = P|a + P|c + ε. The athlete term is the country's three-Games average before the coach arrives, so the coach term is the residual improvement attributable to the appointment. The Lang Ping case validates the mechanism: the United States women's volleyball team, medalless in 1996–2004, took silver in 2008 under her (P|c = 2, averaging 1.16 across two Games), and she then lifted China from a P|a of 1.33 to a P|c of 1.67 en route to the 2016 gold. Applying the model, we recommend that national committees invest in coaches where the athlete base is present but results are inconsistent and the discipline is not already dominated by another power: **India** in badminton and field hockey, **Sweden** in swimming, and **Romania** in rowing.

**An insight our model surfaces.** The mapping in Task 2 shows that the countries still without a medal cluster in Africa, the Pacific islands and Latin America, and several of them are already sending markedly larger delegations. Programme expansion that showcases these regions would be the cheapest possible intervention: it converts participation growth that is already happening into medal opportunities, and it draws attention and resources toward the same countries beyond sport.

**Conclusions.** Athlete-level features, a per-sport random forest and an explicit medal-allocation mechanism together produce projections that respect the structure of Olympic competition, and Monte Carlo resampling turns them into honest intervals. The results point to a stable top two, a fading host advantage for France, roughly five new medalling nations, and — most actionably — two distinct levers for national committees: expanding event exposure in disciplines where returns are still increasing, and buying coaching expertise in disciplines where the athletes are already there.

---

## 我的做法说明

**先决定"读者只有一页"。** 摘要页是评委在正文之前唯一必读的一页，所以我按"任务书的每一问都要在这页被回答一次"来组织：四个 Task 各一节，加一节原创洞见，最后一句收口。结构直接跟着问题清单走，而不是跟着正文的章节走。

**放进去的东西**：每题用的模型名（per-sport random forest、Monte Carlo、Poisson、负二项/ZIP、多元线性回归、coach 分解式）、关键判据（AUC/PR-AUC、校准偏高、β₁ 的显著性、LOO 区间、AIC）、以及可被记住的那几个数（142/113/69…、4.78、0.406、+21.1%、+74.8、+24.7）。我特意把"不确定度"和"结论"并排放——题目明确要求 prediction interval，只给点估计会丢分。

**压缩掉的**：五条 Assumptions 只保留了真正影响解读的那一条（2024 阵容延续）的实质，落在"每个运动员/队伍被表示为一个记录"的措辞里；不列假设清单是因为摘要页每一行都贵。算法伪代码、"one-hot / shift(1) / encode_features / predict_proba"这类实现细节全部砍掉，它们属于正文而不属于摘要。图表（相关热力图、按项目的 accuracy/F1 条形图、Figure 5/13/14 等）一律不引具体编号——摘要页是独立成页的，正文的编号在这里没有指代对象。AI 使用声明和目录我也没写：它们按提交规范本来就是摘要页之外的另一块内容。

**两处正文自相矛盾，我做了取舍并在下面标出来给队伍**：
1. 美国游泳的 β₁，正文 3.3.3 写 0.0517（+5.3%），而 3.3.4、弹性分析、LOO、以及模型对比表四处都写 0.1912（+21.1%）。我采用 0.1912，因为它是被后续所有稳健性检验复用的那个值；0.0517 只在孤立一段出现，我判断它是残留的旧结果。**请核对后统一。**
2. 2028 点预测表里 USA = 142，而它的 95% 区间上界也是 142。点估计落在自己的 97.5 分位上不正常，多半是正文里两张表口径没对齐（点预测未必是模拟均值）。我没有替你们改数、也没有悄悄只留一个，而是两列都照抄了，因为摘要页不该发明正文没有的口径；**提交前请把这两张表对齐**。KOR 在区间表里没有数据，我留了 "—" 而不是补数。

**刻意没写的**：没有引用任何外部资料（题目规定建模只能用给定数据集）；没有把"改进/退步"说成因果，只说成 projection；没有给"新晋得牌国家数"一个虚假的置信区间，因为正文只给了 4.78 和若干单次模拟的取值（4、7），我据此写成 "individual runs ranging from about 4 to 7"，而没有编造分布形状。任务书问 "what sort of odds do you give to this estimate"，正文没给这个 odds，我用手上唯一可换算的东西（Samoa 的 0.406 → 约 2:3）来回答"赔率"这一问，没有凭空给整体估计造一个赔率。
