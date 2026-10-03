#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3（`mcm-topic-select`）：生成 `tests/skills/topic-select/TOPICSELECT-evidence.md`（RED × GREEN 对照证据）。

用法：  python tests/skills/topic-select/make-evidence.py

## 它做什么

**同一件事、同一把尺**地量两侧，并把读数**机器抽取**成对照表（不手抄）：

- **同一件事**：`tests/skills/topic-select/red/brief.md`（唯一一份，RED 与 GREEN 逐字共用）+
  同一组六道题面 `tests/skills/topic-select/red/problems/`（**2025 A–F 的真实题面**，抽取口径见 §0）。
- **同一把尺**：`tests/skills/topic-select/check-topic-select.py`（判据 `S1`–`S6`）。
  **两侧同一组参数**：`--problems` / `--corpus` / `--skill-md` / `--method` 全指向**同一份**；
  只有 `--output` 各指向**该侧自己的产出**（RED = 写手产出的那份 `decision.md`；GREEN = 用本 skill 出的那份）。
- **判据清单现取**：从检查器输出里读 `PASS|FAIL  <id>` 行得到 id 集合，**不写死条数**
  （先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。

## ★★ 两轮 RED（同一 brief，一个变量之差）

- **第一轮（无形态）**：`red/out-R{1,2,3}/decision.md` —— 只给 brief + 六份题面。
  实测：写手产不出承重形态 ⇒ `S1`–`S4` 全在解析层 **fail-closed**（走不到"逐字 vs 改写"那一格）。
- **第二轮（有中性形态）**：`red/out-R{1,2,3}-shape/decision.md` —— 多给一份 `red/neutral-shape.md`
  （**只有形状、无纪律**的空壳）。实测：写手产出了可比结构，`S1` **逐条判红**支撑句（非子串 12/12/12）。
- **两轮都留、都真读数**；各自证明/不能证明什么见 §10。**不许把两轮读成同一件事的两次呈现。**

## 本文件必须如实写清的五件事

1. **RED 是自变量**：两轮的 `decision.md` 都是写手的字节（照实入库，本轮未改）。
2. **RED 的红逐条点名**（哪条判据、什么读数、为什么、**性质**：真红 / 级联 / 假红已修）—— §6，手写。
3. **RED 的诚实边界**：中性 brief **已经限定**要挑一道并说明为什么 ⇒ 这轮 RED **测不到**
   「连推荐都给不出」那一类失败。**不声称覆盖全部失败模式。** —— §0 与 §6。
4. **「看一眼」层的替代品**（设计 §3.3）：本支**无产物可看** ⇒ 如实标不适用，
   并用**替代品**（把产出的「推荐 + 依据」拿给人读、问照这个你能定题吗）。
   ★ **要写明它是替代品，不是等价物**。 —— §8，手写。
5. ★ ★ **本轮测不到的真实赛期情形**：2027 的题**尚不存在**，而**任何真实可得的 MCM 题集（2016–2026）
   都已在语料里** ⇒ 本轮 RED/GREEN **复现不了**「当天新题刚放出、尚不在语料里」那一情形。
   **不声称覆盖真实赛期情形。** —— §0 与 §10。

## 一条并进来的行修正（Task 2 复核留的）

`references/method.md` 的「题标题行」那句原写「后面接**非字母数字字符**或行尾」，与检查器
`PROB_HEAD` 所用 `\\b` 不符（实测 `## 题 A_` 不匹配）。本轮**改文档、不改正则**，并当场证「改文档对
任何判据读数零影响」（§9）。
"""
import importlib.util
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/topic-select
REPO = HERE.parents[2]                                   # 仓根
CHECK = HERE / "check-topic-select.py"
BRIEF = HERE / "red" / "brief.md"
NEUTRAL_SHAPE = HERE / "red" / "neutral-shape.md"
PROBLEMS = HERE / "red" / "problems"
CORPUS = REPO / "corpus/papers"
SKILL_MD = REPO / ".claude/skills/mcm-topic-select/SKILL.md"
METHOD = REPO / ".claude/skills/mcm-topic-select/references/method.md"
OUT_DOC = HERE / "TOPICSELECT-evidence.md"
SCENES = (1, 2, 3)                                       # 第一轮（无形态）
SHAPE_SCENES = (1, 2, 3)                                 # 第二轮（有中性形态）
NL = chr(10)

# ★ 本任务的**基线 commit**（Task 3 任务书给的那个）。用它、**不用 `HEAD`**：
#   本支改动 `method.md`（题标题行那句订正）⇒ 提交之后 `HEAD` 就变成「改后版」了，
#   拿 `HEAD` 当参照会**在提交前后给出两个不同的读数**（生成器就不动了）。基线是**固定**的。
BASE_REF = "5cf6ed2"

GREEN_DOC = HERE / "green" / "out-G1" / "decision.md"
LINE_RE = re.compile(r"^(PASS|FAIL)\s+(\S+)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)? *$")

# 标签 → (产物路径, 侧, 说明)。顺序 = 报告里出现的顺序。
def red_doc(n):
    return HERE / "red" / ("out-R%d" % n) / "decision.md"


def shape_doc(n):
    return HERE / "red" / ("out-R%d-shape" % n) / "decision.md"


def doc_table():
    rows = []
    for n in SCENES:
        rows.append(("R%d" % n, red_doc(n), "RED", "第一轮·无形态"))
    for n in SHAPE_SCENES:
        rows.append(("R%ds" % n, shape_doc(n), "RED", "第二轮·有中性形态"))
    rows.append(("G1", GREEN_DOC, "GREEN", "用本 skill"))
    return rows


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(cwd or REPO))
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + NL
    return out, r.returncode


def _argv(output, method=None):
    """同一把尺同一组参数：只有 `--output`（与 §9 专门用的 `--method`）会变。"""
    def rel(p):
        return pathlib.Path(p).resolve().relative_to(REPO).as_posix()
    return [sys.executable, rel(CHECK),
            "--problems", rel(PROBLEMS),
            "--output", rel(output),
            "--corpus", rel(CORPUS),
            "--skill-md", rel(SKILL_MD),
            "--method", rel(method or METHOD)]


def check(output, method=None):
    cmd = _argv(output, method)
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


def git_hash_object(p):
    return run(["git", "hash-object", str(p)])[0].strip()


def load_checker():
    spec = importlib.util.spec_from_file_location("_ts_check", str(CHECK))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def structure_probe(mod, output, problems_map):
    """机器抽取一份产出里：题小节 / 标签行 / 引文（子串与否）/ 历史行 / 推荐节。"""
    text = pathlib.Path(output).read_bytes().decode("utf-8")
    probs, rec = mod.split_sections(text)
    letters = [L for L, _ in probs]
    n_lbl = n_q = n_miss = 0
    miss = []
    for letter, body in probs:
        npt = mod.TX.normalize_for_locate(problems_map[letter]) if letter in problems_map else None
        for _mark, label, quotes in mod.labels_in(body):
            n_lbl += 1
            for q in quotes:
                n_q += 1
                if npt is None or mod.TX.normalize_quote(q) not in npt:
                    n_miss += 1
                    miss.append((letter, label, q[:60]))
    n_hist = sum(1 for _L, body in probs for ln in body.splitlines()
                 if ln.strip().startswith("- 历史："))
    return {"letters": letters, "n_sections": len(probs), "n_labels": n_lbl,
            "n_quotes": n_q, "n_miss": n_miss, "miss": miss,
            "n_hist": n_hist, "rec": rec is not None}


# ---------------------------------------------------------------- 手写块（判断层）
NATURE = """**这一节是判断层，机械判据判不了它。** 下面的**红集是机器抽取**（§2 的 stdout）；**性质判定是人工**，逐条写。

