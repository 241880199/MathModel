"""正文抽取：字形层 → markdown。全程无 OCR、无推断。

水印在抽取时**置空其 XObject 的流**（`watermark.strip_in_memory`），
与图表/公式路径同源。**不用字体/字号启发式**——实测水印字体有三种，
启发式只覆盖 43/120，且试点的 43 份恰在命中范围内，会绿着通过。
详见 spec §4.1.1。

**不读任何清洗版 PDF**——原件是唯一输入，且全程只读。

## 标题阈值：全局绝对常量 → 逐篇相对阈值（2026-09-24 修正）

原先只有 `HEADING_MIN_SIZE = 13.5` 这一个**全局绝对常量**。全局常量遇到**逐篇变化**
的量，就是出错的温床：试点 42 份正文 12.0pt（标题落在 14.0/14.4，确实在 13.5 之上），
而 `2522820` 正文 **10.9pt**、小节标题 **12.0pt**——它整篇的小节被降级成粗体 `**…**`。
**正文字一个没丢，丢的是小节层级**，而 M2 要按章节类型取措辞，正需要这一层。

改为**相对于该篇自己的正文字号**：正文字号 = 该篇内**承载非空白字符数最多**的字号
（四舍五入到 0.1），`raw_size >= 正文字号 + HEADING_DELTA` 判为标题。

`HEADING_DELTA = 1.0` **不是挑出来的**。实现判的是原始 size 与"四舍五入后的正文号
+ DELTA"，所以每一篇对 DELTA 的约束是一个半开区间（低于阈值的最大字号必须仍低于、
不低于阈值的最小字号必须仍不低于）。全 43 份的**交集**实测为

    (0.9100, 1.0600]        宽 0.15pt

（下界由 `2504218` 顶住——正文 9.96，而它的运行页眉在 10.91；上界由 `2522820` 顶住
——正文 10.91，而它的小节标题在 11.96）。**这个交集里唯一的 0.1 倍数是 1.0**
（0.9 ≤ 0.91 被否、1.1 > 1.06 被否）。取 1.0 后两侧余量 0.09pt / 0.06pt，43 份无一份
的字号落在阈值上。逐篇直方图与可行区间：`tests/papers/reports/b2-size-histogram.txt`。

**为什么是绝对差而不是比例**：同一批数据换比例形式，可行区间只有约 0.0008 宽
（下界 `2504218` 10.91/9.96 = 1.0954、上界 `2522820` 11.96/10.91 = 1.0962）。
`body * 1.10` 更会直接越过 `2522820`（10.91 × 1.10 = 12.001 > 11.96）——漏掉它全部
小节标题，正是本轮要修的那条 B2 红。绝对差没有这个放大效应：四舍五入的 ±0.05 误差
在比例里被乘 1.1 放大，在绝对差里只被加 1.0。

正文号取"承载字符数最多的字号"而非"出现次数最多的字号"：`2516695` 的 12.0（27479 字符）
与 11.9（11010 字符）是同一名义字号在两种字体度量下的落值，按行数会被噪声带偏。
**已知边界：余量只有 0.06–0.09pt**。这不是调参空间而是语料事实（这批论文的字号阶梯
就是 9.96 / 10.91 / 11.96 / 14.35 这样的值）；全量 201 份若出现落在 +1.0 附近的层级，
阈值必须重测——本轮只对试点 43 份负责。

## 假标题（2026-09-24 新增，`is_title`）

43 份全量量过，被提升为 `## ` 的非标题行有四类，都是**形态**而非某个具体字符串：

| 形态 | 实测实例 | 43 份上的量 |
| :--- | :--- | :--- |
| 项目符号前缀 | `## ⚫ Step 1: Define Parameter Uncertainty` | `⚫`(U+26AB) 2 行、`•`(U+2022) 8 行 |
| 纯单字母 | `## A`（摘要页 `Problem Chosen: A`）、`## x`/`## z`（图轴标） | 含在下面 87 行里 |
| 纯数字 | `## 2500836`（`Team Control Number`）、`## 2025`、`## 1`（章节号） | 第 1 页 87 行 + 正文 250 余行 |
| 无任何字母数字 | `## ∑`、`## (`、`## U+F0E5`（Symbol/Mathtype 私有区码位） | **153 行 / 10 份** |

前两类不是"只在第 1 页"的形态：`2500759` 的目录页把 11 个页码排成了标题大小的行，
`2504218` 的 Notation 表把 `h`/`p`/`S`/`N` 排成了标题大小，`2517690` 的图轴标是
`X`/`z`。一处口径覆盖全部，比"只排除摘要页"更省事也更干净。

`1.1` 这类**小节号会被留下**（含数字、又不是纯数字）：语料里"号"与"题"常分两行排
（`1.1` / `Problem Background`），丢掉号会让 `2505964`、`2522820` 的 B2 不通过
（判据 `tests/papers/verify_b.py` 的 B4 是同一份规格的另一处实现，改这里要同步改那里）。

## 已知边界（字号层分不开，本轮不声称解决）

`2504218` 正文 10.0pt，而**摘要页正文与 Notation 表也在 12.0pt**（= 正文 + 2.0）。
逐篇相对阈值必然把它们一并提为 `## `（实测：该篇 `## ` 行 61 → 244，再经假标题排除
后 213，净 +152）。**这不是参数没调好**：12.0 在 `2522820` 是必须认的小节标题
（正文 +1.1），在 `2504218` 是要排除的摘要页（正文 +2.0），**任何单一阈值都同时满足
不了**。B3（过度提升上界 20%）正是承认该边界而设。要真正分开得引入版式/内容判据
（例如"标题所在 block 只有 1–2 行"），超出本轮范围，已登记。
"""
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import fitz

