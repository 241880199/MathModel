"""正文抽取判据 B1/B2/B3/B4 + 正文侧水印判据 A2/A3。

B1 非空且与 pdftotext（另一引擎）字数差 <= 2%；md 与 PDF 文本层是**双边等式**
B2 识别出的标题数 >= 论文自己 Contents 页的条目数
B3 **过度提升**：`## ` 行承载的非空白字符 <= 全篇 20%（B1/B2 都抓不到的那一类）
B4 **假标题**：md 里没有 项目符号前缀 / 裸 token / 无字母数字 的 `## ` 行
A2 产出的 md 里水印字 0 命中
A3 置空流所移除的 span **全部**是水印碎片

报告是入库的判据证据，所以（与 verify_wm.py 同规矩）：
  * 一律 write_bytes + LF 落盘，只写仓库相对路径；
  * 报告写入无条件执行（main 的结尾，不在 try 内）——脚本崩了也不能把上一次
    的 RESULT: PASS 留在库里冒充本次结论；
  * io / textmd / watermark 的 import 放在 checks() 体内：模块被改坏时 import
    当场抛，那是 main() 的 try 保护得到的路径，能拿到「崩溃 → 写成 FAIL」的证据；
  * **放行证据与限样本报告分两个文件**（见「限样本跑不得覆写放行证据」一节）：
    `report_path` 把全量跑映射到 `tests/papers/reports/b-report.txt`、把 `--limit N`
    映射到别处。**措辞强度要说准**：守卫保证的是"绕开就判 FAIL 并改写落点"，不是
    "物理上写不进去"——调用点被绕开时限样本跑**仍会写进**放行证据本体，那一次判 FAIL
    并在报告里写明（probe B 的实测正是这个形态，见该节）。

## B1 为什么在 ASCII 子集上比（2026-09-23 实测，本脚本每次运行重算）

初版 B1 直接比两侧的非空白字符总数，实测 43 份里 **3 份超 2%**
（`2515235` 2.07%、`2524070` 2.53%、`2508861` 3.94%）。逐篇追差异，超出的部分
**全部**是数学字母数字符号（U+1D400–U+1D7FF，论文里的 CambriaMath 公式），
而 pdftotext 那侧是 0：

| 论文 | 我方非 BMP | pdftotext 非 BMP | 差值 |
| :--- | ---: | ---: | ---: |
| 2508861 | 1910 | 0 | 3.94% |
| 2524070 | 901 | 0 | 2.53% |
| 2515235 | 735 | 0 | 2.07% |

全语料 201 份上重算（不是拿试点当通则）：pdftotext 的**每一个**非 ASCII 块都是
0（CJKUnified 55007→0、Greek 5004→0、MathOperators 7553→0、MathAlphanumeric
26828→0）。加 `-enc UTF-8` 不能救：xpdf 4.00 对 Identity-H 字体不去解 ToUnicode
的代理对，改为逐字形吐 U+FFFD（实测 2515235 一份 4410 个）。

**结论**：第二引擎在本语料上对非 ASCII 内容两种模式都不可信——默认编码下直接丢，
UTF-8 下吐替换字符。于是 B1 把**两侧都投影到 ASCII 子集**再比。这是**缩小比对
范围**，不是放宽阈值：阈值仍是 2%。**代价要说清**：B1 因此不覆盖 CJK 与数学符号
的完整性（那部分没有可信的第二参照）。投影后的结果与「输出流该按什么编码解码」
无关——ASCII 字节在任何编码下都是同一个字符。

另：`-enc UTF-8` 是必需的。xpdf 4.00 的默认输出不是 UTF-8（全语料按 UTF-8 解码
会得到 14083 个 U+FFFD），默认编码下还会把 `’` 转写成 ASCII `'`，让两侧字符不同源。

## B1 的伴随判据：双边等式，不是「不少于」（2026-09-23 改为等式）

原写法只拿 `filt`（PDF 置空后的文本层）与 pdftotext 比——**那量的是 PDF，不是本
阶段落盘的 `corpus/papers/md/`**。`to_markdown` 若静默丢正文，A2（无越界水印字）
绿、A3（移除的都是水印碎片）绿、B1（PDF 的文本层没变）绿——整条链子没有一条会红，
而交付物已经残缺。

**上一轮补的是单边下界 `md_nons >= own_raw`，那是过宽的**：`to_markdown` 加的标记
（`<!-- page N -->` 每页一条、`## ` / `*` / `**`）本身就带字符，实测 43 份的差值
+462…+1315，所以「最多可以静默丢 1315 个非空白字符（正文的 2.5%）仍然绿」——
**静默丢一段正文能通过**。单边下界挡住的是「丢得比标记还多」，不是「丢了一段」。

标记是**可精确记账**的，所以这里改成**等式**：

    md 的非空白字符数 − filt 的非空白字符数 == 标记贡献的非空白字符数

标记贡献由 md 自身的标记语法当场数出来（页标记 `<!-- page N -->` = 11 + N 的位数；
`## ` 2 个；`*…*` 2 个；`**…**` 4 个）。两侧**任何**方向的偏差都红：少了 → 丢了正文，
多了 → 多出了正文。实测 43 份该等式**逐份成立**（差值 − 标记 = 0）。

## B2 的实测口径（2026-09-23 修正：上一轮的证据文件写了关于语料的错事实）

上一轮的报告与证据文件写「B2 不适用 30 份（未检出 Contents 目录）」，并把原因
归到「论文没有 Contents 页…这是语料实况」。**那是错的**：独立量过 43 份原件，
**42 份都有含 `Contents` 的页**（只有 `2517199` 没有）。

真实原因在**排版**：这些目录页的点引线是**带空格的**点（`1.1 / Background . . . . . / 3`，
页码另起一行），而旧写法用 `\\.{3,}\\s*\\d+\\s*$` 要求「点＋页码同一行」，于是 30 份
里 29 份解析出 0 条，再被 `if toc_entries:` 与「没有目录」**合并成同一条分支**——
**一个真实存在的参照被静默丢掉**（正是全局约束点名要防的方向）。

三处修正：

1. **点引线口径**：接受点号族（`.`、`·`、`•`、`…`、`․`）与点之间的空白。语料里
   41 份用 ASCII `.`；`2500759` 全篇用 U+00B7（`· · · ·`）——按只认 ASCII 点的口径
   它会落到「有目录页却解析 0 条」的硬失败，但**参照其实存在且可读**，那种硬失败
   是误报，故一并接受。
2. **引线折行**：引线过长会折到下一行（整行只有点）。先把「整行只有点」的行并进
   上一行再数，否则一条条目会被数成两条（`2522820` 的目录页有 9 处折行）。
3. **三态拆分**，不许把「有参照但没读出来」混进「没有参照」：
   * (a) 没有 Contents 页　　　　 → 记「不适用」，**不计入通过**；
   * (b) 有 Contents 页但解析 0 条 → **硬 FAIL**（参照存在，是我们没读出来）；
   * (c) 解析出 n>0 条　　　　　　→ 比 `res.n_headings >= n`。
   另外**不再**在第一个含 `Contents` 的页上 `break`：逐页找，取解析出条目最多的那页
   （正文里可能只是提到 Contents，或目录页不止一处）。

修后实测：**适用 42/43**（上轮 13/43）；`2517199` 无 Contents 页（不适用）。
`2522820` 当时不通过（标题 20 < 目录条目 26），**根因不在本文件**：它的小节标题是
12.0pt（正文 10.9pt、章标题 14.4pt），落在 `HEADING_MIN_SIZE = 13.5` 这个**全局绝对
常量**之下。2026-09-24 已把该常量换成**逐篇相对阈值**（`textmd.HEADING_DELTA`，取法
与全 43 份的字号直方图证据见 `reports/b2-size-histogram.txt`），B2 由此转为全通过。

**这条红是本轮最有价值的产出**：它不是误报，是判据暴露的真实缺口（md 对小节层级的
结构保真度），而"其余 42 份绿着"正是最容易掩盖它的形态。

## B3 过度提升（2026-09-24 新增）

B1 的双边等式**抓不到**"阈值调得太低"：把正文句子提为 `## ` 时，标记数会同步变大，
`md 非空白字符 − filt 非空白字符 == 标记字符数` 照样成立。B2 也抓不到——它只有下界。

B3 因此量**标题占全篇的份量**：

    md 里 `## ` 行承载的非空白字符 <= 全篇非空白字符 × 20%

* 定稿规则下实测全 43 份最大 **7.99%**（`2504218`，本次运行的汇总行会重算），
  余量 2.5 倍；
* 把阈值降到正文层（`HEADING_DELTA = -0.5`，见变异证据 M9）实测 **84.9%–88.6%**
  （**限样本 5 份口径**——M9 本身跑的是 `--limit 3` + 见证集，没有全量口径这一说）
  ——两侧相差一个数量级，不是擦边判定。
* **它在什么情况下会失败**：只要实现开始把正文句子（整段、整页）当标题提升，分子
  立刻从"章节标题"变成"正文"，分母不变 → 越界。20% 这个上界是**量出来的**，不是
  推出来的；下界那一侧由 B2 守着，两条合起来才是双边。

**已知边界（如实登记，不声称解决）**：`2504218` 正文 10.0pt，而摘要页正文与 Notation
表也在 12.0pt，相对阈值必然把它们一并提升（实测 61 → 244 行，再经假标题排除后 213）。
这不是参数没调好——12.0 在 `2522820` 是必须认的小节标题（正文 +1.1），在 `2504218`
是要排除的摘要页（正文 +2.0），**任何单一阈值都同时满足不了**。B3 的上界设在 20%
（而不是 10%）正是承认该边界。要真正分开，需要引入版式/内容判据（例如"标题所在
block 只有 1–2 行"），超出本轮范围。

### B3/B4 的伴随判据：**标题集合非空**（2026-09-24，自查补）

写完 B3/B4 才发现它们与 A3 是同一个形状：**零标题时两条都恒真**——"没有假标题"
trivially 成立，"标题承载占比 0% ≤ 20%" 也 trivially 成立。而实现一旦把标题全丢光
（例如 `is_heading` 恒假、`is_title` 误判成恒定拒绝），两条判据会**一起绿着**。
本项目 4.2 的第 5 例正是这个形状（A3 的 `not bad_removed` 在零移除时恒真）。

故两条都加同一句前置条件 `bool(head_lines)`：零标题即 FAIL，且失败行明写
"前置条件未满足，不得算通过"。它还是 `2517199` 唯一的前置守卫——那份**没有 Contents
页**，B2 对它记"不适用"，没有这句它就只剩 B4 一条会说话的判据。
变异 M12（`is_heading` 恒假）证明这句真的会红。

## B4 假标题（2026-09-24 新增）

md 里不得出现这些形态的 `## ` 行（每一条都实测到具体实例，43 份全量量过）：

| 形态 | 实例 | 为什么不是标题 |
| :--- | :--- | :--- |
| 纯单字母 | `## A`、`## x`、`## z` | 摘要页栏位值 `Problem Chosen: A`；图表轴标 |
| 纯数字 | `## 2500836`、`## 2025`、`## 1` | `Team Control Number` 栏位值；目录页码；章节号 |
| 项目符号前缀 | `## ⚫ Step 1: …` | 列表项，且同篇 `Step 2` 缺失（提升不一致） |
| 无字母数字 | `## ∑`、`## (`、`## U+F0E5` | 公式字形与 Symbol/Mathtype 私有区码位 |

前两类合计 87 行落在第 1 页（摘要页），其余散在正文（图表轴标 `X`/`z`、表格单元
`h`/`p`、`2500759` 目录页的页码 11 行）；"无字母数字"一类实测 153 行 / 10 份。

口径与 `textmd.is_title` 是**同一份规格的两处实现，但不共享代码**：常量与正则在本文件
另写了一份副本（`FAKE_BARE` ≡ `_BARE_TOKEN`、`FAKE_BULLET` ≡ `BULLET_CHARS`，逐字节
相同）。所以它抓得住的是**实现侧**的放宽/收紧——`textmd` 那侧改宽了，这里不会跟着变，
会红；但**规格本身若错（正则/字表写错），两侧会同时错，B4 不会喊**。故两处必须同步改：
本文件的判据是**下界**（实现比它更严时它不会喊）。

## `--limit N`：变异演示与发布校验分样本量（2026-09-24 新增）

Task 3 上一轮单次墙钟 85 分钟，根因是"演示也跑了全量 43 份"。故本脚本支持
`--limit N`：取排序后的**前 N 份**，并**并入固定见证集** `FOCUS`。

**不并入 FOCUS 是不行的**：`2522820` 排在排序序第 29 位，`--limit 3` 取不到它，
而它正是逼出相对阈值的那一份——B2 的变异演示会在一个看不见它的样本上"绿着通过"。
`2500836` 是假标题（`## A`/`## 2500836`/`## ⚫`）的实例件，`2504218` 是正文最小
（10.0pt）与过度提升边界的实例件。

取样运行的报告会写明 `样本 N/43`，且 RESULT 行变成
`RESULT: PASS (LIMITED …)` / `RESULT: FAIL (LIMITED …)`——**限样本的绿不得冒充放行
结论**（`^RESULT: PASS$` 只可能来自全量跑）。

## 限样本跑不得覆写放行证据（2026-09-24 修复机制缺陷）

上一版把两条路径做成**同一个常量** `REPORT`，`main()` 结尾无条件写它：

    REPORT.write_bytes(text.encode("utf-8"))          # 旧版，无 --limit 分支

于是 `--limit 3`（5 份样本）**把 43 份全量跑的放行证据整个覆写掉**——`git status`
上是一处「修改」，`git checkout` 才还原得回来。当时加的那半条防线（限样本跑的
RESULT 行带 `LIMITED` 后缀）**挡不住它**：后缀让人**读的时候看出来**，可覆写已经
把 43 份的结论删了。它属于本项目栽过五次的「判据/证据在什么都没验的情况下报绿」
家族（判据空过、崩溃后旧 `RESULT: PASS` 留在库里冒充本次结论、证据文件里写假断言）。
计划强制 Task 4–7 的每个校验脚本都提供 `--limit N`（变异演示一律 `--limit 3`），
所以这个机制会被复制四次，必须在源头挡住。

**防线从「读的时候看得出来」升级为「根本不覆盖」**，三处：

1. **落点随样本口径分离**（`report_path()`，全脚本唯一决定写哪份的地方）：

   | 样本口径 | `report_path` **选定**的落点 | 那个落点入库？ |
   | :--- | :--- | :--- |
   | `--limit N`（N>0） | `tests/papers/reports-limited/b-report-limited-N.txt` | **否**（根级 .gitignore 忽略） |
   | 全量（`limit <= 0`，默认） | `tests/papers/reports/b-report.txt` | **是**（放行证据） |

   **这张表的唯一读法**（2026-09-24 复审第 4 条：表格里原来写的是「限样本那份
   **不入库**」/「入库=否」，与 `LIMITED_DIR` 那处**已限定**的注释（"选为"）处理
   不一致；本轮统一到**限定**这一种读法，并由它支配）：表说的是 `report_path`
   **选定**哪个落点、以及**那个落点**入不入库——**不是**"限样本跑写下的字节永远
   不会进 git"。理由：**路径只是选择器**，实际写到哪由守卫决定（调用点被绕开时
   限样本跑实际写的就是放行证据本体，那一次判 FAIL 并在报告正文里写明；probe B
   的实测正是这个形态，见下面的三道防线表）——所以「入库=否」是**被选为**的那个
   文件的性质，不是对实际字节的保证。（`--help` 首句里的"（不入库…）"是同一形状
   的未限定句，非交付物，**登记**在此，不改。）

   限样本那份**按设计不入库**：每次样本口径都可能不同，进 git 只制造噪声 diff。
   文件名带 `N` 于是 `--limit 3` 与 `--limit 5` 互不覆盖。样本口径的权威声明在
   正文（`样本 N/M 份` + `取样：…` 那两行 + RESULT 行的 `LIMITED` 后缀），
   因为限样本样本集是「前 N 份 ∪ `FOCUS` 见证集」，不是「N 份」。

2. **`resolve_report()` 落点守卫（fail-closed tripwire）**：限样本跑算出的落点若与
   放行证据重合（即 `report_path` 被人改回单路径），**既不写放行证据，也不是干脆
   不写**——改写到不入库目录 + 报告里明写守卫触发 + 判 FAIL。后半句同样重要：
   「不写」会让上一次的 PASS 留在库里冒充本次结论，那是同一家族的另一个形态。

3. **限样本跑的落点自检（每次都当场量、当场判）**：跑前取一次放行证据的 sha256，
   **落盘之后**再取一次，两次**必须相同**，写进报告并参与判定。顺序是要紧的——
   "量完再写"量到的是覆写**之前**的字节，判据会对着已经被覆写的事实报 True
   （probe B 的实测，见下）。**已知边界（如实登记）**：只盯得住本进程；另有并发的
   全量跑同时写那份证据时它看不出来（没有共同锁，也不在本判据的职责范围）。

**三道防线各自实测能挡住什么**（改坏被测代码 → 跑 `--limit 3` → 看红不红；
probe A/B 的逐字输出见 `.superpowers/sdd/task-3-round2-report.md`）：

| 改法 | probe A：`report_path` 的 `limit>0` 分支改回 `REPORT` | probe B：调用点绕开守卫（`out, _ = REPORT, ""`） |
| :--- | :--- | :--- |
| (1) `resolve_report` 决策点守卫 | **红**（改写落到不入库目录） | 不触发（守卫被整个绕开） |
| (2) 写前 `out == REPORT` 复核 | 不触发（落点已被改写） | **红**（写前复核当场判 FAIL） |
| (3) 落盘后 sha256 对账 | 不触发（没写 REPORT） | **红**（`两次相同 = False`） |

(1)(2) 判的是**落点决策**，(3) 判的是**字节事实**（兜底）；任一层红了，`ok` 就是
False、退出码就是 1、RESULT 行就是 FAIL。

**"改不红就是假判据"——两处都是实测抓出来才改对的，不是想出来的**：

* 只留 (1) 不够。probe A 第一跑：守卫消息写进了报告，`RESULT` 行却照样打印
  `PASS`、退出码照样 0（守卫消息没并进 `ok`）——判据说了话而结论不听；补一句
  `if guard_msg: ok = False` 才红。
* 只留 (3) 不够。probe B 第一跑：`两次相同 = True`，而 `b-report.txt` 的 sha256
  已经从 `83dc4396…` 变成 `055d69e3…`——**缺陷在场时判据正好不喊**，因为 `post`
  是在本次覆写**之前**量的。把量测挪到落盘之后才红。

**修复前的代码上实测过它会红**（这条验收不是事后补的装饰）：`--limit 3` 把
`tests/papers/reports/b-report.txt` 从 `83dc4396…` 覆写成 `124bebb9…`，
`git status --short tests/papers/reports/` 出现 ` M`。

## 反方向：全量跑必须落在放行证据上（2026-09-24 复审补，上面那个机制的镜像）

上面那三道防线**只覆盖了一个方向**：`pre` 只在 `limit > 0` 时量，守卫也一律以
`args.limit > 0` 为前提。**没有任何一句**断言全量跑的落点就是放行证据。于是把
`report_path` 的全量分支（`limit <= 0`）改坏（`return LIMITED_DIR / …`，正是
「`report_path` 被人改回单路径」那类改动的**镜像**）之后：

* 全量跑静默写进 `reports-limited/`：不触发任何守卫、不量 sha、
  `RESULT: PASS` **且无 `LIMITED` 后缀**、退出码 **0**；
* 而 `b-report.txt` **保留上一次的 `RESULT: PASS`** 冒充本次结论——本文件开头点名
  的"报告停在旧状态"家族（main 结尾那句"无条件写"就是为它加的，落点一改就失效）。

**完全无红**，且是"改坏被测代码但所有判据都绿"的形态。补法（两处，与正向互为镜像）：

4. **`resolve_report()` 的镜像守卫**：`limit <= 0` 且落点不是放行证据 → **改写回
   放行证据** + 报告里明写守卫触发 + 判 FAIL。改写方向与正向那条相反是要紧的：
   **决策点上**正向那条把与 `REPORT` 重合的落点**改写走**（不写别人家的证据），反向
   这条**必须**把它改写成 `REPORT`（全量跑本来就拥有它，而且不许把旧结论留在原地）。
   **"禁止写 `REPORT`"这个说法只对决策点那条守卫成立**：写前复核（2）只判 FAIL、
   **不改写 `out`**——probe B 的实测就是证据（调用点被绕开后限样本跑**确实写进了**
   放行证据本体，靠 (3) 的 sha 对账与 (2) 的 FAIL 才红）。
5. **写前复核的镜像**：`args.limit <= 0 and out != REPORT` → 判 FAIL 并**改写回
   放行证据**。理由与 (2) 完全对称——决策点守卫可以被改坏**调用点**绕过去。

**这道镜像的两条守卫谓词是 `<= 0`**（2026-09-24 复审收口）：`pick_sample` 把
`limit <= 0` 当全量跑，故"全量跑"的全部取值是 `<= 0`。此前写的是 `== 0`，于是
`--limit -3`（一次真全量跑、却不等于 0）从中间穿过去，两条反向守卫静默不触发；
实测见 `build/vb_where_captured/neg_prefix.txt` 的 C2 格。

**实测会红**（"改不红就是假判据"，做法同 probe A/B：改坏被测代码 → 跑
`python tests/papers/verify_b.py` 全量 → 看红不红）：把 `report_path` 的全量分支
（`limit <= 0`）改成 `return LIMITED_DIR / f"b-report-limited-{limit}.txt"`，
全量跑实测 `EXIT=1`、`RESULT: FAIL`（**无 `LIMITED` 后缀**——它是一次真全量），
且**其余判据全绿**（`全部判据通过: True`）——即本条红是**唯一**的说话者，正是
"这个方向上此前没有判据"的实测形态。落点被守卫改写回放行证据（`reports-limited/`
下**没有**出现 `b-report-limited-0.txt`），报告顶部写着落点守卫 FAIL。逐字输出见
`.superpowers/sdd/task-3-round2-report.md` 的「修复：落点判据的反方向」。

## A3 的已知边界（不声称更强的东西）

A3 是**必要非充分**：正文里若恰好有一个 span 的文本等于水印碎片（例如单独一个
「校」字），它被误删时 A3 会放行。本语料实测 0 例（本脚本每次运行重算并打印）。

**这条边界现在设门**（2026-09-23）：`n_boundary`（置空后仍在文本中、且本身是
WM_WORDS 子串的 span 数）> 0 即 FAIL。上一轮它只被打印、不参与判定——量了却不判。
它还是**唯一**盯得住「水印按单字片段绘制」的判据：`WM_WORDS` 是多字短语，A2 按短语
包含匹配、`had_wm_text` 同理，2023 那批（77 份按 校/苑/数/模 单字片段绘制）若有片段
残留，只有这条计数会看见。
"""
import hashlib
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
# 放行证据：**正常路径下只有 43 份全量跑**写这一份，入库、受版本控制（.gitattributes
# 的 `tests/papers/reports/**  -text` 保证 blob 与工作树是同一串字节）。"正常路径"
# 是必须加的限定：限样本跑若落到这里（report_path 被改回单路径），落点守卫判 FAIL
# 并在报告里写明"实际落点就是放行证据"，见 resolve_report()。
REPORT = REPORTS / "b-report.txt"
# 限样本跑（`--limit N`）的落点由 report_path() **选为**另一个文件（与放行证据不
# 重合、不入库——根级 .gitignore 忽略 `tests/papers/reports-limited/`）。"选为"
# 不等于"实际写到哪"：调用点被绕开时，限样本跑实际写的就是放行证据本体，那一次判
# FAIL 并在报告正文里写明（见 resolve_report）。落点的选择集中在 report_path() 一处，
# 理由见模块 docstring 的「限样本跑不得覆写放行证据」。
LIMITED_DIR = HERE / "reports-limited"
WS = re.compile(r"\s+")
NON_ASCII = re.compile(r"[^\x00-\x7F]")

