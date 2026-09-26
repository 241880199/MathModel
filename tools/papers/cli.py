"""统一入口：`python -m tools.papers.cli <stage> [--collection 名] [--limit N]`

    stage ∈ text | figures | formulas | index | all

**没有 `watermark` 阶段**：去水印不是独立产出步骤，它在 text/figures/formulas 各自
读取时于内存中完成（`watermark.strip_in_memory`），不产出任何文件（spec §4.1）。
计划里两处自相矛盾——接口行把 `watermark` 列进子命令、同页的示例代码又写「没有
watermark 阶段」——本入口以**示例代码与 spec §4.1** 为准（`{text,figures,formulas,
index,all}` 这五个），并把这条不一致登记在 Task 7 报告里。

所有阶段都直接读**原件**（`corpus/历届优秀论文/`）。原件全程只读，本模块不写原件。

## 与计划示例代码的三处差异（都是「先核仓里有没有」的结果）

1. `DEFAULT_COLLECTION` 取 `index.PILOT`（值同计划的字面量 `"2025美赛O奖论文"`）。
   写第二份字面量就是在两处维护同一个口径（`docs/mcm-suite-lessons.md` §4.8）。
2. 合集目录不存在 / 目录下没有 PDF → **当场抛**。`Path.rglob` 对不存在的目录**静默
   返回空**，于是「零依据地跑完 0 份并报告成功」凭空成立——`index.build` 与
   `io.sha256_tree` 各自都栽过这个坑，本模块按 fail-closed 处理，不靠它们兜。
3. `io.problem_of` 的实参传 `str(Path)`：计划写的是 `src.relative_to(io.ORIGIN)`
   （`PurePath`），实现里做的是 `Path(rel).parts`，两者都行；本模块统一成字符串形式，
   与 `index.build` 里那一处调用**逐字一致**。

## `--limit N`（N > 0 = 限样本跑）

只处理**排序后的前 N 份**（序 = `io.ORIGIN/<合集>` 下 `sorted(rglob("*.pdf"))`，
与 `index.build` 的 `all_pdfs` 同序，故稳定 ID 的到达顺序不受影响）。

限样本跑与全量跑**只有两处**行为不同，都是为了「限样本的绿不得冒充放行结论」：

1. `index` / `all` 的**聚合产物**（INDEX.md / TAGS.md / PROVENANCE.md）写到
   `build/cli-limit-<N>-products/`，**不碰入库产物**。`index.build` 的守卫是
   「`sample` 与 `out_dir=None` 同时出现即抛」——本入口显式给出 `out_dir`，
   不去绕它、也不去撞它。
2. 每份论文的派生物（md / figures / formulas）仍走**正常落点**（`io.md_path` /
   `io.figures_dir` / `io.formulas_dir`）：路径口径只有 `io` 一处权威，限样本跑
   不另造一套；它们逐份独立、确定性重写，真写坏了 `git status` / 重跑比对看得见。

末行带 `LIMITED` 后缀并列明实际份数，免得「前 N 份的耗时」被当成 43 份的耗时读。
"""
import argparse
import sys
import time
from pathlib import Path

if __package__ in (None, ""):  # 直接 `python tools/papers/cli.py` 也能跑
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.papers import figures, formulas, index, io, textmd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
# 限样本跑的聚合产物落点（不入库：根级 .gitignore 忽略 `build/`）。
LIMIT_PRODUCTS = ROOT / "build"

DEFAULT_COLLECTION = index.PILOT
STAGES = ("text", "figures", "formulas", "index", "all")


def originals(collection: str) -> list[Path]:
    """该合集下的全部原件 PDF（排序后）。

    **两处 fail-closed 都是刻意的**：`Path.rglob` 对不存在的目录不报错、只返回空，
    「空"等于"这个合集没有论文」会让整条流水线在零依据下报成功。合集名写错在本仓
    是活的风险（磁盘上是 `2023年美赛O奖论文`，别处写作 `2023美赛O奖论文`）。
    """
    root = io.ORIGIN / collection
    if not root.is_dir():
        raise FileNotFoundError(
            f"合集目录不存在：{root}——拒绝用空表冒充「该合集没有论文」")
    paths = sorted(root.rglob("*.pdf"))
    if not paths:
        raise ValueError(f"合集下没有任何 PDF：{root}")
    return paths


