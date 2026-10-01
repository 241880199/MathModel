# M3 `mcm-plot-matlab` 实施计划（2026-10-01）

设计：`docs/superpowers/specs/2026-10-01-m3-plot-matlab-design.md`（本计划的每个"为什么"都在那里）。
上游样式线：`docs/superpowers/specs/2026-09-30-m3-style-single-source-design.md`（载体无关样式表 `mcm-style.json` + 三判据 `F4`/`F5`/`F6`）。
侦察（**已入库**）：`tests/m3-matlab-recon/`（36 件）· `tests/m3-matlab-font-probe/`（40 件）。
先例（照抄其节奏）：`docs/superpowers/plans/2026-09-29-m3-plot-python.md`。

**用户已裁六条（不要再问）**：① 导出载体 = **`print` 家族**为权威（`exportgraphics` 只写用法与风险，不作权威）② 字体 = **系统 `Times New Roman`**（点名即内嵌，**入库 OTF 那条路已否**）③ 每张 figure **显式上浅色主题** ④ 颜色**同值** / 字体**按族等价** / `H11` 不覆盖 ⑤ **验收要把生成的图渲染出来给人看**（通用要求，从本模块起）⑥ 跨版本/跨机**未验**，如实登记。

---

## Global Constraints（**每个任务的复审都要拿到这一份**）

1. **唯一权威**：规范正文只在 `.claude/skills/mcm-figure-choose/references/house-style.md`。本模块**只给指针、不重述**。
   `mcm-plot-matlab/SKILL.md` **必须**含字面量 `references/house-style.md`（`K2`）。
2. **`SKILL.md` 与 `references/**` 零数字字面量**（`K3` 是**子串**判据，普通写法会意外触发）。**要说的数一律回规范去说。**
3. **★ 本模块的命门：不许出现第二份样式来源。** `assets/mcmplot.m` 里的**每一个样式值**只能来自
   `.claude/skills/mcm-figure-choose/assets/mcm-style.json`（生成器读表产出）；`how` 一栏里的规范值一律**回表**去说。
   这条是 `m3-style-single-source` 线的**目的本身**（python 侧先例：`gen-mcm-style.py` 从表读、不再是第二份）。
4. **写入一律 `write_bytes`**（`write_text` 在 Windows 会写 CRLF），**文档与源码全 LF（CRLF=0）**。
5. **凡数字必来自当场跑过的命令**，命令与原始输出贴进证据；**"我没找到" ≠ "它不存在"**（通则 4.5）。
6. **判据脚本 `check-figure-style.py` 一字不改**——RED 与 GREEN 共用同一把尺，这才叫对照。
   ⚠️ 该件的 `F4` 口径 **2026-10-01 刚改过**（改成"外缘环 ∧ 近灰众数"合取）⇒ 本模块**以派发时 HEAD 的版本为准**，
   并把**该件 blob sha 记进每轮证据**（免得日后对不上是哪一版）。
7. **派生件不许手改**：`mcmplot.m` 只许由入库的生成器重放产出。
8. **声明了覆盖就必须有一次真的红**（本仓纪律）。凡"这条判据会拦住 X"，必须有一条**真红**作证；**判据只能从失败方向证明**。
9. **收工门（每个任务都要跑并贴输出）**：`check-house-style.py` → `RESULT: PASS` ·
   `mutate-figure-style.py` → 合计行全红（**现取值不在这里写死** —— 以 `docs/mcm-suite-todo.md`
   §H.5.3 记载的**当场读数**为准；`docs/mcm-suite-todo.md` §H.5.3 为这个字面维护了一份**全库位置
   清单 + 自带复核命令**，在这里再抄一份会让那份清单当场变假。命令 `python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"`，
   **合计行不是末行**；约 225 s）· `run-expected.py` → **`MISMATCH 0 / 34`** ·
   **`check-spec-pointers.py`** → `RESULT: PASS (绘图家族 2 个，K2/K3 全绿)`（**本模块 Task 3 之后**）·
   样式表新鲜度两守卫 + `gen-style-table.py --check`（**15 条一致**）。
   > **不许把提示语当读数列**：`RED-BAD` 只在失败时逐条打印，干净跑里一条都没有（本仓 2026-09-30 栽过）。
10. **不许提交脏树**；每个任务收工 `git status --short` 为空。任务之间**另起提交**，**不许 `--amend`**。
11. **★ 产物必须能被人看见**（用户裁定，通用要求）：每轮的产物 `.png`/`.pdf` 都要**渲染出来**并把路径交给控制者与用户；
    "机械层验不了的用眼睛验"。**写手/agent 必须亲眼看图并写下"从这张图读到了什么"**。
