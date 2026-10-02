#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-table` 的**机械层判据**（设计 `2026-10-02-m3-table-design.md` §5.1 的 8 条；计划 Task 2）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/table/check-table-style.py [--tex PATH] [--png OUT] [--skeleton PATH]

**被判对象**：一份**表格片段** `.tex`（就是本 skill 的产物形态 —— 可粘的
`\\begin{table}…\\end{table}`，其前可有来源回显注释）。默认 = `tests/skills/table/fixtures/good-basic.tex`。

退出码 **0 / 1**（无 2）；末行**恒**为 `RESULT: …`；每条判词**一行**，形态 `PASS|FAIL  <id>  <读数>`。
**fail-closed = 判红 + exit 1**（输入读不出 / 解析不出承重结构 / 编译跑不动 ⇒ 红，**不许静默绿**）。

## 八条判据（对应设计 §5.1 的表；ID 供 Task 3 的契约与变异驱动器逐条点名）

| ID | 判什么 | 口径 |
| :--- | :--- | :--- |
| `C1` | **编得过** | 片段塞进自带模板编一遍，`pdflatex` rc=0（**硬门**）。pdflatex 不在 PATH ⇒ 红。 |
| `C2` | **三线结构** | `\\toprule`/`\\midrule`/`\\bottomrule` **各 ≥1** 且 `tabular` 列说明里**无 `|`**。不要求"恰三条"（多级表头要 `\\cmidrule`）。 |
| `C3` | **表题在 `tabular` 之上**（默认；可覆盖） | 见下「覆盖口径」。 |
| `C4` | **编译后实测表宽 ≤ 版心宽** | **分母** = 编译 log 里 `MCMLAYOUT textwidth=<pt>`（LaTeX 自算的确定数，**不是**从渲染图推的）；**分子** = 同次编译里 `\\settowidth` 量出的 `tabular` 宽度（`MCMLAYOUT tablewidth=<pt>`；**只量到 `\\end{tabular}` 为止**，含包住它的**花括号组**，如 `{\\small …}` —— 见 `table_body_for_width` 里 RED 暴露的 `\\par` 假红）。两行任一缺失 ⇒ 红。 |
| `C5` | **列数一致、无空格子** | 每行（`\\multicolumn{n}` 按 `n` 展宽）格数 == 列数；且无空白格。空列（整列皆空）是空格子的特例。**例外**：两级表头的**首格留空 + 紧随一个跨列分组头**（`\\multicolumn{n≥2}`）算结构性占位，不算空格子（见 `placeholder_holes`；RED `R1`/`R3` 即此形态）。 |
| `C6` | **同列精度一致** | 同一列数值格的小数位数集合大小 ≤ 1（`\\pm` 取左值；非数值格跳过）。 |
| `C7` | **缺失值形态一致** | 见下「缺失值口径」。 |
| `C8` | **来源回显覆盖每一格** | `% mcm-table-src: r<行>c<列> <- …`（格式钉死在 `table-style.md` §3.2）；`{1..行}×{1..列}` 每一格都要在某行注释**左端**出现。缺格 ⇒ 红。 |

## ★ `C3` 的「覆盖口径」（设计件没钉死，本条由**本判据**定义并写进 Task 3 的契约）

默认 = `\\caption` 在 `\\begin{tabular}` **之前**。**声明覆盖**的写法 = 片段里出现一行注释

    % mcm-table-caption: below

即：**表题在下**时，只有**显式**声明了这行注释才判绿；没声明 ⇒ 判红。**不出现 `\\caption`
（无表题）⇒ 判红**（默认要求有表题且在上，且没有声明覆盖）。`\\caption` **多于一个** ⇒ 判红（位置歧义）。

## ★ `C7` 的「缺失值口径」（与 `D6` 一致，**R2：规范值现取、不手抄**）

- **规范 token 从 `table-style.md` 的 `D6` 行现取**（`read_missing_token()`）；取不到 ⇒ 红（fail-closed），
  **不是**在脚本里写死一个 `--` 再静默比 —— 写死一次，规范改了这条判据就**静默失效**。
- 一个格子算"缺失值"：其内容（剥掉最外层花括号后）∈ {空, `-`, `--`, `—`, `–`, `NA`, `N/A`, `nan`,
  `null`} （**判别用的这些"错形"不在规范里**，故就地列出；**不声称穷尽**）。
- **一致 = 每一格都写成该列该有的规范形**：`S` 列里必须**带花括号**写成 `{<token>}`
  （`siunitx` 的 `S` 列放非数值必须包花括号，否则编不过 —— `table-style.md` §3.3 的耦合点）；
  非 `S` 列必须写成**裸** `<token>`。任一处不是规范形 ⇒ 红。
  ★ 这条**在源码层面**判，不靠"编不过"：`S` 列裸 token 会连带 `C1` 红，但非 `S` 列写 `NA` 能编过、
  **只有 `C7` 抓得到**（变异 `MUT-C7a` 即证）。

## 覆盖范围（**不声称穷尽**）

