"""题型分类法与「题目 ↔ 标注」的受控口径（Task 6b 阶段 1）。

**这个模块负责三件事**：

1. **受控分类法**：从 `tools/papers/vocab/problem_types.txt` 读出 L1/L2 两级的名字与定义
   （`load_taxonomy`）。分类法**不是**模型词表（`vocab/models.txt`）——前者是**任务形态**、
   后者是**方法**，二者**不得同名**（判据 T3，理由见 `verify_types.py` 的 T3 一节：
   同名会让「题型 → 模型」的配对退化成同义反复）。
2. **题面文本的抽取口径**：`extract_text()` —— `pdftotext <pdf> -`（poppler 默认模式，
   **不加 `-layout`**），在 Python 里把行尾归一成 LF、去掉分页符 `\\x0c`。
   判据 T2（支撑句可定位）用的就是这一份文本，**口径唯一**，不许各脚本各抽一遍。
   另附**两条独立的「有没有文本层」探针**（`text_op_counts` 用原件内容流的操作符、
   `extract_text` 的字符数），供判据 T5 独立判定「读不出」的集合。
3. **标注的数据模型**：`Annotation` dataclass 与 `load_annotations()`，
   读的是人工撰写的标注 `corpus/papers/PROBLEM_TYPES.md`
   （格式见该文件头部；阶段 1 它是 `recon/PROBLEM_TYPES-draft.md` 的草案，
   2026-09-26 用户过闸门后**原样转正**——正文语义一字未改）。

## 抽取口径的两个已知边界（都在证据里如实登记，不藏）

* **`2020_MCM_Problem_A.pdf` 没有文本层**：全篇正文是用**矢量路径**画的（实测第 1 页
  内容流里 `BT`/`Tf`/`Tj` 操作符 **0** 个、填充路径 **2332** 条；第 2 页只有 2 个 `TJ`，
  画的是杂志名 *Hook Line and Sinker* 那两行斜体）。`pdftotext` 与 `fitz` **两个独立抽取器
  都只得到 25/22 个字符**。⇒ 这道题**无法**给出「可定位的支撑句」，T5 按「读不出」登记，
  **不靠标题猜题意**；处置与理由见 `recon/types-recon.txt` 与任务报告。
* **2020 年的首页首行是刊头**：2020 的题面首行形如
  `2020 ICM Weekend 1 Problem D: Teaming Strategies`（刊头与标题**同一行**），
  2020 MCM 的另两题是 `2020 MCM Weekend 2 Problem B: …`。故**标题一律不从「首行」推**：
  题号取自**文件名**（机器事实），标题只作展示、由 `title_of()` 按一条**具名规则**取。
"""
import argparse
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

# 官方题面的落点。**只此一处**：判据与抽取都从这里出发，不许各写一份。
PROBLEM_DIR = ROOT / "corpus" / "官方原题"

# 标注（人工撰写；2026-09-26 用户过闸门后由 `recon/PROBLEM_TYPES-draft.md` 转正到此，
# 见 `tests/papers/recon/types-recon.txt` 的编者按）。**旧名 `DRAFT_PATH` 不保留别名**——
# 留两个名字就会有人用错那个（任务书 §一 产物 1）。
ANNOTATIONS_PATH = ROOT / "corpus" / "papers" / "PROBLEM_TYPES.md"
# 受控分类法。
TAXONOMY_PATH = ROOT / "tools" / "papers" / "vocab" / "problem_types.txt"

# 数据形态（**受控枚举**，逐字取自任务书 §一 第 5 条）。写进标注的第一个词必须是其中之一。
DATA_REGIMES = (
    "无数据(纯机理/假设)",
    "时序",
    "截面",
    "面板",
    "空间/地理",
    "网络",
    "文本/文献",
    "混合",
)
# 标签标记（任务书 §一 第 2 条）：`核心` = 题干明确要求做这件事；`附带` = 题面出现但非题干任务。
MARKS = ("核心", "附带")
# 标注状态。`读不出` 是**三态里的第三态**（参照存在、但件里没有文本层），
# **不是**「不适用」——它必须逐题登记原因，且其集合由判据独立重算（T5）。
STATUS_OK, STATUS_UNREADABLE = "标定", "读不出"

