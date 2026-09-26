"""公式裁图与编号/引述句（Task 5）。**无 OCR、不转 LaTeX**——只做「认出编号 → 裁图」。

本任务不把公式转成 LaTeX（spec §1），所以「这份论文有几条编号公式」这个数**就是
交付物本身**：M2 将来按它取"表述方式"。**数错了就是交付物错了。**

## 检测器（结构性、不截断）——推导与失败条件

### 候选：**行尾编号 token**（不使用任何坐标比例/常量）

一条候选 = 某个文本行，其**行尾**匹配 `\\(\\s*(\\d{1,2})\\s*\\)\\s*$`。**不用任何坐标、比例或页宽常量。**

* **为什么可以不用"靠右"**（这是本任务要修的旧判据，实测依据）：
  计划草稿用 `x1 >= 页宽 - 0.15*页宽` 判"靠右"。实测 `2517690` 页宽 595.3 → 阈值 506.0，
  而该篇 (2)–(10) 的**真实且严格递增**的编号 x1 = 498.0–502.9（该页文本栏右缘 529.5，
  编号距栏右缘 27.8–46.6pt）——**差 3–8 点落在阈值外**，于是链在第 1 条就断、全篇只报
  1 条（真值 21）。同类：`2504188` 0/32、`2517273` 1/41、`2500759` 3/7、`2502355` 12/34。
  「靠右」在这里连"文本栏相对"都不成立（那 9 条在栏内 28–47pt 处）。删掉这条约束的
  代价实测为 **0**：43 份的候选集里**没有一条真编号**因坐标被误剔（`2517690` 的 21 条
  全数入链），而被它拦下的那 82 条（R3 = 661 与 R1 = 743 之差）逐条看**全是真编号**。
* **为什么候选要允许括号内空格**：实测 `2508861` 全篇编号排版成 `( 1 )`（括号与数字
  之间有空格，PyMuPDF 逐 span 可见）。按"括号内不得有空白"的严格口径，该篇 md 侧
  纯编号行 = **0**、pdftotext 行尾 = 9，而它实际有 **29** 条编号公式（p6–p21，逐条可复算）。
  即：**严格口径的参照在这一篇上是漏的**，不是"没有公式"。
* **为什么候选用"行尾"而不是"整行只有编号"**：实测有 **6 份论文、共 11 条**编号与公式体
  排在**同一文本行**（`2504223` 3 条、`2517199` 3 条、`2517273` 2 条、`2501869` 1 条、
  `2507692` 1 条、`2508861` 1 条）。只认"整行只有编号"会漏掉这 11 条真编号
  （例：`2508861` p9 y=79.6 的行 `'𝑓𝑓𝑓𝑓𝑓𝑓𝑃𝑃wheats −𝑑𝑑𝑃𝑃𝑃𝑃, ( 6 )  '`）。
  **复算**：`python - <<PY` 逐篇 `formulas.scan(doc).picks` 里 `score == 1` 的那些
  ——总数 11，逐条坐标见 `tests/papers/recon/formula-recon.txt` §八。
  （⚠️ 本 docstring 早先写「**9 份**论文…`2516695`/`2516219`/`2524070` 各若干」，
  本轮逐条复算**不成立**：那三篇一条 `score == 1` 的检出都没有——旧话是未复算的声称，
  本轮改掉。）

### 链：**严格递增 + 有界跳号**（保留剔噪意图，但**不截断**）

候选按 (页, y0, x0) 排序后逐个走：`num >= last + 1` **且** `num - last <= GAP_MAX` 才入链，
否则**只剔除该候选、`last` 不动**，继续看下一个。

* 旧实现是 `num == last + 1`，**一处不符即永久停止收链**：一个候选被误剔就截断全篇
  （`2517690` 1/21、`2502355` 12/34 …）。本实现把"断一处即全弃"换成"逐候选判、逐候选剔"，
  于是**单个候选被剔除不可能截断全篇**——这是本任务书约束 A 的第二条。
* `GAP_MAX = 10` **是量出来的**：全 43 份入链序列里**最大跳号 = 4**（`2504223`，
  该篇编号 1–8 后跳到 13；md 侧与 pdftotext 侧都复算出同一个 4，故它是语料事实）。
  取 10 = 2.5 倍余量。它实际拦下的是两条**语料侧非编号**：`2501869` p11 的
  `'Countries with at least 3 medals(56)'`（跳 48）与 `2513705` p8 的正文句尾 `(20)`（跳 20）。
* **失败条件（这条链抓不住什么）**：
  1. 若某篇的编号**回退**（如正文里出现更小的编号且位置在先），链会把它算作噪声剔除；
     实测 43 份未出现该形态，但**未证否**。
  2. 若一篇里有**两条不同公式共用同一编号**（真重号），第二条必被剔。实测 43 份里的
     "重号"逐条复核**全部**是语料侧非编号（清单见 `tests/papers/recon/formula-recon.txt`）。
  3. 若某篇的编号**整体不从 1 开始**（实测 `2504188` 从 4 开始：p8 起 (4)–(35)，md 与
     pdftotext 两侧一致），链不要求从 1 起，故不受影响。

### 代表：同一编号只留一条，按结构分选

链定的是**编号集合**；同一编号可能有多个候选（真编号 + 语料侧噪声行尾）。代表取
`(score, 页, y0, x0)` 最小者，`score` 由**该行自己的文本**决定：
`0 = 整行只有编号` > `1 = 编号在行尾（行内还有别的文本）`。
实测它是必需的：`2501869` 的正文行 `'Task 1 Develop an Olympic medal prediction model
using historical data to forecast: (1)'` 与真编号 `(1)`（p8 y=160.5，整行只有编号）
**同号**，只按先后会留下前者、裁到正文而不是公式。

### 产出

`<out_dir>/eq-NN-pP.png`（NN = 编号，P = 页码，1 起）+ 同名 `.context`。

`.context` 内容（逐行，LF）——**口径**：
```
REF: (N)                  编号行本身（规范形式；原件里可能是 `( N )`）
SRC: 行原文（空白归一化）  该编号在原件里的那一行，逐字
WHERE: …                  该式的 where 引述句（逐字，空白归一化），可 0..n 行
CITE: …                   显式引用该式的句子（`Eq. (N)` / `Equation (N)`），可 0..n 行
```
* **where 句归属口径**：一条以 `where` 开头（`^\\s*where\\b`，不分大小写）的文本行归属
  到"**位置在它之前、最近的那条检出编号**"（按 (页, y0) 全局排序）。这是结构性的
  （该语料里 where 段紧跟公式之后），但**它是一条先验**：若某篇把 where 段写在公式之前，
  会归错式——实测 43 份未出现，登记为已知边界。
* **n_refs 口径**：= **写进 `.context` 的 `CITE:` 行条数**，即"引用某个**已检出编号**的
  `Eq./Equation (N)` 出现次数"。另有两个覆盖指标（不参与判定）：`n_cite_all` = 原件全文
  里该模式的**全部**出现次数（含引用了未检出编号的），`n_where` = WHERE 行条数。
  与 md 侧参照（`tests/papers/recon/formula-recon.txt`：40 处 / 11 份）**同一条正则**
  `\\b(?:Eq\\.?|Equation)\\s*\\(\\s*(\\d{1,2})\\s*\\)`（不分大小写），故两侧可比。

### 水印（机制层）

`extract_all` 在**任何 `get_pixmap` 之前**调 `watermark.strip_in_memory(doc)`（与
`figures.extract_all` 同源）。`equation_numbers` **自己不 strip**——它要求调用方先
strip 过（同 `figures.caption_blocks` 的约定）。这不是洁癖：若它内部自行 strip，
把 `extract_all` 里那一句删掉（变异 M3）也不会让水印进 PNG，D3 就没有区分力了。

### 已知边界（如实登记，不声称解决）

1. **裁图"内容框对了没有"无判据覆盖**——本模块只按版面实物的重叠/间隙机械地定带，
   没有任何机器判据能证明框住的就是那条公式（`verify_d.py` 的 D1 只数条数，D1-a 更是
   恒真）。见 `docs/mcm-suite-todo.md` §D 第 10 条的公式版。
2. **裁图带不能复用 `figures.band_of`**（实测 **331/782** 条定不出带，理由与替代取法
   逐条写在 `formula_band` 的 docstring 里）；改用的是 `figures` 的**同一套量**
   （`_page_items` / `_is_flow_text` / `_line_scale` / `GAP_PITCH_MULT`）加一个
   `REACH_PITCH_MULT`（取值表在同一处）。新旧两种取法的高度分布差异**逐份、两组并列**
   印在 `d-report.txt`（实测：新取法逐份 min 最低 10.6 / 逐份 max 最高 78.5pt，
   逐份中位的中位 34.3pt；固定点法（草稿 `y0-6/y1+6`）逐份 min 最低 22.0 /
   逐份 max 最高 35.5pt，逐份中位的中位 24.0pt）。
   ⚠️ **「逐份中位的中位」的取法要写明**（复审 Minor 5）：34.3 与 24.0 用的是
   **上中位数**（把逐份的中位数排序后取第 `n//2` 个）；用 `statistics.median`
   （偶数个取中间两个的平均）复算得到的是 **34.22** 与 **23.96**（用**未舍入**的逐份中位数，
   §F 逐字）——两者**不相等**就是这个取法差异造成的。**两种取法都印在
   `formula-band-scans.txt` §F**，别混用。
   **三组数的复算脚本与逐字输出**：`tests/papers/recon/formula-band-scan.py` →
   `tests/papers/recon/formula-band-scans.txt`（入库；本 docstring 里所有实测数都指向它）。
3. **`formula_band` 退化的条数**（= 没吸收到任何非正文实物、且编号行是"整行只有编号"）
   实测 **7/782**，在报告里逐份印出；那些条仍产出图（保证"检出多少条就产出多少张"，
   与 D1-a 的形状一致），但**它裁的是不是公式就不知道**。
4. **带可能圈进页眉/页脚**：可达域取 2.0 倍行距时实测 **2/782** 条带把 `Team #…` /
   `Page N of M` 那类页眉行也圈了进去（取 2.5 倍时涨到 **8** 条、3.0 倍 **12** 条，
   见 `REACH_PITCH_MULT`；逐条清单在 `formula-band-scans.txt` §C）。
   这是"宁可多收一点"的代价，逐条可复算（按页眉文本匹配），登记在此。
5. **带高不足 1.2 倍行距的续行不会被吸收**——多行公式的续行可能被切掉（取法刻意保守，
   见 `formula_band` 的失败条件）。**没有判据覆盖**，与第 1 条同属裁图质量那一族。
"""
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import fitz

