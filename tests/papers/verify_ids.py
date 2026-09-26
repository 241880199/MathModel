"""索引与稳定 ID 的判据（Task 6 阶段 5）：I1–I13。

被测产物：`corpus/papers/INDEX.md` / `TAGS.md` / `PROVENANCE.md`（由
`tools/papers/index.py` 生成）。被测实现：`tools/papers/index.py`、`tools/papers/vocab.py`。

## 判据总表（**每一栏的参照是什么、为什么独立**）

| # | 判据 | 参照（独立的东西） |
| :--- | :--- | :--- |
| **I1** | 稳定 ID 双射：`ID ↔ 磁盘 PDF ↔ md 文件`，两向一致 + 唯一 + 覆盖 | **磁盘**（`rglob`）与 **`io.problem_of` 数出来的到达顺序** |
| **I2** | 条目数**双边等式**：n_entries == 唯一 ID 数 == 样本 PDF 数 == 样本 md 数 == INDEX 表行数 == TAGS 一层行数；二层篇数 + 三层篇数 == n_entries | 磁盘 + 产物 |
| **I3** | `sections` 与 **md 的 `## ` 行**逐字逐条对账 | **md**（Task 3 的产物，**不由本任务生成**） |
| **I4** | `has_*` 与本脚本自己按「标题行」口径重算的值逐篇相等 + 分布与 recon 登记一致 + 零区分力栏在 TAGS 头部**有声明** | 本脚本的独立实现 + `recon/ids-recon.txt` |
| **I5** | `keywords` 与 md 重算值逐篇相等；**无该行的篇留空**且篇数 == 独立重算的「无该行」数 | md |
| **I6** | `n_figures`/`n_tables`/`n_equations` **从 `c-report.txt`/`d-report.txt` 读回**并逐篇相等 | **C1/D1 的放行证据**（另一条流水线的产物） |
| **I6-b** | 产物 `n_pages` == **原件** `page_count`（逐篇**双边**）+ 逐篇 md 页锚条数 == 原件 `page_count` | **原件**（`fitz` 开一次）+ **md**（Task 3 产物） |
| **I7** | `models` 每条指针：词 + md 文件 + 页码 + 片段；**片段是 md 的整行逐字**；页码 == 该行自己的页；`xN` == 独立重算的出现次数；一层词集 == 二层词集 | md（本脚本独立重算） |
| **I8** | 「题目 ↔ 论文」：产物 `problem` vs **论文自报题号**；**不符 → FAIL**；**有栏但读不出 → FAIL**（约束 4）；「没有该栏」按三态计数 + **上界** | md 摘要页（论文自己的话） |
| **I9** | `PROVENANCE.md` 的 `ID ↔ 词干` 双射两向一致 | 磁盘 |
| **I10** | 栏位契约：INDEX 表头 11 栏齐 + TAGS 原有 10 栏齐；**INDEX 表头继续不得出现 `原题类型`**；`problem_type` 在 TAGS 字段序的**末尾** | 用户 2026-09-26 定案 + 任务书 §一 |
| **I10-a…g** | **解冻后的 `problem_type` 栏**（2026-09-26 用户裁决「解冻并强化 I10」）：a 栏在；b 逐行非空且非占位串；c 同题号字母取值逐字相同；d 字母数 == 互异取值数（全量另断言 == 6）；**e 取值解析出的 `(L1,L2)` 集合 == 标注文件该题那一节的标签集合**（本脚本**自己解析**该 .md）；f 每个标签名 ∈ 分类法 且 ∉ 词表；g 覆盖边界可机读且为等式 | **标注文件**（另一份解析）+ 分类法/词表（独立读）+ 产物字节 |
| **I10-h / I10-i** | `亮点` 全空且头部有 `[社区]` 说明 / 奖项注记在两个 .md 的文件头（**内容与原 `I10-b`/`I10-c` 一字未改，只顺延编号**） | 用户 2026-09-26 定案 |
| **I11** | **fail-closed**：合集名不存在时 `index.build` **必须抛错**（不得返回空表静默 PASS） | 无（行为断言） |
| **I12** | 已知边界**具名断言**：UMAP 名 → `stable_id` 抛 `ValueError`；少一个「年」字 → **撞同一个 ID** | `io` 的实测行为 |
| **I13** | 词表：结构可追加、规范词唯一、零命中词**逐词登记**、增长候选（**来源限于作者 Keywords 行，未扫正文**——具名范围边界）**逐条给出** | 词表文件 + md |
| **I13-b** | 「`vocab.load` **不缓存**」**真验**：临时词表写 1 条 → `load` → 追加 1 条 → **同一进程内**再 `load`，必须读到 2 条 | 词表文件（临时副本） |

## 三个「判据自己会不会假绿」的防线（照 `verify_d.py` 的现行范式）

1. **不读「自称」、只读「产物」**：`n_*` 一律从**放行证据文件**读回、`sections`/`has_*`/
   `keywords`/`models` 一律从 **md** 重算、`problem` 一律从**论文自己的摘要页**读。
   **唯一一处读实现自报值的是 I2 的第一项 `res.n_entries`**——它被另外**六个独立量**
   （唯一 ID 数 / TAGS 一层行数 / INDEX 表行数 / PROVENANCE 行数 / 磁盘 PDF 数 / md 文件数）
   **夹住**，自报值必须与那六个**同时相等**才可能成立，**不可能单独造成假绿**
   （本项目第八例是拿自报值**当结论**：第一版拿实现自报的 `n_refs` 判，变异下全绿）。
2. **双边等式**：判据是 `A == B` 而不是 `A >= 1`（约束 5）；差额逐条具名登记，
   **未解释必须为 0**。
3. **已知边界要断言**（I11/I12）：不得假装 UMAP 抛错与跨合集撞号不存在。

## 限样本跑（`--limit N`）

样本 = 前 N 份 ∪ 见证集 `FOCUS`（见下）。**限样本跑另立落点**：
报告写 `tests/papers/reports-limited/ids-report-limited-N.txt`（不入库），
**产物写到 `tests/papers/reports-limited/ids-products/`**——否则 `--limit` 会把入库的
`corpus/papers/{INDEX,TAGS,PROVENANCE}.md` 覆写成 10 份的版本（`report.py` 的落点机制
管的是**报告**，产物这一侧由本脚本自己守：跑前跑后对三份产物量 sha256，变了就判 FAIL）。
"""
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

COLLECTION = "2025美赛O奖论文"

# `--limit` 的见证集。**不并入取样是不行的**：排序序里靠后的关键样本取不到，
# 变异演示会在看不见它的集合上"绿着通过"。
#
#   2522820  排序第 29 位。**M3 的头号见证**：正文 10.9pt、小节标题 12.0pt ——
#            计划草稿的 `size >= 13.5` 全局常量把它的小节**整层丢掉**（实测 11 vs 35 条）。
#            它同时是**唯一没有作者自写 Keywords 行**的一篇（`I5` 空值分支的实例）。
#   2501687  排序第 6 位。**M8 的见证**：它是 A 题之外的第一篇（题 B），
#            而前 3 份全是 A 题——不并入它就**换不出**两篇不同题号的论文，
#            「论文被错放」这条链路在 `--limit 3` 下演示不出来。
FOCUS = ("2522820", "2501687")

# ---- 参照侧的独立实现（**不 import 被测模块的对应函数**）--------------------
# 参照必须与被测实现分开：实现那份改宽/收紧了，这里不跟着变、会红
# （通则候选①「同一语义必须用同一谓词」的另一半：参照侧要留一份独立的）。
V_H2 = "## "
V_PAGE_ANCHOR = re.compile(r"^<!-- page (\d+) -->$")
V_KEYWORDS = re.compile(r"^[#>*_ \t]*(?:Key\s*words?|关键词)\s*[:：]\s*(.*?)[*_ \t]*$",
                        re.I | re.M)
V_KEYWORDS_DRAFT = re.compile(r"^\s*(Key\s*words?|关键词)\s*[:：]\s*(.+)$", re.I)
V_KEYWORDS_DRAFT_M = re.compile(r"^\s*(Key\s*words?|关键词)\s*[:：]\s*(.+)$", re.I | re.M)
V_HAS_PROBES = {
    "has_contents": ("Contents",),
    "has_assumptions": ("Assumptions", "Assumption"),
    "has_notations": ("Notations", "Notation"),
    "has_sensitivity": ("Sensitivity",),
    "has_extension": ("Extension", "Extend"),
}
V_HAS_ORDER = ("has_contents", "has_assumptions", "has_notations",
               "has_sensitivity", "has_extension")
V_PROBLEM_FIELD = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]?\s*"
                             r"[*_ \t]*$", re.I | re.M)
V_PROBLEM_INLINE = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]"
                              r"[*_ \t]*([A-Fa-f])[*_ \t]*$", re.I | re.M)
V_LONE_LETTER = re.compile(r"^[*_#>\s]*([A-Fa-f])[*_#>\s]*$")
V_FIELD_STOP = re.compile(r"\b(?:MCM|ICM|Summary\s+Sheet|Team\s+Control\s+Number|"
                          r"19\d\d|20\d\d)\b", re.I)
V_TEAM_INLINE = re.compile(r"Team\s*(?:Control\s*Number|#|Number)\s*[:：]?\s*[*_ \t]*"
                           r"(\d{6,8})", re.I)
V_TEAM_FIELD = re.compile(r"^[#>*_ \t]*(?:Team\s+Control\s+Number|队号)\s*[:：]?[*_ \t]*$",
                          re.I | re.M)
