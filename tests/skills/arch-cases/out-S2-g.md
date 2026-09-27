## Strength and Weakness

### Strengths

Wear on a tread accumulates from several processes that interact, and the model holds three of them within a single framework: the mechanical abrasion produced by each footfall, the regularity with which the stairwell was used, and the properties of the material from which the treads were formed. Holding these factors within the same framework gives an integrated account of how wear accumulates over the life of a staircase, and it allows the effect of a change in one of them to be traced while the others are held fixed.

The position of a foot on a tread is not treated as fixed. Each footfall is a random event whose position on the tread is described by a normal distribution, and by a joint normal distribution when the two directions of the tread are considered together. The resulting wear pattern therefore reflects how people actually moved on the stairs: in single file or side by side, and ascending or descending.

The quantities the model requires as input can all be obtained without damaging the structure. The depth of wear measured across a tread and the hardness of the material from which it was formed are both measured on the staircase itself, so the investigation leaves the fabric of the building intact, as archaeological work on a standing structure requires.

### Weaknesses

The model rests on simplifying assumptions about the constancy of the factors it carries. It assumes that the conditions governing wear remained broadly the same throughout the period during which the staircase was in use, and real use may fluctuate far more than this. A building that stood empty for a long time, or whose traffic changed when a doorway was blocked or an upper floor added, will have left a wear record that is the sum of several regimes of use, and the model reports that record as one.

The model treats environmental variation in a coarse way, through a single rate constant, $p$, that stands for the rate of corrosion and wear under any conditions of humidity and temperature. Those conditions differ between one part of a stairwell and another and change with the seasons. Rates of that kind vary with time, and their variation is not represented here, so the effect of a damp climate cannot be separated from the effect of heavy use on the stairs.

## Conclusion

The Stair Wear Model was developed to help archaeologists draw inferences about the past from a set of worn stairs [1]. It takes as its starting point the measured wear matrix of the staircase under study and consists of two coupled components. The Wear Volume Model (WVM) accounts for the amount of material lost from the treads and states the relations among the factors that cause that loss. The Wear Distribution Model (WDM) accounts for the distribution of the wear over the tread and uses it to investigate how people moved on the stairs, including the direction in which they travelled and whether they passed in single file or side by side. Together the two components speak to the questions about use that the problem statement poses [1].

The model also provides the auxiliary judgements that an archaeological interpretation requires. Indices of consistency and of reliability were defined for the wear distribution and for the estimated age of the staircase, so that the wear observed on a set of stairs can be tested against the history that the surviving records suggest. Methods were given for inferring the source of the stone from the wear that the treads have suffered, and for recognising where repairs and renovations have been carried out. Simulation was used extensively in this work, both to generate wear patterns under conditions that are specified in advance and to examine how the quantities the model infers respond when those conditions are changed.

Wear is an inevitable consequence of use, and the worn surface of a staircase is a record left by the people who passed over it. Much of the difficulty in reading that record arises from the environment, and a direction for future work is to introduce environmental variables at a finer scale, so that the influence of climate on the stone can be separated with more confidence from the influence of the people who walked on it. We hope that the model will help archaeologists to obtain the information they seek from a set of worn stairs.

## 我的做法说明

### 怎么做的这两节
先读题面（确认"This is Problem A: 台阶磨损"、三个 use 类问题、以及"非破坏性/低成本/小队伍"的约束），再读 brief-S2.md 的 8 条要点，最后通读 `docs/mcm-writing-discipline.md` 后再下笔。brief 只给要点不给成句，所以段落划分、语序、过渡与全部措辞由我决定：把 2/3/4 条合成 `Strengths` 三段（整合框架 / 踩踏的统计处理 / 无损测量），把 5/6 条合成 `Weaknesses` 两段（恒常性假设 / 环境速率被压成一个常数），第 7 条拆成 `Conclusion` 的前两段（部件与交付物清单 / 辅助判据与仿真），第 8 条收成第三段（痕迹 → 环境变量细化 → 期望）。用无编号的两级标题，正文一律为完整句散文，不用条目式短句。