### 逐条点名（判据 · 读数 · 为什么 · 性质）

| 判据 | 谁红 | 读数（§2 原文） | 为什么红 | 性质 |
| :--- | :--- | :--- | :--- | :--- |
| `S1` | R1/R2/R3 | `fail-closed：产出里解析不出任何「## 题 <字母>」小节` | `S1` 的承重结构是**一个 `## 题 <字母>` 小节里的一张标签表**；三份写手稿**都用了自己的标题层级**（R1 `### A — …`、R2 `## 0. 结论`…、R3 `## 结论`…），**无一处**形如 `## 题 <字母>` ⇒ `split_sections` 返回空 `probs` ⇒ `check_s1` **fail-closed** | **真红（fail-closed 型）** —— 检查器读不出 ⇒ 判红 + `exit 1`。★ **不是**设计预期的「逐字性那一红」（第一轮够不到，见 §7） |
| `S2` | R1/R2/R3 | `fail-closed：产出里解析不出任何题目小节` | `S2` 在**同一个小节结构**上读 `- 历史：…` 行；无题小节 ⇒ **无对象可判** | **真红（fail-closed 型）**；★ 根因是**形态**（写手不产该结构），**不是**写手把某个历史数写错 |
| `S3` | R1/R2/R3 | `fail-closed：产出里解析不出任何题目小节` | 同上：四轴行要**挂在题小节下**；无题小节 ⇒ 无对象 | **真红（fail-closed 型）**；★ 与 `S2` **共享根因**（**不是级联** —— 两条臂各判各的、独立地撞上「没有题小节」） |
| `S4` | R1/R2/R3 | `fail-closed：产出里没有「## 推荐」小节` | 三份稿**都给了推荐**（都推**题 C**、都带推翻条件），但**标题不是** `## 推荐`（R1 `## 4. 为什么是 C`、R2 `## 0. 结论`、R3 `## 结论`）⇒ `split_sections` 找不到推荐节 | **真红（fail-closed 型）**；★ 特别注意：**推荐的内容是在的**，红的是**形态**（没按 `## 推荐` 这个节名交） |

**★ 别把这四条读成四个独立的缺陷**：它们**根因同源** —— **这份产物不在检查器的输入契约之内**（承重形态缺失）；
但**实测可分两个子族**：

- **格式因（缺题小节）—— `S1`/`S2`/`S3`**：承重形态是**每道题一个 `## 题 <字母>` 小节**；三份稿都按**自己的标题法**
  组织（`### A —` / `## 0. 结论` / `## 结论`），**没有一道**产出那个节头 ⇒ 三条臂各自解析不到对象。
- **格式因（缺推荐节名）—— `S4`**：**推荐是在的**（内容层齐），但节名不是契约要的 `## 推荐`。

所以：

- **没有级联**（没有哪条红是被另一条红带出来的）：四条臂**各判各的**，每条都在自己的解析面上读空。
- **没有假红已修**：本轮**没有**任何一条红是判据自身的错。（本支**不动** `check-topic-select.py`；
  唯一的改动是一句 `method.md` **文档措辞**，且**已实证对全部产出的判据判定零影响**，见 §9。）
- **★ 也别说成写手做得差**：三份稿**都读得懂、都自洽、推荐还都一致（都推题 C）**，
  各自都给了理由、都写了推翻条件、都列了诚实清单。判据红的是**没按本 skill 的契约产出** ——
  与先例 `mcm-playbook` / `mcm-schematic` 那两支「红的是没被告知的约定」是**同一型**。

**本表不声称穷尽**：它只列本支三份第一轮产物**实际触发**的判据，不声明覆盖率。"""

NATURE2 = """**这一节是判断层，机械判据判不了它。** 下面的**红集是机器抽取**（§3 的 stdout）；**性质判定是人工**，逐条写。

### 逐条点名（判据 · 读数 · 为什么 · 性质）

