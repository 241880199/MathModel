# Task 4 · RED × GREEN 对照证据（`mcm-plot-matlab`）

本文件由 `tests/skills/plot-matlab/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
文里每个读数都来自下面附的原始 stdout。**对照表是机器抽取的**：判词行逐格解析成
`(状态, 判据 ID, 详情)`，不是手抄。

## §0 口径（两侧同源同数）

- **场景**：`tests/skills/plot-matlab/red/brief-R{1,2,3}.md`（MATLAB 版，场景/数据段与
  `tests/skills/figure-choose/red/brief-R{1,2,3}.md` **逐字节相同**、只换 Deliverables 段）。
  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景。
- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。
- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。
  工作树 blob `31621e433d23` · `HEAD:` blob `31621e433d23` ⇒ **相同**
- **同数**：每侧 3 场景 × 2 载体（PNG/PDF）= **6 张图**，两侧共 12 张；判据 9 条 × 12 张。
- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行；
  **PDF 不给 `--dpi`**（走页盒）。
- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；
  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。
  RED **不 `addpath` 本模块、不调 `mcmplot`**。
- **GREEN 侧**：由本任务 agent **用模块**（`mcmplot` 的 `figure/apply/save`）产出；
  **图注是判断层动作**（我写的），不是场景给的。
- ★ **两个载体不可比 `F2`**：PNG 与 PDF 在检查器里走**不同的栅格化路径**
  （PNG 原生像素、PDF 按固定的 150 dpi 栅格化）⇒ F2/F5 的读数**不是同一个量**，
  **不许跨载体比 F2**（见 §4 的探针与收窄说明）。

## §1 RED 原始读数（朴素写手 · 无规范）

### R1（dpi=298）

图注（`red/out-R1/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six study districts. Each bar is one
district (A-F) and is divided into the share of that district's land area in the
low, medium and high vulnerability tiers; because the three shares of a district
sum to 1.00, all bars have the same height and are directly comparable. Sections
are labelled with their share values. Low vulnerability is the largest tier in
districts C (0.55), F (0.50) and A (0.42), whereas medium vulnerability is the
largest tier in D (0.47), B (0.44) and E (0.38); the high tier is the smallest
component of every district and varies only over the narrow range 0.15 (C) to
0.25 (A, B, D, E). The bracket marks the two districts with the most similar
structure. Districts B and D are that pair: their low, medium and high shares
differ by only 0.03, 0.03 and 0.00 respectively, a total absolute difference of
0.06, below the next closest pairs A-E and C-F (0.10 each). The remaining
districts diverge more sharply, C and D being the most dissimilar (0.54).
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R1\figure.png --caption @tests\skills\plot-matlab\red\out-R1\caption.txt --textwidth-in 6.31 --dpi 298
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 98.07%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 57.34%）；下限 136
FAIL  F1  图宽比 0.748（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#9ec9e0', 0.1534), ('#fcbf59', 0.1417), ('#c93030', 0.0809)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 178 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 178 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R1\figure.pdf --caption @tests\skills\plot-matlab\red\out-R1\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 99.19%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 57.28%）；下限 136
FAIL  F1  图宽比 0.748（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#9ec9e0', 0.1446), ('#fcbf59', 0.1328), ('#c93030', 0.075)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 178 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 178 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

### R2（dpi=486）

