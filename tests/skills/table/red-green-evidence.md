# Task 3 · RED x GREEN 对照证据（`mcm-table`）

本文件由 `tests/skills/table/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。**§1 / §2 / §3 / §5 的机器部分逐格解析自 stdout，不手抄**；**§4 的性质判定、§5 的注释、§6 是手写**（文里已标明）。

## §0 口径（两侧同源同数）

- **场景**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，本支未改写）。R1/R3 同一组数据（六区低/中/高三档构成），R2 另一组数据（五属性 + 历史灾次计数）。
- **同数**：每侧 3 张表，两侧共 6 张；判据清单**现取**（本支 8 条）x 6 张。
- **同一把尺**：`tests/skills/table/check-table-style.py` **一字未改**。工作树 blob `534a775500b7` · `HEAD:` blob `534a775500b7` ⇒ **相同**
- **RED 侧**：三份由**干净上下文的写手**产出（只给 brief 路径 + 输出目录 + 一件环境事实 `pdflatex` 在 PATH；**未给**规范 / 模块 / 判据 / 先例证据）。派发口径与三份自述见 `red/writer-self-reports.md`。**RED 是本任务的自变量** —— `red/out-R{n}/table.tex` 与 `caption.txt` 本轮**未改**（逐个 blob 与 `HEAD` 比对，见下）。
- **GREEN 侧**：由本任务用本规范（`references/table-style.md` 的 `T1`–`T3` / `D4`–`D8`）产出，并过判据 8 条。
- ★ **判据修过三处假红**：`bd97fd6`（2026-10-02）修两处 —— 修前 R1 红集 `{C1,C5,C7,C8}`、R3 `{C5,C7,C8}`、R2 `{C1,C2,C3,C5,C6,C7,C8}`；修后 R1/R3 只剩 `{C8}`、R2 `{C2,C3,C5,C6,C7,C8}`。第三处（`RULES_RE` 不吞可选线宽参数 `\toprule[..]` ⇒ 幻影一行 ⇒ `C5`/`C8` 假红）由 **2026-10-03 全分支终审修复轮 I-1** 修掉，**不影响 R1/R2/R3 的红集**。三处假红各有**正控制**（`fixtures/good-note-after-tabular.tex` · `good-multilevel-leading.tex` · `good-rulethickness.tex`，都全绿）。
- ★ **判据非空泛**的另一条臂（失败方向）：变异驱动器 `mutate-table-style.py` 本轮复跑 = **14/14 真红变异**（`C1`–`C8` 逐条 + 2 条 fail-closed 分支 + 2 条修复边界）+ **6/6 必须绿对照** = **20/20 达预期**；命令与读数见 §7。
- ★ `--skeleton`（可选加分项，设计 §5.3）：本支给了 `mcm-latex-format` 的骨架 `mcm-2027-summary.tex`，逐件读数见 §1/§2 的 `SKEL:` 行 —— **它本就该红**（骨架缺 `booktabs` / `siunitx`，实测 `\toprule` 等未定义），这是**信息行、不进 RESULT**。
- ★ **RED 三份的冻结自证**（`git hash-object` vs `HEAD:`）：

| 文件 | 工作树 blob | `HEAD:` blob | 相同？ |
| :-- | :-- | :-- | :-- |
| `tests/skills/table/red/out-R1/table.tex` | `d3e062075c35` | `d3e062075c35` | 是 |
| `tests/skills/table/red/out-R1/caption.txt` | `00113ccc7a8c` | `00113ccc7a8c` | 是 |
| `tests/skills/table/red/out-R2/table.tex` | `0b8770bf45b5` | `0b8770bf45b5` | 是 |
| `tests/skills/table/red/out-R2/caption.txt` | `3ee5afd6d65b` | `3ee5afd6d65b` | 是 |
| `tests/skills/table/red/out-R3/table.tex` | `64100fa3eb1d` | `64100fa3eb1d` | 是 |
| `tests/skills/table/red/out-R3/caption.txt` | `9d5012c5a008` | `9d5012c5a008` | 是 |

## §1 RED 原始读数（朴素写手 · 无规范）

### R1

表题（`tests/skills/table/red/out-R1/caption.txt`，逐字）：
```text
Vulnerability composition of the six districts. Entries are the share of each district's land area in the low, medium and high vulnerability tiers; the three shares in a row sum to 1.00. The right-hand panel gives each district's nearest neighbour under the L1 (Manhattan) distance between composition vectors; districts B and D are the most similar pair (distance 0.06).
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/red/out-R1/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/red/out-R1/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
PASS  C2  toprule/midrule/bottomrule 齐 · 列说明无 `|`
PASS  C3  `\caption` 在 `\begin{tabular}` 之前（默认位）
PASS  C4  表宽 ≤ 版心：表宽 296.58679pt（4.104in） · 版心 469.75502pt（6.500in） · 占 63.1%
PASS  C5  8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外）
PASS  C6  各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2）
PASS  C7  缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`）
FAIL  C8  一条 `% mcm-table-src: r<行>c<列> <-` 都没有
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 73 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'cmidrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 1 条
RESULT: FAIL（C8）
[exit=1]
```

### R2

表题（`tests/skills/table/red/out-R2/caption.txt`，逐字）：
```text
Correlation of each district attribute with the historical disaster count (a) and pairwise similarity of the six districts (b). Mean slope is by far the strongest correlate of the disaster count (Pearson r = 0.930, rank correlation 0.943), ahead of infrastructure index (r = -0.777) and vegetation cover (r = -0.744), while population density is only weakly related (r = 0.360); steeper, sparsely vegetated and less developed districts therefore record more disasters. In (b) smaller distances mean more similar districts and each district's nearest neighbour is shown in bold: districts A and C form the most similar pair (d = 1.59) and E and F the next closest (d = 2.28), whereas D is the most distinctive district and E the most typical. Attributes in (a) are ranked by |r| and the rank correlation is tied (-0.771) between vegetation cover and infrastructure index; with only six districts these values are indicative rather than conclusive. Source: district attribute data supplied with the brief.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/red/out-R2/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/red/out-R2/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
FAIL  C2  片段里 `tabular` 不唯一（2 个）或解析不出（fail-closed）
FAIL  C3  没有可定位的 `tabular` ⇒ 表题位置无从判（fail-closed）
PASS  C4  表宽 ≤ 版心：表宽 350.77913pt（4.854in） · 版心 469.75502pt（6.500in） · 占 74.7%
FAIL  C5  列说明或行解析不出 ⇒ 无从判（fail-closed）
FAIL  C6  列说明解析不出 ⇒ 无从判（fail-closed）
FAIL  C7  列说明解析不出 ⇒ 无从判（fail-closed）
FAIL  C8  行/列解析不出 ⇒ 无从判覆盖（fail-closed）
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 59 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 6 条
RESULT: FAIL（C2,C3,C5,C6,C7,C8）
[exit=1]
```

