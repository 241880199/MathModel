#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-plot-python` 的**新鲜度守卫** + **字体守卫**（计划 Task 3）。**只读 + 原地重放后还原**：
除"查前先快照、原地重跑生成器写那两份派生件、随后 `write_bytes` 还原成查前字节"之外不改任何东西；
还原**非原子**（进程在重跑与还原之间被杀会留脏，见下）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/plot-python/check-style-freshness.py
    python tests/skills/plot-python/check-style-freshness.py --doc <规范副本>   # 变异/演示用

退出码 **0 / 1**（无 2：本器与 `check-spec-pointers.py` 同一条纪律）；末行**恒**为 `RESULT: …`；
每条判词**一行**，形态 `PASS|FAIL  <id>  <读数>`；判红的差异上下文/字体集合另起**缩进行**（不以
`PASS`/`FAIL` 起头，故逐行解析器不受影响）。**fail-closed 在本器里 = 判红 + exit 1**（不像
`check-figure-style.py` 那样另开 exit 2）—— 因为本器没有"判过且红"以外的第三种出口。

## 新鲜度：为什么必须**先快照、再重跑**（本任务最容易做错的一处）

生成器 `gen-mcm-style.py` 是**原地写**的。照计划原文"重跑生成器 → 与入库件逐字节相等"实现是
**恒真**的：一份**过期**的派生件被原地重跑一次就**被改对了**，再比对必然相等 ⇒ 这条判据什么都
抓不到。故本器的形态是：**先把要比对的两份字节取下来**，**再**重跑，**再**比对：

- **`A1` 入库快照臂**：比对对象 = `git show HEAD:<path>` 的字节（**受版本控制的那一份**）。
  它答的是"**入库的派生件是不是当前规范能重放出来的**"。规范改了而派生件没重放 ⇒ 红。
- **`A2` 工作树臂**：比对对象 = **检查前**工作树里那一份的字节（在重跑**之前**快照的）。
  它答的是"**手头这份派生件是不是重放出来的**"。手工改派生件（Global Constraint 6 禁止）
  ⇒ 重放把它改回去 ⇒ 与**改前**快照不等 ⇒ 红。**A1 抓不到这一态**：工作树被手改而 HEAD 干净时，
  `A1` 比的是 HEAD 与重放的结果，两者都干净、**相等**；只有把"重跑之前的字节"也留一份才有得比。

两条臂**都不恒真**：`A1` 由变异 M54（改规范锚点值）证、`A2` 由变异 M55（改派生件常量）证。
重跑完成后**工作树一律还原成检查前的字节**（`write_bytes`）⇒ 正常收尾下工作树**不变**。但这**非原子**：
若进程在重跑与还原之间被杀（Ctrl-C / OOM），工作树会留下**重放后的**字节 —— 那时 `A2` 会红、能自曝。

## 字体：走设计 §11.3 的**途径 ①**（核产物本身）

**理由**：① 验的是**产物**（PDF 里 `fitz` 实报的 basefont），也就是"**渲染这一步真的选了哪份字体**"；
②（`font_manager.findfont()`）验的是**matplotlib 的查找结果**，即便查找命中，渲染仍可能因别的原因
不用它，且它看不到"字体文件被换成别的字体、但路径没变"这种**内容级**问题。① 覆盖更靠下游。

**射程（如实写窄）**：① 证明的是"**这张探针图用的是入库的这几份字体文件**"——**不证明**
"这份字体与论文正文观感一致"（数学是另一套实现 `mathtext` 的 `stix`，见 `mcmplot.py` 已知缺口），
**也不**验**字体文件的字节**（本臂判的是渲染出的 PostScript 名；字形轮廓被改而名不变时**不会红**），
**也不**是 `check-figure-style.py` 的一部分（那支判据一字不改，Global Constraint 5）。

**缺口归属（实测）**：全 `tests/` 下**没有**任何判据把入库 `.otf` 的 `git hash-object`
与 `assets/fonts/PROVENANCE.md` 对账（`gen-plot-style-verify.py` 的 `BOUND` 只**记录**字体 blob、
不比对 `PROVENANCE.md`）⇒ Global Constraint 10 括注那句"改了哈希就变，判据会红"**目前无归属**。
本任务硬要求 5 只要"用的是不是入库那一份"、且扩展范围已被裁定禁止 ⇒ **不补哈希臂**，缺口照实写在这里。

