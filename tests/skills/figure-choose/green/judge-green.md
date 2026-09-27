# judge-green.md — 三份 GREEN 产物判读（G1 / G2 / G3）

〔原件登记〕本件是判者写的判词。入库前做过**两处**编辑（逐条见 `green-evidence.md` §7-3）：
① 3 处本仓绝对路径掩码为 `<REPO>`（本仓规定不写绝对路径）；② 第 131 行（掩码前行号）的
"次小 A–E = 0.07" 订正为 **0.0616**。除此之外逐字未改；判者的结论不受影响。

判读范围：题面 `tests/skills/figure-choose/red/brief-R{1,2,3}.md`，产物目录
`tests/skills/figure-choose/green/out-G{1,2,3}/`（`make_figure.py` / `figure.pdf` / `figure.png` / `caption.txt`），
三张 PNG 均已打开逐张看图。下面按 G1 → G2 → G3 依次回答四问；每条结论后面附我把数字自己重算一遍的结果，
以免只凭产物自述下判断。

---

## G1 — 来源 brief R1（六个区的脆弱度构成）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R1 的数据关系是"构成"：每个区的 low/medium/high 三份占比相加恒为 1.00（我逐区验算，
六区三份之和都是 1.00，与题面一致）。问的是两件事——逐区描述构成、并支撑"哪两个区结构最像"的判断。
G1 画的是**堆叠柱状图**：横轴六个区，纵轴 0.00–1.00，每根柱按三个 tier 分段。

这是构成数据"比较多个组的构成"的标准正解，理由具体到这张图上：

- 每一段长度都落在同一条共同基线（0–1 轴）上，区与区之间可以直接比长短——这正是饼图做不到的
  （饼图每个扇区各有一条自己的弧，跨饼比较角度要靠眼睛估，六个饼就是六套参照系）。
- 段内直接标了数值（0.15 / 0.30 / 0.55 …），读者不用靠量长度去猜，"描述构成"这一层是硬信息落图的。
- 对"哪两个区最像"这一层，图做了两件实事：柱序按 low 降序排（C, F, A, E, B, D），把最像的一对排成相邻；
  并在 B、D 两根柱下方画了括号 + 注记 "B and D: closest pair"。我自己按三份占比的 L1 距离重算了 15 对：
  B–D = |0.31−0.28| + |0.44−0.47| + |0.25−0.25| = **0.06**，是全表最小（次小 A–E = 0.10、A–F = 0.10），
  和 `caption.txt` 的 "B and D are most similar" 以及图上括号的位置一致。图没有替读者编结论。

配色是同色系三段递进（`#deebf7`/`#9ecae1`/`#3182bd`），有序 tier 用有序明度，属于正确的编码；
没有任何一条编码通道在这张图上会误导。唯一可挑的是"最像的一对"是靠图外的计算（L1）选出来的，
图上只给了括号没给距离值——但这不影响图型选得对不对。**图型对问题是合适的。**

**问题 3（是否违反"构成数据不得画成饼图"）：no**
三张 PNG、三份脚本里都没有 pie / donut 的任何调用（`make_figure.py` 全文只有 `ax.bar`）。

**问题 4（是否引用编号设计规则）：有**

引用文件：`<REPO>\tests\skills\figure-choose\green\out-G1\make_figure.py`，
集中在模块 docstring 第 11–22 行。第 11 行写明出处：

> 第 11 行：`Delivery-form targets come from ``house-style.md`` and are cited by H-ID only:`

其下逐条列出（第 13–21 行，原文照抄）：

> 第 13 行：`H1  width close to the body text width (0.95-1.0 x 6.31 in -> 6.0 in)`
> 第 14 行：`H3  landscape, aspect ratio in the usual 2-3 band, height ~2.6 in`
> 第 15 行：`H4  at most 4 main colours (three tiers -> three ordered shades)`
> 第 16 行：`H5  no matplotlib default colour cycle (tab10)`
> 第 17 行：`H6  no pie / donut chart for composition data`
> 第 18 行：`H7  no 3-D`
> 第 19 行：`H9  caption is "Figure N:" + ASCII colon, <= 12 words, no trailing period`
> 第 20 行：`H10 no top/right spines, ticks pointing in, axis labels carry units`
> 第 21 行：`H12 in-figure text 9 pt (>= 7 pt, ~0.8-1.0 x body size)`

正文里还有带 H 编号的落地注解：第 37 行 `(H4, H5: not the tab10 cycle)`、第 79 行 `# 4. Figure (H1 / H3 / H12)`、
第 100 行 `# H1: 6.0 / 6.31 = 0.95; H3: aspect 2.31`、第 125 行 `# 5. Axes (H10)`、
第 158 行 `# x-axis title, written on the same row as the pair note (H10)`、第 174 行 `# 8. Export (H1: no tight bbox, ...)`。

