# Task 2 RED 基线的派发提示词与写手/判者自报（抢救件）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件逐字收录**写手自己对规范表的引述** —— 作废轮的写手自报里抄了 H1-H13 的阈值，
> 并写明"是按这些阈值选的"。任何"写手" agent 读过本文件，产出的就不再是 RED 基线。
> **与它同案看待的还有** `red-evidence.md` / `judge.md` / `README.md`（点名清单见
> `README.md` 文首警示头）。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是"写手到底读到了什么"：
  它只能靠**审计原文**。而这些原文（subagent transcript）在仓外、且 `.superpowers/` 是
  gitignored ⇒ 不搬进受版本控制的目录就随时会丢。本文件由
  `rescue-transcripts.py` 从 transcript 一次性摘录。

【摘录口径】每个 agent 两段，均为原文，**本脚本不加删节**：
  ① 首条 `user` 消息 = 派发的提示词（对本轮，它就是**单独一行**提示词本身 ——
     这一点同时**可复核"未用 fork"**：`fork` 会继承主 agent 上下文，首条消息会是长篇上下文）；
  ② `SubagentHandback` 的 `message` = 它回给调度者的完整报告。
  **不等于"文件里没有省略号"**：文件里出现的省略号（三个句点）**全部**在两段引用
  **内部** —— 是原文作者自己写的简写，如命令行里的图路径、md5 前缀；**本脚本一处未删**
  （逐处计数见 `red-evidence.md` §11，附可复跑的命令）。

【对原文的加工 —— **只有一种**，且逐处计数】写手自己写了**绝对路径**（含 Windows 用户名与
  系统临时目录），本仓规定报告与证据不写绝对路径，故掩码之：仓外临时目录 → `<TMP>/m3-t2-red`，
  仓内根 → `<REPO>`。**本文件共掩码 15 处**，除此之外两段引用**逐字节未改、未软换行**。
  （本文件里**不是原文**的只有脚本写的那几行：文首这几段【】说明与警示块、每个 agent 的
  标题/说明/`transcript`/`字符数` 行。）

【强度声明（不许下游读过头）】①②是**原文**，但"写手是否真的只读了那一份 brief"
**只有自报、没有沙箱可证**（没有文件系统审计、没有 syscall 记录）。
自报一致 ≠ 已证；本文件能做的是：把自报存下来，让下游能自己判断。

---

==============================================================================
## R1-writer-voided-round-1

- 说明：作废轮 R1 写手（读到了仓内规范；产物已删除）
- transcript：`agent-ae596db8d1fadaf74.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**212** 字符（原文；掩码后 212）
- SubagentHandback：**3186** 字符（原文；掩码后 3186）

### ① 派发提示词（原文）

```text
Read the brief at tests/skills/figure-choose/red/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R1/.
```

### ② 自报 / 报告（原文）

```text
R1 done. Three deliverables written into `tests/skills/figure-choose/red/out-R1/` (untracked, not committed):

- `make_figure.py` — regenerates figure + caption from the brief numbers, offline, single command (`python make_figure.py`), writes into its own directory.
- `figure.pdf` — vector, page box exactly 6.31 × 2.60 in (aspect 2.43).
- `caption.txt` — `Figure 1: District vulnerability composition; B and D are most similar` (11 words, ASCII colon, no trailing period, LF newline).

**Figure design (two panels, 3 non-grey colours)**
- (a) 100 % stacked horizontal bars, districts sorted by low-tier share ascending (D, B, E, A, F, C), share printed inside each segment, x-axis "Share of district area (%)" — this is the composition description.
- (b) 6×6 pairwise L1 distance matrix in *grey only* (grey pixels are excluded by the F2 counter), integer percentage points printed in every cell, with the minimum cell boxed (B–D, both mirror cells). This is the evidence for the "which two are most similar" judgement; no colourbar needed, so panel (b) adds zero coloured ink.
- Palette: ColorBrewer YlOrRd 3-class (`#ffeda0/#feb24c/#f03b20`), ordinal and colour-blind-safe; serif text (DejaVu Serif); all fonts ≥7 pt; top/right spines removed; legend above panel (a).