图注（`red/out-R2/caption.txt`，逐字）：
```text
Figure 1. Drivers of historical disaster counts across the six districts (A-F).
(a) Pearson correlation between each measured attribute and the historical
disaster count, sorted by absolute strength. Mean slope is the factor most
strongly correlated with disaster count (r = +0.93), followed by the
infrastructure index (r = -0.78) and vegetation cover (r = -0.74); population
density is only weakly related (r = +0.36). Steeper terrain therefore goes with
more historical disasters, whereas denser infrastructure and higher vegetation
cover go with fewer.
(b) District similarity, shown as standardized (z-scored) attribute profiles,
with districts ordered so that similar ones are adjacent. Two groups emerge.
Districts D and B are the most similar pair: they are the two steepest districts
and record the highest disaster counts (D: 14.8 degrees, 38 events; B: 11.5
degrees, 31 events), and both have low population density. D is the more extreme
of the two, and of all districts, holding the lowest vegetation cover (0.41) and
the lowest infrastructure index (55). Districts A, C and E form the opposite,
low-risk group: gentle slopes and below-average disaster counts (8-16, C being
the lowest at 8); among them A and C also exceed the average in vegetation cover
and infrastructure, with C the most extreme on both (vegetation 0.72,
infrastructure 81). District F is the least typical: near average on every
attribute except population density, where it is the clear outlier (1750
people/km2, z = +1.7), and its disaster count is only moderate (24). Because
only six districts are available, these correlation coefficients are indicative
rather than statistically precise.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R2\figure.png --caption @tests\skills\plot-matlab\red\out-R2\caption.txt --textwidth-in 6.31 --dpi 486
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 99.85%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 72.77%）；下限 136
FAIL  F1  图宽比 1.310（分母 6.31 in）
FAIL  F2  彩色主色数 15
FAIL  F5  越界主色 21 种（不在 H14 允许集合）：[('#2166ab', 0.0256), ('#c93036', 0.0217), ('#c2d5e8', 0.0109), ('#d14d51', 0.0108)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 261 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 261 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F2,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R2\figure.pdf --caption @tests\skills\plot-matlab\red\out-R2\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.95%）；下限 136
FAIL  F1  图宽比 1.310（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 2 种（不在 H14 允许集合）：[('#2066ab', 0.007), ('#c93036', 0.006)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 261 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 261 词）
FAIL  F6  内嵌字体 ['ArialMT']
RESULT: FAIL（F1,F5,F3a,F3b,F3c,F6）
[exit=1]
```

### R3（dpi=299）

图注（`red/out-R3/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six districts (A-F): the share of each district's land area falling into the low, medium and high vulnerability tiers, which sum to 100% within every district. Districts C and F are the least vulnerable, with the largest low-tier shares (55% and 50%) and the smallest high-tier shares (15% and 17%), while D and B devote the largest shares to the medium tier (47% and 44%). Districts B and D have the most similar structure: their tier shares differ by at most 3 percentage points (low 31% vs 28%, medium 44% vs 47%, high 25% vs 25%), the smallest discrepancy of any pair of districts.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R3\figure.png --caption @tests\skills\plot-matlab\red\out-R3\caption.txt --textwidth-in 6.31 --dpi 299
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 96.45%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 52.58%）；下限 136
PASS  F1  图宽比 0.846（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#fee0d2', 0.1791), ('#fc9272', 0.1669), ('#de2d26', 0.0939)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 110 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 110 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\red\out-R3\figure.pdf --caption @tests\skills\plot-matlab\red\out-R3\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 99.82%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 52.73%）；下限 136
PASS  F1  图宽比 0.847（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#fee0d2', 0.1712), ('#fc9272', 0.1599), ('#de2d26', 0.0902)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 110 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 110 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']
RESULT: FAIL（F5,F3a,F3b,F3c）
[exit=1]
```

## §2 GREEN 原始读数（模块 · `mcmplot`）

### G1（dpi=300）

图注（`green/out-G1/caption.txt`，逐字）：
```text
Figure 1: Vulnerability composition by district; B and D most similar
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G1\figure.png --caption @tests\skills\plot-matlab\green\out-G1\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 63.65%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 9（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 9 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G1\figure.pdf --caption @tests\skills\plot-matlab\green\out-G1\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 63.13%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 9（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 9 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']
RESULT: PASS
[exit=0]
```

### G2（dpi=300）

图注（`green/out-G2/caption.txt`，逐字）：
```text
Figure 2: Pearson correlation of district attributes with disaster count
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G2\figure.png --caption @tests\skills\plot-matlab\green\out-G2\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 86.60%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 1
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 8（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 8 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G2\figure.pdf --caption @tests\skills\plot-matlab\green\out-G2\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 85.97%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 1
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 8（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 8 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']
RESULT: PASS
[exit=0]
```

