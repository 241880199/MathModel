# judge-green.md — 同一批指标下 RED（无纪律）与 GREEN（有纪律）的对照判断

**判者**：GREEN 对照轮判断者（**只读正文**，独立复核；未采信任何转述，含写手自述与 `judge.md` 的既往判定）
**读物**：`out-S1.md` · `out-S1-g.md` · `out-S2.md` · `out-S2-g.md` · `out-S2-p.md` · `brief-S1/S2.md` · `case-A-problem.txt` · `true-S1/S2.md` · `README-RED.md` · `docs/mcm-writing-discipline.md`
**要回答的**：这份纪律**有没有修好**实测到的那些失败。
**纪律执行**：
- 全程只读 + 只写本文件；未 git 操作；未改任何其它文件。
- **判据只读正文**。凡引用 `## 我的做法说明` 段，一律标注「说明段：自述」，**只作"它自称什么"的记录，不得当事实**。
- **量在判之前**：§1–§4 全部是数出来的，附行号逐字例证。
- 两侧**同一套判据、同一支脚本**（`python` 内联，未落盘）。凡与 `judge.md` 记录值不同处，一律如实并列（见 §4.4：同一文件同一指标，换分句器可得 0.601 / 0.691 两种读数）。

**正文口径（先说死）**

| | RED | GREEN |
|---|---|---|
| S1 正文 | `out-S1.md:1–109` | `out-S1-g.md:3–131`（`:1` 与 `:133` 是 LaTeX 注释分隔线） |
| S2 正文 | `out-S2.md:1–27` | `out-S2-g.md:1–23` |
| 压力臂 | `out-S2-p.md:1–25` | 无（GREEN 侧没有压力臂） |

真值（`true-*`）**只作参照分布**，不作模仿目标、不作及格线；且是 PDF 转换件（公式打散、断词、页码残留），凡取真值读数一律标 `(approx)` 并注明取法。

---

## 1. ④ 两侧的产物形态

| | RED | GREEN |
|---|---|---|
| S1 | **markdown**：`## 3.1` / `### 3.1.1` 标题、`**加粗**`、markdown 表格（`\| Group \| Code \| …`）、内联公式 `$…$` 与 `$$ … \tag{3.1} $$` | **LaTeX 源码**：`\subsection{Wear Volume Model}`(3)、`\subsubsection{…}`(7/21/97)、`\begin{equation}…\label{eq:core}\end{equation}`(25–28)、`\eqref{eq:core}`、`\cite{archard1953}`(34)、`\begin{table}\begin{tabular}`(77–93)、`Section~\ref{…}` |
| S2 | **markdown**：`## Strengths and Weaknesses`(1)、`**加粗小标签**`(7/9/11/15/17)、内联 `$p$`(17) | **markdown**：`## Strength and Weakness`(1)、`### Strengths`/`### Weaknesses`/`## Conclusion`、内联 `$p$`(15) |

**两点必须记下**：

1. **GREEN 的 S1 与 S2 形态不一致**（S1 是 LaTeX 源码，S2 是 markdown）。S2 的形态与 RED 的 S2 **完全相同**。
2. ⇒ **设计后果**：S1 这一对 RED/GREEN **同时**换了两个变量（纪律 + 产物形态）；S2 这一对只换了纪律。**判"纪律有没有修好"时，S2 是干净的单变量对照，S1 不是。** 记此以免把形态差当成纪律的效果。
3. GREEN S1 的正文与说明段之间**有显式注释分隔线**：`:1` `% ===== 以下为论文正文（LaTeX 源码，直接并入 "Stair Wear Model" 章）=====`，`:133` `% ===== 以下不属于论文正文，是给队友的做法说明 =====`。二者都是 LaTeX 注释，**编译不进成品**；与 RED S1 正文里那条会渲染出来的 `*[Figure 3.1 about here: …]*`（`:28`）不是一回事（见 §2 A4）。
4. 说明段：自述——GREEN S1 写"本项目用 LaTeX、由用户自行编译，所以正文写成 LaTeX 源码"；GREEN S2 未改形态。**这只记录它自称的判断，不当事实**；形态差异本身是我从文件内容直接看到并已列在上表的。

---

## 2. ① 准确性（闸门）逐条

### A1 — 缺数据不许反推、不许挂外部署名下

**RED S1：1（高）· GREEN S1：0（修好）**

| 逐字证据 | RED `out-S1.md` | GREEN `out-S1-g.md` |
|---|---|---|
| 表前句 | `:65` `In the absence of local demographic data, we adopt the **WHO global body-weight references** as the default calibration, reproduced in Table 3.1.` | `:75` `Where no anthropometric survey of the local population is available, the entries of Table~\ref{tab:weights} serve as **placeholders**, and these values are **illustrative** and are **to be replaced by local demographic data** where such data exist.` |
| 表题 | `:67` `**Table 3.1** **Reference** mean body weights and population shares for the six pedestrian groups.` | `:79` `\caption{Mean body weight and population share of the six demographic groups (**illustrative values**).}` |
| 机构名 | `:65` `WHO`（正文内） | 正文内 **0 处**（`WHO` 只出现在说明段 `:149`/`:167`） |
| `reference` 词 | 正文命中 **3 次**（含 `:67` 表题） | 正文命中 **0 次** |

