#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/plot-matlab/check-style-freshness.py` 的**变异驱动器** —— 一条命令复跑全部变异。

用法：  python tests/skills/plot-matlab/mutate-plot-style.py

## 编号顺延 + 总数现算

`M62` 起顺延（编号是**全模块**的坐标，不是本文件的行号；`M1`–`M46` 在
`tests/skills/figure-choose/mutate-figure-style.py`，`M47`–`M53` 是 Task 1 的 `K3` 阈值标记臂，
`M54`–`M61` 在 `tests/skills/plot-python/mutate-plot-style.py`）。**总数一律 `len(MUTATIONS)` 现算**，不手抄。

## 每条变异做什么

全部**当场改、当场还原**：

- 改**表**的一律走**表副本**（生成器 `--table <副本>`，真表一字不碰；副本按 json 解析后改再 dump，
  反正生成器读的是 json）；
- 改**派生件**的一律 `write_bytes` 当场还原（`try/finally`）；
- ④/⑤ 要**真渲染**（MATLAB `-batch`）：产 `.png`/`.pdf` 到 `build/m3-matlab-t2/`（gitignored、给人看），
  再用**一字不改**的 `check-figure-style.py`（GC6）判 —— 这**不是**本器自证，是**判据真的接住了**。
- 收尾用 `git hash-object` 自证"改过的件逐字节还原"，并断言 `git status --short` 为空（"没碰真根"）。

## 变异清单（每条对应一条**已被声明**的覆盖）

| id | 打的是哪条声明 | 期望 |
| :--- | :--- | :--- |
| `M62` | 硬要求 3① / 两臂专属红：**改表一个值** ⇒ 派生件落后 ⇒ **`A1` 专属红**（`A2` 绿） | 红 `A1` |
| `M63` | 硬要求 3② / 两臂专属红：**改派生件生成区常量** ⇒ 重放会改对它 ⇒ **`A2` 专属红**（`A1` 绿） | 红 `A2` |
| `M64` | 硬要求 3③：**删掉一条锚点的目标行** ⇒ 生成器命中 0 ⇒ fail-closed | 红 `G0` |
| `M65` | 硬要求 2：**复制一条锚点** ⇒ 命中 >1 ⇒ 生成器 fail-closed | 红 `G0` |
| `M66` | 硬要求 3④：**摘掉浅色主题机制** ⇒ 渲染照常成功但产物深色 ⇒ **`F4` 真红**（motivating case） | 红 `F4` |
| `M67` | 硬要求 3⑤：**字体点名一个不存在的族** ⇒ **静默回退** ⇒ **`F6` 真红** | 红 `F6` |

对照（`kind` 决定行标号）：`GREEN` = 判据必须**仍绿**；`REFUTED` = 字面形态必须被**证伪**。

- `M68` **射程边界对照**：改表里**不参与抽取**的字段（一个 `same-value` 格的 `how`，生成器**不读**它）
  ⇒ 两臂**仍绿**。没有这条，"本器在改表时会红"这句话就无从证伪。
- `M69` **字面形态对照（证伪）**：任务书的**字面形态**（"重跑生成器 → 与入库件比"）**恒真**。

## ★ `④` 的如实登记（与任务书字面的一处偏差）

