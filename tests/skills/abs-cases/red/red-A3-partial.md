# Stair Wear: Traces of History

## Summary

Historical records can tell an archaeologist roughly when a staircase was built, but they rarely say how it was used, and they say nothing at all about the thousands of people who wore it down. We take the worn tread surface itself to be the primary record. We build a **Stair Wear Model** that converts one non-destructive survey of a staircase into quantitative statements about its age, the traffic it carried, and the behaviour of the people who carried it — and we specify exactly what must be measured to run it: a wear-depth matrix of the tread, the tread geometry, and the initial hardness of the material, all obtainable at low cost by a small team with minimal tools.

**The model.** We rasterize the tread into an $m\times n$ grid, record the wear depth $d(x,y)$ at the centre of every cell, and form the measurement matrix $D^{\text{measure}}$. Two coupled sub-models interpret it.

*Wear Volume Model (WVM).* Cumulative wear is the product of exposure time, traffic and load:

$$d(x,y) = T\cdot N_d\cdot D(x,y)\cdot G\cdot k_m,$$

where $T$ is the age, $N_d$ the average number of people per day, $D(x,y)$ the distribution of footfalls, $G$ the average load, and $k_m$ the material wear coefficient. $k_m$ comes from Archard's wear law, $k_m = K d / H$; because stone and wood soften as they weather, we let hardness decay as $H(t)=H_0e^{-pt}$ and use the hardness integrated over the life of the staircase. $G$ is built bottom-up from six age-and-sex population groups on WHO reference weights (global mean $W=62.8$ kg, re-weightable for a specific site), giving $G=Wg$. Solving the WVM for $T$ and $N_d$ shows that the observed wear is a one-parameter family: age and daily frequency determine each other.

*Wear Distribution Model (WDM).* Accumulated footfalls are the sum of very many weakly correlated steps, so by the central limit theorem the wear in each direction is a normal or mixture-of-normal distribution whose modes carry direct traffic meaning. In the walking ($y$) direction one mode means a favoured direction of travel and two modes mean two-way use, with the ratio of the component weights giving the up-to-down traffic ratio; the mode positions distinguish ascent from descent, because ascending feet land heel-first and nearer the lower edge of the tread. In the lateral ($x$) direction the number of modes is the number of lanes — how many people walked abreast. Assuming the two directions are independent, $D(x,y)=D_X\cdot D_Y$, and we fit the mixture components to the marginals of the measured matrix with a Gauss Mixture algorithm.

**Task 1: what the wear alone tells us.** We apply the model to a set of ancient Edinburgh sandstone steps (tread $2\ \text{m}\times0.4\ \text{m}$, $H=95\ \text{N/mm}^2$), reconstructed from 3D imaging.

- Lateral wear resolves into three normal components centred at $0.30$ m, $1.10$ m and $1.76$ m: three people typically walked **side by side**, which points to heavy traffic. The central component carries the largest weight and the smallest spread, so people preferred the middle of the stair.
- Longitudinal wear resolves into two components, so the staircase was used in **both directions**, with an up-to-down traffic ratio of about **3 : 2**. The component means ($0.08$ m for ascent, $0.15$ m for descent) both lie near the lower edge of the tread, and ascent lies closer than descent — exactly the asymmetry predicted by gait studies.
- Combining the distribution with the measured load and material parameters links age to frequency. The model returns $N_d\approx261$ people per day, equivalently a staircase built roughly a century ago (about $36\,500$ days) at about $260$ people per day.

**Task 2: the harder questions.** For the second group of questions we formulate decision rules rather than ad-hoc judgements.

- *Is the wear consistent with the available information?* We reconstruct the wear matrix $D^{\text{available}}$ implied by the assumed age, usage and daily pattern of life, and compare it with $D^{\text{measure}}$ through a log-ratio consistency index $P_A$; $|P_A|$ measures how far the two disagree.
- *Age and its reliability.* Ages are estimated step by step; steps whose age falls more than 5% below that of the oldest step are discarded as later work, and the remainder give the age of the stairwell, $T_{\text{set}}$. Reliability is not asserted but bounded: we report a two-sided confidence interval $CI$ computed from the counts of accepted and rejected estimates through an $F$-distribution at $\alpha=0.05$.
- *Repairs and renovations.* Two independent detectors. A step-age correlation $R_{SA}$ flags any step that falls below $0.95$ of the stairwell age; independently, a non-destructive hardness test reads a Brinell-scale hardness for each step out of the wear matrix, and wear fields are compared pairwise by a KL-style divergence with threshold $\varepsilon=0.05$. Together they identify which steps were replaced, and the elapsed time since repair is recovered from the age gap and from an exponential relation between divergence and elapsed time.
- *Provenance of the material.* Inverting the WVM gives the life-averaged hardness of the material actually present. Comparing it with tabulated hardnesses of candidate materials — metasequoia (18), poplar (24), sandstone (95) and marble (175 N/mm²) — accepts a proposed quarry of origin when the relative mismatch $\eta$ is below 5%. For wood we add a hardness-decay law that also carries relative humidity, and note that growth rings provide an independent age check.
- *Pattern of use on a typical day.* A Monte-Carlo study of a single day, resolved into 1000 time steps with the probability $P_0$ that one rather than two people begin a crossing, shows that short bursts of heavy use broaden and multi-modalize the lateral wear, while a few people over a long period concentrate it. Fitting the simulated daily population $Q$ against the resulting lateral standard deviation $\sigma$ by least squares gives a calibration curve from which the measured width of the tread wear can be read back as the number of people in a typical day.

