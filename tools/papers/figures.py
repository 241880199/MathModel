"""按图注定位抽取图表：图注旁的内容带 **整区渲染** 成 PNG，图注另存 `.caption.txt`。

矢量图与位图统一处理，**不逐图判断类型**（实测两种都有，逐图判断会漏）；
整区渲染对两种一视同仁。

**渲染前必须 `strip_in_memory(doc)`**——水印是覆盖层（独立 Form XObject，压在
正文与图表之上），不摘掉会被烤进产出的 PNG。这一步只改内存对象，不写回原件。

## 与设计文档的一处实测出入（2026-09-24 发现，必须登记）

设计文档与计划草案都写「取图注**上方**内容区整区渲染」（草案 `_band_above` 只往
上看）。**实测这条对表格是错的**：本语料里表格的题注**多数在表格上方**
（`2501909` 的 Table 2/3/4 都在表格上方，题注下方 5.6pt 处就是表格的框线），
只有图的题注在下方。照「只往上看」做，`2501909` 那几张表的带高实测为 **0pt**
（往上第一件实物就是正文段落行，被"正文行判定"当场挡住）——产出直接缺失。

故本模块**按内容侧定带的方向**，判法是两步（见 `band_of` 的 docstring，两步都是
被实测逼出来的）：

1. 两侧**紧邻**的那件实物里，只有一侧不是"正文段落行"（`_is_flow_text`）→ 取那一侧；
2. 两侧都不是 / 两侧都是 → 取**空隙更小**的那一侧。

这是**结构性的**：不需要"图在上、表在下"这类先验，也不需要任何方向常量——
两种排版约定自动分开。每次运行的方向分布与跳过数在 `c-report.txt` 里重算。

## 内容带的边界怎么定（不给固定常数）

从图注出发往内容侧走，逐件实物（图片 bbox / drawings 的 rect / 文本行 bbox）：

* **第一跳**允许跨过"图注与实物之间的留白"（实测 0.3–21pt，因篇而异）；
* 之后的**相邻两件之间的空隙**超过 `GAP_PITCH_MULT × 本页正文行距` 即停——
  行距是**该页自己的量**（正文行的 y0 中位间距），不是全局常量；
* 反向的守卫是**正文行判定**（`_is_flow_text`）：整幅宽 × 正文字号的行视为正文
  段落，遇到即停（否则会一路爬进上方正文，实测 `2500836` p6 那种"段落最后一行
  紧贴图片上沿"的版式没有空隙可用）。

带的近端取**第一件实物的边**（不是图注的边），于是带里不含图注本身——图注另存
`.caption.txt`，两者不重复。

## 已知边界（如实登记，不声称解决）

1. **题注与表体之间没有可分辨的空隙时，`_is_flow_text` 会误停在表体的第一行**。
   `2500836` p8 的 Table 2 是无框线的算法步骤表，其行是整幅宽的正文号文本行
   （实测 w=469.4 / 列宽 595），与正文段落**在几何上不可分**。该类图注会被记为
   「跳过」，并**逐条写进 `FigResult.skipped` 与报告**——不静默、不抹平。
   实测条数见 `c-report.txt`（每次运行重算）。
2. **无标点式图注（`Figure 1 Our Work`）与正文引用句（`Figure 3 depicts …`）只靠
   「数字后第一个字符是不是大写/数字」分开**。本语料 43 份上这条实测 **100% 分对**
   （逐条读过，见模块 `_BARE_CAP` 的注释）；但它是**形态规则**，全量 201 份上
   若出现 `Figure 3 The results …` 这类以大写词开头的正文引用句，会被误当图注。
   届时判据 C1 抓不住（两侧用同一份规格），只能靠人读报告——**登记为已知风险**。
3. **一行里并列两条图注**（实测 `2507817` p21 的 `Figure 18 Cross-Validation Diagram
   Figure 19 Plot of vs. Model Coefficients` 同处一行）只会认第一条（正则锚在行首）。
   第二条**不被计数、不产出**——C1 两侧同口径，故不报红。真实条数会少算。
"""
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import fitz

from . import watermark

