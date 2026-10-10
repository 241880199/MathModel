# sim/2026 · Problem C — schematic figures (Figure 4, Figure 5)

Judge feedback for this sim: the paper had **no workflow overview and no schematic at all**.
This directory now holds the two TikZ schematics. Everything below is produced by the
`mcm-schematic` skill (category choice → skeleton → edits → compile → render-and-look →
the skill's shipment checker).

## Files

| file | role |
| :--- | :--- |
| `figure-4-workflow.tex` | TikZ **fragment** (a `tikzpicture`; `\input` it in the paper body) |
| `figure-4-workflow.pdf` | compiled one-page PDF (what `\includegraphics` picks up) |
| `figure-5-model-structure.tex` | TikZ fragment |
| `figure-5-model-structure.pdf` | compiled one-page PDF |

The `.tex` files are **fragments, not standalone documents** (deliverable contract). Each one
carries the style-layer line in a header comment. The paper PREAMBLE needs, once:

    \usepackage{tikz}
    \usetikzlibrary{arrows.meta,positioning,calc,fit,backgrounds,shapes.geometric}
    \input{../../../.claude/skills/mcm-schematic/assets/schematic-style.tex}

`../../../.claude/...` resolves from both `sim/2026/tex/` and `sim/2026/fig/` (same depth).
The style layer is the **single source** of colour / line width / rounding / spacing / font —
**no style literal is written into either fragment.**

## Selection echo (contract item ③)

- **Figure 4 — category 1** (technical route: a process with a fan-out and a merge).
  Skeleton **`pipeline-branch`**. Adapted: the fan-out is gated by one hold-out box and then
  re-merges into a single conclusion, so it is drawn as a **bus** (trunk + one horizontal rail
  + three drops) rather than three crossing diagonals. A **third line-semantics** (dashed =
  out of scope) is used, so a **one-line legend** is added (S2 boundary).
- **Figure 5 — category 3** (model structure: stacked composition).
  Skeleton **`model-layered`**. Adapted to three single-box layers with **double-headed**
  relation arrows (`mcmdim`), because the object is one relation chain, not parallel units.

## Compile readings (contract item ④)

Engine: `pdflatex` (TeX Live 2026; `rc=0`, **0 `Overfull \hbox`** on both). One page each.

| figure | page box (in) | page count | top / bottom content margin (pt) |
| :--- | :--- | :--- | :--- |
| Figure 4 | 6.4125 × 3.55 | 1 | 16.6 / 23.2 |
| Figure 5 | 6.4125 × 2.90 | 1 | 20.2 / 7.3 |

The page box width equals the style layer's `\mcmscfigwidth`, so F1 is stable.

## Shipment-checker readings (contract item ④) — with `--schematic`

    python tests/skills/figure-choose/check-figure-style.py \
      --fig sim/2026/fig/figure-4-workflow.pdf \
      --caption "Figure 4: Pipeline from data to conclusions, with the inversion's season scope" \
      --textwidth-in 6.31 --schematic

    python tests/skills/figure-choose/check-figure-style.py \
      --fig sim/2026/fig/figure-5-model-structure.pdf \
      --caption "Figure 5: Structure of the inversion with elimination records" \
      --textwidth-in 6.31 --schematic

★ **订正（2026-10-10）**：上面 figure 5 那条命令**原先没有记录在案**（本节当时只留了 figure 4 的），
而下面 figure 5 的读数来自一条没被记下来的调用 ⇒ **补记在本行**。
同一批：两张图都按**新的样式层**（节点**白底** + 层级靠**边框**，见 `schematic-style.md` 的 `S4.1`）
**重编过** ⇒ `F4` 的"近灰众数"占比随之变了（见下），`A1` 的节点框计数**未变**（9 / 3）。

Figure 4:

    PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 99.68%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 88.95%）；下限 136
    PASS  F1  图宽比 1.016（分母 6.31 in）
    PASS  F2  彩色主色数 0
    PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
    PASS  F3a  图注以 `Figure N:` 起
    PASS  F3b  图注词数 10（上限 12，硬上限 17）
    PASS  F3c  句末不加句号
    PASS  F3d  图注正文非空（正文 10 词）
    PASS  F6  内嵌字体 ['TeXGyreTermesX-Regular']
    PASS  A1  节点框 9 个，重叠 0 对：[]
    PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 93 词
    PASS  A4  越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
    RESULT: PASS

Figure 5:

    PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 79.90%）；下限 136
    PASS  F1  图宽比 1.016（分母 6.31 in）
    PASS  F2  彩色主色数 0
    PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
    PASS  F3a  图注以 `Figure N:` 起
    PASS  F3b  图注词数 7（上限 12，硬上限 17）
    PASS  F3c  句末不加句号
    PASS  F3d  图注正文非空（正文 7 词）
    PASS  F6  内嵌字体 ['TeXGyreTermesX-Bold', 'TeXGyreTermesX-Regular']
    PASS  A1  节点框 3 个，重叠 0 对：[]
    PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 74 词
    PASS  A4  越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
    RESULT: PASS

Note on F2/F5 = 0: the only non-grey colour is the single accent (`#0072B2`, H14 position 5) on
one node border and it rasterises below the 0.5% significance threshold, so it is not counted —
the "at most one accent" rule (S4) holds, it is simply too thin to register.

## What I saw (contract item ④ / step 5 — render and look)

Rendered each page to PNG (`fitz`, 170 dpi) and inspected:

- **Figure 4**: the five pipeline stages read left-to-right; the accent (blue) marks the
  *Inversion* stage and a dashed box sits around it; the scope note "scope: seasons 3-27 only"
  sits below the dashed box with a clear gap and **does not touch the node text**; the bus
  drops cleanly into (b)/(c)/(d); the three streams merge into one conclusion box; the one-line
  legend is legible. **No arrow presses on a glyph, no annotation leaves the frame, no node
  text overflows.** The only cosmetic point left is that the Inversion node is taller than its
  neighbours (content-driven, S3).
- **Figure 5**: three layers, obs on top, constraint in the middle, latent `u` at the bottom
  (accented); a double-headed arrow between each adjacent pair, each with a one-line caption to
  its right; the `u` formulas render as text with `\textsubscript` (no math mode — F6 stays
  green). **No overlap, no clipping.**

## Facts drawn (must not be wrong)

Source: `sim/2026/tex/S5-results.tex`, `S4-model.tex`, `out/table-1..7`.

- Figure 4: `Results.csv` 53 cols × 421 rows → wide-to-long + in-panel test + N/A-vs-0 →
  **inversion** (single-week LP, then season latent LP with cross-week smoothing) → **feasible
  share intervals (deterministic)** → **leave-one-week-out consistency 0.390 / oracle 1.000** →
  **(b)** rank-vs-percent disagreement **0.197**, **(c)** `age` negative for judge and fan shares,
  **(d)** `alpha ≈ 0.25` + bottom-two (flagged **tie-break dependent**) → conclusions.
- **Scope** (drawn, not just stated): the inversion covers **only the percentage-method seasons
  3–27**; the rank-method seasons (1–2 and 28+) give no share LP. This is drawn as a dashed box
  + note + legend, so the named **season 2 is visibly outside the scope**.
- Figure 5: every (season, week) gives **one linear inequality on `u`**; `u` is a within-season
  latent quantity **shared by all weeks of the season**; `share_i = u_i / (sum over the in-panel
  contestants of u)`.

## Rerun

The fragments are not standalone; compile each through a small driver in the gitignored `build/`
(recreate it from the box below; the driver is not kept):

    \documentclass[12pt]{article}
    \input{schematic-style.tex}                       % a copy of the skill's style layer
    \usepackage[paperwidth=\mcmscfigwidth,paperheight=3.55in,margin=0pt]{geometry}   % 2.90in for Figure 5
    \pagestyle{empty}
    \setlength{\parindent}{0pt}
    \begin{document}\input{fragment.tex}\end{document}      % keep this line SINGLE (no trailing newline)

    pdflatex -interaction=nonstopmode -halt-on-error driver.tex

Two gotchas the skill does not document (see feedback 2 below): keep
`\begin{document}\input{...}\end{document}` on one line, and give the fragment a bounding box a
few mm taller than the drawn content — otherwise the exact-height page box clips the top and a
blank second page appears.

## Skill feedback — where I got stuck

1. **"可直接 `\input`" vs "编译出的 `.pdf` 同名" is under-specified.** A true `\input`-able
   fragment cannot compile by itself (no `\documentclass`), and a standalone page needs a driver.
   I resolved it as: fragment in `fig/` (with the preamble `\input` line in a comment) + PDF next
   to it, compiled through a throwaway driver. The skill's §"第四步" says "keep the relative
   position of `schematic-style.tex`" but gives no help for the fragment/driver split, which is
   exactly the shape `mcm-table` already ships (`T1..T6` are `\input` fragments, no driver).
2. **The page box is anchored to the page TOP with a fixed ~5 pt overhang**, so a picture whose
   `\useasboundingbox` height equals `paperheight` overflows the top and clips; and an empty
   trailing paragraph creates a blank page 2. `references/workflow.md` says "页盒靠 geometry 的
   `paperwidth` 钉死" and warns about `F1`, but says nothing about **`paperheight` behaviour** —
   none of the five skeletons hits it because they are short. My fix (bounding box a few mm taller
   than the content + no trailing line) is not documented anywhere in the skill.
3. **No guidance on a "third line-semantics" beyond "add a legend".** The task needed dashed =
   "out of scope" (not loopback/feedback). S2's boundary says a third semantics needs a legend but
   does not say which style to use — I drew the dashed rectangle with `mcmdashplain` (the only
   dashed no-arrow style), and I had to read `assets/schematic-style.tex` to find it.
4. **The narrow-node wrapping trap is only in prose.** S3 ("缩字号或改断行") does not mention that
   hyphenation of a Latin word ("la-tent") creases the box; the mechanical checks (A1/A3/A4) never
   flag it, so only the eye-step catches it. Widening one node fixed it.
