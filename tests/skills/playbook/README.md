# `tests/skills/playbook/` —— `mcm-playbook` 的验证层（判据 + 变异 + RED/GREEN）

本目录是 **`mcm-playbook`**（M1 赛程编排，本套件**家族外第一个** skill）的验证层。
★ 它**不产任何产物**（无图 / 表 / 代码）⇒ 这里的判据**不是"量产物"**，而是**"查一致性"**（设计 §4）。

## 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `check-playbook.py` | 机械层判据 **`T1`–`T5`**（设计 §4.1）。用法：`python tests/skills/playbook/check-playbook.py` |
| `mutate-playbook.py` | **变异驱动器**（计划 Task 2）：每条判据至少一条真红变异 + 4 条"必须仍绿"的射程边界对照 |
| `make-evidence.py` | **RED × GREEN 对照证据生成器**（机器抽取；`write_bytes`、全 LF；判据清单**现取**） |
| `PLAYBOOK-evidence.md` | 由生成器产出的对照证据件（**唯一权威的对照结论在这里**） |
| `red/` | **RED**：三位干净上下文写手（无 skill）产出的赛程表 + 派发口径与自述 |
| `green/` | **GREEN**：用本 skill 出的同一件事（= 本 skill 本身，**不存副本**） |

## 五条判据（详表见 `check-playbook.py` 的 docstring 与设计 §4.1）

| ID | 判什么 | 现取的读数源 |
| :--- | :--- | :--- |
| `T1` | 硬时刻 4 项 + 两个推算时长（99 / 100 h）与 `INDEX.md` §2.6 **逐位/逐值一致** | `corpus/official/INDEX.md` §2.6.1/§2.6.2/§2.6.5 |
| `T2` | 每条「失误」带**分级** + **`§id` 出处**，且该 `§id` **现场解析得到** | `INDEX.md` 表格行 id 全集 |
| `T3` | 凡点名的 skill **真的存在**；**不存在的必须明写「未建」** | `.claude/skills/` |
| `T4` | 北京时间换算**由 `zoneinfo` 现算**比对（不是抄常数） | `zoneinfo`（标准库） |
| `T5` | 阶段边界与失误归类带**「构造」**标注 · 示例评分表处带官方限定串 | 本地文档断言 |

★ **每条 fail-closed**：读不出 ⇒ 红 + `exit 1`（**不许静默绿**）。末行恒为 `RESULT: …`。

## 一键复跑

```bash
python tests/skills/playbook/check-playbook.py       # 期望 5/5 PASS
python tests/skills/playbook/mutate-playbook.py      # 期望 16/16 达预期
python tests/skills/playbook/make-evidence.py        # 重生成 PLAYBOOK-evidence.md（不动点）
```

## 覆盖边界（**不声称穷尽**）

- 判的是**文档与来源之间的机械一致性**；**判不了**：这张时刻表讲不讲得清 / 动作清单照做做不做得出来 /
  阶段切分合不合理 / 文字措辞好不好。
- **「看一眼」层不适用**（本支无产物）；其**替代品**（把动作清单拿给人读一遍）**不在本器里**
  —— 执行记录见 `PLAYBOOK-evidence.md` §7，★ 并**如实标明它是替代品，不是等价物**。
- **不声称覆盖全部失败模式。**
