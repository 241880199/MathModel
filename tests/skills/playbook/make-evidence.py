#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3（`mcm-playbook`）：生成 `tests/skills/playbook/PLAYBOOK-evidence.md`（RED × GREEN 对照证据）。

用法：  python tests/skills/playbook/make-evidence.py

## 它做什么

**同一件事、同一把尺**地量两侧，并把读数**机器抽取**成对照表（不手抄）：

- **同一件事**：`tests/skills/playbook/red/brief.md`（唯一一份，RED 与 GREEN 逐字共用）。
- **同一把尺**：`tests/skills/playbook/check-playbook.py`（判据 `T1`–`T5`）。**两侧同一组参数**：
  `--index` / `--skills-root` 都取默认（**同一份**官方事实基线与同一个 skill 根）；
  `--skill-md` / `--timeline` / `--mistakes` 各指向**该侧自己的产物集** ——
  GREEN = 本 skill 的三份文档；RED = 写手产出的那份 `schedule.md`（一份文件填三个角色）。
- **判据清单现取**：从检查器输出里读 `PASS|FAIL  <id>` 行得到 id 集合，**不写死条数**
  （先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。

## 本文件必须如实写清的四件事

1. **RED 是自变量**：`red/out-R{n}/schedule.md` 是写手的字节（照实入库，本轮未改）。
2. **RED 的红逐条点名**（哪条判据、什么读数、为什么、**性质**：真红 / 级联 / 假红已修）—— §5，手写。
3. **RED 的诚实边界**：中性 brief **已经限定**要产出一份赛程表 ⇒ 这轮 RED **测不到**连表都做不出来
   那一类失败。**不声称覆盖全部失败模式。** —— §0 与 §5。
4. **「看一眼」层的替代品**（设计 §4.4 / 计划 P6）：本支**无产物可看** ⇒ 如实标不适用，
   并用**替代品**（把产出的当前阶段动作清单拿给人读、问照这个能做吗）。
   ★ **要写明它是替代品，不是等价物**。 —— §7，手写。

另：**一个折叠进来的修复**（Task 2 复核登记的 Minor）—— `T5` 的 arm C 原**扫到文件尾**（无结束标记），
本支给了结束标记；生成器**当场用工作树版与基线（`e9d8d47`）版各跑一遍两侧**，证明**两侧读数一字未变** —— §8。
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/playbook
REPO = HERE.parents[2]                                   # 仓根
CHECK = HERE / "check-playbook.py"
BRIEF = HERE / "red" / "brief.md"
RED = HERE / "red"
SKILL_DIR = REPO / ".claude/skills/mcm-playbook"
OUT_DOC = HERE / "PLAYBOOK-evidence.md"
SCENES = (1, 2, 3)
NL = chr(10)

# ★ 本任务的**基线 commit**（Task 3 任务书给的那个）。用它、**不用 `HEAD`**：
#   本支自己会改 `check-playbook.py`（arm C 结束标记）⇒ 提交之后 `HEAD` 就变成"改后版"了，
#   拿 `HEAD` 当参照会**在提交前后给出两个不同的读数**（生成器就不动了）。基线是**固定**的。
BASE_REF = "e9d8d47"

# GREEN = 本 skill 本身（SKILL.md 契约 + references/）；★ 不复制副本（副本 = 第二份权威）。
GREEN_DOCS = {
    "skill_md": SKILL_DIR / "SKILL.md",
    "timeline": SKILL_DIR / "references/timeline.md",
    "mistakes": SKILL_DIR / "references/phase-mistakes.md",
}

# ★ 检查器的**两条默认源**（工作树版靠自推仓根得到）。给落在 `build/` 的基线版副本**显式钉住**用
#   —— 见 `verdicts_only` 的 docstring：副本目录深度不同 ⇒ 自推 `ROOT` 会偏 ⇒ 默认源会指到仓外。
PIN_INDEX = REPO / "corpus/official/INDEX.md"
PIN_SKILLS_ROOT = REPO / ".claude/skills"

LINE_RE = re.compile(r"^(PASS|FAIL)\s+(\S+)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)? *$")
HOUR_RE = re.compile(r"(\d+(?:\.\d+)?)\s*小时")


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(cwd or REPO))
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + NL
    return out, r.returncode


def git_hash_object(p):
    return run(["git", "hash-object", p])[0].strip()


def red_doc(n):
    return RED / ("out-R%d" % n) / "schedule.md"


def docset_red(d):
    """RED 侧产物集：写手产出的那一份文件**填三个角色**（它只产出了一份）。"""
    return {"skill_md": d, "timeline": d, "mistakes": d}


def _argv(checker, docs):
    def rel(p):
        return p.relative_to(REPO).as_posix() if p.resolve().is_relative_to(REPO) else str(p)
    return [sys.executable, rel(checker),
            "--skill-md", rel(docs["skill_md"]),
            "--timeline", rel(docs["timeline"]),
            "--mistakes", rel(docs["mistakes"])]


