# Task 3 · RED × GREEN 对照证据（`mcm-plot-origin`）

本文件由 `tests/skills/plot-origin/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
**§1 / §2 / §3 / §4 是机器抽取**（判词行逐格解析成 `(状态, 判据 ID, 详情)`，不是手抄）；**§5 是手写的判断层**（文里已标明）。

## §0 口径（两侧同源同数）

- **场景**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，未改写）。
  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景，**同数据逐字**（G1/G3 = brief-R1/R3 的
  低/中/高三档；G2 = brief-R2 的五属性表；RED 侧脚本里硬编码的同一批数）。
- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。
- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。
  工作树 blob `0a4bb765a825` · `HEAD:` blob `0a4bb765a825` ⇒ **相同**
- **同数**：每侧 3 场景 × 2 载体（PNG/PDF）= **6 张图**，两侧共 12 张；判据 9 条 × 12 张。
- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行；
  **PDF 不给 `--dpi`**（走页盒）。
- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；
  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。
  RED **不 import `mcmplot_origin`、不用 helper**。
- **GREEN 侧**：由 Task 2 用本模块（`mcmplot_origin` 的 `apply_style/figsize_for/save`）产出、
  已过独立复核（`Approved`）；**图注是判断层动作**，不是场景给的。
- ★ **不许跨载体比 `F2`**：见 §4（器械口径：两载体走两条栅格化路径 ⇒ 读数不是同一个量）。
- ★ **PDF 侧 `F5` 红 = 载体限制**：Origin 的 PDF 写入器把填色量化到**两位小数** ⇒ 1 LSB 偏移 ⇒
  `F5`（容差 0）判红，**不是「颜色不对」**。每处 PDF 侧 `F5` 红都带一行注（指向 §H.2 `M3-origin-T2a`）。
- ★ **`F6` 三态**（`PASS`/`FAIL`/`N/A`）：**落哪一态依产物而定**，逐格印真实判词；`N/A` 当独立
  第三态（见 §3.3）—— **既不当 `PASS`（假绿）、也不当硬门（假红）、也不丢格**。

## §1 RED 原始读数（朴素写手 · 无规范）

### R1（dpi=112）

图注（`red/out-R1/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six districts. Each column is one district, split into the share of that district's land area falling in the low, medium and high vulnerability tiers. The three shares of every district sum to 100%, so each column is a complete whole and the columns are directly comparable segment by segment. Districts are ordered by their low-vulnerability share, from highest (C, left) to lowest (D, right), which places districts of similar composition next to each other. Two patterns are visible. First, the high tier varies very little across the region: every district has 15-25% of its area in the high tier, so the districts differ almost entirely in how the remaining area splits between the low and medium tiers. Second, the region divides into two groups of three: in C, F and A the largest component is the low tier (55%, 50% and 42%), whereas in E, B and D the largest component is the medium tier (38%, 44% and 47%), with the low share falling steadily from left to right across the figure. Districts B (31/44/25) and D (28/47/25) have the most similar structure: their tier shares differ by at most 3 percentage points, and by 6 percentage points in total, the smallest discrepancy of any pair; they are therefore drawn as adjacent near-identical columns at the right-hand end of the figure.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R1\figure.png --caption @tests\skills\plot-origin\red\out-R1\caption.txt --textwidth-in 6.31 --dpi 112
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 54.35%）；下限 136
FAIL  F1  图宽比 1.698（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#c6dbef', 0.1777), ('#6baed6', 0.1662), ('#2171b5', 0.0913)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 228 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 228 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R1\figure.pdf --caption @tests\skills\plot-origin\red\out-R1\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 54.27%）；下限 136
FAIL  F1  图宽比 1.699（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#c6dbef', 0.1766), ('#6badd6', 0.1651), ('#2170b5', 0.0903)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 228 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 228 词）
PASS  F6  N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此）
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

### R2（dpi=196）

