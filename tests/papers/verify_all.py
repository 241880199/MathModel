"""试点汇总与放行评估（Task 7）：跑齐**磁盘上实际存在的全部判据脚本** + 原件哈希复核，
把结论写 `tests/papers/reports/pilot-summary.txt`（放行证据，入库）。

## 这份汇总回答什么、不回答什么

**回答**：2025 试点 43 份这条流水线能不能放行——判据集齐不齐、全量跑是不是全绿、
原件有没有被改动、抽取能不能确定性重跑、耗时有没有实测。

**不回答**：「能不能放行全量 201 份」。那是 Task 9，它的第一道闸门是 **R6**
（`io.problem_of` 对三类目录布局取不到题号）。本汇总把它**当场量出来**写进【6】，
不用一句「待办」代替测量。让这份 PASS 顺带被读成「201 份也能上」，
正是本项目最怕的那类假陈述（教训 4.2 家族）。

## 判据集**由磁盘派生**（D1，本任务的核心要求）

计划里的 `STAGES` 是 2026-09-23 的六项快照（`verify_io/wm/b/c/d/ids`）。仓里现在
**还有** `verify_types.py`（10 条）与 `verify_map.py`（16 条）——Task 6b 的产物。
照抄那份快照 ⇒ 6b 的 26 条判据**被漏在放行评估之外**，而汇总照样写「可放行」
= **假放行**。故清单每次运行**从 `tests/papers/verify_*.py` 派生**（减去本文件自身，
否则递归），派生结果逐项打印；另加两条回归守卫：派生为空 ⇒ 红；派生清单里**没有**
`verify_types.py` 或 `verify_map.py` ⇒ 红（这两条是对「有人把清单改回硬编码」的
定点防线，不是清单本身）。

## 判据：不读「自称」，只读「产物」（D5）

每个子脚本的**退出码**收上来，它的 `RESULT:` 行**逐字**抄进汇总；两者矛盾
（退出 0 却写 `RESULT: FAIL`，或非 0 却写 `RESULT: PASS`）⇒ 红；没有 `RESULT:` 行
⇒ 红（fail-closed）。**光看 stdout 不算数**：真正的产物是那个脚本**写入库的放行
证据文件**，本脚本另读它并要求 ① 存在 ② 末行 `RESULT:` 是**裸的** `RESULT: PASS`
（带 `LIMITED` ⇒ 红：写它的是限样本跑）③ 它的 mtime 落在本次运行之内（否则
「上一次的 PASS 留在库里冒充本次结论」——本项目栽过六次的那一族）④ 文件里的
`RESULT:` 行与 stdout 的**逐字相同**。

## `--limit N` 与双向落点守卫（D4）

`--limit N`（N > 0）= 限样本跑：转发给**支持 `--limit` 的子脚本**（谁支持由
`--help` 当场探测，探测结果逐项打印），并逐个子脚本判「放行证据 sha256 跑前 == 跑后」。
**2026-09-26（A-2）**：8 个脚本现在**全部**支持 `--limit`。此前 `verify_io.py` /
`verify_wm.py` 没有（输入是代码级探针/固定样本集，不是 43 份 PDF）⇒ 它们仍全量跑、
会重写自己的放行证据，汇总为它们单列了一栏「本次运行已触碰它」。两者已按本项目的
落点机制补齐（落点在 `report.resolve_report`，限样本写不入库目录、不得写放行证据），
**那一栏与那段特例说明随之失效并已删**。

本脚本自己的落点也双向守，**照 `tools/papers/report.py` 的机制写**：

| 层 | 判什么 | 触发 |
| :--- | :--- | :--- |
| `resolve_summary()` 正向 | 落点决策 | `limit > 0` 且落点与放行证据重合 → 改写走 + 判 FAIL |
| `resolve_summary()` 镜像 | 落点决策 | `limit <= 0` 且落点不是放行证据 → **改写回** + 判 FAIL |
| `recheck_summary()` | 紧贴 write 的复核 | 调用点被绕开时补判（正向只判 FAIL、不改写；镜像改写回） |
| 落盘后 sha256 对账 | 字节事实（兜底） | 限样本跑前后放行证据的 sha 必须相同 |

**为什么不能直接调 `report.resolve_report()`**：它的落点名是 `f"{kind}-report.txt"`，
而本任务的放行证据按计划与本任务书三处点名必须是 `tests/papers/reports/pilot-summary.txt`
——`kind` 取任何值都拼不出这个名。于是这里**照它的语义另写一份**，并在每次运行里
**当场对账**：`report.resolve_report("pilot-summary", limit)` 与 `resolve_summary(limit)`
必须走到**同一个分支**（正常放行 / 正常限样本 / 正向守卫 / 镜像守卫）。对账失败 ⇒ 红。
这条对账把「两份实现」的漂移风险变成一次运行内的判据，而不是留给下一个人去发现。

## 与 `report.py` 的其余口径逐条一致

`--limit` 在 argparse 层拒负数（同一处语义、两个入口，理由写在 `report.limit_arg`）；
报告一律 `write_bytes` + LF（`report.flush`）；只写仓库相对路径（`report.rel` +
`report.path_audit` 全文扫）；崩溃 traceback 过 `report.fmt_exc`；报告写入**无条件
执行**（放在 main 结尾、不在 try 内）。

## 复审后加严的五处（2026-09-26，全部是**加严**或**修错话**，无一处放宽）

1. **放行条件 ⑤ 真判数**（原先只判 `all-determinism.txt` 里含「跑前/跑后/43 份」三个
   词）。那三个词对**确定性结论免疫**：一次真非确定的 `cli all` 被如实落盘后，文件照样
   含这三个词，汇总照印 ✓、照写「可放行」。现在解析该文件的**最后一遍**那一节，要求
   `入库产物`/`md`/`figures`/`formulas` 四处读数**都是 0**，口径与命令见
   `check_determinism_counts`（教训 4.8：口径与命令只写在那一处）。
2. **产物的「自报失败」判据行加一支**（`CRIT_RX`）：原先只认 `名=FAIL`，而
   `verify_b/c/d` 三份产物**不用**这个形态（实测 ids 34 / map 16 / types 10 条，
   b/c/d/io/wm 全是 0）——它们用 `…: True|False`（`b-report.txt:56-58` 的
   「A2/A3/B1/B2 全通过: True」等，实测 3/1/1 条）。于是「产物里出现 FAIL 行、末行
   却仍写 `RESULT: PASS`」这一形态在那三份产物上**不受判**。现在两支都收。
3. **墙钟搬出放行证据**：逐脚本耗时原先写在 `pilot-summary.txt` 的正文里 ⇒ 放行证据
   **不是逐字节可重放的**（同一输入连跑两遍，8 个子脚本产物全同、汇总只差那几行）。
   现在耗时写进 `tests/papers/reports/all-timing.txt`（**测量记录**，全量跑每次重写），
   汇总里只**指向**它、不写秒数 ⇒ 放行证据恢复逐字节可重放。
4. **子脚本产物补一道绝对路径痕迹扫描**：六个脚本自扫（`verify_b.py:1087` 等），
   `verify_io.py`/`verify_wm.py` 当时一个都不扫（它们用 `traceback.format_exc()`；
   **2026-09-26 已改**：两者改用 `report.fmt_exc` 并自扫，见下段）。
   `check_evidence` 现在从**外面**补这一刀（不改冻结件）：产物全文过
   `report.path_audit`，非空即红。
5. **限样本分支的两处**：① 「本次运行未触碰放行证据」这句对**不支持 `--limit`** 的
   io/wm 不实（它们真跑了一次），改为**如实分栏**；② `pre == post` 在产物**缺失**时
   两边都是 `report.sha256_of` 的哨兵串 ⇒ 恒真，现在哨兵直接判红。另加 mtime 的
   **上界**（原先只判下界）。

## 2026-09-26 终审修复轮（B-1 / C-2，四处；全部是**加严**或**说清楚**）

1. **B-1 范围声明**：【5】加了 ⑦（放行证据自身入库，M-9）与【5b】——**两项人工目视
   闸门不在本汇总的判定范围内**，并把 C4 的机读值作为**报告量**摆出来（**登记它不构成
   判据**、不参与 ok/退出码）。起因：`verify_c.py` 的人工目视闸门**不并入 RESULT**，
   缺档时那份产物写「未判定 / 未放行」而 `RESULT` 仍是 `PASS`，而 `CRIT_RX` 两支都
   收不到那两行 ⇒ 「可放行」会被读成覆盖了目视项。**没有放宽任何判据**。
2. **M-1**：`CRIT_RX` 支 1 允许前导空白——原先**缩进的** `名=FAIL` 行两支都不收。
   实测八份产物**自报失败仍是 0 条**（不产生假红）。
3. **M-2**：`check_determinism_counts` 由 `hits[0]` 改为**取该标签下的全部行并取最严**
   ——原先取"最先出现的以标签开头的行"，生成器把「汇总 0」写在「明细非 0」前即
   **fail-open**。
4. **M-9**：加 `git_tracked(RELEASE)` 判据——放行证据**自己**原先没有任何护栏
   （`derive_stages` 排除自身、`check_record` 判的是它的兄弟记录）。
"""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent          # tests/papers
REPORTS = HERE / "reports"
LIMITED_DIR = HERE / "reports-limited"
RELEASE = REPORTS / "pilot-summary.txt"
ME = Path(__file__).resolve()
ME_NAME = ME.name
STAGE_GLOB = "verify_*.py"
# **Task 6b 的判据脚本**：它们在派生清单里的存在性单列一条回归守卫（D1 的失效形态
# 就是「清单被改回六项快照」——那两条会静默消失，汇总照样绿）。
REQUIRED_STAGES = ("verify_types.py", "verify_map.py")