### R3

表题（`tests/skills/table/red/out-R3/caption.txt`，逐字）：
```text
Vulnerability composition of the six districts. For each district the low, medium and high columns give the share of its land area falling in each vulnerability tier; the three shares sum to 1.00 in every district. The last two columns name the district whose composition is closest to that district, measured by the total-variation distance (half the sum of the absolute differences over the three tiers), so smaller distances mean more similar structure. Districts B and D form the most similar pair (distance 0.03), differing by at most 0.03 in any tier.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/red/out-R3/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/red/out-R3/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
PASS  C2  toprule/midrule/bottomrule 齐 · 列说明无 `|`
PASS  C3  `\caption` 在 `\begin{tabular}` 之前（默认位）
PASS  C4  表宽 ≤ 版心：表宽 297.75706pt（4.120in） · 版心 469.75502pt（6.500in） · 占 63.4%
PASS  C5  8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外）
PASS  C6  各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2）
PASS  C7  缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`）
FAIL  C8  一条 `% mcm-table-src: r<行>c<列> <-` 都没有
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 73 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'cmidrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 1 条
RESULT: FAIL（C8）
[exit=1]
```

## §2 GREEN 原始读数（本 skill 规范产物）

### G1

表题（`tests/skills/table/green/out-G1/caption.txt`，逐字）：
```text
Vulnerability composition of the six districts. The Low, Medium and High columns give the share of each district's land area in that tier; the three shares sum to 1.00. The right-hand pair of columns names, for each district, the district whose composition is closest and the total-variation distance between the two (smaller = more similar). Districts B and D form the most similar pair, differing by at most 0.03 in any tier.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/green/out-G1/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/green/out-G1/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
PASS  C2  toprule/midrule/bottomrule 齐 · 列说明无 `|`
PASS  C3  `\caption` 在 `\begin{tabular}` 之前（默认位）
PASS  C4  表宽 ≤ 版心：表宽 297.75706pt（4.120in） · 版心 469.75502pt（6.500in） · 占 63.4%
PASS  C5  8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外）
PASS  C6  各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2）
PASS  C7  缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`）
PASS  C8  来源回显覆盖 8×6=48 格全齐（注释 48 条）
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 71 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 0 条
RESULT: PASS
[exit=0]
```

### G2

表题（`tests/skills/table/green/out-G2/caption.txt`，逐字）：
```text
Correlation of each district attribute with the historical disaster count over the six districts. Mean slope is by far the strongest correlate (Pearson $r = 0.930$, Spearman $\rho = 0.943$), ahead of the infrastructure index ($r = -0.777$) and vegetation cover ($r = -0.744$); population density is only weakly related ($r = 0.360$). Attributes are ranked by $|r|$; the rank correlation is tied at $-0.771$ between the infrastructure index and vegetation cover. With six districts these values are indicative rather than conclusive.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/green/out-G2/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/green/out-G2/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
PASS  C2  toprule/midrule/bottomrule 齐 · 列说明无 `|`
PASS  C3  `\caption` 在 `\begin{tabular}` 之前（默认位）
PASS  C4  表宽 ≤ 版心：表宽 379.41382pt（5.250in） · 版心 469.75502pt（6.500in） · 占 80.8%
PASS  C5  5 行 × 6 列 · 列数一致 · 无空格子
PASS  C6  各列小数位集合大小 ≤1（c1:∅ · c2:∅ · c3:3 · c4:3 · c5:3 · c6:0）
PASS  C7  缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`）
PASS  C8  来源回显覆盖 5×6=30 格全齐（注释 30 条）
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 56 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 0 条
RESULT: PASS
[exit=0]
```

### G3

表题（`tests/skills/table/green/out-G3/caption.txt`，逐字）：
```text
Vulnerability composition of the six districts: the share of each district's land area falling in the low, medium and high vulnerability tiers. In every district the three shares sum to 1.00, so the Low, Medium and High columns together describe each district completely. The most similar pair is B and D, whose tier shares differ by at most 0.03 in any tier.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/table/check-table-style.py --tex tests/skills/table/green/out-G3/table.tex --skeleton .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）
被判片段 = tests/skills/table/green/out-G3/table.tex
模板（preamble + 版心 `\typeout` 的来源） = .claude/skills/mcm-table/assets/table-template.tex
规范（缺失值 token 现取处） = .claude/skills/mcm-table/references/table-style.md · D6 token = '--'
------------------------------------------------------------------------------
PASS  C1  pdflatex rc=0（片段在自带模板里编过）
PASS  C2  toprule/midrule/bottomrule 齐 · 列说明无 `|`
PASS  C3  `\caption` 在 `\begin{tabular}` 之前（默认位）
PASS  C4  表宽 ≤ 版心：表宽 175.01682pt（2.422in） · 版心 469.75502pt（6.500in） · 占 37.3%
PASS  C5  7 行 × 4 列 · 列数一致 · 无空格子
PASS  C6  各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2）
PASS  C7  缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`）
PASS  C8  来源回显覆盖 7×4=28 格全齐（注释 28 条）
------------------------------------------------------------------------------
SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 54 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']
------------------------------------------------------------------------------
判据 8 条 · 红 0 条
RESULT: PASS
[exit=0]
```