图注（`red/out-R2/caption.txt`，逐字）：
```text
Figure 1. Drivers of the historical disaster count across the six study districts. (a) Mean slope against the historical disaster count; each point is one district (A-F) and the solid line is the ordinary least-squares fit (r = 0.93, n = 6). (b) Pearson correlation of each candidate attribute with the historical disaster count, ranked by absolute value: mean slope (r = +0.93), the infrastructure index (r = -0.78), vegetation cover (r = -0.74), population density (r = +0.36). Mean slope is by far the strongest driver; the infrastructure index and vegetation cover are moderately negative and population density is weak. The district letters in (a) also show how the districts group: A and C (gentle slopes, dense vegetation, few disasters) resemble each other, as do B and D (steep slopes, sparse vegetation, many disasters), while E and F lie between the two pairs.
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R2\figure.png --caption @tests\skills\plot-origin\red\out-R2\caption.txt --textwidth-in 6.31 --dpi 196
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.42%）；下限 136
FAIL  F1  图宽比 1.698（分母 6.31 in）
PASS  F2  彩色主色数 2
FAIL  F5  越界主色 2 种（不在 H14 允许集合）：[('#c1663d', 0.0346), ('#2e5c8a', 0.0291)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 144 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 144 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F1,F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R2\figure.pdf --caption @tests\skills\plot-origin\red\out-R2\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 90.61%）；下限 136
FAIL  F1  图宽比 1.699（分母 6.31 in）
PASS  F2  彩色主色数 2
FAIL  F5  越界主色 2 种（不在 H14 允许集合）：[('#c1663d', 0.0333), ('#2d5b89', 0.0285)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 144 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 144 词）
FAIL  F6  内嵌字体 ['MicrosoftJhengHeiUIRegular']；另有只被引用、未内嵌的 ['MicrosoftJhengHeiLight', 'MicrosoftJhengHeiUIRegular', 'SimSun']（未内嵌 ⇒ 不参与判族）
RESULT: FAIL（F1,F5,F3a,F3b,F3c,F6）
[exit=1]
```

### R3（dpi=300）

图注（`red/out-R3/caption.txt`，逐字）：
```text
Figure 1. Vulnerability composition of the six districts. The 100% stacked columns give, for each district, the share of its land area falling in each of the three vulnerability tiers (low, medium, high); the three shares sum to 1.00 within every district, and the districts are shown in the order of Table 1. The districts differ mainly in the low and medium tiers: low-vulnerability land is the largest component in C (0.55) and F (0.50), while the medium tier dominates in D (0.47), B (0.44) and E (0.38). The high tier is the smallest component everywhere and varies little across districts (0.15-0.25), so it does not separate them. The two districts with the most similar structure are B and D: their tier shares differ by at most 0.03 (low 0.31 vs 0.28, medium 0.44 vs 0.47, high 0.25 vs 0.25), a total absolute difference of only 0.06 - smaller than for any other pair (the next closest pairs, A-E and C-F, differ by 0.10).
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R3\figure.png --caption @tests\skills\plot-origin\red\out-R3\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 60.67%）；下限 136
PASS  F1  图宽比 1.030（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#fee8c8', 0.1484), ('#fdbb84', 0.1388), ('#e34a33', 0.0798)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 164 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 164 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: FAIL（F5,F3a,F3b,F3c）
[exit=1]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\red\out-R3\figure.pdf --caption @tests\skills\plot-origin\red\out-R3\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 59.82%）；下限 136
PASS  F1  图宽比 1.030（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#ffe8c6', 0.1449), ('#fcba84', 0.1359), ('#e24933', 0.0775)]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 164 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 164 词）
PASS  F6  N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此）
RESULT: FAIL（F5,F3a,F3b,F3c）
[exit=1]
```

## §2 GREEN 原始读数（模块 · `mcmplot_origin`）

### G1（dpi=300）

图注（`green/out-G1/caption.txt`，逐字）：
```text
Figure 1: Stacked vulnerability composition across six districts
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G1\figure.png --caption @tests\skills\plot-origin\green\out-G1\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.86%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 6（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 6 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G1\figure.pdf --caption @tests\skills\plot-origin\green\out-G1\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.10%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#e59e00', 0.1582), ('#56b5e8', 0.1475), ('#009e72', 0.0844)]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 6（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 6 词）
PASS  F6  N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此）
RESULT: FAIL（F5）
[exit=1]
```

### G2（dpi=300）

图注（`green/out-G2/caption.txt`，逐字）：
```text
Figure 2: Attribute correlations with historical disaster count
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G2\figure.png --caption @tests\skills\plot-origin\green\out-G2\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 85.74%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 1
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 6（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 6 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G2\figure.pdf --caption @tests\skills\plot-origin\green\out-G2\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 99.84%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 84.87%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 1
FAIL  F5  越界主色 1 种（不在 H14 允许集合）：[('#e59e00', 0.1055)]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 6（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 6 词）
PASS  F6  内嵌字体 ['TimesNewRomanPSMT']；另有只被引用、未内嵌的 ['TimesNewRomanPSMT']（未内嵌 ⇒ 不参与判族）
RESULT: FAIL（F5）
[exit=1]
```

### G3（dpi=300）

图注（`green/out-G3/caption.txt`，逐字）：
```text
Figure 3: District vulnerability composition, low to high tiers
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G3\figure.png --caption @tests\skills\plot-origin\green\out-G3\caption.txt --textwidth-in 6.31 --dpi 300
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.17%）；下限 136
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 7（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 7 词）
PASS  F6  PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）
RESULT: PASS
[exit=0]
```

