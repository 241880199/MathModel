# M3 跨载体样式单源 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把"设计半 / 实现半"之间缺的那层补上 —— 一份**可被机器复算的载体无关样式表**，让"跨载体一致性"从纪律约定变成结构上可见、可被一条命令核的东西。

**Architecture:** 规范（`house-style.md`）补三条（§0 底色前提 / 新 H14 显式色序 / H12 默认值）⇒ 一个**重放式生成器**把它投影成 `mcm-style.json`（每格带条目号 / 值 / 来源性质 / 各载体落地状态）⇒ 各载体生成器**只读它、各自映射**（python 改造、matlab 待建、origin 契约写死）⇒ **判据加在共享的 `check-figure-style.py` 上**（底色 / 显式色序 / 字体族），载体无关。

**Tech Stack:** Python 3.11.9 · pytest 风格的仓内自检脚本（本项目实际用「可复跑脚本 + 逐字转录」而非 pytest）· `fitz`/`Pillow`（读产物）· `git hash-object`（判字节）

## Global Constraints

逐条从设计件 `docs/superpowers/specs/2026-09-30-m3-style-single-source-design.md` 抄来，**每个任务都隐含包含本节**：

1. **一致性目标 = 同规范 / 按族等价**，**不追求逐字同值**（design §1.1）。
2. **单源 = 共享派生件**：一份载体无关样式表，各载体生成器**只读它**；**matlab 不许另起一份抽取**（§1.2）。
3. **表放设计半**：`.claude/skills/mcm-figure-choose/assets/mcm-style.json`；生成器与守卫放 `tests/skills/figure-choose/`（§1.3、§5.5）。
4. **全收规范条目逐格标落地状态**；**H11（网格/图例/双 Y 轴）无论如何不进表**（§1.4）。
5. **色序新开 H14，不改 H5**；H14 来源标〔交付形态/口径〕、**不是**样本读数（§1.5、§4.2）。
6. **表里不许出现无主的数**：每个值必须能追到规范某条；追不到的**先补进规范**（§1.6、§5.2）。
7. **背景判据落进共享的 `check-figure-style.py`**，python 一起盖（§1.7）。
8. **三种来源不许混标**：① 实测分布 / ② 社区值 / ③ 交付形态（§4.4）。
9. **阈值不许拍脑袋**：背景"白"的阈值必须**由实测两端标定**并在计划里写明是量出来的（§7.1）。
10. **★ 硬纪律（本项目既有）**：所有 Python 写入一律 `write_bytes`（**禁 `write_text`**，Windows 会写 CRLF）；判字节用 `git hash-object`；**凡"证据件记录自身所在工作树状态"的生成器，必须"先干净 → 再捕获 → 再提交 → 再跑一次证不动点"**。
11. **★ 硬纪律（本项目既有）**：**判据必须能真的红**——新判据必须配变异，且要有"**必须仍绿**"的边界对照（仿 `M50`）。
12. **★ 硬纪律**：**声明必须能被一条命令一秒推翻**；只验了一部分就**明写只验了哪一部分**（"声明比事实大"是本项目第一号病灶）。

## 实测基线（**快照**：写计划时 2026-09-30 已确认 —— **不是今天的事实**；改动前必须复跑确认。**★ 不逐个改写表里的数**：改了就从"快照"变成"活的"、下次还会漂，同 §H.1.1"逐字捕获件只能重跑重捕获"的纪律。**要取今天的值**：对下表各件跑 `wc -l tests/skills/figure-choose/check-figure-style.py tests/skills/figure-choose/check-house-style.py tests/skills/plot-python/gen-mcm-style.py .claude/skills/mcm-plot-python/assets/mcmplot.py .claude/skills/mcm-figure-choose/references/house-style.md tests/skills/figure-choose/fixtures/expected.tsv`，变异总数跑 `python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"`（**合计行不是末行**：驱动器真正的末行是「（本驱动器共…）」括注，`tail -1` 取不到；约 225 s））

| 事实 | 值 | 出处 |
| :--- | :--- | :--- |
| `check-figure-style.py` | 223 行；判据在 `check()` L178–197 **顺序 append**，**没有表** | 探查报告 B4 |
| `fail_closed()` | L103–106；exit **2**，不打判词 | 同上 |
| `color_count()` | L138–150，**先剔近灰 `max−min<24`** 再按占比 ≥0.5% 数 | 同上 |
| `check-figure-style.py` 今天 | **没有任何**判"底色"或"色序/颜色集合"的逻辑（5 条 grep 全 exit=1） | 探查报告 E |
| `check-house-style.py` | 1142 行；`GUARDS` **5 元组** `(id, 正则, 期望值来源, 容差, 说明)` | 探查报告 B5 |
| **`CENSUS`** | 扫 `house-style.md` **全文所有数字**；未进 `REASONS`(7) 或 `CONTEXT_REASONS`(12) 的**一律 FAIL**，**无兜底** | 同上 |
| **`K8`** | `house-style.md` **每个 `### H<n>.` 条目必须恰有一行 `**验证**：`** | 同上 |
| `mutate-figure-style.py` | 总数 **53 = 9+13+7+13+4+7**（L1661 现算）；跑一次 **约 225 s** | 探查报告 B6 |
| `gen-mcm-style.py` | 205 行；`ANCHORS` **11 条三元组**；`MPLSTYLE_OVERRIDES` **8 条**；`replace_region()` 只换标记之间 | 探查报告 A1 |
| `expected.tsv` | 3 列；**21 条数据行**（`MISMATCH 0 / 21` 的 21 就是它） | 探查报告 B7 |
| `house-style.md` | 267 行；§0「交付形态前提」= **L26–L30**；H12 = **L240–L254** | 探查报告 C8 |
| `mcmplot.py` | 125 行；生成标记区 **L55–L72**；`HOUSE_STYLE` **11 键**；『已知缺口』段 **L26–L41** | 探查报告 C10/D14 |

**★ 两个会咬人的（本计划必须处理）**：
- **`CENSUS` 会因 H14 里任何新数字而红** ⇒ 破坏任一整数数字都要么进 `REASONS`/`CONTEXT_REASONS`，要么**写成不带裸数字的措辞**。
- **`K8` 要求 H14 条目内恰有一行 `**验证**：`**，否则红。

---

## Task 1: 规范侧三条改动（含让既有守卫重新全绿）

**Files:**
- Modify: `.claude/skills/mcm-figure-choose/references/house-style.md`（§0 = L26–L30；H12 = L240–L254；文件末 = L267 后追加 H14）
- Modify: `tests/skills/figure-choose/check-house-style.py`（`REASONS` L319–327 · `CONTEXT_REASONS` L330–342）
- Modify: `.claude/skills/mcm-figure-choose/SKILL.md`（**仅当** K5 因新数字需要声明时）
- Test: 既有 `python tests/skills/figure-choose/check-house-style.py`（整份跑）

**Interfaces:**
- Consumes: 无（本任务是最上游）
- Produces: `house-style.md` 里**三条新内容** ——
  ① §0 新增一条「**底色 = 论文底色（白）**」的交付形态前提；
  ② 新增 **`### H14. 配色：显式色序`**（含恰好一行 `**验证**：`），其中给出一份**载体无关的显式色序 N 色 hex 列表**；
  ③ **H12 条目内**补一组**明确的默认倍数与默认值**。
  ⇒ Task 2 的生成器要按这三处的**字面形态**写锚点。

- [ ] **Step 1: 先跑一遍现状，确认基线全绿**

```bash
python tests/skills/figure-choose/check-house-style.py | tail -3
```
Expected: `RESULT: PASS`（这是改动前的基线。**若不是 PASS ⇒ 停手报 BLOCKED**，先查清为什么不绿）

- [ ] **Step 2: 写 §0 底色前提（L30 之后插入一段）**

插在 `house-style.md` **L30 之后**（即 §0「交付形态前提」那一段的末尾），**措辞里不许出现裸整数**（防 CENSUS）：

```markdown
**★ 交付形态前提：底色 = 论文底色（白）。**
论文正文是白底 ⇒ 图文件也必须是白底，否则贴进正文是一块黑斑。
**这条是「交付形态」前提，不是「获奖分布」读数**——本规范**没有**统计过获奖图底色，故它**不带任何样本读数**。
⚠️ **实测算出的危险**：无头 MATLAB 默认出**深色底**图，而 `check-figure-style.py` 的 F1/F2/F3 对它
**逐条 PASS**（实测：深色底产物四载体满分通过）⇒ **本条必须有机械判据兜底**，判据归属 = `check-figure-style.py` 的同名判据。
```

- [ ] **Step 3: 追加 `### H14.`（文件末 L267 之后）**

**必须含恰好一行 `**验证**：`**（K8 硬要求），且**整条不出现任何裸整数数字字面**（防 CENSUS）：

```markdown
### H14. 配色：显式色序（**不用工具默认色序**）

**规则**：图的**系列色**必须从下面这份**载体无关的显式色序**里取（按序取用，序列超过则可循环或加标记区分）；
**不得**使用任何绘图工具的**默认色序**。
**序列表**（八个色，hex，按序取用）：

| 序位 | hex | 说明 |
| :--- | :--- | :--- |
| 一 | `#E69F00` | 橙 |
| 二 | `#56B4E9` | 天蓝 |
| 三 | `#009E73` | 青绿 |
| 四 | `#CC79A7` | 玫紫 |
| 五 | `#0072B2` | 蓝 |
| 六 | `#D55E00` | 朱红 |
| 七 | `#7570B3` | 紫 |
| 八 | `#4D4D4D` | 深灰（**非彩色**，用满前七色后才轮到） |

⚠️ **本表经用户 2026-09-30 两次定稿**，与**第一版完全不同**：第一版是控制者从 MATLAB 侦察 dump 里抄的
（被复审判为"**被本规则禁止的 MATLAB 默认色序的手改版**"、自相矛盾）；第二版起换成真自选的色板。
⇒ 若在别处（含 `tests/m3-matlab-recon/out-*.txt` 这类**逐字捕获的证据件**）看到 `#1171BE` 一类旧色，
那是**历史捕获，不许改**；**本条以本表为准**。

