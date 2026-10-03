#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 `tests/skills/figure-choose/pointer-verify.txt`（Task 7 的逐字证据件）。

用法：  python tests/skills/figure-choose/gen-pointer-verify.py

## 为什么要落盘

与 `gen-house-style-verify.py` / `gen-chart-types-verify.py` / `gen-skill-verify.py` 同一惯例：
证据件要能被**复核员自己重跑出来**，而不是只能读我贴的那几行。落盘的生成器 = 把"哪些命令、
以什么顺序、输出怎么截"这件事本身也变成可复跑的。

## 纪律

- **`write_bytes` 落盘**（Windows 上 `write_text` 会把 LF 写成 CRLF，而证据件恒 LF）；
- **不写绝对路径**（全程用 `Path(__file__)` 推仓根；命令一律用仓内相对路径）；
- 所有子进程命令的 `cwd` = **仓根**；
- §4 的读数**由本生成器当场算**（不经 shell）—— 手敲的带引号命令会被再切一次、**exit=2、
  什么都没证**（Task 3 §5 的教训）。

## 五节（+§5 自证）

§0 blob 自证（含五份假 skill fixture 自己的 blob）· §1 真仓跑一次（**0 个绘图家族 ⇒ 无对象**，
末行必须披露）· §2 假 skill 目录跑一次（**必须红**，且两条规则各打各的）· §3 坏目录两分支
（不存在 / 目录在但没有 `*/SKILL.md`）· §4 变异驱动器（一条命令跑全部，含 `M43`–`M46`）·
§5 生成器当场算的几组读数（**判据复用自证**：`K2`/`K3` 来自 `check-house-style.py`，本器零重写）·
§6 自证。
"""
import importlib.util
import inspect
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # 仓根（本文件在 tests/skills/figure-choose/）
SKILLS_ROOT = ROOT / ".claude/skills"
SKILL = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"   # §5b 现算「边界段点名的家族载体」
CHK = HERE / "check-spec-pointers.py"
MUT = HERE / "mutate-figure-style.py"
GEN = HERE / "gen-pointer-verify.py"
FAKE = HERE / "fixtures/fake-skills"
OK, NOPOINTER, RESTATE = "mcm-plot-ok", "mcm-plot-nopointer", "mcm-plot-restate"
# 家族正则 `FAMILY_RE` 的另外两条备选（复审 Minor-3）：在射程内、各缺指针 ⇒ 逐条压住一条备选
TABLE, SCHEMATIC = "mcm-table", "mcm-schematic"
OUT = HERE / "pointer-verify.txt"
# ★ 家族正则**不在这里手写**（终审 Important-2）：`FAMILY_RE` 的唯一权威在 `check-spec-pointers.py`。
# 本器原先抄了同一条字面量，而 §5b 标题却写"现算，不是抄它的输出" —— 正是本模块招牌毛病
# （"声明比事实大"）。§5a 已把 `k3_reference()` 改成 import（那一次改动该带上的邻行就是这里）：
# 现于 §5b 处 `load(CHK)` 取 `mod.FAMILY_RE`，检查器正则一改它即跟。
FILES = [CHK, MUT, GEN, FAKE / OK / "SKILL.md", FAKE / NOPOINTER / "SKILL.md",
         FAKE / RESTATE / "SKILL.md", FAKE / TABLE / "SKILL.md", FAKE / SCHEMATIC / "SKILL.md"]

HEADER = """Task 7 证据 · 引用完整性检查器（check-spec-pointers.py）+ 假 skill 变异 M43–M46
生成者：Task 7 实施者（2026-09-29）· 写入用 write_bytes ⇒ 本文件恒 LF · 逐字输出
本文件由 `python tests/skills/figure-choose/gen-pointer-verify.py` 整份重生成；命令 cwd = 仓根。
收工时的 `git status --short` 为空见报告（本文件生成于入库之前）。

