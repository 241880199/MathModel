# Task 5 RED 基线的派发提示词与写手自报

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何"写手" agent 读过本文件，产出的就不再是
> RED 基线。与它同案看待的还有 `red-green-evidence.md`（在上一级）与 `red/README.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是"写手到底读到了什么"：
 它只能靠**审计写手的自报**。

【来源 —— 与先例不同，**照实记**】先例 `figure-choose/red/writer-self-reports.md` 是从仓外
 transcript 文件里**程序化**摘出的。本任务**做不到**：本会话 subagent 的 `.output` 文件实测为
 **0 字节**（命令与输出见文末），transcript 不在可解析的位置。故本文件的提示词与自报是
 **逐字转录自会话内 `SubagentHandback` 投递的文本**（写手自己回给调度者的那段），
 **不是**从 transcript 文件里机器摘的。⇒ 本文件**没有**机器可复核的"逐字节"保证，
 只有**转录音频级**的忠实度声明。

【对原文的唯一加工】写手自报里写了**绝对路径**（含 Windows 用户名），本仓规定证据不写绝对
 路径，故掩码之：本仓根 → `<REPO>`，系统临时目录 → `<TMP>`。除此之外**逐字未改**。

【强度声明】"写手是否真的只读了那一份 brief"**只有自报、没有沙箱可证**（另外：**未用 `fork`**
 —— 三个写手都是新起的干净上下文 agent，首条 user 消息就是下面那一条提示词本身）。
 自报一致 ≠ 已证。

【环境旁路的如实披露（复审 2026-09-29 要求补记，不许删）】"只给两样"说的是**派发那一刻的 user
 消息**；但写手是本机 Claude Code 的 agent，**会话级共享上下文里另有两处本任务删不掉的可见面**：
 ① **可用 skill 列表里 `mcm-plot-python` 的那一行描述**——它恰好点名了三类判据的**类别名**
    （"图宽比不合、彩色主色太多、图注不合规"），并列了 trigger `scienceplots` / `套用期刊样式`；
 ② **项目记忆文件 `MEMORY.md`**——它点名了底座 **SciencePlots（`science+no-latex`）** 与
    **随 skill 入库的字体**。
 这两处**不在**派发消息里（`§0` 那句只给 brief 路径 + 输出目录），但写手**看得到**。
 **写手看得到 / 看不到的边界（关键）**：看得到的是**类别名与工具名**（"有这几类要求"、"用过
   scienceplots 这号东西"）；**看不到**的是**阈值与规范正文** —— F1 的合规带、F2 的主色上限、
   F3b 的词数上限、以及 `house-style.md` 的条文，**一个字都没进写手的可见范围**（派发消息没有、
   skill 描述没有、记忆里也没有）。
 **为什么这**不**推翻 RED**：泄的只是"**有**这几类判据"、不是"判据的**边界**在哪"。证据是：
  三张图**仍全部判红**（R1 红 F1/F3a/F3b/F3c；R2/R3 各红 F1/F2/F3a/F3b/F3c），而 R3 写手在第 3 节
  末尾**明说**它**没有**去查 aspect-ratio / colour-count / caption-format 的任何要求。这反而是
  **更强**的结论：**知道"有这几类判据"也照样全红** —— 合规不是靠"知道有要求"，得靠**读到阈值与
  规范正文**。⇒ 旁路**不**足以让写手"见过规范"，RED 的对照**成立**。

---

## 0. 派发口径（三个写手逐字同一份模板，只换场景号与输出目录）

```text
Read the brief at <TMP>\brief-R{n}.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <REPO>\tests\skills\plot-python\red\out-R{n}\. Work only from that brief - do not read or write any other file.
```

（`<TMP>` = `%TEMP%\m3-t5-red`，其中放着 `brief-R{1,2,3}.md` 的**逐字节副本**——权威副本是
`tests/skills/figure-choose/red/brief-R{1,2,3}.md`。副本与权威副本 `cmp` 相同，见文末。）

**只给了两样**：① 场景 brief 的路径；② 产物输出目录。**未给**：规范
`house-style.md`、模块 `mcm-plot-python/`、判据 `check-figure-style.py`、本任务书、先例 `figure-choose/red/`
的任何证据件。末尾那句是**隔离句**（不给它读仓内别的文件），**不是**规范信息。

---

## 1. R1 写手自报（逐字）

```text
Done. All three deliverables are in `<REPO>\tests\skills\plot-python\red\out-R1\`:

- `<REPO>\tests\skills\plot-python\red\out-R1\make_figure.py`
- `<REPO>\tests\skills\plot-python\red\out-R1\figure.pdf` and `figure.png`
- `<REPO>\tests\skills\plot-python\red\out-R1\caption.txt`

Worked only from the brief (no other files read or written).

**Figure design.** Two panels, one figure.
- Left: horizontal 100% stacked bar, six districts × three vulnerability tiers (green/amber/red for low/medium/high), every segment labelled with its percentage. Districts ordered by decreasing low-tier share (C, F, A, E, B, D) so the most similar pair lands adjacent. An assertion in the script fails loudly if any row does not sum to 1.00, since the stacked-bar encoding is only exact because the data are compositional.
- Right: the 15 pairwise Euclidean distances between composition vectors, sorted, with the minimum highlighted — i.e. the figure carries the evidence for the "most similar" judgement rather than only asserting it.

**Answer to the brief's question (computed, not eyeballed).** B and D have the most similar structure: distance 0.042, differing by at most 0.03 in any tier and sharing an identical 0.25 high-tier share. Runner-up pairs A–E and C–F are at 0.062; the most dissimilar pair is C–D at 0.334. The rank-1 conclusion is metric-robust — B–D is also the minimum under L1/Manhattan (0.06 vs 0.10 for both runner-ups), so it does not depend on the Euclidean choice. Substantively: the high tier is nearly constant across districts (0.15–0.25) while the low tier ranges 0.28–0.55, so districts differ mainly in how their non-high area splits between low and medium.

**Reproducibility.** Agg backend, no randomness, no network, no manual steps. Verified by running the script twice and hashing: both `figure.png` and `figure.pdf` are byte-identical across runs (fixed PDF metadata strips the embedded date; without that the PDF hash changed per run). Also switched `pdf.fonttype` to 42 — matplotlib's default writes Type 3 fonts, which render but carry no real embedded font and extract poorly; the PDF now embeds TrueType (2 `FontFile2` objects, 0 Type3), which matters since the deliverable is headed for LaTeX.

Caveats worth noting: the similarity metric (Euclidean on raw share vectors) is a choice, not something the brief fixed — I report the L1 cross-check above for that reason. The district display order is likewise a deliberate choice made to serve the comparison, and the caption states it so the ordering is not read as data.
```

