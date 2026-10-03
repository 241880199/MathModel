#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_0_inventory.py —— 分母侦察：论文层是哪些 PDF、图注锚点有多少。

★ **不收税重造分母**：`unit` 分类**直接复用** `tests/m3-table-recon/probe_0_inventory.py`
  的 `probe_pdf` / `classify`（同一支仪器、同一套阈值）—— 本探针只做两件事：
    ① 把 table 那支的 276 份分类**当场重跑**一遍，确认论文层仍是 164 份；
    ② 数**图注锚点**（`Figure N:` 起首的行）—— 这是本支的"图"单位。

铁律：只读 corpus/**，不写任何文件。
"""
import os
import sys
import glob
import importlib.util
from collections import Counter

import fitz
fitz.TOOLS.mupdf_display_errors(False)
fitz.TOOLS.mupdf_display_warnings(False)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import schematicprobe as sp                                    # noqa: E402

# ---- 按路径加载 table 那支的 probe_0（文件名撞名，不能直接 import）--------
_tp_path = os.path.join(REPO, "tests", "m3-table-recon", "probe_0_inventory.py")
_spec = importlib.util.spec_from_file_location("_table_inv", _tp_path)
_ti = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ti)


def main():
    corpus = _ti.CORPUS
    print("### probe_0_inventory —— 分母侦察（复用 table 支的 unit 分类）")
    print("# repo = %s" % REPO)
    print("# fitz = %s" % fitz.__doc__.splitlines()[0])
    print("# 分类器出处 = tests/m3-table-recon/probe_0_inventory.py（probe_pdf / classify）")
    print()

    paths = sorted(glob.glob(os.path.join(corpus, "**", "*.pdf"), recursive=True))
    rows = []
    for f in paths:
        rec = _ti.probe_pdf(f)
        unit = _ti.classify(_src(f, _ti), rec)
        rows.append((f, unit, rec))
    c = Counter(u for _, u, _ in rows)
    print("## A) 276 份 PDF 的 unit 分布（table 支的判据，当场重跑）")
    for k, v in sorted(c.items()):
        print("   %-12s %4d" % (k, v))
    print("   %-12s %4d" % ("TOTAL", len(rows)))
    print()

    papers = [f for f, u, _ in rows if u == "paper"]
    print("## B) 论文层（分母）= %d 份" % len(papers))
    print("   口径：单册单题、有文本层、页数 <60 的 O 奖论文 PDF（与 table 支**同一判据**）。")
    print("   不含：37 份 UMAP 扫描合集 · 67 份官方赛题 · 8 份官方文档。")
    print()

    print("## C) 图注锚点（`Figure N:` 起首的行）= 本支的「图」单位")
    tot_caps = 0
    per_pdf = {}
    pages = 0
    for f in papers:
        d = fitz.open(f)
        n = 0
        for p in d:
            pages += 1
            n += len(sp.captions(p))
        per_pdf[os.path.relpath(f, REPO).replace("\\", "/")] = n
        tot_caps += n
        d.close()
    pdfs_with = sum(1 for v in per_pdf.values() if v > 0)
    print("   论文层总页数 = %d" % pages)
    print("   图注锚点总数 = %d，分布在 %d / %d 份论文里" % (tot_caps, pdfs_with, len(papers)))
    print("   单篇最多 = %d（%s）" % (max(per_pdf.values()),
                                   max(per_pdf, key=per_pdf.get)))
    print("   ★ 注意：这是**图注锚点**数，不等于「图」数 —— 一页多图、图注跨行都会让它偏。")
    print("     真正的按图分类见 probe_2。")
    print()

    print("## D) 可量性预判（读数 1 的伏笔；真读数在 probe_2）")
    print("   ★ 本支实测的核心事实：这些论文的图**绝大多数是位图贴入**（PNG/JPEG 嵌进 PDF），")
    print("     不是矢量绘制 ⇒ 几何特征（节点框 / 箭头）**只对矢量图可用**。")
    print("     故 probe_2 会把每张图先判 raster / vector，并**点名排除**不可量的那批。")
    print()


def _src(f, ti):
    """按路径反推先验来源类型（与 table 支的 SOURCES 同表）。"""
    rel = os.path.relpath(f, ti.CORPUS).replace("\\", "/")
    for sub, stype in ti.SOURCES:
        if rel.startswith(sub + "/"):
            return stype
    return "?"


if __name__ == "__main__":
    main()
