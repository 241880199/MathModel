#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`A` 族的**可测性探针**（`mcm-schematic` Task 2 硬要求 1 / 计划 P4）—— 不是判据，是取证。

**为什么要有它**：设计把 `A1–A4` 四条全标成**候选**（"`get_drawings()` 在这些 TikZ 产物上能不能
稳定切出节点框与箭头，没人验过"）。本探针把"能 / 不能"当场量出来，**验不出来的如实降级**
（那条降级决定与它的读数一起落盘，见 `README.md` 的「A 族可测性」段与设计 §5.1 的订正）。

**产出（只用 `print`，捕获由调用方重定向）**：

  python tests/skills/schematic/fixtures/probe-a-measurability.py > build/m3-schematic-fixtures/a-measurability.txt 2>&1

**只读**：本目录的 `*.pdf`（骨架正/反控制）· 仓内**别的载体的产物**（数据图，用来证"无条件会假红”）。
只读不写；输出**逐字**进捕获件（与 `tests/m3-*-recon/out-*.txt` 同一套纪律）。**幂等**（无时间戳/随机数）。
"""
import pathlib
import sys

import fitz

ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding="utf-8")

# 与 check-figure-style.py 的 A 族常量**同值**（探针是独立的取证件，口径要对齐才比得出）
NODE_MIN_AREA, NODE_MIN_W, NODE_MIN_H = 200.0, 10.0, 6.0
MM = 2.834645669291339
LW_OK = (0.5, 0.7, 0.9, round(0.5 * MM, 4), round(1.4 * MM, 4))
LW_TOL = 0.02


def _closed(dr):
    return bool(dr["items"]) and all(x[0] in ("l", "c", "qu", "re") for x in dr["items"])


def node_boxes(page, words):
    """README §A 族的**节点框**口径：既填充又描边 + 闭合 + 尺寸过线 + 含文字 + 不被同类框包住。"""
    cand = []
    for dr in page.get_drawings():
        t = dr.get("type") or ""
        if "f" not in t or "s" not in t or not dr.get("fill") or not _closed(dr):
            continue
        r = dr["rect"]
        if r.width < NODE_MIN_W or r.height < NODE_MIN_H or r.width * r.height < NODE_MIN_AREA:
            continue
        nt = sum(1 for w in words if r.x0 <= (w[0] + w[2]) / 2 <= r.x1 and r.y0 <= (w[1] + w[3]) / 2 <= r.y1)
        cand.append((r, nt))
    tb = [(r, n) for r, n in cand if n > 0]
    return [r for r, _ in tb
            if not any(q != r and q.width * q.height < r.width * r.height - 1
                       and q.x0 >= r.x0 - 0.5 and q.x1 <= r.x1 + 0.5
                       and q.y0 >= r.y0 - 0.5 and q.y1 <= r.y1 + 0.5 for q, _ in tb)]


def naive_boxes(page):
    """**被否掉的**节点框口径：只要"填充 + 闭合 + 面积 ≥400pt² + 宽≥18 + 高≥8"就当节点框。

    留着它是为了给"**靠几何推断这是不是示意图不可靠**"这句话**一条实测背书** —— 口径一放宽
    （去掉"要描边 / 要有字 / 要最内层"三条），**数据图**（MATLAB 产物）的图框会成批被当成节点框
    并互相报重叠。它**不是**本 skill 采用的口径。
    """
    out = []
    for dr in page.get_drawings():
        t = dr.get("type") or ""
        if "f" not in t or not dr.get("fill") or not _closed(dr):
            continue
        r = dr["rect"]
        if r.width >= 18 and r.height >= 8 and r.width * r.height >= 400:
            out.append(r)
    return out


def _point_in_poly(pt, poly):
    x, y = pt
    inside = False
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def _poly(dr):
    pts = []
    for it in dr["items"]:
        if it[0] == "l":
            pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] in ("c", "qu"):
            pts += [(it[1].x, it[1].y), (it[-1].x, it[-1].y)]
        elif it[0] == "re":
            r = it[1]
            pts += [(r.x0, r.y0), (r.x1, r.y1)]
    out = []
    for p in pts:
        if not out or abs(p[0] - out[-1][0]) > 1e-6 or abs(p[1] - out[-1][1]) > 1e-6:
            out.append(p)
    return out


def readings(path):
    with fitz.open(path) as doc:
        page = doc[0]
        rect, words, dls = page.rect, page.get_text("words"), page.get_drawings()
        boxes = node_boxes(page, words)
        # A1：节点框两两重叠（bbox 相交 > 0.5pt 两个方向）
        ov = sum(1 for i in range(len(boxes)) for j in range(i + 1, len(boxes))
                 if min(boxes[i].x1, boxes[j].x1) - max(boxes[i].x0, boxes[j].x0) > 0.5
                 and min(boxes[i].y1, boxes[j].y1) - max(boxes[i].y0, boxes[j].y0) > 0.5)
        # A3：词框越出页框（容差 0.5pt）
        bad = sum(1 for w in words if w[0] < -0.5 or w[1] < -0.5
                  or w[2] > rect.width + 0.5 or w[3] > rect.height + 0.5)
        # A4：纯描边（type=='s'）线宽 —— 外加"若把 fs 也算进来会怎样"（证伪箭头尖假红）
        s_w = sorted({round(dr.get("width") or 0, 3) for dr in dls if (dr.get("type") or "") == "s"})
        all_w = sorted({round(dr.get("width") or 0, 3) for dr in dls
                        if "s" in (dr.get("type") or "")})
        off_s = [w for w in s_w if min(abs(w - a) for a in LW_OK) > LW_TOL]
        off_all = [w for w in all_w if min(abs(w - a) for a in LW_OK) > LW_TOL]
        # A2 的**两种失败量法**（探针要证它们假红）：
        #   ① bbox 法：非填充闭合块（含菱形）当节点框，线段端点落在其 bbox 内
        polys = [(_poly(dr), dr["rect"]) for dr in dls
                 if _closed(dr) and "f" in (dr.get("type") or "") and dr.get("fill")]
        segs = [(it[1], it[2]) for dr in dls if (dr.get("type") or "") == "s"
                for it in dr["items"] if it[0] == "l"]
        a2_bbox = 0
        for p, q in segs:
            for r in boxes:
                for pt in (p, q):
                    if r.x0 + 0.5 < pt.x < r.x1 - 0.5 and r.y0 + 0.5 < pt.y < r.y1 - 0.5:
                        a2_bbox += 1
        a2_poly = 0
        for p, q in segs:
            for poly, _r in polys:
                for pt in (p, q):
                    if _point_in_poly((pt.x, pt.y), poly):
                        a2_poly += 1
        return dict(n_draw=len(dls), n_box=len(boxes), a1_ov=ov, a3_bad=bad, n_words=len(words),
                    a4_off_s=off_s, a4_off_all=off_all, a2_bbox=a2_bbox, a2_poly=a2_poly)


def main():
    print("=" * 100)
    print("A 族可测性探针 · mcm-schematic Task 2 · 命令：python tests/skills/schematic/fixtures/probe-a-measurability.py")
    print("=" * 100)
    print("段 1 · 骨架（A 族要判的产物）：`A1`/`A3`/`A4` 应全 0；`A2` 的两种量法**应当暴露假红**")
    print("-" * 100)
    print("%-28s %6s %6s %6s %6s %6s  %-22s  %s" % (
        "产物", "draw", "box", "A1ov", "A3bad", "words", "A4off(纯描边)", "A2假红(bbox/点-多边形)"))
    for p in sorted(HERE.glob("*.pdf")):
        r = readings(p)
        print("%-28s %6d %6d %6d %6d %6d  %-22s  %d/%d" % (
            p.name, r["n_draw"], r["n_box"], r["a1_ov"], r["a3_bad"], r["n_words"],
            str(r["a4_off_s"]), r["a2_bbox"], r["a2_poly"]))
    print()
    print("段 2 · `A4` 的\"只取纯描边\"这条窄化是承重的（把 `fs` 也算进来 ⇒ 箭头尖的 pgf 线宽越界）")
    print("-" * 100)
    for p in sorted(HERE.glob("*.pdf")):
        r = readings(p)
        if r["a4_off_all"] != r["a4_off_s"]:
            print("  %-28s 纯描边越界 %s ；把 fs 也算进来 ⇒ 越界 %s" % (p.name, r["a4_off_s"], r["a4_off_all"]))
    print()
    print("段 3 · `--schematic` 门控是承重的：同一套量法落到**别的载体的产物**上（数据图）会假红")
    print("-" * 100)
    others = (sorted((ROOT / "tests/skills/plot-python/green").glob("out-G*/figure.pdf"))
              + sorted((ROOT / "tests/skills/plot-matlab/green").glob("out-G*/figure.pdf"))
              + sorted((ROOT / "tests/skills/figure-choose/fixtures").glob("ok-0*.pdf")))
    print("  （这些产物**不该**被 A 族碰 —— 它们是数据图，A 族的家要它们全绿）")
    for p in others:
        r = readings(p)
        rel = p.relative_to(ROOT).as_posix()
        print("  %-58s box=%2d A1ov=%2d A3bad=%d A4off(纯描边)=%s A4off(含fs)=%s" % (
            rel, r["n_box"], r["a1_ov"], r["a3_bad"], r["a4_off_s"], r["a4_off_all"]))
    print()
    print("段 4 · \"靠几何**推断**这是不是示意图\"不可靠（实测反例）：口径一放宽 ⇒ 数据图的图框成批入集合")
    print("-" * 100)
    print("  （口径 = naive_boxes()：填充+闭合+面积≥400pt²+宽≥18+高≥8，**不要**描边 / 文字 / 最内层三条；")
    print("    它不是本 skill 的口径 —— 这里只用来给\"推断不可靠\"一句实测背书）")
    for p in others:
        with fitz.open(p) as doc:
            page = doc[0]
            nb = naive_boxes(page)
            nov = sum(1 for i in range(len(nb)) for j in range(i + 1, len(nb))
                      if min(nb[i].x1, nb[j].x1) - max(nb[i].x0, nb[j].x0) > 0.5
                      and min(nb[i].y1, nb[j].y1) - max(nb[i].y0, nb[j].y0) > 0.5)
        print("  %-58s naive 节点框 %2d 个 ⇒ 若拿它判 `A1` 会报重叠 %2d 处" % (
            p.relative_to(ROOT).as_posix(), len(nb), nov))
    print()
    print("读法（结论见 README.md 的「A 族可测性」段）：")
    print("  · 段 1：`A1`/`A3`/`A4`（纯描边口径）在**全部骨架**上读到 0 —— 三条可测、且对合法产物不假红；")
    print("  · 段 1 的 `A2` 两列在 `mechanism-block` / `pipeline-branch` 上**不是 0** ⇒ 两种量法都在")
    print("    **合法骨架**上假红 ⇒ `A2` 降级到「看一眼」层（不是\"没做\"，是\"做了会乱红\"）；")
    print("  · 段 2：`A4` 若不排除 `fs`，箭头尖的 pgf 线宽（0.861）当场越界 ⇒ \"只取纯描边\"这条窄化承重；")
    print("  · 段 3：`A4` 的允许集合是**示意样式**的 ⇒ 同一套量法打到数据图产物上是**别的数值**")
    print("    （实测 plot-python out-G2 的纯描边宽 0.6 越界）⇒ 无条件跑会把一张该全绿的数据图判红；")
    print("  · 段 4：`A1` 的\"节点框\"靠几何推断**也不可靠**（放宽口径 ⇒ MATLAB 数据图的图框成批入集合）。")
    print("  ⇒ 合起来：判据的射程由**调用方声明**（`--schematic`），不由几何推断。")


if __name__ == "__main__":
    main()
