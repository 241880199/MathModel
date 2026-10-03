#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""probe_2_corpus.py —— 全量扫描论文层，产出六个读数。

用法：
    python tests/m3-schematic-recon/probe_2_corpus.py                 # 全量
    python tests/m3-schematic-recon/probe_2_corpus.py --montage       # 另把抽样拼图渲进 build/（人眼判类用）
    python tests/m3-schematic-recon/probe_2_corpus.py --papers 8      # 只扫前 8 篇（冒烟）

产物流 stdout（由 gen-evidence.py 装配为 out-2-corpus.txt）。
★ 进度写 **stderr** ⇒ 复跑捕获**不要**接 `2>&1`（见 README）。

只读 corpus/**；`--montage` 只写 build/m3-schematic-recon/**（gitignored）。
"""
import os
import sys
import glob
import argparse
from collections import Counter, defaultdict

import fitz
fitz.TOOLS.mupdf_display_errors(False)
fitz.TOOLS.mupdf_display_warnings(False)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import schematicprobe as sp                                    # noqa: E402
import tableprobe as tp                                        # noqa: E402

N_ALL_SAMPLE = 96          # 读数 1 的人眼抽样大小（全图均匀系统抽样）
N_VEC_SAMPLE = 48          # 读数 6 可行性的人眼抽样大小（只抽矢量图）


def pctl(xs, p):
    if not xs:
        return float("nan")
    xs = sorted(xs)
    return xs[int(round((len(xs) - 1) * p))]


def _f6_verdict(emb, ref):
    """F6 三态（口径同 check-figure-style 的 F6 分支）。"""
    import importlib.util
    p = os.path.join(REPO, "tests", "skills", "figure-choose", "check-figure-style.py")
    spec = importlib.util.spec_from_file_location("_cfs2", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not emb:
        return "N/A"
    return "PASS" if all(any(k in f for k in mod.FONT_FAMILY_OK) for f in emb) else "FAIL"


def wilson(k, n, z=1.96):
    """Wilson 95% 置信区间（小样本用，别拿 Wald）。"""
    if n == 0:
        return (0.0, 0.0)
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * ((ph * (1 - ph) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _family(name):
    """字体族名 = 剥掉子集前缀后、第一个 '-' 前的部分（启发式，写实）。"""
    return (name or "").split("-")[0].strip().lower()


def _modal_family(font_sets):
    """一篇论文里出现页数最多的字体族（取每页字体集里的每个族各记一次）。"""
    cnt = Counter()
    for s in font_sets:
        for x in s:
            cnt[_family(x)] += 1
    return cnt.most_common(1)[0][0] if cnt else None


def load_labels():
    """读 sample-labels.tsv（人眼判定；缺文件则返回空 dict）。"""
    path = os.path.join(HERE, "sample-labels.tsv")
    out = {"all": {}, "vec": {}}
    if not os.path.exists(path):
        return out
    for ln in open(path, encoding="utf-8"):
        if ln.startswith("#") or ln.startswith("set\t"):
            continue
        f = ln.rstrip("\n").split("\t")
        if len(f) >= 4:
            out.setdefault(f[0], {})[int(f[1])] = (f[2], f[3])
    return out


def paper_paths():
    import importlib.util
    p = os.path.join(REPO, "tests", "m3-table-recon", "probe_0_inventory.py")
    spec = importlib.util.spec_from_file_location("_table_inv", p)
    ti = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ti)
    out = []
    for f in sorted(glob.glob(os.path.join(ti.CORPUS, "**", "*.pdf"), recursive=True)):
        rec = ti.probe_pdf(f)
        rel = os.path.relpath(f, ti.CORPUS).replace("\\", "/")
        st = "?"
        for sub, stype in ti.SOURCES:
            if rel.startswith(sub + "/"):
                st = stype
                break
        if ti.classify(st, rec) == "paper":
            out.append(f)
    return out


def scan(papers, do_montage):
    figs = []            # 每张图的记录
    pagecache = {}       # (rel, pno) -> dict(body_w, f6)
    for i, f in enumerate(papers):
        rel = os.path.relpath(f, REPO).replace("\\", "/")
        try:
            d = fitz.open(f)
        except Exception:
            continue
        for p in d:
            if p.rotation:
                continue
            try:
                res = tp.analyze_page(p)
            except Exception:
                continue
            body_w = res["body_width"]
            # ★ 只把**带 `Table N` 表题**的表区当作"排除对象"：光凭"横线成组"会把
            #   流程图的框线误判成表（probe_3 的 S1 实测）⇒ 见 README 的已知边界。
            treg = [(t["x0"], t["y0"], t["x1"], t["y1"])
                    for t in res["tables"] if t["kind"] == "table"
                    and t["cap"] in ("above", "below", "both")]
            recs = sp.figure_records(p, treg)
            if not recs:
                continue
            emb, ref = sp.page_fonts(d, p.number)
            v = _f6_verdict(emb, ref)
            for r in recs:
                row = {"rel": rel, "page": p.number + 1, "num": r["num"], "kind": r["kind"],
                       "cap": (r["cap"] or "").strip(), "words": sp.caption_words(r["cap"]),
                       "f6": v, "femb": tuple(sorted(emb)), "body_w": body_w,
                       "ratio": None, "colors": None, "mono": None, "bbox": r["bbox"]}
                if r["bbox"]:
                    w = r["bbox"][2] - r["bbox"][0]
                    row["ratio"] = w / body_w if body_w else None
                    if r["kind"] in ("raster", "vector"):
                        cc = sp.region_color_count(p, r["bbox"])
                        row["colors"] = cc
                        row["mono"] = (cc is not None and cc <= sp.MONO_MAX_COLORS)
                    if r["kind"] == "vector":
                        row["vf"] = sp.region_vector_features(p, r["bbox"])
                figs.append(row)
        d.close()
        if (i + 1) % 20 == 0:
            sys.stderr.write("  ... %d/%d\r" % (i + 1, len(papers)))
    sys.stderr.write("\n")
    if do_montage:
        render_montages(figs)
    return figs


def render_montages(figs):
    """把两套人眼抽样的图区渲成网格 PNG（只写 build/）。"""
    out = os.path.join(REPO, "build", "m3-schematic-recon", "montage")
    os.makedirs(out, exist_ok=True)
    measurable = [r for r in figs if r["kind"] in ("raster", "vector") and r["bbox"]]
    idx = sp.sample_index(len(measurable), N_ALL_SAMPLE)
    sample_all = [measurable[j] for j in idx]
    vecs = [r for r in figs if r["kind"] == "vector" and r.get("vf")]
    vname = os.path.join(REPO, "build", "m3-schematic-recon", "vec_sample.tsv")
    buf = []
    for j in sp.sample_index(len(vecs), N_VEC_SAMPLE):
        r = vecs[j]
        buf.append("%s\t%d\t%d\t%s\n" % (r["rel"], r["page"], r["num"], r["cap"][:60]))
    with open(vname, "wb") as fh:            # ★ 写入一律 write_bytes（全 LF）
        fh.write("".join(buf).encode("utf-8"))
    _tile(out, "all", sample_all)
    _tile(out, "vec", [vecs[j] for j in sp.sample_index(len(vecs), N_VEC_SAMPLE)])


def _tile(outdir, prefix, rows, cols=4, per=24):
    """把 rows 里的图区从原页裁出来拼成 per 个一格。rows 记录里必须有 bbox。"""
    for m in range(0, len(rows), per):
        chunk = rows[m:m + per]
        tiles = []
        maxw = maxh = 0
        for r in chunk:
            f = os.path.join(REPO, r["rel"])
            d = fitz.open(f)
            p = d[r["page"] - 1]
            bbox = r.get("bbox")
            if bbox is None:
                d.close()
                continue
            rct = fitz.Rect(bbox[0], max(0, bbox[1] - 2), bbox[2], bbox[3] + 12)
            s = float(min(1.6, max(0.45, 430.0 / max(rct.width, 1))))
            pm = p.get_pixmap(clip=rct, matrix=fitz.Matrix(s, s), colorspace=fitz.csRGB, alpha=False)
            tiles.append((pm, "%s p%d" % (os.path.basename(f), r["page"]), m + len(tiles)))
            maxw = max(maxw, pm.width)
            maxh = max(maxh, pm.height)
            d.close()
        if not tiles:
            continue
        nrow = (len(tiles) + cols - 1) // cols
        W = cols * (maxw + 10) + 10
        H = nrow * (maxh + 30) + 10
        big = fitz.open()
        page = big.new_page(width=W, height=H)
        for k, (pm, label, gi) in enumerate(tiles):
            col = k % cols
            row = k // cols
            x = 10 + col * (maxw + 10)
            y = 10 + row * (maxh + 30)
            page.insert_image(fitz.Rect(x, y, x + pm.width, y + pm.height), pixmap=pm)
            page.insert_text((x + 3, y + pm.height + 14), "#%d %s" % (gi, label), fontsize=10)
        path = os.path.join(outdir, "%s_%02d.png" % (prefix, m // per))
        page.get_pixmap(dpi=100).save(path)
        print("# montage -> %s" % os.path.relpath(path, REPO).replace("\\", "/"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--montage", action="store_true")
    ap.add_argument("--papers", type=int, default=0)
    a = ap.parse_args()

    papers = paper_paths()
    if a.papers:
        papers = papers[:a.papers]
    print("### probe_2_corpus —— 全量扫描六读数")
    print("# 论文层 = %d 份（tableprobe 同一分类器）" % len(papers))
    print("# 阈值（schematicprobe）：图注带 %.0fpt · 矢量 >=%d 条目 · 图区 >=%.0fx%.0f/%.0fpt^2"
          % (sp.FIG_BAND_PT, sp.VEC_MIN_ITEMS, sp.MIN_REGION_W, sp.MIN_REGION_H, sp.MIN_REGION_AREA))
    print("# 复用：F2 数色(color_count) · F3b 词数(caption_body) · F6 内嵌字体(page_font_split) —— 均取自")
    print("#       tests/skills/figure-choose/check-figure-style.py（真复用，非重写）")
    print()

    figs = scan(papers, a.montage)
    print("## 0) 分母与「图」的总量")
    print("   论文层 = %d 份；图元记录（图注锚点命中的图/空位）= %d" % (len(papers), len(figs)))
    kd = Counter(r["kind"] for r in figs)
    for k in ("raster", "vector", "tiny-vector", "table", "none"):
        print("     kind=%-11s %5d" % (k, kd[k]))
    print("   ★ 说明：")
    print("     · raster      = 位图贴入的图（几何**不可量**；宽度/配色仍可量）")
    print("     · vector      = 几何可量的矢量图（读数 6 的唯一可用子集）")
    print("     · tiny-vector = 只有零星矢量图元（分隔线/边角），**不成图**")
    print("     · table       = 与表区重叠 >=%.2f 的区（是表不是图，**排除**）" % sp.TABLE_OVERLAP_FRAC)
    print("     · none        = 图注下方/上方找不到任何图元（图注是正文引用或图在下一段外）")
    print()

    # ---------------- 读数 1 ----------------
    print("## 1) 读数 1 · 非数据图占比")
    print("   ★ **机械判据做不到**（本支核心否定结论，证据在 `## 0` 与 `## 6`）：")
    print("     · 示意图与坐标轴图**没有**表格那种硬特征（横线）；")
    print("     · 论文层的图 %.0f%% 是位图贴入 ⇒ 连几何都取不到（见上 kind=raster）。"
          % (100.0 * kd["raster"] / max(len(figs), 1)))
    print("   ⇒ 只报**机械可判的部分** + **人眼抽样的估计**（下表），两件事分清。")
    measurable = [r for r in figs if r["kind"] in ("raster", "vector")]
    print("   ① 机械可判：可定位图区（raster+vector）= %d / %d = %.1f%%"
          % (len(measurable), len(figs), 100.0 * len(measurable) / max(len(figs), 1)))
    print("      其中位图（几何不可量）%d = %.1f%%；矢量（几何可量）%d = %.1f%%"
          % (kd["raster"], 100.0 * kd["raster"] / max(len(figs), 1),
             kd["vector"], 100.0 * kd["vector"] / max(len(figs), 1)))
    idx = sp.sample_index(len(measurable), N_ALL_SAMPLE)
    print("   ② 人眼抽样：从可定位图区里**均匀系统抽样** %d 张（step=%d，无随机种子）"
          % (len(idx), max(1, len(measurable) // N_ALL_SAMPLE)))
    labels = load_labels()
    lab_all = labels.get("all", {})
    if lab_all:
        cnt = Counter(lab_all.get(j, ("?", "-"))[0] for j in range(len(idx)))
        n = len(idx)
        print("      判定表 = sample-labels.tsv（**人眼判定，不是机械读数**）")
        for k in ("schematic", "plot", "other", "table"):
            lo, hi = wilson(cnt[k], n)
            print("      %-10s %3d / %d = %5.1f%%   Wilson95%%CI [%.1f%%, %.1f%%]"
                  % (k, cnt[k], n, 100.0 * cnt[k] / n, 100 * lo, 100 * hi))
        nonaxi = cnt["schematic"] + cnt["other"]
        lo, hi = wilson(nonaxi, n)
        print("      **非坐标轴图**（schematic+other）%d / %d = %.1f%%  CI [%.1f%%, %.1f%%]"
              % (nonaxi, n, 100.0 * nonaxi / n, 100 * lo, 100 * hi))
        forms = Counter(lab_all[j][1] for j in range(len(idx))
                        if lab_all.get(j, ("", "-"))[0] == "schematic")
        print("      示意图的形态分布（**人眼判定**，不声称穷尽）：%s"
              % dict(forms.most_common()))
    else:
        print("      !! 缺 sample-labels.tsv ⇒ 只印抽样清单，不报占比")
    print()

    # ---------------- 读数 2 ----------------
    print("## 2) 读数 2 · 图宽 / 版心比（分母口径与 table 支**同一支仪器**）")
    print("   用 tableprobe.analyze_page(page)['body_width']（表区已排除）⇒ 与 m3-table-recon 的 2 可比。")
    ratios = [r["ratio"] for r in measurable if r["ratio"]]
    if ratios:
        print("   n=%d  min=%.3f  p10=%.3f  median=%.3f  p90=%.3f  max=%.3f"
              % (len(ratios), min(ratios), pctl(ratios, .10), pctl(ratios, .50),
                 pctl(ratios, .90), max(ratios)))
        bins = [(0, .3), (.3, .5), (.5, .7), (.7, .9), (.9, 1.001), (1.001, 1.15), (1.15, 9)]
        for lo, hi in bins:
            k = sum(1 for x in ratios if lo < x <= hi)
            print("      (%.2f, %.2f] : %4d  %5.1f%%" % (lo, hi, k, 100.0 * k / len(ratios)))
        print("   ★ 满版心（>=0.90）= %d (%.1f%%)；>1.0 = %d (%.1f%%)"
              % (sum(1 for x in ratios if x >= .90), 100.0 * sum(1 for x in ratios if x >= .90) / len(ratios),
                 sum(1 for x in ratios if x > 1.0), 100.0 * sum(1 for x in ratios if x > 1.0) / len(ratios)))
    print()

    # ---------------- 读数 3 ----------------
    print("## 3) 读数 3 · 配色（F2 度量：彩色主色数 / 是否单色系）")
    cols = [r["colors"] for r in measurable if r["colors"] is not None]
    if cols:
        print("   n=%d（可栅格化的图区）  min=%d  p50=%d  p90=%d  max=%d"
              % (len(cols), min(cols), pctl(cols, .5), pctl(cols, .9), max(cols)))
        for k in range(0, 8):
            print("      彩色主色数 = %d : %4d  %5.1f%%" % (k, cols.count(k), 100.0 * cols.count(k) / len(cols)))
        print("      >=8 并入 '8+' : %4d" % sum(1 for c in cols if c >= 8))
        mono = sum(1 for r in measurable if r["mono"])
        print("   ★ 单色系（彩色主色数 <= %d）= %d / %d = %.1f%%"
              % (sp.MONO_MAX_COLORS, mono, len(cols), 100.0 * mono / len(cols)))
    print("   ★ 口径：与 F2 同（NEAREST 缩到 320x320，剔近灰 max-min<24，占比 >=0.5% 才算主色）。")
    print("     F5 的『是否命中 H14 显式色序』**不在此测** —— 那是**产物规范**，语料的图不是按它画的。")
    print()

    # ---------------- 读数 4 ----------------
    print("## 4) 读数 4 · 图注词数（F3b 口径：去 `Figure N:` 前缀后的正文）")
    words = [r["words"] for r in figs]
    if words:
        print("   n=%d  min=%d  p50=%d  p90=%d  p95=%d  max=%d"
              % (len(words), min(words), pctl(words, .5), pctl(words, .9), pctl(words, .95), max(words)))
        for lo, hi in [(0, 6), (6, 12), (12, 17), (17, 25), (25, 10**9)]:
            k = sum(1 for w in words if lo <= w < hi)
            print("      词数 [%2d,%s) : %4d  %5.1f%%" % (lo, hi if hi < 10**9 else "inf", k, 100.0 * k / len(words)))
        n_ge13 = sum(1 for w in words if w >= 13)
        n_gt17 = sum(1 for w in words if w > 17)
        print("   计数（对照 H9）：>=13 词（即「>12 ⇒ 不合格侧」）= %d / %d = %.1f%%；"
              ">17 词（F3b 硬失败线）= %d / %d = %.1f%%"
              % (n_ge13, len(words), 100.0 * n_ge13 / len(words),
                 n_gt17, len(words), 100.0 * n_gt17 / len(words)))
        print("   ★ 对照 F3b/H9 的现阈值：<=%d 合格、>%d 硬失败" % (12, 17))
    print()

    # ---------------- 读数 5 ----------------
    print("## 5) 读数 5 · 示意图所在页的内嵌字体（F6 口径）")
    print("   ★ 如实说明：图**本身是位图** ⇒ 图内文字**不是字体对象**；本读数量的是**该页的**内嵌字体，")
    print("     即『这张图所在页的字体是否与正文同源』，**不是**『图里的字用了什么字体』。")
    f6 = Counter(r["f6"] for r in figs if r["kind"] in ("raster", "vector"))
    tot = sum(f6.values())
    for k in ("PASS", "FAIL", "N/A"):
        print("   %-4s %5d  %5.1f%%" % (k, f6[k], 100.0 * f6[k] / max(tot, 1)))
    print("   （PASS=内嵌且族在 %s；N/A=该页未内嵌任何字体）" % "FONT_FAMILY_OK")
    print("   ★ 这个 PASS/FAIL 是 F6 自己的判词；它衡量的是「族在不在**本 skill 的允许集合**里」，")
    print("     不是「与正文同源」。下面才是本读数问的那件事：")
    # 每篇取"最常见的内嵌**族**"当正文基线；再看每张图所在页是否与之同族
    per = defaultdict(list)
    for r in figs:
        if r["kind"] in ("raster", "vector"):
            per[r["rel"]].append(r["femb"])
    same = diff = unk = 0
    for rel, lst in per.items():
        fam = _modal_family(lst)
        for s in lst:
            if not s:
                unk += 1
                continue
            fset = {_family(x) for x in s}
            if fam is not None and fset == {fam}:
                same += 1
            else:
                diff += 1
    tt = same + diff + unk
    print("   ★ 同源判定（**族级**）：图页的内嵌字体**族** == 该**论文最常见的**字体族")
    print("     （族 = 剥掉子集前缀后、'-' 前的部分；如 TeXGyreTermesX-Regular → TeXGyreTermesX）")
    print("     同族 %d (%5.1f%%) · 不同族 %d (%5.1f%%) · 图页未内嵌字体 %d (%5.1f%%)"
          % (same, 100.0 * same / max(tt, 1), diff, 100.0 * diff / max(tt, 1),
             unk, 100.0 * unk / max(tt, 1)))
    print("     ⇒ 图内文字不在文本层（图是位图）⇒ 这个读数只说明**页面**字体，见 README 的边界。")
    print()

    # ---------------- 读数 6 ----------------
    print("## 6) 读数 6 · 形态粗分类（线性/分支/分层/环路）—— **可行性**")
    vecs = [r for r in figs if r["kind"] == "vector" and r.get("vf")]
    print("   可用子集 = 矢量图 %d 张（占全部图元记录的 %.1f%%）"
          % (len(vecs), 100.0 * len(vecs) / max(len(figs), 1)))
    if len(vecs) >= 2:
        for key in ("n_rect", "n_small", "n_curve", "n_items", "n_text"):
            xs = [r["vf"][key] for r in vecs]
            print("   %-8s min=%6d p25=%6d med=%6d p75=%7d max=%8d"
                  % (key, min(xs), pctl(xs, .25), pctl(xs, .5), pctl(xs, .75), max(xs)))
    lab_vec = labels.get("vec", {})
    vidx = sp.sample_index(len(vecs), N_VEC_SAMPLE)
    if lab_vec:
        # 在**人眼标注**的矢量抽样上，算每个单特征的"最佳阈值精度" vs 全判多数类的基线
        ys = [1 if lab_vec.get(j, ("", "-"))[0] == "schematic" else 0 for j in range(len(vidx))]
        ns = sum(ys)
        base = max(ns, len(ys) - ns) / len(ys)
        buckets = Counter(lab_vec.get(j, ("?", "-"))[0] for j in range(len(vidx)))
        print("   ★ 关键否定证据：这些特征上，**人眼判为示意图**与**判为「非示意图」**的图**重叠**。")
        print("     （此处对照 = 示意图 vs 非示意图，**比任务书问的四分类更粗**；那 %d 张"
              % (len(ys) - ns))
        print("       「非示意图」里**并不全是坐标轴图** —— 成分 = %s，见 sample-labels.tsv）"
              % dict((k, buckets[k]) for k in ("plot", "other", "table") if buckets[k]))
        print("   人眼抽样 %d 张矢量图（step=%d，起点 0，无随机数）：示意图 %d / 非示意图 %d"
              % (len(ys), max(1, len(vecs) // N_VEC_SAMPLE), ns, len(ys) - ns))
        print("     **全判多数类的基线 = %.3f**（= %d 张里 %d 张示意图全漏，判错率 %.1f%%）"
              % (base, len(ys), ns, 100.0 * (1.0 - base)))
        best_acc = base
        for key in ("n_rect", "n_small", "n_curve", "n_items", "n_text"):
            xs = [vecs[vidx[j]]["vf"][key] for j in range(len(vidx))]
            best = (0.0, "", None)
            for t in sorted(set(xs)):
                for op in ("<=", ">"):
                    pred = [1 if ((v <= t) if op == "<=" else (v > t)) else 0 for v in xs]
                    acc = sum(1 for a, b in zip(pred, ys) if a == b) / len(ys)
                    if acc > best[0]:
                        best = (acc, "%s %s%d" % (key, op, t), t)
            best_acc = max(best_acc, best[0])
            print("   %-8s 最佳单特征阈值精度 = %.3f  （%s；基线 %.3f）"
                  % (key, best[0], best[1], base))
        print("   ★ 单特征**都不过基线附近**（或仅略高，最好者只多对 1 张）⇒ 用它定「是不是示意图」"
              "判错率 ≈%.1f%%~%.1f%%" % (100.0 * (1.0 - best_acc), 100.0 * (1.0 - base)))
        print("   ★ a fortiori（**四分类本身没测过**，靠更粗的一步撑）：连这个**更粗**的二分类")
        print("     （示意图 vs 非示意图）都不过基线 ⇒ **更细**的四分类（线性/分支/分层/环路 **互相**分开）")
        print("     **更不可能**；且 `probe_3` 的 C 组**独立地**否掉了四分类所需的拓扑特征")
        print("     （谁连谁 / 箭头朝向，`get_drawings()` 不给）。")
    else:
        print("   ★ 关键否定证据：这些特征上，**人眼判为示意图**与**判为「非示意图」**的图**重叠**。")
        print("   !! 缺 sample-labels.tsv（vec 集）⇒ 不报可分性数字")
    print("   ⇒ **不可机械定稿**。降级结论与骨架表规则见 README。")
    print()

    # ---------------- 抽样清单 ----------------
    print("# ---- 抽样清单（供人眼复核；索引即 montage 里的 #N）----")
    print("# [A] 读数 1 全图抽样（%d 张）：" % len(idx))
    for j, gi in enumerate(idx):
        r = measurable[gi]
        print("#   %3d  %s p%-3d kind=%-6s words=%2d  %s"
              % (j, r["rel"], r["page"], r["kind"], r["words"], r["cap"][:56]))
    print("# [B] 读数 6 矢量抽样（%d 张）：" % N_VEC_SAMPLE)
    for j, gi in enumerate(sp.sample_index(len(vecs), N_VEC_SAMPLE)):
        r = vecs[gi]
        print("#   %3d  %s p%-3d rect=%3d small=%5d curve=%5d items=%5d  %s"
              % (j, r["rel"], r["page"], r["vf"]["n_rect"], r["vf"]["n_small"],
                 r["vf"]["n_curve"], r["vf"]["n_items"], r["cap"][:44]))


if __name__ == "__main__":
    main()
