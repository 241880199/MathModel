# `green/` —— GREEN 对照件（**用本 skill** 出的同一件事）

> ## !! 本目录（连同上一级证据件与 `red/**`）含泄题风险，绝不给写手 !!
>
> **点名**：上一级 `PLAYBOOK-evidence.md`（对照结论）与 `../red/README.md` / `../red/writer-self-reports.md`
> **都不给写手**。**这个点名不是穷举**：`../red/out-R{n}/schedule.md`（别的写手的产物）与本 `README.md` 自身**同样不给写手**。

## 1. 这是什么

Task 3 的 GREEN 侧：与 `red/` **同一件事、同一把尺**，只换一个自变量 —— **用不用本 skill**。

- **同一件事**：`tests/skills/playbook/red/brief.md`（**权威副本在 `red/`**，本目录**不重复内联**）——
  "**做一份美赛赛程表**"。RED 与 GREEN **逐字共用同一份 brief**。
- **GREEN 就是本 skill 本身**（依据 Task 3 任务书硬要求 2 的括注"**its `references/` and its contract**"）：
  `.claude/skills/mcm-playbook/SKILL.md`（契约）＋ `references/timeline.md`（赛程时间线）
  ＋ `references/phase-mistakes.md`（每阶段典型失误）。
  ★ **本目录不存放 GREEN 产物的副本** —— 那会造出**第二份权威**（本仓反复栽过的一型：
  复述即造第二份权威）。**权威在 `.claude/skills/mcm-playbook/`，被验的就是它。**
  ⇒ 本目录**只有一个 README**，**没有 `out-G1/`**（与先例 `schematic/green/out-G1/` 的形态差别，理由如上）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `README.md` | 本文件（泄题风险件） |

**上表不声称穷尽**：本目录内任何文件派写手时都不给。

**对照表在上一层**：`../PLAYBOOK-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. 本支产物在机械判据上的读数

- **GREEN 五条判据全绿**（`T1`–`T5`）—— 逐字读数见 `../PLAYBOOK-evidence.md` §3。
- **`T1`**：硬时刻 4 项与 `corpus/official/INDEX.md` §2.6.1/§2.6.2 **现取**比对一致；
  两个推算时长（99 / 100 小时）与 §2.6.5 **且**与"由硬时刻现算的差"一致。
- **`T4`**：北京侧 4 行由 `zoneinfo` **现算**比对（不是抄常数）。

## 4. 与 RED 的比对口径

同一件事（`red/brief.md`，逐字）、同一把尺（`check-playbook.py`，**两侧同一版** —— 工作树版；与基线 `e9d8d47` 的差 = 一处 **arm C 结束标记**，**已实证两侧读数一字未变**，见 `../PLAYBOOK-evidence.md` §0 与 §8）。
**两侧同一组参数**：`--index` 与 `--skills-root` 指向**同一份**官方事实基线与同一个 skill 根；
`--skill-md` / `--timeline` / `--mistakes` 各指向**该侧自己的产物集**（GREEN = 本 skill 的三份文档；
RED = 写手产出的那份 `schedule.md`）。**不许**因为 RED 红得多就调判据或换数据。

★ **RED 的诚实边界**（硬要求 7 / 设计 §4.3）：中性 brief **已经限定**"要产出一张赛程表"
⇒ 这轮 RED **测不到"连表都做不出来"那一类失败**。**不声称覆盖全部失败模式。**
逐条对照与判词见 `../PLAYBOOK-evidence.md`。
