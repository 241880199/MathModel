# Task 4 RED 基线的派发提示词与写手自报（`mcm-plot-matlab`）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何"写手" agent 读过本文件，产出的就不再是
> RED 基线。与它同案看待的还有 `red-green-evidence.md`（在上一级）与 `red/README.md`。

【为什么有这个文件】本任务里**最难核实**的一件是"写手到底读到了什么"：
 其余面向（提示词逐字 / 未用 `fork` / 产物本身）都能从入库件复核，**这一件不能** ——
 它只能靠**审计写手的自报**（凭据：transcript 不可解析，见文末）。

【来源 —— 与先例不同，**照实记**】先例 `figure-choose/red/writer-self-reports.md` 是从仓外
 transcript 文件里**程序化**摘出的。本任务**做不到**：本会话 subagent 的 `.output` 文件实测为
 **0 字节**（命令与输出见文末），transcript 不在可解析的位置。故本文件的提示词与自报是
 **逐字转录自会话内 `SubagentHandback` 投递的文本**（写手自己回给调度者的那段），
 **不是**从 transcript 文件里机器摘的。⇒ 本文件**没有**机器可复核的"逐字节"保证，
 只有**转录音频级**的忠实度声明。

【对原文的唯一加工】写手自报里写了**绝对路径**，本仓规定证据不写绝对路径，故掩码之：
 本仓根 → `<REPO>`。除此之外**逐字未改**（写手自报里出现的、不含用户名的第三方安装路径
 —— 如 MATLAB 安装路径 —— **原样保留**，与 python 先例同口径）。

【强度声明】"写手是否真的只读了那一份 brief"**只有自报、没有沙箱可证**（另外：**未用 `fork`**
 —— 三个写手都是新起的干净上下文 agent，首条 user 消息就是下面那一条提示词本身）。
 自报一致 ≠ 已证。

【环境旁路的如实披露（照 python 先例的强度写，不许省）】"只给两样"说的是**派发那一刻的 user
 消息**；但写手是本机 Claude Code 的 agent，**会话级共享上下文里另有两处本任务删不掉的可见面**：
 ① **可用 skill 列表里 `mcm-plot-matlab` 的那一行描述**——它恰好点名了**类别名**
    （"图宽比不合、底色是深色、字体族不对"），并列了 trigger `MATLAB 画图` / `print 导出` /
    `plot the figure in MATLAB`；
 ② **项目记忆文件 `MEMORY.md`**——它点名了本机**已装 TeX + SciencePlots**、以及
    "字体随 skill 入库"这类工具面信息。
 这两处**不在**派发消息里（§0 那句只给 brief 路径 + 输出目录），但写手**看得到**。
 **写手看得到 / 看不到的边界（关键）**：看得到的是**类别名与工具名**（"有这几类要求"、
"用的是 MATLAB"）；**看不到**的是**阈值与规范正文** —— F1 的合规带、F2 的主色上限、
F3b 的词数上限、F4 的亮度下限、要上浅色主题、色序要落 H14、字体族的可接受表，以及
 `house-style.md` 的条文，**一个字都没进写手的可见范围**（派发消息没有、skill 描述没有、
 记忆里也没有）。
 **为什么这**不**推翻 RED**：泄的只是"**有**这几类判据"、不是"判据的**边界**在哪"。证据是：
 三张图**仍全部判红**（R1 红 F1/F5/F3a/F3b/F3c；R2 红 F1/F2/F5/F3a/F3b/F3c/F6；R3 红 F5/F3a/F3b/F3c），
 而写手自报里**没有一处**引用过任何阈值或规范条文。这反而是**更强**的结论：**知道"有这几类判据"
 也照样判红** —— 合规不是靠"知道有要求"，得靠**读到阈值与规范正文**。
 ⇒ 旁路**不**足以让写手"见过规范"，RED 的对照**成立**。

---

## 0. 派发口径（三个写手逐字同一份模板，只换场景号与输出目录）

```text
Read the brief at <TMP>\m3-t4-red\brief-R{n}.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <REPO>\tests\skills\plot-matlab\red\out-R{n}\. Work only from that brief - do not read or write any other file.
```

（`<TMP>` = `%TEMP%\m3-t4-red`，其中放着 MATLAB 版 `brief-R{1,2,3}.md` 的**逐字节副本**——
权威副本是 `tests/skills/plot-matlab/red/brief-R{1,2,3}.md`；后者场景/数据段与
`tests/skills/figure-choose/red/brief-R{1,2,3}.md` **逐字节相同**。副本与权威副本 `cmp` 相同，见文末。）

