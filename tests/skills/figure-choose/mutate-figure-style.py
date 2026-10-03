#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/figure-choose/check-figure-style.py` 的**变异驱动器**——一条命令复跑全部变异。

用法：  python tests/skills/figure-choose/mutate-figure-style.py

## 为什么必须落盘

本仓已栽过**六次**"判据在什么都没验的情况下报绿"。变异驱动器**入库**才能让复核员
独立复现"它真的会红"这句话；不落盘的变异等于自称。

## 每条变异做什么

1. 读检查器的**原始字节**（`rb`），在内存里做**一次**字面替换
   （替换次数必须恰为 1，否则驱动器自己报错）；
2. 用 `write_bytes` 把变异体写到 `fixtures/_mut/`（**改副本，原文件全程不碰**；
   全仓禁用 `write_text`——Windows 上会把 LF 写成 CRLF）；
3. 对**同一批 fixture**分别跑**原检查器**与**变异体**，逐条断言"该红的那条真的翻了"；
4. 跑完清空 `_mut/`，并用 **`git hash-object`** 自证检查器逐字节没变，最后复跑一遍
   逐格验收（`fixtures/run-expected.py`，exit 0）。

## 与任务书的差异（三处，均为实测逼出，逐条见输出里的 NOTE）

- **M4**：任务书写"改 0.005 → 0.0，断言 ok-02 仍绿、bad-f2 必红"——但**原 6 张 fixture 上
  这个变异一个读数都不变**（六张全等，NOTE 里逐张打印），那是个**证不了东西的变异**。
  故断言改锚在**新增的 ok-04.png**（4 主色 + 1 个 0.292% 的稀有彩色）上：地板一改，
  第 5 色被数出来 ⇒ 地板真的参与判定。
- **M5**：任务书说 `caption:2` 是 15 词、改 `CAP_MAX` 即由 FAIL 转 PASS。实测 `caption:2`
  是 **24 词**（`split()` 计数；F3b 现按正文口径数得 **22**），**超硬上限 17** ⇒ 只改
  `CAP_MAX` 时它**照样红**。
  故断言改锚在**新增的 `caption:5`（整条 15 / 正文 13 词）**上——只有它能把 `CAP_MAX` 单独证活。
- **M3**：任务书写"删掉 `sys.exit`"。实现里那条 fail-closed 走 `fail_closed()`（exit 2），
  故变异写成把 PNG 分支的守卫改成恒不成立（`if dpi is None:` → `if False:`），
  等价于删掉该守卫，且**只**动这一条路径。

## 复验补齐的三处（独立评审判定 M7/M8/P1，逐条见各行说明）

- **M7**（Important-1）：F2 的 **PDF 栅格化分支**是修完 PDF 崩溃后的新增分支，把它拆掉，
  PDF 立刻退回"`Image.open` 读 PDF"的老缺陷（rc=2、无判词）⇒ 该分支确实承重。
- **M8**（Important-3）：**F3a** 原先**没有任何"它能红"的证明**（`expected.tsv` 里 F3a 只有
  一条且是 PASS）⇒ 补一条谓词取反的变异 + 一条 `caption:6`（缺冒号）的 FAIL 行。
- **P1**（R-5）：`run-expected.py` 的 **ERROR 分支**（rc 异常/没打判词 ⇒ 记 ERROR、整轮非零退出）
  是新增分支 ⇒ 用一支"只在**期望 FAIL 的那一行** fail-closed"的变异体驱动它，证明
  **"没判成"不再被记成"判成红"**。

## 修复轮（独立评审 1 Critical + 3 Important + 4 Minor）新增的变异

- **M13–M19**：给修复轮**新写的每一个判据位**配回归位，逐条必须实测红。其中
  M13 打的是**已被证伪的 48.79**（Critical-1 的那句不实陈述在文档里的原位置）、
  M14 打的是连续色图闸门的箱数下限（Important-3 收紧的那条腿）、
  M17 打的是 H9 的宽口径条数 578（Important-4）、
  M18 打的是 `provenance.md` **散文**里的数（N-7）、
  M19 打的是 H12 的〔社区〕字号下限（N-8，原先改成 `≥6 pt` 一路全绿）。
- **C1 / C2 单独一组**：M9–M19 全走 `--only <id>`，而 `check-house-style.py` 的 **CENSUS 只在
  不带 `--only` 时才跑**（`if not want:`）⇒ 上面那些变异**一条都没验过 CENSUS**。这两条故意
  整份跑（`--no-provenance` 只为省掉 46 次子进程），断言的是 `CENSUS … 未入理由表 ≥1 个`：
  C1 往文档加一句带**整数**的话（原先整数被 `(r"\d+", …)` 兜底豁免，Important-2）、
  C2 把仪器实现常量 `quantize(32)` 改成 `quantize(99)`（证明上下文豁免表也不是万能兜底）。

## Task 4 新增的一组（`M22`–`M26` + 修复轮的 `M27`/`M28` + 读数条探针 `R1`）

这一组打的**不是** house-style / provenance，是 **`chart-types.md`**（图型决策树）的形状，
被验对象 = `check-house-style.py` 的**结构守卫** `S1`/`S2`/`S3`/`S5`。编号从 **`M22`** 起
（`M1`–`M8` 是检查器那一组、`M9`–`M19` 是规范数守卫那一组、`C1`/`C2` 是 CENSUS），
**不撞号**才引得住"哪条红了"。

- **`M22`**：入口 9 从『不确定性』**改名** ⇒ `S1` 红（八个名字对不上九个）。
  *只改标题不改块*，故 `S2` 不受影响 —— 这条专门把 `S1` **单独**证活。
- **`M23`**：删掉入口 1 的『**备选**』那一段 ⇒ `S2` 红（四段少一段），`S1` 不受影响。
- **`M24`**：删掉 **radar 定义行**上的『低频』⇒ `S3` 红。
  ⚠️ 任务书给的正则（**全文**扫 `radar` × `低频`）在本变异体上**仍然命中**（别的入口顺带提到
  radar 时也标了低频）⇒ 照任务书写法这条**不会红**。本实现把 `S3` 收紧成**只看 radar 的那条定义行**，
  逐条见该变异的 NOTE（NOTE 是**现算**的，不是抄进脚本的结论）。
- **`M25`**：把 3D 那条参照分布数 `9.2%` 改成 `9.3%` ⇒ `S5` 红（与 house-style 不同值）。
- **`M26`**：把两个小数**都**写成中文数字 ⇒ `S5` 抽不到任何小数 ⇒ 红（fail-closed：
  "把数全删光"不许成为转绿路径）。这条用**多替换**变体（`edits` 是列表）。
- **`R1`（读数条探针，不是判据变异）**：`S4` 只印计数、不进 `bad`（见检查器模块头第 5 条）。
  故它**没有"会红"可证**；这里证的是另一件事：**它真的在读数**（改坏副本上计数会动）
  **且从不改判词**（rc 恒 0、恒不出现 `PASS/FAIL  S4`）。一个"读数条"该有的两条性质都由一次运行钉住。
  （唯一例外见检查器模块头：`chart-types.md` **读不出**时它与其余结构守卫一起记红。）

## 修复轮（复审 N-2）新增的 `M27`/`M28`：`S5` 的归属口径

`S5` 原先只查"值 ∈ `house-style.md` ∪ `provenance.md` 的全局池"（123 个数，混着容差常量
`0.02/0.1/0.2` 与**别的 `H<n>` 条目**的数）——这是对任务书口径（"必须能在 `house-style.md` 找到同值"）
的**弱化**：往 3D 那条上写 `1.20`（H1 上限）或 `0.5`（H4 地板）照样绿。收紧为"**归到同行 `H<n>` 引用**
且 **∈ 该条目的数**"后，两条都要红（NOTE 里**现算**旧写法会怎么判）：

- **`M27`**：写进一个**池内但无所属**的数 `1.20`（H1 的上限）⇒ 新写法：该行没有 `H<n>` ⇒ 红。
- **`M28`**：把 `H7` 那条的数 `9.2` 换成 `0.5`（H4 的地板，池内）⇒ 新写法：`0.5 ∉ H7` ⇒ 红。

## Task 5 新增的一组（`M29`–`M41`）：`SKILL.md` 的短契约守卫 `K1`–`K8`

被验对象 = `check-house-style.py` 的 `SKILL_GUARDS`，文档 = `SKILL.md`（**短契约**）。
任务书给的 `M14`/`M15`/`M16` 与已占用的编号**撞号**，故顺延 **`M29`** 起（同 Task 3 那次顺延）。

- **`M29`**：写进一条规范数值（`0.951`）⇒ `K3`（现取禁止串）与 `K5`（数字的处置）**都**红。
  两条是**两道不同的闸**：`K3` 只认"规范里确实有的数"，`K5` 与禁止串表无关 —— 见该条的 NOTE。
- **`M30`**：**删掉指针行**、别处只留裸文件名 ⇒ `K2` 红。
  ⚠️ 任务书给的 `K2` 是 `"references/house-style.md" in txt or "house-style.md" in txt` ——
  `SKILL.md` 通篇要提规范，裸文件名**必然**还在 ⇒ **照任务书写法这条不会红**。本实现要求
  **skill 目录内的相对路径**（Task 7 的检查器要核的那个形态），逐条见该条 NOTE。
  ★ **Task 3b 修 ②**：这个"别处只留裸文件名"必须**对所有出现处**做（本变异用 `sub_all`）。
  原变异只动 L10、指针行只删 L79 ⇒ Task 2 添在 L83 的那处完整路径仍在 ⇒ `K2` 仍绿、M30 RED-BAD。
  该路径今天在 `SKILL.md` 里出现**三处**（L10 · L79 指针行 · L83），故"删指针行"这个手法
  **必须**配合"全文降成裸文件名"，否则它证的就不是它自称的那件事。
- **`M31`**：把文件撑到 151 行 ⇒ `K1` 红（短契约上限 `<150`）。
- **`M32`**：入口名『不确定性』改名 ⇒ `K4` 红（`ENTRIES` 是契约、缺一即红）。
- **`M33`**：把点名绘图 skill 的那行的 **〔拟建〕** 去掉 ⇒ `K6` 红（点名不存在的 skill 即错；
  `K6` 同时是 fail-closed：一个绘图 skill 都不点名也红 —— "不点名"不许成为转绿路径）。
  ★ 目标**不写死名字**：从被改文本**现取**"当前仍标〔拟建〕"的那一个（`marked_plot_skills`，
  今天取到 `mcm-plot-origin`）。沿革：`mcm-plot-python`（M3-plot Task 2 落地）→
  `mcm-plot-matlab`（M3-matlab Task 1 落地时**写死**，一落地即失去锚点）→ **现取**。
  ⚠️ 取不到（= 一个仍〔拟建〕的都没有）⇒ 本变异**失去对象**、抛错（fail-closed）。
- **`M34`**：打的是 **`house-style.md` 的副本**（`--doc` 指它）：把小数字面量与 `≤n` 形态全抹掉
  ⇒ `K3` 的"现取禁止串"**抽到空集** ⇒ 必须红（fail-closed）。不证这一臂，
  "抽不到即 FAIL"就只是注释里的一句话 —— 仪器取不到参照物却默认放行，正是本仓栽过的那一类。

### 修复轮（复审 1 Important + 6 Minor）新增的 `M35`–`M41`

- **`M35`**：`主色四色以内` 插进副本 ⇒ `K3` **中文数词臂**红（Important-1：主臂 `\d+(?:\.\d+)?`
  只认 ASCII/全角数字，**这四种中文写法原先整句走绿**；这条与 `M36` 各证一条臂）。
- **`M36`**：`图宽不超过一倍正文宽` 插进副本 ⇒ `K3` 红，**且由 NOTE 现算证明是"单位词臂"单独在红**
  （`一` < `SK_CN_BARE_MIN`=4 ⇒ 裸值臂不覆盖它）。
- **`M37`**：把 `4`（H4 的规范值）写进**声明行** ⇒ `K5` 红（N-2：旧写法下"声明行上的数自证"，
  写进那一行即被判"已声明"）。
- **`M38`**：删掉「输出契约」整段 ⇒ `K7` 红（N-3：这一段原先**没有任何机械存在性守卫**；
  NOTE 现算 `K1`–`K6` 在该副本上仍全绿）。
- **`M39`**：往决策树表里多加一行（= 多一个入口名）⇒ `K4` + `K5` 红（N-4：旧写法只查"九个名字
  出现过"，加一行不会红）。
- **`M40`**：`--skills-root` 指向一个**临时根**，把 `SKILL.md` 点到的**每一个**绘图 skill 都
  在那里建出目录 ⇒ 仍标〔拟建〕的那一个（今天 = `mcm-plot-origin`）变成"**标了却存在**" ⇒ `K6` 红
  （N-5：标了〔拟建〕的 skill 真的存在时，守卫必须红）。
  ★ **隔离性质**：其余名字（存在且未标）在临时根里一致 ⇒ 本变异**只**打在"标了却存在"这一个方向上。
  ★ **非侵入自证** = **真根路径集合跑前/跑后逐字比对**（`_skills_tree`）——**不**再用"真根里反正没有
  某个 skill"当代理（那种代理在该 skill 真建出来那天**恒假**，先例见 `_skills_tree` 的 docstring）。
  ★ 目标**不写死名字**（同 `M33`）：`mcm-plot-python` → `mcm-plot-matlab` → **现取**。
- **`M41`**：抹掉 `house-style.md` **副本**里 `H4` 的 `**验证**：` 行 ⇒ `K8` 红（N-7：
  `SKILL.md` 断言"逐条标了验证状态"，原先无人守）。

## Task 6 涟漪新增的一条（`M42`）

- **`M42`**：`check-figure-style.py` 的 **F3b 词数口径**由**正文**（去 `Figure N:` 标签）
  换回**整条** ⇒ 新增的口径锚 `caption:7`（整条 13 / 正文 11）由 PASS 转 FAIL。
  这是 Task 6 GREEN 对照 **Important-2** 的回归位：那一轮把 F3b 收敛到规范侧
  （`len(caption_body(cap).split())`，常量 12/17 与 `G-H9-*` 一个没动）。
  同批其余图注两口径同判 ⇒ 证不了口径，故**新增** fixture 与 expected 行，理由见 `m42` 的 docstring。

## Task 7 新增的一组（`M43`–`M46`）：引用完整性检查器的"防恒真"证明

被验对象**不是** `check-figure-style.py`，也不是 `house-style.md`，是新增的
`tests/skills/figure-choose/check-spec-pointers.py`（`.claude/skills/*/SKILL.md` 的引用纪律：
绘图家族的 skill 必须指向 `house-style.md`、且不许重述规范数值）。编号从 **`M43`** 起
（任务书给的 `M17`–`M20` 与已占号**撞号**，故顺延 —— 同 Task 3 顺延 `M9`、Task 5 顺延 `M29` 两次）。

**这一组为什么非有不可**：真仓**此刻** 0 个绘图家族 skill（`mcm-plot-*` / `mcm-table` /
`mcm-schematic` 这几族还没建出来）⇒ 只跑真仓，检查器的逐份判据**一次都不执行**，
"它会红"就是一句自称。故四条全靠 `--skills-dir` 指到 `fixtures/fake-skills/` 的假 skill 上做
（那些 fixture 就是为这件事存在的）。

- **`M43`**：整体跑假 skill 目录 ⇒ `mcm-plot-nopointer`（缺指针）由 **`K2`** 点名、
  `mcm-plot-restate`（重述 `1.20`/`0.951`）由 **`K3`** 点名，且互不打偏
  （断言写成"**各打各的**"，不是"反正红了"—— 否则随便哪一份坏就够红两次，另一条拆掉也看不出来）。
  家族正则 `FAMILY_RE` 还有**两条非 `mcm-plot-*` 的备选**（`mcm-table` / `mcm-schematic`），
  故 `M43` 另断两份**在射程内且缺指针**的同名 fixture 各自由 `K2` 点名 —— 否则把那两条备选
  从正则里删掉也不会红（"声明了但没被任何变异证明"的判据腿，复审 Minor-3）。
- **`M44`**：只留 `mcm-plot-ok` 再跑 ⇒ **绿**。这是**本组唯一**能证"检查器不是恒 FAIL"的一条；
  没有它，`M43` 的"红"什么都证明不了。
- **`M45`**：把 `check-house-style.py`（`K2`/`K3` 的实现处）**副本**里 `_k3` 主臂的
  **三族参照物全改坏**（小数正则 + `SK_CN_TIER_RES` 整条 ⇒ 两族值池一起抽到空集）
  ⇒ **仪器探针** `FAIL  INSTR K3@空串` ⇒ fail-closed 红。
  故意打**真仓**：那里 0 个家族、逐份判据根本不执行，唯一能红的就是全局探针 ——
  这才证得到"仪器取不到参照物时，哪怕无对象也红"（本仓栽过六次的那一类：仪器抽空却默认放行）。
- **`M46`**：`--skills-dir` 指向坏目录 ⇒ 非零退出，**两个分支都证**：
  分支 a 目录**不存在**、分支 b 目录在但**一个 `*/SKILL.md` 都没有**。两分支都不许打出 `RESULT: PASS`。

## M3 绘图实现层新增的一组（`M47`–`M53`）：`K3` 主臂的 **ASCII 阈值标记**

被验对象 = `check-house-style.py` 的 `_k3` **主臂**（文档 = `SKILL.md` 的副本）。
编号从 **`M47`** 起：任务书给的 `M17`–`M20` 与已占号**撞号**（同 Task 3 顺延 `M9`、
Task 5 顺延 `M29`、Task 7 顺延 `M43` 三次），故继续顺延。

**为什么非有不可**：主臂原先只认 `\d+\.\d+` 与 `≤n` / `<n 词`，而 `H12` 的规范值**恰恰**写的就是
**`≥7 pt`** ⇒ `≥n` / `上限 n` / `不超过 n` 这一整族重述**全走绿**（实测四条 `≥7 pt` / `上限 4` /
`不超过 12 词` / `主色 4 个` 都 PASS）。对齐标记表后：**六个标记各有一条真红**
（`M47`–`M49` + `M51`–`M53`），外加一条**边界对照组** `M50`（三种"不该红"的写法必须**仍绿**）。

- **`M47`**：写进『`≥7 pt`』（规范 `H12` 的原话）⇒ `K3` 红（`≥` 这一族原先整族走绿）。
- **`M48`**：写进『`上限 4`』⇒ `K3` 红。注意规范里写的是 `≤4`，**没有** `上限 4` 这个字面 ——
  它红在"**同方向的标记可互换**"上（`≤4` 与 `上限 4` 是同一个阈值的重述）。
- **`M49`**：写进『`不超过 12 词`』⇒ `K3` 红（`不超过 n` 这一族进射程；值池按方向共享）。
- **`M51`**：写进『`字号下限 7 pt`』⇒ `K3` 红（`下限 n` 这一族；值 `7` 现取自规范里的 `≥7`）。
- **`M52`**：写进『`图注 < 12 词`』⇒ `K3` 红（`<n 词` 这一族；值 `12` 现取自 `上限 12 词`）。
- **`M53`**：写进『`图注 ≤12 词`』⇒ `K3` 红（`≤n` 这一族**本尊**；值 `12` 现取自 `上限 12 词`）。
  为什么 `M51`/`M52`/`M53` 也要各来一条：只证 `≥`/`上限`/`不超过` 的话，"六个标记都在射程内"就是
  **声明比事实大**（本仓明令：声明了覆盖就必须有一次真的红；同 Task 7 复审 Minor-3 那条腿）。
  `M53` 是修复轮补的（复审 Important-1）：它取 `≤12` 而**不是**规范原话 `≤4` —— `≤4` 旧臂逐字也能抓，
  证不到"值池化后**新增**的射程"；`≤12` 只有新臂才红（旧臂只认与规范逐字相同的 `≤4`/`≤3`）。