判的是**一张片段表**的结构与几何；**判不了**：表讲没讲清 / 表注与表是否同指一事 / 列是否"缩过头"
看不清 / 列头单位对不对。**`\\resizebox` 压得过狠**在本器里**只**表现为"宽度没超版心"（绿），
"字小到读不下去"它判不出 ⇒ 必须**渲图看一眼**（`--png` 只是把这一步的输入给你，**看是你的事**）。

**不支持的写法**（**如实登记，不声称穷尽**）：`\\begin{tabular*}{宽度}{列说明}`（带宽度实参的
`tabular*`）**本器不支持** —— 正则只认 `\\begin{tabular}`，`tabular*` 会被判成"0 个 `tabular`"
⇒ `C2`–`C8` fail-closed 红。要支持需另做宽度实参的解析（本支未做）。`\\resizebox` 因自带模板
**没有载 `graphicx`** ⇒ 带它的片段在 `C1` 上**本来就编不过**（见 `table_body_for_width` 的边界）。
写法用 `\\toprule[粗细]`/`\\midrule[..]`/`\\bottomrule[..]`/`\\cmidrule[粗细]...` 的**可选线宽参数**：
自 2026-10-03 起**已支持**（`RULES_RE` 吞掉 `[..]`；**同一行内**宏名与 `[` 之间可夹**横空白**，
如 `\\midrule [0.8pt]`；正控制 fixture `good-rulethickness.tex`）。**未覆盖**：**换行后**再写 `[..]`
（本器只吞横空白、**不跨行**）等（**不声称穷尽**）。

## 环境

需 PATH 里有 `pdflatex`（本机 TeX Live 2026 实测在）。**仓库路径含非 ASCII**（`数学建模`）⇒
**编译一律在系统临时目录**（`tempfile.mkdtemp()`）里做，**绝不把仓内路径塞给 pdflatex**。
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]                 # tests/skills/table/x.py → 仓根
NORM = ROOT / ".claude/skills/mcm-table/references/table-style.md"  # 规范（token 现取的来源）
TEMPLATE = ROOT / ".claude/skills/mcm-table/assets/table-template.tex"
DEFAULT_TEX = ROOT / "tests/skills/table/fixtures/good-basic.tex"

# 缺失值的**错形**（用于识别"这是个缺失值"，不是规范值；见 docstring 的 C7 口径）
MISSING_VARIANTS = {"", "-", "--", "—", "–", "NA", "N/A", "nan", "NaN", "null"}
RULES_RE = re.compile(r"\\cmidrule[ \t]*(?:\[[^\]]*\])?(?:\s*\([^)]*\))?\s*(?:\{[^{}]*\})?"
                      r"|\\(?:top|mid|bottom)rule[ \t]*(?:\[[^\]]*\])?"
                      r"|\\(?:hline|addlinespace|specialrule)(?:\{[^{}]*\}){0,3}")


def _shown(p):
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


# --------------------------------------------------------------------- 小工具（配平花括号）
def _next_nonescaped(s, i):
    """`s[i] == '\\'` 时，跳过它后面的一个字符（处理 `\\{` / `\\}` 转义）。返回下一个扫描位。"""
    if s[i] == "\\" and i + 1 < len(s):
        return i + 2
    return i + 1


def _is_escaped(s, i):
    """`s[i]` 的**正前方**有奇数个连续反斜杠 ⇒ 它被转义（如 `\\{`），不算结构花括号。"""
    n, j = 0, i - 1
    while j >= 0 and s[j] == "\\":
        n += 1
        j -= 1
    return n % 2 == 1


def matching_brace(s, i):
    """`s[i] == '{'` ⇒ 返回与它配平的 `'}'` 的下标；不配平/不合法 ⇒ `None`。"""
    if i >= len(s) or s[i] != "{":
        return None
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j = _next_nonescaped(s, j)
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return None


def strip_outer_braces(s):
    """反复剥掉**完整包住整串**的最外层花括号。"""
    s = s.strip()
    while len(s) >= 2 and s[0] == "{" and s[-1] == "}" and matching_brace(s, 0) == len(s) - 1:
        s = s[1:-1].strip()
    return s


def strip_comments(s):
    """去掉 `%` 到行尾的注释（尊重 `\\%`）；**用于源码结构判定**（C8 另用原文）。"""
    out = []
    for line in s.splitlines():
        i = 0
        while i < len(line):
            if line[i] == "\\":
                i += 2
                continue
            if line[i] == "%":
                line = line[:i]
                break
            i += 1
        out.append(line)
    return "\n".join(out)


