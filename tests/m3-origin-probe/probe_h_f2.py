#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_h_f2.py —— F2 专项：6 色的**填充柱**（并排、面积大）能不能被 F2 数到？

对照 probe_g 的 6 色**细线**（F2 读 0）。构造：X=1..6，Yk 只在第 k 位非零 ⇒ 6 根并排柱、6 色。

跑法：python tests/m3-origin-probe/probe_h_f2.py > build/m3-origin-probe/raw_probe_h.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'h')
os.makedirs(OUT, exist_ok=True)

import numpy as np
import fitz
import originpro as op

print('### probe_h_f2 start ###')
op.set_show(False)

def exp(name, extra=''):
    p = os.path.join(OUT, name)
    ext = os.path.splitext(name)[1][1:]
    op.po.LT_execute(f'expgraph type:={ext} path:="{OUT}" filename:="{name}" overwrite:=replace {extra}')
    return p if os.path.exists(p) else None

def f2(p):
    if not p or not os.path.exists(p):
        return None
    from PIL import Image
    if os.path.splitext(p)[1].lower() == '.pdf':
        with fitz.open(p) as d:
            pm = d[0].get_pixmap(dpi=150, colorspace=fitz.csRGB, alpha=False)
            im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
    else:
        im = Image.open(p).convert('RGB')
    im = im.resize((320, 320), Image.NEAREST)
    tot = 320 * 320
    keep = {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24:
            continue
        keep[(r // 16, g // 16, b // 16)] = keep.get((r // 16, g // 16, b // 16), 0) + cnt
    sig = [k for k, v in keep.items() if v / tot >= 0.005]
    return len(sig), sorted(sig)

wb = op.new_book('w', 'Bars')
ws = wb[0]
ws.from_list(0, [1.0, 2, 3, 4, 5, 6])
for k in range(6):
    ws.from_list(k + 1, [float(k + 2) if i == k else 0.0 for i in range(6)])
gp = op.new_graph('Bars')
gl = gp[0]
hexes = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#00ced1']
ps = []
for i in range(6):
    ps.append(gl.add_plot(ws, chr(ord('B') + i), type='c'))
gl.rescale()
for p, h in zip(ps, hexes):
    p.color = h
print('  柱色读回 =', [tuple(p.color) for p in ps])
pb = exp('bars6.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
pn = exp('bars6.png', 'tr1.Unit:=2 tr1.Width:=1893')
print('  bars6.pdf F2 =', f2(pb))
print('  bars6.png F2 =', f2(pn))

op.exit()
print('### probe_h_f2 done ###')
