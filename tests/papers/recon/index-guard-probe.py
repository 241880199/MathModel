"""`index.build` 的**落点守卫**命令行探针（不改任何入库文件；Task M2-hygiene）。

它量的是**变异不好覆盖的那几支**（等价路径、相对路径、大小写、哪条守卫先响），
逐条断言并把结论并进退出码。由 `tests/papers/recon/index-guard-mutdrive.py` 调起
（输出逐字进 `tests/papers/reports/index-guard-evidence.txt`），也可单独跑：

    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/index-guard-probe.py

**它自己不写任何入库产物**：唯一一个会写盘的用例（MB4）落在
`tests/papers/reports-limited/`（本项目约定的「不入库」目录）。用例 MB1/MB2/MB3/MB7
在**任何写盘动作之前**就该抛。每一条都打印跑前跑后的三份入库产物 blob（同一时刻），
证明它们没被碰。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.papers import index, io, report as rep  # noqa: E402

PRODUCTS = ["corpus/papers/INDEX.md", "corpus/papers/TAGS.md", "corpus/papers/PROVENANCE.md"]
SCRATCH = rep.LIMITED_DIR / "index-guard-probe"      # 不入库目录（.gitignore 已忽略）


def blobs() -> dict:
    """三份入库产物的**工作树 sha256**（不是 git blob）：本探针只问「变没变」。"""
    return {p: rep.sha256_of(ROOT / p) for p in PRODUCTS}


def show(msg: str) -> str:
    """消息里的绝对路径一律消毒（报告只许带仓库相对路径）。"""
    return rep.scrub(msg)


def case(label: str, fn, expect_throw: bool, expect_part: str = "") -> bool:
    before = blobs()
    threw, msg = False, ""
    try:
        r = fn()
        msg = f"没有抛错（n_entries={r.n_entries}、落点={rep.rel(r.index_path)}）"
    except Exception as e:                       # noqa: BLE001 —— 任何异常都算「抛」
        threw, msg = True, f"{type(e).__name__}: {show(str(e))}"
    after = blobs()
    churned = [p for p in PRODUCTS if before[p] != after[p]]
    ok = (threw == expect_throw) and (expect_part in msg) and not churned
    print(f"* {label}")
    print(f"    抛错 = {threw}（要求 {expect_throw}）"
          f" · 入库产物被写 = {bool(churned)}（要求 False；改了 {churned or '无'}）")
    print(f"    消息逐字：{msg}")
    return ok


def main() -> int:
    col = index.PILOT
    pdfs = sorted((io.ORIGIN / col).rglob("*.pdf"))
    one = pdfs[:1]
    print(f"（样本 = `{col}` 里排序第一的 1 份；正例的落点 = {rep.rel(SCRATCH)}）")
    print()
    r = []
    r.append(case("MB1  sample=1 + out_dir=io.DERIVED（**显式**指向入库产物）",
                  lambda: index.build(col, sample=one, out_dir=io.DERIVED), True,
                  "不得落到入库产物"))
    r.append(case("MB2  sample=1 + out_dir=相对等价路径 `corpus/papers`",
                  lambda: index.build(col, sample=one, out_dir=Path("corpus/papers")), True,
                  "不得落到入库产物"))
    r.append(case("MB3  sample=1 + out_dir=None（默认落点就是入库产物）",
                  lambda: index.build(col, sample=one), True, "必须显式指定 out_dir"))
    r.append(case("MB4  sample=1 + out_dir=不入库目录（**正例**：必须能跑）",
                  lambda: index.build(col, sample=one, out_dir=SCRATCH), False,
                  "没有抛错"))
    r.append(case("MB5  collection 不存在 + out_dir=不入库目录（既有 I11）",
                  lambda: index.build(col + "X", out_dir=SCRATCH), True, "合集目录不存在"))
    r.append(case("MB6  collection 不存在 + sample 也给 + out_dir=不入库目录（I11 的加严支）",
                  lambda: index.build(col + "X", sample=one, out_dir=SCRATCH), True,
                  "合集目录不存在"))
    r.append(case("MB7  collection 不存在 + sample 也给 + out_dir=io.DERIVED"
                  "（**哪条先响**：实测落点守卫先，两条都抛、都 fail-closed）",
                  lambda: index.build(col + "X", sample=one, out_dir=io.DERIVED), True,
                  "不得落到入库产物"))
    print()
    ok = all(r)
    print(f"**探针结论**：{len(r)} 条用例全部符合期望 = {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
