# -*- coding: utf-8 -*-
"""probe_origin_font.py — Origin 侧字体族侦察（任务书 §2.2）

铁律：每一条"设上了"的判断都**落在产物上**（导出 PDF 的字体读数），
不用 API 返回值 / run=OK 当证据。

进程纪律：try/finally: op.exit()，崩溃路径也要退实例。

用法: python tests/m3-origin-font-probe/probe_origin_font.py [--only STAGE]
产物: build/m3-origin-font/origin/
"""
import os
import sys
import json
import argparse
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


def dump_log(name):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LOG) + "\n")


def read_pdf(pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    gf = [(f[3], f[2], f[5]) for f in page.get_fonts()]   # (basefont, type, enc)
    spans = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                spans[s["font"]] = spans.get(s["font"], 0) + len(s["text"])
    txt = page.get_text().replace("\n", "|")
    doc.close()
    return {"get_fonts": gf, "spans": spans, "text": txt}


def snap(tag, pdf):
    r = read_pdf(pdf)
    P("### %s  [%s]" % (tag, os.path.basename(pdf)))
    P("    get_fonts:", json.dumps(r["get_fonts"], ensure_ascii=False))
    P("    spans    :", json.dumps(r["spans"], ensure_ascii=False))
    P("    text     :", r["text"][:200])
    return r


def exp(gp, name, width=1893):
    p = os.path.join(OUT, name)
    ok = gp.save_fig(p, width=width)
    return p, ok


def lt(cmd, tag=""):
    """跑一条 LabTalk，返回 execute 的布尔（**不作为生效证据**，只作为是否报错）"""
    r = op.lt_exec(cmd)
    P("  LT[%s] %-58s -> exec_ok=%s" % (tag, cmd[:58], r))
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="all")
    args = ap.parse_args()

    P("=== originpro 版本 ===")
    import originpro
    P("originpro:", getattr(originpro, "__file__", "?"))
    op.set_show(False)

    ctx = {}
    try:
        # ---------- 建数据与图 ----------
        wks = op.new_sheet()
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]
        wks.from_list(0, x)
        wks.from_list(1, y)
        gp = op.new_graph()          # 默认模板
        gl = gp[0]
        gl.add_plot(wks, 1, 0)
        gp.activate()
        P("=== 图已建 ===", "sheets/graphs:", op.graph_list())

        # ---------- B 基线 ----------
        p, ok = exp(gp, "b0_baseline.pdf")
        P("save_fig ok=", ok)
        base = snap("B0 基线（默认模板）", p)
        ctx["baseline"] = base

        # ---------- 结构 dump 尝试（§2.2.4） ----------
        P("\n=== 结构 introspection 尝试 ===")
        for name, cmd in [
            ("page_as_string", 'string __S$ = page;'),
            ("layer_as_string", 'string __S2$ = layer;'),
            ("label_list", 'label -l;'),
        ]:
            try:
                lt(cmd, name)
                v = op.get_lt_str("__S$" if name == "page_as_string" else "__S2$")
                P("   -> value len=%s head=%r" % (len(v or ""), (v or "")[:300]))
            except Exception as e:
                P("   -> EXC", repr(e))

        # 用 tree 转 xml 试试
        for tree_expr in ["page.tree", "layer.tree"]:
            try:
                lt("Tree __T; __T = %s;" % tree_expr, "tree:" + tree_expr)
                xs = op.get_lt_str("__S3$")
                lt('string __S3$ = __T;', "xml:" + tree_expr)
                xs = op.get_lt_str("__S3$")
                P("   -> %s xml len=%s head=%r" % (tree_expr, len(xs or ""), (xs or "")[:300]))
            except Exception as e:
                P("   -> EXC", repr(e))

        # ---------- C 主题 ----------
        P("\n=== C 主题路线 ===")
        lt('themeApply2g theme:="Times New Roman Font";', "theme")
        p, ok = exp(gp, "c1_theme_TNR.pdf")
        after = snap("C1 应用主题 Times New Roman Font 后", p)
        ctx["theme"] = after

        # 反证：应用一个明显不同的主题，确认主题系统**真的**在动
        lt('themeApply2g theme:="Night Sky";', "theme-neg")
        p, ok = exp(gp, "c2_theme_nightsky.pdf")
        neg = snap("C2 应用 Night Sky（反证：主题有没有在动）", p)
        ctx["neg"] = neg

        # ---------- D 直接点名（复现上轮 + 新候选） ----------
        P("\n=== D 直接点名候选 ===")
        cands = [
            ('xb.font$ = "Times New Roman";', "xb.font$"),
            ('yl.font$ = "Times New Roman";', "yl.font$"),
            ('legend.font$ = "Times New Roman";', "legend.font$"),
            ('page.font$ = "Times New Roman";', "page.font$"),
            ('layer.font$ = "Times New Roman";', "layer.font$"),
            ('sys.font$ = "Times New Roman";', "sys.font$"),
            ('xb.font = 2;', "xb.font=2"),
        ]
        for cmd, tag in cands:
            lt(cmd, tag)
        p, ok = exp(gp, "d1_named.pdf")
        named = snap("D1 点名之后", p)
        ctx["named"] = named

        # ---------- E 中文 ----------
        P("\n=== E 中文文本 ===")
        lt('xb.text$ = "温度 (°C)";', "cjk-text")
        lt('yl.text$ = "Wavelength (nm)";', "latin-text")
        p, ok = exp(gp, "e1_cjk.pdf")
        cjk = snap("E1 中文轴标题", p)
        ctx["cjk"] = cjk

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
        dump_log("probe_origin_font.log")
        with open(os.path.join(OUT, "probe_origin_font.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
