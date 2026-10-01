#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_checks.py --- run the shipped product checker (check-figure-style.py) on the
MATLAB artifacts, one line per invocation, capturing the verdicts verbatim.

The checker is NOT copied and NOT modified: it is invoked by path. Denominator is the
repo convention --textwidth-in 6.31.

re-run from repo root:
  python tests/m3-matlab-recon/probe_checks.py
"""
import subprocess
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CHK = ROOT / "tests/skills/figure-choose/check-figure-style.py"
B = ROOT / "build/m3-matlab-recon"

# (label, fig path, caption, dpi or None)
CAP_GOOD = "Figure 1: Two sample series"
CAP_BAD = "Figure 1. This figure shows the two sample series under baseline conditions for the study area."
CAP_R1 = "Figure 1: Vulnerability composition by district"
CAP_R2 = "Figure 1: Correlation of each factor with disaster count"

CASES = [
    ("C default-N1 png",   B / "c/c_defN1.png",  CAP_GOOD, 200),
    ("C default-N1 pdf",   B / "c/c_defN1.pdf",  CAP_GOOD, None),
    ("C default-N2 png",   B / "c/c_defN2.png",  CAP_GOOD, 200),
    ("C default-N2 pdf",   B / "c/c_defN2.pdf",  CAP_GOOD, None),
    ("C default-N3 png",   B / "c/c_defN3.png",  CAP_GOOD, 200),
    ("C default-N3 pdf",   B / "c/c_defN3.pdf",  CAP_GOOD, None),
    ("C default-N4 png",   B / "c/c_defN4.png",  CAP_GOOD, 200),
    ("C default-N4 pdf",   B / "c/c_defN4.pdf",  CAP_GOOD, None),
    ("C default-N5 png",   B / "c/c_defN5.png",  CAP_GOOD, 200),
    ("C default-N5 pdf",   B / "c/c_defN5.pdf",  CAP_GOOD, None),
    ("C default-N6 png",   B / "c/c_defN6.png",  CAP_GOOD, 200),
    ("C default-N6 pdf",   B / "c/c_defN6.pdf",  CAP_GOOD, None),
    ("C default-N7 png",   B / "c/c_defN7.png",  CAP_GOOD, 200),
    ("C default-N7 pdf",   B / "c/c_defN7.pdf",  CAP_GOOD, None),
    ("C manual-N2 png",    B / "c/c_manN2.png",  CAP_GOOD, 200),
    ("C manual-N2 pdf",    B / "c/c_manN2.pdf",  CAP_GOOD, None),
    ("C manual-N3 png",    B / "c/c_manN3.png",  CAP_GOOD, 200),
    ("C manual-N3 pdf",    B / "c/c_manN3.pdf",  CAP_GOOD, None),
    ("C manual-N4 png",    B / "c/c_manN4.png",  CAP_GOOD, 200),
    ("C manual-N4 pdf",    B / "c/c_manN4.pdf",  CAP_GOOD, None),
    ("S2 good exportgraphics png",  B / "f/s2_good.png",     CAP_GOOD, 200),
    ("S2 good exportgraphics pdf",  B / "f/s2_good.pdf",     CAP_GOOD, None),
    ("S2 good print png",           B / "f/s2_good_pr.png",  CAP_GOOD, 200),
    ("S2 good print pdf",           B / "f/s2_good_pr.pdf",  CAP_GOOD, None),
    ("S2 good saveas png",          B / "f/s2_good_sa.png",  CAP_GOOD, 150),
    ("S2 good saveas pdf",          B / "f/s2_good_sa.pdf",  CAP_GOOD, None),
    ("S2 good caption BAD variant", B / "f/s2_good_pr.png",  CAP_BAD, 200),
    ("S3 bad exportgraphics png",   B / "f/s3_bad.png",      CAP_BAD, 200),
    ("S3 bad exportgraphics pdf",   B / "f/s3_bad.pdf",      CAP_BAD, None),
    ("S3 bad print png",            B / "f/s3_bad_pr.png",   CAP_BAD, 200),
    ("S3 bad print pdf",            B / "f/s3_bad_pr.pdf",   CAP_BAD, None),
    ("S4 R1 stacked png",           B / "f/s4_R1.png",       CAP_R1, 200),
    ("S4 R1 stacked pdf",           B / "f/s4_R1.pdf",       CAP_R1, None),
    ("S5 R2 corrbar png",           B / "f/s5_R2.png",       CAP_R2, 200),
    ("S5 R2 corrbar pdf",           B / "f/s5_R2.pdf",       CAP_R2, None),
    ("S6 R3 exportgraphics pdf",    B / "f/s6_R3.pdf",       CAP_R1, None),
    ("S6 R3 print -dpdf",           B / "f/s6_R3_pr.pdf",    CAP_R1, None),
    ("S6 R3 exportgraphics png",    B / "f/s6_R3.png",       CAP_R1, 200),
    ("D r5_w631 eg pdf",            B / "d/r5_w631_eg.pdf",  CAP_GOOD, None),
    ("D r5_w631 eg png",            B / "d/r5_w631_eg.png",  CAP_GOOD, 200),
    ("D r5_w631 print pdf",         B / "d/r5_w631_pr.pdf",  CAP_GOOD, None),
    ("D r5_w631 print png",         B / "d/r5_w631_pr.png",  CAP_GOOD, 200),
    ("D r5_w400 eg pdf",            B / "d/r5_w400_eg.pdf",  CAP_GOOD, None),
    ("D r5_w800 eg pdf",            B / "d/r5_w800_eg.pdf",  CAP_GOOD, None),
    ("D r5_w1000 eg pdf",           B / "d/r5_w1000_eg.pdf", CAP_GOOD, None),
    ("D r5_w1200 eg pdf",           B / "d/r5_w1200_eg.pdf", CAP_GOOD, None),
    # ---- theme / background round (probe_h): does a BLACK figure pass every criterion? ----
    ("H T5 exportgraphics png (dark)",  B / "h_off/T5_eg1.png",      CAP_GOOD, 200),
    ("H T6 print png (dark)",           B / "h_off/T6_pr1.png",      CAP_GOOD, 200),
    ("H T7 new-figure png (dark)",      B / "h_off/T7_newfig.png",   CAP_GOOD, 200),
    ("H C1 figure+axes Color=w png",    B / "h_off/C1_colorw.png",   CAP_GOOD, 200),
    ("H L1 theme-light eg png",         B / "h_off/L1_light_eg.png", CAP_GOOD, 200),
    ("H L1 theme-light eg pdf",         B / "h_off/L1_light_eg.pdf", CAP_GOOD, None),
    ("H L1 theme-light print png",      B / "h_off/L1_light_pr.png", CAP_GOOD, 200),
    ("H L1 theme-light print pdf",      B / "h_off/L1_light_pr.pdf", CAP_GOOD, None),
    ("H P label-heavy eg png (dark)",   B / "h_off/P_eg.png",        CAP_GOOD, 200),
    ("H P label-heavy eg pdf (dark)",   B / "h_off/P_eg.pdf",        CAP_GOOD, None),
    ("H P label-heavy print png (dark)", B / "h_off/P_pr.png",       CAP_GOOD, 200),
    ("H P label-heavy print pdf (dark)", B / "h_off/P_pr.pdf",       CAP_GOOD, None),
    # ---- which theme fix actually produces a light figure? ----
    ("I W1 figure(...,'Theme','light') png", B / "i/W1_newlight.png",  CAP_GOOD, 200),
    ("I W2 theme(fig,'light')+colors png",   B / "i/W2_themelight.png", CAP_GOOD, 200),
    ("I W3 theme('light') no-handle png",    B / "i/W3_newfig.png",    CAP_GOOD, 200),
    ("D r5_w600 eg pdf",           B / "d/r5_w600_eg.pdf",  CAP_GOOD, None),
    ("G g1 PaperSize=[6.31 2.6] print -dpdf", B / "g/g1_ps63_pr.pdf", CAP_GOOD, None),
    ("G g1 PaperSize=[6.31 2.6] print -dpng", B / "g/g1_ps63_pr.png", CAP_GOOD, 200),
    ("G g2 PaperSize=[6.31 2.6] auto print -dpdf", B / "g/g2_auto_pr.pdf", CAP_GOOD, None),
    ("G g3 A4 control print -dpdf", B / "g/g3_a4_pr.pdf",    CAP_GOOD, None),
    ("D r6_pad0 pdf",               B / "d/r6_pad0.pdf",     CAP_GOOD, None),
    ("D r6_pad10 pdf",              B / "d/r6_pad10.pdf",    CAP_GOOD, None),
    # ---- caption SOURCE: what MATLAB can actually emit ----
    ("F3 via MATLAB-written caption FILE (good)",   B / "f/s2_good_pr.png", "@build/m3-matlab-recon/f/s2_caption.txt", 200),
    ("F3 via MATLAB-written caption FILE (bad)",    B / "f/s2_good_pr.png", "@build/m3-matlab-recon/f/s2_caption_bad.txt", 200),
    ("F3 via MATLAB title string as caption",       B / "f/s2_good_pr.png", "Series sample", 200),
    ("F3 via MATLAB xlabel string as caption",      B / "f/s2_good_pr.png", "t", 200),
    ("A p5 exportgraphics pdf",     B / "a/p5_exportgraphics_pdf.pdf", CAP_GOOD, None),
    ("A p5 exportgraphics pdf_image", B / "a/p5_exportgraphics_pdf_image.pdf", CAP_GOOD, None),
    ("A p5 print dpdf",             B / "a/p5_print_dpdf.pdf", CAP_GOOD, None),
]


def main():
    print(f"# checker = {CHK.relative_to(ROOT)}  (invoked by path, not modified)")
    print(f"# denominator = --textwidth-in 6.31 (repo convention)")
    n_fail = 0
    for label, fig, cap, dpi in CASES:
        if not fig.is_file():
            print(f"### {label}\n  !! MISSING {fig}")
            continue
        cmd = [sys.executable, str(CHK), "--fig", str(fig), "--caption", cap, "--textwidth-in", "6.31"]
        if dpi is not None:
            cmd += ["--dpi", str(dpi)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(f"### {label}  [{fig.suffix.lstrip('.')}]  exit={r.returncode}")
        for line in r.stdout.rstrip("\n").split("\n"):
            print("   " + line)
        if r.stderr.strip():
            print("   STDERR " + r.stderr.strip())
        if r.returncode != 0:
            n_fail += 1
    print(f"\n# invocations with exit!=0: {n_fail} / {len(CASES)}")


if __name__ == "__main__":
    main()
