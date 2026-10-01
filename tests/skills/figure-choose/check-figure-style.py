#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcm-figure-choose 产物判据。只读被测图，不改任何东西。fail-closed。

用法：
  python tests/skills/figure-choose/check-figure-style.py \
      --fig <path> --caption <text|@file> --textwidth-in <float> [--dpi <int>] [--json]

退出码：0 全 PASS · 1 有 FAIL · 2 参数/参照缺失（fail-closed：**不产生判词**，只管报错退出）
末行：`RESULT: PASS` 或 `RESULT: FAIL（...）`，**恒定是最后一行**（`--json` 的 JSON 打在它**之前**）；
     exit 2 的路径不打印任何判词，也不打印 `RESULT:`。

判据 ID：F1 图宽比 ∈[0.80,1.20] · F2 彩色主色数 ≤4 · F3a 图注以 `Figure <n>:` 起 ·
F3b **正文**词数 ≤12（>17 硬失败）· F3c 句末无句号 · F3d 图注正文非空 ·
F4 背景为白（**合取口径**：**外缘环**众数亮度 ≥ `BG_MIN_LUMA` **且** **近灰众数**亮度 ≥ `BG_MIN_LUMA`；
  全图无近灰像素即判红 —— 量的是**背景**，不是"全图最多的颜色"，口径与局限见 §F4 长注）· F5 显式色序（显著色须**精确命中** `mcm-style.json` 的 H14 集合）·
F6 字体族（PDF **内嵌**字体名的族；三态：PASS 族对 / FAIL 族错 / **N/A 未内嵌任何字体**——PNG 载体亦标不适用）。
  ★ 「内嵌」按 **PDF 的内嵌事实**判（字体描述符里的 `/FontFile`/`FontFile2`/`FontFile3`，Type3 另论），
    **不拿"有没有字体名"当代理**：只被**引用**、没内嵌的字体（base14 的 Helvetica、Origin 导出件）
    `get_page_fonts` 照样报名字 ⇒ 那种 PDF 一律落 `N/A`（Task 3b 修 ③，口径见 `font_embedded()`）。

**两种载体都判**：PNG（本 Task 的 fixture）与 **PDF**（M3 的载体定为 TikZ，主要产物格式）。
  · F1：PDF 走页盒 `doc[0].rect.width/72`（矢量、精确，**不用 --dpi**）；PNG 走 `--dpi`（必须显式给）。
  · F2：PDF 第 1 页按 `RASTER_DPI` 栅格化成 RGB 再数色（`get_pixmap` → `Image.frombytes`）；
        PNG 直接 `Image.open`。**两条载体走同一条 `raster_rgb()`**，保证 F2 口径一致。

**fail-closed 的覆盖面**（拿到不参照就不判，一律 exit 2、且不打印判词）：
  `--textwidth-in ≤ 0` · `--dpi ≤ 0` · `--fig` 不存在／是目录 · `--fig` 不是图像（含 PDF 解析不了） ·
  `--caption @file` 读不出 · PNG 未给 `--dpi`。实现上：所有 I/O 与形参校验都在 `fail_closed()` 里出口，
  **不许**让 `FileNotFoundError` / `UnidentifiedImageError` / `ZeroDivisionError` 之类裸异常漏出去
  ——裸异常的退出码也是 1，会与「判过且红」撞号（那正是本 Task 要消灭的盲区）。

**分母口径**：`--textwidth-in` 由调用方传入，本脚本**不预设**。本仓 2026-09-27 的演示一律传
`6.31`（= 逐篇正文行宽 p90 的全局中位，侦察读数；见 tests/figures-recon/b-stats.txt
`col_w_in: ... median=6.310`）。换口径（如逐篇 p90）会给出不同的比值，**结论可能不同**。

---
**与派发任务书（`.superpowers/sdd/task-m3-t1-brief.md` Step 3）的代码差异 —— 八处，均为实测逼出**

D1（F2 算法）：`resize((320,320))` → `resize((320,320), Image.NEAREST)`。
  任务书用默认重采样（Pillow 12 = BICUBIC），重采样在色带交界处**造出新颜色**，再经
  `//16` 分箱时把**同一个真色劈成两个箱**。实测（命令与输出见
  `tests/skills/figure-choose/figure-style-baseline.txt`）：ok-01 只有 3 色却读成 **4**、
  ok-03 只有 4 色却读成 **5** ⇒ 任务书自带的期望表（ok-01 F2 PASS / ok-03 F2 PASS）
  **当场对不上**。改 NEAREST 后 6 个 fixture 的读数与任务书期望表逐格一致
  （ok-01=3 · ok-02=1 · ok-03=4 · bad-f2=6）。
  **阈值 320/16/24/0.005/≤4 一个没动** —— 动的只是"怎么采到像素"。
  ⚠️ 口径提醒：本函数与侦察用的 `quantize(32, MEDIANCUT)` **不是同一支仪器**（166 张抽样上
  中位 2 vs 4），故 spec 里"实测中位 3"这个数**不能直接用本函数复算**（Task 3 须二选一并写明）。

