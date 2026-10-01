#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""measure_artifacts.py --- read the MATLAB-produced artifacts WITHOUT eyeballing.

For every PNG: pixel width/height (PNG header) and the DPI meta if present.
For every PDF: page box in pt and inches (fitz), page count, embedded fonts (page.get_fonts()),
               and whether the page carries a raster image.
Prints one line per artifact. Nothing is written.

re-run from repo root:
  python tests/m3-matlab-recon/measure_artifacts.py build/m3-matlab-recon/a build/m3-matlab-recon/b
"""
import sys
import pathlib
import struct
import fitz


def png_dims(path):
    """PNG IHDR width/height + pHYs (pixels per metre) if present."""
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None, None
    w, h = struct.unpack(">II", raw[16:24])
    dpi = None
    i = 8
    while i < len(raw) - 8:
        ln = struct.unpack(">I", raw[i:i + 4])[0]
        typ = raw[i + 4:i + 8]
        if typ == b"pHYs":
            px, py, unit = struct.unpack(">IIB", raw[i + 8:i + 17])
            if unit == 1:
                dpi = round(px * 0.0254, 3)
            break
        if typ == b"IDAT":
            break
        i += 12 + ln
    return w, h, dpi


def main(dirs):
    for d in dirs:
        p = pathlib.Path(d)
        if not p.is_dir():
            print(f"!! not a dir: {d}")
            continue
        files = sorted([f for f in p.iterdir() if f.suffix.lower() in (".png", ".pdf")])
        for f in files:
            if f.suffix.lower() == ".png":
                w, h, dpi = png_dims(f)
                print(f"PNG {f.name:34s} px={w}x{h}  pHYs_dpi={dpi}  bytes={f.stat().st_size}")
            else:
                with fitz.open(f) as doc:
                    npages = doc.page_count
                    r = doc[0].rect
                    fonts = doc[0].get_fonts()
                    imgs = doc[0].get_images()
                fdesc = " ".join(f"{x[3]}/{x[2]}" for x in fonts) if fonts else "(none)"
                print(f"PDF {f.name:34s} pages={npages} box={r.width:.3f}x{r.height:.3f}pt "
                      f"= {r.width/72:.4f}x{r.height/72:.4f}in  imgs={len(imgs)}  bytes={f.stat().st_size}")
                print(f"      fonts embedded: {fdesc}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["build/m3-matlab-recon/a", "build/m3-matlab-recon/b"])