12. **环境（如实登记）**：本机 **R2025b Update 5**，`-batch` 可跑（`/d/Software/Matlab/bin/matlab`）；
    **跨版本/跨机未验**。`run('相对路径.m')` 会把 cwd 切到脚本所在目录（实测）⇒ 出具的 `.m` 脚本**必须**
    用 `mfilename('fullpath')` 反推仓根。
13. **第三方素材**：本模块**无新增**入库二进制（字体走系统 TNR，不装、不复制）。

## 派发指令必带（每次派 subagent 都要附）

- 任务书路径（本文件的那一节 + 该任务的 brief 文件）· 报告落点 `.superpowers/sdd/task-m3-matlab-t<N>-report.md`（**必须真的落盘**）。
- Global Constraints 全文（上面那一节）。
- 明确：**只回报**状态 + 提交 + 一句话测试结论 + 顾虑；**不要把报告内容复制进回复**。
- 基线 commit（派发前的 `HEAD`）——复审的 diff 范围就用它，**不许用 `HEAD~1`**。
- **产物路径**（Global Constraint 11）：让控制者能亲眼看图。

---

## 文件结构（终态）

```
.claude/skills/mcm-plot-matlab/
├─ SKILL.md                     # 短契约（零数字字面量，行数上界 150）
├─ references/workflow.md       # 场景 → 脚本 → 产物 → ★看图（固定一节）
└─ assets/
    └─ mcmplot.m                # ★ 派生件：由生成器从 mcm-style.json 重放产出（勿手改）

tests/skills/plot-matlab/
├─ gen-mcm-style-matlab.py      # 生成器（重放式，入库）
├─ check-style-freshness.py     # 新鲜度守卫（**两臂**，仿 python 侧）
├─ mutate-plot-style.py         # 变异（必须真的红）
├─ probe-h10-band-ink.py        # `H10` 产物级回读（带内墨迹；与 python 侧同型）
├─ red/…                        # 没看过规范的写手产出的产物 + 判词
├─ green/…                      # 走模块的产物 + 判词
└─ plot-style-verify.txt        # 对照与全量读数（生成器产出）

tests/m3-matlab-recon/          # 既有 36 件；本线**重捕获**其中 2 件过期件（见质检记录 T6）
```

---

## 质检记录（写计划时查出来的**六处陷阱**，不是事后补的）

### T1 ★ `M33` / `M40` 的锚点会随"家族落地"漂移 —— **必须先整跑实测，再据实测处置**

`mutate-figure-style.py:964` 的 **`M33`** = "把点名绘图 skill 那行的〔拟建〕去掉 ⇒ `K6` 红"；
`mcm-plot-matlab` 一落地、`SKILL.md:67` 的〔拟建〕一摘，**`M33` 的锚点就不再命中 ⇒ `AssertionError` ⇒ 整轮 `MUT` 跑不完**。
`:1636` 的 **`M40`** = `K6` 的**反向臂**（标了〔拟建〕的 skill 真的存在时必须红）——它现在**借"真仓里 `mcm-plot-matlab` 尚不存在"**这一状态；
家族落地后**后置臂会转 `RED-BAD`**。
⚠️ **设计 §6 如实写了**：这一条是**侦察"只复刻了判据路径与断言表达式、未整跑"**的推断 ⇒
**落地时必须先整跑实测（不是假设），再据实测处置**；两条都要**换成语义锚**（别写死字面量），**不许直接删掉了事**。
> 先例：`mcm-plot-python` 落地时就踩过同型（`mutate-figure-style.py:1265` 借"目录反正不存在"当代理 ⇒ 恒假）。**归 Task 3。**

### T2 ★ `mcm-figure-choose/SKILL.md` 有**三处**要同步，`:71` 那句**同时点名两个 skill** —— **不许 naive 删**

`sed -n '67p;68p;71p' .claude/skills/mcm-figure-choose/SKILL.md`：
`:67` = `- \`mcm-plot-matlab\`（〔拟建〕）` · `:68` = `- \`mcm-plot-origin\`（〔拟建〕）` ·
`:71` = "`mcm-plot-matlab` 与 `mcm-plot-origin` **仍是〔拟建〕**（名字已登记、文件未建）"。
⇒ **`mcm-plot-matlab` 建出后：`:67` 摘标记、`:71` 必须拆句改写**（改成"matlab 已建、origin 仍是〔拟建〕"）。
**naive 地删整句会把 origin 带红**（`K6` 判双向）。**归 Task 3。**

