"""`verify_all.py` 新增判据的**变异/负例证据**驱动器（Task 7 · D4/D5/D9）。

    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-mutation-driver.py \
        tests/papers/reports/all-mutation-evidence.txt

判据不得只写「我认为它会因 X 失败」（`docs/mcm-suite-lessons.md` §4.2 第一道防线
拦不住第 4 例）。每条**新增判据**要么有一条**源码变异**（改坏被测对象 → 跑 → 看红），
要么（被测对象是**已冻结**的子脚本、不得改动时）有一条**负例探针**——两种都在下面的
记录里**标明是哪一种**，不混为一谈。

## 第九例（陈旧字节码）的处理

改码实验必须 `PYTHONDONTWRITEBYTECODE=1` **并清 `__pycache__`**，两者配对。
本驱动器：① 开工前删掉 `tests/papers`、`tools/papers` 下的 `__pycache__`（并记录删了
几个）；② 每个探针都跑在**新进程**里、env 带 `PYTHONDONTWRITEBYTECODE=1`
（`.pyc` 失效只看源文件 mtime 的**整数秒** + 字节数，「改坏 → 跑 → 还原」落在同一秒
且长度相同时，进程仍会加载**坏**字节码）；③ 每条变异跑完**还原并当场核对 blob**
（`git hash-object`），对不上就记「作废」并让它影响总体判定。

## 四个阶段

* 阶段 1：源码变异 / 负例探针（秒级，不跑子脚本）
* 阶段 2：**端到端**限样本跑（干净版）——限样本跑不碰放行证据的正面证据
* 阶段 3：**端到端**限样本跑（`M-D4F` 变异在位）——落点守卫会红、放行证据仍未被触碰

阶段 2/3 每跑一次会依次拉起八个子脚本（`--limit 1` = 各脚本的 1 份 + 自己的见证集），
故本驱动器是分钟级、不是秒级。它**不重跑** `cli all`（那是
`tests/papers/recon/all-determinism-scan.py` 的活）。

## 复审后补的条目（2026-09-26）

`N-DET`（A-1 的**判数**，同时当场量出**旧**判据对「变了 17」免疫）· `N-EV-FALSE`
（A-2 的第二支：`…: False`）· `N-EV-SUFFIX`、`N-A1-THREE`（复审点名的两条入库红证据）·
`N-EV-ABSPATH`（A-4 从外面补的那道扫描）。负例用的假产物一律写进 `build/`（gitignored）
并在用完后删除，条目里逐条打印「已删 = True」。

## 本文件的输出**逐字节可重放**（A-3 的连带）

它内嵌了 `verify_all.py` 的 blob 与放行证据的 sha256，也**逐字转抄**阶段 2/3 的 stdout
末尾 22 行。原先那些末尾里含「耗时 X.Xs」（逐脚本墙钟），于是本文件重跑一次就不一样；
A-3 把墙钟搬进 `tests/papers/reports/all-timing.txt` 之后，`verify_all.py` 的 stdout 里
**不再有任何随运行变化的量**，本文件才真的是「跑两遍逐字节相同」。
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "tests" / "papers"
VERIFY_ALL = HERE / "verify_all.py"
LIMITED_DIR = HERE / "reports-limited"
RELEASE = HERE / "reports" / "pilot-summary.txt"
MUTANT = HERE / "verify_zzmutant.py"

PROBE_HEAD = f"""
import importlib.util, os, sys, time
from pathlib import Path
spec = importlib.util.spec_from_file_location("va", r"{VERIFY_ALL.as_posix()}")
va = importlib.util.module_from_spec(spec)
spec.loader.exec_module(va)
"""

PROBE_D1 = PROBE_HEAD + """
lines = []
stages, ok = va.check_stages(lines)
print("DERIVED=" + " ".join(s.name for s in stages))
print("STAGES_OK=" + str(ok))
print("TEXT=" + " || ".join(lines))
"""

PROBE_LIM = PROBE_HEAD + """
out, msg = va.resolve_summary(%(limit)d)
same, _x = va.branch_crosscheck(%(limit)d, out, msg)
print("OUT_REL=" + va.rel(out))
print("RELEASE_REL=" + va.rel(va.RELEASE))
print("GUARD_FIRED=" + str(bool(msg)))
print("CROSS_OK=" + str(same))
print("MSG=" + (msg or "<空>"))
"""

PROBE_BYPASS = PROBE_HEAD + """
out, msg = va.recheck_summary(3, va.RELEASE)
print("A_OUT=" + va.rel(out))
print("A_GUARD_FIRED=" + str(bool(msg)))
print("A_MSG=" + (msg or "<空>"))
out2, msg2 = va.recheck_summary(0, va.limited_path(0))
print("B_OUT=" + va.rel(out2))
print("B_RELEASE_REL=" + va.rel(va.RELEASE))
print("B_GUARD_FIRED=" + str(bool(msg2)))
print("B_MSG=" + (msg2 or "<空>"))
"""

PROBE_D5 = PROBE_HEAD + """
lines = []
ok = va.check_one_stage(lines, va.HERE / "verify_zzmutant.py", 0, {})
print("OK=" + str(ok))
print("DERIVED_HAS_MUTANT=" + str("verify_zzmutant.py" in [s.name for s in va.derive_stages()]))
print("TEXT=" + " || ".join(lines))
"""

PROBE_EV = PROBE_HEAD + """
lines = []
ok = va.check_evidence(lines, va.HERE / "verify_io.py", va.REPORTS / "io-report.txt",
                       "RESULT: PASS", 0, "", time.time() + 10**6, time.time() + 10**6,
                       False)