| 判据 | 谁红 | 读数（§3 原文） | 为什么红 | 性质 |
| :--- | :--- | :--- | :--- | :--- |
| `S1` | R1s/R2s/R3s | `题 6 道 · 标签 12 个 · 支撑句 12 条 · 非子串 12 条` | 三位写手**都产出了可比结构**（`## 题 <字母>` 六节 + 标签表都填了），但支撑句是**中文复述 / 翻译**，**不是英文题面的子串** ⇒ 逐条判红 | ★★ **真红（判别型）—— 正是设计要 `S1` 抓的那一格**（第一轮够不到，第二轮第一次走到） |
| `S2` | R1s/R2s/R3s | `fail-closed：产出里解析不出任何「- 历史：…」读数行` | 三条产出的「历史」行**存在**，但**不成正则形态**（`出现约 N 次` / `≈N 次` / `其后 … 合计约 N 题` —— `出现`/`用过模型` 后不是数字）⇒ 一条都不匹配 ⇒ fail-closed | **真红（fail-closed 型）**；★ 与第一轮**不同**：这轮是「**行在、形态不合**」，不是「行都没有」。⇒ **`S2` 的「N 写错」那一格仍未被 RED 行使**（见 §10.2） |
| `S3` | R1s/R2s/R3s | `四轴读数 0 / 7 / 6 处（应 24）· 不符 24 / 31 / 30 处` | 四轴行**在**（每题四条），但**轴名**是写手自拟（`方法成熟度` / `区分度上限` / `翻车风险` / `评判友好度` …），且**可核性标签**多为自拟（`可核：高/中/低`、`不可核`）⇒ 不合 `method.md` §5 的**轴名关键词 + 可核性枚举** | **真红（判别型）** —— R2/R3 有**个别**轴恰好用了 `半可核` 字样（故读数 7/6 而非 0），但轴名与其余轴仍不合 ⇒ **部分命中、整体红** |
| `S4` | R1s/R2s | `推荐 = None · 推翻条件 = None` | 两份稿**都给了推荐与推翻条件**，但行首是 `- **推荐：…**` / `- **推荐**：…`（**粗体标记夹在冒号前**）⇒ 不合 `- 推荐：` / `- 推翻条件：` 的行首形态 | **真红（判别型）** —— **内容在、形态不合** |
| `S4` | （R3s **不红**） | `推荐 = '**选 C（2025 MCM Problem C…' …` | R3 用了逐字的 `- 推荐：` / `- 推翻条件：` ⇒ **PASS** | ★ **对照**：三份里只有一份形态对 ⇒ 说明 `S4` 的形态**不是"给谁都过"** |

（R1s/R2s/R3s 的 `S5`/`S6` 恒 `PASS` —— 规范侧，与 `--output` 无关。）

**★ 第二轮的红与第一轮不是同一型**：第一轮四条臂**全在"结构缺失"上读空**；第二轮**结构在**，
红的是**内容与形态**（引文非子串 / 历史行不成形态 / 轴名与可核性自拟 / 推荐行带粗体）。
⇒ **两轮合起来才既证明"契约外产物 fail-closed"，又证明"契约内但写歪了会被逐条抓住"。**

**本表不声称穷尽**：它只列本支三份第二轮产物**实际触发**的判据，不声明覆盖率。"""

TARGET = """### ★ 期望 vs 实测（两轮对照；P8 的口径：**预期不等于保证**）

**设计的靶子**：没受过「逐字」约束的写手**会用自己的话复述题面** ⇒ 支撑句**不是当天题面的子串** ⇒ `S1` 红。

**第一轮（无形态）实测**：**三位写手一位都没产出标签表 / 支撑句** —— 题小节 0 · 标签行 0 · 引文 0（§7.1）
⇒ **「逐字性」这个靶子第一轮根本没被触发**；`S1` 先在**承重结构**上 fail-closed（`产出里解析不出任何「## 题 <字母>」小节`）。

**第二轮（有中性形态）实测 —— 靶子**到了**：三位写手都产出了**可比结构**（每题一节 `## 题 <字母>`、标签表都填了：
**题 6 道 · 标签 12 个 · 支撑句 12 条**，三人一致），而 **`S1` 对这 36 条支撑句逐条判红**：
**非子串 12 / 12 / 12 条**（§3、§7.1）。⇒ **第二轮才第一次在 RED 里走到「逐字 vs 改写」那一格**，
且**结果正是设计预期的那一红**：写手**没有逐字引用（英文）题面**，而是**用中文复述 / 翻译** ⇒ **非子串**。

⇒ **「`S1` 抓到一句改写过的引文」这件事，现在有两类证据**：

1. **RED（第二轮）**：写手**自发**产出的支撑句**全部非子串**（**中文复述 / 翻译**型）；
2. **变异驱动器**：`MUT-S1a`（**近逐字**改写 —— `in space and time` → `over space and time`）、`MUT-S1b`（清空支撑句单元格）。
   ★ **第二类才是"一词之差"那一格**。

★ **照实说两条边界**：

- 第二轮的 36 条非子串是**中文复述 / 翻译**（题面是英文、brief 是中文）⇒ 它证明的是 `S1` **能抓住"没逐字引"**，
  **不**证明 `S1` 能抓住**近逐字的一词之差**（那一格由 `MUT-S1a` 证）。
  **不把 RED 第二轮读成"`S1` 已被全面验证"。**
- **第一轮的结论仍然有效、且与第二轮不同**：它证明**契约外产物在产出侧全臂 fail-closed** ——
  两轮**不是同一件事的两次呈现**（对照见 §10）。

★ **处置（照 P8）**：**不调 brief、不换写手、不凑数** —— 两轮**都照实记**。
★ **为什么第二轮够得到「逐字性」那一格**：要触发它，产出里得**先有** `## 题 <字母>` 小节 + 标签表；
第一轮写手对着中性 brief **不产那个结构** ⇒ `S1` 在结构上已 fail-closed；第二轮给了**只有形状、无纪律**的空壳
⇒ 写手产出了那个结构 ⇒ `S1` 才走到比对支撑句那一步。"""

LOOK = """**★ 先把这件事说清楚：这一节是「替代品」，不是「等价物」。**

本模块**不产可「看」的产物**（无图 / 无表 / 无代码 / 无 PDF）⇒ 设计 §3.3 的口径是 **「看一眼」层对本支不适用**，
并给一条**替代**：**把产出的「推荐 + 依据」拿给一个人读，问「照这个你能定题吗」**。
下面就是这条替代品的执行记录。**两层替代必须都标明**：

