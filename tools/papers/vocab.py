"""受控词表的**字面匹配**（Task 6 阶段 5）。

刻意不做自由生成：字面匹配能给出**命中位置**，可复核、不虚构。由模型自由生成的标签
是**判断**而非事实——第一期反复踩过这个坑（`docs/mcm-suite-lessons.md` §一.1）。

## 词表是**开放的、可追加**的

用户 2026-09-26：「新遇到的模型/算法可以加入语料库」。故
`vocab/models.txt` 设计成**一行一词条 + 变体**，`load()` 每次现读现解析
（**不做缓存**——若缓存了，追加一行后在**同一个进程**里再 `load` 会拿不到新词，
那正是「改了却没生效」的静默形态）。文件格式与八大类来源见该文件的头部注释。

## 词边界的**实测依据**（不是风格选择）

不加词边界时，`logistic` 会命中 `logistics`、`SEM` 命中 22 篇而词边界下只有 2 篇、
`SHAP` 22→4、`DID` 27→23。逐词两口径对照见
`tests/papers/recon/ids-recon.txt` §4c。故：

* 变体里**含 ASCII 字母/数字**时，两侧加 `(?<![A-Za-z0-9])` / `(?![A-Za-z0-9])`；
* 变体**全是非 ASCII**（纯中文名）时，用**字面子串**——中文没有词边界这件事，
  给它加 lookaround 只会让它永不命中（那时"零命中"是**实现造成的**，不是语料事实）。

**不做 Unicode `\\b`**：`\\b` 在 Python `re` 里是 ASCII 词边界，对中文的语义与
上面那条规则不一致（`\\b主成分分析\\b` 在中文文本里恒不命中）；规则写在一起、
理由写在这里，免得下一个人"顺手"改成 `\\b`。

## 两条**实测换来的**细化（不是风格）

1. **markdown 标记不算边界**：变体自身含 `*`/`_` 时，邻接集合要**再加上 `*` 与 `_`**。
   实测：裸词边界下 `A*` 命中 **11** 篇，而其中有的是 md 的粗体标记 `**A**`——
   `A*` 从 `**A**` 里被切了出来（`(?<![A-Za-z0-9])` 看不见前面的 `*`）。加上之后
   `A*` 只剩真命中（`2504188` 的 `A* and GA`）。逐词对照见 `ids-report.txt`。
2. **缩写**：变体若**全由大写 ASCII 字母 + 数字/符号**构成（如 `DID` / `SEM` / `PCA` /
   `LSTM`），一律**大小写敏感**。实测：`re.I` 下 `DID` 命中 **23** 篇——因为英文动词
   `did` 就是它的小写形（`\\b` 挡不住）。这些论文写缩写时一律大写，故大小写敏感既
   没漏、又把动词滤掉了。

## `match()` 返回**全部出现位置**

不是"每词首次"——那是**调用方**（`index.py`）的取舍，不该烧进这里：
首次位置会被用来做指针，而**出现次数**是判据要独立复核的量
（`tests/papers/verify_ids.py` 的 M-a…M-e）。返回全部，两种用法都成立。
"""
import re
from dataclasses import dataclass
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent / "vocab" / "models.txt"
_ASCII_ALNUM = re.compile(r"[A-Za-z0-9]")


@dataclass(frozen=True)
class Term:
    """一个受控词条：`word` 是**规范词**（索引里一律显示它），`variants` 是变体（含规范词自身）。"""
    word: str
    variants: tuple[str, ...]


@dataclass(frozen=True)
class Hit:
    """一次命中：词条（规范词）+ 在文本里的**字符偏移**（`str` 下标，0 起）。"""
    word: str
    start: int


def load(path: Path | None = None) -> list[Term]:
    """读词表。`path=None` → `vocab/models.txt`。

    fail-closed：文件不存在、或**一个词条都没有**时**抛错**——返回空表会让
    `match()` 对任何文本都返回空，于是「零命中篇」变成 43/43，
    「词表缺口」被说成语料事实（`io.sha256_tree` 的先例：宁可抛也不返回空表）。
    """
    p = path or DEFAULT
    if not p.is_file():
        raise FileNotFoundError(f"词表文件不存在：{p}")
    terms: list[Term] = []
    seen: dict[str, str] = {}
    for ln in p.read_bytes().decode("utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        word = parts[0]
        if not word:
            raise ValueError(f"词表里有空词条：{ln!r}")
        variants = tuple(dict.fromkeys([x for x in parts if x]))
        # 规范词必须唯一：两行同名会让 `match` 产出两组同名 `Hit`，
        # 而索引按 `word` 归并——重复词条是**静默丢一组**的形态，当场抛。
        if word in seen:
            raise ValueError(f"词表里有重复规范词 {word!r}（另一行是 {seen[word]!r}）")
        seen[word] = ln
        terms.append(Term(word=word, variants=variants))
    if not terms:
        raise ValueError(f"词表里没有任何词条，拒绝返回空表：{p}")
    return terms


def _neighbour_class(variant: str) -> str:
    """词边界的**邻接集合**：ASCII 字母/数字；变体自身含 md 标记时再并上 `*` `_`。

    理由见模块 docstring 第 1 条（裸词边界下 `A*` 会从 md 粗体 `**A**` 里被切出来）。
    """
    cls = r"A-Za-z0-9"
    if "*" in variant or "_" in variant:
        cls += r"*_"
    return cls


def _flags(variant: str) -> int:
    """匹配标志。缩写（全大写 ASCII 字母，且没有小写字母）→ **大小写敏感**。

    理由见模块 docstring 第 2 条（`re.I` 下 `DID` 命中英文动词 `did`，23 篇）。
    """
    letters = [c for c in variant if c.isascii() and c.isalpha()]
    if len(letters) >= 2 and all(c.isupper() for c in letters):
        return 0
    return re.IGNORECASE


def _pattern(variant: str) -> str:
    """变体 → 正则片段。规则见模块 docstring（含 ASCII 字母/数字才加词边界）。"""
    esc = re.escape(variant)
    if not _ASCII_ALNUM.search(variant):
        return esc
    cls = _neighbour_class(variant)
    return rf"(?<![{cls}])" + esc + rf"(?![{cls}])"


def match(text: str, terms: list[Term] | None = None) -> list[Hit]:
    """在 `text` 里找全部命中，按 `(start, word)` 升序返回。

    `terms=None` → 现读默认词表（**不缓存**，理由见模块 docstring）。

    同一词条在同一位置只出一条（不同变体同位置命中时取**最长**的那个变体，
    口径写死在这里）：`Hit` 只带 `word`/`start` 两个字段，若不收敛，
    "同词同位置两条"会让调用方的计数凭空翻倍。
    """
    if terms is None:
        terms = load()
    out: list[Hit] = []
    for t in terms:
        best: dict[int, int] = {}          # start → 命中变体的长度（取最长）
        for v in t.variants:
            for m in re.finditer(_pattern(v), text, _flags(v)):
                s = m.start()
                if best.get(s, -1) < len(v):
                    best[s] = len(v)
        for s in best:
            out.append(Hit(word=t.word, start=s))
    out.sort(key=lambda h: (h.start, h.word))
    return out
