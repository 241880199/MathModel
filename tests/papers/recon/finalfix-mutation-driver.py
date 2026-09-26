"""终审修复轮（2026-09-26）新增判据与新增纪律的**变异 / 负例驱动器**。

范围（只覆盖本轮改动，不重复 `all-mutation-driver.py` 的 17 条）：

| id | 被测对象 | 变异 / 负例 | 期望 |
| :--- | :--- | :--- | :--- |
| FX-1 | `tests/papers/verify_io.py` 的落点 | 主流程的落点决策被换成「放行证据本体」 | **红**（写前复核判 FAIL + 退出码非 0；**实测还发现**：脚本自己的 sha 自检测不到本脚本的覆写，见下） |
| FX-2 | `tests/papers/verify_wm.py` 的落点 | 同上 | **红** |
| FX-3 | `verify_all.CRIT_RX`（M-1） | 缩进的 `名=FAIL` 行 | **红**（旧正则两支都不收 ⇒ 对照见本节） |
| FX-4 | `verify_all.check_determinism_counts`（M-2） | 同一标签下"汇总 0"在前、"明细 17"在后 | **红**（旧 `hits[0]` 取到 0 ⇒ fail-open） |
| FX-5 | `verify_all.check_release_tracked`（M-9） | 放行证据落在一个**未入库**的文件上 | **红** |

每条都带**对照**：变异下判红之外，**现状态必须是绿的**（不产生假红）——FX-3 的对照是
八份入库产物里自报失败**仍为 0 条**，FX-4 的对照是真记录仍判绿，FX-5 的对照是真
`pilot-summary.txt` 仍受版本控制。

纪律（与仓内其它驱动器一致）：
  * 变异体是**改写源码的副本**，放在 `tests/papers/` 下（脚本靠 `parent.parent.parent`
    定位仓库根，**换目录就跑不起来**），跑完即删；删不掉就整轮报 FAIL，不静默留下。
  * 变异体会**写坏入库的放行证据**（FX-1/FX-2 正是这个形态），故：跑前备份字节、
    跑后**逐字节还原并核 sha256**；不一致即整轮 FAIL。
  * 一切临时文件在 `build/`（gitignored）；子进程一律 `PYTHONDONTWRITEBYTECODE=1`。
  * 证据文件按本项目的报告纪律落盘：`write_bytes` + LF、只写仓库相对路径。

复现：`PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/finalfix-mutation-driver.py`
"""
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]     # 本文件在 tests/papers/recon/ 下（比判据脚本深一层）
sys.path.insert(0, str(ROOT))

HERE = ROOT / "tests" / "papers"
sys.path.insert(0, str(HERE))     # `verify_all` 在 tests/papers/ 下，不在包里
REPORTS = HERE / "reports"
RECON = HERE / "recon"
SCRATCH = ROOT / "build" / "finalfix"
EVIDENCE = REPORTS / "finalfix-mutation-evidence.txt"

CHILD_ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
             "PYTHONIOENCODING": "utf-8"}

GATE = ("b-report.txt", "c-report.txt", "d-report.txt", "ids-report.txt",
        "io-report.txt", "map-report.txt", "types-report.txt", "wm-report.txt")


def rel(p) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except Exception:
        return "<仓库外路径>"