1. **层本身是替代品**：本支**没有**可供「看」的东西（不像绘图那支有 PNG 可看）。**不写我们也做了看一眼层。**
2. **读的人也是替代品**：设计说拿给**一个人**读；本任务在后台跑、**够不到人** ⇒ 实际读的是
   一个**干净上下文、非 `fork` 的 `general-purpose` agent**（给了它 GREEN 产出 `green/out-G1/decision.md`
   的路径 + 一句「照这个你能定题吗」）。⇒ 它是**替代品的替代品**：**agent 的判读 ≠ 人的判读**，
   **只有转录级忠实度**，无沙箱可证。

**被读的那份**：`green/out-G1/decision.md`（用本 skill 出的同一件事，**已入库**；它不是「跑出来的一次输出」，是本支 GREEN 产物本身）。

### 读的人的原话（转录；压缩了篇幅，未改判词）

> **结论一句话：No — not finalize. Yes — narrow and start.** 文档把你从「六道题」带到「**A，C 作后备**」，
> 且**对它停在哪里是诚实的**；但真正决定 A-vs-C 的那个问题，**文档自己承认核不了**。
> 你能承诺一张**候选表**、能烧掉第一小时；**你不能只凭这一页就签字定题**。

**它判「能让你承诺」的**：

- **数据可得性那一轴具体且决定性强**：C 给 5 个文件且**禁用外部数据**（`Your models and data analysis must ONLY use
  the provided data sets`）、D 给 9 个文件且允许更多（`teams are not limited to these data`）、A/B/E/F 无数据要自采
  ⇒ 这一条**单独**就把 B/E/F 杀掉。
- **分类（L1/L2 + 支撑句）可核**：每个标签都钉在一句可引的题面上，几分钟可审计、不必信任顾问。
- **有唯一点名的推荐（A）+ 五条显式推翻条件**：够行动一小时，不够收口。

**它判「照做不了」的**：

- **四轴不带分 ⇒ 没有跨题比较**：文档说「推荐从证据档里推出来」，**但证据档 → 排序这一步从没展示**；
  你**复现不了**为什么 A 赢 D，顾问的加权（创新 vs 可交付）**不可见**。
- **轴 3（拥挤）自认不能作判据**（「最软」「可能整体偏」「不预测选题人数」）⇒ **它什么也没决定**。
- **轴 4（创新）大多落在「未知 / 你这版算不算新」** ⇒ 是判断不是读数 ⇒ **什么也没决定**。
  实际只有轴 1、2 在工作，而**轴 2 是纯判断**。
- **「同型历史」的计数出处不清**：组合是**跨 2016–2026** 数的（B 的「7 次」含 2026 B），
  而文档又说**模型配对只覆盖 2025** ⇒ 两条证据线混在一个 bullet 里，**没说哪个数出自哪份文件**。

**它判「会停下来问人」的**：

1. **我们到底做不做得动 A？**（要害）推荐靠的是它自己那条轴 2 判断「可交付（不判否）」（**自标「判断、非读数」**），
   又在推翻条件里写「若判定逆问题交不出东西就推翻」。**唯一承重的输入是一句文档背不了书的意见。**
2. **目标 = 求新还是求稳？** 文档说 A 求「做得不同」、C 求「绝对做得完」，**把这是价值选择交回给你**。
3. **这真是我们的题集吗？** 文档**限定在 2025 A–F**，且自己承认「**当天六题与语料的 2025 A–F 同文**」 ⇒
   若比赛是**别的年份**，整份作废。**先核年份。**
4. **语料覆盖** —— 用任何计数前，先确认 `PROBLEM_TYPES.md` 与 `MODEL_MAP.md` 各覆盖什么。

**它列「不核不信」的**：**每一个「N 次」历史计数** · **每一个模型频次**（且 `MODEL_MAP.md` 只覆盖 2025、n 很小，**不可外推**）·
题面里的 Juneau 事实 · ★ **「新打标签与语料 2025 标注一致」这条不算独立验证**（输入是同一段文本 ⇒ **一致是构造出来的，不是证明了什么**）·
全部难度判词。

**★ 本层最诚实的读法（别夸大也别埋没）**：

- 读的人**没有指出任何「数字与来源对不上」的**（`S1`/`S2` 那些读数他可独立核） —— 与 §7.1 的机器读数一致。
- 它指出的是**可用性 / 完整性**：**四轴无分 ⇒ 复现不了排序** · **承重判断是判断不是读数** ·
  **两条历史证据线混用** · **题集年份边界要先核**。
  ★ **这几点机械判据一条都报不出来**（`S1`–`S6` 查的是「引文是不是题面子串 / 历史数对不对 / 四轴齐不齐标没标可核性 /
  有没有推翻条件 / 时间盒与禁令在不在位」） —— 这正是看一眼层存在的理由。
- ★ **但有一条要分清楚**：读的人把「轴 3 什么也没决定」「轴 4 什么也没决定」当**缺陷**；
  在本 skill 的**设计口径**里，轴 3 **本来就被钉成「最软、不得单独决定推荐」**（设计 §7-1）、
  轴 4 的**后半本来就是判断** ⇒ **那是设计的有意选择**，不是产出走样。
  ★ 不过读的人由此推出的**「实际只有轴 1、2 在工作，而轴 2 是纯判断」**是一条**有效**的提醒：
  本 skill 的排序**承重在一次纯判断上** —— 这条**登记在案**，供后续复核 `method.md` 的取舍规则时参考。
- ★ **反例也记**：读的人**没有**质疑「引文是不是题面的逐字句」这一点（他默认接受了那些引用可核） ——
  说明 `S1` 那条纪律**在这一次阅读里没被误读成「差不多就行」**，
  ★ **但这只是 1 个读者 × 1 份产物的读数，不是 `S1` 已被验证有效**。"""

PROOF = """## §10 两轮 RED 各自证明了什么 / 不能证明什么（本轮修复）

