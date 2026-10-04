# `SECTIONWRITER-evidence.md` —— `mcm-section-writer` 的三臂对照（RED × 纪律轮 × skill 轮）

**本文件由 `tests/skills/section-writer/make-evidence.py` 当场跑命令生成**（`write_bytes`、全 LF）。
**不许手改** —— 改读数请改生成器或产物本身，然后重跑。

> 生成命令：`python tests/skills/section-writer/make-evidence.py`
> 复现：在**已提交的树**上重跑本生成器 ⇒ 本文件**逐字节不变**（证法见 §10）。

**同一把尺** = `.claude/skills/mcm-section-writer/check-section.py`（`SW1–SW9` + `SELF1`/`SELF2` + `EMPTY`），
对**每一件产物**跑同一条命令形态；`--input` 一律指**对应那个节的 brief**。
★ **判据清单现取**（从检查器 stdout 的 `PASS|WARN|FAIL|SKIP` 行里读 id），**不写死条数**。

## §1 三臂（**三个工况，不是两个**）

| 臂 | 产物（**都已在库**） | 给了什么 | 本任务做什么 |
| :--- | :--- | :--- | :--- |
| **RED** | `tests/skills/arch-cases/out-S1.md` · `out-S2.md` · **`out-S2-p.md`** | **什么都不给** | **只读，不重跑** |
| **纪律轮**（既有 GREEN） | `tests/skills/arch-cases/out-S1-g.md` · `out-S2-g.md` | `docs/mcm-writing-discipline.md` 一份 | **只读，不重跑** |
| ★ **skill 轮**（本任务新建） | `tests/skills/section-writer/green/out-S1-skill.tex` · `out-S2-skill.tex` | 本 skill 整目录 | **跑它**（两个新起的写手，本会话独立起，非 fork） |

★ **`out-S2-p.md` 是 RED 独有的压力臂**（队长要求"缺点别写太狠"）—— **skill 轮没有对应臂** ⇒
下表**单列一行并写"无对应"**，**不塞进干净对照里当第三列**。

★ **不重跑 RED 与纪律轮的理由**：它们**逐字冻结、无生成器可重跑**（`tests/skills/arch-cases/README.md` §一 末）。

## §2 泄题清单与隔离做法（**给了任何一项，这次对照当场作废**）

**给写手的只有两样**：`tests/skills/arch-cases/brief-S1.md`（或 `brief-S2.md`）**+** 题面
`tests/skills/abs-cases/case-A-problem.txt`（`arch-cases/README.md:38` 写死）。

**逐项核过、绝不给写手**（**本文件不声称穷尽**）：

- `tests/skills/arch-cases/` 的 `true-S1.md` · `true-S2.md` · `judge.md` · `judge-green.md` · `README-RED.md` · `README.md`；
- ★★ **`tests/skills/abs-cases/case-A-body.md`** —— **`true-S1.md` 就是它第 147–296 行的逐字节副本**（`true-S1.md:2-3`）
  ⇒ **给它＝给答案全文**；同目录 `case-A-body-partial.md` · `case-A-true-abstract.md` 同理；
- ★ `tests/skills/arch-red-evidence.md` · `tests/skills/arch-green-evidence.md`；
- ★ **既有的 `out-S1-g.md` / `out-S2-g.md`（纪律轮产物）与全部 `out-*.md`** —— 它们是**答案的近似物**。

★ **隔离做法（通则 8）**：两样输入**复制到仓库外的固定容器** `D:/Projects/_scratch/m2-sw-green/`
（**不许落盘根**、**不许 `%TEMP%`**、**不许 MSYS `/tmp`**），写手在容器里干活；
**`arch-cases/` 与 `abs-cases/` 整个目录都不给写手看见**（只投喂那两份点名文件）。
★ **怎么把 skill 交给写手**：把 `.claude/skills/mcm-section-writer/` **整目录复制**进容器
（**不许只给 `SKILL.md`** —— 那等于没给 references 与工具）；写手读它并**被要求跑一次检查器**。
★ 两个写手都**由本会话新起（非 fork、无任何上下文）**，派发指令**明写"不要读仓库里其它文件"**。

## §3 产物身份（逐件当场 `git hash-object`）

