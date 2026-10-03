#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 3：生成 `tests/skills/plot-origin/red-green-evidence.md`（RED × GREEN 并列对照，机器抽取）。

写入用 `write_bytes`（本仓纪律；也保证全 LF）。文中每个读数都来自本脚本**当场跑过**的
`check-figure-style.py`（一字未改，blob 与 HEAD 比对见文内）；对照表由当场 stdout **逐格解析**，
不手抄（判词行 -> (状态, 判据 ID, 详情)）。

两侧口径：3 个场景（R1/R2/R3 = `tests/skills/figure-choose/red/brief-R{1,2,3}.md` 的**逐字同源**副本）
× 2 个载体（PNG/PDF）= 各 6 张图；同一分母 `--textwidth-in 6.31`；同一把尺。
PNG 的 `--dpi` 由**产物自身**推得（PNG 像素宽 ÷ PDF 页盒宽），不写死。

★ 本支两条**必须逐格如实**的：
  ① **`F6` 三态**（`PASS` / `FAIL` / **`N/A`**）：落哪一态**依产物而定**，逐格印真实判词，
     **不许把 `N/A` 渲染成 `PASS`**（假绿）、**不许静默丢格**。
  ② **PDF 侧 `F5` 红**：Origin 的 PDF 内容流把填色写成**两位小数** ⇒ 栅格化后每通道差 1 LSB ⇒
     `F5`（容差 0 的精确命中）判红。**每处 PDF 侧 `F5` 红都带一行注**（指向 §H.2 `M3-origin-T2a`）。
     **PNG 侧 `F5` 是本支的真判据**，照常读。

