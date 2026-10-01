# -*- coding: utf-8 -*-
"""probe_origin_font4b.py — 第四轮 B：**每次新起一个 Origin 进程**，验 OPDF.INI [Fonts] 是否在启动时读

上一支探针在同一会话里改 INI 发现产物完全不变 ⇒ 需要区分两种可能：
  (a) Origin 在**启动时**读一次 OPDF.INI；
  (b) Origin 读的是**安装目录** 的 opdf.ini（那个我不许动）。

做法：把用户 OPDF.INI 改成目标值 → **新起** Origin → 导出 → 退出 → 还原 INI。

用法: python tests/m3-origin-font-probe/probe_origin_font4b.py <embed> <outline> <tag>
"""
import os
import sys
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = os.path.join(REPO, "build", "m3-origin-probe", "site")
OUT = os.path.join(REPO, "build", "m3-origin-font", "origin")
INI = r"D:\Shameless\Documents\OriginLab\User Files\OPDF.INI"
BAK = os.path.join(OUT, "OPDF.INI.orig.bak")

sys.path.insert(0, SITE)
import originpro as op          # noqa: E402
import fitz                     # noqa: E402

LOG = []


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def set_ini(embed, outline):
    with open(BAK, "rb") as fh:
        txt = fh.read().decode("utf-8", "surrogateescape")
    out = []
    for ln in txt.split("\n"):
        s = ln.strip().lower()
        if s.startswith("embed="):
            ln = "Embed=%d" % embed
        if s.startswith("outlinemode="):
            ln = "OutLineMode=%d" % outline
        out.append(ln)
    with open(INI, "w", encoding="utf-8", newline="", errors="surrogateescape") as fh:
        fh.write("\n".join(out))


def main():
    embed, outline, tag = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    orig = open(BAK, "rb").read()
    orig_sha = hashlib.sha256(orig).hexdigest()
    set_ini(embed, outline)
    P("=== 本次: Embed=%d OutLineMode=%d tag=%s ===" % (embed, outline, tag))
    P("   INI 已设；启动 Origin")

    op.set_show(False)
    try:
        wks = op.new_sheet()
        wks.from_list(0, [0, 1, 2, 3, 4, 5])
        wks.from_list(1, [0, 1, 4, 9, 16, 25])
        gp = op.new_graph()
        gp[0].add_plot(wks, 1, 0)
        gp.activate()
        op.lt_exec('themeApply2g theme:="Times New Roman Font";')
        # 也加一条中文，看 outline 模式下中文字形在不在
        op.lt_exec('xb.text$ = "温度 (°C)";')
        p = os.path.join(OUT, "i_%s.pdf" % tag)
        gp.save_fig(p, width=1893)
        doc = fitz.open(p)
        page = doc[0]
        gf = [(f[3], f[2], f[1]) for f in page.get_fonts()]
        nd = len(page.get_drawings())
        txt = page.get_text().replace("\n", "|")
        doc.close()
        P("   get_fonts:", json.dumps(gf, ensure_ascii=False))
        P("   drawings :", nd)
        P("   text     :", json.dumps(txt[:200], ensure_ascii=False))
        raw = open(p, "rb").read()
        P("   /FontFile 计数:", raw.count(b"/FontFile"), "/FontFile2:", raw.count(b"/FontFile2"))
    except Exception as e:
        P("   EXC:", repr(e))
    finally:
        try:
            op.exit()
        except Exception as e:
            P("   op.exit EXC:", repr(e))
        with open(INI, "wb") as fh:
            fh.write(orig)
        P("   INI 还原一致:", hashlib.sha256(open(INI, "rb").read()).hexdigest() == orig_sha)
        with open(os.path.join(OUT, "probe4b_%s.log" % tag), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
