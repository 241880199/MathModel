#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/section-writer/mutate-section-writer.py` —— `check-section.py` 的**变异驱动器**。

用法：  python tests/skills/section-writer/mutate-section-writer.py

## 它做什么

把**已知好的节文本**（`build/section-writer-mut/` 下的两份夹具：`.md` 与 `.tex`）与
**本工具自己的源码**各取一份副本**逐条改坏**（当场改、当场跑、当场判、然后收走），
断言检查器**点名红在该条判据上**；另设**必须仍绿**的射程边界对照。

**每条判据 `SW1`–`SW8` 至少一条真红作证**，两条静态自检（`SELF1`/`SELF2`）各一条真红作证
（本仓硬规矩：判据只能从失败方向证明）。

- **判据本体不动**：驱动器**调 skill 目录那一份**（`.claude/skills/mcm-section-writer/check-section.py`），
  **不在 `tests/` 下再写一份镜像版**；变异只碰 `build/` 下的副本（仓内 gitignored，**不落 C 盘 / `%TEMP%`**）。
- 收尾逐件 `git hash-object` 自证"受保护件逐字节未变"，并核 `git status --short` 为空。
- **期望集逐条写死**：每条变异断言"**与基准逐条相比，恰好这些判据的状态变了、且变成什么**"。
  "该红没红"或"顺手带红了别的判据"都会被当场抓出来。
- **判据清单现取**：先把检查器在**干净夹具**上跑一遍、把 `PASS|WARN|FAIL|SKIP  <id>` 行读成 id 集合，
  **再并上"空节夹具"的输出**（`EMPTY` 只在空节路径出现，不并进来它永远进不了清单 —— 见下），
  拿这个并集当"全部判据"。变异若点名了**不在现取集合里**的判据 ⇒ 该条直接判失败（防"打错靶子还报绿"）。
  ★ **这条断言不恒真**：驱动器自带一条**自证** —— 造一个点名**清单外**判据（`SW9`）的假 Case，
  断言它**必被** `_bad_target_ids()` 抓到；抓不到即 `rc≠0`（防"白名单把断言架空"）。
- ★ **`WARN` 不许做成非 0**：每条 `WARN` 变异**同时断言退出码 = 0**（这条正是任务书 C 的硬要求）。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望 |
| :--- | :--- | :--- |
| `MUT-SW1` | 表内数字改成写手输入里搜不到的（表题仍挂具名外源 `WHO`，且已带 `illustrative` 标注） | `SW1` → `FAIL` |
| `MUT-SW2` | 表题**保留具名外源（`WHO`）**、**抹掉** `illustrative` 标注，数字仍搜不到 | `SW1`+`SW2` → `FAIL` |
| `MUT-EMPTY` | 空文件（0 字节） | 至少 `FAIL`（`EMPTY`）· 退出码非 0 |
| `MUT-HEADONLY` | 只有标题、无正文 | 至少 `FAIL`（`EMPTY`）· 退出码非 0 |
| `MUT-FORMULAONLY` | 只有公式（`$$…$$`）、无散文无表 | 至少 `FAIL`（`EMPTY`）· 退出码非 0 |
| `MUT-ALIGNATONLY` | 只有 `\begin{alignat}` 环境、无散文无表 | 至少 `FAIL`（`EMPTY`）· 退出码非 0 |
| `MUT-FORMULA-PERIOD` | 块级公式后多一个句号（`$$…$$.`） | 至少 `FAIL`（`EMPTY`）· 退出码非 0 |
| `MUT-SW3` | 把**每一段**末尾都补成"评价/格言"句（9 段全中） | `SW3` → `WARN` |
| `MUT-SW4` | **灌水膨胀**（正文词数 ÷ 写手输入词数越过提请复核线） | `SW4` → `WARN` |
| `MUT-SW5` | 塞满 `rather than`（对比式构造密度越过 3‰） | `SW5` → `WARN` |
| `MUT-SW6` | 塞自评套话（`the purpose of this section` / `worth stating`） | `SW6` → `WARN` |
| `MUT-SW7` | 连续插入极短断言句（4 词 × 多段） | `SW7` → `WARN` |
| `MUT-SW8` | 塞可整句删除的元话语（`Taken together, …`，占比 ≥15%） | `SW8` → `WARN` |
| `MUT-SELF1` | 把明令不用的判据（举例之一）**字面**写进工具源码副本 | `SELF1` → `FAIL` |
| `MUT-SELF2` | 把工具头部那段**压力臂局限文字删掉** | `SELF2` → `FAIL` |
| `CTRL-good-md` | 射程边界：干净 `.md` 夹具（含带出处的表） | （无变化） |
| `CTRL-good-tex` | 射程边界：干净 `.tex` 夹具（`.tex` 输入也要能吃） | （无变化） |
| `CTRL-prose-edit` | 射程边界：只改一句普通散文（不碰表 / 词表 / 句长） | （无变化） |
| `CTRL-selfcalc` | ★ 合法**自算结果表**（无外源、无标注串、数字搜不到） | `SW2` → `WARN`（**只提请复核**、退出码 0） |
| `CTRL-truth-S1` | ★ 真值 `true-S1.md` —— **`SW3`–`SW8` 不得出 `WARN`** | `SW3`–`SW8` ≠ `WARN` |
| `CTRL-truth-S2` | ★ 真值 `true-S2.md` —— **`SW3`–`SW8` 不得出 `WARN`** | `SW3`–`SW8` ≠ `WARN` |
| `CTRL-no-input` | `--input` 缺失 ⇒ `SW1`/`SW2` 必须报**"无法判定"**（`SKIP`），**不许报 `PASS`** | `SW1`,`SW2` → `SKIP` |
| `CTRL-unknown-section` | `--section` 给不认识的值 ⇒ **fail-closed 红** | 退出码非 0 |
| `CTRL-shortprose-formula` | ★ H1 对照：一句 `<5` 词短散文 + 一条公式 | **不得**判 `EMPTY`（`<5` 词是解析门，那一句散文算正文）、`exit=0` |
| `CTRL-inline-formula-prose` | ★ H2-1 对照：含**行内公式**的散文行（`We obtain $T = 18743$ from the fit.`） | **不得**判 `EMPTY`（残留含字母 ⇒ 仍是正文）、`exit=0` |

