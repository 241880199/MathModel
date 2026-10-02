# `tests/m3-table-recon/` —— `mcm-table` 的**侦察快照目录**

本目录是 **2026-10-02 侦察期**的一次性取证现场，不是一套常跑测试。它记录
"在 `mcm-table` 写出来之前，`corpus/**` 里那些 O 奖论文的表格到底长什么样"。

先例：`tests/m3-origin-probe/`、`tests/m3-plot-recon/`、`tests/m3-matlab-recon/`，
本目录照它们的形态建。

**本目录不复述任何规范的"应当值"** —— 数字一律以现场命令的输出为准。

## 头号结论（先看这个）

1. **表要能从 PDF 量出来**：`get_drawings()` 取长横线 → 按左右端对齐分组 ⇒ 表区。
   控制者给的"可行性已实测"（`2200289.pdf` 第 7 页 4 条长横线）本目录**重跑并复核**（`out-1`）。
2. **分母是 164 份论文**，不是"276 份 PDF"、也不是"201 份 `历届优秀论文`"（T1，见下）。
3. **没有正/负控制（`probe_3`）的读数一律降级为"自报"** —— 本目录的控制 **12/12 PASS**。

## 三类文件，纪律不同

| 类别 | 文件 | 纪律 |
| :--- | :--- | :--- |
| **取数库** | `tableprobe.py` | 共享判据（阈值全写死在里面）。改它 = 改探针本身，要留痕、要重跑。 |
| **探针** | `probe_0_inventory.py` · `probe_1_knownfact.py` · `probe_2_corpus.py` · `probe_3_controls.py` | 可运行源码，**只读 `corpus/**`**。 |
| **装配器** | `gen-evidence.py` | 把 `build/` 里的 CRLF 捕获归一化为 LF 并装配 `out-*.txt`。 |
| **输出的捕获** | `out-*.txt` | **逐字 stdout 捕获**（LF）。**手改 = 造伪**。 |

## 复跑（全量 ≈ 4 分 10 秒，主要在 `probe_2`）

```
python tests/m3-table-recon/probe_0_inventory.py  > build/m3-table-recon/raw_probe_0.txt 2>&1
python tests/m3-table-recon/probe_1_knownfact.py  > build/m3-table-recon/raw_probe_1.txt 2>&1
python tests/m3-table-recon/probe_2_corpus.py     > build/m3-table-recon/raw_probe_2.txt 2>/dev/null
python tests/m3-table-recon/probe_3_controls.py   > build/m3-table-recon/raw_probe_3.txt 2>&1
python tests/m3-table-recon/gen-evidence.py
```

**采样口径 = 全量**（276 份，无抽样，无随机种子）⇒ T6 不需要抽样清单。
`probe_2 --papers` 只扫论文层（调试用）。

`probe_3` 会**现画** 12 份 PDF 到 `build/m3-table-recon/controls/`（**不入库**）。

### ★ `probe_2` 那行的 `2>` 口径（2026-10-02 `mcm-table` Task 4 复跑发现 ⇒ 订正）

原文四行**一律**写 `2>&1`。**复跑实测**：`probe_2` 的**进度是写去 stderr 的**（`sys.stderr.write("  ... %d/%d\r")`，
`\r` 无换行），故 `2>&1` 会把 **14 行进度**（`... 20/276` … `260/276`）灌进捕获；`gen-evidence.py`
再把裸 `\r` 归一成 `\n` ⇒ 入库件会比"纯 stdout 捕获"多出这 14 行。
**入库的 `out-2-corpus.txt` 是纯 stdout 捕获**（复跑命令：`python tests/m3-table-recon/probe_2_corpus.py > raw 2>/dev/null`
⇒ 4341 B、逐字节等于 `HEAD`）。另三台探针**不写 stderr**，`2>&1` 无副作用。
⇒ 按本目录自己的定性（见下"`out-*.txt` = **逐字 stdout 捕获**"），`probe_2` 那行**不接 stderr**。
★ 这条属"**自带复核命令的声明**"——照原样跑**复现不出**入库件，故当场订正。

