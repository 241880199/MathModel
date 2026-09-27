#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 `tests/skills/figure-choose/chart-types-verify.txt`（Task 4 的逐字证据件）。

用法：  python tests/skills/figure-choose/gen-chart-types-verify.py

## 为什么要落盘

与 `gen-house-style-verify.py` 同一惯例：证据件要能被**复核员自己重跑出来**，而不是只能读我贴的那几行。
落盘的生成器 = 把"哪些命令、以什么顺序、输出怎么截"这件事本身也变成可复跑的。

## 纪律

- **`write_bytes` 落盘**（Windows 上 `write_text` 会把 LF 写成 CRLF，而证据件恒 LF）；
- **不写绝对路径**（全程用 `Path(__file__)` 推仓根；命令一律用仓内相对路径）；
- 所有子进程命令的 `cwd` = **仓根**（与文档里"可直接粘进 bash"的口径一致）；
- §4 的三组读数**由本生成器当场算**（不经 shell）—— 理由与 Task 3 §5 同：
  手敲的带引号命令会被再切一次，**exit=2、什么都没证**。这里按参数/表达式直接算，
  数就是现场数，没有引号可切。

## 五节

§0 blob 自证 · §1 全量守卫（含结构守卫 S1–S5）· §2 只跑结构守卫 ·
§3 变异驱动器（一条命令跑全部；含 M22–M28 与读数条探针 R1）· §4 生成器当场算的三组读数 · §5 自证。
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # 仓根（本文件在 tests/skills/figure-choose/）
REF = ROOT / ".claude/skills/mcm-figure-choose/references"
OUT = HERE / "chart-types-verify.txt"
CHK = HERE / "check-house-style.py"
MUT = HERE / "mutate-figure-style.py"
CT = REF / "chart-types.md"
FILES = [CT, CHK, MUT, HERE / "gen-chart-types-verify.py"]

HEADER = """Task 4 证据 · chart-types.md（九个数据关系入口 + 题型索引 + radar 低频）+ 结构守卫 S1–S5
生成者：Task 4 实施者（2026-09-27）· 写入用 write_bytes ⇒ 本文件恒 LF · 逐字输出
本文件由 `python tests/skills/figure-choose/gen-chart-types-verify.py` 整份重生成；命令 cwd = 仓根。
收工时的 `git status --short` 为空见报告（本文件生成于入库之前）。

读法提示（四处最容易看错的地方）：
  1. **`S4` 不是判据**：它出现在 §1/§2 里的时候前缀是 `READ` 而不是 `PASS`/`FAIL`——
     它只印"定义行 / 不同名 / 重名"的计数，**不进判词**（**唯一例外**：`chart-types.md` **读不出**时
     它随其余结构守卫一起记红 —— 见检查器模块头第 5 条）。它没有"会红"可证，
     故由 §3 的探针 `R1` 证另一件事：**该动的时候动（读数会随文档变）、该判的时候不判（rc 恒 0）**。
  2. **`S5` 抽不到任何小数也红**（fail-closed）：§3 的 `M26` 把两个小数都写成中文数字，
     证明"把数全删光"不是转绿路径。
  3. **`M24` 的 NOTE 是现算的**：任务书给的正则（**全文**扫 `radar` × `低频`）在那种改法下
     **不会红**（别的入口顺带提到 radar 时也标了低频）⇒ `S3` 被收紧成**只看 radar 的那条定义行**。
  4. **`S5` 判的是"归到哪个 `H<n>`"**（修复轮 N-2 收紧）：每个小数必须**归到它同行的 `H<n>` 引用**、
     且**值 ∈ 那个 `H<n>` 条目里的数**。旧写法只查"值 ∈ house-style ∪ provenance 的全局池"
     （123 个数）⇒ 池内的数写哪儿都绿（`M27` 的 `1.20`、`M28` 的 `0.5` 都会漏）。§4b 印归属。
"""


