# Task 5 · RED × GREEN 对照证据（`mcm-code` · `CD1`–`CD6`）

本文件由 `tests/skills/code/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
**它不含**时间戳 / 随机序 / 绝对路径（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`）⇒ **重新生成字节级一致**（不动点，见 §6）。**§1–§4 是机器抽取**（逐字解析检查器 stdout、逐条跑样例）；**§5 的边界是手写**（文里已标明）。

## §0 口径（样例驱动 · 只评「判据红没红」 · 现取判据清单）

- **RED / GREEN 是「样例驱动」的**（设计 §5；**不是**另起写手 agent 作对照）：
  - **RED 侧** = 逐条判据的**违规样例**（`tests/skills/code/samples/<判据号>/violate/`）跑`check-code.py --scope artifact` 的**实测读数** —— 每条确实红，**且红的是它自己那条**。
  - **GREEN 侧** = 逐条判据的**合规样例**（`…/comply/`）跑一遍的**实测读数** —— 每条确实绿。
- **对照口径**：**只评「判据红没红」**，不评别的（设计 §5）。
- **判据清单现取**（**不写死条数**）：从检查器 stdout 现取 `CD*` 行 ⇒ 本次 **6 条**（`CD1、CD2、CD3、CD4、CD5、CD6`）。
- **检查器自证**：`.claude/skills/mcm-code/check-code.py` worktree blob `8f8efa433076`（本支不动它；两侧同一版）。
- **外检靶子形态**：每对 = 一个**代码目录** `…/code/`（含代码文件 + `result-manifest.md`）＋ 一个**论文文件** `…/appendix.md`（`--appendix` 靶子）。
- **样本量边界**：样例是**构造的**、每判据仅**一对**（`n` 小）⇒ 见 §5 —— **不声称穷尽**失效形态。

## §1 不变式 ①：判据总数 == `samples/` 下一级目录数

| 现取到的判据（左） | 条数 | `samples/` 一级目录（右） | 个数 | 集合相等 |
| :-- | --: | :-- | --: | :-- |
| CD1、CD2、CD3、CD4、CD5、CD6 | 6 | CD1、CD2、CD3、CD4、CD5、CD6 | 6 | **是** |

★ 两边**现取**：删掉检查器里任一条判据 ⇒ 左少一个；删掉任一样例目录 ⇒ 右少一个；**两边都会当场红**。
★ 该不变式**自带一条自证探针**：喂一对不等集合必判否 ⇒ **OK**（断言没被架空）。

## §2 RED 侧：逐条判据的**违规样例**实测读数（`violate/`）

### §2.1 汇总（机器抽取：逐条 status）

| 判据 | 它自己这条 | 同侧其余判据 | 该侧 `exit` | 只红它自己 |
| :-- | :-- | :-- | --: | :-- |
| `CD1` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |
| `CD2` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |
| `CD3` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |
| `CD4` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |
| `CD5` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |
| `CD6` | **FAIL** | 其余 5 条 = PASS | 1 | **是** |

★ 每行**只评「它自己那条」红没红**（设计 §5 的对照口径）；**不评别的**。

### §2.2 RED 原始 stdout（逐条判据的 `violate/` 跑一遍 · **逐字**贴检查器输出）

**`CD1`** —— 打的是：求解入口固定随机源（MATLAB `rng(` / Python `default_rng`|`.seed(`）；per-file 启发式

```
$ check-code.py --scope artifact tests/skills/code/samples/CD1/violate/code --appendix tests/skills/code/samples/CD1/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD1/violate/code
      | appendix = tests\skills\code\samples\CD1\violate\appendix.md
      | FAIL  CD1  势=2（代码文件）· 用随机未固定 2 个  <<< solve.m ; solve.py
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD1）
```

**`CD2`** —— 打的是：结果落盘（`save`/`writetable`/`to_csv`/`savefig` …），且**不只有** `disp`/`print`

```
$ check-code.py --scope artifact tests/skills/code/samples/CD2/violate/code --appendix tests/skills/code/samples/CD2/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD2/violate/code
      | appendix = tests\skills\code\samples\CD2\violate\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | FAIL  CD2  势=2（代码文件）· 落盘惯用法 无 · 问题 2 处  <<< 只打印未落盘：solve.m/solve.py ; 整个代码集无任何落盘惯用法（空集不许判绿）
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD2）
```

**`CD3`** —— 打的是：结果文件名带论文编号，与正文 图 X / 表 Y / 式 Z 对得上