# 点引线：点号族 + 点之间的空白。`.` 之外还有 U+00B7 `·`（2500759 全篇如此）、
# U+2026 `…`、U+2022 `•`、U+2024 `․`——语料实况，不是猜的。
LEADER = re.compile(r"(?:[.·•…․]\s*){3,}")
# 整行只有点（引线折行的续行）
LEADER_ONLY = re.compile(r"^[\s.·•…․]+$")
CONTENTS_MARK = "Contents"

# 页标记 `<!-- page N -->` 里非空白字符的固定部分：`<!--` + `page` + `-->`
PAGE_MARK_BASE = len("<!--") + len("page") + len("-->")
PAGE_MARK = re.compile(r"^<!-- page (\d+) -->$")

# B3 的上界：`## ` 行承载的非空白字符 / 全篇非空白字符。**量出来的**——定稿规则下
# 全 43 份最大 7.99%（2504218，见模块 docstring 的已知边界），取 20% 有 2.5 倍余量；
# 阈值降到正文层时实测 84.9%–88.6%（**限样本 5 份口径**——变异 M9 本身跑的是
# `--limit 3` + 见证集，**没有全量口径这一说**；与上一句的全 43 份不是同一个口径，
# 两句并列时不得当成同口径的两个数）。两边相差一个数量级，不是擦边判定。
HEADING_BUDGET = 0.20