### T3 ★ 摘〔拟建〕与建目录**必须在同一次变更里**（`K6` 无论先后都红）

`check-house-style.py` 的 `_k6` 判的是**目录存不存在**（`(SKILLS_ROOT / n).exists()`）。
⇒ 先摘标记后建目录 ⇒ "点名不存在的 skill"红；先建目录后摘标记 ⇒ "存在的 skill 仍标〔拟建〕"红。
**两条腿必须在同一个提交里落地。**

> ★ **订正（2026-10-01，写计划当晚自查）：这条归 `Task 1`，不是 `Task 3`** —— 我初稿把它排在 Task 3，**但 Task 1 就要建出
> `.claude/skills/mcm-plot-matlab/assets/mcmplot.m`**，目录一出现 `K6` 当场翻红 ⇒ **Task 1 的收工门（`check-house-style` PASS）就过不了**。
> **实测复核（写计划后当场跑）**：`_k6` 判的是 `SKILLS_ROOT / <名字>` **存不存在**；今天 `--only K6` = `PASS`，
> 其判词逐字为「`mcm-plot-matlab`（**不存在**·标了〔拟建〕）、`mcm-plot-origin`（不存在·标了〔拟建〕）、`mcm-plot-python`（存在·未标〔拟建〕）」。
> ⇒ **同型陷阱我已写进本计划的质检记录，却仍把归口写错了一次** —— 与 `mcm-plot-python` 计划当初"把 K6 排到 Task 4"是**同一个坑**。

### T4 ★ 普查字面量数的是 `SKILL.md` ⇒ 转录涟漪跟 **Task 3** 走

`check-spec-pointers.py` 的 `census()` = `sorted(root.glob("*/SKILL.md"))` ⇒
`SKILL.md` 一出现，`扫到 6 个 skill` → **`7 个`**、`绘图家族 1 个` → **`2 个`**，
`house-style-verify` 一族与 `check-spec-pointers.py` **docstring 里**的字面量随之过期。
⇒ **按本仓节奏**：先干净 → 再捕获 → 再提交 → 再跑一次**证不动点**。

> ★ **订正（2026-10-01，Task 1 落地后）：转录涟漪有两条，别混为一谈** ——
> - **`K6` 的判词行**（把三个绘图 skill 的"存在/未标〔拟建〕"逐格印出来）：随**〔拟建〕标记**变 ⇒ **Task 1 摘标记时就已刷过**
>   （实测落地于 `7cbde85`：`chart-types-verify` / `house-style-verify` / `skill-verify` / `plot-style-verify` 各若干行）。
> - **`census()` 的"扫到 N 个 skill / 绘图家族 M 个"**（数的是 `*/SKILL.md`）：仍**跟 Task 3**（`SKILL.md` 一出现才变）。
> ⇒ 我原稿把两条写成一条、且**都**排给 Task 3 —— **与 `M33`/`M40` 是同一处归口错**（见 T1 订正与 Task 1 硬要求 13）。
其中 `check-spec-pointers.py:42,51` 是**真·声明**（docstring 示例 + "真仓现状即此态"那句）⇒ **语义正确**地改写，**不是数字替换**；
其余是证据件的**转录** ⇒ 按各自的入库生成器重生成。

### T5 ★ `H10` 今天对 matlab 记的是 `not-landable` —— 本模块要把它**变成能验**

样式线 2026-10-01 把 `H10`（去上/右框线 · 刻度朝内 · 只留主刻度 · 轴标签带单位）补进了表，**正是为了让 matlab/origin 照表实现时拿得到它**。
而 `mcm-style.json` 的 `h10.axes_box.carriers.matlab.status` 今天是 **`not-landable`**，措辞是
"**能设、不能验**：侦察记录有对应 API（`box(ax,'off')` / `set(ax,'TickDir','in')`），但产物端零回读"。
⇒ **本模块要给出产物级回读**（python 侧的先例是 `probe-gap1-hanging-ticks.py` 量"带内墨迹"：落地态顶/右带 0、旧态对照 234/120）。
**两种结局都接受，只要求如实**：① 探针证明落地 ⇒ 把该格 `status` 改 `same-value` + 按实测改写 `how`（连带表新鲜度重生成）；
② 证明落不了地 ⇒ **保持 `not-landable`，但措辞升级为实测口径**（"实测过 X 命令，产物差分仍 0"）。
**不许**既不测也不改、留一句"能设不能验"当结论。**归 Task 1（落地）+ Task 2（回读与表同步）。**

### T6 两件 **m3-matlab 侦察证据已过期** ⇒ 本线**重捕获**，**不许手改**

