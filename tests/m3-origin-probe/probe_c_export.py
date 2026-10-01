#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_c_export.py —— 续 B：英寸单位 / 隐式裁剪（Margin 旋钮）/ 格式清单 /
DPI / PDF 是否矢量。

线索来源：安装目录 `OriginC/OriginLab/GraphicalExport.c`
  · 单位枚举 GUI: 0=inch 1=cm 2=pixel 3=ratio；Page: UNIT_INCH=0,CM=1,MM=2,PIXEL=3,POINT=4,RATIO=5
  · `tr.Margin` = Margin Control：0=Border, 1=Tight, 2=Page, 3=Tight in Page
  · `tr.Advanced.Resolution` = DPI

跑法：python tests/m3-origin-probe/probe_c_export.py > build/m3-origin-probe/raw_probe_c.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'c')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image
import fitz
import originpro as op

print('### probe_c_export start ###')
op.set_show(False)


def lt_var(n):
    try:
        return op.po.LT_get_var(n)
    except Exception as e:                                    # noqa: BLE001
        return f'<err {type(e).__name__}: {e}>'


def exp(name, extra):
    p = os.path.join(OUT, name)
    ext = os.path.splitext(name)[1][1:]
    cmd = f'expgraph type:={ext} path:="{OUT}" filename:="{name}" overwrite:=replace {extra}'
    op.po.LT_execute(cmd)
    return p if os.path.exists(p) else None


def m(path, label=''):
    if not path or not os.path.exists(path):
        print(f'  {label:26s} !!! 未产出')
        return None
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        try:
            with fitz.open(path) as d:
                r = d[0].rect
                print(f'  {label:26s} PDF 页盒 {r.width/72:.5f} x {r.height/72:.5f} in'
                      f'  ratio={r.width/r.height:.5f} bytes={os.path.getsize(path)}')
                return (r.width / 72.0, r.height / 72.0)
        except Exception as e:                                # noqa: BLE001
            print(f'  {label:26s} PDF 读不了 {type(e).__name__} bytes={os.path.getsize(path)}')
            return None
    try:
        with Image.open(path) as im:
            print(f'  {label:26s} PNG {im.size[0]} x {im.size[1]} px'
                  f'  ratio={im.size[0]/im.size[1]:.5f} bytes={os.path.getsize(path)}')
            return im.size
    except Exception as e:                                    # noqa: BLE001
        print(f'  {label:26s} (非图像 {type(e).__name__}) bytes={os.path.getsize(path)}')
        return None


wb = op.new_book('w', 'Data')
ws = wb[0]
x = np.linspace(0, 10, 41)
ws.from_list(0, x.tolist())
ws.from_list(1, (np.sin(x)).tolist())
ws.from_list(2, (np.cos(x)).tolist())
ws.set_labels(['X', 'Y1', 'Y2'], type_='L')
gp = op.new_graph('G1')
gl = gp[0]
gl.add_plot(ws, 'B')
gl.add_plot(ws, 'C')
gl.rescale()
op.wait('s', 0.3)

pw, ph, rx = lt_var('page.width'), lt_var('page.height'), lt_var('page.resx')
print('默认页面 = %.5f x %.5f in (page.width=%s resx=%s)' % (pw / rx, ph / rx, pw, rx))

print('\n--- 1. tr1.Unit:=0 (inch) 直接指定英寸 ---')
m(exp('in631.pdf', 'tr1.Unit:=0 tr1.Width:=6.31'), 'in631.pdf')
m(exp('in500.pdf', 'tr1.Unit:=0 tr1.Width:=5.00'), 'in500.pdf')
m(exp('in800.pdf', 'tr1.Unit:=0 tr1.Width:=8.00'), 'in800.pdf')
m(exp('in631.png', 'tr1.Unit:=0 tr1.Width:=6.31'), 'in631.png')

print('\n--- 2. tr1.Unit:=2 (pixel) 直接指定像素 ---')
for w in (600, 1200, 1893, 2400):
    m(exp(f'px{w}.png', f'tr1.Unit:=2 tr1.Width:={w}'), f'px{w}.png')

print('\n--- 3. 隐式裁剪：tr.Margin 四种取值（0=Border 1=Tight 2=Page 3=TightInPage）---')
for mv in (0, 1, 2, 3):
    m(exp(f'margin{mv}.png', f'tr.Margin:={mv} tr1.Unit:=0 tr1.Width:=6.31'), f'tr.Margin={mv}')
print('  对照 tr1.Margin:')
for mv in (1,):
    m(exp(f'tr1_margin{mv}.png', f'tr1.Margin:={mv} tr1.Unit:=0 tr1.Width:=6.31'), f'tr1.Margin={mv}')

print('\n--- 4. 同请求宽、不同 Margin 下边缘像素（判断是否裁到内容）---')
for f in ('margin0.png', 'margin1.png', 'margin2.png', 'margin3.png'):
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        im = Image.open(p).convert('RGB')
        w, h = im.size
        corners = [im.getpixel((1, 1)), im.getpixel((w - 2, 1)), im.getpixel((1, h - 2)), im.getpixel((w - 2, h - 2))]
        print(f'  {f}: size={im.size} 四角={corners}')

print('\n--- 5. DPI（tr.Advanced.Resolution）---')
for dpi in (72, 150, 300, 600):
    m(exp(f'dpi{dpi}.png', f'tr1.Unit:=0 tr1.Width:=6.31 tr.Advanced.Resolution:={dpi}'), f'dpi={dpi}')

print('\n--- 6. Height / KeepRatio 节点探测 ---')
m(exp('h_only.pdf', 'tr1.Unit:=0 tr1.Height:=3.0'), 'Height only')
m(exp('wh.pdf', 'tr1.Unit:=0 tr1.Width:=6.31 tr1.Height:=3.0'), 'W+H')
for node in ('tr1.KeepRatio', 'tr.KeepRatio', 'tr1.Rescaling', 'tr.Rescaling', 'tr1.Ratio'):
    m(exp(f'node_{node.replace(".","_")}.png', f'{node}:=0 tr1.Unit:=0 tr1.Width:=6.31'),
      f'{node}:=0')

print('\n--- 7. 格式清单 ---')
for ext in ('png', 'pdf', 'svg', 'emf', 'eps', 'tif', 'tiff', 'jpg', 'jpeg', 'bmp', 'gif', 'pcx', 'psd', 'wmf', 'cgm', 'dxf'):
    name = f'fmt_{ext}.{ext}'
    p = exp(name, 'tr1.Unit:=0 tr1.Width:=6.31')
    hdr = ''
    if p:
        with open(p, 'rb') as fh:
            hdr = fh.read(8).hex()
    print(f'  type:{ext:5s} 产出={bool(p)} bytes={os.path.getsize(p) if p else 0} hdr={hdr}')

print('\n--- 8. PDF 矢量性 + 内嵌字体 ---')
p = os.path.join(OUT, 'in631.pdf')
if os.path.exists(p):
    with fitz.open(p) as d:
        pg = d[0]
        print('  get_images() =', pg.get_images())
        print('  get_drawings() 数 =', len(pg.get_drawings()))
        print('  get_fonts() =', pg.get_fonts())
        print('  get_text() 前 200 字 =', repr(pg.get_text()[:200]))

op.exit()
print('### probe_c_export done ###')