from . import figures, watermark

# 行尾编号 token。**括号内允许空白**（`( 1 )`），理由见模块 docstring。
NUM_TOKEN = re.compile(r"\(\s*(\d{1,2})\s*\)\s*$")
# 编号的下界。**取 0，不取 1**——理由是实测的，不是宽松：
# `2507817` p6 y=80.3 `x0=509.3 x1=526.4` 有一条**整行只有 `(0)`** 的行，位置与全篇其它
# 编号**完全相同**（右缘、另一侧是公式碎片），是该篇的编号 (0)。若把它按"编号从 1 起"
# 拒掉，R1=21 与检出=20 之间就出现一条**用语料侧解释不了**的差额——那是检测器自己的
# 取舍，任务书二节明令**不算解释**（记「未解释」并判 FAIL）。链的起点因此取 `last = -1`。
# 反过来，`β(0)` / `θ(0)` 这类**行内**的 `(0)` 不是编号，链会用「回退/重号」把它们剔掉
# （它们的行文本里紧贴前面的字符是字母，实测 `2516695` p9、`2524070` p9）。
#
# **`781` 与 `782` 的差就是这一条**：docstring 里早先出现过 `781` 这个分母，那是
# `MIN_NUM = 1`（把上面那条 `(0)` 排除）那一版的检出总数；现行 `MIN_NUM = 0` 下是
# **782**（`782 − 781 = 1`，差的正是 `2507817` 的 `(0)`）。复算见
# `tests/papers/recon/formula-band-scans.txt` §D。
MIN_NUM = 0
# 链的起点值：`num >= last + MIN_STEP`。取 -1 使"首条是 (0)"可以入链（见 MIN_NUM）。
CHAIN_START = -1
# 入链允许的最大跳号。量出来的上限是 4，取 10。见模块 docstring「链」一节。
GAP_MAX = 10
# 显式引用（`Eq. (N)` / `Equation (N)`）。**与参照侧同一条正则**。
CITE_RX = re.compile(r"\b(?:Eq\.?|Equation)\s*\(\s*(\d{1,2})\s*\)", re.I)
# where 引述句。
WHERE_RX = re.compile(r"^\s*where\b", re.I)
# 可达域：实物必须落在「编号行 ± 本倍数 × 本页行距」之内才可能被吸收。
# 行距由 `figures._line_scale` **逐页量**（不是全局常量）。
#
# 取值的实测依据（全 43 份 **782** 条上逐条量过，五个候选值的对照）。
# **复算脚本 + 逐字输出已入库**：`tests/papers/recon/formula-band-scan.py` →
# `tests/papers/recon/formula-band-scans.txt` §B/§C（这是这几组数**唯一的**依据；
# 旧版本把这些数只写在注释里，等于无法核）。
#
# | 倍数 | 退化条数 | 带高中位 | 带高最大 | 吞进页眉/页脚的带 |
# | :--- | :--- | :--- | :--- | :--- |
# | 1.2（= `figures.GAP_PITCH_MULT`） | 26 | 29.1 | 52.0 | 0 |
# | 1.5 | 14 | 30.9 | 63.1 | 1 |
# | **2.0** | **7** | **34.6** | **78.5** | **2** |
# | 2.5 | 7 | 40.4 | 94.2 | 8 |
# | 3.0 | 7 | 45.8 | 107.3 | 12 |
#
# 1.2 倍（直接沿用 `figures` 的值）不可用：退化 26 条（1.5 是 14，2.0 已经到底的 7），
# 其中 `2504223` 一篇就占 13 条——该篇是多行展示式，续行距编号行 ~21pt，而该页行距 12pt。
# 2.0 是**退化条数已经到底（7）而误收页眉还没涨起来（2）**的那一档；再放大只有副作用。
#
# ⚠️ **旧表与实测的两处不符**（本轮复算发现，逐条见 `formula-band-scans.txt` §E）：
#   1. 旧表 1.2 那一格写 **223**：那是**旧口径**（`带高 < MIN_BAND=20pt` 也算退化）下的数
#      ——那个分支已被 `formula_band` 刻意删除，现行代码上同口径复算得 231，仍差 8。
#      本表改用**现行口径**的 26。
#   2. 旧表 2.5 / 3.0 的「吞页眉」写 7 / 11：实测 **8 / 12**（逐条清单见 §C，两份差异
#      都在 `2517273` 的页眉上）。
REACH_PITCH_MULT = 2.0


