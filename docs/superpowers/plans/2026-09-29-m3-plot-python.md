# M3 `mcm-plot-python` 实施计划（2026-09-29）

设计：`docs/superpowers/specs/2026-09-29-m3-plot-python-design.md`（本计划的每个"为什么"都在那里）。
侦察：`tests/m3-plot-recon/`（入库）· `.superpowers/sdd/task-m3-plot-recon-report.md`（过程件）。
用户已裁的四条：底座 `science`+`no-latex` 并自管 bbox · 样式数值走**派生件 + 新鲜度守卫** ·
`K3` 标记集**现在修且与家族落地同一次重生成** · `house-metrics` 的 `95→129` 订正（**已落地**）。

---

## Global Constraints（**每个任务的复审都要拿到这一份**）

1. **唯一权威**：规范正文只在 `.claude/skills/mcm-figure-choose/references/house-style.md`。
   本模块**只给指针、不重述**。`mcm-plot-python/SKILL.md` **必须**含字面量 `references/house-style.md`（`K2`）。
2. **`SKILL.md` 与 `references/**` 零数字字面量**（`K3` 是**子串**判据，实测会让 `figsize=(6.3, 2.6)` 这类普通写法
   意外触发；中文侧 `四川`/`第四版` 也会误红）。**要说的数一律回规范去说。**
3. **写入一律 `write_bytes`**（`write_text` 在 Windows 会写 CRLF——本仓栽过），**文档与源码全 LF（CRLF=0）**。
4. **凡数字必来自当场跑过的命令**，命令与原始输出贴进证据；**"我没找到" ≠ "它不存在"**（通则 4.5）。
5. **判据脚本 `check-figure-style.py` 一字不改**——RED 与 GREEN 共用同一把尺，这才叫对照。
6. **派生件不许手改**：只许由入库的生成器重放产出（`mcm.mplstyle`、`mcmplot.py` 的常量区）。
7. **声明了覆盖就必须有一次真的红**（本仓纪律）。凡"这条判据会拦住 X"，必须有一条**真红**的变异作证。
8. **收工三件套**（每个任务都要跑并贴输出）：`check-house-style.py` → `RESULT: PASS` ·
   `mutate-figure-style.py` → 全红（`RED-BAD 0`）· `run-expected.py` → `MISMATCH 0/21`（**订正 2026-10-01**：`expected.tsv` 已由 21 条增到 **23 条**〔M3-style Task 3 加的 `F4`/`F5` 两条 fixture〕⇒ **今天应为 `MISMATCH 0 / 23`**，见 `docs/mcm-suite-todo.md` §H.5.6）。
   > **⚠️ 订正（2026-09-30 终审修复轮）**：这个 `RED-BAD 0` 是**把提示语当读数列** —— `RED-BAD` **只在失败时逐条打印**，干净跑里一条都没有。**实为**合计行 `MUT: 53/53 达预期（合计）`（**该轮当时的合计**；一条命令可核：`python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"` —— **合计行不是末行**，`tail -1` 取不到它；**今天同命令取到的合计 = 64**，见 `docs/mcm-suite-todo.md` §H.5）。
9. **不许提交脏树**；每个任务收工 `git status --short` 为空。任务之间**另起提交**，**不许 `--amend`**。
10. **第三方二进制入库的规矩（本模块首次用到）**：随 skill 入库的字体必须
    ① **逐件 `git hash-object` 记录并写进 PROVENANCE**；② 记**来源绝对路径 + 上游包与版本 + 许可标识 + 取件日期**；
    ③ **许可原文一同入库**（GFL 明确要求随字体分发）；④ 这些文件**只许字节级复制、不许手改**（改了哈希就变，
    判据会红——那正是要的）。

## 派发指令必带（每次派 subagent 都要附）

