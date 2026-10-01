#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_d_appearance.py —— C 段：规范里的外观量 Origin 侧能不能落地。

逐条实测 + **读产物核实**：
  ① 底色 ② 字体族/内嵌字体/回退 ③ 字号·线宽粒度 ④ 默认色序&显式色序
  ⑤ 去上/右框线·刻度朝内·只留主刻度 ⑥ 中文字符

跑法：python tests/m3-origin-probe/probe_d_appearance.py > build/m3-origin-probe/raw_probe_d.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'd')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image
import fitz
import originpro as op

print('### probe_d_appearance start ###')
op.set_show(False)

def rd(n):
    """读一个属性（数值），失败返回 '<ERR>'。"""
    try:
        return op.po.LT_get_var(n)
    except Exception as e:                                    # noqa: BLE001
        return f'<ERR {type(e).__name__}>'

def rs(n):
    try:
        return op.po.LT_get_str(n)
    except Exception as e:                                    # noqa: BLE001
        return f'<ERR {type(e).__name__}>'

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

# ---------- 数据 + 图（6 条曲线，便于看默认色序）----------
wb = op.new_book('w', 'Data')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
for i in range(6):
    ws.from_list(i + 1, (np.sin(x + i * 0.4)).tolist())
ws.set_labels(['X'] + [f'Y{i+1}' for i in range(6)], type_='L')
gp = op.new_graph('G1')
gl = gp[0]
plots = []
for i in range(6):
    plots.append(gl.add_plot(ws, chr(ord('B') + i)))
gl.rescale()
# 显式加图例（默认模板不一定带）
run('legend;')
op.wait('s', 0.3)

# ===== ④ 默认色序 =====
print('--- ④ 默认色序（6 条线的 Plot.color 读数）---')
seq = []
for i, p in enumerate(plots):
    try:
        c = p.color
        seq.append(c)
        print(f'  plot{i+1}.color = {c}  (type {type(c).__name__})')
    except Exception as e:                                    # noqa: BLE001
        print(f'  plot{i+1}.color 读取失败: {type(e).__name__}: {e}')
print('  色序 =', seq)
# 直接读 LabTalk 的 color 属性
for i in range(1, 7):
    print(f'  layer.plot{i}.color(LT) =', rd(f'layer.plot{i}.color'), '| colorinc=', rd(f'layer.plot{i}.colorinc'))

# ===== ③ 线宽粒度 =====
print('\n--- ③ 线宽 / 字号粒度 ---')
for i in (1, 2, 3):
    print(f'  layer.plot{i}.line.width =', rd(f'layer.plot{i}.line.width'))
for cand in ('layer.plot1.line.width', 'layer.plot1.line.conn', 'layer.x.label.pt', 'layer.x.label.font',
             'layer.x.majorTicks', 'layer.x.minorTicks', 'layer.x.ticklen', 'layer.y.label.pt'):
    print(f'  读 {cand} =', rd(cand))

# ===== ① 底色 =====
print('\n--- ① 底色 ---')
for cand in ('page.color', 'layer.color', 'layer.background', 'layer.fill.color', 'layer.bgcolor'):
    print(f'  读 {cand} =', rd(cand))

def corners(p):
    im = Image.open(p).convert('RGB')
    w, h = im.size
    return im.size, [im.getpixel((1, 1)), im.getpixel((w - 2, 1)), im.getpixel((1, h - 2)), im.getpixel((w - 2, h - 2)),
                     im.getpixel((w // 2, h // 2))]

p0 = exp('bg_default.png', 'tr1.Unit:=2 tr1.Width:=800')
print('  默认导出角/中心像素:', corners(p0) if p0 else 'N/A')
# 试把底色设成暗色，看导出是否变化
print('  设暗底尝试:')
for cmd in ('page.color=15;', 'layer.color=15;', 'layer.background=15;'):
    print('    ', cmd, '->', run(cmd))
p1 = exp('bg_set.png', 'tr1.Unit:=2 tr1.Width:=800')
print('  设暗色后导出角/中心像素:', corners(p1) if p1 else 'N/A')
# 还原
for cmd in ('page.color=0;', 'layer.color=0;', 'layer.background=0;'):
    run(cmd)

# ===== ⑤ 去上/右框线 · 刻度朝内 · 只留主刻度 =====
print('\n--- ⑤ 框线 / 刻度 ---')
for cand in ('layer.x.opposite', 'layer.y.opposite', 'layer.x2.show', 'layer.y2.show',
             'layer.x.ticks', 'layer.x.majorTicks', 'layer.x.tick.direction', 'layer.x.tickdir',
             'layer.x.tickslen', 'layer.x.major.tick.direction'):
    print(f'  读 {cand} =', rd(cand))

# ===== ② 字体 =====
print('\n--- ② 字体族：候选设置命令 ---')
for cand in ('layer.x.label.font', 'layer.x.label.pt', 'layer.x.label.bold', 'xb.font', 'xb.pt',
             'xb.text$', 'layer.x.label.font$', 'layer.x.label.typeface$'):
    print(f'  读 {cand} =', rd(cand) if not cand.endswith('$') else rs(cand))

font_cmds = [
    'layer.x.label.font=0;',
    'layer.x.label.font$="Times New Roman";',
    'xb.font="Times New Roman";',
    'xb.font$="Times New Roman";',
    'xb.pt=14;',
    'set xb -fn "Times New Roman";',
    'label -fn "Times New Roman" -fs 14 -n xb;',
    'system.font.names$;',
]
for c in font_cmds:
    print(f'  执行 {c!r} -> {run(c)}')

print('  当前 xb.text$ =', repr(rs('xb.text$')), '| xb.font =', rd('xb.font'),
      '| layer.x.label.font =', rd('layer.x.label.font'))

# 导出，看内嵌字体
pf = exp('font_default.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
if pf:
    with fitz.open(pf) as d:
        print('  默认字体 PDF get_fonts() =', d[0].get_fonts())

# ===== ⑥ 中文字符 =====
print('\n--- ⑥ 中文字符 ---')
print('  set xb.text$ 中文 ->', run('xb.text$="温度 (°C)";'))
pn = exp('chinese.pdf', 'tr1.Unit:=0 tr1.Width:=6.31')
if pn:
    with fitz.open(pn) as d:
        print('  含中文 PDF get_fonts() =', d[0].get_fonts())
        print('  get_text() 前 120 =', repr(d[0].get_text()[:120]))

op.exit()
print('### probe_d_appearance done ###')
