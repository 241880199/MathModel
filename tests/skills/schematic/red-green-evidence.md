# Task 3 · RED × GREEN 对照证据（`mcm-schematic`）

本文件由 `tests/skills/schematic/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。**§1 / §2 / §3 / §4 / §6 的机器部分逐格解析自 stdout，不手抄**；**§5 的性质判定与 §7 的看图记录是手写**（文里已标明）。

## §0 口径（同场景 · 同一把尺 · RED 是自变量）

- **场景**：`tests/skills/schematic/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联）。★ 本支与另三支载体的**一处设计差异**（依据 Task 3 任务书与设计 §5.3「三个隔离写手各拿**同一份**场景描述」）：**同一场景 × 3 位隔离写手**（看写手间离散度），**不是** 3 场景 × 1 位。
- **两侧**：RED = 3 位**干净上下文**写手（**未用 `fork`**）的图；GREEN = **用本 skill** 出的同场景图（1 份）。
- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` —— 两侧用的是**同一版**（工作树 blob == `HEAD:` blob，见下）；**判据逻辑一字未改**。两侧**同一组参数**：`--schematic` ＋ `--textwidth-in 6.75`。
- **判据清单现取**：本支 **12 条**（`A1、A3、A4、F1、F2、F3a、F3b、F3c、F3d、F4、F5、F6`）。**不写死条数**（先例：plot-python 把清单写死成 6 条而实得 9 条 ⇒ 汇总表静默归零）。
- **RED 侧冻结自证**（`git hash-object` vs `HEAD:`）—— **RED 是本任务的自变量**，本轮**未改**：

| 文件 | 工作树 blob | `HEAD:` blob | 相同？ |
| :-- | :-- | :-- | :-- |
| `tests/skills/schematic/red/out-R1/figure.tex` | `296714f2d04c` | `296714f2d04c` | 是 |
| `tests/skills/schematic/red/out-R1/caption.txt` | `d53735314390` | `d53735314390` | 是 |
| `tests/skills/schematic/red/out-R2/figure.tex` | `da3a88ba2064` | `da3a88ba2064` | 是 |
| `tests/skills/schematic/red/out-R2/caption.txt` | `211b98e7c2e3` | `211b98e7c2e3` | 是 |
| `tests/skills/schematic/red/out-R3/figure.tex` | `10f17cf792c3` | `10f17cf792c3` | 是 |
| `tests/skills/schematic/red/out-R3/caption.txt` | `e11f2f6b8738` | `e11f2f6b8738` | 是 |
| `tests/skills/schematic/green/out-G1/figure.tex` | `307f8e18eba7` | `307f8e18eba7` | 是 |
| `tests/skills/schematic/green/out-G1/caption.txt` | `e7b938cbaac2` | `e7b938cbaac2` | 是 |

- **检查器自证**：工作树 blob `0a4bb765a825` · `HEAD:` blob `0a4bb765a825` ⇒ **相同**

- ★ **RED 的诚实边界（硬要求 7 / 设计 §9.3）**：中性骨架 `neutral-skeleton.tex` **本身已保证**「能编译、有节点有箭头」⇒ 这轮 RED **测不到「连图都出不来」那一类失败**。**不声称覆盖全部失败模式。**
- ★ **环境旁路如实披露**：写手是本机 Claude Code 的 agent，会话级共享上下文里另有两处删不掉的可见面 ——① 可用 skill 列表里 `mcm-schematic` 那一行的**类别名**；② 项目记忆 `MEMORY.md`。**它们泄的是「有这几类要求」，不是「判据的边界在哪」**（阈值、线宽集合、图注形态、`A` 族 ID 与口径都看不到）。详见 `red/writer-self-reports.md`。

## §1 场景（逐字内联；RED 与 GREEN 同一份）

```text
# Brief: a schematic for the paper's modelling workflow

You are helping a team prepare a figure for their MCM/ICM paper. Their
modelling workflow for an epidemic-control study is described below.
Draw **one schematic figure** that lets a reader follow this workflow.

The workflow:

- **Data collection** - assemble weekly case counts, mobility traces and
  vaccination coverage for the study city.
- **Preprocessing** - clean the three streams and align them onto a common
  weekly grid.
- **Calibration** - estimate the transmission parameters by fitting a
  compartmental model to the aligned data.
- **Fit check** - decide whether the fit residual is acceptable.
  - If it is **not** acceptable, revise the model structure or the priors
    and return to **Calibration** (this loop can repeat).
  - If it is acceptable, move on.
- **Scenario projections** - run the calibrated model forward under three
  alternative policies: no intervention, a vaccination campaign, and
  school closure.
- **Comparison** - compare the three projections and rank them.
- **Recommendation** - write the recommendation that goes into the paper.

Deliverables - write all of these into the output directory:

1. `figure.tex` - a **self-contained, compilable** LaTeX document whose body
   is the figure as a TikZ picture. It must compile with `pdflatex` as-is.
   A minimal working TikZ skeleton is provided at the path given to you;
   you may copy it and build the figure on top of it.
2. `figure.pdf` - the compiled figure.
3. `caption.txt` - the English caption for the figure, as plain text.

Notes:

- The figure should be a schematic a reader can follow: boxes for the steps
  and arrows for the flow between them.
- Single figure, deterministic, no network access.

