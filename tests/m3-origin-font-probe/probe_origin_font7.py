# -*- coding: utf-8 -*-
"""probe_origin_font7.py — 第七轮：用户级 OPDF.INI 到底**有没有被读**？

第 4/4b 轮把 `[Fonts] Embed` 改成 1/2 都没效果。两种解释：
  (a) 整个 OPDF.INI 都被忽略（Origin 读的是安装目录那份）；
  (b) 只有 [Fonts] 那几个键不被 expgraph 采用。
区分办法：改一个**与字体无关、效果刺眼**的键 —— `Color Translation=3`（灰度），
画一张**红色**折线，看导出的 PDF 里的线是不是变灰。

判定：渲染 PDF → 数"红像素"。红的多 ⇒ INI 没被读（或该键无效）。

★ 纪律：只临时改用户 OPDF.INI，跑完**按字节还原**并核对 sha256。

用法: python tests/m3-origin-font-probe/probe_origin_font7.py
"""
import os
import sys
import json
import hashlib
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = os.path.join(REPO, "build", "m3-origin-probe", "site")
OUT = os.path.join(REPO, "build", "m3-origin-font", "origin")
INI = r"D:\Shameless\Documents\OriginLab\User Files\OPDF.INI"
BAK = os.path.join(OUT, "OPDF.INI.orig.bak")

sys.path.insert(0, SITE)
import originpro as op          # noqa: E402
import fitz                     # noqa: E402
from PIL import Image           # noqa: E402
import numpy as np              # noqa: E402

LOG = []


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def set_ini_color(n):
    with open(BAK, "rb") as fh:
        txt = fh.read().decode("utf-8", "surrogateescape")
    out = []
    for ln in txt.split("\n"):
        if ln.strip().lower().startswith("color translation="):
            ln = "Color Translation=%d" % n
        out.append(ln)
    with open(INI, "w", encoding="utf-8", newline="", errors="surrogateescape") as fh:
        fh.write("\n".join(out))


def redness(pdf, png):
    doc = fitz.open(pdf)
    doc[0].get_pixmap(matrix=fitz.Matrix(2.0, 2.0)).save(png)
    doc.close()
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = int(((r > 120) & (r - g > 60) & (r - b > 60)).sum())
    return red


def main():
    orig = open(BAK, "rb").read()
    orig_sha = hashlib.sha256(orig).hexdigest()
    op.set_show(False)
    try:
        set_ini_color(3)
        P("=== 用户 OPDF.INI 已设 Color Translation=3（灰度），新起的 Origin 进程 ===")
        wks = op.new_sheet()
        wks.from_list(0, [0, 1, 2, 3, 4, 5])
        wks.from_list(1, [0, 1, 4, 9, 16, 25])
        gp = op.new_graph()
        gl = gp[0]
        p = gl.add_plot(wks, 1, 0)
        gl.activate()
        p.color = "#e41a1c"          # 上一轮已实测：hex 逐色精确命中
        op.lt_exec('layer.plot1.line.width = 3;')
        pdf = os.path.join(OUT, "m1_gray_test.pdf")
        gp.save_fig(pdf, width=1893)
        red = redness(pdf, os.path.join(OUT, "m1_gray_test.png"))
        P("Color Translation=3 下，红色像素数 =", red)
    except Exception:
        P("EXC:", traceback.format_exc())
        red = None
    finally:
        try:
            op.exit()
        except Exception as e:
            P("op.exit EXC:", repr(e))
        with open(INI, "wb") as fh:
            fh.write(orig)
        ok = hashlib.sha256(open(INI, "rb").read()).hexdigest() == orig_sha
        P("OPDF.INI 还原逐字节一致:", ok)

        # 对照组：正常 INI（Color Translation=0）下的红像素
        op.set_show(False)
        try:
            wks = op.new_sheet()
            wks.from_list(0, [0, 1, 2, 3, 4, 5])
            wks.from_list(1, [0, 1, 4, 9, 16, 25])
            gp = op.new_graph()
            gl = gp[0]
            p2 = gl.add_plot(wks, 1, 0)
            gl.activate()
            p2.color = "#e41a1c"
            op.lt_exec('layer.plot1.line.width = 3;')
            pdf2 = os.path.join(OUT, "m2_color_control.pdf")
            gp.save_fig(pdf2, width=1893)
            red2 = redness(pdf2, os.path.join(OUT, "m2_color_control.png"))
            P("Color Translation=0（对照）下，红色像素数 =", red2)
        except Exception:
            P("EXC2:", traceback.format_exc())
            red2 = None
        finally:
            try:
                op.exit()
            except Exception:
                pass
        with open(os.path.join(OUT, "probe_origin_font7.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font7.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump({"red_gray_ini": red, "red_control": red2,
                       "ini_restored": ok}, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
