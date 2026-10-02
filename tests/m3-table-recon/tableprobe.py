#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tableprobe.py —— `mcm-table` 侦察用的**共享取数库**（只读）。

本模块把"从一页 PDF 里量表格"这件事拆成可独立复核的几步：

  1. `h_segments(page)` / `v_segments(page)` —— 把 `get_drawings()` 的路径拆成
     水平 / 垂直**线段**（`l` 线段、`re` 矩形的四条边都算），并**裁剪到页面框**
     （T5：本语料实测有 PDF 的线画到 MediaBox 之外，不裁就会把表宽算大）。
  2. `text_lines(page)` —— 抽文本行 bbox（`get_text("dict")`）。
  3. `long_rules(segs, body_width, ...)` —— 从水平线段里挑"长横线"。
  4. `group_rules(...)` —— 把长横线按**左右端对齐**分组 ⇒ 表区候选。
  5. `body_box(...)` —— 从文本行推**版心**（T1/T5 的分母）。
  6. `caption_pos(...)` —— 表题在表上方 / 下方 / 未定。

**口径不声称穷尽。** 每条判据的阈值都写在这里，且 probe_3 的正/负控制会验它们。
"""
import re
from statistics import median

# ---- 判据阈值（**全部写死在这里，改 = 改探针**）----------------------------
MIN_RULE_LEN_FRAC = 0.50   # "长"横线：长度 >= 版心宽 * 此比例
H_THIN_PT = 2.5            # 水平线的厚度上限（> 此值当矩形/色块，不当线）
V_THIN_PT = 2.5            # 垂直线的厚度上限
ALIGN_TOL = 2.0            # 端点对齐容差（pt）
LEN_TOL = 3.0              # 同组内长度容差（pt）
MIN_GROUP = 3              # 三线表：一组至少几条长横线
MAX_RULE_GAP_FRAC = 0.75   # 同组相邻两线的最大 y 间距（> 页面高*此比例 ⇒ 拆组）
PROSE_MIN_GAP = 30.0       # 拆组：两线间距 < 此值不拆（普通表行不拆）
PROSE_LEFT_FRAC = 0.08     # "正文行"：x0 距表区左端 <= 表宽*此比例
PROSE_LEN_FRAC = 0.45      # "正文行"：长度 >= 表宽*此比例
PROSE_LINES_MIN = 2        # 夹缝里 >= 这么多"正文行" ⇒ 判为两表之间的段落
HEADER_BAND_FRAC = 0.075   # 页眉带：y0 < 页高*此比例 ⇒ 不当表线（T2）
FOOTER_BAND_FRAC = 0.930   # 页脚带：y1 > 页高*此比例 ⇒ 不当表线（T2）
CAPTION_WINDOW = 46.0      # 表题搜索窗（pt）
CAPTION_RE = re.compile(r"(?:^|[\s(（\[])(Table|TABLE|Tab\.?|表)\s*[0-9IVXivx]")
FIGURE_RE = re.compile(r"(?:^|[\s(（\[])(Figure|FIGURE|Fig\.?|图)\s*[0-9IVXivx]")
ALGO_RE = re.compile(r"(?:^|[\s(（\[])(Algorithm|ALGORITHM|算法)\s*[0-9IVXivx]")
SMALL_SEG_PT = 6.0         # "小图元"（刻度/标记）长度上限
SMALL_SEG_MAX = 40         # 表区内小图元超过此数 ⇒ 疑为图（T2）
MIN_REGION_H = 8.0         # 表区最小高度：矮于此 ⇒ 退化（几条线画在同一 y），丢弃
VERT_MIN_FRAC = 0.25       # 竖线：高度 >= 表区高 * 此比例 ⇒ 记为该表区有竖线

INK_DARK = 0.5             # 线的亮度上限（0=黑 1=白）；白/浅色线不算


def _lum(c):
    if c is None:
        return None
    if isinstance(c, (int, float)):
        return float(c)
    try:
        r, g, b = c[0], c[1], c[2]
    except Exception:
        return None
    return (r + g + b) / 3.0


def h_segments(page):
    """返回 [(x0, x1, y, color, width)]，已裁剪到页面框。"""
    out = []
    rect = page.rect
    for dr in page.get_drawings():
        col = dr.get("color")
        fill = dr.get("fill")
        w = dr.get("width") or 0.0
        for it in dr["items"]:
            kind = it[0]
            if kind == "l":
                p1, p2 = it[1], it[2]
                if abs(p1.y - p2.y) <= H_THIN_PT:
                    y = (p1.y + p2.y) / 2.0
                    x0, x1 = sorted((p1.x, p2.x))
                    x0 = max(x0, rect.x0); x1 = min(x1, rect.x1)
                    if x1 - x0 > 0:
                        out.append((x0, x1, y, col, w))
            elif kind == "re":
                r = it[1]
                if r.height <= H_THIN_PT:          # 扁矩形 = 一条线（含填充色块边）
                    x0 = max(r.x0, rect.x0); x1 = min(r.x1, rect.x1)
                    if x1 - x0 > 0:
                        out.append((x0, x1, r.y0, fill if fill else col, dr.get("width") or 0.0))
                elif col is not None:              # 描边矩形：取上下两条边
                    for yy in (r.y0, r.y1):
                        x0 = max(r.x0, rect.x0); x1 = min(r.x1, rect.x1)
                        if x1 - x0 > 0:
                            out.append((x0, x1, yy, col, w))
                # else: 纯填充背景块（表头色带等）⇒ **不**当线
    return out


def v_segments(page):
    """返回 [(y0, y1, x, color, width)]，已裁剪到页面框。"""
    out = []
    rect = page.rect
    for dr in page.get_drawings():
        col = dr.get("color")
        fill = dr.get("fill")
        w = dr.get("width") or 0.0
        for it in dr["items"]:
            kind = it[0]
            if kind == "l":
                p1, p2 = it[1], it[2]
                if abs(p1.x - p2.x) <= V_THIN_PT:
                    x = (p1.x + p2.x) / 2.0
                    y0, y1 = sorted((p1.y, p2.y))
                    y0 = max(y0, rect.y0); y1 = min(y1, rect.y1)
                    if y1 - y0 > 0:
                        out.append((y0, y1, x, col, w))
            elif kind == "re":
                r = it[1]
                if r.width <= V_THIN_PT:
                    y0 = max(r.y0, rect.y0); y1 = min(r.y1, rect.y1)
                    if y1 - y0 > 0:
                        out.append((y0, y1, r.x0, fill if fill else col, w))
                elif col is not None:
                    for xx in (r.x0, r.x1):
                        y0 = max(r.y0, rect.y0); y1 = min(r.y1, rect.y1)
                        if y1 - y0 > 0:
                            out.append((y0, y1, xx, col, w))
                # else: 纯填充背景块（表头色带等）⇒ **不**当线
    return out


MAX_LINE_H_ABS = 30.0      # 单行文本行高度上限（超过 ⇒ 旋转气泡/水印，非正文行）


def text_lines(page):
    """返回 [(x0, y0, x1, y1, text)]（按 y 排序）。

    ★ 实测事实（2025 语料）：页面水印（如"校苑数模公众号"）被抽成**一条跨越整页的
    文本行**（bbox 高可达 450pt）。这种"行"的 y 中心会落进任何表缝里，若不剔除
    就会把每张表都拆开 ⇒ 按行高上限剔除。
    """
    out = []
    d = page.get_text("dict")
    for b in d.get("blocks", []):
        if b.get("type") != 0:
            continue
        for ln in b.get("lines", []):
            x0, y0, x1, y1 = ln["bbox"]
            txt = "".join(s.get("text", "") for s in ln.get("spans", []))
            out.append((x0, y0, x1, y1, txt))
    if not out:
        return out
    hs = sorted(y1 - y0 for (_, y0, _, y1, _) in out)
    med = hs[len(hs) // 2]
    cap = max(3.0 * med, MAX_LINE_H_ABS)
    out = [l for l in out if (l[3] - l[1]) <= cap]
    out.sort(key=lambda t: (t[1], t[0]))
    return out


def _pct(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    i = int(round((len(xs) - 1) * p))
    return xs[i]


def body_box(lines, page_rect, exclude_regions=()):
    """从文本行推版心 (left, right)。

    exclude_regions: [(x0,y0,x1,y1)] —— 表格区；与表区相交的文本行不参与推版心
    （表内文字往往超出正文栏宽，会把分母撑大）。
    """
    keep = []
    for (x0, y0, x1, y1, t) in lines:
        if not t.strip():
            continue
        if _overlaps_any(x0, y0, x1, y1, exclude_regions):
            continue
        keep.append((x0, x1))
    if len(keep) < 3:
        keep = [(l[0], l[2]) for l in lines if l[4].strip()] or keep
    if not keep:
        return None
    left = _pct([k[0] for k in keep], 0.02)
    right = _pct([k[1] for k in keep], 0.98)
    return left, right


def _overlaps_any(x0, y0, x1, y1, regions, pad=2.0):
    for (rx0, ry0, rx1, ry1) in regions:
        if x1 > rx0 - pad and x0 < rx1 + pad and y1 > ry0 - pad and y0 < ry1 + pad:
            return True
    return False


def long_rules(hsegs, body_width, page_rect):
    """挑长横线：长度 >= 版心宽*MIN_RULE_LEN_FRAC，且在版心（非页眉/页脚带）。"""
    H = page_rect.height
    thr = body_width * MIN_RULE_LEN_FRAC if body_width else 0
    out = []
    for (x0, x1, y, col, w) in hsegs:
        if y < page_rect.y0 + H * HEADER_BAND_FRAC:
            continue
        if y > page_rect.y0 + H * FOOTER_BAND_FRAC:
            continue
        if (x1 - x0) < thr:
            continue
        lum = _lum(col)
        if lum is not None and lum > INK_DARK:
            continue
        out.append((x0, x1, y))
    # 去重：整格矩形描边会把同一条线报两次（上边=下边）
    seen = set()
    ded = []
    for (x0, x1, y) in out:
        k = (round(x0, 1), round(x1, 1), round(y, 1))
        if k in seen:
            continue
        seen.add(k)
        ded.append((x0, x1, y))
    ded.sort(key=lambda t: t[2])
    # 再把「同一条线被画了两三笔」按 y 容差并掉（B18：三条线同在 y≈129 ⇒ 零高区）
    merged = []
    for (x0, x1, y) in ded:
        if merged and abs(merged[-1][2] - y) <= 1.5 \
                and abs(merged[-1][0] - x0) <= ALIGN_TOL and abs(merged[-1][1] - x1) <= ALIGN_TOL:
            continue
        merged.append((x0, x1, y))
    return merged


def _gap_is_prose(lines, y_lo, y_hi, rx0, rx1):
    """两线夹缝里是不是一段正文（⇒ 两表之间的间隔，应拆组）。

    正文行 := x0 靠表区左端 AND 长度接近表宽。表内单元格文本多是短行/居中，
    不满足这两条。
    """
    rw = max(rx1 - rx0, 1.0)
    seg = [l for l in lines
           if y_lo < (l[1] + l[3]) / 2.0 < y_hi and l[2] > rx0 and l[0] < rx1]
    if len(seg) < PROSE_LINES_MIN:
        return False
    n_prose = sum(1 for l in seg
                  if (l[0] - rx0) <= rw * PROSE_LEFT_FRAC and (l[2] - l[0]) >= rw * PROSE_LEN_FRAC)
    return n_prose >= PROSE_LINES_MIN and n_prose >= 0.5 * len(seg)


def _gap_has_outside_line(lines, y_lo, y_hi, rx0, rx1):
    """夹缝里是否有**起点落在表区左端之外**的文本行（⇒ 表与表之间的标题/段落）。

    表内单元格文本不会跑到表区左端之外；表外的行会（缩进表前的小标题、
    正文段落、项目符号）。判据：行的 x0 <= 表区左端 - 3。
    """
    for l in lines:
        yc = (l[1] + l[3]) / 2.0
        if y_lo < yc < y_hi and l[4].strip() and l[0] <= rx0 - 3.0:
            return True
    return False


def _gap_has_caption(lines, y_lo, y_hi):
    """两线夹缝里是否夹着一条表题（⇒ 后一表从这条线开始，应拆组）。"""
    for l in lines:
        yc = (l[1] + l[3]) / 2.0
        if y_lo < yc < y_hi and CAPTION_RE.search(l[4] or ""):
            return True
    return False


def group_rules(rules, page_rect, lines=()):
    """按左右端对齐分组，再按 y 间距裂组。返回 [dict(x0,x1,y0,y1,rules=[(y,x0,x1)])]。"""
    groups = []
    for (x0, x1, y) in rules:
        placed = False
        for g in groups:
            if (abs(x0 - g["x0"]) <= ALIGN_TOL and abs(x1 - g["x1"]) <= ALIGN_TOL):
                g["ys"].append((y, x0, x1))
                placed = True
                break
            if abs((x1 - x0) - (g["x1"] - g["x0"])) <= LEN_TOL and \
               (abs(x0 - g["x0"]) <= ALIGN_TOL or abs(x1 - g["x1"]) <= ALIGN_TOL):
                g["ys"].append((y, x0, x1))
                placed = True
                break
        if not placed:
            groups.append({"x0": x0, "x1": x1, "ys": [(y, x0, x1)]})
    # 裂组：相邻两条 y 距 > 页高*MAX_RULE_GAP_FRAC
    maxgap = page_rect.height * MAX_RULE_GAP_FRAC
    out = []
    for g in groups:
        ys = sorted(g["ys"])
        rx0 = min(r[1] for r in ys); rx1 = max(r[2] for r in ys)
        run = [ys[0]]
        for prev, cur in zip(ys, ys[1:]):
            gap = cur[0] - prev[0]
            if gap > maxgap:
                out.append(run); run = []
            elif gap >= PROSE_MIN_GAP and (
                    _gap_is_prose(lines, prev[0], cur[0], rx0, rx1)
                    or _gap_has_caption(lines, prev[0], cur[0])
                    or _gap_has_outside_line(lines, prev[0], cur[0], rx0, rx1)):
                out.append(run); run = []
            run.append(cur)
        out.append(run)
    regions = []
    for run in out:
        ys = [r[0] for r in run]
        xs0 = [r[1] for r in run]; xs1 = [r[2] for r in run]
        if (max(ys) - min(ys)) < MIN_REGION_H:      # 退化区（同一条 y 上叠了几笔）
            continue
        regions.append({
            "x0": min(xs0), "x1": max(xs1),
            "y0": min(ys), "y1": max(ys),
            "n": len(run),
            "rules": sorted(run),
        })
    regions.sort(key=lambda r: r["y0"])
    return regions


def has_vertical(page, region):
    """表区内是否有长竖线。

    ★ 实测事实（2200401.pdf p5）：列分隔竖线常被**逐行画成小段**（每段只有一行高）。
    ⇒ 必须先按 x 归并相邻竖段、拼出总跨度，再比阈值；否则整张网格表会漏判。
    """
    h = region["y1"] - region["y0"]
    if h <= 0:
        return False
    thr = h * VERT_MIN_FRAC
    # 收集表区内的竖段（按 x 归并）
    segs = []
    for (y0, y1, x, col, w) in v_segments(page):
        if not (region["x0"] - ALIGN_TOL <= x <= region["x1"] + ALIGN_TOL):
            continue
        if y1 <= region["y0"] or y0 >= region["y1"]:
            continue
        lum = _lum(col)
        if lum is not None and lum > INK_DARK:
            continue
        segs.append((x, max(y0, region["y0"]), min(y1, region["y1"])))
    segs.sort()
    merged = []
    for (x, y0, y1) in segs:
        hit = False
        for m in merged:
            if abs(m[0] - x) <= ALIGN_TOL and y0 <= m[2] + 3.0 and y1 >= m[1] - 3.0:
                m[1] = min(m[1], y0); m[2] = max(m[2], y1); hit = True
                break
        if not hit:
            merged.append([x, y0, y1])
    return any((m[2] - m[1]) >= thr for m in merged)


def caption_pos(lines, region):
    """表题在上方还是下方。

    上方判据：top_rule_y 之上 CAPTION_WINDOW 内、x 与表区有交叠、匹配 CAPTION_RE 的行。
    下方同理。返回 'above' / 'below' / 'both' / 'none'。
    """
    above = below = False
    for (x0, y0, x1, y1, t) in lines:
        if not CAPTION_RE.search(t or ""):
            continue
        if x1 < region["x0"] - 4 or x0 > region["x1"] + 4:
            continue
        if 0 < (region["y0"] - y1) <= CAPTION_WINDOW:
            above = True
        if 0 < (y0 - region["y1"]) <= CAPTION_WINDOW:
            below = True
    if above and below:
        return "both"
    if above:
        return "above"
    if below:
        return "below"
    return "none"


def figure_caption_near(lines, region):
    """表区上下窗内是否有 **Figure 类** 表题（⇒ 这是图不是表，T2）。"""
    for (x0, y0, x1, y1, t) in lines:
        if not FIGURE_RE.search(t or ""):
            continue
        if x1 < region["x0"] - 4 or x0 > region["x1"] + 4:
            continue
        if 0 < (region["y0"] - y1) <= CAPTION_WINDOW or 0 < (y0 - region["y1"]) <= CAPTION_WINDOW:
            return True
    return False


def _window_has(lines, region, regex):
    for (x0, y0, x1, y1, t) in lines:
        if not regex.search(t or ""):
            continue
        if x1 < region["x0"] - 4 or x0 > region["x1"] + 4:
            continue
        if 0 < (region["y0"] - y1) <= CAPTION_WINDOW or 0 < (y0 - region["y1"]) <= CAPTION_WINDOW:
            return True
    return False


def algo_mark(lines, region):
    """表区窗内**或区内**有没有 Algorithm 类标题（⇒ 多半是**伪代码框**，口径分歧非 bug）。

    ★ 实测（`2504188.pdf` p11）：算法框的框线画在标题**之上**，"Algorithm 1 …"
    落在**区内** ⇒ 只看窗内会漏掉。故窗内 + 区内一起看。
    """
    if _window_has(lines, region, ALGO_RE):
        return True
    for (x0, y0, x1, y1, t) in lines:
        if not ALGO_RE.search(t or ""):
            continue
        if x1 < region["x0"] - 4 or x0 > region["x1"] + 4:
            continue
        if region["y0"] - 2 <= (y0 + y1) / 2.0 <= region["y1"] + 2:
            return True
    return False


def any_text_in_window(lines, region):
    """表区窗内有没有**任何**文本行（用来量化"表题存在但没编号"的风险）。"""
    for (x0, y0, x1, y1, t) in lines:
        if not t.strip():
            continue
        if x1 < region["x0"] - 4 or x0 > region["x1"] + 4:
            continue
        if 0 < (region["y0"] - y1) <= CAPTION_WINDOW or 0 < (y0 - region["y1"]) <= CAPTION_WINDOW:
            return True
    return False


def small_seg_count(page, region):
    """表区内"小图元"（刻度/散点/标记）条数 —— 图的强特征。"""
    n = 0
    pad = 1.0
    for (x0, x1, y, col, w) in h_segments(page):
        if (x1 - x0) <= SMALL_SEG_PT and region["y0"] - pad <= y <= region["y1"] + pad \
                and x0 >= region["x0"] - pad and x1 <= region["x1"] + pad:
            n += 1
    for (y0, y1, x, col, w) in v_segments(page):
        if (y1 - y0) <= SMALL_SEG_PT and region["y0"] - pad <= y0 <= region["y1"] + pad \
                and region["x0"] - pad <= x <= region["x1"] + pad:
            n += 1
    return n


def analyze_page(page):
    """把一页量成一个 dict（无表则 tables=[]）。"""
    lines = text_lines(page)
    rect = page.rect
    hseg = h_segments(page)
    # 先用"粗略版心"（不含表区排除）挑线；再用线结果反推版心
    left0, right0 = body_box(lines, rect) or (rect.x0, rect.x1)
    bw0 = max(right0 - left0, 1.0)
    rules = long_rules(hseg, bw0, rect)
    regions = group_rules(rules, rect, lines)
    cand = [r for r in regions if r["n"] >= MIN_GROUP]
    # 用表区反推版心
    ex = [(r["x0"], r["y0"], r["x1"], r["y1"]) for r in cand]
    bb = body_box(lines, rect, ex) or (left0, right0)
    body_left, body_right = bb
    body_width = max(body_right - body_left, 1.0)
    # 用新版心重挑线
    rules = long_rules(hseg, body_width, rect)
    regions = group_rules(rules, rect, lines)
    tables = []
    for r in regions:
        if r["n"] < MIN_GROUP:
            continue
        r["vert"] = has_vertical(page, r)
        r["cap"] = caption_pos(lines, r)
        r["width_ratio"] = (r["x1"] - r["x0"]) / body_width
        r["x0_rel"] = (r["x0"] - body_left) / body_width
        r["x1_rel"] = (r["x1"] - body_left) / body_width
        r["fig_cap"] = figure_caption_near(lines, r)
        r["small_seg"] = small_seg_count(page, r)
        r["cap_algo"] = algo_mark(lines, r)
        r["win_text"] = any_text_in_window(lines, r)
        r["n_lines"] = sum(1 for (lx0, ly0, lx1, ly1, lt) in lines
                           if lt.strip() and r["y0"] < (ly0 + ly1) / 2.0 < r["y1"]
                           and lx1 > r["x0"] and lx0 < r["x1"])
        r["kind"] = "figure" if (r["fig_cap"] or r["small_seg"] > SMALL_SEG_MAX) else "table"
        tables.append(r)
    return {
        "body_left": body_left, "body_right": body_right, "body_width": body_width,
        "tables": tables,
    }