Environment fact (not part of the brief): `pdflatex` is on PATH.
```

## §2 RED 原始读数（三位干净上下文写手 · 中性骨架 · 无规范）

### R1

图注（`tests/skills/schematic/red/out-R1/caption.txt`，逐字字节读入）：
```text
Schematic of the epidemic-control modelling workflow. Weekly case counts, mobility traces and vaccination coverage are assembled for the study city and, in preprocessing, cleaned and aligned onto a common weekly grid. Transmission parameters are estimated by fitting a compartmental model to the aligned data (calibration); if the fit residual is unacceptable the model structure or the priors are revised and calibration is repeated, and once the fit is accepted the calibrated model is projected forward under three policies (no intervention, a vaccination campaign, and school closure). The three projections are compared and ranked, and the ranking is written up as the paper's recommendation.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/figure-choose/check-figure-style.py --fig tests/skills/schematic/red/out-R1/figure.pdf --caption @tests/skills/schematic/red/out-R1/caption.txt --textwidth-in 6.75 --schematic
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 97.04%）；下限 136
FAIL  F1  图宽比 1.225（分母 6.75 in）
PASS  F2  彩色主色数 0
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 103 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 103 词）
FAIL  F6  内嵌字体 ['CMR10', 'CMR7', 'CMR9']
PASS  A1  节点框 0 个，重叠 0 对：[]
PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 155 词
FAIL  A4  越界线宽 2 种：[0.399, 0.797]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
RESULT: FAIL（F1,F3a,F3b,F3c,F6,A4）
[exit=1]
```

### R2

图注（`tests/skills/schematic/red/out-R2/caption.txt`，逐字字节读入）：
```text
Figure 1. Modelling workflow. Weekly case counts, mobility traces and vaccination coverage for the study city are collected and, during preprocessing, cleaned and aligned onto a common weekly grid. Transmission parameters are then estimated by calibrating a compartmental model to the aligned data. If the fit residual is not acceptable, the model structure or the priors are revised and calibration is repeated; this loop may run more than once. Once the fit is acceptable, the calibrated model is projected forward under three alternative policies (no intervention, a vaccination campaign, and school closure), and the three projections are compared and ranked to produce the recommendation written into the paper.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/figure-choose/check-figure-style.py --fig tests/skills/schematic/red/out-R2/figure.pdf --caption @tests/skills/schematic/red/out-R2/caption.txt --textwidth-in 6.75 --schematic
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 96.92%）；下限 136
FAIL  F1  图宽比 1.259（分母 6.75 in）
PASS  F2  彩色主色数 0
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 108 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 108 词）
FAIL  F6  内嵌字体 ['CMR10', 'CMR7', 'CMR9']
PASS  A1  节点框 0 个，重叠 0 对：[]
PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 158 词
FAIL  A4  越界线宽 2 种：[0.399, 0.797]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
RESULT: FAIL（F1,F3a,F3b,F3c,F6,A4）
[exit=1]
```

### R3

图注（`tests/skills/schematic/red/out-R3/caption.txt`，逐字字节读入）：
```text
Modelling workflow of the epidemic-control study. Weekly case counts, mobility traces and vaccination coverage are collected for the study city and aligned onto a common weekly grid, and a compartmental transmission model is calibrated to the aligned data. If the fit residual is unacceptable, the model structure or the priors are revised and calibration is repeated; otherwise the calibrated model is projected forward under three policies (no intervention, a vaccination campaign, and school closure). The three projections are compared and ranked, and the ranking is summarised as the paper's recommendation.
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/figure-choose/check-figure-style.py --fig tests/skills/schematic/red/out-R3/figure.pdf --caption @tests/skills/schematic/red/out-R3/caption.txt --textwidth-in 6.75 --schematic
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.18%）；下限 136
FAIL  F1  图宽比 1.259（分母 6.75 in）
PASS  F2  彩色主色数 0
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 90 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 90 词）
FAIL  F6  内嵌字体 ['CMR10', 'CMR7', 'CMR9']
PASS  A1  节点框 11 个，重叠 0 对：[]
PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 124 词
PASS  A4  越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
RESULT: FAIL（F1,F3a,F3b,F3c,F6）
[exit=1]
```

## §3 GREEN 原始读数（本 skill 产物）

### G1

图注（`tests/skills/schematic/green/out-G1/caption.txt`，逐字字节读入）：
```text
Figure 1: Modelling workflow from data collection to policy recommendation
```

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe tests/skills/figure-choose/check-figure-style.py --fig tests/skills/schematic/green/out-G1/figure.pdf --caption @tests/skills/schematic/green/out-G1/caption.txt --textwidth-in 6.75 --schematic
PASS  F4  外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.98%）；下限 136
PASS  F1  图宽比 0.950（分母 6.75 in）
PASS  F2  彩色主色数 0
PASS  F5  越界主色 0 种（不在 H14 允许集合）：[]
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 8（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 8 词）
PASS  F6  内嵌字体 ['TeXGyreTermesX-Regular']
PASS  A1  节点框 9 个，重叠 0 对：[]
PASS  A3  越出页框 0 词（容差 0.5pt）：[]；共 16 词
PASS  A4  越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt）
RESULT: PASS
[exit=0]
```

## §4 对照表（机器抽取）

每个格子 = 状态：绿 = `PASS` / 红 = `FAIL`。判定词逐格解析自 §2/§3 的 stdout；判据 ID 见表头（**现取**）。

| 产品 | 侧 | A1 | A3 | A4 | F1 | F2 | F3a | F3b | F3c | F3d | F4 | F5 | F6 | RESULT |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | RED | 绿† | 绿 | 红 | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 绿 | 红 | FAIL |
| R2 | RED | 绿† | 绿 | 红 | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 绿 | 红 | FAIL |
| R3 | RED | 绿 | 绿 | 绿 | 红 | 绿 | 红 | 红 | 红 | 绿 | 绿 | 绿 | 红 | FAIL |
| G1 | GREEN | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | 绿 | PASS |

★ **`†` = 空绿格**（本表出现的：`R1×A1、R2×A1`）：判词为 `节点框 0 个` ⇒ 判据**在这份上没有判到任何对象**（`A1` 的节点框集合只收既填充又描边的闭合块，对 `fill=none` 的节点**视而不见**）⇒ 该格**不构成「判据在这份上过了」的证据**。`A1` 的已知边界见 `.claude/skills/mcm-schematic/references/schematic-style.md` §3 第 1 条（残余那一句）。★ **`GREEN` 的 `A1` 不是空绿**（G1 = `节点框 9 个`），别与 R1/R2 混为一谈。

### §4.1 逐判据判词（机器抽取；判词原文，不手抄）