> **[PENDING — the numerical results of Task 2 have not yet been produced.]** The rules above are formulated and implemented, but the paper does not yet report their values for the Edinburgh staircase: the consistency index, the reliability interval, the set of steps identified as repaired, the provenance verdict, and the points on the daily-population calibration curve. When those runs are complete, replace this note with one or two sentences of concrete outcome — e.g. "for the Edinburgh staircase the reconstructed and measured wear matrices agree to $|P_A|=\dots$, the age estimate is reliable to $\dots$, and the origin of the sandstone is confirmed to within $\eta=\dots$" — and re-read the Conclusion to make sure it still holds.

**Sensitivity and robustness.** Wear accumulation is strongly sensitive to the initial hardness $H_0$ across the material range above, which is what makes hardness a genuinely informative measurement rather than a nuisance parameter. The weathering rate $p$ is another matter: over timescales up to roughly four centuries the model is insensitive to it, but beyond that it is highly sensitive — doubling $p$ from $0.0025$ to $0.005$ shortens the time to saturation by $64.2\%$ — so for very old staircases $p$ must be treated as a first-class uncertain input. Across four modelled regions with different climates and traffic, century-scale wear differs by well under $0.01\%$, with Brazil highest because its humidity drives the fastest corrosion. The model is therefore robust in the regime where it is meant to be used, and honest about where it is not.

**Conclusion.** The Stair Wear Model starts from a single measured wear matrix and returns both a volume story (how much wear, hence how much use, over how long) and a distribution story (who walked where, in which direction, abreast or single file, steadily or in bursts), together with indicators of consistency, reliability, repair and provenance. Wear on a staircase is inevitable — and that is precisely why it is an archive. Our model reads it without touching it.

## 我的做法说明

**这份文件是什么。** 上面是摘要页（Summary Sheet）的内容，可直接排进提交 PDF 的第一页；`## 我的做法说明` 这一段不属于摘要页，排版时整段删掉。

**怎么处理"Task 2 还没有结果"。** 分三步：

1. **只写机制，不写数字。** Task 2 那五条，我把正文里已经成形的东西——判据、阈值、指标（$P_A$、$CI$、$R_{SA}$、$\varepsilon=0.05$、$\eta<5\%$、$Q$–$\sigma$ 标定曲线）——照实写出来，一个具体数值都不给。这些规则本身是论文的真实内容，写了不算编造；它们的**取值**才是没有的东西。
2. **留一个显式占位段。** 用 `[PENDING ...]` 起头，写明缺哪五项、以及填回时该怎么改写。我没有把它藏成一句含糊的"results will be reported"，因为含糊的写法最容易被漏掉、最后带着它提交出去。占位段必须是删得掉、看得见的。
3. **让"未完成"不污染已完成的部分。** Task 1 的结论、敏感性分析、结论段全部与 Task 2 解耦：即使 Task 2 那一节整段被替换，摘要的其余部分不需要重写。

**取舍。** 我选了"摘要写全 + 一处显式缺口"，而不是"干脆不写 Task 2"。理由是题目问的就是两批问题，摘要里对 Task 2 只字不提，会让摘要与正文（正文第 4 章已经写了很多）不一致，也会让评阅人以为我们漏答了一半。同时我也没有把 Task 2 写成"我们已经解决"——那是最省事也最危险的一种写法。

**没写进去的东西，以及原因。**

- **Task 2 的任何数值**：$CI$ 区间、$|P_A|$、哪几级台阶被判定修复及 $T_{re}$、$\eta$ 的判定结果、$Q$–$\sigma$ 的拟合系数。正文里没有，我不替它生成。
- **4.4 / 4.5 的模拟结论**。这两个小节正文里只有图题占位（Figure 9–11、Table 8），没有数据；我把它们当作**方法**写进摘要，没有把"四种材料模拟出不同磨损""标定曲线成立"当结果来宣布。
- **"来源已确认 / 修复已定位 / 信息自洽"这类结论性措辞**。这些正是 Task 2 要回答的问题本身，在结果出来之前任何一个都是编的。
- **摘要里没有引用文献编号、没有表格、没有公式推导**，也没有写目录页或 AI disclosure 段落——摘要页是独立的一页，这些属于正文部件。
- **我没有改正文一个字，也没有翻 `build/abs-red/` 下你点名之外的文件、没有读 `corpus/` 或 `.claude/skills/`。**

**两处留给你裁定的隐患**（我没有在摘要里替你们选边，摘要用的是不依赖它们的表述）：

1. 正文 Table 4 取 $G=700$ N，但按正文自己的 Table 2 算出 $W=62.8$ kg，$Wg\approx616$ N。摘要里我写的是"由六个年龄性别组自下而上构造 $G$"，没有复述 700 N 这个数。
2. 正文说"constructed in a century ago"，与 36492 天（≈100 年）自洽，但与 $N_d\approx261$ 是同一组解的两端。摘要里我按"约一个世纪 / 约 260 人每天"表述，回避了具体到年的说法。

**待办只有一件**：Task 2 跑完后，把 `[PENDING ...]` 那一段换成实测数字，并复核结论段。
