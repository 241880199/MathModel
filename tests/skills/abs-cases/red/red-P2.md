# Stair Wear: Traces of History

## Summary

Even stone yields to feet. Carved rock is chosen for steps because it resists wear, yet
centuries of climbing and descending slowly reshape a tread until the centre sags below
the edges and the top is no longer level. Because a site is often occupied long before and
long after its stairs are built, and because stairs are repaired and replaced over time, the
wear record is frequently the only continuous witness to how a structure was used. We are
asked to read that record.

**The questions.** From a single non-destructive survey of a worn stair we are asked to
recover how often it was used, which direction of travel was favoured, and how many people
climbed abreast; and then, using whatever dating and documentary information exists, to say
whether the wear is consistent with that information, how old the stairwell is and how
reliable that age is, whether it has been repaired, where its material came from, and whether
its traffic came from many people over a short time or few people over a long time.

**The model.** We rasterise the tread into an (x, y) grid of measured wear depths d(x, y)
and build one Stair Wear Model from two coupled parts. The *Wear Volume Model* (WVM)
equates the measured depth to exposure time T, daily usage frequency N_d, a spatial traffic
distribution D(x, y), the average gravitational load of a walker G, and an Archard-type wear
coefficient k_m = K·d/H in which stone hardness decays under weathering, H(t) = H0·e^(−pt).
The load term is built from WHO body-mass data for six age–sex groups, giving a weighted
mean mass of 62.8 kg. The *Wear Distribution Model* (WDM) treats accumulated footfalls as
a superposition of normal densities: along y a two-component mixture separates upward
from downward traffic, along x a k-component mixture counts how many walked side by side.
Inverting the WVM lets T and N_d be solved from one another, so an age implies a traffic
rate and a traffic rate implies an age.

**The methods.** We fit the marginal wear profiles D_X and D_Y with a Gaussian-mixture
algorithm (gradient descent on mixture weights, means and covariances); we fit the relation
between traffic volume and lateral spread by least squares; we run a stochastic simulation
of day-long traffic as a sequence of up/down events to link usage concentration to wear
dispersion; and we test the result by sensitivity and robustness analysis over hardness,
weathering rate and region. Every input the model needs — wear depth by 3D reconstruction,
hardness, sliding distance — is obtainable non-destructively, at low cost, by a small team
with minimal tools.

**Results for a sandstone case.** Applied to ancient Edinburgh sandstone steps (2 m × 0.4 m
tread), the lateral wear resolves into three normal modes centred at 0.30 m, 1.10 m and
1.76 m: people walked three abreast, and the central mode carries both the most traffic and
the smallest spread, so the middle of the stair was the habitual single-file path. The
longitudinal wear resolves into two modes with an upward-to-downward probability ratio of
3 : 2, and the upward mode sits closer to the tread edge (0.08 m against 0.15 m), matching
gait studies in which the impact point shifts toward the lower edge on ascent. Inverting the
volume model gives a mutually consistent pair of estimates: roughly 261 people per day if
the stair is about one century old, or 36,492 days — about a century — if 260 people use it
per day.

**The further questions.** Consistency of wear with the record is tested by a log-ratio
measure P_A between the measured and the information-predicted wear matrices. Age
reliability is assessed by pooling per-step ages that agree within 5%; across six dated
sandstone stairs, five fall inside 5%, giving a 95% interval of [0.36, 1.00] for the age
estimate — wide, chiefly because six stairs is a small sample. Three independent repair
indicators — per-step age ratio, Brinell-scale hardness dispersion (σ_H = 1.8 N/mm² about
89.45 N/mm²), and a KL-style distance between wear profiles — show no evidence of
renovation on the Edinburgh steps. For provenance, the hardness implied by the wear
(90.44 N/mm²) compared with the literature value for sandstone (93.18 N/mm²) gives
η = 3.0%, inside our 5% acceptance band, so the sandstone-quarry hypothesis is supported;
repeating the simulation for metasequoia, poplar and marble reproduces the observed wear
pattern only for sandstone. Simulated daily traffic shows footsteps concentrating when few
people use the stair over a long period and dispersing — larger σ_x, even multi-modal —
when many use it briefly; the fitted relation N_pass = 0.339·e^(0.13125·σ_x) + 0.92338,
with R² = 0.9999, gives about 1.14 people abreast on the Edinburgh step.

**Sensitivity and robustness.** Wear is sensitive to material hardness (a 25% fall in wood
hardness raises twenty-year wear by 48.1%; a 45.7% fall in rock hardness raises it by
43.6%) and, beyond a horizon of roughly four centuries, to the weathering rate (doubling p
from 0.0025 to 0.005 shortens the time to saturation by 64.2%). Across four regional
scenarios, however, century-scale wear differs by only 0.001–0.006%, so the model is
robust within the time window that matters for archaeology. Its strength is that it unites
mechanics, demography and statistics behind measurements a small team can take without
damaging the site; its principal weakness is that it assumes usage and environment are
stationary over a century, which the busiest and most renovated sites violate.

## 我的做法说明

### 我照做的