- 任务书路径（本文件的那一节 + 该任务的 brief 文件）· 报告落点 `.superpowers/sdd/task-m3-t<N>-report.md`（**必须真的落盘**）。
- Global Constraints 全文（上面那一节）。
- 明确：**只回报**状态 + 提交 + 一句话测试结论 + 顾虑；**不要把报告内容复制进回复**。
- 基线 commit（派发前的 `HEAD`）——复审的 diff 范围就用它，**不许用 `HEAD~1`**。

---

## 文件结构（终态）

```
.claude/skills/mcm-plot-python/
├─ SKILL.md                     # 短契约（零数字字面量）
├─ references/workflow.md       # 出图流程（零规范数值）
└─ assets/
    ├─ mcm.mplstyle             # ★ 派生
    ├─ mcmplot.py               # ★ 常量区派生；apply_style() / figsize_for(textwidth_in) / save()
    └─ fonts/                   # ★ 第三方二进制（随 skill 入库，见设计 §11.2）
        ├─ PROVENANCE.md        #   来源·版本·许可·取件日期·逐件哈希
        ├─ GFL.txt              #   许可原文（GFL 要求随字体分发）
        ├─ LPPL.txt             #   （若所取文件属 LPPL 1.3）
        └─ TeXGyreTermesX-*.otf #   只许字节级复制，不许手改

tests/skills/plot-python/
├─ gen-mcm-style.py             # 生成器（重放式，入库）
├─ check-style-freshness.py     # 新鲜度守卫（重跑生成器 → 逐字节相等）
├─ mutate-plot-style.py         # 变异（必须真的红）
├─ red/…                        # 朴素脚本 + 产物 + 判词
├─ green/…                      # 走模块的脚本 + 产物 + 判词
└─ plot-style-verify.txt        # 对照与全量读数（生成器产出）
```

---

## 质检记录（写计划时查出来的两处**顺序陷阱**，不是事后补的）

这两条方向相反，写任务书时**极易弄反**（通则 11 的形态：新裁的东西让早先抄来的安排静默失效）：

- **`K6` 判的是目录**：`check-house-style.py` 的 `_k6` 用 `(SKILLS_ROOT / n).exists()`，即
  **`.claude/skills/mcm-plot-python` 这个目录存不存在**，**不是**判它有没有 `SKILL.md`
  ⇒ **Task 2 一建目录，`K6` 立刻变红**，〔拟建〕必须在 **Task 2** 摘，**不能等 Task 4**。
  （Task 2 的验收因此包含 `check-house-style.py --only K6` 转绿。）
- **普查字面量数的是 `SKILL.md`**：`check-spec-pointers.py` 的 `census()` 是 `sorted(root.glob("*/SKILL.md"))`
  ⇒ `扫到 5 个 skill` / `绘图家族 0 个` **只有 Task 4（建出 `SKILL.md`）才让它过期**，
  故那 8 份入库件的重生成跟 **Task 4** 走，**不跟 Task 2**。
- **★ 驱动器里有一行硬断言也判"目录在不在"**（本计划查出来的**阻断项**）：
  `mutate-figure-style.py:1265` 的收尾自证里写着
  `and not (HOUSE_SKILLS / "mcm-plot-python").exists()`——它本意是**证 `M40` 换 `--skills-root` 没碰真根**
  （当时的写法借了"这个 skill 反正不存在"当廉价代理）。**目录一落地，这一项恒假 ⇒ 驱动器 `exit 1`
  ⇒ Global Constraint 8 从 Task 2 起就再也满足不了。** 修法：把这条代理换成**真正测 `M40` 非侵入**的断言
  （例如比对真 skills 根的路径集合 / 用 `M40` 自己那个临时根去断言），**不许**直接删掉了事。
  ⇒ 归 **Task 2**（与摘〔拟建〕同批）。侦察**没查到这一处**（它只复刻了 `M43` 的 `pre_ok`，
  并如实写明"驱动器没在真仓增家族的情况下跑过"）——**这正是"未验证"清单该被读的地方**。

---

### Task 1：`K3` 的 ASCII 标记集对齐 + 变异证明