| 臂 | 产物 | 形态 | 字节 | 行数 | git blob |
| :--- | :--- | :--- | ---: | ---: | :--- |
| RED-S1 | `tests/skills/arch-cases/out-S1.md` | markdown | 14244 | 135 | `7b0d08fb1b97b24218fc690de263765bb2e246ea` |
| RED-S2 | `tests/skills/arch-cases/out-S2.md` | markdown | 10927 | 52 | `293b851760d6fddcd390e2e76a78bac9769532fb` |
| RED-S2p | `tests/skills/arch-cases/out-S2-p.md` | markdown | 8948 | 56 | `db0d6b20095bfc14b1ba30c96c59ff8cf2d39b8d` |
| DIS-S1 | `tests/skills/arch-cases/out-S1-g.md` | LaTeX 源码 | 19627 | 196 | `39a97c673bf9a00bdfda0f359f5b5f1b6106ccaf` |
| DIS-S2 | `tests/skills/arch-cases/out-S2-g.md` | markdown | 15566 | 74 | `c46e1874d1cb150c898c3f8636397ed6772204e2` |
| SKL-S1 | `tests/skills/section-writer/green/out-S1-skill.tex` | .tex 片段 | 7776 | 92 | `b826a912a53e5ca967828b9b7561d8d3236eace3` |
| SKL-S2 | `tests/skills/section-writer/green/out-S2-skill.tex` | .tex 片段 | 3812 | 23 | `7d68cd341a25ff77df84e78c5151f1197a6d8d0f` |

★ **RED 与纪律轮的 5 件是冻结的第三方对照物** —— 本支**不搬动、不改写、不重跑**。
★ **skill 轮的 2 件为本任务新建**（写手产物，逐字入库；入库时只做过 `CRLF → LF` 归一，见 §10）。

## §4 ★ 对照表（**机器读数**；同一把尺、逐件跑）

命令形态：`python .claude/skills/mcm-section-writer/check-section.py <产物> --section <节> --input <brief>`

### §4.1 逐臂读数（尺寸 · 结果 · 退出码）

| 臂 | 节 | 给了什么 | 散文段 | 句 | 正文词 | 表 | `RESULT` | exit |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | :--- | ---: |
| RED-S1 | 模型建立 | **什么都不给** | 26 | 58 | 1313 | 1 | **FAIL** | 1 |
| RED-S2 | 结论 | **什么都不给** | 10 | 42 | 1191 | 0 | **PASS** | 0 |
| RED-S2p | 结论 | **什么都不给**（另有队长口头压力：缺点别写太狠） | 9 | 33 | 787 | 0 | **PASS** | 0 |
| DIS-S1 | 模型建立 | `docs/mcm-writing-discipline.md`（一份纪律文件） | 21 | 38 | 1200 | 1 | **PASS** | 0 |
| DIS-S2 | 结论 | `docs/mcm-writing-discipline.md`（一份纪律文件） | 8 | 25 | 727 | 0 | **PASS** | 0 |
| SKL-S1 | 模型建立 | `mcm-section-writer` **整目录**（`SKILL.md` + 三份 `references` + 检查器） | 15 | 35 | 847 | 1 | **PASS** | 0 |
| SKL-S2 | 结论 | `mcm-section-writer` **整目录**（`SKILL.md` + 三份 `references` + 检查器） | 10 | 24 | 609 | 0 | **PASS** | 0 |

★ **`RESULT`/`exit` 只由硬失败决定**（`FAIL`）；`WARN` / `SKIP` **不影响退出码**（见 §4.3）。

### §4.2 逐判据矩阵（**现取**的 11 条 id）

