"""A 组：规则化关键词表 → 图型分类。只读 corpus/，产出落 build/。

**判据面**：图注 `*.caption.txt`（文件名不含任何图型信息——命名是
`{fig|tab}-NN-pP`，只有 kind / 编号 / 页码，见 tools/papers/figures.py:411）。

**规则表是词界正则 + 优先级序列**，不是"包含子串"：
  1. 一律 `\\b` 词界，避免 `roc` 被 `process` 吃掉、`bar` 被 `barrier` 吃掉；
  2. 从上到下第一条命中即定类（顺序 = 优先级），命中行原样打印，可被质疑；
  3. 命中 0 条 → `other`（**这就是"未覆盖"**，不是"其他图型"）。

用法：python build/m3-figure-recon/probe_a_rules.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "corpus/papers/figures/2025美赛O奖论文"

# (类目, 正则, 人读的判据说明)
# 顺序即优先级：越"具体"的越靠前（3d 比 line 具体；heatmap 比 map 具体）。
RULES = [
    ("flow-diagram", r"\b(flow\s?chart|flow\s?diagram|workflow|pipeline\s+diagram|"
                     r"process\s+diagram|framework\s+diagram|roadmap)\b", "流程图/工作流框"),
    ("schematic",    r"\b(schematic|illustration|conceptual\s+diagram|"
                     r"schematic\s+diagram|architecture)\b", "示意图/概念图"),
    ("surface-3d",   r"\b(3\s?-?d|three[\s-]dimensional|surface\s+plot|"
                     r"3d\s+(surface|plot|scatter|bar))\b", "三维"),
    ("heatmap",      r"\b(heat\s?map|heatmap|correlation\s+matrix|confusion\s+matrix|"
                     r"matrix\s+of)\b", "热力图/矩阵图"),
    ("contour",      r"\b(contour|iso[\s-]?line|level\s+curve)\b", "等值线"),
    ("violin",       r"\b(violin)\b", "小提琴"),
    ("box",          r"\b(box\s?plot|boxplot|box\s+and\s+whisker|whisker)\b", "箱线"),
    ("histogram",    r"\b(histogram|hist\b|frequency\s+distribution)\b", "直方图"),
    ("pie",          r"\b(pie\s?chart|pie\b|donut\s+chart|doughnut)\b", "饼图"),
    ("network",      r"\b(network|graph\s+of|node[\s-]link|knowledge\s+graph|"
                     r"tree\s+diagram|dendrogram|sankey)\b", "网络/图结构"),
    ("map",          r"\b(map|map\s+of|geograph|spatial\s+distribution|choropleth|"
                     r"world\s+map|heatmap\s+of\s+the\s+world)\b", "地图"),
    ("scatter",      r"\b(scatter|scatterplot|scatter\s+plot|bubble\s+chart|"
                     r"joint\s+plot|pair\s?plot)\b", "散点"),
    ("bar",          r"\b(bar\s?chart|bar\s?plot|bar\b|column\s+chart|"
                     r"stacked\s+bar|grouped\s+bar)\b", "柱/条"),
    ("line",         r"\b(line\s?chart|line\s?plot|line\s+graph|curve|"
                     r"time\s+series|trend|trajectory|density\s+plot|"
                     r"plot\s+of|chart\s+of|graph\s+of|radar\s+chart|"
                     r"radar\s+plot|area\s+chart|roc\s+curve|qq\s+plot)\b", "折线/曲线"),
]
COMPILED = [(name, re.compile(rx, re.I), why) for name, rx, why in RULES]

# 表（tab-*）不参与图型分类：表格不是"图型"，量它等于把类别体系用错。
CLASSES = [n for n, _, _ in RULES] + ["other"]


def classify(text: str):
    for name, rx, why in COMPILED:
        m = rx.search(text)
        if m:
            return name, m.group(0), why
    return "other", "", ""


def strip_label(t: str) -> str:
    return re.sub(r"^\s*(?:Figure|Fig\.|Table)\s*\d+\s*[:.：．。]?\s*", "", t)


def main():
    figs = sorted(BASE.rglob("fig-*.caption.txt"))
    print("# 规则表（顺序=优先级；正则带 \\b 词界）")
    for name, rx, why in RULES:
        print(f"#   {name:14s} {rx}")
    print("#")
    print("path\tcaption\tclass\tmatched")
    for p in figs:
        raw = p.read_bytes().decode("utf-8")
        body = strip_label(raw)
        cls, hit, _ = classify(body)
        print(f"{p.relative_to(BASE).as_posix()}\t{raw}\t{cls}\t{hit}")


if __name__ == "__main__":
    main()
