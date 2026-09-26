"""公式判据 D1/D2/D3（Task 5）：编号检出、引述句、裁图无水印。

| # | 判据 | 参照 | 独立吗 |
| :--- | :--- | :--- | :--- |
| **D1-a** | 机制层：`len(产出裁图) == len(检出编号)` | **无独立参照** | **否**（见下） |
| **D1-b** | 硬判据：逐份 `检出数` vs **R1 = 该篇 md 里整行只有编号的行数** | md 是 **Task 3 的产物、不由本任务代码产生** | 是 |
| **D1-c** | 硬判据：逐份 `检出数` vs **R2 = `pdftotext -layout` 行尾 `(N)` 数** | **不同引擎、不同实现** | 是 |
| **D1-d** | 硬判据：**有参照（R1 ≥ 5）而检出 = 0** 的篇 → 硬失败 | R1 | 是 |
| **D2-a** | 每个 `.context` 的 `REF: (N)` 能在该篇 md 里定位 | md | 是 |
| **D2-b** | 每个 `WHERE:`/`CITE:` 引述句能在**空白归一化后**的 md 里定位（逐份计数） | md | 是 |
| **D2-c** | 计数型硬判据：**md 有显式引用而 `.context` 抽出 0 条 → FAIL**（条数一律**从产物文件读回**，不用实现自报的数） | md 侧实测 40 处 / 11 份 | 是 |
| **D2-d** | 分叉 tripwire：实现自报的 `REF/CITE/WHERE` 条数必须与产物文件里读回的条数**逐项相等** | 产物文件（不是自报） | 是（分叉即 FAIL） |
| **D3-a** | 机制层：`extract_all` 自报的 `n_stripped` 必须等于本脚本**另行**算出的水印对象数（分叉即 FAIL） | C4 同一谓词 `watermark.find_watermark_xrefs` | 是（分叉 tripwire） |
| **D3-b** | 产出图像素层：C4 的 `strip_provenance` **原样调用**（黑盒 A/B 差分） | 见下「D3-b 怎么复用 C4 的谓词」 | 是 |

## D1-a **只对「渲染/落盘」环节有区分力，对「检出」环节零区分力**（必须写明）

`D1-a` 的两边调的是**同一个函数**（产出的张数由检出的条数决定），所以差额**按构造恒为 0**。
任务书一节点名的第七例「判据在什么都没验的情况下报绿」正是它：`2517690` 丢掉 20 条公式，
`D1-a` 照样印 PASS。它**唯一**能抓的是落盘环节（少写一张、名字拼错、写进别的目录）。
真正的区分力在 D1-b / D1-c / D1-d，而它们的参照（md / pdftotext）**不由本任务代码产生**。

## D2-a 的强度声明（**与 D1-a 同级，必须写明**——任务书「凡近乎恒真的判据都要写明边界」）

`D2-a` 的谓词是「`.context` 里那个编号**出现在**该篇 md 的空白归一化全文的**任意位置**」
（`re.search(r"\(N\)", md_ns)`）。两侧是同一条流水线的产物（`.context` 由 `formulas` 写、
md 由 `textmd` 从同一份 PDF 重排），而流水线内部对同一批编号做过同一套归一化——
**对「同一条流水线的产物之间的一致性」它近乎恒真**：

* 它能抓的**只有**一种形态：`.context` 里的编号是**凭空写出来的**（md 全文里根本没有
  这个 `(N)` 字符串）——即 `context_text` 把编号**写错**（如 `num + 90`）。
  变异 M6 实测的正是这一条。
* 它**抓不住**的：编号定位到了**别处**（md 里存在这个 `(N)`，但不是那条公式的）；
  引述句归属错；`REF` 的编号与产出图名不一致。前者要靠人看逐份的 `SRC:` 行，
  后两者分别由 D2-b / D2-d 与 D1-a 的落盘名单覆盖。
* 它与 `D2-b` **不可互相替代**：`D2-b` 判的是**整句引述**能在 md 里定位（长串，
  区分力远高），`D2-a` 判的是**编号 token**（短串，近乎恒真）。

**同理，报告里的 `WHERE` 条数没有任何独立参照，不参与判定**（属「不适用」）：
`where` 引述句的**归属**是一条先验（「位置在它之前、最近的那条检出编号」，见
`formulas` 模块 docstring），md 侧没有与之对应的可数对象，故没有任何一层判它。
它在报告里只作**覆盖指标**印出。

## 「已解释」的定义（任务书二节，一字不改地照办）

> 「已解释」只能陈述**关于语料的实测事实**（那条行是表格单元格 / 页脚 / 引用 / 年份 /
> 非公式，附**页码 + 坐标 + 复算命令**）。**禁止把检测器自己的取舍写成解释**——
> 「被我的右带约束剔除了」「被递增约束剔除了」「不在候选集里」**一律不算解释**。

本脚本把这条做成**可核的形状**：每条差额都必须被下列**具名类别**之一解释，且每条解释都
**带页码 + 坐标 + 原文**（页与坐标取自 PyMuPDF `get_text("dict")` 的 line bbox，逐条印在
报告里，任何一条都能用 `build/t5_probe2.py <stem> <页>` 一类命令复算）：

| 类 | 判据（可核谓词） | 方向 |
| :--- | :--- | :--- |
| **A 行内合并** | 该编号在原件里**与公式体同处一个文本行**（`Candidate.score == 1`，即该行文本 ≠ 编号 token） | 检出有、参照没有 |
| **B 引擎假阳性** | 该号**没有**被证明是独立编号行（`n_proven == 检出数`），且参照侧命中行里**至少有一条确非编号行**：行内编号 token 之前有 ≥3 个连续 ASCII 字母（正文词/题注），或 token 紧贴前一字符（`#(24)`、`𝜃(1)` 一类行内标记） | 参照有、检出没有 |
| **C 第二引擎漏检** | 该编号在原件里是**整行只有编号**（`score == 0`），`pdftotext` 那一行的行尾不是它 | 检出有、R2 没有 |
| **D 参照口径漏** | 该编号**行尾的 token** 排成 `( N )`（括号内**确有**空白——这才是严格口径的正则漏它的原因），**严格口径的正则**两侧同漏 | 检出有、参照没有 |
| **E 语料侧非公式（编号 0）** | 编号 0，而且**没有任何独立证据**（md 纯编号行 / 原件侧整行只有编号的文本行 / 几何口径）证明该号有编号行——该行确非编号行（见下「E 类的边界」） | 参照有、检出没有 |
| **F 引述句指向的编号不在检出集** | `CITE:` 没写进 `.context` 是因为它引用的编号**没被检出**（D2-c 专用） | 计数差 |

**未解释 = 不属于以上任何一类 → 直接判 FAIL。** 这条就是本任务书要的「只许语料侧解释」：
它使 M1（令检测器丢掉真编号）下那些条**不可能**落进任何语料类别。

### E 类的边界（复审 Minor 4：不能把它写成与 B/D 对称的类别）

E 类的三个**结构**边界（都是实测的，不是措辞问题）：

1. **它在 R1 层不可达**（**这一条我复算过，理由与「参照为空」不同**）：要把编号 0 放进
   R1 的参照，就必须有一条「整行 `(0)`」的 **md** 行——实测**全批只有 1 条**（`2507817`）。
   而**同一条行也进 `proven`**（`md_w(0) ≥ 1`）：若检出里没有它，则
   `proven ≥ 1 > 检出数 = 0` ⇒ 走**未解释**，**永远到不了 E**；若检出里有它，则差额不存在。
   故 E 在 R1 层**结构上不可达**——它与「参照为空」不是一回事（参照**不**为空，是那条行
   把封条先点着了）。R2 层不同：`pdftotext` 的命中行**不是** md 行，`θ(0)` 类行内标记
   在那里的行尾恰好是 `(0)`，而它与 `proven` 的三条证据都不相干（md 纯行 0、原件纯行 0、
   几何口径 0）——E 就是这样被触发的（`2524070` p9）。
2. **它被 B 抢先**：判定顺序是「封条 → `detected_count > 0` 的 B → E」，故一个**被检出**的
   编号 0（如 `2507817` p6 那条整行 `(0)`，它是该篇的真编号）永远走 B 而不走 E。
3. **它的措辞不得与 `formulas.MIN_NUM = 0` 相反**：编号 0 在本任务里**是合法编号**
   （理由见 `formulas.MIN_NUM` 的注释：`2507817` 的 `(0)` 位置与全篇其它编号完全相同）。
   E 类说的**不是**「编号 0 不是编号」，而是「**这一条**行内标记没有任何独立证据证明
   它是一条编号行」——判据是那三条证据（md 纯行 / 原件纯行 / 几何口径）全为 0，
   **不是** `num == 0` 本身。

## 封条：**检测器丢的真编号不得被 B 类吞掉**（Task 5 复审 Critical 1）

「参照有、检出没有」有**两种成因**，必须分开：

1. 参照那一行**确非编号行**（题注/正文/伪代码/行内标记）→ 语料侧事实，B 或 E；
2. **检测器把一条真编号丢了** → 检测器侧问题，**必须**记「未解释」并判 FAIL。

判定的谓词是**关于语料的实测事实**，与实现的候选口径无关：

> `n_proven(num)` = `max(md 侧整行只有编号的行数, 原件侧整行只有编号的文本行数, 几何口径命中数)`
> （三者观测的是**同一批原件行**的三个视角，故取 max 而不是相加，避免同一条物理行被数两次）。
>
> **`n_proven(num) > 检出里该号的出现次数` → 必记「未解释」**，B/E 一律不许用。
> 只有在 `n_proven <= 检出数` 时，那一行才允许被称为「不是编号行」。

## 几何口径：**「这条行尾 token 是不是落在编号列右缘」**（本轮换的地基）

**上一版为什么不够**（复审本轮逐条实测的形态）：`proven` 的两个视角
（md 纯行 / 原件纯行）都只认「**整行只有编号**」——而本语料有 **11 条真编号与公式体
排在同一个 PyMuPDF 文本行**（`2517273` (13)(14)、`2504223` (20)(21)(22)、
`2517199` (4)(7)(8)、`2501869` (11)、`2507692` (13)、`2508861` (6)）。
这 11 条**两侧都不是纯行** ⇒ `proven == 0` ⇒ 封条**永不触发** ⇒ 检测器丢掉它们时
逐条落进 B 类「已解释」。观测口径太窄，所以**加宽观测口径本身**，而不是再加一张网。

**新视角的谓词（可核，逐条复算见 `tests/papers/recon/formula-geom-scan.py`）**：

> 一条文本行的**行尾 token 就是 `(N)`**，**且**该 token 的 **x1 落在本页「编号列右缘」
> ± `EDGE_TOL` 之内**。「编号列右缘」由**本页其它编号行**（= 该页整行只有编号的行）的
> token x1 **逐页**推出；本页一条纯编号行都没有时，退到**本篇**的同一集合。
> **没有任何全局绝对常量**（页宽、比例、字号都没进来），符合任务书约束 A。

* token 的 bbox 用 **`get_text("rawdict")` 的字符级 bbox** 求和，**不是整行 bbox**——
  整行 bbox **含行尾空白**，会把「靠不靠右」这个量污染掉（实测 `2517199` p8 的 `(4)`：
  行 bbox x1 = 508.4 而 token bbox x1 = **505.4**；`2508861` p9 的 `( 6 )`：520.4 vs 515.4）。
* 行内引用（`Table 5: … Equation (11)`、`… such as Germany (20) and …`）的 token 落在
  段落中间，x1 与编号列右缘差 **85.7–272.2pt**（4 条远缘实测值）→ 仍留 B 类；
  第 5 条 `2513705` 的 `(20)` 所在那一篇**没有任何纯编号行**，连右缘都推不出（见 §九.2）。

**这一层是「存在性证明」，不是「计数」——理由是实测的**（`formula-geom-scan.py` §C）：

| 量 | 实测 |
| :--- | :--- |
| 11 条「编号与公式体同行」真编号的 |Δ| | **0.0（10 条）** · **2.7（1 条**：`2517273` (14)，公式行超出版心**）** |
| 落在同一容差内的**非编号行**（假阳性） | **2 条**：`2502617` p10 `… includes two steps. (1)`（Δ=+0.2）、`2501869` p3 `Task 1 … forecast: (1)`（Δ=+0.2） |
| 能分开这两类的容差 | **不存在**：假阳性的 |Δ| (0.2) 比真编号的最大 |Δ| (2.7) 小一个量级 |

即：**几何口径看得见真编号，但它也把两条「正文行恰好排到版心右缘、行尾又正好是
`(N)`」的行圈进来了**。故本脚本**只把几何口径当 0/1 的「存在性证明」用**
（`geom_exists(num) = 1 if 有任何一条几何命中行 else 0`），**绝不用它去抬高任何计数**：
一旦拿它当计数，`2502617` 的 `(1)`（检出 1 条、几何看到 2 条）就会变成「未解释」——
那是**把 B 级证据误升格**，正是复审点名不许发生的事。`max`（并集）而不是相加，
理由同前：三个视角看的是同一批物理行。

**第一版为什么会被绕过**（复审逐字举出的实例）：它把 B 类的「编号 token 之前有正文词」
测试作用在 **`pdftotext` 那一行**上，而本语料里**「编号与公式体同行」的公式行**
（`2504188` `BS Accessibility(Ci, S j ) (6)`、`2502617` `max S = s Cadd (7)`、
`2514362` `Effect Intensity = Average Mc,s,t for X = 1 . (20)` …）长得跟题注**一模一样**。
于是检测器丢掉真编号时，那些号逐条落进 B 类＝「已解释」，`未解释` 恒为 0、判据不喊。
**现在它们必落「未解释」**：`2504188` 的 `(6)` 在 md 侧有整行只有编号的行、在原件侧也有
（`n_proven = 1 > 0`）→ 不许解释。

**差额上界**：`D1-b` / `D1-c` 的**未解释条数必须是 0**（硬条件，不参与上界）。差额本身
由**实测**给出，报告里印出逐份差额与合计、并按层印刷「差额条数 / 未解释条数」两列
（`D1 差额归类（逐层）` 那两行）。

**那两列的关系要说准**（复审 Minor 2）：**两列本来就不相等**（差额 = 已解释 + 未解释）——
上一轮放行时是 `R1 39 / 0`、`R2 31 / 0`，本轮参照变强后是 `R1 0 / 0`、`R2 8 / 0`，都不是同数。**被吞掉的差额让 `未解释` 这一列变小**（差额条数由
多重集减法算出、与分类器无关；分类器一旦把某条差额说成「已解释」，未解释就少一条）。
所以那两行末尾写的是「**未解释必须为 0**」，不是「两列必须相等」。

## 参照取数：**并集口径**（本轮参照变了，旧值留在 `recon/formula-recon.txt` §三）

D1-b / D1-c 的参照从「纯行口径」换成「**纯行 ∪ 几何口径**」的**并集**
（`max(纯行数, 几何存在性)` 逐号取，不相加——三者看的是同一批原件行）：

| 层 | 参照 | 新口径 | 旧口径（历史保留） |
| :--- | :--- | :--- | :--- |
| **R1** | `max(md 严格纯行数, 几何存在性)` | 报告里的 `R1'=` 列（括号里同时印原口径的 `R1=`） | 743（md 严格纯行） |
| **R2** | `max(pdftotext 行尾数, 几何存在性)` | 报告里的 `R2'=` 列（同上） | 767 |

**为什么这是收紧而不是放宽**：并集只会让参照**变大**（每条差额都要么更早出现、要么不变），
且锚点是**语料侧的行**（不是检测器的候选）——它使「检出有、参照没有」这一方向的差额
变小（那 11 条同行编号与 `2508861` 的 28 条 `( N )` 现在被参照数到了），代价是
**A / C / D 三类在本语料上不再出现**（逐条见报告；三类仍保留在代码里，对其他形态可达）。
C 类（第二引擎漏检）同样是参照变强的后果：`R2' = max(pdftotext 行尾, 几何口径)` 之后，
「检出有、R2 没有」这一方向的差额也消失了。

### 不变量**只对 R1 层成立**（旧版写成两层都成立，是**假陈述**，复审 Important 1）

`proven = max(md_w, pdf_pure, geom) >= max(md_strict, geom) = R1'`（因 `md_w ⊇ md_strict`，
`md_w` 是宽容口径 `MD_PURE_W`、`md_strict` 是 `MD_PURE`）⇒ **R1 层**「参照里有、检出没有」的
**任何一条**都不可能被解释掉（`proven >= 参照数 > 检出数` ⇒ 走未解释）。

**R2 层不成立**，且本语料当场把它证伪：`proven` 的三条证据（md 纯编号行 / 原件侧整行只有
编号的文本行 / 几何口径）与 `pdftotext -layout` 的行尾口径**不相干**——`pdftotext` 的行尾本身
包含**正文行尾**的 `(N)`。实例（本文件生成的放行报告里逐字可查）：
`2513705` 的 `(20)` —— `R2' = 1`（`pdftotext` 行尾 `'Countries with Strong Legal Measures: …
Germany (20) and Australia (20)'`）而该号 `proven = 0` ⇒ **没有任何独立证据**证明它是编号行
（md 纯编号行 0 条、原件侧整行只有编号的文本行 0 条、几何口径命中 0 条）——
**措辞与 `classify_extra_in_ref` 自己的 docstring（本文件 533-534 行）及放行报告里那三处
B 类说明串逐字一致**，不得在这里另写成「`proven = 0`」了事（同一份文件同一份证据两种说法
都成立会让人以为是两件事）⇒ `proven(0) > 检出数(0)` **不成立** ⇒ **按设计**走 B 类
（`[B 引擎假阳性] 20: … 参照侧命中行是 'Countries with Strong Legal Measures: …(20)'`）。
故 R2 层「参照有、检出没有」的**一部分按设计**走 B / E。
**R2 层对「丢真编号」的封死，靠的是 `geom` / `md` / `pdf_pure` 这三条证据本身**
（`proven > 检出数` ⇒ 未解释），**不是**上面那句 R1 的不变量。

**反过来，上面这条不变量带来一条**新的**静默丢失通路**（39 条号，本轮**具名登记**在
`tests/papers/recon/formula-recon.txt` §八 与本任务报告 §9）：这 39 条号的 **R1 参照完全由
几何口径给出**（`md_strict = 0`）；几何在其中任一条上失效 ⇒ 该号 `ref_r1(n) = 0` ⇒
**连差额都不会出现**（封条只在差额的分类里被咨询），检测器丢掉它也不会红。
39 = `2508861` 的 **28 条 `( N )` 排版号**（`md` 严格纯行 0、几何 1）+ **11 条「编号与公式体
同行」的真编号**（六份：`2517273` 2 / `2504223` 3 / `2517199` 3 / `2501869` 1 / `2507692` 1 /
`2508861` 1）。其中 11 条的**封条证明**也**只**由几何给出（`md_w = pdf_pure = 0`）；另 28 条的
封条证明另有 `md_w` / `pdf_pure` 两条支撑，但那两条**够不到**它们——参照为 0 时差额不存在。
若参照漏了而检测器**没**丢，方向变成「检出有、参照没有」：11 条同行号走 **A 类**
（行内合并，`candidate.score == 1` 分支）、28 条 `( N )` 号走 **D 类**（参照口径漏，
行尾 token 括号内含空白）——**两类都是「已解释」**，同样不红。

## D3-b 怎么复用 C4 的谓词（没有复制 C4 的逻辑）

`verify_c.strip_provenance(src, dimg, figures, watermark)` **原样调用**，只换一个
适配器 `_FigShim`：它的 `caption_blocks(doc)` 返回 `formulas.equation_captions(doc)`
（每条检出编号一个 `Caption`，`kind="eq"`），它的 `_page_items` / `band_of` 转发到
`figures` 与 `formulas`。之所以能这么接：产出图名是 `eq-{num:02d}-p{page+1}.png`，
而 `strip_provenance` 内部拼的正是 `f"{cap.kind}-{cap.num:02d}-p{cap.page+1}.png"`——
**逐字相同**，故 `verify_c.py` 一个字节都不用改，A/B 差分、三态、上界全部沿用 C4 的。

## 报告纪律（照抄 verify_b/verify_c，不自创）

* 一律 `report.flush()`（`write_bytes` + LF）、只写仓库相对路径（`report.path_audit`
  每次运行当场扫，命中即判 FAIL）；
* 报告写入**无条件执行**（`main()` 结尾、不在 try 内）——脚本崩了也不能把上一次的
  `RESULT: PASS` 留在库里冒充本次结论；
* 被测模块的 import 放在 `checks()` 体内；崩溃路径用 `report.fmt_exc`（**不得**用
  `traceback.format_exc()`）；
* 落点随样本口径分离（`tools/papers/report.py`）：全量跑写
  `tests/papers/reports/d-report.txt`（入库）；`--limit N` 写
  `tests/papers/reports-limited/d-report-limited-N.txt`（不入库），`RESULT` 行带
  `LIMITED` 后缀。
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
COLLECTION = "2025美赛O奖论文"

# `--limit` 的见证集。**不并入取样是不行的**：排序序里靠后的关键样本 `--limit 3`
# 取不到，变异演示会在看不见它的集合上"绿着通过"。
#
#   2517690  排序第 27 位。**本轮的头号见证**：真值 21 条且全递增，旧判据（右带 +
#            断一处即全弃）只出 1 条。它的 (2)–(10) 在 x1 = 498.0–502.9、该页文本栏
#            右缘 529.5——「靠右」失效的原始实例；也是 M1 变异下必须有 20 条落进
#            「未解释」的那一份。
#   2504188  排序第 30 位。32 条整行编号，旧口径「靠右」下 **0/32**（R3 全灭）；
#            且它**从 (4) 开始**编号（不是从 1）——链不要求从 1 起，是这条的见证。
#   2500759  排序第 13 位。7 条，旧口径 3 条（截断）。
#   2517273  排序第 37 位。41 条整行编号，旧口径只剩 1 条（右带）；本轮 43 条，
#            其中 (13)(14) 是**行内合并**（A 类）的实例。
#   2514461  排序第 20 位。**多行公式 + 编号上下都紧邻公式行**（任务书 Step 3 点名），
#            是裁图带取法（M5）的见证；23 条全入链。
#   2502617  排序第 7 位（`--limit 3` 取不到）。**复审 Critical 1 的见证**：它的
#            `max S = s Cadd (7)` / `min Env = CCO2 - Cenv (11)` 在 `pdftotext -layout`
#            里与公式体同行——第一版的 B 类谓词（「编号 token 之前有正文词 → 判不是编号行」）
#            正是在这类行上把**检测器丢的真编号**说成「已解释」。变异 M1/M7 的计数断言
#            必须有它在样本里，否则"被吞掉"这件事在 `--limit 3` 下看不见。
#            **本轮实测补充**：在 PyMuPDF 侧 `(7)` 是**整行只有编号**的行（p10 y=260.8
#            x1=540.0），只有 `pdftotext` 把它并进了公式行——故它是**纯行口径**的见证。
#            （「编号与公式体同行」的 11 条见 `formula-recon.txt` §八，都不在本见证集里：
#            它们是 `--limit 3` 取不到的那几份上的。）
#   2514362  排序第 11 位（`--limit 3` 取不到）。**复审本轮点名的三条逐实例断言之
#            一**（`2514362 (20)`）：它必须出现在 M1 的**未解释**清单里。它同时是
#            `(20)` 所在 p17 的**几何口径见证**（`(20)` 的 token x1=538.6）。
FOCUS = ("2517690", "2504188", "2500759", "2517273", "2514461", "2502617",
         "2514362")

# 参照侧的正则。**与 `formulas` 里对应的谓词逐字相同，但不 import 它**——参照必须与
# 实现分开：实现那份改宽/收紧了，这里不跟着变，会红（通则候选①「同一语义必须用同一
# 谓词」的另一半是：**参照侧要留一份独立的**，否则规格写错时两侧同错、判据不喊）。
MD_PURE = re.compile(r"^\s*\((\d{1,2})\)\s*$")
MD_PURE_W = re.compile(r"^\s*\(\s*(\d{1,2})\s*\)\s*$")
R2_TAIL = re.compile(r"\((\d{1,2})\)[ \t]*$")
CITE = re.compile(r"\b(?:Eq\.?|Equation)\s*\(\s*(\d{1,2})\s*\)", re.I)
# 引述句对账（D2-c）用的谓词：**作用在空白归一化后的文本上**，且**不带词边界**。
#
# 为什么两侧都要用它：`.context` 里的 `CITE:` 行是空白归一化过的（`formulas.nospace`），
# 而 `CITE` 的 `\b` 在 `…formulaisequation(2)` 这种粘连形上**匹配不到**（"equation" 前
# 一个字符是字母 → 无词边界）。若两侧各用一种形式，差额全是口径噪声、不是语料事实。
# 故 D2-c 的**对账**两侧都用 `CITE_NS`；`CITE`（带词边界，与任务书口径逐字相同）用来
# 数 **md 侧参照**那一行（实测全批 40 处 / 11 份，与任务书一致）。
CITE_NS = re.compile(r"(?:eq(?:uation)?\.?)\((\d{1,2})\)", re.I)
# 「行内编号 token 之前有正文词」= 那一行不是编号行（B 类）。
WORD = re.compile(r"[A-Za-z]{3,}")
# D1-d 的参照下界：R1 至少这么多条才认为"参照存在"。
D1D_MIN_REF = 5
# `pdftotext` 的尝试次数。本机实测：全量跑里它偶发返回 3221225794
# （Windows `STATUS_DLL_INIT_FAILED`，进程创建期资源问题，与 PDF 无关），**重试即成功**。
# 注意它**不掩盖**"这份 PDF 真的跑不出来"——那时三次都会失败、照样抛。
PDFTOTEXT_TRIES = 3
# D3-b 沿用 C4 的未验证上界（`verify_c.PROV_UNVERIFIED_CEILING` 的同一个值，
# **两处必须同步改**——C4 那边写明了它的实测依据是 1/43 = 2.33%）。
PROV_UNVERIFIED_CEILING = 0.10
# **几何口径的容差（pt）**。**量出来的，不是挑的**（逐条见
# `tests/papers/recon/formula-geom-scan.py` 的输出，§B/§C）：
#   * 11 条「编号与公式体同行」的真编号：|Δ| = **0.0 ×10** 与 **2.7 ×1**（`2517273` (14)）
#     （`2517273` (14) 的公式行本身超出版心，故它是这 11 条里的上界）；
#   * 取 3.0 = 上界 2.7 向上取整。
# **这个容差分不开真编号与两条假阳性**（`2502617` p10 / `2501869` p3 的正文行，
# Δ=+0.2）——故几何口径**只当存在性证明用**，不参与计数（见模块 docstring）。
EDGE_TOL = 3.0
STRIP_PROBE_MAX = 4


def _load_verify_c():
    """**按路径**载入 `tests/papers/verify_c.py`（`tests/` 不是包，不能 `import`）。

    D3-b 要**原样调用**它的 `strip_provenance`——那是本项目现行范式里
    「产出图确实来自置空之后的渲染」这条谓词，复制一份就等于又开一个会静默分叉的副本
    （通则候选①）。`verify_c.py` 一个字节都不改。
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("_verify_c", HERE / "verify_c.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def md_text(prob: str, stem: str) -> str:
    """该篇 md 的全文（Task 3 的产物，**本任务不生成它**）。"""
    from tools.papers import io
    return io.md_path(COLLECTION, prob, stem).read_bytes().decode("utf-8")


def md_pure_counts(text: str) -> tuple[Counter, Counter]:
    """md 侧的 R1（严格）与 R1w（括号内允空白），逐份的**编号多重集**。"""
    strict = Counter()
    wide = Counter()
    for ln in text.splitlines():
        m = MD_PURE.match(ln)
        if m:
            strict[int(m.group(1))] += 1
        m = MD_PURE_W.match(ln)
        if m:
            wide[int(m.group(1))] += 1
    return strict, wide


def r2_counts(pdf: Path) -> tuple[Counter, list[tuple[int, str]]]:
    """pdftotext -layout 侧的 R2（严格口径）：行尾 `(N)`。返回 (多重集, 命中行)。

    **容许重试**：本机实测在全量跑里 `pdftotext` 会偶发返回 `3221225794`
    （Windows `STATUS_DLL_INIT_FAILED`，进程创建期的资源问题，与 PDF 内容无关——
    同一份文件重试即成功）。故最多试 `PDFTOTEXT_TRIES` 次，**全部失败才抛**：
    重试掩盖不了"真的跑不出来"，因为那时三次都失败。
    """
    import time
    for attempt in range(PDFTOTEXT_TRIES):
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                             capture_output=True, timeout=600)
        if out.returncode == 0:
            break
        last = out.returncode
        time.sleep(1.0 + attempt)
    else:
        raise RuntimeError(
            f"pdftotext 连续 {PDFTOTEXT_TRIES} 次返回码 {last}（{pdf.stem}）"
        )
    text = out.stdout.decode("utf-8", "replace")
    cnt: Counter = Counter()
    hits: list[tuple[int, str]] = []
    for ln in text.splitlines():
        m = R2_TAIL.search(ln)
        if m and ln.strip():
            cnt[int(m.group(1))] += 1
            hits.append((int(m.group(1)), ln.rstrip()))
    return cnt, hits


