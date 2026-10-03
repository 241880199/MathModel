# `tests/skills/memo/` —— `mcm-memo` 的测试侧

**判据本体不在本目录。** 它**随 skill 走**：

```
.claude/skills/mcm-memo/check-memo.py     ← 判据本体（★ 全仓唯一一份）
```

本仓既有的 `check-*.py` **两种落点都活着**（`mcm-abstract/check-summary.py` 在 skill 目录；
`figure-choose` / `playbook` / `table` / `topic-select` 的在 `tests/`）。本支照 `mcm-abstract` 与
`mcm-section-writer` 的先例**选 skill 目录侧** —— 使用者拿到 skill 就能跑它。
⇒ **`tests/` 下不许再写一份"镜像版"**（两份必然漂移，本仓栽过同型）；驱动器里有一条现取断言盯着这件事
（`RUN:` 行的 "`tests/` 下的 `check-memo.py` 镜像"）。

本目录现有**驱动器 + 证据**（★ **无 `fixtures/`**：夹具由生成器/驱动器**当场写进仓内 `build/`**，用完即清）：

```
tests/skills/memo/
├─ mutate-memo.py        # 变异驱动器（调 skill 目录里那份检查器）
├─ make-evidence.py      # 证据生成器
├─ MEMO-evidence.md      # 由 make-evidence.py 产出（**不许手改**）
└─ README.md             # 本文件
```

---

## 1. 怎么跑

```bash
# ① 变异驱动器：MO1–MO4 逐条证红 + "必须仍绿"的对照
python tests/skills/memo/mutate-memo.py

# ② 证据生成器：产出 MEMO-evidence.md
python tests/skills/memo/make-evidence.py

# ③ 直接跑检查器
python .claude/skills/mcm-memo/check-memo.py <memo.tex> [--problem <题面>]
python .claude/skills/mcm-memo/check-memo.py --help
```

- **临时件只落仓内 `build/memo-mut/` · `build/memo-ev/`**（gitignored；**不落 C 盘 / `%TEMP%` / 盘根**），
  两个脚本收尾都 `shutil.rmtree` 清掉。
- 驱动器收尾自证：受保护件逐个 `git hash-object` 未变 · 干净夹具复跑仍全 `PASS` · `git status --short` 为空。
- ★ **`make-evidence.py` 不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`，锚点一律用固定基线）
  ⇒ 在**已提交的树**上重跑 ⇒ `MEMO-evidence.md` **逐字节不变**（不动点，通则 14）。

---

## 2. 判据、状态与出处

每行输出形如 `<STATUS> <ID> <标题>  # <说明>`；最后一行 `RESULT: PASS|FAIL`。

| id | 判据 | 状态 | 原始出处 |
| :-- | :-- | :-- | :-- |
| `MO1` | 触发条件在场（题面**未**要求 memo/letter ⇒ 不得产出该文件） | **`FAIL`**（硬） | `[社区]` 操作纪律（由 `[官方]†` ① `corpus/official/MCM-ICM_Tips.txt:160-162` 推出） |
| `MO2` | ★★ **匿名落款**（须为 `Sincerely, Team #<队号>` 一类；真名/校名/机构名 ⇒ 红） | **`FAIL`**（硬） | `[官方]†` ② `MCM-ICM_Tips.txt:239-241` |
| `MO3` | 恰好一页（`pdfLaTeX` 编两遍 + `fitz` 读页数） | **`FAIL`**（硬） | `[社区]` 口径 |
| `MO4` | 受众在文首点名（题面点名的受众出现在前 15 非空行） | **`FAIL`**（硬） | `[社区]` 口径 |

**状态语义**：

- **四条都是硬失败（`FAIL`）** —— 与 `check-section.py` 不同，本工具**没有 `WARN` 档**
  （memo 的四项都可机判，且 `MO1`/`MO2` 直接对应官方规则）。
- `SKIP` = **无法判定**（既不是 `PASS` 也不是 `FAIL`）：
  **缺 `--problem` ⇒ `MO1`/`MO4` `SKIP`**；**PATH 里没有 `pdflatex` ⇒ `MO3` `SKIP`**。
  ★ **缺燃料一律报"无法判定"，不许报 `PASS`**（fail-closed）—— 驱动器 `CTRL-no-problem` 盯着这条。
- **退出码**：有 `FAIL` ⇒ **非 0**；只有 `PASS`/`SKIP` ⇒ **0**。

★ **"检查器 PASS" ≠ "这份备忘录写好了"** —— 它只判这四项形式；**措辞 / 受众适配 / 内容覆盖仍靠人工**。
★ **`自查 A14`（题目特定要求，含"要求的 memo 或 letter"）是 `mcm-selfreview` 的检查侧**，
本 skill 只给指针、**不复述 A14 的判据**。

**两条官方规则**（原文见 `MEMO-evidence.md` §1）：

- `[官方]†` **① 触发**（`Tips:160-162`）：题目会有各自不同的特定要求（**required memos or letters** /
  特定解法格式 / 页数限制）⇒ **先读题面**（**这句是官方的**）。
  ★ 由此推出的操作纪律 **`[社区]`**：**题面要求了才写**；**没要求就绝不产出**（memo 是**题目特定要求**，非通用交付物）。
  （★ 官方原文**未**禁止主动写 memo —— "没要求就不写"是本项目据此采取的**更严**处置，故标 `[社区]`。）
- `[官方]†` **② 匿名落款**（`Tips:239-241`，**一票否决类**）：**不得署真名 / 校名 / 机构名 / 地域**；
  要正式收尾用官方建议写法 `Sincerely, Team #<队号>`。★ 漏了它，skill 会把队伍引向在 letter 上署真名。

