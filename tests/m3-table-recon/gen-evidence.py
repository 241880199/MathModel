#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""gen-evidence.py —— 把 build/ 里的原始 stdout 捕获归一化为 LF 并装配 out-*.txt。

shape 照 tests/m3-origin-probe/gen-evidence.py。

原始捕获（CRLF，Windows）→ out-*.txt（LF，入库）。
**能手改的只有归一化，不能改内容**：任何与今天事实不符的行，正确做法是重跑探针。
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(REPO, "build", "m3-table-recon")
OUT = os.path.join(REPO, "tests", "m3-table-recon")

PAIRS = [
    ("raw_probe_0.txt", "out-0-inventory.txt"),
    ("raw_probe_1.txt", "out-1-knownfact.txt"),
    ("raw_probe_2.txt", "out-2-corpus.txt"),
    ("raw_probe_3.txt", "out-3-controls.txt"),
]


def main():
    total_cr = 0
    for raw, out in PAIRS:
        src = os.path.join(RAW, raw)
        if not os.path.exists(src):
            print("!! 缺原始捕获: %s" % raw)
            continue
        data = open(src, "rb").read()
        cr = data.count(b"\r")
        total_cr += cr
        norm = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        dst = os.path.join(OUT, out)
        with open(dst, "wb") as fh:
            fh.write(norm)
        print("%-24s CR=%3d  -> %s (LF, %d bytes)" % (raw, cr, out, len(norm)))
    # 自查：本目录 out-*.txt 应当 CR=0
    bad = 0
    for _, out in PAIRS:
        p = os.path.join(OUT, out)
        if os.path.exists(p):
            d = open(p, "rb").read()
            if b"\r" in d:
                bad += 1
                print("!! %s 仍含 CR" % out)
    print("原始捕获裸 CR 合计 = %d；自查 out-*.txt 含 CR 的文件数 = %d" % (total_cr, bad))


if __name__ == "__main__":
    main()