def _where(lines: list[tuple], num: int, page: int | None = None) -> str:
    """`lines` = `[(页, bbox, 原文)]`；返回该编号所在行的位置串（解释用）。

    先找**行尾就是该号**的行（那是编号行本身），再退而找任意出现它的行
    （该情形会注明「该行行尾不是这个编号」，不让读者以为那是编号行）。

    `page` 给出**差额所在的那一页**时优先取同页的命中行（复审 Minor 6）：全篇搜第一个
    命中会指到**别页的题注**（例如 `2500836` 的 `(11)` 真编号在 p14，而引用它的表题注
    也在 p14、按行序搜索却可能先撞上别的页）——解释串必须指向**差额那一页**的行。
    """
    tail = re.compile(r"\(\s*%d\s*\)\s*$" % num)
    anyw = re.compile(r"\(\s*%d\s*\)" % num)
    for rx, exact in ((tail, True), (anyw, False)):
        for want_page in ([page, None] if page is not None else [None]):
            for pno, bbox, t in lines:
                if want_page is not None and pno != want_page:
                    continue
                if rx.search(t):
                    pos = (f"p{pno + 1} y={bbox[1]:.1f} x0={bbox[0]:.1f} "
                           f"x1={bbox[2]:.1f}")
                    return pos if exact else f"{pos}（该行行尾不是这个编号）"
    return ""