BASELINE_PILOT = REPORTS / "origin-sha256-2025.txt"
BASELINE_ALL = REPORTS / "origin-sha256-all.txt"
PILOT = "2025美赛O奖论文"

# 外部实测记录（由 Task 7 实施者跑完 `cli` 后逐字写入；本脚本**只读并转抄**，
# 不重跑 `cli all`——它在本机实测约 10 分钟量级，放进每次汇总会让汇总不可运行）。
TIMING = REPORTS / "cli-timing.txt"
DETERMINISM = REPORTS / "all-determinism.txt"

# 逐阶段墙钟的落点（**测量记录，不是放行证据**）。全量跑每次重写它；限样本跑不写。
# 它是「放行证据逐字节可重放」的代价换来的：秒数是运行时刻的函数，**同一输入连跑两遍
# 本文件必然不同**，故它必须与放行证据分开——见模块 docstring 的第 3 条。
TIMING_DETAIL = REPORTS / "all-timing.txt"

# 两份**人工目视**存档（B-1）。它们**不在本汇总的判定范围内**，只作报告量转述：
# Task 2 的那份在 `verify_wm.py` 第 8 节是硬判据（缺了该脚本自己判 FAIL ⇒ 进 ①），
# C4 的那份在 `verify_c.py` **不并入 RESULT**（缺了 c-report.txt 会写「未放行」，
# 而它的 RESULT 仍可能是 PASS）——同一件事两个力道，故必须把机读值摆出来。
VISUAL_C4 = REPORTS / "c4-visual-confirm.txt"
VISUAL_WM = REPORTS / "wm-visual-confirm.txt"
# C4 目视闸门的机读值（由 `verify_c.py` 写进 `c-report.txt`）；取不到时**不判红**
# （它是报告量：任何取值都不改本汇总的 ok/退出码）。
C4_VIS_RX = re.compile(r"机读值 visual_ok=(True|False)")

# 子进程环境：**一律不写字节码**。本仓的判据链条从源码读，`__pycache__` 只会带来
# 第九例（陈旧字节码：`.pyc` 失效只看源文件 mtime 的整数秒 + 字节数）。汇总跑一次
# 会拉起八个子进程，留着它们写 `__pycache__` 等于给下一次改码实验埋雷。
CHILD_ENV = {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}

RESULT_RX = re.compile(r"^RESULT: (PASS|FAIL)(.*)$", re.M)
# 产物里**机器可读的判据行**，两种形态（加严：复审实测只认支 1 时，b/c/d 三份产物
# 是**零覆盖**——它们不用 `名=状态`，于是「产物里出现 FAIL 行而末行仍写 RESULT: PASS」
# 这一形态在那三份上不受判）：
#   支 1 `名=状态`：verify_ids / verify_map / verify_types 用（实测 34 / 16 / 10 条）；
#   支 2 `…: True|False`：verify_b / verify_c / verify_d 用（实测 3 / 1 / 1 条，例如
#     `b-report.txt:56` 的「A2/A3/B1/B2 全通过: True」）。
# **2026-09-26（M-1）**：支 1 原先锚 `^[A-Za-z]`，于是**缩进的** `名=FAIL` 行两支都不收
# （支 2 要求以 `: True|False` 收尾）⇒ 产物里一条缩进的失败行可以静静躺着。加 `[ \t]*`。
# **收不到的两行（不属于本判据，别以为它管）**：`verify_c.py` 的人工目视闸门缺档时，
# `c-report.txt` 会写 `C4 人工目视闸门: FAIL（未判定）` 与 `发布放行: **未放行**`——
# 前者不以 `: True|False` 收尾（是 `: FAIL（未判定）`），也不满足支 1（支 1 判的是 `名=状态`）；
# 后者既不是 `名=状态`、也不以 `: True|False` 收尾。**两支都不收**。
# 那不是本判据的漏洞而是**范围**：这两行不是「机器可读的判据行」，它们是**人工项的状态行**，
# 见【5】的范围声明。复核口径（可复现，不写会随编辑过期的计数）：
#   grep -nE '^[[:space:]]*[A-Za-z][A-Za-z0-9._-]*=(OK|FAIL)[[:space:]]*$|^.*:[[:space:]]*(True|False)[[:space:]]*$' tests/papers/reports/c-report.txt
# 只收机器可核判据行，不收上面那两行。
# **口径与 grep 写法同步改动**：下面 `check_evidence` 里打印的口径串是那两行 grep，
# 与这里的正则必须是同一件事（教训 4.8：口径只允许一处权威表述——它就在这两行）。
CRIT_RX = re.compile(
    r"^[ \t]*(?:[A-Za-z][A-Za-z0-9._-]*=(?P<eq>OK|FAIL)"
    r"|[^\n]*:\s*(?P<colon>True|False))\s*$",
    re.M)
# 打印进汇总的**等价 grep**（与 CRIT_RX 的两支一一对应，两式相加；改了上面必须改这里）。
CRIT_GREPS = (r"grep -cE '^[[:space:]]*[A-Za-z][A-Za-z0-9._-]*=(OK|FAIL)[[:space:]]*$'",
              r"grep -cE '^.*:[[:space:]]*(True|False)[[:space:]]*$'")


def crit_grep_idiom(path_rel: str) -> str:
    """上面那两支的**等价命令行**（口径串；两式相加 = `CRIT_RX` 的命中数）。

    **这个计数是报告量、不是判据**（B-1 的登记）：判据是 `crit_fails` 那一条
    （「产物内有**自报失败**的判据行」）。计数本身不参与 ok——它只回答"这份产物里
    有多少行是机器可读的判据行"。**它也不覆盖人工目视闸门的状态行**
    （`C4 人工目视闸门: FAIL（未判定）` / `发布放行: **未放行**` 两支都收不到，
    见 `CRIT_RX` 定义处；范围声明在【5b】）。
    """
    return " + ".join(f"`{g} {path_rel}`" for g in CRIT_GREPS)
# 确定性记录里的「最后一遍」节头（`## <跑前>.json → <跑后>.json`）与任一节头。
PASS_SECTION_RX = re.compile(r"^##\s+(?P<pre>\S+\.json)\s*→\s*(?P<post>\S+\.json)\s*$", re.M)
ANY_SECTION_RX = re.compile(r"^##\s", re.M)
CHANGED_RX = re.compile(r"变了\s*\**\s*(?P<n>\d+)")
# 那一节里要取数的四处（标签 → 判据：该节里以它开头的行）。`入库产物` 是汇总行，
# 另三处是逐类的对账行。
DET_LABELS = ("入库产物", "md", "figures", "formulas")
# 文件系统时间戳粒度：NTFS 是 100ns，取 1.0s 的容差只为覆盖极端情形（FAT 2s）。
MTIME_TOL = 1.0
MAX_SECONDS = 7200


# --------------------------------------------------------------------------
# 落点（照 tools/papers/report.py 写；分支对账见模块 docstring）
# --------------------------------------------------------------------------
def limited_path(limit: int) -> Path:
    return LIMITED_DIR / f"pilot-summary-limited-{limit}.txt"


def guard_path() -> Path:
    return LIMITED_DIR / "pilot-summary-落点守卫触发.txt"


def resolve_summary(limit: int) -> tuple[Path, str]:
    """落点 + 守卫消息（空串 = 未触发）。**两个方向都守**，语义逐条照
    `report.resolve_report`：正向把与放行证据重合的落点**改写走**；镜像把
    「全量跑却落在别处」的落点**改写回**放行证据。两处都判 FAIL。
    """
    out = limited_path(limit) if limit > 0 else RELEASE
    rel_ev = rel(RELEASE)
    if limit > 0 and out == RELEASE:
        return guard_path(), (
            f"落点守卫 FAIL：限样本跑（--limit {limit}）算出的落点与放行证据 {rel_ev} "
            f"重合——落点函数被改坏了。已改写到不入库目录，放行证据未被本次运行触碰。")
    if limit <= 0 and out != RELEASE:
        return RELEASE, (
            f"落点守卫 FAIL：全量跑（limit={limit}）算出的落点是 {rel(out)}，**不是**"
            f"放行证据 {rel_ev}——落点函数的全量分支被改坏了（这条是「限样本不得覆写"
            f"放行证据」那条的镜像）。已把落点改写回放行证据（全量跑必须拥有这份证据，"
            f"否则它会停在上一次的状态冒充本次结论），判 FAIL。")
    return out, ""


