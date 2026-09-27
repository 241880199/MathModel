"""入库探针：本轮新增的两个块（`INDEX.md` 的「覆盖边界」/ `PROVENANCE.md` 的
「不能推出的结论」）**有没有判据覆盖**——**可重跑**，与当前 HEAD 的内容无关。

**它为什么存在**（Task M2-hygiene 复审 Important-1）：原先的证据是一份 gitignored 的
`build/m2_coverage_gap.py`，它用 `git show HEAD:<path>` 取「**没有那两个块**的字节」。
那份探针跑的时候 HEAD 里确实还没有那两个块（「拿掉块」成立），**今天 HEAD 已含块** ⇒
重跑变成**空操作**，而它打印的两行「块确实被拿掉了」是**写死的文字**、退出码仍是 0
⇒ 谁翻到它重跑，都会得出**与已登记结论相反**的结论（真值：`M-1` 判红）。本脚本把
「没有块的字节」钉死成两个 **blob sha**、**从 git 对象库取**（`git cat-file blob`），
不依赖任何时刻的 HEAD ⇒ 任何时候重跑问的都是同一个问题。（那份雷已按修复轮要求删除。）

**做法**：把两份入库产物换成**去掉那两个块**的字节 → 跑三份判据脚本的 `--limit 3` 跑 →
**逐字打出**每份的退出码、`RESULT:` 行与失败行 → `finally` 里按**原始字节**还回去 →
收尾断言 `git hash-object` 回到跑前值，**还原结论并进退出码**。

**判据**（全过才退 0）：

  ① **前提成立**：两个钉死 blob 在对象库里取得到；且**逐行**看「当前字节 == 钉死字节 +
     若干**插入**行」（插入行非空）——即「去掉的确实就是那些块」，**不作口头声明**，
     把被去掉的那些行连同行号逐字打出来；
  ② **阶段 1**（只去掉 `INDEX.md` 的「覆盖边界」块）：三份判据**全绿**
     （⇒ 这个块**没有任何判据覆盖**）；
  ③ **阶段 2**（只去掉 `PROVENANCE.md` 的「不能推出的结论」块）：`verify_map` 非 0 且
     逐字含 `M-1=FAIL`；`verify_ids` / `verify_types` 绿；
  ④ **施加与还原**：两阶段替换后的 blob 都 == 对应的钉死值（替换真的落上去了）；
     跑完两份产物 `git hash-object` == 跑前值（**逐字节还原成功**）。

**三份判据在这两个阶段里的期望强度不一样，别读成一样的**：

  * `verify_ids --limit 3`：产物落点是 `tests/papers/reports-limited/ids-products/`
    （`verify_ids.py` 的 `prod_dir`），**不读入库产物** ⇒ 它绿是**结构性必然**；
  * `verify_types --limit 3`：`--limit` 只缩 T2 的样本口径，**根本不碰入库产物**
    ⇒ 它绿同样是**结构性必然**；
  * `verify_map --limit 3`：**仍读入库产物**（M-1 逐行比 `INDEX.md`、逐字节比
    `PROVENANCE.md`；`--limit` 只改报告落点并跳过要重跑 43 份原件的 M-1-b）
    ⇒ **只有它**可能对这次替换有反应。

  故「三份全绿」这句话里，**只有 `verify_map` 那一格是实验发现**，另两格不是。
  （复审 Minor-2：别把结构性必然写成实验发现。）

**将来若有人给 `INDEX.md` 那个块加上判据**，阶段 1 就不再全绿 ⇒ 本探针会判非 0。
那时要更新的是**登记结论**（缺口已补），不是这条断言——它报告的正是「结论变了」。

**只读窗口**：本探针不改任何代码文件、不碰放行证据与入库报告（三份判据在 `--limit`
下都只写 `tests/papers/reports-limited/`，那是不入库目录）。对两份产物的写入在 `finally`
里**按原始字节无条件还原**，还原结果**并进退出码**（没还原成功就非 0）。

运行：`PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/coverage-gap-probe.py`
（stdout 即记录；本脚本不写自己的输出文件。）
"""
import difflib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]      # tests/papers/recon/ → 仓库根