## 2. R2 写手自报（逐字）

```text
Produced the Brief R2 deliverables in <REPO>\tests\skills\plot-python\red\out-R2\ — worked only from the brief, no other file read or written.

Files written (all absolute paths):
- <REPO>\tests\skills\plot-python\red\out-R2\make_figure.py
- <REPO>\tests\skills\plot-python\red\out-R2\figure.pdf
- <REPO>\tests\skills\plot-python\red\out-R2\figure.png
- <REPO>\tests\skills\plot-python\red\out-R2\caption.txt

Figure design (2 panels, 9.0 x 3.9 in, data hard-coded from the brief's table, districts A–F):
- Panel (a) "Which factor tracks the disaster count?" — horizontal bars of Pearson r between each of the four predictors and the historical disaster count, sorted by |r|, with the strongest bar in red; hollow circles overlay the Spearman rho on the same scale; value labels carry an asterisk for p < 0.05; footnote "* Pearson p < 0.05".
- Panel (b) "Districts that behave alike" — 6x6 heatmap of pairwise Euclidean distance in the space of all five attributes standardised (ddof=1), sequential blue colormap, annotated cells, red outlines on the closest pair (both symmetric cells), colourbar labelled "Euclidean distance (standardised)", plus a line under the panel giving the most similar and most distinct districts.

Answer the figure gives (verified numerically by the script's own output):
- Most strongly correlated factor: mean slope, r = +0.930, p = 0.007 (Spearman rho = +0.943) — the only statistically significant relationship. Then infrastructure index r = -0.777 (p = 0.069), vegetation cover r = -0.744 (p = 0.090) as weaker negative/protective factors, population density r = +0.360 (p = 0.483), essentially unrelated.
- District similarity: A–C are the closest pair (d = 1.45); D is the most distinct district (nearest-neighbour d = 2.91, and its largest gap is D–C at 5.7). A/C combine gentle slopes, highest cover, strongest infrastructure; D pairs the steepest slopes and lowest cover with the weakest infrastructure and the largest disaster count (38).
- caption.txt flags explicitly that with n = 6 these correlations are indicative rather than conclusive.

Verification performed: script runs with no network/manual steps (matplotlib Agg, numpy, scipy.stats); ran it twice and confirmed figure.png, figure.pdf and caption.txt are byte-identical across runs (PDF made stable by passing metadata={"CreationDate": None} — without it the PDF hash changed every run). Rendered PNG was inspected visually three times and two layout defects were fixed: the legend previously collided with the "+0.36" value label, and the "* p < 0.05" note floated detached below the figure; value labels are now positioned beyond max(|r|, |rho|) so they never sit on the Spearman marker.

Dependency note for the harness: the script imports scipy.stats (only for Pearson/Spearman p-values); scipy is present in this environment. No styling package (e.g. scienceplots) or bundled font is required — the figure uses only DejaVu Serif, matplotlib's default.
```