def check(docs):
    cmd = _argv(CHECK, docs)
    out, rc = run(cmd)
    cells, order, result = {}, [], None
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1) == "PASS", m.group(3).strip())
            order.append(m.group(2))
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
    return {"cmd": " ".join(cmd), "stdout": out.rstrip(NL), "rc": rc,
            "cells": cells, "order": order, "result": result}


def verdicts_only(checker, docs, pin_sources=False):
    """跑检查器、只取 `id → PASS|FAIL`（不取逐条判词）。

    ★ `pin_sources=True` 时**显式**给 `--index` / `--skills-root`（`PIN_INDEX` / `PIN_SKILLS_ROOT`）——
    给**落在 `build/` 的基线版副本**用：副本与工作树版**目录深度不同**，副本自推的 `ROOT`（`parents[3]`）
    **不再是仓根**，于是它那两条**默认**源会指到仓外 ⇒ 两个侧就不在同一份源上比了。
    钉住的**值 = 工作树版默认读的那同两份**（同值，只是从"默认"变"显式"）。
    """
    argv = _argv(checker, docs)
    if pin_sources:
        argv += ["--index", str(PIN_INDEX), "--skills-root", str(PIN_SKILLS_ROOT)]
    out, _rc = run(argv)
    v = {}
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            v[m.group(2)] = m.group(1)
    return v


def criteria_ids(*sides):
    """判据清单**现取**（从检查器输出里读 id），**不写死**。"""
    ids = []
    for data in sides:
        for k in data["order"]:
            if k not in ids:
                ids.append(k)
    return ids


def reds(data, crit):
    return [k for k in crit if k in data["cells"] and not data["cells"][k][0]]


def hour_lines(text):
    """机器抽取：所有含 `N 小时` 的行（去重、保序）。"""
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        if HOUR_RE.search(s) and s not in out:
            out.append(s)
    return out


def total_lines(lines):
    """**声明总长**的那一句（口径写死、可复算）：含 `N 小时` **且**（有 `总时长`，**或**同时有 `开赛` 与 `交稿/截止/收稿`）。"""
    return [s for s in lines
            if HOUR_RE.search(s) and ("总时长" in s or ("开赛" in s and re.search(r"(交稿|截止|收稿)", s)))]


def mentions(lines, needle):
    return [ln for ln in lines if needle in ln]


