# Task 5 · RED × GREEN 对照证据（`mcm-data` · `DA1`–`DA5`）

本文件由 `tests/skills/data/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
**它不含**时间戳 / 随机序 / 绝对路径（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`）⇒ **重新生成字节级一致**（不动点，见 §6）。**§1–§4 是机器抽取**（逐字解析检查器 stdout、逐条跑样例）；**§5 的边界是手写**（文里已标明）。

## §0 口径（样例驱动 · 只评「判据红没红」 · 现取判据清单）

- **RED / GREEN 是「样例驱动」的**（设计 §5；**不是**另起写手 agent 作对照）：
  - **RED 侧** = 逐条判据的**违规样例**（`tests/skills/data/samples/<判据号>/violate/`）跑`check-data.py --scope artifact` 的**实测读数** —— 每条确实红，**且红的是它自己那条**。
  - **GREEN 侧** = 逐条判据的**合规样例**（`…/comply/`）跑一遍的**实测读数** —— 每条确实绿。
- **对照口径**：**只评「判据红没红」**，不评别的（设计 §5）。
- **判据清单现取**（**不写死条数**）：从检查器 stdout 现取 `DA*` 行 ⇒ 本次 **5 条**（`DA1、DA2、DA3、DA4、DA5`）。
- **检查器自证**：`.claude/skills/mcm-data/check-data.py` worktree blob `c4c30aa29193`（本支不动它；两侧同一版）。
- **样本量边界**：样例是**构造的**、每判据仅**一对**（`n` 小）⇒ 见 §5 —— **不声称穷尽**失效形态。

## §1 不变式 ①：判据总数 == `samples/` 下一级目录数

| 现取到的判据（左） | 条数 | `samples/` 一级目录（右） | 个数 | 集合相等 |
| :-- | --: | :-- | --: | :-- |
| DA1、DA2、DA3、DA4、DA5 | 5 | DA1、DA2、DA3、DA4、DA5 | 5 | **是** |

★ 两边**现取**：删掉检查器里任一条判据 ⇒ 左少一个；删掉任一样例目录 ⇒ 右少一个；**两边都会当场红**。
★ 该不变式**自带一条自证探针**：喂一对不等集合必判否 ⇒ **OK**（断言没被架空）。

## §2 RED 侧：逐条判据的**违规样例**实测读数（`violate/`）

### §2.1 汇总（机器抽取：逐条 status）

| 判据 | 它自己这条 | 同侧其余判据 | 该侧 `exit` | 只红它自己 |
| :-- | :-- | :-- | --: | :-- |
| `DA1` | **FAIL** | 其余 4 条 = PASS | 1 | **是** |
| `DA2` | **FAIL** | 其余 4 条 = PASS | 1 | **是** |
| `DA3` | **FAIL** | 其余 4 条 = PASS | 1 | **是** |
| `DA4` | **FAIL** | 其余 4 条 = PASS | 1 | **是** |
| `DA5` | **FAIL** | 其余 4 条 = PASS | 1 | **是** |

★ 每行**只评「它自己那条」红没红**（设计 §5 的对照口径）；**不评别的**。

### §2.2 RED 原始 stdout（逐条判据的 `violate/` 跑一遍 · **逐字**贴检查器输出）

**`DA1`** —— 打的是：来源表在场 + `出处`/`口径`/`局限`/`获取日期`/`取数方` 五列每行非空（`取数方` 取值域 fail-closed）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA1/violate/data-sources.md --refs tests/skills/data/samples/DA1/violate/paper.md   → exit=1
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA1/violate/data-sources.md
      | refs   = tests\skills\data\samples\DA1\violate\paper.md
      | FAIL  DA1  势=2（数据行）· 五列有空 / 取值非法 1 处  <<< 第1行 `口径` 空
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（DA1）
```

**`DA2`** —— 打的是：每个**非自主**来源都有对应引用（`[官方]` `corpus/official/instructions.html:1121`）；保留值 `本队自产` 的行豁免

```
$ check-data.py --scope artifact tests/skills/data/samples/DA2/violate/data-sources.md --refs tests/skills/data/samples/DA2/violate/paper.md   → exit=1
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA2/violate/data-sources.md
      | refs   = tests\skills\data\samples\DA2\violate\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | FAIL  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 1 条  <<< 「https://example.com/private-dataset」
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（DA2）
```

**`DA3`** —— 打的是：`可信度层级` 每行非空且在五级内；保留值 `本队自产` 的行豁免（填 `—`）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA3/violate/data-sources.md --refs tests/skills/data/samples/DA3/violate/paper.md   → exit=1
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA3/violate/data-sources.md
      | refs   = tests\skills\data\samples\DA3\violate\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | FAIL  DA3  势=2（数据行）· 空缺/越级 1 处  <<< 第1行「9 自媒体」不在五级内
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（DA3）
```