D2（F3d）：任务书写 `words > 0`，但样本里的空图注形态是 `Figure 13:`（只有前缀没正文，
  17/662）——`"Figure 13:".split()` 有 2 个词，`words > 0` 恒真，**这条判据抓不到它要抓的东西**。
  且任务书自己的 fixture `caption:4 = Figure 4:` 标的是 F3d FAIL，用 `words > 0` 只能得 PASS。
  故 F3d 改为"**去掉 `Figure N:` 前缀后的正文非空**"（F3a 已单独判前缀形态）。

D3（退出码）：任务书写 `sys.exit("...")`（= exit 1），但同一份任务书的 Interfaces 段与
  spec 都写死 `2 = 参数/参照缺失（fail-closed）`。两者冲突时取 **exit 2**，理由：`1` 已被
  "有 FAIL" 占用，若 fail-closed 也退 1，"判过且红"与"根本没判成"就分不开——这正是本任务
  M3 变异要证的那件事。

D4（PDF 的 F2，**独立复审判定 Important-1 逼出**）：任务书的 Step 3 代码把 `Image.open(fig)`
  无条件用在 F2 上，而 PDF 是本设计的**主要产物格式**（载体已定为 TikZ）。实测一张
  6.0×2.6 in 的 PDF：rc=1、**stdout 空**、`PIL.UnidentifiedImageError` —— 即"F1 用 fitz、
  F2 用 Pillow"这个半吊子状态让 PDF **根本判不完整**。本实现的取法：**F2 也吃 PDF**——
  第 1 页 `get_pixmap(dpi=RASTER_DPI, colorspace=csRGB, alpha=False)` → `Image.frombytes`
  → 与 PNG 走同一条 `color_count`。因此文件头"两种载体都判"的自称与本实现一致。
  （另一条路是删掉 fitz 分支、写死"仅 PNG"，但那会与本设计的载体选择直接冲突。）

D5（fail-closed 覆盖面，**独立复审判定 Important-2 逼出**）：任务书的 Step 3 只对
  `--textwidth-in ≤ 0` 与"图不存在"做了守卫，其余全部裸异常漏出（实测：`@不存在` →
  `FileNotFoundError` rc=1；图不是图像 → `UnidentifiedImageError` rc=1；`--fig <目录>` →
  `PermissionError` rc=1；`--dpi 0` → `ZeroDivisionError` rc=1；**`--dpi -200` 竟然打印判词**
  `FAIL F1 图宽比 -0.951`）。本实现把这五条全并进 `fail_closed()`，并**把 `--dpi ≤ 0` 与
  `--textwidth-in ≤ 0` 同等拒绝**。

D6（`--json` 的位置，**独立复审判定 R-4 逼出**）：任务书把 JSON 打在 `RESULT:` **之后**，
  于是"末行固定为 `RESULT:`"这条接口契约在 `--json` 下**不成立**。本实现把 JSON 挪到
  `RESULT:` 之前：末行恒为判词行，JSON 是它的机器可读副本。

D7（F3b 的词数口径，**Task 6 GREEN 对照的 Important-2 逼出**）：F3b 原先数**整条图注**
  （`cap.split()`，含 `Figure N:` 这 2 个词），而规范 H9 与它的复跑仪器 `house-metrics.py`
  的 `cap_words_*` 用的是**去掉 `Figure N:` 前缀后的正文**（口径原文见
  `references/provenance.md` 的 P-D-c1）。同一批 662 条图上两口径**相差恰好 2 词**、
  **不可互换** ⇒ 出货检查器与规范在当时是**两个口径**。本轮收敛到**规范侧**：
  `words = len(caption_body(cap).split())`（`caption_body` 见下，F3d 本就在用）。
  **常量 `CAP_MAX` 12 / `CAP_HARD` 17 与 `G-H9-*` 守卫一个没动**——12/17 本来就是
  **正文口径**的 p95/max（`c8-caption.tsv:913`：正文 p95=12 / max=17；含标签口径是 14/19）。
  影响面（实测）：GREEN 三份由"整条 13 词"变为"正文 11 词"⇒ F3b 转绿；RED 三份的图注以
  `Figure 1.`（句点、无冒号）起，`caption_body` 切不出前缀 ⇒ 整条算正文 ⇒ 读数一字不变
  （203/285/177，仍红）。

