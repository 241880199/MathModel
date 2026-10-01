#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_i_dpi_pagesize.py —— 收尾三问：
  (1) 正确的 DPI 节点 `tr.Advanced.DPI` 能不能改 PNG 的 像素/英寸 换算？
  (2) 改页面尺寸 `page.width/height` 能不能改导出物的**宽高比**？
  (3) 会话内色序会不会翻转？（同一模板连建两张图比较）
  外加：去上/右框线候选再试一批（图像差分判定）。

跑法：python tests/m3-origin-probe/probe_i_dpi_pagesize.py > build/m3-origin-probe/raw_probe_i.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'i')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image, ImageChops
import originpro as op

print('### probe_i_dpi_pagesize start ###')
op.set_show(False)

def run(c):
    try:
        op.po.LT_execute(c)
        return 'OK'
    except Exception as e:                                    # noqa: BLE001
        return f'<ERR {type(e).__name__}: {e}>'

def rd(n):
    try:
        return op.po.LT_get_var(n)
    except Exception:                                         # noqa: BLE001
        return '<ERR>'

def exp(name, extra=''):
    p = os.path.join(OUT, name)
    ext = os.path.splitext(name)[1][1:]
    op.po.LT_execute(f'expgraph type:={ext} path:="{OUT}" filename:="{name}" overwrite:=replace {extra}')
    if not os.path.exists(p):
        return None
    with Image.open(p) as im:
        return (im.size, p)

wb = op.new_book('w', 'D')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
ws.from_list(1, (np.sin(x)).tolist())
ws.from_list(2, (np.cos(x)).tolist())

def fresh(name):
    g = op.new_graph(name)
    gl = g[0]
    gl.add_plot(ws, 'B')
    gl.add_plot(ws, 'C')
    gl.rescale()
    op.wait('s', 0.15)
    return g

g = fresh('G1')

print('--- (1) tr.Advanced.DPI 节点 ---')
for dpi in (100, 300, 600):
    r = exp(f'dpi_{dpi}.png', f'tr.Advanced.Resolution:=0 tr.Advanced.DPI:={dpi} tr1.Unit:=0 tr1.Width:=6.31')
    print(f'  tr.Advanced.DPI:={dpi} (Resolution:=0) -> {r[0] if r else "未产出"}')

print('\n--- (2) 改页面尺寸 → 导出宽高比 ---')
print('  改前 page.width/height/resx =', rd('page.width'), rd('page.height'), rd('page.resx'))
for w, h in ((4500, 3000), (6000, 3000)):
    print(f'  设 page.width={w} page.height={h} ->', run(f'page.width={w}; page.height={h};'))
    op.wait('s', 0.15)
    r = exp(f'page_{w}x{h}.png', 'tr1.Unit:=2 tr1.Width:=1500')
    print(f'    导出(宽钉 1500px) = {r[0] if r else "未产出"}  ratio={r[0][0]/r[0][1]:.4f}' if r else '    未产出')
run('page.width=6432; page.height=4560;')
op.wait('s', 0.15)

print('\n--- (3) 会话内色序是否翻转：同模板连建两图比色 ---')
def colors(gp):
    gl = gp[0]
    return [tuple(p.color) for p in gl.plot_list()]
gA = fresh('CA')
cA = colors(gA)
gB = fresh('CB')
cB = colors(gB)
print('  图A 颜色 =', cA)
print('  图B 颜色 =', cB)
print('  两次一致 =', cA == cB)
gA.destroy(); gB.destroy()

print('\n--- (4) 去上/右框线：候选再试一批（差分像素）---')
cands = [
    ('layer.x2.show=0',        'layer.x2.show=0;'),
    ('layer.y2.show=0',        'layer.y2.show=0;'),
    ('layer.x.opposite=0',     'layer.x.opposite=0;'),
    ('layer.y.opposite=0',     'layer.y.opposite=0;'),
    ('layer.frame=0',          'layer.frame=0;'),
    ('layer.axes=0',           'layer.axes=0;'),
    ('layer.x.axes=0',         'layer.x.axes=0;'),
    ('layer.x.tickdir=2',      'layer.x.tickdir=2;'),
    ('layer.x.tick.dir=2',     'layer.x.tick.dir=2;'),
]
for tag, c in cands:
    gg = fresh('FX')
    p0 = exp('fx_base.png')
    run(c)
    p1 = exp('fx_after.png')
    d = 'N/A'
    if p0 and p1:
        ia, ib = Image.open(p0[1]).convert('RGB'), Image.open(p1[1]).convert('RGB')
        d = sum(1 for px in ImageChops.difference(ia, ib).getdata() if px != (0, 0, 0))
    print(f'  {tag:22s} run={run(c):8s} 差分像素={d}')
    gg.destroy()

op.exit()
print('### probe_i_dpi_pagesize done ###')