**`DA4`** —— 打的是：★ 人机确认闸：凡 `取数方=AI` 的行，`确认` 须「已核」+ 确认人 + 日期（`P6`）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA4/violate/data-sources.md --refs tests/skills/data/samples/DA4/violate/paper.md   → exit=1
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA4/violate/data-sources.md
      | refs   = tests\skills\data\samples\DA4\violate\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | FAIL  DA4  势=1（`取数方=AI` 的行）· 未确认 1 处  <<< 第1行；仍为「待核」
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（DA4）
```

**`DA5`** —— 打的是：清洗与口径对齐步骤有记录、且每步可重跑（启发式：认脚本/命令标记）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA5/violate/data-sources.md --refs tests/skills/data/samples/DA5/violate/paper.md   → exit=1
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA5/violate/data-sources.md
      | refs   = tests\skills\data\samples\DA5\violate\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | FAIL  DA5  势=2（清洗步骤项）· 不可重跑 2 项  <<< 第 1/2 项无脚本/命令标记
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（DA5）
```

## §3 GREEN 侧：逐条判据的**合规样例**实测读数（`comply/`）

### §3.1 汇总（机器抽取：逐条 status）

| 判据 | `comply/` 全员 status | 该侧 `exit` | 全绿 |
| :-- | :-- | --: | :-- |
| `DA1` | 全 PASS | 0 | **是** |
| `DA2` | 全 PASS | 0 | **是** |
| `DA3` | 全 PASS | 0 | **是** |
| `DA4` | 全 PASS | 0 | **是** |
| `DA5` | 全 PASS | 0 | **是** |

### §3.2 GREEN 原始 stdout（逐条判据的 `comply/` 跑一遍 · **逐字**贴检查器输出）

**`DA1`** —— 打的是：来源表在场 + `出处`/`口径`/`局限`/`获取日期`/`取数方` 五列每行非空（`取数方` 取值域 fail-closed）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA1/comply/data-sources.md --refs tests/skills/data/samples/DA1/comply/paper.md   → exit=0
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA1/comply/data-sources.md
      | refs   = tests\skills\data\samples\DA1\comply\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`DA2`** —— 打的是：每个**非自主**来源都有对应引用（`[官方]` `corpus/official/instructions.html:1121`）；保留值 `本队自产` 的行豁免

```
$ check-data.py --scope artifact tests/skills/data/samples/DA2/comply/data-sources.md --refs tests/skills/data/samples/DA2/comply/paper.md   → exit=0
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA2/comply/data-sources.md
      | refs   = tests\skills\data\samples\DA2\comply\paper.md
      | PASS  DA1  势=3（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条  · 自产豁免 1 行
      | PASS  DA3  势=3（数据行）· 空缺/越级 0 处  · 自产豁免 1 行
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`DA3`** —— 打的是：`可信度层级` 每行非空且在五级内；保留值 `本队自产` 的行豁免（填 `—`）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA3/comply/data-sources.md --refs tests/skills/data/samples/DA3/comply/paper.md   → exit=0
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA3/comply/data-sources.md
      | refs   = tests\skills\data\samples\DA3\comply\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`DA4`** —— 打的是：★ 人机确认闸：凡 `取数方=AI` 的行，`确认` 须「已核」+ 确认人 + 日期（`P6`）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA4/comply/data-sources.md --refs tests/skills/data/samples/DA4/comply/paper.md   → exit=0
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA4/comply/data-sources.md
      | refs   = tests\skills\data\samples\DA4\comply\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`DA5`** —— 打的是：清洗与口径对齐步骤有记录、且每步可重跑（启发式：认脚本/命令标记）

```
$ check-data.py --scope artifact tests/skills/data/samples/DA5/comply/data-sources.md --refs tests/skills/data/samples/DA5/comply/paper.md   → exit=0
      | check-data.py · scope=artifact
      | target = <REPO>/tests/skills/data/samples/DA5/comply/data-sources.md
      | refs   = tests\skills\data\samples\DA5\comply\paper.md
      | PASS  DA1  势=2（数据行）· 五列有空 / 取值非法 0 处
      | PASS  DA2  势=2（不同非自主 `出处` 值）· 在 `--refs` 中搜不到 0 条
      | PASS  DA3  势=2（数据行）· 空缺/越级 0 处
      | PASS  DA4  势=1（`取数方=AI` 的行）· 未确认 0 处
      | PASS  DA5  势=3（清洗步骤项）· 不可重跑 0 项
      | ------------------------------------------------------------------------------
      | 判据 5 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

## §4 不变式 ②：`DA4`（人机确认闸）的红来自「确认缺失」那一行本身（`P6` 的核心）

**机器交叉核**（两条独立路径对齐）—— 路径 1 = 检查器判词里**报出的行号**；路径 2 = 从样例表里**独立读出**的「`取数方=AI` 且 `确认` 未「已核」」的**行号**。

| 侧 | `取数方=AI` 的行（路径 2） | 其中「确认缺失」的行（路径 2） | 检查器**报出**的行（路径 1） | `DA4` status | 对齐 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `DA4/violate` | [1] | [1] | [1] | FAIL | **是** |
| `DA4/comply` | [1] | [] | （空） | PASS | **是** |

