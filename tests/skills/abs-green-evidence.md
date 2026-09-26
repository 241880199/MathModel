# `mcm-abstract` GREEN 阶段实测证据

**这是什么。** `mcm-abstract` skill 的 GREEN 阶段（TDD for skills 第二步：**装上 skill 后 agent 是否不再失败**）
实测记录。被测对象是 `.claude/skills/mcm-abstract/SKILL.md` 与其随附的 `check-summary.py`；
材料见 `tests/skills/abs-cases/green/`（三份 `.tex` + 三份 `-note.md`）。

**与 RED 证据的分工。** 本文件**不重复** RED 的实测（那在 `abs-red-evidence.md` 里）；
本文只做三件事：**① 三份产物的机检结果（本人当场跑过）② GREEN 相对 RED 的变化 ③ 两个真缺陷的处置 + 残余**。

**纪律。** 每条数字都给**来源**（盘上文件 / 命令输出）与**复现方式**。
凡本次**未能核实**的，在 §5 显式列出，**不写"我记得"**。

---

## 0. 口径与来源

### 0.1 来源（带 sha256，数字锚死在这些字节上）

| 标签 | 文件 | 字节数 | sha256（前 16 位） |
|---|---|---|---|
| `[G1]` | `tests/skills/abs-cases/green/G1.tex` | 7637 | `ee3b526c407b41d2` |
| `[G1n]` | `tests/skills/abs-cases/green/G1-note.md` | 8944 | `db86d0f2bb210069` |
| `[G2]` | `tests/skills/abs-cases/green/G2.tex` | 7142 | `26de862c59679501` |
| `[G2n]` | `tests/skills/abs-cases/green/G2-note.md` | 6910 | `e2a65df29e07d519` |
| `[G3]` | `tests/skills/abs-cases/green/G3.tex` | 6945 | `bcaf94d9d5e2aec0` |
| `[G3n]` | `tests/skills/abs-cases/green/G3-note.md` | 5387 | `b9a52520ca846972` |
| `[C]` | `.claude/skills/mcm-abstract/check-summary.py` | 45072 | `e58ef4fa92ecfa77` | ← **入库时的锚，已失效**；版本演进见 **§0.4** |
| `[K]` | `.claude/skills/mcm-abstract/SKILL.md` | 6294 | `91a6751bb45df252` | ← 同上 |
| `[R]` | `tests/skills/abs-red-evidence.md`（RED 侧全部数字的来源） | — | — |
| `[RC]` | `tests/skills/abs-cases/README.md`（RED 侧的"坏法"清单，§三/§四） | — | — |
| `[Q]` | `tests/skills/mcm-abstract-quality-rubric.md`（13 条判分表） | 38673 | — |
| `[M]` | 本次**当场实测**（命令见 §1.0 与 §6） | — | — |

`[G*]` 三份 `.tex` 与三份 `-note.md` 是 `build/abs-green/` 同名文件的**逐字节副本**（入库时实测 `b == src` 全 True，
见 `abs-cases/green/README.md` §复制校验），所以对它们的哈希即等于对入库产物的哈希。

### 0.2 ★ 一条竞态记录：检查器在本次落库期间被上游改过一次

**这是本项目第 11 条教训（"证据不得在生产者仍在写的时候落盘"）的复发，如实记下：**

1. 落库开始时 `[C]` 的 mtime 是 `01:33`。我跑完三份 G1/G2/G3 的机检，输出行是
   `C1_行内未转义百分号=0  # % 静默吞掉该行剩余部分`。
2. 紧接着我再跑一条自造探针，**同一条命令的输出行变了**：
   `C1_行内未转义百分号=0  # 误写的 % 会静默吞掉该行剩余部分（判据：% 紧贴前一字符且其后仍有内容）`
   **并多出一行 `C1b_行尾注释_不计违规=3`**。
3. 实测 `[C]` 的新状态：mtime `2026-09-27 01:37:55`、大小 45072 B、sha256 `e58ef4fa92ecfa77`
   （`[K]` 同时也有写入：mtime `01:37:43`、大小 6294 B、sha256 `91a6751bb45df252`；它 `:40` 的「拼装契约」一段即 §3.2 所述。
   **我没有旧版 `[K]` 的副本**，故**只记"该时刻有写入"，不断言那一段就是此刻新增的**）。

⇒ **处理**：§1 的全部机检数字都以 **`[C]` = `e58ef4fa92ecfa77` 这一版**重跑取得；
运行**前后各测一次哈希，两次相同**（见 §1.0），确认本次跑的是同一版。
**第一轮（旧版）的输出作废，不引用。**

**同一时段还在动的另外两处（一并记下，作为"生产者未停"的旁证）**：

- `build/abs-green/` 在我落库期间**新增了 4 份**上游自己的验收产物：`good-summary-verify.pdf`、
  `official-asset-verify.pdf`、`silent-percent-verify.pdf`、`trailing-comment-verify.pdf`
  （名字恰好对应 §1.3 的三例 + 一个正例）。**我没有打开它们**（它们是 PDF，判据应看报告而非 PDF）——
  我按同样的用例**自己重跑了一遍**，见 §1.3。
- `build/abs-red/tex-pdf/` 的 `A1-check.pdf`/`A2-check.pdf` 等也在同期被重写（目录 mtime `01:40`）。
  **这些都在 `build/`（gitignored），与本次入库无关**，仅作为"上游仍在写"的佐证记录在此。

> **对本文件"未变更"类结论的效力**：`[G*]` 六份的 mtime 全在 `01:35:52–01:36:53`；
> **末次全量核对（`2026-09-27 01:41:54`）时，这六份的 sha256 与 §0.1 表逐位相符**——
> 即从入库复制到核对那一刻**未被改动**。`build/abs-green/` 当时共 **15 个文件**，
> 除上列 4 份**新增**的 `*-verify.pdf` 外没有其它变化。
> **本节"未变更"类结论的有效时刻 = `2026-09-27 01:41:54`。** 此后若该目录再有写入，请按 `.md5`/sha256 重核。

### 0.3 口径

- **机检** = `python .claude/skills/mcm-abstract/check-summary.py <tex> --pdf <out>`，
  `--pdf` 一律指到 **`build/green-recheck/`**（gitignored 的暂存区），**不往 `tests/` 里写 PDF**。
- **页数**：判据是 `[C]` 用 pdfLaTeX 编两遍后的 PDF 页数（本机 TeX Live 2026 / pdfTeX）。
- **本机余量** = `720 pt`（正文栏底，`bottom=1in` → 792−72）**减去**第 1 页正文最低文字块的 `y1`；
  用 `[C]` 自己的 `page_body_stats()` 量（见 §6.3），与 `[C]` 报的"栏底"同源。
- **字数口径**：中文文件一律给**字节数或汉字数**，不给 `wc -w` —— 它按空白分词，对中文严重低估
  （例：入库时的 `[K]` = **6294 字节 / 1135 汉字**，`wc -w` 只报 **352**）。
  > 复审记录的是"6295 B / 321"，与本次实测（6294 B / 352）在**字节数与 `wc -w` 上都对不上**（汉字数一致）；
  > 以本次实测为准，两个数都带上面这个口径。**凡 `[K]` 的体积，一律引 §0.4 表里的字节数。**

### 0.4 版本锚（复审 + 第二轮 GREEN）

`[C]` 与 `[K]` 在本次落库之后又变过两次，**§0.1 的锚已失效**。逐版如实登记：

| 版本 | 文件 | 字节数 | sha256（前 16 位） | 用它的证据 |
|---|---|---|---|---|
| **v1**（入库冻结） | `[C]` | 45072 | `e58ef4fa92ecfa77` | §1 的机检（本人当场跑）；**已失效** |
| **v1**（入库冻结） | `[K]` | 6294 | `91a6751bb45df252` | 三份 GREEN 产物写于 v1 之前 |
| **v2**（复审用） | `[C]` | 46554 | `820cb147c706e642` | **复审用现行版重跑，输出数字逐行相同**（除新增的 `C1b` 行） |
| **v2**（复审判据） | `[K]` | 6294 | `91a6751bb45df252` | 复审据此判 **G1/G3 违反 ★不过度技术**（`G1.tex:88,90,91,93`；`G3.tex:73,75,76,78-81`）⇒ **v2 的质量类 ★ 没有一条正面证据** |
| **v3**（本轮修订） | `[C]` | 49212 | `f9ea5a2ac79f2e61` | **只改了 `~`（C6）判据 + 年份诊断那行的说明**；`~` 判据的四例实测见 §7 |
| **v3a**（本轮修订；**第二轮 GREEN 的 `G2b`/`G3b` 读到的**） | `[K]` | 11627 | `07a970151b0dd57e` | C-1 修（配方 + 逐条清单）与 I-1/I-2/I-5 都落在这一版 |
| v3b（中间态） | `[K]` | 12355 | `eae42e7a8568cbd2` | 写手开跑后的表述性编辑（★ 图例行、Q7 拆条、错字） |
| **v3c**（第二轮 GREEN 之后） | `[K]` | **13297** | `19ed3b1365c64ea5` | v3b + **§8.5 的两处回写**（「亲眼看那一页」的可执行命令、Q11 余量的量法）。7 个 ★ + 7 条规格 = 14 个条目，**每条都带「怎么查」** |
| **v3d**（复审后末态） | `[K]` | **15824** | `3f7271f1fedb9798` | 复审 5 条的收口：Q12 词表删 `robust`（并写明"优缺点陈述要留"）、删掉自指计数、**新增 ★"摘要自身不许前后打架"**（§8.4.1）、Q13 加"亮点句不许与标缺句打架"。**8 个 ★ + 7 条规格 = 15 个条目**，每条都带「怎么查」（`grep -o 怎么查 \| wc -l` = 16，其中 1 处是读法说明行） |
| （提交锚） | — | — | — | **v2** = 提交 `8d872e5`；**v3a–v3c** = 提交 `4dff42e`（"复审收口——质量层配可执行自查清单…"）；**v3d = 本轮的 5 条收口，截至本文成文未提交** |

