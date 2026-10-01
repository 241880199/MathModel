# Task 5 · RED × GREEN 对照证据（mcm-plot-python）

本文件由 `tests/skills/plot-python/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
文里每个读数都来自下面附的原始 stdout。**对照表是机器抽取的**：判词行逐格解析成
`(状态, 判据 ID, 详情)`，不是手抄。

## §0 口径（两侧同源同数）

- **场景**：同一份 `tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，未改写）。
  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景。
- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。
- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。
  工作树 blob `55e5e9683603` · `HEAD:` blob `55e5e9683603` ⇒ **相同**
- **同数**：每侧 3 场景 × 2 载体（PNG/PDF）= **6 张图**，两侧共 12 张；判据 9 条 × 12 张。
- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行。
- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；
  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。
  RED **不 import `mcmplot`、不用 `mcm.mplstyle`**。
- **GREEN 侧**：由本任务 agent **用模块**（`mcmplot.apply_style/figsize_for/save`）产出；
  **图注是判断层动作**（我写的），不是场景给的。

## §1 RED 原始读数（朴素写手 · 无规范）

### R1（dpi=300）

图注（`red/out-R1/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six districts (A-F). Left: share of
each district's land area falling in the low, medium and high vulnerability
tiers; the three shares sum to 100% within every district, and districts are
ordered by decreasing low-tier share (C, F, A, E, B, D). Right: Euclidean
distance between the composition vectors of all 15 district pairs, sorted from
most to least similar. Districts B and D have by far the most similar structure
(distance 0.042: they differ by at most 3 percentage points in any single tier
and share the same 25% high-tier share), well ahead of the next-closest pairs
A-E and C-F (0.062) and far from the most dissimilar pair C-D (0.334). Across
districts the high tier is nearly constant (15-25%), whereas the low tier ranges
from 28% (D) to 55% (C); the districts therefore differ mainly in how their
non-high area splits between the low and medium tiers, with C and F the most
low-dominated and D and B the most medium-dominated.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R1\figure.png --caption @tests\skills\plot-python\red\out-R1\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.213（分母 6.31 in）
PASS  F2  彩色主色数 4
FAIL  F5  越界主色 4 种（不在 H14 允许集合）：[('#5aae61', 0.0518), ('#f4a259', 0.0483), ('#c1443c', 0.0279), ('#faf1d6', 0.0172)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 168 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 168 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R1\figure.pdf --caption @tests\skills\plot-python\red\out-R1\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.214（分母 6.31 in）
PASS  F2  彩色主色数 4
FAIL  F5  越界主色 4 种（不在 H14 允许集合）：[('#5aae61', 0.0498), ('#f4a259', 0.0464), ('#c1443c', 0.0264), ('#faf1d7', 0.0163)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 168 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 168 词）
FAIL  F6  内嵌字体 ['DejaVuSans', 'DejaVuSans-Bold']
RESULT: FAIL（F1,F5,F3a,F3b,F3c,F6）
[exit=1]
```

### R2（dpi=300）

图注（`red/out-R2/caption.txt`，逐字）：
```text
Figure 1. Drivers of the historical disaster count and the similarity of the six districts. (a) Pearson correlation between each measured attribute and the historical disaster count, ordered by absolute strength; hollow circles mark the Spearman rank correlation and an asterisk marks p < 0.05. Mean slope is the only factor that is both strongly and significantly correlated with the disaster count (r = +0.93, p = 0.007), so terrain steepness rather than exposure or population dominates; the infrastructure index (r = -0.78) and vegetation cover (r = -0.74) act as weaker protective factors and population density is nearly unrelated (r = +0.36). (b) Pairwise Euclidean distance between districts in the space of all five standardised attributes; darker cells are more dissimilar and the red outlines mark the closest pair. Districts A and C are the most similar (d = 1.45), both combining gentle slopes, the highest vegetation cover and the strongest infrastructure, and E is the next nearest to this group, whereas D is the most distinct district overall (d = 2.91 to its nearest neighbour) because it pairs the steepest slopes and the lowest vegetation cover with the weakest infrastructure and the largest disaster count. With only six districts, these correlations are indicative rather than conclusive.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R2\figure.png --caption @tests\skills\plot-python\red\out-R2\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.385（分母 6.31 in）
FAIL  F2  彩色主色数 12
FAIL  F5  越界主色 15 种（不在 H14 允许集合）：[('#95b1ce', 0.0236), ('#6e8fbe', 0.0235), ('#4c72b0', 0.0218), ('#c44e52', 0.0125)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 208 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 208 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F2,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R2\figure.pdf --caption @tests\skills\plot-python\red\out-R2\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.385（分母 6.31 in）
FAIL  F2  彩色主色数 12
FAIL  F5  越界主色 15 种（不在 H14 允许集合）：[('#95b1ce', 0.0229), ('#6e8fbe', 0.0224), ('#4c72b0', 0.0214), ('#c44e52', 0.012)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 208 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 208 词）
FAIL  F6  内嵌字体 ['DejaVuSerif', 'DejaVuSerif-Italic']
RESULT: FAIL（F1,F2,F5,F3a,F3b,F3c,F6）
[exit=1]
```