### 纪律逐条的落地
**A1（缺数据不许反推、不许挂外署名）**：两节通篇**零数值**，没有任何数字可以是编造或反推的；全篇没有出现任何机构名、没有 `reference` 式表题（本文没有表）。brief 只保证"磨损深度、石材初始硬度等可无损取得"，我就只写到"不必从实物上取下材料"，**没有**替它加上"成本低""小队伍、少工具"这类题面里存在但 brief 未背书的合规声明。
**A2（每个数字追到来源）**：同上，零数值 ⇒ 无不可追溯项。`p` 是既有符号，不是新数字。
**A3（不许声称读过、验证过未读部分）**：我**没有**读前面各章（任务书也明确说我没读过）。因此这两节里**没有一处**"as shown in Section 4.3""the results in Chapter 5 confirm"之类的指认，也**没有**任何对前文具体结论、具体数值、具体图表的断言。两节被写成自足的文本：只用 brief 明确交底的东西（部件名、`p`、无损、仿真、一致性/可靠性指标、来源与修缮判据）。同样的原因，**两节标题不带章号**——我不知道前面的编号规则，编号是会写错前文的东西。
**A4（正文不留制作注记）**：正文里没有"待补""占位""此处待定"一类痕迹；需要队伍自己补的东西（见下）全部写在**这一段**里，不进正文。
**A5（同一处不许自相矛盾）**：优点的第 1 条说"把三因素放进同一框架"，缺点第 1、2 条说的恰是其中两个因素被简化——这两处不冲突：一个讲耦合关系被建立，一个讲耦合中的环境项被压成一个常数；措辞上我刻意让"整合"只落在框架层面，不落到"环境被精确刻画"。
**B1（引用义务：正文 + 参考文献）**：正文给了 `[1]`（两处，都指向题面本身）。**这是我唯一敢引的来源**——它是我实际读过的文件，其余可引之处我一概不知道你们参考文献表里有什么。请把这一条加进 References：`[1] COMAP. 2025 MCM Problem A: Testing Time: The Constant Wear On Stairs. Mathematical Contest in Modeling, 2025.` 若要改编号或换成你们表里已有的题面条目，改编号即可，正文两处 `[1]` 随之改。
**B2（语域与人称）**：第一人称只用 `we`（"We hope…"），其余用被动或事物作主语（"Indices … were defined"）；没有口语、没有感叹、没有比喻。brief 第 8 条那句"磨损是过去的人留下的痕迹"本身带抒情色彩，我按规范性降格为陈述句：*"the worn surface of a staircase is a record left by the people who passed over it"*，保留意思、去掉抒情。
**B3（术语与符号）**：`Stair Wear Model`、`Wear Volume Model (WVM)`、`Wear Distribution Model (WDM)` 首次出现即给全称与缩写；`$p$` 只出现一次、只作 brief 所述的"腐蚀/磨损速率常数"，未重新定义、未换语义（这是 RED 里出过警号的地方）。
**B4（单位与精度）**：无单位、无区间、无点估计——本节按 brief 就不该有数值，因此不存在把区间写成点估计的风险。
**B5（时态）**：我定了一个一致的分工——`Strengths`/`Weaknesses` 讲模型的**性质**，全用现在时（holds / is described / reflects / rests / stands）；`Conclusion` 第二段讲**本次工作交付了什么**，全用过去时（were defined / were given / was used），第一段讲模型的**构成与功能**，用现在时（accounts for / consists of / speak to）。同一段内不来回跳。
**C1（套话/自评句比，真值 0/50 句）**：我逐句做了减法测试，没有留下"本节将说明…""This section presents…""The model has several advantages"这类删掉不掉信息的句子；段首句都直接承载内容（"Wear on a tread accumulates from…"、"The position of a foot on a tread is not treated as fixed."、"The model rests on simplifying assumptions…"）。
**C2（对比式 + 强调式构造，真值 0.00‰）**：`rather than` / `not merely` / `not only` / `precisely` / 句首 `This X …` **一次都没用**（写完用脚本查过，见下）。唯一保留的比较级是 *"gives an integrated account … than"* 一类——因为 brief 第 2 条本身要求"更整体"，比较是命题内容而非修辞腔。
**C3（极短断言句，真值最短 11 词）**：我按词数逐句量过，最短句 12 词（真值区间下沿 11 词），无 2–6 词类断言。这也是我不用条目式 "1) … 2) …" 的原因：那种排版天然产出极短句。
**明令别用的四个指标**：句长 CV、root-TTR、Flesch、以及 `delve/leverage/robust/comprehensive` 一类"AI 词表"——**一个都没当判据用**（前三个是反向或零分辨力，词表在本语料上是反的）。我只按 C1–C3 三条已知有分辨力的信号收束。