| 产品 | 侧 | 判据 | 状态 | 判词 |
| :-- | :-- | :-- | :-- | :-- |
| R1 | RED | A1 | PASS | 节点框 0 个，重叠 0 对：[] |
| R1 | RED | A3 | PASS | 越出页框 0 词（容差 0.5pt）：[]；共 155 词 |
| R1 | RED | A4 | FAIL | 越界线宽 2 种：[0.399, 0.797]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt） |
| R1 | RED | F1 | FAIL | 图宽比 1.225（分母 6.75 in） |
| R1 | RED | F2 | PASS | 彩色主色数 0 |
| R1 | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R1 | RED | F3b | FAIL | 图注词数 103 超硬上限 17 |
| R1 | RED | F3c | FAIL | 句末不加句号 |
| R1 | RED | F3d | PASS | 图注正文非空（正文 103 词） |
| R1 | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 97.04%）；下限 136 |
| R1 | RED | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| R1 | RED | F6 | FAIL | 内嵌字体 ['CMR10', 'CMR7', 'CMR9'] |
| R2 | RED | A1 | PASS | 节点框 0 个，重叠 0 对：[] |
| R2 | RED | A3 | PASS | 越出页框 0 词（容差 0.5pt）：[]；共 158 词 |
| R2 | RED | A4 | FAIL | 越界线宽 2 种：[0.399, 0.797]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt） |
| R2 | RED | F1 | FAIL | 图宽比 1.259（分母 6.75 in） |
| R2 | RED | F2 | PASS | 彩色主色数 0 |
| R2 | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R2 | RED | F3b | FAIL | 图注词数 108 超硬上限 17 |
| R2 | RED | F3c | FAIL | 句末不加句号 |
| R2 | RED | F3d | PASS | 图注正文非空（正文 108 词） |
| R2 | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 96.92%）；下限 136 |
| R2 | RED | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| R2 | RED | F6 | FAIL | 内嵌字体 ['CMR10', 'CMR7', 'CMR9'] |
| R3 | RED | A1 | PASS | 节点框 11 个，重叠 0 对：[] |
| R3 | RED | A3 | PASS | 越出页框 0 词（容差 0.5pt）：[]；共 124 词 |
| R3 | RED | A4 | PASS | 越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt） |
| R3 | RED | F1 | FAIL | 图宽比 1.259（分母 6.75 in） |
| R3 | RED | F2 | PASS | 彩色主色数 0 |
| R3 | RED | F3a | FAIL | 图注以 `Figure N:` 起 |
| R3 | RED | F3b | FAIL | 图注词数 90 超硬上限 17 |
| R3 | RED | F3c | FAIL | 句末不加句号 |
| R3 | RED | F3d | PASS | 图注正文非空（正文 90 词） |
| R3 | RED | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.18%）；下限 136 |
| R3 | RED | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| R3 | RED | F6 | FAIL | 内嵌字体 ['CMR10', 'CMR7', 'CMR9'] |
| G1 | GREEN | A1 | PASS | 节点框 9 个，重叠 0 对：[] |
| G1 | GREEN | A3 | PASS | 越出页框 0 词（容差 0.5pt）：[]；共 16 词 |
| G1 | GREEN | A4 | PASS | 越界线宽 0 种：[]；允许集合 (0.5, 0.7, 0.9, 1.4173, 3.9685)（容差 0.02pt） |
| G1 | GREEN | F1 | PASS | 图宽比 0.950（分母 6.75 in） |
| G1 | GREEN | F2 | PASS | 彩色主色数 0 |
| G1 | GREEN | F3a | PASS | 图注以 `Figure N:` 起 |
| G1 | GREEN | F3b | PASS | 图注词数 8（上限 12，硬上限 17） |
| G1 | GREEN | F3c | PASS | 句末不加句号 |
| G1 | GREEN | F3d | PASS | 图注正文非空（正文 8 词） |
| G1 | GREEN | F4 | PASS | 外缘环 RGB (255, 255, 255) 亮度 255（占环 100.00%）；近灰众数 RGB (255, 255, 255) 亮度 255（占全图 91.98%）；下限 136 |
| G1 | GREEN | F5 | PASS | 越界主色 0 种（不在 H14 允许集合）：[] |
| G1 | GREEN | F6 | PASS | 内嵌字体 ['TeXGyreTermesX-Regular'] |

### §4.2 汇总（由 §4 的格子逐格重算）

| 侧 | 红格数（判据 × 产物） | 判红的判据 ID（并集） | 全绿产物数 | 空绿格数（判到 0 个对象） |
| :-- | :-- | :-- | :-- | :-- |
| RED | 17 | A4、F1、F3a、F3b、F3c、F6 | 0/3 | 2 |
| GREEN | 0 | （无） | 1/1 | 0 |

★ **空绿格（`†`）不计入「绿」**：`A1` 在 R1/R2 上判到 `0` 个节点框 ⇒ 判据**没有判到对象**（见 §4 表注与 `schematic-style.md` §3 第 1 条）；`GREEN` 的 `A1` 是**真过**（G1 `节点框 9 个`）。**红格数与全绿产物数不受空绿影响** —— 本器**只**把 `A1` 的「节点框 0 个」识别为空绿（`is_empty_green` 硬编码 `k == "A1"`）；**其余判据若判到 0 个对象，本器看不见**（**不声称它们不是空绿**）—— 而 R1/R2 本就因他判据判红，故那几格不影响红格数。

## §5 RED 的红逐条点名（硬要求 1：真红 / 级联 / 假红已修）

（红集**机器抽取**自 §2；性质判定是人工判定，逐条写。**本支无级联、无假红** —— 理由见下表与末段。）

- **R1 红集** = `{A4, F1, F3a, F3b, F3c, F6}`
- **R2 红集** = `{A4, F1, F3a, F3b, F3c, F6}`
- **R3 红集** = `{F1, F3a, F3b, F3c, F6}`

**这一节是判断层，机械判据判不了它。** 下面是本任务读完四份判词、并**亲眼看过四张图**
（`red/out-R{n}/figure.png` ×3 与 `green/out-G1/figure.png`）之后写下的。**本节手写，不是机器抽取。**

### 逐条点名（判据 · 读数 · 为什么 · 性质）

| 判据 | 谁红 | 读数（见 §2/§3） | 为什么红 | 性质 |
| :--- | :--- | :--- | :--- | :--- |
| `F1` 图宽比 | R1/R2/R3 | R1 `1.225`（A4 页盒）/ R2 `1.259` / R3 `1.259`（letter 页盒），分母 `6.75` | 三位写手都**没把页盒／图框钉到版心宽** —— 中性骨架用的是 `article` 默认页盒，而宽度纪律只存在于规范里（`\mcmscfigwidth`），写手看不到 | **真红**（三条独立，同一根因） |
| `F3a` 图注前缀 | R1/R2/R3 | `caption.txt` 不以 `Figure N:` 起：R1 以 `Schematic of...` 起、R3 不带前缀；★ **最有信息量的一例 = R2 以 `Figure 1.`（句点）起** —— 它**知道要写前缀、却用错了分隔符**（`N.` 而非 `N:`）⇒ 正好证明这条判据编码的是**猜不到**的约定（连"知道要写 `Figure N`"的写手也落红） | 图注形态（`Figure N:` 前缀）是规范 ∕ `house-style` 的产物契约，写手没被告知 | **真红** |
| `F3b` 图注词数 | R1/R2/R3 | `103` / `108` / `90` 词（硬上限 `17`） | 写手把整段工作流写进了图注（R1 的图注就是一段方法学散文） | **真红**（与 `F3a` 同一根因：图注惯例） |
| `F3c` 句末句号 | R1/R2/R3 | 三条 `caption.txt` **都以句号收尾** | 同上：图注**不押句号**这条是规范 ∕ `house-style` 的契约 | **真红**（同上根因） |
| `F6` 字体族 | R1/R2/R3 | 内嵌 `['CMR10','CMR7','CMR9']`（Computer Modern），不在可接受族里 | 中性骨架不载字体宏包 ⇒ 默认 CM；规范要求与论文正文同源（`newtxtext`） | **真红** |
| `A4` 线宽 | R1/R2 | R1/R2 越界线宽 `[0.399, 0.797]`（TikZ 默认 0.4pt 与 `thick`≈0.8pt） | 写手用 TikZ 默认线宽；允许集合是**本支样式层**的（`0.5/0.7/0.9pt` + `0.5/1.4mm`） | **真红** |
| `A4` 线宽 | R3 | **PASS**（越界 0 种） | R3 自己选了 `0.7pt` 统一线宽，**恰好命中**允许集合 ⇒ 同一判据**依写手而异** | **不是红**（R3 的偶然命中，如实记） |

