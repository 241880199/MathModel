#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/plot-python/check-style-freshness.py` 的**变异驱动器** —— 一条命令复跑全部变异。

用法：  python tests/skills/plot-python/mutate-plot-style.py

## 为什么必须落盘

本仓已栽过**六次**"判据在什么都没验的情况下报绿"（`mutate-figure-style.py` 头部），最近一次是
Task 2 的生成器 fail-closed：那两条"真的红"当时**只活在 gitignored 的报告里**（Task 2 复审
Minor T2-M3）⇒ 本轮把生成器的 fail-closed 臂做成**常驻**（`M56`/`M59`），别让覆盖只活在过程件里。

## 编号顺延 + 总数现算

`M54` 起顺延（编号是**全模块**的坐标，不是本文件的行号；`M47`–`M53` 是 Task 1 的 `K3` 阈值标记臂，
`M1`–`M46` 在 `mutate-figure-style.py`）。**总数一律 `len(MUTATIONS)` 现算**，不手抄。

⚠️ **对任务书的一处引用更正**：任务书写"先例见 `mutate-figure-style.py:821-824` 里写了编号顺延的原因"，
**实测不实** —— `:821-824` 是 `k6_exists_mut()` 的函数体（建临时 skill 根那段），与编号无关。
顺延理由的**真实落点**是 `:146`（`M43` 起）、`:881-882`（`M43` 起，注释里列了前三次）、
`:1107`（`M47` 起）、`:1120-1121`（`M53`，理由最完整："已占号 / 插号会让既有引用失准"）。
本文件的编号取法照**那些落点**，不照任务书那行。

## 每条变异做什么

全部**当场改、当场还原**：

- 只碰**规范副本 / 派生件工作树 / 字体文件**三类，**逐条 `try/finally` 还原**；
- 规范类变异走 `--doc <副本>`（生成器**本来就有**这个开关，未新增任何生成器形态）；
- 收尾用 `git hash-object` 自证"改过的文件逐字节还原"，并断言 `git status --short` 为空。

## 变异清单（每条对应一条**已被声明**的覆盖）

| id | 打的是哪条声明 | 期望 |
| :--- | :--- | :--- |
| `M54` | `A1` 入库快照臂：规范改了而派生件没重放 ⇒ 红 | 红 `A1:mcmplot.py` |
| `M55` | `A2` 工作树臂：派生件**生成区**被手改（重放会把它改对 ⇒ `A1` 抓不到）⇒ 红 | 红 `A2:mcmplot.py` |
| `M56` | 硬要求 2：锚点**命中 0 处** ⇒ 生成器 fail-closed ⇒ 判据非零退出 | 红 `G0` |
| `M57` | 硬要求 5：入库字体**改名/移走** ⇒ 判据红（**不是**静默回退） | 红 `FON` |
| `M58` | 设计 §11.3 的前提：字体**没注册**就**静默回退成 DejaVu** ⇒ 判据红 | 红 `FON`（报 `DejaVuSerif`） |
| `M59` | 硬要求 2：锚点**命中 >1 处** ⇒ 生成器 fail-closed ⇒ 判据非零退出 | 红 `G0` |
| `M60` | **射程边界对照**：改规范里**不参与抽取**的散文 ⇒ 判据**仍绿**（本器不是"改了就红"） | 绿 |
| `M61` | **字面形态对照（证伪）**：计划原文"重跑后比"在过期态下**恒真** | 被证伪 |