# 题面文件名 → (年, 题号)。**年与题号一律取自文件名**（机器事实），
# 不从题面的任何一行文字里推（2020 的刊头会把这套推断弄错）。
PDF_NAME = re.compile(r"^(\d{4})_(?:MCM|ICM)_Problem_([A-Z])\.pdf$")
# 标题行的形态（**只用于展示**）：`2016 MCM Problem A A Hot Bath` /
# `2017 ICM` + `Problem D: Optimizing …` / `2020 MCM Weekend 2 Problem B: …` /
# `2022 ICM Problem D: Data Paralysis? Use Our Analysis!`
TITLE_INLINE = re.compile(
    r"^(?P<year>\d{4})\s+(?P<series>MCM|ICM)\s+(?:Weekend\s*\d\s+)?"
    r"Problem\s+(?P<letter>[A-Z])\b[.:\s]*(?P<title>.*)$",
    re.I,
)
TITLE_BARE = re.compile(
    r"^Problem\s+(?P<letter>[A-Z])\b[.:\s]*(?P<title>.*)$", re.I)
# 抽取文本里的**非空白行少于这个数**就判「件里没有正文文本层」。实测依据：
# 全 67 份里只有 `2020_MCM_Problem_A` 低于它（2 行），次低的 `2016_MCM_Problem_A` 是 5 行。
# 取 **4** 是「2 与 5 之间」的一个**实测空档**，不是拍的整数。
MIN_TEXT_LINES = 4
# 内容流的文本操作符（第二条独立探针）。`BT` = begin-text；实测该件全篇 **2** 个
# （且都在杂志名那两行），其余 66 份最低也有数百个。
TEXT_OP = re.compile(rb"(?<![A-Za-z])(BT|Tj|TJ)(?![A-Za-z])")
# 「件里没有正文文本层」的第二条阈值（探针二）。实测：`2020_MCM_Problem_A` 是 **4**，
# 次低的 `2017_MCM_Problem_A` 是 **102** —— 取 **50** 落在实测空档里，不是拍的整数。
MIN_TEXT_OPS = 50
# 项目符号（T2 的格式归一化第一步）。**只收列举用的几何符号**，不收 `-`/`*`：
# 后者在正文里是连字符与下标星号，去掉会把词改掉。
LIST_MARK = re.compile(r"[•●○◦‣▪▫∙]")
_QUOTE_FOLD = str.maketrans({c: '"' for c in "'’‘‛′\"“”‟″"})


@dataclass(frozen=True)
class ProblemFile:
    """一份官方题面 PDF：`(年, 题号)` 取自**文件名**，`path` 是磁盘上的原件。"""

    year: int
    problem: str
    path: Path

    @property
    def rel(self) -> str:
        return self.path.resolve().relative_to(ROOT).as_posix()


@dataclass
class Annotation:
    """一道题的标注（草案里的一节）。

    `labels` 是 `[(L1 名, L2 名, 核心|附带), …]`；`evidence_sentences` 是**逐条**的
    题面片段（英文原句，与 `labels` **按序对应到行**——一行的多个片段都算该行的支撑）。
    `status` 为 `读不出` 时 `labels`/`evidence_sentences` 为空，原因必须写在 `note` 里。
    """

    year: int
    problem: str
    title: str = ""
    abstract_zh: str = ""
    require: str = ""
    given: str = ""
    constraints: str = ""
    labels: list[tuple[str, str, str]] = field(default_factory=list)
    # 与 `labels` 等长的「该标签的支撑片段」列表（每个标签一个 list）。
    evidence_sentences: list[list[str]] = field(default_factory=list)
    data_regime: str = ""
    data_detail: str = ""
    scenario: str = ""
    status: str = STATUS_OK
    note: str = ""

    @property
    def key(self) -> str:
        return f"{self.year} {self.problem}"


# --------------------------------------------------------------------------
# 题面文本的抽取（T2 的唯一口径）
# --------------------------------------------------------------------------
def normalize_newlines(s: str) -> str:
    """行尾归一：CRLF/CR → LF，分页符 `\\x0c` → LF（`pdftotext` 逐页之间用它分隔）。"""
    return s.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")