def split_top(s, ch):
    """在花括号深度 0 处按单字符 `ch` 切分。"""
    parts, buf, depth, i = [], [], 0, 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            buf.append(s[i:i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if c == ch and depth == 0:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts


def split_rows(body):
    """花括号深度 0 处的 `\\\\` 切分成行；吃掉行首可选的 `[..]`（行距参数）。"""
    rows, buf, depth, i = [], [], 0, 0
    while i < len(body):
        c = body[i]
        if c == "\\":
            if depth == 0 and body[i:i + 2] == "\\\\":
                rows.append("".join(buf))
                buf = []
                i += 2
                if i < len(body) and body[i] == "[":
                    k = body.find("]", i)
                    i = (k + 1) if k != -1 else i
                continue
            buf.append(body[i:i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        buf.append(c)
        i += 1
    rows.append("".join(buf))
    return [r for r in rows if r.strip()]


# --------------------------------------------------------------------- 解析 table / tabular
def find_tabular(src):
    """片段里**唯一**一个 `tabular`。返回 `((colspec, body, begin, end), n)`；不唯一 ⇒ `(None, n)`。

    ★ 只认 `\\begin{tabular}`（**无** `\\*?`）：`tabular*` 的宽度实参会被当列说明解析，
    故**不支持** `tabular*`（见 docstring「覆盖范围」）；`tabular*` 文件按 0 个 `tabular`
    fail-closed 红，不静默绿。
    """
    n = len(re.findall(r"\\begin\{tabular\}", src))
    if n != 1:
        return None, n
    m = re.search(r"\\begin\{tabular\}", src)
    j = m.end()
    while j < len(src) and src[j] in " \t\r\n":
        j += 1
    if j >= len(src) or src[j] != "{":
        return None, n
    end = matching_brace(src, j)
    if end is None:
        return None, n
    colspec = src[j + 1:end]
    e = re.search(r"\\end\{tabular\}", src[end:])
    if not e:
        return None, n
    body = src[end + 1:end + e.start()]
    return (colspec, body, m.start(), end + e.end()), n


CAPTION_LABEL_CENTER_RE = re.compile(r"\\caption\s*(?:\[[^\]]*\])?\s*\{|\\label\s*\{|\\centering\b")


def _enclosing_group_start(body, inner_start, inner_end):
    """`body[inner_start:inner_end]` 之外**最内层**仍把它整个包住的那个 `{` 的下标；没有 ⇒ `None`。

    用途：把 `{\\small …\\begin{tabular}… }` 这类**花括号组**包装连同被量的 `tabular` 一起留下
    （越靠后的候选 = 越内层）。★ 只认花括号组；`\\resizebox{..}{..}{…}` 这种**宏 + 实参**的包装
    不在此列 —— 边界与理由见 `table_body_for_width`。
    """
    best = None
    for i, ch in enumerate(body):
        if i >= inner_start:
            break
        if ch != "{" or _is_escaped(body, i):
            continue
        m = matching_brace(body, i)
        if m is not None and m >= inner_end:
            best = i
    return best


def table_body_for_width(src, env):
    """量宽用的"被排版体"：**只到 `\\end{tabular}` 为止**（含包住它的**花括号组**包装），剥掉其后的表注。

    ★ 为什么不能把整个 `table` 环境体塞进 `\\settowidth`（2026-10-02 三份 RED 暴露的假红）：
    `\\settowidth` 的实参是在一个 `\\hbox` 里排的，**一碰到 `\\par` 就报**
    `Paragraph ended before \\@settodim was complete` ⇒ 整个 harness 编译 rc≠0 ⇒ `C1`
    **假红**（片段本身能编过）、`C4` 的分子量成 `0.0pt`（假绿）。RED 写手在 `\\end{tabular}`
    **之后**、浮动体里写的表注（`\\par\\smallskip` + `minipage`）正好踩中；`R1`/`R2` 都栽在这。
    故这里只取"决定表宽"的那一段：`tabular` 加包住它的**花括号组**（如 `{\\small …}`）。

    ★ 已知边界（**如实说，不假装覆盖**）：`\\resizebox{\\linewidth}{!}{…}` 这类**宏 + 若干实参
    + `{内容}`** 的包装，这里**只留 `{…}`、丢掉宏名与实参** ⇒ 量到的是**没缩放的自然宽**。
    之所以不特判：harness 的 preamble 取自 `table-template.tex`，它**没有载 `graphicx`** ⇒
    带 `\\resizebox` 的片段在 `C1` 上**本来就编不过**（2026-10-02 实测 `rc=1`，`\\resizebox` 未定义），
    `C4` 对它无从谈起。本器**不声称**覆盖 `\\resizebox` 形态。
    """
    m = re.search(r"\\begin\{table\*?\}(?:\[[^\]]*\])?", src)
    body = src
    if m:
        e = re.search(r"\\end\{table\*?\}", src[m.end():])
        if e:
            body = src[m.end():m.end() + e.start()]
    elif env is not None:
        body = src[env[2]:env[3]]
    while True:
        m2 = CAPTION_LABEL_CENTER_RE.search(body)
        if not m2:
            break
        if m2.group(0).endswith("{"):
            k = matching_brace(body, m2.end() - 1)
            body = (body[:m2.start()] + body[k + 1:]) if k is not None else body[:m2.start()] + body[m2.end():]
        else:
            body = body[:m2.start()] + body[m2.end():]
    # 裁到 `\end{tabular}`：其后的表注会把 `\par` 带进 `\settowidth`（见上）
    mb = re.search(r"\\begin\{tabular\}", body)
    if mb:
        me = re.search(r"\\end\{tabular\}", body[mb.end():])
        if me:
            b0, e_end = mb.start(), mb.end() + me.end()
            g = _enclosing_group_start(body, b0, e_end)
            ge = matching_brace(body, g) if g is not None else None
            body = body[g:ge + 1] if (g is not None and ge is not None) else body[b0:e_end]
    # `\settowidth` 的实参里不许出现空行（`\par`）——剥 caption/centering 会留下空行，折叠掉
    return "\n".join(l for l in body.splitlines() if l.strip())


def parse_colspec(spec):
    """列说明 → 列类型列表（`*{n}{…}` 展开；`p{…}`/`S[..]`/`@{…}`/`>{…}` 处理）。不认识 ⇒ 抛 `ValueError`。"""
    cols, i = [], 0
    while i < len(spec):
        c = spec[i]
        if c in " \t\r\n|":
            i += 1
            continue
        if c in "@><":
            j = i + 1
            while j < len(spec) and spec[j] in " \t\r\n":
                j += 1
            k = matching_brace(spec, j)
            if k is None:
                raise ValueError(f"列说明里的 `{c}` 后没有配平的花括号：…{spec[i:i+20]!r}")
            i = k + 1
            continue
        if c == "*":
            j = spec.find("{", i)
            k = matching_brace(spec, j) if j != -1 else None
            if k is None:
                raise ValueError("`*{n}{…}` 形式不完整")
            try:
                rep = int(spec[j + 1:k].strip())
            except ValueError:
                raise ValueError(f"`*{{n}}` 的 n 不是整数：{spec[j+1:k]!r}")
            j2 = spec.find("{", k)
            k2 = matching_brace(spec, j2) if j2 != -1 else None
            if k2 is None:
                raise ValueError("`*{n}{…}` 的第二个花括号不完整")
            cols.extend(parse_colspec(spec[j2 + 1:k2]) * rep)
            i = k2 + 1
            continue
        if c in "lcrX":
            cols.append(c)
            i += 1
            continue
        if c in "pmb":
            j = spec.find("{", i)
            k = matching_brace(spec, j) if j != -1 else None
            if k is None:
                raise ValueError(f"`{c}{{宽度}}` 形式不完整")
            cols.append(c)
            i = k + 1
            continue
        if c == "S":
            cols.append("S")
            i += 1
            while i < len(spec) and spec[i] in " \t\r\n":
                i += 1
            if i < len(spec) and spec[i] == "[":
                k = spec.find("]", i)
                if k == -1:
                    raise ValueError("`S[...]` 的 `]` 缺失")
                i = k + 1
            continue
        raise ValueError(f"不认识的列说明字符：{c!r}（列说明 {spec!r}）")
    return cols


def count_row_cols(row):
    """一行的**展宽后**列数（`\\multicolumn{n}` 按 `n` 计；`\\multirow` 按 1 计）。

    返回 `(total, cells, starts)`：`starts[i]` = `cells[i]` 的**起始列号**（0 基）。
    `\\multicolumn{n}` 为**计数**展宽成 n 列，但其 `cells` 项仍只算**一格** ⇒ 下游必须按
    `starts` 定位列，**不可**拿 `enumerate(cells)` 的下标当列号：多级/跨列表头会把其后的
    数值格整体错位（真第 3 列的数值记到第 2 列），从而把**合规表**在 `C6`/`C7` 上**假红**。
    """
    cells = split_top(row, "&")
    total = 0
    starts = []
    for cell in cells:
        m = re.match(r"\s*\\multicolumn\s*\{(\d+)\}", cell)
        starts.append(total)
        total += int(m.group(1)) if m else 1
    return total, cells, starts


def placeholder_holes(row):
    """这一行里**属于结构性占位**的空格下标集合（0 基，按 `count_row_cols` 的 `cells` 序）。

    形态 = **两级表头的首格留空**：首格为空、紧跟着一个跨列分组头，例如
    `& \\multicolumn{3}{c}{Share of land area} & \\multicolumn{2}{c}{Nearest neighbour} \\\\`
    （首格由 `\\cmidrule` 分组留下、本就无值 ⇒ **不是**"该有值却空着"）。
    判据：`cells[0]` 为空 **且** `cells[1]` 是 `\\multicolumn{n}` 且 `n ≥ 2`。

    **不声称穷尽**其它合法占位写法（非首格的空洞、跨列之后留空格、`\\cmidrule` 之外的分组约定
    等本器不认）；反过来，**只在首格、且紧邻跨列分组**这一形态放行，故"该有值却空着"的普通
    空格子（含表头行里的首格，只要其后不是跨列分组）照旧判红。RED 里 `R1`/`R3` 正是这一形态。
    """
    _cnt, cells, _starts = count_row_cols(row)
    if not cells or cells[0].strip() != "":
        return set()
    if len(cells) >= 2:
        m = re.match(r"\s*\\multicolumn\s*\{(\d+)\}", cells[1])
        if m and int(m.group(1)) >= 2:
            return {0}
    return set()


# --------------------------------------------------------------------- 规范 token 现取
def read_missing_token(norm_path):
    """从 `table-style.md` 的 `D6` 行**现取**缺失值 token（反引号里的那个）。取不到 ⇒ `None`。"""
    try:
        txt = norm_path.read_bytes().decode("utf-8")
    except OSError:
        return None
    for line in txt.splitlines():
        if "D6" in line:
            spans = [s for s in re.findall(r"`([^`]+)`", line) if s != "D6"]
            if len(spans) == 1:
                return spans[0]
    return None


# --------------------------------------------------------------------- 编译（在临时目录里）
def build_harness(template_path, fragment, body_for_width):
    """用自带模板的 **preamble**（含它的 `\\typeout{MCMLAYOUT textwidth=…}`）+ 片段，拼一个可编译文档。

    preamble **从模板文件现读**（分母那一行由此而来，不在本脚本里重抄）；片段**原样**放进正文
    （`C1` 判的就是它）；另用 `\\settowidth` 量出 `tabular` 自然宽（`C4` 的分子）。
    """
    tmpl = template_path.read_bytes().decode("utf-8")
    k = tmpl.find(r"\begin{document}")
    if k == -1:
        raise ValueError(f"模板里找不到 `\\begin{{document}}`：{template_path}")
    preamble = tmpl[:k]
    if "\\newlength{\\mcmtabw}" not in preamble:
        preamble += "\\newlength{\\mcmtabw}\n"
    doc = (preamble
           + "\\begin{document}\n"
           + "\\settowidth{\\mcmtabw}{" + body_for_width + "}\n"
           + "\\typeout{MCMLAYOUT tablewidth=\\the\\mcmtabw}\n"
           + fragment + "\n\\end{document}\n")
    return doc


def run_pdflatex(tex_text):
    """把 harness 写进系统临时目录编一遍。返回 `(rc, log_text, err)`；起不动 pdflatex ⇒ `rc=None`。"""
    if shutil.which("pdflatex") is None:
        return None, "", "PATH 里没有 pdflatex"
    d = tempfile.mkdtemp(prefix="mcmtable-")
    try:
        p = pathlib.Path(d) / "t.tex"
        p.write_bytes(tex_text.encode("utf-8"))                 # 一律 write_bytes（全 LF）
        try:
            pr = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-file-line-error", "t.tex"],
                                cwd=d, capture_output=True, text=True)
        except OSError as e:
            return None, "", f"{type(e).__name__}: {e}"
        logp = pathlib.Path(d) / "t.log"
        log = logp.read_text(encoding="utf-8", errors="replace") if logp.is_file() else ""
        return pr.returncode, log, ""                           # 第三个返回值 = **出错说明**（rc≠None 时为空）
                                                                # ★ 批量清 M-5：原返回 t.pdf 的路径，但它是临时目录、下面 finally 已删 ⇒ 无人能用
    finally:
        shutil.rmtree(d, ignore_errors=True)                    # PDF 留到最后一步单独渲（见 --png 说明）


def compile_and_measure(template_path, fragment, body_for_width):
    """编译 + 从 log 取 `textwidth`/`tablewidth`。返回 `(rc, err, textwidth_pt, tablewidth_pt, log)`。"""
    try:
        harness = build_harness(template_path, fragment, body_for_width)
    except (OSError, ValueError) as e:
        return None, f"{type(e).__name__}: {e}", None, None, ""
    rc, log, err = run_pdflatex(harness)
    tw = re.search(r"MCMLAYOUT\s+textwidth=([\d.]+)pt", log)
    bw = re.search(r"MCMLAYOUT\s+tablewidth=([\d.]+)pt", log)
    return rc, err, (float(tw.group(1)) if tw else None), (float(bw.group(1)) if bw else None), log


# --------------------------------------------------------------------- 判据主体
def judge(tex_path, missing_token):
    """对一份片段跑完 8 条。返回 `rows` —— 每项是 `(id, ok, detail, [extra_lines])`。

    ★ 批量清 M-5：原返回 `(rows, extra)`，而 `extra` **恒为 `[]`**（第二返回值是死代码）⇒ 收成单返回值。
    """
    rows = []
    try:
        raw = tex_path.read_bytes().decode("utf-8")
    except OSError as e:
        for cid in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8"):
            rows.append((cid, False, f"读不出输入（fail-closed）：{type(e).__name__}: {e}", []))
        return rows

    src = strip_comments(raw)                                   # 结构判定用无注释文本
    env, n_tab = find_tabular(src)
    colspec = body = None
    coltypes = []
    colspec_err = None                                          # 解析异常 = `env=None` 的**等价 fail-closed 态**
    if env is not None:
        colspec, body = env[0], env[1]
        try:
            coltypes = parse_colspec(colspec)
        except ValueError as e:
            coltypes = []
            colspec_err = e                                      # 只**记录**，判词**仅**由 C2 块出（避免 C2 既 FAIL 又 PASS）
    rows_text = []
    if body is not None:
        rows_text = split_rows(re.sub(RULES_RE, "", body))

    # ---- 供 C4 用的"被排版体"（剥掉 caption/label/centering；保留 resizebox/small 等改宽包装）
    body_for_width = table_body_for_width(src, env)
    rc, err, textwidth_pt, tablewidth_pt, _log = compile_and_measure(TEMPLATE, raw, body_for_width)

    # ---------------------------------------------------------------- C1 编得过
    if rc is None:
        rows.append(("C1", False, f"编译跑不动（fail-closed）：{err}", []))
    elif rc == 0:
        rows.append(("C1", True, "pdflatex rc=0（片段在自带模板里编过）", []))
    else:
        # ★ 批量清 M-4：`-file-line-error` 的真实错误行形如 `t.tex:<行>: <消息>`（**不以 `!` 开头**），
        #   只挑 `!` 行常只抓到 `! Emergency stop.`（误导）⇒ 优先取 `-file-line-error` 行，退而求其次才取 `!` 行。
        errlines = [l for l in _log.splitlines() if re.search(r"\.tex:\d+:", l)]
        first = (errlines[0] if errlines
                 else next((l for l in _log.splitlines() if l.startswith("!")), "（log 里无错误行）"))
        rows.append(("C1", False, f"pdflatex rc={rc} ⇒ 编不过", [f"      首个错误：{first[:160]}"]))

    # ---------------------------------------------------------------- C2 三线结构
    if env is None:
        if n_tab == 0:
            rows.append(("C2", False, "片段里找不到 `tabular`（0 个；`tabular*` 不支持，见「覆盖范围」）"
                                     "或解析不出（fail-closed）", []))
        else:
            rows.append(("C2", False, f"片段里 `tabular` 不唯一（{n_tab} 个）或解析不出（fail-closed）", []))
    elif colspec_err is not None:
        rows.append(("C2", False, f"列说明解析失败（fail-closed）：{colspec_err}", []))
    else:
        miss = [c for c in ("toprule", "midrule", "bottomrule") if f"\\{c}" not in src]
        bars = "|" in colspec
        if miss or bars:
            why = []
            if miss:
                why.append("缺 " + "/".join(f"\\{c}" for c in miss))
            if bars:
                why.append("列说明里有竖线 `|`")
            rows.append(("C2", False, "三线结构不合规：" + "；".join(why),
                         [f"      列说明 = {colspec!r}"]))
        else:
            rows.append(("C2", True, "toprule/midrule/bottomrule 齐 · 列说明无 `|`", []))

    # ---------------------------------------------------------------- C3 表题位置
    caps = [m.start() for m in re.finditer(r"\\caption\b", src)]
    tab_at = env[2] if env else None
    override = re.search(r"%\s*mcm-table-caption:\s*below", raw) is not None
    if env is None:
        rows.append(("C3", False, "没有可定位的 `tabular` ⇒ 表题位置无从判（fail-closed）", []))
    elif len(caps) == 0:
        rows.append(("C3", False, "无 `\\caption`（默认要求表题在 `tabular` 之上，且未见覆盖声明）", []))
    elif len(caps) > 1:
        rows.append(("C3", False, f"`\\caption` 出现 {len(caps)} 次 ⇒ 位置歧义", []))
    elif caps[0] < tab_at:
        rows.append(("C3", True, "`\\caption` 在 `\\begin{tabular}` 之前（默认位）", []))
    elif override:
        rows.append(("C3", True, "表题在下，但声明了覆盖 `% mcm-table-caption: below`", []))
    else:
        rows.append(("C3", False, "表题在 `tabular` 之下且**未**声明覆盖（`% mcm-table-caption: below`）", []))

    # ---------------------------------------------------------------- C4 表宽 ≤ 版心宽
    if rc is None or textwidth_pt is None or tablewidth_pt is None:
        why = ("编译跑不动" if rc is None else
               "log 里缺 " + "/".join(n for n, v in (("textwidth", textwidth_pt), ("tablewidth", tablewidth_pt)) if v is None))
        rows.append(("C4", False, f"量不出宽（{why}）⇒ 无从判（fail-closed）", []))
    else:
        ratio = tablewidth_pt / textwidth_pt
        detail = (f"表宽 {tablewidth_pt:.5f}pt（{tablewidth_pt/72.27:.3f}in） · "
                  f"版心 {textwidth_pt:.5f}pt（{textwidth_pt/72.27:.3f}in） · 占 {ratio*100:.1f}%")
        if tablewidth_pt <= textwidth_pt:
            rows.append(("C4", True, "表宽 ≤ 版心：" + detail, []))
        else:
            rows.append(("C4", False, "表宽**超**版心：" + detail, []))

    # ---------------------------------------------------------------- C5 列数一致、无空格子
    if env is None or not coltypes or not rows_text:
        rows.append(("C5", False, "列说明或行解析不出 ⇒ 无从判（fail-closed）", []))
    else:
        n = len(coltypes)
        bad = []
        n_holes = 0
        for ri, row in enumerate(rows_text, 1):
            cnt, cells, _starts = count_row_cols(row)
            holes = placeholder_holes(row)
            n_holes += len(holes)
            if cnt != n:
                bad.append(f"第 {ri} 行列数 {cnt} != {n}")
            for ci, cell in enumerate(cells):
                if cell.strip() == "" and ci not in holes:
                    bad.append(f"第 {ri} 行第 {ci+1} 格为空")
        if bad:
            rows.append(("C5", False, f"列数/空格子不合规（{len(bad)} 处）：" + "；".join(bad[:3])
                         + ("…" if len(bad) > 3 else ""), []))
        else:
            extra = f"（{n_holes} 处表头占位格除外）" if n_holes else ""
            rows.append(("C5", True, f"{len(rows_text)} 行 × {n} 列 · 列数一致 · 无空格子{extra}", []))

    # ---------------------------------------------------------------- C6 同列精度一致
    if env is None or not coltypes:
        rows.append(("C6", False, "列说明解析不出 ⇒ 无从判（fail-closed）", []))
    else:
        n = len(coltypes)
        dpsets = [set() for _ in range(n)]
        for row in rows_text:
            _cnt, cells, starts = count_row_cols(row)
            for ci, cell in enumerate(cells):
                c0 = starts[ci]                                 # 按**起始列**定位（`\multicolumn` 塌缩后仍正确）
                if c0 >= n:
                    continue
                d = _decimals(cell)
                if d is not None:
                    dpsets[c0].add(d)
        bad = [f"第 {ci+1} 列小数位 {sorted(s)}" for ci, s in enumerate(dpsets) if len(s) > 1]
        if bad:
            rows.append(("C6", False, "同列精度不一致：" + "；".join(bad), []))
        else:
            shown = [f"c{ci+1}:{'∅' if not s else sorted(s)[0]}" for ci, s in enumerate(dpsets)]
            rows.append(("C6", True, "各列小数位集合大小 ≤1（" + " · ".join(shown) + "）", []))

    # ---------------------------------------------------------------- C7 缺失值形态一致
    if env is None or not coltypes:
        rows.append(("C7", False, "列说明解析不出 ⇒ 无从判（fail-closed）", []))
    elif missing_token is None:
        rows.append(("C7", False, "规范里取不到缺失值 token（`D6`）⇒ 无从判（fail-closed）", []))
    else:
        n = len(coltypes)
        bad = []
        for ri, row in enumerate(rows_text, 1):
            _cnt, cells, starts = count_row_cols(row)
            holes = placeholder_holes(row)                      # 首格占位不算缺失值（F1）
            for ci, cell in enumerate(cells):
                if ci in holes:
                    continue
                c0 = starts[ci]                                 # 按**起始列**定位（同 C6）
                if c0 >= n:
                    continue
                raw_cell = cell.strip()
                inner = strip_outer_braces(raw_cell)
                if inner not in MISSING_VARIANTS and inner != missing_token:
                    continue                                   # 不是缺失值格
                want_braced = (coltypes[c0] == "S")
                okform = (raw_cell == "{" + missing_token + "}") if want_braced else (raw_cell == missing_token)
                if not okform:
                    want = ("{" + missing_token + "}") if want_braced else missing_token
                    bad.append(f"r{ri}c{c0+1}={raw_cell!r}（该列应写 {want!r}）")
        if bad:
            rows.append(("C7", False, f"缺失值形态不一致（{len(bad)} 处）：" + "；".join(bad[:3])
                         + ("…" if len(bad) > 3 else ""), []))
        else:
            rows.append(("C7", True, f"缺失值一律为规范形（`S` 列 `{{{missing_token}}}` · 非 `S` 列 `{missing_token}`）", []))

    # ---------------------------------------------------------------- C8 来源回显
    covered = set()
    for m in re.finditer(r"^[^\n]*?%\s*mcm-table-src:\s*r(\d+)c(\d+)\s*<-", raw, re.M):
        covered.add((int(m.group(1)), int(m.group(2))))
    if env is None or not coltypes or not rows_text:
        rows.append(("C8", False, "行/列解析不出 ⇒ 无从判覆盖（fail-closed）", []))
    elif not covered:
        rows.append(("C8", False, "一条 `% mcm-table-src: r<行>c<列> <-` 都没有", []))
    else:
        nrow, ncol = len(rows_text), len(coltypes)
        need = {(r, c) for r in range(1, nrow + 1) for c in range(1, ncol + 1)}
        missing = sorted(need - covered)
        if missing:
            shown = "、".join(f"r{r}c{c}" for r, c in missing[:6])
            rows.append(("C8", False, f"来源回显漏格（{len(missing)}/{nrow*ncol}）：{shown}"
                         + ("…" if len(missing) > 6 else ""), []))
        else:
            rows.append(("C8", True, f"来源回显覆盖 {nrow}×{ncol}={nrow*ncol} 格全齐（注释 {len(covered)} 条）", []))

    return rows


def _decimals(cell):
    """格子的小数位数；非数值 ⇒ `None`。`\\pm` 取左值；支持 `\\num{…}`。"""
    c = strip_outer_braces(cell.strip())
    if "\\pm" in c:
        c = c.split("\\pm")[0]
    c = c.strip()
    m = re.fullmatch(r"\\num\s*\{(.*)\}", c, re.S)
    if m:
        c = strip_outer_braces(m.group(1).strip())
    m = re.fullmatch(r"[+-]?\d+(?:\.(\d+))?", c)
    if not m:
        return None
    return len(m.group(1)) if m.group(1) else 0


# --------------------------------------------------------------------- main
def render_png(tex_path, out_path):
    """把编译出的**第一页**渲成 PNG（`--png`，供"看一眼"；非判据）。返回一行说明。

    ★ 批量清 M-5：原签名多一个 `missing_token` 形参，函数体里**从未用到** ⇒ 删掉这个死参数。
    """
    try:
        import fitz
    except Exception as e:                                      # noqa: BLE001
        return f"PNG: 未生成（PyMuPDF 不在：{type(e).__name__}: {e}）"
    try:
        raw = tex_path.read_bytes().decode("utf-8")
        src = strip_comments(raw)
        env, _ = find_tabular(src)
        body_for_width = table_body_for_width(src, env)
        harness = build_harness(TEMPLATE, raw, body_for_width)
        d = tempfile.mkdtemp(prefix="mcmtable-png-")
        p = pathlib.Path(d) / "t.tex"
        p.write_bytes(harness.encode("utf-8"))
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "t.tex"], cwd=d,
                       capture_output=True, text=True)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with fitz.open(str(pathlib.Path(d) / "t.pdf")) as doc:
            pix = doc.load_page(0).get_pixmap(dpi=150)
            pix.save(str(out_path))
        shutil.rmtree(d, ignore_errors=True)
        return f"PNG: {_shown(out_path)}（第 1 页 · 150dpi · {out_path.stat().st_size} 字节）"
    except Exception as e:                                      # noqa: BLE001
        return f"PNG: 未生成（{type(e).__name__}: {str(e).splitlines()[0][:120]}）"


def main():
    ap = argparse.ArgumentParser(description="mcm-table：表格机械层判据（8 条，fail-closed）")
    ap.add_argument("--tex", default=None, help="被判的表格片段 .tex（默认 = fixtures/good-basic.tex）")
    ap.add_argument("--png", default=None, help="把编译结果第 1 页渲成 PNG（非判据，供人看）")
    ap.add_argument("--skeleton", default=None, help="论文骨架 .tex；给了就**额外**编一遍（信息行 SKEL，非判据）")
    a = ap.parse_args()

    tex_path = pathlib.Path(a.tex) if a.tex else DEFAULT_TEX
    if not tex_path.is_absolute():
        tex_path = (ROOT / tex_path)
    missing_token = read_missing_token(NORM)

    print("mcm-table 机械层判据（设计 §5.1 的 8 条 · fail-closed）")
    print(f"被判片段 = {_shown(tex_path)}")
    print(f"模板（preamble + 版心 `\\typeout` 的来源） = {_shown(TEMPLATE)}")
    print(f"规范（缺失值 token 现取处） = {_shown(NORM)} · D6 token = {missing_token!r}")
    print("-" * 78)

    rows = judge(tex_path, missing_token)
    for rid, ok, detail, extra in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {rid}  {detail}")
        for line in extra:
            print(line)

    if a.skeleton:
        print("-" * 78)
        print(compile_in_skeleton(tex_path, pathlib.Path(a.skeleton)))

    if a.png:
        print("-" * 78)
        print(render_png(tex_path, pathlib.Path(a.png)))

    bad = [rid for rid, ok, _d, _e in rows if not ok]
    print("-" * 78)
    print(f"判据 {len(rows)} 条 · 红 {len(bad)} 条")
    print("RESULT: PASS" if not bad else f"RESULT: FAIL（{','.join(bad)}）")
    return 0 if not bad else 1


def compile_in_skeleton(tex_path, skeleton_path):
    """硬要求 5(b)：在**用户骨架的 preamble** 下再编一遍，报"缺哪个宏包 / 会不会爆版心"。

    ★ **信息行，不进 RESULT**：本支的 `mcm-latex-format` 骨架实测**缺全部表格宏包**
    （设计 §7.2）⇒ 这一步**本就该红**，不能拿它当判据。它答的是"嵌得进你的论文吗"。
    """
    try:
        sk = skeleton_path.read_bytes().decode("utf-8")
        frag = tex_path.read_bytes().decode("utf-8")
    except OSError as e:
        return f"SKEL: 读不出（{type(e).__name__}: {e}）"
    if "\\end{document}" not in sk:
        return "SKEL: 骨架里没有 `\\end{document}` ⇒ 不验（如实说）"
    body = ("\\typeout{MCMLAYOUT textwidth=\\the\\textwidth}\n"      # 借骨架自己的版心
            + "\\typeout{MCMLAYOUT skeleton=yes}\n"
            + frag + "\n")
    inj = sk.replace("\\end{document}", body + "\\end{document}")
    if shutil.which("pdflatex") is None:
        return "SKEL: PATH 里没有 pdflatex ⇒ 不验"
    d = tempfile.mkdtemp(prefix="mcmtable-skel-")
    try:
        p = pathlib.Path(d) / "s.tex"
        p.write_bytes(inj.encode("utf-8"))
        pr = subprocess.run(["pdflatex", "-interaction=nonstopmode", "s.tex"], cwd=d,
                            capture_output=True, text=True)
        lp = pathlib.Path(d) / "s.log"
        log = lp.read_text(encoding="utf-8", errors="replace") if lp.is_file() else ""
        undef = sorted(set(re.findall(r"Undefined control sequence[\s\S]{0,80}?\\([A-Za-z@]+)", log)))
        overfull = log.count("Overfull \\hbox")
        nerr = len(re.findall(r"^!", log, re.M))
        return (f"SKEL: 骨架 = {_shown(skeleton_path)} · rc={pr.returncode} · log 错误 {nerr} 条 · "
                f"Overfull \\hbox {overfull} 处 · 未定义控制序列 {undef or '无'}")
    finally:
        shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
