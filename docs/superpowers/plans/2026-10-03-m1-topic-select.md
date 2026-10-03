# `mcm-topic-select` 实施计划（2026-10-03）

设计：`docs/superpowers/specs/2026-10-03-m1-topic-select-design.md`（**本计划的每个"为什么"都在那里**）。
**先例（照抄其节奏）**：`docs/superpowers/plans/2026-10-03-m1-playbook.md` —— 本模块**上一支、同层姊妹**，
任务级走"实现 → 独立复核 → 修复 → 定点复核"，收尾走"全分支终审 → 推送"。
**读数来源**：`corpus/official/INDEX.md`（官方）· `corpus/papers/{PROBLEM_TYPES,MODEL_MAP,INDEX,TAGS}.md`（**我们的标注件**）。

**用户已裁（不要再问）**：设计 §0 的六条 —— 尤其 ① **逐轴证据档、不编分数** ② **带上语料分类与检索** ③ **硬时间盒 ≤2h**
④ **撤队伍画像** ⑤ **四轴 = 数据可得性+可信度 / 难度 / 拥挤风险 / 创新空间** ⑥ **家族外第二个**
★ 其中**第 3 轴**是用户当日追问后**再订正过**的：**它判的是"题面有没有吸引人扎堆的特征"，不是"预计多少队伍会选"**（**赛期内不可回答**）。

---

## Global Constraints（**每个任务的复审都要拿到这一份**）

1. ★★ **它是家族外第二个 skill**（与 `mcm-playbook` 同）：`FAMILY_RE = ^(?:mcm-plot-.+|mcm-table|mcm-schematic)$` **不含它**
   ⇒ **无 `house-style.md` 指针义务（`K2`）、无零数字约束（`K3`）**。
   ★ **不许把它塞进家族正则** —— 那会改普查读数与射程，**与用户裁决相反**。
2. ★★ **`A9` 同批清（第一处涟漪）**：`docs/mcm-writing-discipline.md` 的**同一行**载着 `A9` 会重算的**两个数** ——
   **`.claude/skills/` 目录数**（现 **11** ⇒ 落地后 **12**）与 **`grep -rn "mcm-writing-discipline" .claude/` 命中数**（现 **4** ⇒ 落地后**再变**）。
   ⇒ **一次改到位**；按本仓规矩 **"改时点标注 + 追加现值、不覆盖旧值"**（那一行**已有**两段 2026-10-03 的括注）。
3. ★★ **`mcm-playbook` 的 5 处「未建」同批改（第二处涟漪，且判据管不到）**：
   `SKILL.md:28/59` · `timeline.md:73` · `phase-mistakes.md:25/37`（实测 `grep -c` = 2+2+1 = **5**）。
   ★ **该 skill 的判据 `T3` 不会抓它** —— 其逻辑是 `if tok in existing: continue`（**见名字存在就跳过**）。
   ⇒ 这是一处**判据管不到的假话**：**必须靠人同批改**，并**在台账登记"这一类"**（否则下一个人不知道怎么发现的）。
   ★ 改完**必须实跑** `python tests/skills/playbook/check-playbook.py` 确认仍 **5/5**（**实测，不许推断**）。
4. ★ **总 skill 数捕获件（第三处，只登记）**：那 7 份印着"扫到 1N 个 skill"的 `*-verify.txt` 会再假一次 ——
   按 `mcm-playbook` Task 4 已定的口径：**家族外 skill 落地不触发捕获件重生成** ⇒ **只登记，不重跑**。