# 证据串的**显示**截断口径（复审 Important 3）：超长时保留「头 head 字 + … + 尾 tail 字」。
CLIP_HEAD, CLIP_TAIL = 40, 30


def _clip(s: str, head: int = CLIP_HEAD, tail: int = CLIP_TAIL) -> str:
    """证据串的**显示**截断：保留**行尾**。

    为什么必须留尾（复审 Important 3）：B / D 两类的整个论证依赖「该行**行尾**是 `(N)`」，
    旧版 `s[:70]` 正好把行尾那一截切掉，读者从证据串里**无法自行判断**那是不是编号行
    （上一轮 Important 4「证据不全」只修了一半）。口径写在这里，两处调用点共用。
    """
    s = s.strip()
    return s if len(s) <= head + tail else f"{s[:head]}…{s[-tail:]}"


def _ref_hit_lines(num: int, tag: str, mdt: str, r2_hits: list[tuple[int, str]]) -> list[str]:
    """该号在**该参照侧**的命中行（逐条原文，`_clip` 后显示）——**证据必须是参照侧那一行**。

    R1 层取 **md 的行**（md 侧口径就是「整行只有编号」，故命中的就是那些纯编号行）；
    R2 层取 **`pdftotext` 的行**。**不得**像第一版那样两层都拿 `pdftotext` 的行当证据：
    `2502617` 的 `max S = s Cadd (7)` 在 `pdftotext` 里带正文词、在 md 里却是纯编号行，
    拿错侧会让「检测器丢真编号」看起来像「引擎假阳性」（复审 Critical 1 的放大器）。

    显示截断用 `_clip`（**保留行尾**，理由见它）。R1 侧的参照是**并集**
    （md 纯行 ∪ 几何口径），故某些号在 md 里可能一条纯行都没有（那 11 条同行编号）
    ——那时这里返回空表，`_ev_all` 会写明「参照计数来自并集」，而几何命中行写在
    分类器的说明串里（`geom_ev`）。
    """
    if tag == "R1":
        out = []
        for ln in mdt.splitlines():
            m = MD_PURE_W.match(ln)
            if m and int(m.group(1)) == num:
                out.append(_clip(ln))
        return out
    return [_clip(ln) for n, ln in r2_hits if n == num]