V_C1_ROW = re.compile(r"^(\d{7})\s+C1 图注=(\d+)\s+\(图(\d+)/表(\d+)\)", re.M)
V_D1_ROW = re.compile(r"^(\d{7})\s+检出=(\d+)\s", re.M)
V_L2 = re.compile(r"^### (P\d{4}-[A-F]-\d{2,}) · 题 ([A-F]) · (.+)$")
V_L2_MD = re.compile(r"^md: (.+)$")
V_L3 = re.compile(r"^- (P\d{4}-[A-F]-\d{2,}) · 题 ([A-F]) · (.+)$")
V_L1 = re.compile(r"^P\d{4}-[A-F]-\d{2,} \| ")
V_SID = re.compile(r"P\d{4}-[A-F]-\d{2,}")
# ---- 标注文件与分类法/词表的**独立**读法（I10-a…g 的参照）-----------------------
# 标注文件 2026-09-26 由 `tests/papers/recon/PROBLEM_TYPES-draft.md` **原样转正**
# 到 `corpus/papers/PROBLEM_TYPES.md`（见 `recon/types-recon.txt` 的编者按）。
ANNOTATIONS = "corpus/papers/PROBLEM_TYPES.md"
PROBLEM_TYPES = "tools/papers/vocab/problem_types.txt"
# 标注文件的节头与标签行。与 `taxonomy.SECTION` / `taxonomy.TABLE_ROW` **各写一份**：
# 共用同一段代码就等于让 I10-e 拿实现跟自己比对（「函数跟自己对答案」，本项目第七例）。
V_ANNOT_SECTION = re.compile(r"^###\s+(\d{4})\s+([A-Z])\s*(?:—|-{1,2}\s*)?(.*)$")
V_ANNOT_ROW = re.compile(r"^\|\s*(?:`(核心|附带)`\s*)?\*\*(.+?)\*\*\s*\|")
V_TAXLINE = re.compile(r"^(L1|L2)\s*\|\s*([^|]+?)\s*\|")
# TAGS 头部那行「标注覆盖边界（机读）」的五段。
V_PT_VALUE = re.compile(
    r"标注题数=(\d+)\s*·\s*有论文的题=(\d+)\s*·\s*未配对的题=(\d+)\s*·\s*"
    r"覆盖年份=(.*?)\s*·\s*未配对逐题=(.*?)\s*——")
# `problem_type` 取值里的**占位串**（旧绊线专抓的形态：留空占位列）。「空串」也在内。
PT_PLACEHOLDERS = ("", "-", "N/A", "待定", "TODO", "?")
# 未验证篇数的上界。**实测依据**：43 份里「论文自报题号」读不出的 0 份（recon §6）、
# 「自报队号」读不出的 0 份。取 10% 与 C4/D3-b 的同一个量级，**不是拍出来的**：
# 超过它说明这不是"个别篇格式不同"，而是解析口径系统性失效。
UNVERIFIED_CEILING = 0.10
# `has_*` 零区分力的登记口径（与 recon §3 同一谓词）：一边占比 > 90% 即登记。
ZERO_DISC = 0.90
# recon 登记的分布（`tests/papers/recon/ids-recon.txt` §3「新口径（标题行）」那一列）。
# **本脚本另外自己算一遍**再与它比：不等即 FAIL（recon 是取数记录，不是判据）。
RECON_HAS_NEW = {"has_contents": 42, "has_assumptions": 42, "has_notations": 39,
                 "has_sensitivity": 36, "has_extension": 6}
# recon 登记的作者自写 Keywords 三种口径命中数（`ids-recon.txt` §4b）。
RECON_KW_WIDE, RECON_KW_DRAFT_M, RECON_KW_DRAFT = 42, 27, 0
# recon 登记的 `## ` 行总数（§2）与「编号型」拆分的两个数（§2b）。
RECON_H2_TOTAL = 2340
RECON_H2_ALONE_NUM, RECON_H2_NUM_TITLE = 574, 494
# 旧口径（全文子串）的对照数——**报告量**，说明口径确实换过（recon §3 的旧列）。
RECON_HAS_OLD = {"has_contents": 42, "has_assumptions": 43, "has_notations": 40,
                 "has_sensitivity": 38, "has_extension": 25}
RECON_NAIVE_FIG, RECON_NAIVE_TAB = 597, 212
RECON_C1_FIG, RECON_C1_TAB = 682, 253


def v_lines(text: str) -> list[str]:
    """md 全文 → 行表。**只用 `\\n` 切**（与 `index.md_lines` 同一口径，但这是**另写的一份**：
    `str.splitlines()` 会在 `\\x0b`/`\\u2028` 处也切，两套切法会让「偏移↔行号」错位）。"""
    return text.split("\n")


def v_pages(lines: list[str]) -> list[int]:
    """逐行 → 页码（该行之前最近的 `<!-- page N -->` 锚）。"""
    out, cur = [], 0
    for ln in lines:
        m = V_PAGE_ANCHOR.match(ln.rstrip("\r"))
        if m:
            cur = int(m.group(1))
        out.append(cur)
    return out


def split_unesc(s: str, sep: str) -> list[str]:
    """按**未转义**的 `sep` 切分（转义规则见 `index._esc`）。"""
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
    """`index._esc` 的逆（**独立实现**，逐字符扫描）。"""
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


def v_has_flags(h2: list[str]) -> dict:
    """`has_*` 的参照实现：**md 的 `## ` 标题行里字面出现**（不区分大小写）。"""
    blob = "\n".join(h2).lower()
    return {k: any(x.lower() in blob for x in p) for k, p in V_HAS_PROBES.items()}


def v_problem_field_present(text: str) -> bool:
    """论文**有没有**「Problem Chosen」这个栏位/行——**只判字段在不在，不判读不读得出**。

    这是三态里「没有该栏」与「有栏但读不出」分开的**唯一**依据：`v_problem` 对这两种
    情形**都返回 `None`**，只拿它计数会把两态混成一个数（于是「没有该栏 0 份」只能靠
    硬编码常量去说，语料一变就静默说谎）。两个正则都算「栏位在」：行内形
    （`Problem Chosen: A`）与独占一行的栏位形（`**Problem Chosen**` + 下一行单字母）。
    """
    return bool(V_PROBLEM_INLINE.search(text) or V_PROBLEM_FIELD.search(text))


def v_problem(text: str) -> str | None:
    mi = V_PROBLEM_INLINE.search(text)
    if mi:
        return mi.group(1).upper()
    m = V_PROBLEM_FIELD.search(text)
    if not m:
        return None
    for ln in [x for x in text[m.end():].split("\n") if x.strip()][:6]:
        ml = V_LONE_LETTER.fullmatch(ln)
        if ml:
            return ml.group(1).upper()
        if V_FIELD_STOP.search(ln):
            return None
    return None


def v_team(text: str) -> str | None:
    mi = V_TEAM_INLINE.search(text)
    if mi:
        return mi.group(1)
    m = V_TEAM_FIELD.search(text)
    if not m:
        return None
    for ln in [x for x in text[m.end():].split("\n") if x.strip()][:5]:
        s = ln.strip().strip("*_# ").strip()
        if re.fullmatch(r"\d{6,8}", s):
            return s
        if V_FIELD_STOP.search(s):
            return None
    return None


# ---- 词表的**参照实现**（本脚本按 models.txt 的数据把匹配规则重写一遍）------
def v_load_terms(path: Path) -> list[tuple[str, tuple[str, ...]]]:
    """读词表 → `[(规范词, (变体…)), …]`。**不 import `vocab.load`**。"""
    out = []
    for ln in path.read_bytes().decode("utf-8").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        out.append((parts[0], tuple(x for x in parts if x)))
    return out


def v_annotation_labels(path: Path) -> dict[tuple[int, str], set[str]]:
    """**本脚本自己解析标注文件** → `{(年, 题号): {`L1 · L2`, …}}`。

    这是 I10-e 的**期望值**来源：`index.annotations_problem_types()`（经
    `taxonomy.load_annotations`）是**实现**侧，本函数是**参照**侧，两套正则各写一份。
    **绝不调用实现**——一旦共用，「产物那一栏 == 标注那一节」就变成拿实现跟自己对答案
    （本项目第七例的 D1 就是这么来的：判据恒真而全绿）。
    """
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    out: dict[tuple[int, str], set[str]] = {}
    cur: tuple[int, str] | None = None
    for ln in text.split("\n"):
        m = V_ANNOT_SECTION.match(ln.rstrip())
        if m:
            cur = (int(m.group(1)), m.group(2))
            out.setdefault(cur, set())
            continue
        if cur is None:
            continue
        m2 = V_ANNOT_ROW.match(ln.rstrip())
        if m2 and " · " in m2.group(2):
            out[cur].add(m2.group(2).strip())
    if not out:
        raise ValueError(f"标注文件里一个 `### <年> <题号>` 节都没解析出来：{path}")
    return out


def v_problem_types(path: Path) -> set[str]:
    """分类法全部条目名（L1+L2），**独立读**（不 import `taxonomy.load_taxonomy`）。"""
    out: set[str] = set()
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        m = V_TAXLINE.match(ln.strip())
        if m:
            out.add(m.group(2).strip())
    if not out:
        raise ValueError(f"分类法里一条都没读出来：{path}")
    return out


def v_pt_name_parts(name: str) -> list[str]:
    """标签名 → 去编号后的**整名**与 `/`、`、`、括号拆出的**成分**（T3 的移植）。

    整名与成分都要判：漏判成分会放过 `4.3 随机仿真/蒙特卡洛` 这种「整名不同、
    成分与词表同名」的形态（`verify_types.py` T3 的实测理由）。
    """
    whole = re.sub(r"^\d+(?:\.\d+)?\s+", "", name).strip()
    parts = [whole]
    for piece in re.split(r"[/、()（）]", whole):
        piece = piece.strip()
        if piece and piece not in parts:
            parts.append(piece)
    return parts


def v_term_pattern(variant: str) -> tuple[str, int]:
    """变体 → `(正则, flags)`。规则与 `vocab.py` 的 docstring 逐条对应，但**是另写的一份**：
    含 ASCII 字母/数字才加词边界；变体自身含 `*`/`_` 时邻接集合并上 `*` `_`；
    全大写字母的缩写**大小写敏感**（否则英文动词 `did` 会命中 `DID`）。"""
    esc = re.escape(variant)
    if not re.search(r"[A-Za-z0-9]", variant):
        return esc, re.IGNORECASE
    cls = "A-Za-z0-9"
    if "*" in variant or "_" in variant:
        cls += r"*_"
    letters = [c for c in variant if c.isascii() and c.isalpha()]
    flags = 0 if (len(letters) >= 2 and all(c.isupper() for c in letters)) else re.IGNORECASE
    return rf"(?<![{cls}]){esc}(?![{cls}])", flags


def v_term_positions(text: str, variants: tuple[str, ...]) -> set[int]:
    """该词条在 `text` 里的**全部出现位置**（同一位置多变量体只算一次）。"""
    pos: set[int] = set()
    for v in variants:
        pat, flags = v_term_pattern(v)
        for m in re.finditer(pat, text, flags):
            pos.add(m.start())
    return pos


def v_term_in_line(line: str, variants: tuple[str, ...]) -> bool:
    for v in variants:
        pat, flags = v_term_pattern(v)
        if re.search(pat, line, flags):
            return True
    return False


def _line_of(lines: list[str], off: int) -> int:
    """字符偏移 → 行号（与 `index._line_index_of` 同一判定的**另一份实现**）。"""
    cur = 0
    for i, ln in enumerate(lines):
        if cur + len(ln) >= off:
            return i
        cur += len(ln) + 1
    return len(lines) - 1


