#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_ripples.py --- M3 matlab recon: what BREAKS in the shipped machines the day
`mcm-plot-matlab` is really built.

Targets found by reading the shipped sources (they are NOT edited here):
  * `mutate-figure-style.py` `M33` -- `sub_once(t, "  - `mcm-plot-matlab`（〔拟建〕）", "  - `mcm-plot-matlab`")`
  * `mutate-figure-style.py` `M40` -- reverse arm: temp `--skills-root` with a
    `mcm-plot-matlab` directory while SKILL.md still marks it 〔拟建〕.
  * `.claude/skills/mcm-figure-choose/SKILL.md:67,71` -- the two lines naming it.

Nothing is written outside build/. re-run from repo root:
  python tests/m3-matlab-recon/probe_ripples.py
"""
import importlib.util
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FC = ROOT / "tests/skills/figure-choose"
HOUSE = FC / "check-house-style.py"
REAL_SKILL = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"
REAL_ROOT = ROOT / ".claude/skills"
BUILD = ROOT / "build/m3-matlab-recon"

M33_LITERAL = "  - `mcm-plot-matlab`（〔拟建〕）"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def k6(text, skills_root):
    f = BUILD / "_ripple_skill.md"
    f.write_bytes(text.encode("utf-8"))
    r = subprocess.run([sys.executable, str(HOUSE), "--only", "K6", "--no-provenance",
                        "--skill", str(f), "--skills-root", str(skills_root)],
                       capture_output=True, text=True, cwd=str(ROOT))
    line = next((l for l in r.stdout.split("\n") if l.startswith(("PASS  K6", "FAIL  K6"))), "(no K6 line)")
    return r.returncode, line.strip()


def main():
    txt = REAL_SKILL.read_bytes().decode("utf-8")

    print("=" * 78)
    print("§R1  M33's literal dependency on the 〔拟建〕 mark")
    print("=" * 78)
    n = txt.count(M33_LITERAL)
    print(f"    real SKILL.md occurrences of {M33_LITERAL!r} = {n}")
    mut = load(FC / "mutate-figure-style.py", "mut")
    try:
        mut.sub_once(txt.replace(M33_LITERAL, "  - `mcm-plot-matlab`"), M33_LITERAL, "X")
        print("    sub_once(after mark dropped) -> NO ERROR  (unexpected)")
    except AssertionError as e:
        print(f"    sub_once(after mark dropped) -> AssertionError: {e}")
    print("    => if the 〔拟建〕 is removed from that exact bullet, M33 cannot even build its mutant.\n")

    print("=" * 78)
    print("§R2  M40's post-arm: does it stop being RED once the skill really exists?")
    print("=" * 78)
    tmp = BUILD / "ripple_root"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    (tmp / "mcm-plot-python").mkdir()          # exists, unmarked  -> consistent
    (tmp / "mcm-plot-matlab").mkdir()          # will exist  -> must be unmarked

    rc, line = k6(txt, tmp)
    print(f"    today's SKILL.md    + temp root(python,matlab)  exit={rc}")
    print(f"      {line}")

    # the minimal CORRECT fix: drop the mark on the bullet; split the prose sentence
    fixed = txt.replace(M33_LITERAL, "  - `mcm-plot-matlab`")
    fixed = fixed.replace(
        "  `mcm-plot-matlab` 与 `mcm-plot-origin` **仍是〔拟建〕**（名字已登记、文件未建）——",
        "  `mcm-plot-origin` **仍是〔拟建〕**（名字已登记、文件未建）——")
    assert fixed != txt
    rc, line = k6(fixed, tmp)
    print(f"    FIXED SKILL.md      + temp root(python,matlab)  exit={rc}")
    print(f"      {line}")
    print("    => (exit 0) means M40's post_ok assertion goes False => the driver reports RED-BAD.\n")

    print("=" * 78)
    print("§R3  M40's pre-arm on the REAL root, before vs after the skill is built")
    print("=" * 78)
    rc, line = k6(txt, REAL_ROOT)
    print(f"    today's SKILL.md + REAL root (matlab absent)      exit={rc}")
    print(f"      {line}")
    rc, line = k6(fixed, REAL_ROOT)
    print(f"    FIXED SKILL.md   + REAL root (matlab still absent) exit={rc}")
    print(f"      {line}")
    print("    => the mark must be dropped in the SAME change that creates the skill dir,")
    print("       otherwise K6 is red on the real root either way.\n")

    print("=" * 78)
    print("§R4  the full K-guard set on the FIXED SKILL.md (does the fix break anything else?)")
    print("=" * 78)
    f = BUILD / "_ripple_skill.md"
    f.write_bytes(fixed.encode("utf-8"))
    r = subprocess.run([sys.executable, str(HOUSE), "--skill", str(f),
                        "--skills-root", str(tmp), "--no-provenance"],
                       capture_output=True, text=True, cwd=str(ROOT))
    for l in r.stdout.rstrip("\n").split("\n"):
        if l.strip():
            print("    " + l)
    print(f"    exit={r.returncode}")


if __name__ == "__main__":
    main()