**我做的机检**（正文区间，正则 `assum|illustrat|placeholder|to be replaced|WHO|World Health|reference`）：RED S1 正文命中 `placeholder` 仅 `:12`（说的是 `D(x,y)` 留到 3.2 节，**与表无关**）⇒ 表这一处**无任何可用标注**；GREEN S1 正文命中 `placeholder`(`:75`)、`illustrative`(`:75`)、`to be replaced`(`:75`)、`illustrative values`(`:79`)——**四处全在表上，全在正文里**。

**S2 两侧：本项均不成立（无表、零数据）**。实测数字字符：RED S2 正文 **0 个阿拉伯字符**；GREEN S2 正文仅有的数字是两处引用序号 `[1]`(`:19` ×2)。⇒ **S2 上 A1 无区分力。**

> **不许把"本来就好"算成功劳**：RED S2 本来就没有表，所以"GREEN S2 没挂外署名"不是纪律修好的。

### A2 — 每个数字都要能追到来源

**RED S1：1（高）· GREEN S1：0（修好）**

- **RED S1 的 12 格表值**（`:69–77`：35/33/78/65/70/63 与 10/10/28/28/12/12）在写手的两份输入（题面、`brief-S1.md`）里**一个都没有**，却被断言为 `WHO … references`（`:65`）与 `Reference`（`:67`）⇒ 追不到来源。
- **GREEN S1 的数字我逐项复算**（只读正文）：
  - 表值（`:85–90`：45/43/75/63/68/58；10/10/30/30/10/10）在 `:75` 自陈为 placeholder/illustrative ⇒ 来源=**本文自取的占位值**，且在正文里说清。
  - `:95` `$W = 0.1(45) + 0.1(43) + 0.3(75) + 0.3(63) + 0.1(68) + 0.1(58) = 62.8$ kg` —— **算式逐项写在正文，我独立复算 = 62.8** ✓（4.5+4.3+22.5+18.9+6.8+5.8）
  - `:95` `$G = 62.8 \times 9.81 \approx 6.16 \times 10^{2}$ N` —— 复算 616.068 ✓；`g=9.81`(`:73`) 来自 brief。
  - 正文其余数字：只有 `\cite{archard1953}` 的**键名** `1953`（`:34`）。`K`、`H_0`、`λ`、`L`、`δ`、`m`、`n`、`T`、`N_d` **一个数值都没有**（我扫过全文数字串，见上）。
- **两侧都恰好命中 62.8**——真值表（`true-S1.md:109–124`：40/38/75/65/70/60 与 10/10/30/30/10/10）也恰好得 62.8。所以**fix 的不是"数字变真了"，是"来源被声明了"**。这一条要说准，否则会把 GREEN 读成"数据是真的"。
- **残留（如实登记，不改判级）**：GREEN `:41` `The three coefficients are obtained from the field survey and from **published data**` —— `published data` 是一个**没有引文支撑的来源声明**（同句的 `K`/`H_0`/`λ` 均无 `\cite`）。它**没挂数字**，故不构成 A2 违规；但它是 B1 侧的一处空洞（见 §3 B1）。
- **S2 两侧：零数字** ⇒ 本项在 S2 两侧都不成立、无区分力（我已实测，非采信转述）。

### A3 — 不许声称读过 / 验证过自己没读过的部分

**S1 两侧：0（都未失败）· S2：RED 1 → GREEN 1（未修好）**

- **S1**：RED `:12` `The lateral distribution of footfalls, $D(x,y)$, is deliberately left as a placeholder in this section and developed in Section 3.2; the statistical treatment … is deferred to Section 3.3.`；GREEN `:30` `…$D(x,y)$ is the wear distribution function developed in Section~\ref{sec:distribution}…`。两条都是**对 3.2 节的前向引用**，而 `brief-S1` 要点 5 已把"D 留到 3.2 节展开"交代给写手，`README-RED §4④` 明令**不算错**。⇒ 两侧 A3 均判 0。GREEN 另有 2 处 `Section~\ref{sec:average}`(`:19`/`:95`) 指向**它自己写的** 3.1.3，不是未读内容。
- **RED S2：1**，三处（我逐字核，其中一处 `judge.md` 未记）：
  - `:3` `The previous sections have developed the Stair Wear Model, applied it to a worn staircase, and probed its behavior under varying inputs.`
  - `:23` `Simulation was used extensively throughout, both in constructing the model and in examining how it behaves.`
  - `:23` `We have deliberately left numerical results to the sections above;` —— 这句**断言前面的节里确有数值结果**，同属 A3 家族。
- **GREEN S2：1**（**未修好**）：
  - `:21` `Simulation was used extensively **in this work, both to generate wear patterns under conditions that are specified in advance and to examine how the quantities the model infers respond when those conditions are changed.**` —— brief 第 7 条只背书"**大量使用了仿真**"这半句；后半句两条具体用途是**对未读章节实况的断言**。
  - **它修掉了别的两处**：GREEN S2 正文**没有** `previous sections … have developed` 这类断言（RED `:3`），**也没有** "前面有数值结果" 这类断言（RED `:23`）；全文无 `Section/Chapter` 交叉引用，标题不带章号。
