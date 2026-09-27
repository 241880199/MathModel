#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 2 遗留风险 #1 的取证工具：把 F2 的**每一个色箱占比**打出来。

背景（Task 1 遗留风险 #1，逐字引自 tests/skills/figure-choose/figure-style-baseline.txt）：
  「Task 1 实测 4 色 PDF 的最大抗锯齿箱占 0.312%，而地板是 0.5%（余量 0.188pp）
   => 若写手产出的图带渐变/细网格/抗锯齿色带，F2 可能虚高成假 FAIL。」

本脚本**不改** check-figure-style.py（那是只读的 Task 1 交付物），而是：
  · **直接 import 它**（`raster_rgb` / `color_count` / `RASTER_DPI` 都用原件，不抄）；
  · 只把 `color_count` 里"取箱"那一步**重写一遍**——因为原件只返回**计数**，
    而本工具要的是**每个箱的占比**（这正是不抄就无法回答的那一问）；
  · 于是重写的那份必须自证没漂：对**每一个**输入断言
    `len(过地板的箱) == color_count(rgb)`，并对 `color_count` 的源码做字面 tripwire
    （`// 16` / `< 24` / `0.005` / `resize((320, 320), Image.NEAREST)` 任一消失即拒绝出数）。
  ⇒ Task 1 的检查器一改，本工具**要么当场报错、要么与它逐格一致**，不会静默给出旧口径的读数。

用法：
  python tests/skills/figure-choose/red/f2-diagnose.py <fig...> [--out <file>]
    `--out` 用 `write_bytes` 落盘（本仓纪律；Windows 上 `> file` 会把行尾翻成 CRLF，
    而 `red/f2-boxes.txt` 是 LF 的入库件 ⇒ 要逐字节复现这份证据，只能用 `--out`）。
退出码：0（纯取证，不判红绿；红绿以 check-figure-style.py 为准）· 2（与检查器口径不一致）。
"""
import importlib.util
import pathlib
import sys

import fitz                      # PyMuPDF
from PIL import Image

RED = pathlib.Path(__file__).resolve().parent
CHECKER = RED.parent / "check-figure-style.py"


def load_checker():
    """把 Task 1 的检查器当模块 import（它有 `__main__` 守卫，import 无副作用）。"""
    spec = importlib.util.spec_from_file_location("check_figure_style", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CS = load_checker()

BIN = 16                         # 与 check-figure-style.py::color_count 的 `// 16` 一致
CHROMA = 24                      # 与 `max(r,g,b) - min(r,g,b) < 24` 一致
FLOOR = 0.005                    # 与 `c / tot >= 0.005` 一致
TRIPWIRES = ("resize((320, 320), Image.NEAREST)", "max(r, g, b) - min(r, g, b) < 24",
             "// 16", ">= 0.005")


def assert_checker_shape():
    """源码 tripwire：重写的那份取箱逻辑必须仍与原件同形。"""
    import inspect
    src = inspect.getsource(CS.color_count)
    missing = [t for t in TRIPWIRES if t not in src]
    if missing:
        print(f"FAIL: check-figure-style.py::color_count 已变形（缺 {missing}）"
              f"（fail-closed，拒绝出数）", file=sys.stderr)
        sys.exit(2)


def boxes(rgb):
    """重写 color_count 的取箱逻辑，但**返回全部箱**（不设地板）。

    与原件的一致性由调用方逐例断言 `len(over) == CS.color_count(rgb)`。
    采样用 NEAREST（同原件，见其文件头 D1）。
    """
    im = rgb.convert("RGB").resize((320, 320), Image.NEAREST)
    tot = 320 * 320
    keep = {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < CHROMA:
            continue
        k = (r // BIN, g // BIN, b // BIN)
        keep[k] = keep.get(k, 0) + cnt
    return tot, keep


def page_count(path):
    if path.suffix.lower() != ".pdf":
        return None
    with fitz.open(path) as doc:
        return doc.page_count


def main():
    assert_checker_shape()
    argv = sys.argv[1:]
    out_path = None
    if "--out" in argv:
        i = argv.index("--out")
        if i + 1 >= len(argv):
            print("FAIL: --out 需要跟一个路径（fail-closed）", file=sys.stderr)
            sys.exit(2)
        out_path = pathlib.Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print("FAIL: 至少要给一个图路径（fail-closed）", file=sys.stderr)
        sys.exit(2)
    args = argv
    lines = []

    def emit(s=""):
        lines.append(s)
        print(s)

    for arg in args:
        p = pathlib.Path(arg)
        n_pages = page_count(p)
        rgb = CS.raster_rgb(p)                       # ← 原件，非抄件
        tot, keep = boxes(rgb)
        shares = sorted(((c / tot, k) for k, c in keep.items()), reverse=True)
        over = [s for s in shares if s[0] >= FLOOR]
        if len(over) != CS.color_count(rgb):         # ← 逐例一致性断言（漂移即报错）
            print(f"FAIL: 本工具取箱 {len(over)} 个过地板箱，检查器 color_count 报 "
                  f"{CS.color_count(rgb)} —— 两者已不一致（fail-closed）", file=sys.stderr)
            sys.exit(2)
        emit(f"=== {p.as_posix()}")
        emit(f"    loaded_px={rgb.size[0]}x{rgb.size[1]}"
             + (f"  pdf_pages={n_pages}" if n_pages is not None else "  (raster)"))
        emit(f"    F2-relevant boxes (>= 0.5% floor): {len(over)}   => F2 "
             f"{'PASS' if len(over) <= CS.F2_MAX else 'FAIL'}")
        emit(f"    all chroma boxes kept (before floor): {len(shares)}")
        for i, (s, k) in enumerate(shares):
            mark = ">=FLOOR" if s >= FLOOR else "  below"
            emit(f"      #{i + 1:<2d} bin{k}  share={s * 100:7.3f}%  {mark}")
        below = [s for s in shares if s[0] < FLOOR]
        if below and over:
            emit(f"    boundary: highest sub-floor box = {below[0][0] * 100:.3f}%"
                 f"  |  lowest counted box = {over[-1][0] * 100:.3f}%"
                 f"  |  floor = {FLOOR * 100:.3f}%")
        elif not below:
            emit("    boundary: no sub-floor chromatic box at all"
                 " (nothing near-missed the 0.5% floor)")
        else:
            emit("    boundary: no box reached the 0.5% floor (F2 = 0)")
        emit()

    if out_path is not None:
        blob = ("\n".join(lines) + "\n").encode("utf-8")     # 恒为 LF（write_bytes，不转换）
        out_path.write_bytes(blob)
        print(f"wrote {out_path.as_posix()}  bytes={len(blob)}  "
              f"lines={blob.count(chr(10).encode())}")


if __name__ == "__main__":
    main()
