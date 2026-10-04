#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 14（`mcm-model-select`）：生成 `tests/skills/model-select/MODELSELECT-evidence.md`（RED × GREEN 对照证据）。

用法：  python tests/skills/model-select/make-evidence.py

## 它做什么

**同一件事、同一把尺**地量两侧，并把读数**机器抽取**成对照表（不手抄）：

- **同一件事**：`tests/skills/model-select/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用）+
  同一题面 `tests/skills/abs-cases/case-A-problem.txt`（**2025 MCM Problem A**，与 M2 的 RED 同源）。
- **两侧**：RED = **干净上下文写手**（**未给本 skill**）产出的「选模型 + 求解代码」；
  GREEN = **用本 skill**（`SKILL.md` + `references/` + 检查器）出的同一件事。
- **两把尺（本支的口径，与 topic-select 不同 —— 见 §0 的"可比列"）**：
  1. **产物探针**（`probe_product`）——**同一函数**逐份量两侧的**产物目录**：文件表 · 选用的**类词表** ·
     假设节 · 辨识讨论 · 代码文件 · **入口代码实跑**（`matlab -batch`）。**这一把对两侧同尺。**
  2. **skill 检查器**（`check-model-select.py`）——**它没有 `--output`**（与 `check-topic-select.py` 不同）：
     它判的是**skill 本体**，不是写手产物 ⇒ **它只对 GREEN 侧（用本 skill）有对象**，
     **RED 侧无对象（不适用）**。★ **这一点必须标出来、不许混入"可比列"。**
- **判据清单现取**：从检查器输出里读 `PASS|FAIL|SKIP  <id>` 行得到 id 集合，**不写死条数**。

## 本文件必须如实写清的四件事

1. **RED 是自变量**：`red/out-R{1,2,3}/**` 是**写手的字节**（照实入库，本轮未改）。
2. **预测写在前**（`red/README.md` §1，**先于写手入库**）⇒ 本节 §6 逐条回填**实际（含没发生的）**。
3. **诚实边界**：**本轮的"尺"只量机械层**（`MS3` 判不了"参照是否真独立"；本轮的 GREEN **不代表真实赛期表现**）；
   **真实赛期是"题面刚放出、你手上还没有任何建模素材"，而本轮双方都拿到了同一仓库** ⇒ **不声称覆盖真实赛期**（§7）。
4. **样本量边界**：**n = 1 道题 × 3 位 RED 写手 × 1 位 GREEN 写手**（§0、§7）⇒ **不许写成"普遍规律"**。

## 环境旁路（**照实披露**，§0）

写手是本机 Claude Code 的 agent，会话级上下文里另有三处可见面：**skill 列表**里 `mcm-model-select` 那一行的
**描述**（它点了名"两跳 / 候选模型 + 判据 / 带推翻条件的推荐 / 六格详情"）· `git status` 快照 · **Recent commits**。
★ **本轮这不是"没泄漏"**：RED 的 R3 产物里出现了 **`六格` / `推翻条件`** 这类**本 skill 描述里的词**
（机器抽取见 §2、§6）⇒ **R3 已被环境旁路污染**。★ **2026-10-04 Task 14 复核发现①订正**：本行**原写**
"（R1/R2 未抽到同类词…）"是**无限定、可一秒推翻**的声明 —— 补探两个描述词后实测 **R2 含 `候选模型`×1 · R3 另含 `判据`×3**
⇒ **只有 R1 全净**（详见 §0 的逐份读数）。**照实披露。**
"""
import hashlib
import importlib.util
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/model-select
REPO = HERE.parents[2]                                   # 仓根
CHECK = REPO / ".claude/skills/mcm-model-select/check-model-select.py"
BRIEF = HERE / "red" / "brief.md"
PROBLEM = REPO / "tests/skills/abs-cases/case-A-problem.txt"
OUT_DOC = HERE / "MODELSELECT-evidence.md"
NL = chr(10)

# 八个类名（EN + CN）—— 用于**机器抽取**"两侧各用了哪些类词"。★ 这只是"词"，不是"选对了没有"的判据。
CLASS_EN = ["evaluation", "prediction", "optimization", "mechanism",
            "simulation", "statistics", "network", "ml"]
CLASS_CN = {"evaluation": "评价", "prediction": "预测", "optimization": "优化",
            "mechanism": "机理", "simulation": "仿真", "statistics": "统计",
            "network": "网络", "ml": "机器学习"}

LINE_RE = re.compile(r"^(PASS|FAIL|SKIP)\s+(\S+)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)?(?:  \[SKIP (.*)\])? *$")

# 标签 → (产物目录, 侧)。顺序 = 报告里出现的顺序。
RED_ARMS = [("R1", HERE / "red" / "out-R1"), ("R2", HERE / "red" / "out-R2"),
            ("R3", HERE / "red" / "out-R3")]
GREEN_ARM = ("G1", HERE / "green" / "out-G1")


def all_arms():
    return RED_ARMS + [GREEN_ARM]


def run(cmd, timeout=1800):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8", errors="replace")
    out = r.stdout or ""
    if (r.stderr or "").strip():
        out += "STDERR: " + r.stderr.strip() + NL
    return out, r.returncode


def git_hash_object(p):
    return run(["git", "hash-object", str(p)])[0].strip()


# ---------------------------------------------------------------- 尺 1：产物探针（两侧同尺）
ZEROARG_GUARD = re.compile(r"if\s+nargin\s*(?:==\s*0\b|==\s*1\b|<=\s*1\b|<\s*1\b)")


def find_entryproduct(d):
    """在产物目录里**机器识别**入口 `.m`：文件名 == 首个函数名，**且零参可调**
    （签名零参 / `varargin` / 有**允许零参**的 `nargin` 守卫 `==0` / `==1` / `<1` / `<=1`）。
    ★ **只认"允许零参"的守卫** —— `if nargin < 6` 那种（如 `wear_ci`）**不算**入口
    （本支第一版曾把它误判为入口 ⇒ 实测 rc=1 的假红；已收紧）。"""
    entries = []
    for f in sorted(pathlib.Path(d).glob("*.m")):
        txt = f.read_bytes().decode("utf-8", "replace")
        m = re.search(r"^\s*function\s+(?:\[[^\]]*\]\s*=\s*|\w+\s*=\s*)?(\w+)\s*\(([^)]*)\)",
                      txt, re.M)
        if not m:
            continue
        name, arglist = m.group(1), m.group(2).strip()
        if name != f.stem:
            continue
        if arglist == "" or "varargin" in arglist or ZEROARG_GUARD.search(txt):
            entries.append((f.stem, f))
    return entries


def probe_product(d):
    """**同一函数**逐份量一个产物目录。返回机器抽取的读数（不含判断）。"""
    d = pathlib.Path(d)
    files = sorted([p for p in d.rglob("*") if p.is_file()], key=lambda p: p.name)
    md = None
    for p in files:
        if p.suffix == ".md" and p.name == "selection.md":
            md = p
    text = md.read_bytes().decode("utf-8") if md else ""
    low = text.lower()
    cls = {}
    for k in CLASS_EN:
        n = len(re.findall(r"\b" + re.escape(k) + r"\b", low))
        n += text.count(CLASS_CN[k])
        if n:
            cls[k] = n
    fences = len(re.findall(r"```\s*matlab", text, re.I))
    mfiles = [p for p in files if p.suffix == ".m"]
    out = {
        "dir": d,
        "n_files": len(files),
        "total_bytes": sum(p.stat().st_size for p in files),
        "md_bytes": (md.stat().st_size if md else 0),
        "md_lines": (len(text.splitlines()) if md else 0),
        "classes": cls,
        "assum_head": _heading_hits(text, r"假设|assum"),
        "assum_all": len(re.findall(r"假设|assum", text, re.I)),
        "identif": len(re.findall(r"可辨识|辨识|identif", text, re.I)),
        "falsify": len(re.findall(r"推翻|falsif", text, re.I)),
        "sixcell": len(re.findall(r"六格|six[ -]?cell", text, re.I)),
        "skeleton": len(re.findall(r"骨架|skeleton", text, re.I)),
        # ★ 本 skill `description` 里的另两个词（2026-10-04 Task 14 复核发现①补探）：
        "candmodel": len(re.findall(r"候选模型", text)),
        "crit": len(re.findall(r"判据", text)),
        "fences": fences,
        "mfiles": [p.name for p in mfiles],
        "entries": [],
        "run": None,
    }
    for stem, f in find_entryproduct(d):
        out["entries"].append((stem, f))
    return out


def _heading_hits(text, pat):
    hits = []
    for ln in text.splitlines():
        if re.match(r"^\s{0,3}#{1,6}\s", ln) and re.search(pat, ln, re.I):
            hits.append(ln.strip())
    return hits


def run_entry(d, stem):
    """**同一把尺**跑入口代码：`matlab -batch "addpath('<dir>'); <stem>"`。"""
    script = f"addpath('{pathlib.Path(d).as_posix()}'); {stem}"
    out, rc = run(["matlab", "-batch", script])
    return {"cmd": f'matlab -batch "addpath(\'<arm dir>\'); {stem}"', "rc": rc, "stdout": out.rstrip(NL)}


# ---------------------------------------------------------------- 尺 2：skill 检查器
def check(scope):
    cmd = [sys.executable, CHECK.relative_to(REPO).as_posix(), "--scope", scope]
    out, rc = run(cmd)
    cells, order, result, skip = {}, [], None, None
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1), m.group(3).strip())
            order.append(m.group(2))
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
            if m.group(3):
                skip = m.group(3)
    return {"scope": scope, "cmd": " ".join(str(c) for c in cmd), "stdout": out.rstrip(NL),
            "rc": rc, "cells": cells, "order": order, "result": result, "skip": skip}


def criteria_ids(*data):
    ids = []
    for d in data:
        for k in d["order"]:
            if k not in ids:
                ids.append(k)
    return ids


def load_checker():
    spec = importlib.util.spec_from_file_location("_ms_check", str(CHECK))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ================================================================ 手写块（判断层）
PRED_ACTUAL = """**这一节是判断层，机械读数判不了它。** 上表（§5）的读数是**机器抽取**；下表的**结论是人工**，
逐条写、**含"没发生的"**。★ 逐条**以 §2/§3 的机器读数为据**（不另编数字）。

| # | 预测（**写在前**，`red/README.md` §1） | RED 实际（R1/R2/R3） | GREEN 实际（G1） | 判定 |
| :-- | :-- | :-- | :-- | :-- |
| `P1` | **选错类**：不按"类"的框架组织、直接跳到具体方法；把**反问题**当**正向**建模 | ★ **没发生（3/3）**：三位**都选了"磨损累积律 + 反演"**这一**机理（mechanism）**族模型；**都把"从磨损反推人流"当反问题**处理 | 选 **mechanism**（主类）+ 参数辨识（反演） | ★ **预测被推翻**（两侧**选到同一类**：mechanism） |
| `P1b` | （§1 表未单列，**落地时补记**）**说不说得出"类"** | **R1：类词命中 0**；**R2/R3：命中 5 个类词**（§2） | **G1：8 个类词都在、且点名主类 `mechanism`×36**（§2） | ★ **拆开的现象**：**选对了类 ≠ 说得出类名**（R1 与 GREEN 同族模型，却一个类词也不给） |
| `P2` | **用不存在的函数**：MATLAB 里出现幻觉 / 拼错的函数名 ⇒ 运行报 `Undefined function` | ★ **没发生（3/3）**：三份入口代码**都 rc=0、实跑通过**（§2 的实跑读数） | ★ **没发生**：入口代码 rc=0（§3） | ★ **预测被推翻**（这一条本轮**两个预测位**都指向"会发生"，实测"没发生"）—— 见 §7 的"边界" |
| `P3` | **骨架跑不通**：代码跑不起来 / 跑不完 | ★ **没发生（3/3）**：三份入口代码**都 rc=0**、有输出（§2） | ★ **没发生**：入口代码 rc=0（§3） | ★ **预测被推翻** |
| `P4` | **把假设当已知**：把一批数值 / 关系当既成事实、**不单列假设** | ★ **没发生（3/3）**：三份产物**都有显式假设 / 局限节**（§2 的 `assum_head` 非空） | ★ 有显式假设节（§3） | ★ **预测被推翻** |
| `P5` | **无参数辨识**：不提"哪些参数从题面给不出来" | ★ **没发生（3/3）**：三份**都点了辨识问题**（R1「`b` 是辨识最弱的参数」；R2「`α/Δμ` 不可辨识 ⇒ 自信的错答案」；R3「纯磨损下人多人少不可辨识」） | ★ 点了（§3） | ★ **预测被推翻** |

★★ **一条必须写死的读法**（别把"预测被推翻"读成"本 skill 没用"）：**这五条预测是设计 §6 写死的"预期失败模式"，
本轮在这道题上"没发生"** —— 原因见 §7：**这道题（2025 A）的类与法几乎是"题面直接指出来"的**
（"踏面被磨凹" + "随时间累积" ⇒ 累积律 + 反演），**不够刁**，**不足以把本 skill 的价值区分出来**。
⇒ **本节结论的射程 = 这一道题、这一批写手；不许外推**（§7 的样本量边界）。

★ **另记一条 RED 侧的差异（机器读数，不是预测）**：**R1 产物里"类词"命中 0**（§2）——
它**给出的模型与 GREEN 同族，却没有用"类"这个词** ⇒ 说明**"能否明确点出类"在本轮 RED 里不稳**
（3 位里 1 位 0 命中、2 位有命中）。**本行不声称穷尽**：只报**实际抽到**的。"""

HONESTY = """**这一节照 `TOPICSELECT-evidence.md` 的写法，逐条写清本轮测不到的东西。**

### 7.1 ★★ 本轮的"尺"只量机械层（`MS3` 那型的同族）

- `MS3` **判不了"参照是否真的独立"**（设计 §5 末写死）—— 它只判"参照记录在场 + 四要素齐"。
  ★ **本轮的 GREEN 用到了 `MS3` 覆盖的骨架**（它的推荐骨架 `param_id_stability.m`）；
  **GREEN 的 `MS3` 绿**只说明**那份参照记录在、四要素齐**，**不说明参照真的与骨架不同源**。
- ★ **同族**：**本轮的 GREEN 不代表真实赛期表现** —— 它只是**一份干净上下文写手用本 skill 产出的一次结果**。

### 7.2 ★★ 本轮测不到的真实赛期情形（M4 的对应物）

- **真实赛期是"题面刚放出、你手上还没有任何建模素材"**；而**本轮双方（RED/GREEN）都拿到了同一仓库**
  （写手是本机 Claude Code 的 agent，能看到 `corpus/**`、别的 skill、本仓的 git 历史）。
  ⇒ **本轮复现不了"零素材"那一情形**。**不声称覆盖真实赛期。**
- ★ **加剧这一条的**：**2025 A 的题面本身把"类"与"法"点得很明**（"踏面被磨凹" + "常年的磨损" ⇒ 累积律 + 反演）
  ⇒ **n = 1 道题的 RED，区分力天然弱**（见 §6）。

### 7.3 ★★ 样本量边界（**原话**）

> **本轮样本量：`n = 1` 道题（2025 MCM Problem A）× `3` 位 RED 写手 × `1` 位 GREEN 写手。**
> **n 小 ⇒ 本证据件里的任何"两侧都/都不"一律只是"这一次的读数"，不得写成"普遍规律"。**

### 7.4 ★★ 一条**不许**做的读法

- **不许**把本轮的"预测被推翻"读成**"写手不看 skill 也做得一样好"**：
  **3 位 RED 也都实跑了代码、都写了假设与辨识**是**这一道题**上的读数；**换一道更刁的题未必如此**（§7.2）。
- **不许**把 **GREEN 的 `MS1`–`MS6` 全绿**读成"GREEN 的产物质量被 `MS` 判据背书"：
  `MS` 判的是**skill 本体**（索引 / 骨架 / 参照 / 边界声明），**不判这份 `selection.md` 写得好不好**。
  ★ **GREEN 的产物没有任何一条 `MS` 判据去量它**（§5 的"不可比列"）。"""


def main():
    mod = load_checker()
    allres = check("all")
    idxres = check("index-self")
    CRIT = criteria_ids(allres, idxres)
    # ★ 这一行是**故意的 tripwire**，**不是**"写死条数"：判据清单本身由**上一行现取**
    #   （从检查器 stdout 读 `PASS|FAIL|SKIP <id>`）。本行只把"现取到的东西"钉在**本支已知的这 6 条**上 ——
    #   一旦上游增/删判据，宁可**当场炸**请人来核，也**不**静默跟着变（否则 §5 的汇总表会悄悄漂移）。
    assert CRIT == ["MS1", "MS2", "MS3", "MS4", "MS5", "MS6"], "判据清单变了：%s" % CRIT
    assert allres["result"][0], "skill 检查器（--scope all）非全绿：%s" % allres["stdout"]

    probes = {tag: probe_product(d) for tag, d in all_arms()}
    # ★ 入口代码实跑（同一把尺）：逐臂跑它自己的入口
    for tag, d in all_arms():
        ents = probes[tag]["entries"]
        if ents:
            stem = ents[0][0]
            probes[tag]["run"] = run_entry(d, stem)
            probes[tag]["run"]["entry"] = stem

    brief_bytes = BRIEF.read_bytes().decode("utf-8")
    prob_bytes = PROBLEM.read_bytes().decode("utf-8")
    prob_blob = git_hash_object(PROBLEM.relative_to(REPO).as_posix())
    brief_blob = git_hash_object(BRIEF.relative_to(REPO).as_posix())
    chk_blob = git_hash_object(CHECK.relative_to(REPO).as_posix())

    meta = {}
    for tag, d in all_arms():
        rows = []
        for p in sorted(pathlib.Path(d).rglob("*")):
            if p.is_file():
                b = p.read_bytes()
                rows.append((p.name, len(b), len(b.decode("utf-8", "replace").splitlines()),
                             b.count(b"\r"),
                             git_hash_object(p.relative_to(REPO).as_posix())))
        meta[tag] = rows

    L = []
    a = L.append
    a("# Task 14 · RED × GREEN 对照证据（`mcm-model-select`）")
    a("")
    a("本文件由 `tests/skills/model-select/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("**§2 / §3 / §4（原始读数）· §5（对照表）· §9（blob）是机器抽取**（逐格解析检查器 stdout、"
      "逐份扫产物、**实跑 MATLAB**）；**§6 的性质判定 · §7 的诚实边界是手写**（文里已标明）。")
    a("")

    # ---------------- §0
    a("## §0 口径（同一件事 · **两把尺** · 可比列 vs 不可比列 · 样本量边界）")
    a("")
    a("- **同一件事**：`tests/skills/model-select/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联）"
      " ＋ 同一题面 `tests/skills/abs-cases/case-A-problem.txt`（**2025 MCM Problem A**，与 M2 的 RED 同源）。")
    a("- **两侧**：RED = **干净上下文、未用 `fork`、未给本 skill** 的写手产出的「选模型 + 求解代码」（3 位）；"
      "GREEN = **用本 skill**（`SKILL.md` + `references/` + 检查器）出的同一件事（1 位）。")
    a("- ★★ **两把尺（本支口径，与 `topic-select` **不同** —— 那支的检查器有 `--output`，本支没有）**：")
    a("  1. **产物探针**（`probe_product`）：**同一函数**逐份量**产物目录**（文件 / 类词 / 假设节 / 辨识讨论 / "
      "代码文件 / **入口代码实跑**）。★ **这一把对两侧同尺 ⇒ 它给出的列是“可比列”。**")
    a("  2. **skill 检查器** `check-model-select.py`：**它没有 `--output`** —— 它判的是 **skill 本体**，"
      "**不是写手产物** ⇒ ★ **它只对 GREEN 侧（用本 skill）有对象；RED 侧无对象（不适用）** ")
    a("     ⇒ **它给出的列是“不可比列”，不许混进对照表当两侧同尺。**")
    a("- **判据清单现取**：本支 **%d 条**（`%s`）—— 读检查器 stdout 的 `PASS|FAIL|SKIP  <id>` 行，**不写死条数**"
      "（先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。" % (len(CRIT), "、".join(CRIT)))
    a("- **检查器自证**：工作树 blob `%s`（**本支不动检查器**；两侧用的是同一版）。" % chk_blob[:12])
    a("- **题面自证**：`tests/skills/abs-cases/case-A-problem.txt` blob `%s`。" % prob_blob[:12])
    a("- **brief 自证**：`tests/skills/model-select/red/brief.md` blob `%s`（§1 全文内联）。" % brief_blob[:12])
    a("- **RED 是自变量**：三份写手产物**照实入库**（本轮未改）。逐件读数：")
    a("")
    a("| 产物 | 侧 | 文件 | 字节 | 行数 | CR（`\\r` 数） | 工作树 blob |")
    a("| :-- | :-- | :-- | --: | --: | --: | :-- |")
    for tag, _d in all_arms():
        side = "RED" if tag.startswith("R") else "GREEN"
        for name, b, ln_, cr, bl in meta[tag]:
            a("| `%s/%s` | %s | %s | %d | %d | %d | `%s` |" % (tag, name, side, name, b, ln_, cr, bl[:12]))
    a("")
    a("★ **`CR` 列是一处如实登记**：写手产物**照实入库、本轮不改**（含**换行符**）—— "
      "所以若某份写手件落盘时是 **CRLF**，这里就照实记它的 `CR > 0`（本支的 **G1 `stair_wear_archard.m` = %d**）。"
      "★ **本仓 `CRLF=0` 纪律管的是“我方作者件”**（本证据件与生成器都是全 LF）；"
      "**写手产物沿既有先例保留其原始字节**（先例：`tests/skills/table/red/out-R2/table.tex` 等既有写手件同样带 CR）。"
      % meta["G1"][[r[0] for r in meta["G1"]].index("stair_wear_archard.m")][3])
    a("")
    a("- ★★ **样本量边界（**原话**）**：**`n = 1` 道题 × `3` 位 RED 写手 × `1` 位 GREEN 写手 ⇒ "
      "任何“两侧都/都不”只是“这一次的读数”，不得写成“普遍规律”。**")
    a("- ★★ **环境旁路（照实披露）**：写手是本机 Claude Code 的 agent，会话级上下文里另有三处可见面 —— "
      "① **skill 列表**里 `mcm-model-select` 那一行的**描述**（点了名“两跳 / 候选模型 + 判据 / 带推翻条件的推荐 / "
      "六格详情”）；② `git status` 快照；③ **Recent commits**。★ **本轮这不是“没泄漏”**："
      "**RED 的 R3 产物里抽到了 `六格`（%d）与 `推翻`（%d）** —— 那是**本 skill 描述里的词**（§2、§6）"
      "⇒ **R3 已被环境旁路污染**。★ **“未抽到” ≠ “没读到”**（只有自报，没有沙箱可证）。"
      % (probes["R3"]["sixcell"], probes["R3"]["falsify"]))
    _cm = {t: probes[t]["candmodel"] for t in ("R1", "R2", "R3")}
    _cr = {t: probes[t]["crit"] for t in ("R1", "R2", "R3")}
    _sc = {t: probes[t]["sixcell"] for t in ("R1", "R2", "R3")}
    _fa = {t: probes[t]["falsify"] for t in ("R1", "R2", "R3")}
    _sk = {t: probes[t]["skeleton"] for t in ("R1", "R2", "R3")}
    a("- ★★ **污染面逐份给（2026-10-04 Task 14 复核发现①补探 —— 本行原写“R1/R2 未抽到同类词”，"
      "是无限定、可一秒推翻的声明，已按实测改写）**："
      "`候选模型` R1=**%d** R2=**%d** R3=**%d**；`判据` R1=**%d** R2=**%d** R3=**%d**；"
      "`六格` R1=**%d** R2=**%d** R3=**%d**；`推翻` R1=**%d** R2=**%d** R3=**%d**；"
      "`骨架` R1=**%d** R2=**%d** R3=**%d**。"
      "⇒ **只有 R1 全净；R2 命中 `候选模型`×%d；R3 命中多处**。"
      "⇒ **不得读成“R1/R2 未抽到同类词”**（复核命令：`grep -c 候选模型 "
      "tests/skills/model-select/red/out-R2/selection.md` ⇒ **%d**）。"
      "★ **强指纹（`## …六格` / `…推翻条件` 标题）仍是本件已披露的那两处** ⇒ **实质污染未隐瞒**，"
      "多出的是**通用词、信号弱**；★ 污染再宽**只会把 RED 推向“更不盲”，不动结论方向**。"
      % (_cm["R1"], _cm["R2"], _cm["R3"],
         _cr["R1"], _cr["R2"], _cr["R3"],
         _sc["R1"], _sc["R2"], _sc["R3"],
         _fa["R1"], _fa["R2"], _fa["R3"],
         _sk["R1"], _sk["R2"], _sk["R3"],
         _cm["R2"], _cm["R2"]))
    a("- ★ **另一处旁路（2026-10-04 Task 14 复核发现②）**：`red/out-R3/selection.md` **复现了本仓的内部口号**"
      "（“判据恒真与‘声明超过事实’是同一类错误…凡列证据都写明‘不声称穷尽’”）—— 该句**不在 brief、不在题面、"
      "也不在最近提交主题行**，疑**继承自写手 agent 的 `CLAUDE.md` / 记忆文件**（**未证**）⇒ "
      "**RED 臂“不盲”的不止 skill 描述一面**。★ 如实登记，**未重跑、未换人**（与发现①同处置）。")
    a("")

    # ---------------- §1
    a("## §1 同一件事（逐字内联；RED 与 GREEN 共用）")
    a("")
    a("```text")
    a(brief_bytes.rstrip(NL))
    a("```")
    a("")
    a("★ **中立性抉择**：brief **只问**「选模型 + 给可跑的求解代码」，**不含**本 skill 的任何契约词"
      "（不提“两跳”“类索引”“六格”“判据”“骨架路径”）、**不含**任何来源（不给本 skill、不给语料、不给判据、"
      "不给本任务书）。**唯一**算限定的一句是 **“用 MATLAB”** —— 它**不是** skill 内容，"
      "是为了让**两侧的“代码能不能跑”落在同一把尺上**（GREEN 的骨架也是 MATLAB）。")
    a("")
    a("★ **题面（权威副本在 `tests/skills/abs-cases/case-A-problem.txt`；此处不重复内联）**："
      "2025 MCM Problem A「Testing Time: The Constant Wear On Stairs」（%d 字节）。" % len(prob_bytes.encode("utf-8")))
    a("")

    # ---------------- §2 RED
    a("## §2 RED 原始读数（三位干净上下文写手 · 只给 brief + 题面）")
    a("")
    a("### §2.1 机器抽取：产物特征（`probe_product`，同一函数）")
    a("")
    a("| 产物 | 文件数 | 总字节 | `selection.md` 行 | 抽到的**类词** | 假设节标题 | 假设词命中（全篇） | 辨识命中 | 推翻命中 | 六格命中 | 骨架命中 | ```matlab 围栏 | `.m` 文件 |")
    a("| :-- | --: | --: | --: | :-- | :-- | --: | --: | --: | --: | --: | --: | :-- |")
    for tag, _d in all_arms():
        p = probes[tag]
        cls = "、".join("%s×%d" % (k, v) for k, v in sorted(p["classes"].items(), key=lambda x: -x[1])) or "（无）"
        ah = ("有（%d）" % len(p["assum_head"])) if p["assum_head"] else "（无）"
        a("| %s | %d | %d | %d | %s | %s | %d | %d | %d | %d | %d | %d | %s |" % (
            tag, p["n_files"], p["total_bytes"], p["md_lines"], cls, ah, p["assum_all"], p["identif"],
            p["falsify"], p["sixcell"], p["skeleton"], p["fences"],
            "、".join("`%s`" % m for m in p["mfiles"]) or "（无）"))
    a("")
    a("★ **这张表里的“类词”只是词频**（EN 名 + CN 别名在 `selection.md` 里的命中数），"
      "**它不判“选对了类没有”** —— 后者是 §6 的判断层。**本表不声称穷尽**（只抽这一组词）。")
    a("")
    a("### §2.2 机器抽取：**入口代码实跑**（同一把尺 · `matlab -batch`）")
    a("")
    for tag, _d in all_arms():
        p = probes[tag]
        if not p["run"]:
            a("**%s**：**未识别出入口 `.m`** ⇒ 不实跑。" % tag)
            a("")
            continue
        r = p["run"]
        a("**%s**（入口 = `%s`）" % (tag, r["entry"]))
        a("")
        a("```")
        a("$ " + r["cmd"])
        a(r["stdout"] if r["stdout"] else "(无输出)")
        a("[exit=%d]" % r["rc"])
        a("```")
        a("")

    # ---------------- §3 GREEN
    a("## §3 GREEN 原始读数（用本 skill 的同一件事）")
    a("")
    a("（§2.1 的特征表与 §2.2 的实跑表**已含 G1**；本节只把 GREEN 侧的**检查器**读数单列 —— 见 §4。）")
    a("")

    # ---------------- §4 检查器
    a("## §4 检查器读数（`check-model-select.py` · **机器抽取**；★ 判的是 skill 本体，不是写手产物）")
    a("")
    for d in (allres, idxres):
        a("### `--scope %s`" % d["scope"])
        a("")
        a("```")
        a("$ " + d["cmd"])
        a(d["stdout"])
        a("[exit=%d]" % d["rc"])
        a("```")
        a("")
    a("★ **状态图例**：`PASS` / `FAIL` / `SKIP`。★ `--scope index-self` 的 `MS1` 是 **`SKIP`**"
      "（该面按定义不含方法文件 —— **这不是“通过”**）。")
    a("")

    # ---------------- §5 对照表
    a("## §5 对照表（机器抽取）")
    a("")
    a("### §5.1 ★★ 可比的列（**产物探针**，两侧同尺）")
    a("")
    a("| 列（机器抽取） | R1 | R2 | R3 | G1 | 两侧同尺？ |")
    a("| :-- | :-- | :-- | :-- | :-- | :-- |")
    def cell(tag, key):
        return probes[tag][key]

    a("| 产物文件数 | %d | %d | %d | %d | **是** |" % tuple(probes[t]["n_files"] for t in ("R1", "R2", "R3", "G1")))
    a("| 入口 `.m` | %s | %s | %s | %s | **是** |" % tuple(
        ("、".join("`%s`" % e[0] for e in probes[t]["entries"]) or "（无）") for t in ("R1", "R2", "R3", "G1")))
    a("| 入口实跑 exit | %s | %s | %s | %s | **是** |" % tuple(
        (str(probes[t]["run"]["rc"]) if probes[t]["run"] else "—") for t in ("R1", "R2", "R3", "G1")))
    a("| 入口实跑有输出 | %s | %s | %s | %s | **是** |" % tuple(
        ("是" if (probes[t]["run"] and probes[t]["run"]["stdout"]) else "否") for t in ("R1", "R2", "R3", "G1")))
    a("| 抽到的类词（个） | %d | %d | %d | %d | **是** |" % tuple(len(probes[t]["classes"]) for t in ("R1", "R2", "R3", "G1")))
    a("| 假设节标题 | %s | %s | %s | %s | **是** |" % tuple(
        ("有" if probes[t]["assum_head"] else "无") for t in ("R1", "R2", "R3", "G1")))
    a("| 假设词命中（全篇） | %d | %d | %d | %d | **是** |" % tuple(probes[t]["assum_all"] for t in ("R1", "R2", "R3", "G1")))
    a("| 辨识讨论命中 | %d | %d | %d | %d | **是** |" % tuple(probes[t]["identif"] for t in ("R1", "R2", "R3", "G1")))
    a("| 推翻条件命中 | %d | %d | %d | %d | **是** |" % tuple(probes[t]["falsify"] for t in ("R1", "R2", "R3", "G1")))
    a("| `.m` 文件数 | %d | %d | %d | %d | **是** |" % tuple(len(probes[t]["mfiles"]) for t in ("R1", "R2", "R3", "G1")))
    a("")
    a("★ **上表每一列都两侧同尺**（同一个 `probe_product` / 同一个 `run_entry` 跑的）⇒ 它是对照表的**主体**。")
    a("")
    a("### §5.2 ★★ 不可比的列（**skill 检查器** —— **只有 GREEN 侧有对象**）")
    a("")
    a("| 判据 | 打的是（机制） | `--scope all` | `--scope index-self` | RED 侧 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    MSDESC = {
        "MS1": "六格齐备（每个方法文件）",
        "MS2": "引用的盘上素材路径存在",
        "MS3": "每个骨架有参照记录（四要素齐）",
        "MS4": "骨架可跑 + 遮蔽守卫",
        "MS5": "边界声明在场",
        "MS6": "类索引 ↔ 实际方法文件（双向一致）",
    }
    for k in CRIT:
        st_all = allres["cells"].get(k, ("", ""))[0]
        st_idx = idxres["cells"].get(k, ("", ""))[0]
        a("| `%s` | %s | %s | %s | **不适用（无对象）** |" % (k, MSDESC.get(k, ""), st_all, st_idx))
    a("")
    a("★ **这两列不可比**：`check-model-select.py` **没有 `--output`**（与 `check-topic-select.py` 不同）——"
      "它判的是 **skill 本体**（索引 / 骨架 / 参照 / 边界声明），**不是写手产物**。")
    a("  ⇒ ★★ **RED 侧没有 skill 本体可以喂给它** ⇒ **RED 在这几列上“无对象”**，"
      "**不许把 RED 的“空”当成“红”或“绿”**。")
    a("  ★ **同族**：**GREEN 的产物 `selection.md` 也没有任何一条 `MS` 判据去量它** —— "
      "`MS1`–`MS6` 全绿只说明 **skill 本体**齐备，**不说明这份产物写得好**（§7.4）。")
    a("")
    a("### §5.3 检查器逐判词（机器抽取；判词原文，不手抄）")
    a("")
    a("| 面 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- |")
    for d in (allres, idxres):
        for k in CRIT:
            if k in d["cells"]:
                st, txt = d["cells"][k]
                a("| `%s` | %s | %s | %s |" % (d["scope"], k, st, txt))
    a("")

    # ---------------- §6
    a("## §6 ★ 预测（**写在前**）vs 实际（逐条，含没发生的）")
    a("")
    a(PRED_ACTUAL)
    a("")

    # ---------------- §7
    a("## §7 诚实边界")
    a("")
    a(HONESTY)
    a("")

    # ---------------- §8
    a("## §8 可重放性（通则 14）—— 先干净 → 捕获 → 提交 → 再跑一次证不动点")
    a("")
    a("- **本文件完全由生成器当场产出**：`python tests/skills/model-select/make-evidence.py`。")
    a("  ★ 它**实跑**：`check-model-select.py`（两次 · 含 `MS4` 的 MATLAB）＋ **四份入口代码各一次**（MATLAB）。")
    a("- **不动点的证法**：在**已提交的树上**重跑本生成器 ⇒ **本文件逐字节不变**"
      "（证法：跑后 `git status --short` 仍为空）。")
    a("  ★★ **边界（照实说）**：不动点依赖两件**不完全由本器控制**的事 ——（i）检查器的 `MS4` 每跑一次会"
      "**实调 MATLAB**（本机已知**退出期自崩**现象，见检查器“已知边界”第 5 条）：若某次自崩触发**有界重试**，"
      "该次 `MS4` 判词会**多一段重试回显** ⇒ 本文件**不再逐字节相等**；"
      "（ii）四份写手代码**实跑**：本轮**实测两跑逐字节相同**（§8 末的读数），但这是一个**观测事实、不是保证**。")
    a("- **判据非空泛（失败方向的另一条臂）**：`tests/skills/model-select/mutate-model-select.py` 的读数"
      "（**本生成器不执行该驱动器**，故**不声称当场跑过**；复跑命令见收工门）。它证明 `MS1`–`MS6` **逐条真红**、"
      "两条空集反证、四条“必须仍绿”对照。")
    a("")

    # ---------------- §9
    a("## §9 生成器口径与数据来源（机器抽取）")
    a("")
    a("- 生成器 `tests/skills/model-select/make-evidence.py` blob `%s`。" % git_hash_object(
        pathlib.Path(__file__).relative_to(REPO).as_posix())[:12])
    a("- 检查器 `.claude/skills/mcm-model-select/check-model-select.py` blob `%s`（**本支不动它**）。" % chk_blob[:12])
    a("- brief blob `%s` · 题面 blob `%s`。" % (brief_blob[:12], prob_blob[:12]))
    a("- 四臂产物的逐件 blob 见 §0 的表（`git hash-object`，**当场跑**）。")
    a("- ★ **本文件不声称穷尽**：机器抽取只覆盖 `probe_product` 抽的那几列 + 检查器判的那几条判据。")
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace("\r\n", NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO).as_posix(), OUT_DOC.stat().st_size, "B")
    print("criteria %d: %s" % (len(CRIT), CRIT))
    for tag, _d in all_arms():
        r = probes[tag]["run"]
        print("  %-3s files=%d entry=%s rc=%s" % (
            tag, probes[tag]["n_files"], (r["entry"] if r else "（无）"), (r["rc"] if r else "—")))
    print("OK")


if __name__ == "__main__":
    sys.exit(main())