print("FRESH_OK=" + str(ok))
print("FRESH_TEXT=" + " || ".join(lines))
lines2 = []
ok2 = va.check_evidence(lines2, va.HERE / "verify_nope.py", va.REPORTS / "nope-report.txt",
                        "RESULT: PASS", 0, "", 0.0, 0.0, False)
print("MISSING_OK=" + str(ok2))
print("MISSING_TEXT=" + " || ".join(lines2))
"""

# ---- 复审后新增判据的负例探针（2026-09-26，A-1 / A-2 / A-4 / m-6）----
# 确定性**判数**（A-1）。同时跑**旧**判据（`check_record` 的短语那一层），是为了把
# 「为什么非要加这条」当场量出来：旧判据对「变了 17」**免疫**。
PROBE_DET = PROBE_HEAD + """
p = Path(os.environ["ZDET_FILE"])
old_lines = []
va.git_tracked = lambda _p: True      # 模拟「这份记录已入库」，把差异隔离到「只判短语」
old = va.check_record(old_lines, p, "确定性实测", ("跑前", "跑后"))
print("OLD_OK=" + str(old))
new_lines = []
new = va.check_determinism_counts(new_lines, p)
print("NEW_OK=" + str(new))
print("NEW_TEXT=" + " || ".join(new_lines))
"""

# 产物侧的三种负例（A-2 的 `…: False`、m-6 的「末行带后缀」、A-4 的绝对路径痕迹）。
PROBE_EVFAKE = PROBE_HEAD + """
p = Path(os.environ["ZEV_FILE"])
lines = []
ok = va.check_evidence(lines, va.HERE / "verify_b.py", p, os.environ["ZEV_RESULT"],
                       0, "", time.time() - 100.0, time.time() + 100.0, True)
print("EV_OK=" + str(ok))
print("EV_TEXT=" + " || ".join(lines))
"""

# `read_baseline` 的两条 raise（坏行 / 空表）。**空表特别要紧**：两份空表相等会让
# 「原件未改动」凭空成立。非法基线一律**抛**、不返回空表。
PROBE_BASE = PROBE_HEAD + """
out = {}
for name in ("build/fake-baseline-摘要长度不对.txt", "build/fake-baseline-空表.txt"):
    try:
        va.read_baseline(Path(name))
        out[name] = "**没有抛**"
    except ValueError as e:
        out[name] = "ValueError: " + str(e)[:70]
    except Exception as e:                      # noqa: BLE001
        out[name] = "别的异常：" + type(e).__name__