4b. ★★ **第四处涟漪（Pre-Flight 当场查出来的，会咬人）**：`mcm-playbook` 的证据件**绑着它自己三份文件的 blob** ——
   `tests/skills/playbook/PLAYBOOK-evidence.md:21` 印着 `skill_md=643cef1cca0a · timeline=fc6ef3a8c946 · mistakes=f3cbc7a48f3d`，
   **而 Task 1 要改的正是这三份**（修那 5 处「未建」）⇒ **它们一变，那一行当场变假**。
   ⇒ **必须同批重跑** `python tests/skills/playbook/make-evidence.py`，并**确认**：`PLAYBOOK-evidence.md:21` 的三个 blob **跟上了**、
   **`:23` 的检查器自证不变**（`check-playbook.py` 本支**不动**）、生成器**幂等**（连跑两次同 hash）。
   ★ 这一型正是本仓的 `M3-plot-T7c`（"改了文件没复跑命令"）⇒ **别只改不跑**。
5. ★★ **`S1` 的归一化必须复用**：`tools/papers/taxonomy.py` 的 `normalize_for_locate` / `normalize_quote`（**实测可导入**，
   `tools/papers/__init__.py` 在）⇒ **不许另写一套**（两套归一化 ⇒ 两支的"可核"会有一天对不上）。
6. ★★ **语料那套分类是"我们的标注"，不是官方** ⇒ 凡引用必带这句边界（同"不许把构造读成官方"）。
   ★ 并带三条已知边界：**`MODEL_MAP.md` 只有 2025 一年** · **六题不在语料里**（分类是当天现做）· **场景标签与模型选择无关**（语料口径 7 的用户裁决）。
7. **写入一律 `write_bytes`；全 LF（CRLF=0）**。
8. **凡数字必来自当场跑过的命令**；**"我没找到" ≠ "它不存在"**；全称/强弱断言词要么有实测背书、要么加限定；**凡列清单必写"不声称穷尽"**。
9. **声明了覆盖就必须有一次真的红**；**判据只能从失败方向证明**。
10. **收工门（全路径，全绿）**：`python tests/skills/topic-select/check-topic-select.py`（**本支新建**）·
    `python tests/skills/topic-select/mutate-topic-select.py`（**本支新建**）· `python tests/skills/playbook/check-playbook.py`（**5/5**）·
    `python tests/skills/playbook/mutate-playbook.py`（**16/16**）· `python tests/skills/check-writing-discipline.py` ·
    `python tests/skills/figure-choose/check-house-style.py` · `python tests/skills/figure-choose/check-spec-pointers.py`（**家族仍 5 个**）·
    `python tests/skills/figure-choose/fixtures/run-expected.py`（`MISMATCH 0 / 34`）· `python tests/skills/figure-choose/check-style-table-freshness.py` ·
    `python tests/skills/plot-python/check-style-freshness.py` · `python tests/skills/plot-matlab/check-style-freshness.py` ·
    `python tests/skills/figure-choose/gen-style-table.py --check` · `python tests/skills/table/mutate-table-style.py`（`20/20`）·
    `python tests/skills/figure-choose/mutate-figure-style.py`（`64/64`）· `python tests/skills/schematic/fixtures/make-fixtures.py --check`。
    ★ **Task 1 跑门时要减掉本支那两个还不存在的脚本**（Pre-Flight 已标的坑）。