# ---------------------------------------------------------------- 手写块（判断层）
NATURE = """**这一节是判断层，机械判据判不了它。** 下面的**红集是机器抽取**（§2 的 stdout）；**性质判定是人工**，逐条写。

### 逐条点名（判据 · 读数 · 为什么 · 性质）

| 判据 | 谁红 | 读数（§2 原文） | 为什么红 | 性质 |
| :--- | :--- | :--- | :--- | :--- |
| `T1` | R1/R2/R3 | `fail-closed：timeline.md §1 硬时刻表解析不出任何行` | `T1` 的承重结构是 **一个 `## 1.` 小节里、一张带 `YYYY-MM-DD HH:MM` 形态时刻的表**；三份写手稿**有 `## 1.` 小节、也有表**（R1/R2 的 `## 1. 比赛的关键时刻`、R3 的 `## 1. 关键时刻…`，均在 `red/out-R*/schedule.md:9`），但表里的时刻写成**相对小时 + 周四 17:00** 这种钟点（**无年份、非 `YYYY-MM-DD HH:MM` 形态**）⇒ `check-playbook.py` 的 `re.fullmatch(DT, est)` 对每一行都不匹配、`timeline_hard_moments` 返回空表 | **真红（fail-closed 型）** —— 检查器读不出 ⇒ 判红 + `exit 1`（设计 §4.1 的 fail-closed 口径）。★ **不是**设计预期的「写了 96 小时」那一红（见 §6） |
| `T2` | R1/R2/R3 | `fail-closed：phase-mistakes.md 解析不出任何「失误」块` | `T2` 判的是**每条「失误」的出处 `§id`**；三份稿里**一条「失误」块都没有**（brief 只问了赛程，**没问**失误清单）⇒ 无对象可判 | **真红（fail-closed 型）**；★ 根因是**范围**（brief 没要求那份产物），**不是**写手答错 |
| `T3` | R1/R2/R3 | `fail-closed：三份文档里一个 mcm-* skill 名都没抽到` | `T3` 判**点名的 skill 真的存在**。三份写手稿**通篇没点名任何一个 `mcm-*` skill**（它们不讲本套件）⇒ 一个 token 都抽不到 | **真红（fail-closed 型）**；★ **这一条恰好印证设计 §1.1 的正面**：本 skill 的真内容 = **该调哪个 skill 的依赖图**，而写手对着中性 brief **给不出那张图** |
| `T4` | R1/R2/R3 | `fail-closed：timeline.md §1 硬时刻表解析不出任何行` | 与 `T1` **同一个缺口**：§1 那张带绝对时刻的表不存在 ⇒ 北京侧换算无处可比 | **真红（fail-closed 型）**；★ 与 `T1` **共享根因**（不是级联 —— 两条臂各判各的，独立地撞上同一个「表不存在」） |
| `T5` | R1/R2/R3 | `§4 阶段边界理由 0 条逐条带「构造」  <<< §4 未声明阶段表「全是构造」 ；fail-closed：§4 解析不出任何「为何切在…」的理由行 ；fail-closed：phase-mistakes.md 解析不出任何「失误」块 ；fail-closed：phase-mistakes.md 取不到示例评分表那一节` | 三份稿都有阶段表（内容上很像），但**没有一句「构造」标注**、没有为何切在…的理由行、没有失误块、没有评分表限定节 | **真红**（四臂中三臂 fail-closed + 一臂「未声明全是构造」）；★ 根因同上：**标记哪些是构造**这件事只存在于本 skill 的契约里，中性 brief 不会给 |

**★ 别把这五条读成五个独立的缺陷**：它们**根因同源** —— **这份产物不在检查器的输入契约之内**；
但**实测可分两个子族**（分族依据 = 各行「读数」列的 fail-closed 原文，见下）：

- **格式因 —— `T1`/`T4`**：`T1` 的承重形态是**一个 `## 1.` 小节里的一张带 `YYYY-MM-DD HH:MM` 形态时刻的表**；
  三份稿**有 `## 1.` 小节、也有表**（表在，`## 1.` 也在），但表里的时刻写成**相对小时 + 钟点**（无年份）
  ⇒ **时刻单元格逐行不匹配 `DT` 这个形态**（`## 1.` 与表都在，缺的是**绝对时刻形态**）。
  （`T4` 与 `T1` 共用同一张 §1 表 ⇒ **同一格式因**，读数原文都是
  `fail-closed：timeline.md §1 硬时刻表解析不出任何行`。）
- **范围因 —— `T2`/`T3`**：brief **根本没要**失误清单（`T2` 的判对象）与 skill 名（`T3` 的判对象）
  ⇒ 这两条**没有可判的对象**，读空。
- **`T5` 两组因都在**（依 §2 的四臂读数）：三臂读空属**范围因**（没有失误块 / 没有示例评分表节 /
  没有「为何切在…」行），一臂「§4 阶段表未声明『全是构造』」属**格式/标注因**（阶段表有其实、缺契约要求的标注）。

所以：

- **没有级联**（没有哪条红是被另一条红带出来的）：五条臂**各判各的**，每条都在自己的解析面上读空。
- **没有假红已修**：本轮**没有**任何一条红是判据自身的错。（本任务的**唯一**判据改动 = §8 的 `T5` arm C
  结束标记，那**不是**假红修复，且**已实证两侧读数一字未变**。）
- **★ 也别说成写手做得差**：三份稿**都读得懂、都自洽、内容还都正确**（§6）。判据红的是
  **没按本 skill 的契约产出** —— 与先例 `mcm-schematic` 那支「红的是没被告知的约定」是**同一型**。

**本表不声称穷尽**：它只列本支三份 RED 产物**实际触发**的判据，不声明覆盖率。

### ★★ 一条必须写死的实际结果：设计预期的那个红（96 小时）**没有出现**

设计 §4.3 / 计划 P5 预期无材料的写手**大概**会写出流传的 **96 小时**，那恰好是 `T1` 要抓的。
**实测：三位写手全部写了 `99 小时`（就『到停止修改』口径而言的正确值 —— brief 问的「交稿」有两读：本模块时间线里 `开赛→停止修改 = 99` 与 `开赛→提交截止 = 100`，三位都锚在周一 20:00 EST 即 99 那一口径），96 一次都没被采纳。** 详见 §6 的机器抽取。
`T1` 那条红**不是**「抓到 96」，而是**「解析器够不到内容层」** —— 这两件事**不许混为一谈**。"""