def _non_number_line_why(ref_lines: list[str]) -> tuple[str, str]:
    """参照侧命中行里挑一条**能证明自己不是编号行**的，返回 `(行, 理由)`；挑不出返回 `("", "")`。

    谓词只用**该行自己的文本**（可核）：编号 token 之前有 ≥3 连续 ASCII 字母（正文/题注），
    或 token **紧贴前一字符**（`#(24)`、`𝜃(0)` 一类行内标记）。按行文长度降序挑，
    取最像正文的那条当具名证据（全部命中行另外逐条列出，见 `_ref_hit_lines`）。
    """
    tok_rx = re.compile(r"\(\s*\d{1,2}\s*\)")
    for ln in sorted(ref_lines, key=len, reverse=True):
        tok = tok_rx.search(ln)
        before = ln[:tok.start()] if tok else ln
        if WORD.search(before):
            return ln, "编号 token 之前有正文词（正文/题注行），不是编号行"
        if before and not before[-1].isspace():
            return ln, "编号 token **紧贴前一字符**（行内标记），不是编号行"
    return "", ""


def _ev_all(ref_lines: list[str], tag: str) -> str:
    """把参照侧的**全部**命中行列成一条证据串（复审 Important 4：多命中时不得只挑一条）。

    空表时按 `tag` **分派措辞**（复审 Minor 2）：旧版无论哪一层都印「R1 的 md 纯行口径…」，
    于是 **R2 层出现空表时会印错层名**（本语料不可达——换语料就会印错）。两层的空表成因不同：

    * **R1**：`_ref_hit_lines` 收的是 md 的**宽口径**纯行（`MD_PURE_W`，括号内允空白），
      故空表只可能是「该号在 md 里连一条纯行都没有」——本语料实测就是那 11 条
      「编号与公式体同行」的真编号；
    * **R2**：收的是 `pdftotext` 的命中行，空表只可能是「该号是靠**几何口径**进参照的」
      （`R2' = max(pdftotext 行尾, 几何口径)`），或 `pdftotext` 压根没把那号排在行尾。
    """
    if not ref_lines:
        if tag == "R2":
            return ("（该号在本层的**原口径**（`pdftotext -layout` 行尾）里没有命中行：它只由"
                    "**几何口径**数进来——参照计数来自**并集**（pdftotext 行尾 ∪ 几何口径），"
                    "见几何命中行那一段）")
        return ("（该号在本层的**原口径**里没有命中行：R1 的 md 纯行口径（本脚本用的是**宽**"
                "口径 `MD_PURE_W`，括号内允空白）看不到「编号与公式体同行」的行——参照计数"
                "来自**并集**（纯行 ∪ 几何口径），见几何命中行那一段）")
    return "；".join(f"[{i + 1}] {ln!r}" for i, ln in enumerate(ref_lines))


def classify_missing_from_ref(num: int, cand, tag: str) -> tuple[str, str]:
    """**检出有、参照没有** → `(类别, 说明)`。空类别 = 未解释。

    `cand` 是实现给出的候选（`Candidate`），`tag` 是参照名（`R1` / `R2`）。
    判据只用**该行自己的文本与几何**（可核），不含"我的约束把它剔了"这类话。
    """
    b = cand.bbox
    pos = f"p{cand.page + 1} y={b[1]:.1f} x0={b[0]:.1f} x1={b[2]:.1f}"
    if cand.score == 1:
        return "A 行内合并", (
            f"{pos} 该编号与公式体**同处一个 PyMuPDF 文本行**（行原文 "
            f"{_clip(cand.text)!r}）→ {tag} 的行级口径看不到它"
        )
    # D 类**只判行尾那个 token**（复审 Critical 1 的第 ③ 条）：判据必须是
    # 「`( N )` 就是该行的**行尾编号**」，而不是「行里某处有 `( ` 或 ` )`」——后者会把
    # 公式体里的无关括号（`P (Y = 3) (5)` 之类）说成「参照口径漏」，把检测器侧问题洗成语料侧。
    #
    # **还必须要求 token 内确有空白**：这才是「参照口径漏」的**原因**（严格口径的参照正则
    # 是 `^\s*\((\d{1,2})\)\s*$`，括号内不许空白）。只写行尾锚定是不够的——`\(\s*\d{1,2}\s*\)\s*$`
    # 对 `(7)` 也命中（实测本语料 771 条 score==0 的候选里命中，而旧谓词只命中 28 条），
    # 那样反而**放宽**了 D 类：一条普通的 `(7)` 被参照漏掉时会被说成「参照口径漏」，
    # 而它其实是检测器/参照的别的问题。故两个条件都要（行尾锚定 + 括号内含空白）。
    mtail = re.search(r"\(\s*%d\s*\)\s*$" % num, cand.text)
    if mtail and any(ch.isspace() for ch in mtail.group(0)):
        return "D 参照口径漏", (
            f"{pos} 该编号**行尾的 token** 排成 `( N )`（括号内含空白；行原文 "
            f"{_clip(cand.text, 30, 30)!r}）→ 严格口径的正则（括号内不许空白）两侧同漏"
        )
    if tag == "R2":
        return "C 第二引擎漏检", (
            f"{pos} 该编号在原件里是**整行只有编号**（行原文 {_clip(cand.text, 10, 12)!r}），"
            f"而 pdftotext -layout 那一行的行尾不是它"
        )
    return "", f"{pos} 行原文 {_clip(cand.text)!r}（**无法用语料侧事实解释**）"


def classify_extra_in_ref(num: int, ref_lines: list[str], proven: int,
                          detected_count: int, tag: str, where: str,
                          md_w: int, pdf_pure: int, geom_n: int,
                          geom_line: str) -> tuple[str, str]:
    """**参照有、检出没有** → `(类别, 说明)`。空类别 = 未解释。

    ## 顺序是要紧的（复审 Critical 1）

    **先判「检测器有没有丢真编号」**，再谈语料侧解释：

    * `proven > detected_count` → **未解释**。`proven` 是三个**语料侧视角**的并集
      （md 纯编号行 / 原件侧整行只有编号的文本行 / **几何口径**）——前两个只认「整行
      只有编号」，第三个才看得见「编号与公式体同行」的那 11 条。检出里少于这么多
      → 检测器丢了真编号。此时候选行是题注还是公式行**都不影响结论**。
    * 其余情况才允许 B / E：`detected_count >= proven` 意味着「参照里多出来的那一次出现」
      不可能是一条真编号行，于是拿**参照侧命中行自己的文本**（正文词 / 紧贴前一字符）
      说明它确实不是编号行。

    ## 措辞必须**据实**（复审 Important 2）

    旧的 B 类说「该号在原件里只有 {proven} 条整行编号行、**且已全部检出**」——当
    `proven == 0` 时那是**假陈述**（0 条 ≠ 全部检出），而那句话正是 Critical 里那句
    「已解释」。本版改成**逐项报出三个视角各自的数**，并且：

    * `proven > 0` 时才说「证据数不超过检出数，故参照里多出来的一次不可能是一条被丢掉的
      编号行」；
    * `proven == 0` 时**不许**说「已全部检出」，要说「**没有任何独立证据**证明该号有编号行」
      ——判决由封条（含几何口径）给出，不由这一句给出。
    """
    ev = _ev_all(ref_lines, tag)
    proof = (f"md 纯编号行 {md_w} 条、原件侧整行只有编号的文本行 {pdf_pure} 条、"
             f"几何口径（行尾 token 的 x1 落在编号列右缘 ±{EDGE_TOL:g}pt 内）命中 {geom_n} 条")
    ev_geom = f"几何命中行：{geom_line}"
    if proven > detected_count:
        return "", (
            f"{where} 该号在原件里**有独立证据**证明存在编号行（{proof}），"
            f"而检出里只有 {detected_count} 条——**检测器丢了一条真编号**"
            f"（这不是语料侧事实，是检测器的取舍）。{ev_geom}。{tag} 命中行（全部 "
            f"{len(ref_lines)} 条）：{ev}"
        )
    if detected_count > 0:
        return "B 引擎假阳性", (
            f"{where} 该号的独立证据共 {proven} 条（{proof}）**不超过**检出数 "
            f"{detected_count}——故参照里多出来的这一次**不可能**是一条被丢掉的编号行"
            f"（检测器没丢编号），它是该号在题注/正文里的**再次出现**。"
            f"{ev_geom}。{tag} 命中行（全部 {len(ref_lines)} 条）：{ev}"
        )
    if num == 0:
        return "E 语料侧非公式（编号 0）", (
            f"{where} 编号 0，且**没有任何独立证据**证明它是一条编号行（{proof}）——"
            f"证据数 {proven} = 检出数 {detected_count} = 0，判决**由封条给出**"
            f"（不是由「编号 0」这个数给出：`formulas.MIN_NUM = 0` 里 `(0)` 是合法编号），"
            f"故该行只出现在 `θ(0)`/伪代码一类**行内**位置。{ev_geom}。"
            f"{tag} 命中行（全部 {len(ref_lines)} 条）：{ev}"
        )
    ln, why = _non_number_line_why(ref_lines)
    if ln:
        return "B 引擎假阳性", (
            f"{where} 参照侧命中行是 {ln!r}（{why}）；而**没有任何独立证据**证明该号有"
            f"编号行（{proof}）——故它确是语料侧的非编号行。{ev_geom}。"
            f"{tag} 命中行（全部 {len(ref_lines)} 条）：{ev}"
        )
    return "", (
        f"{where} 该号**没有任何独立证据**证明它是一条编号行（{proof}），但参照侧命中行里"
        f"也挑不出「确非编号行」的那一条——**无法用语料侧事实解释**。{ev_geom}。"
        f"{tag} 命中行（全部 {len(ref_lines)} 条）：{ev}"
    )


