"""Task 5 裁图带的复算脚本（入库；`formulas.py` docstring 里那些实测数的唯一依据）。

输出 **A–F 六张表**（复审 Minor 5：旧版首句写「四张表」，与下面列出的六项不符；
其中 §E 是旧值的口径辨析、§F 是两种取法的逐份高度分布。本脚本的 stdout 逐字存进
`tests/papers/recon/formula-band-scans.txt`）：

  A. `figures.band_of` 对**公式编号**「定不出带」的条数（docstring 的 `331/782`）；
  B. `REACH_PITCH_MULT` 取值扫描（**现行口径**：1.2→26 / 1.5→14 / 2.0→7 / 2.5→7 / 3.0→7；
     ⚠️ 这里早先写的是**被废止的旧数** `1.2→223 / 3.0→11`，本轮按复审 Minor 1 改成现行值，
     旧值的口径辨析在 §E）；
  C. 可达域取 2.0 / 2.5 / 3.0 时「带圈进页眉/页脚」的**逐条**（docstring 的 `2/782`，
     旧数 2.5→7 / 3.0→11 同样是废止值，现行 8 / 12，差异逐条在 §C 里）；
  D. `MIN_NUM=1` 时的检出总数——`781` 这个分母从哪来；
  E. 旧表各格的**口径辨析**（1.2 那一格为什么量不到 223）；
  F. 两种取法的**逐份高度分布**（复审 Minor 5：`中位的中位` 两种取法中位数都算出来，
     免得「34.3 / 34.25」两处打架）。

**口径**（缺了它这几张表不可复算）：

* 「公式编号」= `formulas.scan(doc).picks` 的**全批检出**（每号一条，代表候选）；
  一律先 `watermark.strip_in_memory(doc)`，与 `extract_all` 取的是同一批对象，**不另加过滤**。
* **A** 的口径：把编号行表示成 `figures.Caption`（`kind="eq"`、`num`=编号、`page`=页、
  `y0`=编号行 y0、`text`=编号行原文），调 `figures.band_of(items, cap, body_size,
  page.rect, colw)`；返回值 `rect is None` 即「定不出带」。这是**代理口径**：编号行文本
  是 `(7)` 一类，`band_of` 的 `_caption_match` 认不出它，故它内部的 `own` 为空、
  `cap_y1 = cap.y0 + 1.0`——这正是 docstring 说的「`band_of` 的语义是图注、不是编号」。
  原因串里的数字在打印前被归一化成 `N`（否则同一原因会因坐标不同而分裂成上百行）。
* **B/C** 的口径：`formulas.REACH_PITCH_MULT` 逐个取值改一次（**进程内改，不落盘**），
  逐条算 `formula_band(...)`；「退化」= 返回值第 4 个布尔为 True（= 带里一件非正文实物都
  没吸收到、且编号行是「整行只有编号」）；「吞页眉的带」= 该带矩形**完整覆盖**了本页一条
  页眉行（`^\\s*(Team\\s*#|Page\\s+\\d+\\s+of\\s+\\d+)`，不分大小写）的 y 范围。
* **D**：`formulas.MIN_NUM = 1` 再数一遍检出总数（`2507817 p6 y=80.3` 那条整行 `(0)`
  就此被排除）。
* **E**：在 REACH=1.2 下另数四个候选口径（退化标志 / 未吸收 / 带高 < `figures.MIN_BAND` /
  带高 < 1.2×本页行距），并单独复算 `2504223` 一栏——用来定位旧表 1.2 那一格的口径。

**只读**：不改任何文件（`REACH_PITCH_MULT` / `MIN_NUM` 只在进程内改，脚本退出即失效）。
"""
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import fitz  # noqa: E402

from tools.papers import figures, formulas, io, textmd, watermark  # noqa: E402

HEAD = re.compile(r"^\s*(Team\s*#|Page\s+\d+\s+of\s+\d+)", re.I)
COLLECTION = "2025美赛O奖论文"
pdfs = sorted((io.ORIGIN / COLLECTION).rglob("*.pdf"))


def open_scan(pdf):
    doc = fitz.open(pdf)
    watermark.strip_in_memory(doc)
    return doc, formulas.scan(doc), textmd.body_size(doc)


def bands_of(pdf):
    """逐条产出 `(num, page, rect, basis, degenerate, page_items, body_size)`。"""
    doc, sc, bs = open_scan(pdf)
    by = {}
    for c in sc.picks:
        by.setdefault(c.page, []).append(c.as_eqnum())
    out = []
    for c in sc.picks:
        eq = c.as_eqnum()
        page = doc[eq.page]
        items, colw = figures._page_items(page)
        r, basis, _why, deg = formulas.formula_band(
            items, eq, bs, page.rect, colw, tuple(by[eq.page]))
        out.append((c.num, eq.page, r, basis, deg, items, bs))
    doc.close()
    return out