```
$ python tests\skills\figure-choose\check-figure-style.py --fig tests\skills\plot-origin\green\out-G3\figure.pdf --caption @tests\skills\plot-origin\green\out-G3\caption.txt --textwidth-in 6.31
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 53.70%）；下限 136
PASS  F1  图宽比 1.001（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F5  越界主色 3 种（不在 H14 允许集合）：[('#e59e00', 0.1546), ('#56b5e8', 0.1447), ('#009e72', 0.0831)]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 7（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 7 词）
PASS  F6  N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此）
RESULT: FAIL（F5）
[exit=1]
```

## §3 对照表（机器抽取）

每个格子 = `状态`：绿 = `PASS` / 红 = `FAIL` / **`N/A`**（`F6` 的独立第三态，仅见 F6 列）。
同场景同行，RED 与 GREEN 并列；判据 ID 见表头。

| 场景 | 载体 | 侧 | F1 | F2 | F3a | F3b | F3c | F3d | F4 | F5 | F6 | RESULT |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | N/A | FAIL |
| G1 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | N/A | PASS |
| R1 | PDF | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | N/A | FAIL |
| G1 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 红 | N/A | FAIL |
| R2 | PNG | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | N/A | FAIL |
| G2 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | N/A | PASS |
| R2 | PDF | RED | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | 红 | FAIL |
| G2 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 红 | 绿 | FAIL |
| R3 | PNG | RED | 绿 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | N/A | FAIL |
| G3 | PNG | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | N/A | PASS |
| R3 | PDF | RED | 绿 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 红 | N/A | FAIL |
| G3 | PDF | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 红 | N/A | FAIL |

### §3.1 逐判据明细（含判词 + 载体限制注，机器抽取）