class _FigShim:
    """D3-b 的适配器：把「公式裁图」接进 C4 的 `strip_provenance`（**不复制它的逻辑**）。

    它只做三件转发：`caption_blocks` → 本任务的检出编号；`_page_items` / `band_of`
    → `figures` 与本任务的 `formulas.formula_band`（同一个函数、同一份定位，故
    `strip_provenance` 重算出的矩形与 `extract_all` 裁的**逐字节同源**）。
    """

    page_items_cache: dict

    def __init__(self, formulas_mod):
        self.f = formulas_mod
        self.page_items_cache = {}

    def caption_blocks(self, doc):
        """**必须在 strip 之后调用**（`strip_provenance` 的 A 侧就是这么调的）。"""
        return self.f.equation_captions(doc)

    def _page_items(self, page):
        from tools.papers import figures
        return figures._page_items(page)

    def band_of(self, items, cap, body_size, page_rect, colw):
        """转发到 `formulas.formula_band`（矩形同源），签名保持 C4 的形状。"""
        eqs = self.page_items_cache.get((cap.page, cap.num))
        if eqs is None:
            return None, "", ""
        rect, _basis, why, _deg = self.f.formula_band(
            items, eqs, body_size, page_rect, colw,
            self.page_items_cache.get(("nb", cap.page), ()))
        return (None if rect is None else rect), "", why