**Answer the figure supports:** B–D are the most similar pair (L1 = 0.06, i.e. 6 pp; row sums all 1.00). Runner-ups A–E and C–F at 0.10. Every value in the matrix was cross-checked against `.superpowers/sdd/m3-t2-truth.py` — all 15 off-diagonal cells match.

**Verification (actually run, not asserted)**
- `python tests/skills/figure-choose/check-figure-style.py --fig .../figure.pdf --caption @.../caption.txt --textwidth-in 6.31` → `RESULT: PASS`, all of F1 (ratio 1.000) / F2 (3 colours) / F3a / F3b (11 words) / F3c / F3d PASS, exit 0. Also PASS at denominators 5.76 / 6.50 / 7.19 (ratio 1.000 passes for any denominator in 5.26–7.89).
- Determinism: byte-identical across repeated runs (figure.pdf md5 `f88fdafd8e7776e554e50134ced7daea`; PDF CreationDate/ModDate suppressed), caption LF-only, no network, no input files.
- Deleted and regenerated from clean to confirm no manual step.

**Two things you need to know**
1. **This is not a clean naive RED product.** While orienting in the repo I read `tests/skills/figure-choose/check-figure-style.py`, `fixtures/expected.tsv`, the recon files under `tests/figures-recon/`, and the `.superpowers/sdd/task-m3-t3-brief.md` house-style table (H1–H13: width ≤1.2× column, no pie charts, ≤4 colours, ≤12-word captions, aspect 2–3, ≥7 pt). I deliberately conformed to all of them. A genuinely naive R1 run would most likely fail several of these (default `figsize=(10,6)` → F1 red; caption with a full stop → F3c red; possibly a pie chart). So this output understates the RED baseline — if the RED baseline is meant to be skill-free, re-dispatch to a fresh agent told to read only the brief, or run it in a clean checkout.
2. I shipped **PDF only, no PNG**. The checker requires an explicit `--dpi` for PNG; a 300 dpi PNG measured at the wrong assumed dpi fails F1, whereas the PDF page box is dpi-independent. Say the word if you also want a PNG and at which dpi.

```

==============================================================================
## R2-writer-voided-round-1

- 说明：作废轮 R2 写手（读到了仓内规范；产物已删除）
- transcript：`agent-aeed32664fe4cef1a.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**212** 字符（原文；掩码后 212）
- SubagentHandback：**4004** 字符（原文；掩码后 3964）

### ① 派发提示词（原文）

```text
Read the brief at tests/skills/figure-choose/red/brief-R2.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R2/.
```

### ② 自报 / 报告（原文）

