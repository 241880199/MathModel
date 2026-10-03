#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3: generate `tests/skills/schematic/red-green-evidence.md` (RED x GREEN, machine-extracted).

Writes with `write_bytes` (repo discipline; also guarantees LF). Every reading in the document
comes from a command this script runs **on the spot**: the same `check-figure-style.py`
(**blob == HEAD**, see §0) over the frozen products, plus a fresh `pdflatex` compile of each
product's source. The comparison table is parsed **cell by cell** from the checker's stdout
(never hand-copied); the criteria list is taken **live** (a hard-coded list once silently
zeroed a summary -- the table arm's precedent).

Three things this arm must state honestly:
  (1) **RED is the independent variable**: `red/out-R{n}/figure.tex` and `caption.txt` are the
      writers' bytes, unchanged (per-file blob vs HEAD, see §0).
  (2) **RED's reds are named per criterion** with their **true nature** (real red / cascade /
      false red since fixed) -- see §4 (hand-written).
  (3) **The RED arm's honest boundary**: the neutral skeleton already guarantees "it compiles
      and has nodes and arrows", so this RED **cannot test** the "could not even produce a
      figure" class of failure. **It does not claim to cover every failure mode.**

Usage: python tests/skills/schematic/make-evidence.py
"""
import difflib
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/schematic
REPO = HERE.parents[2]                                   # repo root
CHECKER = REPO / "tests" / "skills" / "figure-choose" / "check-figure-style.py"
STYLE = REPO / ".claude" / "skills" / "mcm-schematic" / "assets" / "schematic-style.tex"
RED = HERE / "red"
GREEN = HERE / "green"
BRIEF = RED / "brief.md"
OUT_DOC = HERE / "red-green-evidence.md"
BUILD = REPO / "build" / "m3-schematic-t3-ev"            # gitignored, in-repo (as the fixtures do)
NL = chr(10)
BS = chr(92)

# Same ruler, same parameters on both sides.
TEXTWIDTH_IN = 6.75      # the paper text width (F1 denominator); == schematic-style.tex's 6.75in derivation
SCENES = (1, 2, 3)       # three isolated writers, ONE shared scenario (see red/README.md §3)

# The criteria list is taken live; this is only the *expected* RED red-set per product, used to
# assert stability (the table arm pinned its red-sets the same way). A change here = a real change.
RED_EXPECTED = {
    1: {"F1", "F3a", "F3b", "F3c", "F6", "A4"},
    2: {"F1", "F3a", "F3b", "F3c", "F6", "A4"},
    3: {"F1", "F3a", "F3b", "F3c", "F6"},
}

LINE_RE = re.compile(r"^(PASS|FAIL)\s+([A-Z]\d+[a-z]?)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)? *$")


def tp(s):
    """`@B@` -> backslash, so the hand-written blocks stay free of literal backslashes."""
    return s.replace("@B@", BS)


def run(cmd, cwd=None):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=cwd)
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + NL
    return out, r.returncode


def blob_of(relpath):
    return run(["git", "hash-object", relpath])[0].strip()


def head_blob(relpath):
    return run(["git", "rev-parse", "HEAD:" + relpath])[0].strip()


def check(pdf):
    """Run the shared checker on a product PDF (with `--schematic`); parse stdout cell by cell."""
    cmd = [sys.executable, CHECKER.relative_to(REPO).as_posix(),
           "--fig", pdf.relative_to(REPO).as_posix(),
           "--caption", "@" + (pdf.parent / "caption.txt").relative_to(REPO).as_posix(),
           "--textwidth-in", str(TEXTWIDTH_IN), "--schematic"]
    out, rc = run(cmd)
    cells, result = {}, None
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1) == "PASS", m.group(3).strip())
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
    return {"cmd": " ".join(cmd), "stdout": out.rstrip(NL), "rc": rc,
            "cells": cells, "result": result}


def criterion_key(cid):
    """Order F1,F2,F3a..F3d,F4,F5,F6,A1,A3,A4 -- derived from the live IDs, not hard-coded."""
    letter, rest = cid[0], cid[1:]
    num = int(re.match(r"\d+", rest).group(0))
    sub = rest[len(re.match(r"\d+", rest).group(0)):]
    return (letter, num, sub)


def criteria_ids(*sides):
    """Union of criteria IDs, taken live from the checker output (never hard-coded)."""
    ids = []
    for data in sides:
        for key in data:
            for k in data[key]["cells"]:
                if k not in ids:
                    ids.append(k)
    return sorted(ids, key=criterion_key)


def reds(data, key, crit):
    return sorted((k for k in crit if k in data[key]["cells"] and not data[key]["cells"][k][0]),
                  key=criterion_key)


def is_empty_green(data, k):
    """An `A1` PASS whose reading shows **0 node-boxes**: the criterion judged nothing here.

    `A1` collects only `fill`-and-`stroke` closed blocks, so a product whose nodes are drawn
    with `fill=none` yields an empty subject set. The checker reports this honestly (`节点框 0 个`)
    and still prints PASS; the *presentation* must not let that read as "the criterion passed".

    **Scope limit (honest)**: the detector is **hard-coded to `A1`** (the `k == "A1"` arm below),
    so it **cannot observe** an empty green for any other criterion. This function does *not*
    establish that empty greens occur **only** at `A1` -- it can only see this one. Do not read
    the generator's summary as "no other criterion ever judged nothing".
    """
    cell = data["cells"].get(k)
    return bool(cell) and cell[0] and k == "A1" and cell[1].startswith("节点框 0 个")


def empty_green_cells(rows, crit):
    return "、".join("%s×%s" % (t, k) for t, _, d in rows for k in crit
                     if is_empty_green(d, k)) or "（无）"


def compile_readings():
    """Fresh `pdflatex` compile of every product's source, in an ASCII cwd under build/.

    The PDFs are NOT byte-comparable (new CreationDate / ID); the point is the rc and the
    Overfull count. GREEN's source `@B@input`s `../schematic-style.tex`, so the style file is
    staged one level up (the skeleton's own relative layout).
    """
    if BUILD.exists():
        shutil.rmtree(BUILD)
    BUILD.mkdir(parents=True)
    shutil.copyfile(STYLE, BUILD / "schematic-style.tex")
    readings = {}
    for tag, srcdir in [("R1", RED / "out-R1"), ("R2", RED / "out-R2"),
                        ("R3", RED / "out-R3"), ("G1", GREEN / "out-G1")]:
        d = BUILD / f"out-{tag}"
        d.mkdir()
        shutil.copyfile(srcdir / "figure.tex", d / "figure.tex")
        out, rc = run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "figure.tex"], cwd=str(d))
        overfull = out.count("Overfull " + BS + "hbox")
        m = re.search(r"Output written on [^\s(]+ \((\d+) pages?, (\d+) bytes\)", out)
        readings[tag] = (rc, overfull, m.group(0) if m else "**no Output written line**")
    return readings


def structural_read(srcdir):
    """Machine-extracted structural facts about a product source (not a hand copy)."""
    t = (srcdir / "figure.tex").read_bytes().decode("utf-8")
    return {
        "lines": len(t.splitlines()),
        "nodes": t.count(BS + "node"),
        "draws": t.count(BS + "draw"),
        "edgemacro": t.count(BS + "mcmedge"),
        "has_input_style": ("schematic-style.tex" in t),
        "has_documentclass": (BS + "documentclass" in t),
        "packages": sorted(set(re.findall(re.escape(BS) + r"usepackage(?:\[[^\]]*\])?\{([^}]+)\}", t))),
    }


# ---------------------------------------------------------------- hand-written blocks (judgement layer)
NATURE = tp("""**这一节是判断层，机械判据判不了它。** 下面是本任务读完四份判词、并**亲眼看过四张图**
（`red/out-R{n}/figure.png` ×3 与 `green/out-G1/figure.png`）之后写下的。**本节手写，不是机器抽取。**

### 逐条点名（判据 · 读数 · 为什么 · 性质）

| 判据 | 谁红 | 读数（见 §2/§3） | 为什么红 | 性质 |
| :--- | :--- | :--- | :--- | :--- |
| `F1` 图宽比 | R1/R2/R3 | R1 `1.225`（A4 页盒）/ R2 `1.259` / R3 `1.259`（letter 页盒），分母 `6.75` | 三位写手都**没把页盒／图框钉到版心宽** —— 中性骨架用的是 `article` 默认页盒，而宽度纪律只存在于规范里（`@B@mcmscfigwidth`），写手看不到 | **真红**（三条独立，同一根因） |
| `F3a` 图注前缀 | R1/R2/R3 | `caption.txt` 不以 `Figure N:` 起：R1 以 `Schematic of...` 起、R3 不带前缀；★ **最有信息量的一例 = R2 以 `Figure 1.`（句点）起** —— 它**知道要写前缀、却用错了分隔符**（`N.` 而非 `N:`）⇒ 正好证明这条判据编码的是**猜不到**的约定（连"知道要写 `Figure N`"的写手也落红） | 图注形态（`Figure N:` 前缀）是规范 ∕ `house-style` 的产物契约，写手没被告知 | **真红** |
| `F3b` 图注词数 | R1/R2/R3 | `103` / `108` / `90` 词（硬上限 `17`） | 写手把整段工作流写进了图注（R1 的图注就是一段方法学散文） | **真红**（与 `F3a` 同一根因：图注惯例） |
| `F3c` 句末句号 | R1/R2/R3 | 三条 `caption.txt` **都以句号收尾** | 同上：图注**不押句号**这条是规范 ∕ `house-style` 的契约 | **真红**（同上根因） |
| `F6` 字体族 | R1/R2/R3 | 内嵌 `['CMR10','CMR7','CMR9']`（Computer Modern），不在可接受族里 | 中性骨架不载字体宏包 ⇒ 默认 CM；规范要求与论文正文同源（`newtxtext`） | **真红** |
| `A4` 线宽 | R1/R2 | R1/R2 越界线宽 `[0.399, 0.797]`（TikZ 默认 0.4pt 与 `thick`≈0.8pt） | 写手用 TikZ 默认线宽；允许集合是**本支样式层**的（`0.5/0.7/0.9pt` + `0.5/1.4mm`） | **真红** |
| `A4` 线宽 | R3 | **PASS**（越界 0 种） | R3 自己选了 `0.7pt` 统一线宽，**恰好命中**允许集合 ⇒ 同一判据**依写手而异** | **不是红**（R3 的偶然命中，如实记） |

**没有级联、没有假红。** 与表格那支不同，本支的 `A` 族**没有 fail-closed 红**：四份产物的
矢量层与文字层都在；`A3`/`A4` 拿到输入，而 **`A1` 在 R1/R2 上判到 `0` 个框**（**空绿**，见 §4）——
它在这两份上**什么都没判到**，不是"判过了"。**`GREEN` 的 `A1` 是真过**（G1 = `节点框 9 个`），
别把两者混为一谈。图层非空 ⇒ 不存在"一条红了带红一串"的级联；
检查器本任务**一字未改**（blob == `HEAD`，见 §0）⇒ 也**没有"判据假红已修"**这一类。
**不声称穷尽**：上表只列本支四份产物**实际触发**的判据，不声明覆盖率。

### 本支 RED 最诚实的读法（别把"红得多"当质量证明）

- **三份 RED 都编译成功**（`rc=0` · `Overfull @B@hbox=0`，见 §8），**都画出了正确的拓扑**
  （竖排七步 · 一条修订回环 · 三路投影扇出再汇合）—— 图**读得清**（见 §7）。
- 判据抓的是**没被告知的约定**：**图宽怎么钉**（`F1`）、**图注怎么写**（`F3a/b/c`）、
  **字体跟谁同源**（`F6`）、**线宽取哪一档**（`A4`）。这些**都不是"图烂"**，而是
  **"没看规范就不会知道"**。
- ★ **反向也要照实**：`F3a`/`F3b`/`F3c` 三条红**共享同一个根因**（图注惯例），读的时候
  别当成"三个独立的图缺陷"；`A4` 在 R3 身上**根本没红** ⇒ 这一条有**写手侧的偶然性**。
- ★ **RED 的诚实边界**（设计 §9.3 / 硬要求 7）：中性骨架**已经保证**"能编译、有节点有箭头"
  ⇒ 这轮 RED **测不到"连图都出不来"那一类失败**（写不出 TikZ、编不过、没有节点/箭头）。
  **不声称覆盖全部失败模式。**""")

LOOK = tp("""**这一节是「看一眼」层（GC11 / 设计 §5.4），机器判不了它。** 四张图**都编译、都渲成 150dpi PNG、
都由本 agent 亲眼看过**；下面是**从这张图读到了什么**。★ 先例：origin 那支的粉边与图例压数据、
表格那支的超长表题，**判据一条都不报** —— 本节就是找那种东西。

本支必看的五点：① 箭头有没有压住字；② 主流程与回环/反馈**一眼分得开**吗；③ 图例在不在；
④ 标注有没有落到画外；⑤ 节点内文字有没有溢出。

### GREEN（`green/out-G1/figure.png`，962×615 @150dpi）

- **读到**：一条横向主流程 `Data collection → Preprocessing → Calibration → fit ok?`（菱形判定），
  一条**虚线**从菱形顶部标着 `No` 绕回 `Calibration` 顶部；`Yes` 向下扇出到三个并列方框
  （`No intervention` / `Vaccination campaign` / `School closure`），三路再汇入 `Comparison` → `Recommendation`。
- ① 箭头不压字；② **虚线反馈 vs 实线主流程一眼可分**；③ 无图例（只有两种线义，虚线那条已用 `No` 标注
  ⇒ 不需要图例）；④ 标注都在框内；⑤ 文字不溢出节点。
- **判据不报、眼睛看得见**：`Yes` 标签落在菱形右侧，而三条出边都从菱形**底部**离开 ⇒ `Yes`
  离其中两条边略远；三条扇出边在菱形附近**有短距离重叠**（扇出常态，非缺陷）。

### RED（`red/out-R{n}/figure.png`）

- **R1**（`red/out-R1/figure.png`，1241×1754 @150dpi ≈ A4）：读到竖排七步 · 菱形 `Fit check` ·
  一条**实线**回环（在左侧，标 `No: revise model or priors (repeat)`）绕回 `Calibration` ·
  三路扇出再汇合 · 图下一整段 103 词图注。① 不压字；② ★ **回环是实线、与主流程同款**
  ⇒ **主/环靠线型分不开**，只能读标签；③ 无图例；④ 标注在框内；⑤ 文字不溢出。
- **R2**（`red/out-R2/figure.png`）：同上竖排，回环从菱形**东侧**绕上去接 `Calibration` **东侧**，
  同样是**实线**。② ★ **主/环同样靠线型分不开**；其余四点同上。
- **R3**（`red/out-R3/figure.png`）：竖排；`not acceptable` 一路向右进 `Revise model structure or priors` 框，
  再以**虚线**标 `revise & refit` 回到 `Calibration` 东侧 —— ② ★ **这一份把回环画成了虚线，主/环一眼可分**
  （与 R1/R2 恰成对照）。① ★ **`not acceptable` 这条边标签紧贴（接近贴住）`Revise model...` 框的左边框**
  —— 属"标注与框挤在一起"，**判据一条都不报**（`A1` 管的是框与框，不管标签与框）；③④⑤ 同上。

### 一句话（本层最诚实的读法）

**机械层报的是"没按约定的那几条"（宽度 / 图注 / 字体 / 线宽），看图层报的是"读起来顺不顺"
（R1/R2 的回环与主流程同款线型、R3 的一条边标签挤框）—— 两者交集为空。** 本支**没有任何一条看图发现**能被
现有判据看见：`A2`（箭头端点）已降级、也没有"图例 / 线型语义 / 标签拥挤"的判据。**不声称本节穷尽。**""")

DIFF_ANNOT = tp("""**人工读一遍：差异是不是"规范导致"的？**

- **可归因于规范（结构性的）**：
  1. **`@B@input{../schematic-style.tex}`**：G1 有一行 `@B@input` 样式层；三份 RED **一行都没有**
     （它们是自包含 `article` 文档，样式散落在自己文件里）—— 这是本 skill 的**样式单源**契约，直接对应
     `F6`（字体族，由样式层载 `newtxtext`）与 `A4`（线宽，由样式层的长度变量给出）。
  2. **页盒**：G1 用 `geometry` 的 `paperwidth=@B@mcmscfigwidth` 把页盒钉成`@B@mcmscfigwidth`；三份 RED
     都是 `article` 默认页盒 ⇒ 直接对应 `F1`。
- **不是规范要求、属设计 / 写手判断的**：
  1. **朝向不同**：G1 是**横向**主流程；三份 RED 都是**竖向**主流程（R1/R2/R3 各自的选择）。
  2. **图注措辞与长度**：G1 图注 8 词；RED 三份是 90–108 词的段落 —— 差异**双向**（既有 `F3` 的形态差，
     也有"写多写少"的判断差）。
  3. **回环线型**：R3 自己就把回环画成虚线（与 G1 同向）；R1/R2 画成实线。**这条差异一半是规范
     （`S2` 要求虚线编码回环／反馈）、一半是写手自己的好坏判断** —— 不能全记在规范头上。
- **结论**：两侧差异**集中在**（a）样式单源与页盒钉宽（规范契约）、（b）朝向 / 图注长度 / 回环线型
  （设计选择）。**不是**"某些节点画错"——**四份图的拓扑按工作流图层级而言一致**（同一场景的七步 + 回环 + 三路分支）。
  ★ **本句原写"四份图的拓扑完全一致"，过宽**：**不声称图元逐字同构** —— **R3 把"修订"画成了一个显式 `@B@node`**
  （`tests/skills/schematic/red/out-R3/figure.tex:39` 的 `@B@node[proc] (rev) {Revise model structure or priors}`），
  而 R1/R2 没有把同一语义画成**工作流节点**（R1 只在回环旁放一个**标签** `@B@node[lbl]`（`:49`）、R2 把它作**边标签**（`:62`））
  ⇒ 结构表自印 `@B@node` 计数 **R1=11 / R2=10 / R3=11**（见上）。**按工作流图层级**读，四份是同构的。""")

GENERATOR = tp("""## §8 生成器 · 判据非空泛 · 编译读数 · 不动点

- 本文件的机器部分由 `tests/skills/schematic/make-evidence.py` **当场跑** `check-figure-style.py`
  生成（`write_bytes` · 全 LF）；对照表**现取**判据清单、逐格解析 stdout（§4）。
- **编译读数**（本节末的块）：`make-evidence.py` 把四份产物源码 stage 到仓内 `build/`（gitignored，
  在 D 盘）后**当场重编**，读数 = `rc` · `Overfull @B@hbox` 计数 · `Output written` 行。
  ★ **PDF 非字节可比**（每次重编带新 `CreationDate`/`ID`）—— 判据基于几何 / 文本读数，不拿字节比。
- ★ **判据非空泛（失败方向的另一条臂）** —— `mutate-figure-style.py` 的读数**逐字取自快照**（**本生成器不执行该驱动器**，故**不声称「当场跑过」**；复跑命令见本节末的 `$ python …` 块），摘其合计段：
  ```text
  MUT: 6/6 达预期（检查器的 `A` 族 M59–M64：4 条必须红 + 2 条**射程边界对照**（`A1` 容差 / `A3` 容差）必须绿）
  MUT: 64/64 达预期（合计）
  ```
  ⇒ 其中 `A` 族 **4 条真红变异 + 2 条必须绿对照**；`F1`–`F6` 的真红变异与其它臂见该驱动器的完整输出。
  ★ **`A4` 的真红变异**证明"线宽不在允许集合里 ⇒ `A4` 真的会红"，所以 §4 里 R1/R2 的 `A4` 红**不是"尺子恒绿/恒红"**。
- **不动点**：在已提交的树上重跑本生成器 ⇒ 本文件**逐字节不变**（证法：跑后 `git status --short` 仍为空；
  见本任务报告）。""")

MUTATION_SNAPSHOT = """$ python tests/skills/figure-choose/mutate-figure-style.py
MUT: 6/6 达预期（检查器的 `A` 族 M59–M64：4 条必须红 + 2 条**射程边界对照**（`A1` 容差 / `A3` 容差）必须绿）
MUT: 64/64 达预期（合计）
"""


def main():
    red = {n: check(RED / f"out-R{n}" / "figure.pdf") for n in SCENES}
    green = {1: check(GREEN / "out-G1" / "figure.pdf")}
    CRIT = criteria_ids(red, green)
    assert {"A1", "A3", "A4"} <= set(CRIT), f"A-family missing (--schematic dropped?): {CRIT}"
    for n in SCENES:
        assert set(red[n]["cells"]) == set(CRIT), (n, sorted(red[n]["cells"]))
    assert set(green[1]["cells"]) == set(CRIT), sorted(green[1]["cells"])

    readings = compile_readings()

    rel = CHECKER.relative_to(REPO).as_posix()
    wt_blob, hd_blob = blob_of(rel), head_blob(rel)
    frozen = {}
    for tag, d in [(f"R{n}", RED / f"out-R{n}") for n in SCENES] + [("G1", GREEN / "out-G1")]:
        for f in ("figure.tex", "caption.txt"):
            r = (d / f).relative_to(REPO).as_posix()
            frozen[r] = (blob_of(r), head_blob(r))
    brief_bytes = BRIEF.read_bytes().decode("utf-8")

    L = []
    a = L.append
    a("# Task 3 · RED × GREEN 对照证据（`mcm-schematic`）")
    a("")
    a("本文件由 `tests/skills/schematic/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。"
      "**§1 / §2 / §3 / §4 / §6 的机器部分逐格解析自 stdout，不手抄**；**§5 的性质判定与 §7 的看图记录是手写**"
      "（文里已标明）。")
    a("")
    a("## §0 口径（同场景 · 同一把尺 · RED 是自变量）")
    a("")
    a("- **场景**：`tests/skills/schematic/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联）。"
      "★ 本支与另三支载体的**一处设计差异**（依据 Task 3 任务书与设计 §5.3「三个隔离写手各拿**同一份**场景描述」）："
      "**同一场景 × 3 位隔离写手**（看写手间离散度），**不是** 3 场景 × 1 位。")
    a("- **两侧**：RED = 3 位**干净上下文**写手（**未用 `fork`**）的图；GREEN = **用本 skill** 出的同场景图（1 份）。")
    a("- **同一把尺**：`%s` —— 两侧用的是**同一版**（工作树 blob == `HEAD:` blob，见下）；"
      "**判据逻辑一字未改**。两侧**同一组参数**：`--schematic` ＋ `--textwidth-in %s`。"
      % (rel, TEXTWIDTH_IN))
    a("- **判据清单现取**：本支 **%d 条**（`%s`）。**不写死条数**（先例：plot-python 把清单写死成 6 条而实得 9 条 ⇒ 汇总表静默归零）。"
      % (len(CRIT), "、".join(CRIT)))
    a("- **RED 侧冻结自证**（`git hash-object` vs `HEAD:`）—— **RED 是本任务的自变量**，本轮**未改**：")
    a("")
    a("| 文件 | 工作树 blob | `HEAD:` blob | 相同？ |")
    a("| :-- | :-- | :-- | :-- |")
    for r, (w, h) in frozen.items():
        a("| `%s` | `%s` | `%s` | %s |" % (r, w[:12], h[:12], "是" if w == h else "**否**"))
    a("")
    a("- **检查器自证**：工作树 blob `%s` · `HEAD:` blob `%s` ⇒ %s"
      % (wt_blob[:12], hd_blob[:12], "**相同**" if wt_blob == hd_blob else "**不同（！）**"))
    a("")
    a("- ★ **RED 的诚实边界（硬要求 7 / 设计 §9.3）**：中性骨架 `neutral-skeleton.tex` **本身已保证**"
      "「能编译、有节点有箭头」⇒ 这轮 RED **测不到「连图都出不来」那一类失败**。"
      "**不声称覆盖全部失败模式。**")
    a("- ★ **环境旁路如实披露**：写手是本机 Claude Code 的 agent，会话级共享上下文里另有两处删不掉的可见面 ——"
      "① 可用 skill 列表里 `mcm-schematic` 那一行的**类别名**；② 项目记忆 `MEMORY.md`。"
      "**它们泄的是「有这几类要求」，不是「判据的边界在哪」**（阈值、线宽集合、图注形态、`A` 族 ID 与口径都看不到）。"
      "详见 `red/writer-self-reports.md`。")
    a("")
    a("## §1 场景（逐字内联；RED 与 GREEN 同一份）")
    a("")
    a("```text")
    a(brief_bytes.rstrip(NL))
    a("```")
    a("")

    for si, (name, data, tag) in enumerate((("RED", red, "R"), ("GREEN", green, "G")), start=1):
        a("## §%d %s 原始读数（%s）" % (si + 1, name,
          "三位干净上下文写手 · 中性骨架 · 无规范" if name == "RED" else "本 skill 产物"))
        a("")
        keys = SCENES if name == "RED" else (1,)
        for n in keys:
            d = data[n]
            capf = (RED if name == "RED" else GREEN) / ("out-%s%d" % (tag, n)) / "caption.txt"
            a("### %s%d" % (tag, n))
            a("")
            a("图注（`%s`，逐字字节读入）：" % capf.relative_to(REPO).as_posix())
            a("```text")
            a(capf.read_bytes().decode("utf-8").rstrip(NL))
            a("```")
            a("")
            a("```")
            a("$ " + d["cmd"])
            a(d["stdout"])
            a("[exit=%d]" % d["rc"])
            a("```")
            a("")

    a("## §4 对照表（机器抽取）")
    a("")
    a("每个格子 = 状态：绿 = `PASS` / 红 = `FAIL`。判定词逐格解析自 §2/§3 的 stdout；判据 ID 见表头（**现取**）。")
    a("")
    a("| 产品 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    rows = [(f"R{n}", "RED", red[n]) for n in SCENES] + [("G1", "GREEN", green[1])]
    for tag, side, data in rows:
        c = data["cells"]
        row = [tag, side]
        for k in CRIT:
            cell = c.get(k)
            if cell is None:
                row.append("—")
            elif not cell[0]:
                row.append("红")
            else:
                row.append("绿†" if is_empty_green(data, k) else "绿")
        row.append("PASS" if data["result"][0] else "FAIL")
        a("| " + " | ".join(row) + " |")
    a("")
    a("★ **`†` = 空绿格**（本表出现的：`%s`）：判词为 `节点框 0 个` ⇒ 判据**在这份上没有判到任何对象**"
      "（`A1` 的节点框集合只收既填充又描边的闭合块，对 `fill=none` 的节点**视而不见**）"
      "⇒ 该格**不构成「判据在这份上过了」的证据**。`A1` 的已知边界见 "
      "`.claude/skills/mcm-schematic/references/schematic-style.md` §3 第 1 条（残余那一句）。"
      "★ **`GREEN` 的 `A1` 不是空绿**（G1 = `节点框 9 个`），别与 R1/R2 混为一谈。"
      % empty_green_cells(rows, CRIT))
    a("")
    a("### §4.1 逐判据判词（机器抽取；判词原文，不手抄）")
    a("")
    a("| 产品 | 侧 | 判据 | 状态 | 判词 |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for tag, side, data in rows:
        for k in CRIT:
            cell = data["cells"].get(k)
            if not cell:
                continue
            a("| %s | %s | %s | %s | %s |" % (tag, side, k, "PASS" if cell[0] else "FAIL", cell[1]))
    a("")
    a("### §4.2 汇总（由 §4 的格子逐格重算）")
    a("")
    a("| 侧 | 红格数（判据 × 产物） | 判红的判据 ID（并集） | 全绿产物数 | 空绿格数（判到 0 个对象） |")
    a("| :-- | :-- | :-- | :-- | :-- |")
    for side, minset in (("RED", red), ("GREEN", green)):
        allreds, ok, total, empt = [], 0, 0, 0
        for n, data in minset.items():
            total += 1
            c = data["cells"]
            if set(c) == set(CRIT) and all(v[0] for v in c.values()) and data["result"][0]:
                ok += 1
            allreds += reds(minset, n, CRIT)
            empt += sum(1 for k in CRIT if is_empty_green(data, k))
        a("| %s | %d | %s | %d/%d | %d |" % (side, len(allreds),
                                              "、".join(sorted(set(allreds), key=criterion_key)) or "（无）",
                                              ok, total, empt))
    a("")
    a("★ **空绿格（`†`）不计入「绿」**：`A1` 在 R1/R2 上判到 `0` 个节点框 ⇒ 判据**没有判到对象**"
      "（见 §4 表注与 `schematic-style.md` §3 第 1 条）；`GREEN` 的 `A1` 是**真过**（G1 `节点框 9 个`）。"
      "**红格数与全绿产物数不受空绿影响** —— 本器**只**把 `A1` 的「节点框 0 个」识别为空绿"
      "（`is_empty_green` 硬编码 `k == \"A1\"`）；**其余判据若判到 0 个对象，本器看不见**"
      "（**不声称它们不是空绿**）—— 而 R1/R2 本就因他判据判红，故那几格不影响红格数。")
    a("")
    a("## §5 RED 的红逐条点名（硬要求 1：真红 / 级联 / 假红已修）")
    a("")
    a("（红集**机器抽取**自 §2；性质判定是人工判定，逐条写。**本支无级联、无假红** —— 理由见下表与末段。）")
    a("")
    for n in SCENES:
        a("- **R%d 红集** = `{%s}`" % (n, ", ".join(reds(red, n, CRIT))))
    a("")
    a(NATURE)
    a("")
    a("## §6 两侧 `.tex` 并排逐字 diff（机器抽取 + 人工注释）")
    a("")
    a("**结构读数（机器抽取）**：")
    a("")
    a(tp("| 产品 | 行数 | `@B@node` | `@B@draw` | `@B@mcmedge` | 有 `@B@input` 样式层 | 有 `@B@documentclass` | `@B@usepackage` |"))
    a("| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |")
    struct = {}
    for tag, d in [(f"R{n}", RED / f"out-R{n}") for n in SCENES] + [("G1", GREEN / "out-G1")]:
        struct[tag] = structural_read(d)
        s = struct[tag]
        a("| %s | %d | %d | %d | %d | %s | %s | %s |" % (
            tag, s["lines"], s["nodes"], s["draws"], s["edgemacro"],
            "是" if s["has_input_style"] else "否", "是" if s["has_documentclass"] else "否",
            ", ".join(s["packages"]) or "（无）"))
    a("")
    for n in SCENES:
        rp = RED / f"out-R{n}" / "figure.tex"
        gp = GREEN / "out-G1" / "figure.tex"
        rl = rp.read_bytes().decode("utf-8").splitlines()
        gl = gp.read_bytes().decode("utf-8").splitlines()
        diff = list(difflib.unified_diff(rl, gl,
                                         fromfile="red/out-R%d/figure.tex" % n,
                                         tofile="green/out-G1/figure.tex", lineterm=""))
        a("### 场景（唯一）：R%d vs G1（`difflib.unified_diff`，逐字）" % n)
        a("")
        a("```diff")
        a(NL.join(diff) if diff else "（两侧逐字相同）")
        a("```")
        a("")
    a(DIFF_ANNOT)
    a("")
    a("## §7 看图记录（硬要求 4：亲眼看图）")
    a("")
    a(LOOK)
    a("")
    a(GENERATOR)
    a("")
    a("```text")
    a(tp("$ python tests/skills/schematic/make-evidence.py   # 编译读数（rc · Overfull @B@hbox · Output written）"))
    for tag in ("R1", "R2", "R3", "G1"):
        rc, of, ow = readings[tag]
        a("%s  rc=%d · Overfull %shbox=%d · %s" % (tag, rc, BS, of, ow))
    a("```")
    a("")
    a("★ 下面是 **`mutate-figure-style.py` 的快照**（**非生成时现跑**）：首行是**复跑命令**，其余是**该命令的合计段读数**（逐字取自快照）。")
    a("")
    a("```text")
    a(MUTATION_SNAPSHOT.rstrip(NL))
    a("```")
    a("")

    doc = (NL.join(L).rstrip(NL) + NL).replace("\r\n", NL)
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO).as_posix(), OUT_DOC.stat().st_size, "B")

    # ---- self-证 assertions (non-zero exit if violated) ----
    assert wt_blob == hd_blob, "checker blob != HEAD!"
    for r, (w, h) in frozen.items():
        assert w == h, "frozen product changed: %s" % r
    for n in SCENES:
        assert red[n]["result"] is not None, "RED %d: no RESULT parsed" % n
        assert set(reds(red, n, CRIT)) == RED_EXPECTED[n], \
            "R%d red-set changed: %s" % (n, reds(red, n, CRIT))
    assert green[1]["result"] is not None, "GREEN: no RESULT parsed"
    assert all(v[0] for v in green[1]["cells"].values()) and green[1]["result"][0], \
        "GREEN not all-green: %s" % reds(green, 1, CRIT)
    assert all(rc == 0 and of == 0 for rc, of, _ in readings.values()), readings
    print("criteria %d: %s" % (len(CRIT), CRIT))
    for n in SCENES:
        print("  RED  R%d red: %s" % (n, reds(red, n, CRIT) or "(none)"))
    print("  GREEN G1 red: %s" % (reds(green, 1, CRIT) or "(none)"))
    print("OK")


if __name__ == "__main__":
    main()