**没有级联、没有假红。** 与表格那支不同，本支的 `A` 族**没有 fail-closed 红**：四份产物的
矢量层与文字层都在；`A3`/`A4` 拿到输入，而 **`A1` 在 R1/R2 上判到 `0` 个框**（**空绿**，见 §4）——
它在这两份上**什么都没判到**，不是"判过了"。**`GREEN` 的 `A1` 是真过**（G1 = `节点框 9 个`），
别把两者混为一谈。图层非空 ⇒ 不存在"一条红了带红一串"的级联；
检查器本任务**一字未改**（blob == `HEAD`，见 §0）⇒ 也**没有"判据假红已修"**这一类。
**不声称穷尽**：上表只列本支四份产物**实际触发**的判据，不声明覆盖率。

### 本支 RED 最诚实的读法（别把"红得多"当质量证明）

- **三份 RED 都编译成功**（`rc=0` · `Overfull \hbox=0`，见 §8），**都画出了正确的拓扑**
  （竖排七步 · 一条修订回环 · 三路投影扇出再汇合）—— 图**读得清**（见 §7）。
- 判据抓的是**没被告知的约定**：**图宽怎么钉**（`F1`）、**图注怎么写**（`F3a/b/c`）、
  **字体跟谁同源**（`F6`）、**线宽取哪一档**（`A4`）。这些**都不是"图烂"**，而是
  **"没看规范就不会知道"**。
- ★ **反向也要照实**：`F3a`/`F3b`/`F3c` 三条红**共享同一个根因**（图注惯例），读的时候
  别当成"三个独立的图缺陷"；`A4` 在 R3 身上**根本没红** ⇒ 这一条有**写手侧的偶然性**。
- ★ **RED 的诚实边界**（设计 §9.3 / 硬要求 7）：中性骨架**已经保证**"能编译、有节点有箭头"
  ⇒ 这轮 RED **测不到"连图都出不来"那一类失败**（写不出 TikZ、编不过、没有节点/箭头）。
  **不声称覆盖全部失败模式。**

## §6 两侧 `.tex` 并排逐字 diff（机器抽取 + 人工注释）

**结构读数（机器抽取）**：

| 产品 | 行数 | `\node` | `\draw` | `\mcmedge` | 有 `\input` 样式层 | 有 `\documentclass` | `\usepackage` |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| R1 | 63 | 11 | 12 | 0 | 否 | 是 | geometry, tikz |
| R2 | 79 | 10 | 12 | 0 | 否 | 是 | geometry, tikz |
| R3 | 88 | 11 | 13 | 0 | 否 | 是 | geometry, tikz |
| G1 | 51 | 11 | 1 | 10 | 是 | 是 | geometry |

### 场景（唯一）：R1 vs G1（`difflib.unified_diff`，逐字）

