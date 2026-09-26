#!/usr/bin/env python3
# Verify that every `INDEX.md §X` pointer in the three SKILL.md files resolves to
# an existing entry of corpus/official/INDEX.md. Without this, renumbering INDEX
# silently re-points a skill at a *different* fact and no test fails.
# Usage:  python tests/check-index-pointers.py      (exit 1 = dangling pointer)
#
# KNOWN LIMITATION: this catches only DANGLING pointers (the number no longer
# exists). If INDEX is renumbered such that a cited number STILL EXISTS but now
# denotes a different fact, this check passes and the mis-pointing stays silent.
# Closing that gap needs a stable per-entry ID in INDEX.md (structural change;
# deferred to the M6 corpus-index phase). Do not treat "OK" as full safety.
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NUM = re.compile(r"\d+(?:\.\d+)*")
SKILLS = ["mcm-selfreview", "mcm-ai-disclosure", "mcm-latex-format"]

valid = set()  # anchors = section headings ("## §2.5") + table row labels ("| 2.2.9 |")
for line in (ROOT / "corpus/official/INDEX.md").read_text(encoding="utf-8").splitlines():
    if line.startswith("#"):
        valid.update(NUM.findall(line.lstrip("#").strip().lstrip("§")))
    elif line.startswith("|") and NUM.fullmatch(line.split("|")[1].strip()):
        valid.add(line.split("|")[1].strip())

bad = 0
for name in SKILLS:
    src = (ROOT / f".claude/skills/{name}/SKILL.md").read_text(encoding="utf-8")
    refs = set(re.findall(r"§(\d+(?:\.\d+)*)", src))
    for r in sorted(refs):
        if r not in valid:
            print(f"DANGLING  {name}: §{r}")
            bad += 1
    print(f"{name}: {len(refs)} pointer(s) checked")
print("OK" if not bad else f"FAIL: {bad} dangling pointer(s)")
sys.exit(1 if bad else 0)