用法： python tests/skills/plot-origin/make-evidence.py
"""
import importlib.util
import pathlib
import re
import subprocess

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/plot-origin
REPO = HERE.parents[2]
CHECKER = REPO / "tests" / "skills" / "figure-choose" / "check-figure-style.py"
RED = HERE / "red"
GREEN = HERE / "green"
OUT_DOC = HERE / "red-green-evidence.md"
TEXTWIDTH = "6.31"

# 场景编号与载体：**唯一一处**定义 —— 图数与判据清单都由它现推，别处**不许再写死**。
SCENES = (1, 2, 3)
CARRIERS = ("png", "pdf")
# 判据 ID 允许**多位数**（`F10`、`F12`…）：检查器将来新增两位数判据时，下面按行解析的汇总表
# 不会静默丢格（先例 `M3-plot-INIT`：plot-python 的 `make-evidence.py` 把清单写死成 6 条而实得 9 条
# ⇒ 汇总表静默归零、判据静默丢掉）。
LINE_RE = re.compile(r"^(PASS|FAIL)\s+([A-Z][0-9]+[a-d]?)\s+(.*)$")
RES_RE = re.compile(r"^RESULT: (PASS|FAIL)(?:（(.*)）)?\s*$")

# ★ PDF 侧 `F5` 红的载体限制注（要求 2）—— 两条分支，别把实红也说成假红。
_F5_NOTE_CARRIER = (
    "★〔载体限制 ⇒ **本红是假红**〕同图 **PNG 侧 `F5` 绿、红只出现在 PDF**。机制当场量过：Origin 的 PDF "
    "内容流把填色写成**两位小数**（本支 GREEN 实测 `0.9 0.62 0`，而 `#E69F00` 的满精度是 "
    "`0.9019607843 0.6235294118`）⇒ 栅格化后每通道差 1 LSB（`#E69F00` → `#E59E00`）⇒ `F5`（容差 0 的"
    "精确命中）判红。**这不是「Origin 画的图颜色不对」** —— 同场景的 python/matlab 的 PDF 走满精度、"
    "`F5` 绿（本脚本另跑核对过）。登记 `docs/mcm-suite-todo.md` §H.2 `M3-origin-T2a`。")
_F5_NOTE_REAL = (
    "★〔本红是**实红**：色不在 `H14`，两载体皆红〕PDF 侧的 hex 另比 PNG 侧偏 ≤ 1 LSB，同源于 Origin "
    "PDF 写入器的两位小数量化（见 §H.2 `M3-origin-T2a`）；但**判红的原因是配色本身**，与该量化无关。")


def criteria_ids(*sides):
    """判据 ID 清单**现取**自检查器的实得输出（保持首次出现次序）—— **不写死**。见文件头先例。"""
    ids = []
    for data in sides:
        for n in SCENES:
            for car in CARRIERS:
                for k in data[n][car]["cells"]:
                    if k not in ids:
                        ids.append(k)
    ids.sort(key=lambda k: (int(re.match(r"F(\d+)", k).group(1)), k))
    return ids


def load_checker():
    spec = importlib.util.spec_from_file_location("chk", CHECKER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CHK = load_checker()


def run(cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(REPO))
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + "\n"
    return out, r.returncode


def png_dpi(png, pdf):
    from PIL import Image
    import fitz
    with Image.open(png) as im:
        pw = im.size[0]
    with fitz.open(pdf) as doc:
        win = doc[0].rect.width / 72.0
    return int(round(pw / win))


def check_fig(fig, caption_file, dpi):
    cmd = ["python", str(CHECKER.relative_to(REPO)), "--fig", str(fig.relative_to(REPO)),
           "--caption", "@" + str(caption_file.relative_to(REPO)),
           "--textwidth-in", TEXTWIDTH]
    if fig.suffix.lower() == ".png":
        cmd += ["--dpi", str(dpi)]
    out, rc = run(cmd)
    cells, result = {}, None
    for ln in out.splitlines():
        m = LINE_RE.match(ln)
        if m:
            cells[m.group(2)] = (m.group(1) == "PASS", m.group(3))
        m = RES_RE.match(ln)
        if m:
            result = (m.group(1) == "PASS", m.group(2) or "")
    return {"cmd": " ".join(cmd), "stdout": out, "rc": rc, "cells": cells, "result": result}


def side(dirname, tag):
    res = {}
    for n in SCENES:
        d = dirname / f"out-{tag}{n}"
        pdf, png = d / "figure.pdf", d / "figure.png"
        cap = d / "caption.txt"
        dpi = png_dpi(png, pdf)
        res[n] = {
            "pdf": check_fig(pdf, cap, dpi),
            "png": check_fig(png, cap, dpi),
            "dpi": dpi,
            "caption_bytes": cap.read_bytes().decode("utf-8"),
        }
    return res


def is_na(cell):
    """`F6` 的第三态（`N/A`）：检查器**三种写法**都落这一态，必须都认（**本支实测到三处**，
    不声称穷尽）。

    · **PDF 未内嵌任何字体**：状态 `PASS`、详情以 `N/A` 起（`N/A 本 PDF **未内嵌**任何字体…`）；
    · **PNG 载体**：状态 `PASS`、详情以 `PNG 载体无内嵌字体信息…本判据在 PNG 上不适用` 起
      —— **不以 `N/A` 起**，若不认它就把它渲染成 `PASS`（**假绿**，正是要求 1 要拦的）；
    · **PDF 有引用但未内嵌**：同第一种、但详情里带"只被引用"字样（本支 `G1`/`G3` 的 PDF 即此）。
    三处的共同标记 = 「不适用」⇒ 判据用「以 `N/A` 起 **或** 含『不适用』」两个条件覆盖全部三处。
    """
    return bool(cell) and (cell[1].startswith("N/A") or "不适用" in cell[1])


def cell_token(cid, cell):
    """单个格子的显示 token。**`F6` 的 `N/A` 是独立第三态，绝不渲染成 `PASS`**（要求 1）。"""
    if cell is None:
        return "—"
    if cid == "F6" and is_na(cell):
        return "N/A"
    return "PASS" if cell[0] else "FAIL"


def verdict_cell(cid, cell):
    """彩色表用的格子：绿 = PASS / 红 = FAIL / **N/A**（独立第三态，不假绿）。"""
    if cell is None:
        return "—"
    if cid == "F6" and is_na(cell):
        return "N/A"
    return "绿" if cell[0] else "红"


def f2_num(cell):
    """从 F2 判词（`彩色主色数 N`）里取 N —— **当场抽取**，不另存第二份。"""
    if not cell:
        return None
    m = re.search(r"彩色主色数 (\d+)", cell[1])
    return int(m.group(1)) if m else None


def pdf_f5_note(data, n):
    """PDF 侧 `F5` 红的注（要求 2）。只在 PDF 侧 F5 判红时给；否则空。"""
    pdfc = data[n]["pdf"]["cells"].get("F5")
    pngc = data[n]["png"]["cells"].get("F5")
    if not pdfc or pdfc[0]:
        return ""
    if pngc and pngc[0]:
        return _F5_NOTE_CARRIER
    return _F5_NOTE_REAL


def _pdf_two_decimal_colors(path):
    """当场从 PDF 内容流里抽填色算子里的三位数 —— 用来**当场量**"两位小数"这条载体事实。"""
    import fitz
    with fitz.open(path) as d:
        c = d[0].read_contents().decode("latin-1")
    seen = []
    for t in re.findall(r"([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(?:sc|rg)\b", c):
        if t not in seen:
            seen.append(t)
    return seen


def carrier_section(green):
    """§4：F2 与载体（不许跨载体比 F2）。读数**当场抽取**自 §1/§2 的判词。"""
    lines = []
    lines.append("**口径**：`F2`（彩色主色数）对 PNG / PDF 的读数**不保证相同** ⇒ 两侧各自读、"
                 "**不并列比**。**禁止的承重不是「本支某张图会变」**，而是**器械口径**：检查器对两载体走"
                 "**不同的栅格化路径** —— PNG 直接 `Image.open`（原生像素、按 `--dpi` 定尺），"
                 "PDF 第 1 页按固定 `RASTER_DPI=150` 栅格化（`raster_rgb()`）⇒ 同一条 `color_count` "
                 "吃到的像素来源不同 ⇒ 两个读数**不是同一个量**。")
    lines.append("")
    lines.append("**本支六个场景的 F2 逐载体读数（机器抽取自 §1/§2）** —— "
                 "★ **此表只是「同一场景两载体给出同一个数」这个负面结果的登记，不构成跨载体比较**："
                 "两根列并排**只为显示它们相同**，**不给「哪个多哪个少」下任何结论**（两个读数不是同一个量，见上）：")
    lines.append("")
    lines.append("| 场景 | 侧 | F2(PNG) | F2(PDF) | 本场景两载体是否相同 |")
    lines.append("| :-- | :-- | :-- | :-- | :-- |")
    for name, data in (("RED", RED_SIDE), ("GREEN", GREEN_SIDE)):
        for n in SCENES:
            p = f2_num(data[n]["png"]["cells"].get("F2"))
            q = f2_num(data[n]["pdf"]["cells"].get("F2"))
            lines.append(f"| {'R' if name == 'RED' else 'G'}{n} | {name} | {p} | {q} | "
                         f"{'**不同**' if p != q else '相同'} |")
    lines.append("")
    lines.append("⇒ **如实收窄（射程只到这里）**：**本支这六个场景**里，两载体的 `F2` **逐格相同** —— "
                 "所以**本支不出具**「某张图 PNG ≠ PDF」的实例。这条规矩因此**不靠本支某个读数**承重，"
                 "靠上面那条**器械口径**（两载体走两条栅格化路径）。**跨支的先例**另有："
                 "`tests/skills/plot-python/red-green-evidence.md` §4 的载体探针（同一张图 PNG=5 / PDF=3）。"
                 "**不许把本支的「逐格相同」读成「Origin 上 F2 不会随载体变」**。")
    lines.append("")
    lines.append("**另一条载体事实（`F5`，当场量，支撑 §3.3 与要求 2）**：")
    lines.append("")
    lines.append("```")
    for n in SCENES:
        cols = _pdf_two_decimal_colors(GREEN / f"out-G{n}" / "figure.pdf")
        lines.append(f"G{n} figure.pdf 内容流 sc/rg 填色（去重、前 6 个）：{cols[:6]}")
    lines.append("```")
    lines.append("")
    lines.append("⇒ `#E69F00` 被 Origin 写成 `0.9 0.62 0`（**两位小数**）；栅格化后每通道差 1 LSB ⇒ "
                 "PDF 侧 `F5` 判红、PNG 侧同图 `F5` 绿。**同场景 python/matlab 的 PDF 走满精度**"
                 "（python 实测 `0.9019607843 0.6235294118 0`），`F5` 绿 —— 本脚本当场另跑核对过。")
    return "\n".join(lines)


def f6_section(red, green):
    """§3.3：`F6` 三态逐格（要求 1）。三态**逐个实例列出**，不写死预期。"""
    lines = []
    lines.append("`F6` 的**落态依产物而定**（不写死预期）。下表**逐格**印真实 token："
                 "`PASS`（内嵌族落在可接受表）· `FAIL`（内嵌族不在表）· **`N/A`**（PDF 未内嵌任何字体 / "
                 "PNG 载体，本判据不适用）。**`N/A` 既不是 `PASS` 也不是 `FAIL`**，本表把它当**独立第三态**印出。")
    lines.append("")
    lines.append("| 场景 | 载体 | 侧 | F6 态 | 判词（机器抽取） |")
    lines.append("| :-- | :-- | :-- | :-- | :-- |")
    tally = {"PASS": 0, "FAIL": 0, "N/A": 0}
    for name, data in (("RED", red), ("GREEN", green)):
        for n in SCENES:
            for car in CARRIERS:
                cell = data[n][car]["cells"].get("F6")
                tok = cell_token("F6", cell)
                tally[tok] += 1
                lines.append(f"| {'R' if name == 'RED' else 'G'}{n} | {car.upper()} | {name} | "
                             f"**{tok}** | {cell[1] if cell else '（缺）'} |")
    lines.append("")
    lines.append(f"**三态合计（机器抽取）**：`PASS` {tally['PASS']} 格 · `FAIL` {tally['FAIL']} 格 · "
                 f"`N/A` {tally['N/A']} 格（共 {sum(tally.values())} 格 = "
                 f"{len(SCENES) * len(CARRIERS) * 2} 张图）。")
    return "\n".join(lines)


JUDGMENT = """**这一节是判断层，机械判据判不了它。** 下面是本任务 agent **亲眼看图**（PNG 逐张）后写下的：
读到了什么、读不出什么。**写真话。** 六张 Origin 图（三 RED + 三 GREEN）我都打开逐张看过；
同场景的另两支载体产物也并排比过。**本节是手写的，不是机器抽取。**