---

## 3. 驱动器打的是什么（**不声称穷尽**）

| id | 变异 | 期望 |
| :-- | :-- | :-- |
| `MUT-MO1` | 题面**不要求** memo/letter，却产出该文件 | `MO1` → `FAIL` |
| `MUT-MO1-PAPER` | 题面出现 `US Letter or A4`（**纸张尺寸**，不是要求 memo） | `MO1` → `FAIL`（**不误判为"要求"**） |
| `MUT-MO2-NAME` | ★ **落款改成署真名**（`Sincerely, John Smith`）—— 官方硬规则 ② | `MO2` → `FAIL` |
| `MUT-MO2-INST` | 落款改成署**校名**（`Sincerely, Nanjing University`） | `MO2` → `FAIL` |
| `MUT-MO3` | 灌水成**两页** | `MO3` → `FAIL` |
| `MUT-MO4` | 把 `To:` 行的**点名受众**换成别的 | `MO4` → `FAIL` |
| `CTRL-good` | 干净的一页备忘录 + 要求 memo 的题面 | 全 `PASS`、`exit=0` |
| `CTRL-no-sig` | **删掉整个落款**（无正式收尾） | `MO2` **不得** `FAIL`（无落款不违规） |
| `CTRL-other-audience` | 另一份备忘录（`To: the World Medical Association`）+ 对应题面 | `MO4` = `PASS`（不写死某一受众） |
| `CTRL-no-problem` | 不给 `--problem` | `MO1`/`MO4` = `SKIP`（**不是 `PASS`**）、`exit=0` |

★ 每条变异的期望**逐条写死**（与基准逐条比对，**恰好**这些状态变了、且变成什么）：
"该红没红"或"顺手带红了别的判据"都会被当场抓出来。判据清单**现取**（不写死条数）。
★ **判据只从失败方向证明**；**合计行不是末行**（末行放"运行完整性"读数）。

---

## 4. 已知边界（**不声称穷尽**）

1. ★★ **`MO2` 的机构词表与"残余标识"判法是 `[社区]` 口径**：官方只列举
   *"student names, institution name or geographical region"*，**未给词表**。⇒ 词表**不声称穷尽**。
2. ★ **`MO2` 只查落款块**：落款块**之外**的团队标识（如正文或 `From:` 行里的真名）**本工具不查** ——
   那属于 `自查 A14` / 人工。
3. ★ **`MO4` 靠题面里的固定句式**（`memo/letter ... to/for the <受众>`）提取受众：**提不出 ⇒ `SKIP`**，
   **不猜**；作者换一种措辞写题面就可能提不出 ⇒ 该行**不是**"受众写错"，而是"无法判定"。
4. ★ **`MO3` 要能编译**：备忘录须是**可编译的完整 `.tex`**（含 `\documentclass`）；**非 `.tex` ⇒ fail-closed 红**。
   ★ 无 `pdflatex` ⇒ `SKIP`（不是 `FAIL`）。
5. ★★ **`MO1` 的"题面要求"识别有已知误报类（★ 登记，**不修**；★ 本清单**不声称穷尽**）**：
   已登记的成因有 ① `memo`/`memorandum` 的**任意出现**即算"要求"
   （如 `memorandum of understanding`、"the word memo appears in the glossary"）；
   ② `letter` 的**否定式无处理**（如 `Do not write a letter to the editor` 也会被判"要求"）；
   ③ `RE_REQ_LETTER` 在**非交付语境**下也命中（**两个分支都会**）：
   · `\bletter\b[^.\n]{0,40}?\b(?:to|for)\b` 分支**无动作动词也命中** ——
   实测 `The letter to the editor was already published.`（命中 `letter to`）⇒ 被判"要求"；
   · **动作动词分支**（`write/prepare/include/… … letter`）**过宽** ——
   实测 `Please write a letter of recommendation for the dean.`（命中 `write a letter`，是"写推荐信"、
   **非**"题面要求交付 memo/letter"）⇒ 被判"要求"。
   ⇒ 这些**不要求** memo 的题面会被 `MO1` 判成"题面要求 memo/letter"（即 `MO1` **漏报**）。
   ★ **方向一律 = 宁可漏、不误红**（宁可不报这类红）；**修它属改判据面**，本任务只登记（同见
   `check-memo.py` 里 `RE_REQ_MEMO` / `RE_REQ_LETTER` **下方**的注释）。
6. **只判形式**：`MO1–MO4` 覆盖不了措辞 / 受众适配 / 内容覆盖 —— "检查器 PASS" ≠ "写好了"。
7. **不做**判"这段是不是 AI 生成的"；**不做**全稿提交前合规（那是 `mcm-selfreview`）。
8. **本 README 不声称穷尽**：以上是**已知**边界，不是"工具的全部局限清单"。

---

## 5. 证据（由生成器产出，不许手改）

```bash
python tests/skills/memo/make-evidence.py      # 产出 MEMO-evidence.md
```

**同一把尺** = `.claude/skills/mcm-memo/check-memo.py`，对**若干份备忘录 × 题面组合**逐件跑同一条命令形态。
`MEMO-evidence.md` §4 的读数表含 8 个场景（干净件 / 缺题面 / 署真名 / 署校名 / 两页 / 受众缺失 /
另一受众），每个场景的夹具由生成器当场写进 `build/memo-ev/` 并给 `git blob`。
★ **本支没有 RED / GREEN 三臂对照** —— 那是 `mcm-section-writer`（Task 3）的做法；
`mcm-memo` 的"证据"是**检查器在夹具上的机器读数 + 两条官方规则的出处登记**。
