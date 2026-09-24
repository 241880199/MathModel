"""水印处理：**三条路径共用同一个机制**——在内存里置空水印 XObject 的流。

水印形态（2026-09-23 实测，见 tests/papers/recon/）：
  独立 Form XObject，带 /PieceInfo <</ADBE_CompoundType
  <</Private /Watermark>>>> 标记，压在正文与图表之上。

**为什么不用字体/字号启发式**（初版做法，已废弃）：
从单份论文观察到的「水印恒为 MicrosoftYaHei 72pt」被当成了通则，实测全
201 份有**三种**字体——2025 是 MicrosoftYaHei 72pt，2023/2024 是
KaiTi 74.4/76.5pt，2023 另有 SimHei 83.4pt。字体启发式只覆盖 43/120；
而试点的 43 份恰好全在命中范围内，所以**试点会绿着通过、全量才炸**。

置空 XObject 流是**结构性**的：流空了就画不出任何东西，与字体无关。
实测 120/120 命中，81 份无水印件零误伤。
"""
import fitz

WM_WORDS = ["校苑数模公众号", "校苑数模", "英伽教育"]
_WM_MARK = ("/PieceInfo", "/Watermark")


def find_watermark_xrefs(doc: fitz.Document) -> list[int]:
    """返回所有带 PieceInfo/Watermark 标记的 xref。

    必须逐 xref 加 try：这些 PDF 的对象流里有悬空引用，
    xref_object 会对部分 xref 抛 RuntimeError（实测 2025 那批有 9 处）。
    """
    hits = []
    for x in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(x, compressed=True)
        except Exception:
            continue
        if all(m in obj for m in _WM_MARK):
            hits.append(x)
    return hits


def strip_in_memory(doc: fitz.Document) -> int:
    """把水印 XObject 的流置空。**只改内存对象，不保存、不写回任何文件。**

    返回处理的对象数。水印在全部页共用同一 xref，故一次置空即全篇生效。

    返回 0 对本流水线是**异常信号**，不是无事发生：说明这份论文的水印形态
    与已知的不同，下游会静静地带水印。调用方应把 0 当失败处理。
    """
    xrefs = find_watermark_xrefs(doc)
    for x in xrefs:
        doc.update_stream(x, b"")
    return len(xrefs)


def spans(doc: fitz.Document) -> list[str]:
    """逐 span 取文本。供 A3 做差集比对（不拼接、不折叠空白）。"""
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for s in line["spans"]:
                    if s["text"].strip():
                        out.append(s["text"])
    return out


def content_text(doc: fitz.Document) -> str:
    """置空水印流后的全文。

    **会就地修改传入的 doc**——调用方若要对照"置空前"的文本，必须
    在调用前先取好（见 verify_wm.py 的 A3 检查）。
    """
    strip_in_memory(doc)
    return "".join(doc[i].get_text() for i in range(doc.page_count))