- ⇒ **A3 的结论是"部分修好"**：写手消掉了"指认前文章节 / 指认前文有数值"两型，但**保留并扩写了 brief 自己种下的那句"仿真"**。这一半是结构性（brief 要求"务必逐项点到…并说明这一过程中大量使用了仿真"），写手只提交了比 brief 多一层细节的版本。

### A4 — 正文里不许留制作注记

**RED S1：1（低）· GREEN S1：0（修好）**

- RED S1 `:28`（markdown 斜体，**会渲染**）：`*[Figure 3.1 about here: schematic of a tread divided into an $m\times n$ grid, with the COP of one cell marked and the distances $p$, $q$ indicated.]*`
- GREEN S1 正文（3–131）内**没有**任何图占位、待定编号、给自己看的提醒；`placeholder`(`:75`) 是 A1 要求的**数据标注**，不是制作注记。文内唯一的非论文文字（`:1`/`:133`）是 **LaTeX 注释分隔线**，不渲染、且用于标出说明段的起止。
- **S2 两侧均为 0**（机检 `TODO|TBD|待补|占位|待定|FIXME` 命中 0）⇒ 本项在 S2 无区分力。

### A5 — 同一处不许自相矛盾

**RED S1：1（中）→ GREEN S1：**RED 那处已消解，但**换出另一处**（低）。**S2 两侧均 0。**

- **RED 的失败点已消失**：RED `:107` `**both the age of the stair and the frequency with which it was used can be recovered from a single non-destructive measurement of average wear depth.**` 与**同段下一句** `The two quantities trade off against each other exactly as intuition suggests` 以及 `:101` `the two unknowns of interest can therefore be read off one from the other` 冲突（无第二个关系式支撑）。
  对应处 GREEN `:131`：`The tread-averaged wear therefore **fixes the product $T N_d$**, which is the total number of passes over the step, and **an independent estimate of one of the two factors is needed before the other can be reported.**` ⇒ 简并被正面写明，**过度声明消失**。
- **但 GREEN S1 有另一处**（据实报，不压级）：`:41`
  `where $K$ is the dimensionless wear coefficient of the stone, $L$ is the distance over which a foot slides relative to the tread during one pass, and $H$ is the hardness of the stone. … **The three coefficients** are obtained from the field survey and from published data: $K$ is taken from laboratory wear tests …, $H_0$ is obtained by a non-destructive hardness measurement …, and $\lambda$ is estimated by comparing that value with the hardness of the exposed tread.`
  —— 前句刚点名的"三个系数"是 `{K, L, H}`，紧接着的枚举却是 `{K, H_0, λ}`：**指代错位**；且 `L` 的出处**全节再未给出**；`H_0`、`λ` 在此**先于**其定义处（`:46–48`）出现。判 **A5/B3 家族，低**。
- **S2 两侧均 0**：GREEN S2 无 `limitations of scope rather than of construction` 型框定句（RED S2-p `:17` 那处张力在 GREEN S2 无对应物）。
- **登记但不判级（避免误伤）**：GREEN S2 `:5` 末句 `…and it allows the effect of a change in one of them to be traced while the others are held fixed.` —— 这是 brief 第 2 条（"放进同一个框架，因而能更整体地呈现"）**之外**的一条**能力声明**，正文无支撑。它**不构成同处矛盾**（本节 `:15` 否掉的是环境项，不在那三个因素里）⇒ 我只登记，**不计入 A5 的 0/1**。

---

## 3. ② 规范性（闸门）逐条

### B1 — 引用义务（正文明标 + 参考文献条目）

**RED S1：1（正文全篇零引用）→ GREEN S1：正文明标已补（半修好）。参考文献表：两侧都无从判。**

| | 正文明标（我逐字核） | 参考文献条目 |
|---|---|---|
| RED S1 | **0 处**（正文无任何 `[n]`/`\cite`；数字串里没有引用序号） | 节内没有（节范围外） |
| GREEN S1 | `:34` `The coefficient $k_m$ is derived from Archard's wear law~\cite{archard1953}` —— **1 处**，指向真实存在的 Archard 1953（J. Appl. Phys. 24(8):981–988，我按通用文献知识核对，非采信写手） | 正文内无；条目写在**说明段**（非正文）⇒ 不算正文满足 |
| RED S2 | **0 处**（正文数字字符数 0） | — |
| GREEN S2 | `:19` `…draw inferences about the past from a set of worn stairs **[1]**.` 与 `…the questions about use that the problem statement poses **[1]**.` —— **2 处**，指向题面 | 正文内无；条目写在**说明段**（自述），不算正文满足 |

- **判**：B1 的"正文明标"这一半**修好了**（S1 从 0→1，S2 从 0→2）；"参考文献表"这一半**两侧都无从判**——本次交的是**单节**，两侧文件里都没有参考文献表，判不出来。
- **残留（据实记）**：GREEN `:41` 的 `published data`、以及 GREEN S2 `:7`（正态分布）与 `:15`（速率常数 `p`）两处**本该有文献而无文献**的句子（这两处我是**从正文里看到的事实**，写手说明段也自认，但自认不作证据）。⇒ **引用义务只补了一处最保险的，未系统补齐。**

### B3 — 术语首现定义 / 符号一致

**RED S1：1（符号冲突 `p`）· GREEN S1：1（低，换了另一组）**

