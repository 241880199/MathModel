"""阶段 5：`INDEX.md`（人读）+ `TAGS.md`（机读三层）+ `PROVENANCE.md`。

## 三份产物各是什么

| 文件 | 给谁看 | 内容 |
| :--- | :--- | :--- |
| `INDEX.md` | 人读 | 一张表：稳定 ID / 年份 / 题号 / 队号 / 页数 / 图注 / 表注 / 公式 / 主题 / 模型算法 / 亮点 |
| `TAGS.md` | 机读 | **三层**：①逐篇一行（客观栏）②受控词表命中（**带指针**：词 + md 文件 + 页码 + 片段）③词表零命中篇 |
| `PROVENANCE.md` | 追溯 | `稳定 ID ↔ 文件名词干` 的**双射表**（两向一致） |

## 为什么 INDEX 里必须有「队号」，而 TAGS 里没有

稳定 ID 按**到达顺序**生成、**内容无关**（`io.stable_id` 的注释：条号重排不改已发 ID），
所以 **`ID → 原始 PDF` 这个映射推不出来**。INDEX 是「原文件定位列」的载体，故它保留队号；
`PROVENANCE.md` 再放一张双射表兜底。TAGS 是检索入口，队号与奖项都不在里面
（用户 2026-09-26 定案：「去掉队号与奖项；奖项在合集内统一，写进两个 .md 的文件头注记」）。

## `problem_type` 栏（Task 6b 阶段 2a 解冻，2026-09-26 用户裁决）

用户要求 `TAGS.md` 带上**原题的类型**。这一栏是 `TAGS_FIELDS` 的**最后一个**字段，取值
**从 `corpus/papers/PROBLEM_TYPES.md` 读回**（`annotations_problem_types()`，经
`taxonomy.load_annotations`）——**不在索引侧推断**。两个方向都 fail-closed：
本合集有论文而标注里没有这道题（或该题标注状态是「读不出」）→ **抛错**；
标注里有而本次产物无论文 → **不抛错**，但在 TAGS 头部**具名列出**（覆盖边界，见
该行的「标注覆盖边界（机读）」）。`INDEX.md` 的**表头继续不得**出现「原题类型」。

## 同一份事实**不在两处各算一次**（spec §6）

* `n_figures` / `n_tables` → **从 C1 的放行证据** `tests/papers/reports/c-report.txt`
  **读回**（该行 `C1 图注=N (图F/表T)` 的 `F`/`T`）；
* `n_equations` → **从 D1 的放行证据** `tests/papers/reports/d-report.txt` **读回**
  （该行 `检出=N`）；
* **不重算**。实测代价：自己重算得 **597/212**，C1 是 **682/253**，逐份 11 篇不等
  （`tests/papers/recon/ids-report.txt` 与 `ids-recon.txt` §4）。
  两者语义**不同**：C1 的「图注」是**图注条数**，不是产出 PNG 张数（产出是 662/246）。
* `n_pages` 是**原件的页数**（`fitz.open(...).page_count`）——原件是它唯一的权威，
  不存在"别处已经算过一次"的产物，故这里取原件。md 的 `<!-- page N -->` 锚点数
  是**另一条独立路径**，判据拿它交叉核对（实测 43/43 相等）。

## fail-closed（本项目已栽过六次的形态）

合集名不存在 / 合集下没有 PDF / **md 产物缺失** / **放行证据里没有这一篇**
一律**抛错**，**不得返回空表静默 PASS**（`io.sha256_tree` 的先例）。
这个坑在本仓是**活的**：磁盘上是 `2023年美赛O奖论文`（带「年」），别处写作
`2023美赛O奖论文`，而 `Path.rglob` 对不存在的目录**静默返回空**。

## 已知边界（判据里逐条断言，不假装它们不存在）

1. 两个 UMAP 合集名不以 4 位数字开头 ⇒ `io.stable_id` **抛 `ValueError`**（涉 37 份）；
2. 合集名少一个「年」字 ⇒ 与带「年」的合集**撞同一个 ID**（`P2023-A-01`）；
3. `io.problem_of` 要求路径里有**整段等于 `A`–`F` 的目录**：`2024年美赛O奖论文/`
   把题号写进了目录名（35/35 抛错）、2023 的春季赛子目录（5/42）、两个 UMAP（37/37）
   都不满足——**故本模块只对布局满足该约定的合集有意义**，别的合集**抛错**是
   **按设计**的行为（不是"这些合集也有索引"）。
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

from . import io, textmd, vocab

# 索引的默认合集（试点 = 2025，43 份，唯一有 md/图表/公式产物的一批）。
PILOT = "2025美赛O奖论文"

# 计划草稿的栏位探测词**逐字照抄**（要复现的就是它那套全文子串口径）。
HAS_PROBES: dict[str, tuple[str, ...]] = {
    "has_contents": ("Contents",),
    "has_assumptions": ("Assumptions", "Assumption"),
    "has_notations": ("Notations", "Notation"),
    "has_sensitivity": ("Sensitivity",),
    "has_extension": ("Extension", "Extend"),
}
# 标签序（TAGS 一层与判据都按它读）。
HAS_ORDER = ("has_contents", "has_assumptions", "has_notations",
             "has_sensitivity", "has_extension")

# 作者自写 Keywords 行。**带 `re.M`**（缺了它 `^` 只在全文开头匹配 → 实测 0/43；
# 计划草稿正是缺它）。行首允许 md 标记（`## ` 标题 / `**粗体**` / `> ` 引用）——
# 实测 43 份里有 14 份写成 `**Keywords: …**`、1 份写成 `## Keywords: …`；
# 只认裸行的正则在它们上面**看不见**，而那会让「无该行」的登记变成**假陈述**。
KEYWORDS = re.compile(r"^[#>*_ \t]*(?:Key\s*words?|关键词)\s*[:：]\s*(.*?)[*_ \t]*$",
                      re.I | re.M)
# 论文自报题号：栏位独占一行、或与题号同行；**大小写都认**（`2516695` 写的是小写 `c`）。
PROBLEM_FIELD = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]?\s*"
                           r"[*_ \t]*$", re.I | re.M)
PROBLEM_INLINE = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]"
                            r"[*_ \t]*([A-Fa-f])[*_ \t]*$", re.I | re.M)
LONE_LETTER = re.compile(r"^[*_#>\s]*([A-Fa-f])[*_#>\s]*$")
# 摘要页在题号**之后**还有这些栏位——遇到就停，免得把别处的单字母当题号。
FIELD_STOP = re.compile(r"\b(?:MCM|ICM|Summary\s+Sheet|Team\s+Control\s+Number|"
                        r"19\d\d|20\d\d)\b", re.I)
# 队号：`Team Control Number` 栏位、或 `Team # 2504188` 一类行内形（`2504188` 只有后者）。
TEAM_FIELD = re.compile(r"^[#>*_ \t]*(?:Team\s+Control\s+Number|队号)\s*[:：]?[*_ \t]*$",
                        re.I | re.M)
TEAM_INLINE = re.compile(r"Team\s*(?:Control\s*Number|#|Number)\s*[:：]?\s*[*_ \t]*"
                         r"(\d{6,8})", re.I)
# md 的页锚（Task 3 写的）。
PAGE_ANCHOR = re.compile(r"^<!-- page (\d+) -->$")
# C1 的逐份行：`2507789    C1 图注=1  (图1/表0) 产出=0  (图0/表0) 差额=1 …`
# **注意 `=1` 后面是两个空格**（实现用 `{n:<3}` 补齐）——正则必须容忍定宽填充，
# 否则 43 行里会静默少一行（实测：写死单空格时只解析出 42 行）。
C1_ROW = re.compile(r"^(\d{7})\s+C1 图注=(\d+)\s+\(图(\d+)/表(\d+)\)", re.M)
# D1 的逐份行：`2500836    检出=28  候选=…`
D1_ROW = re.compile(r"^(\d{7})\s+检出=(\d+)\s", re.M)
# 报告里的列表分隔符与字段分隔符；转义规则见 `_esc`。
FIELD_SEP = " | "
LIST_SEP = ";"
EMPTY = "-"


def _esc(s: str, semi: bool = True) -> str:
    r"""字段值转义。**必须可逆**：`\` → `\\`、`|` → `\|`、（`semi` 时）`;` → `\;`、
    `\x00` → `\0`、CR/LF → `\r`/`\n`。

    为什么非要有：实测 md 的标题行里**确有** `|`（`p(Θ|·)`）与 `;`，
    而 TAGS 一层用 ` | ` 分字段、`;` 分列表——不转义就会把一个标题切碎，
    读回来时**静默多出一列/多项**（本项目"证据看起来比实际强"家族的形态）。
    `\x00` 是实测存在的（12 份 md 含 NUL），整行片段会把它带进来。

    `semi=False` 给 `INDEX.md` 用：那张表是**给人读**的，`;` 不是它的分隔符，
    转义只会让「主题」栏满屏 `\;`（转义要按**该文件自己的分隔符集合**来定，
    多转义不是"更安全"，是把噪声写进产物）。
    """
    s = s.replace("\\", "\\\\").replace("|", "\\|")
    if semi:
        s = s.replace(";", "\\;")
    return (s.replace("\x00", "\\0").replace("\r", "\\r").replace("\n", "\\n"))


def _unesc(s: str) -> str:
    r"""`_esc` 的逆。**逐字符扫描**，不能用一串 `replace`（`\\|` 会被二次拆开）。"""
    out: list[str] = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            out.append({"\\": "\\", "|": "|", ";": ";", "0": "\x00",
                        "r": "\r", "n": "\n"}.get(n, "\\" + n))
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


@dataclass
class PaperRow:
    """TAGS 一层的**一行** + INDEX 的一行（字段见模块 docstring 的栏目契约）。

    `model_first` 的每项 = `(规范词, 页码, md 整行片段, 该词在本篇的出现次数)`。
    """
    stable_id: str
    collection: str
    year: str
    problem: str
    team: str
    stem: str
    pdf_rel: str
    md_rel: str
    n_pages: int
    n_figures: int
    n_tables: int
    n_equations: int
    sections: tuple[str, ...] = ()
    has: dict = field(default_factory=dict)
    keywords: str = ""
    model_first: tuple = ()
    declared_problem: str | None = None


@dataclass
class IndexResult:
    n_entries: int
    index_path: Path
    tags_path: Path
    prov_path: Path


# --------------------------------------------------------------------------
# 放行证据的读回（**唯一**取 n_figures / n_tables / n_equations 的地方）
# --------------------------------------------------------------------------
def read_release_c(path: Path | None = None) -> dict[str, tuple[int, int]]:
    """C1 的逐份图注计数 → `{stem: (图注数, 表注数)}`。**从放行证据读回，不重算。**

    fail-closed：证据文件不存在、或**一行都没解析出来**时**抛错**——返回空表会让
    每一篇都"查不到计数"，而查不到与"这篇真没有图表"是两件事（约束 4）。
    """
    from . import report
    p = path or report.release_path("c")
    if not p.is_file():
        raise FileNotFoundError(f"C1 的放行证据不存在：{p}（阶段 4 未跑就不能声称图表数）")
    text = p.read_bytes().decode("utf-8")
    out: dict[str, tuple[int, int]] = {}
    for m in C1_ROW.finditer(text):
        out[m.group(1)] = (int(m.group(3)), int(m.group(4)))
    if not out:
        raise ValueError(f"C1 的放行证据里一行逐篇计数都没有：{p}")
    return out


def read_release_d(path: Path | None = None) -> dict[str, int]:
    """D1 的逐份检出编号数 → `{stem: 检出数}`。**从放行证据读回，不重算。**"""
    from . import report
    p = path or report.release_path("d")
    if not p.is_file():
        raise FileNotFoundError(f"D1 的放行证据不存在：{p}（阶段 4 未跑就不能声称公式数）")
    text = p.read_bytes().decode("utf-8")
    out: dict[str, int] = {}
    for m in D1_ROW.finditer(text):
        out[m.group(1)] = int(m.group(2))
    if not out:
        raise ValueError(f"D1 的放行证据里一行逐篇计数都没有：{p}")
    return out


# --------------------------------------------------------------------------
# 逐篇取数
# --------------------------------------------------------------------------
def md_lines(text: str) -> list[str]:
    """md 全文 → 行表。**只用 `\\n` 切**（`str.splitlines()` 会在 `\\x0b`/`\\u2028` 等
    处也切，而 Task 3 写盘时只写 `\\n`——两套切法会让"偏移 ↔ 行号"错位）。
    """
    return text.split("\n")


def sample_page_of(lines: list[str]) -> list[int]:
    """逐行 → 页码（该行之前**最近**的那个 `<!-- page N -->` 锚）。无锚前的行记 0。"""
    out: list[int] = []
    cur = 0
    for ln in lines:
        m = PAGE_ANCHOR.match(ln.rstrip("\r"))
        if m:
            cur = int(m.group(1))
        out.append(cur)
    return out


def extract_keywords(text: str) -> str:
    """作者自写 Keywords 行的值（无该行 → 空串，**不编**）。见 `KEYWORDS` 的三条实测理由。"""
    m = KEYWORDS.search(text)
    return m.group(1).strip() if m else ""


def extract_problem(text: str) -> str | None:
    """论文**自己宣称**的题号（`Problem Chosen: X` 一类）；读不出→`None`（三态里的中态）。

    **不能一遇不匹配的行就放弃**：摘要页在题号之后还有 `**2025**` / `**MCM/ICM**` /
    `## Summary Sheet` 等栏位，故最多扫其后 6 个非空行，遇到 `FIELD_STOP` 才停。
    """
    mi = PROBLEM_INLINE.search(text)
    if mi:
        return mi.group(1).upper()
    m = PROBLEM_FIELD.search(text)
    if not m:
        return None
    for ln in [x for x in text[m.end():].split("\n") if x.strip()][:6]:
        ml = LONE_LETTER.fullmatch(ln)
        if ml:
            return ml.group(1).upper()
        if FIELD_STOP.search(ln):
            return None
    return None


def extract_team(text: str) -> str | None:
    """论文**自己宣称**的队号（栏位形或 `Team # N` 行内形）；读不出→`None`。"""
    mi = TEAM_INLINE.search(text)
    if mi:
        return mi.group(1)
    m = TEAM_FIELD.search(text)
    if not m:
        return None
    for ln in [x for x in text[m.end():].split("\n") if x.strip()][:5]:
        s = ln.strip().strip("*_# ").strip()
        if re.fullmatch(r"\d{6,8}", s):
            return s
        if FIELD_STOP.search(s):
            return None
    return None


def _flags_of(blob: str) -> dict[str, bool]:
    blob = blob.lower()
    return {k: any(x.lower() in blob for x in probes)
            for k, probes in HAS_PROBES.items()}


def has_flags(h2: list[str]) -> dict[str, bool]:
    """`has_*` —— 判据是「**md 的 `## ` 标题行里**字面出现该词」（不区分大小写）。

    **不是全文子串**：全文口径下 Contents 42/43、Assumptions 43/43、Notation 40/43、
    Sensitivity 38/43 —— 前四列近乎恒真，判据零区分力（`b-report.txt` 曾据此写下
    「30 份论文没有 Contents 页」而实测 42/43 都有，见 `docs/mcm-suite-lessons.md` §4.1）。
    """
    return _flags_of("\n".join(h2))


def has_flags_old(full_text: str) -> dict[str, bool]:
    """**已被证伪的旧口径**（全文子串）。

    **判据一个字节都不读它**——留着它是为了让「换过口径」这件事**当场可量**
    （`has_*` 两种口径的逐栏分布见 `tests/papers/recon/ids-recon.txt` §3），
    并让「把载体换回全文」这个改法在变异演示里可施加、可被抓住。
    """
    return _flags_of(full_text)


def fig_tab_counts(pdf: Path, ev_c: dict[str, tuple[int, int]]) -> tuple[int, int]:
    """`n_figures` / `n_tables` —— **从 C1 的放行证据读回**，**不重算**（spec §6）。

    实测依据：自己重算得 597/212，C1 是 682/253，逐份 11 篇不等。两者语义也不同
    （C1 的「图注」是**图注条数**，不是产出 PNG 张数 662/246）。

    fail-closed：证据里没有这一篇**抛错**——「证据没登记」与「这篇真没有图表」是两件事。
    """
    if pdf.stem not in ev_c:
        raise KeyError(f"C1 的放行证据里没有 {pdf.stem} 这一篇（不得当成「这篇没有图表」）")
    return ev_c[pdf.stem]


def pdf_facts(pdf: Path) -> dict:
    """开一次原件，取 `n_pages` 与 `sections`。

    `sections` **复用 `textmd` 的口径**（`body_size` + `HEADING_DELTA` + `is_title`），
    判序与 `textmd.to_markdown` 逐字相同（`CAPTION` 抢先 → 标题 → 其余）——
    **禁止第五份「字号 ≥ 常量」的实现**：`size >= 13.5` 是**全局绝对常量**，
    而正文号逐篇不同（42 份 12.0pt，`2522820` 10.9pt），实测丢 335 条
    （`2522820` 11 vs 35）。逐份对账见 `tests/papers/recon/ids-recon.txt` §2。
    """
    import fitz
    from . import watermark
    with fitz.open(pdf) as doc:
        watermark.strip_in_memory(doc)
        n_pages = doc.page_count
        body = textmd.body_size(doc)
        sections: list[str] = []
        for pno in range(n_pages):
            for block in doc[pno].get_text("dict")["blocks"]:
                if block.get("type") != 0:
                    continue
                for line in block.get("lines", []):
                    spans = line["spans"]
                    if not spans:
                        continue
                    text = "".join(s["text"] for s in spans).rstrip()
                    if not text.strip():
                        continue
                    if textmd.CAPTION.match(text):
                        continue
                    if textmd.is_heading(max(s["size"] for s in spans), body) \
                            and textmd.is_title(text):
                        sections.append(text.strip())
    return {"n_pages": n_pages, "sections": sections}


def _model_first(text: str, lines: list[str], pages: list[int],
                 terms: list[vocab.Term]) -> tuple:
    """每词**首次出现** → `(词, 页码, md 整行片段, 出现次数)`，按 (页码, 词) 排序。

    片段取**该次出现所在的 md 整行**（逐字，不截断、不裁剪）——这样判据能要求
    「片段是 md 的**一整行**」，而"指针错一位"就**必然**定位失败（不是"大概在附近"）。
    """
    hits = vocab.match(text, terms)
    first: dict[str, int] = {}
    n_occ: dict[str, int] = {}
    for h in hits:
        first.setdefault(h.word, h.start)
        n_occ[h.word] = n_occ.get(h.word, 0) + 1
    line_of = _line_index_of(lines)
    rows = []
    for w, s in first.items():
        li = line_of(s)
        rows.append((w, pages[li], lines[li], n_occ[w]))
    rows.sort(key=lambda r: (r[1], r[0]))
    return tuple(rows)


def _line_index_of(lines: list[str]):
    """字符偏移 → 行号（闭包）。**只用 `\\n` 计长**，与 `md_lines` 同一套口径。"""
    starts = []
    o = 0
    for ln in lines:
        starts.append(o)
        o += len(ln) + 1

    def f(off: int) -> int:
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo
    return f


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def build(collection: str = PILOT, sample: list[Path] | None = None,
          out_dir: Path | None = None) -> IndexResult:
    """生成三份产物。

    `sample=None` → **全量**（该合集下的全部 PDF）；否则只处理给定样本
    （**变异演示必须能限样本**，否则每条演示都要跑 43 份）。
    `out_dir=None` → `io.DERIVED`（入库产物目录）；限样本跑**必须**另给一个目录，
    否则 `--limit` 会把入库的 INDEX/TAGS/PROVENANCE 覆写成 10 份的版本
    （`tools/papers/report.py` 的落点机制管的是**报告**，产物这边由调用方负责）。

    **`sample` 与 `out_dir=None` 同时出现 = 当场抛**：默认落点是**入库产物**
    `io.DERIVED`，于是 `build(PILOT, sample=[…])` 会**静默覆写**入库的三份产物
    （`git status` 上只显示一处「修改」，形态与 Task 3 的「限样本覆写放行证据」同族）。
    这个敞口原先只有 docstring 提醒、**没有机制强制**——现在按 fail-closed 处理。
    """
    # 先于一切取数：这条守卫必须在**任何写盘动作之前**触发（否则守卫自己变成破坏者）。
    if sample is not None and out_dir is None:
        raise ValueError(
            f"限样本跑（sample 给了 {len(sample)} 份）必须显式指定 out_dir："
            f"out_dir=None 的默认落点是**入库产物**目录 {io.DERIVED}"
            f"（会覆写 INDEX.md/TAGS.md/PROVENANCE.md）。"
            f"limit 跑请给一个不入库的目录。")

    root = io.ORIGIN / collection
    # fail-closed：合集名不存在就抛。`Path.rglob` 对不存在的目录**静默返回空**，
    # 于是零依据的「全通过」凭空成立——这个坑在本仓是活的（`2023美赛O奖论文`）。
    if not root.is_dir():
        raise FileNotFoundError(
            f"合集目录不存在：{root}（拒绝用空表冒充「该合集没有论文」）")
    all_pdfs = sorted(root.rglob("*.pdf"))
    if not all_pdfs:
        raise ValueError(f"合集下没有任何 PDF，拒绝产出空索引：{root}")

    pdfs = all_pdfs if sample is None else sorted(sample)
    outside = [p for p in pdfs if p not in set(all_pdfs)]
    if outside:
        raise ValueError(f"样本里有不属于该合集的 PDF（拒绝静默跳过）：{outside[:3]}")

    terms = vocab.load()
    c1 = read_release_c()
    d1 = read_release_d()

    dest = out_dir or io.DERIVED
    dest.mkdir(parents=True, exist_ok=True)

    rows: list[PaperRow] = []
    per_problem: dict[str, int] = {}
    for src in pdfs:
        rel = src.relative_to(io.ORIGIN)
        problem = io.problem_of(str(rel))
        per_problem[problem] = per_problem.get(problem, 0) + 1
        sid = io.stable_id(collection, problem, per_problem[problem])
        md = io.md_path(collection, problem, src.stem)
        if not md.is_file():
            raise FileNotFoundError(
                f"md 产物缺失：{md}（阶段 4/3 没跑过就不能声称「这篇没有 md」）")
        text = md.read_bytes().decode("utf-8")
        lines = md_lines(text)
        pages = sample_page_of(lines)
        facts = pdf_facts(src)
        h2 = [ln[3:].strip() for ln in lines if ln.startswith("## ")]
        if src.stem not in c1 or src.stem not in d1:
            raise KeyError(
                f"放行证据里没有 {src.stem} 这一篇（c={src.stem in c1} d={src.stem in d1}）"
                f"——「证据没登记」与「这篇真的没有」是两件事，不得混同")
        nf, nt = fig_tab_counts(src, c1)
        rows.append(PaperRow(
            stable_id=sid, collection=collection, year=sid[1:5], problem=problem,
            team=src.stem, stem=src.stem,
            pdf_rel=rel.as_posix(), md_rel=md.relative_to(io.REPO).as_posix(),
            n_pages=facts["n_pages"], n_figures=nf,
            n_tables=nt, n_equations=d1[src.stem],
            sections=tuple(facts["sections"]), has=has_flags(h2),
            keywords=extract_keywords(text),
            model_first=_model_first(text, lines, pages, terms),
            declared_problem=extract_problem(text),
        ))

    rows.sort(key=lambda r: r.stable_id)
    # **零区分力栏**由**本次数据**算出（不是写死的字符串）：一边占比 > 90% 的 `has_*` 栏
    # 在本语料上没有区分力，必须在 TAGS 头部**具名登记**——否则下一个人会拿它当证据。
    # 由此，判据（`verify_ids.py` 的 I4-c）能要求「登记行具名的栏集合 == 判据自己算出的
    # 零区分力集合」——**这是双边等式**；写死一句话的那种写法会让判据永远为真。
    dist = {k: sum(1 for r in rows if r.has.get(k)) for k in HAS_ORDER}
    zero_disc = [k for k in HAS_ORDER if len(rows) and dist[k] > 0.9 * len(rows)]
    idx = dest / "INDEX.md"
    tags = dest / "TAGS.md"
    prov = dest / "PROVENANCE.md"
    _write_index(idx, collection, rows)
    _write_tags(tags, collection, rows, terms, dist, zero_disc)
    _write_prov(prov, collection, rows, pdfs)
    return IndexResult(n_entries=len(rows), index_path=idx, tags_path=tags,
                       prov_path=prov)


def _award_note(collection: str) -> str:
    return (f"**奖项注记**：本合集 `{collection}` 内**全部为 O 奖（Outstanding Winner）论文**"
            f"——奖项在合集内统一，故**不设「奖项」栏**（用户 2026-09-26 定案）。")


def _write_index(path: Path, collection: str, rows: list[PaperRow]) -> None:
    L = [
        f"# 2025 美赛 O 奖论文索引（阶段 5 · Task 6）",
        "",
        f"> 合集：`corpus/历届优秀论文/{collection}/`　·　篇数：**{len(rows)}**",
        f"> {_award_note(collection)}",
        "",
        "## 栏目契约（用户 2026-09-26 定案，未自改）",
        "",
        "`稳定 ID | 年份 | 题号 | 队号 | 页数 | 图注 | 表注 | 公式 | 主题 | 模型/算法 | 亮点`",
        "",
        "**标级**：`[客观]` = 可由**原件或产物**直接确定（不含判断）；"
        "`[社区]` = **含判断**，须附页/行指针、可复核。",
        "",
        "* `图注` / `表注` = **C1 的图注计数**（`tests/papers/reports/c-report.txt` 读回）；"
        "`公式` = **D1 的检出编号数**（`d-report.txt` 读回）。"
        "**均不重算**（spec §6「同一份事实不在两处各算一次」）。"
        "注意语义：这是**图注/编号条数**，**不是产出 PNG 张数**。",
        "* `主题` = **作者自写 Keywords 行**的原文。**该篇没有这一行时**留空（不填推测）；"
        f"逐份登记与计数见 `tests/papers/reports/ids-report.txt`。",
        "* `模型/算法` = 受控词表（`tools/papers/vocab/models.txt`）的**字面命中**规范词；"
        "**指针（词 + md 文件 + 页码 + 片段）在 `TAGS.md` 第二层**。",
        "* `亮点` = **`[社区]` 判断栏**：须附**页/行指针、可复核**；"
        "**给不出就留空，不填推测性内容**（spec §5）。",
        "* **`原题类型` 栏由 Task 6b 写入**（题型分类法要从题面正文自建）；"
        "**Task 6 不留空占位列**。",
        "",
        "> **本轮「亮点」为什么一律留空**：本任务没有逐篇精读到能给出**可指回原文**的判断。"
        "留空 ≠ 这些论文没有亮点，只表示**本索引没有为它提供可复核的依据**——"
        "填推测性内容会把判断混进客观栏。",
        "",
        "| 稳定 ID `[客观]` | 年份 `[客观]` | 题号 `[客观]` | 队号 `[客观]` | 页数 `[客观]` "
        "| 图注 `[客观]` | 表注 `[客观]` | 公式 `[客观]` | 主题 `[客观]` | 模型/算法 `[客观]` "
        "| 亮点 `[社区]` |",
        "| :--- | ---: | :-: | :--- | ---: | ---: | ---: | ---: | :--- | :--- | :--- |",
    ]
    for r in rows:
        # **先转义每一项，再用未转义的分隔符拼**（顺序反了会把分隔符也转义掉，
        # 读回来时整格变成一项——实测踩过：`sections` 被读成 1 条）。
        models = LIST_SEP.join(_esc(w, False) for w, _p, _s, _n in r.model_first)
        cells = [
            _esc(r.stable_id, False), _esc(r.year, False), _esc(r.problem, False),
            _esc(r.team, False), str(r.n_pages), str(r.n_figures), str(r.n_tables),
            str(r.n_equations), _esc(r.keywords, False), models or EMPTY, "",
        ]
        L.append("| " + " | ".join(cells) + " |")
    L.append("")
    path.write_bytes(("\n".join(L) + "\n").encode("utf-8"))


TAGS_FIELDS = ("stable_id", "year", "problem", "n_pages", "n_figures", "n_tables",
               "n_equations", "models", "sections") + HAS_ORDER + ("keywords",) \
    + ("problem_type",)
# **`problem_type` 加在末尾**（Task 6b 阶段 2a 解冻）：`verify_ids.py` 与 `verify_types.py`
# 都按**字段序**读这一行，加在末尾才能让已有字段的**位置一个都不变**（有下游按位置解析的
# 风险，加末尾是最小破坏面）。`INDEX.md` 的**表头继续不得**出现「原题类型」——用户只要求
# `TAGS.md` 带这一栏（I10 的 INDEX 那一半**保持不变**）。


def annotations_problem_types() -> dict[tuple[str, str], list[str]]:
    """`(年, 题号) → [标签名, …]`（`L1 · L2` 全名，**按标注文件里的顺序**）。**只读回，不重算。**

    这是 `problem_type` 栏取值的**唯一**来源：题型是**标注文件**（人工逐题读题面后做的分类）
    的属性，不在索引侧重推一遍——重推就是「同一份事实两处各算一次」，两处会静默分叉
    （spec §6）。判据侧另有一份**独立**解析（`verify_ids.py` 的 I10-e 自己解析该 .md、
    **不调本函数**）：两边不共用代码，I10-e 才不会退化成「函数跟自己对答案」。
    """
    from . import taxonomy
    out: dict[tuple[str, str], list[str]] = {}
    for a in taxonomy.load_annotations(taxonomy.ANNOTATIONS_PATH):
        out[(str(a.year), a.problem)] = [f"{l1} · {l2}" for l1, l2, _m in a.labels]
    return out


def annotations_path_note() -> str:
    """标注文件的**仓库相对路径**（错误消息里只写相对形式——产物与报告不许带绝对路径）。"""
    from . import taxonomy
    return taxonomy.ANNOTATIONS_PATH.relative_to(io.REPO).as_posix()


def _write_tags(path: Path, collection: str, rows: list[PaperRow],
                terms: list[vocab.Term], dist: dict, zero_disc: list) -> None:
    n = len(rows)
    # ---- `problem_type` 栏：**从标注文件读回**（Task 6b 阶段 2a 解冻的那一栏）----------
    types = annotations_problem_types()
    # fail-closed 的两个方向：**本合集有这篇论文、标注里却没有它这道题** →
    # 抛错（**不许写空串**——「留空占位列」正是 Task 6 的 I10 绊线专抓的假绿形态）；
    # 「标注里有这道题、但状态是『读不出』（无标签）」同样落这里：索引侧**没有**一个
    # 非占位的可信取值可写。**消息里指名是哪一篇**。
    no_type = [(r.stable_id, r.year, r.problem) for r in rows
               if not types.get((r.year, r.problem))]
    if no_type:
        named = "、".join(f"{sid}（{yr} 题 {pr}）" for sid, yr, pr in
                          sorted(set(no_type)))
        raise KeyError(
            f"`problem_type` 读不回标注：{named}——「标注里没有这道题」与「这道题的标注"
            f"状态是『读不出』（无标签）」都会落到这里，两种情形都**拒绝写空串/占位串**"
            f"（空占位列会被判成绿）。标注文件的落点："
            f"{annotations_path_note()}")
    # **反向**：标注里有、而**本次产物没有论文**的 `(年, 题号)` → **不抛错**，但在产物里
    # **具名列出**（`corpus/官方原题/` 有 2016–2026 共 67 题，本合集只有 2025 六题，
    # 其余 61 题天然落这里——这是覆盖边界，不是错误）。
    have = {(r.year, r.problem) for r in rows}
    uncovered = sorted(k for k in types if k not in have)
    decl = (" · ".join(f"{k}={dist[k]}/{n}" for k in zero_disc)
            if zero_disc else "（无）")
    L = [
        "# TAGS — 机读索引（三层）· 2025 美赛 O 奖论文",
        "",
        f"> 合集：`corpus/历届优秀论文/{collection}/`　·　篇数：**{n}**",
        f"> {_award_note(collection)}",
        "> 稳定 ID **内容无关**（按到达顺序生成）⇒ `ID → 原件` 推不出来，"
        "双射表在 `PROVENANCE.md`。",
        "",
        "## 局限（必读）",
        "",
        "* 词表匹配抓不到「**用了但没写名字**」的模型，也抓不到词表外的模型。"
        "**本文件是检索入口，不是完备清单**——先据此定位候选，再读 md 全文。",
        "* `has_*` 各栏的语义是「**md 的 `## ` 标题行里字面出现了该词**」这个事实，"
        "**不等于**「论文确实做了敏感性分析」。",
        # **具名声明**：由本次数据算出、一行写完、可机读（`k=命中数/篇数`）——
        # 免得下一个人把「算得出来」当成「有区分力」。
        f"* **零区分力登记**（一边占比 > 90%）：{decl}"
        f" —— 这几栏在本语料上**区分力低**，**不因为它们算得出来就当判据用**。"
        f"逐栏分布见 `tests/papers/reports/ids-report.txt`。",
        "* `sections` 是 **md `## ` 标题行逐字**（`;` 连接、去 `## ` 前缀）。"
        "本语料把「号」与「题」**常分两行排**（`## 1.1` 一行、`## Problem Background` 下一行），"
        "本文件**不做「号/题合并」一类推断**——那会把推断写进事实栏。",
        f"* `{TAGS_FIELDS[-1]}` = **该篇题目的题型**（`L1 · L2` 全名，`{LIST_SEP}` 连接）——"
        f"**读回**自 `{annotations_path_note()}`（人工逐题读题面后做的标注），"
        f"**不在索引侧重算**（「同一份事实不在两处各算一次」）。"
        f"`核心` 与 `附带` 两种标记的标签**都收**（标记只活在标注文件里，本栏只放题型名）；"
        f"它是**题的属性、不是篇的属性**（同一题号的所有行取值逐字相同）。",
        # **反向覆盖边界**（机读）：标注里有、而本次产物无论文的题**具名列出**——
        # 「没有这一栏」与「这一栏是空的」不是一回事，覆盖边界必须写出来而不是省略。
        f"* **标注覆盖边界（机读）**：标注题数={len(types)} · 有论文的题={len(have)} · "
        f"未配对的题={len(uncovered)} · 覆盖年份="
        f"{'/'.join(sorted({y for y, _p in have})) if have else '（无）'} · "
        f"未配对逐题={'、'.join(f'{y} {p}' for y, p in uncovered) if uncovered else '（无）'}"
        f" —— 本合集只有 2025 的论文，`corpus/官方原题/` 的其余年份**尚无论文产物**"
        f"（Task 9 才扩），故这些题**有题型、无配对**。",
        "",
        "## 第一层 · 逐篇一行（客观栏）",
        "",
        f"**每篇一行**，字段以 `{FIELD_SEP}` 分隔、列表以 `{LIST_SEP}` 分隔、空值写 `{EMPTY}`。"
        "值内的 `|`、`;`、NUL、CR、LF 与反斜杠**一律转义**（前四者写成"
        "「反斜杠 + 原字符 / 反斜杠 + 数字」的形式，反斜杠自身写成两个反斜杠）——"
        "实测 md 的标题行里确有 `|`（`p(Θ|·)`）与 `;`，不转义会把一条记录静默切成多列。",
        "",
        "字段序：",
        "",
        "```",
        FIELD_SEP.join(TAGS_FIELDS),
        "```",
        "",
        "记录（同一行序，**入库文件里就是这一段**）：",
        "",
        "```",
    ]
    for r in rows:
        # **先转义每一项、再用未转义的分隔符拼**（顺序反了会把分隔符也转义掉，
        # 读回来时整格变成一项——实测踩过：`sections`/`models` 被读成 1 项）。
        models = LIST_SEP.join(_esc(w) for w, _p, _s, _n in r.model_first)
        sections = LIST_SEP.join(_esc(s) for s in r.sections)
        ptype = LIST_SEP.join(_esc(x) for x in types[(r.year, r.problem)])
        vals = [
            _esc(r.stable_id), _esc(r.year), _esc(r.problem), str(r.n_pages),
            str(r.n_figures), str(r.n_tables), str(r.n_equations),
            models or EMPTY, sections or EMPTY,
            *["1" if r.has.get(k) else "0" for k in HAS_ORDER],
            _esc(r.keywords) or EMPTY,
            ptype or EMPTY,
        ]
        L.append(FIELD_SEP.join(vals))
    L += [
        "```",
        "",
    ]

    with_hits = [r for r in rows if r.model_first]
    zero = [r for r in rows if not r.model_first]
    L += [
        "## 第二层 · 受控词表命中（**指针：词 + md 文件 + 页码 + 片段**）",
        "",
        f"本层收**有命中**的 **{len(with_hits)}** 篇；第三层收零命中的 **{len(zero)}** 篇；"
        f"两层之和 = **{len(with_hits) + len(zero)}** = 篇数（**每篇恰好进一层**）。",
        "",
        "指针格式（每行一条，**刻意不用反引号包裹**——md 整行里可能有反引号）：",
        "",
        "```",
        f"- {LIST_SEP.join(['<规范词>', 'p<页码>', 'x<出现次数>', '<md 整行逐字>'])}",
        "```",
        "",
        "解析式：`^- (.*); p(\\d+); x(\\d+); (.*)$`（`;` 是转义过的分隔符，"
        "片段按 `_esc` 的规则转义）。"
        "页码由该行之前最近的 `<!-- page N -->` 锚数出；**片段是 md 的整行逐字**"
        "（可用 `grep -F` 直接在该 md 里定位）；`x<N>` 是**全篇**出现次数，**不是**这一行的。"
        "**md 文件**列在每篇小标题下的 `md: ` 一行。",
        "",
    ]
    for r in with_hits:
        L.append(f"### {r.stable_id} · 题 {r.problem} · {r.pdf_rel}")
        L.append(f"md: {r.md_rel}")
        for w, pg, snippet, n in r.model_first:
            L.append(f"- {w}{LIST_SEP} p{pg}{LIST_SEP} x{n}{LIST_SEP} {_esc(snippet)}")
        L.append("")
    L += [
        f"## 第三层 · 词表缺口自曝（受控词表**零命中**的篇）",
        "",
        f"本层 **{len(zero)}** 篇（= {len(rows)} − 第二层 {len(with_hits)}）。"
        "如为零也**照印**：这一层必须存在，空与「没写」不是一回事。"
        "这些篇要么真没用词表里的模型，要么用了词表外的模型——**这是已知漏检，登记而非掩盖**。",
        "",
    ]
    for r in zero:
        L.append(f"- {r.stable_id} · 题 {r.problem} · `{r.md_rel}`")
    L += [
        "",
        "### 词表本身",
        "",
        f"`tools/papers/vocab/models.txt`：**{len(terms)}** 个词条、"
        f"**{sum(len(t.variants) for t in terms)}** 个变体；**一行一詞条、可追加**"
        f"（用户 2026-09-26：「新遇到的模型/算法可以加入语料库」）。"
        f"零命中词条与「论文里出现但词表没有」的增长候选清单在 "
        f"`tests/papers/reports/ids-report.txt`。",
        "",
    ]
    path.write_bytes(("\n".join(L) + "\n").encode("utf-8"))


def _write_prov(path: Path, collection: str, rows: list[PaperRow],
                pdfs: list[Path]) -> None:
    L = [
        "# PROVENANCE — 稳定 ID ↔ 原件（双射表）",
        "",
        f"> 合集：`corpus/历届优秀论文/{collection}/`　·　篇数：**{len(rows)}**",
        f"> {_award_note(collection)}",
        "",
        "## 为什么要这张表",
        "",
        "稳定 ID（`io.stable_id`）按**到达顺序**生成、**内容无关**——条号重排不会改变已发 ID"
        "（教训三.1 要的正是这一点）。代价是 **`ID → 原始 PDF` 的映射推不出来**，"
        "必须另有出处。`INDEX.md` 保留「队号」栏作定位列，本表给出**更强的一层**："
        "**逐篇双射**。",
        "",
        "**双射的判据（两向一致）**：",
        "",
        "* 正向 `ID → 文件名词干`：本表每行的 ID **唯一**（不会两行同 ID）；",
        "* 反向 `文件名词干 → ID`：每个词干**只出现一次**（不会两行同词干）；",
        "* 两向互逆，且并集**恰好覆盖**该合集磁盘上的全部 PDF（不重不漏）。",
        "",
        "## 双射表",
        "",
        "| 稳定 ID | 年月 | 题号 | 文件名词干（= 队号） | 原件（仓库相对） | md（仓库相对） |",
        "| :--- | ---: | :-: | :--- | :--- | :--- |",
    ]
    for r in rows:
        L.append(f"| {_esc(r.stable_id)} | {_esc(r.year)} | {_esc(r.problem)} "
                 f"| {_esc(r.stem)} | `{_esc(r.pdf_rel)}` | `{_esc(r.md_rel)}` |")
    L += [
        "",
        f"表内 {len(rows)} 行；磁盘上该合集的 PDF {len(pdfs)} 份"
        "（限样本跑时本表只覆盖样本，**覆盖数是判据当场算的**）。",
        "",
        "## 原件路径口径",
        "",
        f"`corpus/历届优秀论文/{collection}/<题号目录>/<队号>.pdf`；"
        "2023 与 2024 合集的目录层不同（2023 多一层中文长名、2024 把题号写进目录名），"
        "故**题号一律用 `io.problem_of` 从路径取**，不用 `p.parent.name`。"
        "逐合集的 `problem_of` 行为实测见 `tests/papers/recon/ids-recon.txt` §5。",
        "",
    ]
    path.write_bytes(("\n".join(L) + "\n").encode("utf-8"))