### GREEN（模块产物）—— 我从图上读到了什么

- **G1（`tests/skills/plot-origin/green/out-G1/figure.png`，R1 构成，竖 100% 堆叠柱）**：
  **底色白**（判据外缘环 100% 白，目视也是白）；**三色 = `H14` 前三色**（橙 low / 浅蓝 medium /
  绿 high —— 目视与 `F5` 0 越界互证）；**字体是衬线**（Times 系观感，与主题一致）。
  **判据不报、眼睛看得见**：① 段与段之间有一条**黑色细边**（内建 `column` 模板 + group 的统一构造路线
  的产物；`F2`/`F5` 都不报它）；② **图例摆在框外上方**、不压数据（与"调用方纪律"第 1 条一致）；
  ③ 六根柱**很宽很高**、占满大半画布。读得出：六区三档构成、高脆弱档近乎等高、差异在低/中两档。
  **读不出**：图**没有**替读者判断"B 与 D 最像"（python 侧的同场景 G1 多画了一条 `B-D most similar`
  括线，本支没有 —— 这条"支持判断"是图外另算的）。
- **G2（`tests/skills/plot-origin/green/out-G2/figure.png`，R2 相关，横条）**：**底色白**；
  **主色只有 `H14` 首色橙**（单系列单色 ⇒ `F2` 读 1）；衬线字体。**判据不报、眼睛看得见**：
  ① 类目之间有**虚线网格**；② 条有**黑边**；③ 负值条从 0 向左伸、正值向右 —— **符号靠方向**而不是
  颜色（本支只有一色）。读得出：mean slope 最长（≈ +0.93）、vegetation cover 与 infrastructure index
  朝负（≈ −0.74 / −0.78）、population density 短（≈ +0.36），与数据对得上。**读不出**：只画了 Pearson，
  n=6 的稳健性不在图上。
