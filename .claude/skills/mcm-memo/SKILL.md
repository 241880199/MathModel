---
name: mcm-memo
description: Use when **题面明确要求 letter/memo（备忘录）**时要起草或复核一份面向指定受众的一页备忘录（letter / memo）。★ **题面没要求就绝不产出**（`[社区]` 操作纪律）—— 它是**题目特定要求**，不是通用交付物。Triggers include 写备忘录、写memo、备忘录、letter、memo、给某个机构的一封信、letter to、memo to、one-page memo、非技术性信件。
---

# mcm-memo —— 题面要求 letter/memo 时的写作范式

**只回答一件事**：当**题面明确要求** letter/memo 时，产出一份**面向指定受众的一页备忘录 `.tex`**。

★★ **它不是通用交付物** —— **题面没要求就绝不产出**（★ **`[社区]` 操作纪律**；由官方① `MCM-ICM_Tips.txt:160-162` 推出的**更严推论**：官方*只*说 *"Each problem will have different and specific requirements, such as **required memos or letters**, specific solution format, and/or page limits."*，**未**禁止主动写 memo）。这一点写死在 `description` 里，是本 skill 最容易误触发的点。

## 什么时候用 / 不用

**用**：题面**明写**要一封 memo / letter（例如 *"one-page memo to …"* / *"non-technical letter for …"*）时。

**不用（边界，逐条写死）**：
- **题面没要求 letter/memo** ⇒ **不产出**（`[社区]` 操作纪律；本 skill 的第一条，见上）；
- **写论文的某一节正文** ⇒ `mcm-section-writer`（本 skill **不抢它的触发词**）；
- **排版 / 骨架 / 页眉 / `\documentclass`** ⇒ `mcm-latex-format`（本 skill **不抢它的触发词**）；
- **全稿提交前合规** ⇒ `mcm-selfreview`；
- **出图 / 表 / 示意图** ⇒ M3 的绘图类 skill。

## 两条官方规则（★ 仅见于 `corpus/official/MCM-ICM_Tips.txt`，两条都标 `[官方]†`）

1. `[官方]†` **① 触发**（`MCM-ICM_Tips.txt:160-162`）：题目会有**各自不同的特定要求**
   （**required memos or letters** / 特定解法格式 / 页数限制）⇒ **先读题面**（这句是官方的）。
   ★ 由此推出的操作纪律 **`[社区]`**：**要求了才写**；**没要求就绝不产出**。
2. `[官方]†` **② 匿名落款**（`MCM-ICM_Tips.txt:239-241`，**一票否决类**）：
   *"Do not include any type of team identification such as student names, institution name or
   geographical region. If you are required to include a letter with your submission, be sure not to
   sign the letter with your name. If you feel as though you need to have a formal closing to such a
   letter we suggest using: **Sincerely, Team #2000000**."*
   ⇒ ★★ **不得署真名 / 校名 / 机构名 / 地域**；要正式收尾就用官方建议写法
   `Sincerely, Team #<队号>`。**漏了这条，本 skill 会把队伍引向在 letter 上署真名。**

★ 凡"**体例应当如何**"的自订项（下节与 `references/format.md`）一律标 **`[社区]`（操作纪律）** + 官方指针，
**不标 `[官方]`** —— 官方**没有**"memo 该有哪几段"这类体例规则。

## 体例（`[社区]` 操作纪律 + 官方指针；逐字形态见 `references/format.md`）

- **一页**（`[社区]`）—— 官方只给**官方建议写法**与"one-page memo"的**例题**形态；
- **受众在文首点名**（`To:` 行 / 首句）—— 面向题面点名的那个受众；
- **结论先行**：先给建议 / 结果，再给支撑；
- **不写公式推导长段**：这是**非技术**受众件（例题口径 *"non-technical letter"*）；
- **匿名落款**（★ 这一条**不是** `[社区]`，是 `[官方]†` ②）。

## 输入契约（缺一样就先向用户要）

1. **题面**（判"要不要写"与"写给谁"的燃料）；
2. **受众**（题面点名的那一个）；
3. **要传达的建议 / 结果**（来自论文正文的**已定稿**结果，不是让本 skill 重算）。

## 输出契约

一份**可直接编译的一页备忘录 `.tex`**（含 `\documentclass`；见 `references/format.md`）。

## 检查器（可机器执行；`check-memo.py`，判据 `MO1–MO4`）

```
python check-memo.py <memo.tex> [--problem <题面>]
```

- `MO1` 触发条件在场 · `MO2` 匿名落款 · `MO3` 恰好一页 · `MO4` 受众在文首点名。
- ★ **四条都是硬失败（`FAIL`）**；**缺 `--problem` ⇒ `MO1`/`MO4` 报"无法判定"（`SKIP`），
  不许报 `PASS`**；无 `pdflatex` ⇒ `MO3` `SKIP`。
- ★ **"检查器 PASS" ≠ "这份备忘录写好了"** —— 它只判这四项形式；**措辞 / 受众适配 / 内容覆盖
  仍靠人工**（同 `mcm-abstract` 的口径：工具只判形式）。

## 与 `mcm-selfreview` 的关系（★ 只给指针、不复述）

`mcm-selfreview` 的 **`自查 A14`（题目特定要求，含"要求的 memo 或 letter"）** 是**它的检查侧**。
本 skill 是**它的写作侧** —— ★ **A14 的判据只在 `mcm-selfreview`，本 skill 不复述**（同一句话写两处必有一处忘改）。

## 指针（唯一权威）

- **一页备忘录的体例（逐字形态）**：`references/format.md`。
- **两条官方规则的原文**：`corpus/official/MCM-ICM_Tips.txt:160-162` · `:239-241`。
- **写作纪律的唯一权威表述**（14 条，三层有序）：`docs/mcm-writing-discipline.md` —— 本 skill 只给指针、不复述规则原文。
- **题目特定要求的检查侧**（含 memo/letter）：`.claude/skills/mcm-selfreview/SKILL.md` 的 `自查 A14`。