### G3（dpi=300）

图注（`green/out-G3/caption.txt`，逐字）：
```text
Figure 3: Vulnerability composition by district, paper-ready
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G3\figure.png --caption @tests\skills\plot-matlab\green\out-G3\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 69.11%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 5（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 5 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-matlab\green\out-G3\figure.pdf --caption @tests\skills\plot-matlab\green\out-G3\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 68.35%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 5（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 5 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']
RESULT: PASS
[exit=0]
```

## §3 对照表（机器抽取）

每个格子 = `状态`（绿=PASS / 红=FAIL）。同场景同行，RED 与 GREEN 并列；判据 ID 见表头。

| 场景 | 载体 | 侧 | F1 | F2 | F3a | F3b | F3c | F3d | F4 | F5 | F6 | RESULT |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G1 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R1 | PDF | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G1 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R2 | PNG | RED | 红 | 红 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G2 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R2 | PDF | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 红 | FAIL |
| G2 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R3 | PNG | RED | 绿 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G3 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R3 | PDF | RED | 绿 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G3 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |

### §3.1 逐判据红/绿明细（含判词，机器抽取）

| 场景 | 载体 | 侧 | 判据 | 状态 | 判词 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | F1 | FAIL | 图宽比 0.748（分母 6.31 in） |
| R1 | PNG | RED | F2 | PASS | 彩色主色数 3 |
| R1 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R1 | PNG | RED | F3b | FAIL | 图注词数 178 超硬上限 17 |
| R1 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R1 | PNG | RED | F3d | PASS | 图注正文非空（正文 178 词） |
| R1 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 98.07%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 57.34%）；下限 136 |
| R1 | PNG | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#9ec9e0', 0.1534), ('#fcbf59', 0.1417), ('#c93030', 0.0809)] |
| R1 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G1 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G1 | PNG | GREEN | F2 | PASS | 彩色主色数 3 |
| G1 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G1 | PNG | GREEN | F3b | PASS | 图注词数 9（上限 12，硬上限 17） |
| G1 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G1 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 9 词） |
| G1 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 63.65%）；下限 136 |
| G1 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G1 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R1 | PDF | RED | F1 | FAIL | 图宽比 0.748（分母 6.31 in） |
| R1 | PDF | RED | F2 | PASS | 彩色主色数 3 |
| R1 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R1 | PDF | RED | F3b | FAIL | 图注词数 178 超硬上限 17 |
| R1 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R1 | PDF | RED | F3d | PASS | 图注正文非空（正文 178 词） |
| R1 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 99.19%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 57.28%）；下限 136 |
| R1 | PDF | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#9ec9e0', 0.1446), ('#fcbf59', 0.1328), ('#c93030', 0.075)] |
| R1 | PDF | RED | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT'] |
| G1 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） |
| G1 | PDF | GREEN | F2 | PASS | 彩色主色数 3 |
| G1 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G1 | PDF | GREEN | F3b | PASS | 图注词数 9（上限 12，硬上限 17） |
| G1 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G1 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 9 词） |
| G1 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 63.13%）；下限 136 |
| G1 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G1 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT'] |
| R2 | PNG | RED | F1 | FAIL | 图宽比 1.310（分母 6.31 in） |
| R2 | PNG | RED | F2 | FAIL | 彩色主色数 15 |
| R2 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R2 | PNG | RED | F3b | FAIL | 图注词数 261 超硬上限 17 |
| R2 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R2 | PNG | RED | F3d | PASS | 图注正文非空（正文 261 词） |
| R2 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 99.85%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 72.77%）；下限 136 |
| R2 | PNG | RED | F5 | FAIL | 越界主色 21 种（不在 H14 允许集合）：[('#2166ab', 0.0256), ('#c93036', 0.0217), ('#c2d5e8', 0.0109), ('#d14d51', 0.0108)] |
| R2 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G2 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G2 | PNG | GREEN | F2 | PASS | 彩色主色数 1 |
| G2 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G2 | PNG | GREEN | F3b | PASS | 图注词数 8（上限 12，硬上限 17） |
| G2 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G2 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 8 词） |
| G2 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 86.60%）；下限 136 |
| G2 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G2 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R2 | PDF | RED | F1 | FAIL | 图宽比 1.310（分母 6.31 in） |
| R2 | PDF | RED | F2 | PASS | 彩色主色数 3 |
| R2 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R2 | PDF | RED | F3b | FAIL | 图注词数 261 超硬上限 17 |
| R2 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R2 | PDF | RED | F3d | PASS | 图注正文非空（正文 261 词） |
| R2 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.95%）；下限 136 |
| R2 | PDF | RED | F5 | FAIL | 越界主色 2 种（不在 H14 允许集合）：[('#2066ab', 0.007), ('#c93036', 0.006)] |
| R2 | PDF | RED | F6 | FAIL | 内嵌字体 ['ArialMT'] |
| G2 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） |
| G2 | PDF | GREEN | F2 | PASS | 彩色主色数 1 |
| G2 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G2 | PDF | GREEN | F3b | PASS | 图注词数 8（上限 12，硬上限 17） |
| G2 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G2 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 8 词） |
| G2 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 85.97%）；下限 136 |
| G2 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G2 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT'] |
| R3 | PNG | RED | F1 | PASS | 图宽比 0.846（分母 6.31 in） |
| R3 | PNG | RED | F2 | PASS | 彩色主色数 3 |
| R3 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R3 | PNG | RED | F3b | FAIL | 图注词数 110 超硬上限 17 |
| R3 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R3 | PNG | RED | F3d | PASS | 图注正文非空（正文 110 词） |
| R3 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 96.45%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 52.58%）；下限 136 |
| R3 | PNG | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#fee0d2', 0.1791), ('#fc9272', 0.1669), ('#de2d26', 0.0939)] |
| R3 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G3 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G3 | PNG | GREEN | F2 | PASS | 彩色主色数 3 |
| G3 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G3 | PNG | GREEN | F3b | PASS | 图注词数 5（上限 12，硬上限 17） |
| G3 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G3 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 5 词） |
| G3 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 69.11%）；下限 136 |
| G3 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G3 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R3 | PDF | RED | F1 | PASS | 图宽比 0.847（分母 6.31 in） |
| R3 | PDF | RED | F2 | PASS | 彩色主色数 3 |
| R3 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R3 | PDF | RED | F3b | FAIL | 图注词数 110 超硬上限 17 |
| R3 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R3 | PDF | RED | F3d | PASS | 图注正文非空（正文 110 词） |
| R3 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 99.82%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 52.73%）；下限 136 |
| R3 | PDF | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#fee0d2', 0.1712), ('#fc9272', 0.1599), ('#de2d26', 0.0902)] |
| R3 | PDF | RED | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT'] |
| G3 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） |
| G3 | PDF | GREEN | F2 | PASS | 彩色主色数 3 |
| G3 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G3 | PDF | GREEN | F3b | PASS | 图注词数 5（上限 12，硬上限 17） |
| G3 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G3 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 5 词） |
| G3 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 68.35%）；下限 136 |
| G3 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G3 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT'] |

