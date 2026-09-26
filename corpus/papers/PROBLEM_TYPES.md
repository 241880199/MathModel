# 题型标注 · 官方赛题 2016–2026（Task 6b）

> **这是正式产物。** 本文件 2026-09-26 由 `tests/papers/recon/PROBLEM_TYPES-draft.md`
> **原样转正**（`git mv` 保住历史；正文语义一字未改，只去掉标题里的「草案」、补这一段定位说明）。
> 用户已于 2026-09-26 过闸门（「继续」+ 本轮解冻裁决）。
>
> **它是机读源**：`tools/papers/taxonomy.py` 的 `load_annotations()` 直接解析本文件
> （`SECTION` / `TABLE_ROW` / `TABLE_HEAD` / `QUOTED` 四条正则，见该模块）；
> 判据在 `tests/papers/verify_types.py`（T1–T8）。转正前的草案 blob 与转正记录见
> `tests/papers/recon/types-recon.txt` 的编者按。

**范围**：`corpus/官方原题/` 下 **67 份题面 PDF** —— 2016–2026 共 11 年 × 6 题 = **66**，
外加 `2023 ICM Problem Z` **一份**（它的处置见「例外登记 ②」）。**67 份逐份读题面**，
**没有一道是靠标题猜的**。

## 口径（每条都可复核）

1. **题面抽取**：`pdftotext -enc UTF-8 <pdf> -`（poppler；**不加 `-layout`**），行尾归一成 LF、
   分页符 `\x0c` 归一成 LF。实现见 `tools/papers/taxonomy.py:extract_text`，逐份的抽取产出见
   `tests/papers/recon/types-recon.txt` §2。
   **`-enc UTF-8` 是实测逼出来的**：不写它时，中文 Windows 上 `pdftotext` 按 **ANSI 代码页**输出，
   题面里的项目符号 `•`、弯引号 `’`、破折号 `–` 会被写坏成 `�`，**正确的引文反而定不到**。
