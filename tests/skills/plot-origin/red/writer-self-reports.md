# Task 3 RED 基线的派发提示词与写手自报（`mcm-plot-origin`）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何"写手" agent 读过本文件，产出的就不再是
> RED 基线。与它同案看待的还有上一级的 `red-green-evidence.md` 与 `README.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是"写手到底读到了什么"：
 它只能靠**审计写手的自报**。

【来源 —— 照实记】先例 `mcm-plot-python/red/writer-self-reports.md` 是从仓外 transcript 文件里
 **程序化**摘出的；`mcm-plot-matlab/red/` 那份做不到（`.output` 实测 0 字节）。本支**与 matlab 同型**：
 三个写手的提示词与自报是**逐字转录自会话内 `SubagentHandback` 投递的文本**（写手回给调度者那段），
 **不是**从 transcript 文件里机器摘的。⇒ 本文件**没有**机器可复核的"逐字节"保证，
 只有**转录级**的忠实度声明。

【对原文的唯一加工】写手自报里写了**绝对路径**（含 Windows 用户名），本仓规定证据不写绝对路径，
 故掩码之：本仓根 → `<REPO>`，系统临时目录 → `<TMP>`。除此之外**逐字未改**。

【强度声明】"写手是否真的只读了那一份 brief"**只有自报、没有沙箱可证**（另外：**未用 `fork`**
 —— 三个写手都是新起的干净上下文 agent，首条 user 消息就是下面那一条提示词本身）。
 自报一致 ≠ 已证。

【环境旁路的如实披露（照先例的强度写，不许省）】"只给两样"说的是**派发那一刻的 user 消息**；
 但写手是本机 Claude Code 的 agent，**会话级共享上下文里另有两处本任务删不掉的可见面**：
 ① **可用 skill 列表里 `mcm-plot-origin` 的那一行描述**——它点名了**类别名**
    （"图宽比不合、底色不是白、显式色序不对"），并列了 trigger `Origin 画图` / `print 导出` 等；
 ② **项目记忆文件 `MEMORY.md`**——它点名了本机已装 TeX、以及本套件的模块名与工具面信息。
 这两处**不在**派发消息里（§0 那条只给 brief 路径 + 输出目录 + 三件环境事实），但写手**看得到**。
 **写手看得到 / 看不到的边界（关键）**：看得到的是**类别名与工具名**（"有这几类要求"、"用的是 Origin"）；
 **看不到**的是**阈值与规范正文** —— `F1` 的合规带、`F2` 的主色上限、`F3b` 的词数上限、
 `F4` 的亮度下限、要落 `H14` 色序、字体族的可接受表，以及 `house-style.md` 的条文。
 派发消息没有、skill 描述没有、记忆里也没有。
 **为什么这**不**推翻 RED**：泄的只是"**有**这几类判据"，不是"判据的**边界**在哪"。
 三条产物各自**≥3 条红**即是证据（判词见 `red-green-evidence.md`）。

【★ 本支特有的一条额外披露 —— **写手读了"工具链"**】R1 与 R3 在自报里**主动**说明：为写 Origin 代码，
 它们读了 **`originpro` 包的源码**（`<REPO>/build/m3-origin-probe/site/originpro/`，**gitignored**）
 与 **Origin 自带的资源**（`Plot.ogs` / `LAYER.OGS` / `X-Functions/Plotting/*.OXF` /
 `OriginC/System/graph.h` 等，在本机安装目录下）。**理由**：brief 禁止读仓内别的件、而 API 否则无从得知。
 **三个写手均声明未碰任何仓内 skill / 规范 / 判据 / 证据件。**
 ⇒ 这与计划 §质检 **T7** 的预判一致（写手**必须**能驱动 Origin），**是环境信息、不是规范信息**；
 但**必须写全**，否则本文件就成了"只给两样"的假声明。

---

## 0. 派发口径（三个写手逐字同一份模板，只换场景号与输出目录）

```text
Read the brief at <TMP>\m3-origin-t3-red\brief-R{n}.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <REPO>\tests\skills\plot-origin\red\out-R{n}\. Work only from that brief - do not read or write any other file.

Environment facts you will need (these are environment facts, not part of the brief):
- The `originpro` python package is installed at `<REPO>\build\m3-origin-probe\site` - put that directory on `sys.path` before importing it.
- OriginPro 2026 (Education) is installed and licensed on this machine; it starts hidden.
- Your script must end by calling `op.exit()` (wrap the work in `try/finally`) - otherwise a stray `Origin64.exe` process is left behind.

When you are done, reply with a short self-report: what you read, what you produced (with file names and sizes), the chart choice and why, and any environment issues you hit and fixed.
```

（`<TMP>` = `%TEMP%\m3-origin-t3-red`，其中放着 `brief-R{1,2,3}.md` 的**逐字节副本**——
 权威副本是 `tests/skills/figure-choose/red/brief-R{1,2,3}.md`，本支**未做任何改写**（它本来就是
 Python 场景，不涉及换语言）。副本与权威副本 `cmp` 相同，见文末。）

**只给了三样**：① 场景 brief 的路径；② 产物输出目录；③ **三件环境事实**（`originpro` 装在哪 ·
 Origin 已授权 · 收尾必须 `op.exit()`；后者是 T7 点名的"环境三件"）。**未给**：规范
 `house-style.md`、本模块 `mcm-plot-origin/`（含 helper）、判据 `check-figure-style.py`、本任务书、
 任何先例证据件。

---

## 1. R1 写手自报（逐字）

```text
Done. All three deliverables are in <REPO>\tests\skills\plot-origin\red\out-R1\.

**What I read**
Only `brief-R1.md` (the task file). To write the Origin code I additionally had to consult the *tooling* — the bundled `originpro` package source under `<REPO>\build\m3-origin-probe\site\originpro\` and Origin's own installed resources (`Plot.ogs`, `LAYER.OGS`, `X-Functions/Plotting/*.OXF`, `OriginC/System/graph.h`, `PlotPopup/ResourceCustomize.xml`) — because the brief forbade reading any other project file and the API was otherwise unknowable. No repo/skill files were touched.

**What I produced**
- `make_figure.py` — 3,147 B; deterministic, offline, no manual steps; wraps all Origin work in `try/finally` with `op.exit()`.
- `figure.png` — 17,110 B, 1200x850 px.
- `figure.pdf` — 3,386 B (vector), byte-identical across repeated runs.
- `caption.txt` — 1,336 B, English plain text.
(Re-ran 3x: PDF byte-identical; PNG differs only in embedded metadata — decoded pixels are bit-identical, verified with PIL.)

**Chart choice and why**
100% stacked column, one column per district, three ordinal tiers stacked; y axis "Share of district area (%)" fixed 0–100; x axis `District`. The data are parts of a whole where every district sums to 1.00, so a stacked bar is the direct encoding; the 100% height makes the six columns segment-by-segment comparable, which is exactly what the question ("which two districts have the most similar structure") needs. Tier colours are a single-hue sequential ramp (light→dark) because the tiers are ordinal, not nominal. Districts are sorted by low-tier share descending (C, F, A, E, B, D) as a single stated rule — this makes B and D adjacent so their near-identical profiles read off the figure; the caption states the rule. Caption content: high tier is near-constant (15–25%) everywhere; the region splits into three low-dominated districts (C/F/A, largest tier = low) and three medium-dominated ones (E/B/D, largest tier = medium); B (31/44/25) and D (28/47/25) differ by ≤3 points per tier / 6 points total, the smallest gap of any pair — asserted as the "most similar" judgement.

**Environment issues hit and fixed**
1. `originpro` needs `sys.path.insert(0, ...\build\m3-origin-probe\site)` before import — done.
2. **Stacking is the hard part.** `gl.add_plot(..., type='c')` creates *side-by-side* columns; `gl.group(True)` groups but does not stack; `layer.stack=1`, `gl.set_int('stack'/'stack.offset'/'plot1.line.color', …)` are all silently accepted no-ops (Origin accepts any property name and returns 0). What works: build the plot with LabTalk `plotxy iy:=((1,2),(1,3),(1,4)) plot:=213 legend:=1;` — plot id 213 = stacked column, and `plotxy` internally calls `AddPlot(range, id, GAP_GROUP_PLOTS|GAP_USE_TEMPLATE)`. `worksheet -P 213 StackColP;` also stacks but **hangs Origin** (a hidden dialog) — do not use it, and avoid `op.wait()`.
3. LabTalk column indices are **1-based** — my first attempt used 0-based indices and Origin silently fell back to row numbers on the X axis.
4. A timed-out probe run left `Origin64.exe` behind; I killed it. The delivered script leaves **0** stray processes (verified with `tasklist`).
5. I created scratch PNGs in Origin's user folder while probing the API and deleted them all afterwards.

**Known unfixed limitation (flagging honestly)**
Origin draws a thin (≈1 px) border on **stacked** segments — blue at the high/medium boundary, red at the medium/low boundary in the shipped figure. I could not find any scriptable way to remove or recolour it: `Plot.set_int('Line.Width', 0)`, `gl.set_int('plot{n}.line.color'|'border.color'|'Line.Color', …)` and `Plot.set_cmd('-c/-e/-b/-l/-w/-f/-k/-z …')` all left it unchanged (only the ineffective `plot.set_int("line.width", 0)` line was removed from the script so it doesn't claim otherwise); `set_cmd('-e 0')` removes the *whole fill*, not the border. Note also a call-order trap: after `Plot.color = …` is assigned, subsequent `Plot.set_cmd(...)` calls on that plot stop taking effect. The chart is otherwise correct and readable, but a reviewer who looks closely will see those hairline outlines.
```

## 2. R2 写手自报（逐字）

```text
Done. Brief R2 satisfied; all three deliverables plus the script are in <REPO>\tests\skills\plot-origin\red\out-R2\.

WHAT I READ
Only the brief (<TMP>\m3-origin-t3-red\brief-R2.md). No other project file was opened — I did not look at out-R1/out-R3, the plot-origin skill, or any repo doc. OriginPro's own Python API was probed by runtime introspection (dir/signature) rather than by reading files.

PRODUCED (all in <REPO>\tests\skills\plot-origin\red\out-R2\)
- make_figure.py — 8,981 bytes. Self-contained: data hard-coded, no network, one command, writes all three outputs itself (so the caption's numbers can never drift from the plotted ones). Ends with try/finally: op.exit().
- figure.png — 68,737 bytes, 2100 x 1488 px (~326 dpi on a 6.43 x 4.56 in Origin page), white background.
- figure.pdf — 7,760 bytes, 1 page, MediaBox 772 x 548 pt; verified to be a real vector export (237 text-show ops + 378 path ops in the decompressed content stream).
- caption.txt — 873 bytes, English, plain text.

ANSWER THE FIGURE GIVES
Pearson r against historical disaster count, over the six districts: mean slope +0.930, infrastructure index −0.777, vegetation cover −0.744, population density +0.360. So mean slope is by far the strongest driver; the OLS fit is count = 5.37 + 2.20 x slope. District similarity: A and C pair up (gentle slope, high vegetation, low counts), as do B and D (steep, sparse vegetation, high counts); E and F sit between the two pairs.

CHART CHOICE AND WHY
A two-panel figure, because the brief asks two different questions:
- Panel (a) scatter (mean slope x, disaster count y), one labelled point per district A–F, plus the least-squares line and a two-entry legend — slope is the dominant continuous driver and this is where "which districts look alike" is visible; labelling by district is what makes the similarity readable.
- Panel (b) bar chart of Pearson r for all four candidate attributes, ranked by |r|, split into two series (blue r>0, orange r<0) so sign is carried by both colour and direction — this answers "which factor" as a ranked comparison rather than six more scatter panels.
Palette is two colours only (blue #2E5C8A / orange #C1663D) shared across both panels.

ENVIRONMENT ISSUES HIT AND FIXED
1. `save_fig` with a relative path silently writes into Origin's User Files folder, not the cwd — must pass an absolute path.
2. `gp.add_layer(2)` ("righty") produced a layer nested inside layer 1 and inherited its geometry; `add_layer(0)` gives a clean independent layer and is what the script uses.
3. A freshly added layer has no legend object (`gl.label('legend')` returns None); `gl.lt_exec('legendupdate;')` creates it.
4. The graph page keeps its template aspect ratio: setting page width *or* height rescales the other, so a wider page is not achievable this way (set_float/lt_exec on page.width/height both rescale). The two panels are therefore laid out inside the default 6.43 x 4.56 in page; the figure is 1.41:1.
5. A layer resize redraws the axes and drops an earlier tick-label rotation — the rotate call is re-applied after the layer geometry is set.
6. Axis font size and rotation are settable via the Layer (`x.label.font`, `x.label.rotate`); the axis object itself has no set_int/set_str, and no working font-face property (`x.label.font.name` etc. all read back empty), so the tick/label font face is Origin's default.
7. Determinism: the PDF is byte-identical across runs; the PNG differs in bytes (metadata/timestamp chunk) but is pixel-identical (verified by comparing two runs with numpy/PIL).
8. No stray Origin64.exe left behind after any run (checked with tasklist both times).
```

## 3. R3 写手自报（逐字，含补 PDF 那一轮的追加段）

```text
Done. Read only the brief (brief-R3.md); wrote only into out-R3/.

PRODUCED (all in <REPO>\tests\skills\plot-origin\red\out-R3\)
- make_figure.py (5,337 B) - regenerates the figure from the brief's table via the originpro package; wraps everything in try/finally with op.exit().
- figure.png (27,207 B; 1950 x 1382 px = 6.5 in wide at 300 dpi, white background).
- caption.txt (932 B) - English, plain text, paste-ready.

CHART CHOICE
100% stacked column (Origin `plotxy ... plot:=213`), districts in Table-1 order A-F, segments Low -> Medium -> High bottom-to-top, y axis 0-1 with 0.2 ticks ("Share of district area"), legend outside the frame on the right.
Why: the task is composition of a whole that sums to 1.00 per district, read across six districts - a stacked-column chart answers both halves at once (within-district shares and between-district comparison), where pies/facets would not be comparable. The three fills are an explicit sequential single-hue ramp (OrRd: #FEE8C8 / #FDBB84 / #E34A33), light -> dark = low -> high vulnerability, so the ordinal tier order survives greyscale printing.

SIMILARITY ANSWER (stated in the caption, independently recomputed)
B and D are the most similar: shares 0.31/0.44/0.25 vs 0.28/0.47/0.25, max component gap 0.03, total absolute difference 0.06 - the unique minimum over all 15 pairs (next closest: A-E and C-F, both 0.10). The caption also notes the high tier is the smallest and near-constant everywhere (0.15-0.25), so it does not separate districts.

ENVIRONMENT ISSUES HIT AND FIXED
1. `worksheet -p <type>` (the classic LabTalk plotting command) hangs forever in this hidden-session setup - presumably a modal dialog that nobody can dismiss. It hung two probe runs and each hang left an Origin64.exe behind. Abandoned it; `plotxy` + explicit range works and returns cleanly.
2. The `plotxy plot:=` id table is NOT the classic 200/201/202 set (201 renders a scatter, 200/202 blank). Found the right one empirically: swept ids 200-230, exported each and measured pixel coverage, then tiled the candidates into one contact sheet - `plot:=213` is the 100% stacked column (216 is the horizontal equivalent).
3. A Unicode output path passed with backslashes got silently corrupted (a `\t` in `\tests` became a TAB), so `save_fig` returned '' and wrote nothing, with no exception. Switched to forward slashes / os.path.join and made save_fig's return value a hard error.
4. `layer.x.label.font$="Times New Roman"` silently switches the axis tick labels to a BOLD face (verified by zooming the rendered pixels; `bold=0` does not undo it). Dropped font-name assignment entirely - the Origin template already uses a serif face - and set only point sizes.
5. Legend: `%(n)` placeholders resolve to empty when assigned through `legend.text$`, and `\r\n` escapes are not interpreted by LabTalk (produced a one-line, clipped legend). Fixed by setting `Label.text` through the API with real CRLF and `\l(n)` symbol codes; position is now computed from the runtime page/legend geometry rather than hardcoded.
6. `legend.show` is a bool property, not a method (TypeError).
7. Page geometry: the template locks the page aspect ratio at sqrt(2) (~1.411); setting page.width rescales the height. Accepted the resulting 6.5 x 4.6 in page.
8. Determinism: two runs give byte-different PNGs (Origin writes varying PNG metadata) but pixel-identical images - verified with numpy. So content is reproducible, bytes are not.
9. All stray Origin64.exe processes my hung probes left were killed by explicit PID (verified clean at the end; the finished script leaves none).

Note: temporary probe images were written inside out-R3 while I was reverse-engineering the Origin API; they have all been deleted, so the directory contains exactly the three deliverables.
```

**追加一轮（补 PDF；只加"再导出一个载体"，未给任何新信息）的自报（逐字）**：

```text
Follow-up done. `figure.pdf` now exists alongside the PNG, produced by the same `make_figure.py` in the same run.

FILES (<REPO>\tests\skills\plot-origin\red\out-R3\)
- make_figure.py (6,134 B) - unchanged workflow, now exports both carriers; still try/finally + op.exit().
- figure.png (35,503 B; 1950 x 1382 px, 300 dpi, 6.5 in wide)
- figure.pdf (3,794 B)
- caption.txt (932 B)

PDF ANSWERS YOU ASKED FOR
- File size: 3,794 bytes.
- Page size: 468.0 x 332.0 pt = 6.500 x 4.611 in = 165.1 x 117.1 mm (1 page). Same aspect as the PNG (1.411), which is the Origin template's locked page ratio.
- Vector: yes. 0 image XObjects - the page has no /XObject entry at all, the file contains no "/Subtype /Image", and the content stream has no `Do` operator. Content is path ops (`re`, `f`, `S`) plus text (`BT`/`Tj`) in 4 embedded TrueType subsets. 9,236 bytes of content stream.

tasklist //FI "IMAGENAME eq Origin64.exe" -> "INFO: No tasks are running which match the specified criteria." No leftover process.

WHAT CHANGED TO GET THE PDF RIGHT (beyond just adding the call)
1. Origin page units turned out to be 1/600 in, not 1/1000 in: the first PDF came out 10.85 x 7.68 in. Retuned PAGE_W to 3900 units = 6.5 in, which also makes the PNG a true 300 dpi and keeps the 9/10 pt labels at their real print size instead of shrinking them to ~5.5 pt.
2. With the smaller page the original sizes overflowed - the x-axis title "District" was clipped off the bottom and the legend overlapped the plot frame. Retuned to ticks/legend 9 pt, axis titles 10 pt, and narrowed the layer (left 12%, width 62%, top 12%, height 74%); the legend is still positioned from runtime geometry (page width minus measured legend width), so it adapts rather than being hardcoded.

ONE RESIDUAL LIMITATION, STATED PLAINLY (both carriers affected, so they stay consistent)
The embedded text font is SimSun, not Times New Roman. I could not force a Latin serif reliably: `layer.x.label.font$="Times New Roman"` leaves the exported PDF entirely unchanged (verified by reading the PDF font table - only SimSun), the alternative `layer.x.label.font` is an integer index whose sweep on this machine yielded only CJK faces (MS-Gothic, MalgunGothic, MicrosoftYaHei, MingLiU, NotoSansSC...), and that index is machine-specific. I chose not to hardcode an index, since a wrong fallback would produce a nameless font resource and make the script non-portable. The text is legible and fully vector; if a Latin serif matters downstream it needs a template/theme change rather than a script change. This is the only thing I would call a quality gap.

DETERMINISM (unchanged from before): repeated runs give byte-different PNGs but pixel-identical images; the PDF is likewise content-stable.
```

---

## 附：可复核的两条命令（当场跑过）

```text
$ for n in 1 2 3; do cmp tests/skills/figure-choose/red/brief-R$n.md "$TEMP/m3-origin-t3-red/brief-R$n.md" && echo "R$n identical"; done
R1 identical
R2 identical
R3 identical

$ tasklist //FI "IMAGENAME eq Origin64.exe"
INFO: No tasks are running which match the specified criteria.
```

★ **本支与另两支载体的一处口径差异（如实记）**：写手**读了工具链**（见上"本支特有的一条额外披露"）。
 另两支的写手只需知道语言本身；Origin 的 API **不在任何随附文档里**（R1/R3 都这么说），
 所以"读工具链"是本支**不可避免**的旁路。它泄的是**工具面**，不是**规范面**。