D8（F6 的"内嵌"口径，**Task 3b 修 ③ 逼出**）：Task 3 的 F6 只看 `get_page_fonts(rec[3])` 的名字，
  **空集 ⇒ N/A**。但"只引用、没内嵌"的字体（base14 的 Helvetica、Origin 导出的那 34/34 件）
  `get_page_fonts` **照样报名字**、xref 里却没有 `/FontFile*` ⇒ 那种 PDF 会被**判族**（PASS/FAIL），
  而不是 design §7.3 要求的 `N/A`。现按**内嵌事实**判（`font_embedded()`：Type3 另论，
  其余核描述符 `/FontFile*`、Type0 走 `DescendantFonts`）⇒ 只引用不算内嵌、那种 PDF 落 `N/A`，
  判词里写清"未内嵌 ⇒ 不适用"；无字体与只引用两类**分开写**（原先都写"未内嵌任何字体"，
  把"这份文件里没有字体"也说成"未内嵌"）。
  **判据没放宽**：可接受族表 `FONT_FAMILY_OK`、三态语义、`N/A` 仍是 `PASS`+详情以 `N/A` 开头，
  一个没动；实测 16 份管道内 PDF 上旧新两版**只有 4 份**的 F6 行不同（3 份是措辞细分、
  1 份是新增的"只引用"样本由 FAIL 转 N/A），**其余 12 份 rc 与 F6 行逐字相同**。
  另加变异 `M58` 钉住这条承重件（拆掉内嵌事实 ⇒ 该样本由 `N/A` 转 `FAIL`）。
"""

import argparse
import json
import pathlib
import re
import sys

import fitz                      # PyMuPDF
from PIL import Image

F1_LO, F1_HI = 0.80, 1.20        # spec house-style #1（实测 p25 / max）
F2_MAX = 4                       # spec #4（实测中位 3）
CAP_MAX, CAP_HARD = 12, 17       # spec #9（实测 p95 / 全样本上界）
RASTER_DPI = 150                 # PDF 栅格化密度（只影响 F2 采样，与 F1 无关；见 D4）
EXIT_FIG_FAIL = 1                # 判过，且至少一条判据红
EXIT_FAIL_CLOSED = 2             # 拿不到参照：不产生判词，只报错退出

# ---- M3 Task 3 新增三条判据（F4 底色 / F5 显式色序 / F6 字体族）的常量 ----
# ★ 底色下限 `BG_MIN_LUMA` 由**实测两端**标定，**不是选的**（design §7.1 / Global Constraint 9）：
#   深色端 = 实测 MATLAB 深色底产物画布 (16,16,16) / 轴区 (18,18,18)（tests/m3-matlab-recon/）；
#   浅色端 = (255,255,255)（python 侧 6 张图 + MATLAB 浅色配方）。取两端中点：(18 + 255) // 2 = 136
#   （Task 3 Step 1 当场打印）。亮度用 Rec.601 加权：299R + 587G + 114B（`luma()`）。
#   ★ 取样区（F4 的两路，见 `check()` 里 §F4 那一段）**也由这两端标定**：
#     两个端都**中性**（`max(r,g,b)-min(r,g,b)` = 0）⇒ 都落在「近灰」档（`max-min < 24`）里
#     ⇒ 「近灰众数」这一路在两端都取得到背景。
#   ⚠️ **订正（2026-10-01 F4 再修一轮）**：旧注那句「内容色（饱和）落在档外」**对中性色内容不成立**
#     —— 均匀中灰 `(100,100,100)` 就在档内，与中性色背景同档。故「近灰众数」这一路**单靠它自己
#     分不开**「中性色内容」与「中性色背景」；**「外缘环」那一路也救不了**（2026-10-01 二次订正：
#     此处原写「分开它们的是「外缘环」那一路」，与 §F4 里被订正的同一句过度声明同型）—— 合取
#     ⇒ 近灰众数红即红；内容内缩、不碰边时环读到**纯白**也照样红，见 §F4 长注「已知局限」②的
#     实测反例。两路合取见 `check()` 的 §F4。
BG_MIN_LUMA = 136
# ★ 字体族判据可接受的内嵌字体名（design §1.1「按族等价」/ §7.3）：
#   python 入库 OTF = TeXGyreTermesX-*；matlab / origin 取系统 Times New Roman（含 PS 名与 Nimbus/FreeSerif 等价实现）。
FONT_FAMILY_OK = ("TeXGyreTermesX", "TimesNewRomanPSMT", "TimesNewRoman", "NimbusRoman", "FreeSerif")
SUBSET_RE = re.compile(r"^[A-Z]{6}\+")     # 剥 PDF 字体子集前缀；与 plot-python/check-style-freshness.py L87 同形
# ★ F6 的「内嵌」事实（Task 3b 修 ③）：字形真在 PDF 里时，字体**描述符**带
#   `/FontFile`（Type1）/ `/FontFile2`（TrueType）/ `/FontFile3`（CFF/OpenType）。
#   **只被引用、没内嵌**的字体（base14 的 Helvetica、Origin 导出的 PDF）这三者一个都没有，
#   而 `get_page_fonts()` **照样报它的名字** ⇒ 不许拿"有没有字体名"当内嵌的代理。
#   实测：Origin 的 34/34 个导出件 `/FontFile*` = 0（tests/m3-origin-font-probe/out-pdf-embedding-scan.txt）。
FONTFILE_RE = re.compile(r"/FontFile[23]?(?![0-9A-Za-z])")
FD_RE = re.compile(r"/FontDescriptor\s+(\d+)\s+0\s+R")
DESC_FONTS_RE = re.compile(r"/DescendantFonts\s*\[\s*(\d+)\s+0\s+R")


def fail_closed(msg):
    """拿不到参照时的唯一出口：非零退出，**不得**返回空结果静默通过。"""
    print(msg, file=sys.stderr)
    sys.exit(EXIT_FAIL_CLOSED)


# ★ 显式色序的允许集合 = **单源**取自 Task 2 的载体无关样式表 mcm-style.json（**不许手写第二份**）。
#   路径**不能**写死层数：变异驱动器会把本检查器**复制**到 `fixtures/_mut/`（那时 `parents[N]` 就不再是仓根，
#   实测 `parents[2]`/`parents[3]` 都会落到仓外 ⇒ fail-closed），故**由本文件所在目录向上一层找**。
#   `SERIES_COLORS` 必须写成**单行**：变异 `M55`/`M57` 按字面串替换它。
_STYLE_REL = pathlib.Path(".claude/skills/mcm-figure-choose/assets/mcm-style.json")


def _style_path():
    """从本文件所在目录**向上**找载体无关样式表（复制到 `fixtures/_mut/` 后也能命中）。"""
    here = pathlib.Path(__file__).resolve().parent
    for base in (here, *here.parents):
        if (base / _STYLE_REL).is_file():
            return base / _STYLE_REL
    return None


_STYLE_PATH = _style_path()
if _STYLE_PATH is None:
    fail_closed(f"FAIL: 向上找不到样式表 {_STYLE_REL}（fail-closed）")
try:
    _STYLE = json.loads(_STYLE_PATH.read_text(encoding="utf-8"))
except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
    fail_closed(f"FAIL: 读不出样式表 {_STYLE_PATH}（{type(e).__name__}: {e}）（fail-closed）")
SERIES_COLORS = {c.lower() for c in next(e["value"] for e in _STYLE["entries"] if e["id"] == "series.color")}


def read_caption(spec):
    """`--caption` 原样返回；`@file` 读文件。读不出 ⇒ fail_closed（不裸抛 FileNotFoundError）。"""
    if not spec.startswith("@"):
        return spec
    path = pathlib.Path(spec[1:])
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图注文件 {path}（{type(e).__name__}: {e}）（fail-closed）")


def raster_rgb(path):
    """把图变成 RGB 像素供 F2 数色：PDF 走第 1 页栅格化，PNG/JPG 走 Pillow。

    两个载体的像素都经同一条 `color_count`，故 F2 口径一致。读不出 ⇒ fail_closed。
    """
    try:
        if path.suffix.lower() == ".pdf":
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                pm = doc[0].get_pixmap(dpi=RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
                return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        with Image.open(path) as im:
            return im.convert("RGB")       # 立刻取像素，脱离文件句柄；坏文件在这里就报
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图 {path}（{type(e).__name__}: {e}）（fail-closed）")


def color_count(im):
    """彩色主色数：去掉近黑/近白/近灰，只数占比 >=0.5% 的颜色。

    采样用 NEAREST：重采样（BICUBIC 等）会在色带交界造出新色，`//16` 分箱随即把同一真色
    劈成两箱 ⇒ 系统性**多**数（见文件头 D1）。
    """
    im = im.convert("RGB").resize((320, 320), Image.NEAREST)   # 与分辨率无关；不重采样造色
    tot, keep = 320 * 320, {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24:           # 近灰（含黑/白）
            continue
        keep[(r // 16, g // 16, b // 16)] = keep.get((r // 16, g // 16, b // 16), 0) + cnt
    return sum(1 for c in keep.values() if c / tot >= 0.005)


def luma(rgb):
    """Rec.601 加权亮度（F4 的唯一亮度口径）：(299R + 587G + 114B) // 1000。"""
    r, g, b = rgb
    return (r * 299 + g * 587 + b * 114) // 1000


