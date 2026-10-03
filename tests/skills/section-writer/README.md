# `tests/skills/section-writer/` —— `mcm-section-writer` 的测试侧

**判据本体不在本目录。** 它**随 skill 走**：

```
.claude/skills/mcm-section-writer/check-section.py     ← 判据本体（★ 全仓唯一一份）
```

本仓既有的 `check-*.py` **两种落点都活着**（`mcm-abstract/check-summary.py` 在 skill 目录；
`figure-choose` / `playbook` / `table` / `topic-select` 的在 `tests/`）。本支照 `mcm-abstract` 的先例
**选 skill 目录侧** —— 使用者拿到 skill 就能跑它。⇒ **`tests/` 下不许再写一份"镜像版"**
（两份必然漂移，本仓栽过同型）；驱动器里有一条现取断言盯着这件事（`RUN:` 行的
"`tests/` 下的 `check-section.py` 镜像"）。

本目录现有**驱动器 + 对照证据**：

```
tests/skills/section-writer/
├─ mutate-section-writer.py      # 变异驱动器（调 skill 目录里那份检查器）
├─ make-evidence.py              # 三臂对照证据生成器（Task 3 新建）
├─ SECTIONWRITER-evidence.md     # 由 make-evidence.py 产出（**不许手改**）
├─ green/                        # ★ 带 skill（skill 轮）的产物 + 写手自查单 + 写手跑检查器的原始输出
└─ README.md                     # 本文件
```

---

## 1. 怎么跑

```bash
# ① 变异驱动器：SW1–SW8 逐条证红 + 两条静态自检（SELF1/SELF2）证红 + "必须仍绿"的对照
python tests/skills/section-writer/mutate-section-writer.py

# ② 直接跑检查器
python .claude/skills/mcm-section-writer/check-section.py <节文件> --section <节名> [--input <要点清单>]
python .claude/skills/mcm-section-writer/check-section.py --selfcheck
python .claude/skills/mcm-section-writer/check-section.py --help
```

- **临时件只落仓内 `build/section-writer-mut/`**（gitignored；**不落 C 盘 / `%TEMP%` / 盘根**）。
- 驱动器收尾自证：受保护件逐个 `git hash-object` 未变 · 干净夹具复跑仍全 `PASS` · `git status --short` 为空。

### 1.1 `--section` 的取值（★ **现场取自** `references/sections.md` 的 8 个 `##` 标题）

| § | 节名（**逐字**） |
| :-- | :-- |
| 1 | `问题重述` |
| 2 | `假设及其论证` |
| 3 | `问题的分析` |
| 4 | `模型建立` |
| 5 | `求解与结果` |
| 6 | `灵敏度 / 误差 / 稳定性` |
| 7 | `优缺点` |
| 8 | `结论` |

★ 工具**每次运行都去读 `references/sections.md`**（不是把这张表写死在工具里）——
`references/sections.md` 改了标题，取值表就跟着变。
★ **给不认识的值 ⇒ fail-closed 红**（`FAIL  SECTION` + 退出码非 0，不许静默绿、不许猜）。
★ 取不到 `references/sections.md`（缺文件 / 8 个标题解析不出来）⇒ 同样 **fail-closed**
（"取值表取不到就不许猜"）。

---

## 2. 判据、状态与出处

每行输出形如 `<STATUS> <ID> <标题>  # <说明>`；最后一行 `RESULT: PASS|FAIL`。

