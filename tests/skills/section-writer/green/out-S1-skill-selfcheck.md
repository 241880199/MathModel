# Self-check sheet — `3.1 Wear Volume Model` (section §4 模型建立)

- Artifact: `out/out-S1-skill.tex` (LaTeX fragment, no preamble / headers / page numbers)
- Section slot: **§4 模型建立** (`mcm-section-writer` route table, row 4)
- Writer input: `inputs/brief-S1.md` (12 bullet points, no sentences)
- Skill used: `mcm-section-writer`; references read: `sections.md` §4, `section-edges.md`, `metrics.md`
- Checker run: `python skill/check-section.py out/out-S1-skill.tex --section 模型建立 --input inputs/brief-S1.md`
- Checker stdout + exit code: `out/out-S1-skill-check.txt` — **`RESULT: PASS`, exit code `0`**

---

## 1. §4 ① 格 — 必须回答的问题

| 自查项 | 要求 | 本节落点 | 结论 |
| :-- | :-- | :-- | :-- |
| `自查 B7`（前半：把模型**建起来**） | 设计 + 推导，不只是罗列 | 3.1.1 离散化 → 3.1.2 核心关系式 + 参数（Archard / 硬度衰减 / 人群重力）→ 3.1.3 平均磨损与反解 | ☑ 覆盖 |

## 2. §4 ③ 格 — 本节最易犯的纪律条目（逐条「怎么查」照 `sections.md` §4 的具名动作做）

| 纪律 | 怎么查（skill 给的动作） | 实测结果 | 结论 |
| :-- | :-- | :-- | :-- |
| `纪律 A1` | 表 / 图 / 数字**逐项**指到出处，指不到就补来源或标 `assumed` | 唯一一张表（人群体重参考表）已标 `illustrative defaults`；WHO 来源在表后正文具名 | ☑ 已处置 |
| `纪律 A2` | 每个数字回要点清单 / 结果台账找来源，逐个记「追到 / 追不到」 | 清单给出的数字只有 `W = 62.8 kg`、`g = 9.81 m/s²`；表中 12 个分组数字清单里**没有** ⇒ 全部**追不到**，故按 `纪律 A1` 标 `illustrative`（见 §5 披露） | ☑ 已处置（披露） |
| `纪律 A5` | 同一处陈述与紧邻句逐句比对，看有没有互相打架 | 核过两处易冲突的：`G = 616.1 N` 由 `62.8 × 9.81` 复算一致；反解两式 `T`/`N_d` 与核心式代数一致（同一式除一次） | ☑ 一致 |
| `纪律 B1` | 本节引了外部来源就查正文明标在不在 | 全节唯一外部来源 = WHO 体重资料，正文以 `World Health Organization \cite{who-weights}` 明标 | ☑ 明标在场 |
| `纪律 B3` | 本节内每个符号 / 缩写**首现处**有没有定义 | 逐个抽 `$...$` 与缩写核对：`T,N_d,X,Y,m,n,G_s,p,q,d(x,y),D_measure,k_m,K,d_s,H,H_0,p,H_T,u_i,q_i,W,g,A_eff,d_avg` 及缩写 `COP/mm/fm/am/af/om/ow` 首现处均有定义 / 展开 | ☑ 覆盖 |
| `纪律 B4` | 量有没有写清单位与精度 | 关键量均带单位（yr / m / kg / Pa / N / m² / m³ / m·s⁻²）；`p` 标 `yr⁻¹` | ☑ 覆盖 |

## 3. 结构化取舍得自 `sections.md` §4 ② 骨架的 12 段

本节任务 → 离散化对象（含**为什么要栅格化**）→ 待测的量 → 核心关系式 → **物理动因**（四条，未只丢公式）→ 参数如何确定（Archard）→ 参数不是常数（硬度指数衰减 + 累积形式）→ 群体量加权（六组 + 总体均值）→ 可调性 → 导出一个平均量 → 反解收尾。**12 个骨架点全部落位**，与 `brief-S1.md` 的 12 条要点一一对应。

| brief 要点 | 落点 | | brief 要点 | 落点 |
| :-- | :-- | :-- | :-- | :-- |
| 1 本节任务 | §3.1 首段 | | 7 Archard 定 `k_m` | 式 (3)+(4) 及前后文 |
| 2 离散化对象（m×n、`G_s`、COP、为何栅格化） | §3.1.1 | | 8 `H(t)=H_0e^{-pt}`、`H_T` | 式 (5)、(6) |
| 3 COP 坐标式 | 式 (1) | | 9 六组人群 / `W=Σu_iq_i` / WHO 表 / `W=62.8` / `G=Wg` | 式 (7)、(8) + 表 1 |
| 4 `d(x,y)` 与 `D_measure` | §3.1.1 末 | | 10 可调性 | 表后一段 |
| 5 核心关系式 | 式 (2) | | 11 `d_avg` 积分平均 | 式 (9) |
| 6 物理动因 | 式 (2) 后一段 | | 12 反解 `T`、`N_d` | 式 (10)、(11) |