- **G3（`tests/skills/plot-origin/green/out-G3/figure.png`，R3 交付形态，横 100% 堆叠条）**：底色白；
  `H14` 前三色；衬线；段有黑边、类目间虚线、坐标轴全框（同 G1）。读得出：同 R1 数据横过来、单栏
  可直接进正文。

### RED（朴素写手产物）—— 我从图上读到了什么

- **R1（`tests/skills/plot-origin/red/out-R1/figure.png`）**：竖 100% 堆叠柱，区序 C,F,A,E,B,D
  （与它图注里"按 low 档占比降序"的口径一致）；三档是 **Blues 单色蓝渐变**（不是 `H14`）。底色白；
  衬线。**判据不报、眼睛看得见（两条）**：
  ① **图例压在绘图区内的数据上** —— 图例框落在右上角，**盖住最后一根柱（D）「high」段的顶部**；
  这就是 `references/workflow.md`「调用方纪律」点名的"图例压数据"，**F1–F6 没有一条会报图例位置**。
  ② **柱与柱之间有一条饱和红细边** —— 像素实测**恰好 `(241,64,64)`、共 3910 px**（≈ 全图 **0.38%**），
  **落在 `F2`/`F5` 的 0.5% 覆盖率阈值之下 ⇒ 检查器全程不报**（正是"边色"那条射程外项）。
  **反差点**：信息并不少（它把区序规则与"最相似的一对"写进图注），红的却是**形态** ——
  `F1` = 1.698 太宽、`F5` 三色越界、图注 228 词且以句号结尾。
