#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen-evidence.py --- normalise the captured transcripts to LF and (re)build every
`out-*.txt` in this directory. Nothing here is hand-written; every `out-*.txt` is the
verbatim stdout of a command that is run by this script.

WHY LF NORMALISATION IS A MEASURED STEP AND NOT A HABIT
  MATLAB `-batch` writes its stdout in **CRLF** on Windows (measured below and printed:
  the raw files carry one CR per line). The probe *files* written by MATLAB via
  `fopen(...,'w'|'W'|'wb')` are already LF-only -- only the shell-captured stdout is CRLF.
  So: MATLAB-side bytes are LF-clean, shell-side capture is not. This script prints the
  CR count of every raw file and writes LF-only copies.

RE-RUN (from repo root), after the MATLAB probes have been run:
  1) d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_a.m')" > build/m3-matlab-recon/raw_probe_a.txt 2>&1
     ... same for probe_b .. probe_g
  2) python tests/m3-matlab-recon/gen-evidence.py
"""
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BUILD = ROOT / "build/m3-matlab-recon"

RAW = ["raw_version.txt", "raw_probe_a.txt", "raw_probe_b.txt", "raw_probe_c.txt", "raw_probe_d.txt",
       "raw_probe_e.txt", "raw_probe_f.txt", "raw_probe_g.txt",
       "raw_probe_h_off.txt", "raw_probe_h_on.txt", "raw_probe_i.txt",
       "raw_pixels.txt", "raw_checks.txt",
       "raw_guards.txt", "raw_ripples.txt", "raw_mutate.txt", "raw_house_style.txt"]
OUTNAME = {
    "raw_version.txt": "out-version.txt",
    "raw_probe_a.txt": "out-a-env-export-fonts.txt",
    "raw_probe_b.txt": "out-b-size-single-variable.txt",
    "raw_probe_c.txt": "out-c-palette-groundtruth-f2.txt",
    "raw_probe_d.txt": "out-d-size-law-theme.txt",
    "raw_probe_e.txt": "out-e-palette-trigger.txt",
    "raw_probe_f.txt": "out-f-e2e-and-red-scenarios.txt",
    "raw_probe_g.txt": "out-g-pdf-pagebox-control.txt",
    "raw_probe_h_off.txt": "out-h-theme-dark-visible-off.txt",
    "raw_probe_h_on.txt": "out-h-theme-dark-visible-on.txt",
    "raw_probe_i.txt": "out-i-theme-trigger-and-fixes.txt",
    "raw_pixels.txt": "out-pixels-backgrounds.txt",
    "raw_checks.txt": "out-checks-figure-style.txt",
    "raw_guards.txt": "out-guards-k6-family-k3.txt",
    "raw_ripples.txt": "out-ripples-m33-m40.txt",
    "raw_mutate.txt": "out-mutate-today.txt",
    "raw_house_style.txt": "out-house-style-baseline.txt",
}


def norm(src, dst):
    raw = src.read_bytes()
    ncr = raw.count(b"\r")
    nlf = raw.count(b"\n")
    dst.write_bytes(raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    out = dst.read_bytes()
    out_cr = out.count(b"\r")
    out_lf = out.count(b"\n")
    print(f"  {src.name:28s} bytes={len(raw):7d} CR={ncr:5d} LF={nlf:6d}"
          f"  -> {dst.name} bytes={len(out)} CR={out_cr} LF={out_lf}")
    return ncr


def run_to(cmd, dst):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, cwd=str(ROOT))
    body = r.stdout
    if r.stderr.strip():
        body += "\n--- STDERR ---\n" + r.stderr
    dst.write_bytes(body.encode("utf-8"))
    print(f"  $ {' '.join(str(c) for c in cmd[1:] if not str(c).startswith(str(ROOT)))}"
          f"  -> {dst.name}  (exit={r.returncode})")


def main():
    print("== 1. normalise MATLAB shell captures to LF ==")
    total_cr = 0
    for name in RAW:
        src = BUILD / name
        if not src.is_file():
            print(f"  !! missing {src} (run the matching probe first)")
            continue
        total_cr += norm(src, HERE / OUTNAME[name])
    print(f"  total bare CR removed: {total_cr}")

    print("\n== 2. re-run the pure-python instruments (their stdout IS the evidence) ==")
    run_to([sys.executable, HERE / "measure_artifacts.py",
            "build/m3-matlab-recon/a", "build/m3-matlab-recon/b", "build/m3-matlab-recon/c",
            "build/m3-matlab-recon/d", "build/m3-matlab-recon/e", "build/m3-matlab-recon/f",
            "build/m3-matlab-recon/g"], HERE / "out-artifacts-measured.txt")
    run_to([sys.executable, HERE / "probe_checks.py"], HERE / "out-checks-figure-style.txt")

    print("\n== 3. font list ==")
    lf = BUILD / "a/p3_listfonts.txt"
    if lf.is_file():
        (HERE / "out-listfonts.txt").write_bytes(lf.read_bytes().replace(b"\r\n", b"\n"))
        cr = lf.read_bytes().count(b"\r")
        print(f"  listfonts -> out-listfonts.txt  (raw CR count = {cr})")

    print("\n== 4. size-law table (assembled from out-artifacts-measured.txt) ==")
    meas = (HERE / "out-artifacts-measured.txt").read_text(encoding="utf-8")
    rec = {}
    for line in meas.split("\n"):
        if line.startswith("PNG "):
            p = line.split()
            rec.setdefault(p[1], {})["png_px"] = p[2].split("=", 1)[1]
        elif line.startswith("PDF "):
            p = line.split()
            for tok in p:
                if tok.endswith("in") and "x" in tok:
                    rec.setdefault(p[1], {})["pdf_in"] = tok.split("x")[0]
                    break
    rowsdef = [
        ("t0_base",       "Position 631x260 · PaperPosition 6.31x2.6", "no change"),
        ("t1_pos_w800",   "Position 800x260 (ONLY pixel width)",       "pixel Position"),
        ("t2_pos_h400",   "Position 631x400 (ONLY pixel height)",      "pixel Position"),
        ("t3_paper_w800", "PaperPosition 8.0x2.6 (ONLY paper width)",  "PaperPosition"),
        ("t4_paper_h350", "PaperPosition 6.31x3.5 (ONLY paper height)","PaperPosition"),
        ("t5_paper_size", "PaperSize 11x8.5 (ONLY paper size)",        "PaperSize"),
        ("t6_letter",     "PaperSize 8.5x11 (letter)",                 "PaperSize"),
    ]
    out = ["# SIZE CALIBER -- one variable changed per row; identical plot content in every row.",
           "# source: out-artifacts-measured.txt (rebuilt by gen-evidence.py from the MATLAB artifacts).",
           "# columns: eg_* = exportgraphics (Resolution 200 for png), pr_* = print(-dpng -r200 / -dpdf).",
           f"# {'case':14s} {'what changed':42s} {'eg.pdf in':>10s} {'eg.png px':>10s} {'eg.png in':>10s}"
           f" {'pr.pdf in':>10s} {'pr.png px':>10s} {'pr.png in':>10s}",
           ]
    for case, what, _fam in rowsdef:
        eg_p = rec.get(f"{case}_eg.pdf", {})
        eg_n = rec.get(f"{case}_eg.png", {})
        pr_p = rec.get(f"{case}_pr.pdf", {})
        pr_n = rec.get(f"{case}_pr.png", {})
        eg_px = eg_n.get("png_px", "?").split("x")[0]
        pr_px = pr_n.get("png_px", "?").split("x")[0]
        eg_in = float(eg_p.get("pdf_in", "nan"))
        pr_in = float(pr_p.get("pdf_in", "nan"))
        out.append(f"{case:16s} {what:42s} {eg_in:10.4f} {eg_px:>10s} {int(eg_px)/200:10.4f}"
                   f" {pr_in:10.4f} {pr_px:>10s} {int(pr_px)/200:10.4f}")
    out.append("")
    out.append("# F1 = width / 6.31.  exportgraphics ignores PaperPosition and PaperSize entirely;")
    out.append("# it crops to the axes content bbox (+ padding) scaled by the figure's PIXEL Position.")
    out.append("# print -dpng follows PaperPosition; print -dpdf puts the figure on the PaperSize page.")
    (HERE / "out-size-law.txt").write_bytes(("\n".join(out) + "\n").encode("utf-8"))
    print("\n".join("  " + l for l in out))


if __name__ == "__main__":
    main()