判据：探针 PDF 里 `fitz` 报的 basefont 集合（剥掉子集前缀 `XXXXXX+`）必须
**非空** · **⊆ 预期集合**（预期 = 入库 `mcmplot.py` 的 `_FONTS` 逐件用 `ft2font.FT2Font()` 读出的
PostScript 名 ⇒ **不手写字体名**） · **含探针正文要的那一档**（`style_name == "Regular"`，
因为探针只画罗马正体）。任一条不成立 ⇒ 红。**"字体被改名/移走"时 `apply_style()` 的
`addfont()` 会抛 `FileNotFoundError` ⇒ 本臂把它兜成判红**（见变异 M57），**不是**静默回退还绿。

## 与派发任务书的差异（逐条为实测逼出）

- **D1（`fitz` 的 API）**：任务书写 `fitz` 的 `get_fonts()`。本机 PyMuPDF **1.27.2.3** 上
  `fitz.Document.get_fonts()` **已不存在**（实测 `AttributeError: 'Document' object has no attribute
  'get_fonts'`），文档级等价物是 `Document.get_page_fonts(pno)`（实测存在）。本器用后者**逐页取**。
- **D2（探针栏宽）**：探针要调 `mcmplot.figsize_for(textwidth_in)`，而本臂与图幅无关 ⇒ 传任意正值
  `PROBE_WIDTH_IN`（**不是**规范值、也不参与判定；F1 图宽比归 `check-figure-style.py`）。
- **D3（fail-closed 的出口）**：任务书硬要求 2 要"记红并非零退出"，硬要求 4 要"退出码 0/1" ⇒
  本器**不设 exit 2**：生成器跑不动 / git 取不到入库快照 / 字体读不出，一律 **判红 + exit 1**。
- **D4（生成器失败时的两条臂）**：生成器 fail-closed 时它**什么都不写**（先渲染后写），
  若仍照常比对，`A1`/`A2` 会与"没重放过"的字节相等而**假绿**。故 `G0` 红时 `A1`/`A2` 一并**记红**
  （"生成器没跑成 ⇒ 无从比对"），不让"没判到"读成"通过"。