def outer_ring_mode(im):
    """外缘环（四边、厚度 `max(1, round(0.01 * min(w,h)))`，**含四角**）的颜色众数。

    返回 `(rgb, 该色在环里的像素数, 环的总像素数)`。F4 的「外缘环」那一路用它，
    作用是把「深色底」与「白底上的深色内容」分开：前者环是深色、后者环仍是白。
    ★ **但它不是"唯一"这样的量，且对「内容铺到最外圈」（紧裁 / 去边）的情形失效**（那时后者的环
      也变深 ⇒ 分不开）。这一句的限定、反例与完整口径**与 §F4 长注「已知局限」①同一出处**
      （**在此不另写一套**；`outer_ring_mode()` 的 ① 那一路订正见 `check()` 里 §F4 长注）。

    ★ **平票的取法不是小事**（如实登记）：按**行主序首次出现序**计数，`max` 取**首个**最大值
      —— 与 `PIL.getcolors()`（`check()` 的近灰那一路就用它）**同一口径**，故平票时**行主序里
      先出现的色胜出**。本仓 fixture 里「上白边 vs 下色带」的环**恰恰是精确平票**（实测
      `ok-01`/`ok-02`/`ok-03`/`ok-04`/两张 `bad-f1-*`/`good-color-order`/`bad-color-order`
      共 8 张两两平票），而左上角是白 ⇒ 平票由白胜出。若把计数换成 `set`（哈希序遍历），
      这 8 张里的若干张当场翻红 —— 这不是"某一条判据"，是**口径**，故写死在这里。
    """
    w, h = im.size
    t = max(1, round(0.01 * min(w, h)))
    px = im.load()
    cnt = {}
    for y in range(h):
        edge_row = y < t or y >= h - t
        for x in range(w):
            if edge_row or x < t or x >= w - t:
                c = px[x, y]
                cnt[c] = cnt.get(c, 0) + 1
    rgb, n = max(cnt.items(), key=lambda kv: kv[1])       # 平票取首个（行主序首见 = 左上角）
    return rgb, n, sum(cnt.values())