LOOK = """**★ 先把这件事说清楚：这一节是「替代品」，不是「等价物」。**

本模块**不产任何产物**（无图 / 无表 / 无代码）⇒ 设计 §4.4 / 计划 P6 的口径是 **「看一眼」层对本支不适用**，
并给一条**替代**：**把产出的当前阶段动作清单拿给一个人读，问照这个能做吗**。
下面就是这条替代品的执行记录。**两层替代必须都标明**：

1. **层本身是替代品**：本支**没有**可供看的东西（不像绘图那支有 PNG 可看）。**不写我们也做了看一眼层。**
2. **读的人也是替代品**：设计说拿给**一个人**读；本任务在后台跑、**够不到人** ⇒ 实际读的是
   一个**干净上下文、非 `fork` 的 `general-purpose` agent**（给了它那份清单的路径 + 一句照这个能做吗）。
   ⇒ 它是**替代品的替代品**：**agent 的判读 ≠ 人的判读**，**只有转录级忠实度**，无沙箱可证。

**被读的那份**：`mcm-playbook` 的输出契约在一张具体赛程上跑出来的当前阶段动作清单
（情景：开赛 2027-01-29 06:00 北京；现在距开赛 **52 小时**；队伍自报「主模型跑通、第一版图表已出、正文未写」）。
★ 那份清单是**本任务照 skill 现场跑的**，**未入库**（它是**跑出来的一次输出**，不是权威件）。

### 读的人的原话（转录；未改）

> 结论一句话：**能照做一半，但主干那条会真卡住，另有两处顺序/锚点会让你现场停下来问人。**

**它判能用的**：输入齐且自洽（01-29 06:00 → 01-31 10:00 = 52 小时算对，与第 52 小时落在阶段 3 一致）；
阶段判定逻辑自洽（按表 = 阶段 3、按进展 = 写作期、两者不打架）；动作 1 给了正文**章节清单**，最可执行；
动作 2/3/4 点名的 skill 都标「已建」、方向清楚；动作 5 提醒「阶段 4 合规自查一票否决」。

**它判会卡 / 要说清的（原话浓缩）**：

1. **核心动作没有已建工具兜底。** 动作 1「写正文主体」是阶段 3 的主干，却只把你推给
   `docs/mcm-writing-discipline.md`；而清单自己承认本阶段本该用的 `mcm-paper-architecture`（页数预算）与
   `mcm-section-writer`（逐节写作）**未建**，**既没给替代技能、也没给「没有它就先怎么干」的降级路径**。
   ★ **2026-10-03 改时点（编辑后加；上一条是读者原话的浓缩，按原样保留、不覆盖旧值）**：
   现值 = `mcm-section-writer`（逐节写作）**已落地**（`.claude/skills/mcm-section-writer/`）⇒
   上面这条判断**关于它的那一半已消解**；`mcm-paper-architecture`（页数预算）**仍未建**，该句对它**仍成立**。
2. **缺「截止时刻 / 剩余总时长」。** 只给了开赛与当前，没给交稿时间；动作 5 却要给阶段 4 留够时间 ⇒ **没法排期**。
3. **动作 1 与动作 2 实际互相依赖，却标按先后**（结果节依赖图表定稿）⇒ 结果节会悬空；每个动作也没有时间盒。
4. **已有第一版图，到底重做还是重画没说**（「先选型再落代码」是**从零**的路径）。
5. **`§` 号锚点两处指向不同对象**（动作 4 明写 `corpus/official/INDEX.md §2.2.8`；§4 三条依据只写 §号、没说哪份文件）。
6. **§4 与 §5 口径打架**：§4 标题「典型失误」读起来像「历史上大家怎么栽」，§5 却声明**不是**历史上大家怎么栽的。

**★ 本层最诚实的读法（别夸大也别埋没）**：

- 读的人**没有指出任何数字错** —— 与 §6 的内容探针一致（这一侧的内容是可核的）。
- 它指出的是**可用性 / 完整性**：**主干缺工具兜底、缺 deadline / 时间盒、依赖顺序没写**。
  ★ **这几点机械判据一条都报不出来**（`T1–T5` 查的是「与官方一致 / 出处理由 / 引用存在 / 换算可复算 / 构造有标注」）
  —— 这正是看一眼层存在的理由（先例：origin 那支的粉边、表格那支的超长表题，判据都不报）。
- ★ **但有几条是「我这份样例清单」的毛病，不是 skill 的判决**：第 2 条（我那份清单没写交稿时刻）、
  第 5 条（我那份清单的 § 号没带文件名）、第 6 条（我那份清单把两节并排摆）——
  **这三条是「我照着 skill 手搓这份样例时」留下的**，**不能记到 `mcm-playbook` 头上**
  （第 6 条尤其：skill 的 `phase-mistakes.md` 里「每条标构造」与「不是历史上大家怎么栽的」是**并存的、刻意的**两侧，
  这里被读成人打架，是**呈现**问题）。
- ★ **反例也要记**：读的人**没有**质疑「第 52 小时落在阶段 3」这类**阶段边界是构造**这一点
  （它默认接受了 50–80 这个切法）—— 说明构造标注**在这一次阅读里没被误解成官方口径**，
  ★ **但这只是 1 个读者 × 1 个情景的读数，不是构造标注已被验证有效**。"""