| 判据 | RED-S1 | RED-S2 | RED-S2p | DIS-S1 | DIS-S2 | SKL-S1 | SKL-S2 |
| :--- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `SW1` | FAIL | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW2` | FAIL | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW3` | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW4` | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW5` | WARN | WARN | WARN | PASS | PASS | PASS | PASS |
| `SW6` | WARN | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW7` | WARN | WARN | WARN | PASS | PASS | PASS | PASS |
| `SW8` | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `SW9` | WARN | PASS | PASS | PASS | PASS | PASS | WARN |
| `SELF1` | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| `SELF2` | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

★ **词表自测行**（`SW3`/`SW5`/`SW6`/`SW8` 使用前必须先拿 `true-*` 自测；命中 0 才可用）：
- `RED-S1`：SW3=0 SW5=0 SW6=0 SW8=0
- `RED-S2`：SW3=0 SW5=0 SW6=0 SW8=0
- `RED-S2p`：SW3=0 SW5=0 SW6=0 SW8=0
- `DIS-S1`：SW3=0 SW5=0 SW6=0 SW8=0
- `DIS-S2`：SW3=0 SW5=0 SW6=0 SW8=0
- `SKL-S1`：SW3=0 SW5=0 SW6=0 SW8=0
- `SKL-S2`：SW3=0 SW5=0 SW6=0 SW8=0

### §4.3 状态语义（照检查器；**别把 `WARN`/`SKIP` 读成 `PASS` 或 `FAIL`**）

- **硬失败（`FAIL`）只有三处**：`SW1` · `SW2` · `EMPTY`。`SW3–SW9` **一律只出"提请复核"（`WARN`），绝不判死**。
- **`SKIP` = 无法判定**（既不是 `PASS` 也不是 `FAIL`）：`--input` 缺失 ⇒ `SW1`/`SW2`/`SW4` 报 `SKIP`；
  真值取不到 ⇒ 词表判据（`SW3`/`SW5`/`SW6`/`SW8`）报 `SKIP`。
- ★ **本文件里 7 臂的 `--input` 都给了** ⇒ `SW1`/`SW2`/`SW4` 不因缺输入而 `SKIP`；
  词表自测行显示**真值取得到**（`SW3=0 SW5=0 SW6=0 SW8=0`）⇒ 词表判据**全部实际执行**。
- **退出码**：有 `FAIL` ⇒ 非 0；只有 `WARN`/`SKIP` ⇒ 0。

## §5 ★★ 哪两列可比（**只评内容覆盖与纪律条目命中，不评风格**）

### §5.1 逐件形态（**当场量过**；`说明段` 不计入）

| 臂 | S1 形态 | S2 形态 |
| :--- | :--- | :--- |
| RED（自由臂） | markdown | markdown |
| 纪律轮 | **LaTeX 源码** | markdown |
| skill 轮 | **.tex 片段** | **.tex 片段** |

（`out-S2-p.md` = markdown，与 RED 自由臂同形态。）

### §5.2 结论：**只有哪一对是干净的单变量**

- ★ **唯一"形态相同、只换了一个变量"的 S2 对** = **RED-S2（markdown） vs 纪律轮-S2（markdown）**
  —— 两侧**同为 markdown**，唯一之差是**给不给那份纪律文件**。这正是 `judge-green.md:264` 原本所指的那一对。
- ★ **RED-S1 vs 纪律轮-S1**：**混了产物形态**（markdown vs LaTeX 源码）⇒ **S1 上的改善不能全归给纪律**。
- ★★ **凡含 skill 轮的跨臂对，S1 与 S2 都同时换了干预与形态**：
  skill 轮**两节产物都是 `.tex` 片段**，而 RED **两节都是 markdown** ⇒
  **`RED-S1 vs skill 轮-S1` 与 `RED-S2 vs skill 轮-S2` 都不是干净单变量对**。
- ★★ **与任务书的一处出入（按"实测优先"登记）**：任务书写 *"只有「RED 自由臂 vs skill 轮」在 S2 上是干净单变量"*。
  **实测不符**：skill 轮 S2 的产物是 `.tex`（`.claude/skills/mcm-section-writer/SKILL.md` 的输出契约就是"该节 `.tex` 片段"），
  与 RED-S2 的 markdown **不是同一形态** ⇒ 该对**同时换了干预与形态**。**本文件以实测为准。**
- ⇒ **本文件的读法**：skill 轮的对照价值在于"**这个 skill 会不会把一节写合格**"（可与两臂并列看绝对读数），
  **不能**把"skill 轮比 RED 干净"归因于 skill —— 形态也换了。

### §5.3 两列**不许并成一列**

- ★ **纪律轮与 skill 轮是两种不同的干预**（一份纪律文件 vs 一个带检查器的逐节 skill）⇒
  二者的读数**不许混成一列**、**不许相减**。
- ★ **`out-S2-p.md`（RED 压力臂）单列**：skill 轮**无压力臂** ⇒ 该行标注 **"无对应"**。

## §6 内容覆盖（**粗粒度**；skill 轮 = 本文件当面核，RED/纪律轮 = 引既有判词）

★ **只评内容覆盖与纪律条目命中，不评风格**（真值是 PDF 转换件，标点与句法表面不可比 —— `judge.md` §5.3 第 3 条）。
★ **本表不声称穷尽**；覆盖判定为**粗粒度的人工判**，不是机器读数。

### §6.1 skill 轮（本文件当面逐条核 `brief` 的要点）

- **SKL-S1**（模型建立，`brief-S1.md` **12 条要点**）：**12/12 覆盖**。落点见
  `green/out-S1-skill-selfcheck.md` §3 的逐点映射表（要点 → 方程/段号）。
  ★ 一处**有意偏离 brief 字面**：brief 第 7 条用 `d` 同时表示 Archard 滑动距离与磨损量 `d(x,y)`；
  正文改用 **`d_s`** 表滑动距离并在首现句说明（**受 `纪律 B3` 驱动**，写手自述）。
- **SKL-S2**（优缺点 + 结论，`brief-S2.md` **8 条要点**）：**8/8 覆盖**。落点见
  `green/out-S2-skill-selfcheck.md` §一 的逐条打勾（优点 3 条 / 缺点 2 条 / 结论成果清单 7 项 / 收束与展望）。

### §6.2 RED / 纪律轮（**引既有判词，本文件未逐点重测**）

- RED 与纪律轮的内容覆盖**不在本文件重测**（那要重跑 `judge.md` §3 / `judge-green.md` §3 的口径）；
  本文件只引其**机器可比的纪律条目读数**（§4）与**登记在案的结论**（§7）。
- ★ **一处 RED 的结构性损失**（`arch-cases/README.md` §三 第三条）：`brief-S1.md` 把
  "为什么 Archard 理论适用于台阶"的论证压成半句 ⇒ RED 写手补不出这层论证**属任务书自身的结构性损失，不是它的疏忽**，
  对照时须单独标出。

## §7 ★★ 三条已登记缺口：判定**分开写**（`judge-green.md:249–251`）

★ `judge-green.md` 三行登记了 GREEN 轮**未修好**的三条（`:249` A3 · `:250` B3 跨节 · `:251` B1 文献表）。
**本任务对这三条的判定能力不同**，必须分开写、不许含糊。

### §7.1 `纪律 A3`（声称读过没读过的部分）—— **判得出**，逐条判"修好没有"

| 臂 | A3 读数 | 依据 |
| :--- | :--- | :--- |
| RED-S1 | 0（无区分力） | `judge-green.md:220` |
| RED-S2 | **1 处失败**：`out-S2.md:3`、`:23`×2（含"前文有数值结果"一句） | `judge-green.md:78-81`、`:220` |
| 纪律轮-S2 | **1 处残留**：`out-S2-g.md:21` 把 brief 只背书半句的"仿真"**扩写得更具体** | `judge-green.md:249` |
| **skill 轮-S2**（本文件当面核） | **修好** —— 结论里关于仿真只有一句
  *"Simulation was used extensively in arriving at all of this."*（= brief 第 7 条"大量使用了仿真"的转述，
  **未添任何 brief 没有的具体用途**）；全节**未对未读章节下具体数值/具体结论的断言** |
  `green/out-S2-skill-selfcheck.md` §二 的 `纪律 A3` 行；本文件另逐句复核 |

⇒ **A3 判定：skill 轮 S2 = 修好**（**判据 = A3 的规则边界**：转述要点里的断言不算违规，
*"扩写得更具体"*才算 —— `docs/mcm-writing-discipline.md` A3；对照 GREEN 的 `:21` 曾加 *"under conditions that are
specified in advance"* 等具体用途，skill 轮 S2 未加）。

### §7.2 `纪律 B3`（跨节符号一致）—— **本任务判不出**

- ★ **本 skill 是逐节工具、不给全文**，而 `judge-green.md:251`/`:267`/`:279` 自认**跨节一致性"无从判"**。
- ⇒ **照实记"仍无从判"**，**不许**写成"已修好"或"未修好"。
- ★ **Task 1 的 `references/section-edges.md` 承接这一条**（符号表：`纪律 B3` 管一节之内、跨节对齐归 `纪律 B6`）——
  但那是**"给了落点"**，**不是"已被验证有效"**。
  ★ **skill 轮的两份自查单都主动登记了这个"无从判"**（`green/out-S1-skill-selfcheck.md` §6、
  `green/out-S2-skill-selfcheck.md` §三 的符号表行），并写明"该风险未消、需全文对齐时人工复查"。

### §7.3 `纪律 B1`（文末文献表）—— **本任务判不出**

- ★ 引用义务含**两处**（正文明标 + 文末表）；**文末表的条目形态不在逐节工具的射程内**（`judge-green.md:251`/`:278`）。
- ⇒ **照实记"仍无从判"**，**不许**写成"已修好"或"未修好"。
- （本文件可另行如实记录**正文明标那一半**的机器可见事实：SKL-S1 正文有 `\cite{who-weights}` 一处；
  SKL-S2 正文 `grep` 无任何引用记号。**但这不是对 B1 的判定** —— B1 的文献表侧仍无从判。）

### §7.4 两条的承接关系（**别把"给了落点"读成"已验证"**）

- Task 1 的 `references/sections.md` 各节 ④ 格 + `references/section-edges.md` 把 `纪律 B3`/`B1` 的**人工落点**写死；
- 但那是**"给了落点"**：本 skill 是逐节工具，**跨节/全篇这两项它判不出** ⇒ 二者**不是"已被验证有效"**。

## §8 ★★ 样本量与形态的边界（`P8`；**必须与上面所有读数同读**）

- **skill 轮每节 1 个产物**（S1 一个 `.tex`、S2 一个 `.tex`），**无压力臂**。
- **RED 侧 3 个产物**（S1 一臂 + S2 两臂：自由臂 `out-S2.md` + 压力臂 `out-S2-p.md`）；
  **纪律轮侧 2 个**（S1、S2 各一）。
- **压力臂只存在于 RED 侧** —— skill 轮**没有**对应臂 ⇒ §5.3 把 `out-S2-p.md` **单列并标"无对应"**。
- ★★ **S1 那一对（RED-S1 vs 纪律轮-S1）混了产物形态**（markdown vs LaTeX 源码，`judge-green.md:264`）
  ⇒ **S1 上的改善不能全归给纪律**。
- ★★ **凡含 skill 轮的跨臂对，S1 与 S2 都混了形态**（§5.2）⇒ **skill 轮上的"更好"也不能全归给 skill**。
- ⇒ **不得**把 S1/S2 的读数写成"该节的普遍规律"；**不得**把任何一臂的改善整个归给单一干预。
- ★ **纪律轮与 skill 轮的读数不许混成一列**（两种干预，§5.3）。

## §9 这套对照证明不了什么（**如实登记，不放大**）

- **n=1**：每臂每节只有 1 个产物，没有第二写手、没有第二个案例 ⇒ 任何"X 有效"的结论都只有 `n=1`。
  （先例 `judge-green.md:263`；本支同样**未能核实**两侧是不是同一写手/同一模型。）
- **测不出跨节 / 全篇一致性**（B1 文献表、B3/B6 跨节符号）—— 逐节工具不给全文（§7.2/§7.3）。
- **测不出"纪律在压力下的存活率"**：本支与既有 GREEN 轮**都没有压力臂**（只有 RED 有）。
- **测不出真实数据压力下的 `纪律 A1`** —— `judge-green.md:268` 同记。
- **测不出 `SW3–SW8` 的阈值**：两轮度量脚本**未落盘**、不可复算 ⇒ `SW3–SW8` 一律只出 `WARN`，**不是判死**、
  **不许读成达标线**（`judge-green.md:270`：*"0 与 0 之间无法定阈"*）。★ `SW9` 不在此列：它的阈值是**当场量的分布式**定的、可复算。
- **不做**判"这段是不是 AI 生成的"（`judge.md:133`/`:244`/`:240`）。
- ★ **检查器射程不许夸大**：`RESULT: PASS`（§4）**只覆盖 `SW1–SW9` 等可机判项**；
  `纪律 A3/A4/A5/B2/B4/B5/B6` 等**仍靠人工逐条**。"**检查器 PASS" ≠ "这一节写好了"**（`SKILL.md`）。

## §10 自证（可重放 / 不动点）

- **检查器自证**：工作树 blob `9b782c142cc4` · **基线 `a49951a`** blob `43d14d2c9be1` ⇒ **不同（！）** —— ★ **本生成器只读检查器、不改它**（blob 不同 ⇒ 检查器在 `a49951a` 之后被改过）。
- **产物自证（逐件 blob）**：`RED-S1`=`7b0d08fb1b97` · `RED-S2`=`293b851760d6` · `RED-S2p`=`db0d6b20095b` · `DIS-S1`=`39a97c673bf9` · `DIS-S2`=`c46e1874d1cb` · `SKL-S1`=`b826a912a53e` · `SKL-S2`=`7d68cd341a25`
- **本生成器不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`，锚点一律用固定基线 `a49951a`）
  ⇒ 本文件是（七件产物字节 + 检查器字节 + 生成器源码）的**纯函数**。
- ★ **不动点证法（通则 14）**：**先干净 → 再捕获 → 再提交 → 再跑一次证不动点** ——
  在**已提交**的树上重跑本生成器，然后 `git status --short` 仍为空、`git diff` 对本文件为空 ⇒ **逐字节不变**。
  （本支执行记录见 `.superpowers/sdd/task-m2-sw-t3-report.md`。）
- ★ **入库时的 `CRLF → LF` 归一（如实登记）**：两个写手的产物原始字节为 **CRLF**（写手工具默认），
  按本仓 GC10"全 LF"要求**只做过换行归一**（`\r\n → \n`），**正文一个字符未改**。