★ **读法**：`violate/` 侧把**确认那格**从「已核（…）」改成「待核」—— **只动这一格**；`DA4` 的 `FAIL` 判词 **`<<< 第1行；仍为「待核」`** 报的正是**那条 AI 行本身**（不是别行、不是别的判据连坐）⇒ 这就是设计 §1.2 那句边界话的**机械落地**。
★ **`comply/` 侧**同一行填「已核（…, 日期）」⇒ `DA4` 判 `PASS` ⇒ **正反真的分得开**。
★ 该不变式**不靠手抄行号**：行号由**样例表当场读出**、再与**检查器报出**的行号**集合比对**。

## §5 诚实边界（**不声称穷尽** · 手写）

- ★★ **样本量边界（原话）**：**样例是构造的** —— 每条判据**只钉一对**（`comply` + `violate`），`n` 小 ⇒ **本文只证明「判据真的会红 / 会绿」，不代表真实赛期表现、也不覆盖全部失效形态**。**凡本文列的清单都不声称穷尽。**
- ★ **RED / GREEN 是「样例驱动」的**（设计 §5）：**不另起写手 agent 作对照** ⇒ 它**证明不了**「一个不看 skill 的写手会不会踩同样的坑」——**那是另一支（M4）的口径，本支不做**。
- ★ **外检是启发式**（设计 §4.4）：`DA2`（出处全列搜子串）、`DA3`（五级启发式）、`DA5`（可重跑认脚本/命令标记）**都有假阳性 / 假阴性面**；本文只如实贴某一次读数，**不背书内容对错**。
- ★ **只评「判据红没红」**：本文不对样例产物的**质量**下任何判断（设计 §5 的对照口径）。

## §6 可重放性（**不动点**：先干净 → 捕获 → 提交 → 再跑一次）

- **本文件完全由生成器当场产出**：`python tests/skills/data/make-evidence.py`（跑完 `git status --short` 应为空）。
- **不动点的证法**：在**已提交的树上**、**同一操作系统内**重跑本生成器 ⇒ **本文件逐字节不变**（跑后 `git status --short` 仍为空）；**平台边界见下条**。
- **非确定性被逐项堵住**：无时间戳 / 无 `random` / 无 `set` 遍历序（一律 `sorted()`）/**无绝对路径**（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`）⇒ **不写「生成日期」这类会漂的字段**。
- ★ **平台边界（非跨平台规范形）**：本件内含**检查器 stdout 逐字捕获的 Windows 反斜杠相对路径**（如 `refs   = tests\…` —— `pathlib` 在 Windows 上按 `os.sep` 渲染）⇒ **不动点只在同一操作系统内成立**；换 Linux/macOS 重跑**不再逐字节一致**。
- **它实跑**：`check-data.py`（逐对 ×2 侧 + 一次 `--scope artifact` 现取判据 + 不变式 ② 的两次 + 一次 `--scope self`）。

## §7 生成器口径与数据来源（机器抽取 · blob 当场跑 `git hash-object`）

- 生成器 `tests/skills/data/make-evidence.py` blob `5a4993fe872e`。
- 检查器 `.claude/skills/mcm-data/check-data.py` blob `c4c30aa29193`（本支不动它）。
- 样例夹具逐件 blob：

| 夹具 | blob |
| :-- | :-- |
| `tests/skills/data/samples/DA1/comply/data-sources.md` | `9a549e7e00da` |
| `tests/skills/data/samples/DA1/comply/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA1/violate/data-sources.md` | `62cf002e73b5` |
| `tests/skills/data/samples/DA1/violate/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA2/comply/data-sources.md` | `bc9cc45e065c` |
| `tests/skills/data/samples/DA2/comply/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA2/violate/data-sources.md` | `1aa993e7f0c8` |
| `tests/skills/data/samples/DA2/violate/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA3/comply/data-sources.md` | `9a549e7e00da` |
| `tests/skills/data/samples/DA3/comply/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA3/violate/data-sources.md` | `f5b3bcb83b02` |
| `tests/skills/data/samples/DA3/violate/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA4/comply/data-sources.md` | `9a549e7e00da` |
| `tests/skills/data/samples/DA4/comply/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA4/violate/data-sources.md` | `767c1ed5a8a4` |
| `tests/skills/data/samples/DA4/violate/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA5/comply/data-sources.md` | `9a549e7e00da` |
| `tests/skills/data/samples/DA5/comply/paper.md` | `2c8d7b3748df` |
| `tests/skills/data/samples/DA5/violate/data-sources.md` | `2780f7cf4fd5` |
| `tests/skills/data/samples/DA5/violate/paper.md` | `2c8d7b3748df` |

- **内检 `--scope self`（补充读数，非 RED/GREEN）**：

```
$ check-data.py --scope self   → exit=0
      | check-data.py · scope=self
      | skill-dir = <REPO>/.claude/skills/mcm-data
      | PASS  SELF1  势=2（边界句）· 缺 0 句
      | PASS  SELF2  势=7（内部指针）· 悬空 0 条
      | PASS  SELF3  势=1（模板表头）· 不符 0 处
      | ------------------------------------------------------------------------------
      | 判据 3 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

- ★ **本文不声称穷尽**：只覆盖 `samples/` 里**现存的**那一对一夹具 + 检查器判的那几条判据。
