#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-summary.py -- MCM/ICM 摘要页自检工具（mcm-abstract skill 随附）

用途
----
输入一份**只含摘要页**的 .tex（= 官方模板 + 填好的摘要，没有正文），一次跑完给出：

  A. 页眉三栏是否填实（题号 / 队号 / 年份 2027）
  B. 用 pdfLaTeX 编两遍 -> 硬错误数、PDF 路径、页数；超页时给末页填充率与要砍的字数
  C. 机械扫描 6 类"编译不报错但静默出错"的写法（C1 见下；C6 见"§C6 的判据"）

**本工具只判形式。** 页数 / 页眉 / 机械错误这层它管；**内容、措辞、取舍它一概不管** ——
一份"数字是编的 + 引言逐字搬"的摘要同样能拿到 `RESULT: PASS`。
⇒ `RESULT: PASS` **不代表摘要可交付**；质量层必须按 `SKILL.md`「必须自检」的逐条清单人工打勾。

依赖：Python 3 标准库 + PyMuPDF(fitz)；需要 PATH 里有 pdflatex（pdfLaTeX，不是 xelatex）。

输出为中文、机读友好：每行形如 `键=值` 或 `检查项: PASS/FAIL`。
最后一行 `RESULT: PASS|FAIL`；退出码 0=PASS，1=FAIL（编译失败也算 FAIL）。

用法
----
    python check-summary.py summary.tex
    python check-summary.py summary.tex --pdf out/check.pdf
    python check-summary.py summary.tex --keep-temp

--keep-temp 保留临时目录（.aux/.log 等中间产物留给人看）；默认清理。
PDF 默认写到 `<输入目录>/<输入名>-check.pdf`，路径在 `PDF=` 行给出，
供 agent 用 Read 直接看那一页（.aux/.log 不会撒进仓库）。

判据只读产物
------------
A 的结论**取自编译出来的 PDF 第 1 页文字**（三栏字样 + 从页眉抽出的题号/队号/年份原文字符串），
不取自 .tex 源码 —— 宏写法不是标准，"渲染出来那一页显示什么"才是。
源码侧的宏/页眉栏检查只作 `[辅助诊断]` 打印，不参与判定。

已知坑与修法（换机器/换用户仍会踩，勿删）
------------------------------------------
1. **Windows 上 `tempfile.mkdtemp()` 可能返回 8.3 短名，而 pdfTeX 打不开含 `~` 的路径。**
   本机实测：`%TEMP%` 即 `C:\\Users\\SHAMEL~1\\AppData\\Local\\Temp`，首次实现直接把该路径
   传给 pdflatex，得到 `! I can't find file `C:/Users/SHAMEL'.`，**只产出 texput.log、
   输入文件从未被打开**（日志在 `**C:/Users/SHAMEL~` 处断行）—— 看起来像"编译失败"，
   其实输入根本没读进去。修法：`make_workdir()` 建好目录后用 `ctypes.GetLongPathNameW`
   解析成长名，并在候选目录里排除仍含 `~` 的；实在不行退到当前工作目录下再建。
2. **末页页码块会污染"末页填充率"。** 第 2 页的页码坐在 y≈740.8-752.8，**低于正文栏底
   722.5**（`bottom=1in` → 792-72=720）。若直接取"全页文字 bbox"，栏高会被算大、填充率被算小。
   修法（`page_blocks()`）：先取该页**最高**的文字块为正文主块，剔除 ① 整块落在主块顶之上的
   （页眉三栏的标签与红字值都是独立小块）② 页底 15% 内的裸数字（页码）③ 落在页眉区且含
   `Problem Chosen`/`Team Control Number`/`Summary Sheet` 的小块。剔除后 A1 栏高 = 647.6pt，
   与 `build/abs-red/tex-pdf/_measure.json` 口径一致。
3. **CRLF 本身无害**（实测：合规摘要转 CRLF 后仍 rc=0 / RESULT: PASS）——不要为 Windows 换行报警。

扫描面的两个例外（避免"带已知误报的检查器训练人忽略它"）
--------------------------------------------------------
`NON_TYPESET_ARGS` 里那些命令的**第一个 `{...}` 参数不排版**，其中的 `_` `^` `|` 是合法的，
不计入违规、也不计入 C7：
  - `\\includegraphics{plot_1.pdf}` 的 `_`（文件名）   -> 曾误报为 C2
  - `\\begin{tabular}{|c|c|}` 的 `|`（列格式说明）      -> 曾误报为 C5
  - 同类：`\\label` `\\ref` `\\cite` `\\input` `\\usepackage` ...
**只跳过第一个参数**（`\\href{url}{text}` 的第二个参数要排版，不跳）；
正文散文里的裸 `|` `_` `^` 照旧报 —— 收敛假阳性不得放过真违规。

C1 的判据：为什么不是"见 % 就报"
---------------------------------
LaTeX 里 `%` **永远**是注释符，所以"误写的 `95% of the wear`"与"有意写的行尾注释
`\\graphicspath{{.}}  % Place your...`"在语法上**同形**，只能按书写惯例分辨。
实测依据（这是判据的来源，别凭感觉改）：
  - RED 三份 raw 源 `build/abs-red/red-{A1,A2,C1,P1,P2}.md` 里**全部**误用形态都
    **紧贴前一个字符**：`5% below`、`within 5%)`、`3.0%`、`48%)`、`0.01%,`
    —— **无一例带前置空白**；
  - 官方资产 `mcm-latex-format/assets/mcm-2027-summary.tex` 里的合法注释只有两种形态：
    `:59  \\graphicspath{{.}}  % Place your graphic files...`（**前置空白**）
    与 `:73  \\textcolor{red}{%`（**其后无内容**）。
判据 = 未转义 **且** `%` 紧贴前一字符 **且** `%` 后仍有非空白内容 ⇒ 计 C1，
并报出被吞字符数与内容（那是证据）。其余 `%` 计入 `C1b_行尾注释_不计违规`，只报数。
**已知漏报（已裁决接受，别"修"）**：`95 %`（数字与 `%` 之间有空格）这种误写抓不到。
这是"不误报合法注释"的**必然代价** —— 合法注释**大量**是"前置空白"形态
（官方资产 `:59` 就是），若为抓 `95 %` 而判"前置空白也算违规"，会立刻把官方资产
自己判红，即重新引入刚修掉的那个假阳性。取舍已定：**宁可漏 `95 %`，不可误报合法注释。**