def nospace(s: str) -> str:
    """空白归一化：把**所有**空白（含 U+00A0 等 Unicode 空白）删掉。

    md 是 `textmd` 重排出来的产物，逐字原样常常对不上（换行位置、连字符都变过），
    故「引述句能在 md 中定位」这条判据一律在**本函数的像里**做。口径写死在这里、
    由 `verify_d.py` 与报告共用，避免两处各写一个归一化。
    """
    return re.sub(r"\s+", "", s)


@dataclass(frozen=True)
class EqNum:
    """一条编号公式的**编号**在原件里的位置。字段是任务书钉死的接口。"""
    num: int
    page: int     # 0 起
    x0: float
    y0: float
    y1: float


@dataclass(frozen=True)
class Candidate:
    """一个候选：某一行的行尾编号 token。"""
    num: int
    page: int
    bbox: tuple[float, float, float, float]   # 整行的 x0,y0,x1,y1
    text: str                                  # 整行的原文（已 strip）
    score: int                                 # 0 = 整行只有编号；1 = 编号在行尾

    def as_eqnum(self) -> EqNum:
        return EqNum(self.num, self.page, self.bbox[0], self.bbox[1], self.bbox[3])


@dataclass
class Scan:
    """一次扫描的**全部机械量**（候选数 / 入链数 / 被剔除数及其原因）。

    报告里必须印这三样（任务书约束 A）：只报"检出多少条"的话，"丢了多少、为什么丢"
    就无从核对。
    """
    cands: tuple[Candidate, ...]
    accepted: tuple[Candidate, ...]                 # 链上被接受的候选（未选代表）
    rejected: tuple[tuple[Candidate, str], ...]     # (候选, 被剔理由)
    picks: tuple[Candidate, ...]                    # 代表：每个入链编号一条

    @property
    def numbers(self) -> list[int]:
        return [c.num for c in self.picks]


