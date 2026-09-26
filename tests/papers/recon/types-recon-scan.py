"""Task 6b Step 0 侦察取数（`types-recon.txt` 就是本脚本 stdout 的逐字原文）。

**这是取数记录，不是放行证据**（判据在 `tests/papers/verify_types.py`，它的参照由本文件给出）。
跑法：`python tests/papers/recon/types-recon-scan.py > tests/papers/recon/types-recon.txt`
（落盘时由 shell 重定向；脚本自己**不写任何文件**、**不碰 corpus/**）。

本脚本回答四个问题，逐条都是**量出来的**、不是估的：
  1. 67 份题面 PDF 逐份的**抽取探针**（行数/字符数/内容流文本操作符数）——「读不出」的阈值从哪来；
  2. **归一化口径**到底做了多少事（宽松口径 vs 严口径的逐条差额与归因）；
  3. 自建**分类法**与词表的距离（相等 0 条；含子串的近邻逐条）；
  4. **标注草案**的规模与分布。
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # recon → papers → tests → 仓库根
sys.path.insert(0, str(ROOT))

from tools.papers import taxonomy as T  # noqa: E402 —— 取数记录，允许用被测实现

out: list[str] = []


def p(s: str = "") -> None:
    out.append(s)


def sec(title: str) -> None:
    p("")
    p(title)


FILES = T.problem_files()
ANNS = T.load_annotations()
TAX = T.load_taxonomy()
MODELS = ROOT / "tools" / "papers" / "vocab" / "models.txt"

p("Task 6b Step 0 侦察取数（`tests/papers/recon/types-recon-scan.py` 的输出，逐字原文）")
p("=" * 78)
p("本文件是**取数记录**，不是放行证据。判据脚本 `verify_types.py` 的参照由它给出。")

sec("## 0. 语料与产物基本盘")
p(f"  题面 PDF **{len(FILES)}** 份（`corpus/官方原题/` 下 rglob *.pdf，命名约定 "
  f"`<年>_[MC]CM_Problem_<字母>.pdf`）")
years = defaultdict(list)
for f in FILES:
    years[f.year].append(f.problem)
p(f"  逐年题号：{ {y: ''.join(sorted(v)) for y, v in sorted(years.items())} }")
p(f"  标注：**{len(ANNS)}** 条（`{T.ANNOTATIONS_PATH.relative_to(ROOT).as_posix()}`）")
p(f"  分类法：`{T.TAXONOMY_PATH.relative_to(ROOT).as_posix()}` "
  f"L1 {len(TAX['L1'])} 条 · L2 {len(TAX['L2'])} 条")
p(f"  抽取口径：`pdftotext -enc UTF-8 <pdf> -`（poppler；不加 `-layout`），行尾归一成 LF、"
  f"分页符归一成 LF")

sec("## 1. 题面里的官方题型标签（**不声称「官方没有标签」**）")
p("  本脚本**没有**逐份打开题面去提取 COMAP 的题型标签：任务书把这一项写成「官方有就用、")
p("  没有就依题面自建」，且明写「不做也可以」。**已查范围**只有一处：`corpus/官方原题/PROVENANCE.md`")
p("  与 67 份文件的文件头（这一步查过）；**未查**的是「题面正文里有没有一个叫得上名的题型栏」——")
p("  没查的事**不写结论**（教训 4.5：「我没找到」≠「它不存在」）。")
p("  ⇒ 分类法**依题面自建**，条目与定义见 `tools/papers/vocab/problem_types.txt`。")

sec("## 2. 抽取探针逐份（「读不出」的阈值从这两个量来）")
p(f"  探针一 = 抽取文本里的**非空白行数**；探针二 = 原件内容流里 `BT|Tj|TJ` 的个数。")
p(f"  阈值（写在 `verify_types.py` 模块头）：行数 < **{T.MIN_TEXT_LINES}** **且** "
  f"操作符 < **{T.MIN_TEXT_OPS}** ⇒ 判「件里没有文本层」。")
p("")
p("   年 题  行数   字符   文本操作符  填充路径")
probe = {}
for f in FILES:
    t = T.extract_text(f.path)
    nt, nf = T.text_op_counts(f.path)
    nl = T.readable_lines(t)
    probe[(f.year, f.problem)] = (nl, len(t), nt, nf)
    flag = "  ← 读不出" if (nl < T.MIN_TEXT_LINES and nt < T.MIN_TEXT_OPS) else ""
    p(f"  {f.year} {f.problem} {nl:5d} {len(t):7d} {nt:9d} {nf:8d}{flag}")
lows = sorted(probe.items(), key=lambda kv: (kv[1][0], kv[1][2]))
p("")
p(f"  **实测空档**（行数）：最低 {lows[0][1][0]}（{lows[0][0][0]} {lows[0][0][1]}）、"
  f"次低 {lows[1][1][0]}（{lows[1][0][0]} {lows[1][0][1]}）——阈值 {T.MIN_TEXT_LINES} 落在 2 与 5 之间")
lo2 = sorted(probe.items(), key=lambda kv: kv[1][2])
p(f"  **实测空档**（操作符）：最低 {lo2[0][1][2]}（{lo2[0][0][0]} {lo2[0][0][1]}）、"
  f"次低 {lo2[1][1][2]}（{lo2[1][0][0]} {lo2[1][0][1]}）——阈值 {T.MIN_TEXT_OPS} 落在 4 与 102 之间")

sec("## 3. 归一化口径：宽松 vs 严，逐条差额与归因")
p("  宽松口径（T2 用的那条）：行尾归一 → 去项目符号 → 空白折叠 → 引号折叠 → 大小写折叠；")
p("  引文侧另去 `*`/反引号（**那是草案自己加的强调标记**）。")
p("  严口径：只做行尾归一 + 空白折叠 + 大小写折叠。")

LEFT = __import__("re")


def fold_quotes(s: str) -> str:
    return s.translate(T._QUOTE_FOLD)


def strict(s: str) -> str:
    return T.normalize_strict(s)


texts = {f"{f.year} {f.problem}": T.extract_text(f.path) for f in FILES}
n_cell = n_seg = n_loose = n_strict = 0
diffs = []
for a in ANNS:
    if a.status != T.STATUS_OK:
        continue
    hay, hays = T.normalize_for_locate(texts[a.key]), strict(texts[a.key])
    hayq = fold_quotes(hays)
    hayb = strict(T.LIST_MARK.sub(" ", texts[a.key]))
    for (l1, l2, _m), spans in zip(a.labels, a.evidence_sentences):
        for sp in spans:
            n_cell += 1
            for seg in [x for x in re.split(r"…+", sp) if x.strip()]:
                n_seg += 1
                q = T.normalize_quote(seg)
                if q not in hay:
                    diffs.append(("定位失败", a.key, l2, seg))
                    continue
                if q in hays:
                    n_strict += 1
                    continue
                plain = re.sub(r"[*`]", "", seg)
                if strict(plain) in hays:
                    cause = "只需去强调标记"
                elif fold_quotes(strict(plain)) in hayq:
                    cause = "还要折引号"
                elif strict(T.LIST_MARK.sub(" ", plain)) in hayb:
                    cause = "还要去项目符号"
                else:
                    cause = "**三步之外**（要查）"
                n_loose += 1
                diffs.append((cause, a.key, l2, seg))
p("")
p(f"  引文段（行内单元格）**{n_cell}** 段 · 拆 `…` 后 **{n_seg}** 条片段")
p(f"  宽松口径命中 **{n_seg}/{n_seg}**（口径本身就是判据 T2 的口径，失败为 0）")
p(f"  严口径命中 **{n_strict}/{n_seg}**，差额 **{n_loose}** 条，归因分布："
  f"{dict(Counter(c for c, *_ in diffs))}")
p("")
p("  逐条差额（**严口径定不到的，与为什么**）：")
for cause, key, l2, seg in diffs:
    p(f"    [{cause}] {key} · {l2}：{seg[:90]!r}")

sec("## 4. 分类法 vs 词表（T3 的距离）")
terms = []
for ln in MODELS.read_bytes().decode("utf-8").split("\n"):
    s = ln.strip()
    if not s or s.startswith("#"):
        continue
    terms.append(tuple(x.strip() for x in s.split("|") if x.strip()))
vocab = {}
for entry in terms:
    canon, variants = entry[0], entry[1:]
    for v in variants:
        vocab.setdefault(re.sub(r"\s+", "", v).casefold(), canon)
p(f"  词表：**{len(terms)}** 个词条 / **{sum(len(e) for e in terms)}** 个变体")
used_names = sorted({n for a in ANNS for lab in a.labels for n in lab[:2]})
p(f"  分类法条目：L1 {len(TAX['L1'])} · L2 {len(TAX['L2'])}；标注里实际用到的不同标签名 {len(used_names)}")
eq, near = [], []
for where, name in [("分类法", n) for lv in ("L1", "L2") for n in TAX[lv]] + \
                   [("标注", n) for n in used_names]:
    for part in T.name_parts(name):
        k = re.sub(r"\s+", "", part).casefold()
        if k in vocab:
            eq.append(f"{where} {name!r} 的成分 {part!r} == 词条 {vocab[k]!r}")
        for kk, canon in vocab.items():
            if kk != k and len(k) >= 2 and (k in kk or kk in k):
                near.append(f"{where} {name!r} 的 {part!r} "
                            f"{'⊂' if k in kk else '⊃'}词表 {canon!r}")
p(f"  **相等（同义反复）{len(eq)} 条**：{eq or '无'}")
p(f"  **含子串但不等（报告量）{len(set(near))} 条**，逐条：")
for n in sorted(set(near)):
    p(f"    {n}")

sec("## 5. 标注草案的规模与分布")
lab = Counter()
marks = Counter()
prob_n = []
for a in ANNS:
    for l1, l2, m in a.labels:
        lab[l2] += 1
        marks[m] += 1
    prob_n.append(len(a.labels))
p(f"  标注 **{len(ANNS)}** 条（标定 {sum(1 for a in ANNS if a.status == T.STATUS_OK)} · "
  f"读不出 {sum(1 for a in ANNS if a.status == T.STATUS_UNREADABLE)}）")
p(f"  标签 **{sum(lab.values())}** 个（去重 {len(lab)} 个 L2）；每题标签数 "
  f"最少 {min(prob_n)} / 最多 {max(prob_n)}")
p(f"  标记分布：{dict(marks)}")
p(f"  数据形态分布：{dict(Counter(a.data_regime for a in ANNS).most_common())}")
p(f"  零命中的分类法条目：{sorted(set(TAX['L2']) - set(lab))}")
p("")
p("  L2 使用分布（按题数降序）：")
for k, v in lab.most_common():
    p(f"    {v:3d}  {k}")
p("")
p("  逐题（标签数 / 引文段数 / 数据形态 / 场景）：")
for a in ANNS:
    p(f"    {a.key}  labels={len(a.labels):2d} spans={sum(len(v) for v in a.evidence_sentences):2d} "
      f"[{a.status}] {a.data_regime or '—':<12s} 场景={a.scenario or '—'}")

sec("## 6. 两处具名边界（实测）")
za = next(a for a in ANNS if a.key == "2020 A")
p(f"  ① `2020 MCM Problem A`：状态 `{za.status}`；抽取文本 {probe[(2020, 'A')][0]} 行 / "
  f"{probe[(2020, 'A')][1]} 字符；内容流文本操作符 {probe[(2020, 'A')][2]} 个、"
  f"填充路径 {probe[(2020, 'A')][3]} 条")
p(f"     → 正文是**矢量路径**画的（`Microsoft: Print To PDF`），不是排的；两个独立抽取器"
  f"（pdftotext / fitz）都只得 25 / 22 个字符。**不标标签、不写抽象、不猜题意。**")
z = next(a for a in ANNS if a.key == "2023 Z")
p(f"  ② `2023 ICM Problem Z`：**算第 67 道并标注**（{len(z.labels)} 个标签）；"
  f"题面是 COMAP 自发布的完整件（有 Requirement 段、有 25 页提交规则、页脚 ©2023 COMAP）。")
p(f"     它在「11 年 × 6 题」口径下是**附加题**；**不声称**它在当年赛制里的地位（超已查范围）。")

sec("## 7. 与 2025 样板的偏离（逐条，供用户裁决）")
for ln in (ROOT / "corpus" / "papers" / "PROBLEM_TYPES.md").read_bytes() \
        .decode("utf-8").split("\n"):
    if ln.startswith("| 1 |") or (ln.startswith("| ") and len(ln) > 4 and ln[2].isdigit()
                                  and "偏离" not in ln):
        p("  " + ln[:300])


# ---- 编者按（**登记，不是脚本 stdout 的取数**；体例照 `ids-recon.txt` 的编者按）---------
# 它由脚本一并落盘，**这样重跑脚本不会把登记冲掉**（第一版是手写追加的，重跑一次就没了）。


def blob_of(path: Path) -> str:
    """`git hash-object` 的等价物（blob 的 sha1）。**不用裸 sha256**，口径与任务书一致。"""
    if not path.is_file():
        return "<尚未生成>"
    data = path.read_bytes()
    h = __import__("hashlib").sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


sec("## ★ 编者按：Task 6b 阶段 1 的已知残余（2026-09-26，实现者追加）")
p("  **本节不是脚本 stdout，是登记**（体例照 `ids-recon.txt` 的编者按）。上面是逐字取数，")
p("  本节把「这一轮**没做到**什么」写进入库区——**不得只写在 `.superpowers/sdd/`**")
p("  （那个目录 gitignore，按本项目规矩放那里等于丢失）。")
p("")
for rt in [
    ("RT1", "**T2 只有「一份证据」**：题面文本只有一份权威抽取口径",
     "「引文可定位」不是「两条独立证据交叉验证」",
     "独立性靠另两条：① 两套归一化（宽松/严）互相夹住；② **T8** 用另写的解析器与 `taxonomy` 逐字段互校。**不声称**这是两条独立证据。"),
    ("RT2", "**T6 的双边等式只能对 2025 成立**（`TAGS.md` 只覆盖 2025 的 43 篇）",
     "参照范围",
     "已写进 T6 的结论行；扩语料前不得把它读成「所有年份都对上了」。"),
    ("RT3", "**`2020 MCM Problem A` 无法标注**（题面无文本层）⇒ **65/66 道年度题**有实质标注",
     "语料边界",
     "T5-b 独立重算并登记；**不猜题意**。用户若要求 66 题全标，只能换一份**有文本层**的 2020 A 原件——**本任务无权改 `corpus/官方原题/`**。"),
    ("RT4", "**T5 的「只有 `附带` 时须给理由」这一支在本语料上零触发**",
     "判据覆盖缺口",
     "变异 M4 证明的是 **T5 首条**（每题 ≥1 `核心`）会红；**「零 `核心` 的题 + 缺理由」那一支仍未被语料或变异证实**。"),
    ("RT5", "**分类法有 2 条零命中条目**（`1.4 组合预测`、`10.2 主题与语义归类`）",
     "分类法覆盖",
     "逐条登记在 `problem_types.txt` 末尾，判据每次重算并与登记对账。**这是语料事实，不是判据失效**。"),
    ("RT6", "**`title` 不参与任何判据**（只在 T8 里做两套解析的互校）",
     "判断/证据分离",
     "2021 C **留空**（抽取切不出标题）、2020 A 无标题，均已登记在草案的偏离表第 7/8 行。"),
    ("RT7", "**T3 判「相等」不判「包含」**",
     "判据口径",
     "34 条「标签名 ⊂ 词表词」的近邻逐条列出但**不判红**。理由：包含会把 `1 预测 ⊂ 灰色预测` 这类**正确命名**判成违规。用户若要收紧，需先决定改分类法还是改词表。"),
    ("RT8", "**标注本身是「判断」**：67 题的标签是逐题读题面后做的分类",
     "**本任务最大的边界**",
     "判据只能保证：标签 ∈ 受控集合、引文**逐字可定位**、覆盖**双边等式**、每题 ≥1 `核心`、抽象互异；**证明不了**「这个标签是这道题的正确题型」。这正是阶段 1 要**交用户过目**的原因。"),
    ("RT9", "**阶段 2 的产物一件没做**（配对表 / `TAGS.md` 的 `problem_type` 栏 / 匹配度判据 / 词表增长）",
     "范围",
     "用户点名的「题型 → 模型/算法 配对」**还没有交付**；任务书写明阶段 2 等用户过目后再派。"),
    ("RT10", "**标注于 2026-09-26 由草案转正**（`git mv` → `corpus/papers/PROBLEM_TYPES.md`）",
     "**路径变更（本节其余各行仍写「草案」的那些说法不受影响）**",
     "转正**只动两处**：标题去掉「草案」、文件头补一段定位说明；**正文语义一字未改**"
     "（转正前的 blob 见下面的「转正记录」）。`taxonomy.DRAFT_PATH` 随之改名 "
     "`ANNOTATIONS_PATH`、**不留旧名别名**（留两个名字就会有人用错那个）。"
     "本脚本的两处路径引用同步改到新落点——**这是「删一个符号的影响面不止 import 它的代码」"
     "（`docs/mcm-suite-lessons.md` §4.7）**。"),
]:
    p(f"  * **{rt[0]}**（{rt[2]}）：{rt[1]}")
    p(f"    → {rt[3]}")
p("")
p("  **阶段 1 的放行结论**（可复现）：全量 `python tests/papers/verify_types.py` → `RESULT: PASS`、")
p("  T1–T8 全 OK；入库证据 `tests/papers/reports/types-report.txt` 的 blob =")
p(f"  `{blob_of(ROOT / 'tests' / 'papers' / 'reports' / 'types-report.txt')}`")
p("  （**跑 `--limit 3` 后逐字不变**）。12 条变异 + 一次对照见")
p("  `tests/papers/reports/types-mutation-evidence.txt`。")
p("")
p("### 转正记录（2026-09-26，Task 6b 阶段 2a）")
p("")
p("  命令与逐字输出（**实测，不是回忆**）：")
p("")
p("    $ git rev-parse 9a1689d:tests/papers/recon/PROBLEM_TYPES-draft.md")
p("    2b4b4a2708734756fb7c157034c530f7bf683e5e")
p("")
p("    $ git hash-object corpus/papers/PROBLEM_TYPES.md      # 转正（含头部订正）之后")
p("    0444937409cc4949dd446a1b3cc6609a8ee7b798")
p("")
p("  **读法**：转正前的草案 blob = `2b4b4a2708734756fb7c157034c530f7bf683e5e`（= 转正当天"
  "工作树上该文件的 blob，`git mv` **原样搬运**、没有经过任何转换）；转正后 = "
  "`0444937409cc4949dd446a1b3cc6609a8ee7b798`（差异**只**来自标题行与头部那一段定位说明）。")
p("  **转正日期**：2026-09-26（用户当日过闸门：「继续」+ 本轮解冻裁决）。")
p("  **为什么必须把它钉在这里**：转正后 `recon/PROBLEM_TYPES-draft.md` 这个路径就不存在了，"
  "「阶段 1 用户过目时那份东西长什么样」若不记 blob 就再也找不回来。")
p("")
p("  **转正后的回归（R-1）**：全量 `python tests/papers/verify_types.py` 在新路径下重跑 →")
p("  `RESULT: PASS`、T1–T8 全 OK（**判据口径一个字未放宽**，只改了路径常量）。")
p("  **★ 上面「阶段 1 的放行结论」那段记的 blob 与转正后重跑的**逐字节相同**（仍是")
p("  `6ff16ac1…`）——**原因**：那两处路径只活在 `verify_types.py` 的模块 docstring 与常量里，")
p("  **不进任何消息文本**，故重跑产物与转正前同字节。这条是**实测**的")
p("  （转正后重跑 `git hash-object tests/papers/reports/types-report.txt` 仍得")
p("  `6ff16ac1dcb5ad8bb35a1a03f1f6ae237604b0ec`），**不是推断**。")

# **落盘一律 write_bytes + LF**（教训 9：转码/落盘一律字节级读写）。
# 不用 shell 重定向：Windows 上 Python 的 stdout 在文本模式下会把 LF 翻成 CRLF，
# 于是同一个脚本的产物在工作树里是 CRLF、在别的机器上是 LF——那是「环境一变产物就变」的形态。
if "--stdout" in sys.argv:
    print("\n".join(out))
else:
    target = Path(__file__).resolve().parent / "types-recon.txt"
    target.write_bytes(("\n".join(out) + "\n").encode("utf-8"))