- **`M50`**：**边界对照组**（必须**仍绿**，同 `M44` 那种反证条），三例：
  ① 『`主色 4 个`』（**无标记裸整数**）—— 要判它就得退化成"文档里出现 `4` 就红"，而规范里的
  `0/2/3/4/7/12/17/20/100` 会在任何普通句子里误红；
  ② 『`下限 4`』（值在**另一个方向**的池里）—— **跨方向不算重述**，这条正是 `mcm-abstract` 的
  `≥12pt` 不被假红的依据；
  ③ 『`< 25 词`』（值不在任何池里）。谁把臂写成"见数就红"，三例里至少一条立刻 RED-BAD。

★ **假 skill 的目录名带家族前缀**（`mcm-plot-ok` / `mcm-plot-nopointer` / `mcm-plot-restate`）：
任务书给的目录名是 `fake-ok` / `fake-nopointer` / `fake-restate`，但规则①②的**射程**是
"名字匹配绘图家族"（增量任务书差异 2/5）⇒ 叫 `fake-*` 的样本**根本不在射程内**（会整目录判绿），
那样 `M43` 不红、`M44` 也证不到"家族 ≥1 且全绿"这条路径。三条**角色**照原样，只加家族前缀。

## M3 跨载体样式单源新增的一组（`M54`–`M58`）：共享判据三条 `F4`/`F5`/`F6`

三条新判据各配一条"判据失效即红"的变异，外加 `F5` 的**射程边界对照**（同 `M50` 的角色），
以及（Task 3b 修 ③）`F6` 的**内嵌事实**那一条承重件：

- **`M54`**：F4 的**外缘环**那一路**退回全图众数**（= 把 F4 从"外缘环 ∧ 近灰众数"的合取新口径，
  退回 **I-1 的病根口径**"全图出现最多的颜色"）⇒ 支点 ★新 `fixtures/ok-06.png` 由
  `F4` PASS 转 FAIL（众数 = 那片 `#0072B2`、亮度 87 < 136）。
  ★ 它承 `F4` 的**"必须仍绿"边界对照**（硬纪律 11），但**对照必须跑在变体上**（同 `M50`/`M57`）
    —— 旧写法拿 `ok-04.png` 在**未变异件**上断言"必须仍绿"，而 `ok-04` 的全图众数是 H14 色带
    （亮度 ≥ 136）⇒ 退回全图众数它照样 PASS ⇒ **恒真、什么都没证**（终审 **Important-1**：
    I-1 与 I-4 同轮互噬）。`ok-04` 现已**降级为"仅记录、不作断言"**。
  ★ `BG_MIN_LUMA` **仍承重**：主变异之外附**第二支自建变体**（`136 → 0`）单证 —— `bad-bg-dark.png`
    由 FAIL 转 PASS。覆盖率不因主变异换向而减少。
- **`M55`**：`F5` 的**允许色序清空**（H14 → 仅 `#000000`）⇒ 合法 H14 子集样本
  `good-color-order.png` 由 PASS 转 FAIL（允许集合真参与判定）。
- **`M56`**：`F6` 的**可接受字体族清空**（`FONT_FAMILY_OK → ("__none__",)`）⇒ 真实产物
  `plot-python/green/out-G1/figure.pdf`（内嵌 `TeXGyreTermesX-Regular`）由 PASS 转 FAIL。
- **`M57`**：**射程边界对照**（**必须仍绿**，同 `M50`）：把允许集合收窄成 H14 的**前三色子集** ⇒
  正好用那三色的 `good-color-order.png` **仍 PASS**。它钉死"`F5` 不是恒红"且"不要求凑满八色"；
  同副本上非 H14 的 `bad-color-order.png` 仍红 ⇒ 收窄没扩到乱红。
- **`M58`**：`F6` 的**内嵌事实拆掉**（`font_embedded()` 恒 `True` = 退回"有字体名即算内嵌"）⇒
  只引用、未内嵌的 `font-not-embedded.pdf`（base14 `Helvetica`）由 `N/A` 转 `FAIL`。
  它钉的是 Task 3b 修 ③ 那件事：**"报得出名字"不等于"内嵌"**（Origin 的 34/34 导出件即 `/FontFile*` = 0）。

⚠️ **涟漪**（含 2026-10-01 I-4 的后续）：`F5` 落地时对既有 `ok-*` fixture（当时用 Tol-bright 色、
非 H14）为红 ⇒ `M7` 的前置曾放宽为 `rc0 in (0, 1)`。**I-4 把 `ok-*` 重上色成 H14** 后它们全部全绿
⇒ `M7` 的前置**收紧回 `rc0 == 0`**，且 `ok-*` 的 `F5 = PASS` 另有 `expected.tsv` 逐格守着。
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sanitize(s):
    """证据里不写绝对路径：把本目录的绝对前缀剥掉。"""
    return s.replace(str(HERE) + os.sep, "").replace(str(HERE), "")