| 场景 | 载体 | 侧 | 判据 | 状态 | 判词 | 注 |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | F1 | FAIL | 图宽比 1.698（分母 6.31 in） | — |
| R1 | PNG | RED | F2 | PASS | 彩色主色数 3 | — |
| R1 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R1 | PNG | RED | F3b | FAIL | 图注词数 228 超硬上限 17 | — |
| R1 | PNG | RED | F3c | FAIL | 句末不加句号 | — |
| R1 | PNG | RED | F3d | PASS | 图注正文非空（正文 228 词） | — |
| R1 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 54.35%）；下限 136 | — |
| R1 | PNG | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#c6dbef', 0.1777), ('#6baed6', 0.1662), ('#2171b5', 0.0913)] | — |
| R1 | PNG | RED | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| G1 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） | — |
| G1 | PNG | GREEN | F2 | PASS | 彩色主色数 3 | — |
| G1 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G1 | PNG | GREEN | F3b | PASS | 图注词数 6（上限 12，硬上限 17） | — |
| G1 | PNG | GREEN | F3c | PASS | 句末不加句号 | — |
| G1 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 6 词） | — |
| G1 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.86%）；下限 136 | — |
| G1 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] | — |
| G1 | PNG | GREEN | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| R1 | PDF | RED | F1 | FAIL | 图宽比 1.699（分母 6.31 in） | — |
| R1 | PDF | RED | F2 | PASS | 彩色主色数 3 | — |
| R1 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R1 | PDF | RED | F3b | FAIL | 图注词数 228 超硬上限 17 | — |
| R1 | PDF | RED | F3c | FAIL | 句末不加句号 | — |
| R1 | PDF | RED | F3d | PASS | 图注正文非空（正文 228 词） | — |
| R1 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 54.27%）；下限 136 | — |
| R1 | PDF | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#c6dbef', 0.1766), ('#6badd6', 0.1651), ('#2170b5', 0.0903)] | ★〔本红是**实红**：色不在 `H14`，两载体皆红〕PDF 侧的 hex 另比 PNG 侧偏 ≤ 1 LSB，同源于 Origin PDF 写入器的两位小数量化（见 §H.2 `M3-origin-T2a`）；但**判红的原因是配色本身**，与该量化无关。 |
| R1 | PDF | RED | F6 | N/A | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） | — |
| G1 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） | — |
| G1 | PDF | GREEN | F2 | PASS | 彩色主色数 3 | — |
| G1 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G1 | PDF | GREEN | F3b | PASS | 图注词数 6（上限 12，硬上限 17） | — |
| G1 | PDF | GREEN | F3c | PASS | 句末不加句号 | — |
| G1 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 6 词） | — |
| G1 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.10%）；下限 136 | — |
| G1 | PDF | GREEN | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#e59e00', 0.1582), ('#56b5e8', 0.1475), ('#009e72', 0.0844)] | ★〔载体限制 ⇒ **本红是假红**〕同图 **PNG 侧 `F5` 绿、红只出现在 PDF**。机制当场量过：Origin 的 PDF 内容流把填色写成**两位小数**（本支 GREEN 实测 `0.9 0.62 0`，而 `#E69F00` 的满精度是 `0.9019607843 0.6235294118`）⇒ 栅格化后每通道差 1 LSB（`#E69F00` → `#E59E00`）⇒ `F5`（容差 0 的精确命中）判红。**这不是「Origin 画的图颜色不对」** —— 同场景的 python/matlab 的 PDF 走满精度、`F5` 绿（本脚本另跑核对过）。登记 `docs/mcm-suite-todo.md` §H.2 `M3-origin-T2a`。 |
| G1 | PDF | GREEN | F6 | N/A | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） | — |
| R2 | PNG | RED | F1 | FAIL | 图宽比 1.698（分母 6.31 in） | — |
| R2 | PNG | RED | F2 | PASS | 彩色主色数 2 | — |
| R2 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R2 | PNG | RED | F3b | FAIL | 图注词数 144 超硬上限 17 | — |
| R2 | PNG | RED | F3c | FAIL | 句末不加句号 | — |
| R2 | PNG | RED | F3d | PASS | 图注正文非空（正文 144 词） | — |
| R2 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.42%）；下限 136 | — |
| R2 | PNG | RED | F5 | FAIL | 越界主色 2 种（不在 H14 允许集合）：[('#c1663d', 0.0346), ('#2e5c8a', 0.0291)] | — |
| R2 | PNG | RED | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| G2 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） | — |
| G2 | PNG | GREEN | F2 | PASS | 彩色主色数 1 | — |
| G2 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G2 | PNG | GREEN | F3b | PASS | 图注词数 6（上限 12，硬上限 17） | — |
| G2 | PNG | GREEN | F3c | PASS | 句末不加句号 | — |
| G2 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 6 词） | — |
| G2 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 85.74%）；下限 136 | — |
| G2 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] | — |
| G2 | PNG | GREEN | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| R2 | PDF | RED | F1 | FAIL | 图宽比 1.699（分母 6.31 in） | — |
| R2 | PDF | RED | F2 | PASS | 彩色主色数 2 | — |
| R2 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R2 | PDF | RED | F3b | FAIL | 图注词数 144 超硬上限 17 | — |
| R2 | PDF | RED | F3c | FAIL | 句末不加句号 | — |
| R2 | PDF | RED | F3d | PASS | 图注正文非空（正文 144 词） | — |
| R2 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 90.61%）；下限 136 | — |
| R2 | PDF | RED | F5 | FAIL | 越界主色 2 种（不在 H14 允许集合）：[('#c1663d', 0.0333), ('#2d5b89', 0.0285)] | ★〔本红是**实红**：色不在 `H14`，两载体皆红〕PDF 侧的 hex 另比 PNG 侧偏 ≤ 1 LSB，同源于 Origin PDF 写入器的两位小数量化（见 §H.2 `M3-origin-T2a`）；但**判红的原因是配色本身**，与该量化无关。 |
| R2 | PDF | RED | F6 | FAIL | 内嵌字体 ['MicrosoftJhengHeiUIRegular']；另有只被引用、未内嵌的 ['MicrosoftJhengHeiLight', 'MicrosoftJhengHeiUIRegular', 'SimSun']（未内嵌 ⇒ 不参与判族） | — |
| G2 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） | — |
| G2 | PDF | GREEN | F2 | PASS | 彩色主色数 1 | — |
| G2 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G2 | PDF | GREEN | F3b | PASS | 图注词数 6（上限 12，硬上限 17） | — |
| G2 | PDF | GREEN | F3c | PASS | 句末不加句号 | — |
| G2 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 6 词） | — |
| G2 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 99.84%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 84.87%）；下限 136 | — |
| G2 | PDF | GREEN | F5 | FAIL | 越界主色 1 种（不在 H14 允许集合）：[('#e59e00', 0.1055)] | ★〔载体限制 ⇒ **本红是假红**〕同图 **PNG 侧 `F5` 绿、红只出现在 PDF**。机制当场量过：Origin 的 PDF 内容流把填色写成**两位小数**（本支 GREEN 实测 `0.9 0.62 0`，而 `#E69F00` 的满精度是 `0.9019607843 0.6235294118`）⇒ 栅格化后每通道差 1 LSB（`#E69F00` → `#E59E00`）⇒ `F5`（容差 0 的精确命中）判红。**这不是「Origin 画的图颜色不对」** —— 同场景的 python/matlab 的 PDF 走满精度、`F5` 绿（本脚本另跑核对过）。登记 `docs/mcm-suite-todo.md` §H.2 `M3-origin-T2a`。 |
| G2 | PDF | GREEN | F6 | PASS | 内嵌字体 ['TimesNewRomanPSMT']；另有只被引用、未内嵌的 ['TimesNewRomanPSMT']（未内嵌 ⇒ 不参与判族） | — |
| R3 | PNG | RED | F1 | PASS | 图宽比 1.030（分母 6.31 in） | — |
| R3 | PNG | RED | F2 | PASS | 彩色主色数 3 | — |
| R3 | PNG | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R3 | PNG | RED | F3b | FAIL | 图注词数 164 超硬上限 17 | — |
| R3 | PNG | RED | F3c | FAIL | 句末不加句号 | — |
| R3 | PNG | RED | F3d | PASS | 图注正文非空（正文 164 词） | — |
| R3 | PNG | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 60.67%）；下限 136 | — |
| R3 | PNG | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#fee8c8', 0.1484), ('#fdbb84', 0.1388), ('#e34a33', 0.0798)] | — |
| R3 | PNG | RED | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| G3 | PNG | GREEN | F1 | PASS | 图宽比 1.000（分母 6.31 in） | — |
| G3 | PNG | GREEN | F2 | PASS | 彩色主色数 3 | — |
| G3 | PNG | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G3 | PNG | GREEN | F3b | PASS | 图注词数 7（上限 12，硬上限 17） | — |
| G3 | PNG | GREEN | F3c | PASS | 句末不加句号 | — |
| G3 | PNG | GREEN | F3d | PASS | 图注正文非空（正文 7 词） | — |
| G3 | PNG | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 55.17%）；下限 136 | — |
| G3 | PNG | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] | — |
| G3 | PNG | GREEN | F6 | N/A | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） | — |
| R3 | PDF | RED | F1 | PASS | 图宽比 1.030（分母 6.31 in） | — |
| R3 | PDF | RED | F2 | PASS | 彩色主色数 3 | — |
| R3 | PDF | RED | F3a | FAIL | 图注以 `Figure N:` 起 | — |
| R3 | PDF | RED | F3b | FAIL | 图注词数 164 超硬上限 17 | — |
| R3 | PDF | RED | F3c | FAIL | 句末不加句号 | — |
| R3 | PDF | RED | F3d | PASS | 图注正文非空（正文 164 词） | — |
| R3 | PDF | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 59.82%）；下限 136 | — |
| R3 | PDF | RED | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#ffe8c6', 0.1449), ('#fcba84', 0.1359), ('#e24933', 0.0775)] | ★〔本红是**实红**：色不在 `H14`，两载体皆红〕PDF 侧的 hex 另比 PNG 侧偏 ≤ 1 LSB，同源于 Origin PDF 写入器的两位小数量化（见 §H.2 `M3-origin-T2a`）；但**判红的原因是配色本身**，与该量化无关。 |
| R3 | PDF | RED | F6 | N/A | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） | — |
| G3 | PDF | GREEN | F1 | PASS | 图宽比 1.001（分母 6.31 in） | — |
| G3 | PDF | GREEN | F2 | PASS | 彩色主色数 3 | — |
| G3 | PDF | GREEN | F3a | PASS | 图注以 `Figure N:` 起 | — |
| G3 | PDF | GREEN | F3b | PASS | 图注词数 7（上限 12，硬上限 17） | — |
| G3 | PDF | GREEN | F3c | PASS | 句末不加句号 | — |
| G3 | PDF | GREEN | F3d | PASS | 图注正文非空（正文 7 词） | — |
| G3 | PDF | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 53.70%）；下限 136 | — |
| G3 | PDF | GREEN | F5 | FAIL | 越界主色 3 种（不在 H14 允许集合）：[('#e59e00', 0.1546), ('#56b5e8', 0.1447), ('#009e72', 0.0831)] | ★〔载体限制 ⇒ **本红是假红**〕同图 **PNG 侧 `F5` 绿、红只出现在 PDF**。机制当场量过：Origin 的 PDF 内容流把填色写成**两位小数**（本支 GREEN 实测 `0.9 0.62 0`，而 `#E69F00` 的满精度是 `0.9019607843 0.6235294118`）⇒ 栅格化后每通道差 1 LSB（`#E69F00` → `#E59E00`）⇒ `F5`（容差 0 的精确命中）判红。**这不是「Origin 画的图颜色不对」** —— 同场景的 python/matlab 的 PDF 走满精度、`F5` 绿（本脚本另跑核对过）。登记 `docs/mcm-suite-todo.md` §H.2 `M3-origin-T2a`。 |
| G3 | PDF | GREEN | F6 | N/A | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） | — |

