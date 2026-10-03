# Task 3 RED 基线的派发口径与写手自述（`mcm-schematic`）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何「写手」agent 读过本文件，产出的就不再是 RED 基线。
> 与它同案看待的还有上一级的 `red-green-evidence.md` 与 `README.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是「写手到底读到了什么」：它只能靠**审计写手的自报**。

【来源 —— 照实记】本会话 subagent 的 `.output` 不可靠（先例：`plot-python` 那支实测 0 字节）⇒ 本文件的
 提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**（写手回给调度者那段），
 **不是**从 transcript 文件里机器摘的 ⇒ **没有**机器可复核的「逐字节」保证，只有**转录级**的忠实度声明。

【对原文的唯一加工】写手自述里写了**绝对路径**（含盘符与用户名）⇒ 掩码之：系统临时工作区
 `D:\m3-t3-schematic` → `<TMP>/m3-t3-schematic`。除此之外**逐字未改**。

【强度声明】「写手是否真的只读了那两个文件」**只有自报、没有沙箱可证**（另外：**未用 `fork`** —— 三个写手都是
 新起的干净上下文 `general-purpose` agent，首条 user 消息就是下面那条提示词本身）。**自报一致 ≠ 已证**。

【环境旁路的如实披露（照先例的强度写，不许省）】「只给三样」说的是**派发那一刻的 user 消息**；
 但写手是本机 Claude Code 的 agent，**会话级共享上下文里另有两处本任务删不掉的可见面**：
 ① **可用 skill 列表里 `mcm-schematic` 的那一行描述** —— 它点名了**类别名**（"图宽不合、底色不是白、
 显著色不在允许色序、图注不合规、字体族不对"）；
 ② **项目记忆文件 `MEMORY.md`** —— 它点名了本套件的模块名与工具面信息（含本机已装 TeX）。
 这两处**不在**派发消息里，但写手**看得到**。
 **写手看得到 / 看不到的边界（关键）**：看得到的是**类别名与工具名**（"有这几类要求"、"用的是 TikZ/pdflatex"）；
 **看不到**的是**阈值与规范正文** —— 图宽怎么由 `\mcmscfigwidth` 算出来、`A4` 的**允许线宽集合**、
 图注的形态契约（`Figure N:` 前缀 / 不押句号 / 词数上限）、字体族要与论文同源（`newtxtext`）、
 判据的 ID 与口径。派发消息没有、skill 描述没有、记忆里也没有。

---

## 0. 派发口径（三个写手逐字同一份提示词，只换输出目录）

```text
Read the brief at <TMP>/m3-t3-schematic/brief.md and the minimal TikZ skeleton at <TMP>/m3-t3-schematic/neutral-skeleton.tex, and produce the figure and caption the brief asks for. Write all deliverables into <TMP>/m3-t3-schematic/out-R{n}/. Work only from those two files - do not read or write any other file.

Environment fact (not part of the brief): `pdflatex` is on PATH if you want to check that your document compiles.

When you are done, reply with a short self-report: which files you read, what you produced (file names and sizes), why you drew the figure the way you did, and any issues you hit.
```

（实际派发时是**绝对 Windows 路径** `D:\m3-t3-schematic\...`；上面是掩码后的等价写法。三个写手之间
**只有 `out-R{n}` 这一个 token 不同**。）

**给写手的 two files 是**仓内权威件的**仓外副本**，派发前**逐字节比对**过（当场跑过）：

```text
$ python -c "import pathlib; a=pathlib.Path('tests/skills/schematic/red/brief.md').read_bytes(); b=pathlib.Path('D:/m3-t3-schematic/brief.md').read_bytes(); c=pathlib.Path('tests/skills/schematic/neutral-skeleton.tex').read_bytes(); d=pathlib.Path('D:/m3-t3-schematic/neutral-skeleton.tex').read_bytes(); print('brief identical:', a==b, '| skel identical:', c==d)"
brief identical: True | skel identical: True
```

⇒ 写手拿到的 brief 与骨架**就是我们入库的那两份**（`read_bytes()` 直接比，不经 blob）。

---

## 1. R1 写手自述（原文，掩码后）

```text
Done. All three deliverables are in `<TMP>/m3-t3-schematic/out-R1/` and the document compiles cleanly with `pdflatex` (1 page, no warnings — no Overfull/Underfull/Missing in the log).

Files read (only these two, per the instruction):
- `<TMP>/m3-t3-schematic/brief.md`
- `<TMP>/m3-t3-schematic/neutral-skeleton.tex`

Files produced:
- `<TMP>/m3-t3-schematic/out-R1/figure.tex` — 3005 bytes. Self-contained article document with `tikz`, `positioning`, `arrows.meta`, `shapes.geometric`; body is one `tikzpicture` inside a `figure`, with the caption in `\caption{}`.
- `<TMP>/m3-t3-schematic/out-R1/figure.pdf` — 49529 bytes (1 page, 1241x1754 px at 150 dpi).
- `<TMP>/m3-t3-schematic/out-R1/caption.txt` — 698 bytes, plain text.