## §3 对照表（机器抽取）

每个格子 = 状态：绿 = `PASS` / 红 = `FAIL`。同场景同行，RED 与 GREEN 并列；判据 ID 见表头（**现取**）。

| 场景 | 侧 | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | RESULT |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | RED | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 红 | FAIL |
| R1 | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R2 | RED | 绿 | 红 | 红 | 绿 | 红 | 红 | 红 | 红 | FAIL |
| R2 | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R3 | RED | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 红 | FAIL |
| R3 | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |

### §3.1 逐判据明细（判词 + `SKEL` 信息行，机器抽取）

| 场景 | 侧 | 判据 | 状态 | 判词 |
| :-- | :-- | :-- | :-- | :-- |
| R1 | RED | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| R1 | RED | C2 | PASS | toprule/midrule/bottomrule 齐 · 列说明无 `|` |
| R1 | RED | C3 | PASS | `\caption` 在 `\begin{tabular}` 之前（默认位） |
| R1 | RED | C4 | PASS | 表宽 ≤ 版心：表宽 296.58679pt（4.104in） · 版心 469.75502pt（6.500in） · 占 63.1% |
| R1 | RED | C5 | PASS | 8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外） |
| R1 | RED | C6 | PASS | 各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2） |
| R1 | RED | C7 | PASS | 缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`） |
| R1 | RED | C8 | FAIL | 一条 `% mcm-table-src: r<行>c<列> <-` 都没有 |
| G1 | GREEN | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| G1 | GREEN | C2 | PASS | toprule/midrule/bottomrule 齐 · 列说明无 `|` |
| G1 | GREEN | C3 | PASS | `\caption` 在 `\begin{tabular}` 之前（默认位） |
| G1 | GREEN | C4 | PASS | 表宽 ≤ 版心：表宽 297.75706pt（4.120in） · 版心 469.75502pt（6.500in） · 占 63.4% |
| G1 | GREEN | C5 | PASS | 8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外） |
| G1 | GREEN | C6 | PASS | 各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2） |
| G1 | GREEN | C7 | PASS | 缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`） |
| G1 | GREEN | C8 | PASS | 来源回显覆盖 8×6=48 格全齐（注释 48 条） |
| R2 | RED | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| R2 | RED | C2 | FAIL | 片段里 `tabular` 不唯一（2 个）或解析不出（fail-closed） |
| R2 | RED | C3 | FAIL | 没有可定位的 `tabular` ⇒ 表题位置无从判（fail-closed） |
| R2 | RED | C4 | PASS | 表宽 ≤ 版心：表宽 350.77913pt（4.854in） · 版心 469.75502pt（6.500in） · 占 74.7% |
| R2 | RED | C5 | FAIL | 列说明或行解析不出 ⇒ 无从判（fail-closed） |
| R2 | RED | C6 | FAIL | 列说明解析不出 ⇒ 无从判（fail-closed） |
| R2 | RED | C7 | FAIL | 列说明解析不出 ⇒ 无从判（fail-closed） |
| R2 | RED | C8 | FAIL | 行/列解析不出 ⇒ 无从判覆盖（fail-closed） |
| G2 | GREEN | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| G2 | GREEN | C2 | PASS | toprule/midrule/bottomrule 齐 · 列说明无 `|` |
| G2 | GREEN | C3 | PASS | `\caption` 在 `\begin{tabular}` 之前（默认位） |
| G2 | GREEN | C4 | PASS | 表宽 ≤ 版心：表宽 379.41382pt（5.250in） · 版心 469.75502pt（6.500in） · 占 80.8% |
| G2 | GREEN | C5 | PASS | 5 行 × 6 列 · 列数一致 · 无空格子 |
| G2 | GREEN | C6 | PASS | 各列小数位集合大小 ≤1（c1:∅ · c2:∅ · c3:3 · c4:3 · c5:3 · c6:0） |
| G2 | GREEN | C7 | PASS | 缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`） |
| G2 | GREEN | C8 | PASS | 来源回显覆盖 5×6=30 格全齐（注释 30 条） |
| R3 | RED | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| R3 | RED | C2 | PASS | toprule/midrule/bottomrule 齐 · 列说明无 `|` |
| R3 | RED | C3 | PASS | `\caption` 在 `\begin{tabular}` 之前（默认位） |
| R3 | RED | C4 | PASS | 表宽 ≤ 版心：表宽 297.75706pt（4.120in） · 版心 469.75502pt（6.500in） · 占 63.4% |
| R3 | RED | C5 | PASS | 8 行 × 6 列 · 列数一致 · 无空格子（1 处表头占位格除外） |
| R3 | RED | C6 | PASS | 各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2 · c5:∅ · c6:2） |
| R3 | RED | C7 | PASS | 缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`） |
| R3 | RED | C8 | FAIL | 一条 `% mcm-table-src: r<行>c<列> <-` 都没有 |
| G3 | GREEN | C1 | PASS | pdflatex rc=0（片段在自带模板里编过） |
| G3 | GREEN | C2 | PASS | toprule/midrule/bottomrule 齐 · 列说明无 `|` |
| G3 | GREEN | C3 | PASS | `\caption` 在 `\begin{tabular}` 之前（默认位） |
| G3 | GREEN | C4 | PASS | 表宽 ≤ 版心：表宽 175.01682pt（2.422in） · 版心 469.75502pt（6.500in） · 占 37.3% |
| G3 | GREEN | C5 | PASS | 7 行 × 4 列 · 列数一致 · 无空格子 |
| G3 | GREEN | C6 | PASS | 各列小数位集合大小 ≤1（c1:∅ · c2:2 · c3:2 · c4:2） |
| G3 | GREEN | C7 | PASS | 缺失值一律为规范形（`S` 列 `{--}` · 非 `S` 列 `--`） |
| G3 | GREEN | C8 | PASS | 来源回显覆盖 7×4=28 格全齐（注释 28 条） |

**`SKEL`（在 `mcm-latex-format` 骨架 preamble 下再编一遍 —— 信息行，不进 RESULT）**：

