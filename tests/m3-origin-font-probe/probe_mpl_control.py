# -*- coding: utf-8 -*-
"""probe_mpl_control.py — 建"已知正确"的 matplotlib 对照图，并自检读数方法。

目的（任务书 §2.1.2）：证明我用 fitz 读 PDF 字体的方法**能区分** SimSun 与 Times 系。
若连这张对照都读不出差别，"我读到 Times"就是不可信的自证。

产出（全部落 build/m3-origin-font/mpl/，不入库）：
  ctrl_times.pdf   —— 全图 Times New Roman
  ctrl_simsun.pdf  —— 全图 SimSun
  ctrl_cjk_times.pdf  / ctrl_cjk_simsun.pdf —— 含中文标签（测 CJK 覆盖）
  glyph_times.png / glyph_simsun.png / glyph_side_by_side.png —— 字形对照（人眼判"像不像"）

用法: python tests/m3-origin-font-probe/probe_mpl_control.py
"""
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import fitz  # PyMuPDF

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "build", "m3-origin-font", "mpl")
os.makedirs(OUT, exist_ok=True)

LATIN = "Wavelength 0123456789"


def make(font, path, cjk=False, png=None):
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [font],
        "pdf.fonttype": 42,          # 内嵌 TrueType（不用 Type3）
        "axes.unicode_minus": False,
    })
    fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
    x = [0, 1, 2, 3, 4, 5]
    y = [0, 1, 4, 9, 16, 25]
    ax.plot(x, y, marker="o", lw=1.0, color="#333333")
    ax.set_xlabel("X axis (s)" if not cjk else "时间 温度")
    ax.set_ylabel("Y axis (m)" if not cjk else "温度 (°C)")
    ax.set_title(LATIN)
    ax.grid(False)
    fig.tight_layout()
    fig.savefig(path, format="pdf")
    if png:
        fig.savefig(png, format="png", dpi=100)
    plt.close(fig)
    return path


def read_pdf(path):
    """两层读数：page.get_fonts()（内嵌字体名） + span["font"]（谁用了哪个字体）"""
    doc = fitz.open(path)
    page = doc[0]
    fonts = [(f[3], f[2], f[4], f[5]) for f in page.get_fonts()]  # (basefont, type, refname, enc)
    spans = {}
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                spans.setdefault(s["font"], 0)
                spans[s["font"]] += len(s["text"])
    txt = page.get_text()
    doc.close()
    return {"get_fonts": fonts, "span_fonts": spans, "text": txt}


def main():
    results = {}
    for name, font in [("times", "Times New Roman"), ("simsun", "SimSun")]:
        p = make(font, os.path.join(OUT, "ctrl_%s.pdf" % name),
                 png=os.path.join(OUT, "glyph_%s.png" % name))
        results[name] = read_pdf(p)
    for name, font in [("cjk_times", "Times New Roman"), ("cjk_simsun", "SimSun")]:
        p = make(font, os.path.join(OUT, "ctrl_%s.pdf" % name), cjk=True)
        results[name] = read_pdf(p)

    # 解析 matplotlib 到底把 4 个字体名解析到了哪个文件（"值名承重"同型检查）
    resolve = {}
    for n in ["Times New Roman", "SimSun"]:
        try:
            resolve[n] = fm.findfont(fm.FontProperties(family=n), fallback_to_default=False)
        except Exception as e:
            resolve[n] = "ERR: %s" % e

    print("=== mpl 字体解析 ===")
    print(json.dumps(resolve, ensure_ascii=False, indent=2))
    for k, v in results.items():
        print("=== %s ===" % k)
        print("  get_fonts():", json.dumps(v["get_fonts"], ensure_ascii=False))
        print("  span fonts :", json.dumps(v["span_fonts"], ensure_ascii=False))
        print("  text       :", json.dumps(v["text"], ensure_ascii=False)[:200])

    # 自检判据：两组的内嵌字体名集合必须不同，且各自首名含预期关键词
    def names(r):
        return sorted({f[0] for f in r["get_fonts"]})
    nt, ns = names(results["times"]), names(results["simsun"])
    print("\n=== 读数方法自检 ===")
    print("Times 组内嵌名:", nt)
    print("SimSun 组内嵌名:", ns)
    distinguishable = (nt != ns)
    print("两组集合不同 =", distinguishable)
    print("Times 组含 TIMES(忽略大小写) =",
          any("times" in n.lower() for n in nt))
    print("SimSun 组含 SIMSUN(忽略大小写) =",
          any("simsun" in n.lower() for n in ns))

    with open(os.path.join(OUT, "mpl_control_readout.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump({"resolve": resolve, "results": results,
                   "distinguishable": bool(distinguishable)}, fh,
                  ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
