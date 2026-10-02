# Task 3 RED 基线的派发口径与写手自述（`mcm-table`）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何"写手" agent 读过本文件，产出的就不再是 RED 基线。
> 与它同案看待的还有上一级的 `red-green-evidence.md` 与 `README.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是"写手到底读到了什么"：它只能靠**审计写手的自报**。

【来源 —— 照实记】本会话 subagent 的 `.output` 不可靠（先例：`plot-python` 那支实测 0 字节）⇒ 本文件的
 提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**（写手回给调度者那段），
 **不是**从 transcript 文件里机器摘的 ⇒ **没有**机器可复核的"逐字节"保证，只有**转录级**的忠实度声明。

【对原文的唯一加工】写手自述里写了**绝对路径**（含 Windows 用户名），本仓规定证据不写绝对路径 ⇒ 掩码之：
 本仓根 → `<REPO>`，系统临时目录 → `<TMP>`。除此之外**逐字未改**。

【强度声明】"写手是否真的只读了那一份 brief"**只有自报、没有沙箱可证**（另外：**未用 `fork`** —— 三个写手都是
 新起的干净上下文 agent，首条 user 消息就是下面那条提示词本身）。**自报一致 ≠ 已证**。

【环境旁路的如实披露（照先例的强度写，不许省）】"只给两样"说的是**派发那一刻的 user 消息**；
 但写手是本机 Claude Code 的 agent，**会话级共享上下文里另有两处本任务删不掉的可见面**：
 ① **可用 skill 列表里 `mcm-table` 的那一行描述** —— 它点名了**类别名**（"缺三线结构、表宽溢出、表题位置不对、来源没回显"）；
 ② **项目记忆文件 `MEMORY.md`** —— 它点名了本套件的模块名与工具面信息（含本机已装 TeX）。
 这两处**不在**派发消息里，但写手**看得到**。
 **写手看得到 / 看不到的边界（关键）**：看得到的是**类别名与工具名**（"有这几类要求"、"用的是 LaTeX"）；
 **看不到**的是**阈值与规范正文** —— `T1`–`T3` 的读数与边界、`D4`–`D8` 的惯例、**来源回显的注释格式**
 （`% mcm-table-src: …`）、表宽上限的来源（编译时的 `\textwidth`）、判据的 8 条 ID 与口径。
 派发消息没有、skill 描述没有、记忆里也没有。
 **为什么这**不**推翻 RED**：泄的只是"**有**这几类判据"，不是"判据的**边界**在哪"。
 ★ **而且本支实测到一个更强的结论**（见 `red-green-evidence.md`）：**修掉判据的两处假红之后，R1 与 R3 各只剩 `C8` 一条红** ——
 因为它们**能编、用 `booktabs`、无竖线、表题在上、`siunitx` S 列**，那些**本就是称职写手的默认**。
 ⇒ **判据抓的是"非常规写法"，不是"烂表"。** 这句话是本支 RED 最诚实的读法，**别拿"RED 红得多"当质量证明**。

---

## 0. 派发口径（三个写手逐字同一份提示词，只换场景号与输出目录）

```text
Read the brief at <TMP>\m3-table-t3-red\brief-R{n}.md and produce the table and caption it asks for. Write them into <REPO>\tests\skills\table\red\out-R{n}\. Work only from that brief - do not read or write any other file.

Environment fact you may use (not part of the brief): `pdflatex` is on PATH if you want to check that your snippet compiles.

When you are done, reply with a short self-report: what you read, what you produced (file names and sizes), the table design and why, and any issues you hit.
```

**brief 是怎么来的（★ 与图那三支的差别，必须写清）**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`
是**图**的 brief。本支**只改"交付物"那一节**：从"出一张图"改为

```text
Deliverables - write all of these into the output directory:

1. `table.tex` - the LaTeX source for **one table** that answers the question above, as a
   self-contained snippet the author can paste into a paper (do **not** include a preamble;
   assume `booktabs` and `siunitx` are available). Deterministic, no network, no manual steps.
2. `caption.txt` - the table caption, in English, as plain text.
```

**数据段与问题段**（含那张数据表）**逐字保留**（已用"逐行数据比对"验过）⇒ **与另两支载体的同场景可比**。
★ **一处我的疏漏（如实记）**：改交付段时**漏改了 brief 的标题**（仍写 "brief" / 措辞里带 "figure"）——
R3 的写手主动点出了这个不一致（"the brief's heading says 'figure' but the deliverable list says 'one table'"）。
**不影响产出**（写手按交付段办），但记下来。