Why the figure looks this way:
- Single vertical main spine in workflow order: Data collection -> Preprocessing -> Calibration -> Fit check -> Scenario projections -> Comparison -> Recommendation. Top-to-bottom matches the brief's own ordering and is the easiest direction to read.
- Fit check is drawn as a decision diamond because it is the one genuine branch; its "No" edge is a distinct loop that exits left, rises, and re-enters Calibration.west, labelled "No: revise model or priors (repeat)" so the repetition the brief mentions is explicit. The "Yes" edge carries the main flow downward and is labelled "Yes".
- Scenario projections fan out to three parallel policy boxes (No intervention / Vaccination campaign / School closure) and those three converge into Comparison, which mirrors "run forward under three alternative policies" then "compare the three projections and rank them". Comparison -> Recommendation closes the flow.
- Kept the skeleton's plain `article` + `tikz` primitives and added only rounded rectangles, a diamond, LaTeX arrowheads and a small caption font. No palette, no width/colour/font pinning beyond a 1.6 cm page margin, since the brief gives none and I worked only from the two provided files.
- Node text is a bold step name plus a small parenthetical sub-line (e.g. "clean and align to a weekly grid") so a reader can follow each step without the prose.

Verification:
- `pdflatex -interaction=nonstopmode -halt-on-error` exited 0; output "Output written on figure.pdf (1 page, 49529 bytes)".
- Rasterised the PDF with PyMuPDF and inspected it visually: boxes, arrow directions, the feedback loop, the three-policy fan-out/fan-in, and the caption all render as intended.
- Deleted build artifacts (aux/log/png); only the three deliverables remain in out-R1.

Issues hit: none blocking. `pdftoppm`/Ghostscript are not installed, so I used Python (PyMuPDF) to rasterise for visual verification. The figure occupies the upper portion of an A4 page with white space below (normal for a `figure` in an `article`); the TikZ picture itself fits within the text width.
```

## 2. R2 写手自述（原文，掩码后）

```text
Done. Produced the schematic and caption into `<TMP>/m3-t3-schematic/out-R2/`.

Files read (only these two, as instructed):
- `<TMP>/m3-t3-schematic/brief.md`
- `<TMP>/m3-t3-schematic/neutral-skeleton.tex`

Deliverables written (all in `<TMP>/m3-t3-schematic/out-R2/`):
- figure.tex — 3520 bytes. Self-contained `\documentclass{article}` + tikz document following the provided skeleton's shape (article, `\usepackage{tikz}`, `\usetikzlibrary{positioning}`, `\begin{document}...\end{document}`); the body is a single tikzpicture inside a figure float with the caption.
- figure.pdf — 49237 bytes, 1 page. Compiled with `pdflatex -halt-on-error` (exit 0), then recompiled after a label tweak; last compile exit 0.
- caption.txt — 717 bytes, English plain-text caption.

How the figure is drawn and why:
- Vertical main flow, one rounded box per workflow step, matching the brief's sequence: Data collection -> Preprocessing -> Calibration -> Fit check -> Scenario projections -> Comparison -> Recommendation. Each box carries a one-line sub-label paraphrasing the step's job (e.g. "clean and align to a weekly grid") so a reader can follow it without the prose.
- Fit check is drawn as a diamond (the only genuine decision in the workflow). Its "Yes" edge goes straight down to Scenario projections; its "No" edge exits right and loops back up into Calibration, labelled "No: revise model structure or priors". This encodes the brief's "this loop can repeat" as an explicit cycle rather than a note.
- The three policies are drawn as three parallel boxes (No intervention / Vaccination campaign / School closure) fanned out of "Scenario projections" and converging into "Comparison", so the branching structure of the projections is visible rather than hidden inside one box.
- Only the skeleton's primitives are used (nodes, directed arrows) plus shapes/positioning/arrows.meta/calc for the diamond and arrowheads; no colours, no external assets, deterministic, no network.

Issues hit and fixed:
- First compile failed: `! Package pgfkeys Error: The key '/tikz/step' requires a value.` My style was named `step`, which collides with TikZ's built-in `step` key (grid step). Renamed the style to `proc`; compiles clean.
- Visual check (rendered via PyMuPDF) showed the "No: revise..." label initially sat on top of the feedback line; moved it to `below right` so it is clear of the line. Verified the re-rendered PDF.
- Minor: I temporarily created build.log/figure.aux/figure.log/_preview.png for compilation and visual checking; these were deleted, so out-R2 contains only the three deliverables.

Note: I did not touch out-R1 or out-R3 (they exist side by side but are outside my scope).
```

## 3. R3 写手自述（原文，掩码后）

```text
Done. All three deliverables are in `<TMP>/m3-t3-schematic/out-R3/`.

