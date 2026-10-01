"""生成判据 fixtures。用途：让检查器的每条判据都有一个'必须红'的样本。"""
import io, pathlib
import fitz
from PIL import Image, ImageDraw
D = pathlib.Path(__file__).parent

def fig(name, w_in, h_in, colors):
    """按 200 dpi 出图：w_in*200 px 宽。colors=彩色主色列表（外加大片白底）。"""
    px, py = int(w_in*200), int(h_in*200)
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    band = py // (len(colors) + 1)
    for i, c in enumerate(colors):
        d.rectangle([0, band*(i+1), px, band*(i+2)], fill=c)   # 每色占 ~1/(n+1) 面积
    im.save(D/name, dpi=(200, 200))

# 合格：6.0in 宽（正文 6.31in ⇒ 比值 0.951），3 色
# ★ 2026-10-01（M3-style 终审 I-4）：`ok-*` 的系列色**改用 H14 显式色序**。
#   原先用的是 Tol-bright（`#4477AA/#EE6677/#228833/#CCBB44`）—— 那是 H14 之前的遗留色序，
#   在 F5 下**全部越界** ⇒ 名为 `ok-*` 的图却不合规（名不副实）。合格图必须用规范的色序
#   （H14），故 `ok-*` 一律取 H14 的前 N 色。F2 读数不受影响（色数不变：3 / 1 / 4 / 4 / 4）。
fig("ok-01.png", 6.0, 2.6, ["#E69F00", "#56B4E9", "#009E73"])
fig("ok-02.png", 5.1, 2.6, ["#E69F00"])                       # 0.808，单色
fig("ok-03.png", 6.3, 3.0, ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"])  # 0.999，4 色
# 违规：各只踩一条
fig("bad-f1-too-narrow.png", 4.4, 2.6, ["#4477AA"])           # 0.697 < 0.80
fig("bad-f1-too-wide.png",   7.8, 3.0, ["#4477AA"])           # 1.236 > 1.20
fig("bad-f2-five-colors.png", 6.0, 2.6,
    ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"])  # 6 色

# 追加（2026-09-27 实施时实测逼出，见 figure-style-baseline.txt）：
# 原 6 张 fixture 上，把 F2 的噪声地板 `>= 0.005` 改成 `>= 0.0`，**读数一模一样**
# （ok-01=3 ok-02=1 ok-03=4 bad-f2=6，六张全等）⇒ 地板成了**恒真判据**，变异证不了它。
# 故补一张带"稀有彩色"的样本：4 个主色（各 ~20%）+ 一个 50×35 px 的小色块（~0.28%），
# 地板一改它就数出第 5 色 ⇒ 地板真的参与判定。
def fig_ok04():
    """ok-04：4 个主色 + 1 个占比 <0.5% 的稀有彩色（小色块，形如小图例块）。"""
    px, py = int(6.0*200), int(2.6*200)
    colors = ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"]   # H14 前四色（见上）
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    band = py // (len(colors) + 1)
    for i, c in enumerate(colors):
        d.rectangle([0, band*(i+1), px, band*(i+2)], fill=c)
    d.rectangle([40, 30, 90, 65], fill="#D55E00")      # 稀有彩（H14 第六色）：50×35 px，占比远低于 0.5%
    im.save(D/"ok-04.png", dpi=(200, 200))

fig_ok04()

# 追加（2026-09-27 复验时补，理由见 figure-style-baseline.txt §8）：
# 上面 6+1 张全是 PNG，而本设计的**载体是 TikZ ⇒ 主要产物格式是 PDF**。独立复验实测：
# 旧实现的 F2 无条件用 `Image.open`，一张 6.0×2.6 in 的 PDF 会 rc=1 / stdout 空 /
# `PIL.UnidentifiedImageError` ⇒ PDF 根本判不完。修完（F2 也吃 PDF：第 1 页栅格化）之后，
# 必须有一张**入库的 PDF 样本**来钉住这条分支，否则驱动器只能靠临时文件自证。
# 尺寸：页盒直接写点（w_in*72 pt）⇒ F1 精确等于 w_in/6.31，与 --dpi 无关。
def fig_pdf(name, w_in, h_in, colors):
    """按 72 pt = 1 in 出 PDF：色带布局与 fig() 同构（外加大片白底）。

    `no_new_id=1`：fitz 默认每次 save 都随机生成 trailer `/ID` ⇒ 同一个 fixture 每跑一次
    `make-fixtures.py` 就换一次 blob（fixtures 不再幂等，`git status` 会脏）。钉掉它。
    """
    doc = fitz.open()
    page = doc.new_page(width=w_in*72, height=h_in*72)
    for i, c in enumerate(colors):
        y0 = h_in*72*(i+1)/(len(colors)+1); y1 = h_in*72*(i+2)/(len(colors)+1)
        page.draw_rect(fitz.Rect(0, y0, w_in*72, y1), color=None,
                       fill=tuple(int(c[k:k+2], 16)/255 for k in (1, 3, 5)))
    doc.save(D/name, no_new_id=1); doc.close()

fig_pdf("ok-05.pdf", 6.0, 2.6, ["#E69F00", "#56B4E9", "#009E73", "#CC79A7"])   # 0.951，4 色（H14 前四色）
fig_pdf("bad-f2-five-colors.pdf", 6.0, 2.6,
        ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"])    # 0.951，6 色

# 追加（M3 Task 3）：F4 / F5 两条新判据各要一个"必须红"的样本 + F5 一条"必须仍绿"的边界对照。
# 三张统一 6.0×2.6 in @200 dpi ⇒ F1 = 6.0/6.31 = 0.951（PASS），与 ok-01 同尺寸。
def fig_bg_dark():
    """bad-bg-dark.png：纯 (18,18,18) 底（= 实测 MATLAB 深色底轴区像素）+ 一条彩色带。

    底色众数 = (18,18,18)、亮度 18 < BG_MIN_LUMA(136) ⇒ F4 红（`expected.tsv` 钉住）。
    """
    px, py = int(6.0*200), int(2.6*200)
    im = Image.new("RGB", (px, py), (18, 18, 18)); d = ImageDraw.Draw(im)
    d.rectangle([0, py//2, px, py//2 + py//5], fill="#4477AA")
    im.save(D/"bad-bg-dark.png", dpi=(200, 200))

fig_bg_dark()

def fig_color_order(name, colors):
    """白底 + 给定色带（F5 的样本/边界对照）。

    `bad-color-order.png`：本机**旧默认色序**三色（实测 out-G1/figure.png 的 #0c5da5/#00b945/#ff9500）
      ⇒ 精确比对下全部越界 ⇒ F5 红。
    `good-color-order.png`：H14 八色的**前三色** ⇒ 合法子集 ⇒ F5 **必须仍绿**（钉死 F5 非恒红）。
    """
    px, py = int(6.0*200), int(2.6*200)
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    band = py // (len(colors) + 1)
    for i, c in enumerate(colors):
        d.rectangle([0, band*(i+1), px, band*(i+2)], fill=c)
    im.save(D/name, dpi=(200, 200))

fig_color_order("bad-color-order.png", ["#0C5DA5", "#00B945", "#FF9500"])    # 非 H14 ⇒ F5 红
fig_color_order("good-color-order.png", ["#E69F00", "#56B4E9", "#009E73"])   # H14 前三色 ⇒ F5 必须仍绿

# 追加（M3 Task 3b 修 ③）：F6 的**第三态 `N/A`** 要有一个"只引用、没内嵌"的入库样本。
# 实测 Origin 的 34/34 个导出件 `/FontFile*` = 0，但本仓此前**没有**这一类 PDF 入库
# （`ok-05.pdf` 与两页探针 = 一个字体都没有；python 绿件 = 内嵌 Type3）⇒ 那个差异无人钉住。
# base14 的 `helv` 是"名字报得出来、字形不在文件里"的最小样本：实测 `get_page_fonts` 报
# `(6, 'n/a', 'Type1', 'Helvetica', 'helv', 'WinAnsiEncoding')`、整份 PDF 的 `/FontFile*` 计数 = 0。
# 图的其余各条与 `ok-*` 同档（6.0 in ⇒ F1 0.951 · H14 三色 ⇒ F5 PASS · 白底 ⇒ F4 PASS）
# ⇒ 判词里翻红的那一条只会是 F6。断言见变异 `M58`（该样本的 F6 由 `N/A` 转 `FAIL`）。
def fig_not_embedded(name, w_in, h_in, colors):
    """与 `fig_pdf()` 同构（72 pt = 1 in、`no_new_id=1`），但页面上写一行 **base14 `helv`** 文字。

    ★ 色带只占**页面上半**（每色 ~1/8 高）⇒ 白底是**明确的众数**（62.5%）。
      `fig_pdf()` 那种"白底恰 1/4、与三条色带并列"的布局下，众数由 ±1 像素的舍入决定
      ⇒ F4 会**靠平票的运气**过关（实测这一版不改布局时，众数落在 `#56B4E9` 上、亮度 157
      刚刚过线）。本样本只要它**干净地**只暴露 F6 那一条，故把白底做实。
    """
    doc = fitz.open()
    page = doc.new_page(width=w_in*72, height=h_in*72)
    n = len(colors)
    for i, c in enumerate(colors):
        y0 = h_in*72*0.5*(i+1)/(n+1); y1 = h_in*72*0.5*(i+2)/(n+1)
        page.draw_rect(fitz.Rect(0, y0, w_in*72, y1), color=None,
                       fill=tuple(int(c[k:k+2], 16)/255 for k in (1, 3, 5)))
    page.insert_text((24, h_in*72 - 18), "Figure 1: base14 helv, referenced not embedded",
                     fontname="helv", fontsize=12)
    doc.save(D/name, no_new_id=1); doc.close()

fig_not_embedded("font-not-embedded.pdf", 6.0, 2.6, ["#E69F00", "#56B4E9", "#009E73"])

# 追加（2026-10-01 · M3-style 的 F4 再修一轮）：F4 由「近灰众数」换成「外缘环 ∧ 近灰众数」的合取
# 口径后，两条新判据腿各要一个样本：① 外缘环这一路**必须能红**（深饱和底 + 有白色元素）；
# ② 合取口径**必须仍能救**「白底但彩色面积大」的那一类（F4 的"必须仍绿"支点，兼 `M54` 的支点）。
# 两件统一 6.0×2.6 in @200 dpi ⇒ F1 = 6.0/6.31 = 0.951（PASS），与 ok-01 同尺寸。
def fig_bg_navy():
    """bad-bg-navy.png：**整幅深藏青 (13,27,42)**（**饱和**：`max-min = 29 ≥ 24`）+ 一条极细白线。

    规格（冻结，不许随手改）：底 = `(13, 27, 42)`、白线 = 4×520 px 竖线（占全图 **0.33%**）。
    · **底必须饱和**（`max-min ≥ 24`）—— 这是本样本的**要害**：饱和底**不落进**「近灰」档，
      于是「近灰众数」这一路只取得到那条白线 ⇒ **单靠近灰众数会判 PASS（假绿）**。
    · 白线 = 「有白色元素」这个致命前提（`max-min` 极小、正是近灰那一路取的）。

    期望（`expected.tsv` 钉住）：**F4 = FAIL** —— 外缘环 = `(13,27,42)` 亮度 24 < 136 判红；
    近灰众数 = 那条白线的 255 ≥ 136（**正是它骗过了旧口径**）。两路合取 ⇒ 红。
    """
    px, py = int(6.0*200), int(2.6*200)
    im = Image.new("RGB", (px, py), (13, 27, 42)); d = ImageDraw.Draw(im)
    d.rectangle([px//2, 0, px//2 + 3, py], fill="white")     # 4×520 px = 0.33%（竖细白线；PIL 矩形含两端点）
    im.save(D/"bad-bg-navy.png", dpi=(200, 200))

fig_bg_navy()

def fig_ok06():
    """ok-06.png：**白底 + 一大片深饱和填充 `#0072B2`（亮度 87）占 ~69%**，四周留白边。

    ★ 它是 **`M54` 边界对照的支点**（M3-style-终审 I-1 的同型修正），必须满足三件事：
      ① **新口径下 PASS** —— 白边够宽，使 **1% 外缘环整圈落在白上**（不碰那片蓝）；近灰众数也 = 白。
      ② **「退回全图众数」的变异下 FAIL** —— 蓝片是全图**众数**（69%），其亮度 87 < 136。
      ③ 蓝 `#0072B2` ∈ H14 ⇒ **F5 不该被它打红**（本样本只暴露 F4 那一条）。

    几何（冻结）：1200×520、蓝片 = `[60, 60]–[1140, 460]`（1080×400 = **69.23%**）、
    四周白边 60 px（≫ 外缘环厚 5 px）⇒ 环 = 纯白。白线不碰边、蓝片也不碰边。
    """
    px, py = 1200, 520
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 1140, 460], fill="#0072B2")          # 1080×400 = 69.23%
    im.save(D/"ok-06.png", dpi=(200, 200))

fig_ok06()
