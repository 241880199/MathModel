# -*- coding: utf-8 -*-
"""probe_origin_font6.py — 第六轮：expGraph 的 theme:= 能不能覆盖"后加的文本对象"

第五轮发现：`themeApply2g` 只影响**应用那一刻已存在**的对象，后建的文本对象回到 SimSun。
第六轮问：`expGraph ... theme:=` 是**导出那一刻**施加，是否覆盖页面上的全部对象（含后加注释）？

用法: python tests/m3-origin-font-probe/probe_origin_font6.py
"""
import os
import sys
import json
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = os.path.join(REPO, "build", "m3-origin-probe", "site")
OUT = os.path.join(REPO, "build", "m3-origin-font", "origin")
sys.path.insert(0, SITE)
import originpro as op          # noqa: E402
import fitz                     # noqa: E402

LOG = []
OP = OUT.replace("\\", "/")


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def dump(tag, pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    per = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if not t:
                    continue
                per.setdefault(s["font"], []).append(t)
    gf = [(f[3], f[1]) for f in page.get_fonts()]
    doc.close()
    P("### %s  [%s]" % (tag, os.path.basename(pdf)))
    P("    fonts:", json.dumps(gf, ensure_ascii=False))
    for f, ts in per.items():
        P("    span font %-22s n=%d  sample=%s" % (f, len(ts), json.dumps("".join(ts[:14]), ensure_ascii=False)))
    return {"fonts": gf, "per_font": {k: "".join(v) for k, v in per.items()}}


def main():
    op.set_show(False)
    ctx = {}
    try:
        wks = op.new_sheet()
        wks.from_list(0, [0, 1, 2, 3, 4, 5])
        wks.from_list(1, [0, 1, 4, 9, 16, 25])
        gp = op.new_graph()
        gp[0].add_plot(wks, 1, 0)
        gp.activate()

        # 先加注释（此时默认 SimSun）
        op.lt_exec('label -a 3 5 -s "R2 = 0.99";')
        op.lt_exec('xb.text$ = "Wavelength (nm)";')
        op.lt_exec('yl.text$ = "Intensity (a.u.)";')
        P("  已加注释（未应用任何主题）")

        p0 = "%s/k0_plain.pdf" % OP
        gp.save_fig(p0, width=1893)
        ctx["k0"] = dump("K0 不加主题（含注释）", p0)

        p1 = "%s/k1_export_theme.pdf" % OP
        op.lt_exec('expGraph type:=pdf path:="%s" filename:="k1_export_theme.pdf" '
                   'overwrite:=replace tr1.Unit:=2 tr1.Width:=1893 '
                   'theme:="Times New Roman Font";' % OP)
        if os.path.exists(p1):
            ctx["k1"] = dump("K1 expGraph + theme:=（含注释）", p1)

        # 反证：先 themeApply2g 再加注释（第五轮已知会有 SimSun 残留）
        gp2 = op.new_graph()
        w = op.new_sheet()
        w.from_list(0, [0, 1, 2, 3, 4, 5])
        w.from_list(1, [0, 1, 4, 9, 16, 25])
        gp2[0].add_plot(w, 1, 0)
        gp2.activate()
        op.lt_exec('themeApply2g theme:="Times New Roman Font";')
        op.lt_exec('label -a 3 5 -s "R2 = 0.99";')
        p2 = "%s/k2_theme_then_label.pdf" % OP
        gp2.save_fig(p2, width=1893)
        ctx["k2"] = dump("K2 先 themeApply2g 再加注释（反证）", p2)

    except Exception:
        P("!!! EXCEPTION !!!")
        P(traceback.format_exc())
    finally:
        try:
            op.exit()
        except Exception as e:
            P("op.exit EXC:", repr(e))
        with open(os.path.join(OUT, "probe_origin_font6.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font6.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