2. **支撑句可定位（T2 的口径）**：引文与题面都做**格式归一化**后，引文必须是题面的子串。
   步骤：行尾归一 → **去项目符号**（`•` 一类）→ **空白折叠** → **引号折叠**（直/弯、单/双一律折成 `"`）
   → 大小写折叠；引文侧**另**去掉草案自己加的强调标记（`*`、`` ` ``）。
   报告里**同时**给出「严口径」的命中数（只做行尾归一 + 空白折叠 + 大小写折叠），差额**逐条列出**：
   读者能看见前两步到底做了多少事。这些步骤只动**排版与字形**，**动不了任何一个词**——
   所以它们不可能让「编造的句子」变成能命中的句子，而那正是 T2 要守的东西。
3. **标签**：`L1 名 · L2 名`（` · ` 分隔），两级都必须**逐字**命中
   `tools/papers/vocab/problem_types.txt`（T4）。**多标签、不设上限**（用户 2026-09-26 定案），
   每个标签标 **`核心`** 或 **`附带`**：
   * `核心` ＝ 题干的**要求句**（`Requirement(s)` / `Your task` / 问题句）明确要求做这件事；
   * `附带` ＝ 该要素在题面**出现**（背景、数据说明、可选提示），但不是被要求交付的东西。
   **不设上限，但有下界**：每题至少一个 `核心`（T5）。
4. **每个标签必须附题面支撑句**（英文原句，可复核）。引文里若需要引号，**一律写单引号**
   （归一化会把直/弯、单/双折成同一个字符）；**引文内不得出现直双引号**——它在本文件里是片段的定界符。
5. **层级止于「任务形态」**，不细到方法名；方法活在 `models.txt`。T3 保证两级名字都**不与词表同名**
   （否则配对退化成同义反复）。
6. **`数据形态`**（受控枚举，逐字取自任务书 §一 第 5 条）：`无数据(纯机理/假设)` · `时序` ·
   `截面` · `面板` · `空间/地理` · `网络` · `文本/文献` · `混合`。本行**第一个词必须命中该枚举**；
   括号里补的是**该题具体是什么数据**（只作说明，不进判据）。
7. **`场景`**：自建，**只作检索标签，与模型选择无关**（用户 2026-09-26：*「'考古/旅游'等领域都只是
   一个场景，实际模型的确立并不与场景有关」*）。**配对的推理轴只有两条：数学任务 × 数据形态。**

## 与 2025 样板的偏离（逐条列出，供用户裁决）

| # | 偏离 | 为什么 |
| :-- | :-- | :-- |
| 1 | 字段名用 **`场景`**（样板正文那一行写的是 `领域`） | 用户在 2026-09-26 把这条轴定案改名为「场景」（任务书 §一 第 6 条），样板的**约定**段也写「场景（原'领域'轴）」，只有正文的字段名没跟着改。两处只能取一个，取定案。 |
| 2 | **`4.6 系统动力学/反馈结构` → `4.6 反馈结构与动态演化`** | T3：`系统动力学` 是 `models.txt` 的词条（`system dynamics`）。**标签名带模型名 = 配对退化成同义反复**。**这是样板里唯一一处必须改的分类法名字，请用户确认**（改名的替代方案是删掉词表里 `系统动力学` 那个变体，但那会动 Task 6 的放行产物链，本任务无权）。 |
| 3 | `4.1 物理/化学机理(ODE/PDE)` → `4.1 物理/化学机理建模` | T3：`ODE`/`PDE` 是词表变体（词表 86/87 行）。 |
| 4 | `4.3 随机仿真/蒙特卡洛` → `4.3 随机仿真/概率模拟`；`4.4 元胞自动机/多智能体` → `4.4 局部规则演化/个体交互仿真`；`5.1 假设检验/显著性` → `5.1 差异显著性检验`；`8.1 结构与中心性` → `8.1 网络结构与重要性`；`8.2 网络流/路由` → `8.2 流量分配/路由` | 同上，全部是 T3 逼出来的改名。撞车的那个词逐个写在 `problem_types.txt` 的条目注释里。 |
| 5 | 表格第一列里写 **`核心`/`附带` 标记**（`` `核心` **L1 · L2** ``） | 样板**正文的表**没有标记列（标记只在「去掉上限后的重扫结果」那张附表里出现），而约定第 2 条要求**每条**都标。不写进表就无法机读，T4/T5 都要判它。 |
| 6 | **2025 F 的一处引文订正** | 样板写的是 `identify parts of a policy or law that are particularly effective (or ineffective)`，题面原文是 `… (or particularly ineffective)`。**T2 实测把这处抓出来了**（少一个 `particularly`）。按约定第 3 条「英文原句，可复核」订正为原文。 |
| 7 | 2020 A 一题**无标题、无标签、无抽象** | 该件**没有文本层**，给不出可定位的支撑句（见「例外登记 ①」）。 |
| 8 | 2021 C 一题**不写标题** | 该件的抽取把**标题与正文首句排在同一行**（`2021 MCM Problem C: Confirming the Buzz about Hornets In September 2019, a colony of …`），抽取口径下**切不出**标题。按「不猜、不目视」的纪律，这一行**留空**并在此登记。 |
| 9 | 样板正文里的 **「论文侧（… Key words）」预览行本轮不抄** | 那一行是**阶段 2 的配对材料**（样板约定第 7 条自己写着「配对预览」）。而且本轮的 66 道题里**只有 2025 有论文产物**（`corpus/papers/` 只覆盖 2025 那 43 份），抄进来会造成「别人也验过」的**不对称假象**。 |
| 10 | 样板 2025 C 把**两个标签写在一格**（`1.2 回归/相关预测（含 1.5 零膨胀/受限计数预测）`），本草案**拆成两行** | T4 要求**每个标签逐字命中**分类法；一行两标签无法判，且会让「标签数」这种统计量失真。 |
| 11 | 样板 2025 D/F 的 `数据形态` 是 `网络 + 官方提供的车流量附件`、`面板/截面 + 政策文本` 这类**组合写法**，本草案**归一成单个枚举值**、把组合信息移进括号 | T4 判「本行第一个词必须命中受控枚举」；`面板/截面` 这种写法既不是枚举值、也无法判。2025 A/B/C/E 的样板写法（`无数据（…）`）则**原样保留**，只把枚举值补全为 `无数据(纯机理/假设)`。 |

## 例外登记（**不静默**）

### ① `2020 MCM Problem A` —— 题面件**没有文本层**（标注状态：**读不出**）

* 抽取口径下只得 **25** 个字符 / **2** 行，全部是第 2 页杂志名那两行斜体（`Hook Line and Sinker`）；
  用 `fitz.get_text()` **独立**复核得 **22** 个字符（同一个东西）。
* 原件内容流里 `BT`/`Tf`/`Tj`/`TJ` 操作符合计 **4** 个，而**填充路径 3922 条**——正文是**画**出来的
  （`Microsoft: Print To PDF` 的产出，字形被转成了矢量轮廓），不是**排**出来的。
* ⇒ **无法给出可定位的支撑句** ⇒ 按「读不出」登记：**不标标签、不写抽象、不靠标题猜题意**。
* 两条**互相独立**的探针（抽取文本的行数；内容流的文本操作符数）都判它无文本层；
  全 67 份里**只有这一份**落在阈值的另一侧——次低的题是 **5 行 / 102 个操作符**
  （见 `recon/types-recon.txt` §2）。阈值取在**实测空档**里，不是拍的整数。
* **它在 66 题里算一道**：T1 的双边等式按 **67** 判（含它），T5 把它登记为「读不出」，
  **它的未标注不会被摊到别的题上**，也不会被记成「不适用」（任务书 §二 T5 明令）。

### ② `2023 ICM Problem Z` —— **算第 67 道，已标注**

* 处置：**计入并标注**。理由：它是 COMAP 自己发布的**完整题面**（有 `Requirement` 段、有 25 页提交规则、
  页脚 `©2023 by COMAP`），与同年 A–F 同构；把它排除会让 `n_annotations == 题面文件数`（T1 的**双边等式**）
  不成立，而那条等式的意义正是「**有题面就必须有标注**」。`corpus/官方原题/PROVENANCE.md` 也登记它为
  *「COMAP 当年额外发布的题，是真件，非错文件」*。
* **不声称**它在当年赛制里的地位（是否正式比赛题、是否替代某题）——那超出**已查范围**；
  按教训 4.5（「我没找到」≠「它不存在」）只登记上面这些**已查**事实。
* 后果说清：在「11 年 × 6 题」这个口径下它是**附加题**。排序按 `(年, 题号)`，故它排在 `2023 F` 之后。

---

## 逐题标注

### 2016 A — A Hot Bath

**问题抽象**：给一个只有单龙头、无二次加热与循环的浴缸建「水温随**空间与时间**演化」的物理模型，
并以它求「在不浪费太多水的前提下，把水温尽量均匀地维持在初始温度附近」的注水策略。
**结构化**：`要求`＝水温的时空模型 + 最优注水策略 + 该策略对浴缸形状/体积、人的形状/体积/体温、人的动作的依赖程度 + 泡泡浴添加剂的影响 ｜ `已知`＝单龙头 + 溢流排水；几何与人体参数**自设**（题面不给数据） ｜ `约束/不确定性`＝温度要在**空间上**也均匀、且尽量贴近初始温度，同时**不能浪费太多水**；人的动作与添加剂会改变换热与混合

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Develop a model of the temperature of the bathtub water in space and time"* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"determine the best strategy the person in the bathtub can adopt to keep the temperature even throughout the bathtub and as close as possible to the initial temperature without wasting too much water"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"determine the extent to which your strategy depends upon the shape and volume of the tub, the shape/volume/temperature of the person in the bathtub, and the motions made by the person in the bathtub"* |

**数据形态**：无数据(纯机理/假设)（几何、人体与注水参数全部自设）｜**场景**：日常生活 / 传热

### 2016 B — Space Junk

**问题抽象**：为「私人公司把清除轨道碎片当作商业机会」建**含时间**的成本-风险-收益模型，
在若干技术方案**及其组合**之间评估机会是否存在，并给出方案比较与推荐（或替代方案）。
**结构化**：`要求`＝各方案与组合的成本/风险/收益估计 + 一组 "What if?" 情景 + 「机会是否存在」的判断 + 方案比较与具体推荐 ｜ `已知`＝碎片规模的量级估计（50 万件以上）与已提出的几类清理手段（水射流、高能激光、清扫卫星）；**无附件数据集** ｜ `约束/不确定性`＝碎片尺寸/质量跨度极大、速度高难捕获；成本与效果只能估计；组合方案的空间很大

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Your model should include quantitative and/or qualitative estimates of costs, risks, benefits, as well as other important factors"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"provide a comparison of the different options for removing debris, and include a specific recommendation as to how the debris should be removed"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"be able to explore a variety of important 'What if?' scenarios"* |
| `核心` **9 决策与博弈 · 9.3 风险与效用** | *"determine whether an economically attractive opportunity exists or no such opportunity is possible"* |
| `附带` **3 优化 · 3.4 动态与随机** | *"Develop a time-dependent model to determine the best alternative or combination of alternatives"* |

**数据形态**：无数据(纯机理/假设)（题面只给量级估计，无附件数据集）｜**场景**：航天 / 商业投资

### 2016 C — The Goodgrant Challenge

**问题抽象**：在已有其他大型资助者占据部分学校的前提下，把一笔固定年度捐赠分配到候选学校集合上，
使「学生表现提升」的期望最大——要同时给出入选学校名单与优先级、每校的投入额与投入年限、
以及该捐赠的 ROI 定义。
**结构化**：`要求`＝最优投资策略（学校名单 + 优先级 + 每校金额 + 回报 + 年限）+ 适合慈善机构的 ROI 定义 ｜ `已知`＝IPEDS 与 College Scorecard 两个数据集（附件 `ProblemCDATA.zip`，题面要求只用其中「有意义且可辩护的子集」） ｜ `约束/不确定性`＝不得与其他大型资助者重复投入；ROI 对慈善机构需重新定义（不能直接用商业口径）；数据只覆盖部分学校、部分指标

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.2 离散/组合** | *"develop a model to determine an optimal investment strategy that identifies the schools, the investment amount per school"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"a 1 to N optimized and prioritized candidate list of schools you are recommending for investment"* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"an estimated return on investment (ROI) defined in a manner appropriate for a charitable organization such as the Goodgrant Foundation"* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"they do not want to duplicate the investments and focus of other large grant organizations"* |
| `附带` **1 预测 · 1.2 回归/相关预测** | *"based on each candidate school's demonstrated potential for effective use of private funding"* |

**数据形态**：截面（一批评分卡指标 × 一批学校）｜**场景**：教育 / 慈善投资

### 2016 D — Measuring the Evolution and Influence in Society's Information Networks

**问题抽象**：为「信息价值 × 传播速度」的关系建模型，用五个历史时期的数据检验它、外推到 2050 年的
网络关系与容量，并回答「公众意见如何被信息网络改变」。
**结构化**：`要求`＝(a) 信息流与「什么算新闻」的模型 (b) 用历史数据验证并预测今天 (c) 2050 年的网络关系与容量 (d) 舆论如何被网络改变 (e) 信息价值/初始偏见/信息形式/网络拓扑各起什么作用 ｜ `已知`＝五个时期（1870s/1920s/1970s/1990s/2010s）的媒介环境描述 + 一组样本数据源链接（报纸发行量、收视调查等） ｜ `约束/不确定性`＝历史数据缺失且异质；「信息价值」需自定义；题干要求报告假设与所用数据

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.3 传播与级联** | *"Develop one or more model(s) that allow(s) you to explore the flow of information and filter or find what qualifies as news"* |
| `核心` **8 网络与图 · 8.1 网络结构与重要性** | *"the information finding its way to influential or central network nodes that accelerate its spread through social media"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Use your model to predict the communication networks' relationships and capacities around the year 2050"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"model how public interest and opinion can be changed through information networks in today's connected world"* |
| `附带` **2 评价与排序 · 2.1 指标体系构建** | *"Determine how information value, people's initial opinion and bias, form of the message or its source, and the topology or strength of the information network in a region, country, or worldwide could be used to spread information"* |

**数据形态**：混合（自采历史发行量/收视数据 + 文献叙述）｜**场景**：传媒 / 社会史

### 2016 E — Are we heading towards a thirsty planet?

**问题抽象**：为一个区域建「供水能力」的度量模型（含供需两端的动态因素），选一个缺水区域解释其缺水
成因，预测 15 年后的水情，再设计一套干预方案并用模型评估它对本地与周边的影响。
**结构化**：`要求`＝区域供水能力的度量 + 选定区域的物理/经济缺水解释 + 15 年后的水情及对居民的影响 + 干预方案及其对周边与水生态的外溢影响 + 干预后的前景 ｜ `已知`＝UN 缺水地图与一组公开数据源（UNEP / FAO / World Bank 等链接） ｜ `约束/不确定性`＝干预必然外溢到周边与整个水生态；供需驱动因素随时间变化；15 年与更远处的预测不确定

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Develop a model that provides a measure of the ability of a region to provide clean water to meet the needs of its population"* |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"use your model from Task 1 to show what the water situation will be in 15 years"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"design an intervention plan taking all the drivers of water scarcity into account"* |
| `附带` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Be sure to detail the strengths and weaknesses of your model"* |
| `附带` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"The supply of water must take into account the physical availability of water (e.g., natural water source, technological advances such as desalination plants or rainwater harvesting techniques)"* |

**数据形态**：混合（区域供需的公开统计 + 文献）｜**场景**：水资源 / 公共政策

### 2016 F — Modeling Refugee Immigration Policies

**问题抽象**：为六条难民路线的「最优流动」建模（含容量、可达性、安全与资源约束），
再在动态变化与外部冲击下设计一套支持性政策并检验其韧性。
**结构化**：`要求`＝(1) 危机的度量与参数 (2) 六条路线上的最优流动模型 (3) 动态容量与资源前置 (4) 支持最优流动的政策集合 (5) 外生事件的冲击与政策韧性 (6) 规模放大 10 倍后的可扩展性 ｜ `已知`＝六条路线的描述与 2015 年的统计数字（71.5 万份庇护申请等）+ 一组在线参考链接 ｜ `约束/不确定性`＝容量会先被最受欢迎的目的地填满并形成**级联**；政治/安全外生冲击（如巴黎恐袭）会整体改变参数；规模放大后可能出现新约束

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"Create a model of optimal refugee movement that would incorporate projected flows of refugees across the six travel routes"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Your UN commission has asked you to consider and prioritize the health and safety of refugees and of the local populations"* |
| `核心` **3 优化 · 3.4 动态与随机** | *"Identify the environmental factors that change over time; and show how capacity can be incorporated into the model to account for these dynamic elements"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"propose a set of policies that will support the optimal set of conditions ensuring the optimal migration pattern"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"explain the sensitivities of your model to these dynamics"* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"the most desired destinations will reach maximum capacity the quickest, creating a cascade effect altering the parameters for the patterns of movement"* |
| `附带` **4 机理建模与仿真 · 4.4 局部规则演化/个体交互仿真** | *"Transportation availability, safety of routes and access to basic needs at destination are considered by each individual or family in this enormous migration"* |

**数据形态**：混合（题面给量级与链接，需自采/自设）｜**场景**：难民 / 国际政策

### 2017 A — Managing The Zambezi River

**问题抽象**：在「修 / 重建 / 拆除并改建多座小坝」三条路线之间为水坝管理方做成本-效益评估，
并把选定的那条（拆除改建）做成**可执行的调度规则**（含极端水情的处置）。
**结构化**：`要求`＝三个方案的成本/效益概览 + 对方案 (3) 的详细分析（新坝群的**数量与位置**，且要维持原坝的水管理能力）+ 兼顾安全与成本的**流量调度策略** + 极端丰枯水情的处置指引 + 河段暴露时长与位置的限制 ｜ `已知`＝Kariba 坝的工程背景与 2015 年风险报告；洪水/枯水的水文量级**由队伍自设或引用** ｜ `约束/不确定性`＝新坝群必须**至少**维持原坝的防洪与供水能力；极端水情（最大/最小预期泄量）的处置必须给出；河段受损暴露有时长与位置约束

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"a brief assessment of the three options listed, with sufficient detail to provide an overview of potential costs and benefits associated with each option"* |
| `核心` **3 优化 · 3.6 选址与布局** | *"Your analysis must support a recommendation as to the number and placement of the new dams along the Zambezi River"* |
| `核心` **3 优化 · 3.5 调度与配置** | *"you should include a strategy for modulating the water flow through your new multiple dam system that provides a reasonable balance between safety and costs"* |
| `附带` **3 优化 · 3.4 动态与随机** | *"your strategy should provide guidance to the ZRA managers that explains and justifies the actions that should be taken to properly handle emergency water flow situations"* |
| `附带` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"This new system of dams should have the same overall water management capabilities as the existing Kariba Dam"* |

**数据形态**：无数据(纯机理/假设)（题面只给工程背景，水文量级自设/引用）｜**场景**：水利 / 基础设施

### 2017 B — Merge After Toll

**问题抽象**：设计收费站下游「B 条出口车道→L 条行车车道」的**几何形状与并流方式**，
使通行能力、事故风险与造价三项同时合理——题面明确要求**不是**评估现有设计，而是给出更好的方案。
**结构化**：`要求`＝B→L 收窄区的形状/尺寸/并流规则设计 + 轻/重交通下的性能 + 混入自动驾驶车后的变化 + 不同收费闸机（人工/零钱/电子）比例的影响 ｜ `已知`＝车道数与收费口数的关系（B > L）、`L` 与 `B` 为参数；无数据附件 ｜ `约束/不确定性`＝事故预防、吞吐量（辆/小时）、土地与造价三者冲突；自动驾驶车比例未知

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.2 逆向设计** | *"The point is to determine if there are better solutions (shape, size, and merging pattern) than any in common use"* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"Determine the shape, size, and merging pattern of the area following the toll barrier in which vehicles fan in from B tollbooth egress lanes down to L lanes of traffic"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"accident prevention, throughput (number of vehicles per hour passing the point where the end of the plaza joins the L outgoing traffic lanes), and cost"* |
| `附带` **1 预测 · 1.3 情景与概率预测** | *"How does your solution change as more autonomous (self-driving) vehicles are added to the traffic mix?"* |

**数据形态**：无数据(纯机理/假设)｜**场景**：交通 / 道路工程

### 2017 C — "Cooperate and navigate"

**问题抽象**：为「网联自动驾驶车与人工驾驶车混流」建交通流模型，回答随自动驾驶比例升高时
通行能力如何变化、是否存在均衡与临界点，并据此给出车道专用化等政策建议。
**结构化**：`要求`＝含车道数/交通量/自动驾驶比例的车流模型 + 自动驾驶车之间及其与人工车的相互作用 + 把模型应用到附件 Excel 的实际路网数据 + 10%/50%/90% 三档比例的效果 + 均衡与临界点 + 是否应设专用道及其他政策 ｜ `已知`＝附件地图与 Excel 路网数据（I-5/I-90/I-405/SR-520 的车道、交通量、里程标）；题面另给若干背景常数（8% 日交通量在高峰、限速 60 mph 等） ｜ `约束/不确定性`＝题面规定数据冲突时以题面数据为准；自动驾驶车的混流行为「尚未被充分理解」；政策结论依赖比例的假设

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"Your answer should include a model of the effects on traffic flow of the number of lanes, peak and/or average traffic volume, and percentage of vehicles using self-driving, cooperating systems"* |
| `核心` **9 决策与博弈 · 9.2 博弈与策略** | *"Do equilibria exist? Is there a tipping point where performance changes markedly?"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"how do the effects change as the percentage of self-driving cars increases from 10% to 50% to 90%?"* |
| `附带` **9 决策与博弈 · 9.4 机制/规则设计** | *"Under what conditions, if any, should lanes be dedicated to these cars?"* |

**数据形态**：空间/地理（路网几何 + 分段交通量；附件 Excel）｜**场景**：交通 / 公共政策

### 2017 D — Optimizing the Passenger Throughput at an Airport Security Checkpoint

**问题抽象**：把机场安检流程建成分区排队/服务系统，找出瓶颈，提出两套以上改造方案并量化它们对
吞吐量与等待时间**方差**的影响，同时把不同文化下的旅客行为差异做成敏感性分析。
**结构化**：`要求`＝(a) 旅客流过安检点、识别瓶颈 (b) ≥2 套流程改造方案及其量化影响 (c) 文化/旅客风格差异的敏感性分析 (d) 政策与流程建议 ｜ `已知`＝A/B/C/D 四区的流程描述、Pre-Check 占比（约 45%）与 1:3 车道比；**附件 Excel 给了各步骤的实测数据** ｜ `约束/不确定性`＝安全标准不得降低；等待时间**方差**（不只是均值）要降；文化差异可实测也可模拟

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.5 离散事件** | *"Develop one or more model(s) that allow(s) you to explore the flow of passengers through a security check point and identify bottlenecks"* |
| `核心` **3 优化 · 3.5 调度与配置** | *"Develop two or more potential modifications to the current process to improve passenger throughput and reduce variance in wait time"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Consider how cultural differences may impact the way in which passenger's process through checkpoints as a sensitivity analysis"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"Propose policy and procedural recommendations for the security managers based on your model"* |

**数据形态**：截面（每名旅客在各步骤的耗时记录；附件 Excel）｜**场景**：航空 / 公共安全

### 2017 E — Sustainable Cities Needed!

**问题抽象**：先定义「城市精明增长成功度」的度量，再用它评估两座城市（不同大洲）的现行增长规划、
设计新的增长规划、并按潜力排序其中的举措。
**结构化**：`要求`＝(1) 成功度指标 (2) 两城现行规划按该指标的评估 (3) 新增长规划及其评估 (4) 规划内举措按潜力的排序与两城对比 (5) 人口再增 50% 时规划如何支撑 ｜ `已知`＝精明增长的十条原则与「三个 E」；两座城市的社会/地理数据**自采** ｜ `约束/不确定性`＝城市须为 10–50 万人的中等城市且位于两个大洲；指标要兼顾经济/社会/环境三方面并适配城市自身条件

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Define a metric to measure the success of smart growth of a city"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"rank the individual initiatives within your redesigned smart growth plan as the most potential to the least potential"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Compare and contrast the initiatives and their ranking between the two cities"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Suppose the population of each city will increase by an additional 50% by 2050, explain in what way(s) your plan supports this level of growth?"* |

**数据形态**：混合（城市统计自采 + 规划文献）｜**场景**：城市规划 / 公共政策

### 2017 F — Migration to Mars: Utopian Workforce of the 2100 Urban Society

**问题抽象**：为火星首批 1 万人聚落设计「收入—教育—平等」三维的社会-经济-教育系统模型，
在冲突目标间做权衡，并给出政策建议与长期可持续性检验。
**结构化**：`要求`＝(1) 三因子的参数与产出指标 (2) 抽取/合成 1 万人样本人口 (3) 三因子整合模型与关键相互依赖 (4) 分群后的模型修正 (5) 对后续移民批次与 100 年尺度的敏感性 (6) 地球毁灭情景下的鲁棒性 (7) 给 LIFE 局长的政策建议 ｜ `已知`＝PUMS 人口微观数据的下载与抽样说明（R/MATLAB 代码链接）；人口可**合成** ｜ `约束/不确定性`＝两个目标（GDP 与幸福感）可能对立；分群后可能不再最优；100 年尺度的参数会变

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Create metrics that you will use to evaluate whether the system is meeting its objective by identifying and defining the critical parameters for each of the three factors"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"these two goals can be in opposition, so the policy recommendation has to consider balancing factors"* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"When integrating these three factors, what are the critical interdependencies among the parameters?"* |
| `核心` **4 机理建模与仿真 · 4.3 随机仿真/概率模拟** | *"generate a sample population of 10,000 people to emigrate to Mars. Extract data from a census dataset (link to one is provided below) or synthesize one."* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"Determine the optimal minimum wage and salary distribution to best manage the tension between wellbeing (higher quality of life) and support for those less equipped to provide labor services"* |
| `附带` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"How sensitive is your model to the population selection for various migration phases?"* |

**数据形态**：截面（PUMS 个人级数据，或自造 1 万人样本）｜**场景**：社会制度 / 航天移民

### 2018 A — Multi-hop HF Radio Propagation

**问题抽象**：为 HF 电波经电离层—海面多次反射的传播建物理模型，算湍流海面与平静海面对首次反射强度
的差异，并求信号在多跳后跌破可用信噪比阈值前能走的最多跳数；再把模型推广到船载移动接收。
**结构化**：`要求`＝Part I 海面反射模型 + 湍流/平静对比 + 最大跳数；Part II 山地/崎岖地形对比；Part III 船载移动接收；Part IV 给 IEEE 的短评 ｜ `已知`＝HF 频段、100 瓦恒载信号、SNR 阈值 10 dB、MUF 随季节/日/太阳活动变化等物理背景；**无数据附件** ｜ `约束/不确定性`＝海洋湍流改变海水的电磁梯度、介电常数与反射面高度/角度，且浪高/浪形/浪频快速变化；反射损耗只有经验关系

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Develop a mathematical model for this signal reflection off the ocean"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"How do your findings from Part I compare with HF reflections off mountainous or rugged terrain versus smooth terrain?"* |
| `附带` **2 评价与排序 · 2.5 分级/阈值划定** | *"what is the maximum number of hops the signal can take"*；*"(SNR) threshold of 10 dB"* |
| `附带` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"It has been found empirically that reflections off a turbulent ocean are attenuated more than reflections off a calm ocean"* |

**数据形态**：无数据(纯机理/假设)｜**场景**：通信 / 海洋

### 2018 B — How Many Languages?

**问题抽象**：用影响语言消长的诸因素建模全球语言使用者的**分布随时间的演变**，预测 50 年后
母语者与总使用者数、前十名是否易位、地理分布如何变，并据此为客户公司选择新设办公室的地点。
**结构化**：`要求`＝Part I 语言分布的时间模型 + 50 年预测 + 前十是否被替换 + 地理分布变化；Part II 六个新办公室的选址与语言 + 「少于六个是否更好」的分析；Part III 给 COO 的备忘录 ｜ `已知`＝附件《按总使用者排序的语言表》（Ethnologue 2017，26 种 5000 万人以上语言）；背景给出因素清单 ｜ `约束/不确定性`＝须忽略小概率高冲击事件（如小行星撞击）；语言统计口径本身不可靠（题面明说「totals are generally not reliable」）；迁移与政策因素难以量化

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"Based on projected trends, and some or all of these influences and factors, model the distribution of various language speakers over time"* |
| `核心` **3 优化 · 3.6 选址与布局** | *"where might you locate these offices and what languages would be spoken in the offices?"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Given the global population and human migration patterns predicted for the next 50 years, do the geographic distributions of these languages change over this same period of time?"* |
| `附带` **2 评价与排序 · 2.3 排序规则/权重设计** | *"Do you predict that any of the languages in the current top-ten lists (either native speakers or total speakers) will be replaced by another language?"* |
| `附带` **9 决策与博弈 · 9.1 多准则决策** | *"Would your recommendations be different in the short term versus the long term?"* |

**数据形态**：截面（附件语言表 + 人口/迁移统计）｜**场景**：语言 / 企业选址

### 2018 C — Energy Production

**问题抽象**：用 50 年 × 605 变量的州级能源数据为四州建立「能源画像」，刻画其演变、比较谁最
「清洁可再生」、并在无政策变动假设下预测 2025 与 2050 的画像，据此为四州能源联盟设定目标。
**结构化**：`要求`＝Part I 各州能源画像 + 演变刻画 + 谁「最好」及其判据 + 无政策情景的 2025/2050 预测；Part II 目标与至少三项行动；Part III 给州长们的备忘录 ｜ `已知`＝附件 `ProblemCData.xlsx`（seseds 工作表 605 个变量 × 50 年 × 4 州，msncodes 给变量定义） ｜ `约束/不确定性`＝「最好」的判据必须自己给并论证；1960–2009 的历史区间固定；无政策情景是**假设**

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"create an energy profile for each of the four states"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Determine which of the four states appeared to have the 'best' profile for use of cleaner, renewable energy in 2009. Explain your criteria and choice."* |
| `核心` **1 预测 · 1.1 时序外推** | *"predict the energy profile of each state, as you have defined it, for 2025 and 2050 in the absence of any policy changes"* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"determine renewable energy usage targets for 2025 and 2050 and state them as goals for this new four-state energy compact"* |

**数据形态**：面板（4 州 × 50 年 × 605 变量；附件）｜**场景**：能源 / 州际政策

### 2018 D — Out of Gas and Driving on E (for electric, not empty)

**问题抽象**：为「全电动化」的国家设计充电网络的**终局架构与建设时间线**：终局要给出充电站的数量、
位置与城乡分布，时间线要给出从零到全面电动化的推进节奏与关键因子。
**结构化**：`要求`＝Task 1 特斯拉充电网络现状与「多少站、如何城乡分布」；Task 2 选定国家的终局布点 + 从零开始的演进方案 + 全面电动化的时间线；Task 3 五国地理/人口/财富差异下的可迁移性与分类系统；Task 4 新兴技术的影响；Task 5 给国际能源峰会的单页材料 ｜ `已知`＝特斯拉两类充电桩的说明与链接、可选国家（韩国/爱尔兰/乌拉圭）与对照国家清单；**无附件数据集** ｜ `约束/不确定性`＝只聚焦乘用个人车辆；建桩与购车的先后顺序是策略选择；各国地理与财富差异使方案不可直接照搬

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.6 选址与布局** | *"Determine the optimal number, placement, and distribution of charging stations"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"what should the network look like when electric vehicles represent 10% of all cars, 30% of all cars, 50% of all cars, and 90% of all cars?"* |
| `核心` **3 优化 · 3.4 动态与随机** | *"what is the timeline you propose for the full evolution to electric vehicles in your country?"* |
| `核心` **7 分类与聚类 · 7.1 监督分类/识别** | *"Discuss the feasibility of creating a classification system that would help a nation determine the general growth model they should follow"* |
| `附带` **3 优化 · 3.5 调度与配置** | *"Should the country build all city-based chargers first, or all rural chargers, or a mix of both?"* |

**数据形态**：空间/地理（站点分布 + 各国地理/人口密度）｜**场景**：能源 / 交通基础设施

### 2018 E — How does climate change influence regional instability?

**问题抽象**：建一个同时刻画「国家脆弱度」与「气候变化冲击」的模型，把国家划成脆弱/易感/稳定三档，
并在给定案例国上度量气候变化如何（直接或间接）增加脆弱性、干预能挽回多少。
**结构化**：`要求`＝Task 1 脆弱度 + 气候冲击的联合模型与三档判定；Task 2 前十脆弱国的个例分析；Task 3 非前十国 + 临界点定义与预测；Task 4 可减轻风险的干预及其总成本；Task 5 模型能否用于城市/大陆尺度 ｜ `已知`＝脆弱国家指数（FSI）与其数据链接、世界银行脆弱情境清单、若干学术文献 ｜ `约束/不确定性`＝环境压力**单独**不必然引发冲突（题面明说），须与弱治理、社会撕裂共同作用；临界点需自己定义；干预成本只能估计

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"Your model should identify when a state is fragile, vulnerable, or stable."* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Develop a model that determines a country's fragility and simultaneously measures the impact of climate change."* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"determine how climate change may have increased fragility of that country"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"see in what way and when climate change may push it to become more fragile"* |
| `附带` **9 决策与博弈 · 9.4 机制/规则设计** | *"Use your model to show which state driven interventions could mitigate the risk of climate change and prevent a country from becoming a fragile state."* |

**数据形态**：面板（国家 × 年份的脆弱度与气候指标）｜**场景**：气候 / 国家安全

### 2018 F — Cost of Privacy

**问题抽象**：为「个人隐私/个人信息的货币价值」建定价模型：先定风险与价值的参数体系，
再对至少三个领域（社交媒体、金融交易、医疗记录）给出定价结构，并讨论监管与数据共享的网络外部性。
**结构化**：`要求`＝Task 1 隐私保护的「价格点」与风险参数体系；Task 2 三领域定价模型；Task 3 面向个人/群体/国家的定价体系与供需机制；Task 4 模型的假设与约束（含监管与基本人权）；Task 5 代际差异；Task 6 数据共享的网络效应与连带责任；Task 7 大规模数据泄露的冲击与赔偿；Task 8 政策备忘录 ｜ `已知`＝**无附件数据集**；题面给大量情境与权衡描述 ｜ `约束/不确定性`＝风险的度量高度主观且随群体与领域变化；数据是「公共品」还是「私人财产」本身有争议；泄露与级联事件难以估计

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **9 决策与博弈 · 9.3 风险与效用** | *"Develop a price point for protecting one's privacy and PI in various applications."* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"the set of parameters and measures that would need to be considered to accurately model risk"* |
| `核心` **3 优化 · 3.4 动态与随机** | *"Consider introducing a dynamic element to your model by introducing the variations over time in human decision-making"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"Should the government regulate this information or is it better left to privacy industry or the individual?"* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"Are there good ways to capture the network effects of data sharing?"* |
| `附带` **5 统计推断与因果 · 5.1 差异显著性检验** | *"Are there generational differences in perceptions of the risk-to-benefit ratio of PI and data privacy?"* |

**数据形态**：无数据(纯机理/假设)（题面不给数据集；参数与企业需自设/自采）｜**场景**：隐私 / 公共政策

### 2019 A — Game of Ecology

**问题抽象**：为三条虚构巨龙建**生态与能量**模型：算它们的能量支出与热量需求、需要多大面积与多大规模的
聚落来供养，并回答气候带迁移（干旱/温带/寒带）对资源需求的影响。
**结构化**：`要求`＝生态影响与需求 + 能量支出与卡路里需求 + 所需面积 + 支撑龙的社区规模 + 气候条件的重要性 + 给原著作者的两页信 + 该建模方法在现实问题上的迁移 ｜ `已知`＝题面给的生物学基线（孵化约 10 kg、一年后 30–40 kg、终生生长）；其余假设自设 ｜ `约束/不确定性`＝生理参数（代谢、飞行能耗、喷火）全部是自设假设，且必须与「大小/食物/功能」的物理约束自洽；虚构对象 ⇒ **无法用实测数据校准**

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"What is the ecological impact and requirements of the dragons? What are the energy expenditures of the dragons, and what are their caloric intake requirements?"*；*"How much area is required to support the three dragons?"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"it should be clear how your assumptions are related to the physical constraints of the functions, size, diet, changes, or other characteristics associated with the animals"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"would moving a dragon between an arid region, a warm temperate region, and an arctic region make a big difference in the resources required to maintain and grow a dragon?"* |

**数据形态**：无数据(纯机理/假设)｜**场景**：奇幻 / 生态

### 2019 B — Send in the Drones: Developing an Aerial Disaster Relief Response System

**问题抽象**：在「最多 3 个 ISO 集装箱、给定候选机型与医疗包需求」的约束下，选机队与医疗包组合、
设计装箱与投送航线/时刻表，并给出集装箱的最佳部署位置。
**结构化**：`要求`＝A 机队 + 医疗包 + 装箱方案；B 一/二/三箱时的**最佳部署位置**；C 每型机的载荷装箱、投送航线与时刻表 + 用机载视频评估主干路网的飞行计划；Part 2 给 CEO 的备忘录 ｜ `已知`＝附件 1–5：波多黎各地图、候选无人机 A–G（+系留 H）的性能表、两种货舱的尺寸、5 个点位的医疗包需求（型号/数量/每日频次）、医疗包尺寸与重量 ｜ `约束/不确定性`＝整机队必须装进 ≤3 个 20 尺集装箱且尽量不留空隙；无人机**必须落地**才能卸货；需求可能超过机队能力，此时必须说明取舍

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.2 离散/组合** | *"Recommend a drone fleet and set of medical packages for the HELP, Inc. DroneGo disaster response system that will meet the requirements of the Puerto Rico hurricane scenario."* |
| `核心` **3 优化 · 3.6 选址与布局** | *"Identify the best location or locations on Puerto Rico to position one, two, or three cargo containers of the DroneGo disaster response system"* |
| `核心` **3 优化 · 3.5 调度与配置** | *"Provide the drone payload packing configurations (i.e. the medical packages packed into the drone cargo bay), delivery routes and schedule to meet the identified emergency medical package requirements of the Puerto Rico hurricane scenario."* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"wants to clearly understand any tradeoffs that it must make for implementing solutions to address these shortcomings"* |

**数据形态**：空间/地理（波多黎各地图与点位经纬度；5 份附件）｜**场景**：应急物流 / 航空

### 2019 C — The Opioid Crisis

**问题抽象**：用县级药物鉴定计数与普查社经数据，建阿片类（含海洛因）事件的**时空扩散**模型、
反推可能的起始地点、给出阈值预警，并检验应对策略的有效性。
**结构化**：`要求`＝Part 1 五州内部与之间的传播/特征模型 + 起始地点识别 + 阈值水平与未来预测；Part 2 与普查社经数据的关联并据此改造模型；Part 3 应对策略及其有效性检验与关键参数边界；另加给 DEA/NFLIS 的备忘录 ｜ `已知`＝NFLIS 2010–2017 县级鉴定计数 + 7 份 ACS 社经数据（2010–2016）+ 变量代码表；题面明令**只能用这些数据** ｜ `约束/不确定性`＝县级位置数据「假定正确」；2017 年普查数据缺失；报案偏差；策略效果的**参数边界**必须给出

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.3 传播与级联** | *"build a mathematical model to describe the spread and characteristics of the reported synthetic opioid and heroin incidents (cases) in and between the five states and their counties over time"* |
| `核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"Using your model, identify any possible locations where specific opioid use might have started in each of the five states."* |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"Is use or trends-in-use somehow associated with any of the U.S. Census socio-economic data provided? If so, modify your model from Part 1 to include any important factors from this data set."* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"At what drug identification threshold levels do these occur? Where and when does your model predict they will occur in the future?"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"identify a possible strategy for countering the opioid crisis. Use your model(s) to test the effectiveness of this strategy"* |