from . import watermark

# 标题相对本篇正文字号的最小差值。取法见模块 docstring 的实测表
# （43 份可行区间交集 (0.9100, 1.0600]；0.9 在交集外，不可用）。
HEADING_DELTA = 1.0
CAPTION = re.compile(r"^\s*(Figure|Fig\.|Table)\s*\d+\s*[:.]", re.I)
_WS = re.compile(r"\s+")

# 项目符号族。实测本语料被提升为标题的行里只出现 U+26AB `⚫` 与 U+2022 `•`；
# 这里列同族的圆/方/星字形，是为了不把"一份论文的观测"写死成规则（教训 §4.3）。
BULLET_CHARS = "⚫●○•∙▪▫■□◆◇★☆"
_BULLET_START = re.compile(r"^[" + re.escape(BULLET_CHARS) + r"]")
# 裸 token：单个拉丁字母或纯数字。见模块 docstring 的四类形态表。
_BARE_TOKEN = re.compile(r"^[A-Za-z]$|^[0-9]+$")


@dataclass
class MdResult:
    n_headings: int
    n_chars: int
    n_captions: int


def is_heading(size: float, body_size: float) -> bool:
    """**相对该篇自己的正文字号**判标题。

    接口变更（2026-09-24）：原为 `is_heading(size)`，唯一消费者在本模块内部
    （`to_markdown`），故可改。`body_size` 由 `body_size()` 逐篇算出。
    """
    return size >= body_size + HEADING_DELTA


def is_title(text: str) -> bool:
    """这一行的**文本**像不像标题（假标题排除；形态表见模块 docstring）。

    判据只有三条，都不认具体字符串：
      1. 行首不是项目符号（列表项，且同篇提升不一致）；
      2. 整行不是裸 token（摘要页栏位值 / 队号 / 年份 / 章节号 / 图轴标 / 表格单元）；
      3. 行内至少有一个字母数字字符（公式字形与私有区码位既不是字也不是数）。
    """
    t = text.strip()
    if not t:
        return False
    if _BULLET_START.match(t) or _BARE_TOKEN.match(t):
        return False
    return any(c.isalnum() for c in t)