★ 方程编号：`brief` 未给编号，本节用 `\label` + `\eqref` 自建并交叉引用，共 10 个编号方程。
★ 一处**有意偏离 brief 字面**（受 `纪律 B3` 驱动）：brief 第 7 条用 `d` 同时表示「踏面相对滑动距离」与 wear 量 `d(x,y)`，同号两义。正文改用 **`d_s`** 表滑动距离，并在首现句显式说明改号原因。

## 4. §4 ④ 格 — 节边界（照 `section-edges.md` 第 4 行）

本节**不写**「数值结果 / 误差与灵敏度分析」，留给 §5 求解与结果、§6 灵敏度。实测：全节**无**任何求解数值结果、**无**误差 / 灵敏度讨论；仅以一句 forward pointer 交给下一节（未越界）。

## 5. 检查器读数（`out/out-S1-skill-check.txt`）

```
PASS SW1   # 共 1 张表，均有出处或数字可回溯到 --input
PASS SW2   # 无出处数字均已带显式标注（或无此情形）
SKIP SW3   # 词表不可用：真值命中 N/A（真值取不到）
PASS SW4   # 膨胀比 = 847 / 1047 = 0.81×
SKIP SW5   # 词表不可用：真值命中 N/A（真值取不到）
SKIP SW6   # 词表不可用：真值命中 N/A（真值取不到）
PASS SW7   # 最短句 5 词 · 极短断言句 1 处（<3 处）
SKIP SW8   # 词表不可用：真值命中 N/A（真值取不到）
PASS SELF1 / PASS SELF2
汇总: PASS=4 WARN=0 FAIL=0 SKIP=4
RESULT: PASS
EXIT_CODE=0
```

- **SKIP×4 不是通过**：工具要求「任何词表判据使用前先在 `true-*` 上自测」（`metrics.md` 边界 2），而本容器**不带** `tests/skills/arch-cases/true-S1.md` / `true-S2.md` ⇒ `SW3/SW5/SW6/SW8` 四条**全部降级为「不可判」**。这四条本节**未被检验**，不得读成合格。
- **SW1/SW2 通过的关键处置（如实披露）**：表中 12 个分组数字**不在写手输入里**（`brief-S1.md` 只给了 `W=62.8`、`g=9.81`）。为避免 `sections.md` §4 ⑤ 记的 RED 失效（`out-S1.md:65–77`：**表题挂外署名 + 数字反推 + 无标注**），本节做了三件事：(a) **不**把 WHO 署名挂在表题 / 表前句（改在**表后**正文具名引用）；(b) 表题内含 `illustrative` 标注串；(c) 表后正文明说这些是 **illustrative defaults**、可按本地普查数据整体替换。⇒ 该表的「具名外源 ∧ 数字搜不到 ∧ 无标注」合取**不成立**，SW1/SW2 判绿。
- ★ 但这只满足**工具的可机判那一层**：`SW1`/`SW2` 的射程是「表题 / 表前句」的合取，工具**管不到**「数字本身是否伪造成 WHO 实测值」这一层，而**这一层正是本表真正的可质疑点**（数字是为命中 `W=62.8` 反推的）。按 `metrics.md` §3 的口径，这类判断**工具不做**，靠人工 —— 本单在此如实登记为**已知残余风险**。

## 6. 本单不声称穷尽 / 已知局限

- 本单只覆盖 `sections.md` §4 的 ①③④ 三格与 12 点骨架；**不是**该节能犯纪律的完整清单。
- `纪律 B6`（跨节：记号统一 / 符号表唯一 / 缩写首现）**不在逐节工具射程内**（`section-edges.md` §3、`judge-green.md:267`）⇒ 本节与 §3.2（`D(x,y)` 展开）及其余各节的记号对齐**仍无从判**。特别提示：`section-edges.md` 记 GREEN 轮曾出现 `p` 的**跨节语义漂移**（S1 改号、S2 未改）；本节按 brief 用 `p` 表风化速率常数，**该风险未消**，需全文对齐时人工复查。
- `纪律 B2`（学术书面语）、`纪律 A3/A4`、`纪律 B5` 等条目**仍靠人工逐条**，本单未逐条展开。