### R3（dpi=300）

图注（`red/out-R3/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six districts and the similarity of their composition profiles. (a) Share of each district's land area in the low, medium and high vulnerability tiers; the three shares of every district sum to 1.00 and each is printed inside its segment. (b) Total variation distance between every pair of districts, TV(i, j) = 0.5 * sum_t |p_it - p_jt|, where p_it is the share of district i in tier t; the diagonal is omitted and darker cells denote more dissimilar districts. The most similar pair, outlined in orange in both panels, is B and D with TV(B, D) = 0.03: their compositions differ by 3 percentage points in total, their high-tier shares are identical (0.25) and their low and medium shares differ by 0.03 each. This is the smallest of all fifteen pairwise distances under both total variation and Euclidean distance, and less than half of the next smallest values (0.05 for A-E and C-F), whereas the least similar pair is C and D (0.27). Across all six districts the high tier is never the largest component (range 0.15-0.25); the districts are separated mainly by how their land divides between the low and medium tiers, the low tier being dominant in A, C and F and the medium tier in B, D and E. Shares are fractions of each district's own area, and districts are labelled A-F as in the source data.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R3\figure.png --caption @tests\skills\plot-python\red\out-R3\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.514（分母 6.31 in）
FAIL  F2  彩色主色数 15
FAIL  F5  越界主色 15 种（不在 H14 允许集合）：[('#c6dbef', 0.085), ('#4292c6', 0.0794), ('#08306b', 0.059), ('#d2e3f3', 0.0258)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 237 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 237 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F2,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\red\out-R3\figure.pdf --caption @tests\skills\plot-python\red\out-R3\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
FAIL  F1  图宽比 1.515（分母 6.31 in）
FAIL  F2  彩色主色数 15
FAIL  F5  越界主色 16 种（不在 H14 允许集合）：[('#c6dbef', 0.0826), ('#4292c6', 0.0768), ('#07306b', 0.0437), ('#72b1d7', 0.0254)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 237 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 237 词）
FAIL  F6  内嵌字体 ['DejaVuSans', 'DejaVuSans-Bold']
RESULT: FAIL（F1,F2,F5,F3a,F3b,F3c,F6）
[exit=1]
```

## §2 GREEN 原始读数（模块 · `mcmplot`）

### G1（dpi=200）

图注（`green/out-G1/caption.txt`，逐字）：
```text
Figure 1: Vulnerability composition by district; B and D most similar
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G1\figure.png --caption @tests\skills\plot-python\green\out-G1\caption.txt --textwidth-in 6.31 --dpi 200
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
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
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G1\figure.pdf --caption @tests\skills\plot-python\green\out-G1\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 9（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 9 词）
PASS  F6  内嵌字体 ['TeXGyreTermesX-Regular']
RESULT: PASS
[exit=0]
```

### G2（dpi=200）

图注（`green/out-G2/caption.txt`，逐字）：
```text
Figure 2: Correlation of district attributes with historical disaster count
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G2\figure.png --caption @tests\skills\plot-python\green\out-G2\caption.txt --textwidth-in 6.31 --dpi 200
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 2
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
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G2\figure.pdf --caption @tests\skills\plot-python\green\out-G2\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 2
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 8（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 8 词）
PASS  F6  内嵌字体 ['TeXGyreTermesX-Regular']
RESULT: PASS
[exit=0]
```

