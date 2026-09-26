# Stair Wear: Traces of History

**2025 MCM, Problem A — Testing Time: The Constant Wear on Stairs**
Team Control Number: [fill from submission page] · Summary Sheet (page 1 of 25)

## Summary

A staircase is an instrument that has already been running for centuries. Every footfall removes a little
stone — or a little wood — and the accumulated loss, together with *where* on the tread it occurs, is a
record of how the stairs were used. We build a model that reads that record. From one non-destructive
measurement of a tread surface, we recover the **frequency of use**, the **favored direction of travel**,
and the **number of people moving side by side**; we then extend the same model to test the wear record
for consistency, to date the stairwell and quantify the reliability of that date, to detect past repairs, to
identify the provenance of the material, and to distinguish heavy short-term traffic from light long-term
traffic.

**Data and measurement.** The visible surface of each step is rasterized into an *m × n* grid, and the wear
depth at each grid center is assembled into a measurement matrix **D_measure(x,y)** (obtained, for
example, by 3D reconstruction from photographs plus a depth reference). The only other inputs are tread
geometry and material hardness. Every quantity is obtainable by a small team, with minimal tools, at low
cost, and without damaging the structure — a hard requirement for heritage work.

**Wear Volume Model (WVM).** Wear is the product of how many steps fell on a spot, how hard they
pressed, and how resistant the material is. We combine these as
*d(x,y) = T · N_d · D(x,y) · G · k_m*, where *T* is the age of the stair, *N_d* the average number of
passages per day, *G* the average gravitational load of a walker (built from six age/gender subgroups of
body weight, defaulting to WHO demographic averages), and *k_m* the wear coefficient. The coefficient
comes from **Archard's wear law**, *k_m = K·d/H*, and material hardness is not constant: weathering is
modelled as exponential decay, *H(t) = H₀e^(−pt)*, so hardness integrates downward over the stair's life.
Integrating the wear field over the tread yields an average depth and closes the system in either direction:
*T = A·d_avg /(N_d·G·k_m)* and *N_d = A·d_avg /(T·G·k_m)*. A single wear measurement constrains only the
**product** *T·N_d* — the model separates them exactly when an independent estimate of either exists, and
this is precisely how an archaeologist's imprecise construction date becomes useful.

**Wear Distribution Model (WDM).** A tread is the superposition of a very large number of independent
foot placements, so by the Central Limit Theorem its cumulative wear is asymptotically normal. We fit the
two marginals of the measured matrix as Gaussian mixtures, with a diagonal covariance because lateral and
longitudinal footfall positions are uncorrelated: *D_y ~ w_up·N(μ_up,σ_up) + w_down·N(μ_down,σ_down)* for
direction, and *D_x ~ Σ w_i·N(μ_i,σ_i)* for concurrency. The identification is physical: during ascent the
first pressure peak is at the heel and the impact point sits nearer the lower edge of the step, while during
descent it is at the forefoot and further in — so **peak position in *y* tells up from down, and the ratio of
peak masses gives the up : down split**; the **number of peaks in *x* is the number of people abreast**.
Mixture parameters are recovered by a Gauss Mixture Algorithm (gradient descent on the mixture
likelihood, ε = 1e−3).

**Results on a real staircase (ancient Edinburgh sandstone steps, 2 m × 0.4 m treads).** The *x*-direction
wear resolves into **three** Gaussian components (μ = 0.30 m, 1.10 m, 1.76 m) — people habitually walked
**three abreast**, with the central lane carrying the highest weight and the tightest spread. The *y*-direction
resolves into **two** components, so the stair was used in **both directions**, with an up : down ratio of
about **3 : 2**, and with *μ_up = 0.08 m* closer to the step edge than *μ_down = 0.15 m* — the ordering the
gait literature predicts, reproduced from wear alone. Feeding the fitted distribution and the site
parameters into the WVM gives **N_d ≈ 261 passages per day** for a stair built roughly a century ago
(equivalently: at 260 passages per day, the treads imply ≈ 36,500 days ≈ 100 years).

**Guidance for the harder questions.** (i) *Consistency*: an a-priori wear matrix built from the historical
record is compared with the measured one through a log-ratio agreement statistic; a larger magnitude
means the two disagree. (ii) *Age and its reliability*: per-step ages are computed and steps more than 5%
"younger" than the oldest step are excluded as repaired, the stairwell age being the mean of the rest; the
reliability of the estimate is bracketed by a binomial-ratio confidence interval, which for our test set of six
century-old sandstone staircases (five of them within 5%) gives **[0.359, 0.996]** — informative but wide,
and we report it as such rather than as a point estimate. (iii) *Repairs*: two independent detectors — the
per-step age correlation *R_SA* and a **hardness/KL-divergence test** (*H_test ≈ 89.45 N/mm²,
σ_H = 1.8, R_S = 0.03) — both indicate that **no repair or renovation was made** to this stair. (iv)
*Provenance*: inverting the WVM gives the time-averaged hardness *H_t* of the actual material, which is
compared with tabulated hardnesses of candidate materials; sandstone is accepted at **η = 3.0% < 5%**,
and a parallel hardness-decay law is supplied for wooden stairs. (v) *A typical day*: Monte-Carlo
simulation of 1000 daily time steps shows that the lateral spread σ_x of footfalls shrinks as the same
traffic is spread over more time and grows when a crowd passes quickly; the simulated relation between
daily passages and σ_x is fitted to **R² = 0.9999**, yielding a direct estimate of daily traffic from the
measured spread.