**为什么先做**：`K3` 是**家族级**判据（`check-spec-pointers.py` 复用），而"样式数值不许复述"正是本模块的核心纪律。
实测缺口：`≥7 pt` / `上限 4` / `不超过 12 词` / `主色 4 个` **全判 PASS**（`≤4` 判得到），
而 `H12` 的规范值恰恰写的就是 `≥7 pt`。

**改哪**：`tests/skills/figure-choose/check-house-style.py` 的 `_k3` **主臂**——banned 集目前只有
`\d+\.\d+` + `≤\s*\d+|< \s*\d+\s*词`。要**与中文臂的标记表 `SK_CN_TIER_RES` 逐条对齐**（不许凭印象加）。

**硬要求**：

1. **先跑误伤回归**：新的 banned 集对现有 **5 份** `.claude/skills/*/SKILL.md` 必须**零命中**（今天已有 4 份被
   小数串假红，那是**射程收窄**的理由，不是本任务的）。命令与逐份读数贴进证据。
   **若有任一份命中了新标记 ⇒ 停下来报 BLOCKED**，不许为了过而删标记或改口径。
2. **新变异至少 4 条**（`M47` 起）：`≥7 pt` / `上限 4` / `不超过 12 词` / `主色 4 个`，**每条都要真的红**并贴输出。
   编号顺延原因写在驱动器里 —— 先例在 `mutate-figure-style.py:145-146`（`M43` 顺延）、
   `:172-173`（`M47` 顺延）、`:1134-1135`（`M53` 顺延）；更早同型见 `:95`、`:441-443`、`:634`。
3. **总数现算**，不许手抄（沿用 Task 7 的做法）。
4. `_k3` / `_cn_arm` 的 docstring 要按**改后**的射程改写，**不许留下比事实大的措辞**。
5. 受影响的入库证据件**同批重生成**（别留过期声明）。

**验收**：三件套全绿（Global Constraints 8）+ 上面第 1、2 条的原始输出入库。

---

### Task 2：生成器与派生件

**产出**：`tests/skills/plot-python/gen-mcm-style.py`（入库、**重放式**）·
`.claude/skills/mcm-plot-python/assets/mcm.mplstyle` · `.../assets/mcmplot.py`。

**硬要求**：

1. **只抽 H1 / H3 / H4 / H12**，**逐条锚定正则**，每条必须**恰命中 1 处**（沿用 `GUARDS` 的 fail-closed 惯用法）。
   **禁止全文档扫数**——实测朴素 `\d+\.\d+` 会误抽 `tab10`→`10`、`3D`→`3`、`p90`→`90`、`§7.2`→`7.2`。
2. 生成器头部**照实写出可抽性边界**：H2/H6/H8/H10/H11/H13 **无数可抽**；H9 的可操作数在**依据**段、与 43 个分布读数**同形**。
   **抽不到的绝不硬凑。**
3. **`mcm.mplstyle` 必须覆盖 `savefig.bbox`**（底座 `science` 自带 `'tight'`，会把输出宽裁掉、毁掉 `figsize`↔F1 的干净映射）。
4. 底座 = `science` + `no-latex` **两个 style 叠加**；`mcmplot.py` 暴露
   `apply_style()` · `figsize_for(textwidth_in)` · `save(fig, path, dpi)`，其中 `save()` **强制默认 `bbox_inches`**。
   **★ `import scienceplots` 是必需的**——它靠 **import 的副作用**注册 style；只 `import matplotlib.style`
   再 `plt.style.use(["science", …])` 会 `OSError: 'science' is not a valid …`（**实测**）。
   **★ 设计 §9 的机制已在系统 matplotlib 3.10.7 上验过**（`figsize=(6.31,2.6)` / 分母 6.31）：
   原样 `science+no-latex` ⇒ F1 **0.870(PNG)/0.871(PDF)**；把 `savefig.bbox` 覆盖回 `standard` ⇒ **1.000/1.000 逐位一致**。
   **★ 图内元素溢出时用 `layout='constrained'`（或 `fig.tight_layout()`）**——实测两者都**不动 F1**；
   **`bbox_inches='tight'` 才是那个会改输出宽的键**，不许用它当补救。
