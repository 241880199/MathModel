#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Normalise the raw captures in build/m3-matlab-font/ into LF-only evidence
files in this directory, then re-measure the embedded PDF fonts.

Why: MATLAB's stdout on Windows is CRLF while files MATLAB writes with
fopen(...,'wb') are LF-only.  This repo's evidence files are LF-only, so the
raw captures are normalised here (with the original CR count printed).

Run AFTER the probes:
    python tests/m3-matlab-font-probe/gen-evidence.py

Inputs  (build/m3-matlab-font/, gitignored)
Outputs (this directory, version controlled)
"""
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BUILD = ROOT / "build" / "m3-matlab-font"

# (raw capture, evidence file name)
RAW = [
    ("raw_probe_a.txt", "out-a-font-discovery.txt"),
    ("raw_probe_a2.txt", "out-a2-preinstall-baselines.txt"),
    ("raw_probe_a3.txt", "out-a3-pf-fonts-api.txt"),
    ("raw_probe_b.txt", "out-b-postinstall-style-named.txt"),
    ("raw_probe_d.txt", "out-d-postinstall-family-named.txt"),
    ("raw_probe_c.txt", "out-c-postrollback.txt"),
    ("post/install_log.txt", "out-install-log-style-named.txt"),
    ("post/install_log_v2.txt", "out-install-log-family-named.txt"),
    ("afterroll/uninstall_log.txt", "out-uninstall-log.txt"),
    ("pre/pre_registry_and_dir.txt", "out-state-pre.txt"),
    ("post/post_registry_and_dir.txt", "out-state-after-install-style-named.txt"),
    ("post/state_after_install_v2.txt", "out-state-after-install-family-named.txt"),
    ("afterroll/state_final.txt", "out-state-after-rollback.txt"),
    ("post/check1_after_broadcast.txt", "out-check1-after-broadcast.txt"),
    ("post/check2_sets.txt", "out-check2-font-sets.txt"),
    ("post/check3_after_sessionadd.txt", "out-check3-after-session-add.txt"),
    ("post/check4_inprocess_add.txt", "out-check4-inprocess-add.txt"),
    ("post/check5_naming.txt", "out-check5-value-name-family.txt"),
    ("post/control_delete_plainname.txt", "out-control-delete-plain-name.txt"),
    ("post/check7_out_of_dir.txt", "out-check7-out-of-font-dir.txt"),
]

# listfonts-family dumps already written as LF by MATLAB (fopen 'wb')
LF_COPY = [
    ("probe_a/listfonts_probe_a_before.txt", "out-listfonts-a-before.txt"),
    ("probe_b/listfonts_probe_b_after.txt", "out-listfonts-b-after.txt"),
    ("probe_d/listfonts_probe_d.txt", "out-listfonts-d-after.txt"),
    ("probe_c/listfonts_probe_c_afterrollback.txt", "out-listfonts-c-after-rollback.txt"),
    ("probe_a2/FontUtils_getFontNames.txt", "out-fontutils-getfontnames.txt"),
    ("check/pf_fonts_now.txt", "out-pf-fonts-now.txt"),
]

PDF_DIRS = [
    "probe_a", "probe_a2", "probe_b", "probe_c", "probe_d", "check4",
]


def norm(src: Path, dst: Path) -> None:
    if not src.exists():
        print("  MISSING %s" % src)
        return
    raw = src.read_bytes()
    cr = raw.count(b"\r")
    text = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    dst.write_bytes(text)
    print("  %-46s -> %-42s CR=%d -> 0  %d B" % (src.name, dst.name, cr, len(text)))


def main() -> int:
    print("== normalising raw captures to LF ==")
    for rel, out in RAW:
        norm(BUILD / rel, HERE / out)
    print("== copying MATLAB-written (already LF) font lists ==")
    for rel, out in LF_COPY:
        src = BUILD / rel
        if not src.exists():
            print("  MISSING %s" % src)
            continue
        raw = src.read_bytes()
        (HERE / out).write_bytes(raw)
        print("  %-46s -> %-42s CR=%d  %d B" % (src.name, out, raw.count(b"\r"), len(raw)))

    print("== re-measuring embedded PDF fonts ==")
    out_lines = []
    for d in PDF_DIRS:
        p = BUILD / d
        if not p.is_dir():
            continue
        out_lines.append("### %s" % d)
        r = subprocess.run(
            [sys.executable, str(HERE / "measure_fonts.py"), str(p)],
            capture_output=True, text=True,
        )
        out_lines.append(r.stdout.rstrip())
    text = "\n".join(out_lines) + "\n"
    (HERE / "out-pdf-embedded-fonts.txt").write_bytes(text.encode("utf-8"))
    print("  wrote out-pdf-embedded-fonts.txt  %d B" % len(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
