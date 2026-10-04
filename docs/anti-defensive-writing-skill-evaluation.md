# 外部 skill 评估：`anti-defensive-writing-Skill`

> **评估对象**：<https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill>（MIT）。
> **评估日期**：2026-10-05。**触发**：用户提出"关于防御性写作，这个 skill 是否有帮助"。
> **入库范围**：只有本文（评估结论）。**被评估的仓库本身不入库** —— 评估时临时 clone 到 `build/anti-def/`（已 gitignore）。
> **本文的每个数都附可复跑的命令**；凡列清单均写"不声称穷尽"。

---

## 0 结论

**不引入。只取它点出的一个词类，且那一类在本语料上判不了机器判据。**

- **它的语言规则与本套件两条硬约束冲突**（详见 §3）：① **COMAP 官方要求讨论优缺点**（`corpus/official/instructions.html:1162`）；② 本套件层序是**准确 ≻ 规范 ≻ 文风**，而它的目标函数是"说服力"。
- **它是一条纯提示词规则**：无脚本、无判据、无阈值、无 RED/GREEN 证据 —— 与本仓"判据必须真的会红"的约定不同型。
- **它唯一补充的词类 = "hedge / 自我削弱姿态"**（`遗憾的是` / `仅` / `效果有限`）。这一类**已按本仓流程落成** `docs/mcm-writing-discipline.md` §③ 的「**自我削弱口径**」：实质局限**必须写**，要压的是包裹它的**姿态层**；判法 = 人工（`C1` 减法测试的负向特例）；**机判 = 无**（实测见 §4）。

---

## 1 它是什么

一个**零依赖、纯提示词**的 skill（MIT）：

| 件 | 体量 |
| :--- | ---: |
| `skills/anti-defensive-writing/SKILL.md` | 5.6 KB |
| `skills/anti-defensive-writing-en/SKILL.md` | 6.5 KB |
| `prompts/精简版提示词.txt` · `prompts/quick-prompt-en.txt` | 1.9 KB · 2.4 KB |
| `README.md` · `README_EN.md` · `LICENSE` | — |

核心原则（原话）：*"论文是一场学术发布会，不是项目总结、实验日志或自我审查报告。"* 12 条规则分四类：**叙事**（只围绕优势组织）·**语言**（禁用自我削弱表达、不说输）·**实验**（每个实验承担一个论证职责）·**结构**（摘要引言 = 发布会开场、结论只强化记忆点）。

---

## 2 与套件写作纪律的对照

本套件处理"措辞 / 机器味"的权威件 = `docs/mcm-writing-discipline.md` §③（其下 `C1`/`C2`/`C3` 三条统计代理量 + 加粗口径 + `mcm-section-writer` 的 `SW6`/`SW8`/`SW9`）。

| 它的规则 | 套件里已有（更硬） |
| :--- | :--- |
| 删掉信息量不变的句子 | `C1` 套话/自评句比（**减法测试**，有 RED/GREEN 读数） |
| 措辞克制、不写未验证的比较级 | `mcm-abstract` 的 `Q12`（空话 + 未验证比较级） |
| 不写元话语（`This section …`） | `SW6` 自评式元话语 · `SW8` 可整句删除的元话语 |
| ——（它没提过度加粗） | `SW9` 正文加粗密度（2026-10-04 立） |
| 不写"我们做了什么"的过程流水账 | `A4` 不留制作注记 + 各节范式规定的次序 |

⇒ **它的"叙事 / 实验 / 结构"三类，套件用"官方要求 + 节范式"覆盖；"语言"类里的"删空话"由 `C1`/`Q12` 覆盖。** 剩下一格是**负向姿态词**（§4）。

---

## 3 硬件冲突（不引入的理由）

1. **COMAP 官方 `corpus/official/instructions.html:1162` 明文**：
   > • Discuss any apparent strengths or weaknesses to your model or approach.

   即**官方要求讨论优缺点**。它的"**不说输**""**打不过的维度不设为比赛**""**重新定义论文故事**"是**压掉或绕开**这类陈述 —— 与本条正面对撞。本套件的 `mcm-abstract` 的 `Q12` **已经**把 `limitations` / `robustness` / `sensitivity` 一类明确判为"**属官方要求的优缺点陈述，不能删**"，并在 `Q12` 里钉了一句：

   > **照抄词表把合法的内容删掉，就是这一整轮在修的形态。**

   这份外部 skill 的"禁用自我削弱表达"，正是一份**这类词表**。

