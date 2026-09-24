"""路径映射、稳定 ID 与字节级读写。

本模块是唯一知道"原件在哪、派生物该去哪"的地方。各阶段模块只接收
显式路径，不自己拼路径。
"""
import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ORIGIN = REPO / "corpus" / "历届优秀论文"
DERIVED = REPO / "corpus" / "papers"

# 稳定 ID：P<年份>-<题号>-<序号>，序号为该题号下的到达顺序（1 起）
# 内容无关，故条号重排不会改变已发 ID——这正是教训三.1 要的。
_ID = re.compile(r"^P(\d{4})-([A-F])-(\d{2,})$")
# 合集名形如 "2025美赛O奖论文"，取开头的 4 位年份
_YEAR = re.compile(r"^(\d{4})")
# 合法题号。**必须是元组，不能写成字符串**：`problem in "ABCDEF"` 是子串
# 测试，会放行 "AB"、"" 这类输入，产出 P2025-AB-01 / P2025--01，而
# parse_stable_id 的正则一概拒绝——双向不变式就在 guard 声称拒绝的输入上破裂。
_PROBLEMS = tuple("ABCDEF")


def stable_id(collection: str, problem: str, seq: int) -> str:
    """由合集名、题号、序号生成稳定 ID。"""
    m = _YEAR.match(collection)
    if not m:
        raise ValueError(f"合集名不以 4 位年份开头: {collection!r}")
    if problem not in _PROBLEMS:
        raise ValueError(f"题号须为 A-F: {problem!r}")
    return f"P{m.group(1)}-{problem}-{seq:02d}"


def parse_stable_id(sid: str) -> tuple[str, str, int]:
    """stable_id 的逆运算，供双向解析校验用。"""
    m = _ID.match(sid)
    if not m:
        raise ValueError(f"不是合法稳定 ID: {sid!r}")
    return m.group(1), m.group(2), int(m.group(3))


def problem_of(rel: str) -> str:
    """从路径中取出 A-F 题号层。

    刻意**只返回题号、不返回合集**：合集名由调用方显式传入。
    曾试图从路径反推合集，但 2023 合集的布局是
    `2023美赛O奖论文/<中文长名>/A/xxx.pdf`，题号的上一层是子目录而非
    合集，反推会静默取错。显式传入消除这一整类歧义。
    """
    parts = [p for p in Path(rel).parts if p not in (".", "..")]
    for p in parts:
        if p in _PROBLEMS:
            return p
    raise ValueError(f"路径中找不到 A-F 题号层: {rel!r}")


def sha256_tree(collection: str) -> dict[str, str]:
    """记录某合集下全部原件的 sha256，供 A1 判据前后比对。

    这是"原件未被改动"从承诺变成事实的关键：流水线跑之前存一份，
    跑完再存一份，两份必须逐字相同。

    因此本函数**宁可抛异常也不返回空表**。A1 判据是"比对前后两张表"，
    两张空表相等——合集名写错时正好落到这里（磁盘上是 `2023年美赛O奖论文`，
    别处写作 `2023美赛O奖论文`），于是一份零哈希支撑的"原件未改动"绿票
    凭空成立。`Path.rglob` 对不存在的目录不报错、只返回空，
    所以这道检查必须由本函数自己做。
    """
    root = ORIGIN / collection
    if not root.is_dir():
        raise FileNotFoundError(root)
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*.pdf")):
        out[str(p.relative_to(ORIGIN))] = hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
    if not out:
        raise ValueError(f"合集下没有任何 PDF，拒绝返回空哈希表: {root}")
    return out


def md_path(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "md" / collection / problem / f"{stem}.md"


def figures_dir(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "figures" / collection / problem / stem


def formulas_dir(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "formulas" / collection / problem / stem


def write_bytes_checked(path: Path, data: bytes) -> None:
    """字节级写入并回读校验。

    回读**只能覆盖文件系统这一环**：写入被截断、被并发进程改写、路径
    落到了意料之外的位置——这些会当场暴露，而不是等到下游。
    它**抓不住行尾转换**：`write_bytes`/`read_bytes` 都是二进制路径，
    根本不经过 git，autocrlf 一类事故在此无从发生，也就无从被这里拦住。
    防那一类的是 `.gitattributes` 的 `-text` 规则加 `git add → blob →
    git checkout` 的字节往返，证据见 `tests/papers/reports/gitattributes-gate.txt`。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    if path.read_bytes() != data:
        raise IOError(f"写入回读不一致（写入被截断或路径被并发修改）：{path}")