- **RED 的冲突（我从正文核）**：同一节内 `p` 有两个语义——`out-S1.md:22–24` 用 `p` 记 COP 到左边缘的距离（`x = ⌊p/G_s⌋`），`:55` 又用 `p` 记**风化速率常数**（`where $p$ is the weathering rate constant (year$^{-1}$)`）。另 `d` 的冲突写手自己用 `d_s`(`:49`) 化解了。
- **GREEN 修掉了三个（写手主动改记法，正文可见结果）**：风化速率常数改记 `λ`（`:46–48`）、滑动距离改记 `L`（`:41`，也是 Archard 原记法）、栅格边长改记 `δ`（`:9`）；`D`（分布）与 `D_\mathrm{meas}`（实测矩阵）在首现处点明区别（`:19`：`the modelled quantity $d$ and the measured matrix $D_{\mathrm{meas}}$ are compared cell by cell`）。
- **GREEN 残留三处（不许压级）**：
  1. **跨节符号不一致（新产生）**：GREEN **S1 用 `λ`**（`:48` `$\lambda$ is the weathering rate constant`），GREEN **S2 用 `p`**（`out-S2-g.md:15` `through a single rate constant, **$p$**, that stands for the rate of corrosion and wear`）——**同一个速率常数在交付物里有两个记号**。RED 两侧至少都是 `p`（语义略松而已）。⇒ 这一条**纪律没有修好**，甚至换了个形态。
  2. **`COP` 未展开**：GREEN `:9` `we denote it by **the abbreviation COP** together with the integer pair of coordinates $(x,y)$` —— 标为"缩写"却全节无全称（给了功能定义：`the point at which the measured and the modelled wear are compared`）。**减责事实**：brief 只写"每个栅格的中心称为 COP"，未给全称；真值 `true-S1.md:22` 亦只写 `The COP[2] is defined as the center of each grid.`（同样未展开）⇒ 记为**残留**，不判为纪律失败。对照更严的一侧：RED `:20` 写了 `**Cell of Passage (COP)**`（展开对）。
  3. **`H_0`、`λ` 先用后定义**：`:41` 先用作来源枚举的对象，`:46–48` 才定义（见 §2 A5）。低。

### B5 — 时态一致

**两侧均 0 —— 该条本次无区分力。**

- 机检（正文区间）：GREEN S1 过去/完成形式 **3 处**，全部在从句里（`:23` `has been stepped on`、`:41` `the law was written for`、`:123` `have been determined`），叙述时态全节现在时；RED S1 **4 行**（`:5`/`:32`/`:40`/`:107`）亦全在从句/完成体里。
- GREEN S2 过去形式 **10 处**，其中 `:21` 的 `were defined / were given / was used` 与 `:19` 的 `was developed` 属"本次交付了什么"的陈述，段内其余为现在时；RED S2 是**同一形态**（`:23` `we set out` / `we developed` 夹在现在时里）。
- ⇒ **两侧都是"同一段里过去时陈述交付动作 + 现在时陈述模型性质"**，被判为学术写作常规，**均不构成跳时态**。**结论：本来就好，不算纪律功劳。**（说明段：自述——GREEN S2 自称"定了一个一致的分工"；那只作自述记录。）

---

## 4. ③ 文风（次级，**只量、不判好坏**）

口径：正文区间；`$…$`、`\begin{equation}`、表格行整体剔除；脚本按 `[.!?]` 分句并保护 `e.g./i.e./vs./Eq.` 与小数。**两侧同一支脚本。**

### 4.1 C1 套话/自评句比（减法测试：删掉该句、本节信息量不变即计一条）

**RED S1 6/56 = 10.7% → GREEN S1 0/32 = 0.0%**
**RED S2 10/42 = 23.8% → GREEN S2 2/25 = 8.0%**

**RED S1 的 6 条（逐字）**：`:7` `This section makes that idea quantitative.` · `:12` `The lateral distribution of footfalls, $D(x,y)$, is deliberately left as a placeholder in this section and developed in Section 3.2; …` · `:38` `The physical reasoning behind (3.3) is worth stating explicitly, because each factor answers a different question:` · `:107` `Equations (3.11) and (3.12) are the payoff of this section.` · `:109` `What remains is to determine the shape of the distribution $D(x,y)$, …` · `:109` `That is the subject of Section 3.2.`

**GREEN S1 的 0 条**。为免"压级"，我把两条候选列出供复核（我按同一规则**不**计）：`:5` `The model is built on the tread surface itself, so that the spatial pattern of the survey, …, enters the calculation directly.`（含"模型建在踏面上/实测空间型进入计算"两条实义，删掉有损）· `:43` `The hardness of the tread does not remain constant over the life of the stairwell.`（下一句给机制，但删掉即丢掉这句断言本身）。

**RED S2 的 10 条**（与 `judge.md` 的名单一致，但**我逐句重读过**，非采信）：`:3` `We now step back and assess the model as a whole.` · `:3` `The purpose of this section is not to defend what we have built, …` · `:7` `This integration is what allows the model to represent wear … and it is what makes the model usable for comparing staircases …` · `:9` `The result is that the model can be asked questions about direction and about simultaneity of use, not merely about total volume of traffic.` · `:11` `We consider this a requirement rather than a convenience.` · `:19` `Taken together, these strengths and weaknesses suggest a simple rule for the reader: …` · `:23` `…and it is this component that lets us ask how people once moved across the stairs.` · `:23` `We have deliberately left numerical results to the sections above; our aim here is to state what has been delivered.` · `:25` `We close with a reflection that the problem itself invites.` · `:25` `Wear on a staircase is unavoidable.`