> **`~` 判据的修改不影响既有结论**：用 v3 重跑 v1 的三份 GREEN 产物（§6.1 的命令，`--pdf` 指到
> `build/abs-green2/replay/`），**每一行都与 §1.1 相同**，只多出两行新计数 `C6_裸波浪号=0` /
> `C6b_不断行空格_不计违规=0`（三份都是 0）。命令与实测见 §7.4。
>
> **任务书对第二轮的口径与实际做法**：任务书要求"用**当前 shipped** 的 SKILL.md 重跑 GREEN"。
> 实际用的是 **v3a**（本轮修订版，后经 `4dff42e` 提交）—— 因为 C-1 的修（把形状类改成配方、
> 加逐条自查清单）**正是为了让质量类 ★ 有正面证据**；拿 v2 重跑只会复现复审已判定的失败。
> **各版哈希都在上表**，§8 的四份产物对应 **v3a / v3**。

---

## 1. 三份产物的机检结果（`[M]`，本人当场跑）

### 1.0 命令与哈希锚

```console
$ python -c "import hashlib;b=open('.claude/skills/mcm-abstract/check-summary.py','rb').read();print(hashlib.sha256(b).hexdigest()[:16])"
e58ef4fa92ecfa77                       # 跑之前

$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green/G1.tex --pdf build/green-recheck/G1-recheck.pdf
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green/G2.tex --pdf build/green-recheck/G2-recheck.pdf
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green/G3.tex --pdf build/green-recheck/G3-recheck.pdf

$ python -c "import hashlib;b=open('.claude/skills/mcm-abstract/check-summary.py','rb').read();print(hashlib.sha256(b).hexdigest()[:16])"
e58ef4fa92ecfa77                       # 跑之后：相同 ⇒ 三次跑的是同一版
```

### 1.1 关键输出行（逐字粘贴；三份各取 A / B / C / 结论四段）

**G1（A 题齐全）**

```
A1_三栏字样齐全: PASS  # PDF 抽出="Problem Chosen" | "Summary Sheet" | "Team Control Number"
A2_Problem_Chosen: PASS  # PDF 抽出值="A"
A3_Team_Control_Number: PASS  # PDF 抽出值="2534567"
A4_年份_2027: PASS  # PDF 抽出值="2027"
rc=0
硬错误条数=0
页数=1
C1_行内未转义百分号=0  # 误写的 % 会静默吞掉该行剩余部分（判据：% 紧贴前一字符且其后仍有内容）
C1b_行尾注释_不计违规=4  # 合法行尾注释/行首注释行，见 docstring C1 判据
C2_裸下划线上标=0
C3_markdown残留=0
C4_HTML残留=0
C5_裸竖线=0
C6_裸波浪号=0
C7_非ASCII字符=0
RESULT: PASS
EXITCODE=0
```

**G2（C 题齐全）**：`A1` PASS（三栏齐全）/ `A2` PASS 值=`"C"` / `A3` PASS 值=`"2400001"` / `A4` PASS 值=`"2027"`；
`rc=0` · `硬错误条数=0` · `页数=1`；`C1=0` · **`C1b=15`** · `C2=C3=C4=C5=C6=0` · `C7=0`；`RESULT: PASS`；`EXITCODE=0`。

**G3（A 题结果不全）**：`A1` PASS（三栏齐全）/ `A2` PASS 值=`"A"` / `A3` PASS 值=`"2401056"` / `A4` PASS 值=`"2027"`；
`rc=0` · `硬错误条数=0` · `页数=1`；`C1=0` · **`C1b=13`** · `C2=C3=C4=C5=C6=0` · `C7=0`；`RESULT: PASS`；`EXITCODE=0`。

**汇总表**

| 产物 | A1 三栏 | A2 题号 | A3 队号 | A4 年份 | rc | 硬错误 | 页数 | C1 | C1b | C2–C7 | RESULT | 退出码 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `[G1]` | PASS | PASS `A` | PASS `2534567` | PASS `2027` | 0 | 0 | **1** | **0** | 4 | 全 0 | **PASS** | **0** |
| `[G2]` | PASS | PASS `C` | PASS `2400001` | PASS `2027` | 0 | 0 | **1** | **0** | 15 | 全 0 | **PASS** | **0** |
| `[G3]` | PASS | PASS `A` | PASS `2401056` | PASS `2027` | 0 | 0 | **1** | **0** | 13 | 全 0 | **PASS** | **0** |

> **`C7_非ASCII字符=0` 的实情（我实测过，别误读）**：C7 只扫"活的"排版区（**注释不排版、不在扫描面内**），
> 所以 `[C]` 的 `C7=0` 本身**并不能**证明整个文件是 ASCII。于是我用字节级检查复核了整份文件
> （`[M]`，复现见 §6.6）：三份 `.tex` 的**非 ASCII 字节数都是 0**（G1/G2/G3 均为 0）
> ⇒ `C7=0` 在**整份文件**意义上也成立。这与写手自己的声明一致：`[G1]` 头部 `:33` 明写
> "This comment block is ASCII-only on purpose"；`[G3]` 头部 `:15-16` 明写 "This file is kept ASCII-only on purpose…"。

### 1.2 `C1b` 是什么（本次新增的计数项）

`C1b_行尾注释_不计违规` 是 `[C]` 在本次落库期间**新增**的一项（见 §0.2）。当前判据（`[C]` docstring `:71`）：

> 判据 = 未转义 **且** `%` 紧贴前一字符 **且** `%` 后仍有非空白内容 ⇒ 计 `C1`…其余 `%` 计入 `C1b_行尾注释_不计违规`，只报数。
> （`[C]` `:71-72`）

**我自己写了一条三例探针来证明这条判据"既修好了误报、又没放过真违规"**（`[M]`，`build/green-recheck/c1probe2.tex`）：

```latex
\graphicspath{{.}}  % PROBE-A official-template trailing comment, space before percent
% PROBE-B standalone comment line
Text with a tight percent 5% PROBE-C percent hugs the 5, content follows
```

```console
$ python .claude/skills/mcm-abstract/check-summary.py build/green-recheck/c1probe2.tex --pdf build/green-recheck/c1probe2.pdf
C1_行内未转义百分号=1  # 误写的 % 会静默吞掉该行剩余部分（判据：% 紧贴前一字符且其后仍有内容）
C1b_行尾注释_不计违规=2  # 合法行尾注释/行首注释行，见 docstring C1 判据
```

⇒ **PROBE-A（官方模板那种行尾注释，`%` 前有空格）与 PROBE-B（整行注释）都不计违规；
PROBE-C（`5%` 这种紧贴形态）仍计 C1 —— 正是要抓的那一类。** 修好了误报，真违规没放过。

### 1.3 三例验收（`[M]`，我独立重跑 —— 即上游为这次 C1 修改规定的验收条件）

上游给这次修改定的验收条件是"**三例同时证明**"：官方资产（应 `C1=0`）+ `silent-percent`（应仍 `C1=1` 且报出被吞内容）
+ 行尾注释例（应 `C1=0`）。**我自己把三例跑了一遍**：

```console
$ python .claude/skills/mcm-abstract/check-summary.py \
      .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex \
      --pdf build/green-recheck/official-asset-recheck.pdf
A1_三栏字样齐全: PASS … A2_Problem_Chosen: FAIL  # PDF 抽出值="ABCDEF"（模板占位符，题号未填）
A3_Team_Control_Number: FAIL  # PDF 抽出值="1111111"（模板占位符，队号未填）
rc=0 / 页数=2 / C1_行内未转义百分号=0 / C1b_行尾注释_不计违规=12
RESULT: FAIL
失败项=A2_Problem_Chosen,A3_Team_Control_Number,B.页数=2(>1)      # ← 失败项里没有 C1

$ python .claude/skills/mcm-abstract/check-summary.py build/abs-red/tex-pdf/silent-percent.tex \
      --pdf build/green-recheck/silent-percent-recheck.pdf
C1_行内未转义百分号=1 / C1b_行尾注释_不计违规=0
  C1 行=28 列=385 被吞字符数=128 吞掉内容=' of the wear signal from a single depth map of the worn trea'
RESULT: FAIL     失败项=C1=1      EXITCODE=1

$ python .claude/skills/mcm-abstract/check-summary.py build/abs-red/tex-pdf/trailing-comment.tex \
      --pdf build/green-recheck/trailing-comment-recheck.pdf
C1_行内未转义百分号=0 / C1b_行尾注释_不计违规=2 / RESULT: PASS / EXITCODE=0
```

| 用例 | 验收期望 | 我实测 | 判定 |
|---|---|---|---|
| 官方资产 `mcm-2027-summary.tex` | `C1=0` | **`C1=0`**（`C1b=12`）；`RESULT: FAIL` 的失败项是 `A2`/`A3`（模板占位符未填）与 `B.页数=2`，**不含 C1** | **通过** |
| `silent-percent.tex` | 仍 `C1=1`，且报出被吞内容 | **`C1=1`**，报出**被吞 128 字符**及原文（行 28 列 385） | **通过** |
| `trailing-comment.tex` | `C1=0` | **`C1=0`**（`C1b=2`），`RESULT: PASS`，退出码 0 | **通过** |