# 「**没有那两个块**的字节」——钉死的 blob sha，**从 git 对象库取**，与当前 HEAD 无关。
# 两个值来自 `tests/papers/recon/map-recon.txt` §0 与本轮报告的改前登记（同一时刻实测）：
# 它们 = 本轮「加块」之前的入库 blob。
PINNED = {
    "corpus/papers/INDEX.md": "0d8d4970efb245ab732a4dc7c21e7838ee8d675d",
    "corpus/papers/PROVENANCE.md": "85484c4d233a6183031a3827510e09fde306e0db",
}
STAGES = [
    "tests/papers/verify_ids.py",
    "tests/papers/verify_map.py",
    "tests/papers/verify_types.py",
]
LIMIT = "3"
# 阶段 2 必须逐字出现的那条 FAIL 标记（`verify_map` 的 M-1）。
EXPECT_STAGE2 = "M-1=FAIL"
CACHES = ("tools/papers/__pycache__", "tools/__pycache__",
          "tests/papers/__pycache__", "tests/papers/recon/__pycache__")


def env0() -> dict:
    e = dict(os.environ)
    # **禁写 .pyc**（与下面 purge 配对；本项目硬纪律）。
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    return e


def purge() -> list:
    gone = []
    for d in CACHES:
        q = ROOT / d
        if q.is_dir():
            shutil.rmtree(q, ignore_errors=True)
            gone.append(d)
    return gone


def blob(rel: str) -> str:
    """`git hash-object` 的实测值（**会应用** `-text` 等过滤器口径）。"""
    r = subprocess.run(["git", "hash-object", "--", rel], cwd=str(ROOT),
                       capture_output=True, env=env0())
    if r.returncode != 0:
        raise RuntimeError(f"`git hash-object` 非零退出（{r.returncode}）：{rel}")
    return r.stdout.decode("utf-8", "replace").strip()


def pinned_bytes(rel: str) -> bytes:
    """从 **git 对象库**取钉死的字节；取不到就整轮作废（不静默退化）。"""
    r = subprocess.run(["git", "cat-file", "blob", PINNED[rel]], cwd=str(ROOT),
                       capture_output=True, env=env0())
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(f"钉死 blob 取不到：{rel} = {PINNED[rel]}（rc={r.returncode}）")
    return r.stdout


def removed_lines(old: bytes, cur: bytes) -> list:
    """逐行看「cur == old + 若干**插入**行」，返回被插入的行（1-based 行号 + 文本）。

    返回空列表 = 前提不成立（不是纯插入 ⇒ 说明「去掉的」不止那些块）。
    """
    a = old.decode("utf-8").splitlines(keepends=True)
    b = cur.decode("utf-8").splitlines(keepends=True)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    ops = [t for t in sm.get_opcodes() if t[0] != "equal"]
    if not ops or any(t[0] != "insert" for t in ops):
        return []
    out = []
    for _tag, _i1, _i2, j1, j2 in ops:
        for k in range(j1, j2):
            out.append((k + 1, b[k]))
    return out


def run_stage(tag: str) -> dict:
    """在当前工作树状态下跑三份判据的限样本跑；返回每份的 (EXIT, RESULT 行, 失败行)。"""
    print(f"  ---- {tag} ----")
    res = {}
    for st in STAGES:
        r = subprocess.run([sys.executable, st, "--limit", LIMIT], cwd=str(ROOT),
                           capture_output=True, timeout=3600, env=env0())
        out = (r.stdout + r.stderr).decode("utf-8", "replace").replace("\r\n", "\n")
        reslines = [ln for ln in out.splitlines() if ln.startswith("RESULT:")]
        fails = [ln for ln in out.splitlines()
                 if "=FAIL" in ln and not ln.startswith(" ")]
        res[st] = (r.returncode, reslines[-1] if reslines else "(无 RESULT 行)", fails)
        print(f"    {st:<34} EXIT={r.returncode}  "
              f"{res[st][1] if reslines else '(无 RESULT 行)'}")
        print(f"      失败行（逐字）= {fails or '无'}")
    return res


def green(res: dict, st: str) -> bool:
    rc, resline, fails = res[st]
    return rc == 0 and resline.startswith("RESULT: PASS") and not fails