def recheck_summary(limit: int, out: Path) -> tuple[Path, str]:
    """写前落点复核（紧贴 `report.flush`）。语义照 `report.recheck_target`：
    正向只判 FAIL **不改写** out；镜像判 FAIL **并改写回**放行证据。"""
    rel_ev = rel(RELEASE)
    if limit > 0 and out == RELEASE:
        return out, (
            f"落点守卫 FAIL（写前复核）：限样本跑（--limit {limit}）的写入目标就是放行"
            f"证据 {rel_ev}——resolve_summary 的守卫在调用点被绕过了。判 FAIL。")
    if limit <= 0 and out != RELEASE:
        wrong = out
        return RELEASE, (
            f"落点守卫 FAIL（写前复核）：全量跑（limit={limit}）算出的写入目标是 "
            f"{rel(wrong)}，**不是**放行证据 {rel_ev}——落点判据被改坏或在调用点被绕过"
            f"了。已把落点改写回放行证据，判 FAIL。")
    return out, ""


def rel(p: Path) -> str:
    from tools.papers import report
    return report.rel(p)


def branch_of(out: Path, msg: str) -> str:
    """落点分支名（用于与 `report.resolve_report` 对账）。"""
    if msg:
        return "正向守卫" if out.parent == LIMITED_DIR else "镜像守卫"
    return "限样本落点" if out.parent == LIMITED_DIR else "放行证据"


def branch_crosscheck(limit: int, mine: Path, my_msg: str) -> tuple[bool, str]:
    """**两份实现的分支对账**：本文件照 `tools/papers/report.py` 另写了一份落点机制
    （因为它拼不出 `pilot-summary.txt` 这个名，见模块 docstring）。这里当场跑一遍
    原件，要求两者走**同一个分支**——mirror 漂移是这份复制品唯一的风险，把它变成
    一次运行内的判据。

    对账的粒度是**分支**（正常-全量 / 正常-限样本 / 正向守卫 / 镜像守卫），不比字节：
    两边的文件名按设计不同（`pilot-summary-report.txt` vs `pilot-summary.txt`）。
    """
    from tools.papers import report
    ref_out, ref_msg = report.resolve_report("pilot-summary", limit)
    ref_branch, my_branch = branch_of(ref_out, ref_msg), branch_of(mine, my_msg)
    same = ref_branch == my_branch
    return same, (
        f"落点机制的分支对账：`tools/papers/report.py` 走 **{ref_branch}** · "
        f"本脚本走 **{my_branch}** ⇒ {'一致' if same else '**不一致，判 FAIL**'}"
        f"（对账粒度是分支，不比文件名——两边的名字按设计不同）")


# --------------------------------------------------------------------------
# 【0】判据集：由磁盘派生
# --------------------------------------------------------------------------
def derive_stages() -> list[Path]:
    """`tests/papers/verify_*.py` 减去本文件自身（否则递归）。"""
    return sorted(p for p in HERE.glob(STAGE_GLOB) if p.resolve() != ME)


def check_stages(lines: list[str]) -> tuple[list[Path], bool]:
    ok = True
    lines.append(f"  派生命令（复用即复现）：`sorted(Path('tests/papers').glob('{STAGE_GLOB}'))`"
                 f" 减去本文件自身（`{ME_NAME}`，否则递归）")
    try:
        stages = derive_stages()
    except OSError as e:
        lines.append(f"  FAIL：派生抛异常（`{type(e).__name__}`）——判据集不可知，"
                     f"不得给出任何放行结论")
        return [], False
    if not stages:
        lines.append(f"  FAIL：派生结果**为空**——一个判据脚本都没有。"
                     f"「零依据地报绿」正是本项目栽过六次的形态，这里按 fail-closed 处理")
        return [], False
    lines.append(f"  派生到 **{len(stages)}** 个："
                 + " ".join(s.name for s in stages))
    missing_files = [s for s in stages if not s.is_file()]
    if missing_files:
        lines.append(f"  FAIL：派生出的路径不是文件：{[rel(s) for s in missing_files]}")
        ok = False
    names = {s.name for s in stages}
    for need in REQUIRED_STAGES:
        if need in names:
            lines.append(f"  Task 6b 的判据脚本在清单里：`{need}` ✓")
        else:
            lines.append(f"  FAIL：`{need}` **不在派生清单里**——Task 6b 的判据会被漏在"
                         f"放行评估之外，而汇总照样写「可放行」，那是**假放行**（D1）")
            ok = False
    return stages, ok


# --------------------------------------------------------------------------
# 【1】A1：原件哈希复核
# --------------------------------------------------------------------------
def read_baseline(path: Path) -> dict[str, str]:
    """基线文件 → {仓库相对路径: sha256}。空文件/坏行**抛**（不返回空表）。"""
    out: dict[str, str] = {}
    for ln in path.read_bytes().decode("utf-8").splitlines():
        if not ln.strip():
            continue
        h, k = ln.split("  ", 1)
        if len(h) != 64:
            raise ValueError(f"{rel(path)} 里有一行摘要长度不是 64：{ln[:40]!r}")
        out[k] = h
    if not out:
        raise ValueError(f"{rel(path)} 是空表——两份空表相等会让「原件未改动」"
                         f"凭空成立（本项目栽过）")
    return out


def diff_tables(base: dict[str, str], now: dict[str, str]) -> tuple[list, list, list]:
    missing = sorted(set(base) - set(now))
    added = sorted(set(now) - set(base))
    changed = sorted(k for k in set(base) & set(now) if base[k] != now[k])
    return changed, missing, added


def check_origin(lines: list[str]) -> bool:
    """A1：原件 sha256 与基线逐字相同。**A1 管的是「原件有没有被改动」**，
    它不判派生物、也不判判据——那是别的节的事。

    比计划强的一处：计划只核 `2025美赛O奖论文` 43 份（当时的范围），这里**全语料
    201 份一起核**（`origin-sha256-all.txt` 已在仓里）。两次都算在同一遍哈希上，
    省一次 1.7 GB 的读盘。
    """
    from tools.papers import io

    ok = True
    base_all = read_baseline(BASELINE_ALL)
    base_pilot = read_baseline(BASELINE_PILOT)
    colls = sorted({Path(k).parts[0] for k in base_all})
    lines.append(f"  基线：`{rel(BASELINE_ALL)}` {len(base_all)} 条（{len(colls)} 个合集）· "
                 f"`{rel(BASELINE_PILOT)}` {len(base_pilot)} 条")
    lines.append(f"  基线里的合集：{' · '.join(colls)}")

    now: dict[str, str] = {}
    for c in colls:
        try:
            now.update(io.sha256_tree(c))
        except (OSError, ValueError) as e:
            lines.append(f"  FAIL：读不到合集 {c!r} 的原件哈希：{type(e).__name__}"
                         f"（`io.sha256_tree` 对不存在的合集**抛**而不是返回空表，"
                         f"这里照收）")
            ok = False
    if not ok:
        return False

    changed, missing, added = diff_tables(base_all, now)
    lines.append(f"  A1（全语料）：基线 {len(base_all)} 份 / 现在 {len(now)} 份 · "
                 f"改动 {changed or '无'} · 缺失 {missing or '无'} · 新增 {added or '无'}")
    ok &= not changed and not missing and not added

    sub = {k: v for k, v in now.items() if Path(k).parts[0] == PILOT}
    if set(base_pilot) - set(now):
        lines.append(f"  FAIL：试点基线的键没被全语料基线覆盖："
                     f"{sorted(set(base_pilot) - set(now))[:3]}")
        ok = False
    else:
        c2, m2, a2 = diff_tables(base_pilot, sub)
        lines.append(f"  A1（试点 {PILOT}）：基线 {len(base_pilot)} 份 / 现在 {len(sub)} 份 · "
                     f"改动 {c2 or '无'} · 缺失 {m2 or '无'} · 新增 {a2 or '无'}")
        ok &= not c2 and not m2 and not a2

    lines.append(f"  A1 结论：{'原件一字未动（全语料）' if ok else '**原件被改动**'}")
    return ok


# --------------------------------------------------------------------------
# 【2】逐脚本：退出码 + RESULT 行 + 放行证据产物
# --------------------------------------------------------------------------
def stage_evidence(stage: Path) -> Path:
    """`verify_X.py` → `tests/papers/reports/X-report.txt`。

    **命名是约定、不是机制**（各脚本自己决定写哪一份）。这里把约定写成一条
    可核的事实：文件不存在 ⇒ 该脚本这一轮没有留下任何入库产物 ⇒ 红。
    """
    name = stage.stem
    if name.startswith("verify_"):
        name = name[len("verify_"):]
    return REPORTS / f"{name}-report.txt"