def checks(lines: list[str], limit: int = 0, meta: dict | None = None,
           out: Path | None = None, report=None) -> bool:
    import fitz

    from tools.papers import figures, formulas, io, watermark

    root = io.ORIGIN / COLLECTION
    all_pdfs = sorted(root.rglob("*.pdf"))
    # fail-closed：试点目录取不到就抛，不得空跑一圈然后报「全通过」。
    if not all_pdfs:
        raise FileNotFoundError(f"试点目录下没有任何 PDF：{root}")
    pdfs = report.pick_sample(all_pdfs, limit, FOCUS)
    if meta is not None:
        meta["n_sample"], meta["n_all"] = len(pdfs), len(all_pdfs)

    lines.append(
        f"公式判据 D1/D2/D3 · **限样本 {len(pdfs)}/{len(all_pdfs)} 份**"
        f"（--limit {limit} + 见证集 {'/'.join(FOCUS)}）"
        if limit > 0 else f"公式判据 D1/D2/D3 · 试点 {len(pdfs)} 份"
    )
    if limit > 0:
        lines.append(f"  取样：{' '.join(p.stem for p in pdfs)}")
        lines.append(
            f"  ! 这是**限样本跑**，不是放行依据；放行证据是 "
            f"{report.rel(report.release_path('d'))}。"
        )
    lines.append("=" * 72)

    bad: list = []
    tot: Counter = Counter()
    unexplained: list[str] = []
    d2a_bad: list[str] = []
    d2b_bad: list[str] = []
    d2c_rows: list[str] = []
    d3b_rows: list[str] = []
    n_d3b_unverified = 0
    n_d3b_ran = 0
    n_wm_obj = 0          # 水印对象 > 0 的份数（D3-a 的覆盖指标）
    # `verify_c` **只载入一次**（旧版写在逐篇循环里，43 份就 `exec` 43 次同一个文件；
    # 它一个字节都不改，载入是幂等的，纯浪费）。
    verify_c = _load_verify_c()

    for src in pdfs:
        try:
            prob = src.parent.name
            out_dir = io.formulas_dir(COLLECTION, prob, src.stem)
            res = formulas.extract_all(src, out_dir)

            # ---- 上下文重读（同一篇的**另一次**扫描，用于对账与解释）----
            # **这一次 open 里把该篇的四种取数一次做完**（复审 Minor 8：旧版对同一份 PDF
            # 开了 3 次、各做一次全扫；`strip_in_memory` 只能 strip 一次，所以并进来时
            # 其余取数**不得再 strip**）。
            with fitz.open(src) as doc:
                watermark.strip_in_memory(doc)   # 只 strip 这一次
                sc = formulas.scan(doc)
                n_xrefs = len(watermark.find_watermark_xrefs(doc))
                n_wm_obj += 1 if n_xrefs else 0
                line_items = formulas._line_texts(doc)
                # 原件侧整行只有编号的行（**独立取数路径**：dict 逐行 + 纯行正则）。
                # 命中行明细（元组的第 2 项）本脚本**用不到**——差额解释里的位置串一律取自
                # `line_items`（`_where` 需要同页优先），故这里是死变量，按 `_` 丢弃。
                pdf_pure, _ = pdf_pure_line_counts(doc)
                # 几何口径（**独立取数路径**：rawdict 字符级 bbox + 逐页编号列右缘）
                geom_cnt, geom_hits = geom_number_lines(doc)
                body_size = None
                try:
                    from tools.papers import textmd
                    body_size = textmd.body_size(doc)
                except Exception:
                    body_size = None

            detected = Counter(c.num for c in sc.picks)
            mdt = md_text(prob, src.stem)
            r1, r1w = md_pure_counts(mdt)
            r2, r2_hits = r2_counts(src)
            # 三个视角（md 纯行 / 原件纯行 / 几何口径）→ **并集**（不相加，见模块 docstring）；
            # 几何口径一律降成 0/1（它有 2 条实测假阳性）。
            geom_ex = geom_exists(geom_cnt)
            r1u, r2u = union_ref(r1, geom_ex), union_ref(r2, geom_ex)
            n_geom_inline = sum(1 for z in geom_hits if not z["pure"])

            # ---- D1-a：机制层（**对检出的区分力为零**，见模块 docstring）----
            pngs = sorted(p.name for p in out_dir.glob("eq-*.png"))
            ctxs = sorted(p.name for p in out_dir.glob("eq-*.context"))
            # 产出图名由 (编号, 页) 唯一决定；重号（同页同号）会互相覆盖——`scan()` 的
            # 代表层已保证每号一条，故这里不再需要额外的去重谓词（旧版留了一个
            # 恒返回 False 的 `_dup_name`，是死代码，本轮删掉）。
            want_names = sorted(f"eq-{c.num:02d}-p{c.page + 1}.png" for c in sc.picks)
            name_ok = pngs == want_names
            d1a = (len(pngs) == res.n_eq == len(ctxs)) and name_ok
            tot["n_eq"] += res.n_eq
            tot["n_png"] += len(pngs)

            # ---- D1-b：逐份 检出 vs R1（md 纯行 ∪ 几何口径，**Task 3 的产物**）----
            d1b, d1b_notes, n_diff_b, n_une_b = _diff_layer(
                detected, r1, sc, "R1", mdt, r2_hits, r1w, pdf_pure, geom_ex,
                geom_hits, line_items)
            # ---- D1-c：逐份 检出 vs R2（pdftotext 行尾 ∪ 几何口径，**第二引擎**）----
            d1c, d1c_notes, n_diff_c, n_une_c = _diff_layer(
                detected, r2, sc, "R2", mdt, r2_hits, r1w, pdf_pure, geom_ex,
                geom_hits, line_items)
            tot["d1_diff_r1"] += n_diff_b
            tot["d1_une_r1"] += n_une_b
            tot["d1_diff_r2"] += n_diff_c
            tot["d1_une_r2"] += n_une_c
            tot["n_ref_r1u"] += sum(r1u.values())
            tot["n_ref_r2u"] += sum(r2u.values())
            tot["n_geom"] += sum(geom_cnt.values())
            tot["n_geom_inline"] += n_geom_inline
            tot["n_geom_doc"] += 1 if geom_cnt else 0
            # ---- D1-d：有参照而零检出 ----（参照同样用**并集**：它只会更强）
            d1d = True
            if sum(r1u.values()) >= D1D_MIN_REF and res.n_eq == 0:
                d1d = False
                d1b_notes.append(
                    f"**D1-d FAIL**：该篇 R1（并集）= {sum(r1u.values())} 条（参照存在）"
                    f"而检出 = 0——参照存在却没解析出来"
                )
            for n in d1b_notes + d1c_notes:
                if "未解释" in n:
                    unexplained.append(f"{src.stem}: {n}")

            # ---- D2-a/b/c ----
            ctx = _read_contexts(out_dir)
            md_ns = formulas.nospace(mdt)
            md_lines_ns = [formulas.nospace(l) for l in mdt.splitlines()]
            a_bad = [k for k, v in ctx.items()
                     if not re.search(r"\(" + str(v["num"]) + r"\)", md_ns)]
            for k in a_bad:
                d2a_bad.append(f"{src.stem}/{k}: REF ({ctx[k]['num']}) 在 md 里找不到")
            b_bad = []
            for k, v in ctx.items():
                for q in v["wheres"] + v["cites"]:
                    if not q or q not in md_ns:
                        b_bad.append(f"{src.stem}/{k}: {q[:60]!r}")
            for x in b_bad:
                d2b_bad.append(x)
            # **参照（任务书口径）**: md 侧 `CITE`（带词边界、原始文本）——40 处 / 11 份。
            md_cites_raw = Counter(int(m.group(1)) for m in CITE.finditer(mdt))
            n_refs_md_raw = sum(md_cites_raw.values())
            tot["n_refs_md_raw"] += n_refs_md_raw
            tot["n_refs"] += res.n_refs
            tot["n_where"] += res.n_where
            # **产物侧的实际条数**（从文件读回，**不信实现的自报**）。
            # 第一版这里是拿 `res.n_refs`（实现自报的数）判的，于是变异 M4
            # （只把写入内容的 wheres/cites 换成空、计数照旧）**判据全绿**
            # ——"判据读的是自称、不是产物"正是本项目 4.2 家族的第 8 例（实测抓到）。
            n_ref_ctx = sum(len(v["cites"]) for v in ctx.values())
            n_where_ctx = sum(len(v["wheres"]) for v in ctx.values())
            n_ref_art = sum(1 for v in ctx.values() if v["num"] is not None)
            # **D2-c 硬判据（零检出门）**：md 有显式引用而 `.context` **文件里**一条都没有。
            d2c = not (n_refs_md_raw >= 1 and n_ref_ctx == 0)
            if not d2c:
                lines.append(
                    f"{src.stem:<10} ^ D2-c FAIL：md 里 `Eq./Equation (N)` 有 "
                    f"{n_refs_md_raw} 处（{sorted(md_cites_raw)}）而 `.context` **文件里** "
                    f"抽出的 CITE 条数 = 0（实现自报 {res.n_refs} 条）"
                )
            # **D2-d（分叉 tripwire）**：实现自报的条数必须与**产物文件里读回**的条数逐项相等。
            # 它抓的是"计数与写入分叉"（M4 的形态）：自报说登记了 N 条、文件里一条都没有。
            d2d = (n_ref_art == res.n_eq and n_ref_ctx == res.n_refs
                   and n_where_ctx == res.n_where)
            if not d2d:
                lines.append(
                    f"{src.stem:<10} ^ D2-d FAIL（自报 vs 产物文件分叉）：自报 "
                    f"REF={res.n_eq}/CITE={res.n_refs}/WHERE={res.n_where}，"
                    f"文件里 REF={n_ref_art}/CITE={n_ref_ctx}/WHERE={n_where_ctx}"
                )
            tot["n_ref_ctx"] += n_ref_ctx
            tot["n_where_ctx"] += n_where_ctx
            # **逐号的**presence 对账（不是逐次计数对账）。用**号集合**而不是计数，
            # 是因为两侧是不同的产物（md 是重排产物、`.context` 的 CITE 行来自 PDF 的行），
            # 逐次计数会被"一行里提两次""重排把一行拆成两行"这类口径噪声污染——那些噪声
            # 不是语料事实、也不是交付物的毛病。**逐号的 presence 差异**才是要看得见的东西。
            ctx_nums = set()
            for v in ctx.values():
                for q in v["cites"]:
                    ctx_nums |= {int(m.group(1)) for m in CITE_NS.finditer(q)}
            md_nums = set(md_cites_raw)
            f_rows = []
            for num in sorted(md_nums - ctx_nums):
                if num not in detected:
                    cls = "F1 引用指向的编号不在检出集"
                else:
                    cls = "F2 原件里 `equation` 与编号之间被换行切断（行级正则匹配不到）"
                # md 侧的证据取**整篇归一化文本里的上下文窗口**（两侧对账用的同一谓词）。
                # 逐行取证据会得到空串：该篇的引用写成 `… in equation` + 换行 + `(9), …`
                # （**引用被换行切断**，这正是 F2 类要说明的那件事）——`CITE` 与逐行的
                # `CITE_NS` 都匹配不到，只有归一化的整篇文本能把它连起来
                # （实测第一版逐行取，F 行里就是 `md 行 ''`）。
                _m = next((m for m in CITE_NS.finditer(md_ns)
                           if int(m.group(1)) == num), None)
                ev_md = (("…" + md_ns[max(0, _m.start() - 34):_m.end() + 12] + "…")
                         if _m else "")
                ev_pdf = next((f"p{p + 1} y={b[1]:.1f} {t.strip()[:56]!r}"
                               for p, b, t in line_items
                               if re.search(r"\(\s*%d\s*\)" % num, t)), "")
                f_rows.append(f"[{cls}] ({num}) md 行 {ev_md[:64]!r}｜原件行 {ev_pdf}")
            for num in sorted(ctx_nums - md_nums):
                f_rows.append(f"[F3 .context 登记了这个号、md 侧没有] ({num})")
            if n_refs_md_raw or res.n_refs:
                d2c_rows.append(
                    f"{src.stem:<10} D2-c 显式引用：md（任务书口径）={n_refs_md_raw} 处 / "
                    f"号集 {sorted(md_nums)} · 登记的 CITE 行={res.n_refs} / 号集 "
                    f"{sorted(ctx_nums)} · WHERE={res.n_where}"
                    + ("" if not f_rows else "   < 号集不等，逐条见下（F 类）")
                )
            for r in f_rows:
                d2c_rows.append(f"{'':10}   {r}")
            tot["n_d2c_f"] += len(f_rows)

            # ---- D3-a：机制层 + 分叉 tripwire ----
            d3a = (res.n_stripped == n_xrefs)
            # ---- D3-b：产出图确实来自置空后的渲染（**原样调用 C4 的谓词**）----
            shim = _FigShim(formulas)
            for c in sc.picks:
                shim.page_items_cache[(c.page, c.num)] = c.as_eqnum()
            by_page: dict[int, list] = {}
            for c in sc.picks:
                by_page.setdefault(c.page, []).append(c.as_eqnum())
            for pno, eqs in by_page.items():
                shim.page_items_cache[("nb", pno)] = tuple(eqs)
            prov, prov_msg = verify_c.strip_provenance(src, out_dir, shim, watermark)
            # **覆盖率只算"有产出可验"的份**：该篇 0 条编号公式时没有带可试，
            # `strip_provenance` 按设计返回未验证——把它算进分母等于用"本来没有东西可验"
            # 去冲淡这一层的覆盖数。0 产出的份单列（`无产出可验`），不进占比。
            if res.n_eq > 0:
                n_d3b_ran += 1
                if prov is None:
                    n_d3b_unverified += 1
            d3b = prov is not False

            # 三态之外的取值（`strip_provenance` 将来若改成别的返回型）不得 KeyError——
            # 旧版写成 `{True:…, False:…, None:…}[prov]`，第四个取值会当场抛。
            prov_state = {True: "已验证", False: "**FAIL**", None: "未验证"}.get(
                prov, f"未知状态 {prov!r}（`strip_provenance` 的返回型变了）")
            d3b_rows.append(
                f"{src.stem:<10} D3-b 置空来源（A/B 差分，C4 的谓词原样调用）= "
                f"{prov_state if res.n_eq else '无产出可验'}："
                + prov_msg
            )

            # ---- 裁图带的**高度分布**（报告量，M5 变异要它才抓得住）----
            # 两种取法**并列**（复审 Important 5：任务书 Step 3 明令「新旧两种取法的高度
            # 分布差异逐份报告」，只印新取法不算）：
            #   * 新取法 = `formulas.formula_band`（版面空白法）；
            #   * 固定点法 = 计划草稿的 `y0-6 / y1+6`（`x1+60` 只影响宽度，不影响高度）——
            #     它同时是变异 M5 施加之后新取法会退化成的那一支，故两列在 M5 下相等。
            hs, hs_fixed = _band_heights(src, sc, body_size)
            tot["n_band"] += len(hs)

            lines.append(
                f"{src.stem:<10} 检出={res.n_eq:<3} 候选={res.n_cand:<3} 被剔={res.n_rejected:<3} "
                f"退化={res.n_band_fallback:<2} R1'={sum(r1u.values()):<3} R2'={sum(r2u.values()):<3} "
                f"(原口径 R1={sum(r1.values()):<3} R2={sum(r2.values()):<3}) "
                f"n_refs={res.n_refs:<3} n_where={res.n_where:<3} "
                f"D1-a={'OK' if d1a else 'FAIL'} D1-b={'OK' if d1b else 'FAIL'} "
                f"D1-c={'OK' if d1c else 'FAIL'} D1-d={'OK' if d1d else 'FAIL'} "
                f"D2-a={'OK' if not a_bad else 'FAIL'} D2-b={'OK' if not b_bad else 'FAIL'} "
                f"D2-c={'OK' if d2c else 'FAIL'} D2-d={'OK' if d2d else 'FAIL'} "
                f"D3-a={'OK' if d3a else 'FAIL'}（水印对象={n_xrefs} 自报 strip={res.n_stripped}）"
            )
            # **几何口径的逐份报告量**（新地基的覆盖：它看得见多少行、其中多少是
            # 「编号与公式体同行」、右缘是本页还是本篇推出来的）。逐条坐标印出来，
            # 任何一条都能用 `tests/papers/recon/formula-geom-scan.py` 复算。
            lines.append(
                f"{'':10} 几何口径：右缘来源 本页 "
                f"{sum(1 for z in geom_hits if z['edge_src'] == '本页')} 行 / 本篇 "
                f"{sum(1 for z in geom_hits if z['edge_src'] == '本篇')} 行"
                f"· 命中 {sum(geom_cnt.values())} 行（其中**非纯行** {n_geom_inline} 行："
                f"含真编号与**实测假阳性**两种，逐条看行原文）"
                f" · 逐号存在性 {sorted(geom_ex)}"
                + ("".join(
                    f"\n{'':14} 同行命中：p{z['page'] + 1} y={z['y']:.1f} ({z['num']}) "
                    f"Δ={z['delta']:+.1f}[{z['edge_src']}] {_clip(z['text'])!r}"
                    for z in geom_hits if not z["pure"]))
                + f"\n{'':14} 纯行口径交叉核对（报告量）：md 宽容 {sum(r1w.values())} 条 · "
                  f"原件整行只有编号 {sum(pdf_pure.values())} 条"
            )
            # **裁图带的报告量**：逐份的 min/中位/max（pt），**两种取法并列**。
            # 它**不是判据**（裁图内容对不对无判据覆盖，见模块 docstring 的债），但它是
            # M5（裁图带退回固定点数）能**被抓住**的唯一量——所以必须印出来，且必须是
            # **逐份两组三个数**而不是一句汇总。
            lines.append(
                f"{'':10} 裁图带高（**报告量，非判据**）："
                + (f"新取法 n={len(hs)} min={min(hs):.1f} 中位={_median(hs):.1f} "
                   f"max={max(hs):.1f} pt · 固定点法（草稿 y0-6/y1+6）n={len(hs_fixed)} "
                   f"min={min(hs_fixed):.1f} 中位={_median(hs_fixed):.1f} "
                   f"max={max(hs_fixed):.1f} pt · 退化 {res.n_band_fallback} 条 · "
                   f"候选 {res.n_cand} 入链 {len(sc.accepted)} 被剔 {res.n_rejected}"
                   if hs else "（本篇检出 0 条，无带）")
            )
            # **逐条登记，不得悄悄抹平**：差额非 0 时把每条的类别与坐标印出来——
            # 登记是判据的一部分，不是失败时才打印的附注。
            for n in d1b_notes + d1c_notes:
                lines.append(f"{'':10}   D1 差额：{n}")
                # 逐类计数（复审要求「逐类重印差额归属」）：类别是说明串开头的 `[X …]`。
                if n.startswith("["):
                    tot[f"cls {n[1:n.index(']')]}"] += 1
            if not (d1a and d1b and d1c and d1d and not a_bad and not b_bad and d2c
                    and d3a and d3b and d2d):
                bad.append((src.stem, d1a, d1b, d1c, d1d, bool(a_bad), bool(b_bad),
                            d2c, d3a, d3b))
        except BaseException as e:
            lines.append(f"{src.stem:<10} ! 处理该篇时抛出异常：")
            lines.append(report.fmt_exc(e))
            bad.append((src.stem, False, False, False, False, False, False, False,
                        False, False))

    lines.append("=" * 72)
    # **「未解释差额」的两个派生必须同源**（复审 Minor 3）：旧版一个用 `len(unexplained)`
    # （按说明串里有没有「未解释」二字筛），一个用分类器返回的 `tot['d1_une_*']`——只要
    # 某条说明串里出现「未解释」三个字，两个数就打架。合计行一律用 `tot` 的两个数，
    # 并同时印出 `len(unexplained)` 让两者**当场可核对**（不一致即判 FAIL）。
    n_une_tot = tot["d1_une_r1"] + tot["d1_une_r2"]
    lines.append(f"D1 合计：检出 {tot['n_eq']} 条 · 产出 PNG {tot['n_png']} 张"
                 f" · 未解释差额 **{n_une_tot}** 条（= R1 层 {tot['d1_une_r1']} + "
                 f"R2 层 {tot['d1_une_r2']}，**必须为 0**）")
    # 逐层的「差额条数 / 未解释条数」两列（**机器可核**，变异驱动器按这两行取数）。
    # 差额条数是**多重集减法**算出来的，与分类器无关；分类器一旦吞掉差额，
    # 「未解释」这一列就变小——这就是复审 Critical 1 的判据形态。
    # **两列不相等是正常的**（差额 = 已解释 + 未解释），见模块 docstring 的说明。
    lines.append(
        f"D1 差额归类（逐层）：R1 层差额 {tot['d1_diff_r1']} 条 / 未解释 "
        f"{tot['d1_une_r1']} 条 · R2 层差额 {tot['d1_diff_r2']} 条 / 未解释 "
        f"{tot['d1_une_r2']} 条（**未解释必须为 0**；差额 − 未解释 = 已解释，"
        f"放行时两列本来就**不相等**——被吞掉的差额会让**未解释**这一列变小）"
    )
    lines.append(
        f"参照基数（**新口径 = 纯行 ∪ 几何口径，逐号取 max**）：R1' = {tot['n_ref_r1u']} · "
        f"R2' = {tot['n_ref_r2u']} · 几何口径命中 {tot['n_geom']} 行"
        f"（其中**非纯行** {tot['n_geom_inline']} 行——里面**既有真编号、也有实测假阳性**"
        f"（正文行恰好排到版心右缘、行尾正好是 `(N)`），**容差分不开这两种**，"
        f"故几何口径只当存在性证明用；逐条坐标与原见逐篇的「同行命中」行与 "
        f"`tests/papers/recon/formula-recon.txt` §八；{tot['n_geom_doc']} 份有命中）"
    )
    lines.append(
        "  旧口径（**历史保留**，逐份复算见 tests/papers/recon/formula-recon.txt §三）："
        "R1 = 743（md 严格纯行）· R1w = 773 · R2 = 767（pdftotext 行尾）· R3 = 661（已废弃的"
        "「靠右」口径）。**本行的新值只增不减**（并集只会让参照变大）。"
    )
    cls_tally = " · ".join(
        f"{k[4:]} {v} 条" for k, v in sorted(tot.items()) if k.startswith("cls "))
    lines.append(
        f"D1 差额逐类归属（R1+R2 两层合计）：{cls_tally or '（无差额）'}"
        "　·　**A / C / D 三类在本语料上为 0 条**：参照并上几何口径之后，「检出有、参照没有」"
        "这一方向不再有差额（那 11 条同行编号与 `2508861` 的 28 条 `( N )` 已被参照数到）；"
        "C 类（第二引擎漏检）同理——`R2' = max(pdftotext 行尾, 几何口径)` 之后，「检出有、R2 "
        "没有」这一方向也归零。三类仍保留在代码里（对其他形态可达），**不作为「已覆盖」声称**。"
    )
    if len(unexplained) != n_une_tot:
        lines.append(
            f"**分叉 FAIL**：「未解释」的两个派生不等（说明串数 {len(unexplained)} ≠ "
            f"分类器计数 {n_une_tot}）——说明串里混进了「未解释」三个字，或分类器被改坏。"
        )
        bad.append(("<未解释的两个派生分叉>", False, False, False, False, False,
                    False, False, False, False))
    lines.append(f"裁图带高（**报告量，非判据**）合计：{tot['n_band']} 条带；逐份的 "
                 f"「新取法 / 固定点法」两组 min/中位/max 见上（这条量是 M5"
                 f"「带取法退回固定点数」唯一的抓手）")
    for x in unexplained:
        lines.append(f"  **未解释**：{x}")
    lines.append(
        "D1-a 的强度声明（**必须与本节同读**）：它的两边是同一个函数算出来的，差额按构造"
        "恒为 0，**对检出环节零区分力**——它只抓落盘（少写/写错名）。区分力在 D1-b/c/d。"
    )
    lines.append(
        f"D2-d 自报 vs 产物文件（分叉 tripwire）：REF/WHERE/CITE 逐项相等才绿 · "
        f"本次文件里读回 REF={tot['n_eq']} / CITE={tot['n_ref_ctx']} / WHERE={tot['n_where_ctx']}"
    )
    lines.append(f"D2-a 编号行定位（md，空白归一化后）：不可定位 **{len(d2a_bad)}** 条")
    for x in d2a_bad[:10]:
        lines.append(f"    {x}")
    lines.append(f"D2-b 引述句定位（md，空白归一化后）：{tot['n_where'] + tot['n_refs']} 条"
                 f"（WHERE {tot['n_where']} + CITE {tot['n_refs']}），不可定位 "
                 f"**{len(d2b_bad)}** 条")
    for x in d2b_bad[:10]:
        lines.append(f"    {x}")
    lines.append(
        "D2-a 的强度边界（**必须与 D1-a 那句同读**）：它的谓词只是「`(N)` 出现在该篇 md "
        "归一化全文的**任意位置**」，两侧是同一条流水线的产物 → **对「定位对不对」近乎恒真**；"
        "它只抓「`.context` 里的编号是凭空写出来的」（变异 M6）。长串引述的定位在 D2-b，"
        "编号与产出图名的一致性在 D1-a 的落盘名单。"
    )
    lines.append(
        "WHERE 条数：**没有任何独立参照，不参与判定**（属「不适用」）。`where` 引述句的归属"
        "是一条先验（「位置在它之前、最近的那条检出编号」，见 `formulas` 模块 docstring），"
        "md 侧没有与之对应的可数对象——故它只作**覆盖指标**印出，任何一层判据都不用它。"
    )
    lines.append(
        f"D2-c 显式引用对账（md 侧**任务书口径**全批 {tot['n_refs_md_raw']} 处 / "
        f"{sum(1 for r in d2c_rows if 'D2-c 显式引用' in r)} 份有 · "
        f"登记的 CITE 行 {tot['n_refs']} 条 / WHERE {tot['n_where']} 条）："
        f"**硬判据只有『md 有引用而 .context 抽 0 条 → FAIL』这一条**（任务书二节的零检出门）；"
        f"md 引用号集与 `.context` 登记号集**不等的**条目逐条以 F 类列出"
        f"（共 {tot['n_d2c_f']} 条），**不判红**——那是必须看得见的语料事实，不是判据；"
        f"两侧**逐次计数**刻意不做 1:1 比对（md 是重排产物、CITE 行来自 PDF 的行，"
        f"计数差里混着口径噪声）"
    )
    for r in d2c_rows:
        lines.append("    " + r)
    lines.append(
        f"D3-a 机制层：逐份断言「`extract_all` 自报 strip 数 == 本脚本另算的水印对象数」· "
        f"本次 {len(pdfs)} 份里**水印对象 > 0** 的有 **{n_wm_obj}** 份（覆盖指标：=0 不等于"
        f"干净，只等于「本脚本没找到水印对象」）；逐份的 `水印对象=/strip=` 见上"
    )
    n_d3b_noprod = sum(1 for r in d3b_rows if "无产出可验" in r)
    lines.append(f"D3-b 无产出可验（本篇检出 0 条，没有带可试）：{n_d3b_noprod} 份，不进占比分母")
    prov_rate = n_d3b_unverified / n_d3b_ran if n_d3b_ran else 1.0
    prov_ok = prov_rate <= PROV_UNVERIFIED_CEILING
    lines.append(
        f"D3-b 置空来源（产出图）：C4 的 A/B 差分谓词**原样调用**（`verify_c.strip_provenance`，"
        f"配一个只做转发的适配器；说明串里「图注」二字是 C4 的原话，本任务未改它一个字） · **已验证 "
        f"{n_d3b_ran - n_d3b_unverified} 份 / 未验证 {n_d3b_unverified} 份**"
        f"（未验证 = 该带盖不到水印 / 无带可试 / 与两个参照都不同，差分无区分力；"
        f"**既不并进通过、也不硬失败该篇**）"
    )
    lines.append(
        f"D3-b 未验证占比（**分母只含『有产出可验』的份**）：{n_d3b_unverified}/{n_d3b_ran} "
        f"= {prov_rate * 100:.2f}% "
        f"（上界 {PROV_UNVERIFIED_CEILING * 100:.0f}%）"
        f"{'（**超上界 → 全批判 FAIL：判据被自己的前提架空**）' if not prov_ok else ''}"
    )
    if not prov_ok:
        bad.append(("<D3-b未验证超上界>", False, False, False, False, False, False,
                    False, False, False))
    for r in d3b_rows:
        lines.append("    " + r)
    lines.append(f"D1/D2/D3（机器可核）本批判定: {not bad}")
    if bad:
        lines.append("失败明细:")
        for row in bad:
            lines.append(f"  {row}")
    return not bad


