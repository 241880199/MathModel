"""`RT-M3` 的**入库**探针：`M-7` 的幻影 stable ID 红路（断言的是**现行真实存在的 id**）。

**它为什么存在**：`RT-M3`（原先）登记的「`M-7` 的幻影 ID 新红路没有变异证据」这条缺口，
**唯一**证据曾是一份 gitignored 的 `build/t6b2a_probe_phantom.py`——按本项目规矩
（「残余一律落库区，放 `.superpowers/` 或 `build/` 等于丢失」）**等于丢失**。本脚本是那份
探针的入库版本（登记见 `tests/papers/recon/map-recon.txt` §13 `RT-M3` 与
`docs/mcm-suite-triage-2026-09-26.md` §4.3）。

**与旧版的关键差别**：旧版第 ④ 条断言 `M-3=FAIL`——而 **2b 把配对判据从 `M-3` 改名成了
`M-13`**（`tests/papers/verify_map.py`：`M-3` 那个编号**不再存在**，见该文件的说明），
于是那条断言**恒为 False**、旧探针**今天自己跑不过**。本版改成断言**红 id 集合**：
非空、且**含 `M-13`**；整份红 id 清单**逐行打进记录**（不在这里抄成会随编辑过期的常量）。

**做法**：只碰 `corpus/papers/MODEL_MAP.md` 的**一行桶指针**（把 `P2025-A-01` 改成
TAGS 一层根本没有的 `P2025-Z-99`），跑 `tests/papers/verify_map.py --limit 3`——
`--limit` 在本脚本里**不缩样本**，只改报告落点为 gitignored 的
`tests/papers/reports-limited/` 并跳过 M-1-b ⇒ **不碰任何放行证据**。

**五条断言**（全过才退 0）：
  ① 退出码非 0（fail-closed 一点不减）；
  ② 红的 id 集合**非空**且**含 `M-13`**；
  ③ `M-7` 那一块里有**具名**说明（逐字含 `配对表里出现了 TAGS 一层没有的稳定 ID` 与幻影 ID）；
  ④ 无 traceback、无「校验过程中抛出异常」兜底文本（幻影 ID 不许把整条判据带崩）；
  ⑤ **还原**：`git hash-object` 回到跑前的值。

**只读窗口**：本探针不改任何代码文件、不碰放行证据；对 `MODEL_MAP.md` 的唯一写入在
`finally` 里**按原始字节无条件还原**，还原结果**并进退出码**（不还原成功就非 0）。
运行：`PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/map-phantom-probe.py`
（stdout 即记录；本脚本不写自己的输出文件）。
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]      # tests/papers/recon/ → 仓库根
MM = ROOT / "corpus" / "papers" / "MODEL_MAP.md"

# 锚点 = 那一行桶指针的**原文**（对不上就整轮作废，不静默跳过）。
ANCHOR = b"- Monte Carlo; P2025-A-01; p1; "
REPL = b"- Monte Carlo; P2025-Z-99; p1; "
PHANTOM = "P2025-Z-99"
NAMED_MSG = "配对表里出现了 TAGS 一层没有的稳定 ID"
# 判据行形态：`M-13=FAIL` / `M-1-b=OK` 一类（**行首硬锚**——别把复述当成判据行）。
RED_ID = re.compile(r"^([A-Z][A-Z0-9-]*)=FAIL$", re.M)

CACHES = ("tools/papers/__pycache__", "tools/__pycache__",
          "tests/papers/__pycache__", "tests/papers/recon/__pycache__")


def env0() -> dict:
    e = dict(os.environ)
    # **禁写 .pyc**（与下面 purge 配对；本项目硬纪律）。
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    return e


def purge() -> list[str]:
    gone = []
    for d in CACHES:
        q = ROOT / d
        if q.is_dir():
            shutil.rmtree(q, ignore_errors=True)
            gone.append(d)
    return gone


def blob(p: Path) -> str:
    """`git hash-object` 的实测值（**会应用** `core.autocrlf` 与 `.gitattributes` 过滤器）。

    口径：判「文件有没有被改」要用**能应用过滤器的工具**，不是裸字节哈希
    （`mcm-suite-todo.md` §D 第 9 条 ⑤）。
    """
    r = subprocess.run(["git", "hash-object", "--", p.relative_to(ROOT).as_posix()],
                       cwd=str(ROOT), capture_output=True, env=env0())
    if r.returncode != 0:
        raise RuntimeError(f"`git hash-object` 非零退出（{r.returncode}）：{p}")
    return r.stdout.decode("utf-8", "replace").strip()


def verdict_block(out: str, name: str) -> str:
    """取 `name` 那条判据的**整块**（`add()` 的格式：`<名>=FAIL` 一行 + 缩进明细若干行）。"""
    lines = out.splitlines()
    i = next((k for k, ln in enumerate(lines) if ln.startswith(f"{name}=")), None)
    if i is None:
        return ""
    block = []
    for ln in lines[i + 1:]:
        if ln and not ln.startswith(" "):
            break
        block.append(ln)
    return "\n".join(block)


def main() -> int:
    print("[探针] 清 __pycache__：", purge() or "（无）")
    orig = MM.read_bytes()
    b_pre = blob(MM)
    print(f"[探针] MODEL_MAP.md 改前 blob = {b_pre}")

    if orig.count(ANCHOR) < 1:
        print(f"[探针] **整轮作废**：锚点没命中（找不到那行桶指针 {ANCHOR!r}）")
        return 1
    if PHANTOM.encode() in orig:
        print(f"[探针] **整轮作废**：幻影 ID {PHANTOM} 竟然已经存在（探针的前提不成立）")
        return 1

    out = ""
    rc = -1
    restored = False
    b_mid = b_post = "<未跑>"
    try:
        MM.write_bytes(orig.replace(ANCHOR, REPL, 1))
        b_mid = blob(MM)
        print(f"[探针] 施加探针后 blob = {b_mid}（必须 != 改前 = {b_mid != b_pre}）")
        purge()
        r = subprocess.run([sys.executable, "tests/papers/verify_map.py", "--limit", "3"],
                           cwd=str(ROOT), capture_output=True, timeout=3600, env=env0())
        rc = r.returncode
        out = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
        # 子进程的流在 Windows 上是 CRLF ⇒ 先归一化，否则行尾硬锚（`^…=FAIL$`）一条都匹配不上。
        out = out.replace("\r\n", "\n")
    finally:
        MM.write_bytes(orig)              # **无条件还原**（哪怕上面抛了）
        b_post = blob(MM)
        restored = (b_post == b_pre)

    red_ids = RED_ID.findall(out)
    block7 = verdict_block(out, "M-7")
    named = (PHANTOM in block7 and NAMED_MSG in block7)
    has_tb = ("Traceback (most recent call last)" in out
              or "校验过程中抛出异常" in out)
    # 旧名 `M-3` 的现状（**记录，不作断言**——将来若真有人把 `M-3` 加回来，这条登记才需要重看）。
    m3_lines = [ln for ln in out.splitlines() if ln.startswith("M-3=")]

    print(f"[探针] 退出码 = {rc}（要求非 0）")
    print(f"[探针] 红的 id 集合（{len(red_ids)} 条）：{' '.join(red_ids) or '（空）'}")
    print(f"[探针] 红 id 非空 = {bool(red_ids)}（要求 True）")
    print(f"[探针] 红 id 含 `M-13` = {'M-13' in red_ids}（要求 True）")
    print(f"[探针] `M-7` 那一块逐字（前 6 行）：")
    for ln in block7.splitlines()[:6]:
        print(f"        {ln}")
    print(f"[探针] M-7 块里有具名说明（幻影 ID + 那句话）= {named}（要求 True）")
    print(f"[探针] 含 traceback / 兜底异常文本 = {has_tb}（要求 False）")
    print(f"[探针] 行首 `M-3=` 的行（记录，非断言）= {m3_lines or '（一行都没有）'}")
    print(f"[探针] 还原后 blob = {b_post}（== 改前 = {restored}）")

    ok = (rc != 0 and bool(red_ids) and "M-13" in red_ids and named
          and not has_tb and restored)
    print(f"[探针] 全部断言通过 = {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