**只给了两样**：① 场景 brief 的路径；② 产物输出目录。**未给**：规范
`house-style.md`、模块 `mcm-plot-matlab/`、判据 `check-figure-style.py`、本任务书、先例
`figure-choose/red/` 的任何证据件。末尾那句是**隔离句**（不给它读仓内别的文件），**不是**规范信息。

---

## 1. R1 写手自报（逐字）

```text
Done. Delivered brief R1 into <REPO>\tests\skills\plot-matlab\red\out-R1\ — worked only from brief-R1.md, no other file read or written.

Files produced (all in that directory):
- make_figure.m (6206 B) — MATLAB script, script-form (not a function), runnable headlessly with `matlab -batch "cd('<dir>'); make_figure"`. Data are inlined from the brief table; asserts each district row sums to 1.00; no randomness, no network, no manual steps.
- figure.png — 1406x830 px, 300 dpi, RGB truecolor, no alpha, white background.
- figure.pdf — vector (0 image XObjects), page 340 x 203 pt (12.0 x 7.2 cm), embedded TrueType font subset (FontFile2).
- caption.txt — English plain-text caption.

Chart choice and content: 100% stacked bar chart, one bar per district A–F in table order, three tiers in an ordinal light-to-dark palette (low = light blue #9EC9E0, medium = amber #FCC05A, high = red #C93030 — 3 colors total, colorblind-distinguishable, white segment edges). Share values are printed inside each segment with per-segment text color chosen by luminance. Ordinal axes: y ticks 0–1.0, light grey horizontal grid, box off, Times New Roman throughout. Headroom above 1.0 carries a bracket joining the closest pair, labelled "most similar pair: B & D (L_1 = 0.06)".

Answer to the brief's question, computed in-script from the data (L1 = sum of absolute share differences) and stated in the caption: districts B and D have the most similar structure (L1 = 0.06; shares differ by 0.03 low, 0.03 medium, 0.00 high), ahead of A–E and C–F (0.10 each); most dissimilar pair is C–D (0.54). Composition: low tier dominates C (0.55), F (0.50), A (0.42); medium dominates D (0.47), B (0.44), E (0.38); high is smallest everywhere and spans only 0.15–0.25.

Verification performed: script ran end-to-end from a clean directory; PNG is pixel-identical across two independent runs (0 differing pixels, same size). File MD5s differ between runs only because PNG/PDF metadata carries a creation timestamp — the rendered content is deterministic.

Two environment issues found and fixed in the script, worth noting since they will bite any MATLAB figure work on this machine:
1. MATLAB here is R2025b (D:\Software\Matlab\bin\matlab), where `bar(y,'stacked',width)` no longer parses — the width must be given as the name-value `'BarWidth'`. The old positional form throws "class Bar has no property 'stacked'".
2. This MATLAB install is running a dark theme, so the axes background defaults to near-black: the first render exported a black-backed figure even though the figure Color was white. The script now pins `ax.Color='w'` and legend TextColor/Color explicitly, so output no longer depends on the IDE theme.
```

## 2. R2 写手自报（逐字）

```text
Done. Brief R2 fully delivered; only the brief was read, nothing else.

Deliverables (all in <REPO>\tests\skills\plot-matlab\red\out-R2\)
- make_figure.m — MATLAB script computing everything from the tabulated numbers; headless-runnable via `matlab -batch "run('.../make_figure.m')"`; writes its outputs next to itself, no network, no manual steps.
- figure.png (600 dpi, 4016x1796 px)
- figure.pdf (vector)
- caption.txt (English, plain text)

Figure design — two panels answering the two halves of the question:
(a) signed Pearson correlation of each factor with the historical disaster count, sorted by |r|;
(b) district similarity as a z-scored attribute-profile heatmap (diverging blue-white-red, values annotated), with districts ordered by spectral seriation of pairwise distances so similar districts sit together.

Key results computed from the data
- Correlations with disaster count: mean slope r = +0.93 (strongest), infrastructure index r = -0.78, vegetation cover r = -0.74, population density r = +0.36 (weak). So mean slope is the factor most strongly correlated.
- District similarity order: D, B, F, E, A, C. D and B are the closest pair (steepest slopes, highest disaster counts 38 and 31; low population density); D is the most extreme overall (lowest vegetation 0.41, lowest infrastructure 55). A, C, E form the opposite low-risk group (gentle slopes, disasters 8-16, C lowest at 8 with the highest vegetation and infrastructure). F is the outlier, average on everything except a standout population density (1750 people/km^2, z = +1.7) with only a moderate disaster count (24).
- Caption notes the n = 6 caveat.

Two things worth flagging: (1) an initial bug where the correlation block indexed X(:,1:4), which included the disaster count column itself — caught by comparing the printed r values against a hand calculation and fixed to predictors [1 2 3 5] / outcome column 4. (2) The script is content-deterministic: re-running produces pixel-identical PNG data (verified via imread/isequal); byte-level hashes differ only because MATLAB embeds creation timestamps in the PNG/PDF metadata.
```