5. **分母与判据同名同义**：参数名一律 `textwidth_in` / `--textwidth-in`，且**不预设默认值**。
6. `mcmplot.py` 的常量区要带**生成标记**（生成器只重写标记之间），其余散文**原样保留**。
7. 不得在 `SKILL.md` 之外的载体里**手写**任何规范数值——本次**一个都不许手写**。
8. **入库字体（用户 2026-09-29 裁，见设计 §11.2）**：把 TeX Live 的
   `fonts/opentype/public/newtx/TeXGyreTermesX-{Regular,Italic,Bold,BoldItalic}.otf` **字节级复制**进
   `assets/fonts/`（论文嵌的就是这一族——实测嵌的是 `TeXGyreTermesX-Regular`）。配 `PROVENANCE.md`
   （来源路径 · 上游包与版本 · 许可标识 · 取件日期 · **逐件 `git hash-object`**）+ **许可原文入库**：
   实测 `tlpkg/tlpobj/*.tlpobj` 的 `catalogue-license` 为 **`newtx` = LPPL 1.3** · `tex-gyre`/`tex-gyre-math` = GFL；
   **本机 TeX Live 的 `doc/` 树是精简的、没有许可文件** ⇒ 许可全文需**另处取回**（取回途径与日期写进 PROVENANCE），
   **GFL 明确要求许可随字体分发**。`mcmplot.py` 的 `apply_style()` 负责把它们 `fontManager.addfont()` 注册进来。
   ⚠️ **不许依赖 TeX Live 路径**（那正是用户选"入库"要换掉的环境耦合）。
9. **数学**：`mathtext.fontset` 默认取 `stix`（与 Times 相容）。**可选**：试一次
   `mathtext.fontset='custom'` + 入库的 TeX Gyre Termes Math，**若能更近就采用、不能就保持 `stix`**，
   并把实测差异如实写进已知缺口（设计 §7.1 已写明"数学逐字形同一做不到"）。

**验收**：生成器跑两遍输出**逐字节相同**（幂等）；改 `house-style.md` 的一个锚点值 ⇒ 输出随之变
（**当场演示后还原**，两次输出都贴）；**并**摘掉 `mcm-figure-choose/SKILL.md:66` 里 `mcm-plot-python` 的〔拟建〕
（本任务一建目录 `K6` 就红 —— 见「质检记录」），`check-house-style.py --only K6` 转绿；
**并**修掉 `mutate-figure-style.py:1265` 那条会恒假的断言（见「质检记录」第三条），
令驱动器在**目录已存在**时仍 `exit 0`、合计行仍全红 —— **两条修法都要在本任务内实测**。

---

### Task 3：判据 —— 新鲜度守卫 + **字体守卫** + 变异

**产出**：`tests/skills/plot-python/check-style-freshness.py` · `mutate-plot-style.py` · 证据入库。

**硬要求**：

1. 守卫 = **重跑生成器 → 与入库件逐字节相等**；不等即 FAIL，并**打印差异处上下文**。
   > **⚠️ 订正（2026-09-30 终审修复轮）**：本条**照字面实现是恒真的** —— 生成器**原地写**派生件，一份过期件被原地重跑就被改对、再比必然相等。落地时改成"**两份参考都取在重跑之前**"（`git show HEAD:<path>` 快照 + 检查前的工作树字节；即 `tests/skills/plot-python/check-style-freshness.py` 的 A1/A2 两臂）。见 `docs/mcm-suite-todo.md` §H.1。
2. **fail-closed**：锚点不命中 / 命中 >1 / 生成器跑不动 ⇒ 一律记红并**非零退出**（别让异常裸漏出去）。
3. **三类变异各自必须真的红**并贴输出：① 改 `house-style.md` 的锚点值 ⇒ 派生件落后 ⇒ 红；
   ② 改派生件的一个常量 ⇒ 红；③ 删掉一条锚点的目标行 ⇒ fail-closed 红。