### §3.2 汇总（由 §3 的格子逐格重算）

| 侧 | 红格数（判据×图） | 判红的判据 ID（并集） | 全绿图数 |
| :-- | :-- | :-- | :-- |
| RED | 30 | F1、F2、F3a、F3b、F3c、F5、F6 | 0/6 |
| GREEN | 0 | （无） | 6/6 |

## §4 F2 与载体（**不许跨载体比 F2**）

同一份数据、同一张图（六段**横向堆叠条**，**H14 配色**）；被换的量 = **描不描白边**（驱动脚本里就改 `EdgeColor` / `LineWidth` 两个字段，其余逐行相同），每态各出两载体。读数**当场算**（`check-figure-style.py` 本人的判词，逐字抄）：

```
              PNG  PDF
描白边          3    3
不描边（对照）   3    3
```

⇒ 本机实测（R2025b Update 5）：**就这一个构造、这两态**而言，同图两态的 F2 在 PNG 与 PDF 上逐格相同（描白边 3/3 · 不描边 3/3）—— **与 python 侧那件探针的结论相反**（python 上描白边把 PNG 的 F2 由 3 抬到 5、PDF 不变）。
⇒ **如实收窄（射程只到这里）**：本探针只证明「**这一个构造、这两态**不移动 F2」，**驳不倒**「MATLAB 产物的 F2 可以随载体变」—— 另有一个**未入库的自造构造**能把同一张图的 F2 在两个载体上拉开（读数未落盘，此处不复述，先例 `M3-plot-INIT`）。故本探针**不构成**「MATLAB 上 F2 不随载体变」的证据，**也无权**被那样读。
**那么「不许跨载体比 F2」这条规矩**的承重**不是**本探针，而是**器械口径**：检查器对两载体走**不同的栅格化路径** —— PNG 直接 `Image.open`（原生像素、按 `--dpi` 定尺）、PDF 第 1 页按固定 `RASTER_DPI=150` 栅格化（`raster_rgb()`）⇒ 同一条 `color_count` 吃到的像素来源不同 ⇒ 两个读数**不是同一个量**，故**不可跨载体比**。这是设计 §2、检查器 docstring 与 python 先例共同定下的口径。
同一支检查器的 F5 判词（逐字）：

