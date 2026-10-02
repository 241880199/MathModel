#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/table/check-table-style.py` 的**变异驱动器**（计划 Task 2 · 硬要求 4）。

用法：  python tests/skills/table/mutate-table-style.py

## 它做什么

把**正控制样本** `fixtures/good-basic.tex` 的副本逐条改坏（**当场改、当场跑、当场删**），
断言检查器**点名红在那一条判据上**；另设**必须仍绿**的对照（射程边界）。

- 每条变异**只碰临时目录里的副本**（`tempfile.mkdtemp()`，系统临时目录 = ASCII 路径），
  **不碰**仓内任何入库件；收尾逐件 `git hash-object` 自证"受保护件逐字节未变"。
- 期望集**逐条写死**（不是"红了就算数"）：实际红的判据集合必须**恰好等于**该条声明的集合。
  这样"一条变异顺手带红别的判据"或"该红没红"都会被抓出来。
- **判据只能从失败方向证明**（本仓硬规矩）：每个 `C1`–`C8` 至少有一条真红作证；
  **fail-closed 分支**另由 `MUT-FC1`/`MUT-FC2` 真红作证（清单上的声明必须有一条真的红）。
- 合计行形态照 `mutate-figure-style.py`：`MUT: n/m 达预期（合计）`，**合计行不是末行**。

## 覆盖（**不声称穷尽**）