4. 走 `check-spec-pointers.py` 的同一条纪律：**末行恒为 `RESULT:`**、每条判词一行、退出码 0/1。
5. **字体守卫（用户 2026-09-29 裁"加"，见设计 §11.3）**：今天 `F1`/`F2`/`F3` **一个字都不判字体** ⇒
   字体没找到就**静默回退成 DejaVu**、没有任何判据会红。本任务要补上这条：
   **渲染后核"实际用的是不是入库那一份"**。两条途径择一并写明理由：① 产出 PDF 的
   `fitz` `get_fonts()` 所报 basefont 集合 ⊆ 预期集合（验产物本身，强）；② 对每个用到的族跑
   `font_manager.findfont(...)` 与预期文件路径比对。**必须有一条真红**：把入库字体**改名或移走** ⇒
   **判据红**（**不是**静默回退还绿）。射程如实写：它证明"用的是这份文件"，**不证明**"与论文观感一致"。

---

### Task 4：`SKILL.md` + `references/workflow.md` + 家族落地的最小同步

**产出**：`.claude/skills/mcm-plot-python/SKILL.md` · `.../references/workflow.md` ·
`mcm-figure-choose/SKILL.md` 的两处订正。

**硬要求**：

1. `SKILL.md`：**零数字字面量**（Global Constraints 2）· **必须**含 `references/house-style.md` ·
   五段式（什么时候用 / 怎么用 / 输出契约 / 边界 / 指针）· 写明前置条件（依赖 SciencePlots，**不写"自动安装"**）。
2. `mcm-figure-choose/SKILL.md:66` **摘掉 `mcm-plot-python` 的〔拟建〕**（`K6` 判双向，家族一落地就必须摘）。
3. `mcm-figure-choose/SKILL.md:70` 那句"**这三个 skill 现在还不存在**"是**过期散文**且 `K6` **抓不到**
   （该行不含 `mcm-plot-` 前缀）⇒ **手改**，并如实改成"`mcm-plot-python` 已建、另两个仍是〔拟建〕"。
4. `workflow.md` 要写清与判据的**契约**：调用 `check-figure-style.py`，`--textwidth-in` 与脚本侧同名同义，
   `--dpi` 必须与 `savefig(dpi=)` 一致（Task 6 N-4 的教训）。
5. **出图后 agent 亲眼看图**这一步要写成流程的**固定一节**（M3"载体选择以 agent 能否看见产物为准"的直接兑现）。

**验收**：`check-spec-pointers.py` 真仓 ⇒ `RESULT: PASS (绘图家族 1 个，K2/K3 全绿)`；
`SKILL.md` 行数 < 150；`check-house-style.py --only K6` **本任务前应已由 Task 2 转绿**（若它此刻是红的 ⇒ 说明 Task 2 漏了摘标记）。

**本任务同时要做的涟漪**（`SKILL.md` 一出现就让它们过期，见「质检记录」）：
`git grep -l "扫到 5 个 skill"` 逐件列出 —— `扫到 5 个 skill` → `6 个`、`绘图家族 0 个` → `1 个`。
其中 `check-spec-pointers.py:42,51` 是**真·声明**（docstring 里的示例与"真仓现状即此态"那句），
必须**语义正确**地改写，**不是数字替换**；其余是 verify/fixture 证据件的**转录**，按各自的入库生成器重生成。

---

### Task 5：RED / GREEN 对照与证据

**产出**：`tests/skills/plot-python/red/**`（朴素脚本 + 产物 + 判词）· `green/**` · 对照表 · 生成器入库。

**硬要求**：

1. **同场景、同数据、同分母、同一把尺**（`check-figure-style.py` 一字不改）。场景用
   `red/brief-R1..R3.md` 的那三个（数据逐字取自它们；侦察已实测三个都能出图并过判据）。