```
描白边 PNG：越界主色 0 种（不在 H14 允许集合）：[]
描白边 PDF：越界主色 0 种（不在 H14 允许集合）：[]
不描边 PNG：越界主色 0 种（不在 H14 允许集合）：[]
不描边 PDF：越界主色 0 种（不在 H14 允许集合）：[]
```


- **仓内实测佐证 —— 同一张图的 F2 在两个载体上不同（逐图，机器抽取自 §1/§2）**：

| 场景 | 侧 | F2(PNG) | F2(PDF) | 随载体变？ |
| :-- | :-- | :-- | :-- | :-- |
| R1 | RED | 3 | 3 | 否 |
| R2 | RED | 15 | 3 | **是** |
| R3 | RED | 3 | 3 | 否 |
| G1 | GREEN | 3 | 3 | 否 |
| G2 | GREEN | 1 | 1 | 否 |
| G3 | GREEN | 3 | 3 | 否 |

⇒ `R2`（PNG 15 / PDF 3）是**仓内实例**：同一张图的两载体 F2 确实不同 —— 但它**不是**「不许跨载体比 F2」的**唯一**支撑（该规矩的承重是上面那条**器械口径**：两载体走两条栅格化路径 ⇒ 读数不是同一个量）。其余各行两载体相同、也不矛盾 —— 该规矩是**禁止把一个载体的读数当成另一个的**，不是声称「每张图的 F2 都会变」。

## §5 判断层（亲眼看图 · 机械判据之外的那一层）

**这一节是判断层，机械判据判不了它。** 下面是我（本任务 agent）**亲眼看图**后写下的：读到了什么、
读不出什么。**写真话**。六张图（逐张列在下面、各带仓内相对路径）我都打开看过（PNG），并另核了 PDF 同源。
对每一张必看的两点：**底色是不是浅色** · **顶/右框线在不在、刻度朝内还是朝外**（`H10`）。
刻度朝向不是"看着像"：用像素量过（底脊线上方 / 下方各 8 px 带里灰度 < 60 的墨迹像素数），读数写在每条里。

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（`tests/skills/plot-matlab/green/out-G1/figure.png`，R1 构成，竖堆叠条）**：
  **底色浅色**（F4 外缘环 100% 白）；**无顶/右框线**；**刻度朝内**（底脊上方 130 : 下方 32 墨迹像素）。
  轴标签带单位（`Share of district area (fraction)`）。读得出：六区 A–F 的三档构成与每段占比；
  读不出：这张图**没有**替读者判断"B 与 D 最像"——那条判断是我在图外另算的。
