"""落点机制：**「写哪一份报告」由样本口径唯一决定**（Task 4 起各校验脚本共用）。

本模块的语义**照抄**已冻结的 `tests/papers/verify_b.py`（Task 3 八轮换来的那套），
抽出来供 Task 4–7 共用。**`verify_b.py` 一个字节都不改**——它是那套防线的原件，
本模块是**副本**。两份并存是已知的债（`docs/mcm-suite-todo.md` §A 终审清单里
「两套落点机制并存」），登记在此，不在本轮消除。

## 为什么要有这套东西（原委，逐字承自 verify_b.py）

Task 3 上一版把两条路径做成**同一个常量** `REPORT`，`main()` 结尾无条件写它：

    REPORT.write_bytes(text.encode("utf-8"))          # 旧版，无 --limit 分支

于是 `--limit 3`（5 份样本）**把 43 份全量跑的放行证据整个覆写掉**——`git status`
上是一处「修改」。当时那半条防线（限样本跑的 RESULT 行带 `LIMITED` 后缀）**挡不住
它**：后缀让人**读的时候看出来**，可覆写已经把 43 份的结论删了。它属于本项目栽过
五次的「判据/证据在什么都没验的情况下报绿」家族。

**防线从「读的时候看得出来」升级为「根本不覆盖」**，且**两个方向都守**：

| 层 | 判什么 | 触发条件 |
| :--- | :--- | :--- |
| `resolve_report()` 正向守卫 | 落点**决策** | `limit > 0` 且落点算出与放行证据重合 → 改写到不入库目录 + 判 FAIL |
| `resolve_report()` 镜像守卫 | 落点**决策** | `limit <= 0` 且落点不是放行证据 → **改写回**放行证据 + 判 FAIL |
| `recheck_target()`（写前复核） | 落点**决策**（紧贴 write） | 调用点被绕开时补判；两方向同上，镜像那条同样**改写 out** |
| 落盘后 sha256 对账（调用方做） | **字节事实**（兜底） | 限样本跑前后放行证据的 sha 必须相同 |

**措辞强度要说准**（这句原先把两种情况并成了一句，会让读者以为"绕开时也会被改写"）：守卫保证的是
「**决策点**被改坏 → 判 FAIL **并改写落点**；**整个绕开调用点** → 限样本跑确实会写进
放行证据本体、只判 FAIL **而不改写**」，**不是**「物理上写不进去」——
后一种（verify_b 的 probe B 实测形态、本轮的 M-L2）靠写前复核与落盘后 sha256 对账才红。

## 谓词口径：全量跑 = `limit <= 0`（不是 `== 0`）

`pick_sample` 把 `limit <= 0` 当全量跑，所以「全量跑」这个语义的**全部**取值是
`<= 0`。写成 `== 0` 时 `--limit -3` 落在两者之间——那是一次真全量跑，却两条反向
守卫都不认（verify_b 实测过这条旁路，见其 `limit_arg` 的 docstring）。故：
**`--limit` 在 argparse 层就拒负数**（`limit_arg`），**且**守卫谓词一律用 `<= 0`。
只做一层都不叫收口。

## 报告口径（与 verify_b.py 同，别自创）

* 一律 `write_bytes` + LF 落盘（见 `flush()`）；
* 只写仓库相对路径（`rel()`；`ABSPATH_TRACE` 每次运行当场扫，见 `path_audit`）；
* 报告写入**无条件执行**（放在 main 结尾、不在 try 内）——脚本崩了也不能把上一次的
  `RESULT: PASS` 留在库里冒充本次结论；
* 崩溃的 traceback 经 `fmt_exc()` 消毒（**不得用 `traceback.format_exc()`**：它每条
  栈帧都把仓库根写成绝对路径，平时的绿跑看不出，正好在看门狗触发那刻破）。
"""
import argparse
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
REPORTS = ROOT / "tests" / "papers" / "reports"
# 限样本跑的落点**选为**这个目录（不入库，根级 .gitignore 忽略）。
# "选为"不等于"实际写到哪"：调用点被绕开时限样本跑实际写的就是放行证据本体，
# 那一次判 FAIL 并在报告正文里写明（见 resolve_report）。
LIMITED_DIR = ROOT / "tests" / "papers" / "reports-limited"