2. **层序冲突**：本套件 `docs/mcm-writing-discipline.md` 定的层序是 **① 准确性（闸门）→ ② 规范性（闸门）→ ③ 文风（次级分）**，且**后层不得抵消前层**。它的目标函数是"说服力最大化"（"只围绕优势组织""优势必须被明确说出来"），会把文风层提到闸门之上 —— 方向上与本套件相反。

---

## 4 实测探针：为什么"自我削弱词表"不能用

口径（**与 `docs/mcm-writing-discipline.md` §③「自我削弱口径」同一套、同一命令**）：`grep -o -i -E <模式>`；正文区间 = 该文档 C2 段那 5 条 `sed` 行；人写样本 = `corpus/papers/md/2025美赛O奖论文/**/*.md`（43 份）。**唯一复跑命令**：`python tests/skills/check-writing-discipline.py`（看 `A11` 行）。

**① 显式自我削弱词** —— 模式 `\b(unfortunately|admittedly|regretfully|sadly|we must admit|to be honest|we were unable to|we failed to|we regret)\b`：

| 侧 | 命中 | 密度 |
| :--- | ---: | ---: |
| RED（无纪律 3 份） | **0** 次 | 0.00 ‰ |
| 真值（人写 2 份） | **0** 次 | 0.00 ‰ |
| 43 份人写 O 奖论文 | **1** 次（仅 1 件） | ≈ 0.00 ‰ |

⇒ **两侧同为 0 —— "零 vs 零"定不了阈**（同 `C2` 那条"0 与 0 之间无法定阈"的通例）。**没量，故不设机器判据。**

**② 弱化词** —— 模式 `\b(only|merely|simply|weak|weaker|limited)\b`：

| 侧 | 密度 |
| :--- | ---: |
| **真值（人写 2 份）** | **1.45 ‰** |
| RED（无纪律 3 份） | 0.80 ‰ |
| 43 份人写 O 奖论文 | 1.04 ‰（**43/43 份都有**，中位 9 次/件，最大 31） |

⇒ **方向相反**：真值（好写作）用得**比 RED 还多**。真值里那两处 `limited` 逐处看过，分别是"物理受限"（`is limited`）与一个**局限小标题**（`Limited Treatment of Environmental Variability:`）—— 都是**合法内容**。⇒ **词表禁用会伤合法写作**，判为**明令别用**（与 `C2` 那条"过度收敛"的风险同型）。

---

## 5 已落地的动作（本评估的产出）

1. `docs/mcm-writing-discipline.md` **§③ 新增「自我削弱口径」**：实质局限必须写（引官方 `:1162`）；压的是姿态层；判法 = 人工（`C1` 的负向特例）；**明令别用弱化词表**；**机判 = 无**（§4 的实测）。
2. `tests/skills/check-writing-discipline.py` 新增 **`A11`** 复算（§4 的四个读数现取现算）+ `SELF_COMPUTED_ROSTER` 登记 + `ANCHORS` 新增 `(instructions.html, 1162)` + 头部自陈同步（出站指针 **107→108**、去重落点 **76→77**）。
3. `tests/skills/mutate-writing-discipline.py`：`M25` 改靶（`107→108` 已成真值）+ 新增 **`M44`**（把 hedge 的 RED 读数改错 ⇒ `A11` 必须红）。
4. 台账 `docs/mcm-suite-todo.md` §H.3 登记。

---

## 6 复现命令

```bash
# 四个读数（hedge 两侧为 0 / 弱化词方向相反），一次跑全：
python tests/skills/check-writing-discipline.py        # 看 A11 行；末行 RESULT: PASS

# 证明 A11 真的会红（GC12）：
python tests/skills/mutate-writing-discipline.py       # 末行 MUT: 全红（44 条变异；还原 3/3 逐字节）

# 官方那条硬要求（本评估 §3 的出处）：
sed -n '1162p' corpus/official/instructions.html
```

**未做 / 不声称**：本评估**没有**在 Claude Code 之外实测该 skill；**没有**逐条判它 README 里的每个说法；**只**核了它的规则文本与套件纪律、官方要求、以及本语料上的实测。
