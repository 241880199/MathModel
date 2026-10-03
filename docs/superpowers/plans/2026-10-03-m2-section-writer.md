# `mcm-section-writer` + `mcm-memo` 实施计划（2026-10-03）

设计：`docs/superpowers/specs/2026-10-03-m2-section-writer-design.md`（**本计划的每个"为什么"都在那里**，提交 `9c9ad72`）。
**先例（照抄其节奏）**：`docs/superpowers/plans/2026-10-03-m1-topic-select.md` —— **同层姊妹支**，
任务级走「实现 → 独立复核 → 修复 → 定点复核」，收尾走「全分支终审 → 推送」。

**读数来源**（四类，见设计件顶部）：
- **官方**：`corpus/official/INDEX.md` §2.5（10 条内容清单）· §2.1.6（题目特定要求）
- **纪律**：`docs/mcm-writing-discipline.md`（14 条，三层有序）—— **唯一权威表述**
- **镜像**：`.claude/skills/mcm-selfreview/SKILL.md` 的 `自查 B1–B11`（官方 10 条清单的逐条化）
- **实测对照**：`tests/skills/arch-cases/` + `judge.md` / `judge-green.md` —— **只有 S1/S2 两节**

**用户已裁（不要再问）**：设计 §0 三条 —— ① 节覆盖 = **全部正文节、按证据强度标注**
② 落**入库可重跑的 `check-section.py`** ③ 本支**另含 `mcm-memo` 与 §H.3 ① 的 `mcm-abstract` 四格去重**（后者单开 Task + 独立复核）。

---

## Global Constraints（**每个任务的复审都要拿到这一份**）

1. ★★ **两件新 skill 都是家族外**（与 `mcm-playbook` / `mcm-topic-select` 同）：
   `FAMILY_RE = ^(?:mcm-plot-.+|mcm-table|mcm-schematic)$` **不含它们** ⇒ **无 `K2` 指针义务、无 `K3` 零数字约束**、**不改家族计数**。
   ★ **不许**把它们塞进家族正则。
2. ★★★ **`A9` 的两个数是「跨 Task 的共享可变值」—— 每个建 skill 的 Task 都要把它改到自己那一步的终值，否则**总有一个 Task 的门必红**（**复核当场点出的一处设计缺陷，初稿没处理**）**：
   `docs/mcm-writing-discipline.md` 的 **`:3`**（`grep -rn "mcm-writing-discipline" .claude/` 命中数，现 **5**）
   与 **`:4`**（`.claude/skills/` 目录数，现 **12** + 名单）—— `自检件 §A 的 A9`（`check-writing-discipline.py:543-562`）**两个都读、两个都当场重算**。
   ⇒ **口径（写死）**：
   - **Task 1 收工时**：`mcm-memo` 尚不存在 ⇒ 目录数 = **13**，`:3` 的命中数按**当场实跑**写。
   - **Task 4 收工时**：`mcm-memo` 已建 ⇒ 目录数 = **14**，**`:4` 的名单补 `mcm-memo`**，`:3` 的命中数再按当场实跑写。
   - ★ **`:3` 的命中数只在 `mcm-memo` 真的写了 `mcm-writing-discipline` 串时才变** ——
     **本支不许为了凑这个数而给它强加指针**；以**当场 `grep` 实测**为准。
   - ★ **Task 4 的任务书必须写明"顺带把 GC2 的两个数改到 14"**（初稿 Task 4 全文未提 A9 —— 那是必红的）。
   - 按本仓规矩 **「改时点标注 + 追加现值、不覆盖旧值」**；每次改完**实跑** `python tests/skills/check-writing-discipline.py` 确认绿。
3. ★★ **`mcm-playbook` 的 6 行要动（第二处涟漪，且判据管不到）** —— ★★ **只看下面这张逐行表，不要再去数"几处未建"**：
   本计划初稿与 Task 1 任务书都写过"**4 行去「未建」/ 2 行补名字**"，**那个计数是错的** ——
   按"**section-writer 的「未建」被去掉**"计是 **3 行**、按"**补名字**"计是 **3 行**（`git diff --numstat` = `phase-mistakes` 4/4 行、`timeline` 2/2 行）；
   "4"那个数来自把 `timeline.md:76` 也算成"带未建"——**而那行的「未建」说的是 `mcm-paper-architecture`、不是 section-writer**。
   ⇒ **计数会骗人；逐行表不会**（Task 1 独立复核当场抓到这个数）：
   | 行 | 现文 | 动作 |
   | :--- | :--- | :--- |
   | `timeline.md:74` | `无（M2 的 \`mcm-paper-architecture\`、\`mcm-section-writer\` 均**未建**）` | 改调 `mcm-section-writer`；**`mcm-paper-architecture` 的「未建」保留** |
   | `timeline.md:76` | 阶段 3 已列 `mcm-latex-format` · `mcm-abstract` · 纪律文档（**该行无 section-writer 的「未建」**） | **补** `mcm-section-writer` |
   | `phase-mistakes.md:44` | `该调：无（写作类 M2 的 \`mcm-paper-architecture\`、\`mcm-section-writer\` 均**未建**）` | 改调 `mcm-section-writer` |
   | `phase-mistakes.md:49` | `该调：无（同上，M2 未建）`（**不含 skill 名**） | 改调 `mcm-section-writer` |
   | `phase-mistakes.md:76` | `该调：\`docs/mcm-writing-discipline.md\`（M2 的 \`mcm-paper-architecture\` **未建**）` | **补** `mcm-section-writer`（该处正是 `纪律 B1` 引用规范） |
   | `phase-mistakes.md:81` | `该调：\`docs/mcm-writing-discipline.md\``（**无「未建」**） | **补** `mcm-section-writer` |
   ★ **`check-playbook.py` 的 `T3` 抓不到**（其逻辑 `if tok in existing: continue` —— **见名字存在就跳过**）。
   ★ 改完**必须实跑** `python tests/skills/playbook/check-playbook.py` 确认仍 **5/5**（**实测，不许推断**）。
