#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-plot-matlab` 的**样式新鲜度守卫**（计划 Task 2 硬要求 1）。**只读 + 原地重放后还原**：
除"查前先快照、原地重跑生成器写那份派生件、随后 `write_bytes` 还原成查前字节"之外不改任何东西；
还原**非原子**（进程在重跑与还原之间被杀会留脏，见下）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/plot-matlab/check-style-freshness.py
    python tests/skills/plot-matlab/check-style-freshness.py --table <表副本>   # 变异/演示用
    python tests/skills/plot-matlab/check-style-freshness.py --only A1          # 可选：只跑一条

退出码 **0 / 1**（与 `check-style-table-freshness.py` 同一条纪律：本器没有"判过且红"以外的第三种出口）；
末行**恒**为 `RESULT: …`；每条判词**一行**，形态 `PASS|FAIL  <id>  <读数>`；判红的差异上下文另起
**缩进行**（不以 `PASS`/`FAIL` 起头，故逐行解析器不受影响）。

## 新鲜度：为什么必须**先快照、再重跑**（本任务最容易做错的一处）

生成器 `gen-mcm-style-matlab.py` 是**原地写**的。照任务书原文"重跑生成器 → 与入库件逐字节相等"
实现是**恒真**的：一份**过期**的派生件被原地重跑一次就**被改对了**，再比对必然相等 ⇒ 这条判据
什么都抓不到。故本器的形态是：**先把要比对的两份字节取下来**，**再**重跑，**再**比对：

- **`A1` 入库快照臂**：比对对象 = `git show HEAD:<path>` 的字节（**受版本控制的那一份**）。
  它答的是"**入库的派生件是不是当前规范/表能重放出来的**"。表改了而派生件没重放 ⇒ 红。
- **`A2` 工作树臂**：比对对象 = **检查前**工作树里那一份的字节（在重跑**之前**快照的）。
  它答的是"**手头这份派生件是不是重放出来的**"。手工改派生件生成区（GC7 禁止）⇒ 重放把它改回去
  ⇒ 与**改前**快照不等 ⇒ 红。**A1 抓不到这一态**：工作树被手改而 HEAD 干净时，`A1` 比的是
  HEAD 与重放的结果，两者都干净、**相等**；只有把"重跑之前的字节"也留一份才有得比。

两条臂**都不恒真**，且**各有专属真红**（由 `mutate-plot-style.py` 的 `M62`/`M63` 证）：
`M62`（改表一个值 ⇒ 派生件落后 ⇒ `A1` 红、`A2` 绿 · `A1` 专属）·
`M63`（手改派生件生成区 ⇒ 重放会改对它 ⇒ `A2` 红、`A1` 绿 · `A2` 专属）。
重跑完成后**工作树一律还原成检查前的字节**（`write_bytes`）⇒ 正常收尾下工作树**不变**。但这**非原子**：
若进程在重跑与还原之间被杀（Ctrl-C / OOM），工作树会留下**重放后的**字节 —— 那时 `A2` 会红、能自曝。

## 与已知陷阱的关系（本仓纪律）

- 硬要求 2 要"锚点不命中 / 命中 >1 / 生成器跑不动 ⇒ 记红并非零退出"：那些 fail-closed 出口**在生成器里**
  （`gen-mcm-style-matlab.py` 的 `entry()`：id 命中 ≠ 1 / 值空 / 表里出现未知 H10 需求串 ⇒ 非零退出、
  **不写文件**）。本器的 `G0` 把那一路**兜成判红 + exit 1**。
