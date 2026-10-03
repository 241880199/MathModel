#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-schematic` 骨架族的**自证控制组**：把每份骨架编一遍，再用出货检查器量一遍。

用法：
  python tests/skills/schematic/fixtures/make-fixtures.py            # 重编 + 重量 + 落盘（默认）
  python tests/skills/schematic/fixtures/make-fixtures.py --check    # 只重量已入库的 PDF（不重编）

两组控制：

  · **正控制** = `assets/skeletons/*.tex`（每份骨架一份）—— 断言 **pdflatex rc=0 且 `F1–F6` + `A1`/`A3`/`A4` 全绿**。
  · **反控制** = `negative-control-math.tex` —— 故意用数学模式，断言 **F6 判红**
    （判据只能从失败方向证明：它证明 F6 在"字体族不对"时**真的会红**，而不是恒绿；
    ★ 它在 `--schematic` 下 A 族**全绿**，实测判词仍是 `RESULT: FAIL（F6）` ⇒ 这条控制没被 A 族污染）。

产出（本目录，入库）：
  <名>.pdf         —— 编译产物（一个图文件 = 一页）
  <名>.check.txt   —— 该产物上 `check-figure-style.py` 的**逐字 stdout**（LF）
  <名>.build.txt   —— 那次编译的读数：rc · `Overfull \\hbox` 计数 · `Output written` 行
  captions.tsv     —— 每份正控制的图注（量 F3a–d 用的那个字符串）

**本文件不重写任何判据**：`F1–F6` 与 `A` 族一律由 `tests/skills/figure-choose/check-figure-style.py` 判
（**同一个检查器**；`A` 族由 Task 2 落地，带 `--schematic` 才追加 —— 见 `check_one`）。
★ **反控制仍是 F6 单条**：它在 `--schematic` 下 A 族**全绿**（实测 `RESULT: FAIL（F6）`），
故"用数学模式 ⇒ F6 红"这条控制没有被 A 族污染。

★ 环境事实（如实登记，不是可选项）：
  · 需要 PATH 上有 `pdflatex`（本机 TeX Live 2026）⇒ **干净检出复跑不相容**。
  · 本机 TeX Live **没有** `standalone.cls` / `preview.sty` / `pdfcrop`
    （实测 `kpsewhich standalone.cls` ⇒ 空）⇒ 页盒靠 `geometry` 的 `paperwidth` 钉死，
    **不用** standalone；这条实测决定了骨架的写法，见 `README.md`。
  · 临时目录一律落**仓内 `build/`**（`.gitignore`），**不落 C 盘 / %%TEMP%%**。
  · 路径含空格 / 非 ASCII ⇒ **不把路径直接塞给 `pdflatex`**：先 cd 进 build 下的 ASCII 短路径，
    再用**文件名**调用它（本仓 `mcm-abstract/check-summary.py` 记过这个坑）。
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent            # tests/skills/schematic/fixtures
ROOT = HERE.parents[3]                                     # 仓根
SKILL = ROOT / ".claude/skills/mcm-schematic"
STYLE = SKILL / "assets/schematic-style.tex"
SKEL_DIR = SKILL / "assets/skeletons"
CHECKER = ROOT / "tests/skills/figure-choose/check-figure-style.py"
BUILD = ROOT / "build/m3-schematic-fixtures"               # gitignored，且**在 D 盘**（不落 C 盘）
TEXTWIDTH_IN = 6.75    # 论文版心宽（mcm-latex-format 的 article 12pt + geometry）；F1 的分母
CAPTIONS = HERE / "captions.tsv"

# 反控制：文件名（.tex 在本目录）→ 它的**预期判词**（必须逐字出现在检查器输出里）
NEGATIVES = {"negative-control-math": "RESULT: FAIL（F6）"}

# 正控制**必须**出现的 `A` 族判词行（`--schematic` 触发才追加的那三条）。
# ★ fail-closed：`check_one` 一旦漏传 `--schematic`，检查器只打 `F1–F6` ⇒ 正控制照样 PASS、
#   而 `A1`/`A3`/`A4` 的覆盖**悄悄消失**（静默绿）。故正控制的输出里**必须**逐条出现这三行，缺则 FAIL。
#   （订正这个洞只能在**示意图这一侧**补：改检查器默认 stdout/stderr 会让已入库的 9 份捕获失效。）
A_TAGS = ("A1", "A3", "A4")