读法提示（五处最容易看错的地方）：
  1. **判据一条都不在 `check-spec-pointers.py` 里**：`K2`（指针）/ `K3`（不复述规范数值）**import 复用**
     自 `check-house-style.py`（`_load()` 惯用法），本器只把它们从「`--skill <单个文件>`」扩成
     「**对一族 skill 的全扫**」。§5a 逐字印出这两条判据的**来源文件** —— 抄件会随检查器漂移，
     本仓明令"绝不抄实现"（`house-metrics.py` 头部"三支仪器"）。
  2. **射程 = 绘图家族**（`mcm-plot-*` / `mcm-table` / `mcm-schematic`），**不是"任何 skill"**：
     `K3` 的禁止串只从 `house-style.md` 现取，它假设被验文本是那份规范的**消费者**；把别人的
     `§` 章节引用当规范数值是**口径偶合**，不是重述（实测原写法会在 5 份里的 4 份上假红）。
     ★ **不许用"排除 `§` 前缀"打补丁** —— 那等于给真正的重述开一个藏身处（`§0.951` 即转绿）。
  3. **`--skills-dir` 是这门检查器唯一的变异入口**：真仓当前 **0 个**绘图家族 skill ⇒ 只跑真仓，
     逐份判据**一次都不执行**（§1 的"无对象"就是这件事）⇒ "它会红"若不指到假 skill 上，
     就只是自称。§2/§3 与 §4 的 `M43`–`M46` 全在做这件事。
  4. **"0 个对象"判绿还是判红**：锚在**扫到的 skill 总数**，不锚在家族数 ——
     扫到 0 个 skill ⇒ **FAIL**（目录坏 / 空）；扫到 N ≥ 1 而家族 0 个 ⇒ **PASS + 末行显式披露**。
     照 `_k6` 那条先例（"一个绘图 skill 都不点名 = 红"）搬过来会让本器在真仓**恒红**，
     那正是本任务要防的"恒真"的**镜像**。
  5. **假 skill 的目录名带家族前缀**（`mcm-plot-ok` / `mcm-plot-nopointer` / `mcm-plot-restate`）：
     任务书原文给的是 `fake-ok` / `fake-nopointer` / `fake-restate`，但规则①②的射程是"名字匹配
     绘图家族" ⇒ 叫 `fake-*` 的样本**根本不在射程内**，那样 `M43` 不红、`M44` 也证不到
     "家族 ≥1 且全绿"这条路径。三条**角色**（带指针 / 缺指针 / 重述数值）照原样，只加家族前缀。
  6. **`mcm-table` / `mcm-schematic` 两份是后来补的**（复审 Minor-3）：`FAMILY_RE` 有**三条**
     备选，而 `mcm-plot-*` 那三份只压得住第一条 ⇒ 后两条从正则里删掉也不会红（"声明了但没被
     任何变异证明"的判据腿）。修法**不是**放一份干净的同名样例 —— 那样删掉备选它只是**掉出射程**，
     `M43` 的交叉断言一字不变 ⇒ 照样 RED-OK。故这两份**在射程内且脏**（各缺指针）⇒ `M43` 逐条
     点名 `K2@mcm-table` / `K2@mcm-schematic` ⇒ 删掉任一条备选，对应那条预期红当即消失。
     它们**只**为证这条腿，不带别的角色。
"""


def rel(p):
    return pathlib.Path(p).relative_to(ROOT).as_posix()


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, (p.stdout + p.stderr).rstrip("\n")


def sha(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True).stdout.strip()


def load(path, name):
    """与检查器同一惯用法（本生成器也**只 import、不抄**它的判据，只为 §5 取来源文件）。"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


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