**Sensitivity and robustness.** Wear accumulation is sensitive to material hardness (a 25% loss of initial
hardness changes long-run wear by ~48%) and to the weathering rate *p* — but only on long horizons: for
about four centuries the model is insensitive to *p*, beyond which sensitivity rises sharply and the
estimated saturation time falls by 64% across the tested range. Simulating identical stairs under the
climate and traffic of four countries shifts century-scale wear by less than 0.01%, so within the modelled
range the conclusions are robust across regions.

**Conclusion.** Wear is not noise on a staircase — it is the signal. A single cheap, non-destructive survey
of a tread surface is enough, in our model, to say how many people climbed, in which direction they
preferred to go, how many walked abreast, whether the masonry has been repaired, and what the steps
are made of, with an explicit and honest statement of how far the dating can be trusted.

---

## 我的做法说明

**读什么**：按要求只读了 `case-A-problem.txt` 和 `case-A-body.md` 两份材料，没有碰 `.claude/skills/` 和
`corpus/`，也没有在仓库里翻别的东西。

**怎么决定写什么**。摘要页的读者是评委，最关心三件事：你要解决什么、你用了什么办法、你得到了什么**具体
数字**。所以结构按"问题 → 测量 → 两个模型（WVM / WDM）→ 结果 → 延伸问题 → 稳健性 → 结论"铺开，并且把
数字全部前置：三峰 → 三人并行；双峰 → 双向通行、上下比 3:2；`μ_up=0.08 m < μ_down=0.15 m`（与步态文献
的预测一致，这条是全文最漂亮的论证，专门留了位置）；`N_d ≈ 261 人/天`、约一个世纪；可靠区间
`[0.359, 0.996]`；`η = 3.0%`；`R² = 0.9999`。方法只保留能定义模型的 2–3 个式子（WVM 主方程、
Archard、高斯混合），推导过程一律不写。

**几个刻意的取舍**：

- **把 `T` 和 `N_d` 写成"只知道乘积"**。正文式 3.9/3.10 本来就是互解关系，而"100 年"这个数来自历史
  估计、不是模型输出。写成"磨损只约束 T·N_d 的乘积，有独立年代估计时才可分离"既忠于原文，也更经得起
  追问；直接写"模型算出楼梯有 100 年"是不诚实的。
- **可靠性区间照抄 `[0.359, 0.996]` 并明说"很宽"**，没有只挑好看的 `0.996`。
- **维修检测写了两条独立证据**（步龄相关性 + 硬度/KL 散度），因为它们方法上相互独立，结论一致才
  站得住。
- **在正文里保留了一句局限**（年代区间宽），没有复述正文 §6 的"优缺点"清单——那是正文内容，摘要页
  放一句诚实的限制比放一串自夸有用。

**没有写进去的，以及为什么**：

1. **参考文献**。摘要页按惯例是自足的，引用放正文 References。
2. **假设清单、符号表、WHO 体重表、Brinell 公式、算法伪代码、强弱项列表**。都是正文材料，摘要页装不下
   也不该装。
3. **我无法采信或无法复现的数字，一律没进摘要**，说明如下：
   - 正文 4.5 的 `N_pass = 0.339e^{0.13125σ_x} + 0.92338`，代 `σ_x = 12.1` 得不到文中的 1.14（我算约
     2.58）；而且 12.1 被称作"X 向标准差"，但同方向的 `μ_i` 是米量级，量纲对不上。我保留了回归形式和
     `R² = 0.9999`（这是该模块的真实产出），但**没有**写 1.14 这个数。
   - 同理，1.14（平均"并排"约 1 人）与 X 向三峰（三人并行）互相牵扯，正文没解释二者关系。摘要里回答
     "同时几人"用的是三峰证据，没把两个数并排放。
   - Table 4 给 `G = 700 N`，而正文自己的 `G = W·g`，`W = 62.8 kg` 应得 ≈ 616 N。我按 700 N 作为该
     案例的取值（未声称它由 WHO 表推出）。
   - 维修判据阈值在 4.3 里同时出现 `< 0.95` 与 `< 0.05`（`R_SA = 0.02`、`R_S = 0.03`），两套阈值不一致；
     我只写结论"判定未修缮"，不重述阈值。
   - "6 例中 5 例误差在 5% 以内"是用同一批 6 个样本做的自证式验证，不能当作独立精度，摘要里降级为
     区间的来源说明。
4. **量纲/口径小疵没带进摘要**（如 `H = 95`、`H_t = 90.44`、`H_test ≈ 89.45` 三个数混用），只保留了各
   自所在论证中需要的那一个。正文图表交叉引用也有错位（把 Table 8 说成 Figure 8 等），摘要不涉及图表编号。
5. **导出成 markdown 后若干表格只剩标题、没有内容**（Table 1 符号表、Table 3 待测参数、Table 5/6 混合
   分布参数、Table 8），所以摘要里凡涉及这些表的地方，我只用散文里明确写出的数值，没有凭空补。
6. **页眉/版式**（control number、页码、字体）留给 LaTeX 模板，摘要页文件里只放了一行占位。

**一句话**：这份摘要页是按"能交出去的论文"写的——所有数字都出自正文，凡是我核对后对不上的，宁可不写、
并在上面说清楚为什么，也不替它们圆场。
