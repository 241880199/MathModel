# `abs-cases/green/` — `mcm-abstract` skill 的 GREEN 阶段产物（正面对照）

**GREEN 阶段** = "TDD for skills" 的第二步：**装上 skill 之后，agent 是否不再失败**。
本目录冻结的是那次实验的**产物**（3 份 `.tex` + 3 份 `-note.md`），全部逐字节复制，
未重新排版、未加头注（复制校验见文末）。

> **一句话分工**
> - **RED 侧**（`../red/`，6 份）：**没有** skill 时的产物 → 用来证明"确有失败"。
> - **GREEN 侧**（本目录，3 份）：**装上** skill 后的产物 → 用来证明"skill 真的把它治好了"。
> - 两侧合起来构成一份 positive control：**同场景、同输入、只差 skill 装没装**。

---

## 一、本目录的 6 份文件

每份 GREEN 产物都是一对：**`.tex`（产物本体）+ `-note.md`（写手的产出说明/取舍/不足）**。

| 文件 | 是什么 | 场景 |
|---|---|---|
| `G1.tex` | A 题摘要页，LaTeX 源码（**只含摘要页**，可独立编译） | **A 题齐全**（正文 `../case-A-body.md`，结果完整） |
| `G1-note.md` | G1 写手的产出说明：用了什么 skill、哪几条没照做及原因、它自己另挖出的正文矛盾、逐数字出处表 | 同上 |
| `G2.tex` | C 题摘要页，LaTeX 源码 | **C 题齐全**（正文 `../case-C-body.md`） |
| `G2-note.md` | G2 写手的产出说明：为何是 `.tex`、题面逐条映射表、三处矛盾数的取舍、还没做到的地方 | 同上 |
| `G3.tex` | A 题摘要页，LaTeX 源码 | **A 题结果不全**（正文 `../case-A-body-partial.md`，Task 2 的数值结果**不存在**） |
| `G3-note.md` | G3 写手的产出说明：怎么处理"Task 2 没有结果"、哪些正文数字没带进摘要、自检证据 | 同上 |
| `README.md` | 本文件 | — |

**三份场景的差别（一句话）**：G1 是"材料齐全的正常题"，G2 是"**不告诉它有这个 skill**、看它会不会自己触发"，
G3 是"**正文只写了一半**、看它会不会编数据"。三个场景**互不相同**，所以是三条独立的证据，不是三次重复采样。

> **G2 的特别之处**：派发时**没有提** `mcm-abstract`。它自己发现并调用了该 skill（触发准确），
> 且独立执行了同一条数字纪律（`G2-note.md` §2）。这是"触发条件写对了"的证据。

## 二、RED 六份 vs GREEN 三份 —— 同一批场景的两侧

**对照关系**（场景是配对键；**RED 的压力探针在 GREEN 侧没有对应物**，见下）：

| 场景 | RED 侧（无 skill） | GREEN 侧（装 skill） |
|---|---|---|
| **A 题齐全** | `../red/red-A1.md`、`../red/red-A2.md`（同输入独立采样两份） | `G1.tex` |
| **C 题齐全** | `../red/red-C1.md` | `G2.tex` |
| **A 题结果不全**（正文是 `case-A-body-partial.md`） | `../red/red-A3-partial.md` | `G3.tex` |
| **压力：队友要求"估个数先写上"** | `../red/red-P1.md` | **无对应**（GREEN 侧未重复这一压力） |
| **压力：要求"把引言两段直接搬"+"随便挑几个显眼的数字"** | `../red/red-P2.md` | **无对应**（同上） |

> ⚠️ **必须写明的缺口**：GREEN 侧**只重跑了 3 个非压力场景**。
> RED 的两条**压力探针**（P1 编数诱惑、P2 搬引言+挑数）**在 GREEN 侧没有被复测**——
> 所以"装上 skill 后权威压力还会不会放宽纪律"这个问题，**本目录不提供证据**。
> `red-P2.md` 已被 controller 裁为**一次真实失败**（见 `../../abs-red-evidence.md` §4.0 与 `../README.md` §三.6）。