> **两处必须说清的边界**：
> ① 官方资产那一例的 `RESULT: FAIL` **不是因为 C1**，而是模板本身留着 `ABCDEF`/`1111111` 占位符且**编出 2 页**
> （它是整篇论文模板，不是只含摘要的文件）。**读这一例只看 `C1=0` 这一格**。
> ② 我用的是 `build/abs-red/tex-pdf/` 下**现成的** `silent-percent.tex` 与 `trailing-comment.tex`
> （上游的探针文件，`[M]` 只读使用）——**不是**我自己写的用例；我自己写的那条在 §1.2。

---

## 2. GREEN 相对 RED 的变化

### 2.1 三类形式失败：**全部消失**

（RED 侧的"坏法"清单与数字来自 `[RC]` §三/§四 与 `[R]`：**本文未重算 RED**，逐条引其入库件。）

| # | RED 侧实测的失败（无 skill） | 来源 | GREEN 侧实测 | 结论 |
|---|---|---|---|---|
| 1 | **产物根本不是 LaTeX 源码**：markdown / HTML / 裸 Unicode / 未转义 `%` / 裸下标混在一起，每份要 **32–117 处**机械修复才编得过 | `[RC]` §三.1 | 三份产物都是 **`.tex`**；`C1=C2=C3=C4=C5=C6=C7=0`（§1.1） | **消失** |
| 1b | `%` 静默吞字符：**177 / 226 / 1111** 个字符被当注释吃掉，且**编译退出码不受影响** | `[RC]` §三.2 | 三份的 `C1=0`；`rc=0` 且 `硬错误条数=0` | **消失** |
| 2 | **尺寸失控**：854 / 1127 / 1307 词，编出来**都是 2 页**（摘要页只能占 1 页） | `[RC]` §三.3 与 §四 | 三份**页数=1**（§1.1） | **消失** |
| 3 | **页眉缺字段**：三份基线**全部**没有 `Problem Chosen` 栏 | `[RC]` §三.4 | 三份 `A1_三栏字样齐全: PASS`（判据是**编译出的 PDF 第 1 页文字**） | **消失** |

> ⚠️ 第 2 行的对照要留神口径：RED 侧的三份是 `xelatex` + 官方模板编出 2 页（`[R]` §1.1/§1.4b），
> GREEN 侧是 `pdfLaTeX` 编出 1 页（`[C]` 的固定口径）。**引擎不同**，但 RED 的 2 页是"超出一页"这个**结论**
> 的来源，而 GREEN 的 1 页正是在**同一套 `[C]` 口径**下判的，故"从 2 页到 1 页"方向可信。

### 2.2 内容层：**生效**（不编数 / 标缺 / 剔矛盾数）

**(a) 不编数 + 显式标缺** —— 两处正文原句（`[M]`，grep 自 `[G1]`/`[G3]`）：

| 产物 | 面对的情形（**来源**） | 摘要里怎么写 |
|---|---|---|
| `[G1]` | 正文 §4.1 只**定义**了 `P_A`、**从未算过值**（`[G1n]` §4 第 2 条） | `…the paper defines it but reports no value for this stair, so none is claimed here.`（`[G1]:115`） |
| `[G3]` | 正文 §4 整节（Task 2 五问）**只有判据、没有任何算出来的值**（`[G3n]` §1："`PA`、`CI`、`RSA`、`Htest`、`RS`、`eta` 这些指标**只有公式与阈值，没有任何一个算出来的值**"） | `The numerical work for (i)--(v) has not been carried out, so we mark those five results as missing; no value is quoted for them here, and none is guessed.`（`[G3]:110-111`） |

对照 RED：`red-A3-partial.md` 面对同类削过的正文，Task 2 一个数字都没写（`[RC]` §三.5）；
`red-P1.md` 同类情形下**未披露**结果缺失（`[Q]` §3-Q7、§5-⑦）。

**(b) 剔矛盾数** —— 三份 `.tex` 里 grep 正文里那几个**自相矛盾**的数（`[M]`）：

```console
$ for f in G1 G2 G3; do for p in '1\.14' '62\.8' '616' '0\.02' 'RSA'; do
      echo "$f '$p' -> $(grep -c -- "$p" build/abs-green/$f.tex)"; done; done
G1 '1\.14' -> 0     G1 '62\.8' -> 0     G1 '616' -> 0     G1 '0\.02' -> 0     G1 'RSA' -> 0
G2 '1\.14' -> 0     G2 '62\.8' -> 0     G2 '616' -> 0     G2 '0\.02' -> 0     G2 'RSA' -> 0
G3 '1\.14' -> 0     G3 '62\.8' -> 0     G3 '616' -> 0     G3 '0\.02' -> 0     G3 'RSA' -> 0
```

（grep 覆盖整份 `.tex`，**连注释都没有**这些数 ⇒ 不是"藏在注释里"。）

对照 RED：`red-P2.md` 在"随便挑几个显眼的数字"的压力下，把正文里**自相矛盾**的数 `1.14` 写进了摘要，
已被 controller 裁为**一次真实失败**（`[RC]` §三.6、`[R]` §4.0）。
三份 GREEN 产物**各自独立**给出了剔除理由（`[G1n]` §4.1、`[G2n]` §2、`[G3n]` §2）。

### 2.3 **不能声称的**（免得把 GREEN 读成"全修好了"）

1. **GREEN 侧只重跑了 3 个非压力场景。** RED 的两条**压力探针**（P1 编数诱惑、P2 搬引言+挑数）
   **在 GREEN 侧没有被复测** ⇒ "装上 skill 后权威压力还会不会放宽纪律"**本文件不提供证据**。
   配对关系与这个缺口写在 `abs-cases/green/README.md` §二。
2. **RED 里本来就没失败的三条**（不编数据 / 不搬引言 / 顺序正确）——`[RC]` §三已写明本次采样未观察到失败
   ⇒ 这三条上的"改善"**没有对照意义**，不能记成 skill 的功劳。
   > **【复审更正，此前写成四条】** 原文把**逐问作答**也列在这里，依据是 `[R]` §4.1 的**话题覆盖率词法探针**
   > （关键词命中 8/8）。那个探针**不能判"有没有答那一问"**（`[R]` §4.1 自己也标了"命中关键词 ≠ 真答了那一问"）。
   > 按**产物级证据**（`[Q]` §3-Q7：逐句读产物），**逐问作答在 6 份里失败 5 次**（A1/A2/P2 对"一致性"那一问
   > 只给判据、A3/P1 的 Task 2 五问整块无结论，只有 C1 逐问有答案）。⇒ 它是**已观察到的失败**。
   > `[R]` §4.1 已加同口径警告，`abs-cases/README.md` §三的同名表述也已一并更正。
3. **本节 (b) 的"剔矛盾数"只在三份产物与 `red-P2` 一份之间构成对照**（`red-A1`/`red-A2` 当时也拒绝了 `1.14`，
   见 `[R]` §4.0）⇒ 严格说，GREEN 在这条上**没有超出 RED 已有的水平**，只是**稳定复现**了它。

---

## 3. GREEN 挖出的两个真缺陷及处置

### 3.1 缺陷一：检查器 `C1` 误判官方模板的行尾注释（**三个写手独立撞到**）

**现象。** 官方模板（`mcm-latex-format/assets/mcm-2027-summary.tex`）有一行

```latex
\graphicspath{{.}}  % Place your graphic files in the same directory as your main document
```

这是**合法**的行尾注释（逐字取自官方资产 `:59`），但被旧版 `[C]` 的 `C1` 计为"未转义百分号"
⇒ 模板原样照抄就 `RESULT: FAIL`。

**为什么旧版会判它违规（我读了旧版源码，逻辑可直接推）**：旧版 `[C]`（42695 B / mtime `01:33`，
**我手上已无副本、无哈希**）第 394 行的判据是
`if comment_at is not None and line[:comment_at].strip() != "":` —— 即"**`%` 之前有非空白字符**就算违规"。
官方资产 `:59` 的 `\graphicspath{{.}}` 正是"`%` 之前有内容" ⇒ 旧版计 `C1≥1` ⇒ `RESULT: FAIL`。
（**这一条是"我读过旧源码 + 资产原文"的推论，不是我跑出来的**；旧副本已不存在，无法重放。
**现行版本的实测见 §1.3：`C1=0`。**）

**三份产物的处置（互相不通气的三个写手，做了同一件事）**：都把那句注释**挪到独立行**（`[M]`）：

| 产物 | `\graphicspath` 行 | 其上一行 | 行内还有 `%` 吗 |
|---|---|---|---|
| `[G1]`:68-69 | `\graphicspath{{.}}` | `% Place your graphic files in the same directory as your main document` | 无 |
| `[G2]`:60-61 | `\graphicspath{{.}}` | `% Place your graphic files in the same directory as your main document` | 无 |
| `[G3]`:51-52 | `\graphicspath{{.}}` | `% Put your graphic files in the same directory as your main document` | 无 |

`[G1n]` §3.2 与 `[G2n]` §1 各自写明了理由（前者："那条注释是官方模板自带的合法注释，挪行后语义完全不变"）；
`[G3n]` 未写理由，但产物同样挪了。

**已处置（修在检查器里）。** 当前 `[C]` 的判据是**三个条件的合取**：未转义 **且** `%` **紧贴前一字符**
**且** 其后仍有非空白内容（`[C]`:71，实现在 `[C]`:426-431）；不符合的 `%` 归入 `C1b_行尾注释_不计违规`，**只报数不判违规**。
**我独立重跑了上游为这次修改定的三例验收（官方资产 / `silent-percent` / 行尾注释例），三例全过 —— 见 §1.3**；
另有一条我自己写的三例探针（§1.2）。两者都证明该判据**修好了误报、且没放过 `5%` 这种真违规**。

`[C]` 的 docstring 把这条合取判据的**来源与代价**都写明了（逐字节引 `[C]:419-427` 与 `:73`）：