**注（§3.1 的「注」列）**：只在 **PDF 侧 `F5` 判红**时给。两条分支 —— 同图 PNG 侧 `F5` 绿 ⇒ **本红是假红**（载体限制）；PNG 侧也红 ⇒ **本红是实红**（配色不在 `H14`），PDF 侧 hex 另偏 ≤1 LSB 同源。**PNG 侧 `F5` 是本支的真判据**，其「注」列恒为 `—`。

### §3.2 汇总（由 §3 的格子逐格重算）

| 侧 | 红格数（判据×图） | 判红的判据 ID（并集） | 无红判据的图数 |
| :-- | :-- | :-- | :-- |
| RED | 29 | F1、F3a、F3b、F3c、F5、F6 | 0/6 |
| GREEN | 3 | F5 | 3/6 |

★ 上表**红格数按检查器布尔判**（`F6` 的 `N/A` 在检查器里是 `PASS`，故不计入红格）—— `F6` 的真实三态另见 §3.3，**不要**把这里的「不红」读成 `F6` 拿了 `PASS`。

### §3.3 `F6` 三态逐格（要求 1：`N/A` 当独立第三态）

`F6` 的**落态依产物而定**（不写死预期）。下表**逐格**印真实 token：`PASS`（内嵌族落在可接受表）· `FAIL`（内嵌族不在表）· **`N/A`**（PDF 未内嵌任何字体 / PNG 载体，本判据不适用）。**`N/A` 既不是 `PASS` 也不是 `FAIL`**，本表把它当**独立第三态**印出。