def supports_limit(stage: Path) -> bool:
    """当场探测该脚本接不接受 `--limit`（`--help` 里有没有这一项）。

    **这是行为探测，不是读自称**：`--help` 的内容由该脚本自己的 argparse 现场
    生成，探测的是「传 `--limit` 会不会被拒」。探测结果逐项打印进汇总。

    ⚠ **一处已知形态**（登记，判据不动——它往 fail-closed 方向倒，不产生假绿）：

    ① 判的是「`--help` 的 stdout 里有没有 `--limit` 这个**字符串**」。若哪天某份报告
       的正文里出现「本脚本不支持 `--limit`」这样的句子，它会被读成「支持」，于是限
       样本跑会给它传 `--limit N`。**后果不是假绿**：真 argparse 的脚本当场报错
       （退出码非 0 ⇒ 红）；唯一的例外形态是「自称支持、实际忽略 argv」的脚本——
       那种脚本会照跑并写进自己的**限样本落点**，而 `check_evidence` 还会去核那份
       落点文件存在且带 `LIMITED` 标记（缺 ⇒ 红）。形态如此，登记在此。

    **2026-09-26 起本探测的适用面变了**：原先 `verify_io.py` / `verify_wm.py` 不解析
    argv，对它们传 `--help` **等于真跑一次**（且发生在本次运行的 t0 **之前** ⇒ 探测
    阶段就把自己的放行证据重写了）。A-2 给两者加了 argparse，**这一形态不存在了**：
    现在 8 个脚本一律解析 argv，`--help` 是纯打印、不触碰任何产物。`check_evidence`
    的限样本分支据此改回与其它脚本一致的表述（不再有「本次运行已触碰它」那一栏）。
    """
    try:
        p = subprocess.run([sys.executable, str(stage), "--help"],
                           capture_output=True, timeout=120, cwd=str(ROOT),
                           env={**_env(), "PYTHONIOENCODING": "utf-8"})
    except (OSError, subprocess.SubprocessError):
        return False
    return b"--limit" in p.stdout


def _env() -> dict:
    import os
    return {**os.environ, **CHILD_ENV}


def run_sub(stage: Path, limit: int, can_limit: bool) -> dict:
    argv = [sys.executable, str(stage)]
    if limit > 0 and can_limit:
        argv += ["--limit", str(limit)]
    t0 = time.time()
    try:
        p = subprocess.run(argv, capture_output=True, timeout=MAX_SECONDS,
                           cwd=str(ROOT), env=_env())
        rc: int | None = p.returncode
        out_b, err_b = p.stdout, p.stderr
        note = ""
    except subprocess.TimeoutExpired:
        rc, out_b, err_b = None, b"", b""
        note = f"**超时**（>{MAX_SECONDS}s）——按 FAIL 处理"
    return {"argv": argv, "rc": rc, "out": out_b, "err": err_b,
            "dt": time.time() - t0, "t0": t0, "note": note}


def decode(raw: bytes) -> tuple[str, str]:
    """子进程输出 → 文本。**解码失败不吞**：`errors='replace'` 会让「逐字转抄」
    变成「转抄一串替换符」，那比红更坏。解不出来就返回可辨识的标记，由调用方判红。
    """
    try:
        return raw.decode("utf-8"), ""
    except UnicodeDecodeError as e:
        return "", f"子进程输出不是合法 UTF-8（{e}）——「逐字转抄」无法成立"


def last_result(text: str) -> str:
    """`RESULT:` 行逐字（最后一条；没有则空串）。"""
    ms = RESULT_RX.findall(text)
    if not ms:
        return ""
    # findall 只给了分组，取原文那一段。
    lines = [ln for ln in text.splitlines() if ln.startswith("RESULT: ")]
    return lines[-1] if lines else ""


def check_one_stage(lines: list[str], stage: Path, limit: int, meta: dict) -> bool:
    ok = True
    can = supports_limit(stage)
    ev = stage_evidence(stage)
    pre = report_sha(ev) if limit > 0 else ""
    r = run_sub(stage, limit, can)
    out_txt, dec_err = decode(r["out"])
    # 墙钟**不进本汇总**（A-3：放行证据必须逐字节可重放）。它只随 meta 走去
    # `all-timing.txt`——那一份是测量记录，见模块 docstring 第 3 条。
    meta.setdefault("timing", []).append((stage.name, r["dt"], r["rc"], can))

    lines.append("")
    lines.append(f"· `{stage.name}`　支持 --limit：{'是' if can else '否'}　"
                 f"退出码 {r['rc']}")
    if r["note"]:
        lines.append(f"  FAIL：{r['note']}")
        ok = False
    if dec_err:
        lines.append(f"  FAIL：{dec_err}")
        ok = False

    res_out = last_result(out_txt)
    if not res_out:
        lines.append(f"  FAIL：stdout 里没有 `RESULT:` 行——汇总不得替它给结论"
                     f"（fail-closed）")
        ok = False
    else:
        lines.append(f"  stdout 的 RESULT 行（**逐字**）：`{res_out}`")

    # ---- 退出码 vs RESULT 行：矛盾即红（D5 ③）----
    if res_out and r["rc"] is not None:
        says_pass = res_out.startswith("RESULT: PASS")
        if r["rc"] == 0 and not says_pass:
            lines.append(f"  FAIL：退出码 0 却写着 `{res_out}`——**退出码与它自己的 "
                         f"RESULT 行矛盾**（判据说了话而结论不听，正是本项目假绿家族的形态）")
            ok = False
        elif r["rc"] != 0 and says_pass:
            lines.append(f"  FAIL：退出码 {r['rc']} 却写着 `{res_out}`——同上，矛盾即红")
            ok = False
    if r["rc"] not in (0, None):
        lines.append(f"  退出码非 0 ⇒ 该阶段未通过（RESULT 行照抄如上）")
        ok = False

    # ---- 产物侧：放行证据文件（D5 的正题：不读自称，读产物）----
    ok &= check_evidence(lines, stage, ev, res_out, limit, pre,
                         r["t0"], r["t0"] + r["dt"], can)
    return ok


def report_sha(p: Path) -> str:
    from tools.papers import report
    return report.sha256_of(p)


def missing_sha_sentinel() -> str:
    """`report.sha256_of` 对「读不出来」的返回值（`"<不存在>"`）。

    **不抄那串字面量**：`report.py` 是冻结件，它改了名这个判据会**静默失配**（就又
    变回恒真）。这里当场拿一个必然读不出来的路径问它一遍——`tests/papers/` 这个
    **目录**本身：`read_bytes` 在任何平台上都抛 `OSError`（Linux 抛
    `IsADirectoryError`、Windows 抛 `PermissionError`，都是 `OSError` 的子类）。
    """
    from tools.papers import report
    return report.sha256_of(HERE)


def crit_fails(text: str) -> list[str]:
    """产物里**自报失败**的判据行（两种形态都收：`名=FAIL` 与 `…: False`）。"""
    out = []
    for ln in text.splitlines():
        m = CRIT_RX.match(ln)
        if m and (m.group("eq") == "FAIL" or m.group("colon") == "False"):
            out.append(ln)
    return out