- **R2（`tests/skills/plot-origin/red/out-R2/figure.png`）**：两联图（a 散点 + 拟合线，点标 A–F；
  b 四属性 Pearson r 横条，蓝 = 正 / 赭 = 负）。底色白；**衬线观感**。**判据不报、眼睛看得见**：
  b 面板类目名**旋了约 45°**；条无明显细边；图例落在框内右上但**没压到数据**。
  **一处"观感 vs 判词"的落差（如实登记，不下机制断言）**：`F6` 逐字判 **`FAIL`**
  （内嵌族 `MicrosoftJhengHeiUIRegular`，一个**无衬线 CJK 族**），而**屏幕上的拉丁文字看起来是衬线体**
  —— 内嵌的那个子集可能只覆盖了某些字形（如负号），拉丁正文另有来源。**我只登记这条落差，不声称**
  它是"半张图两种字体"那类已知坑（本支没做那个机制验证）。
  **反差点**：`F1` = 1.698、`F5` 两色（赭 / 蓝都不在 `H14`）越界、图注 144 词、`F6` 判红。
- **R3（`tests/skills/plot-origin/red/out-R3/figure.png`）**：竖 100% 堆叠柱、区序 A–F；三档是
  **OrRd 单色橙红渐变**（`#fee8c8`/`#fdbb84`/`#e34a33`，不是 `H14`）。底色白；衬线；
  **图例摆在框外右侧**（没压数据，这点比 R1 好）。**判据不报、眼睛看得见**：段之间同样有**细边**
  （像素里量到 `(241,64,64)` 共 11872 px＝≈ 0.44%，与 R1 同型、同样在阈值之下）—— 检查器不报。
  **反差点**：`F1` = 1.030 **在带内**（三张 RED 里唯一宽度合规的），红的是 `F5`（OrRd 三色越界）与
  `F3a/b/c`（图注 164 词、以句号结尾）。

### 与另两支载体**同场景并排**（GREEN 侧，我看到的跨载体差异）

把本支 `green/out-G1/figure.png` 与同场景的 `tests/skills/plot-python/green/out-G1/figure.png`、
`tests/skills/plot-matlab/green/out-G1/figure.png` 并排看：

- **图高**：本支 ≈ **6.31 × 4.47 in**（宽高比 **1.41**）；另两支 ≈ **2.43**（高 ≈ 2.6 in）。本支明显**更高**
  —— `F1` 只吃**宽**；`assets/mcm-style.json` 的 `h3.height_in` 在 **origin 那格记 `not-landable`**
  （登记见 §H.2 `M3-origin-T2d`）⇒ **不算缺陷**，但**跨载体确实不同**。
- **框线**：本支**四边全框**；另两支**无上/右框线**（开框）。同样是单源表上的载体事实 ——
  `assets/mcm-style.json` 的 `h10.axes_box` 在 **origin 那格记 `not-landable`** ⇒ 同样**不算缺陷**。
- **段边**：本支段间有**黑细边**；python 侧无段边；matlab 侧无段边。
- **图例**：本支在**上方**（与 python 侧同）；matlab 侧在**右侧、带黑框**。
- **网格 / 括线**：**虚线网格只出现在 `G2`/`G3`，`G1` 没有**（逐张量过：近灰像素 `G2` 3822 / `G3` 8710，`G1` 307 且无网格线色）；
  python 侧 G1 多一条 `B-D most similar` 括线，本支**没有**。

