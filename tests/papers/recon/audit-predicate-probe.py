"""C-1 先量：把 `ABSPATH_TRACE` 的 POSIX 支换成与 `_ABS_POSIX` 同一套交替式后，
全部入库证据的 `path_audit` 有没有从干净变红。

口径：只扫**文本**文件（放行证据 / recon 记录 / 产出的 md / 词表 / docs）。
`corpus/papers/{figures,formulas}` 是 PNG，二进制解码后必然乱命中，不在扫描面内。

**旧谓词是硬编码的（2026-09-26 更正）**：本探针原先用 `report.ABSPATH_TRACE` 当"旧"、
用本地一份交替式当"新"——**统一之后两者成了同一串**，于是它必然打印"判定翻转 0 份"
（**自己跟自己比**），那条记录也就**复现不了**了（这正是 `mcm-suite-lessons.md` 4.8 的
"引用复现不了"形态）。现在：`OLD` = **`fad9384` 之前**那条谓词（逐字硬编码，只在那一刻
有区分力），`NEW` = **现行** `report.ABSPATH_TRACE`（走 `report.path_audit` 这个真入口）。
⇒ 本脚本量的是"**当时的改动**在今天会不会让任何一份从干净变红"，**可重跑、可复现**。

复现命令（`tools/papers/report.py` 的注释里指名的就是本脚本）：
`PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/audit-predicate-probe.py`
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]     # tests/papers/recon/
os.chdir(ROOT)      # 本脚本按仓库相对路径扫，与调用时的 cwd 无关
sys.path.insert(0, str(ROOT))
from tools.papers import report  # noqa: E402

# **旧谓词**：`git show fad9384^:tools/papers/report.py:63` 的逐字原文。
# 与现行那条只差 POSIX 支（旧：`Users|home|root`；新：再加 `tmp|var|opt|mnt|Volumes`）。
OLD = re.compile(r"\b[A-Za-z]:[\\/]|\\\\[^\s]|/(?:Users|home|root)/")
NEW = report.ABSPATH_TRACE                      # 现行（= `path_audit` 实际用的那条）

print("OLD pattern（fad9384 之前，硬编码）:", OLD.pattern)
print("NEW pattern（现行 report.ABSPATH_TRACE）:", NEW.pattern)
print("两条逐字相同 =", OLD.pattern == NEW.pattern, "（**必须 False**——"
      "相同就说明这次量的又是自己跟自己比）")

roots = [Path("tests/papers/reports"), Path("tests/papers/recon"),
         Path("corpus/papers"), Path("tools/papers/vocab")]
files = []
for r in roots:
    files += sorted(p for p in r.rglob("*") if p.is_file() and p.suffix != ".png")
files += [Path("docs/mcm-suite-todo.md")]

old_red, new_red, flipped = [], [], []
for p in files:
    try:
        t = p.read_bytes().decode("utf-8", "replace")
    except OSError:
        continue
    o = OLD.search(t)
    n = report.path_audit(t)        # 现行谓词的真入口（不是本地复制品）
    if o:
        old_red.append((p, o.group(0)))
    if n:
        new_red.append((p, n))
    if bool(o) != bool(n):
        flipped.append((p, o.group(0) if o else "", n))

print(f"\n扫描 {len(files)} 份文本文件 · 旧谓词命中（红）{len(old_red)} 份 · "
      f"新谓词命中（红）{len(new_red)} 份 · 判定翻转 {len(flipped)} 份")

print("\n=== 判定翻转（任一方向）===")
for p, o, n in flipped:
    print(f"  {p}\n      old={o!r} new={n!r}")
print("（空 = 没有一份因为这次统一而改变判定）")

print("\n=== 旧谓词已红的那些（现行谓词仍应全部命中同一处）===")
for p, m in old_red:
    print(f"  {p}: {m!r}")

print("\n=== 新谓词命中明细（含旧谓词已命中的）===")
for p, n in new_red:
    t = p.read_bytes().decode("utf-8", "replace")
    ls = [(i + 1, ln) for i, ln in enumerate(t.splitlines()) if NEW.search(ln)]
    print(f"  {p}: 命中 {len(ls)} 行 · 首处 {n!r}")
    for i, ln in ls[:2]:
        print(f"      :{i} {ln.strip()[:110]}")
