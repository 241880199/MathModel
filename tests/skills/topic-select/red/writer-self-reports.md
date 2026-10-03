# Task 3 RED 基线的派发口径与写手自述（`mcm-topic-select`）

★ 本文件含**两轮** RED 的派发口径与自述：**§0–§4 = 第一轮（无形态）**；**§5 = 第二轮（有中性形态）**。

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何「写手」agent 读过本文件，产出的就不再是 RED 基线。
> 与它同案看待的还有本目录的 `README.md` 与上一级的 `TOPICSELECT-evidence.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是「写手到底读到了什么」：它只能靠**审计写手的自报**。

【来源 —— 照实记】本会话 subagent 的 `.output` 不可靠（先例：`plot-python` 那支实测 0 字节）⇒ 本文件的
提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**（写手回给调度者那段），
**不是**从 transcript 文件里机器摘的 ⇒ **没有**机器可复核的「逐字节」保证，只有**转录级**的忠实度声明。

【对原文的唯一加工】写手自述里写了**绝对路径** ⇒ 掩码之：`D:/Projects/数学建模/build/topic-select-red`
→ `<WS>/topic-select-red`。除此之外**逐字未改**。

【强度声明】「写手是否真的只读了那一份 brief 与六份题面」**只有自报、没有沙箱可证**（另外：**未用 `fork`**——
三个写手都是新起的干净上下文 `general-purpose` agent，首条 user 消息就是下面那条提示词本身）。
**自报一致 ≠ 已证**。

---

## 0. 派发口径（三个写手逐字同一份提示词，只换输出目录）

```text
Read the brief at <WS>/topic-select-red/brief.md and produce the deliverable it asks for. The six problem
statements it refers to are in <WS>/topic-select-red/problems/ (A.md, B.md, C.md, D.md, E.md, F.md). Write your
deliverable into <WS>/topic-select-red/out-R{n}/. Work only from that brief file and those six problem files -
do not read or write any other file.

Environment fact (not part of the brief): you do not need network access; work offline from your own knowledge
and judgement.

When you are done, reply with a short self-report: which files you read, what you produced (file names and
sizes), why you chose the problem you chose, and any issues you hit.
```

（实际派发时是**绝对 Windows 路径** `D:\Projects\数学建模\build\topic-select-red\...`；上面是掩码后的等价写法。
三个写手之间**只有 `out-R{n}` 这一个 token 不同**。）

**给写手的那份 brief 是**仓内权威件 `tests/skills/topic-select/red/brief.md` 的**副本**，派发前**逐字节比对**过（当场跑过）：

```text
$ python -c "import pathlib; a=pathlib.Path('tests/skills/topic-select/red/brief.md').read_bytes(); b=pathlib.Path('build/topic-select-red/brief.md').read_bytes(); print('brief identical:', a==b, '| bytes:', len(a))"
brief identical: True | bytes: 679
```

⇒ 写手拿到的 brief **就是我们入库的那一份**（`read_bytes()` 直接比，不经 blob）。

### 0.1 为什么 brief 里**没有**形态要求、**没有**来源 —— 中立性抉择（硬要求 1）

- **没有形态要求。** brief **只问**「从这六道题里挑一道，并说明为什么」——**不提**「分类」「同型历史」
  「四轴证据档」「推翻条件」「表格」这些**本 skill 契约里的词**。理由：一旦提了，写手就会**照着契约的形态**
  去凑，RED 就不再是"没受过本 skill 约束"的基线。
- **没有来源。** 不给本 skill、不给语料、不给判据、不给本任务书。
- ★ **brief 里唯一算"限定"的一句是**「从这六道题里挑一道，并说明为什么」**（必答项：挑一道 + 理由）。
  ★ **这条限定本身就是 RED 的诚实边界**（硬要求 6）：它保证了写手**一定给得出一个选择** ⇒
  这轮 RED **测不到"连推荐都给不出"那一类失败**。**不声称覆盖全部失败模式。**

---

## 1. R1 写手自述（原文，掩码后）

```text
## 自述报告