**数据形态**：面板（县 × 年；NFLIS + 7 份 ACS 附件）｜**场景**：公共卫生 / 执法

### 2019 D — Time to leave the Louvre

**问题抽象**：为卢浮宫建**疏散**模型：把人流分配到出口与路径上、找出瓶颈，并在「威胁会移除部分路径」
的情形下保持方案可用，最后给出应急管理的政策与流程建议。
**结构化**：`要求`＝疏散模型（可让负责人探索多种方案，并让应急人员也能快速进入）+ 瓶颈识别 + 对多类威胁的适应性 + 模型验证与实施方式 + 政策/流程建议 + 迁移到其他大型拥挤建筑 ｜ `已知`＝卢浮宫的规模与出入口事实（5 层、38 万件展品、4 个主要入口、`Affluences` 实时等待时间应用）；**无附件数据集** ｜ `约束/不确定性`＝出口点位只有应急人员知道，公开使用会带来安保问题；人数随日/季变化、访客语言/团体/残障差异大；威胁会改变可行路径集合

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"individuals egress to and through an optimal exit in order to empty the building as quickly as possible"* |
| `核心` **8 网络与图 · 8.4 连通性与鲁棒性** | *"Each threat has the potential to alter or remove segments of possible routes to safety that may be essential in a single optimized route."* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"propose policy and procedural recommendations for emergency management of the Louvre"* |
| `附带` **4 机理建模与仿真 · 4.5 离散事件** | *"It is important to identify potential bottlenecks that may limit movement towards the exits."* |
| `附带` **3 优化 · 3.5 调度与配置** | *"while also allowing emergency personnel to enter the building as quickly as possible"* |

