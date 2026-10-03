#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_1_knownfact.py —— 正 / 负控制（**人眼确认过的真实语料页**，不引用，当场跑）。

硬要求 4：至少一条已知事实的验证 —— 一张人眼确认**是**示意图的页（探针认得出），
再加一条人眼确认**不是**的（探针不误判）。

★ 本支的"认得出"是**分层的**（因为读数 1 的机械分类做不到，见 README）：
   · 认得出 = 探针**定位到图区**并判对它的 kind（vector / raster / none）；
   · 不误判 = 纯文本页不冒出图来、图不在此页的图注不当成图。

四张控制页（**人眼判定，2026-10-03 当场看渲出的 crop**）：
  C1 正 · 矢量示意图：2209812.pdf p3「Figure 1: Literature Review Framework」（框+箭头）
  C2 正 · 位图示意图：2200289.pdf p5「Figure 1: Structure of Our Work」（框+箭头，**位图贴入**）
  C3 负 · 纯文本页：2210307.pdf p2（无图注、无图元）
  C4 负 · 图不在此页：2207343.pdf p11「Figure 8: ...」的行锚点（图在别处 ⇒ 应判 none）

渲染的 crop 落在 build/m3-schematic-recon/controls/（**不入库**，可由本探针重跑）。

只读 corpus/**；只写 build/**。
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

CASES = [
    ("C1", "历届优秀论文/2022年美赛特等奖原版论文集/A/2209812.pdf", 2,
     "正 · 矢量示意图（Literature Review Framework）", "vector"),
    ("C2", "历届优秀论文/2022年美赛特等奖原版论文集/A/2200289.pdf", 4,
     "正 · 位图示意图（Structure of Our Work）", "raster"),
    ("C3", "历届优秀论文/2022年美赛特等奖原版论文集/A/2210307.pdf", 1,
     "负 · 纯文本页（无图）", "no-figure"),
    ("C4", "历届优秀论文/2022年美赛特等奖原版论文集/A/2207343.pdf", 10,
     "负 · 图不在此页（图注行锚点）", "nonfigure"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    print("### probe_1_knownfact —— 正/负控制（真实语料页）")
    print("# 阈值同 schematicprobe（矢量 >=%d 条目 · 图区 >=%.0fx%.0f/%.0fpt^2）"
          % (sp.VEC_MIN_ITEMS, sp.MIN_REGION_W, sp.MIN_REGION_H, sp.MIN_REGION_AREA))
    print()
    npass = nfail = 0
    for cid, rel, pno, desc, expect in CASES:
        path = os.path.join(REPO, "corpus", rel)
        d = fitz.open(path)
        p = d[pno]
        res = tp.analyze_page(p)
        treg = [(t["x0"], t["y0"], t["x1"], t["y1"]) for t in res["tables"] if t["kind"] == "table"]
        recs = sp.figure_records(p, treg)
        kinds = [r["kind"] for r in recs]
        print("== %s  %s" % (cid, desc))
        print("   pdf  = corpus/%s" % rel)
        print("   page = %d (0-based) / %d" % (pno, d.page_count))
        print("   图注锚点 = %d 条；判出的 kind = %s" % (len(recs), kinds))
        for r in recs:
            bw = res["body_width"]
            if r["bbox"]:
                w = r["bbox"][2] - r["bbox"][0]
                cc = sp.region_color_count(p, r["bbox"]) if r["kind"] in ("raster", "vector") else None
                print("     #%s %-11s bbox=%s  w=%.1f ratio=%.3f colors=%s words=%d   %r"
                      % (r["num"], r["kind"], [round(v) for v in r["bbox"]], w,
                         w / bw if bw else float("nan"), cc, sp.caption_words(r["cap"]),
                         r["cap"].strip()[:46]))
                if r["kind"] == "vector":
                    print("        矢量特征 %s" % sp.region_vector_features(p, r["bbox"]))
            else:
                print("     #%s %-11s （无图区）  %r" % (r["num"], r["kind"], r["cap"].strip()[:46]))
        # 渲出 crop 供人眼复核（文件名含记录下标 ⇒ 同页多图不互相覆盖）
        for k, r in enumerate(recs):
            if not r["bbox"]:
                continue
            rct = fitz.Rect(r["bbox"][0], max(0, r["bbox"][1] - 3), r["bbox"][2], r["bbox"][3] + 16)
            pm = p.get_pixmap(clip=rct, dpi=110, colorspace=fitz.csRGB, alpha=False)
            fn = os.path.join(OUT, "%s_p%d_%d.png" % (cid, pno + 1, k))
            pm.save(fn)
            print("     crop -> %s" % os.path.relpath(fn, REPO).replace("\\", "/"))
        if expect == "no-figure":
            ok = (len(recs) == 0)
        elif expect == "nonfigure":
            # 该页的图注里有一条**不是图**（none / 只有零星线段的 tiny-vector）
            ok = ("none" in kinds or "tiny-vector" in kinds)
        else:
            ok = (expect in kinds)
        npass += ok
        nfail += (not ok)
        print("   → 期望 kind=%s ；实测 %s  ⇒ %s" % (expect, kinds, "PASS" if ok else "FAIL"))
        print()
        d.close()
    print("### 汇总：PASS %d / FAIL %d（共 %d）" % (npass, nfail, len(CASES)))
    print("★ 若有一条 FAIL：以本文为准订正探针或如实标边界，**不许当没看见**。")


if __name__ == "__main__":
    main()