| id | 打的是 | 期望红 |
| :--- | :--- | :--- |
| `MUT-C1` | 表题里放一个未定义控制序列 ⇒ 编不过（`settowidth` 臂不受影响 ⇒ `C4` 仍绿） | `C1` |
| `MUT-C2a` | 删掉 `\\bottomrule` | `C2` |
| `MUT-C2b` | 列说明里塞一个 `|` | `C2` |
| `MUT-C3` | 把 `\\caption` 移到 `tabular` 之下（**未**声明覆盖） | `C3` |
| `MUT-C4` | 表头塞一个超长不可断词 ⇒ 表宽超版心 | `C4` |
| `MUT-C5` | 把一个格子清空 ⇒ 空格子（空格子**同时**是"错形缺失值" ⇒ `C7` 也红） | `C5`,`C7` |
| `MUT-C6` | 同列改一处小数位 ⇒ 同列精度不一致 | `C6` |
| `MUT-C7a` | 非 `S` 列的缺失值由 `--` 改成 `NA`（**能编过** ⇒ 证明 `C7` 不靠 `C1`） | `C7` |
| `MUT-C7b` | `S` 列的 `{--}` 去掉花括号 ⇒ 源码层面非规范形（**连带编不过**） | `C1`,`C7` |
| `MUT-C8` | 删掉一条来源回显注释 ⇒ 漏一格 | `C8` |
| `MUT-C1b` | `\end{tabular}` **之后**的表注里塞未定义控制序列 ⇒ `C1` 真红（证明修好 `C4` 量宽后 `C1` 仍抓得到片段里的真错） | `C1` |
| `MUT-LEAD-a` | **前导 `&` 占位的边界**：把列头行首格清空（其后**不是**跨列分组）⇒ 仍算空格子 | `C5`,`C7` |
| `MUT-FC1` | 列说明塞 `d{2}` ⇒ 列说明**解析失败**（fail-closed）＋ `d` 列型编不过 | `C1`,`C2`,`C5`,`C6`,`C7`,`C8` |
| `MUT-FC2` | 表里再塞一个 `tabular` ⇒ `tabular` **不唯一**（fail-closed；产物照常编过） | `C2`,`C3`,`C5`,`C6`,`C7`,`C8` |
| `CTRL-GREEN-a` | **射程边界对照**：只改表题**措辞** ⇒ 判据**必须仍绿** | （无） |
| `CTRL-GREEN-b` | **覆盖口径对照**：表题移下 + 声明 `% mcm-table-caption: below` ⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-c` | **防假红对照**：`good-multicolumn.tex`（含 `\multicolumn` 的**合规表**）⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-d` | **防假红对照**：`good-multilevel-leading.tex`（**前导 `&`** 的两级表头合规表；`C5`/`C7` 首格占位）⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-e` | **防假红对照**：`good-note-after-tabular.tex`（`\end{tabular}` 之后有 `\par` 表注；`C1`/`C4` 量宽）⇒ **必须仍绿** | （无） |
| `CTRL-GREEN-f` | **防假红对照**：`good-rulethickness.tex`（三条主线带可选线宽参数 `\toprule[1.2pt]` 等 + `\cmidrule[..](lr){..}`；`RULES_RE` 吞 `[..]`）⇒ **必须仍绿** | （无） |

`MUT-C7a` 与 `MUT-C7b` 的区别：前者改在**非 `S` 列**、产物**照常编过** ⇒ 只有 `C7` 抓得到
（这正是"别只靠编不过当判据"的实证）；后者改在 `S` 列、**连 `C1` 一起红** ⇒ 两条并排，
说明源码层判据与编译层判据是**两条独立的臂**。

★ **两处"连带红"是判据的性质、不是驱动器出错**（`expect` 里如实写死，不掩盖）：
`MUT-C5` 清空一格 ⇒ 空格子**既是** `C5` 的"空格子"**也是** `C7` 的"非规范缺失值"（空串在缺失变体集里）；
`MUT-C7b` 去掉花括号 ⇒ 源码层 `C7` 与编译层 `C1` 同时红。**空格的 C5-only 变体**（纯列数错）在 `tabular`
里会先触发 `Extra alignment tab` ⇒ 必带 `C1`，故本表不设该变体。**`\\pm` / `\\resizebox` 等更细的形态本表未覆盖**（不声称穷尽）。

★ `MUT-FC1` / `MUT-FC2` 打的是**fail-closed 分支**（不是"内容不合规"）：解析不出列说明 / `tabular`
不唯一 ⇒ 下游 `C5`–`C8` 一并**无从判而判红**（`C2`/`C3` 报"不唯一/解析失败"）。
★ **射程（2026-10-02 Task 4 收紧）**：报告 §1 并列 **5 类** fail-closed，**这两条只兑现其中 2 类**
（列说明解析失败 / `tabular` 不唯一）—— **不许**读成"§1 的声明已全部有真红作证"；
余 3 类**仍无真红**（其中 2 类**不触碰冻结件构造不出**）。口径见 Task 2 报告 §7.3 与
`tests/skills/table/red-green-evidence.md` §7 —— 本仓硬规矩「凡列清单必须有真红」在此**只到 2/5**。
`CTRL-GREEN-c` 则是**反向**锁：`\\multicolumn` 塌缩成 cells 一格后，跨列之后的数值格**必须**按起始列归位，
**不许**把合规表判红（`C6` 假红的回归对照）。

★ `CTRL-GREEN-d` / `MUT-LEAD-a` 一正一反锁住 `C5`/`C7` 的**首格占位豁免**（2026-10-02 RED 暴露）：
豁免只认"首格空 **且** 紧随一个 `\\multicolumn{n≥2}` 跨列分组"（两级表头的标准写法）——
`CTRL-GREEN-d` 是这一形态（必须绿），`MUT-LEAD-a` 把**列头行**首格清空、其后是普通格
（必须红 `C5`,`C7`）⇒ 证明豁免不是"凡首格空就放行"。**非首格的空洞、跨列后留空格等其它写法本表未覆盖**（不声称穷尽）。

★ `CTRL-GREEN-e` / `MUT-C1b` 一绿一红锁住**量宽只取到 `\\end{tabular}`**（2026-10-02 RED 暴露）：
`\\settowidth` 的实参碰 `\\par` 会炸（`Paragraph ended before \\@settodim`）⇒ 表注里的 `\\par` 曾让
`C1` **假红**、`C4` 分子量成 0。`CTRL-GREEN-e` 是"表注在 `tabular` 之后"的合规表（必须绿）；
`MUT-C1b` 在同一件的表注里塞未定义控制序列 ⇒ `C1` 真红，证明修好量宽后 `C1` 仍抓得到片段里的真错。

★ `CTRL-GREEN-f`（2026-10-03 全分支终审修复轮 I-1）：**可选线宽参数**（`\\toprule[1.2pt]` /
`\\midrule [0.8pt]`（宏名与 `[` 间可夹横空白）/ `\\bottomrule[1.2pt]` / `\\cmidrule[0.6pt](lr){2-3}`）
是 booktabs 的**标准合法写法**（`C1` 绿），而旧 `RULES_RE` 不吞 `[..]` ⇒ 剥掉规则线后留裸 `[..]` ⇒
幻影一行 ⇒ `C5`+`C8` **假红**。`CTRL-GREEN-f` 是这一形态的合规表（必须全绿）—— 与 `bd97fd6` 修掉的
前两处假红（前导 `&`、表注 `\\par`）**同型**（都只在另一种合法写法下现形）。
**其余可选参数写法（换行后的 `[..]`、`\\specialrule` 的更多实参组合等）本表未覆盖**（不声称穷尽）。
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
CHK = ROOT / "tests/skills/table/check-table-style.py"
BASE = ROOT / "tests/skills/table/fixtures/good-basic.tex"
TEMPLATE = ROOT / ".claude/skills/mcm-table/assets/table-template.tex"
NORM = ROOT / ".claude/skills/mcm-table/references/table-style.md"
FIX2 = ROOT / "tests/skills/table/fixtures/good-multilevel.tex"
FIX3 = ROOT / "tests/skills/table/fixtures/good-multicolumn.tex"
FIX_LEADING = ROOT / "tests/skills/table/fixtures/good-multilevel-leading.tex"   # F1 正控制（前导 `&`）
FIX_NOTE = ROOT / "tests/skills/table/fixtures/good-note-after-tabular.tex"      # F2 正控制（表注在 tabular 后）
FIX_RULE = ROOT / "tests/skills/table/fixtures/good-rulethickness.tex"           # F3 正控制（可选线宽参数 `[..]`）
ALL_IDS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"]
# 变异**不许**动的入库件（收尾逐件比对 blob）
GUARDED = (CHK, BASE, FIX2, FIX3, FIX_LEADING, FIX_NOTE, FIX_RULE, TEMPLATE, NORM)


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], cwd=str(ROOT),
                          capture_output=True, text=True).stdout.strip()


def run_checker(tex_path):
    """跑检查器；返回 `(rc, stdout, {判据ID: PASS|FAIL})`。"""
    pr = subprocess.run([sys.executable, str(CHK), "--tex", str(tex_path)],
                        cwd=str(ROOT), capture_output=True, text=True)
    verdict = {}
    for line in pr.stdout.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(\S+)\s", line)
        if m:
            verdict[m.group(2)] = m.group(1)
    return pr.returncode, pr.stdout, verdict


def _raw(cmdline, rc, out):
    body = "\n".join("      | " + l for l in out.rstrip("\n").splitlines())
    return f"$ {cmdline}   → exit={rc}\n{body}"


class Mutation:
    """一条变异：把一个文本变换加到**某个基准副本**上，断言红的判据集合**恰好**是 `expect`。

    `base` 默认 `good-basic.tex`；F1/F2 的对照走各自的新正控制样本（`base=` 显式给）。
    """

    def __init__(self, mid, desc, transform, expect, base=None):
        self.mid, self.desc, self.transform, self.expect = mid, desc, transform, set(expect)
        self.base = base or BASE

    def run(self, tmpdir):
        src = self.base.read_bytes().decode("utf-8")
        new = self.transform(src)
        if new == src:
            return False, f"驱动器自己报错：变换没有改变文本（{self.mid}）"
        p = tmpdir / f"{self.mid}.tex"
        p.write_bytes(new.encode("utf-8"))                     # 一律 write_bytes（全 LF）
        rc, out, verdict = run_checker(p)
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == self.expect)
        note = "" if ok else f"   <<< 期望红 {sorted(self.expect)} · 实红 {sorted(actual)}"
        detail = (f"变换：{self.desc}\n"
                  f"      期望红 = {sorted(self.expect) or '（无，必须全绿）'} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)} {note}\n"
                  + _raw(f"check-table-style.py --tex {self.mid}.tex", rc, out))
        return ok, detail


def _sub(old, new):
    def f(src):
        if old not in src:
            raise AssertionError(f"基准里找不到待改片段：{old!r}")
        return src.replace(old, new, 1)
    return f


def _move_caption_below(src):
    m = re.search(r"[ \t]*\\caption\{[^}]*\}\n", src)
    if not m:
        raise AssertionError("找不到 `\\caption{…}` 行")
    cap = m.group(0).strip("\n ")
    rest = src[:m.start()] + src[m.end():]
    if "\\end{tabular}" not in rest:
        raise AssertionError("找不到 `\\end{tabular}`")
    return rest.replace("\\end{tabular}", "\\end{tabular}\n  " + cap, 1)


def _caption_below_with_override(src):
    """表题移下 + 在 `\\begin{table}` 前声明覆盖 ⇒ `C3` 必须仍绿。"""
    out = _move_caption_below(src)
    return out.replace("\\begin{table}", "% mcm-table-caption: below\n\\begin{table}", 1)


def _add_second_tabular(src):
    """在 `\\begin{table}` 内**再塞一个** `tabular` ⇒ `tabular` 不唯一（fail-closed）。"""
    tail = "  \\end{tabular}\n"
    extra = ("  \\begin{tabular}{l}\n"
             "    \\toprule\n"
             "    x \\\\\n"
             "    \\bottomrule\n"
             "  \\end{tabular}\n")
    if tail not in src:
        raise AssertionError("基准里找不到 `  \\end{tabular}\\n`")
    return src.replace(tail, tail + extra, 1)


MUTATIONS = [
    Mutation("MUT-C1", "表题里塞未定义控制序列（编不过；settowidth 臂不受影响）",
             _sub("\\caption{A small illustrative table.}", "\\caption{\\zzundefinedmacro A small illustrative table.}"),
             {"C1"}),
    Mutation("MUT-C2a", "删掉 `\\bottomrule`", _sub("    \\bottomrule\n", ""), {"C2"}),
    Mutation("MUT-C2b", "列说明里塞 `|`",
             _sub("{l l S[table-format=3.2]}", "{|l l S[table-format=3.2]}"), {"C2"}),
    Mutation("MUT-C3", "`\\caption` 移到 `tabular` 之下（未声明覆盖）", _move_caption_below, {"C3"}),
    Mutation("MUT-C4", "表头塞超长不可断词 ⇒ 表宽超版心",
             _sub("Method & Note &", "Method & " + "W" * 260 + " &"), {"C4"}),
    Mutation("MUT-C5", "把一个格子清空（空格子同时也是「错形缺失值」⇒ 连带 C7）",
             _sub("Beta  & -- & {--}  ", "Beta  &  & {--}  "), {"C5", "C7"}),
    Mutation("MUT-C6", "同列改一处小数位", _sub("Gamma & ok & 5.67", "Gamma & ok & 5.6"), {"C6"}),
    Mutation("MUT-C7a", "非 `S` 列缺失值 `--` → `NA`（能编过）",
             _sub("Beta  & -- & {--}  ", "Beta  & NA & {--}  "), {"C7"}),
    Mutation("MUT-C7b", "`S` 列 `{--}` → `--`（源码层非规范形；连带编不过）",
             _sub("Beta  & -- & {--}  ", "Beta  & -- & --  "), {"C1", "C7"}),
    Mutation("MUT-C8", "删掉一条来源回显注释（漏一格）",
             _sub("% mcm-table-src: r3c2 <- pasted:r3c2\n", ""), {"C8"}),
    # ---- fail-closed 分支的真红（I-3）：报告 §1 的那批"任一 ⇒ 判红"声明，逐条给出红作证。
    Mutation("MUT-FC1", "列说明塞 `d{2}` ⇒ 解析失败（fail-closed；且 `d` 列型编不过）",
             _sub("{l l S[table-format=3.2]}", "{l l d{2}}"), {"C1", "C2", "C5", "C6", "C7", "C8"}),
    Mutation("MUT-FC2", "表里再塞一个 `tabular` ⇒ `tabular` 不唯一（fail-closed）",
             _add_second_tabular, {"C2", "C3", "C5", "C6", "C7", "C8"}),
    # ---- 2026-10-02 三份 RED 暴露的两条修复：各自的正/反向对照（见 docstring）。
    Mutation("MUT-C1b", "`\\end{tabular}` 之后的表注里塞未定义控制序列 ⇒ `C1` 真红（修量宽后仍抓得到真错）",
             _sub("Note: this note", "Note: \\zzundefinedmacro this note"),
             {"C1"}, base=FIX_NOTE),
    Mutation("MUT-LEAD-a", "前导 `&` 占位的边界：列头行首格清空（其后**不是**跨列分组）⇒ 仍算空格子",
             _sub("District & {Low}", " & {Low}"), {"C5", "C7"}, base=FIX_LEADING),
]

CONTROLS = [
    Mutation("CTRL-GREEN-a", "射程边界：只改表题**措辞**（不碰任何承重结构）",
             _sub("A small illustrative table.", "A different caption wording entirely."), set()),
    Mutation("CTRL-GREEN-b", "覆盖口径：表题移下 + 声明 `% mcm-table-caption: below`",
             _caption_below_with_override, set()),
]


class FileControl:
    """一条**防假红对照**：直接判一份**入库样本**，断言**全绿**（不做 BASE 变换）。

    与 `Mutation` 的区别：`Mutation` 是从 `good-basic.tex` 现场改坏；`FileControl` 判的是
    一份**本来就合规**的样本 —— 用来锁住"本器不会把合规构造判红"（`I-2` 的 `\\multicolumn` 假红即此类）。
    """

    def __init__(self, cid, desc, path, expect=()):
        self.cid, self.desc, self.path, self.expect = cid, desc, path, set(expect)

    @property
    def mid(self):                                              # 与 `Mutation` 统一（`main` 里共用 `mu.mid`）
        return self.cid

    def run(self, _tmpdir):
        rc, out, verdict = run_checker(self.path)
        actual = {cid for cid, v in verdict.items() if v == "FAIL"}
        ok = (actual == self.expect)
        note = "" if ok else f"   <<< 期望红 {sorted(self.expect)} · 实红 {sorted(actual)}"
        detail = (f"对照件：{self.desc}\n"
                  f"      期望红 = {sorted(self.expect) or '（无，必须全绿）'} · 实红 = {sorted(actual)}"
                  f" · 覆盖到的判据行 {sorted(verdict)} {note}\n"
                  + _raw(f"check-table-style.py --tex {self.path.name}", rc, out))
        return ok, detail


FILE_CONTROLS = [
    FileControl("CTRL-GREEN-c",
                "`\\multicolumn` **合规表**必须全绿（`I-2` 假红回归对照：跨列后的数值格按**起始列**归位）",
                FIX3, set()),
    FileControl("CTRL-GREEN-d",
                "**前导 `&`** 的两级表头合规表必须全绿（`C5`/`C7` 首格占位豁免；2026-10-02 RED 假红回归）",
                FIX_LEADING, set()),
    FileControl("CTRL-GREEN-e",
                "`\\end{tabular}` **之后**有 `\\par` 表注的合规表必须全绿（`C1`/`C4` 量宽假红回归；2026-10-02 RED 暴露）",
                FIX_NOTE, set()),
    FileControl("CTRL-GREEN-f",
                "三条主线带可选线宽参数（`\\toprule[1.2pt]` 等）+ `\\cmidrule[..](lr){..}` 的合规表必须全绿"
                "（I-1 假红回归：`RULES_RE` 不吞 `[..]` ⇒ 幻影一行 ⇒ `C5`+`C8` 假红；2026-10-03 终审修复轮）",
                FIX_RULE, set()),
]


def main():
    print("=" * 78)
    print(f"变异驱动器 · check-table-style.py（mcm-table）：8 条判据逐条打红 + 2 条 fail-closed 分支打红 "
          f"+ 2 条修复边界打红 + {len(CONTROLS) + len(FILE_CONTROLS)} 条对照（必须绿）")
    print("=" * 78)
    print(f"检查器 = {CHK.relative_to(ROOT).as_posix()}  blob {git_hash_object(CHK)}")
    print(f"基准样本 = {BASE.relative_to(ROOT).as_posix()}  blob {git_hash_object(BASE)}")
    guarded_before = {p: git_hash_object(p) for p in GUARDED}

    # 前置：干净态必须**全绿**（否则下面每条"红"都不说明问题）
    rc0, out0, v0 = run_checker(BASE)
    base_ok = rc0 == 0 and all(v0.get(i) == "PASS" for i in ALL_IDS)
    print(f"\n前置（基准样本干净态）：exit={rc0} · "
          f"{'8 条全 PASS' if base_ok else '未全绿 <<< 判据行=' + str(sorted(v0.items()))}")

    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix="mcmtable-mut-"))
    rows, failed = [], []
    try:
        for mu in MUTATIONS:
            try:
                ok, detail = mu.run(tmpdir)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            rows.append(("RED-OK" if ok else "RED-BAD", mu.mid, mu.desc, detail))
            if not ok:
                failed.append(mu.mid)

        ctrl_rows = []
        for mu in CONTROLS + FILE_CONTROLS:
            try:
                ok, detail = mu.run(tmpdir)
            except AssertionError as e:
                ok, detail = False, f"驱动器自己报错：{e}"
            if not ok:
                failed.append(mu.mid)
            ctrl_rows.append(("GREEN-OK" if ok else "GREEN-BAD", mu.mid, mu.desc, detail))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("\n" + "=" * 78)
    print("逐条结果（每条**逐字**贴检查器的原始 stdout）")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<11} {mid:<10} {desc}")
        print(detail)
    print("-" * 78)
    print("对照（不是判据变异：`GREEN` = 该绿）")
    for st, mid, desc, detail in ctrl_rows:
        print(f"{st:<11} {mid:<10} {desc}")
        print(detail)

    # ---------------------------------------------------------------- 还原自证
    guarded_after = {p: git_hash_object(p) for p in GUARDED}
    byte_ok = guarded_after == guarded_before
    st = subprocess.run(["git", "status", "--short"], cwd=str(ROOT),
                        capture_output=True, text=True).stdout
    dirty = sorted(l for l in st.splitlines() if l.strip())
    rerun_rc, rerun_out, rerun_v = run_checker(BASE)

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    for p in GUARDED:
        now = guarded_after[p]
        print(f"  {p.relative_to(ROOT).as_posix():<58} blob {now}  "
              f"{'== 变异前' if now == guarded_before[p] else '!= 变异前 <<<'}")
    print(f"  受保护件逐个 blob 还原: {byte_ok}")
    print(f"  变异后复跑（基准样本）：exit={rerun_rc} · "
          f"{'8 条全 PASS' if all(rerun_v.get(i) == 'PASS' for i in ALL_IDS) else sorted(rerun_v.items())}")
    print(f"  全仓 `git status --short`:\n{st if st.strip() else '      （空）'}")

    n_red_ok = len(MUTATIONS) - len([m for m in failed if m in [mm.mid for mm in MUTATIONS]])
    all_ctrls = CONTROLS + FILE_CONTROLS
    n_ctl_ok = len(all_ctrls) - len([m for m in failed if m in [cc.cid for cc in all_ctrls]])
    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {n_red_ok}/{len(MUTATIONS)} 红（check-table-style.py 的 C1–C8 逐条打红 + 2 条 fail-closed 分支打红 "
          f"+ 2 条修复边界打红：`MUT-C1b`/`MUT-LEAD-a`）"
          + ("" if not [m for m in failed if m.startswith('MUT')] else f"（未达预期：{', '.join(m for m in failed if m.startswith('MUT'))}）"))
    print(f"MUT: 对照 {n_ctl_ok}/{len(all_ctrls)} 达预期（必须绿：射程边界 + C3 覆盖口径 + `\\multicolumn` 合规表 "
          f"+ 前导 `&` 两级表头 + `\\end{{tabular}}` 后表注 + 可选线宽参数合规表）")
    print(f"MUT: 合计 {n_red_ok + n_ctl_ok}/{len(MUTATIONS) + len(all_ctrls)} 达预期（合计）")
    # ★ 合计行**不是末行**（照 mutate-figure-style.py 的形态）：末行放"运行完整性"读数。
    print(f"RUN: 受保护件 blob 逐件还原={byte_ok} · 基准样本复跑 exit={rerun_rc} · "
          f"全仓 `git status --short` {'空' if not dirty else '非空 <<< ' + '; '.join(dirty)}")
    return 0 if (not failed and base_ok and byte_ok and rerun_rc == 0 and not dirty) else 1


if __name__ == "__main__":
    sys.exit(main())