def rel(p):
    return pathlib.Path(p).relative_to(ROOT).as_posix()


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, (p.stdout + p.stderr).rstrip("\n")


def sha(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True).stdout.strip()


class Ev:
    def __init__(self):
        self.lines, self.log = [], []

    def __call__(self, s=""):
        self.lines.append(s)

    def banner(self, t):
        self("=" * 78)
        self(t)
        self("=" * 78)

    def cmd(self, argv, shown=None):
        shown = shown or " ".join(argv)
        self(f"$ {shown}")
        rc, out = run(argv)
        if out:
            self(out)
        self(f"[exit={rc}]")
        self.log.append((shown, rc))
        self()
        return rc


# ---------------------------------------------------------------- §4 的三组读数
MUT_TARGETS = [
    ("M22", "### 入口 9 · 不确定性"),
    ("M23", "**备选**：`dot plot`"),
    ("M24", "连成多边形 —— **低频**：获奖样本里属罕见选择"),
    ("M25", "**9.2%**"),
    ("M26", "**0.0%**"),
    ("M27", "机械守卫 `S5` 管的是**抄过来之后有没有漂**"),
    ("M28", "**9.2%**"),
]
# `S5` 的判据是"小数**归到同行 `H<n>`** 且 **∈ 该条目的数**"（修复轮 N-2 收紧）。
# 这里对照三个数三种下场（`M27`/`M28` 采用前两个）：
#   1.20 —— 旧全局池里**有**它（H1 的上限）⇒ 旧写法漏；同行无 `H<n>` ⇒ 新写法红（M27）；
#   0.5  —— 旧全局池里**有**它（H4 的地板）、语义完全不同 ⇒ 旧写法漏；∉ H7 ⇒ 新写法红（M28）；
#   9.3  —— 旧全局池里**也没有**它 ⇒ 两种写法都红（M25 用这条证"数漂了"）。
S5_CANDIDATES = [("1.20", None), ("0.5", "7"), ("9.3", "7")]


def h_nums(house_text, hid):
    """`house-style.md` 的 `### H<hid>.` 条目里的小数字面量（与检查器 `_h_entries` 同口径，现取）。"""
    m = re.search(rf"^### H{hid}\..*?$(.*?)(?=^### H\d+\.|\Z)", house_text, re.M | re.S)
    return set(re.findall(r"\d+\.\d+", m.group(1))) if m else set()