# `--limit` 的见证集：必须并入取样，否则演示会在看不见关键样本的集合上"绿着通过"。
#   2522820 逼出相对阈值（正文 10.9pt，小节 12.0pt 落在旧的绝对常量 13.5 之下）
#   2500836 是假标题实例件（## A / ## 2500836 / ## ⚫ Step 1）
#   2504218 是正文最小（10.0pt）与过度提升边界件（摘要页正文与标题同为 12.0）
FOCUS = ("2500836", "2504218", "2522820")

# B4 的形态。**另写一份副本，不 import textmd 的常量**：故能抓住实现侧的放宽/收紧
# （textmd 改了这里不跟着变，必须同步改）；规格本身若错则两侧同错，不代表已验。
# 它是规格的下界——实现比它更严时它不会喊，实现一旦放宽就会红。
FAKE_BULLET = re.compile(r"^[" + re.escape("⚫●○•∙▪▫■□◆◇★☆") + r"]")
FAKE_BARE = re.compile(r"^[A-Za-z]$|^[0-9]+$")


def fake_reason(t: str) -> str:
    """`## ` 行文本 → 假标题的原因；不是假标题返回空串。"""
    if FAKE_BULLET.match(t):
        return "项目符号前缀"
    if FAKE_BARE.match(t):
        return "裸 token（单字母/纯数字）"
    if not any(c.isalnum() for c in t):
        return "无字母数字（公式/私有区字形）"
    return ""