def check_evidence(lines: list[str], stage: Path, ev: Path, res_out: str,
                   limit: int, pre: str, t0: float, t_exit: float,
                   can_limit: bool) -> bool:
    """放行证据（入库产物）侧的复核。全量跑与限样本跑判的东西不同。

    `t0` / `t_exit` = 该子脚本这一次的**启动**与**退出**时刻（下界 + 上界都判：
    只判下界时，任何一份**未来时间戳**的文件都算「本次写的」）。
    """
    from tools.papers import report

    ok = True
    if limit > 0:
        post = report_sha(ev)
        sent = missing_sha_sentinel()
        same = pre == post
        # **哨兵不是摘要**：产物缺失时两边都是 `report.sha256_of` 的哨兵串，
        # 「相同」是空比对（恒真），什么都没证 ⇒ 直接判红（第七例家族）。
        if pre == sent or post == sent:
            lines.append(f"  产物 `{rel(ev)}`：限样本跑前/后 sha256 = `{pre}` / `{post}`"
                         f" ⇒ **FAIL（哨兵串不是摘要）**")
            lines.append(f"    FAIL：本脚本的放行证据本次**读不出来**（不存在或读不了）——"
                         f"「跑前 == 跑后」在这种情形下是**空比对（恒真）**，什么都证不了")
            return False
        # **如实分栏**（m-1）：对支持 `--limit` 的脚本才敢说「未触碰放行证据」；
        # 不支持的那一类本次**已经**碰过它，那一栏必须明说。
        # **2026-09-26（A-2）**：原先这里点名 `verify_io.py` / `verify_wm.py`——它们
        # 现在有了 argparse 与落点机制，不再走这一栏（`supports_limit` 对它们返回
        # 「支持」，且 `--help` 不再等于真跑一次）。**不留一段描述已不存在状态的文字**：
        # 措辞改回与其它脚本一致，分栏结构保留（将来再有脚本不接 `--limit` 时仍成立）。
        if can_limit:
            note = ("相同 ✓（本脚本支持 `--limit`，本次跑的是限样本分支，"
                    "放行证据未被本次运行触碰）" if same else "**不同 ⇒ FAIL**")
        else:
            note = ("相同 ✓（**但本次运行已触碰它**：本脚本不支持 `--limit`，限样本跑里"
                    "它仍全量跑并重写自己那份证据——同样的字节才允许）"
                    if same else "**不同 ⇒ FAIL**")
        lines.append(f"  产物 `{rel(ev)}`：限样本跑前/后 sha256 {note}")
        if not same:
            lines.append(f"    FAIL：限样本跑重写了放行证据（{pre} → {post}）")
            ok = False
        if not can_limit:
            lines.append(f"    注：本脚本不支持 `--limit`，限样本跑里它仍全量跑并重写"
                         f"自己那份证据——**同样的字节才允许**，上面判的就是这个。")
        else:
            lim = LIMITED_DIR / f"{stage.stem[len('verify_'):]}-report-limited-{limit}.txt"
            if not lim.is_file():
                lines.append(f"    FAIL：限样本跑的落点 `{rel(lim)}` 不存在——"
                             f"要么它没接 `--limit`，要么它把限样本结论写到了别处")
                ok = False
            else:
                t = lim.read_bytes().decode("utf-8", "replace")
                rl = last_result(t)
                good = "(LIMITED" in rl
                lines.append(f"    限样本落点 `{rel(lim)}` 的 RESULT 行：`{rl}`"
                             f" ⇒ {'带 LIMITED 标记 ✓' if good else '**缺 LIMITED 标记 ⇒ FAIL**'}")
                ok &= good
        return ok

    # 全量跑
    if not ev.is_file():
        lines.append(f"  FAIL：放行证据 `{rel(ev)}` 不存在——这个脚本本轮没有留下任何"
                     f"入库产物，汇总不得据它的 stdout 给结论")
        return False
    mtime = None
    try:
        mtime = ev.stat().st_mtime
    except OSError:
        pass
    fresh = mtime is not None and mtime + MTIME_TOL >= t0
    # **上界**（m-3）：这一条原先只判下界，于是「时间戳落在未来」的文件也算本次写的。
    # 免费的加严：该子脚本本次的退出时刻已在手（`t_exit`）。
    not_future = mtime is not None and mtime <= t_exit + MTIME_TOL
    lines.append(f"  产物 `{rel(ev)}`：存在 ✓ · 本次运行内重写 = {fresh}"
                 f"（判据：**启动时刻 ≤** mtime **≤ 退出时刻**，两侧容差 {MTIME_TOL}s "
                 f"覆盖文件系统时间戳粒度；只判下界时未来时间戳也能冒充）· "
                 f"上界内 = {not_future}")
    if not fresh:
        lines.append(f"    FAIL：这份放行证据**不是本次跑写出来的**——「上一次的 "
                     f"RESULT: PASS 留在库里冒充本次结论」正是本项目栽过六次的形态")
        ok = False
    if not not_future:
        lines.append(f"    FAIL：这份放行证据的 mtime **晚于**该子脚本的退出时刻"
                     f"（> t_exit + {MTIME_TOL}s）——时间戳在未来，它不是一次正常落盘")
        ok = False
    ev_txt = ev.read_bytes().decode("utf-8", "replace")
    # **绝对路径痕迹扫描**（A-4：从外面补这一刀，不改冻结件）。六个子脚本自己扫，
    # `verify_io.py` / `verify_wm.py` 一个都不扫（它们用 `traceback.format_exc()`，
    # 崩溃那一次会把机器相关绝对路径写进入库产物）。判的是**产物全文**。
    dirty = report.path_audit(ev_txt)
    lines.append(f"  产物全文的绝对路径痕迹扫描（`report.path_audit`，口径与各子脚本"
                 f"自扫的那条相同）：{report.scrub(dirty) if dirty else '干净 ✓'}")
    if dirty:
        lines.append(f"    FAIL：入库产物里出现机器相关绝对路径痕迹 "
                     f"{report.scrub(repr(dirty))}——违反「报告只带仓库相对路径」")
        ok = False
    ev_res = last_result(ev_txt)
    bare = ev_res == "RESULT: PASS"
    lines.append(f"  产物里的 RESULT 行：`{ev_res or '<无>'}`"
                 f" ⇒ {'**裸的 RESULT: PASS** ✓（带 LIMITED 后缀的一律不算）' if bare else 'FAIL'}")
    if not bare:
        lines.append(f"    FAIL：入库放行证据的末行不是裸的 `RESULT: PASS`——"
                     f"它要么是红的，要么是限样本跑写的（两种都不构成放行依据）")
        ok = False
    if res_out and ev_res and res_out != ev_res:
        lines.append(f"    FAIL：stdout 的 RESULT 行与产物的**逐字不同**"
                     f"（`{res_out}` vs `{ev_res}`）——两者必须同一份")
        ok = False
    # **两种形态都收**（A-2）：只认 `名=FAIL` 时，b/c/d 三份产物零覆盖——它们的判据行
    # 形态是 `…: True|False`，于是「产物里出现 FAIL 行、末行却仍写 RESULT: PASS」这一
    # 形态（判据说了话而结论不听）在那三份上不受判。
    fails = crit_fails(ev_txt)
    if fails:
        lines.append(f"    FAIL：产物内有**自报失败**的判据行 {len(fails)} 条"
                     f"（口径：{crit_grep_idiom(rel(ev))} 命中且状态为 FAIL/False）："
                     f"{fails[:3]}")
        ok = False
    n_crit = len(CRIT_RX.findall(ev_txt))
    lines.append(f"  判据行计数（口径：{crit_grep_idiom(rel(ev))}，两式相加）：**{n_crit}**"
                 + ("" if n_crit else "（本脚本的报告两种形态都不用，计数不适用）")
                 + "　← **本行是报告量，不构成判据**：判据是上面那条「产物内有自报失败"
                   "的判据行」（只对状态为 FAIL/False 的行判红）；本行既不参与 ok，"
                   "也不覆盖人工目视闸门的状态行（见【5b】）")
    return ok


# --------------------------------------------------------------------------
# 【3】Task 6b 的产物与其判据（D7）
# --------------------------------------------------------------------------
SIX_B = (
    ("corpus/papers/PROBLEM_TYPES.md", "人工撰写的题型标注本体（**不由脚本生成**）"),
    ("corpus/papers/MODEL_MAP.md", "题型 → 模型/算法 配对表（`model_map.build` 生成）"),
    ("tools/papers/vocab/growth_triage.txt", "词表增长候选的三态分流表"),
    ("tools/papers/vocab/body_triage.txt", "正文扫描跨篇 token 的三态分流表（同格式）"),
)


def check_6b(lines: list[str]) -> bool:
    ok = True
    lines.append("  Task 6b 的三样交付**不在计划的六项阶段里**，它们的判据脚本是 "
                 "`verify_types.py`（题型标注）与 `verify_map.py`（配对表 + 两张分流表）：")
    for relp, what in SIX_B:
        p = ROOT / relp
        if not p.is_file():
            lines.append(f"  FAIL：`{relp}` 不存在——{what}")
            ok = False
            continue
        lines.append(f"  · `{relp}`　{what}；blob `{git_blob(p)}`"
                     f"（口径：`git hash-object {relp}`）")
    lines.append("  判据落点：`verify_types.py` → `" + rel(stage_evidence(HERE / "verify_types.py"))
                 + "`；`verify_map.py` → `" + rel(stage_evidence(HERE / "verify_map.py")) + "`")
    return ok


def git_blob(p: Path) -> str:
    """工作树文件 → **git blob 哈希**（不是裸 sha256）。

    本仓 `core.autocrlf=true`：工作树字节与入库字节可能不同，"入库的是哪一串"
    只有 git 知道。故凡陈述「这份产物的 blob 是 X」一律走 `git hash-object`
    （`corpus/papers/**` 虽有 `-text` 规则、两者应相等，但**口径不依赖那个规则
    成立**）。取不到时返回哨兵串，由调用方照常打印（缺失本身要能被看见）。
    """
    try:
        r = subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                           timeout=60, cwd=str(ROOT))
        if r.returncode == 0:
            return r.stdout.decode("ascii", "replace").strip()
        return f"<git hash-object 退出码 {r.returncode}>"
    except (OSError, subprocess.SubprocessError) as e:
        return f"<git 不可用：{type(e).__name__}>"


