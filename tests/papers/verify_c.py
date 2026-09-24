"""图表判据 C1/C2/C3/C4（Task 4）。

| # | 判据 | 参照 |
| :--- | :--- | :--- |
| C1 | **图注计数 == 产出图片数**；差额必须**逐条登记**（且每条**原因具体**、可核）且占比 <= 10% | 独立数一遍图注（本文件自带的形态副本）|
| C2 | 每张图 **非白像素占比 >= 0.5%**，否则判空图 | 像素直方图（阈值见下）|
| C3 | 每张图配同名 **`.caption.txt`** | 图注随图落盘，可逐条核对 |
| C4 | 产出图不含水印 | **两层**：① strip 后水印 XObject 流长必须为 0；② A/B 差分证明产出 PNG 来自**置空后**的渲染（三态，见下）|

## C1 的判定写成这个形状的理由（措辞要说准，别夸大也别缩小）

任务书的口径是「**差额为 0；非 0 须逐条登记解释，不得悄悄抹平**」。实测定稿规则下
43 份有 **27/935 = 2.89%** 的图注**定不出内容带**（题注与图/表不相邻、或带高不足
一个行距），`figures.extract_all` 把它们**逐条**写进 `FigResult.skipped`（带具体
原因：哪一侧、最近实物在多远、带高多少）。故 C1 判两条：

1. `len(extract_all.skipped) == 图注数 − 产出数`——**每一条差额都有登记**。
   少了 = 有图注既不产出也不登记（静默丢失）；多了 = 登记与事实不符。两者都 FAIL。
2. **每条登记本身必须"原因具体"**（`SKIP_RECORD_RX` / `SKIP_SIDE_RX` / `SKIP_SIGNAL_RX`
   / `MIN_BAND_CLAIM_RX` 四条，见其定义处）——须含**页码 + 编号 + 侧别 + 一个可核的
   具体信号**（量出的 pt 值，或"正文段落行"/"无实物"这类定点原因），且**明写了不等式的
   那一句必须自洽**（`X < MIN_BAND=Y` 要求 X < Y）。第 1 条**只数条数**，抓不住
   "登记的是不是废话"：把 `band_of` 的返回换成空串、登记 27 条"定不出带"，差额与占比
   都不变，只判第 1 条照样绿（复审 2026-09-24 点名的缺口）。第 2 条就是为它加的；
   第 4 小条（不等式的自洽）是**复核轮顺带实测出的一处真身**：入库证据里曾有一句
   `下侧带高只有 91.2pt < MIN_BAND=20.0pt`——**这句话不成立**（`figures.band_of`
   已把两种情形分开报，并把两处必须同步写在原地）。
3. `差额 / 图注总数 <= SKIP_CEILING`（10%，实测定稿值 2.89% 的 3.4 倍）。
   这条是**防第 1 条被自己的前提架空**：只判"登记齐"的话，一个"什么都定不出"的
   实现会把 935 条全登记进去、C1 照样绿。

**C1 抓得住什么**：提取侧静默丢弃图注（跳过时不登记）、匹配口径与实现不一致、
图注形态整类失配（两侧数量一起塌）、登记退化成噪音（笼统话/缺页码侧别与数值）。
**C1 抓不住什么**：① 规格本身错——本文件的形态正则与 `figures.CAPTION_FORMS`
是**同一份规格的两处实现、不共享代码**，规格写错时两侧同错，C1 不喊；
② 产出的**图像内容**对不对（带切偏、把正文当图渲染）——C1 只数条数，C2 只能
发现"几乎全白"那一种；③ 登记**对着错的图注**（条数对、对象错）——报告把两份清单
并排印出，但仍只能靠人对着看（**已知边界，如实登记**）。

## C2 的阈值来源

设计文档给的是"初始值 0.5%，试点后按实测分布校正并记录校正理由"。实测分布与
最小值写进报告（每次运行重算）——**它是量出来的，不是推出来的**。

## C4 的四项，强度不一样（措辞要说准）

（三层机器判据 + 一项人工闸门。**判定链**上的是第 1、2 层；第 3 层只是筛选器。）

1. **结构化判据（权威）**：`strip_in_memory` 之后，所有带 `/PieceInfo +
   /Watermark` 标记的 XObject，流长必须为 0。流空了就画不出任何东西——与字体、
   与厂商无关，故它对"水印换了个字体/拆成片段"也成立（2023 那批按 校/苑/数/模
   单字片段绘制，本判据同样覆盖）。**论文本来没有水印对象时**（`水印对象=0`），
   判据退化为"残留流长必须为 0"，此时它**不声称**水印被摘掉了——那份论文没有
   水印可摘。故报告里 `水印对象=N strip=N` 是必须逐份看的**覆盖指标**：
   `水印对象=0` 而文本层里带水印字，是"形态未知"的信号，不是"干净"。
   **`水印对象 == strip` 这半句不构成判据**：`strip_in_memory` 的返回值**按定义**
   就是 `len(find_watermark_xrefs(doc))`，与左边是**同一次调用、同一个谓词**数的数，
   该等式**按构造恒真**（M-C4a 变异下 strip 一个流都没清，等式照样成立，实测）。
   真正起作用的是 `残留流长>0 == []`。扫描的 xref 集合取**机制自己的谓词**
   （`find_watermark_xrefs`），本文件另留一份**独立副本**并逐篇断言两者集合相等
   ——不一致即 FAIL（「同一语义必须用同一谓词」，通则候选①；修复前这份副本是唯一的
   扫描实现，且不共享代码，将来会**静默分叉**）。
2. **产出图来源层**：见 `strip_provenance`——它是**三态**（已验证 / FAIL / 未验证），
   三态各自的去向写在那里的 docstring 与 `checks()` 的 C4 段。
3. **像素代理（筛选器，不是结论）**：偏红像素占比。它**只用来筛出可疑样件送人工**，
   **不参与 ok**——残余偏红可能来自照片本身的暖色（石质/木质），实测
   `2500836` p3 的水印页偏红 1.873% → 摘后 0.402%，那 0.402% 就是石阶照片。
4. **人工目视（用户侧的闸门）**：见下。

**凡"结论由部分样本支撑"的地方，报告一律给覆盖数（`已验证 N/M`），不说"全通过"**——
第 2 层的结论只建立在"试出来的那几条带"上，说"全通过"就是把部分样本说成全体。

## 人工目视项：为什么它**不并入 `RESULT` 行**

`c4-visual-confirm.txt` 是**人工**文件，本脚本只**读**它（缺了/为空即判该闸门
FAIL，见 `VISUAL`）。但它的 FAIL **不并进 `RESULT`**，理由两条：

* **任务书 Step 4 要求全量跑在人工介入之前就得到 `RESULT: PASS`**——把人工项并进
  `RESULT`，那一行在人工写入之前**恒为 FAIL**，与"恒真"的判据同罪（本项目 4.2 的
  家族：既不说话的判据、永远说同一句话的判据，都不提供区分力）。`RESULT` 因此
  只覆盖**机器可核**的部分；
* 任务书 Step 6 明写"这是用户侧的闸门，**不是**你能否通过的判据"。

它的效力放在**别处**、且**不可能被漏看**：报告末尾另起一行 `C4 人工目视闸门: …`
与一行 `发布放行: 未放行 …`，并在 `c4-visual-confirm.txt` 存在时把人工结论**逐字**
抄进报告（做法同 `verify_wm.py` 读 `wm-visual-confirm.txt`）。

**本脚本不得声称"已目视确认"**——它没有眼睛。它只给可核代理指标。

## 报告纪律（照抄 verify_b.py / verify_wm.py，不自创）

* 一律 `write_bytes` + LF 落盘、只写仓库相对路径（`report.path_audit` 每次运行
  当场扫，命中即判 FAIL）；
* 报告写入**无条件执行**（`main()` 结尾、不在 try 内）——脚本崩了也不能把上一次的
  `RESULT: PASS` 留在库里冒充本次结论；
* 被测模块（figures / io / watermark）的 import 放在 `checks()` 体内：模块被改坏时
  import 当场抛，那是 `main()` 的 try 保护得到的路径，能拿到「崩溃 → 写成 FAIL」；
* **落点随样本口径分离**（`tools/papers/report.py`）：全量跑写
  `tests/papers/reports/c-report.txt`（放行证据，入库）；`--limit N` 写
  `tests/papers/reports-limited/c-report-limited-N.txt`（不入库）。守卫**两个方向
  都守**（限样本不得落放行证据 / 全量**必须**落放行证据），且 `RESULT` 行带
  `LIMITED` 后缀——`^RESULT: PASS$` 只可能来自全量跑。

## 与 `verify_b.py` 的关系（登记为已知的债）

落点机制是 `verify_b.py` 那套的**副本**（抽成 `tools/papers/report.py`），
`verify_b.py` 本身**一个字节都没改**。两份机制并存是 Task 3 冻结留下的债，
见 `docs/mcm-suite-todo.md` §A 的终审清单——**不在本轮消除**。
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
# 人工目视结论的存档。**本脚本只读、绝不生成**（生成它就是把"人工"两个字抹掉）。
VISUAL = REPORTS / "c4-visual-confirm.txt"
COLLECTION = "2025美赛O奖论文"

# C1 的差额上界：**定不出内容带的图注**占总图注数的比例不得超过它。
#
# `0.10` 是**量出来的**：定稿规则下全 43 份实测 27/935 = **2.89%**
# （见 c-report.txt 的汇总行，每次运行重算），取 10% 有 3.4 倍余量。
# 它的作用只有一个——**防"差额全登记"这条判据被自己的前提架空**：C1 允许
# "定不出的图注"存在（只要逐条登记），若不加这条上界，一个"什么都定不出"的
# 实现会把 935 条全登记进去、C1 照样绿（本项目 4.2 家族：判据被自己的前置条件
# 架空）。与 B3 的 `HEADING_BUDGET = 0.20` 同一种形状：量出来的上界，不是推的。
# **已知边界**：这个数只对试点 43 份负责（字号/版式相近）；全量 201 份若版式
# 差异大，须重测。
SKIP_CEILING = 0.10
# C2：非白像素占比低于这个值判空图。**实测校正见模块 docstring 与报告汇总行。**
NONWHITE_MIN = 0.005
# 灰度 < 245 计为非白（与设计文档的初版口径一致）
NONWHITE_CUT = 245
# C4 像素代理的筛选阈：占比 >= 此值的样件列入"待人工确认"。
RED_SUSPECT = 0.01
# 偏红像素的判定：r > 140 且 r-g > 40 且 r-b > 40（设计文档的初版口径）
RED_MIN = 140
RED_DIFF = 40

# C4 第二层（产出图来源）的**未验证份数上界**：`strip_provenance` 返回 `None`
# 的份数占比不得超过它，超了**全批判 FAIL**，理由写「判据被自己的前提架空」。
#
# 为什么这一层需要上界（复核人 2026-09-24 的阻断项正是这里）：
# `None` 的语义是**证据不足**（这条带盖不到水印 / 无带可试 / 与两个参照都不同
# ——A/B 差分对它没有区分力），**不是证据为否**。三个处置里只有上界是诚实的：
#   * 并进通过 → 重蹈「什么都没验就报绿」（修复前正是这个：`prov is None` 不动
#     `c4`，实测 M-C4b 下 7 份里有 1 份**带着水印判绿**）；
#   * 硬失败该篇 → 因非缺陷卡住放行（证据不足 ≠ 该篇有缺陷）；
#   * **上界** → 少量未验证可接受，多了就说明这一层整体验不出东西。
#
# `0.10` 的依据：全量 43 份实测 **1/43 = 2.33%** 未验证（`2507789`：全篇只检出 1 条
# 图注且它定不出带 → 0 张产出 → 无带可试；见 c-report.txt 汇总行，每次运行重算），
# 上界取 **10% = 4.3 倍余量**。**倍数是选择、不是量出来的**——选它只为与
# `SKIP_CEILING` 用同一档；它对"整层验不出东西"（100%）这一真正要防的情形仍然有效。
# **已知边界**：只对试点 43 份负责（样本量越小、单份权重越大：`--limit 3` 的 7 份里
# 1 份未验证就是 14.3% > 10%，但那正是"要么判死、要么明说"的分界，不是误伤）。
PROV_UNVERIFIED_CEILING = 0.10

# C1 的「原因具体」判据（**可核，不靠人读**）。一条登记必须说清四件事：
#   **页码** + **编号**（fig/tab-N）+ **侧别**（上侧/下侧）+ **一个可核的具体信号**
#   （量出的 pt 值，或"正文段落行"/"无实物"这种定点原因——两者都是引擎真算出来的
#    量，不是笼统话），后面还要带图注原文。
# 反例（本判据要抓的形状）：`p7 fig-4: 定不出带`——差额在、条数对、占比也没变，
# 第 1 条判据照样绿，而"逐条解释"已经退化成噪音。
SKIP_RECORD_RX = re.compile(
    r"^p(?P<page>\d+) (?P<kind>fig|tab)-(?P<num>\d+): 定不出内容带"
    r"（(?P<why>.+?)）｜图注 (?P<cap>.+)$"
)
# 侧别：登记串必须指明是哪一侧（实测 27 条**全部**满足——`band_of` 的每条原因都
# 以"上侧/下侧"起头，故这条不是过宽的猜测，而是这条链路的构造性质）。
SKIP_SIDE_RX = re.compile(r"上侧|下侧")
# 具体信号：一个量出的数值（带 pt），或一条定点原因。**"两侧都够不着"这类笼统
# 兜底串不在此列**（实测它在 43 份上不可达——`band_of` 的兜底条目只在两侧都给出
# 具体原因后才可能空）。
SKIP_SIGNAL_RX = re.compile(r"\d+(?:\.\d+)?pt|正文段落行|无实物")
# 登记串里**明写了不等式**的那一句，必须**自洽**：`带高只有 X pt < MIN_BAND=Y pt`
# 要求 X < Y。**这不是洁癖**：2026-09-24 复核轮实测到入库证据里有一处
# `2513314` p4 fig-2 的「下侧带高只有 **91.2pt** < MIN_BAND=**20.0pt**」——
# 91.2 并不小于 20.0（真实原因是宽度被裁成 0）。**"证据里一句不成立的话，比没有这句话
# 更坏"**，所以把"这句话里的数必须满足它自己声明的不等式"做成判据（`_skip_record_bad`）。
# 对应的 `figures.band_of` 已把两种情形**分开报**，并在那里注明了两处必须同步。
MIN_BAND_CLAIM_RX = re.compile(r"带高只有 ([\d.]+)pt < MIN_BAND=([\d.]+)pt")

# C1 的**独立参照**：图注形态在这里**另写一份副本**（≡ `figures.CAPTION_FORMS`，
# 逐字节相同的正则，但不 import 它）。所以它抓得住**实现侧**的放宽/收紧
# （`figures` 那份改宽了，这里不跟着变，会红）；**规格本身若错（正则写错），
# 两侧会同时错，C1 不会喊**——故两处必须同步改，且本判据是规格的**下界**。
# 这三条形态的实测覆盖（各多少条、几份）见报告汇总行。
CAPTION_FORMS = (
    re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*(\d+)\s*[:.]", re.I),
    re.compile(r"^\s*(?:Figure|Fig\.|Table)\s*(\d+)\s*[：．。]", re.I),
    re.compile(r"^\s*(?i:figure|fig\.|table)\s*(\d+)\s+[A-Z0-9]"),
)

# `--limit` 的见证集。**不并入取样是不行的**：排序序里靠后的关键样本
# `--limit 3` 取不到，变异演示会在看不见它的集合上"绿着通过"。
#
#   2501869  排序第 14 位。**无标点式图注**（`Figure 1 Our Work`）——第一条
#            ASCII 冒号形态对它一条都匹配不上（**实测该篇冒号式 0 条、无标点式
#            23 条**，两种口径都是 23：笼统式 `figure\s+\d+\s+` = 23、实现口径
#            `[A-Z0-9]` = 23；`c-report.txt` 该篇 `C1 图注=23` 与之一致。
#            此前这里写 30，**是错的、且无物证**，2026-09-24 复核轮实测改正）。
#            前 3 份（2500836/2501567/2501909）**全部**用冒号式，
#            没有它，`--limit 3` 根本走不到第三种形态那条分支。
#   2516178  排序第 25 位。无标点式 + 本篇正文字号最小（10.6pt），是"字号逐篇变化"
#            那一类风险的实例件。
#   2517199  排序第 42 位。**`Fig.` 缩写形态**（`Fig.1 Types of cybercrime [1]`）
#            + 全篇只此一份；它同时是 B2 记「不适用（无 Contents 页）」的那一份。
#   2522820  排序第 29 位（任务书点名：`--limit 3` 取不到它），表最多（18 张），
#            是 C1 **表分支**与"表在题注下方/上方"两种排版的实例件。
FOCUS = ("2501869", "2516178", "2517199", "2522820")


def caption_kinds(doc) -> Counter:
    """独立数图注：逐行匹配，返回 Counter({"fig": n, "tab": m})。

    **不调 `figures.caption_blocks`**——参照必须与实现分开（见模块 docstring）。
    """
    counts: Counter = Counter()
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"]).strip()
                for rx in CAPTION_FORMS:
                    m = rx.match(t)
                    if m:
                        counts["tab" if m.group(0).lstrip()[:1].lower() == "t" else "fig"] += 1
                        break
    return counts


def caption_index(doc) -> list[str]:
    """逐条图注的登记串（页/编号/文本），C1 差额非 0 时**逐条列出**用。"""
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                t = "".join(s["text"] for s in line["spans"]).strip()
                for rx in CAPTION_FORMS:
                    m = rx.match(t)
                    if m:
                        kind = "tab" if m.group(0).lstrip()[:1].lower() == "t" else "fig"
                        out.append(f"p{pno + 1} {kind}-{int(m.group(1)):02d}")
                        break
    return out


# C4 的「置空确实发生在渲染之前」这一层最多试几条图注（见 `strip_provenance`）。
STRIP_PROBE_MAX = 4


def strip_provenance(src: Path, dimg: Path, figures, watermark) -> tuple[bool | None, str]:
    """产出图确实来自**水印置空之后**的渲染？`(判定, 说明)`——**三态**。

    | 返回 | 含义 | 去向（在 `checks()` 里） |
    | :--- | :--- | :--- |
    | `True` | **已验证**：产出图与置空后的渲染逐像素相同 | 该篇该层通过 |
    | `False` | **FAIL**：产出图与未置空的渲染逐像素相同 | 硬失败，进 `bad` |
    | `None` | **未验证**：这条带盖不到水印 / 无带可试 / 与两个参照都不同，A/B 差分**没有区分力** | **既不算通过、也不硬失败该篇**；但**必须计数**，且受 `PROV_UNVERIFIED_CEILING` 上界约束（超界 → 全批判 FAIL，理由「判据被自己的前提架空」） |

    **为什么 `None` 不能算通过**（2026-09-24 复核的阻断项）：修复前
    `c4 = c4 and (prov is not False)` 对 `None` 一视同仁，于是 M-C4b（删掉
    `extract_all` 里的 `strip_in_memory`、产出图张张带水印）那一跑里，7 份中有 1 份
    报"与两个参照都不同" → `None` → **那份带着水印却判绿**。而同一行的括注与本
    docstring 当时写的都是"不记为通过"——**代码与自己的说明相反**。三态是唯一诚实
    的位置：`None` 是**证据不足**，不是证据为否，所以既不并进通过、也不当成该篇的缺陷；
    它被计数，并由上界兜住"整层都验不出来"的情形。

    **为什么非要有这一层**：上面那条结构化判据是**在原件上**验"置空能不能把水印流
    清空"——它验的是**机制**，不是**产出图**。`extract_all` 里那句
    `strip_in_memory(doc)` 若被删掉，机制照样成立、产出图却张张带水印，那条判据
    **不会红**（实测：删掉它，C4 结构化判据全绿）。

    做法是**在产出文件上做 A/B 差分**（黑盒，不读 `extract_all` 的内部状态）：

      A = 本脚本从**置空后**的 doc 重渲染同一条带
      B = 从**未置空**的 doc 重渲染同一条带
      产出 PNG 必须等于 A。等于 B（且 A ≠ B）→ 产出图没经过置空 → FAIL。

    只在 A ≠ B 的带上判定：`A == B` 说明这条带根本没盖到水印，它对"有没有置空"
    不敏感，**不能当证据**（本项目 4.2 家族：拿一个恒等的比对当判据）。逐条往下试，
    最多 `STRIP_PROBE_MAX` 条；一条都试不出差异 → **未验证**（`None`）。

    **说明串必须与实情等强**（本项目最重的那类缺陷是"证据文件里一句不成立的断言"）：
    `tried == 0` 时**一条带都没比较过**，所以那时**不许**说"A == B"——A == B 从未被
    建立过（修复前那一版就是这么写的，而它被永久写进了入库的放行证据）。

    已知边界：本层用的是 `figures` 的定位函数（`_page_items` / `band_of`），
    所以它验的是"**渲染来源**"，不是"定位对不对"——定位对不对归 C1/C2。
    产出图与 A、B 都不同时**不判死**（那是 C2 的活），但**也不报通过**——记
    "无法判定"，并入未验证计数（修复前它同样静默地算通过）。
    """
    from PIL import Image

    import fitz

    from tools.papers import textmd

    # A 侧：**置空后**的 doc（用与 `extract_all` 同一套定位口径）
    with fitz.open(src) as doc:
        watermark.strip_in_memory(doc)
        try:
            body = textmd.body_size(doc)
        except Exception:
            body = None
        tried = 0
        for cap in figures.caption_blocks(doc):
            if tried >= STRIP_PROBE_MAX:
                break
            page_a = doc[cap.page]
            items, colw = figures._page_items(page_a)
            rect, _dir, _why = figures.band_of(items, cap, body, page_a.rect, colw)
            if rect is None:
                continue
            png = dimg / f"{cap.kind}-{cap.num:02d}-p{cap.page + 1}.png"
            if not png.is_file():
                continue
            tried += 1
            pa = page_a.get_pixmap(dpi=200, clip=rect)
            # B 侧：另开一份原件（**不置空**）。置空是就地改内存对象，回不去。
            #
            # **B 侧必须先做与 A 侧同样的解析调用**——这不是洁癖，是实测逼出来的：
            # 同一页同一条带，**"已解析过文本/drawings 的 doc"与"刚打开的 doc"渲染
            # 出来的像素不同**（2026-09-24 实测 `2501909` p3：fresh vs fresh 相同、
            # used vs fresh **不同**、同一 doc 解析前后渲染相同）。不做这一步，
            # `A != B` 会被"解析历史不同"这一项满足，本层就会在**没置空**的时候
            # 报出 True（M-C4a 实测正是两篇报 True）。机制不明，只登记实测量。
            with fitz.open(src) as doc_b:
                page_b = doc_b[cap.page]
                page_b.get_text("dict")
                page_b.get_drawings()
                pb = page_b.get_pixmap(dpi=200, clip=rect)
            a = (pa.samples, pa.width, pa.height)
            b = (pb.samples, pb.width, pb.height)
            if a == b:
                continue          # 这条带对"有没有置空"不敏感，不能当证据
            got = Image.open(png).convert("RGB")
            probe = (got.tobytes(), got.width, got.height)
            if probe == b:
                return False, (
                    f"{png.name} 与**未置空**的渲染逐像素相同（而置空后的渲染与之不同）"
                    f"——产出图没有经过水印置空"
                )
            if probe == a:
                return True, f"{png.name} 与置空后的渲染逐像素相同（该带盖到水印）"
            return None, (
                f"**无法判定**：{png.name} 与两个参照（置空后 / 未置空）都不同——"
                f"本层未验证该篇（内容对不对是 C2 的活）"
            )
        if tried == 0:
            # **tried == 0 = 一条带都没比较过**，所以这里**不许**说"A == B"：
            # 那个等式从未被建立过。修复前这里写的正是
            # 「试过 0 条图注的带都盖不到水印（A == B）」，一句**不成立的断言**
            # ——而它被永久写进了入库的放行证据（复核 2026-09-24 点名）。
            # 该篇的真实理由是"没有可试的带"（0 张产出 / 图注定不出带），
            # 不是"试过且都盖不到"。
            return None, "未比较任何带（tried=0：本篇没有定得出带且已产出的图注）→ 未验证"
        return None, (
            f"试过 {tried} 条图注的带，**每条都是 A == B**（该带盖不到水印，差分无"
            f"区分力）→ 未验证"
        )


def image_stats(png: Path) -> tuple[float, float]:
    """一张 PNG → `(非白像素占比, 偏红像素占比)`。**一次解码算两个量。**

    全量 201 份会有上万张 PNG，两个指标分开算就要解码两遍——解码是这里最贵的一步。
    两侧谓词都走 PIL 的 C 层算子（`point` / `subtract` / `logical_and` / `histogram`），
    **不走 Python 逐像素**（`getdata()` 在 200dpi 的整页渲染上完全不可行）。

    非白 = 灰度 < `NONWHITE_CUT`（C2 的判据量）。
    偏红 = `r > RED_MIN` 且 `r-g > RED_DIFF` 且 `r-b > RED_DIFF`（水印是半透明红）。
    """
    from PIL import Image, ImageChops
    im = Image.open(png).convert("RGB")
    total = im.width * im.height
    if not total:
        return 0.0, 0.0
    nonwhite = sum(im.convert("L").histogram()[:NONWHITE_CUT]) / total
    rr = im.getchannel("R")
    m = rr.point(lambda v: 255 if v > RED_MIN else 0).convert("1")
    m = ImageChops.logical_and(
        m, ImageChops.subtract(rr, im.getchannel("G"))
        .point(lambda v: 255 if v > RED_DIFF else 0).convert("1"))
    m = ImageChops.logical_and(
        m, ImageChops.subtract(rr, im.getchannel("B"))
        .point(lambda v: 255 if v > RED_DIFF else 0).convert("1"))
    # mode "1" 的 histogram() 只有两个桶：[0 的个数, 255 的个数]
    return nonwhite, m.histogram()[-1] / total


def _skip_record_bad(s: str) -> str:
    """一条 `FigResult.skipped` 登记串 → 不合规的理由（空串 = 合规）。

    这是 C1 第 2 条判据的**可核**实现（正则，不做人工判断）：一条登记必须说清
    「哪一页、哪张图/表、哪一侧、**算出的那个数**」。判三个形状：

      1. 整体形状：`p<页> <fig|tab>-<号>: 定不出内容带（<原因>）｜图注 <原文>`
      2. `<原因>` 里点明**侧别**（上侧/下侧）——`band_of` 的每条原因都以它起头，
         故这是这条链路的构造性质，不是过宽的猜测；
      3. `<原因>` 里含**一个可核的具体信号**：量出的 pt 值，或"正文段落行"/"无实物"
         这类定点原因。**笼统兜底串（如"两侧都够不着"）不在此列。**
      4. **明写了不等式的那一句必须自洽**：`带高只有 X pt < MIN_BAND=Y pt` 要求 X < Y
         （见 `MIN_BAND_CLAIM_RX` 的注释——这一条是从一次**实测到的不成立的断言**里长出来的）。

    实测：全量 43 份的 27 条登记**逐条合规**（每次运行重算，见报告汇总行）。
    """
    m = SKIP_RECORD_RX.match(s)
    if not m:
        return "形状不符（缺页码/编号/原因/图注原文四段之一）"
    why = m.group("why")
    if not SKIP_SIDE_RX.search(why):
        return "原因里没点明是哪一侧（上侧/下侧）"
    if not SKIP_SIGNAL_RX.search(why):
        return "原因里没有任何量出的数值/定点原因（只有笼统话）"
    for x, y in MIN_BAND_CLAIM_RX.findall(why):
        if not float(x) < float(y):
            return (
                f"登记串里的不等式不成立：它写「带高只有 {x}pt < MIN_BAND={y}pt」，"
                f"而 {x} 不小于 {y}（不成立的断言比没有这句话更坏）"
            )
    return ""


def checks(lines: list[str], limit: int = 0, meta: dict | None = None,
           out: Path | None = None, report=None) -> bool:
    import fitz

    from tools.papers import figures, io, watermark

    root = io.ORIGIN / COLLECTION
    all_pdfs = sorted(root.rglob("*.pdf"))
    # fail-closed：试点目录取不到就抛，不得空跑一圈然后报「全通过」。
    if not all_pdfs:
        raise FileNotFoundError(f"试点目录下没有任何 PDF：{root}")
    pdfs = report.pick_sample(all_pdfs, limit, FOCUS)
    if meta is not None:
        meta["n_sample"], meta["n_all"] = len(pdfs), len(all_pdfs)

    lines.append(
        f"图表判据 C1/C2/C3/C4 · **限样本 {len(pdfs)}/{len(all_pdfs)} 份**"
        f"（--limit {limit} + 见证集 {'/'.join(FOCUS)}）"
        if limit > 0 else f"图表判据 C1/C2/C3/C4 · 试点 {len(pdfs)} 份"
    )
    if limit > 0:
        lines.append(f"  取样：{' '.join(p.stem for p in pdfs)}")
        lines.append(
            f"  ! 这是**限样本跑**，不是放行依据；放行证据是 {report.rel(report.release_path('c'))}"
            f"（本句按实际落点判定，见报告末尾的落点声明）。"
        )
    lines.append("=" * 72)

    bad: list = []
    n_blank = 0
    n_missing_cap = 0
    min_nonwhite = float("inf")
    min_nonwhite_where = ""
    n_c4_unknown = 0        # 水印对象=0 的份数（覆盖指标，逐份要看得见）
    n_c4_unverified = 0     # C4 第二层"未验证"的份数（`prov is None`，受上界约束）
    n_red_suspect = 0
    tot_fig_cap = tot_tab_cap = tot_fig_png = tot_tab_png = 0
    n_skip_total = 0
    n_skip_bad_shape = 0    # 登记串"原因不具体"的条数（C1 第 2 条判据）
    n_c4_diverged = 0       # 两处水印谓词给出不同集合的份数（C4 的分叉 tripwire）
    n_c1_diff_papers = 0
    for src in pdfs:
        try:
            prob = src.parent.name
            out_dir = io.figures_dir(COLLECTION, prob, src.stem)
            res = figures.extract_all(src, out_dir)

            # ---- C1：独立数图注 vs 产出 ----
            with fitz.open(src) as doc:
                want = caption_kinds(doc)
                want_index = caption_index(doc)
            figs = sorted(out_dir.glob("fig-*.png"))
            tabs = sorted(out_dir.glob("tab-*.png"))
            produced = figs + tabs
            tot_fig_cap += want["fig"]
            tot_tab_cap += want["tab"]
            tot_fig_png += len(figs)
            tot_tab_png += len(tabs)
            diff = (want["fig"] + want["tab"]) - len(produced)
            # C1 判两条（见模块 docstring）：
            #   ① 差额必须**全部登记**——每一条差额都要在 extract_all 自述的
            #      `skipped` 里有对应的一条。少了 = 有图注既没产出也没登记（静默丢失）；
            #      多了 = 登记与事实不符。两者都 FAIL。
            #   ② 每条登记本身必须**原因具体**（`_skip_record_bad` 的可核形状）——
            #      第 ① 条只数条数，抓不住"登记的是不是废话"（复核 2026-09-24 点名的
            #      缺口：把原因换成"定不出带"这种笼统话，条数/占比全不变，①照样绿）。
            bad_records = [s for s in res.skipped if _skip_record_bad(s)]
            c1 = (len(res.skipped) == diff) and not bad_records
            c1_note = ""
            if len(res.skipped) != diff:
                c1_note += (
                    f"（图注数−产出数 = {diff}，而 extract_all 自述登记 "
                    f"{len(res.skipped)} 条——**登记数与差额不符**，有图注既没产出也没"
                    f"被登记，或登记与事实不一致）"
                )
            if bad_records:
                n_skip_bad_shape += len(bad_records)
                reasons = sorted({_skip_record_bad(s) for s in bad_records})
                c1_note += (
                    f"（**登记串不合规** {len(bad_records)} 条：{'；'.join(reasons)}；"
                    f"不合规的前 3 条 = {bad_records[:3]}）"
                )
            if diff:
                n_c1_diff_papers += 1
            n_skip_total += len(res.skipped)

            # ---- C2 / C3：逐张图 ----
            blank, missing_cap, ratios = [], [], []
            reds_all: list[tuple[str, float]] = []
            for p in produced:
                try:
                    nw, red = image_stats(p)
                except Exception as e:
                    blank.append(f"{p.name}(读不出：{type(e).__name__})")
                    continue
                ratios.append(nw)
                reds_all.append((p.name, red))
                if nw < min_nonwhite:
                    min_nonwhite, min_nonwhite_where = nw, f"{src.stem}/{p.name}"
                if nw < NONWHITE_MIN:
                    blank.append(f"{p.name}({nw * 100:.2f}%)")
                cap = p.with_suffix(".caption.txt")
                if not (cap.is_file() and cap.read_bytes().strip()):
                    missing_cap.append(p.name)
            # C2/C3 逐篇只判**实际量到的东西**；
            # **零产出**那条前置条件放在**样本级**（见循环后的 `out_ok`）——
            # 逐篇放会误伤"本来就几乎没有图注"的论文（实测 `2507789` 全篇只有 1 条
            # 图注、且它定不出带，于是该篇零产出；而"这一条没产出"这件事 C1 已经
            # 逐条登记过了，C2/C3 再判一次只是重复计一次同样的信息）。
            # 样本级那条守的是另一种形状：**实现什么都没产出时
            # `not blank` 与 `all(... for p in [])` 都恒真**，两条判据一起绿着通过
            # （本项目 4.2 第 5 例：A3 的 `not bad_removed` 在零移除时恒真）。
            c2 = not blank
            c3 = not missing_cap
            n_blank += len(blank)
            n_missing_cap += len(missing_cap)

            # ---- C4：结构化（权威）+ 像素代理（筛选器）----
            with fitz.open(src) as doc:
                n_marked = len(watermark.find_watermark_xrefs(doc))
                n_stripped = watermark.strip_in_memory(doc)
                # 权威集合：**置空之后**由机制自己的谓词给出（同一函数、同一常量）。
                marked = set(watermark.find_watermark_xrefs(doc))
                leftover = [x for x in sorted(marked)
                            if len(doc.xref_stream(x) or b"") > 0]
                # **独立副本**（本文件自己的谓词，只用私有常量 `_WM_MARK`）：
                # 它不参与判定，唯一作用是让「机制扩了检出规则、这份副本没跟」这种
                # **静默分叉变成响的**（本项目通则候选①「同一语义必须用同一谓词」。
                # 修复前这里是**唯一**的扫描实现，与 `find_watermark_xrefs` 逐条件
                # 等价但**不共享代码**——将来 `find_watermark_xrefs` 的函数体一改
                # （加第二检出规则 / 收窄成 `/Subtype /Form`），`strip` 与 `n_marked`
                # 跟着变而这份副本不跟，`leftover` 就会扫错集合，判据对新形态水印失明。
                copy_set = set()
                for x in range(1, doc.xref_length()):
                    try:
                        o = doc.xref_object(x, compressed=True)
                    except Exception:
                        continue
                    if all(m in o for m in watermark._WM_MARK):
                        copy_set.add(x)
            # `水印对象 == strip` **不构成判据**：`strip_in_memory` 的返回值按定义就是
            # `len(find_watermark_xrefs(doc))`，与左边同一次调用的同一个谓词数的数，
            # 这个等式**按构造恒真**（M-C4a 变异下 strip 一个流都没清，等式照样成立，
            # 实测）。它是**覆盖指标**，不是判据；真正起作用的是 `not leftover`
            # （流空了就画不出东西）。
            predicate_diverged = copy_set != marked
            c4 = (n_stripped == n_marked) and not leftover and not predicate_diverged
            if n_marked == 0:
                n_c4_unknown += 1
            if predicate_diverged:
                n_c4_diverged += 1
            # 第二层：**产出图确实来自置空之后的渲染**（黑盒 A/B 差分，见其 docstring）。
            # **三态**：True = 已验证 / False = FAIL / None = **未验证**
            # （既不并进通过、也不硬失败该篇；计数 + 上界兜底）。
            prov, prov_msg = strip_provenance(src, out_dir, figures, watermark)
            c4 = c4 and (prov is not False)
            if prov is None:
                n_c4_unverified += 1
            prov_state = {True: "已验证", False: "**FAIL**", None: "未验证"}[prov]

            # 代理指标**覆盖该篇的每一张图**（不是抽样）：两张图分开解码要解码两遍，
            # 而抽样会留盲区——「最大 3 张」与「最可能带水印的那张」不是一回事。
            # 逐份列偏红最高的 3 张送人工。
            reds = sorted(reds_all, key=lambda t: t[1], reverse=True)[:3]
            suspicious = [n for n, r in reds if r >= RED_SUSPECT]
            n_red_suspect += len(suspicious)

            lines.append(
                f"{src.stem:<10} C1 图注={want['fig'] + want['tab']:<3}"
                f"(图{want['fig']}/表{want['tab']}) 产出={len(produced):<3}"
                f"(图{len(figs)}/表{len(tabs)}) 差额={diff:<3}"
                f"C2 最小非白={(min(ratios) * 100 if ratios else float('nan')):5.2f}% "
                f"空图={blank or '无'} C3 图注文件={'齐' if c3 else '缺' + str(missing_cap)} "
                f"C4 水印对象={n_marked} strip={n_stripped} 残留流长>0={leftover or '无'}"
            )
            lines.append(
                f"{'':10} C4 代理（仅筛选器·逐份偏红 top3）: "
                + " ".join(f"{n}={r * 100:.2f}%" for n, r in reds)
                + (f"  <- 待人工确认 {suspicious}" if suspicious else "")
            )
            lines.append(
                f"{'':10} C4 置空来源（A/B 差分）= {prov_state}："
                + ("**FAIL** —— " + prov_msg if prov is False else prov_msg)
            )
            if diff:
                # **逐条登记，不得悄悄抹平**：给出该篇的图注清单、产出清单与每条
                # 未产出的**具体原因**。差额非 0 而登记齐全时这一段照写不误——
                # 登记是判据的一部分，不是失败时才打印的附注。
                lines.append(
                    f"{'':10} C1 差额 {diff} 条，逐条登记：图注清单（独立数）= "
                    f"{' '.join(want_index)}；产出清单 = "
                    f"{' '.join(p.name for p in produced) or '（无）'}"
                )
                for s in res.skipped:
                    lines.append(f"{'':10}   未产出：{s}")
            if not c1:
                lines.append(
                    f"{'':10} ^ C1 FAIL：图注数 {want['fig'] + want['tab']} != 产出数 "
                    f"{len(produced)}（差额 {diff}）{c1_note}"
                )
            if not c2:
                lines.append(f"{'':10} ^ C2 FAIL：空图/读不出 {blank}")
            if not c3:
                lines.append(
                    f"{'':10} ^ C3 FAIL：缺 .caption.txt 或内容为空 {missing_cap}"
                )
            if not c4:
                lines.append(
                    f"{'':10} ^ C4 FAIL：水印对象={n_marked} strip={n_stripped} "
                    f"残留流长>0={leftover}；置空来源={prov_state}（{prov}）"
                    f"——流没被置空、或产出图没用置空后的 doc 渲染，水印会**被烤进** PNG"
                )
                if predicate_diverged:
                    lines.append(
                        f"{'':10}   **两处水印谓词已分叉**：`find_watermark_xrefs` 给出 "
                        f"{sorted(marked)}，本文件自己的副本谓词给出 {sorted(copy_set)}"
                        f"——同一语义必须用同一谓词（通则候选①）。`leftover` 扫的已经不"
                        f"是机制处理过的那一批，须**停手对齐两处**再谈本判据有效"
                    )
                if n_marked == 0:
                    lines.append(
                        f"{'':10}   **水印对象=0**：这份论文的水印形态与已知不同，"
                        f"find_watermark_xrefs 漏了它。须**停下调查该份的水印形态**"
                    )
            if not (c1 and c2 and c3 and c4):
                bad.append((src.stem, c1, c2, c3, c4, diff, blank, missing_cap, leftover))
        except BaseException as e:
            lines.append(f"{src.stem:<10} ! 处理该篇时抛出异常：")
            lines.append(report.fmt_exc(e))
            bad.append((src.stem, False, False, False, False, -1, ["<异常>"], ["<异常>"], []))

    lines.append("=" * 72)
    tot_want = tot_fig_cap + tot_tab_cap
    tot_diff = tot_want - tot_fig_png - tot_tab_png
    rate = tot_diff / tot_want if tot_want else 1.0
    tot_png = tot_fig_png + tot_tab_png
    # **样本级前置条件**（C2/C3 共用的那条）：整批零产出时，`not blank` 与
    # `all(... for p in [])` 恒真，两条判据会一起绿着通过。故显式判死。
    # 逐篇零产出**不在此判**——那是 C1 逐条登记的活（见循环内的注释）。
    out_ok = tot_png > 0
    if not out_ok:
        bad.append(("<零产出>", False, False, False, False, tot_diff, [], [], []))
    lines.append(
        f"C2/C3 前置条件：整批产出 {tot_png} 张"
        f"{'（**为 0 → C2/C3 会被自己的前置条件架空，判 FAIL**）' if not out_ok else '（非 0，两条判据有东西可验）'}"
    )
    lines.append(
        f"C1 合计：图注 {tot_want} 条（图 {tot_fig_cap} / 表 {tot_tab_cap}）"
        f"· 产出 {tot_fig_png + tot_tab_png} 张（图 {tot_fig_png} / 表 {tot_tab_png}）"
        f"· 合计差额 {tot_diff}· 有差额的份数 {n_c1_diff_papers}"
    )
    lines.append(
        f"C1 差额登记（**复述，不参与判定**）：extract_all 自述登记 {n_skip_total} 条 / "
        f"合计差额 {tot_diff} 条。这一行**不是判据**——判定由逐份的 "
        f"`len(skipped) == diff` 做（复核 2026-09-24 指出：原写法「不等 → FAIL」把自己"
        f"说成了执行点，而它既不 append 进 bad、也不改返回值；逐份那条在数学上已蕴含"
        f"本条，故它只是同义反复，只会给「靠子串读报告」的人一个假信号）"
    )
    # **前置条件守卫**（缺了它这条判据会被自己的前提架空）：允许"定不出带的图注"
    # 存在的前提是它**很少**。上界 `SKIP_CEILING` 是实测值的 3.4 倍，理由见常量注释。
    rate_ok = tot_want > 0 and rate <= SKIP_CEILING
    lines.append(
        f"C1 差额占比：{tot_diff}/{tot_want} = {rate * 100:.2f}% "
        f"（上界 {SKIP_CEILING * 100:.0f}%，实测定稿值 2.89%）"
        f"{'（超上界 → FAIL：判据被自己的前提架空）' if not rate_ok else ''}"
    )
    lines.append(
        f"C1 登记串「原因具体」（页码+编号+侧别+一个量出的数值/定点原因，"
        f"且明写的不等式必须自洽）：本次 {n_skip_total} 条登记里不合规 "
        f"**{n_skip_bad_shape}** 条"
        f"（可核形状 = `SKIP_RECORD_RX` / `SKIP_SIDE_RX` / `SKIP_SIGNAL_RX` / "
        f"`MIN_BAND_CLAIM_RX`；不合规即 FAIL——只判条数的旧口径抓不住这种退化）"
    )
    if not rate_ok:
        bad.append(("<差额占比>", False, False, False, False, tot_diff,
                    [], [], []))
    lines.append(
        f"C2 非白像素阈值 {NONWHITE_MIN * 100:.2f}%（灰度 < {NONWHITE_CUT} 计非白）"
        f"· 本次最小 {min_nonwhite * 100:.2f}%（{min_nonwhite_where or '无产出'}）"
        f"· 空图 {n_blank} 张"
    )
    lines.append(f"C3 缺 .caption.txt 的图 {n_missing_cap} 张")
    lines.append(
        f"C4 结构化（机制）：strip 找到的水印对象流必须全部为空 · "
        f"本次 {len(pdfs)} 份里 **水印对象=0** 的有 {n_c4_unknown} 份"
        f"（覆盖指标：=0 **不等于干净**，只等于「本脚本没找到水印对象」）"
    )
    lines.append(
        f"C4 结构化（机制）覆盖指标：`水印对象 == strip` **按构造恒真、不构成判据**"
        f"（`strip_in_memory` 的返回值按定义就是 `len(find_watermark_xrefs(doc))`）；"
        f"两处谓词分叉的份数 = **{n_c4_diverged}**（分叉即 FAIL，见 tripwire）"
    )
    # C4 第二层：**给覆盖数，不说"全通过"**——本层的结论只建立在"试出来的那几条带"上。
    prov_rate = n_c4_unverified / len(pdfs) if pdfs else 1.0
    prov_rate_ok = prov_rate <= PROV_UNVERIFIED_CEILING
    lines.append(
        f"C4 置空来源（产出图）：A/B 差分证明产出 PNG 来自置空后的渲染 · "
        f"**已验证 {len(pdfs) - n_c4_unverified} 份 / 未验证 {n_c4_unverified} 份**"
        f"（未验证 = 该带盖不到水印 / 无带可试 / 与两个参照都不同，差分无区分力；"
        f"**既不并进通过、也不硬失败该篇**）"
    )
    lines.append(
        f"C4 置空来源 未验证占比：{n_c4_unverified}/{len(pdfs)} = {prov_rate * 100:.2f}% "
        f"（上界 {PROV_UNVERIFIED_CEILING * 100:.0f}%，实测定稿值 2.33%）"
        f"{'（**超上界 → 全批判 FAIL：判据被自己的前提架空**）' if not prov_rate_ok else ''}"
    )
    if not prov_rate_ok:
        bad.append(("<C4未验证超上界>", False, False, False, False, tot_diff,
                    [], [], []))
    lines.append(
        f"C4 像素代理（**仅筛选器，不参与 ok**）：偏红 >= {RED_SUSPECT * 100:.0f}% 的样件 "
        f"{n_red_suspect} 张，已逐份列出待人工确认"
    )
    lines.append(
        "  ⚠ 本项**只是可核代理指标**：偏红残余可能来自照片本身的暖色（石质/木质），"
        "**不是水印**；目视结论须由人工给出。"
    )
    # **不说"全通过"**：凡是结论由部分样本支撑的地方，都给覆盖数（复核 2026-09-24
    # 的要求）。C1/C2/C3 的覆盖面是全样本（逐份/逐张量过），C4 第二层不是——
    # 故这里逐条印覆盖数，而不是一句"全通过"。
    lines.append(f"C1/C2/C3/C4（机器可核）本批判定: {not bad}")
    lines.append(
        f"  覆盖数：C1 图注 {tot_want} 条 / 产出 {tot_png} 张（**逐份**比对）· "
        f"C2/C3 **逐张**（{tot_png} 张）· C4 机制层 **逐份**（{len(pdfs)} 份）· "
        f"C4 来源层 **已验证 {len(pdfs) - n_c4_unverified}/{len(pdfs)}，"
        f"未验证 {n_c4_unverified}**（上界 {PROV_UNVERIFIED_CEILING * 100:.0f}%）· "
        f"C4 像素代理**只是筛选器**（{n_red_suspect} 张待人工），不构成结论"
    )
    if bad:
        lines.append("失败明细（C1 差额须逐条解释，不得静默）:")
        for stem, c1, c2, c3, c4, diff, blank, missing_cap, leftover in bad:
            lines.append(
                f"  {stem}: C1={c1}(差额{diff}) C2={c2} C3={c3} C4={c4} "
                f"空图={blank} 缺图注={missing_cap} 残留水印流={leftover}"
            )

    # ---- 人工目视闸门（**不并入 ok**，理由见模块 docstring）----
    lines.append("=" * 72)
    lines.append("C4 人工目视闸门（**只能由人工写入，本脚本只读**）")
    visual_ok = False
    if VISUAL.is_file() and VISUAL.read_bytes().strip():
        visual_ok = True
        lines.append(report.rel(VISUAL) + " 逐字存档：")
        lines.append(VISUAL.read_bytes().decode("utf-8").rstrip())
        lines.append(f"  （刻意不由本脚本生成——本报告每次重跑都会被重写）")
    else:
        lines.append(
            f"  C4 人工目视闸门: FAIL（未判定）—— 缺 {report.rel(VISUAL)} ← **待人工目视**"
        )
        lines.append(
            "  本脚本不得声称「已目视确认」（它看不了图）。人工须逐张打开"
            " tests/papers/reports/c4-*.png 核对有无「校苑数模公众号」字样，"
            "把结论写进该文件；缺了则本闸门判 FAIL。"
        )
    lines.append(
        "  本行**不并入 RESULT**：RESULT 只覆盖机器可核判据。理由见本文件 docstring"
        "（Step 4 要求全量跑在人工介入前即得 RESULT: PASS；把人工项并进去会让那一行"
        "在人工写入前恒为 FAIL，与恒真的判据同罪）。"
        f"机读值 visual_ok={visual_ok}"
    )
    if visual_ok:
        lines.append("发布放行: 已放行（人工目视已判定，逐字存档见上）")
    else:
        lines.append(
            "发布放行: **未放行** —— C4 人工目视项未判定时，**Task 5 不得开工**"
            "（用户侧的闸门，不是本脚本能否通过的判据）"
        )
    return not bad


def main() -> int:
    import argparse

    from tools.papers import report

    ap = argparse.ArgumentParser(
        description="图表判据 C1/C2/C3/C4（图注计数 / 空图 / 图注随图 / 图无水印）",
    )
    ap.add_argument(
        "--limit", type=report.limit_arg, default=0, metavar="N",
        help="只跑前 N 份 + 见证集（变异演示用，秒级）。报告按 report_path 选定的"
             "落点写到 tests/papers/reports-limited/（不入库）；"
             "0 = 全量（默认，写放行证据 tests/papers/reports/c-report.txt）；"
             "负数不接受（会被当成全量跑从而绕过反向落点守卫）",
    )
    args = ap.parse_args()

    # 落点先定下来（含 fail-closed 守卫，两个方向都守）
    out, guard_msg = report.resolve_report("c", args.limit)
    # 跑前量一次放行证据的 sha256，**落盘之后**再量一次作对账（顺序要紧：
    # 写成"量完再写"量到的是覆写**之前**的字节，判据会对着已经被覆写的事实报 True）。
    # 全量跑不适用：那一次的产物就是这份证据，它本来就该变。
    # 已知边界：只盯得住本进程；并发的另一次全量跑同时写它时看不出来。
    pre = report.sha256_of(report.release_path("c")) if args.limit > 0 else ""

    meta: dict = {}
    lines = ["图表抽取校验（C1/C2/C3/C4）"]
    if guard_msg:
        lines.append(guard_msg)
    try:
        ok = checks(lines, args.limit, meta, out, report)
    except BaseException as e:
        lines.append("校验过程中抛出异常：")
        lines.append(report.fmt_exc(e))
        ok = False

    # 写前复核（第二道，紧贴 write_bytes）：决策点可以被改坏调用点绕过去。
    out, msg2 = report.recheck_target("c", args.limit, out)
    if msg2:
        lines.append(msg2)
    # **这一句不能省**：守卫消息只是往报告里写了"FAIL"，不并进 ok 的话
    # RESULT 行照样打印 PASS、退出码照样是 0——判据说了话而结论不听。
    if guard_msg or msg2:
        ok = False

    lines.append("")
    lines.append(f"写入：{report.rel(out)}")
    if args.limit > 0:
        if out == report.release_path("c"):
            lines.append(
                f"  本次是**限样本跑**（--limit {args.limit}），但**实际落点就是放行证据**"
                f" 本体——落点判据被改坏或被绕过，见本报告中的落点守卫 FAIL 消息，判 FAIL。"
            )
        else:
            lines.append(
                f"  本文件是**限样本跑**（--limit {args.limit} + 见证集 "
                f"{'/'.join(FOCUS)}）的报告，**不入库、不是放行依据**；放行证据是 "
                f"{report.rel(report.release_path('c'))}，只有全量跑会写它。"
            )
    else:
        lines.append(
            f"  本文件是**全量跑的放行证据**（入库）——前半句由本次运行的落点自证；"
            f"全量侧另有镜像落点守卫（`limit <= 0` 而落点不是本文件时，写前复核会把它"
            f"改写回本文件并判 FAIL）。限样本跑的落点**按设计**是 "
            f"{report.rel(report.LIMITED_DIR)}/ 下的另一份文件——**后半句是关于别的"
            f"运行的承诺，本次运行不检查它**：它由限样本侧的守卫与写前复核保证，"
            f"强度止于「**决策点**被改坏就判 FAIL 并改写落点；**整个绕开调用点**"
            f"（M-L2 的形状）则限样本跑确实会写进放行证据本体、只判 FAIL 而不改写」，"
            f"不是「物理上写不进来」。"
        )

    text = "\n".join(lines) + "\n"
    # 自检（fail-closed）：报告只许带仓库相对路径。**崩溃那一次最容易破**，
    # 故做成每次都当场量、当场判的判据。
    dirty = report.path_audit(text)
    if dirty:
        text += (
            f"\n报告里出现绝对路径痕迹 {dirty!r}"
            f"——违反「报告只带仓库相对路径」，判 FAIL\n"
        )
        ok = False

    # 先落盘，**然后**才量放行证据（顺序见上面 pre 的注释）
    report.flush(out, text)
    if args.limit > 0:
        post = report.sha256_of(report.release_path("c"))
        same = pre == post
        ok = ok and same
        text += "\n" + "\n".join([
            f"放行证据完整性自检（只对限样本跑做）· {report.rel(report.release_path('c'))}",
            f"  本次跑前 sha256 = {pre}",
            f"  本次跑后 sha256 = {post}",
            f"  两次相同 = {same}（False → 本次限样本跑碰到了全量放行证据，判 FAIL）",
        ]) + "\n"

    # RESULT 行放在最后、且在自检之后才算 ok：结论行必须反映**全部**机器判据。
    text += (
        f"\nRESULT: {'PASS' if ok else 'FAIL'}"
        f"{report.result_suffix('c', args.limit, meta, FOCUS)}\n"
    )
    report.flush(out, text)
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
