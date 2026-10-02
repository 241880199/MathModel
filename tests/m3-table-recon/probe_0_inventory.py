#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_0_inventory.py —— T1 分母侦察：把 corpus/** 的 276 份 PDF 逐份分类。

产出（stdout，由 gen-evidence.py 装配为 out-0-inventory.txt）：
  * 每个来源目录的 PDF 计数
  * 逐份：页数 / 首页尺寸 / 文本层字符数 / 矢量图元数 → 归入 unit 类
  * 分母候选的汇总

unit 类（不声称穷尽，本探针只区分这 4 类）：
  paper     —— 单篇论文（一册一题，页数少，有文本层）
  volume    —— 多篇合集/扫描卷（页数多，或整册无文本层）
  problem   —— 官方赛题
  official  —— 官方说明/规则文档

铁律：只读 corpus/**，不写任何文件。
"""
import sys, glob, os, json

import fitz

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS = os.path.join(REPO, "corpus")

# 来源目录 → 单元类型（先验，逐份再按实测修正）
SOURCES = [
    ("official",                          "official"),
    ("历届优秀论文/2022年美赛特等奖原版论文集", "paper"),
    ("历届优秀论文/2023年美赛O奖论文",        "paper"),
    ("历届优秀论文/2024年美赛O奖论文",        "paper"),
    ("历届优秀论文/2025美赛O奖论文",          "paper"),
    ("历届优秀论文/UMAP2000-2010年美赛特等奖优秀论文集", "volume"),
    ("历届优秀论文/UMAP2010-2019年美赛特等奖优秀论文集", "volume"),
    ("官方原题",                            "problem"),
    ("algorithms",                        "?"),
    ("papers",                            "?"),
]


def probe_pdf(path):
    """返回单份 PDF 的读数；打不开则返回 None + 原因。"""
    rec = {}
    try:
        d = fitz.open(path)
    except Exception as e:  # 不吞异常：如实上报
        return {"error": "%s: %s" % (type(e).__name__, e)}
    rec["pages"] = d.page_count
    # 全册文本字符数（只读）
    total_chars = 0
    for p in d:
        total_chars += len(p.get_text())
    rec["chars"] = total_chars
    # 首页尺寸（多数册统一；不同则记首页）
    r = d[0].rect
    rec["w"] = round(r.width, 1)
    rec["h"] = round(r.height, 1)
    # 矢量图元：抽 3 页探测（全册太慢）；记录是否任一页有 get_drawings
    n_draw = 0
    for i in range(min(3, d.page_count)):
        try:
            n_draw += len(d[i].get_drawings())
        except Exception:
            pass
    rec["draw3"] = n_draw
    # 位图对象：抽 3 页探测（扫描件的判据）
    n_img = 0
    for i in range(min(3, d.page_count)):
        try:
            n_img += len(d[i].get_images(full=True))
        except Exception:
            pass
    rec["img3"] = n_img
    # 页面尺寸是否全册统一
    sizes = set()
    for i in range(min(10, d.page_count)):
        rr = d[i].rect
        sizes.add((round(rr.width), round(rr.height)))
    rec["sizes10"] = sorted(sizes)
    d.close()
    return rec


def classify(src_type, rec):
    """按实测把先验类型修正。判据写清，不声称穷尽。"""
    if rec.get("error"):
        return "unreadable"
    if src_type in ("official", "problem", "?"):
        return src_type
    # 论文/合集：无文本层 ⇒ 扫描件（归 volume/unmeasurable 层）
    per_page = rec["chars"] / max(rec["pages"], 1)
    if per_page < 20:
        return "volume" if src_type == "volume" else "paper-scan"
    # 页数阈值：单篇 MCM 论文 20~35 页；合集 >= 60 页
    if rec["pages"] >= 60:
        return "volume"
    return "paper"


def main():
    rows = []
    print("### probe_0_inventory —— corpus/** PDF 分类（T1 分母）")
    print("# repo = %s" % REPO)
    print("# fitz = %s" % fitz.__doc__.splitlines()[0])
    print()
    print("%-58s %-10s %5s %8s %6s %6s %6s  %s" %
          ("relpath", "src-type", "pages", "chars", "w", "h", "draw3", "unit"))
    print("-" * 120)
    for sub, stype in SOURCES:
        d = os.path.join(CORPUS, sub)
        if not os.path.isdir(d):
            print("!! 目录不存在: %s" % sub)
            continue
        fs = sorted(glob.glob(os.path.join(d, "**", "*.pdf"), recursive=True))
        for f in fs:
            rel = os.path.relpath(f, REPO).replace("\\", "/")
            rec = probe_pdf(f)
            unit = classify(stype, rec)
            rec["unit"] = unit
            rec["rel"] = rel
            rec["src_type"] = stype
            rows.append(rec)
            if rec.get("error"):
                print("%-58s %-10s  ERROR %s" % (rel, stype, rec["error"]))
            else:
                print("%-58s %-10s %5d %8d %6.0f %6.0f %6d  %s" %
                      (rel, stype, rec["pages"], rec["chars"], rec["w"], rec["h"],
                       rec["draw3"], unit))
    print()
    print("### 汇总（不声称穷尽；本探针只区分下表这些 unit）")
    from collections import Counter
    c = Counter(r["unit"] for r in rows)
    for k, v in sorted(c.items()):
        print("  %-12s %4d" % (k, v))
    print("  %-12s %4d  (= 文件总数)" % ("TOTAL", len(rows)))
    # 分母候选
    papers = [r for r in rows if r["unit"] == "paper"]
    print()
    print("### 论文分母候选（unit=paper）：%d 份" % len(papers))
    print("  口径：单册单题、有文本层、页数 <60 的 O 奖论文 PDF。")
    print("  不含：scanned 卷（UMAP）、官方赛题、官方文档。")
    print()
    print("### 可量性预判（reading 6 的伏笔；真正的读数在 probe_2）")
    n_text = sum(1 for r in rows if not r.get("error") and r["chars"] > 0)
    n_draw = sum(1 for r in rows if not r.get("error") and r["draw3"] > 0)
    print("  全样本 %d 份：有文本层 %d、抽 3 页见矢量图元 %d" % (len(rows), n_text, n_draw))
    print("  ⇒ 无文本层的 PDF 一律量不出表（probe_2 会以 chars/pages 判）")


if __name__ == "__main__":
    main()
