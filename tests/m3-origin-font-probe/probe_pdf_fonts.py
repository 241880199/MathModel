# -*- coding: utf-8 -*-
"""probe_pdf_fonts.py — 统一读数器：对目录下所有 PDF 打印字体层 + span 层

fitz 的 page.get_fonts() 每个元素是 7 元组：
  (xref, ext, type, basefont, name, encoding, referencer)
  ★ ext == 'n/a' 表示**没有内嵌字体文件**（只是引用/描述符）；
    ext 是 'ttf'/'otf'/'cff' 等才表示**真的内嵌**。

用法: python tests/m3-origin-font-probe/probe_pdf_fonts.py <dir> [...]
"""
import os
import sys
import json
import glob

import fitz


def read(pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    rows = []
    for f in page.get_fonts():
        rows.append({"xref": f[0], "ext": f[1], "type": f[2],
                     "basefont": f[3], "name": f[4], "enc": f[5]})
    spans = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                spans[s["font"]] = spans.get(s["font"], 0) + len(s["text"])
    ndraw = len(page.get_drawings())
    nimg = len(page.get_images())
    txt = page.get_text()
    doc.close()
    return {"fonts": rows, "spans": spans, "drawings": ndraw,
            "images": nimg, "text": txt}


def main(paths):
    out = {}
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "*.pdf")))
        else:
            files.append(p)
    for pdf in files:
        r = read(pdf)
        out[os.path.basename(pdf)] = r
        emb = [(f["basefont"], f["type"], f["ext"]) for f in r["fonts"]]
        print("### %-28s  fonts=%d drawings=%d images=%d"
              % (os.path.basename(pdf), len(r["fonts"]), r["drawings"], r["images"]))
        print("    (basefont, type, ext):", json.dumps(emb, ensure_ascii=False))
        print("    spans:", json.dumps(r["spans"], ensure_ascii=False))
        print("    text :", json.dumps(r["text"].replace("\n", "|")[:160], ensure_ascii=False))
    return out


if __name__ == "__main__":
    res = main(sys.argv[1:])
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "out-pdf-font-readout.json")
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    print("wrote:", dest)