`tests/m3-matlab-recon/out-checks-figure-style.txt`（重跑得 350/125，多行 `PASS→FAIL(F4)`）与
`out-mutate-today.txt` 是**家族落地前**的抓拍；`F4` 口径变更 + 变异总数变更 + 家族数变更都会让它们过期。
⇒ 由**各自的生成器**（`tests/m3-matlab-recon/gen-evidence.py` 等）**重捕获**，**一律不许手改**（先例：`figure-style-baseline.txt` 的教训）。
**归 Task 5。**

---

## Task 1：生成器 `gen-mcm-style-matlab.py` + 派生件 `mcmplot.m`

**产出**：`tests/skills/plot-matlab/gen-mcm-style-matlab.py`（入库、**重放式**）·
`.claude/skills/mcm-plot-matlab/assets/mcmplot.m`。

**为什么先做**：`mcmplot.m` 是**唯一**会被写手抄进脚本的东西 ⇒ 它一旦自带第二份样式，单源线就白做了。

**硬要求**：

1. **只读表、零规范字面量**（Global Constraint 3）：`mcmplot.m` 里的每个样式值都由生成器**从 `mcm-style.json` 取**，
   脚本里**不许出现**任何规范数值的字面（尤其 `H14` 的八个 hex、`0.80` 这类比例）。
2. **逐条锚定、fail-closed**：沿用 `gen-mcm-style.py` 的惯用法——锚点在源里**恰命中 1 处**，否则**非零退出**。
   **禁止全文档扫数**（朴素 `\d+\.\d+` 会把 `R2025b`、`§6.2`、`x2.show=0` 一类当数据抽走）。
3. **`not-landable` 与空值不许静默跳过**：生成器必须**把状态写进产物**（注释 + 一句"今天为何落不了地"），
   **"没抽到"必须与"表里写着没落地"区分开**。
4. **每张 figure 显式上浅色主题**（设计 §3.1）：产物里给出**可用的两种写法**（`figure(...,'Theme','light')` 与
   `theme(fig,'light')` 带句柄），**并注明 `theme('light')` 不带句柄 = 静默空操作（实测 `ok=1`、图仍深色 84.8%）**，
   **不许**给出那种写法。
5. **导出走 `print` 家族**（设计 §0.1）：`PaperUnits`/`PaperPositionMode`，**PNG 跟 `PaperPosition`、PDF 跟 `PaperSize` 两条口径分别设**；
   `exportgraphics` **只作"风险说明"**（宽 = 内容包围盒 ⇒ F1 0.861/0.865），不许当权威交付。
6. **字体点名 `Times New Roman`**（设计 §0.2 / §3.3）。
7. **`.m` 脚本用 `mfilename('fullpath')` 反推仓根**（设计 §2.6）。
8. **`H10`：先量后写**（见 T5，**不许先写再假装验过**）。表里 matlab 那一格今天写着 `not-landable`
   （"能设、不能验"）⇒ 本任务**先用 `box(ax,'off')` / `set(ax,'TickDir','in')` 做一次产物级实测**
   （顶/右带内墨迹，与 python 侧同型口径）：
   **能落地** ⇒ 才把这几行写进 `mcmplot.m` 的产物（值/形态**从表来**，不许手写字面）；
   **落不了地** ⇒ **不写进产物**，把实测过程与理由写成产物里的一段注释。
   **轴标签带单位**是调用方纪律 ⇒ 在 `workflow.md` 里交代（**载体侧无设置项**这句要写清）。
   ⚠️ **本任务只做"提前探明"**；把它做成**入库的探针 + 改表**归 Task 2（T5）。
9. **常量区带生成标记**（生成器只重写标记之间），其余散文**原样保留**。
10. **幂等**：生成器跑两遍，输出**逐字节相同**。
11. ★ **本任务一建目录，`K6` 就翻红 ⇒ 必须同批摘〔拟建〕**（见 T3 的订正）：改 `.claude/skills/mcm-figure-choose/SKILL.md`
    的 `:67`（摘掉 `mcm-plot-matlab` 的〔拟建〕）与 `:71`（**拆句改写**成"matlab 已建、`mcm-plot-origin` 仍是〔拟建〕"——**不许 naive 删整句**，那会把 origin 带红）。
    **验收**：`python tests/skills/figure-choose/check-house-style.py --only K6` **转绿**（其判词里 matlab 那格应变为"存在·未标〔拟建〕"）。
12. ★ **新写法规矩（本会话刚立的，对所有产物的散文/注释生效）**：凡出现**全称/强弱断言词**（`唯一` / `都` / `全部` / `任何` / `只能` / `必然` / `一定` / `绝不`…），
    **要么当场给实测背书，要么加限定**；凡列"已知清单"，**必须写明"不声称穷尽"**（除非能证明穷尽）。