任务书写"**摘掉浅色主题那一行**"。实测：`mcmplot.m` 只把 `'Theme','light'` 一个 token 去掉**并不**让产物变深
—— 因为 `new_figure`/`apply_style` **还各自显式设了白**（`'Color',S.bg` 共 3 处）⇒ 白是**过定的**。
⇒ 本变异摘的是**浅色主题机制**（那三处白一并去掉），这才等价于"没上浅色主题的图"。
**实测读数见 `M66` 的判据输出**（落地态 `F4` PASS / 本变异 `F4` FAIL）。
"""
import copy
import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
CHK = ROOT / "tests/skills/plot-matlab/check-style-freshness.py"
GEN = ROOT / "tests/skills/plot-matlab/gen-mcm-style-matlab.py"
TABLE = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"
TARGET = ROOT / ".claude/skills/mcm-plot-matlab/assets/mcmplot.m"
CHECK_FS = ROOT / "tests/skills/figure-choose/check-figure-style.py"
MUTDIR = ROOT / "build/m3-matlab-t2/_mut"          # 表副本（自清）
PROBEDIR = ROOT / "build/m3-matlab-t2/_probe"      # 临时 .m 驱动（自清）
OUTDIR = ROOT / "build/m3-matlab-t2"               # 渲染产物（gitignored、给人看）
MATLAB = "D:/Software/Matlab/bin/matlab.exe"       # GC12：本机 R2025b Update 5
# 变异**不许**动的件（收尾逐件比对 blob）—— 表 / 派生件 / 两个生成器
GUARDED = (TABLE, TARGET, GEN, ROOT / "tests/skills/figure-choose/gen-style-table.py")

# 渲染驱动（临时 .m，写进 PROBEDIR、收工自清）：用**入库件** M.figure / M.apply / M.save
RENDER_M = r"""root = fileparts(fileparts(fileparts(fileparts(mfilename('fullpath'))))); cd(root);
addpath(fullfile(root, '.claude', 'skills', 'mcm-plot-matlab', 'assets'));
M = mcmplot();
fig = M.figure(6.31); ax = axes(fig);
plot(ax, linspace(0, 1, 30), sin(linspace(0, 2*pi, 30))); xlabel(ax, 'Angle (rad)'); ylabel(ax, 'Resp (a.u.)');
M.apply(fig); drawnow;
M.save(fig, '{png}', 300);
M.save(fig, '{pdf}');
close(fig);
fprintf('rendered {tag}\n');
"""


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def run_guard(table_arg=None, only=None):
    cmd = [sys.executable, str(CHK)] + (["--table", table_arg] if table_arg else []) \
        + (["--only", only] if only else [])
    pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return pr.returncode, pr.stdout + pr.stderr


def run_gen(table_arg=None):
    cmd = [sys.executable, str(GEN)] + (["--table", table_arg] if table_arg else [])
    pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return pr.returncode, pr.stdout, pr.stderr


def run_check_fs(fig):
    cmd = [sys.executable, str(CHECK_FS), "--fig", str(fig), "--caption", "Figure 1: mutant",
           "--textwidth-in", "6.31", "--dpi", "300"]
    pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return pr.returncode, pr.stdout


def _raw(cmdline, rc, out):
    """逐条**贴原始 stdout**：把那条命令与它的 stdout 原文一并带回证据。"""
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return f"$ {cmdline}   → exit={rc}\n{body}"


def _tbl():
    return json.loads(TABLE.read_bytes().decode("utf-8"))


def _entry(obj, eid):
    return next(e for e in obj["entries"] if e["id"] == eid)


def _write_tbl(name, obj):
    MUTDIR.mkdir(parents=True, exist_ok=True)
    p = MUTDIR / name
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))  # write_bytes（GC4）
    return p


# ---------------------------------------------------------------- 表副本类
def m62_table_value_changed():
    """`M62`（硬要求 3① / `A1` 专属红）：改表的一个值 ⇒ 派生件落后 ⇒ `A1` 红、`A2` 绿。

    ★ 先**预重放**（用乱表跑一次生成器），让工作树 = "乱表的重放结果" ⇒ `A2`（工作树 vs 重放）相等而绿；
    而 `A1` 比的是 `HEAD`（干净件）vs 重放（乱件）⇒ 红。两条臂的**分工**在这里显形。
    """
    orig_t = TARGET.read_bytes()
    obj = _tbl()
    old = _entry(obj, "h3.height_in")["value"]
    _entry(obj, "h3.height_in")["value"] = 3.7
    cp = _write_tbl("m62.mcm-style.json", obj)
    try:
        rc_g, _go, ge = run_gen(cp.relative_to(ROOT).as_posix())     # ★ 预重放
        if rc_g != 0:
            raise AssertionError(f"预重放没跑成（exit={rc_g}）：{ge.strip()[:160]}")
        rc, out = run_guard(cp.relative_to(ROOT).as_posix())
    finally:
        TARGET.write_bytes(orig_t)                                   # 当场还原（守卫自己也还原过一次）
        cp.unlink(missing_ok=True)
    ok = rc == 1 and "FAIL  A1" in out and "PASS  A2" in out and "FAIL  A2" not in out
    return ok, (f"表 `h3.height_in` {old} → 3.7（只改副本）· 预重放后工作树 = 乱表的重放结果 ⇒ "
                f"期望 `A1` 红 / `A2` 绿 · 实得 exit={rc}\n"
                + _raw(f"check-style-freshness.py --table {cp.name}", rc, out))


def m63_derived_constant():
    """`M63`（硬要求 3② / `A2` 专属红）：改派生件**生成区**的常量 ⇒ 重放改对它 ⇒ `A2` 红、`A1` 绿。"""
    orig = TARGET.read_bytes()
    s = orig.decode("utf-8")
    m = re.search(r"STYLE\.height_in = ([\d.]+);", s)
    if not m:
        raise AssertionError("派生件里找不到 STYLE.height_in = <数>;")
    old = m.group(1)
    mut = s[:m.start(1)] + "9.9" + s[m.end(1):]
    try:
        TARGET.write_bytes(mut.encode("utf-8"))
        rc, out = run_guard()
    finally:
        TARGET.write_bytes(orig)
    ok = rc == 1 and "FAIL  A2" in out and "PASS  A1" in out and "FAIL  A1" not in out
    return ok, (f"派生件生成区 `STYLE.height_in` {old} → 9.9（当场还原）· 期望 `A1` **仍绿** + `A2` 红 "
                f"（`A1` 抓不到『手工改生成区』这一态）· 实得 exit={rc}\n"
                + _raw("check-style-freshness.py", rc, out))


def m64_anchor_missing():
    """`M64`（硬要求 3③）：删掉一条锚点的目标行（整条 entry）⇒ 生成器命中 0 ⇒ fail-closed ⇒ `G0` 红。"""
    obj = _tbl()
    obj["entries"] = [e for e in obj["entries"] if e["id"] != "h3.height_in"]
    cp = _write_tbl("m64.mcm-style.json", obj)
    try:
        rc, out = run_guard(cp.relative_to(ROOT).as_posix())
    finally:
        cp.unlink(missing_ok=True)
    ok = rc == 1 and "FAIL  G0" in out and "生成器退出 1" in out and "RESULT: FAIL" in out
    return ok, ("删掉锚点 `h3.height_in` 的整条 entry（只改副本）⇒ 生成器命中 0 ⇒ `G0` 红 + 非零退出"
                f" · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --table {cp.name}", rc, out))


def m65_anchor_duplicated():
    """`M65`（硬要求 2）：复制一条锚点（整条 entry）⇒ 命中 2 ⇒ 生成器 fail-closed ⇒ `G0` 红。"""
    obj = _tbl()
    obj["entries"].append(copy.deepcopy(_entry(obj, "h3.height_in")))
    cp = _write_tbl("m65.mcm-style.json", obj)
    try:
        rc, out = run_guard(cp.relative_to(ROOT).as_posix())
    finally:
        cp.unlink(missing_ok=True)
    ok = rc == 1 and "FAIL  G0" in out and "生成器退出 1" in out and "命中 2 条" in out
    return ok, ("把锚点 `h3.height_in` 的整条 entry 复制一份（只改副本）⇒ 生成器命中 2 ⇒ `G0` 红 + 非零退出"
                f" · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --table {cp.name}", rc, out))


# ---------------------------------------------------------------- 渲染类（④ / ⑤）
def _render(tag, mutate):
    """把 `mutate` 施加到派生件 → 渲染（MATLAB）→ 还原 → 用 `check-figure-style.py` 判。

    返回 `(ml_rc, fs_rc, fs_out, paths)`；判 ④ 看 `.png`（F4）、判 ⑤ 看 `.pdf`（F6）。
    """
    orig = TARGET.read_bytes()
    PROBEDIR.mkdir(parents=True, exist_ok=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    png = OUTDIR / f"{tag}.png"
    pdf = OUTDIR / f"{tag}.pdf"
    ms = PROBEDIR / ("render_" + tag.replace("-", "_") + ".m")   # .m 文件名必须是合法标识符（无连字符）
    ms.write_bytes(RENDER_M.format(png=png.as_posix(), pdf=pdf.as_posix(), tag=tag).encode("utf-8"))
    try:
        TARGET.write_bytes(mutate(orig.decode("utf-8")).encode("utf-8"))
        rel = ms.relative_to(ROOT).as_posix()
        pr = subprocess.run([MATLAB, "-batch", f"run('{rel}')"], cwd=str(ROOT),
                            capture_output=True, text=True)
    finally:
        TARGET.write_bytes(orig)
    fig = pdf if tag.endswith("font") else png
    rc_fs, out_fs = run_check_fs(fig)
    return pr.returncode, rc_fs, out_fs, (png, pdf, fig)


def m66_no_light_theme():
    """`M66`（硬要求 3④）：**摘掉浅色主题机制** ⇒ 产物深色 ⇒ `F4` 真红（motivating case）。"""
    def mutate(s):
        s = s.replace("fig = figure('Visible', 'on', 'Color', S.bg, 'Theme', 'light');"
                      "   % ← (a) 建时上浅色主题",
                      "fig = figure('Visible', 'on');   % MUT4: 不上浅色主题")
        s = s.replace("set(fig, 'Color', S.bg);\n", "")
        s = s.replace("set(ax, 'Color', S.bg, 'XColor', 'k', 'YColor', 'k');",
                      "set(ax, 'XColor', 'k', 'YColor', 'k');")
        if "Theme', 'light'" in s or "set(fig, 'Color', S.bg);" in s:
            raise AssertionError("浅色主题机制没被完全摘掉 ⇒ 前提不成立")
        return s
    rc_ml, rc_fs, out_fs, (png, _pdf, _f) = _render("mut4-no-light-theme", mutate)
    ok = "FAIL  F4" in out_fs and "PASS  F1" in out_fs and "PASS  F5" in out_fs
    return ok, (f"摘掉浅色主题机制（`'Theme','light'` + 三处显式白）⇒ 渲染 exit={rc_ml}（照常成功）· "
                f"产物 `{png.relative_to(ROOT).as_posix()}` · 期望 `F4` 红（且 `F1`/`F5` **仍绿**，"
                f"证明深色只被 `F4` 接住）· 实得：\n"
                + _raw(f"check-figure-style.py --fig {png.name} ...", rc_fs, out_fs))


def m67_bad_font():
    """`M67`（硬要求 3⑤）：字体点名一个不存在的族 ⇒ **静默回退** ⇒ `F6` 真红（设计 §5 的核心断言）。"""
    def mutate(s):
        s2 = re.sub(r"STYLE\.font_serif = \{[^}]*\};", "STYLE.font_serif = {'NoSuchFontXYZ'};", s)
        if s2 == s:
            raise AssertionError("派生件里找不到 STYLE.font_serif = {...};")
        return s2
    rc_ml, rc_fs, out_fs, (_png, pdf, _f) = _render("mut5-bad-font", mutate)
    ok = "FAIL  F6" in out_fs and "SimSun" in out_fs
    return ok, (f"把 `STYLE.font_serif` 点名成不存在的族 `NoSuchFontXYZ` ⇒ 渲染 exit={rc_ml}"
                f"（照常成功、**不报错**）· 产物 `{pdf.relative_to(ROOT).as_posix()}` · 期望 `F6` 红且读到"
                f"回退字体（`SimSun`）· 实得：\n"
                + _raw(f"check-figure-style.py --fig {pdf.name} ...", rc_fs, out_fs))


# ---------------------------------------------------------------- 对照
def m68_prose_only():
    """`M68`（**射程边界对照**）：改表里**不参与抽取**的字段 ⇒ 判据**必须仍绿**。

    改的是一个 `same-value` 格的 `how` —— 生成器只对 `not-landable` 格调 `carrier_how()`，
    `same-value` 格的 `how` **不读** ⇒ 派生件不变 ⇒ 两臂仍绿。没有这条，"本器在改表时会红"无从证伪。
    """
    obj = _tbl()
    cell = _entry(obj, "bg")["carriers"]["matlab"]
    cell["how"] = cell["how"] + "（MUT68：这段散文不参与抽取）"
    cp = _write_tbl("m68.mcm-style.json", obj)
    try:
        rc, out = run_guard(cp.relative_to(ROOT).as_posix())
    finally:
        cp.unlink(missing_ok=True)
    ok = rc == 0 and "RESULT: PASS" in out
    return ok, ("改表里 `bg.matlab.how` 的散文（生成器**不读** `same-value` 格的 `how`）⇒ 期望**仍绿**"
                f" · 实得 exit={rc}\n" + _raw(f"check-style-freshness.py --table {cp.name}", rc, out))


def m69_literal_form_is_vacuous():
    """`M69`（对照 · **证伪**）：任务书的**字面形态**（"重跑生成器 → 与入库件比"）**恒真**。

    在**过期**状态下（表已改、派生件未重放）原地重跑一次生成器 ⇒ 派生件**当场被改对**。
    既然重跑会把参考件本身改成"重放的结果"，那么在重跑**之后**取参考再比 —— 比的两个东西是同一份 ⇒ **必等**。
    本器的两臂都在重跑**之前**取参考（`A1` 取 `HEAD`、`A2` 取工作树），故不落这个坑。
    """
    orig_t = TARGET.read_bytes()
    obj = _tbl()
    _entry(obj, "h3.height_in")["value"] = 4.2
    cp = _write_tbl("m69.mcm-style.json", obj)
    try:
        rc_gen, _go, _ge = run_gen(cp.relative_to(ROOT).as_posix())
        after = TARGET.read_bytes()
        st = subprocess.run(["git", "status", "--short", TARGET.relative_to(ROOT).as_posix()],
                            cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
    finally:
        TARGET.write_bytes(orig_t)
        cp.unlink(missing_ok=True)
    ok = rc_gen == 0 and after != orig_t and st.startswith("M ")
    return ok, (f"过期态（表 `h3.height_in` → 4.2，派生件未重放）下**原地重跑**：生成器 exit={rc_gen} · "
                f"派生件字节被改={after != orig_t} · 重跑后的 `git status --short` = 『{st}』\n"
                f"      ⇒ 重跑之后取参考再比，参考件已被改成重放结果本身 ⇒ **恒真**。"
                f"本器在重跑**之前**取参考，故不恒真。")


MUTATIONS = [
    ("M62", "改表一个值（h3.height_in）⇒ 派生件落后 ⇒ `A1` 专属红", m62_table_value_changed),
    ("M63", "改派生件生成区常量（STYLE.height_in）⇒ 重放改对它 ⇒ `A2` 专属红", m63_derived_constant),
    ("M64", "删掉锚点的目标行（h3.height_in 整条 entry）⇒ 命中 0 ⇒ `G0` 红", m64_anchor_missing),
    ("M65", "复制锚点的目标行 ⇒ 命中 2 ⇒ `G0` 红", m65_anchor_duplicated),
    ("M66", "摘掉浅色主题机制 ⇒ 产物深色 ⇒ `F4` 真红", m66_no_light_theme),
    ("M67", "字体点名不存在的族 ⇒ 静默回退 ⇒ `F6` 真红", m67_bad_font),
]
CONTROLS = [
    ("M68", "**射程边界对照**：改表里不参与抽取的散文 ⇒ 判据仍绿", m68_prose_only, "GREEN"),
    ("M69", "**字面形态对照**：原地重跑把过期件改对 ⇒「重跑后再比」恒真", m69_literal_form_is_vacuous, "REFUTED"),
]


def main():
    print("=" * 78)
    print("变异驱动器 · check-style-freshness.py（mcm-plot-matlab）：新鲜度两臂 + 生成器 fail-closed + F4/F6 真红")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    print(f"判据 = {CHECK_FS.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHECK_FS)}")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}
    for p, h in guarded_before.items():
        print(f"  受保护件 {p.relative_to(ROOT).as_posix():<56} blob {h}")

    # 前置：干净态必须**全绿**（否则下面每条的"红"都不说明问题）
    rc0, out0 = run_guard()
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
    for d in (MUTDIR, PROBEDIR):                          # 临时根**自清**（表副本 + 临时 .m 驱动）
        shutil.rmtree(d, ignore_errors=True)
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    st = subprocess.run(["git", "status", "--short"], cwd=str(ROOT), capture_output=True, text=True).stdout
    dirty = sorted(l for l in st.splitlines() if l.strip())
    rerun_rc, rerun_out = run_guard()

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print(f"  {p.relative_to(ROOT).as_posix():<56} blob {now}  "
              f"{'== 变异前' if now == guarded_before[p] else '!= 变异前 <<<'}")
    print(f"  受保护件逐个 blob 还原: {byte_ok}")
    print(f"  临时根已清空: _mut={not MUTDIR.exists()} · _probe={not PROBEDIR.exists()}")
    print(f"  变异后复跑（干净态）: exit={rerun_rc} · {rerun_out.strip().splitlines()[-1]}")
    print(f"  `git status --short`（应为空）:\n{st if st.strip() else '      （空）'}")

    n_red = len(MUTATIONS)
    n_ok = n_red - len([m for m in failed if m in [mm[0] for mm in MUTATIONS]])
    ctl_ok = sum(1 for st_, *_ in ctrl_rows if st_.endswith("OK"))
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {n_ok}/{n_red} 红（新鲜度两臂 / 生成器 fail-closed / F4 / F6）"
          + ("" if not failed else f"（未达预期：{', '.join(failed)}）"))
    ctl_what = "、".join(("{} 该{}".format(cid, "绿" if kind == "GREEN" else "被证伪"))
                         for cid, _d, _f, kind in CONTROLS)
    print(f"MUT: 对照 {ctl_ok}/{len(ctrl_rows)} 达预期（{ctl_what}）")
    print(f"MUT: 合计 {n_ok}/{n_red} 条判据变异 + {ctl_ok}/{len(ctrl_rows)} 条对照")
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty) else 1


if __name__ == "__main__":
    sys.exit(main())
