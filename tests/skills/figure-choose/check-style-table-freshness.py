#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mcm-style.json 新鲜度守卫。只读 + 重跑生成器 + 逐字节比对。

两条臂（缺一不可，理由同 check-style-freshness.py：生成器会**原地重写**派生件）：
  A1 入库快照臂：比 `git show HEAD:<path>` 的原始字节
  A2 工作树臂  ：比**重跑之前**读到的工作树字节
退出码 0/1（本器无 2）。末行恒为 `RESULT: …`。

## 为什么必须"先快照、再重跑"

`gen-style-table.py`（不带 `--check`）是**原地写**的。若照"重跑 → 与当前件逐字节相等"实现，
判据**恒真**：一份过期/被手改的派生件被重跑一次就被改对了，再比对必然相等。故本器的形态是
**先把要比对的两份字节取下来，再重跑，再比对**：A1 抓"入库的派生件是不是当前规范能重放出来的"，
A2 抓"手头这份是不是重放出来的"（手改派生件时 A1 抓不到 —— 工作树被手改而 HEAD 干净时两臂才有分工）。
重跑完成后工作树一律还原成检查前的字节；还原**非原子**（进程在重跑与还原之间被杀会留脏）。

## 排期注意（本项目硬纪律 10 的"先提交、再证不动点"）

A1 比的是 `HEAD:<path>`。**派生件首次入库前，`git show HEAD:` 取不到它 ⇒ A1 必红**
（这是本器的正确行为，不是缺陷）。故本器在**新件首次提交之后**才会两臂全绿 —— 提交前的
一次跑只用来暴露 A1，不作为验收。

## 与派发任务书的一处偏差

任务书给的骨架写 `ROOT = ...parents[2]`。本文件在 `tests/skills/figure-choose/` 下，
`parents[2]` 落在 `tests/`（⇒ `TARGET`/`GEN` 全会指到不存在的路径）。**照 `check-style-freshness.py`
同一深度取 `parents[3]`**（仓根）。这是**改正**，见 task-m3-style-t2-report.md。
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]     # tests/skills/figure-choose → 仓根
TARGET = ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"
GEN = ROOT / "tests/skills/figure-choose/gen-style-table.py"
REL = TARGET.relative_to(ROOT).as_posix()


def snapshot_head():
    r = subprocess.run(["git", "show", f"HEAD:{REL}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def run():
    head = snapshot_head()
    wt = TARGET.read_bytes()
    rows, bad = [], 0
    try:
        rc = subprocess.run([sys.executable, str(GEN)], cwd=ROOT, capture_output=True).returncode
        for arm, want in (("A1", head), ("A2", wt)):
            if rc != 0 or want is None:
                rows.append(("FAIL", arm, "生成器没跑成或参照缺失 ⇒ 两臂一并记红"))
                bad += 1
                continue
            now = TARGET.read_bytes()
            ok = now == want
            rows.append(("PASS" if ok else "FAIL", arm,
                         "逐字节一致" if ok else f"不一致（{len(want)}B → {len(now)}B）"))
            bad += 0 if ok else 1
    finally:
        TARGET.write_bytes(wt)          # 还原（非原子：进程在重跑与还原之间被杀会留脏，那时 A2 会自曝）
    for st, arm, note in rows:
        print(f"{st}  {arm}  {note}")
    print(f"RESULT: {'PASS' if bad == 0 else 'FAIL'}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(run())
