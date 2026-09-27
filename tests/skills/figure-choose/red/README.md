# `red/` - RED 基线（无 skill 场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（四份并列，没有"次要"档）**：`red-evidence.md` / `judge.md` / `README.md` /
> **`writer-self-reports.md`**。它们写明了**期望的失败形态**（图宽比、配色数、图注形态、
> 饼图那条规则）；其中 `writer-self-reports.md` 是**最完整**的一份 —— 它逐字含写手对
> 规范表（H1-H13）的引述，以及"这些阈值我都知道"的自述。任何"写手" agent 一旦读到
> 其中**任何一份**，产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：第 2 节的**"证据"与"工具"两栏整体同样不给写手**，
> 派写手时提示词只给**场景 brief 的路径**与**产物输出目录**。

## 1. 三份场景正文（Task 6 的 GREEN 必须逐字复用同一份，不许改写）

下面三节是 `brief-R1.md` / `brief-R2.md` / `brief-R3.md` 的**逐字**内联副本
（脚本从这三个文件的字节直接读入，不经过改写）。**权威副本是那三个文件**；
若本文件与它们不一致，以文件为准。

### 场景 R1（构成数据） —— 逐字内联自 `brief-R1.md`

````markdown
# Brief R1 - district vulnerability composition

A regional risk assessment divides a study area into six districts (A-F). For each
district, the share of its land area falling into each of three vulnerability tiers
(low, medium, high) has been measured. Within every district the three shares sum to
1.00.

| District | low  | medium | high |
|----------|------|--------|------|
| A        | 0.42 | 0.35   | 0.23 |
| B        | 0.31 | 0.44   | 0.25 |
| C        | 0.55 | 0.30   | 0.15 |
| D        | 0.28 | 0.47   | 0.25 |
| E        | 0.37 | 0.38   | 0.25 |
| F        | 0.50 | 0.33   | 0.17 |

Question to answer with the figure: describe the vulnerability composition of each
district, and support a judgement about which two districts have the most similar
structure.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
````

### 场景 R2（多变量对比 / 相关） —— 逐字内联自 `brief-R2.md`

````markdown
# Brief R2 - drivers of historical disaster counts

A regional risk assessment divides a study area into six districts (A-F). Five
attributes have been measured for each district.

| District | Population density (people/km2) | Mean slope (degrees) | Vegetation cover (fraction of area) | Historical disaster count | Infrastructure index (0-100) |
|----------|--------------------------------|----------------------|-------------------------------------|---------------------------|------------------------------|
| A        | 820                            | 3.2                  | 0.61                                | 12                        | 74                           |
| B        | 640                            | 11.5                 | 0.58                                | 31                        | 72                           |
| C        | 610                            | 2.4                  | 0.72                                | 8                         | 81                           |
| D        | 1210                           | 14.8                 | 0.41                                | 38                        | 55                           |
| E        | 990                            | 7.1                  | 0.49                                | 16                        | 66                           |
| F        | 1750                           | 5.0                  | 0.55                                | 24                        | 70                           |

Question to answer with the figure: identify which factor is most strongly correlated
with the historical disaster count, and describe the similarity between districts.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
````

### 场景 R3（交付形态） —— 逐字内联自 `brief-R3.md`

````markdown
# Brief R3 - district vulnerability composition, paper-ready

A regional risk assessment divides a study area into six districts (A-F). For each
district, the share of its land area falling into each of three vulnerability tiers
(low, medium, high) has been measured. Within every district the three shares sum to
1.00.

| District | low  | medium | high |
|----------|------|--------|------|
| A        | 0.42 | 0.35   | 0.23 |
| B        | 0.31 | 0.44   | 0.25 |
| C        | 0.55 | 0.30   | 0.15 |
| D        | 0.28 | 0.47   | 0.25 |
| E        | 0.37 | 0.38   | 0.25 |
| F        | 0.50 | 0.33   | 0.17 |

Question to answer with the figure: describe the vulnerability composition of each
district, and support a judgement about which two districts have the most similar
structure. I need one figure (with its caption) that I can paste straight into the
body text of my paper.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
````

## 2. 目录内容

**场景（只给写手的东西）**