> 实测依据：RED 三份 raw 源…里**全部**误用形态都**紧贴前一个字符**：`5% below` `within 5%)` `3.0%` `48%)` `0.01%,` ——无一例带前置空白；
> 官方资产里的合法行尾注释是 `\graphicspath{{.}}  % Place your...`（**前置空白**）与 `\textcolor{red}{%`（**其后无内容**）。
> **已知漏报（已裁决接受，别"修"）**：`95 %`（数字与 `%` 之间有空格）这种误写抓不到。

> **⚠️ 与我收到的任务书有一处出入，照记不掩**：任务书把这次修改描述为
> "**仅当 `%` 后有非空白内容才算"会吞内容"**"；**实装判据是合取**（还额外要求"`%` **紧贴前一字符**"）。
> 差别有实际后果：`\graphicspath{{.}}  % …`（`%` 前有空格）**只满足"其后有内容"**，
> 但因不满足"紧贴"而不计违规——**这正是官方模板的形态**，符合修的本意。
> 代价是 `95 %`（**数字与 `%` 之间有空格**）这类误写会**漏报**；`[C]:73` 已把这个漏报登记为"**已裁决接受，别"修"**"。
> **谁改的、什么时候改的：本次落库期间由上游改（§0.2），非本文所为。**

### 3.2 缺陷二："只含摘要 → 1 页" 与官方模板尾段的张力（**G2/G3 独立撞到**）

**现象。** `[K]` 的产出契约要求"只含摘要的 `.tex` 编译后 `page_count == 1`"；而官方模板摘要段之后有一整段
**正文分页脚手架**：`\clearpage` / `\pagestyle{fancy}` / `\newpage` / `\setcounter{page}{1}` /
`\rhead{Page \thepage\ }` / `Begin your paper here`。留着它，pdfLaTeX 会多产一页，
**而那一页与摘要溢出无关**——它是"摘要页不编号、页码从正文第 1 页起算"的**机制**（`mcm-latex-format` 规则 4）。
两条规则**直接冲突**。

**三份产物的处置**（`[M]`，grep 自三份 `.tex`）：

| 产物 | 处置 | 盘上证据 |
|---|---|---|
| `[G1]` | **整段删除**，并在头部注释里写明"omitted, because this file holds no body" | `[G1]:16-19` |
| `[G2]` | **整段注释掉**，并写明"Uncomment it (or simply paste the summary block above into the paper skeleton)" | `[G2]:126-131`（`%\clearpage` … `%\rhead{Page \thepage\ }`） |
| `[G3]` | **删除**，并用注释写明拼装全文时**必须还原** | `[G3]:121-128`（"they must be restored in the full paper, where they make the body restart at page 1"） |

理由写在 `[G1n]` §3.1、`[G2n]` §1（偏离 2）、`[G3n]` §3.1 —— 三份都实测过"留着就多一页"。

**已处置（修在 `SKILL.md` 里，`[K]:40`，逐字引）**：

> **拼装契约（GREEN 实测两路都撞到，务必照做）**：本 skill 的产物是**只含摘要页、可独立编译**的文件
> （这样才能自检"恰好一页"）⇒ **它不含**官方模板摘要之后的尾段。**把它拼进全文时，必须把模板尾段还原**：
> `\clearpage` / `\pagestyle{fancy}` / `\setcounter{page}{1}` / `\rhead{Page \thepage}` /
> `Begin your paper here`——**那是"摘要页不编号、页码从正文第 1 页起算"的机制**（`mcm-latex-format` 规则 4）。
> 别把只含摘要的文件当整篇论文提交。

**我的独立复核**：三份的**页数都是 1**（§1.1），且三份的正文区里**都不含活的** `\clearpage` / `\setcounter{page}{1}`
（grep 命中的全部落在注释块内，见上表"盘上证据"栏）。⇒ 契约与产物一致。

---

## 4. 残余

### 4.1 三份都用**占位队号** —— **交稿前必换真值**

| 产物 | 填的队号 | 位置 | 写手自陈 |
|---|---|---|---|
| `[G1]` | `2534567` | `[G1]:47` `\newcommand{\Team}{2534567}` | `[G1n]` §3.3："本次是测试件、没有真实队号，故填一个占位数字（**若这是真实提交，须换成真队号**）" |
| `[G2]` | `2400001` | `[G2]:39` `\newcommand{\Team}{2400001}` | `[G2n]` §4.1："**这是本件唯一的必改项**——交稿前换成真队号，并把提交文件名同时改成 `<队号>.pdf`" |
| `[G3]` | `2401056` | `[G3]:30` `\newcommand{\Team}{2401056}` | `[G3n]` §3.2："**提交前必须换成真实队号**（同时改 `\lhead{Team \Team}` 与摘要页右栏，两者同源，改宏即可）" |

`[C]` 只查"不得留模板占位符 `1111111`"（源码侧 `[C]`:628-630，PDF 侧 `[C]`:773），**它不查这个数是不是真的**——
所以三份都 `PASS`，但**没有一个是真的**。**这是三份产物共同的、也是唯一的必改项。**

### 4.2 本机余量（`[M]`，口径见 §0.3）

| 产物 | 第 1 页正文最低文字块 `y1` | 栏底 720 pt − `y1` | 写入手自报 |
|---|---|---|---|
| `[G1]` | 670.2 pt | **49.8 pt**（约 3.4 行） | `[G1n]` §2："尚余 **49.8 pt ≈ 3.4 行**" ⇒ **逐位相符** |
| `[G2]` | 661.6 pt | **58.4 pt**（约 4 行） | `[G2n]` §4.2："尚余约 **58 pt ≈ 4 行**" ⇒ **相符** |
| `[G3]` | 701.1 pt | **18.9 pt**（约 1.3 行） | `[G3n]` §4 **只写了"第 1 页 3451 字符"**，未记点数 ⇒ **本行为我实测，非自报** |

> `[G3]` 的 **18.9 pt** 值得单独看：`[K]` ★简洁行新增了"**别刚好填满**——本机编译一页 ≠ 网页端也一页
> （换页点可能不同），留几行余量"。**G3 是三条里余量最小的**，若网页端 TeX 的换行点稍有不同，
> 它有溢到第 2 页的风险。**这是本文件对下游唯一的风险提示**（G1/G2 的余量分别是它的 2.6 倍与 3.1 倍）。

另附（`[M]`）三份第 1 页**渲染**词数（口径：PDF 第 1 页 `y > 70pt` 的词，即剔除页眉三栏）：
`[G1]` 597 · `[G2]` 561 · `[G3]` 557。**这是"页面容量"口径，不是"摘要词数"口径**，勿与 `[RC]` §四 的
RED 词数（854/1127/1307，摘自 `.md` 源）直接比。

### 4.3 另外两条我注意到的（**不属任务书列举**，登记备查，未作处置）

1. **`[G1]` 把 `[0.359, 0.996]` 带进了摘要**（`[G1]:117`）。`[Q]` §5-① 判该区间的**下界 `0.359` 在正文里不可复现**
   （按正文自己的式 (4.3)(4.4) 与 `α=0.05`、`RA=5, RC=1` 代入应得 ≈0.957）。`[Q]` §6-顾虑 3 与裁决栏第 4 条
   已裁"**不计入 Q9**"，所以**这不是本文要推翻的结论**，但它**确实是三份 GREEN 产物里唯一一个带进了
   "正文自相矛盾/不可复现数"的地方**。`[G2]`/`[G3]` 无此形态（grep `0\.359` 命中数：G1=1、G2=0、G3=0）。
2. **`[G3n]` §4 的"第 1 页 3451 字符"我未能复现**（见 §5）。

---

## 5. 未能核实 / 存疑清单（不掩盖）

| # | 事项 | 状态 |
|---|---|---|
| 1 | `[G3n]` §4 自报"第 1 页 **3451 字符**" | **未能核实**。我实测两种口径都对不上：整页非空白字符 **2884**、剔页眉后分词拼串 **2823**（`[M]`）。note 未写明口径 ⇒ 无法判定其算法。**该数不引用。** |
| 2 | `[G2n]` §4.3 自报"一页还有余量未用（**552 词正文**）" | **未能逐字复现**。我按"第 1 页渲染词数"口径得 **561**（`[M]`）。差 9 词，方向合理（口径不同：note 大概率数的是 `.tex` 源），但**我没找到它的确切口径** ⇒ 引 552 时须带出处、不要当成实测值。 |
| 3 | `[G1n]` §2 自报"版式实测：US Letter（612×792 pt）；正文末行距栏底（720 pt）尚余 **49.8 pt ≈ 3.4 行**" | **已核实**（`[M]`，逐位相符；见 §4.2）。页面尺寸亦实测 612×792 pt。 |
| 4 | 三份在**网页端**（用户实际提交用的编译器）的页数 | **未能核实，且本机也不可能核实**。`[K]` 与 `[G2n]` §4.2 均已声明"以实际提交那次编译为准"。本文件所有页数都是**本机** pdfLaTeX 的结果。 |
| 5 | `[G2n]` §3 提到 `[G2]` 的标题行沿用正文标题 | **已核实**：`[G2]:73` 的 `\textbf{2028 Olympic Medal Predictions Based on Random Forest Model}` 与 `[G2n]` §2 表述一致。 |
| 6 | RED 侧的**全部**数字（32–117 处 / 177·226·1111 / 854·1127·1307 / 全部缺 `Problem Chosen` / 2 页） | **本文未重算**，逐条引自入库件 `[RC]` §三/§四 与 `[R]`。要重算请看那两份文件里的复现命令。 |
| 7 | `[C]` 的改动是**谁**在**何时**做的 | **未能核实身份，只核实了时间与哈希**（§0.2：mtime `01:37:55`、sha256 `e58ef4fa92ecfa77`）。本文件只记录"期间被上游改过"这一事实。 |
| 8 | §2.1 第 2 行 RED(2 页) vs GREEN(1 页) 的**引擎不同**（RED 用 xelatex，GREEN 用 pdfLaTeX） | 已如实标注（§2.1 的 ⚠️）。**这不是"未能核实"，是"口径不同"，不可混用。** |
| 9 | 上游那 4 份 `*-verify.pdf`（`build/abs-green/`，§0.2）的**内容** | **未打开、未核对**。理由：判据应看**机检报告**而不是 PDF（PDF 每次编译都带新时间戳/ID，不可逐字节比）。我改用"按同样用例自己重跑检查器"来核实，见 §1.3。 |
| 10 | `build/abs-red/tex-pdf/` 里 `silent-percent.tex` / `trailing-comment.tex` 的**作者与来历** | **未能核实**。我只核实了它们**存在且可读**（`[M]` 只读使用）以及它们跑出来的结果（§1.3）。**它们不在本次入库范围内。** |
| 11 | **第二轮 GREEN（§8）的三条未核实项** | 见 **§8.6**（压力场景仍未复测 / 网页端分页未验证 / 占位队号未换）。**本节（第一轮的清单）与那三条并列，不互相替代。** |

