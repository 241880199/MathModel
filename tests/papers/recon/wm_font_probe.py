"""侦察：水印 span 的字体/字号在实际语料里到底长什么样。

**只读**——不写任何文件、不改动任何原件（`find_watermark_xrefs` 与
`content_text` 都只读内存；本脚本不调 `strip_in_memory`）。

动机：初版 `tools/papers/watermark.py` 曾有一个 `is_watermark_span`，按
「MicrosoftYaHei + >=60pt」过滤正文水印。这个判据来自 2025 那批的实测，
但设计文档把它写成了普适结论（`水印 span 特征唯一：MicrosoftYaHei 72pt`）。
本脚本对全部 201 份逐份取数，看这句话到底对哪些合集成立。

**该函数已从模块里删除**（commit 476915c：正文侧改走结构性机制——置空带
`/PieceInfo` + `/Watermark` 标记的 Form XObject 流），所以本脚本自带一份
**退役实现的本地副本**（见下面的 `_RETIRED_*`）。副本存在的唯一目的是把
「它为什么被退役」这件事做成**可复算的证据**：`命中 43/120` 这个数字是
每次运行当场算出来的，不是抄一句注释。它不是模块的接口，也不得被复制回
`tools/papers/watermark.py`。

输出即证据，逐字抄进 `wm-font-coverage.txt`；末尾的自检会在副本与记录
的数字不符时**当场失败**，免得证据在语料或副本漂移后静默失真。
"""
import json
import sys
from collections import Counter
from pathlib import Path

# 本文件比 tests/papers/*.py 深一层（recon/），故要多退一级才到仓库根
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import fitz  # noqa: E402
from tools.papers import io, watermark  # noqa: E402

SCAN = Path(__file__).resolve().parent / "watermark-scan.json"
# 扫水印字时只看前几页：水印每页都有，取前 4 页足够定特征
PAGES = 4

# ---------------------------------------------------------------------------
# 退役实现的本地副本。原文见 476915c^:tools/papers/watermark.py。
# 模块**不再提供**这个符号；这里是它唯一的存世副本，用途只有一个：
# 每个运行当场复算「它只覆盖 120 份里的 43 份」，作为退役决定的证据。
# ---------------------------------------------------------------------------
_RETIRED_FONT = "MicrosoftYaHei"
_RETIRED_MIN_SIZE = 60.0


def retired_is_watermark_span(font: str, size: float) -> bool:
    """已退役的字体启发式（副本，逐字复刻 476915c^）。"""
    return _RETIRED_FONT in font and size >= _RETIRED_MIN_SIZE


# wm-font-coverage.txt 里记下的数字。自检用它——不一致就说明证据失真。
EXPECTED_TOTAL = 120
EXPECTED_HIT = 43


def watermark_span_profile(doc, words):
    """返回 (字体计数, 最小字号, 最大字号)——只看含水印字的 span。"""
    fonts = Counter()
    lo, hi = float("inf"), 0.0
    for pno in range(min(doc.page_count, PAGES)):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for s in line["spans"]:
                    if any(w in s["text"] for w in words):
                        fonts[s["font"]] += 1
                        lo = min(lo, s["size"])
                        hi = max(hi, s["size"])
    return fonts, lo, hi


def main() -> int:
    scan = json.loads(SCAN.read_text("utf-8"))
    print(f"扫描清单 {len(scan)} 份（来自 tests/papers/recon/watermark-scan.json）")

    prof = Counter()
    xref_wm, xref_clean, false_pos, open_fail = Counter(), Counter(), [], 0

    for r in scan:
        try:
            doc = fitz.open(io.REPO / r["file"])
        except Exception:
            open_fail += 1
            continue
        try:
            n = len(watermark.find_watermark_xrefs(doc))
            if r.get("n_wm", 0) > 0:
                xref_wm[n] += 1
            else:
                xref_clean[n] += 1
                if n:
                    false_pos.append((r["file"], n))
            if r.get("n_wm", 0) > 0 and r.get("wm_texts"):
                coll = Path(r["file"]).parts[2]  # corpus/历届优秀论文/<合集>/...
                fonts, lo, hi = watermark_span_profile(doc, r["wm_texts"])
                if fonts:
                    head = next(iter(fonts))
                    prof[
                        (
                            coll,
                            "+".join(r["wm_texts"]),
                            ",".join(sorted(fonts)),
                            f"{lo:.1f}-{hi:.1f}",
                            retired_is_watermark_span(head, lo),
                        )
                    ] += 1
        finally:
            doc.close()

    print("\n[1] 正文水印 span 的字体/字号（有水印的逐份实测前 4 页）")
    print(f"{'合集':<30}{'水印字':<16}{'span 字体':<20}{'字号':<12}{'is_watermark_span':<20}份数")
    for (coll, words, fonts, rng, hit), n in sorted(prof.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        print(f"{coll:<30}{words:<16}{fonts:<20}{rng:<12}{str(hit):<20}{n}")
    total = sum(prof.values())
    hit_n = sum(n for k, n in prof.items() if k[4])
    print(f"合计有水印 {total} 份；is_watermark_span 命中 {hit_n} 份，漏 {total - hit_n} 份")

    # 自检：上面这行数字是**证据**（`wm-font-coverage.txt` 逐字抄的就是它，
    # 退役决定靠它成立）。副本或语料任一漂移，证据就失真——当场红，
    # 而不是安静地打印一个新数字冒充原结论。
    if (total, hit_n) != (EXPECTED_TOTAL, EXPECTED_HIT):
        print(
            f"\n自检失败：本次实测 有水印 {total} 份 / 命中 {hit_n} 份，"
            f"与 wm-font-coverage.txt 记录的 {EXPECTED_TOTAL} / {EXPECTED_HIT} 不符。"
            f"这份证据已失真：需重新测量并更新 wm-font-coverage.txt"
            f"（不是把这里的常量改成新数字）。",
            file=sys.stderr,
        )
        return 1

    print("\n[2] find_watermark_xrefs 的判别力（全部 201 份）")
    print(f"有水印的命中数分布 = {dict(sorted(xref_wm.items()))}（期望全是 1）")
    print(f"无水印的命中数分布 = {dict(sorted(xref_clean.items()))}（期望全是 0）")
    print(f"无水印误报 = {len(false_pos)} 份  打开失败 = {open_fail} 份")
    for f, n in false_pos[:10]:
        print(f"   误报: {f} -> {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