## 关于 `out-*.txt`：**手改 = 造伪**

`out-*.txt` 是某个时点的 stdout 原文。若某份捕获与今天的事实不一致，唯一正确的做法是
**重跑产出它的探针并重新捕获**，**不是**去改里面的字面量。

**实测（2026-10-02）**：四个探针各跑两遍，`raw_probe_{0,1,2,3}.txt` **逐字节不动**（`diff` = 0）。
⇒ 本目录**没有**需要声明的环境量行（唯一"环境味"的是 `out-0` 头部的 `fitz` 版本行，
它随 PyMuPDF 版本变，本机 = `PyMuPDF 1.27.2.3`）。

## ★ 分母（T1）：谁算"论文"

`probe_0` 把 276 份 PDF 逐份过一遍，实测分四类：

| unit | 份数 | 是什么 | 算普及度分母吗 |
| :--- | ---: | :--- | :--- |
| `paper` | **164** | 单册单题 O 奖论文（2022–2025 四个合集） | **是** |
| `volume` | 37 | UMAP 2000–2019 **多篇扫描合集**（96–304 页/册，22 份无文本层） | 否 |
| `problem` | 67 | `官方原题/**` 赛题 | 否 |
| `official` | 8 | `official/**` 官方文档（`20YearsofGoodAdvice.pdf` 等） | 否 |

★ **任务书里的 T1 是对的，而且更深一层**：`历届优秀论文/**` 的 **201** 份里，
**37 份 UMAP 是整册扫描合集（不是单篇论文、且无文本层）**；
若把 201 直接当分母，既混了单元、又把不可量的一批算进分子/分母。

## ★ 已实测的失效边界（**不声称穷尽**）

按"踩到的顺序"列，每条都标了是否已在 `tableprobe.py` 里处置：

| # | 现象 | 实测样本 | 处置 |
| :-- | :--- | :--- | :--- |
| B1 | **页眉/页脚规则线**也是长横线（T2） | `2200289.pdf` p7 的 `y=48.9` 线（页高 0.058） | 页眉带 `0.075·H` / 页脚带 `0.930·H` 外剔除；且单条不成组 |
| B2 | **线画到 MediaBox 之外**（T5） | `2200289.pdf` p7 三条表线 `x1=612.6 > 页宽 595.28`，渲染时被页框裁掉 | 一律**裁剪到页框**再算长度；论文层 580 张里右端被裁的只有 **1** 张 |
| B3 | **两表被并成一张**：中间隔一段正文 | `2207343.pdf` p1（两张三线表，`n` 误成 6） | `_gap_is_prose`（夹缝里有"靠左且够长的正文行"就拆） |
| B4 | **两表被并成一张**：中间只隔一条**居中表题** | `2207343.pdf` p6「Table 2 / Table 3」 | `_gap_has_caption`（夹缝里有 `Table N` 就拆） |
| B5 | **两表被并成一张**：中间只隔一条**表外小标题** | `2200401.pdf` p5（`* Vanilla Grid Strategy`） | `_gap_has_outside_line`（有行起点落在表区左端之外就拆） |
| B6 | **整页水印被抽成一条跨页文本行**，y 中心落进每个夹缝 ⇒ 把每张表都拆碎 | 2025 语料 `校苑数模公众号`（bbox 高可达 447pt） | `text_lines` 按行高上限 `max(3×中位, 30pt)` 剔除 |
| B7 | **竖线按行逐段画**（每段只有一行高）⇒ 整张网格表漏判"有竖线" | `2200401.pdf` p5（6 段 × 15.5pt） | `has_vertical` 先按 x 归并相邻竖段再比阈值 |
| B8 | **整格矩形描边**把同一条横线报两次 ⇒ `n` 翻倍 | `2209812.pdf` p18 的图 | `long_rules` 按 `(x0,x1,y)` 去重 |
| B9 | **表头填充色带**（无描边的色块）被当"竖线" | `2516695.pdf` p10（Table 4/5 深蓝表头） | 只有**描边**矩形才取边；纯填充块**不**当线 |
| B10 | **图框/坐标轴/散点**被当表（T2 主案） | `2209812.pdf` p18（Figure 17 的绘图框 `n=4`） | `kind=figure`：`Figure N` 表题 **或** 区内小图元 > 40 ⇒ 剔除 |
| B11 | **版心被表内文字撑大**（分母错） | `2200289.pdf` p7：粗算 477.76 vs 精算 451.29 | `analyze_page` **两遍**：先用粗版心挑线 → 排除表区文本行 → 再算版心与长度阈值 |
| B18 | **同一条线画了两三笔**（y 相差 <0.2pt）⇒ 凑成"同一 y 上的三条线"，成一个**零高表区** | `2504188.pdf` p11（三条线同在 `y≈129`） | `long_rules` 按 `y` 容差 1.5pt 归并；`group_rules` 再丢弃高 < `MIN_REGION_H`(8pt) 的区 |