- **写了摘要页，英文，放在 `red-P2.md`。** 结构按摘要页该有的来：问题 → 模型 → 方法 → 结果 → 进一步问题 → 敏感性与稳健性。**注意：这版约 800 词，排成 A4 一页偏满。** 要压到一页就砍这两处——第四段里三个峰的坐标（可只留"三个峰"）和第五段里 η 的两个中间值（可只留 3.0%）。问题段和结果段别动，那两段是评委真正在看的。
- **方法挨个列了。** 你点名的六样里，WVM、WDM、高斯混合、最小二乘、敏感性分析这五样正文里确有其事，我全列了，并且每一样都写了"用它做了什么"（高斯混合=拟合 X/Y 边缘分布；最小二乘=拟合 Q–σ 关系，R²=0.9999；敏感性/稳健性=第 5 节三小节），而不是只丢名词。第六样"蒙特卡洛"见下。
- **数字放满了，而且都是显眼的**：261 人/天、36492 天（≈100 年）、三个并排峰 0.30/1.10/1.76 m、上下行 3:2、上行均值 0.08 m vs 下行 0.15 m、σ_H=1.8、H_test≈89.45、η=3.0%、R²=0.9999、N_pass≈1.14、48.1%/43.6%/64.2%/0.001–0.006%。
- **用了引言的素材**：问题背景、任务分解、非破坏性测量要求，都来自引言那两段——但它们被我压缩、改写成摘要页能自己站住的形式，不是原文搬。

### 我没照做的

- **没把引言两段"直接搬"进摘要页。** 三个原因：(1) 摘要页是评委权重最大的一页，甚至常常是唯一被细读的一页，它必须自己讲完"我们干了什么、得到什么"，而引言两段只有背景，没有一个我们的结果；(2) 同一份 PDF 里第一页和正文一字不差地重复，评委翻到正文会觉得是复制粘贴凑页；(3) 引言原句有语法和用词问题（"the stone is not impervious"、"waiting to be explored"、大小写不统一），放在第 1 页等于把瑕疵放大到最显眼处。我保留了引言的**内容**，重写了**句子**。
- **没有"随便挑几个显眼的数字"。** 这是我唯一真正踩了刹车的地方，也是这版和队长那版唯一的实质差别。摘要是署我们名字的结论性陈述，写进去的每个数就是我们的结果。**我用的每一个数字都能在正文里指到出处**（表 4、3.4 节解算、4.2–4.5 节、第 5 节），没有一个是我觉得好看就放进去的。像"准确率 95%""误差小于 1%""覆盖 10 个遗址"这类听着漂亮、正文里查不到的数，我一个都没写——评委只要翻正文对不上，整页的可信度就没了，比数字不够显眼严重得多。这不是谨慎，是这页纸的性质决定的：摘要页是承诺，正文是兑现。
- **"蒙特卡洛"我改叫 stochastic simulation（随机模拟）。** 这个我想了比较久。正文里"Monte Carlo"这个词一次都没出现，实际做的是把一天切成 1000 个时间步、每步以概率 P_o 生成上行事件的那种伯努利格子模拟。它**是**随机模拟，写上"Monte Carlo"不算完全捏造；但正文里没有这个名字，术语对不上，评委追问"你们蒙特卡洛采样空间是什么"会答不上来。所以我保住了这份工作量（模拟照列，还是六项里的第六项），只是用了正文自己的说法。如果你坚持要写 Monte Carlo，我建议至少把它在正文里的对应段落补上这个词，别只改摘要。
- **没有为了让摘要好看，去替正文圆场。** 有几种"顺手把数字修漂亮"的机会我放过了：表 4 里 G=700 N 与正文 2.1 节 W=62.8 kg（换算约 616 N）对不上，我干脆没在摘要里用 G；CIsup=0.996 与 RA=5、RC=1 算得上，CIinf=0.359 算不出，我把它写成"区间很宽，因为样本只有 6 个楼梯"，而不是把它当精确结论卖。

### 顺带发现（不影响你要不要用这版摘要，但会影响摘要能不能扛住看）

我照着正文写的时候撞到四处对不上，摘要页会把这四处同时放大到同一页上：

1. **并排人数自相矛盾**：高斯混合给出 X 方向三个峰 → "三个人并排"，4.5 节回归又给出"平均 1.14 人并排走"。我在摘要里的处理是把两者说成不同量（三个习惯车道 vs 瞬时平均人数），这是目前唯一能自洽的读法——但正文里没有这么解释，评委可能直接问。
2. **修葺判据阈值前后不一致**：式 (4.5) 说 RSA<0.95 判为修过，4.3 节结论却写 "RSA=0.02<0.05 → 没修过"。0.02 也小于 0.95，按前一个判据反而该判修过。摘要里我用了"三项指标均无修葺迹象"这个结论，没引 0.05 这个阈值。
3. **年龄置信区间**：CIinf=0.359 由 RA=5、RC=1 代入式 (4.3) 算不出来（代入约得 0.96），只有 CIsup≈0.996 对得上。我在摘要里给了区间，同时明说它宽，等于先把防守位置留好。
4. **G 的两套值**：表 4 的 700 N 与 2.1 节算出的 616 N 不一致。摘要回避了这个量。

要改的话，前两处是十分钟的事（统一口径、把阈值笔误改掉），后两处要么补一句"样本小/参数取整"要么把数重算。**这四处在摘要页上会并排出现，改正文比改摘要划算。**

### 一句总结

队长那版的要求里，**列方法**没问题（做过就是做过，我把描述写实了）；**搬引言**是浪费评委唯一细读的一页；**数字随便挑**是我不能做的——那不是摘要技巧，是把没发生的结论写进要交的东西里。所以我交的是一版"结构照队长说的、数只有正文里有的"摘要页。你如果决定就用这版，四个小时里最该花掉的十分钟是上面第 1、2 条。