# 图注的三种形态（**逐条实测过**，不是猜的；覆盖数见模块 docstring 与 c-report.txt）：
#   1. ASCII 冒号/点号   `Figure 1: xxx` / `Table 1. xxx`        —— 809 条（43 份）
#   2. 全角冒号/句点     `Figure 2：xxx` / `Figure 11．xxx`       —— 12 条，4 份
#   3. 无标点式          `Figure 1 Our Work` / `Table12  xxx`     —— 需靠字首大小写分流
#
# 第 3 条**不得带全局 `re.I`**：`[A-Z0-9]` 会被一并放宽成小写，于是
# `Figure 3 depicts …`（正文引用句）也命中。2026-09-24 第一版就栽在这里，
# 实测把 176 条候选全判成图注。词首用**局部** flag `(?i:…)`，字符类保持大小写敏感。
CAPTION_FORMS = (
    re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*(\d+)\s*[:.]", re.I),
    re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*(\d+)\s*[：．。]", re.I),
    re.compile(r"^\s*(?i:figure|fig\.|table)\s*(\d+)\s+[A-Z0-9]"),
)

# 相邻实物之间的空隙超过「本页正文行距 × 这个倍数」就断开。
# 行距逐页量（`_line_scale`），所以这里不是"绝对值 vs 逐篇变化的量"那一类缺陷；
# 倍数本身是形态取舍：实测表内行距≈正文行距，段间留白≈0–2 倍行距。
GAP_PITCH_MULT = 1.2
# 第一跳（跨过图注与实物之间的留白）的上限，同样以本页行距为单位。
# 实测该留白 0.3–30.3pt；不设上限时图注上方很远处的一个图片会把带拉到页顶。
FIRST_JUMP_MULT = 3.0# `_is_flow_text`：字号与本篇正文号之差 <= 这个容差、且行宽 >= 列宽的这个比例
# → 判为正文段落行。容差与 `textmd.body_size` 的字号四舍五入粒度同量级（0.1），
# 取 0.6 是为了容下同一名义字号在不同字体度量下的落值（实测 11.9/12.0 成对出现）。
SIZE_TOL = 0.6
COLW_FRAC = 0.6
# 内容带的最小高度。**这是本模块唯一的回退常数**，覆盖面实测并登记在
# c-report.txt（`h<MIN_BAND` 的图注逐条列出）。低于它的带只可能是误判。
MIN_BAND = 20.0
# 找不到行距时的兜底行距（pt）。仅在该页没有任何正文号文本行时用到。
FALLBACK_PITCH = 13.4


@dataclass
class Caption:
    """一条图注。字段是 Task 4 任务书钉死的接口。"""
    kind: str      # "fig" | "tab"
    num: int
    page: int      # 0 起
    y0: float
    text: str


@dataclass
class FigResult:
    """抽取结果。

    `skipped` **是自述**（哪条图注没产出、为什么），**不是 C1 的依据**——
    C1 用 `verify_c.py` 里独立数出来的图注数比对。自述只在报告里做"逐条登记"。
    额外字段带默认值，故任务书钉死的 `n_fig` / `n_tab` 两个字段的用法不变。
    """
    n_fig: int
    n_tab: int
    skipped: tuple[str, ...] = ()


@dataclass
class _Item:
    """版面实物：图片 bbox、drawings 的 rect、文本行 bbox。"""
    kind: str      # "T" | "I" | "D"
    x0: float
    y0: float
    x1: float
    y1: float
    size: float = 0.0
    text: str = ""


def _caption_match(text: str) -> tuple[str, int] | None:
    """行文本 → (kind, num)；不是图注返回 None。三种形态见 `CAPTION_FORMS`。"""
    if not text:
        return None
    for rx in CAPTION_FORMS:
        m = rx.match(text)
        if m:
            label = m.group(0).lstrip().lower()
            # 只看行首那个词：`table` → 表，`figure`/`fig.` → 图
            kind = "tab" if label.startswith("tab") else "fig"
            return kind, int(m.group(1))
    return None


def caption_blocks(doc: fitz.Document) -> list[Caption]:
    """按**行**找图注。**调用方必须已经 `strip_in_memory` 过**。

    不 strip 的话水印 Form XObject 的文本块（实测 72pt、跨半页）会混进版面实物
    列表，把内容带的边界算错。
    """
    out: list[Caption] = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"]).strip()
                hit = _caption_match(t)
                if hit:
                    out.append(Caption(hit[0], hit[1], pno, line["bbox"][1], t))
    return out