**仍未处置 / 已知会错，但如实报告**：

- **B12 跨页续表**：一张表被排版分到两页 ⇒ 会被记成两张表（本侦察**未**合并、**未**量化）。
- **B13 相邻两表之间既无正文、无表题、也无表外行**（例如只隔一个空行）⇒ 仍会并成一张。
- **B14 框起来的算法/伪代码框**：本探针计入"表"。实测**窗内或区内**有 `Algorithm N`
  标题的 = **36 / 580 = 6.2%**（多半是伪代码框）。**这是口径分歧，不是 bug** ——
  其中一部分作者自己就标成 `Table N`（`2504223.pdf` p8 "Table 2: Survival EM Algorithm"），
  另一部分标 `Algorithm N`（`2504188.pdf` p11）。
- **B15 无编号表题**：`CAPTION_RE` 只认 `Table/表 + 编号` ⇒ 未标号的表在读数 3 落到 `none`，
  **不许**把它们硬塞进"上/下"。
- **B16 页眉线低于 0.075·H** 的 PDF 会把页眉线当候选（单条不成组，但若页眉线 + 两条别的线对齐就可能成组）。
- **B17 旋转页**：本语料实测 **0 页**有 `rotation != 0`；若有，探针会**跳过该页**并计数
  （`probe_2` 会打印跳过的份数/页数）。

## 探针速查

| 探针 | 干什么 | 产出 |
| :--- | :--- | :--- |
| `probe_0_inventory.py` | 276 份 PDF 分类（T1 分母）、页数/文本层/尺寸 | `out-0-inventory.txt` |
| `probe_1_knownfact.py` | 重跑控制者那条"已知事实"（`2200289.pdf` p7） | `out-1-knownfact.txt` |
| `probe_2_corpus.py` | 全量扫描 → **六个读数** | `out-2-corpus.txt`（+ `build/.../tables_detail.csv`，**不入库**） |
| `probe_3_controls.py` | ★ T8 正/负控制 12 例 | `out-3-controls.txt` |

## ★ 与 `mcm-table` 落地的关系（2026-10-02 · Task 4 复核）

**前提**：本目录的探针**只读 `corpus/**` 与 `build/**`**，**不读** `.claude/skills/**`
（`grep -rnE "\.claude|skills|mcm-table" tests/m3-table-recon/*.py` 只见 `tableprobe.py` 标题里的一处**文字**，
无任何代码依赖）。⇒ **`mcm-table` 落地不会让本目录的证据过期** —— 这是**先查后量**的结论，不是默认。

**实测（2026-10-02，`mcm-table` Task 4 当场跑）**：四台探针**全部仍可跑**（`rc=0`），
按上面的纯 stdout 配方重跑 ⇒ 四份 `out-*.txt` **逐字节等于 `HEAD`**
（`git status --short` 跑完为空）。⇒ **本目录不新增"冻结的历史"例外段**（与 `m3-matlab-recon` 不同：
那支有两台探针落地后**直接崩**，本支**没有**）。

## 二进制产物

**一份都不入库。** `build/m3-table-recon/controls/*.pdf`、`verify/*.png`、
`tables_detail.csv` 全部可由上面的命令重跑产出（`probe_3` 现画控制页）。
`build/` 已 gitignore。
