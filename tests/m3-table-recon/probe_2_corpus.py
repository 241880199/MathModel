#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_2_corpus.py —— 全量扫描 corpus/**，产出六个读数。

用法：
    python tests/m3-table-recon/probe_2_corpus.py            # 全量 276 份
    python tests/m3-table-recon/probe_2_corpus.py --papers   # 只扫论文层 164 份

【采样口径】默认**全量**，不抽样（T6）。分母分两层（T1）：
  * 论文层 = probe_0 判为 unit=paper 的 164 份（单册单题 O 奖论文）
  * 全语料 = 276 份（另含 37 份扫描合集、67 份赛题、8 份官方文档）

产物：stdout（由 gen-evidence.py 装配为 out-2-corpus.txt）
      + build/m3-table-recon/tables_detail.csv（逐表留痕；**不入库**）
"""
import sys, os, glob, csv, argparse
from collections import Counter, defaultdict

import fitz
fitz.TOOLS.mupdf_display_errors(False)   # 本语料有 PDF 缺 ExtGState/ICC ⇒ 关掉噪声
fitz.TOOLS.mupdf_display_warnings(False)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tableprobe as tp
from probe_0_inventory import probe_pdf, classify, SOURCES, CORPUS, REPO

DETAIL = os.path.join(REPO, "build", "m3-table-recon", "tables_detail.csv")


def pct(xs, p):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    return xs[int(round((len(xs) - 1) * p))]


def scan(paths, only_papers):
    """扫一批 PDF，返回 (per_pdf_rows, table_rows, counters)。"""
    pdf_rows = []
    table_rows = []
    c = Counter()
    for n, f in enumerate(paths):
        rel = os.path.relpath(f, REPO).replace("\\", "/")
        rec = probe_pdf(f)
        unit = classify(unit_of(f), rec)
        if only_papers and unit != "paper":
            continue
        page_chars = rec["chars"] / max(rec["pages"], 1) if not rec.get("error") else 0
        row = {"rel": rel, "unit": unit, "pages": rec.get("pages"),
               "chars": rec.get("chars"), "chpp": round(page_chars, 1),
               "measurable": False, "ntab": 0, "nrot": 0, "nerr": 0}
        try:
            d = fitz.open(f)
        except Exception as e:
            row["nerr"] = 1
            pdf_rows.append(row)
            continue
        measurable = page_chars >= 20
        row["measurable"] = measurable
        ntab = 0
        for p in d:
            if p.rotation:
                row["nrot"] += 1
                continue
            try:
                res = tp.analyze_page(p)
            except Exception as e:
                row["nerr"] += 1
                c["page_error"] += 1
                continue
            for t in res["tables"]:
                c["cand_total"] += 1
                if t["kind"] == "figure":       # 图框被误当表（T2）⇒ 剔除并计数
                    c["dropped_figure"] += 1
                    if t["fig_cap"]:
                        c["drop_by_caption"] += 1
                    if t["small_seg"] > tp.SMALL_SEG_MAX:
                        c["drop_by_smallseg"] += 1
                    continue
                ntab += 1
                c["tables"] += 1
                c["rules_n_%d" % min(t["n"], 9)] += 1
                if t["vert"]:
                    c["vert_yes"] += 1
                else:
                    c["vert_no"] += 1
                c["cap_%s" % t["cap"]] += 1
                if t["width_ratio"] > 1.001:
                    c["ratio_gt1"] += 1
                if t["width_ratio"] > 0.999 and t["width_ratio"] <= 1.001:
                    c["ratio_eq1"] += 1
                clipped = t["x1"] >= p.rect.x1 - 0.5
                if clipped:
                    c["clipped_right"] += 1
                table_rows.append({
                    "rel": rel, "page": p.number + 1, "n_rules": t["n"],
                    "x0": round(t["x0"], 2), "x1": round(t["x1"], 2),
                    "y0": round(t["y0"], 2), "y1": round(t["y1"], 2),
                    "body_w": round(res["body_width"], 2),
                    "width_ratio": round(t["width_ratio"], 4),
                    "vert": int(t["vert"]), "cap": t["cap"],
                    "small_seg": t["small_seg"], "fig_cap": int(t["fig_cap"]),
                    "n_lines": t["n_lines"], "cap_algo": int(t["cap_algo"]),
                    "win_text": int(t["win_text"]),
                    "clipped": int(clipped),
                    "page_w": round(p.rect.width, 2),
                    "page_h": round(p.rect.height, 2),
                })
        row["ntab"] = ntab
        if measurable:
            c["measurable_pdf"] += 1
        else:
            c["unmeasurable_pdf"] += 1
        if ntab:
            c["pdf_with_table"] += 1
        pdf_rows.append(row)
        if (n + 1) % 20 == 0:
            sys.stderr.write("  ... %d/%d\r" % (n + 1, len(paths)))
    sys.stderr.write("\n")
    return pdf_rows, table_rows, c


def unit_of(f):
    """由路径反推先验来源类型（与 probe_0 的 SOURCES 一致）。"""
    rel = os.path.relpath(f, CORPUS).replace("\\", "/")
    for sub, stype in SOURCES:
        if rel.startswith(sub + "/"):
            return stype
    return "?"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers", action="store_true", help="只扫论文层")
    args = ap.parse_args()

    paths = sorted(glob.glob(os.path.join(CORPUS, "**", "*.pdf"), recursive=True))
    print("### probe_2_corpus —— 全量扫描六读数")
    print("# 扫描范围 = corpus/**/*.pdf 共 %d 份" % len(paths))
    print("# --papers = %s" % args.papers)
    print("# 阈值（tableprobe）：长线>=版心宽*%.2f · 三线表>=%d 条 · 厚度<=%.1fpt"
          % (tp.MIN_RULE_LEN_FRAC, tp.MIN_GROUP, tp.H_THIN_PT))
    print()
    rows, tabs, c = scan(paths, args.papers)
    if args.papers:
        rows = [r for r in rows if r["unit"] == "paper"]
        keep = {r["rel"] for r in rows}
        tabs = [t for t in tabs if t["pdf"] in keep]

    units = Counter(r["unit"] for r in rows)
    print("## 0) 分母（T1）")
    for k, v in sorted(units.items()):
        print("   unit=%-10s %4d 份" % (k, v))
    print("   合计 %d 份" % len(rows))
    print("   ★ 只有 unit=paper 是**论文**；unit=volume(扫描合集)/problem(赛题)/official(文档) 不是。")
    print()

    # 读数 6：不可量（在**全 276** 上报，因为分母错则后面全错）
    print("## 6) 不可量的比例（**先看这个**，否则上面占比不可信）")
    n = len(rows)
    unmeas = [r for r in rows if not r["measurable"]]
    print("   无可测文本层（<20 字/页）：%d / %d = %.1f%%" % (len(unmeas), n, 100.0 * len(unmeas) / n))
    print("     其中按 unit：%s" % dict(Counter(r["unit"] for r in unmeas)))
    print("   有文本层但页解析报错（nerr>0）：%d 份" % sum(1 for r in rows if r["nerr"]))
    print("   有旋转页被跳过：%d 份（共 %d 页）" % (sum(1 for r in rows if r["nrot"]),
                                              sum(r["nrot"] for r in rows)))
    print("   ⇒ **可量层**（全语料）= %d 份" % sum(1 for r in rows if r["measurable"]))
    print()

    print("## 0b) T2 剔除：图框/坐标轴被误当表区（**这层不算完读数就是假的**）")
    print("   表区候选总数（剔除前）= %d" % c["cand_total"])
    print("   判为图而剔除 = %d（由图类表题 %d + 小图元过多 %d；两者可同时命中）"
          % (c["dropped_figure"], c["drop_by_caption"], c["drop_by_smallseg"]))
    print("   ⇒ 保留为「表」 = %d" % c["tables"])
    print("   ★ 残余风险：无表题、且小图元 < %d 的图框仍可能混进来（本探针无判据，未量化）"
          % tp.SMALL_SEG_MAX)
    print()

    # ★ 主分母 = 论文层
    papers = [r for r in rows if r["unit"] == "paper"]
    papers_m = [r for r in papers if r["measurable"]]
    paper_rels = {r["rel"] for r in papers_m}
    ptabs = [t for t in tabs if t["rel"] in paper_rels]
    print("## 1) 三线表的普及度  ※**主分母 = 论文层 164 份**")
    print("   定义：一页上有一组 >= %d 条**长横线**（长度 >= 版心宽*%.2f），"
          % (tp.MIN_GROUP, tp.MIN_RULE_LEN_FRAC))
    print("         左右端对齐；同组内是否含长竖线属读数 5。这里先记「表区候选」。")
    print("   论文层：%d 份，其中可量 %d 份（不可量 %d 份 = %.1f%%）" %
          (len(papers), len(papers_m), len(papers) - len(papers_m),
           100.0 * (len(papers) - len(papers_m)) / max(len(papers), 1)))
    pw = sum(1 for r in papers_m if r["ntab"] > 0)
    print("   ① 按**论文**（分母 %d）：含 >=1 表区的论文 %d = **%.1f%%**" %
          (len(papers_m), pw, 100.0 * pw / max(len(papers_m), 1)))
    tot_pages = sum(r["pages"] for r in papers_m)
    tab_pages = len({(t["rel"], t["page"]) for t in ptabs})
    print("   ② 按**页**（论文层总页 %d，跳过的旋转页 %d）：含表区的页 %d = %.1f%%" %
          (tot_pages, sum(r["nrot"] for r in papers_m), tab_pages,
           100.0 * tab_pages / max(tot_pages, 1)))
    print("   ③ 表区总数 = %d（每篇平均 %.2f 个）" % (len(ptabs), len(ptabs) / max(len(papers_m), 1)))
    per = Counter(t["rel"] for t in ptabs)
    if per:
        print("   ④ 单篇最多表区 = %d（%s）" % (max(per.values()), max(per, key=per.get)))
    print("   ---- 对照（非论文层，**不是**普及度分母，仅供参考）----")
    for u in ("volume", "problem", "official"):
        us = {r["rel"] for r in rows if r["unit"] == u and r["measurable"]}
        ut = [t for t in tabs if t["rel"] in us]
        print("     unit=%-8s 可量 %3d 份 / 表区 %4d 个" % (u, len(us), len(ut)))
    print()

    print("## 0c) 内部一致性自检：表区内有没有文本行（空框/纯图框的嫌疑）")
    nl = Counter(min(t.get("n_lines", 0), 3) for t in ptabs)
    tot_all = max(len(ptabs), 1)
    print("   表区（论文层，剔除图后）共 %d" % len(ptabs))
    for k, lab in ((0, "0 行"), (1, "1 行"), (2, "2 行"), (3, ">=3 行")):
        print("   区内文本行 %-6s：%4d (%.1f%%)%s" %
              (lab, nl[k], 100.0 * nl[k] / tot_all,
               "  ← **空框/图框嫌疑**" if k == 0 else ""))
    for t in [t for t in ptabs if t.get("n_lines", 0) == 0][:5]:
        print("      e.g. %s p%s n=%s ratio=%s" % (t["rel"], t["page"], t["n_rules"], t["width_ratio"]))
    print()

    # 之后的读数只在论文层上讲
    tabs = ptabs
    print("## 2) 表宽占版心比（分母 = 版心宽，由文本行推）※以下读数一律以论文层为准")
    ratios = [t["width_ratio"] for t in tabs]
    if ratios:
        print("   n=%d  min=%.3f  p10=%.3f  median=%.3f  p90=%.3f  max=%.3f" %
              (len(ratios), min(ratios), pct(ratios, .10), pct(ratios, .50),
               pct(ratios, .90), max(ratios)))
        bins = [(0, .5), (.5, .7), (.7, .9), (.9, 1.001), (1.001, 1.15), (1.15, 9)]
        for lo, hi in bins:
            k = sum(1 for r in ratios if lo < r <= hi)
            print("      (%.2f, %.2f] : %4d  %5.1f%%" % (lo, hi, k, 100.0 * k / len(ratios)))
        gt1 = sum(1 for r in ratios if r > 1.0)
        clip = sum(1 for t in tabs if t["clipped"])
        print("   ★ 超版心(ratio>1.0) = %d (%.1f%%)；其中**右端被页框裁掉** = %d" %
              (gt1, 100.0 * gt1 / len(ratios), clip))
        print("   ★ 裁掉右端 = 该 PDF 的线画到 MediaBox 之外（T5 实测事实，见 probe_1）")
    print()

    print("## 3) 表题在上方还是下方")
    cap = Counter(t["cap"] for t in tabs)
    tot = sum(cap.values())
    for k in ("above", "below", "both", "none"):
        print("   %-6s %4d  %5.1f%%" % (k, cap[k], 100.0 * cap[k] / max(tot, 1)))
    print("   ★ 误判风险量化：'both'/'none' = 未能唯一判定归属的 = %d / %d = %.1f%%"
          % (cap["both"] + cap["none"], tot,
             100.0 * (cap["both"] + cap["none"]) / max(tot, 1)))
    algo = sum(1 for t in tabs if t["cap_algo"])
    none_win = sum(1 for t in tabs if t["cap"] == "none" and t["win_text"])
    print("   ★ 口径分歧：窗内**或区内**有 **Algorithm N** 标题的 = %d (%.1f%%) —— 多半是**伪代码框**"
          % (algo, 100.0 * algo / max(tot, 1)))
    print("   ★ 风险上界：cap='none' 中窗内**有文本行**的 = %d —— "
          "它们可能是**没编号的表题**（本探针认不出，故不塞进上/下）" % none_win)
    print("   ★ 说明：CAPTION_RE 只认带编号的表题（Table/表 + 编号）；")
    print("     带 *文字* 表题（如 '…shown in the table below'）不计入上/下 ——")
    print("     未标号的表在读数里落到 'none'，**不许硬塞进上或下**。")
    print()

    print("## 4) 横线条数分布（三线表是不是真的三线）")
    nr = Counter(min(t["n_rules"], 9) for t in tabs)
    for k in range(3, 10):
        if nr[k]:
            print("   %d 条横线：%4d  %5.1f%%" % (k, nr[k], 100.0 * nr[k] / max(tot, 1)))
    print("   (>=9 条并入 '9' 桶；本探针不区分更多)")
    print()

    print("## 5) 有竖线 / 全网格的比例")
    vy = sum(1 for t in tabs if t["vert"])
    vn = tot - vy
    print("   表区内检出长竖线（>=表高*%.2f）：%d / %d = **%.1f%%**"
          % (tp.VERT_MIN_FRAC, vy, tot, 100.0 * vy / max(tot, 1)))
    print("   纯三线（无长竖线）：%d = %.1f%%" % (vn, 100.0 * vn / max(tot, 1)))
    print()

    # 逐表落 CSV（build/，不入库）
    os.makedirs(os.path.dirname(DETAIL), exist_ok=True)
    with open(DETAIL, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(tabs[0].keys()))
        w.writeheader()
        for t in tabs:
            w.writerow(t)
    print("# 逐表明细（%d 行，论文层，**不入库**）→ %s" % (len(tabs), os.path.relpath(DETAIL, REPO)))


if __name__ == "__main__":
    main()