def pick_sample(pdfs: list[Path], limit: int) -> list[Path]:
    """`--limit N` 的取样：前 N 份 ∪ 见证集（见 FOCUS 的注释）。"""
    if limit <= 0:
        return pdfs
    chosen = {p for p in pdfs[:limit]}
    chosen |= {p for p in pdfs if p.stem in FOCUS}
    return sorted(chosen)

# 报告只许带仓库相对路径。这三种形态是「机器特定绝对路径」的判据形态。
ABSPATH_TRACE = re.compile(r"\b[A-Za-z]:[\\/]|\\\\[^\s]|/(?:Users|home|root)/")
_ABS_WIN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>|]*")
_ABS_UNC = re.compile(r"\\\\[^\s\"'<>|]+")
_ABS_POSIX = re.compile(r"/(?:Users|home|root|tmp|var|opt|mnt|Volumes)/[^\s\"'<>|]*")


def scrub(s: str) -> str:
    """把仓库根与任何绝对路径形态替换成占位符。"""
    s = s.replace(str(ROOT), "<repo>").replace(ROOT.as_posix(), "<repo>")
    s = _ABS_WIN.sub("<abs-path>", s)
    s = _ABS_UNC.sub("<abs-path>", s)
    s = _ABS_POSIX.sub("<abs-path>", s)
    return s


def rel_code_path(name: str) -> str:
    """代码文件路径 → 仓库相对路径；仓库外的（stdlib/第三方）只留文件名。"""
    try:
        p = Path(name).resolve()
    except Exception:  # 路径拿不到时也不能把原串写出去
        return "<路径无法解析>"
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return f"<外部>/{p.name}"


def fmt_exc(e: BaseException) -> str:
    """异常 → 机器无关、只带仓库相对路径的文本。

    **不得用 traceback.format_exc()**：它每条栈帧都把**仓库根写成绝对路径**
    （`File "` + 盘符路径 + `"`），于是**崩溃那一次**
    会把机器特定绝对路径写进入库的报告——违反「报告只带仓库相对路径」。
    平时的绿跑看不出这条，正好在看门狗触发那刻破，所以必须在这里消毒，
    而不是靠人事后看一眼。异常**消息本身**也可能带绝对路径（例如
    `FileNotFoundError(io.ORIGIN / ...)`），同样过一遍 scrub。
    """
    frames = []
    tb = e.__traceback__
    while tb is not None:
        code = tb.tb_frame.f_code
        frames.append(
            f'  File "{rel_code_path(code.co_filename)}", '
            f"line {tb.tb_lineno}, in {code.co_name}"
        )
        tb = tb.tb_next
    out = ["Traceback (most recent call last):", *frames,
           f"{type(e).__name__}: {scrub(str(e))}"]
    ctx = e.__context__ if e.__cause__ is None else e.__cause__
    depth = 0
    while ctx is not None and depth < 5:
        out.append(f"[链上异常 {depth + 1}] {type(ctx).__name__}: {scrub(str(ctx))}")
        ctx = ctx.__context__ if ctx.__cause__ is None else ctx.__cause__
        depth += 1
    return "\n".join(out)


def pdftotext_text(p: Path) -> str:
    """第二引擎的文本。stderr 里的字体告警属预期，用 -q 压掉，不视为失败。

    **必须显式 `-enc UTF-8`**：默认编码下 xpdf 4.00 会丢掉全部非 ASCII 字符并
    把 `’` 一类的字符转写成 ASCII，两侧字符就不是同一个来源了（见模块 docstring）。

    pdftotext 不在 PATH 上时**不吞掉**：B1 的独立参照就此消失，必须抛出去落到
    main 的 FAIL 路径，而不是当作「量不了就跳过」。
    """
    r = subprocess.run(
        ["pdftotext", "-q", "-enc", "UTF-8", str(p), "-"],
        capture_output=True,
        timeout=300,
    )
    return r.stdout.decode("utf-8", "replace")


def marker_chars(md: str) -> tuple[int, int, int, int, int]:
    """md 里标记贡献的非空白字符数。

    只数 `to_markdown` 会加的标记，逐条对应它的三个分支：
      * 每页一条 `<!-- page N -->` → 11 + N 的位数（`page` 与 N 之间的空格是空白，不计）
      * 标题 `## X` → 2（`##`）
      * 图注 `*X*` → 2
      * 粗体 `**X**` → 4
    返回 (合计, 页标记, 标题数, 图注数, 粗体数)，便于 FAIL 时逐项对账。
    """
    n_page = n_head = n_cap = n_bold = 0
    for ln in md.split("\n"):
        m = PAGE_MARK.match(ln)
        if m:
            n_page += PAGE_MARK_BASE + len(m.group(1))
        elif ln.startswith("## "):
            n_head += 1
        elif ln.startswith("**") and ln.endswith("**") and len(ln) > 4:
            n_bold += 1
        elif ln.startswith("*") and ln.endswith("*") and len(ln) > 2:
            n_cap += 1
    total = n_page + 2 * n_head + 2 * n_cap + 4 * n_bold
    return total, n_page, n_head, n_cap, n_bold


def toc_entries(page_text: str) -> int:
    """Contents 页的条目数。

    引线过长会折到下一行（整行只有点），先把那种续行并进上一行——否则一条条目
    会被数成两条（`2522820` 的目录页实测 9 处折行，不并会多算）。
    """
    merged: list[str] = []
    for ln in page_text.split("\n"):
        if merged and LEADER_ONLY.match(ln) and ln.strip():
            merged[-1] = merged[-1].rstrip() + " " + ln.strip()
        else:
            merged.append(ln)
    return sum(1 for ln in merged if LEADER.search(ln))


def rel(p: Path) -> str:
    """路径 → 报告里可写的仓库相对形式。

    报告只许带仓库相对路径（`ABSPATH_TRACE` 每次运行当场扫），所以写路径进报告
    一律走这里，不 print 原始 `Path`。
    """
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except Exception:  # 解析不了也不能把原始串（可能带盘符）写出去
        return "<仓库外路径>"


def report_path(limit: int) -> Path:
    """样本口径 → 报告落点。**全脚本唯一决定写哪一份的地方。**

      * `limit > 0`（限样本 / 变异演示）→ `tests/papers/reports-limited/` 下的
        独立文件（入库与否按"被选为的落点"判定：那个目录不入库）；文件名带
        `limit`，于是 `--limit 3` 与 `--limit 5` 互不覆盖；
      * `limit <= 0`（全量；谓词与 `pick_sample` 的 `limit <= 0` 同口径，
        2026-09-24 复审收口）→ 放行证据 `tests/papers/reports/b-report.txt`。

    为什么必须分开、以及为什么限样本那份按设计不入库：见模块 docstring 的
    「限样本跑不得覆写放行证据」一节——**这是本轮的修复本体**。
    """
    if limit > 0:
        return LIMITED_DIR / f"b-report-limited-{limit}.txt"
    return REPORT