| id | 判据 | 状态 | 原始出处 |
| :-- | :-- | :-- | :-- |
| `SW1` | 数字与出处成对（**合取**：有具名外源 ∧ 数字搜不到） | **`FAIL`**（硬） | `judge.md:222-225`（`:223(d)`） |
| `SW2` | 无出处数字须带标注（★ 仅在"有具名外源"时判硬 `FAIL`；无外源 ⇒ `WARN`） | **`FAIL`** / `WARN` | `judge.md:224` |
| `SW3` | 段末总结率 | `WARN` | `judge.md:309`（`≥90%` 且 `≥6` 段） |
| `SW4` | 膨胀比 | `WARN` | 读数出 `judge.md:235`；阈值 `4.0` = 本项目 `[社区]` 口径 |
| `SW5` | 对比式 + 强调式构造密度 | `WARN` | `judge.md:315`（§6.3 P8：`>3‰`） |
| `SW6` | 自评式元话语数 | `WARN` | 读数出 `judge.md:237`；阈值 `2` = 本项目 `[社区]` 口径 |
| `SW7` | 极短断言句 | `WARN` | `judge.md:308`（最短句 `<8` 词且 `≥3` 处；★ 极短句**下界 `2` 词** = 本项目 `[社区]` 口径，判词只给 `<8` 词） |
| `SW8` | 可整体删除而信息量不变的句比 | `WARN` | `judge.md:311`（`≥15%`） |
| `EMPTY` | 本节没有可检正文（**无散文行、无表**；**只有公式行也不够** —— "纯公式行"判法见下）⇒ fail-closed | **`FAIL`**（硬） | 本项目口径（**无对象不许判绿**） |
| `SELF1` | 源码里不得出现四项明令不用的判据（`judge-green.md:202-208`） | `FAIL` | 工具对自己的静态自检 |
| `SELF2` | 工具头部那段"压力臂局限"文字必须在场 | `FAIL` | 同上 |

**状态语义**：

- **硬失败（`FAIL`）只有三处**：`SW1`、`SW2`（★ **`SW2` 仅在"有具名外源"时判死**（与 `SW1` 同一合取口径）；
  **无具名外源**（一张**自算结果表**的常见形态）⇒ 只出 `WARN`）、`EMPTY`（无正文）。
  `SW3`–`SW8` **一律只出"提请复核"（`WARN`），绝不判死**。
- `SKIP` = **无法判定**（不是 PASS，也不是 FAIL）：`--input` 缺失 ⇒ `SW1`/`SW2`/`SW4` 报 `SKIP`；
  真值取不到 ⇒ 词表判据（`SW3`/`SW5`/`SW6`/`SW8`）报 `SKIP`。
- `EMPTY` = **本节没有可检正文（无散文行、无表；"只有公式行"也不够）** ⇒ **fail-closed `FAIL`** ——
  **不许**对"什么都没写"判 `PASS`（那会让"判据在无对象时不算失败"变成恒真）；
  ★ **"只有公式、无散文无表"同样触发**：那种形态下 `SW1`/`SW2` 无表、`SW3`–`SW8` 无可切句
  ⇒ **八条判据一条都检不了**。**一句 4 词的散文（`We use the following.`）仍算正文** ⇒ 不判 `EMPTY`。
  ★ **"纯公式行"的判法**：一行掩掉**块级数学**、再抹掉**行内公式**后，**残留里没有一个字母（中英文均可）**
  ⇒ 判**纯公式行**（不算正文）—— ⇒ `$$ E=mc^2 $$.` 的残留只有 `.` ⇒ **仍判公式行**；
  而 `We obtain $T = 18743$ from the fit.` 残留含字母 ⇒ **仍是正文**（不许误伤）。（同一口径也写在工具头部与 `references/metrics.md`。）
  ★ **数学环境清单不声称穷尽（已知局限）**：工具只认**它列出的**那些环境
  （`equation`/`align`/`alignat`/`flalign`/`gather`/`multline`/`eqnarray`/`displaymath`/`math`/`split`/`cases`/`array`，
  及 `$$…$$` / `\[…\]`）；**自定义 / 未列出的环境可能不被识别** ⇒ 那一行可能被当成正文（**漏判 `EMPTY`**）。
- **退出码**：有 `FAIL` ⇒ **非 0**；只有 `WARN`/`SKIP` ⇒ **0**（`WARN` 会在输出里显眼列出）。
  ★ 把 `WARN` 做成非 0 = 把"提请复核"变成"判死" —— 驱动器里有 6 条变异**同时断言 `WARN` 时退出码 = 0**。

**各判据的口径与四条边界**（同一口径写在工具头部、`references/metrics.md` 与本文件三处，
措辞冲突时以 `references/metrics.md` 为准）：