TARGET = """### ★ 期望 vs 实测（P5 的口径：**预期不等于保证**）

**靶子是现成的**：**96 小时**是流传最广的错说法。**但它的出处要写准**：

- ★ **不是** `corpus/official/INDEX.md`（**当场实测**：`grep -c 96 corpus/official/INDEX.md` ⇒ **0**）。
- ★ 是**本仓自己的** `docs/superpowers/specs/2026-09-22-mcm-skill-suite-design.md:42`
  （原文：**常被引用的「96 小时」与 2027 日期不符**）。**不许**把它归给官方材料。

**实测结果（机器抽取，见下表）**：**三位写手全部给出 `99 小时`**，**没有一位采纳 96**。
⇒ 设计件与计划里那句**大概率他会写出 96 小时**在本轮被推翻。

★ **口径限定**：brief 问的是「开赛 → **交稿**」，而本模块时间线里 `开赛→停止修改 = 99`、
`开赛→提交截止 = 100` 是**两个不同口径**；三位写手都把「交稿」锚在**周一 20:00 EST**（= 停止修改那一口径）。
⇒ 下文说 `99` 为「正确值 / 写对了」，**只在『到停止修改』口径下成立**（若按「到提交截止」口径，对应值是 100）。

★ **处置（照 P5 的硬规定）**：**不调 brief、不换写手、不凑数** —— **照实记**。
写手**在『到停止修改』口径下**写对了，**本身就是一个有意思的读数**：它说明在本机这个模型上，
**美赛赛程 = 周四 17:00 EST 开赛 → 周一 20:00 EST 收稿 = 99 小时**这条知识是有的，
⇒ 本支 RED **没能**在总时长这一格上制造出设计预期的红。

★ **同时要照实说清为什么 `T1` 抓不到**：`T1` 的时长臂要读的是 `开赛 → 停止修改 = N 小时` 这种**契约形态**，
写手稿里**没有**这种串 ⇒ **就算写手真的写了 96，`T1` 这一轮也够不到它**
（它只会先 fail-closed 在 §1 那张表上）。**`T1` 抓 96 这件事的真实证据在别处**：
`mutate-playbook.py` 的 `MUT-T1a`（把 `timeline.md` 的 99.0 改成 96.0 ⇒ `T1` **真红**，见 §8）。
⇒ 别把这两件事混为一谈：**本支 RED 证明的是契约外产物全臂 fail-closed，不是 `T1` 抓到 96**。"""

GENERATOR_TAIL = """## §8 生成器 · 判据非空泛 · 折叠进来的修复 · 不动点

- 本文件的机器部分由 `tests/skills/playbook/make-evidence.py` **当场跑** `check-playbook.py` 生成
  （`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout（§4）。
- ★ **判据非空泛（失败方向的另一条臂）**：`mutate-playbook.py` 的读数收在此处（**本生成器不执行该驱动器**，
  故**不声称当场跑过**；复跑命令见本节末）。它证明 `T1`–`T5` **逐条都能真红**、
  fail-closed 两条真红、4 条射程边界对照必须绿，**合计 `16/16`**。

### ★ 折叠进来的修复：`T5` 的 arm C 加结束标记（Task 2 复核登记的 Minor）

- **原状**：`check_t5` 的 arm C 用 `section(ms_text, "## 关于那份")`（**无结束标记**）⇒ **扫到文件尾**。
  两条官方限定串（`A Sample` / `adjusting categories and points as needed`）于是被**在小节之外**也搜索
  ⇒ 若将来在后面的小节里复述它们，这一臂会**为错误的理由通过**。
- **本支的处置**：给结束标记 `## `（= 下一个**顶层** `## ` 小节）⇒ **把搜索面收进小节内**。
  该小节当前是**最后一节** ⇒ 干净文档上的读数**不变**。
- ★ **实证（不是推理）**：生成器**当场用工作树版与基线 `e9d8d47` 版各跑两侧**（§0 末的对照块），
  **逐一比较判据判定** ⇒ **RED 三份、GREEN 一份，四份的判定完全一致**。
  ⇒ **这个修复对本文档里的任何读数都是零影响**；它防的是**将来**。
- ★ **不声称穷尽**：只验证了在**当前**这份 `phase-mistakes.md` 与三份 RED 稿上两侧同判，
  **没有**对「将来若真的在别处复述那两条串」做端到端复现（那时正是这条修复要挡的场面）。

### 不动点

在**已提交的树上**重跑本生成器 ⇒ 本文件**逐字节不变**（证法：跑后 `git status --short` 仍为空）。

```text
$ python tests/skills/playbook/mutate-playbook.py   # 快照，非生成时现跑
MUT: 10/10 红（判据 T1–T5 逐条打红）
MUT: 2/2 红（fail-closed）
MUT: 对照 4/4 达预期（必须绿）
MUT: 16/16 达预期（合计）
```

★ 其中与本支 RED 最相关的两条：`MUT-T1a`（时长 99.0 → **96.0** ⇒ `T1` 真红）——
**这才是 T1 抓得到 96 的证据**（不是本支的 RED）；`MUT-FC1`（`--timeline` 读不出 ⇒ `T1,T3,T4,T5` 真红）——
**这才是 fail-closed 真的是红的证据**（本支 RED 的红全是 fail-closed 型，靠它背书）。"""


