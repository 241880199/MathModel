#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D14 探针：三个 RED 场景（`red/brief-R{1,2,3}.md`）在 **Python 层**各能不能产出图并过判据。

数据**逐字取自** `tests/skills/figure-choose/red/README.md` §1 内联的 R1/R2/R3 表格
（权威副本是 `red/brief-R{1,2,3}.md`）。每个场景出 PNG + PDF，跑 `check-figure-style.py`。

复跑（仓根）：
  python tests/m3-plot-recon/d14_scenarios.py --out build/m3-plot-recon/d14
"""
import argparse
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHK = "tests/skills/figure-choose/check-figure-style.py"

DISTRICTS = list("ABCDEF")
# R1 / R3：三个脆弱度档的占比（每行和 = 1.00）
R1_LOW = [0.42, 0.31, 0.55, 0.28, 0.37, 0.50]
R1_MED = [0.35, 0.44, 0.30, 0.47, 0.38, 0.33]
R1_HIGH = [0.23, 0.25, 0.15, 0.25, 0.25, 0.17]
# R2：五个属性
R2 = {
    "Population density": [820, 640, 610, 1210, 990, 1750],
    "Mean slope": [3.2, 11.5, 2.4, 14.8, 7.1, 5.0],
    "Vegetation cover": [0.61, 0.58, 0.72, 0.41, 0.49, 0.55],
    "Disaster count": [12, 31, 8, 38, 16, 24],
    "Infrastructure index": [74, 72, 81, 55, 66, 70],
}

CAP_R1 = "Figure 1: Vulnerability composition by district"
CAP_R2 = "Figure 2: Correlation of district attributes with disaster count"
CAP_R3 = "Figure 3: Vulnerability composition by district, paper-ready"


def run_check(fig, caption, dpi, tw):
    cmd = ["python", CHK, "--fig", str(fig), "--caption", caption, "--textwidth-in", str(tw)]
    if str(fig).lower().endswith(".png"):
        cmd += ["--dpi", str(dpi)]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--textwidth", type=float, default=6.31)
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import numpy as np

    print(f"matplotlib = {matplotlib.__version__}（本机默认）")

    # ---- R1 构成：堆叠条（H6 说构成别画饼 —— 这里是合规替代）
    fig, ax = plt.subplots(figsize=(6.31, 2.6))
    bot = np.zeros(6)
    for vals, lab in ((R1_LOW, "low"), (R1_MED, "medium"), (R1_HIGH, "high")):
        ax.bar(DISTRICTS, vals, bottom=bot, label=lab, width=0.62)
        bot = bot + np.array(vals)
    ax.set_ylabel("Share of area")
    ax.legend(loc="upper center", ncol=3, fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    r1_png, r1_pdf = out / "R1_composition.png", out / "R1_composition.pdf"
    fig.savefig(r1_png, dpi=a.dpi)
    fig.savefig(r1_pdf)
    plt.close(fig)

    # ---- R2 多变量对比：各属性与灾害数的相关系数条（单序列）
    dc = np.array(R2["Disaster count"])
    labels, rs = [], []
    for k, v in R2.items():
        if k == "Disaster count":
            continue
        r = np.corrcoef(np.array(v), dc)[0, 1]
        labels.append(k)
        rs.append(r)
    order = np.argsort(rs)
    fig, ax = plt.subplots(figsize=(6.31, 2.6))
    ax.barh([labels[i] for i in order], [rs[i] for i in order], height=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Pearson r with disaster count")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    r2_png, r2_pdf = out / "R2_correlation.png", out / "R2_correlation.pdf"
    fig.savefig(r2_png, dpi=a.dpi)
    fig.savefig(r2_pdf)
    plt.close(fig)

    # ---- R3 交付形态：同一份构成，论文正文宽（6.31）单页 PDF
    fig, ax = plt.subplots(figsize=(6.31, 2.6))
    bot = np.zeros(6)
    for vals, lab in ((R1_LOW, "low"), (R1_MED, "medium"), (R1_HIGH, "high")):
        ax.bar(DISTRICTS, vals, bottom=bot, label=lab, width=0.62)
        bot = bot + np.array(vals)
    ax.set_ylabel("Share of area")
    ax.legend(loc="upper center", ncol=3, fontsize=7, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    r3_png, r3_pdf = out / "R3_delivery.png", out / "R3_delivery.pdf"
    fig.savefig(r3_png, dpi=a.dpi)
    fig.savefig(r3_pdf)
    plt.close(fig)

    for tag, png, pdf, cap in (("R1 构成", r1_png, r1_pdf, CAP_R1),
                               ("R2 多变量对比", r2_png, r2_pdf, CAP_R2),
                               ("R3 交付形态", r3_png, r3_pdf, CAP_R3)):
        print("=" * 78)
        print(f"### {tag} ###")
        for f in (png, pdf):
            rc, outt = run_check(f, cap, a.dpi, a.textwidth)
            print(f"  $ python {CHK} --fig {f} --caption {cap!r} --textwidth-in {a.textwidth}"
                  + (f" --dpi {a.dpi}" if f.suffix == ".png" else ""))
            print("    " + "\n    ".join(outt.rstrip().splitlines()))
            print(f"    ⇒ exit = {rc}")


if __name__ == "__main__":
    main()