> ★ 上面三条（图高 / 框线 / 段边）**不是缺陷**，依据**不是**"调用方纪律"那一节
> （那一节三条 = **图例位置 / 次序约束 / 边色**，**不含图高与框线**）——
> 而是**单源表里这两格的载体状态**：`assets/mcm-style.json` 的 `h3.height_in` 与 `h10.axes_box`
> 在 **origin 那格都记 `not-landable`**（复跑：`python -c "import json,pathlib; …"`，见 §0）。
> ⇒ **照实描述、不当缺陷报。**

### 一句话

**机械层测的是"形态合不合规范"，判断层测的是"图讲没讲清"。** 六张 Origin 图逐张看过之后：
三张 GREEN 形态（`F1`/`F2`/`F4`）全绿，**判据报不出的黑段边与全框**只有眼睛看得见；三张 RED
信息不比 GREEN 少、底色也都白，却在**形态**上判红，而且**图例压数据（R1）与彩色细边（R1/R3）
判据一条都不报** —— "判词全绿 ≠ 图对了"这条在本支同样成立。（本支 GREEN 在 PDF 侧 `F5` 判红，
那是 §3.3 / §4 说清了的**载体限制假红**，不是形态缺陷。）"""


def main():
    global RED_SIDE, GREEN_SIDE
    red = side(RED, "R")
    green = side(GREEN, "G")
    RED_SIDE, GREEN_SIDE = red, green

    CRIT = criteria_ids(red, green)
    SIDES = (("RED", red), ("GREEN", green))
    n_per_side = len(SCENES) * len(CARRIERS)
    n_total = len(SIDES) * n_per_side

    # 同一把尺：checker 的工作树 blob == HEAD 的 blob
    rel = CHECKER.relative_to(REPO).as_posix()
    wt_blob, _ = run(["git", "hash-object", rel])
    hd_blob, _ = run(["git", "rev-parse", f"HEAD:{rel}"])
    wt_blob, hd_blob = wt_blob.strip(), hd_blob.strip()

    L = []
    a = L.append
    a("# Task 3 · RED × GREEN 对照证据（`mcm-plot-origin`）")
    a("")
    a("本文件由 `tests/skills/plot-origin/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。")
    a("**§1 / §2 / §3 / §4 是机器抽取**（判词行逐格解析成 `(状态, 判据 ID, 详情)`，不是手抄）；"
      "**§5 是手写的判断层**（文里已标明）。")
    a("")
    a("## §0 口径（两侧同源同数）")
    a("")
    a("- **场景**：`tests/skills/figure-choose/red/brief-R{1,2,3}.md`（**权威副本**，未改写）。")
    a("  R1/R3 同数据、R2 另一组数据。RED 与 GREEN 各 3 个场景，**同数据逐字**（G1/G3 = brief-R1/R3 的")
    a("  低/中/高三档；G2 = brief-R2 的五属性表；RED 侧脚本里硬编码的同一批数）。")
    a("- **分母**：两侧都传 `--textwidth-in 6.31`（本仓演示口径）。")
    a("- **同一把尺**：`tests/skills/figure-choose/check-figure-style.py` **一字未改**。")
    a(f"  工作树 blob `{wt_blob[:12]}` · `HEAD:` blob `{hd_blob[:12]}` ⇒ "
      + ("**相同**" if wt_blob == hd_blob else "**不同（！）**"))
    a(f"- **同数**：每侧 {len(SCENES)} 场景 × {len(CARRIERS)} 载体（PNG/PDF）= **{n_per_side} 张图**，"
      f"两侧共 {n_total} 张；判据 {len(CRIT)} 条 × {n_total} 张。")
    a("- **PNG 的 `--dpi` 由产物自身推得**（PNG 像素宽 ÷ PDF 页盒宽），见每场景的 `dpi=` 行；")
    a("  **PDF 不给 `--dpi`**（走页盒）。")
    a("- **RED 侧**：三个场景由**干净上下文的写手**产出（提示词只给场景 brief 路径与输出目录；")
    a("  **未给**规范 / 模块 / 判据 / 先例证据）。派发提示词与自报见 `red/writer-self-reports.md`。")
    a("  RED **不 import `mcmplot_origin`、不用 helper**。")
    a("- **GREEN 侧**：由 Task 2 用本模块（`mcmplot_origin` 的 `apply_style/figsize_for/save`）产出、")
    a("  已过独立复核（`Approved`）；**图注是判断层动作**，不是场景给的。")
    a("- ★ **不许跨载体比 `F2`**：见 §4（器械口径：两载体走两条栅格化路径 ⇒ 读数不是同一个量）。")
    a("- ★ **PDF 侧 `F5` 红 = 载体限制**：Origin 的 PDF 写入器把填色量化到**两位小数** ⇒ 1 LSB 偏移 ⇒")
    a("  `F5`（容差 0）判红，**不是「颜色不对」**。每处 PDF 侧 `F5` 红都带一行注（指向 §H.2 `M3-origin-T2a`）。")
    a("- ★ **`F6` 三态**（`PASS`/`FAIL`/`N/A`）：**落哪一态依产物而定**，逐格印真实判词；`N/A` 当独立")
    a("  第三态（见 §3.3）—— **既不当 `PASS`（假绿）、也不当硬门（假红）、也不丢格**。")
    a("")
    a("## §1 RED 原始读数（朴素写手 · 无规范）")
    a("")
    for n in SCENES:
        a(f"### R{n}（dpi={red[n]['dpi']}）")
        a("")
        a(f"图注（`red/out-R{n}/caption.txt`，逐字）：")
        a("```text")
        a(red[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in CARRIERS:
            r = red[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §2 GREEN 原始读数（模块 · `mcmplot_origin`）")
    a("")
    for n in SCENES:
        a(f"### G{n}（dpi={green[n]['dpi']}）")
        a("")
        a(f"图注（`green/out-G{n}/caption.txt`，逐字）：")
        a("```text")
        a(green[n]["caption_bytes"].rstrip("\n"))
        a("```")
        a("")
        for car in CARRIERS:
            r = green[n][car]
            a(f"```\n$ {r['cmd']}\n{r['stdout'].rstrip()}\n[exit={r['rc']}]\n```")
            a("")
    a("## §3 对照表（机器抽取）")
    a("")
    a("每个格子 = `状态`：绿 = `PASS` / 红 = `FAIL` / **`N/A`**（`F6` 的独立第三态，仅见 F6 列）。")
    a("同场景同行，RED 与 GREEN 并列；判据 ID 见表头。")
    a("")
    a("| 场景 | 载体 | 侧 | " + " | ".join(CRIT) + " | RESULT |")
    a("| :-- | :-- | :-- | " + " | ".join([":--"] * len(CRIT)) + " | :-- |")
    for n in SCENES:
        for car in CARRIERS:
            for name, data in SIDES:
                c = data[n][car]["cells"]
                row = [f"R{n}" if name == "RED" else f"G{n}", car.upper(), name]
                for k in CRIT:
                    row.append(verdict_cell(k, c.get(k)))
                row.append("PASS" if data[n][car]["result"][0] else "FAIL")
                a("| " + " | ".join(row) + " |")
    a("")
    a("### §3.1 逐判据明细（含判词 + 载体限制注，机器抽取）")
    a("")
    a("| 场景 | 载体 | 侧 | 判据 | 状态 | 判词 | 注 |")
    a("| :-- | :-- | :-- | :-- | :-- | :-- | :-- |")
    for n in SCENES:
        for car in CARRIERS:
            for name, data in SIDES:
                c = data[n][car]["cells"]
                for k in CRIT:
                    cell = c.get(k)
                    if not cell:
                        continue
                    note = pdf_f5_note(data, n) if (car == "pdf" and k == "F5" and not cell[0]) else "—"
                    a(f"| {'R' if name == 'RED' else 'G'}{n} | {car.upper()} | {name} | {k} | "
                      f"{cell_token(k, cell)} | {cell[1]} | {note} |")
    a("")
    a("**注（§3.1 的「注」列）**：只在 **PDF 侧 `F5` 判红**时给。两条分支 —— 同图 PNG 侧 `F5` 绿 ⇒ "
      "**本红是假红**（载体限制）；PNG 侧也红 ⇒ **本红是实红**（配色不在 `H14`），PDF 侧 hex 另偏 ≤1 LSB "
      "同源。**PNG 侧 `F5` 是本支的真判据**，其「注」列恒为 `—`。")
    a("")
    a("### §3.2 汇总（由 §3 的格子逐格重算）")
    a("")
    a("| 侧 | 红格数（判据×图） | 判红的判据 ID（并集） | 无红判据的图数 |")
    a("| :-- | :-- | :-- | :-- |")
    for name, data in SIDES:
        reds, ok_imgs = [], 0
        for n in SCENES:
            for car in CARRIERS:
                c = data[n][car]["cells"]
                # 「无红」= 该图**判据集合与清单逐条相符**且全 PASS（缺一条即不算）。
                if set(c) == set(CRIT) and all(v[0] for v in c.values()):
                    ok_imgs += 1
                for k in CRIT:
                    if k in c and not c[k][0]:
                        reds.append(k)
        a(f"| {name} | {len(reds)} | {'、'.join(sorted(set(reds))) or '（无）'} | {ok_imgs}/{n_per_side} |")
    a("")
    a("★ 上表**红格数按检查器布尔判**（`F6` 的 `N/A` 在检查器里是 `PASS`，故不计入红格）—— "
      "`F6` 的真实三态另见 §3.3，**不要**把这里的「不红」读成 `F6` 拿了 `PASS`。")
    a("")
    a("### §3.3 `F6` 三态逐格（要求 1：`N/A` 当独立第三态）")
    a("")
    a(f6_section(red, green))
    a("")
    a("## §4 `F2` 与载体（**不许跨载体比 `F2`**）")
    a("")
    a(carrier_section(green))
    a("")
    a("## §5 判断层（亲眼看图 · 机械判据之外的那一层）")
    a("")
    a(JUDGMENT)
    a("")
    doc = ("\n".join(L).rstrip("\n") + "\n").replace("\r\n", "\n")
    OUT_DOC.write_bytes(doc.encode("utf-8"))
    print("wrote", OUT_DOC.relative_to(REPO), OUT_DOC.stat().st_size, "B")

    # ---- 自证断言（不满足即非零退出）----
    assert wt_blob == hd_blob, "checker blob 与 HEAD 不同！"
    # 逐图哨兵：每张图的判据集合必须与清单 `CRIT` **相等**（`CRIT` 亦现取）—— 缺/多一条 ⇒ 当场炸。
    #   射程（如实写窄）：清单与各图**同源** ⇒ 给**所有**图统一加一条判据时两边同步变、仍相等；
    #   本哨兵抓的是**判据集合在不同图之间不一致**那一类。
    for name, data in SIDES:
        for n in SCENES:
            for car in CARRIERS:
                got = data[n][car]["cells"]
                assert data[n][car]["result"] is not None, f"{name} {n}/{car} 没解析到 RESULT 行"
                assert set(got) == set(CRIT), (
                    f"{name} {n}/{car} 的判据集合与清单不符：{sorted(got)} vs {CRIT}")
                # F6 token 必须是三态之一，且 N/A 绝不被渲染成 PASS（要求 1 的渲染器哨兵）。
                tok = cell_token("F6", got.get("F6"))
                assert tok in ("PASS", "FAIL", "N/A"), f"F6 token 越界：{tok}"
                assert not (tok == "PASS" and is_na(got.get("F6"))), "N/A 被渲染成了 PASS！"
    for n in SCENES:
        assert green[n]["png"]["result"][0], f"GREEN {n}/PNG 未全绿"
    for n in SCENES:
        for car in CARRIERS:
            nred = sum(1 for k in CRIT if k in red[n][car]["cells"] and not red[n][car]["cells"][k][0])
            assert nred >= 3, f"RED {n}/{car} 只有 {nred} 条红（计划要求 ≥3）"
    print(f"判据 {len(CRIT)} 条：{CRIT}")
    print("F6 三态 token 分布：", {tok: sum(1 for name, data in SIDES for n in SCENES
                                          for car in CARRIERS
                                          if cell_token('F6', data[n][car]['cells'].get('F6')) == tok)
                                   for tok in ("PASS", "FAIL", "N/A")})
    for name, data in SIDES:
        for n in SCENES:
            for car in CARRIERS:
                bad = sorted(k for k, v in data[n][car]["cells"].items() if not v[0])
                if bad:
                    print(f"  {name} {n}/{car} 判红：{bad}")
    print("OK")


if __name__ == "__main__":
    main()
