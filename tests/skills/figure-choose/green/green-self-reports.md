# Task 6 GREEN 的派发提示词与写手/判者自报（抢救件）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件逐字收录 **GREEN 写手的自报**与**派发提示词**；自报里可能引用 skill 的规则编号或
> 数值，且**提示词本身就是 Task 6 派发 GREEN 的口径**。任何"写手" agent 读过本文件，
> 产出的就不再是干净的对照件。**与它同案看待的还有** `green-evidence.md` /
> `green/judge-green.md` 与整个 `red/`（点名清单见 `red/README.md` 文首警示头）。

【为什么有这个文件】Task 6 唯一**无法靠单变量复核**的东西是"GREEN 写手到底读到了什么"：
  它只能靠**审计原文**。而这些原文（subagent transcript）在仓外、且 `.superpowers/` 是
  gitignored ⇒ 不搬进受版本控制的目录就随时会丢。本文件由
  `rescue-transcripts.py` 从 transcript 一次性摘录。

【摘录口径】每个 agent 两段，均为原文，**本脚本不加删节**：
  ① 首条 `user` 消息 = 派发的提示词（对本轮，它就是**单独一行**提示词本身 ——
     这一点同时**可复核"未用 fork"**：`fork` 会继承主 agent 上下文，首条消息会是长篇上下文）；
  ② `SubagentHandback` 的 `message` = 它回给调度者的完整报告。
  **不等于"文件里没有省略号"**：文件里出现的省略号（三个句点）**全部**在两段引用
  **内部** —— 是原文作者自己写的简写；**本脚本一处未删**。

【对原文的加工 —— **只有一种**，且逐处计数】写手自己写了**绝对路径**（含 Windows 用户名与
  系统临时目录），本仓规定报告与证据不写绝对路径，故掩码之：仓外临时目录 → `<TMP>/m3-t6-green`，
  仓内根 → `<REPO>`。**本文件共掩码 10 处**，除此之外两段引用**逐字节未改、未软换行**。
  （本文件里**不是原文**的只有脚本写的那几行：文首这几段【】说明与警示块、每个 agent 的
  标题/说明/`transcript`/`字符数` 行。）

【强度声明（不许下游读过头）】①②是**原文**，但"GREEN 写手是否真的**没有**去读 `red/`"
**只有自报、没有沙箱可证**（没有文件系统审计、没有 syscall 记录）。
自报一致 ≠ 已证；本文件能做的是：把自报存下来，让下游能自己判断。

---

==============================================================================
## R1-writer-green

- 说明：GREEN R1 写手（可读 skill；本 GREEN 产物的来源）
- transcript：`agent-adec53c15412da08f.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**361** 字符（原文；掩码后 297）
- SubagentHandback：**3538** 字符（原文；掩码后 3506）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t6-green/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t6-green/out-R1/. Work from that brief and the skill at .claude/skills/mcm-figure-choose/ - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
Done — brief R1 figure, script and caption are written to <TMP>/m3-t6-green/out-R1/ (make_figure.py, figure.png, figure.pdf, caption.txt). No files outside the brief, the skill dir and out-R1 were read or written.

## Chart-type decision (mcm-figure-choose, chart-types.md)

Data relationship = **composition** (each district's land area is one whole split into three parts that sum back to the whole; the question is "how is each whole divided" plus "which two wholes have the same structure"). That is entry 4 of the decision tree, and its **first choice applies here**: `stacked bar chart` (several wholes compared with each other). The first choice is not displaced, so no fallback (`ternary` / `treemap` / `radar`) was used. Drawn as a 100 % stacked bar — bar length = whole, segment length = share, which is exactly what the attribute says to read.

Forbidden options checked and avoided: `pie`/`donut` (H6 — the only rule with a real judgement layer), `stacked area chart` for shares (no common baseline), and the `3-D` family (`3-D pie` included) per H7. Nothing in the figure imitates a pie.

## Design points, by H-ID (measured, not asserted)

- **H1/H2** figure width 6.0 in = **0.95 × 6.31 in** (H2's global-median column-width denominator). PDF MediaBox measured `432 × 187.2 pt` = 6.0 × 2.6 in, **1 page** (one figure = one file = one page).
- **H3** landscape, height 2.6 in, aspect **2.31**.
- **H4** 3 main colours, measured with the shipping binning (320×320 NEAREST, `//16`, near-grey dropped, 0.5 % floor) → **colour_count = 3**, under the ≤4 bar and far from any continuous-ramp gate.
- **H5** no matplotlib default cycle: single-hue ordered Blues ramp `#deebf7 / #9ecae1 / #3182bd`, i.e. shade carries the tier order (low→high), which is ordinal data.
- **H6** no pie (also the one rule the judgement layer actually enforces).
- **H7** no 3-D.
- **H8** single panel — no reason to split.
- **H9** caption = `Figure 1:` + ASCII colon, body **11 words** (cap 12), no trailing period, no non-ASCII characters, self-contained.
- **H10** top/right spines removed, ticks point in, y axis label carries its unit: "Share of land area (fraction)".
- **H11** gridlines/legend/dual-axis are explicitly out of scope for the spec, so no claim is made either way; a frameless one-row legend is used to name the three tiers.
- **H12** 9 pt axes text, 7–8 pt for segment labels and the note (≥ 7 pt floor).