@dataclass
class EqResult:
    """抽取结果。

    任务书钉死的是 `n_eq` / `n_refs` 两个字段；其余字段**都带默认值**，故那两个的
    用法不变（同 `figures.FigResult` 的处置）。它们的作用是让 `verify_d.py` 能对账：
    `n_stripped` 是 D3 的分叉 tripwire、`n_cand`/`n_rejected` 是约束 A 要求报告的
    「候选数 / 入链数 / 被剔除数」、`cite_all`/`n_where` 是 n_refs 的覆盖指标。
    """
    n_eq: int
    n_refs: int
    n_stripped: int = 0
    n_cand: int = 0
    n_rejected: int = 0
    n_where: int = 0
    n_cite_all: int = 0
    n_band_fallback: int = 0


def _line_texts(doc: fitz.Document) -> list[tuple[int, tuple, str]]:
    """全篇文本行 → `[(页, bbox, 原文)]`，与 `figures._page_items` 同粒度（按 line）。"""
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"])
                if t.strip():
                    out.append((pno, tuple(line["bbox"]), t))
    return out


def scan(doc: fitz.Document) -> Scan:
    """候选 → 链 → 代表。**要求调用方已经 `strip_in_memory` 过**。

    水印 Form XObject 的文本块（实测 72pt、跨半页）会混进文本行列表；不 strip 的话
    它可能被算成候选（它的文字不含行尾编号，故实测不产生候选，但那是运气，不是保证）。
    """
    cands: list[Candidate] = []
    for pno, bbox, text in _line_texts(doc):
        m = NUM_TOKEN.search(text)
        if not m:
            continue
        num = int(m.group(1))
        if num < MIN_NUM:
            continue
        stripped = text.strip()
        token = m.group(0).strip()
        cands.append(Candidate(
            num=num, page=pno, bbox=bbox, text=stripped,
            score=0 if stripped == token else 1,
        ))
    cands.sort(key=lambda c: (c.page, c.bbox[1], c.bbox[0]))

    accepted: list[Candidate] = []
    rejected: list[tuple[Candidate, str]] = []
    last = CHAIN_START
    for c in cands:
        if c.num >= last + 1 and c.num - last <= GAP_MAX:
            accepted.append(c)
            last = c.num
        elif c.num <= last:
            rejected.append((c, f"编号 {c.num} <= 已入链最大 {last}（回退/重号）"))
        else:
            rejected.append((c, f"跳号 {c.num} - {last} = {c.num - last} > GAP_MAX={GAP_MAX}"))

    # 代表：同一编号按 (score, 页, y0, x0) 取最优。**候选集里所有同号者都参与**——
    # 被链剔掉的重号候选也可能是**真编号**（`2501869` p8 的 `(1)` 就是：正文行里的
    # 列表序号占了这个号，真编号被链判成重号剔除）。只挑"结构上更像编号行"的那条。
    best: dict[int, Candidate] = {}
    for c in cands:
        k = (c.score, c.page, c.bbox[1], c.bbox[0])
        cur = best.get(c.num)
        if cur is None or k < (cur.score, cur.page, cur.bbox[1], cur.bbox[0]):
            best[c.num] = c
    nums = {c.num for c in accepted}
    picks = sorted((v for n, v in best.items() if n in nums),
                   key=lambda c: (c.page, c.bbox[1], c.bbox[0]))
    return Scan(tuple(cands), tuple(accepted), tuple(rejected), tuple(picks))