**两轮不是同一次跑的两个副本，是两个**不同**的读数。**

### §10.1 第一轮（无形态）—— 证明了「契约外产物 fail-closed」，**不能**证明 `S1` 的逐字性

- **证明了**：对着只有「挑一道并说明为什么」的中性 brief，写手**不会自发产出本 skill 的承重形态**
  （题小节 / 标签表 / 推荐节全 0）⇒ 检查器对**契约外产物**在**产出侧全臂 fail-closed**（`S1`–`S4` 全红、
  **无假红、无级联**）。★ 这是一条**真结果**，也是「fail-closed 不许静默绿」的正面证据。
- **不能证明**：`S1` 的**逐字判别力** —— 它在那一步（解析不出 `## 题 X`）就停了，**没走到比对支撑句**。
  ⇒ 第一轮对 `S1` 的判别力**提供不了证据**。

### §10.2 第二轮（有中性形态）—— 第一次走到并点亮「逐字」那一格

- **证明了**：给一份**只有形状、无纪律**的空壳后，写手**产得出可比结构**（题 6 道 · 标签 12 个 · 支撑句 12 条 ×3 人），
  且 **`S1` 逐条判红这 36 条支撑句（非子串 12 / 12 / 12）** ⇒ **`S1` 的逐字判别力在 RED 里被真正行使**。
  ★ 顺带还行使了 `S3`（轴名 / 可核性自拟 ⇒ 红）与 `S4`（推荐行带粗体 ⇒ 红；R3 形态对 ⇒ PASS，构成对照组）。
- **不能证明**：
  - **近逐字（一词之差）**那一格 —— 本轮非子串是**中文复述 / 翻译**型，那一格由 `MUT-S1a` 证；
  - **`S2` 的「N 写错」那一格** —— 第二轮三条 `- 历史：` 行**写得不成正则形态**（`出现约 N 次` / `≈N 次` /
    `其后 … 合计约 N 题`）⇒ `S2` 仍是 **fail-closed**（解析不出历史行），**没走到「N 与语料现取不符」那一格**。
    `S2` 那格的证据仍只在 `MUT-S2`（组合数 / 模型篇数）里；
  - **真实赛期情形**（当天新题不在语料里）—— 见 §0。

### §10.3 ★★ GREEN 的 `S2` 读数因边界 ③ 被违反而**退化**

- `references/corpus-lookup.md` 的**边界 ③** 写着「**当天六题不在语料里**」。
- 本轮**故意用 2025 A–F**（它们**就在语料里**）⇒ 边界 ③ **被违反** ⇒ GREEN 里那行
  `- 历史：题 `2025 A` 用过模型 …` **引的正是当天那道题自己**（`green/out-G1/decision.md` 有 6 处同型行）。
- ⇒ **GREEN 的 `S2` 这一条**：**只验证了形式**（篇数与 `MODEL_MAP.md` 现取一致、判据 `PASS`），
  **没有验证真实赛期下的语义**（真实赛期引不到当天题，行的来源/语义都不同）。
  ★ **不把 GREEN 的 `S2` `PASS` 读成「`S2` 在真实赛期也 `PASS`」。**