```text
R2 figure + caption produced. Files (all new, untracked, nothing committed):

- <REPO>\tests\skills\figure-choose\red\out-R2\make_figure.py
- <REPO>\tests\skills\figure-choose\red\out-R2\figure.pdf   (primary, vector, 6.30 x 2.80 in)
- <REPO>\tests\skills\figure-choose\red\out-R2\figure.png   (convenience preview, 300 dpi)
- <REPO>\tests\skills\figure-choose\red\out-R2\caption.txt

WHAT THE FIGURE IS
One landscape row, three panels, 6.3 x 2.8 in (page box; the script deliberately does not use bbox_inches="tight" so the saved canvas is exactly the size asked for):
- (a) four horizontal bars = Pearson r of each factor vs. disaster count, sorted, strongest on top; slope highlighted in the single accent colour (#B3402E), everything else grey; values printed at the bar ends.
- (b) the winning factor as raw data: mean slope vs. disaster count scatter, districts A-F labelled, OLS line, r and p in-panel.
- (c) average-linkage (UPGMA) dendrogram over the z-scored attribute profiles = the district-similarity answer.
A grey footnote under panel (a) states that vegetation cover and infrastructure index are collinear (r = 0.98), because that qualification is load-bearing for "which factor" and should not live only in prose.

NUMBERS THE FIGURE RESTS ON (recomputed by the script, printed to stdout on every run)
- mean slope: r = +0.930, p = 0.0071  <- the answer; the only factor significant at 5%
- infrastructure index: r = -0.777, p = 0.0693
- vegetation cover: r = -0.744, p = 0.0902
- population density: r = +0.360, p = 0.4834
- vegetation ~ infrastructure: r = +0.980 (near-duplicate columns; slope is itself correlated with both, so the data cannot cleanly separate the three - this is the main caveat on the headline claim)
- closest district pair: A-C at z-scored Euclidean distance 1.410 (then B-E at 1.633), i.e. A and C are the most alike, D is the outlier.

VERIFIED (not asserted)
- Determinism: ran the script twice from the repo root; md5 of figure.pdf and figure.png identical across runs. The PDF is saved with metadata={"CreationDate": None} precisely so the hash comparison is meaningful. Script writes next to itself via __file__, so cwd does not matter and there are no manual steps. Offline: only numpy/matplotlib/scipy.
- Criteria checker (read-only) run on the PDF: F1 0.998 PASS, F2 colour count 1 PASS, F3a PASS, F3c PASS, F3d PASS, **F3b FAIL - caption is 13 words, threshold is 12** (soft limit 12, hard 17). RESULT: FAIL (F3b), exit 1. Same result on the PNG with --dpi 300. I left the caption at 13 words because that is the wording I judged best ("Figure 1: Slope is the top disaster correlate; A and C are closest"); it is one word over. If you want a clean pass for the RED run, trimming to e.g. "Figure 1: Slope is the top disaster correlate; A and C nearest" is a one-word edit in caption.txt.

CONTAMINATION CAVEAT - please weigh this before using the artifact as a RED baseline
Lessons §二.8 says a RED subagent should receive only the scenario text. I was given the brief plus free rein in the repo, and before drawing anything I read the M3 design spec (docs/superpowers/specs/2026-09-27-m3-figure-choose-design.md), the checker source (tests/skills/figure-choose/check-figure-style.py) and the fixtures. So this artifact is NOT a clean no-skill baseline: knowing the future house style almost certainly influenced three choices that happen to line up with it - figure width at paper text width (6.3 in), a deliberately restrained palette (one accent + greys), and a short result-bearing single-line caption. What I did NOT do is tune against the checker's thresholds (I did not check colour count or word count while designing; the 13-word caption fails as written). Treat the judgement layer here ("did it pick a sensible chart type for multivariate correlation / did it split panels") as usable, and the mechanical layer as contaminated. If a clean RED is needed, re-run with a fresh agent given only brief-R2.md.
```

==============================================================================
## R3-writer-voided-round-1

- 说明：作废轮 R3 写手（读到了仓内规范；产物已删除）
- transcript：`agent-a519891fc821ef523.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**212** 字符（原文；掩码后 212）
- SubagentHandback：**2908** 字符（原文；掩码后 2898）

### ① 派发提示词（原文）

```text
Read the brief at tests/skills/figure-choose/red/brief-R3.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into tests/skills/figure-choose/red/out-R3/.
```

### ② 自报 / 报告（原文）

```text
Done. Brief R3 figure + caption produced in `<REPO>\tests\skills\figure-choose\red\out-R3\` — three files, nothing extra:

- `make_figure.py` — self-contained, offline, no manual steps, resolves paths from `__file__` (verified running from `D:\`)
- `figure.pdf` — one page, exactly 6.00 × 2.60 in (aspect 2.31), fonts embedded as TrueType (Type 42, submission-safe)
- `caption.txt` — `Figure 1: (a) Vulnerability-tier composition by district; (b) pairwise L1 distance`

**Design.** Two panels, both answering the brief. (a) 100 % stacked horizontal bars, one per district A–F, with the three tier shares printed inside each segment — composition readable directly. (b) 6×6 pairwise L1 distance matrix between the share vectors, grayscale-shaded, all values annotated, the minimum pair boxed. No pie chart (composition data is the classic pie trap). Tier colours are an ordinal 3-step ColorBrewer Blues ramp (`#c6dbef / #6baed6 / #2171b5`, light = low vulnerability), not the matplotlib default qualitative cycle — the tiers are ordered, so an ordered ramp is what carries the meaning.