# 报告只许带仓库相对路径。这三种形态是「机器特定绝对路径」的判据形态。
ABSPATH_TRACE = re.compile(r"\b[A-Za-z]:[\\/]|\\\\[^\s]|/(?:Users|home|root)/")
_ABS_WIN = re.compile(r"\b[A-Za-z]:[\\/][^\s\"'<>|]*")
_ABS_UNC = re.compile(r"\\\\[^\s\"'<>|]+")
_ABS_POSIX = re.compile(r"/(?:Users|home|root|tmp|var|opt|mnt|Volumes)/[^\s\"'<>|]*")


def release_path(kind: str) -> Path:
    """放行证据的落点（入库、受版本控制）。

    `kind` 是判据组的小写名（`"c"` → `tests/papers/reports/c-report.txt`）。
    """
    return REPORTS / f"{kind}-report.txt"


def report_path(kind: str, limit: int) -> Path:
    """样本口径 → 报告落点。**全脚本唯一决定写哪一份的地方。**

      * `limit > 0`（限样本 / 变异演示）→ `tests/papers/reports-limited/` 下的独立
        文件（入库与否按"被选为的落点"判定：那个目录不入库）；文件名带 `limit`，
        于是 `--limit 3` 与 `--limit 5` 互不覆盖；
      * `limit <= 0`（全量；谓词与 `pick_sample` 同口径）→ 放行证据。

    返回 `Path`，**不做任何判断**——守卫在 `resolve_report()`。分开是要紧的：
    守卫的对象是"决策点"，而本函数只是那张表。
    """
    if limit > 0:
        return LIMITED_DIR / f"{kind}-report-limited-{limit}.txt"
    return release_path(kind)


def resolve_report(kind: str, limit: int) -> tuple[Path, str]:
    """落点 + 守卫消息（空串 = 未触发）。**结构性 tripwire，两个方向都守。**

      * **限样本跑不得落在放行证据上**：`limit > 0` 且落点算出来与放行证据重合，
        说明 `report_path` 被人改回了单路径。此时**既不写放行证据（不覆盖），也不是
        干脆不写**（不写的话上一次的 `RESULT: PASS` 会留在库里冒充本次结论，那是
        同一家族的另一个形态），而是改写到不入库目录 + 报告里明写 + 判 FAIL。
      * **全量跑必须落在放行证据上**：`limit <= 0` 且落点不是放行证据，说明
        `report_path` 的全量分支被改坏（正是上面那条守卫存在理由的**镜像改法**）：
        全量跑会**静默写进** `reports-limited/`——不触发任何守卫、不量 sha、
        `RESULT: PASS` 且无 `LIMITED` 后缀、退出码 0，而放行证据保留**上一次**的
        `RESULT: PASS` 冒充本次结论，**完全无红**。此时**改写回放行证据**：一次全量跑
        既不能把结论写进别处、也不能把旧结论留在原地。

    **改写方向两条相反是要紧的**：正向那条把与放行证据重合的落点**改写走**；
    反向这条**必须**把它改写成放行证据。「禁止写放行证据」只对正向的**决策点**
    守卫成立——写前复核（`recheck_target`）只判 FAIL、**不改写 out**（调用点被绕开
    后限样本跑确实写进了放行证据本体，靠字节对账与 FAIL 才红）。

    调用方**必须把返回的消息并进 `ok`**：守卫消息只是往报告里写了"FAIL"、
    不并进 ok 的话 RESULT 行照样打印 PASS——判据说了话而结论不听，
    正是本文件存在的理由（verify_b 的 probe A 实测抓到的就是这个）。
    """
    out = report_path(kind, limit)
    rel_ev = rel(release_path(kind))
    if limit > 0 and out == release_path(kind):
        return LIMITED_DIR / f"{kind}-report-落点守卫触发.txt", (
            f"落点守卫 FAIL：限样本跑（--limit {limit}）算出的落点与放行证据 "
            f"{rel_ev} 重合——report_path 被改坏了。已改写到不入库目录，"
            f"放行证据未被本次运行触碰。"
        )
    if limit <= 0 and out != release_path(kind):
        return release_path(kind), (
            f"落点守卫 FAIL：全量跑（limit={limit}）算出的落点是 {rel(out)}，**不是**"
            f"放行证据 {rel_ev}——report_path 的全量分支（`limit <= 0`）被改坏了（这条是"
            f"'限样本不得覆写放行证据'那条守卫的镜像：同一个机制的反方向）。已把落点"
            f"改写回放行证据（全量跑必须拥有这份证据，否则它会停在上一次的状态冒充本次"
            f"结论），判 FAIL。"
        )
    return out, ""