13. ★ **`M33`/`M40` 必须在本任务内 retarget 回绿**（**归口订正**：见 T1；原计划把它们排在 Task 3 是错的 —— **是 Task 1 的 K6 编辑把这两个变异弄红的**）。
    实测：`M33` 的锚点字面 `"  - \`mcm-plot-matlab\`（〔拟建〕）"` 被本任务删掉 ⇒ `sub_once` 抛错；`M40` 的反向臂从**已无〔拟建〕**的 `SKILL.md` 复制 ⇒ 收不到 FAIL。
    **目标换成当前仍〔拟建〕的 `mcm-plot-origin`**（`M33`：摘它的〔拟建〕⇒ `K6` 红；`M40`：临时根里让 `mcm-plot-origin` **标着〔拟建〕却存在** ⇒ 红），**注释一并改写**（现在注释里写的还是 matlab 目标）。
    **不许减覆盖**（两条都要**真的红**）· **不许删掉** · 总数要回到 `docs/mcm-suite-todo.md` §H.5.3 记载的现取值。
    **连带**：捕获件里印了 `M33`/`M40` 的正文（实测 4 件各 3 处）⇒ 按各自的生成器重生成，并**逐行分类差异**（只许元数据行 + 这两条的合法读数变）。

**验收**：跑两遍逐字节相同；改 `mcm-style.json` 的一个值（**当场演示后还原**，两次输出都贴）⇒ 产物随之变；
`mcmplot.m` 里 `git grep -nE "#[0-9A-Fa-f]{6}|0\.[0-9]{2}"` 的命中**全是生成标记/注释引用**，逐条解释；
`check-house-style.py --only K6` **绿**（第 11 条）。

---

### Task 2：新鲜度守卫（两臂）+ 变异 + `H10` 回读 + 表同步

**产出**：`tests/skills/plot-matlab/check-style-freshness.py` · `mutate-plot-style.py` · `probe-h10-band-ink.py` · 证据入库。

**硬要求**：

1. 守卫 = **重跑生成器 → 与入库件逐字节相等**；不等即 FAIL 并**打印差异处上下文**。
   ⚠️ **照字面实现恒真**（生成器原地写 ⇒ 过期件被原地重跑就被改对）⇒ **必须做成两臂**：
   **A1 = `git show HEAD:<path>` 快照 vs 重放** · **A2 = 重放前的工作树字节**（python 侧先例已实测"两臂互补各有专属真红"）。
2. **fail-closed**：锚点不命中 / 命中 >1 / 生成器跑不动 ⇒ 记红并**非零退出**；**末行恒为 `RESULT:`**、每条判词一行、退出码 0/1、`--only` 可选。
3. **每类变异都必须真的红**并贴输出，至少覆盖：
   ① 改 `mcm-style.json` 的一个值 ⇒ 派生件落后 ⇒ 红；② 改 `mcmplot.m` 的一个常量 ⇒ 红；③ 删掉一条锚点的目标行 ⇒ fail-closed 红；
   ④ **摘掉浅色主题** ⇒ 渲染**照常成功**但产物是深色 ⇒ **`F4` 真红**（本支是 `F4` 的 motivating case）。
   ★ **订正（2026-10-01，Task 2 实测 + 独立复核双方复现）**：本条原写字面"摘掉浅色主题**那一行**"—— **为假**。
   `mcmplot.m` 的**白是过定的**（`'Color', S.bg` 出现在**三处**：`new_figure` 建图、`set(fig,'Color',…)`、`apply_style` 里的 `set(ax,'Color',…)`）
   ⇒ **只去 `'Theme','light'` 一个 token，产物仍白、`F4` 仍 PASS**。变异必须摘掉**浅色主题机制**（三处白一并去掉）才真红。
   ⇒ **由此得到的判据口径**：`F4` 接住的是"**产物是深色**"，**不是**"忘了写 `Theme`"——这两件事在**本模块**里不等价（白过定）。
   ⚠️ **教训**：这是控制者第二次把"没实测过的行为口径"写进计划（先例：`_k6` 判目录存在那条归口）。**凡写死"某操作会怎样"，落地前必须实测复算。**
   ⑤ **字体点名一个不存在的族** ⇒ **静默回退** ⇒ **`F6` 真红**（"点名不存在的字体会静默回退"是设计 §5 的核心断言，**必须有真红**）。