def main():
    ev = Ev()
    for line in HEADER.splitlines():
        ev(line)
    ev()

    ev.banner("§0  blob 自证（git hash-object：被验对象就是即将入库的那几个文件）")
    for f in FILES:
        ev(f"{sha(f)}  {rel(f)}")
    ev()

    ev.banner("§1  全量守卫（规范数守卫 + CENSUS + 结构守卫 S1–S5）：python tests/skills/figure-choose/check-house-style.py")
    ev.cmd([sys.executable, rel(CHK)], "python " + rel(CHK))

    ev.banner("§2  只跑结构守卫（S4 是读数条 ⇒ 前缀是 READ）："
              "python tests/skills/figure-choose/check-house-style.py --only S1 S2 S3 S4 S5")
    ev.cmd([sys.executable, rel(CHK), "--only", "S1", "S2", "S3", "S4", "S5"],
           "python " + rel(CHK) + " --only S1 S2 S3 S4 S5")

    ev.banner("§3  变异驱动器（一条命令跑全部）：python tests/skills/figure-choose/mutate-figure-style.py")
    ev.cmd([sys.executable, rel(MUT)], "python " + rel(MUT))

    # ---------------- §4
    ev.banner("§4  生成器当场算的三组读数（**不经 shell** ⇒ 没有引号可切）")
    ev("说明（与 Task 3 §5 同一条教训）：手敲的带引号命令会被再切一次、exit=2、什么都没证。")
    ev("下面三组数由本生成器**直接算**并打印，命令就是上面那一行 `python …/gen-chart-types-verify.py`。")
    ev()

    ct_text = CT.read_bytes().decode("utf-8")
    hs_text = (REF / "house-style.md").read_bytes().decode("utf-8")
    # 旧写法（修复前）的"同值池" = house-style ∪ provenance 的小数字面量全集 —— 只为对照印出来
    pool = set(re.findall(r"\d+\.\d+", hs_text)) | \
        set(re.findall(r"\d+\.\d+", (REF / "provenance.md").read_bytes().decode("utf-8")))

    ev("§4a  七个变异的目标串在**出货件**里各命中几次（必须恰为 1 —— 否则驱动器自己报错）")
    for mid, lit in MUT_TARGETS:
        ev(f"     {mid:<4} 命中 {ct_text.count(lit)} 次   {lit[:52]}")
    ev()

    ev("§4b  S5 的**归属**（修复轮 N-2 收紧）：每个小数归到**同行 `H<n>` 引用**、值 ∈ **该条目**的数")
    ev("     旧写法只查『值 ∈ house-style ∪ provenance 的全局池』⇒ 池内的数写哪儿都绿（弱化）。")
    for lineno, line in enumerate(ct_text.splitlines(), 1):
        refs = list(re.finditer(r"H(\d+)", line))
        for m in re.finditer(r"\d+\.\d+", line):
            num = m.group(0)
            before = [r for r in refs if r.start() < m.start()]
            ref = before[-1] if before else (refs[0] if refs else None)
            if ref is None:
                ev(f"     行 {lineno:<4} `{num}`：同行**没有** `H<n>` 引用 ⇒ 新写法红（fail-closed）")
                continue
            hid = ref.group(1)
            ent = h_nums(hs_text, hid)
            ev(f"     行 {lineno:<4} `{num}` → H{hid}：∈ H{hid} 条目的数 {num in ent}"
               f"（该条目的小数 {sorted(ent)}）· 在旧全局池（{len(pool)} 个）里 {num in pool}")
    ev("     三个备选改法（`M27`/`M28` 采用前两个）：")
    for cand, hid in S5_CANDIDATES:
        ent = h_nums(hs_text, hid) if hid else set()
        where = "归到 H7 时 ∈ H7 的数" if hid else "无所属（同行无 `H<n>`）⇒ 归不进任何条目"
        ev(f"     {cand:<5} 旧全局池里: {cand in pool} · {where}: {cand in ent}"
           f" ⇒ 新写法{'绿' if cand in ent else '**红**'}")
    ev()

    ev("§4c  九个入口标题 —— **入口名是契约**：那九个名字**硬编码在检查器 `ENTRIES`**、"
       "**不从文档现取**")
    ev("     （现取就等于『改文档即改期望值』，`S1` 会退化成恒真）；这里把**文档里的标题印出来供人核对**。")
    heads = re.findall(r"^#{2,}\s*入口\s*\d+\s*·\s*(\S+)\s*$", ct_text, re.M)
    ev(f"     标题 {len(heads)} 个：{' / '.join(heads)}")
    ev()

    # ---------------- §5
    bad = [(c, rc) for c, rc in ev.log if rc != 0]
    ev.banner("§5  本节自证：上面每条命令都要 exit=0")
    ev(f"§0-§4 共跑 {len(ev.log)} 条；非零退出 {len(bad)} 条"
       + ("" if not bad else "：" + "; ".join(f"{c} → exit={rc}" for c, rc in bad)))
    ev()

    blob = ("\n".join(ev.lines) + "\n").encode("utf-8")
    OUT.write_bytes(blob)                                    # write_bytes ⇒ 恒 LF
    print(f"wrote {rel(OUT)}  bytes={len(blob)}  lines={blob.count(10)}  "
          f"命令 {len(ev.log)} 条 · 非零退出 {len(bad)} 条")
    if bad:
        for c, rc in bad:
            print(f"  exit={rc}  {c}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