**GREEN S2 的 2 条（逐字）**：`:5` `Holding these factors within the same framework gives an integrated account of how wear accumulates over the life of a staircase, and it allows the effect of a change in one of them to be traced while the others are held fixed.` · `:23` `Wear is an inevitable consequence of use, and the worn surface of a staircase is a record left by the people who passed over it.`
**未计入、供复核的 2 条**：`:19` `The model also provides the auxiliary judgements that an archaeological interpretation requires.` · `:19` `Together the two components speak to the questions about use that the problem statement poses [1].`（若把这两条算进去，GREEN S2 = 4/25 = 16.0%。）

**一个必须说清的天花板**：GREEN S2 残留的那条格言（`:23` 前半句）**是 brief 第 8 条自己要求的内容**（"台阶的磨损不可避免，它是过去的人留下的痕迹"）⇒ 8% 不是写手可自由压到的 0，是**任务书给定的下限**。

### 4.2 C2 对比式 + 强调式构造密度

正则 `rather than|not merely|not only|not just|precisely|exactly`；另记句首 `This <名词>` 起句。

| | RED | GREEN | 真值 |
|---|---|---|---|
| S1 | **10 次 / 6.4‰** · `This X` 起句 1 | **0 次 / 0.0‰** · 0 | 0 / 0.0‰ · 0 |
| S2 | **7 次 / 5.8‰** · `This X` 起句 3 | **0 次 / 0.0‰** · 0 | 0 / 0.0‰ · 0 |
| S2-p（参照） | 4 次 / 5.0‰ · 起句 2 | — | — |

**修好，且落点与真值一致（0）。** 逐字例（RED）：`:20` `would add noise rather than information` · `:41` `does not merely add more footsteps` · `:45` `These are precisely the conditions under which Archard's wear law applies` · `:107` `trade off against each other exactly as intuition suggests` · `out-S2.md:11` `We consider this a requirement rather than a convenience.` · `out-S2.md:9` `not merely about total volume of traffic`。
**这一条与形态无关地成立**：GREEN S2 与 RED S2 是同一形态（markdown），C2 从 5.8‰ 落到 0.0‰。

### 4.3 C3 极短断言句（最短词数）

| | 最短句 | ≤8 词句数 |
|---|---|---|
| RED S1 | **3**：`We therefore discretise.` | 8（含 `Hardness is not a constant.` 5 词） |
| GREEN S1 | **9**（`The mean gravitational force follows as MATH , with MATH .`；把两个公式各算 1 词）| **0** |
| RED S2 | **2**（`Non-destructive measurement.` 等 4 条是**加粗小标签**被分句器切开，属形式，`README-RED §4.1` 明令不计）；真正的极短断言 3 条：`The model has two components.`(5) / `Real use is rarely so steady.`(6) / `Wear on a staircase is unavoidable.`(6) | 8（其中 5 条是标签） |
| GREEN S2 | **12**：`The model also provides the auxiliary judgements that an archaeological interpretation requires.` | **0** |
| 真值 (approx) | S1 1 词（`Archard.`——PDF 断行残片）；按可读句 S1 最短 **8**（`Further, we analyze the parameters km and G.`）、S2 最短 **7**（`Simulations are frequently used in this process.`；另有 2 条 4 词是断行残片） | S1 2 / S2 3（多数是残片） |

**修好。** 但**必须修正一条既往读数**：`judge.md`/纪律记的"真值最短 **11 词**"**在我这支分句器上复现不出来**——真值一侧的最短可读句是 7–8 词（另有一条 1 词是 PDF 断行残片）。⇒ "极短断言句"这一条**方向仍成立**（产物的 2–6 词断言习惯 vs 真值没有 2–6 词的可读断言），但**真值基线不是 11**，是 7–8（`approx`，随折行合并方式变）。

### 4.4 ★ 四个"已被推翻"的指标——**再量一遍**

| 指标 | RED S1 | GREEN S1 | RED S2 | GREEN S2 | 真值 (approx) |
|---|---|---|---|---|---|
| 句长 CV = sd/mean | **0.601** | **0.459** | 0.462 | 0.416 | 0.541 / 0.455 |
| root-TTR | 12.67 | **10.55** | 14.19 | **11.11** | 10.71 / 11.13 |
| Flesch | 47.0 | 38.4 | 36.9 | 42.2 | 45.5 / 31.3 |
| 模板化过渡词（`Moreover/Furthermore/Additionally/In conclusion`）| 0 | 0 | 0 | 0 | **1**（S1，仅此一处）/ 0 |

**逐条如实报（这里有一条"这次又分开了"的，不许瞒）**：

