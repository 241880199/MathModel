#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_a_connect.py —— Origin 支线侦察 A 段：能不能驱动 / 版本 / 版别 / 干净退出。

只读 + 只在本进程内建一个临时实例；不改任何既有文件。
前置：`originpro` 已按 README 装到 build/m3-origin-probe/site（--target，--no-deps）。

跑法：
  python tests/m3-origin-probe/probe_a_connect.py > build/m3-origin-probe/raw_probe_a.txt 2>&1
"""
import os
import sys
import time
import platform

HERE = os.path.dirname(os.path.abspath(__file__))            # tests/m3-origin-probe
ROOT = os.path.dirname(os.path.dirname(HERE))                # 仓根
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)

print('### probe_a_connect start ###')
print('platform :', platform.platform())
print('python   :', sys.version.replace('\n', ' '), '|', sys.executable)
print('site path:', SITE, '| exists=', os.path.isdir(SITE))

try:
    import importlib.metadata as md
    for pkg in ('originpro', 'OriginExt', 'pywin32', 'numpy', 'pandas', 'Pillow', 'PyMuPDF'):
        try:
            print(f'pkg {pkg:10s}:', md.version(pkg))
        except Exception as e:                                # noqa: BLE001
            print(f'pkg {pkg:10s}: (未装) {type(e).__name__}')
except Exception as e:                                        # noqa: BLE001
    print('metadata 读取失败:', e)

t0 = time.time()
import originpro as op
print('import originpro: OK  (+%.2fs)' % (time.time() - t0))
print('originpro.__file__:', op.__file__)

# ---- 第一个 API 触碰会真正拉起 Origin 进程；先记录"未显式隐藏前"的可见性 ----
t0 = time.time()
try:
    show_before = op.get_show()
    print('首次 API 触碰耗时 %.2fs' % (time.time() - t0))
    print('op.get_show()  [未显式隐藏前，默认可见性]:', show_before)
except Exception as e:                                        # noqa: BLE001
    import traceback
    traceback.print_exc()
    print('!!! 连接失败，后续跳过')
    sys.exit(3)

# 显式隐藏
op.set_show(False)
print('op.get_show()  [set_show(False) 之后]:', op.get_show())

# ---- 版本 / 路径 ----
def ltvar(name):
    try:
        return op.po.LT_get_var(name)
    except Exception as e:                                    # noqa: BLE001
        return f'<err {type(e).__name__}: {e}>'

def ltstr(name):
    try:
        return op.po.LT_get_str(name)
    except Exception as e:                                    # noqa: BLE001
        return f'<err {type(e).__name__}: {e}>'

print('--- 版本探测 ---')
for v in ('@V', '@V1', '@V2', '@S', '@B'):
    print(f'LT_get_var({v!r}) =', ltvar(v))
print("op.path('u') [User Files] =", op.path('u'))
print("op.path('e') [Exe]        =", op.path('e'))
print("op.path('p') [project]    =", op.path('p'))

# ---- 版别探测：OriginPro vs Origin ----
print('--- 版别探测（OriginPro / Origin）---')
names = [n for n in dir(op.po) if any(k in n.lower() for k in ('lic', 'pro', 'vers', 'title', 'edition', 'name'))]
print('dir(op.po) 里含 lic/pro/vers/title/edition/name 的成员:', sorted(names))
try:
    print('op.po.LT_get_str("%B") [应用名?] =', ltstr('%B'))
except Exception as e:                                        # noqa: BLE001
    print('  %B 读取异常:', e)
# 常见候选系统变量
for v in ('@PT', '@LC', '@LCT', '@OR', '@SS'):
    print(f'候选 {v} =', ltvar(v))

# 看 ApplicationBase 公开方法里有没有"标题/许可"类
base_members = [n for n in dir(op.po) if not n.startswith('_')]
print('op.po 公开成员数:', len(base_members))
print('  GetMainWnd*:', [n for n in base_members if 'Main' in n or 'MainWnd' in n])
print('  GetVersion*:', [n for n in base_members if 'Version' in n])

# ---- 干净退出 ----
print('--- op.exit() ---')
t0 = time.time()
op.exit()
print('op.exit() 返回，耗时 %.2fs' % (time.time() - t0))
print('### probe_a_connect done ###')
