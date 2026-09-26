Summary
Even the hardest stone steps can wear down over time under the repeated footsteps of peo-
ple. Stairs record history in the unique way. To assist archaeologists in extracting more infor-
mation from a set of worn stairs, we analyze measurable data and establish relevant models.
For task1:To analyze stair basic information, we established the Stair Wear Model, which
is consisting of the Wear Volume Model (WVM) and the Wear Distribution Model (WDM). We
rasterize the top view of the steps and combine it with wear data to create a wear measurement
matrix. Based on this matrix and Archard Wear Law, we develop the WVM. We introducing
and analyze parameters such as the wear coefﬁcient, average human weight, material hardness,
and stair area to calculate the stair’s age and usage frequency. Additionally, we established the
WDM based on the Central Limit Theorem. It calculate the marginal distribution of the wear
measurement matrix and ﬁt the wear distribution in the X and Y directions with a Gaussian
Mixture Algorithm. In the Y-direction, the number and location of normal distribution indicate
walking direction, while the X-direction distribution reﬂects the parallelism of movement.
We provided archaeologists with measurements and queries (Table 3) and detailed usage
instructions (Figure 7). All the methods we propose follow the non-destruction principle. As an
example, a set of ancient sandstone steps in Edinburgh is analyzed. The results demonstrate the
steps were built about a century ago, typically used by three people walking side by side. Both
directions were used, with an upward-to-downward ratio of 3:2 and a daily usage frequency of
261. More detailed results are presented in Table 5, Table 6 and Figure 8.
For Task 2: We address further problems with the Stair Wear Model and information avail-
able. To assess wear distribution consistency, we deﬁne a consistency parameter between wear
matrices. The stairwell age is calculated from step age, with a reliability parameter to evaluate
accuracy. To determine if the staircase was repaired, besides the step age method we introduce
an innovative non-destructive approach based on the Brinell Scale and KL divergence for a
more comprehensive consistency analysis.
Based on the consistency of material hardness, we developed a method to trace material
origins. Simulations with the Stair Wear Model help evaluate material wear consistency. Monte
Carlo Method reveals the relationship between the standard deviation of X-direction wear
and daily stair usage. Applying these methods to the studied steps yielded an age prediction
reliability above 95%. Both methods conﬁrms no repairs in this stair, and materials matches
archival records. The dispersed X-direction wear indicates heavy use over short periods.
Material hardness demonstrates a high sensitivity in our model. The model shows low
sensitivity to weathering rate constant within 4 century but higher sensitivity over a 20-century
scale, indicating its strong performance within a certain time frame. Robustness tests across
regions further support this. We hope our work can help the archaeologists. The hard stones
have their method to record the history, and we have the model to read them.
Keywords: Stair Wear, Archard Law, Central Limit Theorem, Gaussian Mixture Algorithm