```diff
--- red/out-R1/figure.tex
+++ green/out-G1/figure.tex
@@ -1,63 +1,51 @@
-\documentclass{article}
-\usepackage[a4paper,margin=1.6cm]{geometry}
-\usepackage{tikz}
-\usetikzlibrary{positioning,arrows.meta,shapes.geometric}
+% =====================================================================
+% mcm-schematic · green/out-G1/figure.tex
+%
+% GREEN product for Task 3 — produced with the mcm-schematic skill:
+%   category  = technical route (course of action, with a branch + a loop);
+%   skeleton  = assets/skeletons/pipeline-branch.tex, adapted (a 3-way
+%               projection fan instead of 2 routes, plus a dashed revision
+%               loop back to Calibration);
+%   styling   = ONLY via ../schematic-style.tex (this file pins no colour,
+%               line width, corner radius, font or spacing literal).
+% =====================================================================
+
+\documentclass[12pt]{article}
+\input{../schematic-style.tex}
+\usepackage[paperwidth=\mcmscfigwidth,paperheight=4.10in,margin=0pt]{geometry}
+\pagestyle{empty}
+\setlength{\parindent}{0pt}
 
 \begin{document}
+\begin{tikzpicture}[x=1in, y=1in]
+  \useasboundingbox (0,0) rectangle (\mcmscfigwidth, 4.10in);
 
-\begin{figure}[htbp]
-\centering
-\begin{tikzpicture}[
-  font=\small,
-  box/.style={draw, rounded corners=2pt, align=center,
-              minimum width=42mm, minimum height=10mm, inner sep=3pt},
-  pol/.style={draw, rounded corners=2pt, align=center,
-              minimum width=30mm, minimum height=9mm, inner sep=3pt},
-  decision/.style={draw, diamond, aspect=1.9, align=center,
-                   inner sep=1pt, minimum width=44mm, minimum height=16mm},
-  arr/.style={-{Latex[length=2mm]}, thick},
-  lbl/.style={font=\scriptsize, inner sep=2pt, align=center},
-]
+  \node[mcmnode, text width=0.95in]                    (nData) at (0.85, 3.05) {Data collection};
+  \node[mcmnode, text width=0.95in]                    (nPre)  at (2.15, 3.05) {Preprocessing};
+  \node[mcmnode, text width=0.85in]                    (nCal)  at (3.45, 3.05) {Calibration};
+  \node[mcmdec, text width=0.58in, minimum size=0.66in] (nDec) at (5.05, 3.05) {fit ok?};
 
-% ---- main spine -------------------------------------------------
-\node[box] (data)  at (0,0)      {Data collection\\[-1pt]{\scriptsize weekly cases, mobility, vaccination}};
-\node[box] (prep)  at (0,-1.8)   {Preprocessing\\[-1pt]{\scriptsize clean and align to a weekly grid}};
-\node[box] (calib) at (0,-3.6)   {Calibration\\[-1pt]{\scriptsize fit compartmental model}};
-\node[decision] (check) at (0,-5.9) {Fit check\\ residual acceptable?};
-\node[box] (proj)  at (0,-8.5)   {Scenario projections\\[-1pt]{\scriptsize calibrated model, forward}};
-\node[pol] (p1) at (-5.4,-10.9)  {No intervention};
-\node[pol] (p2) at (0,-10.9)     {Vaccination campaign};
-\node[pol] (p3) at (5.4,-10.9)   {School closure};
-\node[box] (comp)  at (0,-12.9)  {Comparison\\[-1pt]{\scriptsize compare and rank}};
-\node[box] (rec)   at (0,-14.6)  {Recommendation\\[-1pt]{\scriptsize written into the paper}};
+  \node[mcmfillalt, text width=1.05in] (nP1) at (1.45, 2.00) {No intervention};
+  \node[mcmfillalt, text width=1.05in] (nP2) at (3.20, 2.00) {Vaccination campaign};
+  \node[mcmfillalt, text width=1.05in] (nP3) at (4.95, 2.00) {School closure};
 
-% ---- spine arrows -----------------------------------------------
-\draw[arr] (data)  -- (prep);
-\draw[arr] (prep)  -- (calib);
-\draw[arr] (calib) -- (check);
-\draw[arr] (check) -- (proj) node[midway, right, lbl] {Yes};
-\draw[arr] (proj)  -- (p1);
-\draw[arr] (proj)  -- (p2);
-\draw[arr] (proj)  -- (p3);
-\draw[arr] (p1)    -- (comp);
-\draw[arr] (p2)    -- (comp);
-\draw[arr] (p3)    -- (comp);
-\draw[arr] (comp)  -- (rec);
+  \node[mcmnode, text width=1.00in] (nCmp) at (3.20, 1.10) {Comparison};
+  \node[mcmterm, text width=1.18in] (nOut) at (3.20, 0.33) {Recommendation};
 
-% ---- revise-and-return loop -------------------------------------
-\draw[arr] (check.west) -- (-6.4,-5.9) -- (-6.4,-3.6) -- (calib.west);
-\node[lbl] at (-4.1,-4.75) {No: revise model\\or priors (repeat)};
+  \mcmedge{nData}{nPre}
+  \mcmedge{nPre}{nCal}
+  \mcmedge{nCal}{nDec}
+  \mcmedge{nDec}{nP1}
+  \mcmedge{nDec}{nP2}
+  \mcmedge{nDec}{nP3}
+  \mcmedge{nP1}{nCmp}
+  \mcmedge{nP2}{nCmp}
+  \mcmedge{nP3}{nCmp}
+  \mcmedge{nCmp}{nOut}
 
+  % revision loop (S2: dashed = feedback / optional; one dashed semantic only)
+  \draw[mcmdash] (nDec.north) -- ++(0,0.42) -| (nCal.north);
+  \node[mcmnote] at ($(nDec.north)!0.5!(nCal.north) + (0,0.42)$) {No};
+  \node[mcmlabel] at ($(nDec.south) + (0.26,-0.16)$) {Yes};
 \end{tikzpicture}
-\caption{Schematic of the epidemic-control modelling workflow. Weekly case counts,
-mobility traces and vaccination coverage are assembled for the study city and, in
-preprocessing, cleaned and aligned onto a common weekly grid. Transmission
-parameters are estimated by fitting a compartmental model to the aligned data
-(calibration); if the fit residual is unacceptable the model structure or the
-priors are revised and calibration is repeated, and once the fit is accepted the
-calibrated model is projected forward under three policies (no intervention, a
-vaccination campaign, and school closure). The three projections are compared and
-ranked, and the ranking is written up as the paper's recommendation.}
-\end{figure}
-
 \end{document}
```

### 场景（唯一）：R2 vs G1（`difflib.unified_diff`，逐字）