---

## 6. 复现命令

### 6.1 三份产物的机检（本文 §1 的全部数字）

```bash
cd <repo-root>
mkdir -p build/green-recheck
for f in G1 G2 G3; do
  echo "######## $f ########"
  python .claude/skills/mcm-abstract/check-summary.py build/abs-green/$f.tex \
         --pdf build/green-recheck/$f-recheck.pdf
  echo "EXITCODE=$?"
done
```

### 6.2 `C1` / `C1b` 判据的三例探针（本文 §1.2）

```bash
cat > build/green-recheck/c1probe2.tex <<'EOF'
\documentclass[12pt]{article}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{left=1in,right=0.75in,top=1in,bottom=1in}
\newcommand{\Problem}{A}
\newcommand{\Team}{1234567}
\usepackage{fancyhdr}
\begin{document}
\thispagestyle{empty}
\graphicspath{{.}}  % PROBE-A official-template trailing comment, space before percent
% PROBE-B standalone comment line
Text with a tight percent 5% PROBE-C percent hugs the 5, content follows
\end{document}
EOF
python .claude/skills/mcm-abstract/check-summary.py build/green-recheck/c1probe2.tex \
       --pdf build/green-recheck/c1probe2.pdf | grep -E "^C1|^C1b"
# 期望：C1=1（PROBE-C，紧贴的真违规）· C1b=2（PROBE-A 行尾注释、PROBE-B 整行注释）
```

### 6.3 本机余量（本文 §4.2）

用 `[C]` 自己的 `page_body_stats()`，与它报的"栏底"同源：

```bash
python - <<'PY'
import importlib.util, fitz
spec = importlib.util.spec_from_file_location('cs', '.claude/skills/mcm-abstract/check-summary.py')
cs = importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)
for f in ('G1','G2','G3'):
    doc = fitz.open('build/green-recheck/%s-recheck.pdf' % f)
    st = cs.page_body_stats(doc[0])
    print('%s: pages=%d  page=%.0fx%.0fpt  body_y1=%.1f  720-y1=%.1f pt'
          % (f, doc.page_count, doc[0].rect.width, doc[0].rect.height, st['y1'], 720-st['y1']))
    doc.close()
PY
# 期望：G1 49.8 / G2 58.4 / G3 18.9（pt）
```

### 6.4 内容层 grep（本文 §2.2）

```bash
for f in G1 G2 G3; do
  for p in '1\.14' '62\.8' '616' '0\.02' 'RSA' '0\.359'; do
    echo "$f '$p' -> $(grep -c -- "$p" build/abs-green/$f.tex)"
  done
done
# 期望：除 G1 的 '0\.359' = 1 外，其余全 0（见 §4.3 第 1 条）
```

### 6.5 三份产物与 note 的指纹（本文 §0.1）

```bash
python -c "import hashlib,glob
for f in sorted(glob.glob('tests/skills/abs-cases/green/*')):
    print(f, hashlib.sha256(open(f,'rb').read()).hexdigest()[:16])"
```

### 6.6 三份 `.tex` 是否真为纯 ASCII（本文 §1.1 的旁注）

```bash
python -c "
for f in ('G1','G2','G3'):
    raw = open('build/abs-green/%s.tex' % f, 'rb').read()
    print(f, '非ASCII字节数 =', sum(1 for b in raw if b > 127))"
# 期望：三行都是 0
```

### 6.7 三例验收（本文 §1.3）

```bash
mkdir -p build/green-recheck
python .claude/skills/mcm-abstract/check-summary.py \
       .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex \
       --pdf build/green-recheck/official-asset-recheck.pdf | grep -E "^C1_|^C1b|^失败项"
# 期望：C1_行内未转义百分号=0 · C1b=12 · 失败项里没有 C1

python .claude/skills/mcm-abstract/check-summary.py build/abs-red/tex-pdf/silent-percent.tex \
       --pdf build/green-recheck/silent-percent-recheck.pdf | grep -E "^C1_|^C1b|^  C1 |^失败项"
# 期望：C1=1 且报出被吞字符数=128；退出码 1

python .claude/skills/mcm-abstract/check-summary.py build/abs-red/tex-pdf/trailing-comment.tex \
       --pdf build/green-recheck/trailing-comment-recheck.pdf | grep -E "^C1_|^C1b|^RESULT"
# 期望：C1=0 · C1b=2 · RESULT: PASS；退出码 0
```

> `--pdf` **必须给**：省略时检查器会把 PDF 写到**输入文件所在目录**（对官方资产那一例就是
> `.claude/skills/mcm-latex-format/assets/`——那是**只读区，不能落文件**）。

---

## 7. `~`（C6）的四例实测 + `95 %` 漏报的实测 —— 工具 v3 的两处证据

`[C]` 在 v3（§0.4）改了两处：**`~` 的判据**（这处是判据修改）与**年份诊断那行的说明**（只加说明）。
本节是这两处的实测证据；用例文件都在 `build/abs-green2/`（gitignored 暂存区，可现场重建）。

### 7.1 `~` 的判据（v3 起）

> 判据 = 未转义 **且** 文本模式 **且** `~` **前是空白（或行首）** **且** `~` **后是数字** ⇒ 计 `C6`；
> 其余 `~` 计入 `C6b_不断行空格_不计违规`，只报数。（`[C]` docstring「C6 的判据」）

**为什么必须分开这两类**：`~` 在 LaTeX 里是**不断行空格**，`Fig.~1` / `12~pt` / `Dr.~Smith` 都是合法用法；
但作者若想写"约"（`~48%` = about 48%），`~` 在页面上会**消失**、把语义改成"48%" —— 编译不报错。
两者同形，只能按上下文分。两侧都实测到了（下两小节）。

### 7.2 四例：一违规 + 三合法（逐例跑过）

用例文件 `build/abs-green2/tilde-cases.tex` = `build/abs-red/tex-pdf/good-summary.tex` ＋ 末尾一段探针句：

```latex
The central band carries about ~48\% of the signal, which the caption reports at 12~pt type
(Fig.~1 and the note by Dr.~Smith, who re-read the same map).
```

命令与关键输出（`[M]`，本人当场跑）：

```console
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green2/tilde-cases.tex \
       --pdf build/abs-green2/tilde-cases-check.pdf
C6_裸波浪号=1  # `~` 作「约」讲时会凭空消失并改语义（判据：`~` 前是空白或行首 且 `~` 后是数字）
C6b_不断行空格_不计违规=3  # Fig.~1 / 12~pt / Dr.~Smith 这类合法用法
  C6 行=41 列=32 裸 ~ 上下文='ies about ~48\\% of th'
RESULT: FAIL      失败项=C6=1      EXITCODE=1
```

| `~` 用例 | 前一字符 | 后一字符 | 期望 | 实测 |
|---|---|---|---|---|
| `about ~48\%`（作者本意是"约"） | 空格 | 数字 `4` | **计 C6（违规）** | ✅ 计入，报出行 41 列 32 |
| `Fig.~1` | `.` | 数字 `1` | 不计（合法 nbsp） | ✅ 计入 `C6b` |
| `12~pt` | 数字 `2` | 字母 `p` | 不计（合法 nbsp） | ✅ 计入 `C6b` |
| `Dr.~Smith` | `.` | 字母 `S` | 不计（合法 nbsp） | ✅ 计入 `C6b` |

⇒ **一违规三合法四例同时成立**：真违规没放过（`~48%` 命中），三类合法的不断行空格没误报（合计 `C6b=3`）。
另：**RED 侧真出现过的那个 `~48%`**（`tests/skills/abs-cases/red/red-A2.md:73` "changes long-run wear by ~48%"）
正落在这个判据的命中区（前空格 + 后数字）—— 判据不是凭空定的。

**反向一测：只有合法不断行空格时，`C6b` 不影响结论**（用例 `build/abs-green2/tilde-legal-only.tex`
= 同一份探针，**只**把那句里的 `~48\%` 换成不含 `~` 的写法）：

```console
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green2/tilde-legal-only.tex \
       --pdf build/abs-green2/tilde-legal-only-check.pdf
C6_裸波浪号=0 · C6b_不断行空格_不计违规=3
页数=1
RESULT: PASS      EXITCODE=0
```

⇒ `C6b` 是**只报数、不参与 `RESULT`** 的计数项（与 `C1b` 同设计）。

### 7.3 `95 %` 漏报的实测（`SKILL.md` I-1 那条的依据）

用例 `build/abs-green2/space-percent.tex` = `build/abs-red/tex-pdf/silent-percent.tex`，**只**把
`recover 95% of` 改成 `recover 95 % of`（其它逐字节不变）：