**读了哪些文件**（严格限定在指定范围内，未读/未写任何其他文件）
- `<WS>/topic-select-red/brief.md`
- `<WS>/topic-select-red/problems/A.md`、`B.md`、`C.md`、`D.md`、`E.md`、`F.md`

**产出了什么**
- `<WS>/topic-select-red/out-R1/decision.md` —— 18,537 字节 / 164 行，中文 markdown。
- 结构：§0 一页结论 → §1 四轴判据（数据 / 建模 / 交付 / 风险，各 1–5 分）→ §2 六题逐题档案（题族分类 · 题面诉求 · 数据 · 建模主线 · 主要坑 · 2016–2026 同型历史 · 四轴评级）→ §3 横向对比表 → §4 推荐理由并正面回应反对意见 → §5 带量化信号的推翻条件 → §6 若选 C 的头两小时落点 → §7 诚实清单。

**为什么这么挑**
- 推荐 **C 题（Olympic Medal Tables）**，得分 19/20，理由六条：唯一"给数据且数据干净（5 个 CSV + 数据字典）"；建模主线成熟且**可回测自证**；6 个子问可切块保底（部分解被接受）；不确定性是题面硬要求＝天然区分度；无强制 memo/letter、交付最轻；产出大量数值结果契合写作/绘图工具链。
- 排序 C(19) ≻ D(13) ≻ B≈A(12) ≻ E(10) ≻ F(7)。F 数据轴 1、风险轴 1，最易写成空谈，明确不推荐。
- 推荐**带推翻条件**：队伍熟 GIS/图算法→改选 D；偏爱优化+会写 memo→改选 B；物理强→A；生态动力学→E；政策文献整合强→F；并给了开赛后 2–3 小时的量化切换信号（3 小时内跑不出可回测基线即考虑切 D 或退 B）。

**拿不准的地方 / 遇到的问题**
1. 题面**未给队伍画像**（人数、专业、技能），结论建立在"统计/编程中等偏上、自编译 LaTeX 的典型队伍"这一显式假设上，已用 §5 的翻转条件补偿。
2. **未真正读到数据文件**：fixture 里只有六份 `.md` 题面，C/D 声称的数据包不在目录中；对"数据干净/脏"的判断来自题面自述，未核实。
3. **2016–2026 同型历史来自离线记忆**，未联网、未逐条核对，年度-题目归属可能有误，已在文中标注"不声称穷尽"，只用于判断题型是否反复出现；2026 年题面不在给定范围，未纳入。
4. 四轴打分与权重是主观判断，未做权重敏感性；若把"差异化空间"单列加重，D 可能反超 C。
5. "名帅效应"是因果问题、观测数据难识别，已列为 C 的主要坑；若评委对此要求极高，C 的优势会削弱。
6. 环境事实（离线）已遵守：全程未联网，仅凭题面与自身判断完成。
```

## 2. R2 写手自述（原文，掩码后）

```text
Done. Deliverable produced as asked.

