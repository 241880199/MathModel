# `references/format.md` —— 一页备忘录（letter / memo）的体例

**本文件是"体例应当如何"的唯一落点。** 凡**自订项**一律标 **`[社区]`（操作纪律）** + 官方指针；
**只有 ② 匿名落款**标 **`[官方]†`**（它是官方硬规则，不是自订）。

> ★ **两条官方规则（原文见 `corpus/official/MCM-ICM_Tips.txt`）**：
> - `[官方]†` **① 触发**（`:160-162`）：*"Each problem will have different and specific requirements,
>   such as **required memos or letters**, specific solution format, and/or page limits."*
>   ⇒ 官方**只**说"每题有各自要求"，**未**禁止主动写 memo。★ 由它推出的**更严操作纪律** **`[社区]`**：
>   **题面要求了才写**；**没要求就绝不产出**。
> - `[官方]†` **② 匿名落款**（`:239-241`）：*"…be sure not to sign the letter with your name.
>   If you feel as though you need to have a formal closing to such a letter we suggest using:
>   **Sincerely, Team #2000000**."* ⇒ **不得署真名 / 校名 / 机构名 / 地域**。

---

## 1. 逐字形态（一份可直接编译的一页备忘录 `.tex`）

```tex
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\begin{document}

\begin{center}\textbf{MEMORANDUM}\end{center}

\noindent\textbf{To:} <受众，题面点名的那个>\\
\textbf{From:} Team \#<队号>\\
\textbf{Date:} <日期>\\
\textbf{Subject:} <一句话主题>

\medskip
<第 1 段：结论先行 —— 直接给建议 / 结果。>
<第 2 段：支撑 —— 一句话讲清模型给出的证据，不复述公式。>
<第 3 段：行动 / 展望 —— 建议怎么做、什么条件下改。>

Sincerely, Team \#<队号>

\end{document}
```

★ **`From:` 与落款都只用 `Team \#<队号>`**（`[官方]†` ②；`#` 在 LaTeX 源码里写作 `\#`）。
★ **本件是可直接编译的完整文档**（含 `\documentclass`）—— 与论文"节片段"不同：
memo/letter 是**独立成篇**的交付物，`MO3` 要编译它读页数。

## 2. 五条体例（逐条标出处）

| # | 体例 | 标记 | 出处 / 说明 |
| :-- | :-- | :-- | :-- |
| 1 | **一页** | `[社区]` | 官方只给"one-page memo"的**例题**形态（`MCM-directors-overview.txt:247`）与"题面可能有页数限制"（`Tips:160-162`）；"恰好一页"是本项目操作线，由 `MO3` 判 |
| 2 | **受众在文首点名**（`To:` 行 / 首句） | `[社区]` | 面向**题面点名的那个受众**；由 `MO4` 判 |
| 3 | **结论先行**（先建议 / 结果，再支撑） | `[社区]` | 非技术受众件的通行做法；例题口径 *"non-technical letter"*（`MCM-directors-overview.txt:149`） |
| 4 | **不写公式推导长段** | `[社区]` | 同上：这是**非技术**件；推导留在论文正文 |
| 5 | **匿名落款**（`Sincerely, Team #<队号>`） | **`[官方]†`** | `Tips:239-241`，**一票否决类**；由 `MO2` 判 |

★ **"一页 / 文首 / 结论先行 / 不写长推导"是 `[社区]` 操作纪律**；**只有匿名落款是 `[官方]†`**。
★ **例题不等于规则**：`MCM-directors-overview.txt:149` / `:247` 与 `20YearsofGoodAdvice.txt:270`
是**例题形态**，**不是**体例规则 —— 引用时按例题引用。

## 3. 最易栽的点（`[社区]` 操作纪律）

- ★★ **题面没要求就别写**（`[社区]` 操作纪律；由官方① 推出的更严推论）—— 它是**题目特定要求**，不是通用交付物（`MO1`）。
- ★★ **别署名**：真名 / 校名 / 机构名 / 地域**一律不写**（`[官方]†` ②；`MO2`）。
  *"我们学校在……"* 这类**地域**也别出现在落款。
- ★ **别把它写成技术报告**：受众是题面点名的那一方，公式推导留在论文正文（`[社区]`）。

## 4. 与检查侧的关系

- **写作侧** = 本 skill；**检查侧** = `mcm-selfreview` 的 **`自查 A14`（题目特定要求，含"要求的 memo 或 letter"）**。
  ★ 本文件**只给指针、不复述 A14 的判据**（同一句话写两处必有一处忘改）。
- **可机器判的四项**（`MO1–MO4`）见 `check-memo.py`；★ **"检查器 PASS" ≠ "这份备忘录写好了"** ——
  措辞 / 受众适配 / 内容覆盖**仍靠人工**。

★ **本文件不声称穷尽**：以上是**已知**体例与栽点，不是"memo 的全部写法"。
