# `tests/skills/` —— 家族证据件的**重生成次序**（`mcm-table` Task 1 实测，2026-10-02）

## 0. 为什么需要这张表

一个新家族 skill 落地（`mcm-table`）会让
`tests/skills/figure-choose/check-spec-pointers.py` 的**家族普查读数**变化：

- `扫到 8 个 skill` → **9 个**；`绘图家族 3 个` → **4 个**。

⇒ 一批**证据件（捕获件）** 过期，必须**按各自的生成器**重生成。
**而这些生成器之间有次序约束**（`mcm-plot-origin` 那支踩过一次：次序跑反 ⇒ **烤进一次假红**）。

## 1. 七台生成器（六台「内嵌驱动器」+ 一台「重放式」）

| # | 生成器 | 它内嵌跑什么 | 读**全仓** `git status --short` 吗 |
| :- | :--- | :--- | :--- |
| 1 | `figure-choose/gen-chart-types-verify.py` | `mutate-figure-style.py` | **否**（只 `git hash-object`） |
| 2 | `figure-choose/gen-house-style-verify.py` | 同上 | 否 |
| 3 | `figure-choose/gen-pointer-verify.py` | 同上 | 否 |
| 4 | `figure-choose/gen-skill-verify.py` | 同上 | 否 |
| 5 | `plot-python/gen-plot-style-verify.py` | `plot-python/mutate-plot-style.py`（**末行断言全仓为空**） | **是** |
| 6 | `plot-matlab/gen-plot-matlab-verify.py` | `plot-matlab/mutate-plot-style.py`（**末行断言全仓为空**） | **是** |
| 7 | `figure-choose/gen-figure-style-baseline.py`（**重放式**，`1`/`2` 两相） | 重跑它在 `.txt` 里登记的命令（含 `mutate-figure-style.py`） | 否，但 `§8.5` 必须**提交后**跑 |

## 2. 正确次序（实测）

```
① 1–4 四台 figure-choose 生成器 —— 可**背靠背**跑；末尾**一次**提交四份 *-verify.txt
② 5 plot-python 生成器 跑 → ★**提交** plot-style-verify.txt     ← 中间必须提交
③ 6 plot-matlab 生成器 跑 → ★**提交** plot-matlab-verify.txt
④ 7 重放式生成器：
     相 1（干净树）→ 提交 → 相 1 再跑到**不动点**（只动 §8.4 自指字节行）→ 提交
     → 相 2（提交后，更新 §8.5）→ 提交
     → 相 1 再跑到不动点（自指字节行随 §8.5 的长度变化）→ 提交
```

★ **② 与 ③ 之间那次提交是 load-bearing 的。**

- **机制（读源码得到）**：`plot-python/mutate-plot-style.py` 与 `plot-matlab/mutate-plot-style.py`
  的末行都是 `return 0 if (… and not dirty) else 1`，而 `dirty` 取自**全仓** `git status --short`。
  ⇒ 不提交就接着跑，后一台会读到前一台**刚写脏的捕获件** ⇒ 把自己的结论判成"树脏" ⇒ **红**。
- **实测（本任务现场）**：当 `git status --short` 显示 `M tests/skills/plot-python/plot-style-verify.txt`
  时，直接跑 `python tests/skills/plot-matlab/mutate-plot-style.py` ⇒ 它的判据变异**全部达标**
  （`MUT: 6/6 红` · `对照 2/2 达预期`），但末行 `git status --short`（应为空）印出那条 `M …`，
  **退出码 = 1**。⇒ 若那时跑整台 plot-matlab 生成器，它的 `[2/9]`（期望 `exit 0`）会记成 `exit=1`
  ⇒ **假红入档**。（本任务**没有**真跑那台生成器去撞，只跑了它的驱动器来取证。）
- **① 那四台为什么不冲突**：它们只做 `git hash-object`，**不读** `git status`
  ⇒ 实测把四台**背靠背**跑、树逐台变脏，**四台全部 `rc=0`**、且只写各自的捕获件。

## 3. 不动点判据（怎么证"跑对了"）