**只给了三样**：① brief 的路径（临时目录里的副本）② 输出目录 ③ **一件环境事实**（`pdflatex` 在 PATH，可选择自编验证）。
**未给**：`mcm-table/` 整个 skill · `table-style.md` · 判据脚本 · 本任务书 · 任何先例证据。

---

## 1. R1 写手自述（逐字）

```text
Done. Read only the brief `<TMP>\m3-table-t3-red\brief-R1.md`; wrote only the two deliverables into `<REPO>\tests\skills\table\red\out-R1\`.

Files produced
- `<REPO>\tests\skills\table\red\out-R1\table.tex` — 1706 bytes
- `<REPO>\tests\skills\table\red\out-R1\caption.txt` — 372 bytes (one paragraph, also mirrored verbatim inside the LaTeX \caption, with `$L_1$` spelled as "L1" in the plain-text version)

Table design and why
- Single `table` float, caption above, `booktabs` rules (`\toprule/\cmidrule(lr)/\midrule/\bottomrule`), siunitx `S[table-format=1.2]` columns, six data rows A–F. No preamble (self-contained snippet).
- Two-panel header: "Share of land area" spanning the three tier columns, "Nearest neighbour" spanning the last two. Left panel gives the composition (low/medium/high shares as reported, each row sums to 1.00); right panel gives, per district, the closest district and the L1 (Manhattan) distance between composition vectors. This answers both halves of the question in one table: the composition is read directly, and the similarity judgement is supported by a whole-table similarity structure rather than a bare claim — B and D appear as a mutual nearest pair with the smallest distance, marked with a `$\dagger$` and explained in the `\footnotesize` note below the tabular.
- I deliberately did NOT add a "dominant tier" column: for district E the top two tiers are 0.38 vs 0.37, so forcing a label there would misstate a near-tie; the shares let the reader see this.
- Numbers were computed, not assumed: all 15 pairwise L1 distances were recomputed with Python. Confirmed every row sums to 1.0000; the unique minimum is B–D = 0.06; every other district's nearest neighbour is (A→E, B→D, C→F, D→B, E→A, F→C) at distance 0.10. Runner-up pairs A–E and C–F are tied at 0.10, so the B–D judgment is unambiguous.

Verification
- Compile-checked the snippet by wrapping it in a `booktabs`+`siunitx` `article` document in an OS temp dir (outside the deliverable dir, removed afterwards): `pdflatex` reported COMPILE OK with no Overfull/Underfull warnings (only the benign "rerun for cross-references" from the `\label`). The deliverable directory contains exactly the two requested files and nothing else.

Issues hit
- One self-inflicted detour: my first wrapper file was built with `printf`, which ate the `\b`/`\u` sequences and produced a bogus Unicode compile error. Fixed by generating the wrapper with a quoted heredoc; the snippet itself was never at fault.
- Judgment call worth flagging: the brief gives no data source, so the note states the shares are "reported as measured" and defines the L1 metric rather than inventing a citation. I also left the "Table N:" prefix out of caption.txt on the assumption the author's `\caption` supplies the number — if the consumer expects the prefix, that is the one thing to change.
```

## 2. R2 写手自述（逐字）

```text
Done. Read only the brief at `<TMP>\m3-table-t3-red\brief-R2.md`; wrote only into the output dir.

Produced (`<REPO>\tests\skills\table\red\out-R2\`):
- table.tex — 3169 bytes
- caption.txt — 1004 bytes

Table design and why
The brief poses two sub-questions (which factor is most correlated with the disaster count; how similar are the districts), so the single table float carries one caption/label and two panels:
- Panel (a), correlation with the historical disaster count: the four candidate attributes as rows, sorted by |r| descending, with columns Pearson r, Spearman rho, |r| and Rank. The winner, mean slope, is bolded (r = 0.930, rho = 0.943), ahead of infrastructure index (r = -0.777) and vegetation cover (r = -0.744); population density is weak (r = 0.360). Numbers in siunitx S columns; units kept as plain math in the stub headers to stay siunitx-version agnostic.
- Panel (b), similarity of districts: a 6x6 symmetric matrix of Euclidean distances between districts computed on all five standardised attributes (including the count), rows ordered by disaster count, diagonal omitted, each district's nearest neighbour bolded, plus a mean-distance column that exposes D as the outlier (4.27) and E as the most typical (2.62). This answers "similarity" directly rather than by a hand-waved grouping: A-C is the tightest pair (1.59), E-F next (2.28).
- Caption is above the table (standard for tables), states the answer with numbers, and adds the small-sample caveat (n = 6) plus a source echo. A \footnotesize note under the table defines the distance metric and the bold/mean conventions.

Verified numbers independently from the brief's data (Pearson and Spearman per attribute; pairwise standardised distances and means), and confirmed the snippet compiles.

Issues hit (both fixed)
1. `\lvert r\rvert` needs amsmath, which a preamble-free snippet cannot assume — pdflatex failed with "Undefined control sequence". Replaced with `$|r|$` throughout (tex and caption).
2. siunitx `S[table-format=1.3]` overfull each cell by 7.7778pt for negative values (the signed cells in panel (a)). Changed the two signed columns to `S[table-format=-1.3]`; overfull count went to 0.
Final check: compiled with the snippet wrapped in an 11pt article (1in margins, booktabs + siunitx only) — exit 0, zero errors and zero over/underfull boxes; visually inspected the rendered page and both panels lay out correctly.

Note on a judgement call: panel (b) standardises all five attributes including the disaster count, so similarity reflects overall profile rather than the four predictors alone. This is stated explicitly in the caption and the table note; switch to predictors-only if the intent was different.
```

