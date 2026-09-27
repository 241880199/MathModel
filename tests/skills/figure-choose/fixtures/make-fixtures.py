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
fig("ok-01.png", 6.0, 2.6, ["#4477AA", "#EE6677", "#228833"])
fig("ok-02.png", 5.1, 2.6, ["#4477AA"])                       # 0.808，单色
fig("ok-03.png", 6.3, 3.0, ["#4477AA", "#EE6677", "#228833", "#CCBB44"])  # 0.999，4 色
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
    colors = ["#4477AA", "#EE6677", "#228833", "#CCBB44"]
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    band = py // (len(colors) + 1)
    for i, c in enumerate(colors):
        d.rectangle([0, band*(i+1), px, band*(i+2)], fill=c)
    d.rectangle([40, 30, 90, 65], fill="#AA3377")      # 稀有彩：50×35 px，占比远低于 0.5%
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

fig_pdf("ok-05.pdf", 6.0, 2.6, ["#4477AA", "#EE6677", "#228833", "#CCBB44"])   # 0.951，4 色
fig_pdf("bad-f2-five-colors.pdf", 6.0, 2.6,
        ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"])    # 0.951，6 色