def missing_a_tags(out):
    """正控制输出里缺哪些 `A` 族判词行（`^(PASS|FAIL)  A<n>` 形态）。返回缺失的 tag 列表。

    这是 Important 3 的 fail-closed 守卫：没有它，漏传 `--schematic` 就是一次**静默绿**。
    """
    seen = set(re.findall(r"(?m)^(?:PASS|FAIL)\s+(A\d+)\b", out))
    return [t for t in A_TAGS if t not in seen]



def read_captions():
    """`captions.tsv`：`<骨架名>\\t<图注>`。图注就是喂给检查器 `--caption` 的那个字符串。"""
    rows = {}
    for ln in CAPTIONS.read_bytes().decode("utf-8").splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        name, cap = ln.split("\t", 1)
        rows[name.strip()] = cap.strip()
    return rows


def positives():
    return sorted(p.stem for p in SKEL_DIR.glob("*.tex"))


def stage():
    """把 `assets/` 整棵树按原样搬到 build 下（保住 `\\input{../schematic-style.tex}` 的相对路径）；
    反控制也放进同一个 skeletons 目录（它用的是同一条相对路径）。"""
    d = BUILD / "assets"
    if d.exists():
        shutil.rmtree(d)
    (d / "skeletons").mkdir(parents=True)
    shutil.copy2(STYLE, d / "schematic-style.tex")
    for p in SKEL_DIR.glob("*.tex"):
        shutil.copy2(p, d / "skeletons" / p.name)
    for name in NEGATIVES:
        shutil.copy2(HERE / f"{name}.tex", d / "skeletons" / f"{name}.tex")
    return d / "skeletons"


def compile_one(name, workdir):
    """cwd = build 下的 ASCII 路径，只把**文件名**交给 pdflatex（避路径坑）。rc=0 是硬门。"""
    tex = workdir / f"{name}.tex"
    if not tex.exists():
        return None, f"缺文件：{tex}"
    proc = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
        cwd=str(workdir), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    log = proc.stdout.decode("utf-8", "replace")
    overfull = len(re.findall(r"Overfull \\hbox", log))
    m = re.search(r"Output written on ([^\s(]+) \((\d+) pages?, (\d+) bytes\)", log)
    line = (f"rc={proc.returncode} · Overfull \\hbox={overfull} · "
            + (m.group(0) if m else "**没有 Output written 行 ⇒ 没产出 PDF**"))
    pdf = workdir / f"{name}.pdf"
    return (pdf if (proc.returncode == 0 and pdf.exists()) else None), line


def check_one(pdf, caption):
    """跑**现有**出货检查器（F1–F6 + `--schematic` 追加的 `A` 族），逐字收 stdout。判据本体不在这里。

    ★ `--schematic`：本支的产物**就是示意图**，故带上它 —— 检查器据此追加 `A1`/`A3`/`A4`
    （节点框重叠 / 文字越界 / 线宽；`A2` 已降级，见 `README.md` 的 A 族段）。不给这个旗标时
    检查器只打 `F1–F6`，与上一版**逐字相同**。

    ★ **捕获归一化**：Windows 上子进程的 stdout 是 CRLF；本仓要求入库文本**全 LF**
    ⇒ 落盘前把 `\\r\\n` / 单独 `\\r` 归一成 `\\n`。这是**采集口径**，不是改内容
    （先例：`tests/m3-schematic-recon/gen-evidence.py` 同样把 CRLF 捕获归一化为 LF）。
    """
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--fig", str(pdf),
         "--caption", caption, "--textwidth-in", str(TEXTWIDTH_IN), "--schematic"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    out = proc.stdout.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    return proc.returncode, out