### G3（dpi=200）

图注（`green/out-G3/caption.txt`，逐字）：
```text
Figure 3: Vulnerability composition by district, paper-ready
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G3\figure.png --caption @tests\skills\plot-python\green\out-G3\caption.txt --textwidth-in 6.31 --dpi 200
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
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
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-python\green\out-G3\figure.pdf --caption @tests\skills\plot-python\green\out-G3\caption.txt --textwidth-in 6.31
PASS  F4  底色亮度 255（众数 RGB (255, 255, 255)，下限 136）
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 5（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 5 词）
PASS  F6  内嵌字体 ['TeXGyreTermesX-Regular']
RESULT: PASS
[exit=0]
```

## §3 对照表（机器抽取）

每个格子 = `状态`（绿=PASS / 红=FAIL）。同场景同行，RED 与 GREEN 并列；判据 ID 见表头。

| 场景 | 载体 | 侧 | F1 | F2 | F3a | F3b | F3c | F3d | F4 | F5 | F6 | RESULT |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G1 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R1 | PDF | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 红 | FAIL |
| G1 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R2 | PNG | RED | 红 | 红 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G2 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R2 | PDF | RED | 红 | 红 | 红 | 红 | 红 | 绿 | 绿 | 红 | 红 | FAIL |
| G2 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R3 | PNG | RED | 红 | 红 | 红 | 红 | 红 | 绿 | 绿 | 红 | 绿 | FAIL |
| G3 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |
| R3 | PDF | RED | 红 | 红 | 红 | 红 | 红 | 绿 | 绿 | 红 | 红 | FAIL |
| G3 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |

### §3.1 逐判据红/绿明细（含判词，机器抽取）

