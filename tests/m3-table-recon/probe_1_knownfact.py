#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_1_knownfact.py —— 重跑任务书里那条"已知事实"探针（不引用，当场跑）。

对象：corpus/历届优秀论文/2022年美赛特等奖原版论文集/A/2200289.pdf 第 7 页（0-based 6）。
任务书说：fitz 的 get_drawings() 量到 4 条长横线（y=107.3/122.1/512.6 成组 + 48.9 像页眉线）。
本探针：把原始 4 条线逐条打印，再用 tableprobe 的判据过一遍，看它把这条判成什么。
"""
import os
import fitz

import tableprobe as tp

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(REPO, "corpus", "历届优秀论文",
                   "2022年美赛特等奖原版论文集", "A", "2200289.pdf")
PAGE = 6


def main():
    print("### probe_1_knownfact —— 复跑 2200289.pdf 第 7 页")
    print("pdf  = %s" % os.path.relpath(PDF, REPO).replace("\\", "/"))
    print("page = %d (0-based) / %d pages" % (PAGE, fitz.open(PDF).page_count))
    d = fitz.open(PDF)
    p = d[PAGE]
    rect = p.rect
    print("mediabox/page rect = %.2f x %.2f" % (rect.width, rect.height))
    print()
    print("--- 原始 get_drawings() 全部条目 ---")
    for i, dr in enumerate(p.get_drawings()):
        r = dr["rect"]
        over = "  <== x1 出页框(%.2f)" % rect.x1 if r.x1 > rect.x1 else ""
        print("  #%d type=%s color=%s w=%.3f rect=(%.2f,%.2f,%.2f,%.2f)%s" %
              (i, dr["type"], dr["color"], dr.get("width") or 0.0,
               r.x0, r.y0, r.x1, r.y1, over))
    print()
    print("--- 水平线段（h_segments，已裁到页框）---")
    hs = tp.h_segments(p)
    for (x0, x1, y, col, w) in hs:
        print("  y=%8.3f  x %8.3f .. %8.3f  len=%7.3f  color=%s" % (y, x0, x1, x1 - x0, col))
    print()
    lines = tp.text_lines(p)
    left, right = tp.body_box(lines, rect)
    print("--- 版心（由文本行推，不含表区前）left=%.2f right=%.2f width=%.2f" %
          (left, right, right - left))
    print()
    print("--- analyze_page() 判词 ---")
    res = tp.analyze_page(p)
    print("  body_left=%.2f body_right=%.2f body_width=%.2f" %
          (res["body_left"], res["body_right"], res["body_width"]))
    print("  tables=%d" % len(res["tables"]))
    for t in res["tables"]:
        print("   region x %.1f..%.1f  y %.1f..%.1f  n_rules=%d  vert=%s  cap=%s  width_ratio=%.3f" %
              (t["x0"], t["x1"], t["y0"], t["y1"], t["n"], t["vert"], t["cap"], t["width_ratio"]))
        for (y, x0, x1) in t["rules"]:
            print("     rule y=%.2f x %.2f..%.2f" % (y, x0, x1))
    print()
    print("--- 表题文本行（CAPTION_RE 命中）---")
    for (x0, y0, x1, y1, t) in lines:
        if tp.CAPTION_RE.search(t or ""):
            print("   y %.1f..%.1f x %.1f..%.1f  %r" % (y0, y1, x0, x1, t.strip()[:60]))


if __name__ == "__main__":
    main()