def _page_items(page: fitz.Page) -> tuple[list[_Item], float]:
    """该页的版面实物列表（按 y1 升序）与列宽。"""
    items: list[_Item] = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") == 0:
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"]).strip()
                if not t:
                    continue
                items.append(_Item(
                    "T", line["bbox"][0], line["bbox"][1],
                    line["bbox"][2], line["bbox"][3],
                    round(max(s["size"] for s in line["spans"]), 1), t,
                ))
        else:
            r = b["bbox"]
            items.append(_Item("I", r[0], r[1], r[2], r[3]))
    for dr in page.get_drawings():
        r = dr["rect"]
        items.append(_Item("D", r.x0, r.y0, r.x1, r.y1))
    items.sort(key=lambda z: z.y1)
    return items, (page.rect.x1 - page.rect.x0)


def _line_scale(items: list[_Item], body_size: float | None) -> float:
    """本页正文文本行的**行高中位值**（y1−y0）——**逐页量**，不是全局常量。

    为什么量行高而不是"相邻行 y0 之差"：后者在版式里混着表格单元、公式碎片、
    图表轴标时会被拉偏（实测 `2501687` p16 的一页里有 11pt 间距的表格行与 3pt
    间距的公式碎片，中位间距掉到 4pt 上下，于是"第一跳"上限跟着缩水、图注上方
    13.5pt 的图片被判成"够不着"，那张图直接丢）。行高只取决于字号，本身很稳。
    """
    import statistics
    hs = [z.y1 - z.y0 for z in items
          if z.kind == "T" and body_size and abs(z.size - body_size) <= SIZE_TOL]
    hs = [round(h, 1) for h in hs if 2.0 < h < 40.0]
    return statistics.median(hs) if hs else FALLBACK_PITCH


def _is_flow_text(it: _Item, body_size: float | None, colw: float) -> bool:
    """整幅宽 × 正文字号的文本行 = 正文段落行（见模块 docstring 的守卫说明）。"""
    if it.kind != "T" or not body_size:
        return False
    return abs(it.size - body_size) <= SIZE_TOL and (it.x1 - it.x0) >= COLW_FRAC * colw


def _walk(items: list[_Item], y_from: float, body_size: float | None,
          colw: float, gap_limit: float, upward: bool
          ) -> tuple[float, float, float, float] | None:
    """从图注出发往一侧走，返回 (近端, 远端, x0, x1)；一件实物都没走到返回 None。

    第一跳允许跨过图注与实物之间的留白（`started` 之前不受空隙上限约束）；
    之后受 `gap_limit` 约束，并受正文行判定（`_is_flow_text`）约束。

    水平范围取**走进来的这些实物自己的 x 范围的并集**（不是页边距、不是常量）：
    "整区渲染"要的是别切掉内容，而内容的就是这些实物。
    """
    seq = sorted(items, key=lambda z: z.y1, reverse=upward)
    near = far = y_from
    cur = y_from
    started = False
    x0 = x1 = None
    for it in seq:
        if upward:
            if it.y1 > y_from + 0.5:
                continue
            gap = cur - it.y1
        else:
            if it.y0 < y_from - 0.5:
                continue
            gap = it.y0 - cur
        if started and gap > gap_limit:
            break
        if _is_flow_text(it, body_size, colw):
            break
        if upward:
            far = min(far, it.y0)
            cur = far
            if not started:
                near = it.y1
        else:
            far = max(far, it.y1)
            cur = far
            if not started:
                near = it.y0
        x0 = it.x0 if x0 is None else min(x0, it.x0)
        x1 = it.x1 if x1 is None else max(x1, it.x1)
        started = True
    if not started or x0 is None or x1 is None:
        return None
    return near, far, x0, x1


def _side_score(near: _Item | None, gap: float, body_size: float | None,
                colw: float, first_jump_max: float) -> tuple[int, float] | None:
    """某一侧"像不像图注的内容"的排序键（越小越像）；该侧不可用返回 None。

    0 = 紧邻的是图形实物（图片/drawings）——最像；
    1 = 紧邻的是**非正文**文本行；
    2 = 紧邻的是正文段落行——最不像（图注的邻件不可能是正文段落的一行）；
    该侧没有实物、或空隙超过 `first_jump_max` → 不可用。
    """
    if near is None or gap > first_jump_max:
        return None
    if near.kind in ("I", "D"):
        return (0, gap)
    if not _is_flow_text(near, body_size, colw):
        return (1, gap)
    return (2, gap)


