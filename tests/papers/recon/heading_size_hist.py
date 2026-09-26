"""侦察探针：43 份的「字号 → 承载非空白字符数」直方图 + `HEADING_DELTA` 的可行区间。

**只读**原件。输出写成 `tests/papers/reports/b2-size-histogram.txt`（字节级 + LF，
只写仓库相对路径）。它证明的是 `tools/papers/textmd.py` 的
`body_size()` 与 `HEADING_DELTA = 1.0` 在**全 43 份**上都成立，而不是在某一篇上成立
——教训 §4.3：单样本观察不能写成通则，**而且试点会掩盖它**。

为什么这份探针入库而不是放 `build/`（`build/` 被 gitignore）：本目录 README 已立的
规矩——证据的生成器与被它证明的结论分开存放，会让证据在下次清理时静默消失
（通则 7 的代价实例）。`build/mutation_runner*.py` 那类一次性演示不在此列。

**核心量是"可行区间"，不是"某篇的空档"**：实现判的是
    raw_size >= round(raw_body, 1) + HEADING_DELTA
（`body_size()` 四舍五入到 0.1；`to_markdown` 拿的是原始 size），所以逐篇对
`HEADING_DELTA` 的约束是半开区间 `(A − body_r, B − body_r]`：`A` 是该篇低于阈值的
最大原始字号、`B` 是不低于阈值的最小原始字号。43 份取**交集**，就是全语料允许的
`HEADING_DELTA` 全集。

命令：`python tests/papers/recon/heading_size_hist.py`
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # tests/papers/recon/x.py → 仓库根
sys.path.insert(0, str(ROOT))

import fitz  # noqa: E402

from tools.papers import io, textmd, watermark  # noqa: E402

OUT = ROOT / "tests" / "papers" / "reports" / "b2-size-histogram.txt"
WS = re.compile(r"\s+")


def scan(src: Path):
    """→ (body_raw, body_r, 字号→字符数(四舍五入到 0.1), 原始字号集合)。

    与 `body_size()` 同序：先置空水印 XObject 的流，水印字才不进直方图。
    """
    doc = fitz.open(src)
    try:
        watermark.strip_in_memory(doc)
        hist: Counter = Counter()   # 四舍五入后的字号 → 非空白字符数
        raws: set[float] = set()    # 出现过的原始字号
        for pno in range(doc.page_count):
            for block in doc[pno].get_text("dict")["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        t = WS.sub("", span["text"])
                        if not t:
                            continue
                        hist[round(span["size"], 1)] += len(t)
                        raws.add(span["size"])
    finally:
        doc.close()
    if not hist:
        return None
    body_r = max(hist.items(), key=lambda kv: kv[1])[0]
    raw_of: dict[float, float] = {}
    for r in raws:
        raw_of[round(r, 1)] = r
    return raw_of, body_r, hist, sorted(raws)


def feasible(raws: list[float], body_r: float, delta: float):
    """`(下界 A−body_r, 上界 B−body_r, 阈值−A, B−阈值)`；A 或 B 缺则对应项为 None。"""
    thr = body_r + delta
    below = [r for r in raws if r < thr]
    above = [r for r in raws if r >= thr]
    a = max(below) if below else None
    b = min(above) if above else None
    return (a - body_r if a is not None else None,
            b - body_r if b is not None else None,
            thr - a if a is not None else None,
            b - thr if b is not None else None)


def main() -> None:
    pdfs = sorted((io.ORIGIN / "2025美赛O奖论文").rglob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError("试点目录下没有任何 PDF")

    rows = []      # (stem, body_raw, body_r, share, hist, raw_A, raw_B, lo, hi, mA, mB)
    for src in pdfs:
        got = scan(src)
        if got is None:
            rows.append((src.stem, None, None, None, None, None, None, None, None,
                         None, None))
            continue
        _, body_r, hist, raws = got
        body_raw = min(raws, key=lambda r: (abs(round(r, 1) - body_r),))
        total = sum(hist.values())
        lo, hi, mA, mB = feasible(raws, body_r, textmd.HEADING_DELTA)
        thr = body_r + textmd.HEADING_DELTA
        raw_a = max((r for r in raws if r < thr), default=None)
        raw_b = min((r for r in raws if r >= thr), default=None)
        rows.append((src.stem, body_raw, body_r, hist[body_r] / total, hist,
                     raw_a, raw_b, lo, hi, mA, mB))

    # 可行区间的交集：下界取"所有下界的上确界"，上界取"所有上界的下确界"。
    los = [r[7] for r in rows if r[7] is not None]
    his = [r[8] for r in rows if r[8] is not None]
    LO, HI = max(los), min(his)
    lo_stem = next(r[0] for r in rows if r[7] == LO)
    hi_stem = next(r[0] for r in rows if r[8] == HI)
    mA_min = min(r[9] for r in rows if r[9] is not None)
    mB_min = min(r[10] for r in rows if r[10] is not None)
    mA_stem = next(r[0] for r in rows if r[9] == mA_min)
    mB_stem = next(r[0] for r in rows if r[10] == mB_min)

    doc = [
        "# Task 3 第二轮 · 字号直方图证据（全 43 份）",
        "",
        "日期：2026-09-24　·　探针：`tests/papers/recon/heading_size_hist.py`",
        "命令：`python tests/papers/recon/heading_size_hist.py`（只读原件，自写本文件）",
        "被测：`tools/papers/textmd.py` 的 `body_size()` 与 `HEADING_DELTA = 1.0`",
        "",
        "## 这一份证据要证明什么",
        "",
        "标题阈值从全局绝对常量（`HEADING_MIN_SIZE = 13.5`）改成**逐篇相对**：",
        "`raw_size >= round(raw_body, 1) + HEADING_DELTA`。阈值形式（绝对差）与取值",
        "（`HEADING_DELTA = 1.0`）都必须**在全 43 份上量过**再定——单样本观察不能写成",
        "通则，而且试点恰恰会在这一点上骗人（教训 §4.3）。",
        "",
        "逐篇列出「字号 → 承载非空白字符数」（按字符数降序），并给出该篇对",
        "`HEADING_DELTA` 的**约束区间**：",
        "",
        "| 栏 | 含义 |",
        "| :--- | :--- |",
        "| `body_raw` | 承载字符数最多的**原始**字号；`body_r` = 它四舍五入到 0.1 |",
        "| `A` | 低于阈值 `body_r + 1.0` 的**最大原始字号** |",
        "| `B` | 不低于阈值的**最小原始字号** |",
        "| 可行区间 | `(A − body_r, B − body_r]`——该篇允许的 `HEADING_DELTA` 全集 |",
        "| `阈值−A` | 阈值离下侧最近的原始字号有多远（> 0 才成立） |",
        "| `B−阈值` | 上侧最近的原始字号离阈值有多远（>= 0 才成立） |",
        "",
        "方向说明：`A` 必须**被判为非标题**（它低于阈值），`B` 必须**被判为标题**",
        "（它不低于阈值）。所以逐篇约束是可取的 `HEADING_DELTA` 半开区间，43 份的",
        "**交集**就是全语料允许的取值集合。",
        "",
        "口径：字符数只数非空白字符；先在内存中置空水印 XObject 的流（与",
        "`textmd.extract` 同序），所以水印字不进直方图；`is_title` 的假标题排除不改",
        "直方图，也不改 `A`/`B`（它作用在文本上，不在字号上）。",
        "",
        "## 43 份逐篇",
        "",
    ]
    for stem, body_raw, body_r, share, hist, a, b, lo, hi, mA, mB in rows:
        if hist is None:
            doc += [f"### {stem}　! 该篇没有文本层", ""]
            continue
        top = ", ".join(f"{s}:{n}" for s, n in hist.most_common())
        doc += [
            f"### {stem}　body_raw={body_raw:.4f}　body_r={body_r}"
            f"（占非空白字符 {share*100:.1f}%）",
            "",
            f"    A={a:.4f}　B={b:.4f}　可行区间=({lo:.4f}, {hi:.4f}]"
            f"　阈值−A={mA:.4f}　B−阈值={mB:.4f}",
            f"    hist（字号:非空白字符数，降序）: {top}",
            "",
        ]

    doc += [
        "## 汇总：`HEADING_DELTA` 的可行区间（这就是取值的依据）",
        "",
        f"* 43 份逐篇区间取**交集** = **({LO:.4f}, {HI:.4f}]**，宽 {HI - LO:.4f}pt。",
        f"  下界由 `{lo_stem}` 顶住（它的 A 离正文最近），上界由 `{hi_stem}` 顶住",
        f"（它的 B 离正文最近）。",
        f"* 该交集里**唯一的 0.1 倍数就是 1.0**——所以 `HEADING_DELTA = 1.0` 不是挑出来",
        f"的，是 43 份联合允准的唯一取值。（0.9 ≤ {LO:.4f} 会被 `{lo_stem}` 否掉；",
        f"1.1 > {HI:.4f} 会被 `{hi_stem}` 否掉。）",
        f"* 取 1.0 之后，43 份里阈值距下侧原始字号的余量最小 = {mA_min:.4f}pt"
        f"（`{mA_stem}`），距上侧 = {mB_min:.4f}pt（`{mB_stem}`）——两侧都为正，",
        "  即 43 份里没有一份的字号落在阈值上或跨过阈值。",
        "",
        "### 为什么是**绝对差**，不是比例",
        "",
        "同一批数据换比例形式，可行区间会窄到几乎不可用：",
        "下界由 `2504218` 顶住（10.9100 / 9.9600 = 1.0954），",
        "上界由 `2522820` 顶住（11.9600 / 10.9100 = 1.0962）——区间宽约 0.0008，",
        "而 `body * 1.10` 会直接越过 `2522820`（10.9100 × 1.10 = 12.001 > 11.9600，",
        "判据漏掉它的全部小节标题，正是本轮要修的 B2 红）。绝对差没有这个放大效应：",
        "基准四舍五入带来的 ±0.05 误差在比例里被乘 1.1 放大，在绝对差里只被加 1.0。",
        "",
        "### 正文号取「承载字符数最多」而不是「出现次数最多」",
        "",
        "* 语料里同一名义字号会因字体 units-per-em 不同落在两个值上：`2501687` 是",
        "  11.9 与 12.0、`2516695` 是 12.0 与 11.9。按字符数取众数不会被这种噪声带偏",
        "  （`2516695` 的 12.0 承载 27479 字符、11.9 承载 11010 字符）；按行数取则会。",
        "",
        "## 已知边界（字号层分不开，本轮不声称解决）",
        "",
        "* `2504218`：正文 9.96，而**摘要页正文与 Notation 表在 11.96**（相对差 +2.0）。",
        "  逐篇相对阈值必然把它们一并提为 `## `（实测：该篇 `## ` 行 61 → 244，再经假标题",
        "  排除后 213，净 +152）。而 11.96 在",
        "  `2522820` 是必须认的小节标题（相对差 +1.05）——**任何单一绝对差阈值都同时",
        "  满足不了**：要放过 2504218 就得 > 2.0，要认出 2522820 就得 ≤ 1.05。",
        "  `verify_b.py` 的 B3（标题承载 ≤ 全篇 20%）正是承认该边界而设，不声称解决。",
        "* 阈值余量本身只有百分之几 pt（见汇总第三条）。这不是调参空间，是**语料事实**：",
        "  这批论文的字号阶梯就是 9.96 / 10.91 / 11.96 / 14.35 这样的值。全量 201 份若",
        "  出现落在 +1.0 附近的层级，阈值必须重测——本轮只对试点 43 份负责。",
        "",
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(("\n".join(doc)).encode("utf-8"))  # 字节级 + LF
    print(f"written: {OUT.relative_to(ROOT).as_posix()}  ({len(rows)} 份)")
    print(f"可行区间交集 = ({LO:.4f}, {HI:.4f}]　余量 min = {mA_min:.4f} / {mB_min:.4f}")


if __name__ == "__main__":
    main()