```
$ check-code.py --scope artifact tests/skills/code/samples/CD3/violate/code --appendix tests/skills/code/samples/CD3/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD3/violate/code
      | appendix = tests\skills\code\samples\CD3\violate\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | FAIL  CD3  势=2（清单行）· 编号对不上/缺编号 1 处  <<< 第2行 文件名 table-2 与正文 table-1 对不上
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD3）
```

**`CD4`** —— 打的是：论文附录里**不含程序正文**（`[官方]` `corpus/official/instructions.html:1227` / `:1305`）

```
$ check-code.py --scope artifact tests/skills/code/samples/CD4/violate/code --appendix tests/skills/code/samples/CD4/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD4/violate/code
      | appendix = tests\skills\code\samples\CD4\violate\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | FAIL  CD4  势=14（附录行）· 程序正文命中 3 处  <<< 第7行「```」 ; 第8行「function out = solve(seed)」 ; 第12行「```」
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD4）
```

**`CD5`** —— 打的是：**可执行语句内**没有写死的机器绝对路径（`C:\` / `D:\` / `/Users/`）；**注释内不算**

```
$ check-code.py --scope artifact tests/skills/code/samples/CD5/violate/code --appendix tests/skills/code/samples/CD5/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD5/violate/code
      | appendix = tests\skills\code\samples\CD5\violate\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | FAIL  CD5  势=2（代码文件）· 可执行语句内绝对路径 2 处（注释内不算）  <<< solve.m:5「D:\」 ; solve.py:13「C:\」
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD5）
```

**`CD6`** —— 打的是：★ 人机确认闸：结果清单在场、五列非空，且凡 `代码来自=AI` 的行有「跑过人 + 日期 + 已核」（`P6`）

```
$ check-code.py --scope artifact tests/skills/code/samples/CD6/violate/code --appendix tests/skills/code/samples/CD6/violate/appendix.md   → exit=1
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD6/violate/code
      | appendix = tests\skills\code\samples\CD6\violate\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | FAIL  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 1 处  <<< 第1行；仍为「待核」
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 1 条 · N/A 0 条
      | RESULT: FAIL（CD6）