```console
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green2/space-percent.tex \
       --pdf build/abs-green2/space-percent-probe.pdf
C1_行内未转义百分号=0  # 误写的 % 会静默吞掉该行剩余部分（判据：% 紧贴前一字符且其后仍有内容）
C6_裸波浪号=0 · C6b_不断行空格_不计违规=0
页数=1
RESULT: PASS      EXITCODE=0
```

**而同一行 `%` 之后有 128 个字符已被静默吞掉**（实测：行=28，`%` 在第 386 列，
其后的 128 字符不排版）。对照紧贴写法：

| 输入 | 写法 | `C1` | 被吞字符数 | `RESULT` | 退出码 |
|---|---|---|---|---|---|
| `build/abs-red/tex-pdf/silent-percent.tex` | `recover 95% of`（紧贴） | **1** | **128** | FAIL | 1 |
| `build/abs-green2/space-percent.tex` | `recover 95 % of`（有空隙） | **0** | **128**（工具未报） | **PASS** | **0** |

⇒ **漏报是真的，且吞掉的内容一样多（128 字符）** —— 一份有 128 字符消失、页面上少半句话的摘要
能拿到 `RESULT: PASS` 与退出码 0。**这就是 `SKILL.md` 把"用 Read 亲眼去看那一页"写成不可省的理由**
（取舍与本工具的已知漏报同源，见 `[C]` docstring「C1 的判据」）。

### 7.4 v3 重跑 v1 三份产物：**既有结论逐行未变**

改判据必须证明"没动到别的结论"。用 v3 重跑 `[G1]`/`[G2]`/`[G3]`（命令同 §6.1，`--pdf` 指到
`build/abs-green2/replay/`）：

| 产物 | A1 三栏 | A2 题号 | A3 队号 | A4 年份 | rc | 硬错误 | 页数 | C1 | C1b | **C6** | **C6b** | C2–C5/C7 | RESULT | 退出码 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `[G1]` | PASS | PASS `A` | PASS `2534567` | PASS `2027` | 0 | 0 | **1** | **0** | 4 | **0** | **0** | 全 0 | **PASS** | **0** |
| `[G2]` | PASS | PASS `C` | PASS `2400001` | PASS `2027` | 0 | 0 | **1** | **0** | 15 | **0** | **0** | 全 0 | **PASS** | **0** |
| `[G3]` | PASS | PASS `A` | PASS `2401056` | PASS `2027` | 0 | 0 | **1** | **0** | 13 | **0** | **0** | 全 0 | **PASS** | **0** |

⇒ 除新加的 `C6`/`C6b` 两行（三份都是 0）外，**与 §1.1 的表逐格相同**。

### 7.5 年份诊断那行（v3 加的说明）

跑官方资产时源码侧会打出 `年份=2026`，而 A4 从 PDF 读到 `2027`、判定正确：

```console
$ python .claude/skills/mcm-abstract/check-summary.py \
       .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex \
       --pdf build/abs-green2/official-asset-probe.pdf
A4_年份_2027: PASS  # PDF 抽出值="2027"
[辅助诊断-源码] 不参与判定: Problem=ABCDEF(宏定义) | Team=1111111(宏定义) | 年份=2026(MCM/ICM 标题栏)
  年份诊断说明=这里的年份取自**源码**（…第一处 `MCM/ICM` 前 80 字符窗口），可能取到注释里的旧年份
  （官方资产 `mcm-2027-summary.tex` 的注释里就有 `2026`）⇒ **这不是判定依据**；
  判定依据是上方 A4（从编译出的 PDF 第 1 页读出的年份）。
```

`2026` 的来源已核到源：官方资产 `mcm-2027-summary.tex:9-12` 的**注释**里写着 `2026 MCM/ICM Summary Sheet`
（那是"官方原件漏改年份"的说明文字）。**判据不看它**（`[C]` docstring「判据只读产物」）。

---

## 8. 第二轮 GREEN —— 用本轮的 skill 重跑（**C-2 的收口**）

### 8.0 ⚠️ 四个写手**读到的不是同一版 skill** —— 一个必须登记的交付事故

四个写手各起一个独立 agent，**显式调用 `Skill` 工具加载 `mcm-abstract`**，只读 `case-{A,C}-problem.txt`
与对应正文，**明令禁止**读 `red/**`、`green/**`、`build/abs-green/**`、两份 evidence、判分表与 `*-true-abstract*`。

**派发时刻盘上的 `[K]` 是 v3a（11627 B / `07a970151b0dd57e`，§0.4）。实测结果是：四个写手拿到了两个不同版本（v2 与 v3）。**

| 写手 | 它加载到的 `[K]` | 判定依据（可核） |
|---|---|---|
| `G1b`（A 题齐全） | **v2 = 本轮修订前的 shipped 版**（提交 `8d872e5` 里的 6294 B / `91a6751bb45df252`） | **它自己的转述**（`build/abs-green2/G1b-note.md:274-276`，本节按其原话转述、不加引号当逐字引文）：它说 skill 的「质量与措辞」一节**从未把它们编号**、也**没有给每条配检查方法**，`13 条里只有 Q5 给了可操作的两步法`，12/13 条的检查方法是它自己补的；并逐字给出条目形态是 `不用技术细节占版面` 这种**没有 Q 编号、没有 `**怎么查**：` 字段**的写法 —— 这正是 v2 的文本（v3 每一条都带 Q 编号与「怎么查」）。**⇒ 判定"G1b 读到的是 v2"成立。** |
| `G2b`（C 题齐全） | **v3**（≥ v3a） | 它逐条引用的是 v3 才有的标签：`★Q6 / ★Q7 / ★Q11 / ★Q12 / ★Q9 / ★Q2 / Q1 / Q3 / Q4 / Q5 / Q8 / Q10 / Q13`，并称每条都做了「怎么查」 |
| `G3b`（A 题结果不全） | **v3a**（末态与其引用一致） | 它引用 `★Q7 逐问作答 + 标缺`（**v3a 的合并写法**，v3b 已拆开） |
| `G1c`（A 题齐全，补派） | **v3**（v3a–v3c 的 Q6 行逐字相同，无法再细分） | **它做了强制版本核对**：`Read` 盘上文件逐项核对后报"`Skill` 工具给的内容与盘上一致"，并引盘上原文 `★ **Q6 不让技术细节占版面**（形状类）` 与其 `- **怎么查**：…` 行；同时确认旧版特征串 `★ 不用技术细节占版面` 在盘上 **grep 0 命中** |

> **⇒ 这是一次真实的交付事故，与 §0.2 记的第 11 条教训同族（"证据不得在生产者仍在写的时候落盘"），
> 但根因不同：这次是"**消费端拿到的版本可能滞后于生产者盘上的版本**"。**
> 同一个 `Skill` 工具、同一批派发、同一份盘上文件，三个写手拿到两版。**机制未查明**（可能是
> 会话级 skill 缓存与落盘的时序），**本文只登记现象与可核证据，不给因果结论**。
>
> **对证据效力的处置**：
> 1. **`G1b` 的"逐条自查"叙述不能当作对 v3 的验证**（它读的是 v2）—— 但**它的产物与机检数字仍然有效**
>    （那些是对 `.tex` 的实测，与写手读了哪版 skill 无关）。它因此**不算本轮 v3 的正面证据**，
>    只作**旁证**：**v2（禁令式）这一版在 A 题齐全这一场景下也没排公式**，而**第一轮同样用 v2 的三份全排了公式**
>    （§8.2）⇒ 与 `writing-skills` 的判断一致：**禁令式在竞争性动机下是"噪声大"而不是"必然失败"**。
> 2. 为拿到**干净的 A 题齐全 × v3** 这一臂，已补派第 4 个写手（`G1c`），并在任务书里加了
>    **"读盘核对 + 与 `Skill` 工具内容不一致时以盘上为准"** 的强制步骤 —— 这既是本轮的对策，
>    也是给下一次的现成做法。
> 3. `G1b-note.md` §2 里一处自述错误（"7 个 ★ + 6 条规格 = 13 条"）：写手在核对后**自己**发现并更正为
>    **"7 + 7 = 14 个条目，整节完全未编号"**。**该 note 未被修改**（它要求冻结），本文以本表的判定为准。
> 4. **"G1b 读到的是 v2"这条判断已独立复核，结论不变**（本文与复审各自核过一遍，命令可重放）：
>    特征串 `不用技术细节占版面` —— 在 **v2 里有 1 处**、在**本轮 shipped 版（v3c）里 0 处**、
>    在 **`G1b-note.md` 里有 1 处** ⇒ 该写手手上的文本含 v2 独有、v3 已删的串。
>    ```bash
>    git cat-file -p 8d872e5:.claude/skills/mcm-abstract/SKILL.md | grep -c 不用技术细节占版面   # → 1（v2）
>    grep -c 不用技术细节占版面 .claude/skills/mcm-abstract/SKILL.md                            # → 0（v3c）
>    grep -c 不用技术细节占版面 build/abs-green2/G1b-note.md                                    # → 1（写手手上）
>    ```
>    **同时更正本文前一版的引用方式**：本表原先给 `G1b` 那一行加了引号的"逐字引文"
>    （`值得照做` / `可照此两步查`）**在该 note 里命中 0** —— 它们是**本文的转述、不是引文**。
>    现已改成**转述形态**并只保留 note 里**真实存在**的串（`不用技术细节占版面`、`从未把它们编号`、
>    `只有 Q5 给了可操作的两步法`）。**转述写成引文是本轮新引入的缺陷之一，这里如实更正。**

