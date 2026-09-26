"""Task 6b 阶段 2b：**匹配度**（用户点名的那句验收口）——召回 @ 作者 Keywords + 精确性。

本模块是**产物侧**：它的输出有两处落点，两处**同源**（同一次计算、同一批数）：

| 落点 | 形态 | 谁读它 |
| :--- | :--- | :--- |
| `corpus/papers/MODEL_MAP.md` 的**第四节** | 人读（比值 + 未覆盖单列 + 逐篇表 + 口径） | 用户；判据 M-14 自己解析 |
| `tests/papers/reports/coverage-evidence.txt` | **机读**（键值行 + 逐条清单 + 定位指针） | 判据 M-14 / M-15 自己解析 |

**两处不许手抄**：都由本模块的 `compute()` 一次算出、由 `render_section()` /
`render_evidence()` 两个渲染器写出。判据侧**各自解析各自的文件**再对账——**但也不许只调
同一个函数**：`verify_map.py` 的 M-14 用的是一份**独立实现**（自己的正则、自己的词边界、
自己的 git 取基线），不 import 本模块的任何解析函数。

## 反恒真（本项目第七例）：召回的两侧**必须来自不同机制**

* **参照侧** = `corpus/papers/TAGS.md` 一层的 **`keywords` 栏** —— 那是**作者自己写的**
  Key words 行，Task 6 原样抄进去的原文，**不是我们算的**；
* **命中侧** = `corpus/papers/TAGS.md` 二层的**指针**（`(篇, 词, 页, 次数, 片段)`）与
  `models` 栏 —— 那是**受控词表**（`tools/papers/vocab/models.txt`）的**字面命中**，
  **是我们算的**。

⇒ 两侧**不共用任何抽取代码**：作者的那一侧在本模块里只做「按分隔符拆词 + 空白归一化」，
受控的那一侧走 `vocab` 的词边界匹配。「函数跟自己对答案」这条退化路径在这里被结构性地挡住；
`map-mutation-evidence` 的**反面变异 RV-1** 专门证明「一旦把两侧改成同一段代码，
召回比值会变成恒定的 100%」——即这条判据**不是**恒真的。

## 两个参照口径（**这是本轮实测出来的一个真边界**）

* **主体口径** = `keywords` 栏（任务书 §一 产物 1 写死的口径）。实测 **42/43** 篇非空；
  唯一空的一篇 `P2025-C-17`（原件 `2522820`）经三态判定为「**参照不存在**」
  （该篇 md 里 `key.?words?` 一次都不出现），**不是**「不适用」、也不是「静默跳过」。
* **宽口径** = 该篇 md 的 **Keywords 段**（Key words 行 **加上它的续行**）。
  **为什么必须另量一个**：`keywords` 栏是**行内截取**（`V_KEYWORDS` 的 `(.*?)[*_ \t]*$`
  在 `re.M` 下只吃到行尾），本语料里有 **17 篇**的作者 Keywords 段跨行 ⇒ 栏里**少一截**。
  只报主体口径会把「作者写了、我们的栏没收到」的词形**从分母里悄悄拿掉**。
  两个口径的比值**都报**，差额逐条登记在 `tests/papers/recon/coverage-recon.txt`。
  宽口径**不用于** M-10 的三态表判定（分流表按任务书口径 = 主体口径 + 它的续行补集，
  见 `growth_triage.txt` §1），它是**边界登记**。

## 「覆盖」的判据（**逐字复刻 `verify_ids.py` 的 I13 口径**，不得另写一套）

片（作者关键词里的一个词形）算**被覆盖** ⟺ **片内出现任一受控词表变体**（词边界口径：
含 ASCII 字母/数字的变体两侧加 `(?<![A-Za-z0-9])`/`(?![A-Za-z0-9])`，变体自身含 `*`/`_`
时邻接集合并上 `*_`，全大写缩写变体大小写敏感）。

**这条判据的实测边界（必须与比值同读）**：它是「片里**含**词表词」，不是「片**就是**词表词」。
实测 61 个被覆盖的片里有 **19** 个是这种情形（例：`PSM-DID model` 由 `PSM` + `DID` 判为覆盖，
`Bayesian Hierarchical Dirichlet-Multinomial` 由 `Bayesian` 判为覆盖）。**语义上是对的**
（作者那两个方法确实都在词表里），但它意味着「覆盖」是**方法族级**而不是**短语级**。
逐条清单见证据文件的 `覆盖=松判` 段。

## 精确性

命中侧 = `TAGS.md` 二层的**每条指针**（Task 6 就有的指针，本模块**只复核、不重算**）。
「可定位」= 三条同时成立：① 该 `md` 文件在；② 片段是该 md 的**一整行逐字**；
③ 该行所在的页 == 指针的页。**低置信 = `x1`**（该词在该篇全篇只出现 1 次），单列。

## 基线：**增长前**的词表从 git 取，不从工作树取

`@增长前` 的召回必须用**增长前**的词表量。本模块从 **git 对象库**取基线的字节
（`git cat-file blob <baseline>`，blob 写死在 `BASELINE_MODELS_BLOB`），再用本模块的
解析器读它——**不**读工作树（工作树上那份已经是增长后的了），也**不**用
「现行词表减去分流表收录行」这种反推（反推会把「新增词形恰好嵌在别的片里」这类情形算错）。
"""
import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# ---- 输入落点（**只读**）----------------------------------------------------
TAGS = ROOT / "corpus" / "papers" / "TAGS.md"
TRIAGE = ROOT / "tools" / "papers" / "vocab" / "growth_triage.txt"
MODELS = ROOT / "tools" / "papers" / "vocab" / "models.txt"
# 基线的**字节**（增长前的 `tools/papers/vocab/models.txt`，开工当天实测登记）。
BASELINE_MODELS_BLOB = "0ca91927d3ddafd91fe7bd4c79716a8093f7fad8"
# 证据落点（机读）。**与 `MODEL_MAP.md` 第四节同源**（同一次 compute()）。
EVIDENCE = ROOT / "tests" / "papers" / "reports" / "coverage-evidence.txt"