**来源**：〔**交付形态 / 口径**〕—— **不是**样本读数。
⚠️ **本条与 H5 是两回事，不许互相引用成"依据"**：H5 是**实测分布陈述**（"默认色序在获奖样本中未观察到广泛使用，
下界 0.9%"），本条是**规定**。**H5 原样保留、不改**；本条的序列表**不得**被说成"从样本里量出来的"。
**违反判据**：`check-figure-style.py` 的**显式色序判据**报 FAIL（图上系列色落在允许集合外）。
**复跑命令**：`python tests/skills/figure-choose/check-figure-style.py --fig <路径> --caption 'Figure 1: x' --textwidth-in 6.31`
**验证**：①（机械：`check-figure-style.py` 的显式色序判据）
```

- [ ] **Step 4: 跑整份守卫，看它红在哪**

```bash
python tests/skills/figure-choose/check-house-style.py 2>&1 | grep -E "^FAIL|RESULT"
```
Expected: 至少 `FAIL  CENSUS`（新加的数字没进白名单）。
**★ 这是预期内的红**——它证明 CENSUS 真的在守（不是恒真）。若**没有**红 ⇒ 说明 CENSUS 没管到这里，**停下来查清**再往下。

- [ ] **Step 5: 按 CENSUS 的报错逐条补白名单**

对每一条 CENSUS 报出的命中，**二选一**：
- **能自证的**（数字本体就说明它是什么，如「八个色」这种**不落阿拉伯数字**的写法**不会**触发）；⇒ 优先**改措辞消除裸数字**。
- **消除不掉的** ⇒ 加进 `check-house-style.py` 的 `REASONS`（L319–327，**数字本体自证**）或 `CONTEXT_REASONS`（L330–342，**±80 字符窗口自证**）。
  ⚠️ **加进去的每条必须写清"它为什么自证"**；**不许加万能兜底**（`REASONS`/`CONTEXT_REASONS` 两张表本来就刻意没有兜底，见文件 L314–318 的自述）。

- [ ] **Step 6: H12 补默认值（在 L242 规则行内补齐，不动 L243 起的元数据段）**

⚠️ **不许改坏生成器三个 H12 锚点依赖的字面**（`正文的 **0.8–1.0×**` / `最小 **≥7 pt**`，见 `gen-mcm-style.py` L79–85 的
`H12-font-scale-lo/hi/min-pt` 与 `check-house-style.py` L287/289/291 的 `G-H12-*`）。

在 **L242 那一行**（`**规则**：图内字号 = …`）**行尾追加**：

```markdown
**默认取值（本规范规定的落地默认，来源〔社区〕、非样本读数）**：默认取 **上限**（即正文 p t 的 `1.0×`），
但**不得低于下限**（`≥7 pt`）；线宽默认 `1.0 pt`；字体族默认 **Times 系衬线**（罗马正体）。
```

⚠️ 上面这段里的阿拉伯数字会触发 CENSUS ⇒ **按 Step 5 的同一套办法处理**。

- [ ] **Step 7: 跑整份守卫，必须全绿**

```bash
python tests/skills/figure-choose/check-house-style.py | tail -3
```
Expected: `RESULT: PASS`
**★ 若 K8 红**（H14 缺 `**验证**：` 行或多于一行）⇒ 修 H14 条目本身，**不许改 K8**。

- [ ] **Step 8: 跑引用完整性全扫器**（H14 引入的小数会不会与家族 skill 文本碰撞）

```bash
python tests/skills/figure-choose/check-spec-pointers.py | tail -3
```
Expected: `RESULT: PASS (绘图家族 1 个，K2/K3 全绿)`
**★ 若 K3 红** ⇒ 说明 H14 新增的某个小数字面与某个家族 `SKILL.md` 现有文本碰撞
（⚠️ **hex 里的数字不会进小数族** —— `#` 与字母的邻接把 `\d+` 前瞻挡掉了，已实测；**真会进的是你自己写的带小数点的东西**）
⇒ **改 H14 的措辞消除碰撞**，**不许改 `mcm-plot-python/SKILL.md`**（它在射程外）。

- [ ] **Step 9: 提交**

```bash
git add .claude/skills/mcm-figure-choose/references/house-style.md \
        tests/skills/figure-choose/check-house-style.py
git commit -m "docs(m3-style): 规范侧三条 —— §0 底色前提 + 新 H14 显式色序 + H12 默认值"
```

---

## Task 2: 载体无关样式表（生成器 + 派生件 + 新鲜度守卫）

**Files:**
- Create: `tests/skills/figure-choose/gen-style-table.py`
- Create: `.claude/skills/mcm-figure-choose/assets/mcm-style.json`（**派生件**，由生成器产出）
- Create: `tests/skills/figure-choose/check-style-table-freshness.py`
- Modify: `.claude/skills/mcm-figure-choose/SKILL.md`（说明分工；**须先过 K1 行数上界 150，当前 84 行**）

**Interfaces:**
- Consumes: Task 1 产出的 `house-style.md` 三条新内容的**字面形态**
- Produces: `mcm-style.json`，其**顶层结构**（Task 3/4 依赖）：

```json
{
  "_generated_by": "tests/skills/figure-choose/gen-style-table.py",
  "_source": ".claude/skills/mcm-figure-choose/references/house-style.md",
  "entries": [
    {
      "id": "bg",
      "clause": "§0",
      "value": "#FFFFFF",
      "origin": "as-delivered",
      "carriers": {
        "python": {"how": "rcParams: figure.facecolor / axes.facecolor / savefig.facecolor", "status": "same-value"},
        "matlab": {"how": "figure(...,'Theme','light') + set Color", "status": "same-value"},
        "origin": {"how": null, "status": "pending-probe"}
      }
    },
    {
      "id": "series.color",
      "clause": "H14",
      "value": ["#E69F00", "#56B4E9", "#009E73", "#CC79A7", "#0072B2", "#D55E00", "#7570B3", "#4D4D4D"],
      "origin": "as-delivered",
      "carriers": { "...": "..." }
    }
  ]
}
```

**`origin` 字段**的三个**枚举值**（与 Global Constraint 8 一一对应，**不许自造**）：
`"measured"`（① 实测分布）· `"community"`（② 社区值）· `"as-delivered"`（③ 交付形态/口径）。

**★ `carriers.<名>.status` 的枚举 —— 以本条为唯一权威（共 5 个值，不许自造）**：

| 值 | 含义 | 今天用在哪 |
| :--- | :--- | :--- |
| `same-value` | 该载体能设成**同一个值** | python / matlab |
| `family-equivalent` | 只能做到**同族等价**（如字体各取本机可用的 Times 系） | python / matlab |
| `not-landable` | **该载体今天没有实测到的落地方式**（**必须写 `why`，且措辞只能到"今天没测到"，不许断言"永不可能"**） | python / matlab / origin |
| `scriptable` | 该支**能脚本化**、且 `F1`/`F4`/`F5` 在它上面有承重（Origin 支专用，design §6.3 定） | origin |
| `not-embedded` | 该格的值**不体现在产物里**（Origin 的 PDF 不内嵌字体 ⇒ `F6` 对它只能判 `N/A`）**——**★ **这半句已被实测证伪，见下方订正** | origin |

⚠️ **本节原先写"三个枚举值"、`design §6.3` 又加了两个 ⇒ 计划内部自相矛盾**（三处写法各不相同：本节 3 个、
下一段 5 个、代码骨架 4 个）。**2026-09-30 由 Task 2 修复轮的 Q2 指出、控制者当场坐实并统一到本表。**
⚠️ **`pending-probe` 已废弃**（Origin 探针已回）⇒ 表里**不许**再出现它。

★★ **订正（2026-10-03 批量清 `M3-origin-T1i`）：上表 `not-embedded` 格与本节下文里"Origin 的 PDF 不内嵌字体 ⇒ `F6` 只能判 `N/A`"这个负向全称，已被 `mcm-plot-origin` 支实测证伪** ——
Origin 产物**落哪一态依产物而定**：含**内嵌的 `Type3` 过程字形件**时 `F6` 按**族名**判（`PASS`/`FAIL`），
不含时才 `N/A`。且 **`/FontFile* = 0` ≠ 没内嵌字体**（`Type3` 过程字形件无该条目）。
**现行口径以 `.claude/skills/mcm-figure-choose/assets/mcm-style.json` 的 origin 字体两格为准**（`status = family-equivalent`）。
下文凡出现同一负向全称处，均按此订正理解。

**★ `origin` 列的契约（design §6.3，**2026-09-30 更新：脚本为权威、值已实测**）**：
每个 id 的 `carriers.origin` **必须**填**实测到的脚本命令 + 操作步骤**（不再是 `null`），并满足四条：
① 含载体无关值（hex/pt/字体族名）；② **可照做的脚本命令**（LabTalk / X-Function **原文**）；
③ **可照做的操作步骤**（菜单路径 + 控件名 + 要填的值）作为**辅路**；
④ 标**针对哪个 Origin 版本**（本机实测 `10.300197` = Origin 2026 **OriginPro 教育版**）。
`status` 的取值：**`"scriptable"`**（本支能脚本化、且 `F1`/`F4`/`F5` 在它上面有承重）；
**字体那一格单独标 `"not-embedded"`**（它的 PDF 不内嵌字体 ⇒ `F6` 只能判 `N/A`，见 Task 3 Step 6）。
★ **订正（2026-10-03 批量清 `M3-origin-T1i`）**：这句的负向全称**已被实测证伪** —— 现行该格 `status = family-equivalent`，
`F6` 依产物是否含内嵌 `Type3` 过程字形件而落 `PASS`/`FAIL`/`N/A` 三态（见本节上方订正块）。

**已实测、可直接落进表的四条**（来自 `tests/m3-origin-probe/` 与 `tests/m3-origin-font-probe/`）：
- **导出宽度**：`GPage.save_fig(width=N)` / `expGraph … tr1.Unit:=2 tr1.Width:=N`（英寸用 `tr1.Unit:=0`）；
  PNG 像素逐值命中、PDF 页盒量化 1/144 in（`6.31 → 6.31944`）；**实测 F1 = 1.001**。
- **字体族**：`expGraph … theme:="Times New Roman Font";`（产物字体名 `SimSun → TimesNewRomanPSMT`）。
  ⚠️ **次序坑**：主题**必须在导出那一刻施加**（`themeApply2g` 只作用于已存在对象 ⇒ 否则半张图两字体）。
  ⚠️ **给不存在的主题名会静默成功**（`exec_ok=True`、产物无变化）⇒ **只能用产物证明**。
- **底色 = 白**：默认就是白（四角 `255,255,255`）。
- **显式色序**：hex 逐色可设、**无会话内翻转**。
- ⚠️ **进程卫生**：包装必须 `try/finally: op.exit()`（`atexit` 只卸连接、**不退进程**）。

⚠️ **填值前必须自己复跑一遍**（`tests/m3-origin-*/README.md` 里有再生成命令）——**不许照抄本计划的读数**。

