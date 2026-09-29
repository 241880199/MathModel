# `red/` —— RED 基线（**无规范**场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（三份并列）**：本 `README.md` / `writer-self-reports.md` / 上一级的
> `red-green-evidence.md`。它们写明了**判据**（图宽比、彩色主色数、图注形态）与**对照结论**；
> `writer-self-reports.md` 还写明**派发口径**。任何"写手" agent 读过其中**任何一份**，
> 产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：`out-R{n}/make_figure.py`（写手产物）与 `out-R{n}/figure.*` 本身
> 也**不给写手**（它们是别的写手的产物）。派写手时提示词只给**场景 brief 的路径**与
> **产物输出目录**。

## 1. 这是什么

Task 5 的 RED 侧：**同一份场景、同一把尺**下，**没见过规范**的写手产出的图。
与上一级 `green/` 对照：GREEN 侧是**用模块**（`mcmplot`）产出的同场景图。

- **场景（权威副本）**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`。
  本目录**不重复内联**那三份场景 —— 免得造第二份权威。派写手时把它们复制到仓外
  `%TEMP%\m3-t5-red\` 的**逐字节副本**（`cmp` 相同，见 `writer-self-reports.md` 文末）。
- **判据**：`tests/skills/figure-choose/check-figure-style.py`，**一字未改**
  （工作树 blob == `HEAD` blob，见 `red-green-evidence.md` §0）。
- **分母**：`--textwidth-in 6.31`（本仓演示口径），与 GREEN 侧同值。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-R{n}/make_figure.py` | 写手产出的生成脚本（无参可跑、离线、可复算） |
| `out-R{n}/figure.png` · `figure.pdf` | 写手导出的图（两载体） |
| `out-R{n}/caption.txt` | 写手产出的图注文本 |
| `writer-self-reports.md` | 三个写手的**派发提示词与自报**（⚠️ 泄题风险件） |
| `README.md` | 本文件（⚠️ 泄题风险件） |

**对照表与判断层在上一级**：`red-green-evidence.md`
（RED × GREEN 并列红绿表 · 逐判据判词 · 载体敏感性探针 · 判断层）。

**生成器**：`../make-evidence.py`（机器抽取对照表；`write_bytes`、全 LF）。

## 3. RED 之所以是 RED

- 三个写手都是**新起的干净上下文 agent**（**未用 `fork`**）。首条 user 消息 = 一条提示词本身，
  只含**两样**：场景 brief 的路径 + 产物输出目录，末尾一句**隔离句**
  （"Work only from that brief - do not read or write any other file."）。**未给**规范 / 模块 /
  判据 / 先例证据。
- **强度边界（照实）**：写手"只读了那一份 brief"这件事**只有自报、没有沙箱可证**
  （摘要 transcript 的 `.output` 实测 0 字节，无法程序化复核）。能复核的只有"未用 `fork`"
  与"提示词逐字如此"。详见 `writer-self-reports.md` 文首。

## 4. 与 GREEN 的比对口径

同场景（`brief-R{1,2,3}.md`）、同数据（逐字）、同分母（`--textwidth-in 6.31`）、
同一把尺（`check-figure-style.py` 一字不改）。**两载体都出**（PNG 与 PDF），
证据里两个都有。**不许**因为 GREEN 没改善就调判据。