```diff
--- red/out-R2/figure.tex
+++ green/out-G1/figure.tex
@@ -1,79 +1,51 @@
 % =====================================================================
-% Modelling-workflow schematic for the epidemic-control study.
-% Self-contained: compiles with pdflatex as-is.
-% Built on top of the provided neutral skeleton (node + directed arrow).
+% mcm-schematic · green/out-G1/figure.tex
+%
+% GREEN product for Task 3 — produced with the mcm-schematic skill:
+%   category  = technical route (course of action, with a branch + a loop);
+%   skeleton  = assets/skeletons/pipeline-branch.tex, adapted (a 3-way
+%               projection fan instead of 2 routes, plus a dashed revision
+%               loop back to Calibration);
+%   styling   = ONLY via ../schematic-style.tex (this file pins no colour,
+%               line width, corner radius, font or spacing literal).
 % =====================================================================
-\documentclass{article}
-\usepackage[margin=1in]{geometry}
-\usepackage{tikz}
-\usetikzlibrary{positioning,shapes.geometric,arrows.meta,calc}
+
+\documentclass[12pt]{article}
+\input{../schematic-style.tex}
+\usepackage[paperwidth=\mcmscfigwidth,paperheight=4.10in,margin=0pt]{geometry}
+\pagestyle{empty}
+\setlength{\parindent}{0pt}
 
 \begin{document}
-\pagestyle{empty}
+\begin{tikzpicture}[x=1in, y=1in]
+  \useasboundingbox (0,0) rectangle (\mcmscfigwidth, 4.10in);
 
-\begin{figure}[htbp]
-\centering
-\begin{tikzpicture}[
-  every node/.style={font=\small},
-  proc/.style={draw, rounded corners=2pt, align=center,
-               minimum width=3.8cm, minimum height=1.0cm, inner sep=4pt},
-  decision/.style={draw, diamond, aspect=2.4, align=center,
-                   inner sep=1pt, minimum width=3.4cm},
-  branch/.style={draw, rounded corners=2pt, align=center,
-                 minimum width=2.9cm, minimum height=1.0cm, inner sep=4pt},
-  arrow/.style={-{Latex[length=2mm]}, thick},
-  flow/.style={arrow},
-]
+  \node[mcmnode, text width=0.95in]                    (nData) at (0.85, 3.05) {Data collection};
+  \node[mcmnode, text width=0.95in]                    (nPre)  at (2.15, 3.05) {Preprocessing};
+  \node[mcmnode, text width=0.85in]                    (nCal)  at (3.45, 3.05) {Calibration};
+  \node[mcmdec, text width=0.58in, minimum size=0.66in] (nDec) at (5.05, 3.05) {fit ok?};
 
-% ---- main column -----------------------------------------------------
-\node[proc] (data) at (0,0)          {Data collection\\{\scriptsize case counts, mobility, vaccination}};
-\node[proc] (prep) at (0,-2.0)       {Preprocessing\\{\scriptsize clean and align to a weekly grid}};
-\node[proc] (calib) at (0,-4.0)      {Calibration\\{\scriptsize fit compartmental model}};
-\node[decision] (fit) at (0,-6.1)    {Fit residual\\acceptable?};
-\node[proc] (proj) at (0,-8.4)       {Scenario projections\\{\scriptsize run calibrated model forward}};
+  \node[mcmfillalt, text width=1.05in] (nP1) at (1.45, 2.00) {No intervention};
+  \node[mcmfillalt, text width=1.05in] (nP2) at (3.20, 2.00) {Vaccination campaign};
+  \node[mcmfillalt, text width=1.05in] (nP3) at (4.95, 2.00) {School closure};
 
-% ---- three policy branches ------------------------------------------
-\node[branch] (polA) at (-4.6,-10.6) {No intervention};
-\node[branch] (polB) at (0,-10.6)    {Vaccination campaign};
-\node[branch] (polC) at (4.6,-10.6)  {School closure};
+  \node[mcmnode, text width=1.00in] (nCmp) at (3.20, 1.10) {Comparison};
+  \node[mcmterm, text width=1.18in] (nOut) at (3.20, 0.33) {Recommendation};
 
-% ---- convergence and output -----------------------------------------
-\node[proc] (comp) at (0,-12.8)      {Comparison\\{\scriptsize compare and rank the three projections}};
-\node[proc] (rec)  at (0,-14.8)      {Recommendation};
+  \mcmedge{nData}{nPre}
+  \mcmedge{nPre}{nCal}
+  \mcmedge{nCal}{nDec}
+  \mcmedge{nDec}{nP1}
+  \mcmedge{nDec}{nP2}
+  \mcmedge{nDec}{nP3}
+  \mcmedge{nP1}{nCmp}
+  \mcmedge{nP2}{nCmp}
+  \mcmedge{nP3}{nCmp}
+  \mcmedge{nCmp}{nOut}
 
-% ---- forward flow ----------------------------------------------------
-\draw[flow] (data) -- (prep);
-\draw[flow] (prep) -- (calib);
-\draw[flow] (calib) -- (fit);
-\draw[flow] (fit) -- node[right, pos=0.5] {\scriptsize Yes} (proj);
-
-\draw[flow] (proj) -- (polA);
-\draw[flow] (proj) -- (polB);
-\draw[flow] (proj) -- (polC);
-
-\draw[flow] (polA) -- (comp);
-\draw[flow] (polB) -- (comp);
-\draw[flow] (polC) -- (comp);
-
-\draw[flow] (comp) -- (rec);
-
-% ---- feedback loop: fit check -> calibration -------------------------
-\draw[flow] (fit.east) -- ++(3.0,0)
-      node[below right, pos=0.45, align=left] {\scriptsize No: revise model\\\scriptsize structure or priors}
-      |- (calib.east);
-
+  % revision loop (S2: dashed = feedback / optional; one dashed semantic only)
+  \draw[mcmdash] (nDec.north) -- ++(0,0.42) -| (nCal.north);
+  \node[mcmnote] at ($(nDec.north)!0.5!(nCal.north) + (0,0.42)$) {No};
+  \node[mcmlabel] at ($(nDec.south) + (0.26,-0.16)$) {Yes};
 \end{tikzpicture}
-\caption{Modelling workflow. Weekly case counts, mobility traces and
-vaccination coverage for the study city are collected and, during
-preprocessing, cleaned and aligned onto a common weekly grid.
-Transmission parameters are then estimated by fitting a compartmental
-model to the aligned data. If the fit residual is not acceptable, the
-model structure or the priors are revised and calibration is repeated
-(this loop may run more than once). Once the fit is acceptable, the
-calibrated model is projected forward under three alternative policies
---- no intervention, a vaccination campaign, and school closure --- and
-the three projections are compared and ranked to produce the
-recommendation written into the paper.}
-\end{figure}
-
 \end{document}
```

### 场景（唯一）：R3 vs G1（`difflib.unified_diff`，逐字）

