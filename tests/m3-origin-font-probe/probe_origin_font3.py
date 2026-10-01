# -*- coding: utf-8 -*-
"""probe_origin_font3.py — 第三轮：主题到底动了哪些属性？能不能不用主题复现？

第一轮只证明了"应用主题后内嵌字体变了"，但**缺反证**（主题系统是不是真的在动、
假主题名会不会静默失败、是不是全局开关）。这一轮补上。

  G6: 新图 -> 读一批候选字体索引 -> 应用主题 -> 再读 (差集 = 主题动了谁)
  G7: 新图 -> 只设 G6 差集里的属性 -> 导出 -> 与"直接应用主题"的产物比对
  G8: 单点验证 layer.x.label.font 等（逐条）

用法: python tests/m3-origin-font-probe/probe_origin_font3.py
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


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def read_pdf(pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    gf = [(f[3], f[2]) for f in page.get_fonts()]
    spans = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                spans[s["font"]] = spans.get(s["font"], 0) + len(s["text"])
    txt = page.get_text().replace("\n", "|")
    doc.close()
    return gf, spans, txt


def snap(tag, pdf):
    gf, spans, txt = read_pdf(pdf)
    P("### %s  [%s]" % (tag, os.path.basename(pdf)))
    P("    get_fonts:", json.dumps(gf, ensure_ascii=False))
    P("    spans    :", json.dumps(spans, ensure_ascii=False))
    return {"get_fonts": gf, "spans": spans, "text": txt}


def new_graph(name):
    wks = op.new_sheet()
    wks.from_list(0, [0, 1, 2, 3, 4, 5])
    wks.from_list(1, [0, 1, 4, 9, 16, 25])
    gp = op.new_graph()
    gp[0].add_plot(wks, 1, 0)
    gp.activate()
    return gp


def exp(gp, name, width=1893):
    p = os.path.join(OUT, name)
    gp.save_fig(p, width=width)
    return p


def lt(cmd):
    r = op.lt_exec(cmd)
    P("  LT %-50s -> exec_ok=%s" % (cmd[:50], r))
    return r


def num(expr):
    try:
        import math
        v = op.lt_float(expr)
        if v is None:
            return None
        if isinstance(v, float) and math.isnan(v):
            return "NaN"
        return v
    except Exception as e:
        return "ERR"


PROPS = [
    "xb.font", "yl.font", "yr.font", "xt.font",
    "layer.x.label.font", "layer.y.label.font",
    "layer.x.font", "layer.y.font",
    "layer.font", "page.font",
    "legend.font", "legend.text.font",
]


def battery(tag):
    d = {}
    for p in PROPS:
        d[p] = num(p)
    P("  [%s] %s" % (tag, json.dumps(d, ensure_ascii=False)))
    return d


def main():
    op.set_show(False)
    ctx = {}
    try:
        # ---------- G6 差集 ----------
        P("\n========== G6: 主题动了哪些字体索引 ==========")
        g6 = new_graph("G6")
        before = battery("主题前")
        lt('themeApply2g theme:="Times New Roman Font";')
        after = battery("主题后")
        changed = {k: (before[k], after[k]) for k in before
                   if before[k] != after[k] and before[k] != "NaN"}
        P("  ==> 变化的: ", json.dumps(changed, ensure_ascii=False))
        ctx["g6_before"], ctx["g6_after"], ctx["g6_changed"] = before, after, changed
        p = exp(g6, "g6_theme.pdf")
        ctx["g6_theme"] = snap("G6 应用主题（参照物）", p)

        # ---------- G7 用变化项复现 ----------
        P("\n========== G7: 不用主题，只设变化项 ==========")
        g7 = new_graph("G7")
        for prop, (b, a) in changed.items():
            # 只设真正能写的文本对象属性
            lt("%s = %s;" % (prop, a))
        p = exp(g7, "g7_by_props.pdf")
        ctx["g7_props"] = snap("G7 只设变化项", p)

        # ---------- G8 逐条单点 ----------
        P("\n========== G8: 逐条单点（每个属性单独一张图） ==========")
        for i, prop in enumerate(["layer.x.label.font", "layer.y.label.font",
                                  "xb.font", "yl.font", "legend.font"]):
            g = new_graph("G8_%d" % i)
            lt("%s = 338;" % prop)
            p = exp(g, "g8_%d_%s.pdf" % (i, prop.replace(".", "_")))
            ctx["g8_" + prop] = snap("G8 %s=338" % prop, p)

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
        with open(os.path.join(OUT, "probe_origin_font3.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font3.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