def body_size(doc: fitz.Document) -> float:
    """该篇承载**非空白字符数最多**的字号 = 本篇正文字号。

    字号四舍五入到 0.1 再统计：同一名义字号会因字体 units-per-em 不同落在
    11.99–12.05（实测 `2501687` 的正文是 11.9 与 12.0 两个值、`2516695` 是
    12.0 与 11.9），不归一化会让"最多的那个"在噪声里抖。

    **fail-closed**：一个文本层都没有的 PDF 拿不到基准，**抛错**而不是返回 0
    ——返回 0 会让每个字号都过阈，静默产出一堆假标题（本项目已四次栽在
    "判据在什么都没验的情况下报绿"，这里是它的同一形状）。
    """
    hist: Counter = Counter()
    for pno in range(doc.page_count):
        for block in doc[pno].get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                for span in line["spans"]:
                    t = _WS.sub("", span["text"])
                    if t:
                        hist[round(span["size"], 1)] += len(t)
    if not hist:
        raise RuntimeError("该篇没有文本层，定不出正文字号（拒绝静默产出假标题）")
    return max(hist.items(), key=lambda kv: kv[1])[0]


def to_markdown(doc: fitz.Document) -> tuple[str, MdResult]:
    """把文档转成 markdown。

    **调用方必须已经 `strip_in_memory` 过**——本函数不做水印判断，
    因为那需要认字体，而字体判据是错的（见模块 docstring）。
    """
    body = body_size(doc)   # 先扫一遍定本篇正文字号（逐篇不同，不能用常量）
    out: list[str] = []
    n_headings = n_captions = 0

    for pno in range(doc.page_count):
        page = doc[pno]
        out.append(f"\n<!-- page {pno + 1} -->\n")
        for block in page.get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = line["spans"]
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).rstrip()
                if not text.strip():
                    continue
                size = max(s["size"] for s in spans)
                bold = any("Bold" in s["font"] for s in spans)
                if CAPTION.match(text):
                    n_captions += 1
                    out.append(f"\n*{text.strip()}*\n")
                elif is_heading(size, body) and is_title(text):
                    n_headings += 1
                    out.append(f"\n{'#' * 2} {text.strip()}\n")
                elif bold and len(text.strip()) < 80 and not text.strip().endswith("."):
                    out.append(f"\n**{text.strip()}**\n")
                else:
                    out.append(text)

    body_md = "\n".join(out)
    body_md = re.sub(r"\n{3,}", "\n\n", body_md)
    return body_md, MdResult(
        n_headings=n_headings,
        n_chars=len(re.sub(r"\s+", "", body_md)),
        n_captions=n_captions,
    )


def extract(src: Path, out_md: Path) -> MdResult:
    """从**原件**抽正文。原件只读，水印在内存中置空。

    **fail-closed 判据**：若文本层本来就带着水印字，却找不到水印 XObject
    （`strip_in_memory` 返回 0），说明这份论文的水印形态与已知的不同——
    继续下去会把水印字静静写进 md。此时**抛错**，不静默产出。
    反过来，文本层本来没有水印字的（2022 与 UMAP 那 81 份），返回 0 是正常的。
    """
    doc = fitz.open(src)
    try:
        raw = "".join(doc[i].get_text() for i in range(doc.page_count))
        had_wm_text = any(w in raw for w in watermark.WM_WORDS)
        n = watermark.strip_in_memory(doc)
        if had_wm_text and n == 0:
            raise RuntimeError(
                f"文本层带水印字，却找不到水印 XObject（形态未知）: {src.name}"
            )
        body, res = to_markdown(doc)
    finally:
        doc.close()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_bytes(body.encode("utf-8"))  # 字节级，勿用 write_text
    return res
