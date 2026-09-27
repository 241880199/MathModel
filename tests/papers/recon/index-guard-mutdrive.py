"""`tools/papers/index.py` 的**限样本覆写守卫**的变异驱动器（Task M2-hygiene · 2026-09-27）。

**为什么新写一份、而不是并进 `build/ids_mutdrive.py`**：那份在 `build/`（gitignored）
⇒「驱动器本身不入库」是本项目已登记的债（`docs/mcm-suite-todo.md` §D.10，Task 7 起
新探针一律放 `tests/papers/recon/`）。本文件**入库**，与它写出的证据同处可复现路径上。

**它证明什么**（三条，各配一次对照）：

| 编号 | 形态 | 期望 |
| :--- | :--- | :--- |
| **MA** | 调用点**显式**把 `out_dir` 指到 `io.DERIVED`（+ 给了 `sample`） | **必须抛**（新守卫：判的是**落点**，不是「有没有给 out_dir」） |
| **MA-0** | 同上，**再把守卫倒回旧谓词**（`if out_dir is None:`）= **改前形态** | **不抛**、且**真的把入库产物覆写**成 5 份版本 ⇒ `sha256` 自检判 `False`、`RESULT: FAIL` |
| **MB** | 合集名不存在（**且给了 `sample`**） | 仍须抛 `FileNotFoundError`（既有 I11 的 fail-closed 不被这次改动破坏） |

**MA-0 是「改前确实会覆写」的**可复现**证据**：它不是"我记得那一刻是那样的"，
而是把守卫倒回旧谓词后当场重演（改前那次真实复现的记录在改前探针里，形态一致）。

## 纪律（与 `build/ids_mutdrive.py` 逐条同）

* **清 `__pycache__` + 子进程 `PYTHONDONTWRITEBYTECODE=1` 必须配对**（前者只禁**写**、
  不禁**读**；`cpython` 的 `.pyc` 失效判据是「源文件 mtime **整数秒** + 字节数」，
  「改坏 → 跑 → 还原」落在同一秒且字节数不变时进程会继续加载**被改坏的字节码」）。
* **锚点必须恰好命中 1 次**；施加前后 `git hash-object` 必须不同。
* **还原用双轨**：`git hash-object`（blob）**加**原始字节 sha256——只看 blob 会被
  行尾过滤糊过去。
* **探针绝不许当破坏者**：MA / MA-0 两条都按 `touch` 处理（跑前留三份入库产物的原始
  字节，跑后**无条件**按字节还原并断言 blob 复原），即使守卫那天回归了、它们真的写了，
  也不会留下残骸。还原失败**并进退出码**。
* 报告走 `tools/papers/report.py` 的 `flush()`（`write_bytes` + LF），
  全文过 `path_audit`（绝对路径痕迹 ⇒ 判 FAIL 并进退出码）。

用法（仓库根）：

    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/index-guard-mutdrive.py
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.papers import report as rep  # noqa: E402

VERIFY = "tests/papers/verify_ids.py"
INDEX_PY = "tools/papers/index.py"
PROBE = ROOT / "tests" / "papers" / "recon" / "index-guard-probe.py"
# 改前实测的逐字记录（**历史，不可重跑**）。驱动器把它的内容**读进来原样嵌入**报告，
# 免得那一段只活在 gitignored 的 `build/`（本项目规矩：放那里等于丢失）。
PRECHANGE = ROOT / "tests" / "papers" / "recon" / "index-guard-prechange.txt"
PRODUCTS = ["corpus/papers/INDEX.md", "corpus/papers/TAGS.md", "corpus/papers/PROVENANCE.md"]
EVIDENCE = "tests/papers/reports/index-guard-evidence.txt"
LIMIT = "3"

# 调用点（`verify_ids.py` 里唯一一处 `index_mod.build`）——三条变异都改它。
CALLSITE_OLD = ('    res = index_mod.build(COLLECTION, sample=None if limit <= 0 else sample,\n'
                '                          out_dir=prod_dir)\n')
CALLSITE_DERIVED = (
    '    res = index_mod.build(COLLECTION, sample=None if limit <= 0 else sample,\n'
    '                          out_dir=io.DERIVED)   # 变异：显式指向入库产物\n')
CALLSITE_MISSING = (
    '    res = index_mod.build(COLLECTION + "X", sample=None if limit <= 0 else sample,\n'
    '                          out_dir=prod_dir)   # 变异 MB：合集名不存在\n')
# 守卫谓词（新 → 旧）。旧谓词只看 `out_dir is None` ⇒ 显式给 `io.DERIVED` 绕得过去。
PRED_NEW = "        if on_derived:\n"
PRED_OLD = "        if out_dir is None:   # 变异 MA-0：倒回旧谓词（只看 out_dir 是不是 None）\n"

# (编号, [(文件, 锚点, 替换), …], 期望逐字出现的标记, 说明, touch)
MUTATIONS = [
    (
        "MA", [(VERIFY, CALLSITE_OLD, CALLSITE_DERIVED)],
        ["不得落到入库产物", "即使显式指定 out_dir"],
        "**显式**把 `out_dir` 指到入库产物（`sample` 也给了）——旧谓词（`out_dir is None`）"
        "对这一写法**不触发**，于是三份已放行的产物会被**静默覆写**成 5 份的版本。"
        "新守卫判的是**落点**，必须当场抛 `ValueError`（在任何写盘动作之前）。",
        True,
    ),
    (
        "MA-0", [(INDEX_PY, PRED_NEW, PRED_OLD), (VERIFY, CALLSITE_OLD, CALLSITE_DERIVED)],
        ["跑前跑后相同 = False"],
        "**改前形态的可复现重演**：把守卫谓词倒回 `if out_dir is None:`，其余（含上面那条"
        "调用点写法）不变 ⇒ `build` **不抛**、真的把入库的三份产物写成 5 份版本 ⇒ "
        "`verify_ids` 自己的 `sha256` 自检判 `False` 并 `RESULT: FAIL`。"
        "`I2=FAIL`（`IndexResult` 报的落点与实际写的不一致）也会一并红。",
        True,
    ),
    (
        "MB", [(VERIFY, CALLSITE_OLD, CALLSITE_MISSING)],
        ["合集目录不存在"],
        "**既有 fail-closed 的保持性检查**：合集名不存在、`sample` 也给了、`out_dir` 是"
        "不入库目录 ⇒ 仍须抛 `FileNotFoundError`（`Path.rglob` 对不存在的目录静默返回空，"
        "这一条是 I11 的实体）。本条**不写盘**：抛在取数之前。",
        False,
    ),
]


def sh(cmd: list[str]) -> tuple[int, str]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, timeout=3600, env=env)
    return (r.returncode,
            r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace"))


def blob_sha(p: Path) -> str:
    rc, out = sh(["git", "hash-object", str(p.relative_to(ROOT).as_posix())])
    return out.strip() if rc == 0 else f"<hash-object 失败 rc={rc}>"


def run_verify() -> tuple[int, str]:
    return sh([sys.executable, VERIFY, "--limit", LIMIT])


def clean(out: str) -> str:
    """证据块：滤掉 `^MuPDF error` 行与空行，**不截尾**。"""
    return "\n".join(ln for ln in out.splitlines()
                     if not ln.startswith("MuPDF error") and ln.strip())


def purge_pycache() -> list[str]:
    n = []
    for d in sorted(ROOT.rglob("__pycache__")):
        if d.is_dir():
            n.append(d.relative_to(ROOT).as_posix())
            shutil.rmtree(d, ignore_errors=True)
    return n


def apply_mutation(path: Path, old: str, new: str) -> dict:
    """施加变异。**锚点按该文件实际行尾转换后再比对**。"""
    raw = path.read_bytes()
    crlf = b"\r\n" in raw
    conv = (lambda s: s.replace("\n", "\r\n")) if crlf else (lambda s: s)
    old_b, new_b = conv(old).encode("utf-8"), conv(new).encode("utf-8")
    n = raw.count(old_b)
    before = hashlib.sha256(raw).hexdigest()
    info = {"path": path, "rel": path.relative_to(ROOT).as_posix(), "crlf": crlf,
            "anchor_hits": n, "sha_before": before, "applied": False,
            "sha_after": before, "blob_before": blob_sha(path), "blob_after": "",
            "_raw": raw}
    if n != 1:
        return info
    path.write_bytes(raw.replace(old_b, new_b))
    info["applied"] = True
    info["sha_after"] = hashlib.sha256(path.read_bytes()).hexdigest()
    info["blob_after"] = blob_sha(path)
    return info


def restore_all(infos: list[dict]) -> list[tuple[str, bool, bool]]:
    """**按文件**还原：同一文件的多次改动只还原一次，用**最早**那份原始字节。"""
    seen: dict[str, dict] = {}
    for info in infos:
        seen.setdefault(info["rel"], info)
    out = []
    for rel, info in seen.items():
        info["path"].write_bytes(info["_raw"])
        out.append((rel,
                    hashlib.sha256(info["path"].read_bytes()).hexdigest() == info["sha_before"],
                    blob_sha(info["path"]) == info["blob_before"]))
    return out


def main() -> int:
    import datetime
    A: list[str] = []
    W = A.append
    touched = sorted({rel for entry in MUTATIONS for rel, _o, _n in entry[1]})
    base = {rel: {"raw": (ROOT / rel).read_bytes(), "blob": blob_sha(ROOT / rel)}
            for rel in touched}
    frozen_pre = {f: blob_sha(ROOT / f) for f in PRODUCTS}

    W("# 限样本覆写守卫（`index.build`）的变异证据 · Task M2-hygiene（2026-09-27）")
    W("")
    W(f"日期：{datetime.date.today().isoformat()}　·　被测代码：`{INDEX_PY}`"
      f"（守卫）·　判据脚本：`{VERIFY}`。")
    W("")
    W(f"**驱动器**：`tests/papers/recon/index-guard-mutdrive.py`（**入库**——"
      f"不重复 `build/ids_mutdrive.py` 那条「驱动器不入库」的债）。")
    W(f"**命令**：`PYTHONDONTWRITEBYTECODE=1 python {rep.rel(Path(__file__))}` → 逐条跑 "
      f"**`python {VERIFY} --limit {LIMIT}`**（样本量与该跑的取样清单见每块输出里的 "
      f"`取样：` 行，**逐字输出、不手抄**）。")
    W("**没有为了本证据跑过全量 43 份**（全量只用于放行校验，写 "
      "`tests/papers/reports/ids-report.txt`）。")
    W("")
    W("## 证据块的取法（**这一句必须成立**）")
    W("")
    W(f"每条变异下面是 **`python {VERIFY} --limit {LIMIT}` 的 stdout 全文**，**不截尾**；"
      f"**只滤掉两类行**：`^MuPDF error` 开头的（MuPDF 的 C 层噪声，实测走 stdout）与空行。"
      f"其余一字不动。")
    W("")
    W("每条下面还有**驱动器的断言结果**（不是「我认为它会红」）：`EXIT != 0` 且输出含 "
      "`RESULT: FAIL` 且期望标记**逐字出现**；对照（变体 0）必须 `EXIT == 0`、含 "
      "`RESULT: PASS`、且**不含**任何 `=FAIL`。")
    W("")
    W("**清缓存两条必须配对**：每条跑判据前清 `__pycache__`，子进程一律带 "
      "`PYTHONDONTWRITEBYTECODE=1`（只禁**写**不禁**读**，清缓存才是起作用那一步），"
      "**清了几何个目录逐条写在本文件里**。")
    W("")
    W("## 覆盖边界（**这条也要如实说**）")
    W("")
    W("本轮覆盖三条：**新守卫对「显式指向入库产物」生效**（MA）· **改前形态确实会覆写**"
      "（MA-0，可复现重演）· **既有 fail-closed 不被破坏**（MB）。")
    W("")
    W("**未覆盖（登记在这里而不是假装没有）**：① 新守卫的 `resolve()` 分支（路径等价类，"
      "如 `./corpus/papers`、大小写差异）只由 MA-0 之外的**命令行探针**量过"
      "（`--limit 3` 用例，逐字见本文件末尾）；② 既有 I11 的**红路**由 "
      "`tests/papers/reports/ids-mutation-evidence.txt` 的 **M2**（删掉 fail-closed 守卫）"
      "证明——本条 MB 只补「`sample` 同时给出」的那一支；③ 「`sample` 给了 + 合集名不存在"
      " + `out_dir` 指到入库产物」时**哪条守卫先响**（实测是新守卫先响，两条都抛、都 "
      "fail-closed）**没有**单独做变异——它不改变结论，只改变消息。")
    W("")
    # ---- 改前实测（历史，**不可重跑**）：逐字嵌进本节，免得它只活在 gitignored 的 build/
    W("## 改前实测（历史记录 · **不可重跑**）：这条敞口**真的**存在过")
    W("")
    W("MA-0 是它的**可复现重演**；下面这份是加严**之前**当场跑出来的原始记录"
      "（探针只在一次性的 `build/` 暂存区里，故把逐字输出搬进入库文件，"
      "原本见 `tests/papers/recon/index-guard-prechange.txt`——**本节是它的逐字副本**，"
      "由驱动器读入、不手抄）：")
    W("")
    W("```")
    W(PRECHANGE.read_text(encoding="utf-8").rstrip("\n"))
    W("```")
    W("")
    W("## 对照（变体 0）")
    W("")
    results: list[tuple[str, bool, str]] = []
    touch_bad: list[str] = []
    cleared = purge_pycache()
    rc, out = run_verify()
    hit = re.findall(r"^I[0-9]+(?:-[a-z])?=FAIL", out, re.M)
    control_ok = (rc == 0 and "RESULT: PASS" in out and not hit)
    W(f"* 跑前清 `__pycache__`：**{len(cleared)}** 个目录"
      + (f"（{'、'.join(cleared[:3])}…）" if cleared else "")
      + "　·　子进程带 `PYTHONDONTWRITEBYTECODE=1`（**与清缓存配对**）")
    W(f"* 退出码 = {rc}（要求 0）")
    W(f"* 含 `RESULT: PASS` = {'RESULT: PASS' in out}（要求 True）")
    W(f"* 不含任何 `=FAIL` 标记 = {not hit}（要求 True；实际命中 {hit}）")
    W(f"* **对照通过 = {control_ok}**")
    W("")
    W("对照跑的输出（逐字全文，取法见文件头）：")
    W("")
    W("```")
    W(clean(out))
    W("```")
    W("")
    results.append(("对照（变体 0）", control_ok, "" if control_ok else "对照跑未绿"))

    for entry in MUTATIONS:
        mid, edits, marks, desc = entry[:4]
        touch = len(entry) > 4 and entry[4]
        W(f"## {mid}：{desc}")
        W("")
        infos = []
        for rel, old, new in edits:
            info = apply_mutation(ROOT / rel, old, new)
            infos.append(info)
            W(f"* 文件 `{rel}`：行尾 {'CRLF' if info['crlf'] else 'LF'}　·　"
              f"锚点在原始字节里找到 **{info['anchor_hits']}** 次（必须恰好 1 次）")
            W(f"* 已施加 = {info['applied']}（要求 True）；blob "
              f"`{info['blob_before'][:16]}…` → `{info['blob_after'][:16]}…`（必须不同）")
        W("")
        pre_raw = {f: (ROOT / f).read_bytes() for f in PRODUCTS} if touch else {}
        cleared = purge_pycache()
        rc, out = run_verify()
        W(f"* 跑前清 `__pycache__`：**{len(cleared)}** 个目录"
          + (f"（{'、'.join(cleared[:3])}…）" if cleared else "")
          + "　·　子进程带 `PYTHONDONTWRITEBYTECODE=1`（**与清缓存配对**）")
        found = [m for m in marks if m in out]
        extra = [x for x in re.findall(r"^I[0-9]+(?:-[a-z])?=FAIL", out, re.M)
                 if x not in marks]
        missing = [m for m in marks if m not in out]
        passed = (rc != 0 and "RESULT: FAIL" in out and not missing)
        W(f"* 退出码 = {rc}（要求非 0）")
        W(f"* 含 `RESULT: FAIL` = {'RESULT: FAIL' in out}（要求 True）")
        W(f"* 逐字命中的标记 = {found + extra}（**要求 ⊇ {marks}**；缺 {missing or '无'}）")
        W(f"* **本条变异通过 = {passed}**")
        W("")
        W("变异跑的输出（逐字全文，取法见文件头）：")
        W("")
        W("```")
        W(clean(out))
        W("```")
        W("")
        if touch:
            W("* **本条按 `touch` 处理**：跑前留三份入库产物的原始字节，下面**无条件**按"
              "字节还原并断言 blob 复原——守卫哪天回归了也不会留下残骸"
              "（MA 这一条**期望它没写**，MA-0 **期望它写了**；两者都按同一套兜底）：")
            wrote = [f for f in PRODUCTS if blob_sha(ROOT / f) != frozen_pre[f]]
            for f in PRODUCTS:
                (ROOT / f).write_bytes(pre_raw[f])
                same_touch = blob_sha(ROOT / f) == frozen_pre[f]
                if not same_touch:
                    touch_bad.append(f)
                W(f"* `{f}`：本次跑到还原前 blob 与跑前"
                  f"{'**不同**（真的被覆写了）' if f in wrote else '相同（没被写）'}"
                  f"　·　还原后与跑前相同 = {same_touch}（跑前 `{frozen_pre[f][:16]}…`）")
            W(f"* **本条实测覆写了入库产物 = {bool(wrote)}**"
              f"（MA 要求 `False`——守卫必须在写盘之前抛；MA-0 要求 `True`——那正是它要"
              f"证明的改前形态）")
            W("")
        restored_all = True
        for rel, same_sha, same_blob in restore_all(infos):
            restored_all = restored_all and same_sha and same_blob
            W(f"* 还原 `{rel}`：sha256 与施加前相同 = {same_sha}　·　`git hash-object` "
              f"blob 相同 = {same_blob}（两条都要 True）")
        W("")
        results.append((mid, passed and restored_all,
                        "未通过" if not passed else ("未还原" if not restored_all else "")))

    # ---- 命令行探针：`resolve()` 那一支（等价路径 / 相对路径）-------------
    # 它**不改任何文件**，只调 `index.build`，故不放进变异表；逐字落盘以便复核。
    W("## 命令行探针（**不改任何文件**）：守卫的 `resolve()` 分支与 fail-closed 的分支")
    W("")
    W("变异表覆盖不到的三支（等价路径 `resolve()`、相对路径、以及「哪条守卫先响」）"
      "由 `tests/papers/recon/index-guard-probe.py` 逐条断言——它**入库**，"
      "与本节证据同处可复现路径上（不像变异表那样只活在驱动器里）：")
    W("")
    W("```")
    W(f"$ PYTHONDONTWRITEBYTECODE=1 python {rep.rel(PROBE)}   （cwd = 仓库根）")
    W("```")
    W("")
    rc3, out3 = sh([sys.executable, str(PROBE.relative_to(ROOT).as_posix())])
    W(f"退出码 = {rc3}")
    W("")
    W("```")
    W(clean(out3))
    W("```")
    W("")

    # ---- 收尾断言 ---------------------------------------------------------
    W("### 收尾断言 ①：被改文件必须回到**开工基准**（逐字节 + blob 双轨）")
    W("")
    bad = []
    for rel, info in base.items():
        same_sha = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == \
            hashlib.sha256(info["raw"]).hexdigest()
        same_blob = blob_sha(ROOT / rel) == info["blob"]
        if not (same_sha and same_blob):
            bad.append(rel)
        W(f"* `{rel}`：与开工基准逐字节相同 = {same_sha}　·　blob 相同 = {same_blob}"
          f"（基准 blob = `{info['blob'][:16]}…`）")
    W("")
    W("### 收尾断言 ②：入库的三份产物全程未被改动（`touch` 的两条已按字节还原）")
    W("")
    for f in PRODUCTS:
        now = blob_sha(ROOT / f)
        same = now == frozen_pre[f]
        if not same:
            bad.append(f)
        W(f"* `{f}`：blob 跑前跑后相同 = {same}"
          f"（跑前 `{frozen_pre[f][:16]}…` · 跑后 `{now[:16]}…`）")
    W("")
    W(f"**驱动器断言全部通过 = {not bad and all(p for _m, p, _r in results)}**"
      f"（对照跑绿 · 三条变异按期望红/绿 · 被改文件逐字节还原 · 入库产物零差异"
      f"{'；异常：' + str(bad) if bad else ''}）")
    W("")
    W("| 编号 | 通过 | 备注 |")
    W("| :--- | :--- | :--- |")
    for mid, passed, note in results:
        W(f"| {mid} | {passed} | {note if note else '—'} |")
    W("")

    text = "\n".join(A) + "\n"
    trace = rep.path_audit(text)
    text += (f"\n**报告全文的绝对路径痕迹扫描**（`report.path_audit`，口径与各判据脚本"
             f"自扫那一道相同）= {'**命中：' + trace + '（判 FAIL）**' if trace else '干净'}\n")
    rep.flush(ROOT / EVIDENCE, text)
    print(f"写入：{EVIDENCE}")
    ok = (not bad) and all(p for _m, p, _r in results) and not trace and not touch_bad
    print(f"RESULT: {'PASS' if ok else 'FAIL'}"
          + (f"（还原异常：{touch_bad + bad}）" if not ok else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