def resolve_report(limit: int) -> tuple[Path, str]:
    """落点 + 守卫消息（空串 = 未触发）。

    守卫是**结构性 tripwire**，且**两个方向都守**（只守一个方向 = 同一个机制只
    覆盖一半，另一半静默）：

      * **限样本跑不得落在放行证据上**：`limit > 0` 且落点算出来与放行证据重合，
        说明 `report_path` 被人改回了单路径——正是本文件修掉的那个形态。此时
        **既不写放行证据（不覆盖），也不是干脆不写**（不写的话上一次的
        `RESULT: PASS` 会留在库里冒充本次结论，那是同一家族的另一个形态），而是
        改写到不入库目录并在报告里明写守卫触发、判 FAIL。
      * **全量跑必须落在放行证据上**（2026-09-24 复审补：反方向此前**没有任何
        一句断言**——`pre` 与这道守卫都以 `limit > 0` 为前提）。`limit <= 0` 且
        落点不是放行证据，说明 `report_path` 的全量分支被改坏（正是
        上面那条守卫存在理由的**镜像改法**）：全量跑会**静默写进
        `reports-limited/`**——不触发任何守卫、不量 sha、`RESULT: PASS` 且无
        LIMITED 后缀、退出码 0，而 `b-report.txt` 保留**上一次**的 `RESULT: PASS`
        冒充本次结论（模块 docstring 点名的"报告停在旧状态"家族），**完全无红**。
        此时**改写回放行证据**：全量跑本来就拥有这份证据，一次全量跑既不能把
        结论写进别处、也不能把旧结论留在原地。

    **谓词是 `limit <= 0`，不是 `limit == 0`**（2026-09-24 复审收口）：`pick_sample`
    把 `limit <= 0` 当全量跑，所以"全量跑"这个语义的**全部**取值是 `<= 0`；写成
    `== 0` 时 `limit < 0` 落在两者之间——那是一次真全量跑，却两条反向守卫都不认。
    对 `limit == 0` 两者等价，故 C3（全量）的产出不变。
    """
    out = report_path(limit)
    if limit > 0 and out == REPORT:
        return LIMITED_DIR / "b-report-落点守卫触发.txt", (
            f"落点守卫 FAIL：限样本跑（--limit {limit}）算出的落点与放行证据 "
            f"{rel(REPORT)} 重合——report_path 被改坏了。已改写到不入库目录，"
            f"放行证据未被本次运行触碰。"
        )
    if limit <= 0 and out != REPORT:
        return REPORT, (
            f"落点守卫 FAIL：全量跑（limit={limit}）算出的落点是 {rel(out)}，**不是**放行"
            f"证据 {rel(REPORT)}——report_path 的全量分支（`limit <= 0`）被改坏了（这条是"
            f"'限样本不得覆写放行证据'那条守卫的镜像：同一个机制的反方向）。已把落点"
            f"改写回放行证据（全量跑必须拥有这份证据，否则 b-report.txt 会停在"
            f"上一次的状态冒充本次结论），判 FAIL。"
        )
    return out, ""


def sha256_of(p: Path) -> str:
    """文件摘要；不存在时返回哨兵串（**不抛**：缺失本身要能被写进报告）。"""
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "<不存在>"