| 场景 | 侧 | SKEL 行 |
| :-- | :-- | :-- |
| R1 | RED | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 73 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'cmidrule', 'midrule', 'toprule']` |
| G1 | GREEN | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 71 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']` |
| R2 | RED | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 59 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']` |
| G2 | GREEN | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 56 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']` |
| R3 | RED | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 73 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'cmidrule', 'midrule', 'toprule']` |
| G3 | GREEN | `SKEL: 骨架 = .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex · rc=1 · log 错误 54 条 · Overfull \hbox 0 处 · 未定义控制序列 ['bottomrule', 'midrule', 'toprule']` |

### §3.2 汇总（由 §3 的格子逐格重算）

| 侧 | 红格数（判据 x 表） | 判红的判据 ID（并集） | 全绿表数 |
| :-- | :-- | :-- | :-- |
| RED | 8 | C2、C3、C5、C6、C7、C8 | 0/3 |
| GREEN | 0 | （无） | 3/3 |

## §4 RED 的红逐条点名（硬要求 2：真红 / 级联 / 判据假红-已修）

（红集**机器抽取**自 §1；性质判定是人工判定，逐条写。）

### R1（红集 = `{C8}`）· R3（红集 = `{C8}`）

- **`C8` 一条真红**：RED 写手**从未被告知**来源回显的注释格式
  （`% mcm-table-src: r<行>c<列> <- …`）—— 那是本规范 §3.2 的**产物契约**，写手看不到
  ⇒ 三份里一条都没有 ⇒ 判据判红。**不是"表烂"**。
- 其余 7 条全绿：**能编过 · `booktabs` 三线无竖线 · `\caption` 在 `tabular` 之上 ·
  `siunitx` S 列 · 表宽 ≤ 版心**。
- ★ **修前** R1 红集是 `{C1,C5,C7,C8}`、R3 是 `{C5,C7,C8}`；其中 **`C1`（R1）与 `C5`/`C7`（R1/R3）
  是判据假红**，已由 `bd97fd6` 修掉（`C1` = 量宽把整个 `table` 体塞进 `\settowidth`、表注里的
  `\par` 触发 `Paragraph ended`；`C5`/`C7` = 两级表头的**前导 `&`** 被当空格子）。
  **这两类假红不计入 RED 的红。**

### R2（红集 = `{C2,C3,C5,C6,C7,C8}`）

- **`C2` 一条真的"射程边界"触发项**：R2 做的是**双面板表**（`table` 里**两个** `tabular`），
  而判据声明的覆盖范围是**单 `tabular`** ⇒ `tabular` 不唯一 ⇒ `C2` 红。
  ★ **这是已裁定的射程边界，不是判据缺陷**（R2 写手的双面板设计本身能编过、也美观）——**不许为它放宽判据**。
- **`C3,C5,C6,C7,C8` 五条是级联**：`find_tabular` 对"不唯一"返回 `None` ⇒ 表题位置 / 列数 /
  精度 / 缺失值 / 来源回显**皆无从判 ⇒ fail-closed 红**。它们**不是**五条独立的表缺陷。
- ★ **修前** R2 红集是 `{C1,C2,C3,C5,C6,C7,C8}`；多出来的 **`C1` 是判据假红**（同上），已修，不计入。

### §4 的一句话（本支 RED 最诚实的读法）

三份写手的表**都编得过、都 `booktabs` 三线无竖线、表题都在上、都用 `siunitx` S 列** ——
那些**本就是称职 LaTeX 写手的默认**。⇒ **判据抓的是"非常规写法"（来源回显格式、单 `tabular` 假设），
不是"烂表"。别拿"RED 红得多"当质量证明**（反过来，也别因为"红得少"就以为尺错了 —— 尺另有
14 条变异真红作证，见 §7）。

## §5 两侧 `.tex` 并排逐字 diff（机器抽取 + 人工注释）

**结构读数（机器抽取）**：

| 场景 | R 行数 | R 来源回显注释行 | G 行数 | G 来源回显注释行 |
| :-- | :-- | :-- | :-- | :-- |
| 1 | 34 | 0 | 75 | 48 |
| 2 | 56 | 0 | 51 | 30 |
| 3 | 21 | 0 | 49 | 28 |

### 场景 1：R1 vs G1（`difflib.unified_diff`，逐字）

```diff
--- red/out-R1/table.tex
+++ green/out-G1/table.tex
@@ -1,34 +1,75 @@
-% Vulnerability composition of the six districts.
-% Self-contained snippet: paste into an existing document.
-% Requires: booktabs, siunitx.
+% mcm-table-src: r1c1 <- pasted:r1c1
+% mcm-table-src: r1c2 <- pasted:r1c2
+% mcm-table-src: r1c3 <- pasted:r1c3
+% mcm-table-src: r1c4 <- pasted:r1c4
+% mcm-table-src: r1c5 <- pasted:r1c5
+% mcm-table-src: r1c6 <- pasted:r1c6
+% mcm-table-src: r2c1 <- pasted:r2c1
+% mcm-table-src: r2c2 <- pasted:r2c2
+% mcm-table-src: r2c3 <- pasted:r2c3
+% mcm-table-src: r2c4 <- pasted:r2c4
+% mcm-table-src: r2c5 <- pasted:r2c5
+% mcm-table-src: r2c6 <- pasted:r2c6
+% mcm-table-src: r3c1 <- pasted:r3c1
+% mcm-table-src: r3c2 <- pasted:r3c2
+% mcm-table-src: r3c3 <- pasted:r3c3
+% mcm-table-src: r3c4 <- pasted:r3c4
+% mcm-table-src: r3c5 <- pasted:r3c5
+% mcm-table-src: r3c6 <- pasted:r3c6
+% mcm-table-src: r4c1 <- pasted:r4c1
+% mcm-table-src: r4c2 <- pasted:r4c2
+% mcm-table-src: r4c3 <- pasted:r4c3
+% mcm-table-src: r4c4 <- pasted:r4c4
+% mcm-table-src: r4c5 <- pasted:r4c5
+% mcm-table-src: r4c6 <- pasted:r4c6
+% mcm-table-src: r5c1 <- pasted:r5c1
+% mcm-table-src: r5c2 <- pasted:r5c2
+% mcm-table-src: r5c3 <- pasted:r5c3
+% mcm-table-src: r5c4 <- pasted:r5c4
+% mcm-table-src: r5c5 <- pasted:r5c5
+% mcm-table-src: r5c6 <- pasted:r5c6
+% mcm-table-src: r6c1 <- pasted:r6c1
+% mcm-table-src: r6c2 <- pasted:r6c2
+% mcm-table-src: r6c3 <- pasted:r6c3
+% mcm-table-src: r6c4 <- pasted:r6c4
+% mcm-table-src: r6c5 <- pasted:r6c5
+% mcm-table-src: r6c6 <- pasted:r6c6
+% mcm-table-src: r7c1 <- pasted:r7c1
+% mcm-table-src: r7c2 <- pasted:r7c2
+% mcm-table-src: r7c3 <- pasted:r7c3
+% mcm-table-src: r7c4 <- pasted:r7c4
+% mcm-table-src: r7c5 <- pasted:r7c5
+% mcm-table-src: r7c6 <- pasted:r7c6
+% mcm-table-src: r8c1 <- pasted:r8c1
+% mcm-table-src: r8c2 <- pasted:r8c2
+% mcm-table-src: r8c3 <- pasted:r8c3
+% mcm-table-src: r8c4 <- pasted:r8c4
+% mcm-table-src: r8c5 <- pasted:r8c5
+% mcm-table-src: r8c6 <- pasted:r8c6
 \begin{table}[htbp]
   \centering
