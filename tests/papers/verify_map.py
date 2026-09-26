"""`MODEL_MAP.md` 的判据（Task 6b 阶段 2b）：M-1…M-16。

**被测产物**：`corpus/papers/MODEL_MAP.md`（由 `tools/papers/model_map.py` 生成）。
**独立参照**（本脚本**各自另写一份解析**，不调 `taxonomy` / `index` / `model_map` / `coverage`
的解析函数）：

| 参照 | 提供什么 |
| :--- | :--- |
| `corpus/papers/PROBLEM_TYPES.md` | 题型 `(L1,L2)`、`核心/附带`、`data_regime` |
| `corpus/papers/TAGS.md`（Task 6 的产物） | `models` 命中、二层指针（词 + md + 页 + 片段）、**作者自写的 `keywords` 栏** |
| `tools/papers/vocab/growth_triage.txt` | 增长候选的**三态处置 + 类别 + 理由** |
| `tools/papers/vocab/body_triage.txt` | **正文扫描的跨篇复用 token** 的**三态处置 + 类别 + 理由**（**与上表同一套格式与规则**，收口轮新增；两表的**词形集合必须互斥**） |
| `tests/papers/reports/coverage-evidence.txt` | 匹配度的**机读证据**（与被测产物的第四节同源） |
| **git 对象库** | **增长前**的 `tools/papers/vocab/models.txt`（基线 blob，写死在 `BASELINE_MODELS_BLOB`） |

**被测实现** `tools/papers/model_map.py` **只在 M-8 里被调用**（拿它的输出与入库产物比字节）。

## 判据总表（每一栏的参照是什么、为什么独立）

| # | 判据 | 参照（独立的东西） |
| :--- | :--- | :--- |
| **M-1** | **解冻面（两阶段合并）**：`INDEX.md` / `PROVENANCE.md` / `TAGS.md` 的 blob vs 开工基准——`PROVENANCE.md` **逐字节不变**；`TAGS.md` **变了**；`INDEX.md` **变了、但只差「模型/算法」一栏**（逐行逐栏与基准比对，其余 10 栏逐字相同） | 开工基准（`recon/map-recon.txt` §0 登记）+ 基准里 `INDEX.md` 的**旧字节**（`git cat-file`） |
| **M-1-b** | **重放性**（全量跑才跑）：`index.build` 重跑到**不入库**目录 → 三份产物与入库的**逐字节相同** | 重跑出来的字节 vs 入库字节 |
| **M-2** | **覆盖双边等式**：逐题表的题数 == TAGS 一层出现过的 `(年, 题号)` 数 == **6**；逐题论文数之和 == **43** == TAGS 一层行数；**且**第二节表的每一行（论文数 / 对数 / 模型列 / 来源题）都能由**去重指针行的「所属桶」列**反推出来（两向） | `TAGS.md` 一层 + 产物自身（两张表互为参照） |
| **M-4** | **指针可落地**：每条**去重指针行**的 `md + 页 + 片段` == TAGS 二层那一条；且片段是该 md **在该页的整行逐字** | `TAGS.md` 二层 + **md 文件**（Task 3 产物） |
| **M-5** | **轴合法**：桶的 `(L1,L2)` ∈ `problem_types.txt` 且 ∉ `models.txt` 词条/变体；`data_regime` ∈ 受控枚举；**去重指针的桶号集合 == 第二节表的桶号集合** | 分类法 + 词表（各自独立读） |
| **M-6** | **边界可机读且为等式**：有论文的题 + 未配对的题 == 标注题数，且逐题具名清单两边对得上 | 标注文件（本脚本自己解析） |
| **M-7** | **无幻影**：指针行里每个 stable ID ∈ TAGS 一层；第二节每一行的**来源题**与「所属桶」反推出来的篇**两向一致**；第三节低置信条目逐条 ∈ TAGS 二层 | `TAGS.md` + 产物自身（结构自洽） |
| **M-8** | **重放一致性**：`model_map.build()` 重跑到不入库目录 → 与入库产物**逐字节相同** | 生成器输出 vs 入库字节 |
| **M-9** | **召回分母口径**：参照篇数 == TAGS 里 `keywords` 非空的篇数 == **42**；`P2025-C-17` **单列**为「参照不存在」（本脚本**自己去读那篇 md**，确认 `key.?words?` 零命中），与「参照存在但没解析出来」**分列**、两者互斥、并集 == 43 − 42 == 1 | `TAGS.md` 一层 + **md 文件** |
| **M-10** | **未解释为 0**：**独立重算**每篇「未被**基线**词表覆盖、且分流表判`模型`」的片集合 → 必须与产物/证据里的「未覆盖模型条目」**逐条两向相等**；每个未覆盖片（含判`场景`的）都要在分流表里有行、处置合法、理由非空。**两张同格式表（`growth_triage` / `body_triage`）按同一套规则判**；两表的**词形集合必须互斥** | `TAGS.md` 的 `keywords` 栏 + 两张分流表 + **git 基线词表** |
| **M-11** | **分流表可定位**：每一行的定位符成立——`kw:<sid>` ⇒ 词形在该篇 `keywords` **栏**里命中；`kwseg:<sid>` ⇒ 词形在该篇 md 的 **Keywords 段**（含续行）里命中；`body:<sid>@p<页>` ⇒ 词形在该篇 md 的**第 <页> 页**里命中（词边界口径）。`<sid>` 必须是 TAGS 一层的 ID。**形态照 T2（空白归一化后子串命中）** | `TAGS.md` + **md 文件** |
| **M-12** | **词表合法**：`models.txt` 相对**基线**（git blob）的**新增词形集合 == 两张分流表的 `处置=收录` 词形集合之并**（两向） | **git 基线 blob** + 两张分流表 |
| **M-13** | **去重后的两向等式 + 桶归属**（原 M-3 的新形态）：去重指针行的 `(篇, 模型)` 集合 ↔ TAGS 二层同名集合（两向）；**每行的「所属桶」集合 == 由标注（该篇题号的标签集合）+ 第二节桶表推出的桶集合**（逐行） | `TAGS.md` 二层 + 标注文件 + 第二节表 |
| **M-14** | **第四节与证据同源**：产物第四节的机读行 / 逐篇表 / 未覆盖清单 == `coverage-evidence.txt` 的同名键与清单 == **本脚本自己的独立重算**（三方相等；**本脚本不调 `coverage`**） | 证据文件 + 产物 + 独立重算 |
| **M-15** | **精确性**：把产物第四节报的精确性比值与低置信条数，跟**本脚本对 TAGS 二层指针的独立复核**（md + 页 + 片段三条同时成立）与 `x1` 集合对账；低置信**逐条单列且不为空** | `TAGS.md` 二层 + **md 文件** |
| **M-16** | **R1 真收口**：**默认路径** `load()` 下「追加即生效」的探针**真的会红**——在系统临时目录上把 `vocab.DEFAULT` 指过去，`load()`（**不带参数**）读 1 条 → 追加 1 行 → **同一进程内**再 `load()` 必须读到 2 条 | `tools/papers/vocab.py` 的行为（探针，不写任何入库文件） |

## 三件「判据自己会不会假绿」的事（照 `verify_ids.py` 的现行范式）

1. **不读「自称」、只读「产物」**：题型/模型/指针一律**从产物文本重新解析**（本脚本自己那份正则），
   md 一律**从磁盘重读**，开工基准一律**从 recon 登记读回**。唯一调用实现的地方是 M-8，
   而它判的就是「实现的输出 == 入库的字节」——两侧一份来自实现、一份来自磁盘，是**等式**不是自称。
2. **双边等式**：M-1（变/不变都要判）、M-2、M-13（两向）、M-4（对账）、M-6（和式 + 逐题）、
   M-7（两向）都是 `A == B`，不是 `A >= 1`。
3. **两个真正的独立参照在哪**（**这句话的强度要说准**）：M-13 的**桶归属那一半**两侧各有一份
   数据源——题型来自**标注文件**、桶表来自**产物**，两边**不同源**。而 M-13 的**配对相等那一半**
   两侧**同源于 `TAGS.md`**（配对表的指针行是 `model_map.py` 从 TAGS 的**二层**读回来的）：
   那是「**一份数据、两份解析器**」——它能抓住生成器漏抄/重抄，**抓不住两侧对 `TAGS.md`
   格式的共同误读**（要证「不共用抽取代码」的是解析器这一层，不是数据这一层）。
   ⇒ 判这条时**别高估它**。

## `--limit N`

本脚本的判据**全部是全量口径**：输入是两份文本产物（不是 43 份 PDF），全量检查不到几秒，
**没有**需要抽样的慢对象。故 `--limit N`**不缩样本**，它只做两件事：把报告写到不入库的
`reports-limited/`、并跳过需要重跑 43 份原件的 **M-1-b**。这条**逐字写进 RESULT 行**，
免得读的人把 `LIMITED` 当成「样本口径」（本项目栽过「限样本的绿冒充放行结论」）。
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

COLLECTION = "2025美赛O奖论文"
MAP = "corpus/papers/MODEL_MAP.md"
TAGS = "corpus/papers/TAGS.md"
ANNOTATIONS = "corpus/papers/PROBLEM_TYPES.md"
PROBLEM_TYPES = "tools/papers/vocab/problem_types.txt"
MODELS = "tools/papers/vocab/models.txt"
TRIAGE = "tools/papers/vocab/growth_triage.txt"
# **第二张同格式表**（收口轮新增）：正文扫描的「跨篇复用」token 的逐条处置。M-10/M-11/M-12
# 把它与 `growth_triage.txt` **按同一套规则**判（口径只有一处；见 `v_body_triage` 的注释），
# 并另判一条：**两表的词形集合必须互斥**（同一词形落两张表 = 两处口径的开端）。
BODY_TRIAGE = "tools/papers/vocab/body_triage.txt"
COV_EVIDENCE = "tests/papers/reports/coverage-evidence.txt"
RECON = "tests/papers/recon/map-recon.txt"
INDEX_PRODUCTS = ("corpus/papers/INDEX.md", "corpus/papers/TAGS.md",
                  "corpus/papers/PROVENANCE.md")
# **增长前**的 `tools/papers/vocab/models.txt`（开工当天实测登记的 blob）。M-10/M-12/M-14
# 要拿它当**基线**：`@增长前` 的召回与「词表新增」两个量都必须对着**增长前的字节**量。
# 从 **git 对象库**取（`git cat-file blob`），**不读工作树**（工作树上那份已经是增长后的）、
# 也**不**用「现行词表减去分流表收录行」反推（反推会让基线依赖本轮产物）。
BASELINE_MODELS_BLOB = "0ca91927d3ddafd91fe7bd4c79716a8093f7fad8"
# 作者 Keywords 段的两道探针（口径与 `coverage.py` 的 `taxonomy_v_keywords()` 相同，
# 但**本脚本另写一份**——判据侧的参照必须独立；`key.?words?` 那一道只用来判三态）。
V_KEYWORDS = re.compile(r"^[#>*_ \t]*(?:Key\s*words?|关键词)\s*[:：]\s*(.*?)[*_ \t]*$",
                        re.I | re.M)
V_ANY_KEYWORD = re.compile(r"key\s*words?", re.I)
V_KW_SEG_STOP = re.compile(
    r"^(#{1,6}\s|<!-- page|\d+(\.\d+)*\s|Problem\s+Chosen|Team\s+Control)", re.I)
# 片的拆法（**逐字复刻 `verify_ids.py` 的 I13**）。
V_PIECE_SEP = re.compile(r"[;,；，、|/]")
# 分流表一行：`词形 \t 处置 \t 类别 \t 理由`。
# `TAGS.md` 一层的空值哨兵（**ASCII `-`**；全角 `—` 不是它——本项目在这条上栽过两次）。
EMPTY_CELL = "-"
V_TRIAGE_LOC = re.compile(r"^(kw|kwseg):(P\d{4}-[A-F]-\d{2,})\s—\s(.*)$", re.S)
# **第三个定位符模式**（只出现在正文扫描那张表里）：`body:<稳定 ID>@p<页> — …`。
V_BODY_LOC = re.compile(r"^body:(P\d{4}-[A-F]-\d{2,})@p(\d+)\s—\s(.*)$", re.S)
# 产物第四节的机读行（键=值，` · ` 分隔）。
V_COV_LINE = re.compile(r"^> 匹配度：(.+)$")
V_COV_KV = re.compile(r"([^=·]+?)=([^·]*)")
# 第四节逐篇表行：`| P2025-A-01（2025 A） | 有参照 | 6 | 2 | 0 | 0 | 2/2 | 2/2 |`
V_COV_PAPER = re.compile(
    r"^\| (P\d{4}-[A-F]-\d{2,})（\d{4} [A-F]） \| ([^|]+?) \| (\d+) \| (\d+) \| (\d+) \|"
    r" (\d+) \| ([^|]+?) \| ([^|]+?) \|$")
# 第四节未覆盖表行：`| P2025-A-05 | `Depth Estimation` | 不收 | … |`
V_COV_UNCOV = re.compile(r"^\| (P\d{4}-[A-F]-\d{2,}) \| `(.+?)` \| (收录|不收|待定) \|")
# 证据文件的键=值行。
V_EV_KV = re.compile(r"^([^=\t#]+)=(.+)$")
# 受控枚举与标记（**逐字**取自任务书 §一 第 5/2 条）。与 `taxonomy.DATA_REGIMES` /
# `taxonomy.MARKS` 各写一份：那份是**实现**、这份是**参照**，实现改宽了这里不跟着变、会红。
V_REGIMES = ("无数据(纯机理/假设)", "时序", "截面", "面板", "空间/地理", "网络",
             "文本/文献", "混合")
V_MARKS = ("核心", "附带")
# `--limit` 不取样（见模块 docstring）⇒ 没有见证集。留着这个常量是为了让 RESULT 行
# 与别的脚本**同形**（`report.result_suffix` 的签名要它）。
FOCUS: tuple[str, ...] = ()

# ---- 参照侧的独立实现（**不 import 被测模块的对应函数**）------------------------
V_L1_ROW = re.compile(r"^(P\d{4}-[A-F]-\d{2,}) \| (\d{4}) \| ([A-F]) \| ")
V_L2_HEAD = re.compile(r"^### (P\d{4}-[A-F]-\d{2,}) · 题 ([A-F]) · ")
V_L2_MD = re.compile(r"^md: (.+)$")
V_L3_COUNT = re.compile(r"^本层 \*\*(\d+)\*\* 篇")
V_PAGE_ANCHOR = re.compile(r"^<!-- page (\d+) -->$")
V_ANNOT_SECTION = re.compile(r"^###\s+(\d{4})\s+([A-Z])\s*(?:—|-{1,2}\s*)?(.*)$")
# 标注文件里的「数据形态」指令行（M-13 判桶归属要它；**自己一份正则**）。
V_ANNOT_REGIME_LINE = re.compile(r"^\*\*数据形态\*\*：(.+)$")
V_ANNOT_ROW = re.compile(r"^\|\s*(?:`(核心|附带)`\s*)?\*\*(.+?)\*\*\s*\|")
V_TAXLINE = re.compile(r"^(L1|L2)\s*\|\s*([^|]+?)\s*\|")
TAGS_SEP = "; "
# MODEL_MAP 的解析式（**与生成器各写一份**）。
V_M_PROBLEM = re.compile(r"^### (\d{4}) ([A-F]) — ")
V_M_NPAPERS = re.compile(r"^- 论文数：(\d+)$")
V_M_BUCKET_ID = re.compile(r"^#### (\d+)\. ")
V_M_COVER = re.compile(
    r"覆盖边界：标注题数=(\d+)\s*·\s*有论文的题=(\d+)\s*·\s*未配对的题=(\d+)\s*·\s*"
    r"覆盖年份=(.*?)\s*·\s*未配对逐题=(.*)$")
V_M_ZERO = re.compile(r"条数=(\d+) · TAGS第三层=(\d+) · 逐篇=(.*)$")
V_M_LOW = re.compile(r"条数=(\d+) · 总指针=(\d+) · 口径=")
# 开工基准的行：`    <路径>    <40 位 blob>`。
V_BASELINE_ROW = re.compile(r"^\s{2,}(\S+)\s+([0-9a-f]{40})\s*$", re.M)


def v_blob_bytes(p: Path) -> str:
    """`git` **blob** 的 sha1（`sha1("blob <n>\\0" + bytes)`）。"""
    data = p.read_bytes()
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def v_git_blob(p: Path) -> str:
    """`git hash-object` 的实测值（**同一件事的第二条独立算法**）。

    **为什么非要用 `git hash-object` 而不是裸 sha256**：本仓 `core.autocrlf=true`，
    裸 sha256 量的是**工作树字节**、`git hash-object` 量的是**入库 blob**（按
    `.gitattributes` 的过滤器口径）。本判据声称的是「**入库字节**逐字节不变」，
    口径必须是后者（本项目在这一条上有过事故）。两条算法**都要**跑：结果不等 ⇒ 红——
    那说明 `corpus/papers/**` 的 `-text` 约定被破坏了。
    """
    r = subprocess.run(["git", "hash-object", "--", str(p)], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"`git hash-object` 非零退出（{r.returncode}）：{p.name}；"
            f"stderr={r.stderr.decode('utf-8', 'replace')[:200]}")
    return r.stdout.decode("utf-8").strip()


def v_baseline(recon: Path) -> dict[str, str]:
    """从 `recon/map-recon.txt` 的 **§0「开工基准」** 段读回开工时的 blob 登记。

    fail-closed 的三态都要分开（约束 4）：**登记文件不存在** → 抛；**§0 段不存在** → 抛；
    **该路径没登记** → 抛（「基准里没有这一条」与「这一条没变」是两件事）。
    """
    if not recon.is_file():
        raise FileNotFoundError(f"开工基准的登记不在：{recon.as_posix()}")
    text = recon.read_bytes().decode("utf-8")
    m = re.search(r"^## 0\. 开工基准.*?^## 1\.", text, re.S | re.M)
    if not m:
        raise ValueError(f"{recon.as_posix()} 里找不到 §0「开工基准」那一段")
    out: dict[str, str] = {}
    for mm in V_BASELINE_ROW.finditer(m.group(0)):
        out.setdefault(mm.group(1), mm.group(2))
    if not out:
        raise ValueError(f"{recon.as_posix()} §0 里一行基准都没解析出来")
    return out


def v_split_unesc(s: str, sep: str = "|") -> list[str]:
    """按**未转义**的 `sep` 切（`\\X` 一律当整体；与 `index._esc` 的转义规则配套）。"""
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


def v_unesc(s: str) -> str:
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


def v_annotation_labels(path: Path) -> dict[tuple[int, str], set[str]]:
    """**自己解析标注文件** → `{(年, 题号): {标签名…}}`（`L1 · L2` 逐字）。"""
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
        raise ValueError(f"标注文件里一个节都没解析出来：{path.as_posix()}")
    return out


def v_annotation_regimes(path: Path) -> dict[tuple[int, str], str]:
    """**自己解析**标注文件 → `{(年, 题号): data_regime}`（受控枚举逐字）。**独立实现**。

    M-13 判「桶归属」时要用它：一个 `(模型, 篇)` 对落在哪些桶，由**该篇题号的标签集合**
    与**该题的 `data_regime`** 一起决定。
    """
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    out: dict[tuple[int, str], str] = {}
    cur: tuple[int, str] | None = None
    for ln in text.split("\n"):
        m = V_ANNOT_SECTION.match(ln.rstrip())
        if m:
            cur = (int(m.group(1)), m.group(2))
            continue
        if cur is None or cur in out:
            continue
        mr = V_ANNOT_REGIME_LINE.match(ln.rstrip())
        if not mr:
            continue
        dr = mr.group(1).split("｜")[0].split("|")[0]
        for cand in sorted(V_REGIMES, key=len, reverse=True):
            if dr.startswith(cand):
                out[cur] = cand
                break
    if not out:
        raise ValueError(f"标注文件里一个 `data_regime` 都没解析出来：{path.as_posix()}")
    return out


def v_problem_types(path: Path) -> set[str]:
    """分类法条目名（L1+L2），独立读。"""
    out = {m.group(2).strip() for m in
           (V_TAXLINE.match(x.strip()) for x in
            path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n")) if m}
    if not out:
        raise ValueError(f"分类法一条都没读出来：{path.as_posix()}")
    return out


def v_models(path: Path) -> list[tuple[str, tuple[str, ...]]]:
    """词表 → `[(规范词, (变体…)), …]`，独立读。"""
    out = []
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        out.append((parts[0], tuple(x for x in parts if x)))
    if not out:
        raise ValueError(f"词表是空的：{path.as_posix()}")
    return out


def v_name_parts(name: str) -> list[str]:
    """标签名 → 去编号后的整名与 `/`、`、`、括号拆出的成分（`verify_types.py` T3 的同一套）。"""
    whole = re.sub(r"^\d+(?:\.\d+)?\s+", "", name).strip()
    parts = [whole]
    for piece in re.split(r"[/、()（）]", whole):
        piece = piece.strip()
        if piece and piece not in parts:
            parts.append(piece)
    return parts


def v_tags(path: Path) -> dict:
    """**自己解析** `TAGS.md` → 一层行 / 二层指针 / 三层篇数 / **keywords 栏** / sid→md。

    `keywords` 栏自 2b 起由本判据读：**M-9/M-10/M-11 的参照侧就是它**（作者自己写的
    Key words 行，Task 6 原样抄进去的）。它与 `models` 栏（我们算的）**来源不同**——
    这正是召回度量不恒真的根。
    """
    papers: list[tuple[str, str, str]] = []
    hits: list[dict] = []
    kw: dict[str, str] = {}
    md_of: dict[str, str] = {}
    l3, cur_sid, cur_md, seen_l3 = -1, "", "", False
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        m1 = V_L1_ROW.match(ln)
        if m1:
            cells = [v_unesc(x) for x in v_split_unesc(ln.strip()[1:-1], "|")]
            if len(cells) != 16:
                raise ValueError(f"TAGS 一层不是 16 栏：{ln[:80]!r}")
            sid = m1.group(1)
            papers.append((sid, m1.group(2), m1.group(3)))
            kw[sid] = cells[14].strip()
            continue
        mh = V_L2_HEAD.match(ln)
        if mh:
            cur_sid, cur_md = mh.group(1), ""
            continue
        mm = V_L2_MD.match(ln)
        if mm and cur_sid:
            cur_md = mm.group(1).strip()
            md_of[cur_sid] = cur_md
            continue
        if cur_sid and ln.startswith("- "):
            parts = v_split_unesc(ln[2:], TAGS_SEP)
            assert len(parts) == 4, f"二层指针不是 4 段：{ln[:80]!r}"
            pg = re.fullmatch(r"p(\d+)", parts[1].strip())
            nx = re.fullmatch(r"x(\d+)", parts[2].strip())
            assert pg and nx, f"二层指针的页/次数不合式：{ln[:80]!r}"
            hits.append({"sid": cur_sid, "model": v_unesc(parts[0]).strip(),
                         "page": int(pg.group(1)), "n_occ": int(nx.group(1)),
                         "snippet": v_unesc(parts[3]), "md": cur_md})
            continue
        m3 = V_L3_COUNT.match(ln)
        if m3 and not seen_l3:
            l3, seen_l3 = int(m3.group(1)), True
    if not papers or not hits or l3 < 0:
        raise ValueError("TAGS 的解析缺件：一层/二层/三层三样都要能解析出来（fail-closed）")
    if len(kw) != len(papers) or len(md_of) != len(papers):
        raise ValueError("TAGS 一层行数 ≠ keywords 栏数或 md 数（fail-closed）")
    return {"papers": papers, "hits": hits, "n_zero": l3, "kw": kw, "md_of": md_of}


def v_index_rows(text: str) -> list[tuple[str, list[str]]]:
    """`INDEX.md` 的记录表 → `[(稳定 ID, [11 栏]), …]`。**独立读**（自己一份正则）。"""
    out: list[tuple[str, list[str]]] = []
    for ln in text.replace("\r\n", "\n").split("\n"):
        if not ln.startswith("| ") or ln.startswith("| :"):
            continue
        cells = [v_unesc(x).strip() for x in v_split_unesc(ln.strip()[1:-1], "|")]
        if len(cells) != 11 or not re.fullmatch(r"P\d{4}-[A-F]-\d{2,}", cells[0]):
            continue
        out.append((cells[0], cells))
    if not out:
        raise ValueError("`INDEX.md` 的记录表一行都没解析出来（fail-closed）")
    return out


def v_md_lines(path: Path) -> tuple[list[str], list[int]]:
    """md 文件 → `(行表, 逐行页码)`。**另一份实现**（与 `index.sample_page_of` 各写一份）。"""
    text = path.read_bytes().decode("utf-8")
    lines = text.split("\n")
    pages, cur = [], 0
    for ln in lines:
        m = V_PAGE_ANCHOR.match(ln.rstrip("\r"))
        if m:
            cur = int(m.group(1))
        pages.append(cur)
    return lines, pages


def v_parse_map(path: Path) -> dict:
    """**自己解析** `MODEL_MAP.md`（与生成器各写一份正则）。

    只认机器可读的东西：① 覆盖边界那一行；② 第一节的逐题块（题号 + 论文数）；
    ③ 第二节的桶表行与**去重指针行**（6 段，末段是「所属桶」）；④ 第三节的两个计数行与
    低置信逐条；⑤ **第四节**的机读行、逐篇表、未覆盖清单。人工撰写的散文**一概不解析**。
    """
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n")
    lines = text.split("\n")
    out: dict = {"cover": None, "problems": [], "buckets": [], "ptr_rows": [],
                 "zero": None, "low": None, "low_items": [], "n_prose": 0,
                 "cov": None, "cov_papers": [], "cov_uncollected": []}
    sec = ""
    cur_prob: tuple[str, str] | None = None
    for ln in lines:
        if ln.startswith("## 第一节"):
            sec = "1"
            continue
        if ln.startswith("## 第二节"):
            sec = "2"
            continue
        if ln.startswith("## 第三节"):
            sec = "3"
            continue
        if ln.startswith("## 第四节"):
            sec = "4"
            continue
        if out["cover"] is None and "覆盖边界：" in ln:
            out["cover"] = ln.strip()
            continue
        if sec == "1":
            mp = V_M_PROBLEM.match(ln)
            if mp:
                cur_prob = (mp.group(1), mp.group(2))
                out["problems"].append({"year": mp.group(1), "problem": mp.group(2),
                                        "n_papers": None})
                continue
            mq = V_M_NPAPERS.match(ln)
            if mq and cur_prob is not None and out["problems"]:
                out["problems"][-1]["n_papers"] = int(mq.group(1))
                continue
        if sec == "2":
            if ln.startswith("| ") and not ln.startswith("| :"):
                cells = [v_unesc(x).strip() for x in
                         v_split_unesc(ln.strip()[1:-1], "|")]
                if len(cells) != 8 or not cells[0].isdigit():
                    out["n_prose"] += 1
                    continue
                out["buckets"].append({
                    "idx": int(cells[0]), "l1l2": cells[1], "regime": cells[2],
                    "mark": cells[3], "srcs": cells[4], "n_papers": int(cells[5]),
                    "n_pairs": int(cells[6]), "models": cells[7]})
                continue
            if ln.startswith("- "):
                parts = v_split_unesc(ln[2:], TAGS_SEP)
                if len(parts) != 6:
                    raise ValueError(
                        f"去重指针行不是 6 段（词; 篇; 页; md; 片段; 桶号）：{ln[:90]!r}")
                pp = re.fullmatch(r"p(\d+)", parts[2].strip())
                if not pp:
                    raise ValueError(f"去重指针行的页不合式：{ln[:90]!r}")
                bnos = v_unesc(parts[5]).strip()
                if not re.fullmatch(r"\d+(,\d+)*", bnos):
                    raise ValueError(f"「所属桶」列不合式（应 `1,3,5`）：{ln[:90]!r}")
                out["ptr_rows"].append({
                    "model": v_unesc(parts[0]).strip(), "sid": v_unesc(parts[1]).strip(),
                    "page": int(pp.group(1)), "md": v_unesc(parts[3]),
                    "snippet": v_unesc(parts[4]),
                    "buckets": [int(x) for x in bnos.split(",")]})
                continue
        if sec == "3":
            mz = V_M_ZERO.search(ln)
            if mz and out["zero"] is None:
                out["zero"] = (int(mz.group(1)), int(mz.group(2)), mz.group(3).strip())
                continue
            ml = V_M_LOW.search(ln)
            if ml and out["low"] is None:
                out["low"] = (int(ml.group(1)), int(ml.group(2)))
                continue
            if out["low"] is not None and ln.startswith("  - "):
                parts = v_split_unesc(ln[4:], TAGS_SEP)
                if len(parts) == 4:
                    out["low_items"].append((v_unesc(parts[0]).strip(),
                                             v_unesc(parts[1]).strip(), parts[2].strip()))
                continue
        if sec == "4":
            mc = V_COV_LINE.match(ln)
            if mc and out["cov"] is None:
                # **键要去空白**：分隔符是 ` · `，`[^=·]+?` 会把分隔符后的那个空格吃进键里
                # （实测踩过：`参照不存在` 被读成 ` 参照不存在`，于是整格对不上）。
                out["cov"] = {k.strip(): v.strip()
                              for k, v in V_COV_KV.findall(mc.group(1))}
                continue
            mp = V_COV_PAPER.match(ln)
            if mp:
                out["cov_papers"].append((mp.group(1), mp.group(2).strip(),
                                          int(mp.group(3)), int(mp.group(4)),
                                          int(mp.group(5)), int(mp.group(6)),
                                          mp.group(7).strip(), mp.group(8).strip()))
                continue
            mu = V_COV_UNCOV.match(ln)
            if mu:
                out["cov_uncollected"].append((mu.group(1), mu.group(2), mu.group(3)))
                continue
    return out


def v_git_blob_bytes(blob: str) -> bytes:
    """从 **git 对象库**取一个 blob 的字节（用于「增长前」的基线；fail-closed）。"""
    r = subprocess.run(["git", "cat-file", "blob", blob], cwd=str(ROOT),
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"`git cat-file blob {blob}` 非零退出（{r.returncode}）："
            f"{r.stderr.decode('utf-8', 'replace')[:200]}")
    return r.stdout


def v_vocab_forms(data: bytes) -> set[str]:
    """词表**字节** → 全部词形（规范词 + 变体）的集合。**独立读**（不调 `vocab.load`）。"""
    out: set[str] = set()
    for ln in data.decode("utf-8").replace("\r\n", "\n").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        for x in (y.strip() for y in s.split("|")):
            if x:
                out.add(x)
    if not out:
        raise ValueError("词表字节里一个词形都没读出来（fail-closed）")
    return out


def v_triage(path: Path) -> list[tuple[str, str, str, str]]:
    """分流表 → `[(词形, 处置, 类别, 理由), …]`。**独立读**（不调 `coverage.read_triage`）。"""
    return v_triage_rows(path, TRIAGE)


def v_triage_rows(path: Path, rel: str) -> list[tuple[str, str, str, str]]:
    """一张分流表的**解析**（两张表共用这一份实现 ⇒ 规则不会分叉）。"""
    if not path.is_file():
        raise FileNotFoundError(f"分流表不在：{rel}")
    out: list[tuple[str, str, str, str]] = []
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        if not ln.strip() or ln.startswith("#"):
            continue
        cells = ln.split("\t")
        if len(cells) != 4:
            raise ValueError(f"{rel} 不是 4 栏（TAB 分隔）：{ln[:80]!r}")
        out.append((cells[0], cells[1], cells[2], cells[3]))
    if not out:
        raise ValueError(f"{rel} 一行都没有（fail-closed）")
    return out


def v_body_triage(path: Path) -> list[tuple[str, str, str, str]]:
    """**第二张同格式表**（正文扫描的逐条处置）→ 与 `v_triage` **同一个四元组**。

    它是 `v_triage_rows` 的第二个调用点：解析、`场景 ⇒ 不收` / `无法归类 ⇒ 待定` 的约束、
    `收录` 的两向等式**都走同一份代码**——这就是「口径只有一处」的可执行含义。
    """
    return v_triage_rows(path, BODY_TRIAGE)


def v_kw_segment(md_text: str) -> str:
    """该 md 的 **Keywords 段**（keywords 行 + 续行，行间只留一个空格）。**独立实现**。

    切法写死在 `growth_triage.txt` §2；`coverage.py` 里另有一份（那是实现侧）。
    """
    text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    m = V_KEYWORDS.search(text)
    if not m:
        return ""
    lines = text.split("\n")
    cur, idx = 0, 0
    for i, ln in enumerate(lines):
        if cur <= m.end() <= cur + len(ln) + 1:
            idx = i
            break
        cur += len(ln) + 1
    seg = [m.group(1).strip()]
    for ln in lines[idx + 1:]:
        s = ln.strip()
        if not s or V_KW_SEG_STOP.match(s) or V_KEYWORDS.match(s):
            break
        seg.append(s)
    return " ".join(seg)


def v_norm_locate(s: str) -> str:
    """定位用的归一化（**T2 的形态**：行尾归一 + 空白折叠 + `casefold`）。"""
    return re.sub(r"\s+", " ", s.replace("\r\n", "\n").replace("\r", "\n")).strip().casefold()


def v_pieces(keywords: str) -> list[str]:
    """一行作者关键词 → 片表（**逐字复刻 `verify_ids.py` 的 I13 拆法**）。"""
    out: list[str] = []
    for piece in V_PIECE_SEP.split(keywords):
        p = piece.strip().strip("*_ ").strip()
        if 2 <= len(p) <= 40:
            out.append(p)
    return out


def v_term_pattern(variant: str) -> tuple[str, int]:
    """变体 → `(正则, flags)`。规则与 `tools/papers/vocab.py` 的 docstring 逐条对应，
    **但是本文件另写的一份**（判据侧的参照必须独立于实现；`coverage.py` 里还有第三份）。

    载重规则三条：含 ASCII 字母/数字才加词边界；变体自身含 `*`/`_` 时邻接集合并上 `*_`；
    全大写字母的缩写**大小写敏感**（否则英文动词 `did` 会命中 `DID`）。
    """
    e = re.escape(variant)
    if not re.search(r"[A-Za-z0-9]", variant):
        return e, re.IGNORECASE
    cls = "A-Za-z0-9"
    if "*" in variant or "_" in variant:
        cls += r"*_"
    letters = [c for c in variant if c.isascii() and c.isalpha()]
    flags = 0 if (len(letters) >= 2 and all(c.isupper() for c in letters)) else re.IGNORECASE
    return rf"(?<![{cls}]){e}(?![{cls}])", flags


def v_covered(text: str, vocab_rows: list[tuple[str, tuple[str, ...]]]) -> list[str]:
    """`text` 被哪些词条覆盖（词条规范词表）。**独立实现**（见 `v_term_pattern`）。"""
    hit: list[str] = []
    for word, variants in vocab_rows:
        for v in variants:
            pat, flags = v_term_pattern(v)
            if re.search(pat, text, flags):
                hit.append(word)
                break
    return hit


def v_vocab_rows(data: bytes) -> list[tuple[str, tuple[str, ...]]]:
    """词表**字节** → `[(规范词, (变体…)), …]`（**独立读**）。"""
    out: list[tuple[str, tuple[str, ...]]] = []
    for ln in data.decode("utf-8").replace("\r\n", "\n").split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        parts = [x.strip() for x in s.split("|")]
        out.append((parts[0], tuple(x for x in parts if x)))
    if not out:
        raise ValueError("词表字节里一个词条都没读出来（fail-closed）")
    return out


def v_cov_evidence(path: Path) -> dict:
    """`coverage-evidence.txt` → `{键: 值}` + 三份清单。**独立读**（本脚本自己的正则）。"""
    if not path.is_file():
        raise FileNotFoundError(f"匹配度证据不在：{COV_EVIDENCE}")
    kv: dict[str, str] = {}
    uncov: list[tuple[str, str, str]] = []
    papers: list[tuple[str, ...]] = []
    low: list[tuple[str, str]] = []
    for ln in path.read_bytes().decode("utf-8").replace("\r\n", "\n").split("\n"):
        if ln.startswith("未覆盖\t"):
            c = ln.split("\t")
            uncov.append((c[1], c[2], c[3]))
            continue
        if ln.startswith("收录\t"):
            c = ln.split("\t")
            kv.setdefault("_收录清单", "")
            papers.append(("收录", c[1], c[2]))
            continue
        if ln.startswith("篇\t") or ln == "篇":       # 逐篇表头
            continue
        if ln.startswith("低置信\t"):
            c = ln.split("\t")
            low.append((c[1], c[2]))
            continue
        m = V_EV_KV.match(ln)
        if m:
            kv.setdefault(m.group(1).strip(), m.group(2).strip())
    if not kv or "召回分母" not in kv:
        raise ValueError(f"{COV_EVIDENCE} 里读不到「召回分母」等键（fail-closed）")
    kv["_未覆盖清单"] = uncov
    kv["_收录清单"] = [x for x in papers if x[0] == "收录"]
    kv["_低置信清单"] = low
    return kv


def checks(lines: list[str], limit: int = 0, meta: dict | None = None,
           out: Path | None = None, report=None) -> bool:
    """判据主体。**被测模块的 import 放在函数体内**（照 `verify_ids.py`）。"""
    from tools.papers import io as io_mod
    from tools.papers import report as rep

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

    map_p = ROOT / MAP
    if not map_p.is_file():
        raise FileNotFoundError(f"配对产物不在：{MAP}（「没生成」与「生成为空」是两件事）")
    mv = v_parse_map(map_p)
    tags = v_tags(ROOT / TAGS)
    ann = v_annotation_labels(ROOT / ANNOTATIONS)
    # 每题的 `data_regime`（**自己再解析一次**；M-13 判桶归属要用）。
    regime_of = v_annotation_regimes(ROOT / ANNOTATIONS)
    tax = v_problem_types(ROOT / PROBLEM_TYPES)
    terms = v_models(ROOT / MODELS)
    vocab_norm = {re.sub(r"\s+", "", v).casefold() for _c, vs in terms for v in vs}
    base = v_baseline(ROOT / RECON)
    # **匹配度的机读证据**（M-10 起都要用它）。早读一次：M-10 在 M-14 之前就要拿它对账。
    ev = v_cov_evidence(ROOT / COV_EVIDENCE)

    lines.append(
        f"配对表判据 M-1…M-16 · 全量 {len(tags['papers'])} 篇 / {len(ann)} 题标注"
        f"（`--limit {limit}`：**不缩样本**，只改报告落点并跳过 M-1-b）"
        if limit > 0 else
        f"配对表判据 M-1…M-16 · 全量 {len(tags['papers'])} 篇 / {len(ann)} 题标注")
    lines.append(f"  产物：`{MAP}`（{map_p.stat().st_size} B）· "
                 f"参照：`{TAGS}` 一层 {len(tags['papers'])} 行 / 二层 {len(tags['hits'])} 条指针")
    lines.append("=" * 78)

    # ==================== M-1：解冻面（blob 双边）============================
    # **开工基准里该有的六条**：三份入库产物（解冻面的双边） + 旧放行证据 + 旧标注草案。
    # `MODEL_MAP.md` **不在其中**——它是本轮**新生成**的产物，开工时不存在、没有基准可比；
    # 「它是不是生成器产出的」由 M-8 判（那条才是它的重放性判据）。
    needed = [TAGS, "corpus/papers/INDEX.md", "corpus/papers/PROVENANCE.md",
              "tests/papers/reports/ids-report.txt", "tests/papers/recon/PROBLEM_TYPES-draft.md"]
    miss_base = [k for k in needed if k not in base]
    if miss_base:
        add("M-1", False, [f"开工基准（`{RECON}` §0）里没有这些路径的登记：{miss_base}"
                           f"——「没登记」与「没变」是两件事，判 FAIL"])
    else:
        cur = {p: v_git_blob(ROOT / p) for p in INDEX_PRODUCTS}
        cur[MAP] = v_git_blob(map_p)
        py = {p: v_blob_bytes(ROOT / p) for p in (*INDEX_PRODUCTS, MAP)}
        py_bad = [p for p in py if py[p] != cur[p]]
        changed = [p for p in INDEX_PRODUCTS if cur[p] != base[p]]
        bad1 = []
        # （1）`PROVENANCE.md`：**逐字节不变**（既不含 `problem_type` 也不含 `models`）。
        if cur["corpus/papers/PROVENANCE.md"] != base["corpus/papers/PROVENANCE.md"]:
            bad1.append(
                f"corpus/papers/PROVENANCE.md：blob "
                f"{cur['corpus/papers/PROVENANCE.md'][:12]}… ≠ 开工基准 "
                f"{base['corpus/papers/PROVENANCE.md'][:12]}…（**这一份本该逐字节不变**"
                f"——它既不含 `problem_type` 也不含 `models`）")
        # （2）`TAGS.md`：**变了**（2a 加栏 + 2b 词表增长，两轮都该动它）。
        if cur[TAGS] == base[TAGS]:
            bad1.append(f"{TAGS}：blob 与开工基准**相同**（{base[TAGS][:12]}…）——"
                        f"解冻后它本该多一栏 `problem_type`、2b 后 `models` 栏也该变，"
                        f"没变说明两轮里有一轮没落地")
        # （3）`INDEX.md`：**变了，但只许差「模型/算法」一栏**（下标 9 / 第 10 栏）。
        # 2a 的口径是「INDEX 逐字节不变」（那一轮只加 `problem_type` 栏）；2b 里
        # **词表增长必然改到 `INDEX.md` 的 `模型/算法` 栏**（与 `TAGS.md` 的 `models` 栏同源）。
        # 判据跟着改成**逐行逐栏**比对：**只允许第 10 栏不同**。这比「不变」更严——
        # 「不变」抓不到「只改对了 models 栏、同时顺手改了别的栏」这种形态。
        idx_change_cols: set[int] = set()
        old_idx = v_index_rows(v_git_blob_bytes(base["corpus/papers/INDEX.md"])
                               .decode("utf-8"))
        new_idx = v_index_rows((ROOT / "corpus/papers/INDEX.md").read_bytes().decode("utf-8"))
        if [r[0] for r in old_idx] != [r[0] for r in new_idx]:
            bad1.append("`INDEX.md` 的**行序或行集合**变了（2b 只许改 `模型/算法` 一栏"
                        "的字，不许增删行）")
        else:
            for (sid, a), (_s2, b) in zip(old_idx, new_idx):
                if len(a) != len(b):
                    bad1.append(f"`INDEX.md` 的 {sid} 栏数 {len(a)} ≠ 基准的 {len(b)}")
                    continue
                for i, (x, y) in enumerate(zip(a, b)):
                    if x != y:
                        idx_change_cols.add(i)
            if idx_change_cols - {9}:
                bad1.append(f"`INDEX.md` 变动的栏位 {sorted(idx_change_cols)} 里出现了"
                            f"**`模型/算法`（第 10 栏）之外**的栏——2b 的词表增长只该动那一栏")
        if py_bad:
            bad1.append(f"两条独立算法（Python 的 blob 公式 vs `git hash-object`）不等："
                        f"{py_bad}——说明字节保真被行尾转换破坏了（`corpus/papers/**` 的 "
                        f"`-text` 约定）")
        add("M-1", not bad1, bad1 or [
            f"**三份产物、两种期望**：`PROVENANCE.md` 与开工基准**逐字节相同**"
            f"（{base['corpus/papers/PROVENANCE.md'][:12]}…）；`TAGS.md` **变了**"
            f"（{base[TAGS][:12]}… → {cur[TAGS][:12]}…）；`INDEX.md` **变了但只差第 10 栏**"
            f"（`模型/算法`：实测变动栏位 {sorted(idx_change_cols)}，共 {len(new_idx)} 行）",
            f"开工基准来自 `{RECON}` §0（开工当天 `git hash-object` 实测登记，"
            f"HEAD = 9a1689daa68824f10c69a505f60b0b933a35c5bd）："
            f"INDEX {base['corpus/papers/INDEX.md'][:12]}… · "
            f"TAGS {base[TAGS][:12]}… · PROVENANCE {base['corpus/papers/PROVENANCE.md'][:12]}…",
            "**`INDEX.md` 那条为什么改了形状（2a → 2b）**：2a 要求「逐字节不变」，因为那一轮"
            "只往 `TAGS.md` 加 `problem_type` 栏；2b 的词表增长**必然**改到 `INDEX.md` 的"
            "`模型/算法` 一栏（它与 `TAGS.md` 的 `models` 栏是同一份事实的两个落点）。"
            "这不是放宽：从「整份不变」改成「**逐行逐栏**比对、只许第 10 栏不同」——"
            "后者才抓得到「顺手改了别的栏」。基准的旧字节从 **git 对象库**取"
            "（`git cat-file blob`），不靠记忆。",
            "**同一份 fact 的第二条算法**：本判据同时用 `git hash-object` 与 Python 的 "
            "`sha1(\"blob <n>\\0\" + bytes)` 算一遍，两者必须相等——不相等就说明工作树字节"
            "与入库 blob 分叉（`core.autocrlf` 的形态）。",
            f"**另：`{MAP}` 的 blob 本次实测** = {cur[MAP][:12]}…；`recon` 里另登记了旧 "
            f"`ids-report.txt`（{base['tests/papers/reports/ids-report.txt'][:12]}…）与旧标注草案"
            f"（{base['tests/papers/recon/PROBLEM_TYPES-draft.md'][:12]}…，转正前的来源）。",
        ])

    # ---- M-1-b：重放性（**全量跑才跑**：要重开 43 份原件，是全脚本唯一慢的一步）----
    if limit > 0:
        lines.append("  M-1-b 本次**未跑**（`--limit` 不重建产物；重放性由全量跑证明）")
    else:
        from tools.papers import index as index_mod
        scratch = rep.LIMITED_DIR / "map-index-replay"
        r = index_mod.build(COLLECTION, out_dir=scratch)
        pb = []
        for name in ("INDEX.md", "TAGS.md", "PROVENANCE.md"):
            a, b = v_git_blob(scratch / name), v_git_blob(io_mod.DERIVED / name)
            if a != b:
                pb.append(f"{name}: 重跑 {a[:12]}… ≠ 入库 {b[:12]}…")
        add("M-1-b", not pb and r.n_entries == len(tags["papers"]), pb or [
            f"`index.build` 重跑到**不入库**目录（`{rep.rel(scratch)}`），三份产物与入库的"
            f"**逐字节相同**（INDEX/TAGS/PROVENANCE 各 {v_git_blob(scratch / 'TAGS.md')[:12]}… "
            f"一类实测）——生成器确定性 + 入库的就是它产出的",
            "**为什么重跑到不入库目录**：本判据**不许碰入库产物**（碰了就可能把证据毁了，"
            "「探针自己变成破坏者」是本项目栽过的形态）；重跑的目的只是「同样的输入 ⇒ "
            "同样的字节」，在不入库目录里同样成立。",
        ])

    # ==================== M-2：覆盖双边等式 ================================
    tags_probs: list[tuple[str, str]] = []
    for _sid, y, p in tags["papers"]:
        if (y, p) not in tags_probs:
            tags_probs.append((y, p))
    mv_probs = [(d["year"], d["problem"]) for d in mv["problems"]]
    # **`or` 会把合法的 `n_papers == 0` 折成 −1**（`0 or -1` ⇒ `-1`）——那是一条
    # 「潜在的错误结论源」：真出现「某题 0 篇」时本判据会拿 −1 去求和、把一个正确的
    # 产物判红（或把差额说错）。取数只认 `None`（「没解析出来」），与下面那行同一写法。
    # 当前语料上不可达（6 题都有论文），但写法必须正确。
    sums = sum(-1 if d["n_papers"] is None else d["n_papers"] for d in mv["problems"])
    m2_bad = []
    if len(mv_probs) != len(tags_probs):
        m2_bad.append(f"逐题表 {len(mv_probs)} 题 ≠ TAGS 一层的 {len(tags_probs)} 题")
    if set(mv_probs) != set(tags_probs):
        m2_bad.append(f"题号集合不等：只在配对表 {sorted(set(mv_probs) - set(tags_probs))}"
                      f" · 只在 TAGS {sorted(set(tags_probs) - set(mv_probs))}")
    if sums != len(tags["papers"]):
        m2_bad.append(f"逐题论文数之和 {sums} ≠ TAGS 一层行数 {len(tags['papers'])}")
    if any(d["n_papers"] is None for d in mv["problems"]):
        m2_bad.append("有逐题块的「论文数」行没解析出来")
    # ---- 第二节表 ↔ 去重指针行：**两张表互为参照**（2b 的形状）----------------
    # 上一版的逐桶指针节没了 ⇒ 桶表里的「论文数 / 对数 / 模型列 / 来源题」不能再用
    # 「逐桶指针」对账。改成用**去重指针行的「所属桶」列反推**：桶 i 的成员 = 桶列里含 i
    # 的所有行。**这是两向的**：桶表声明的数 == 反推出来的数；而「每个桶号都被至少一行
    # 引用」由 M-5 判。
    sid2prob = {sid: (y, p) for sid, y, p in tags["papers"]}
    bucket_from_ptr: dict[int, list[dict]] = {}
    for p in mv["ptr_rows"]:
        for b in p["buckets"]:
            bucket_from_ptr.setdefault(b, []).append(p)
    for b in mv["buckets"]:
        members = bucket_from_ptr.get(b["idx"], [])
        sids = {p["sid"] for p in members}
        srcs = sorted({sid2prob[s] for s in sids if s in sid2prob})
        want_srcs = {tuple(x.strip().split(" ", 1)) for x in b["srcs"].split("、") if x.strip()}
        want_srcs = {k for k in want_srcs if len(k) == 2 and k[1]}
        if len(sids) != b["n_papers"]:
            m2_bad.append(f"桶 {b['idx']}：表里论文数 {b['n_papers']} ≠ 由「所属桶」列反推的 "
                          f"{len(sids)}")
        if len(members) != b["n_pairs"]:
            m2_bad.append(f"桶 {b['idx']}：表里 (模型,篇) 对 {b['n_pairs']} ≠ 反推的 "
                          f"{len(members)}")
        if set(srcs) != want_srcs:
            m2_bad.append(f"桶 {b['idx']}：表里来源题 {sorted(want_srcs)} ≠ 反推的 {srcs}")
        want_models: dict[str, int] = {}
        for p in members:
            want_models[p["model"]] = want_models.get(p["model"], 0) + 1
        got_models: dict[str, int] = {}
        for piece in b["models"].split(" · "):
            mm2 = re.fullmatch(r"(.*)（(\d+) 篇）", piece.strip())
            if not mm2:
                m2_bad.append(f"桶 {b['idx']}：模型列的 {piece!r} 不合式（应为 `模型（N 篇）`）")
                continue
            got_models[mm2.group(1).strip()] = int(mm2.group(2))
        if got_models != want_models:
            m2_bad.append(f"桶 {b['idx']}：模型列 {got_models} ≠ 反推的 {want_models}")
    if limit <= 0 and len(mv_probs) != 6:
        m2_bad.append(f"全量跑要求 6 题，实测 {len(mv_probs)}")
    add("M-2", not m2_bad, m2_bad[:20] or [
        f"题数 **{len(mv_probs)}** == TAGS 一层出现过的 `(年, 题号)` 数 **{len(tags_probs)}**"
        f" == **{len(mv_probs)}**；逐题论文数之和 **{sums}** == TAGS 一层行数 "
        f"**{len(tags['papers'])}**",
        f"**第二节表 ↔ 去重指针行（{len(mv['buckets'])} 个桶、{len(mv['ptr_rows'])} 行）**："
        f"逐桶的「论文数 / (模型,篇) 对 / 模型列 / 来源题」**全部**由「所属桶」列反推得到、"
        f"**两向相等**",
        f"逐题：{' · '.join(f'{y} {p} {d}篇' for (y, p), d in zip(mv_probs, [x['n_papers'] for x in mv['problems']]))}",
        "**双边等式，不是下界**：多一题、少一题、多算一篇、桶里少一行都会红。"
        "**2b 的形状变化**：上一版这两张表靠「逐桶指针」对账；去重后靠「所属桶」列反推——"
        "判的是同一件事，而且**新增了一列可单独判的桶归属**（见 M-13）。",
    ])

    # ==================== M-13：去重后的两向等式 + 桶归属 ==================
    # **原 M-3 的新形态**（任务书 §一 产物 4 点名）：M-3 那个编号**不再存在**，
    # 它的实体在 M-13（同一件事 + 新增「桶归属」那一半）。旧编号的去向逐字登记在
    # `tests/papers/recon/map-recon.txt` §14（**别在旧证据文件里找 M-3**）。
    mv_pairs = {(p["sid"], p["model"]) for p in mv["ptr_rows"]}
    tg_pairs = {(h["sid"], h["model"]) for h in tags["hits"]}
    only_mv = sorted(mv_pairs - tg_pairs)
    only_tg = sorted(tg_pairs - mv_pairs)
    # 桶归属：每行的桶号集合 == 由标注（该篇题号的标签集合）推出、经第二节表映射的桶号集合。
    key2no: dict[tuple[str, str, str], int] = {}
    for b in mv["buckets"]:
        if " · " not in b["l1l2"]:
            continue
        l1, l2 = (x.strip() for x in b["l1l2"].split(" · ", 1))
        key2no[(l1, l2, b["regime"])] = b["idx"]
    n_bad_bucket: list[str] = []
    n_dup_rows: list[str] = []
    seen_rows: set[tuple[str, str]] = set()
    for p in mv["ptr_rows"]:
        key = (p["sid"], p["model"])
        if key in seen_rows:
            n_dup_rows.append(f"{key} 在去重指针节里出现了两次")
        seen_rows.add(key)
        yrs = sid2prob.get(p["sid"])
        if yrs is None:
            n_bad_bucket.append(f"{p['sid']} 不在 TAGS 一层里（幻影）")
            continue
        labels = ann.get((int(yrs[0]), yrs[1]))
        if labels is None:
            n_bad_bucket.append(f"{yrs[0]} {yrs[1]}（{p['sid']}）在标注文件里找不到那一节")
            continue
        want: set[int] = set()
        for lab in labels:
            if " · " not in lab:
                continue
            l1, l2 = (x.strip() for x in lab.split(" · ", 1))
            k = (l1, l2, regime_of[(int(yrs[0]), yrs[1])])
            if k not in key2no:
                n_bad_bucket.append(f"{p['sid']} 的标签 {lab!r} 映射不到任何桶")
                continue
            want.add(key2no[k])
        if set(p["buckets"]) != want:
            n_bad_bucket.append(
                f"{p['sid']} 的 {p['model']!r}：「所属桶」{sorted(set(p['buckets']))} "
                f"≠ 由标注推出的 {sorted(want)}")
    add("M-13", not only_mv and not only_tg and not n_bad_bucket and not n_dup_rows,
        (only_mv or only_tg or n_bad_bucket or n_dup_rows)[:20] and
        [f"只在配对表（**发明**）：{only_mv[:8] or '无'}（合计 {len(only_mv)}）",
         f"只在 TAGS（**丢失**）：{only_tg[:8] or '无'}（合计 {len(only_tg)}）",
         f"去重指针节里重复的行：{n_dup_rows[:4] or '无'}（合计 {len(n_dup_rows)}）",
         f"「所属桶」与标注推出的桶集合不等：{n_bad_bucket[:8] or '无'}"
         f"（合计 {len(n_bad_bucket)}）"] or [
        f"**两向互相包含**：配对表 **{len(mv_pairs)}** 对 · TAGS 二层 **{len(tg_pairs)}** 对"
        f"（**本来就是去重口径**——去重后的一行 = 一个对，重复的行也会被本判据抓出来）",
        f"**桶归属另判**：{len(mv['ptr_rows'])} 行的「所属桶」集合逐行 == 由"
        f"「标注文件的该题标签集合」+「第二节表的 `(L1,L2)`×`data_regime` → 桶号」映射"
        f"推出的桶集合（**这是 2b 新增的那一半**：旧形态靠「在几个桶里各抄一遍」隐式携带"
        f"桶归属，无从单独判）",
        f"**这一条的强度要说准（两半不一样）**：**配对相等那一半**两侧**同源于 `TAGS.md`**"
        f"（指针行是 `model_map.py` 从 TAGS 二层读回来的）⇒ 是「**一份数据、两份解析器**」："
        f"它能抓住生成器**漏抄/重抄**，**抓不住**两侧对 `TAGS.md` 格式的**共同误读**。"
        f"**真正两个数据源的只有桶归属那一半**（标注文件 × 第二节桶表；两向相等）。"
        f"⇒ 别把它读成「两侧完全独立」。",
        f"**期望被哪一类变异打红**（**本判据不点名变异编号**：编号↔判据的对账在证据文件的"
        f"封面表里，那张表由驱动器从它自己的变异清单生成）：删/增一个 `(篇, 模型)` 对 ⇒ "
        f"配对相等那一半；改错一行的「所属桶」⇒ 桶归属那一半。",
        f"**编号说明**：本条在 2a 里叫 `M-3`（那时判的是「逐桶展开」下的两向集合）。"
        f"2b 去重后，**同一个集合**改由去重行判，并**新增**桶归属；编号随之改为 `M-13`"
        f"（任务书 §二 判据表点名）。旧 `M-3` **不留别名**——留两个名字就会有人用错那个。",
    ])

    # ==================== M-4：指针可落地 ==================================
    tg_ptr = {(h["sid"], h["model"]): h for h in tags["hits"]}
    md_cache: dict[str, tuple[list[str], list[int]]] = {}
    m4_bad: list[str] = []
    n_ptr = 0
    for p in mv["ptr_rows"]:
        n_ptr += 1
        key = (p["sid"], p["model"])
        if key not in tg_ptr:
            m4_bad.append(f"{key} 在 TAGS 二层没有对应指针（幻影）")
            continue
        h = tg_ptr[key]
        if (p["md"], p["page"], p["snippet"]) != (h["md"], h["page"], h["snippet"]):
            m4_bad.append(f"{key} 的指针与 TAGS 二层不等——配对表 "
                          f"({p['md']}, p{p['page']}) vs TAGS ({h['md']}, p{h['page']})")
            continue
        if p["md"] not in md_cache:
            fp = ROOT / p["md"]
            if not fp.is_file():
                m4_bad.append(f"{key} 的 md 文件不在：{p['md']}")
                continue
            md_cache[p["md"]] = v_md_lines(fp)
        ls, pages = md_cache[p["md"]]
        if p["snippet"] not in ls:
            m4_bad.append(f"{key} 的片段不是 `{p['md']}` 的整行逐字："
                          f"{p['snippet'][:60]!r}")
            continue
        idx = ls.index(p["snippet"])
        if pages[idx] != p["page"]:
            m4_bad.append(f"{key} 的页码 p{p['page']} ≠ 该行所在页 "
                          f"p{pages[idx]}（片段在 {p['md']}）")
    add("M-4", not m4_bad, m4_bad[:20] or [
        f"**逐条落地**：{n_ptr} 条指针，每条都（已读 `{len(md_cache)}` 份 md）"
        f"① 与 TAGS 二层的 `(md 文件, 页码, 片段)` **逐字相等**；"
        f"② 片段是该 md 的**一整行**；③ 该行所在的页 == 指针的页",
        "**两个方向都判**：① 与 TAGS 不等 ⇒ 配对表自己编了指针；② 片段在 md 里定位不到 "
        "⇒ 指针悬空。md 是 **Task 3 的产物**（不由本任务生成），是这一条的独立参照。",
        "**为什么片段必须是整行**：`TAGS.md` 二层的契约就是「md 整行逐字」——"
        "片段只截前 30 字也能在 md 里 `grep` 到，但那样「指针错一位」就查不出来了。",
        "**2b 的形状变化**：上一版逐桶展开（同一对在几个桶里各一条），本版一条一行。"
        "**判据一字未放松**：条目数从 1644 条降到 496 条，但**要求没变**（逐条落地），"
        "而且去重后「一个对少了哪条指针」更容易被直接看出来。",
    ])

    # ==================== M-5：轴合法 ======================================
    m5_bad = []
    for b in mv["buckets"]:
        l1l2 = b["l1l2"]
        if " · " not in l1l2:
            m5_bad.append(f"桶 {b['idx']}：`(L1,L2)` 列 {l1l2!r} 不含 ` · `")
            continue
        for x in (y.strip() for y in l1l2.split(" · ", 1)):
            if x not in tax:
                m5_bad.append(f"桶 {b['idx']}：{x!r} 不在 `{PROBLEM_TYPES}` 里")
            for part in v_name_parts(x):
                q = re.sub(r"\s+", "", part).casefold()
                if q in vocab_norm:
                    m5_bad.append(f"桶 {b['idx']}：{x!r} 的成分 {part!r} == 词表词条/变体"
                                  f"（题型侧与模型侧必须不相交）")
        if b["regime"] not in V_REGIMES:
            m5_bad.append(f"桶 {b['idx']}：`data_regime` {b['regime']!r} 不在受控枚举里")
        if b["mark"] not in V_MARKS and "/".join(sorted(V_MARKS)) != b["mark"]:
            m5_bad.append(f"桶 {b['idx']}：标记列 {b['mark']!r} 不是 {V_MARKS} 的组合")
    # 桶表与逐桶指针小节**两边都要齐**（表里有桶、节里没指针 = 表在说空话）
    ids_tbl = [b["idx"] for b in mv["buckets"]]
    # **每个桶都必须有成员**：去重指针行的「所属桶」列里出现过的桶号集合，必须**恰好**等于
    # 桶表的编号集合（两向）。少了 ⇒ 桶表在说一个没有配对的桶；多了 ⇒ 桶表漏了一个桶。
    ids_ptr = {b for p in mv["ptr_rows"] for b in p["buckets"]}
    if set(ids_tbl) != ids_ptr:
        m5_bad.append(f"桶表编号集合 {sorted(set(ids_tbl))} ≠ 去重指针行「所属桶」列里出现过的"
                      f"编号集合 {sorted(ids_ptr)}——每个桶都必须有成员、每个成员都必须有桶")
    add("M-5", not m5_bad, m5_bad[:20] or [
        f"**{len(mv['buckets'])}** 个桶：`(L1,L2)` 两半都逐字命中 `{PROBLEM_TYPES}`"
        f"（{len(tax)} 个条目），整名与成分**都不与词表变体相等**（{len(vocab_norm)} 个）；"
        f"`data_regime` 逐桶 ∈ 受控枚举（{len(V_REGIMES)} 个值）；标记列合法；"
        f"桶表与逐桶指针小节的编号集合**一致**",
        "**为什么判「不相等」而不是「不包含」**：包含会把 `1 预测 ⊂ 灰色预测` 这类正确命名"
        "判成违规；本判据要拦的是「**标签名就是模型名**」——那一定表现为相等。",
        "**受控集合这一条守的是「轴」**：桶的两条轴必须都取自**受控枚举/分类法**，"
        "否则「题型 → 模型」的检索键就是自由文本，跨题不可比（用户要的匹配度也就无从谈起）。",
    ])

    # ==================== M-6：边界可机读且为等式 ==========================
    m6_bad = []
    cov = mv["cover"]
    if not cov:
        m6_bad.append("产物里没有可机读的覆盖边界行（找 `覆盖边界：`）")
    else:
        m = V_M_COVER.search(cov)
        if not m:
            m6_bad.append(f"覆盖边界行不合式：{cov[:160]!r}")
        else:
            n_ann, n_cov, n_unc = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
            want_years = "/".join(sorted({y for y, _p in tags_probs}))
            if m.group(4).strip() != want_years:
                m6_bad.append(f"覆盖年份={m.group(4).strip()!r} ≠ 独立重算的 {want_years!r}"
                              f"——「覆盖 2025」与「覆盖 2025/2026」不是同一条声明")
            listed = {tuple(x.strip().split(" ", 1)) for x in m.group(5).split("、")
                      if x.strip() and x.strip() != "（无）"}
            listed = {k for k in listed if len(k) == 2 and k[1]}
            want_unc = {(str(y), p) for (y, p) in ann} - set(tags_probs)
            if n_ann != len(ann):
                m6_bad.append(f"标注题数={n_ann} ≠ 本脚本独立解析的 {len(ann)}")
            if n_cov != len(tags_probs):
                m6_bad.append(f"有论文的题={n_cov} ≠ TAGS 一层的不同题数 {len(tags_probs)}")
            if n_unc != n_ann - n_cov:
                m6_bad.append(f"未配对的题={n_unc} ≠ {n_ann} − {n_cov} = {n_ann - n_cov}"
                              f"（**双边等式**：有论文的题 + 未配对的题 == 标注题数）")
            if listed != want_unc:
                m6_bad.append(f"逐题具名清单与独立重算不等：只在产物 "
                              f"{sorted(listed - want_unc)[:6] or '无'} · 只在重算 "
                              f"{sorted(want_unc - listed)[:6] or '无'}")
    add("M-6", not m6_bad, m6_bad or [
        f"**边界是等式**：{cov.strip()[:180]}",
        f"`有论文的题 + 未配对的题 == 标注题数`（{len(tags_probs)} + "
        f"{len(ann) - len(tags_probs)} == {len(ann)}），且**逐题具名清单**与"
        f"「标注里有、而 TAGS 一层没有」的独立重算集合**逐题对得上**（{len(ann) - len(tags_probs)} 道）",
        "**为什么必须具名+构成等式**：本表的覆盖面只有 2025 六题，其余 61 题**有题型、"
        "无配对**。写成「覆盖 2016–2026」或把 61 写成 60 都会红——「看起来更满」不是配对，"
        "是编造。",
    ])

    # ==================== M-7：无幻影 ======================================
    tg_sids = {sid for sid, _y, _p in tags["papers"]}
    m7_bad = []
    bad_sid_set = {p["sid"] for p in mv["ptr_rows"]} - tg_sids
    bad_sid = sorted(bad_sid_set)
    if bad_sid:
        m7_bad.append(f"配对表里出现了 TAGS 一层没有的稳定 ID：{bad_sid}")
    src_by_sid = {sid: (y, p) for sid, y, p in tags["papers"]}
    # 桶表每行的**来源题列**：① 每一题在 TAGS 一层里都有论文；② **当且仅当**该桶里有
    # 属于该题的指针行。这是「桶表 ↔ 去重指针行」在**来源题**这一栏上的两向一致。
    # **幻影 stable ID 不许把整条判据带崩**：`bad_sid` 已在上面登记成本条判据的具名 FAIL
    # （明细第一行就是那条）；这里**逐条跳过**它们再做自洽核对——旧写法在 2a 里直接
    # `src_by_sid[p["sid"]]` ⇒ `KeyError` ⇒ 异常逃出 `checks()` ⇒ 具名的 `M-7=FAIL` 与
    # 后面的 `M-8` 两行**根本没被打印**（读者只看到一段 traceback；退出码仍是 1，故那是
    # **可读性**缺口、不是 fail-open）。
    # **fail-closed 一点不减**：幻影 ID 仍让 `M-13` 红（两向集合不等）、退出码仍非 0。
    for b in mv["buckets"]:
        srcs = {tuple(x.strip().split(" ", 1)) for x in b["srcs"].split("、") if x.strip()}
        srcs = {k for k in srcs if len(k) == 2 and k[1]}
        members = [p for p in mv["ptr_rows"]
                   if b["idx"] in p["buckets"] and p["sid"] not in bad_sid_set]
        got_srcs = {src_by_sid[p["sid"]] for p in members}
        if got_srcs != srcs:
            m7_bad.append(f"桶 {b['idx']}：来源题列 {sorted(srcs)} ≠ 指针行反推的题 "
                          f"{sorted(got_srcs)}")
        for y, p in srcs:
            if (y, p) not in tags_probs:
                m7_bad.append(f"桶 {b['idx']}：来源题 {y} {p} 在 TAGS 一层里没有论文")
    # **桶表里的数字对账（论文数 / 对数 / 模型列）已移到 `M-2`**：2b 去重后它们由
    # 「所属桶」列**反推**得出（两向），比 2a 拿「逐桶指针」对账**更严**（反推是对**去重后
    # 的全集**做的，桶里少一行必红）。这一条是**搬迁不是放松**，逐字登记在
    # `tests/papers/recon/map-recon.txt` §14。
    # 第三节的低置信条目：逐条必须真的在 TAGS 二层里（**不藏也不编**）
    low_n = mv["low"][0] if mv["low"] else -1
    low_items = mv["low_items"]
    if low_n != len(low_items):
        m7_bad.append(f"第三节低置信条目：声明的条数 {low_n} ≠ 逐条列出的 {len(low_items)}")
    for model, sid, pg in low_items:
        h = tg_ptr.get((sid, model))
        if h is None:
            m7_bad.append(f"低置信条目 {model!r}@{sid} 在 TAGS 二层里没有")
        elif h["n_occ"] != 1 or f"p{h['page']}" != pg:
            m7_bad.append(f"低置信条目 {model!r}@{sid} {pg}：TAGS 里是 "
                          f"p{h['page']} / x{h['n_occ']}（口径是 `x1`）")
    add("M-7", not m7_bad, m7_bad[:20] or [
        f"**无幻影**：去重指针行里出现的稳定 ID "
        f"**{len({p['sid'] for p in mv['ptr_rows']})}** 个，全部 ∈ TAGS 一层的 {len(tg_sids)} 个；"
        f"每个桶的**来源题列**与「由「所属桶」列反推出来的题」**两向相等**；"
        f"每个来源题在 TAGS 一层里都有论文",
        f"第三节低置信条目 **{low_n}** 条（口径 `x1`）逐条都在 TAGS 二层里、页与次数都对得上；"
        f"零命中篇：本表 {mv['zero'][0] if mv['zero'] else '?'} 篇 == TAGS 第三层 "
        f"{tags['n_zero']} 篇",
        "**为什么这条是 fail-closed**：`MODEL_MAP` 是**派生**产物——它出现的任何 ID、任何"
        "来源题都必须能追回 `TAGS.md`；追不回去就是幻影（本项目「证据里不成立的语料断言」"
        "家族的形态）。",
        "**2b 的形状变化**：桶表里「论文数 / (模型,篇) 对 / 模型列」三栏的对账**移到 M-2**"
        "（去重后由「所属桶」列反推，两向）。本条保留「幻影」「来源题」「第三节诚实栏」三件；"
        "**搬迁不是放松**，逐字登记在 `tests/papers/recon/map-recon.txt` §14。",
    ])

    # ==================== M-8：重放一致性 ==================================
    from tools.papers import model_map as mm_mod
    scratch = rep.LIMITED_DIR / "map-products"
    res = mm_mod.build(COLLECTION, out_dir=scratch)
    fresh = (scratch / "MODEL_MAP.md").read_bytes()
    cur_bytes = map_p.read_bytes()
    loc_ok = res.map_path == scratch / "MODEL_MAP.md"
    add("M-8", fresh == cur_bytes and loc_ok and res.n_papers == len(tags["papers"]), [
        f"`model_map.build()` 重跑到不入库目录（`{rep.rel(scratch)}`）→ 与入库产物"
        f"**逐字节相同** = {fresh == cur_bytes}（{len(cur_bytes)} B）",
        f"落点断言：`ModelMapResult.map_path` == 本判据写的那个目录 = {loc_ok}"
        f"（**「写一处、读另一处」会让判据对着别的文件下结论**——`verify_ids.py` 的 I2 "
        f"就是这么防的）",
        f"自报量 `n_papers` = {res.n_papers}（与 TAGS 一层的 {len(tags['papers'])} 对照）· "
        f"`n_problems` = {res.n_problems} · `n_buckets` = {res.n_buckets} · "
        f"`n_pairs` = {res.n_pairs}",
        "**这一条抓两类事**：① 入库的那份是不是**生成器产出的**（手工订正会当场红——"
        "而 2b 会重跑这个生成器，手工订正会被冲掉、不订正又对不上）；"
        "② 生成器是不是确定的（同输入同字节）。",
    ])

    # ==================== M-9：召回分母口径 ================================
    # **参照侧**（作者自写）从 `keywords` 栏读；**命中侧**（我们算的）走词表匹配。
    # 两侧**不共用任何抽取代码**：这一侧只按分隔符拆词，那一侧走 `v_term_pattern`。
    kw_cell = tags["kw"]
    md_of = tags["md_of"]
    ref_ok = [sid for sid, _y, _p in tags["papers"] if kw_cell[sid] not in ("", EMPTY_CELL)]
    ref_absent: list[str] = []
    ref_unparsed: list[str] = []
    for sid, _y, _p in tags["papers"]:
        if kw_cell[sid] not in ("", EMPTY_CELL):
            continue
        md_text = (ROOT / md_of[sid]).read_bytes().decode("utf-8", "replace")
        (ref_unparsed if V_ANY_KEYWORD.search(md_text) else ref_absent).append(sid)
    cov_line = mv["cov"] or {}
    m9_bad = []
    if len(ref_ok) != 42:
        m9_bad.append(f"`keywords` 栏非空的篇数 {len(ref_ok)} ≠ 42")
    if len(ref_ok) + len(ref_absent) + len(ref_unparsed) != len(tags["papers"]):
        m9_bad.append("三态（有参照 / 参照不存在 / 参照存在但没解析出来）之和不等于 43"
                      "——三态必须**互斥且完备**")
    for key, want, label in (
            ("参照不存在", ref_absent, "参照不存在"),
            ("参照存在但没解析出来", ref_unparsed, "参照存在但没解析出来")):
        got = cov_line.get(key, "")
        parsed = [] if got in ("", "（无）") else [x for x in got.split("、") if x]
        if parsed != want:
            m9_bad.append(f"产物第四节的「{label}」清单 {parsed} ≠ 独立重算的 {want}"
                          f"——**这一格必须具名**，不许静默跳过、也不许写成「不适用」")
    if not ref_absent:
        m9_bad.append("「参照不存在」的清单为空——本语料实测有 1 篇（原文里 `key.?words?` "
                      "一次都不出现），空清单说明这一格没在报")
    add("M-9", not m9_bad, m9_bad or [
        f"**参照篇数 == 42**（`keywords` 栏非空；样本共 {len(tags['papers'])} 篇）；"
        f"**参照不存在 = {ref_absent}**（独立重算：该篇 md 里 `key.?words?` 零命中 ⇒ "
        f"**参照不存在**，不是「不适用」、不是静默跳过；产物第四节与证据都**具名**写着它）",
        f"**三态互斥且完备**：有参照 {len(ref_ok)} + 参照不存在 {len(ref_absent)} + "
        f"参照存在但没解析出来 {len(ref_unparsed)} == {len(tags['papers'])}"
        f"（后者实测 {len(ref_unparsed)} 篇：{ref_unparsed or '（无）'}——"
        f"「参照不存在」与「参照存在但没解析出来」是**两件事**，本判据分两栏判）",
        "**两个来源为什么不同**：参照侧 = 作者自己写的 `keywords` 栏，命中侧 = 受控词表的"
        "字面命中。`keywords` 栏的解析只做「按分隔符拆词」，**不调 `vocab`**——"
        "两侧共用抽取代码会让召回退化成「函数跟自己对答案」（本项目第七例）。",
        "**这条量的是分母的「大小」，不是分母的「来源」**：把召回的两侧改成调用同一个函数"
        "（换掉分母的来源）时，本判据**单独看仍是绿的**——那一类由 M-14（三方对账）与 "
        "M-10 抓。**别把这条读成「M-9 也证过两侧同源」**；这条边界逐字登记在 "
        "`recon/map-recon.txt` §14.9。",
    ])

    # ==================== M-10：未解释为 0 =================================
    # **独立重算**：用**基线**词表（git 对象库里的增长前字节）判每篇的片是否被覆盖。
    base_rows = v_vocab_rows(v_git_blob_bytes(BASELINE_MODELS_BLOB))
    triage = v_triage(ROOT / TRIAGE)
    # **第二张同格式表**（收口轮新增）：同一份解析、同一套规则。两张表的**词形集合必须互斥**
    # ——同一词形落两张表就等于「同一件事两处口径」，那正是本判据家族要拦的形态。
    body_triage = v_body_triage(ROOT / BODY_TRIAGE)
    tri_overlap = sorted({t[0] for t in triage} & {t[0] for t in body_triage})
    triage_all = triage + body_triage
    tri_map = {t[0]: t for t in triage_all}
    recov_uncovered: list[tuple[str, str]] = []      # (sid, piece) 判`模型`的
    recov_all_unc: list[tuple[str, str]] = []        # (sid, piece) 全部未覆盖片
    recov_cov = 0
    recov_model_entries = 0
    recov_collected = 0
    # 「分流表里**没有这一片**」这一类：**不许 `raise`**——`raise` 会让整轮在「判据汇总」
    # 之前结束，读者只看到一段 traceback，连 `M-10=FAIL` 那行都打不出来
    # （2a 在 M-7 的幻影 stable ID 上栽过同一形态：那是**可读性**缺口、不是 fail-open，
    # 但**具名诊断丢了**）。收集到这里，等 `m10_bad` 建好之后并进去。
    missing_triage: list[str] = []
    for sid, _y, _p in tags["papers"]:
        if kw_cell[sid] in ("", EMPTY_CELL):
            continue
        for piece in v_pieces(kw_cell[sid]):
            if v_covered(piece, base_rows):
                recov_cov += 1
                recov_model_entries += 1
                continue
            recov_all_unc.append((sid, piece))
            row = tri_map.get(piece)
            if row is None:
                missing_triage.append(
                    f"{sid} 的未覆盖片 {piece!r} **不在分流表里**——未解释项必须为 0")
                continue
            if row[2] == "模型":
                recov_uncovered.append((sid, piece))
                recov_model_entries += 1
                if row[1] == "收录":
                    recov_collected += 1
    ev_unc = [(s, p, d) for s, p, d in ev.get("_未覆盖清单", [])]
    prod_unc = [(s, p, d) for s, p, d in mv["cov_uncollected"]]
    m10_bad = list(missing_triage)
    # 证据的**两份清单合起来**才是「全部未覆盖模型条目」：`收录` 的进 `收录` 清单
    # （它们在增长后被覆盖了）、其余进 `未覆盖` 清单。判据要求**并集**与独立重算相等——
    # 这就是「未解释为 0」：每一条未覆盖的模型条目都必须在证据里有它的处置。
    ev_all = ({(s, p) for s, p, _d in ev_unc}
              | {(s, p) for _tag, s, p in ev.get("_收录清单", [])})
    if set(recov_uncovered) != ev_all:
        m10_bad.append(f"**独立重算**的未覆盖模型条目 vs 证据（未覆盖 + 收录两份清单的并集）："
                       f"只在重算 {sorted(set(recov_uncovered) - ev_all)[:6]} · 只在证据 "
                       f"{sorted(ev_all - set(recov_uncovered))[:6]}")
    if sorted(prod_unc) != sorted(ev_unc):
        m10_bad.append(f"产物第四节的未覆盖表 {sorted(prod_unc)[:6]} ≠ 证据的 "
                       f"{sorted(ev_unc)[:6]}（**两处必须同源**）")
    for sid, piece, disp in ev_unc:
        row = tri_map.get(piece)
        if row is None:
            m10_bad.append(f"证据里的未覆盖条目 {piece!r} 不在分流表里")
            continue
        if row[1] != disp:
            m10_bad.append(f"{piece!r}：证据里处置 {disp} ≠ 分流表的 {row[1]}")
        if not row[3].strip():
            m10_bad.append(f"{piece!r}：分流表的**理由为空**——未解释项就是它")
    named = "、".join(f"{s}:{p}" for s, p in sorted(set(recov_uncovered)))
    # **分流规则本身的合法性**（任务书 §3 的约束，逐行判）：
    #   `场景` ⇒ 处置**必须**是 `不收`（用户 2026-09-26 定案：场景不进模型词表）；
    #   `无法归类` ⇒ 处置**必须**是 `待定`（且理由要写明缺什么——理由非空已由上面判）。
    for piece, disp, cat, why in triage_all:
        if cat == "场景" and disp != "不收":
            m10_bad.append(f"{piece!r}：类别是`场景`、处置却是 {disp!r}"
                           f"——场景**只能**不收（用户 2026-09-26 定案）")
        if cat == "无法归类" and disp != "待定":
            m10_bad.append(f"{piece!r}：类别是`无法归类`、处置却是 {disp!r}"
                           f"——无法归类**只能**待定（并写明缺什么才能判）")
    if tri_overlap:
        m10_bad.append(f"两张分流表（`{TRIAGE}` / `{BODY_TRIAGE}`）的**词形集合不互斥**："
                       f"{tri_overlap} —— 同一个词形落两张表 = 同一件事两处口径")
    add("M-10", not m10_bad, m10_bad[:20] or [
        f"**未解释 = 0**：{len(ref_ok)} 篇的 `keywords` 片共 "
        f"{recov_cov + len(recov_all_unc)} 个（覆盖 {recov_cov} · 未覆盖 "
        f"{len(recov_all_unc)}），**每一个未覆盖片都在分流表里有一行**"
        f"（处置合法、理由非空）；其中判`模型`的 **{len(recov_uncovered)}** 条"
        f"（逐篇计，去重后 {len(set(recov_uncovered))} 种）**逐条点名**：",
        f"  {named}",
        f"**三态分布**：收录 {recov_collected} · 不收 {len(recov_uncovered) - recov_collected} "
        f"· 待定 0；**独立重算的集合 == 证据的清单 == 产物第四节的表**（三处两向相等）",
        f"**两张表的规模**（同一套规则判）：`{TRIAGE}` **{len(triage)}** 行"
        f"（窄 85 + 宽 27）· `{BODY_TRIAGE}` **{len(body_triage)}** 行"
        f"（正文扫描的跨篇复用 token：不收 "
        f"{sum(1 for t in body_triage if t[1] == '不收')} · 待定 "
        f"{sum(1 for t in body_triage if t[1] == '待定')} · 收录 "
        f"{sum(1 for t in body_triage if t[1] == '收录')}）。**两表的词形集合互斥**已判"
        f"（交叠 = ∅）——正文那张表**不进召回的分母**（分母只由 `keywords` 片构成），"
        f"它的用途是把「扫了但不可收」变成**逐条可核的处置**。",
        "**为什么这条不许看自称**：`未覆盖` 是**本脚本**拿基线词表逐片重算出来的，"
        "不是读产物里的数。产物把它写成 0 条，本判据会红。",
        "**分流规则的合法性也在这条判**：`场景` ⇒ 处置必须 `不收`、`无法归类` ⇒ 必须 `待定`"
        "（任务书 §3 的约束；用户 2026-09-26 定案「场景不进模型词表」）。"
        "**两张同格式表（`growth_triage` / `body_triage`）按这一套规则判**；两表的词形集合"
        "必须互斥（同一词形出现在两张表里 = 两处口径的开端）。",
        "**期望被哪一类变异打红**：把一条 `收录` 行的类别改成 `场景`（或反之）⇒ 这条当场红。"
        "（**本判据不点名变异编号**——编号↔判据的对账在证据文件的封面表里。）",
    ])

    # ==================== M-11：分流表可定位 ===============================
    tri_md_cache: dict[str, str] = {}
    m11_bad = []
    n_kw = n_kwseg = n_body = 0
    body_md_cache: dict[str, tuple[list[str], list[int]]] = {}
    for piece, disp, cat, why in triage_all:
        mloc = V_TRIAGE_LOC.match(why)
        mbody = None if mloc else V_BODY_LOC.match(why)
        if not mloc and not mbody:
            m11_bad.append(f"{piece!r} 的理由不以定位符开头"
                           f"（应 `kw:<ID> —` / `kwseg:<ID> —` / `body:<ID>@p<页> —`）："
                           f"{why[:40]!r}")
            continue
        if mbody:                       # **正文定位**：词形必须真出现在该篇 md 的第 <页> 页
            sid, page = mbody.group(1), int(mbody.group(2))
            if sid not in kw_cell:
                m11_bad.append(f"{piece!r} 的定位符指向 TAGS 一层里没有的 ID：{sid}")
                continue
            if sid not in body_md_cache:
                body_md_cache[sid] = v_md_lines(ROOT / md_of[sid])
            blines, bpages = body_md_cache[sid]
            pat = re.compile(rf"(?<![A-Za-z0-9]){re.escape(piece)}(?![A-Za-z0-9])")
            hit = [ln for ln, pg in zip(blines, bpages) if pg == page and pat.search(ln)]
            if not hit:
                m11_bad.append(f"{piece!r}（body:{sid}@p{page}）在该篇 md 的**第 {page} 页**"
                               f"里定位不到——正文定位模式判的是「这个词形真的出现在那一页」")
                continue
            n_body += 1
            continue
        mode, sid, _rest = mloc.group(1), mloc.group(2), mloc.group(3)
        if sid not in kw_cell:
            m11_bad.append(f"{piece!r} 的定位符指向 TAGS 一层里没有的 ID：{sid}")
            continue
        hay = kw_cell[sid] if mode == "kw" else None
        if mode == "kwseg":
            if sid not in tri_md_cache:
                tri_md_cache[sid] = v_kw_segment(
                    (ROOT / md_of[sid]).read_bytes().decode("utf-8", "replace"))
            hay = tri_md_cache[sid]
        if v_norm_locate(piece) not in v_norm_locate(hay):
            m11_bad.append(f"{piece!r}（{mode}:{sid}）在那一处**定位不到**——"
                           f"这条抓的是「分流表里编了一个作者没写过的词形」")
            continue
        n_kw += mode == "kw"
        n_kwseg += mode == "kwseg"
    add("M-11", not m11_bad, m11_bad[:20] or [
        f"**两张表共 {len(triage_all)} 行逐行可定位**：`kw:<ID>` **{n_kw}** 行（词形在该篇的 "
        f"`keywords` 栏里逐字命中）+ `kwseg:<ID>` **{n_kwseg}** 行（词形在该篇 md 的 "
        f"**Keywords 段**里逐字命中——段 = keywords 行 + 其续行，口径写死在分流表 §2）+ "
        f"`body:<ID>@p<页>` **{n_body}** 行（词形在该篇 md 的**第 <页> 页**里按词边界命中"
        f"——只出现在正文扫描那张表里，见该表 §1）",
        "**形态照 T2**：两侧都做「空白归一化后子串命中」。**每条都指名到「哪一篇」**"
        "（任务书原口径只要求「在 42 篇 keywords 栏的并集里能搜到」，本判据更严）。",
        "**为什么要有 `kwseg` 这条模式**：实测 `keywords` 栏是**行内截取**，本语料有 "
        "**17 篇**的作者 Keywords 段跨行 ⇒ 栏里少一截。只留 `kw` 会把作者**确实写了**的词形"
        "判成「编造的」（M-11 的反向误报）。这条加模式**不是放宽**：定位范围仍是"
        "**作者的 Keywords 段**（不是全文），且要求指名。",
    ])

    # ==================== M-12：词表合法 ===================================
    base_forms = v_vocab_forms(v_git_blob_bytes(BASELINE_MODELS_BLOB))
    cur_forms = v_vocab_forms((ROOT / MODELS).read_bytes())
    new_forms = cur_forms - base_forms
    # **两张表的 `收录` 行并起来**才是 M-12 的右侧（口径只有一处：两张表走同一份实现）。
    collected_forms = {t[0] for t in triage_all if t[1] == "收录"}
    m12_bad = []
    if new_forms - collected_forms:
        m12_bad.append(f"`models.txt` 新增了 **分流表里没有「收录」行**的词形："
                       f"{sorted(new_forms - collected_forms)}——「顺手多收」正是本条要拦的")
    if collected_forms - new_forms:
        m12_bad.append(f"分流表里「收录」了、而 `models.txt` 里**没有**的词形："
                       f"{sorted(collected_forms - new_forms)}")
    add("M-12", not m12_bad, m12_bad or [
        f"**两向相等**：`models.txt` 相对基线（`git cat-file blob "
        f"{BASELINE_MODELS_BLOB[:12]}…`，**增长前**的字节）新增 **{len(new_forms)}** 个词形 "
        f"== **两张分流表** `处置=收录` 的 **{len(collected_forms)}** 行（并集："
        f"`growth_triage` {sum(1 for t in triage if t[1] == '收录')} 行 + "
        f"`body_triage` {sum(1 for t in body_triage if t[1] == '收录')} 行；逐字相等，"
        f"**大小写算词形的一部分**——作者写的是 `Archard’s theory` 就收这个形态）",
        f"词表规模：基线 {len(base_forms)} 词形 → 现行 {len(cur_forms)} 词形",
        "**来源与两向**：每一条新增都能指出它的来源——**就是分流表那条「收录」行的理由**"
        "（`kw:<ID>` / `kwseg:<ID>` + 判类说明）。想把新词加进词表，**先往分流表加一行"
        "「收录」并给定位符**；反过来，往词表里顺手加一个分流表没有的词形会当场红。",
        "**为什么 `casefold` 不算相等**：本语料里 `Sustainable Tourism` 与 "
        "`Sustainable tourism` 是两行（作者的大小写不同）；`casefold` 会把它们压成一条，"
        "让「一个片找不到自己的分流行」这类真错被掩盖。",
    ])

    # ---- 精确性的**独立复核**（M-14 与 M-15 都要用）：命中侧 = `TAGS.md` 二层的每条指针。
    # md + 页 + 片段三条同时成立才算「可定位」。**这份复核是 M-15 的实体**，放在这里
    # 只是因为它同时喂 M-14 的三个键——两处**同一份**计算，不各算一遍。
    ptr_ok = 0
    ptr_bad: list[tuple[str, str, str]] = []
    md_cache2: dict[str, tuple[list[str], list[int]]] = {}
    for h in tags["hits"]:
        fp = ROOT / h["md"]
        if not fp.is_file():
            ptr_bad.append((h["sid"], h["model"], "md 不在"))
            continue
        if h["md"] not in md_cache2:
            md_cache2[h["md"]] = v_md_lines(fp)
        ls, pages = md_cache2[h["md"]]
        if h["snippet"] not in ls:
            ptr_bad.append((h["sid"], h["model"], "片段不是整行逐字"))
            continue
        i = ls.index(h["snippet"])
        if pages[i] != h["page"]:
            ptr_bad.append((h["sid"], h["model"], f"页 p{h['page']} ≠ p{pages[i]}"))
            continue
        ptr_ok += 1
    x1 = sorted((h["sid"], h["model"]) for h in tags["hits"] if h["n_occ"] == 1)

    # ==================== M-14：第四节与证据同源 ===========================
    # **三方对账**：产物第四节 / 证据文件 / 本脚本的独立重算。
    # 本脚本**不 import `coverage`**——它的解析是另写的一份（`v_pieces` / `v_covered` /
    # `v_kw_segment` / `v_vocab_rows` 全在本文件里）。
    # 宽口径（Keywords 段）：独立重算
    wide_cov = wide_den = 0
    for sid, _y, _p in tags["papers"]:
        if kw_cell[sid] in ("", EMPTY_CELL):
            continue
        seg = tri_md_cache.get(sid) or v_kw_segment(
            (ROOT / md_of[sid]).read_bytes().decode("utf-8", "replace"))
        tri_md_cache[sid] = seg
        wps = v_pieces(seg)
        wc = [x for x in wps if v_covered(x, base_rows)]
        wu = [x for x in wps if x not in wc and (tri_map.get(x) or ("", "", "", ""))[2] == "模型"]
        wide_cov += len(wc)
        wide_den += len(wc) + len(wu)
    recomputed = {
        "参照篇": str(len(ref_ok)),
        "参照不存在": "、".join(ref_absent) or "（无）",
        "参照存在但没解析出来": "、".join(ref_unparsed) or "（无）",
        "召回分子前": str(recov_cov),
        "召回分子后": str(recov_cov + recov_collected),
        "召回分母": str(recov_model_entries),
        "宽参照分子": str(wide_cov),
        "宽参照分母": str(wide_den),
        "未覆盖模型条目": str(len(recov_uncovered)),
        "未覆盖不收录": str(len(recov_uncovered) - recov_collected),
        "未解释": str(len(missing_triage)),
        "分流表行数": str(len(triage)),
        "分流表收录行数": str(len(collected_forms)),
        "收录条数": str(recov_collected),
        "精确性可定位": str(ptr_ok),
        "精确性总数": str(len(tags["hits"])),
        "低置信条数": str(len(x1)),
    }
    m14_bad = []
    for k, want in recomputed.items():
        a, b = cov_line.get(k), ev.get(k)
        if a is None:
            m14_bad.append(f"产物第四节的机读行里没有键 {k!r}")
        elif a != want:
            m14_bad.append(f"键 {k!r}：产物 {a!r} ≠ 独立重算 {want!r}")
        if b is None:
            m14_bad.append(f"证据文件里没有键 {k!r}")
        elif b != want:
            m14_bad.append(f"键 {k!r}：证据 {b!r} ≠ 独立重算 {want!r}")
    if set(cov_line) != set(recomputed):
        m14_bad.append(
            f"产物第四节的机读行**键集合**与独立重算的键集合不等："
            f"只在产物 {sorted(set(cov_line) - set(recomputed))} · "
            f"只在重算 {sorted(set(recomputed) - set(cov_line))}"
            f"（键集合本身是契约：少一个键就等于少一格对账）")
    add("M-14", not m14_bad, m14_bad[:20] or [
        f"**三方相等**（产物第四节 · 证据 · **本脚本独立重算**）：{len(recomputed)} 个键"
        f"逐个对账，**无一处不等**。核心三个：召回 {recomputed['召回分子前']} → "
        f"{recomputed['召回分子后']} / {recomputed['召回分母']}；"
        f"未覆盖模型条目 {recomputed['未覆盖模型条目']}（不收录 "
        f"{recomputed['未覆盖不收录']}）；宽参照 "
        f"{recomputed['宽参照分子']}/{recomputed['宽参照分母']}",
        "**为什么是三方而不是两方**：产物与证据**同源**（同一次 `coverage.compute()`），"
        "两边都改错、或一边手抄错，两方对账**抓不到**。第三方是本脚本自己的一份实现"
        "（另一份拆词、另一份定位、另一份词表读取），三方同时错到一块去才会假绿。",
        "**本判据不调 `coverage` 的任何函数**（也不调 `vocab`）：一旦共用，这条就退化成"
        "「函数跟自己对答案」（本项目第七例）。",
    ])

    # ==================== M-15：精确性 =====================================
    # `ptr_ok` / `ptr_bad` / `x1` 已在 M-14 之前算好（同一份计算，两处共用）。
    m15_bad = []
    for k_src, val in (("精确性可定位", str(ptr_ok)), ("精确性总数", str(len(tags["hits"]))),
                       ("低置信条数", str(len(x1)))):
        if cov_line.get(k_src) != val:
            m15_bad.append(f"产物第四节的 {k_src}：{cov_line.get(k_src)!r} ≠ 独立复核 {val!r}")
        if ev.get(k_src) != val:
            m15_bad.append(f"证据的 {k_src}：{ev.get(k_src)!r} ≠ 独立复核 {val!r}")
    if mv["low"] is None:
        m15_bad.append("第三节没有可机读的低置信计数行")
    else:
        if mv["low"][0] != len(mv["low_items"]):
            m15_bad.append(f"第三节低置信：声明 {mv['low'][0]} 条 ≠ 逐条列出 "
                           f"{len(mv['low_items'])} 条")
        if not mv["low_items"]:
            m15_bad.append("第三节的低置信清单**为空**——本语料实测有 "
                           f"{len(x1)} 条 `x1`，空清单说明它没在报")
        got_low = sorted((sid, m) for m, sid, _p in mv["low_items"])
        if got_low != x1:
            m15_bad.append(f"第三节的低置信清单与独立重算的 `x1` 集合不等："
                           f"只在产物 {sorted(set(got_low) - set(x1))[:4]} · "
                           f"只在重算 {sorted(set(x1) - set(got_low))[:4]}")
    if ptr_bad:
        m15_bad.append(f"有 {len(ptr_bad)} 条命中**不能定位**：{ptr_bad[:4]}")
    add("M-15", not m15_bad, m15_bad[:20] or [
        f"**精确性 {ptr_ok}/{len(tags['hits'])}**：`TAGS.md` 二层每条指针的 "
        f"`(md 文件, 页码, 片段是该 md 的整行逐字)` **逐条复核**（读回 {len(md_cache2)} 份 md）"
        f"——这是 Task 6 已有的指针，本判据**只复核、不重算**",
        f"**低置信（`x1`）单列且不为空**：**{len(x1)}** 条，第三节的逐条清单与独立重算的 "
        f"`x1` 集合**两向相等**",
        "**「可定位」不等于「用对了」**：它证明的是「这个片段确实在那篇的那一页那一行」，"
        "**证明不了**「作者在那里把它当模型名用」。后者是语义判断，本判据不出具（那正是"
        "「不得声称任何目视确认」这条纪律的落点）。",
        "**「不为空」是实测事实、不是阈值**：本语料 43 篇里 `x1` 有 "
        f"{len(x1)} 条。**若将来它变成 0，本判据会红——那是故意的**：空清单与「这一格没在报」"
        "在文本产物里同形，逼下一个人来改这一条而不是让它静默变成空表。",
    ])

    # ==================== M-16：R1 真收口（默认路径）======================
    # R1 原文（`recon/ids-recon.txt` 编者按）：`I13-b` 的探针**只覆盖显式路径**
    # `vocab.load(path)`；**默认路径 `load()` 的缓存不被覆盖** —— 而用户承诺的
    # 「往词表追加即生效」针对的**正是默认路径** ⇒ 一个只给默认路径加缓存的实现会绿着过。
    # 本判据就是那一格：在**系统临时目录**上把 `vocab.DEFAULT` 指过去，然后调 **`load()`**
    # （**不带参数**）——读 1 条 → 追加 1 行 → **同一进程内**再 `load()` 必须读到 2 条。
    # **不碰任何入库文件**（临时目录跑完即删；`vocab.DEFAULT` 在 finally 里还原）。
    import tempfile
    from tools.papers import vocab as vocab_mod
    m16_bad = []
    n_def = (-1, -1)
    orig_default = vocab_mod.DEFAULT
    try:
        with tempfile.TemporaryDirectory(prefix="verify-map-vocab-default-") as td:
            tv = Path(td) / "models.txt"
            tv.write_bytes(b"probe alpha | probe alpha variant\n")
            vocab_mod.DEFAULT = tv
            n1 = len(vocab_mod.load())                       # **不带参数 = 默认路径**
            tv.write_bytes(tv.read_bytes() + b"probe beta | probe beta variant\n")
            n2 = len(vocab_mod.load())                       # 同一进程内再读默认路径
            n_def = (n1, n2)
        if n_def != (1, 2):
            m16_bad.append(
                f"**默认路径**探针：`load()` 首读 {n_def[0]} 条（应 1）、追加一行后同一进程内"
                f"再 `load()` {n_def[1]} 条（应 2）——**默认路径上「追加即生效」不成立**")
    except Exception as e:               # noqa: BLE001 —— 探针抛错本身就是 FAIL
        m16_bad.append(f"默认路径探针抛错：{type(e).__name__}: {rep.scrub(str(e))}")
    finally:
        vocab_mod.DEFAULT = orig_default
    add("M-16", not m16_bad, m16_bad or [
        "**R1 真收口**：探针走的是**默认路径** `vocab.load()`（**不带参数**）——"
        "先 1 条 → 追加 1 行 → 同一进程内再读 ⇒ 要求 **1 / 2**",
        f"实测 首读 **{n_def[0]}** 条 / 追加后 **{n_def[1]}** 条 ⇒ 默认路径上「追加即生效」成立",
        "**它比 `I13-b` 多覆盖什么**：`I13-b` 走的是**显式路径** `vocab.load(path)`。"
        "用户承诺的「往词表追加即生效」针对的是**默认路径**——`models.txt` 就是默认路径那份。"
        "所以「只给默认路径加缓存」的实现能绿着过 `I13-b`，却过不了本条。"
        "**期望被哪一类变异打红**：给**默认路径**加模块级缓存（只给默认路径）那一类；"
        "该形态已实测会红（**本判据不点名变异编号**——编号↔判据的对账在证据文件的封面表里）。",
        "**R2（按文件内容哈希缓存）本条抓不到**：那种缓存的键是**内容**，追加一行内容就变、"
        "缓存自然失效 ⇒ **它不破坏承诺**。本条只抓「按路径/按默认参数缓存」这一类"
        "（它们才破坏承诺）。这条边界逐字登记在 `recon/map-recon.txt` §14。",
    ])

    # ---- 报告量 -----------------------------------------------------------
    lines.append(f"  桶数 {len(mv['buckets'])} · (模型,篇) 对 {len(mv_pairs)} · "
                 f"指针行 {n_ptr} · md 读回 {len(md_cache)} 份 · "
                 f"TAGS 三层零命中 {tags['n_zero']} 篇")
    lines.append("  覆盖：2025 A–F 共 6 题 / 43 篇；未配对 61 题（见覆盖边界行）")
    lines.append(f"  匹配度：参照篇 {len(ref_ok)}（参照不存在 {ref_absent or '（无）'}）· "
                 f"召回 {recov_cov} → {recov_cov + recov_collected} / {recov_model_entries}"
                 f"（{recov_cov / recov_model_entries:.4f} → "
                 f"{(recov_cov + recov_collected) / recov_model_entries:.4f}）· "
                 f"精确性 {ptr_ok}/{len(tags['hits'])} · 低置信 {len(x1)} 条")
    lines.append("=" * 78)
    lines.append(f"判据汇总：{'全部通过' if ok else '**有 FAIL**'}"
                 f"（所有差额逐条具名登记见上，**未解释为 0**）")
    return ok


def main() -> int:
    import argparse as _ap

    from tools.papers import report

    ap = _ap.ArgumentParser(
        description="题型 → 模型/算法 配对表 + 匹配度判据 M-1…M-16（corpus/papers/MODEL_MAP.md）",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="**只改报告落点并跳过 M-1-b**（本脚本的判据不取样，见模块 docstring）；"
             "报告写到 tests/papers/reports-limited/（不入库）；0 = 全量（默认，写放行证据 "
             "tests/papers/reports/map-report.txt）；负数不接受。",
    )
    args = ap.parse_args()

    out, guard_msg = report.resolve_report("map", args.limit)
    pre = report.sha256_of(report.release_path("map")) if args.limit > 0 else ""

    meta: dict = {"n_sample": 0, "n_all": 0}
    lines = ["题型 → 模型/算法 配对表判据（M-1…M-16）· Task 6b 阶段 2b"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out, report)
    except BaseException as e:            # noqa: BLE001 —— 任何异常都算 FAIL
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    out, msg2 = report.recheck_target("map", args.limit, out)
    if msg2:
        lines.append(msg2)
    if guard_msg or msg2:
        ok = False

    lines.append("")
    lines.append(f"写入：{report.rel(out)}")
    if args.limit > 0:
        lines.append(
            f"  本文件是**限样本跑**（--limit {args.limit}）的报告，**不入库、不是放行依据**；"
            f"放行证据是 {report.rel(report.release_path('map'))}，只有全量跑会写它。")
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）；限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件。")

    text = "\n".join(lines) + "\n"
    if args.limit > 0:
        post = report.sha256_of(report.release_path("map"))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· "
            f"{report.rel(report.release_path('map'))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    # RESULT 行。**不用 `report.result_suffix`**：那个函数按「前 N 份 + 见证集」描述样本，
    # 而本脚本**不取样**（输入是两份文本产物）——照抄会把「不取样」说成「取样」，那是假陈述。
    # 语义与它一致：**只有全量跑才可能出现裸 `RESULT: PASS`**。
    suffix = "" if args.limit <= 0 else (
        f" (LIMITED --limit {args.limit}；**本脚本不取样**：M-1…M-16 全量口径，"
        f"`--limit` 只改报告落点并跳过 M-1-b；非放行依据)")
    text += f"\nRESULT: {'PASS' if ok else 'FAIL'}{suffix}\n"
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
