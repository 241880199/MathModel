# -*- coding: utf-8 -*-
"""probe_origin_font2.py — 第二轮：因果对照 + 最小命令 + 中文 + 主题是否覆盖后改文本

第一轮只证明了"应用主题后内嵌字体变了"，但**缺反证**（主题系统是不是真的在动、
假主题名会不会静默失败、是不是全局开关）。这一轮补上：

  G1: 新图 -> 基线(期望 SimSun)
      -> 只用 xb.font$="Times New Roman"  (复现上轮"点名无效")
      -> 导出
  G2: 新图(期望 SimSun)
      -> 假主题名(期望：静默失败，仍 SimSun)
      -> 真主题名(期望：TimesNewRomanPSMT)
  G3: 新图 -> 读 font 索引 -> 应用主题 -> 再读索引 (值名承重：主题到底把索引设成了几)
      -> 用那个索引直接赋值(不用主题) -> 导出
  G4: 应用主题后 -> 再改轴标题文本(拉丁) -> 导出(主题覆盖不覆盖后改的文本)
      -> 再改成中文 -> 导出(中文字形有没有)

用法: python tests/m3-origin-font-probe/probe_origin_font2.py
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
    P("    text     :", txt[:200])
    return {"get_fonts": gf, "spans": spans, "text": txt}


def new_graph(name):
    wks = op.new_sheet()
    wks.from_list(0, [0, 1, 2, 3, 4, 5])
    wks.from_list(1, [0, 1, 4, 9, 16, 25])
    gp = op.new_graph()
    gp[0].add_plot(wks, 1, 0)
    gp.activate()
    P("--- 建图: %s (%s)" % (name, gp.lt_range()))
    return gp


def exp(gp, name, width=1893):
    p = os.path.join(OUT, name)
    gp.save_fig(p, width=width)
    return p


def lt(cmd):
    r = op.lt_exec(cmd)
    P("  LT %-52s -> exec_ok=%s" % (cmd[:52], r))
    return r


def idx(expr):
    """读一个 LabTalk 数值属性（字体索引）"""
    try:
        v = op.lt_float(expr)
    except Exception as e:
        v = "ERR:%s" % e
    return v


def main():
    op.set_show(False)
    ctx = {}
    try:
        # ================= G1 =================
        P("\n========== G1: 基线 + 点名 xb.font$ ==========")
        g1 = new_graph("G1")
        ctx["g1_font_before"] = idx("xb.font")
        P("  G1 xb.font (默认) =", ctx["g1_font_before"])
        p = exp(g1, "g1_a_baseline.pdf")
        ctx["g1_base"] = snap("G1-a 基线", p)

        lt('xb.font$ = "Times New Roman";')
        ctx["g1_font_after"] = idx("xb.font")
        P("  G1 xb.font (点名后) =", ctx["g1_font_after"])
        p = exp(g1, "g1_b_named.pdf")
        ctx["g1_named"] = snap("G1-b 只点名 xb.font$ 之后", p)

        # ================= G2 =================
        P("\n========== G2: 假主题名 vs 真主题名 ==========")
        g2 = new_graph("G2")
        p = exp(g2, "g2_a_baseline.pdf")
        ctx["g2_base"] = snap("G2-a 基线", p)

        lt('themeApply2g theme:="NoSuchThemeXYZ12345";')
        p = exp(g2, "g2_b_bogus_theme.pdf")
        ctx["g2_bogus"] = snap("G2-b 假主题名之后", p)

        lt('themeApply2g theme:="Times New Roman Font";')
        p = exp(g2, "g2_c_real_theme.pdf")
        ctx["g2_real"] = snap("G2-c 真主题名之后", p)

        # ================= G3: 值名承重 =================
        P("\n========== G3: 主题把索引设成了几（值名承重） ==========")
        g3 = new_graph("G3")
        before = {"xb.font": idx("xb.font"), "yl.font": idx("yl.font"),
                  "x1.font": idx("x1.font"), "y1.font": idx("y1.font")}
        P("  G3 主题前索引:", json.dumps(before))
        lt('themeApply2g theme:="Times New Roman Font";')
        after = {"xb.font": idx("xb.font"), "yl.font": idx("yl.font"),
                 "x1.font": idx("x1.font"), "y1.font": idx("y1.font")}
        P("  G3 主题后索引:", json.dumps(after))
        ctx["g3_idx_before"], ctx["g3_idx_after"] = before, after

        # ================= G4: 主题后改文本 =================
        P("\n========== G4: 主题之后再改文本 ==========")
        g4 = new_graph("G4")
        lt('themeApply2g theme:="Times New Roman Font";')
        lt('xb.text$ = "Wavelength (nm)";')
        lt('yl.text$ = "Intensity (a.u.)";')
        p = exp(g4, "g4_a_latin_text.pdf")
        ctx["g4_latin"] = snap("G4-a 主题后写拉丁轴标题", p)

        lt('xb.text$ = "温度 (°C)";')
        p = exp(g4, "g4_b_cjk_text.pdf")
        ctx["g4_cjk"] = snap("G4-b 主题后写中文轴标题", p)

        # 主题后 font 索引有没有被文本操作改回
        P("  G4 改文本后 xb.font =", idx("xb.font"))

        # ================= G5: 用索引直接赋值（不用主题） =================
        P("\n========== G5: 用索引 N 直接赋值，不经主题 ==========")
        N = after.get("xb.font")
        g5 = new_graph("G5")
        for obj in ["xb", "yl", "x1", "y1"]:
            lt("%s.font = %s;" % (obj, N))
        p = exp(g5, "g5_by_index.pdf")
        ctx["g5_by_index"] = snap("G5 用索引 %s 直接赋值" % N, p)
        ctx["g5_N"] = N

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
        with open(os.path.join(OUT, "probe_origin_font2.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font2.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