-  \caption{Vulnerability composition of the six districts. Entries are the share of
-  each district's land area in the low, medium and high vulnerability tiers; the three
-  shares in a row sum to 1.00. The right-hand panel gives each district's nearest
-  neighbour under the $L_1$ (Manhattan) distance between composition vectors; districts~B
-  and~D are the most similar pair (distance 0.06).}
-  \label{tab:district-vulnerability}
+  \caption{Vulnerability composition of the six districts. The Low, Medium and High
+  columns give the share of each district's land area in that tier; the three shares
+  sum to 1.00. The right-hand pair of columns names, for each district, the district
+  whose composition is closest and the total-variation distance between the two
+  (smaller = more similar). Districts B and D form the most similar pair, differing
+  by at most 0.03 in any tier.}
+  \label{tab:vulnerability-composition}
   \begin{tabular}{l S[table-format=1.2] S[table-format=1.2] S[table-format=1.2] l S[table-format=1.2]}
     \toprule
-    & \multicolumn{3}{c}{Share of land area} & \multicolumn{2}{c}{Nearest neighbour} \\
-    \cmidrule(lr){2-4}\cmidrule(lr){5-6}
-    District & {Low} & {Medium} & {High} & {District} & {$L_1$ distance} \\
+    & \multicolumn{3}{c}{Land-area share by tier} & \multicolumn{2}{c}{Closest composition} \\
+    District & {Low} & {Medium} & {High} & District & {Distance} \\
     \midrule
-    A             & 0.42 & 0.35 & 0.23 & E & 0.10 \\
-    B$^{\dagger}$ & 0.31 & 0.44 & 0.25 & D & 0.06 \\
-    C             & 0.55 & 0.30 & 0.15 & F & 0.10 \\
-    D$^{\dagger}$ & 0.28 & 0.47 & 0.25 & B & 0.06 \\
-    E             & 0.37 & 0.38 & 0.25 & A & 0.10 \\
-    F             & 0.50 & 0.33 & 0.17 & C & 0.10 \\
+    A & 0.42 & 0.35 & 0.23 & E & 0.05 \\
+    B & 0.31 & 0.44 & 0.25 & D & 0.03 \\
+    C & 0.55 & 0.30 & 0.15 & F & 0.05 \\
+    D & 0.28 & 0.47 & 0.25 & B & 0.03 \\
+    E & 0.37 & 0.38 & 0.25 & A & 0.05 \\
+    F & 0.50 & 0.33 & 0.17 & C & 0.05 \\
     \bottomrule
   \end{tabular}
   \par\smallskip
-  \begin{minipage}{\linewidth}
-    \footnotesize
-    \textit{Notes:} Shares are dimensionless fractions of land area, reported as
-    measured. The $L_1$ distance is the sum of absolute differences between two
-    districts' composition vectors (range 0--2); it is computed on the shares as
-    tabulated. $\dagger$ marks the two districts forming the most similar pair.
-  \end{minipage}
+  {\footnotesize Note: shares are dimensionless fractions of land area. ``Distance''
+  is the total-variation distance, half the sum of the absolute tier differences
+  (range 0--1), computed on the shares as tabulated.}
 \end{table}
```

### 场景 2：R2 vs G2（`difflib.unified_diff`，逐字）

```diff
--- red/out-R2/table.tex
+++ green/out-G2/table.tex
@@ -1,56 +1,51 @@
-% Table: drivers of the historical disaster count across six districts.
-% Self-contained snippet (no preamble). Requires: booktabs, siunitx.
+% mcm-table-src: r1c1 <- pasted:r1c1
+% mcm-table-src: r1c2 <- pasted:r1c2
+% mcm-table-src: r1c3 <- pasted:r1c3
+% mcm-table-src: r1c4 <- pasted:r1c4
+% mcm-table-src: r1c5 <- pasted:r1c5
+% mcm-table-src: r1c6 <- pasted:r1c6
+% mcm-table-src: r2c1 <- pasted:r2c1
+% mcm-table-src: r2c2 <- pasted:r2c2
+% mcm-table-src: r2c3 <- pasted:r2c3
+% mcm-table-src: r2c4 <- pasted:r2c4
+% mcm-table-src: r2c5 <- pasted:r2c5
+% mcm-table-src: r2c6 <- pasted:r2c6
+% mcm-table-src: r3c1 <- pasted:r3c1
+% mcm-table-src: r3c2 <- pasted:r3c2
+% mcm-table-src: r3c3 <- pasted:r3c3
+% mcm-table-src: r3c4 <- pasted:r3c4
+% mcm-table-src: r3c5 <- pasted:r3c5
+% mcm-table-src: r3c6 <- pasted:r3c6
+% mcm-table-src: r4c1 <- pasted:r4c1
+% mcm-table-src: r4c2 <- pasted:r4c2
+% mcm-table-src: r4c3 <- pasted:r4c3
+% mcm-table-src: r4c4 <- pasted:r4c4
+% mcm-table-src: r4c5 <- pasted:r4c5
+% mcm-table-src: r4c6 <- pasted:r4c6
+% mcm-table-src: r5c1 <- pasted:r5c1
+% mcm-table-src: r5c2 <- pasted:r5c2
+% mcm-table-src: r5c3 <- pasted:r5c3
+% mcm-table-src: r5c4 <- pasted:r5c4
+% mcm-table-src: r5c5 <- pasted:r5c5
+% mcm-table-src: r5c6 <- pasted:r5c6
 \begin{table}[htbp]
   \centering