- **G2（`.../green/out-G2/figure.png`，R2 相关，横条）**：**底色浅色**；**无顶/右框线**；
  **刻度朝内**（77 : 21）。读得出：四条属性的 Pearson r 与灾难次数（mean slope 最强 ≈ +0.93）。
  **看图层逼出两处修图**（初版四个类目名平排互相压住、
  ylabel 太长在 2.6 in 图高里被裁掉顶端 ⇒ 类目名旋 20°、ylabel 缩成 `Pearson r (dimensionless)` 后重出）。
  **初版送检是自报口径**：出图时另跑过一次初版送检、观察到 F1–F6 全 PASS（**未捕获 stdout、未落产物**）；
  **承重的是结构论证**：检查器的 `F1`–`F6` **本来就没有**任何关于刻度标签排版的判据 ——
  一条命令即可列举其全部判据（`grep -nE 'res\.append\(\("F' tests/skills/figure-choose/check-figure-style.py`，
  实测 9 条，无刻度标签排版类）；详见 `green/README.md` §3.1。
  读不出：图上只有 Pearson，n=6 的稳健性不在图上。
- **G3（`.../green/out-G3/figure.png`，R3 交付形态，横堆叠条）**：**底色浅色**；**无顶/右框线**；
  **刻度朝内**（119 : 0）。轴标签带 `(fraction)`。读得出：同 R1 数据横过来、单栏可直接进正文。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1（`tests/skills/plot-matlab/red/out-R1/figure.png`）**：竖堆叠条，段内印占比，顶部括线标
  "most similar pair: B & D (L1 = 0.06)"。**底色浅色**（写手**自己**把出厂深色修掉了 —— 其自报：
  本机 MATLAB 跑深色主题、首图导出成黑底，它 pin 了 `ax.Color = 'w'`）；**无顶/右框线**；
  **但刻度朝外**（41 : 95）。信息很足；反差点在**形态**：图偏窄（F1 = 0.748）、配色不落 H14（F5 = 3 种越界）、
  图注 178 词且以句号结尾（F3a/b/c 三条红）。
- **R2（`.../red/out-R2/figure.png`）**：两联图（a 相关横条 + b z-score 热图带 colorbar），
  每个格子印 z 值、相关条带值标 —— 信息量最大的一张。**底色浅色**；**刻度朝内**（907 : 227，量的是 b 面板）；
  **但 b 面板的坐标系带完整四边黑框（上/右框线都在）** —— `H10` 要的是去上/右框线，这一点它没做到。
  反差点：F1 = 1.310 偏宽、F2 PNG = 15（热图多档）、F5 越界 21 种、图注 261 词、PDF 内嵌 **ArialMT**（F6 红）。
- **R3（`.../red/out-R3/figure.png`）**：横堆叠条，Reds 单色三档，段内印整数百分比。
  **底色浅色**；**无顶/右框线**；**刻度朝外**（14 : 78）；xlabel 带 `(%)` 单位。
  反差点：配色（#fee0d2 / #fc9272 / #de2d26）不落 H14（F5 红）、图注 110 词且以句号结尾（F3a/b/c 红）；
  F1 = 0.846 在带内、F2 = 3 绿。

### 一句话
**机械层测的是"形态合不合规范"，判断层测的是"图讲没讲清"。** 六张图（上面六条）都真看过以后：
三张 RED 的信息常常更多（R1 标出最相似对、R2 连 z 值都印了）、底色也都自己修成了浅色，
却仍在**形态**上判红；而且 **R1 / R3 的刻度朝外、R2 的 b 面板带上/右全框** 这三条 `H10` 违反，
**检查器的 F1–F6 没有一条会报** —— 只能靠这一层看见（`H10` 的产物级回读另有入库探针）。
三张 GREEN 形态全绿，但"支持判断"那一层要我在图上另加一笔、图注里另写一句 ——
把 GREEN 读成"这张图没问题"是不对的。