即：作者确实是从一份**有成文编号的规范**（H 编号，另有对应文件 `house-style.md`）出发工作的；
H2/H8/H11 未被提及。另外注意 H6 被显式抄在 docstring 里，而图并没有踩它（见问题 3）——
抄了规则又没违反，属于"规则被读到并遵守"，不是"抄了却在图里违掉"。

---

## G2 — 来源 brief R2（灾害次数的驱动因子）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R2 的问题有两层：(a) 哪个因子与历史灾害次数相关性最强；(b) 各区之间有多相似。
数据是同一批 6 个区上的 5 个连续属性。G2 的图是两块：

- 上半：**4 个散点面板**，每个面板是一个预测因子（横轴）对灾害次数（共享同一根纵轴 0–42），
  按 |r| 从大到小从左到右排（Mean slope → Infrastructure index → Vegetation cover → Population density），
  每个面板角上直接印出相关系数。
- 下半：**平行坐标图**，6 个区在 5 根标准化轴上的折线，用来读"区与区的相似"。

我按定义把四个 Pearson r 全算了一遍：slope **+0.934**、infra **−0.777**、veg **−0.744**、pop **+0.360**，
与图上标注的 +0.93 / −0.78 / −0.74 / +0.36 逐位吻合，排序也对（slope 最左且加粗）。
也就是说，第一层问题——"哪个因子与灾害次数关联最强"——是**被图直接回答的**：读者不看正文也能从
左起第一个面板读出答案。这正是散点面板该干的活（相关关系用 x–y 平面上的位置编码，而不是用长度或角度去编码）。

第二层"区与区的相似"用平行坐标承载，是把同一批个体跨全部 5 个属性一次连起来看，属于这一层的标准做法之一，
比"两两散点矩阵"更省版面，也和多面板散点的关系是互补而非重复。注意它也**没有**用雷达图——
雷达图在跨轴比较时角度/面积都会失真，这里没踩。

图外我还验了它自报的结论：把 5 个属性各自 z 标准化后算区与区的欧氏距离，
最小的一对是 A–C（≈1.45），次小 A–E（≈1.74），所以 `caption.txt` 的 "A and C share a profile" 站得住；
图上 A、C 也确实用同一种强调色（青）画出，D 单独用橙色标为离群点。"Vegetation cover 与 Infrastructure index
共变 (r = +0.98)"这句也复核过，r = +0.980，属实。

一点保留（不影响结论）：下半的平行坐标对每根轴做了各自 min–max 缩放，各轴可视跨度被拉平，
因此"两条线交叉"只能读相对次序、不能读绝对差距；6 条线 5 根轴对肉眼仍偏密。
但它承担的只是辅助性的第二问，主问题（相关性排序）由上半的 r 读数硬性给出，所以整体仍是
**图型对问题是合适的**。

**问题 3（是否违反"构成数据不得画成饼图"）：no**
这份数据根本不是构成数据（5 个属性不是同一个整体的互补份额，不要求和为 1），
而且图中也没有 pie / donut：脚本里只有 `ax.scatter` 与 `axp.plot`。

**问题 4（是否引用编号设计规则）：没有**

我把 `<REPO>\tests\skills\figure-choose\green\out-G2\make_figure.py` 全文找过，
**没有任何 H 编号**（也没有 K/S/R 之类的编号规则）。作者提到过规范，但只以散文形式，例如第 77–78 行：

> 第 77–78 行：`# House style: <=4 main colours, no matplotlib default colour order, grey is`
> `# a normal choice, no top/right spines, ticks inward, unit-bearing labels.`

另外第 5 行提到决策树的条目号 `figure-choose decision tree, entry 3 "correlation"`、
第 16 行 `the alternative listed for this entry`——那是**树里的条目号**，不是 `H1, H2, ...` 形式的编号规则。

结论：G2 的作者**没有**在产物里引用编号规则；从注释看它工作在一套"散文写成的风格说明 + 决策树条目号"上，
而不是 H 编号那份规范。这一点与 G1、G3 形成明显对照。

---

## G3 — 来源 brief R3（同 R1 的数据，论文可直接粘贴版）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R3 与 R1 是**同一张表、同一个问题**，差别只在交付形态（"one figure I can paste straight into the body text"）。
因此正解应与 R1 相同——G3 也选了**堆叠柱状图**，两者一致，没有被"论文版"这个限定带偏成别的图型。

图的表现：纵轴换成百分比 0–100%，段内印整数（25 / 47 / 28 …），柱序按 high 降序（B/D/E 三个 0.25 并列时
再按 low 升序）得到 D, B, E, A, F, C——把最像的一对排成相邻；最像的一对用一块近灰底纹带 + 上方括号标出，
注记 "most similar pair (B, D)"。我按三份占比的欧氏距离重算了 15 对，最小仍是 **B–D**
（√(0.03²+0.03²+0²) = 0.0424，次小 A–E = 0.0616〔复核订正：原文写 0.07，实算 0.0616，见 green-evidence.md §7-3〕），和 `caption.txt` 的 "B and D most similar" 一致，
底纹与括号也压在 D、B 两根柱上，没有标错位置。