## 3. R3 写手自报（逐字）

```text
Brief R3 complete. All three deliverables are in <REPO>\tests\skills\plot-python\red\out-R3\: make_figure.py, figure.pdf + figure.png, caption.txt. Nothing outside the brief and that directory was read or written.

What the figure is (two panels, one figure):
- (a) 100% stacked composition bars, one per district A–F, three ordinal tiers bottom-to-top (low → high) in a single-hue sequential ramp (`#c6dbef / #4292c6 / #08306b`), each segment value printed inside it, y-axis in percent 0–100%.
- (b) 6x6 pairwise total-variation-distance matrix, TV(i,j) = 0.5·Σ|p_it − p_jt|, every off-diagonal cell annotated to 2 dp, diagonal masked, same Blues ramp for the heatmap, slim colorbar.

Answer the figure supports: B and D are the most similar pair. TV(B,D) = 0.03 — their high-tier shares are identical (0.25) and low/medium differ by 0.03 each. This is the minimum of all 15 pairs under total variation *and* under Euclidean distance (checked both; ranking is identical), less than half the next smallest values (0.05 for A–E and C–F); least similar is C–D (0.27). The pair is marked by an orange outline on both bars in (a) and both mirror cells in (b), plus orange bold tick labels, and spelled out in the shared figure legend. Composition summary carried in the caption: low tier dominant in A/C/F, medium dominant in B/D/E, high tier never dominant and confined to 0.15–0.25.

Verification actually run (not just asserted):
1. Reproducibility — ran the script twice and hashed both outputs; both `figure.pdf` and `figure.png` are byte-identical across runs, and identical again when invoked from a different cwd. This required pinning PDF `CreationDate`/`ModDate`, since matplotlib otherwise stamps wall-clock time into the PDF and the first two runs differed (PNG was already stable).
2. Fonts — PDF embeds TrueType subsets (DejaVu Sans, DejaVu Sans Bold), zero Type3, `pdf.fonttype=42`, so it is safe for pdflatex.
3. Script has no network access, no randomness, no manual steps, and asserts the input table is a valid composition (rows sum to 1.00) before drawing.

One real defect found and fixed by rendering and pixel-checking rather than by reading the code: a `HIGHLIGHT` set of integer indices was being tested against district letters, so the accent-coloured tick labels silently never applied (the declared highlight was not in the fact). I caught it by sampling the exported PNG for the accent colour and finding zero accent pixels in the tick band; split into `PAIR_INDEX` (bar rectangles) vs `PAIR_LETTER` (tick labels), re-rendered, and confirmed 33k accent pixels now span the tick-label band. An earlier layout defect (tier legend colliding with the panel-(a) title, and an inline note sitting on top of the dark bars) was also fixed by moving both into a shared figure-level legend with a fourth proxy entry for the highlighted pair.

I did not invoke the `mcm-plot-python` skill or any other skill, per the brief's constraint to work only from it — so this output is an unguided baseline, not one that followed the skill's own rules (e.g. any aspect-ratio, colour-count or caption-format requirements the skill imposes were not consulted).
```

---

## 附：可复核的两条命令（当场跑过）

```text
$ for n in 1 2 3; do cmp tests/skills/figure-choose/red/brief-R$n.md <TMP>/brief-R$n.md && echo "R$n identical"; done
R1 identical
R2 identical
R3 identical

$ ls -l <TMP>/claude/D--Projects-----/<session>/tasks/a03f2dc625cab58d9.output \
        <TMP>/claude/D--Projects-----/<session>/tasks/a02304a1f56e83a96.output \
        <TMP>/claude/D--Projects-----/<session>/tasks/a07b6eeee2235d8a1.output
-rw-r--r-- 1 Shameless 197121 0 Sep 29 22:19 …/a02304a1f56e83a96.output
-rw-r--r-- 1 Shameless 197121 0 Sep 29 22:19 …/a03f2dc625cab58d9.output
-rw-r--r-- 1 Shameless 197121 0 Sep 29 22:19 …/a07b6eeee2235d8a1.output
（三个写手的 .output 文件均为 0 字节 ⇒ transcript 不可程序化摘录，故本文件用转录）
```