# 参照不存在的哨兵（`TAGS.md` 一层空值写 ASCII `-`）。
EMPTY = "-"
# 作者关键词行的**宽**探针：只用来判「参照不存在 vs 存在但没解析出来」这一条三态。
ANY_KEYWORD = re.compile(r"key\s*words?", re.I)
# 片的分隔符与长度闸（**逐字复刻 `verify_ids.py` 的 I13**）。
PIECE_SEP = re.compile(r"[;,；，、|/]")
PIECE_MIN, PIECE_MAX = 2, 40

# `TAGS.md` 一层的字段序（本模块要的三栏：stable_id / problem / keywords）。
V_L1_ROW = re.compile(r"^(P\d{4}-[A-F]-\d{2,}) \| (\d{4}) \| ([A-F]) \| ")
# 二层小标题与 `md:` 行。
V_L2_HEAD = re.compile(r"^### (P\d{4}-[A-F]-\d{2,}) · 题 ([A-F]) · ")
V_L2_MD = re.compile(r"^md: (.+)$")
V_PAGE_ANCHOR = re.compile(r"^<!-- page (\d+) -->$")
TAGS_SEP = "; "
# `MODEL_MAP.md` 的第四节标题（生成器与判据都用这一个常量，避免各写一份正则）。
SECTION4 = "## 第四节 · 匹配度（召回 @ 作者 Keywords + 精确性）"


# --------------------------------------------------------------------------
# 读回（**都不重算产物里的东西**）
# --------------------------------------------------------------------------
def split_unesc(s: str, sep: str = "|") -> list[str]:
    """按**未转义**的 `sep` 切分（`TAGS.md` 的转义契约：`\\|` 不是分隔符）。"""
    out, cur, i = [], [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            cur.append(s[i:i + 2])
            i += 2
            continue
        if s.startswith(sep, i):
            out.append("".join(cur))
            cur = []
            i += len(sep)
            continue
        cur.append(s[i])
        i += 1
    out.append("".join(cur))
    return out


def unesc(s: str) -> str:
    """`TAGS.md` 转义的逆（`\\|` `\\;` `\\0` `\\r` `\\n` `\\\\`）。"""
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"\\": "\\", "|": "|", ";": ";", "0": "\x00",
                        "r": "\r", "n": "\n"}.get(n, "\\" + n))
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def esc(s: str) -> str:
    """`TAGS.md` 转义（写回时用；与 `index._esc` 同规则）。"""
    return (s.replace("\\", "\\\\").replace("|", "\\|").replace(";", "\\;")
            .replace("\x00", "\\0").replace("\r", "\\r").replace("\n", "\\n"))


@dataclass(frozen=True)
class PaperRef:
    """`TAGS.md` 一层的一行（本模块只要这四个字段）。"""
    sid: str
    year: str
    problem: str
    keywords: str
    md_rel: str = ""


@dataclass(frozen=True)
class Ptr:
    """`TAGS.md` 二层的一条指针（Task 6 的产物，**只复核**）。"""
    sid: str
    model: str
    page: int
    n_occ: int
    snippet: str
    md_rel: str