FILES READ (only these two, as instructed)
- `<TMP>/m3-t3-schematic/brief.md`
- `<TMP>/m3-t3-schematic/neutral-skeleton.tex`
I did not read or write anything else — in particular I did not open the `mcm-schematic` skill, the `red/` folder, or any other output round. So every style choice below is my own judgment from general practice, NOT taken from the skill's rule set.

PRODUCED
- `<TMP>/m3-t3-schematic/out-R3/figure.tex` — 3,881 bytes. Self-contained article document built on the skeleton's preamble (extended with geometry + shapes.geometric + arrows.meta; the skeleton's two primitives are still visible in spirit but the figure is fully rebuilt).
- `<TMP>/m3-t3-schematic/out-R3/figure.pdf` — 46,843 bytes, 1 page. Compiled with the system pdflatex (TeX Live 2026), exit 0, no errors and no overfull/underfull box warnings.
- `<TMP>/m3-t3-schematic/out-R3/caption.txt` — 613 bytes, plain text, identical wording to the `\caption{}` inside figure.tex.

HOW THE FIGURE IS DRAWN, AND WHY
- Vertical spine for the linear stages (Data collection -> Preprocessing -> Calibration -> Fit check -> Scenario projections -> Comparison and ranking -> Recommendation), which matches how a reader scans a method section.
- Fit check is a diamond (the conventional decision symbol) carrying "Fit residual acceptable?" with two labelled out-edges: "acceptable" continuing down, "not acceptable" going right into "Revise model structure or priors", from which a dashed arrow returns into Calibration's east side and is labelled "revise & refit". The dashed edge is the visual signal for the repeatable loop, and the loop is drawn off to the right so it never crosses the forward path.
- Scenario projections fans out to three equal sibling boxes ("No intervention", "Vaccination campaign", "School closure" — each force-broken onto two lines so the three boxes are the same height), which re-converge through short bus segments into Comparison, then Recommendation. The three branches are the brief's three policies; the converge-then-rank step is what makes "Comparison" readable as a synthesis rather than a fourth parallel branch.
- Greyscale only (black/white with black!4 fills, black!75 strokes): white page background, no chromatic colours at all, so it cannot violate a palette rule and it prints/scans safely.
- Arrowheads via arrows.meta Latex, uniform 0.7pt strokes, rounded-corner nodes, `\small` body / `\scriptsize` edge labels; figure centred with the caption directly beneath it.

ISSUES / CAVEATS
- Cannot consult the mcm-schematic skill under the "those two files only" constraint, so the competition-specific choices it likely pins (figure width exactly `\linewidth`, a named font package, a specific palette order, an exact caption convention such as never ending in a period or a required leading phrase) are unverified. If a shipment checker runs against this, those are the rules most likely to be tripped; the geometry is the first thing I would pin to `\linewidth`.
- The figure's natural width (~13.7 cm) is narrower than the 16.5 cm text block of the 1 in-margin demo page, so it sits centred rather than edge-to-edge. I chose not to `\resizebox` it up, which would have scaled the fonts ~1.2x and made the schematic oversized — but a width check would flag this.
- caption.txt carries the caption body only, with no "Figure 1:" prefix, because LaTeX adds the number; it matches the `\caption{}` string exactly.
- No network access used; output is deterministic (same source -> same PDF modulo the usual PDF /ID and timestamp).
- Verification: I rendered the compiled PDF to a PNG with PyMuPDF and inspected it visually — all seven stages, both decision labels, the dashed loop and the three-way fan/converge are legible and nothing overlaps or is clipped. The temporary preview PNG was deleted, so out-R3 contains exactly the three deliverables and nothing else.
```

---

## 4. 三个写手在「运气」上的分歧（照实记，供读 RED 时参考）

三个写手都**没看过规范**，但在**同一份提示词、同一个场景**下做出了不同的偶然选择，
足以说明 RED 侧**存在写手间的离散度**（这正是「同一场景 × 3 位写手」想量到的东西）：

| | 页盒（决定 `F1`） | 线宽（决定 `A4`） | 回环线型（判据不判） | 图注形态（决定 `F3a/b/c`） |
| :-- | :-- | :-- | :-- | :-- |
| **R1** | A4 默认 | TikZ 默认 ⇒ `A4` 红 | **实线**（与主流程同款） | 无前缀 · 103 词 · 句号结尾 ⇒ 三条红 |
| **R2** | letter 默认 | TikZ 默认 ⇒ `A4` 红 | **实线**（与主流程同款） | 无前缀 · 108 词 · 句号结尾 ⇒ 三条红 |
| **R3** | letter 默认 | 自选 0.7pt ⇒ **`A4` 绿** | **虚线**（与主流程可分） | 无前缀 · 90 词 · 句号结尾 ⇒ 三条红 |

★ 这张表**不声称穷尽**差异；它只记本支四份产物上**实际被触发/未触发**的那几项。
它的用处是**防止把 RED 的红读成"写手无能"**：**R3 的 `A4` 本来就没红** —— 同一条判据，
**依写手的偶然选择而红或不红**。
