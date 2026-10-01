# -*- coding: utf-8 -*-
"""probe_origin_font4.py — 第四轮：OPDF.INI [Fonts] 的 Embed / OutLineMode 有没有用

背景：fitz 读到 Origin 导出的 PDF **一个 /FontFile 都没有**（ext='n/a'）——
即"字体根本没内嵌，只是按名字引用"。安装目录 `opdf.ini` 的 [Fonts] 段写着：

    ; Embedding
    ; 0 = none, only font descriptor (default)
    ; 1 = embedded
    ; 2 = outline fonts
    Embed=0

★ 纪律：这里**只临时改**用户配置 `Documents/OriginLab/User Files/OPDF.INI`，
  跑完**按字节还原并用 sha256 核对**；绝不动安装目录。

本脚本在**一个** Origin 会话里，逐个改 INI 再导出，看读数变不变。
（若全不变 ⇒ Origin 在启动时读一次，下面的结论要改成"会话内改无效"。）

用法: python tests/m3-origin-font-probe/probe_origin_font4.py
"""
import os
import sys
import json
import hashlib
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = os.path.join(REPO, "build", "m3-origin-probe", "site")
OUT = os.path.join(REPO, "build", "m3-origin-font", "origin")
os.makedirs(OUT, exist_ok=True)
INI = r"D:\Shameless\Documents\OriginLab\User Files\OPDF.INI"

sys.path.insert(0, SITE)
import originpro as op          # noqa: E402
import fitz                     # noqa: E402

LOG = []


def P(*a):
    line = " ".join(str(x) for x in a)
    print(line, flush=True)
    LOG.append(line)


def read_pdf(pdf):
    doc = fitz.open(pdf)
    page = doc[0]
    gf = [(f[3], f[2], f[1]) for f in page.get_fonts()]     # basefont, type, ext
    ndraw, nimg = len(page.get_drawings()), len(page.get_images())
    spans = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                spans[s["font"]] = spans.get(s["font"], 0) + len(s["text"])
    txt = page.get_text().replace("\n", "|")
    doc.close()
    return gf, spans, ndraw, nimg, txt


def snap(tag, pdf):
    gf, spans, nd, ni, txt = read_pdf(pdf)
    P("### %s  [%s]" % (tag, os.path.basename(pdf)))
    P("    (basefont, type, ext):", json.dumps(gf, ensure_ascii=False), "drawings=%d" % nd)
    P("    spans:", json.dumps(spans, ensure_ascii=False))
    return {"fonts": gf, "spans": spans, "drawings": nd, "text": txt}


def new_graph():
    wks = op.new_sheet()
    wks.from_list(0, [0, 1, 2, 3, 4, 5])
    wks.from_list(1, [0, 1, 4, 9, 16, 25])
    gp = op.new_graph()
    gp[0].add_plot(wks, 1, 0)
    gp.activate()
    return gp


def set_ini(embed=None, outline=None):
    """改用户 OPDF.INI 的 [Fonts] 段（只动这两行），返回新内容"""
    with open(INI, "r", encoding="utf-8", errors="surrogateescape") as fh:
        txt = fh.read()
    lines = txt.split("\n")
    outl = []
    for ln in lines:
        s = ln.strip()
        if embed is not None and s.lower().startswith("embed="):
            ln = "Embed=%d" % embed
        if outline is not None and s.lower().startswith("outlinemode="):
            ln = "OutLineMode=%d" % outline
        outl.append(ln)
    with open(INI, "w", encoding="utf-8", newline="", errors="surrogateescape") as fh:
        fh.write("\n".join(outl))
    return "\n".join(outl)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    orig_bytes = open(INI, "rb").read()
    orig_sha = hashlib.sha256(orig_bytes).hexdigest()
    P("=== OPDF.INI 备份 ===")
    P("path:", INI)
    P("sha256(原):", orig_sha, "bytes:", len(orig_bytes))
    with open(os.path.join(OUT, "OPDF.INI.orig.bak"), "wb") as fh:
        fh.write(orig_bytes)

    op.set_show(False)
    ctx = {"orig_sha": orig_sha}
    try:
        gp = new_graph()
        op.lt_exec('themeApply2g theme:="Times New Roman Font";')

        for tag, embed, outline in [
            ("baseline_Embed0", 0, 0),
            ("embed1", 1, 0),
            ("embed2_outline", 2, 0),
            ("embed1_outline1", 1, 1),
        ]:
            body = set_ini(embed, outline)
            P("  INI -> Embed=%s OutLineMode=%s" % (embed, outline))
            p = os.path.join(OUT, "h_%s.pdf" % tag)
            gp.save_fig(p, width=1893)
            ctx[tag] = snap("H %s" % tag, p)

        # 顺带：把 INI 的当前样子留档
        with open(os.path.join(OUT, "OPDF.INI.during-test.txt"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write(body)

    except Exception:
        P("!!! EXCEPTION !!!")
        P(traceback.format_exc())
    finally:
        P("\n=== op.exit() ===")
        try:
            op.exit()
            P("op.exit() 返回")
        except Exception as e:
            P("op.exit() 抛异常:", repr(e))

        # ---- 还原（在 Origin 退出之后）----
        with open(INI, "wb") as fh:
            fh.write(orig_bytes)
        now = sha(INI)
        P("=== OPDF.INI 还原 ===")
        P("sha256(还原后):", now)
        P("逐字节一致:", now == orig_sha)
        ctx["restored_sha"] = now
        ctx["restored_identical"] = (now == orig_sha)

        with open(os.path.join(OUT, "probe_origin_font4.log"), "w",
                  encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LOG) + "\n")
        with open(os.path.join(OUT, "probe_origin_font4.json"), "w",
                  encoding="utf-8", newline="\n") as fh:
            json.dump(ctx, fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