4. ★★ **`PLAYBOOK-evidence.md` 绑 blob ⇒ 同批重跑生成器（第三处涟漪）**：
   该件的 `:119`/`:160` 印着 `T3 … 不存在的名字 2 个 ['mcm-paper-architecture', 'mcm-section-writer']`，
   且 `:21` 印着它自己三份文件的 blob —— **而 GC3 要改的正是那三份** ⇒ **不改就跑 = 当场变假**。
   ⇒ 同批跑 `python tests/skills/playbook/make-evidence.py`，并核三件：**blob 跟上了** · **检查器自证不变** · **生成器幂等**（连跑两次同 hash）。
   ★ 该件 `:350` 登记的缺陷「核心动作没有已建工具兜底……既没给替代技能、也没给降级路径」**由本支消解** ⇒
     按本仓口径**改时点标注**（历史判断保留、追加现值），**不覆盖旧值**。
5. ★ **总 skill 数捕获件（第四处，只登记、不重跑）**：那批印着「扫到 1N 个 skill」的 `*-verify.txt`
   会再假一次（12 → **14**）。依 `mcm-playbook` Task 4 已定口径：**家族外 skill 落地不触发捕获件重生成** ⇒ **只登记**。
   ★ **枚举不声称穷尽** —— `tests/m3-matlab-recon/README.md:14`、`tests/m3-plot-recon/README.md:11` 等**说明件也内嵌该读数**，
     **派发时以现场 `git grep` 为准**。
6. ★★ **判据名：`mcm-section-writer` 用 `SW1–SW8` · `mcm-memo` 用 `MO1–MO4`**。
   **已实测不撞名**（见质检记录 P2）。**不许用 `D*`** —— `自检件 §D` 的覆盖守卫已占用 `D1–D3`。
7. ★★ **检查器的射程不许夸大**：`SW1`/`SW2` 是**硬失败**；`SW3–SW8` **一律只出"提请复核"（`WARN`），绝不判死**
   —— 它们的阈值全是**〔判词读数〕**（两轮度量脚本**未落盘**，不可复算）。
   ★ 工具头部与 `references/metrics.md` 都必须**明写这条**，并写明 **`judge-green.md:270`「0 与 0 之间无法定阈」**。
8. ★★ **任何词表判据必须先拿真值自测**（`judge.md:238` 明令）：
   工具**内置**这条；**词表在 `true-S1.md`/`true-S2.md` 上命中 ⇒ 报"词表不可用"，不报产物有罪**。
9. ★★ **纪律文档是唯一权威**（`docs/mcm-suite-lessons.md` 4.8）⇒ `references/**` 里凡引纪律
   **只给条号 + 「怎么查」的具名动作，绝不复述规则原文**。
10. **写入一律 `write_bytes`；全 LF（CRLF=0）**。
11. **凡数字必来自当场跑过的命令**；**「我没找到」≠「它不存在」**；全称/强弱断言词要么有实测背书、要么加限定；**凡列清单必写「不声称穷尽」**。
12. **声明了覆盖就必须有一次真的红**；**判据只能从失败方向证明**。
13. **收工门（全路径，全绿）** —— ★ **每条都已在本仓核实存在**：
    `python .claude/skills/mcm-section-writer/check-section.py` · `python tests/skills/section-writer/mutate-section-writer.py` ·
    `python .claude/skills/mcm-memo/check-memo.py` · `python tests/skills/memo/mutate-memo.py`（**以上四条本支新建**）·
    `python tests/skills/check-writing-discipline.py` · `python tests/skills/mutate-writing-discipline.py` ·
    `python tests/skills/playbook/check-playbook.py` · `python tests/skills/playbook/mutate-playbook.py` ·
    `python tests/check-index-pointers.py` ·
    `python tests/skills/figure-choose/check-house-style.py` · `check-spec-pointers.py`（**家族仍 5 个**）· `check-style-table-freshness.py` ·
    `python tests/skills/figure-choose/gen-style-table.py --check` · `python tests/skills/figure-choose/fixtures/run-expected.py` ·
    `python tests/skills/figure-choose/mutate-figure-style.py`（**64/64**）·
    `python tests/skills/plot-python/check-style-freshness.py` · `python tests/skills/plot-matlab/check-style-freshness.py` ·
    `python tests/skills/table/check-table-style.py` · `python tests/skills/table/mutate-table-style.py`（**20/20**）·
    `python tests/skills/schematic/fixtures/make-fixtures.py --check` ·
    `python tests/skills/topic-select/check-topic-select.py` · `python tests/skills/topic-select/mutate-topic-select.py`
    ★ **Task 1 跑门时要减掉本支那四个还不存在的脚本**。
    ★★ **已知不在本表内的两个真变异驱动器**（复核点出）：`tests/skills/plot-python/mutate-plot-style.py` ·
    `tests/skills/plot-matlab/mutate-plot-style.py` —— 它们**也不在 `m1-topic-select` 的门里**（`2026-10-03-m1-topic-select.md:42-49`）
    ⇒ 这是**既有缺口**（本支不动绘图 skill、**不收**，理由在此写明，**不是静默漏掉**）；同理 `tests/skills/figure-choose/fixtures/make-fixtures.py`
    的**产出**已被 `fixtures/run-expected.py` 传递覆盖。
    ★ **口径**：**本表不声称穷尽全仓脚本**（`tests/m3-*` / `tests/papers/*` 属别的子系统，本支不涉）。