★ `CTRL-truth-S1` 会看到 `SW1`/`SW2` 报 `FAIL`（真值那张 WHO 表的数字**确实不在 `brief-S1.md` 里**，
`judge.md` §4.1 同记："brief 要了表、要了数、没给数"。）。**这不是误报**，故**不**把 `SW1`/`SW2` 列入
真值对照的断言面 —— 真值对照**只断言任务书 E.2 要求的那六条**（`SW3`–`SW8` 不得出 `WARN`）。
**其它可能的读失败入口本表未逐条覆盖（不声称穷尽）。**

## 合计行形态

照 `mutate-topic-select.py` / `mutate-table-style.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**
（末行放"运行完整性"读数）。
"""

import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]     # tests/skills/section-writer/x.py → 仓根
CHK = ROOT / ".claude/skills/mcm-section-writer/check-section.py"
SKILL = ROOT / ".claude/skills/mcm-section-writer"
ARCH = ROOT / "tests/skills/arch-cases"
BUILD = ROOT / "build/section-writer-mut"              # ★ 临时件只落仓内 `build/`
GUARDED = (CHK, SKILL / "SKILL.md", SKILL / "references/sections.md",
           SKILL / "references/metrics.md",
           ARCH / "true-S1.md", ARCH / "true-S2.md",
           ARCH / "brief-S1.md", ARCH / "brief-S2.md")
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
STATUS_RE = re.compile(r"^(PASS|WARN|FAIL|SKIP)\s+(\S+)\s")
# ★ `EMPTY` 必须在 `IDS` 里：它是 README §2 列为判据的那一条（fail-closed 硬失败）。
#   它只在**空节路径**出现（见 `check-section.py` 的 `main()`），干净夹具上不出现 ⇒
#   现取 `criteria` 时要把**空节夹具的输出**并进来，否则 `EMPTY` 永远进不了清单（G2）。
IDS = ["SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8", "SELF1", "SELF2", "EMPTY"]

# --------------------------------------------------------------------------
# 夹具（B 用；**不落入库件**，只写 build/）
# --------------------------------------------------------------------------

GOOD_MD = """## 4 Model Development

### 4.1 Wear volume and the tread surface

The tread of a step is treated as a rectangular surface of length X metres and width Y metres, and the survey team records every measurement in those coordinates. We divide that rectangle into a grid of m by n cells and label the centre of each cell as a control point. The grid lets a computer compare measured depths with modelled ones at the same places without any further geometric work.

Every control point carries a wear depth d that the survey team can measure with a profilometer. A survey of a complete stair produces one depth for each control point, and those depths are collected into a matrix. The matrix becomes the empirical input for every later stage of the model.

The volume lost at a control point grows with the number of times that point is stepped on. A point beside the handrail loses material slowly, while a point on the main walking line loses material much faster. Reproducing that difference is the central task of the model.

The coefficient that converts a load into a lost volume depends on the stone as well as on the load. We take its form from the classical abrasion law and keep one symbol for the coefficient that turns pressure into lost volume. The symbol is defined once and used unchanged in every later equation.

Hardness is treated as a quantity that declines slowly through time. We write it as a decaying function of age and carry the decay rate as a separate parameter of the model. Both the initial hardness and the decay rate can be estimated from petrographic inspection of the stone.

The load comes from the people who actually use the stair. We group the population by age and sex and weight every group by its share of the total. The weighted sum gives one representative body weight for the whole population that uses the building.

**Table 1** Reference mean body weights and population shares, adopted from the WHO global body-weight references as illustrative default values.

| Group | Mean weight (kg) | Share (%) |
| --- | --- | --- |
| Minors, male | 40 | 10 |
| Minors, female | 38 | 10 |
| Adults, male | 75 | 30 |
| Adults, female | 65 | 30 |
| Older adults, male | 70 | 10 |
| Older adults, female | 60 | 10 |

Multiplying the representative weight by the gravitational constant gives the load that the model uses. The load is then combined with the abrasion coefficient to predict the depth lost at each control point. A predicted depth that matches the measured depth supports the choice of coefficient.

Averaging the predicted depths over the whole tread produces a single number for the stair. That number can be compared directly with the average depth that the survey team reports for the same stair. Agreement between the two averages is the simplest check that the model has been calibrated sensibly.

Two unknowns remain once the other terms of the model are fixed. The age of the stair and the number of daily users trade off against each other, so one can be read from the other whenever the remaining parameters are known. A second relation would be needed to separate them, and the survey design should be chosen with that in mind.
"""

GOOD_TEX = """\\section{Model Development}

\\subsection{Wear volume and the tread surface}

The tread of a step is treated as a rectangular surface of length X metres and width Y metres, and the survey team records every measurement in those coordinates. We divide that rectangle into a grid of m by n cells and label the centre of each cell as a control point. The grid lets a computer compare measured depths with modelled ones at the same places without any further geometric work.

Every control point carries a wear depth $d$ that the survey team can measure with a profilometer. A survey of a complete stair produces one depth for each control point, and those depths are collected into a matrix. The matrix becomes the empirical input for every later stage of the model.

The volume lost at a control point grows with the number of times that point is stepped on. A point beside the handrail loses material slowly, while a point on the main walking line loses material much faster. Reproducing that difference is the central task of the model.

The load comes from the people who actually use the stair. We group the population by age and sex and weight every group by its share of the total. The weighted sum gives one representative body weight for the whole population that uses the building.

\\begin{table}
\\caption{Reference mean body weights and population shares, adopted from the WHO global body-weight references as illustrative default values.}
\\begin{tabular}{lcc}
Group & Mean weight (kg) & Share (\\%) \\\\
\\hline
Minors, male & 40 & 10 \\\\
Minors, female & 38 & 10 \\\\
Adults, male & 75 & 30 \\\\
Adults, female & 65 & 30 \\\\
Older adults, male & 70 & 10 \\\\
Older adults, female & 60 & 10 \\\\
\\end{tabular}
\\end{table}

Multiplying the representative weight by the gravitational constant gives the load that the model uses. The load is then combined with the abrasion coefficient to predict the depth lost at each control point. A predicted depth that matches the measured depth supports the choice of coefficient.

Averaging the predicted depths over the whole tread produces a single number for the stair. That number can be compared directly with the average depth that the survey team reports for the same stair. Agreement between the two averages is the simplest check that the model has been calibrated sensibly.
"""

INPUT_GOOD = """# 要点清单（good 夹具）

- 这一节要把测量到的磨损深度与"这台阶多少年了 / 每天多少人走"连起来。
- 踏面看成长 X 米、宽 Y 米的矩形，切成 m×n 个栅格，栅格中心记作控制点。
- 每个控制点的磨损深度记作 d，实测后汇成一个磨损矩阵，作为本节后续全部推导的经验输入。
- 磨损量与"该处被踩的次数"成正比；靠墙的格子磨损慢，走道中线的格子磨损快。
- 磨损体积系数取自经典磨损律，本节只保留一个符号，后面各式的用法保持一致。
- 硬度不是常数，随时间缓慢衰减；初始硬度与衰减率由岩相勘察估出。
- 人群按年龄与性别分组，各组按人口占比加权，得到全体使用者的代表体重。
- 参考表（来自 WHO 全球体重资料，作为本节的 illustrative 默认值）：
  六组的平均体重（kg）为 40 / 38 / 75 / 65 / 70 / 60，
  对应占比（%）为 10 / 10 / 30 / 30 / 10 / 10。
- 代表体重乘以重力加速度得到荷载；荷载再与磨损系数合成，得到每个控制点的预测深度。
- 把预测深度在整块踏面上取平均，得到一个可实测对照的平均值。
- 最后：年龄与每日人数互相制约，其余参数已知时可互解。
"""

INPUT_NONUMS = """# 要点清单（无数字版夹具；用于打 SW1 / SW2）

- 这一节要把测量到的磨损深度与台阶年龄、每日使用人数连起来。
- 踏面按矩形栅格离散，栅格中心记作控制点。
- 各控制点的实测磨损深度汇成磨损矩阵，作为本节后续推导的经验输入。
- 磨损量与踩踏次数成正比，靠墙处磨损慢，走道中线磨损快。
- 磨损体积系数取自经典磨损律，本节只保留一个符号。
- 硬度随时间缓慢衰减，初始硬度与衰减率由岩相勘察估出。
- 人群按年龄与性别分组并按占比加权，得到代表体重。
- 参考表把人群分成若干组，逐组给出平均体重与占比，具体数值见正文表格。
- 代表体重乘重力加速度得到荷载，荷载与磨损系数合成各处预测深度。
- 把预测深度在整块踏面上取平均，得到一个可实测对照的平均值。
- 年龄与每日人数互相制约，其余参数已知时可互解。
"""

FEW_MD = """## 2 Assumptions and justification

We assume that the stone of a single step is uniform enough that one hardness value describes it. Petrographic inspection of comparable steps in the same building supports that reading, and the survey team can confirm it on site without cutting the stone.

We assume that the tread keeps its shape over the period of interest. Repair work would break that assumption, and the survey notes record any repair that the team can see.

We assume that the people who use the stair are drawn from the population of the building. A stair that also serves a public passage would break that assumption, so the survey notes record whether the stair is open to outsiders.

We assume that the depth readings are accurate to the resolution of the instrument. The operator repeats a subset of readings, and the two sets are compared before the depths enter the matrix.

We assume that the age of the building is known to within a few decades. Documentary evidence usually settles the question, and where it does not the model reports the wider range that the evidence supports.
"""

PAD_PARA = ("The survey team records every depth with the same instrument, and the instrument is calibrated "
            "before each session so that readings taken on different days remain comparable with one another. "
            "A second operator repeats a fixed subset of the readings, and the two sets of numbers are compared "
            "for any systematic offset between the two observers. Any offset that is larger than the resolution "
            "of the instrument is corrected before the depths enter the matrix that the model consumes.")

# F5 / H1：三种"没有可检正文"的夹具（空文件 / 只有标题 / **只有公式**）——
#   都必须至少 FAIL，不许 `RESULT: PASS`（"只有公式"那种形态下 `SW1`/`SW2` 无表、
#   `SW3`–`SW8` 无可切句 ⇒ 八条判据一条都检不了，判 `PASS` 就是恒真型失效）。
EMPTY_MD = ""
HEADONLY_MD = "## 5 Solution and results\n"
FORMULA_ONLY_MD = "## 4.1 Model\n\n$$ E = m c^2 $$\n"

# H1：**有可检对象**、"看起来像空节"的样本 —— **不得**判 `EMPTY`：
#   一句 **<5 词** 的短散文 + 一条公式："`<5` 词不进 `SW3`/`SW7` 统计"是**解析门**，
#   与"本节有没有正文"是两件事（那一句散文**算正文** ⇒ 不判 EMPTY）。
SHORTPROSE_FORMULA_MD = "## 4.1 Model\n\nWe use the following.\n\n$$ E = m c^2 $$\n"

# H2-1：三种"看起来像空节"的样本 —— 用来钉死"纯公式行"的**一致口径**：
#   ① 只有 `\begin{alignat}` 环境（旧环境清单不含 alignat ⇒ 会被当成正文 ⇒ 判绿 ← 病）
#   ② 块级公式后多一个句号（旧口径"残留非空"救活它 ⇒ 判绿 ← 病）
#   ③ 含**行内公式**的散文行（★ 防回红：它**必须**仍是正文，不许被新判据误伤）
ALIGNAT_ONLY_MD = ("## 4.2 Model\n\n"
                   "\\begin{alignat}{2}\n"
                   "a &= b + c \\\\\n"
                   "d &= e - f\n"
                   "\\end{alignat}\n")
FORMULA_PERIOD_MD = "## 4.3 Model\n\n$$ E = m c^2 $$.\n"
INLINE_FORMULA_MD = "## 4.4 Model\n\nWe obtain $T = 18743$ from the fit.\n"

# F1：把 good.md 那张 WHO 表换成一张**合法自算结果表**（无外源、无标注串、数字搜不到）——
#     用来断言 `SW2` **只 `WARN`**（不是 `FAIL`）：判词该"提请复核"的情形没被做成"判死"。
SELFCALC_CAP_OLD = ("**Table 1** Reference mean body weights and population shares, adopted from the "
                    "WHO global body-weight references as illustrative default values.")
SELFCALC_CAP_NEW = ("**Table 1** Fitted parameters and the mean wear depth they reproduce, "
                    "computed in this section.")
SELFCALC_ROWS_OLD = ("| Group | Mean weight (kg) | Share (%) |\n"
                     "| --- | --- | --- |\n"
                     "| Minors, male | 40 | 10 |\n"
                     "| Minors, female | 38 | 10 |\n"
                     "| Adults, male | 75 | 30 |\n"
                     "| Adults, female | 65 | 30 |\n"
                     "| Older adults, male | 70 | 10 |\n"
                     "| Older adults, female | 60 | 10 |")
SELFCALC_ROWS_NEW = ("| Quantity | Value | Unit |\n"
                     "| --- | --- | --- |\n"
                     "| Fitted age | 18743 | days |\n"
                     "| Daily users | 412 | persons |\n"
                     "| Mean wear depth | 0.0031 | m |")


# --------------------------------------------------------------------------
# 工具
# --------------------------------------------------------------------------

def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))          # 一律 write_bytes（全 LF）


def run_checker(section_path, section, input_path=None, checker=CHK, extra=()):
    args = [sys.executable, str(checker), str(section_path)]
    if section is not None:
        args += ["--section", section]
    if input_path is not None:
        args += ["--input", str(input_path)]
    args += list(extra)
    pr = subprocess.run(args, cwd=str(ROOT), capture_output=True, text=True,
                        encoding="utf-8", errors="replace", env=ENV)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = STATUS_RE.match(line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def run_selfcheck(checker):
    pr = subprocess.run([sys.executable, str(checker), "--selfcheck"], cwd=str(ROOT),
                        capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = STATUS_RE.match(line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def _raw(cmdline, rc, out):
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return "$ %s   → exit=%d\n%s" % (cmdline, rc, body)


# ---- 变异变换 -------------------------------------------------------------

def _skip_block(blk):
    ls = blk.lstrip()
    return (not blk.strip()) or ls.startswith("|") or ls.startswith("**Table") or ls.startswith("#")


def _per_para(mutate, tex=False):
    """对每个散文段跑一次 mutate(段文本)；表格/表题/标题段原样保留。"""
    def f(src):
        sep = "\n\n"
        out = []
        for blk in src.split(sep):
            if _skip_block(blk):
                out.append(blk)
                continue
            out.append(mutate(blk.rstrip()))
        return sep.join(out)
    return f


def _append(extra):
    """把 extra 补成**每段的段末句**（⇒ 打 SW3：段末总结率）。"""
    return _per_para(lambda b: b + " " + extra)


def _insert_mid(insert):
    """把 insert 插到**每段倒数第二句之前**（⇒ 不是段末句、也不单独成段）。"""
    def mut(b):
        ss = re.split(r"(?<=[.!?])\s+", b.strip())
        if len(ss) >= 2:
            ss = ss[:-1] + [insert] + ss[-1:]
        else:
            ss = ss + [insert]
        return " ".join(ss)
    return _per_para(mut)


def _strip_marker(src):
    """把 `illustrative` 一类显式标注拿掉 ⇒ 打 SW2（表题仍留具名外源 `WHO`）。"""
    return re.sub(r"\s*as illustrative default values", "", src)


def _drop_table(src):
    """把表题行与管道表行整段删掉（⇒ SW1/SW2 无适用对象）。"""
    keep = [l for l in src.split("\n")
            if not l.lstrip().startswith("|") and not l.lstrip().startswith("**Table")]
    return "\n".join(keep)


def _to_selfcalc(src):
    """把 good.md 的 WHO 表换成一张**自算结果表**（无外源、无标注串、数字搜不到）。

    ⇒ `SW1` 仍 `PASS`（合取第一项"有具名外源"不成立）、`SW2` **只 `WARN`**。
    """
    if SELFCALC_CAP_OLD not in src or SELFCALC_ROWS_OLD not in src:
        raise AssertionError("selfcalc 变换：基准里找不到那张 WHO 表")
    return (src.replace(SELFCALC_CAP_OLD, SELFCALC_CAP_NEW)
               .replace(SELFCALC_ROWS_OLD, SELFCALC_ROWS_NEW))


def _pad(n):
    def f(src):
        return src.rstrip() + "\n\n" + "\n\n".join([PAD_PARA] * n) + "\n"
    return f


# --------------------------------------------------------------------------
# 变异清单
# --------------------------------------------------------------------------

class Case(object):
    def __init__(self, cid, desc, target, transform=None, input_file="good",
                 expect=None, expect_rc="zero", kind="red", checker=None):
        self.cid, self.desc, self.target = cid, desc, target
        self.transform, self.input_file = transform, input_file
        self.expect, self.expect_rc = (expect or {}), expect_rc
        self.kind, self.checker = kind, checker


def _bad_target_ids(case_list, criteria):
    """点名了**现取判据清单之外**的判据的变异 id（`truth` 类豁免：它不按 `base_md` 比对）。

    ★ **别再把 `empty` 类也豁免掉** —— `EMPTY` 已纳入 `IDS`、并靠"干净夹具输出 ∪ 空节夹具输出"
    进了现取 `criteria`（G2）；豁免 `empty` 会让"变异点名了清单外的判据"这句断言**对 `EMPTY` 恒真**。
    """
    return [c.cid for c in case_list
            if not (set(c.expect) <= set(criteria) or c.kind == "truth")]


def cases():
    R = []
    # ---- SW1 / SW2：判据本体驱动，夹具侧只动"数字能不能回输入搜到"----
    R.append(Case("MUT-SW1",
                  "表内数字改成写手输入里搜不到的（表题仍挂 `WHO`、且带 `illustrative` 标注）",
                  "good.md", None, "nonums", {"SW1": "FAIL", "SW2": "PASS"}, "nonzero"))
    R.append(Case("MUT-SW2",
                  "表题**保留具名外源**（`WHO`）、抹掉 `illustrative` 标注，数字仍搜不到"
                  "（判词 :223(d) 的合取齐备）⇒ `SW1` 与 `SW2` 都判死",
                  "good.md", _strip_marker,
                  "nonums", {"SW1": "FAIL", "SW2": "FAIL"}, "nonzero"))

    # ---- F5 / H1：没有可检正文 ⇒ 至少 FAIL，不许 RESULT: PASS ----
    R.append(Case("MUT-EMPTY", "空文件（0 字节）⇒ 至少 FAIL（`EMPTY`）、退出码非 0",
                  "empty.md", None, "good", {"EMPTY": "FAIL"}, "nonzero", kind="empty"))
    R.append(Case("MUT-HEADONLY", "只有标题、无正文 ⇒ 至少 FAIL（`EMPTY`）、退出码非 0",
                  "headonly.md", None, "good", {"EMPTY": "FAIL"}, "nonzero", kind="empty"))
    R.append(Case("MUT-FORMULAONLY",
                  "只有公式（`$$…$$`）、无散文无表 ⇒ 至少 FAIL（`EMPTY`）、退出码非 0"
                  "（那种形态 `SW1`/`SW2` 无表、`SW3`–`SW8` 无可切句 ⇒ 一条都检不了）",
                  "formulaonly.md", None, "good", {"EMPTY": "FAIL"}, "nonzero", kind="empty"))
    # ---- H2-1：把"纯公式行"的口径钉死（同一裁定下三种等价输入不许走向相反）----
    R.append(Case("MUT-ALIGNATONLY",
                  "只有 `\\begin{alignat}` 环境、无散文无表 ⇒ 至少 FAIL（`EMPTY`）、退出码非 0"
                  "（环境清单漏 `alignat` 时它会被当成正文 ⇒ 判绿）",
                  "alignatonly.md", None, "good", {"EMPTY": "FAIL"}, "nonzero", kind="empty"))
    R.append(Case("MUT-FORMULA-PERIOD",
                  "块级公式后多一个句号（`$$…$$.`）⇒ 残留只有 `.`、无字母 ⇒ 仍判 `EMPTY`、退出码非 0"
                  "（旧口径『残留非空』会把它救活 ⇒ 判绿）",
                  "formulaperiod.md", None, "good", {"EMPTY": "FAIL"}, "nonzero", kind="empty"))

    # ---- SW3–SW8：WARN（★ 同时断言退出码 = 0）----
    R.append(Case("MUT-SW3", "把每一段末尾都补成『评价/格言』句（9 段全中）",
                  "good.md", _append("That is what makes the model worth trusting."),
                  "good", {"SW3": "WARN"}, "zero"))
    R.append(Case("MUT-SW4", "灌水膨胀（追加成段的水文，正文词数 ÷ 写手输入词数越过提请复核线）",
                  "good.md", _pad(14), "good", {"SW4": "WARN"}, "zero"))
    R.append(Case("MUT-SW5", "塞满 `rather than`（对比式构造密度越过 3‰）",
                  "good.md", _insert_mid("We report the loss as a rate rather than a total."),
                  "good", {"SW5": "WARN"}, "zero"))
    R.append(Case("MUT-SW6", "塞自评套话（`the purpose of this section` / `worth stating`）",
                  "good.md", _insert_mid("The purpose of this section is to set out the "
                                         "calibration, and that point is worth stating once more."),
                  "good", {"SW6": "WARN"}, "zero"))
    R.append(Case("MUT-SW7", "连续插入极短断言句（4 词 × 多段）",
                  "good.md", _insert_mid("Hardness is not constant."),
                  "good", {"SW7": "WARN"}, "zero"))
    R.append(Case("MUT-SW8", "塞可整句删除的元话语（`Taken together, …`，占比 ≥15%）",
                  "good.md", _insert_mid("Taken together, the two components describe the same process."),
                  "good", {"SW8": "WARN"}, "zero"))

    # ---- 两条静态自检：打工具自己的源码副本 ----
    R.append(Case("MUT-SELF1", "把明令不用的判据（举例之一）字面写进工具源码副本",
                  "checker", _self1_transform, None, {"SELF1": "FAIL"}, "nonzero",
                  kind="selfcheck"))
    R.append(Case("MUT-SELF2", "把工具头部那段『压力臂局限』文字删掉",
                  "checker", _self2_transform, None, {"SELF2": "FAIL"}, "nonzero",
                  kind="selfcheck"))
    return R


def _self1_transform(src):
    # ★ 这行的**字面**就是被明令不用的四项之一（举其一项为例）；写进源码副本即应被 SELF1 抓到。
    return src.rstrip() + "\n\n# 变异注入：加一条 " + "Fle" + "sch" + " readability probe\n"


def _self2_transform(src):
    i = src.find("★ 边界 3（压力臂）")
    j = src.find("★ 边界 4（四项不用）")
    if i == -1 or j <= i:
        raise AssertionError("基准里找不到工具头部的『压力臂局限』段")
    return src[:i] + src[j:]


def controls():
    C = []
    C.append(Case("CTRL-good-md", "射程边界：干净 `.md` 夹具（含带出处的表）",
                  "good.md", None, "good", {}, "zero", kind="green"))
    C.append(Case("CTRL-good-tex", "射程边界：干净 `.tex` 夹具（`.tex` 输入也要能吃）",
                  "good.tex", None, "good", {}, "zero", kind="green"))
    C.append(Case("CTRL-prose-edit", "射程边界：只改一句普通散文（不碰表 / 词表 / 句长）",
                  "good.md", lambda s: s.replace("the classical abrasion law",
                                                 "the classical abrasion relationship"),
                  "good", {}, "zero", kind="green"))
    C.append(Case("CTRL-selfcalc",
                  "★ 合法自算结果表（无外源、无标注串、数字搜不到）⇒ `SW2` 只 `WARN`、退出码 0"
                  "（判词该『提请复核』的情形不许做成『判死』）",
                  "good.md", _to_selfcalc, "good", {"SW2": "WARN"}, "zero", kind="green"))
    C.append(Case("CTRL-few-paras", "射程边界：段数 < 6 时节节段末都写成总结句，SW3 也**不得**出 WARN"
                  "（判词 309 的 `≥6 段` 是一道门）",
                  "few.md", _append("That is what makes the model worth trusting."),
                  "good", {}, "zero", kind="green"))
    C.append(Case("CTRL-no-table", "射程边界：把表整段删掉 ⇒ SW1/SW2 无适用对象、报 PASS 而不是 FAIL",
                  "good.md", _drop_table, "good", {}, "zero", kind="green"))
    C.append(Case("CTRL-shortprose-formula",
                  "★ H1 对照：一句 <5 词短散文 + 一条公式 ⇒ **不得**判 EMPTY"
                  "（『<5 词不进 SW3/SW7 统计』是解析门，那一句散文算正文）",
                  "shortprose.md", None, "good", {}, "zero", kind="nonempty"))
    C.append(Case("CTRL-inline-formula-prose",
                  "★ H2-1 对照：含**行内公式**的散文行（`We obtain $T = 18743$ from the fit.`）"
                  "⇒ **不得**判 EMPTY（残留含字母 ⇒ 仍是正文）、exit=0",
                  "inlineformula.md", None, "good", {}, "zero", kind="nonempty"))
    C.append(Case("CTRL-truth-S1", "★ 真值 true-S1.md —— SW3–SW8 不得出 WARN",
                  "truth-S1", None, "brief-S1", {}, "any", kind="truth"))
    C.append(Case("CTRL-truth-S2", "★ 真值 true-S2.md —— SW3–SW8 不得出 WARN",
                  "truth-S2", None, "brief-S2", {}, "any", kind="truth"))
    C.append(Case("CTRL-no-input", "`--input` 缺失 ⇒ SW1/SW2 必须报『无法判定』（SKIP），不许报 PASS"
                  "（SW4 的分母也在 --input 上 ⇒ 一并 SKIP）",
                  "good.md", None, None,
                  {"SW1": "SKIP", "SW2": "SKIP", "SW4": "SKIP"}, "zero", kind="green"))
    C.append(Case("CTRL-unknown-section", "`--section` 给不认识的值 ⇒ fail-closed 红",
                  "good.md", None, "good", {}, "nonzero", kind="green"))
    return C


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("变异驱动器 · check-section.py（mcm-section-writer）：判据 SW1–SW8 逐条打红 "
          "+ SELF1/SELF2 打红 + %d 条对照" % len(controls()))
    print("=" * 78)
    print("检查器 = %s  blob %s" % (CHK.relative_to(ROOT).as_posix(), git_hash_object(CHK)))
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    # ---- 夹具 ----
    shutil.rmtree(BUILD, ignore_errors=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    write(BUILD / "good.md", GOOD_MD)
    write(BUILD / "good.tex", GOOD_TEX)
    write(BUILD / "few.md", FEW_MD)
    write(BUILD / "input-good.md", INPUT_GOOD)
    write(BUILD / "input-nonums.md", INPUT_NONUMS)
    write(BUILD / "empty.md", EMPTY_MD)             # F5：空文件
    write(BUILD / "headonly.md", HEADONLY_MD)       # F5：只有标题
    write(BUILD / "formulaonly.md", FORMULA_ONLY_MD)        # G3：只有公式
    write(BUILD / "shortprose.md", SHORTPROSE_FORMULA_MD)   # G3：<5 词短散文 + 公式
    write(BUILD / "alignatonly.md", ALIGNAT_ONLY_MD)        # H2-1：只有 alignat 环境
    write(BUILD / "formulaperiod.md", FORMULA_PERIOD_MD)    # H2-1：块级公式 + 行尾句号
    write(BUILD / "inlineformula.md", INLINE_FORMULA_MD)    # H2-1：含行内公式的散文行
    copy_checker = BUILD / "checker" / "check-section.py"
    write(copy_checker, CHK.read_bytes().decode("utf-8"))

    SECT = "模型建立"
    inputs = {"good": BUILD / "input-good.md",
              "nonums": BUILD / "input-nonums.md",
              None: None}
    targets = {"good.md": BUILD / "good.md", "good.tex": BUILD / "good.tex",
               "few.md": BUILD / "few.md",
               "empty.md": BUILD / "empty.md", "headonly.md": BUILD / "headonly.md",
               "formulaonly.md": BUILD / "formulaonly.md", "shortprose.md": BUILD / "shortprose.md",
               "alignatonly.md": BUILD / "alignatonly.md",
               "formulaperiod.md": BUILD / "formulaperiod.md",
               "inlineformula.md": BUILD / "inlineformula.md",
               "truth-S1": ARCH / "true-S1.md", "truth-S2": ARCH / "true-S2.md"}
    truth_input = {"brief-S1": ARCH / "brief-S1.md", "brief-S2": ARCH / "brief-S2.md"}

    # ---- 前置：干净夹具必须全绿；并现取判据清单 ----
    rc0, out0, base_md = run_checker(targets["good.md"], SECT, inputs["good"])
    _, _, base_tex = run_checker(targets["good.tex"], SECT, inputs["good"])
    # ★ 判据清单现取：干净夹具输出 **∪** 空节夹具输出 —— `EMPTY` 只在空节路径出现，
    #   不并进来它永远进不了 `criteria`（⇒ `bad_target` 对 `EMPTY` 恒真，见 G2）。
    _, _, base_empty = run_checker(targets["empty.md"], SECT, inputs["good"])
    criteria = [i for i in IDS if i in base_md or i in base_empty]
    base_pass_ids = [i for i in criteria if i in base_md]   # 干净夹具上应出现且全 PASS 的那些
    base_ok = (rc0 == 0 and base_md
               and all(base_md.get(i) == "PASS" for i in base_pass_ids)
               and all(base_tex.get(i) == "PASS" for i in base_pass_ids))
    print("\n前置（干净夹具 good.md / good.tex + 现取判据清单）: exit=%d · 现取 = %s"
          % (rc0, criteria))
    print("  good.md  = %s" % sorted(base_md.items()))
    print("  good.tex = %s" % sorted(base_tex.items()))
    print("  empty.md = %s（`EMPTY` 只在此路径出现，并进现取清单）" % sorted(base_empty.items()))
    print("  %s" % ("全 PASS" if base_ok else "未全绿 <<< 夹具或判据有问题"))
    if not criteria:
        print("RUN: 现取不到任何判据 ⇒ 无法变异（fail-closed）")
        return 1

    rows, ctrl_rows, failed = [], [], []
    bad_target = _bad_target_ids(cases() + controls(), criteria)
    # ★ G2 自证：「点名清单外的判据」这句断言**不恒真** —— 造一个点名**清单外**判据（`SW9`）的
    #   假 Case，它必须被 `_bad_target_ids()` 抓到；抓不到 ⇒ 断言已被架空（并入 rc_all ⇒ fail-closed 红）。
    _probe = Case("__PROBE_OUT_OF_LIST__", "(自证) 点名清单外的判据 SW9", "good.md", None,
                  "good", {"SW9": "FAIL"}, "zero", kind="red")
    bad_target_probe = _bad_target_ids([_probe], criteria)
    bad_target_probe_ok = (bad_target_probe == ["__PROBE_OUT_OF_LIST__"])

    try:
        for c in cases():
            rows.append(run_case(c, targets, inputs, SECT, base_md, criteria))
        for c in controls():
            ctrl_rows.append(run_case(c, targets, inputs, SECT, base_md, criteria,
                                      truth_input=truth_input))
    finally:
        pass

    for st, cid, desc, detail in rows + ctrl_rows:
        if st.endswith("BAD"):
            failed.append(cid)

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    for st, cid, desc, detail in rows:
        print("%-11s %-16s %s" % (st, cid, desc))
        print(detail)
    print("-" * 78)
    print("对照（`GREEN` = 该绿 / 该无 WARN）")
    for st, cid, desc, detail in ctrl_rows:
        print("%-11s %-16s %s" % (st, cid, desc))
        print(detail)

    # ---- 还原自证 ----
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    stx = subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                         capture_output=True, text=True).stdout
    dirty = sorted(l for l in stx.splitlines() if l.strip())
    rerun_rc, _, rerun_v = run_checker(targets["good.md"], SECT, inputs["good"])

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print("  %-62s blob %s  %s" % (p.relative_to(ROOT).as_posix(), now,
                                       "== 变异前" if now == guarded_before[p] else "!= 变异前 <<<"))
    print("  受保护件逐个 blob 还原: %s" % byte_ok)
    print("  变异后复跑（干净夹具）：exit=%d · %s"
          % (rerun_rc, "全 PASS" if all(rerun_v.get(i) == "PASS" for i in criteria)
             else sorted(rerun_v.items())))
    print("  全仓 `git status --short`:\n%s" % (stx if stx.strip() else "      （空）"))

    n_mut = len([c for c in cases() if c.kind == "red"])
    n_self = len([c for c in cases() if c.kind == "selfcheck"])
    n_empty = len([c for c in cases() if c.kind == "empty"])
    n_nonempty = len([c for c in controls() if c.kind == "nonempty"])
    n_ctl = len([c for c in controls() if c.kind in ("green", "truth")])
    fail_mut = [c.cid for c in cases() if c.kind == "red" and c.cid in failed]
    fail_self = [c.cid for c in cases() if c.kind == "selfcheck" and c.cid in failed]
    fail_empty = [c.cid for c in cases() if c.kind == "empty" and c.cid in failed]
    fail_nonempty = [c.cid for c in controls() if c.kind == "nonempty" and c.cid in failed]
    fail_ctl = [c.cid for c in controls() if c.cid in failed]
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print("MUT: %d/%d 达预期（判据打红：SW1 出处 / SW2 标注 / SW3 段末 / SW4 膨胀 / "
          "SW5 对比式 / SW6 自评 / SW7 短句 / SW8 可删句）%s"
          % (n_mut - len(fail_mut), n_mut,
             "" if not fail_mut else "（未达预期：%s）" % ", ".join(fail_mut)))
    print("MUT: %d/%d 达预期（静态自检打红：SELF1 禁用项入源码 / SELF2 局限文字被删）%s"
          % (n_self - len(fail_self), n_self,
             "" if not fail_self else "（未达预期：%s）" % ", ".join(fail_self)))
    print("MUT: %d/%d 达预期（空节 fail-closed：空文件 / 只有标题 / 只有公式 / 只有 alignat / "
          "公式+句号 都不许 RESULT: PASS）%s"
          % (n_empty - len(fail_empty), n_empty,
             "" if not fail_empty else "（未达预期：%s）" % ", ".join(fail_empty)))
    print("MUT: %d/%d 达预期（H1/H2-1 对照：有可检对象（<5 词短散文行 / 含行内公式的散文行）"
          "不得判 EMPTY）%s"
          % (n_nonempty - len(fail_nonempty), n_nonempty,
             "" if not fail_nonempty else "（未达预期：%s）" % ", ".join(fail_nonempty)))
    print("MUT: 对照 %d/%d 达预期（必须绿：干净 md / 干净 tex / 散文微改 / 自算结果表 SW2 只 WARN / "
          "真值两节不出 WARN / --input 缺失报不可判 / --section 未知 fail-closed）%s"
          % (n_ctl - len(fail_ctl), n_ctl,
             "" if not fail_ctl else "（未达预期：%s）" % ", ".join(fail_ctl)))
    total = n_mut + n_self + n_empty + n_nonempty + n_ctl
    print("MUT: %d/%d 达预期（合计）" % (total - len(failed), total))
    # ★ 判据逻辑全仓只许有一份：`tests/` 下不许再出现 `check-section.py` 的镜像版
    dups = sorted(p.relative_to(ROOT).as_posix()
                  for p in (ROOT / "tests").rglob("check-section.py"))
    # ★ 合计行**不是末行**：末行放"运行完整性"读数。
    print("RUN: 受保护件 blob 逐件还原=%s · 干净夹具复跑 exit=%d · 判据清单现取 %d 条 %s · "
          "变异点名了清单外的判据 %s · bad_target 自证（点名清单外判据必被抓）%s · "
          "`tests/` 下的 check-section.py 镜像 %s · "
          "全仓 `git status --short` %s"
          % (byte_ok, rerun_rc, len(criteria), criteria, bad_target or "无",
             "OK" if bad_target_probe_ok else "失败 <<<（断言已被架空）",
             dups or "无（唯一一份在 skill 目录）",
             "空" if not dirty else "非空 <<< " + "; ".join(dirty)))
    rc_all = 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty
                   and not bad_target and not dups and bad_target_probe_ok) else 1
    shutil.rmtree(BUILD, ignore_errors=True)      # ★ 自己造的临时件当场清（build/ 下）
    return rc_all


def run_case(c, targets, inputs, SECT, base_md, criteria, truth_input=None):
    cid = c.cid
    try:
        if c.kind == "selfcheck":
            src = c.transform(CHK.read_bytes().decode("utf-8"))
            if src == CHK.read_bytes().decode("utf-8"):
                return ("RED-BAD", cid, c.desc, "驱动器自己报错：变换没有改变源码")
            p = BUILD / cid / "check-section.py"
            write(p, src)
            rc, out, verdict = run_selfcheck(p)
            present = [i for i in criteria if i in verdict]
            actual = {i: verdict.get(i) for i in present}
            want = dict((i, "PASS") for i in criteria)
            want.update(c.expect)
            ok = all(actual.get(i) == want.get(i) for i in present) and \
                all(i in verdict for i in c.expect) and \
                (rc == 0) == (c.expect_rc == "zero")
            note = "" if ok else "   <<< 期望 %s · 实得 %s（exit=%d）" % (want, actual, rc)
            detail = ("变换：%s\n      期望 = %s · 实得 = %s · exit=%d %s\n"
                      % (c.desc, c.expect, actual, rc, note)
                      + _raw("check-section.py（副本）--selfcheck", rc, out))
            return ("RED-OK" if ok else "RED-BAD", cid, c.desc, detail)

        if c.kind == "empty":
            # F5：没有可检正文 ⇒ 必须至少 FAIL（`EMPTY` 红、退出码非 0），不许 RESULT: PASS。
            tgt = targets[c.target]
            inp = inputs.get(c.input_file)
            rc, out, verdict = run_checker(tgt, SECT, inp)
            ok = (rc != 0) and (verdict.get("EMPTY") == "FAIL")
            note = "" if ok else ("   <<< 期望 EMPTY=FAIL 且 exit≠0 · 实得 %s（exit=%d）"
                                  % (verdict, rc))
            detail = ("对象：%s（--input %s）\n      期望 = 至少 FAIL（`EMPTY` 红、退出码非 0）· "
                      "实得 = EMPTY=%s（exit=%d）%s\n"
                      % (c.target, c.input_file, verdict.get("EMPTY"), rc, note)
                      + _raw("check-section.py %s --section %s --input %s"
                             % (tgt.name, SECT, inp.name if inp else "-"), rc, out))
            return ("RED-OK" if ok else "RED-BAD", cid, c.desc, detail)

        if c.kind == "nonempty":
            # G3：有可检对象（公式行 / <5 词短散文行）⇒ **不得**判 EMPTY、退出码应为 0。
            tgt = targets[c.target]
            inp = inputs.get(c.input_file)
            rc, out, verdict = run_checker(tgt, SECT, inp)
            ok = (verdict.get("EMPTY") is None) and (rc == 0)
            note = "" if ok else ("   <<< 期望 不判 EMPTY 且 exit=0 · 实得 EMPTY=%s（exit=%d）"
                                  % (verdict.get("EMPTY"), rc))
            detail = ("对象：%s（--input %s）\n      期望 = 不得判 EMPTY（有可检对象）、exit=0 · "
                      "实得 = EMPTY=%s（exit=%d）%s\n"
                      % (c.target, c.input_file, verdict.get("EMPTY"), rc, note)
                      + _raw("check-section.py %s --section %s --input %s"
                             % (tgt.name, SECT, inp.name if inp else "-"), rc, out))
            return ("GREEN-OK" if ok else "GREEN-BAD", cid, c.desc, detail)

        # ---- 节文本类 ----
        tgt = targets[c.target]
        sec = tgt
        xform = None
        if c.transform is not None:
            xform = c.transform
            new = xform(tgt.read_bytes().decode("utf-8"))
            if new == tgt.read_bytes().decode("utf-8"):
                return ("RED-BAD", cid, c.desc, "驱动器自己报错：变换没有改变文本")
            sec = BUILD / cid / tgt.name
            write(sec, new)
        if c.input_file in ("brief-S1", "brief-S2"):
            inp = truth_input[c.input_file]
        else:
            inp = inputs.get(c.input_file)
        section_name = "这不是一个节名" if cid == "CTRL-unknown-section" else SECT
        rc, out, verdict = run_checker(sec, section_name, inp)
        actual = {i: verdict.get(i) for i in criteria}
        if c.kind == "truth":
            bad = [i for i in ("SW3", "SW4", "SW5", "SW6", "SW7", "SW8")
                   if actual.get(i) == "WARN"]
            ok = not bad
            note = "" if ok else "   <<< 真值上出了 WARN：%s" % bad
            detail = ("对象：%s（--input %s）\n      期望 = SW3–SW8 均不出 WARN · "
                      "实得 = %s %s\n" % (c.target, c.input_file, actual, note)
                      + _raw("check-section.py %s --section %s --input %s"
                             % (tgt.name, SECT, c.input_file), rc, out))
            return ("GREEN-OK" if ok else "GREEN-BAD", cid, c.desc, detail)

        if c.kind == "green" and cid == "CTRL-no-input":
            want = dict(base_md)
            want.update(c.expect)
        elif c.kind == "green" and cid == "CTRL-unknown-section":
            want = None
        else:
            want = dict(base_md)
            want.update(c.expect)
        if want is None:
            ok = ("FAIL" in verdict.values()) and rc != 0
            note = "" if ok else "   <<< 期望 fail-closed 红 · 实得 %s（exit=%d）" % (verdict, rc)
        else:
            ok = all(actual.get(i) == want.get(i) for i in criteria)
            if c.expect_rc == "zero" and c.kind == "green":
                ok = ok and rc == 0
            if cid in ("MUT-SW3", "MUT-SW4", "MUT-SW5", "MUT-SW6", "MUT-SW7", "MUT-SW8"):
                ok = ok and rc == 0           # ★ WARN 不许做成非 0
            note = "" if ok else "   <<< 期望 %s · 实得 %s（exit=%d）" % (want, actual, rc)
        st = ("RED-OK" if rank(c) == "red" else "GREEN-OK") if ok else \
             ("RED-BAD" if rank(c) == "red" else "GREEN-BAD")
        detail = ("变换：%s\n      期望 = %s · 实得 = %s · exit=%d %s\n"
                  % (c.desc, c.expect if want is not None else "fail-closed 红", actual, rc, note)
                  + _raw("check-section.py %s --section %s%s"
                         % (sec.name, section_name,
                            "" if inp is None else " --input " + inp.name), rc, out))
        return (st, cid, c.desc, detail)
    except AssertionError as e:
        return ("RED-BAD" if rank(c) == "red" else "GREEN-BAD", cid, c.desc,
                "驱动器自己报错：%s" % e)


def rank(c):
    return "red" if c.kind in ("red", "selfcheck", "empty") else "green"


if __name__ == "__main__":
    sys.exit(main())