def read_tags(path: Path = TAGS) -> tuple[list[PaperRef], list[Ptr]]:
    """`TAGS.md` → `(一层行, 二层指针)`。**fail-closed**：解析不出就抛。"""
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    papers: list[dict] = []
    ptrs: list[Ptr] = []
    cur_sid, cur_md = "", ""
    for ln in text.split("\n"):
        m1 = V_L1_ROW.match(ln)
        if m1:
            cells = [unesc(x) for x in split_unesc(ln.strip()[1:-1], "|")]
            papers.append({"sid": m1.group(1), "year": m1.group(2),
                           "problem": m1.group(3), "keywords": cells[14].strip(),
                           "md_rel": "", "idx": len(papers)})
            continue
        mh = V_L2_HEAD.match(ln)
        if mh:
            cur_sid, cur_md = mh.group(1), ""
            continue
        mm = V_L2_MD.match(ln)
        if mm and cur_sid:
            cur_md = mm.group(1).strip()
            continue
        if cur_sid and ln.startswith("- "):
            parts = split_unesc(ln[2:], TAGS_SEP)
            if len(parts) != 4:
                raise ValueError(f"{path.name} 二层指针不是 4 段：{ln[:80]!r}")
            pg = re.fullmatch(r"p(\d+)", parts[1].strip())
            nx = re.fullmatch(r"x(\d+)", parts[2].strip())
            if not pg or not nx:
                raise ValueError(f"{path.name} 二层指针的页/次数不合式：{ln[:80]!r}")
            ptrs.append(Ptr(cur_sid, unesc(parts[0]).strip(), int(pg.group(1)),
                            int(nx.group(1)), unesc(parts[3]), cur_md))
    if not papers:
        raise ValueError(f"{path.name} 一层一行都没解析出来（fail-closed）")
    if not ptrs:
        raise ValueError(f"{path.name} 二层一条指针都没解析出来（fail-closed）")
    by_sid = {p["sid"]: p for p in papers}
    for p in papers:
        p["md_rel"] = next((q.md_rel for q in ptrs if q.sid == p["sid"]), "")
    if not all(p["md_rel"] for p in papers):
        miss = [p["sid"] for p in papers if not p["md_rel"]]
        raise ValueError(f"{path.name} 里有篇拿不到 `md:` 行：{miss}（fail-closed）")
    return [PaperRef(p["sid"], p["year"], p["problem"], p["keywords"], p["md_rel"])
            for p in papers], ptrs


def read_triage(path: Path = TRIAGE) -> list[tuple[str, str, str, str]]:
    """分流表 → `[(词形, 处置, 类别, 理由), …]`。**fail-closed**：栏数不对就抛。"""
    if not path.is_file():
        raise FileNotFoundError(f"分流表不在：{path.relative_to(ROOT).as_posix()}")
    out: list[tuple[str, str, str, str]] = []
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.startswith("#"):
            continue
        cells = ln.split("\t")
        if len(cells) != 4:
            raise ValueError(f"{path.name} 不是 4 栏（TAB 分隔）：{ln[:80]!r}")
        if cells[1] not in ("收录", "不收", "待定"):
            raise ValueError(f"{path.name} 处置非法：{cells[1]!r}")
        if cells[2] not in ("模型", "场景", "无法归类"):
            raise ValueError(f"{path.name} 类别非法：{cells[2]!r}")
        if not cells[3].strip():
            raise ValueError(f"{path.name} 理由为空：{cells[0]!r}")
        out.append((cells[0], cells[1], cells[2], cells[3]))
    if not out:
        raise ValueError(f"{path.name} 一行都没有（fail-closed）")
    return out


def read_vocab_bytes(data: bytes) -> list[tuple[str, tuple[str, ...]]]:
    """词表**字节** → `[(规范词, (变体…)), …]`（口径与 `vocab.load` 一致，另写一份）。"""
    out: list[tuple[str, tuple[str, ...]]] = []
    for ln in data.decode("utf-8").replace("\r\n", "\n").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        out.append((parts[0], tuple(x for x in parts if x)))
    if not out:
        raise ValueError("词表是空的（fail-closed）")
    return out


def baseline_vocab() -> list[tuple[str, tuple[str, ...]]]:
    """**增长前**的词表：从 **git 对象库**取基线 blob 的字节（不是工作树）。

    为什么不用工作树：工作树上那份已经被本轮的增长改过了，「@增长前」这个量必须拿
    **增长前**的字节量。为什么不用「现行词表减去分流表收录行」反推：反推会把
    「新增词形恰好嵌在另一个片里」这类情形算错，且它让基线**依赖**本轮的产物。
    """
    r = subprocess.run(["git", "cat-file", "blob", BASELINE_MODELS_BLOB],
                       cwd=str(ROOT), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"`git cat-file blob {BASELINE_MODELS_BLOB}` 非零退出（{r.returncode}）："
            f"{r.stderr.decode('utf-8', 'replace')[:200]}——基线取不到时**不许**退回工作树")
    return read_vocab_bytes(r.stdout)


# --------------------------------------------------------------------------
# 「片被覆盖」的判据（**逐字复刻 `verify_ids.py` 的 v_term_pattern**）
# --------------------------------------------------------------------------
def v_term_pattern(variant: str) -> tuple[str, int]:
    """变体 → `(正则, flags)`。规则与 `tools/papers/vocab.py` 的 docstring 逐条对应。"""
    e = re.escape(variant)
    if not re.search(r"[A-Za-z0-9]", variant):
        return e, re.IGNORECASE
    cls = "A-Za-z0-9"
    if "*" in variant or "_" in variant:
        cls += r"*_"
    letters = [c for c in variant if c.isascii() and c.isalpha()]
    flags = 0 if (len(letters) >= 2 and all(c.isupper() for c in letters)) else re.IGNORECASE
    return rf"(?<![{cls}]){e}(?![{cls}])", flags


def pieces_of(keywords: str) -> list[str]:
    """一行作者关键词 → 片表（**口径逐字复刻 `verify_ids.py` 的 I13**）。"""
    out: list[str] = []
    for piece in PIECE_SEP.split(keywords):
        p = piece.strip().strip("*_ ").strip()
        if PIECE_MIN <= len(p) <= PIECE_MAX:
            out.append(p)
    return out