**数据形态**：空间/地理（楼层平面图）｜**场景**：公共安全 / 文旅

### 2019 E — What is the Cost of Environmental Degradation?

**问题抽象**：把生态系统服务计入成本-收益，为土地利用项目建**生态服务估值模型**，
并用它比较从小型社区项目到大型国家项目的真实经济成本。
**结构化**：`要求`＝生态服务估值模型 + 对不同规模项目的成本-收益分析 + 模型有效性评估 + 对规划者/管理者的启示 + 模型随时间如何变 ｜ `已知`＝题面给生态服务/生物多样性等术语定义 + 数据源链接（data.gov 生态数据、NOAA 卫星数据）+ 若干文献 ｜ `约束/不确定性`＝生态系统服务没有市价（须用影子价格/替代成本一类方法）；累积效应跨项目边界；「真实成本」的界定本身是判断

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"create an ecological services valuation model to understand the true economic costs of land use projects when ecosystem services are considered"* |
| `核心` **9 决策与博弈 · 9.3 风险与效用** | *"Is it possible to put a value on the environmental cost of land use development projects? How would environmental degradation be accounted for in these project costs?"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"perform a cost benefit analysis of land use development projects of varying sizes, from small community-based projects to large national projects"* |
| `附带` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Evaluate the effectiveness of your model based on your analyses and model design."* |
| `附带` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"whenever humans alter the ecosystem, we potentially limit or remove ecosystem services"* |

**数据形态**：空间/地理（土地利用 + 生态数据；题面给数据源链接）｜**场景**：环境经济 / 土地规划

### 2019 F — Universal, Decentralized, Digital Currency: Is it possible?

**问题抽象**：为一种「通用、去中心化、数字」的货币建**系统模型**，识别限制/促进其增长、可及、安全与稳定的
关键因素，并设计配套的监管机制、评估它对银行体系与国际关系的长期影响。
**结构化**：`要求`＝货币系统模型 + 增长/可及/安全/稳定的关键因素 + 采纳策略与实施难点 + 监管机制 + 对银行业、地方/区域/世界经济与国际关系的长期影响 + 给国家领导人的单页政策建议 ｜ `已知`＝题面给数字货币/加密货币/区块链等术语定义 + 两篇参考文献；**无附件数据集** ｜ `约束/不确定性`＝不得选定任何一种现有数字货币；各国放弃本币的意愿不同；监管与匿名性之间的张力；长期影响高度不确定

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"You should also include the mechanisms for oversight of such a global digital currency."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"The ICM Alliance has asked you to extend your analysis to consider the long-term effects of such a system on the current banking industry; the local, regional, and world economy; and international relations between countries."* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"You are not to choose an existing digital currency, but discuss the strategies for adoption, and problems in implementation of, a general digital currency."* |
| `附带` **9 决策与博弈 · 9.3 风险与效用** | *"Some governments, however, view the lack of regulation around these currencies and their anonymity as too risky because of how easily they can be used in illicit transactions"* |

**数据形态**：文本/文献（无数据集；政策与经济文献）｜**场景**：金融 / 货币政策

### 2020 A

**状态**：`读不出`
**登记**：题面件**没有文本层**——正文是用**矢量路径**画出来的，不是排出来的。
抽取口径（`pdftotext -enc UTF-8 <pdf> -`）只得 **25** 个字符 / **2** 行，全部是第 2 页杂志名那两行斜体
（`Hook Line and Sinker`）；`fitz.get_text()` 独立复核得 **22** 个字符。原件内容流里
`BT`/`Tf`/`Tj`/`TJ` 操作符合计 **4** 个，而**填充路径 3922 条**。
两条互相独立的探针都判它无文本层，全 67 份里只有这一份落在阈值另一侧（次低是 5 行 / 102 个操作符）。
⇒ **给不出可定位的支撑句**，故按「读不出」登记：**不标标签、不写抽象、不靠标题猜题意**。
判据 T5 会把这个集合**独立重算一遍**并与本行对账（标了「读不出」而题面其实可读 → 红）。

### 2020 B — The Longest Lasting Sandcastle(s)

**问题抽象**：求「最持久的三维沙堡基座形状」，在此基础上定最优沙水配比，再把模型扩展到降雨情形。
**结构化**：`要求`＝(1) 最耐久的三维基座形状 (2) 最优沙水配比 (3) 降雨下是否仍最优 (4) 其他延长寿命的策略 (5) 面向大众读者的科普文章 ｜ `已知`＝游乐海滩的常识背景；沙型、沙量、与水距离等条件被题面**固定为「相同」**，其余自设 ｜ `约束/不确定性`＝不得使用任何添加剂（塑料/木支撑、石头等）；波浪潮汐的侵蚀过程只能建模近似；降雨是附加扰动

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.2 逆向设计** | *"Construct a mathematical model to identify the best 3-dimensional geometric shape to use as a sandcastle foundation that will last the longest period of time on a seashore that experiences waves and tides"* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"determine an optimal sand-to-water mixture proportion for the castle foundation, assuming you use no other additives or materials"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Adjust your model as needed to determine how the best 3-dimensional sandcastle foundation you identified in requirement 1 is affected by rain"* |
| `附带` **3 优化 · 3.4 动态与随机** | *"the inflow of ocean waves coupled with rising tides erodes sandcastles"* |

**数据形态**：无数据(纯机理/假设)｜**场景**：海滩 / 休闲

### 2020 C — A Wealth of Data

**问题抽象**：用三张亚马逊评论表（星评、文本评论、有用性投票）找出可用于**预测产品成败**的文本与评分度量，
并回答「哪种星评会引发更多评论」这类关联问题。
**结构化**：`要求`＝(1) 找出评分/评论/有用性之间的模式、关系、度量与参数 (2) 具体问题：该跟踪哪些度量、随时间变化的声誉指标、文本+评分度量的组合、星评是否引发评论、质量描述词与评分等级的关联 (3) 给市场总监的信 ｜ `已知`＝附件 `Problem_C_Data.zip` 的三张 TSV（hair_dryer / microwave / pacifier）+ 字段说明；题面明令**只能用这些数据** ｜ `约束/不确定性`＝文本是非结构化数据、需先量化；「成功」的判据要自己定；数据只覆盖三个品类

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **10 文本与语义处理 · 10.1 文本特征与情感抽取** | *"Are specific quality descriptors of text-based reviews such as 'enthusiastic', 'disappointed', and others, strongly associated with rating levels?"* |
| `核心` **5 统计推断与因果 · 5.5 关联/相关模式** | *"identify, describe, and support with mathematical evidence, meaningful quantitative and/or qualitative patterns, relationships, measures, and parameters within and between star ratings, reviews, and helpfulness ratings"* |
| `核心` **1 预测 · 1.1 时序外推** | *"Identify and discuss time-based measures and patterns within each data set that might suggest that a product's reputation is increasing or decreasing in the online marketplace."* |
| `核心` **7 分类与聚类 · 7.3 降维与特征** | *"Determine combinations of text-based measure(s) and ratings-based measures that best indicate a potentially successful or failing product."* |
| `附带` **5 统计推断与因果 · 5.3 因果/政策评估** | *"Do specific star ratings incite more reviews?"* |

**数据形态**：混合（三张含日期的评论表：文本 + 星评 + 投票）｜**场景**：电子商务 / 市场营销

### 2020 D — Teaming Strategies

**问题抽象**：把足球队的传球事件建成**网络**，用它刻画团队结构/构型与动力学特征、提取超越胜负的团队绩效
指标，并据此给出教练层面的策略建议。
**结构化**：`要求`＝传球网络 + 网络模式（二元/三元构型、阵型等）与结构指标 + 多尺度（微观到宏观）与多时间尺度 + 团队绩效指标 + 捕获结构/构型/动态的团队模型 + 给教练的改进建议 + 向一般团队推广 ｜ `已知`＝附件 `2020_Problem_D_DATA.zip`（`fullevents.csv` / `matches.csv` / `passingevents.csv` / `README.txt`）：38 场比赛、19 个对手、23,429 次传球、366 名球员、59,271 个事件 ｜ `约束/不确定性`＝指标须超出胜负、并区分「普适有效」与「依赖对手反制」；跨比赛与跨球队的可比性

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.1 网络结构与重要性** | *"Create a network for the ball passing between players, where each player is a node and each pass constitutes a link between players."* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Identify performance indicators that reflect successful teamwork (in addition to points or wins)"* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"create a model that captures structural, configurational, and dynamical aspects of teamwork"* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"explore how the complex interactions among the players on the field impacts their success"* |

**数据形态**：网络（事件级传球网络 + 比赛结果；附件）｜**场景**：体育 / 团队科学

### 2020 E — Drowning in Plastic

**问题抽象**：为一次性塑料废弃物的**可安全消纳上限**建模，讨论能压到什么水平、给出全球目标与时间线，
并处理国别之间的公平问题。
**结构化**：`要求`＝可安全消纳的最大废弃量模型 + 能减到什么程度（含替代品、民生影响、政策有效性）+ 全球最小可达水平的目标与其影响 + 公平性问题与建议 + 给 ICM 的两页备忘录 ｜ `已知`＝题面给的量级事实（约 9% 被回收、每年 400–1200 万吨入海等）与 4 篇文献；**无附件数据集** ｜ `约束/不确定性`＝区域差异使同一政策效果不同；「环境安全水平」需要自己界定；塑料产业规模巨大、替代路径的代价难估

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"Develop a model to estimate the maximum levels of single-use or disposable plastic product waste that can safely be mitigated without further environmental damage."* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"to solve the plastic waste problem, we need to slow down the flow of plastic production and improve how we manage plastic waste"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"You may consider ways in which human life is altered, the environmental impacts, or the effects on the multi-trillion-dollar plastic industry."* |
| `核心` **3 优化 · 3.4 动态与随机** | *"a timeline to reach this level, and any circumstances that may accelerate or hinder the achievement of your target and timeline"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"policies of cities, regions, countries, and continents to decrease single-use or disposable plastic and the effectiveness of such policies"* |
| `附带` **2 评价与排序 · 2.4 方案比较** | *"considering regional-specific constraints may make some policies more effective than others"* |

**数据形态**：混合（文献量级 + 政策/产业数据自采）｜**场景**：环境 / 公共政策

### 2020 F — The Place I Called Home…

**问题抽象**：为「海平面上升导致岛国消失后的环境流离失所者（EDP）」建模型与政策框架：
量化风险人口与文化价值、设计兼顾人权与文化保存的政策、并评估政策的潜在影响。
**结构化**：`要求`＝(1) 风险人口与「文化损失风险」的量化 (2) 人权与文化保存两方面的政策 (3) 度量政策影响的模型 (4) 模型如何改进政策 (5) 为何必须实施 ｜ `已知`＝题面 Issue Paper（第 3 页起）详述三组张力（人权/国家责任/个人选择；同化 vs 包容；时间因素）+ 5 篇文献；**无附件数据集** ｜ `约束/不确定性`＝文献对 EDP 人数的估计相差极大（1.4 亿到 10 亿），题面要求用自己的模型独立分析；「文化价值」难以定价；谁有权决定安置地本身有争议

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"how should the world respond with an international policy that specifically focuses on protecting the rights of persons whose nations have disappeared in the face of climate change while also aiming to preserve culture?"* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"An analysis of the scope of the issue in terms of both the number of people at risk and the risk of loss of culture"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"how many people are currently at risk of becoming EDPs"*；*"what is the value of the cultures of at-risk nations; how are those answers likely to change over time?"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"A description of the development of a model used to measure the potential impact of proposed policies"* |
| `附带` **9 决策与博弈 · 9.1 多准则决策** | *"who gets a say in deciding where these nationless EDPs make a new home"* |

**数据形态**：文本/文献（Issue Paper + 文献；无数据集）｜**场景**：气候 / 国际法

### 2021 A — Fungi

**问题抽象**：用两个性状（生长速率、耐湿性）建**多物种真菌分解木质纤维**的动力学模型，
刻画种间竞争与短/长期动态，并对环境波动与生物多样性做敏感性分析。
**结构化**：`要求`＝分解过程的数学模型 + 两性状驱动的种间相互作用 + 动态刻画（短/长期）与环境快速波动的敏感性 + 各物种/组合在不同环境（干旱/半干旱/温带/树栖/热带雨林）下的优劣与共存预测 + 多样性与系统效率的关系 + 面向大学教材的两页文章 ｜ `已知`＝题面给两篇论文的图 1/图 2（生长速率—分解率、耐湿性—分解率关系）、论文梗概与术语表 ｜ `约束/不确定性`＝环境在空间上差异很大且随时间变化；论文只覆盖「分解中期」，其他阶段假设一致

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Build a mathematical model that describes the breakdown of ground litter and woody fibers through fungal activity in the presence of multiple species of fungi."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Your analysis should examine the sensitivity to rapid fluctuations in the environment, and you should determine the overall impact of changing atmospheric trends"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Include predictions about the relative advantages and disadvantages for each species and combinations of species likely to persist, and do so for different environments including arid, semi-arid, temperate, arboreal, and tropical rain forests."* |
| `附带` **7 分类与聚类 · 7.1 监督分类/识别** | *"Predict the importance and role of biodiversity in the presence of different degrees of variability in the local environment."* |