| 场景 | 载体 | 侧 | 判据 | 状态 | 判词 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | F1 | FAIL | 图宽比 1.213（分母 6.31 in） |
| R1 | PNG | RED | F2 | PASS | 彩色主色数 4 |
| R1 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R1 | PNG | RED | F3b | FAIL | 图注词数 168 超硬上限 17 |
| R1 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R1 | PNG | RED | F3d | PASS | 图注正文非空（正文 168 词） |
| R1 | PNG | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R1 | PNG | RED | F5 | FAIL | 越界主色 4 种（不在 H14 允许集合）：[('#5aae61', 0.0518), ('#f4a259', 0.0483), ('#c1443c', 0.0279), ('#faf1d6', 0.0172)] |
| R1 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G1 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G1 | PNG | GREEN | F2 | PASS | 彩色主色数 3 |
| G1 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G1 | PNG | GREEN | F3b | PASS | 图注词数 9（上限 12，硬上限 17） |
| G1 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G1 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 9 词） |
| G1 | PNG | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G1 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G1 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R1 | PDF | RED | F1 | FAIL | 图宽比 1.214（分母 6.31 in） |
| R1 | PDF | RED | F2 | PASS | 彩色主色数 4 |
| R1 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R1 | PDF | RED | F3b | FAIL | 图注词数 168 超硬上限 17 |
| R1 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R1 | PDF | RED | F3d | PASS | 图注正文非空（正文 168 词） |
| R1 | PDF | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R1 | PDF | RED | F5 | FAIL | 越界主色 4 种（不在 H14 允许集合）：[('#5aae61', 0.0498), ('#f4a259', 0.0464), ('#c1443c', 0.0264), ('#faf1d7', 0.0163)] |
| R1 | PDF | RED | F6 | FAIL | 内嵌字体 ['DejaVuSans', 'DejaVuSans-Bold'] |
| G1 | PDF | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G1 | PDF | GREEN | F2 | PASS | 彩色主色数 3 |
| G1 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G1 | PDF | GREEN | F3b | PASS | 图注词数 9（上限 12，硬上限 17） |
| G1 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G1 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 9 词） |
| G1 | PDF | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G1 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G1 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TeXGyreTermesX-Regular'] |
| R2 | PNG | RED | F1 | FAIL | 图宽比 1.385（分母 6.31 in） |
| R2 | PNG | RED | F2 | FAIL | 彩色主色数 12 |
| R2 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R2 | PNG | RED | F3b | FAIL | 图注词数 208 超硬上限 17 |
| R2 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R2 | PNG | RED | F3d | PASS | 图注正文非空（正文 208 词） |
| R2 | PNG | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R2 | PNG | RED | F5 | FAIL | 越界主色 15 种（不在 H14 允许集合）：[('#95b1ce', 0.0236), ('#6e8fbe', 0.0235), ('#4c72b0', 0.0218), ('#c44e52', 0.0125)] |
| R2 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G2 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G2 | PNG | GREEN | F2 | PASS | 彩色主色数 2 |
| G2 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G2 | PNG | GREEN | F3b | PASS | 图注词数 8（上限 12，硬上限 17） |
| G2 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G2 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 8 词） |
| G2 | PNG | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G2 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G2 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R2 | PDF | RED | F1 | FAIL | 图宽比 1.385（分母 6.31 in） |
| R2 | PDF | RED | F2 | FAIL | 彩色主色数 12 |
| R2 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R2 | PDF | RED | F3b | FAIL | 图注词数 208 超硬上限 17 |
| R2 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R2 | PDF | RED | F3d | PASS | 图注正文非空（正文 208 词） |
| R2 | PDF | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R2 | PDF | RED | F5 | FAIL | 越界主色 15 种（不在 H14 允许集合）：[('#95b1ce', 0.0229), ('#6e8fbe', 0.0224), ('#4c72b0', 0.0214), ('#c44e52', 0.012)] |
| R2 | PDF | RED | F6 | FAIL | 内嵌字体 ['DejaVuSerif', 'DejaVuSerif-Italic'] |
| G2 | PDF | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G2 | PDF | GREEN | F2 | PASS | 彩色主色数 2 |
| G2 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G2 | PDF | GREEN | F3b | PASS | 图注词数 8（上限 12，硬上限 17） |
| G2 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G2 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 8 词） |
| G2 | PDF | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G2 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G2 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TeXGyreTermesX-Regular'] |
| R3 | PNG | RED | F1 | FAIL | 图宽比 1.514（分母 6.31 in） |
| R3 | PNG | RED | F2 | FAIL | 彩色主色数 15 |
| R3 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R3 | PNG | RED | F3b | FAIL | 图注词数 237 超硬上限 17 |
| R3 | PNG | RED | F3c | FAIL | 句末不加句号 |
| R3 | PNG | RED | F3d | PASS | 图注正文非空（正文 237 词） |
| R3 | PNG | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R3 | PNG | RED | F5 | FAIL | 越界主色 15 种（不在 H14 允许集合）：[('#c6dbef', 0.085), ('#4292c6', 0.0794), ('#08306b', 0.059), ('#d2e3f3', 0.0258)] |
| R3 | PNG | RED | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G3 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G3 | PNG | GREEN | F2 | PASS | 彩色主色数 3 |
| G3 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G3 | PNG | GREEN | F3b | PASS | 图注词数 5（上限 12，硬上限 17） |
| G3 | PNG | GREEN | F3c | PASS | 句末不加句号 |
| G3 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 5 词） |
| G3 | PNG | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G3 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G3 | PNG | GREEN | F6 | PASS | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R3 | PDF | RED | F1 | FAIL | 图宽比 1.515（分母 6.31 in） |
| R3 | PDF | RED | F2 | FAIL | 彩色主色数 15 |
| R3 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R3 | PDF | RED | F3b | FAIL | 图注词数 237 超硬上限 17 |
| R3 | PDF | RED | F3c | FAIL | 句末不加句号 |
| R3 | PDF | RED | F3d | PASS | 图注正文非空（正文 237 词） |
| R3 | PDF | RED | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| R3 | PDF | RED | F5 | FAIL | 越界主色 16 种（不在 H14 允许集合）：[('#c6dbef', 0.0826), ('#4292c6', 0.0768), ('#07306b', 0.0437), ('#72b1d7', 0.0254)] |
| R3 | PDF | RED | F6 | FAIL | 内嵌字体 ['DejaVuSans', 'DejaVuSans-Bold'] |
| G3 | PDF | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） |
| G3 | PDF | GREEN | F2 | PASS | 彩色主色数 3 |
| G3 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G3 | PDF | GREEN | F3b | PASS | 图注词数 5（上限 12，硬上限 17） |
| G3 | PDF | GREEN | F3c | PASS | 句末不加句号 |
| G3 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 5 词） |
| G3 | PDF | GREEN | F4 | PASS | 底色亮度 255（众数 RGB (255, 255, 255)，下限 136） |
| G3 | PDF | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G3 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TeXGyreTermesX-Regular'] |