| 项 | 值 |
|---|---|
| 派发时盘上的 `[K]` | **v3a** = 11627 B / `07a970151b0dd57e`（§0.4） |
| 本文成文时的末态 `[K]` | **v3c**（含 §8.5 的回写；哈希见 §0.4 表末行） |
| v3a → v3c 的差异 | 全是**表述性／可执行性**编辑：① ★ 图例句独立成行 ② "结果没出来就显式标缺"从 Q7 拆成独立一条并补它的「怎么查」 ③ 两处错字/口径措辞 ④ **补「亲眼看那一页」的执行命令**（§8.5，三个写手独立撞到的真缺陷）。**质量层的要求没有增减。** |

### 8.1 机检：四份都是 1 页、机械面全 0（`[M]`，本人当场跑）

命令（`--pdf` 指到 `build/abs-green2/`；每份都另存了一份独立复核 PDF）：

```console
$ python .claude/skills/mcm-abstract/check-summary.py build/abs-green2/<G?b 或 G1c>.tex \
       --pdf build/abs-green2/<同名>-verify.pdf
```

| 产物 | 场景 | 读到的 skill | A1 三栏 | A2 题号 | A3 队号 | A4 年份 | rc | 硬错误 | 页数 | C1 | C1b | C2–C5/C7 | C6/C6b | RESULT | 退出码 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `G1c` | A 题齐全 | **v3** | PASS | PASS `A` | PASS `2401057` | PASS `2027` | 0 | 0 | **1** | **0** | 9 | 全 0 | 0/0 | **PASS** | **0** |
| `G2b` | C 题齐全 | **v3a** | PASS | PASS `C` | PASS `2401057` | PASS `2027` | 0 | 0 | **1** | **0** | 13 | 全 0 | 0/0 | **PASS** | **0** |
| `G3b` | A 题结果不全 | **v3a** | PASS | PASS `A` | PASS `2401057` | PASS `2027` | 0 | 0 | **1** | **0** | 12 | 全 0 | 0/0 | **PASS** | **0** |
| `G1b` | A 题齐全 | v2（滞后，§8.0） | PASS | PASS `A` | PASS `2401057` | PASS `2027` | 0 | 0 | **1** | **0** | 3 | 全 0 | 0/0 | **PASS** | **0** |

### 8.2 ★ **本次唯一的硬验收：读了 v3 的那三份都不再把公式排进第 1 页**（C-2 的判据）

判据 = 正文区（`begin{document}` 之后、`end{document}` 之前、**排除注释行**）里的 `$` 出现次数、
`_`/`^` 出现次数、`\[`/`equation` 环境数。**第一轮（v2 skill）与第二轮（v3 skill）同一口径对照**：

| 轮次 | 写手读到的 skill | 产物 | 正文 `$` 个数 | `_`/`^` 个数 | 显示数学 | 是否违反 ★不过度技术 |
|---|---|---|---|---|---|---|
| 第一轮 | v2 | `G1` | **72** | **23** | 0 | **违反**（`G1.tex:88,90,91,93`，复审已判） |
| 第一轮 | v2 | `G2` | 18 | 2 | 0 | 违反 |
| 第一轮 | v2 | `G3` | **56** | **27** | 0 | **违反**（`G3.tex:73,75,76,78-81`，复审已判） |
| 第二轮 | **v2**（滞后版，§8.0） | `G1b` | 0 | 0 | 0 | 不违反 —— **旁证，不算 v3 的证据** |
| 第二轮 | **v3a** | `G2b` | **0** | **0** | 0 | **不违反** |
| 第二轮 | **v3a** | `G3b` | **0** | **0** | 0 | **不违反** |
| 第二轮 | **v3** | `G1c` | **0** | **0** | 0 | **不违反**（§8.7） |

复现（本文用的口径，逐字节可重放）：

```bash
python - <<'PY'
import re
for tag, base, files in (("v2-第一轮", "tests/skills/abs-cases/green/", ("G1","G2","G3")),
                         ("v3-第二轮", "build/abs-green2/", ("G1c","G2b","G3b"))):
    for f in files:
        t = open(base + f + ".tex", encoding="utf-8").read()
        i, j = t.find("begin{document}"), t.find("end{document}")
        body = "\n".join(l for l in t[i:j].split("\n") if not l.lstrip().startswith("%"))
        print(tag, f, "正文$=%d _^=%d" % (body.count("$"), len(re.findall("[_^]", body))))
PY
# 期望：v2-第一轮 G1 72/23 · G2 18/2 · G3 56/27 ；v3-第二轮 三份全 0/0
```

⇒ **v3（本轮修订）的质量类 ★ 拿到了正面证据**：读了 v3 的两份产物（`G2b`、`G3b`，另加补派的
`G1c` 见 §8.7）覆盖 **C 题齐全 / A 题结果不全 / A 题齐全** 三个不同场景，**一个公式、一个下标都没排**。
这与 v2 第一轮的"三份全违反"构成干净对照（`G1b` 那一份读的是滞后的 v2，见 §8.0，**不计入**本结论）。

### 8.3 其余量测（`[M]`）

| 产物 | 读到的 skill | 字节数 | sha256(16) | 第 1 页正文块底 `y1` | 到栏底 720pt 的余量 | 第 1 页渲染词数 |
|---|---|---|---|---|---|---|
| `G1c` | **v3** | 6606 | `07eeabb875923fb4` | 621.4 pt | **98.6 pt**（≈7.3 行） | 608 |
| `G2b` | **v3a** | 6379 | `7f43172ffc99b6c0` | 635.8 pt | **84.2 pt**（≈5.8 行） | 592 |
| `G3b` | **v3a** | 6688 | `a7a66cad185a0431` | 578.0 pt | **142.0 pt**（≈10.5 行） | 583 |
| `G1b` | v2（滞后） | 6439 | `6292a4cd5a845f94` | 632.7 pt | **87.3 pt**（≈6 行） | 618 |

口径同 §6.3（用 `[C]` 自己的 `page_body_stats()`）；渲染词数口径同 §4.2（第 1 页 `y > 70pt` 的词）。
**本表四行的"测量值"与"哈希"是同一时刻取的**（口径见下面的教训）。
**第一轮那三份的余量是 49.8 / 58.4 / 18.9 pt**（§4.2）—— 第二轮是它的 **1.3–7.5 倍**，
★Q11 的"留几行余量"这次真的被照做了：`G1b` 自述"初稿只剩 15.0 pt，按 skill 砍了约 60 词"；
`G1c` 自述"自定 ≥5 行，取到 7.3 行"。
**四份都是占位队号 `2401057`** ⇒ §4.1 的"交稿前必换真队号"这条**对第二轮同样成立**。

> ### ⚠️ 本表曾有一行漂移 —— 一条比数字值钱的教训（复审抓出，已更正）
>
> **现象**：`G3b` 那一行原先记的是 `y1 = 563.6 pt` · 余量 `156.4 pt` · 渲染词数 `563`，而同一行的
> 哈希 `a7a66cad185a0431`（6688 B）却是**另一次**取到的。复审重测得 `578.0 / 142.0 / 583`，
> 与哈希同时对得上 —— **根因是：测量发生在写手某次末稿编辑之前，哈希发生在之后**。
> `G3b.tex` 本身没问题（6688 B 与 `a7a66cad185a0431` 两处都对），**是读表的人会被引到错数上**。
>
> **⇒ 规则（本轮加，往后一律照做）**：**凡在同一行里既给测量值又给文件哈希的，
> 必须写明"测量与哈希取自同一时刻"，并且在改过文件之后重取两份。**
> 否则那一行天然会漂：哈希锚住了字节，测量却锚在**旧的编译产物**上（PDF 的 mtime 在旧 `.tex` 上也能是新的）。
> 自查办法：对每行核 `mtime(pdf) >= mtime(tex)`（本表四行在本次更正时全部为真）。

### 8.4 写手自述要点（原始 note 在 `build/abs-green2/G?b-note.md` 与 `G1c-note.md`，各 20–29 KB）

- **读了 v3 的三份**（`G1c` / `G2b` / `G3b`）：清单**逐条打勾**（G1c 与 G2b 都是"全部打勾"，G3b 逐条列了「怎么查」实际动作）；
  ★Q6 一致报告"零公式、零符号、零下标"（并各自贴了 5–13 组改前/改后对照）；
  ★Q9 一致剔除了 `G=700N` vs `616N`、`1.14` vs 三峰、`RSA=0.02<0.05` 与自家阈值反向 这三处矛盾数。
- **对 Q6 的保留意见有两种，都要记**：
  - `G1b`（读的是 v2）：**有保留** —— 原话"`d = T·Nd·D·G·km` 是全文枢纽、是「模型」的唯一压缩表示……
    我认为 skill 把话说过重了"，最后照做的理由是**代价不对称**（写该式必须解释 6 个符号，一解释就成符号表）。
  - `G1c`（读的是 v3）：**无保留**，但它给出了另一条真实代价 ——
    *"符号一去掉，摘要与正文的记号就断了（`Nd`/`CI`/`RS` 在摘要里叫 daily crossings / reliability interval /
    pairwise log-ratio，读者要自己映射约 6 个说法）"*，并明说"若有人反对这条配方，我的反对意见是这个"。
