#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_3_controls.py —— ★ T8：**自己造**正/负控制页，证明探针认得正样本、不误报负样本。

没有这个控制，probe_2 的任何读数**一律降级为"自报"**。

做法：用 fitz **现画** 12 页已知样本（每页一个 PDF），
跑 tableprobe.analyze_page()，把"实测"与"期望"逐条比对，打印 PASS/FAIL。

样本（**不声称穷尽**，只覆盖本侦察里踩过的坑）：
  正：P1 三线表 · P2 四线表 · P3 全网格(竖线逐行画) · P8 表头填充色带
  负：N1 纯文本无表 · N2 页眉/页脚规则线 · N5 图框+Figure 表题 · N6 扫描位图页
  拆组：N3 两表夹正文 · N4 两表夹表题
  干扰：N7 整页水印 + 一张三线表
"""
import os
import fitz

import tableprobe as tp

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "build", "m3-table-recon", "controls")

W, H = 612.0, 792.0
BL, BR = 72.0, 540.0          # 版心左右
BW = BR - BL                  # 468


def _page():
    doc = fitz.open()
    p = doc.new_page(width=W, height=H)
    return doc, p


def _txt(p, x, y, s, size=11, **kw):
    p.insert_text((x, y), s, fontsize=size, fontname="helv", **kw)


def _hrule(p, y, x0=BL, x1=BR, w=0.8):
    p.draw_line(fitz.Point(x0, y), fitz.Point(x1, y), color=(0, 0, 0), width=w)


def _vrule(p, x, y0, y1, w=0.8):
    p.draw_line(fitz.Point(x, y0), fitz.Point(x, y1), color=(0, 0, 0), width=w)


# ---------------- 正样本 ----------------
def build_P1():
    """标准三线表：顶线/表头线/底线 + Table 1 表题在上方。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 1: Demo")
    _txt(p, 90, 115, "Name"); _txt(p, 300, 115, "Value")
    _hrule(p, 120); _hrule(p, 136)
    for i, (a, b) in enumerate([("alpha", "1.0"), ("beta", "2.0"), ("gamma", "3.5")]):
        _txt(p, 90, 152 + 16 * i, a); _txt(p, 300, 152 + 16 * i, b)
    _hrule(p, 202)
    return doc


def build_P2():
    """四线表：表头两行 => 4 条横线。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 2: Demo")
    _txt(p, 90, 115, "A"); _txt(p, 300, 115, "B")
    _hrule(p, 120); _hrule(p, 136); _hrule(p, 152)
    _txt(p, 90, 170, "x"); _txt(p, 300, 170, "1")
    _hrule(p, 190)
    return doc


def build_P3():
    """全网格：横线 + 竖线（**竖线按行逐段画**，专测合并）。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 3: Grid")
    ys = [120, 140, 160, 180, 200]
    for y in ys:
        _hrule(p, y)
    for y0, y1 in zip(ys, ys[1:]):
        _vrule(p, 200, y0, y1); _vrule(p, 350, y0, y1)   # 逐行小段
        _vrule(p, BL, y0, y1); _vrule(p, BR, y0, y1)
    return doc


def build_P8():
    """表头填充色带（无描边）+ 3 条横线、无竖线 ⇒ 不应因色带被判"有竖线"。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 8: Filled header")
    _hrule(p, 120)                                     # 顶线
    p.draw_rect(fitz.Rect(BL, 120.5, BR, 137.5), color=None, fill=(0.15, 0.3, 0.6))
    _txt(p, 90, 133, "Col A", color=(1, 1, 1)); _txt(p, 300, 133, "Col B", color=(1, 1, 1))
    _hrule(p, 138)                                     # 表头下线
    _txt(p, 90, 155, "1"); _txt(p, 300, 155, "2")
    _hrule(p, 170)                                     # 底线
    return doc


# ---------------- 负样本 ----------------
def build_N1():
    """纯文本页：没有任何线。"""
    doc, p = _page()
    for i in range(20):
        _txt(p, BL, 100 + 18 * i, "Lorem ipsum dolor sit amet, consectetur adipiscing elit sed do.")
    return doc


def build_N2():
    """纯文本页 + 页眉规则线 + 页脚规则线（长线但非表）。"""
    doc, p = _page()
    _hrule(p, 50)          # 页眉带内
    _hrule(p, 750)         # 页脚带内
    for i in range(18):
        _txt(p, BL, 100 + 18 * i, "Body text line that is long enough to look like a paragraph.")
    return doc


def build_N2b():
    """三条长横线但**左右端都不对齐** ⇒ 不成组、不成表。"""
    doc, p = _page()
    _hrule(p, 120, BL, BR)
    _hrule(p, 300, BL, BR - 120)
    _hrule(p, 480, BL + 60, BR)
    _txt(p, BL, 150, "Some text between the rules.")
    return doc


# ---------------- 拆组 ----------------
def build_N3():
    """两张同宽三线表，中间隔**一段正文**。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 1: one")
    _hrule(p, 100); _hrule(p, 116); _hrule(p, 160)
    for i in range(3):
        _txt(p, BL, 200 + 16 * i,
             "Between the two tables there is a real paragraph of running text here.")
    _hrule(p, 280); _hrule(p, 296); _hrule(p, 340)
    return doc


def build_N4():
    """两张同宽三线表，中间**只隔一条表题**。"""
    doc, p = _page()
    _txt(p, 250, 90, "Table 1: one")
    _hrule(p, 100); _hrule(p, 116); _hrule(p, 160)
    _txt(p, 250, 200, "Table 2: two")          # 居中表题，非正文
    _hrule(p, 230); _hrule(p, 246); _hrule(p, 290)
    return doc