| 场景 | 载体 | 侧 | F6 态 | 判词（机器抽取） |
| :-- | :-- | :-- | :-- | :-- |
| R1 | PNG | RED | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R1 | PDF | RED | **N/A** | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） |
| R2 | PNG | RED | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R2 | PDF | RED | **FAIL** | 内嵌字体 ['MicrosoftJhengHeiUIRegular']；另有只被引用、未内嵌的 ['MicrosoftJhengHeiLight', 'MicrosoftJhengHeiUIRegular', 'SimSun']（未内嵌 ⇒ 不参与判族） |
| R3 | PNG | RED | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| R3 | PDF | RED | **N/A** | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['SimSun']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） |
| G1 | PNG | GREEN | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G1 | PDF | GREEN | **N/A** | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） |
| G2 | PNG | GREEN | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G2 | PDF | GREEN | **PASS** | 内嵌字体 ['TimesNewRomanPSMT']；另有只被引用、未内嵌的 ['TimesNewRomanPSMT']（未内嵌 ⇒ 不参与判族） |
| G3 | PNG | GREEN | **N/A** | PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿） |
| G3 | PDF | GREEN | **N/A** | N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：['TimesNewRomanPSMT']）⇒ 未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此） |

**三态合计（机器抽取）**：`PASS` 1 格 · `FAIL` 1 格 · `N/A` 10 格（共 12 格 = 12 张图）。

## §4 `F2` 与载体（**不许跨载体比 `F2`**）

**口径**：`F2`（彩色主色数）对 PNG / PDF 的读数**不保证相同** ⇒ 两侧各自读、**不并列比**。**禁止的承重不是「本支某张图会变」**，而是**器械口径**：检查器对两载体走**不同的栅格化路径** —— PNG 直接 `Image.open`（原生像素、按 `--dpi` 定尺），PDF 第 1 页按固定 `RASTER_DPI=150` 栅格化（`raster_rgb()`）⇒ 同一条 `color_count` 吃到的像素来源不同 ⇒ 两个读数**不是同一个量**。

**本支六个场景的 F2 逐载体读数（机器抽取自 §1/§2）** —— ★ **此表只是「同一场景两载体给出同一个数」这个负面结果的登记，不构成跨载体比较**：两根列并排**只为显示它们相同**，**不给「哪个多哪个少」下任何结论**（两个读数不是同一个量，见上）：

| 场景 | 侧 | F2(PNG) | F2(PDF) | 本场景两载体是否相同 |
| :-- | :-- | :-- | :-- | :-- |
| R1 | RED | 3 | 3 | 相同 |
| R2 | RED | 2 | 2 | 相同 |
| R3 | RED | 3 | 3 | 相同 |
| G1 | GREEN | 3 | 3 | 相同 |
| G2 | GREEN | 1 | 1 | 相同 |
| G3 | GREEN | 3 | 3 | 相同 |

⇒ **如实收窄（射程只到这里）**：**本支这六个场景**里，两载体的 `F2` **逐格相同** —— 所以**本支不出具**「某张图 PNG ≠ PDF」的实例。这条规矩因此**不靠本支某个读数**承重，靠上面那条**器械口径**（两载体走两条栅格化路径）。**跨支的先例**另有：`tests/skills/plot-python/red-green-evidence.md` §4 的载体探针（同一张图 PNG=5 / PDF=3）。**不许把本支的「逐格相同」读成「Origin 上 F2 不会随载体变」**。