def equation_numbers(doc: fitz.Document) -> list[EqNum]:
    """检出该文档的公式编号（每号一条）。

    **不做 strip**——调用方必须先 `watermark.strip_in_memory(doc)`（见模块 docstring）。
    返回按 (页, y0) 升序；每条是**代表**候选的 `EqNum`。
    """
    return [c.as_eqnum() for c in scan(doc).picks]


def number_line(items: list[figures._Item], eq: EqNum) -> figures._Item | None:
    """`eq` 对应的**编号行**（该页 y0 与 `eq.y0` 对齐、且行尾就是该编号的文本行）。"""
    best = None
    for z in items:
        if z.kind != "T" or abs(z.y0 - eq.y0) >= 0.5:
            continue
        m = NUM_TOKEN.search(z.text)
        if m and int(m.group(1)) == eq.num:
            if best is None or z.x1 > best.x1:
                best = z
    return best


def formula_band(items: list[figures._Item], eq: EqNum, body_size: float | None,
                 page_rect: fitz.Rect, colw: float,
                 neighbours: tuple[EqNum, ...] = ()
                 ) -> tuple[fitz.Rect, str, str, bool]:
    """`eq` → `(裁图矩形, 依据, 备注)`。**不改原件、不写盘。**

    ## 为什么**不能**直接复用 `figures.band_of`（实测量的理由，逐条）

    `band_of` 的语义是"图注在一侧、内容在另一侧"，它把版面实物切成 `above` / `below`
    两半（`z.y1 <= cap.y0-0.5` / `z.y0 >= cap_y1+0.5`）。对**公式编号**这个前提不成立：

    1. **公式体与编号纵向重叠**。编号右对齐在公式行的右端，两者 y 范围交叠 → 实物
       既不在 `above` 也不在 `below`，`band_of` **看不见它**。实测 331/782 条（42%）
       的带因此定不出（`2500836` p7 的 `(1)`：公式是整幅图片 `I y=676.1..707.0`，
       编号行 `y=685.9..699.2` 落在图片内部；同篇 p16 的 `(15)`、`2511565` p23 的
       `(41)` 是分式，分子/分母分别跨过编号行的上下沿，同理）。
    2. **`_is_flow_text` 会把整幅宽的正文号公式行判成正文段落行**而当场停走
       （`2500836` p12 的 `(5)` 报的就是「上侧紧邻即正文段落行」）。
    3. **`band_of` 刻意把"图注那一行"排除在带外**（图注另存 `.caption.txt`）。编号行
       本职是标签、该排除；但**编号与公式体同行**的那 9 条里，那一行就是公式体。

    故本函数**复用 `figures` 的同一套量**（`_page_items` / `_is_flow_text` /
    `_line_scale` / `GAP_PITCH_MULT`——没有新的常数），但把"上下分区"换成
    **以编号行为锚、被「本页相邻编号行」与「`±REACH_PITCH_MULT × 本页行距`」双重
    夹住的连通区间**：

    | 层 | 条件 | 为什么 |
    | :--- | :--- | :--- |
    | 可达域 | 实物的 y 范围落在 `[lo, hi]` 内，且非正文行 | 把带**钉死**在编号行附近，吸收**不可能连锁跑掉** |
    | 吸收 | 与当前区间**纵向重叠 >= 0.5pt**，或与当前区间的**间隙 <= 1.2 × 本页行距** | 公式行/分式的分子分母/整幅图片都与编号行交叠；间隙那一条管多行公式的续行 |

    其中 `lo = max(编号行.y0 − REACH, 上一条编号行.y1)`、
    `hi = min(编号行.y1 + REACH, 下一条编号行.y0)`；`neighbours` 由调用方传入
    「本页检出的全部编号」（`extract_all` 与 `verify_d.py` 的适配器传的是同一个列表，
    故两处算出的矩形逐字节一致）。**「相邻编号行」这一条不是凑的**：两条编号公式的
    排版区不会互相穿插，故用它们当硬边界——实测 `2504223` p10 的 (1)/(2)/(3) 是三个
    各占 3 行的展示式、彼此相距 32pt，没有这条边界就只能靠距离阈值把它们分开
    （(2) 的分子 `P(Y=3)` 与 (3) 的分子 y 范围仅相差几 pt）。

    正文行（`_is_flow_text`）一律不吸收——它是段落，不是公式。

    **可达域那一层不是装饰，是实测逼出来的**：不加它时吸收会**连锁**（`2500836` 每页
    有一个 `D y=0..842 x=0..595.5` 的整页缘矩形，与任何编号行都"纵向重叠" → 23 条带高
    全变成 842.0pt 整页；`2502355` 的 `(2)`/`(3)` 则连页眉 `Team # 2502355` 一起吞掉，
    带高 441.6pt）。加上它之后**区间一定落在 `[lo, hi]` 里**——这条不变式可直接核，
    报告里逐份印出带高与该区间的用量。

    ## 失败条件（这条取法在什么情况下会切掉内容）

    * **续行距编号行超过 `REACH_PITCH_MULT × 本页行距` 时不会被吸收**，**多行公式的
      续行可能被切掉**（取法刻意保守：宁可少收，不可把整节吞进来）。实测"用掉的可达
      距离"分布与该倍数的推导写在 `REACH_PITCH_MULT` 的定义处（**复算脚本与逐字输出**：
      `tests/papers/recon/formula-band-scan.py` → `formula-band-scans.txt`）；两种取法的
      带高**逐份、两组并列**印在 `d-report.txt`；`2514461` p9/p10 这类"编号上下都紧邻
      公式行"的实例逐条可复算。
    * 退化（没吸收到任何非正文实物）时返回编号行自身并置位——**条数照报**，不静默。
    * **不改原件**：原件的字节由 A1（io 层）在流水线两侧比对，本函数只读。

    返回的矩形**保证非空**（至少包含编号行自身），所以"检出多少条就产出多少张"成立。
    """
    line = number_line(items, eq)
    own = (fitz.Rect(line.x0, line.y0, line.x1, line.y1) if line is not None
           else fitz.Rect(eq.x0, eq.y0, eq.x0 + 1.0, eq.y1))
    scale = figures._line_scale(items, body_size)
    reach = REACH_PITCH_MULT * scale
    gap_limit = figures.GAP_PITCH_MULT * scale
    lo, hi = own.y0 - reach, own.y1 + reach
    for nb in neighbours:
        if nb.num == eq.num:
            continue
        if nb.y1 <= own.y0:
            lo = max(lo, nb.y1)
        elif nb.y0 >= own.y1:
            hi = min(hi, nb.y0)
    pool = [z for z in items
            if z is not line
            and not figures._is_flow_text(z, body_size, colw)
            and z.y0 >= lo and z.y1 <= hi]
    box = fitz.Rect(own)
    absorbed: list[figures._Item] = []
    notes: list[str] = []
    while True:
        grew = False
        for z in pool:
            if z in absorbed:
                continue
            overlap = min(box.y1, z.y1) - max(box.y0, z.y0)
            if overlap < 0.5:
                gap = max(z.y0 - box.y1, box.y0 - z.y1)
                if gap > gap_limit:
                    continue
                notes.append(f"{z.kind}@y{z.y0:.0f} 按间隙 {gap:.1f}pt<=上限 {gap_limit:.1f}pt 吸收")
            absorbed.append(z)
            box |= fitz.Rect(z.x0, z.y0, z.x1, z.y1)
            grew = True
        if not grew:
            break
    # 一件实物都没吸收到，**且编号行是"整行只有编号"**（不是与公式体同行的那种）：
    # 这时带 = 编号行自己，这一条没有任何版面依据。
    #
    # 判"是不是纯编号行"用的是**该行自己的文本**（与 `scan()` 里 `score` 同一个谓词）：
    # 编号与公式体同行时（`Candidate.score == 1`），编号行**本身就是公式体那一行**，
    # 带里已经有内容，不算退化。
    #
    # **刻意不套 `figures.MIN_BAND`**：那是图注口径的常量（"带高不足一个行距 = 误判"），
    # 而**单行公式的带本来就只有一个行距高**（12pt 正文 → 约 13pt）。套上去会把
    # 所有单行公式判成退化（实测 `2508861`、`2517273` 那类单行展示式全部中招）。
    pure_line = line is None or NUM_TOKEN.fullmatch(line.text.strip()) is not None
    if not absorbed:
        if pure_line:
            return own, "无依据（未吸收到任何非正文实物）", "退化为编号行自身", True
        return own, "编号与公式体同行", "", False
    # 「最长延伸」= 吸收到的实物距编号行 y 范围最远的距离，以本页行距为单位。
    # 它是**可达域倍数取值的实测依据**（见 `REACH_PITCH_MULT`），逐份印在报告里。
    used_pitch = 0.0
    if absorbed:
        used_pitch = max(
            max(own.y0 - z.y0, z.y1 - own.y1, 0.0) for z in absorbed
        ) / scale
    return box, (
        f"吸收 {len(absorbed)} 件实物（{len(notes)} 处按行距延伸；"
        f"最长延伸 {used_pitch:.2f}×行距）"
    ), "", False