def fig_width_in(path, dpi):
    """图宽（英寸）。PDF 用页盒（矢量、精确，不用 --dpi）；PNG 走 --dpi（必须显式给）。"""
    if path.suffix.lower() == ".pdf":
        try:
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                return doc[0].rect.width / 72.0
        except Exception as e:                                 # noqa: BLE001（fail-closed 出口）
            fail_closed(f"FAIL: 读不出 PDF 页盒 {path}（{type(e).__name__}: {e}）（fail-closed）")
    if dpi is None:
        fail_closed("FAIL F1: PNG 需要显式 --dpi（PNG 的 dpi 元信息不可信，见 provenance）")
    try:
        with Image.open(path) as im:
            return im.size[0] / dpi
    except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
        fail_closed(f"FAIL: 读不出图 {path}（{type(e).__name__}: {e}）（fail-closed）")


def caption_body(cap):
    """图注正文 = 去掉 `Figure N:` 前缀之后的部分；切不出前缀时整条算正文（F3a 会另外报红）。"""
    m = re.match(r"^Figure\s+\d+\s*:", cap)
    return cap[m.end():].strip() if m else cap


def font_embedded(doc, xref, ftype):
    """该页字体**是否内嵌**（判的是"内嵌"，不是"被引用"）—— F6 的第三态靠它分。

    · **Type3**：字形过程（`CharProcs`）本身就是 PDF 里的流、描述符里没有 `/FontFile*`
      ⇒ **算内嵌**（python 侧入库产物走的就是这条，见 `out-G1/figure.pdf`）。
    · **其余**（Type1 / TrueType / Type0…）：按**字体描述符**里的 `/FontFile*` 判；
      Type0 是复合字体，内嵌事实落在 `/DescendantFonts` 指的 CIDFont 上。
    · **只被引用、没内嵌**（base14 / Origin 导出件）⇒ **不算内嵌** ⇒ 该 PDF 走 `N/A` 分支。

    ★ 口径（写实，别读成"覆盖了所有退路"）：**族只按内嵌的字体判** —— 一个只被引用的字体的族
      **不是这份文件里的事实**（真正渲染时用哪个替代字体由阅读器定），拿名字去判族是把"引用"
      当"内嵌"。同页若同时有内嵌与只引用两种字体，**只引用那部分写进判词、但不参与判族**。
    """
    if not xref:                       # fitz 对个别字体给 xref 0 ⇒ 取不到对象，按"没内嵌"处置
        return False
    if ftype == "Type3":
        return True
    obj = doc.xref_object(xref, compressed=True)
    if FONTFILE_RE.search(obj):
        return True
    m = FD_RE.search(obj)              # 描述符是单独的间接对象：/FontDescriptor N 0 R
    if m and FONTFILE_RE.search(doc.xref_object(int(m.group(1)), compressed=True)):
        return True
    m = DESC_FONTS_RE.search(obj)      # Type0：内嵌事实在 DescendantFonts[0] 的 CIDFont / 其描述符上
    if m:
        dobj = doc.xref_object(int(m.group(1)), compressed=True)
        if FONTFILE_RE.search(dobj):
            return True
        m2 = FD_RE.search(dobj)
        if m2 and FONTFILE_RE.search(doc.xref_object(int(m2.group(1)), compressed=True)):
            return True
    return False


def page_font_split(doc):
    """整份 PDF 的字体按**内嵌 / 只引用未内嵌**分成两组（名字已剥子集前缀）。"""
    emb, ref = set(), set()
    for pno in range(doc.page_count):
        for rec in doc.get_page_fonts(pno):
            name = SUBSET_RE.sub("", rec[3])
            (emb if font_embedded(doc, rec[0], rec[2]) else ref).add(name)
    return emb, ref