11. **不许提交脏树**；任务之间**另起提交**；**不许 `--amend`**。
12. ★ **不许**用"读-改-写写成一条表达式"的写法（先求值左边就截断 —— 清空过本仓一个 880 KB 的文件）。
13. ★★ **临时件只许落两处**：**仓内 `build/`** 或**一个固定名字的容器**；**绝对不许落在盘根**（`C:\` / `D:\` 直接下面）——
    本仓 2026-10-03 栽过（`D:\m3-t3-schematic\`）。**路径参数一律写 `D:/...` 形式；`cd` 之后先 `pwd` 核一次。**

## 派发指令必带（每次派 subagent 都要附）

- 任务书路径（本文件的那一节 + 该任务的 brief 文件）· 报告落点 `.superpowers/sdd/task-m1-topicselect-t<N>-report.md`（**必须真的落盘**）。
- Global Constraints 全文 · 基线 commit（派发前 `HEAD`，**不许用 `HEAD~1`**）。
- 明确：**只回报**状态 + 提交 + 一句话测试结论 + 顾虑；**不要把报告内容复制进回复**。

---

## 质检记录（**写计划时查出来的八处陷阱**，不是事后补的）

### P1 ★★ **本支有四处涟漪，四种处置各不相同 —— 别混成一件事做**
① `A9` 那一行的**两个数**（目录数 + grep 命中数）**同批改**；
② `mcm-playbook` 的 **5 处「未建」**（**`T3` 抓不到**）⇒ **必须改 + 登记**；
③ 7 份印"扫到 1N 个 skill"的捕获件 ⇒ **必须不改，只登记**；
④ ★★ `mcm-playbook` 证据件的**三文件 blob 自证**（`PLAYBOOK-evidence.md:21`）⇒ **必须同批重跑生成器**（Pre-Flight 查出，最易漏）。
★ **四种处置**：改 / 改+登记 / 只登记 / 重跑生成器。**混了任何一种，就是一处漏网的假话。**

### P2 ★★ **`T3` 的逻辑决定了"改完不会红"—— 但那是推断，必须实测**
`check-playbook.py` 的 `T3`：`if tok in existing: continue`（**名字存在就跳过**，不要求「未建」）。
⇒ 改完 5 处后 `check-playbook.py` **应当仍 5/5**。★ **这是推断**（本仓"计划里写死的行为口径落地前必须实测复算"）⇒ **Task 1 必须实跑确认**。

### P3 ★ **`S1` 的归一化复用是"由构造消除风险"，别退化成复制**
`tools/papers/taxonomy.py` 实测可导入且已有 `normalize_for_locate` / `normalize_quote`。
⇒ **import 它**；若因故不能 import 而被迫复制，**必须在两处各写一句互指**（否则两支会漂）。

### P4 ★★ **语料那套分类是"我们的标注"，不是官方**
`PROBLEM_TYPES.md` 的 `L1 · L2` 标签、`数据形态` 枚举、`模型配对`**全是我们自己标的**（其口径段自证）。
⇒ 凡引用必带"**我们的标注**"这句，**不许**写成"官方分类"。

### P5 ★ **`MODEL_MAP.md` 只有 2025 一年** ⇒ 任何"历史上这类题常用 X"的引用**必须带这句**。

### P6 ★ **"数据可信度"不能替用户判断** —— 只能给**候选来源 + 各自边界**；**不许**给出"这个源可信/不可信"的定论。

### P7 ★ **"拥挤风险"是四轴里最软的一条** ⇒ 推荐时**必须把它当软证据**，并在"推翻条件"里写明它可能整体偏。

### P8 ★ **RED 的靶子（`S1` 逐字性）是预期，不是保证** —— 写手若逐字抄了，**照实记**（那是真读数）。

---

## 文件结构（终态）

```
.claude/skills/mcm-topic-select/
├─ SKILL.md                     # 短契约：入口 · 时间盒 · 输出契约 · 指针（家族外，无 K2/K3 义务）
└─ references/
   ├─ method.md                 # 四轴证据档怎么填（含每轴的可核性）· 取舍规则 · 推翻条件 · 常见误判
   └─ corpus-lookup.md          # 语料怎么用 + **四条已知边界**（我们的标注 / MODEL_MAP 只 2025 / 六题不在语料里 / 场景与模型无关）