```diff
--- red/out-R3/figure.tex
+++ green/out-G1/figure.tex
@@ -1,88 +1,51 @@
 % =====================================================================
-% figure.tex -- schematic of the epidemic-control modelling workflow
+% mcm-schematic · green/out-G1/figure.tex
 %
-% Self-contained: compiles with pdflatex as-is.
-% Greyscale only; white background; caption below the figure.
+% GREEN product for Task 3 — produced with the mcm-schematic skill:
+%   category  = technical route (course of action, with a branch + a loop);
+%   skeleton  = assets/skeletons/pipeline-branch.tex, adapted (a 3-way
+%               projection fan instead of 2 routes, plus a dashed revision
+%               loop back to Calibration);
+%   styling   = ONLY via ../schematic-style.tex (this file pins no colour,
+%               line width, corner radius, font or spacing literal).
 % =====================================================================
-\documentclass{article}
-\usepackage[margin=1in]{geometry}
-\usepackage{tikz}
-\usetikzlibrary{positioning, shapes.geometric, arrows.meta}
+
+\documentclass[12pt]{article}
+\input{../schematic-style.tex}
+\usepackage[paperwidth=\mcmscfigwidth,paperheight=4.10in,margin=0pt]{geometry}
+\pagestyle{empty}
+\setlength{\parindent}{0pt}
 
 \begin{document}
+\begin{tikzpicture}[x=1in, y=1in]
+  \useasboundingbox (0,0) rectangle (\mcmscfigwidth, 4.10in);
 
-\begin{figure}[htbp]
-  \centering
-  \begin{tikzpicture}[
-      proc/.style={rectangle, rounded corners=2pt,
-                   draw=black!75, line width=0.6pt,
-                   fill=black!4, text width=3.2cm, minimum height=1.0cm,
-                   align=center, inner sep=3pt, font=\small},
-      dec/.style={diamond, aspect=2.4,
-                  draw=black!75, line width=0.6pt,
-                  fill=black!4, align=center, inner sep=1pt,
-                  minimum width=5.2cm, font=\small},
-      flow/.style={draw=black!80, line width=0.7pt,
-                   -{Latex[length=2.1mm,width=1.6mm]}},
-      retry/.style={draw=black!80, line width=0.7pt, dashed,
-                    -{Latex[length=2.1mm,width=1.6mm]}},
-      elab/.style={font=\scriptsize, inner sep=2pt, fill=white},
-    ]
+  \node[mcmnode, text width=0.95in]                    (nData) at (0.85, 3.05) {Data collection};
+  \node[mcmnode, text width=0.95in]                    (nPre)  at (2.15, 3.05) {Preprocessing};
+  \node[mcmnode, text width=0.85in]                    (nCal)  at (3.45, 3.05) {Calibration};
+  \node[mcmdec, text width=0.58in, minimum size=0.66in] (nDec) at (5.05, 3.05) {fit ok?};
 
-    % ---- main spine ------------------------------------------------
-    \node[proc] (data) {Data collection};
-    \node[proc, below=7mm of data] (pre) {Preprocessing};
-    \node[proc, below=7mm of pre] (cal) {Calibration};
-    \node[dec, below=10mm of cal] (chk) {Fit residual\\acceptable?};
+  \node[mcmfillalt, text width=1.05in] (nP1) at (1.45, 2.00) {No intervention};
+  \node[mcmfillalt, text width=1.05in] (nP2) at (3.20, 2.00) {Vaccination campaign};
+  \node[mcmfillalt, text width=1.05in] (nP3) at (4.95, 2.00) {School closure};
 
-    % ---- revision loop ---------------------------------------------
-    \node[proc, text width=3.4cm, right=16mm of chk] (rev)
-      {Revise model structure or priors};
+  \node[mcmnode, text width=1.00in] (nCmp) at (3.20, 1.10) {Comparison};
+  \node[mcmterm, text width=1.18in] (nOut) at (3.20, 0.33) {Recommendation};
 
-    % ---- scenario branch -------------------------------------------
-    \node[proc, below=13mm of chk] (proj) {Scenario projections};
-    \node[proc, text width=3.2cm, below=9mm of proj] (p2)
-      {Vaccination\\campaign};
-    \node[proc, text width=3.2cm, left=8mm of p2] (p1) {No\\intervention};
-    \node[proc, text width=3.2cm, right=8mm of p2] (p3) {School\\closure};
+  \mcmedge{nData}{nPre}
+  \mcmedge{nPre}{nCal}
+  \mcmedge{nCal}{nDec}
+  \mcmedge{nDec}{nP1}
+  \mcmedge{nDec}{nP2}
+  \mcmedge{nDec}{nP3}
+  \mcmedge{nP1}{nCmp}
+  \mcmedge{nP2}{nCmp}
+  \mcmedge{nP3}{nCmp}
+  \mcmedge{nCmp}{nOut}
 
-    % ---- tail of the spine -----------------------------------------
-    \node[proc, text width=4.6cm, below=11mm of p2] (cmp)
-      {Comparison and ranking};
-    \node[proc, text width=4.6cm, below=7mm of cmp] (rec) {Recommendation};
-
-    % ---- forward flow ----------------------------------------------
-    \draw[flow] (data) -- (pre);
-    \draw[flow] (pre) -- (cal);
-    \draw[flow] (cal) -- (chk);
-    \draw[flow] (chk) -- node[elab, right] {acceptable} (proj);
-
-    \draw[flow] (proj) -- (p2);
-    \draw[flow] (proj.south) -- ++(0,-4mm) -| (p1.north);
-    \draw[flow] (proj.south) -- ++(0,-4mm) -| (p3.north);
-
-    \draw[flow] (p2) -- (cmp);
-    \draw[flow] (p1.south) -- ++(0,-4mm) -| (cmp.north);
-    \draw[flow] (p3.south) -- ++(0,-4mm) -| (cmp.north);
-
-    \draw[flow] (cmp) -- (rec);
-
-    % ---- feedback (revision) loop ----------------------------------
-    \draw[retry] (chk.east) -- node[elab, above] {not acceptable} (rev.west);
-    \draw[retry] (rev.north) |- node[elab, right, pos=0.15] {revise \& refit}
-      (cal.east);
-
-  \end{tikzpicture}
-  \caption{Modelling workflow of the epidemic-control study. Weekly case
-  counts, mobility traces and vaccination coverage are collected for the
-  study city and aligned onto a common weekly grid, and a compartmental
-  transmission model is calibrated to the aligned data. If the fit residual
-  is unacceptable, the model structure or the priors are revised and
-  calibration is repeated; otherwise the calibrated model is projected
-  forward under three policies (no intervention, a vaccination campaign, and
-  school closure). The three projections are compared and ranked, and the
-  ranking is summarised as the paper's recommendation.}
-  \label{fig:workflow}
-\end{figure}
-
+  % revision loop (S2: dashed = feedback / optional; one dashed semantic only)
+  \draw[mcmdash] (nDec.north) -- ++(0,0.42) -| (nCal.north);
+  \node[mcmnote] at ($(nDec.north)!0.5!(nCal.north) + (0,0.42)$) {No};
+  \node[mcmlabel] at ($(nDec.south) + (0.26,-0.16)$) {Yes};
+\end{tikzpicture}
 \end{document}
```

**人工读一遍：差异是不是"规范导致"的？**

- **可归因于规范（结构性的）**：
  1. **`\input{../schematic-style.tex}`**：G1 有一行 `\input` 样式层；三份 RED **一行都没有**
     （它们是自包含 `article` 文档，样式散落在自己文件里）—— 这是本 skill 的**样式单源**契约，直接对应
     `F6`（字体族，由样式层载 `newtxtext`）与 `A4`（线宽，由样式层的长度变量给出）。
  2. **页盒**：G1 用 `geometry` 的 `paperwidth=\mcmscfigwidth` 把页盒钉成`\mcmscfigwidth`；三份 RED
     都是 `article` 默认页盒 ⇒ 直接对应 `F1`。
- **不是规范要求、属设计 / 写手判断的**：
  1. **朝向不同**：G1 是**横向**主流程；三份 RED 都是**竖向**主流程（R1/R2/R3 各自的选择）。
  2. **图注措辞与长度**：G1 图注 8 词；RED 三份是 90–108 词的段落 —— 差异**双向**（既有 `F3` 的形态差，
     也有"写多写少"的判断差）。
  3. **回环线型**：R3 自己就把回环画成虚线（与 G1 同向）；R1/R2 画成实线。**这条差异一半是规范
     （`S2` 要求虚线编码回环／反馈）、一半是写手自己的好坏判断** —— 不能全记在规范头上。
- **结论**：两侧差异**集中在**（a）样式单源与页盒钉宽（规范契约）、（b）朝向 / 图注长度 / 回环线型
  （设计选择）。**不是**"某些节点画错"——**四份图的拓扑按工作流图层级而言一致**（同一场景的七步 + 回环 + 三路分支）。
  ★ **本句原写"四份图的拓扑完全一致"，过宽**：**不声称图元逐字同构** —— **R3 把"修订"画成了一个显式 `\node`**
  （`tests/skills/schematic/red/out-R3/figure.tex:39` 的 `\node[proc] (rev) {Revise model structure or priors}`），
  而 R1/R2 没有把同一语义画成**工作流节点**（R1 只在回环旁放一个**标签** `\node[lbl]`（`:49`）、R2 把它作**边标签**（`:62`））
  ⇒ 结构表自印 `\node` 计数 **R1=11 / R2=10 / R3=11**（见上）。**按工作流图层级**读，四份是同构的。