2. **RED 至少 3 条红且逐条点名**（侦察实测的朴素脚本判红 4 条：F1 1.426 / F3a / F3b 21 词 / F3c；
   若实现时被某条的不同原因判红，**如实写是哪条、为什么**）。
3. **两个载体都出**（PNG 与 PDF）——因为 **F2 随载体变**（例：侦察线图
   `tests/m3-plot-recon/out-d11-red-loop.txt` 同一张图 PNG=2 / PDF=1），
   证据里**必须两个都有**，并写明"不能跨载体比 F2"。
4. **判断层**：出图后**亲眼看图**并写下"从这张图读到了什么"——机械层判不了这一层，**不许省**。
5. 对照表要**机器抽取**（别手抄判词），并写清两侧**同源同数**。

---

### Task 6：真家族 ≥1 下的整跑 + 全库收口

**产出**：**真家族 ≥1 下的驱动器整跑**（侦察未验项） · `docs/` 的变异总数散文订正 · 全库残留扫描归零。

**硬要求**：

1. **补跑侦察未验项（本任务的核心）**：`mutate-figure-style.py` 与 `run-expected.py` 在
   **真家族 ≥1**（`mcm-plot-python` 已在仓里）下的**整跑**，贴全量输出与末行计数。
   这是唯一能证明"家族落地没把既有判据弄坏"的一步；侦察只复刻了 `M43` 的 `pre_ok` 断言，**没在真仓跑过**。
   `M43` 的前置锚已改成语义锚（不再写死普查字面量），但**别假设它一定没事**——跑出来的才算。
2. `docs/` 里凡写死变异总数的散文（`46/46` 一类）→ 改成与 Task 1 之后的总数一致；**不许留过期声明**。
3. **残留分类收口**（**替换原「全库 `git grep` 残留 = 0」——那条恒不可达**：残留里有 8 件属"改了才是错"：
   `fam == 0` 才执行的代码分支、带年代指纹的历史快照、假 skill 根读数、fixture 普查）。
   重写成**一条判据 + 一次分两层的验收**（★ **这不是把验收改软，是不许把判断层说成机械层**）：
   ① **不得残留"述说今天真仓状态"的过期陈述**（`扫到 5 个 skill` / `绘图家族 0 个` / 过期变异总数 /
   「这三个 skill 现在还不存在」一类，**且上下文在讲现状**）；**其余每一处字面量出现，必须在逐件分类表里有行**。
   **验收分两层**：
   - **机械层（一条命令一秒推翻）**：**B 钥匙一条命令；A 钥匙四条（可合成一条 `-E` 并联）**，**命中集的去重并集 == 该表的行数**——
     `git grep -n "扫到 5 个 skill"` 与 `git grep -nE "绘图家族[ ]0[ ]个"` / `git grep -nE "4[6]/4[6]"` / `git grep -nE "5[2]/5[2]"`
     四条的**去重并集 == A 表行数**；`git grep -nE "还不存[在]"` 的**命中集 == B 表行数**（键与计数见 `docs/mcm-suite-todo.md` §H.1.1）。
   - **判断层（须人读，机械层判不了这一层）**：每一行是历史/快照/仪器输出/无家族分支代码/带时点标注 ——
     由人读该行同列的复核命令确认，**如实标为判断层**。
   分类表落 `.superpowers/sdd/task-m3-plot-t6-report.md`，
   并在 `docs/mcm-suite-todo.md` §H.1.1 留一份**入库副本**（报告在 gitignored 目录，不能只活在会话里）。

---

## 结束条件

六个任务全绿后，派**最终全分支复审**（范围 = 本模块基线到 `HEAD` 的全部提交），
按结果修复或收口 ⇒ 台账 + `docs/mcm-suite-todo.md` §H/§H.1 + 记忆 + 推送（仓外 worktree 配方，只推 `docs tests .claude tools`）。
