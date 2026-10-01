#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_a2_edition.py —— 定版：这是 OriginPro 还是 Origin？

手段（任一可读即记录）：
  1. 运行中 Origin 主窗口标题（win32gui 枚举顶层窗口）—— OriginPro 版的标题里带 "OriginPro"。
  2. LabTalk 候选系统变量。
  3. 版本号 @V。

跑法：
  python tests/m3-origin-probe/probe_a2_edition.py > build/m3-origin-probe/raw_probe_a2.txt 2>&1
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SITE = os.path.join(ROOT, 'build', 'm3-origin-probe', 'site')
sys.path.insert(0, SITE)

print('### probe_a2_edition start ###')
import originpro as op

op.set_show(False)               # 先隐藏，再探测
print('op.get_show() =', op.get_show())

# --- 手段 1：顶层窗口标题 ---
try:
    import win32gui
    rows = []

    def _cb(hwnd, _):
        t = win32gui.GetWindowText(hwnd)
        if 'Origin' in t or 'origin' in t:
            rows.append((hwnd, bool(win32gui.IsWindowVisible(hwnd)), t))
    win32gui.EnumWindows(_cb, None)
    print('枚举到含 Origin 的顶层窗口数:', len(rows))
    for h, vis, t in rows:
        print(f'  hwnd={h} visible={vis} title={t!r}')
except Exception as e:                                        # noqa: BLE001
    import traceback
    traceback.print_exc()

# --- 手段 2：LabTalk 候选 ---
print('--- LabTalk 候选变量 ---')
for v in ('@V', '@PT', '@OR', '@LC', '@SS', '@V3'):
    try:
        print(f'  LT_get_var({v!r}) =', op.po.LT_get_var(v))
    except Exception as e:                                    # noqa: BLE001
        print(f'  LT_get_var({v!r}) err:', type(e).__name__, e)

# --- 手段 3：读 Origin 自己的信息串 ---
print('--- 其它可读串 ---')
for expr in ('%@PT', '%B', '%H', '%N'):
    try:
        print(f'  LT_get_str({expr!r}) =', repr(op.po.LT_get_str(expr)))
    except Exception as e:                                    # noqa: BLE001
        print(f'  LT_get_str({expr!r}) err:', type(e).__name__, e)

# --- 手段 4：Pro-only X-Function 探测（非线性拟合 nlfit 属 Pro 功能） ---
print('--- Pro-only 功能探测 ---')
for lt in ('nlfit', 'fitlr', 'img2m', 'xyz2m'):
    try:
        op.po.LT_execute(f'{lt};')
        print(f'  执行 `{lt};` : 无异常')
    except Exception as e:                                    # noqa: BLE001
        print(f'  执行 `{lt};` err:', type(e).__name__, e)

op.exit()
print('### probe_a2_edition done ###')