def sha(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return "<不存在>"


def run(argv: list[str]) -> tuple[int, str]:
    p = subprocess.run(argv, capture_output=True, cwd=str(ROOT), env=CHILD_ENV)
    return p.returncode, p.stdout.decode("utf-8", "replace")


class Rec:
    """一段证据的正文。"""

    def __init__(self) -> None:
        self.blocks: list[str] = []

    def add(self, s: str) -> None:
        self.blocks.append(s)

    def text(self) -> str:
        return "\n".join(self.blocks)


# --------------------------------------------------------------------------
# FX-1 / FX-2：限样本跑把落点算成放行证据本体 ⇒ 两道判据都得红
# --------------------------------------------------------------------------
def mutation_landing(rec: Rec, script: str, kind: str) -> bool:
    """把 `script` 的落点决策那一行换成"放行证据本体"，跑 `--limit 1`。

    红路有三重（任一命中即红，这里逐条记）：
      ① `report.recheck_target` 的写前复核（紧贴 write）——决策点被绕开时补判；
      ② 落盘后「放行证据 sha256 跑前 == 跑后」自检；
      ③ 退出码非 0。
    跑完**逐字节还原**放行证据并核 sha256。
    """
    ok = True
    src = HERE / script
    mutant = HERE / f"zz_fixmut_{kind}.py"
    release = REPORTS / f"{kind}-report.txt"
    # 锚点：那一行的**原文**（对不上就整轮作废，不静默跳过）
    anchor = "    out, guard_msg = report.resolve_report(KIND, args.limit)"
    orig = src.read_bytes().decode("utf-8")
    if anchor not in orig:
        rec.add(f"  **整轮作废**：`{rel(src)}` 里找不到落点决策锚点 `{anchor}`")
        return False
    mutated = orig.replace(
        anchor,
        '    out, guard_msg = report.release_path(KIND), ""   # FX 变异：决策点被绕开')
    backup = release.read_bytes()
    pre_sha = hashlib.sha256(backup).hexdigest()
    rec.add(f"  变动：`{rel(src)}` 的落点决策行 → 直接返回放行证据本体 `{rel(release)}`")
    rec.add(f"  锚点原文：`{anchor}`")
    rec.add(f"  跑前放行证据 sha256 = {pre_sha}")
    try:
        mutant.write_bytes(mutated.encode("utf-8"))   # 与真脚本同目录（同深度）
        rc, out = run([sys.executable, str(mutant), "--limit", "1"])
    finally:
        if mutant.exists():
            mutant.unlink()
    post = release.read_bytes()
    post_sha = hashlib.sha256(post).hexdigest()
    restore = post != backup
    if restore:
        release.write_bytes(backup)
    back_sha = hashlib.sha256(release.read_bytes()).hexdigest()
    rec.add(f"  变异体退出码 = {rc}")
    hits = {
        "① 写前复核判 FAIL": "落点守卫 FAIL（写前复核）" in out,
        "② 放行证据 sha 自检判 FAIL": "两次相同 = False" in out,
        "③ 本文件被写坏（sha 变了）": post_sha != pre_sha,
    }
    for k, v in hits.items():
        rec.add(f"    {k} = {v}")
    # **一条本轮实测出来的结构事实（登记，不是通过项）**：② 恒为 False。本脚本沿用的
    # 是 `verify_d.py` / `verify_ids.py` 的自检写法——`post` 在 `report.flush` **之前**
    # 测，于是「本脚本自己的那次覆写」永远测不到（`verify_c.py` 反过来：先 flush、再测，
    # 所以那一份能看到）。真正兜住这次绕过的是 ①（写前复核）与退出码；外侧还有
    # `verify_all.check_evidence` 的限样本分支（判「产物 sha 跑前==跑后」与「产物
    # RESULT 行是裸的」，**代码事实、非本轮实测**）。三者都堵在这里，故无假绿。
    rec.add("    注（登记）：② 在本脚本的结构下**恒为 False**——`post` 在 `flush` 之前测，"
            "本脚本自己的覆写它测不到（`verify_c.py` 先 flush 再测，那一份能看到）。"
            "本次实测判红靠的是 ① 与退出码。")
    ok &= rc != 0
    ok &= hits["① 写前复核判 FAIL"] and hits["③ 本文件被写坏（sha 变了）"]
    # 还原与核对
    rec.add(f"  跑后放行证据 sha256 = {post_sha}"
            f"（{'已被变异体写坏 ⇒ 已还原' if restore else '未被写坏'}）")
    rec.add(f"  还原后 sha256 = {back_sha} · 与跑前相同 = {back_sha == pre_sha}")
    ok &= back_sha == pre_sha
    rec.add("  变异体保留的 stdout（**逐字**）：")
    rec.add("    " + "\n    ".join(out.rstrip("\n").splitlines()))
    return ok


# --------------------------------------------------------------------------
# FX-3：CRIT_RX 的缩进支（M-1）
# --------------------------------------------------------------------------
OLD_CRIT_RX = re.compile(
    r"^(?:[A-Za-z][A-Za-z0-9._-]*=(?P<eq>OK|FAIL)|[^\n]*:\s*(?P<colon>True|False))\s*$",
    re.M)


def probe_crit_indent(rec: Rec, va) -> bool:
    ok = True
    cases = ["  I2-c=FAIL", "I2-c=FAIL", "  I2-c=OK", "\tD3-b=FAIL",
             "  C4 人工目视闸门: FAIL（未判定）", "  发布放行: **未放行**",
             "  机读值 visual_ok=False", "  某判据: True"]
    for s in cases:
        old = bool(OLD_CRIT_RX.search(s)) and (
            OLD_CRIT_RX.search(s).group("eq") == "FAIL"
            or OLD_CRIT_RX.search(s).group("colon") == "False")
        new = bool(va.crit_fails(s))
        tag = "**新收、旧不收**" if (new and not old) else ""
        rec.add(f"    {s!r:44s} 旧判={old!s:5s} 新判={new!s:5s} {tag}")
    # 该红的那一种：缩进的 `名=FAIL`
    red_ok = bool(va.crit_fails("  I2-c=FAIL")) and not bool(OLD_CRIT_RX.search("  I2-c=FAIL"))
    rec.add(f"  缩进的 `名=FAIL`：新判据收、旧正则不收 = {red_ok}")
    ok &= red_ok
    # 对照（不得产生假红）：八份入库产物自报失败仍为 0 条
    tot = 0
    for n in GATE:
        p = REPORTS / n
        t = p.read_bytes().decode("utf-8", "replace")
        f = va.crit_fails(t)
        tot += len(f)
        rec.add(f"    对照 `{n}`：自报失败 {len(f)} 条"
                + (f" ← {f[:2]}" if f else ""))
    rec.add(f"  对照合计：八份产物自报失败 **{tot}** 条（必须为 0：新支不得产生假红）")
    ok &= tot == 0
    # 口径一致性（教训 4.8）：打印进汇总的那两条 grep 必须与 CRIT_RX 是同一件事
    rec.add("  口径一致性（打印进汇总的 grep 串 vs `CRIT_RX`）：")
    for n in GATE:
        p = REPORTS / n
        n_rx = len(va.CRIT_RX.findall(p.read_bytes().decode("utf-8", "replace")))
        cnt = 0
        for g in va.CRIT_GREPS:
            cmd = g + " " + rel(p)            # g 形如 `grep -cE '<正则>'`
            # 走 `sh -c` 原样执行**打印进汇总的那串**（不重写它）；`grep -c` 命中 0 时
            # 退出码是 1 但 stdout 仍是 `0`，故 rc ∈ {0,1} 都取 stdout，rc ≥ 2 才算错。
            rc, out = run(["sh", "-c", cmd])
            cnt += int(out.strip() or 0) if rc in (0, 1) else -10**6
        rec.add(f"    `{n}`：CRIT_RX 命中 {n_rx} · 两条 grep 相加 {cnt}"
                f" ⇒ {'一致 ✓' if n_rx == cnt else '**不一致 ⇒ FAIL**'}")
        ok &= n_rx == cnt
    return ok


# --------------------------------------------------------------------------
# FX-4：check_determinism_counts 取"全部行并取最严"（M-2）
# --------------------------------------------------------------------------
def probe_det_multiline(rec: Rec, va) -> bool:
    ok = True
    real = REPORTS / "all-determinism.txt"
    # 对照：真记录仍判绿
    lines: list[str] = []
    real_ok = va.check_determinism_counts(lines, real)
    rec.add(f"  对照：真记录 `{rel(real)}` 判 = {real_ok}（必须为 True）")
    for ln in lines:
        rec.add("    " + ln)
    ok &= real_ok
    # 变异：同标签下"汇总 0"在前、"明细 17"在后
    base = real.read_bytes().decode("utf-8")
    fake = base + "\n".join([
        "",
        "## fake-a.json → fake-b.json",
        "  入库产物：5 份，blob 变了 **0** 份",
        "  md         跑前 43 个 · 跑后 43 个 · blob 变了 0 ⇒ 逐字节相同",
        "  figures    跑前 1816 个 · 跑后 1816 个 · blob 变了 0 ⇒ 逐字节相同",
        "  formulas   汇总（变了 0 处）",
        "  formulas   跑前 1564 个 · 跑后 1564 个 · 只在跑后 16 · blob 变了 17 ⇒ **有变化**",
        "",
    ])
    SCRATCH.mkdir(parents=True, exist_ok=True)
    fake_p = SCRATCH / "det-multiline.txt"
    fake_p.write_bytes(fake.encode("utf-8"))
    lines2: list[str] = []
    new_ok = va.check_determinism_counts(lines2, fake_p)
    rec.add(f"  变异：在真记录尾部追加一节，`formulas` 出现两行——先 `变了 0`、后 `变了 17`")
    for ln in lines2:
        rec.add("    " + ln)
    # 旧实现（hits[0]）在同一份输入上的判定：取到第一行 ⇒ 0 ⇒ 绿（fail-open）
    body = fake[fake.rindex("\n## fake-a.json"):]
    first = [ln for ln in body.splitlines() if ln.strip().startswith("formulas")][0]
    old_n = int(re.search(r"变了\s*\**\s*(\d+)", first).group(1))
    rec.add(f"  旧实现（`hits[0]`）在同一份输入上取到的是 `{first.strip()}` ⇒ 读数 {old_n}"
            f" ⇒ 旧判 = {'绿（**fail-open**）' if old_n == 0 else '红'}")
    rec.add(f"  新判 = {new_ok}（必须为 False：任一非 0 即红）")
    ok &= new_ok is False and old_n == 0
    fake_p.unlink()
    return ok


# --------------------------------------------------------------------------
# FX-5：check_release_tracked（M-9）
# --------------------------------------------------------------------------
def probe_release_tracked(rec: Rec, va) -> bool:
    ok = True
    lines: list[str] = []
    real_ok = va.check_release_tracked(lines)
    rec.add(f"  对照：真放行证据 `{rel(va.RELEASE)}` 判 = {real_ok}（必须为 True）")
    for ln in lines:
        rec.add("    " + ln)
    ok &= real_ok
    # 变异：把放行证据的落点换到一个**未入库**的文件（正是"改常量名"那一手的效果）
    fake = HERE / "reports-limited" / "pilot-summary-zz-未入库.txt"
    fake.parent.mkdir(parents=True, exist_ok=True)
    fake.write_bytes(b"RESULT: PASS\n")
    real_release = va.RELEASE
    lines2: list[str] = []
    try:
        va.RELEASE = fake
        fake_ok = va.check_release_tracked(lines2)
    finally:
        va.RELEASE = real_release
        fake.unlink()
    rec.add(f"  变异：`RELEASE` 指向未入库的 `{rel(fake)}` ⇒ 判 = {fake_ok}（必须为 False）")
    for ln in lines2:
        rec.add("    " + ln)
    ok &= fake_ok is False
    ok &= not fake.exists()
    return ok


def main() -> int:
    import verify_all as va                      # noqa: E402（与真脚本同深度，import 得到）

    SCRATCH.mkdir(parents=True, exist_ok=True)
    started = time.time()
    rec = Rec()
    rec.add("终审修复轮（2026-09-26）新增判据 / 新增纪律的变异与负例证据")
    rec.add("=" * 78)
    rec.add(f"复现：`PYTHONDONTWRITEBYTECODE=1 python {rel(Path(__file__))}`")
    rec.add(f"落点：`{rel(EVIDENCE)}`（入库判据证据；变异体与临时文件在 gitignored 的 "
            f"`{rel(SCRATCH)}`）")
    rec.add("")
    ok = True
    for fx, (script, kind) in {
        "FX-1": ("verify_io.py", "io"),
        "FX-2": ("verify_wm.py", "wm"),
    }.items():
        rec.add(f"## {fx} · 限样本跑把落点算成放行证据本体（`--limit 1`）")
        rec.add("-" * 78)
        r = mutation_landing(rec, script, kind)
        rec.add(f"  {fx} 判定：{'红（符合期望）' if r else '**未红 ⇒ FAIL**'}")
        rec.add("")
        ok &= r
    rec.add("## FX-3 · `CRIT_RX` 的缩进支（M-1）")
    rec.add("-" * 78)
    r = probe_crit_indent(rec, va)
    rec.add(f"  FX-3 判定：{'红（符合期望），且现状态 0 条假红' if r else '**未达标 ⇒ FAIL**'}")
    rec.add("")
    ok &= r
    rec.add("## FX-4 · 确定性判数取「该标签下的全部行并取最严」（M-2）")
    rec.add("-" * 78)
    r = probe_det_multiline(rec, va)
    rec.add(f"  FX-4 判定：{'红（符合期望），真记录仍绿' if r else '**未达标 ⇒ FAIL**'}")
    rec.add("")
    ok &= r
    rec.add("## FX-5 · 放行证据自身入库（M-9）")
    rec.add("-" * 78)
    r = probe_release_tracked(rec, va)
    rec.add(f"  FX-5 判定：{'红（符合期望），真放行证据仍绿' if r else '**未达标 ⇒ FAIL**'}")
    rec.add("")
    ok &= r
    rec.add("=" * 78)
    rec.add(f"合计：{'全部达标（每条都实测判红，且现状态无假红）' if ok else '**有未达标项 ⇒ FAIL**'}")
    rec.add(f"本驱动器退出码 = {0 if ok else 1}；耗时 {time.time() - started:.1f}s")
    text = "\n".join(rec.blocks) + "\n"
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_bytes(text.encode("utf-8"))
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
