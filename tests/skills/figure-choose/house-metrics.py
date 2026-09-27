#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`house-style.md` / `provenance.md` 里**每个实测数的复跑仪器**——一条命令给一个数。

用法：
  python tests/skills/figure-choose/house-metrics.py --metric h1_med
  python tests/skills/figure-choose/house-metrics.py --list
  python tests/skills/figure-choose/house-metrics.py --metrics h1_med,h1_max

输出恒为一行 `NAME = VALUE`（数值类给 4 位小数；文本类原样）。`--list` 打名册。

## 三支仪器，别混用（这是本任务最重要的一条口径纪律）

1. **出货仪器** = `check-figure-style.py` 的 `color_count`（320×320 **NEAREST** 采样 + `//16` 分箱 +
   去近灰 `<24` + **0.5% 地板**）。本文件**import 它**、绝不抄实现（抄件会随检查器漂移）。
   前缀 `color_*` 的读数一律出自它。
2. **侦察仪器** = `quantize(colors=32, MEDIANCUT)` + 去近白(`max>=240`)/近黑(`max<=40`)/近灰(`<=24`)
   + 0.5% 地板；`tab10` 另用 `quantize(64)` + 非灰 C0–C6/C8/C9 + `TOL=3` + 占比 `>=0.3%` + 命中 `>=2`。
   前缀 `recon_*` / `tab10_*` 出自它。**它的生成器不在受版本控制的目录里**
   （`build/m3-figure-recon/probe_c_color.py` 等是未入库的工作副本）⇒ 本文件把它**重写**了一遍，
   并把「与入库台账逐格一致」做成读数（`recon_ledger_match` / `tab10_v2_ledger_match`），
   一旦重写漂了就当场不是 662。
3. **几何仪器** = PNG 像素 ÷ 200 dpi（渲染 dpi 是构造已知，不读元信息）。宽高比 = 宽/高。
   前缀 `h1_*` / `h3_*`。**比值分母** = 43 篇正文行宽 p90 的全局中位（见 `h2_colw_p90_median`，H2 写死）。

## 不是"尺子"的部分

`f2_*` 只用来看**连续色图会不会把 F2 的条数变成地板切连续谱的产物**（H4 的射程界定），
它 import `red/f2-diagnose.py` 的取箱重写件并逐例断言与出货 `color_count` 一致。
`probe_*` 是"一个图文件 = 一页"的两页探针读数（H4 上文 §交付形态）。

## 修复轮改掉的两处口径

1. **`recon_baseline_minw_*`（Critical-1）**：原先那支"转写口径"漏了 baseline §7 的 **`//16` 分箱**
   ⇒ 在 662 图上算得 48.79%，被写成了"57.2% 未能复现"。补回分箱后：**166 抽样 = 57.23%**
   （与 baseline §7 的 `median=4.0 / zero%=15.7 / <=4占比=57.2%` 逐格相同）、662 图 = **51.81%**。
   **57.2% 是可复现的**；它之所以不能与 72.9% 对举，是因为转写件与真侦察仪器有**两处**口径差
   （`min>=240` vs `max>=240`、**分箱** vs **不分箱**）。
2. **`cont_*` 闸门（Important-3）**：旧闸门 `箱数≥20 且 最高落选箱≥0.3%` 的**箱数那一半形同虚设**
   （95.62% 过），"最高落选箱"那一半**两方向都不站得住**（真热力图低到 0.094% < 离散标定件 R1 的
   0.127%）。改成 `箱数 ≥ CONT_BOX_MIN` **或** `最高落选箱 ≥ CONT_SUBFLOOR_MIN_PCT`；
   代价是命中率由 49.40% 升到 72.81%（已写进 H4 正文）。