1. **阈值全是〔判词读数〕** —— 两轮度量脚本**都没落盘** ⇒ 不可复算 ⇒ 只出"提请复核"
   （`judge-green.md:270`：*"0 与 0 之间无法定阈"*）。
2. **词表判据必须先拿真值自测**（`judge.md:238`）：工具**每次运行**都先拿
   `tests/skills/arch-cases/true-S1.md` / `true-S2.md` 跑一遍；命中 ⇒ 输出
   `词表不可用：真值命中 N 处` 并把该项**降级为不可判**，**不得**据此判产物有罪。
3. **压力臂与自由臂必须分别设阈 —— 本工具做不到**（节片段里没有"压力臂"这个概念；
   `out-S2.md` 自由臂 vs `out-S2-p.md` 压力臂是 RED 轮的测法）⇒ 工具**放弃的正是 RED 那一半控制手段**。
   **这是明确局限，不是"已覆盖"。**
4. **明令不用的四项判据一律不出现**（清单与理由见 `references/metrics.md` §边界 4）；
   工具源码里出现其中任一项的**字面**即 `SELF1` 红。

---

## 3. 驱动器打的是什么（**不声称穷尽**）

| id | 变异 | 期望 |
| :-- | :-- | :-- |
| `MUT-SW1` | 表内数字改成写手输入里搜不到的（表题仍挂具名外源 `WHO`、且带 `illustrative` 标注） | `SW1` → `FAIL` |
| `MUT-SW2` | 表题**保留具名外源**（`WHO`）、抹掉 `illustrative` 标注，数字仍搜不到（合取齐备） | `SW1` **和** `SW2` → `FAIL` |
| `MUT-EMPTY` | 空文件（0 字节） | 至少 `FAIL`（`EMPTY`）、退出码非 0 |
| `MUT-HEADONLY` | 只有标题、无正文 | 至少 `FAIL`（`EMPTY`）、退出码非 0 |
| `MUT-FORMULAONLY` | 只有公式（`$$…$$`）、无散文无表 | 至少 `FAIL`（`EMPTY`）、退出码非 0 |
| `MUT-ALIGNATONLY` | 只有 `\begin{alignat}` 环境、无散文无表 | 至少 `FAIL`（`EMPTY`）、退出码非 0 |
| `MUT-FORMULA-PERIOD` | 块级公式后多一个句号（`$$…$$.`） | 至少 `FAIL`（`EMPTY`）、退出码非 0 |
| `MUT-SW3` | 把每一段末尾都补成"评价/格言"句（9 段全中） | `SW3` → `WARN`（且 exit=0） |
| `MUT-SW4` | 灌水膨胀 | `SW4` → `WARN`（且 exit=0） |
| `MUT-SW5` | 塞满 `rather than` | `SW5` → `WARN`（且 exit=0） |
| `MUT-SW6` | 塞自评套话 | `SW6` → `WARN`（且 exit=0） |
| `MUT-SW7` | 连续插入极短断言句 | `SW7` → `WARN`（且 exit=0） |
| `MUT-SW8` | 塞可整句删除的元话语 | `SW8` → `WARN`（且 exit=0） |
| `MUT-SELF1` | 把明令不用的判据（举一项）**字面**写进工具源码副本 | `SELF1` → `FAIL` |
| `MUT-SELF2` | 把工具头部那段"压力臂局限"文字**删掉** | `SELF2` → `FAIL` |
| `CTRL-good-md` / `CTRL-good-tex` | 干净 `.md` / `.tex` 夹具（`.tex` 输入也要能吃） | 无变化（全 `PASS`） |
| `CTRL-prose-edit` | 只改一句普通散文 | 无变化 |
| `CTRL-selfcalc` | ★ 合法**自算结果表**（无外源、无标注串、数字搜不到） | `SW2` → `WARN`（**只提请复核**、exit=0），**不是** `FAIL` |
| `CTRL-few-paras` | 段数 `<6` 时节节段末都写成总结句 | `SW3` **不得**出 `WARN`（`≥6 段` 是门） |
| `CTRL-no-table` | 把表整段删掉 | `SW1`/`SW2` 报 `PASS`（无适用对象）而不是 `FAIL` |
| `CTRL-truth-S1` / `CTRL-truth-S2` | ★ 真值两节 | **`SW3`–`SW8` 不得出 `WARN`** |
| `CTRL-no-input` | 不给 `--input` | `SW1`/`SW2`（+`SW4`）→ `SKIP`，**不许** `PASS` |
| `CTRL-inline-formula-prose` | ★ H2-1 对照：含**行内公式**的散文行（`We obtain $T = 18743$ from the fit.`） | **不得**判 `EMPTY`（残留含字母 ⇒ 仍是正文）、`exit=0` |
| `CTRL-unknown-section` | `--section` 给不认识的值 | fail-closed 红（退出码非 0） |

