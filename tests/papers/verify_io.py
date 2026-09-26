"""校验 io 层的路径映射、稳定 ID 与字节级写入。

判据证据写入 `tests/papers/reports/io-report.txt`：报告用 `write_bytes` + LF 落盘
（故 blob 与工作树是同一串字节），路径一律按仓库相对形式打印（故换台机器重跑
不会产生虚假 diff）。

终端输出与报告内容一致，但不是逐字节相同：Windows 的文本模式 stdout 会把
`\\n` 翻成 `\\r\\n`，报告文件不经过那一层。逐字节相等这件事只对文件成立，
证据见 tests/papers/reports/gitattributes-gate.txt 第 5 节。

函数本身是**设计成抛异常**的（坏合集名、坏题号、坏路径）。若某次回归让它们
在此抛出，main() 会把 traceback 连同 `RESULT: FAIL` 写进报告——报告是入库的
判据证据，绝不能留下一份没人复核的绿色结论。

## `--limit N` 与落点（2026-09-26 补齐，此前本脚本是 8 个闸门脚本里 2 个没有它的之一）

`--limit N`（N > 0）走 `tools/papers/report.py` 的落点机制——**落点由样本口径唯一
决定**：限样本写 `tests/papers/reports-limited/io-report-limited-N.txt`（不入库）、
**不得写放行证据**；`limit <= 0`（全量，默认）才写放行证据。
**本脚本的 `--limit` 不改变判据集**：它没有"43 份 PDF"这种样本口径（输入是代码级
探针 + 两份基线表），故 `--limit` 在这里的语义**只是落点判别式**——把"限样本的结论
不得当放行依据"这条纪律补上，而不是声称"少验了几份"。另两条同批补的纪律：
崩溃路径改用 `report.fmt_exc`（**不得用 `traceback.format_exc()`**：它每条栈帧
都把仓库根写成绝对路径），报告全文过 `report.path_audit`。
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tools.papers import io  # noqa: E402

# 判据组名（`report.release_path(KIND)` → 放行证据；落点由 resolve_report 决定）。
KIND = "io"


def rel(p) -> str:
    """仓库相对路径。

    报告是入库的判据证据：绝对路径（`D:\\Projects\\数学建模\\...`）只在这台
    机器上成立，换台机器重跑就整篇变红，等于噪音。
    """
    try:
        return Path(p).relative_to(io.REPO).as_posix()
    except ValueError:
        return Path(p).as_posix()


def checks(lines: list[str]) -> bool:
    ok = True

    # 1. 原件根存在，派生物根可建
    lines.append(f"ORIGIN={rel(io.ORIGIN)} exists={io.ORIGIN.is_dir()}")
    ok &= io.ORIGIN.is_dir()

    # 2. 稳定 ID 与路径可双向解析
    sid = io.stable_id("2025美赛O奖论文", "A", 1)
    lines.append(f"stable_id('2025美赛O奖论文','A',1) = {sid!r}")
    ok &= sid == "P2025-A-01"

    got = io.parse_stable_id(sid)
    lines.append(f"parse_stable_id({sid!r}) = {got!r}")
    ok &= got == ("2025", "A", 1)

    # 2b. 题号校验必须与 parse_stable_id 的正则是同一套语义。
    # `problem in "ABCDEF"` 是子串测试，会放行 "AB" 与 ""，产出
    # P2025-AB-01 / P2025--01，而 parse_stable_id 一概拒绝——
    # 双向不变式恰在 guard 声称拒绝的输入上破裂。
    for bad in ("AB", ""):
        try:
            bad_sid = io.stable_id("2025美赛O奖论文", bad, 1)
        except ValueError:
            lines.append(f"stable_id(题号={bad!r}) 抛 ValueError")
        else:
            lines.append(
                f"stable_id(题号={bad!r}) = {bad_sid!r} ← 未拒绝，与 parse_stable_id 语义不一致"
            )
            ok = False

    # 3. 路径映射：题号从路径取，合集由调用方传
    src = "corpus/历届优秀论文/2025美赛O奖论文/A/2500836.pdf"
    prob = io.problem_of(src)
    lines.append(f"problem_of({src!r}) = {prob!r}")
    ok &= prob == "A"

    # 2023 合集的题目录下还有一层中文长名，题号上一层不是合集——
    # 这正是 problem_of 只返回题号、要求合集显式传入的原因
    deep = "2023美赛O奖论文/2023年美国大学生数学建模竞赛（常规赛）O奖论文/A/x.pdf"
    lines.append(f"problem_of(深层路径) = {io.problem_of(deep)!r}")
    ok &= io.problem_of(deep) == "A"

    md = io.md_path("2025美赛O奖论文", prob, "2500836")
    fdir = io.figures_dir("2025美赛O奖论文", prob, "2500836")
    qdir = io.formulas_dir("2025美赛O奖论文", prob, "2500836")
    lines.append(f"md_path   = {rel(md)}")
    lines.append(f"figures   = {rel(fdir)}")
    lines.append(f"formulas  = {rel(qdir)}")
    ok &= rel(md).endswith("corpus/papers/md/2025美赛O奖论文/A/2500836.md")
    ok &= "clean" not in str(md) and "clean" not in str(fdir)

    # 4. 原件哈希表：A1 判据的基础，必须非空且可复现
    h1 = io.sha256_tree("2025美赛O奖论文")
    h2 = io.sha256_tree("2025美赛O奖论文")
    lines.append(f"sha256_tree: {len(h1)} 份；两次调用一致={h1 == h2}")
    ok &= len(h1) == 43 and h1 == h2

    # 4b. 合集名写错必须报错，不能返回 {}
    # 两份空表相等，A1 会给出零哈希支撑的"原件未改动"。磁盘上的真名是
    # `2023年美赛O奖论文`，"2023美赛O奖论文"正是实际存在过的那种写错。
    try:
        io.sha256_tree("2023美赛O奖论文")
    except FileNotFoundError:
        lines.append("sha256_tree(不存在的合集名) 抛 FileNotFoundError")
    else:
        lines.append("sha256_tree(不存在的合集名) 未报错 ← 会静默产出可被 A1 采信的空表")
        ok = False

    # 4c. 合集目录存在但没有 PDF，同样必须报错
    # 把 ORIGIN 临时换成空目录来验，而不是往原件树里写探针目录：
    # 原件树全程只读是流水线自身的前提。
    real_origin = io.ORIGIN
    with tempfile.TemporaryDirectory() as tmp:
        io.ORIGIN = Path(tmp)
        try:
            (Path(tmp) / "空合集").mkdir()
            io.sha256_tree("空合集")
        except ValueError:
            lines.append("sha256_tree(无 PDF 的合集) 抛 ValueError")
        else:
            lines.append("sha256_tree(无 PDF 的合集) 未报错 ← 空表会被当成「未改动」")
            ok = False
        finally:
            io.ORIGIN = real_origin
    ok &= io.ORIGIN == real_origin

    # 5. 字节级写入的回读校验
    # 它只覆盖文件系统这一环：write_bytes/read_bytes 是二进制路径、绕开 git，
    # **抓不住行尾转换**。防 autocrlf 的是 .gitattributes 的 -text 与
    # git add → blob → git checkout 的字节往返，证据在
    # tests/papers/reports/gitattributes-gate.txt。
    probe = io.DERIVED / "_probe" / "bytes.bin"
    payload = b"line1\nline2\r\nline3\r\r\n\x00\xff binary tail"
    io.write_bytes_checked(probe, payload)
    back = probe.read_bytes()
    lines.append(f"write_bytes_checked roundtrip identical={back == payload}")
    ok &= back == payload
    probe.unlink()
    probe.parent.rmdir()

    return ok


def main() -> int:
    import argparse

    from tools.papers import report

    ap = argparse.ArgumentParser(
        description="io 层校验：路径映射、稳定 ID、字节级写入",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="只改**落点**（本脚本没有 PDF 样本口径，判据集不变）：报告写到 "
             "tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/io-report.txt）；负数不接受。",
    )
    args = ap.parse_args()

    out, guard_msg = report.resolve_report(KIND, args.limit)
    pre = report.sha256_of(report.release_path(KIND)) if args.limit > 0 else ""

    meta: dict = {}
    lines: list[str] = []
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines)
    except BaseException as e:
        # io 层的函数是**设计成抛异常**的（坏合集名、坏题号、坏路径）。
        # 若未来某次回归让它们在此抛出，脚本绝不能带着上一次的 PASS 死掉：
        # 这份报告是入库的判据证据，留在仓库里的绿色结论会被当成事实，
        # 而 git status 上看不出任何异常。
        # traceback 过 `report.fmt_exc`：**不得用 `traceback.format_exc()`**，
        # 它每条栈帧都把仓库根写成绝对路径（崩溃那一次会写进入库证据）。
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = report.recheck_target(KIND, args.limit, out)
    if msg2:
        lines.append(msg2)
    # **这一句不能省**：守卫消息只是往报告里写了"FAIL"，不并进 ok 的话
    # RESULT 行照样打印 PASS、退出码照样是 0。
    if guard_msg or msg2:
        ok = False

    lines.append("")
    lines.append(f"写入：{report.rel(out)}")
    if args.limit > 0:
        lines.append(
            f"  本文件是**限样本落点**（--limit {args.limit}）的报告，"
            f"**不入库、不是放行依据**；放行证据是 "
            f"{report.rel(report.release_path(KIND))}，只有全量跑会写它。"
        )
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件。"
        )

    text = "\n".join(lines) + "\n"
    if args.limit > 0:
        post = report.sha256_of(report.release_path(KIND))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· "
            f"{report.rel(report.release_path(KIND))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    text += (f"\nRESULT: {'PASS' if ok else 'FAIL'}"
             f"{report.result_suffix(KIND, args.limit, meta, ())}\n")
    # 绝对路径痕迹的扫描**必须放在最后**（含 `RESULT:` 行与自检段）。
    dirty = report.path_audit(text)
    if dirty:
        text += (f"\n报告里出现绝对路径痕迹 {report.scrub(str(dirty))!r}"
                 f"——违反「报告只带仓库相对路径」，判 FAIL\n")
        ok = False

    report.flush(out, text)
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