def checks(
    lines: list[str], limit: int = 0, meta: dict | None = None,
    out: Path | None = None,
) -> bool:
    import fitz  # noqa: F401

    from tools.papers import io, textmd, watermark  # noqa: F401

    WM_WORDS = watermark.WM_WORDS

    root = io.ORIGIN / "2025美赛O奖论文"
    all_pdfs = sorted(root.rglob("*.pdf"))
    # fail-closed：试点目录取不到就抛，不得空跑一圈然后报「全通过」。
    if not all_pdfs:
        raise FileNotFoundError(f"试点目录下没有任何 PDF：{root}")
    pdfs = pick_sample(all_pdfs, limit)
    # 样本量回传给 main()：RESULT 行的 LIMITED 标记要能写出**实际**样本量
    # （限样本集是「前 N 份 ∪ 见证集」，不是 N 份）。checks 抛异常时 meta 为空，
    # 那时 RESULT 行照实写「样本数未能确定」——不拿 --limit 冒充实际样本量。
    if meta is not None:
        meta["n_sample"], meta["n_all"] = len(pdfs), len(all_pdfs)
    if limit > 0:
        lines.append(
            f"B 组 + A2/A3 判据 · **限样本 {len(pdfs)}/{len(all_pdfs)} 份**"
            f"（--limit {limit} + 见证集 {'/'.join(FOCUS)}）"
        )
        lines.append(f"  取样：{' '.join(p.stem for p in pdfs)}")
        # 这一句**按实际的落点 out 判定**，不按 LIMITED_DIR 推定（2026-09-24 复审）：
        # 写死"本文件写在 reports-limited/ 下"时，一旦守卫被绕开，这句会被写进
        # `b-report.txt` **本体**，成为**不成立的断言**——交付物里写假事实正是本
        # 项目反复栽的那个家族。
        if out is None:
            where = "实际落点未传入 checks()，本句无法判定这份报告写在哪儿"
        elif out == REPORT:
            # 指代**不写方向**（2026-09-24 复审 Minor）：本分支唯一可达的形态是
            # "调用点绕开 resolve_report 的守卫、由 main() 的写前复核补判"，
            # 而写前复核的消息是在 checks() **返回之后**才 append 的——那一份
            # 报告里真消息在**下**方；反过来，若哪天 resolve_report 自己在
            # out==REPORT 时就返回消息，消息就会在**上**方。写死任一个方向都有
            # 一种可达形态使它指错，故只指"本报告里有那条消息"。
            where = (
                f"**实际落点就是放行证据 {rel(REPORT)}**——落点判据被改坏或被绕过，"
                f"见本报告中的落点守卫 FAIL 消息，判 FAIL"
            )
        else:
            where = (
                f"实际落点是 {rel(out)}（放行证据是 {rel(REPORT)}，两者不同，"
                f"本次运行不写放行证据）"
            )
        lines.append(
            f"  ! 这是**限样本跑**，不是放行依据：{where}。"
            f"（本句按实际落点判定，不按 {rel(LIMITED_DIR)}/ 推定。）"
        )
    else:
        lines.append(f"B 组 + A2/A3 判据 · 试点 {len(pdfs)} 份")
    lines.append("=" * 72)
    bad = []
    bad34 = []
    n_na = 0          # 无 Contents 页 → 不适用
    n_toc_empty = 0   # 有 Contents 页但解析 0 条 → 硬失败
    n_toc = 0         # 适用
    n_toc_pass = 0
    n_boundary = 0
    n_b3_bad = 0      # 过度提升越界
    n_b4_bad = 0      # 假标题行数合计
    n_b4_papers = 0   # 含假标题行的份数
    frac_max = 0.0
    frac_max_stem = ""
    for src in pdfs:
        try:
            prob = src.parent.name
            md = io.md_path("2025美赛O奖论文", prob, src.stem)
            res = textmd.extract(src, md)

            mdtext = md.read_bytes().decode("utf-8")

            # A2 产出物里水印字 0 命中
            hit = [w for w in WM_WORDS if w in mdtext]
            a2 = not hit

            with fitz.open(src) as doc:
                raw = "".join(doc[i].get_text() for i in range(doc.page_count))
                before = watermark.spans(doc)
                watermark.strip_in_memory(doc)
                after = watermark.spans(doc)
                filt = "".join(doc[i].get_text() for i in range(doc.page_count))

            # A3 **fail-closed**：被置空流移除的 span 必须**全部**是水印碎片。
            # 只要有一个非水印片段消失，就说明 stripping 吃掉了正文 → FAIL。
            # 2023 那批把水印拆成每页 8 个片段（校/苑/数/模/…），所以必须逐 span
            # 做差集，不能靠整段字符串替换——那种做法多替少替都不易察觉。
            removed = Counter(before) - Counter(after)
            bad_removed = [
                t for t in removed if not any(t in w for w in WM_WORDS)
            ]
            # 伴随判据（缺了它 A3 会被自己的前置条件架空）：文本层**本来带水印字**
            # 却一个 span 都没被移除，说明置空根本没生效。此时差集为空，而空差集
            # 当然不含「越界片段」——`not bad_removed` 恒真，A3 绿着通过。这正是
            # 本项目已出现四次的「判据什么都没验就报绿」那一类，故显式判死。
            wm_in_raw = any(w in raw for w in WM_WORDS)
            a3 = not bad_removed and (not wm_in_raw or bool(removed))

            # A3 已知边界的**实测**：置空后仍在文本里的 span，有多少本身就是
            # WM_WORDS 的子串？那类 span 若被误删，A3 会放行。**现在设门**：
            # >0 即 FAIL——上一轮只打印不判定，量了却不判等于没量。它还是唯一
            # 盯得住「水印按单字片段绘制」的判据（WM_WORDS 是多字短语，A2 与
            # had_wm_text 都按短语包含匹配，片段残留它们看不见）。
            n_paper_boundary = sum(
                1 for t in after if any(t in w for w in WM_WORDS)
            )
            n_boundary += n_paper_boundary
            a3b = n_paper_boundary == 0

            # B1 与第二引擎对照（用置空后的文本）。两侧都投影到 ASCII 子集，
            # 理由见模块 docstring——阈值仍是 2%，缩的是比对范围不是阈值。
            pt_text = pdftotext_text(src)
            own_raw = len(WS.sub("", filt))
            other_raw = len(WS.sub("", pt_text))
            own = len(NON_ASCII.sub("", WS.sub("", filt)))
            other = len(NON_ASCII.sub("", WS.sub("", pt_text)))
            diff = abs(own - other) / max(other, 1)
            # 伴随判据（**双边等式**，不是下界）：`filt` 是 PDF 的文本层，md 才是本
            # 阶段真正的交付物。to_markdown 只加标记、不加也不减正文，故
            #   md 非空白字符 − filt 非空白字符 == 标记贡献的非空白字符
            # 必须**逐份成立**。写成下界时「静默丢一段正文」可以过关（松量最大
            # 1315 字符 = 正文 2.5%）；等式两侧任一方向的偏差都红。
            md_nons = len(WS.sub("", mdtext))
            mk, mk_page, mk_head, mk_cap, mk_bold = marker_chars(mdtext)
            delta = md_nons - own_raw
            b1_md = delta == mk
            b1 = diff <= 0.02 and b1_md

            # B2 论文自己的 Contents 页条目数。**三态**，见模块 docstring：
            # (a) 无 Contents 页 → 不适用；(b) 有页但 0 条 → 硬 FAIL；
            # (c) n>0 → 比 res.n_headings >= n。逐页找、取最多的那页，不 break。
            with fitz.open(src) as doc:
                cands = [
                    (pno + 1, toc_entries(doc[pno].get_text()))
                    for pno in range(doc.page_count)
                    if CONTENTS_MARK in doc[pno].get_text()
                ]
            if not cands:
                b2, b2_label = None, "不适用(无 Contents 页)"
                n_na += 1
            else:
                b2_page, n_entries = max(cands, key=lambda t: t[1])
                if not n_entries:
                    b2 = False
                    b2_label = f"FAIL(有 Contents 页 p.{b2_page} 但解析 0 条)"
                    n_toc_empty += 1
                else:
                    b2 = res.n_headings >= n_entries
                    b2_label = f"{n_entries}(p.{b2_page})"
                    n_toc += 1
                    n_toc_pass += bool(b2)

            # B3 过度提升：`## ` 行承载的非空白字符占全篇的比例。B1 的等式与 B2 的
            # 下界都看不见这一类，故单列（见模块 docstring）。参照是**md 自身**——
            # 不依赖 textmd 的内部量，改动实现不会连带改动参照。
            head_lines = [ln[3:] for ln in mdtext.split("\n") if ln.startswith("## ")]
            hchars = sum(len(WS.sub("", t)) for t in head_lines)
            frac = hchars / max(md_nons, 1)
            # **伴随判据**（B3/B4 共用，缺了它两条都会被自己的前置条件架空）：零标题时
            # "没有假标题" 与 "标题承载占比小" 都恒真——实现若把标题全丢光，两条判据一起
            # 绿。本项目 4.2 的第 5 例正是这个形状（A3 的 `not bad_removed` 在零移除时恒真，
            # strip 完全失效也报绿）。故显式要求标题集合非空；`2517199` 无目录页，B2 对它
            # 不适用，这条是它唯一的前置条件守卫。
            has_heads = bool(head_lines)
            b3 = has_heads and frac <= HEADING_BUDGET
            if frac > frac_max:
                frac_max, frac_max_stem = frac, src.stem
            n_b3_bad += not b3

            # B4 假标题：md 里不得有 项目符号前缀 / 裸 token / 无字母数字 的 `## `
            # 行。逐行给出行号与文本（"必须能列出它抓到的是哪几行"）。
            fakes = [
                (i, ln[3:].strip())
                for i, ln in enumerate(mdtext.split("\n"), 1)
                if ln.startswith("## ") and fake_reason(ln[3:].strip())
            ]
            b4 = has_heads and not fakes
            n_b4_bad += len(fakes)
            n_b4_papers += bool(fakes)

            lines.append(
                f"{src.stem:<10} A2水印字={hit or '无'} "
                f"A3移除{sum(removed.values())}span/越界={bad_removed or '无'}"
                f"/边界{n_paper_boundary} "
                f"B1(ASCII) 我方={own:<7} 对照={other:<7} 差={diff*100:5.2f}% "
                f"[原始 我方={own_raw} 对照={other_raw}] "
                f"B2 标题={res.n_headings:<3} 目录={b2_label:<26} "
                f"[md={md_nons} = filt {own_raw} + 标记 {mk} "
                f"{'OK' if b1_md else '不等!'}] "
                f"B3 标题承载={frac*100:5.2f}%/{HEADING_BUDGET*100:.0f}%"
                f"{'' if b3 else ' 越界!'} B4 假标题={len(fakes)}"
            )
            if not b3:
                if not has_heads:
                    lines.append(
                        f"{'':10} ^ B3/B4 FAIL：md 里一行 `## ` 都没有——零标题时"
                        f"「标题承载占比小」与「没有假标题」都恒真，两条判据会被自己的"
                        f"前置条件架空，不得算通过"
                    )
                else:
                    lines.append(
                        f"{'':10} ^ B3 FAIL：`## ` 行承载 {hchars} 个非空白字符 = 全篇 "
                        f"{md_nons} 的 {frac*100:.2f}%，超过上界 "
                        f"{HEADING_BUDGET*100:.0f}%——阈值把正文提到了标题层"
                        f"（全 43 份定稿实测最大 7.99%）"
                    )
            if not b4 and has_heads:
                lines.append(
                    f"{'':10} ^ B4 FAIL：md 里有 {len(fakes)} 行假标题，"
                    f"前几行 = "
                    + "; ".join(
                        f"L{i}={t[:24]!r}({fake_reason(t)})" for i, t in fakes[:4]
                    )
                )
            if bad_removed:
                lines.append(
                    f"{'':10} ^ A3 FAIL：以下被移除的 span 不是水印碎片 "
                    f"{bad_removed[:5]}"
                )
            if wm_in_raw and not removed:
                lines.append(
                    f"{'':10} ^ A3 FAIL：文本层带水印字，却一个 span 都没被移除"
                    f"（置空未生效，空差集不能算通过）"
                )
            if not a3b:
                lines.append(
                    f"{'':10} ^ A3 FAIL：置空后仍有 {n_paper_boundary} 个 span 本身是 "
                    f"WM_WORDS 的子串——边界被踩到，A3 此时可能放行误删；"
                    f"WM_WORDS 是多字短语，片段残留 A2 看不见"
                )
            if not b1_md:
                lines.append(
                    f"{'':10} ^ B1 FAIL：md 非空白字符 {md_nons} − filt {own_raw} "
                    f"= {delta}，但标记只应带来 {mk} 个"
                    f"（页标记 {mk_page} + 标题 {mk_head}×2 + 图注 {mk_cap}×2 "
                    f"+ 粗体 {mk_bold}×4）——"
                    f"{'md 丢了正文' if delta < mk else 'md 多出了字符'}"
                )
            if diff > 0.02:
                lines.append(
                    f"{'':10} ^ B1 超阈：ASCII 差 {diff*100:.2f}% > 2%，"
                    f"须解释差异来源（换行/连字符）；不得调大阈值"
                )
            if not b1 and b1_md and diff <= 0.02:
                lines.append(
                    f"{'':10} ^ B1 FAIL：原因未归类（判据组合异常，须查）"
                )
            if b2 is False:
                if not cands:
                    lines.append(f"{'':10} ^ B2 FAIL：原因未归类（须查）")
                elif not max(c for _, c in cands):
                    lines.append(
                        f"{'':10} ^ B2 FAIL：Contents 页在（p.{b2_page}），"
                        f"但解析出 0 条条目——参照存在，是我们没读出来"
                    )
                else:
                    lines.append(
                        f"{'':10} ^ B2 FAIL：识别出的标题 {res.n_headings} < "
                        f"目录条目 {b2_label}——论文自己声明的小节没被识别成标题"
                    )
            if not (a2 and a3 and a3b and b1) or b2 is False:
                bad.append((src.stem, a2, a3, b1, b2, bad_removed))
            if not (b3 and b4):
                bad34.append((src.stem, b3, b4, frac, len(fakes), has_heads))
        except BaseException as e:
            # 逐篇兜底：一篇抛了不能把其余 42 篇的证据一起带走，更不能让整份报告
            # 停在旧状态。textmd.extract 的 fail-closed 守卫（水印形态未知）正是
            # 走这条路径的合法输入。**异常经 fmt_exc 消毒**：见它的 docstring。
            lines.append(f"{src.stem:<10} ! 处理该篇时抛出异常：")
            lines.append(fmt_exc(e))
            bad.append((src.stem, False, False, False, False, ["<异常>"]))
            bad34.append((src.stem, False, False, 0.0, 0, True))

    lines.append("=" * 72)
    lines.append(
        f"B2 无 Contents 页（记为不适用，**不计入通过**）: {n_na} 份"
    )
    lines.append(
        f"B2 有 Contents 页但解析 0 条（**硬失败**，参照存在）: {n_toc_empty} 份"
    )
    lines.append(
        f"B2 适用 {n_toc} 份 / 通过 {n_toc_pass} 份"
        f"（点引线口径：点号族 + 点间空白；引线折行已并；逐页找不 break）"
    )
    lines.append(f"B1 口径：两侧均投影到 ASCII 子集后再比，阈值 2%（见本文件 docstring）")
    lines.append(
        f"B1 交付物口径：md 非空白字符 − filt 非空白字符 == 标记字符数（双边等式）"
    )
    lines.append(
        f"A3 已知边界实测：置空后仍在文本中、且本身是 WM_WORDS 子串的 span = "
        f"{n_boundary} 个（>0 即 FAIL——边界被踩到）"
    )
    lines.append(
        f"B3 过度提升：`## ` 行承载非空白字符 ≤ 全篇 {HEADING_BUDGET*100:.0f}%；"
        f"本次 {len(pdfs)} 份里最大 {frac_max*100:.2f}%（{frac_max_stem}），"
        f"越界 {n_b3_bad} 份"
    )
    lines.append(
        f"B4 假标题：md 里 项目符号前缀 / 裸 token / 无字母数字 的 `## ` 行；"
        f"本次合计 {n_b4_bad} 行，涉及 {n_b4_papers} 份"
    )
    lines.append(f"A2/A3/B1/B2 全通过: {not bad}")
    lines.append(f"B3/B4 全通过: {not bad34}")
    lines.append(f"全部判据通过: {not bad and not bad34}")
    if bad:
        lines.append("失败明细（每一条都必须给出解释，不得静默）:")
        for stem, a2, a3, b1, b2, bad_removed in bad:
            lines.append(
                f"  {stem}: A2={a2} A3={a3} B1={b1} B2={b2} "
                f"越界移除={bad_removed[:3]}"
            )
    if bad34:
        lines.append("B3/B4 失败明细:")
        for stem, b3, b4, frac, nfake, has_heads in bad34:
            if not has_heads:
                lines.append(f"  {stem}: 零标题（前置条件未满足，B3/B4 不得算通过）")
            else:
                lines.append(
                    f"  {stem}: B3={b3}（标题承载 {frac*100:.2f}%） B4={b4}"
                    f"（假标题 {nfake} 行）"
                )
    return not bad and not bad34


