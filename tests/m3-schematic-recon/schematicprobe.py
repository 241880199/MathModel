#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""schematicprobe.py —— `mcm-schematic` 侦察用的**共享取数库**（只读 corpus）。

与 `tests/m3-table-recon/tableprobe.py` 同形：把"从一页 PDF 里量一张示意图"拆成可独立复核的几步。

**本模块的核心事实（Task 0 实测所得，见 README）**：
  论文层的图**绝大多数是位图贴入** ⇒ 几何路线只对**矢量图**可用；本模块因此把每张图先判
  `raster` / `vector` / `tiny-vector` / `table` / `none`，**再**决定能不能量。

复用（**真复用，不是重写**）：
  * `tableprobe`（同仓 `tests/m3-table-recon/`）的 `text_lines` / `analyze_page`（版心、表区）。
  * `tests/skills/figure-choose/check-figure-style.py` 的 `color_count`（F2 度量）·
    `caption_body`（F3b 口径）· `page_font_split`（F6 口径）。用 importlib 按路径加载（文件名带 `-`）。

**口径不声称穷尽。** 每条判据的阈值都写死在这里（改 = 改探针）。
"""
import os
import re
import sys
import importlib.util

import fitz

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "tests", "m3-table-recon"))
import tableprobe as tp                                    # noqa: E402

# ---- 判据阈值（**全部写死在这里，改 = 改探针**）----------------------------
CAP_RE = re.compile(r"^\s*(?:Figure|FIGURE|Fig\.?)\s*([0-9]{1,2})\s*[:.．]")
FIG_BAND_PT = 330.0        # caption 之上多少 pt 内找图（超出 ⇒ 归上一张 caption 的带）
MIN_REGION_W = 30.0        # 图区最小宽（pt）
MIN_REGION_H = 30.0        # 图区最小高（pt）
MIN_REGION_AREA = 8000.0   # 图区最小面积（pt^2）
VEC_MIN_ITEMS = 3          # 判"矢量图"的最小路径条目数（描点/框线都算条目；零散线已被尺寸阈值挡掉）
CLUSTER_GAP_X = 18.0       # drawing 簇合并容差（x）
CLUSTER_GAP_Y = 14.0       # drawing 簇合并容差（y）
CAPTION_RULE_MAX_H = 2.0   # 页内整宽细线（>=0.7 页宽且高 < 此值）不当图元
TABLE_OVERLAP_FRAC = 0.5   # 图区与表区重叠面积 / 图区面积 >= 此值 ⇒ 判为 table（排除）
RASTER_DPI = 150           # 区域栅格化密度（与 check-figure-style 的 F2 同口径）

# ---- 懒加载 check-figure-style.py（文件名的连字符不能 import）-------------
_CHK = None


def _checker():
    global _CHK
    if _CHK is None:
        p = os.path.join(REPO, "tests", "skills", "figure-choose", "check-figure-style.py")
        spec = importlib.util.spec_from_file_location("_cfs", p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _CHK = mod
    return _CHK


def color_count(im):
    """F2 的彩色主色数（**直接复用** check-figure-style.color_count）。"""
    return _checker().color_count(im)


def caption_body(cap):
    """F3b 的图注正文口径（去 `Figure N:` 前缀；**直接复用**）。"""
    return _checker().caption_body(cap)


def page_font_split(doc):
    """F6 的内嵌字体口径（**直接复用** check-figure-style.page_font_split）。"""
    return _checker().page_font_split(doc)


def page_fonts(doc, pno):
    """单页的 (内嵌字体集, 只引用未内嵌字体集) —— 与 F6 同口径（名字剥子集前缀）。"""
    chk = _checker()
    emb, ref = set(), set()
    for rec in doc.get_page_fonts(pno):
        name = chk.SUBSET_RE.sub("", rec[3])
        (emb if chk.font_embedded(doc, rec[0], rec[2]) else ref).add(name)
    return emb, ref


def f6_verdict(doc, pno):
    """按 F6 的三态给单页判词：('PASS'|'FAIL'|'N/A', 说明)。"""
    chk = _checker()
    emb, ref = page_fonts(doc, pno)
    if not emb:
        return ("N/A", "未内嵌任何字体（只引用：%s）" % (sorted(ref) if ref else "无"))
    ok = all(any(k in f for k in chk.FONT_FAMILY_OK) for f in emb)
    return ("PASS" if ok else "FAIL", "内嵌 %s" % sorted(emb))


def sample_index(n_total, n_sample, offset=0):
    """均匀系统抽样：返回 [offset, offset+step, ...] 取前 n_sample 个（无随机数）。"""
    if n_total <= 0:
        return []
    step = max(1, n_total // n_sample)
    return list(range(offset, n_total, step))[:n_sample]


# ---- 图区定位 -------------------------------------------------------------
def captions(page):
    """返回页上 `Figure N:` 起首的图注行 [(x0,y0,x1,y1,text,num)]（按 y 排序）。"""
    out = []
    for (x0, y0, x1, y1, t) in tp.text_lines(page):
        m = CAP_RE.match(t or "")
        if m:
            out.append((x0, y0, x1, y1, t, int(m.group(1))))
    out.sort(key=lambda r: r[1])
    return out


def _is_page_rule(page, r):
    return r.width > 0.7 * page.rect.width and r.height < CAPTION_RULE_MAX_H


def drawings_cluster(page, top, bot, anchor="bottom"):
    """区间 top..bot 内的 drawings：从**最靠近 caption** 的那条起，邻接连成簇。

    anchor='bottom'（caption 在图**下方**）：种子 = y1 最大者。
    anchor='top'   （caption 在图**上方**）：种子 = y0 最小者。
    返回 (bbox, n_items) 或 None。bbox = [x0,y0,x1,y1]。
    """
    drs = []
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.y1 < top or r.y0 > bot:
            continue
        if _is_page_rule(page, r):
            continue
        if r.width < 0.5 and r.height < 0.5:
            continue
        drs.append((r, len(dr["items"])))
    if not drs:
        return None
    drs.sort(key=(lambda t: -t[0].y1) if anchor == "bottom" else (lambda t: t[0].y0))
    seed = drs[0][0]
    box = [seed.x0, seed.y0, seed.x1, seed.y1]
    nitems = drs[0][1]
    used = {0}
    changed = True
    while changed:
        changed = False
        for i, (r, ni) in enumerate(drs):
            if i in used:
                continue
            if (r.x0 - CLUSTER_GAP_X <= box[2] and box[0] - CLUSTER_GAP_X <= r.x1
                    and r.y0 - CLUSTER_GAP_Y <= box[3] and box[1] - CLUSTER_GAP_Y <= r.y1):
                box = [min(box[0], r.x0), min(box[1], r.y0),
                       max(box[2], r.x1), max(box[3], r.y1)]
                nitems += ni
                used.add(i)
                changed = True
    return box, nitems


def image_block(page, top, bot, anchor="bottom"):
    """区间 top..bot 内、最靠近 caption 的位图 block 的 bbox；无则 None。

    anchor='bottom'：取 y1 最大者（caption 在图下方）。anchor='top'：取 y0 最小者。
    """
    best = None
    for b in page.get_text("dict").get("blocks", []):
        if b.get("type") != 1:
            continue
        x0, y0, x1, y1 = b["bbox"]
        if y1 < top or y0 > bot:
            continue
        if (x1 - x0) < MIN_REGION_W or (y1 - y0) < MIN_REGION_H:
            continue
        if best is None:
            best = (x0, y0, x1, y1)
        elif anchor == "bottom":
            if y1 > best[3]:
                best = (x0, y0, x1, y1)
        else:
            if y0 < best[1]:
                best = (x0, y0, x1, y1)
    return best


def _overlap_frac(bb, regions):
    """bb 与若干 region 的重叠面积 / bb 面积（最大者）。"""
    x0, y0, x1, y1 = bb
    a = max((x1 - x0) * (y1 - y0), 1.0)
    best = 0.0
    for (rx0, ry0, rx1, ry1) in regions:
        ox = max(0.0, min(x1, rx1) - max(x0, rx0))
        oy = max(0.0, min(y1, ry1) - max(y0, ry0))
        best = max(best, ox * oy / a)
    return best


def _pick(page, top, bot, anchor):
    """在区间 top..bot 里挑一个图元：矢量簇 vs 位图，取**离 caption 更近**的那个。

    返回 (bbox, n_items, kind) 或 None。
    """
    cl = drawings_cluster(page, top, bot, anchor)
    im = image_block(page, top, bot, anchor)
    if cl and im:
        if anchor == "bottom":
            use_cl = cl[0][3] >= im[3]
        else:
            use_cl = cl[0][1] <= im[1]
    else:
        use_cl = bool(cl)
    if use_cl:
        bbox, nitems = cl[0], cl[1]
        kind = "vector" if nitems >= VEC_MIN_ITEMS else "tiny-vector"
        return bbox, nitems, kind
    if im:
        return list(im), 0, "raster"
    return None


def figure_records(page, table_regions=()):
    """把一页拆成若干「图」记录。

    返回 [dict(page, cap, num, kind, bbox, ...)]；kind ∈
      raster      —— 位图贴入（几何不可量；但能栅格化量色 / 量宽度）
      vector      —— 矢量图（几何可量）
      tiny-vector —— 只有少量矢量图元（多半是分隔线/边角，**不成图**）
      table       —— 与表区重叠 >= TABLE_OVERLAP_FRAC（是表不是图，**排除**）
      none        —— 找不到任何图元
    ★ 判据不声称穷尽。
    """
    out = []
    caps = captions(page)
    for i, (x0, y0, x1, y1, text, num) in enumerate(caps):
        above_top = max((caps[i - 1][3] if i > 0 else 0.0), y0 - FIG_BAND_PT)
        below_bot = min((caps[i + 1][1] if i + 1 < len(caps) else page.rect.y1), y1 + FIG_BAND_PT)
        cand = _pick(page, above_top, y0, "bottom") or _pick(page, y1, below_bot, "top")
        if cand is None:
            out.append({"page": page.number, "num": num, "cap": text, "kind": "none",
                        "bbox": None, "n_items": 0})
            continue
        bbox, nitems, kind = cand
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w < MIN_REGION_W or h < MIN_REGION_H or w * h < MIN_REGION_AREA:
            kind = "tiny-vector" if kind != "raster" else "raster"
        if table_regions and _overlap_frac(bbox, table_regions) >= TABLE_OVERLAP_FRAC:
            kind = "table"
        out.append({"page": page.number, "num": num, "cap": text, "kind": kind,
                    "bbox": bbox, "n_items": nitems})
    return out


# ---- 区域读数 -------------------------------------------------------------
def region_rgb(page, bbox, dpi=RASTER_DPI):
    """把图区栅格化成 PIL RGB 图（供 F2 数色）。"""
    from PIL import Image
    r = fitz.Rect(*bbox)
    if r.width <= 0 or r.height <= 0:
        return None
    pm = page.get_pixmap(clip=r, dpi=dpi, colorspace=fitz.csRGB, alpha=False)
    if pm.width < 1 or pm.height < 1:
        return None
    return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)


def region_color_count(page, bbox):
    """图区的 F2 彩色主色数（复用 check-figure-style.color_count）。"""
    im = region_rgb(page, bbox)
    if im is None:
        return None
    return color_count(im)


def region_is_mono(page, bbox):
    """图区是否「单色系」：F2 口径下彩色主色数 <= MONO_MAX_COLORS。"""
    n = region_color_count(page, bbox)
    if n is None:
        return None
    return n <= MONO_MAX_COLORS


MONO_MAX_COLORS = 1        # 单色系 = 彩色主色数 <= 1（F2 口径的显著非彩色主色）


def region_vector_features(page, bbox):
    """矢量图区的几何特征（只对 kind=vector 有意义）。"""
    x0, y0, x1, y1 = bbox
    w = max(x1 - x0, 1.0)
    f = {"n_rect": 0, "n_small": 0, "n_long": 0, "n_curve": 0, "n_items": 0, "n_text": 0}
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.x1 < x0 - 4 or r.x0 > x1 + 4 or r.y1 < y0 - 4 or r.y0 > y1 + 4:
            continue
        for it in dr["items"]:
            f["n_items"] += 1
            k = it[0]
            if k == "re":
                rr = it[1]
                if rr.width > 10 and rr.height > 8:
                    f["n_rect"] += 1
            elif k == "l":
                p1, p2 = it[1], it[2]
                L = ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5
                if L <= 6.0:
                    f["n_small"] += 1
                elif L >= 0.4 * w:
                    f["n_long"] += 1
            elif k in ("c", "qu"):
                f["n_curve"] += 1
    for (lx0, ly0, lx1, ly1, t) in tp.text_lines(page):
        cx, cyy = (lx0 + lx1) / 2.0, (ly0 + ly1) / 2.0
        if x0 - 2 <= cx <= x1 + 2 and y0 - 2 <= cyy <= y1 + 2 and (t or "").strip():
            f["n_text"] += 1
    return f


def caption_words(text):
    """F3b 口径的图注词数（正文口径）。"""
    return len(caption_body((text or "").strip()).split())


def body_width_of(page):
    """版心宽 —— **与 table 那支同一支仪器**（tableprobe.analyze_page['body_width']）。"""
    try:
        return tp.analyze_page(page)["body_width"]
    except Exception:
        lines = tp.text_lines(page)
        bb = tp.body_box(lines, page.rect)
        return (bb[1] - bb[0]) if bb else None


def table_regions_of(page):
    """页上表区（用 tableprobe 判）。"""
    try:
        return [(t["x0"], t["y0"], t["x1"], t["y1"])
                for t in tp.analyze_page(page)["tables"] if t["kind"] == "table"]
    except Exception:
        return []