- [ ] **Step 1: 写失败测试（生成器还不存在）**

```bash
python tests/skills/figure-choose/gen-style-table.py --check
```
Expected: `exit != 0`，`No such file or directory`（因为文件还没建）

- [ ] **Step 2: 写生成器（重放式，仿 `gen-mcm-style.py`）**

Create `tests/skills/figure-choose/gen-style-table.py`。**结构照抄 `tests/skills/plot-python/gen-mcm-style.py`**（205 行）的范式：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M3 载体无关样式表生成器（重放式）。从规范 house-style.md 抽取/投影出 mcm-style.json。

用法：
  python tests/skills/figure-choose/gen-style-table.py [--doc <路径>] [--check]
退出码：0 成功 · 1 锚点不命中或标记缺失（**不写任何文件**）
末行：`重放 → <产出件>（<N> 条）`
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
HOUSE = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
OUT   = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"


class GeneratorError(Exception):
    pass


# ── 锚点：从规范抽"有数可抽"的量（逐条必须恰命中 1 处，仿 gen-mcm-style.py 的 fail-closed）
ANCHORS = (
    ("H1-width-min",       r"\*\*不窄于 ([\d.]+)×\*\*",           ("h1.width_ratio.min", "measured")),
    ("H1-width-max",       r"\*\*不超过 ([\d.]+)×\*\*",           ("h1.width_ratio.max", "measured")),
    # ★★ 2026-09-30 补（Task 2 复审 I-2 逼出）：**F1 承重的默认比值必须进表**。
    #   原先漏了这两条 ⇒ 表里没有它、而 `_W_PY` 的 how 却宣称"表内的 default_hi"，**声明比事实大**。
    #   锚点形态与既有 `gen-mcm-style.py:22-23` 的 `H1-width-default-lo/hi` **一致**（同一份规范、同一处字面）。
    ("H1-width-default-lo", r"（\*\*([\d.]+)–[\d.]+×\*\*）",        ("h1.width_ratio.default_lo", "measured")),
    ("H1-width-default-hi", r"（\*\*[\d.]+–([\d.]+)×\*\*）",        ("h1.width_ratio.default_hi", "measured")),
    ("H3-height",          r"图高按 \*\*([\d.]+) in 量级\*\*",     ("h3.height_in",       "measured")),
    ("H4-max-main-colors", r"彩色\*\*主色 ≤(\d+)\*\*",            ("h4.max_main_colors", "measured")),
    ("H12-font-scale-lo",  r"正文的 \*\*([\d.]+)–[\d.]+×\*\*",    ("h12.font_scale_lo",  "community")),
    ("H12-font-scale-hi",  r"正文的 \*\*[\d.]+–([\d.]+)×\*\*",    ("h12.font_scale_hi",  "community")),
    ("H12-font-min-pt",    r"最小 \*\*≥(\d+) pt\*\*",             ("h12.font_min_pt",    "community")),
)


def extract(text):
    out = []
    for aid, pat, (key, origin) in ANCHORS:
        hits = list(re.finditer(pat, text))
        if len(hits) != 1:
            raise GeneratorError(f"{aid}：正则命中 {len(hits)} 处（必须恰 1）")
        out.append((key, hits[0].group(1), origin))
    return out


# ── 常量区：正则抽不到的（规范里只有规则没有数、或来源是交付形态）——
#    ★ 每一条都必须带 origin，且 origin 必须来自 Global Constraint 8 的三个枚举值，不许自造。
#    ★ 这些常量本身也要有守卫（见 check-house-style.py 的 const: 机制）。
CONSTS = (
    # 底色：来源 = §0「交付形态前提」，不是样本读数
    ("bg",            "#FFFFFF", "as-delivered", "§0",  "论文底色 = 白"),
    # 显式色序：来源 = H14，是**规定**不是读数
    ("series.color",  ["#E69F00", "#56B4E9", "#009E73", "#CC79A7",
                       "#0072B2", "#D55E00", "#7570B3", "#4D4D4D"],
                      "as-delivered", "H14", "H14 的八色序列（用户 2026-09-30 二次定稿）"),
    # 字体族：按族等价（Global Constraint 1）
    ("font.family",   "serif", "as-delivered", "H12", "衬线族"),
    ("font.serif",    ["TeXGyreTermesX", "Times New Roman"], "as-delivered", "H12",
                      "各载体取本机可用的 Times 系实现"),
    ("lines.linewidth", 1.0, "community", "H12", "线宽默认值"),
)


def carrier_map():
    """每个 id 的载体落地表。status 只能取本节上方统一表里的 5 个值之一（同一条**唯一权威**）。"""
    return {
        "bg": {
            "python": {"how": "rcParams: figure.facecolor / axes.facecolor / savefig.facecolor", "status": "same-value"},
            "matlab": {"how": "figure(...,'Theme','light') + set(gcf,'Color','w') + set(gca,'Color','w')", "status": "same-value"},
            "origin": {"how": None, "status": "pending-probe"},
        },
        "series.color": {
            "python": {"how": "rcParams: axes.prop_cycle", "status": "same-value"},
            "matlab": {"how": "set(gca,'ColorOrder',[...])", "status": "same-value"},
            "origin": {"how": None, "status": "pending-probe"},
        },
        "font.family": {
            "python": {"how": "font.family: serif", "status": "family-equivalent"},
            "matlab": {"how": "set(gca,'FontName','Times New Roman')", "status": "family-equivalent"},
            "origin": {"how": None, "status": "pending-probe"},
        },
        "font.serif": {
            "python": {"how": "入库 OTF TeXGyreTermesX（随 skill，干净检出可用）", "status": "family-equivalent"},
            "matlab": {"how": "系统 Times New Roman（点名即内嵌，非静默回退）", "status": "family-equivalent"},
            "origin": {"how": None, "status": "pending-probe"},
        },
        "lines.linewidth": {
            "python": {"how": "lines.linewidth", "status": "same-value"},
            "matlab": {"how": "set(h,'LineWidth',v)", "status": "same-value"},
            "origin": {"how": None, "status": "pending-probe"},
        },
    }


