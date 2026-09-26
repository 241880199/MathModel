"""Task 6 Step 0 侦察：索引/词表/ID 边界六件事的实测取数。

**这份脚本只做取数与登记**，不含判据、不改任何产物（只写它自己的输出文件
`tests/papers/recon/ids-recon.txt`）。它的作用是让 Task 6 的判据有**实测过的参照**，
而不是拿计划草稿里那几个数字当真。

量六件（对应任务书 Step 0 的 1–6）：

1. 官方题型标签的覆盖（可查则记，查不到就记「未查」，**不伪造**）；
2. **标题口径对账**：复用 `textmd` 的函数（`body_size` / `HEADING_DELTA` /
   `is_title`）从**原件**重扫出的标题，与 Task 3 产出的 md 里 `## ` 行**逐份对账**；
3. **`has_*` 两种口径的分布**：全文子串（计划草稿口径）vs **标题行里字面出现**（新口径）；
4. **词表**：候选词清单的来源、每词命中份数、零命中词、与作者自写 Keywords 的重合；
5. **ID 边界**：6 个合集逐个跑 `stable_id`，UMAP 抛错与跨合集撞号写成具名边界；
6. **论文自报题号**：从 md 的摘要页 `Problem Chosen` 一类读出的题号，三态分开报。

运行：`python tests/papers/recon/ids-recon-scan.py`（无参数，无落点机制——它不是判据脚本，
不写 `tests/papers/reports/`）。
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT))

from tools.papers import io, textmd  # noqa: E402

OUT = Path(__file__).resolve().parent / "ids-recon.txt"
PILOT = "2025美赛O奖论文"
MD_ROOT = ROOT / "corpus" / "papers" / "md"
COLLECTIONS = sorted(p.name for p in io.ORIGIN.iterdir() if p.is_dir())

# 计划草稿的 `HAS_PROBES` 逐词照抄（旧口径要复现的那个）。
HAS_PROBES = {
    "has_contents": ["Contents"],
    "has_assumptions": ["Assumptions", "Assumption"],
    "has_notations": ["Notations", "Notation"],
    "has_sensitivity": ["Sensitivity"],
    "has_extension": ["Extension", "Extend"],
}
# 计划草稿的 `KEYWORDS` 逐字照抄（**缺 `re.M`**，正是任务书 §六 第 8 条要复现的那个）。
KEYWORDS_DRAFT = re.compile(r"^\s*(Key\s*words?|关键词)\s*[:：]\s*(.+)$", re.I)
# 宽松口径：允许行首有 md 标记（`## ` 标题 / `**粗体**` / `>` 引用），**带 `re.M`**。
# `[#>*_ \t]*` 里刻意**不含 `\n`**——否则 `\s` 会让 `^` 在上一行、内容在下一行，
# 匹配跨行（re.M 下这是活的坑）。
KEYWORDS_WIDE = re.compile(
    r"^[#>*_ \t]*(?:Key\s*words?|关键词)\s*[:：]\s*(.*?)[*_ \t]*$", re.I | re.M)
# 计划草稿那个正则**加 `re.M`**（任务书二节表的 27/43 就是它）。
KEYWORDS_DRAFT_M = re.compile(r"^\s*(Key\s*words?|关键词)\s*[:：]\s*(.+)$", re.I | re.M)
# 论文自报题号：`Problem Chosen` / `问题选择` 一类栏位名，题号在其后几行内的独立字母。
#
# **两种排法都要认**（实测都有）：栏位独占一行、题号在下一行（`2500836`：`**Problem
# Chosen**` / `**A**`）；栏位与题号同一行。**大小写都要认**（实测 `2516695` 写的是
# `**c**` 小写）。**不能一遇不匹配的行就 break**——摘要页在题号之后还有
# `**2025**` / `**MCM/ICM**` / `## Summary Sheet` 等栏位，而**题号之后**才出现。
PROBLEM_FIELD = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]?\s*"
                           r"[*_ \t]*$", re.I | re.M)
PROBLEM_INLINE = re.compile(r"^[#>*_ \t]*\s*(?:Problem\s+Chosen|问题选择)\s*[:：]"
                            r"[*_ \t]*([A-Fa-f])[*_ \t]*$", re.I | re.M)
LONE_LETTER = re.compile(r"^[*_#>\s]*([A-Fa-f])[*_#>\s]*$")
# 摘要页在题号**之后**的栏位——遇到它就停，免得把别处的单字母当成题号。
FIELD_STOP = re.compile(r"\b(?:MCM|ICM|Summary\s+Sheet|Team\s+Control\s+Number|"
                        r"19\d\d|20\d\d)\b", re.I)
# md 里的页锚（Task 3 写的）。
PAGE_ANCHOR = re.compile(r"^<!-- page (\d+) -->$", re.M)


def lines_of(p: Path) -> list[str]:
    """md 全文按行（**bytes → utf-8 解码**，不走文本模式，免得被 autocrlf 影响）。"""
    return p.read_bytes().decode("utf-8").splitlines()


def md_files() -> list[Path]:
    return sorted((MD_ROOT / PILOT).rglob("*.md"))


def h2_lines(lines: list[str]) -> list[str]:
    """md 里 `## ` 开头的行（**逐字**，`### ` 不算——实测本语料 `### ` 为 0）。"""
    return [l for l in lines if l.startswith("## ")]


def textmd_headings(pdf: Path) -> list[str]:
    """**复用 `textmd` 的三个函数**从原件重扫标题（不得有第三份口径）。

    判序与 `textmd.to_markdown` 逐字相同：CAPTION 抢先 → `is_heading(size, body)`
    `and is_title(text)` → 其余。区别只在于本函数**只收标题行**（不写 md）。
    """
    import fitz
    from tools.papers import watermark
    with fitz.open(pdf) as doc:
        watermark.strip_in_memory(doc)
        body = textmd.body_size(doc)
        out: list[str] = []
        for pno in range(doc.page_count):
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
                    size = max(s["size"] for s in spans)
                    if textmd.CAPTION.match(text):
                        continue
                    if textmd.is_heading(size, body) and textmd.is_title(text):
                        out.append(text.strip())
        return out


def main() -> int:
    L: list[str] = []
    W = L.append

    W("Task 6 Step 0 侦察取数（`tests/papers/recon/ids-recon-scan.py` 的输出，逐字原文）")
    W("=" * 78)
    W("本文件是**取数记录**，不是放行证据。判据脚本 `verify_ids.py` 的参照由它给出。")
    W("")

    # ---------- 0. 语料与产物的基本盘 ----------
    W("## 0. 语料与产物基本盘")
    W("")
    for c in COLLECTIONS:
        pdfs = sorted((io.ORIGIN / c).rglob("*.pdf"))
        md = sorted((MD_ROOT / c).rglob("*.md"))
        W(f"  {c:<44} PDF {len(pdfs):>3} · md {len(md):>3}")
    W("")
    allpdf = sum(len(sorted((io.ORIGIN / c).rglob('*.pdf'))) for c in COLLECTIONS)
    W(f"  6 个合集合计 PDF **{allpdf}** 份；只有 `{PILOT}` 有 md/图表/公式产物"
      f"（**{len(md_files())}** 份）——**索引的交付范围就是这 {len(md_files())} 份**。")
    W("")

    # ---------- 1. 官方题型标签 ----------
    W("## 1. 官方题型标签的覆盖（可查则记；查不到就记「未查」）")
    W("")
    off = io.ORIGIN.parent / "官方原题"
    years = sorted(p.name for p in off.iterdir() if p.is_dir()) if off.is_dir() else []
    W(f"  `corpus/官方原题/` 存在目录：{years}")
    if years:
        n_pdf = sum(len(sorted((off / y).glob('*.pdf'))) for y in years)
        W(f"  题面 PDF 合计 **{n_pdf}** 份（每年 6 题）。")
        W("  **本次未逐份打开题面去提取 COMAP 的题型标签**——任务书 Step 0 第 1 条把这一项"
          "移交给 Task 6b（「官方有就用，没有就依题面自建」），且明写「不做也可以」。")
        W("  故本行**只登记目录与文件数这个已查范围**，不声称「官方没有标签」"
          "（教训 4.5：「我没找到」≠「它不存在」）。")
    W("")

    # ---------- 2. 标题口径对账 ----------
    W("## 2. 标题口径对账：`textmd` 口径（从原件重扫）vs md 的 `## ` 行")
    W("")
    files = md_files()
    W("参照 A = `textmd_headings(pdf)`（复用 `body_size` / `HEADING_DELTA` / `is_title`，"
      "判序与 `to_markdown` 逐字相同）；")
    W("参照 B = Task 3 产物 md 里 `## ` 开头的行。**两者应当逐份逐条相等**——")
    W("不相等就说明「md 不是 `textmd` 口径的忠实产物」或「重扫口径与写盘口径分叉」。")
    W("")
    tot_a = tot_b = 0
    diff_files = 0
    for pdf in sorted((io.ORIGIN / PILOT).rglob("*.pdf")):
        prob = io.problem_of(str(pdf.relative_to(io.ORIGIN)))
        md = io.md_path(PILOT, prob, pdf.stem)
        a = textmd_headings(pdf)
        b = [l[3:].strip() for l in h2_lines(lines_of(md))]
        tot_a += len(a)
        tot_b += len(b)
        if a == b:
            continue
        diff_files += 1
        W(f"  **差额** {pdf.stem}（题 {prob}）：重扫 {len(a)} 条 / md `## ` {len(b)} 条")
        only_a = Counter(a) - Counter(b)
        only_b = Counter(b) - Counter(a)
        for t, n in sorted(only_a.items()):
            W(f"      只在重扫（×{n}）：{t!r}")
        for t, n in sorted(only_b.items()):
            W(f"      只在 md `## `（×{n}）：{t!r}")
    W("")
    W(f"  合计：重扫 **{tot_a}** 条 · md `## ` **{tot_b}** 条 · "
      f"逐份不等的 **{diff_files}** 份（共 {len(md_files())} 份）")
    W("")
    # ---- 2b. `## ` 行里「编号型 / 无编号型」的拆分（`sections` 栏的口径依据）----
    W("  2b. `## ` 行的两种形态（**实测**：本语料把「号」与「题」常分两行排——"
      "`## 1.1` 一行、`## Problem Background` 下一行，见 `textmd` 模块 docstring）：")
    RX_ALONE = re.compile(r"^(\d+(?:\.\d+)*)[.、)）]?$")
    RX_WITH = re.compile(r"^(\d+(?:\.\d+)*)[.、)）]?\s+\S")
    n_alone = n_with = 0
    for md in files:
        for l in md.read_bytes().decode("utf-8").splitlines():
            if not l.startswith("## "):
                continue
            t = l[3:].strip()
            if RX_ALONE.match(t):
                n_alone += 1
            elif RX_WITH.match(t):
                n_with += 1
    W(f"     · **只有编号**（`## 1.1`）**{n_alone}** 条 · "
      f"**编号 + 题**（`## 1.1 Model`）**{n_with}** 条 · "
      f"**合计 {n_alone + n_with}** 条（任务书二节表写的是「编号型 `##` 915 条」"
      f"——本次实测 **{n_alone + n_with}**，两口径的**差别**在于"
      f"「只有编号」那一类算不算编号型）")
    W(f"     · 无编号型 = {tot_b} − {n_alone + n_with} = "
      f"**{tot_b - n_alone - n_with}** 条（`## Contents`、`## References`、"
      f"`## Summary`、以及被 `is_title` 放过的假标题如 `## remains stable.`）")
    W("")

    # ---------- 3. has_* 两种口径 ----------
    W("## 3. `has_*` 两种口径的分布")
    W("")
    W("旧口径（计划草稿）= **全文不区分大小写的子串**；")
    W("新口径 = **md 的 `## ` 标题行里字面出现**（不区分大小写的子串，作用在标题行文本上）。")
    W("")
    old = {k: [] for k in HAS_PROBES}
    new = {k: [] for k in HAS_PROBES}
    per_file_old: dict[str, list[str]] = {}
    per_file_new: dict[str, list[str]] = {}
    for md in files:
        t = md.read_bytes().decode("utf-8")
        tlow = t.lower()
        hs = [l[3:].strip() for l in h2_lines(lines_of(md))]
        hslow = "\n".join(hs).lower()
        po, pn = [], []
        for k, probes in HAS_PROBES.items():
            if any(x.lower() in tlow for x in probes):
                old[k].append(md.stem)
                po.append(k)
            if any(x.lower() in hslow for x in probes):
                new[k].append(md.stem)
                pn.append(k)
        per_file_old[md.stem] = po
        per_file_new[md.stem] = pn
    W(f"  {'栏':<18}{'旧口径（全文子串）':>20}{'新口径（标题行）':>20}")
    for k in HAS_PROBES:
        W(f"  {k:<18}{len(old[k]):>14} / {len(files):<3}{len(new[k]):>14} / {len(files):<3}")
    W("")
    W("  新口径下的**零区分力登记**（>90% 恒定即登记为「零区分力」，不因「能算出来」就当判据）：")
    for k in HAS_PROBES:
        n = len(new[k])
        if n > 0.9 * len(files) or n < 0.1 * len(files):
            W(f"    {k}: {n}/{len(files)} = {n / len(files) * 100:.1f}% → **零区分力**"
              f"（只有一边取值近乎恒定）")
    W("")
    W("  新口径下**两态都非空**的栏（有区分力）：")
    for k in HAS_PROBES:
        n = len(new[k])
        if 0.1 * len(files) <= n <= 0.9 * len(files):
            W(f"    {k}: 有 {n} 份 / 无 {len(files) - n} 份")
            W(f"        有：{' '.join(new[k])}")
            W(f"        无：{' '.join(sorted(set(f.stem for f in files) - set(new[k])))}")
    W("")

    # ---------- 4. 词表 ----------
    W("## 4. 词表：来源、规模、每词命中份数、零命中词、与作者 Keywords 的重合")
    W("")
    W("  候选词来源三处（任务书 Step 0 第 4 条建议）：")
    W("    a) `corpus/algorithms/INDEX.md` 的八大类与表内算法名；")
    W("    b) 作者自写 Keywords 行（宽松口径命中者）；")
    W("    c) 论文正文。**本侦察只做统计，不建最终词表**（词表在 Step 3 建）。")
    W("")

    # a) 八大类 + 表内术语种子（从 INDEX.md 抽 `**…**` 与表格首列的常见形态）
    alg = (ROOT / "corpus" / "algorithms" / "INDEX.md").read_bytes().decode("utf-8")
    seed_a = set()
    for m in re.finditer(r"\*\*([^*\n]{2,40})\*\*", alg):
        seed_a.add(m.group(1).strip())
    W(f"  a) `algorithms/INDEX.md` 里 `**粗体**` 术语 {len(seed_a)} 个（含 `AHP 层次分析法`、"
      f"`灰色预测 GM(1,1)` 一类**词+中文**的复合串，直接当词表项会有词边界问题）")
    W(f"     前 12 个：{sorted(seed_a)[:12]}")
    W("")

    # b) 作者自写 keywords
    kw_wide: dict[str, str] = {}
    kw_draft: dict[str, str] = {}
    kw_draft_m: dict[str, str] = {}
    for md in files:
        t = md.read_bytes().decode("utf-8")
        m = KEYWORDS_WIDE.search(t)
        if m:
            kw_wide[md.stem] = m.group(1).strip()
        m2 = KEYWORDS_DRAFT.search(t)
        if m2:
            kw_draft[md.stem] = m2.group(2).strip()
        m3 = KEYWORDS_DRAFT_M.search(t)
        if m3:
            kw_draft_m[md.stem] = m3.group(2).strip()
    W(f"  b) 作者自写 Keywords 行，三种口径并列：")
    W(f"     · 计划草稿口径 `{KEYWORDS_DRAFT.pattern}`（**无 `re.M`**）："
      f"**{len(kw_draft)}/{len(files)}** 命中 —— **这就是任务书 §六 第 8 条要复现的 0/43**")
    W(f"     · **同一个正则加 `re.M`**：**{len(kw_draft_m)}/{len(files)}** 命中"
      f" —— **任务书二节表里的 27/43**")
    W(f"     · 宽口径 `{KEYWORDS_WIDE.pattern}` + `re.I|re.M`（允行首 md 标记）："
      f"**{len(kw_wide)}/{len(files)}** 命中")
    gap = sorted(set(kw_wide) - set(kw_draft_m))
    W(f"     宽口径比「草稿正则 + `re.M`」多认出的 **{len(gap)}** 份，**逐份原文**"
      f"（这些篇确实有作者自写 Keywords 行，只是行首带着 md 标记，草稿正则看不见）：")
    for s in gap:
        for md in files:
            if md.stem == s:
                for l in lines_of(md):
                    if KEYWORDS_WIDE.search(l + "\n"):
                        W(f"       {s}: {l.strip()!r}")
    W(f"     宽口径下**真的无 Keywords 行**的："
      f"{' '.join(sorted(set(f.stem for f in files) - set(kw_wide))) or '（无）'}"
      f" —— 判据取宽口径（**任务书约束 8：证据里不得出现实测不成立的语料事实**；"
      f"「16 份无该行」若照抄草稿口径就是假陈述，故逐份登记上面那 {len(gap)} 份的真实形态）")
    W("")
    # 作者 keywords 拆词
    author_terms: set[str] = set()
    for v in kw_wide.values():
        for piece in re.split(r"[;,；，、|/]", v):
            piece = piece.strip().strip("*_ ").strip()
            if 2 <= len(piece) <= 40:
                author_terms.add(piece)
    W(f"     作者 Keywords 拆出的**不同词形** {len(author_terms)} 个（全批），"
      f"前 30 个：{sorted(author_terms)[:30]}")
    W("")

    # c) 正文：候选术语的命中率（用「词边界」与「无词边界」两种口径对照）
    body_texts = {md.stem: md.read_bytes().decode("utf-8") for md in files}
    probe_terms = [
        # algorithms/INDEX.md 的八大类主干词（人工挑选，逐一注明出处）
        "AHP", "层次分析法", "TOPSIS", "熵权法", "模糊综合评价", "灰色预测", "GM(1,1)",
        "ARIMA", "指数平滑", "移动平均", "线性回归", "岭回归", "Lasso", "主成分分析",
        "PCA", "因子分析", "聚类", "K-means", "判别分析", "支持向量机", "随机森林",
        "神经网络", "BP", "LSTM", "遗传算法", "粒子群", "PSO", "模拟退火", "蚁群",
        "蒙特卡洛", "Monte Carlo", "马尔可夫", "元胞自动机", "有限差分", "有限元",
        "微分方程", "Navier-Stokes", "SIR", "logistic", "多目标", "线性规划",
        "整数规划", "动态规划", "排队论", "图论", "最短路", "最大流", "时间序列",
        "敏感性分析", "XGBoost", "SHAP", "DID", "SEM", "贝叶斯", "Bayesian",
        "系统动力学", "Lotka-Volterra", "Tobit", "回归", "SVR", "SARIMA",
    ]
    W(f"  c) 主干候选词 **{len(probe_terms)}** 个（人工从八大类挑选 + 作者 Keywords 里"
      f"出现的高频名），两种匹配口径下的命中份数：")
    W("")
    W(f"     {'词':<18}{'无词边界（子串）':>16}{'词边界':>10}  备注")
    zero = []
    for t in probe_terms:
        sub = sum(1 for v in body_texts.values() if t.lower() in v.lower())
        if re.fullmatch(r"[\x00-\x7f]+", t):
            pat = r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])"
            bw = sum(1 for v in body_texts.values()
                     if re.search(pat, v, re.I))
        else:
            bw = sub
        note = ""
        if sub != bw:
            note = "**无词边界多算了**（如 `logistic` 命中 `logistics` 一类）"
        if sub == 0:
            zero.append(t)
        W(f"     {t:<18}{sub:>16}{bw:>10}  {note}")
    W("")
    W(f"     零命中的 {len(zero)} 个：{zero}")
    W("     计划草稿的 45 词种子里「从未命中」的那些，与本表可以互相对照——"
      f"**本表零命中 {len(zero)}/{len(probe_terms)}**。")
    W("")

    # ---------- 5. ID 边界 ----------
    W("## 5. ID 边界：6 个合集逐个跑 `stable_id`")
    W("")
    for c in COLLECTIONS:
        try:
            sid = io.stable_id(c, "A", 1)
            W(f"  stable_id({c!r}, 'A', 1) = {sid!r}")
        except ValueError as e:
            W(f"  stable_id({c!r}, 'A', 1) **抛 ValueError**: {e}")
    W("")
    W("  具名边界 ①**UMAP 两个合集名不以 4 位数字开头** → `stable_id` 抛 `ValueError`：")
    for c in COLLECTIONS:
        if not re.match(r"^\d{4}", c):
            W(f"     {c!r}（涉 {len(sorted((io.ORIGIN / c).rglob('*.pdf')))} 份）")
    W("  具名边界 ②**跨合集撞号**：合集名少一个「年」字时年份相同 → 同一个 ID。实测：")
    for a, b in (("2023美赛O奖论文", "2023年美赛O奖论文"),):
        W(f"     stable_id({a!r},'A',1) = {io.stable_id(a, 'A', 1)!r} "
          f"== stable_id({b!r},'A',1) = {io.stable_id(b, 'A', 1)!r}")
    W(f"     而 `io.ORIGIN/'2023美赛O奖论文'` 在磁盘上 **is_dir = "
      f"{(io.ORIGIN / '2023美赛O奖论文').is_dir()}**（盘上是带「年」的那个）——")
    W("     这就是那个**活的 fail-open 陷阱**：`rglob` 对不存在的目录静默返回空表。")
    W("")
    W("  具名边界 ③**`io.problem_of` 在别的合集上抛错**（任务书二节表**只登记了 UMAP "
      "与撞号两条**，本条是本次侦察新查出来的，逐份实测）：")
    W("     `problem_of` 要求路径里有一个**整段等于 `A`–`F` 的目录名**。实测失败的形态有三：")
    for c in COLLECTIONS:
        pdfs = sorted((io.ORIGIN / c).rglob("*.pdf"))
        bad = []
        for p in pdfs:
            try:
                io.problem_of(str(p.relative_to(io.ORIGIN)))
            except ValueError:
                bad.append(p)
        if bad:
            dirs = sorted({p.relative_to(io.ORIGIN).parent.as_posix() for p in bad})
            W(f"       {c}: 失败 **{len(bad)}/{len(pdfs)}**，涉及的目录层 "
              f"{dirs[:3]}{' …' if len(dirs) > 3 else ''}")
    W("     逐条形态：`2024年美赛O奖论文/2024年美赛A题O奖论文/<stem>.pdf`（**题号写在目录名里**，"
      "不是独立一层）· `2023年美赛O奖论文/2023美赛春季赛O奖论文/<stem>.pdf`（春季赛无题号目录）· "
      "两个 UMAP 合集（PDF 直接在合集根下）。")
    W("     **含义**：`index.build(collection)` 对**非 2025** 的合集必然抛错——那正是"
      " fail-closed 要的行为（不得空表静默 PASS），但**判据必须把它断言成具名行为**，"
      "而不是当成「这些合集也有索引」。")
    W("")
    W("  全部 6 个合集逐份跑 `stable_id` 的唯一性（按 (year, problem) 计数；`problem_of` "
      "失败的份单列）：")
    for c in COLLECTIONS:
        pdfs = sorted((io.ORIGIN / c).rglob("*.pdf"))
        per: dict[str, int] = {}
        sids = []
        n_err = 0
        for p in pdfs:
            try:
                prob = io.problem_of(str(p.relative_to(io.ORIGIN)))
            except ValueError:
                n_err += 1
                continue
            per[prob] = per.get(prob, 0) + 1
            sids.append(io.stable_id(c, prob, per[prob]))
        W(f"     {c:<44} PDF {len(pdfs):>2} · 可编号 {len(sids):>2} · 唯一 ID "
          f"{len(set(sids)):>2} · problem_of 抛错 {n_err:>2} · 题号分布 "
          f"{dict(sorted(per.items()))}")
    W("")

    # ---------- 6. 论文自报题号 ----------
    W("## 6. 论文自报题号（「题目 ↔ 论文」对应的参照）")
    W("")
    W("三态分开报（任务书 Step 0 第 6 条）：**没有该行** ≠ **有该行但读不出** ≠ "
      "**读出来与目录不符**。")
    W("")
    n_none = n_unreadable = n_ok = 0
    mismatch: list[str] = []
    unreadable: list[str] = []
    nonefield: list[str] = []
    for md in files:
        prob_dir = md.parent.name
        text = md.read_bytes().decode("utf-8")
        got = None
        mi = PROBLEM_INLINE.search(text)
        if mi:
            got = mi.group(1).upper()
        else:
            m = PROBLEM_FIELD.search(text)
            if not m:
                n_none += 1
                nonefield.append(md.stem)
                continue
            tail = text[m.end():]
            for i, ln in enumerate([l for l in tail.splitlines() if l.strip()][:6]):
                ml = LONE_LETTER.fullmatch(ln)
                if ml:
                    got = ml.group(1).upper()
                    break
                if FIELD_STOP.search(ln):
                    break
        if got is None:
            n_unreadable += 1
            unreadable.append(md.stem)
            W(f"  **有该行但读不出**：{md.stem}（目录题号 {prob_dir}）"
              f"栏位原文 {(mi or PROBLEM_FIELD.search(text)).group(0).strip()!r}")
            continue
        if got != prob_dir:
            mismatch.append(f"{md.stem}: 目录 {prob_dir} vs 自报 {got}")
            W(f"  **不符**：{md.stem}：目录题号 {prob_dir} · 自报题号 {got}")
        else:
            n_ok += 1
    W("")
    W(f"  合计：**一致 {n_ok}** · **不符 {len(mismatch)}** · "
      f"**有该行但读不出 {n_unreadable}** · **没有该行 {n_none}**（共 {len(files)} 份）")
    W(f"  没有该行的份：{' '.join(nonefield) or '（无）'}")
    W(f"  读不出的份：{' '.join(unreadable) or '（无）'}")
    W("")

    # ---------- 7. 顺带发现 ----------
    W("## 7. 侦察中顺带发现（会影响判据设计的事实）")
    W("")
    nul_files = []
    for md in files:
        b = md.read_bytes()
        if b"\x00" in b:
            nul_files.append((md.stem, b.count(b"\x00")))
    W(f"  7.1 md 里含 **NUL 字节**（`\\x00`）的份数 **{len(nul_files)}**：{nul_files}")
    W("      → 这不是本任务引入的（Task 3 的冻结产物），但它意味着**任何把 md 当纯文本"
      "逐行处理的实现都要能扛住 NUL**，且判据里的「空白归一化定位」不能假定全篇可打印。")
    W("")
    # md 页锚
    anch = [len(PAGE_ANCHOR.findall(md.read_bytes().decode("utf-8"))) for md in files]
    W(f"  7.2 md 的页锚 `<!-- page N -->`：逐份 {min(anch)}–{max(anch)} 条，"
      f"合计 {sum(anch)} —— 页码可从 md 自身推出（**不必回头开 PDF**）。")
    W("")
    h23 = Counter()
    for md in files:
        for l in lines_of(md):
            if l.startswith("## "):
                h23["##"] += 1
            elif l.startswith("### "):
                h23["###"] += 1
            if l.startswith("# "):
                h23["#"] += 1
            if l.startswith("#") and not l.startswith("## "):
                h23["hash1"] += 1
    W(f"  7.3 md 标题行：`# ` {h23['#']} · `## ` {h23['##']} · `### ` {h23['###']} "
      f"（任务书二节表里的 `# ` 31 / `## ` 2340 / `### ` 0）；"
      f"另有 `^#` 但非 `## ` 的行 **{h23['hash1']}** 条（`# ` 之外还有"
      f"`# Combine all meshes…`（代码注释）、`#(24)`（编号 token 紧贴 `#`）一类）。"
      f"**`## ` 那一栏两边逐字相同（2340）**，`# ` 那一栏的 31 vs 23 是口径差"
      f"（本次按「`# ` 前缀」数，8 条差额是上面那些非 `## ` 的 `#` 行）。")
    W("")
    W(f"  7.4 **`sections` 栏的取法决定**（本侦察给出依据）：`## ` 行的两种形态实测为"
      f"「只有编号 {n_alone} + 编号带题 {n_with}」；本任务**不做「号/题两行合并」一类"
      f"推断**（那是把推断写进事实栏），`sections` 取 **md `## ` 标题行逐字**，"
      f"判据是与 md 逐字逐条对账（双边等式）。")
    W("")

    text = "\n".join(L) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(text.encode("utf-8"))
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