```

## §3 GREEN 侧：逐条判据的**合规样例**实测读数（`comply/`）

### §3.1 汇总（机器抽取：逐条 status）

| 判据 | `comply/` 全员 status | 该侧 `exit` | 全绿 |
| :-- | :-- | --: | :-- |
| `CD1` | 全 PASS | 0 | **是** |
| `CD2` | 全 PASS | 0 | **是** |
| `CD3` | 全 PASS | 0 | **是** |
| `CD4` | 全 PASS | 0 | **是** |
| `CD5` | 全 PASS | 0 | **是** |
| `CD6` | 全 PASS | 0 | **是** |

### §3.2 GREEN 原始 stdout（逐条判据的 `comply/` 跑一遍 · **逐字**贴检查器输出）

**`CD1`** —— 打的是：求解入口固定随机源（MATLAB `rng(` / Python `default_rng`|`.seed(`）；per-file 启发式

```
$ check-code.py --scope artifact tests/skills/code/samples/CD1/comply/code --appendix tests/skills/code/samples/CD1/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD1/comply/code
      | appendix = tests\skills\code\samples\CD1\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`CD2`** —— 打的是：结果落盘（`save`/`writetable`/`to_csv`/`savefig` …），且**不只有** `disp`/`print`

```
$ check-code.py --scope artifact tests/skills/code/samples/CD2/comply/code --appendix tests/skills/code/samples/CD2/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD2/comply/code
      | appendix = tests\skills\code\samples\CD2\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`CD3`** —— 打的是：结果文件名带论文编号，与正文 图 X / 表 Y / 式 Z 对得上

```
$ check-code.py --scope artifact tests/skills/code/samples/CD3/comply/code --appendix tests/skills/code/samples/CD3/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD3/comply/code
      | appendix = tests\skills\code\samples\CD3\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`CD4`** —— 打的是：论文附录里**不含程序正文**（`[官方]` `corpus/official/instructions.html:1227` / `:1305`）

```
$ check-code.py --scope artifact tests/skills/code/samples/CD4/comply/code --appendix tests/skills/code/samples/CD4/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD4/comply/code
      | appendix = tests\skills\code\samples\CD4\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`CD5`** —— 打的是：**可执行语句内**没有写死的机器绝对路径（`C:\` / `D:\` / `/Users/`）；**注释内不算**

```
$ check-code.py --scope artifact tests/skills/code/samples/CD5/comply/code --appendix tests/skills/code/samples/CD5/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD5/comply/code
      | appendix = tests\skills\code\samples\CD5\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

**`CD6`** —— 打的是：★ 人机确认闸：结果清单在场、五列非空，且凡 `代码来自=AI` 的行有「跑过人 + 日期 + 已核」（`P6`）

```
$ check-code.py --scope artifact tests/skills/code/samples/CD6/comply/code --appendix tests/skills/code/samples/CD6/comply/appendix.md   → exit=0
      | check-code.py · scope=artifact
      | target   = <REPO>/tests/skills/code/samples/CD6/comply/code
      | appendix = tests\skills\code\samples\CD6\comply\appendix.md
      | PASS  CD1  势=2（代码文件）· 用随机未固定 0 个
      | PASS  CD2  势=2（代码文件）· 落盘惯用法 有 · 问题 0 处
      | PASS  CD3  势=2（清单行）· 编号对不上/缺编号 0 处
      | PASS  CD4  势=9（附录行）· 程序正文命中 0 处
      | PASS  CD5  势=2（代码文件）· 可执行语句内绝对路径 0 处（注释内不算）
      | PASS  CD6  势=2（清单行）· 五列有空/取值非法 0 处 · `代码来自=AI` 的行 1，未确认 0 处
      | ------------------------------------------------------------------------------
      | 判据 6 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

## §4 不变式 ②：`CD6`（人机确认闸）的红来自「确认缺失」那一行本身（`P6` 的核心）

**机器交叉核**（两条独立路径对齐）—— 路径 1 = 检查器判词里**报出的行号**；路径 2 = 从结果清单里**独立读出**的「`代码来自=AI` 且 `确认` 未「已核」」的**行号**。

| 侧 | `代码来自=AI` 的行（路径 2） | 其中「确认缺失」的行（路径 2） | 检查器**报出**的行（路径 1） | `CD6` status | 对齐 |
| :-- | :-- | :-- | :-- | :-- | :-- |
| `CD6/violate` | [1] | [1] | [1] | FAIL | **是** |
| `CD6/comply` | [1] | [] | （空） | PASS | **是** |

★ **读法**：`violate/` 侧把**确认那格**从「已核（…）」改成「待核」；该侧还改了**清单标题行**（`# 结果清单（样例）` → `# 结果清单（样例 · CD6 违规侧：AI 行未确认）`）—— **改动不止确认格**（`diff …/comply/… …/violate/…` 可见两处：标题行 + 确认格）；`CD6` 的 `FAIL` 判词 **`<<< 第1行；仍为「待核」`** 报的正是**那条 AI 行本身**（不是别行、不是别的判据连坐）⇒ 这就是设计 §1.2 那句边界话的**机械落地**。
★ **`comply/` 侧**同一行填「已核（…, 日期）」⇒ `CD6` 判 `PASS` ⇒ **正反真的分得开**。
★ 该不变式**不靠手抄行号**：行号由**结果清单当场读出**、再与**检查器报出**的行号**集合比对**。

## §5 诚实边界（**不声称穷尽** · 手写）

- ★★ **样本量边界（原话）**：**样例是构造的** —— 每条判据**只钉一对**（`comply` + `violate`），`n` 小 ⇒ **本文只证明「判据真的会红 / 会绿」，不代表真实赛期表现、也不覆盖全部失效形态**。**凡本文列的清单都不声称穷尽。**
- ★ **RED / GREEN 是「样例驱动」的**（设计 §5）：**不另起写手 agent 作对照** ⇒ 它**证明不了**「一个不看 skill 的写手会不会踩同样的坑」——**那是另一支（M4）的口径，本支不做**。
- ★ **外检是启发式**（设计 §4.4）：`CD1`/`CD2`（per-file 随机源 / 落盘花名）、`CD3`（只判文件名↔清单编号对应，不查文件是否真落盘）、`CD4`（两层强信号，**有假阳性面**：`class 词:` / `function 词(` 起首的散文行可能被误判）、`CD5`（路径形态启发式）**都有假阳性 / 假阴性面**；本文只如实贴某一次读数，**不背书内容对错**。
- ★ **`CD4` 的前提**：`CD4` 只在给了 `--appendix` 时判；不给 ⇒ `N/A`（本文的每对都给了 `--appendix`）。
- ★ **只评「判据红没红」**：本文不对样例产物的**质量**下任何判断（设计 §5 的对照口径）。

## §6 可重放性（**不动点**：先干净 → 捕获 → 提交 → 再跑一次）

- **本文件完全由生成器当场产出**：`python tests/skills/code/make-evidence.py`（跑完 `git status --short` 应为空）。
- **不动点的证法**：在**已提交的树上**、**同一操作系统内**重跑本生成器 ⇒ **本文件逐字节不变**（跑后 `git status --short` 仍为空）；**平台边界见下条**。
- **非确定性被逐项堵住**：无时间戳 / 无 `random` / 无 `set` 遍历序（一律 `sorted()`）/**无绝对路径**（检查器 stdout 的仓根前缀已脱敏为 `<REPO>/…`；`CD4` 判词回显的 `\begin{…}` 不含仓根前缀，**未动**）⇒ **不写「生成日期」这类会漂的字段**。
- ★ **平台边界（非跨平台规范形）**：本件内含**检查器 stdout 逐字捕获的 Windows 反斜杠相对路径**（如 `appendix = tests\…` —— `pathlib` 在 Windows 上按 `os.sep` 渲染）⇒ **不动点只在同一操作系统内成立**；换 Linux/macOS 重跑**不再逐字节一致**。
- **它实跑**：`check-code.py`（逐对 ×2 侧 + 一次 `--scope artifact` 现取判据 + 不变式 ② 的两次 + 一次 `--scope self`）。

## §7 生成器口径与数据来源（机器抽取 · blob 当场跑 `git hash-object`）

- 生成器 `tests/skills/code/make-evidence.py` blob `2bde75cda59e`。
- 检查器 `.claude/skills/mcm-code/check-code.py` blob `8f8efa433076`（本支不动它）。
- 样例夹具逐件 blob：

| 夹具 | blob |
| :-- | :-- |
| `tests/skills/code/samples/CD1/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD1/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD1/comply/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD1/comply/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD1/violate/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD1/violate/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD1/violate/code/solve.m` | `2de1d66c5e4a` |
| `tests/skills/code/samples/CD1/violate/code/solve.py` | `2862f434fd59` |
| `tests/skills/code/samples/CD2/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD2/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD2/comply/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD2/comply/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD2/violate/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD2/violate/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD2/violate/code/solve.m` | `630d312c45e4` |
| `tests/skills/code/samples/CD2/violate/code/solve.py` | `534077b37e3f` |
| `tests/skills/code/samples/CD3/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD3/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD3/comply/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD3/comply/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD3/violate/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD3/violate/code/result-manifest.md` | `ca0fd647cb4f` |
| `tests/skills/code/samples/CD3/violate/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD3/violate/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD4/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD4/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD4/comply/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD4/comply/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD4/violate/appendix.md` | `5fe26819a3a1` |
| `tests/skills/code/samples/CD4/violate/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD4/violate/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD4/violate/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD5/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD5/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD5/comply/code/solve.m` | `0056924583b5` |
| `tests/skills/code/samples/CD5/comply/code/solve.py` | `94f13c81edc8` |
| `tests/skills/code/samples/CD5/violate/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD5/violate/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD5/violate/code/solve.m` | `58d9af0979bf` |
| `tests/skills/code/samples/CD5/violate/code/solve.py` | `5f90cf0eb799` |
| `tests/skills/code/samples/CD6/comply/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD6/comply/code/result-manifest.md` | `8da4c5a019a9` |
| `tests/skills/code/samples/CD6/comply/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD6/comply/code/solve.py` | `ac4e7e1fa59b` |
| `tests/skills/code/samples/CD6/violate/appendix.md` | `35865e6408d3` |
| `tests/skills/code/samples/CD6/violate/code/result-manifest.md` | `968b9969f1a7` |
| `tests/skills/code/samples/CD6/violate/code/solve.m` | `b1c40c7c6982` |
| `tests/skills/code/samples/CD6/violate/code/solve.py` | `ac4e7e1fa59b` |

- **内检 `--scope self`（补充读数，非 RED/GREEN）**：

```
$ check-code.py --scope self   → exit=0
      | check-code.py · scope=self
      | skill-dir = <REPO>/.claude/skills/mcm-code
      | PASS  SELF1  势=2（边界句）· 缺 0 句
      | PASS  SELF2  势=8（内部指针）· 悬空 0 条
      | PASS  SELF3  势=1（模板表头）· 不符 0 处
      | ------------------------------------------------------------------------------
      | 判据 3 条 · 红 0 条 · N/A 0 条
      | RESULT: PASS
```

- ★ **本文不声称穷尽**：只覆盖 `samples/` 里**现存的**那一对一夹具 + 检查器判的那几条判据。