def run_group(names, caps, workdir, a, bad):
    """正控制：断言 rc=0 且 `RESULT: PASS`。"""
    for name in names:
        if a.check:
            pdf = HERE / f"{name}.pdf"
            buildline = "(未重编；--check 只重量已入库产物)"
            if not pdf.exists():
                bad.append(f"{name}: 缺已入库 PDF")
                print(f"FAIL  {name}  {buildline}")
                continue
        else:
            pdf_src, buildline = compile_one(name, workdir)
            if pdf_src is None:
                bad.append(f"{name}: 编译失败（{buildline}）")
                print(f"FAIL  {name}  {buildline}")
                continue
            pdf = HERE / f"{name}.pdf"
            shutil.copy2(pdf_src, pdf)
            (HERE / f"{name}.build.txt").write_bytes(
                f"# {name} · 编译读数（pdflatex，TeX Live 2026）\n{buildline}\n".encode("utf-8"))

        rc, out = check_one(pdf, caps[name])
        (HERE / f"{name}.check.txt").write_bytes(out.encode("utf-8"))
        missing_a = missing_a_tags(out)
        verdict = "PASS" if (rc == 0 and "RESULT: PASS" in out and not missing_a) else "FAIL"
        if verdict == "FAIL":
            if missing_a:
                bad.append(f"{name}: 正控制输出缺 `A` 族判词行 {missing_a} ⇒ 静默绿"
                           f"（`check_one` 可能漏传 `--schematic`）")
            else:
                tail = out.strip().splitlines()[-1] if out.strip() else "无输出"
                bad.append(f"{name}: 出货检查器 {verdict}（{tail}）")
        print(f"{verdict}  {name}  {buildline} · 检查器 rc={rc}")


def run_negatives(workdir, a, bad):
    """反控制：断言编译 rc=0 **且**检查器输出逐字含预期判词（通常是一条 FAIL）。"""
    for name, expect in sorted(NEGATIVES.items()):
        if a.check:
            pdf = HERE / f"{name}.pdf"
            buildline = "(未重编；--check 只重量已入库产物)"
            if not pdf.exists():
                bad.append(f"{name}: 缺已入库 PDF")
                print(f"FAIL  {name}  {buildline}")
                continue
        else:
            pdf_src, buildline = compile_one(name, workdir)
            if pdf_src is None:
                bad.append(f"{name}: 编译失败（{buildline}）——反控制必须**编得过**")
                print(f"FAIL  {name}  {buildline}")
                continue
            pdf = HERE / f"{name}.pdf"
            shutil.copy2(pdf_src, pdf)
            (HERE / f"{name}.build.txt").write_bytes(
                f"# {name} · 编译读数（pdflatex，TeX Live 2026）\n{buildline}\n".encode("utf-8"))

        rc, out = check_one(pdf, "Figure 9: negative control")
        (HERE / f"{name}.check.txt").write_bytes(out.encode("utf-8"))
        hit = expect in out
        if not hit:
            bad.append(f"{name}: 反控制预期判词 `{expect}` 未出现（检查器 rc={rc}）⇒ 判据没按预期红")
        print(f"{'红-达预期' if hit else 'FAIL'}  {name}  {buildline} · 预期 `{expect}` · 实见 "
              f"{out.strip().splitlines()[-1] if out.strip() else '无输出'}")


def main():
    ap = argparse.ArgumentParser(description="编译骨架并跑出货检查器（F1–F6 + A 族）：正控制 + 反控制")
    ap.add_argument("--check", action="store_true", help="只重量已入库的 PDF，不重编")
    a = ap.parse_args()

    if shutil.which("pdflatex") is None:
        print("FAIL: PATH 上没有 pdflatex（本任务需要本机 TeX 发行版）")
        return 1

    caps = read_captions()
    names = positives()
    if not names:
        print(f"FAIL: {SKEL_DIR} 下一份骨架都没有")
        return 1
    missing = [n for n in names if n not in caps]
    if missing:
        print(f"FAIL: captions.tsv 缺这些骨架的图注：{missing}")
        return 1

    workdir = None if a.check else stage()

    bad = []
    print(f"正控制 = {len(names)} 份骨架 · 反控制 = {len(NEGATIVES)} 份 · "
          f"检查器 = tests/skills/figure-choose/check-figure-style.py · 分母 --textwidth-in = {TEXTWIDTH_IN}")
    print("-" * 78)
    run_group(names, caps, workdir, a, bad)
    print("-" * 78)
    run_negatives(workdir, a, bad)
    print("-" * 78)
    if bad:
        for b in bad:
            print(f"  - {b}")
        print(f"RESULT: FAIL（{len(bad)} 项没过）")
        return 1
    print(f"RESULT: PASS（正控制 {len(names)} 份全绿：pdflatex rc=0 且 F1–F6 + A1/A3/A4 全绿；"
          f"反控制 {len(NEGATIVES)} 份按预期红）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