★ 每条变异的期望**逐条写死**（与基准逐条比对，**恰好**这些状态变了、且变成什么）：
"该红没红"或"顺手带红了别的判据"都会被当场抓出来。判据清单**现取**（不写死条数）。

---

## 4. 已知边界（**不声称穷尽**）

1. ★★ **`SW1`/`SW2` 的硬失败是同一合取口径**（`judge.md:223(d)`）：
   **有具名外源 ∧ 数字搜不到 ∧ 无标注串 ⇒ `FAIL`**（判死）；
   **无具名外源**（一张**自算结果表**的常见形态）⇒ `SW2` **只 `WARN`**，退出码 0 ——
   判词该"提请复核"的情形**不许做成"判死"**。★ `CTRL-selfcalc` 变异盯着这一条。
   "数字搜不到"的判法**有两档**（都只会更严）：① **一个都搜不到**（判词原文口径）；
   ② **过半搜不到**（本工具 `[社区]` 加固，阈值 `0.5`）。
   **为什么必须有②**：实测 `tests/skills/arch-cases/out-S1.md` 那张 WHO 表 10 个数字里，只有 `12`
   能在 `brief-S1.md` 里被搜到 —— 它来自清单标题「要点（**12** 条）」，**不是数据**。
   只按①，这张"编造数据 + 借权威署名"的表会**判绿**（本仓最恨的那种失效）；
   加上②后它判红（`SW1`+`SW2` 双红，`exit≠0`）。
   ★ **这处合取口径的代价（如实记，不是缺陷）**："**无具名外源 ∧ 数字搜不到 ∧ 无标注**"的**编造表**
   由 `FAIL` **降到 `WARN`**（退出码仍 0），且驱动器里**没有红变异专门盯这一档** —— 原 `MUT-SW2` 已改成
   "**保留 `WHO`**"以走双 `FAIL` 路径；该档改由**对照** `CTRL-selfcalc` 盯住"只 `WARN`、退出码 0"
   （对照只能证"该绿"，**证不了"该红"**）。**别把 `WARN` 档读成"判死"**；判词 `:223(d)` 的合取本就是
   "**有具名外源**"才硬失败，此处**忠实判词**。（与 `references/metrics.md` §3 同一口径。）
2. ★ **`SW1`/`SW2` 在真值 `true-S1.md` 上报 `FAIL` —— 这不是误报。** 真值那张 WHO 表的数字
   （40/38/75/…）**确实不在 `brief-S1.md` 里**（`judge.md` §4.1 同记：*"brief 要了表、要了数、没给数"*）。
   ⇒ 真值对照**只断言任务书 E.2 要求的那六条**（`SW3`–`SW8` 不得出 `WARN`），**不**把 `SW1`/`SW2` 纳入断言面。
   ⇒ 使用者须知：**`--input` 按设计 §1 的输入契约收"要点清单 + 已定稿的图表与结果"**
   （契约全文 = **题面 + 哪一节 + 该节要点清单 + 已定稿的图表与结果**；"哪一节"走 `--section`）——
   必须把"已定稿结果"一并带上，否则 `SW1`/`SW2` 会按"无出处"报红。