**数据形态**：混合（文献图片给出的性状关系 + 自设参数）｜**场景**：生态 / 微生物

### 2021 B — Fighting Wildfires

**问题抽象**：为「无人机 + 中继」的野外消防通信/侦察队设计**采购组合与部署方案**：
在能力、安全与经济之间权衡，按火情大小与地形优化中继无人机的位置，并预测未来十年的装备成本。
**结构化**：`要求`＝(1) SSA 与中继无人机的**数量与型号组合**（含火情规模/频率参数与地形）（2）未来十年极端火情概率变化下的适应与成本（3）不同火情规模与地形下中继无人机的**位置**优化（4）给州政府的预算申请 ｜ `已知`＝题面的性能参数（5 W 手持电台 5 km / 城区 2 km、10 W 中继 20 km、WileE 15.2X 无人机 30 km / 20 m/s / 2.5 h / 约 $10,000 AUD）+ 地形图 ｜ `约束/不确定性`＝通信距离由距离与地形支配；极端火情概率在变化；成本按「系统价格不变」假设外推

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.2 离散/组合** | *"determine the optimal numbers and mix of SSA drones and Radio Repeater drones to purchase for a proposed new division"* |
| `核心` **3 优化 · 3.6 选址与布局** | *"Determine a model for optimizing the locations of hovering VHF/UHF radio-repeater drones for fires of different sizes on different terrains"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Your model should balance capability and safety with economics"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Illustrate how your model adapts to the changing likelihood of extreme fire events over the next decade."* |
| `附带` **8 网络与图 · 8.4 连通性与鲁棒性** | *"The range of a repeater is also determined by distance and topography, but is significantly greater than lower power handheld radios."* |

**数据形态**：空间/地理（地形图 + 通信距离参数）｜**场景**：应急通信 / 消防

### 2021 C

**问题抽象**：用公众目击报告数据建**误判概率**的分类模型，据此给有限资源的核查排优先级，
并回答种群扩散能否预测、模型如何随新报告更新、何种证据算「已根除」。
**结构化**：`要求`＝扩散的时间可预测性与精度 + 只用给定数据建「误判分类」模型 + 用分类结果给报告排优先级 + 模型随新报告的更新频率 + 「根除」的证据标准 + 给农业部的两页备忘录 ｜ `已知`＝四份附件：物种背景 PDF、4440 条目击记录 xlsx（含 `Lab Status` 评级、日期、经纬度、`Notes`）、3305 张图片（需自行下载）、图片—记录映射表 ｜ `约束/不确定性`＝题面明令**只能用给定数据**；大量目击是误判；`Lab Status` 含 `Unprocessed`/`Unverified` 等未定态；题干另列统计建模最佳实践（区间估计、拟合优度、分布假设检查）

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **7 分类与聚类 · 7.1 监督分类/识别** | *"create, analyze, and discuss a model that predicts the likelihood of a mistaken classification"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"Use your model to discuss how your classification analyses leads to prioritizing investigation of the reports most likely to be positive sightings."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Any estimate of a parameter should include an interval estimate."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Address and discuss whether or not the spread of this pest over time can be predicted, and with what level of precision."* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"A new queen has a range estimated at 30km for establishing her nest."* |
| `附带` **5 统计推断与因果 · 5.1 差异显著性检验** | *"All assumptions associated with the data should be checked, and the robustness of a technique with respect to those assumptions should be examined."* |

**数据形态**：混合（4440 条目击记录 + 文本备注 + 3305 张图片 + 经纬度）｜**场景**：入侵物种 / 农业监管

### 2021 D — The Influence of Music

**问题抽象**：把「艺术家影响」数据建成有向网络并定义「影响力」度量，再用歌曲音频特征定义相似度，
回答 genre 内/间的相似与影响关系、哪些特征更「传染」、革命性跃迁如何识别。
**结构化**：`要求`＝(1) 有向影响网络 + 影响力参数 + 子网络分析 (2) 相似度度量与 genre 内/间比较 (3) genre 的边界与演化 (4) 「影响者是否真的影响了跟随者」（特征的传染性）(5) 革命性跃迁与代表人物 (6) 单一 genre 的演化过程与文化/技术因素 (7) 给 ICM 学会的一页文件与数据受限的讨论 ｜ `已知`＝四份 csv：`influence_data`（5,854 位艺术家的影响关系）、`full_music_data`（98,340 首歌 × 16 个音频特征）、`data_by_artist`、`data_by_year`；题面明令只能用这些数据 ｜ `约束/不确定性`＝数据是完整集合的**子集**（只含两个数据集的交集艺术家与部分 genre）；「影响」是艺术家自报与专家意见的混合；相似度与影响力都是自建度量

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.3 传播与级联** | *"create a (multiple) directed network(s) of musical influence, where influencers are connected to followers"* |
| `核心` **8 网络与图 · 8.1 网络结构与重要性** | *"Develop parameters that capture 'music influence' in this network."* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"Do the 'influencers' actually affect the music created by the followers?"* |
| `核心` **7 分类与聚类 · 7.2 无监督聚类/分段** | *"Compare similarities and influences between and within genres. What distinguishes a genre and how do genres change over time?"* |
| `核心` **7 分类与聚类 · 7.3 降维与特征** | *"use full_music_data and/or the two summary data sets (with artists and years) of music characteristics, to develop measures of music similarity"* |
| `附带` **1 预测 · 1.1 时序外推** | *"Analyze the influence processes of musical evolution that occurred over time in one genre."* |

**数据形态**：混合（影响网络 + 歌曲级特征面板；附件）｜**场景**：音乐 / 文化

### 2021 E — Re-Optimizing Food Systems

**问题抽象**：为「食品系统」建可调优先级的模型（效率/利润/可持续/公平），并比较不同优先级下的系统差异、
成本收益与时滞，再在发达国家与发展中国家各验一次。
**结构化**：`要求`＝可针对效率/利润/可持续/公平调节的食品系统模型 + 「按公平与可持续优化会怎样、与现状差多少、要多久」+ 改变优先级的收益与成本及时点 + 至少一个发达与一个发展中国家上的应用 + 可扩展性与可迁移性 ｜ `已知`＝题面给的背景统计（8.21 亿人饥饿、占 29% 温室气体等）与 3 条文献链接 ｜ `约束/不确定性`＝系统复杂、方面自选；「公平/可持续」要自己操作化；时滞与国别差异大

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"you should provide a food system model that is robust enough to be able to be adjusted to optimize for various levels of efficiency, profitability, sustainability, and/or equity"* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"What are the benefits and costs of changing the priorities of a food system? When would they occur?"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"What happens if a food system is optimized for equity and sustainability? How would that system differ from the current one?"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Once you have developed your food system model, apply your model to at least one developed and one developing country to support your findings."* |
| `附带` **3 优化 · 3.4 动态与随机** | *"How long would such a system take to implement?"* |

**数据形态**：混合（文献统计 + 自采国别数据）｜**场景**：农业 / 公共政策

### 2021 F — Checking the Pulse and Temperature of Higher Education

**问题抽象**：为一个国家的高等教育系统建「健康度」度量与目标态，再用模型评估政策把系统从现状迁移到
目标态的效果与代价。
**结构化**：`要求`＝可评估任何国家高教系统健康度的模型 + 应用于多国并选定一个 + 提出可达的目标态 + 度量现状与目标态 + 政策包与实施时间线 + 用模型评估政策 + 讨论对各方的影响 ｜ `已知`＝题面给高教/系统健康等术语定义；国家数据自采 ｜ `约束/不确定性`＝「健康/可持续」需自己定义；改革需要长期政策且「change is hard」；跨国可比性

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"develop and validate a model or suite of models that allow you to assess the health of any nation's system of higher education"* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"identify a healthy and sustainable state for a given nation's higher education system"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"propose targeted policies and an implementation timeline that will support the migration from the current state to your proposed state"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"discuss the real-world impacts (e.g., on students, on faculty, on schools, on communities, on the nation) of implementing your plan both during the transition and in the end state"* |
| `附带` **3 优化 · 3.4 动态与随机** | *"an implementation timeline that will support the migration from the current state to your proposed state"* |

**数据形态**：面板（跨国 × 跨年教育统计）｜**场景**：高等教育 / 公共政策

### 2022 A — Power Profile of a Cyclist

**问题抽象**：在功率曲线与累积疲劳约束下，求个人计时赛中「位置 → 功率输出」的最优策略，
并做成天气与执行偏差下的敏感性分析。
**结构化**：`要求`＝任意类型车手的「位置—功率」模型（含总能量上限、既往激进行为的累积、超功率曲线的代价）+ 两类车手（含不同性别）的功率曲线 + 三条指定赛道上的应用 + 自设赛道 + 天气（风向风速）影响与敏感性 + 对目标功率偏差的敏感性 + 团队计时赛的扩展 + 给车队经理的两页比赛指引 ｜ `已知`＝功率曲线概念说明与指定赛道名称（东京奥运、弗兰德斯世锦赛）；**无附件数据集** ｜ `约束/不确定性`＝总能量有限、超出功率曲线要付出恢复代价；实际执行必然偏离目标；天气是外生扰动

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.1 连续/非线性** | *"Develop a model that can be applied to any type of rider that determines the relationship between the rider's position on the course and the power the rider applies."* |
| `核心` **3 优化 · 3.4 动态与随机** | *"Keep in mind that the rider has a limit on the total energy that can be expended over the course, as well as limits that accumulate from past aggressiveness and for exceeding the power curve limits."* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Determine the potential impact of weather conditions, including wind directions and wind strengths, to determine how sensitive your results are for small differences in the weather and environment."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Determine how sensitive the results are to rider deviations from the target power distribution."* |
| `附带` **2 评价与排序 · 2.4 方案比较** | *"Discuss how to extend your model to include the optimal power use for a team time trial of six riders per team"* |

**数据形态**：无数据(纯机理/假设)（功率曲线与赛道自设）｜**场景**：体育 / 最优控制

### 2022 B — Water and Hydroelectric Power Sharing

**问题抽象**：为两座串联水库建「水量—发电—分配」模型，在给定供需与水库水位下给出放水与分配方案，
并回答需求增长、可再生比例上升等情形下的行为。
**结构化**：`要求`＝水分配计划（两库水位为 M/P 时各取多少水、固定需求下还能撑多久、需要补多少水）+ 竞争性利益的解决方式与判据 + 水不够时的处置 + 若干情形下的表现 + 墨西哥的剩余水权 + 入海流量 + 给《Drought and Thirst》的文章 ｜ `已知`＝Glen Canyon / Hoover 两坝与 Lake Powell / Lake Mead 的背景、五州（AZ/CA/WY/NM/CO）与既有的超额分配事实；**无附件数据集** ｜ `约束/不确定性`＝题面要求**不得**依赖历史协议与政治权力，只做数学上的最优分配；两库串联（上游出流是下游入流）；水位—库容关系必须显式使用；需求可能增长

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Use your model to recommend the best means to resolve the competing interests of water availability for general (agricultural, industrial, residential) usage and electricity production."* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"When the water level in Lake Mead is M and the water level in Lake Powell is P, how much water should be drawn from each lake to meet stated demands?"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"respecting the relationship between water height in the reservoirs and the volume of water in the reservoirs"* |
| `核心` **3 优化 · 3.4 动态与随机** | *"If no additional water is supplied (from rainfall, etc.), and considering the demands as fixed, how long will it take before the demands are not met?"* |
| `附带` **9 决策与博弈 · 9.1 多准则决策** | *"Explicitly state the criteria you are using to resolve competing interests."* |
| `附带` **8 网络与图 · 8.2 流量分配/路由** | *"The operations of the Glen Canyon dam (Lake Powell) and the Hoover dam (Lake Mead) should be closely coordinated because water outflows from the Glen Canyon dam supply part of the water input to the Hoover dam."* |

**数据形态**：无数据(纯机理/假设)（题面给坝参数背景，无附件）｜**场景**：水资源 / 能源

### 2022 C — Trading Strategies

**问题抽象**：只用「当日及之前」的历史日价求每日买/持/卖的最优策略，使 1000 美元在五年末最大，
并给出策略优越性的证据与对交易成本的敏感性。
**结构化**：`要求`＝每日交易策略模型 + 期末价值 + 「该策略最好」的证据 + 交易成本敏感性 + 给交易员的备忘录 ｜ `已知`＝两个 csv（LBMA 金价、BCHAIN 比特币价）与初始状态 [1000,0,0]、佣金率（金 1%、比特币 2%）、交易日程约束（金只在开市日可交易）；题面明令只能用这两个文件 ｜ `约束/不确定性`＝只能用「当日之前」的信息（防前视）；金与比特币的交易日不同；交易成本会吃掉高频策略的收益

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.4 动态与随机** | *"develop a model that uses only the past stream of daily prices to date to determine each day if the trader should buy, hold, or sell their assets in their portfolio"* |
| `核心` **1 预测 · 1.1 时序外推** | *"Develop a model that gives the best daily trading strategy based only on price data up to that day."* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Present evidence that your model provides the best strategy."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Determine how sensitive the strategy is to transaction costs."* |
| `附带` **9 决策与博弈 · 9.3 风险与效用** | *"Market traders buy and sell volatile assets frequently, with a goal to maximize their total return."* |

**数据形态**：时序（两张日价表；附件）｜**场景**：金融 / 投资

### 2022 D — Data Paralysis? Use Our Analysis!

**问题抽象**：为一家港口公司建「数据与分析（D&A）系统成熟度」的度量与改进方案：用人员/技术/流程三要素的
KPI 给出成熟度，并据此给出优化路径与推广条件。
**结构化**：`要求`＝衡量 D&A 成熟度的指标（含三类关键绩效指标）+ 用模型推荐改造路径 + 效果度量的协议 + 向更大/更小港口与其他行业推广的可行性 + 给港口用户的单页信 ｜ `已知`＝题面第 3 页起给 ICM 公司运营与数据类型的一般描述；**因公司规章不得共享具体的人员/技术/流程/数据** ｜ `约束/不确定性`＝没有该公司内部的任何具体数据；成熟度尺度与阈值须自建；跨行业迁移性待论证

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"A metric to measure the current D&A system maturity level for ICM Corporation. Include key performance indicators that measure the success of their D&A people, technologies, and processes."* |
| `核心` **2 评价与排序 · 2.2 多指标综合评价** | *"your models provide companies with the ability to measure the D&A system maturity through examination of these three key components"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"demonstrate how they could use your model to recommend changes to the system allowing the company to maximize the potential of their data assets"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Demonstrate how your model might be applied to a larger or smaller seaport. Analyze how your system maturity metric could be adapted to other industries."* |
| `附带` **2 评价与排序 · 2.5 分级/阈值划定** | *"After ICM Corporation uses your model to determine their current D&A maturity level"* |
| `附带` **4 机理建模与仿真 · 4.5 离散事件** | *"the time a ship, truck, or train spends at the port is minimized"* |

