# -*- coding: utf-8 -*-
"""probe_origin_font5.py — 第五轮：export 期 theme 参数 + 主题后新建文本对象

发现 `expGraph` 有一个 `theme` 参数（OXF 原文：Graph theme which is used to applied
on the exported pages）⇒ 也许**不用改页面**，在导出那一刻换字体。

  G9 : 新图 -> 记 xb.font -> `expGraph ... theme:="Times New Roman Font"` -> 读数
       -> 再记 xb.font（页面有没有被动过）-> 不带 theme 再导一次（是不是每次导出独立）
  G10: 应用主题 -> 新建文本对象 -> 读数（新对象继承 Times 还是回到 SimSun）

用法: python tests/m3-origin-font-probe/probe_origin_font5.py
"""
import os
import sys
import json
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = os.path.join(REPO, "build", "m3-origin-probe", "site")
OUT = os.path.join(REPO, "build", "m3-origin-font", "origin")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, SITE)
import originpro as op          # noqa: E402
import fitz                     # noqa: E402

LOG = []
OP = OUT.replace("\\", "/")


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def snap(tag, pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    gf = [(f[3], f[1]) for f in page.get_fonts()]      # basefont, ext
    txt = page.get_text().replace("\n", "|")
    doc.close()
    P("### %s  [%s]" % (tag, os.path.basename(pdf)))
    P("    (basefont, ext):", json.dumps(gf, ensure_ascii=False))
    P("    text:", json.dumps(txt[:200], ensure_ascii=False))
    return {"fonts": gf, "text": txt}


def lt(cmd):
    r = op.lt_exec(cmd)
    P("  LT %-64s -> exec_ok=%s" % (cmd[:64], r))
    return r


def new_graph():
    wks = op.new_sheet()
    wks.from_list(0, [0, 1, 2, 3, 4, 5])
    wks.from_list(1, [0, 1, 4, 9, 16, 25])
    gp = op.new_graph()
    gp[0].add_plot(wks, 1, 0)
    gp.activate()
    return gp


def num(expr):
    try:
        return op.lt_float(expr)
    except Exception:
        return "ERR"


def main():
    op.set_show(False)
    ctx = {}
    try:
        # ---------------- G9 ----------------
        P("\n========== G9: expGraph 的 theme 参数（导出期换字，不动页面） ==========")
        g9 = new_graph()
        P("  G9 xb.font (导出前) =", num("xb.font"))

        p = "%s/j1_export_theme.pdf" % OP
        lt('expGraph type:=pdf path:="%s" filename:="j1_export_theme.pdf" '
           'overwrite:=replace tr1.Unit:=2 tr1.Width:=1893 '
           'theme:="Times New Roman Font";' % OP)
        if os.path.exists(p):
            ctx["j1"] = snap("J1 expGraph + theme:=（导出期）", p)
        else:
            P("  !! j1 没产出")

        P("  G9 xb.font (导出后) =", num("xb.font"), "  <- 页面有没有被动过")

        # 不带 theme 再导一次
        lt('expGraph type:=pdf path:="%s" filename:="j2_no_theme.pdf" '
           'overwrite:=replace tr1.Unit:=2 tr1.Width:=1893;' % OP)
        p2 = "%s/j2_no_theme.pdf" % OP
        if os.path.exists(p2):
            ctx["j2"] = snap("J2 expGraph 不带 theme（同一张图）", p2)

        # 假主题名
        lt('expGraph type:=pdf path:="%s" filename:="j3_bogus_theme.pdf" '
           'overwrite:=replace tr1.Unit:=2 tr1.Width:=1893 theme:="NoSuchThemeXYZ";' % OP)
        p3 = "%s/j3_bogus_theme.pdf" % OP
        if os.path.exists(p3):
            ctx["j3"] = snap("J3 expGraph + 假主题名", p3)

        # ---------------- G10 ----------------
        P("\n========== G10: 应用主题后新建文本对象 ==========")
        g10 = new_graph()
        lt('themeApply2g theme:="Times New Roman Font";')
        for form in ['label -a 3 5 -s "R2 = 0.99";',
                     'label -s "R2 = 0.99";',
                     'label -mg -s -sa -dc 3 5 "R2 = 0.99";']:
            lt(form)
        p4 = "%s/j4_new_text.pdf" % OP
        g10.save_fig(p4, width=1893)
        ctx["j4"] = snap("J4 主题后新建文本对象", p4)

    except Exception:
        P("!!! EXCEPTION !!!")
        P(traceback.format_exc())
    finally:
        P("\n=== op.exit() ===")
        try:
            op.exit()
            P("op.exit() 返回")
        except Exception as e:
            P("op.exit() 抛异常:", repr(e))
        with open(os.path.join(OUT, "probe_origin_font5.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font5.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