4. **`H10` 产物级回读**（T5）：`probe-h10-band-ink.py` 量**顶/右带内墨迹**（与 python 侧同型口径）；
   给出**落地态 vs 对照态**两个读数。测得出 ⇒ 把 `mcm-style.json` 的 `h10.axes_box.carriers.matlab`
   **`status` 改 `same-value` + `how` 改写为实测口径 + 表新鲜度重生成**；测不出 ⇒ 保持 `not-landable` 但**措辞升级为实测口径**。
   ⚠️ **改表要走生成器**（`house-style.md` → `gen-style-table.py` → `mcm-style.json`），**不许手改派生件**。
5. **驱动器收工自证**要**真测"没碰真根"**（先例：拿"目录反正不存在"当代理会恒假 —— 见 T1）。
6. ★ **`same-value` 的口径空缺**（**Task 1 执行者查出来的**，与样式线 `H10` 那条 Important-5 同型）：`gen-style-table.py` 对 `same-value`
   **没有正面定义** ⇒ 它接不住"载体有能力设、但产物里不落活常量"这一类。实况：
   - **matlab 格** `h1.width_ratio.default_lo` 写 `same-value`，而产物**只把它落成注释**（"本模块不落活常量"）；
   - **对照 python 格**：python **落了活常量**（但 `figsize_for()` 只取 `default_hi`、**无人消费**）；
   - ⚠️ **python 那格的 `how` 还写「令宽 = 栏宽 × 0.95 ⇒ F1 = 0.95」，而代码里不发生**（取的是 `default_hi`）—— **既有问题**，本任务登记并按实测订正。
   - ★ **范围订正（2026-10-01，Task 1 独立复核 Findings-M4 撑开）**：**同型误述不止 `default_lo` 一格，而是三格** ——
     `h1.width_ratio.{min,max,default_lo}` 的 python `how` **都**写着"令宽 = 栏宽 × 表内 `<该键>`（0.80 / 1.20 / 0.95）⇒ F1 = 0.80 / 1.20 / 0.95"，
     而 `figsize_for()` **只**乘 `default_hi` ⇒ **三句话描述的动作都不发生**（**只有 `default_hi` 那格与代码一致**）。
     **复现**：`grep -n "def figsize_for" -A9 .claude/skills/mcm-plot-python/assets/mcmplot.py`（取 `default_hi`）；对照表里四格 `how`。
     ⇒ **(c) 必须一并订正三格**，不许"改了一格、另两格继续假"（**先例：治理一句假话必须全文件搜同型**，本会话已犯三次）。
   **要做的**：(a) **给 `same-value` 一个正面定义**（写进生成器与表头）；(b) 按该定义处置 `default_lo` 那一格（三选一：落活常量 / 改该格 `status` / 改口径）；
   ⚠️ **(b) 若选"落活常量"会多一条 `0.xx` 的 tripwire 命中**（`0.95` 是表里唯一形如 `0.xx` 的规范值），与 Task 1 验收第 3 条冲突 ⇒ **要显式裁决该怎么判**，**不许偷偷放宽**；
   ★ **控制者已预先裁定这条口径（2026-10-01，Task 2 落地后；Task 2 实测选了"改口径"、故该情形今天不发生，此处是为将来定死判法）**：
   Task 1 验收第 3 条的原意是抓**手写的规范字面**。判定规则 = **命中行同时满足下列两条才算合规**：
   ① 该行**位于生成标记之间**（`>>> BEGIN GENERATED …` / `<<< END GENERATED …`）；② 该行的值**可追到表**（同一行的 `% <id>` 标注能对上 `mcm-style.json`）。
   **只有①不满足**（手写）**或只有②不满足**（表里没有这个数）⇒ **仍判红**。⇒ **这是"按机制判"、不是"按形判"，不构成放宽**；执行者若将来落活常量，**按此判并在证据里写明哪条命中靠①②过关**。
   (c) 走生成器改表 + 重生成表新鲜度，**不许手改派生件**。