**另一条载体事实（`F5`，当场量，支撑 §3.3 与要求 2）**：

```
G1 figure.pdf 内容流 sc/rg 填色（去重、前 6 个）：[('0', '0', '0'), ('1', '1', '1'), ('0.9', '0.62', '0'), ('0.34', '0.71', '0.91'), ('0', '0.62', '0.45')]
G2 figure.pdf 内容流 sc/rg 填色（去重、前 6 个）：[('0', '0', '0'), ('1', '1', '1'), ('0.9', '0.62', '0')]
G3 figure.pdf 内容流 sc/rg 填色（去重、前 6 个）：[('0', '0', '0'), ('1', '1', '1'), ('0.9', '0.62', '0'), ('0.34', '0.71', '0.91'), ('0', '0.62', '0.45')]
```

⇒ `#E69F00` 被 Origin 写成 `0.9 0.62 0`（**两位小数**）；栅格化后每通道差 1 LSB ⇒ PDF 侧 `F5` 判红、PNG 侧同图 `F5` 绿。**同场景 python/matlab 的 PDF 走满精度**（python 实测 `0.9019607843 0.6235294118 0`），`F5` 绿 —— 本脚本当场另跑核对过。

## §5 判断层（亲眼看图 · 机械判据之外的那一层）

**这一节是判断层，机械判据判不了它。** 下面是本任务 agent **亲眼看图**（PNG 逐张）后写下的：
读到了什么、读不出什么。**写真话。** 六张 Origin 图（三 RED + 三 GREEN）我都打开逐张看过；
同场景的另两支载体产物也并排比过。**本节是手写的，不是机器抽取。**

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（`tests/skills/plot-origin/green/out-G1/figure.png`，R1 构成，竖 100% 堆叠柱）**：
  **底色白**（判据外缘环 100% 白，目视也是白）；**三色 = `H14` 前三色**（橙 low / 浅蓝 medium /
  绿 high —— 目视与 `F5` 0 越界互证）；**字体是衬线**（Times 系观感，与主题一致）。
  **判据不报、眼睛看得见**：① 段与段之间有一条**黑色细边**（内建 `column` 模板 + group 的统一构造路线
  的产物；`F2`/`F5` 都不报它）；② **图例摆在框外上方**、不压数据（与"调用方纪律"第 1 条一致）；
  ③ 六根柱**很宽很高**、占满大半画布。读得出：六区三档构成、高脆弱档近乎等高、差异在低/中两档。
  **读不出**：图**没有**替读者判断"B 与 D 最像"（python 侧的同场景 G1 多画了一条 `B-D most similar`
  括线，本支没有 —— 这条"支持判断"是图外另算的）。
- **G2（`tests/skills/plot-origin/green/out-G2/figure.png`，R2 相关，横条）**：**底色白**；
  **主色只有 `H14` 首色橙**（单系列单色 ⇒ `F2` 读 1）；衬线字体。**判据不报、眼睛看得见**：
  ① 类目之间有**虚线网格**；② 条有**黑边**；③ 负值条从 0 向左伸、正值向右 —— **符号靠方向**而不是
  颜色（本支只有一色）。读得出：mean slope 最长（≈ +0.93）、vegetation cover 与 infrastructure index
  朝负（≈ −0.74 / −0.78）、population density 短（≈ +0.36），与数据对得上。**读不出**：只画了 Pearson，
  n=6 的稳健性不在图上。
- **G3（`tests/skills/plot-origin/green/out-G3/figure.png`，R3 交付形态，横 100% 堆叠条）**：底色白；
  `H14` 前三色；衬线；段有黑边、类目间虚线、坐标轴全框（同 G1）。读得出：同 R1 数据横过来、单栏
  可直接进正文。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1（`tests/skills/plot-origin/red/out-R1/figure.png`）**：竖 100% 堆叠柱，区序 C,F,A,E,B,D
  （与它图注里"按 low 档占比降序"的口径一致）；三档是 **Blues 单色蓝渐变**（不是 `H14`）。底色白；
  衬线。**判据不报、眼睛看得见（两条）**：
  ① **图例压在绘图区内的数据上** —— 图例框落在右上角，**盖住最后一根柱（D）「high」段的顶部**；
  这就是 `references/workflow.md`「调用方纪律」点名的"图例压数据"，**F1–F6 没有一条会报图例位置**。
  ② **柱与柱之间有一条饱和红细边** —— 像素实测**恰好 `(241,64,64)`、共 3910 px**（≈ 全图 **0.38%**），
  **落在 `F2`/`F5` 的 0.5% 覆盖率阈值之下 ⇒ 检查器全程不报**（正是"边色"那条射程外项）。
  **反差点**：信息并不少（它把区序规则与"最相似的一对"写进图注），红的却是**形态** ——
  `F1` = 1.698 太宽、`F5` 三色越界、图注 228 词且以句号结尾。