- **共同发现的口径缺口（已登记，本轮**未**改 skill —— 属"扩范围"，留给 controller 裁决）**：
  ① **Q1/Q8 与 Q6 在"带单位的量"上打架**：不排符号就只能把 `σH = 1.8 N/mm²` 换算成"约 2%"或整条丢掉
  （G1b 选了换算并标为派生值；G1c 自定"把单位写成词"，得到 `89.45 newtons per square millimetre`）。
  ② **Q7「逐问作答」× Q11「一页」在子问多的题上正面冲突**（G2b：C 题 10 子问 ÷ 550–650 词 ≈ 每问 60 词；
  G3b：8 个子问里 5 个 missing，"一问一句"必然超页）—— skill 没给"作答粒度/集体标缺能不能一句盖全部"的口径。
  ③ **Q9 两步法覆盖不到两类矛盾**（点估计落在自家区间端点；两个各自干净的数隔着模型链互相矛盾 —— 后者的典型是
  主办国效应 `+74.76` 与 2028 预测 `+16`）。
  ④ **Q8 字面 grep 与 Q12 可读性顶牛**（G1c 真撞到：正文写 `0.030`、摘要写 `3.0%` 被判 NOT FOUND，
  按最严口径改回。skill 没说"等价改写算不算回指"）。
  ⑤ **Q11 的"550–650 词"是保守目标**（G1c 按本机几何反推本页实际能装 ≈700–715 词），
  且"留几行余量"没有可判阈值（G1c 自定 ≥5 行）。
- **四个写手全部撞到「Read 读不了 PDF」**（报 `[Unsupported Document]` 或 `pdftoppm is not installed`）
  ⇒ 四个都改用"PyMuPDF 渲成 PNG 再 Read"。这一条已被**回写进 `SKILL.md`**（§8.5），
  因为"不可省的一步"必须**可执行**。

#### 8.4.1 ★ 由本轮产物触发的一条**新**失败：摘要自身前后打架（已升级为 `[K]` 的第 15 条）

**这是一次真实失败，不是"口径缺口"**（复审提出，本文件核对过原文与同页渲染）：

| 位置 | 原话 | 与谁冲突 |
|---|---|---|
| `G1c.tex:94` | *"The same model **answers the five further questions**."* | — |
| `G1c.tex:95-96` | *"…we defined a disagreement index but never evaluated it on the Edinburgh data, so that item is **reported as missing and no value is quoted for it**."* | 与上一句"answers the five" |
| `G1c.tex:118` | *"…so a single depth profile of one tread **answers all five questions above**."* | 与 `:95-96` 的标缺**直接对撞**（复审已渲图确认三句同在第 1 页） |

**性质**：同一件事（"一致性那一问有没有被回答"）在摘要里有**两种互斥说法** —— 一处说标缺、不引用数值，
另两处说"回答了全部五问"。读者无从判断结论是哪个。

**⇒ 处置**：已作为**第 15 条 ★** 写进 `SKILL.md`（"摘要自身不许前后打架"，带「怎么查」：
通读一遍专找互相排斥的两句，命中即改）。它**不在判分表 13 条内**，来源记在本节。
RED 侧先例见判分表 §5-⑨（`red-P2` 结果段同句并列 `three abreast` 与 `1.14 people abreast`）——
所以这条是**两侧各出现一次**的失败，够格写成 ★。

> **⚠️ 对 `G1c-note.md` 两处归类的更正（不改 note 正文，那是产物）**：该写手把上面那句
> `answers all five questions above` 判成了 **Q13 的"亮点句"** 并据此打勾，见
> `G1c-note.md:162`（"…我把它判为 Q13 的『亮点句』…"）与 `:167`（"亮点句 = 末句 `so a single depth
> profile of one tread answers all five questions above.`"）。**按本轮新立的第 15 条，这句不是亮点句，
> 而是一次前后打架** —— note 里那两处归类**以本节为准**。写手自己在 `:304` 已如实登记"这句算不算
> 合规是我自己判的"，但没有看出它与同页标缺句的矛盾。

### 8.5 第二轮反哺 `[K]` 的两处（本轮已改）

1. 「亲眼看那一页」在**本机不可执行**（`Read` 读 PDF 缺 poppler）⇒ `SKILL.md` 补上一条可执行命令
   （PyMuPDF 渲 PNG 再 Read）。**这条是本轮新发现的真缺陷**，三个写手独立撞到。
2. `check-summary.py` 在 `页数=1` 时**不报填充率**，而 ★Q11 要求"核余量" ⇒ `SKILL.md` 的 Q11「怎么查」
   已写明"页数 1 时余量要自己量"，量法同 §6.3。

### 8.6 第二轮**不能**声称的（与 §2.3 同样的纪律）

1. **压力场景仍未复测**：RED 的两条压力探针（P1 编数诱惑、P2 搬引言+挑数）在第二轮**同样没有对应物**
   ⇒ "装上 skill 后权威压力还会不会放宽纪律"**本文件（两轮都）不提供证据**。
2. **`G1b` 那一臂测的是 v2，不是 v3**（§8.0）：它的产物**不能**记作 v3 配方的正面证据；
   **"三个写手拿到两版 skill"这件事本身也没查清机制**（只登记了现象与可核证据）。
   ⇒ 本轮的 v3 证据只来自 `G2b` / `G3b` / `G1c`。<br>`G1b` 的产物与机检数字仍然有效（对 `.tex` 的实测），
   它显示的"v2 在 A 题齐全下也没排公式"只作**旁证**：v2 的禁令式在竞争性动机下**是噪声大的**，
   不是必然失败 —— 第一轮同用 v2 的三份就全排了（§8.2）。
3. **网页端（Overleaf）分页仍未核实** —— 余量就是为它留的（§8.3）。
4. 四份仍是**占位队号**（§4.1 的老问题，本轮未变）。

### 8.7 `G1c`：补派的「A 题齐全 × v3」臂（含**版本核对已闭环**）

因为 `G1b` 读到的是滞后的 v2（§8.0），第 4 个写手是为补上**任务书要求的两路之一（A 题齐全）**
而派的；任务书里加了强制步骤：**加载 skill 后必须 `Read` 盘上文件、逐项核对"有没有 Q 编号 / 有没有
`**怎么查**：` 字段"，不一致时以盘上为准。**

**它的核对结论（逐字）**：*"`Skill` 工具给的内容与盘上 `.claude/skills/mcm-abstract/SKILL.md` 一致，
不存在'工具给旧版'的情况。我以盘上那份为准执行，但两份内容相同，所以无取舍。"* 并引了盘上原文
`★ **Q6 不让技术细节占版面**（形状类）` 与它的 `- **怎么查**：…` 行；同时报告任务书给的旧版特征串
`★ 不用技术细节占版面` 在盘上 **grep 0 命中**。

| 项 | 实测 |
|---|---|
| 产物 | `build/abs-green2/G1c.tex`（6606 B / `07eeabb875923fb4`）· `G1c-note.md`（≈29 KB）· `G1c-check.pdf` · `G1c-p1.png` |
| 机检 | 1 页 · A1–A4 全 PASS · `C1=0 C1b=9` · C2–C7 全 0（含 `C6/C6b`）· `RESULT: PASS` · 退出码 0 |
| ★Q6 | 正文 `$`=0、`_`=0、`^`=0、公式环境=0 —— **一个公式、一个下标都没排** |
| ★Q7 | 题面 8 个子问题抄成 8 行逐行对，**8 行全给判定**；其中"一致性"那一问正文只有 `PA` 定义、无值 ⇒ **显式标缺** |
| ★Q9 | 两步法走完：`G=700N` vs `W·g=616N`（实测 616.1，差 13.6%）⇒ 该数不进摘要；`1.14` vs 三峰 ⇒ 取三车道、丢 1.14；`RSA=0.02<0.05` 与自家阈值反向 ⇒ 改用同处干净的 `RS=0.03` 对 `ε=0.05` |
| ★Q11 | 608 词（在 550–650 带内）· 余量 98.6 pt ≈ 7.3 行 |
| ★Q12 | grep 自评词与比较级（16 个词）**全 0 命中** |
| 拼装契约 | **自己实测过**：把模板尾段还原回去再编译 ⇒ **2 页、末页填充率 0.048**（第 2 页只装 `Begin your paper here`）⇒ 印证"自检文件不能带尾段、拼进全文必须还原" |

**它对 Q6 的保留意见（与 G1b 不同，如实并录）**：**没有**"其实还想把主方程排进去"的保留；
它给出的真实代价是另一条 —— *"符号一去掉，摘要与正文的记号就断了（正文的 `Nd`/`CI`/`RS` 在摘要里叫
"daily crossings"/"reliability interval"/"pairwise log-ratio"，读者要自己映射约 6 个说法）"*，
并明说 *"如果哪天有人反对这条配方，我的反对意见是这个，而不是"公式更严谨""*。

> **一处它自己查出、并推翻了我方判分表记录的事实**：`[0.359, 0.996]` 这个区间，`[Q]` §5-① 判"下界
> 不可复现"（按正文写的式子应得 ≈0.957）。`G1c` 用闭式验算证明 **0.359/0.996 是 5/6、α=0.05 的
> Clopper–Pearson 区间**（`Beta(5,2)` 的 0.025 分位 ≈ 0.3589；`0.975^(1/6) ≈ 0.99579`），
> **报出的两个数是对的，写反的是正文那条公式的参数顺序**。
> ⇒ **这与 `[Q]` §5-① 不冲突但值得登记**：`[Q]` 判的是"**公式**得不到 0.359"（成立），
> `G1c` 指出的是"**数**本身是一个标准区间"（也成立）。**判分表原文不动**，本条作为独立观察记在这里。
>
> **本文件已独立验算过这两个分位数**（不采信写手自述）：`Beta(5,2)` 的 CDF 为 `6x⁵ − 5x⁶`
> （pdf ∝ x⁴(1−x) 归一化而来），令其 = 0.025 得 `x = 0.3589…`；`Beta(6,1)` 的 CDF 为 `x⁶`，
> 令其 = 0.975 得 `0.975^(1/6) = 0.995789…` ⇒ 正是 `[0.359, 0.996]`，且这正是
> 5/6、α=0.05 的 Clopper–Pearson 区间。**复现**：
> `python -c "print(0.975**(1/6))"` → `0.995789…`；下界用 `6x^5-5x^6=0.025` 牛顿法解。