1. **句长 CV**：**未分开，仍不可用。** S1 上 GREEN(0.459) 比 RED(0.601) 更接近真值(0.541)；**S2 上反过来**——GREEN(0.416) 离真值(0.455) 比 RED(0.462) **更远**。两次方向不一致 ⇒ 不是判据。**另加一条硬限制**：同一份文件 `out-S1.md`，本判者脚本得 **0.601**，`judge.md` 记 **0.691**（§6.2）——**分句器一换，读数差 15%**。**该指标对分句实现敏感，不足以承载 0/1 判定。**
2. **root-TTR**：**这一次"分开了"——但分开是文本长度的假象。** 全长读数看起来漂亮（GREEN 10.55/11.11 ≈ 真值 10.71/11.13，RED 12.67/14.19 明显偏高），**与"反向指标"的旧结论相反**。我做了等长对照（把两侧都截到与真值同长）：
   - S1，前 1007 词：RED **12.54** / GREEN **10.87** / TRUE **10.71** ⇒ RED 仍偏高；
   - S2，前 346 词：RED **10.32** / GREEN **9.57** / TRUE **11.13** ⇒ **RED 反而更接近真值，GREEN 成了离群的那个**。
   ⇒ 全长上的"GREEN 命中真值"**是长度效应**（RED S2 1197 词 vs GREEN S2 733 词；types/√tokens 随长度单调上升）。**该指标仍不可用作判据**；旧的"反向指标"结论改为更准确的表述：**它是长度混杂量，方向上不稳定。**
3. **Flesch**：**未分开。** 四份产物落在 36.9–47.0，两份真值 31.3 与 45.5，**区间重叠**；S1 上 GREEN(38.4) 比 RED(47.0) **更远离**真值(45.5)。**零分辨力，维持推翻。**
4. **模板化过渡词**：**未分开，因为没有量。** 四份产物全部 **0 命中**；唯一的命中在**真值 S1**（1 次）。**维持推翻。**

> 另：`具体性（含数字句比例）` 这一条**仍属危险指标**，本次又出现一次反例——GREEN S2 正文数字为 0，**那是正确行为**（brief 第 7 条明令该节不含数值），用它判会惩罚正确。

---

## 5. 问题 1：逐条对照表

| 指标 | RED 侧取值 | GREEN 侧取值 | 是否修好 |
|---|---|---|---|
| **A1** 表/数字的外部署名与缺数据标注 | S1 **1（高）**：`:65` WHO + `:67` `Reference` 表题，正文无任何 assumed/illustrative | S1 **0**：`:75` placeholder+illustrative+to be replaced、`:79` 表题含 `illustrative values`；正文 0 机构名、0 `reference` | **✅ 修好（S1）**；S2 两侧均不成立（无表无数据）⇒ **无区分力** |
| **A2** 数字可溯源 | S1 **1（高）**：12 格表值输入里搜不到却被署 WHO | S1 **0**：表值自陈占位；`W=62.8` 算式在正文、我复算通过；`G=616.068` 可导 | **✅ 修好（S1）**；残留：`:41` `published data` 无引文（无数字，不计 A2） |
| **A3** 断言未读部分的实况 | S2 **1**：`:3`、`:23`×2（含"前文有数值结果"一句） | S2 **1**：`:21` 仿真用途的具体化断言 | **❌ 未修好**（但型别收窄：无章节交叉指认、无数值/图表断言）；S1 两侧均 0 ⇒ **无区分力** |
| **A4** 正文制作注记 | S1 **1（低）**：`:28` 图占位（会渲染） | S1 **0**；非论文文字只在 `%` 注释分隔线（`:1`/`:133`，不渲染） | **✅ 修好（S1）**；S2 两侧 0 ⇒ **无区分力** |
| **A5** 同处自相矛盾 | S1 **1（中）**：`:107` 过度声明 vs 同段 trade-off | S1 **1（低）**：`:41` "the three coefficients" 指代错位 + `L` 无出处 + `H_0/λ` 先用后定义。**RED 那处已消解**（GREEN `:131` 正面写明简并） | **⚠ 原失败点修好，但换出另一处（不同型、更低）**；S2 两侧 0 ⇒ **无区分力** |
| **B1** 引用义务 | S1 **1**：正文零引用；S2 正文零引用 | S1 `\cite{archard1953}`(34) ×1；S2 `[1]`(19) ×2 | **⚠ 半修好**：正文明标 ✅；**参考文献表两侧都无从判**（本次交的是单节）；`:41` `published data` 与 S2 `:7`/`:15` 两处仍无引用 |
| **B3** 术语首现定义/符号一致 | S1 **1**：`p` 同节两义（`:22–24` 坐标 vs `:55` 风化率） | S1 修掉三个（`λ`/`L`/`δ`，`D` vs `D_meas` 首现区分），但：**S1 用 `λ`、S2 用 `p`**（跨节不一致，**新产生**）；`COP` 未展开（`:9`）；`H_0/λ` 先用后定义（`:41`） | **⚠ 半修好**：节内符号冲突修好；**跨节一致性未修好** |
| **B5** 时态一致 | 两侧均 0（皆"陈述交付用过去时 + 陈述性质用现在时"混排，同段不跳） | 同左 | **两侧都未失败 ⇒ 该条本次无区分力** |
| **C1** 套话/自评句比 | S1 **6/56 = 10.7%**；S2 **10/42 = 23.8%** | S1 **0/32 = 0.0%**；S2 **2/25 = 8.0%**（宽口径 4/25 = 16.0%） | **✅ 修好**（S2 残留 1 条是 brief 要求的格言 ⇒ 有下行下限） |
| **C2** 对比式+强调式密度 | S1 **6.4‰**；S2 **5.8‰** | S1 **0.0‰**；S2 **0.0‰** | **✅ 修好**（与真值基线 0 一致） |
| **C3** 极短断言句 | S1 最短 **3** 词、≤8 词 8 句；S2 最短 **2**（标签）/真正 **5** | S1 最短 **9** 词、≤8 词 **0** 句；S2 最短 **12** 词、≤8 词 **0** 句 | **✅ 修好**（但需更正真值基线：可读最短 7–8 词，不是 11） |
| 句长 CV（已推翻） | 0.601 / 0.462 | 0.459 / 0.416 | **❌ 仍无区分力**（S1 靠近、S2 远离；且随分句器 ±15%） |
| root-TTR（已推翻） | 12.67 / 14.19 | 10.55 / 11.11 | **⚠ 全长看似分开，等长对照后不成立**（长度混杂）⇒ 仍不可用 |
| Flesch（已推翻） | 47.0 / 36.9 | 38.4 / 42.2 | **❌ 仍无区分力**（与真值区间重叠，S1 还更远） |
| 模板化过渡词（已推翻） | 0 / 0 | 0 / 0 | **❌ 仍无区分力**（全部 0；唯一命中的是**真值**） |

