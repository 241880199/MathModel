#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""measure_pixels.py --- what colour is actually in the exported figure?

For each PNG: corner pixel, and the 4 most common colours with their share, quantised
to 8 levels per channel (so a "background" shows up as one big bin whatever its exact
value). This is how "black figure / white figure" is decided here -- not by eye.

re-run from repo root:
  python tests/m3-matlab-recon/measure_pixels.py build/m3-matlab-recon/h_off build/m3-matlab-recon/h_on
"""
import sys
import pathlib
from PIL import Image


def top_colors(im, q=8, n=4):
    small = im.convert("RGB").resize((160, 160), Image.NEAREST)
    cnt = {}
    for k, c in small.getcolors(160 * 160):
        key = (c[0] // q, c[1] // q, c[2] // q)
        cnt[key] = cnt.get(key, 0) + k
    tot = 160 * 160
    out = []
    for key, k in sorted(cnt.items(), key=lambda kv: -kv[1])[:n]:
        out.append(f"~({key[0]*q},{key[1]*q},{key[2]*q}) {100*k/tot:5.1f}%")
    return out


def ink_margins(im, tol=24):
    """Margins (px) from each edge to the first column/row that carries 'ink'
    (a pixel differing from the modal background by > tol on some channel).
    A margin of ~0-2 px means the content is FLUSH to the edge (tight crop);
    a missing edge would show up as a large margin on the opposite side."""
    im = im.convert("RGB")
    w, h = im.size
    px = im.load()
    bg = max(im.getcolors(w * h), key=lambda k: k[0])[1]

    def is_ink(c):
        return max(abs(c[0] - bg[0]), abs(c[1] - bg[1]), abs(c[2] - bg[2])) > tol

    left = next((x for x in range(w) if any(is_ink(px[x, y]) for y in range(0, h, 3))), -1)
    right = next((x for x in range(w - 1, -1, -1) if any(is_ink(px[x, y]) for y in range(0, h, 3))), -1)
    top = next((y for y in range(h) if any(is_ink(px[x, y]) for x in range(0, w, 3))), -1)
    bot = next((y for y in range(h - 1, -1, -1) if any(is_ink(px[x, y]) for x in range(0, w, 3))), -1)
    if -1 in (left, right, top, bot):
        return bg, None
    return bg, (left, top, w - 1 - right, h - 1 - bot)


def main(dirs):
    for d in dirs:
        p = pathlib.Path(d)
        if not p.is_dir():
            print(f"!! not a dir: {d}")
            continue
        print(f"== {d} ==")
        for f in sorted(p.glob("*.png")):
            with Image.open(f) as im:
                im = im.convert("RGB")
                corner = im.getpixel((0, 0))
                w, h = im.size
                tc = top_colors(im)
                bg, marg = ink_margins(im)
            m = "-" if marg is None else f"L{marg[0]} T{marg[1]} R{marg[2]} B{marg[3]}"
            print(f"  {f.name:22s} {w:5d}x{h:<5d} corner={corner} bg={bg} margins(px)={m}")
            print(f"      top: " + " | ".join(tc))


if __name__ == "__main__":
    main(sys.argv[1:] or ["build/m3-matlab-recon/h_off"])