def band_of(items: list[_Item], cap: Caption, body_size: float | None,
            page_rect: fitz.Rect, colw: float
            ) -> tuple[fitz.Rect | None, str, str]:
    """图注 → `(裁剪矩形, 方向, 定不出的原因)`。矩形为 None 时原因非空。

    **原因必须具体**：`extract_all` 的 `FigResult.skipped` 逐条登记它，而登记是
    C1「差额非 0 须逐条解释」的全部依据——写成"定不出带"这种笼统话等于没解释。

    方向怎么定：两侧各算一个 `_side_score`，**按分数排序逐侧试走**
    （`_walk` 走不出带就试另一侧），第一侧走通就用。三个要点都是实测逼出来的：

    * **图形实物优先**：`2517690` p9 的 `Table 3` 上方 2.9pt 处是一行正文、下方
      19.6pt 处是表格图片；只按空隙近远会判成"上"，带高只有一个行距。
      同一条也解决了**图注折行**：`2516695` p23 的 `Figure 22: …` 折成两行，
      第二行紧贴题注下方（间隙 13.4pt，是个非正文文本行 = 分数 1），而图片在
      题注上方（分数 0）——分数优先即选对；只按空隙近远时那三张图全丢。
    * **第一跳要有上限**：跨过图注留白的那一跳实测最长 30.3pt
      （`2516695` p24 的 fig-24）；不设上限时，图注上方很远处的一个图片会把带
      一路拉到页顶。
    """
    # 图注行的 y1（下侧起点用它，否则"下方"会把图注自己那一行算进去）。
    # **只取图注那一行，不取它的整个 block**：实测表格的题注常与**表体单元**
    # 同属一个 block（`2500836` p10 的 Table 3、`2505199` p15 的 Table 2 都是），
    # 按 block 剔除会把整张表一起剔掉，那两张表就此消失。
    own = [z for z in items
           if z.kind == "T" and abs(z.y0 - cap.y0) < 0.5 and _caption_match(z.text)]
    cap_y1 = max((z.y1 for z in own), default=cap.y0 + 1.0)
    above = [z for z in items if z.y1 <= cap.y0 - 0.5]
    below = [z for z in items if z.y0 >= cap_y1 + 0.5]
    near_up = max(above, key=lambda z: z.y1) if above else None
    near_down = min(below, key=lambda z: z.y0) if below else None
    gap_up = (cap.y0 - near_up.y1) if near_up is not None else float("inf")
    gap_down = (near_down.y0 - cap_y1) if near_down is not None else float("inf")

    scale = _line_scale(items, body_size)
    gap_limit = GAP_PITCH_MULT * scale
    jump_max = FIRST_JUMP_MULT * scale
    cands = [
        (True, _side_score(near_up, gap_up, body_size, colw, jump_max)),
        (False, _side_score(near_down, gap_down, body_size, colw, jump_max)),
    ]
    tried = []
    for upward, score in sorted(cands, key=lambda t: (t[1] is None, t[1] or (9, 9.0))):
        side = "上" if upward else "下"
        if score is None:
            gap = gap_up if upward else gap_down
            tried.append(
                f"{side}侧够不着（最近实物在 {gap:.1f}pt 外 > 第一跳上限 {jump_max:.1f}pt）"
                if gap != float("inf") else f"{side}侧无实物"
            )
            continue
        got = _walk(items, cap.y0 if upward else cap_y1, body_size, colw,
                    gap_limit, upward)
        if got is None:
            tried.append(f"{side}侧紧邻即正文段落行")
            continue
        near, far, x0, x1 = got
        r = fitz.Rect(
            max(x0, page_rect.x0 + 1), max(min(near, far), page_rect.y0 + 1),
            min(x1, page_rect.x1 - 1), min(max(near, far), page_rect.y1 - 1),
        )
        # **两种"带不可用"必须分开报**：宽度塌成 0 与"带高不够"不是一回事。
        # 2026-09-24 复核轮实测到一个**不成立的断言**：修复前两支共用同一句话，于是入库的
        # 放行证据里出现过 `2513314` p4 fig-2 的
        # `下侧带高只有 91.2pt < MIN_BAND=20.0pt`——**91.2 并不小于 20.0**（真实原因是那一侧
        # 的 x 范围被裁成了 0 宽）。本项目最重的那类缺陷就是"证据里一句不成立的话"，
        # 故这里**分开报**，并让 `verify_c.py` 的「原因具体」判据**逐条核这句话里的不等式**
        # （`MIN_BAND_CLAIM_RX`）：声明了 `X < MIN_BAND` 就必须 X < MIN_BAND。
        if r.width < 1.0:
            tried.append(f"{side}侧带宽塌成 {r.width:.1f}pt（< 1.0pt，裁不出内容）")
            continue
        if r.height < MIN_BAND:
            tried.append(f"{side}侧带高只有 {r.height:.1f}pt < MIN_BAND={MIN_BAND}pt")
            continue
        return r, ("up" if upward else "down"), ""
    return None, "", "；".join(tried) or "两侧都够不着"