- ★ **同批的文档加固（本轮落地）**：`references/corpus-lookup.md` §3 新增一条 —— **同型历史行必须引「另一道题」、
  不许引当天那道题自己**（`S2` **抓不到**这条 —— 它只核 `MODEL_MAP.md` 的篇数）；`references/method.md` §5 同批加指针。"""


def main():
    mod = load_checker()
    problems_map = mod.parse_problems(str(PROBLEMS)) or {}
    table = doc_table()
    tags = [t for t, _p, _s, _d in table]
    results = {tag: check(p) for tag, p, _s, _d in table}
    CRIT = criteria_ids(*[results[t] for t in tags])
    # ★ 这一行是**故意的 tripwire**，**不是**「写死条数」的反例：判据清单本身是**上一行现取**的
    #   （`criteria_ids(...)` —— 从检查器 stdout 读 `PASS|FAIL <id>`，见 §0 与硬要求 8）；
    #   本行只把「现取到的东西」钉在**本支已知的这 6 条**上：一旦上游增/删判据，宁可**当场炸**请人来核，
    #   也**不**静默跟着变（否则 §5/§5.2 那几张汇总表会在判据增减时**悄悄漂移**）。
    #   ★ 与「写死条数」那一型的区别（下一个编辑者别搞混）：那一型是**唯一来源**被写死、判据增减时**静默**跟着变；
    #     本行旁边**另有一条独立的现取路径**（上一行的 `criteria_ids`），写死的那 6 条只作**响闸**用。
    assert CRIT == ["S1", "S2", "S3", "S4", "S5", "S6"], "判据清单变了：%s" % CRIT
    for t in tags:
        assert set(results[t]["cells"]) == set(CRIT), (t, sorted(results[t]["cells"]))
    assert results["G1"]["result"][0] and reds(results["G1"], CRIT) == [], "GREEN 非全绿"

    # ---- §9 零影响证明：基线版 method.md（含旧措辞）vs 工作树版（含订正）逐判据比对 ----
    build_dir = REPO / "build"
    build_dir.mkdir(parents=True, exist_ok=True)
    base_method = build_dir / "_topicselect-base-method.md"
    src, _ = run(["git", "show", BASE_REF + ":.claude/skills/mcm-topic-select/references/method.md"])
    base_method.write_bytes(src.replace("\r\n", NL).encode("utf-8"))
    try:
        zerodiff = {}
        for tag, p, _s, _d in table:
            a_, b_ = check(p, method=base_method), check(p, method=METHOD)
            va = {k: a_["cells"][k][0] for k in CRIT}
            vb = {k: b_["cells"][k][0] for k in CRIT}
            zerodiff[tag] = (va, vb, va == vb)
    finally:
        base_method.unlink()

    meta = {}
    for tag, p, _s, _d in table:
        b = p.read_bytes()
        meta[tag] = (len(b), len(b.decode("utf-8").splitlines()),
                     git_hash_object(p.relative_to(REPO).as_posix()))
    probe = {tag: structure_probe(mod, p, problems_map) for tag, p, _s, _d in table}
    brief_bytes = BRIEF.read_bytes().decode("utf-8")
    shape_bytes = NEUTRAL_SHAPE.read_bytes().decode("utf-8")
    shape_blob = git_hash_object(NEUTRAL_SHAPE.relative_to(REPO).as_posix())
    wt_blob = git_hash_object(CHECK.relative_to(REPO).as_posix())
    base_blob = run(["git", "rev-parse", BASE_REF + ":tests/skills/topic-select/check-topic-select.py"])[0].strip()
    prob_blobs = {p.stem: git_hash_object(p.relative_to(REPO).as_posix())
                  for p in sorted(PROBLEMS.glob("*.md"))}

    L = []
    a = L.append
    a("# Task 3 · RED × GREEN 对照证据（`mcm-topic-select`）")
    a("")
    a("本文件由 `tests/skills/topic-select/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("**§2 / §3 / §4（原始读数）· §5（对照表）· §7.1（结构探针）是机器抽取**（逐格解析检查器 stdout、逐行扫产物）；")
    a("**§6 的性质判定 · §7.2 的判决 · §8 的看/读记录 · §10 的两轮对照是手写**（文里已标明）。")
    a("")

    # ---------------- §0
    a("## §0 口径（同一件事 · 同一把尺 · RED 是自变量 · **两轮**）")
    a("")
    a("- **同一件事**：`tests/skills/topic-select/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联）"
      " ＋ 同一组**六道题面** `tests/skills/topic-select/red/problems/A.md`–`F.md`（**2025 A–F 的真实题面**）。")
    a("- **两侧**：RED = **干净上下文写手**产出的选题决策（**两轮**，见下）；"
      "GREEN = **用本 skill**（`SKILL.md` 契约 + `references/`）出的同一件事。")
    a("- ★★ **两轮 RED（一个变量之差）**：")
    a("  - **第一轮（无形态）** = `red/out-R{1,2,3}/decision.md` —— 只给 **brief + 六份题面**。")
    a("  - **第二轮（有中性形态）** = `red/out-R{1,2,3}-shape/decision.md` —— 多给一份 **`red/neutral-shape.md`**"
      "（**只有形状、无纪律**的空壳；§1.1 全文内联）。")
    a("  - ★ **两轮都留、都真读数**；各自证明 / 不能证明什么见 **§10**。")
    a("- **同一把尺**：`tests/skills/topic-select/check-topic-select.py`（判据 `S1`–`S6`）。**同一组参数**："
      "`--problems` / `--corpus` / `--skill-md` / `--method` 全指向**同一份**；**只有 `--output` 各指向该侧自己的产出**。")
    a("- **判据清单现取**：本支 **%d 条**（`%s`）。**不写死条数**"
      "（先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。" % (len(CRIT), "、".join(CRIT)))
    a("- **检查器自证**：工作树 blob `%s` · **基线 `%s`** blob `%s` ⇒ %s —— ★ **本支不动检查器**"
      "（两侧用的是同一版工作树版；参照系取**基线 commit**、**不取 `HEAD`**，理由同先例）。"
      % (wt_blob[:12], BASE_REF, base_blob[:12],
         "**相同**" if wt_blob == base_blob else "**不同（！）**"))
    a("- **题面自证（逐件 blob）**：" + " · ".join("`%s`=`%s`" % (k, v[:12]) for k, v in prob_blobs.items()))
    a("- **中性形态自证**：`red/neutral-shape.md` 工作树 blob `%s`（§1.1 全文内联）" % shape_blob[:12])
    a("- **RED 是自变量**：两轮写手稿**照实入库**（本轮未改）。逐件读数：")
    a("")
    a("| 产物 | 轮 | 字节 | 行数 | 工作树 blob |")
    a("| :-- | :-- | --: | --: | :-- |")
    for tag, _p, side, desc in table:
        b, ln_, bl = meta[tag]
        a("| `%s` | %s | %d | %d | `%s` |" % (tag, desc, b, ln_, bl[:12]))
    a("")
    a("- ★ **RED 的诚实边界（硬要求 6 / 设计 §3.2）**：中性 brief **已经限定**要「从六道题里挑一道并说明为什么」"
      "（必答项：挑一道 + 理由）⇒ RED **测不到**「连推荐都给不出」那一类失败"
      "（写不出任何选择、给不出理由）。**不声称覆盖全部失败模式。**")
    a("- ★ ★ **本轮测不到的真实赛期情形**：**2027 的题尚不存在**，而**任何真实可得的 MCM 题集（2016–2026）"
      "都已在语料里**（`corpus/papers/PROBLEM_TYPES.md` 逐题标注）⇒ 本轮选**真实旧题集 2025 A–F** 做 RED/GREEN，"
      "**复现不了**「当天新题刚放出、尚不在语料里」那一情形。**本轮测的是**形态/逐字纪律**（`S1`）与判据本身，"
      "**不是**「新题不在语料里」那一情形。**不声称覆盖真实赛期情形。**")
    a("- ★ **题面口径**：六份题面由 `tools/papers/taxonomy.extract_text`（`pdftotext -enc UTF-8`）"
      "从 `corpus/官方原题/2025/*.pdf` 抽出（**唯一口径**，见 `taxonomy.py`）；逐件 blob 见上。")
    a("- ★ **环境旁路**：写手是本机 Claude Code 的 agent，会话级共享上下文里另有三处可见面"
      "（skill 列表里 `mcm-topic-select` 那一行的**描述** + `git status` 快照 + **Recent commits**）。"
      "★ **本轮这不是「没泄漏」**：旁路**实打实漏了**「要做哪几样」；**第二轮旁路更重**"
      "（recent commits 里多了点名「判据 `S1–S6` + 变异驱动器」的提交）。**照实披露**"
      "（探针全文与探针自身的边界见 `red/writer-self-reports.md` §4、§5）。")
    a("")

    # ---------------- §1
    a("## §1 同一件事（逐字内联；RED 与 GREEN 共用）")
    a("")
    a("```text")
    a(brief_bytes.rstrip(NL))
    a("```")
    a("")
    a("★ **中立性抉择**（硬要求 1）：brief **只问**「从六道题里挑一道并说明为什么」，"
      "**不含**任何形态要求（不提「分类」「历史」「四轴」「推翻条件」「表格」）、**不含**任何来源"
      "（不给本 skill、不给语料、不给判据、不给本任务书）。**唯一**算限定的一句是**挑一道 + 说明为什么** —— "
      "它**既是**任务的交付形态，**也是**本支 RED 的那条诚实边界。")
    a("")
    a("### §1.1 第二轮的**追加件**：`red/neutral-shape.md`（**只有形状、无纪律**的空壳；逐行判定见 `red/README.md` §6）")
    a("")
    a("```text")
    a(shape_bytes.rstrip(NL))
    a("```")
    a("")
    a("★ **它只加了一个变量**：**形状**。它**没有**加任何「内容该怎么写」的纪律 —— "
      "**尤其没有「支撑句必须逐字来自当天题面」这条**（那正是第二轮要测的 `S1` 靶子）。")
    a("")

    # ---------------- §2 / §3（RED 两轮 + GREEN）
    for si, (name, subtags, sub) in enumerate((
            ("RED · 第一轮（无形态）", ["R%d" % n for n in SCENES], "三位干净上下文写手 · 只给 brief + 六份题面"),
            ("RED · 第二轮（有中性形态）", ["R%ds" % n for n in SHAPE_SCENES], "三位干净上下文写手 · 另给一份中性形态"),
            ("GREEN（用本 skill（契约 + references））", ["G1"], "用本 skill"))):
        a("## §%d %s 原始读数（%s）" % (si + 2, name, sub))
        a("")
        for tag in subtags:
            d = results[tag]
            a("### %s" % tag)
            a("")
            a("```")
            a("$ " + d["cmd"])
            a(d["stdout"])
            a("[exit=%d]" % d["rc"])
            a("```")
            a("")

    # ---------------- §5
    a("## §5 对照表（机器抽取）")
    a("")
    a("每格 = 状态：绿 = `PASS` / 红 = `FAIL`。逐格解析自 §2/§3/§4 的 stdout；判据 ID 取现行（**现取**，见 §0）。")
    a("")
    a("| 产物 | 侧 | 轮 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    for tag, _p, side, desc in table:
        data = results[tag]
        c = data["cells"]
        row = [tag, side, desc] + ["绿" if c[k][0] else "红" for k in CRIT]
        row.append("PASS" if data["result"][0] else "FAIL")
        a("| " + " | ".join(row) + " |")
    a("")
    a("### §5.1 逐判据判词（机器抽取；判词原文，不手抄）")
    a("")
    a("| 产物 | 侧 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for tag, _p, side, _desc in table:
        data = results[tag]
        for k in CRIT:
            cell = data["cells"].get(k)
            if cell:
                a("| %s | %s | %s | %s | %s |" % (tag, side, k, "PASS" if cell[0] else "FAIL", cell[1]))
    a("")
    a("### §5.2 汇总（由 §5 的格子逐格重算）")
    a("")
    a("| 侧·轮 | 产物数 | 红格数（判据 × 产物） | 判红的判据 ID（并集） | 全绿产物数 |")
    a("| :-- | --: | --: | :-- | --: |")
    groups = (("RED·第一轮（无形态）", ["R%d" % n for n in SCENES]),
              ("RED·第二轮（有中性形态）", ["R%ds" % n for n in SHAPE_SCENES]),
              ("GREEN", ["G1"]))
    for gname, gtags in groups:
        allred, ok, total = [], 0, 0
        for tag in gtags:
            data = results[tag]
            total += 1
            if all(data["cells"][k][0] for k in CRIT) and data["result"][0]:
                ok += 1
            allred += reds(data, CRIT)
        a("| %s | %d | %d | %s | %d/%d |" % (gname, total, len(allred),
          "、".join(dict.fromkeys(allred)) or "（无）", ok, total))
    a("")
    a("★ **这张表是契约一致性的读数，不是质量的读数** —— RED 的红**不是**选题决策做得差（见 §6、§7）。")
    a("")
    a("★ **一条必须写死的口径**：`S5`/`S6` 判的是**规范侧**（`SKILL.md` + `references/method.md`），"
      "**与 `--output` 无关** ⇒ 两侧这两条恒 `PASS`（它们对 RED/GREEN 的差**不敏感**）。"
      "RED 与 GREEN 的**分野只体现在 `S1`–`S4`（产出侧）**。")
    a("")

    # ---------------- §6 红逐条点名
    a("## §6 RED 的红逐条点名（硬要求 4：真红 / 级联 / 假红已修）")
    a("")
    a("（红集**机器抽取**自 §2/§3；性质判定是人工判定，逐条写。）")
    a("")
    a("### §6.1 第一轮（无形态）")
    a("")
    for n in SCENES:
        a("- **R%d 红集** = `{%s}`" % (n, ", ".join(reds(results["R%d" % n], CRIT))))
    a("")
    a(NATURE)
    a("")
    a("### §6.2 第二轮（有中性形态）")
    a("")
    for n in SHAPE_SCENES:
        a("- **R%ds 红集** = `{%s}`" % (n, ", ".join(reds(results["R%ds" % n], CRIT))))
    a("")
    a(NATURE2)
    a("")

    # ---------------- §7 靶子
    a("## §7 ★ 靶子：`S1` 的逐字性（硬要求 3 / 计划 P8）")
    a("")
    a(TARGET)
    a("")
    a("### §7.1 机器抽取：七份产出的承重结构（复用检查器的解析，不手抄）")
    a("")
    a("| 产物 | 轮 | `## 题 X` 小节 | 标签行 | 引文 | 非子串引文 | `- 历史：` 行 | `## 推荐` 节 |")
    a("| :-- | :-- | :-- | --: | --: | --: | --: | :-- |")
    for tag, _p, _s, desc in table:
        p = probe[tag]
        a("| %s | %s | %s | %d | %d | %d | %d | %s |" % (
            tag, desc, ("、".join(p["letters"]) or "（无）"), p["n_labels"], p["n_quotes"],
            p["n_miss"], p["n_hist"], "有" if p["rec"] else "（无）"))
    a("")
    a("### §7.2 逐题面比对：引文不是题面子串的**逐条**（机器抽取）")
    a("")
    any_miss = False
    for tag, _p, _s, _d in table:
        p = probe[tag]
        if not p["miss"]:
            continue
        any_miss = True
        a("**%s**（%d 条）" % (tag, len(p["miss"])))
        a("")
        for letter, label, q in p["miss"]:
            a("- 题 %s · 标签「%s」：`%s`" % (letter, label, q))
        a("")
    if not any_miss:
        a("（七份产出里**没有一条**引文落在题面之外。）")
        a("")
    a("★ **本探针与 `S1` 同源**（复用检查器的 `split_sections` / `labels_in` / `taxonomy` 归一化，"
      "**不另写一套形态**）：这里的读数与 §2/§3 的 `S1` 判词是**同一件事的两种呈现**。")
    a("")

    # ---------------- §8 替代品
    a("## §8 「看一眼」层的替代品（硬要求 7 / 设计 §3.3）")
    a("")
    a(LOOK)
    a("")

    # ---------------- §9 生成器
    a("## §9 生成器 · 判据非空泛 · 并进来的行修正 · 不动点")
    a("")
    a("- 本文件的机器部分由 `tests/skills/topic-select/make-evidence.py` **当场跑** "
      "`check-topic-select.py` 生成（`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout（§5）。")
    a("- ★ **判据非空泛（失败方向的另一条臂）**：`mutate-topic-select.py` 的读数收在此处"
      "（**本生成器不执行该驱动器**，故**不声称当场跑过**；复跑命令见本节末）。"
      "它证明 `S1`–`S6` **逐条都能真红**、4 条 fail-closed 真红、4 条射程边界对照必须绿，**合计 `17/17`**。")
    a("")
    a("### ★ 并进来的行修正：`method.md` 的题标题行措辞（Task 2 复核登记的 Minor）")
    a("")
    a("- **原状**：`references/method.md` 的「题标题行」那句写「字母在「题」之后，**后面接非字母数字字符或行尾**」，"
      "而检查器 `PROB_HEAD` 用的是 `\\b`（**Unicode 词边界**）—— 两者**不等价**："
      "**实测** `## 题 A_` **不匹配**（`_` 是 Unicode 词字符、对 `\\b` 不构成边界）。")
    a("- **本支的处置（二选一，选了改文档）**：把那句改成与 `\\b` 相符的说法"
      "（「后面接**词边界**（`\\b`，Unicode 语义）—— 即后一个字符不是 Unicode 词字符（字母 / 数字 / **下划线**）"
      "或已到行尾」）。★ **理由**：正则 `PROB_HEAD` 是那份形态的**机读实现**（检查器 docstring 自己写着"
      "「改形态请改 `method.md` §5，再回来对正则」）；文档错、正则对 ⇒ **改文档**代价最小、"
      "且**不必碰检查器与变异驱动器**（改正则则两处都要跟着动，见任务书那条括注）。")
    a("- ★ **实证（不是推理）**：生成器**当场用基线 `%s` 版 `method.md`（旧措辞）与工作树版（新措辞）各跑全部产出**，"
      "**逐判据比较** ⇒ 全部判定**完全一致**（本节末的零影响块）。" % BASE_REF)
    a("- ★ **不声称穷尽**：只验证了在**当前**这份 `method.md` 与全部产出上两版同判，"
      "**没有**对「将来若真有产出一行 `## 题 A_`」做端到端复现。")
    a("")
    a("**零影响证明（机器抽取；基线 `%s` 版 method.md 旧措辞 vs 工作树版新措辞，逐判据）**：" % BASE_REF)
    a("")
    a("| 产物 | 旧措辞版判定 | 新措辞版判定 | 同？ |")
    a("| :-- | :-- | :-- | :-- |")
    for tag, _p, _s, _d in table:
        va, vb, same = zerodiff[tag]
        fmt = lambda d: " ".join("%s=%s" % (k, "P" if d[k] else "F") for k in CRIT)
        a("| %s | `%s` | `%s` | %s |" % (tag, fmt(va), fmt(vb), "**是**" if same else "**否**"))
    a("")
    a("⇒ **这处行修正对本文档里的任何判据读数都是零影响**（它改的是一句**文档措辞**，不是判据的射程）。")
    a("")
    a("### 不动点")
    a("")
    a("在**已提交的树上**重跑本生成器 ⇒ 本文件**逐字节不变**（证法：跑后 `git status --short` 仍为空）。")
    a("")
    a("```text")
    a("$ python tests/skills/topic-select/mutate-topic-select.py   # 快照，非生成时现跑")
    a("MUT: 9/9 达预期（判据打红：S1 改写+清空 / S2 组合数+模型篇数 / S3 判断改读数 / S4 删推翻条件 / "
      "S5 method 默认值+SKILL 契约值 / S6 禁令改坏）")
    a("MUT: 4/4 达预期（fail-closed：output / problems / corpus / method 读不出即红）")
    a("MUT: 对照 4/4 达预期（必须绿：轴依据措辞 / 推荐题号 / 新增合法标签行 / 规范散文）")
    a("MUT: 17/17 达预期（合计）")
    a("```")
    a("")
    a(PROOF)
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace("\r\n", NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO).as_posix(), OUT_DOC.stat().st_size, "B")
    print("criteria %d: %s" % (len(CRIT), CRIT))
    for tag, _p, _s, _d in table:
        print("  %-4s red: %s" % (tag, reds(results[tag], CRIT) or "(none)"))
    print("zero-impact same:", {t: zerodiff[t][2] for t in zerodiff})
    print("OK")


if __name__ == "__main__":
    sys.exit(main())