`M55` 与 `M58` 的区别是**改在生成标记的哪一侧**：生成器只重写两条标记**之间**，故
`M55`（标记内）重放会把它改对、只有 `A2` 抓得到；`M58`（标记外的 `apply_style()`）重放**改不动**它，
`A1` 与 `FON` 同时红。两条都是真红，覆盖的是不同的手改位置。
"""
import importlib.util
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CHK = ROOT / "tests/skills/plot-python/check-style-freshness.py"
GEN = ROOT / "tests/skills/plot-python/gen-mcm-style.py"
DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
ASSETS = ROOT / ".claude/skills/mcm-plot-python/assets"
MCM_PY = ASSETS / "mcmplot.py"
MUTDIR = ROOT / "tests/skills/plot-python/fixtures/_mut"
# 变异**不许**动的件（收尾逐件比对哈希）—— 四份 OTF 全在列：`M57` 移走的是**排序后第一份**
# （`Bold`），若只盯 `Regular` 这条守卫就守错了文件（"声明比事实大"的典型）。
GUARDED = (DOC, ASSETS / "mcm.mplstyle", MCM_PY,
           *(sorted((ASSETS / "fonts").glob("*.otf"))))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git_hash_object(p):
    """入库件的身份（`git hash-object`）。"""
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def write_doc_copy(name, text):
    """把规范副本写进 `fixtures/_mut/`（`write_bytes`：不用 `write_text`，Windows 会写 CRLF）。"""
    MUTDIR.mkdir(parents=True, exist_ok=True)
    p = MUTDIR / name
    p.write_bytes(text.encode("utf-8"))
    return p


def run_checker(doc_arg=None):
    cmd = [sys.executable, str(CHK)] + (["--doc", doc_arg] if doc_arg else [])
    pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return pr.returncode, pr.stdout


def run_generator(doc_arg=None):
    """跑生成器（唯一真调用形态：cwd = 仓根；`--doc` 只换输入文档）。"""
    cmd = [sys.executable, str(GEN)] + (["--doc", doc_arg] if doc_arg else [])
    pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return pr.returncode, pr.stdout, pr.stderr


def _raw(cmdline, rc, out):
    """逐条**贴原始 stdout**：把那条命令与它的 stdout 原文一并带回证据。"""
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return f"$ {cmdline}   → exit={rc}\n{body}"


def _anchors():
    """生成器自己的锚点表（**不在这里重抄正则**：抄件会随生成器漂移）。"""
    return _load(GEN, "gen_mcm_style_for_mutations").ANCHORS


def _hit(src, pattern, want, flags=0):
    hits = list(re.finditer(pattern, src, flags))
    if len(hits) != want:
        raise AssertionError(f"前提不成立：正则命中 {len(hits)} 处（要 {want}）：{pattern}")
    return hits[0]


def _first(src, pattern, flags=0):
    """命中 ≥1 处时取**第一处**（用于"随便挑一条"的变异，如派生件里的某个常量）。"""
    m = next(re.finditer(pattern, src, flags), None)
    if m is None:
        raise AssertionError(f"前提不成立：正则一处都没命中：{pattern}")
    return m


# ---------------------------------------------------------------- 规范副本类
def m54_spec_anchor_value():
    """`M54`：改规范的一个锚点值（`H1` 图宽比上限）⇒ 重放出的常量随之变 ⇒ `A1` 该红。

    走 `--doc <副本>`：**真规范一字不碰**（生成器本就有 `--doc`，未新增生成器形态）。
    """
    aid, pat, key = next(a for a in _anchors() if a[0] == "H1-width-max")
    src = DOC.read_bytes().decode("utf-8")
    m = _hit(src, pat, 1)
    val = m.group(1)
    new = f"{float(val) + 0.5:g}"
    mut = src[:m.start(1)] + new + src[m.end(1):]
    mp = write_doc_copy("m54.house-style.md", mut)
    rc, out = run_checker(mp.relative_to(ROOT).as_posix())
    mp.unlink()
    ok = rc == 1 and "FAIL  A1:mcmplot.py" in out and f"'{key}': {new}," in out
    return ok, (f"锚点 {aid}：{val} → {new}（只改副本，真规范未碰）· 期望 `A1:mcmplot.py` 红且差异行"
                f"显示新值 · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --doc {mp.name}", rc, out))


# ---------------------------------------------------------------- 派生件工作树类
def m55_derived_constant():
    """`M55`：派生件**生成区**的一个常量被手改 ⇒ `A2` 该红。

    ★ 这条同时证明 `A1` **不是够用的**：手改发生在生成标记**之间**，重放会把它**改对**
    ⇒ 与入库快照（HEAD，本来就干净）**相等**、`A1` 绿；只有"重跑**之前**的工作树字节"这份快照
    才留得住证据。输出里 `A1` 绿 / `A2` 红并排，就是这句话的实证。
    """
    src = MCM_PY.read_bytes().decode("utf-8")
    m = _first(src, r"^    '([a-z0-9_]+)': ([\d.]+),$", flags=re.M)
    key, val = m.group(1), m.group(2)
    g = 2                                                    # 值所在组（组 1 = 键）
    new = f"{float(val) + 1.5:g}"
    mutated = src[:m.start(g)] + new + src[m.end(g):]
    orig = MCM_PY.read_bytes()
    try:
        MCM_PY.write_bytes(mutated.encode("utf-8"))
        rc, out = run_checker()
    finally:
        MCM_PY.write_bytes(orig)
    ok = rc == 1 and "FAIL  A2:mcmplot.py" in out and "PASS  A1:mcmplot.py" in out
    return ok, (f"常量 {key}：{val} → {new}（生成标记之间；当场还原）· 期望 `A1` **仍绿** + `A2` 红"
                f" · 实得 exit={rc}\n" + _raw("check-style-freshness.py", rc, out))


def m58_font_unregistered():
    """`M58`：**设计 §11.3 的前提**——字体没注册就**静默回退成 DejaVu** ⇒ `FON` 该红。

    改的是生成标记**外**的 `apply_style()`（重放**改不动**它）⇒ `A1` 与 `FON` 同时红，
    而产物实报集合由 `TeXGyreTermesX-Regular` 变成 `DejaVuSerif` —— 这就是"静默回退"的直接读数。
    """
    src = MCM_PY.read_bytes().decode("utf-8")
    m = _hit(src, r"for f in _FONTS:\n\s+font_manager\.fontManager\.addfont\(str\(f\)\)\n", 1)
    mutated = src[:m.start()] + "pass  # MUT M58：不注册入库字体\n" + src[m.end():]
    orig = MCM_PY.read_bytes()
    try:
        MCM_PY.write_bytes(mutated.encode("utf-8"))
        rc, out = run_checker()
    finally:
        MCM_PY.write_bytes(orig)
    ok = rc == 1 and "FAIL  FON" in out and "DejaVuSerif" in out
    return ok, ("拆掉 apply_style() 的 addfont 循环（生成标记**外**；当场还原）· 期望 `FON` 红且实报 "
                "`DejaVuSerif`（静默回退的实证）· 实得 exit=" + str(rc) + "\n"
                + _raw("check-style-freshness.py", rc, out))


# ---------------------------------------------------------------- 生成器 fail-closed 臂
def _doc_line_of_last_anchor(src):
    """取**最后一条**锚点命中的那一行（**现算**：锚点与行都不许抄进本脚本）。"""
    aid, pat, _key = _anchors()[-1]
    m = _hit(src, pat, 1)
    lo = src.rfind("\n", 0, m.start()) + 1
    hi = src.find("\n", m.end())
    return aid, pat, lo, hi


def m56_anchor_hit_zero():
    """`M56`：删掉一条锚点的目标行 ⇒ 生成器**命中 0 处**、fail-closed ⇒ 判据非零退出（硬要求 2）。"""
    src = DOC.read_bytes().decode("utf-8")
    aid, pat, lo, hi = _doc_line_of_last_anchor(src)
    mut = src[:lo] + src[hi + 1:]
    if next(re.finditer(pat, mut), None) is not None:
        raise AssertionError("删行后正则仍命中 ⇒ 前提不成立")
    mp = write_doc_copy("m56.house-style.md", mut)
    rc, out = run_checker(mp.relative_to(ROOT).as_posix())
    mp.unlink()
    ok = rc == 1 and "FAIL  G0" in out and "生成器退出 1" in out and "RESULT: FAIL" in out
    return ok, (f"删掉锚点 {aid} 所在行（只改副本）⇒ 生成器命中 0 处 ⇒ G0 红 + 非零退出"
                f" · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --doc {mp.name}", rc, out))


def m59_anchor_hit_many():
    """`M59`：把一条锚点的目标行**复制一份** ⇒ 生成器**命中 2 处**、fail-closed ⇒ 判据非零退出。"""
    src = DOC.read_bytes().decode("utf-8")
    aid, pat, lo, hi = _doc_line_of_last_anchor(src)
    line = src[lo:hi + 1]
    mut = src[:hi + 1] + line + "\n" + src[hi + 1:]
    if len(list(re.finditer(pat, mut))) != 2:
        raise AssertionError("复制行后正则命中数 != 2 ⇒ 前提不成立")
    mp = write_doc_copy("m59.house-style.md", mut)
    rc, out = run_checker(mp.relative_to(ROOT).as_posix())
    mp.unlink()
    ok = rc == 1 and "FAIL  G0" in out and "生成器退出 1" in out and "命中 2 处" in out
    return ok, (f"复制锚点 {aid} 所在行（只改副本）⇒ 生成器命中 2 处 ⇒ G0 红 + 非零退出"
                f" · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --doc {mp.name}", rc, out))


# ---------------------------------------------------------------- 字体文件类
def m57_font_moved():
    """`M57`：把入库字体**改名/移走** ⇒ 判据红（硬要求 5；**不是**静默回退还绿）。"""
    fonts = sorted((ASSETS / "fonts").glob("*.otf"))
    if not fonts:
        raise AssertionError("fonts/ 下一份 OTF 都没有 ⇒ 前提不成立")
    target = fonts[0]
    bak = target.with_suffix(".otf.moved")
    if bak.exists():
        raise AssertionError(f"残留的 {bak.name} 未清 ⇒ 拒绝跑（免得覆盖证据）")
    try:
        target.rename(bak)
        rc, out = run_checker()
    finally:
        bak.rename(target)                                   # 当场还原
    ok = rc == 1 and "FAIL  FON" in out and "fail-closed" in out
    return ok, (f"把 {target.name} **移走**（{target.name} → {bak.name}，当场还原）⇒ 期望 FON 红、"
                f"非零退出 · 实得 exit={rc}\n" + _raw("check-style-freshness.py", rc, out))


# ---------------------------------------------------------------- 射程边界对照
def m60_prose_only():
    """`M60`：改规范里**不参与抽取**的散文 ⇒ 判据**必须仍绿**。

    这条是**射程边界对照**（不是"变异"）：本器红的是"锚点值 / 派生件 / 字体"三类**承重的**改动，
    **不是**"规范被动过就红"。没有这一条，"本器在改文档时会红"这句话就无从证伪。
    """
    src = DOC.read_bytes().decode("utf-8")
    mp = write_doc_copy("m60.house-style.md", src + "\n")     # 末尾加一个空行：不落在任何锚点里
    rc, out = run_checker(mp.relative_to(ROOT).as_posix())
    mp.unlink()
    ok = rc == 0 and "RESULT: PASS" in out
    return ok, ("规范副本末尾加一个空行（不参与抽取）⇒ 期望**仍绿** · 实得 exit=" + str(rc) + "\n"
                + _raw(f"check-style-freshness.py --doc {mp.name}", rc, out))


def m61_literal_form_is_vacuous():
    """`M61`（对照 · **证伪**）：计划的**字面形态**（"重跑生成器 → 与入库件比"）**恒真**。

    本行**不跑判据**，跑的是"字面形态"本身：在**过期**状态下（规范已改、派生件未重放）
    原地重跑一次生成器 ⇒ `git status` 当场显示**派生件被改对了**。既然重跑会把参考件本身
    改成"重放的结果"，那么在重跑**之后**取参考再比 —— 比的两个东西是同一份 ⇒ **必等**。
    本器的两臂都在重跑**之前**取参考（`A1` 取 `HEAD`、`A2` 取工作树），故不落这个坑。

    断言（只要这两条）：① 重放退出 0；② 工作树里的派生件**确实被改**（`git status` 显示 `M`）。
    """
    aid, pat, _key = next(a for a in _anchors() if a[0] == "H1-width-max")
    src = DOC.read_bytes().decode("utf-8")
    m = _hit(src, pat, 1)
    new = f"{float(m.group(1)) + 0.5:g}"
    mp = write_doc_copy("m61.house-style.md", src[:m.start(1)] + new + src[m.end(1):])
    before = MCM_PY.read_bytes()
    rc_gen, _gout, gerr = run_generator(mp.relative_to(ROOT).as_posix())
    after = MCM_PY.read_bytes()
    st_raw = subprocess.run(["git", "status", "--short", MCM_PY.relative_to(ROOT).as_posix()],
                            cwd=str(ROOT), capture_output=True, text=True).stdout
    st = st_raw.strip()                                      # 展示用（首列那个空格是 git 的状态位）
    MCM_PY.write_bytes(before)                               # 当场还原
    mp.unlink()
    ok = rc_gen == 0 and after != before and st.startswith("M ")   # `M <path>`：工作树里被改过
    return ok, (f"过期态（锚点 {aid}：{m.group(1)} → {new}，派生件未重放）下**原地重跑**：生成器 exit={rc_gen}"
                f" · 派生件字节被改={after != before} · 重跑后的 `git status --short` = 『{st}』\n"
                f"      ⇒ 重跑之后取参考再比，参考件已被改成重放结果本身 ⇒ **恒真**。"
                f"本器在重跑**之前**取参考，故不恒真。")


MUTATIONS = [
    ("M54", "改规范锚点值（`H1` 宽比上限）⇒ 派生件落后 ⇒ `A1` 红", m54_spec_anchor_value),
    ("M55", "改派生件生成区常量 ⇒ 重放会改对它（`A1` 抓不到）⇒ `A2` 红", m55_derived_constant),
    ("M56", "删一条锚点的目标行 ⇒ 命中 0 处 ⇒ 生成器 fail-closed ⇒ `G0` 红", m56_anchor_hit_zero),
    ("M57", "入库字体改名/移走 ⇒ `FON` 红（不是静默回退）", m57_font_moved),
    ("M58", "拆掉 addfont 注册 ⇒ 静默回退成 DejaVu ⇒ `FON` 红", m58_font_unregistered),
    ("M59", "复制一条锚点的目标行 ⇒ 命中 2 处 ⇒ 生成器 fail-closed ⇒ `G0` 红", m59_anchor_hit_many),
]
# 对照（`kind` 决定行的标号）：GREEN = 判据必须**仍绿**；REFUTED = 字面形态必须被**证伪**
CONTROLS = [
    ("M60", "**射程边界对照**：改不参与抽取的散文 ⇒ 判据仍绿", m60_prose_only, "GREEN"),
    ("M61", "**字面形态对照**：原地重跑把过期件改对 ⇒「重跑后再比」恒真", m61_literal_form_is_vacuous, "REFUTED"),
]


def main():
    print("=" * 78)
    print("变异驱动器 · check-style-freshness.py（mcm-plot-python）：新鲜度两臂 + 生成器 fail-closed + 字体臂")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}
    for p, h in guarded_before.items():
        print(f"  受保护件 {p.relative_to(ROOT).as_posix():<58} blob {h}")

    # 前置：干净态必须**全绿**（否则下面每条的"红"都不说明问题）
    rc0, out0 = run_checker()
    base_ok = rc0 == 0 and "RESULT: PASS" in out0
    print(f"\n前置（干净态）：exit={rc0} · {'RESULT: PASS' if base_ok else '未绿 <<<'}")

    rows, failed = [], []
    for mid, desc, fn in MUTATIONS:
        try:
            ok, detail = fn()
        except AssertionError as e:
            rows.append(("RED-BAD", mid, desc, f"驱动器自己报错：{e}")); failed.append(mid); continue
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)

    ctrl_rows = []
    for cid, cdesc, cfn, kind in CONTROLS:
        try:
            cok, cdetail = cfn()
        except AssertionError as e:
            cok, cdetail = False, f"驱动器自己报错：{e}"
        if not cok:
            failed.append(cid)
        ctrl_rows.append((f"{kind}-OK" if cok else f"{kind}-BAD", cid, cdesc, cdetail))

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴判据的原始 stdout）")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<11} {mid:<4} {desc}")
        print(detail)
    print("-" * 78)
    print("对照（不是判据变异：`GREEN` = 该绿、`REFUTED` = 该被证伪）")
    for st, mid, desc, detail in ctrl_rows:
        print(f"{st:<11} {mid:<4} {desc}")
        print(detail)

    # ------------------------------------------------------------ 还原自证
    if MUTDIR.is_dir() and not any(MUTDIR.iterdir()):
        MUTDIR.rmdir()
    if MUTDIR.parent.is_dir() and not any(MUTDIR.parent.iterdir()):
        MUTDIR.parent.rmdir()                                # 别留一个空的 fixtures/ 在地上
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    st = subprocess.run(["git", "status", "--short"], cwd=str(ROOT), capture_output=True, text=True).stdout
    dirty = sorted(l for l in st.splitlines() if l.strip())
    rerun_rc, rerun_out = run_checker()

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print(f"  {p.relative_to(ROOT).as_posix():<58} blob {now}  "
              f"{'== 变异前' if now == guarded_before[p] else '!= 变异前 <<<'}")
    print(f"  受保护件逐个 blob 还原: {byte_ok}")
    print(f"  fixtures/_mut/ 已清空: {not MUTDIR.exists()}")
    print(f"  全仓 `git status --short`（本轮的变异目标都已按上面的 blob 还原；此列是**全仓**状态，"
          f"可能含本任务尚未入库的新件）: {dirty or '（空）'}")
    print(f"  变异后复跑（干净态）: exit={rerun_rc} · {rerun_out.strip().splitlines()[-1]}")
    print(f"  `git status --short`（应为空）:\n{st if st.strip() else '      （空）'}")

    n_red = len(MUTATIONS)
    n_ok = n_red - len([m for m in failed if m in [mm[0] for mm in MUTATIONS]])
    ctl_ok = sum(1 for st, *_ in ctrl_rows if st.endswith("OK"))
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {n_ok}/{n_red} 红（新鲜度两臂 / 生成器 fail-closed / 字体臂）"
          + ("" if not failed else f"（未达预期：{', '.join(failed)}）"))
    ctl_what = "、".join(("{} 该{}".format(cid, "绿" if kind == "GREEN" else "被证伪"))
                         for cid, _d, _f, kind in CONTROLS)
    print(f"MUT: 对照 {ctl_ok}/{len(ctrl_rows)} 达预期（{ctl_what}）")
    print(f"MUT: 合计 {n_ok}/{n_red} 条判据变异 + {ctl_ok}/{len(ctrl_rows)} 条对照")
    # 头部那句"并断言 `git status --short` 为空"必须**真的是退出条件**（"声明比事实大"的补丁）：
    # 脏树 ⇒ 非零退出，不是只打印一行读数。`dirty` 取自第 370 行那次**全仓** `git status --short`。
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty) else 1


if __name__ == "__main__":
    sys.exit(main())