def main():
    ev = Ev()
    for line in HEADER.splitlines():
        ev(line)
    ev()

    ev.banner("§0  blob 自证（git hash-object：被验对象就是即将入库的那几个文件）")
    for f in FILES:
        ev(f"{sha(f)}  {rel(f)}")
    ev()

    ev.banner(f"§1  真仓跑一次（**0 个绘图家族 ⇒ 无对象**；末行必须披露）：python {rel(CHK)}")
    ev.cmd([sys.executable, rel(CHK)], "python " + rel(CHK))

    ev.banner(f"§2  假 skill 目录跑一次（**必须红**：缺指针由 `K2` 点名、重述数值由 `K3` 点名）："
              f"python {rel(CHK)} --skills-dir {rel(FAKE)}")
    ev.cmd([sys.executable, rel(CHK), "--skills-dir", rel(FAKE)],
           "python " + rel(CHK) + " --skills-dir " + rel(FAKE))

    ev.banner("§3  坏目录的**两个分支**都必须红（fail-closed）")
    ev("分支 a：目录**不存在**")
    ev.cmd([sys.executable, rel(CHK), "--skills-dir", rel(FAKE) + "-does-not-exist"],
           "python " + rel(CHK) + " --skills-dir " + rel(FAKE) + "-does-not-exist")
    ev("分支 b：目录**存在**但一个 `*/SKILL.md` 都没有 —— 用 `fixtures/` 本身"
       "（它下面只有 `fake-skills/<家族名>/SKILL.md` 这种**孙辈**，没有 `*/SKILL.md` 这种子辈）。")
    ev("    复核员可自己数一遍（本生成器§5c 也会当场印出来）。注：驱动器 `M46` 用的是**临时空目录**"
       "（对 fixture 目录将来新增子目录免疫），两处证的是同一条分支。")
    ev.cmd([sys.executable, rel(CHK), "--skills-dir", rel(HERE / "fixtures")],
           "python " + rel(CHK) + " --skills-dir " + rel(HERE / "fixtures"))

    ev.banner(f"§4  变异驱动器（一条命令跑全部，含 `M43`–`M46`）：python {rel(MUT)}")
    ev.cmd([sys.executable, rel(MUT)], "python " + rel(MUT))

    # ---------------- §5
    ev.banner("§5  生成器当场算的几组读数（**不经 shell** ⇒ 没有引号可切）")
    hs = load((HERE / "check-house-style.py").resolve(), "check_house_style")
    src = CHK.read_bytes().decode("utf-8")
    doc_text = hs.DOC.read_bytes().decode("utf-8")
    # 三族参照物**import 复用**检查器的 `k3_reference()`（M3-T1 起不再抄一条正则 —— 抄件会漂移）
    dec_all, up_all, lo_all = hs.k3_reference(doc_text)

    ev("§5a  **判据复用自证**（本器零重写）")
    for fn in (hs._k2, hs._k3):
        ev(f"     `{fn.__name__}` 的来源文件：{rel(inspect.getsourcefile(fn))}")
    self_defs = [n for n in ('_k2', '_k3') if re.search(rf'^def {n}', src, re.M)]
    ev(f"     本器自己定义的 `_k2`/`_k3`：{self_defs or '**零个**'}"
       f"（有的话就是抄件 ⇒ 会随检查器漂移）")
    # ★ 硬化（2026-10-03 批量清 T7-4）：原先只是**披露**这个读数，非零也不红 ⇒ 改成 raise（fail-closed）。
    assert not self_defs, f"本器自己定义了 {self_defs} ⇒ 是抄件，判据复用自证不成立"
    ev(f"     本器点名的兄弟模块：`check-house-style.py`（全文 {src.count('check-house-style')} 处）")
    ev(f"     本器全文的 `re.findall` 调用：{src.count('re.findall')} 处"
       f"（0 处 ⇒ 它没有自己抽一份禁止串表；唯一用 `re` 的地方是家族名匹配）")
    ev()

    ev("§5b  家族判定与普查（**import 检查器取同一条正则**；**现算**，不是抄它的输出）")
    sp = load(CHK.resolve(), "check_spec_pointers")   # 家族正则的**唯一权威** = 检查器模块
    family_re = sp.FAMILY_RE                           # 取**对象本身**（不是抄 pattern 字面量 ⇒ 不漂移）
    # 边界段点名的家族载体**现算**（不写死个数 —— SKILL.md 的边界段随家族演进变，
    # 写死"三个"会在 `mcm-schematic` 之类落地那刻变假；同 §5b 标题"现算，不是抄它的输出"）。
    # FAMILY_RE is `^(?:...)$` (anchored per name, no MULTILINE) ⇒ match token-by-token,
    # NOT findall over the whole file (that yields 0).
    _toks = set(re.findall(r"mcm-[a-z-]+", SKILL.read_text(encoding="utf-8")))
    named = sorted(n for n in _toks if family_re.match(n))
    ev(f"     正则：`{family_re.pattern}`（**现取**自 {rel(CHK)}：改检查器那条它即跟；"
       f"对照 `mcm-figure-choose/SKILL.md` 边界段点名的家族载体 {len(named)} 个："
       f"{'、'.join(named)}）")
    for root, label in ((SKILLS_ROOT, ".claude/skills（默认）"), (FAKE, "fixtures/fake-skills")):
        rows = [(p.parent.name, bool(family_re.match(p.parent.name)))
                for p in sorted(root.glob("*/SKILL.md"))]
        n_fam = sum(1 for _n, f in rows if f)
        ev(f"     {label}：扫到 {len(rows)} 个 skill · 绘图家族 {n_fam} 个")
        for n, f in rows:
            ev(f"       {'家族  ' if f else '非家族'}  {n}")
    ev()

    ev("§5c  `fixtures/` 下为什么没有子辈 `*/SKILL.md`（§3 分支 b 的依据）")
    fx = HERE / "fixtures"
    ev(f"     `fixtures/*/SKILL.md` = "
       f"{[rel(p) for p in sorted(fx.glob('*/SKILL.md'))] or '**一个都没有**'}")
    ev(f"     `fixtures/*/` 的子目录 = "
       f"{[p.name for p in sorted(fx.iterdir()) if p.is_dir()] or '无'}")
    ev()

    ev("§5d  五份假 skill 各自的形态（**逐字**印出它们的关键读数，别让复核员只能信 M43 的结论）")
    for name, want in ((OK, "含指针、无数值 ⇒ `K2`/`K3` 都该绿"),
                       (NOPOINTER, "缺指针 ⇒ `K2` 该红（`K3` 该绿）"),
                       (RESTATE, "重述数值 ⇒ `K3` 该红（`K2` 该绿）"),
                       (TABLE, "家族正则备选②：在射程内、缺指针 ⇒ `K2` 该红"
                               "（删掉 `|mcm-table` 它就掉出射程 ⇒ M43 变 RED-BAD）"),
                       (SCHEMATIC, "家族正则备选③：在射程内、缺指针 ⇒ `K2` 该红"
                                   "（删掉 `|mcm-schematic` 同上）")):
        txt = (FAKE / name / "SKILL.md").read_bytes().decode("utf-8")
        ptr = txt.count(hs.SK_POINTER)
        hits = hs.k3_main_hits(doc_text, txt)[0]
        ev(f"     {name}（{want}）：指针 `{hs.SK_POINTER}` 出现 {ptr} 处 · 命中的现取禁止串 "
           f"{hits or '无'}（参照物：小数 {len(dec_all)} 条 + 阈值值池 上界 {sorted(up_all)} / "
           f"下界 {sorted(lo_all)}，现取）· 行数 {len(txt.splitlines())}")
    ev()

    ev("§5e  口径边界（**写实**：本器与这两条判据都判不了的）")
    ev("     · `K2`/`K3` 的**口径本身**（判得对不对）不在这里验 —— 那一侧由 `check-house-style.py` "
       "的 `M29`–`M41` 与 `M47`–`M53` 守；本器只验它们**在一族 skill 上真的会被触发**、"
       "且不恒真/不恒红。")
    ev("     · `K3` 的机械射程只到「小数 / 六个阈值标记（`≤n` · `≥n` · `上限 n` · `下限 n` · "
       "`不超过 n` · `<n 词`，**同方向内可互换**）/ 中文数词 + 规范单位词 / "
       "≥4 的规范整数值的中文写法」；1–3 的中文写法、百位以上、"
       "**无标记裸整数（`主色 4 个`）**、以及「这句话是不是在复述规范」本身**都不在射程内**"
       "（判断层的事；裸整数那条由驱动器 `M50` 常驻对照守住）。")
    ev()

    def want_of(shown):
        return 1 if "--skills-dir" in shown else 0      # §1/§4 = 0；§2/§3 两分支 = 1
    bad = [(c, rc) for c, rc in ev.log if rc != want_of(c)]
    ev.banner("§6  本节自证：上面每条命令的退出码都要**符合预期**"
              "（§1 真仓 = 0；§2/§3 两分支 = 1；§4 驱动器 = 0）")
    for shown, rc in ev.log:
        w = want_of(shown)
        ev(f"     [{'OK ' if rc == w else 'BAD'}] exit={rc}（应 {w}）  {shown}")
    ev()

    blob = ("\n".join(ev.lines) + "\n").encode("utf-8")
    OUT.write_bytes(blob)                                    # write_bytes ⇒ 恒 LF
    print(f"wrote {rel(OUT)}  bytes={len(blob)}  lines={blob.count(10)}  "
          f"命令 {len(ev.log)} 条 · 退出码不符预期 {len(bad)} 条")
    for c, rc in bad:
        print(f"  exit={rc}  {c}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
