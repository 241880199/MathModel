# `MEMO-evidence.md` —— `mcm-memo` 的证据（同一把尺：`check-memo.py` 的 `MO1–MO4`）

**本文件由 `tests/skills/memo/make-evidence.py` 当场跑命令生成**（`write_bytes`、全 LF）。
**不许手改** —— 改读数请改生成器或夹具，然后重跑。

> 生成命令：`python tests/skills/memo/make-evidence.py`
> 复现：在**已提交的树**上重跑本生成器 ⇒ 本文件**逐字节不变**（证法见 §6）。

**同一把尺** = `.claude/skills/mcm-memo/check-memo.py`，对**每份备忘录 × 题面组合**
跑同一条命令形态：`python check-memo.py <memo.tex> [--problem <题面>]`。
★ **判据清单现取**（从检查器 stdout 的 `PASS|FAIL|SKIP` 行里读 id），**不写死条数**。

## §1 两条官方规则（本 skill 的判据源头；★ 仅见于 `corpus/official/MCM-ICM_Tips.txt`）

| # | 规则 | 出处 | 原文（节录） |
| :-- | :-- | :-- | :-- |
| ① | **触发**（每题有**各自**要求，如 required memos or letters） | `MCM-ICM_Tips.txt:160-162` | *"Each problem will have different and specific requirements, such as **required memos or letters**, specific solution format, and/or page limits."* |
| ② | ★★ **匿名落款**（一票否决类） | `MCM-ICM_Tips.txt:239-241` | *"Do not include any type of team identification such as student names, institution name or geographical region. If you are required to include a letter with your submission, be sure not to sign the letter with your name. If you feel as though you need to have a formal closing to such a letter we suggest using: **Sincerely, Team #2000000**."* |

★ **② 最要紧**：漏了它，skill 会把队伍引向**在 letter 上署真名**。两条均标 `[官方]†`（**仅见于 Tips**）。
★ **题面没要求就绝不产出**（★ `[社区]` **操作纪律**；由官方① 推出的**更严推论** —— 官方① *只*说"每题有各自要求（如 required memos or letters）"，**未**禁止主动写 memo）—— memo/letter 是**题目特定要求**，不是通用交付物（`MO1` 判它）。

## §2 判据 `MO1–MO4`（★ 四条都是硬失败 `FAIL`）

| id | 判据 | 出处 | 燃料 / 缺燃料时 |
| :-- | :-- | :-- | :-- |
| `MO1` | 触发条件在场（题面**未**要求 memo/letter ⇒ 不得产出该文件） | `[社区]` 操作纪律（由 `[官方]†` ① `Tips:160-162` 推出） | `--problem`；**缺 ⇒ `SKIP`（不报 `PASS`）** |
| `MO2` | 匿名落款（须为 `Sincerely, Team #<队号>` 一类；真名/校名/机构名 ⇒ 红） | `[官方]†` ② `Tips:239-241` | 备忘录本体；机构词表与"残余标识"判法是 `[社区]` |
| `MO3` | 恰好一页（`pdfLaTeX` 编两遍 + `fitz` 读页数） | `[社区]` 口径（官方只说题面可能有页数要求） | PATH 里 `pdflatex`；**缺 ⇒ `SKIP`** |
| `MO4` | 受众在文首点名（题面点名的受众出现在前 15 非空行） | `[社区]` 口径 | `--problem` 提受众；**缺/提不出 ⇒ `SKIP`** |

★ **"检查器 PASS" ≠ "这份备忘录写好了"** —— 措辞 / 受众适配 / 内容覆盖**仍靠人工**；
  `自查 A14`（题目特定要求）是 `mcm-selfreview` 的**检查侧**，本 skill **只给指针、不复述**。

## §3 夹具身份（逐件当场 `git hash-object`）

| 场景 | 备忘录 | 形态 | 字节 | 行数 | git blob |
| :-- | :-- | :-- | ---: | ---: | :-- |
| `SKL-good` | `good.tex` | `.tex` | 976 | 21 | `6f19ad89111c867c635b9139962a1bfb51b3e955` |
| `SKL-nomemo` | `good.tex` | `.tex` | 976 | 21 | `6f19ad89111c867c635b9139962a1bfb51b3e955` |
| `SKL-noproblem` | `good.tex` | `.tex` | 976 | 21 | `6f19ad89111c867c635b9139962a1bfb51b3e955` |
| `SKL-name` | `name.tex` | `.tex` | 972 | 21 | `ec230029509eb97362faca309881c2cd05480cb8` |
| `SKL-inst` | `inst.tex` | `.tex` | 980 | 21 | `f8f0744f3a621931e1163761b2ee71231bd83898` |
| `SKL-twopage` | `long.tex` | `.tex` | 7072 | 69 | `cff225971177fcab324568d35a67d77eac657204` |
| `SKL-audmiss` | `audmiss.tex` | `.tex` | 976 | 21 | `fd88760b1889b042656721dbe06b5e1dfd0cb13d` |
| `SKL-wma` | `wma.tex` | `.tex` | 983 | 21 | `1d8453c921283f241b10be6ac32e6060a86926a3` |

★ 夹具由本生成器**当场写出**（`build/memo-ev/`，仓内 gitignored）⇒ 上面每个 blob 是**纯函数**读数。