- 每跑完一台、**提交一次 ⇒ `git status --short` 为空**；
- **每台生成器在已提交的树上重跑 ⇒ 它那份捕获件逐字节不变**
  （判据形态：重跑后 `git status --short` **仍为空** —— 捕获件一个字节都没动）。

## 4. 本次的跑法（`mcm-table` Task 1 · 2026-10-02 · 基线 `8da85d7`）

| 次序 | 生成器 | 提交 | 捕获件 | `git hash-object` |
| :-- | :--- | :--- | :--- | :--- |
| ① | `figure-choose/gen-chart-types-verify.py` | `b3c1404` | `tests/skills/figure-choose/chart-types-verify.txt` | `1166e36a2be2a00dc9c903e82da99cade6754ec0` |
| ① | `figure-choose/gen-house-style-verify.py` | `b3c1404` | `tests/skills/figure-choose/house-style-verify.txt` | `ddae4fc8d4d7a8cd510030e978f504819d3c4917` |
| ① | `figure-choose/gen-pointer-verify.py` | `b3c1404` | `tests/skills/figure-choose/pointer-verify.txt` | `10d1e59f61c4303d474f85229f56b596e49b227c` |
| ① | `figure-choose/gen-skill-verify.py` | `b3c1404` | `tests/skills/figure-choose/skill-verify.txt` | `52a1b706db8c27d219bc50eed468e23f69dcdf31` |
| ② | `plot-python/gen-plot-style-verify.py` | `089dceb` | `tests/skills/plot-python/plot-style-verify.txt` | `7d74b1174ddf642129237aa58d610f5643785ba9` |
| ③ | `plot-matlab/gen-plot-matlab-verify.py` | `5de22b1` | `tests/skills/plot-matlab/plot-matlab-verify.txt` | `3f85092239d2cadd1311a78bf1b9bdabe60794c8` |
| ④ | `figure-choose/gen-figure-style-baseline.py 1` → `5a3181a` → `2` → `1` | `3766415`/`5a3181a`/`9ebef9c`/`1c7dc93` | `tests/skills/figure-choose/figure-style-baseline.txt` | `36db2ad9bb8cbdc26ed3ec5f32e9cfa230c52634` |

**差异来源**（逐类都可在 `git show <commit>` 里核）：

- **census 一类**：`M43` 前置「真仓扫到 8→9 个 skill / 绘图家族 3→4 个」；
  `M45` 的 `K3` 家族 FAIL 列表多出 `K3@mcm-table`（且「全跑共红 4→5 条」）；
  `check-spec-pointers.py` 的普查块多一行 `家族  mcm-table`。
- **字节一类**：`figure-style-baseline.txt §8.4` 的落盘字节行
  （`chart-types 59369→59382` · `house-style 85011→85024` · `pointer 48789→49275` ·
  `skill-verify 64292→64305` · `baseline 自指 93866→93872`）。
- **顺带订正一处先存漂移**：`§8.4` 的 `gen-style-table.py 37239→40688` —— 该件在 `ef89bf9`
  （origin 终审修复轮）改过，当时的基线未同步；**不是**本支改动。

## 5. 例外与边界（**不声称穷尽**）

- 这七台**不是** `tests/skills/` 下的全部生成器：另有 `figure-choose/gen-style-table.py`
  （派生 `mcm-style.json`）、`plot-python/gen-mcm-style.py`、`plot-matlab/gen-mcm-style-matlab.py`、
  各 `fixtures/make-fixtures.py` 与 `make-evidence.py` —— 它们的重生成条件见各自文件头。