14. **不许提交脏树**；任务之间**另起提交**；**不许 `--amend`**。
15. ★ **不许**用"读-改-写写成一条表达式"的写法（先求值左边就截断 —— 清空过本仓一个 880 KB 的文件）。
16. ★★ **临时件只许落两处**：**仓内 `build/`** 或**固定名字的容器**；**绝对不许落在盘根**（`C:\` / `D:\` 直接下面）。
    路径参数一律写 `D:/...` 形式；`cd` 之后先 `pwd` 核一次。

## 派发指令必带（每次派 subagent 都要附）

- 任务书路径（本文件的那一节 + 该任务的 brief 文件）· 报告落点 `.superpowers/sdd/task-m2-sw-t<N>-report.md`（**必须真的落盘**）。
- Global Constraints 全文 · 基线 commit（派发前 `git log -1 --format=%H`，**不许用 `HEAD~1`**）。
- 明确：**只回报**状态 + 提交 + 一句话测试结论 + 顾虑；**不要把报告内容复制进回复**。
- ★ **控制者写的任务书本身也是候选错误** —— 执行者遇到与任务书矛盾的事实，**以实测为准并当场报告**。

---

## 质检记录（**写计划时查出来的陷阱**，不是事后补的）

### P1 ★★ 本支有**四处**涟漪，**四种处置各不相同 —— 别混成一件事做**
① `A9` 两数（GC2）**改**；② playbook 6 处「未建」（GC3）**改**；③ `PLAYBOOK-evidence.md`（GC4）**改完必须同批重跑生成器**；
④ 总 skill 数捕获件（GC5）**只登记、不重跑、不手改**（手改捕获件 = 造伪）。
★ **先例**：`mcm-topic-select` Task 1 正是把这四处混着做，被 Pre-Flight 当场挡回一次。

### P2 ★★ 判据名会撞 —— **实测过才敢用**
本仓同时活着**至少十套**短编号，`A/B/C/D/E` 被其中四套共用（设计件记号表）。
**本计划的实测结论**：`SW1–SW8` 在 `.claude/**` `tests/**` `docs/**` `tools/**` 里**只命中本设计件自身**；
`MO1–MO4` **0 命中**。⇒ **可用**。
★ **`D1–D3` 已被 `自检件 §D` 的覆盖守卫占用** ⇒ 本支**不许**用 `D*`（这正是设计件初稿犯过的那处）。

### P3 ★★ 检查器**不是**判卷器 —— 射程写死在文档里
`SW1`/`SW2` 硬失败（有 `judge.md:222-225` 的**明确判据**背书）；**`SW3–SW8` 只出 `WARN`**。
★ 它们的阈值是**〔判词读数〕**：`judge.md` 的判者脚本**两轮都没落盘** ⇒ **不可重跑、不可复算** ⇒ **不许读成"达标线"**。

### P4 ★★ 词表不先自测 ⇒ 会**误伤真值**
`judge.md:238` 明令任何词表判据**使用前必须先在 `true-*` 上跑一遍**。
★ 本支的 `SW5`（对比式 + 强调式）**一定有词表** ⇒ 这条是**硬要求**，不是建议。

### P5 ★★ 纪律文档**只许给条号**，不许复述
`references/sections.md` 的 ③ 格若把 `纪律 A1` 的正文抄一遍，就**造出第二份权威** ——
`docs/mcm-suite-lessons.md` 4.8 明写：同一句话写两处，**必有一处忘改**。
★ 正确形态：**「`纪律 A1`（怎么查：把该节每个数字回写手输入的要点清单里 `grep` 一次）」**。

### P6 ★★ `mcm-memo` 有**两条**官方规则，**漏第二条会把队伍引向署真名**
① 触发：`corpus/official/MCM-ICM_Tips.txt:160-162`；② ★ **匿名落款**：同文件 **`:239-241`**
（*"be sure not to sign the letter with your name … we suggest using: **Sincerely, Team #2000000**"*）—— **一票否决类**。
★ 设计件初稿写"官方只有一句" —— **那是假的**，复核当场纠正。**执行者不许退回那个说法。**

### P7 ★★★ §6 的四格去重会撞**一份金标**，必须同批改三处
`自检件 §B 的 B2`（出站指针全扫）的 `ANCHORS` 表**逐行钉死了 checklist 的那四行正文**（`check-writing-discipline.py:670-674`），
`RANGE_ENDS` 另钉四个区间止行（`:694`）；而 `docs/mcm-writing-discipline.md:171-174` 的指针**逐字引用它们的标题**。
⇒ 改 Q7/Q8/Q9/Q12 的正文 ⇒ **三处必须同批改**：① checklist 条目 · ② 两个金标表 · ③ 纪律文档那四行引用。
★ 另有两条不变量：`E7`（清单顶层 **15** 条）与 `E11`（`### Q<n>` **13** 条）**不许增减**。

### P8 ★★ S1/S2 的证据强度**不许放大**
- **GREEN 侧**两节**各 1 个产物**；**RED 侧 3 个**（S1 一臂 + **S2 两臂**：自由臂 `out-S2.md` + 压力臂 `out-S2-p.md`）。
- **只有 S2 那一对是干净的单变量对照**（`judge-green.md:264`）；S1 那一对**混了产物形态**（markdown vs LaTeX）。
- **结论节的 `[实测对照]` 只覆盖文风层** —— 它对应的官方项（`自查 B9`「明确报告结果」）**RED 轮自认测不到**（`judge.md:247`）。
⇒ ★ **两种计法要分清（本计划初稿写错过，Task 1 执行者当场指出并改正）**：
**按案例计 = 2 个**（S1 · S2）；**按节计 = 3 节**（§4 = S1 · §7 = S2 · §8 = S2 —— **S2 一个案例覆盖两节**）
⇒ 故 **`[实测对照]` 三节、`[仅规格来源]` 五节**（**不是**"两节 / 六节"）。
**不许**把两个案例的读数写成"该节的普遍规律"。

---

## 文件结构（终态）

```
.claude/skills/mcm-section-writer/
├─ SKILL.md                    # 短契约：节路由表 · 输入/输出契约 · 检查清单 · 指针（<150 行）
├─ check-section.py            # 检查器：SW1–SW8（本支新建）
└─ references/
   ├─ sections.md              # 8 节 × 五格（本 skill 的主体）
   ├─ section-edges.md         # 节边界表：这节不写什么、留给哪节（纪律 B3/B6 的落点）
   └─ metrics.md               # SW 各判据的口径 + **它的边界**（判词读数挂牌 · 词表自测要求）

.claude/skills/mcm-memo/
├─ SKILL.md                    # 短契约：只在题面要求时产出
├─ check-memo.py               # 检查器：MO1–MO4（本支新建，随 skill 走）
└─ references/format.md        # 一页备忘录的体例（自订项全标 [社区]）

tests/skills/section-writer/
├─ mutate-section-writer.py    # 变异驱动器（调 skill 目录里的检查器）
├─ make-evidence.py            # 对照证据生成器
├─ SECTIONWRITER-evidence.md   # 由 make-evidence.py 产出
├─ green/                      # **带 skill** 的产物与对照（RED 侧只读复用 tests/skills/arch-cases/）
└─ README.md

tests/skills/memo/
├─ mutate-memo.py · make-evidence.py · README.md
```

★ **判据落点（写死，别让执行者猜）**：
- **`mcm-section-writer` 的判据本体 = `.claude/skills/mcm-section-writer/check-section.py`**（**随 skill 走** —— 同 `mcm-abstract/check-summary.py` 的先例：使用者拿到 skill 就能跑它）。
- **`mcm-memo` 的判据本体 = `.claude/skills/mcm-memo/check-memo.py`**（同上）。
- **测试侧只放驱动器与证据**（`mutate-*.py` / `make-evidence.py` / `README.md`），**调用 skill 目录里那一份**。
- ★★ **判据逻辑全仓只许有一份** —— **不许**在 `tests/` 下再写一份"镜像版"（两份 = 必然漂移，本仓栽过同型）。
★★ **注意**：本仓既有 `check-*.py` 的落点**两种都有** —— `mcm-abstract/check-summary.py` 在 **skill 目录**，
而 `figure-choose` / `playbook` / `table` / `topic-select` 的在 **`tests/`**。本支**按设计件 §1.2 选定 skill 目录侧**，**理由如上（随 skill 走）**。
★ **为什么没有 `assets/`**：本 skill **不产图、不产骨架**（骨架是 `mcm-latex-format` 的 `assets/mcm-2027-summary.tex`）。

---

## Task 1：`mcm-section-writer` 的 `SKILL.md` + 三份 `references` + **全部涟漪**

**产出**：`.claude/skills/mcm-section-writer/{SKILL.md, references/sections.md, references/section-edges.md, references/metrics.md}` ·
`docs/mcm-writing-discipline.md` 的 `:3`/`:4` 改到本 Task 终值 · `mcm-playbook` 6 行按 GC3 表改 · `PLAYBOOK-evidence.md` 重跑 ·
★ **台账** = **`docs/mcm-suite-todo.md`**（本支的登记全落在这**一个**文件；进度台账另由 Task 6 追加）。

**硬要求**：

1. **`SKILL.md`（短契约，<150 行）**：
   - **触发**：description 写清「**你正在写论文的某一节**」；触发词中英混合（写正文、这一节怎么写、write a section…）。
   - **节路由表**：你写哪一节 → 读 `references/sections.md` 的哪一段 → 该节挂哪几条 `纪律` 条号。
   - **输入契约**（照设计 §1）：题面 + **哪一节** + **该节要点清单**（形态照 `brief-S1.md`）+ 已定稿图表与结果。
   - **输出契约**：① 该节 `.tex` 片段；② 该节的按节自查单。
   - **边界**：不排版 / 不写摘要 / 不出图表 / 不做全稿合规 / 不做页数预算 / **不判是不是 AI 生成**。
2. **`references/sections.md`**：**8 节 × 五格**（设计 §3）。★★ **③ 格只给条号 + 「怎么查」，绝不复述纪律原文**（P5）。
   ★ 每节的 **证据强度标注**必须写：**§2 表**里那两节 `[实测对照]`、其余六节 `[仅规格来源]`；**不许**把标注省掉或写得含糊。
   ★ **⑤ 格（反面实例）只对两节有**：`out-S1.md:65–77`（WHO 表）· `out-S2.md` 的段末总结 10/10；**不许**把 S2 的读数搬到别的节。
3. **`references/section-edges.md`**：**一处集中**的节边界表 ——
   ① 每节「**不写什么、留给哪一节**」；② `自查 B6`（正文只放推导摘要、冗长入附录）**作为一条跨节规则**落在这里；
   ③ ★ **符号表**（`纪律 B3` 只管一节之内、跨节对齐归 `纪律 B6`）—— 正对 GREEN 轮**未修好**的那条（S1/S2 间 `p` 的语义漂移）。
4. **`references/metrics.md`**：`SW1–SW8` 的口径 + **四条边界**（设计 §4.1 逐条）：判词读数不可复算 · 词表先自测 ·
   压力臂分别设阈**本工具做不到**（**RED 侧有压力臂、GREEN 侧没有**，本工具放弃的正是 RED 那一半控制手段）·
   **明令不用的四项**（句长 CV / root-TTR / Flesch / 模板化过渡词，`judge-green.md:202-208`）。
5. ★★ **四处涟漪各按各的处置**（GC2 / GC3 / GC4 / GC5，见 P1）：
   ① `docs/mcm-writing-discipline.md` 的 `:3` 与 `:4` **改到本 Task 末的终值** —— `:4` 的目录数 **12 → 13**、名单补 `mcm-section-writer`；
      `:3` 的命中数**按当场 `grep` 实跑写**（GC2 有完整口径）；
   ② `mcm-playbook` 的 6 行**按 GC3 的逐行表改**（★ **别数"几处未建"** —— 那个计数已证会骗人，见 GC3）；
      ★ **`mcm-paper-architecture` 的「未建」一律保留**；
   ③ ★★ **同批重跑** `python tests/skills/playbook/make-evidence.py`，并核三件（blob 跟上 / 检查器自证不变 / 幂等）；
      ★★ **时点注必须改在生成器源里**：`PLAYBOOK-evidence.md:350` 那段正文的**源头是 `tests/skills/playbook/make-evidence.py:239`**
        （复核实测）⇒ **只改 `.md` 再重跑 = 时点注被抹掉；只改 `.md` 不重跑 = 破坏幂等/可重放**。**改源串，再重跑**。
   ④ 总 skill 数捕获件 **只登记、不重跑**；台账写清"这一类"；
   ⑤ `mcm-topic-select` 的 `SKILL.md:27` · `references/method.md:113`：**去掉本支两件新 skill 的「未建」**
      （`mcm-paper-architecture` 的**保留**）；★ 但 `mcm-memo` 要到 **Task 4** 才建 ⇒
      **本 Task 只去掉 `mcm-section-writer` 那一个，`mcm-memo` 的「未建」保留到 Task 4**。
6. ★ **未建的明写「未建」**：`mcm-paper-architecture`（本支**无** `T3` 那种判据守 ⇒ 靠自律 + 复核）。

**验收**：8 节**每节五格齐备**且**带证据强度标注** · `references/**` 里**纪律条目全部只给条号**（抽查 10 条，0 条复述原文）·
**`check-writing-discipline.py` 实跑绿**（`A9` 两数跟上）· **`check-playbook.py` 实跑 5/5** ·
`PLAYBOOK-evidence.md` 的 blob **与三份文件现取 hash 一致** · `check-spec-pointers.py` 家族**仍 5 个** ·
收工门全绿（**减掉本支四个尚不存在的脚本**）。

---

## Task 2：`check-section.py`（`SW1–SW8`）+ 变异驱动器

**产出**：`.claude/skills/mcm-section-writer/check-section.py`（**判据本体，全仓唯一一份**）·
`tests/skills/section-writer/mutate-section-writer.py`（**驱动器**）。

**硬要求**：

1. **八条判据逐条落地**（设计 §4 表），**`SW1`/`SW2` fail-closed 硬失败、`SW3–SW8` 只出 `WARN`**（P3）。
   ★ **`SW1` 的燃料**：`--input <要点清单>` 缺省即**报"无法判定"**，**不许报 PASS**。
2. ★★ **词表自测是硬要求**（P4）：`SW5`（对比式 + 强调式）等**任何词表判据**，**每次运行先拿
   `tests/skills/arch-cases/true-S1.md` / `true-S2.md` 跑一遍**；命中 ⇒ 输出 **`词表不可用：真值命中 N 处`** 并
   **把该项降级为"不可判"**，**不得**据此判产物有罪。
3. **CLI 输入面（写死）**：`python check-section.py <节文件> --section <8 节之一> [--input <要点清单>]`。
   ★ `--section` 取值**必须**是设计 §2 那 8 个名字之一；**给不认识的值 ⇒ fail-closed 红**（不许静默绿）。
4. **变异驱动器**：**`SW1`–`SW8` 每项至少一条变异** + **"必须仍绿"的射程边界对照**；**合计行不是末行**。
   ★ 八条必查（**逐条真红**）：`SW1` 删掉表内数字的出处 ⇒ 红 · `SW2` 抹掉 `illustrative` 标注 ⇒ 红 ·
   `SW3` 把每段末尾都写成总结句 ⇒ `WARN` · `SW4` 灌水膨胀 ⇒ `WARN` · `SW5` 塞满 `rather than` ⇒ `WARN` ·
   `SW6` 塞自评套话 ⇒ `WARN` · `SW7` 连续极短断言句 ⇒ `WARN` · `SW8` 塞可整段删除句 ⇒ `WARN`。
   ★ **并各有一条"仍绿"对照**：**真值 `true-S1.md`/`true-S2.md` 上，`SW3–SW8` 不得报 `WARN`**
     （**若报，说明阈值/词表有问题 —— 如实报告，不许调阈值把它压绿**）。
5. ★★ **工具必须自带两条「关于它自己」的静态自检**（复核实测：初稿把这条只写在缺口归宿表里、**Task 2 正文根本没有** ⇒ 那条"去处"判不出来）：
   ① **四项禁用不得出现** —— 源码/输出里出现 **句长 CV · root-TTR · Flesch · 模板化过渡词** 任一即 **FAIL**
     （依据 `judge-green.md:202-208`）；
   ② **"压力臂分别设阈本工具做不到"这段局限文字必须在场** —— 缺即 **FAIL**（这样"明写为局限"才**判得出来**）。
   ★ 两条都要进 `mutate-section-writer.py` 的必查清单：**把那项禁用写进工具 ⇒ 红**；**把那段局限文字删掉 ⇒ 红**。
6. **不许**为了凑数写恒真的检查；**判据只能从失败方向证明**。
7. **本支不动**任何既有 `check-*.py` / `mutate-*.py`（**唯一例外见 Task 5**，且那是改**金标**不是改逻辑）。

**验收**：`SW1`/`SW2` 在**已知好的产物**上绿、在变异体上**真红** · `SW3–SW8` 在变异体上**真出 `WARN`**、
在**真值上不出 `WARN`** · **两条静态自检在变异体上真红**（把禁用项写进工具 · 删掉局限文字）·
`mutate-section-writer.py` 合计行全红 · **既有各支的门一个都没动且仍全绿**。

---

## Task 3：RED / GREEN 对照与证据

★★ **本任务面对的是「三个工况」，不是两个**（复核点出 —— 初稿把第三臂整整漏了）：

| 臂 | 产物（**都已在库**） | 给了什么 | 本任务做什么 |
| :--- | :--- | :--- | :--- |
| **RED** | `arch-cases/out-S1.md` · `out-S2.md` · **`out-S2-p.md`** | **什么都不给** | **只读，不重跑** |
| **纪律轮**（既有 GREEN） | `arch-cases/out-S1-g.md` · `out-S2-g.md` | `docs/mcm-writing-discipline.md` 一份 | **只读，不重跑** |
| ★ **本支的 skill 轮** | `tests/skills/section-writer/green/`（**本任务新建**） | 本 skill（`SKILL.md` + 三份 references + 检查器） | **跑它** |

★ **不重跑 RED 与纪律轮的理由**：它们**逐字冻结、无生成器可重跑**（`arch-cases/README.md` §一 末）。
★ **`out-S2-p.md` 是 RED 独有的压力臂** —— **skill 轮没有对应臂**，对照表里**单列一行并写明"无对应"**，
**不许**把它塞进干净对照里当第三列。

**产出**：`tests/skills/section-writer/green/`（**带 skill 产物**）· `make-evidence.py` · `SECTIONWRITER-evidence.md` · `README.md`。

**硬要求**：

1. **输入照 RED 原样**：`tests/skills/arch-cases/README.md:38` 写死 ——
   *"给写手的正式输入 = `brief-S1.md`（或 `brief-S2.md`）**+** 题面 `../abs-cases/case-A-problem.txt`，**仅此两项**"*。
2. ★★ **泄题清单（初稿只列了三类，复核实测点出四类漏项 —— 给了任何一项，这次对照当场作废）**：
   - `tests/skills/arch-cases/` 的 `true-S1.md` · `true-S2.md` · `judge.md` · `judge-green.md` · `README-RED.md` · `README.md`
   - ★★ **`tests/skills/abs-cases/case-A-body.md`** —— **`true-S1.md` 就是它第 147–296 行的逐字节副本**（`true-S1.md:3` 自述）
     ⇒ **给它＝给答案全文**；同目录的 `case-A-body-partial.md` 同理
   - ★ `tests/skills/arch-red-evidence.md` · `arch-green-evidence.md` · `arch-cases/judge*.md`（满是判词读数）
   - ★ **既有的 `out-S1-g.md` / `out-S2-g.md`**（纪律轮产物）与**全部 `out-*.md`** —— 它们是**答案的近似物**，
     写手看过就再也测不出"自己会不会写成那样"
   ★ **口径**：给写手的**只有** `brief-*.md` + `case-A-problem.txt`；**目录都不给他看**（用复制到仓外临时目录再喂的方式，同通则 8）。
3. **怎么把 skill 交给写手（写死，照既有先例）**：本仓既有的两轮 GREEN 都是**直接把文件给写手** ——
   纪律轮给 `docs/mcm-writing-discipline.md`（`arch-green-evidence.md:6`）；abs 轮实测对象是
   `.claude/skills/mcm-abstract/{SKILL.md, check-summary.py}`（`abs-green-evidence.md` §0.1）。
   ⇒ **本支照此**：把 `.claude/skills/mcm-section-writer/` **整目录复制**到仓外临时目录，写手读它并**被要求跑一次检查器**。
   ★ **不许**只给 `SKILL.md`（那等于没给 references 与工具）；★ **写手自述"我用了 skill 的哪一条"要单独记录**（不算论文措辞）。
4. **对照组口径**：**只评内容覆盖与纪律条目命中，不评风格**（真值是 PDF 转换件，标点与句法表面不可比 —— `judge.md` §5.3 第 3 条）。
   ★ **对照表必须标出"哪两列可比"** —— ★★ **本句初稿写错了，Task 3 执行者以实测推翻**：
     初稿说"**只有「RED 自由臂 vs skill 轮」在 S2 上是干净单变量**"，**实测不成立** ——
     **skill 轮的产物是 `.tex`**（`SKILL.md` 的输出契约就是"该节 `.tex` 片段"），而 **RED-S2 是 markdown**
     ⇒ **那一对同样同时换了「干预」与「产物形态」**。
     ⇒ **实际结论：本支的 skill 轮与 RED 之间，没有任何一对是干净的单变量对照**；
     **唯一的干净单变量对是「RED-S2 vs 纪律轮-S2」（两轮同为 markdown，`judge-green.md:264`）——它不含 skill 轮。**
     ★ 这条限制**必须写在证据件里**，**不许**把 skill 轮的改善整个归给 skill。
   **S1 那一对混了产物形态**（RED 是 markdown、GREEN 是 LaTeX 源码，`judge-green.md:264`）⇒ **S1 上的改善不能全归给 skill**。
5. ★★ **三条已登记缺口的判定要分开写（复核指出：3 条里只有 1 条判得出来）**：
   - **`纪律 A3`**（声称读过没读过的部分）—— **判得出**（`judge-green.md:220`/`:249`），**逐条判"修好没有"**；
   - **`纪律 B3`**（跨节符号一致）与 **`纪律 B1`**（文末文献表）—— ★ **本任务判不出**：
     本 skill 是**逐节**工具、**不给全文**，而 `judge-green.md:251`/`:267`/`:279` 自认这两项**"无从判"**。
     ⇒ **照实记"仍无从判"**，**不许**写成"已修好"或"未修好"。
   ⇒ 故 Task 1 的 `section-edges.md` 承接这两条，**是"给了落点"，不是"已被验证有效"** —— 证据件里要写清这个区别。
6. ★ **样本量与形态的边界必须写在证据件里**（P8）：skill 轮每节 **1 个产物** · **无压力臂**（RED 侧才有）·
   **S1 那一对混了形态**。
7. **可重放性**：证据件由 `make-evidence.py` 生成；★ **生成器若记录自身工作树状态，必须"先干净 → 再捕获 → 再提交 → 再跑一次证不动点"**
   （`docs/mcm-suite-lessons.md` 通则 14）。
8. **RED 与纪律轮的四份产物** ⇒ **本支不搬动、不改写、不重跑**。

**验收**：skill 轮产物入库 · **泄题清单逐项在派发指令里列全**（含 `case-A-body.md`）·
对照表**标出可比的列**且**把 `out-S2-p.md` 单列** · **`A3` 逐条判、`B3`/`B1` 照实记"无从判"** ·
证据件**可由生成器重放**（同 hash）。

---

## Task 4：`mcm-memo`

**产出**：`.claude/skills/mcm-memo/{SKILL.md, check-memo.py, references/format.md}`（**判据本体随 skill 走**）·
`tests/skills/memo/{mutate-memo.py, make-evidence.py, MEMO-evidence.md, README.md}`。

**硬要求**：

1. **`SKILL.md`**：★ **description 必须把触发条件写死** —— 「**题面明确要求 letter/memo 时**」；
   **并明写"题面没要求就绝不产出"**（它不是通用交付物 —— 这是它最容易误触发的点）。
2. **两条官方规则都在**（P6）：① 触发（`Tips:160-162`）② ★ **匿名落款**（`Tips:239-241`，含官方建议写法
   `Sincerely, Team #2000000`）。**两条都标 `[官方]†`**（**仅见于 Tips**）。
   ★ 凡"体例应当如何"的自订项，**一律标 `[社区]`（操作纪律）+ 官方指针**，**不标 `[官方]`**。
3. **`references/format.md`**：面向指定受众的一页备忘录体例（受众在文首点名 · 结论先行 · 不写公式推导长段 · 匿名落款）。
4. **检查器 `check-memo.py` 判据 `MO1–MO4`**（★ 已实测不撞名）：
   `MO1` 触发条件在场（题面未要求 ⇒ 不得产出该文件）· ★ `MO2` **匿名落款**（须为 `Sincerely, Team #<队号>` 形态，
   **出现真名/校名 ⇒ 红**）· `MO3` **恰好一页**（`pdfLaTeX` 编两遍读页数，口径同 `mcm-abstract/check-summary.py`）·
   `MO4` 受众在文首点名。
   ★ **`MO1` 的燃料**：`--problem <题面>` 缺失 ⇒ **报"无法判定"**，不许报 PASS。
5. **变异驱动器**：`MO1–MO4` 每项至少一条变异（含**"署真名"那条**—— 它对应官方硬规则）+ 一条"仍绿"对照。
6. **`mcm-selfreview` 的 `自查 A14` 是它的检查侧** ⇒ SKILL.md 里**明写这条关系**，**不重复** A14 的判据。
7. ★★ **本 Task 必须顺手做掉 GC2 的第二半**（`mcm-memo` 一建，`A9` 的目录数就变了）：
   把 `docs/mcm-writing-discipline.md:4` 的目录数 **13 → 14**、名单**补 `mcm-memo`**；
   `:3` 的命中数**按当场 `grep` 实跑**（**memo 若没有真的指向该文件，就不许凑数加指针**）；
   改完**实跑** `python tests/skills/check-writing-discipline.py`。
   ★ **不写这一条的后果**：Task 4 的收工门**必红**（复核当场算出来的）。

**验收**：四条判据各自真红 · 真值（题面未要求 memo 的场合）上 `MO1` **不出红** ·
`check-memo.py` 在已知好的产物上绿 · 收工门全绿。

---

## Task 5：§H.3 ① —— `mcm-abstract` 四格去重（**单开、独立复核**）

★★ **执行时机（写死）**：**必须在 Task 1 之后跑** —— 本 Task 要改的
`docs/mcm-writing-discipline.md:171-174` **与 Task 1 改的 `:3`/`:4` 是同一个文件**（复核点出的文件冲突对）。
⇒ **不许与 Task 1 并行**；开工前先 `git log -1` 确认 Task 1 已提交、**工作树干净**。

**依据**：`docs/mcm-writing-discipline.md:171-176`（重叠表，含"合并方式应为……**须单独走一遍流程**"）·
`docs/mcm-suite-todo.md:1551`/`:1554`。

**做什么**：把 `mcm-abstract/references/quality-checklist.md` 的 **Q7 / Q8 / Q9 / Q12** 改成
**指向** `纪律 A1 / 纪律 A2 / 纪律 A5 / 纪律 C1`（**保留"摘要特有项"在 `mcm-abstract` 侧**）。

**硬要求（P7 逐条）**：

1. ★★ **三处同批改，缺一即红**：
   ① `quality-checklist.md` 的那四个条目正文；② `check-writing-discipline.py` 的 **`ANCHORS`**（`:670-674`）
   与 **`RANGE_ENDS`**（`:694`）金标；③ `docs/mcm-writing-discipline.md:171-174` 那四行**逐字引用**这些标题的指针。
2. ★ **不许增减条目数**：`E7` = 清单顶层 **15** 条 · `E11` = `### Q<n>` **13** 条。
3. ★ **`--pmap` 的头部自陈**（`:17` 的 107 条出站指针 / 76 个去重落点 / 覆盖率）**改完必须与 `--pmap` 现跑一致**
   （`自检件 §E 的 E1` 会当场比对；★ **`E1` 属 `§E` 机器守卫**，**不在 `§A`** —— 初稿标错过，复核当场纠正）。
4. **这是对已交付冻结 skill 的改动** ⇒ 走**独立的实现 → 独立复核 → 修复 → 定点复核**，**不与 Task 1–4 合并**。
5. ★ **改前先留痕**：记下改动前 `python tests/skills/check-writing-discipline.py` 的**逐行输出**，
   改后**再跑一次**，**逐行比对"哪些行变了"**——`B2` 的判词形态变化要**解释得清**，不许只说"变绿了"。

**验收**：`check-writing-discipline.py` **全绿** · `mutate-writing-discipline.py` **全红** ·
`A9` 两数仍对 · `E7`/`E11` 条数未变 · **`--pmap` 三数自陈一致** · `mcm-abstract/check-summary.py` 未被波及（实跑）。

---

## Task 6：全库收口

**产出**：`docs/mcm-suite-todo.md` 的 §C（M2 行）· §H.3（两条欠账）· §H.5.8h（交付节 + 计数）同批订正 ·
进度台账追加。

**硬要求**：

1. **§H.2.2 的「家族成员计数散文」与「捕获件里印着总 skill 数」两条**：本支**再加两个家族外 skill** ⇒
   ① **家族计数不变**（仍 5，实跑 `check-spec-pointers.py` 核）；② **总 skill 数 12 → 14** ⇒ 按已定口径**只登记、不重跑**。
2. **全库回扫本支新造的陈旧断言**（写法：`git grep -n '<新 skill 名>' -- .` **逐处看有无残留「未建」**；
   ★ **量词扫描面 = 全仓**，不用 `.claude/` 收窄 —— 陈旧「未建」**也活在 `.claude/` 外面**）。
3. ★ **`mcm-written-discipline.md` 的 `:4` 名单**要**列全 14 个**（两个新 skill 都在）。
4. ★ 台账里**登记**：① 总 skill 数捕获件这一类**又触发一次**；② `PLAYBOOK-evidence.md:350` 那条缺陷**已消解**（带时点）；
   ③ `tests/skills/arch-cases/README.md` §五 的 `build/arch-red/` 三份 RED 产物**仍无版本**（本支仍不搬，**代价随支数递增**）。
5. **收工门全绿**（GC13 全表，含本支四条新脚本）。

**验收**：§C/§H.3/§H.5.8h 无过期断言 · 收工门全绿 · 台账已追加 · **工作树干净**。

---

## 设计件已知缺口的归宿（**逐条给去处，不许悬空**）

| 设计件的限定 | 去处（★ **复核逐条核过"承接得住吗"，三行已改**） |
| :--- | :--- |
| `纪律 A3` / `纪律 B3` / `纪律 B1` 三条 GREEN 未修好 | **Task 1**（`sections.md` ①③ 格 + `section-edges.md`）给**落点**；**Task 3 只判得动 `A3`** —— `B3`/`B1` 是逐节工具**无从判**的 ⇒ **照实记"仍无从判"**（★ 初稿写"逐条判修好没有"是**做不到的承诺**） |
| `SW3–SW8` 阈值不可复算 | **Task 2** 工具头部 + **Task 1** 的 `metrics.md` 明写；**只出 `WARN`**（可由变异体证） |
| 压力臂分别设阈**做不到** | **Task 1** `metrics.md` + **Task 2** 工具头部明写 ⇒ ★ **并且 Task 2 要有一条静态自检盯这段文字在场**（否则判不出来；初稿缺这条） |
| `judge-green.md:202-208` 明令不用的四项 | **Task 2** 硬要求 5①：**源码里出现即 FAIL**（★ 初稿只在归宿表提、正文没有） |
| RED 侧三份产物无生成器 | **Task 3** 不搬动、不改写、不重跑 |
| **设计 §8：跨节一致性「自动核」不做** | **Task 1** `section-edges.md` 给**人工落点** + **Task 3** 照实记"无从判" |
| **设计 §8：真实数据压力下的 `纪律 A1` 不做** | **Task 3** 证据件的限制清单里**明写**（`judge-green.md:268`） |
| `build/arch-red/` 三份 RED 产物无版本 | **Task 6** 台账登记（本支仍不搬） |
| `mcm-paper-architecture` 已决定不做 | **Task 1** 各处「未建」**保留**（`timeline.md:74` · `phase-mistakes.md:44/76` · topic-select 两处） |
| 总 skill 数捕获件会再假一次 | **Task 6** 只登记、不重跑 |

## 结束条件

1. Task 1–6 **全部收口**（每个任务走满「实现 → 独立复核 → 修复 → 定点复核」）。
2. **全分支终审**（独立 agent）⇒ 判 `Ready to merge`（或 `With fixes` 后修完）。
3. **推送**（按 §A.5 配方：仓外 worktree + 普通快进 + 两条硬检查；**用户已授「默认推送」**）——
   ★ **同步集必须显式剔除** `corpus/**` 与 `tests/papers/{recon,reports}/*.png`。
4. 台账与记忆更新；`agents-busy.py clear`。