def build(doc_path):
    text = pathlib.Path(doc_path).read_text(encoding="utf-8")
    entries = []
    for key, raw, origin in extract(text):
        entries.append({"id": key, "clause": key.split(".")[0].upper(),
                        "value": (float(raw) if "." in raw else int(raw)),
                        "origin": origin, "carriers": carrier_map().get(key, {})})
    for key, val, origin, clause, why in CONSTS:
        entries.append({"id": key, "clause": clause, "value": val, "origin": origin,
                        "why": why, "carriers": carrier_map()[key]})
    return {"_generated_by": "tests/skills/figure-choose/gen-style-table.py",
            "_source": str(HOUSE.relative_to(ROOT)).replace("\\", "/"),
            "entries": entries}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    doc = a.doc or HOUSE
    try:
        data = build(doc)
    except GeneratorError as e:
        print(f"FAIL  ANCHOR  {e}", file=sys.stderr)
        return 1
    body = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    if a.check:
        cur = OUT.read_bytes().decode("utf-8") if OUT.is_file() else None
        if cur != body:
            print("FAIL  STALE  派生件与重放结果不一致", file=sys.stderr)
            return 1
        print(f"重放 → {OUT.relative_to(ROOT)}（{len(data['entries'])} 条）· 一致")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(body.encode("utf-8"))          # ★ write_bytes，全仓禁 write_text
    print(f"重放 → {OUT.relative_to(ROOT)}（{len(data['entries'])} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: 跑生成器，产出派生件**

```bash
python tests/skills/figure-choose/gen-style-table.py
python -c "import json;d=json.load(open('.claude/skills/mcm-figure-choose/assets/mcm-style.json',encoding='utf-8'));print(len(d['entries']),'条');print([e['id'] for e in d['entries']])"
```
Expected: 末行 `重放 → .claude/skills/mcm-figure-choose/assets/mcm-style.json（12 条）`，随后打印 12 个 id

- [ ] **Step 4: 跑 `--check`（漂移检测必须能真的红）**

```bash
python tests/skills/figure-choose/gen-style-table.py --check   # 期望 exit 0
python - <<'PY'
import pathlib
p = pathlib.Path('.claude/skills/mcm-figure-choose/assets/mcm-style.json')
p.write_bytes(p.read_bytes().replace(b'#FFFFFF', b'#FFFFFE'))   # 手改一个字节
PY
python tests/skills/figure-choose/gen-style-table.py --check   # 期望 exit 1 + FAIL STALE
git checkout .claude/skills/mcm-figure-choose/assets/mcm-style.json
```
Expected: 第一次 exit 0；手改后 exit 1 且打印 `FAIL  STALE`；然后还原

- [ ] **Step 5: 写新鲜度守卫**

Create `tests/skills/figure-choose/check-style-table-freshness.py`。**照 `tests/skills/plot-style-python/check-style-freshness.py`（314 行）的范式**，但**剪到最小**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcm-style.json 新鲜度守卫。只读 + 重跑生成器 + 逐字节比对。

两条臂（缺一不可，理由同 check-style-freshness.py：生成器会**原地重写**派生件）：
  A1 入库快照臂：比 `git show HEAD:<path>` 的原始字节
  A2 工作树臂  ：比**重跑之前**读到的工作树字节
退出码 0/1（本器无 2）。末行恒为 `RESULT: …`。
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"
GEN = ROOT / "tests/skills/figure-choose/gen-style-table.py"
REL = TARGET.relative_to(ROOT).as_posix()


def snapshot_head():
    r = subprocess.run(["git", "show", f"HEAD:{REL}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def run():
    head = snapshot_head()
    wt = TARGET.read_bytes()
    rows, bad = [], 0
    try:
        rc = subprocess.run([sys.executable, str(GEN)], cwd=ROOT, capture_output=True).returncode
        for arm, want in (("A1", head), ("A2", wt)):
            if rc != 0 or want is None:
                rows.append(("FAIL", arm, "生成器没跑成或参照缺失 ⇒ 两臂一并记红"))
                bad += 1
                continue
            now = TARGET.read_bytes()
            ok = now == want
            rows.append(("PASS" if ok else "FAIL", arm,
                         "逐字节一致" if ok else f"不一致（{len(want)}B → {len(now)}B）"))
            bad += 0 if ok else 1
    finally:
        TARGET.write_bytes(wt)          # 还原（非原子：进程在重跑与还原之间被杀会留脏，那时 A2 会自曝）
    for st, arm, note in rows:
        print(f"{st}  {arm}  {note}")
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
```

- [ ] **Step 6: 跑守卫（两臂都要绿）**

```bash
python tests/skills/figure-choose/check-style-table-freshness.py; echo "exit=$?"
```
Expected:
```
PASS  A1  逐字节一致
PASS  A2  逐字节一致
RESULT: PASS
exit=0
```

- [ ] **Step 7: 证明它能真的红（★ 硬纪律 11）**

```bash
python - <<'PY'
import pathlib
p = pathlib.Path('.claude/skills/mcm-figure-choose/assets/mcm-style.json')
p.write_bytes(p.read_bytes().replace(b'#FFFFFF', b'#FFFFFE'))
PY
python tests/skills/figure-choose/check-style-table-freshness.py; echo "exit=$?"   # 期望 **只红 A2**
python tests/skills/figure-choose/gen-style-table.py               # ← 用重跑还原（新件未入库，git checkout 无效）
```
Expected: **`PASS  A1` + `FAIL  A2` + `RESULT: FAIL` + `exit=1`**

**★★ 本节原写"A1 + A2 都红"是错的（2026-09-30 Task 2 实现者当场证伪，控制者的机理判断错）。**
**A1 的语义是"HEAD 快照 vs 重跑结果"** —— 手改**工作树**的字节**不动 HEAD**、而重跑又会把字节改回**正确**值
⇒ **A1 必然 PASS**，这是它的正确行为（与参照件 `tests/skills/plot-python/check-style-freshness.py` 同构），**不是缺陷**。
⇒ **要证 A1 也能被证伪**，须让 **HEAD 自身变陈旧**（例如临时改生成器的常量区、提交、再跑），
拿到 `FAIL A1 + FAIL A2` 后还原。⇒ **A1 与 A2 是两条互补的臂，不是同一条的两份。**
⚠️ **还原方式**：新件**尚未入库**时 `git checkout <路径>` **无效**（没有 HEAD 版本可还原）⇒ 用**重跑生成器**还原，并核哈希回到原值。

- [ ] **Step 8: `SKILL.md` 说清分工（注意 K1 行数上界 150，当前 84）**

在 `.claude/skills/mcm-figure-choose/SKILL.md` 的**指针段**（指 `references/house-style.md` 的那一处）之后追加一段：

```markdown
**机器投影**：`assets/mcm-style.json` 是本规范给**实现方**用的机器投影（由
`tests/skills/figure-choose/gen-style-table.py` 从本规范重放产出）。
**分工**：规范正文（本目录 `references/house-style.md`）是**唯一权威**；那份 json 是它的投影，**勿手改**——
每个载体（`mcm-plot-*` 等）只读它、各自映射成本工具的设置。
```

- [ ] **Step 9: 跑 K1–K8，必须全绿**

```bash
python tests/skills/figure-choose/check-house-style.py | tail -3
python tests/skills/figure-choose/check-spec-pointers.py | tail -3
time python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"   # ★ 合计行不是末行；见下
```
Expected: 前两个 `RESULT: PASS`；驱动器 **全达预期、`grep -c '^RED-BAD'` = 0**
**★ 若 K5 红**（SKILL.md 里出现了未声明的数字）⇒ 按 K5 的要求补声明行或改措辞，**不许改 K5**。

**★★ 本步原漏了 MUT —— 这是控制者的计划缺口，代价已经付过一次（2026-09-30）**：
本任务会改 `.claude/skills/mcm-figure-choose/SKILL.md`（Step 8 加那段"机器投影/分工"），
而**变异驱动器里有一条 `M30` 正是打 `SKILL.md` 的指针行的**：它原假设"删掉指针行 ⇒ `K2` 红"，
而新加的那段**又含了一次同一个相对路径** ⇒ `M30` 变成 **`RED-BAD`**（它证的那件事不再成立）。
**这个回归 Task 2 的独立复审没抓到 —— 因为本任务当时的验收里没有 MUT**，直到 **Task 3** 的实现者顺手跑了驱动器才发现。
⇒ **凡本任务改 `SKILL.md`，MUT 必须进验收**；**并且不许为了让 `M30` 变绿而弱化它的断言**（正确做法是让 `M30` 真的把指针删干净，或让 `SKILL.md` 里该路径回到唯一一处）。

- [ ] **Step 10: 提交**

```bash
git add tests/skills/figure-choose/gen-style-table.py \
        tests/skills/figure-choose/check-style-table-freshness.py \
        .claude/skills/mcm-figure-choose/assets/mcm-style.json \
        .claude/skills/mcm-figure-choose/SKILL.md
git commit -m "feat(m3-style): 载体无关样式表 —— 生成器 + mcm-style.json + 新鲜度守卫"
```

---

## Task 3: 共享判据三条（底色 / 显式色序 / 字体族）+ 变异

**Files:**
- Modify: `tests/skills/figure-choose/check-figure-style.py`（判据 append 处 = `check()` L178–197；常量区）
- Modify: `tests/skills/figure-choose/fixtures/expected.tsv`（+ 新行）与 `fixtures/make-fixtures.py`（+ 新 fixture）
- Modify: `tests/skills/figure-choose/mutate-figure-style.py`（`MUTATIONS` L377–400 或相应表）
- Test: `python tests/skills/figure-choose/fixtures/run-expected.py`

**Interfaces:**
- Consumes: Task 2 的 `mcm-style.json`（`entries` 里 `id == "bg"` 的 `#FFFFFF`；`id == "series.color"` 的八色序列）
- Produces: 三个新判据 id —— **`F4`**（底色）· **`F5`**（显式色序）· **`F6`**（字体族）；
  以及一份**实测标定**出的底色阈值常量 `BG_MIN_LUMA`（写进 `check-figure-style.py` 常量区）。

- [ ] **Step 1: ★ 先标定底色阈值（**不许拍脑袋**，Global Constraint 9）**

本仓已实测的两端（**用它们标定，不许自己选数**）：
- 深色端：MATLAB 深色底产物画布 `(16,16,16)`、轴区 `(18,18,18)`（见 `tests/m3-matlab-recon/` 的证据与报告）
- 浅色端：`(255,255,255)`（python 侧 6 张图 + MATLAB 浅色配方）

```bash
python - <<'PY'
# 标定：取两头的中点，并把「近白」定义为「众数亮度 >= 阈值」
dark_axis, white = 18, 255
print("候选阈值（南辕北辙的两头中点）:", (dark_axis + white) // 2)
PY
```
Expected: 打印出候选阈值（约 **136**）。
**把量出来的这个数写进 `check-figure-style.py` 常量区**，并在常量旁注释**它是怎么来的**（哪两端的实测值）。

- [ ] **Step 2: 写 `F4`（底色）的失败测试**

```bash
python - <<'PY'
from PIL import Image
import pathlib
p = pathlib.Path('/tmp/bg-dark-probe.png')
Image.new('RGB', (400, 300), (18, 18, 18)).save(p)
print(p)
PY
python tests/skills/figure-choose/check-figure-style.py \
  --fig /tmp/bg-dark-probe.png --caption 'Figure 1: x' --textwidth-in 6.31 --dpi 100 | grep -E "F4|RESULT"
```
Expected: `FAIL  F4`（**因为 F4 还没实现 ⇒ 这一步其实会「没有 F4 这一行」**）
⇒ **先确认它现在没有 F4**（`grep -c "F4" tests/skills/figure-choose/check-figure-style.py` = 0），再往下。

- [ ] **Step 3: 实现 `F4`（底色）**

在 `check-figure-style.py` 常量区加：

```python
# ★ 底色阈值：由实测两端标定（深色端轴区 (18,18,18) / 浅色端 (255,255,255)），中点见 Task 3 Step 1
BG_MIN_LUMA = 136
```

在 `check()`（L178–197）**F1 那一条之前**插入。
★ **`im4` 只取一次**（下面的 F5 也用它）；`getcolors` 的分母**按实际尺寸算**，**不许写死**：

```python
    # ---- 底色 / 颜色身份：共用一次栅格化（避免两次读图口径不一致）
    im4 = raster_rgb(fig)
    tot4 = im4.size[0] * im4.size[1]
    _cols = im4.getcolors(tot4) or []

    # F4 **背景**为白。★ 不能用角落单像素（实测 MATLAB 会出现「外围白、轴区仍深」）。
    # ★★ 2026-10-01 订正：以下是**最终口径**（合取），**不是**本计划初稿那版「单口径全图众数底色」。
    #   初稿写的是 `mode_rgb = max(_cols, key=lambda t: t[0])[1]` / 判词「底色亮度」，已被
    #   F4-refix 轮取代：全图众数会被大面积内容占住，且没有一路能把「深色底」与「白底上的深色内容」
    #   分开。**权威实现在 tests/skills/figure-choose/check-figure-style.py 的 §F4**（判据只写一处，
    #   这里给指针；下面的代码块与它逐行同形，不含第二份判据）。
    #   判词说的是**背景**亮度：两条腿量的都是背景（外缘环 / 近灰档），不是"全图最多的颜色"。
    ring_rgb, ring_cnt, ring_tot = outer_ring_mode(im4)     # ① 外缘环（四边 1% 厚、含四角）的众数
    luma_ring = luma(ring_rgb)
    gray = [t for t in _cols if max(t[1]) - min(t[1]) < 24]  # ② 近灰档（与 F2/F5 同一支仪器）
    if gray:
        gray_cnt, gray_rgb = max(gray, key=lambda t: t[0])    # 平票取首个（与 getcolors 同序）
        luma_gray = luma(gray_rgb)
        gray_txt = f"近灰众数 RGB {gray_rgb} 亮度 {luma_gray}（占全图 {gray_cnt / tot4:.2%}）"
        f4_ok = luma_ring >= BG_MIN_LUMA and luma_gray >= BG_MIN_LUMA   # 合取：只收紧、不放宽
    else:                                                     # ③ 全图无近灰像素（整幅饱和色）⇒ 直接红
        gray_txt = "近灰众数 无（全图无近灰像素 ⇒ 红）"
        f4_ok = False
    res.append(("F4", f4_ok,
                f"外缘环 RGB {ring_rgb} 亮度 {luma_ring}（占环 {ring_cnt / ring_tot:.2%}）；"
                f"{gray_txt}；下限 {BG_MIN_LUMA}"))
```

- [ ] **Step 4: 跑测试，确认 `F4` 真的红/绿**

```bash
# 深色底 ⇒ 必须红
python tests/skills/figure-choose/check-figure-style.py \
  --fig /tmp/bg-dark-probe.png --caption 'Figure 1: x' --textwidth-in 6.31 --dpi 100 | grep -E "F4|RESULT"
# 真实 GREEN 产物 ⇒ 必须绿（用仓里现成的）
python tests/skills/figure-choose/check-figure-style.py \
  --fig tests/skills/plot-python/green/out-G1/figure.png --caption 'Figure 1: A test figure caption' \
  --textwidth-in 6.31 --dpi 300 | grep -E "F4|RESULT"
```
Expected（**2026-10-01 按最终口径订正**，原文写的是初稿判词 `FAIL  F4  底色亮度 18…`）：
第一句 `FAIL  F4  外缘环 RGB (18, 18, 18) 亮度 18（占环 …%）；近灰众数 …；下限 136` + `RESULT: FAIL`；
第二句 `PASS  F4  …` + `RESULT: PASS`（判词两段都可能被 % 截断，**只看 `FAIL`/`PASS` 与 `RESULT` 行**）。

- [ ] **Step 5: 实现 `F5`（显式色序）**

在常量区加（**从 Task 2 的 `mcm-style.json` 取，不许手写第二份**）：

```python
import json as _json
_STYLE = _json.loads(
    (pathlib.Path(__file__).resolve().parents[2] /
     ".claude/skills/mcm-figure-choose/assets/mcm-style.json").read_text(encoding="utf-8"))
SERIES_COLORS = {c.lower() for c in next(e["value"] for e in _STYLE["entries"] if e["id"] == "series.color")}
```

⚠️ **`SERIES_COLORS` 那一行必须写成单行**（Task 3 Step 9 的 `M55` 要按**字面串**替换它；跨行会让替换次数 ≠ 1、驱动器自报错）。

在 `check()` 里**紧跟 F2 之后**插入（`im4` / `_cols` 已在 F4 那一段取过，**不要重复取图**）：

```python
    # F5 显式色序：图上出现的**显著**颜色必须落在 H14 允许集合的**附近**。
    # ★ 用「最近调色板色距离」而不是精确 hex 相等 —— 抗锯齿/合成必然造出调和色，
    #   精确相等会把合法产物判假红。容差 PALETTE_TOL 是**量出来的**（见本步 ⚠️），不是选的。
    PALETTE = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in sorted(SERIES_COLORS)]
    tot4 = im4.size[0] * im4.size[1]
    far = []
    for cnt, (r, g, b) in _cols:
        if max(r, g, b) - min(r, g, b) < 24:          # 与 color_count() 同口径剔近灰
            continue
        if cnt / tot4 < 0.005:                         # 与 color_count() 同口径：占比 <0.5% 不算主色
            continue
        d = min((r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2 for pr, pg, pb in PALETTE) ** 0.5
        if d > PALETTE_TOL:
            far.append((f"#{r:02x}{g:02x}{b:02x}", round(d, 1), round(cnt / tot4, 4)))
    far.sort(key=lambda t: -t[2])
    res.append(("F5", not far, f"越界主色 {len(far)} 种（离最近调色板色 > {PALETTE_TOL}）：{far[:4]}"))
```

⚠️ **`PALETTE_TOL` 必须先量再定（Global Constraint 9 同一把尺子）**：写判据**之前**，
拿**一张真实产物**（先用 Task 4 之前的口径也行）把每个显著色到最近调色板色的距离**打出来**，看分布：
```bash
python - <<'PY'
from PIL import Image
import pathlib, math
im = Image.open('tests/skills/plot-python/green/out-G1/figure.png').convert('RGB')
im = im.resize((320, 320), Image.NEAREST); tot = 320 * 320
PAL = [(0x11,0x71,0xBE),(0xDD,0x54,0x16),(0xED,0xB1,0x20),(0x7E,0x4A,0xD3),
       (0x3B,0xA9,0x2F),(0x2F,0xBE,0xEF),(0xD1,0x03,0x8B),(0x4A,0x4A,0x4A)]
for cnt, (r,g,b) in sorted(im.getcolors(tot), key=lambda t:-t[0])[:40]:
    if max(r,g,b)-min(r,g,b) < 24 or cnt/tot < 0.005: continue
    d = min(math.dist((r,g,b), p) for p in PAL)
    print(f"#{r:02x}{g:02x}{b:02x}  占比 {cnt/tot:.4f}  离最近调色板色 {d:.1f}")
PY
```
**把量出来的分布写进 `check-figure-style.py` 的注释**（写明"这个阈值是怎么量出来的"），再定 `PALETTE_TOL`。
⚠️ **注意**：本步跑在 Task 4 之前 ⇒ **python 产物此刻还没有 H14 色序**，测出来的距离会**偏大**；
**这一步的目的正是量出"没有显式色序时它离得多远"**（那正是 F5 该抓的）。⇒ **量完之后**：
- 若距离分布**明显两簇**（合法色近、默认色远）⇒ 阈值取在两簇之间，**写下这两个簇的读数**；
- 若**分不开** ⇒ **停手报 BLOCKED**（说明 F5 这个口径在这个判据机器上不成立），**不许硬凑一个阈值**。

⚠️ **这条判据天生偏严**：图中任何**非灰且非全彩色**的像素（抗锯齿边、图例、网格线）都可能落进 `seen`。
⇒ **必须先测出真实产物的读数，再决定口径**（例如按占比过滤 ≥0.5% 才算"系列色"，与 `color_count()` 同口径）。
**把最终口径与它跑出来的读数写进提交信息**。若真实 GREEN 产物在本口径下红 ⇒ **按实测收窄口径**（收窄的依据要写清楚），
**不许**为了让它绿而删掉判据。

- [ ] **Step 6: 实现 `F6`（字体族，"按族等价"）**

在常量区加（**族 → 可接受的内嵌字体名**，依据 design §1.1/§1.8）：

```python
FONT_FAMILY_OK = ("TeXGyreTermesX", "TimesNewRomanPSMT", "TimesNewRoman", "NimbusRoman", "FreeSerif")
```

在 `check()` 里追加：

```python
    # F6 字体族：读**产物内嵌字体**（不能看属性设没设 —— 实测 MATLAB 侧 set 不存在的名字不报错、get 还回声、产物静默回退）
    fams = set()
    if fig.suffix.lower() == ".pdf":
        with fitz.open(fig) as _d:
            for _p in range(_d.page_count):
                for rec in _d.get_page_fonts(_p):
                    fams.add(SUBSET_RE.sub("", rec[3]))
    else:
        res.append(("F6", True, "PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）"))
        fams = None
    if fams is not None:
        # ★ 三态：内嵌且族对 = PASS；内嵌但族错 = FAIL；**一个都没内嵌 = N/A**（判词里必须写出这个事实）
        if not fams:
            res.append(("F6", True, "N/A 本 PDF 未内嵌任何字体 ⇒ 本判据不适用（~~实测 Origin 的 PDF 即如此~~ ★ 订正见 2026-10-03 批量清 M3-origin-T1i：该负向全称已被证伪，Origin 依产物落三态）"))
        else:
            ok = all(any(k in f for k in FONT_FAMILY_OK) for f in fams)
            res.append(("F6", ok, f"内嵌字体 {sorted(fams)}"))
```

★ **第三态 `N/A` 的口径**（design §7.3，2026-09-30 由 Origin 实测逼出）：
- **`fams` 为空 ≠ 通过** —— 它意味着**这个载体不内嵌字体**，判据**对它无从判起**。
- 判词里**必须写出"未内嵌 ⇒ 不适用"这句事实**，**不许**只写 `PASS F6`（那会让"读不到"冒充"读到了且是对的"）。
- ⚠️ 实现上**这里返回 `True`**（不把流水线卡死），但**详情串必须以 `N/A` 开头** ⇒ 汇总结论里能一眼看出
  "这条是通过的**还是没判的**"。**若你找到更好的表示法（如单列一态），说明理由后可以用**。

并加常量 `SUBSET_RE = re.compile(r"^[A-Z]{6}\+")`（与 `check-style-freshness.py` L87 同形）。

⚠️ **PNG 上的处置必须如实**：PNG 里没有字体名 ⇒ **不许让它假绿**（上面写成"不适用"并在详情里写明）。
`fitz` 已在文件里 import 过（`raster_rgb()` 用了），**若没有则补**。
⚠️ **新 fixture 要覆盖 `N/A` 这一态**：仓里现成的 Origin 产物（若有）或**造一个"零内嵌字体"的 PDF**
（可用 `fitz` 或一个不含字体的最小 PDF），断言它得 `N/A` 而**不是** `PASS`。

- [ ] **Step 7: 三个判据都跑一遍真实产物（PNG 与 PDF）**

```bash
for f in tests/skills/plot-python/green/out-G1/figure.png tests/skills/plot-python/green/out-G1/figure.pdf; do
  echo "== $f"
  python tests/skills/figure-choose/check-figure-style.py --fig "$f" \
    --caption 'Figure 1: A test figure caption' --textwidth-in 6.31 ${f##*.} 2>/dev/null || true
done
python tests/skills/figure-choose/check-figure-style.py \
  --fig tests/skills/plot-python/green/out-G1/figure.png \
  --caption 'Figure 1: A test figure caption' --textwidth-in 6.31 --dpi 300
python tests/skills/figure-choose/check-figure-style.py \
  --fig tests/skills/plot-python/green/out-G1/figure.pdf \
  --caption 'Figure 1: A test figure caption' --textwidth-in 6.31
```
Expected（**★ 本步的预期是"有红"，别当成失败**）：

| 判据 | PNG 上 | PDF 上 | 为什么 |
| :--- | :--- | :--- | :--- |
| `F4` 底色 | **PASS** | **PASS** | python 产物本来就是白底（`savefig` 默认） |
| `F5` 显式色序 | **FAIL** | **FAIL** | ★ **预期之内**：**H14 还没在 python 侧落地**（那正是 Task 4 Step 2 的 `axes.prop_cycle`），此刻产物用的还是底座默认色序 ⇒ **F5 抓到的是真问题** |
| `F6` 字体族 | 不适用（如实标，不假绿） | **PASS** | PDF 内嵌的是入库 OTF |

**★ 这一格是本任务最重要的读数**：`F5` 在**Task 4 之前**必须是红的、**Task 4 之后**必须转绿。
⇒ 把它当成 F5 的**端到端证明**：判据真的能红（现在），也能真的被修绿（Task 4 之后，见 Task 5 Step 5）。

**★ 若 `F5` 现在是绿的** ⇒ **F5 是恒真的假判据**，**停手重写它**（这是本项目第一号病灶）。
**★ 若 `F4` 是红的** ⇒ 先查是不是阈值标定错了（Step 1），**不许**直接放宽容差。
**★ 一律不许为了让它绿而删判据或缩小它的射程** —— 射程的收窄只能来自 Step 5 ⚠️ 那条"先量再定"的实测依据。

- [ ] **Step 8: 加 fixture 与期望行**

在 `tests/skills/figure-choose/fixtures/make-fixtures.py` 里加两张 fixture：
`bad-bg-dark.png`（纯 `(18,18,18)` 底 + 一条彩色线）与 `bad-color-order.png`（用一套**不在 H14 里**的色）。
在 `fixtures/expected.tsv` **追加**（保持 3 列）：

```tsv
bad-bg-dark.png	F4	FAIL
bad-color-order.png	F5	FAIL
```

⚠️ **同时确认现有 21 行仍然全对** ⇒ `MISMATCH 0 / 23`（原 21 + 新 2）。

```bash
python tests/skills/figure-choose/fixtures/run-expected.py | tail -3
```
Expected: `MISMATCH 0 / 23`

- [ ] **Step 9: 加变异（★ 硬纪律 11：判据必须能真的红）**

在 `mutate-figure-style.py` 的 `MUTATIONS`（L377–400）**追加三条**（5 元组 `(id, 描述, 源串, 替换串, 断言函数)`），
id 顺延为 **`M54` / `M55` / `M56`**：

```python
("M54", "F4 底色下限 BG_MIN_LUMA 136 -> 0（判据失效）",
        "BG_MIN_LUMA = 136", "BG_MIN_LUMA = 0", m54),
("M55", "F5 允许色序清空（判据失效）",
        'next(e["value"] for e in _STYLE["entries"] if e["id"] == "series.color")',
        '["#000000"]', m55),
("M56", "F6 可接受字体族清空（判据失效）",
        'FONT_FAMILY_OK = ("TeXGyreTermesX", "TimesNewRomanPSMT", "TimesNewRoman", "NimbusRoman", "FreeSerif")',
        'FONT_FAMILY_OK = ("__none__",)', m56),
```

**并各写一个断言函数**（仿 `m1`/`m42` 的写法：跑一次判据，断言它**确实变红**）。
**★ 同时必须加一条"必须仍绿"的边界对照**（仿 `M50` 的 `TIER_GREEN`）：
一条 **H14 之外的合法色序**（例如 H14 八色的前三种）在改动后**必须仍 PASS**，用来钉死"F5 不是恒红"。

- [ ] **Step 10: 跑全套驱动器**

```bash
time python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"   # 合计行不是末行
python tests/skills/figure-choose/fixtures/run-expected.py | tail -2
python tests/skills/figure-choose/check-house-style.py | tail -2
```
Expected: `MUT: 59/59 达预期（合计）`（原 53 + 新 6 = 3 条变异 + 1 条仍绿对照 + 2 条 fixture 相关，**具体数以驱动器现算的合计行为准**——合计行不是末行，须 `| grep "达预期（合计）"`）
· `MISMATCH 0 / 23` · `RESULT: PASS`
**★ 以驱动器**现算的合计行为准**（`| grep "达预期（合计）"`；**合计行不是末行**），不许手写总数到任何文档里**。

- [ ] **Step 11: ★ 本步**不**重生成入库判词转录（节奏）**

**理由**：此刻 `F5` 对真实产品**还是红的**（H14 要到 Task 4 才在 python 侧落地）。
现在重生成 ⇒ 那批证据件会印着"非零退出 N 条"，**一个中间态的假象**会进版本库。
⇒ **转录统一推迟到 Task 5 Step 5**（那时全链已绿），**只重生成一次**。

本步**只需确认一件事**：新判据没有把**其他**驱动器搞崩——
```bash
python tests/skills/figure-choose/check-house-style.py | tail -2
python tests/skills/figure-choose/fixtures/run-expected.py | tail -2
```
Expected: `RESULT: PASS` · `MISMATCH 0 / 23`

- [ ] **Step 12: 提交**

```bash
git add tests/skills/figure-choose/
git commit -m "feat(m3-style): 共享判据三条 F4 底色 / F5 显式色序 / F6 字体族 + 变异

F5 对现有 python 产物为 FAIL —— 预期之内：H14 尚未在 python 侧落地（Task 4 落地）。
判据能真红 = 本任务的验收，不是缺陷。"
```

---

## Task 4: python 生成器改读表 + `facecolor` + 缺口①（悬空刻度）

**Files:**
- Modify: `tests/skills/plot-python/gen-mcm-style.py`（`ANCHORS` L69–85 · `MPLSTYLE_OVERRIDES` L97–109）
- Modify: `tests/skills/plot-python/check-style-freshness.py`（若派生件集合变化）
- Modify: `.claude/skills/mcm-plot-python/assets/mcm.mplstyle`（**派生件**，由生成器产出）
- Modify: `.claude/skills/mcm-plot-python/assets/mcmplot.py`（**派生件**；散文段 L26–L41 手改有效）

**Interfaces:**
- Consumes: Task 2 的 `mcm-style.json`（`bg` / `series.color` / `lines.linewidth` / `font.*`）
- Produces: `mcm.mplstyle` 新增 **4 条 facecolor 键 + 2 条悬空刻度键**；
  `mcmplot.py` 的 `HOUSE_STYLE` 常量区**保持 11 键不变**
  ⚠️ **本行原写"键数由 11 增到 12+"—— 那句已作废（2026-09-30）**：它与本任务 Step 3 的 Expected（"生成区不变"，且带停手条件）**直接冲突**，
  且 `HOUSE_STYLE` 的 docstring 自述「**规范**在本模块里的镜像」⇒ **把样式表（另一来源）的数塞进去会违反 Global Constraint 8「三种来源不许混标」**。
  实现者按 Step 3 做、保持 11 键，**独立复审判"处置正确"**。**色序值走 `mcm.mplstyle` 的 rcParams，不进 `HOUSE_STYLE`。**

- [ ] **Step 1: 记录基线**

```bash
python tests/skills/plot-python/check-style-freshness.py | tail -2
python -c "import sys;sys.path.insert(0,'.claude/skills/mcm-plot-python/assets');import mcmplot as m;print(len(m.HOUSE_STYLE),'键')"
```
Expected: `RESULT: PASS` · `11 键`

- [ ] **Step 2: 在 `MPLSTYLE_OVERRIDES`（L97–109）追加 6 条**

按现有 `(键, 值, 为什么)` 三元组格式追加 **7 条**：

```python
    ("figure.facecolor",      "white", "§0 交付形态：底色 = 论文底色（白）"),
    ("axes.facecolor",        "white", "§0：同上（否则轴区不是白）"),
    ("savefig.facecolor",     "white", "§0：同上（保存时不许被底座改写）"),
    ("savefig.edgecolor",     "white", "§0：同上（外边）"),
    ("xtick.top",             "False", "H10：底座 science 自带 xtick.top=True ⇒ 关掉 spines 后会留悬空刻度"),
    ("ytick.right",           "False", "H10：同上（底座 science 自带 ytick.right=True）"),
    # ★ H14：必须是显式色序 —— 今天本件**没有** prop_cycle 覆盖，python 用的是底座/默认色序，
    #   这在 H14 下是违规的（且 F5 判据正是判它）。色值**从 mcm-style.json 取，不许手写第二份**。
    # ★★ hex 必须**不带 `#`**（带 `#` 会被 mplstyle 当注释 ⇒ 静默解析失败、色序不变）。
    ("axes.prop_cycle",       "cycler('color', SERIES_COLORS_NO_HASH)",
                              "H14：显式色序（值来自 mcm-style.json 的 series.color，**去掉 # 前缀**）"),
```

★ **`SERIES_COLORS` 的取法**：在 `gen-mcm-style.py` 顶部读一次 Task 2 的派生件（与 `check-figure-style.py` 的读法**同源**）：

```python
import json as _json
_TBL = _json.loads((ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json").read_text(encoding="utf-8"))
SERIES_COLORS = next(e["value"] for e in _TBL["entries"] if e["id"] == "series.color")
```

**★★ 已实测的两个坑（2026-09-30，控制者当场跑出来的，别重踩）**：

1. **hex 一律不带 `#`**。matplotlib 的 mplstyle 解析器**把 `#` 当注释起始** ⇒
   `axes.prop_cycle: cycler('color', ['#E69F00', …])` **解析失败**，而**失败是静默的**
   （只往 stderr 打一条 `Bad value in file …`，`rcParams` **保持原值** = 底座色序）。
   ⇒ **必须写成不带 `#` 的形式**（SciencePlots 自己就是这么写的：`science.mplstyle:6` 是 `'0C5DA5'`）。
   实测对照：不带 `#` ⇒ 读回**逐位等于 H14**；带 `#` ⇒ 读回仍是 science 的七色。
2. **★ 因此必须加一条断言**（这条是硬要求）：
   ```python
   # 设完之后当场读回、断言它就是那一串 —— 因为"设不上"在这里是静默的
   from matplotlib import cycler
   _want = cycler("color", SERIES_COLORS)
   assert list(plt.rcParams["axes.prop_cycle"]) == list(_want), \
       f"prop_cycle 没落上（静默失败）：得到 {plt.rcParams['axes.prop_cycle'].by_key()['color']}"
   ```
   放在 `apply_style()` 里 `plt.style.use(...)` **之后**。**没有这条断言，"色序没落上"会一路没人发现**。

⚠️ `render_mplstyle_body()`（L147–152）**怎么渲染值、就按它的实际行为写** —— 实现者须**实测读回**，
不许只看生成的文本长得对。

- [ ] **Step 3: 重跑生成器并核产物**

```bash
python tests/skills/plot-python/gen-mcm-style.py
git diff --stat .claude/skills/mcm-plot-python/assets/
```
Expected: `mcm.mplstyle` 增加 **7 行**；`mcmplot.py` 的生成区**不变**（本次没动 `ANCHORS`）
**★ 若 `mcmplot.py` 也变了 ⇒ 停手查清**（不该变）

- [ ] **Step 3b: ★ 处理"色序变了 ⇒ 入库产物与证据件都变"（本计划最容易漏的一步）**

**三个后果，逐个处置**：

1. **GREEN 产物是入库二进制、且是用 `mcmplot` 出的** ⇒ `axes.prop_cycle` 一落地，它们的**字节就变**：
   ```bash
   # 逐个重跑场景脚本（从仓根跑；它们各自独立出图）
   for d in tests/skills/plot-python/green/out-G1 tests/skills/plot-python/green/out-G2 tests/skills/plot-python/green/out-G3; do
     (cd "$d" && python make_figure.py) || echo "FAIL $d"
   done
   git status --short tests/skills/plot-python/green/
   ```
   ⇒ **预期看到 `figure.png` / `figure.pdf` 变**。**变是应该的**（H14 落地了），提交时**在提交信息里写清"GREEN 产物因显式色序落地而重生成"**。
2. **RED 产物不应变**（写手产出物，`make_figure.py` **不 import 本 skill 的任何东西** —— 已有独立的 grep 证据）：
   ```bash
   for d in tests/skills/plot-python/red/out-R1 tests/skills/plot-python/red/out-R2 tests/skills/plot-python/red/out-R3; do
     (cd "$d" && python make_figure.py) || echo "FAIL $d"
   done
   git status --short tests/skills/plot-python/red/
   ```
   ⇒ **预期：只有 `make_figure.py` 之外的东西不动、图件一字不变**。
   **★ 若 RED 的图件也变了 ⇒ 停手报 BLOCKED**（说明 RED 并不独立于本 skill，那会推翻 RED 的隔离性主张）。
   ⚠️ **RED 的判词列表会变**（多出 F4/F5 两条 FAIL）—— 但那是**证据件的内容**，**不许手改**：
   走生成器（`python tests/skills/plot-python/make-evidence.py`）重跑。
3. **两端都重跑证据件**：
   ```bash
   python tests/skills/plot-python/make-evidence.py
   git diff --stat tests/skills/plot-python/red-green-evidence.md
   ```
   ⇒ 复查 diff：**只该是判词列表的增补与随之平移的行号**，**不应有结论反转**（RED 仍全红、GREEN 仍全绿）。
   **★ 若出现结论反转 ⇒ 停手报 BLOCKED**（要么 H14 把 GREEN 判红了、要么判据写错了）。

- [ ] **Step 4: 证派生件真的修好了缺口①（悬空刻度）**

```bash
python - <<'PY'
import sys, pathlib, tempfile
sys.path.insert(0, '.claude/skills/mcm-plot-python/assets')
import matplotlib; matplotlib.use("Agg")
import mcmplot as m, matplotlib.pyplot as plt
m.apply_style()
fig, ax = plt.subplots(figsize=m.figsize_for(6.31))
ax.plot([0, 1], [0, 1])
out = pathlib.Path(tempfile.mkdtemp()) / "probe.png"
m.save(fig, out, 300)
import fitz
from PIL import Image
# 断言：上边与右边**没有**刻度墨迹（悬空刻度的直接证据）
im = Image.open(out).convert("RGB")
w, h = im.size
top = sum(1 for x in range(w) if im.getpixel((x, 2)) < 200)      # 顶边内 2px 的非白像素数
right = sum(1 for y in range(h) if im.getpixel((w - 3, y)) < 200)  # 右边内 3px
print("top_dark =", top, "right_dark =", right)
assert top == 0 and right == 0, "仍见悬空刻度的墨迹"
print("OK 悬空刻度已消失")
PY
```
Expected: `top_dark = 0 right_dark = 0` + `OK 悬空刻度已消失`
**★ 若不为 0** ⇒ 说明 `xtick.top`/`ytick.right` 不是唯一来源，**停手报 BLOCKED 并附读数**（不许改判据凑绿）。

- [ ] **Step 5: 改 `mcmplot.py` 的『已知缺口』散文段（L38 起的那条处置掉）**

把 **L33–L37** 的「上/右悬空刻度」那一条**改成处置记录**（散文在生成标记**之外**，手改有效、生成器原样保留）：

```markdown
- ~~**上/右悬空刻度（底座副作用）**~~ **已处置**：底座 `science` 自带 `xtick.top: True` / `ytick.right: True`，
  而本件原先只关 `axes.spines.top/right` ⇒ 留出悬空刻度。现已在 `mcm.mplstyle` 显式置
  `xtick.top: False` / `ytick.right: False`。**证据**：判据脚本断言顶边/右边 2–3 px 内无刻度墨迹（见 Task 4 Step 4）。
```

- [ ] **Step 6: 跑新鲜度守卫（★ 它必须证明生成器原样保留了新散文）**

```bash
python tests/skills/plot-python/check-style-freshness.py | tail -4
```
Expected: `PASS  A1 …` `PASS  A2 …`（两份派生件各两条）· `PASS  FON …` · `RESULT: PASS`
**★ 若 A1 红** ⇒ HEAD 里的旧版本与重放结果不同 ⇒ **这正是"先提交再证不动点"的节奏问题**，见 Step 8。

- [ ] **Step 7: 重生成证据件**

```bash
python tests/skills/plot-python/gen-plot-style-verify.py
git status --short
```
Expected: 只有 `plot-style-verify.txt` 与两份派生件在列

- [ ] **Step 8: 提交，然后**在干净树上再跑一次证不动点（★ 硬纪律 10）**

```bash
git add .claude/skills/mcm-plot-python/assets/ tests/skills/plot-python/plot-style-verify.txt
git commit -m "fix(m3-plot): 缺口① 悬空刻度（显式关 xtick.top/ytick.right）+ 底色 facecolor 落地"
python tests/skills/plot-python/check-style-freshness.py | tail -1     # 期望 RESULT: PASS
python tests/skills/plot-python/gen-plot-style-verify.py && git diff --stat   # 期望：无输出（不动点）
```
Expected: `RESULT: PASS`；第二条命令 `git diff --stat` **无输出**（逐字节不变）

---

## Task 5: 缺口②（描白边抬高 PNG 的 F2）与 `M3-plot-gap` 收口

**Files:**
- Modify: `tests/skills/plot-python/make-evidence.py`（L259 附近的 `edgecolor="white"`；**★ 另见下方「本任务的硬性阻塞项」**）
- **`tests/skills/plot-python/red/out-R1/make_figure.py:132` · `red/out-R2/make_figure.py:130`** —— ⚠️ **本行原列在"要改"里，已作废（2026-09-30）**：
  它们**是 RED 语料**，而**同一任务的 Step 2 明写"不许改 RED 语料（写手产出物，手改 = 造伪）"** ⇒ **两句话头直接冲突**。
  处置改为"**不动 RED**"，缺口由**判据侧**（`F4`/`F5`）与**新增的 skill 侧禁令**共同承重（见 Step 2）。
  ⇒ **本任务对这两件应"只读不改"**；**若你发现非改它们不可，停下来报 BLOCKED 并说明为什么。**
- Modify: `.claude/skills/mcm-plot-python/assets/mcmplot.py`（散文段 L38–L41 处置记录）
- Modify: `tests/skills/plot-python/red-green-evidence.md`（证据件，由生成器/重跑产出）

**★★ 本任务的硬性阻塞项（Task 4 复审加的，**不是"可以顺带"**）**：`make-evidence.py` 的 `CRIT` **没同步 Task 3 新加的三条判据**。
- 根因：`CRIT` **6 条**，而解析器按任意 `PASS/FAIL <ID>` 抓到 **9 条** ⇒ `len(c)==len(CRIT)` = `9==6` **恒 False**。
- 后果（**同根因、已实测四处，不止一处**）：
  ① `red-green-evidence.md:361` 印 **`GREEN | 0 | （无） | 0/6`**（而 12 个原始块里 GREEN **全 `RESULT: PASS`**）；
  ② `:14` 印 **`判据 6 条 × 12 张`**（实为 **9 条**）；
  ③ §3 表头与 §3.1 明细**只列到 `F1..F3d`** ⇒ **F4/F5/F6 被静默丢掉**；
  ④ RED 红格数 **28** 漏了 F5/F6（真值 ≈ **37** = 28 + F5 红 6 张 + F6 红 3 张）。
- **这是第 1 号病灶（"声明比事实大"）在入库件里的活体。**
- **要做**：① **把判据总数参数化**（用 `len(c)`），**不许再写死"6 条"**；② 汇总表按 `CRIT` 的键算（复审同意实现者建议的那一行改法）；
  ③ 改完**重生成**该证据件，并核**汇总口径与 12 个原始块自洽**（"全绿图数"必须等于原始块里 GREEN 全 PASS 的张数）。
- **判据**：改完后**不许**再出现任何"某个数字与我当场跑出来的不一致"的行。

**Interfaces:**
- Consumes: Task 4 的派生件；Task 3 的 `F4/F5`
- Produces: 两条缺口**都已处置并各有证据**；`mcmplot.py` 的『已知缺口』段只剩真正的缺口

- [ ] **Step 1: 先测出"描白边"到底抬多少（**先量再改**）**

```bash
python - <<'PY'
# 同一份数据、同一张图，唯一变量 = edgecolor
import sys, pathlib, tempfile
sys.path.insert(0, '.claude/skills/mcm-plot-python/assets')
import matplotlib; matplotlib.use("Agg")
import mcmplot as m
import matplotlib.pyplot as plt
from PIL import Image
out = pathlib.Path(tempfile.mkdtemp())
for tag, ec in (("with-white-edge", "white"), ("no-edge", "none")):
    m.apply_style()
    fig, ax = plt.subplots(figsize=m.figsize_for(6.31))
    ax.barh([0, 1, 2], [3, 5, 4], color=["#E69F00", "#56B4E9", "#009E73"],
            edgecolor=ec, linewidth=0.6 if ec != "none" else 0)
    ax.set_xlabel("Value (unit)"); ax.set_ylabel("Group")
    p = out / f"{tag}.png"; m.save(fig, p, 300); plt.close(fig)
    im = Image.open(p).convert("RGB").resize((320, 320), Image.NEAREST)
    tot = 320 * 320; keep = {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24: continue
        keep[(r // 16, g // 16, b // 16)] = keep.get((r // 16, g // 16, b // 16), 0) + cnt
    print(tag, "F2 =", sum(1 for c in keep.values() if c / tot >= 0.005), "→", p)
PY
```
Expected: 两个读数**必须不同**（这正是缺口②的定义）。**把这两个数写进 Step 4 的处置记录**。

- [ ] **Step 2: 处置它 —— 明确"谁负责"（**含用户点名要加的那条 skill 侧禁令**）**

**本任务的处置 = 三件事**：① 把这条缺口从"未处置"改成"**已定性 + 有 owner + 有机械依据**"；
② **★ 再加一条 skill 侧的使用禁令**（**用户 2026-09-30 裁** —— 原先只做了"定性 + 判据侧承重"，用户要求**源头也拦一道**）；
③ **不许**在场景脚本里一键删掉描边（RED 语料是**写手产出物**，手改 = 造伪，见 `tests/m3-plot-recon/README.md` 的先例）。

**★ ②的落点与要求**：在 `.claude/skills/mcm-plot-python/references/workflow.md`（**或 `SKILL.md` 的边界段**，你按哪个更合适定、并说明）
加一条**给用的人看的禁令**：**条/柱`不要描白边`**，并**写清为什么**（抗锯齿边与白底混出浅色 ⇒ **在 PNG 上把 F2 抬高一档**，而那张图的 PDF 不会）。
⚠️ **这条禁令本身也要能被推翻**：附一条能跑的复算命令（或指向 Task 5 Step 1/3 的那份两态读数）。
⚠️ **同时把这条禁令纳入"可被推翻"的范围** —— 它属"声明"，不是"装饰"。

在 `.claude/skills/mcm-plot-python/assets/mcmplot.py` 的 **L38–L41** 把该条改写为：

```markdown
- **描白边会抬高 PNG 的 F2**（**已定性，改由判据侧承重**）：条/柱描白边时抗锯齿边与白底混出浅色，
  在 PNG 上把 F2 抬高一档（实测两态读数见 `tests/skills/plot-python/red-green-evidence.md`）。
  **处置**：**不改 RED 语料**（写手产出物，手改 = 造伪）；改由 `check-figure-style.py` 的
  **F4/F5** 与 `green/out-G*/make_figure.py` 已去掉描边这一事实共同承重。
  **owner** = `mcm-plot-python` 后续任何改动 F2 口径的任务。
```

- [ ] **Step 3: 在证据件里留可复导的读数**

把 Step 1 的两个读数用**同一套仪器**再跑一遍，通过 `tests/skills/plot-python/make-evidence.py` 的既有机制写进
`red-green-evidence.md`（**照它现有的 `edgecolor` 探针段落**，见 `make-evidence.py:238` 的函数 docstring 与 `:259`）。
⚠️ **不许手改 `red-green-evidence.md`** —— 它是生成件；改的是生成器、然后重跑。

```bash
python tests/skills/plot-python/make-evidence.py
git diff --stat tests/skills/plot-python/red-green-evidence.md
```

- [ ] **Step 4: 收口 `M3-plot-gap`**

确认两条缺口**都已处置**后，更新 `docs/mcm-suite-todo.md` §H.2 的 `M3-plot-gap` 行状态为「**已处置**」，
并指向两处证据（Task 4 Step 4 的悬空刻度断言 + 本条的两态读数）。
⚠️ 行号已变过多次 ⇒ **用 `git grep -n "^| M3-plot-gap" docs/mcm-suite-todo.md` 定位**，**别写死行号**。

- [ ] **Step 5: 全链三件套整跑**

```bash
python tests/skills/figure-choose/check-house-style.py | tail -2
python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"   # 合计行不是末行
python tests/skills/figure-choose/fixtures/run-expected.py | tail -2
python tests/skills/plot-python/check-style-freshness.py | tail -1
python tests/skills/plot-python/mutate-plot-style.py | tail -2
```
Expected: 全绿（具体判词以各驱动器**现算**为准，**不许把总数写死进文档**）

**★ 并在此刻（全链已绿）重生成全部入库判词转录 —— 这是唯一一次**：
```bash
python tests/skills/plot-python/gen-plot-style-verify.py
python tests/skills/figure-choose/gen-house-style-verify.py
python tests/skills/figure-choose/gen-chart-types-verify.py
python tests/skills/figure-choose/gen-skill-verify.py
python tests/skills/figure-choose/gen-pointer-verify.py
git status --short
```
⚠️ **必须遵守硬纪律 10 的节奏**：**先干净 → 再捕获 → 再提交 → 再跑一次证不动点**。
⇒ 现在（干净树上）跑第一遍并**入库提交**，**提交之后**再各跑一遍，`git diff` 必须为空（逐字节不变）。
**★ 若第二遍不同 ⇒ 停手报 BLOCKED**（那是"证据件记录自身工作树状态"的经典陷阱）。

- [ ] **Step 6: 提交**

```bash
git add .claude/skills/mcm-plot-python/assets/mcmplot.py tests/skills/plot-python/ \
        tests/skills/figure-choose/ docs/mcm-suite-todo.md
git commit -m "fix(m3-plot): 缺口② 描白边抬 F2（已定性 + 判据侧承重）+ M3-plot-gap 收口

含全链全绿后唯一一次转录重生成（figure-choose 侧 5 份）。"
```

---

## Task 6: 全库残留回扫与文档收口

**Files:**
- Modify: `docs/mcm-suite-todo.md`（§H.1 / §H.2 / 新 §H.5）
- Modify: `docs/superpowers/specs/2026-09-30-m3-style-single-source-design.md`（把"任务分解"落成"已执行"）
- Modify: `.claude/skills/mcm-figure-choose/references/chart-types.md`（**H 清单 13 → 14**）
- Test: 全库 grep

**★ 本任务必须认领 `chart-types.md` 的 H 清单漂移**（Task 1 复审点名，原计划**无人认领** ⇒ 复审判它会"**安全穿过整个计划**"）：
`chart-types.md` 有两处枚举停在 `H13` —— 其一列"… 字号线宽 `H12` · 参照分布的地位 `H13`"，其二写"本文件不重述 `H1–H13` 的任何规则与数值"。
新增 `H14` 后**两处都不再完备**，而**无任何守卫抓它**（复审实测：把副本里的 `H13` 全改成 `H99`，`check-house-style.py --ct <副本>` 仍 `RESULT: PASS`）。
⇒ 复核并补齐这两处，**并如实记下"今天是靠人读发现的，不是靠判据"**。

**Interfaces:**
- Consumes: Task 1–5 的全部产出
- Produces: 一份**逐件分类表**（同 §H.1.1 的形态：**两把钥匙、各自声明键与计数、各一条命令可推翻**）

- [ ] **Step 1: 全库回扫"述说今天真仓状态"的过期陈述**

```bash
git grep -nE "扫到 6 个[ ]?skill|绘图家族 1[ ]个|5[3]/5[3]" -- .
```
⚠️ **模式串刻意用 `[ ]?` 拆分，免得这一行自己变成新的命中**（§H.1.1 的先例）。
Expected: 逐条判"拿今天的事实去核会不会判定为假" ⇒ **必须归零的**当场改；**幸存的**逐条登记（类别 + 为什么今天读它不是假的 + 复核命令）。

**★★ 本任务新增的一整个类别（2026-10-01 实测，原计划未预见）：变异总数的现取值已从 `53` 变成 `58`。**
Task 2/3 加了 `M54`–`M57`、Task 3b 加了 `M58` ⇒ **驱动器现算合计行是 `MUT: 58/58 达预期（合计）`**（**合计行不是末行**：末行是「（本驱动器共…）」括注，`tail -1` 取到的是它；须 `python tests/skills/figure-choose/mutate-figure-style.py | grep "达预期（合计）"`，约 225 s）。
而 `53/53` 这个字面**写本计划时（2026-09-30）还挂在 5 处**（`docs/mcm-suite-todo.md` 3 处 + `plans/2026-09-29-m3-plot-python.md` 1 处 + 本设计件 1 处）——**这是写计划时的快照；收口后的现取值以 `docs/mcm-suite-todo.md` §H.5 C 表（自带命令）为准，本行不写死**——
**其中 §H.1.1 当初把它登记成"现取值（非残留）"，那时是对的**。
⇒ **本任务必须逐处重判**：**该归零的**（述说现状的句子）改掉；**逐字 stdout 捕获**的**不许手改**
（只能重跑重捕获，见 `tests/m3-plot-recon/README.md` 的先例）；**历史叙述**的加时点。
⚠️ **并重算 §H.1.1 那个"现取值 N 处"的计数**（它自带一条命令）——**别让它悄悄变成假的**（这正是 `M3-plot-T7c` 那一型的复发点）。
⚠️ **另核 `4[6]/4[6]` / `5[2]/5[2]` 那两条老钥匙是否仍成立**（本线没动它们，但**要复算，不许假设**）。

**★★ 另一条要一并登记的（2026-10-01 新增）**：**本仓的颜色距离数有两把尺子**（欧氏 RGB 与 CIE76，**同一对色差好几倍**，
且 H14 的"最紧一对"在不同尺子下会**翻转结论**）⇒ 本任务**顺带把这条口径登记进 `lessons` 或 `docs`**：
**凡写颜色距离数，必须写明是哪把尺子；别把两套的数并置比较**（通则 13 的同族）。

- [ ] **Step 2: 复算两把钥匙的等式**

```bash
git grep -nE "扫到 5 个[ ]?skill" -- . | wc -l
git grep -nE "绘图家族[ ]0[ ]个" -- . | wc -l
git grep -nE "4[6]/4[6]" -- . | wc -l
git grep -nE "5[2]/5[2]" -- . | wc -l
```
**★ 并把去重并集与分类表行数逐一对应**（双向无剩余）——这是 §H.1.1 建立的可推翻口径，**必须照做**。
⚠️ **注意分档**：有些命中是**逐字 stdout 捕获**（判"不许手改"，只能重跑重捕获）、有些是**历史叙述**。

- [ ] **Step 3: 把新的分类表落进 `docs/mcm-suite-todo.md`**

新增 **§H.5**（或并入 §H.1.1），含：**两把钥匙各自声明键与计数** + **逐件分类表**（位置 / 类别 / 为什么今天读它不是假的 / 复核命令）。
⚠️ **不许让"行数 == N"那个等式悄悄变成假的** —— 加了行就要重算，并写清两个数各说的是什么（通则 13）。

- [ ] **Step 4: 更新 §H.1 的 M3 剩余表**

把 `mcm-plot-python` 之外的状态改成今天的事实；把本设计线的完成情况记上；**下一步**指向 `mcm-plot-matlab` 的本体设计。

- [ ] **Step 5: 提交**

```bash
git add docs/
git commit -m "docs(todo): 样式单源线的全库残留逐件分类 + §H.1 状态推进"
```

---

## 明确**不在**本计划内（各自另有归属）

- **`mcm-plot-matlab` 模块本体**（设计 + 计划 + Task 1..N）—— 在它自己的计划里；本计划为它定死了生成器契约（design §6.2）。
- **origin 列填值** —— 等 Origin 载体侦察回来后另起。
- **跨载体一致性判据**（同数据同场景两载体对比）—— **待 matlab 建成**才能比。
- **H11 族（网格 / 图例 / 双 Y 轴）** —— 规范明确不覆盖。