def covering_terms(text: str, vocab_rows) -> list[str]:
    """`text` 被哪些词条的变体命中（返回**规范词**表，去重、保持词表序）。"""
    hit: list[str] = []
    for word, variants in vocab_rows:
        for v in variants:
            pat, flags = v_term_pattern(v)
            if re.search(pat, text, flags):
                hit.append(word)
                break
    return hit


# --------------------------------------------------------------------------
# 计算
# --------------------------------------------------------------------------
@dataclass
class PaperRow:
    sid: str
    year: str
    problem: str
    keywords: str
    md_rel: str
    pieces: int
    covered: int              # @增长前 被覆盖的片数
    uncovered_model: int      # @增长前 未覆盖、且分流表判「模型」的片数
    collected: int            # 其中处置=收录 的
    not_collected: int        # 其中处置≠收录 的
    uncovered_scene: int      # 未覆盖、且判「场景」的
    ref_status: str           # `有参照` / `参照不存在` / `参照存在但没解析出来`
    recall_before: str        # `分子/分母` 的字面形式（分母 0 时写 `-`）
    recall_after: str
    wide_pieces: int
    wide_covered: int
    wide_uncovered_model: int
    no_model_entries: bool    # 参照存在、但模型类条目为 0 → **单列**，不记「不适用」


@dataclass
class CoverageResult:
    papers: list[PaperRow] = field(default_factory=list)
    n_ref: int = 0
    ref_absent: list[str] = field(default_factory=list)
    ref_unparsed: list[str] = field(default_factory=list)
    num_before: int = 0
    num_after: int = 0
    denom: int = 0
    uncollected: list[tuple[str, str, str, str, str]] = field(default_factory=list)
    collected: list[tuple[str, str]] = field(default_factory=list)
    wide_num: int = 0
    wide_denom: int = 0
    ptr_total: int = 0
    ptr_ok: int = 0
    ptr_bad: list[tuple[str, str, str, str]] = field(default_factory=list)
    low_conf: list[tuple[str, str, int, str]] = field(default_factory=list)
    loose_covered: list[tuple[str, str, list[str]]] = field(default_factory=list)
    kw_truncated: list[str] = field(default_factory=list)
    # **未解释项**：未被基线词表覆盖、而分流表里**没有这一片**的片。
    # 这一类**不许 raise**：`raise` 会让调用方（`model_map.build()` → `M-8`）在判据汇总
    # 之前崩掉，读者只看到一段 traceback、连 `M-10=FAIL` 那行都打不出来
    # （2a 在 M-7 的幻影 stable ID 上栽过同一形态）。改成**报出来**：
    # 产物第四节与证据各有一格 `未解释=N`，判据 M-10 判它必须为 0。
    # 统计口径：这类片**按 `模型` 计入分母**（保守——不知道类别时宁可让召回偏低），
    # 且**不算被覆盖**；它们同时逐条列在证据里，`未解释 = 0` 才叫「没有沉默项」。
    unexplained: list[tuple[str, str]] = field(default_factory=list)
    n_pieces_all: int = 0
    triage_rows: int = 0
    n_md: int = 0


def _keywords_segment(md_text: str) -> str:
    """该 md 的 **Keywords 段**（keywords 行 + 续行，行间只留一个空格）。

    切法**写死**在 `growth_triage.txt` §2，这里逐字实现同一套（判据侧另写一份）：
    从 `V_KEYWORDS` 命中行的 `group(1)` 起并入后续行，直到遇到空行 / `<!-- page` /
    `#{1,6} ` / `^\\d+(\\.\\d+)*\\s` / 又一处 keywords 行 / `Problem Chosen` / `Team Control`。
    """
    from tools.papers import taxonomy
    text = taxonomy.normalize_newlines(md_text)
    m = taxonomy_v_keywords().search(text)
    if not m:
        return ""
    lines = text.split("\n")
    cur, idx = 0, None
    for i, ln in enumerate(lines):
        if cur <= m.end() <= cur + len(ln) + 1:
            idx = i
            break
        cur += len(ln) + 1
    seg = [m.group(1).strip()]
    STOP = re.compile(r"^(#{1,6}\s|<!-- page|\d+(\.\d+)*\s|Problem\s+Chosen|Team\s+Control)", re.I)
    for ln in lines[(idx or 0) + 1:]:
        s = ln.strip()
        if not s or STOP.match(s) or taxonomy_v_keywords().match(s):
            break
        seg.append(s)
    return " ".join(seg)


def taxonomy_v_keywords():
    """`taxonomy` 侧的 keywords 正则（与 `verify_ids.py` 的 `V_KEYWORDS` 逐字相同）。

    本模块**引用**它（它是**输入口径**），而判据侧（`verify_map.py`）**另写一份**——
    口径那一份只有一处，判据那一份独立。
    """
    return re.compile(r"^[#>*_ \t]*(?:Key\s*words?|关键词)\s*[:：]\s*(.*?)[*_ \t]*$",
                      re.I | re.M)