CHK = HERE / "check-figure-style.py"
FIX = HERE / "fixtures"
MUTD = FIX / "_mut"
CAPS = {n: t.strip() for n, t in
        (l.split("\t", 1) for l in (FIX / "captions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())}
IMG_CAP = "Figure 1: A test figure caption"     # 无尾句号：图样本的判词只反映它自己要测的东西（R-7）
PDF_OK = "ok-05.pdf"                            # 4 色 PDF（F1/F2 全 PASS）
PDF_BAD = "bad-f2-five-colors.pdf"              # 6 色 PDF（F2 必红）
EXIT_FAIL_CLOSED = 2


# ---------------------------------------------------------------- 跑与读
def run_checker(checker, fig, caption, dpi="200"):
    cmd = [sys.executable, str(checker), "--fig", str(fig), "--caption", caption, "--textwidth-in", "6.31"]
    if dpi is not None:
        cmd += ["--dpi", dpi]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verdict(out, crit):
    if f"PASS  {crit} " in out:
        return "PASS"
    if f"FAIL  {crit} " in out:
        return "FAIL"
    return "-"


def reader(checker):
    """返回 (图样本读数, 图注样本读数) 两个闭包，都绑定到同一个检查器。"""
    fig_v = lambda name, crit: verdict(run_checker(checker, FIX / name, IMG_CAP)[1], crit)
    cap_v = lambda n, crit: verdict(run_checker(checker, FIX / "ok-01.png", CAPS[n])[1], crit)
    return fig_v, cap_v


# ---------------------------------------------------------------- 断言
def m1(before, after, mp):
    """F1_HI 1.20 → 0.90：阈值真参与判定 ⇒ ok-01（0.951）也得红，ok-02（0.808）不受影响。"""
    b1, b2 = before[0]("ok-01.png", "F1"), before[0]("ok-02.png", "F1")
    a1, a2 = after[0]("ok-01.png", "F1"), after[0]("ok-02.png", "F1")
    return (b1 == "PASS" and a1 == "FAIL" and a2 == b2 == "PASS",
            f"ok-01 F1 {b1}→{a1}（比值 0.951 > 0.90）；ok-02 F1 {b2}→{a2}（0.808 ≤ 0.90，不受影响）")


def m2(before, after, mp):
    """F1_LO > F1_HI：区间判据不是恒真（原本全绿的三张合格图全红）。

    前置断言（R-6）：先要求三张合格图**变异前就是绿的**——否则"之后全 FAIL"这条断言
    在"它们本来就是红的"时也会通过，等于什么都没证。
    """
    rows = []
    for name in ("ok-01.png", "ok-02.png", "ok-03.png", "bad-f1-too-narrow.png", "bad-f1-too-wide.png"):
        b, a = before[0](name, "F1"), after[0](name, "F1")
        rows.append((name, b, a))
    ok = (all(a == "FAIL" for _n, _b, a in rows)
          and all(b == "FAIL" for n, b, _a in rows if n.startswith("bad-"))
          and all(b == "PASS" for n, b, _a in rows if n.startswith("ok-")))    # ← 前置：三张本就得是绿的
    return ok, "；".join(f"{n} {b}→{a}" for n, b, a in rows)


def m3(before, after, mp):
    """PNG 无 --dpi：必须**不判**（rc=2、无判词）；变异体把守卫换成"默认 200 硬着头皮判"。

    读法：变异体**印出了判词**（rc=1）⇒ 它不再拒绝判——这正是"拿不到参照就别判"这条
    契约被拆掉的证据。（若把守卫写成 `if False:`，变异体会被 D5 新加的通用兜底接住、
    仍退 2，只是报错变成 TypeError——那样这条变异就证不了"守卫承重"，故不取。）
    """
    rc0, out0, err0 = run_checker(CHK, FIX / "ok-01.png", IMG_CAP, dpi=None)
    rc1, out1, err1 = run_checker(mp, FIX / "ok-01.png", IMG_CAP, dpi=None)
    clean0 = rc0 == EXIT_FAIL_CLOSED and "RESULT:" not in out0 and "需要显式 --dpi" in err0
    clean1 = rc1 == EXIT_FAIL_CLOSED and "RESULT:" not in out1
    return (clean0 and not clean1,
            f"原检查器 exit={rc0} 拒绝判（'RESULT:' 未打印；stderr '{sanitize(err0).strip()[:40]}'）；"
            f"变异体 exit={rc1} 印出判词（'{out1.strip().splitlines()[-1][:40]}'）⇒ 守卫被拆掉")


def m4(before, after, mp):
    """噪声地板 0.005 → 0.0：ok-04 的稀有彩（0.292%）由"不算"变"算" ⇒ 地板真参与判定。"""
    b4, a4 = before[0]("ok-04.png", "F2"), after[0]("ok-04.png", "F2")
    b2, a2 = before[0]("ok-02.png", "F2"), after[0]("ok-02.png", "F2")
    bf, af = before[0]("bad-f2-five-colors.png", "F2"), after[0]("bad-f2-five-colors.png", "F2")
    same = "；".join(f"{n} {before[0](n,'F2')}→{after[0](n,'F2')}"
                    for n in ("ok-01.png", "ok-02.png", "ok-03.png", "bad-f1-too-narrow.png",
                              "bad-f1-too-wide.png", "bad-f2-five-colors.png"))
    return (b4 == "PASS" and a4 == "FAIL" and a2 == "PASS" and af == "FAIL",
            f"ok-04 F2 {b4}→{a4}（4 主色 + 0.292% 稀有彩：读数 4 → 5）；ok-02 F2 {b2}→{a2}；"
            f"bad-f2 F2 {bf}→{af}　NOTE/原 6 张 fixture 上此变异读数全等：{same}")


def m5(before, after, mp):
    """CAP_MAX 12 → 99：正文 13 词的 caption:5 由 FAIL 转 PASS ⇒ 词数上限真参与判定。

    注意 caption:2（正文 22 词）**不会**翻绿——它超硬上限 17，被 CAP_HARD 那条兜住（见输出 NOTE）。
    """
    b5, a5 = before[1]("5", "F3b"), after[1]("5", "F3b")
    b2, a2 = before[1]("2", "F3b"), after[1]("2", "F3b")
    return (b5 == "FAIL" and a5 == "PASS",
            f"caption:5（整条 15 / 正文 13 词）F3b {b5}→{a5}；"
            f"NOTE/caption:2（整条 24 / 正文 22 词）F3b {b2}→{a2}"
            f"（超正文硬上限 17，CAP_MAX 抬高也翻不了）")


def m6(before, after, mp):
    """F3c 取反：方向确实被检（合格图注转红、endswith('.') 的 caption:3 转绿）。"""
    b1, a1 = before[1]("1", "F3c"), after[1]("1", "F3c")
    b3, a3 = before[1]("3", "F3c"), after[1]("3", "F3c")
    return (b1 == "PASS" and a1 == "FAIL" and b3 == "FAIL" and a3 == "PASS",
            f"caption:1 F3c {b1}→{a1}（合格图注转红）；caption:3 F3c {b3}→{a3}（句末句号转绿）")


def m7(before, after, mp):
    """F2 的 PDF 栅格化分支（Important-1）：拆掉它 ⇒ PDF 退回"Image.open 读 PDF"的老缺陷。

    读法：原检查器对 ok-05.pdf 给出 F2 **判词**（PASS）；变异体**给不出任何判词**——
    rc=2、stdout 空。这不是"判成红"，是"根本没判成"，正是 F2 的 PDF 分支承重的证据。
    （PDF 上 F2 **真会红**另有入库样本兜着：`bad-f2-five-colors.pdf F2 FAIL`，见 expected.tsv。）

    ⚠️ 前置曾是 `rc0 in (0, 1)`（M3 Task 3 涟漪：ok-05.pdf 当时用 Tol-bright 色、**不是** H14 ⇒
    F5 对它红 ⇒ 原检查器整体 rc=1）。**2026-10-01（I-4）ok-05.pdf 已重上色为 H14** ⇒ 它现在
    **全绿**（rc=0）⇒ 前置收紧回 `rc0 == 0`（比原来更严；这条变异证的是"F2 分支承重"，
    现在可以连同"整份也全绿"一起要求）。
    """
    rc0, out0, _ = run_checker(CHK, FIX / PDF_OK, IMG_CAP)
    rc1, out1, err1 = run_checker(mp, FIX / PDF_OK, IMG_CAP)
    png_b, png_a = before[0]("ok-01.png", "F2"), after[0]("ok-01.png", "F2")
    ok = (rc0 == 0 and "RESULT:" in out0 and verdict(out0, "F2") == "PASS"
          and rc1 == EXIT_FAIL_CLOSED and "RESULT:" not in out1 and verdict(out1, "F2") == "-"
          and png_a == png_b == "PASS")
    return ok, (f"ok-05.pdf F2 原检查器 exit={rc0} 判词 {verdict(out0, 'F2')}；"
                f"变异体 exit={rc1} 无判词（stderr '{sanitize(err1).strip()[:44]}'）⇒ 该分支承重；"
                f"PNG 侧 ok-01 F2 {png_b}→{png_a}（不受影响）")


def m8(before, after, mp):
    """F3a 谓词取反（Important-3）：方向确实被检（合格前缀转红、缺冒号的 caption:6 转绿）。"""
    b1, a1 = before[1]("1", "F3a"), after[1]("1", "F3a")
    b6, a6 = before[1]("6", "F3a"), after[1]("6", "F3a")
    return (b1 == "PASS" and a1 == "FAIL" and b6 == "FAIL" and a6 == "PASS",
            f"caption:1 F3a {b1}→{a1}（合格前缀转红）；caption:6 F3a {b6}→{a6}"
            f"（'Figure 6 Model structure' 缺冒号，转绿）")


def m42(before, after, mp):
    """F3b 的词数口径（Task 6 的 Important-2）：换回"整条图注"口径 ⇒ caption:7 由 PASS 转 FAIL。

    背景：F3b 原先数整条图注（含 `Figure N:` 这 2 个词），而规范 H9 与它的复跑仪器
    `house-metrics.py` 的 `cap_words_*` 数的是**去掉标签后的正文**（P-D-c1）——两口径相差 2 词。
    本轮把 F3b 收敛到规范侧（`len(body.split())`），这条变异就是它的回归位。

    为什么必须**新增** fixture：同批其余图注两口径**同判**（caption:1 整条 8 / 正文 6、
    caption:5 整条 15 / 正文 13、caption:2 整条 24 / 正文 22 —— 都同红绿），
    拿它们证不了"F3b 数的到底是哪一段"。故新增 `caption:7`（整条 **13** / 正文 **11**），
    恰好卡在 `CAP_MAX=12` 的分界上：正文口径 PASS、整条口径 FAIL。
    它同时钉进 `expected.tsv` 的 `caption:7  F3b  PASS` ⇒ 口径若被改回去，逐格验收也 MISMATCH。
    """
    b7, a7 = before[1]("7", "F3b"), after[1]("7", "F3b")
    b5, a5 = before[1]("5", "F3b"), after[1]("5", "F3b")
    return (b7 == "PASS" and a7 == "FAIL" and a5 == b5 == "FAIL",
            f"caption:7（整条 13 词 / 正文 11 词）F3b {b7}→{a7}（口径换回整条 ⇒ 越线 1 词）；"
            f"NOTE/caption:5（整条 15 / 正文 13）F3b {b5}→{a5}"
            f"（两口径同判红 ⇒ 它证不了口径，故口径锚另立 caption:7）")


# ---------------------------------------------------------------- M3 Task 3（F4/F5/F6）
def f4_line(checker, fig):
    """取某检查器对某图打出的 **F4 那一行原文**（判词行，含两路读数）。

    为什么要整行而不是 `verdict()`：F4 现在有**两路读数**（外缘环 / 近灰众数），
    汇总判词只有 PASS/FAIL；把整行读出来，"它为什么翻"才在证据里一眼可见（任务书 §2.3）。
    """
    out = run_checker(checker, fig, IMG_CAP)[1]
    return next((l.strip() for l in out.splitlines() if l.startswith(("PASS  F4", "FAIL  F4"))), "(无 F4 判词)")


def _m54_threshold_probe():
    """`M54` 的**第二支**变体：`BG_MIN_LUMA` 136 → 0 ⇒ 深色底样本由 FAIL 转 PASS（阈值常量仍承重）。

    为什么要有第二支：任务书 §2 把 M54 的**主变异**定成「外缘环那一路退回全图众数」（好让
    `ok-06` 支点咬得住），而旧 M54 承的"`BG_MIN_LUMA` 真参与判定"这件事**不许在重做时丢掉**
    （覆盖率只许增、不许减）。故主变异之外，这里再自建一支阈值变体，单证阈值常量。
    副本写在 `fixtures/_mut/`（驱动器收工会清空），并在 `finally` 里当场删掉。
    """
    src = CHK.read_bytes().decode("utf-8")
    old = "BG_MIN_LUMA = 136"
    if src.count(old) != 1:
        raise AssertionError(f"`{old}` 命中 {src.count(old)} 次（必须恰 1）—— 检查器漂了，这条要跟着改")
    mp = MUTD / "check-figure-style.M54thr.py"
    try:
        mp.write_bytes(src.replace(old, "BG_MIN_LUMA = 0", 1).encode("utf-8"))   # write_bytes
        b = verdict(run_checker(CHK, FIX / "bad-bg-dark.png", IMG_CAP)[1], "F4")
        a = verdict(run_checker(mp, FIX / "bad-bg-dark.png", IMG_CAP)[1], "F4")
    finally:
        mp.unlink(missing_ok=True)
    return b, a


def m54(before, after, mp):
    """F4 的**外缘环**那一路承重，且它的「必须仍绿」边界对照**真的咬得住**（终审 Important-1 的修正）。

    本变异把 `outer_ring_mode(im4)`（外缘环众数）**退回全图众数** —— 即把 F4 从"合取新口径"
    退回 **I-1 之前那个病根口径**（"全图出现最多的颜色"）。两件事同时被钉住：

    ★ **边界对照在**变体**上跑**（同 `M50`/`M57` 的角色）：支点 = ★新 `fixtures/ok-06.png`
      （白底 + 一大片 `#0072B2` 占 ~69% + 四周白边 ⇒ **新口径**下外缘环 = 纯白 255、近灰众数 255
      ⇒ **PASS**）。退回全图众数时，众数 = 那片蓝 `#0072B2`（**亮度 87 < 136**）⇒ **PASS 转 FAIL**。
      ⚠️ **为什么换掉 `ok-04`**：`ok-04` 的全图众数是某个 H14 色带（**亮度 ≥ 136**）⇒ 退回全图众数
      它**照样 PASS** —— 那条对照**恒真**、什么都没证（终审 **Important-1**：I-1 与 I-4 同轮互噬）。
    ★ **两个读数**都打进断言（任务书 §2.3）：下面 detail 里逐字打印新旧两支检查器对 `ok-06` 的
      **F4 整行**（外缘环 + 近灰众数两路读数），"为什么它会翻"写在证据里。
    ★ **`ok-04` 降级为"仅记录、不作断言"**（任务书 §2.4）：它在**新旧两口径下都 PASS**，
      与 `ok-06` 的区别正是"内容色亮度过不过线" ⇒ 不作断言，但打印出来供对账。
    ★ **`BG_MIN_LUMA` 仍承重**：由第二支变体（`_m54_threshold_probe`）单证 —— `bad-bg-dark.png`
      由 FAIL 转 PASS ⇒ 阈值常量真参与判定（覆盖率不因主变异换向而减少）。
    """
    o6_b, o6_a = before[0]("ok-06.png", "F4"), after[0]("ok-06.png", "F4")
    o6_line_b, o6_line_a = f4_line(CHK, FIX / "ok-06.png"), f4_line(mp, FIX / "ok-06.png")
    ok_b, ok_a = before[0]("ok-01.png", "F4"), after[0]("ok-01.png", "F4")
    ctl_b, ctl_a = before[0]("ok-04.png", "F4"), after[0]("ok-04.png", "F4")     # 仅记录
    thr_b, thr_a = _m54_threshold_probe()
    ok = (o6_b == "PASS" and o6_a == "FAIL" and ok_a == ok_b == "PASS"
          and thr_b == "FAIL" and thr_a == "PASS")
    return ok, (
        f"**边界对照（跑在变体上）** ok-06.png F4 {o6_b}→{o6_a}：原『{o6_line_b}』 → 变异『{o6_line_a}』"
        f"（全图众数 = 那片 `#0072B2` 亮度 87 < 136 ⇒ 前提为真、咬得住）；"
        f"ok-01.png F4 {ok_b}→{ok_a}（白底，不受影响）；"
        f"**仅记录·不作断言** ok-04.png F4 {ctl_b}→{ctl_a}（它新旧两口径都 PASS ⇒ 拿它当对照是恒真，"
        f"终审 Important-1）；"
        f"**阈值常量仍承重（第二支变体 BG_MIN_LUMA 136→0）** bad-bg-dark.png F4 {thr_b}→{thr_a}")


def m55(before, after, mp):
    """F5 允许色序清空（H14 → 仅 #000000）：合法 H14 子集样本 good-color-order.png 由 PASS 转 FAIL ⇒ 允许集合真参与判定。"""
    g_b, g_a = before[0]("good-color-order.png", "F5"), after[0]("good-color-order.png", "F5")
    b_b, b_a = before[0]("bad-color-order.png", "F5"), after[0]("bad-color-order.png", "F5")
    return (g_b == "PASS" and g_a == "FAIL" and b_a == b_b == "FAIL",
            f"good-color-order.png F5 {g_b}→{g_a}（H14 前三色 ⊆ 允许集合；清空后全部越界）；"
            f"bad-color-order.png F5 {b_b}→{b_a}（本来就越界，不受影响）")


def m56(before, after, mp):
    """F6 可接受字体族清空（→ ("__none__",)）：入库 OTF 的 green PDF 由 PASS 转 FAIL ⇒ 族表真参与判定。

    打的是**真实产物** `plot-python/green/out-G1/figure.pdf`（内嵌 `TeXGyreTermesX-Regular`），
    不是 fixture —— 仓里没有别的"内嵌合法族"的 PDF 可打。PNG 侧 F6 走"不适用"支、不受影响。
    """
    fig = HERE.parent / "plot-python/green/out-G1/figure.pdf"
    b = verdict(run_checker(CHK, fig, IMG_CAP)[1], "F6")
    a = verdict(run_checker(mp, fig, IMG_CAP)[1], "F6")
    png = verdict(run_checker(mp, FIX / "ok-01.png", IMG_CAP)[1], "F6")
    return (b == "PASS" and a == "FAIL" and png == "PASS",
            f"out-G1/figure.pdf F6 {b}→{a}（内嵌 TeXGyreTermesX 被族表清空 ⇒ 越界）；"
            f"PNG 侧 ok-01 F6 = {png}（PNG 载体标『不适用』= PASS，不受影响）")


def m57(before, after, mp):
    """F5 射程边界对照（**必须仍绿**，同 `M50` 的角色）：允许集合收窄成 H14 的**前三色子集** ⇒ 正好用那三色的样本**仍 PASS**。

    它钉死两件事：① F5 **不是恒红**（谁哪天把 F5 写成"见彩色就红"，这条立刻 RED-BAD）；
    ② F5 **不要求凑满八色** —— 合法色序的子集（前三色）收窄后仍绿。非 H14 的样本同时仍红 ⇒ 收窄没扩到乱红。
    """
    g = verdict(run_checker(mp, FIX / "good-color-order.png", IMG_CAP)[1], "F5")
    b = verdict(run_checker(mp, FIX / "bad-color-order.png", IMG_CAP)[1], "F5")
    return (g == "PASS" and b == "FAIL",
            f"允许集合 = H14 前三色时：good-color-order.png F5 = {g}（该样本正是那三色 ⇒ 收窄后**仍绿**）；"
            f"bad-color-order.png F5 = {b}（非 H14 仍红）")


def f6_line(checker, fig):
    """取某检查器对某图打出的 **F6 那一行原文**（判词行，含详情串）。

    为什么要整行而不是 `verdict()`：`N/A` 与"判过且族对"在**汇总判词上都是 `PASS`**
    （第三态只写在详情串里，见 `check-figure-style.py` 的 F6）⇒ 只读 PASS/FAIL 会把
    "没判成" 读成 "判成了且对的"，正是本仓第一号病灶。
    """
    out = run_checker(checker, fig, IMG_CAP, dpi=None)[1]
    return next((l.strip() for l in out.splitlines() if l.startswith(("PASS  F6", "FAIL  F6"))), "(无 F6 判词)")


def m58(before, after, mp):
    """F6 的**内嵌事实**（`/FontFile*`）是判据的承重件：把它拆掉（退回"有字体名即算内嵌"）⇒
    只引用、未内嵌的样本 `font-not-embedded.pdf` 由 `N/A` 转 `FAIL`（`Helvetica` 不在族表里）。

    ★ 这条钉的正是 **Task 3b 修 ③** 那件事：旧口径下"`get_page_fonts` 报了名字"就算内嵌
    ⇒ 该样本会被**判族**（而不是如实标"未内嵌 ⇒ 不适用"）。断言要**整行**读（见 `f6_line`），
    否则 `N/A` 与"判过且族对"在 `PASS/FAIL` 上分不开。
    """
    fix = FIX / "font-not-embedded.pdf"
    b = f6_line(CHK, fix)
    a = f6_line(mp, fix)
    ok = (b.startswith("PASS") and "N/A" in b and "未内嵌" in b
          and a.startswith("FAIL") and "Helvetica" in a)
    return (ok,
            f"font-not-embedded.pdf F6 『{b}』→『{a}』（内嵌事实被拆掉 ⇒ 只被引用的 `Helvetica` 被当成内嵌、"
            f"族表里没有它 ⇒ 判族转红；内嵌事实没拆时它走 `N/A` 分支、**不**判族）")


# ---------------------------------------------------------------- mcm-schematic Task 2（`A` 族）
# 这一组打的是**示意图专属**的 `A1`/`A3`/`A4`（检查器带 `--schematic` 才追加）。
# ★ 为什么单独一组、单独一个 runner：`reader()` 走的是**默认路径**（不带 `--schematic`），
#   而那正是"F1–F6 一字未动"的回归面 —— 拿它测 A 族会**永远读不到 A 行**（恒 `-`）。
# ★ 支点 = `tests/skills/schematic/fixtures/*.pdf`（Task 1 的骨架自证控制组；它们**本就该 A 全绿**）。
SCH_FIX = HERE.parent / "schematic" / "fixtures"
SCH_LIN = SCH_FIX / "pipeline-linear.pdf"      # 线宽 ∈ {0.5, 0.7} 的两阶段流程图
SCH_MECH = SCH_FIX / "mechanism-block.pdf"     # 含 0.5mm/1.4mm 两条"流"，fs 里有 pgf 宽 0.861 的箭头尖
SCH_LAY = SCH_FIX / "model-layered.pdf"        # 9 个节点 + 3 条**只描边**的分组框


def sch_run(checker, fig, caption="Figure 1: a schematic"):
    """跑某检查器（**带 `--schematic`**）：返回 (rc, stdout, stderr)。"""
    cmd = [sys.executable, str(checker), "--fig", str(fig), "--caption", caption,
           "--textwidth-in", "6.75", "--schematic"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def sch_v(checker, fig, crit):
    """某检查器在 `--schematic` 下对某骨架打的某条 A 判词的 PASS/FAIL（`-` = 没这条）。"""
    return verdict(sch_run(checker, fig)[1], crit)


def m59(before, after, mp):
    """`A1` 的"重叠"谓词参与了判定（取反 ⇒ 干净骨架由 PASS 转 FAIL）；同一条变异体上 A3/A4 **不受影响**。"""
    lin_b, lin_a = sch_v(CHK, SCH_LIN, "A1"), sch_v(mp, SCH_LIN, "A1")
    lay_b, lay_a = sch_v(CHK, SCH_LAY, "A1"), sch_v(mp, SCH_LAY, "A1")
    a3 = sch_v(mp, SCH_LIN, "A3")
    a4 = sch_v(mp, SCH_LIN, "A4")
    return (lin_b == "PASS" and lin_a == "FAIL" and lay_b == "PASS" and lay_a == "FAIL"
            and a3 == "PASS" and a4 == "PASS",
            f"pipeline-linear A1 {lin_b}→{lin_a}；model-layered A1 {lay_b}→{lay_a}"
            f"（两条 A1 都翻红 ⇒ 谓词在判定）；同一变异体上 pipeline-linear A3={a3} · A4={a4}"
            f"（A3/A4 不受影响 ⇒ 变异是定向的）")


def m60(before, after, mp):
    """`A1` 的**射程边界对照（必须仍绿）**：把重叠容差收成"天文数字"（只认大到离谱的交叠）⇒ 干净骨架**仍 PASS**。

    与 `M59` 配对：`M59` 把谓词取反 ⇒ 全部翻红；`M60` 把闸门收到几乎不可能触发 ⇒ 全部仍绿。
    两条一起把 `A1` 的"红/绿都由真读数决定、不是恒红也不是恒绿"钉住。
    """
    lin = sch_v(mp, SCH_LIN, "A1")
    lay = sch_v(mp, SCH_LAY, "A1")
    mech = sch_v(mp, SCH_MECH, "A1")
    return (lin == "PASS" and lay == "PASS" and mech == "PASS",
            f"容差收到 1e9pt 后：pipeline-linear A1={lin} · model-layered A1={lay} · mechanism-block A1={mech}"
            f"（三条骨架**仍全绿** ⇒ `A1` 的绿不是「闸门关死」的结果）")


def m61(before, after, mp):
    """`A4` 的"**只取纯描边**"这条窄化承重：把 `fs`（填充+描边）也算进来 ⇒ 只有 `mechanism-block` 翻红
    （它的箭头尖读到 pgf 宽 0.861，不在允许集合里）。

    ★ 这条同时是**射程边界对照**：同一变异体上 `pipeline-linear`/`model-layered` 的 `fs` 件
      （节点框 + 箭头尖）宽度都落在 {0.5, 0.7, 0.9} 里 ⇒ **仍绿** ⇒ 翻红的是"箭头尖那类"，
      不是"整个 A4 恒红"。
    """
    mech_b, mech_a = sch_v(CHK, SCH_MECH, "A4"), sch_v(mp, SCH_MECH, "A4")
    lin_a, lay_a = sch_v(mp, SCH_LIN, "A4"), sch_v(mp, SCH_LAY, "A4")
    return (mech_b == "PASS" and mech_a == "FAIL" and lin_a == "PASS" and lay_a == "PASS",
            f"mechanism-block A4 {mech_b}→{mech_a}（把 fs 也算进来 ⇒ 箭头尖的 0.861 越界）；"
            f"对照 pipeline-linear A4={lin_a} · model-layered A4={lay_a}（它们的 fs 件宽度合法 ⇒ 仍绿）")


def m62(before, after, mp):
    """`A4` 的允许集合真参与判定：收窄成 `(0.5, 0.7)` ⇒ 只用这两档的 `pipeline-linear` **仍绿**，
    而用 1.4mm/0.5mm 两条"流"的 `mechanism-block` **转红**（同 `M57` 的"收窄"角色）。"""
    lin_b, lin_a = sch_v(CHK, SCH_LIN, "A4"), sch_v(mp, SCH_LIN, "A4")
    mech_b, mech_a = sch_v(CHK, SCH_MECH, "A4"), sch_v(mp, SCH_MECH, "A4")
    return (lin_b == "PASS" and lin_a == "PASS" and mech_b == "PASS" and mech_a == "FAIL",
            f"允许集合收窄到 (0.5, 0.7)：pipeline-linear A4 {lin_b}→{lin_a}（它的线宽正是这两档 ⇒ **仍绿**）；"
            f"mechanism-block A4 {mech_b}→{mech_a}（它的流 1.417/3.968 出集合 ⇒ 转红）")


def m63(before, after, mp):
    """`A3` 的谓词参与了判定（取反 ⇒ 干净骨架由 PASS 转 FAIL）。"""
    lin_b, lin_a = sch_v(CHK, SCH_LIN, "A3"), sch_v(mp, SCH_LIN, "A3")
    mech_b, mech_a = sch_v(CHK, SCH_MECH, "A3"), sch_v(mp, SCH_MECH, "A3")
    return (lin_b == "PASS" and lin_a == "FAIL" and mech_b == "PASS" and mech_a == "FAIL",
            f"pipeline-linear A3 {lin_b}→{lin_a}；mechanism-block A3 {mech_b}→{mech_a}（谓词在判定）")


def m64(before, after, mp):
    """`A3` 的**射程边界对照（必须仍绿）**：把页框容差收到 0pt（最严）⇒ 骨架的文字**本来全在框内**
    ⇒ 仍 PASS ⇒ `A3` 的绿不是"容差给的"。"""
    lin = sch_v(mp, SCH_LIN, "A3")
    mech = sch_v(mp, SCH_MECH, "A3")
    lay = sch_v(mp, SCH_LAY, "A3")
    return (lin == "PASS" and mech == "PASS" and lay == "PASS",
            f"容差收到 0pt 后：pipeline-linear A3={lin} · mechanism-block A3={mech} · model-layered A3={lay}"
            f"（三条骨架**仍全绿** ⇒ 它们的文字确实都在页框内，不是容差兜的）")


def m65(before, after, mp):
    """`P3b` · **丢格探针**：`A` 行会不会被"只认 `F` 的"证据解析器**静默丢掉**？

    做法：拿**真产物**跑出带 `A` 行的检查器输出（`mechanism-block` + `--schematic`），
    喂给 `figure-choose/green/make-evidence.py` 里那个**入库的** `CELL_RE`（现在放宽成 `[A-Z]\\d+[a-z]?`），
    再喂给**放宽前**的老串 `(F\\d[abcd]?)`。断言：放宽后**每条 A 行都被抓到**、老串**把 A 行全丢**。
    ⇒ 这一条钉的是"**放宽真的承重**"：没有它，`A` 行进证据表就是**少几格而汇总照旧绿**。
    ★ 它**不是**"判据变异"（不改检查器）—— 是一条**解析器探针**（同 `R1` 的角色），故**不进 `MUTATIONS`**；
      由 `sch_parser_probe()` 单独跑，不参与 `MUT:n/m 红` 的分子分母。

    ⚠️ **覆盖边界（如实登记，不声称穷尽）**：P3b 放宽的"只认 `F` 前缀"的取证解析器共 **5 处**
    （`git grep 're.compile/match' × 'PASS|FAIL'` 逐件查过）：`figure-choose/green/make-evidence.py`
    的 `CELL_RE`（**:85**）与 `verdicts()` 里的内联 `re.match`（**:353**）、`plot-python`（**:31**）、
    `plot-matlab`（**:37**）、`plot-origin`（**:41**）三份 `make-evidence.py` 的 `LINE_RE`。
    本探针**只钉住其中 1 处**（`CELL_RE`）；**另外 4 处未被本探针覆盖**。
    ★ 且 `A` 族被 `--schematic` 门控 ⇒ 这 5 个走默认路径的解析器**今天还收不到 `A` 行**
    ⇒ 本探针证明的是"**放宽真的承重**"（放宽前老串确实丢 `A` 行），**不是**"今天就在丢格"。
    """
    out = sch_run(CHK, SCH_MECH)[1]
    src = (HERE / "green" / "make-evidence.py").read_bytes().decode("utf-8")
    m = re.search(r"^CELL_RE = re\.compile\((.*)\)$", src, re.M)
    if not m:
        raise AssertionError("green/make-evidence.py 里找不到 CELL_RE 的 `re.compile(...)` 行（驱动器自己报错）")
    new_pat = re.compile(eval(m.group(1)))                      # noqa: S307（读的是本仓自己的字面量）
    old_pat = re.compile(r"^(PASS|FAIL)\s+(F\d[abcd]?)\s+(.*)$")
    def ids(pat):
        return [ln.split()[1] for ln in out.splitlines() if pat.match(ln)]
    new_ids, old_ids = ids(new_pat), ids(old_pat)
    n_a_new = sum(1 for i in new_ids if i.startswith("A"))
    n_a_old = sum(1 for i in old_ids if i.startswith("A"))
    ok = (n_a_new >= 3 and n_a_old == 0 and len(new_ids) > len(old_ids))
    return ok, (f"真产物 mechanism-block（`--schematic`）的输出里 A 行 {n_a_new} 条 —— 入库 `CELL_RE`（放宽后）"
                f"抓到 {len(new_ids)} 条 id，含 A {n_a_new} 条；**放宽前**的老串 `(F\\d[abcd]?)` 只抓 {len(old_ids)} 条、"
                f"A {n_a_old} 条 ⇒ {'放宽真的承重' if ok else '未达预期 <<<'}（不放宽 ⇒ 证据表少这几格而汇总照旧绿）")


def run_sch_mutations():
    """跑 `A` 族的变异组（`M59`–`M64`）+ 丢格探针 `M65`。

    变异体的断言**全部**走 `sch_v()`（`--schematic`）；`byte_ok` 在跑完后由调用方统一自证。
    """
    src = CHK.read_bytes()
    MUTD.mkdir(exist_ok=True)
    rows, failed = [], []
    for mid, desc, old, new, fn in SCH_MUTATIONS:
        mp = MUTD / f"check-figure-style.{mid}.py"
        try:
            mutate(src, old, new, mp)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            rows.append(("RED-BAD", mid, desc, f"驱动器自己报错：{e}"))
            continue
        try:
            ok, detail = fn(None, None, mp)
        except AssertionError as e:
            ok, detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
        mp.unlink(missing_ok=True)
    # 丢格探针（不是判据变异）
    try:
        p_ok, p_detail = m65(None, None, None)
    except (AssertionError, KeyError, StopIteration) as e:      # noqa: BLE001（驱动器自己的出口）
        p_ok, p_detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    probe = ("RED-OK" if p_ok else "RED-BAD", "M65",
             "丢格探针：`A` 行会不会被只认 `F` 的证据解析器静默丢掉", p_detail)
    if not p_ok:
        failed.append("M65")
    return rows, failed, probe


# (编号, 说明, 原文, 改文, 断言)
SCH_MUTATIONS = [
    ("M59", "`A1`：重叠谓词取反（`not ov` → `bool(ov)`）⇒ 干净骨架由 PASS 转 FAIL",
     'out.append(("A1", not ov, f"节点框 {len(boxes)} 个，重叠 {len(ov)} 对：{ov[:4]}"))',
     'out.append(("A1", bool(ov), f"节点框 {len(boxes)} 个，重叠 {len(ov)} 对：{ov[:4]}"))', m59),
    ("M60", "`A1` 射程边界对照（**必须仍绿**）：重叠容差 0.5pt → 1e9pt（几乎不可能触发）",
     'if (min(a.x1, b.x1) - max(a.x0, b.x0)) > 0.5 and (min(a.y1, b.y1) - max(a.y0, b.y0)) > 0.5:',
     'if (min(a.x1, b.x1) - max(a.x0, b.x0)) > 1e9 and (min(a.y1, b.y1) - max(a.y0, b.y0)) > 1e9:', m60),
    ("M61", "`A4` 的\"只取纯描边\"窄化承重：`type == 's'` → `\"s\" in type`（把 fs 也算进来）⇒ "
            "只有 mechanism-block 翻红（箭头尖 0.861）",
     'widths = [(dr.get("width") or 0.0) for dr in drawings if (dr.get("type") or "") == "s"]',
     'widths = [(dr.get("width") or 0.0) for dr in drawings if "s" in (dr.get("type") or "")]', m61),
    ("M62", "`A4` 允许集合收窄成 (0.5, 0.7)：pipeline-linear **仍绿**、mechanism-block 转红",
     "SCH_LINEWIDTH_OK = (0.5, 0.7, 0.9, round(0.5 * _MM_PT, 4), round(1.4 * _MM_PT, 4))",
     "SCH_LINEWIDTH_OK = (0.5, 0.7)", m62),
    ("M63", "`A3`：越界谓词取反（`not bad` → `bool(bad)`）⇒ 干净骨架由 PASS 转 FAIL",
     'out.append(("A3", not bad, f"越出页框 {len(bad)} 词（容差 {SCH_PAGE_TOL}pt）：{bad[:4]}；共 {len(words)} 词"))',
     'out.append(("A3", bool(bad), f"越出页框 {len(bad)} 词（容差 {SCH_PAGE_TOL}pt）：{bad[:4]}；共 {len(words)} 词"))', m63),
    ("M64", "`A3` 射程边界对照（**必须仍绿**）：页框容差 0.5pt → 0pt（最严）",
     "SCH_PAGE_TOL = 0.5", "SCH_PAGE_TOL = 0.0", m64),
]

# (编号, 说明, 原文, 改文, 断言)
MUTATIONS = [
    ("M1", "F1_HI 1.20 → 0.90", "F1_LO, F1_HI = 0.80, 1.20", "F1_LO, F1_HI = 0.80, 0.90", m1),
    ("M2", "F1_LO/F1_HI 互换（区间空）", "F1_LO, F1_HI = 0.80, 1.20", "F1_LO, F1_HI = 1.20, 0.80", m2),
    ("M3", "PNG 无 --dpi 时不再 fail-closed，改成默认 200 硬着头皮判",
     '    if dpi is None:\n        fail_closed("FAIL F1: PNG 需要显式 --dpi（PNG 的 dpi 元信息不可信，见 provenance）")',
     '    if dpi is None:\n        dpi = 200  # 变异：守卫拆掉，默认 200 硬着头皮判', m3),
    ("M4", "F2 噪声地板 0.005 → 0.0", "c / tot >= 0.005", "c / tot >= 0.0", m4),
    ("M5", "CAP_MAX 12 → 99（CAP_HARD 17 不动）", "CAP_MAX, CAP_HARD = 12, 17", "CAP_MAX, CAP_HARD = 99, 17", m5),
    ("M6", "F3c 判定取反", 'res.append(("F3c", not cap.endswith("."), "句末不加句号"))',
     'res.append(("F3c", cap.endswith("."), "句末不加句号"))', m6),
    ("M7", "F2 的 PDF 栅格化分支整段删掉（退回 Image.open 读 PDF）",
     '''        if path.suffix.lower() == ".pdf":
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                pm = doc[0].get_pixmap(dpi=RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
                return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        with Image.open(path) as im:''',
     "        with Image.open(path) as im:", m7),
    ("M8", "F3a 判定取反", 'res.append(("F3a", bool(re.match(r"^Figure\\s+\\d+\\s*:", cap)), "图注以 `Figure N:` 起"))',
     'res.append(("F3a", not bool(re.match(r"^Figure\\s+\\d+\\s*:", cap)), "图注以 `Figure N:` 起"))', m8),
    ("M42", "F3b 词数口径由**正文**换回**整条**（`len(body.split())` → `len(cap.split())`）",
     "    words = len(body.split())", "    words = len(cap.split())", m42),
    # ---- M3 Task 3：F4/F5/F6 三条新判据的变异（+ F5 的射程边界对照 M57）
    ("M54", "F4 的**外缘环**那一路退回**全图众数**（合取口径换回 I-1 的病根口径）⇒ "
            "支点 ok-06 由 PASS 转 FAIL（边界对照**跑在变体上**）；附第二支变体单证 BG_MIN_LUMA 仍承重",
     "    ring_rgb, ring_cnt, ring_tot = outer_ring_mode(im4)",
     "    _gm = max(_cols, key=lambda t: t[0])\n"
     "    ring_rgb, ring_cnt, ring_tot = _gm[1], _gm[0], tot4   # 变异 M54：退回全图众数", m54),
    ("M55", "F5 允许色序清空（H14 → 仅 #000000；判据失效）",
     'next(e["value"] for e in _STYLE["entries"] if e["id"] == "series.color")',
     '["#000000"]', m55),
    ("M56", "F6 可接受字体族清空（→ (\"__none__\",)；判据失效）",
     'FONT_FAMILY_OK = ("TeXGyreTermesX", "TimesNewRomanPSMT", "TimesNewRoman", "NimbusRoman", "FreeSerif")',
     'FONT_FAMILY_OK = ("__none__",)', m56),
    ("M57", "F5 射程边界对照：允许集合收窄成 H14 前三色子集 ⇒ 合法子集样本必须**仍绿**（同 `M50` 角色）",
     'next(e["value"] for e in _STYLE["entries"] if e["id"] == "series.color")',
     '["#E69F00", "#56B4E9", "#009E73"]', m57),
    ("M58", "F6 的内嵌判定退回『有字体名即算内嵌』（不看 /FontFile*）⇒ "
            "只引用未内嵌的 `font-not-embedded.pdf` 由 `N/A` 转 `FAIL`",
     '    if ftype == "Type3":\n        return True', '    if True:  # 变异：不看 /FontFile*，有名字就算内嵌\n        return True', m58),
]

# 探针（不是"判据变异"，是"验收脚本的 ERROR 分支变异"）：只在 **期望 FAIL 的那一行** fail-closed
PROBE = ("P1", "run-expected.py 的 ERROR 分支：rc=2/无判词 ⇒ 记 ERROR 且整轮非零退出",
         "    res = check(p, cap, a.textwidth_in, a.dpi, schematic=a.schematic)",
         "    if p.name == \"bad-f2-five-colors.pdf\":\n"
         "        sys.exit(EXIT_FAIL_CLOSED)  # 探针：只在期望 FAIL 的那一行 fail-closed\n"
         "    res = check(p, cap, a.textwidth_in, a.dpi, schematic=a.schematic)")


def p1(mp):
    """跑两遍逐格验收：干净一遍（须 MISMATCH 0 / N 且 exit 0），对变异体一遍（须记 ERROR 且 exit≠0）。

    `--checker` 就是为这条探针加的（默认值不变，收工 gate 不带该参数跑）。
    """
    clean = subprocess.run([sys.executable, str(FIX / "run-expected.py")], capture_output=True, text=True)
    mut = subprocess.run([sys.executable, str(FIX / "run-expected.py"), "--checker", str(mp)],
                         capture_output=True, text=True)
    c_last, m_last = clean.stdout.strip().splitlines()[-1], mut.stdout.strip().splitlines()[-1]
    err_rows = [l for l in mut.stdout.splitlines() if l.startswith("ERROR")]
    rc_b, out_b, _ = run_checker(CHK, FIX / PDF_BAD, IMG_CAP)
    rc_m, out_m, _ = run_checker(mp, FIX / PDF_BAD, IMG_CAP)
    # 旧版谓词（只看 "PASS  <crit>" 在不在）读同一份空 stdout 会得出什么：
    old_got = "PASS" if "PASS  F2 " in out_m else "FAIL"
    ok = (clean.returncode == 0 and c_last.startswith("MISMATCH 0 / ") and "ERROR" not in c_last
          and mut.returncode != 0 and m_last.startswith("MISMATCH 0 / ") and "ERROR 1" in m_last
          and len(err_rows) == 1
          and rc_b == 1 and verdict(out_b, "F2") == "FAIL"      # 原检查器：该行真的判成红（rc=1）
          and rc_m == EXIT_FAIL_CLOSED and out_m == "")          # 变异体：该行根本没判成（rc=2）
    return ok, (f"干净一遍 exit={clean.returncode} '{c_last}'；"
                f"对变异体一遍 exit={mut.returncode} '{m_last}'（{len(err_rows)} 行 ERROR）　"
                f"NOTE/同一行：原检查器 exit={rc_b} 判词 F2={verdict(out_b, 'F2')}；"
                f"变异体 exit={rc_m} stdout 空 ⇒ 旧版谓词会记 got={old_got}（= want ⇒ 记 OK，"
                f"整轮报 MISMATCH 0 假绿）；新版记 ERROR 且 exit≠0")


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True, text=True).stdout.strip()


# ================================================================ 规范数守卫的变异（Task 3）
# 为什么**不叫** M7/M8：任务书给的编号 M7–M10 与 `check-figure-style.py` 那一组已占用的
# M7（F2 的 PDF 分支）/ M8（F3a 取反）**撞号**；撞号的变异表会让"哪条红了"没法引用，
# 故本组顺延为 **M9–M12**（逐条对应任务书 M7/M8/M9/M10 的四种手法）。
#
# 这一组打的**不是检查器**，是 `house-style.md` / `provenance.md` ——
# 被验对象 = `check-house-style.py` 的规范数守卫（抽不到数即 fail-closed）。
ROOT = HERE.resolve().parents[2]
HOUSE_DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
HOUSE_PROV = ROOT / ".claude/skills/mcm-figure-choose/references/provenance.md"
HOUSE_SKILLS = ROOT / ".claude/skills"           # `K6` 判"这个 skill 存不存在"的真根
HOUSE_CHK = HERE / "check-house-style.py"
HMUTD = FIX / "_mut-house"


def house_run(checker, doc, prov, only):
    """跑规范数守卫：`--only` 限定被验的那几条，返回 (rc, stdout)。"""
    cmd = [sys.executable, str(checker), "--doc", str(doc), "--prov", str(prov), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def house_assert(desc, doc_src, prov_src, old, new, target, ids):
    """一次字面替换 + 前置/后置两跑。

    前置（`before`）：**原件**上这几条守卫必须全绿 —— 否则"改坏了才红"这条断言在
    "它本来就是红的"时也会通过（与 M2 的 R-6 同一条教训）。
    后置（`after`）：改坏副本上必须 **exit≠0** 且被点名的守卫**逐条**报 FAIL。
    """
    src = (HOUSE_DOC if target == "doc" else HOUSE_PROV).read_bytes()
    n_hit = src.decode("utf-8").count(old)
    if n_hit != 1:
        raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）")
    mutated = src.decode("utf-8").replace(old, new, 1).encode("utf-8")
    assert mutated != src, "变异体与原文相同"
    mp = HMUTD / ("house-style.md" if target == "doc" else "provenance.md")
    mp.write_bytes(mutated)                                  # write_bytes：不用 write_text
    rc_b, out_b = house_run(HOUSE_CHK, doc_src, prov_src, ids)
    rc_a, out_a = house_run(HOUSE_CHK, doc_src if target != "doc" else mp,
                            prov_src if target != "prov" else mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    return pre_ok and post_ok, f"{desc}　{detail}"


def house_mutations():
    """任务书 Step 4 的四种手法（M9–M12）+ 修复轮新增的七条（M13–M19），逐条必须实测红。"""
    return [
        ("M9", "house-style.md 里 H1 的上限 1.20 → 9.99", "doc",
         "**不超过 1.20×**", "**不超过 9.99×**", ["G-H1-hi"]),
        ("M10", "house-style.md 里 H9 的词数上限 12 → 3", "doc",
         "**上限 12 词**（p95）", "**上限 3 词**（p95）", ["G-H9-wmax", "G-H9-const-max"]),
        ("M11", "删掉 H4 那一行（主色中位那条依据）", "doc",
         "出货：主色中位 **2**、出货：零彩色 **30.5%**（202/662）、出货：≤4 覆盖率 **66.3%**（439/662）。\n",
         "", ["G-H4-med", "G-H4-zero", "G-H4-cov"]),
        ("M12", "provenance.md 里 P-H2-a 的复跑命令把分母口径从 p90 改成 mean", "prov",
         "python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_median",
         "python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_mean",
         ["P-H2-a"]),
        # ---- 修复轮（独立评审 Critical-1 / Important-3 / Important-4 / Minor N-7）新增
        ("M13", "H4 把 662 图上的转写口径读数 51.81 改回**已被证伪的 48.79**（Critical-1 的回归位）", "doc",
         "上是 **51.81%** ⇒ **57.2% 与 72.9% 不同源", "上是 **48.79%** ⇒ **57.2% 与 72.9% 不同源",
         ["G-H4-n2lo"]),
        ("M14", "H4 连续色图闸门的箱数下限 ≥100 → ≥20（退回形同虚设的那条腿）", "doc",
         "**彩色箱数 ≥100** **或**", "**彩色箱数 ≥20** **或**", ["G-H4-gate-box"]),
        ("M15", "H4 旧闸门在 heatmap 样本上的命中数 5/13 → 9/13（漏检证据被改坏）", "doc",
         "旧闸门只命中 **5/13**", "旧闸门只命中 **9/13**", ["G-H4-heat-old"]),
        ("M16", "H3 的 120 抽样中位区间 2.24–2.42 → 2.14–2.42（N-5 的回归位）", "doc",
         "中位落在 **2.24–2.42**", "中位落在 **2.14–2.42**", ["G-H3-s120-lo"]),
        ("M17", "H9 的宽口径条数 578 → 572（Important-4 的回归位）", "doc",
         "（**578**/662 = 87.31%", "（**572**/662 = 87.31%", ["G-H9-578"]),
        ("M18", "provenance.md P-H2-b 散文里的右尾 max 7.19 → 8.19（N-7：散文数也要守）", "prov",
         "（max 7.19 in）", "（max 8.19 in）", ["G-P-H2b-max"]),
        ("M19", "H12 的〔社区〕字号下限 ≥7 pt → ≥6 pt（N-8：社区值也不能被静默改掉）", "doc",
         "最小 **≥7 pt**", "最小 **≥6 pt**", ["G-H12-minpt"]),
    ]


# ============================================== `chart-types.md` 的结构守卫变异（Task 4）
# 打的是 `check-house-style.py` 的 `S1`/`S2`/`S3`/`S5`（被验对象 = 那棵决策树的形状）。
# 期望值**分两类**（修复轮 N-2 后）：**入口名 = 契约**（硬编码在检查器的 `ENTRIES`，不从文档现取）；
# **数 = 现取**（该小数所属 `H<n>` 条目里的小数字面量），故这里只写"改哪一处"，不写"应该等于几"。
# `S4` 是读数条（无谓词 ⇒ 无红可证），由探针 `R1` 另证（见 `s4_readout_probe`）。
CT_DOC = ROOT / ".claude/skills/mcm-figure-choose/references/chart-types.md"


def struct_run(checker, ct, only):
    """跑结构守卫：只换 `--ct`（被验的决策树），`house-style.md` / `provenance.md` 用真件。"""
    cmd = [sys.executable, str(checker), "--ct", str(ct), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def ct_assert(desc, edits, ids, probe=None):
    """对 `chart-types.md` 做**一次或多次**字面替换 + 前置/后置两跑。

    `edits` 是 `[(原文, 改文), …]`，每条的命中数必须恰为 1（否则驱动器自己报错）；
    多替换是给 `M26`（要把**两个**小数一起抹掉）用的。
    `probe`：可选，收变异体全文、返回一行**现算**的补充说明（`M24` 用它记"任务书的宽松写法
    在这种改法下不会红"）。
    """
    text = CT_DOC.read_bytes().decode("utf-8")
    for old, new in edits:
        n_hit = text.count(old)
        if n_hit != 1:
            raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）：{old[:48]!r}")
        text = text.replace(old, new, 1)
    if text == CT_DOC.read_bytes().decode("utf-8"):
        raise AssertionError("变异体与原文相同")
    mp = HMUTD / "chart-types.md"
    mp.write_bytes(text.encode("utf-8"))                      # write_bytes：不用 write_text
    rc_b, out_b = struct_run(HOUSE_CHK, CT_DOC, ids)
    rc_a, out_a = struct_run(HOUSE_CHK, mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    if probe:
        detail += "　" + probe(text)
    return pre_ok and post_ok, f"{desc}　{detail}"


def _m24_probe(txt):
    """`M24` 的现算 NOTE：任务书那条正则（**全文**扫 radar×低频）在这个变异体上到底还红不红。"""
    lax = bool(re.search(r"radar[^\n]*低频|低频[^\n]*radar", txt, re.I))
    return (f"NOTE/任务书给的正则（**全文**扫 `radar` × `低频`）在本变异体上仍"
            f"{'**命中** ⇒ 那个写法会漏掉这次改坏' if lax else '不命中'}"
            f"；本实现只扫 **radar 定义行** ⇒ 红")


def _old_pool():
    """**修复前**的 `S5` 同值池：`house-style.md` ∪ `provenance.md` 的小数字面量全集（现取）。"""
    return set(re.findall(r"\d+\.\d+", HOUSE_DOC.read_bytes().decode("utf-8"))) | \
        set(re.findall(r"\d+\.\d+", HOUSE_PROV.read_bytes().decode("utf-8")))


def _house_h_nums(hid):
    """`house-style.md` 的 `### H<hid>.` 条目里的小数字面量（与检查器 `_h_entries` 同口径，现取）。"""
    txt = HOUSE_DOC.read_bytes().decode("utf-8")
    m = re.search(rf"^### H{hid}\..*?$(.*?)(?=^### H\d+\.|\Z)", txt, re.M | re.S)
    return set(re.findall(r"\d+\.\d+", m.group(1))) if m else set()


def _s5_scope_probe(num, hid=None):
    """`M27`/`M28` 的现算 NOTE：这个数**旧写法怎么会绿**、**新写法为什么红**。

    旧写法（`S5` 修复前）= "值 ∈ house-style ∪ provenance 的全局池"（池里混着容差常量与
    别的 `H<n>` 条目的数）⇒ 池内一律绿。新写法 = **归到同行 `H<n>` 引用**且 **∈ 该条目的数**。
    """
    def probe(_txt):
        pool = _old_pool()
        if hid is None:
            return (f"NOTE/`{num}` 在**旧池子**（{len(pool)} 个数）里: {num in pool}"
                    f" ⇒ 旧写法**判绿、漏掉这次改坏**；新写法：该行**没有任何 `H<n>` 引用**"
                    f" ⇒ 无所属 ⇒ 红（fail-closed）")
        ent = _house_h_nums(hid)
        return (f"NOTE/`{num}` 在**旧池子**（{len(pool)} 个数）里: {num in pool}"
                f" ⇒ 旧写法**判绿、漏掉这次改坏**；`H{hid}` 条目的数 {sorted(ent)} 里"
                f"{'有它' if num in ent else '**没有它**'} ⇒ 新写法红（跨条目搬数）")
    return probe


def struct_mutations():
    """`M22`–`M28`：`chart-types.md` 的七种改坏手法，逐条必须实测红。"""
    return [
        ("M22", "chart-types.md：入口 9 由『不确定性』**改名**（九个入口少一个）",
         [("### 入口 9 · 不确定性", "### 入口 9 · 时变")], ["S1"], None),
        ("M23", "chart-types.md：删掉入口 1 的『**备选**』那一段（四段少一段）",
         [("**备选**：`dot plot`", "**可替代方案**：`dot plot`")], ["S2"], None),
        ("M24", "chart-types.md：删掉 **radar 定义行**上的『低频』标注",
         [("连成多边形 —— **低频**：获奖样本里属罕见选择", "连成多边形 —— 获奖样本里属罕见选择")],
         ["S3"], _m24_probe),
        ("M25", "chart-types.md：3D 那条参照分布数 9.2% → 9.3%（与 house-style 不同值）",
         [("**9.2%**", "**9.3%**")], ["S5"], None),
        ("M26", "chart-types.md：两个小数**都**写成中文数字 ⇒ 一个实测数都抽不到（fail-closed 该红）",
         [("**0.0%**", "**零**"), ("**9.2%**", "**九点二**")], ["S5"], None),
        # ---- 修复轮（复审 N-2）：`S5` 的归属口径从"全局池"收紧到"该 `H<n>` 条目"
        ("M27", "chart-types.md：写进一个**池内但无所属**的数 `1.20`（H1 的上限，旧池子里有它）",
         [('   机械守卫 `S5` 管的是**抄过来之后有没有漂**，不是"这个数本身对不对"。',
           '   机械守卫 `S5` 管的是**抄过来之后有没有漂**，不是"这个数本身对不对"。'
           '图宽与正文宽之比**不超过 1.20**。')], ["S5"], _s5_scope_probe("1.20")),
        ("M28", "chart-types.md：H7 那条的数 `9.2` 换成 `0.5`（H4 的地板，**池内但语义不同**）",
         [("**9.2%**", "**0.5%**")], ["S5"], _s5_scope_probe("0.5", "7")),
    ]


# ============================================== `SKILL.md` 的短契约守卫变异（Task 5）
# 打的是 `check-house-style.py` 的 `K1`–`K6`（被验对象 = `SKILL.md` 这份**短契约**）。
# 为什么从 **`M29`** 起：`M1`–`M8`（检查器）· `M9`–`M19`（规范数）· `C1`/`C2`（CENSUS）·
# `M22`–`M28`（`chart-types.md` 的结构）已占号；任务书给的 `M14`/`M15`/`M16` 与上面**撞号**，
# 撞号的变异表会让"哪条红了"没法引用（同 Task 3 顺延 `M9`–`M12` 的那次），故顺延 `M29` 起。
# 期望值分两类（与结构守卫同）：**契约型硬编码**（行数上限 / 指针路径 / 九个入口名）·
# **现取型**（禁止串从 `house-style.md` 现取）—— 故这里只写"改哪一处"，不写"应该等于几"。
SKILL_MD = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"


def sub_once(text, old, new):
    """一次字面替换：命中数必须恰为 1（否则驱动器自己报错）。"""
    n = text.count(old)
    if n != 1:
        raise AssertionError(f"原文串命中 {n} 次（必须恰为 1）：{old[:44]!r}")
    return text.replace(old, new, 1)


def sub_all(text, old, new):
    """替换**全部**出现处（用于"把某个名字从全文拿掉"这类改法；命中数必须 ≥1）。"""
    n = text.count(old)
    if n < 1:
        raise AssertionError(f"原文串一次都没命中：{old[:44]!r}")
    return text.replace(old, new)


def pad_to(text, n):
    """在文末补空行，把行数**恰**撑到 `n`（`M31` 用）。"""
    cur = len(text.splitlines())
    if cur >= n:
        raise AssertionError(f"原文已有 {cur} 行 ≥ {n}")
    return text + "\n" * (n - cur)


# ---- `M33`/`M40` 的**自造〔拟建〕场景**（2026-10-02 origin Task 1 改造）。
# 为什么不再"从被改文本现取仍〔拟建〕的那一个"：`mcm-plot-origin` 是本支**最后一个**待建绘图
# skill，它落地后真仓**一个仍〔拟建〕的绘图 skill 都没有** ⇒ 现取式写法在**空集**上 fail-closed
# 抛错（`M33`/`M40` 双双失去对象），而这一次**没有"下一个待建"可以换过去**（matlab 那轮换到了
# origin，正是本支）。⇒ 改成**自造场景**：在**副本 / 临时根**里**注入**一个**永不建目录**的绘图
# skill 名（带〔拟建〕）——「标记与事实一致（不存在且标了）」= 绿、**可断言**；「摘掉标记」(`M33`)
# 或「让它"存在"」(`M40`) = 红。两条都**不再依赖真仓是否还有待建 skill**。
# ★ 这同时**了结了已知脆弱 `M3-matlab-T1c`**（"若某天一个仍〔拟建〕的都没有，M33/M40 都会抛错"）。
PENDING_SKILL = "mcm-plot-pending"          # 该名**永不建目录** ⇒ 在 `K6` 眼里它"不存在"
PENDING_MARK = "（〔拟建〕）"
PENDING_NAMED = f"- `{PENDING_SKILL}`"      # 不带标记的形态
PENDING_MARKED = PENDING_NAMED + PENDING_MARK   # 带标记的形态（= `K6` 眼里"一致"的那态）
_PLOT_LINE_RE = re.compile(r"^\s*- `mcm-plot-[a-z]+`")


def inject_pending(text, marked=True):
    """在 `text` 的**最后一行绘图 skill 列表项**之后**注入**一行 `mcm-plot-pending`（可带标记）。

    注入点 = `_PLOT_LINE_RE` 命中的**最后一行**（语义锚是"边界段那张列表的末尾"），
    **不写死任何一个真 skill 名** —— 那些名字本身也会随绘图家族演进变。
    """
    lines = text.splitlines(keepends=True)
    hits = [i for i, l in enumerate(lines) if _PLOT_LINE_RE.match(l)]
    if not hits:
        raise AssertionError("被改文本里找不到『- `mcm-plot-*`』形态的行 ⇒ 注入点不存在（fail-closed）")
    lines.insert(hits[-1] + 1, "  " + (PENDING_MARKED if marked else PENDING_NAMED) + "\n")
    return "".join(lines)


def strip_pending_mark(text):
    """`M33` 的改法：把**注入行**上的〔拟建〕摘掉（只摘我们自己注入的那一行，真件的行不碰）。"""
    if PENDING_MARKED not in text:
        raise AssertionError(f"文本里没有注入的『{PENDING_MARKED}』 ⇒ M33 失去对象（fail-closed）")
    return text.replace(PENDING_MARKED, PENDING_NAMED)


def skill_run(checker, skill, only):
    """跑 SKILL 守卫：只换 `--skill`（被验的短契约），其余文档用真件。"""
    cmd = [sys.executable, str(checker), "--skill", str(skill), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def skill_assert(desc, transform, ids, probe=None):
    """对 `SKILL.md` 做一次（或一串）字面替换 + 前置/后置两跑。

    前置（原件）必须全绿、后置（改坏副本）必须 exit≠0 **且**被点名的守卫逐条报 FAIL ——
    与 `house_assert` / `ct_assert` 同一条纪律（"它本来就是红的"不算证据）。
    `probe`：可选，收**变异体全文**、返回一行**现算**的补充说明（`M30` 用它记"任务书那条宽松
    谓词（`references/house-style.md` 或裸 `house-style.md` 任一命中即可）在这种改法下不会红"）。
    """
    text0 = SKILL_MD.read_bytes().decode("utf-8")
    text = transform(text0)
    if text == text0:
        raise AssertionError("变异体与原文相同")
    mp = HMUTD / "SKILL.md"
    mp.write_bytes(text.encode("utf-8"))                      # write_bytes：不用 write_text
    rc_b, out_b = skill_run(HOUSE_CHK, SKILL_MD, ids)
    rc_a, out_a = skill_run(HOUSE_CHK, mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    if probe:
        detail += "　" + probe(text)
    return pre_ok and post_ok, f"{desc}　{detail}"


def _m30_probe(_txt):
    """`M30` 的现算 NOTE：**任务书那条宽松谓词**在这个变异体上会不会红。

    任务书的 `K2` 写的是 `"references/house-style.md" in txt or "house-style.md" in txt` ——
    `SKILL.md` 通篇要提规范，裸文件名**必然**还在 ⇒ 那个写法**判绿**、漏掉这次改坏
    （"指针还在不在"会被一句"见 house-style.md"顶包）。本实现要求**skill 目录内的相对路径**，
    即 Task 7 的检查器要核的那个形态。
    """
    hit_bare = "house-style.md" in _txt
    return (f"NOTE/任务书那条宽松谓词（路径**或**裸文件名任一即可）在本变异体上仍"
            f"{'**命中** ⇒ 那个写法会漏掉这次改坏' if hit_bare else '不命中'}；"
            f"本实现要求 `references/house-style.md` 这个**相对路径** ⇒ 红")


def _k5_scope_probe(num):
    """`M29` 的现算 NOTE：这个数为什么**两条守卫都该红**（K3 与 K5 是两道不同的闸）。"""
    def probe(_txt):
        doc = HOUSE_DOC.read_bytes().decode("utf-8")
        banned = bool(re.search(rf"(?<![\d.]){re.escape(num)}(?![\d])", doc))
        return (f"NOTE/`{num}` 在 `house-style.md` 里出现: {banned} ⇒ `K3`（现取禁止串）"
                f"{'红' if banned else '**不会红（不在禁止串表里）**'}；`K5`（除 `H<n>` 外每个数"
                f"都要被声明为结构性计数）与禁止串表无关 —— 这个数没被声明就红（本次即红，"
                f"故两条是**两道不同的闸**，不是同一条判两遍）")
    return probe


def drop_section(text, start, end):
    """把 `## <start>` 那一节**整段**删掉（删到下一个 `## <end>` 之前）。"""
    lines = text.splitlines(keepends=True)
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = next(k for k, l in enumerate(lines) if k > i and l.startswith(end))
    return "".join(lines[:i] + lines[j:])


TOP_ITEM = "- **推荐图型**：给**一个首选**；"


def _m36_probe(_txt):
    """`M36` 的现算 NOTE：为什么这条**只能**由单位词臂红 —— 直接读 `K3` 在同一副本上印出的读数。"""
    _rc, out = skill_run(HOUSE_CHK, HMUTD / "SKILL.md", ["K3"])
    line = next((l for l in out.splitlines() if l.startswith(("PASS  K3", "FAIL  K3"))), "")
    mb = re.search(r"裸值词 \[([^\]]*)\]", line)
    mu = re.search(r"≥(\d+)", line)
    mh = re.search(r"中文命中 (\[[^\]]*\]|无)", line)
    return (f"NOTE/同一副本上 `K3` 印出的『裸值词』= [{mb.group(1) if mb else '?'}]"
            f"（下界 ≥{mu.group(1) if mu else '?'}）、『中文命中』= {mh.group(1) if mh else '?'}"
            f" ⇒ 插入串里的 `一` **不在裸值词里**（1 < 下界），这条红的是**单位词臂**"
            f"（`倍` 是 `×` 的中文写法）—— 两条臂各管一段，只留一条就会漏掉这一半")


def _m38_probe(_txt):
    """`M38` 的现算 NOTE：这段被删掉时 `K1`–`K6` 会不会红 —— 现跑一遍给结论。"""
    rc, out = skill_run(HOUSE_CHK, HMUTD / "SKILL.md", ["K1", "K2", "K3", "K4", "K5", "K6"])
    res = next((l for l in out.splitlines() if l.startswith("RESULT")), "(无 RESULT 行)")
    return (f"NOTE/同一副本上 `K1`–`K6` 现跑 exit={rc}『{res}』 ⇒ 这六条**一条都不红**"
            f"（删掉整段不违反它们中的任何一条）—— `K7` 是这段唯一的机械守卫")


def skill_mutations():
    """`M29`–`M39`（**去 M33**）：`SKILL.md` 的九种改坏手法，逐条必须实测红。

    ★ `M33`（`K6` 正向臂）已于 2026-10-02（origin Task 1）**移出本表**，改由 `m33_pending_mut()`
    以**自造〔拟建〕场景**做（与 `M40` 同批，见 `k6_exists_mut`）—— 理由见上面那段注释。
    """
    return [
        ("M29", "SKILL.md：写进一条规范数值『图宽用满 0.951×正文宽』⇒ 重述规范（`K3` 与 `K5` 都红）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（图宽用满 0.951×正文宽）；"),
         ["K3", "K5"], _k5_scope_probe("0.951")),
        ("M30", "SKILL.md：指针行删掉、别处只留裸文件名 ⇒ `K2` 红（宽松谓词会漏，见 NOTE）",
         # ★ Task 3b 修 ②（M30 曾 RED-BAD）：**拿掉完整路径时必须拿掉所有出现处** ——
         #   Task 2 的 Step 8 又添了一处（L83 的 `规范正文（本目录 references/house-style.md）`），
         #   而原变异只删指针行 + 只改 L10 那一处 ⇒ 该路径仍在 ⇒ `K2` 仍绿、M30 转 RED-BAD。
         #   `sub_all` 是本驱动器既有的"多处字面替换"入口（同 `M32` 拿九个入口名时的用法），
         #   本变异的两步：① 删掉指针行；② 把**其余所有** `\`references/house-style.md\`` 降成裸文件名。
         lambda t: sub_all(sub_once(t, "- **规范正文**（图通常长什么样、每条规则的数值与验证状态）："
                                       "`references/house-style.md`\n", ""),
                            "`references/house-style.md`", "`house-style.md`"),
         ["K2"], _m30_probe),
        ("M31", "SKILL.md：把文件撑到 151 行 ⇒ `K1` 红（短契约上限 <150）",
         lambda t: pad_to(t, 151), ["K1"], None),
        ("M32", "SKILL.md：入口 9 由『不确定性』改名 ⇒ `K4` 红（九个入口少一个）",
         lambda t: sub_all(t, "不确定性", "时变"), ["K4"], None),
        # ---- 修复轮（复审 1 Important + N-2/N-3/N-4）
        ("M35", "SKILL.md：写进『主色四色以内』（中文数词 + 规范单位词）⇒ `K3` 的中文数词臂红"
                "（原先整句走绿，见 Important-1）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（主色四色以内）；"),
         ["K3"], None),
        ("M36", "SKILL.md：写进『图宽不超过一倍正文宽』⇒ `K3` 红（**单位词臂**单独在红，见 NOTE）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（图宽不超过一倍正文宽）；"),
         ["K3"], _m36_probe),
        ("M37", "SKILL.md：把 `4`（H4 的规范值）写进**声明行** ⇒ `K5` 红（声明行只许出现契约数）",
         lambda t: sub_once(t, "② **结构性计数**——全文只有一处，就是决策树的入口数 **9**",
                            "② **结构性计数**——入口数 **9** 与主色上限 **4**"),
         ["K5"], None),
        ("M38", "SKILL.md：删掉「输出契约」整段 ⇒ `K7` 红（该段原先没有任何机械存在性守卫）",
         lambda t: drop_section(t, "## 输出契约", "## 边界"), ["K7"], _m38_probe),
        ("M39", "SKILL.md：决策树表多加一行（= 多一个入口名）⇒ `K4` + `K5` 红（旧写法不会红）",
         lambda t: sub_once(t, "| **不确定性** | 结论有多稳 / 最坏能坏到哪 |",
                            "| **不确定性** | 结论有多稳 / 最坏能坏到哪 |\n| **雷达** | 谁跟谁像 |"),
         ["K4", "K5"], None),
    ]


def _skills_tree():
    """真 skills 根的路径集合指纹（相对路径，已排序）—— 用于证 `M40` **没往真根里写东西**。

    为什么需要它（M3-plot Task 2 的阻断项）：`M40` 原先借"真仓里反正没有 `mcm-plot-python`"
    当**廉价代理**来证"换 `--skills-root` 没碰真根"；该 skill 已真建出 ⇒ 那条代理**恒假**
    ⇒ 驱动器恒 `exit 1`。换成**真测**：把真根的路径集合在跑 `M40` 前后各快照一次、逐字比对。
    """
    return sorted(p.relative_to(HOUSE_SKILLS).as_posix() for p in HOUSE_SKILLS.rglob("*"))


def m33_pending_mut():
    """`M33`：`K6` 的**正向臂** —— 点名一个**不存在**的绘图 skill **却不标〔拟建〕** ⇒ 红。

    **自造场景**（不再从真件现取"仍〔拟建〕"的那一个，理由见上面那段注释）：副本 = 真件 +
    注入一行 `mcm-plot-pending`（〔拟建〕）。先把**注入后（带标记）**这一态跑一遍，证它**绿**
    （⇒ 这条不是恒红、注入点也没落错地方）；再把注入行的标记**摘掉** ⇒ `K6` 红。
    """
    text0 = SKILL_MD.read_bytes().decode("utf-8")
    marked = inject_pending(text0, marked=True)
    stripped = strip_pending_mark(marked)
    if stripped == marked:
        raise AssertionError("摘标记没改到文本（注入没命中？）")
    mp_ok = HMUTD / "k6.pending-marked.SKILL.md"
    mp_bad = HMUTD / "k6.pending-stripped.SKILL.md"
    mp_ok.write_bytes(marked.encode("utf-8"))              # write_bytes：不用 write_text
    mp_bad.write_bytes(stripped.encode("utf-8"))
    rc_ok, out_ok = skill_run(HOUSE_CHK, mp_ok, ["K6"])
    rc_bad, out_bad = skill_run(HOUSE_CHK, mp_bad, ["K6"])
    pre_ok = rc_ok == 0 and "PASS  K6 " in out_ok
    post_ok = rc_bad != 0 and "FAIL  K6 " in out_bad
    line = next((l.split(None, 2)[-1] for l in out_bad.splitlines() if l.startswith("FAIL  K6")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (
        f"前置(注入 `{PENDING_SKILL}`〔拟建〕、真根无此目录) exit={rc_ok} "
        f"{'K6 绿' if pre_ok else '未绿 <<<'}；"
        f"后置(摘掉该行标记 ⇒ 点名不存在却不标) exit={rc_bad} 『{line}』")


def k6_exists_mut():
    """`M40`：`K6` 的**反向臂** —— 标了〔拟建〕的 skill **真的存在**时必须红（复审 N-5）。

    **自造场景**（同 `M33`，不再从真件现取"仍〔拟建〕"的那一个）：副本 = 真件 + 注入一行
    `mcm-plot-pending`（〔拟建〕）；`--skills-root` 指到一个**临时根**，把副本点到的**每一个**
    绘图 skill（含 pending）都建出目录（`K6` 用 `SKILLS_ROOT / <名字>` 的 `.exists()` 判目录）⇒
      · pending：标了〔拟建〕却"存在" ⇒ **标记与事实不符** ⇒ 红；
      · 其余（未标〔拟建〕且"存在"）⇒ 一致 ⇒ 不红。**隔离性质**就在这一步：本变异因此**只**打在
        "标了〔拟建〕却存在"这一个方向上，不与"未标却不存在"的正向臂混在一起。
    前置（真件 + 真根）必须绿；**并**自证跑前跑后真根的路径集合逐字未变（**非侵入**）。
    """
    def run(skpath, sroot):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--skill", str(skpath),
                            "--skills-root", str(sroot), "--only", "K6"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    text0 = SKILL_MD.read_bytes().decode("utf-8")
    fixture = inject_pending(text0, marked=True)
    mp = HMUTD / "k6.pending-exists.SKILL.md"
    mp.write_bytes(fixture.encode("utf-8"))
    names = sorted(set(re.findall(r"mcm-plot-[a-z]+", fixture)))       # `K6` 同款正则

    tree_before = _skills_tree()
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        for n in names:
            (tmp / n).mkdir()          # 每个点名的 skill 都"存在"：未标的与事实一致、标了的（pending）不符
        rc_b, out_b = run(SKILL_MD, HOUSE_SKILLS)          # 前置(真件 + 真根) ⇒ 绿
        rc_a, out_a = run(mp, tmp)                         # 后置(注入行 + 临时根) ⇒ 红
    tree_after = _skills_tree()
    clean = tree_after == tree_before
    pre_ok = rc_b == 0 and "PASS  K6 " in out_b
    post_ok = rc_a != 0 and "FAIL  K6 " in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K6")), "（缺 FAIL 行）")
    return pre_ok and post_ok and clean, (
        f"前置(真 skills 根) exit={rc_b} {'K6 绿' if pre_ok else '未绿 <<<'}；"
        f"后置(临时根里 `{PENDING_SKILL}`〔拟建〕却存在) exit={rc_a} 『{line}』；"
        f"非侵入(真根路径集合跑前/跑后逐字相等)={clean}")


def k8_verify_line_mut():
    """`M41`：`K8` —— `house-style.md` 的每个 `H<n>` 条目都要有**恰一行** `**验证**：`（复审 N-7）。

    做法：在**副本**上把**第一个**带验证行的 `H<n>` 条目里那行抹掉（真件不碰）⇒ 必须红；前置必须绿。
    哪一条被抹掉是**现算**的（不写死 `H4`）—— `H<n>` 的名字与位置都不许抄进脚本。
    """
    src = HOUSE_DOC.read_bytes().decode("utf-8")
    sec = next((m for m in re.finditer(r"^### (H\d+)\..*?$(.*?)(?=^### H\d+\.|\Z)", src, re.M | re.S)
                if "**验证**：" in m.group(2)), None)
    if sec is None:
        raise AssertionError("house-style.md 里找不到带 `**验证**：` 的 `H<n>` 条目（前提不成立）")
    new_blk = re.sub(r"\n\*\*验证\*\*：.*?(?=\n\n)", "\n", sec.group(0), count=1, flags=re.S)
    if new_blk == sec.group(0):
        raise AssertionError("副本没改到（那行没命中？）")
    mut = src[:sec.start()] + new_blk + src[sec.end():]
    mp = HMUTD / "k8.house-style.md"
    mp.write_bytes(mut.encode("utf-8"))                      # write_bytes：不用 write_text

    def run(doc):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--doc", str(doc),
                            "--skill", str(SKILL_MD), "--only", "K8"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    rc_b, out_b = run(HOUSE_DOC)
    rc_a, out_a = run(mp)
    mp.unlink()
    pre_ok = rc_b == 0 and "PASS  K8 " in out_b
    post_ok = rc_a != 0 and "FAIL  K8 " in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K8")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (f"前置(真件) exit={rc_b} {'K8 绿' if pre_ok else '未绿 <<<'}；"
                                f"后置(副本抹掉 `{sec.group(1)}` 的验证行) exit={rc_a} 『{line}』")


# ========================================== 引用完整性检查器（Task 7）的变异（`M43`–`M46`）
# 打的是 `check-spec-pointers.py`（被验对象 = `.claude/skills/*/SKILL.md` 的**引用纪律**：
# 绘图家族的 skill 必须指向 `house-style.md`、且不许重述规范数值）。
#
# 为什么从 **`M43`** 起：`M1`–`M8`（检查器）· `M9`–`M19` + `C1`/`C2`（规范数）· `M22`–`M28`
# （`chart-types.md` 结构）· `M29`–`M41`（`SKILL.md` 短契约）已占号；任务书给的 `M17`–`M20`
# 与上面**撞号**，撞号的变异表会让"哪条红了"没法引用（同 Task 3 顺延 `M9`、Task 5 顺延 `M29`
# 那两次），故顺延 `M43` 起。
#
# 为什么这四条**必须**存在：真仓**此刻** 0 个绘图家族 skill（`mcm-plot-*` / `mcm-table` /
# `mcm-schematic` 这几族还没建出来）⇒ 只跑真仓，检查器的逐份判据**一次都不执行**，
# "它真的会红"就只是一句自称。故这组全靠 `--skills-dir` 指到 `fixtures/fake-skills/`
# 的假 skill 上做（那些 fixture 就是为这件事存在的）。
# ★ 因此 `M43` 的前置锚**只准写语义、不准写普查字面量**（复审 Important-1）：真仓的族数是
# **会变的**（M3 的下一步就把那几个 skill 建出来），锚写死那天就是无端 RED-BAD。
#
# ★ 假 skill 的目录名带**家族前缀**（`mcm-plot-ok` / `mcm-plot-nopointer` / `mcm-plot-restate`）：
# 任务书原文给的三个目录名是 `fake-ok` / `fake-nopointer` / `fake-restate`，但规则①②的**射程**
# 是"名字匹配绘图家族"（差异 2/5）⇒ 叫 `fake-*` 的样本**根本不在射程内**，那样 M43 会绿、
# M44 也证不到"家族 ≥1 且全绿"这条路径。三条角色（带指针 / 缺指针 / 重述数值）照原样，只加前缀。
#
# ★★ `mcm-table` / `mcm-schematic` 两份（复审 Minor-3）：`FAMILY_RE` 有**三条**备选，
# 而 `mcm-plot-*` 那三份只压得住第一条 ⇒ 后两条**删掉也不会红**（"声明了但没被任何变异证明"
# 的判据腿）。修法**不是**放一份干净的同名样例 —— 那样删掉备选它只是**掉出射程**，
# `M43` 的交叉断言一字不变 ⇒ 照样 RED-OK，腿仍然没被证。故放**在射程内且脏**的两份：
# 各缺 `references/house-style.md` 指针 ⇒ `M43` 必须**分别点名** `K2@mcm-table` /
# `K2@mcm-schematic` ⇒ 删掉任一条备选，对应那条预期红当即消失 ⇒ `M43` 转 RED-BAD。
PTR_CHK = HERE / "check-spec-pointers.py"
FAKE_SKILLS = FIX / "fake-skills"
PTR_OK = "mcm-plot-ok"                    # 合格的那份（含指针、无数值）
PTR_NOPOINTER = "mcm-plot-nopointer"      # 缺指针的那份
PTR_RESTATE = "mcm-plot-restate"          # 重述数值的那份
PTR_TABLE = "mcm-table"                   # 家族正则备选②：在射程内、缺指针
PTR_SCHEMATIC = "mcm-schematic"           # 家族正则备选③：在射程内、缺指针
PTR_MUT45 = HERE / "check-house-style.__mut45__.py"   # `M45` 的副本名（**必须同目录**，见那条）


def pointer_run(skills_dir=None, checker=None):
    """跑引用完整性检查器：`--skills-dir` 换被扫的根、`--checker` 换提供 `K2`/`K3` 的检查器。"""
    cmd = [sys.executable, str(PTR_CHK)]
    if skills_dir is not None:
        cmd += ["--skills-dir", str(skills_dir)]
    if checker is not None:
        cmd += ["--checker", str(checker)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout, p.stderr


def _ptr_result(out):
    """取末行 `RESULT: …`（没有就说明它没判）。"""
    return next((l for l in out.splitlines() if l.startswith("RESULT")), "（缺 RESULT 行）")


def _ptr_scanned(out, default="?"):
    """取普查行的 `扫到 N 个 skill` —— **当场从输出里读**，不写死字面量（复审 Important-1 的同一条理由：
    这两个数都会变：真仓那边 `M3` 的下一步就要建家族 skill，假 skill 那边本轮的 fixture 数也变过）。"""
    m = re.search(r"扫到 (\d+) 个 skill", out)
    return m.group(1) if m else default


def _ptr_families(out, default="?"):
    """取普查行的 `绘图家族 N 个` —— 同 `_ptr_scanned()`：**当场从输出里读**，不写死字面量
    （真仓家族数会随绘图 skill 落地而变；`M45` 判词里那句『真仓 N 个家族』必须跟着走，
    否则家族一落地，出货证据里就印着"真仓 0 个家族"这种被事实证伪的硬编码）。"""
    m = re.search(r"绘图家族 (\d+) 个", out)
    return m.group(1) if m else default


def m43_ptr():
    """`M43`：整体跑假 skill 目录 ⇒ 缺指针的与重述数值的**必须分别点名**，且**四条**各打各的。

    断言故意写成"**各打各的**"：不只是"反正红了"。只看"红了"的话，随便哪一份坏就够红两次，
    另一条规则拆掉也看不出来 ⇒ 这条同时是"`K2` 与 `K3` 两条各自承重"的证明。

    四条 = `K2@mcm-plot-nopointer` · `K3@mcm-plot-restate` · `K2@mcm-table` · `K2@mcm-schematic`。
    后两条（复审 Minor-3）压的是 `FAMILY_RE` 里**另外两条备选** —— 只放 `mcm-plot-*` 的话，
    把 `|mcm-table` / `|mcm-schematic` 从正则里删掉也不会红，那两条备选就只是"声明"。

    前置锚在真仓：它必须**跑到并判绿**（有 `RESULT` 行且不是 PASS 之外的、且一行 `FAIL` 都没有）
    —— 否则"改坏了才红"这条断言在"它本来就是红的"时也会通过（同 `M2` 的 R-6 那条教训）。
    ★ **前置锚不许写普查字面量**（复审 Important-1）：原来锚的是
    `RESULT: PASS (无对象：扫到 5 个 skill，绘图家族 0 个)` —— 那是**真仓那天的读数**。
    `M3` 的下一步就把那 5 个绘图 skill 建出来，届时默认运行印的是『绘图家族 5 个，…』
    ⇒ 字面量当场失配、`M43` 无端报 RED-BAD。而本器**恰恰是故意**设计成"家族 skill 一落地
    即自动纳入"的 —— 驱动器那行锚跟它对着干。现在锚的是**语义**。
    ⚠️ **不许再弱化成 `rc0 == 0`**：那会让"检查器没跑起来但退出码正常"也算过。
    """
    rc0, out0, _e0 = pointer_run()
    rc1, out1, _e1 = pointer_run(skills_dir=FAKE_SKILLS)
    res0 = _ptr_result(out0)
    pre_ok = (rc0 == 0 and res0.startswith("RESULT: PASS")
              and not [l for l in out0.splitlines() if l.startswith("FAIL")])
    f_k2 = f"FAIL  K2  {PTR_NOPOINTER}" in out1          # 缺指针 ⇒ K2 点名
    f_k3 = f"FAIL  K3  {PTR_RESTATE}" in out1            # 重述数值 ⇒ K3 点名
    f_k2_tb = f"FAIL  K2  {PTR_TABLE}" in out1           # 家族备选②缺指针 ⇒ K2 点名
    f_k2_sch = f"FAIL  K2  {PTR_SCHEMATIC}" in out1      # 家族备选③缺指针 ⇒ K2 点名
    g_k2_rs = f"PASS  K2  {PTR_RESTATE}" in out1         # 它**不该**由 K2 打（指针在）
    g_k3_np = f"PASS  K3  {PTR_NOPOINTER}" in out1       # 它**不该**由 K3 打（没写数值）
    g_ok = f"PASS  K2  {PTR_OK}" in out1 and f"PASS  K3  {PTR_OK}" in out1
    post_ok = (rc1 != 0 and f_k2 and f_k3 and f_k2_tb and f_k2_sch
               and g_k2_rs and g_k3_np and g_ok)
    n_fail = len([l for l in out1.splitlines() if l.startswith("FAIL  ")])
    return pre_ok and post_ok, (
        f"前置(真仓扫到 {_ptr_scanned(out0)} 个 skill) exit={rc0} 末行『{res0}』"
        f"{'绿：判到且无 FAIL 行' if pre_ok else '未绿 <<<'}；"
        f"后置(假 skill 目录扫到 {_ptr_scanned(out1)} 份) exit={rc1} 全目录共红 {n_fail} 条、"
        f"末行『{_ptr_result(out1)}』 —— "
        f"`{PTR_NOPOINTER}` 由 **K2** 点名={f_k2}、`{PTR_RESTATE}` 由 **K3** 点名={f_k3}、"
        f"`{PTR_TABLE}` 由 **K2** 点名={f_k2_tb}、`{PTR_SCHEMATIC}` 由 **K2** 点名={f_k2_sch}；"
        f"NOTE/两条规则**各打各的**（另四格全绿）：K3@{PTR_NOPOINTER}={g_k3_np} · "
        f"K2@{PTR_RESTATE}={g_k2_rs} · `{PTR_OK}` 两格={g_ok}")


def m44_ptr():
    """`M44`：只留**合格的那一份**再跑 ⇒ 必须**绿**（**本组唯一**能证"这个检查器不是恒 FAIL"的一条）。

    一个恒 FAIL 的检查器照样能让 `M43` 变红 ⇒ 没有这一条，`M43` 的"红"证明不了任何事。
    做法：把 `mcm-plot-ok` 复制进一个**临时根**再跑 —— 真件不碰、也不在仓里留第二份会漂的副本。
    """
    src_ok = FAKE_SKILLS / PTR_OK / "SKILL.md"
    if not src_ok.is_file():
        raise AssertionError(f"缺 fixture：{src_ok}（前提不成立）")
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / PTR_OK).mkdir()
        (tmp / PTR_OK / "SKILL.md").write_bytes(src_ok.read_bytes())   # write_bytes：不用 write_text
        rc, out, _e = pointer_run(skills_dir=tmp)
    k2 = f"PASS  K2  {PTR_OK}" in out
    k3 = f"PASS  K3  {PTR_OK}" in out
    ok = rc == 0 and k2 and k3 and "RESULT: PASS" in out
    return ok, (f"只留 `{PTR_OK}`（临时根，真件不碰；目录名**逐字**打出来自证人不在赌路径）exit={rc} "
                f"K2={'PASS' if k2 else '未绿 <<<'}、K3={'PASS' if k3 else '未绿 <<<'}、"
                f"末行『{_ptr_result(out)}』 ⇒ 这个检查器**不是恒 FAIL**")


def m45_ptr():
    """`M45`：把 `check-house-style.py` 抽数的**正则改坏** ⇒ 仪器取不到参照物 ⇒ fail-closed 红。

    做法：把检查器复制到**同目录**下（副本要能 `_load` 同目录的 `house-metrics.py` /
    `check-figure-style.py`，且 `parents[3]` 仍指到仓根），把 `_k3` 主臂的**三族参照物全改到抽不出**：
      · 小数族：`k3_reference()` 里那句 `re.findall(r"\\d+\\.\\d+", doc)` → `\\d{9}`；
      · 两个阈值值池：`SK_CN_TIER_RES` **整条语句**换成打不中的形态（`r"\\d{9}"`）⇒
        由它现分的上界 / 下界两族一起空（`_tier_split()` 是现分的，改一处两族都塌）。
    为什么都要改（M3-T1 修 K3 主臂后**必须跟着改**，这是本条与检查器的耦合点）：三族**任一为空**
    就记红（fail-closed），只改小数族也能红 —— 但那样证不到"阈值值池这一族也真的承重"，
    故三族一起改坏，让空集是真空集（同 `M35`/`M36` 各证一道臂的道理）。
    跑的时候**故意用真仓**：**全局仪器探针**自身 fail-closed ⇒ 哪怕该轮没有逐份对象也会红
    （真仓有没有绘图家族都是这样；有家族时逐份判据照跑，探针那条仍单独承重）
    —— 这才证得到"仪器坏了、哪怕无对象也会红"。
    """
    src = HOUSE_CHK.read_bytes().decode("utf-8")
    old = '    dec = set(re.findall(r"\\d+\\.\\d+", doc))'
    n_hit = src.count(old)
    if n_hit != 1:
        raise AssertionError(f"`check-house-style.py` 的小数抽数那一行命中 {n_hit} 次（必须恰 1）"
                             f"—— 检查器漂了，这条变异要跟着改")
    # 整条 `SK_CN_TIER_RES = (...)` 语句（行长不定：按**括号配平**取，不写死它的换行与缩进）
    lines = src.splitlines(keepends=True)
    i = next((k for k, l in enumerate(lines) if l.startswith("SK_CN_TIER_RES = (")), None)
    if i is None:
        raise AssertionError("`SK_CN_TIER_RES = (` 这一行找不到 —— 检查器漂了，这条变异要跟着改")
    j = next((k for k in range(i, len(lines)) if lines[k].rstrip().endswith(")")), None)
    if j is None:
        raise AssertionError("`SK_CN_TIER_RES` 语句的收尾行找不到（括号没配平？）")
    mut = src.replace(old, '    dec = set(re.findall(r"\\d+\\.\\d{9}", doc))  # 变异：小数抽不到', 1)
    mut = "".join(mut.splitlines(keepends=True)[:i]) \
        + 'SK_CN_TIER_RES = (r"\\d{9}",)   # 变异：六个标记全改坏（两族值池一起抽到空集）\n' \
        + "".join(mut.splitlines(keepends=True)[j + 1:])
    if mut == src:
        raise AssertionError("变异体与原文相同（没改到？）")
    rc_b, out_b, _eb = pointer_run(checker=HOUSE_CHK)
    try:
        PTR_MUT45.write_bytes(mut.encode("utf-8"))                        # write_bytes：不用 write_text
        rc_a, out_a, _ea = pointer_run(checker=PTR_MUT45)
    finally:
        PTR_MUT45.unlink(missing_ok=True)          # 副本不属于交付物，跑完必须消失（同一目录也是纪律）
    pre_ok = rc_b == 0 and "PASS  INSTR" in out_b
    post_ok = rc_a != 0 and "FAIL  INSTR" in out_a
    line = next((l for l in out_a.splitlines() if l.startswith("FAIL  INSTR")), "（缺 FAIL 行）")
    n_red = len([l for l in out_a.splitlines() if l.startswith("FAIL  ")])
    fam = _ptr_families(out_a)                    # 真仓家族数**当场从输出现读**（家族落地就会变）
    n_skill_red = len([l for l in out_a.splitlines()   # 除仪器探针外的逐份判据红 —— 也是现算
                       if l.startswith("FAIL  ") and "INSTR" not in l])
    return pre_ok and post_ok, (
        f"前置(真检查器) exit={rc_b} {'仪器探针绿' if pre_ok else '未绿 <<<'}；"
        f"后置(副本三族参照物全改坏) exit={rc_a} 『{line[:96]}…』、全跑共红 {n_red} 条"
        f"（真仓 {fam} 个家族 ⇒ 除仪器探针外逐份判据红 {n_skill_red} 条）、"
        f"末行『{_ptr_result(out_a)}』"
        f"　NOTE/副本已删：{not PTR_MUT45.exists()}")


def m46_ptr():
    """`M46`：`--skills-dir` 指向**坏目录** ⇒ 必须非零退出（fail-closed 的**两个分支**）。

    分支 a：目录**不存在**；分支 b：目录存在但**一个 `*/SKILL.md` 都没有**。
    两条都是"扫不到东西"，但走的是两条不同的代码路径（`is_dir()` 与 `len(rows)==0`），
    故两个都要证。两条都**不许**打出 `RESULT: PASS`。
    """
    miss = FIX / "fake-skills-does-not-exist"
    if miss.exists():
        raise AssertionError(f"{miss} 居然存在（这条变异的前提不成立）")
    rc_a, out_a, err_a = pointer_run(skills_dir=miss)
    with tempfile.TemporaryDirectory() as d:
        rc_b, out_b, err_b = pointer_run(skills_dir=Path(d))
    a_ok = rc_a != 0 and "RESULT: PASS" not in out_a + err_a
    b_ok = rc_b != 0 and "RESULT: PASS" not in out_b + err_b
    a_line = next((l for l in out_a.splitlines() if l.startswith("FAIL")), "（缺 FAIL 行）")
    b_line = next((l for l in out_b.splitlines() if l.startswith("FAIL")), "（缺 FAIL 行）")
    return a_ok and b_ok, (
        f"分支 a(目录不存在) exit={rc_a} 『{a_line[:72]}…』；"
        f"分支 b(目录在、一个 `SKILL.md` 都没有) exit={rc_b} 『{b_line[:72]}…』；"
        f"两分支都没有 `RESULT: PASS`={a_ok and b_ok}")


def run_pointer():
    """跑 `M43`–`M46` 四条。返回 `(rows, failed, 本组条数)`。"""
    rows, failed = [], []
    for mid, desc, fn in (
        ("M43", f"引用完整性：整体跑 `fixtures/fake-skills/` ⇒ `{PTR_NOPOINTER}` 缺指针由 **K2** 点名、"
                f"`{PTR_RESTATE}` 重述数值由 **K3** 点名，家族正则另外两条备选（`{PTR_TABLE}` / "
                f"`{PTR_SCHEMATIC}`）缺指针也**各自**由 **K2** 点名（四条各打各的）", m43_ptr),
        ("M44", f"引用完整性：只留 `{PTR_OK}` 再跑 ⇒ **绿**"
                f"（本组唯一能证这个检查器不是恒 FAIL 的一条）", m44_ptr),
        ("M45", "check-house-style.py：把 `_k3` 抽参照物的**三族全改坏**（小数正则 + "
                "`SK_CN_TIER_RES` 整条 ⇒ 两族值池一起空）⇒ **仪器探针** `FAIL  INSTR K3@空串` "
                "⇒ fail-closed 红（打真仓：全局仪器探针自身 fail-closed —— 哪怕该轮没有逐份对象，"
                "它照样承重）", m45_ptr),
        ("M46", "引用完整性：`--skills-dir` 指向坏目录 ⇒ 非零退出"
                "（分支 a 目录不存在 · 分支 b 目录在但一个 `SKILL.md` 都没有）", m46_ptr),
    ):
        try:
            ok, detail = fn()
        except AssertionError as e:                                 # noqa: BLE001（驱动器自己的出口）
            ok, detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
    return rows, failed, len(rows)


# ========================================== `K3` 的 ASCII **阈值标记臂**（M3-T1）的变异（`M47`–`M53`）
# 打的是 `check-house-style.py` 的 `_k3` **主臂**（被验对象 = `mcm-figure-choose/SKILL.md` 的副本）。
#
# 为什么从 **`M47`** 起：`M1`–`M8`（检查器）· `M9`–`M19` + `C1`/`C2`（规范数）· `M22`–`M28`
# （`chart-types.md` 结构）· `M29`–`M41`（`SKILL.md` 短契约）· `M43`–`M46`（引用完整性检查器）
# 已占号；任务书给的 `M17`–`M20` 与上面**撞号**，撞号的变异表会让"哪条红了"没法引用
# （同 Task 3 顺延 `M9`、Task 5 顺延 `M29`、Task 7 顺延 `M43` 那三次），故本组顺延 `M47` 起。
#
# 为什么这七条**必须**存在：`K3` 主臂原先只认 `\d+\.\d+` 与 `≤n` / `<n 词`，而 `H12` 的规范值
# 恰恰写的就是 **`≥7 pt`** ⇒ `≥n` / `上限 n` / `不超过 n` 这一整族重述**全走绿**。
# `M47`–`M49` + `M51`–`M53` 让**六个标记各有一条真红**（每条由 NOTE 现算证明红的是阈值标记臂
# 本身）—— 只证其中几个的话，"六个标记都在射程内"就是一句**声明比事实大**的话
# （本仓栽过多次；同 Task 7 复审 Minor-3 那条"声明了但没被任何变异证明"的判据腿）。
# `M50` 是**射程边界对照**（`主色 4 个` 这类无标记裸整数必须**仍绿**）—— 它证的是
# "这条臂没有偷偷扩到乱红"：谁哪天把裸值臂加了回来，`M50` 立刻 RED-BAD。
#
# ★ 修复轮（复审 Important-1）：补 **`M53`**（`≤n` 腿的**专属真红**）。原句"六个标记各有一条真红"
#   当时只有 **5** 条专属变异 —— `≤` 那腿被误引到 `M34` 的既有路径上，而 `M34` 的红来自**小数族
#   抽空**（后置读数「小数 0 条」），与 `≤` 无关 ⇒ 声明比事实大。补 `M53` 后声明成真。
#   **编号顺延 `M53`**（不插号、不改既有号）：本组 `M47`–`M52` 已在 5 份入库证据件与报告里被引用，
#   插号会让那些引用全部失准 —— 与上面"为什么从 `M47` 起"（`M9`/`M29`/`M43` 三次顺延）同一理由。
#
# ★ 两条反面对照（**必须绿**，由 `M50` 的兄弟断言覆盖在 `m50_tier_boundary` 的扩展里）：
#   `下限 4`（值在**另一个方向**的池里）与 `< 25 词`（值不在任何池里）**都不该红** ——
#   这才是"方向纪律"的下半句：跨方向**不算**重述（否则 `mcm-abstract` 的 `≥12pt` 会被假红）。

TIER_INSERTS = (
    ("M47", "≥7 pt", "`H12` 的规范值**原话**（生成器现取自 `house-style.md`：`≥7`）"),
    ("M48", "上限 4", "**跨标记、同方向**：规范写的是 `≤4`，`上限 4` 是同一个阈值的重述"),
    ("M49", "不超过 12 词", "`不超过 n` 这一族（规范里是 `不超过 17 词`，值池按方向共享）"),
    ("M51", "字号下限 7 pt", "`下限 n` 这一族（下界方向；值 `7` 现取自规范里的 `≥7`）"),
    ("M52", "图注 < 12 词", "`<n 词` 这一族（上界方向；值 `12` 现取自规范里的 `上限 12 词`）"),
    ("M53", "图注 ≤12 词", "`≤n` 这一族**本尊**（上界方向；值 `12` 现取自规范里的 `上限 12 词`）—— "
                         "规范**原话**是 `≤4`/`≤3`，旧臂逐字也只认这两个 ⇒ `≤12` 是值池化后**新增**的"
                         "射程、旧臂抓不到"),
)

# `M50` 的**边界对照**用例：插进 SKILL.md 后 `K3` 必须**仍绿**（每一组里第一条是主用例，
# 其余是"跨方向 / 不在池里"的反面对照——它们证的是方向纪律没被写成"见数就红"）。
TIER_GREEN = (
    ("主色 4 个", "**无标记裸整数** ⇒ 不在射程内（判它就得判『出现 `4` 就红』）"),
    ("下限 4", "值 `4` 在**另一个方向**的池里（它是 `≤4` 的值）⇒ 跨方向**不算**重述"),
    ("< 25 词", "值 `25` **不在任何池里**（规范里没有 25 这个词数）⇒ 不是重述"),
)


def _k3_line(out):
    """从 `--only K3` 的输出里取 `PASS/FAIL  K3` 那一行的**读数正文**（现算，不写死）。"""
    line = next((l for l in out.splitlines() if l.startswith(("PASS  K3", "FAIL  K3"))), "")
    return line.split(None, 2)[-1] if line else "（缺 K3 行）"


def _tier_probe(_txt):
    """`M47`–`M49`/`M51`–`M53` 的现算 NOTE：红的是**阈值标记臂**（不是小数臂、也不是中文数词臂）。

    读的是同一副本上 `K3` 印出的那一行 —— 命中串里必须出现**带标记的字面**（`≥7` / `上限 4` /
    `不超过 12`）；只出现小数的话，这条变异就没打在目标臂上。
    """
    _rc, out = skill_run(HOUSE_CHK, HMUTD / "SKILL.md", ["K3"])
    m = re.search(r"命中 (\[[^\]]*\]|无)", _k3_line(out))
    return (f"NOTE/同副本 `K3` 的『命中』= {m.group(1) if m else '?'}"
            f"（**带标记的字面** ⇒ 打在阈值标记臂上）")


def m50_tier_boundary():
    """`M50`：**射程边界对照组** —— 三种"不该红"的写法下 `K3` 必须**仍绿**（逐一插进副本试）。

    为什么这是**对照**而不是判据变异：`K3` 的主臂只认小数与六个阈值标记，判不了"数字不配标记
    直接甩出来"；要判它就得退化成"文档里出现 `4` 就红"，而规范里的 `0`/`2`/`3`/`4`/`7`/`12`/
    `17`/`20`/`100` 会在**任何普通句子**里误红（看着能红、实则乱红）。故这条边界**写实登记在
    `_k3` 的 docstring 里**，并由本对照**常驻守住**。

    三例（`TIER_GREEN`）：① `主色 4 个`（无标记裸整数）；② `下限 4`（值在**另一个方向**的池里
    ⇒ 跨方向不算重述 —— 这正是 `mcm-abstract` 的 `≥12pt` 不被假红的那条规矩）；③ `< 25 词`
    （值不在任何池里）。谁哪天把臂写成"见数就红"，这三条里至少一条立刻 RED-BAD。

    断言：① 原件 `K3` 绿；② **三例逐个**插进去之后**都仍绿**。
    """
    text0 = SKILL_MD.read_bytes().decode("utf-8")
    mp = HMUTD / "SKILL.md"
    rc_b, out_b = skill_run(HOUSE_CHK, SKILL_MD, ["K3"])
    pre_ok = rc_b == 0 and "PASS  K3 " in out_b
    parts, ok_all = [], pre_ok
    for lit, why in TIER_GREEN:
        mp.write_bytes(sub_once(
            text0, TOP_ITEM,
            f"- **推荐图型**：给**一个首选**（{lit}）；").encode("utf-8"))   # write_bytes：不用 write_text
        rc_a, out_a = skill_run(HOUSE_CHK, mp, ["K3"])
        green = rc_a == 0 and "PASS  K3 " in out_a
        ok_all = ok_all and green
        parts.append(f"『{lit}』exit={rc_a} {'**仍绿** ✓' if green else '红了 <<< 越界乱红'}（{why}）")
    return ok_all, (f"前置(原件) exit={rc_b} {'K3 绿' if pre_ok else '未绿 <<<'}；"
                    + "；".join(parts))


def run_k3_tier():
    """跑 `M47`–`M53` 七条（6 条判据变异 + 1 条边界对照组）。返回 `(rows, failed, 本组条数)`。

    `M47`–`M53` 里除 `M50` 外都走 `skill_assert`（前置绿 / 后置由 `K3` 点名红，同 `M29` 的纪律）；
    `M50` 是反向对照组（**必须仍绿**），见 `m50_tier_boundary`。
    """
    rows, failed = [], []
    for mid, lit, why in TIER_INSERTS:
        desc = (f"SKILL.md：写进『{lit}』（{why}）⇒ `K3` **阈值标记臂**红（该族原先整族走绿）")
        try:
            ok, detail = skill_assert(
                desc, lambda t, s=lit: sub_once(
                    t, TOP_ITEM, f"- **推荐图型**：给**一个首选**（{s}）；"), ["K3"], _tier_probe)
        except AssertionError as e:                                 # noqa: BLE001（驱动器自己的出口）
            ok, detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
    desc50 = ("SKILL.md：写进三种**不该红**的写法（`主色 4 个` / `下限 4` / `< 25 词`）"
              "⇒ `K3` 必须**仍绿** —— 射程边界对照组（不是判据变异，同 `M44`："
              "它证「这条臂没扩到乱红」、且跨方向不算重述）")
    try:
        ok50, detail50 = m50_tier_boundary()
    except AssertionError as e:                                     # noqa: BLE001（驱动器自己的出口）
        ok50, detail50 = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    rows.append(("RED-OK" if ok50 else "RED-BAD", "M50", desc50, detail50))
    if not ok50:
        failed.append("M50")
    return rows, failed, len(rows)


def k3_fail_closed_mut():
    """`M34`：`K3` 的 **fail-closed 臂** —— 禁止串**一条都抽不到**时，这条判据必须红。

    做法：把**副本** `house-style.md` 里的小数字面量与 `≤n` 形态全抹掉（真件不碰），
    于是 `K3` 的"现取禁止串"抽到空集 —— 前置（真件）必须绿、后置必须红。
    不证这一臂的话，"抽不到即 FAIL"就只是注释里的一句话（本仓栽过的"判据恒绿"里，
    最常见的一类就是**仪器取不到参照物时默认放行**）。
    """
    src = HOUSE_DOC.read_bytes().decode("utf-8")
    mut = re.sub(r"\d+\.\d+", "□", src)
    mut = re.sub(r"≤\s*\d+", "□", mut)
    mut = re.sub(r"<\s*\d+\s*词", "□", mut)
    if mut == src:
        raise AssertionError("变异体与原文相同（一条都改不动？）")
    mp = HMUTD / "house-style.md"
    mp.write_bytes(mut.encode("utf-8"))                      # write_bytes：不用 write_text

    def run(doc):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--doc", str(doc),
                            "--skill", str(SKILL_MD), "--only", "K3"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    rc_b, out_b = run(HOUSE_DOC)
    rc_a, out_a = run(mp)
    left = len(set(re.findall(r"\d+\.\d+", mut)) | set(re.findall(r"≤\s*\d+", mut)))
    pre_ok = rc_b == 0 and "PASS  K3 " in out_b
    post_ok = rc_a != 0 and "FAIL  K3 " in out_a and "fail-closed" in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K3")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (f"前置(真件) exit={rc_b} {'K3 绿' if pre_ok else '未绿 <<<'}；"
                                f"后置(副本抹掉小数与 `≤n`) exit={rc_a} 『{line}』"
                                f"（副本里剩下的禁止串 {left} 条）")


def s4_readout_probe():
    """`R1`：证 `S4` 是**读数条**（不是判据）—— 改坏副本上**读数会动**、**判词不动**。

    两条断言（缺一条这个"读数条"就是坏的）：
      ① 原件 `--only S4`：rc=0、出现 `READ  S4`、**不出现** `PASS  S4` / `FAIL  S4`；
      ② 把 `bar chart` 的定义**复制成两份**（真的制造一次重名）后：rc **仍为 0**（它不判红），
         而读数里的 `重名` 字段**必须变**（它真在读那份文档）。
    """
    rc0, out0 = struct_run(HOUSE_CHK, CT_DOC, ["S4"])
    read_line = next((l for l in out0.splitlines() if l.startswith("READ  S4")), "")
    n0 = re.search(r"定义行 (\d+)", read_line)
    dup0 = re.search(r"重名 ([^（]*)（", read_line)
    text = CT_DOC.read_bytes().decode("utf-8")
    line = next(l for l in text.splitlines() if l.startswith("**bar chart**:"))
    mp = HMUTD / "chart-types.md"
    mp.write_bytes((text.replace(line, line + "\n" + line, 1)).encode("utf-8"))
    rc1, out1 = struct_run(HOUSE_CHK, mp, ["S4"])
    read_line1 = next((l for l in out1.splitlines() if l.startswith("READ  S4")), "")
    n1 = re.search(r"定义行 (\d+)", read_line1)
    dup1 = re.search(r"重名 ([^（]*)（", read_line1)
    clean = (rc0 == 0 and bool(read_line) and "PASS  S4" not in out0 and "FAIL  S4" not in out0)
    moved = (rc1 == 0 and n0 and n1 and int(n1.group(1)) == int(n0.group(1)) + 1
             and dup1 and "bar chart" in dup1.group(1))
    def _body(l):
        return l.split(None, 2)[-1] if len(l.split(None, 2)) == 3 else l

    return clean and moved, (
        f"原件 `--only S4` exit={rc0} 『{_body(read_line) if read_line else '(缺 READ 行) <<<'}』"
        f"（无 PASS/FAIL 判词）　"
        f"把 `bar chart` 定义复制一份后 exit={rc1} 『{(dup1.group(1).strip() if dup1 else '?')}』"
        f"⇒ 读数从 {n0.group(1) if n0 else '?'} 行涨到 {n1.group(1) if n1 else '?'} 行、"
        f"重名被点出，而 **rc 仍为 0**（读数条只读不判；一个判据做不到这点）")


# ---------------------------------------------------------------- CENSUS 的变异（Important-2）
# 为什么单列一组：M9–M19 全走 `--only <id>`，而 CENSUS 只在**不带 `--only`** 时才跑
# （`if not want:`）⇒ 上面那些变异**一条都没验过 CENSUS**。这组故意不带 `--only`。
CENSUS_MUTATIONS = [
    ("C1", "往 house-style.md 末尾**加一句带整数的话**（『共 37 条断言，其中 6 条为社区条目。』）",
     "doc", "数 ①（`G-H13-band`）\n", "数 ①（`G-H13-band`）\n\n共 37 条断言，其中 6 条为社区条目。\n"),
    ("C2", "把仪器实现常量 `quantize(32, MEDIANCUT)` 改成 `quantize(99, MEDIANCUT)`"
            "（上下文豁免表不能是万能兜底）",
     "doc", "quantize(32, MEDIANCUT)", "quantize(99, MEDIANCUT)"),
]


def house_census_run(doc, prov):
    """**不带 `--only`** 跑一遍（CENSUS 才会参与）；`--no-provenance` 只为省掉 46 次子进程。"""
    cmd = [sys.executable, str(HOUSE_CHK), "--doc", str(doc), "--prov", str(prov), "--no-provenance"]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    census = [l for l in p.stdout.splitlines() if l.startswith("CENSUS")]
    return p.returncode, p.stdout, (census[0] if census else "(没有 CENSUS 行)")


def run_census_mutations():
    """`C1`/`C2` 两条：改坏副本必须让 rc≠0 **且** CENSUS 报『未入理由表』≥1。"""
    rows, failed = [], []
    for mid, desc, target, old, new in CENSUS_MUTATIONS:
        src = (HOUSE_DOC if target == "doc" else HOUSE_PROV).read_bytes()
        if src.decode("utf-8").count(old) != 1:
            print(f"RED-BAD  {mid}  原文串命中 != 1——驱动器自己报错")
            failed.append(mid)
            continue
        mp = HMUTD / ("census.house-style.md" if target == "doc" else "census.provenance.md")
        mp.write_bytes(src.decode("utf-8").replace(old, new, 1).encode("utf-8"))
        rc_b, out_b, cen_b = house_census_run(HOUSE_DOC, HOUSE_PROV)
        rc_a, out_a, cen_a = house_census_run(mp if target == "doc" else HOUSE_DOC,
                                              mp if target == "prov" else HOUSE_PROV)
        m = re.search(r"未入理由表 (\d+) 个", cen_a)
        n_unlisted = int(m.group(1)) if m else -1
        pre_ok = rc_b == 0 and "未入理由表 0 个" in cen_b
        post_ok = rc_a != 0 and n_unlisted >= 1
        detail = (f"前置(原件) exit={rc_b} 『{(cens := cen_b.split('·')[-1].strip())}』；"
                  f"后置(改坏) exit={rc_a} 未入理由表 {n_unlisted} 个 ⇒ "
                  f"{'CENSUS 当场点了出来' if post_ok else '未达预期 <<<'}")
        rows.append(("RED-OK" if (pre_ok and post_ok) else "RED-BAD", mid, desc, detail))
        if not (pre_ok and post_ok):
            failed.append(mid)
    for f in HMUTD.glob("census.*"):
        f.unlink()
    return rows, failed


def run_house():
    """跑完整组（规范数守卫 M9–M19 + CENSUS C1/C2 + 结构守卫 M22–M26 + 读数条探针 R1）。

    返回 `(rows, failed, 自证 ok, 分组条数)`；`rows` 里 `mid == "R1"` 的那条是**探针**不是判据变异。
    """
    doc_hash, prov_hash = git_hash_object(HOUSE_DOC), git_hash_object(HOUSE_PROV)
    ct_hash = git_hash_object(CT_DOC)
    skill_hash = git_hash_object(SKILL_MD)
    HMUTD.mkdir(exist_ok=True)
    rows, failed = [], []
    f_house, f_census, f_struct = [], [], []
    n_house = 0
    for mid, desc, target, old, new, ids in house_mutations():
        n_house += 1
        try:
            ok, detail = house_assert(desc, HOUSE_DOC, HOUSE_PROV, old, new, target, ids)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            f_house.append(mid)
            continue
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            f_house.append(mid)
    # CENSUS 那两条**必须**在清空 `_mut-house/` 之前跑（它们要写自己的变异副本）
    crows, cfailed = run_census_mutations()
    rows += crows
    failed += cfailed
    f_census += cfailed
    n_census = len(crows)

    # ---- 结构守卫（Task 4）：`chart-types.md`
    srows, sfailed = [], []
    for mid, desc, edits, ids, probe in struct_mutations():
        try:
            ok, detail = ct_assert(desc, edits, ids, probe)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            f_struct.append(mid)
            continue
        srows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            f_struct.append(mid)

    # ---- 读数条探针（不是判据变异）：`S4` 只读不判
    try:
        r_ok, r_detail = s4_readout_probe()
    except (AssertionError, StopIteration) as e:                 # noqa: BLE001（驱动器自己的出口）
        r_ok, r_detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    probe_row = ("RED-OK" if r_ok else "RED-BAD", "R1",
                 "读数条 `S4`：该动的时候动、该判的时候不判", r_detail)
    if not r_ok:
        failed.append("R1")

    # ---- SKILL 守卫（Task 5）：`SKILL.md` 的短契约
    krows, kfailed = [], []
    for mid, desc, transform, ids, probe in skill_mutations():
        try:
            ok, detail = skill_assert(desc, transform, ids, probe)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            kfailed.append(mid)
            continue
        krows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            kfailed.append(mid)

    # ---- `M34`：`K3` 的 fail-closed 臂（打的是 `house-style.md` 的副本，不是 SKILL.md）
    try:
        k34_ok, k34_detail = k3_fail_closed_mut()
    except AssertionError as e:
        k34_ok, k34_detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    krows.append(("RED-OK" if k34_ok else "RED-BAD", "M34",
                  "house-style.md：小数字面量与 `≤n` 全抹掉 ⇒ `K3` 抽不到禁止串 ⇒ fail-closed 红",
                  k34_detail))
    if not k34_ok:
        failed.append("M34")
        kfailed.append("M34")

    # ---- `M33`/`M40`：`K6` 的两个臂（**自造〔拟建〕场景**，真件不碰、也不依赖真仓是否还有待建 skill）
    # ---- `M41`：`K8`（打的是 `house-style.md` 的副本，真件不碰）
    # 跑 `M33`/`M40` 前后各快照一次真 skills 根的路径集合：`byte_ok` 用它证"没往真根里写东西"
    # （原先借"真仓里反正没有 mcm-plot-python"当代理，该 skill 一建出就恒假 —— 见 `_skills_tree`）。
    skills_tree_before = _skills_tree()
    for mid, desc, fn in (
        ("M33", "SKILL.md：副本里**注入**一行 `mcm-plot-pending`（〔拟建〕）再**摘掉其标记** ⇒ "
                "点名不存在的 skill 却不标 ⇒ `K6` 红（正向臂 · 自造场景）", m33_pending_mut),
        ("M40", "SKILL.md：副本注入 `mcm-plot-pending`（〔拟建〕）、`--skills-root` 指到**建出它**的"
                "临时根 ⇒ 『标了却存在』⇒ `K6` 红（反向臂 · 自造场景）", k6_exists_mut),
        ("M41", "house-style.md：副本里抹掉某个 `H<n>` 的『**验证**：』行 ⇒ `K8` 红"
                "（`SKILL.md` 那句『逐条标了验证状态』要成立）", k8_verify_line_mut),
    ):
        try:
            ok_m, detail_m = fn()
        except AssertionError as e:
            ok_m, detail_m = False, f"驱动器自己报错：{type(e).__name__}: {e}"
        krows.append(("RED-OK" if ok_m else "RED-BAD", mid, desc, detail_m))
        if not ok_m:
            failed.append(mid)
            kfailed.append(mid)
    skills_tree_after = _skills_tree()

    # ---- 引用完整性检查器（Task 7）：`M43`–`M46`（打的是 `check-spec-pointers.py` + 假 skill）
    prows, pfailed, n_ptr = run_pointer()

    # ---- `K3` 的 ASCII 阈值标记臂（M3-T1）：`M47`–`M53`（打的是 SKILL.md 的副本）
    trows, tfailed, n_tier = run_k3_tier()

    rows += srows
    rows += prows
    failed += pfailed
    failed += tfailed
    for f in HMUTD.glob("*"):
        f.unlink()
    HMUTD.rmdir()
    clean = not HMUTD.exists()
    byte_ok = (HOUSE_DOC.read_bytes().decode("utf-8").count("**不超过 1.20×**") == 1
               and HOUSE_PROV.read_bytes().decode("utf-8").count("--metric h2_colw_p90_median") == 1
               and CT_DOC.read_bytes().decode("utf-8").count("### 入口 9 · 不确定性") == 1
               and SKILL_MD.read_bytes().decode("utf-8").count("- **推荐图型**：给**一个首选**；") == 1
               # `M40` 换的是 `--skills-root`，真 skills 根不该被碰：核它的路径集合在跑 `M40` 前后
               # **逐字相等**（旧写法借"真仓里反正没有 mcm-plot-python"当代理 —— 该 skill 自
               # M3-plot Task 2 起已真建出 ⇒ 那条代理恒假；这里换成**真测非侵入**，见 `_skills_tree`）
               and skills_tree_after == skills_tree_before
               # `M45` 写的是**同目录**的检查器副本（要能 import 兄弟脚本）⇒ 自证它已删干净
               and not PTR_MUT45.exists())
    same = (git_hash_object(HOUSE_DOC) == doc_hash and git_hash_object(HOUSE_PROV) == prov_hash
            and git_hash_object(CT_DOC) == ct_hash and git_hash_object(SKILL_MD) == skill_hash)
    print("\n" + "=" * 78)
    print(f"规范数守卫的变异（M9–M19 + C1/C2 · 打的是 house-style.md / provenance.md，共 {n_house + n_census} 条）")
    print("=" * 78)
    for st, mid, desc, detail in rows[:n_house + n_census]:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("\n" + "=" * 78)
    print(f"结构守卫的变异（M22–M28 · 打的是 chart-types.md，共 {len(srows)} 条）"
          f" + 读数条探针 R1")
    print("=" * 78)
    for st, mid, desc, detail in srows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("-" * 78)
    print(f"{probe_row[0]:<8} {probe_row[1]:<4} {probe_row[2]}")
    print(f"         {probe_row[3]}")
    print("\n" + "=" * 78)
    print(f"SKILL 守卫的变异（M29–M41 · 打的是 SKILL.md 的副本；M34/M41 打的是 house-style.md 的"
          f"副本、M33/M40 是**自造〔拟建〕场景**，共 {len(krows)} 条）")
    print("=" * 78)
    for st, mid, desc, detail in krows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("\n" + "=" * 78)
    print(f"引用完整性检查器的变异（M43–M46 · 打的是 check-spec-pointers.py；"
          f"`--skills-dir` 指 fixtures/fake-skills/ 与两个坏目录，共 {len(prows)} 条）")
    print("=" * 78)
    for st, mid, desc, detail in prows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("\n" + "=" * 78)
    print(f"`K3` ASCII 阈值标记臂的变异（M47–M53 · 打的是 SKILL.md 的副本；"
          f"其中 M47–M49/M51–M53 必须红、M50 是射程边界对照必须绿，共 {len(trows)} 条）")
    print("=" * 78)
    for st, mid, desc, detail in trows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print(f"还原自证  house-style.md blob {doc_hash} {'== 变异前' if same else '!= 变异前 <<<'}"
          f" · provenance.md blob {prov_hash} · chart-types.md blob {ct_hash}"
          f" · SKILL.md blob {skill_hash}"
          f" · 原件字面仍在: {byte_ok} · _mut-house/ 已清空: {clean}")
    return rows, failed, (clean and byte_ok and same), {
        "house": n_house, "census": n_census, "struct": len(srows), "skill": len(krows),
        "pointer": n_ptr, "tier": n_tier,
        "f_house": f_house, "f_census": f_census, "f_struct": f_struct, "f_skill": kfailed,
        "f_pointer": pfailed, "f_tier": tfailed,
        "probe_row": probe_row}


def mutate(src, old, new, out_path):
    """一次字面替换 → 写副本。命中数必须恰为 1，否则驱动器自己报错。"""
    n_hit = src.decode("utf-8").count(old)
    if n_hit != 1:
        raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）")
    mutated = src.decode("utf-8").replace(old, new, 1).encode("utf-8")
    assert mutated != src, "变异体与原文相同"
    out_path.write_bytes(mutated)               # write_bytes：不用 write_text（Windows CRLF）
    return mutated


def main():
    src = CHK.read_bytes()                      # 原始字节（全程不写回原文件）
    base_hash = git_hash_object(CHK)
    print("=" * 78)
    print("变异驱动器 · check-figure-style.py")
    print("=" * 78)
    print(f"原检查器 blob  {base_hash}")
    print(f"逐格验收基线  python fixtures/run-expected.py → exit ", end="")
    print(subprocess.run([sys.executable, str(FIX / "run-expected.py")],
                         capture_output=True, text=True).returncode)

    MUTD.mkdir(exist_ok=True)
    before = reader(CHK)
    failed, rows = [], []
    for mid, desc, old, new, fn in MUTATIONS:
        mp = MUTD / f"check-figure-style.{mid}.py"
        try:
            mutate(src, old, new, mp)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            continue
        after = reader(mp)
        ok, detail = fn(before, after, mp)
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)

    # ------------------------------------------------------------ 探针 P1
    pmid, pdesc, pold, pnew = PROBE
    pmp = MUTD / f"check-figure-style.{pmid}.py"
    probe_row = None
    try:
        mutate(src, pold, pnew, pmp)
        ok, detail = p1(pmp)
        probe_row = ("RED-OK" if ok else "RED-BAD", pmid, pdesc, detail)
        if not ok:
            failed.append(pmid)
    except AssertionError as e:
        print(f"RED-BAD  {pmid}  {e}——驱动器自己报错")
        failed.append(pmid)

    # ------------------------------------------------------------ mcm-schematic Task 2（A 族）
    srows, sfailed, s_probe = run_sch_mutations()
    failed += sfailed

    print("\n" + "=" * 78)
    print("逐条结果")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    if probe_row:
        print("-" * 78)
        print("变异探针（被打的不是判据，是验收脚本的 ERROR 分支）")
        print(f"{probe_row[0]:<8} {probe_row[1]:<4} {probe_row[2]}")
        print(f"         {probe_row[3]}")
    print("\n" + "=" * 78)
    print(f"`A` 族的变异（M59–M64 · 打的是检查器的 A1/A3/A4；`--schematic` 下以示意骨架为支点，"
          f"其中 M60/M64 是**必须仍绿**的射程边界对照）· 丢格探针 M65")
    print("=" * 78)
    for st, mid, desc, detail in srows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("-" * 78)
    print(f"{s_probe[0]:<8} {s_probe[1]:<4} {s_probe[2]}")
    print(f"         {s_probe[3]}")

    # ------------------------------------------------------------ 还原自证
    now_hash = git_hash_object(CHK)
    byte_ok = CHK.read_bytes() == src
    for f in MUTD.glob("*"):
        f.unlink()
    MUTD.rmdir()
    clean = not MUTD.exists()
    rerun = subprocess.run([sys.executable, str(FIX / "run-expected.py")], capture_output=True, text=True)

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    print(f"  check-figure-style.py  blob  {now_hash}  {'== 变异前' if now_hash == base_hash else '!= 变异前 <<<'}")
    print(f"  工作树字节 == 变异前字节: {byte_ok}")
    print(f"  fixtures/_mut/ 已清空: {clean}")
    print(f"  还原后复跑逐格验收: exit={rerun.returncode}  {rerun.stdout.strip().splitlines()[-1]}")
    n_probe = 1 if probe_row else 0
    mut_failed = [m for m in failed if m != pmid]
    probe_ok = bool(probe_row) and probe_row[0] == "RED-OK"

    rows_h, failed_h, selfok_h, grp = run_house()

    # `rows_h` 里含探针 R1 那条（不是判据变异）⇒ 统计时单列
    n_spec = grp["house"] + grp["census"]                 # M9–M19 + C1/C2
    n_struct = grp["struct"]                              # M22–M28
    n_skill = grp["skill"]                                # M29–M39（+ M34/M40/M41）
    n_ptr = grp["pointer"]                                # M43–M46
    n_tier = grp["tier"]                                  # M47–M53（其中 M50 是必须绿的对照）
    n_spec_ok = n_spec - len(grp["f_house"]) - len(grp["f_census"])
    n_struct_ok = n_struct - len(grp["f_struct"])
    n_skill_ok = n_skill - len(grp["f_skill"])
    n_ptr_ok = n_ptr - len(grp["f_pointer"])
    n_tier_ok = n_tier - len(grp["f_tier"])
    r1_ok = grp["probe_row"][0] == "RED-OK"

    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {len(rows) - len(mut_failed)}/{len(MUTATIONS)} 红（check-figure-style.py）"
          + ("" if not mut_failed else f"（未达预期：{', '.join(mut_failed)}）"))
    print(f"MUT: {n_spec_ok}/{n_spec} 红（house-style.md / provenance.md 的规范数守卫："
          f"{grp['house']} 条 `--only` + {grp['census']} 条 CENSUS 全跑）"
          + ("" if not (grp["f_house"] + grp["f_census"])
             else f"（未达预期：{', '.join(grp['f_house'] + grp['f_census'])}）"))
    print(f"MUT: {n_struct_ok}/{n_struct} 红（chart-types.md 的结构守卫 S1/S2/S3/S5：{n_struct} 条 `--only`）"
          + ("" if not grp["f_struct"] else f"（未达预期：{', '.join(grp['f_struct'])}）"))
    n_skill_copy = len(skill_mutations())                 # 打 SKILL.md 副本的那几条
    print(f"MUT: {n_skill_ok}/{n_skill} 红（SKILL.md 的短契约守卫 K1–K8：{n_skill} 条"
          f"（{n_skill_copy} 条打 SKILL.md 副本 + {n_skill - n_skill_copy} 条打别的："
          f"`K3` fail-closed 臂 / `K6` 的**两个臂**（M33 正向 · M40 反向，均为自造场景）/ `K8`））"
          + ("" if not grp["f_skill"] else f"（未达预期：{', '.join(grp['f_skill'])}）"))
    print(f"MUT: {n_ptr_ok}/{n_ptr} 红（引用完整性检查器 check-spec-pointers.py："
          f"`--skills-dir` 指假 skill 的全扫 + `K3` 仪器 fail-closed + 坏目录 fail-closed）"
          + ("" if not grp["f_pointer"] else f"（未达预期：{', '.join(grp['f_pointer'])}）"))
    print(f"MUT: {n_tier_ok}/{n_tier} 达预期（`K3` 的 ASCII 阈值标记臂 M47–M53："
          f"{n_tier - 1} 条必须红 + 1 条**射程边界对照**（`主色 4 个` / `下限 4` / `< 25 词`）必须绿）"
          + ("" if not grp["f_tier"] else f"（未达预期：{', '.join(grp['f_tier'])}）"))
    n_sch = len(SCH_MUTATIONS)
    n_sch_ok = n_sch - len(sfailed)
    print(f"MUT: {n_sch_ok}/{n_sch} 达预期（检查器的 `A` 族 M59–M64："
          f"{n_sch - 2} 条必须红 + 2 条**射程边界对照**（`A1` 容差 / `A3` 容差）必须绿）"
          + ("" if not sfailed else f"（未达预期：{', '.join(sfailed)}）"))
    print(f"MUT: {len(rows) - len(mut_failed) + n_spec_ok + n_struct_ok + n_skill_ok + n_ptr_ok + n_tier_ok + n_sch_ok}/"
          f"{len(MUTATIONS) + n_spec + n_struct + n_skill + n_ptr + n_tier + n_sch} 达预期（合计）")
    print(f"探针 P1: {'红' if probe_ok else '未红'}（check-figure-style.py 的脚本探针）")
    print(f"探针 R1: {'红' if r1_ok else '未红'}（读数条 S4 的『该动的时候动、该判的时候不判』）")
    print(f"探针 M65: {'红' if s_probe[0] == 'RED-OK' else '未红'}（丢格探针：只认 `F` 的证据解析器会把 `A` 行丢掉）")
    print(f"（本驱动器共 {len(MUTATIONS)} 条检查器判据变异 + {n_sch} 条 `A` 族判据变异 + {n_probe} 条脚本探针"
          f" + {n_spec} 条规范数变异 + {n_struct} 条结构变异 + {n_skill} 条 SKILL.md 变异"
          f" + {n_ptr} 条引用完整性变异 + {n_tier} 条 `K3` 阈值标记臂变异"
          f"（含射程边界对照：`K3` 1 条 + `A` 族 2 条）+ 1 条读数条探针 + 1 条丢格探针）")
    return 0 if (not failed and not failed_h and byte_ok and clean and selfok_h
                 and rerun.returncode == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