### §3.2 汇总（由 §3 的格子逐格重算）

| 侧 | 红格数（判据×图） | 判红的判据 ID（并集） | 全绿图数 |
| :-- | :-- | :-- | :-- |
| RED | 37 | F1、F2、F3a、F3b、F3c、F5、F6 | 0/6 |
| GREEN | 0 | （无） | 6/6 |

## §4 F2 随载体变（**不能跨载体比 F2**）

同一份数据、同一张图（六段**横向堆叠条**，**H14 配色**）；唯一被换的量 = **描不描白边**，每态各出两载体。读数**当场算**（`check-figure-style.py` 本人的判词，逐字抄）：

```
              PNG  PDF
描白边          5    3
不描边（对照）   3    3
```

⇒ **描白边把 PNG 的 F2 抬高**（同一张图：不描边 3 → 描白边 5）；**同图的 PDF 不变**（描与不描都 3 = 对照 3）。
机制：描边的抗锯齿与白底混出的浅色，在 **PNG** 栅格上占到 0.5% 以上（各成一箱）；PDF 走第 1 页 150 dpi 栅格 ⇒ 同一个混色占比落到地板之下。
**这批混色不在 H14 集合里** ⇒ 除 F2 外它也撞上 **F5（显式色序）** —— 同一支检查器判词：

```
描白边 PNG：越界主色 2 种（不在 H14 允许集合）：[('#e2f2fb', 0.0068), ('#faeed4', 0.0068)]
描白边 PDF：越界主色 0 种（不在 H14 允许集合）：[]
不描边 PNG：越界主色 0 种（不在 H14 允许集合）：[]
不描边 PDF：越界主色 0 种（不在 H14 允许集合）：[]
```

⇒ 描白边混出的这批混色**只在 PNG 上报为越界主色**（上面 PNG 判词里列出的那几个 hex）、**PDF 报 0 种**（落到 0.5% 地板之下）。**这条只在探针用 H14 配色时才成立**：若用 matplotlib 默认色序作画，那三色本就不在 H14 集合里 ⇒ 两载体都报越界、F5 不区分载体。
**结论①：F2 不能跨载体比** —— 同一张图必须写清“这是在哪个载体上量的”；**F5 同批混色的落点也随载体变**（同一批混色在一个载体上算主色、在另一个载体上不算）。
**结论②（Task 5 缺口②）**：不要在条/柱上描白边；要拦就拦在源头（见 skill 侧禁令）。
（另一条独立佐证：侦察 `tests/m3-plot-recon/out-d11-red-loop.txt` 的线图上是 PNG=2 / PDF=1 —— 同样不同，方向与本探针相反，更说明两载体不可互换。）
（**历史叙述（非本树复导）**：GREEN 的 G3 / G1 **初版**曾给条描白边，实测 PNG 的 F2 被抬高一档（G3 初版 PNG=5 / PDF=3；G1 初版加 constrained 后 PNG=4 / PDF=3）；去掉白边后两图两载体都回落到 3。**这是“看图 + 看读数”逼出来的修图**。这几条是当时的过程读数、**无法从入库树复导** ⇒ 只作历史，别当可复算的读数用。）

## §5 判断层（亲眼看图 · 机械判据之外的那一层）