7. ★ **`mcmplot.m` STYLE 区头那句「唯一样式来源」要不要加限定**（2026-10-01，**控制者据 Task 1 独立复核残余 R1 上调** ——
   复核者列为"观察、不报缺陷"，理由是紧邻的 `:51`（"下列 id **不声称穷尽**…"）已自限；**控制者裁定这个理由不成立**：
   `:51` 限定的是**清单**（"下列 id 不穷尽"），不是**来源的唯一性**，**两码事**）。
   **一秒可证伪的反例**：`grep -n "XColor" .claude/skills/mcm-plot-matlab/assets/mcmplot.m` ⇒ `apply_style` 里
   `set(ax,'XColor','k','YColor','k')` 是**写死的外观字面**，而 `mcm-style.json` 的 15 条里**没有轴色行**、`house-style.md` 也**不规定轴色**。
   ⇒ 按本会话的硬规矩（**全称/强弱断言词要么给实测背书、要么加限定**；**判据必须能被一条命令一秒推翻**），**"唯一"必须处置**。
   **二选一，二选一即可，但必须显式选并留证（不许默认放过）**：
   (a) 改**生成器**里那句字面（`gen-mcm-style-matlab.py` 的 STYLE 区头字面）⇒ 加限定（例如"**本模块所消费的那些样式值**的唯一来源"），**重放产物**；
   (b) 若判 `'k'` 不构成"样式字面"（例如证明它只是显式重申 MATLAB 默认轴色、与规范无涉）⇒ **当场给出取证**（它凭什么是默认值、规范为何不涉）并**把结论写进产物注释**。
   ⚠️ **产物是派生件 ⇒ 一律走生成器改、重放产出**（GC7），**不许手改 `mcmplot.m`**。
   ⚠️ **改这句要连着复核 Task 1 的验收第 3 条**（`git grep -nE "#[0-9A-Fa-f]{6}|0\.[0-9]{2}"` 命中仍应全是生成标记/注释引用）。

**验收**：守卫两臂各有一条**专属真红**；变异合计行全红；收工时 `git status --short` 空。

---

### Task 3：`SKILL.md` + `references/workflow.md` + **家族落地的最小同步**

**产出**：`.claude/skills/mcm-plot-matlab/SKILL.md` · `.../references/workflow.md` · `mcm-figure-choose/SKILL.md` 的两处订正。

**硬要求**：

1. `SKILL.md`：**零数字字面量** · **必须**含 `references/house-style.md` · 五段式（什么时候用 / 怎么用 / 输出契约 / 边界 / 指针）·
   写明前置条件（**需本机装 MATLAB**；**跨版本未验**如实写，**不许写"自动安装"**）。
2. **`mcm-figure-choose/SKILL.md` 的三处同步**（T2）：**`:67` 摘〔拟建〕 与 `:71` 拆句改写已在 Task 1 办掉**（因为 Task 1 就建目录，见 T3 订正）
   ⇒ **本任务只需复核它没被改坏**（`--only K6` 仍应绿、`:71` 仍点名 origin 是〔拟建〕），**不要重复改**。
   ★ **但有一条必须当场复核（2026-10-01，Task 1 独立复核 Findings-M2）**：Task 1 把 `:71` 改成了
   「`mcm-plot-python` 与 `mcm-plot-matlab` **已建**（"产代码"这一段可以直接交给它们）」——
   **该句今天对 `mcm-plot-matlab` 只按 `K6` 的口径（目录存在）成立**（该目录此刻只有 `assets/mcmplot.m`，无 `SKILL.md`），
   按"skill **可被调用**"读则为**过度声明**（窗口 = Task 1 → 本任务）。
   **本任务收工时**：`find .claude/skills/mcm-plot-matlab -type f` **必须已有 `SKILL.md`** ⇒ 该句**自然转真、不需改词**；
   **若本任务未建出 `SKILL.md`**（被拆分/延后）⇒ **必须同批给该句加限定**（例如"目录已建、代码资产 `mcmplot.m` 可用；`SKILL.md` 待建"），
   **不许把一个按"可调用"读为假的句子留在入口文档里**。**复核命令**：`find .claude/skills/mcm-plot-matlab -type f`。
3. **`check-house-style.py --only K6` 应已由 Task 1 转绿**（若此刻红了 ⇒ 说明 Task 1 漏了摘标记，**停下来报 BLOCKED**，别在这里补）。
4. **`M33`/`M40` 已由 Task 1 处置**（★ **归口订正：原写在 Task 3，是错的** —— 这两条是**被 Task 1 的 K6 编辑弄红的**，只要 Task 1 落地就得同批 retarget，
   否则从 Task 1 到 Task 3 之间**每个中间态都过不了自己的收工门**）。本任务**只需复跑复核**：它们在**家族已存在（`mcm-plot-matlab` 有 `SKILL.md`）**时**仍然红**。
   一并实测 `M43`–`M46` 与 `census` 的家族数（设计 §6 说它们不受影响，**但那是推断，跑出来的才算**）。
5. `workflow.md`：场景 → 脚本 → 产物 → **★看图**（**固定一节**，Global Constraint 11 的直接兑现）；
   写清与判据的契约（调用 `check-figure-style.py`，`--textwidth-in` 与脚本侧同名同义，`--dpi` 必须与实际导出 dpi 一致）。