3. **`SW4` 的分母与判词不同源**：判词的分母是 `true-*` 同内容词数（实测真值上 `true-S1 0.92×` /
   `true-S2 0.46×`），本工具的分母是**写手输入（要点清单）** ⇒ 两边**不同源、不可对齐**
   （判词那三个读数 1.7 / 3.3 / 2.2 与本工具的比值不同量级）；
   本工具只给"同一写手输入下横比"的量。★ 阈值 `4.0` 为本项目 `[社区]` 口径，**不是判词的线**。
4. **`SW3`/`SW7`/`SW8` 是代理量**：段末"评价句"、极短"断言句"、"可整句删除"的判定都靠
   可复核的启发式（线索词 / 词数 / 句首匹配），**不是语义判断**；口径写在全量打印的 detail 行里。
   `SW7` 会把数学残片、图表题注、纯数字行剔出去（否则 PDF 转换件的公式残片会被当成"极短断言句"）。
5. **`.tex` 侧只覆盖 `table`/`tabular` 环境**；散在正文的 `\input` 进来的子文件**不读**（工具只读给定的一份节文件）。
6. **不做**判"这段是不是 AI 生成的"（`judge.md:133` / `:244` / `:240`）；
   **不做**跨节一致性（逐节工具，人工落点在 `references/section-edges.md`）；
   **不做**真实数据压力下的 `纪律 A1`（`judge-green.md:268`）。
7. ★ **`EMPTY` 的"纯公式行"识别不声称穷尽**：工具只认**它列出的**数学环境（见 §2 的 `EMPTY` 条目）；
   **自定义 / 未列出的环境可能不被识别** ⇒ 那一行可能被当成正文（**漏判 `EMPTY`**）。**已知局限。**
8. **本 README 不声称穷尽**：以上是**已知**边界，不是"工具的全部局限清单"。

---

## 5. 三臂对照证据（Task 3 新增；**由生成器产出，不许手改**）

```bash
python tests/skills/section-writer/make-evidence.py      # 产出 SECTIONWRITER-evidence.md
```

**同一把尺** = `.claude/skills/mcm-section-writer/check-section.py`，对**三臂七件产物**逐件跑同一条命令形态
（`--input` 一律指对应那个节的 `brief`）。三臂见 `SECTIONWRITER-evidence.md` §1：

| 臂 | 产物 | 给了什么 | 本任务做什么 |
| :--- | :--- | :--- | :--- |
| **RED** | `arch-cases/out-S1.md` · `out-S2.md` · `out-S2-p.md` | **什么都不给** | **只读，不重跑** |
| **纪律轮** | `arch-cases/out-S1-g.md` · `out-S2-g.md` | `docs/mcm-writing-discipline.md` 一份 | **只读，不重跑** |
| **skill 轮** | `green/out-S1-skill.tex` · `out-S2-skill.tex` | 本 skill 整目录 | **跑它**（两个新起的写手） |

★ **RED 与纪律轮的四件产物逐字冻结** —— 本支**不搬动、不改写、不重跑**（无生成器可重跑）。
★ **`green/` 里写了什么**：`out-S{1,2}-skill.tex`（写手交的 `.tex` 片段）· `out-S{1,2}-skill-selfcheck.md`（按节自查单）·
`writer-run-check-S{1,2}.txt`（写手在**隔离容器**里跑检查器的**原始 stdout**，★ **里面的路径是容器路径**，
仓库里不复现——它只是"写手确实跑过"的存证；权威读数以 `SECTIONWRITER-evidence.md` §4 的当场重跑为准）。
★ **写手是谁**：**本会话新起的两个独立 agent（非 fork、无上下文）**，在**仓外容器** `D:/Projects/_scratch/m2-sw-green/`
里干活，**只看到** `brief-S{1,2}.md` + `case-A-problem.txt` + skill 整目录。
★ **一个已知行为（不是故障）**：隔离容器里**没有 `tests/` 目录** ⇒ 检查器的词表自测（`边界 2`）取不到 `true-*`
⇒ `SW3`/`SW5`/`SW6`/`SW8` 四条**降级为 `SKIP`（不可判）**。这是既定 fail-closed 行为；
**在仓内**（`make-evidence.py` 跑的环境）真值在场 ⇒ 四条**实际执行**（见 `SECTIONWRITER-evidence.md` §4.3）。