def extract_all(src: Path, out_dir: Path, dpi: int = 200) -> FigResult:
    """从**原件**抽图表。原件只读（水印只在内存里置空）。

    产出：`<out_dir>/fig-NN-pP.png`（图）/ `tab-NN-pP.png`（表）+ 同名
    `.caption.txt`。同一页同一编号出现两次时，第二张起名字带 `-2`、`-3` 后缀
    （实测本语料有同页同号并列的图注）——否则后写的那张会覆盖前一张，
    产出数**静默**小于图注数。

    目录里的旧 `*.png` / `*.caption.txt` 先清掉：产出目录是可重生成的派生物
    （`corpus/papers/figures/` 在 .gitignore 里），留着上一轮的残件会让磁盘上的
    张数与本轮的真实产出对不上。

    `dpi=200`：正文 12pt 的图在 200dpi 下约 2.8 倍线宽，够 M3 复用；
    全量 201 份的体积已评估（`docs/mcm-suite-todo.md` §A）。
    """
    doc = fitz.open(src)
    n_fig = n_tab = 0
    skipped: list[str] = []
    try:
        # **必须在任何 get_text / get_pixmap 之前**——否则水印会进版面实物列表，
        # 也会被烤进 PNG。
        watermark.strip_in_memory(doc)
        body_size = None
        try:
            from . import textmd
            body_size = textmd.body_size(doc)
        except Exception:
            # 拿不到正文字号：正文行判定失效（只会让带偏大，不会切图）。不静默——
            # 由 skipped / C1 的差额暴露；这里不抛，因为它是"带偏大"而非"产出错"。
            body_size = None
        caps = caption_blocks(doc)

        out_dir = Path(out_dir)
        if out_dir.is_dir():
            for old in list(out_dir.glob("*.png")) + list(out_dir.glob("*.caption.txt")):
                old.unlink()
        out_dir.mkdir(parents=True, exist_ok=True)

        seen: Counter = Counter()
        for cap in caps:
            page = doc[cap.page]
            items, colw = _page_items(page)
            rect, _dir, why = band_of(items, cap, body_size, page.rect, colw)
            if rect is None:
                # 登记串的**形状**是判据的一部分：`verify_c.py` 用
                # `SKIP_RECORD_RX / SKIP_SIDE_RX / SKIP_SIGNAL_RX / MIN_BAND_CLAIM_RX`
                # 逐条核它（页码 + 编号 + 侧别 + 一个量出的数值/定点原因 + 图注原文，
                # 且**明写的不等式必须自洽**），不合规即判 C1 FAIL——只数条数的旧口径
                # 抓不住"登记退化成噪音"。
                # **改这条消息必须同步改那四条正则**（改窄会假红，属安全方向）。
                skipped.append(
                    f"p{cap.page + 1} {cap.kind}-{cap.num}: 定不出内容带"
                    f"（{why}）｜图注 {cap.text[:40]!r}"
                )
                continue
            seen[(cap.kind, cap.num, cap.page)] += 1
            rep = seen[(cap.kind, cap.num, cap.page)]
            name = f"{cap.kind}-{cap.num:02d}-p{cap.page + 1}"
            if rep > 1:
                name += f"-{rep}"
            png = page.get_pixmap(dpi=dpi, clip=rect)
            (out_dir / f"{name}.png").write_bytes(png.tobytes("png"))
            (out_dir / f"{name}.caption.txt").write_bytes(cap.text.encode("utf-8"))
            if cap.kind == "fig":
                n_fig += 1
            else:
                n_tab += 1
    finally:
        doc.close()
    return FigResult(n_fig=n_fig, n_tab=n_tab, skipped=tuple(skipped))