def extract_text(path: Path) -> str:
    """`pdftotext -enc UTF-8 <pdf> -`（**不加 `-layout`**）→ 行尾归一的文本。**T2 的唯一口径。**

    不加 `-layout` 的理由：`-layout` 会按版面坐标补大量空格来对齐分栏，而本题面语料
    是单栏散文，默认模式已经按阅读序输出、且**不会**把一句里的话拆得七零八落；
    两种模式都能用，**选默认是因为它少一层版面推断**。

    **`-enc UTF-8` 是实测逼出来的**（本节口径的第一版漏了它）：中文 Windows 上
    `pdftotext` 往管道写时按 **ANSI 代码页**选编码，题面里的项目符号 `•`、弯引号 `’`、
    破折号 `–` 都被写成 GBK 字节，用 UTF-8 解出来是 **U+FFFD（`�`）**——实测
    `2025_MCM_Problem_A` 的 `•`、`2018_MCM_Problem_A` 的 `–` 都中招。那会让
    「原句可复核」这条判据**在正确的引文上误报**（引文里有 `’` 就永远定不到）。
    强制 `-enc UTF-8` 后同一批 PDF 逐字得到 `•`/`’`/`–`，**信息不再丢**。
    """
    r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"pdftotext 非零退出（{r.returncode}）：{path.name}；"
            f"stderr={r.stderr.decode('utf-8', 'replace')[:200]}")
    return normalize_newlines(r.stdout.decode("utf-8", "replace"))


def text_op_counts(path: Path) -> tuple[int, int]:
    """**独立的第二条探针**：原件内容流里的 `(文本操作符数, 填充路径数)`。

    与 `extract_text` **互不依赖**（这条不问抽取器，直接数 PDF 内容流的操作符）。
    `2020_MCM_Problem_A` 实测 `(2, 3922)`——正文是**画**出来的，不是**排**出来的。
    """
    import fitz

    n_text = n_fill = 0
    with fitz.open(path) as doc:
        for page in doc:
            cs = page.read_contents()
            for m in TEXT_OP.finditer(cs):
                n_text += 1
            n_fill += len(re.findall(rb"(?<![A-Za-z])f(?![A-Za-z])", cs))
    return n_text, n_fill


def readable_lines(text: str) -> int:
    """抽取文本里的非空白行数（剥掉行内空白后再看是否为空）。"""
    return sum(1 for ln in text.split("\n") if ln.strip())


def title_of(text: str, letter: str) -> str:
    """按**具名规则**取标题（只作展示，不参与任何判据的成立与否）。

    规则：逐行找第一条匹配 `题目行` 的（`<年> <MCM|ICM> [Weekend N] Problem <字母> …`），
    取字母之后的余文；余文为空（2017 那批把标题排在**下一行**）则取**下一个非空行**；
    整篇没有题目行（2020 MCM A 没有文本层）则返回空串——**不许拿文件名猜标题**。
    """
    lines = [ln.strip() for ln in text.split("\n")]
    nonempty = [ln for ln in lines if ln]
    for i, ln in enumerate(lines):
        m = TITLE_INLINE.match(ln)
        if m and m.group("letter").upper() == letter.upper():
            rest = m.group("title").strip()
            if rest:
                return rest
            for nxt in nonempty[nonempty.index(ln) + 1:]:
                mb = TITLE_BARE.match(nxt)
                if mb:
                    return mb.group("title").strip()
                return nxt
            return ""
        mb = TITLE_BARE.match(ln)
        if mb and mb.group("letter").upper() == letter.upper():
            return mb.group("title").strip()
    return ""


