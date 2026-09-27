#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐格验收：对 expected.tsv 的每一行跑一次检查器，比对期望。
captions.tsv 存图注文本 fixture（sample 列写 caption:<n>）。

⚠️ **借位声明**：`caption:<n>` 那几行只验 F3a–F3d（图注形态），而检查器要求必须给一张图，
故**借用 `ok-01.png`** 来满足接口。这是**借位**，不是判据：那几行的 F1/F2 读数**不代表**
被验对象的图宽/配色（本脚本对它们不比对 F1/F2，见下面的过滤器）。借位行在输出里带
`(fig borrowed: ok-01.png)` 标注，**不许把它读成"图注 fixture 的图也合格"**。

⚠️ **"没判成" ≠ "判成红"**（独立复审判定 R-5 逼出）：本脚本按**判词**比对，而**崩掉的运行**
（未捕获异常、fail-closed 退出）在 stdout 上要么什么都不打、要么打得像失败——旧版只看
`PASS  <crit>` 在不在，于是**崩溃 ⇒ 记成 FAIL**，正好把「期望 FAIL 的行」记成 **OK**。
这正是本项目最怕的那种盲区。故本版每行先验运行本身：
**`rc ∉ {0,1}`（含 fail-closed 的 2）或 stdout 里没有 `RESULT:` 行 ⇒ 记 `ERROR`**，
不参与 PASS/FAIL 比对，且整轮 exit 非零。只有 `rc ∈ {0,1}` 且打出判词行，才去读那条判据。

⚠️ **图样本的图注不带尾句号**（独立复审判定 R-7 逼出）：旧版给图样本配的是
`Figure 1: A test figure caption.`（**自带句号** ⇒ F3c 必红），于是**每一行图样本的判词里
都混着一条与它无关的 `FAIL F3c`**，证据不干净、复核员容易误读。现改成不带尾句号的
`Figure 1: A test figure caption`（F3a/F3b/F3c/F3d 全 PASS）⇒ **图样本那几行只剩它们各自
要测的那条**，翻红即所指。

用法：`python tests/skills/figure-choose/fixtures/run-expected.py [--checker <path>]`
  `--checker` 只给**变异探针**用（`mutate-figure-style.py` 的 P1：把被测检查器指到 `_mut/`
  里的副本，好证明下面那条 ERROR 分支真的会红）；**默认就是 `../check-figure-style.py`**，
  收工 gate 一律不带该参数跑。
"""
import argparse
import pathlib
import subprocess
import sys

D = pathlib.Path(__file__).parent
ap = argparse.ArgumentParser(description="逐格验收（expected.tsv）")
ap.add_argument("--checker", default=None,
                help="被测检查器（默认 ../check-figure-style.py；变异探针用）")
_arg = ap.parse_args().checker
CHK = pathlib.Path(_arg) if _arg else (D.parent / "check-figure-style.py")
IMG_CAP = "Figure 1: A test figure caption"          # 无尾句号：见文件头 R-7
CAPS = {n: t.strip() for n, t in
        (l.split("\t", 1) for l in (D / "captions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())}
bad = total = nerr = 0
try:                                    # 证据里不写绝对路径：能相对就相对
    CHK_SHOWN = CHK.resolve().relative_to(D.parents[3].resolve())
except Exception:                       # noqa: BLE001（纯显示用）
    CHK_SHOWN = CHK
print(f"# checker: {str(CHK_SHOWN).replace(chr(92), '/')}")   # 判词属于哪支检查器，写进输出
print("flag      sample                   crit want got")
for line in (D / "expected.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    if not line.strip():
        continue
    sample, crit, want = line.split("\t")
    # 图注 fixture 的 F1/F2 不适用（借用 ok-01），只核它们自己那条判据
    if sample.startswith("caption:") and crit not in ("F3a", "F3b", "F3c", "F3d"):
        continue
    total += 1
    borrowed = "  (fig borrowed: ok-01.png)" if sample.startswith("caption:") else ""
    if sample.startswith("caption:"):
        cmd = [sys.executable, str(CHK), "--fig", str(D / "ok-01.png"),
               "--caption", CAPS[sample.split(":")[1]], "--textwidth-in", "6.31", "--dpi", "200"]
    else:
        cmd = [sys.executable, str(CHK), "--fig", str(D / sample),
               "--caption", IMG_CAP, "--textwidth-in", "6.31", "--dpi", "200"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out, rc = proc.stdout, proc.returncode
    if rc not in (0, 1) or "RESULT:" not in out:      # 没判成：RC 异常，或压根没打判词行
        nerr += 1
        print(f"{'ERROR':9} {sample:24} {crit:4} rc={rc} 没产生判词（fail-closed 或崩溃）{borrowed}")
        continue
    got = "PASS" if f"PASS  {crit} " in out else "FAIL"
    flag = "OK" if got == want else "MISMATCH"
    bad += flag == "MISMATCH"
    print(f"{flag:9} {sample:24} {crit:4} want={want:4} got={got}{borrowed}")
print(f"MISMATCH {bad} / {total}" + (f"  ERROR {nerr}" if nerr else ""))
sys.exit(0 if (bad == 0 and nerr == 0) else 1)
