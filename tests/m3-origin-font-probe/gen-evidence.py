# -*- coding: utf-8 -*-
"""gen-evidence.py — 把 build/ 下的探针输出归一化成入库证据（LF），并核对字节

用法: python tests/m3-origin-font-probe/gen-evidence.py
产物: 本目录下的 out-*.txt / *.json（LF 行尾）+ 控制台打印裸 CR 计数
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
B = os.path.join(REPO, "build", "m3-origin-font")

COPIES = [
    # (源, 目标)
    (os.path.join(B, "mpl", "probe_mpl_control.raw"), "out-mpl-control.txt"),
    (os.path.join(B, "mpl", "probe_glyph_compare.raw"), "out-mpl-glyph-compare.txt"),
    (os.path.join(B, "origin", "probe_origin_font.log"), "out-origin-1-round1.txt"),
    (os.path.join(B, "origin", "probe_origin_font2.log"), "out-origin-2-round2.txt"),
    (os.path.join(B, "origin", "probe_origin_font3.log"), "out-origin-3-round3.txt"),
    (os.path.join(B, "origin", "probe_origin_font4.log"), "out-origin-4-same-session-ini.txt"),
    (os.path.join(B, "origin", "probe4b_embed1.log"), "out-origin-4b-embed1.txt"),
    (os.path.join(B, "origin", "probe4b_embed2.log"), "out-origin-4b-embed2.txt"),
    (os.path.join(B, "origin", "probe4b_embed1_out1.log"), "out-origin-4b-embed1-out1.txt"),
    (os.path.join(B, "origin", "probe_origin_font5.log"), "out-origin-5-round5.txt"),
    (os.path.join(B, "origin", "probe_origin_font6.log"), "out-origin-6-round6.txt"),
    (os.path.join(B, "pdf-readout.txt"), "out-pdf-font-readout.txt"),
    (os.path.join(B, "checker-runs.txt"), "out-checker-runs.txt"),
    # 第 7 轮：**无效探针**的原始读数（保留备查，报告里明确标注它不算证据）
    (os.path.join(B, "origin", "probe_origin_font7.log"), "out-origin-7-VOID.txt"),
]


def norm(src, dst):
    with open(src, "rb") as fh:
        raw = fh.read()
    cr = raw.count(b"\r")
    data = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    with open(dst, "wb") as fh:
        fh.write(data)
    return cr, len(data)


def main():
    total_cr = 0
    for src, dst in COPIES:
        if not os.path.exists(src):
            print("MISSING:", src)
            continue
        cr, n = norm(src, os.path.join(HERE, dst))
        total_cr += cr
        print("%-38s CR=%d -> %s (%d B)" % (os.path.basename(src), cr, dst, n))

    # 二进制对照图（≤200 KB 才入库）
    for src, dst in [
        (os.path.join(B, "mpl", "glyph_ab.png"), "ctrl-mpl-glyph-ab.png"),
        (os.path.join(B, "mpl", "glyph_cjk_ab.png"), "ctrl-mpl-glyph-cjk-ab.png"),
    ]:
        if os.path.exists(src):
            n = os.path.getsize(src)
            if n <= 200 * 1024:
                shutil.copyfile(src, os.path.join(HERE, dst))
                print("copied %-26s %d B" % (dst, n))
            else:
                print("SKIP (too big) %s %d B" % (src, n))

    # 入库文件 CR 自查
    print("\n=== 本目录入库文本文件 CR 自查 ===")
    bad = 0
    for f in sorted(os.listdir(HERE)):
        p = os.path.join(HERE, f)
        if os.path.isfile(p) and f.lower().endswith((".txt", ".json", ".py", ".md")):
            with open(p, "rb") as fh:
                c = fh.read().count(b"\r")
            if c:
                bad += 1
                print("  CR!=0:", f, c)
    print("有裸 CR 的文件数:", bad)
    print("归一化共消除裸 CR:", total_cr)


if __name__ == "__main__":
    main()
