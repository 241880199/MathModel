#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_guards.py --- M3 matlab recon: does the mechanical layer reach a MATLAB skill?

Three measurements, all against the SHIPPED checkers (invoked by path; nothing copied, nothing edited):

  §G1  K6 three states -- today / family-2-with-mark-kept / family-2-with-mark-dropped.
       Uses --skills-root (existence root) and --skill (a COPY of SKILL.md), never the real tree.
  §G2  check-spec-pointers.py on a TEMP skills root that contains a newly "built"
       mcm-plot-matlab SKILL.md (self-authored, with the pointer and ONE deliberate
       restatement of a spec number) => does the family scope pick it up immediately?
  §G3  K3 substring landmine table for idioms that are COMMON in a MATLAB .m plotting script.

re-run from repo root:
  python tests/m3-matlab-recon/probe_guards.py
"""
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
FC = ROOT / "tests/skills/figure-choose"
HOUSE = FC / "check-house-style.py"
PTR = FC / "check-spec-pointers.py"
REAL_SKILL = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"
BUILD = ROOT / "build/m3-matlab-recon"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(label, cmd):
    print(f"### {label}")
    print("    $ " + " ".join(str(c) for c in cmd))
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, cwd=str(ROOT))
    for line in r.stdout.rstrip("\n").split("\n"):
        if line.strip():
            print("    " + line)
    if r.stderr.strip():
        print("    STDERR " + r.stderr.strip())
    print(f"    exit={r.returncode}\n")
    return r


# ---------------------------------------------------------------- §G1 K6 three states
def g1():
    print("=" * 78)
    print("§G1  K6: mcm-plot-matlab from 不存在 to 存在")
    print("=" * 78)

    # state A -- today's real tree (read-only)
    run("A/today: real tree, no --skills-root, no --skill",
        [sys.executable, HOUSE, "--only", "K6", "--no-provenance"])

    # temp roots
    root_b = BUILD / "k6root_existing"          # skills that DO exist as dirs
    for d in (root_b,):
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
    for name in ("mcm-figure-choose", "mcm-plot-python", "mcm-plot-matlab"):
        (root_b / name).mkdir()

    # state B -- family 2 exists, SKILL.md still marks matlab as 〔拟建〕 (the forgetful case)
    run("B/family-2, mark kept (real SKILL.md text + temp root where matlab exists)",
        [sys.executable, HOUSE, "--only", "K6", "--no-provenance",
         "--skills-root", str(root_b)])

    # state C -- the same, with the mark dropped in a COPY of SKILL.md (what the fix does)
    txt = REAL_SKILL.read_bytes().decode("utf-8")
    # drop 〔拟建〕 only on the lines that name mcm-plot-matlab
    out = []
    for line in txt.split("\n"):
        if "mcm-plot-matlab" in line:
            line = line.replace("（〔拟建〕）", "").replace("〔拟建〕", "")
        out.append(line)
    fixed = BUILD / "SKILL_matlab_built.md"
    fixed.write_bytes("\n".join(out).encode("utf-8"))
    print(f"    (wrote {fixed.relative_to(ROOT)} with 〔拟建〕 stripped from mcm-plot-matlab lines)")
    run("C/family-2, mark dropped (modified SKILL.md COPY + temp root)",
        [sys.executable, HOUSE, "--only", "K6", "--no-provenance",
         "--skill", str(fixed), "--skills-root", str(root_b)])

    # show the exact lines that carry the name
    print("    --- real SKILL.md lines naming mcm-plot-matlab ---")
    for i, line in enumerate(txt.split("\n"), 1):
        if "mcm-plot-matlab" in line:
            print(f"    {i}: {line}")


# ---------------------------------------------------------------- §G2 family scope
def g2():
    print("=" * 78)
    print("§G2  check-spec-pointers.py: does a newly built mcm-plot-matlab enter the family?")
    print("=" * 78)
    s2 = BUILD / "skills2"
    if s2.exists():
        shutil.rmtree(s2)
    shutil.copytree(ROOT / ".claude/skills", s2)

    run("baseline: copy of real .claude/skills (family = 1)",
        [sys.executable, PTR, "--skills-dir", str(s2)])

    fake = s2 / "mcm-plot-matlab"
    fake.mkdir()
    (fake / "SKILL.md").write_bytes((
        "---\n"
        "name: mcm-plot-matlab\n"
        "description: fake family skill built by probe_guards.py, for recon only\n"
        "---\n"
        "# mcm-plot-matlab (fake)\n\n"
        "本 skill 的图形规范见 `references/house-style.md`（唯一权威）。\n\n"
        "## 约定\n"
        "- 图高常见取 2.6 in。\n"          # <- the deliberate restatement of an H3 number
        "- 推荐 exportgraphics 导出 PDF。\n"
    ).encode("utf-8"))
    print(f"    (wrote {fake.relative_to(ROOT)}/SKILL.md with one restated number)\n")

    run("family 1 -> 2: same temp root + built mcm-plot-matlab",
        [sys.executable, PTR, "--skills-dir", str(s2)])

    # clean sibling to prove it is not always-red
    clean = s2 / "mcm-plot-clean"
    clean.mkdir()
    (clean / "SKILL.md").write_bytes((
        "# mcm-plot-clean (fake)\n\n"
        "图形规范见 `references/house-style.md`（唯一权威）。\n"
    ).encode("utf-8"))
    run("family 1 -> 3: + a CLEAN sibling mcm-plot-clean (contrast, must stay green)",
        [sys.executable, PTR, "--skills-dir", str(s2)])


# ---------------------------------------------------------------- §G3 K3 landmine
def g3():
    print("=" * 78)
    print("§G3  K3 substring landmine for ordinary MATLAB .m plotting idioms")
    print("=" * 78)
    mod = load(HOUSE, "chs_guards")
    cases = [
        "exportgraphics(fig, 'f.pdf')",
        "exportgraphics(fig, 'f.png', 'Resolution', 200)",
        "print(fig, 'f.png', '-dpng', '-r200')",
        "print(fig, 'f.pdf', '-dpdf')",
        "saveas(fig, 'f.png')",
        "set(fig,'PaperUnits','inches')",
        "set(fig,'PaperPosition',[0 0 6.31 2.6])",
        "set(fig,'Position',[100 100 631 260])",
        "set(ax,'LineWidth',1.5)",
        "set(ax,'FontSize',10)",
        "plot(x, y, 'LineWidth', 0.8)",
        "ylim([0 1.0])",
        "x = 0.5;",
        "alpha = 0.9;",
        "dpi = 300;",
        "fig.Position = [0 0 6.31 2.6];",
        "t = linspace(0, 2*pi, 200);",
        "set(ax,'FontName','Times New Roman')",
        "axis([0 10 0 1]);",
        "legend(ax,'show')",
        "b = bar(D,'stacked');",
        "set(ax,'XTickLabel',{'A','B'})",
        "% 图宽取正文宽（6.31 in）",
        "% 用四种图型",
        "% 分四色显示",
        "set(ax,'TickDir','in')",
        "box(ax,'off')",
        "ax.XMinorTick = 'on';",
        "exportgraphics(fig,'f.pdf','Padding',0)",
        "set(fig,'PaperPositionMode','auto')",
        "matlab -batch \"run('build/probe.m')\"",
    ]
    print(f"{'verdict':8s} {'hits':40s} text")
    n_red = 0
    for t in cases:
        ok, why = mod._k3(t)
        hits = re.findall(r"命中 \[(.*?)\]", why)
        hs = hits[0] if hits else ""
        if not ok:
            n_red += 1
        print(f"{'PASS' if ok else 'FAIL':8s} {hs:40s} {t}")
    print(f"\n# {n_red} / {len(cases)} sample lines judged FAIL by K3")


if __name__ == "__main__":
    g1()
    g2()
    g3()