## 3. R3 写手自述（逐字）

```text
Done. Read only the brief (<TMP>\m3-table-t3-red\brief-R3.md); wrote only into <REPO>\tests\skills\table\red\out-R3\.

Files produced
- <REPO>\tests\skills\table\red\out-R3\table.tex — 1420 bytes, self-contained `table` float (no preamble), booktabs + siunitx only.
- <REPO>\tests\skills\table\red\out-R3\caption.txt — 558 bytes, plain-text English caption, identical wording to the \caption{} in table.tex.

Analysis behind the design
- Verified all six districts sum to 1.00 (0.42+0.35+0.23 etc.).
- Scored all 15 district pairs by total-variation distance (half the sum of absolute tier differences). Ranking: B–D 0.03 (minimum), then A–E 0.05 and C–F 0.05, then B–E 0.06, A–F 0.08, ... up to C–D 0.27. So the answer to "which two are most similar" is B and D (0.31/0.44/0.25 vs 0.28/0.47/0.25; max tier gap 0.03). No ties at the minimum, so the judgement is unambiguous; the caption states the runner-up distance scale implicitly by giving the metric.

Table design (one table answering both halves of the question)
- Rows: districts A–F. Columns: District | Low | Medium | High | closest-matching district | its distance.
- The three tier shares are the composition answer; the last two columns are the similarity answer, so the reader sees per-district composition and the B/D verdict in one object without needing a separate 6x6 distance matrix.
- Numeric columns are siunitx `S[table-format=1.2]` for decimal alignment; two-level header with `\cmidrule(lr)` groups "Land-area share by tier" over the three tier columns and "Closest composition" over the two similarity columns; booktabs `\toprule/\midrule/\bottomrule` only, no vertical rules.
- Section header cells wrapped in braces ({Low}, {District}, ...) so siunitx does not try to parse them.
- Metric named and defined in the caption (total-variation distance = half the sum of absolute tier differences), with the direction of the scale stated ("smaller = more similar"), so the numeric column is interpretable without a methods digression.

Verification
- Compile-checked with a throwaway wrapper document in the system temp directory (pasted the snippet in, `\usepackage{booktabs,siunitx}`); pdflatex exit 0, PDF produced, no overfull/underfull boxes and no warnings other than the usual first-run "rerun for cross-references" (the \label). Temp wrapper deleted afterwards; no other files in the repo touched or read.

Issues / notes
- The brief's heading says "figure" but the deliverable list says "one table"; I produced the table plus caption as specified in the deliverable list.
- Minor: my first compile attempt failed because a shell heredoc/printf in my own wrapper emitted a stray ESC byte before \end{document}; that was a fault in my scaffolding, not in table.tex, and the corrected run passes.
- Assumption: "most similar structure" is operationalised as total-variation distance on the three shares. A different metric (e.g. Euclidean) gives the same winning pair B–D (0.0424 vs next A–E 0.0616), so the verdict is robust to the metric choice.
```

---

## 附：可复核的命令（当场跑过）

```text
$ for n in 1 2 3; do python tests/skills/table/check-table-style.py --tex tests/skills/table/red/out-R$n/table.tex; done | grep '^RESULT'
RESULT: FAIL（C8）                      ← R1
RESULT: FAIL（C2,C3,C5,C6,C7,C8）       ← R2
RESULT: FAIL（C8）                      ← R3
```

★ 三份的红集是**判据修掉两处假红之后**的读数（修前是 `C1,C5,C7,C8` / `C1,C2,C3,C5,C6,C7,C8` / `C5,C7,C8`）
—— 修尺那一轮见 `mutate-table-style.py` 的 `## 覆盖（不声称穷尽）` 表与 `bd97fd6`。