tests/skills/topic-select/
├─ check-topic-select.py        # 判据 S1–S6
├─ mutate-topic-select.py       # 变异驱动器
├─ make-evidence.py             # 对照证据生成器
├─ TOPICSELECT-evidence.md      # 由生成器产出
├─ red/ · green/                # RED / GREEN 对照
└─ README.md
```

**为什么没有 `assets/`**：它**不产图 / 表 / 代码**（产物是一份判断 + 依据），**不需要编译**（同 `mcm-playbook`）。

---

## Task 1：`SKILL.md` + 两份 references + **三处涟漪**

**产出**：`.claude/skills/mcm-topic-select/{SKILL.md, references/method.md, references/corpus-lookup.md}` ·
`docs/mcm-writing-discipline.md` 的两数同批 · **`mcm-playbook` 的 5 处「未建」同批** · 台账登记。

**硬要求**：

1. **`SKILL.md`（短契约）**：入口（贴六题）· **时间盒（≤2h + 何时可超时）** · 输出契约（每题分类 + 历史 + 四轴证据档 + 推荐 + **推翻条件**）·
   边界（**不查数据 / 不建模 / 不排赛程**）· 指针（两份 references）。★ **不复述** references 的数值。
2. **`references/method.md`**：
   - 四轴**逐轴**写：**它问什么 · 可核性（读数/半可核/判断）· 怎么填 · 常见误判**；
   - ★★ **第 3 轴写成"拥挤风险 = 判题面特征"**，并**明写"赛期内没有任何可靠办法知道某题的选题人数"**；
   - **禁令**：不许拿"历史获奖篇数"代理"选题人数"（**并说明它为什么不是空设**：语料就在盘上）；
   - **取舍规则 + 推翻条件 + 时间盒**。
3. **`references/corpus-lookup.md`**：
   - 怎么用 `PROBLEM_TYPES.md` 的词表/口径打 `数学任务 × 数据形态`（★ **标签必须附当天题面原句**）；
   - 四条边界（**我们的标注** / `MODEL_MAP` 只 2025 / 六题不在语料里 / **场景与模型选择无关** —— 语料口径 7 的用户裁决）。
4. ★★ **四处涟漪同批、各按各的处置**（GC2/GC3/GC4/GC4b）：
   ① `A9` 的两数**一次改到位**（含两段时点括注的追加）；
   ② `mcm-playbook` 的 5 处「未建」**改掉**；台账**登记"判据管不到的假话"这一类**（写明 `T3` 为什么抓不到）；
   ③ 7 份总 skill 数捕获件 **只登记、不重跑**；
   ④ ★★ **同批重跑** `python tests/skills/playbook/make-evidence.py`，并核三件：`:21` 的三个 blob **跟上了**、`:23` 的检查器自证**不变**、生成器**幂等**。
5. **未建的明写「未建」**：`mcm-paper-architecture` · `mcm-section-writer` · `mcm-memo`（本支**无** `T3` 那种判据守 ⇒ 靠自律 + 复核）。

**验收**：四轴**每轴带可核性标注** · **`check-writing-discipline.py` 的 `A9` 由红转绿** ·
**`check-playbook.py` 仍 5/5**（**实跑**）· `check-spec-pointers.py` 家族**仍 5 个** · 收工门全绿（**减掉本支两个尚不存在的脚本**）。
★ **本句原写"`SKILL.md` 里凡数值逐处能追到 references（不复述）" —— 那条已订正（2026-10-03 Task 1）**：
那是**绘图家族的规矩**（那边 `SKILL.md` 必须纯指针），**本支是家族外**（**无零数字约束**，同 `mcm-playbook` —— 它的 `SKILL.md` 就有 9 行带数字）。
⇒ **契约值（如时间盒 `≤2 小时`）本来就该写在 `SKILL.md`**；只需**同值只此一处或与 `method.md` 同值**（不造第二份权威），**不要求"零数值"**。

---

## Task 2：判据 `S1–S6` + 变异驱动器

**产出**：`tests/skills/topic-select/check-topic-select.py` · `tests/skills/topic-select/mutate-topic-select.py`。

**硬要求**：

1. **六条判据逐条落地**（设计 §3），**每条 fail-closed**：
   ★★ **`S1` 是心脏** —— 每个标签的支撑句**必须是当天题面的子串**，归一化**复用 `tools/papers/taxonomy.py`**（P3）。
   `S2` 历史读数**现取**比对 · `S3` 四轴齐备且**标明可核性**（判断型不许写成读数）· `S4` 推翻条件在位 ·
   `S5` 时间盒声明在位 · `S6` **禁令在位 + "赛期内不可回答"那句在位**。
2. **变异驱动器**：**每条判据至少一条变异** + **"必须仍绿"的射程边界对照**；**合计行不是末行**。
   ★ 六条必查：**改写一条支撑句** ⇒ `S1` 红 · **改一个历史数** ⇒ `S2` 红 · **判断标成读数** ⇒ `S3` 红 ·
   **删推翻条件** ⇒ `S4` 红 · **抹时间盒** ⇒ `S5` 红 · **把禁令改成"获奖论文多的题选的人少"** ⇒ `S6` 红。
2b. ★ **CLI 输入面（写死，别留给实现者猜）**：`check-topic-select.py` 至少要能接**三个路径** ——
   `--problems`（当天六道题的题面，**一个目录或一个文件**）· `--output`（本 skill 的产出）·
   `--corpus`（`corpus/papers/` 的根，可默认到仓内）。
   ★ **三者任一读不出 ⇒ fail-closed 红**（不许静默绿）；★ `--corpus` 默认值指向仓内，**但判据必须能指向别处**（否则没法做"读不出"的变异）。
3. **不许**为了凑数写恒真的检查；**判据只能从失败方向证明**。
4. **本支不动** `check-figure-style.py` / `check-spec-pointers.py` / `check-playbook.py` / 任何既有 `mutate-*.py`。

**验收**：六条在**已知好的产出**上全绿、在**变异体**上逐条真红 · `mutate-topic-select.py` 合计行全红 ·
**既有各支的门一个都没动且仍全绿**（含 `check-playbook.py` 5/5）。

---

## Task 3：RED / GREEN 对照与证据

**产出**：`tests/skills/topic-select/{red/**, green/**, make-evidence.py, TOPICSELECT-evidence.md, README.md}`。

**硬要求**：

1. **RED** = 三个**新起干净上下文、非 `fork`** 的写手，各拿**同一份 brief**（"**从这六道题里挑一道，并说明为什么**"）+
   **六份题面**；**不给**语料、**不给**规范、**不给**判据。**如实披露旁路**（skill 列表那行描述 + `MEMORY.md`）。
2. **GREEN** = 用本 skill 出**同一件事**的产出。
3. ★★ **靶子 = `S1` 的逐字性**（写手**大概会改写题面** ⇒ 支撑句不是子串 ⇒ 红）。
   ★ **但"预期" ≠ "保证"**（P8）：**写手若逐字抄了，照实记** —— **不许调 brief 去凑**。
   ★★ **订正（2026-10-03 · Task 3 实测：本条预测被推翻）**：三位写手**都没产出可比结构**（题小节/标签表/推荐行全 0）
   ⇒ `S1` 在**解析层**就 fail-closed 红，**没走到逐字那一格**；红集 `{S1,S2,S3,S4}` **全是 fail-closed 型**。
   ⇒ **RED 须按"中性形态"重跑**（shape-only 空壳：标签表/历史行/四轴/推荐的骨架，**不含逐字纪律**）——
   本仓先例 = `mcm-schematic` 的 RED 给写手"中性最小骨架"。**重跑落地前，"`S1` 抓改写"的证据只在变异驱动器里。**
4. **逐条点名红在哪**（哪条判据、什么读数、为什么），**并如实报性质**（真红 / 级联 / 假红已修）。
5. **两侧同一把尺**（同一个 `check-topic-select.py`）；对照表**机器抽取**。
6. ★ **RED 的诚实边界写进证据件**：brief 已限定"要挑一道并说明理由" ⇒ **测不到"连推荐都给不出"**。**不声称覆盖全部失败模式。**
7. ★ **「看一眼」层的替代品**（P6 同族）：无产物可看 ⇒ 把"推荐 + 依据"**拿给人读**，问"照这个你能定题吗"；**标明它是替代品**。
8. **判据清单现取**（先例：写死条数 ⇒ 汇总表静默归零）。

**验收**：RED 的红逐条点名并如实报性质 · GREEN 全绿（或**如实**说明哪条不绿及原因）· 对照表机器抽取 ·
诚实边界在 · 替代品性质标明 · 收工门全绿。

---

## Task 4：全库收口

**产出**：`docs/` 过期散文订正 · 残留两层分类 · §H 计数联动 · **`§H.2.2` 两类的复核**。

**硬要求**：

1. `docs/` 里凡**以现在时**写死旧读数的散文 ⇒ 改现值；**自带复核命令的声明必须复跑那条命令**。
   ⚠️ **不许把"（该轮当时…；今天 = X）"的时点标注改成现值**（那是抹掉历史）。
2. **残留两层分类**（机械层：**去重并集 == 表行数**，两个数都写；判断层：逐行类别 + 理由 + **复核命令**）；
   **不许写"全库残留 = 0"**；**不声称穷尽**。
3. **§H 计数联动**：若新增/移除印着现变异合计的捕获件 ⇒ **同批**改 §H.1.1 / §H.5.3。
4. ★ **复核 §H.2.2 的两类**：**家族成员计数**（不变）· **总 skill 数**（**再变一次** ⇒ 按已定口径只登记、不重跑）。
   ★ 并**复核 Task 1 登记的那条**："判据管不到的假话（`T3` 见名字存在就跳过）"。
5. **逐条判本支与上游登记的待办**：能清的清掉、范围外的**写明归谁**。
6. ★ **登记"本支是家族外第二个"** —— 与 `mcm-playbook` 那条并列。

**验收**：逐处订正表 · 残留两层（两个数相等）· §H 计数自洽 · 两类复核实跑 · 收工门全绿。

---

## 设计 §7 那七条已知缺口的归宿（**逐条给去处，不许悬空**）

| # | 缺口 | 归宿 |
| :-- | :--- | :--- |
| 1 | ★★ **"拥挤风险"无数据、赛期内不可回答** | **Task 1 硬要求 2**（写进 `method.md` 的明写 + 禁令）· **Task 2 的 `S6`** 守 · 并**在推荐里当软证据**（`S4` 的推翻条件） |
| 2 | **`MODEL_MAP` 只有 2025** | **Task 1 硬要求 3**（`corpus-lookup.md` 的边界四之一） |
| 3 | **数据可信度不能替你判断** | **Task 1 硬要求 2**（`method.md` 写明"只给候选来源 + 各自边界"） |
| 4 | **六题不在语料里** | **Task 1 硬要求 3**（边界之一） |
| 5 | **时间盒是默认、可覆盖** | **Task 1 硬要求 1**（`SKILL.md` 写明可覆盖） |
| 6 | **推荐仍是判断** | **Task 1 硬要求 2**（"工具保证依据可核，不保证推荐对"） |
| 7 | **网页端 / 跨机不适用** | **是结论不是未验** ⇒ 写进设计的边界；**不占任务** |

⇒ **本计划不新增第 5 类任务**：上面 2–7 都是**文档内登记**，由 Task 1 一次写完。

---

## 结束条件

四个任务全绿后，派**全分支终审**（范围 = 本模块基线到 `HEAD` 的全部提交；**重点查接缝**：
**`S1` 是否真的复用了语料的归一化**（P3）· **三处涟漪是否各归各位**（改两处、不改一处，P1）·
**"拥挤风险"那一轴有没有被写成读数**（本支头号风险）· **`mcm-playbook` 的「未建」是否真改净** ·
**家族正则没被顺手改** · 给下游留没留绊脚石），
按结果修复或收口 ⇒ 台账 + §H + 记忆 + **推送**（仓外 worktree 配方；**推送是对外不可逆动作 ⇒ 先比 blob sha 与快进性，
并在推送前向用户交底**；★ **路径一律写 `D:/...`，`cd` 后先 `pwd`**，见 GC13）。

> ★ **本轮预告：`mcm-topic-select` 是家族外第二个 skill** —— 它不进绘图家族、**不改家族计数**；
> 但它会**第二次**推高"总 skill 数"，并**销掉 `mcm-playbook` 的 5 处「未建」**（那是已出货产物里的悬空指针）。