def checks(lines: list[str], limit: int = 0, meta: dict | None = None,
           out: Path | None = None, report=None) -> bool:
    """判据主体。**被测模块的 import 放在函数体内**（照 `verify_d.py`）。"""
    from tools.papers import index as index_mod
    from tools.papers import io, report as rep
    from tools.papers import vocab as vocab_mod

    root = io.ORIGIN / COLLECTION
    all_pdfs = sorted(root.rglob("*.pdf"))
    # fail-closed：试点目录取不到就抛，不得空跑一圈然后报「全通过」。
    if not all_pdfs:
        raise FileNotFoundError(f"试点目录下没有任何 PDF：{root}")
    sample = rep.pick_sample(all_pdfs, limit, FOCUS)
    if meta is not None:
        meta["n_sample"], meta["n_all"] = len(sample), len(all_pdfs)

    prod_dir = io.DERIVED if limit <= 0 else rep.LIMITED_DIR / "ids-products"
    release_products = [io.DERIVED / n for n in ("INDEX.md", "TAGS.md", "PROVENANCE.md")]
    pre_products = {p: rep.sha256_of(p) for p in release_products}

    lines.append(
        f"索引判据 I1–I13 · **限样本 {len(sample)}/{len(all_pdfs)} 份**"
        f"（--limit {limit} + 见证集 {'/'.join(FOCUS)}）"
        if limit > 0 else f"索引判据 I1–I13 · 试点 {len(sample)} 份")
    if limit > 0:
        lines.append(f"  取样：{' '.join(p.stem for p in sample)}")
        lines.append(
            f"  ! 这是**限样本跑**，不是放行依据；放行证据是 "
            f"{rep.rel(rep.release_path('ids'))}。产物写到 {rep.rel(prod_dir)}"
            f"（**不入库**），入库的三份产物本次**只读、不写**。")
    lines.append("=" * 78)

    ok = True

    def add(name: str, good: bool, msgs=()) -> None:
        nonlocal ok
        if not good:
            ok = False
            lines.append(f"{name}=FAIL")
        else:
            lines.append(f"{name}=OK")
        for m in msgs:
            lines.append(f"    {m}")

    # ---- 建产物（限样本跑写临时目录；全量跑写入库落点）--------------------
    res = index_mod.build(COLLECTION, sample=None if limit <= 0 else sample,
                          out_dir=prod_dir)
    idx = index_mod.md_lines((prod_dir / "INDEX.md").read_bytes().decode("utf-8"))
    tags = index_mod.md_lines((prod_dir / "TAGS.md").read_bytes().decode("utf-8"))
    prov = index_mod.md_lines((prod_dir / "PROVENANCE.md").read_bytes().decode("utf-8"))

    # ---- 产物解析（**只读产物**）------------------------------------------
    def cells_of(row: str, sep: str) -> list[str]:
        body = row.strip()
        if body.startswith("|") and body.endswith("|"):
            body = body[1:-1]
        return [unesc(x).strip() for x in split_unesc(body, sep)]

    idx_hdr_cells: list[str] = []
    idx_rows: list[list[str]] = []
    for ln in idx:
        if not ln.startswith("| ") or ln.startswith("| :"):
            continue
        cs = cells_of(ln, "|")
        if cs and V_SID.fullmatch(cs[0].strip()):
            idx_rows.append([c.strip() for c in cs])
        elif cs and "稳定 ID" in cs[0]:
            idx_hdr_cells = [c.strip() for c in cs]
    l1: list[list[str]] = []
    tags_hdr: list[str] = []
    for ln in tags:
        if V_L1.match(ln):
            l1.append([x.strip() for x in split_unesc(ln, " | ")])
        elif ln.strip().startswith("stable_id | ") and not tags_hdr:
            tags_hdr = [x.strip() for x in split_unesc(ln.strip(), " | ")]
    l2: list[tuple[str, str, list[tuple[str, int, int, str]]]] = []
    l3: list[str] = []
    cur_sid, cur_md, cur_hits = None, "", []
    in_l3 = False
    for ln in tags:
        if ln.startswith("## 第三层"):
            if cur_sid is not None:
                l2.append((cur_sid, cur_md, cur_hits))
                cur_sid, cur_md, cur_hits = None, "", []
            in_l3 = True
            continue
        if in_l3:
            m = V_L3.match(ln)
            if m:
                l3.append(m.group(1))
            continue
        m = V_L2.match(ln)
        if m:
            if cur_sid is not None:
                l2.append((cur_sid, cur_md, cur_hits))
            cur_sid, cur_md, cur_hits = m.group(1), "", []
            continue
        if cur_sid and ln.startswith("md: "):
            cur_md = V_L2_MD.match(ln).group(1)
            continue
        if cur_sid and ln.startswith("- "):
            parts = split_unesc(ln[2:], "; ")
            if len(parts) != 4:
                cur_hits.append(("<<点数≠4>>" + ln[:60], -1, -1, ""))
                continue
            mp, mx = re.fullmatch(r"p(-?\d+)", parts[1]), re.fullmatch(r"x(-?\d+)", parts[2])
            cur_hits.append((unesc(parts[0]), int(mp.group(1)) if mp else -1,
                             int(mx.group(1)) if mx else -1, unesc(parts[3])))
    if cur_sid is not None:
        l2.append((cur_sid, cur_md, cur_hits))
    # PROVENANCE 行 → `(稳定 ID, 词干, 年月, 原件, md)`。**六列全取**（此前只取 3 列，
    # `年月` 与 `md` 两列入库却**无判据**——「入库了却没人验」正是本项目的失守形态）。
    prov_rows: list[tuple[str, str, str, str, str]] = []
    for ln in prov:
        if not ln.startswith("| P"):
            continue
        c = [unesc(x).strip().strip("`") for x in split_unesc(ln.strip()[1:-1], "|")]
        if len(c) >= 6 and V_SID.fullmatch(c[0]):
            prov_rows.append((c[0], c[3], c[1], c[4], c[5]))

    col = {n: (tags_hdr.index(n) if n in tags_hdr else -1) for n in tags_hdr}
    col.update({n: -1 for n in ("stable_id", "year", "problem", "n_pages", "n_figures",
                                "n_tables", "n_equations", "models", "sections",
                                "keywords", *V_HAS_ORDER) if n not in col})

    # ---- 独立参照：磁盘 / md / 放行证据 -----------------------------------
    disk = {p.stem: p for p in sample}
    mds = {}
    for p in sample:
        md = io.md_path(COLLECTION, io.problem_of(str(p.relative_to(io.ORIGIN))), p.stem)
        if not md.is_file():
            raise FileNotFoundError(f"md 产物缺失：{md}")
        mds[p.stem] = md
    # 到达顺序（**独立数一遍**：按磁盘字典序、逐题号计数）
    per: dict[str, int] = {}
    expected_sid: dict[str, str] = {}
    for p in sample:
        prob = io.problem_of(str(p.relative_to(io.ORIGIN)))
        per[prob] = per.get(prob, 0) + 1
        expected_sid[p.stem] = io.stable_id(COLLECTION, prob, per[prob])
    sid2stem = {v: k for k, v in expected_sid.items()}
    # 放行证据（**独立解析**，不用 index 的解析函数）
    c_txt = rep.release_path("c").read_bytes().decode("utf-8")
    d_txt = rep.release_path("d").read_bytes().decode("utf-8")
    ev_c = {m.group(1): (int(m.group(3)), int(m.group(4))) for m in V_C1_ROW.finditer(c_txt)}
    ev_d = {m.group(1): int(m.group(2)) for m in V_D1_ROW.finditer(d_txt)}
    # 词表（**独立读**）
    terms = v_load_terms(ROOT / "tools" / "papers" / "vocab" / "models.txt")
    term_variants = dict(terms)

    # ---- 逐篇重算 ---------------------------------------------------------
    ref: dict[str, dict] = {}
    import fitz
    for p in sample:
        text = mds[p.stem].read_bytes().decode("utf-8")
        ln_ = v_lines(text)
        pages = v_pages(ln_)
        h2 = [x[3:].strip() for x in ln_ if x.startswith(V_H2)]
        with fitz.open(p) as doc:
            n_pages_pdf = doc.page_count
        first: dict[str, tuple[int, str, int]] = {}
        for w, variants in terms:
            pos = v_term_positions(text, variants)
            if not pos:
                continue
            s0 = min(pos)
            li = _line_of(ln_, s0)
            first[w] = (pages[li], ln_[li], len(pos))
        ref[p.stem] = {
            "text": text, "lines": ln_, "h2": h2, "page_of": pages,
            "pages_from_pdf": n_pages_pdf,
            "has": v_has_flags(h2),
            "keywords": (V_KEYWORDS.search(text).group(1).strip()
                         if V_KEYWORDS.search(text) else ""),
            "problem": v_problem(text), "team": v_team(text), "models": first,
            "problem_field": v_problem_field_present(text),
        }

    # ==================== I1：稳定 ID 双射 ================================
    sids = [r[0] for r in prov_rows]
    dup_id = [s for s, n in Counter(sids).items() if n > 1]
    stems = [r[1] for r in prov_rows]
    dup_stem = [s for s, n in Counter(stems).items() if n > 1]
    want, got = set(disk), set(stems)
    bad_parse: list[str] = []
    for s in sids:
        try:
            io.parse_stable_id(s)
        except ValueError:
            bad_parse.append(s)
    add("I1", not dup_id and not dup_stem and not bad_parse and got == want
        and len(prov_rows) == len(disk), [
        f"PROVENANCE 双射表 {len(prov_rows)} 行 · 磁盘样本 {len(disk)} 份 · "
        f"重复 ID {dup_id or '无'} · 重复词干 {dup_stem or '无'} · 解析失败 {bad_parse or '无'}",
        f"只在磁盘不在表 {sorted(want - got) or '无'} · 只在表不在磁盘 {sorted(got - want) or '无'}"
        f"（**两边都要空**：单边为空只是缺，不是双射）",
        "**「往返恒真」那一版已被换掉**：`parse∘stable_id` 只要两边用同一个合集名就恒真"
        "（计划草稿的三条判据无一能失败）。这里的判据是**双射**："
        "ID↔词干两向单值互逆、且并集 == 磁盘 PDF 集合（用磁盘与 `problem_of` 独立数出来的）。",
    ])
    bad_sid = [(r[1], r[0], expected_sid.get(r[1])) for r in prov_rows
               if expected_sid.get(r[1]) != r[0]]
    add("I1-b", not bad_sid, [
        f"逐篇重算的稳定 ID 与产物不等：{bad_sid or '无'}（重算 = 按磁盘字典序 + 逐题号到达顺序，"
        f"**不是**把 ID 拆开再拼回去）",
    ])
    yr = int(COLLECTION[:4])
    yr_rows = [p.stem for p in sample if re.fullmatch(r"\d{7}", p.stem)]
    yr_bad = [s for s in yr_rows if int(s[:2]) != yr % 100]
    add("I1-c", not yr_bad, [
        f"「年」与词干前两位的一致性：覆盖 {len(yr_rows)}/{len(sample)} 份"
        f"（只对 7 位数字词干起作用，覆盖不到的数量已写明）；不一致 {yr_bad or '无'}",
    ])

    # ==================== I2：条目数双边等式 ==============================
    uniq = len({r[0] for r in l1})
    # 产物**落点**断言：`build` **报告它写到哪**必须 == 本脚本**从哪读**。不等即「写一处、
    # 读另一处」——判据会对着**上一次的旧文件**下结论，而且完全无红（`IndexResult` 的
    # 三个字段此前**无人校验**：`:prod_dir / "INDEX.md"` 是判据自己拼的，不是读来的）。
    path_bad = [f"build 报告的落点 {rep.rel(k)} ≠ 本脚本读的落点 {rep.rel(v)}"
                for k, v in ((res.index_path, prod_dir / "INDEX.md"),
                             (res.tags_path, prod_dir / "TAGS.md"),
                             (res.prov_path, prod_dir / "PROVENANCE.md")) if k != v]
    add("I2", res.n_entries == uniq == len(l1) == len(idx_rows) == len(prov_rows)
        == len(disk) == len(mds) and not path_bad, path_bad + [
        f"n_entries={res.n_entries} == 唯一 ID={uniq} == TAGS 一层行数={len(l1)} "
        f"== INDEX 表行数={len(idx_rows)} == PROVENANCE 行数={len(prov_rows)} "
        f"== 磁盘 PDF（样本）={len(disk)} == md 文件（样本）={len(mds)}",
        "**双边等式，不是单边下界**（约束 5）：每一对都得相等，任一处漏一篇都会红。",
        f"**产物落点**：`IndexResult` 报告的 index/tags/prov 三路径 == 本脚本读的三份 = "
        f"{not path_bad}——判据读的必须是**这一次**写出来的那一份。",
    ])
    l2s, l3s = {a for a, _m, _h in l2}, set(l3)
    add("I2-b", not (l2s & l3s) and (l2s | l3s) == {r[0] for r in l1}, [
        f"TAGS 二层篇数 {len(l2)} + 三层篇数 {len(l3)} = {len(l2) + len(l3)}"
        f"（**必须 == {res.n_entries}**）；二层 ∩ 三层 = {sorted(l2s & l3s) or '空'}；"
        f"两层并集 == 一层 ID 集 = {(l2s | l3s) == {r[0] for r in l1}}"
        f"（**每篇恰好进一层、且没有一篇落在两层之外**）",
    ])

    # ==================== I3：sections 与 md `## ` 行逐字对账 ==============
    si = col["sections"]
    sec_bad: list[str] = []
    n_sec_total = 0
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            sec_bad.append(f"{r[0]}: 一层行对不上任何磁盘样本")
            continue
        raw = "" if si < 0 else r[si]
        want_sec = [] if raw in ("", "-") else [unesc(x) for x in split_unesc(raw, ";")]
        n_sec_total += len(want_sec)
        if want_sec != ref[stem]["h2"]:
            only_p = Counter(want_sec) - Counter(ref[stem]["h2"])
            only_m = Counter(ref[stem]["h2"]) - Counter(want_sec)
            sec_bad.append(
                f"{stem}: 产物 {len(want_sec)} 条 vs md `## ` {len(ref[stem]['h2'])} 条；"
                f"只在产物 {dict(only_p)}；只在 md {dict(only_m)}")
    add("I3", not sec_bad, sec_bad or [
        f"逐份**逐字逐条**相等：合计 **{n_sec_total}** 条 == md `## ` 行（样本内）；"
        f"差额 0 条、未解释 0 条",
        f"`sections` 取 **md `## ` 标题行逐字**（`;` 连接、去 `## ` 前缀）：本语料把「号」与「题」"
        f"常分两行排（实测「只有编号」{RECON_H2_ALONE_NUM} 条 + 「编号带题」"
        f"{RECON_H2_NUM_TITLE} 条 = {RECON_H2_ALONE_NUM + RECON_H2_NUM_TITLE} 条），"
        f"本任务**不做号/题合并那一类推断**（那是把推断写进事实栏）。",
    ])
    if limit <= 0:
        add("I3-b", n_sec_total == RECON_H2_TOTAL, [
            f"全量样本的 `## ` 行合计 **{n_sec_total}**（recon §2 登记 **{RECON_H2_TOTAL}**）"
            f"——**两边各自算的**，不等即 FAIL",
        ])

    # ==================== I4：has_* =======================================
    has_bad, dist = [], {k: 0 for k in V_HAS_ORDER}
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        vals = {k: (col[k] >= 0 and r[col[k]] == "1") for k in V_HAS_ORDER}
        for k in V_HAS_ORDER:
            dist[k] += 1 if vals[k] else 0
        if any(vals[k] != ref[stem]["has"][k] for k in V_HAS_ORDER):
            has_bad.append(
                f"{stem}: 产物 " + " ".join(f"{k}={int(vals[k])}" for k in V_HAS_ORDER)
                + " vs 重算 " + " ".join(f"{k}={int(ref[stem]['has'][k])}" for k in V_HAS_ORDER))
    add("I4", not has_bad, has_bad or [
        f"逐篇与「标题行」口径重算值**逐栏相等**（样本 {len(sample)} 份）",
        "**口径不是全文子串**：全文口径下 Contents 42/43、Assumptions 43/43、Notation 40/43、"
        "Sensitivity 38/43——前四列近乎恒真。`b-report.txt` 曾据全文口径写下"
        "「30 份论文没有 Contents 页」而实测 42/43 都有（`docs/mcm-suite-lessons.md` §4.1）。",
    ])
    if limit <= 0:
        add("I4-b", all(dist[k] == RECON_HAS_NEW[k] for k in V_HAS_ORDER), [
            "分布（标题行口径）：" + " · ".join(f"{k} {dist[k]}/{len(sample)}" for k in V_HAS_ORDER),
            "recon §3 登记：" + " · ".join(f"{k} {RECON_HAS_NEW[k]}" for k in V_HAS_ORDER)
            + f"　·　旧口径（全文子串）登记："
            + " · ".join(f"{k} {RECON_HAS_OLD[k]}" for k in V_HAS_ORDER),
        ])
    zero = [k for k in V_HAS_ORDER if dist[k] > ZERO_DISC * len(sample)]
    decl_line = next((x for x in tags if "零区分力登记" in x), "")
    pairs = re.findall(r"(has_[a-z_]+)=(\d+)/(\d+)", decl_line)
    decl_names = [a for a, _b, _c in pairs]
    decl_bad = []
    if sorted(decl_names) != sorted(zero):
        decl_bad.append(f"登记行具名的栏 {sorted(decl_names)} ≠ 零区分力集合 {sorted(zero)}")
    for a, b, c in pairs:
        if int(b) != dist.get(a, -1) or int(c) != len(sample):
            decl_bad.append(f"登记行 {a}={b}/{c} ≠ 重算 {dist.get(a)}/{len(sample)}")
    add("I4-c", not decl_bad, decl_bad or [
        f"**零区分力登记**（一边占比 > {ZERO_DISC:.0%}）：{zero or '（无）'}",
        f"TAGS 头部的登记行：{decl_line.strip()[:160]}",
        "**为什么要有这条**：近乎恒真的栏不是判据；留着它就必须**写明它零区分力**，"
        "否则下一个人会拿它当证据（`b-report.txt` 曾据全文口径写下「30 份论文没有 "
        "Contents 页」而实测 42/43 都有，见 `docs/mcm-suite-lessons.md` §4.1）。",
        "**判据形状要是「登记行具名的集合 == 自己算出的集合」**：写成「文件里出现过 "
        "`has_contents` 这个词」是**恒真**的——那个名字本身就在一层字段序里。",
    ])

    # ==================== I5：keywords ====================================
    kw_bad = []
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        got_kw = "" if col["keywords"] < 0 else unesc(r[col["keywords"]])
        if got_kw == "-":
            got_kw = ""
        if got_kw != ref[stem]["keywords"]:
            kw_bad.append(f"{stem}: 产物 {got_kw[:50]!r} vs md 重算 "
                          f"{ref[stem]['keywords'][:50]!r}")
    kw_none = sum(1 for v in ref.values() if not v["keywords"])
    n_empty_cells = sum(1 for r in l1 if col["keywords"] >= 0 and r[col["keywords"]] == "-")
    # 「无该行留空的格数 == 独立重算的无该行数」**并进条件**（此前只 `lines.append` 打印，
    # 不进 `ok`——一句 fail-open 的打印被当成判据，本项目栽过多次的形态）。
    add("I5", not kw_bad and n_empty_cells == kw_none, kw_bad or [
        f"逐篇与 md 重算值相等；**无该行留空**的格数 {n_empty_cells} == 独立重算的 "
        f"{kw_none}（样本 {len(sample)} 份）",
        f"三种口径命中数（样本 {len(sample)}）：**宽口径**（带 `re.M` + 允许行首 md 标记）"
        f"{len(sample) - kw_none} · 计划草稿正则**加** `re.M` "
        f"{_rx_count(sample, mds, V_KEYWORDS_DRAFT_M)} · 计划草稿正则**不加** `re.M` "
        f"{_rx_count(sample, mds, V_KEYWORDS_DRAFT)}",
        "**口径偏离要说清**：任务书 §六 第 8 条给的是「带 `re.M` → 27/43」。本判据用的是"
        "**更宽的**口径：43 份里 14 份写成 `**Keywords: …**`、1 份写成 `## Keywords: …`，"
        "只认裸行的正则**看不见它们**——照抄 27/43 会把 15 份**确实有** Keywords 行的论文"
        "登记成「无该行」，那是**假陈述**（约束 8）。实测 0 / 27 / 42（逐份原文见 "
        "`recon/ids-recon.txt` §4b）；**全批唯一真的没有 Keywords 行的是 `2522820`**。",
    ])
    if limit <= 0:
        add("I5-b", (len(sample) - kw_none == RECON_KW_WIDE
                     and _rx_count(sample, mds, V_KEYWORDS_DRAFT_M) == RECON_KW_DRAFT_M
                     and _rx_count(sample, mds, V_KEYWORDS_DRAFT) == RECON_KW_DRAFT), [
            f"三种口径与 recon §4b 登记一致（{RECON_KW_WIDE} / {RECON_KW_DRAFT_M} / "
            f"{RECON_KW_DRAFT}）——两边各自算的",
        ])

    # ==================== I6：n_figures/n_tables/n_equations ==============
    ev_bad = []
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        if stem not in ev_c or stem not in ev_d:
            ev_bad.append(f"{stem}: 放行证据里没有这一篇（c={stem in ev_c} d={stem in ev_d}）")
            continue
        want = (str(ev_c[stem][0]), str(ev_c[stem][1]), str(ev_d[stem]))
        got_v = (r[col["n_figures"]], r[col["n_tables"]], r[col["n_equations"]])
        if got_v != want:
            ev_bad.append(f"{stem}: 产物 图/表/公式={got_v} vs 放行证据={want}")
    add("I6", not ev_bad, ev_bad or [
        f"逐篇与放行证据**逐数相等**（样本 {len(sample)} 份）：`n_figures`/`n_tables` 读 "
        f"`{rep.rel(rep.release_path('c'))}` 的 `C1 图注=N (图F/表T)`、`n_equations` 读 "
        f"`{rep.rel(rep.release_path('d'))}` 的 `检出=N`——**不重算**",
        f"**语义**：这是**图注/编号条数**，**不是**产出 PNG 张数（C1 里 产出=908 而 图注=935）。"
        f"自己重算的口径实测得 **{RECON_NAIVE_FIG}/{RECON_NAIVE_TAB}**，与 C1 的 "
        f"**{RECON_C1_FIG}/{RECON_C1_TAB}** 逐份 11 篇不等——所以这一栏必须**读回**"
        f"（spec §6「同一份事实不在两处各算一次」）。",
        "**「不适用」的两种情形分开了**：放行证据文件不存在 → `index.read_release_*` "
        "**抛错**；证据里没有这一篇 → 也**抛错**（这里是硬失败，不记「不适用」）。"
        "**没有任何一条路径**把「阶段 4 没跑过」记成「这篇真没有公式」。",
    ])
    # **报告量**：C1 的逐份行必须全部解析到（少一行就说明解析口径漏了）
    lines.append(f"  放行证据解析（报告量）：c-report 逐篇行 {len(ev_c)} 条 · "
                 f"d-report 逐篇行 {len(ev_d)} 条 · 样本内缺登记 "
                 f"{sorted(set(disk) - set(ev_c)) or '无'} / {sorted(set(disk) - set(ev_d)) or '无'}")

    # ==================== I6-b：n_pages 的双边等式 ========================
    np_bad, anchor_bad = [], []
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        pc = ref[stem]["pages_from_pdf"]
        got = r[col["n_pages"]] if col["n_pages"] >= 0 else "?"
        if got != str(pc):
            np_bad.append(f"{stem}: 产物 n_pages={got} vs **原件** page_count={pc}")
        n_anchor = sum(1 for x in ref[stem]["lines"] if V_PAGE_ANCHOR.match(x.rstrip("\r")))
        if n_anchor != pc:
            anchor_bad.append(f"{stem}: md 页锚 {n_anchor} 条 vs **原件** page_count={pc}")
    add("I6-b", not np_bad and not anchor_bad, np_bad + anchor_bad + [
        f"**双边等式**：产物 `n_pages` == **原件** `page_count`（逐篇，样本 {len(sample)} 份）"
        f"——原件是这一栏**唯一的权威**（不存在「别处已经算过一次」的产物，故不违反 spec §6）",
        "**第二条独立路径**（同一条 `add` 里）：逐篇 md 的 `<!-- page N -->` **锚条数** == "
        "原件 `page_count`（一条数 md 的锚、一条开原件数页）",
        "**为什么这一栏原先没有判据**：老版本把这两句**算出来的布尔只 `lines.append` 打印**"
        "——既不并进 `ok`、也不比产物的 `n_pages` 栏（比的是 `ref` 的 md 锚数 vs PDF 页数，"
        "**从不碰产物**）。一句 fail-open 的打印被当成了「`n_pages` 的独立参照」"
        "（本项目「判据在什么都没验的情况下报绿」家族的形态）。现在两句都在条件里。",
        "**I7 的页码判据不能替代它**：I7 的两边**都从 md 数页**，md 页锚缺失时两边同时得 "
        "`p0` → **绿着过**；只有这一条拿**原件**当参照。",
    ])

    # ==================== I7：models 指针 =================================
    ptr_bad: list[str] = []
    n_ptr = 0
    l1_models: dict[str, list[str]] = {}
    for r in l1:
        raw = "" if col["models"] < 0 else r[col["models"]]
        l1_models[r[0]] = ([] if raw in ("", "-")
                           else [unesc(x) for x in split_unesc(raw, ";")])
    for sid, md_line, hits in l2:
        stem = sid2stem.get(sid)
        if stem is None:
            ptr_bad.append(f"{sid}: 二层小标题的 ID 不在磁盘样本里")
            continue
        want_md = mds[stem].relative_to(io.REPO).as_posix()
        if md_line != want_md:
            ptr_bad.append(f"{sid}: 二层的 md 指针 {md_line!r} ≠ 该篇真实 md 路径 {want_md!r}")
        seen: list[str] = []
        lineset = ref[stem]["lines"]
        for w, pg, n_occ, snippet in hits:
            n_ptr += 1
            seen.append(w)
            variants = term_variants.get(w)
            if variants is None:
                ptr_bad.append(f"{stem}: 指针里的词 {w!r} **不在词表里**")
                continue
            if snippet not in lineset:
                ptr_bad.append(f"{stem}/{w}: 片段**不是该篇 md 的任意一整行**"
                               f"（定位失败）：{snippet[:60]!r}")
                continue
            li = lineset.index(snippet)
            if not v_term_in_line(snippet, variants):
                ptr_bad.append(f"{stem}/{w}: 片段里**没有**该词（词边界下）：{snippet[:60]!r}")
                continue
            if pg != ref[stem]["page_of"][li]:
                ptr_bad.append(f"{stem}/{w}: 指针页码 p{pg} ≠ 该行在 md 里的页 "
                               f"p{ref[stem]['page_of'][li]}（**指针错位**）")
                continue
            occ = len(v_term_positions(ref[stem]["text"], variants))
            if n_occ != occ:
                ptr_bad.append(f"{stem}/{w}: 指针 x{n_occ} ≠ 独立重算的出现次数 {occ}")
                continue
            want_first = ref[stem]["models"].get(w, (None, None, None))
            if (pg, snippet) != (want_first[0], want_first[1]):
                ptr_bad.append(f"{stem}/{w}: 指针不是该词的**首次出现**（重算 p{want_first[0]}）")
        if sorted(seen) != sorted(l1_models.get(sid, [])):
            ptr_bad.append(f"{sid}: 一层 models 词集 {sorted(l1_models.get(sid, []))} "
                           f"≠ 二层该篇词集 {sorted(seen)}")
    add("I7", not ptr_bad, ptr_bad or [
        f"指针逐条可定位：**{n_ptr}** 条（词 + md 文件 + 页码 + 片段）",
        "每条都满足（**六条都查**）：①二层小标题的 `md:` 指针 == 该篇真实的 md 仓库相对路径 "
        "②片段是该篇 md 的**一整行逐字** ③该行**含该词**（词边界下）"
        "④页码 == 该行在 md 里自己的页（由 `<!-- page N -->` 锚数出）"
        "⑤`xN` == 本脚本**独立重算**的出现次数 ⑥是该词的**首次出现**",
        "**不是「全文偏移」**：计划草稿的指针是「该词在全文文本中的字符位置」——那个位置在"
        "**任何入库产物里都不可定位**（md 是重排产物、没有稳定偏移），"
        "「可据此复核」是**假陈述**。现在指针是**整行逐字**，`grep -F` 就能核。",
        "**强度边界**：它验证的是「指针指得回 md 的那一行」，**不是**「这一行里的词就是"
        "这篇论文的模型」。后者是判断，不在本任务范围（词表命中的语义边界写在 TAGS 头部）。",
    ])
    zero_ref = sum(1 for s in sample if not ref[s.stem]["models"])
    add("I7-b", len(l3) == zero_ref and len(l2) == len(sample) - zero_ref, [
        f"三层（零命中篇）{len(l3)} == 独立重算的零命中篇数 {zero_ref}；"
        f"二层 {len(l2)} == 样本 − 零命中 = {len(sample) - zero_ref}",
    ])

    # ==================== I8：题目 ↔ 论文 对应 ============================
    mm, unver_none, unver_unread = [], [], []
    for r in l1:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        declared = ref[stem]["problem"]
        if declared is None:
            # **三态**：栏位不在（= 参照不存在 → 不适用）vs 栏位在却读不出（= 参照存在
            # 但没解析出来 → 硬失败，约束 4）。`v_problem` 对两者**都**返回 `None`，
            # 故必须另问一句「栏位在不在」，不能只看 `None`。
            (unver_unread if ref[stem]["problem_field"] else unver_none).append(stem)
            continue
        if col["problem"] < 0 or declared != r[col["problem"]]:
            mm.append(f"{stem}: 产物题号 {r[col['problem']] if col['problem'] >= 0 else '?'}"
                      f" vs **论文自报** {declared}")
    n_unver = len(unver_none) + len(unver_unread)
    add("I8", not mm and not unver_unread, mm + [
        f"{s}: 论文自报题号**读不出**，但该篇**确有** `Problem Chosen` 栏位——"
        f"参照存在而解析失败 ⇒ **硬失败**（约束 4，不得记「不适用」）"
        for s in unver_unread] + [
        f"逐篇 `产物题号` vs `论文自报题号`（摘要页 `Problem Chosen` 一类）："
        f"**一致 {len(sample) - n_unver - len(mm)} 份 · 不符 {len(mm)} 份 · "
        f"未验证 {n_unver} 份**",
        f"**三态逐态真报**（**「没有该栏」≠「有但读不出」≠「读出来与目录不符」**）："
        f"没有该栏 {len(unver_none)} 份 {unver_none or ''} · "
        f"有但读不出 {len(unver_unread)} 份 {unver_unread or ''} · 不符 {len(mm)} 份",
        "**为什么要拆三态**：`v_problem` 对「没有该栏」与「有栏但读不出」**同样返回 "
        "`None`**，原先两态**混进同一个计数**、再由判据**印死「没有该栏 0 份」**——"
        "那个 0 在当前语料下恰好为真（侦察侧 `ids-recon-scan.py` 确实分了三态），"
        "但**判据自己不测** ⇒ 语料一变这行就静默说谎（约束 4 + 约束 8）。"
        "现在 `n_none`/`n_unreadable` 由 `v_problem_field_present(text)` 当场分开。",
        "**「有栏但读不出」= 硬失败**（判断与理由）：约束 4 要求「参照**存在**但没解析出来」"
        "判硬失败，「参照**不存在**」才是不适用。栏位在而读不出 ⇒ 解析口径**系统性失效**"
        "（不是「这篇格式特别」）——它原先与「没有该栏」共享同一个 10% 上界，"
        "等于**用上界把一个解析 bug 洗成「未验证」**。当前语料实测 0 份，故这条升级"
        "**不改变本次结论**、只把口径收严。",
        "**这条不是形式**：一篇被错放进目录的论文会**静默毒化**整条「题型 → 模型」配对链"
        "（Task 6b 的配对以 `(origin, problem)` 为地基），而计划草稿对它**没有任何判据**。",
    ])
    ur = n_unver / len(sample)
    add("I8-b", ur <= UNVERIFIED_CEILING, [
        f"「未验证」占比 {n_unver}/{len(sample)} = {ur * 100:.2f}%"
        f"（上界 {UNVERIFIED_CEILING * 100:.0f}%）——三态里的**前两态**（「没有该栏」"
        f"{len(unver_none)} + 「有栏读不出」{len(unver_unread)}）；"
        f"**「未验证」是「通过」与「失败」之间唯一诚实的位置**（沿用 C4 的裁决），"
        f"但它**必须有上界**，否则整列「读不出」也能绿。",
        "**口径比原先更严**：「有栏读不出」已由 I8 单独判**硬失败**，这里**仍**把它计入"
        "占比（上界覆盖的集合不缩小）——两处都不放宽。",
    ])
    tm_bad = []
    for r in idx_rows:
        stem = sid2stem.get(r[0])
        if stem is None:
            continue
        team_cell = r[3] if len(r) > 3 else "?"
        if team_cell != stem:
            tm_bad.append(f"{stem}: INDEX 队号栏 {team_cell!r} ≠ 文件名词干 {stem!r}")
        declared = ref[stem]["team"]
        if declared is not None and declared != stem:
            tm_bad.append(f"{stem}: 论文自报队号 {declared} ≠ 词干 {stem}")
    tm_unver = [s for s in sample if ref[s.stem]["team"] is None]
    add("I8-c", not tm_bad, tm_bad or [
        f"队号三向一致：**INDEX 栏 == 文件名词干 == 论文自报队号**；"
        f"自报读不出的 {len(tm_unver)} 份 {tm_unver or '（无）'}",
    ])

    # ==================== I9：PROVENANCE 双射 =============================
    # 双射表里**每一列**都要有等式（此前 `年月` 与 `md` 两列入库却**无判据**：
    # `prov_rows.append((c[0], c[3], c[4]))` 把 `c[1]`/`c[5]` 丢掉了）。
    prov_bad = []
    for sid_p, stem_p, yy_p, pdf_p, md_p in prov_rows:
        if yy_p != sid_p[1:5]:
            prov_bad.append(f"{stem_p}: 「年月」栏 {yy_p!r} ≠ 稳定 ID 里的年份 "
                            f"{sid_p[1:5]!r}")
        if stem_p not in disk:
            continue
        want_md = mds[stem_p].relative_to(io.REPO).as_posix()
        if md_p != want_md:
            prov_bad.append(f"{stem_p}: `md` 栏 {md_p!r} ≠ 磁盘上该篇 md 的仓库相对路径 "
                            f"{want_md!r}")
        want_pdf = disk[stem_p].relative_to(io.ORIGIN).as_posix()
        if pdf_p != want_pdf:
            prov_bad.append(f"{stem_p}: `原件` 栏 {pdf_p!r} ≠ 磁盘上的原件路径 {want_pdf!r}")
    add("I9", len(prov_rows) == len(disk)
        and len({r[0] for r in prov_rows}) == len(prov_rows)
        and len({r[1] for r in prov_rows}) == len(prov_rows) and not prov_bad,
        prov_bad + [
        f"`PROVENANCE.md` 双射表 {len(prov_rows)} 行 · 唯一 ID {len({r[0] for r in prov_rows})} "
        f"· 唯一词干 {len({r[1] for r in prov_rows})}（**两向单值 ⇒ 互逆**）",
        f"**六列逐列落地**（不等 {prov_bad or '无'}）：`年月` == 稳定 ID 的年份、"
        f"`原件` == 磁盘上的原件相对路径、`md` == 磁盘上该篇 md 的仓库相对路径"
        f"（前两列此前**入库却无判据**——`年月` 与 `md` 被解析时直接丢掉）。",
        "为什么必须有这张表：稳定 ID **内容无关**（按到达顺序生成）⇒ `ID → 原件` 推不出来。"
        "INDEX 的「队号」栏是给人看的定位列，本表是可判的那一份。",
    ])

    # ==================== I10：栏位契约（**解冻后**）=======================
    # **解冻记录（2026-09-26，用户裁决「解冻并强化 I10」）**：
    # 旧的 I10 是「Task 6b 的两栏（`原题类型` / `problem_type`）**必须缺席**」的绊线，
    # 它当初挡的是**「留空占位列」**这类假绿（Task 6 不得替 6b 占位）。6b 现在**就是要**
    # 这一栏 ⇒ 绊线**到期退场**，但**它的保护一条都不许丢**：
    #   * 「不许留空/占位」→ 原样搬到 **I10-b**（逐行非空且不属占位串集合）；
    #   * 「INDEX 的**表头**不得出现 `原题类型`」→ **保持不变**（用户只要求 `TAGS.md`
    #     带这一栏；判的仍是表头那一行，不是全文——正文里一句解释不是占位列）；
    #   * 「TAGS 字段序」→ 从「必须缺席」**反向**为「必须在**末尾**出现」（末尾是为了
    #     让已有字段的**位置一个都不变**）。
    # **「不只是删掉那两行 `if`」是可判的**：删了 `if` 而不补，I10-b 与 I10 的末尾断言
    # 都会红（变异 6/7/8 各证明一条）。
    bad_hdr = []
    for w in ("稳定 ID", "年份", "题号", "队号", "页数", "图注", "表注", "公式",
              "主题", "模型/算法", "亮点"):
        if not any(w in c for c in idx_hdr_cells):
            bad_hdr.append(f"INDEX 表头缺栏 {w}")
    for w in ("stable_id", "year", "problem", "n_pages", "n_figures", "n_tables",
              "n_equations", "models", "sections", "keywords"):
        if w not in tags_hdr:
            bad_hdr.append(f"TAGS 一层缺栏 {w}")
    if any("原题类型" in c for c in idx_hdr_cells):
        bad_hdr.append("INDEX 的**表头**里出现了 `原题类型`——用户 2026-09-26 只要求 "
                       "`TAGS.md` 带这一栏；INDEX 的表头**继续不得**出现它")
    if tags_hdr[-1:] != ["problem_type"]:
        bad_hdr.append(f"TAGS 字段序的**末尾**不是 `problem_type`（实测末尾 = "
                       f"{tags_hdr[-1:] or '（字段序没解析出来）'}）——加在末尾才能保证"
                       f"已有字段的位置一个都不变")
    add("I10", not bad_hdr, bad_hdr or [
        "栏位齐全：INDEX 表头 11 栏 + TAGS 一层原有 10 栏；"
        "**INDEX 表头继续不得出现 `原题类型`**（那一栏只在 TAGS 里）；"
        "**`problem_type` 在 TAGS 字段序的末尾**（解冻时点名的位置约束）。",
        "**解冻不丢保护**：旧绊线抓的「留空占位列」由 I10-b 承接（逐行非空 + 占位串集合），"
        "「表头不得出现该栏」在 INDEX 一侧原样保留。",
    ])

    # ---- `problem_type` 栏的**独立参照**（I10-a…g 的立足点）---------------
    # 取值侧：**只读产物**（TAGS 一层的最后一格），不读实现自报的任何变量。
    pt_col = tags_hdr.index("problem_type") if "problem_type" in tags_hdr else -1
    pt_text: dict[str, str] = {}
    pt_labels: dict[str, list[str]] = {}
    for r in l1:
        sid = r[0]
        raw = r[pt_col] if 0 <= pt_col < len(r) else None
        pt_text[sid] = "" if raw is None else raw
        # **先按未转义的 `;` 切、再逐段反转义**（顺序反了会把标签内部字面的 `;` 也切开）
        pt_labels[sid] = ([] if raw is None else [unesc(x) for x in split_unesc(raw, ";")])
    # 期望侧：**本脚本自己解析标注文件**（另一份实现，见 `v_annotation_labels`）——
    # **绝不调 `index.annotations_problem_types()` / `taxonomy.load_annotations()`**：
    # 一旦两边共用同一段代码，I10-e 就退化成「函数跟自己对答案」（本项目第七例：D1 恒真判据）。
    ann_labels = v_annotation_labels(ROOT / ANNOTATIONS)
    pt_names = v_problem_types(ROOT / PROBLEM_TYPES)
    vocab_norm = {re.sub(r"\s+", "", v).casefold() for _c, vs in terms for v in vs}
    by_prob_val: dict[str, set[str]] = {}
    by_prob_rows: dict[str, list[str]] = {}
    for r in l1:
        prob = r[col["problem"]] if col["problem"] >= 0 else "?"
        by_prob_val.setdefault(prob, set()).add(pt_text[r[0]])
        by_prob_rows.setdefault(prob, []).append(r[0])

    add("I10-a", "problem_type" in tags_hdr, [
        f"`problem_type` 在 TAGS 一层字段序里 = {'problem_type' in tags_hdr}"
        f"（字段序共 {len(tags_hdr)} 栏）",
        "**与 I10 的末尾断言不是同一条**：a 判「在不在」，I10 判「在不在**末尾**」——"
        "把整栏删掉两条都红，但把它挪到中间时**只有 I10 红**（a 是它的必要不充分条件）。",
    ])
    bad_empty = [f"{sid}：取值 {raw!r}" for sid, raw in sorted(pt_text.items())
                 if raw.strip() in PT_PLACEHOLDERS]
    add("I10-b", not bad_empty and len(pt_text) == len(l1) > 0, bad_empty[:20] + [
        f"**{len(pt_text)} 行逐行非空、且不属占位串集合** "
        f"{list(PT_PLACEHOLDERS)}（本判据就是旧绊线的保护：**空占位列照样红**）",
        "**为什么这条必须留着**：Task 6 的旧 I10 抓的正是「留空占位列」这类假绿——"
        "绊线到期（6b 就是要这一栏）时**保护不许跟着走**。",
    ])
    bad_c = [f"题 {prob}：{len(vals)} 种取值 {sorted(vals)}（{by_prob_rows[prob]}）"
             for prob, vals in sorted(by_prob_val.items()) if len(vals) != 1]
    add("I10-c", not bad_c, bad_c or [
        f"**同一 `problem` 字母的所有行取值逐字相同**：{len(by_prob_val)} 个题号，"
        f"每个题号覆盖 {[len(v) for _p, v in sorted(by_prob_rows.items())]} 篇",
        "题型是**题**的属性、不是**篇**的属性——同题的不同论文必须写出同一个题型串。",
    ])
    n_letters = len(by_prob_val)
    n_vals = len({next(iter(v)) for v in by_prob_val.values()})
    add("I10-d", n_letters == n_vals and (limit > 0 or n_letters == 6), [
        f"出现的题号字母 **{n_letters}** 个 · **互异取值 {n_vals}** 个"
        f"（纯结构断言，**不读标注文件**）",
        (f"全量跑另断言字母数 == **6**（本合集 2025 A–F）：实测 {n_letters}"
         if limit <= 0 else
         f"限样本跑只断言「字母数 == 互异取值数」：本次样本覆盖题号 "
         f"{sorted(by_prob_val)}，**不是** 6 个——故 `== 6` 这条留给全量跑"),
    ])
    bad_e: list[str] = []
    for key, want in sorted(ann_labels.items()):
        sids = [sid for sid, _t in pt_text.items()
                if sid[1:5] == str(key[0]) and sid[6] == key[1]]
        if not sids:
            continue
        got = set(pt_labels[sids[0]])
        if got != want:
            bad_e.append(f"{key[0]} {key[1]}：产物 `{'；'.join(sorted(got))}` vs 标注 "
                         f"`{'；'.join(sorted(want))}`"
                         f"（只在产物 {sorted(got - want) or '无'} · 只在标注 "
                         f"{sorted(want - got) or '无'}）")
    add("I10-e", not bad_e, bad_e or [
        f"**跨文件双边等式**：每个题号字母的取值解析出的 `(L1,L2)` 集合 == "
        f"`{ANNOTATIONS}` 里该题那一节的标签集合（**`核心` 与 `附带` 两种标记的标签全含**）"
        f"——本次比对了 **{sum(1 for k in ann_labels if any(s[1:5] == str(k[0]) and s[6] == k[1] for s in pt_text))}** "
        f"个题号",
        f"**期望值是本脚本自己解析标注文件得到的**（`v_annotation_labels`，"
        f"正则与 `taxonomy` 的各写一份）——**绝不调 `index` 的映射函数**。"
        f"两边共用代码就会让这条退化成「函数跟自己对答案」（本项目第七例的 D1 就是这样来的）；"
        f"**变异 6（让 index 写 `problem_type` 时丢掉 `附带` 标签）实测本判据红**，"
        f"证明它非恒真。",
        "**边界（必须同读）**：它验证的是「**产物那一栏 == 标注文件那一节**」，"
        "**不是**「这个题型标得对」——后者是判断，属人工标注（`verify_types.py` T1–T8 "
        "只保证引文可定位、标签合法等结构性事实）。",
    ])
    bad_f: list[str] = []
    for name in sorted({x for labs in pt_labels.values() for x in labs}):
        if " · " not in name:
            bad_f.append(f"{name!r} 不含 ` · `（应为 `L1 名 · L2 名`）")
            continue
        for x in (p.strip() for p in name.split(" · ", 1)):
            if x not in pt_names:
                bad_f.append(f"{name!r} 的一半 {x!r} 不在 `{PROBLEM_TYPES}` 里")
        for part in v_pt_name_parts(name):
            p = re.sub(r"\s+", "", part).casefold()
            if p in vocab_norm:
                bad_f.append(f"{name!r} 的成分 {part!r} == 词表（`models.txt`）里的词条/变体"
                             f"——往这一栏塞模型名会让「题型 → 模型」配对退化成同义反复")
    add("I10-f", not bad_f, bad_f or [
        f"取值里出现的 **{len({x for labs in pt_labels.values() for x in labs})}** 个标签名"
        f"（`L1 · L2`）：两半都逐字命中 `{PROBLEM_TYPES}`（{len(pt_names)} 个条目），"
        f"整名与成分**都不与词表变体相等**（{len(vocab_norm)} 个变体的归一化集合）",
        "这是 `verify_types.py` T3 的**移植**：题型侧与模型侧必须**不相交**——"
        "否则「题型 → 模型/算法」的配对就变成同义反复（`ARIMA` 这样的词一旦进了题型栏，"
        "配对就什么都没说）。",
    ])
    cov_line = next((x for x in tags if "标注覆盖边界（机读）" in x), "")
    cv = V_PT_VALUE.search(cov_line)
    cov_bad: list[str] = []
    if not cv:
        cov_bad.append(f"TAGS 头部**没有可机读的覆盖边界行**（找 `标注覆盖边界（机读）`）："
                       f"{cov_line[:120]!r}")
    else:
        n_ann, n_cov, n_unc = (int(cv.group(1)), int(cv.group(2)), int(cv.group(3)))
        listed = {tuple(x.strip().split(" ", 1)) for x in cv.group(5).split("、")
                  if x.strip() and x.strip() != "（无）"}
        listed = {k for k in listed if len(k) == 2 and k[1]}
        want_unc = {(str(y), p) for y, p in ann_labels
                    if not any(sid[1:5] == str(y) and sid[6] == p for sid in pt_text)}
        if n_ann != len(ann_labels):
            cov_bad.append(f"标注题数={n_ann} ≠ 本脚本独立解析的 {len(ann_labels)}")
        if n_cov != len(by_prob_val):
            cov_bad.append(f"有论文的题={n_cov} ≠ 产物一层的不同题数 {len(by_prob_val)}")
        if n_unc != n_ann - n_cov:
            cov_bad.append(f"未配对的题={n_unc} ≠ 标注题数 − 有论文的题 = "
                           f"{n_ann} − {n_cov} = {n_ann - n_cov}（**双边等式**）")
        if listed != want_unc:
            cov_bad.append(f"逐题具名清单与独立重算的不等：只在产物 "
                           f"{sorted(listed - want_unc) or '无'} · 只在重算 "
                           f"{sorted(want_unc - listed) or '无'}")
    add("I10-g", not cov_bad, cov_bad or [
        f"**覆盖边界可机读、且为等式**：{cov_line.strip()[:200]}",
        f"`标注题数 = 有论文的题 + 未配对的题`（{cv.group(1) if cv else '?'} = "
        f"{cv.group(2) if cv else '?'} + {cv.group(3) if cv else '?'}），"
        f"且**逐题具名清单**与「标注里有、而本次产物无论文」的独立重算集合**逐题对得上**",
        "为什么这条必要：`corpus/官方原题/` 有 2016–2026 共 67 题，而本合集只有 2025 的"
        "论文（**标注里有、产物里没有**的题是 61 道）。「没写出来」与「没有这回事」"
        "不是一回事——把边界**印成可判的一行**，下一个人就不必猜本表覆盖到哪里。",
    ])

    star_i = next((i for i, c in enumerate(idx_hdr_cells) if "亮点" in c), -1)
    nonempty = [r[0] for r in idx_rows if star_i >= 0 and len(r) > star_i + 1
                and r[star_i + 1].strip()]
    decl_star = ("[社区]" in "\n".join(idx)) and ("留空" in "\n".join(idx))
    add("I10-h", not nonempty and decl_star, [
        f"「亮点」栏非空的行：{nonempty or '无'}（**本轮一律留空**——没有可指回原文的依据就"
        f"不填推测）；头部有 `[社区]` 标级与「给不出就留空」的说明 = {decl_star}",
        "**这一条的强度边界（必须与它同读）**：它验证的是「**没有被填进推测性内容**」"
        "与「**头部有标级声明**」，**证明不了**这 43 篇没有亮点。它是**范围声明**、"
        "**不构成**任何「已覆盖」的声称。",
        "**编号说明**：本条与下一条在原文件里叫 `I10-b` / `I10-c`；解冻后 **a–g 七个"
        "子条**用的是小写字母序，故这两条顺延为 `I10-h` / `I10-i`（**判据内容一字未改**，"
        "只改编号）。",
    ])
    aw = all(("奖项注记" in "\n".join(f[:600])) for f in (idx, tags))
    add("I10-i", aw and not any("奖项" in c for c in idx_hdr_cells)
        and "奖项" not in tags_hdr, [
        f"两个 .md 的文件头都有**奖项注记**（合集内统一 = O 奖）= {aw}；"
        f"**两个 .md 都不得再设「奖项」栏**（用户 2026-09-26 定案）= "
        f"{not any('奖项' in c for c in idx_hdr_cells) and '奖项' not in tags_hdr}",
    ])

    # ==================== I11：fail-closed ================================
    missing = COLLECTION + "（不存在的名字）"
    probe_dir = rep.LIMITED_DIR / "ids-products-probe"
    threw = None
    try:
        r2 = index_mod.build(missing, out_dir=probe_dir)
        threw = (f"**没有抛错**——返回 n_entries={r2.n_entries}，并写了 "
                 f"{r2.index_path.name}/{r2.tags_path.name}/{r2.prov_path.name}")
    except Exception as e:            # noqa: BLE001 —— 要的就是"任何异常都算抛"
        lines.append(f"   fail-closed 探针：合集名 {missing!r} → 抛 "
                     f"{type(e).__name__}: {rep.scrub(str(e))}")
    add("I11", threw is None, [
        threw or "合集名不存在时 `index.build` **抛错**（不是返回空表静默 PASS）",
        f"探针的落点被**强制**指到 {rep.rel(probe_dir)}（不入库目录）——"
        f"否则「守卫被删掉」的那一版会把入库的三份产物**覆写成 0 条**"
        f"（探针自己变成破坏者，那是本项目栽过的形态）。",
        "**这就是任务书点名的那个活陷阱**：`Path.rglob` 对不存在的目录**静默返回空**，"
        "而磁盘上是 `2023年美赛O奖论文`（带「年」）、别处写作 `2023美赛O奖论文`。",
    ])

    # ==================== I12：已知边界具名断言 ===========================
    b1 = []
    for name in ("UMAP2000-2010年美赛特等奖优秀论文集",
                 "UMAP2010-2019年美赛特等奖优秀论文集"):
        try:
            io.stable_id(name, "A", 1)
            b1.append(f"{name}: **没有抛错**（与实测的 ValueError 不符）")
        except ValueError:
            pass
    a1 = io.stable_id("2023美赛O奖论文", "A", 1)
    a2 = io.stable_id("2023年美赛O奖论文", "A", 1)
    on_disk = (io.ORIGIN / "2023美赛O奖论文").is_dir()
    b2 = [] if (a1 == a2 and not on_disk) else [
        f"撞号断言不成立：{a1} vs {a2}，is_dir={on_disk}"]
    add("I12", not b1 and not b2, (b1 + b2) or [
        "① 两个 UMAP 合集名不以 4 位数字开头 → `io.stable_id` **抛 `ValueError`**"
        "（涉 37 份）：断言通过",
        f"② **跨合集撞号**：`stable_id('2023美赛O奖论文','A',1)` = **{a1}** = "
        f"`stable_id('2023年美赛O奖论文','A',1)` = **{a2}**——少一个「年」字，ID 完全相同；"
        f"而 `io.ORIGIN/'2023美赛O奖论文'` 的 `is_dir() = {on_disk}`（盘上是带「年」的）",
        "**这两条是具名边界、不是缺陷**：判据把它们**断言成行为**，而不是假装它们不存在"
        "（计划草稿的「往返一致」判据对撞号**零区分力**）。",
        "③ **本次侦察新查出来的第三条边界**：`io.problem_of` 在别的合集上抛错——"
        "`2024年美赛O奖论文/2024年美赛A题O奖论文/` 把题号写进目录名（35/35 抛错）、"
        "2023 春季赛子目录（5/42）、两个 UMAP（37/37）；故本索引**只对「题号是独立目录层」"
        "的合集成立**，别的合集 `build` 抛错是**按设计**。逐份实测见 `recon/ids-recon.txt` §5。",
    ])

    # ==================== I13：词表 =======================================
    zero_terms = [w for w, v in terms
                  if not any(v_term_positions(ref[s.stem]["text"], v) for s in sample)]
    # 增长候选：**来源限于作者自写的 Keywords 行**（一行里的词形拆出来、逐条附出现篇数）。
    # **具名范围边界**：本判据**不扫正文**（任务书 §一 的「未命中片段」那一路没做）。
    # 这是刻意选的窄口径——候选必须能**逐条指回一行原文**才可复核；扫正文需要先自造一套
    # 「什么算一个模型名」的抽取启发式，那是**判断**不是事实，且产出无法验证。
    cand = Counter()
    for s in sample:
        for piece in re.split(r"[;,；，、|/]", ref[s.stem]["keywords"]):
            piece = piece.strip().strip("*_ ").strip()
            if not (2 <= len(piece) <= 40):
                continue
            if not any(v_term_in_line(piece, v) for v in term_variants.values()):
                cand[piece] += 1
    add("I13", len(terms) > 0 and len({w for w, _ in terms}) == len(terms), [
        f"词表 **{len(terms)}** 词条、**{sum(len(v) for _, v in terms)}** 变体；规范词唯一、"
        f"格式为 `规范词 | 变体…`（**一行一条、可追加**）",
        f"**零命中词条 {len(zero_terms)} 个**（口径 = 在**本次样本 {len(sample)} 份**上一篇都不命中"
        f"；限样本跑时它只是「这批上零命中」，不是全语料结论）：",
    ] + [f"    零命中 {w!r}" for w in zero_terms] + [
        f"**词表增长候选（给 Task 6b）**：作者 Keywords 里出现、而词表**覆盖不到**的词形 "
        f"**{len(cand)}** 个，逐条（附出现篇数）：",
        "**具名范围边界（必须与上面这份清单同读）**：候选来源**只取作者自写的 Keywords 行**"
        "（`;`/`,`/`、` 拆词），**未扫正文**——任务书 §一 的「论文里出现但词表没有」"
        "（含**未命中片段**）这一路**本任务只交付了 Keywords 行这一半**。"
        "选窄口径的理由：Keywords 行里的词能**逐条指回一行原文**、可复核；扫正文要先自造"
        "一套「什么算一个模型名」的抽取启发式，那是**判断**不是事实，且产出无从验证。"
        "**代价**：正文里出现而作者没写进 Keywords 的模型**不在本清单里**。",
    ] + [f"    候选 {w!r}（{n} 篇）" for w, n in sorted(cand.items(),
                                                       key=lambda kv: (-kv[1], kv[0]))])

    # ---- I13-b：「词表可追加」**真验**（不是打印一句「不缓存」就算数）------------
    # 形态与「判据读自称」同族：原先这条 `add("I13-b", True, …)` 是**恒真**的，
    # 消息里声称「`vocab.load` 不缓存」，却**没有任何一行去验它**。
    # 现在实做：临时词表写 1 条 → `load` → 追加 1 条 → **同一进程内**再 `load`。
    n_reload = (-1, -1)
    reload_bad = []
    try:
        with tempfile.TemporaryDirectory(prefix="vocab-reload-") as td:
            tv = Path(td) / "models.txt"
            tv.write_bytes(b"probe alpha | probe alpha variant\n")
            n1 = len(vocab_mod.load(tv))
            tv.write_bytes(tv.read_bytes() + b"probe beta | probe beta variant\n")
            n2 = len(vocab_mod.load(tv))
            n_reload = (n1, n2)
        if n_reload != (1, 2):
            reload_bad.append(
                f"临时词表探针：首读 {n_reload[0]} 条（应 1）、追加一行后同一进程内再读 "
                f"{n_reload[1]} 条（应 2）——**追加没有生效**")
    except Exception as e:              # noqa: BLE001 —— 探针抛错本身就是 FAIL
        reload_bad.append(f"临时词表探针抛错：{type(e).__name__}: {rep.scrub(str(e))}")
    add("I13-b", not reload_bad, reload_bad + [
        "**真验**（不是打印一句声称）：临时词表先写 **1** 条 → `vocab.load` → **追加 1 条** "
        "→ **同一进程内**再 `vocab.load`",
        f"实测 首读 **{n_reload[0]}** 条 / 追加后 **{n_reload[1]}** 条（要求 **1 / 2**）"
        f"⇒ `vocab.load` **不缓存**，「追加即生效」成立。临时文件写在系统临时目录、"
        f"跑完即删（**不入库、报告里不出现其路径**）。",
        "**为什么非要真验**：`vocab.load` 一旦缓存（`lru_cache` 一类），"
        "「追加了却没生效」就是**静默形态**——而「词表开放、可追加」是本任务对用户的"
        "承诺（用户 2026-09-26：「新遇到的模型/算法可以加入语料库」）。"
        "原先这条是 `add(..., True, …)`：**恒真**、却计入「全部判据 OK」。"
        "变异证据：给 `vocab.load` 加 `lru_cache` 后本判据红（`ids-mutation-evidence.txt` 的 M14）。",
        "零命中与候选**都不藏**：零命中词条本身是「这批论文没用这些方法」这个语料事实"
        "（不是判据失效），候选清单是 Task 6b 的增长输入。",
    ])

    # ---- 报告量 -----------------------------------------------------------
    occ = Counter()
    for s in sample:
        for w in ref[s.stem]["models"]:
            occ[w] += 1
    lines.append("  词表命中篇数 top8（报告量）："
                 + " · ".join(f"{w} {n}" for w, n in occ.most_common(8)))
    lines.append(f"  一层 models 指针条数合计（样本）：{n_ptr}")
    lines.append("  md 页锚 vs 原件 `page_count` 的交叉核对**已从「打印」升为判据**（I6-b）："
                 "原先它算出来的布尔只 `lines.append`、且**从不碰产物的 `n_pages` 栏**"
                 "——一句 fail-open 的打印。逐篇差额（若有）见 `I6-b=FAIL` 的登记行。")

    # ==================== 限样本跑的产物完整性自检 ========================
    if limit > 0:
        post_products = {p: rep.sha256_of(p) for p in release_products}
        same = pre_products == post_products
        lines.append(f"入库产物完整性自检（限样本跑）：`corpus/papers/` 三份 .md 的 sha256 "
                     f"跑前跑后相同 = {same}（False → 本次限样本跑碰到了入库产物，判 FAIL）")
        for k in release_products:
            lines.append(f"    {rep.rel(k)}：跑前 {pre_products[k][:16]}… · "
                         f"跑后 {post_products[k][:16]}…")
        if not same:
            ok = False

    lines.append("=" * 78)
    lines.append(f"判据汇总：{'全部通过' if ok else '**有 FAIL**'}"
                 f"（所有差额逐条具名登记见上，**未解释为 0**）")
    return ok


