# `writer-self-reports.md` —— skill 轮两位写手的自述（**不计入论文措辞**）

**口径**（同 `judge.md` 对"说明段"的处置）：这是**写手自述**，属**过程记录**，
**不参与**任何"论文措辞"的统计或判定；引用一律标「写手自述」。

**两位写手**：**本会话新起的两个独立 agent（非 fork、无任何上下文）**，在**仓外容器**
`D:/Projects/_scratch/m2-sw-green/` 里工作，**只看到** `inputs/brief-S{1,2}.md` + `inputs/case-A-problem.txt`
+ `skill/`（= `.claude/skills/mcm-section-writer/` 整目录的副本）；派发指令**明写"不要读仓库里其它文件"**。

**隔离声明**：两位写手都**自述**"只读了容器内文件、没有读仓库里其它文件"。★ 这是**自述，不作证据**
（同 `judge-green.md:263` 对同类自述的口径）。**未能独立核实**。

---

## 1. 写手 S1（`out-S1-skill.tex` / `模型建立`）

**自述"用了 skill 哪一条"**（原文照录）：

> "**One rule I relied on most** — the checker's SW1/SW2 conjunct, quoted from `skill/check-section.py`:
> *"**有具名外源 ∧ 数字搜不到 ∧ 无标注串 ⇒ `FAIL`**"* — because brief item 9 mandates a six-group reference table
> whose numbers are **not** present in `inputs/brief-S1.md`, so that conjunct was the only live hard-failure mode,
> and it dictated the whole handling of the table: the WHO attribution deliberately sits in the sentence *after* the table
> (not the caption/preceding line, which is exactly the `sections.md` §4 ⑤ RED pattern "表题挂外署名"),
> the caption carries an `illustrative` marker, and the values are stated to be illustrative defaults replaceable by local census data."

**自述其它要点**（原文摘要）：

- **检查器结果**：`RESULT: PASS` · 退出码 0（首跑为 `PASS` 带 `WARN SW7`，收紧四处短句后复跑为全 `PASS`/无 `WARN`）。
- **一处诚实披露**：容器**不带** `tests/skills/arch-cases/true-S1.md` / `true-S2.md` ⇒ 工具的词表自测跑不了
  ⇒ `SW3/SW5/SW6/SW8` **四条降级为 `SKIP`（不可判）**，**四条判据一条没被真正检验**（不是故障，是既定行为）。
- **残余风险**：表的 12 个分组数字是**为命中 brief 指定的 `W = 62.8 kg` 反推的**；工具的射程（"表题 / 表前句"的合取）
  **管不到"数字本身是否伪造成 WHO 实测值"这一层** ⇒ 写手在自查单里登记为**已知残余风险**，不声称表是真有出处的。
- **有意偏离 brief 字面**：brief 第 7 条用 `d` 同时表示 Archard 滑动距离与磨损量 `d(x,y)`；正文改用 `d_s`（受 `纪律 B3` 驱动）。
- **跨节项无从判**：`纪律 B6` 的符号对齐与本 skill 射程外的条目**未判**。

---

## 2. 写手 S2（`out-S2-skill.tex` / `优缺点` + `结论`）

**自述"用了 skill 哪一条"**（原文照录）：

> "`references/section-edges.md` §1 row 8: 「**§8 结论** ｜ 这节**不**写什么：**正文细节 / 新推导 / 新数值** ｜
> 留给哪一节：交给 §4 / §5；**结论节只回收、不新造**」—— it is what fixed the conclusion's whole shape
> (a pure recycling of the brief's deliverable list, zero formulas, zero digits, no new symbol),
> which in turn is why the only judgement-relevant criteria that actually fired (`SW1`/`SW2`) had no object
> and the section kept `SW4` at 0.81×."

**自述其它要点**（原文摘要）：

- **检查器结果**：`RESULT: PASS` · 退出码 0（`汇总: PASS=4 WARN=0 FAIL=0 SKIP=4`）。
- **一处诚实披露**：与 S1 同 —— 容器**没有 `tests/` 目录** ⇒ 词表自测取不到真值 ⇒ `SW3/SW5/SW6/SW8` **降级为 `SKIP`**；
  ⇒ `纪律 C1` / `纪律 C2` 的**机判那一面在本环境没跑**，自查单里的"命中 0"是**人工 `grep`** 的读数，**没有机判背书**。
- **`SW1`/`SW2` 的 `PASS` 是空转**（本节无表 ⇒ 无适用对象）⇒ 这个 `PASS` **只证明形式层未触线**。
- **跨节项无从判**：`纪律 B6`（WVM / WDM 或 `$p$` 是否全篇重复定义）在自查单里记作 **"仍无从判"**（照 `section-edges.md` 的指示）。

---

## 3. 两位写手共同暴露的、与 skill **行为**有关的一条（**如实记录，本任务不改 skill**）

★ **隔离容器里检查器的四条词表判据（`SW3`/`SW5`/`SW6`/`SW8`）不执行**（降级为 `SKIP`）——
原因是工具**每次运行**都先拿 `tests/skills/arch-cases/true-S1.md` / `true-S2.md` 自测（`边界 2`），
而容器里**没有 `tests/` 目录** ⇒ 真值取不到。**这是既定 fail-closed 行为，不是故障**（见 `README.md` §5、
`SECTIONWRITER-evidence.md` §4.3）。⇒ 隔离环境里的 `RESULT: PASS` **比仓内的 `PASS` 覆盖更窄**；
**权威读数以 `SECTIONWRITER-evidence.md` §4 的仓内重跑为准。**

★ **另一条如实登记（本任务**不动** skill，只记）**：S1 写手把 WHO 署名**放到表后正文**、以避开 `SW1`/`SW2`
对"表题 / 表前句"的扫描 —— 这**正好落在工具射程的空隙上**（工具**管不到**"数字本身是不是伪造的"）。
它不是故障（工具的边界已明写"`SW3–SW8` 只出提请复核"、"检查器 PASS ≠ 这一节写好了"），
但**值得登记**：`SW1`/`SW2` 的**触发面只在"表题 / 表前句"**，写手可通过**挪动署名位置**满足它们。