## 三、为什么不入库那些 PDF / PNG

`build/abs-green/` 里另有 9 份非文本产物（入库时实测）：`G1-check.pdf`、`G1-check.png`、`G2.pdf`、
`G3-check.pdf`、`G3-mine.pdf`，以及上游为"`C1` 判据修改"做的四份验收产物
`good-summary-verify.pdf`、`official-asset-verify.pdf`、`silent-percent-verify.pdf`、`trailing-comment-verify.pdf`。
**本目录一律不收**，理由三条：

1. **体积**：单份 94 KB–283 KB，纯属副产物，与"sources of truth"无关。本目录 6 份文本合计约 43 KB。
2. **不可逐字节复现**：同一份 `.tex` 每次编译，PDF 都带新的 `/CreationDate`、`/ModDate`
   与由它们派生的 `/ID`（同机同 TeX 版本下，两次产物只有几十字节不同，排版几何完全一致）。
   拿 PDF 的哈希当基准会误判"不稳定"——**能当基准的是机检报告，不是 PDF**。
3. **可由脚本现场重生成**：任何一份都能用随 skill 交付的检查器现编出来：

   ```
   python .claude/skills/mcm-abstract/check-summary.py tests/skills/abs-cases/green/G1.tex \
          --pdf build/regen/G1-check.pdf
   ```

   （`--pdf` 指到仓库的 gitignored 暂存区，别把 PDF 写回 `tests/`；**省略 `--pdf` 会把 PDF 写到输入文件所在目录**。）
   三份的重生成结果与结论见 `../../abs-green-evidence.md` §1。

   > 那四份 `*-verify.pdf` 是**上游**做的验收产物。本次落库**没有**采信它们——
   > 而是按同样的用例**自己重跑了一遍**检查器，三例全过，见 `../../abs-green-evidence.md` §1.3。

## 四、产物为什么必须入库

`build/` 是 gitignored 的暂存区（`.gitignore:6`）⇒ 放在那里等于丢失。
这三份 `.tex` 是 **agent 的采样输出，不可再生**：同一个输入再跑一次 agent，得到的是**另一份**文字。
它们的**机检结论**（页数 1 / A1–A4 PASS / C1–C6 全 0 / 退出码 0）是**可复算的**——
只取决于文件内容，跑一遍 `check-summary.py` 就能复现（这正是 `../../abs-green-evidence.md` 所做的事）。
（机检报告里另有一行 `C1b_行尾注释_不计违规`，三份分别报 4 / 15 / 13——那是**合法**行尾注释与整行注释的计数，
**不计违规**、不参与 `RESULT`；口径见 `../../abs-green-evidence.md` §1.2。）

> **交稿前必改**：三份都填了**占位队号**（G1 `2534567` / G2 `2400001` / G3 `2401056`），
> 不是真实控制号。真提交前必须换成真队号。见 `../../abs-green-evidence.md` §4.1。

---

## 复制校验

本目录 6 份文件均为 `build/abs-green/` 对应文件的**逐字节副本**（入库时实测）：

| 文件 | 字节数 | sha256（前 16 位） |
|---|---|---|
| `G1.tex` | 7637 | `ee3b526c407b41d2` |
| `G1-note.md` | 8944 | `db86d0f2bb210069` |
| `G2.tex` | 7142 | `26de862c59679501` |
| `G2-note.md` | 6910 | `e2a65df29e07d519` |
| `G3.tex` | 6945 | `bcaf94d9d5e2aec0` |
| `G3-note.md` | 5387 | `b9a52520ca846972` |

重算：`python -c "import hashlib,glob;[print(f, hashlib.sha256(open(f,'rb').read()).hexdigest()[:16]) for f in sorted(glob.glob('tests/skills/abs-cases/green/*'))]"`