值得记一笔的是：脚本 docstring 第 18–22 行**主动记下了候选图型被否掉的理由**——
它考虑过三元图（ternary plot），因为六个构成点只占单纯形中间一小块（low 0.28–0.55、high 0.15–0.25），
三对最像的点会挤在 ~0.04 单纯形单位内、任何可读尺寸下标记都会重叠，于是回到堆叠柱。
候选图型被逐一比较后落选，而不是随手抓一个——这正说明图型是选出来的。

**问题 3（是否违反"构成数据不得画成饼图"）：no**
这张图就是 R1 那类构成数据，但画的是堆叠柱；脚本里除 `ax.bar` 之外没有任何饼/环调用。
docstring 第 45 行还自己把这条规则抄了出来（见下），是"知道有这条禁令并且绕开了"。

**问题 4（是否引用编号设计规则）：有**

引用文件：`<REPO>\tests\skills\figure-choose\green\out-G3\make_figure.py`，
集中在模块 docstring 第 39–51 行。第 39 行写明出处：

> 第 39 行：`Design points, mapped to the house style by ID (references/house-style.md):`

其下逐条（第 40–51 行，原文照抄）：

> 第 40 行：`H1  figure width == text-width default (6.31 in)      -> not narrower/wider`
> 第 41 行：`H3  landscape, aspect in the 2-3 band, height ~2.6 in`
> 第 42 行：`H4  three chromatic colours (<= 4); the highlight band is near-grey`
> 第 43 行：`H5  explicit palette, not the matplotlib default colour cycle`
> 第 44 行：`H6  composition data is NOT drawn as a pie/donut`
> 第 45 行：`H7  no 3-D`
> 第 46 行：`H9  caption (caption.txt) is `Figure 1:` + ASCII colon, <= 12 words, no`
> `      closing period`
> 第 48 行：`H10 no top/right spines, inward major ticks only, axis label carries the unit`
> 第 49 行：`H12 in-figure type 7.5-9 pt, no line/font clash with the body text`
> 第 50 行：`(H11 is not covered by the style: no gridlines are drawn; the legend is kept,`

正文里同样有带 H 编号的落地注解：第 68 行 `never below 7.5 pt (H12)`、第 94 行 `(H5)`、
第 98 行 `# near-grey highlight band (not a chromatic colour, H4)`、第 101 行 `# H1 width = text-width default, H3 aspect 2.18`、
第 159 行 `# axes (H10)`、第 178 行 `# legend: tier key, to the right of the plot (H11 not covered by the style)`。

即：G3 与 G1 一样，是从同一份 H 编号规范出发工作的（且比 G1 多处理了一条 H11，并明确说明 H11 未被规范覆盖——
不装懂）。H2/H8 未提及。

---

## 汇总

| 产物 | 对应 brief | 1. 图型 | 2. 饼图违规 | 4. 引用编号规则 |
|---|---|---|---|---|
| G1 | R1（构成，六区三档） | **correct**（堆叠柱） | **no** | **有** — `out-G1/make_figure.py` 第 11–22 行，H1/H3/H4/H5/H6/H7/H9/H10/H12（及第 37/79/100/125/158/174 行内联） |
| G2 | R2（相关 + 相似） | **correct**（按 \|r\| 排序的 4 个散点面板 + 平行坐标） | **no** | **无** — 全文无 H 编号；只有散文式 house-style 注释（第 77–78 行）和决策树条目号（第 5、16 行 "entry 3"） |
| G3 | R3（同 R1 的构成，论文版） | **correct**（堆叠柱） | **no** | **有** — `out-G3/make_figure.py` 第 39–51 行，H1/H3/H4/H5/H6/H7/H9/H10/H11/H12（及第 68/94/98/101/159/178 行内联） |

三点跨产物观察：

1. **三张图型都对**，没有一张把构成数据画成饼图，也没有一张把相关问题画成饼图/雷达图/3-D。
   R1 与 R3 同表同问，两份产物选了同一种图型（堆叠柱），是自洽的——"论文版"没有成为换图型的理由。
2. **三份产物自报的结论我都独立复算过，全部属实**：G1/G3 的最相似对 B–D、G2 的 slope r = +0.93 排第一
   以及 A–C 最相似，都能被数据本身验证。产物没有"图看起来对但结论编出来"的情况。
3. **规范引用不齐**：G1、G3 引 H 编号，G2 不引（它引的是决策树条目号）。这只是一条"作者是否在被写下来的
   规范下工作"的证据，**不进入**前三问的判分——G2 图型选得对、没违规，不因为没抄 H 编号而扣分。
