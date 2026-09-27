#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""§7 可复算性取证：脚本能不能独立再生**逐字节相同**的图。

做法（对每个场景 n = 1..3）：
  1. 把 `out-R{n}/` **只复制 make_figure.py** 到仓外临时目录（图与图注都不带）；
  2. 在该目录里跑 `python make_figure.py`，记退出码；
  3. 把新生成的 `figure.pdf` / `figure.png` 与**入库件**比字节 —— 两个口径都给：
     · `git hash-object`（本仓纪律：文件身份用 blob 哈希，不用裸 md5）
     · `md5`（**旧版 §7 用的就是 md5**，这里保留同一支仪器以便逐行对照；
        注意旧版把它标成 `committed=` 容易被读成 git blob，本工具改为显式命名）
  4. `caption.txt` 不由脚本再生，如实记为 `(absent)`。

输出里系统临时目录一律剥成 `<TMP>/`（本仓不写绝对路径）。
退出码：0 = 三份图都逐字节相同；1 = 有任一不同或脚本跑挂。
"""
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

RED = pathlib.Path(__file__).resolve().parent
REPO = RED.parent.parent.parent            # tests/skills/figure-choose/red -> 仓根


def blob(path):
    """git blob 哈希（本仓纪律口径）。"""
    out = subprocess.run(["git", "hash-object", str(path)], cwd=REPO,
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def head_blob(rel):
    """HEAD 里那份的 blob（证明比对对象是**入库**件，不是工作区随手一份）。"""
    out = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], cwd=REPO,
                         capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else "(not in HEAD)"


def md5(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="m3-t2-repro-"))
    print(f"temp workdir: <TMP>/{tmp.name}")
    bad = 0
    try:
        for n in (1, 2, 3):
            src, work = RED / f"out-R{n}", tmp / f"out-R{n}"
            work.mkdir(parents=True)
            shutil.copyfile(src / "make_figure.py", work / "make_figure.py")
            r = subprocess.run([sys.executable, "make_figure.py"], cwd=work,
                               capture_output=True, text=True)
            print(f"--- out-R{n}: rc={r.returncode}")
            if r.returncode != 0:
                bad += 1
                print("      stderr tail: " + r.stderr.strip().splitlines()[-1])
            for name in ("figure.pdf", "figure.png", "caption.txt"):
                rel = f"tests/skills/figure-choose/red/out-R{n}/{name}"
                cb, hb = blob(src / name), head_blob(rel)
                if not (work / name).exists():
                    print(f"      {name:<12} committed_blob={cb[:12]}"
                          f"  md5={md5(src / name)[:12]}  regenerated=(absent)"
                          f"  identical=False")
                    if name != "caption.txt":
                        bad += 1
                    continue
                rb = blob(work / name)
                same = cb == hb == rb
                if not same:
                    bad += 1
                print(f"      {name:<12} committed_blob={cb[:12]}"
                      f"  regenerated_blob={rb[:12]}  (HEAD={hb[:12]})"
                      f"  md5={md5(work / name)[:12]}  identical={same}")
            print()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"RESULT: {'ALL FIGURES BYTE-IDENTICAL' if not bad else f'{bad} MISMATCH/FAIL'}")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