def main():
    red = {n: check(docset_red(red_doc(n))) for n in SCENES}
    green = check(GREEN_DOCS)
    CRIT = criteria_ids(red[1], red[2], red[3], green)
    # ★ 这一行是**故意的 tripwire**，**不是**"写死条数"的反例：判据清单本身是**上一行现取**的
    #   （`criteria_ids(...)` —— 从检查器 stdout 读 `PASS|FAIL <id>`，见 §0 与硬要求 3）；
    #   本行只把"现取到的东西"钉在**本支已知的这 5 条**上：一旦上游增/删判据，宁可**当场炸**请人来核，
    #   也**不**静默跟着变（否则 §4/§4.2 那几张汇总表会在判据增减时**悄悄漂移**）。
    #   ⇒ 现取路径在**上一行**；本行是它的**响闸**，不是它的替代。
    assert CRIT == ["T1", "T2", "T3", "T4", "T5"], "判据清单变了：%s" % CRIT
    for n in SCENES:
        assert set(red[n]["cells"]) == set(CRIT), (n, sorted(red[n]["cells"]))
        assert reds(red[n], CRIT) == CRIT, "R%d 红集变了：%s" % (n, reds(red[n], CRIT))
    assert set(green["cells"]) == set(CRIT), sorted(green["cells"])
    assert reds(green, CRIT) == [] and green["result"][0], "GREEN 非全绿"

    # ---- 基线版（BASE_REF）vs 工作树版：证明 arm C 的修复不改变任何判定 ----
    # ★ 临时件落**仓内 `build/`**（gitignored），**不写进测试目录** —— 先前写在 `tests/skills/playbook/`
    #   时，中断会在被测目录里留一个游离的 `_head_check.py`（Task 3 复核登记的 Minor，本轮修）。
    build_dir = REPO / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    head_tmp = build_dir / "_playbook-head-check.py"
    head_src, _ = run(["git", "show", BASE_REF + ":tests/skills/playbook/check-playbook.py"])
    head_tmp.write_bytes(head_src.replace("\r\n", NL).encode("utf-8"))
    try:
        armc = {}
        for tag, docs in ([("R%d" % n, docset_red(red_doc(n))) for n in SCENES]
                          + [("G1", GREEN_DOCS)]):
            a_, b_ = verdicts_only(head_tmp, docs, pin_sources=True), verdicts_only(CHECK, docs)
            armc[tag] = (a_, b_, a_ == b_)
    finally:
        head_tmp.unlink()

    wt_blob = git_hash_object(CHECK.relative_to(REPO).as_posix())
    hd_blob = run(["git", "rev-parse", BASE_REF + ":tests/skills/playbook/check-playbook.py"])[0].strip()
    same_as_base = (wt_blob == hd_blob)
    red_meta = {}
    for n in SCENES:
        b = red_doc(n).read_bytes()
        red_meta[n] = (len(b), len(b.decode("utf-8").splitlines()),
                       git_hash_object(red_doc(n).relative_to(REPO).as_posix()))
    green_meta = {k: git_hash_object(v.relative_to(REPO).as_posix()) for k, v in GREEN_DOCS.items()}
    brief_bytes = BRIEF.read_bytes().decode("utf-8")

    L = []
    a = L.append
    a("# Task 3 · RED × GREEN 对照证据（`mcm-playbook`）")
    a("")
    a("本文件由 `tests/skills/playbook/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("**§2 / §3 / §4 / §6 是机器抽取**（逐格解析检查器 stdout、逐行扫产物）；")
    a("**§5 的性质判定 · §6 的期望/实测判决 · §7 的看/读记录是手写**（文里已标明）。")
    a("")

    # ---------------- §0
    a("## §0 口径（同一件事 · 同一把尺 · RED 是自变量）")
    a("")
    a("- **同一件事**：`tests/skills/playbook/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联）。")
    a("- **两侧**：RED = **3 位干净上下文写手**（`general-purpose`，**未用 `fork`**）产出的赛程表；"
      "GREEN = **本 skill 本身**（`SKILL.md` 契约 + `references/`），★ **不复制副本**（副本 = 第二份权威）。")
    a("- **同一把尺**：`tests/skills/playbook/check-playbook.py`（判据 `T1`–`T5`）。**两侧同一组参数**："
      "`--index` / `--skills-root` 取默认（**同一份**官方事实基线与同一个 skill 根）；"
      "`--skill-md` / `--timeline` / `--mistakes` 各指向**该侧自己的产物集** —— "
      "GREEN = 本 skill 的三份文档；**RED = 那份 `schedule.md` 填三个角色**（写手只产出了一份文件）。")
    a("- **判据清单现取**：本支 **%d 条**（`%s`）。**不写死条数**"
      "（先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。" % (len(CRIT), "、".join(CRIT)))
    a("- **RED 是自变量**：三份写手稿**照实入库**（本轮未改）。逐件读数：")
    a("")
    a("| 产物 | 字节 | 行数 | 工作树 blob |")
    a("| :-- | --: | --: | :-- |")
    for n in SCENES:
        b, ln_, bl = red_meta[n]
        a("| `red/out-R%d/schedule.md` | %d | %d | `%s` |" % (n, b, ln_, bl[:12]))
    a("")
    a("- **判据对象（GREEN）逐件 blob**："
      + " · ".join("`%s`=`%s`" % (k, v[:12]) for k, v in green_meta.items()))
    a("")
    a("- **检查器自证**：工作树 blob `%s` · **基线 `%s`** blob `%s` ⇒ %s —— "
      "★ **差的就是本支唯一那处改动**（`T5` arm C 加结束标记，§8）。**两侧用的是同一版**（工作树版）。"
      "（★ 参照系取**基线 commit**、**不取 `HEAD`**：本支提交之后 `HEAD` 就等于工作树版了，"
      "拿 `HEAD` 当参照会让本行在**提交前后给出两个不同的读数** ⇒ 生成器就不动了。）"
      "★ 生成器**当场**用基线版各跑一遍两侧、逐判据比对 ⇒ 见本节末两版同判块：**四份判定完全一致**。"
      "（★ 基线版副本落在 `build/`、与工作树版**目录深度不同** ⇒ 其自推仓根会偏；比对时把 "
      "`--index` / `--skills-root` **显式钉住**成工作树版默认读的那同两份，确保两侧在同一份源上比。）"
      % (wt_blob[:12], BASE_REF, hd_blob[:12], "**相同（！）**" if same_as_base else "**不同**"))
    a("")
    a("- ★ **RED 的诚实边界（硬要求 7 / 设计 §4.3）**：中性 brief **已经限定**要产出一份赛程表"
      "（三个必答项：关键节点 / 总时长 / 分阶段表）⇒ 这轮 RED **测不到**连表都做不出来那一类失败"
      "（写不出表、表里空、没有阶段划分）。**不声称覆盖全部失败模式。**")
    a("- ★ **环境旁路**：写手是本机 Claude Code 的 agent，会话级共享上下文里另有两处可见面"
      "（`mcm-playbook` 的**类别名**描述 + 自动注入的 `MEMORY.md`）。"
      "**本次用探针查过：旁路没有泄漏那个时长**（详见 `red/writer-self-reports.md` §4）。")
    a("")
    a("**两版同判（机器抽取；基线 `%s` 版 vs 工作树版，逐判据）**：" % BASE_REF)
    a("")
    a("| 产物 | 基线 `%s` 版判定 | 工作树版判定 | 同？ |" % BASE_REF)
    a("| :-- | :-- | :-- | :-- |")

    def fmt(d):
        return " ".join("%s=%s" % (k, d.get(k)) for k in CRIT)
    for tag in ("R1", "R2", "R3", "G1"):
        ah, bh, same = armc[tag]
        a("| %s | `%s` | `%s` | %s |" % (tag, fmt(ah), fmt(bh), "**是**" if same else "**否**"))
    a("")
    a("⇒ **这个修复对本文档里的任何读数都是零影响**。")
    a("")

    # ---------------- §1
    a("## §1 同一件事（逐字内联；RED 与 GREEN 共用）")
    a("")
    a("```text")
    a(brief_bytes.rstrip(NL))
    a("```")
    a("")
    a("★ **中立性抉择**（硬要求 1）：brief **不含时长**（出现时长本身就污染测试）、**不含年份**"
      "（给了年份会把写手推向回忆那一届的真实日期）、**不含任何来源**（不给 `corpus/official/**`、不给本 skill、"
      "不给判据、不给本任务书）。**唯一**算限定的一句是 **做一份赛程表** —— 它**既是**任务的交付形态，"
      "**也是**本支 RED 的那条诚实边界。")
    a("")

    # ---------------- §2 / §3
    for si, (name, data, tag, keys) in enumerate(
            (("RED", red, "R", SCENES), ("GREEN", {1: green}, "G", (1,))), start=2):
        a("## §%d %s 原始读数（%s）" % (si, name,
          "三位干净上下文写手 · 无 skill" if name == "RED" else "本 skill 本身（契约 + references）"))
        a("")
        for n in keys:
            d = data[n]
            a("### %s%d" % (tag, n))
            a("")
            a("```")
            a("$ " + d["cmd"])
            a(d["stdout"])
            a("[exit=%d]" % d["rc"])
            a("```")
            a("")

    # ---------------- §4
    a("## §4 对照表（机器抽取）")
    a("")
    a("每格 = 状态：绿 = `PASS` / 红 = `FAIL`。逐格解析自 §2/§3 的 stdout；判据 ID 取现行（**现取**，见 §0）。")
    a("")
    a("| 产物 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    rows = [("R%d" % n, "RED", red[n]) for n in SCENES] + [("G1", "GREEN", green)]
    for tag, side, data in rows:
        c = data["cells"]
        row = [tag, side] + ["绿" if c[k][0] else "红" for k in CRIT]
        row.append("PASS" if data["result"][0] else "FAIL")
        a("| " + " | ".join(row) + " |")
    a("")
    a("### §4.1 逐判据判词（机器抽取；判词原文，不手抄）")
    a("")
    a("| 产物 | 侧 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for tag, side, data in rows:
        for k in CRIT:
            cell = data["cells"].get(k)
            if cell:
                a("| %s | %s | %s | %s | %s |" % (tag, side, k, "PASS" if cell[0] else "FAIL", cell[1]))
    a("")
    a("### §4.2 汇总（由 §4 的格子逐格重算）")
    a("")
    a("| 侧 | 产物数 | 红格数（判据 × 产物） | 判红的判据 ID（并集） | 全绿产物数 |")
    a("| :-- | --: | --: | :-- | --: |")
    for side, minset in (("RED", list(red.values())), ("GREEN", [green])):
        allred, ok, total = [], 0, 0
        for data in minset:
            total += 1
            if all(data["cells"][k][0] for k in CRIT) and data["result"][0]:
                ok += 1
            allred += reds(data, CRIT)
        a("| %s | %d | %d | %s | %d/%d |" % (side, total, len(allred),
          "、".join(dict.fromkeys(allred)) or "（无）", ok, total))
    a("")
    a("★ **这张表是契约一致性的读数，不是质量的读数** —— RED 的红**不是**赛程做得差（见 §5、§6）。")
    a("")

    # ---------------- §5
    a("## §5 RED 的红逐条点名（硬要求 5：真红 / 级联 / 假红已修）")
    a("")
    a("（红集**机器抽取**自 §2；性质判定是人工判定，逐条写。）")
    a("")
    for n in SCENES:
        a("- **R%d 红集** = `{%s}`" % (n, ", ".join(reds(red[n], CRIT))))
    a("")
    a(NATURE)
    a("")

    # ---------------- §6
    a("## §6 ★ 内容探针：那个被期待写错、却（在『到停止修改』口径下）写对了的总时长（硬要求 3）")
    a("")
    a(TARGET)
    a("")
    a("### §6.1 机器抽取：三份写手稿里所有含 `N 小时` 的行（逐行扫描产物，**不手抄**）")
    a("")
    for n in SCENES:
        lines = hour_lines(red_doc(n).read_bytes().decode("utf-8"))
        a("**R%d**（%d 行含 `N 小时`）" % (n, len(lines)))
        a("")
        for s in lines:
            a("- `%s`" % s)
        a("")
    a("### §6.2 机器抽取：三份稿里总时长那一句 / 以及所有出现 `96` 的行")
    a("")
    a("| 产物 | 声明总长的行（含 `N 小时` ∧（`总时长` ∨（`开赛` ∧ `交稿/截止/收稿`））） | 含 `96` 的行 |")
    a("| :-- | :-- | :-- |")
    for n in SCENES:
        txt = red_doc(n).read_bytes().decode("utf-8")
        tot = total_lines(hour_lines(txt))
        m96 = mentions(txt.splitlines(), "96")
        a("| R%d | %s | %s |" % (n,
          "<br>".join("`%s`" % s for s in tot) or "（无）",
          "<br>".join("`%s`" % s.strip() for s in m96) or "（无）"))
    a("")
    a("★ **读法（照实）**：三份稿的**总长声明都是 `99 小时`**（见上一列）。"
      "★ **口径限定**：brief 问「开赛 → 交稿」，本模块时间线里 `开赛→停止修改 = 99`、`开赛→提交截止 = 100` 是**两个口径**；三份稿都把「交稿」锚在**周一 20:00 EST**（= 99 那一口径）⇒ 本列读数只说「三份都声明 99」，**不声称 99 是唯一正确值**（按「到提交截止」口径是 100）。"
      "★ 上一列**不是总长一句的精确提取器**：脚注里也提到开赛/收稿的行会被同一条规则一并扫到"
      "（如 R3 那列另有两行是**口径提醒**）—— **本列只保证按这条规则命中的行都在这里，不保证每行都是总长声明**。"
      "`96` 在三份里**都出现过**，但**没有一份把它当成本次比赛的总时长**："
      "R1 是**推导中间量**（「周四 17:00 → 周一 17:00 = 96 小时，再加 3 小时」）；"
      "R2/R3 是**旧制 / 反事实**（「20:00 开赛则为 96 小时」「早期 MCM 是 96 小时制」）。"
      "★ 列 `含 96 的行` 是**逐行机器抽取**，**不区分它在句子里扮演什么角色** —— 角色是人工读出来的（本节两句）。")
    a("★ **本探针不是那把尺**：它是**补充的内容读数**，用**同一份机器抽取规则**扫三份稿的行；"
      "**判据读数以 §2/§4 的 `check-playbook.py` 为准**。")
    a("")

    # ---------------- §7
    a("## §7 「看一眼」层的替代品（硬要求 8 / 计划 P6）")
    a("")
    a(LOOK)
    a("")

    # ---------------- §8
    a(GENERATOR_TAIL)
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace("\r\n", NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO).as_posix(), OUT_DOC.stat().st_size, "B")
    print("criteria %d: %s" % (len(CRIT), CRIT))
    for n in SCENES:
        print("  RED   R%d red: %s" % (n, reds(red[n], CRIT) or "(none)"))
    print("  GREEN G1 red: %s" % (reds(green, CRIT) or "(none)"))
    print("armC two-version same:", {t: armc[t][2] for t in armc})
    print("OK")


if __name__ == "__main__":
    sys.exit(main())
