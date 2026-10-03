# `tests/skills/topic-select/` —— `mcm-topic-select` 的验证层（判据 + 变异 + RED/GREEN）

本目录是 **`mcm-topic-select`**（M1 选题决策，本套件**家族外第二个** skill）的验证层。
★ 它**不产图 / 表 / 代码**（产物是一份**判断 + 依据**）⇒ 这里的判据**不是"量产物"**，而是**"查一致性"**（设计 §3）。

## 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `check-topic-select.py` | 机械层判据 **`S1`–`S6`**（设计 §3）。用法：`python tests/skills/topic-select/check-topic-select.py` |
| `mutate-topic-select.py` | **变异驱动器**（计划 Task 2）：每条判据至少一条真红变异 + 4 条"必须仍绿"的射程边界对照 + 4 条 fail-closed |
| `make-evidence.py` | **RED × GREEN 对照证据生成器**（机器抽取；`write_bytes`、全 LF；判据清单**现取**） |
| `TOPICSELECT-evidence.md` | 由生成器产出的对照证据件（**唯一权威的对照结论在这里**） |
| `fixtures/` | 判据自测用的**已知好产出**与**构造题面**（`fixtures/problems/` 六份是**构造的**，只用于机械自测） |
| `red/` | **RED（两轮）**：干净上下文写手（无 skill 正文）产出的选题决策 + **2025 A–F 真实题面** + 派发口径与自述。**第一轮（无形态）** + **第二轮（给一份"只有形状"的中性形态）** —— 两轮都留 |
| `green/` | **GREEN**：用本 skill 出的同一件事（`out-G1/decision.md`） |

## 六条判据（详表见 `check-topic-select.py` 的 docstring 与设计 §3）

| ID | 判什么 | 现取的读数源 |
| :--- | :--- | :--- |
| ★★ `S1` | **每个标签的支撑句必须是当天题面的子串**（按语料口径归一化后）—— **心脏** | `--problems` 的题面 + `tools/papers/taxonomy` 的归一化 |
| `S2` | 凡引历史，读数与 `PROBLEM_TYPES.md` / `MODEL_MAP.md` **现取**一致 | `corpus/papers/**` |
| `S3` | 四轴**逐轴齐备**，且每轴**标明可核性**（读数 / 半可核 / 判断）；**判断型不许写成读数** | 产出自身 |
| `S4` | 推荐**带推翻条件**（并点名一道在场的题） | 产出自身 |
| `S5` | **时间盒声明在位**（`≤2 小时` + 什么时候值得超时） | `SKILL.md` + `references/method.md` |
| `S6` | **禁令在位**（不许拿"历史获奖论文篇数"代理"选它的人数" + "赛期内不可回答"那句在位） | `references/method.md` |

★ **每条 fail-closed**：读不出 ⇒ 红 + `exit 1`（**不许静默绿**）。末行恒为 `RESULT: …`。
★ **`S5`/`S6` 是规范侧**（判 `SKILL.md` + `references/method.md`，**与 `--output` 无关**）⇒ 在 RED/GREEN 上恒 `PASS`；
**RED 与 GREEN 的分野只体现在 `S1`–`S4`（产出侧）**。

## CLI 输入面（写死；见 `check-topic-select.py` docstring）

`--problems`（当天题面：一个目录或一个文件）· `--output`（本 skill 的产出）· `--corpus`（`corpus/papers/` 根，可指向别处）
· `--skill-md` / `--method`（规范侧两份文档）。**三者任一读不出 ⇒ fail-closed 红。**

## 一键复跑

```bash
python tests/skills/topic-select/check-topic-select.py        # 期望 6/6 PASS
python tests/skills/topic-select/mutate-topic-select.py       # 期望 17/17 达预期
python tests/skills/topic-select/make-evidence.py             # 重生成 TOPICSELECT-evidence.md（不动点）
```

## 覆盖边界（**不声称穷尽**）

- 判的是**产出与"当天题面 + 语料现取 + 规范文档"之间的机械一致性**；**判不了**：推荐对不对 /
  四轴的判断质量 / 分类打得准不准 / 题面本身是不是那场比赛的真题 / 文字措辞好不好。
- **「看一眼」层不适用**（本支无产物可看）；其**替代品**（把"推荐 + 依据"拿给人读一遍）**不在本器里**
  —— 执行记录见 `TOPICSELECT-evidence.md` §8，★ 并**如实标明它是替代品，不是等价物**。
- ★★ **本轮 RED/GREEN 复现不了"当天新题不在语料里"那一情形**（2027 的题尚不存在；真实旧题集都在语料里）
  ⇒ **本轮测的是形态/逐字纪律与判据本身，不是真实赛期情形**。**不声称覆盖真实赛期情形。**
- ★ **两轮 RED 各证明什么**（详见 `TOPICSELECT-evidence.md` §10）：**第一轮（无形态）**证明**契约外产物在产出侧全臂 fail-closed**；
  **第二轮（有中性形态）**第一次**行使了 `S1` 的逐字判别力**（写手产出了可比结构、支撑句逐条非子串）。
  ★ 第二轮的 `S2` 红仍是 **fail-closed 型**（历史行不成形态）⇒ **`S2` 的"N 写错"那一格仍未被 RED 行使**（只在变异驱动器里）。
- ★ **GREEN 的 `S2` 读数因边界 ③ 被违反而退化**（只验证形式、未验证真实赛期语义）—— 见 `TOPICSELECT-evidence.md` §10.3。
- **不声称覆盖全部失败模式。**