# ---------------------------------------------------------------- A
print("=" * 72)
print("A. figures.band_of 对**公式编号**「定不出带」的条数（复算 docstring 的 331/782）")
print("=" * 72)
total = degenerate = 0
reasons = Counter()
for pdf in pdfs:
    doc, sc, bs = open_scan(pdf)
    for c in sc.picks:
        eq = c.as_eqnum()
        page = doc[eq.page]
        items, colw = figures._page_items(page)
        line = formulas.number_line(items, eq)
        cap = figures.Caption("eq", c.num, eq.page,
                              line.y0 if line is not None else eq.y0,
                              line.text if line is not None else f"({c.num})")
        rect, _d, why = figures.band_of(items, cap, bs, page.rect, colw)
        total += 1
        if rect is None:
            degenerate += 1
            reasons[re.sub(r"[\d.]+", "N", why)] += 1
    doc.close()
print(f"检出总数 = {total}；band_of 定不出带 = {degenerate}（{degenerate / total * 100:.1f}%）")
for k, v in reasons.most_common(10):
    print(f"    {v:>4}  {k}")

# ---------------------------------------------------------------- B
print()
print("=" * 72)
print("B. REACH_PITCH_MULT 取值扫描（复算 docstring 的取值表）")
print("=" * 72)
rows = {}
for mult in (1.2, 1.5, 2.0, 2.5, 3.0):
    formulas.REACH_PITCH_MULT = mult
    n = deg = hdr = 0
    hs = []
    for pdf in pdfs:
        for _num, _pno, r, _basis, d, items, _bs in bands_of(pdf):
            n += 1
            deg += 1 if d else 0
            hs.append(r.height)
            for z in items:
                if (z.kind == "T" and HEAD.match(z.text)
                        and z.y0 >= r.y0 - 1 and z.y1 <= r.y1 + 1):
                    hdr += 1
                    break
    rows[mult] = (n, deg, statistics.median(hs), max(hs), hdr)
    print(f"REACH={mult}: n={n} 退化={deg} 带高中位={statistics.median(hs):.1f} "
          f"带高最大={max(hs):.1f} 吞页眉的带={hdr}")

# ---------------------------------------------------------------- C
print()
print("=" * 72)
print("C. 可达域取 2.0 / 2.5 / 3.0 时「带圈进页眉/页脚」的逐条")
print("=" * 72)
for mult in (2.0, 2.5, 3.0):
    formulas.REACH_PITCH_MULT = mult
    got = []
    for pdf in pdfs:
        for num, pno, r, _basis, _d, items, _bs in bands_of(pdf):
            for z in items:
                if (z.kind == "T" and HEAD.match(z.text)
                        and z.y0 >= r.y0 - 1 and z.y1 <= r.y1 + 1):
                    got.append(f"    {pdf.stem} ({num}) p{pno + 1} 带 y={r.y0:.1f}..{r.y1:.1f} "
                               f"吞进页眉行 y={z.y0:.1f}..{z.y1:.1f} {z.text.strip()[:50]!r}")
                    break
    print(f"REACH={mult}: 吞页眉/页脚的带 = {len(got)} 条（表 B 那一格 = {rows[mult][4]}，"
          f"必须相等）")
    for g in got:
        print(g)

# ---------------------------------------------------------------- D
print()
print("=" * 72)
print("D. `781` 这个分母从哪来：MIN_NUM=1（把 2507817 的整行 `(0)` 排除）时的检出总数")
print("=" * 72)
saved_min = formulas.MIN_NUM
formulas.MIN_NUM = 1
n1 = 0
per = {}
for pdf in pdfs:
    doc, sc, _bs = open_scan(pdf)
    n1 += len(sc.picks)
    per[pdf.stem] = len(sc.picks)
    doc.close()
formulas.MIN_NUM = saved_min
n0_2507817 = sum(1 for pdf in pdfs if pdf.stem == "2507817"
                 for _ in bands_of(pdf))
print(f"MIN_NUM=0（现行）= {total}；MIN_NUM=1（旧口径）= {n1}；差 = {total - n1}")
print(f"  2507817：MIN_NUM=0 时 {n0_2507817} 条、MIN_NUM=1 时 {per['2507817']} 条"
      f"——**旧表的分母 781 就是 MIN_NUM=1 那版的数**"
      f"（`formulas.MIN_NUM` 的 docstring 记了把整行 `(0)` 收进来的理由）")

# ---------------------------------------------------------------- E
print()
print("=" * 72)
print("E. 旧表各格的口径辨析：1.2 那一格的 223 是什么口径")
print("=" * 72)
formulas.REACH_PITCH_MULT = 1.2
deg = not_abs = lt_min = lt_pitch = n = 0
per4223 = Counter()
hs = []
for pdf in pdfs:
    for _num, _pno, r, basis, d, items, bs in bands_of(pdf):
        n += 1
        deg += 1 if d else 0
        per4223[pdf.stem] += 1 if d else 0
        if not basis.startswith("吸收"):
            not_abs += 1
        scale = figures._line_scale(items, bs)
        lt_min += 1 if r.height < figures.MIN_BAND else 0
        lt_pitch += 1 if r.height < 1.2 * scale else 0
        hs.append(r.height)