### 我自己补了 brief 里没有的东西（连同依据）
1. **一条脚注级引用 `[1]`**（题面）——brief 没要求。理由：纪律 B1 是硬闸门，而题面是我实际读过、可安全署名的唯一来源。
2. **结论第一段末尾把 use 类问题点名**（行进方向、单列/并排）——brief 第 7 条的清单里没有这一条，我从题面的三个 ask 与 brief 第 3 条（单列/并排、上行/下行）合成而来。措辞限定为"这些问题由两部件共同回应"，**没有**替模型宣称给出过定量答案。
3. **仿真用途的一句话展开**（"generate wear patterns under conditions specified in advance / examine how the inferred quantities respond when conditions change"）——brief 只说"大量使用了仿真"。我按 WVM 是"由因素推磨损量"的正向模型、且前面确有一章"结果与敏感性分析"（任务书告知），把它展开为正向生成 + 条件扰动两项；若与实情不符，删该分句即可，不影响句法。
4. **"恒定假设"的反面举例**（空置很久、门被封、加层）——brief 只说"真实使用可能有大波动"。例子取自题面自述的处境（长期居住、改建、增建）。用"a long time"而**不是**"a century"，就是为了守住零数值。
5. **单速率常数的后果推导**——brief 只说"这一层被简化掉了"，我补了一句后果："a damp climate cannot be separated from … heavy use"。这是该简化的直接推论，不是新数据。
6. **无损测量挂到考古的工作要求上**（"as archaeological work on a standing structure requires"）——brief 只说"契合考古对文物保护的关切"，我把这层关切显式写进句内。
7. **推荐参考文献条目**（题面那条的完整写法）——brief 没给，我按 B1 补齐；正文两处 `[1]` 与它对应。

### 我**没有**写进去的东西，以及原因
1. **任何数值与定量结果**（磨损量、年龄、人数、比率、误差）——brief 第 7 条明说结论段不报数字；纪律 A1/A2 要求每个数字可溯源，而我没有任何可溯源的数值；纪律还专门警告"具体性（含数字句比例）"在本节会惩罚正确行为。所以我一个字都没写，也没有替论文"回忆"前文的数。
2. **新方程、新符号、任何公式**——brief 第 1 条明令禁止。`p` 是既有的，且只用一次。
3. **指向前文章节/图表的交叉引用**（"as derived in Section 4"）——我没读前文，写出来必是 A3 违规；两节因此自足成文，标题也不带章号。
4. **为"正态踩踏"和"环境速率常数"配文献**——这两处**本该**有引用（这正是 B1 的用武之地），但我看不到你们的参考文献表，也无意替我未读的文献编条目；编引用就是 A1/A2 的翻版。**请队伍在这两句上挂你们自己表里的真实文献**：`Each footfall is a random event whose position on the tread is described by a normal distribution…` 与 `A single rate constant, $p$, stands for the rate of corrosion and wear…`。我宁可留白也不挂假来源。
5. **题面里的"低成本、小队伍、少工具"合规声明**（只写了非破坏性）——那是题面**要求**队伍满足的约束，brief 只对"无损"作了背书；替模型宣称成本与人力合规属于未经证实的断言。
6. **与他方法的对比、与获奖论文文风的靠拢**——纪律写明"像不像获奖论文"从来不是判据、参照分布不是模仿目标；对比他法又需文献支撑。两者一起排除。
7. **"本文结论确实不报数字"这句话本身**——把它写进正文就是制作注记（A4 的症状），所以它只出现在这里。
8. **条目式的优点/缺点清单**——见 C3。宁可三段散文，也不要五行断言。

### 我做过的机械核对（可复现）
- 数字：正文（两张标题以下的正文段落）**零个数值**——全篇仅有的两个阿拉伯字符是两处引用标记 `[1]` 的序号（B1 要求正文有引用，序号无法回避），**不是**任何测量值或结果；零个 `%`、零个单位、零个区间。
- 违禁构造：`rather than` / `not merely` / `not only` / `precisely` / `Moreover` / `Furthermore` / `Additionally` / `In conclusion` / `In summary` **命中 0 次**；句首 `This ` **0 次**（用"the model / the resulting wear pattern / the treatment of…"起句）。
- 句长：逐句词数统计，**最短 12 词**，无 ≤10 词句（首稿曾有一句 7 词的"Weaknesses"起句，已合并进上一句）。计数把连字符词算作一词、撇号不断词，故为下界口径。
- 唯一的符号：`$p$`，出现 1 次。

### 两点自查的诚实交代
- 纪律自己登记过：第三层（文风）的三个代理量**只有一个数据点、没有对照组、不足以定阈**。所以上面 C1–C3 我只能说"把已知的三条信号压到最低"，**不能**声称"已达标"。
- 同一处也登记过"写手风格与输入形态分不开"。本次输入是一份要点式的 brief，我特地把要点重写成成句散文而非照抄要点句式；但这层影响我无法从产物里自证剥离。
- 这两节我**没有**核对过与前面各章的任何一致性（术语、符号、编号、结论），因为我按要求没有读它们。请队伍合稿时把 `Stair Wear Model`/WVM/WDM 的写法与正文首次定义处对齐，并确认 `p` 在前文就是速率常数。