def _rx_count(pdfs, mds, rx) -> int:
    """某个 Keywords 正则在这些 PDF 上的命中篇数（**报告量**）。"""
    return sum(1 for p in pdfs if rx.search(mds[p.stem].read_bytes().decode("utf-8")))


def main() -> int:
    import argparse

    from tools.papers import report

    ap = argparse.ArgumentParser(
        description="索引与稳定 ID 判据 I1–I13（INDEX / TAGS 三层 / PROVENANCE）",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="只跑前 N 份 + 见证集（变异演示用）。报告写到 "
             "tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/ids-report.txt）；负数不接受。",
    )
    args = ap.parse_args()

    out, guard_msg = report.resolve_report("ids", args.limit)
    pre = report.sha256_of(report.release_path("ids")) if args.limit > 0 else ""

    meta: dict = {}
    lines = ["索引与稳定 ID 判据（I1–I13）"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out, report)
    except BaseException as e:
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = report.recheck_target("ids", args.limit, out)
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
            f"  本文件是**限样本跑**（--limit {args.limit} + 见证集 {'/'.join(FOCUS)}）的"
            f"报告，**不入库、不是放行依据**；放行证据是 "
            f"{report.rel(report.release_path('ids'))}，只有全量跑会写它。")
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件。")

    text = "\n".join(lines) + "\n"
    if args.limit > 0:
        post = report.sha256_of(report.release_path("ids"))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· "
            f"{report.rel(report.release_path('ids'))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    text += (f"\nRESULT: {'PASS' if ok else 'FAIL'}"
             f"{report.result_suffix('ids', args.limit, meta, FOCUS)}\n")
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
