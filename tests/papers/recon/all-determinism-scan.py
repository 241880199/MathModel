"""D6 探针：`cli all` 的**抽取确定性**——跑前/跑后逐文件 blob 对账。

用法（每两步之间必须夹一次 `cli all`，且**必须在不同进程里**）：

    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-determinism-scan.py \
        snapshot build/all-determinism-s1.json
    PYTHONDONTWRITEBYTECODE=1 python -m tools.papers.cli all          # 第一遍
    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-determinism-scan.py \
        snapshot build/all-determinism-s2.json
    PYTHONDONTWRITEBYTECODE=1 python -m tools.papers.cli all          # 第二遍
    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-determinism-scan.py \
        snapshot build/all-determinism-s3.json
    PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/all-determinism-scan.py \
        compare tests/papers/reports/all-determinism.txt \
        build/all-determinism-s1.json build/all-determinism-s2.json build/all-determinism-s3.json

**为什么要两遍 `cli all`**：第一遍的「跑前」（s1）是**混合来源的残留状态**——本机
在 Task 7 开工前已有 Task 3/4/5 留下的 md/图表/公式，且开工后还跑过两次限样本
`cli all`（`--limit 3` / `--limit 17`，17 份 A/B/C 题被重写）。它与当前代码的输出
是否一致**不能**单独用来断定确定性。第二遍的两侧（s2 → s3）都由全套 `cli all` 产出，
那才是确定性的直判。`compare` 一次吃多个快照、逐对给一节。

**指纹一律用 `git hash-object`，不用裸 sha256**：本仓 `core.autocrlf=true`，
"入库的是哪一串字节"只有 git 知道（`corpus/papers/**` 有 `-text` 规则时两者相等，
但本探针的口径不依赖那条规则成立）。

**这不是判据脚本**（不在 `tests/papers/verify_*.py` 的派生集里）：它需要两遍约
10 分钟量级的 `cli all` 才能跑，放进每次汇总会让汇总不可运行。它产出的是**证据
文件** `tests/papers/reports/all-determinism.txt`，由 `verify_all.py` 的【4】读回并
核对（存在 / 入库 / 含份数与跑前跑后字样 / 不含 LIMITED）。
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DERIVED = ROOT / "corpus" / "papers"
PRODUCTS = ("INDEX.md", "TAGS.md", "PROVENANCE.md", "MODEL_MAP.md", "PROBLEM_TYPES.md")
SUBDIRS = ("md", "figures", "formulas")
BATCH = 120          # 命令行长度与单次进程开销的折中


def blobs(paths: list[Path]) -> dict[str, str]:
    """一批文件 → {仓库相对路径: git blob}。**失败即抛**（不静默留空）。"""
    out: dict[str, str] = {}
    for i in range(0, len(paths), BATCH):
        chunk = [str(p) for p in paths[i:i + BATCH]]
        r = subprocess.run(["git", "hash-object", "--", *chunk],
                           capture_output=True, cwd=str(ROOT))
        if r.returncode != 0:
            raise RuntimeError(f"git hash-object 失败：{r.stderr.decode('utf-8', 'replace')}")
        lines = r.stdout.decode("ascii", "replace").split()
        if len(lines) != len(chunk):
            raise RuntimeError(f"返回 {len(lines)} 条摘要、给了 {len(chunk)} 个文件")
        for p, h in zip(chunk, lines):
            out[Path(p).relative_to(ROOT).as_posix()] = h
    return out


def snapshot() -> dict:
    files: list[Path] = []
    for name in PRODUCTS:
        p = DERIVED / name
        if not p.is_file():
            raise FileNotFoundError(p)
        files.append(p)
    per_dir = {}
    for d in SUBDIRS:
        root = DERIVED / d
        if not root.is_dir():
            raise FileNotFoundError(root)
        got = sorted(x for x in root.rglob("*") if x.is_file())
        per_dir[d] = len(got)
        files += got
    table = blobs(files)
    return {"counts": per_dir, "products": {n: table[f"corpus/papers/{n}"] for n in PRODUCTS},
            "files": table}


def one_pass(lines: list[str], before: dict, after: dict, title: str) -> tuple[bool, int]:
    """一对快照的对账；返回（是否逐字节相同，入库产物 blob 变化数）。"""
    ok = True
    lines.append(f"## {title}")
    b_prod, a_prod = before["products"], after["products"]
    bad_prod = []
    for n in PRODUCTS:
        b, a = b_prod.get(n, "<缺>"), a_prod.get(n, "<缺>")
        if b != a:
            bad_prod.append(f"{n} {b} → {a}")
    lines.append(f"  入库产物：{len(PRODUCTS)} 份，blob 变了 **{len(bad_prod)}** 份"
                 + ("" if not bad_prod else "：" + "；".join(bad_prod)))
    ok &= not bad_prod
    b_all, a_all = before["files"], after["files"]
    touched: dict[str, set] = {}
    for d in SUBDIRS:
        b = {k: v for k, v in b_all.items() if k.startswith(f"corpus/papers/{d}/")}
        a = {k: v for k, v in a_all.items() if k.startswith(f"corpus/papers/{d}/")}
        only_b = sorted(set(b) - set(a))
        only_a = sorted(set(a) - set(b))
        diff = sorted(k for k in set(b) & set(a) if b[k] != a[k])
        same = not only_b and not only_a and not diff
        ok &= same
        lines.append(f"  {d:<10} 跑前 {len(b)} 个 · 跑后 {len(a)} 个 · "
                     f"只在跑前 {len(only_b)} · 只在跑后 {len(only_a)} · "
                     f"blob 变了 {len(diff)} ⇒ {'逐字节相同' if same else '**有变化**'}")
        if only_b:
            lines.append(f"     只在跑前（跑后没产出）：{only_b[:6]}")
        if only_a:
            lines.append(f"     只在跑后（跑前没有）：{only_a[:6]}")
        for k in diff[:6]:
            lines.append(f"     blob 变了：{k}　{b[k]} → {a[k]}")
        # 受影响的**篇**（从路径里取「题号/队号」两段；口径与产物目录同）
        for k in only_b + only_a + diff:
            parts = k.split("/")
            if len(parts) >= 6:
                touched.setdefault(d, set()).add(f"{parts[4]}/{parts[5]}")
    for d, tp in sorted(touched.items()):
        lines.append(f"  {d} 受影响的篇（{len(tp)} 篇）：{' · '.join(sorted(tp))}")
    return ok, len(bad_prod)


def compare(snaps: list[dict], titles: list[str]) -> tuple[str, bool]:
    first = snaps[0]
    n_md = len([k for k in first["files"] if k.startswith("corpus/papers/md/")])
    n_pdf = len(sorted((ROOT / "corpus" / "历届优秀论文" / "2025美赛O奖论文").rglob("*.pdf")))
    lines = ["`cli all` 的抽取确定性实测（D6）· 逐文件 blob 对账",
             "=" * 78,
             "口径：指纹 = `git hash-object`（不是裸 sha256：本仓 `core.autocrlf=true`）；",
             "对账的是**全量**、不是抽样——`corpus/papers/{md,figures,formulas}` 下的每一个文件",
             "+ 五份入库产物（INDEX/TAGS/PROVENANCE/MODEL_MAP/PROBLEM_TYPES）。",
             "",
             "命令（可复现）：",
             "  python tests/papers/recon/all-determinism-scan.py snapshot <n>.json   # 每步之间夹一次 `cli all`",
             "  python -m tools.papers.cli all",
             "  python tests/papers/recon/all-determinism-scan.py compare <out.txt> <n1>.json <n2>.json [...]",
             "",
             f"样本：{n_md} 份 md（全量）· {n_pdf} 份原件（`cli all` 的输入全集；"
             f"份数是**当场从磁盘数出来的**，不是手抄的）",
             "",
             "**为什么有两遍**：第一遍的「跑前」是**混合来源的残留状态**——本轮开工前"
             "本机已经跑过 `--limit 3` / `--limit 17` 两次限样本 `cli all`（17 份 A/B/C 题被",
             "重写过），故它与当前代码的输出是否一致**不能**单独用来断定确定性。",
             "第二遍的两侧**都**由同一次全套 `cli all` 产出，它才是确定性的直判。",
             ""]
    passes = [one_pass(lines, b, a, titles[i]) for i, (b, a) in enumerate(zip(snaps, snaps[1:]))]
    results = [r[0] for r in passes]
    prods = [r[1] for r in passes]
    for _ in passes:
        lines.append("")
    ok = all(results)
    lines.append("## 结论（三个问题分开答，**不合并**）")
    lines.append("  问 1「**当前代码**在同一输入状态下能否逐字节复现」——"
                 f"直判 = 最后一遍对账（{titles[-1]}）："
                 f"**{'逐字节相同 ✓' if results[-1] else '有差异 ✗'}**")
    if len(results) > 1:
        lines.append("  问 2「跑前那份**残留状态**是不是当前代码的产物」——"
                     f"对账 = 第一遍（{titles[0]}）："
                     f"**{'相同' if results[0] else '有差异（见上逐条与受影响篇）'}**")
        lines.append("      有差异**不等于**流水线非确定性：当前代码对同一输入两次跑出"
                     "同一串字节（问 1 已判），故差异只能来自**跑前状态的来源**——"
                     "它不是 `cli all` 的产物（`tools/papers/cli.py` 由 Task 7 新建，"
                     "本机此前从未跑过 `cli all`），而是出自更早的别的路径。"
                     "**本探针不声称知道那是哪一条路径**（要另一份实验）。")
    lines.append("  问 3「**入库产物**（INDEX/TAGS/PROVENANCE/MODEL_MAP/PROBLEM_TYPES）"
                 "会不会被重跑改动」——各遍的 blob 变化数："
                 + " / ".join(str(n) for n in prods)
                 + "（这个数在各节首行**逐份具名**给出，此处只是汇总）")
    lines.append(f"  本探针的退出码 = {'0' if ok else '1'}（= 各遍结果的合取；"
                 f"问 2 有差异时它也会是 1，**不要**把那个 1 读成「流水线不确定」——"
                 f"读上面三个问题各自的答案）")
    return "\n".join(lines) + "\n", ok


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "snapshot" and len(sys.argv) == 3:
        snap = snapshot()
        path = Path(sys.argv[2])
        path.write_bytes(json.dumps(snap).encode("utf-8"))
        print(f"{path.name}: " + json.dumps(snap["counts"], ensure_ascii=False))
        return 0
    if mode == "compare" and len(sys.argv) >= 5:
        out = Path(sys.argv[2])
        snaps = [json.loads(Path(p).read_bytes().decode("utf-8")) for p in sys.argv[3:]]
        names = [Path(p).name for p in sys.argv[3:]]
        titles = [f"{names[i]} → {names[i + 1]}" for i in range(len(snaps) - 1)]
        text, ok = compare(snaps, titles)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(text.encode("utf-8"))
        print(text, end="")
        return 0 if ok else 1
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