**The substantive finding** (printed by the script): the most similar pair is **B–D, L1 = 0.06** — they differ by only 0.03 in low share, 0.03 in medium, and 0.00 in high. Runners-up are A–E and C–F, tied at 0.10. The gap (0.06 vs 0.10) is what justifies "most similar" rather than "similar".

**Verification (commands actually run).**
- `python tests/skills/figure-choose/check-figure-style.py --fig .../figure.pdf --caption @.../caption.txt --textwidth-in 6.31` → `RESULT: PASS`, exit 0 — F1 0.951 · F2 3 colours · F3a/b/c/d all PASS.
- Determinism: reran 3× and diffed bytes. First attempt was *content*-deterministic only — the three files differed by 3 bytes in the PDF `/CreationDate`. Fixed with `savefig(metadata={"CreationDate": None})`; now md5 is identical (`8128f170...`) across reruns.
- Page box re-read from the PDF with fitz: 432 × 187.2 pt = 6.00 × 2.60 in.

**One thing you should know before you use this as a RED baseline.** Before writing anything I read `tests/skills/figure-choose/check-figure-style.py` and `docs/superpowers/specs/2026-09-27-m3-figure-choose-design.md` (they are checked-in repo files, and I checked them to understand the output directory's conventions). Having seen the mechanical criteria, I designed directly against them — the 6.00 in page width, the ≤4-colour palette, the 11-word caption and the ASCII `Figure 1:` were all chosen knowing the thresholds. So this artifact is **not** a skill-free/naive RED baseline; it is closer to what a GREEN run should look like. If `out-R3` is meant to demonstrate that an unaided agent produces a non-compliant deliverable, this run does not demonstrate that and the baseline should be regenerated by an agent with no access to the checker or the spec. I did not modify the checker, the fixtures, or anything outside `out-R3`.
```

==============================================================================
## R1-writer-round-2

- 说明：有效轮 R1 写手（本 RED 基线的来源）
- transcript：`agent-abddc522a216dd8d0.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**309** 字符（原文；掩码后 247）
- SubagentHandback：**3161** 字符（原文；掩码后 3129）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t2-red/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R1/. Work only from that brief - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
Done. Deliverables written to <TMP>/m3-t2-red/out-R1/: make_figure.py, figure.pdf, figure.png, caption.txt.

FIGURE CHOICE
Two panels, both read off the same numbers:
- (a) 100% stacked horizontal bars, districts A-F, segments labelled with their exact shares. This answers "describe the composition of each district" directly and shows the shares sum to 1.00.
- (b) The six districts as points in the low-medium-high simplex (ternary diagram) - the natural geometry for a three-part composition, since every district is one point and similarity of structure is literally proximity. This is what makes the similarity judgement readable rather than asserted.
The pair judged most similar (B-D) is circled and joined; the evidence line above the triangle gives the distance, the two runners-up, and the floor for all remaining pairs, so the ranking behind the judgement is visible in the figure itself.

ANSWER THE FIGURE SUPPORTS
B and D are the most similar pair, and the judgement is metric-independent:
- Aitchison distance (Euclidean distance between centred log-ratios, the standard metric for shares): B-D = 0.1195, vs next closest C-F 0.1692 and A-E 0.1711; every other pair > 0.22.
- Plain Euclidean distance on the share vectors: also ranks B-D first (0.0424).
- Substantively: both put exactly 0.25 of area in the high tier and differ by only 0.03 in the low/medium split (B 0.31/0.44 vs D 0.28/0.47).
The script asserts the two metrics agree on the closest pair, so the headline claim cannot silently become false if the numbers are edited.

VERIFICATION DONE (not self-reported)
- Ran the script; it reproduces both figures with no arguments, no network, no external data, and writes next to itself regardless of cwd (verified by running it from /tmp).
- Determinism checked at byte level: figure.png md5 identical across runs; figure.pdf was initially differing only via matplotlib's timestamp, so the PDF metadata CreationDate is pinned to a fixed value and the PDF md5 is now identical across runs and across cwds (38c92a1dbf4447fc233995260c53b52c).
- PDF validated: %PDF-1.4, one embedded TrueType subset (/FontFile2) plus /ToUnicode, pdf.fonttype 42, so text stays searchable in the compiled paper.
- Rendered the figure and inspected it twice; the first layout put the evidence box over the data points and the callout text over the right-edge tick labels, so panel (b) was restructured (evidence moved to the free strip above the triangle, point labels fanned out with white halos).
- Caption numbers re-checked against the script's printed output (extremes 0.28-0.55 low, 0.15-0.25 high; distances as above). One rounding claim in the figure was tightened from "d ≥ 0.23" to "d > 0.22" because the true third-smallest distance is 0.2291.

NOTE ON PROCESS
The task said to work only from that brief and to read/write no other file, so I did not invoke the dataviz skill (invoking it reads skill files) - the design decisions above were made from first principles instead. Colour encodes severity as an ordered, CVD-safe sequential ramp (ColorBrewer YlOrRd 3-class) so the tier order survives greyscale printing.
```

==============================================================================
## R2-writer-round-2

- 说明：有效轮 R2 写手（本 RED 基线的来源）
- transcript：`agent-af0c82b7bab6fc094.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**309** 字符（原文；掩码后 247）
- SubagentHandback：**3073** 字符（原文；掩码后 3042）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t2-red/brief-R2.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R2/. Work only from that brief - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
Done. Three artifacts written to `<TMP>/m3-t2-red/out-R2/`: `make_figure.py`, `figure.pdf` + `figure.png`, `caption.txt`. Only the brief was read; nothing else in the repo was touched.

**Answer the figure gives**
- **Strongest correlate: mean slope** — Pearson r = +0.93, Spearman rho = +0.94. Clearing the others by a wide margin.
- Infrastructure index r = −0.78 (rho −0.77), vegetation cover r = −0.74 (rho −0.77), population density r = +0.36 (rho +0.54).
- **Similarity:** average-linkage clustering on the four standardised drivers gives A–C as the closest pair (d = 1.54), then B–E (1.79), then E–F (2.15); D is the outlier (min distance 2.42, vs. 1.54–2.15 for every non-D pair). D is simultaneously steepest (14.8 deg), least vegetated (0.41), lowest infrastructure (55) and highest count (38).

**Figure layout** (2x2, 11.0 x 8.4 in, serif, no title inside axes that duplicates the caption text beyond a suptitle): (a) Pearson + Spearman bars per driver, sorted by |r|; (b) scatter of disaster count vs mean slope with all six districts labelled, least-squares line and R² = 0.87; (c) z-score heatmap of all five columns with rows in dendrogram leaf order; (d) dendrogram.

**Two things worth flagging to the caller**
1. The headline result is robust to the correlation measure (rank and linear agree), but the drivers are heavily collinear: infrastructure index and vegetation cover correlate with **each other at r = 0.98**. With n = 6 their separate contributions cannot be disentangled. The caption states this explicitly and states that no causal direction is implied. A figure that quietly crowns "mean slope" as *the* driver without that caveat would overclaim.
2. The dendrogram's middle group is a near-tie at the resolution of the data — B–E at 1.79 is not far above the A–E (1.87) / A–B (1.95) alternatives. The caption therefore only claims the two robust features: the A–C pair and the isolation of D.

**Verification performed**
- Re-ran the script twice from a clean state (`rm figure.pdf figure.png`); `figure.pdf` and `figure.png` are **byte-identical** across runs (md5 match). The first attempt was *not* deterministic — matplotlib embeds a `CreationDate` in the PDF; fixed via `metadata={"CreationDate": None}`, and confirmed `CreationDate` is absent from the output.
- PDF validates as a single page (`%PDF-1.4`, 1 `/Type /Page`, 37,999 bytes), so it is vector and LaTeX-ready.
- Figure visually inspected; fixed three defects found in the first render (y-tick labels clipped at the left figure edge, district labels B/D colliding with markers in panel (b), and a legend overlapping a data label in panel (a)). Also corrected a misleading panel (d) subtitle that read "left = most similar" — leaf order in a dendrogram does not carry that meaning.
- Dependency note: uses numpy / matplotlib / scipy (`scipy.cluster.hierarchy`, `scipy.stats`); all were present in this environment, but that is an environment assumption, not a stated one in the brief, so it is worth knowing if the grader's environment is bare.
```

==============================================================================
## R3-writer-round-2

- 说明：有效轮 R3 写手（本 RED 基线的来源）
- transcript：`agent-a81b38c13c2459afd.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**309** 字符（原文；掩码后 247）
- SubagentHandback：**3094** 字符（原文；掩码后 3063）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t2-red/brief-R3.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R3/. Work only from that brief - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
Done. Three deliverables written to <TMP>/m3-t2-red/out-R3/ (worked only from brief-R3.md, no other file read or written).

Files
- make_figure.py — self-contained, offline, deterministic; data hard-coded from the brief; run as `python make_figure.py` (output path resolved from __file__, so cwd doesn't matter). Verified byte-identical output across two runs (PDF timestamps suppressed via savefig metadata).
- figure.pdf (1 page, 7.6 x 4.0 in, TrueType fonts embedded, selectable text) and figure.png (300 dpi).
- caption.txt — English caption, plain text, paste-ready.

Figure design
Two-panel, because the brief asks for two distinct things and one chart type serves each legibly:
- (a) 100% stacked horizontal bars, one per district, districts sorted by decreasing low-tier share, every share labelled directly, sequential single-hue ramp (ColorBrewer Blues, ordered tiers) with a 3-entry legend.
- (b) The composition triangle (2-simplex) — the canonical display for three-part compositions. Here structural similarity *is* geometric proximity, so "which two districts are most alike" becomes a visual question. 0.1 gridlines, ticks and titles on all three edges, the closest pair drawn in red with a callout, and every district label tied to its marker by a thin leader line (the six points sit in a tight 0.21-unit-wide cluster, so proximity alone left A/E and C/F ambiguous).

Substantive finding the figure supports
Closest pair is B and D under both metrics I checked: total-variation distance 0.030 (they differ by 0.03 on low, 0.03 on medium, 0.00 on high) and Euclidean distance in the simplex 0.042 — the minimum of all 15 pairs. Next closest are A–E and C–F at 0.05. B, D and E all have high = 0.25 exactly, so they fall on one horizontal line. The high tier spans only 0.15–0.25 across all districts, so essentially all the structural contrast is in the low/medium split: C (0.55/0.30) and F (0.50/0.33) least vulnerable through to B (0.31/0.44) and D (0.28/0.47) most medium-weighted, with A (0.42/0.35) and E (0.37/0.38) in between. Sorting by low-tier share also places B and D adjacently in panel (a), so both panels point at the same answer.

Verification performed
- All six districts' shares sum to 1.000000; the script raises if any row does not.
- Closest pair computed programmatically by the script (not hard-coded), so the annotation, the red highlighting and the caption cannot drift from the data.
- Caption numbers independently recomputed: B–D 0.03; A–E and C–F 0.05; high-tier range 0.15–0.25; sort order C F A E B D. All match the caption text.
- Rendered PNG inspected visually at full size and zoomed into the cluster; no label collisions or overflow after iteration.

One judgement call worth flagging: a single-panel ternary was my first attempt, but with this data the six points bunch into a small blob in the middle of the simplex — exact shares are not readable off it and the labels collide. Splitting into a composition readout (a) plus a similarity space (b) was the fix, not decoration; it is still one figure file.

```

==============================================================================
## judge-round-2

- 说明：独立判者（有效轮）
- transcript：`agent-aac99a6fff8db1fdb.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**1194** 字符（原文；掩码后 1194）
- SubagentHandback：**1353** 字符（原文；掩码后 1343）

### ① 派发提示词（原文）

```text
You are reviewing three figures, each produced by a different author from a separate brief. Read the brief and the artifacts for each:

- tests/skills/figure-choose/red/brief-R1.md  ->  artifacts in tests/skills/figure-choose/red/out-R1/
- tests/skills/figure-choose/red/brief-R2.md  ->  artifacts in tests/skills/figure-choose/red/out-R2/
- tests/skills/figure-choose/red/brief-R3.md  ->  artifacts in tests/skills/figure-choose/red/out-R3/

Each artifact directory contains the generating script (make_figure.py), the exported figure (figure.pdf and figure.png) and the caption text (caption.txt). View the figure images.

For each of the three, in turn, answer these three questions:
1. Is the chart type appropriate for the question asked in the brief? Answer exactly one of: correct / partly correct / wrong.
2. Why? Give your reasoning.
3. Does it violate the rule "composition data must not be drawn as a pie chart"? Answer yes or no.

Read only the three briefs and the three artifact directories. Do not read .claude/, docs/, tests/skills/figure-choose/*.py, or any other repository file.

Write your answers for all three to tests/skills/figure-choose/red/judge.md, in your own words.
```

### ② 自报 / 报告（原文）

```text
写完 `<REPO>\tests\skills\figure-choose\red\judge.md`（中文，只读了三个 brief + 三个产物目录；三张 PNG 都看过，并把 figure.pdf 的文本层抽出来确认 PDF 与脚本/PNG 同源）。

结论：

| 产物 | Q1 图表类型 | Q3 违反饼图规则 |
|---|---|---|
| R1（构成数据 + 相似性判断） | correct | no |
| R2（相关因子 + 相似性） | correct | no |
| R3（同 R1 数据，论文直用） | correct | no |

要点：
- R1：100% 堆叠水平条回答"描述每区构成"，三元单纯形回答"哪两区结构最像"（把相似性变成几何邻近），两者都是构成数据的合规载体。轴向/刻度方向是标准约定（左=low、底=medium、右=high）且与刻度值自洽；圈出的 B–D 在 Aitchison（0.12，次近 C–F/A–E 0.17，其余 >0.22）和欧氏距离下都是最近对，脚本里还有断言把这条钉死；caption 数字逐条复算无误；六个标签按最近点判读无歧义。
- R2：四个面板逐一对应 brief 两问——(a) Pearson/Spearman 相关系数条形图（问"哪个因子相关最强"就是这样答）、(b) 最强因子散点 + 最小二乘、 (c) z 分数热图 + (d) 平均连接树回答"相似性"；(c) 行序与 (d) 叶子序一致。r=+0.93、ρ=+0.94、R²=0.87、y=2.20x+5.37 我独立复算一致；聚类只用四个驱动因子（`Z[:, :-1]`，把响应排除），没把被解释量混进相似性度量。关键：这份数据**不是构成数据**（植被覆盖是一个比例，不是和为 1 的份额），饼图规则本就不适用。
- R3：选型与 R1 同路、同样 correct，caption 数字也对（TV 距离 B–D 0.03 最小，次近 A–E/C–F 各 0.05）。**但发现一处硬伤**：三元图 (b) 的 low / medium 两条轴题被互换——底边刻度画的是 medium 值（第 t 个刻度在 `(t,0)`，t 即 medium）却标 "Low share"；左边缘刻度画的是 low 值（`to_xy(t,0,1-t)`）却标 "Medium share"；只有右边缘 "High share" 正确。脚本两行 `ax.text` 坐标、放大后的 PNG、PDF 文本层三处证据一致。后果是按印刷文字读会把 C 读成 low 0.37/medium 0.55（真值 0.55/0.30），即 brief 第一问在 (b) 面板里会读反。我把它判为**标注错误而非选型错误**，故 Q1 仍记 correct，但在 Q2 里明确点出并建议返修。

另外记录了两处排印级小毛病（不影响判据）：R1 面板 (b) 点位挤在单纯形中央、排名文字漂浮在三角形上方，整图偏宽（9.6×4.5 in）排进单栏字会偏小；R3 用总变差距离而非构成数据标准的 Aitchison 度量（本例两种度量结论相同，但论证强度弱于 R1）。
```
