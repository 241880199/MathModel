"""题型标注的判据（Task 6b 阶段 1）：T1–T8。

**被测产物**：`corpus/papers/PROBLEM_TYPES.md`（67 题的标注；**2026-09-26 由
`tests/papers/recon/PROBLEM_TYPES-draft.md` 原样转正**，见 `recon/types-recon.txt` 编者按）、
`tools/papers/vocab/problem_types.txt`（受控分类法）。
**被测实现**：`tools/papers/taxonomy.py`（分类法加载、标注解析、题面抽取）。

> **措辞残留（已知）**：本文件下面若干条消息里仍写着「草案」——它们指的是**标注文件自己
> 写下的口径与撰写纪律**（头部第 2 条的归一化步骤、引文里的强调标记等），转正时**正文一字未改**，
> 故那些话仍然成立；本轮授权只到「路径/回归所需」，不为此重写全部消息。
**这一轮不产出任何 `corpus/` 正式产物**——配对表与 `TAGS.md` 的 `problem_type` 栏是**阶段 2** 的事。

## 判据总表（**每一栏的参照是什么、为什么独立**）

| # | 判据 | 参照（独立的东西） |
| :--- | :--- | :--- |
| **T1** | 覆盖**双边等式**：标注 ↔ 磁盘题面 PDF **双射**；n == 磁盘题面数 == 11 年 × 6 题 + 2023 Z | **磁盘**（本脚本自己 `rglob` + 自己的文件名正则，**不 import `taxonomy.problem_files`**） |
| **T2** | **支撑句可定位**：每条引文必须是该题**题面抽取文本**格式归一化后的子串；且**每个标签行至少一条引文** | **题面原件**（本脚本自己调 `pdftotext`、自己实现归一化）；另用**严口径**再算一遍并登记差额 |
| **T3** | 分类法 ≠ 词表：任一 L1/L2 的**整名与成分**都不得与 `models.txt` 的词条/变体**相等** | `tools/papers/vocab/models.txt`（本脚本独立读） |
| **T4** | 标签合法（L1/L2 逐字命中分类法）+ `核心`/`附带` 标记齐全 + `data_regime` ∈ 受控枚举 + 其他字段非空 | `problem_types.txt`（独立读）+ 受控枚举常量 |
| **T5** | 三态与下界：每题 **≥1 `核心`**；只有 `附带` 的题必须给理由；**「读不出」集合 == 独立重算的集合** | **原件**（两条独立探针：抽取文本的行数 / 内容流里的文本操作符数） |
| **T6** | 与 Task 6 一致：标注的 `(year, problem)` ↔ `TAGS.md` 一层行**逐题对得上** | **Task 6 的入库产物**（`corpus/papers/TAGS.md` 与 `reports/ids-report.txt`，**读回，不重算**） |
| **T7** | `abstract_zh` 非空且**互异**（逐句去重） | 无（唯一性断言） |
| **T8** | **解析器互校**：`taxonomy.load_annotations` 与本脚本的独立解析**逐字段相等** | 本脚本的独立实现（正则另写一份） |

## 三件「判据自己会不会假绿」的事（照 `verify_ids.py` 的现行范式）

1. **不读「自称」、只读「产物」**：标签/引文/字段一律**从草案文本重新解析**（本脚本自己那份正则），
   题面文本一律**从原件重抽**，`TAGS.md`/`ids-report.txt` 一律**读回**。
   唯一一处读实现自报值的是 **T8**，而它本身就是「与独立解析逐字段相等」这条断言。
2. **双边等式**：T1（标注 ↔ 磁盘）、T3（分类法 ↔ 词表）、T5（读不出 ↔ 独立重算）、
   T6（2025 题号集合 ↔ `TAGS.md`）、T7（互异）都是 `A == B`，不是 `A >= 1`。
3. **不加分项判据的「上界洗白」**：本题语料实测只有 **1 道**「读不出」，而它**必须**被
   独立重算集合逐字对上——「标了读不出而题面其实可读」会立刻红（M9）。

## `--limit N` 的口径（**与 `verify_ids.py` 不同，必须说清**）

* **只有 T2 是限样本的**：定位置信要逐份重抽 67 份题面文本，是唯一慢的一步；
  故 `--limit N` 下只对**样本（前 N 份 ∪ 见证集 `FOCUS`）**查 T2。
* **其余判据一律全量**：T1/T3/T4/T5/T6/T7/T8 都不需要重抽题面（T5 的两条探针很便宜），
  全量跑才能让「少标一题」「分类法撞词表」这类变异在限样本跑里也红。
* 因此：限样本跑的 `RESULT` 行会**逐字写出**「T2 是样本口径、其余是全量」，
  免得读者把 `RESULT: PASS` 当成「67 题都验过了」。
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

# 标注的落点。2026-09-26 用户过闸门后由 `recon/PROBLEM_TYPES-draft.md` 转正到
# `corpus/papers/PROBLEM_TYPES.md`（`git mv`，语义一字未改）；本脚本**只跟路径**，
# T1–T8 的口径一个字都没放宽（转正后逐条重跑全绿 = 回归判据 R-1）。
ANNOTATIONS = "corpus/papers/PROBLEM_TYPES.md"
TAXONOMY = "tools/papers/vocab/problem_types.txt"
MODELS = "tools/papers/vocab/models.txt"
TAGS = "corpus/papers/TAGS.md"
IDS_REPORT = "tests/papers/reports/ids-report.txt"
PROBLEM_DIR = "corpus/官方原题"

# `--limit` 的见证集（**逐条给出为什么**）。**不并入取样是不行的**：排序序里靠后的关键样本
# `--limit 3` 取不到，判据的变异演示会在看不见它的集合上「绿着通过」（`report.pick_sample` 的注释即此）。
#
#   2020_MCM_Problem_A  **唯一**一道「读不出」的题（T5 的三态、探针阈值、例外登记都指着它）。
#   2025_MCM_Problem_A  2025 样板的第 1 题：引文里**同时**有 `…` 省略标记、`**强调**` 与项目符号，
#                       T2 三条归一化步骤的见证。
#   2025_MCM_Problem_D  T6 的见证：它同时是 `TAGS.md` 里题号 D（4 篇）与标注里 2025 D 的交点。
#                      **注意文件名是 `2025_ICM_Problem_D`**（D–F 属 ICM）——第一版写成 `…_MCM_…`，
#                      取样里**静默少了这一份**（`pick_sample` 按词干匹配，不匹配就不并入）。
#   2023_ICM_Problem_Z  「第 67 道」这个处置的见证（T1 的 11×6+1 口径）。
#   2024_ICM_Problem_F  T2 的**分页断裂**见证：它的引文跨越「页脚 + 分页」，不可能整段命中。
#   2026_MCM_Problem_A  T2 的**行内连字符**见证：`time-to-` 跨行后被抽成 `time-toempty`。
FOCUS = ("2020_MCM_Problem_A", "2025_MCM_Problem_A", "2025_ICM_Problem_D",
         "2023_ICM_Problem_Z", "2024_ICM_Problem_F", "2026_MCM_Problem_A")

# 受控枚举（**逐字**取自任务书 §一 第 5 条）。与 `taxonomy.DATA_REGIMES` 各写一份：
# 那份是**实现**、这份是**参照**，实现改宽了这里不跟着变、会红。
V_REGIMES = ("无数据(纯机理/假设)", "时序", "截面", "面板", "空间/地理", "网络",
             "文本/文献", "混合")
V_MARKS = ("核心", "附带")
V_STATUS = ("标定", "读不出")

# 「件里没有文本层」的两条独立探针的阈值。**都是实测空档，不是拍的整数**：
#   探针一（抽取文本的非空行数）：只有 2020 A 落在 4 以下（**2** 行），次低是 2016 A / 2017 B 的 **5** 行；
#   探针二（内容流的文本操作符数）：只有 2020 A 落在 50 以下（**4** 个），次低是 2017 A 的 **102** 个。
# 两条都取「最低者」与「次低者」之间的空档里，且**必须同时成立**才算读不出。
V_MIN_LINES = 4
V_MIN_TEXTOPS = 50
# 探针二的计数口径：`BT`（begin-text）、`Tj`（show text）、`TJ`（show text array）。
V_TEXTOP = re.compile(rb"(?<![A-Za-z])(BT|Tj|TJ)(?![A-Za-z])")

# ---- 参照侧的独立实现（**不 import 被测模块的对应函数**）------------------------
# 文件名 → `(年, 题号)`。年与题号一律取自**文件名**（机器事实），不从题面任何一行文字里推。
V_PDF_NAME = re.compile(r"^(\d{4})_(?:MCM|ICM)_Problem_([A-Z])\.pdf$")
V_SECTION = re.compile(r"^###\s+(\d{4})\s+([A-Z])\s*(?:—|-{1,2}\s*)?(.*)$")
V_ROW = re.compile(r"^\|\s*(?:`(核心|附带)`\s*)?\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|\s*$")
V_HEAD = re.compile(r"^\|\s*L1 · L2\s*\|\s*支撑句\s*\|$")
V_SEP = re.compile(r"^\|(?:\s*:?-{2,}:?\s*\|)+$")
V_QUOTED = re.compile(r'"([^"]+)"')
V_LABEL_SPLIT = " · "
V_TAXLINE = re.compile(r"^(L1|L2) \| ([^|]+?) \| (.+)$")
V_TAGS_ROW = re.compile(r"^(P\d{4}-([A-F])-\d{2,}) \| (\d{4}) \| ([A-F]) \|")
V_IDS_I8 = re.compile(r"^I8=(OK|FAIL)$", re.M)
V_IDS_MISMATCH = re.compile(r"不符 (\d+) 份")
V_IDS_UNREAD = re.compile(r"有但读不出 (\d+) 份")
LIST_MARK = re.compile(r"[•●○◦‣▪▫∙]")
QUOTE_FOLD = str.maketrans({c: '"' for c in "'’‘‛′\"“”‟″"})
ESC = re.compile(r"[*`]")


def v_norm(s: str, quote: bool = False) -> str:
    """**逐字重写**一份归一化（不调用 `taxonomy.normalize_*`）。口径与草案头部第 2 条一致：
    行尾归一 → 去项目符号 → 空白折叠 → 引号折叠 → 大小写折叠；引文侧另去强调标记。"""
    s = s.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")
    if quote:
        s = ESC.sub("", s)
    s = LIST_MARK.sub(" ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.translate(QUOTE_FOLD).casefold()


def v_norm_strict(s: str) -> str:
    """**严口径**：只做行尾归一 + 空白折叠 + 大小写折叠（**不去**项目符号、**不折**引号、**不去**强调标记）。"""
    s = s.replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")
    return re.sub(r"\s+", " ", s).strip().casefold()


def v_extract(pdf: Path) -> str:
    """**本脚本自己抽题面**（`pdftotext -enc UTF-8 <pdf> -`），不调 `taxonomy.extract_text`。"""
    import subprocess
    r = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"pdftotext 非零退出（{r.returncode}）：{pdf.name}")
    return r.stdout.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n").replace("\x0c", "\n")


def v_textops(pdf: Path) -> int:
    """探针二：内容流里 `BT|Tj|TJ` 的个数（**不看抽取器**，直接数操作符）。"""
    import fitz
    n = 0
    with fitz.open(pdf) as doc:
        for page in doc:
            n += len(V_TEXTOP.findall(page.read_contents()))
    return n


def v_problem_files() -> list[tuple[int, str, Path]]:
    """磁盘上的题面 PDF（按 `(年, 题号)` 排序）。**fail-closed**：目录空/命名不合约定→抛。"""
    root = ROOT / PROBLEM_DIR
    if not root.is_dir():
        raise FileNotFoundError(f"官方原题目录不存在：{PROBLEM_DIR}")
    out, bad = [], []
    for p in sorted(root.rglob("*.pdf")):
        m = V_PDF_NAME.match(p.name)
        if not m:
            bad.append(p.name)
            continue
        out.append((int(m.group(1)), m.group(2), p))
    if bad:
        raise ValueError(f"官方原题目录里有不合命名约定的 PDF：{bad}")
    if not out:
        raise FileNotFoundError("官方原题目录下没有题面 PDF")
    return sorted(out, key=lambda t: (t[0], t[1]))


def v_load_models() -> list[tuple[str, tuple[str, ...]]]:
    """词表 → `[(规范词, (变体…)), …]`（**独立读**，不 import `vocab.load`）。"""
    out = []
    for ln in (ROOT / MODELS).read_bytes().decode("utf-8").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        out.append((parts[0], tuple(x for x in parts if x)))
    if not out:
        raise ValueError("词表是空的")
    return out


def v_load_taxonomy() -> dict[str, dict[str, str]]:
    """分类法 → `{"L1": {名: 定义}, "L2": {...}}`（**独立读**）。"""
    out: dict[str, dict[str, str]] = {"L1": {}, "L2": {}}
    for ln in (ROOT / TAXONOMY).read_bytes().decode("utf-8").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        m = V_TAXLINE.match(s)
        if not m:
            raise ValueError(f"分类法行不合式：{ln!r}")
        out[m.group(1)][m.group(2).strip()] = m.group(3).strip()
    return out


def v_name_parts(name: str) -> list[str]:
    """标签名 → 去编号后的**整名**与 `/`、`、`、括号拆出的**成分**（T3 两个都要判）。"""
    whole = re.sub(r"^\d+(?:\.\d+)?\s+", "", name).strip()
    parts = [whole]
    for piece in re.split(r"[/、()（）]", whole):
        piece = piece.strip()
        if piece and piece not in parts:
            parts.append(piece)
    return parts


def v_parse_draft() -> list[dict]:
    """**本脚本自己解析草案**（与 `taxonomy.load_annotations` 各写一份，T8 逐字段互校）。"""
    text = (ROOT / ANNOTATIONS).read_bytes().decode("utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    out: list[dict] = []
    cur: dict | None = None
    body: list[str] = []
    row: list[str] = []

    def close_row() -> None:
        if cur is None or not row:
            row.clear()
            return
        ln = row[0]
        row.clear()
        m = V_ROW.match(ln)
        if not m:
            raise ValueError(f"{cur['year']} {cur['problem']}: 标签行不合式：{ln!r}")
        mark, label, cell = m.group(1), m.group(2).strip(), m.group(3)
        if mark not in V_MARKS:
            raise ValueError(f"{cur['year']} {cur['problem']}: 标签 {label!r} 缺标记")
        if V_LABEL_SPLIT not in label:
            raise ValueError(f"{cur['year']} {cur['problem']}: 标签 {label!r} 不含 ` · `")
        l1, l2 = [x.strip() for x in label.split(V_LABEL_SPLIT, 1)]
        cur["labels"].append((l1, l2, mark))
        cur["evidence"].append([q.strip() for q in V_QUOTED.findall(cell)])

    def close_section() -> None:
        nonlocal cur, body
        if cur is None:
            return
        blob = "\n".join(body)
        cur["raw_body"] = blob
        d: dict[str, str] = {}
        for m in re.finditer(r"^\*\*(.+?)\*\*：(.*)$", blob.replace("｜**", "\n**"), re.M):
            d.setdefault(m.group(1).strip(), m.group(2).strip())
        cur["abstract"] = d.get("问题抽象", "")
        struct = d.get("结构化", "")
        for key, attr in (("要求", "require"), ("已知", "given"),
                          ("约束/不确定性", "constraints")):
            m = re.search(r"`" + re.escape(key) + r"`＝(.*?)(?=\s*｜\s*`|$)", struct)
            cur[attr] = m.group(1).strip() if m else ""
        dr = d.get("数据形态", "").split("｜")[0].split("|")[0]
        cur["regime_raw"] = dr
        cur["regime"] = next((c for c in sorted(V_REGIMES, key=len, reverse=True)
                              if dr.startswith(c)), "")
        cur["scenario"] = d.get("场景", "")
        st = d.get("状态", "").strip().strip("`")
        cur["status"] = st or "标定"
        cur["note"] = d.get("登记", "")
        out.append(cur)
        cur, body = None, []

    for raw in text.split("\n"):
        ln = raw.rstrip()
        ms = V_SECTION.match(ln)
        if ms:
            close_row()
            close_section()
            cur = {"year": int(ms.group(1)), "problem": ms.group(2), "title": ms.group(3).strip(),
                   "labels": [], "evidence": []}
            continue
        if cur is None:
            continue
        if V_HEAD.match(ln) or V_SEP.match(ln):
            close_row()
            continue
        if ln.startswith("|"):
            if row:
                close_row()
            row.append(ln)
            continue
        close_row()
        body.append(ln)
    close_row()
    close_section()
    out.sort(key=lambda a: (a["year"], a["problem"]))
    return out


def checks(lines: list[str], limit: int = 0, meta: dict | None = None,
           out: Path | None = None, report=None) -> bool:
    """判据主体。**被测模块的 import 放在函数体内**（照 `verify_ids.py`）。"""
    from tools.papers import taxonomy as tx_mod
    from tools.papers import report as rep

    files = v_problem_files()
    pdfs = [p for _y, _l, p in files]
    sample = rep.pick_sample(pdfs, limit, FOCUS)
    sample_keys = {(y, l) for y, l, p in files if p in set(sample)}
    if meta is not None:
        meta["n_sample"], meta["n_all"] = len(sample), len(pdfs)

    anns = v_parse_draft()                   # 参照侧：本脚本自己的解析
    by_key = {(a["year"], a["problem"]): a for a in anns}
    tax = v_load_taxonomy()
    terms = v_load_models()
    tx = tx_mod.load_taxonomy()

    lines.append(
        f"题型标注判据 T1–T8 · **限样本 {len(sample)}/{len(pdfs)} 份**"
        f"（--limit {limit} + 见证集 {'/'.join(FOCUS)}）——**只有 T2 是样本口径，其余全量**"
        if limit > 0 else f"题型标注判据 T1–T8 · 全量 {len(pdfs)} 份题面")
    if limit > 0:
        lines.append(f"  取样：{' '.join(p.stem for p in sample)}")
        lines.append(
            f"  ! 这是**限样本跑**，不是放行依据；放行证据是 "
            f"{rep.rel(rep.release_path('types'))}。")
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

    # ==================== T1：覆盖的双边等式 ==============================
    disk = {(y, l) for y, l, _p in files}
    ann_keys = {(a["year"], a["problem"]) for a in anns}
    dup = [k for k, n in Counter((a["year"], a["problem"]) for a in anns).items() if n > 1]
    per_year: dict[int, list[str]] = defaultdict(list)
    for y, l in disk:
        per_year[y].append(l)
    years = sorted(per_year)
    extra = {y: sorted(set(v) - set("ABCDEF")) for y, v in per_year.items()
             if set(v) - set("ABCDEF")}
    missing = {y: sorted(set("ABCDEF") - set(v)) for y, v in per_year.items()
               if set("ABCDEF") - set(v)}
    n_expect = len(years) * 6 + sum(len(v) for v in extra.values())
    add("T1", not dup and ann_keys == disk and len(anns) == len(files) == n_expect,
        ([] if not dup else [f"重复的 (年, 题号)：{dup}"]) + [
        f"标注 **{len(anns)}** 条 == 磁盘题面 PDF **{len(files)}** 份 == "
        f"{len(years)} 年 × 6 题 + 附加题 {sum(len(v) for v in extra.values())} = {n_expect}"
        f"（**双边等式**：`n_annotations == 实际题面文件数`）",
        f"只在标注不在磁盘 {sorted(ann_keys - disk) or '无'} · 只在磁盘不在标注 "
        f"{sorted(disk - ann_keys) or '无'}（**两边都要空**）",
        f"逐年题号：{ {y: ''.join(sorted(per_year[y])) for y in years} }",
        f"**超出 A–F 的附加题**：{extra or '无'}——这就是 `2023 ICM Problem Z` 的处置："
        f"**算第 67 道并标注**（处置理由写在草案 §例外登记 ②）。",
        f"**每一年都必须齐 A–F**：{missing or '无缺'}（缺一年一题就红；上界不设，"
        f"因为『11 年 × 6 题』是任务书给死的口径）",
    ])

    # ==================== T2：支撑句可定位（**核心判据**）==================
    n_span = n_strict = 0
    n_cell = n_ellipsis = 0
    bad: list[str] = []
    empty_row: list[str] = []
    strict_only: list[str] = []
    needs_quote, needs_esc, needs_bullet, needs_other = 0, 0, 0, 0
    checked = 0
    for a in anns:
        key = (a["year"], a["problem"])
        if a["status"] != "标定":
            continue
        if limit > 0 and key not in sample_keys:
            continue
        checked += 1
        pdf = next(p for y, l, p in files if (y, l) == key)
        text = v_extract(pdf)
        hay, hay_s = v_norm(text), v_norm_strict(text)
        # 归因用的三个中间态（**只加一步**，用于说清严口径差额到底靠哪一步救回来）
        hay_q = v_norm_strict(text).translate(QUOTE_FOLD)          # 只折引号
        hay_b = v_norm_strict(LIST_MARK.sub(" ", text))             # 只去项目符号
        for (l1, l2, _m), spans in zip(a["labels"], a["evidence"]):
            if not spans:
                empty_row.append(f"{key[0]} {key[1]} · {l1} · {l2}")
                continue
            for sp in spans:
                n_cell += 1
                segs = [x for x in re.split(r"…+", sp) if x.strip()]
                if len(segs) > 1:
                    n_ellipsis += 1
                for seg in segs:
                    n_span += 1
                    q = v_norm(seg, quote=True)
                    if q not in hay:
                        bad.append(f"{key[0]} {key[1]} · {l1} · {l2}：引文定位失败：{seg[:100]!r}")
                        continue
                    if q in hay_s:
                        n_strict += 1
                    else:
                        strict_only.append(f"{key[0]} {key[1]} · {l1} · {l2}：{seg[:70]!r}")
                        # 归因：严口径下靠**最少哪一步**才能救回来。**先测最小的一步**
                        # （只去强调标记 → 再去引号 → 再去项目符号），否则会把「两步都要」
                        # 的条目算到第一步头上（第一版就是这样，把 3 条项目符号算成了引号）。
                        plain = ESC.sub("", seg)
                        if v_norm_strict(plain) in hay_s:
                            needs_esc += 1
                        elif v_norm_strict(plain).translate(QUOTE_FOLD) in hay_q:
                            needs_quote += 1
                        elif v_norm_strict(LIST_MARK.sub(" ", plain)) in hay_b:
                            needs_bullet += 1
                        else:
                            needs_other += 1
    add("T2", not bad and not empty_row and n_span > 0,
        bad + ([f"**有标签行没有引文**：{empty_row}"] if empty_row else []) + [
        f"**逐条可定位**：**{n_span}** 条片段（本次检查 {checked} 道标定题；"
        f"全部 {len(anns)} 条标注里 {sum(1 for a in anns if a['status'] == '标定')} 道为标定）；"
        f"行内引文段共 {n_cell} 段，其中 {n_ellipsis} 段用了 `…` 省略标记（照 2025 样板的写法），"
        f"拆开后共 {n_span} 条待定位片段——**定位失败 {len(bad)} 条**（要求 0）",
        f"口径（草案头部第 2 条，逐字重现在本脚本的 `v_norm`）：行尾归一 → 去项目符号 → "
        f"空白折叠 → 引号折叠 → 大小写折叠；引文侧另去 `*`/反引号（**那是草案自己加的强调标记**）",
        f"**严口径对照**（只做行尾归一 + 空白折叠 + 大小写折叠）：命中 {n_strict}/{n_span}；"
        f"差额 **{len(strict_only)}** 条逐条列在下面。差额的**归因**（各自只差一步）："
        f"**{needs_esc}** 条只需**去强调标记**（`*` 是**草案自己加的**字符）、"
        f"**{needs_quote}** 条还要**折引号**（题面用的是弯引号 `’`/`“`、草案引文里写的是直引号）、"
        f"**{needs_bullet}** 条还要**去项目符号**（题面把话排成了 `•` 列举）、"
        f"**{needs_other}** 条落在这三步之外。"
        f"注意这三类**都不是「用词不同」**：它们只动排版与字形，"
        f"**改一个词**就会被 T2 抓住（变异 M1 实测）。",
        "**这一步不可能让「编造的句子」命中**：它只动排版与字形，不动任何一个词。"
        "本判据的靶子是**编造的引文**（本项目栽过「证据里不成立的语料断言」）；"
        "变异 M1（把一条引文换成题面里没有的句子）实测会红。",
        "**边界（必须同读）**：它验证的是「引文在**该题**题面里找得到」，"
        "**不是**「这句话支持这个标签」——后者是判断，不在本任务范围。",
    ] + [f"    （严口径差额）{x}" for x in strict_only])

    # ==================== T3：分类法 ≠ 词表 ===============================
    vocab: dict[str, str] = {}
    for canon, variants in terms:
        for v in variants:
            vocab.setdefault(re.sub(r"\s+", "", v).casefold(), canon)
    used_names = [n for a in anns for n in (x for lab in a["labels"] for x in lab[:2])]
    coll, near = [], []
    # **两处都要判**：① 分类法**条目**（`problem_types.txt` 里的一行就是一条可用的标签名）；
    # ② 标注里**实际用到的**标签。只判前者会漏掉「分类法干净、但标注里手写了一个词表词」
    # （变异 M2b 实测就是这么漏过去的）——而那正是「题型 → 模型」退化成同义反复的形态。
    checked_names = [("分类法条目", level, name) for level in ("L1", "L2")
                     for name in tax[level]]
    checked_names += [("标注里的标签", f"L{1}", l1) for a in anns for l1, _l2, _m in a["labels"]]
    checked_names += [("标注里的标签", "L2", l2) for a in anns for _l1, l2, _m in a["labels"]]
    for where, level, name in checked_names:
        for part in v_name_parts(name):
            p = re.sub(r"\s+", "", part).casefold()
            if p in vocab:
                coll.append(f"{where} {level} {name!r} 的成分 {part!r} == 词表词条 {vocab[p]!r}")
            for k, canon in vocab.items():
                if k != p and len(p) >= 2 and p in k:
                    near.append(f"{where} {level} {name!r} 的 {part!r} ⊂词表 {canon!r}")
                elif k != p and len(p) >= 2 and k in p:
                    near.append(f"{where} {level} {name!r} 的 {part!r} ⊃词表 {canon!r}")
    # 自建分类法**必须**与词表不相交；`near` 只是报告量（子串关系不等于同义反复）
    add("T3", not coll and len(tax["L1"]) > 0 and len(tax["L2"]) > 0, coll or [
        f"**两处都判、都无一相等**：① 分类法的 **{len(tax['L1'])} 个 L1 / {len(tax['L2'])} 个 L2** "
        f"条目；② 标注里**实际用到**的 **{len(set(used_names))}** 个不同标签名"
        f"（`used_names` 由草案重新解析得到）——对照词表 **{len(terms)} 个词条 / "
        f"{sum(len(v) for _c, v in terms)} 个变体**（整名与按 `/`、`、`、括号拆出的成分都判）",
        f"判「相等」而不判「包含」的理由：包含会把 **`1 预测` ⊂ `灰色预测`** 这类**正确命名**判成违规"
        f"（那是模型的专名，不是题型的名字）；而本判据要拦的**同义反复**是"
        f"「**标签名就是模型名**」——那一定表现为相等。",
        f"**近邻（含子串但不等）{len(set(near))} 条**，逐条列出（**不藏**）：",
    ] + sorted(set(near)))
    # 词表的**读取路径**独立于分类法：正则与拆分各写一份，实现改宽这里不跟着变。

    # ==================== T4：标签合法 + 字段齐全 ==========================
    bad_lab: list[str] = []
    used = Counter()
    for a in anns:
        for l1, l2, mark in a["labels"]:
            used[l2] += 1
            if l1 not in tax["L1"]:
                bad_lab.append(f"{a['year']} {a['problem']}：L1 {l1!r} 不在分类法里")
            if l2 not in tax["L2"]:
                bad_lab.append(f"{a['year']} {a['problem']}：L2 {l2!r} 不在分类法里")
            if mark not in V_MARKS:
                bad_lab.append(f"{a['year']} {a['problem']}：标签 {l2!r} 的标记 {mark!r} 非法")
        if a["status"] == "标定" and a["regime"] not in V_REGIMES:
            bad_lab.append(f"{a['year']} {a['problem']}：数据形态 {a['regime_raw'][:40]!r} "
                           f"不命中受控枚举")
    per_prob = sorted(len(a["labels"]) for a in anns if a["status"] == "标定")
    add("T4", not bad_lab, bad_lab or [
        f"标签 **{sum(used.values())}** 个（去重 {len(used)} 个 L2）；**每题标签数** "
        f"最少 {per_prob[0]} 个、最多 {per_prob[-1]} 个、中位 {per_prob[len(per_prob) // 2]} 个"
        f"（**不设上限**，用户 2026-09-26 定案）；全部逐字命中分类法、标记齐全",
        f"**分类法使用分布**（L2 → 题数）：{dict(used.most_common())}",
        f"**本阶段零命中的条目**（登记在分类法文件末尾，判据每次重算并与它对账）："
        f"{sorted(set(tax['L2']) - set(used))}",
        f"数据形态分布：{dict(Counter(a['regime'] for a in anns).most_common())}"
        f"（空串那一个是 `2020 A` 的「读不出」，见 T5）",
    ])
    missing_f = [f"{a['year']} {a['problem']}：{k} 为空"
                 for a in anns if a["status"] == "标定"
                 for k, v in (("问题抽象", a["abstract"]), ("要求", a["require"]),
                              ("已知", a["given"]), ("约束/不确定性", a["constraints"]),
                              ("数据形态", a["regime"]), ("场景", a["scenario"])) if not v]
    add("T4-b", not missing_f, missing_f or [
        f"**字段齐全**（{sum(1 for a in anns if a['status'] == '标定')} 道标定题）："
        f"`问题抽象`/`要求`/`已知`/`约束-不确定性`/`数据形态`/`场景` 逐个非空",
        "「空着不写」也是一种静默——它会让下游以为「这题没有约束」而不是「没人填」。",
    ])

    # ==================== T5：三态与下界 =================================
    no_core = [f"{a['year']} {a['problem']}" for a in anns
               if a["status"] == "标定" and not any(m == "核心" for _l1, _l2, m in a["labels"])]
    only_inc = [a for a in anns if a["status"] == "标定" and a["labels"]
                and all(m == "附带" for _l1, _l2, m in a["labels"])]
    only_inc_noreason = [f"{a['year']} {a['problem']}" for a in only_inc if not a["note"]]
    add("T5", not no_core and not only_inc_noreason, [
        f"**每题至少一个 `核心`**：违反 {no_core or '无'}（66 道标定题，"
        f"`核心` 合计 {sum(1 for a in anns for _l1, _l2, m in a['labels'] if m == '核心')}、"
        f"`附带` 合计 {sum(1 for a in anns for _l1, _l2, m in a['labels'] if m == '附带')}）",
        f"**只有 `附带` 的题**：{len(only_inc)} 道，其中没给理由的 {only_inc_noreason or '无'}"
        f"（本语料上**这一路不触发**——它存在是为了「只能给出附带」的那种题**不许静默**）",
    ])
    # ---- 探针：独立重算「读不出」的集合 ----------------------------------
    probe: dict[tuple[int, str], tuple[int, int]] = {}
    unreadable = set()
    for y, l, p in files:
        text = v_extract(p)
        nl = sum(1 for x in text.split("\n") if x.strip())
        nt = v_textops(p)
        probe[(y, l)] = (nl, nt)
        if nl < V_MIN_LINES and nt < V_MIN_TEXTOPS:
            unreadable.add((y, l))
    declared = {(a["year"], a["problem"]) for a in anns if a["status"] == "读不出"}
    bad_status = [f"{a['year']} {a['problem']}：状态 {a['status']!r} 不在 {V_STATUS}"
                  for a in anns if a["status"] not in V_STATUS]
    noreason = [f"{y} {l}" for y, l in declared
                if not by_key[(y, l)]["note"]]
    cross = declared & unreadable
    add("T5-b", not bad_status and declared == unreadable and not noreason, bad_status + noreason + [
        f"**「读不出」集合的双边等式**：草案声明 {sorted(declared)} == 独立重算 "
        f"{sorted(unreadable)}（**两边都要空**）",
        f"两条**互相独立**的探针（阈值取在实测空档里，见模块头）："
        f"① 抽取文本的非空行数 < {V_MIN_LINES}；② 内容流文本操作符 `BT|Tj|TJ` < {V_MIN_TEXTOPS}。"
        f"**两条同时成立**才算读不出。实测全 67 份的这一对量：最低 {min(probe.values())}、"
        f"次低 {sorted(probe.values())[1]}（差一个数量级，不是「差不多」）",
        f"**fail-closed 的两个方向都守**：标了「读不出」但题面其实可读（会红，见 M9）；"
        f"或题面读不出却标成「标定」（草案里那道题的引文会定位失败，T2 也会红）",
        f"「读不出」的**处置**：不标标签、不写抽象、**不靠标题猜题意**（任务书 §四 第 7 条）。"
        f"它**不摊到别的题上**：T1 的双边等式仍按 {len(files)} 判，T5 首条只数「标定」的题。",
    ] + [f"    （探针明细）{y} {l}：行数 {probe[(y, l)][0]} · 操作符 {probe[(y, l)][1]}"
         for y, l in sorted(unreadable)])

    # ==================== T6：与 Task 6 一致 ==============================
    tags_p = ROOT / TAGS
    if not tags_p.is_file():
        raise FileNotFoundError(f"Task 6 的产物不在：{TAGS}")
    tags_txt = tags_p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    tags_rows = [m for m in (V_TAGS_ROW.match(ln) for ln in tags_txt.split("\n")) if m]
    if not tags_rows:
        raise ValueError(f"{TAGS} 里没有解析到一层行（参照存在而没解析出来 ⇒ 硬失败）")
    tags_per: dict[int, Counter] = defaultdict(Counter)
    for m in tags_rows:
        sid, sid_letter, year, letter = m.group(1), m.group(2), int(m.group(3)), m.group(4)
        tags_per[year][letter] += 1
        if sid[1:5] != str(year) or sid_letter != letter:
            raise ValueError(f"{TAGS} 的一层行自相矛盾：{m.group(0)[:40]!r}")
    rep_p = ROOT / IDS_REPORT
    if not rep_p.is_file():
        raise FileNotFoundError(f"Task 6 的放行证据不在：{IDS_REPORT}")
    ids_txt = rep_p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    i8 = V_IDS_I8.search(ids_txt)
    mm = V_IDS_MISMATCH.search(ids_txt)
    ur = V_IDS_UNREAD.search(ids_txt)
    t6_bad: list[str] = []
    if i8 is None or i8.group(1) != "OK":
        t6_bad.append(f"`{IDS_REPORT}` 里没有 `I8=OK`（Task 6 的「题目 ↔ 论文」结论不成立）")
    if mm is None or int(mm.group(1)) != 0:
        t6_bad.append(f"`{IDS_REPORT}` 的 I8 不符篇数 != 0：{mm.group(1) if mm else '读不出'}")
    if ur is None or int(ur.group(1)) != 0:
        t6_bad.append(f"`{IDS_REPORT}` 的「有栏但读不出」篇数 != 0：{ur.group(1) if ur else '读不出'}")
    for y in sorted(tags_per):
        a_set = {a["problem"] for a in anns if a["year"] == y}
        t_set = set(tags_per[y])
        if a_set != t_set:
            t6_bad.append(f"{y} 年：标注题号 {sorted(a_set)} ≠ `TAGS.md` 一层行里的题号 "
                          f"{sorted(t_set)}（**双边**：两边都要相等）")
    add("T6", not t6_bad, t6_bad or [
        f"**读回** `{TAGS}` 的一层行 **{len(tags_rows)}** 行（不重算），"
        f"覆盖年份 {sorted(tags_per)}（合计 {sum(sum(c.values()) for c in tags_per.values())} 篇）；"
        f"其中 2025 的题号分布 {dict(tags_per.get(2025, {}))}",
        f"**逐题对得上**：`TAGS.md` 覆盖到的每一年，标注的题号集合与它**相等**"
        f"（{sorted(tags_per)} 年全部相等）",
        f"**读回** `{IDS_REPORT}` 的 I8 结论：`I8={'OK' if i8 and i8.group(1) == 'OK' else '读不出'}`、"
        f"不符 {mm.group(1) if mm else '?'} 份、有栏读不出 {ur.group(1) if ur else '?'} 份"
        f"——即 Task 6 已建的「**目录题号 vs 论文自报题号**」结论（43/43 一致）**仍然成立**，"
        f"本判据**不复算**它。",
        f"**范围边界（必须同写）**：`TAGS.md` 只覆盖 **2025**（其余年份没有论文产物）⇒ "
        f"这条双边等式**只能对 2025 成立**；其余 5 个年份的题号只能靠 T1 走「磁盘题面文件」这一路。"
        f"**这不是「其余年份也验过了」**。",
    ])

    # ==================== T7：abstract 互异 ===============================
    abs_all = [a["abstract"] for a in anns if a["status"] == "标定"]
    dup_abs = [k for k, n in Counter(abs_all).items() if n > 1]
    add("T7", not dup_abs and all(abs_all), [
        f"**{len(abs_all)}** 道标定题各有一句 `问题抽象`，**逐句去重后仍 {len(set(abs_all))} 条**"
        f"（重复 {dup_abs or '无'}）",
        f"「读不出」的 {len(declared)} 道**不参与**这条（它没有抽象可写，已在 T5 单独登记）",
    ])

    # ==================== T8：解析器互校 ================================
    tx_anns = tx_mod.load_annotations()
    t8_bad: list[str] = []
    if len(tx_anns) != len(anns):
        t8_bad.append(f"`taxonomy.load_annotations` {len(tx_anns)} 条 vs 本脚本 {len(anns)} 条")
    else:
        for t_a, v_a in zip(tx_anns, anns):
            if (t_a.year, t_a.problem) != (v_a["year"], v_a["problem"]):
                t8_bad.append(f"顺序不一致：{t_a.key} vs {v_a['year']} {v_a['problem']}")
                continue
            pairs = [("abstract_zh", t_a.abstract_zh, v_a["abstract"]),
                     ("require", t_a.require, v_a["require"]),
                     ("given", t_a.given, v_a["given"]),
                     ("constraints", t_a.constraints, v_a["constraints"]),
                     ("data_regime", t_a.data_regime, v_a["regime"]),
                     ("scenario", t_a.scenario, v_a["scenario"]),
                     ("status", t_a.status, v_a["status"]),
                     ("title", t_a.title, v_a["title"]),
                     ("labels", t_a.labels, [tuple(x) for x in v_a["labels"]]),
                     ("evidence", [x for x in t_a.evidence_sentences],
                      [list(x) for x in v_a["evidence"]])]
            for name, x, y in pairs:
                if x != y:
                    t8_bad.append(f"{t_a.key} 的 {name} 两套解析不等：{str(x)[:60]!r} vs {str(y)[:60]!r}")
    add("T8", not t8_bad, t8_bad or [
        f"`taxonomy.load_annotations` 与**本脚本另写的一份解析**在 "
        f"{len(anns)} 条 × 10 个字段上**逐字段相等**",
        "**为什么要有这条**：判据若只信实现给的 dataclass，实现「解析成空表」时判据会对着空集报绿"
        "（本项目「判据在什么都没验的情况下报绿」家族的形态）。两套解析各写一份、互相夹住，"
        "实现被改窄/改宽时另一份不跟着变 ⇒ 立刻红（变异 M10 实测）。",
        f"另：`taxonomy.load_taxonomy()` 与 `v_load_taxonomy()` 的条目数 "
        f"L1 {len(tx['L1'])}/{len(tax['L1'])} · L2 {len(tx['L2'])}/{len(tax['L2'])}",
    ])

    # ---------------- 报告量 ----------------
    lines.append(f"  抽取探针（全 67 份）：最低 `(行数, 操作符)` = {min(probe.values())}、"
                 f"次低 = {sorted(probe.values())[1]}；阈值 = ({V_MIN_LINES}, {V_MIN_TEXTOPS})")
    lines.append(f"  标注规模：{len(anns)} 题 / {sum(used.values())} 个标签 / "
                 f"{n_span} 条片段（T2 样本内）")
    lines.append("=" * 78)
    lines.append(f"判据汇总：{'全部通过' if ok else '**有 FAIL**'}"
                 f"（所有差额逐条具名登记见上，**未解释为 0**）")
    return ok


def main() -> int:
    import argparse

    from tools.papers import report

    ap = argparse.ArgumentParser(
        description="题型标注判据 T1–T8（受控分类法 + 67 题标注草案）",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="只对**前 N 份题面 ∪ 见证集**查 T2（其余判据一律全量）。报告写到 "
             "tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/types-report.txt）；负数不接受。",
    )
    args = ap.parse_args()

    out, guard_msg = report.resolve_report("types", args.limit)
    pre = report.sha256_of(report.release_path("types")) if args.limit > 0 else ""

    meta: dict = {}
    lines = ["题型标注判据（T1–T8）· 官方题面 2016–2026"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out, report)
    except BaseException as e:            # noqa: BLE001 —— 任何异常都算 FAIL
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = report.recheck_target("types", args.limit, out)
    if msg2:
        lines.append(msg2)
    # **这一句不能省**：守卫消息只是往报告里写了 FAIL，不并进 ok 的话 RESULT 行照样 PASS。
    if guard_msg or msg2:
        ok = False

    lines.append("")
    lines.append(f"写入：{report.rel(out)}")
    if args.limit > 0:
        lines.append(
            f"  本文件是**限样本跑**（--limit {args.limit} + 见证集 {'/'.join(FOCUS)}）的报告，"
            f"**不入库、不是放行依据**；放行证据是 {report.rel(report.release_path('types'))}。"
            f"**只有 T2 是样本口径**，T1/T3–T8 是全量。")
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件。")

    text = "\n".join(lines) + "\n"
    if args.limit > 0:
        post = report.sha256_of(report.release_path("types"))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· {report.rel(report.release_path('types'))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    text += (f"\nRESULT: {'PASS' if ok else 'FAIL'}"
             f"{report.result_suffix('types', args.limit, meta, FOCUS)}\n")
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