def recheck_target(kind: str, limit: int, out: Path) -> tuple[Path, str]:
    """**写前落点复核**（紧贴 `write_bytes` 的那道，对付"调用点被绕开"）。

    `resolve_report` 的守卫判在**决策点**，而决策点可以被改坏**调用点**绕过去
    （`out, guard_msg = resolve_report(...)` 改成常量元组即可）。这一句在写之前用
    **实际要写的那个 out** 再判一次，绕开它就必须直接改这一句。

    两个方向：
      * `limit > 0` 且 `out` 是放行证据 → 判 FAIL，**不改写 out**（正向决策点守卫的
        改写方向是"改写走"，此处若也改写走，就等于替调用方擦了屁股而少一次 FAIL
        信号；verify_b 的 probe B 实测就是"写进了放行证据本体 + 判 FAIL"这个形态）；
      * `limit <= 0` 且 `out` 不是放行证据 → 判 FAIL **并改写回放行证据**（不许把旧
        结论留在原地，理由同 `resolve_report` 的镜像守卫）。
    """
    rel_ev = rel(release_path(kind))
    if limit > 0 and out == release_path(kind):
        return out, (
            f"落点守卫 FAIL（写前复核）：限样本跑（--limit {limit}）的写入目标就是放行"
            f"证据 {rel_ev}——resolve_report 的守卫在调用点被绕过了。判 FAIL。"
        )
    if limit <= 0 and out != release_path(kind):
        wrong = out
        return release_path(kind), (
            f"落点守卫 FAIL（写前复核）：全量跑（limit={limit}）算出的写入目标是 "
            f"{rel(wrong)}，**不是**放行证据 {rel_ev}——落点判据被改坏或在调用点被绕过"
            f"了。已把落点改写回放行证据（全量跑必须拥有这份证据，否则它会停在上一次的"
            f"状态冒充本次结论），判 FAIL。"
        )
    return out, ""


def pick_sample(pdfs: list[Path], limit: int, focus: tuple[str, ...] = ()) -> list[Path]:
    """`--limit N` 的取样：前 N 份 ∪ 见证集。

    **不并入见证集是不行的**：排序序里靠后的关键样本 `--limit 3` 取不到，判据的
    变异演示会在一个看不见它的样本集上"绿着通过"（verify_b 的 `FOCUS` 注释即此）。
    见证集逐脚本自定，各自的**选定理由写在该脚本的注释里**。
    """
    if limit <= 0:
        return pdfs
    chosen = {p for p in pdfs[:limit]}
    chosen |= {p for p in pdfs if p.stem in focus}
    return sorted(chosen)


def limit_arg(s: str) -> int:
    """`--limit` 的类型：**非负**整数（0 = 全量，默认；N > 0 = 前 N 份 + 见证集）。

    **为什么在入口上关掉负数**（两层都要，见模块 docstring）：`pick_sample` 把
    `limit <= 0` 当成全量跑，而否定形谓词写成 `== 0` 时 `--limit -3` 是**一次全量跑、
    却不等于 0**，两条反向守卫静默不触发。`0` 仍是合法值（= 全量，与不放等价）。
    """
    try:
        v = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"不是整数：{s!r}") from None
    if v < 0:
        raise argparse.ArgumentTypeError(
            f"--limit 不接受负数（收到 {v}）：0 = 全量跑（默认），N > 0 = 只跑前 N 份 "
            f"+ 见证集。负数会被当成一次**全量跑**，从而绕过两条反向落点守卫。"
        )
    return v