def problem_files() -> list[ProblemFile]:
    """`corpus/官方原题/**` 下的**题面** PDF，按 `(年, 题号)` 排序。

    **fail-closed**：目录取不到、或出现不符合 `<年>_[MC]CM_Problem_<字母>.pdf` 命名的
    PDF，一律**抛错**（不合命名的件可能是数据附件被误当题面）。
    """
    if not PROBLEM_DIR.is_dir():
        raise FileNotFoundError(f"官方原题目录不存在：{PROBLEM_DIR}")
    out: list[ProblemFile] = []
    bad: list[str] = []
    for p in sorted(PROBLEM_DIR.rglob("*.pdf")):
        m = PDF_NAME.match(p.name)
        if not m:
            bad.append(p.name)
            continue
        out.append(ProblemFile(int(m.group(1)), m.group(2).upper(), p))
    if bad:
        raise ValueError(f"官方原题目录里有不合命名约定的 PDF（可能是数据附件）：{bad}")
    if not out:
        raise FileNotFoundError(f"官方原题目录下没有题面 PDF：{PROBLEM_DIR}")
    out.sort(key=lambda f: (f.year, f.problem))
    return out


# --------------------------------------------------------------------------
# 受控分类法
# --------------------------------------------------------------------------
def load_taxonomy(path: Path = TAXONOMY_PATH) -> dict[str, dict[str, str]]:
    """读 `problem_types.txt` → `{"L1": {名字: 定义}, "L2": {名字: 定义}}`。

    格式（一行一条，`#` 注释、空行忽略）：

        L1 | 1 预测 | 一句话定义
        L2 | 1.1 时序外推 | 一句话定义
    """
    if not path.is_file():
        raise FileNotFoundError(f"分类法文件不存在：{path}")
    out: dict[str, dict[str, str]] = {"L1": {}, "L2": {}}
    for ln in normalize_newlines(path.read_bytes().decode("utf-8")).split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        if len(parts) != 3 or parts[0] not in ("L1", "L2"):
            raise ValueError(f"分类法行格式错误（应为 `L1|名字|定义`）：{ln!r}")
        level, name, definition = parts
        if name in out[level]:
            raise ValueError(f"分类法里 {level} 名字重复：{name!r}")
        if not definition:
            raise ValueError(f"分类法条目缺定义（任务书 §一 要求每级一句定义）：{name!r}")
        out[level][name] = definition
    if not out["L1"] or not out["L2"]:
        raise ValueError("分类法里 L1 或 L2 是空的")
    return out


def anchor_names(taxonomy: dict[str, dict[str, str]]) -> list[str]:
    """分类法全部名字（L1+L2），供 T3 与「同义反复」检查用。"""
    return list(taxonomy["L1"]) + list(taxonomy["L2"])


def name_parts(name: str) -> list[str]:
    """标签名 → 去掉编号后的**整名**与**成分**（`/`、`、`、`(` 处拆开）。

    T3 判「标签名不得是词表里的词」时，**整名与每个成分都要判**：
    漏判成分会放过 `4.3 随机仿真/蒙特卡洛` 这种「整名不同、成分与词表同名」的形态。
    """
    whole = re.sub(r"^\d+(?:\.\d+)?\s+", "", name).strip()
    parts = [whole]
    for piece in re.split(r"[/、]|\(|\)|（|）", whole):
        piece = piece.strip()
        if piece and piece not in parts:
            parts.append(piece)
    return parts


# --------------------------------------------------------------------------
# 标注草案的解析
# --------------------------------------------------------------------------
SECTION = re.compile(r"^###\s+(\d{4})\s+([A-Z])\s*(?:—|-{1,2}\s*)?(.*)$")
TABLE_ROW = re.compile(r"^\|\s*(?:`(核心|附带)`\s*)?\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$")
# 表头与分隔行：**只跳过这两行**，别的 `|` 行一律按标签行严格要求。
TABLE_HEAD = re.compile(r"^\|\s*L1 · L2\s*\|\s*支撑句\s*\|$")
TABLE_SEP = re.compile(r"^\|(?:\s*:?-{2,}:?\s*\|)+$")
# 片段：成对的直双引号。**引号内不得再出现直双引号**（撰写纪律，见草案头部）。
QUOTED = re.compile(r'"([^"]+)"')