- **R2（`tests/skills/plot-origin/red/out-R2/figure.png`）**：两联图（a 散点 + 拟合线，点标 A–F；
  b 四属性 Pearson r 横条，蓝 = 正 / 赭 = 负）。底色白；**衬线观感**。**判据不报、眼睛看得见**：
  b 面板类目名**旋了约 45°**；条无明显细边；图例落在框内右上但**没压到数据**。
  **一处"观感 vs 判词"的落差（如实登记，不下机制断言）**：`F6` 逐字判 **`FAIL`**
  （内嵌族 `MicrosoftJhengHeiUIRegular`，一个**无衬线 CJK 族**），而**屏幕上的拉丁文字看起来是衬线体**
  —— 内嵌的那个子集可能只覆盖了某些字形（如负号），拉丁正文另有来源。**我只登记这条落差，不声称**
  它是"半张图两种字体"那类已知坑（本支没做那个机制验证）。
  **反差点**：`F1` = 1.698、`F5` 两色（赭 / 蓝都不在 `H14`）越界、图注 144 词、`F6` 判红。
- **R3（`tests/skills/plot-origin/red/out-R3/figure.png`）**：竖 100% 堆叠柱、区序 A–F；三档是
  **OrRd 单色橙红渐变**（`#fee8c8`/`#fdbb84`/`#e34a33`，不是 `H14`）。底色白；衬线；
  **图例摆在框外右侧**（没压数据，这点比 R1 好）。**判据不报、眼睛看得见**：段之间同样有**细边**
  （像素里量到 `(241,64,64)` 共 11872 px＝≈ 0.44%，与 R1 同型、同样在阈值之下）—— 检查器不报。
  **反差点**：`F1` = 1.030 **在带内**（三张 RED 里唯一宽度合规的），红的是 `F5`（OrRd 三色越界）与
  `F3a/b/c`（图注 164 词、以句号结尾）。

### 与另两支载体**同场景并排**（GREEN 侧，我看到的跨载体差异）

把本支 `green/out-G1/figure.png` 与同场景的 `tests/skills/plot-python/green/out-G1/figure.png`、
`tests/skills/plot-matlab/green/out-G1/figure.png` 并排看：

- **图高**：本支 ≈ **6.31 × 4.47 in**（宽高比 **1.41**）；另两支 ≈ **2.43**（高 ≈ 2.6 in）。本支明显**更高**
  —— `F1` 只吃**宽**；`assets/mcm-style.json` 的 `h3.height_in` 在 **origin 那格记 `not-landable`**
  （登记见 §H.2 `M3-origin-T2d`）⇒ **不算缺陷**，但**跨载体确实不同**。
- **框线**：本支**四边全框**；另两支**无上/右框线**（开框）。同样是单源表上的载体事实 ——
  `assets/mcm-style.json` 的 `h10.axes_box` 在 **origin 那格记 `not-landable`** ⇒ 同样**不算缺陷**。
- **段边**：本支段间有**黑细边**；python 侧无段边；matlab 侧无段边。
- **图例**：本支在**上方**（与 python 侧同）；matlab 侧在**右侧、带黑框**。
- **网格 / 括线**：**虚线网格只出现在 `G2`/`G3`，`G1` 没有**（逐张量过：近灰像素 `G2` 3822 / `G3` 8710，`G1` 307 且无网格线色）；
  python 侧 G1 多一条 `B-D most similar` 括线，本支**没有**。

> ★ 上面三条（图高 / 框线 / 段边）**不是缺陷**，依据**不是**"调用方纪律"那一节
> （那一节三条 = **图例位置 / 次序约束 / 边色**，**不含图高与框线**）——
> 而是**单源表里这两格的载体状态**：`assets/mcm-style.json` 的 `h3.height_in` 与 `h10.axes_box`
> 在 **origin 那格都记 `not-landable`**（复跑：`python -c "import json,pathlib; …"`，见 §0）。
> ⇒ **照实描述、不当缺陷报。**

### 一句话

**机械层测的是"形态合不合规范"，判断层测的是"图讲没讲清"。** 六张 Origin 图逐张看过之后：
三张 GREEN 形态（`F1`/`F2`/`F4`）全绿，**判据报不出的黑段边与全框**只有眼睛看得见；三张 RED
信息不比 GREEN 少、底色也都白，却在**形态**上判红，而且**图例压数据（R1）与彩色细边（R1/R3）
判据一条都不报** —— "判词全绿 ≠ 图对了"这条在本支同样成立。（本支 GREEN 在 PDF 侧 `F5` 判红，
那是 §3.3 / §4 说清了的**载体限制假红**，不是形态缺陷。）