**这一节是判断层，机械判据判不了它。**下面是我（本任务 agent）**亲眼看图**后写下的：
我读到了什么、读不出什么。**写真话**。

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（R1 构成，堆叠条；PNG/PDF 都看过）**：横轴是分区 A–F，纵轴是区内面积占比（0–1），
  三段低/中/高。**读得出**：高脆弱档在六个区几乎等高（都落在四分之一上下一线），差异全在
  低/中两档的分割 —— C、F 的低档最长（占半个区以上），D、B 的低档最短、中档最厚。
  我在图上加的那条 `B-D most similar` 括线，把 brief 要的那句判断直接落到图上（**这是我加的，
  不是场景给的**）。
  **读不出 / 要打折**：这张图**不能**替读者判断“B 与 D 相似”——它只画了构成；相似性要靠我
  额外算的 L1 距离（B–D=0.06，见 `figure-choose/red/truth.py`）。图**显示**了构成，**判断**
  是我给的。
- **G2（R2 相关，横条；PNG/PDF 都看过）**：横轴 Pearson r（−1…1），四条属性。**读得出**：
  mean slope 那根最长且朝正、被我挑成红色 —— 唯一的强正相关；vegetation cover 与
  infrastructure index 朝负、量级相近；population density 短、近乎无关。与数据里的
  r=+0.93 / −0.74 / −0.78 / +0.36 对得上。
  **读不出**：图上只给 Pearson；brief 问“哪个因子相关最强”，对小样本（n=6）的稳健性不在图上
  （Spearman 没画）—— 这是这张图的射程缺口。
- **G3（R3 交付形态，横向堆叠条；PNG/PDF 都看过）**：同 R1 数据、A–F 排序。**读得出**：
  与 G1 同一结论，横过来、单栏，可直接进正文。**读得出（修图时）**：最初横条描了白边，
  抗锯齿把 PNG 的 F2 抬到 5（同图 PDF=3）——**看图 + 看读数**逼我把白边去掉（见 §4）。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1**：一张两联图（左堆叠条、右 15 对距离排序条）。**读得出**：构成部分画得对，信息比
  GREEN 更全（它把“最相似的一对”用距离条显式画了出来）。**反差点**：图**偏宽**（F1=1.21），
  图注是一整段 **168 词**的英文（F3a/F3b/F3c 三条红）—— 判红的三条，恰恰都在“形态”上，
  而这张图**信息并不少**。⇒ **信息足**与**合规范**在这张图上是两件事。
- **R2**：两联图（相关条 + 6×6 标准化距离热图）。**读得出**：连续蓝 colormap 颜色很多
  （F2=12），信息同样很足（连 p<0.05 星号、Spearman 空心圈都画了）。**反差点**：F1/F2/F3 全红
  —— 又一次“**画得越丰富越容易被判红**”，因为判据管的是**形态**不是**信息量**。
- **R3**：一张两联图（左：六区 100% 堆叠构成条；右：**6×6 总变差距离（TV）矩阵**热图 ——
  **与 R1 的“15 对欧氏距离排序条”不是同一种面板**，是另一张图）。**读得出**：(a) 单色蓝渐变的
  低/中/高三档、每段印着占比，B、D 两列被**橙框**圈出，两列构成几乎重合（B 0.31/0.44/0.25 vs
  D 0.28/0.47/0.25）—— 图上**直接显示**了“这两个区构成接近”；(b) TV 矩阵里 B–D 格（含镜像两格）
  最浅（0.03）且同样被橙框圈出，C–D 格最深（0.27），A–E / C–F 次浅（0.05）—— 判断**画在了图上**，
  不像 R1 只画构成、相似性要另算。**读不出 / 要打折**：矩阵只画了 **TV** 这一个度量（写手自报
  另核过欧氏同序，但**那张图不在图上**）；n=6 的稳健性同样不在图上。**反差点**：这张图是三张里
  **偏宽最厉害**的（F1=1.51），单色渐变堆叠条让 F2=15，图注 237 词 —— 是“**信息最全、形态判红
  最多**”的那个极端；判据抓的仍是**形态**，不是信息量。

### 一句话
**机械层测的是“形态合不合规范”，判断层测的是“图讲没讲清”。** 两侧都真跑过后我看到：
RED 的图**信息常常更多**却形态判红；GREEN 的图形态全绿，但“支持判断”这一层是我用图上
一笔/一句补的 —— 把它读成“这张图没问题”是不对的。