## What the figure does for the second half of the question

1. Districts are ordered by **low-tier share, descending** (C, F, A, E, B, D). The compositions vary mainly along the low↔medium axis, so this ordering makes similar districts adjacent — all three closest pairs end up neighbours.
2. All 18 segment shares are printed on the bars, so the similarity is checkable arithmetically rather than eyeballed.
3. A bracket under the two right-hand bars marks the closest pair: **B and D**, L1 distance over the three shares = **0.06**. (Next closest are A–E and C–F, both 0.10 — B/D wins clearly but not by an order of magnitude.)

Caption text: `Figure 1: Land-area vulnerability shares by district; B and D are most similar`

## Reproducibility

`python make_figure.py` from out-R1 runs offline, hard-codes the six rows, asserts each row sums to 1 before drawing, and needs no manual steps. Two consecutive runs produced byte-identical outputs (md5 `9442d7dc…` for figure.png, `eb0c4520…` for figure.pdf; PDF metadata sets `CreationDate: None` so the timestamp does not break determinism).

```

==============================================================================
## R2-writer-green

- 说明：GREEN R2 写手（可读 skill；本 GREEN 产物的来源）
- transcript：`agent-a47052cc8583ef729.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**361** 字符（原文；掩码后 297）
- SubagentHandback：**3467** 字符（原文；掩码后 3435）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t6-green/brief-R2.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t6-green/out-R2/. Work from that brief and the skill at .claude/skills/mcm-figure-choose/ - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
DONE — Brief R2 figure produced in `<TMP>/m3-t6-green/out-R2/` (4 files, nothing else touched):

- `make_figure.py` (data typed in, no randomness, no network, Agg backend, writes all three artifacts next to itself)
- `figure.png` — 1262×950 px = **6.31 × 4.75 in** @200 dpi (ratio to the 6.31 in text-width denominator in H2 = **1.00**)
- `figure.pdf` — single page, MediaBox 454.32 × 342 pt (same 6.31 × 4.75 in)
- `caption.txt` — `Figure 1: Scatter panels rank slope first; A and C share a profile` (11 words, ASCII colon, no final period — H9)

**Chart-type decision (entry 3 · 相关, per `references/chart-types.md`)**
- Preferred for this entry with 3+ columns is the scatter matrix. The full 5×5 was not used: at 6.31 in text width the cells fall below legibility and the figure would become portrait, against the landscape default (H3). Instead the matrix's **target column** is drawn — 4 scatter panels, one per predictor, on a **shared disaster-count axis**, ordered by |r| so the ranking reads left to right. Panels 2–4 show no y labels (shared scale, not a truncated one).
- Second layer of the brief ("how similar are the districts") is the individual-level structure, which the listed alternative for this entry covers: **parallel coordinates**, the same six districts traced across all five attributes, min–max scaled per axis with each axis's min/max printed underneath.
- Checked against the entry's 禁忌: no line chart joining unordered individuals, no dual-axis chart, no pie, no 3-D; no truncated bar axis.

