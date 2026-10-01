#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Read the *embedded* fonts out of exported PDFs with PyMuPDF.

Why this file exists: on this platform MATLAB's `get(ax,'FontName')` echoes back
whatever string you set, even when the font does not exist -- so the only
ground truth for "which font actually landed in the artifact" is the artifact
itself.  `page.get_fonts()` reports the fonts the PDF really carries.

Run:
    python tests/m3-matlab-font-probe/measure_fonts.py <pdf-or-dir> [...]
"""
import sys
from pathlib import Path

import fitz


def describe(pdf: Path) -> None:
    doc = fitz.open(pdf)
    page = doc[0]
    box = page.rect
    imgs = len(page.get_images(full=True))
    fonts = page.get_fonts(full=True)
    # (xref, ext, type, basefont, name, encoding, referencer)
    names = []
    for f in fonts:
        base, ext, typ = f[3], f[1], f[2]
        tag = "%s/%s" % (base, typ)
        if tag not in names:
            names.append(tag)
    size = pdf.stat().st_size
    print(
        "PDF %-34s box=%.0fx%.0fpt imgs=%d bytes=%-7d fonts: %s"
        % (pdf.name, box.width, box.height, imgs, size, ", ".join(names) or "(none)")
    )
    doc.close()


def main(argv):
    targets = []
    for a in argv:
        p = Path(a)
        if p.is_dir():
            targets.extend(sorted(p.glob("*.pdf")))
        else:
            targets.append(p)
    if not targets:
        print("usage: measure_fonts.py <pdf-or-dir> [...]")
        return 2
    for t in targets:
        try:
            describe(t)
        except Exception as exc:  # noqa: BLE001
            print("PDF %-34s ERROR: %s" % (t.name, exc))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