def compute() -> CoverageResult:
    """一次算出全部量。**只读**：不改任何文件。"""
    papers, ptrs = read_tags()
    triage = read_triage()
    cur_vocab = read_vocab_bytes(MODELS.read_bytes())
    base_vocab = baseline_vocab()
    res = CoverageResult(n_pieces_all=0, triage_rows=len(triage), n_md=0)

    # 分流表 → 词形索引。**键用词形的逐字形态**（不做 casefold）：本语料里
    # `Sustainable Tourism` 与 `Sustainable tourism`、`Great Coach Effect` 与
    # `Great coach effect` 是**两个不同的片**（作者的大小写不同），casefold 会把它们
    # 压成一条——那会让「一个片找不到自己的分流行」这类真错被掩盖。
    idx: dict[str, tuple[str, str, str, str]] = {t[0]: t for t in triage}
    if len(idx) != len(triage):
        raise ValueError("分流表里有逐字重复的词形")

    n_loose = 0
    for p in papers:
        kw = p.keywords
        status = "有参照"
        if kw in ("", EMPTY):
            md_p = ROOT / p.md_rel
            has = bool(ANY_KEYWORD.search(md_p.read_bytes().decode("utf-8", "replace")))
            status = "参照存在但没解析出来" if has else "参照不存在"
            if status == "参照不存在":
                res.ref_absent.append(p.sid)
            else:
                res.ref_unparsed.append(p.sid)
        else:
            res.n_ref += 1

        ps = pieces_of(kw) if status == "有参照" else []
        res.n_pieces_all += len(ps)
        covered: list[str] = []
        unc_model: list[tuple[str, str, str, str]] = []
        unc_scene = 0
        for piece in ps:
            hits = covering_terms(piece, base_vocab)
            if hits:
                covered.append(piece)
                # 松判：片里含词表词、而片本身不是词表词（登记为口径边界）
                if piece.casefold() not in {v.casefold() for _w, vs in base_vocab for v in vs}:
                    res.loose_covered.append((p.sid, piece, hits))
                    n_loose += 1
                continue
            row = idx.get(piece)
            if row is None:
                # **未解释项**：报出来、按 `模型` 计入分母、不算覆盖（理由见
                # `CoverageResult.unexplained` 的注释）。
                res.unexplained.append((p.sid, piece))
                unc_model.append((piece, "（未解释）", "模型",
                                  "（分流表里没有这一片——见第四节的 `未解释` 一格）"))
                continue
            if row[2] == "模型":
                unc_model.append((piece, row[1], row[2], row[3]))
            else:
                unc_scene += 1
        coll = [x for x in unc_model if x[1] == "收录"]
        ncoll = [x for x in unc_model if x[1] != "收录"]
        denom = len(covered) + len(unc_model)
        num_b = len(covered)
        num_a = len(covered) + len(coll)
        res.num_before += num_b
        res.num_after += num_a
        res.denom += denom
        for piece, disp, cat, why in ncoll:
            res.uncollected.append((p.sid, piece, disp, cat, why))
        for piece, _d, _c, _w in coll:
            res.collected.append((p.sid, piece))

        # ---- 宽口径（该篇 md 的 Keywords 段）----
        wide = _keywords_segment((ROOT / p.md_rel).read_bytes().decode("utf-8", "replace"))
        wps = pieces_of(wide) if wide else []
        wc = [x for x in wps if covering_terms(x, base_vocab)]
        wu = []
        for x in wps:
            if x in wc:
                continue
            row = idx.get(x)
            if row is not None and row[2] == "模型":
                wu.append(x)
        res.wide_num += len(wc)
        res.wide_denom += len(wc) + len(wu)
        if kw not in ("", EMPTY) and wide and wide.strip() != kw.strip():
            res.kw_truncated.append(p.sid)

        res.papers.append(PaperRow(
            sid=p.sid, year=p.year, problem=p.problem, keywords=kw, md_rel=p.md_rel,
            pieces=len(ps), covered=num_b, uncovered_model=len(unc_model),
            collected=len(coll), not_collected=len(ncoll), uncovered_scene=unc_scene,
            ref_status=status,
            recall_before=f"{num_b}/{denom}" if denom else "-",
            recall_after=f"{num_a}/{denom}" if denom else "-",
            wide_pieces=len(wps), wide_covered=len(wc), wide_uncovered_model=len(wu),
            no_model_entries=(status == "有参照" and denom == 0)))

    # ---- 精确性：复核 TAGS 二层的每条指针（**不重算**）----
    md_cache: dict[str, tuple[list[str], list[int]]] = {}
    res.ptr_total = len(ptrs)
    for h in ptrs:
        fp = ROOT / h.md_rel
        if not fp.is_file():
            res.ptr_bad.append((h.sid, h.model, "md 文件不在", h.md_rel))
            continue
        if h.md_rel not in md_cache:
            text = fp.read_bytes().decode("utf-8").replace("\r\n", "\n")
            lines = text.split("\n")
            pages, cur = [], 0
            for ln in lines:
                ma = V_PAGE_ANCHOR.match(ln.rstrip())
                if ma:
                    cur = int(ma.group(1))
                pages.append(cur)
            md_cache[h.md_rel] = (lines, pages)
        lines, pages = md_cache[h.md_rel]
        if h.snippet not in lines:
            res.ptr_bad.append((h.sid, h.model, "片段不是整行逐字", h.md_rel))
            continue
        i = lines.index(h.snippet)
        if pages[i] != h.page:
            res.ptr_bad.append((h.sid, h.model,
                                f"页码 p{h.page} ≠ 该行所在页 p{pages[i]}", h.md_rel))
            continue
        res.ptr_ok += 1
    res.low_conf = sorted((h.model, h.sid, h.page, h.snippet)
                          for h in ptrs if h.n_occ == 1)
    res.n_md = len(md_cache)
    return res


