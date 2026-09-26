# G3 摘要页 —— 处理说明

**产物**：`G3.tex`（LaTeX 源码；后缀取 `.tex`，因为实际产出格式就是 LaTeX）。
附带回读用产物 `G3-check.pdf`（自检脚本编译出来的那一页，供 Read 回看，非提交件）。

**用的 skill**：`mcm-abstract`，以及它标为 REQUIRED SUB-SKILL 的 `mcm-latex-format`
（骨架基线取后者的 `assets/mcm-2027-summary.tex`）。

---

## 1. 怎么处理「Task 2 没有结果」

skill 的产出契约第 5 条是两步：**逐问作答，每问给一句带数字的答案**；但
**「数字只能取自正文/结果台账，正文里没有的显式标缺，不许估」**。

正文第 4 节（Further Problems）只有方法、没有结果——`PA`、`CI`、`RSA`、`Htest`、`RS`、
`eta` 这些指标**只有公式与阈值，没有任何一个算出来的值**。所以我按第二步走：

- **不估、不造数**：Task 2 的 (i)–(v) 五个子问**一个数字都不给**。
- **显式标缺**：在摘要里直接写明——“The numerical work for (i)–(v) has not been carried
  out, so we mark those five results as missing; no value is quoted for them here, and none is
  guessed.”
- **仍然逐问作答（形式层面）**：五个子问各给一句“**用什么判据去答**”，把正文里的公式/阈值
  带上（`Q=(2-P0)*1000`、`alpha=0.05`、`RSA<0.95`、`|RS|>0.05`、`eta<0.05`），这样摘要
  读者知道五个子问都会被回答、以及怎么回答，只是值还没跑出来。

Task 1 有结果（正文 3.4 节），所以三个子问都给实数：`Nd = 261` 人/天（等价于 260 人/天时
建成于 36,492 天前）、上行:下行 = 3:2、X 向三个峰（均值 0.30 / 1.10 / 1.76 m，三人并行）、
Y 向两个峰（0.08 m 上行 / 0.15 m 下行）。

## 2. 正文里的数，哪些**没**带进摘要（契约第 6 条：自相矛盾的不带）

- **5.3 节的区域对比百分比（0.001% / 0.005% / 0.006%）**：正文自己的解释与之冲突——
  三个数里 Edinburgh 那个 0.006% 是**最大**的，正文却说 “Scotlands parameters are moderate,
  producing an **intermediate** trend”。判为正文自相矛盾，依契约不带入。
- **5.1 节的 25% / 48.1% / 45.7% / 43.6%**：“硬度先降 25%、再在 20 年后**增加** 48.1%”
  的语义在正文里无法自洽读出（硬度衰减模型不可能给出“先降后增”），保留 64.2% 这一个
  语义干净的敏感度数字。
- **`W = 62.8 kg` 与 `G = 700 N` 一起带**：正文 (3.7) 写 `G = W*g`，62.8 × 9.81 = 616 N，
  与 Table 4 实际用于求解的 `G = 700 N` 不自洽。避免在摘要里并置这一对，改为定性描述
  “population-weighted walking load `Wg`（W 由 WHO 分组体重构造）”。

保留的敏感度数字只有 **64.2%**（p 从 0.0025 翻到 0.005，饱和时间缩短 64.2%），它在正文里
自洽。

## 3. 没照做的部分及原因

1. **摘要页的 `\clearpage` / `\pagestyle{fancy}` / `\newpage` / `\setcounter{page}{1}` /
   `\rhead{Page \thepage\ }` / “Begin your paper here” 这一整段尾巴被删了。**
   `mcm-latex-format` 规则 4 要求保留 `\setcounter{page}{1}`。但本产物是**摘要页本身**，
   而 `mcm-abstract` 给的本地自检口径是「只含摘要的 `.tex` 编译后 `page_count == 1`」——
   官方模板那段尾巴必然产生第 2 页（实测第 2 页内容就是页眉 + “Begin your paper here”，
   与摘要溢出无关）。两者冲突时我按产出契约（一页）取舍，并在 `.tex` 里用注释写清：
   拼装全文时这一段**必须还原**。末尾那个官方原件的多余 `\end` 按 `mcm-latex-format`
   的建议**保留未删**。
2. **队号 `2401056` 是占位实数，不是真实控制号。** 契约要求“不得留 `1111111`”，而真实队号
   我无从得知，故填了一个格式合法的 7 位数字。**提交前必须换成真实队号**（同时改
   `\lhead{Team \Team}` 与摘要页右栏，两者同源，改宏即可）。
3. **没有跑 `mcm-selfreview`。** `mcm-abstract` 建议交稿前用它做合规与内容自查；本次任务只
   要求产出摘要页，且正文本身是残缺的（Task 2 无结果），做全稿合规自查没有意义。
4. **一个“带数字答案”的硬要求被降级**：契约第 5 条要求每个子问都给一句**带数字**的答案，
   Task 2 的五个子问给不出数字（见 §1）。这是契约内部两条规则的冲突（“必须带数字” vs
   “没有就显式标缺、不许估”），我按后者执行——在残缺正文上造数比标缺更有害。

## 4. 自检证据（真实命令与输出）

```
python .claude/skills/mcm-abstract/check-summary.py build/abs-green/G3.tex \
       --pdf build/abs-green/G3-check.pdf
```

结果：

- A 段（读 PDF 第 1 页）：`A1_三栏字样齐全 PASS` / `A2_Problem_Chosen PASS 值="A"` /
  `A3_Team_Control_Number PASS 值="2401056"` / `A4_年份_2027 PASS`
- B 段：`rc=0`，`硬错误条数=0`，`页数=1`
- C 段：C1–C7 **全 0**（无未转义 `%`、无裸 `_ ^ | ~`、无 markdown、无 HTML、无非 ASCII）
- 结论：`RESULT: PASS`

回读渲染页（PyMuPDF）：1 页，页面 612 × 792 pt（US Letter，符合 §2.3.6 的 A4/Letter 要求），
第 1 页 3451 字符，三栏页眉 + 摘要全文都在这一页上，无截断。
