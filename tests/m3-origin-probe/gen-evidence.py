#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen-evidence.py —— 把 build/m3-origin-probe/raw_*.txt（Windows CRLF 捕获）归一化为
LF 并装配成本目录的 out-*.txt。

纪律：out-*.txt 是**逐字 stdout 捕获**，手改=造伪。要更新就重跑探针再跑本脚本。
本脚本**只做一件事**：CRLF→LF（并逐份打印原始 CR 计数，作为"归一化确实发生"的证据）。
用 write_bytes（LF），**不用 write_text**（Windows 会写 CRLF）。

跑法：python tests/m3-origin-probe/gen-evidence.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BUILD = os.path.join(ROOT, 'build', 'm3-origin-probe')

# out 文件名 -> [raw 文件（按序拼接）]
MAP = {
    'out-a-connect-version-edition.txt': ['raw_probe_a.txt', 'raw_probe_a2.txt'],
    'out-b-export-size.txt': ['raw_probe_b.txt'],
    'out-c-export-margin-formats.txt': ['raw_probe_c.txt'],
    'out-d-appearance.txt': ['raw_probe_d.txt'],
    'out-e-font-palette-axis.txt': ['raw_probe_e.txt'],
    'out-f-axis-candidates.txt': ['raw_probe_f.txt'],
    'out-g-e2e-scenarios.txt': ['raw_probe_g.txt'],
    'out-h-f2-bars.txt': ['raw_probe_h.txt'],
    'out-i-dpi-pagesize-frame.txt': ['raw_probe_i.txt'],
    'out-j-env-prereq-residual.txt': ['raw_probe_j.txt'],
    'out-checks-figure-style.txt': ['raw_checks_manual.txt'],
}


def main():
    total_cr = 0
    for out, raws in MAP.items():
        parts = []
        for r in raws:
            p = os.path.join(BUILD, r)
            if not os.path.exists(p):
                print(f'!! 缺 {r}（先跑对应探针）')
                sys.exit(1)
            data = open(p, 'rb').read()
            cr = data.count(b'\r')
            total_cr += cr
            print(f'  {r:28s} 原始 CR={cr:4d}  bytes={len(data)}')
            parts.append(data)
        blob = b''.join(parts).replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        dst = os.path.join(HERE, out)
        with open(dst, 'wb') as f:
            f.write(blob)          # LF
        chk = open(dst, 'rb').read()
        print(f'  -> {out:40s} 写入 {len(chk)} bytes, 复查 CR={chk.count(chr(13).encode())}')
    print(f'合计原始裸 CR = {total_cr}')


if __name__ == '__main__':
    main()