-  \small
-  \caption{Correlation of each district attribute with the historical disaster
-  count (a) and pairwise similarity of the six districts (b). Mean slope is by far
-  the strongest correlate of the disaster count (Pearson $r = 0.930$, rank
-  correlation $0.943$), ahead of infrastructure index ($r = -0.777$) and vegetation
-  cover ($r = -0.744$), while population density is only weakly related
-  ($r = 0.360$); steeper, sparsely vegetated and less developed districts therefore
-  record more disasters. In (b) smaller distances mean more similar districts and
-  each district's nearest neighbour is shown in bold: districts A and C form the
-  most similar pair ($d = 1.59$) and E and F the next closest ($d = 2.28$), whereas
-  D is the most distinctive district and E the most typical. Attributes in (a) are
-  ranked by $|r|$ and the rank correlation is tied ($-0.771$) between vegetation
-  cover and infrastructure index; with only six districts these values are
-  indicative rather than conclusive. Source: district attribute data supplied with
-  the brief.}
-  \label{tab:disaster-drivers}
-
-  \textbf{(a) Correlation with the historical disaster count (target)}\\[0.4em]
-  \begin{tabular}{@{}l S[table-format=-1.3] S[table-format=-1.3] S[table-format=1.3] c@{}}
+  \caption{Correlation of each district attribute with the historical disaster count over the
+  six districts. Mean slope is by far the strongest correlate (Pearson $r = 0.930$,
+  Spearman $\rho = 0.943$), ahead of the infrastructure index ($r = -0.777$) and
+  vegetation cover ($r = -0.744$); population density is only weakly related
+  ($r = 0.360$). Attributes are ranked by $|r|$; the rank correlation is tied at
+  $-0.771$ between the infrastructure index and vegetation cover. With six districts
+  these values are indicative rather than conclusive.}
+  \label{tab:disaster-correlates}
+  \begin{tabular}{l l S[table-format=-1.3] S[table-format=-1.3] S[table-format=1.3] c}
     \toprule
-    Attribute (unit)                        & {$r$}  & {$\rho$} & {$|r|$} & {Rank} \\
+    Attribute & Unit & {$r$} & {$\rho$} & {$|r|$} & {Rank} \\
     \midrule
-    \textbf{Mean slope} ($^\circ$)          & 0.930  & 0.943    & 0.930  & \textbf{1} \\
-    Infrastructure index (0--100)           & -0.777 & -0.771   & 0.777  & 2 \\
-    Vegetation cover (fraction of area)     & -0.744 & -0.771   & 0.744  & 3 \\
-    Population density (people\,km$^{-2}$)  & 0.360  & 0.543    & 0.360  & 4 \\
+    Mean slope           & degrees           &  0.930 &  0.943 & 0.930 & 1 \\
+    Infrastructure index & 0--100            & -0.777 & -0.771 & 0.777 & 2 \\
+    Vegetation cover     & fraction of area  & -0.744 & -0.771 & 0.744 & 3 \\
+    Population density   & people\,km$^{-2}$ &  0.360 &  0.543 & 0.360 & 4 \\
     \bottomrule
   \end{tabular}
-
-  \par\vspace{1.1em}
-  \textbf{(b) Similarity of districts (pairwise distance, smaller = more similar)}\\[0.4em]
-  \begin{tabular}{@{}l r r r r r r r@{}}
-    \toprule
-    District (disaster count) & C & A & E & F & B & D & {Mean} \\
-    \midrule
-    C (8)  & --              & \textbf{1.59} & 3.44 & 4.01 & 3.50 & 6.25 & 3.76 \\
-    A (12) & \textbf{1.59}   & --            & 1.91 & 2.78 & 2.65 & 4.87 & 2.76 \\
-    E (16) & 3.44            & \textbf{1.91} & --   & 2.28 & 2.28 & 3.19 & 2.62 \\
-    F (24) & 4.01            & 2.78          & \textbf{2.28} & -- & 3.28 & 3.75 & 3.22 \\
-    B (31) & 3.50            & 2.65          & \textbf{2.28} & 3.28 & -- & 3.28 & 3.00 \\
-    D (38) & 6.25            & 4.87          & \textbf{3.19} & 3.75 & 3.28 & -- & 4.27 \\
-    \bottomrule
-  \end{tabular}
-
-  \par\vspace{0.5em}
-  {\footnotesize
-  Note: distances in (b) are Euclidean in units of pooled standard deviations over
-  all five attributes, including the disaster count; the diagonal is omitted; bold
-  marks each district's nearest neighbour; the right-hand column is the mean
-  distance from that district to the other five. Columns in (b) follow the same
-  order as the rows.}
 \end{table}