- `G0` 红时 `A1`/`A2` **一并记红**（"生成器没跑成 ⇒ 无从比对"），不让"没判到"读成"通过"。
- **先例**：`tests/skills/plot-python/check-style-freshness.py`（同型两臂）。
"""
import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]          # tests/skills/plot-matlab → 仓根
GEN = ROOT / "tests/skills/plot-matlab/gen-mcm-style-matlab.py"
TABLE = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"
TARGET = ROOT / ".claude/skills/mcm-plot-matlab/assets/mcmplot.m"   # 派生件（生成器原地重写的那一份）
ALL_IDS = ("G0", "A1", "A2")


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


def run_generator(table_arg):
    """跑生成器（**唯一真调用形态**：cwd = 仓根；`--table` 只换输入表）。"""
    cmd = [sys.executable, str(GEN)] + (["--table", table_arg] if table_arg else [])
    try:
        pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    except OSError as e:                                     # 起不动解释器 / 脚本不在
        return None, "", f"{type(e).__name__}: {e}"
    return pr.returncode, pr.stdout, pr.stderr


def diff_context(expected, actual, limit=3):
    """逐字节不等时打印的**差异处上下文**：取首个相异行，前后各 `limit` 行。"""
    try:
        el = expected.decode("utf-8").splitlines()
        al = actual.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        n = next((i for i, (x, y) in enumerate(zip(expected, actual)) if x != y),
                 min(len(expected), len(actual)))
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


def main():
    ap = argparse.ArgumentParser(description="mcm-plot-matlab：样式新鲜度守卫（两臂）")
    ap.add_argument("--table", default=None, help="被读的样式表（默认 = 仓内 mcm-style.json；变异/演示用）")
    ap.add_argument("--only", default=None, choices=ALL_IDS, help="只跑一条判据（可选）")
    a = ap.parse_args()
    table_arg = a.table
    table_shown = _shown(pathlib.Path(table_arg)) if table_arg else _shown(TABLE)

    print("样式新鲜度守卫（Task 2）· 派生件只许由 tests/skills/plot-matlab/gen-mcm-style-matlab.py 重放产出")
    print(f"表 = {table_shown}")
    print(f"派生件 = {TARGET.name}   ·   A1 快照臂 = `git show HEAD:<path>`"
          f"   ·   A2 工作树臂 = 检查前的工作树字节")

    rows = []                                                # (id, ok, detail, extra_lines)
    snap_err = []
    want = set(ALL_IDS) if a.only is None else {a.only}

    # ---------------- 取两份快照（**必须在重跑之前**）
    head = wt = None
    if "A1" in want:
        try:
            head = git_snapshot(TARGET)
        except RuntimeError as e:
            snap_err.append((f"A1:{TARGET.name}", f"取不到入库快照（fail-closed）：{e}"))
    try:                                                     # wt **一律**取：既是 A2 的比对物，也是还原用的底本
        wt = TARGET.read_bytes()
    except OSError as e:
        if "A2" in want:
            snap_err.append((f"A2:{TARGET.name}", f"读不出工作树字节（fail-closed）：{type(e).__name__}: {e}"))

    # ---------------- 重跑生成器（跑完**一律还原**工作树）
    rc, gout, gerr = run_generator(table_arg)
    gen = None
    try:
        gen = TARGET.read_bytes()
    except OSError as e:
        snap_err.append((f"GEN:{TARGET.name}", f"重跑后读不出（fail-closed）：{type(e).__name__}: {e}"))
    finally:
        if wt is not None:                                   # 还原：本器非侵入
            TARGET.write_bytes(wt)

    # ---------------- G0：生成器本身
    if "G0" in want:
        if rc is None:
            rows.append(("G0", False, f"生成器起不动（{gerr}）（fail-closed）", []))
        elif rc != 0:
            tail = (gerr or gout).strip().splitlines()
            rows.append(("G0", False, f"生成器退出 {rc}（fail-closed）：{tail[-1][:200] if tail else '（无输出）'}", []))
        else:
            n = next((l for l in gout.splitlines() if "锚点" in l and "条" in l), "锚点 ? 条")
            rows.append(("G0", True, f"重放成功（{n.strip()}）", []))

    # ---------------- A1 / A2：两条臂
    gen_failed = (rc is None or rc != 0)
    for rid, snap, who in (("A1", head, "入库快照（HEAD）"), ("A2", wt, "工作树快照（检查前）")):
        if rid not in want:
            continue
        if snap is None:
            continue                                         # 快照取不到：已按 `snap_err` 判红
        if gen_failed or gen is None:                        # D4：生成器没跑成 ⇒ 两条臂一并记红
            why = "生成器未跑成（见 G0）" if gen_failed else "重放后的字节读不出"
            rows.append((rid, False, f"{why} ⇒ 无从比对（fail-closed）", []))
            continue
        if gen == snap:
            rows.append((rid, True, f"重放 == 快照（{len(snap)} 字节）", []))
        else:
            rows.append((rid, False, f"重放 != {who}（快照 {len(snap)} 字节 / 重放 {len(gen)} 字节）",
                         diff_context(snap, gen)))

    # ---------------- 判词（每条一行；上下文另起缩进行；末行恒为 RESULT）
    for sid, sdetail in snap_err:
        print(f"FAIL  {sid}  {sdetail}")
    for rid, ok, detail, extra in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {rid}  {detail}")
        for line in extra:
            print(line)
    bad = [sid for sid, _d in snap_err] + [rid for rid, ok, _d, _e in rows if not ok]
    print("-" * 78)
    print(f"判据 {len(rows) + len(snap_err)} 条 · 红 {len(bad)} 条 · 派生件 1 份 · 生成器 exit={rc}")
    print("RESULT: PASS" if not bad else f"RESULT: FAIL（{','.join(bad)}）")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
