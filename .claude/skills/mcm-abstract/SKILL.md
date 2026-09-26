---
name: mcm-abstract
description: Use when 需要写或复核美赛 MCM/ICM 的摘要页（Summary Sheet）——正文与结果完成之后定稿摘要、摘要超出一页、摘要页缺题号/占位符没改、摘要里的符号或下标导致 pdflatex 报错、或摘要与正文数字对不上时。Triggers include 摘要、摘要页、summary sheet、abstract、写摘要、摘要超页、摘要编译报错、Problem Chosen 没填、摘要与正文不一致。
---

产出**摘要页**（Summary Sheet）：提交物的**第 1 页**，**占一页**，含官方三栏页眉且题号/队号**填实**。

**使用时刻**（官方原文）：*"You should write the summary **last**… Ensure you plan time after solving your problem to write a comprehensive and articulate summary."*（`corpus/official/instructions.html:1131`）。**摘要吃的是已完成的正文与结果**，不是思路稿。

判据一律以 `corpus/official/INDEX.md` 为准（§2.2 摘要页 · §2.3 页眉/匿名/格式 · §3 冲突 4 年份），引用写指针；证据分级见该文件 §0。骨架基线是 `mcm-latex-format` 的 `assets/mcm-2027-summary.tex`。

## 产出契约（形式）

1. **三栏页眉齐全且填实**：`Problem Chosen` = 题号（**不得留 `ABCDEF`**，§2.2.9）· `Summary Sheet` 年份 = 2027（§3 冲突 4）· `Team Control Number` = 队号（不得留 `1111111`）。
2. **摘要页不编号**；页码自正文起算（模板已如此，勿改）。
3. 英文、字体 ≥12pt（§2.2.3/§2.3.5）；**摘要页同样匿名**——§2.3.2 的"任何一页"包含它。
4. **占一页**：自检口径 = 只含摘要的 `.tex` 用 pdfLaTeX 编译后 `page_count == 1`（`[社区]`；官方原文只规定"必须是第 1 页"与 *concise*）。
5. **产物是 LaTeX 源码**，不是 markdown 散文：自检见下节。

## 质量与措辞（15 条自查清单）

**工具只管形式**（页数 / 页眉三栏 / 机械错误）；**它给 `RESULT: PASS` 不代表摘要可交付**——一份"数字是编的 + 引言逐字搬"的摘要同样能拿到 `PASS`。

⇒ 写完摘要页后，**逐条打勾**清单在 **`references/quality-checklist.md`**（8 个 ★＝实测有基线失败过 / 7 条规格，每条都带「怎么查」的具体动作）。**必过**，不是可选。

## 必须自检（可机器执行）

> **工具只判形式**（页数 / 页眉三栏 / 机械错误）；**它给 `RESULT: PASS` 不代表摘要可交付** ——
> 一份"数字是编的 + 引言逐字搬"的摘要同样能拿到 `PASS`。**内容、措辞、取舍一律由上一节的自查清单人工逐条打勾。**

```
python check-summary.py summary.tex
```

用 **pdfLaTeX** 编两遍 → 报**页数**（超页给"要砍多少字"的估算与硬下界）· 从**编译出的 PDF 第 1 页**核三栏页眉与题号/队号/年份 · 扫描并**必须为 0**：未转义 `%`（**静默吞掉整行**）· 裸 `_`/`^` · markdown（`**`、行首 `#`、管道表）· HTML（`<sub>`）· **裸 `|`**（渲染成破折号）· **裸 `~`**（作"约"讲时会消失，见下）· 另列非 ASCII 字符（本机实测 `—` `·` `×` 可用、`σ η μ ≈` 必须改写）。产出 PDF 路径 ⇒ **用 Read 直接看那一页**。

- **`%` 有一处已知漏报（本工具抓不到，故这一步不可省）**：`95 %`（数字与 `%` **之间有空格**）与 `95%` 一样会**静默吞掉整行剩余内容**（实测两者都吞掉 128 字符），但工具的判据（`%` 紧贴前一字符）抓不到前者 ⇒ **抓它靠的就是「亲眼看那一页」这一步**。所以这一步是**必做项，不是可选项**。（取舍理由见 `check-summary.py` docstring「C1 的判据」；实测见 `tests/skills/abs-green-evidence.md` §7.3。）
- **「亲眼看那一页」怎么执行（本机实测的坑）**：**本机 `Read` 直接读 PDF 会报 `pdftoppm is not installed`**（缺 poppler）⇒ 先把第 1 页渲染成 PNG 再 Read 那张图：
  ```
  python -c "import fitz;d=fitz.open('summary-check.pdf');d[0].get_pixmap(dpi=150).save('summary-p1.png')"
  ```
  然后 `Read` 那个 PNG。（装了 poppler 的机器可以直接 `Read` PDF、用 `pages:` 指定页。）**看到的三件事**：三栏页眉填实、页面上没有半句话被吃掉、末行到栏底留了余量。
- **`~` 的判据**：`~` 只在"**其前是空白（或行首） 且 其后是数字**"时计违规（`~48%` 这种把"约"写成 `~` 的形态，`~` 在页面上会消失、语义被改）。**作"约"讲时应写 `$\sim$`**（那才是数学符号）；`Fig.~1`、`12~pt`、`Dr.~Smith` 这类**合法不断行空格可以保留**，工具只把它们计入 `C6b_不断行空格_不计违规`。（四例实测见同文件 §7.2。）

**可重放性**：**可比的是本工具的报告**（同机同 TeX 版本同输入下逐行相同）；**PDF 文件本身不可比**——每次重编都带新的 `/CreationDate`/`/ModDate`/`/ID`（实测输入 `tests/skills/abs-cases/green/G1.tex`：两遍都是 **141,949 字节**、相差仅 **58 字节**，排版几何完全一致；相差字节数随当次时间戳的位数浮动，别拿它当常数）。报告里的页数/填充率以**本机编译**为准，最终以你提交那次编译为准（同 `mcm-latex-format` 的口径）。

**字数口径**：本文件与随附工具都是中文源码，**报字节数或汉字数，不用 `wc -w`** —— `wc -w` 按空白分词，中文会被严重低估。

**拼装契约（GREEN 实测两路都撞到，务必照做）**：本 skill 的产物是**只含摘要页、可独立编译**的文件（这样才能自检"恰好一页"）⇒ **它不含**官方模板摘要之后的尾段。**把它拼进全文时，必须把模板尾段还原**：`\clearpage` / `\pagestyle{fancy}` / `\setcounter{page}{1}` / `\rhead{Page \thepage}` / `Begin your paper here`——**那是"摘要页不编号、页码从正文第 1 页起算"的机制**（`mcm-latex-format` 规则 4）。别把只含摘要的文件当整篇论文提交。

**REQUIRED SUB-SKILL**：`mcm-latex-format`（骨架、编译口径、年份冲突）；交稿前用 `mcm-selfreview`。
