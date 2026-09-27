## Strengths and Weaknesses

The previous sections have developed the Stair Wear Model, applied it to a worn staircase, and probed its behavior under varying inputs. We now step back and assess the model as a whole. The purpose of this section is not to defend what we have built, but to state plainly what it does well and where its limitations lie, so that an archaeologist reading our results knows how much weight each conclusion is able to bear.

### Strengths

**Integration of contributing factors.** The model places mechanical wear, the regularity of human use, and the properties of the building material within a single framework, rather than treating them as separate corrections to one another. Wear on a step is therefore not attributed to any one cause in isolation; it accumulates as the joint consequence of how hard the material is, how many feet cross it, and where those feet land. This integration is what allows the model to represent wear as a process that builds up over a long history, and it is what makes the model usable for comparing staircases whose materials or usage histories differ.

**A statistical treatment of footfall.** Our treatment does not place each footstep at a single deterministic point. Instead, the placement of a foot is described by a normal distribution in the X direction and in the Y direction, and by a multivariate normal distribution when the two directions must be considered jointly. This choice reflects how people actually walk: it distinguishes single-file passage from two people climbing side by side, and it distinguishes an upward stream of traffic from a downward one, because each of these patterns leaves a different signature in the spread of the distribution rather than only in its center. The result is that the model can be asked questions about direction and about simultaneity of use, not merely about total volume of traffic.

**Non-destructive measurement.** Every quantity the model requires as input — the wear depth profile across a step, the initial hardness of the stone, and the other material properties we have called for — can be obtained without damaging the object under study. We consider this a requirement rather than a convenience. Archaeology is answerable for the preservation of the structures it studies, so a model whose inputs demanded a core sample or a cut surface would be unusable in practice no matter how accurate it was. The measurements we ask for are also inexpensive and within reach of a small team carrying minimal tools, which keeps the method available to the people who are most likely to need it.

### Weaknesses

**Reliance on simplifying assumptions.** The model assumes that the key factors governing wear remain broadly unchanged over the long timescales involved. Real use is rarely so steady. A stairwell may fall out of use for a generation and then be crowded again; a building may be renovated, reoccupied, or converted to a different purpose. Where such changes occurred, the model's reconstruction of the usage history is an average over the whole period rather than a sequence, and estimates derived from it will be correspondingly less certain. The model is at its strongest for staircases whose pattern of use was reasonably stable, and its conclusions should be read with more caution where the historical record suggests abrupt changes.

**Coarse treatment of environmental variation.** Environmental effects enter the model through a single rate constant $p$ that stands for the rate of corrosion and wear. This is a substantial simplification: a stairwell in a damp, unheated northern church and one in a dry, warm southern one are subject to different microclimates, and within a single structure the rate of wear will vary with the season and with the position of the stair. Reality would call for a rate that varies in time and with local conditions. By collapsing all of this into one number, the model gives up the ability to separate the influence of the environment from the influence of traffic. Any conclusion that depends on the absolute magnitude of wear — most notably the reliability of an age estimate, and the comparison of a stone's wear against the wear expected of a particular quarry — inherits this limitation, whereas conclusions that rest on the shape and distribution of wear are far less exposed to it.

Taken together, these strengths and weaknesses suggest a simple rule for the reader: the model is more trustworthy when it is used to compare, to rank, and to characterize a pattern of use, and less trustworthy when it is used to assign an absolute number to a staircase considered entirely on its own.

## Conclusion

In this paper we set out to give archaeologists a way of reading a set of worn stairs. To that end we developed the Stair Wear Model, which takes as its starting point the measured wear matrix of the steps under study and reasons outward from that measurement to the history that produced it. The model has two components. The Wear Volume Model (WVM) accounts for how much material has been lost, and expresses the relationships among the factors that cause that loss. The Wear Distribution Model (WDM) accounts for how the loss is distributed across the surface of a step, and it is this component that lets us ask how people once moved across the stairs. Alongside these two components we provided consistency and reliability metrics, tied respectively to the wear distribution and to the age of the staircase, so that a user can judge whether a proposed history is compatible with the wear that is actually present and how far the resulting age estimate can be trusted. We also set out methods for determining the source of the stone and for judging whether a staircase has been repaired or renovated. Simulation was used extensively throughout, both in constructing the model and in examining how it behaves. We have deliberately left numerical results to the sections above; our aim here is to state what has been delivered.