print(f"REACH=1.2（n={n}）四个候选口径：")
print(f"  ① 退化标志（现行实现的第 4 位）= {deg}")
print(f"  ② 带里没吸收到任何非正文实物（basis 不以「吸收」开头）= {not_abs}")
print(f"  ③ 带高 < figures.MIN_BAND={figures.MIN_BAND}pt = {lt_min}")
print(f"  ④ 带高 < 1.2×本页行距 = {lt_pitch}")
print(f"  带高中位 = {statistics.median(hs):.1f} 最大 = {max(hs):.1f}"
      f"（旧表那一格写的是 中位 29.1 / 最大 53.4）")
print(f"  2504223 的退化条数 = {per4223['2504223']} / 25（旧表正文写「20/25 条退化」）")
# 2504223 在旧口径（带高 < MIN_BAND）下是多少——这一条是定位口径的关键对照
p4223 = next(p for p in pdfs if p.stem == "2504223")
u = sum(1 for _n, _p, r, _b, _d, _i, _bs in bands_of(p4223) if r.height < figures.MIN_BAND)
print(f"  2504223 在**口径 ③**（带高 < MIN_BAND）下 = {u} / 25"
      f"——与旧表正文的「20/25」**逐字相符**，故旧表 1.2 那一格的"
      f"「退化」口径 = ③（含 `带高 < MIN_BAND` 那一条）")
print(f"  那个 `带高 < MIN_BAND` 分支现已被 `formula_band` **刻意删除**"
      f"（见其 docstring：单行公式的带本来就只有一个行距高），故 223 在现行代码上"
      f"只能由口径 ③ 复算得 {lt_min}（差 {lt_min - 223}）")
formulas.REACH_PITCH_MULT = 2.0

# ---------------------------------------------------------------- F
print()
print("=" * 72)
print("F. 两种取法的逐份高度分布（复审 Minor 5：`中位的中位` 的取法必须写明）")
print("=" * 72)


def per_doc_medians(doc_list):
    """逐份的 `(stem, 新取法 min, 新取法 中位, 新取法 max, 固定点法 min, 固定点法 中位,
    固定点法 max)`；中位 = `statistics.median`（口径与 `verify_d._band_heights` 同）。"""
    out = []
    for pdf in doc_list:
        doc, sc, bs = open_scan(pdf)
        hs, hs_fixed = [], []
        by_page = {}
        for c in sc.picks:
            by_page.setdefault(c.page, []).append(c.as_eqnum())
        for c in sc.picks:
            eq = c.as_eqnum()
            page = doc[c.page]
            items, colw = figures._page_items(page)
            rect, _b, _w, _d = formulas.formula_band(
                items, eq, bs, page.rect, colw, tuple(by_page[c.page]))
            hs.append(rect.height)
            line = formulas.number_line(items, eq)
            own = (fitz.Rect(line.x0, line.y0, line.x1, line.y1) if line is not None
                   else fitz.Rect(eq.x0, eq.y0, eq.x0 + 1.0, eq.y1))
            hs_fixed.append((own.y1 + 6.0) - (own.y0 - 6.0))
        doc.close()
        if hs:
            out.append((pdf.stem, min(hs), statistics.median(hs), max(hs),
                        min(hs_fixed), statistics.median(hs_fixed), max(hs_fixed)))
    return out


rowsF = per_doc_medians(pdfs)
print(f"有带的份数 = {len(rowsF)}")
for stem, mn, med, mx, fmn, fmed, fmx in rowsF:
    print(f"  {stem} 新取法 min={mn:.1f} 中位={med:.1f} max={mx:.1f} pt · "
          f"固定点法 min={fmn:.1f} 中位={fmed:.1f} max={fmx:.1f} pt")
newmed = [r[2] for r in rowsF]
fixmed = [r[5] for r in rowsF]
print(f"新取法：逐份 min 最低 = {min(r[1] for r in rowsF):.1f} · 逐份 max 最高 = "
      f"{max(r[3] for r in rowsF):.1f} · 逐份中位 的 `statistics.median` = "
      f"{statistics.median(newmed):.2f} · 逐份中位 的**上中位数**（排序后第 n//2 个）= "
      f"{sorted(newmed)[len(newmed) // 2]:.1f}")
print(f"固定点法：逐份 min 最低 = {min(r[4] for r in rowsF):.1f} · 逐份 max 最高 = "
      f"{max(r[6] for r in rowsF):.1f} · 逐份中位 的 `statistics.median` = "
      f"{statistics.median(fixmed):.2f} · 上中位数 = "
      f"{sorted(fixmed)[len(fixmed) // 2]:.1f}")
print(f"  → `formulas.py` docstring 里那句「逐份中位的中位 34.3pt / 24.0pt」用的是"
      f"**上中位数**（{sorted(newmed)[len(newmed) // 2]:.1f} / "
      f"{sorted(fixmed)[len(fixmed) // 2]:.1f}）；`statistics.median` 复算 = "
      f"{statistics.median(newmed):.2f} / {statistics.median(fixmed):.2f}"
      f"（两者**不相等**就是这个取法差异造成的）。*两种取法都印在这里*，"
      f"别混用（复审 Minor 5）。")
print()
print("注：本脚本**不改任何文件**（`REACH_PITCH_MULT` / `MIN_NUM` 只在进程内改）。")