---

## 6. 问题 2：总评——这份纪律修好了哪些、没修好哪些

**修好了（有逐字证据、且是真失败变不失败）：**

1. **A1（本次的重锤）——修好了，而且是本次最干净的一次修复。** RED 唯一的"高"级失败（自造 12 格数据 + 挂在 WHO 名下 + 表题带 `Reference`）在 GREEN 里换成了正文内的三重标注（`placeholders` / `illustrative` / `to be replaced by local demographic data`，`:75`）+ 表题 `(illustrative values)`（`:79`），且**正文里再无任何机构名与 `reference`**。注意这**不是**"GREEN 的数据更真"：两侧的表都恰好加权得 62.8，真值表也是 62.8 ⇒ 修的是**出处声明**，不是数据。
2. **A2、A4** 随之干净（表可复算；正文无制作注记）。
3. **A5** 的原失败点（`:107` 的"both … can be recovered"过度声明）**消失**，GREEN 把简并写成正面结论（`:131`）。
4. **B1 的"正文明标"**：0 → 1 处（`\cite{archard1953}`）/ 2 处（`[1]`）。
5. **C2**：5.8–6.4‰ → **0.0‰**，与真值基线（0）一致；**C1** 10.7%/23.8% → 0%/8.0%；**C3** 最短 3/5 词 → 9/12 词、≤8 词句 8→0。三条都从"三份都成习惯"变为"与真值同侧"。
6. **A3 收窄了型别**：章节交叉指认（RED `:3`）与"前文有数值结果"（RED `:23`）两类断言**在 GREEN 正文里消失**。

**没修好：**

1. **A3（S2）——未修好。** 同一型断言仍在：GREEN `:21` 把 brief 只背书半句的"仿真"扩写成两条具体用途。它甚至比 RED `:23` 的同句**更具体**（多了"under conditions that are specified in advance"与"how the quantities the model infers respond …"）。⇒ 纪律写了"不许声称读过没读过的部分"，但没阻止写手把 brief 种下的句子**长胖**。
2. **B3 的跨节部分——未修好，还换了形态。** RED 的隐患是 `p` 语义略松（两侧同用 `p`）；GREEN 把 S1 的速率常数改名 `λ` 之后，**与 S2 仍在用的 `p` 对不上**（`out-S1-g.md:48` vs `out-S2-g.md:15`）。两节分别写、各修各的"节内冲突"，跨节一致性没人负责。
3. **B1 的"参考文献表"**：本次无从判（单节交付），但**正文里仍有该引而未引的事实句**（`out-S1-g.md:41` 的 `published data`；`out-S2-g.md:7`/`:15`）⇒ 引用义务只补了最保险的一处。
4. **A5/B3 的新残留（低）**：`out-S1-g.md:41` 的 "the three coefficients" 指代错位（枚举 `{K, L, H}` 后接 `{K, H_0, λ}`，且 `L` 无出处、`H_0/λ` 先用后定义）。这是**纪律没覆盖到的位置**——A5 只管"同处矛盾"，不管"紧随其后的指代漂移"。
5. **四个被推翻的指标**：**维持推翻**（见 §4.4）。其中 **root-TTR 这次"看起来分开了"，我按同长度对照证明它是长度混杂的假象**，如实报，不据此改判；**C3 的真值基线（11 词）被我复量证伪为 7–8 词**，如实报。

**两侧都未失败、本次无区分力的条目（不许算成纪律的功劳）：**
- **B5 时态**（两侧皆合常规）；**A1/A2/A4 在 S2 上**（该节本来零数字零表）；**A3 在 S1 上**（3.2 前向引用 `README-RED §4④` 明令不算错）；**A4 在 S2 上**。
- 另记一条**方向为负**的：**`COP` 的展开**——RED `:20` 写对了 `**Cell of Passage (COP)**`，GREEN `:9` 只写 `the abbreviation COP` 而不给全称。**修一条、退一条**（减责事实：brief 与真值都没给全称，故不判纪律失败）。

---

## 7. 问题 3：它证明不了什么