# --------------------------------------------------------------------------
# 【4】外部实测记录（耗时 / 抽取确定性）
# --------------------------------------------------------------------------
def check_record(lines: list[str], path: Path, what: str, expect_phrases: tuple) -> bool:
    """两份「跑完 cli 才写得出」的记录：本脚本**只读并逐字转抄**。

    它们是**产物**（由实际那次运行落盘），不是本脚本的自称；本脚本判的是
    ① 文件在库 ② 它被 git 跟踪（不入库的残余等于丢失，D9）③ 里面含的短语齐
    ④ 记的份数 == 磁盘上该合集的 PDF 份数（当场数出来的——手抄的数在这一条上会红）
    ⑤ 不含 `LIMITED`（限样本跑的记录不得当放行依据）。
    """
    from tools.papers import io
    ok = True
    if not path.is_file():
        lines.append(f"  FAIL：`{rel(path)}` 不存在——{what}")
        return False
    txt = path.read_bytes().decode("utf-8", "replace")
    n_pdf = len(sorted((io.ORIGIN / PILOT).rglob("*.pdf")))
    lines.append(f"  `{rel(path)}`　{what}")
    tracked = git_tracked(path)
    lines.append(f"    git 跟踪 = {tracked}（口径：`git ls-files --error-unmatch {rel(path)}`）"
                 f"——不入库的残余等于丢失（D9）")
    if not tracked:
        lines.append(f"    FAIL：这份记录**没入库**")
        ok = False
    for phrase in expect_phrases + (f"{n_pdf} 份",):
        hit = phrase in txt
        lines.append(f"    含 `{phrase}` = {hit}"
                     + ("（份数是**当场从磁盘数出来的**，不是手抄的）"
                        if phrase == f"{n_pdf} 份" else ""))
        ok &= hit
    n_bad = re.findall(r"LIMITED", txt)
    lines.append(f"    出现 `LIMITED` {len(n_bad)} 处（限样本跑的记录不得当放行依据）")
    if n_bad:
        ok = False
    return ok


def read_last_pass(txt: str) -> tuple[str, str, str] | None:
    """`all-determinism.txt` 里**最后一遍**那一节 → `(节头, 节体, 上一节头)`。

    「最后一遍」= 最后一个节头形态为 `## <跑前>.json → <跑后>.json` 的 `## ` 节
    （尾部的「结论」等非 `→` 节头不算）。一节都没有 ⇒ `None`（调用方判红）。
    节体 = 该节头到**下一个任意 `## ` 节头**（或文件末）之间的原文。
    """
    starts = [m.start() for m in ANY_SECTION_RX.finditer(txt)]
    pick = None
    for pos in starts:
        if PASS_SECTION_RX.match(txt, pos):
            pick = pos
    if pick is None:
        return None
    after = [p for p in starts if p > pick]
    stop = after[0] if after else len(txt)
    head = txt[pick:stop].splitlines()[0].strip()
    return head, txt[pick:stop], head


def check_determinism_counts(lines: list[str], path: Path) -> bool:
    """放行条件 ⑤ 的**判数**（A-1 的加严）：最后一遍那一节的四处读数必须都是 0。

    **为什么非加不可**：原先这条条件只判「文件在 + 含『跑前』『跑后』『43 份』」——
    那三个词对**确定性结论免疫**。一次真非确定的 `cli all` 被如实落盘后，文件照样含
    这三个词 ⇒ 汇总照印 ✓、照写「可放行」。**口径与命令**（教训 4.8：一处权威表述，
    就在这里；汇总里印的也是这里出来的那几句）：

      口径：取 `tests/papers/reports/all-determinism.txt` 里**最后一遍**那一节
            （节头 `## <跑前>.json → <跑后>.json`，取**最后一个**这样的一节）；
            在该节里取四处读数 —— `入库产物` / `md` / `figures` / `formulas`，
            读数 = 该标签下**每一行**里 `变了` 之后的那个**整数**（`blob 变了 **0** 份`
            与 `blob 变了 0` 两种写法都取；一个标签下有多行时**取最严**：任一非 0 即红，
            不取「最先出现的那一行」——M-2）；
            四处的每一行**都必须是 0**。
      命令：`python tests/papers/verify_all.py`（本判据每次都跑）；
            只看那四行：`grep -E '变了' tests/papers/reports/all-determinism.txt | tail -4`
      fail-closed：文件读不了 / 一节都没有 / 某处无行 / 某行无数 ⇒ 红。
    """
    ok = True
    lines.append("  抽取确定性**判数**（A-1：条件 ⑤ 原先只判「文件在 + 含三个词」，"
                 "对确定性结论免疫——一份如实记录了非确定的记录照样含那三个词）：")
    lines.append(f"    口径：`{rel(path)}` 的**最后一遍**那一节（节头 "
                 f"`## <跑前>.json → <跑后>.json`，取**最后一个**这样的一节；"
                 f"节体到下一个任意 `## ` 节头为止）；取四处读数 —— "
                 f"{' / '.join('`' + x + '`' for x in DET_LABELS)}，"
                 f"读数 = 该标签下**每一行**里 `变了` 之后的整数（`blob 变了 **0** 份` 与 "
                 f"`blob 变了 0` 两种写法都取；多行时**取最严**、任一非 0 即红）；"
                 f"四处的每一行**都必须是 0**")
    lines.append(f"    命令（复用即复现）：`python {rel(ME)}`；只看那四行："
                 f"`grep -E '变了' {rel(path)} | tail -4`；"
                 f"fail-closed：读不了 / 无节 / 某处无行 / 某行无数 ⇒ 红")
    try:
        txt = path.read_bytes().decode("utf-8", "replace")
    except OSError as e:
        lines.append(f"    FAIL：读不到 `{rel(path)}`（`{type(e).__name__}`）")
        return False
    got = read_last_pass(txt)
    if got is None:
        lines.append(f"    FAIL：文件里找不到「跑前 → 跑后」这样的一节（节头形态 "
                     f"`## <a>.json → <b>.json`）——没有可比的一遍，"
                     f"「确定性」这条放行条件无从判数")
        return False
    head, body, _ = got
    lines.append(f"    最后一遍那一节：`{head}`")
    for label in DET_LABELS:
        hits = [ln for ln in body.splitlines() if ln.strip().startswith(label)]
        if not hits:
            lines.append(f"    FAIL：这一节里找不到 `{label}` 那一行——读数取不到")
            ok = False
            continue
        # **取该标签下的全部行并取最严**（2026-09-26，M-2）。原先 `hits[0]` 取的是
        # 「先出现的、以该标签开头的行」——生成器若把「汇总 0 份」写在「明细非 0」之前，
        # 判据就取到 0，方向是 **fail-open**。现在：任一行的读数非 0 ⇒ 红；
        # 任一行取不到读数 ⇒ 也红（同一条 fail-closed 纪律）。
        reads: list[int | None] = []
        for ln in hits:
            m = CHANGED_RX.search(ln)
            if m is None:
                lines.append(f"    FAIL：`{label}` 的一行里没有可取的读数"
                             f"（找不到 `变了 <n>`）：`{ln.strip()}`")
                reads.append(None)
                continue
            n = int(m.group("n"))
            reads.append(n)
            lines.append(f"    {label}：变了 **{n}** ⇒ {'0 ✓' if n == 0 else '**非 0 ⇒ FAIL**'}"
                         f"　原文：`{ln.strip()}`")
        if len(hits) > 1:
            lines.append(f"    ↑ `{label}` 在这一节里有 **{len(hits)}** 行 ⇒ 判据取**最严**"
                         f"（任一非 0 或取不到读数即红），不取「最先出现的那一行」")
        if any(n is None or n != 0 for n in reads):
            ok = False
    lines.append(f"    判据结论：{'四处读数全为 0 ⇒ 这一条才成立' if ok else '**有非 0 或取不到 ⇒ 判红**'}"
                 f"（范围与本汇总其余各条一致：**2025 试点 43 份**这条流水线）")
    return ok


def timing_detail_text(meta: dict, started: float, now: float) -> str:
    """逐阶段墙钟的落盘文本（**测量记录**，不是放行证据；见模块 docstring 第 3 条）。

    落点 = `tests/papers/reports/all-timing.txt`，**只由全量跑写**；限样本跑碰它即红
    （判在 `main()` 里，紧贴写入处）。
    """
    rows = meta.get("timing") or []
    out = [
        "全量跑的逐阶段墙钟耗时（Task 7 · A-3：从放行证据里搬出来的那一份）",
        "=" * 78,
        "**为什么单独一份**：秒数是**运行时刻的函数**——同一输入连跑两遍，八个子脚本的",
        "产物逐字节相同，而这一份必然不同。它原先写在放行证据",
        "`tests/papers/reports/pilot-summary.txt` 的正文里，于是那一份**不是逐字节可重放的**",
        "（复审实测：两遍只差那几行、sha256 随之改变）——那不是「放行证据」该有的性质。",
        "搬到这里之后：放行证据恢复逐字节可重放，本文件**不追求可重放**。",
        "**读它的纪律**：测量记录，不是结论、不是放行依据。超时判据（>7200s 按 FAIL）在",
        "`tests/papers/verify_all.py` 的 `run_sub` 里，与本文件无关。",
        "",
        f"复现命令：`PYTHONDONTWRITEBYTECODE=1 python {rel(ME)}`"
        f"（全量跑写本文件；限样本跑不写它）",
        "",
        "子脚本墙钟（**不含**本脚本自己的核对开销：A1 全语料哈希复核 + 逐份 `problem_of` +",
        "八个子进程的调度。那一段 ≈ 下面的总墙钟 − 下表之和）：",
        "",
        "| 子脚本 | 支持 `--limit` | 退出码 | 墙钟 |",
        "| :--- | :--- | ---: | ---: |",
    ]
    if not rows:
        out.append("| （本次运行一个子脚本都没跑——见汇总【0】：判据集为空） | | | |")
    for name, dt, rc, can in rows:
        out.append(f"| `{name}` | {'是' if can else '否'} | {rc} | {dt:.1f}s |")
    out.append(f"| 合计（{len(rows)} 个子脚本） | | | {sum(r[1] for r in rows):.1f}s |")
    out.append("")
    out.append(f"本脚本本次总墙钟：{now - started:.1f}s"
               f"（= 上表 + 【1】A1 复核 + 【6】R6 的当场测量）")
    out.append("")
    return "\n".join(out)


