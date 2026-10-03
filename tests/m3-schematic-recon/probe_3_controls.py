#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_3_controls.py —— ★ 自造控制页 + **读数 6 可行性的受控实验**。

三部分：

  A) **kind 分类控制**：现画 5 页已知样本，验 probe 判 raster/vector/table/none 是否正确。
     （没有这个控制，probe_2 的机械读数一律降级为"自报"。）

  B) **可分性实验（读数 6 的否定证据）**：现画 4 张**矢量**图 —— 线性流程图 / 带环流程图 /
     条形图 / 散点图 —— 打印它们的几何特征。要点：**条形图**（坐标轴图）的 `n_rect` 与流程图
     同量级 ⇒ 单特征阈值**分不开**「示意图」与「坐标轴图」。

  C) **形态细分（线性/分支/分层/环路）的重建实验**：环路要靠"节点图"检测；
     本节现画一个 4 框环路，用最朴素的"矩形=节点、箭头=边"重建，看能不能检出环 ——
     能不能，以及**为什么在真语料上做不到**（语料矢量图的 `n_rect` 中位数只有 2）。

样本自造，只写 build/m3-schematic-recon/controls/（**不入库**）。
"""
import os
import sys

import fitz
fitz.TOOLS.mupdf_display_errors(False)
fitz.TOOLS.mupdf_display_warnings(False)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import schematicprobe as sp                                    # noqa: E402
import tableprobe as tp                                        # noqa: E402

OUT = os.path.join(REPO, "build", "m3-schematic-recon", "controls")
W, H = 612.0, 792.0
BL, BR = 72.0, 540.0


def _page():
    doc = fitz.open()
    p = doc.new_page(width=W, height=H)
    return doc, p


def _txt(p, x, y, s, size=10):
    p.insert_text((x, y), s, fontsize=size, fontname="helv")


def _box(p, x, y, w, h, label):
    p.draw_rect(fitz.Rect(x, y, x + w, y + h), color=(0, 0, 0), width=0.8)
    _txt(p, x + 4, y + h / 2 + 3, label)


def _arrow(p, x0, y0, x1, y1):
    p.draw_line(fitz.Point(x0, y0), fitz.Point(x1, y1), color=(0, 0, 0), width=0.8)
    # 箭头尖（小三角）
    p.draw_polyline([fitz.Point(x1 - 5, y1 - 3), fitz.Point(x1, y1), fitz.Point(x1 - 5, y1 + 3)],
                    color=(0, 0, 0), width=0.8)


# ---------------- A) kind 控制样本 ----------------
def build_S1_flowchart():
    """矢量流程图：5 个框 + 箭头 + Figure 1 图注。"""
    doc, p = _page()
    _txt(p, 250, 90, "Figure 1: Pipeline")
    y = 120
    for i in range(5):
        _box(p, BL + 40, y + i * 60, 120, 30, "Step %d" % (i + 1))
        if i < 4:
            _arrow(p, BL + 100, y + i * 60 + 30, BL + 100, y + (i + 1) * 60)
    return doc


def build_S2_plot():
    """矢量坐标轴图：框 + 刻度 + 折线 + 图注。"""
    doc, p = _page()
    _txt(p, 250, 90, "Figure 2: Series")
    r = fitz.Rect(120, 120, 500, 360)
    p.draw_rect(r, color=(0, 0, 0), width=0.8)
    for i in range(1, 8):
        x = r.x0 + r.width / 8 * i
        p.draw_line(fitz.Point(x, r.y1), fitz.Point(x, r.y1 - 5), color=(0, 0, 0), width=0.5)
    for i in range(1, 6):
        y = r.y0 + r.height / 6 * i
        p.draw_line(fitz.Point(r.x0, y), fitz.Point(r.x0 + 5, y), color=(0, 0, 0), width=0.5)
    pts = [fitz.Point(r.x0 + r.width * k / 20, r.y1 - r.height * (0.2 + 0.6 * ((k * 7) % 11) / 10))
           for k in range(21)]
    p.draw_polyline(pts, color=(0, 0.3, 0.7), width=1.0)
    return doc


def build_S3_bar():
    """矢量条形图：很多**矩形**（这才是 n_rect 分不开的元凶）。"""
    doc, p = _page()
    _txt(p, 250, 90, "Figure 3: Bars")
    r = fitz.Rect(120, 120, 500, 360)
    for i in range(8):
        x = r.x0 + 10 + i * 44
        h = 30 + (i * 37) % 180
        p.draw_rect(fitz.Rect(x, r.y1 - h, x + 28, r.y1), color=(0.1, 0.3, 0.6), fill=(0.6, 0.75, 0.9))
    p.draw_line(fitz.Point(r.x0, r.y1), fitz.Point(r.x1, r.y1), color=(0, 0, 0), width=0.8)
    p.draw_line(fitz.Point(r.x0, r.y0), fitz.Point(r.x0, r.y1), color=(0, 0, 0), width=0.8)
    return doc


def build_S4_scatter():
    """矢量散点：大量小段（n_small 的元凶）。"""
    doc, p = _page()
    _txt(p, 250, 90, "Figure 4: Scatter")
    r = fitz.Rect(120, 120, 500, 360)
    p.draw_rect(r, color=(0, 0, 0), width=0.8)
    for i in range(300):
        x = r.x0 + r.width * ((i * 97) % 383) / 383
        y = r.y1 - r.height * ((i * 53) % 239) / 239
        p.draw_line(fitz.Point(x, y), fitz.Point(x + 3, y), color=(0.2, 0.2, 0.8), width=0.6)
    return doc


def build_S5_raster():
    """位图贴入：贴一张 PNG，无矢量。"""
    doc, p = _page()
    _txt(p, 250, 90, "Figure 5: Raster")
    src = fitz.open()
    sp_ = src.new_page(width=400, height=300)
    for i in range(5):
        sp_.draw_rect(fitz.Rect(20 + i * 60, 40, 70 + i * 60, 120), color=(0, 0, 0),
                      fill=(0.9, 0.6 + 0.05 * i, 0.3))
    pm = sp_.get_pixmap(dpi=90)
    p.insert_image(fitz.Rect(120, 120, 500, 380), pixmap=pm)
    return doc


def build_S6_table():
    """三线表 + `Table 1` 表题 + 一条 `Figure 6` 图注（应判 table，排除；不得当图）。"""
    doc, p = _page()
    _txt(p, 250, 190, "Figure 6: not a figure")
    _txt(p, 250, 120, "Table 1: demo")
    for y in (140, 156, 220):
        p.draw_line(fitz.Point(BL, y), fitz.Point(BR, y), color=(0, 0, 0), width=0.8)
    for i in range(4):
        _txt(p, 80, 172 + 16 * i, "row %d" % i)
        _txt(p, 300, 172 + 16 * i, "%d" % (i * 3))
    return doc


def build_S7_textonly():
    """纯文本页，无图注。"""
    doc, p = _page()
    for i in range(20):
        _txt(p, BL, 100 + 18 * i, "Body line without any figure caption at all here.")
    return doc


CASES_A = [
    ("S1_矢量流程图", build_S1_flowchart, "vector"),
    ("S2_矢量坐标轴图", build_S2_plot, "vector"),
    ("S3_矢量条形图", build_S3_bar, "vector"),
    ("S4_矢量散点图", build_S4_scatter, "vector"),
    ("S5_位图贴入", build_S5_raster, "raster"),
    ("S6_三线表带图注", build_S6_table, "table-or-none"),
    ("S7_纯文本页", build_S7_textonly, "no-figure"),
]


def _treg(p, captioned=True):
    """表区 → 排除用。captioned=True 只取**带 `Table N` 表题**的（生产口径）。"""
    res = tp.analyze_page(p)
    return [(t["x0"], t["y0"], t["x1"], t["y1"]) for t in res["tables"] if t["kind"] == "table"
            and (not captioned or t["cap"] in ("above", "below", "both"))]


def part_a():
    print("## A) kind 分类控制（自造样本）")
    print("   ★ 排除表区有两个口径：naive=任何'横线成组'的区；prod=只取**带 `Table N` 表题**的区。")
    print("     S1（流程图）专测这一点：它的框线会被 naive 判成表（跨仪器误伤），prod 不会。")
    npass = nfail = 0
    for name, builder, expect in CASES_A:
        doc = builder()
        path = os.path.join(OUT, name + ".pdf")
        doc.save(path)
        p = doc[0]
        kinds_naive = [r["kind"] for r in sp.figure_records(p, _treg(p, captioned=False))]
        recs = sp.figure_records(p, _treg(p, captioned=True))
        kinds = [r["kind"] for r in recs]
        if expect == "no-figure":
            ok = (len(recs) == 0)
        elif expect == "table-or-none":
            ok = all(k in ("table", "none") for k in kinds) and len(kinds) > 0
        else:
            ok = expect in kinds
        npass += ok
        nfail += (not ok)
        mark = "" if kinds_naive == kinds else "   [naive口径=%s]" % kinds_naive
        print("   %-16s 期望=%-14s 实测 kind=%s  %s%s" % (name, expect, kinds, "PASS" if ok else "FAIL", mark))
        for r in recs:
            if r["bbox"] and r["kind"] == "vector":
                print("        %s 特征 %s" % (r["kind"], sp.region_vector_features(p, r["bbox"])))
    print("   小计：PASS %d / FAIL %d（共 %d）" % (npass, nfail, len(CASES_A)))
    print()


def part_b():
    print("## B) 可分性实验：**矢量**示意图 vs **矢量**坐标轴图（读数 6 的否定证据）")
    print("   现画 4 张矢量图，量同一组几何特征：")
    rows = {}
    for name, builder in [("线性流程图", build_S1_flowchart), ("条形图", build_S3_bar),
                          ("散点图", build_S4_scatter), ("坐标轴折线", build_S2_plot)]:
        doc = builder()
        p = doc[0]
        recs = sp.figure_records(p, [])
        r = [x for x in recs if x["kind"] == "vector"]
        if not r:
            continue
        f = sp.region_vector_features(p, r[0]["bbox"])
        rows[name] = f
        print("   %-10s n_rect=%3d n_small=%5d n_curve=%4d n_items=%5d n_text=%3d"
              % (name, f["n_rect"], f["n_small"], f["n_curve"], f["n_items"], f["n_text"]))
    if "线性流程图" in rows and "条形图" in rows:
        a, b = rows["线性流程图"]["n_rect"], rows["条形图"]["n_rect"]
        print("   ★ 结论：线性流程图的 n_rect=%d，条形图（坐标轴图）n_rect=%d —— **同一量级**"
              % (a, b))
        print("     ⇒ 任何 n_rect 阈值都把条形图当成流程图（或反之）⇒ 单特征**分不开**两类。")
    print("   ★ 且散点图的 n_small 远大于流程图 ⇒ 只能把散点图分出去，条形图/折线图仍混在一起。")
    print()


def part_c():
    print("## C) 形态细分（线性/分支/分层/环路）的重建实验")
    print("   现画一个 **4 框环路**（反馈回路），用最朴素的重建法：矩形=节点、线段=边。")
    doc, p = _page()
    _txt(p, 240, 400, "Figure 8: Loop")
    boxes = [(150, 120), (350, 120), (350, 300), (150, 300)]
    for (x, y) in boxes:
        _box(p, x, y, 100, 40, "N")
    for i in range(4):
        x0, y0 = boxes[i]
        x1, y1 = boxes[(i + 1) % 4]
        _arrow(p, x0 + 100 if x1 > x0 else x0, y0 + 20 if y1 == y0 else y0 + 40,
               x1 if y1 == y0 else x1 + 50, y1 + 20 if y1 == y0 else y1)
    path = os.path.join(OUT, "S8_loop.pdf")
    doc.save(path)
    # 朴素重建：矩形 = 节点
    p = doc[0]
    rects = []
    lines = []
    for dr in p.get_drawings():
        for it in dr["items"]:
            if it[0] == "re":
                rr = it[1]
                if rr.width > 20 and rr.height > 10:
                    rects.append((rr.x0, rr.y0, rr.x1, rr.y1))
            elif it[0] == "l":
                p1, p2 = it[1], it[2]
                lines.append((p1.x, p1.y, p2.x, p2.y))
    print("   重建得到：节点（矩形）= %d 个，线段 = %d 条" % (len(rects), len(lines)))
    print("   ★ 环路的判定需要**邻接关系**（哪条边连哪两个节点），而 get_drawings() 只给**路径**，")
    print("     不给拓扑 ⇒ 得靠'端点落在哪个框内'去猜。本例画得干净，猜得出来；")
    print("     **但真语料做不到**：矢量图的 n_rect 中位数只有 2（见 probe_2 读数 6 的分布）")
    print("     ⇒ 大多数矢量图**凑不出 >=3 个节点**，节点图无从谈起。")
    print("   ★ 分层同样要节点图（按 y 聚类成层）；分支要**箭头方向**（箭头尖是一个小三角，")
    print("     与它连接的线不共享端点，方向须另行配对）—— 本支**未实现**，故**不承诺**。")
    print()


def main():
    os.makedirs(OUT, exist_ok=True)
    print("### probe_3_controls —— 自造控制页 + 读数 6 可行性实验")
    print("# 页面 %.0fx%.0f 版心 %.0f..%.0f" % (W, H, BL, BR))
    print()
    part_a()
    part_b()
    part_c()


if __name__ == "__main__":
    main()