def main() -> int:
    import argparse

    def limit_arg(s: str) -> int:
        """`--limit` 的类型：**非负**整数（0 = 全量，默认；N > 0 = 前 N 份 + 见证集）。

        **为什么在入口上关掉负数**（2026-09-24 复审收口，**两层都要**）：
        `pick_sample` 把 `limit <= 0` 当成全量跑，而两条反向守卫此前写的是
        `limit == 0`——`--limit -3` 于是**是一次全量跑、却不等于 0**，两条反向守卫
        静默不触发。实测（`build/vb_where_captured/neg_prefix.txt`，驱动器 C 的
        C2 格）：`report_path` 尾部被改坏 + `--limit -3` → 写进
        `reports-limited/b-report-limited--3.txt`、**无守卫消息**、**无 sha 对账**、
        `RESULT: PASS`、`EXIT=0`，而放行证据本体留着**上一次**的 `RESULT: PASS`
        冒充本次结论——正是本文件修掉的那个缺陷，从一个单 token 的旁路原地复活。

        谓词那层（`resolve_report` 与写前复核）已统一成 `<= 0`；这一层把负数这个
        入口整个去掉。**只做一层都不叫收口**：只改谓词仍留着一个"看起来合法"的
        负数入口；只改这里则函数被直接调用（或被 Task 4–7 复制的副本）时同一个坑
        还在。注意 `0` 仍是合法值（= 全量，与不放 `--limit` 等价）。
        """
        try:
            v = int(s)
        except ValueError:
            raise argparse.ArgumentTypeError(f"不是整数：{s!r}") from None
        if v < 0:
            raise argparse.ArgumentTypeError(
                f"--limit 不接受负数（收到 {v}）：0 = 全量跑（默认），N > 0 = 只跑前 "
                f"N 份 + 见证集。负数此前会被当成一次**全量跑**，从而绕过两条反向落点"
                f"守卫（`limit == 0` 那条判据看不见它）。"
            )
        return v

    ap = argparse.ArgumentParser(
        description="正文抽取判据 B1/B2/B3/B4 与正文侧水印 A2/A3",
    )
    ap.add_argument(
        "--limit", type=limit_arg, default=0, metavar="N",
        help="只跑前 N 份 + 见证集（变异演示用，秒级）。报告写到 "
             "tests/papers/reports-limited/（入库按 report_path 选定的落点判定；"
             "落点守卫保证不碰放行证据，"
             "绕开守卫即判 FAIL 并把实际落点写进报告）；"
             "0 = 全量（默认，写放行证据 tests/papers/reports/b-report.txt）；"
             "负数不接受（会被当成全量跑从而绕过反向落点守卫）",
    )
    args = ap.parse_args()

    # 落点先定下来（含 fail-closed 守卫，见 resolve_report 的 docstring）：写哪份
    # 由样本口径决定。
    out, guard_msg = resolve_report(args.limit)
    # 跑前先量一次放行证据的 sha256，落盘之后（**注意：落盘之后**，理由见下面那句
    # 注释）再量一次作对账。这给「限样本跑不碰全量放行证据」加一条**字节级判据**，
    # 把约定升级成判据——本项目反复栽的就是"量了却不判 / 判据在缺陷在场时正好不喊"。
    # 全量跑不适用：那一次的产物就是这份证据，它本来就该变。
    # 已知边界：只盯得住本进程；并发的另一次全量跑同时写它时看不出来。
    # **这里的 `args.limit > 0` 是对的，别顺手改成 `<= 0` 去找"一致"**（全局约束
    # "同一语义须用同一谓词"说的是**同一**语义）：本处问的是"**是不是限样本跑**"
    # （= `limit > 0`），反向守卫问的是"**是不是全量跑**"（= `limit <= 0`）。
    # 两个语义互补且合起来覆盖全部整数取值（`--limit` 已由 argparse 拒绝负数，
    # 见 limit_arg），不存在 `> 0` 与 `<= 0` 都认不出的取值。
    pre = sha256_of(REPORT) if args.limit > 0 else ""

    meta: dict = {}
    lines = ["正文抽取校验（B1/B2/B3/B4）与正文侧水印（A2/A3）"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out)
    except BaseException as e:
        lines.append("校验过程中抛出异常：")
        lines.append(fmt_exc(e))
        ok = False

    # **写前落点复核**（第二道，紧贴 write_bytes）。resolve_report 的守卫判在决策点，
    # 而决策点可以被改坏**调用点**绕过去——probe B 就是那么绕的（把
    # `resolve_report(args.limit)` 换成 `REPORT, ""`，守卫整段失效）。这一句在写之前
    # 用**实际要写的那个 out** 再判一次，绕开它就必须直接改这一句。
    if args.limit > 0 and out == REPORT:
        guard_msg = (
            f"落点守卫 FAIL（写前复核）：限样本跑（--limit {args.limit}）的写入目标就是放行"
            f"证据 {rel(REPORT)}——resolve_report 的守卫在调用点被绕过了。判 FAIL。"
        )
        lines.append(guard_msg)
    # **反方向也要复核**（2026-09-24 复审补）：全量跑（`limit <= 0`，与 pick_sample
    # 的口径一致——2026-09-24 复审收口：此前写的是 `args.limit == 0`，`--limit -3`
    # 于是是一次全量跑却不等于 0，这条例外守卫静默不触发）的写入目标必须就是放行
    # 证据。上面 resolve_report 里那条镜像守卫判在决策点，调用点一旦被绕开
    # （例如 `out, guard_msg = report_path(args.limit), ""`）就整段失效；这一句紧贴
    # write_bytes，用**实际要写的那个 out** 再判一次。两个方向合起来才是闭环：
    # 限样本跑不得写放行证据，全量跑**必须**写放行证据——此前只有前一半。
    if args.limit <= 0 and out != REPORT:
        wrong = out
        # 与正向那条守卫的改写方向相反：这里**必须**改写回放行证据（正向**决策点**
        # 那条守卫把与放行证据重合的落点改写走——"禁止写别人家的证据"只对它成立；
        # 正向的**写前复核**只判 FAIL、不改写 out）。反向不许把旧结论留在原地——一次
        # 全量跑必须把结论写进它。
        out = REPORT
        guard_msg = (
            f"落点守卫 FAIL（写前复核）：全量跑（limit={args.limit}）算出的写入目标是 "
            f"{rel(wrong)}，**不是**放行证据 {rel(REPORT)}——落点判据被改坏或在调用点被"
            f"绕过了。已把落点改写回放行证据（全量跑必须拥有这份证据，否则它会停在上"
            f"一次的状态冒充本次结论），判 FAIL。"
        )
        lines.append(guard_msg)
    # 守卫（任一形态）触发就是 FAIL。**这一句不能省**：守卫消息只是往报告里写了
    # "FAIL"，不并进 ok 的话 RESULT 行照样打印 PASS、退出码照样是 0——判据说了话
    # 而结论不听，正是本文件在修的那个家族。probe A 实测抓到的就是这个。
    if guard_msg:
        ok = False

    # 落点声明：写**实际**的那一份（out），不是"应该写的那一份"。守卫改写落点时
    # 两者不同，写后者就是把假事实写进证据。
    lines.append("")
    lines.append(f"写入：{rel(out)}")
    if args.limit > 0:
        if out == REPORT:
            # **本块是 2026-09-24 复审点名的那个漏网**：上一轮只把 checks() 里那句
            # 按实际落点分了支，40 行之外的这里仍然**无条件**写"本文件是限样本跑的
            # 报告，不入库、不是放行依据；放行证据是 b-report.txt，只有 43 份全量跑
            # 会写它"。而在"调用点绕开守卫"的配置下，这一次限样本跑**正是**写进了放行
            # 证据本体（写前复核只判 FAIL、不改写 out）——那三行字就成了写在放行证据
            # 开头的一句反话（上半句把 {REPORT} 说成别人家的文件、下半句自己就是它）。
            # 故本块按**实际** out 分支，与 checks() 那句同一处收口。
            lines.append(
                f"  本次运行是**限样本跑**（--limit {args.limit} + 见证集 "
                f"{'/'.join(FOCUS)}），但**实际落点就是放行证据 {rel(REPORT)} 本体**"
                f"（落点上的「不入库」「不是放行依据」两句**都不成立**，本报告正是那份"
                f"证据文件的内容）——落点判据被改坏或被绕过，见本报告中的落点守卫 "
                f"FAIL 消息，判 FAIL。"
            )
        else:
            lines.append(
                f"  本文件是**限样本跑**（--limit {args.limit} + 见证集 "
                f"{'/'.join(FOCUS)}）的报告，**不入库、不是放行依据**；"
                f"放行证据是 {rel(REPORT)}，只有 43 份全量跑会写它。"
            )
    elif out == REPORT:
        # **这句里有一段限定语，是本轮（2026-09-24 复审第 3 条）折进来的**：原句
        # 「本文件是**全量跑的放行证据**（入库）。限样本跑的落点是 reports-limited/
        # 下的另一份文件，不会写到本文件。」前半句为真（能走到这里就意味着本次运行
        # 的落点就是本文件），后半句却是**关于别的运行**的承诺——而在这句被写出的
        # 那一刻，**从没有任何东西检查过它**：唯一的断言者是限样本侧的正向守卫 /
        # 写前复核 / sha 对账，它们只在**违例的那一次**开火，且那次会用它们的文案
        # 替换这句。所以原句若坏了没有任何东西会去抓这行陈旧文案。限定的强度按模块
        # docstring 开头那句（"绕开就判 FAIL 并改写落点"，不是"物理上写不进来"），
        # **不得写得比实现更强**。
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）——前半句由本条分支的自证"
            f"（本次运行的落点就是本文件）与全量侧的镜像落点守卫共同保证：`limit <= 0` "
            f"而落点不是本文件时，写前复核会把它改写回本文件并判 FAIL。"
            f"限样本跑的落点**按设计**是 {rel(LIMITED_DIR)}/ 下的另一份文件，"
            f"不会写到本文件——**后半句是关于别的运行的承诺，本次运行不检查它**："
            f"它由限样本侧的正向落点守卫与写前复核保证，强度止于「绕开就判 FAIL 并"
            f"改写落点」，不是「物理上写不进来」（调用点被绕开时限样本跑**仍会**写进"
            f"本文件本体，那一次判 FAIL 并在它自己的报告里写明）。"
        )
    else:
        # 与上面限样本那句同一个病（交付物里写不成立的断言），只是反方向：落点不是
        # 放行证据时，绝不能照抄"本文件是放行证据"。**此分支现在（收口后）不可达**，
        # 论证与依赖的两条断言（2026-09-24 复审第 2 条要求写清）：
        #   ① `main()` 的写前复核镜像守卫**条件是 `args.limit <= 0`**（本轮收口前是
        #      `== 0`，`--limit -3` 正好从缺口里进来：那时本分支**可达**，实测在
        #      `reports-limited/b-report-limited--3.txt` 里写下了两句假话——"本次运行
        #      是**全量跑**（limit=0）"（真值是 −3）与"见本报告中的落点守卫 FAIL
        #      消息，判 FAIL"（那份文件里没有该消息，末行是 `RESULT: PASS`）；见
        #      `build/vb_where_captured/neg_prefix.txt` 的 C2 格）；
        #   ② 该守卫在 `out != REPORT` 时**改写** `out = REPORT`，且从那句改写到底下
        #      这个 `else` 之间 `out` 不再被重新赋值。
        # 两条合起来：`args.limit <= 0` ⇒ `out == REPORT`；而本 `else` 的前置恰恰是
        # `args.limit > 0` 为假（即 `<= 0`）且 `out != REPORT`——与 ② 的结论矛盾，
        # 故不可达。**这条论证的强度取决于 ① 用的是 `<= 0`**：`pick_sample` 把
        # `limit <= 0` 当全量跑，所以"全量跑"的全部取值就是 `<= 0`；只要谓词还是
        # `== 0`，`limit < 0` 就落在这两句之间，本分支可达。留在这里是**防御**：
        # 若哪天把改写那句删了，它就是这个方向上唯一的说话者。指代同样不写方向
        # （理由见 checks() 里那句的注释）。
        lines.append(
            f"  本次运行是**全量跑**（limit={args.limit}）：落点**本应是**放行证据 "
            f"{rel(REPORT)}，实际落点是 {rel(out)}——两者不同，见本报告中的落点守卫 "
            f"FAIL 消息，判 FAIL。"
        )

    def flush(body: str) -> None:
        """落盘（LF + write_bytes，见模块 docstring）。"""
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(body.encode("utf-8"))

    text = "\n".join(lines) + "\n"
    # 自检（fail-closed）：报告只许带仓库相对路径。**崩溃那一次最容易破**——
    # traceback 原本每条栈帧都写绝对路径。约束平时看不出来，所以做成每次都当场
    # 量、当场判的判据，而不是靠人事后看一眼。
    dirty = ABSPATH_TRACE.search(text)
    if dirty is not None:
        text += (
            f"\n报告里出现绝对路径痕迹 {dirty.group(0)!r}"
            f"——违反「报告只带仓库相对路径」，判 FAIL\n"
        )
        ok = False
    # **限样本的绿不得冒充放行结论**：`--limit` 那一跑的 RESULT 行带上样本量与
    # 取样口径，于是 `^RESULT: PASS$` 只可能来自全量跑。（上一版只有这条后缀，
    # 它让人"读的时候看得出来"，但**挡不住覆写**——覆写已经把 43 份的结论删了。
    # 现在后缀与落点分离（report_path）是两道互补的防线：落点分离防覆写，
    # 后缀保证即使有人把限样本那份误当放行证据读，也一眼看得出不是。）
    if args.limit > 0:
        n_s, n_a = meta.get("n_sample"), meta.get("n_all")
        scope = (
            f"样本 {n_s}/{n_a} 份 = 前 {args.limit} 份 + 见证集 {'/'.join(FOCUS)}"
            if n_s
            else f"样本数未能确定（checks 未跑到取样处；--limit {args.limit}）"
        )
        suffix = f" (LIMITED {scope}；非放行依据)"
    else:
        suffix = ""

    # 先落盘（不带自检结论与 RESULT 行），**然后**才量放行证据——顺序是要紧的：
    # 本次运行自己的那次 write 也在这之后才发生吗？不是：本次 write 就是这一句。
    # 所以第二遍之前量到的 post 已经把"本次运行覆写过它"算进去了。写成"量完再写"
    # 的话，量的是覆写**之前**的字节，判据会对着已经被覆写的事实报 True——probe B
    # 实测抓到的就是这个形态：`两次相同 = True` 而 b-report.txt 的 sha 已经从
    # 83dc4396… 变成 055d69e3…。判据必须在缺陷在场时报红，否则它只是一句装饰。
    flush(text)
    if args.limit > 0:
        post = sha256_of(REPORT)
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· {rel(REPORT)}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}"
            f"（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    # RESULT 行放在最后、且在自检之后才算 ok：结论行必须反映**全部**判据，
    # 包括上面那条字节级自检。第二遍落盘把自检块与 RESULT 行一起写进去。
    text += f"\nRESULT: {'PASS' if ok else 'FAIL'}{suffix}\n"
    flush(text)
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