def git_tracked(p: Path) -> bool:
    try:
        r = subprocess.run(["git", "ls-files", "--error-unmatch", "--", rel(p)],
                           capture_output=True, timeout=60, cwd=str(ROOT))
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


# --------------------------------------------------------------------------
# 【6】R6：扩到全量 201 份的前置，当场量
# --------------------------------------------------------------------------
def check_release_tracked(lines: list[str]) -> bool:
    """M-9：**放行证据自己**也要受版本控制（D9：不入库的残余等于丢失）。

    `derive_stages` 排除本文件自身、`check_record` 判的是它的两份兄弟记录是否 git
    受控——**都不管 `RELEASE` 自己**。于是「把 `RELEASE` 常量改成别的名字」这一手会让
    新名字的文件（未入库）写「可放行」、入库的旧 `pilot-summary.txt` 留着旧的
    `RESULT: PASS`，**两者都不红**。这一行即堵住。
    """
    tracked = git_tracked(RELEASE)
    lines.append(f"  放行证据自身入库 = {tracked}"
                 f"（口径：`git ls-files --error-unmatch {rel(RELEASE)}`）"
                 f"——不入库的残余等于丢失（D9）")
    if not tracked:
        lines.append(f"    FAIL：放行证据 `{rel(RELEASE)}` **没入库**——换落点/改名之后"
                     f"新文件不受版本控制、旧文件留着上一次的 `RESULT: PASS`，"
                     f"两者都不红")
        return False
    return True


def check_r6(lines: list[str]) -> None:
    """R6：`io.problem_of` 对三类目录布局取不到题号。

    `recon/ids-recon.txt` 的编者按 ① 登记过三个数（2024 全年 35/35、2023 春季赛
    5/42、UMAP 37/37）。**登记不等于测量**，这里当场逐份跑一遍 `problem_of`，
    把实测数打出来——本轮实测与登记逐个相同（差异会当场显形，不去迁就登记）。
    """
    from tools.papers import io
    total = bad_total = 0
    cols = sorted(p for p in io.ORIGIN.iterdir() if p.is_dir())
    for c in cols:
        pdfs = sorted(c.rglob("*.pdf"))
        bad = 0
        for p in pdfs:
            try:
                io.problem_of(str(p.relative_to(io.ORIGIN)))
            except ValueError:
                bad += 1
        total += len(pdfs)
        bad_total += bad
        lines.append(f"  {c.name}：PDF {len(pdfs)} 份 · `problem_of` 取不到题号 **{bad}** 份")
    lines.append(f"  合计 PDF **{total}** 份 · 取不到题号 **{bad_total}** 份 · "
                 f"取得到 **{total - bad_total}** 份"
                 f"（口径：本函数当场对磁盘逐份调 `io.problem_of`）")
    if bad_total:
        lines.append(f"  **结论：扩到全量 201 份的前置条件未满足**——"
                     f"`problem_of` 在 {bad_total} 份上取不到题号（未定义口径），"
                     f"索引在这 {bad_total} 份上跑不起来。本条**不判 FAIL**（它不是本轮"
                     f"范围的判据），但它**不因本汇总的 PASS 而消失**：Task 9 扩语料前"
                     f"必须先定题号口径（R6）。")
    else:
        lines.append(f"  结论：全语料 {total} 份题号全可取 ⇒ 扩语料无这一道阻碍。"
                     f"（实测如此时才这么写。）")
    return


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def checks(lines: list[str], limit: int, started: float, meta: dict) -> bool:
    ok = True
    lines.append(f"运行口径：**{'限样本跑 --limit %d' % limit if limit > 0 else '全量跑'}**"
                 f"（{'限样本跑的结论**不是放行依据**' if limit > 0 else '放行证据只有全量跑会写'}）")
    lines.append("")

    lines.append("【0】判据集：由磁盘派生（D1）")
    stages, ok0 = check_stages(lines)
    ok &= ok0

    lines.append("")
    lines.append("【1】A1 原件哈希复核（流水线全程不得改动原件）")
    try:
        ok &= check_origin(lines)
    except (OSError, ValueError, KeyError) as e:
        lines.append(f"  FAIL：A1 复核本身抛异常（`{type(e).__name__}`）——"
                     f"**算不出来不等于没改**，按 FAIL 处理")
        ok = False

    lines.append("")
    lines.append("【2】逐脚本：退出码 + RESULT 行（逐字）+ 放行证据产物核对（D5）")
    lines.append(f"  **逐脚本墙钟不在本文件里**（A-3）：秒数是运行时刻的函数，写进来本文件就"
                 f"不可逐字节重放了。各阶段耗时见 `{rel(TIMING_DETAIL)}`"
                 f"（**测量记录、不是放行证据**；只由全量跑写，限样本跑碰它即判 FAIL）。")
    if not stages:
        lines.append("  FAIL：判据集为空（见【0】），没有可跑的脚本")
        ok = False
    for st in stages:
        ok &= check_one_stage(lines, st, limit, meta)

    lines.append("")
    lines.append("【3】Task 6b 的产物与其判据（D7：单独一节）")
    ok &= check_6b(lines)

    lines.append("")
    lines.append("【4】放行条件里的外部实测记录（由 Task 7 实施者跑完后逐字落盘）")
    lines.append("  这两份是**产物逐字转抄**，本脚本不重跑 `cli`（见模块 docstring）；"
                 "判据见各自的核对行。")
    ok &= check_record(lines, TIMING, "`cli all` 的耗时实测（末行逐字）",
                       ("耗时", "s/份"))
    ok &= check_record(lines, DETERMINISM, "抽取物（md/图表/公式）的确定性实测",
                       ("跑前", "跑后"))
    ok &= check_determinism_counts(lines, DETERMINISM)

    lines.append("")
    lines.append("【5】放行条件表（与【0】派生出来的实际判据集对齐）")
    n = len(stages)
    lines.append(f"  放行的范围：**{PILOT} 试点 43 份这条流水线**。以下每条都给证据路径。")
    cond = [
        (f"① 全部 {n} 个判据脚本（由磁盘派生，不是计划的六项快照）全量跑"
         f"**退出码 0 且产物里是裸的 `RESULT: PASS`**",
         "【2】逐条；产物 = `tests/papers/reports/<名>-report.txt`"),
        (f"② Task 6b 的判据**在**①的清单里（`verify_types.py` / `verify_map.py` 各一条"
         f"回归守卫，D1）", "【0】；漏一个即红"),
        ("③ A1 原件哈希复核通过（全语料 201 份 + 试点 43 份与基线逐字相同）",
         "【1】；基线 `tests/papers/reports/origin-sha256-all.txt` / `-2025.txt`"),
        ("④ `cli all` 的耗时已实测并逐字落盘", f"`{rel(TIMING)}`（见【4】）"),
        ("⑤ 抽取物（md / 图表 / 公式）的确定性已实测并逐字落盘，"
         "**且最后一次对账的四处读数都为 0（判数，不是只判文件里有那几个词）**",
         f"`{rel(DETERMINISM)}`（见【4】：文件本身的核对行 + **判数**行，"
         f"口径与命令都印在那一节里）；另有两处**每次运行都判**的重放性判据："
         f"`verify_map.py` 的 M-1-b（`index.build` 重跑到不入库目录）、M-8"
         f"（`model_map.build()` 重跑到不入库目录）"),
        ("⑥ Task 6b 的产物齐备且字形可核", "【3】"),
        ("⑦ 放行证据 `" + rel(RELEASE) + "` **自身**受版本控制（D9：不入库的残余"
         "等于丢失；原先没有任何判据护栏，M-9）",
         "【5】；口径：`git ls-files --error-unmatch " + rel(RELEASE) + "`"),
    ]
    for a, b in cond:
        lines.append(f"  {a}")
        lines.append(f"      证据：{b}")
    lines.append(f"  **不在放行范围内**：「全量 201 份」——见【6】。本表的 ① 全部 PASS "
                 f"**不等于** 201 份跑得起来。")
    lines.append(f"  **不在放行范围内**：**两项人工目视闸门**——见【5b】。"
                 f"「可放行」**不覆盖** C4 目视项。")
    ok &= check_release_tracked(lines)

    # ---- 【5b】人工目视闸门：**范围声明 + 报告量**（B-1，不构成判据）----
    lines.append("")
    lines.append("【5b】两项**人工目视闸门**：**不在本汇总的判定范围内**（B-1）")
    lines.append("  **两项人工目视闸门（C4 的与 Task 2 的）不在本汇总的判定范围内**；"
                 "其机读值见各产物。")
    lines.append("  为什么非写不可——**同一件事有两个力道**，只读 `RESULT` 会把两者读成一件：")
    lines.append(f"    · **Task 2** 的 `{rel(VISUAL_WM)}`（在 `verify_wm.py` 第 8 节是"
                 f"**硬判据**）：缺了/为空 ⇒ 该脚本判 FAIL ⇒ 进 ① 的放行范围。")
    lines.append(f"    · **C4** 的 `{rel(VISUAL_C4)}`（在 `verify_c.py` **不并入 RESULT**："
                 f"那段闸门以 `return not bad` 收尾，**不含** `visual_ok`）——缺了 ⇒ "
                 f"`c-report.txt` 会写 `C4 人工目视闸门: FAIL（未判定）` 与 "
                 f"`发布放行: **未放行**`，**而它的 `RESULT` 行照样是 PASS**。")
    lines.append("  ⇒ 「本汇总可放行」**不覆盖 C4 目视项**。那两行**不受本文任何判据管辖**"
                 "（`CRIT_RX` 的两支都收不到它们——口径见 `CRIT_RX` 定义处的复核命令）。")
    c_ev = stage_evidence(HERE / "verify_c.py")
    try:
        c_txt = c_ev.read_bytes().decode("utf-8", "replace")
    except OSError as e:
        c_txt = ""
        c_why = f"读不到 `{rel(c_ev)}`（{type(e).__name__}）"
    else:
        c_why = ""
    m = C4_VIS_RX.search(c_txt)
    c4v = m.group(1) if m else f"取不到（{c_why or '产物里没有 `机读值 visual_ok=` 那一行'}）"
    lines.append(f"  **报告量（不是判据）**：C4 的机读值 visual_ok = {c4v}"
                 f"（口径：`grep -n '机读值 visual_ok=' {rel(c_ev)}`，"
                 f"由 `verify_c.py` 写进它自己的产物）；"
                 f"`{rel(VISUAL_C4)}` 存在 = {VISUAL_C4.is_file()} · "
                 f"`{rel(VISUAL_WM)}` 存在 = {VISUAL_WM.is_file()}")
    lines.append("  **本条是报告量：上面这些取值一个都不参与本汇总的 ok / 退出码**——"
                 "它的作用是把「目视项现在是不是判定过」摆到读者眼前，不是替它下结论。")

    lines.append("")
    lines.append("【6】扩到全量 201 份：当场量出来的前置（R6）")
    check_r6(lines)

    # **状态行不在这里落**：它必须与 RESULT 行同源。落点守卫的两条消息在 main() 里
    # 才并进 ok（写前复核那条更是紧贴 write 才判），若在这里就把「可放行」写进正文，
    # 守卫触发时正文会说「可放行」而 RESULT 行说 FAIL——那正是本项目最重的缺陷族
    # （证据里一句与实测不符的话）。见 main() 末尾那段。
    meta["n_stages"] = n
    return ok