## 3. R3 写手自报（逐字）

```text
Done. All four deliverables are in `<REPO>\tests\skills\plot-matlab\red\out-R3\` and were produced working only from brief-R3.md:

- `make_figure.m` — self-contained MATLAB script (data hardcoded, no network, no manual steps, headless via `matlab -batch "run('make_figure.m')"`; it writes its two outputs next to itself and asserts the shares sum to 1).
- `figure.png` — 300 dpi raster.
- `figure.pdf` — single-page vector.
- `caption.txt` — English caption, plain text.

Figure design: a 100% stacked horizontal bar chart, one bar per district (A–F, alphabetical, A on top), segments Low → Medium → High in a sequential warm ramp (light → dark, ColorBrewer "Reds"), every segment annotated with its integer percentage, legend above the axes, x-axis 0–100%. Verified visually that the render matches the input table exactly (e.g. C = 55/30/15, D = 28/47/25).

Answer to the brief's question (used in the caption): the most similar pair is **B and D** — their tier shares differ by at most 3 percentage points (low 31% vs 28%, medium 44% vs 47%, high 25% vs 25%), the smallest discrepancy of any pair (next closest is C–F at a 5-point max difference). The caption also states the composition highlights: C and F least vulnerable (low 55%/50%, high 15%/17%), D and B most medium-heavy (47%/44%).

One issue worth flagging: this machine's MATLAB (R2025b) exports figures with a **dark background** by default — the axes patch rendered as near-black `[18 18 18]` even though `figure`/`axes` Color were set to white, so the bar gaps came out as heavy black stripes. Setting `figure`/`axes` Color was not enough; the fix was `theme(fig,'light')` (R2025a+ API, wrapped in try/catch for older releases). This is likely the "底色太深" failure mode and is worth carrying into the skill. Also note the earlier "black gridlines" I first suspected were a red herring — the stripes were the dark background, not gridlines.

Determinism check: PNG pixels are byte-identical across reruns; the PDF differs between runs only by its embedded `/CreationDate` metadata (rendered content identical).
```

---

## 附：可复核的两条命令（当场跑过）

```text
$ for n in 1 2 3; do cmp tests/skills/plot-matlab/red/brief-R$n.md "/c/Users/Shameless/AppData/Local/Temp/m3-t4-red/brief-R$n.md" && echo "R$n identical"; done
R1 identical
R2 identical
R3 identical

$ ls -l <TMP>/claude/D--Projects-----/fc24715f-b92e-4066-9ac7-d05f0dc98fec/tasks/{a0076bae5af7bcc2e,a85fa2b2c241c6448,aa2a24c3afb565d7d}.output
-rw-r--r-- 1 Shameless 197121 0 Oct  2 00:03 C:/Users/Shameless/AppData/Local/Temp/claude/D--Projects-----/fc24715f-b92e-4066-9ac7-d05f0dc98fec/tasks/a0076bae5af7bcc2e.output
-rw-r--r-- 1 Shameless 197121 0 Oct  2 00:03 C:/Users/Shameless/AppData/Local/Temp/claude/D--Projects-----/fc24715f-b92e-4066-9ac7-d05f0dc98fec/tasks/a85fa2b2c241c6448.output
-rw-r--r-- 1 Shameless 197121 0 Oct  2 00:03 C:/Users/Shameless/AppData/Local/Temp/claude/D--Projects-----/fc24715f-b92e-4066-9ac7-d05f0dc98fec/tasks/aa2a24c3afb565d7d.output
（三个写手的 .output 文件均为 0 字节 ⇒ transcript 不可程序化摘录，故本文件用转录）
```