**数据形态**：无数据(纯机理/假设)（题面明确说明拿不到公司内部数据）｜**场景**：港口物流 / 企业管理

### 2022 E — Forestry for Carbon Sequestration

**问题抽象**：建森林与木制品的**碳汇**模型求最优采伐管理方案，再建一个「兼顾多种森林价值」的决策模型，
并在具体森林上给出管理计划与过渡策略。
**结构化**：`要求`＝碳汇模型与最优管理方案 + 兼顾多种价值的决策模型（含「哪些条件下应完全不砍」「是否存在对所有森林都适用的转换点」）+ 应用到一个具体森林 + 该森林 100 年的固碳量 + 过渡到新采伐周期的策略 + 面向社区的非技术文章 ｜ `已知`＝题面给森林产品、碳汇、采伐等术语定义；具体森林自选 ｜ `约束/不确定性`＝价值维度多且不可公度（固碳/保育/游憩/文化）；采伐周期改变会给森林管理者带来过渡成本

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Develop a carbon sequestration model to determine how much carbon dioxide a forest and its products can be expected to sequester over time."* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Develop a decision model to inform forest managers of the best use of a forest."* |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"The forest management plan that is best for carbon sequestration is not necessarily the one that is best for society given the other ways that forests are valued."* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"Are there transition points between management plans that apply to all forests?"* |
| `附带` **3 优化 · 3.5 调度与配置** | *"Suppose the best management plan includes a time between harvests that is 10 years longer than current practices in the forest."* |

**数据形态**：混合（森林生长参数 + 产品寿命 + 价值权重自采）｜**场景**：林业 / 气候

### 2022 F — All for One and One (Space) for All!

**问题抽象**：先定义并度量「全球公平」，再在一种具体的太空采矿前景下评估它对公平的影响，
最后给出能提升公平的条约/政策建议。
**结构化**：`要求`＝全球公平的定义与度量（含验证）+ 描述并论证一种采矿前景 + 评估该前景对公平的影响 + 条件变化下的影响差异 + 政策建议（含条约修订） ｜ `已知`＝《外空条约》1967 的条文引用 + 术语表；**无附件数据集** ｜ `约束/不确定性`＝采矿部门的未来形态完全未知（谁开采、谁出资、谁获益都要自行设定并论证）；「公平」的定义本身是判断

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"develop a definition of global equity. Use your definition to develop a model (e.g., tool, metric) that allows you to measure global equity."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Present, describe, and justify one likely vision for the future of asteroid mining, and determine the impact of mining on global equity"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"What policies could be implemented to encourage the asteroid mining sector to advance in a way that promotes more global equity?"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"How do changes in the conditions that you selected in defining a vision for the future of asteroid mining impact global equity?"* |
| `附带` **2 评价与排序 · 2.4 方案比较** | *"Validate your model; this might involve historical and/or regional analyses."* |

**数据形态**：混合（历史/区域数据 + 文献；无附件）｜**场景**：航天 / 国际治理

### 2023 A — Drought-Stricken Plant Communities

**问题抽象**：为「干旱胁迫下植物群落随世代的演化」建模型，回答**物种数**与抗旱适应性的关系、
长期可存续性，以及干旱频率/幅度变化与污染/栖息地缩减的影响。
**结构化**：`要求`＝群落随时间演化的数学模型（含不规则天气周期与种间相互作用）+ 物种数的作用与规模效应 + 物种类型的影响 + 干旱频率与变率的影响 + 污染与栖息地缩减的影响 + 长期存续的对策 ｜ `已知`＝题面给的观察事实（单一物种群落的后代适应不如 4 种以上的群落）；**无附件数据集** ｜ `约束/不确定性`＝「不规则天气周期」须自设随机结构；长期（多世代）演化的参数不确定

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Develop a mathematical model to predict how a plant community changes over time as it is exposed to various irregular weather cycles."* |
| `核心` **4 机理建模与仿真 · 4.3 随机仿真/概率模拟** | *"Include times of drought when precipitation should be abundant. The model should account for interactions between different species during cycles of drought."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"What are the impact of a greater frequency and wider variation of the occurrence of droughts in future weather cycles? If droughts are less frequent, does the number of species have the same impact on the overall population?"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"How do other factors such as pollution and habitat reduction impact your conclusions?"* |

**数据形态**：无数据(纯机理/假设)｜**场景**：生态 / 农业

### 2023 B — Reimagining Maasai Mara

**问题抽象**：为马赛马拉保护区设计「区内分区 + 区外」的管理策略，建动物—人相互作用与其经济影响的模型，
用一个能**排序**方案的方法论选出最优组合，并预测长期趋势与确定性。
**结构化**：`要求`＝区内不同区域的具体政策与管理策略（保护野生动物/自然资源 + 平衡当地居民利益）+ 判定「最佳」的方法论（含排序与比较）+ 动物—人相互作用与经济影响的模型 + 长期趋势预测与不确定性 + 迁移到其他保护区 + 面向肯尼亚委员会的两页非技术报告 ｜ `已知`＝肯尼亚《野生动物保护与管理法》及其修正案背景；**无附件数据集** ｜ `约束/不确定性`＝居民的机会损失与动物—人冲突必须同时缓解；「最佳」的标准须自己给并可比；长期结果的确定性要估计

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"Develop and describe a methodology to determine which policies and management strategies will result in the best outcomes."* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"Your report should discuss how to rank and compare outcomes from your methodology."* |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"include descriptions and analyses of the models used to predict the interactions between animals and people, as well as the resulting economic impacts"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Analyze and provide estimates of the certainties and impacts of the possible long-term outcomes."* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"recommend specific policies and management strategies for different areas within the current preserve"* |
| `附带` **3 优化 · 3.6 选址与布局** | *"determine alternate ways to manage the resources within and outside the current boundaries of the park"* |

**数据形态**：空间/地理（保护区分区 + 动物/居民分布）｜**场景**：野生动物保护 / 地方治理

### 2023 C — Predicting Wordle Results

**问题抽象**：用一年的每日结果数据解释**报告量的日间波动**、预测未来某日的报告量与其分布、
并按难度给答案词**分类**。
**结构化**：`要求`＝报告量波动的模型 + 2023-03-01 的**预测区间** + 词的属性是否影响 Hard Mode 占比 + 预测未来某日的 (1,2,3,4,5,6,X) 分布及其不确定性 + 按难度分类答案词的模型与准确度 + 其他有趣特征 + 给谜题编辑的信 ｜ `已知`＝附件 `Problem C Data Wordle.xlsx`（2022-01-07 至 2022-12-31：日期、题号、答案词、报告数、Hard Mode 人数、各档百分比）；题面明令只能用该文件 ｜ `约束/不确定性`＝百分比因四舍五入可能不等于 100%；Twitter 报告人群有选择偏差；「难度」需自己定义

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.1 时序外推** | *"Develop a model to explain this variation and use your model to create a prediction interval for the number of reported results on March 1, 2023."* |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"Do any attributes of the word affect the percentage of scores reported that were played in Hard Mode?"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"develop a model that allows you to predict the distribution of the reported results"* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"Develop and summarize a model to classify solution words by difficulty."* |
| `核心` **7 分类与聚类 · 7.1 监督分类/识别** | *"Identify the attributes of a given word that are associated with each classification."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"What uncertainties are associated with your model and predictions?"* |

**数据形态**：时序（日度序列 + 词属性；附件）｜**场景**：游戏 / 统计学

### 2023 D — Prioritizing the UN Sustainability Goals

**问题抽象**：把 17 个可持续发展目标之间的相互影响建成**网络**，用网络结构与个体目标一起给工作**排优先级**，
并考察目标达成、外部冲击与新增目标对网络与优先级的影响。
**结构化**：`要求`＝17 个 SDG 的关系网络 + 用个体目标与网络结构设优先级（含效果评估与 10 年可达成度）+ 某一目标达成后的网络结构与优先级变化 + 是否应增补目标 + 技术/疫情/气候/战争/难民等冲击的网络视角影响 + 该方法对其它组织的迁移 ｜ `已知`＝题面列出 17 个 SDG 的名称 + 1 条参考文献；**无附件数据集** ｜ `约束/不确定性`＝目标之间的影响有正有负、还可能双向；「效果」的评估口径要自己定；冲击的量化困难

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.1 网络结构与重要性** | *"Create a network of the relationships between the 17 SDGs. Use the individual SDGs, as well as the structure of your network, to set priorities"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"set priorities that can most efficiently move the work of the UN forward. How did you evaluate the effectiveness of each priority?"* |
| `核心` **8 网络与图 · 8.4 连通性与鲁棒性** | *"If one of the SDGs is achieved (for example, there is no poverty or no hunger), what would be the structure of the resulting network?"* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"Discuss the impact of technological advances, global pandemics, climate change, regional wars, and refugee movements, or other international crises on your team's network"* |

**数据形态**：文本/文献（SDG 之间的关系取自文献；无数据集）｜**场景**：国际发展 / 公共政策

### 2023 E — Light Pollution

**问题抽象**：建一个可广泛适用的**光污染风险等级**度量，把它用在不同类型的四类地点上，
提出三种干预策略并比较它们在两类地点上的有效性。
**结构化**：`要求`＝可广泛适用的风险等级度量 + 应用于四类地点（保护地/乡村/郊区/城市）+ 三种干预策略及其具体行动与影响 + 用度量比较两类地点上哪种策略最有效 + 给一个地点做单页宣传材料 ｜ `已知`＝题面给光污染现象与影响的背景、术语表（人工光/眩光/光侵入/过度照明等）；**无附件数据集** ｜ `约束/不确定性`＝人工光同时有正负效应，且因地点（发展水平、人口、生物多样性、地理、气候）而异；风险等级的分级标准要自己定

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Develop a broadly applicable metric to identify the light pollution risk level of a location."* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"Apply your metric and interpret its results on the following four diverse types of locations"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Choose two of your locations and use your metric to determine which of your intervention strategies is most effective for each of them."* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"Describe three possible intervention strategies to address light pollution."* |
| `附带` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Excessive artificial light may confuse our circadian rhythms, leading to poor sleep quality and perhaps physical and mental health issues."* |

**数据形态**：空间/地理（四类地点的差异 + 光照/生态指标）｜**场景**：城市环境 / 生态保护

### 2023 F — Green GDP

**问题抽象**：假定世界改用「绿色 GDP」作为经济健康的首要度量，用模型估计它对气候减缓的全球影响、
判断这一替换是否值得，并选一个国家做深入分析。
**结构化**：`要求`＝选定一种已有的 GGDP 计算口径并论证其影响潜力 + 可辩护的简单模型估计全球影响 + 判断替换是否值得（上行收益 vs 下行代价）+ 选一个国家做深入分析（自然资源的使用/保存如何变、对当代与后代是否有利）+ 给该国领导人的单页非技术报告 ｜ `已知`＝题面给 GDP 现行口径的引文与 GGDP 概念；**无附件数据集** ｜ `约束/不确定性`＝多边协调极难、替换本身有阻力；「全球影响」的度量口径要自己定；国家层面的影响依赖其经济结构

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"There are many proposed ways to calculate GGDP that have already been developed. Select one that your team believes could have a measurable impact on climate mitigation if it replaced GDP as the primary measure of economic health."* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"Make a simple model that is easily defendable to estimate the expected global impact on climate mitigation if your selected GGDP is adopted as the primary measure of the economic health of a nation."* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"comparing both the potential upside of climate mitigation impact and the potential downside of the effort required to replace the status quo"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"Be sure that your analysis is explicitly tied to the changes between how GDP and GGDP are calculated."* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"Would those changes be beneficial to this specific country, considering both their current economic status and their ability to support future generations?"* |

**数据形态**：混合（国家经济与环境统计 + 文献）｜**场景**：宏观经济 / 气候政策

### 2023 Z — The Future of the Olympics

**问题抽象**：为「奥运会主办模式」建多维影响的度量（经济、土地利用、人的满足度、旅行、未来改进空间、
主办城市声望等），并据此评估若干替代方案（如常设主办地、把项目拆成四组）的可行性与时间线。
**结构化**：`要求`＝多维影响度量 + 若干创意方案/策略/政策（含可行性、实施时间线与影响）+ 给 IOC 的单页备忘录 ｜ `已知`＝题面给申办数下降与既往负面影响的背景、一个参考文献；**无附件数据集** ｜ `约束/不确定性`＝「成功」是多维且利益相关者不同的；新赛制的可行性未知；时间线与影响只能估计

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"The ICMG recommends building metrics for the impacts of hosting the games from various points of view: economic, land use, human satisfaction (athletes and spectators), travel, opportunity for future improvements, host city/nation prestige, and other criteria your team identifies."* |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"Your task is to make recommendations in support of the ICMG's work."* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Consider the feasibility, timeline to implement, and impact of potential strategies on your metrics."* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"perhaps the Summer and Winter Games should each have a permanent location"* |

**数据形态**：无数据(纯机理/假设)（题面只给背景与参考文献，无数据集）｜**场景**：体育治理 / 公共政策

### 2024 A — Resource Availability and Sex Ratios

**问题抽象**：为「海七鳃鳗按食物可得性改变性别比」建生态模型，分析这种可塑性对种群自身、
对生态系统稳定性、以及对其他物种（如寄生生物）的利弊。
**结构化**：`要求`＝能刻画「资源可得性→性别比→种群与生态」的模型 + 对更大生态系统的冲击 + 对种群自身的利弊 + 对生态系统稳定性的影响 + 是否给其他物种带来优势 ｜ `已知`＝题面给的经验关系（食物少时雄性可达约 78%、食物充足时约 56%）与七鳃鳗生活史；**无附件数据集** ｜ `约束/不确定性`＝性别比可塑的**代价**与收益没有现成数据；稳定性与「优势」需自己定义并论证

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Your team should develop and examine a model to provide insights into the resulting interactions in an ecosystem."* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | *"What is the impact on the stability of the ecosystem given the changes in the sex ratios of lampreys?"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"The task is to examine the advantages and disadvantages of the ability for a species to alter its sex ratio depending on resource availability."* |
| `附带` **1 预测 · 1.2 回归/相关预测** | *"Sea lampreys become male or female depending on how quickly they grow during the larval stage. These larval growth rates are influenced by the availability of food."* |