def main() -> int:
    import argparse as _ap

    from tools.papers import report

    ap = _ap.ArgumentParser(
        description="试点汇总与放行评估（Task 7）：跑齐磁盘上实际存在的全部判据脚本",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="限样本跑：转发给支持 `--limit` 的子脚本（谁支持由 `--help` 当场探测），"
             "报告写 tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/pilot-summary.txt）；负数不接受。",
    )
    args = ap.parse_args()

    started = time.time()
    out, guard_msg = resolve_summary(args.limit)
    pre = report.sha256_of(RELEASE) if args.limit > 0 else ""

    lines = ["M6 前置流水线 · 试点汇总与放行评估（Task 7）",
             "=" * 78]
    meta: dict = {}
    if guard_msg:
        lines.append(guard_msg)
    ok = True
    try:
        same, msg = branch_crosscheck(args.limit, out, guard_msg)
        lines.append(msg)
        ok &= same
    except BaseException as e:            # noqa: BLE001
        lines.append("落点机制分支对账抛异常（按 FAIL 处理）：")
        lines.append(report.fmt_exc(e))
        ok = False
    lines.append("")

    try:
        ok &= checks(lines, args.limit, started, meta)
    except BaseException as e:            # noqa: BLE001 —— 任何异常都算 FAIL
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = recheck_summary(args.limit, out)
    if msg2:
        lines.append(msg2)
    if guard_msg or msg2:
        ok = False

    # ---- 逐阶段墙钟：落进**测量记录**（不是放行证据），并守它的落点（A-3）----
    # 这段必须在 `text = "\n".join(lines)` **之前**：它判出来的东西要进正文。
    if args.limit > 0:
        # 限样本跑**不写**入库的耗时记录（与放行证据同一套纪律：入库证据只由全量跑写）。
        # 判据是字节事实那一层：本次运行期间它被重写过 ⇒ mtime > started ⇒ 红。
        touched = False
        try:
            touched = TIMING_DETAIL.is_file() and TIMING_DETAIL.stat().st_mtime > started
        except OSError:
            touched = False
        if touched:
            lines.append(f"落点守卫 FAIL：本次**限样本跑**重写了入库的耗时记录 "
                         f"{rel(TIMING_DETAIL)}——入库证据只由全量跑写（这条是「限样本"
                         f"不得覆写放行证据」那条的延伸）。判 FAIL。")
            ok = False
    else:
        detail = timing_detail_text(meta, started, time.time())
        report.flush(TIMING_DETAIL, detail)
        # 落盘后**对账**（字节事实，兜底）：读回来的必须就是要写的那串。
        try:
            back: bytes | None = TIMING_DETAIL.read_bytes()
        except OSError:
            back = None
        if back != detail.encode("utf-8"):
            lines.append(f"落盘自检 FAIL：耗时记录 `{rel(TIMING_DETAIL)}` 落盘后读回的字节"
                         f"与要写的不一致——落点或写入出了岔子。判 FAIL。")
            ok = False

    # 落点守卫的消息**已经**在这个 ok 里了（上面两句），现在才落状态行——于是
    # 「正文里的状态」与「RESULT 行」由同一个 ok 生成，结构上不可能互相矛盾。
    lines.append("")
    lines.append("=" * 78)
    lines.append(f"判据集规模（**派生值**，不是手抄）：{meta.get('n_stages', 0)} 个脚本")
    lines.append(f"当前状态：{'**可放行**（范围：' + PILOT + ' 试点 43 份）' if ok else '**未放行**'}"
                 + "；「可放行全量 201 份」另见【6】，R6 未决项不因本行而消失"
                 + "；**两项人工目视闸门不在本判定范围内**（见【5b】——"
                 + "「可放行」不覆盖 C4 目视项）")

    lines.append("")
    lines.append(f"写入：{rel(out)}")
    if args.limit > 0:
        lines.append(f"  本文件是**限样本跑**（--limit {args.limit}）的报告，"
                     f"**不入库、不是放行依据**；放行证据是 {rel(RELEASE)}，"
                     f"只有全量跑会写它。")
    else:
        lines.append(f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
                     f"{rel(LIMITED_DIR)}/ 下的另一份文件。")

    text = "\n".join(lines) + "\n"
    if args.limit > 0:
        post = report.sha256_of(RELEASE)
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· {rel(RELEASE)}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"
    else:
        if out != RELEASE:      # 结构上已被镜像守卫挡掉；再判一次是 fail-closed 的落款
            text += (f"\n落点自检 FAIL：全量跑的写入目标 {rel(out)} **不是**放行证据 "
                     f"{rel(RELEASE)}\n")
            ok = False

    # RESULT 行。**不用 `report.result_suffix`**：它按「前 N 份 + 见证集」描述样本，
    # 而本脚本的样本口径由**各子脚本自己**决定（它们各自的见证集不同），逐条照抄在
    # 【2】里。语义与它一致：**只有全量跑才可能出现裸 `RESULT: PASS`**。
    suffix = "" if args.limit <= 0 else (
        f" (LIMITED --limit {args.limit}；样本口径由各子脚本自己决定，逐条见【2】；"
        f"非放行依据)")
    # 绝对路径痕迹判在 **RESULT 行之前**：`verify_map.py` 那一版先把 RESULT 行拼进去、
    # 再扫痕迹，于是"痕迹非空 ⇒ 判 FAIL"只改了退出码，**入库的报告里仍留着
    # `RESULT: PASS`**（文件与退出码互相矛盾）。这里照 fail-closed 排：先扫、后落 RESULT。
    dirty = report.path_audit(text)
    if dirty:
        text += (f"\n报告里出现绝对路径痕迹 {report.scrub(str(dirty))!r}"
                 f"——违反「报告只带仓库相对路径」，判 FAIL\n")
        ok = False
    text += f"\nRESULT: {'PASS' if ok else 'FAIL'}{suffix}\n"

    report.flush(out, text)
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