```

### 场景 3：R3 vs G3（`difflib.unified_diff`，逐字）

```diff
--- red/out-R3/table.tex
+++ green/out-G3/table.tex
@@ -1,21 +1,49 @@
-% Table: vulnerability composition of the six districts.
-% Self-contained snippet; requires \usepackage{booktabs} and \usepackage{siunitx}.
+% mcm-table-src: r1c1 <- pasted:r1c1
+% mcm-table-src: r1c2 <- pasted:r1c2
+% mcm-table-src: r1c3 <- pasted:r1c3
+% mcm-table-src: r1c4 <- pasted:r1c4
+% mcm-table-src: r2c1 <- pasted:r2c1
+% mcm-table-src: r2c2 <- pasted:r2c2
+% mcm-table-src: r2c3 <- pasted:r2c3
+% mcm-table-src: r2c4 <- pasted:r2c4
+% mcm-table-src: r3c1 <- pasted:r3c1
+% mcm-table-src: r3c2 <- pasted:r3c2
+% mcm-table-src: r3c3 <- pasted:r3c3
+% mcm-table-src: r3c4 <- pasted:r3c4
+% mcm-table-src: r4c1 <- pasted:r4c1
+% mcm-table-src: r4c2 <- pasted:r4c2
+% mcm-table-src: r4c3 <- pasted:r4c3
+% mcm-table-src: r4c4 <- pasted:r4c4
+% mcm-table-src: r5c1 <- pasted:r5c1
+% mcm-table-src: r5c2 <- pasted:r5c2
+% mcm-table-src: r5c3 <- pasted:r5c3
+% mcm-table-src: r5c4 <- pasted:r5c4
+% mcm-table-src: r6c1 <- pasted:r6c1
+% mcm-table-src: r6c2 <- pasted:r6c2
+% mcm-table-src: r6c3 <- pasted:r6c3
+% mcm-table-src: r6c4 <- pasted:r6c4
+% mcm-table-src: r7c1 <- pasted:r7c1
+% mcm-table-src: r7c2 <- pasted:r7c2
+% mcm-table-src: r7c3 <- pasted:r7c3
+% mcm-table-src: r7c4 <- pasted:r7c4
 \begin{table}[htbp]
   \centering
-  \caption{Vulnerability composition of the six districts. For each district the low, medium and high columns give the share of its land area falling in each vulnerability tier; the three shares sum to 1.00 in every district. The last two columns name the district whose composition is closest to that district, measured by the total-variation distance (half the sum of the absolute differences over the three tiers), so smaller distances mean more similar structure. Districts B and D form the most similar pair (distance 0.03), differing by at most 0.03 in any tier.}
-  \label{tab:district-vulnerability-composition}
-  \begin{tabular}{l S[table-format=1.2] S[table-format=1.2] S[table-format=1.2] l S[table-format=1.2]}
+  \caption{Vulnerability composition of the six districts: the share of each district's land area
+  falling in the low, medium and high vulnerability tiers. In every district the three
+  shares sum to 1.00, so the Low, Medium and High columns together describe each district
+  completely. The most similar pair is B and D, whose tier shares differ by at most 0.03
+  in any tier.}
+  \label{tab:vulnerability-shares}
+  \begin{tabular}{l S[table-format=1.2] S[table-format=1.2] S[table-format=1.2]}
     \toprule
-    & \multicolumn{3}{c}{Land-area share by tier} & \multicolumn{2}{c}{Closest composition} \\
-    \cmidrule(lr){2-4} \cmidrule(lr){5-6}
-    {District} & {Low} & {Medium} & {High} & {District} & {Distance} \\
+    District & {Low} & {Medium} & {High} \\
     \midrule
-    A & 0.42 & 0.35 & 0.23 & E & 0.05 \\
-    B & 0.31 & 0.44 & 0.25 & D & 0.03 \\
-    C & 0.55 & 0.30 & 0.15 & F & 0.05 \\
-    D & 0.28 & 0.47 & 0.25 & B & 0.03 \\
-    E & 0.37 & 0.38 & 0.25 & A & 0.05 \\
-    F & 0.50 & 0.33 & 0.17 & C & 0.05 \\
+    A & 0.42 & 0.35 & 0.23 \\
+    B & 0.31 & 0.44 & 0.25 \\
+    C & 0.55 & 0.30 & 0.15 \\
+    D & 0.28 & 0.47 & 0.25 \\
+    E & 0.37 & 0.38 & 0.25 \\
+    F & 0.50 & 0.33 & 0.17 \\
     \bottomrule
   \end{tabular}
 \end{table}