def _token_lines(doc) -> list[dict]:
    """全篇「行尾是 `(N)`」的行 → token **自己**的字符级 bbox（**独立取数路径**）。

    `get_text("rawdict")` 的每个 char 带 bbox，故 token 的 x0/x1 是**字符级**求得的
    （整行 bbox 含行尾空白，会把「靠不靠右」污染掉）。**不走 `formulas.scan()` 的
    候选/链/代表逻辑**——与 `pdf_pure_line_counts` 同一条约定。

    返回每条 `{"page", "y", "text", "num", "x0", "x1", "pure"}`。
    **要求调用方已经 `strip_in_memory` 过**（同 `formulas.scan` 的约定）。
    """
    num_end = re.compile(r"\(\s*(\d{1,2})\s*\)\s*$")
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("rawdict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                chars = [c for sp in line["spans"] for c in sp["chars"]]
                text = "".join(c["c"] for c in chars)
                m = num_end.search(text)
                if not m:
                    continue
                end = m.start() + m.group(0).rfind(")") + 1
                box = [c["bbox"] for c in chars[m.start():end]
                       if c["bbox"][2] > c["bbox"][0]]
                if not box:
                    continue
                out.append({
                    "page": pno, "y": line["bbox"][1], "text": text.strip(),
                    "num": int(m.group(1)),
                    "x0": min(z[0] for z in box), "x1": max(z[2] for z in box),
                    "pure": text.strip() == m.group(0).strip(),
                })
    return out


def geom_number_lines(doc) -> tuple[Counter, list[dict]]:
    """**几何口径**：行尾 token 的 x1 落在「编号列右缘」± `EDGE_TOL` 内的行。

    「编号列右缘」= **本页**整行只有编号的行（纯编号行）的 token x1 集合；本页一条都没有
    时退到**本篇**的同一集合。**没有全局绝对常量**（页宽/比例/字号一律不进来）。
    返回 `(逐号命中行数, 逐条明细)`；明细里每条带 `delta` 与 `edge_src`（本页/本篇）。

    **已知假阳性**（实测 2 条，登记在模块 docstring）：正文行恰好排到版心右缘、行尾又
    正好是 `(N)` 时，几何口径会把它当成编号行——故调用方一律用 `geom_exists()` 把它
    降成 0/1 的**存在性证明**，不得当计数用。
    """
    rows = _token_lines(doc)
    per_page: dict[int, set] = {}
    for z in rows:
        if z["pure"]:
            per_page.setdefault(z["page"], set()).add(z["x1"])
    doc_edges: set = set()
    for vs in per_page.values():
        doc_edges |= vs
    cnt: Counter = Counter()
    hits: list[dict] = []
    for z in rows:
        local = per_page.get(z["page"])
        edges = local or doc_edges
        if not edges:
            continue
        delta = min(abs(z["x1"] - e) for e in edges)
        if delta > EDGE_TOL:
            continue
        hits.append(dict(z, delta=delta, edge_src="本页" if local else "本篇"))
        cnt[z["num"]] += 1
    return cnt, hits


def geom_exists(cnt: Counter) -> Counter:
    """几何口径 → **存在性证明**（0/1）。见模块 docstring：它不得当计数用。"""
    return Counter({n: 1 for n in cnt})


def geom_ev(hits: list[dict], num: int, limit: int = 3) -> str:
    """该号的几何命中行 → 一行证据串（页码 + 坐标 + Δ + 行原文，行尾保留）。"""
    rows = [z for z in hits if z["num"] == num]
    if not rows:
        return "（几何口径在本篇没有命中该号）"
    return "；".join(
        f"p{z['page'] + 1} y={z['y']:.1f} token_x1={z['x1']:.1f} Δ={z['delta']:+.1f}"
        f"[{z['edge_src']}] {_clip(z['text'])!r}" for z in rows[:limit]
    ) + (f"（共 {len(rows)} 条）" if len(rows) > limit else "")


def pdf_pure_line_counts(doc) -> tuple[Counter, list[tuple[int, float, str]]]:
    """原件侧**整行只有编号**的文本行的逐号多重集（+ 命中行明细）。

    **独立取数路径**：直接 `doc.get_text("dict")` 逐行取文本 + 纯行正则，**不走
    `formulas.scan()` 的候选/候选链/代表选择**。它与 md 侧（`md_pure_counts` 的 wide）
    观测的是**同一批原件行**，故两者是同一事实的两个视角：`max()` 取其一即可，
    **相加会把同一条物理行数两次**（`classify_extra_in_ref` 的 `proven` 就是这么取的）。

    收**已经打开且已 strip 过**的 doc（复审 Minor 8：不再自己 open/ strip 一次——
    `strip_in_memory` 每份只能算一次，重复 strip 会把 D3-a 的水印对象数打成 0）。
    """
    cnt: Counter = Counter()
    hits: list[tuple[int, float, str]] = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"]).strip()
                m = MD_PURE_W.match(t)
                if m:
                    cnt[int(m.group(1))] += 1
                    hits.append((pno, line["bbox"][1], t))
    return cnt, hits


def union_ref(ref: Counter, geom_ex: Counter) -> Counter:
    """参照的**并集口径**：`max(原口径逐号计数, 几何存在性)`（不相加，见模块 docstring）。

    两个口径看的是**同一批原件行**，相加会把同一条物理行数两次。几何口径一律降成 0/1
    （它的 2 条实测假阳性决定了它不能当计数用）。
    """
    out = Counter(dict(ref))
    for n, v in geom_ex.items():
        if out.get(n, 0) < v:
            out[n] = v
    return out


def _diff_layer(detected: Counter, ref: Counter, sc, tag: str, mdt: str,
                r2_hits: list[tuple[int, str]], md_w: Counter,
                pdf_pure: Counter, geom_ex: Counter, geom_hits: list[dict],
                line_items: list[tuple]) -> tuple[bool, list[str], int, int]:
    """一层参照的对账：`(是否无未解释差额, 逐条登记串, 差额条数, 未解释条数)`。

    `detected` 是检出数的多重集，`ref` 是该参照原口径的多重集——函数内部**先并上几何
    口径**（`union_ref`），再对账。**每条差额都要落进一个具名类别**（见模块 docstring
    的表），落不进去的记「未解释」→ 判 FAIL。

    后两个量是**给报告与变异驱动器看的**：`差额条数 - 未解释条数` 就是「已解释」的条数。
    **被吞掉的差额会让「未解释」这一列变小**（差额条数是多重集减法算的、与分类器无关）。
    """
    notes: list[str] = []
    ok = True
    n_diff = n_unexplained = 0
    picks = {c.num: c for c in sc.picks}
    ref = union_ref(ref, geom_ex)
    for num in sorted((detected - ref).elements()):
        n_diff += 1
        cand = picks.get(num)
        if cand is None:
            n_unexplained += 1
            notes.append(f"**未解释**：检出 {num} 而参照没有（找不到对应候选）")
            ok = False
            continue
        kind, why = classify_missing_from_ref(num, cand, tag)
        if not kind:
            n_unexplained += 1
            ok = False
            notes.append(f"**未解释**：检出 {num}、{tag} 没有 —— {why}")
        else:
            notes.append(f"[{kind}] {num}: {why}")
    for num in sorted((ref - detected).elements()):
        n_diff += 1
        ref_lines = _ref_hit_lines(num, tag, mdt, r2_hits)
        where = _where(line_items, num, picks_page(sc, num))
        md_n = md_w.get(num, 0)
        pdf_n = pdf_pure.get(num, 0)
        g_n = geom_ex.get(num, 0)
        kind, why = classify_extra_in_ref(
            num, ref_lines, max(md_n, pdf_n, g_n), detected.get(num, 0), tag, where,
            md_n, pdf_n, g_n, geom_ev(geom_hits, num))
        if not kind:
            n_unexplained += 1
            ok = False
            notes.append(f"**未解释**：{tag} 有 {num} 而检出没有 —— {why}")
        else:
            notes.append(f"[{kind}] {num}: {why}")
    if not notes:
        notes.append(f"（{tag} 与检出**逐份相等**，无差额）")
    return ok, notes, n_diff, n_unexplained


def picks_page(sc, num: int) -> int | None:
    """该号在**检出**里的页（复审 Minor 6：`_where` 优先取同页那条命中行）。"""
    for c in sc.picks:
        if c.num == num:
            return c.page
    return None


def _median(xs: list[float]) -> float:
    import statistics
    return statistics.median(xs)


def _band_heights(src: Path, sc, body_size) -> tuple[list[float], list[float]]:
    """逐条重算裁图带的**高度**（pt）——报告量，用于抓住"带取法被改回固定点数"（M5）。

    返回 `(新取法的高度, 固定点法的高度)`，**两种取法在同一批检出编号上并列**：

    * **新取法** = `formulas.formula_band`（版面空白法）；
    * **固定点法** = 计划草稿的 `y0-6 / y1+6`（`x1+60` 只影响宽度），即**变异 M5
      施加后新取法会退化成的那一支**——故 M5 一跑，两列会相等（可直接核）。

    任务书 Step 3 明令「新旧两种取法的高度分布差异**逐份**报告」，故这一层必须两组都印。

    **它是报告量、不是判据**：本任务没有任何机器判据能证明"框住的就是那条公式"
    （见模块 docstring 的债）。
    """
    import fitz
    from tools.papers import figures, watermark
    new_hs: list[float] = []
    fixed_hs: list[float] = []
    with fitz.open(src) as doc:
        watermark.strip_in_memory(doc)
        by_page: dict[int, list] = {}
        for c in sc.picks:
            by_page.setdefault(c.page, []).append(c.as_eqnum())
        for c in sc.picks:
            eq = c.as_eqnum()
            page = doc[eq.page]
            items, colw = figures._page_items(page)
            rect, _basis, _why, _deg = formulas_mod().formula_band(
                items, eq, body_size, page.rect, colw, tuple(by_page[eq.page]))
            new_hs.append(rect.height)
            line = formulas_mod().number_line(items, eq)
            own = (fitz.Rect(line.x0, line.y0, line.x1, line.y1) if line is not None
                   else fitz.Rect(eq.x0, eq.y0, eq.x0 + 1.0, eq.y1))
            fixed_hs.append((own.y1 + 6.0) - (own.y0 - 6.0))
    return new_hs, fixed_hs


def formulas_mod():
    from tools.papers import formulas
    return formulas


def _read_contexts(out_dir: Path) -> dict:
    """读该篇的 `.context`：`{文件名: {"num": N, "wheres": [...], "cites": [...]}}`。"""
    out = {}
    for p in sorted(out_dir.glob("*.context")):
        num = None
        wheres: list[str] = []
        cites: list[str] = []
        for ln in p.read_bytes().decode("utf-8").splitlines():
            if ln.startswith("REF: ("):
                num = int(ln[6:-1])
            elif ln.startswith("WHERE: "):
                wheres.append(ln[7:])
            elif ln.startswith("CITE: "):
                cites.append(ln[6:])
        out[p.name] = {"num": num, "wheres": wheres, "cites": cites}
    return out


def main() -> int:
    import argparse

    from tools.papers import report

    ap = argparse.ArgumentParser(
        description="公式判据 D1/D2/D3（编号检出 / 引述句 / 裁图无水印）",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="只跑前 N 份 + 见证集（变异演示用）。报告写到 "
             "tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/d-report.txt）；负数不接受。",
    )
    args = ap.parse_args()

    out, guard_msg = report.resolve_report("d", args.limit)
    pre = report.sha256_of(report.release_path("d")) if args.limit > 0 else ""

    meta: dict = {}
    lines = ["公式抽取校验（D1/D2/D3）"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out, report)
    except BaseException as e:
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = report.recheck_target("d", args.limit, out)
    if msg2:
        lines.append(msg2)
    # **这一句不能省**：守卫消息只是往报告里写了"FAIL"，不并进 ok 的话
    # RESULT 行照样打印 PASS、退出码照样是 0。
    if guard_msg or msg2:
        ok = False

    lines.append("")
    lines.append(f"写入：{report.rel(out)}")
    if args.limit > 0:
        lines.append(
            f"  本文件是**限样本跑**（--limit {args.limit} + 见证集 {'/'.join(FOCUS)}）的"
            f"报告，**不入库、不是放行依据**；放行证据是 "
            f"{report.rel(report.release_path('d'))}，只有全量跑会写它。"
        )
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件。"
        )

    text = "\n".join(lines) + "\n"
    # 限样本跑的「放行证据完整性自检」在**落盘之前**算完并写进正文（旧版先 flush 一次
    # 中间态、再 append 这段、又 flush 一次——中间态那一份**没有 `RESULT:` 行**，
    # 是同一家族的老毛病：读的人可能读到一份没有结论的报告）。
    if args.limit > 0:
        post = report.sha256_of(report.release_path("d"))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· "
            f"{report.rel(report.release_path('d'))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    text += (
        f"\nRESULT: {'PASS' if ok else 'FAIL'}"
        f"{report.result_suffix('d', args.limit, meta, FOCUS)}\n"
    )
    # 绝对路径痕迹的扫描**必须放在最后**（含 `RESULT:` 行与自检段）——旧版在 append
    # 这两段之前扫，那两段没被扫过。且命中时写进报告的那串要过 `report.scrub`，
    # 否则"报告里出现绝对路径"这条消息本身就把绝对路径带进了入库的报告。
    dirty = report.path_audit(text)
    if dirty:
        text += (f"\n报告里出现绝对路径痕迹 {report.scrub(str(dirty))!r}"
                 f"——违反「报告只带仓库相对路径」，判 FAIL\n")
        ok = False

    report.flush(out, text)
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