def main() -> int:
    print("[探针] 清 __pycache__：", purge() or "（无）")
    orig = {rel: (ROOT / rel).read_bytes() for rel in PINNED}
    pre = {rel: blob(rel) for rel in PINNED}
    print("=== 逐份：钉死 blob / 当前 blob / 前提 ===")
    for rel in PINNED:
        print(f"  {rel}")
        print(f"    钉死 blob（git 对象库）= {PINNED[rel]}")
        print(f"    当前 blob               = {pre[rel]}")
        old = pinned_bytes(rel)
        ins = removed_lines(old, orig[rel])
        if not ins:
            print("    **前提不成立**：当前字节不是「钉死字节 + 纯插入行」"
                  "——去掉的不止那两个块，本探针整轮作废")
            return 1
        print(f"    前提 = 当前 = 钉死 + {len(ins)} 行**纯插入**（逐行如下，"
              f"这些就是被去掉的字节）")
        for ln, txt in ins:
            print(f"      {ln:>4} | {txt.rstrip()}")
    print()

    res1 = res2 = None
    restored = {}
    landed = {}
    try:
        # 阶段 1：只去掉 `INDEX.md` 的「覆盖边界」块
        (ROOT / "corpus/papers/INDEX.md").write_bytes(pinned_bytes("corpus/papers/INDEX.md"))
        b1 = blob("corpus/papers/INDEX.md")
        landed["corpus/papers/INDEX.md"] = (b1 == PINNED["corpus/papers/INDEX.md"])
        print("=== 阶段 1：只去掉 `INDEX.md` 的「覆盖边界」块 ===")
        print(f"  INDEX.md 施加后 blob = {b1}"
              f"（== 钉死的那个 = {landed['corpus/papers/INDEX.md']}；"
              f"与跑前不同 = {b1 != pre['corpus/papers/INDEX.md']}）")
        res1 = run_stage("阶段 1 · 只去掉 INDEX 的块")

        # 阶段 2：先还原 INDEX，再去掉 `PROVENANCE.md` 的「不能推出的结论」块
        (ROOT / "corpus/papers/INDEX.md").write_bytes(orig["corpus/papers/INDEX.md"])
        (ROOT / "corpus/papers/PROVENANCE.md").write_bytes(
            pinned_bytes("corpus/papers/PROVENANCE.md"))
        b2 = blob("corpus/papers/PROVENANCE.md")
        landed["corpus/papers/PROVENANCE.md"] = (b2 == PINNED["corpus/papers/PROVENANCE.md"])
        print("=== 阶段 2：只去掉 `PROVENANCE.md` 的「不能推出的结论」块 ===")
        print(f"  PROVENANCE.md 施加后 blob = {b2}"
              f"（== 钉死的那个 = {landed['corpus/papers/PROVENANCE.md']}；"
              f"与跑前不同 = {b2 != pre['corpus/papers/PROVENANCE.md']}）")
        res2 = run_stage("阶段 2 · 只去掉 PROVENANCE 的块")
    finally:                      # **无论上面怎么炸，都要按原始字节还回去**
        for rel in PINNED:
            (ROOT / rel).write_bytes(orig[rel])
        restored = {rel: blob(rel) == pre[rel] for rel in PINNED}
    print()

    print("=== 还原（同一时刻）===")
    for rel in PINNED:
        print(f"  {rel:<34} {pre[rel]}  还原 = {restored[rel]}")

    # ---- 结论与断言 ----
    green1 = {st: green(res1, st) for st in STAGES}
    green2 = {st: green(res2, st) for st in STAGES}
    map2_red = (not green2["tests/papers/verify_map.py"]
                and EXPECT_STAGE2 in res2["tests/papers/verify_map.py"][2])
    ok = (all(green1.values()) and green2["tests/papers/verify_ids.py"]
          and green2["tests/papers/verify_types.py"] and map2_red
          and all(landed.values()) and all(restored.values()))
    print()
    print("=== 读数（含**强度**说明）===")
    print(f"  阶段 1（去掉 `INDEX.md` 的块）：三份全绿 = {all(green1.values())}"
          f"（逐份 {'/'.join(str(int(green1[st])) for st in STAGES)}）"
          f" ⇒ **这个块没有任何判据覆盖**")
    print(f"  阶段 2（去掉 `PROVENANCE.md` 的块）："
          f"`verify_map` 非 0 且逐字含 `{EXPECT_STAGE2}` = {map2_red}"
          f" ⇒ **这个块有信号**（是「与基准逐字节相等」那一支，不是语义判据）")
    print("  强度：上面三份的绿**不是同一种绿**——`verify_ids --limit` 把产物写到 "
          "`tests/papers/reports-limited/ids-products/`、`verify_types --limit` 只缩 T2 "
          "样本口径，两者**都不读入库产物** ⇒ 它们绿是**结构性必然**；只有 `verify_map "
          "--limit` 仍读入库产物（M-1），故**只有它那一格是实验发现**。")
    print(f"  还原：两份产物都回到跑前 blob = {all(restored.values())}")
    print(f"**探针结论**：全部断言通过 = {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
