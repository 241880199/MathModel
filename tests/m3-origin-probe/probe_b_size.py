#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_b_size.py —— ★ 头号问题：Origin 导出物的"图宽"能不能被设定？

测法：建一张确定数据的图，按多种参数导出 PNG/PDF，**用 Pillow/fitz 量像素与页盒**（不目测），
并把每次 `save_fig` 实际发出的 LabTalk 命令原样打出。

关键 API：`GPage.save_fig(path, type, replace, width, ratio)`
  · width>0 时发 `expgraph ... tr1.Unit:=2 tr1.Width:{width}`（Unit 2 = GUI_UNIT_PIXEL）
  · 另设 `ratio` 只在 emf/svg 生效

跑法：python tests/m3-origin-probe/probe_b_size.py > build/m3-origin-probe/raw_probe_b.txt 2>&1
"""
import os
import sys
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)
OUT = os.path.join(ROOT, 'build', 'm3-origin-probe', 'b')
os.makedirs(OUT, exist_ok=True)

import numpy as np
from PIL import Image
import fitz
import originpro as op

print('### probe_b_size start ###')
op.set_show(False)


def lt_var(name):
    try:
        return op.po.LT_get_var(name)
    except Exception as e:                                    # noqa: BLE001
        return f'<err {type(e).__name__}: {e}>'


def lt_str(name):
    try:
        return op.po.LT_get_str(name)
    except Exception as e:                                    # noqa: BLE001
        return f'<err {type(e).__name__}: {e}>'


def measure(path):
    """返回 (kind, w, h, unit) —— PNG 用像素；PDF 用页盒英寸。"""
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        with fitz.open(path) as d:
            r = d[0].rect
            return ('PDF 页盒', r.width / 72.0, r.height / 72.0, 'in', d.page_count, d.is_pdf)
    with Image.open(path) as im:
        return ('PNG 像素', im.size[0], im.size[1], 'px', 1, None)


def report(tag, path):
    if not os.path.exists(path):
        print(f'  [{tag}] 产物不存在: {path}')
        return
    kind, w, h, unit, pages, ispdf = measure(path)
    sz = os.path.getsize(path)
    print(f'  [{tag}] {os.path.basename(path)}: {kind} w={w} h={h} {unit}  ratio(w/h)={w/h:.4f}  bytes={sz}')
    if ispdf is not None:
        print(f'        page_count={pages} is_pdf={ispdf}')
    return w, h


# ---------- 1. 数据 + 图 ----------
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

# ---------- 2. 页面尺寸（打印机点 / DPI） ----------
print('--- 图的默认页面尺寸 ---')
for v in ('page.width', 'page.height', 'page.resx', 'page.resy', 'page.units'):
    print(f'  {v} =', lt_var(v))
try:
    pw, ph, rx, ry = (op.po.LT_get_var('page.width'), op.po.LT_get_var('page.height'),
                      op.po.LT_get_var('page.resx'), op.po.LT_get_var('page.resy'))
    print(f'  => 页面物理尺寸: {pw/rx:.4f} x {ph/ry:.4f} in')
except Exception as e:                                        # noqa: BLE001
    print('  计算页面物理尺寸失败:', e)

# ---------- 3. save_fig 各种 width 导出 ----------
print('\n--- 3a. save_fig(width=N) 导 PNG（tr1.Unit:=2 = 像素）---')
for w in (600, 900, 1200, 1800, 2400):
    p = os.path.join(OUT, f'png_w{w}.png')
    gp.save_fig(p, width=w)
    report(f'width={w}', p)

print('\n--- 3b. save_fig() 不给 width（走"上次导出设置"）---')
p = os.path.join(OUT, 'png_auto.png')
gp.save_fig(p)
report('auto', p)
# 再跑一次，看是否受上一次 2400 影响
p = os.path.join(OUT, 'png_auto2.png')
gp.save_fig(p)
report('auto2', p)

print('\n--- 3c. save_fig(width=N) 导 PDF ---')
for w in (900, 1800):
    p = os.path.join(OUT, f'pdf_w{w}.pdf')
    gp.save_fig(p, width=w)
    report(f'pdf width={w}', p)
p = os.path.join(OUT, 'pdf_auto.pdf')
gp.save_fig(p)
report('pdf auto', p)

# ---------- 4. 裸 LabTalk：inch / cm / height ----------
print('\n--- 4. 裸 expgraph：换 Unit（0=in,1=cm,2=px）与 Height ---')
def raw_exp(extra, name):
    p = os.path.join(OUT, name)
    cmd = f'expgraph type:={os.path.splitext(name)[1][1:]} path:="{OUT}" filename:="{name}" overwrite:=replace {extra}'
    op.po.LT_execute(cmd)
    print('  cmd:', cmd)
    report('raw', p)

raw_exp('tr1.Unit:=0 tr1.Width:=6.31', 'raw_in_w631.png')       # 6.31 英寸
raw_exp('tr1.Unit:=1 tr1.Width:=16', 'raw_cm_w16.png')          # 16 cm
raw_exp('tr1.Unit:=2 tr1.Width:=1000 tr1.Height:=500', 'raw_px_wh.png')
raw_exp('tr1.Unit:=0 tr1.Width:=6.31 tr.Advanced.Resolution:=300', 'raw_in_w631_dpi300.png')

# ---------- 5. 读回"上次导出设置"看有没有别的尺寸旋钮 ----------
print('\n--- 5. 导出设置树（LABTALK 侧有哪些可写节点）---')
for e in ('tr1.Unit', 'tr1.Width', 'tr1.Height', 'tr.Advanced.Resolution'):
    try:
        print(f'  当前 {e} =', lt_var(e))
    except Exception as ex:                                   # noqa: BLE001
        print(f'  {e} 读取异常:', ex)

op.exit()
print('### probe_b_size done ###')