def sha256_of(p: Path) -> str:
    """文件摘要；不存在时返回哨兵串（**不抛**：缺失本身要能被写进报告）。"""
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "<不存在>"


def rel(p: Path) -> str:
    """路径 → 报告里可写的仓库相对形式。

    报告只许带仓库相对路径（`ABSPATH_TRACE` 每次运行当场扫），所以写路径进报告
    一律走这里，不 print 原始 `Path`。
    """
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except Exception:  # 解析不了也不能把原始串（可能带盘符）写出去
        return "<仓库外路径>"


def scrub(s: str) -> str:
    """把仓库根与任何绝对路径形态替换成占位符。"""
    s = s.replace(str(ROOT), "<repo>").replace(ROOT.as_posix(), "<repo>")
    s = _ABS_WIN.sub("<abs-path>", s)
    s = _ABS_UNC.sub("<abs-path>", s)
    s = _ABS_POSIX.sub("<abs-path>", s)
    return s


def rel_code_path(name: str) -> str:
    """代码文件路径 → 仓库相对路径；仓库外的（stdlib/第三方）只留文件名。"""
    try:
        p = Path(name).resolve()
    except Exception:  # 路径拿不到时也不能把原串写出去
        return "<路径无法解析>"
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return f"<外部>/{p.name}"


def fmt_exc(e: BaseException) -> str:
    """异常 → 机器无关、只带仓库相对路径的文本。

    **不得用 `traceback.format_exc()`**：它每条栈帧都把**仓库根写成绝对路径**
    （`File "` + 盘符路径 + `"`），于是**崩溃那一次**会把机器特定绝对路径写进入库的
    报告——违反「报告只带仓库相对路径」。平时的绿跑看不出这条，正好在看门狗触发
    那刻破，所以必须在这里消毒，而不是靠人事后看一眼。异常**消息本身**也可能带绝对
    路径（例如 `FileNotFoundError(io.ORIGIN / ...)`），同样过一遍 scrub。
    """
    frames = []
    tb = e.__traceback__
    while tb is not None:
        code = tb.tb_frame.f_code
        frames.append(
            f'  File "{rel_code_path(code.co_filename)}", '
            f"line {tb.tb_lineno}, in {code.co_name}"
        )
        tb = tb.tb_next
    out = ["Traceback (most recent call last):", *frames,
           f"{type(e).__name__}: {scrub(str(e))}"]
    ctx = e.__context__ if e.__cause__ is None else e.__cause__
    depth = 0
    while ctx is not None and depth < 5:
        out.append(f"[链上异常 {depth + 1}] {type(ctx).__name__}: {scrub(str(ctx))}")
        ctx = ctx.__context__ if ctx.__cause__ is None else ctx.__cause__
        depth += 1
    return "\n".join(out)


def path_audit(text: str) -> str:
    """报告全文的绝对路径痕迹（空串 = 干净）。调用方**必须**把它并进 `ok`。"""
    m = ABSPATH_TRACE.search(text)
    return m.group(0) if m else ""


def flush(out: Path, text: str) -> None:
    """落盘：`write_bytes` + LF（见模块 docstring）。**唯一的写入口。**"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(text.encode("utf-8"))


def result_suffix(kind: str, limit: int, meta: dict, focus: tuple[str, ...]) -> str:
    """RESULT 行的后缀。`limit > 0` 时带上实际样本量与取样口径。

    **限样本的绿不得冒充放行结论**：`^RESULT: PASS$` 只可能来自全量跑。
    样本量取**实际**值（限样本集 = 前 N 份 ∪ 见证集，不是"N 份"）；`checks` 抛异常
    时 meta 为空，那时照实写「样本数未能确定」——不拿 `--limit` 冒充实际样本量。
    """
    if limit <= 0:
        return ""
    n_s, n_a = meta.get("n_sample"), meta.get("n_all")
    scope = (
        f"样本 {n_s}/{n_a} 份 = 前 {limit} 份 + 见证集 {'/'.join(focus)}"
        if n_s
        else f"样本数未能确定（checks 未跑到取样处；--limit {limit}）"
    )
    return f" (LIMITED {scope}；非放行依据)"