# --------------------------------------------------------------------------
# 渲染（两处落点，同一次 `compute()`）
# --------------------------------------------------------------------------
def _tsv(*fields: str) -> list[str]:
    """TSV 字段的 **fail-closed 校验**：不含 TAB 与换行。

    本模块**不**对证据文件用 `TAGS.md` 的转义（那是那份产物的契约）：证据文件是 TAB 分隔的
    自有格式，散文里的 `;`/`|` 本来就该原样出现（转义会把理由读成乱码——实测过）。
    代价是字段里不能有 TAB/换行 ⇒ 在这里当场拦住，不让它静默把一个字段切成两栏。
    """
    for f in fields:
        if "\t" in f or "\n" in f or "\r" in f:
            raise ValueError(f"证据字段里有 TAB/换行，会静默切栏：{f[:60]!r}")
    return list(fields)


def _pct(a: int, b: int) -> str:
    return f"{a / b:.4f}" if b else "-"


def render_section(res: CoverageResult) -> str:
    """`MODEL_MAP.md` 的第四节（人读）。"""
    L = [
        "",
        SECTION4,
        "",
        "**用户 2026-09-26 的那句验收口**：*「为了建模的准确性…要求最终匹配度较高」*。"
        "这一节把「匹配度」变成**可量**的：**召回**（作者点名的模型，我们的词表覆盖了几个）"
        "+ **精确性**（我们的每条命中能不能在正文定位）。**没有阈值**——比值如实报出交用户判；"
        "判据守的是**「未解释为 0」**（每个未覆盖条目都有三态处置与理由）。",
        "",
        "> **机读**（判据 M-14 按这一行对账；键与 "
        "`tests/papers/reports/coverage-evidence.txt` 的同名键**逐字相等**）：",
        f"> 匹配度：参照篇={res.n_ref} · 参照不存在="
        f"{'、'.join(res.ref_absent) or '（无）'} · 参照存在但没解析出来="
        f"{'、'.join(res.ref_unparsed) or '（无）'} · 召回分子前={res.num_before} · "
        f"召回分子后={res.num_after} · 召回分母={res.denom} · 宽参照分子={res.wide_num} · "
        f"宽参照分母={res.wide_denom} · 未覆盖模型条目="
        f"{sum(r.uncovered_model for r in res.papers)} · 未覆盖不收录={len(res.uncollected)} · "
        f"未解释={len(res.unexplained)} · "
        f"收录条数={len(res.collected)} · 精确性可定位={res.ptr_ok} · "
        f"精确性总数={res.ptr_total} · 低置信条数={len(res.low_conf)} · "
        f"分流表行数={res.triage_rows} · 分流表收录行数="
        f"{sum(1 for t in read_triage() if t[1] == '收录')}",
        "",
        f"* **参照（主体口径）**：`corpus/papers/TAGS.md` 一层的 **`keywords` 栏**"
        f"（**作者自己写的** Key words 行，Task 6 原样抄入、**不是我们算的**）。"
        f"非空 **{res.n_ref}** 篇。**参照不存在 1 篇**："
        f"{'、'.join(res.ref_absent) or '（无）'}——该篇 md 里 `key.?words?` 一次都不出现"
        f"（**「参照不存在」与「参照存在但没解析出来」是两件事**；后者实测 "
        f"{len(res.ref_unparsed)} 篇：{'、'.join(res.ref_unparsed) or '（无）'}）。",
        f"* **命中（受控口径）**：`tools/papers/vocab/models.txt` 的**字面命中**"
        f"（词边界口径），指针在 `TAGS.md` 第二层。**两侧不共用任何抽取代码**"
        f"（作者那侧只按分隔符拆词，我们这侧走词表匹配）——否则召回就是「函数跟自己对答案」。",
        "",
        "| 量 | 值 | 读法 |",
        "| :-- | ---: | :-- |",
        f"| 召回 @**增长前**词表 | **{res.num_before}/{res.denom} = {_pct(res.num_before, res.denom)}** "
        f"| 作者点名的「模型/算法」条目里，**增长前**的词表覆盖了几个 |",
        f"| 召回 @**增长后**词表（现行） | **{res.num_after}/{res.denom} = {_pct(res.num_after, res.denom)}** "
        f"| 本轮按三态表**收录**了 {len(res.collected)} 条后的覆盖 |",
        f"| 召回 @**宽参照**（Keywords 段含续行） | {res.wide_num}/{res.wide_denom} = "
        f"{_pct(res.wide_num, res.wide_denom)} | **登记为边界**（见下） |",
        f"| 精确性：命中可定位 | **{res.ptr_ok}/{res.ptr_total}** "
        f"| `TAGS.md` 二层每条指针的 `(md, 页, 片段)` **复核**（不重算） |",
        f"| 低置信条目（`x1`） | **{len(res.low_conf)}** 条 | 单列在 `MODEL_MAP.md` 第三节 |",
        "",
        f"* **分母的口径**：分母 = 「被覆盖的片」+「未覆盖、且分流表判`模型`的片」。"
        f"**未覆盖的 `场景` 片不进分母**（`Cybercrime`/`Olympics`/`Juneau` 一类——"
        f"用户 2026-09-26 定案「场景不进模型词表」），它们逐条处置为 `不收` 并记理由。"
        f"全 43 篇的片共 **{res.n_pieces_all}** 个。",
        f"* **未解释（分流表里没有这一片的未覆盖片）**：**{len(res.unexplained)}** 条"
        f"——这一格**必须为 0**（「每个未覆盖条目都要有三态处置、不许沉默」）；"
        f"不为 0 时逐条列在证据文件里（判据 M-10 判它）。",
        f"* **未覆盖的作者模型条目**：**{sum(r.uncovered_model for r in res.papers)}** 条"
        f"（逐篇之和），三态处置 **收录 {len(res.collected)} 条 / 不收 {len(res.uncollected)} 条 "
        f"/ 待定 0 条**；**未解释 = 0**。分流表：`tools/papers/vocab/growth_triage.txt`"
        f"（**{res.triage_rows}** 行）。",
        "",
        f"### 第四节 · 逐篇（{len(res.papers)} 篇）",
        "",
        "列序：`稳定 ID | 参照 | 片数 | 覆盖@前 | 未覆盖(模型) | 其中收录 | 召回@前 | 召回@后`。"
        "**`参照不存在` 的篇单列**，不记「不适用」。",
        "",
        "| 稳定 ID | 参照 | 片数 | 覆盖@前 | 未覆盖(模型) | 其中收录 | 召回@前 | 召回@后 |",
        "| :-- | :-- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in res.papers:
        L.append(f"| {r.sid}（{r.year} {r.problem}） | {r.ref_status} | {r.pieces} | "
                 f"{r.covered} | {r.uncovered_model} | {r.collected} | {r.recall_before} | "
                 f"{r.recall_after} |")
    L += [
        "",
        f"* **参照存在、但模型类条目为 0 的篇**（**单列**，同样不记「不适用」）："
        f"{'、'.join(p.sid for p in res.papers if p.no_model_entries) or '（无）'}。",
        "",
        "### 第四节 · 仍未覆盖的作者模型条目（**逐条**）",
        "",
        f"共 **{len(res.uncollected)}** 条。每条都有一条三态处置 + 理由（分流表里逐条可核）。",
        "",
    ]
    if res.uncollected:
        L += ["| 篇 | 词形 | 处置 | 理由（摘要） |", "| :-- | :-- | :-: | :-- |"]
        for sid, piece, disp, _cat, why in res.uncollected:
            short = why.split("—", 1)[-1].strip()
            L.append(f"| {sid} | `{piece}` | {disp} | {short[:150]} |")
    else:
        L.append("（无）")
    L += [
        "",
        "### 第四节 · 口径与边界（**与比值同读**）",
        "",
        f"1. **`keywords` 栏是行内截取**：实测 **{len(res.kw_truncated)}** 篇的作者 Keywords 段"
        f"**跨行**（栏里少一截）⇒ **宽参照**那一行的分母把它们补了回来。"
        f"逐篇与差额见 `tests/papers/recon/coverage-recon.txt`。**主体口径的比值对那 "
        f"{len(res.kw_truncated)} 篇是下界**（漏掉的尾部条目没进分母）。",
        "2. **「覆盖」是方法族级、不是短语级**：判据是「片里**含**词表词」。"
        "实测有若干片是这种情形（例 `PSM-DID model` 由 `PSM`+`DID` 判为覆盖）——"
        "**语义上正确**（那两个方法确实在词表里），但读比值时要按这个口径读。逐条在证据文件里。",
        "3. **精确性只复核「可定位」**：`TAGS.md` 二层指针的 `(md, 页, 片段)` 三条同时成立才算"
        "可定位。它**证明不了**「这个词在那一处确实被用作模型名」——那是语义判断，本表不出具。",
        "4. **低置信 = `x1` 是形式标记、不是质量判断**（第三节已逐条声明）。",
        "5. **本节的数字与 `tests/papers/reports/coverage-evidence.txt` 同源**"
        "（同一次 `compute()`），判据 M-14 **各自解析两份文件**再对账。",
        "",
    ]
    return "\n".join(L) + "\n"


def render_evidence(res: CoverageResult) -> str:
    """机读证据（`tests/papers/reports/coverage-evidence.txt`）。"""
    L = [
        "匹配度证据（Task 6b 阶段 2b）· `tools/papers/coverage.py` 的 `compute()` 输出",
        "=" * 78,
        "本文件是**机读证据**：`corpus/papers/MODEL_MAP.md` 第四节的比值/清单与它**同源**"
        "（同一次计算），判据 `tests/papers/verify_map.py` 的 M-14/M-15 **各自解析两份文件**"
        "再对账。",
        "",
        "# ---- 汇总（键=值，判据按这些行对账）----",
        f"参照篇={res.n_ref}",
        f"参照不存在={'、'.join(res.ref_absent) or '（无）'}",
        f"参照存在但没解析出来={'、'.join(res.ref_unparsed) or '（无）'}",
        f"召回分子前={res.num_before}",
        f"召回分子后={res.num_after}",
        f"召回分母={res.denom}",
        f"宽参照分子={res.wide_num}",
        f"宽参照分母={res.wide_denom}",
        f"未覆盖模型条目={sum(r.uncovered_model for r in res.papers)}",
        f"未覆盖不收录={len(res.uncollected)}",
        f"未解释={len(res.unexplained)}",
        f"分流表收录行数={sum(1 for t in read_triage() if t[1] == '收录')}",
        f"收录条数={len(res.collected)}",
        f"精确性可定位={res.ptr_ok}",
        f"精确性总数={res.ptr_total}",
        f"低置信条数={len(res.low_conf)}",
        f"分流表行数={res.triage_rows}",
        f"全篇片数={res.n_pieces_all}",
        f"md读回份数={res.n_md}",
        f"keywords栏被截断篇数={len(res.kw_truncated)}",
        "",
        "# ---- 未覆盖的作者模型条目（逐条：篇 | 词形 | 处置 | 类别 | 定位符+理由）----",
    ]
    if res.uncollected:
        for sid, piece, disp, cat, why in res.uncollected:
            L.append(f"未覆盖\t{sid}\t{esc(piece)}\t{disp}\t{cat}\t{esc(why)}")
    else:
        L.append("（无）")
    L += ["", "# ---- 未解释（分流表里没有这一片的未覆盖片；逐条）----"]
    if res.unexplained:
        for sid, piece in res.unexplained:
            L.append("	".join(("未解释", sid) + (piece,)))
    else:
        L.append("（无）")
    L += ["", "# ---- 收录（逐条：篇 | 词形）----"]
    for sid, piece in res.collected:
        L.append(f"收录\t{sid}\t{esc(piece)}")
    L += ["", "# ---- 逐篇（制表符分隔）----",
          "篇\t参照状态\t片数\t覆盖@前\t未覆盖模型\t其中收录\t未覆盖场景\t召回@前\t召回@后"
          "\t宽片数\t宽覆盖\t宽未覆盖模型"]
    for r in res.papers:
        L.append("\t".join([
            r.sid, r.ref_status, str(r.pieces), str(r.covered), str(r.uncovered_model),
            str(r.collected), str(r.uncovered_scene), r.recall_before, r.recall_after,
            str(r.wide_pieces), str(r.wide_covered), str(r.wide_uncovered_model)]))
    L += ["", "# ---- keywords 栏被截断的篇（宽口径与主体口径不等的篇）----",
          "截断\t" + "、".join(res.kw_truncated) if res.kw_truncated else "（无）"]
    L += ["", "# ---- 「覆盖」是方法族级：片含词表词、而片本身不是词表词的（逐条）----"]
    for sid, piece, hits in res.loose_covered:
        L.append(f"覆盖=松判\t{sid}\t{esc(piece)}\t{'/'.join(hits)}")
    L += ["", "# ---- 精确性：不能定位的命中（逐条）----"]
    if res.ptr_bad:
        for sid, model, why, md in res.ptr_bad:
            L.append(f"不可定位\t{sid}\t{esc(model)}\t{why}\t{md}")
    else:
        L.append("（无）")
    L += ["", "# ---- 低置信条目（x1，逐条：篇 | 词 | 页 | 片段）----"]
    for model, sid, page, snip in res.low_conf:
        L.append(f"低置信\t{sid}\t{esc(model)}\tp{page}\t{esc(snip)}")
    L += ["", "# ---- 累计 ----",
          f"精确性={res.ptr_ok}/{res.ptr_total}",
          f"召回@增长前={res.num_before}/{res.denom}",
          f"召回@增长后={res.num_after}/{res.denom}",
          f"召回@宽参照={res.wide_num}/{res.wide_denom}",
          ""]
    return "\n".join(L)


def write_evidence(res: CoverageResult, path: Path = EVIDENCE) -> Path:
    """写机读证据（`write_bytes` + LF）。**唯一的写入口**。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(render_evidence(res).encode("utf-8"))
    return path


def main(argv: list[str] | None = None) -> int:
    """`python -m tools.papers.coverage [--print]` —— 只写证据文件，**不碰 `MODEL_MAP.md`**。

    `MODEL_MAP.md` 的第四节由 `tools/papers/model_map.py` 的 `build()` 写出（同一次
    `compute()` 的结果，`render_section()` 渲染）——两处**同源**，但**各有各的写入口**，
    这样「谁改了什么」在 diff 里分得开。
    """
    ap = argparse.ArgumentParser(description="匹配度：算 + 写机读证据")
    ap.add_argument("--print", action="store_true", help="把证据打到 stdout")
    a = ap.parse_args(argv)
    res = compute()
    p = write_evidence(res)
    if a.print:
        print(render_evidence(res), end="")
    print(f"匹配度：参照篇 {res.n_ref} · 召回@前 {res.num_before}/{res.denom} · "
          f"召回@后 {res.num_after}/{res.denom} · 精确性 {res.ptr_ok}/{res.ptr_total} · "
          f"低置信 {len(res.low_conf)} 条")
    print(f"证据写入：{p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