"""
import argparse
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]          # tests/skills/plot-python → 仓根
GEN = ROOT / "tests/skills/plot-python/gen-mcm-style.py"
ASSETS = ROOT / ".claude/skills/mcm-plot-python/assets"
DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
MPLSTYLE = ASSETS / "mcm.mplstyle"
MCM_PY = ASSETS / "mcmplot.py"
# 派生件 = 生成器**原地重写**的那两份（Global Constraint 6：只许由生成器重放产出）。
TARGETS = (MPLSTYLE, MCM_PY)

# 子集前缀：PDF 里嵌的子集字体名形如 `GLTHNJ+TeXGyreTermesX-Regular`（实测，见报告）。
SUBSET_RE = re.compile(r"^[A-Z]{6}\+")
PROBE_TEXT = "Probe roman text 0123456789"                  # 纯 ASCII 罗马正体（不引 mathtext）
PROBE_WIDTH_IN = 1.0                                        # D2：任意正值，不参与判定
PROBE_DPI = 72                                              # 矢量 PDF 的 dpi 不参与字体判定


def _load(path, name):
    """本仓既有惯用法：带连字符的脚本名不能 `import`，用 `spec_from_file_location`（同 `check-spec-pointers.py`）。"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _shown(p):
    """证据里不写绝对路径：仓内的写相对路径，仓外的照原样。"""
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def git_snapshot(path):
    """`git show HEAD:<仓相对路径>` 的**原始字节**。取不到 ⇒ 抛 `RuntimeError`（由调用方兜成判红）。"""
    rel = path.relative_to(ROOT).as_posix()
    try:
        pr = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=str(ROOT), capture_output=True)
    except OSError as e:                                     # 连 git 都起不动
        raise RuntimeError(f"起不动 git（{type(e).__name__}: {e}）")
    if pr.returncode != 0:
        raise RuntimeError(f"`git show HEAD:{rel}` 退出 {pr.returncode}："
                           f"{pr.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return pr.stdout


def run_generator(doc_arg):
    """跑生成器（**唯一真调用形态**：cwd = 仓根、无位置参数；`--doc` 只换输入文档）。"""
    cmd = [sys.executable, str(GEN)] + (["--doc", doc_arg] if doc_arg else [])
    try:
        pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    except OSError as e:                                     # 起不动解释器 / 脚本不在
        return None, "", f"{type(e).__name__}: {e}"
    return pr.returncode, pr.stdout, pr.stderr


def diff_context(expected, actual, limit=3):
    """逐字节不等时打印的**差异处上下文**：取首个相异行，前后各 `limit` 行。

    两个入参都是 UTF-8 文本（派生件全是文本）；解不出就退回"首个相异字节"的十六进制说明。
    """
    try:
        el = expected.decode("utf-8").splitlines()
        al = actual.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        n = next((i for i, (x, y) in enumerate(zip(expected, actual)) if x != y), min(len(expected), len(actual)))
        return [f"      首个相异字节 @{n}：快照 {expected[n:n + 1]!r} vs 重放 {actual[n:n + 1]!r}"]
    out = []
    first = next((i for i in range(max(len(el), len(al)))
                  if (el[i] if i < len(el) else None) != (al[i] if i < len(al) else None)), None)
    if first is None:
        return out
    lo, hi = max(0, first - limit), min(max(len(el), len(al)), first + limit + 1)
    out.append(f"      首个相异行 L{first + 1}（共 快照 {len(el)} 行 / 重放 {len(al)} 行）：")
    for i in range(lo, hi):
        mark = "<<" if i == first else "  "
        e = el[i] if i < len(el) else "<无此行>"
        a = al[i] if i < len(al) else "<无此行>"
        out.append(f"      {mark} L{i + 1} 快照: {e[:160]}")
        out.append(f"      {mark} L{i + 1} 重放: {a[:160]}")
    return out


def font_check():
    """字体臂（途径 ①：核探针 PDF 里 `fitz` 实报的 basefont）。返回 `(ok, detail, extra_lines)`。

    预期字体名**从入库字体文件现读**（`ft2font` 的 `postscript_name` / `style_name`），**不手写**。
    任何一步抛异常都**兜成判红**（fail-closed），不让裸异常漏出去。
    """
    try:
        m = _load(MCM_PY, "mcmplot_font_probe")
    except Exception as e:                                   # noqa: BLE001（fail-closed 出口）
        return False, f"载入入库的 mcmplot.py 失败（{type(e).__name__}: {e}）（fail-closed）", []

    expected = {}                                            # PostScript 名 → (文件名, style 名)
    try:
        from matplotlib import ft2font
        for f in m._FONTS:                                   # 入库件自己声明的字体表
            if not f.is_file():
                return False, f"入库字体缺件：{f.name}（fail-closed）", []
            ft = ft2font.FT2Font(str(f))
            expected[ft.postscript_name] = (f.name, ft.style_name)
    except Exception as e:                                   # noqa: BLE001（fail-closed 出口）
        return False, f"读不出入库字体的字体名（{type(e).__name__}: {e}）（fail-closed）", []

    extra = [f"      预期集合（入库件现读）= {sorted(expected)}"]
    roman = sorted(ps for ps, (_n, st) in expected.items() if st == "Regular")
    if not roman:
        return False, "入库字体里没有 Regular 档 ⇒ 探针的罗马正体无从核对（fail-closed）", extra

    try:
        import matplotlib
        matplotlib.use("Agg")                                # 无显示环境也能跑
        import matplotlib.pyplot as plt
        import fitz

        with tempfile.TemporaryDirectory() as d:             # 探针**只写临时目录**，不落仓
            out = pathlib.Path(d) / "font-probe.pdf"
            m.apply_style()                                  # 字体没找到 ⇒ 这里就抛（见 M57）
            fig, ax = plt.subplots(figsize=m.figsize_for(PROBE_WIDTH_IN))
            ax.plot([0.0, 1.0], [0.0, 1.0], label=PROBE_TEXT)
            ax.set_xlabel(PROBE_TEXT)
            ax.set_ylabel(PROBE_TEXT)
            ax.legend()
            m.save(fig, out, PROBE_DPI)
            plt.close(fig)
            with fitz.open(out) as probe:
                found = set()
                for pno in range(probe.page_count):
                    for rec in probe.get_page_fonts(pno):    # D1：1.27 无 Document.get_fonts()
                        found.add(SUBSET_RE.sub("", rec[3]))
    except Exception as e:                                   # noqa: BLE001（fail-closed 出口）
        return False, (f"探针渲染/取字体失败 ⇒ 字体没落到产物上（{type(e).__name__}: "
                       f"{str(e).strip().splitlines()[0][:160]}）（fail-closed）"), extra

    extra += [f"      产物实报集合（探针 PDF）= {sorted(found)}"]
    if not found:
        return False, "探针 PDF 里一个字体都没有 ⇒ 无从判断（fail-closed）", extra
    stray = sorted(found - set(expected))
    if stray:
        return False, f"产物用了**非入库**字体 {stray} ⇒ 回退（判据红）", extra
    missing = sorted(set(roman) - found)
    if missing:
        return False, f"探针的罗马正体未用到入库的 {missing}（判据红）", extra
    return True, f"产物字体 {sorted(found)} ⊆ 入库集合，且用到入库的罗马正体 {roman}", extra


def main():
    ap = argparse.ArgumentParser(description="mcm-plot-python：样式新鲜度守卫 + 字体守卫")
    ap.add_argument("--doc", default=None, help="被抽的规范（默认 = 仓内 house-style.md；变异/演示用）")
    a = ap.parse_args()
    doc_arg = a.doc
    doc_shown = _shown(pathlib.Path(doc_arg)) if doc_arg else _shown(DOC)

    print("样式新鲜度守卫 + 字体守卫（Task 3）· 派生件只许由 tests/skills/plot-python/gen-mcm-style.py 重放产出")
    print(f"规范 = {doc_shown}")
    print(f"派生件 = {[p.name for p in TARGETS]}   ·   A1 快照臂 = `git show HEAD:<path>`"
          f"   ·   A2 工作树臂 = 检查前的工作树字节")

    rows = []                                                # (id, ok, detail, extra_lines)

    # ---------------- 取两份快照（**必须在重跑之前**）
    head, wt, snap_err = {}, {}, []
    for p in TARGETS:
        try:
            head[p] = git_snapshot(p)
        except RuntimeError as e:
            snap_err.append((f"A1:{p.name}", f"取不到入库快照（fail-closed）：{e}"))
        try:
            wt[p] = p.read_bytes()
        except OSError as e:
            snap_err.append((f"A2:{p.name}", f"读不出工作树字节（fail-closed）：{type(e).__name__}: {e}"))

    # ---------------- 重跑生成器（跑完**一律还原**工作树）
    rc, gout, gerr = run_generator(doc_arg)
    gen = {}
    try:
        for p in TARGETS:
            if p in wt:
                try:
                    gen[p] = p.read_bytes()
                except OSError as e:
                    snap_err.append((f"GEN:{p.name}",
                                     f"重跑后读不出（fail-closed）：{type(e).__name__}: {e}"))
    finally:
        for p in TARGETS:                                    # 还原：本器非侵入
            if p in wt:
                p.write_bytes(wt[p])

    # ---------------- G0：生成器本身
    if rc is None:
        rows.append(("G0", False, f"生成器起不动（{gerr}）（fail-closed）", []))
    elif rc != 0:
        tail = (gerr or gout).strip().splitlines()
        rows.append(("G0", False, f"生成器退出 {rc}（fail-closed）：{tail[-1][:200] if tail else '（无输出）'}", []))
    else:
        n = next((l for l in gout.splitlines() if "锚点" in l and "条" in l), "锚点 ? 条")
        rows.append(("G0", True, f"重放成功（{n.strip()}）", []))

    # ---------------- A1 / A2：两条臂
    for p in TARGETS:
        name = p.name
        for arm, snap in (("A1", head.get(p)), ("A2", wt.get(p))):
            rid = f"{arm}:{name}"
            if snap is None:
                continue                                     # 快照取不到：已在上面按 `snap_err` 判红
            if rc != 0 or p not in gen:                      # D4：生成器没跑成 ⇒ 两条臂一并记红
                why = "生成器未跑成（见 G0）" if rc != 0 else "重放后的字节读不出"
                rows.append((rid, False, f"{why} ⇒ 无从比对（fail-closed）", []))
                continue
            if gen[p] == snap:
                rows.append((rid, True, f"重放 == 快照（{len(snap)} 字节）", []))
            else:
                who = "入库快照（HEAD）" if arm == "A1" else "工作树快照（检查前）"
                rows.append((rid, False, f"重放 != {who}（快照 {len(snap)} 字节 / 重放 {len(gen[p])} 字节）",
                             diff_context(snap, gen[p])))

    # ---------------- 字体臂
    fok, fdetail, fextra = font_check()
    rows.append(("FON", fok, fdetail, fextra))

    # ---------------- 判词（每条一行；上下文另起缩进行；末行恒为 RESULT）
    for sid, sdetail in snap_err:
        print(f"FAIL  {sid}  {sdetail}")
    for rid, ok, detail, extra in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {rid}  {detail}")
        for line in extra:
            print(line)
    bad = [sid for sid, _d in snap_err] + [rid for rid, ok, _d, _e in rows if not ok]
    print("-" * 78)
    print(f"判据 {len(rows) + len(snap_err)} 条 · 红 {len(bad)} 条 · 派生件 {len(TARGETS)} 份 "
          f"· 生成器 exit={rc}")
    print("RESULT: PASS" if not bad else f"RESULT: FAIL（{','.join(bad)}）")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