- ★ **补充：`mcm-schematic` 支的两个生成器（2026-10-03 补登）** ——
  `tests/skills/schematic/make-evidence.py`（重生成 `tests/skills/schematic/red-green-evidence.md`）
  与 `tests/skills/schematic/fixtures/make-fixtures.py`（重生成骨架族的 `<名>.pdf` / `<名>.check.txt` /
  `<名>.build.txt`）；两支**都不在上表**。它们的重生成**触发条件 = `check-figure-style.py` 的 blob 变时**
  （两支都调它出判词；`make-evidence.py` 另外断言该 blob == `HEAD`）。
  ★ **`make-evidence.py` 的文件头没写**这条触发条件 ⇒ **以本行为准**（不把重跑条件只寄在文件头里）。
  ★ 该触发条件**不声称穷尽**：本支**样式层 `schematic-style.tex` 或骨架 `.tex` 里会落到产物上的那部分变了**、
  也会改这两支的产物（判据的允许集合来自样式层）。
  ★ 反过来：**只改注释**这类**不进产物**的编辑 ⇒ 产物逐字节不变、**不必**重生成
  （别把上一行读成"动了骨架 `.tex` 就得重跑"；无任何守卫哈希骨架 `.tex`）。
- ★★ **登记（2026-10-10）：`figure-choose` 的四份 `*-verify.txt` 当前**不满足 §3 的不动点判据**。**
  实测：在**已提交的树**上跑 `gen-{chart-types,house-style,pointer,skill}-verify.py` ⇒ **四份全部被改写**。
  **逐份 diff 分类：差异只有一类 —— 技能普查数 `扫到 10 个 skill` → `扫到 17 个 skill`**
  （`pointer` 那份还把 7 个新 skill 展开成 `非家族 …` 行）；**没有任何一条差异与绘图 / 示意图判据有关**。
  ⇒ 这是**技能逐个落地后没人重跑这四台**造成的**既有漂移**（§4 的登记值停在 `b3c1404` 那一轮），
  **不是**任何一条绘图改动的涟漪。
  ★ **本轮（2026-10-10 `mcm-schematic` 视觉语言改版）当场验过：该改动对这四份的判词影响 = 0**
  （跑完逐份 diff，命中的只有普查那一行；四份已**回退**、blob 与改动前逐字节相同）。
  ⇒ **修它得连第 7 台一起走** —— `figure-style-baseline.txt` **同样含普查行**（实测 1 处），
  且它自己的重生成要按 §2 的次序表与 `§8.4`/`§8.5` 的提交仪式。
  **只刷新前四台会造成新的内部不一致**（§4 已记过同型先例："Task 2 改了驱动器却没重生成那 5 份转录"）。
  ⇒ **本轮刻意不修，如实登记。**
- 上表「读不读 `git status`」那一列是**读源码**逐台查的（扫串 `git status --short` 与
  `return 0 if (… and not dirty)`），**不是**穷举跑出来的；**次序**那一列是**实测**的。
- `tests/m3-*-recon/` 下的探针捕获**不在本表**：它们是一次性**取证现场**，纪律不同
  （见各自目录 `README.md`；其中 `m3-matlab-recon` 有两支探针在新 skill 落地后会崩 ⇒ 其捕获**冻结为历史**）。
- **`figure-style-baseline.txt` 的 `§8.1` 不属于「重跑逐字节不变」的射程**：该节标题即
  「提交**前**的 `git status --short`（本轮的改动尚未入库）」，记的是**那一刻**工作树还没提交的 6 个文件；
  在**干净 `HEAD`** 上重跑生成器，同一节会写成**空**（`git status --short` 无输出，此时没有未提交改动）。**这是设计如此**
  （2026-10-03 控制者裁定），**不改生成器行为**。⇒ 判「baseline 是否跑对了」要看的是
  `§2–§8.4` 的**逐条重放**与 `§8.5` 的**提交后 blob 自证**，**不是** `§8.1` 那一段。
- 本表**不覆盖** `docs/` 散文里的旧读数（例：`docs/mcm-writing-discipline.md` 记的
  `.claude/skills/` 目录数）。★ **订正（2026-10-02，`mcm-table` Task 1）**：那一处**本任务就同批清了**
  （它一红就是 `check-writing-discipline.py` 的 `A9`，而 `A9` **不在两道收工门里**）
  —— 原句"那类现值的订正归各模块的「全库收口」任务"**已不准确**，故改成本句；
  其余同类现值的订正**仍归各模块的「全库收口」任务**（**本句不声称穷尽**）。