**已知误报（已裁决接受，不加豁免）**：`\\foo%comment`（有意紧贴、用于吃掉行尾空格的
惯用法）会被计 C1。**为什么不为它加规则**：摘要页正文是散文，这种惯用法多出现在宏定义里；
官方模板里同类形态（`\\textcolor{red}{%`）是"行尾"而非"紧贴+尾随内容"，已被豁免；
为一个**尚未遇到**的形态加规则会削弱真违规拦截，且边界要重新定。
**遇到时的绕法**：把该注释移到独立行，或改成带前置空格的 `  % ...` 形态（两种都不会被判违规）。
C1>0 时报告会打印一行 `提示=` 把这条绕法当场告诉人，免得使用者去怀疑工具。

C6 的判据：为什么不是"见 ~ 就报"
---------------------------------
`~` 在 LaTeX 里是**不断行空格**，本身是合法排版手段（`Fig.~1`、`12~pt`、`Dr.~Smith`
都是标准用法）；但若作者想写的是"约"（`~48%` = about 48%），`~` 在页面上会**消失**、
把"约 48%"变成"48%"—— **语义被悄悄改掉**，编译不报错。两者同形，只能按上下文分辨。
实测依据（判据的来源，别凭感觉改）：
  - **必须抓**：`tests/skills/abs-cases/red/red-A2.md:73` 的 `~48%`
    —— 作者本意是"约"（同句还有 "changes long-run wear by ~48%"），`~` 在页面上消失。
  - **不该判违规（复审实测）**：`Fig.~1 and 12~pt type; Dr.~Smith` —— 三个都是合法的不断行空格。
判据 = 未转义 **且** 文本模式 **且** `~` **前是空白（或行首）** **且** `~` **后是数字**
⇒ 计 `C6`；其余 `~` 计入 `C6b_不断行空格_不计违规`，只报数。
四例（一违规三合法）逐例实测见 `tests/skills/abs-green-evidence.md` §7。
**遇到 C6 怎么改**：`~` 作"约"讲时写成数学符号 `$\sim$`（如 `$\sim$48\%`）；
合法的不断行空格可保留原样。

已知边界（未实现 / 未覆盖，如实登记，别当成 bug 再"修"一遍）
------------------------------------------------------------
- `resolve_refs()` **只扫顶层文件正文，不递归 `\\input` 进来的子文件**：若顶层
  `\\input{extra}` 而 `extra.tex` 内部又 `\\includegraphics{fig2}`，则 `fig2` 不会被拷
  （`extra.tex` 本身会被拷）。**摘要页没有 `\\input`，故对本 skill 的用途无影响**；
  只有把本工具拿去跑含 `\\input` 的正文 `.tex` 时才会碰到。
- `\\graphicspath` 指向**源目录之外**（如 `{../shared/}`）时，拷贝会退化成"只拷文件名到
  临时目录根、相对路径可能对不上"。**未覆盖、未实测**（实测过的只有 `{figs/}` 这类
  源目录内的写法）。摘要页不用图，故不影响本 skill。