**数据形态**：无数据(纯机理/假设)｜**场景**：生态 / 渔业

### 2024 B — Searching for Submersibles

**问题抽象**：为失联的深海观光潜水器建**位置随时间的预测**与**搜索**模型：估计位置与其不确定性、
决定要周期性回传什么信息、设计搜索的初始投放点与搜索图形，并给出找到的概率随时间的变化。
**结构化**：`要求`＝Locate 位置预测模型 + 其不确定性 + 应回传的信息与所需设备；Prepare 主机船应携带的搜索设备（含成本）；Search 初始投放点与搜索图形 + 找到概率随时间的变化；Extrapolate 迁移到别的海域与多潜水器 ｜ `已知`＝MCMS 公司的运营背景与"无缆释放"方式；海域的洋流、密度与海底地形资料**自采** ｜ `约束/不确定性`＝潜水器可能停在海底或中性浮力处；洋流、密度与地形都影响位置；搜索设备有成本与维护代价

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.3 状态估计/数据同化** | *"they would like you to develop a model to predict the location of the submersible over time"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"What are the uncertainties associated with these predictions?"* |
| `核心` **3 优化 · 3.6 选址与布局** | *"recommend initial points of deployment and search patterns for the equipment so as to minimize the time to location of a lost submersible"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Its position could further be affected by currents, differing densities in the sea, and/or the geography of the sea floor."* |
| `核心` **9 决策与博弈 · 9.3 风险与效用** | *"What, if any, additional search equipment would you recommend the company carry on the host ship to deploy if necessary?"* |
| `附带` **3 优化 · 3.5 调度与配置** | *"Determine the probability of finding the submersible as a function of time and accumulated search results."* |

**数据形态**：空间/地理（海底地形、洋流与密度）｜**场景**：海洋搜救 / 旅游安全

### 2024 C — Momentum in Tennis

**问题抽象**：用逐分的比赛数据建「比赛走势」模型（谁打得更好、好多少），并检验「势头」是否真的存在、
能否预测走势反转。
**结构化**：`要求`＝刻画逐分走势的模型 + 谁在何时更好以及好多少 + 可视化 + 用模型检验「走势纯随机」的假设 + 走势反转的预测与相关因素 + 对教练的建议 + 在其他比赛/赛事/场地/运动上的可推广性 + 给教练的备忘录 ｜ `已知`＝附件：`Wimbledon_featured_matches.csv`（2023 温网男单前两轮之后的比赛逐分数据）+ 数据字典 + 示例 + 术语表；可自行补充但须完整注明来源 ｜ `约束/不确定性`＝发球方优势必须考虑；「势头」本身是否真实存在就是待检验的命题；不同赛事的可迁移性未知

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"Your model should identify which player is performing better at a given time in the match, as well as how much better they are performing."* |
| `核心` **5 统计推断与因果 · 5.1 差异显著性检验** | *"A tennis coach is skeptical that 'momentum' plays any role in the match. Instead, he postulates that swings in play and runs of success by one player are random. Use your model/metric to assess this claim."* |
| `核心` **7 分类与聚类 · 7.2 无监督聚类/分段** | *"Develop a model that captures the flow of play as points occur and apply it to one or more of the matches."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"develop a model that predicts these swings in the match"* |
| `附带` **5 统计推断与因果 · 5.2 回归系数与效应量** | *"What factors seem most related (if any)?"* |

**数据形态**：时序（逐分事件序列；附件）｜**场景**：体育 / 统计学

### 2024 D — Great Lakes Water Problem

**问题抽象**：把五大湖与连接河道建成**网络模型**，为两座控制坝设计维持最优水位的控制算法，
并在 2017 年真实数据上检验，处理利益相关者冲突与降雨/雪盖/冰塞等扰动。
**结构化**：`要求`＝五大湖与河道的水量网络模型 + 五湖全年最优水位（含各利益相关者的成本收益）+ 由流入流出数据维持最优水位的算法 + 控制算法对两坝出流的敏感性 + 2017 年数据上的复核 + 对环境条件变化的敏感性 + 给 IJC 的单页备忘录 ｜ `已知`＝附件 `Problem_D_Great_Lakes.xlsx`（流入、流出与水位数据）+ Problem D Addendum + 数据示例清单 ｜ `约束/不确定性`＝题面称之为「wicked」问题：相互依赖、要求复杂、内在不确定；只重点分析安大略湖；降雨/蒸发/侵蚀/冰塞不可控；各利益相关者的目标冲突

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Determination of the optimal water levels of the five Great Lakes at any time of the year, taking into account the various stakeholders' desires"* |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"starting with the building of a network model for the Great Lakes and connecting river flows from Lake Superior to the Atlantic Ocean"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"The water level in each lake is determined by how much water enters and leaves the lake."* |
| `核心` **3 优化 · 3.5 调度与配置** | *"Establishment of algorithms to maintain optimal water levels in the five lakes from inflow and outflow data for the lakes."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"How sensitive is your algorithm to changes in environmental conditions (e.g., precipitation, winter snowpack, ice jams)?"* |

**数据形态**：混合（五大湖水位/流入流出时间序列 + 网络拓扑；附件）｜**场景**：水资源 / 基础设施

### 2024 E — Sustainability of Property Insurance

**问题抽象**：为财产保险公司建「是否承保」的风险定价模型（在极端天气频率上升的区域），
再建一个社区层面的「建筑保护优先级」模型，并在一处历史地标上把两者合起来给建议。
**结构化**：`要求`＝保险公司的承保决策模型（含何时该承担风险、业主能做什么）+ 用两个不同大洲的区域演示 + 迁移到「在哪建、如何建」的评估 + 社区层面识别应保护建筑的方法与保护力度 + 在一处历史地标上应用并给社区写信 ｜ `已知`＝题面给的行业统计（2022 年赔付增 115%、保费到 2040 年涨 30–60%、全球保障缺口均值 57%）+ 3 篇参考文献；**无附件数据集** ｜ `约束/不确定性`＝承保太保守会失去客户、太激进会赔穿；保障缺口与再保险能力；文化/历史/社区意义难以定价

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **9 决策与博弈 · 9.3 风险与效用** | *"Develop a model for insurance companies to determine if they should underwrite policies in an area that has a rising number of extreme weather events."* |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"Develop a preservation model for community leaders to use to determine the extent of measures they should take to preserve buildings in their community."* |
| `核心` **2 评价与排序 · 2.5 分级/阈值划定** | *"community that should be preserved and protected due to their cultural, historical, economic, or community significance?"* |
| `附带` **1 预测 · 1.3 情景与概率预测** | *"As climate change increases the likelihood of more severe weather and natural disasters"* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"there is resilience in the system to cover the cost of future claims while also ensuring long-term health of insurance companies"* |

**数据形态**：混合（两个大洲的区域天气/赔付数据 + 地标资料）｜**场景**：保险 / 气候适应

### 2024 F — Reducing Illegal Wildlife Trade

**问题抽象**：选一个客户并为其设计一个**数据驱动的五年项目**使非法野生动植物贸易显著下降，
量化该项目的预期影响、成功概率与敏感性。
**结构化**：`要求`＝客户是谁及其能做什么 + 项目为何适合该客户（含文献与自有分析的支撑）+ 所需的额外权力与资源 + 项目执行后的可测影响及其分析依据 + 达到目标的概率与情景化敏感性分析 + 给客户的一页备忘录 ｜ `已知`＝题面给的量级（每年约 265 亿美元、全球第四大非法贸易）+ 1 篇参考文献；**无附件数据集** ｜ `约束/不确定性`＝客户与项目都要自己选并论证；「可测影响」需自己设计度量；复杂系统视角可选但要论证取舍

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"In other words, what will the measurable impact on illegal wildlife trade be? What analysis did you do to determine this?"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"How likely is the project to reach the expected goal? Also, based on a contextualized sensitivity analysis, are there conditions or events that may disproportionately aid or harm the project's ability to reach its goal?"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"You are to develop a data-driven 5-year project designed to make a notable reduction in illegal wildlife trade."* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"If you choose to leverage a complexity framework in your solution, be sure to justify your choice by discussing the benefits and drawbacks of this modeling decision."* |
| `附带` **8 网络与图 · 8.3 传播与级联** | *"you may also consider illegal wildlife trade as part of a larger complex system"* |

**数据形态**：混合（文献 + 自采数据）｜**场景**：生态保护 / 刑事政策

### 2025 A — Testing Time: The Constant Wear On Stairs

**问题抽象**：由**观测到的磨损形态**反推这组台阶的**使用史（频次/方向/并行人数）与年代**，还要给出估计的**可靠程度**，且测量方案必须非破坏、低成本、可实施。
**结构化**：`要求`＝年代 + 使用史（频次/方向/并行人数）+ 该估计的可靠性 + 材料来源是否与假定一致 ｜ `已知`＝磨损形态（测量方案自定）+ 可能存在的**不精确**年代估计与史料 ｜ `约束/不确定性`＝测量须**非破坏、低成本、小团队 + 简单工具**；年代估计不精确、史料可能对应不到具体台阶 → **这是逆问题（由观测反推历史过程），不是「仿真」**

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"Your model should provide some basic predictions **given the patterns of wear** on a particular set of stairs: How often were the stairs used? Was a certain direction of travel favored…? How many people used the stairs simultaneously?"* |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"What is the age of the stairwell and how reliable is the estimate? … Can the source of the material be determined?"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"how reliable is the estimate"*；测量约束：*"non-destructive, the cost must be relatively low … minimal tools"* |

**数据形态**：无数据(纯机理/假设)（自设测量方案 + 假设）｜**场景**：考古 / 材料 / 人因

### 2025 B — Managing Sustainable Tourism

**问题抽象**：建「游客—收益—承载力—措施」的系统模型，在**明确目标与约束**下**优化管理措施**，给出预测、措施效果与建议，并说明模型能否迁移到别的目的地。
**结构化**：`要求`＝措施组合（明确何者是被优化的、何者是约束）+ 预测 + 支出如何**反馈**进模型 + 敏感性 ｜ `已知`＝Juneau 案例事实（2023 年 160 万邮轮乘客、约 3.75 亿美元收益、冰川退却、已实施的税费/每日上限定额）；**无给定数据集** ｜ `约束/不确定性`＝当地承载力与居民负担、环境退化、利益相关者冲突；措施效果不确定（题干点名要敏感性分析）

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"**State clearly which factors you are optimizing, and which factors serve as constraints.** Include a plan for expenditures from any additional revenue and show how these expenditures feed back into your model"* |
| `核心` **4 机理建模与仿真 · 4.6 反馈结构与动态演化** | 同上 *"**feed back into your model**"*；*"Include a sensitivity analysis and discuss which factors are most important"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"a one-page memo to the tourist council of Juneau outlining **your predictions, the effects of various measures**"*；*"Demonstrate how your model could be **adapted to another tourist destination**"* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Include a **sensitivity analysis** and discuss which factors are most important"* |

**数据形态**：无数据(纯机理/假设)（Juneau 案例数据需自采）｜**场景**：旅游 / 公共政策

### 2025 C — Models for Olympic Medal Tables

**问题抽象**：只用给定数据建**各国奖牌数预测模型**（含不确定性与**预测区间**、含**尚未得牌国家**与首金概率），并**估计事件/主办/「名帅」等因素的效应量**。
**结构化**：`要求`＝各国金牌/总奖牌数的**预测 + 预测区间**；尚未得牌国家的**首金概率**；「名帅」效应**贡献多大**；项目设置对成绩的影响 ｜ `已知`＝**题面给定**的历届奖牌榜、主办国、各届项目数与运动员级明细（题干限定 *"ONLY use the provided data sets"*） ｜ `约束/不确定性`＝只能用给定数据；**大量零计数**（60+ 国未得牌）；届次样本量小

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.2 回归/相关预测** | *"Develop a model for medal counts for each country … Include **estimates of the uncertainty/precision** … Include **prediction intervals** for all results"* |
| `核心` **1 预测 · 1.5 零膨胀/受限计数预测** | *"**countries that have yet to earn medals**; what is your projection for how many will earn their first medal … What sort of **odds** do you give"* |
| `核心` **5 统计推断与因果 · 5.2 回归系数与效应量** | *"Examine the data for evidence of changes that might be due to a **'great coach' effect**. **How much do you estimate such an effect contributes** to medal counts?"*；*"How do **the events chosen by the home country** impact results?"* |
| `核心` **7 分类与聚类 · 7.1 监督分类/识别** | *"Which countries do you believe are **most likely to improve**? Which will do worse than in 2024?"* |

**数据形态**：面板（国家 × 届次 + 运动员级明细；题面限定只能用给定数据）｜**场景**：体育

### 2025 D — A Roadmap to a Better City

**问题抽象**：为**多利益相关者**的城市交通网络建**网络模型**（题面给了车流量数据），给出**改进措施的优先级建议**，含桥梁中断这类情景。
**结构化**：`要求`＝面向多利益相关者的**改进优先级方案**与建议 ｜ `已知`＝巴尔的摩网络背景（已塌的 Key Bridge、US-40 分割社区、轨道不足）+ **官方提供的路段车流量文件** ｜ `约束/不确定性`＝利益相关者目标冲突；**网络中断**（桥塌）后的影响；地理/水域/土壤/天气干扰

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **8 网络与图 · 8.2 流量分配/路由** | *"**A file with vehicle counts on street segments is provided.** … you should **build a network model**(s) for some part or element of Baltimore's"* |
| `核心` **2 评价与排序 · 2.3 排序规则/权重设计** | *"goals are based upon identifying, **prioritizing**, and implementing initiatives"*；*"**recommending ways to improve** Baltimore's transportation network"* |
| `核心` **9 决策与博弈 · 9.1 多准则决策** | *"All of Baltimore's transportation plans affect **multiple stakeholders with differing perspectives**"*；中断情景：*"The rebuilding of a **collapsed bridge** (Francis Scott Key Bridge)"* |
| `附带` **3 优化 · 3.5 调度与配置** | *"recommending ways to improve"* |