6. **转录涟漪**（T4）：`扫到 6 个 skill` → `7 个`、`绘图家族 1 个` → `2 个`；
   `check-spec-pointers.py` 的 docstring **语义改写**，其余按各自生成器重生成；**先干净 → 再捕获 → 再提交 → 再证不动点**。

**验收**：`check-spec-pointers.py` 真仓 ⇒ `RESULT: PASS (绘图家族 2 个，K2/K3 全绿)`；
`SKILL.md` 行数 < 150；`mutate-figure-style.py` **整跑全红**（合计行现取值）且 `exit 0`。

---

### Task 4：RED / GREEN 对照与证据（含**看图层**）

**产出**：`tests/skills/plot-matlab/red/**` · `green/**` · 对照表 · 生成器入库。

**硬要求**：

1. **★ RED 必须由"没看过规范"的写手产出**（先例纪律：只给**场景 brief 路径 + 输出目录**，不给规范、不给判据）。
   场景 ≥3 个，**同场景、同数据、同分母、同一把尺**（`check-figure-style.py` 一字不改）。
2. **RED 至少 3 条红且逐条点名**（哪条判据、什么读数、为什么）。若某条被不同原因判红，**如实写是哪条、为什么**。
   ⚠️ **诚实披露**：先例里写手仍可能看到"skill 列表那行描述"与记忆文件 ⇒ **"知道类别"照样全红不推翻 RED，但披露必须写全**。
3. **两个载体都出**（PNG 与 PDF），因为 `F2` **随载体变**、`F1` 的**两条口径不同源**（PNG 跟 `PaperPosition`、PDF 跟 `PaperSize`）——
   **不许跨载体比 `F2`**，并在证据里写明。
4. **判断层**：出图后**亲眼看图**并写下"从这张图读到了什么"（Global Constraint 11）。**不许省。**
   本支**必须**看的两点：**底色是不是浅色**（默认深色是 motivating case）· **框线/刻度**（`H10`）。
   > ★ **限定（2026-10-02 加，Task 4 实测 + 独立复核）**：上面那个 motivating case 说的是**工具链默认是深色**，
   > **不是**"干净写手会交出深色图"。Task 4 实测恰好相反：**三个未见规范的写手各自都自己**发现了深色并修掉
   > ⇒ RED 三张**全是浅色**、`F4` 在 RED 集里**一条红都没有**。想看本支 `F4` 的真红，去 **Task 2 的变异件**
   > （`mutate-plot-style.py` 的 F4 臂），**别在本任务的 RED 集里找**。措辞同设计 §2 的限定。
5. 对照表要**机器抽取**（别手抄判词），写清两侧**同源同数**。

---

### Task 5：全库收口

**产出**：**m3-matlab 侦察证据重捕获**（T6） · `docs/` 过期散文订正 · 残留逐件分类入库 · 台账与记忆回写。

**硬要求**：

1. **重捕获** `tests/m3-matlab-recon/out-checks-figure-style.txt` 与 `out-mutate-today.txt`（**由各自生成器**，**不许手改**），
   并把重捕获**前后**的读数差**逐项解释**（`F4` 口径变更 / 变异总数变更 / 家族数变更各占哪些行）。
2. `docs/` 里凡写死"变异总数""家族数""`扫到 N 个 skill`"的散文 ⇒ 改成**现取值**；**自带复核命令的声明必须复跑那条命令**。
3. **残留分类收口**（**不许写成"全库残留 = 0"**——那条恒不可达）：分**机械层**（去重并集 == 表行数，一条命令可推翻）
   与**判断层**（每行的类别与理由须人读）**两层**，逐件给复核命令。**这不是把验收改软，是不许把判断层说成机械层。**
4. 台账 `.superpowers/sdd/progress.md`（gitignored，**但必须回写**）· `docs/mcm-suite-todo.md` §H · 记忆文件回写。

---

## 结束条件

五个任务全绿后，派**最终全分支复审**（范围 = 本模块基线到 `HEAD` 的全部提交），
按结果修复或收口 ⇒ 台账 + `docs/mcm-suite-todo.md` §H + 记忆 + **推送**（仓外 worktree 配方，只推 `docs tests .claude tools`；
**推送是对外不可逆动作 ⇒ 按 [[public-remote-push-guardrails]] 先比 blob sha 与快进性，并在推送前向用户交底**）。
推完按用户 2026-10-01 的路线**直接进 `mcm-plot-origin`**（设计 `e4c6c14` 已就绪 ⇒ 计划 → Task 1..N，同样走满四级）。