```

**人工读一遍：差异是不是"规范导致"的？**

- **规范导致的差异（可归因）**：
  1. GREEN 的 `.tex` **多出一段** `% mcm-table-src: …` 来源回显注释（G1 48 条 / G2 30 条 / G3 28 条），
     RED **一条都没有** —— 这是**规范唯一显式新增的可见文本**，直接对应 `C8`。
  2. RED 的表里**没有**缺失值判据要管的格子；GREEN 的表里**也没有** —— ⇒ **`D6`/`C7` 未被本支 GREEN
     的数据触发**（如实说；`C7` 的真红作证在变异驱动器 `MUT-C7a`/`MUT-C7b`，见 §7）。
- **设计 / 场景导致的差异（不是规范要求）**：
  1. R2 有**两个** `tabular`（双面板），G2 只有**一个** —— GREEN 侧的**单表设计约束**来自判据的 `C2`
     射程（单 `tabular`），**不是**我判 R2 错。
  2. **距离度量不同**（RED R1 用 L1、距离 0.06/0.10；GREEN 用 total-variation、距离 0.03/0.05），
     表题措辞也不同 —— 判断层动作。
  3. G1 保留**两级表头 + 表注**；G3（R3 同数据的 "paper-ready" 场景）用**紧凑单级**四列表、
     把"最相似的一对"放进 caption。
- **结论**：两侧差异**集中在**（a）来源回显注释（规范契约）、（b）单/双 `tabular` 与度量/措辞（设计选择）；
  **不是**三线结构 / 表宽 / 表题位置的差异 —— 那几项**两侧都合规**（见 §3 的 `C2`/`C3`/`C4` 列）。

## §6 看图记录（硬要求 5：亲眼看表）

**这一节是判断层，机械判据判不了它。** 下面是本任务 agent 把**六张表逐张编译、渲成 150dpi PNG、
亲眼看过**之后写下的。**本节手写，不是机器抽取。** PNG 落在各自 `out-*/` 目录（PNG 非字节可复现：
每次重编带新时间戳，本支不拿它当判据）。

### RED（朴素写手 · 无规范）—— 我从这张表读到了什么

- **R1（`red/out-R1/table.png`）**：读到六区**低/中/高三档构成**，以及每个区**最近的相邻区与其 L1 距离**；
  B、D 互为最近（0.06）并用 `$\dagger$` 标注。**三线（`\toprule` / `\cmidrule` / `\midrule` /
  `\bottomrule`）粗细得当**；版心占 **63%**、不爆；`siunitx` S 列**小数位对齐**；上下标**没掉**
  （`$L_1$` 下标、`$\dagger$` 上标都正常）；**表注（Notes）在 `tabular` 之下、与表紧邻**
  （表注没与表头挤在一起）。**判据不报、眼睛看得见**：无。
- **R2（`red/out-R2/table.png`）**：读到**两个面板** ——（a）四个属性与灾次计数的 `$r$` / `$\rho$` /
  `$|r|$` / Rank；（b）**6x6 对称距离矩阵**，对角线用 `--` 省去、最近邻**加粗**。负数**对齐**、单位列正常；
  版心占 **74.7%**、不爆；表注在下方。**判据不报、眼睛看得见**：（b）面板 8 列，**两个面板共享一个
  caption**，读起来像"一张表两件事"—— 这是写手的**判断层**选择，判据不管（也不该管）。
- **R3（`red/out-R3/table.png`）**：与 R1 **同形同数据**（两级表头 + 最近邻列），措辞不同；
  ★ **距离度量不同** —— R1 那一列是 `$L_1$`（Manhattan，B–D = 0.06）、R3 是 **total-variation**
  （B–D = 0.03）⇒ **两列里的数字并不相等**；**判据读数**同 R1（红集皆为 `{C8}`）。版心占 **63.4%**。
- ★ **一句话**：三张 RED 表**视觉上都是好表** —— 判据红的是"**没有来源回显**"（R1/R3）与
  "**双 `tabular` 超出判据射程**"（R2），**不是表本身读不清**。

### GREEN（本 skill 规范产物）—— 我从这张表读到了什么

- **G1（`green/out-G1/table.png`）**：读到与 R1 同任务的答案（构成 + 最近邻 + **TV 距离** 0.03/0.05）；
  两级表头（首格留空 + 两个 `\multicolumn` 分组行，**无 `\cmidrule` 分组线**）**对齐、没挤在一起**；
  表宽 **63.4%**、不爆；小数位对齐（本表无上下标）；**表注在表下、紧邻**。**判据不报、眼睛看得见**：
  caption（满 `\textwidth`）比表（4.12in）宽，表在版心里居中 —— 正常排版，非缺陷。
- **G2（`green/out-G2/table.png`）**：读到**四属性与灾次计数的相关系数**表（`$r$` / `$\rho$` /
  `$|r|$` / Rank）；**负数（infrastructure / vegetation）带负号且对齐**；单位列 `0--100`、
  `people km$^{-2}$` 正常；版心占 **80.8%**（本支最宽的一张，仍不爆）。**判据不报、眼睛看得见**：无。
- **G3（`green/out-G3/table.png`）**：读到**紧凑四列构成表**（District / Low / Medium / High），
  仅 **37%** 版心宽。**判据不报、眼睛看得见**：表**本身不含"最相似的一对"**（这条判断在 caption 里）
  —— 是 "paper-ready 单表" 的**设计选择**（单 `tabular` 里放不下相似度列时，把判断交给 caption）。
- ★ **一句话**：GREEN 三张**全绿**且**读得出任务答案**。

### 总一句话

**机械层测的是"形态合不合规范"，判断层测的是"表讲没讲清"。** 本支两侧**形态都基本合规范**
（RED 仅缺来源回显 / 超出单表射程），**判断层也都讲清了** —— "判词全绿 ≠ 表讲清了"这条在本支
**没有**被逼出一个反例（这本身是如实读数，不是结论）。

## §7 生成器 · 判据非空泛 · 不动点

- 本文件的机器部分由 `make-evidence.py` **当场跑** `check-table-style.py` 生成（`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout。

- ★ **判据非空泛（失败方向的另一条臂）** —— `mutate-table-style.py` **当场跑过**，读数为（**逐字**摘其合计段；全量输出含每条变异的检查器原文，从略）：

```
$ python tests/skills/table/mutate-table-style.py
MUT: 14/14 红（check-table-style.py 的 C1–C8 逐条打红 + 2 条 fail-closed 分支打红 + 2 条修复边界打红：`MUT-C1b`/`MUT-LEAD-a`）
MUT: 对照 6/6 达预期（必须绿：射程边界 + C3 覆盖口径 + `\multicolumn` 合规表 + 前导 `&` 两级表头 + `\end{tabular}` 后表注 + 可选线宽参数合规表）
MUT: 合计 20/20 达预期（合计）
RUN: 受保护件 blob 逐件还原=True · 基准样本复跑 exit=0 · 全仓 `git status --short` 空
```

  ⇒ 其中 **14 条是「真红」变异**（`C1`–`C8` **逐条**有真红 + `MUT-FC1`/`MUT-FC2` 两条 fail-closed 分支 + `MUT-C1b`/`MUT-LEAD-a` 两条修复边界），**6 条是「必须绿」的对照**；合计 **20/20 达预期**。（「驱动器 20 条变异」是**并集口径**；分开看是 **14 真红 + 6 对照**。对照里 `CTRL-GREEN-f`（可选线宽参数合规表）是 **2026-10-03 全分支终审修复轮 I-1** 新增（`RULES_RE` 吞 `[..]`）。）

- **重跑不动点**：在已提交的树上重跑本生成器 ⇒ 本文件**逐字节不变**（证法：跑后 `git status --short` 仍为空；见本任务报告）。