def context_text(eq: EqNum, line_text: str, wheres: list[str],
                 cites: list[str]) -> str:
    """一条公式的 `.context` 正文（口径见模块 docstring）。"""
    out = [f"REF: ({eq.num})", f"SRC: {nospace(line_text)}"]
    out += [f"WHERE: {nospace(w)}" for w in wheres]
    out += [f"CITE: {nospace(c)}" for c in cites]
    return "\n".join(out) + "\n"


def extract_all(src: Path, out_dir: Path, dpi: int = 200) -> EqResult:
    """从**原件**抽公式编号 + 裁图 + 引述句。原件只读。

    产出：`<out_dir>/eq-NN-pP.png` + 同名 `.context`（NN = 编号，P = 页码 1 起）。
    目录里的旧 `*.png` / `*.context` 先清掉（可重生成的派生物）。
    """
    doc = fitz.open(src)
    out_dir = Path(out_dir)
    n_eq = n_refs = n_where = n_cite_all = n_band_fallback = 0
    n_stripped = 0
    n_cand = n_rejected = 0
    try:
        # **必须在任何 get_pixmap 之前**（机制层，D3）。返回 0 对流水线是异常信号
        # （该篇水印形态与已知不同），由 verify_d 的 D3 对账暴露。
        n_stripped = watermark.strip_in_memory(doc)
        try:
            from . import textmd
            body_size = textmd.body_size(doc)
        except Exception:
            body_size = None
        sc = scan(doc)
        n_cand, n_rejected = len(sc.cands), len(sc.rejected)
        all_lines = _line_texts(doc)

        # 引述句归属：**位置在 it 之前、最近的那条检出编号**（见模块 docstring）。
        wheres: dict[int, list[str]] = {c.num: [] for c in sc.picks}
        cites: dict[int, list[str]] = {c.num: [] for c in sc.picks}
        nums = set(wheres)
        picked_pos = [(c.page, c.bbox[1], c.num) for c in sc.picks]
        for pno, bbox, text in all_lines:
            if WHERE_RX.match(text):
                before = [t for t in picked_pos if (t[0], t[1]) < (pno, bbox[1])]
                if before:
                    num = max(before)[2]
                    wheres[num].append(text.strip())
                    n_where += 1
            for m in CITE_RX.finditer(text):
                n_cite_all += 1
                n = int(m.group(1))
                if n in nums:
                    cites[n].append(text.strip())
                    n_refs += 1

        if out_dir.is_dir():
            for old in list(out_dir.glob("*.png")) + list(out_dir.glob("*.context")):
                old.unlink()
        out_dir.mkdir(parents=True, exist_ok=True)

        by_page: dict[int, list[EqNum]] = {}
        for c in sc.picks:
            by_page.setdefault(c.page, []).append(c.as_eqnum())
        for c in sc.picks:
            eq = c.as_eqnum()
            page = doc[eq.page]
            items, colw = figures._page_items(page)
            rect, _basis, _why, degenerate = formula_band(
                items, eq, body_size, page.rect, colw, tuple(by_page[eq.page]))
            if degenerate:
                # 退化：带里**一件非正文实物都没吸收到**，且编号行是"整行只有编号"
                # （`formula_band` 的返回值第 4 位）。**刻意没有"带高 < MIN_BAND"这一支**
                # ——`formula_band` 不套 `figures.MIN_BAND`（理由见那里的注释：单行公式的
                # 带本来就只有一个行距高）。旧版这句话里曾挂着"或带高 < MIN_BAND"，
                # 与实现不符，是残留，本轮删掉。
                # **仍产出**——保证"检出多少条就产出多少张"（D1-a 的形状）；但这一条
                # 没有版面依据，条数逐份印在报告里，不进任何"质量已验"的声称。
                n_band_fallback += 1
            line = number_line(items, eq)
            name = f"eq-{eq.num:02d}-p{eq.page + 1}"
            png = page.get_pixmap(dpi=dpi, clip=rect)
            (out_dir / f"{name}.png").write_bytes(png.tobytes("png"))
            (out_dir / f"{name}.context").write_bytes(context_text(
                eq, line.text if line is not None else f"({eq.num})",
                wheres[c.num], cites[c.num]).encode("utf-8"))
            n_eq += 1
    finally:
        doc.close()
    return EqResult(n_eq=n_eq, n_refs=n_refs, n_stripped=n_stripped,
                    n_cand=n_cand, n_rejected=n_rejected, n_where=n_where,
                    n_cite_all=n_cite_all, n_band_fallback=n_band_fallback)


def equation_captions(doc: fitz.Document) -> list[figures.Caption]:
    """把**检出编号**表示成 `figures.Caption`（形状与图注的 `figures.Caption` 同一个类）。

    `kind="eq"` 不是随手写的：产出图名是 `eq-{num:02d}-p{page+1}.png`，而 C4 的
    `verify_c.strip_provenance` 内部拼的正是
    `f"{cap.kind}-{cap.num:02d}-p{cap.page+1}.png"` ——**逐字相同**。于是 D3 的
    「产出图来源」层可以**原样调用** C4 那条谓词，不必复制它（`verify_d.py` 里那段
    适配器只做这一层映射，见其 `strip_provenance` 的调用点）。
    """
    out = []
    for c in scan(doc).picks:
        items, _colw = figures._page_items(doc[c.page])
        line = number_line(items, c.as_eqnum())
        out.append(figures.Caption("eq", c.num, c.page, c.bbox[1],
                                   line.text if line is not None else f"({c.num})"))
    return out