def directive_lines(body: str) -> dict[str, str]:
    """取一节里的 `**关键字**：值` 片段（关键字 → 值）。同名取**第一条**。

    **同一行里的多个指令要各自成条**：照 2025 样板，`数据形态` 与 `场景` 写在**同一行**
    （`**数据形态**：…｜**场景**：…`）。只认行首的 `**` 会把 `场景` 整个吃掉——
    现象是 `data_regime` 把后半行也吞进去、`scenario` **恒空**（本模块第一版实测如此）。
    故先把 `｜**` 折成换行，再逐行匹配。
    """
    out: dict[str, str] = {}
    for m in re.finditer(r"^\*\*(.+?)\*\*：(.*)$", body.replace("｜**", "\n**"), re.M):
        out.setdefault(m.group(1).strip(), m.group(2).strip())
    return out


def normalize_for_locate(s: str) -> str:
    """定位用的归一化（**T2 的口径：格式归一化**）。

    步骤（**顺序固定**）：行尾归一 → **去掉项目符号** → 空白折叠 → **标点折叠**
    （`'’‘` 与 `"“”` 一律折成 `"`）→ `casefold()`。

    为什么这几步都算「格式」不算「内容」：
      * **项目符号**（`•` 等）是排版层的列举标记，不是句子的一部分——题面把一句话
        排成若干项目时，引文跨项目就会在标记处断开（2025 A 的 `• How often were the
        stairs used?` 那三问就是实例）；
      * **标点折叠**只动引号字形（直/弯、单/双），不动任何字母与词；
      * `casefold()` 只动大小写。
    **它们都不可能把「编造的句子」变成能命中的句子**——这正是 T2 要守的东西。

    **严口径一并报告**（见 `verify_types.py` 的 T2 报告量）：只做「行尾归一 + 空白折叠」
    时的命中数，差额逐条列出。读者因此**能看见**上面前两步到底做了多少事。
    """
    s = normalize_newlines(s)
    s = LIST_MARK.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.translate(_QUOTE_FOLD).casefold()


def normalize_quote(s: str) -> str:
    """片段侧的归一化：**先**去掉强调标记（`*`、`` ` ``），再按 `normalize_for_locate`。

    强调标记是**草稿自己加的**（照 2025 样板把原句里的重点词加粗），题面里没有这些字符。
    """
    return normalize_for_locate(re.sub(r"[*`]", "", s))


def normalize_strict(s: str) -> str:
    """严口径：**只**做行尾归一 + 空白折叠 + `casefold()`（不去项目符号、不折标点）。"""
    return re.sub(r"\s+", " ", normalize_newlines(s)).strip().casefold()