Files read (only these, per the brief's constraint):
- `<WS>/topic-select-red/brief.md`
- `<WS>/topic-select-red/problems/A.md, B.md, C.md, D.md, E.md, F.md`

Produced:
- `<WS>/topic-select-red/out-R2/decision.md` — 12,551 bytes, 160 lines, written in Chinese.

What it contains: a recommendation of Problem C (Olympic Medal Tables) with confidence stated as 中高; a per-problem classification table (track, problem type, whether official data is supplied, extra deliverable); the five axes I judged on (data, modeling depth, verifiability, anti-stuck risk, ceiling); a scored comparison table giving C=23, D=20, A=15, B=15, E=14, F=11; a detailed four-part case for C; the strongest alternative (D) and the signals that would flip the choice; explicit falsifying conditions / swap rules; a first-6-hours checklist; and an honest uncertainty list.

Why C: it is one of only two problems (with D) that ships an official dataset, and its data is clean, structured, spans 1896–2024, and points at a single backtestable, interval-reportable, falsifiable target (LA 2028 predictions). It has four layers of modeling depth that map onto three teammates (main count model, host/event effects, rare-event first-medal prediction, the named "great coach" causal question), and it — like A — carries no memo/letter deliverable burden, so the page budget goes to modeling. D is the real rival and wins if the team has strong GIS/network skills.

Issues / caveats hit:
- The brief gave no team profile, so I stated an assumed team (3 people, Python/R-strong, one statistics/modeling specialist, no domain expert, ~4 days) up front and made the whole recommendation conditional on it — that assumption is the single largest uncertainty in the document.
- The brief forbids reading anything but itself and the six problems, so I deliberately made no year-specific claims about past MCM/ICM problems; the classification is at the family level only (MCM-A continuous/mechanistic, MCM-C data analysis, ICM-D network/OR, ICM-E environment, ICM-F policy), and I flagged this.
- The C data files themselves are not in scope to read, so the field-level details and a small "first 6 hours" checklist are based on the problem statement's descriptions and are flagged as needing verification against the real data.
- No environment problems; no network needed; output directory out-R2/ was created.
```

## 3. R3 写手自述（原文，掩码后）

```text
## 完成

**读了哪些文件**（仅此 7 份，未碰其他文件）：
- `<WS>/topic-select-red/brief.md`
- `<WS>/topic-select-red/problems/A.md` ~ `F.md`（六份题面）

**产出了什么**：
- `<WS>/topic-select-red/out-R3/decision.md` —— 10,691 字节（约 10.4 KB），中文。

**内容结构**：先给结论 → 六题速览表 → 四轴评分表 → 选它的五条理由 → 诚实的顾虑 → 带推翻条件的决策规则表 → 头 24 小时落地清单 → 不确定之处。

**为什么选 Problem C（Models for Olympic Medal Tables）**：
核心理由是**数据风险**。六题里只有 C 和 D 的必需数据是随题给全的（C 是 5 个 CSV，1896–2024 全量；D 是 9 个 GIS/公交文件）；而 C 的执行门槛（pandas 表格统计）远低于 D（GIS/osmnx 地理网络，工具链翻车即全盘皆输）。A/B/E/F 都要赛中自行凑数据，而赛中最贵的就是时间。
在选定 C/D 这组"有数据"的题后，C 再因三点胜出：任务边界清晰（三个明确 bullet 可直接拆章节）、题面**硬性要求预测区间与不确定性量化**（天花板没被牺牲，但也因此最考验队伍）、工具链普通。
我按"最坏情况最好"原则选，C 的下限是"平庸但完整"，D 的下限是"数据用不了"——信息不全时选下限高的。

**关键判断/取舍**：
- 我明确论证了"选 C 的人最多"对**获奖概率近乎中性**（奖项按题池比例分配），因此没把拥挤度当独立轴压分。
- 诚实列出 C 的三大顾虑，并把"名帅效应"标为**因果推断陷阱**，建议降级为"描述性观察 + 反事实讨论 + 局限声明"，不要硬做因果结论。
- 因**队伍构成未知**，我给的是"带推翻条件的推荐"：附一张决策规则表（无数据处理能力→E；OR/GIS 强→D；ODE/生态强→E；物理强且愿押高方差→A；F 不建议）。

**遇到的问题/拿不准的地方**：
- 我**没有数据包**，只能依据题面对数据清单的描述（文件名、年份范围、字段）判定 C/D"数据确定性满格"，未核验过实际 CSV 质量。
- 题面未给队伍构成，这是本决策最大的不确定源；文档第 7 节已如实说明，并指出若补上强项信息可给出唯一确定答案。
- "奖项按题池等比例分配"是常识性假设而非题面事实，若被推翻则需重估 C 的相对优势。已在文中标注。
```

---

## 4. ★ 环境旁路的如实披露（照先例的强度写，不许省）

「只给一份 brief ＋ 六份题面」说的是**派发那一刻的 user 消息**；但写手是本机 Claude Code 的 agent，
**会话级共享上下文里另有两处本任务删不掉的可见面**：

1. **可用 skill 列表里 `mcm-topic-select` 的那一行描述**（harness 自动注入给每个 agent）——
   它写着本 skill 是「贴当天六道题的题面，要一份「**每题按语料口径的分类 + 2016–2026 同型历史 +
   四轴证据档 + 一个带推翻条件的推荐**」」。
   ★★ **这一次旁路是"实打实泄漏了形态的粗粒度"**（不像 `mcm-playbook` 那支旁路没泄漏时长）：
   它**点了名**"分类 / 同型历史 / 四轴 / 推翻条件"这四个契约要素。
2. **项目记忆 `MEMORY.md`**（自动注入）及若干记忆条目（如 `mcm-skill-suite-project.md`，提到本套件的 skill 清单）。

### 4.1 ★ 旁路**泄漏了什么、没泄漏什么** —— 当场用探针查了

派了一个**干净上下文 `general-purpose`** 探针，**明确不读任何文件**，只问它"你启动上下文里关于 `mcm-topic-select`
能看到什么"。探针回报（转录，非机器抽取）：

> Yes — `mcm-topic-select` does appear in the startup context, but only as a one-line skill-listing entry plus
> incidental git metadata. Nothing in the memory files or global instructions describes it.
>
> **1. The skill-listing entry (verbatim)**
>
> ```
> mcm-topic-select: Use when 美赛 MCM/ICM 开赛后要从六道题里挑一道、并说清“为什么是它”——贴当天六道题的题面，要一份「每题按语料口径的分类 + 2016–2026 同型历史 + 四轴证据档 + 一个带推翻条件的推荐」时。Triggers include 选题、选题决策、选哪道题、挑题、定题、哪题好做、第一小时干什么、六题怎么选、topic select、which problem、pick a problem、choose the problem。
> ```
>
> (…only this description line; no separate `mcm-topic-select` documentation, SKILL.md body, or reference text is injected.)
>
> **2. Other startup-context text touching topic selection / problem-choosing**
>
> **a) gitStatus block**（探针当时看到，逐字）：`M .claude/skills/mcm-topic-select/references/method.md` ·
> `?? tests/skills/topic-select/make-evidence.py` · `?? tests/skills/topic-select/red/`
> （另有 `Current branch: feat/m6-corpus-pipeline` 等）。
> **b) Recent commits**（探针当时看到的五条，逐字）：
>
> ```
> 5cf6ed2 docs(m1-topic-select): 修复轮订正 —— §5 题标题行那句措辞说准
> 093b8fd fix(m1-topic-select): Task 2 修复轮 —— 形态权威搬进 skill + 两处 Minor
> 4cdfb20 test(m1-topic-select): Task 2 —— 判据 S1–S6 + 变异驱动器 + 两处 Minor 并办
> d58f29a docs(m1-topic-select): 计划订正 —— Task 1 验收句把绘图家族的『零数值』规矩误套到家族外 skill 上（控制者第十次同类错）
> 384e2df feat(m1-topic-select): Task 1 —— SKILL.md + 两份 references + 四处涟漪（各按各的处置）
> ```
>
> **3. What is NOT in the startup context**: the auto-memory index does **not** mention `mcm-topic-select`;
> the global `CLAUDE.md` has no topic-selection content; no SKILL.md body / reference text is injected.
> ★ **在本会话里，启动上下文能看到 5 条 Recent commits，且条条是 `m1-topic-select`** ⇒
> 写手的 gitStatus 块**大概率**也带了这几行（同 harness）。这一点**照实登记**：旁路**也漏了"这支 skill 有一个
> 判据 `S1–S6` + 变异驱动器"这件事**（commit `4cdfb20` 的标题）。
>
> **结论（照实）**：旁路**泄漏了**三样 —— ①本 skill 存在、且其产出含 分类/同型历史/四轴/推翻条件；
> ②工作树里有 `mcm-topic-select/references/method.md` 与 `tests/skills/topic-select/`；
> ③最近五次提交都在做 `m1-topic-select`、且提到了「判据 `S1–S6` + 变异驱动器」。
> 这从三位写手的产物里**看得到**（R1 用了「四轴」；R1/R2/R3 都写了「推翻条件」）。
>
> ★ **探针自身的不确定**：探针**不知道自己启动时 Recent commits 里是哪几条**（它只报"当时看到的"）——
> 它跑得比写手晚（我那时已多出 `make-evidence.py` 与 `red/` 两项未跟踪件）⇒ 写手当时看到的 gitStatus
> **未必逐字等于**探针上面那一段。**这条差异照实登记，不假装写手与探针看到的是同一份快照。**
★ **但它没泄漏本 skill 真正承重的那一层**：**逐字形态**（`## 题 <字母>` 小节 · 标签表 · `- 历史：…` 两行 ·
`- 轴 N · …【可核性】` 四行 · `## 推荐` 两行）、**判据**、**语料那套词表与口径**、**归一化规则**。
**证据**：三位写手**没有一位**产出 `## 题 <字母>` 小节或 `## 推荐` 小节（见 §5 结构探针）⇒ 检查器的
`S1`–`S4` 全部 fail-closed。旁路把"要做哪几样"漏了出去，**没把"每一样逐字长什么样"漏出去**。

★★ **反过来的一条必须写死**：**旁路的存在使本轮 RED 不是"完全没见过本 skill"的基线** ——
它见过本 skill 的**描述行**。**登记在案**：下一次复用此配方时，要么接受这条旁路（如本轮）、
要么在有条件时把 skill 列表也隔离掉（本机 harness 做不到）。

**探针自身的边界（不声称它是机器证据）**：它是**单个 agent 的自我报告**，不是对上下文的机器检查；
且问的问题本身**带指向性** ⇒ 它只能说明"探针在上下文里看到了/没看到那些字"，
**不能证明"上下文里绝对没有塞进别的东西"**。

---

## 5. 第二轮（有中性形态）—— 派发口径与三份自述

★ **第二轮与第一轮的唯一变量** = **多给一份 `neutral-shape.md`**（仓内权威件 `../neutral-shape.md` 的副本）。
`brief.md` 逐字同一份、六份题面同一份、判据同一版。

### 5.0 派发口径（三个写手逐字同一份提示词，只换输出目录）

```text
Read the brief at <WS>/brief.md, the six problem statements in <WS>/problems/ (A.md, B.md, C.md, D.md, E.md, F.md), and the neutral shape (an empty shell) at <WS>/neutral-shape.md. Produce the deliverable the brief asks for, using that neutral shape as the shape for your document. Write your deliverable into <WS>/out-R{n}/. Work only from that brief file, those six problem files, and that neutral-shape file - do not read or write any other file.

Environment fact (not part of the brief): you do not need network access; work offline from your own knowledge and judgement.

When you are done, reply with a short self-report: which files you read, what you produced (file names and sizes), why you chose the problem you chose, and any issues you hit.
```

（实际派发时是**绝对 Windows 路径** `<WS>` = 仓内 `build/topic-select-red2/`（gitignore）；上面是掩码后的等价写法。
三个写手之间**只有 `out-R{n}` 这一个 token 不同**。三份自述的**来源与强度限制同 §4 文首**：**转录级**、非机器摘。）

**给写手的三份件是**仓内权威件的**副本**，派发前**逐字节比对**过（当场跑过）：

```text
$ python -c "import pathlib; ... 逐件 read_bytes() 相比 ..."
brief.md True (679) · neutral-shape.md True (954)
problems/A.md True (5683) · B.md True (6198) · C.md True (9117) · D.md True (12578) · E.md True (9332) · F.md True (6845)
ALL IDENTICAL True
```

⇒ 写手拿到的 brief / 题面 / 中性形态**就是我们入库的那三份**（`read_bytes()` 直接比，不经 blob）。

### 5.1 R1 写手自述（原文，掩码后）

```text
## 自述报告

**读了哪些文件（仅此 8 个，未读写其他文件）**
- `<WS>/brief.md`
- `<WS>/problems/A.md` – `F.md`（6 份）
- `<WS>/neutral-shape.md`

**产出了什么**
- `<WS>/out-R1/decision.md`，**11,261 字节**（GBK/UTF-8 中文，约 11 KB）。
- 严格按中性形态的壳子落地：每题一节 `## 题 <字母> — <题干词>`（A 磨损反演 / B 可持续旅游 / C 奖牌预测 / D 交通网络 / E 农田食物网 / F 网络安全政策），每节含 `核心`/`附带` 的 L1·L2 表 + 支撑句、两条「历史」行、四条「轴 n · 轴名【可核：高/中/低】」行；末尾一个 `## 推荐` 节，含**推荐**与**推翻条件**。
- 我自建并贯通使用了一套两级分类（L1 建模范式 / L2 模型族）与三值数据形态枚举 `D0 无官方数据 / D1 官方结构化数据集 / D2 多源半结构化`；四根轴在所有六题上同名同序（数据可得性、建模核清晰度/方法成熟度、区分度 vs 拥挤度、交付负担与翻车风险），以保证横向可比。

**为什么这么挑（推荐题 A）**
- 六题逐一打分后，A（Testing Time: 台阶磨损）四项最均衡且风险归己方可控：数据风险最低（无外部数据依赖，且「非破坏、低成本、小团队」的测量方案本身就是交付物）、建模天花板最高（磨损剖面→人流频次/方向/并行人数是真正的反问题，而非套回归）、拥挤度低于 C（C 题基线解扎堆），交付面最干净（无 memo、无数据集清洗）。
- C 的「稳」是拿拥挤度换的，D 的「强」是拿 GIS 清洗的翻车风险换的，故列 C、D 为条件性替代。
- **推翻条件**写死四条：队伍无 ODE/反问题功底→改 C；强在 GIS/网络→改 D；量化弱写作强→改 B 或 F；开赛 2–3 小时仍立不起磨损反演核心假设→切 C 止损。

**拿不准 / 需注意的问题**
1. **历史计数是软肋**：中性形态要求填 N（出现次数、篇数），但环境说明要求离线、不联网，我无法对 2016–2025 语料做普查。N 全部是我凭记忆的估计，我已在文首与文末**显式声明「不声称穷尽、须回语料复核」**，未假装是精确普查值——这也符合用户「声明必须能被一条命令一秒推翻」的纪律。
2. **「N 篇」的口径**：壳子写「<N> 篇」，我按「同族题数」理解并写成「合计约 N 题」，因为离线无从得到论文篇数；若原意是论文篇数，需改口径。
3. **题干词与 L1/L2 命名是我自定义的**：壳子未给词表，六题的分类词条由我拟定；不同顾问会给不同词条，但四轴与两行的结构已严格对齐。
4. 我按「多源半结构化」把 D 归为 D2（GIS/OSM+公交+AADT 混合），C 归 D1；这一归类是可复核的判断，已在文中标注依据。
5. 未使用通知管道（无阻塞、无越权、无可逆动作），未触碰授权外的任何文件。
```

### 5.2 R2 写手自述（原文，掩码后）

```text
已完成，产出 1 个文件。

**读到的文件**（严格限定在任务允许范围内，未读写其他任何文件）：
- `<WS>/brief.md`
- `<WS>/problems/A.md` – `F.md`（六份 2025 MCM/ICM 题面）
- `<WS>/neutral-shape.md`

**产出**：
- `<WS>/out-R2/decision.md`（11,523 字节，约 115 行）

**文档形态**：严格照中性形态——先一段「口径与声明」（把形态里未定义的 L1/L2、数据形态、可核性、历史计数口径钉死），再对六道题**各写一节**（每节含：核心/附带 的 `L1 · L2` 表 + 两条历史行 + 轴 1–4 带【可核性】），最后收在「推荐」节（推荐 + 推翻条件）。

**为什么挑 C（奥运奖牌表）**：它是六题里唯一同时满足三条稀缺条件的——(1) 数据封闭全给（五份 csv，1896–2024 + 2028 programme），解可完全复现、零外部采集风险；(2) 子问分层、给分点最密（预测区间、首金概率、项目-奖牌关系、名帅效应、原创洞见）；(3) 明写不确定性要求，能挡住"拍脑袋"。备选给出 D（数据清洗/网络强）与 E（规避红海、机理强）。推翻条件写了 4 条（含"C 题实际未给全数据 → 改选 D"，这是能被一条命令一秒推翻的那类）。

**拿不准 / 已显式标注的问题**：
1. **历史计数无依据可核**——形态要求「组合 × 数据形态，出现 N 次」「题 YYYY 字母 用过模型，N 篇」这类语料统计量，但本次输入只有六份题面、无任何历史语料。我没有编造精确数，而是：给自有知识下的近似值 + 一律标 `自报·未核` + 明写"不声称穷尽/精确"，并给出把它变可核的**测量协议**（在 2016–2026 全集中按同口径检索计数）。题号锚点（2021 A、2023 C、2023 D、2019 A、2021 D、2023 F）同标未核。
2. **L1/L2、数据形态、可核性三套枚举在 brief/neither 中都未定义**，形态只留 `<…>` 占位。我自定了一套自洽枚举并在开头声明，各节口径统一；若上游有既定词表，需替换。
3. **轴 4（同型密集度/红海-蓝海）标为【不可核】**——无投稿分布语料，只能给方向性判断。
4. C/D 题的"数据全给"结论按题面文本判定（即"题面语料口径下"），因本次未获实际数据文件，已在正文注明该限定。
```

### 5.3 R3 写手自述（原文，掩码后）

```text
Done.

**Files read (7, all within the permitted set):**
- `<WS>/brief.md`
- `<WS>/neutral-shape.md`
- `<WS>/problems/A.md` … `F.md` (six files)

No other file was read or written.

**Produced:**
- `<WS>/out-R3/decision.md` — 10,725 bytes, 99 lines.

**What it contains:** The document follows the neutral shape exactly. After a short 口径 preamble (L1/L2 taxonomy, the 4-value 数据形态 enumeration, the three 可核性 tags, and an honesty note), it has six per-problem sections `## 题 A` … `## 题 F`, each with the shape's `核心`/`附带` L1·L2 table + supporting sentence, the two 历史 lines, and the four axes tagged 【可核】/【半可核】/【不可核】. It closes with `## 推荐` (`推荐` + `推翻条件`).

**Why I chose C (Olympic medal tables):** It is the only problem that both ships its data with the题面 and forbids using outside data, so data risk is lowest; its deliverables (point forecast + prediction intervals + first-medal odds) are checkable and hard to write empty; and its sub-questions still leave differentiation room (event structure, host effect, coach effect, first-medal countries), with the riskiest sub-question allowed to be a partial solution. D named as runner-up (also data-attached, higher ceiling, higher GIS risk).

**Issues hit (important):**
1. The shape demands two "history" lines (a `L1·L2 × 数据形态` occurrence count N, and a `题 YYYY 字母 used-model N 篇` line), but the brief/inputs contain no corpus and no network access was allowed. I could not verify any of these. Rather than fabricate precision, I filled the slots with memory-based estimates and tagged every one "记忆估计·未核", added a global honesty declaration that the counts are unverifiable/not claimed exhaustive, and flagged that the year/letter itself may be misremembered. For F I explicitly labeled the cited historical analogue as a cross-domain analogy.
2. The neutral shape does not define L1/L2, the 数据形态 enumeration values, or the 可核性 tags. I had to invent a self-consistent taxonomy and state it up front; the shape alone does not pin these down.
3. I added a short 口径 preamble, which is one block not present in the shell — the brief grants freedom to add explanation, and without it the L1·L2 / 可核性 values would be uninterpretable. If strict shape fidelity with zero added blocks is required, this preamble is the one deviation to remove.
4. `out-R3` did not exist; I created the directory, then wrote only `decision.md` into it.
```

### 5.4 ★ 环境旁路的如实披露（第二轮；比第一轮更重）

「只给三份件」说的是**派发那一刻的 user 消息**；但写手是本机 Claude Code 的 agent，
**会话级共享上下文里另有三处删不掉的可见面**（与 §4 同型，**本轮更重**）。本轮**另起了一个干净上下文探针**当场读过（不读任何文件），读数如下：

1. **可用 skill 列表里 `mcm-topic-select` 那一行的描述**（harness 自动注入）—— 探针逐字报的就是本 skill
   `description` 那一行，与 §4 探针所见**同一段**：点名了「分类 / 2016–2026 同型历史 / 四轴证据档 / 一个带推翻条件的推荐」。
2. **`git status` 快照**（含 `.claude/skills/mcm-topic-select/references/{corpus-lookup,method}.md` 等路径）。
3. ★ **Recent commits（本轮比第一轮多两条）**：探针看到的五条逐字如下 ——
   `49c4fad`（控制者订正 · §3.2 RED 预测被推翻）· `9b254c8`（**标题点名「判据 `S1–S6` + 变异驱动器」**）·
   `5cf6ed2` · `093b8fd` · `4cdfb20`（**标题点名「判据 `S1–S6` + 变异驱动器」**）。

★ **探针自身的一条不确定（照实登记，不假装精确）**：探针跑在**本轮的后期**（工作树**已经脏**：`gitStatus` 里带着本轮改动的
`M/??` 若干项）⇒ 它看到的 `gitStatus` **不等于**写手当时看到的（写手跑在 `49c4fad` 的**干净树**上）。
**可信的推断**是：写手的 **Recent commits 与探针一致**（同 HEAD `49c4fad`、工作树干净），
而 **`gitStatus` 与探针不同**（写手时干净）。**这条差异照实登记。**

★ **旁路泄漏了什么、没泄漏什么**：泄漏的是**「有分类 / 历史 / 四轴 / 推翻条件这几样」+「本支有一个判据 `S1–S6` + 变异驱动器」**；
**没泄漏**的是**逐字形态与逐字纪律**（`## 题 <字母>` 的**具体正则**、`- 历史：…` 的**逐字行形**、
四轴的**轴名关键词与可核性枚举**、`- 推荐：` 的行形、**「支撑句必须是当天题面子串」这条纪律**、归一化口径）。
**证据（机器抽取，见 `../TOPICSELECT-evidence.md` §3、§6.2）**：三位写手**都没把轴名/可核性写对**
（`方法成熟度`/`区分度上限`/`可核：高`…）、**都没把 `- 历史：` 行写成可解析形态**（`出现约 N 次`/`≈N 次`）
⇒ 他们**不知道**判据真正读的形态与口径。

★★ **必须写死的一条**：**旁路的存在使两轮 RED 都不是"完全没见过本 skill"的基线** —— 它见过**描述行**。
两轮**都登记在案**；下一次复用此配方时要么接受这条旁路（如本轮），要么在有条件时把 skill 列表也隔离掉（本机 harness 做不到）。
**探针自身的边界同 §4**：它是单个 agent 的自我报告，不是对上下文的机器检查。
