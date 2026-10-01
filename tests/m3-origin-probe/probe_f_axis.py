#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_f_axis.py —— ⑤ 去上/右框线 · 刻度朝内 · 只留主刻度：候选属性逐条"改→导出→图像差分"。

判据：差分像素数大 = 该属性确实生效；≈0 = 该属性没生效（诚实记"没找到"）。

跑法：python tests/m3-origin-probe/probe_f_axis.py > build/m3-origin-probe/raw_probe_f.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'f')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image, ImageChops
import originpro as op

print('### probe_f_axis start ###')
op.set_show(False)

def run(cmd):
    try:
        op.po.LT_execute(cmd)
        return 'OK'
    except Exception as e:                                    # noqa: BLE001
        return f'<ERR {type(e).__name__}: {e}>'

def exp(name):
    p = os.path.join(OUT, name)
    op.po.LT_execute(f'expgraph type:=png path:="{OUT}" filename:="{name}" overwrite:=replace tr1.Unit:=2 tr1.Width:=900')
    return p if os.path.exists(p) else None

def diff(a, b):
    ia, ib = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    d = ImageChops.difference(ia, ib)
    return sum(1 for px in d.getdata() if px != (0, 0, 0))

wb = op.new_book('w', 'D')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
ws.from_list(1, (np.sin(x)).tolist())
ws.from_list(2, (np.cos(x)).tolist())

def fresh_graph(name):
    """每次都从模板新建图，保证"改前"是干净的模板默认。"""
    gp = op.new_graph(name)
    gl = gp[0]
    gl.add_plot(ws, 'B')
    gl.add_plot(ws, 'C')
    gl.rescale()
    op.wait('s', 0.15)
    return gp

gp = fresh_graph('G0')
base = exp('base.png')
print('基准图 =', base)

candidates = [
    ('frame=0',            'layer.frame=0;'),
    ('x2.show=0;y2.show=0', 'layer.x2.show=0; layer.y2.show=0;'),
    ('x.opposite=1',       'layer.x.opposite=1;'),
    ('x.show=0 (sanity 大改)', 'layer.x.show=0;'),
    ('x.majorTicks=3',     'layer.x.majorTicks=3;'),
    ('x.minorTicks=0',     'layer.x.minorTicks=0;'),
    ('x.ticks=4',          'layer.x.ticks=4;'),
    ('x.tickDir=1',        'layer.x.tickDir=1;'),
    ('x.tickdir=1',        'layer.x.tickdir=1;'),
    ('x.tick.direction=1', 'layer.x.tick.direction=1;'),
    ('x.ticklength=2',     'layer.x.ticklength=2;'),
    ('plot1.line.width=3', 'layer.plot1.line.width=3;'),
    ('plot1.color=255',    'layer.plot1.color=255;'),
]
for i, (tag, cmd) in enumerate(candidates):
    g = fresh_graph(f'G{i+1}')          # 干净模板
    p0 = exp('cur_base.png')
    r = run(cmd)
    p1 = exp('cur_after.png')
    d = diff(p0, p1) if (p0 and p1) else 'N/A'
    print(f'  {tag:26s} cmd={cmd:34s} run={r:10s} 差分像素={d}')
    g.destroy()                          # 删掉这张图，避免窗口堆积

op.exit()
print('### probe_f_axis done ###')
