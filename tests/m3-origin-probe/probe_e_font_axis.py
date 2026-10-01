#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_e_font_axis.py —— C 续：默认色序真相 / 显式色序 / 字体索引定名 / 框线刻度。

每条改动都**导出后读产物核实**（PNG 像素 / PDF get_fonts / 图像差分）。

跑法：python tests/m3-origin-probe/probe_e_font_axis.py > build/m3-origin-probe/raw_probe_e.txt 2>&1
"""
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'e')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image, ImageChops
import fitz
import originpro as op

print('### probe_e_font_axis start ###')
op.set_show(False)

def rd(n):
    try:
        return op.po.LT_get_var(n)
    except Exception:                                         # noqa: BLE001
        return '<ERR>'

def rs(n):
    try:
        return op.po.LT_get_str(n)
    except Exception:                                         # noqa: BLE001
        return '<ERR>'

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

def color_stats(p):
    """返回 (distinct, 非近灰且占比>=0.5% 的颜色列表) —— 与 check-figure-style F2 同口径的快速读。"""
    im = Image.open(p).convert('RGB').resize((320, 320), Image.NEAREST)
    tot = 320 * 320
    keep = {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24:
            continue
        keep[(r // 16, g // 16, b // 16)] = keep.get((r // 16, g // 16, b // 16), 0) + cnt
    sig = [k for k, v in keep.items() if v / tot >= 0.005]
    return len(set(Image.open(p).convert('RGB').getdata())), len(sig), sorted(sig)

def diffcount(a, b):
    ia, ib = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    if ia.size != ib.size:
        return f'size不同 {ia.size} vs {ib.size}'
    d = ImageChops.difference(ia, ib)
    return sum(1 for px in d.getdata() if px != (0, 0, 0))

# ============ A. 默认色序（不同模板）============
print('--- A. 默认色序：不同模板下 6 条线的颜色 ---')
def build(template, name, tag):
    wb = op.new_book('w', name + '_w')
    ws = wb[0]
    x = np.linspace(0, 10, 41)
    ws.from_list(0, x.tolist())
    for i in range(6):
        ws.from_list(i + 1, (np.sin(x + i * 0.4)).tolist())
    if template:
        gp = op.new_graph(name, template=template)
    else:
        gp = op.new_graph(name)
    if gp is None:
        print(f'  [{tag}] template={template!r} 建图失败（new_graph 返回 None）')
        return None
    gl = gp[0]
    ps = [gl.add_plot(ws, chr(ord('B') + i)) for i in range(6)]
    gl.rescale()
    run('legend;')
    op.wait('s', 0.2)
    cols = [(p.color if p else None) for p in ps]
    print(f'  [{tag}] template={template!r} 颜色 = {cols}')
    p = exp(f'pal_{tag}.png', 'tr1.Unit:=2 tr1.Width:=800')
    if p:
        print(f'        导出 {os.path.basename(p)} distinct/有效彩色 =', color_stats(p))
    return gp

build('', 'Gdefault', 'origin.otp')
build(op.path('e') + '3Ys_Y-Y-Y.otp', 'G3ysA', '3Ys_Y-Y-Y')
build(op.path('e') + 'ReportLineScatter.otp', 'Grep', 'ReportLineScatter')

# ============ B. 显式色序 ============
print('\n--- B. 显式指定 hex 色序 ---')
wb = op.new_book('w', 'Data2')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
for i in range(6):
    ws.from_list(i + 1, (np.sin(x + i * 0.4) + i).tolist())
gp = op.new_graph('Gexplicit')
gl = gp[0]
ps = [gl.add_plot(ws, chr(ord('B') + i)) for i in range(6)]
gl.rescale()
hexes = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#000000']
for p, h in zip(ps, hexes):
    try:
        p.color = h
    except Exception as ex:                                   # noqa: BLE001
        print('  set color 失败', h, ex)
print('  设定色序 =', hexes)
print('  读回 Plot.color =', [p.color for p in ps])
pe = exp('pal_explicit.png', 'tr1.Unit:=2 tr1.Width:=800')
if pe:
    print('  导出 distinct/有效彩色 =', color_stats(pe))

# ============ C. 字体索引定名 ============
print('\n--- C. 字体：索引-名字互查 + 点名 Times New Roman ---')
for expr in ('FontIndexByName("Times New Roman")', 'FontIndex("Times New Roman")',
             'FontNameByIndex(1)', 'FontName$(1)', 'FontNames(0)'):
    r = run(f'__T={expr};') if '(' in expr and expr.endswith(')') else run(f'__S$={expr};')
    v = rd('__T') if 'ByName' in expr or expr.startswith('FontNameByIndex') or expr.startswith('FontIndex(') else rs('__S$')
    print(f'  {expr}  -> run={r} 值={v}')
print('  xb.text$ =', repr(rs('xb.text$')), '| xb.font =', rd('xb.font'))
for f in (5, 10, 20):
    print(f'  FontNameByIndex({f}) ->', (run(f'__T=FontNameByIndex({f});'), rd('__T')))
# 试 FontIndexByName 设到 label.font
idx = None
run('__T=FontIndexByName("Times New Roman");')
idx = rd('__T')
print('  Times New Roman 索引候选 =', idx)
if isinstance(idx, float) and idx == idx:
    print('  设 layer.x.label.font / y / xb ->', run(f'layer.x.label.font={int(idx)};'),
          run(f'layer.y.label.font={int(idx)};'), run(f'xb.font={int(idx)};'))
    pf = exp('font_tnr.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
    if pf:
        with fitz.open(pf) as d:
            print('  点名后 PDF get_fonts() =', d[0].get_fonts())

# 回退是否静默：点名一个不存在的字体
print('\n--- C2. 静默回退测试：不存在的字体名 ---')
print('  FontIndexByName("NoSuchFontXYZ") ->', (run('__T=FontIndexByName("NoSuchFontXYZ");'), rd('__T')))
print('  layer.x.label.font=99999 ->', run('layer.x.label.font=99999;'),
      '| 读回 =', rd('layer.x.label.font'))
pf2 = exp('font_bogus.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
if pf2:
    with fitz.open(pf2) as d:
        print('  乱设索引后 PDF get_fonts() =', d[0].get_fonts())
run('layer.x.label.font=1; layer.y.label.font=1;')

# ============ D. 框线 / 刻度 ============
print('\n--- D. 框线 / 刻度（改前后图像差分核实）---')
base = exp('axis_before.png', 'tr1.Unit:=2 tr1.Width:=900')
# 去上/右框线（opposite 轴）
print('  设 layer.x.opposite=0, layer.y.opposite=0 ->',
      run('layer.x.opposite=0;'), run('layer.y.opposite=0;'))
# 刻度朝内
for cand in ('layer.x.tick.direction', 'layer.x.ticks.direction', 'layer.x.tickdir',
             'layer.x.majorTick.direction', 'layer.x.tickdir=1;'):
    print('   探测', cand, '->', rd(cand) if not cand.endswith(';') else run(cand))
print('  设 layer.x.tick.direction=1 ->', run('layer.x.tick.direction=1;'),
      '| 读回 =', rd('layer.x.tick.direction'))
# 只留主刻度（minor ticks = 0）
print('  设 layer.x.minorTicks=0, layer.y.minorTicks=0 ->',
      run('layer.x.minorTicks=0;'), run('layer.y.minorTicks=0;'))
after = exp('axis_after.png', 'tr1.Unit:=2 tr1.Width:=900')
if base and after:
    print('  改前/改后 像素差 =', diffcount(base, after))

op.exit()
print('### probe_e_font_axis done ###')