**Design points → H-IDs**: canvas/orientation H1·H2·H3; colour density H4 (two accent hues #C1440E / #16697A + greys); no matplotlib default colour order H5; no pie H6; no 3-D H7; multi-panel on one page H8; caption template H9; spines removed / ticks inward / units on axis labels H10; one scale per panel, no dual axis H11; in-figure text 8 pt (7.5 pt for the profile axis names and the note) H12; no distribution figure used as a threshold H13.

**Findings the figure carries**
- **Mean slope is the factor most strongly correlated with the historical disaster count, r = +0.93.** Ranking by |r|: slope +0.93, infrastructure index −0.78, vegetation cover −0.74, population density +0.36. The population panel is the left-to-right ranking's straggler, so "population density drives disasters" is not supported.
- Important caveat the figure states in-figure: vegetation cover and infrastructure index co-vary at **r = +0.98**, so they are one effect, not two independent drivers — the rank-2 vs rank-3 gap is not meaningful.
- District similarity: the closest pair in standardised profile space is **A–C**, and **D stands apart** (largest mean distance to the others). Encoded once, consistently, in both panels: A and C share a colour, D has the other accent, B/E/F stay grey; every district is letter-labelled rather than put in a legend. A label de-collision pass runs at the right edge of the profile panel.

**Verification performed**: rendered PNG inspected visually (found and fixed a point occluded by the correlation readout, a label collision, and a wrong coefficient in the collinearity note); regeneration is byte-identical across runs for all three artifacts (PDF wall-clock metadata suppressed); palette measured with the F2 instrument's method (320×320 NEAREST, //16 bins, grey dropped, 0.5% floor) gives 0 bins over the floor, i.e. well under the ≤4 rule, with 2 accent hues visible to the eye.

```

==============================================================================
## R3-writer-green

- 说明：GREEN R3 写手（可读 skill；本 GREEN 产物的来源）
- transcript：`agent-a63638435c0111769.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**361** 字符（原文；掩码后 297）
- SubagentHandback：**3281** 字符（原文；掩码后 3249）

### ① 派发提示词（原文）

```text
Read the brief at <TMP>/m3-t6-green/brief-R3.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t6-green/out-R3/. Work from that brief and the skill at .claude/skills/mcm-figure-choose/ - do not read or write any other file.
```

### ② 自报 / 报告（原文）

```text
Brief R3 done. Deliverables in `<TMP>/m3-t6-green/out-R3/`:
- `make_figure.py` — deterministic regeneration (fixed data, no network, no manual steps; asserts each district's three shares sum to 1.00; re-running yields byte-identical output, verified by hash on two consecutive runs)
- `figure.pdf` (primary, vector) and `figure.png` (200 dpi) — both allowed by the brief
- `caption.txt` — `Figure 1: Land-area vulnerability composition of six districts; B and D most similar`

**Chart type (skill output contract)**
- Recommended: **stacked bar chart** — entry 4 (composition / 构成) of the decision tree, and its first choice holds (6 groups, a single part-of-whole layer), so no fallback was taken.
- Reason: the share is carried by *length along a common 0–100% baseline* — the same channel for every segment of every bar, which is what makes shares comparable across districts. The two other halves of the brief's question are served by design, not by a different plot type.
- Fallback checked and rejected on the data: the entry's `ternary plot` is the obvious candidate for a three-part composition, but the six compositions occupy only a small central patch of the simplex (low 0.28–0.55, high 0.15–0.25), so the three closest pairs would sit within ~0.04 simplex units of each other and their markers would overlap at any readable size — the position channel cannot resolve them at full-simplex scale.
- Taboos read before drawing: no pie/donut (the one judging-layer rule), no stacked-area-for-shares, no 3-D.

**Design points → H-IDs** (house-style.md): canvas width = the 6.31 in text-width default (H1); landscape, aspect 2.18, height 2.90 in (H3); three chromatic colours + a near-grey highlight band, palette is an explicit sequential ramp, not the default colour cycle (H4, H5); composition drawn as stacked bars, not a pie/donut (H6); no 3-D (H7); caption is `Figure N:` + ASCII colon, 11 words (≤12), no closing period (H9); top/right spines removed, inward major ticks only, the y label carries the unit, exact segment values printed inside each segment (H10); in-figure type 7.5–9 pt (H12). H11 is not covered by the style, so no gridlines were drawn; the legend is kept because it is the three-tier key and there is no less ambiguous alternative.

**Substantive finding the figure supports** (also the reason for two design choices — ordering by high-vulnerability share descending, which makes the closest pair adjacent, plus a highlight band and bracket on it): the most similar pair is **B and D** — 31/44/25 vs 28/47/25: identical high share (25% for both) and an identical low+medium total (75% for both), so the upper two segment boundaries line up exactly across the two adjacent bars. Euclidean distance between the share vectors is 0.042 vs 0.062 for the runners-up (A–E and C–F, which tie exactly because C−A and F−E are the same difference vector, +13/−5/−8 pp), and B–D is also the closest pair under Manhattan distance (0.06 vs 0.10), so the judgement does not depend on the metric chosen.

Only the brief and `.claude/skills/mcm-figure-choose/` (SKILL.md + the three files in `references/`) were read; nothing outside `out-R3/` was written. One placeholder to adjust when pasting: the caption label reads `Figure 1:`.
```

==============================================================================
## judge-green

- 说明：独立判者（GREEN 轮；只读产物，未参与写作，未读 skill）
- transcript：`agent-a6333dc6583bdee21.jsonl`（仓外文件，本行只记文件名，不记绝对路径）
- 首条 user 消息：**1474** 字符（原文；掩码后 1474）
- SubagentHandback：**1879** 字符（原文；掩码后 1869）

### ① 派发提示词（原文）

```text
You are reviewing three figures, each produced by a different author from a separate brief. Read the brief and the artifacts for each:

- tests/skills/figure-choose/red/brief-R1.md  ->  artifacts in tests/skills/figure-choose/green/out-G1/
- tests/skills/figure-choose/red/brief-R2.md  ->  artifacts in tests/skills/figure-choose/green/out-G2/
- tests/skills/figure-choose/red/brief-R3.md  ->  artifacts in tests/skills/figure-choose/green/out-G3/

Each artifact directory contains the generating script (make_figure.py), the exported figure (figure.pdf and figure.png) and the caption text (caption.txt). View the figure images.

For each of the three, in turn, answer these four questions:
1. Is the chart type appropriate for the question asked in the brief? Answer exactly one of: correct / partly correct / wrong.
2. Why? Give your reasoning.
3. Does it violate the rule "composition data must not be drawn as a pie chart"? Answer yes or no.
4. Do the artifacts themselves cite any numbered design rules (of the form H1, H2, ...)? Quote any you find, and say which file and line they are in. If you find none, say so. This question is only to establish whether the author worked from a written specification.

Read only the three briefs and the three artifact directories. Do not read .claude/, docs/, tests/skills/figure-choose/*.py, or any other repository file.

Write your answers for all three to tests/skills/figure-choose/green/judge-green.md, in your own words.
```

### ② 自报 / 报告（原文）

```text
判读完成，写入 `<REPO>\tests\skills\figure-choose\green\judge-green.md`（中文正文 + 英文原句引用）。三张 PNG 都实际打开看过，并且我把每个产物自报的数字结论都独立重算了一遍。

**逐份结论**

| | brief | 1. 图型 | 2. 饼图违规 | 4. 引用 H 编号规则 |
|---|---|---|---|---|
| G1 | R1（六区三档构成） | **correct**（堆叠柱） | **no** | **有** |
| G2 | R2（相关 + 相似） | **correct**（4 散点面板按 \|r\| 排序 + 平行坐标） | **no** | **无** |
| G3 | R3（同 R1 数据，论文版） | **correct**（堆叠柱） | **no** | **有** |

**理由要点**

- G1 / G3：构成数据"比较多个组的构成"，堆叠柱是正解——所有段落在同一根 0–1 基线上可直接比长短，且段内直接印了数值。两图都把最像的一对排成相邻并加括号/底纹标注。R1 与 R3 同表同问，两份都选堆叠柱，自洽（"论文版"没有成为换图型的借口）。
- G2：主问题（哪个因子与灾害次数关联最强）由 4 个散点面板直接回答，按 |r| 从大到小排、角上印 r 值；次问题（区与区相似）由平行坐标承载。属互补而非重复；也没用雷达图。保留意见：平行坐标各轴各自 min–max 缩放，只能读相对次序，且 6 线 5 轴偏密——但它只承担辅助的第二问。

**独立复算（全部属实，产物没有编结论）**

- G1/G3 最相似对确为 B–D：L1 = 0.06（次小 A–E = 0.10），欧氏 = 0.0424（次小 A–E = 0.07）；六区三份均和为 1.00。
- G2 四个 Pearson r：slope **+0.934**、infra **−0.777**、veg **−0.744**、pop **+0.360**，与图上 +0.93/−0.78/−0.74/+0.36 及排序一致；veg–infra 共变 r = **+0.980**（图上写 +0.98）；z 标准化后最相似的一对确为 A–C（≈1.45，次小 A–E ≈1.74）。
- 三份 PDF 的 MediaBox 分别 432×187.2 / 454.32×342 / 454.32×208.8 pt，与各自脚本的 figsize 完全对得上，PDF 与 PNG 是同一张图，没有"图换过但没重导"的情况。

**第 4 问的精确出处**

- G1：`out-G1/make_figure.py` 第 11–22 行，第 11 行声明 "cited by H-ID only"，逐条列 H1/H3/H4/H5/H6/H7/H9/H10/H12；内联见第 37/79/100/125/158/174 行。
- G3：`out-G3/make_figure.py` 第 39–51 行，列 H1/H3/H4/H5/H6/H7/H9/H10/H11/H12，第 50 行还主动说明 H11 未被规范覆盖；内联见第 68/94/98/101/159/178 行。
- G2：`out-G2/make_figure.py` **全文无任何 H 编号**。它引的是另一套东西——第 77–78 行散文式 "# House style: <=4 main colours, no matplotlib default colour order, ..." 和第 5 行决策树条目号 `decision tree, entry 3 "correlation"`（第 16 行另有 "the alternative listed for this entry"）。这是三份里唯一没引用编号规则的一份，但图型选得对、无违规，不因此扣分。

**一处值得注意的细节**：G1 与 G3 的 docstring 都把 H6（构成数据不得画成饼图）逐字抄了出来，而两张图也确实没踩——属于"读到并遵守"；G3 还记下了候选图型 ternary plot 被否掉的理由（六点只占单纯形中间一小块，最像的三对会重叠），说明图型是选出来的而非随手抓的。

写入文件：`tests/skills/figure-choose/green/judge-green.md`。
```
