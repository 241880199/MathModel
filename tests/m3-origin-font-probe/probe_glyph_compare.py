# -*- coding: utf-8 -*-
"""probe_glyph_compare.py — SimSun 的拉丁字形与 Times 系像不像（人眼判 + 量）

任务书 §2.1.3：出两张同内容图并排看，给"你自己的判断 + 依据"。
中文与拉丁**分开说**。

产出（build/m3-origin-font/mpl/）：
  glyph_ab.png        —— 拉丁样本，上 SimSun / 下 Times New Roman（同一 pt，左对齐）
  glyph_cjk_ab.png    —— 中文样本，上 SimSun / 下 Times（Times 应缺字）
  glyph_metrics.json  —— 字形宽度（advance width）逐字
"""
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(REPO, "build", "m3-origin-font", "mpl")
os.makedirs(OUT, exist_ok=True)

LATIN = "Wavelength 0123456789 Rg aQ"
CJK = "温度 时间 数据"

res = {}
for n in ["Times New Roman", "SimSun"]:
    res[n] = Fit = matplotlib.font_manager.findfont(
        FontProperties(family=n), fallback_to_default=False)

fig = plt.figure(figsize=(7.0, 2.2), dpi=200)
fig.patch.set_facecolor("white")
for i, (n, label) in enumerate([("SimSun", "SimSun"), ("Times New Roman", "Times New Roman")]):
    fig.text(0.02, 0.72 - i * 0.42, LATIN, fontsize=21, family=n, color="black")
    fig.text(0.90, 0.74 - i * 0.42, label, fontsize=7, family="DejaVu Sans", color="gray")
fig.savefig(os.path.join(OUT, "glyph_ab.png"), facecolor="white")
plt.close(fig)

fig = plt.figure(figsize=(5.0, 2.0), dpi=200)
fig.patch.set_facecolor("white")
for i, n in enumerate(["SimSun", "Times New Roman"]):
    fig.text(0.05, 0.65 - i * 0.45, CJK, fontsize=21, family=n, color="black")
    fig.text(0.70, 0.68 - i * 0.45, n, fontsize=7, family="DejaVu Sans", color="gray")
fig.savefig(os.path.join(OUT, "glyph_cjk_ab.png"), facecolor="white")
plt.close(fig)

# 量的部分：逐字符 advance width（字形宽度），用 TextToPath 取路径宽度
metrics = {}
for n in ["Times New Roman", "SimSun"]:
    fp = FontProperties(family=n, size=100)
    per = {}
    for ch in "WagR09":
        try:
            verts, codes = TextToPath().get_text_path(fp, ch)[0], None
            import matplotlib.path as mpath
            p = TextToPath().get_text_path(fp, ch)[0]
            xs = [v[0] for v in p]
            per[ch] = round(max(xs) - min(xs), 1) if xs else None
        except Exception as e:
            per[ch] = "ERR:%s" % e
    metrics[n] = per

print("=== 字体解析 ===")
print(json.dumps(res, ensure_ascii=False))
print("=== 逐字符墨迹宽度 @100pt ===")
print(json.dumps(metrics, ensure_ascii=False, indent=2))
with open(os.path.join(OUT, "glyph_metrics.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"resolved": res, "ink_width_100pt": metrics}, fh,
              ensure_ascii=False, indent=2)
print("wrote:", OUT)