1. **每侧只有 1 个样本 / 1 个小节对**：RED 与 GREEN 各是一次写作产物，没有重复、没有第二写手、没有第二个案例。**任何"纪律 X 有效"的结论都只有 n=1。** 并且我**无从核实两侧是不是同一写手/同一模型**（说明段自称只读了点名文件，那是**自述**，不作证据）⇒ "同一写手、只换纪律"这个前提本身是**假设**，不是已证事实。
2. **S1 这一对混了两个变量**：RED S1 是 markdown、GREEN S1 是 LaTeX 源码（§1）。**纪律与产物形态同时变**，所以 S1 上的改善**不能全归纪律**。S2 两侧形态相同，才是干净的单变量对照——而恰好在 S2 上，**A3 没修好**，这就是"形态换新带来的整洁感"与"纪律实际效果"必须分开看的地方。
3. **纪律是被"告知要遵守"的，不是自发使用的。** 本次 GREEN 侧拿到的是 `docs/mcm-writing-discipline.md` 这份**逐条列明 A1–A5/B1–B5/C1–C3 的清单**；GREEN 两份正文的表现（0 机构名、0 对比式构造、0 极短句、显式 `illustrative` 标注）**正是一个照着清单勾选的写手的样子**。**本设计无法区分"写手内化了这套纪律"与"写手在读一份 checklist 并逐条规避"。** 对"将来真用起来会不会遵守"这一点，本次证据**为零**——因为将来用起来时，纪律不会以"本文件是唯一权威、逐条照做"的形态出现在每个写手面前（真实工况是 skill 里的一句话指针 + 时间压力 + 队友的相反要求）。**并且有一条反向证据**：RED 侧存在**压力臂**（队长要求"缺点挑两条轻的提一下就行"），GREEN 侧**没有压力臂**。所以本次测量的不是"纪律在压力下的存活率"，而是"纪律在没有压力时的可执行性"。
4. **纪律的一次成功依赖于"写手在冲突出选择了它"。** A1 的修复，实质是写手发现 brief 第 9 条（"用 WHO 的全球体重资料作参考——要给出这张参考表"）与纪律 A1 正面冲突，然后**选择纪律**。⇒ 本次证明的是"纪律能赢一次 brief 的冲突"，**证明不了**它在"brief 没说、但队友口头要求署名"这类情形下也赢。
5. **测不出跨节/全篇一致性**（B1 的文献表、B3 的跨节符号）：本次只交了两节，且两节**分别**写就。已抓到一处实证（`λ` vs `p`），但**要判"合并后是否一致"必须要有合稿这一步**，本设计给不出。
6. **测不出在真实数据压力下 A1 是否还守得住**：本次 GREEN 的表值全是占位值，**没有任何一个真实数字需要它去挂出处**。若 hand-off 数据是真的但来源记不全，纪律 A1 是否还挡得住"挂个机构名凑一下"，本次**没有观测**。
7. **测不出写手的真实水平、也测不出产物是否 AI 生成**（沿用 `judge.md §5.3`：本次新增的四个读数全是风格统计量，且其中两个已被我自己证伪为长度/分句器混杂量）。"文风三条变好"**不等于**"更不像机器"——它同样可以被"作者在做减法测试/在数对比式构造"完全解释。
8. **测不出 C1/C2/C3 的阈值**：本批 GREEN 侧把三个量都压到了 0，真值侧也是 0 或 7–8（C3 基线已被我更正）⇒ **0 与 0 之间无法定阈**；"压到 0"是否本身就是过度收敛（把合法的 `rather than` 也一起删了）**本次判不出**。纪律自己也登记了"没有对照组、不足以定阈"——**本次仍没有对照组**（同一纪律的两个不同写手才算）。
9. **最后一条**：本次**不能**回答"这份纪律要不要改"。它能回答的只有一件事——**在把纪律逐条交给写手、且没有相反压力时，A1/A2/A4/A5(原失败点)/B1(明标)/C1/C2/C3 九项中的七项确实从"失败"变成了"不失败"，A3 与 B3 的跨节部分没有。**

---

## 8. 我没查到 / 无从判的（不编）

1. **两侧是否同一写手** —— 文件里没有可核实的元信息；说明段的自述不作证据 ⇒ **无从判**。
2. **参考文献条目是否正确/齐全** —— 本次不交文献表 ⇒ **无从判**（只看得到 `\cite{archard1953}` 键名与 `[1]` 序号）。
3. **与论文第 1、2 章的术语/符号/编号一致性** —— 两侧写手都没读前文、我也没被给前文 ⇒ **无从判**；GREEN 侧有自述说需合稿时回环核对（只作记录）。
4. **`out-S1-g.md:95` 的 `6.16 \times 10^{2}` 是否与全篇精度口径一致** —— 节内的 `62.8`(3 位) 与 `6.16×10²`(3 位) 自洽，但没有全篇口径可比 ⇒ 部分**无从判**。
5. **压力臂对照** —— GREEN 侧没有压力臂 ⇒ "纪律 + 压力"这一格**空缺**，无从判。
6. **`brief-S1` 内部的不自洽**（要点 12 带 `A_ceff`、要点 11 定义 `d_avg` 时已除过 `A_ceff`）—— GREEN 把反解式里的 `A_ceff` 删掉（`out-S1-g.md:125–129`）并写明了理由（自述）；节内确实自洽。**我登记这一处 brief 缺陷，但它不在本次七项指标之内，故不计入任何 0/1。**
