# true-S1.md — S1「3.1 Wear Volume Model」的真实节文字（对照用 · 不给写手）

- 来源：`tests/skills/abs-cases/case-A-body.md`（MCM/ICM case A / 论文 2501909 正文；该文件已剥离摘要、Keywords、栏位块、AI 报告）
- 区间：**第 147–296 行**（`## 3.1` + `## Wear Volume Model`，含子小节 3.1.1 / 3.1.2 / 3.1.3 与其中全部方程）
- 性质：**获奖论文原文的逐字副本**（含其小节标题）。仅用于写手交稿后的**逐段对照**。
- ⚠️ **不要给写手看本文件。** 写手只应拿到 `brief-S1.md`。

===== BEGIN VERBATIM 以下为逐字原文 =====
## 3.1

## Wear Volume Model

3.1.1
Rasterize The Surface of The Step
In order to represent the actual physical steps by using a mathematical model for easy
computer processing, we rasterize the steps. As shown in Figure 3, we take the top view of a
step to obtain a rectangle with length X m and width Y m, which is discretized and divided into
m×n rasters.

*Figure 3: Rasterized diagram of the stair surface*

The COP[2] is deﬁned as the center of each grid.
x =
⌊p
Gs
⌋
,
y =
⌊q
Gs
⌋
(3.1)
p denotes the distance from this COP to the leftmost side of the step, q denotes the distance
from this COR to the bottom edge of the step, and Gs is the size of the grid. d(x,y) is deﬁned
as the amount of wear at grid COP(x,y). The archaeologist measures the wear volume of the


stone steps and then constructs the measure wear matrix Dmeasure(x,y).
3.1.2
Wear Volumn Model
Wear results from behavior over time for a material as hard as stone. The total number
of steps taken on the same spot determines the amount of wear on that spot. The length of
time determines the time scale of cumulative wear. The hardness and abrasion resistance of the
material directly affects the wear rate. In addition, different distributions of steps and applied
gravity in different areas can lead to uneven wear. In order to accurately obtain information
about the steps, we introduced a comprehensive Wear Volume Model, combining the wear
distribution model with the introduction of time, material, and number of footsteps:
d(x,y) = T ·Nd ·D(x,y)·G·km
(3.2)
d(x,y) represents the wear measured by the archaeologist, T denotes the age of the stair, Nd
indicates the average number of people who walked the stairs each day, which is also known
as usage frequency. D(x,y) is the wear distribution function, we discuss it in Section 3.2. G is
the average gravitational force experienced by walking people, and km is deﬁned as the wear
volume coefﬁcient (the amount of wear and tear per unit of N on the stone steps). Further, we
analyze the parameters km and G.
• Archard wear theory (km)
Archard wear theory is one of the classical wear models, proposed by J.F. Archard. The
theory is used to describe the wear behavior of solid surfaces. Each step exerts a certain
positive pressure on the step in the process, which can be directly applied to analyze
the wear suffered by the step surface. At the same time, although the relative motion
distance between the person and the step during walking is limited, the slight sliding
of each step will cause localized wear on the step surface. Therefore, Archard’s wear
theory is applicable to analyze the wear of steps caused by people walking. The theory
establishes the fundamental formula for the unit wear coefﬁcient of a solid km, which is
deﬁned as:
km = K · d
H
(3.3)
where K denotes the stone wear coefﬁcient, d represents the relative sliding distance of
the tread surface, and H indicates the material hardness of the stone.
Material hardness H is not static but varies with time, resulting from physical factors
(such as temperature changes and wind erosion) and chemical weathering (such as hy-
drolysis and oxidation). Hence, we use an exponential decay model to simulate the loss
of hardness caused by weathering of rocks:
H(t) = H0e−pt
(3.4)
H0 denotes the initial material hardness while p denotes the weathering rate constant.


Moreover, another form of relationship between hardness and age can be provided:
HT =
∫
t H(t)
(3.5)
Based on the site survey, an information review is needed to obtain K, H0 and p.
• Gravity Assessment Model (G)
The same step may be used by people of different ages and genders with different weight
characteristics. We categorize the population into six groups: male minors (mm), female
minors (fm), adult males (am), adult females (af), older men (om), older women (ow).
To make the results more precise, we use their weight expectation as W in the model,
which is calculated as follows:

## W = ∑

i
ui ·qi
(3.6)
where ui describes the average weight of each population, qi indicates the proportion of each
population to the total population.
If they do not have this information, based on the global weight data provided by the
World Health Organization (WHO)[6][7], we provide the reference data as shown in Table 2.

*Table 2: Global Average Weight and Population Proportion by Age and Gender Group*

Population Group
Average Weight (kg)
Proportion (%)
Male Minors (mm)
40
10
Female Minors (fm)
38
10
Adult Males (am)
75
30
Adult Females (af)
65
30
Older Men (om)
70
10
Older Women (ow)
60
10
The overall average weight of the population is W = 62.8kg. This average is typically
calculated as a weighted sum of the proportions qi and the average weights ui of each sub-
group. To obtain a more precise estimate, archaeologists or researchers can adjust the subgroup
proportions qi or their average weights ui to better reﬂect more localized or up-to-date demo-
graphic data.This can make the calculation results more accurate and increase the ﬂexibility of
the model.
This adjustment allows for a more accurate estimation of the gravitational force G. The
gravitational force is calculated using the following formula:
G = W ·g
(3.7)
where g = 9.81m/s2 [9]is the acceleration due to gravity.


Integrating Equation 3.2, we obtain the expression for the average wear davg as
davg =
1
Acef f
∫
Acef f
T ·Nd ·D(x,y)·G·kmdxdy
(3.8)
in this equation, Acef f denotes the area of the steps overlook.
3.1.3
Calculation of Age and Frequency of Stone Steps
According to the analysis above, When D,G, and km are determined, the age of stone step T
and frequency of use Nd can be solved for each other. The speciﬁc formulas are shown below:
T = Acef f ·davg
Nd ·G·km
(3.9)
Nd = Acef f ·davg
T ·G·km
(3.10)
At this point, the age of the stone step T and frequency of use Nd can be sought.