可重放性（判据可当基准）
------------------------
同一份输入连跑两遍，报告数字应逐位相同（页数 / 填充率 / 栏高 / C1-C7 计数 / 拷贝清单）。
报告里**不含**临时目录名与时间戳：临时目录路径只在 `--keep-temp` 时才打印，编译日志的
时间戳（`This is pdfTeX ... <日期>`）从不进入报告。`边界=` 一行常驻（不条件打印）——
口径写在每次输出里，比藏在 docstring 里更不容易被误读。
"""

import argparse
import bisect
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    sys.stderr.write("错误: 需要 PyMuPDF(fitz)。安装: python -m pip install PyMuPDF\n")
    sys.exit(2)


# --------------------------------------------------------------------------
# 常量 / 正则
# --------------------------------------------------------------------------

ESC_LITERALS = set("%_^$&#{}~")          # 可被 \ 转义的字符
HEADER_MARKERS = re.compile(r"Problem Chosen|Team Control Number|Summary Sheet", re.I)

# 第一个参数不排版的命令 —— 其中的 _ ^ | 是合法的，跳过不计违规（见模块 docstring）
NON_TYPESET_ARGS = {
    "includegraphics", "begin", "end", "label", "ref", "eqref", "pageref",
    "cite", "citep", "citet", "citeauthor", "citeyear", "nocite",
    "input", "include", "includeonly", "graphicspath", "DeclareGraphicsExtensions",
    "bibliography", "bibliographystyle", "addbibresource",
    "usepackage", "documentclass", "RequirePackage",
    "newcommand", "renewcommand", "providecommand", "def",
    "url", "path", "lstinputlisting", "verbatiminput", "includepdf",
}

# 这些命令**所有**连续的 {...} 参数都不排版（环境名 + 位置/列格式说明）
# 例：\begin{tabular}{|c|c|} 有 {tabular} 与 {|c|c|} 两个参数，两个都要跳
ALL_ARGS_COMMANDS = {"begin", "end"}

# A: 宏定义形式（官方模板为 \newcommand{\Problem}{ABCDEF}）
RE_MACRO_DEF = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand)\s*\{\s*\\(Problem|Team)\s*\}"
    r"\s*(?:\[[^\]]*\]\s*)?\{([^{}]*)\}"
)
RE_MACRO_DEF2 = re.compile(r"\\def\s*\\(Problem|Team)\s*\{([^{}]*)\}")
RE_TEAM_LHEAD = re.compile(r"\\lhead\s*\{[^}]*?\bTeam\s+([A-Za-z0-9]+)")
RE_TEXTCOLOR = re.compile(r"\\textcolor\s*\{[^}]*\}\s*\{([^{}]*)\}")
RE_LARGE_ARG = re.compile(r"\\Large\s*\{?([^\s\\&}%]*)")
RE_YEAR_NEAR_MCM = re.compile(r"(\d{4})\s*\\?\\?\s*$")
RE_ANY_YEAR = re.compile(r"\b(19|20)\d{2}\b")

# C
RE_MD_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
RE_MD_BOLD = re.compile(r"(?<!\\)\*\*")
RE_MD_HASH = re.compile(r"^\s*#")
RE_HTML_TAG = re.compile(r"</?[A-Za-z][A-Za-z0-9]*>")
RE_UNICODE_ERR = re.compile(r"U\+([0-9A-Fa-f]{4,6})")

# B: 只拷源码里**真正被引用**的文件（别把整目录图都拷进去）
RE_INCLUDEGRAPHICS = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}")
RE_INPUT_FILE = re.compile(r"\\(?:input|include)\s*\{([^{}]*)\}")
RE_GRAPHICSPATH = re.compile(r"\\graphicspath\s*\{((?:\s*\{[^{}]*\}\s*)+)\}")
GRAPHIC_EXTS = [".pdf", ".png", ".jpg", ".jpeg", ".eps", ".tif", ".tiff"]


# --------------------------------------------------------------------------
# 文本工具
# --------------------------------------------------------------------------

def build_line_starts(text):
    starts = [0]
    i = text.find("\n")
    while i != -1:
        starts.append(i + 1)
        i = text.find("\n", i + 1)
    return starts


def line_of(starts, off):
    return bisect.bisect_right(starts, off)  # 1-based


def skip_group(line, i):
    """line[i] == '{' -> 返回配对的 '}' 之后的下标；同行内扫不完整则 None。"""
    depth = 0
    j = i
    while j < len(line):
        c = line[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    return None


def skip_optional(line, i):
    """line[i] == '[' -> 返回 ']' 之后的下标；否则原样返回 i。"""
    if i < len(line) and line[i] == "[":
        j = line.find("]", i)
        if j != -1:
            return j + 1
    return i


def context_around(text, off, width=10):
    a = max(0, off - width)
    b = min(len(text), off + width + 1)
    return text[a:b].replace("\n", "\\n").replace("\r", "")


def long_path(p):
    """把 Windows 8.3 短名（如 C:\\Users\\SHAMEL~1\\...）展开成长名。

    必须做：pdfTeX 的命令行文件名解析器遇到 `~` 会把路径截断
    （实测 `! I can't find file `C:/Users/SHAMEL'.`，只产出 texput.log）。
    路径必须已存在。
    """
    p = Path(p)
    if os.name != "nt":
        return p
    try:
        import ctypes
        buf = ctypes.create_unicode_buffer(32768)
        n = ctypes.windll.kernel32.GetLongPathNameW(str(p), buf, 32768)
        if n and n < 32768:
            return Path(buf.value)
    except Exception:
        pass
    return p


def make_workdir():
    """建一个不含 `~` 的临时工作目录（pdfTeX 吃不下 `~`）。"""
    tried = []
    cands = [tempfile.gettempdir(), os.environ.get("TMP"), os.environ.get("TEMP")]
    for c in cands:
        if not c:
            continue
        try:
            d = long_path(Path(tempfile.mkdtemp(prefix="mcm-abs-check-", dir=c)))
        except OSError:
            continue
        tried.append(str(d))
        if "~" not in str(d):
            return d, tried
        shutil.rmtree(d, ignore_errors=True)
    # 兜底：当前工作目录下建（跑完会清理）
    d = long_path(Path(tempfile.mkdtemp(prefix=".mcm-abs-check-", dir=os.getcwd())))
    tried.append(str(d))
    return d, tried


def safe_stem(path):
    s = re.sub(r"[^A-Za-z0-9_-]", "_", path.stem)[:40]
    return s or "summary"


def resolve_refs(text, src_dir):
    """解析源码里真正被引用的文件（\\includegraphics / \\input / \\include）。

    返回 (rel_paths, unresolved)：rel_paths 是相对 src_dir 的路径（保目录结构，
    拷到临时目录后相对路径仍然成立）；unresolved 是抽不到/找不到的引用原文。
    """
    search_dirs = [src_dir]
    for m in RE_GRAPHICSPATH.finditer(text):
        for sub in re.findall(r"\{([^{}]*)\}", m.group(1)):
            if sub.strip():
                search_dirs.append(src_dir / sub.strip())

    found, unresolved = [], []

    def consider(raw, exts):
        raw = raw.strip()
        if not raw:
            return
        if "\\" in raw or "#" in raw:      # 宏/参数拼出来的路径
            unresolved.append(raw)
            return
        cands = [raw] if Path(raw).suffix else [raw + e for e in exts]
        for d in search_dirs:
            for c in cands:
                p = d / c
                if p.is_file():
                    try:
                        found.append(p.resolve().relative_to(src_dir.resolve()))
                    except ValueError:
                        found.append(Path(p.name))   # src_dir 之外，退化成文件名
                    return
        unresolved.append(raw)

    for m in RE_INCLUDEGRAPHICS.finditer(text):
        consider(m.group(1), GRAPHIC_EXTS)
    for m in RE_INPUT_FILE.finditer(text):
        consider(m.group(1), [".tex", ""])

    uniq = list(dict.fromkeys(found))
    return uniq, unresolved


def read_source(path):
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1(replace)"


# --------------------------------------------------------------------------
# C: 逐行状态机扫描（$..$ / $$..$$ 数学模式 + 转义 + 注释）
# --------------------------------------------------------------------------

def scan_mechanics(lines, body_start_line):
    """返回 (counts, details, nonascii_list)。

    lines: 正文区（\\begin{document} 之后到 \\end{document} 之前）的每一行。
    body_start_line: lines[0] 在**原文件**中的 1-based 行号。
    """
    counts = dict(c1=0, c1_exempt=0, c2=0, c3=0, c4=0, c5=0, c6=0, c6_exempt=0)
    details = {k: [] for k in counts}
    nonascii = []

    in_math = 0  # 0=文本 1=$..$ 2=$$..$$

    for idx, line in enumerate(lines):
        lineno = body_start_line + idx
        n = len(line)

        live = []          # (col, char, math_state, escaped?)
        comment_at = None
        i = 0
        while i < n:
            c = line[i]
            if c == "\\":
                nxt = line[i + 1] if i + 1 < n else ""
                if nxt == "(":
                    math_prev = in_math
                    in_math = 1
                    i += 2
                    continue
                if nxt == ")":
                    in_math = 0
                    i += 2
                    continue
                if nxt == "[":
                    in_math = 2
                    i += 2
                    continue
                if nxt == "]":
                    in_math = 0
                    i += 2
                    continue
                if nxt in ESC_LITERALS:      # \% \_ \^ \$ \& \# \{ \} \~
                    live.append((i, nxt, in_math, True))
                    i += 2
                    continue
                if nxt == "\\":              # \\ 换行
                    i += 2
                    continue
                j = i + 1
                while j < n and line[j].isalpha():
                    j += 1
                name = line[i + 1:j] if j > i + 1 else ""
                if name in NON_TYPESET_ARGS:
                    # 跳过参数区（其中的 _ ^ | 不排版，合法）
                    k = skip_optional(line, j)
                    skipped = False
                    while k < n and line[k] == "{":
                        e = skip_group(line, k)
                        if e is None:
                            break
                        k = e
                        skipped = True
                        if name not in ALL_ARGS_COMMANDS:
                            break            # 普通命令只跳第一个参数
                        k = skip_optional(line, k)
                    if skipped:
                        i = k
                        continue
                i = j if j > i + 1 else i + 2   # 控制词 / 控制符
                continue
            if c == "$":
                if in_math == 0:
                    if i + 1 < n and line[i + 1] == "$":
                        in_math = 2
                        i += 2
                    else:
                        in_math = 1
                        i += 1
                elif in_math == 1:
                    in_math = 0
                    i += 1
                else:                        # in_math == 2
                    if i + 1 < n and line[i + 1] == "$":
                        in_math = 0
                        i += 2
                    else:
                        i += 1
                continue
            if c == "%":
                comment_at = i
                break
            live.append((i, c, in_math, False))
            i += 1

        head_end = comment_at if comment_at is not None else n
        head = line[:head_end]

        # --- C1 疑似"误写的未转义 %"（会静默吞掉该行剩余内容）-------------
        # LaTeX 里 % **永远**是注释符：误写的 `95% of` 与有意写的行尾注释
        # `}}% comment` 在语法上同形，只能按书写惯例分辨。实测依据：
        #   - RED 三份 raw 源（red-A1/A2/C1/P1/P2.md）里**全部**误用形态都
        #     **紧贴前一个字符**：`5% below` `within 5%)` `3.0%` `48%)` `0.01%,`
        #     —— 无一例带前置空白；
        #   - 官方资产里的合法行尾注释是 `\graphicspath{{.}}  % Place your...`
        #     （**前置空白**）与 `\textcolor{red}{%`（**其后无内容**）。
        # 故判据 = 未转义 且 % **前紧邻字符非空白** 且 % **后仍有非空白内容**。
        if comment_at is not None:
            swallowed = line[comment_at + 1:]
            glued = comment_at > 0 and not line[comment_at - 1].isspace()
            if glued and swallowed.strip() != "":
                counts["c1"] += 1
                details["c1"].append(
                    "行=%d 列=%d 被吞字符数=%d 吞掉内容=%r"
                    % (lineno, comment_at + 1, len(swallowed), swallowed[:60])
                )
            else:
                counts["c1_exempt"] += 1      # 行尾注释 / 行首注释行，不计违规

        # --- C7 非 ASCII（只列不判违规；扫"活的"区域，注释不排版不算） ---
        for (col, ch, _m, _e) in live:
            if ord(ch) > 127:
                nonascii.append((lineno, col + 1, ch, context_around(line, col)))

        is_table_row = bool(RE_MD_TABLE_ROW.match(head)) and head.count("|") >= 2

        # --- C3 markdown 残留 -------------------------------------------
        if RE_MD_HASH.match(head):
            counts["c3"] += 1
            details["c3"].append("行=%d 行首# %r" % (lineno, head.strip()[:60]))
        for m in RE_MD_BOLD.finditer(head):
            counts["c3"] += 1
            details["c3"].append("行=%d 列=%d markdown粗体 ** %r"
                                 % (lineno, m.start() + 1, context_around(line, m.start())))
        if is_table_row:
            counts["c3"] += 1
            details["c3"].append("行=%d markdown表格行 %r" % (lineno, head.strip()[:60]))

        # --- C4 HTML 残留 ----------------------------------------------
        for m in RE_HTML_TAG.finditer(head):
            counts["c4"] += 1
            details["c4"].append("行=%d 列=%d HTML标签 %r"
                                 % (lineno, m.start() + 1, m.group(0)))

        # --- C2 / C5 / C6：文本模式下、未转义的裸字符 --------------------
        for (col, ch, mstate, esc) in live:
            if esc or mstate != 0:
                continue
            if ch == "_" or ch == "^":
                counts["c2"] += 1
                details["c2"].append("行=%d 列=%d 裸 %r 上下文=%r"
                                     % (lineno, col + 1, ch, context_around(line, col)))
            elif ch == "|":
                if is_table_row:
                    continue          # 已按 markdown 表格行报过（C3）
                counts["c5"] += 1
                details["c5"].append("行=%d 列=%d 裸 | 上下文=%r"
                                     % (lineno, col + 1, context_around(line, col)))
            elif ch == "~":
                # C6 判据 = `~` 前是空白（或行首）且 `~` 后是数字 ⇒ 像是把"约"写成了 ~；
                # 其余（Fig.~1 / 12~pt / Dr.~Smith）是合法不断行空格，只报数不判违规。
                prev = line[col - 1] if col > 0 else ""
                nxt = line[col + 1] if col + 1 < n else ""
                if (prev == "" or prev.isspace()) and nxt.isdigit():
                    counts["c6"] += 1
                    details["c6"].append("行=%d 列=%d 裸 ~ 上下文=%r"
                                         % (lineno, col + 1, context_around(line, col)))
                else:
                    counts["c6_exempt"] += 1

    return counts, details, nonascii


# --------------------------------------------------------------------------
# B: 编译 + PDF 几何
# --------------------------------------------------------------------------

def run_pdflatex(tex_path, workdir):
    exe = shutil.which("pdflatex")
    if exe is None:
        return None, None, "PATH 里找不到 pdflatex"
    log = []
    rc_last = None
    for pass_no in (1, 2):
        cmd = [exe, "-interaction=nonstopmode", "-output-directory", str(workdir),
               str(tex_path)]
        p = subprocess.run(cmd, cwd=str(workdir), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        rc_last = p.returncode
        log.append(p.stdout.decode("utf-8", errors="replace"))
    return rc_last, log, None


def parse_log(log_text):
    hard = []
    for ln in log_text.splitlines():
        if ln.startswith("!"):
            hard.append(ln.rstrip())
    # `!  ==> Fatal error occurred...` 是后果行，不算独立错误
    real = [h for h in hard if not h.startswith("!  ==>") and not h.startswith("! ==>")]
    first_ctx = []
    if real:
        i = log_text.find(real[0])
        first_ctx = [ln for ln in log_text[i:i + 400].splitlines() if ln.strip()][:3]
    unicode_cps = []
    for ln in log_text.splitlines():
        if "Unicode character" in ln or "Unicode" in ln and "U+" in ln:
            for m in RE_UNICODE_ERR.finditer(ln):
                cp = "U+" + m.group(1).upper()
                if cp not in unicode_cps:
                    unicode_cps.append(cp)
    return hard, real, first_ctx, unicode_cps


def page_blocks(page):
    """返回该页的"正文"文字块，剔除 (a) 页码块 (b) 页眉三栏块。"""
    H = page.rect.height
    blocks = [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]
    if not blocks:
        return []
    main = max(blocks, key=lambda b: b[3] - b[1])        # 最高的块 = 正文主块
    kept = []
    for b in blocks:
        if b is main:
            kept.append(b)
            continue
        if b[3] <= main[1] + 1.0:                         # 整块落在正文顶之上 => 页眉
            continue
        txt = b[4].strip()
        if re.fullmatch(r"\d+", txt) and b[1] > 0.85 * H:  # 页底裸页码
            continue
        if (b[3] - b[1]) < 0.25 * H and HEADER_MARKERS.search(txt):
            continue
        kept.append(b)
    return kept


def page_body_stats(page):
    bl = page_blocks(page)
    if not bl:
        return None
    y0 = min(b[1] for b in bl)
    y1 = max(b[3] for b in bl)
    txt = "".join(b[4] for b in bl)
    nchar = len(re.sub(r"\s+", "", txt))
    return dict(y0=y0, y1=y1, h=y1 - y0, nchar=nchar)


# --------------------------------------------------------------------------
# A: 页眉三栏
# --------------------------------------------------------------------------

def find_header_cell_value(text, label):
    """在 `label` 之后的小窗口里找 \\textcolor{..}{VALUE} 或 \\Large VALUE。"""
    m = re.search(label, text, re.I)
    if not m:
        return None, None
    seg = text[m.end():m.end() + 300]
    seg = seg.split("&")[0]
    tm = RE_TEXTCOLOR.search(seg)
    if tm:
        return tm.group(1).strip(), m.start()
    lm = RE_LARGE_ARG.search(seg)
    if lm:
        return lm.group(1).strip(), m.start()
    return None, m.start()


def check_header(text, starts):
    """返回 (results, raw_values)。results: list of (name, ok, msg)"""
    res = []
    vals = {}

    # ---- \Problem ----
    src, val, off = None, None, None
    for rx in (RE_MACRO_DEF, RE_MACRO_DEF2):
        for m in rx.finditer(text):
            if m.group(1) == "Problem":
                val, off, src = m.group(2).strip(), m.start(), "宏定义"
                break
        if val is not None:
            break
    if val is None:
        v2, o2 = find_header_cell_value(text, r"Problem\s+Chosen")
        if v2:
            val, off, src = v2, o2, "页眉栏内容(未用 \\Problem 宏)"
    vals["problem"] = (val, src, off)
    if val is None:
        res.append(("Problem_Chosen", False, "未找到 \\Problem 宏，也未在页眉栏找到题号"))
    elif val == "ABCDEF":
        res.append(("Problem_Chosen", False,
                    "仍为模板占位符 ABCDEF（%s）" % src))
    else:
        res.append(("Problem_Chosen", True, "值=%s（来源=%s）" % (val, src)))

    # ---- \Team ----
    src, val, off = None, None, None
    for rx in (RE_MACRO_DEF, RE_MACRO_DEF2):
        for m in rx.finditer(text):
            if m.group(1) == "Team":
                val, off, src = m.group(2).strip(), m.start(), "宏定义"
                break
        if val is not None:
            break
    if val is None:
        m = RE_TEAM_LHEAD.search(text)
        if m:
            val, off, src = m.group(1), m.start(), "\\lhead{Team ...}"
    if val is None or val == r"\Team":
        v2, o2 = find_header_cell_value(text, r"Team\s+Control\s+Number")
        if v2:
            val, off, src = v2, o2, "页眉栏内容(未用 \\Team 宏)"
    vals["team"] = (val, src, off)
    if val is None:
        res.append(("Team_Control_Number", False, "未找到 \\Team 宏，也未在页眉栏找到队号"))
    elif val == "1111111":
        res.append(("Team_Control_Number", False,
                    "仍为模板占位符 1111111（%s）" % src))
    else:
        res.append(("Team_Control_Number", True, "值=%s（来源=%s）" % (val, src)))

    # ---- 年份 2027（摘要标题栏） ----
    year, yoff = None, None
    for m in re.finditer(r"MCM\s*/\s*ICM", text):
        back = text[max(0, m.start() - 80):m.start()]
        ym = None
        for cand in RE_ANY_YEAR.finditer(back):
            ym = cand
        if ym:
            year = ym.group(0)
            yoff = max(0, m.start() - 80) + ym.start()
            break
    vals["year"] = (year, "MCM/ICM 标题栏" if year else None, yoff)
    if year is None:
        res.append(("年份_2027", False, "在 MCM/ICM 标题栏前未找到 4 位年份"))
    elif year != "2027":
        res.append(("年份_2027", False, "标题栏年份=%s（应为 2027）" % year))
    else:
        res.append(("年份_2027", True, "值=2027"))

    return res, vals


# --------------------------------------------------------------------------
# A（判据=编译出的 PDF 第 1 页文字）
# --------------------------------------------------------------------------

A_ITEM_NAMES = ["A1_三栏字样齐全", "A2_Problem_Chosen", "A3_Team_Control_Number",
                "A4_年份_2027"]

# 失败时给"人能照着做"的修法；页眉版式这一项的边界也写在这里
HINT_LACK_PDF = ("先让 B 段编译通过（rc=0 且产出 PDF），再来核页眉——"
                 "本项判据是产物，没有产物就无从核验")
HINT_HEADER = ("用官方模板的摘要页版式（Problem Chosen / MCM/ICM Summary Sheet / "
               "Team Control Number 三栏），不要自造页眉；见 mcm-latex-format 的 "
               "assets/mcm-2027-summary.tex")
HINT_PROBLEM = ("在 \\Problem 宏里填所选题号（官方模板 \\newcommand{\\Problem}{ABCDEF}），"
                "如 \\newcommand{\\Problem}{A}；不要留 ABCDEF")
HINT_TEAM = ("把队号填进 \\Team 宏（官方模板 \\newcommand{\\Team}{1111111}），"
             "如 \\newcommand{\\Team}{1234567}；不要留 1111111")
HINT_YEAR = ("把标题栏年份写成 2027（官方模板原件漏改为 2026，本项目采用侧取 2027）")
BOUNDARY_HEADER = ("本项只看「渲染出来那一页显示什么」；**不判**自造版式是否也算合规——"
                   "那属于 mcm-latex-format 与官方模板的判据，不在本工具的判据范围内")


def header_words(page):
    """第 1 页页眉区的词（含 bbox），页眉区 = 正文主块顶以上。"""
    blocks = page_blocks(page)
    body_top = min((b[1] for b in blocks), default=page.rect.height)
    ws = [w for w in page.get_text("words") if w[3] <= body_top + 0.5]
    ws.sort(key=lambda w: (round(w[1], 1), w[0]))
    return ws


def find_label(words, parts):
    """找由若干相邻词组成的标签，返回 (bbox, 原文字符串) 或 (None, None)。"""
    k = len(parts)
    for i in range(len(words) - k + 1):
        cand = words[i:i + k]
        if not all(parts[t].lower() in cand[t][4].lower() for t in range(k)):
            continue
        cys = [(w[1] + w[3]) / 2 for w in cand]
        if max(cys) - min(cys) > 3:            # 不在同一行
            continue
        return ((min(w[0] for w in cand), min(w[1] for w in cand),
                 max(w[2] for w in cand), max(w[3] for w in cand)),
                " ".join(w[4] for w in cand))
    return None, None


def value_below(words, bbox, max_gap=30.0, slack=20.0):
    """取标签正下方同一列的那一行词，拼成字符串。"""
    if bbox is None:
        return None
    x0, y0, x1, y1 = bbox
    cands = [w for w in words
             if y1 - 1 <= w[1] <= y1 + max_gap
             and x0 - slack <= (w[0] + w[2]) / 2 <= x1 + slack]
    if not cands:
        return None
    top = min(w[1] for w in cands)
    line = sorted([w for w in cands if w[1] <= top + 3], key=lambda w: w[0])
    return "".join(w[4] for w in line)


def year_above(words, mcm):
    """MCM/ICM 词正上方同一列的那一行（标题栏年份）。"""
    if mcm is None:
        return None
    x0, y0, x1, y1 = mcm[:4]
    cx = (x0 + x1) / 2
    cands = [w for w in words
             if w[3] <= y0 + 1 and y0 - w[3] < 22
             and abs((w[0] + w[2]) / 2 - cx) < 70]
    if not cands:
        return None
    bottom = max(w[3] for w in cands)
    line = sorted([w for w in cands if w[3] >= bottom - 3], key=lambda w: w[0])
    return "".join(w[4] for w in line)


def check_header_pdf(page):
    """从第 1 页 PDF 文字核验页眉四件事。返回 [(name, ok, msg, hint)]"""
    words = header_words(page)
    res = []

    lab_p, txt_p = find_label(words, ["Problem", "Chosen"])
    lab_t, txt_t = find_label(words, ["Team", "Control", "Number"])
    lab_s, txt_s = find_label(words, ["Summary", "Sheet"])
    mcm = next((w for w in words if "MCM" in w[4].upper()), None)

    # ① 三栏字样齐全
    missing = [n for n, t in (("Problem Chosen", txt_p), ("Summary Sheet", txt_s),
                              ("Team Control Number", txt_t)) if not t]
    if missing:
        res.append((A_ITEM_NAMES[0], False,
                    "PDF 页眉缺栏: %s" % "/".join(missing), HINT_HEADER))
    else:
        res.append((A_ITEM_NAMES[0], True,
                    'PDF 抽出="%s" | "%s" | "%s"' % (txt_p, txt_s, txt_t), None))

    # ② Problem Chosen 的值
    pv = value_below(words, lab_p)
    if pv is None:
        res.append((A_ITEM_NAMES[1], False,
                    "PDF 页眉里 Problem Chosen 下方抽不到值", HINT_PROBLEM))
    elif pv == "ABCDEF":
        res.append((A_ITEM_NAMES[1], False,
                    'PDF 抽出值="%s"（模板占位符，题号未填）' % pv, HINT_PROBLEM))
    elif re.fullmatch(r"[A-Fa-f]", pv):
        res.append((A_ITEM_NAMES[1], True, 'PDF 抽出值="%s"' % pv, None))
    else:
        res.append((A_ITEM_NAMES[1], False,
                    'PDF 抽出值="%s"（不是单个字母 A-F）' % pv, HINT_PROBLEM))

    # ③ Team Control Number 的值
    tv = value_below(words, lab_t)
    if tv is None:
        res.append((A_ITEM_NAMES[2], False,
                    "PDF 页眉里 Team Control Number 下方抽不到值", HINT_TEAM))
    elif tv == "1111111":
        res.append((A_ITEM_NAMES[2], False,
                    'PDF 抽出值="%s"（模板占位符，队号未填）' % tv, HINT_TEAM))
    elif re.fullmatch(r"\d+", tv):
        res.append((A_ITEM_NAMES[2], True, 'PDF 抽出值="%s"' % tv, None))
    else:
        res.append((A_ITEM_NAMES[2], False,
                    'PDF 抽出值="%s"（不是数字）' % tv, HINT_TEAM))

    # ④ 标题栏年份
    yv = year_above(words, mcm)
    if yv is None:
        res.append((A_ITEM_NAMES[3], False,
                    "PDF 标题栏 MCM/ICM 上方抽不到年份", HINT_YEAR))
    elif yv != "2027":
        res.append((A_ITEM_NAMES[3], False,
                    'PDF 抽出值="%s"（应为 2027）' % yv, HINT_YEAR))
    else:
        res.append((A_ITEM_NAMES[3], True, 'PDF 抽出值="2027"', None))
    return res


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="MCM/ICM 摘要页自检：页眉三栏 / pdfLaTeX 编译与页数 / 机械扫描",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n  python check-summary.py summary.tex\n"
               "  python check-summary.py summary.tex --pdf build/check.pdf --keep-temp\n")
    ap.add_argument("tex", help="只含摘要页的 .tex 文件（官方模板 + 填好的摘要）")
    ap.add_argument("--pdf", default=None,
                    help="把检查用 PDF 拷到该路径（默认 <输入名>-check.pdf，与输入同目录）")
    ap.add_argument("--keep-temp", action="store_true",
                    help="保留临时目录（.aux/.log 等中间产物）")
    args = ap.parse_args()

    src_path = Path(args.tex).resolve()
    if not src_path.is_file():
        sys.stderr.write("错误: 找不到文件 %s\n" % src_path)
        return 1

    text, enc = read_source(src_path)
    starts = build_line_starts(text)

    print("== 输入 ==")
    print("文件=%s" % src_path)
    print("编码=%s" % enc)
    print("总行数=%d" % (text.count("\n") + 1))

    # ---- 正文区（\begin{document} .. \end{document}）----
    mb = re.search(r"\\begin\s*\{document\}", text)
    me = re.search(r"\\end\s*\{document\}", text)
    if not mb:
        print("正文区起始行=(未找到 \\begin{document})")
        body_lines, body_start_line = [], 1
    else:
        b0 = text.find("\n", mb.end())
        b0 = mb.end() if b0 == -1 else b0 + 1
        b1 = me.start() if me else len(text)
        body_start_line = line_of(starts, b0)
        body_lines = text[b0:b1].split("\n")
        print("正文区起始行=%d" % body_start_line)
        print("正文区结束行=%d" % (line_of(starts, b1) if me else -1))
    print("正文区行数=%d" % len(body_lines))

    # ======================= C（先算好，稍后打印）=======================
    c_counts, c_details, nonascii = scan_mechanics(body_lines, body_start_line)

    # ======================= 源码侧辅助诊断（不参与判定）================
    a_src_res, a_src_vals = check_header(text, starts)

    # ======================= B 编译（输出先缓存：A 的判据取自它产出的 PDF）=
    b_lines = []
    b_fail = []
    a_res = None
    emit = b_lines.append
    tmpdir, tried = make_workdir()
    if "~" in str(tmpdir):
        emit("警告=临时目录路径含 `~`（%s），pdfTeX 可能拒绝打开输入文件" % tmpdir)
    jobname = safe_stem(src_path)
    try:
        work_tex = tmpdir / (jobname + ".tex")
        shutil.copyfile(src_path, work_tex)
        # 只拷源码里真正被引用的文件；抽不到的如实报，别静默
        refs, unresolved = resolve_refs(text, src_path.parent)
        for rel in refs:
            dest = tmpdir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_path.parent / rel, dest)
        emit("拷贝清单=[%s]  # 只拷源码里真正被引用的文件（\\includegraphics / \\input）"
             % ", ".join(str(r).replace("\\", "/") for r in refs))
        if unresolved:
            emit("未能解析出的引用=%d  # 未找到或无法解析: %s；相关编译错误可能与此有关"
                 % (len(unresolved), ", ".join(sorted(set(unresolved)))))
        exe = shutil.which("pdflatex")
        emit("pdflatex=%s" % (exe if exe else "(未找到)"))
        rc, logs, err = run_pdflatex(work_tex, tmpdir)
        if err:
            emit("错误=%s" % err)
            b_fail.append("B.未找到pdflatex")
            emit("rc=NA")
            emit("页数=NA")
        else:
            emit("rc=%d" % rc)
            log_text = logs[-1] if logs else ""
            hard, real, first_ctx, unicode_cps = parse_log(log_text)
            emit("硬错误条数=%d" % len(real))
            emit("日志^!行总数=%d" % len(hard))
            if rc != 0:
                b_fail.append("B.rc=%d" % rc)
            if real:
                b_fail.append("B.硬错误")
                for h in first_ctx:
                    emit("首条错误=%s" % h.strip())

            produced = tmpdir / (jobname + ".pdf")
            if produced.is_file():
                # 拷贝到稳定位置，供 Read 直接看
                if args.pdf:
                    dest = Path(args.pdf).resolve()
                else:
                    dest = src_path.with_name(src_path.stem + "-check.pdf")
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(produced, dest)
                doc = fitz.open(str(produced))
                pages = doc.page_count
                emit("页数=%d" % pages)
                emit("PDF=%s" % dest)
                a_res = check_header_pdf(doc[0])   # <<< A 的判据：PDF 第 1 页文字
                if pages > 1:
                    b_fail.append("B.页数=%d(>1)" % pages)
                    stats = [page_body_stats(p) for p in doc]
                    good = [s for s in stats if s]
                    if good:
                        col_top = min(s["y0"] for s in good)
                        col_bot = max(s["y1"] for s in good)
                        col_h = col_bot - col_top
                        first, last = good[0], good[-1]
                        fill = (last["h"] / col_h) if col_h > 0 else 0.0
                        c1n, c2n = first["nchar"], last["nchar"]
                        emit("栏顶_pt=%.1f" % col_top)
                        emit("栏底_pt=%.1f" % col_bot)
                        emit("栏高_pt=%.1f" % col_h)
                        emit("末页bbox高_pt=%.1f" % last["h"])
                        emit("末页填充率=%.3f" % fill)
                        emit("首页字符数=%d" % c1n)
                        emit("末页字符数=%d" % c2n)
                        if fill > 0:
                            cap = c2n / fill
                            need = (c1n + c2n) - cap
                            emit("每栏容量字符=%.0f  # = 末页字符数 %.0f / 填充率 %.3f"
                                 % (cap, c2n, fill))
                            emit("要砍字数估算=%.0f  # 估算(非精确) = ceil((首页%d + 末页%d)"
                                 " - 容量%.0f)；LaTeX 重排不会完美回填"
                                 % (max(0.0, need), c1n, c2n, cap))
                            emit("要砍字数硬下界=%d  # 硬下界 = 末页字符数"
                                 "（把溢出的那一部分整体删掉，至少得砍这么多）" % c2n)
                        else:
                            emit("每栏容量字符=NA")
                            emit("要砍字数估算=NA")
                            emit("要砍字数硬下界=NA")
                else:
                    emit("末页填充率=NA  # 页数=1，不适用")
                doc.close()

                # Unicode 报错与 C7 清单对齐
                if unicode_cps:
                    c7map = {}
                    for (ln, col, ch, ctx) in nonascii:
                        c7map.setdefault("U+%04X" % ord(ch), []).append((ln, col, ctx))
                    emit("编译日志Unicode报错码点=%s" % ",".join(unicode_cps))
                    for cp in unicode_cps:
                        if cp in c7map:
                            ln, col, ctx = c7map[cp][0]
                            emit("对齐: %s -> 必须改写 行=%d 列=%d 上下文=%r"
                                 % (cp, ln, col, ctx))
                        else:
                            emit("对齐: %s -> C7 清单里没有（可能来自模板/宏包）" % cp)
                    accepted = [cp for cp in c7map if cp not in unicode_cps]
                    if accepted:
                        emit("C7清单中被字体接受=%s  # 这些不必改" % ",".join(accepted))
                elif nonascii:
                    emit("编译日志Unicode报错码点=(无)")
                    emit("C7清单中被字体接受=%s  # 全数被接受"
                         % ",".join(dict.fromkeys("U+%04X" % ord(c)
                                                  for (_l, _c, c, _x) in nonascii)))
            else:
                emit("页数=NA  # 未产出 PDF")
                b_fail.append("B.无PDF产出")
    finally:
        if args.keep_temp:
            emit("临时目录=%s  # --keep-temp 保留" % tmpdir)
        else:
            shutil.rmtree(tmpdir, ignore_errors=True)
    if a_res is None:      # 没编出 PDF -> A 无从核验，不能算 PASS
        a_res = [(n, False, "无法从产物核验：未产出 PDF", HINT_LACK_PDF)
                 for n in A_ITEM_NAMES]

    # ======================= A（判据 = PDF 第 1 页文字）=======================
    print("== A 页眉三栏（判据 = 编译出的 PDF 第 1 页文字，不读源码）==")
    a_fail = []
    for name, ok, msg, hint in a_res:
        print("%s: %s  # %s" % (name, "PASS" if ok else "FAIL", msg))
        if not ok:
            a_fail.append(name)
            if hint:
                print("怎么改=%s" % hint)
    print("边界=%s" % BOUNDARY_HEADER)
    print("[辅助诊断-源码] 不参与判定: %s"
          % " | ".join("%s=%s(%s)" % (n, v[0], v[1]) for n, v in
                       (("Problem", a_src_vals["problem"]),
                        ("Team", a_src_vals["team"]),
                        ("年份", a_src_vals["year"]))))
    print("  年份诊断说明=这里的年份取自**源码**（文件里第一处 `MCM/ICM` 前 80 字符窗口），"
          "可能取到注释里的旧年份（官方资产 `mcm-2027-summary.tex` 的注释里就有 `2026`）"
          "⇒ **这不是判定依据**；判定依据是上方 A4（从编译出的 PDF 第 1 页读出的年份）。")

    # ======================= B 输出 =======================
    print()
    print("== B 编译 ==")
    for _ln in b_lines:
        print(_ln)

    # ======================= C 输出 =======================
    print()
    print("== C 机械扫描（扫描面：\\begin{document} 之后 .. \\end{document} 之前）==")
    print("C1_行内未转义百分号=%d  # 误写的 %% 会静默吞掉该行剩余部分"
          "（判据：%% 紧贴前一字符且其后仍有内容）" % c_counts["c1"])
    print("C1b_行尾注释_不计违规=%d  # 合法行尾注释/行首注释行，见 docstring C1 判据"
          % c_counts["c1_exempt"])
    print("C2_裸下划线上标=%d  # 数学模式外的 _ 与 ^" % c_counts["c2"])
    print("C3_markdown残留=%d  # 行首# / ** / 管道表" % c_counts["c3"])
    print("C4_HTML残留=%d  # <sub> 这类标签" % c_counts["c4"])
    print("C5_裸竖线=%d  # pdflatex 里渲染成破折号" % c_counts["c5"])
    print("C6_裸波浪号=%d  # `~` 作「约」讲时会凭空消失并改语义"
          "（判据：`~` 前是空白或行首 且 `~` 后是数字）" % c_counts["c6"])
    print("C6b_不断行空格_不计违规=%d  # Fig.~1 / 12~pt / Dr.~Smith 这类合法用法"
          % c_counts["c6_exempt"])
    print("C7_非ASCII字符=%d  # 只列不判违规" % len(nonascii))
    for key, title in (("c1", "C1"), ("c2", "C2"), ("c3", "C3"),
                       ("c4", "C4"), ("c5", "C5"), ("c6", "C6")):
        for d in c_details[key]:
            print("  %s %s" % (title, d))
    if c_counts["c1"] > 0:
        print("提示=判据：未转义 + % 紧贴前一字符 + 其后仍有非空白内容 ⇒ 计 C1；"
              "% 前置空白的行尾注释、% 后无内容的行尾注释都不计。"
              "已知误报：把「吃行尾空格」的注释接着内容写（紧贴且其后还有内容，"
              "形如 \\foo%comment）会被计入——那是 LaTeX 的惯用法；"
              "遇到就把它移到独立行、或写成带前置空格的 `  % ...`。")
    for (ln, col, ch, ctx) in nonascii:
        print("  C7 行=%d 列=%d 码点=U+%04X %r 上下文=%r"
              % (ln, col, ord(ch), ch, ctx))

    # ======================= D =======================
    print()
    print("== 结论 ==")
    fails = list(a_fail) + list(b_fail)
    for key, title in (("c1", "C1"), ("c2", "C2"), ("c3", "C3"),
                       ("c4", "C4"), ("c5", "C5"), ("c6", "C6")):
        if c_counts[key] != 0:
            fails.append("%s=%d" % (title, c_counts[key]))
    if fails:
        print("RESULT: FAIL")
        print("失败项=%s" % ",".join(fails))
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