def run_stage(stage: str, collection: str, limit: int = 0) -> int:
    """跑一个阶段；返回进程退出码（0 = 成功）。"""
    paths = originals(collection)
    sample = paths if limit <= 0 else paths[:limit]
    if stage in ("index", "all") and limit > 0 and not sample:
        raise ValueError(f"--limit {limit} 取不到任何样本（合集共 {len(paths)} 份）")

    t0 = time.time()
    n = 0
    for src in sample:
        rel = str(src.relative_to(io.ORIGIN))
        prob = io.problem_of(rel)   # 题号从路径取；合集由调用方显式传入
        stem = src.stem

        if stage in ("text", "all"):
            textmd.extract(src, io.md_path(collection, prob, stem))
        if stage in ("figures", "all"):
            figures.extract_all(src, io.figures_dir(collection, prob, stem))
        if stage in ("formulas", "all"):
            formulas.extract_all(src, io.formulas_dir(collection, prob, stem))

        n += 1
        if n % 10 == 0:
            print(f"  ... {n}/{len(sample)}  {time.time() - t0:.1f}s", flush=True)

    if stage in ("index", "all"):
        if limit > 0:
            # **聚合产物限样本跑必须换落点**，否则会把 43 份的
            # INDEX.md/TAGS.md/PROVENANCE.md 覆写成 N 份的版本（`index.build` 的
            # docstring 逐字登记过这个形态）。
            out_dir = LIMIT_PRODUCTS / f"cli-limit-{limit}-products"
            index.build(collection, sample=sample, out_dir=out_dir)
            print(f"  （限样本跑的聚合产物写入 {out_dir.name}/，入库产物未动）",
                  flush=True)
        else:
            index.build(collection)

    dt = time.time() - t0
    suffix = ("" if limit <= 0
              else f"  ← LIMITED 只跑了前 {limit} 份，非全量、不得当放行依据")
    print(f"[{stage}] {collection}: {n} 份，耗时 {dt:.1f}s（{dt / max(n, 1):.2f}s/份）"
          f"{suffix}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="M6 语料流水线统一入口（原件只读；没有 watermark 阶段，见模块 docstring）")
    ap.add_argument("stage", choices=list(STAGES))
    ap.add_argument("--collection", default=DEFAULT_COLLECTION,
                    help=f"合集名（默认 {DEFAULT_COLLECTION}）")
    ap.add_argument("--limit", type=_nonneg, default=0, metavar="N",
                    help="只跑排序后的前 N 份（0 = 全量，默认）；限样本跑不会写入库"
                         "聚合产物（改写 build/cli-limit-N-products/），末行带 LIMITED。")
    args = ap.parse_args(argv)
    try:
        return run_stage(args.stage, args.collection, args.limit)
    except (FileNotFoundError, ValueError) as e:
        # fail-closed 的两条入口检查：错合集名 / 空合集不进循环、不报成功。
        print(f"[!] {e}", file=sys.stderr)
        return 2


def _nonneg(s: str) -> int:
    """`--limit` 的类型：非负整数（0 = 全量）。

    与 `tests/papers/report.py` 的 `limit_arg` 同口径（**同一处语义、两个入口**）：
    负数不接受。那里写全了理由——否定形谓词写成 `== 0` 时 `--limit -3` 是一次全量跑、
    却不等于 0，反向落点守卫会静默不触发。本入口没有落点守卫（它不写报告），
    但把负数当"小样本"读会更糟：`paths[:-3]` 会**静默少跑 3 份**。
    """
    try:
        v = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"不是整数：{s!r}") from None
    if v < 0:
        raise argparse.ArgumentTypeError(
            f"--limit 不接受负数（收到 {v}）：0 = 全量（默认），N > 0 = 只跑前 N 份。")
    return v


if __name__ == "__main__":
    raise SystemExit(main())