def build_N5():
    """图框：矩形框 + 网格线 + 刻度小段 + **Figure 1** 表题 ⇒ 应判为图。"""
    doc, p = _page()
    rect = fitz.Rect(120, 120, 480, 360)
    p.draw_rect(rect, color=(0, 0, 0), width=0.8)
    for i in range(1, 6):
        y = rect.y0 + (rect.height / 6) * i
        _hrule(p, y, rect.x0, rect.x1, w=0.4)
    for i in range(1, 8):
        x = rect.x0 + (rect.width / 8) * i
        _vrule(p, x, rect.y0, rect.y1, w=0.4)
    for i in range(40):                        # 一堆刻度/散点小段
        _hrule(p, 200 + (i % 8) * 3, 150 + i * 7, 152 + i * 7, w=0.5)
    _txt(p, 220, 390, "Figure 1: a plot")
    return doc


def build_N6():
    """扫描页：只贴一张位图，无文本层、无矢量。"""
    doc, p = _page()
    src = fitz.open()
    sp = src.new_page(width=W, height=H)
    sp.draw_rect(fitz.Rect(100, 100, 500, 700), color=(0, 0, 0), fill=(0.9, 0.9, 0.9))
    pm = sp.get_pixmap(dpi=72)
    p.insert_image(fitz.Rect(0, 0, W, H), pixmap=pm)
    return doc


def build_N7():
    """整页斜置水印文本 + 一张正常三线表 ⇒ 仍应只判 1 张表。"""
    doc, p = _page()
    _txt(p, 300, 780, "CONFIDENTIAL-WATERMARK", size=36, rotate=90)
    _txt(p, 250, 90, "Table 1: with watermark")
    _hrule(p, 100); _hrule(p, 116); _hrule(p, 160)
    _txt(p, 90, 130, "a"); _txt(p, 300, 130, "b")
    return doc


CASES = [
    # 名字, 构造器, 期望(dict) —— 期望键: ntables / max_n / vert_any / cap_any / kind_fig
    ("P1_三线表",        build_P1,  {"ntables": 1, "n3": True, "vert": False, "cap": "above"}),
    ("P2_四线表",        build_P2,  {"ntables": 1, "maxn": 4}),
    ("P3_全网格(逐行竖线)", build_P3, {"ntables": 1, "vert": True}),
    ("P8_表头填充色带",   build_P8,  {"ntables": 1, "vert": False}),
    ("N1_纯文本无表",     build_N1,  {"ntables": 0}),
    ("N2_页眉页脚线",     build_N2,  {"ntables": 0}),
    ("N2b_三线不对齐",    build_N2b, {"ntables": 0}),
    ("N3_两表夹正文",     build_N3,  {"ntables": 2}),
    ("N4_两表夹表题",     build_N4,  {"ntables": 2}),
    ("N5_图框+Figure题",  build_N5,  {"ntables": 0, "cand_fig": True}),
    ("N6_扫描位图页",     build_N6,  {"ntables": 0}),
    ("N7_水印+一表",      build_N7,  {"ntables": 1}),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    print("### probe_3_controls —— T8 正/负控制（自造样本）")
    print("# 页面 %.0fx%.0f 版心 %.0f..%.0f（宽 %.0f，长线阈值 %.0fpt）"
          % (W, H, BL, BR, BW, BW * tp.MIN_RULE_LEN_FRAC))
    print()
    npass = nfail = 0
    rows = []
    for name, builder, exp in CASES:
        doc = builder()
        path = os.path.join(OUT, name + ".pdf")
        doc.save(path)
        p = doc[0]
        res = tp.analyze_page(p)
        cands = res["tables"]                                   # 含 figure
        kept = [t for t in cands if t["kind"] == "table"]
        got = {
            "ntables": len(kept),
            "ncand": len(cands),
            "maxn": max([t["n"] for t in kept], default=0),
            "vert": any(t["vert"] for t in kept),
            "cap": kept[0]["cap"] if kept else "-",
            "cand_fig": any(t["kind"] == "figure" for t in cands),
        }
        checks = []
        if "ntables" in exp:
            checks.append(("ntables=%d" % exp["ntables"], got["ntables"] == exp["ntables"], got["ntables"]))
        if exp.get("n3"):
            checks.append(("n==3", got["maxn"] == 3, got["maxn"]))
        if "maxn" in exp:
            checks.append(("n==%d" % exp["maxn"], got["maxn"] == exp["maxn"], got["maxn"]))
        if "vert" in exp:
            checks.append(("vert=%s" % exp["vert"], got["vert"] == exp["vert"], got["vert"]))
        if "cap" in exp:
            checks.append(("cap=%s" % exp["cap"], got["cap"] == exp["cap"], got["cap"]))
        if exp.get("cand_fig"):
            checks.append(("候选判为图", got["cand_fig"] is True, got["cand_fig"]))
        ok = all(c[1] for c in checks)
        npass += ok
        nfail += (not ok)
        rows.append((name, ok, checks, got))
        print("%-22s %s   cand=%d kept=%d  %s" %
              (name, "PASS" if ok else "FAIL", got["ncand"], got["ntables"],
               " ".join("%s:%s%s" % (c[0], c[2], "" if c[1] else " <-- 不符") for c in checks)))
        print("        → 生成 %s" % os.path.relpath(path, REPO).replace("\\", "/"))
    print()
    print("### 汇总：PASS %d / FAIL %d（共 %d）" % (npass, nfail, len(CASES)))
    print("★ 若有一条 FAIL，probe_2 的对应读数就要打折，**不许当没看见**。")


if __name__ == "__main__":
    main()