def load_annotations(path: Path = ANNOTATIONS_PATH) -> list[Annotation]:
    """读标注 → `[Annotation, …]`（按 `(年, 题号)` 排序）。

    格式见 `corpus/papers/PROBLEM_TYPES.md` 头部。**解析是严格模式**：
    节头不合式、标签行的标记缺失、标签名里没有 ` · ` 分隔、都**抛错**——
    「静默跳过一行」会让判据在一个少了几行的集合上绿着通过（本项目栽过的形态）。
    """
    if not path.is_file():
        raise FileNotFoundError(f"标注草案不存在：{path}")
    text = normalize_newlines(path.read_bytes().decode("utf-8"))
    out: list[Annotation] = []
    cur: Annotation | None = None
    body_buf: list[str] = []
    row_buf: list[str] = []

    def close_row() -> None:
        if cur is None or not row_buf:
            row_buf.clear()
            return
        ln = row_buf[0]
        row_buf.clear()
        m = TABLE_ROW.match(ln)
        if not m:
            raise ValueError(f"{cur.key}: 标签行不合式（应有 `| \\`核心\\` **L1 · L2** | 支撑句 |`）：{ln!r}")
        mark, label, cell = m.group(1), m.group(2).strip(), m.group(3)
        if mark not in MARKS:
            raise ValueError(f"{cur.key}: 标签 {label!r} 缺 `核心`/`附带` 标记")
        if " · " not in label:
            raise ValueError(f"{cur.key}: 标签 {label!r} 不含 ` · `（应为 `L1 名 · L2 名`）")
        l1, l2 = [x.strip() for x in label.split(" · ", 1)]
        cur.labels.append((l1, l2, mark))
        cur.evidence_sentences.append([q.strip() for q in QUOTED.findall(cell)])

    def close_section() -> None:
        nonlocal cur, body_buf
        if cur is None:
            return
        body = "\n".join(body_buf)
        d = directive_lines(body)
        cur.abstract_zh = d.get("问题抽象", "")
        struct = d.get("结构化", "")
        for key, attr in (("要求", "require"), ("已知", "given"),
                          ("约束/不确定性", "constraints")):
            m = re.search(r"`" + re.escape(key) + r"`＝(.*?)(?=\s*｜\s*`|$)", struct)
            if m:
                setattr(cur, attr, m.group(1).strip())
        # 本节的正文行是 `**数据形态**：…｜**场景**：…`，取**第一段**（`｜` 之前）判形态。
        dr = d.get("数据形态", "").split("｜")[0].split("|")[0]
        # **枚举值必须逐字命中**（T4）：本行必须以 `DATA_REGIMES` 里的某一项**开头**。
        # 不能写成「取第一个词」——枚举值自身就带括号（`无数据(纯机理/假设)`），
        # 按「第一个词」切会把它切成 `无数据`，于是**每个用它的题都被判非法**（那是判据错，不是数据错）。
        for cand in sorted(DATA_REGIMES, key=len, reverse=True):
            if dr.startswith(cand):
                cur.data_regime = cand
                rest = dr[len(cand):]
                cur.data_detail = re.sub(
                    r"^\s*[（(]\s*", "", rest).strip().rstrip("）)").strip()
                break
        cur.scenario = d.get("场景", "")
        st = d.get("状态", "").strip().strip("`")
        if st:
            cur.status = st
        cur.note = d.get("登记", "")
        out.append(cur)
        cur, body_buf = None, []

    for raw in text.split("\n"):
        ln = raw.rstrip()
        ms = SECTION.match(ln)
        if ms:
            close_row()
            close_section()
            cur = Annotation(year=int(ms.group(1)), problem=ms.group(2).upper(),
                             title=ms.group(3).strip())
            continue
        if cur is None:
            continue
        if TABLE_HEAD.match(ln) or TABLE_SEP.match(ln):
            close_row()
            continue
        if ln.startswith("|"):
            if row_buf:
                close_row()
            row_buf.append(ln)
            continue
        close_row()
        body_buf.append(ln)
    close_row()
    close_section()
    out.sort(key=lambda a: (a.year, a.problem))
    return out


def main(argv: list[str] | None = None) -> int:
    """手工探针：`python -m tools.papers.taxonomy <子命令>`（不是判据，不写任何产物）。"""
    ap = argparse.ArgumentParser(description="Task 6b 分类法/标注的顺手探针")
    ap.add_argument("cmd", choices=["files", "text", "taxonomy", "draft", "probe"])
    ap.add_argument("arg", nargs="?", default="")
    a = ap.parse_args(argv)
    if a.cmd == "files":
        fs = problem_files()
        print(f"题面 PDF {len(fs)} 份")
        for f in fs:
            print(f"  {f.year} {f.problem}  {f.rel}")
    elif a.cmd == "text":
        fs = [f for f in problem_files() if a.arg in f.path.name] or problem_files()
        for f in fs[:1]:
            t = extract_text(f.path)
            print(f"--- {f.rel}  行 {readable_lines(t)}  字符 {len(t)}")
            print(t)
    elif a.cmd == "taxonomy":
        tx = load_taxonomy()
        for lv in ("L1", "L2"):
            print(f"[{lv}] {len(tx[lv])} 条")
            for n, d in tx[lv].items():
                print(f"  {n}  —— {d}")
    elif a.cmd == "draft":
        ans = load_annotations()
        print(f"标注 {len(ans)} 条")
        for x in ans:
            print(f"  {x.key} [{x.status}] tags={len(x.labels)} ev={sum(len(v) for v in x.evidence_sentences)}"
                  f" regime={x.data_regime!r} title={x.title[:40]!r}")
    elif a.cmd == "probe":
        for f in problem_files():
            t = extract_text(f.path)
            nt, nf = text_op_counts(f.path)
            print(f"{f.year} {f.problem} lines={readable_lines(t):4d} chars={len(t):6d} "
                  f"textops={nt:5d} fills={nf:5d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
