#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_g_e2e.py —— D 段端到端：造"能过规范"与"故意违规"两个场景，各出 PNG+PDF。

产物落 build/m3-origin-probe/g/，判词由 shell 侧调
`tests/skills/figure-choose/check-figure-style.py` 逐份跑（见 README）。

跑法：python tests/m3-origin-probe/probe_g_e2e.py > build/m3-origin-probe/raw_probe_g.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'g')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image
import fitz
import originpro as op

print('### probe_g_e2e start ###')
op.set_show(False)

def run(cmd):
    try:
        op.po.LT_execute(cmd)
        return 'OK'
    except Exception as e:                                    # noqa: BLE001
        return f'<ERR {type(e).__name__}: {e}>'

def exp(name, extra=''):
    p = os.path.join(OUT, name)
    ext = os.path.splitext(name)[1][1:]
    op.po.LT_execute(f'expgraph type:={ext} path:="{OUT}" filename:="{name}" overwrite:=replace {extra}')
    return p if os.path.exists(p) else None

def meas(p):
    if not p:
        return '未产出'
    e = os.path.splitext(p)[1].lower()
    if e == '.pdf':
        with fitz.open(p) as d:
            r = d[0].rect
            return f'PDF 页盒 {r.width/72:.5f} x {r.height/72:.5f} in'
    with Image.open(p) as im:
        return f'PNG {im.size[0]} x {im.size[1]} px'

def color_sig(p):
    """check-figure-style F2 同口径的快速读。"""
    if not p or not os.path.exists(p):
        return None
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
    return sum(1 for c in keep.values() if c / tot >= 0.005)

# ===================== GREEN 场景：2 曲线、2 色、白底、图注合规 =====================
print('--- GREEN 场景 ---')
wb = op.new_book('w', 'G')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
ws.from_list(1, (np.sin(x)).tolist())
ws.from_list(2, (np.cos(x)).tolist())
gp = op.new_graph('GREEN')
gl = gp[0]
p1 = gl.add_plot(ws, 'B')
p2 = gl.add_plot(ws, 'C')
gl.rescale()
p1.color = '#000000'
p2.color = '#d62728'
run('layer.plot1.line.width=1.5; layer.plot2.line.width=1.5;')
op.wait('s', 0.3)
gpdf = exp('green.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
gpng = exp('green.png', 'tr1.Unit:=2 tr1.Width:=1893')
print('  green.pdf :', meas(gpdf), '| F2 快速读 =', color_sig(gpdf))
print('  green.png :', meas(gpng), '| F2 快速读 =', color_sig(gpng))

# ===================== RED-1：图偏宽（F1 违规）=====================
print('--- RED-1 图偏宽 ---')
rpdf = exp('red_wide.pdf', 'tr1.Unit:=0 tr1.Width:=8.00')
rpng = exp('red_wide.png', 'tr1.Unit:=2 tr1.Width:=2400')
print('  red_wide.pdf :', meas(rpdf))
print('  red_wide.png :', meas(rpng))

# ===================== RED-2：彩色太多（F2）=====================
print('--- RED-2 彩色太多：细线 6 色 vs 柱状 6 色 ---')
wb2 = op.new_book('w', 'R')
ws2 = wb2[0]
xs = np.linspace(0, 10, 41)
ws2.from_list(0, xs.tolist())
for i in range(6):
    ws2.from_list(i + 1, (np.sin(xs + i * 0.5) + i).tolist())
g2 = op.new_graph('REDLINE')
gl2 = g2[0]
hexes = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#00ced1']
ps = [gl2.add_plot(ws2, chr(ord('B') + i)) for i in range(6)]
gl2.rescale()
for p, h in zip(ps, hexes):
    p.color = h
print('  验证读回 =', [p.color for p in ps])
redline = exp('red_line6.png', 'tr1.Unit:=2 tr1.Width:=1200')
print('  red_line6.png :', meas(redline), '| F2 快速读 =', color_sig(redline))

# 柱状 6 色（面积大）
wb3 = op.new_book('w', 'RBar')
ws3 = wb3[0]
ws3.from_list(0, [1.0])
for i in range(6):
    ws3.from_list(i + 1, [float(2 + i)])
g3 = op.new_graph('REDBAR')
gl3 = g3[0]
ps3 = []
for i in range(6):
    ps3.append(gl3.add_plot(ws3, chr(ord('B') + i), type='c'))
gl3.rescale()
for p, h in zip(ps3, hexes):
    p.color = h
print('  柱状读回 =', [p.color for p in ps3])
redbar = exp('red_bar6.png', 'tr1.Unit:=2 tr1.Width:=1200')
print('  red_bar6.png :', meas(redbar), '| F2 快速读 =', color_sig(redbar))
redbar_pdf = exp('red_bar6.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
print('  red_bar6.pdf :', meas(redbar_pdf), '| F2 快速读 =', color_sig(redbar_pdf))

op.exit()
print('### probe_g_e2e done ###')