"""
import argparse
import csv
import glob
import importlib.util
import math
import pathlib
import re
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[3]
HERE = pathlib.Path(__file__).resolve().parent
DPI = 200.0                                     # 渲染 dpi（构造已知，见 figure-style-baseline.txt §3）
CORPUS = ROOT / "corpus/papers/figures/2025美赛O奖论文"
POOL = 8                                        # quantize/PIL 是 C 层，放线程池里真并行
# H4 的"连续色图"保守闸门（标定样本仅 3 张 R1/R2/R3，见 provenance P-H4-h）：两个常数由
# check-house-style.py 钉住，闸门形态是 `箱数 >= CONT_BOX_MIN` **或** `最高落选箱 >= CONT_SUBFLOOR_MIN_PCT`
# ——两个默认值都是**实测重标定**出来的（旧值 20 / 0.3 的实测否证见 provenance P-H4-h）：
#   · 旧值 20 形同虚设：全 662 里 95.62% 过这一关（只有 29 张 <20 箱）；
#   · 旧值 0.3 漏掉真热力图：语料里图注带 `heatmap` 的图，最高落选箱低到 0.094%（< 离散标定件 R1 的 0.127%）。
CONT_BOX_MIN = 100                              # 未设地板时的彩色箱数下限（旧值 20，实测形同虚设）
CONT_SUBFLOOR_MIN_PCT = 0.4                     # 最高落选箱占比下限（%）（旧值 0.3，实测漏真热力图）
CONT_BOX_VACUOUS_MAX = 20                       # 旧闸门的箱数下限（**只**用来复算"旧闸门"的读数，不参与判定）
CONT_SUBFLOOR_OLD_PCT = 0.3                     # 旧闸门的最高落选箱下限（%，同上）

# H12 的〔社区〕规则值——**本仓没有任何实测可依**（侦察报告 §7.3 明说量不到）。登记在这里**不是**
# 当作读数，而是让"把它悄悄改掉"这件事**会红**（复审 N-8：原先 ≥7 pt 改成 ≥6 pt 一路全绿）。
# 判据形态是 `const:`（文档 == 这里的常量），**不是**"文档 == 实测"。
H12_FONT_SCALE_LO = 0.8                         # 图内字号 = 正文的 0.8–1.0×（社区值）
H12_FONT_SCALE_HI = 1.0                         # 同上右端（社区值）
H12_FONT_MIN_PT = 7                             # 图内字号最小 ≥7 pt（社区值）


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CHECKER = _load(HERE / "check-figure-style.py", "check_figure_style")   # 出货仪器（只 import，不改）
F2DIAG = _load(HERE / "red/f2-diagnose.py", "f2_diagnose")              # 取箱重写件（自带 tripwire）

FIGS = sorted(glob.glob(str(ROOT / "corpus/papers/figures/**/fig-*.png"), recursive=True))
CAPS = sorted(CORPUS.rglob("fig-*.caption.txt"))
JUDGE = ROOT / "tests/figures-recon/a-judgment-rand120.tsv"
PIXEL = ROOT / "tests/figures-recon/c7-pixel-criteria.tsv"
COLW = ROOT / "tests/figures-recon/b-colwidth.tsv"
COLORLED = ROOT / "tests/figures-recon/c-color-count.tsv"
TABLED = ROOT / "tests/figures-recon/c6-tab10-v2.tsv"
FONTLED = ROOT / "tests/figures-recon/d9-fontsize-experiment.tsv"
MULTIPAGE = HERE / "red/multipage-probe.pdf"
R2PDF = HERE / "red/out-R2/figure.pdf"

_recon_cache, _memo = {}, {}


def _paper(path):
    return pathlib.Path(path).parts[-2]


def _aspect_of(rel):
    with Image.open(CORPUS / rel) as im:
        return im.size[0] / im.size[1]


def _q(xs, p):
    """线性插值分位（与侦察的 `stats_b.py` / `probe_c8_caption.py` 同法）。"""
    xs = sorted(xs)
    i = p * (len(xs) - 1)
    lo, hi = int(i), min(int(i) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def _pmap(fn, items):
    with ThreadPoolExecutor(POOL) as ex:
        return list(ex.map(fn, items))


# ------------------------------------------------------------------ 几何
def _wh():
    def one(f):
        with Image.open(f) as im:
            return im.size
    return _pmap(one, FIGS)


def colwidths():
    """43 篇的正文行宽 p90（英寸）。b-colwidth.tsv 是入库台账。"""
    rows = COLW.read_text(encoding="utf-8").splitlines()[1:]
    return {r.split("\t")[0]: float(r.split("\t")[5]) for r in rows if r.strip()}


def n_other_papers():
    """未建索引的其余合集份数（H 文件头"其余 158 份未抽取"的来源）。

    口径：读入库索引 `corpus/papers/INDEX.md` 的"未建索引=其余 N 个合集（X 份）：A 44 · B 42 · …"一行，
    **要求声明的 X 等于各分项之和**（不等就返回 -1，让守卫红）。
    """
    txt = (ROOT / "corpus/papers/INDEX.md").read_text(encoding="utf-8")
    m = re.search(r"未建索引=其余 \d+ 个合集（(\d+) 份）：([^\n]*)", txt)
    if not m:
        raise LookupError("INDEX.md 里抽不到「未建索引」那一行（fail-closed）")
    parts = [int(x) for x in re.findall(r"\s(\d+)(?=\s·|\s*$)", m.group(2))]
    return float(m.group(1)) if sum(parts) == int(m.group(1)) else -1.0


def h2_colw_p90_median():
    return round(st.median(colwidths().values()), 4)


def h2_colw_p90_mean():
    """**不是** H2 的分母——这是 M10 用的对照口径（把 p90 换成均值会怎样）。"""
    return round(st.mean(colwidths().values()), 4)


def _ratios(per_paper=False):
    cw = colwidths()
    den = cw if per_paper else {p: h2_colw_p90_median() for p in cw}
    return [w / DPI / den[_paper(f)] for (w, _h), f in zip(_wh(), FIGS)]


# ------------------------------------------------------------------ 配色
def _shipped_colors():
    if "shipped" not in _recon_cache:
        def one(f):
            with Image.open(f) as im:
                return CHECKER.color_count(im.convert("RGB"))
        _recon_cache["shipped"] = _pmap(one, FIGS)
    return _recon_cache["shipped"]


RECON_TAB10 = [(0x1F, 0x77, 0xB4), (0xFF, 0x7F, 0x0E), (0x2C, 0xA0, 0x2C), (0xD6, 0x27, 0x28),
               (0x94, 0x67, 0xBD), (0x8C, 0x56, 0x4B), (0xE3, 0x77, 0xC2), (0x7F, 0x7F, 0x7F),
               (0xBC, 0xBD, 0x22), (0x17, 0xBE, 0xCF)]


def _quant_colors(path, q, near_white, near_black, floor, want, bin16=False):
    """侦察仪器的公共件：quantize(q, MEDIANCUT) 后的有意义色（含占比）。

    `want="colors"` 给主色列表；`want="tab10"` 给严判据命中数（`TOL=3`、非灰 C0–C6/C8/C9、`>=0.3%`）；
    `want="loose_hits"` 给松判据命中数（`TOL=40`、含 C7 灰，同 `probe_c_color.py`）。
    `bin16=True` = **再走一遍 `//16` 分箱**——**只有** baseline §7 的转写口径才这么做
    （真侦察仪器 `probe_c_color.py` 数的是**不同调色板项**，不分箱；见 provenance P-H4-g）。
    """
    with Image.open(path) as im0:
        im = im0.convert("RGB")
        n = im.width * im.height
        small = im.quantize(colors=q, method=Image.Quantize.MEDIANCUT).convert("RGB")
        counts = {}
        for cnt, col in small.getcolors(q):
            counts[col] = counts.get(col, 0) + cnt
    if bin16:
        # 先按**原色**过闸（近白/近黑/近灰），再 `//16` 分箱合并（= baseline §7 转写口径 `v6` 的次序）
        binned = {}
        for col, cnt in counts.items():
            if near_white(col) or near_black(col) or max(col) - min(col) <= 24:
                continue
            k = (col[0] // 16, col[1] // 16, col[2] // 16)
            binned[k] = binned.get(k, 0) + cnt
        counts = binned
    out = []
    for col, cnt in counts.items():
        if not bin16 and (near_white(col) or near_black(col) or max(col) - min(col) <= 24):
            continue
        if cnt / n < floor:
            continue
        out.append((col, cnt / n))
    if want == "colors":
        return out
    if want == "loose_hits":
        return sum(1 for col, _frac in out
                   if min(math.dist(col, tc) for tc in RECON_TAB10) <= 40.0)
    seen = set()                      # 与 probe_c6_tab10_v2.py 同：命中记的是**色序号集合**
    for col, frac in out:
        if frac < 0.003:
            continue
        for i in range(10):
            if i != 7 and math.dist(col, RECON_TAB10[i]) <= 3.0:
                seen.add(i)
                break
    return len(seen)


def _recon(kind):
    if kind not in _recon_cache:
        black40 = lambda c: max(c) <= 40
        if kind == "c32":
            fn = lambda p: len(_quant_colors(p, 32, lambda c: max(c) >= 240, black40, 0.005, "colors"))
        elif kind == "c32_minw":          # baseline §7 的转写口径（`min>=240` **且** `//16` 分箱）
            fn = lambda p: len(_quant_colors(p, 32, lambda c: min(c) >= 240, black40, 0.005,
                                             "colors", bin16=True))
        elif kind == "tab_strict":
            fn = lambda p: _quant_colors(p, 64, lambda c: max(c) >= 245, lambda c: max(c) <= 25,
                                         0.003, "tab10")
        else:                             # tab_loose = probe_c_color.py 的 tab10 判据（TOL=40）
            fn = lambda p: _quant_colors(p, 32, lambda c: max(c) >= 240, black40, 0.005, "loose_hits")
        _recon_cache[kind] = _pmap(fn, FIGS)
    return _recon_cache[kind]


def _ledger_match(kind):
    """重写件与入库台账逐格一致数（662 = 一致；漂一格就不等于 662）。"""
    if kind == "c32":
        led = {r.split("\t")[0]: int(r.split("\t")[2]) for r in
               COLORLED.read_text(encoding="utf-8").splitlines()[1:] if r.strip()}
        mine = _recon("c32")
        return sum(1 for f, v in zip(FIGS, mine)
                   if led.get(pathlib.Path(f).relative_to(CORPUS).as_posix()) == v)
    if kind == "c32_loose":
        led = {r.split("\t")[0]: r.split("\t")[4] for r in
               COLORLED.read_text(encoding="utf-8").splitlines()[1:] if r.strip()}
        want = lambda h: "tab10" if h >= 2 else ("tab10_partial" if h == 1 else "not_tab10")
        mine = _recon("tab_loose")
        return sum(1 for f, v in zip(FIGS, mine)
                   if led.get(pathlib.Path(f).relative_to(CORPUS).as_posix()) == want(v))
    led = {}
    for r in TABLED.read_text(encoding="utf-8").splitlines()[1:]:
        f = r.split("\t")
        if len(f) >= 6:
            led[f[0]] = (int(f[2]), f[5])
    mine = _recon("tab_strict")
    return sum(1 for f, v in zip(FIGS, mine)
               if led.get(pathlib.Path(f).relative_to(CORPUS).as_posix(), (None,))[0] == v)


# ------------------------------------------------------------------ 判断层 / 图注
def _judge():
    with open(JUDGE, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def _pixel():
    out = {}
    for line in PIXEL.read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("\t")
        if len(f) >= 8:
            out[f[0]] = {"grid": int(f[2]), "legend": int(f[5]), "multi": int(f[7])}
    return out


LABEL = re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*(\d+)\s*([:.：．。]?)", re.I)
F3A = re.compile(r"^Figure\s+\d+\s*:")
CAPTION3D = re.compile(r"3\s*-?\s*D|three[- ]dimensional", re.I)
_cap_cache = {}


def _caps():
    if not _cap_cache:
        rows = []
        for p in CAPS:
            t = p.read_bytes().decode("utf-8")
            m = LABEL.match(t)
            punct = m.group(2) if m else ""
            body = t[len(m.group(0)):].strip() if m else t
            rows.append({"path": p.relative_to(CORPUS).as_posix(), "text": t, "punct": punct,
                         "body": body, "words_full": len(t.split()), "words_body": len(body.split())})
        _cap_cache["rows"] = rows
    return _cap_cache["rows"]


# ------------------------------------------------------------------ 两页探针 / F2 边界
def _probe():
    if "probe" not in _memo:
        import fitz
        with fitz.open(MULTIPAGE) as doc:
            pages = doc.page_count
            p2w = doc[1].rect.width / 72.0 if pages > 1 else float("nan")
            p1w = doc[0].rect.width / 72.0
        pm = None
        with fitz.open(MULTIPAGE) as doc:
            pm = doc[1].get_pixmap(dpi=CHECKER.RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
        p2c = CHECKER.color_count(Image.frombytes("RGB", (pm.width, pm.height), pm.samples))
        with fitz.open(MULTIPAGE) as doc:
            pm1 = doc[0].get_pixmap(dpi=CHECKER.RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
        p1c = CHECKER.color_count(Image.frombytes("RGB", (pm1.width, pm1.height), pm1.samples))
        _memo["probe"] = {"pages": pages, "p2w": p2w, "p2c": p2c, "p1w": p1w, "p1c": p1c}
    return _memo["probe"]


def _boxes_of(pdf):
    """取箱重写件（`red/f2-diagnose.py`）的读数；与出货 `color_count` 逐例一致才出数。"""
    key = f"boxes:{pdf.parent.name}/{pdf.name}"        # 三个探针都叫 figure.pdf ⇒ 键必须带目录名
    if key not in _memo:
        rgb = CHECKER.raster_rgb(pdf)
        tot, keep = F2DIAG.boxes(rgb)
        shares = sorted((c / tot for c in keep.values()), reverse=True)
        over = [s for s in shares if s >= 0.005]
        if len(over) != CHECKER.color_count(rgb):          # 与出货检查器逐例一致（漂了就不出数）
            raise RuntimeError("取箱重写件与 color_count 不一致（fail-closed）")
        below = [s for s in shares if s < 0.005]
        _memo[key] = {"n": len(shares), "counted": len(over),
                      "subfloor": max(below) if below else float("nan"),
                      "lowest": min(over) if over else float("nan")}
    return _memo[key]


def _r2boxes():
    return _boxes_of(R2PDF)


def _r1boxes():
    return _boxes_of(HERE / "red/out-R1/figure.pdf")


# ------------------------------------------------------------------ H4 的连续色图闸门（实测重标定）
HEATCAP = re.compile(r"heat\s*-?\s*map", re.I)
SEEDS_120 = (0, 1, 7, 42, 2792, 20260927)       # 复算"120 张抽样的宽高比中位"用的固定种子集


def _f2all():
    """全 662 图的**取箱**读数（与出货 `color_count` 逐例一致才出数）。"""
    if "f2all" not in _memo:
        def one(f):
            rgb = CHECKER.raster_rgb(pathlib.Path(f))
            tot, keep = F2DIAG.boxes(rgb)
            shares = sorted((c / tot for c in keep.values()), reverse=True)
            over = [s for s in shares if s >= 0.005]
            if len(over) != CHECKER.color_count(rgb):          # 逐例一致（漂了就不出数）
                raise RuntimeError("取箱重写件与 color_count 不一致（fail-closed）")
            below = [s for s in shares if s < 0.005]
            return {"n": len(shares), "counted": len(over),
                    "subfloor": max(below) if below else 0.0}
        _memo["f2all"] = _pmap(one, FIGS)
    return _memo["f2all"]


def _cont_hit(d):
    """新闸门：箱数 ≥CONT_BOX_MIN **或** 最高落选箱 ≥CONT_SUBFLOOR_MIN_PCT%。"""
    return d["n"] >= CONT_BOX_MIN or (d["n"] > 0 and d["subfloor"] * 100 >= CONT_SUBFLOOR_MIN_PCT)


def _cont_hit_old(d):
    """旧闸门（**只**用来复算"旧闸门命中多少"的读数，不参与判定）：箱数 ≥20 **且** 最高落选箱 ≥0.3%。"""
    return d["n"] >= CONT_BOX_VACUOUS_MAX and d["subfloor"] * 100 >= CONT_SUBFLOOR_OLD_PCT


def _heat_idx():
    """图注带 `heatmap` 的图在 FIGS 里的下标（正则 `heat\\s*-?\\s*map`，可复跑）。

    注意 `_caps()` 的 `path` 是**图注文件**的相对路径（`…fig-N-pM.caption.txt`），
    要映射回 `…fig-N-pM.png` 才能与 FIGS 对齐。
    """
    caps = {c["path"].replace(".caption.txt", ".png"): c["text"] for c in _caps()}
    return [i for i, f in enumerate(FIGS)
            if HEATCAP.search(caps.get(pathlib.Path(f).relative_to(CORPUS).as_posix(), ""))]


def _fig_index(rel):
    """按语料相对路径取 FIGS 下标；找不到即抛（fail-closed）。"""
    p = str(CORPUS / rel)
    if p not in FIGS:
        raise LookupError(f"语料里没有这张图：{rel}（fail-closed）")
    return FIGS.index(p)


def _cov4_pct(vals):
    return round(100 * sum(1 for v in vals if v <= 4) / len(vals), 2)


def _zero_pct(vals):
    return round(100 * sum(1 for v in vals if v == 0) / len(vals), 2)


def _comp_counts():
    return [d["counted"] for d in _f2all() if not _cont_hit(d)]


# ------------------------------------------------------------------ N-5：908 池上的 120 抽样宽高比
ALLPNG = sorted(glob.glob(str(ROOT / "corpus/papers/figures/**/*.png"), recursive=True))


def _aspects(paths):
    out = []
    for p in paths:
        with Image.open(p) as im:
            out.append(im.size[0] / im.size[1])
    return out


def _s120_meds():
    import random
    out = []
    for s in SEEDS_120:
        rng = random.Random(s)
        out.append(round(st.median(_aspects(rng.sample(ALLPNG, 120))), 4))
    return out


# ------------------------------------------------------------------ 名册
def _reg():
    R = {}

    def add(name, fn, note):
        R[name] = (fn, note)

    # 几何：H1/H2/H3
    add("n_figs", lambda: len(FIGS), "样本图数（fig-*.png）")
    add("n_papers", lambda: len(colwidths()), "样本份数（b-colwidth.tsv 行数）")
    add("n_other_papers", n_other_papers, "未建索引的其余合集份数（读 corpus/papers/INDEX.md，且与其分项和自洽）")
    add("n_tabs", lambda: len(glob.glob(str(ROOT / "corpus/papers/figures/**/tab-*.png"), recursive=True)),
        "同批抽到的表数（tab-*.png，不在射程）")
    add("n_png_all", lambda: len(ALLPNG), "908 = 662 图 + 246 表的 PNG 总数（H3 差异登记里的『908 池』）")
    add("h1_p25", lambda: round(_q(_ratios(), 0.25), 4), "662 图宽比值 p25")
    add("h1_med", lambda: round(st.median(_ratios()), 4), "662 图宽比值中位")
    add("h1_p75", lambda: round(_q(_ratios(), 0.75), 4), "662 图宽比值 p75")
    add("h1_max", lambda: round(max(_ratios()), 4), "662 图宽比值 max")
    add("h1_band_pct", lambda: round(100 * sum(1 for x in _ratios() if 0.80 <= x <= 1.20) / len(FIGS), 2),
        "落在出货 F1 区间 [0.80,1.20] 内的占比")
    add("h1_below_pct", lambda: round(100 * sum(1 for x in _ratios() if x < 0.80) / len(FIGS), 2),
        "低于 0.80 的占比")
    add("h1_above_pct", lambda: round(100 * sum(1 for x in _ratios() if x > 1.20) / len(FIGS), 2),
        "高于 1.20 的占比")
    add("h2_colw_p90_median", h2_colw_p90_median, "43 篇正文行宽 p90 的全局中位（H2 的分母）")
    add("h2_colw_p90_mean", h2_colw_p90_mean, "同上但取均值（M10 对照口径，不作分母）")
    add("h2_colw_p90_max", lambda: round(max(colwidths().values()), 2), "同上的 max（右尾）")
    add("h2_colw_p90_gap", lambda: round(h2_colw_p90_mean() - h2_colw_p90_median(), 4),
        "均值 − 中位的差（P-H2-b 的说明性数字，由 PROV_GUARDS 守）")
    add("h2_fork_global_pct", lambda: round(100 * sum(1 for x in _ratios() if 0.9 <= x < 1.1) / len(FIGS), 2),
        "全局分母 6.31 下落在 [0.9,1.1) 的占比")
    add("h2_fork_perpaper_pct",
        lambda: round(100 * sum(1 for x in _ratios(True) if 0.9 <= x < 1.1) / len(FIGS), 2),
        "逐篇 p90 作分母时同一区间的占比")
    add("h3_land_pct", lambda: round(100 * sum(1 for w, h in _wh() if w / h >= 1) / len(FIGS), 2),
        "横图（宽高比 >=1）占比")
    add("h3_below1_pct", lambda: round(100 * sum(1 for w, h in _wh() if w / h < 1) / len(FIGS), 2),
        "竖图（宽高比 <1）占比")
    add("h3_aspect_med", lambda: round(st.median([w / h for w, h in _wh()]), 4), "宽高比中位")
    add("h3_ge2_pct", lambda: round(100 * sum(1 for w, h in _wh() if w / h >= 2) / len(FIGS), 2),
        "宽高比 >=2 占比")
    add("h3_in_band_pct", lambda: round(100 * sum(1 for w, h in _wh() if 2 <= w / h <= 3) / len(FIGS), 2),
        "宽高比落在常见带 [2,3] 的占比")
    add("h3_h_med", lambda: round(st.median([h / DPI for _w, h in _wh()]), 4), "图高中位（in）")
    add("h3_h_p25", lambda: round(_q([h / DPI for _w, h in _wh()], 0.25), 4), "图高 p25（in）")
    add("h3_h_p75", lambda: round(_q([h / DPI for _w, h in _wh()], 0.75), 4), "图高 p75（in）")
    add("h3_aspect_p25", lambda: round(_q([w / h for w, h in _wh()], 0.25), 4), "宽高比 p25")
    add("h3_aspect_p75", lambda: round(_q([w / h for w, h in _wh()], 0.75), 4), "宽高比 p75")
    add("h3_legacy_2427",
        lambda: round(_aspect_of("A/2500836/fig-07-p9.png"), 4),
        "入库证据里唯一等于 2.427 的**单张**读数（设计稿那个 2.42 的来源**不是**它——见 h3_aspect_s120_*）")
    add("h3_aspect_pool908_med", lambda: round(st.median(_aspects(ALLPNG)), 4),
        "908 张 PNG（662 图 + 246 表）的宽高比中位")
    add("h3_aspect_s120_med_lo", lambda: min(_s120_meds()),
        "在同一个 908 池里按固定种子集重抽 120 张，宽高比中位的**最小**值（2.42 不可复跑的证据）")
    add("h3_aspect_s120_med_hi", lambda: max(_s120_meds()),
        "同上，宽高比中位的**最大**值")

    # 配色：H4/H5
    add("color_median", lambda: float(st.median(_shipped_colors())), "出货仪器主色数中位")
    add("color_zero_n", lambda: sum(1 for c in _shipped_colors() if c == 0), "出货仪器零彩色张数")
    add("color_zero_pct",
        lambda: round(100 * sum(1 for c in _shipped_colors() if c == 0) / len(FIGS), 2), "出货仪器零彩色占比")
    add("color_cov4_n", lambda: sum(1 for c in _shipped_colors() if c <= 4), "出货仪器 ≤4 覆盖张数")
    add("color_cov4_pct",
        lambda: round(100 * sum(1 for c in _shipped_colors() if c <= 4) / len(FIGS), 2), "出货仪器 ≤4 覆盖率")
    add("recon_median", lambda: float(st.median(_recon("c32"))), "侦察仪器主色数中位")
    add("recon_zero_pct",
        lambda: round(100 * sum(1 for c in _recon("c32") if c == 0) / len(FIGS), 2), "侦察仪器零彩色占比")
    add("recon_cov4_n", lambda: sum(1 for c in _recon("c32") if c <= 4), "侦察仪器 ≤4 覆盖张数")
    add("recon_cov4_pct",
        lambda: round(100 * sum(1 for c in _recon("c32") if c <= 4) / len(FIGS), 2), "侦察仪器 ≤4 覆盖率")
    add("recon_ledger_match", lambda: _ledger_match("c32"), "重写件 vs c-color-count.tsv 的 n_sig_colors 逐格一致数")
    add("recon_baseline_minw_cov4_pct",
        lambda: _cov4_pct(_recon("c32_minw")),
        "baseline §7 的转写口径（min>=240 + //16 分箱）在同一 662 图上的 ≤4 覆盖率")
    add("recon_baseline_minw_s166_cov4_pct",
        lambda: _cov4_pct(_recon("c32_minw")[::4]),
        "同上转写口径，但收在 **166 张抽样**（每 4 取 1）上——baseline §7 的 57.2% 的**原抽样**")
    add("recon_baseline_minw_s166_median",
        lambda: float(st.median(_recon("c32_minw")[::4])),
        "同上转写口径在 166 抽样上的主色中位（baseline §7 报 4.0）")
    add("recon_baseline_minw_s166_zero_pct",
        lambda: _zero_pct(_recon("c32_minw")[::4]),
        "同上转写口径在 166 抽样上的零彩色占比（baseline §7 报 15.7）")
    add("recon_cov4_s166_pct",
        lambda: _cov4_pct(_recon("c32")[::4]),
        "**真侦察仪器**（max>=240、不分箱）在同一 166 抽样上的 ≤4 覆盖率（与转写口径 57.2% 对照）")
    add("tab10_strict_n", lambda: sum(1 for h in _recon("tab_strict") if h >= 2), "严判据命中张数")
    add("tab10_strict_pct",
        lambda: round(100 * sum(1 for h in _recon("tab_strict") if h >= 2) / len(FIGS), 2), "严判据命中占比")
    add("tab10_loose_n", lambda: sum(1 for h in _recon("tab_loose") if h >= 2), "松判据命中张数")
    add("tab10_loose_pct",
        lambda: round(100 * sum(1 for h in _recon("tab_loose") if h >= 2) / len(FIGS), 2), "松判据命中占比")
    add("tab10_v2_ledger_match", lambda: _ledger_match("tab_strict"), "严判据重写件 vs c6-tab10-v2.tsv 逐格一致数")
    add("tab10_loose_ledger_match", lambda: _ledger_match("c32_loose"),
        "松判据重写件 vs c-color-count.tsv 的 tab10_verdict 栏逐格一致数")
    add("f2_r2_counted", lambda: _r2boxes()["counted"], "连续红蓝发散热图在 F2 下的条数")
    add("f2_r2_boxes", lambda: _r2boxes()["n"], "同一张图的（未设地板）彩色箱数")
    add("f2_r2_subfloor_max_pct", lambda: round(_r2boxes()["subfloor"] * 100, 3), "最高落选箱占比 %")
    add("f2_r2_lowest_counted_pct", lambda: round(_r2boxes()["lowest"] * 100, 3), "最低入选箱占比 %")
    add("f2_r2_margin_pp",
        lambda: round((0.005 - _r2boxes()["subfloor"]) * 100, 3), "最高落选箱离 0.5% 地板的富余（pp）")
    add("f2_r1_subfloor_max_pct",
        lambda: round(_boxes_of(HERE / "red/out-R1/figure.pdf")["subfloor"] * 100, 3),
        "离散配色图 R1 的最高落选箱（对照：不该被判成连续色图）")
    add("f2_r3_subfloor_max_pct",
        lambda: round(_boxes_of(HERE / "red/out-R3/figure.pdf")["subfloor"] * 100, 3),
        "离散配色图 R3 的最高落选箱（对照）")

    # 连续色图闸门（H4）：新旧两版在**同一批图**上的读数
    add("cont_gate_pct", lambda: round(100 * sum(1 for d in _f2all() if _cont_hit(d)) / len(FIGS), 2),
        "**新**闸门（箱数 ≥100 或 最高落选箱 ≥0.4%）在 662 图上的命中率")
    add("cont_gate_old_pct",
        lambda: round(100 * sum(1 for d in _f2all() if _cont_hit_old(d)) / len(FIGS), 2),
        "**旧**闸门（箱数 ≥20 且 最高落选箱 ≥0.3%）在同一 662 图上的命中率（对照）")
    add("cont_box20_pass_pct",
        lambda: round(100 * sum(1 for d in _f2all() if d["n"] >= CONT_BOX_VACUOUS_MAX) / len(FIGS), 2),
        "旧闸门那条『箱数 ≥20』的腿**放进来了多少张**（形同虚设的证据）")
    add("cont_box20_below_n",
        lambda: sum(1 for d in _f2all() if d["n"] < CONT_BOX_VACUOUS_MAX),
        "旧闸门那条腿真正挡住了多少张（<20 箱）")
    add("cont_heat_den", lambda: len(_heat_idx()), "图注带 heatmap 的图数（正则 heat\\s*-?\\s*map）")
    add("cont_heat_hit_n",
        lambda: sum(1 for i in _heat_idx() if _cont_hit(_f2all()[i])),
        "新闸门在这组 heatmap 图上命中多少张")
    add("cont_heat_hit_old_n",
        lambda: sum(1 for i in _heat_idx() if _cont_hit_old(_f2all()[i])),
        "旧闸门在这组 heatmap 图上命中多少张（对照）")
    add("cont_cite_den",
        lambda: sum(1 for i in _heat_idx() if _f2all()[i]["counted"] > 4),
        "这组 heatmap 图里 **F2 条数 >4**（会被当离散读数引用）的张数")
    add("cont_cite_n",
        lambda: sum(1 for i in _heat_idx()
                    if _f2all()[i]["counted"] > 4 and _cont_hit(_f2all()[i])),
        "新闸门在那组『条数会被引用』的 heatmap 图里命中多少张")
    add("cont_cite_old_n",
        lambda: sum(1 for i in _heat_idx()
                    if _f2all()[i]["counted"] > 4 and _cont_hit_old(_f2all()[i])),
        "旧闸门在那组『条数会被引用』的 heatmap 图里命中多少张（漏检的证据）")
    add("cont_heat_subfloor_min_pct",
        lambda: round(100 * min(_f2all()[i]["subfloor"] for i in _heat_idx()
                                if _f2all()[i]["counted"] > 4), 3),
        "那组图里**最低**的最高落选箱（%）：比离散标定件 R1 还低 ⇒ 这条线不区分连续/离散")
    add("cont_ratio_disc", lambda: round(_r1boxes()["n"] / _r1boxes()["counted"], 2),
        "离散标定件 R1 的『箱数 ÷ 条数』（证『箱数 ≫ 条数』这条判据方向是反的）")
    add("cont_ratio_heat",
        lambda: round(_f2all()[_fig_index("B/2517929/fig-10-p19.png")]["n"]
                      / _f2all()[_fig_index("B/2517929/fig-10-p19.png")]["counted"], 2),
        "真热力图 B/2517929/fig-10-p19 的同一条比值（< 离散件）")
    add("cont_comp_n", lambda: len(_comp_counts()), "闸门补集（未被判为连续色图）的张数")
    add("cont_ex1_f2", lambda: _f2all()[_fig_index("B/2517929/fig-10-p19.png")]["counted"],
        "旧闸门漏掉的真热力图 #1（B/2517929/fig-10-p19）的 F2 条数")
    add("cont_ex1_sub_pct",
        lambda: round(100 * _f2all()[_fig_index("B/2517929/fig-10-p19.png")]["subfloor"], 3),
        "同图的最高落选箱（%）")
    add("cont_ex2_f2", lambda: _f2all()[_fig_index("C/2505964/fig-08-p13.png")]["counted"],
        "旧闸门漏掉的真热力图 #2（C/2505964/fig-08-p13）的 F2 条数")
    add("cont_ex2_sub_pct",
        lambda: round(100 * _f2all()[_fig_index("C/2505964/fig-08-p13.png")]["subfloor"], 3),
        "同图的最高落选箱（%）——比离散标定件 R1 的 0.127% 还低")
    add("color_median_comp", lambda: float(st.median(_comp_counts())), "补集上的出货仪器主色中位")
    add("color_zero_pct_comp", lambda: _zero_pct(_comp_counts()), "补集上的零彩色占比")
    add("color_cov4_pct_comp", lambda: _cov4_pct(_comp_counts()), "补集上的 ≤4 覆盖率")

    # 判断层 + 像素判据：H6/H7/H8/H11
    add("judge_n", lambda: len(_judge()), "判断层抽样张数")
    add("judge_pie_n", lambda: sum(1 for r in _judge() if r["pie"] == "y"), "判断层判为饼图的张数")
    add("judge_pie_pct", lambda: round(100 * sum(1 for r in _judge() if r["pie"] == "y") / len(_judge()), 2),
        "判断层饼图占比")
    add("judge_3d_n", lambda: sum(1 for r in _judge() if r["three_d"] == "y"), "判断层判为 3D 的张数")
    add("judge_3d_pct", lambda: round(100 * sum(1 for r in _judge() if r["three_d"] == "y") / len(_judge()), 2),
        "判断层 3D 占比")
    add("judge_mp_n", lambda: sum(1 for r in _judge() if r["multi_panel"] == "y"), "判断层判为多面板的张数")
    add("judge_mp_pct",
        lambda: round(100 * sum(1 for r in _judge() if r["multi_panel"] == "y") / len(_judge()), 2),
        "判断层多面板占比")
    add("mp_agree_n", lambda: sum(1 for r in _judge()
                                 if r["path"] in _pixel()
                                 and (r["multi_panel"] == "y") == (_pixel()[r["path"]]["multi"] == 1)),
        "多面板：判断层 vs 像素判据的一致张数")
    add("legend_agree_n", lambda: sum(1 for r in _judge()
                                      if r["path"] in _pixel()
                                      and (r["legend"] == "y") == (_pixel()[r["path"]]["legend"] == 1)),
        "图例：判断层 vs 像素判据的一致张数")
    add("color_cov4_sample166_pct",
        lambda: round(100 * sum(1 for c in _shipped_colors()[::4] if c <= 4) / len(_shipped_colors()[::4]), 2),
        "出货仪器在 166 张抽样（每 4 张取 1）上的 ≤4 覆盖率（Task 1 §7 的同一抽样）")
    add("mp_agree_pct",
        lambda: round(100 * sum(1 for r in _judge()
                               if r["path"] in _pixel()
                               and (r["multi_panel"] == "y") == (_pixel()[r["path"]]["multi"] == 1))
                     / sum(1 for r in _judge() if r["path"] in _pixel()), 2),
        "多面板：判断层 vs 像素判据的一致率")
    add("pixel_mp_n", lambda: sum(1 for k, v in _pixel().items() if "/fig-" in k and v["multi"] == 1),
        "多面板：像素判据命中张数")
    add("pixel_mp_pct",
        lambda: round(100 * sum(1 for k, v in _pixel().items()
                                if "/fig-" in k and v["multi"] == 1)
                      / sum(1 for k in _pixel() if "/fig-" in k), 2),
        "多面板：像素判据在 662 图上的读数")
    add("legend_agree_pct",
        lambda: round(100 * sum(1 for r in _judge()
                               if r["path"] in _pixel()
                               and (r["legend"] == "y") == (_pixel()[r["path"]]["legend"] == 1))
                     / sum(1 for r in _judge() if r["path"] in _pixel()), 2),
        "图例：判断层 vs 像素判据的一致率（证废用）")
    add("grid_reading_pct",
        lambda: round(100 * sum(1 for k, v in _pixel().items()
                                if "/fig-" in k and v["grid"] == 1)
                      / sum(1 for k in _pixel() if "/fig-" in k), 2),
        "网格：像素判据在 662 图上的读数（不是结论）")

    # 图注：H9
    add("cap_n", lambda: len(_caps()), "图注条数（fig-*.caption.txt）")
    add("cap_cut_pct", lambda: round(100 * sum(1 for c in _caps() if LABEL.match(c["text"])) / len(_caps()), 2),
        "标签可机械切出的占比（宽松前缀）")
    add("cap_f3a_n", lambda: sum(1 for c in _caps() if F3A.match(c["text"].strip())), "出货 F3a 严格匹配张数")
    add("cap_f3a_pct", lambda: round(100 * sum(1 for c in _caps() if F3A.match(c["text"].strip())) / len(_caps()), 2),
        "出货 F3a 严格匹配（`^Figure <n>:`）的占比")
    add("cap_ascii_colon_n", lambda: sum(1 for c in _caps() if c["punct"] == ":"), "ASCII 冒号条数")
    add("cap_ascii_colon_pct",
        lambda: round(100 * sum(1 for c in _caps() if c["punct"] == ":") / len(_caps()), 2), "ASCII 冒号占比")
    add("cap_ascii_period_n", lambda: sum(1 for c in _caps() if c["punct"] == "."), "ASCII 句点条数")
    add("cap_ascii_colon_or_period_n",
        lambda: sum(1 for c in _caps() if c["punct"] in (":", ".")),
        "ASCII 冒号**或**句点条数（= 侦察报告 §4.4『合计用 ASCII `:`/`.`』的口径）")
    add("cap_ascii_colon_or_period_pct",
        lambda: round(100 * sum(1 for c in _caps() if c["punct"] in (":", ".")) / len(_caps()), 2),
        "同一更宽口径的占比（设计稿那个 87.3% 的真口径）")
    add("cap_noperiod_n",
        lambda: sum(1 for c in _caps() if not c["text"].strip().endswith(".")), "句末无句号条数")
    add("caption_3d_n", lambda: sum(1 for c in _caps() if CAPTION3D.search(c["text"])), "图注口径的 3D 张数")
    add("n_sample166", lambda: len(FIGS[::4]), "166 张抽样的抽样量（每 4 张取 1）")
    add("f2_floor_pct", lambda: round(F2DIAG.FLOOR * 100, 4), "F2 的噪声地板（%），取自 red/f2-diagnose.py 的 FLOOR")
    add("grid_reading_n",
        lambda: sum(1 for k, v in _pixel().items() if "/fig-" in k and v["grid"] == 1), "网格：像素判据命中张数")
    add("cap_words_med", lambda: float(st.median([c["words_body"] for c in _caps()])), "正文词数中位")
    add("cap_words_p25", lambda: round(_q([c["words_body"] for c in _caps()], 0.25), 4), "正文词数 p25")
    add("cap_words_p75", lambda: round(_q([c["words_body"] for c in _caps()], 0.75), 4), "正文词数 p75")
    add("cap_words_p95", lambda: round(_q([c["words_body"] for c in _caps()], 0.95), 4), "正文词数 p95")
    add("cap_words_max", lambda: float(max(c["words_body"] for c in _caps())), "正文词数上界")
    add("cap_noperiod_pct",
        lambda: round(100 * sum(1 for c in _caps() if not c["text"].strip().endswith(".")) / len(_caps()), 2),
        "句末无句号的占比")
    add("cap_empty_n", lambda: sum(1 for c in _caps() if c["words_full"] == 2), "空图注张数（只有 `Figure N:`）")
    add("cap_empty_f3d_n",
        lambda: sum(1 for c in _caps() if not CHECKER.caption_body(c["text"].strip())),
        "空图注里被 F3d 抓到的张数")
    add("caption_3d_pct",
        lambda: round(100 * sum(1 for c in _caps() if CAPTION3D.search(c["text"])) / len(_caps()), 2),
        "图注口径的 3D 占比（本任务自定判据面）")

    # 字号：H12
    add("font_est_n", lambda: _fontvals()[1], "d9 台账里可用张数")
    add("font_est_pt_min", lambda: min(_fontvals()[0]), "PNG 连通域反推字号的 min（pt）")
    add("font_est_pt_max", lambda: max(_fontvals()[0]), "PNG 连通域反推字号的 max（pt）")

    # 交付形态探针
    add("probe_pages", lambda: _probe()["pages"], "multipage-probe.pdf 的页数")
    add("probe_page1_w_in", lambda: round(_probe()["p1w"], 4), "探针 page1 页盒宽（in）")
    add("probe_page2_w_in", lambda: round(_probe()["p2w"], 4), "探针 page2 页盒宽（in）")
    add("probe_page1_colors", lambda: _probe()["p1c"], "探针 page1 的 F2 读数")
    add("probe_page1_ratio", lambda: round(_probe()["p1w"] / h2_colw_p90_median(), 4),
        "探针 page1 的 F1 比值（分母 = 6.3099，故恰 1.000）")
    add("probe_page2_colors", lambda: _probe()["p2c"], "探针 page2 的 F2 读数")
    add("probe_verdict", lambda: _probe_verdict(), "整份探针在出货检查器下的判词（PASS/FAIL）")
    return R


def _fontvals():
    if "font" not in _memo:
        rows = [r.split("\t") for r in FONTLED.read_text(encoding="utf-8").splitlines()[1:] if r.strip()]
        v = [round(float(r[2]), 4) for r in rows if len(r) > 2 and r[2]]
        _memo["font"] = (v, len(v))
    return _memo["font"]


def _probe_verdict():
    import subprocess
    p = subprocess.run([sys.executable, str(HERE / "check-figure-style.py"),
                        "--fig", "tests/skills/figure-choose/red/multipage-probe.pdf",
                        "--caption", "Figure 1: A two page probe", "--textwidth-in", "6.31"],
                       capture_output=True, text=True, cwd=str(ROOT))
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "(无判词)"
    return last.replace("RESULT: ", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metric")
    ap.add_argument("--metrics")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    R = _reg()
    if a.list:
        for k, (_f, note) in R.items():
            print(f"{k}\t{note}")
        return 0
    names = ([a.metric] if a.metric else []) + ([s for s in a.metrics.split(",") if s] if a.metrics else [])
    if not names:
        print("FAIL: 需要 --metric <name> 或 --metrics a,b（fail-closed）", file=sys.stderr)
        return 2
    bad = 0
    for n in names:
        if n not in R:
            print(f"FAIL: 名册里没有 {n}（fail-closed）", file=sys.stderr)
            bad += 1
            continue
        v = R[n][0]()
        print(f"{n} = {v:.4f}" if isinstance(v, float) else f"{n} = {v}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