## §4 ★ 读数表（机器读数；同一把尺、逐件跑）

命令形态：`python .claude/skills/mcm-memo/check-memo.py <memo.tex> [--problem <题面>]`

| 场景 | 题面 | 说明 | `MO1` | `MO2` | `MO3` | `MO4` | `RESULT` | exit |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | ---: |
| `SKL-good` | `problem-memo.txt` | 干净的一页备忘录 + **要求 memo** 的题面（应全 `PASS`） | PASS | PASS | PASS | PASS | **PASS** | 0 |
| `SKL-nomemo` | `problem-nomemo.txt` | 题面**不要求** memo ⇒ 产物不该存在（`MO1` → `FAIL`） | FAIL | PASS | PASS | SKIP | **FAIL** | 1 |
| `SKL-noproblem` | （无） | **不给 `--problem`** ⇒ `MO1`/`MO4` = `SKIP`（不是 `PASS`） | SKIP | PASS | PASS | SKIP | **PASS** | 0 |
| `SKL-name` | `problem-memo.txt` | ★ 落款**署真名** ⇒ 违反官方②（`MO2` → `FAIL`） | PASS | FAIL | PASS | PASS | **FAIL** | 1 |
| `SKL-inst` | `problem-memo.txt` | 落款**署校名** ⇒ 违反官方②（`MO2` → `FAIL`） | PASS | FAIL | PASS | PASS | **FAIL** | 1 |
| `SKL-twopage` | `problem-memo.txt` | 灌水成**两页** ⇒ 不是一页（`MO3` → `FAIL`） | PASS | PASS | FAIL | PASS | **FAIL** | 1 |
| `SKL-audmiss` | `problem-memo.txt` | `To:` 行不再点名题面受众（`MO4` → `FAIL`） | PASS | PASS | PASS | FAIL | **FAIL** | 1 |
| `SKL-wma` | `problem-wma.txt` | 另一受众（`World Medical Association`）+ 对应题面（`MO4` = `PASS`） | PASS | PASS | PASS | PASS | **PASS** | 0 |

★ **状态语义**：`FAIL` = 硬失败（退出码非 0）；`PASS` = 过；
  `SKIP` = **无法判定**（缺燃料；**既不是 `PASS` 也不是 `FAIL`**，退出码不受影响）。
★ `SKL-noproblem` 一行证明：**缺 `--problem` 时 `MO1`/`MO4` 报 `SKIP` 而不报 `PASS`**（fail-closed）。

## §5 边界（**如实登记，不放大**）

- **只判形式**：`MO1–MO4` 覆盖不了**措辞 / 受众适配 / 内容覆盖** —— "检查器 PASS" ≠ "写好了"。
- **`MO2` 的机构词表与"残余标识"判法是 `[社区]` 口径**：官方只列举 *"student names, institution name or geographical region"*，**未给词表**。⇒ 词表**不声称穷尽**；落款块**之外**的团队标识（如正文或
  `From:` 行里的真名）**本工具不查** —— 那属于 `自查 A14` / 人工。
- **`MO4` 的受众靠题面里的固定句式**（`memo/letter ... to/for the <受众>`）提取：**提不出 ⇒ `SKIP`**，
  **不猜**；作者换一种措辞写题面就可能提不出 ⇒ 该行**不是**"受众写错"，而是"无法判定"。
- **`MO3` 要能编译**：备忘录须是**可编译的完整 `.tex`**（含 `\documentclass`）；**非 `.tex` ⇒ fail-closed 红**。
- **不判"这段是不是 AI 生成的"**；**不做**全稿提交前合规（那是 `mcm-selfreview`）。
- ★ **本文件不声称穷尽**：以上是**已知**边界，不是"工具的全部局限清单"。

## §6 自证（可重放 / 不动点）

- **检查器 blob**：工作树 `ef6ed6b39822` · 基线 `eb43b39` blob `(基线里无此件)`
- **夹具自证（逐件 blob）**：`SKL-good`=`6f19ad89111c` · `SKL-nomemo`=`6f19ad89111c` · `SKL-noproblem`=`6f19ad89111c` · `SKL-name`=`ec230029509e` · `SKL-inst`=`f8f0744f3a62` · `SKL-twopage`=`cff225971177` · `SKL-audmiss`=`fd88760b1889` · `SKL-wma`=`1d8453c92128`
- **本生成器不记录自身工作树状态**（不嵌 `git status` / 不嵌 `HEAD`，锚点一律用固定基线 `eb43b39`）
  ⇒ 本文件是（夹具字节 + 检查器字节 + 生成器源码）的**纯函数**。
- ★ **不动点证法（通则 14）**：**先干净 → 再捕获 → 再提交 → 再跑一次证不动点** ——
  在**已提交**的树上重跑本生成器，然后 `git status --short` 仍为空、`git diff` 对本文件为空 ⇒ **逐字节不变**。
  （本支执行记录见 `.superpowers/sdd/task-m2-sw-t4-report.md`。）
- ★ **判据逻辑全仓只许一份**：判据本体在 `.claude/skills/mcm-memo/check-memo.py`；
  `tests/` 下**无**镜像版（变异驱动器的 `RUN:` 行盯着这件事）。