print("BASE_LEN=" + out["build/fake-baseline-摘要长度不对.txt"])
print("BASE_EMPTY=" + out["build/fake-baseline-空表.txt"])
"""

# `check_record` 的三条 fail 分支（不存在 / 未入库 / 缺短语 / 含样本口径后缀）。
PROBE_REC = PROBE_HEAD + """
va.git_tracked = lambda _p: True            # 把差异隔离到「短语」那一条上
lines = []
a = va.check_record(lines, Path("build/根本没有这份记录.txt"), "x", ("耗时",))
b = va.check_record(lines, Path("build/fake-record-缺短语.txt"), "x", ("绝不出现的短语",))
c = va.check_record(lines, Path("build/fake-record-含样本口径后缀.txt"), "x", ("耗时",))
va.git_tracked = lambda _p: False           # 末条：这份记录没入库
d = va.check_record(lines, va.TIMING, "x", ("耗时", "s/份"))
print("REC_MISSING=" + str(a))
print("REC_SHORT=" + str(b))
print("REC_LIMITED=" + str(c))
print("REC_UNTRACKED=" + str(d))
print("REC_TEXT=" + " || ".join(lines))
"""

# 「派生为空」与「6b 交付缺失」两条回归守卫。
PROBE_EMPTY = PROBE_HEAD + """
Path("build/empty-stages").mkdir(parents=True, exist_ok=True)
va.HERE = Path("build/empty-stages")
lines = []
stages, ok = va.check_stages(lines)
print("STAGES=" + str(stages))
print("EMPTY_OK=" + str(ok))
print("EMPTY_TEXT=" + " || ".join(lines))
"""

PROBE_6B = PROBE_HEAD + """
va.SIX_B = (("corpus/papers/根本不存在.md", "假交付"),)
lines = []
ok = va.check_6b(lines)
print("SIXB_OK=" + str(ok))
print("SIXB_TEXT=" + " || ".join(lines))
"""

# A1 的三类差异（改动 / 缺失 / 新增）。语料原件不得改动 ⇒ 用**负例探针**：拿真实
# 哈希表当底，人工造出三类差异各一条，写进 build/，再把基线指向它。
PROBE_A1 = PROBE_HEAD + """
from tools.papers import io
# **把键统一成 `/` 分隔**（`io.sha256_tree` 在 Windows 上给的是 `\\` 分隔的仓库相对键）。
# 理由：本探针要演示的是 A1 的**三类差异逻辑**，不是路径分隔符；而 `\\` 形态会被
# `report.ABSPATH_TRACE` 的 UNC 那一支读成绝对路径痕迹（`\\\\[^\\s]`），于是**入库的
# 变异证据**里会多出一条「像绝对路径」的串。故这里把**两侧**（基线与 hash 表）都换成
# `/`，逐字转抄的仍然是探针的原样输出——归一化发生在**探针内部**，不发生在记录环节。
_real = io.sha256_tree
io.sha256_tree = lambda c: {k.replace(chr(92), "/"): v for k, v in _real(c).items()}
items = sorted(io.sha256_tree(va.PILOT).items())
fake = dict(items)
fake[items[0][0]] = "0" * 64                      # 改动：摘要与现在不同
del fake[items[1][0]]                             # 新增：基线没有、现在有
fake[va.PILOT + "/ZZ/9999999/不存在.pdf"] = "1" * 64   # 缺失：基线有、现在没有
base = Path("build") / "fake-origin-baseline.txt"
base.write_bytes("".join(h + "  " + k + chr(10) for k, h in sorted(fake.items())).encode("utf-8"))
va.BASELINE_ALL = base
va.BASELINE_PILOT = base
lines = []
ok = va.check_origin(lines)
base.unlink()
print("A1_OK=" + str(ok))
print("A1_TEXT=" + " || ".join(lines))
"""

MUTANT_SRC = '''"""临时变异件（驱动器建、驱动器删）：制造「退出码与 RESULT 行矛盾」。"""
import os
import sys

mode = os.environ.get("ZMUT_MODE", "fail_exit0")
if mode == "fail_exit0":
    print("RESULT: FAIL")
    raise SystemExit(0)
if mode == "bad_utf8":
    sys.stdout.buffer.write("正文\\n".encode("utf-8"))
    sys.stdout.buffer.write(b"\\xff\\xfe\\xfd\\n")
    sys.stdout.buffer.flush()
    print("RESULT: PASS")
    raise SystemExit(0)
print("RESULT: PASS")
raise SystemExit(3)
'''

SIX_SNAPSHOT = (
    'return [HERE / s for s in ("verify_io.py", "verify_wm.py", "verify_b.py",\n'
    '                             "verify_c.py", "verify_d.py", "verify_ids.py")]'
)

# 落点函数里那一行的**原文**（变异替换的锚点；对不上就整轮作废，不静默跳过）。
ANCHOR_LIMIT_LINE = "    out = limited_path(limit) if limit > 0 else RELEASE"
ANCHOR_DERIVE = "    return sorted(p for p in HERE.glob(STAGE_GLOB) if p.resolve() != ME)"


# ---- 负例探针用的假产物（一律放 build/，gitignored；每条用完即删）----
REPORTS = HERE / "reports"


def fake_determinism_changed17() -> str:
    """真实确定性记录的**影子**：尾巴上追加一遍「最后一遍」节，`formulas` 变了 **17**。

    这正是 A-1 说的失效场景——某次 `cli all` 真的非确定，实施者**如实**把那一遍落盘。
    旧判据（只判「文件在 + 含 跑前/跑后/43 份」）对这份记录照样打 ✓；新判据必须红。
    """
    real = (REPORTS / "all-determinism.txt").read_bytes().decode("utf-8")
    return real + (
        "## build/all-determinism-s9.json → build/all-determinism-s10.json\n"
        "  入库产物：5 份，blob 变了 **0** 份\n"
        "  md         跑前 43 个 · 跑后 43 个 · 只在跑前 0 · 只在跑后 0 · blob 变了 0 ⇒ 逐字节相同\n"
        "  figures    跑前 1816 个 · 跑后 1816 个 · 只在跑前 0 · 只在跑后 0 · blob 变了 0 ⇒ 逐字节相同\n"
        "  formulas   跑前 1564 个 · 跑后 1581 个 · 只在跑前 0 · 只在跑后 17 · blob 变了 17 ⇒ **有变化**\n"
        "\n## 结论（影子记录，仅供这条负例使用）\n")


# 形态一：产物里出现 `…: False`（机器可读的判据行自报失败），而行尾仍写 `RESULT: PASS`。
# 形态二：末行是 `RESULT: PASS (LIMITED …)`——限样本跑写的放行证据不构成放行依据。
# 形态三：产物正文里带**机器相关绝对路径**（io/wm 用 `traceback.format_exc()` 的形态）。
FAKE_EV_FALSE = ("正文（负例）\n"
                 "D1/D2/D3（机器可核）本批判定: False\n"
                 "RESULT: PASS\n")
FAKE_EV_SUFFIX = ("正文（负例）\n"
                  "全部判据通过: True\n"
                  "RESULT: PASS (LIMITED --limit 3)\n")
FAKE_EV_ABSPATH = ("正文（负例）：下面这行模拟 io/wm 崩溃时 `traceback.format_exc()` "
                   "写进产物的那一串\n"
                   "  File \"" + str(ROOT / "corpus" / "papers") + "\", line 1\n"
                   "RESULT: PASS\n")


def _sub_of(probe: str, limit: int) -> str:
    return probe % {"limit": limit}


CASES = [
    {
        "id": "M-D1", "kind": "源码变异",
        "what": "把 `derive_stages()` 改回**计划的六项快照**（`verify_io/wm/b/c/d/ids`）"
                "——这正是 D1 要防的失效形态",
        "subs": [(ANCHOR_DERIVE, "    " + SIX_SNAPSHOT.strip())],
        "probe": PROBE_D1,
        "red": lambda o: o.get("STAGES_OK") == "False" and "不在派生清单里" in o.get("TEXT", ""),
        "green": lambda o: (o.get("STAGES_OK") == "True"
                            and "verify_types.py" in o.get("DERIVED", "")
                            and "verify_map.py" in o.get("DERIVED", "")),
        "note": "红 = `check_stages` 判 FAIL 且**具名说出来少了谁**；"
                "绿 = 派生清单里含 6b 的两个脚本",
    },
    {
        "id": "M-D4F", "kind": "源码变异",
        "what": "把落点函数的**限样本分支**改坏（`limit > 0` 也返回放行证据）——正向守卫",
        "subs": [(ANCHOR_LIMIT_LINE, "    out = RELEASE")],
        "probe": _sub_of(PROBE_LIM, 3),
        "red": lambda o: (o.get("GUARD_FIRED") == "True" and o.get("CROSS_OK") == "False"
                          and o.get("OUT_REL") != o.get("RELEASE_REL")),
        "green": lambda o: (o.get("GUARD_FIRED") == "False" and o.get("CROSS_OK") == "True"
                            and o.get("OUT_REL") != o.get("RELEASE_REL")),
        "note": "红 = 守卫触发、落点被**改写走**（不是放行证据）、且与 `report.py` 的分支对账"
                "不一致；绿 = 落在限样本落点、对账一致",
    },
    {
        "id": "M-D4R", "kind": "源码变异",
        "what": "把落点函数的**全量分支**改坏（`limit <= 0` 也返回限样本落点）——镜像守卫",
        "subs": [(ANCHOR_LIMIT_LINE, "    out = limited_path(limit)")],
        "probe": _sub_of(PROBE_LIM, 0),
        "red": lambda o: (o.get("GUARD_FIRED") == "True" and o.get("CROSS_OK") == "False"
                          and o.get("OUT_REL") == o.get("RELEASE_REL")),
        "green": lambda o: (o.get("GUARD_FIRED") == "False" and o.get("CROSS_OK") == "True"
                            and o.get("OUT_REL") == o.get("RELEASE_REL")),
        "note": "红 = 守卫触发、**改写出的是放行证据**（不许把上一次的结论留在原地）、"
                "且分支对账不一致",
    },
    {
        "id": "N-D4B", "kind": "负例探针（不改源码）",
        "what": "模拟**调用点被绕开**：直接把 `RELEASE` / 限样本落点交给写前复核",
        "subs": [],
        "probe": PROBE_BYPASS,
        "red": lambda o: (o.get("A_GUARD_FIRED") == "True" and o.get("B_GUARD_FIRED") == "True"
                          and o.get("A_OUT") == o.get("B_RELEASE_REL")
                          and o.get("B_OUT") == o.get("B_RELEASE_REL")),
        "green": None,     # 这一条没有「绿」态：它就是绕开后的两向读数
        "note": "正向（限样本写放行证据）：**只判 FAIL、不改写**；镜像（全量写别处）："
                "判 FAIL **并改写回**放行证据。字面强度与 `report.py` 的 docstring 对齐——"
                "守卫保证的是「决策点被改坏」这一层，**不是**「物理上写不进去」",
    },
    {
        "id": "M-D5a", "kind": "源码变异（被测对象是临时子脚本）",
        "what": "临时子脚本**退出 0 却打印 `RESULT: FAIL`**——D5 ③ 的矛盾即红；"
                "同时验证派生清单**真的会把它从磁盘捡进来**",
        "subs": [], "make_mutant": "fail_exit0",
        "probe": PROBE_D5,
        "red": lambda o: (o.get("OK") == "False" and "矛盾" in o.get("TEXT", "")
                          and o.get("DERIVED_HAS_MUTANT") == "True"),
        "green": None,
        "note": "红 = 汇总结论不听子脚本的自称，且**具名**指出退出码与 RESULT 行矛盾",
    },
    {
        "id": "M-D5b", "kind": "源码变异（被测对象是临时子脚本）",
        "what": "临时子脚本**退出 3 却打印 `RESULT: PASS`**——反方向的矛盾",
        "subs": [], "make_mutant": "pass_exit3",
        "probe": PROBE_D5,
        "red": lambda o: o.get("OK") == "False" and "矛盾" in o.get("TEXT", ""),
        "green": None,
        "note": "红 = 与 M-D5a 同一条判据的反方向",
    },
    {
        "id": "N-EV", "kind": "负例探针（不改源码）",
        "what": "产物侧判据的两种形态：证据文件「**不是本次跑写的**」与「**根本不存在**」",
        "subs": [],
        "probe": PROBE_EV,
        "red": lambda o: (o.get("FRESH_OK") == "False"
                          and "不是本次跑写出来的" in o.get("FRESH_TEXT", "")
                          and o.get("MISSING_OK") == "False"
                          and "不存在" in o.get("MISSING_TEXT", "")),
        "green": None,
        "note": "两种形态**分开报**（教训：参照不存在 vs 存在但没解析出来，不得混同）",
    },
    {
        "id": "N-DET", "kind": "负例探针（不改源码）· A-1 的加严",
        "what": "确定性**判数**：喂一份「某次 `cli all` 真的非确定、实施者如实落盘」的假记录"
                "（真记录尾巴上追加一遍，`formulas` 那行 `blob 变了 17`，其余三处 0）",
        "subs": [],
        "fakes": {"build/fake-determinism-变了17.txt": fake_determinism_changed17},
        "env": {"ZDET_FILE": "build/fake-determinism-变了17.txt"},
        "env_green": {"ZDET_FILE": "tests/papers/reports/all-determinism.txt"},
        "probe": PROBE_DET,
        "red": lambda o: (o.get("OLD_OK") == "True" and o.get("NEW_OK") == "False"
                          and "非 0 ⇒ FAIL" in o.get("NEW_TEXT", "")),
        "green": lambda o: (o.get("OLD_OK") == "True" and o.get("NEW_OK") == "True"),
        "note": "红 = **旧判据没拦住**（`OLD_OK=True`：那三个词对它免疫——这正是加这条的"
                "理由）而新判据拦住了、且**具名说哪一处非 0**；"
                "绿 = 同一探针喂**真**记录时两条都通过（排除「判据恒红」）",
    },
    {
        "id": "N-EV-FALSE", "kind": "负例探针（不改源码）· A-2 的加严",
        "what": "产物里出现机器可读的 `…: False`（判据行自报失败），而行尾仍写 "
                "`RESULT: PASS`——`verify_d.py` 若某处写了 FAIL 行却漏了 `ok = False`，"
                "产物就是这个形状；b/c/d 三份产物用的正是这个形态（实测 b 3 / c 1 / d 1 条）",
        "subs": [],
        "fakes": {"build/fake-ev-自报False.txt": FAKE_EV_FALSE},
        "env": {"ZEV_FILE": "build/fake-ev-自报False.txt", "ZEV_RESULT": "RESULT: PASS"},
        "probe": PROBE_EVFAKE,
        "red": lambda o: (o.get("EV_OK") == "False"
                          and "自报失败" in o.get("EV_TEXT", "")
                          and "裸的 RESULT: PASS** ✓" in o.get("EV_TEXT", "")
                          and "：干净 ✓" in o.get("EV_TEXT", "")),
        "green": None,
        "note": "红 = 新的一支命中且**具名**列出那条判据行；同时断言另两条判据（裸 RESULT、"
                "绝对路径痕迹）**没**命中 ⇒ 红**归因于**这一支，不是别的判据顺带判红",
    },
    {
        "id": "N-EV-SUFFIX", "kind": "负例探针（不改源码）· 复审点名的入库红证据",
        "what": "放行证据末行带**样本口径后缀**（`RESULT: PASS (LIMITED --limit 3)`）——"
                "限样本跑写的结论不得冒充放行依据",
        "subs": [],
        "fakes": {"build/fake-ev-带后缀.txt": FAKE_EV_SUFFIX},
        "env": {"ZEV_FILE": "build/fake-ev-带后缀.txt",
                "ZEV_RESULT": "RESULT: PASS (LIMITED --limit 3)"},
        "probe": PROBE_EVFAKE,
        "red": lambda o: (o.get("EV_OK") == "False"
                          and "不是裸的" in o.get("EV_TEXT", "")
                          and "自报失败" not in o.get("EV_TEXT", "")),
        "green": None,
        "note": "红 = 「末行不是裸的 `RESULT: PASS`」那条命中；`自报失败`那条**不**命中"
                "（那条假产物里只有 `…: True`）⇒ 归因隔离",
    },
    {
        "id": "N-EV-ABSPATH", "kind": "负例探针（不改源码）· A-4 的加严",
        "what": "子脚本产物里出现**机器相关绝对路径**——`verify_io.py` / `verify_wm.py` "
                "用 `traceback.format_exc()`，崩溃那一次就是这个形状，而它们**自己一个都不扫**",
        "subs": [],
        "fakes": {"build/fake-ev-绝对路径.txt": FAKE_EV_ABSPATH},
        "env": {"ZEV_FILE": "build/fake-ev-绝对路径.txt", "ZEV_RESULT": "RESULT: PASS"},
        "probe": PROBE_EVFAKE,
        "red": lambda o: (o.get("EV_OK") == "False"
                          and "绝对路径痕迹" in o.get("EV_TEXT", "")
                          and "自报失败" not in o.get("EV_TEXT", "")
                          and "干净 ✓" not in o.get("EV_TEXT", "")
                          and "<abs-path>" in o.get("EV_TEXT", "")),
        "green": None,
        "note": "红 = 从**外面**补的那道扫描命中，且路径在报告里被 `report.scrub` 消毒成 "
                "`<abs-path>`（入库证据里不留机器相关绝对路径）",
    },
    {
        "id": "N-A1-THREE", "kind": "负例探针（不改源码）· 复审点名的入库红证据",
        "what": "A1 的**三类差异**（改动 / 缺失 / 新增）：原件与语料不得改动 ⇒ 拿真实哈希表"
                "当底，人工造出三类各一条，写进 `build/` 再让基线指向它"
                "（哈希键在探针内归一到 `/` 分隔——见探针里那段注释：`\\` 形态会被"
                "`report.ABSPATH_TRACE` 的 UNC 那一支读成绝对路径痕迹，那会让**这份入库"
                "证据自身**多出一条像绝对路径的串）",
        "subs": [],
        "probe": PROBE_A1,
        "red": lambda o: (o.get("A1_OK") == "False"
                          and "改动 ['" in o.get("A1_TEXT", "")
                          and "缺失 ['" in o.get("A1_TEXT", "")
                          and "新增 ['" in o.get("A1_TEXT", "")),
        "green": None,
        "note": "红 = 判 FAIL **且三类各自具名**（不是一句「原件被改动」了事）；"
                "绿态就是全量跑里那一条（实测 A1 结论 = 原件一字未动）",
    },
    {
        "id": "N-EMPTY", "kind": "负例探针（不改源码）· D1 的回归守卫",
        "what": "判据集**派生为空**（把 `HERE` 指到一个空目录）——「零依据地报绿」"
                "正是本项目栽过六次的形态",
        "subs": [],
        "probe": PROBE_EMPTY,
        "red": lambda o: (o.get("EMPTY_OK") == "False" and o.get("STAGES") == "[]"
                          and "为空" in o.get("EMPTY_TEXT", "")),
        "green": None,
        "note": "红 = 返回空清单**且**判 FAIL（两种情况分开报：清单空 vs 清单缺 6b 的两个）",
    },
    {
        "id": "N-6B", "kind": "负例探针（不改源码）· 6b 交付的存在性守卫",
        "what": "`check_6b` 的存在性分支：把 `SIX_B` 指向一个不存在的交付",
        "subs": [],
        "probe": PROBE_6B,
        "red": lambda o: (o.get("SIXB_OK") == "False" and "不存在" in o.get("SIXB_TEXT", "")),
        "green": None,
        "note": "红 = 判 FAIL **且具名是哪个交付**（不是一句「6b 不齐」了事）",
    },
    {
        "id": "N-BASE", "kind": "负例探针（不改源码）· 复审点名的入库红证据",
        "what": "`read_baseline` 的两条 raise：**坏行**（摘要不是 64 位）与**空表**"
                "（两份空表相等会让「原件未改动」凭空成立）",
        "subs": [],
        "fakes": {"build/fake-baseline-摘要长度不对.txt": "0" * 10 + "  corpus/x.pdf\n",
                  "build/fake-baseline-空表.txt": "\n   \n"},
        "probe": PROBE_BASE,
        "red": lambda o: ("ValueError" in o.get("BASE_LEN", "").replace("别的异常：", "")
                          and "ValueError" in o.get("BASE_EMPTY", "").replace("别的异常：", "")),
        "green": None,
        "note": "红 = 两条都**抛 `ValueError`**（不是返回空表、也不是别的异常）；"
                "`A1` 的上游由 `checks()` 的 `except (OSError, ValueError, KeyError)` 接住判红",
    },
    {
        "id": "N-REC", "kind": "负例探针（不改源码）· 复审点名的入库红证据",
        "what": "`check_record` 的四条 fail 分支：记录**不存在** / **没入库** / **缺约定的"
                "短语** / 记录里**含样本口径后缀**",
        "subs": [],
        "fakes": {"build/fake-record-缺短语.txt": "耗时 s/份\n43 份\n",
                  "build/fake-record-含样本口径后缀.txt": "耗时 s/份\n43 份\nLIMITED\n"},
        "probe": PROBE_REC,
        "red": lambda o: (o.get("REC_MISSING") == "False" and o.get("REC_SHORT") == "False"
                          and o.get("REC_LIMITED") == "False"
                          and o.get("REC_UNTRACKED") == "False"
                          and "不存在" in o.get("REC_TEXT", "")
                          and "没入库" in o.get("REC_TEXT", "")
                          and "含 `绝不出现的短语` = False" in o.get("REC_TEXT", "")
                          and "出现 `LIMITED` 1 处" in o.get("REC_TEXT", "")),
        "green": None,
        "note": "红 = 四条各自判 FAIL **且各自具名**（缺短语那条打印的是「含 `短语` = False」，"
                "后缀那条打印的是「出现 `LIMITED` N 处」——不混成一句「记录不合格」）",
    },
    {
        "id": "N-UTF8", "kind": "源码变异（被测对象是临时子脚本）",
        "what": "临时子脚本**吐出非 UTF-8 字节**——`decode()` 那一条：解不出来时**不吞、"
                "不替换**，直接判红（`errors='replace'` 会把「逐字转抄」变成「转抄一串"
                "替换符」，那比红更坏）",
        "subs": [], "make_mutant": "bad_utf8",
        "probe": PROBE_D5,
        "red": lambda o: (o.get("OK") == "False" and "不是合法 UTF-8" in o.get("TEXT", "")
                          and o.get("DERIVED_HAS_MUTANT") == "True"),
        "green": None,
        "note": "红 = 解码那一条**具名**报出，且派生清单真的把它从磁盘捡了进来；"
                "这一跑同时会打印另外两条 FAIL（没有 `RESULT:` 行、产物不存在），"
                "本条只断言解码那一条",
    },
]


def clear_pycache() -> list[str]:
    removed = []
    for d in (ROOT / "tests", ROOT / "tools"):
        for pyc in list(d.rglob("__pycache__")):
            shutil.rmtree(pyc, ignore_errors=True)
            removed.append(pyc.relative_to(ROOT).as_posix())
    return removed


def blob_of(p: Path) -> str:
    r = subprocess.run(["git", "hash-object", str(p)], capture_output=True, cwd=str(ROOT))
    return r.stdout.decode().strip()


def sha256_of(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "<不存在>"


def rel(p: Path) -> str:
    return p.resolve().relative_to(ROOT).as_posix()


def run_probe(src: str, extra_env: dict | None = None) -> str:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
    if extra_env:
        env.update(extra_env)
    r = subprocess.run([sys.executable, "-c", src], capture_output=True,
                       cwd=str(ROOT), env=env)
    txt = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        txt += f"\n[探针退出码 {r.returncode}]\n" + r.stderr.decode("utf-8", "replace")
    return txt


def parse(out: str) -> dict:
    got = {}
    for ln in out.splitlines():
        if "=" in ln:
            k, _, v = ln.partition("=")
            if re.fullmatch(r"[A-Z_0-9]+", k):
                got[k] = v
    return got


def run_verify_all(limit: int) -> tuple[int, str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run([sys.executable, str(VERIFY_ALL), "--limit", str(limit)],
                       capture_output=True, cwd=str(ROOT), env=env)
    txt = r.stdout.decode("utf-8", "replace")
    if r.returncode != 0:
        txt += f"\n[stderr] {r.stderr.decode('utf-8', 'replace')[:400]}"
    return r.returncode, txt


def tail(text: str, n: int = 22) -> str:
    return "\n".join(text.splitlines()[-n:])


def write_fakes(case: dict) -> list[Path]:
    """负例探针用的假产物（一律写进 `build/`，gitignored）。返回落盘清单（供删除）。"""
    made = []
    for relp, content in (case.get("fakes") or {}).items():
        p = ROOT / relp
        p.parent.mkdir(parents=True, exist_ok=True)
        body = content() if callable(content) else content
        p.write_bytes(body.encode("utf-8") if isinstance(body, str) else body)
        made.append(p)
    return made


def drop_fakes(made: list[Path]) -> None:
    for p in made:
        try:
            p.unlink()
        except OSError:
            pass


def phase_cases(report: list[str], original: str, orig_blob: str) -> bool:
    ok = True
    for i, case in enumerate(CASES, 1):
        report.append("-" * 78)
        report.append(f"[{i}/{len(CASES)}] {case['id']}　（{case['kind']}）")
        report.append(f"  是什么：{case['what']}")
        bad_anchor = [old for old, _ in case["subs"] if old not in original]
        if bad_anchor:
            report.append("  **变异锚点对不上**"
                          f"（`{bad_anchor[0].strip()[:60]}…`）——整轮作废，不静默跳过")
            ok = False
            continue
        mutated = original
        for old, new in case["subs"]:
            mutated = mutated.replace(old, new, 1)
        if mutated != original:
            VERIFY_ALL.write_bytes(mutated.encode("utf-8"))
        if case.get("make_mutant"):
            MUTANT.write_bytes(MUTANT_SRC.encode("utf-8"))
        fakes = write_fakes(case)
        if fakes:
            report.append("  负例用的假产物（写进 `build/`，gitignored，用完即删）："
                          + " ".join(rel(p) for p in fakes))
        try:
            env = {"ZMUT_MODE": case.get("make_mutant") or "fail_exit0", **case.get("env", {})}
            probe_out = run_probe(case["probe"], env)
        finally:
            VERIFY_ALL.write_bytes(original.encode("utf-8"))
            if MUTANT.exists():
                MUTANT.unlink()
            drop_fakes(fakes)
        got = parse(probe_out)
        red = bool(case["red"](got))
        report.append("  探针（变异在位）逐字输出：")
        report.extend("    " + ln for ln in probe_out.rstrip().splitlines())
        report.append(f"  ⇒ **红 = {red}**（要求：会红）")
        if case["green"] is not None:
            genv = {"ZMUT_MODE": "fail_exit0", **case.get("env_green", case.get("env", {}))}
            clean = run_probe(case["probe"], genv)
            green = bool(case["green"](parse(clean)))
            report.append("  探针（还原后 / 喂真文件）逐字输出：")
            report.extend("    " + ln for ln in clean.rstrip().splitlines())
            report.append(f"  ⇒ **还原后绿 = {green}**（要求：回到绿）")
        else:
            green = None
        report.append(f"  判定：{'通过' if red and (green is None or green) else '**未达标**'}"
                      f"　·　{case['note']}")
        ok &= red and (green is None or green)
        restored = blob_of(VERIFY_ALL)
        same = restored == orig_blob
        report.append(f"  还原核对：blob = {restored}（开工 {orig_blob}）"
                      f"⇒ {'一致 ✓' if same else '**不一致 ⇒ 作废**'}")
        ok &= same
        gone = not MUTANT.exists()
        report.append(f"  临时子脚本 `{MUTANT.name}` 已删 = {gone}")
        ok &= gone
        leftovers = [rel(p) for p in fakes if p.exists()]
        report.append(f"  负例假产物已删 = {not leftovers}"
                      + (f"（**残留：{leftovers}**）" if leftovers else ""))
        ok &= not leftovers
    return ok


def phase_e2e(report: list[str], original: str, orig_blob: str) -> bool:
    ok = True
    pre = sha256_of(RELEASE)
    if pre == "<不存在>":
        # **空比对是恒真判据**（第七例）：放行证据不在时，「跑前 == 跑后」两边都是
        # 哨兵串，什么都没证。这里按 FAIL 处理，逼着驱动器在全量跑**之后**再跑一次。
        report.append("")
        report.append("**前置未满足**：放行证据 `" + rel(RELEASE) + "` 本次不存在 ⇒ "
                      "阶段 2/3 的前后 sha256 对比会退化成**空比对（恒真）**，"
                      "什么都证不了。请先跑一次全量 `verify_all.py` 再来。判 FAIL。")
        return False
    report.append("")
    report.append("=" * 78)
    report.append("阶段 2：端到端限样本跑（**干净版**）——`python tests/papers/verify_all.py --limit 1`")
    rc, txt = run_verify_all(1)
    report.append(f"  退出码 = {rc}"
                  f"（**限样本跑可以退 0**：退出码只表示「这套判据在这套样本口径下全绿」，"
                  f"防误读靠的是落点与 RESULT 行的样本口径后缀，不是退出码——"
                  f"同 `report.py` 的既有设计。本条不拿退出码当判据）")
    report.append(f"  落点守卫字样出现 = {'落点守卫 FAIL' in txt}（干净版**不许**出现）")
    ok &= "落点守卫 FAIL" not in txt
    report.append("  逐字末尾 22 行：")
    report.extend("    " + ln for ln in tail(txt).splitlines())
    post = sha256_of(RELEASE)
    report.append(f"  放行证据 `{rel(RELEASE)}` 跑前/跑后 sha256：")
    report.append(f"    {pre}")
    report.append(f"    {post}　⇒ "
                  f"{'**相同 ✓**（限样本跑没碰放行证据）' if pre == post else '**不同 ⇒ FAIL**'}")
    ok &= pre == post
    lim = LIMITED_DIR / "pilot-summary-limited-1.txt"
    report.append(f"  限样本落点 `{rel(lim)}` 存在 = {lim.is_file()}")
    ok &= lim.is_file()

    report.append("")
    report.append("阶段 3：端到端限样本跑（**`M-D4F` 变异在位**）——落点守卫必须红、"
                  "且放行证据仍未被触碰")
    mutated = original.replace(ANCHOR_LIMIT_LINE, "    out = RELEASE")
    if mutated == original:
        report.append("  **变异锚点对不上**——阶段 3 视为未做")
        return False
    VERIFY_ALL.write_bytes(mutated.encode("utf-8"))
    try:
        rc3, txt3 = run_verify_all(1)
    finally:
        VERIFY_ALL.write_bytes(original.encode("utf-8"))
    report.append(f"  退出码 = {rc3}（必须非 0）")
    ok &= rc3 != 0
    has_guard = "落点守卫 FAIL" in txt3
    report.append(f"  落点守卫字样出现 = {has_guard}（变异在位**必须**出现）")
    ok &= has_guard
    has_fail = "RESULT: FAIL" in txt3
    report.append(f"  末行含 `RESULT: FAIL` = {has_fail}")
    ok &= has_fail
    report.append("  逐字末尾 22 行：")
    report.extend("    " + ln for ln in tail(txt3).splitlines())
    post3 = sha256_of(RELEASE)
    report.append(f"  放行证据跑后 sha256 = {post3} ⇒ "
                  f"{'**与阶段 2 跑后相同 ✓**' if post3 == post else '**不同 ⇒ FAIL**'}")
    ok &= post3 == post
    back = blob_of(VERIFY_ALL)
    report.append(f"  还原核对：blob = {back}（开工 {orig_blob}）"
                  f"⇒ {'一致 ✓' if back == orig_blob else '**不一致 ⇒ 作废**'}")
    ok &= back == orig_blob
    return ok


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    out_path = Path(sys.argv[1])
    original = VERIFY_ALL.read_bytes().decode("utf-8")
    orig_blob = blob_of(VERIFY_ALL)
    pyc = clear_pycache()
    report: list[str] = []
    report.append("`verify_all.py` 的新增判据：变异与负例证据（Task 7 · D4/D5/D9）")
    report.append("=" * 78)
    report.append("口径：每条**新增判据**要么有源码变异（改坏被测对象 → 跑 → 看红），")
    report.append("要么（被测对象是**已冻结**的子脚本、不得改动时）有负例探针；")
    report.append("两种**都在条目里标明**，不混为一谈（教训 4.2：只写「我认为它会失败」不算数）。")
    report.append("")
    report.append("复现命令：")
    report.append("  PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-mutation-driver.py \\")
    report.append("      tests/papers/reports/all-mutation-evidence.txt")
    report.append("")
    report.append(f"开工时清掉的 `__pycache__`：{pyc or '无'}"
                  f"（第九例：`.pyc` 失效只看源文件 mtime 的整数秒 + 字节数，"
                  f"「改坏→跑→还原」可能命中同一秒；本驱动器全程 "
                  f"`PYTHONDONTWRITEBYTECODE=1`、探针一律新进程、每条变异后核对还原 blob）")
    report.append(f"`verify_all.py` 开工 blob = {orig_blob}")
    report.append(f"`verify_all.py` 开工 sha256 = {sha256_of(VERIFY_ALL)}")
    report.append("")

    ok = phase_cases(report, original, orig_blob)
    ok &= phase_e2e(report, original, orig_blob)

    report.append("")
    report.append("=" * 78)
    report.append(f"总体：{'全部达标' if ok else '**有未达标项，见上**'}")
    text = "\n".join(report) + "\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(text.encode("utf-8"))
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