## §7 看图记录（硬要求 4：亲眼看图）

**这一节是「看一眼」层（GC11 / 设计 §5.4），机器判不了它。** 四张图**都编译、都渲成 150dpi PNG、
都由本 agent 亲眼看过**；下面是**从这张图读到了什么**。★ 先例：origin 那支的粉边与图例压数据、
表格那支的超长表题，**判据一条都不报** —— 本节就是找那种东西。

本支必看的五点：① 箭头有没有压住字；② 主流程与回环/反馈**一眼分得开**吗；③ 图例在不在；
④ 标注有没有落到画外；⑤ 节点内文字有没有溢出。

### GREEN（`green/out-G1/figure.png`，962×615 @150dpi）

- **读到**：一条横向主流程 `Data collection → Preprocessing → Calibration → fit ok?`（菱形判定），
  一条**虚线**从菱形顶部标着 `No` 绕回 `Calibration` 顶部；`Yes` 向下扇出到三个并列方框
  （`No intervention` / `Vaccination campaign` / `School closure`），三路再汇入 `Comparison` → `Recommendation`。
- ① 箭头不压字；② **虚线反馈 vs 实线主流程一眼可分**；③ 无图例（只有两种线义，虚线那条已用 `No` 标注
  ⇒ 不需要图例）；④ 标注都在框内；⑤ 文字不溢出节点。
- **判据不报、眼睛看得见**：`Yes` 标签落在菱形右侧，而三条出边都从菱形**底部**离开 ⇒ `Yes`
  离其中两条边略远；三条扇出边在菱形附近**有短距离重叠**（扇出常态，非缺陷）。

### RED（`red/out-R{n}/figure.png`）

- **R1**（`red/out-R1/figure.png`，1241×1754 @150dpi ≈ A4）：读到竖排七步 · 菱形 `Fit check` ·
  一条**实线**回环（在左侧，标 `No: revise model or priors (repeat)`）绕回 `Calibration` ·
  三路扇出再汇合 · 图下一整段 103 词图注。① 不压字；② ★ **回环是实线、与主流程同款**
  ⇒ **主/环靠线型分不开**，只能读标签；③ 无图例；④ 标注在框内；⑤ 文字不溢出。
- **R2**（`red/out-R2/figure.png`）：同上竖排，回环从菱形**东侧**绕上去接 `Calibration` **东侧**，
  同样是**实线**。② ★ **主/环同样靠线型分不开**；其余四点同上。
- **R3**（`red/out-R3/figure.png`）：竖排；`not acceptable` 一路向右进 `Revise model structure or priors` 框，
  再以**虚线**标 `revise & refit` 回到 `Calibration` 东侧 —— ② ★ **这一份把回环画成了虚线，主/环一眼可分**
  （与 R1/R2 恰成对照）。① ★ **`not acceptable` 这条边标签紧贴（接近贴住）`Revise model...` 框的左边框**
  —— 属"标注与框挤在一起"，**判据一条都不报**（`A1` 管的是框与框，不管标签与框）；③④⑤ 同上。

### 一句话（本层最诚实的读法）

**机械层报的是"没按约定的那几条"（宽度 / 图注 / 字体 / 线宽），看图层报的是"读起来顺不顺"
（R1/R2 的回环与主流程同款线型、R3 的一条边标签挤框）—— 两者交集为空。** 本支**没有任何一条看图发现**能被
现有判据看见：`A2`（箭头端点）已降级、也没有"图例 / 线型语义 / 标签拥挤"的判据。**不声称本节穷尽。**

## §8 生成器 · 判据非空泛 · 编译读数 · 不动点

- 本文件的机器部分由 `tests/skills/schematic/make-evidence.py` **当场跑** `check-figure-style.py`
  生成（`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout（§4）。
- **编译读数**（本节末的块）：`make-evidence.py` 把四份产物源码 stage 到仓内 `build/`（gitignored，
  在 D 盘）后**当场重编**，读数 = `rc` · `Overfull \hbox` 计数 · `Output written` 行。
  ★ **PDF 非字节可比**（每次重编带新 `CreationDate`/`ID`）—— 判据基于几何 / 文本读数，不拿字节比。
- ★ **判据非空泛（失败方向的另一条臂）** —— `mutate-figure-style.py` 的读数**逐字取自快照**（**本生成器不执行该驱动器**，故**不声称「当场跑过」**；复跑命令见本节末的 `$ python …` 块），摘其合计段：
  ```text
  MUT: 6/6 达预期（检查器的 `A` 族 M59–M64：4 条必须红 + 2 条**射程边界对照**（`A1` 容差 / `A3` 容差）必须绿）
  MUT: 64/64 达预期（合计）
  ```
  ⇒ 其中 `A` 族 **4 条真红变异 + 2 条必须绿对照**；`F1`–`F6` 的真红变异与其它臂见该驱动器的完整输出。
  ★ **`A4` 的真红变异**证明"线宽不在允许集合里 ⇒ `A4` 真的会红"，所以 §4 里 R1/R2 的 `A4` 红**不是"尺子恒绿/恒红"**。
- **不动点**：在已提交的树上重跑本生成器 ⇒ 本文件**逐字节不变**（证法：跑后 `git status --short` 仍为空；
  见本任务报告）。

```text
$ python tests/skills/schematic/make-evidence.py   # 编译读数（rc · Overfull \hbox · Output written）
R1  rc=0 · Overfull \hbox=0 · Output written on figure.pdf (1 page, 49529 bytes)
R2  rc=0 · Overfull \hbox=0 · Output written on figure.pdf (1 page, 49237 bytes)
R3  rc=0 · Overfull \hbox=0 · Output written on figure.pdf (1 page, 46843 bytes)
G1  rc=0 · Overfull \hbox=0 · Output written on figure.pdf (1 page, 37070 bytes)
```

★ 下面是 **`mutate-figure-style.py` 的快照**（**非生成时现跑**）：首行是**复跑命令**，其余是**该命令的合计段读数**（逐字取自快照）。

```text
$ python tests/skills/figure-choose/mutate-figure-style.py
MUT: 6/6 达预期（检查器的 `A` 族 M59–M64：4 条必须红 + 2 条**射程边界对照**（`A1` 容差 / `A3` 容差）必须绿）
MUT: 64/64 达预期（合计）
```