We close with a reflection that the problem itself invites. Wear on a staircase is unavoidable. Any surface that people cross often enough will yield to them, and the steps we study today are the accumulated record of that yielding. It is a record left unintentionally, by people who were not writing anything down, and for that reason it is one of the few sources of evidence about daily life in a structure that survives when the documents do not. Reading it accurately is difficult precisely because so many influences are folded into a single worn surface.

The most promising direction for further work is therefore the one our second weakness identifies: to bring finer environmental variables into the model, so that humidity, temperature, and their seasonal variation are represented in their own right rather than absorbed into a single rate. Doing so would reduce the influence of environmental factors on the analysis of the stone itself, and would make the age estimates and material attributions that depend on absolute wear considerably more dependable. We hope that the model presented here, and the measurements it asks for, will help archaeologists recover the information they are seeking from the stairs they study.

## 我的做法说明

**怎么做的。** 两节的骨架直接来自要点清单的 8 条：先写 `Strengths and Weaknesses`（优点三条、缺点两条，按清单 2–6 的顺序），再写 `Conclusion`（先逐项回收清单 7 的成果清单，再按清单 8 收束）。优点和缺点都写成"一句论断 + 展开"的段落，用小标题加粗领起，这样评委扫读时能立刻抓到论点。结论分三段：交付物清单、磨损作为"人留下的痕迹"的收束、以及环境变量这一条未来方向。写完通读一遍，确认没有引入任何方程、符号或数字。

**自己补的东西（清单里没有，我加进去的）。** 以下都请队友复核：

1. **两节之间的过渡句**——开头一段"这不是为模型辩护，而是说清楚每条结论能承受多大分量"，以及优缺点之后那句总结性判断（模型用于**比较、排序、刻画使用模式**时更可信，用于**给单个台阶一个绝对数字**时较弱）。
2. **"相对结论比绝对结论更稳"这一层**——清单只给缺点 2，没有说它影响什么。我把环境简化这条缺点**落到具体交付物上**（绝对年龄估计、石材来源比对），并指出磨损**分布形状**类的结论受影响小。这是我的推断，不是清单原话。
3. **把统计化踩踏和题面三问挂钩**——清单优点 2 只说了"正态/多维正态反映单列/并排、上行/下行"，我补了一句它使模型能被问及**方向**与**同时通行人数**（题面的两个小问）。
4. **无损测量一段补了"低成本、小队、少工具"和"考古对文物保护负有责任"的理由**——前三个词出自题面（我读了题面），后一句是我给这条优点补的动机。清单只说"契合考古对文物保护的关切"。
5. **仿真那句的补充**——清单只说"大量使用了仿真"，我写成"既用于构建模型，也用于考察模型行为"。这是为了让它像一句话而不像硬塞的名词，但属于我对清单的**轻度扩写**，若与正文不符请改回。

**没写进去的东西及原因。**

1. **章号/节号**——我没有采用 `7.` `8.` 这类编号，因为我没有读前面的章节，无法知道正文编到第几节；用无编号标题最安全，队友按正文补号即可。
2. **数值结果**——清单明确说结论段不报数字，我也没编任何数字、百分比、年份或精度。全文除正文已有的速率常数外无任何量。
3. **符号**——只出现清单点名的速率常数 $p$（写成过 `$p$`）。如果正文里这个常数的记号不是 $p$，改一个字符即可；我没有另造符号。
4. **与其它模型/文献的对比**——需要读前面章节和参考文献列表，超出我的阅读范围，写了就有编造风险，故略。
5. **未来方向的扩展**——清单只给了"引入更细致的环境变量"一条，我没有自己加第二、第三条（比如数据获取、跨学科验证），以免与正文脱节。
6. **图表与公式**——两节按"纯论文语言"处理，未放任何图表、公式或引用标注。
7. **致谢、参考文献、AI 使用披露**——不属于这两节，未写。
8. **语言与格式的判断**——用英文写，因为这是 MCM 投稿论文，题面与两节标题均为英文；markdown 的 H2/H3 与加粗小标题只是层级标记，转 LaTeX 时对应 `\section`/`\subsection`。

**阅读范围**：只读了 `case-A-problem.txt` 与 `brief-S2.md` 两个文件，未打开同目录任何其它文件（含 `README`、`true`、`out-` 打头的文件），也未读 `.claude/skills/` 或 `corpus/`。