def check(fig, caption, textwidth_in, dpi):
    res = []
    if textwidth_in <= 0:
        fail_closed("FAIL: --textwidth-in 必须为正（fail-closed）")
    if dpi is not None and dpi <= 0:          # 与 --textwidth-in 同等拒绝（见文件头 D5）
        fail_closed(f"FAIL: --dpi 必须为正（收到 {dpi}）（fail-closed）")
    # ---- 底色 / 颜色身份：共用一次栅格化（F4 与 F5 共用，避免两次读图口径不一致）
    im4 = raster_rgb(fig)
    tot4 = im4.size[0] * im4.size[1]
    _cols = im4.getcolors(tot4) or []

    # ================= F4 底色：论文背景是白。★ 合取口径（**量出来的**，不是设计出来的）=========
    # 规则：**（外缘环众数亮度 ≥ BG_MIN_LUMA）且（近灰众数亮度 ≥ BG_MIN_LUMA）**。
    #   ① **外缘环** = 图像四边、厚度 `max(1, round(0.01 * min(w,h)))` 的一圈像素（含四角），
    #      取众数（`outer_ring_mode()`）。它把「深色底」与「白底上的深色内容」分开：前者的环是
    #      深色、后者的环仍是白。**但它不是"唯一"这样的量**（2026-10-01 订正：旧注释写死"唯一"，
    #      是过度声明）—— 它自己有反例（内容铺到最外圈时后者的环也变深 ⇒ 见「已知局限」①），
    #      而 ② 那一路也分不开二者（`bad-bg-navy.png` 的近灰众数是白线 `(255,255,255)` L255
    #      ⇒ 只看 ② 会把深蓝底判成 PASS（假绿））。故**必须**用 1% 外缘环、不许退回角像素
    #      （design §7.1 当初据 MATLAB 实测「外围白、轴区仍深」否掉了角落单像素）。⚠️ 旧注释此处
    #      另写「用『四角补丁』实测会假红 6 张」，已于 2026-10-01 **删除**：该读数的口径没落盘、
    #      按最自然的角补丁读法复算与之不符（`bad-f2-five-colors` 与满幅热力**四角全白** ⇒
    #      角补丁读它们得到白、判 PASS，与「假红它俩」矛盾）⇒
    #      **只作已撤回的历史转述、不作依据**（登记与书证见 `docs/mcm-suite-todo.md` §H.2 `M3-style-F4c`）。
    #   ② **近灰众数** = 只在 `max(r,g,b)-min(r,g,b) < 24` 的像素里取众数（与 F2/F5 同一支仪器，
    #      见 color_count()）。★ **它量的是"某个单一色的像素数（众数）"，不是"面积"**（2026-10-01
    #      订正：旧注释写成"内容面积压过白底"，那只在**浅底是单一色**时才等价）—— 浅底被**拆成多档**
    #      （渐变 / 棋盘 / 噪声）时，**面积更小的内容也能占住近灰众数** ⇒ 近灰那路假红。真机制 =
    #      **近灰档里"像素数最大的那个单一色"是内容色**。它负责终审 I-1 那一类：内容占比压过白底
    #      时（如 ok-04 = 白底 19.71% + 四色带各 20.0%），全图众数会落到内容色上，而近灰档里仍取得到白。
    #      实测对照（仓外当场造 1200×520；内容 = 内缩中灰 `(100,100,100)` 占 **40.0%**、浅底占 **60.0%**，
    #      两件**面积完全相同**）：**平白底** ⇒ 近灰众数 = 白（60.0%）**PASS**；**渐变白底**（255→246
    #      十档、每档 10.0%）⇒ 近灰众数 = 中灰（40.0%）**FAIL**。差别**只在浅底是否被打碎**。
    #   ③ **全图无近灰像素**（整幅饱和色，如整幅 `#E69F00`）⇒ **直接判红**：
    #      **取消**旧的「退回全图众数」分支 —— 那条分支实测会把整幅 `#E69F00` 判成 PASS 162。
    #   ④ **为什么是合取**：合取只会**收紧**、不会放宽（硬纪律：不许放宽判据来自证干净）。
    #   ⚠️ 单靠 ② **分不开**「中性色内容」与「中性色背景」：均匀中灰 `(100,100,100)` 也在近灰档里
    #      ⇒ 白底 35% + 中灰 65% 那种图，近灰众数取到中灰、亮度 100 < 136 ⇒ 红。这不是回归
    #      （旧口径同样红）；**也不能说成"靠 ① 把中性内容/中性背景分开"**（2026-10-01 订正：
    #      旧注释如此写，对"内容不碰边"的情形为假）—— 合取 ⇒ ② 红即红，环读到白**也救不了**，
    #      实测反例见下面「已知局限」②。这一路只能**如实登记为局限**。
    #   ★ 阈值 `BG_MIN_LUMA` = 136 由**实测两端**标定（深端 (18,18,18) / 浅端 (255,255,255) 的中点），
    #     本轮**未重标定**（design §7.1 / GC9）。
    #   ★ **已知局限（不许藏）**：本口径有**两条已知的独立**假红通道（2026-10-01 订正：旧注释写
    #     "唯一的假红通道"，为假）。**"两条"= 本仓今天已当场复算的两条，本清单不声称穷尽** ——
    #     判据是「环众数 ∨ 近灰众数」两路合取：**能让任一路读到暗色的背景构造，还可能有别的**
    #     —— 本清单只登记今天已复算的两条。合取 ⇒ 任一路红即红 ⇒ **① 救不了 ②**，这正是 ② 能独立存在的原因：
    #     ① **内容一直铺到图像最外圈**（紧裁 / 去边）：外缘环被内容占据 ⇒ **环那一路**假红。
    #        本仓三个权威载体（matplotlib `savefig` / MATLAB `print` / Origin `expGraph`）的**合规
    #        （浅色）产物**留白边（**就本仓已入库 / 当场实读的样本而言，不声称覆盖两载体的全部产物**；
    #        matplotlib 侧当场出图实读：**无标签**线图 1% 外缘环 **100.00%** 纯白、四角 `(255,255,255)`；
    #        **带轴标签**的线图**不到 100%**（复核件 946×375 `tight_layout(pad=0.1)` 量得 **99.56%**，
    #        本机复跑同尺寸 99.65%、1200×520 件 99.88%）⇒ 这个"100%"**随图而变、不冒充普适**，
    #        MATLAB / Origin 两侧的产物读数见 `tests/m3-matlab-recon/out-pixels-backgrounds.txt`、
    #        `tests/m3-origin-probe/out-c-export-margin-formats.txt`），紧裁的 `exportgraphics`
    #        本来就不是权威载体（design §0.1 已裁）。
    #        实测反例（白底 1200×520 + 5px 黑框贴最外圈）：`FAIL F4`；环 `(0,0,0)` L0（占环
    #        **100.00%**）⇒ 环红，而近灰众数 = `(255,255,255)` L255（占全图 97.26%）⇒ 近灰绿。
    #     ② **中性灰（或深色）内容占住了"近灰众数"那一格**（`max−min < 24`，如中灰 `(100,100,100)`）：
    #        与内容是否碰边**无关** —— 外缘环可以是 100% 纯白，近灰众数仍被内容占住 ⇒ **近灰那一路**
    #        假红（上面 ① 的反例里是"环红/近灰绿"，这里恰好相反 ⇒ 两路彼此独立）。
    #        ★ **它量的不是"面积压过"**（见上面 ② 定义的订正）：浅底被打碎成多档时，"面积更小的
    #        内容"也占得住这一格 —— **渐变白底那件（内容仅 40.0%）就是本条的又一条实测反例**。
    #        实测反例（白底 1200×520 + 内缩灰块 `[60,60]–[1140,460]`，中灰 `(100,100,100)`）：
    #        `FAIL F4`；外缘环 `(255,255,255)` L255（占环 **100.00%**）⇒ 环绿；近灰众数
    #        `(100,100,100)` L100（占全图 **69.47%**）⇒ 近灰红。对照：同为占全图 69.47% 的
    #        `ok-06`（内容是**饱和色** `#0072B2`、环 100% 白、近灰众数 = 白 30.53%）**PASS**
    #        ⇒ 中性灰内容与饱和色内容被**不对称**对待。
    #   ★ **薄余量登记**：白底夹具的环内容常是「上白边 vs 下色带」的**精确平票**（本仓 8 张），
    #     平票由「行主序首见 = 左上角白」胜出（见 `outer_ring_mode()` 的注释）—— 口径一变、
    #     若改走 `set` 哈希序，这 8 张里的若干张当场翻红。
    ring_rgb, ring_cnt, ring_tot = outer_ring_mode(im4)
    luma_ring = luma(ring_rgb)
    gray = [t for t in _cols if max(t[1]) - min(t[1]) < 24]
    if gray:
        gray_cnt, gray_rgb = max(gray, key=lambda t: t[0])     # 平票取首个（与 getcolors 同序）
        luma_gray = luma(gray_rgb)
        gray_txt = f"近灰众数 RGB {gray_rgb} 亮度 {luma_gray}（占全图 {gray_cnt / tot4:.2%}）"
        f4_ok = luma_ring >= BG_MIN_LUMA and luma_gray >= BG_MIN_LUMA
    else:
        gray_txt = "近灰众数 无（全图无近灰像素 ⇒ 红）"
        f4_ok = False
    res.append(("F4", f4_ok,
                f"外缘环 RGB {ring_rgb} 亮度 {luma_ring}（占环 {ring_cnt / ring_tot:.2%}）；"
                f"{gray_txt}；下限 {BG_MIN_LUMA}"))
    ratio = fig_width_in(fig, dpi) / textwidth_in
    res.append(("F1", F1_LO <= ratio <= F1_HI, f"图宽比 {ratio:.3f}（分母 {textwidth_in:.2f} in）"))
    n = color_count(raster_rgb(fig))
    res.append(("F2", n <= F2_MAX, f"彩色主色数 {n}"))

    # F5 显式色序：图上**显著**颜色（非灰、占比 ≥0.5%，与 F2 同口径）必须**精确命中** H14 允许集合。
    # ★ 用**精确比对**而不是「最近调色板色距离 + 容差」（design §7.2 / 任务书口径）：实测本机旧默认色序到
    #   最近 H14 色的欧氏 RGB 距离为 #ff9500→#E69F00 = 26.93 / #0c5da5→#0072B2 = 27.46 /
    #   #00b945→#009E73 = 53.34（最小 ≈26.93；Task 3 Step 5 当场用 out-G1/figure.png 量出）；而合法 H14
    #   产物的主色落在允许集合上、距离 = 0。⇒ T = 27 只放 #ff9500 一色过、#0c5da5 与 #00b945 仍越界（F5 仍红）；
    #   **要整条旧色序都躲过 F5 需容差 ≥ 53.34** ⇒ 无安全区间可用 ⇒ 容差取 0（精确比对）。
    far = []
    for cnt, (r, g, b) in _cols:
        if max(r, g, b) - min(r, g, b) < 24:          # 与 color_count() 同口径剔近灰
            continue
        if cnt / tot4 < 0.005:                         # 与 color_count() 同口径：占比 <0.5% 不算主色
            continue
        hx = f"#{r:02x}{g:02x}{b:02x}"
        if hx not in SERIES_COLORS:
            far.append((hx, round(cnt / tot4, 4)))
    far.sort(key=lambda t: -t[1])
    res.append(("F5", not far, f"越界主色 {len(far)} 种（不在 H14 允许集合）：{far[:4]}"))
    cap = caption.strip()
    res.append(("F3a", bool(re.match(r"^Figure\s+\d+\s*:", cap)), "图注以 `Figure N:` 起"))
    body = caption_body(cap)                              # 正文口径：见文件头 D7（口径与 H9 收敛）
    words = len(body.split())
    res.append(("F3b", words <= CAP_MAX, f"图注词数 {words}（上限 {CAP_MAX}，硬上限 {CAP_HARD}）"))
    if words > CAP_HARD:
        res[-1] = ("F3b", False, f"图注词数 {words} 超硬上限 {CAP_HARD}")
    res.append(("F3c", not cap.endswith("."), "句末不加句号"))
    res.append(("F3d", bool(body), f"图注正文非空（正文 {len(body.split())} 词）"))

    # F6 字体族：读**产物内嵌字体**（不能看属性设没设 —— 实测 MATLAB 侧 set 不存在的名字不报错、get 还回声、产物静默回退）
    if fig.suffix.lower() != ".pdf":
        # PNG 里没有字体名 ⇒ 不许假绿：如实标「不适用」，并在详情里写出这个事实。
        res.append(("F6", True, "PNG 载体无内嵌字体信息 ⇒ 本判据在 PNG 上不适用（如实标，不假绿）"))
    else:
        # ★ 三态：内嵌且族对 = PASS；内嵌但族错 = FAIL；**一个都没内嵌 = N/A**。
        #   「内嵌」按 `/FontFile*`（等价的内嵌事实）判 —— **只引用不算内嵌**（见 `font_embedded()`）。
        with fitz.open(fig) as _d:
            emb, ref = page_font_split(_d)
        if not emb:
            if not ref:
                res.append(("F6", True, "N/A 本 PDF 未引用任何字体 ⇒ 本判据不适用（无字体可判）"))
            else:
                res.append(("F6", True,
                            f"N/A 本 PDF **未内嵌**任何字体（只被引用、未内嵌：{sorted(ref)}）⇒ "
                            f"未内嵌 ⇒ 本判据不适用（族不是这份文件里的事实；实测 Origin 的 PDF 即如此）"))
        else:
            ok6 = all(any(k in f for k in FONT_FAMILY_OK) for f in emb)
            extra = "" if not ref else f"；另有只被引用、未内嵌的 {sorted(ref)}（未内嵌 ⇒ 不参与判族）"
            res.append(("F6", ok6, f"内嵌字体 {sorted(emb)}{extra}"))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fig", required=True)
    ap.add_argument("--caption", required=True)
    ap.add_argument("--textwidth-in", type=float, required=True)
    ap.add_argument("--dpi", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.fig)
    if not p.is_file():                       # 不存在 / 是目录 / 是设备文件，一律 fail-closed
        fail_closed(f"FAIL: 图不存在或不是普通文件 {a.fig}（fail-closed）")
    cap = read_caption(a.caption)
    res = check(p, cap, a.textwidth_in, a.dpi)
    for cid, ok, why in res:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {why}")
    if a.json:                                # JSON 在判词行**之前**（见文件头 D6）
        print(json.dumps({c: ok for c, ok, _ in res}, ensure_ascii=False))
    bad = [c for c, ok, _ in res if not ok]
    print(f"RESULT: {'PASS' if not bad else 'FAIL'}" + ("" if not bad else f"（{','.join(bad)}）"))
    sys.exit(0 if not bad else EXIT_FIG_FAIL)


if __name__ == "__main__":
    main()
