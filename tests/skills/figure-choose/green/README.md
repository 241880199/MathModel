# `green/` - GREEN 对照件（**读了 skill** 的三个写手的产物）

> ## !! 本目录同样含泄题风险文件，绝不给写手 !!
>
> 与 `red/` 同案：`green-evidence.md` / `green/judge-green.md` / `green-self-reports.md` /
> 本文件都写明了**派发口径与对照结论**。任何"写手" agent 读过其中任何一份，
> 产出的就不再是干净的对照件。**这个点名不是穷举**：`out-G{n}/make_figure.py` 里
> 逐条引着 `H<n>` 编号（= 规范的位置），下表"工具"栏整体也**不给写手**。

## 1. 这是什么

Task 6 的对照实验：**同一份场景、同一把尺**，只放开一个自变量 ——
"写手能不能读 `.claude/skills/mcm-figure-choose/`"。

- **场景**：逐字复用 `red/brief-R{1,2,3}.md`（**权威副本在 `red/`**；
  `green-evidence.md` §0.1 当场证过写手拿到的仓外副本与之逐字节相同）。
  本目录**不重复内联**那三份场景 —— 免得造第二份权威。
- **判据**：`check-figure-style.py`，**一字不改**（工作树 blob == `HEAD` 的 blob，
  见 `green-evidence.md` §0.2），`--textwidth-in 6.31`。
- **写手提示词**：逐字复用 RED 第二轮那一份，**只改隔离句**（RED-2 是
  `Work only from that brief - do not read or write any other file.`；GREEN 改成允许读那一个
  skill 目录、其余仍然禁止）。两版原文并排 + 机器 diff 在 `green-evidence.md` §0.3。
- **隔离**：三份场景**原样搬到仓外**临时目录，每个写手只拿到自己那一份。
- **判者**：独立判者**只读产物**，未参与写作、未读 skill。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-G{1,2,3}/make_figure.py` | 写手产出的生成脚本（无参可跑、离线、可复算） |
| `out-G{1,2,3}/figure.pdf` · `figure.png` | 写手导出的图（PDF 为矢量主产物） |
| `out-G{1,2,3}/caption.txt` | 写手产出的图注文本（**G1 / G3 不由各自脚本再生**；`out-G2/make_figure.py` 确实写了它，见 `green-evidence.md` §8 末的机器扫描） |
| `judge-green.md` | 独立判者的判断层判词（**判者未看任何规范文件**） |
| `green-self-reports.md` | 三个写手 + 判者的**派发提示词与完整自报原文**（逐字节，抢救自仓外 transcript） |
| `rescue-transcripts.py` | 上一条的抢救脚本（记录它从哪来、摘了什么、掩码了几处） |
| `make-evidence.py` | 上一级 `green-evidence.md` 的**生成器**（与证据同目录入库，照 Task 1/2 的规矩） |

**对照表与结论在上一级**：`tests/skills/figure-choose/green-evidence.md`
（RED × GREEN 并列红绿表 · 逐格重算 · 改善/未改善/**无区分力**三类分开 · F2 连续色图闸门 ·
判断层射程 · 偏离登记）。

## 3. 一处必须跟着读的口径

- **F3b 的词数口径已收敛到规范侧**（`green-evidence.md` §6-2）：检查器原先数**整条图注**
  （含 `Figure N:` 那 2 个词），规范 H9 的 12 词上限写的是**去掉标签后的正文**
  （登记在 `references/provenance.md` 的 P-D-c1 —— **不是新发现**）。
  本轮把 F3b 改成 `len(caption_body(cap).split())`，**常量 12 / 17 与 `G-H9-*` 一个没动**：
  GREEN 三份 F3b 由"整条 13 词 FAIL"转成"正文 11 词 PASS"，RED 三份读数一字不变。
  口径改动的回归位 = 新 fixture `caption:7` + 变异 `M42`（见 Task 1 证据件 §3.2 / §4 / §9.2）。
- **PNG 的 `--dpi` 不是载体无关的**（§2.2）：Task 2 Step 3 命令里的 `--dpi` 是**占位符**
  （`--dpi <导出 dpi>`）；字面 `300` 只出现在 `red/red-evidence.md`，因为 RED 三份恰好都导出 300 dpi。
  GREEN 的 R2/R3 是 200 dpi，硬套 300 会给 F1 造成**假红**。两组读数都逐字列出；
  真 dpi 由 `PNG 像素宽 ÷ PDF 页盒宽` 与写手脚本里的 `savefig(..., dpi=N)` 两条证据交叉得出
  （**不读 PNG 的 dpi 元信息** —— 检查器 `:152` 与 `provenance.md:20` 都禁止）。
- **判者通过 ≠ 规范得到背书**（§7-1）：判者提示词里**逐字内嵌的规范规则只有 H6（饼图）那一条**。