| 路径 | 是什么 |
| :--- | :--- |
| `brief-R{1,2,3}.md` | 场景正文。**权威副本**。 |
| `out-R{1,2,3}/make_figure.py` | 写手产出的生成脚本（无参可跑、离线、可复算） |
| `out-R{1,2,3}/figure.pdf` · `figure.png` | 写手导出的图（PDF 为矢量主产物，PNG 为同源栅格） |
| `out-R{1,2,3}/caption.txt` | 写手产出的图注文本（**不由脚本再生**，见 `red-evidence.md` §7） |

**证据（⚠️ 与文首点名的泄题件同类 —— 这一栏整体不给写手，不只是被点名的那几份）**

| 路径 | 是什么 |
| :--- | :--- |
| `red-evidence.md` | 机械层逐字读数 + 红绿表 + 两条遗留风险的实测回答 + 修复记录 |
| `judge.md` | 独立判者的判断层判词（**判者未看任何规范文件**） |
| `writer-self-reports.md` | 六个写手 + 判者的**派发提示词与完整自报原文**（逐字节，抢救自仓外 transcript）。**⚠️ 本栏泄题风险最高的一份**：写手自报里逐字引了规范表（H1-H13）并写明"按这些阈值选的" |
| `f2-boxes.txt` | F2 全量色箱取证输出（341 行；由 `f2-diagnose.py --out` 用 `write_bytes` 落盘，可逐字节复现） |
| `multipage-probe.pdf` | §6"只判第 1 页"的两页探针（由 `make-multipage-probe.py` 生成，1923 B） |
| `truth.py` | 场景地面真值（R1 的 L1 相似度排序 / R2 的相关系数） |

**工具（造上面那些证据的脚本 —— 放在这里，不放 gitignored 的 `.superpowers/`）**
（⚠️ 这些脚本也**不给写手**：`f2-diagnose.py` 直接 import 检查器，等于把阈值常量摆出来）

| 路径 | 是什么 |
| :--- | :--- |
| `f2-diagnose.py` | F2 每个色箱占比的取证工具。**import** `check-figure-style.py` 的 `raster_rgb`/`color_count`（不抄），并对重写的取箱步骤做逐例一致性断言 |
| `verify-reproducible.py` | §7"逐字节重生成"：把 `make_figure.py` 单独复制到仓外跑，再与 `HEAD:` 的 blob 比 |
| `make-multipage-probe.py` | 生成 `multipage-probe.pdf`（固定 CreationDate，可重复生成） |
| `rescue-transcripts.py` | 从仓外 transcript 摘出 `writer-self-reports.md` 的那个一次性脚本 |
| `make-briefs.py` · `make-readme.py` · `make-evidence.py` | 生成 `brief-R*.md` · 本文件 · `red-evidence.md` |

## 3. 两层判据的分工（本目录要留的现场证据）

- **机械层**（`check-figure-style.py`）：F1 图宽比 · F2 彩色主色数 · F3a-d 图注形态。
  可判、可复算、**一字不改**地两边同用。
- **判断层**（独立判者）：图型选得对不对 —— **机械层抓不到这一层**。
  典型反例：饼图也常常 <=4 色，F2 会放它过去；而"构成数据不该用饼图"是判断题。
  **本目录的 `judge.md` 就是这一层的现场证据。**
- **⚠️ 两层都不管的一层**：**"图里每个几何元素都画对了没有"**。
  现场反例：`out-R1/make_figure.py:174-178` 把三族网格线里的两族算成了同一个数组
  （一族从未画出、一族画了两遍），**机械层与判断层都没有报它**（详见 `red-evidence.md` §4-3 / §8 形态 8）。
  **不许把"两层都判过了"读成"这张图没问题"。**
- **⚠️ 隔离强度的边界**：写手"只读了那一份 brief"这件事**只有自报、没有沙箱可证**；
  能复核的只有"未给它们继承的上下文"（⇒ 未用 `fork`，实测首条 user 消息就是那一条提示词）。
  详见 `red-evidence.md` §0.1 与 `writer-self-reports.md` 顶部。

## 4. 与 GREEN 的比对口径

Task 6 用**同一份场景**（第 1 节逐字复用）、**同一把尺**（`check-figure-style.py`
一字不改、同一 `--textwidth-in 6.31`）跑 GREEN，再做 RED/GREEN 并列红绿表。
**不许**因为 GREEN 没改善就调判据。
