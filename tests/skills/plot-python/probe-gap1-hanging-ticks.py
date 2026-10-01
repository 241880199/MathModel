#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""缺口①（上/右**悬空刻度**）的**入库探针** —— `mcmplot.py` 散文里那条"复算命令"指的就是本文件。

用法：  python tests/skills/plot-python/probe-gap1-hanging-ticks.py

## 它证什么

底座 `science` 自带 `xtick.top: True` / `ytick.right: True`。`mcm.mplstyle` 关掉上/右边框线
（`axes.spines.top/right: False`）之后，若不同时把这两个刻度键关掉，图的上/右会留下**没有边框线
却仍在的悬空刻度**。本探针量**轴区顶边 / 右边内侧**那条带里的**非白像素数**，并同跑一条对照：

- **落地态**（`apply_style()` 之后：`xtick.top=False` / `ytick.right=False`）⇒ 两带均应为 **0**；
- **旧态**（对照：同一条链、只把这两个键改回 `True`）⇒ 两带读到**墨迹**（非 0）。

对照非 0 同时证明探针**不是恒零**（不是"什么都没量到也报绿"）。

## 口径（为什么这么量）

- 底座刻度**朝内**（`xtick.direction='in'`、`xtick.major.size=3.0pt`）⇒ 墨迹落在**轴区内侧**那条带里；
  带宽 = `ceil(刻度长pt × 300dpi / 72) + 2 px 余量`（**现算**，不写死魔法数）。
- 只数**轴区严格内部**的带（`x∈(left,right)`、`y∈(top,bottom)`）：否则会把**仍在的**左/下边框线
  也算进去，落地态就不再是 0（实测：不排除时落地态顶/右带各读到 14 px 的**边框线**，与刻度无关）。
- 折线取 `x∈[0.1,0.9]`、`y∈[0.3,0.7]`，刻意**避开**被测的两条带 ⇒ 读数只反映刻度，不掺数据墨迹。
- 非白阈值：灰度 `< 200`（同 Task 4 报告所用口径）。
- 只写**临时目录**，不落仓。

## 射程（写实，别读大）

读数**绝对值**依赖底座 `science` 的刻度方向/长度（本机 SciencePlots 2.2.2）⇒ 换个底座版本绝对值会变；
但"**落地态 0 / 对照非 0**"这个**判别性**不变（那才是缺口①被处置的直接证据）。
"""
import math
import pathlib
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / ".claude/skills/mcm-plot-python/assets"))

DPI = 300                    # 与散文里"300dpi ≈ 12.5px"一致
TEXTWIDTH_IN = 6.31          # 任一正值即可：本探针与图幅无关，只用 figsize_for 拿一张标准图
THRESHOLD = 200              # 灰度 < 此值记为"非白"


def measure(xtick_top, ytick_right, band):
    """渲一张标准图，返回 `(顶边带, 右边带)` 的非白像素数。只写临时目录。"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import mcmplot as m
    from PIL import Image

    plt.rcParams["xtick.top"] = xtick_top
    plt.rcParams["ytick.right"] = ytick_right
    fig, ax = plt.subplots(figsize=m.figsize_for(TEXTWIDTH_IN))
    ax.plot([0.1, 0.9], [0.3, 0.7])                     # 刻意避开顶/右两条被测带
    out = pathlib.Path(tempfile.mkdtemp()) / "probe-gap1.png"
    m.save(fig, out, DPI)

    fig.set_dpi(DPI)
    fig.canvas.draw()
    bb = ax.get_window_extent(fig.canvas.get_renderer())
    im = Image.open(out).convert("L")
    _, h = im.size
    px = im.load()
    left, right = round(bb.x0), round(bb.x1)
    top_edge, bot_edge = round(h - bb.y1), round(h - bb.y0)
    top_band = sum(1 for y in range(top_edge, top_edge + band)
                   for x in range(left + 1, right) if px[x, y] < THRESHOLD)
    right_band = sum(1 for y in range(top_edge + 1, bot_edge - 1)
                     for x in range(right - band, right) if px[x, y] < THRESHOLD)
    plt.close(fig)
    return top_band, right_band


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import mcmplot as m

    m.apply_style()
    tick_pt = max(plt.rcParams["xtick.major.size"], plt.rcParams["ytick.major.size"])
    band = math.ceil(tick_pt * DPI / 72.0) + 2
    print(f"apply_style() 后：xtick.top={plt.rcParams['xtick.top']} "
          f"ytick.right={plt.rcParams['ytick.right']} · 刻度方向={plt.rcParams['xtick.direction']} · "
          f"刻度长={tick_pt}pt ⇒ 探针带宽 {band}px")

    landed = measure(False, False, band)
    control = measure(True, True, band)
    print(f"落地态（xtick.top=False / ytick.right=False）  顶边带 = {landed[0]:>4}  "
          f"右边带 = {landed[1]:>4}")
    print(f"旧态（对照：同一条链、两键改回 True）          顶边带 = {control[0]:>4}  "
          f"右边带 = {control[1]:>4}")

    ok = landed == (0, 0) and control[0] > 0 and control[1] > 0
    if ok:
        print("OK 悬空刻度已消失，且对照能读到墨迹（探针不是恒零）")
    else:
        print("FAIL 读数不符预期（落地态应 0/0、对照应非 0）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