**数据形态**：网络（官方提供的路段车流量附件 + 路网数据）｜**场景**：城市交通 / 基础设施

### 2025 E — Making Room for Agriculture

**问题抽象**：建**森林→农田演替的生态动力学模型（自然过程 + 人类决策）**，用它比较化学 / 有机农业路径并给管理建议。
**结构化**：`要求`＝演替**轨迹**（食物网/物种随时间的动态）+ 管理策略（去草剂、引入蝙蝠等）的**稳定性后果** + 有机农业情景比较 ｜ `已知`＝可自设假设，或用 *"a real historic sample of this kind of evolution"*（文献/历史数据）；**无给定数据集** ｜ `约束/不确定性`＝自然过程与人类决策**耦合**；季节性与农药；去掉草剂后生态系统是否失稳；成本 vs 可持续性

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.2 生态/生物动力学** | *"Build a basic **food web model** … Include the producers and the consumers as well as the impact of the agriculture cycle and its **seasonality which changes the system dynamics over time**"*；*"**Model bats as insectivores** … and as pollinators"* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Consideration should be given to **different scenarios with varying components** of organic farming"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Discuss aspects such as pest control, crop health … and **cost effectiveness**"*；*"economic trade-offs as well as sustainability"* |
| `附带` **9 决策与博弈 · 9.1 多准则决策** | *"Advise the farmer on what methods should be employed"* |

**数据形态**：无数据(纯机理/假设)（假设 / 文献 / 真实历史样本）｜**场景**：农业 / 生态

### 2025 F — Cyber Strong?

**问题抽象**：提出「**什么算强的国家网络安全政策**」的理论，并用跨国数据找**有效性模式与相关/因果**（题面明确**不要求新建指数**）。
**结构化**：`要求`＝「强政策」的**理论（构成要素）** + 政策**有效性的模式/相关性**（并讨论本国国情的作用） ｜ `已知`＝各国公开的政策/法律文本 + 网络犯罪分布数据（题面提示 ITU GCI、VERIS/VCDB，鼓励另找但须核验） ｜ `约束/不确定性`＝**跨国管辖权**、**大量未报案/瞒报**（机构宁付赎金）、政策生效时间不一、数据质量与完整性（题干要求讨论局限）

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"identify parts of a policy or law that are **particularly effective (or particularly ineffective)** in addressing cybercrime"*；*"it may be relevant to consider **when each policy was adopted**"*；*"seek meaningful patterns in the **effectiveness** of national cybersecurity policies"* |
| `核心` **2 评价与排序 · 2.1 指标体系构建** | *"**Develop a theory for what makes a strong national cybersecurity policy** and present a data-driven analysis to support your theory"* |
| `核心` **7 分类与聚类 · 7.2 无监督聚类/分段** | *"How is cybercrime **distributed across the globe**? Which countries are **disproportionately high targets** … Do you notice any **patterns**?"* |

**数据形态**：混合（跨国政策/法律文本 + 网络犯罪分布；自采）｜**场景**：网络安全 / 公共政策

### 2026 A — Modeling Smartphone Battery Drain

**问题抽象**：为智能手机的锂离子电池建**连续时间**的状态电荷（SOC）模型，用它预测不同初始电量与使用情景下的
剩余可用时间，并做假设/参数/使用模式的敏感性分析与建议。
**结构化**：`要求`＝连续时间模型（SOC 随时间）+ 各贡献项（屏幕/处理器/网络/GPS/后台）+ 不同情景下的 time-to-empty 与其不确定性 + 敏感性 + 面向用户与操作系统的建议 ｜ `已知`＝题面给的物理背景（锂离子电池、温度影响、老化影响）；数据可自采或引用公开测量（须开放许可、可自由使用） ｜ `约束/不确定性`＝**明令不得**只做离散曲线拟合/逐步回归/黑箱机器学习，必须有**显式连续时间机制模型**；参数须论证与验证；老化会降低有效容量

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Develop a model to represent the state of charge using a continuous-time equation or system of equations."* |
| `核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"You may collect or use data for parameter estimation and validation."* |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Use your model to compute or approximate the"*；*"under various initial charge levels and usage scenarios."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"Examine how your predictions vary after making changes in your modeling assumptions, parameter values, and fluctuations in usage patterns."* |
| `附带` **9 决策与博弈 · 9.4 机制/规则设计** | *"How might an operating system implement more effective power-saving strategies based on insights from your model?"* |

**数据形态**：混合（可自采或引用公开数据做参数估计与验证）｜**场景**：消费电子 / 能源

### 2026 B — Creating a Moon Colony Using a Space Elevator System

**问题抽象**：为「把 1 亿吨材料送上月球」比较三种运输方案（太空电梯 / 传统火箭 / 组合）的**成本与时间线**，
并做可靠性、水需求与环境影响的扩展。
**结构化**：`要求`＝三种情景下的成本与时间线 + 非完好状态（缆绳摆动、火箭失败、电梯故障等）下的变化 + 殖民地为 10 万人供水一年的额外成本与时间 + 各方案对地球环境的影响与改进 + 给 MCM 局的信 ｜ `已知`＝题面给的系统参数（3 个 Galactic Harbour 相隔 120°、每条缆绳 10 万 km、电梯年运力 17.9 万吨、火箭每次 100–150 吨、10 个发射场位置） ｜ `约束/不确定性`＝假设「完美条件」，但**同时要求**讨论非完好状态；材料总量 1 亿吨、时间从 2050 年起；成本参数需自设或引用

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"You will need to compare the Modern-Day Space Elevator System's three Galactic Harbours to traditional rockets launched from selected rocket bases."* |
| `核心` **3 优化 · 3.5 调度与配置** | *"utilize a mathematical model to determine the cost and associated timeline in order to transport material to build a 100,000 person Moon Colony"* |
| `核心` **3 优化 · 3.4 动态与随机** | *"To what extent does your solution(s) change if the transportation systems are not in perfect working order"* |
| `核心` **3 优化 · 3.2 离散/组合** | *"a. using the Space Elevator System's three Galactic Harbor's alone, b. traditional rocket launches from existing bases alone (you may choose which facilities to use), or, c. some combination of the two methods."* |
| `附带` **3 优化 · 3.3 多目标/权衡** | *"Discuss the impact on the Earth's environment for achieving the 100,000-person Moon Colony under the different scenarios."* |

**数据形态**：无数据(纯机理/假设)｜**场景**：航天 / 工程物流

### 2026 C — Data With The Stars

**问题抽象**：由**未知的粉丝投票**与已知的评委评分、淘汰结果**反推**每对选手每周的粉丝票数，
再用它比较两种合并规则、评估选手特征的影响，并设计一套更「公平」的规则。
**结构化**：`要求`＝估计粉丝票的模型（含与淘汰结果的一致性度量、估计的确定性）+ 用估计票数比较 rank 与 percentage 两种口径、检验争议案例、评估「评委从末二选一」的方案 + 选手特征（职业舞者、年龄、行业）对评委分与粉丝票影响是否同向 + 提出并论证一种新的合并系统 + 给制片人的备忘录 ｜ `已知`＝附件 `2026_MCM_Problem_C_Data.csv`（第 1–34 季：选手信息、结果、每周评委分）+ 表 1 字段说明；可另行补充但须注明来源 ｜ `约束/不确定性`＝粉丝票**保密且未知**；合并规则变更的确切季次只能「合理假设」；估计的确定性逐周逐人不同

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **6 反演与参数估计 · 6.1 由观测反推参数/历史** | *"Develop a mathematical model (or models) to produce estimated fan votes (which are unknown and a closely guarded secret) for each contestant for the weeks they competed."* |
| `核心` **5 统计推断与因果 · 5.4 不确定性与敏感性** | *"How much certainty is there in the fan vote totals you produced, and is that certainty always the same for each contestant/week?"* |
| `核心` **2 评价与排序 · 2.4 方案比较** | *"Compare and contrast the results produced by the two approaches used by the show to combine judge and fan votes (i.e. rank and percentage) across seasons"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"Propose another system using fan votes and judge scores each week that you believe is more 'fair'"* |
| `核心` **5 统计推断与因果 · 5.2 回归系数与效应量** | *"How much do such things impact how well a celebrity will do in the competition? Do they impact judges scores and fan votes in the same way?"* |
| `附带` **2 评价与排序 · 2.3 排序规则/权重设计** | *"the combined scores from fans and judges are used to rank them from 1st to 3rd"* |

**数据形态**：面板（选手 × 周 × 季；附件）｜**场景**：电视娱乐 / 投票制度

### 2026 D — Managing Sports for Success

**问题抽象**：为一个职业球队建「动态决策 + 财务」的管理模型，在球员获取与联赛规则的约束下最大化球队利润与价值，
并给出赛季策略与扩张情景下的调整。
**结构化**：`要求`＝动态决策模型（随球队表现与经济条件调整杠杆）+ 球员获取策略（选秀/自由球员/交易等）+ 联赛扩张下的策略变化与新队位置的影响 + 一项自选商业决策的最优策略（票价/场馆/球员股权/媒体/赛区等）+ 给球队老板与总经理的信 ｜ `已知`＝题面给的行业背景（WNBA 的财务变化、薪资帽/奢侈税等联盟规则的存在）；公开的体育与财务数据自采（球队须 ≥5 人同时协作且属职业联盟） ｜ `约束/不确定性`＝联盟规则（薪资帽、名单、赛程、媒体合同）由外部决定；伤病、交易机会、税率与利率随时间变化；扩张同时影响所有球队

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **3 优化 · 3.4 动态与随机** | *"Design a dynamic decision-making model that would help your team owner and general managers adjust their leverage in response to changing team performance and economic conditions."* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"The goal is to maximize team profit and value while managing team structure and performance."* |
| `核心` **3 优化 · 3.2 离散/组合** | *"develop a strategy to acquire players for next season using the standard practice for your team's league such as a draft, free agency, trades, transfer fees, or other standard practices"* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"Use your model to decide how your team's strategy should change from your initial strategy during a season with league expansion."* |
| `附带` **9 决策与博弈 · 9.3 风险与效用** | *"the owner must decide how much to finance with debt versus equity and whether risks in the form of seeking better team performance with associated additional costs are worth taking"* |
| `附带` **2 评价与排序 · 2.1 指标体系构建** | *"there continue to be challenges to build statistics that quantify the value of player talents and performances"* |

**数据形态**：面板（体育统计 + 财务；自采）｜**场景**：职业体育 / 企业管理

### 2026 E — Passive Solar Shading

**问题抽象**：为两所虚构大学建被动式遮阳的**热工模型与设计**：估计得热与冷负荷削减、优化遮阳几何与热质量配置，
并迁移到不同纬度与未来气候。
**结构化**：`要求`＝Sungrove 主楼的改造设计（优化全年供暖与制冷）+ 面向 Borealis 的热质量方案 + 迁移到其他纬度的设计考量 + 新学生中心的遮阳策略（含得热预测、负荷削减、季节变化、采光与遮阳的权衡）+ 给其中一所大学的信 ｜ `已知`＝题面给的建筑几何与围护参数（60m×24m、长边东西向、南向窗墙比 45%、其余 30%、双层玻璃 + 砖饰面）+ 太阳位置与气候背景 ｜ `约束/不确定性`＝要计入**未来气候条件**；采光与遮阳冲突；材料与热质量的选择影响性能；**并非真实**的校园参数需自行设定并写明

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **4 机理建模与仿真 · 4.1 物理/化学机理建模** | *"Predicting solar heat gain"* |
| `核心` **6 反演与参数估计 · 6.2 逆向设计** | *"design a retrofit for Sungrove University's Academic Hall North that optimizes heating and cooling throughout the academic year"* |
| `核心` **3 优化 · 3.1 连续/非线性** | *"the typical calculations make use of the angle of the sun at solar noon on the Summer and Winter Solstices to calculate the optimal extension of a shade over a window"* |
| `核心` **3 优化 · 3.3 多目标/权衡** | *"Evaluating the tradeoffs between daylighting needs and shading effectiveness"* |
| `附带` **1 预测 · 1.3 情景与概率预测** | *"their passive solar strategy design must perform well not only today, but under projected climate conditions well into the future"* |

**数据形态**：空间/地理（建筑几何 + 太阳位置 + 气候）｜**场景**：建筑节能 / 能源

### 2026 F — To Gen-AI, or Not To Gen-AI (or how to Gen-AI)? That is the Question!

**问题抽象**：为三类职业（STEM / 技工 / 艺术）各建「Gen-AI 冲击下未来」的模型，
并据此为三类院校的专业设置给出建议。
**结构化**：`要求`＝选定三类职业并建数据驱动的未来模型（含数据来源与驱动因素的论证）+ 为每个职业指定一所院校与专业并给出建议（该扩张还是收缩、教什么、如何支持就业）+ 除就业外还应考虑哪些因素及模型如何变 + 建议的可推广范围 ｜ `已知`＝可引用「未来工作」的既有研究（须注明用法）；数据自采 ｜ `约束/不确定性`＝Gen-AI 的轨迹本身不确定；「成功」的判据不止就业；三个职业分属不同院校类型

| L1 · L2 | 支撑句 |
| :-- | :-- |
| `核心` **1 预测 · 1.3 情景与概率预测** | *"Design a data-informed model to explore the future of each of your three chosen professions, given the current trajectory and expected impacts of Gen-AI."* |
| `核心` **9 决策与博弈 · 9.4 机制/规则设计** | *"what do you recommend to best support the employability of their graduates? Be sure to support your recommendations with the results of a mathematical model"* |
| `核心` **5 统计推断与因果 · 5.3 因果/政策评估** | *"Should the program of study grow or shrink (graduate more or fewer people) as a result of changes in the career due to Gen-AI?"* |
| `附带` **2 评价与排序 · 2.1 指标体系构建** | *"perhaps employment demands are not the only way to measure the success of the institutional policies you are proposing. What other factors do you believe should be considered"* |

**数据形态**：混合（既有研究文献 + 自采劳动市场数据）｜**场景**：教育政策 / 技术冲击
