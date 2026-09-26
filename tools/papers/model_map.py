"""Task 6b 阶段 2a：`corpus/papers/MODEL_MAP.md` —— **题型 → 模型/算法** 配对表。

## 两个数据源、都**读回**、都不重算

| 来源 | 提供什么 |
| :--- | :--- |
| `taxonomy.load_annotations()`（`corpus/papers/PROBLEM_TYPES.md`） | 题型 `(L1,L2)`、`核心/附带` 标记、`data_regime` |
| `corpus/papers/TAGS.md`（Task 6 的产物） | `models` 命中与**二层指针**（词 + md 文件 + 页码 + 片段） |

**本模块绝不自己去 md 里抽模型。** 模型只从 `TAGS.md` 读回：若在这里再抽一遍，
配对的两侧就共用同一份抽取代码，判据 M-3（`(篇, 模型)` 对的**两向等式**）当场退化成
恒真——**那正是本项目第七例「判据跟自己对答案」的形态**。同理，题型只从标注文件读回
（TAGS 的 `problem_type` 栏是它的副本，本模块不重推）。

## 推理轴只有两条：`(L1,L2)` × `data_regime`

`scenario`（场景）**不进配对**——用户 2026-09-26 定案：*「'考古/旅游'等领域都只是一个场景，
实际模型的确立并不与场景有关」*。场景只在标注文件里作检索标签。

## 覆盖边界（**必须与表同读**）

`corpus/历届优秀论文/` 下**只有 `2025美赛O奖论文` 这 43 篇**被 Task 6 建过索引
（其余合集：2022/2023/2024 三本、UMAP 两本，**未建索引**，Task 9 才做）。所以
`corpus/官方原题/` 的 **67 题**里只有 **2025 六题**有论文可配，其余 **61 题**有题型、无配对。
**不得**拿别的年份的论文来凑——那不是配对、是编造。产物里有一行**机读**的边界声明
（`标注题数=67 · 有论文的题=6 · 未配对的题=61 · …`）并**逐题列出**那 61 道。

## `--limit` 与产物落点

本模块**没有 `sample` 参数**：输入是两份文本产物（不是 43 份 PDF），全量构建不到一秒，
故**不存在**「限样本覆写入库产物」这个敞口。调用方（`verify_map.py`）的 `--limit` 只影响
**报告落点**与「产物是不是入库的那一份」。
"""
import re
from dataclasses import dataclass
from pathlib import Path

from . import io, taxonomy
from .index import _esc, _unesc

# 合集的默认口径：只有它有 md/图表/公式产物，也只有它被 Task 6 建过索引。
PILOT = "2025美赛O奖论文"

# ---- 产物解析（**读回** `TAGS.md` 与 `PROBLEM_TYPES.md`）------------------------
# 一层行：`P2025-A-01 | 2025 | A | …`
L1_ROW = re.compile(r"^(P\d{4}-[A-F]-\d{2,}) \| (\d{4}) \| ([A-F]) \| ")
# 二层小标题：`### P2025-A-01 · 题 A · 2025美赛O奖论文/A/2500836.pdf`
L2_HEAD = re.compile(r"^### (P\d{4}-[A-F]-\d{2,}) · 题 ([A-F]) · ")
L2_MD = re.compile(r"^md: (.+)$")
# 二层指针行：`- <词>; p<页>; x<次数>; <片段>`（分隔符与转义规则是 `TAGS.md` 的契约）
L2_PTR = re.compile(r"^- (.*)$")
# `; ` 是 `TAGS.md` 的列表分隔符（转义后的 `;` 不会被它切开）。
TAGS_SEP = "; "
# 三层的计数行：`本层 **N** 篇（= …）`
L3_COUNT = re.compile(r"^本层 \*\*(\d+)\*\* 篇")
# 标注文件的节头（只用来**数列**：`标注题数` 这个量必须独立数一遍）。
ANNOT_SECTION = re.compile(r"^###\s+(\d{4})\s+([A-Z])\s*(?:—|-{1,2}\s*)?(.*)$")
# 数据形态的受控枚举（逐字取自 `taxonomy.DATA_REGIMES`；这里**引用它**而不是重抄——
# 它是本模块的**输入口径**，不是判据的参照；参照那一份在 `verify_map.py` 里另写）。
REGIMES = taxonomy.DATA_REGIMES
MARKS = taxonomy.MARKS


@dataclass
class ModelMapResult:
    n_problems: int
    n_papers: int
    n_buckets: int
    n_pairs: int
    map_path: Path
    # 阶段 2b 新增：**去重后**的 `(模型, 篇)` 指针行数（= `n_pairs`，同一件事的两条取法）
    # 与第四节的匹配度摘要（自报量，判据只用它跟**产物字节**对账，不拿它当依据）。
    n_ptr_rows: int = -1
    n_collected: int = -1
    n_uncollected: int = -1
    recall_num_before: int = -1
    recall_num_after: int = -1
    recall_denom: int = -1


@dataclass(frozen=True)
class Paper:
    """`TAGS.md` 一层的一行（只取本模块要用的三个字段）。"""
    sid: str
    year: str
    problem: str


@dataclass(frozen=True)
class Hit:
    """`TAGS.md` 二层的**一条指针**：`(篇, 模型)` 对 + 可落地的证据。"""
    sid: str
    model: str
    page: int
    n_occ: int
    snippet: str
    md_rel: str


# --------------------------------------------------------------------------
# 读回 `TAGS.md`
# --------------------------------------------------------------------------
def read_tags(path: Path) -> tuple[list[Paper], list[Hit], int]:
    """`TAGS.md` → `(一层行, 二层指针, 三层篇数)`。**fail-closed**：解析不出就抛。

    三条都在这一处解析：一层的 `(年, 题号)` 决定配对表的覆盖面，二层的指针决定每个
    `(篇, 模型)` 对的证据，三层的篇数进「诚实栏」。**解析不出来 = 硬失败**——
    「参照存在而没解析出来」不得记成「不适用」（约束 4）。
    """
    text = path.read_bytes().decode("utf-8")
    papers: list[Paper] = []
    hits: list[Hit] = []
    l3 = -1
    cur_sid, cur_md = "", ""
    for ln in text.split("\n"):
        ln = ln.rstrip("\r")
        m1 = L1_ROW.match(ln)
        if m1:
            papers.append(Paper(m1.group(1), m1.group(2), m1.group(3)))
            continue
        mh = L2_HEAD.match(ln)
        if mh:
            cur_sid, cur_md = mh.group(1), ""
            continue
        mm = L2_MD.match(ln)
        if mm and cur_sid:
            cur_md = mm.group(1).strip()
            continue
        mp = L2_PTR.match(ln)
        if mp and cur_sid:
            parts = _split_unesc(mp.group(1), TAGS_SEP)
            if len(parts) != 4:
                raise ValueError(
                    f"{path.name} 二层指针不是 4 段（词; 页; 次数; 片段）：{ln[:80]!r}")
            pg = re.fullmatch(r"p(\d+)", parts[1].strip())
            nx = re.fullmatch(r"x(\d+)", parts[2].strip())
            if not pg or not nx:
                raise ValueError(f"{path.name} 二层指针的页/次数不合式：{ln[:80]!r}")
            if not cur_md:
                raise ValueError(f"{path.name} 二层 {cur_sid} 的指针在 `md: ` 行之前")
            hits.append(Hit(cur_sid, _unesc(parts[0]).strip(), int(pg.group(1)),
                            int(nx.group(1)), _unesc(parts[3]), cur_md))
            continue
        m3 = L3_COUNT.match(ln)
        if m3 and l3 < 0:
            l3 = int(m3.group(1))
    if not papers:
        raise ValueError(f"{path.name} 一层一行都没解析出来（参照存在而没解析出来 ⇒ 硬失败）")
    if not hits:
        raise ValueError(f"{path.name} 二层一条指针都没解析出来")
    if l3 < 0:
        raise ValueError(f"{path.name} 三层的计数行没解析出来")
    return papers, hits, l3


def _split_unesc(s: str, sep: str) -> list[str]:
    """按**未转义**的 `sep` 切分（转义规则是 `index._esc` 的契约：`\\;` 不是分隔符）。"""
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


# --------------------------------------------------------------------------
# 生成
# --------------------------------------------------------------------------
def build(collection: str = PILOT, out_dir: Path | None = None) -> ModelMapResult:
    """生成 `MODEL_MAP.md`。**确定性**：同输入 ⇒ 同字节（2b 会重跑它）。

    `out_dir=None` → `io.DERIVED`（入库产物目录）。与 `index.build` 不同，本函数
    **没有 `sample`**（见模块 docstring），故不存在「限样本覆写入库产物」的敞口，
    也就不需要那条 `sample + out_dir=None` 的守卫。
    """
    anns = taxonomy.load_annotations(taxonomy.ANNOTATIONS_PATH)
    tags_path = io.DERIVED / "TAGS.md"
    if not tags_path.is_file():
        raise FileNotFoundError(
            f"Task 6 的 `{tags_path.relative_to(io.REPO).as_posix()}` 不在"
            f"——「没跑过」与「零命中」是两件事，不得混同（fail-closed）")
    papers, hits, n_zero = read_tags(tags_path)

    by_key = {(str(a.year), a.problem): a for a in anns}
    if len(by_key) != len(anns):
        raise ValueError("标注文件里有重复的 `(年, 题号)` 节")

    # 本合集实际有论文的题（**由 TAGS 一层决定**，不由标注决定——
    # 「标注里有、产物里没有」的题落进覆盖边界，不是错误）。
    probs: list[tuple[str, str]] = []
    for p in papers:
        if (p.year, p.problem) not in probs:
            probs.append((p.year, p.problem))
    probs.sort()
    for year, prob in probs:
        if (year, prob) not in by_key:
            raise KeyError(
                f"TAGS 一层里有 {year} 题 {prob}，标注文件里却没有它——"
                f"题型读不回来，拒绝写空值（fail-closed）")
        if not by_key[(year, prob)].labels:
            raise KeyError(
                f"标注文件里 {year} 题 {prob} 的状态是「读不出」（无标签）——"
                f"配对表没有可用的题型轴，拒绝写占位值")
    uncovered = [k for k in sorted(by_key) if k not in set(probs)]

    hits_by_paper: dict[str, list[Hit]] = {}
    for h in hits:
        hits_by_paper.setdefault(h.sid, []).append(h)
    for v in hits_by_paper.values():
        v.sort(key=lambda h: (h.page, h.model))
    papers_by_prob: dict[tuple[str, str], list[Paper]] = {}
    for p in papers:
        papers_by_prob.setdefault((p.year, p.problem), []).append(p)
    for v in papers_by_prob.values():
        v.sort(key=lambda p: p.sid)
    sid2paper = {p.sid: p for p in papers}

    # ---- 桶：`(L1, L2, data_regime)` → 该桶的 `(模型, 篇)` 对 ------------------
    buckets: dict[tuple[str, str, str], list[tuple[str, str]]] = {}
    marks: dict[tuple[str, str, str], set[str]] = {}
    for (year, prob), group in sorted(papers_by_prob.items()):
        a = by_key[(year, prob)]
        if a.data_regime not in REGIMES:
            raise ValueError(f"{year} {prob} 的 `data_regime` {a.data_regime!r} 不在受控枚举里")
        for l1, l2, mark in a.labels:
            key = (l1, l2, a.data_regime)
            marks.setdefault(key, set()).add(mark)
            for p in group:
                for h in hits_by_paper.get(p.sid, []):
                    buckets.setdefault(key, []).append((h.model, p.sid))
    # 每个桶内**去重**（同一个 `(模型, 篇)` 对只列一次），并按 (模型, 篇) 排序
    for k in buckets:
        buckets[k] = sorted(set(buckets[k]))

    # ---- 去重后的 `(模型, 篇)` 行 + 「所属桶」列（Task 6b 阶段 2b 的形态）----------
    # 桶号 = `第二节` 表里「桶」列的编号（= `sorted(buckets)` 的序号，1 起）。
    # **判据 M-13 判这一列**：每行的桶号集合 == 由标注（该篇题号的标签集合）推出的桶集合。
    order = sorted(buckets)
    bucket_no = {k: i for i, k in enumerate(order, 1)}
    pair_buckets: dict[tuple[str, str], list[int]] = {}
    for k in order:
        for model, sid in buckets[k]:
            pair_buckets.setdefault((model, sid), []).append(bucket_no[k])
    for v in pair_buckets.values():
        v.sort()
    ptr_rows = sorted(pair_buckets)

    # ---- 第四节：匹配度（**同源**：`coverage.compute()` 一次算出，这里只渲染）----
    from . import coverage as cov
    cres = cov.compute()
    sec4 = cov.render_section(cres)

    dest = out_dir or io.DERIVED
    dest.mkdir(parents=True, exist_ok=True)
    path = dest / "MODEL_MAP.md"
    path.write_bytes(_render(collection, papers, hits, n_zero, by_key, probs,
                             uncovered, buckets, marks, papers_by_prob,
                             hits_by_paper, sid2paper, pair_buckets, ptr_rows,
                             sec4).encode("utf-8"))
    return ModelMapResult(
        n_problems=len(probs), n_papers=len(papers), n_buckets=len(buckets),
        n_pairs=len({(s, m) for v in buckets.values() for m, s in v}),
        map_path=path, n_ptr_rows=len(ptr_rows), n_collected=len(cres.collected),
        n_uncollected=len(cres.uncollected),
        recall_num_before=cres.num_before, recall_num_after=cres.num_after,
        recall_denom=cres.denom)


def _render(collection: str, papers: list[Paper], hits: list[Hit], n_zero: int,
            by_key: dict, probs: list[tuple[str, str]], uncovered: list[tuple[str, str]],
            buckets: dict, marks: dict, papers_by_prob: dict,
            hits_by_paper: dict, sid2paper: dict,
            pair_buckets: dict | None = None,
            ptr_rows: list | None = None, sec4: str = "") -> str:
    # **兼容旧签名**（第四、五位置参数按位置传）：本函数只在 `build()` 里被调用，
    # 但把新参数放成关键字默认值能让「谁没跟上新形态」当场表现为**产物少一节**，
    # 而不是一个 `TypeError` 逃出 `checks()`（那是 2a 栽过的形态）。
    pair_buckets = pair_buckets or {}
    ptr_rows = ptr_rows or []
    L: list[str] = []
    n_pairs = len({(s, m) for v in buckets.values() for m, s in v})
    L += [
        "# MODEL_MAP — 题型 → 模型/算法 配对表（2025 美赛 O 奖论文）",
        "",
        f"> 合集：`corpus/历届优秀论文/{collection}/`　·　篇数：**{len(papers)}**"
        f"　·　题数：**{len(probs)}**　·　桶数：**{len(buckets)}**"
        f"　·　`(模型, 篇)` 对：**{n_pairs}**",
        "> 生成器：`tools/papers/model_map.py` 的 `build()`（**确定性**：同输入同字节）；"
        "判据：`tests/papers/verify_map.py`（M-1…M-16）。",
        "",
        "## 口径（读表之前先读这一段）",
        "",
        "1. **两个数据源、都读回、都不重算**：题型/数据形态 ← "
        f"`{_ann_note()}`（人工逐题读题面后的标注）；模型/算法与其**指针** ← "
        "`corpus/papers/TAGS.md`（Task 6 的产物：受控词表 `tools/papers/vocab/models.txt` "
        "的**字面命中**）。**本表不自己去 md 里抽模型**——那会让配对的两侧同源，"
        "「配对 == 指针」这条判据当场变成恒真。",
        "2. **配对的推理轴只有两条：`(L1,L2)` × `data_regime`**（用户 2026-09-26 定案）。"
        "`scenario`（场景，如「考古 / 旅游」）**只作检索标签、不进配对**"
        "（原话：*「实际模型的确立并不与场景有关」*）。",
        "3. **`核心` / `附带` 的用法**：`核心` = 题干明确要求做这件事；"
        "`附带` = 题面出现但非题干任务。**两类都进桶**（信息不丢），桶的「标记」列写出该桶"
        "的标记；**查表时优先看 `核心` 桶**——`附带` 桶说的是「获奖论文在解决题干任务时"
        "顺带用到的」。",
        "4. **指针的展开形态（阶段 2b 改过形状，这里说明为什么）**：第二节先给**每个桶一行**"
        "的配对总表（8 列），再给**按 `(模型, 篇)` 去重**的指针行——**每条 = 一个对**，"
        "末尾多一列**「所属桶」**。**上一版**是「同一个对在每个标签桶里各抄一遍」"
        "（1646 行 / 334 KB），同一个对平均重复约 3.8 次；用户 2026-09-26 裁决去重。"
        "**判据跟着改了形状**（原 M-3 → 现 M-13）：不再拿「逐桶展开」判两向相等，"
        "改成拿**去重后的对集合**判，并**另判**每行的「所属桶」集合 == 由标注推出的桶集合。"
        "这不是放宽：**去重后判的是同一个集合**，而「桶归属」这一列在旧形态里**根本没有**"
        "（旧形态靠重复隐式携带它，无从单独判）。",
        "5. **`x<次数>` 是「该词在**该篇全篇**出现的次数」**（不是这一行的）；"
        "**低置信 = `x1`（全篇只出现一次）**，单列在第三节。",
        "6. **本表是「获奖论文用过什么」的事实登记，不是「这道题该用什么模型」的规范建议**"
        "（后者要的是匹配度与效度分析，属阶段 2b）。",
        "",
        "## 覆盖边界（**机读**，必须与表同读）",
        "",
        f"> 覆盖边界：标注题数={len(by_key)} · 有论文的题={len(probs)} · "
        f"未配对的题={len(uncovered)} · 覆盖年份="
        f"{'/'.join(sorted({y for y, _p in probs}))} · "
        f"未配对逐题={'、'.join(f'{y} {p}' for y, p in uncovered) if uncovered else '（无）'}",
        "",
        f"* **本表只覆盖 {'/'.join(sorted({y for y, _p in probs}))} 的 "
        f"{'/'.join(p for _y, p in probs)} 共 {len(probs)} 题**"
        f"（`corpus/历届优秀论文/` 里**只有 `{collection}` 这 {len(papers)} 篇被建过索引**；"
        "其余合集：2022 / 2023 / 2024 三本与 UMAP 两本**未建索引**，Task 9 才做）。",
        f"* `corpus/官方原题/` 的题面共 **{len(by_key)}** 道，其余 **{len(uncovered)}** 道"
        "**有题型、无配对**（逐题列在上面那一行里）。**不得**拿别的年份的论文来凑——"
        "那不是配对、是编造（任务书 §一 产物 3 的明文边界）。",
        "* 等式：**有论文的题 + 未配对的题 == 标注题数**"
        f"（{len(probs)} + {len(uncovered)} == {len(by_key)}），"
        "两边都与标注文件**逐题**对得上（判据 M-6）。",
        "",
        "## 第一节 · 逐题（{} 题）".format(len(probs)),
        "",
    ]
    for year, prob in probs:
        a = by_key[(year, prob)]
        group = papers_by_prob[(year, prob)]
        L.append(f"### {year} {prob} — {a.title or '（题面抽取切不出标题）'}")
        L.append("")
        labs = "；".join(f"`{m}` **{l1} · {l2}**" for l1, l2, m in a.labels)
        L.append(f"- 题型（`核心` / `附带` **全列**）：{labs or '（无）'}")
        L.append(f"- 数据形态：`{a.data_regime}`")
        L.append(f"- 场景（**只作检索标签，不进配对**）：{a.scenario or '（无）'}")
        L.append(f"- 论文数：{len(group)}")
        cnt: dict[str, int] = {}
        for p in group:
            for h in hits_by_paper.get(p.sid, []):
                cnt[h.model] = cnt.get(h.model, 0) + 1
        L.append(f"- 该题论文用过的模型/算法（**去重 {len(cnt)} 个**，附篇数）：")
        if not cnt:
            L.append("  - （无命中——见第三节「诚实栏」）")
        for model, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
            sids = " ".join(p.sid for p in group
                            if any(h.model == model for h in hits_by_paper.get(p.sid, [])))
            L.append(f"  - {_esc(model)}（{c} 篇）：{sids}")
        L.append("")

    L += [
        f"## 第二节 · 按 `(L1,L2)` × `data_regime` 聚合（**每个桶一行**）",
        "",
        f"共 **{len(buckets)}** 个桶。列序：`桶 | (L1,L2) | data_regime | 标记 | 来源题 | "
        f"论文数 | (模型,篇) 对 | 模型/算法（篇数）`。",
        "",
        "| 桶 | `(L1,L2)` | `data_regime` | 标记 | 来源题 | 论文数 | (模型,篇) 对 "
        "| 模型/算法（篇数） |",
        "| :-- | :-- | :-- | :-: | :-- | ---: | ---: | :-- |",
    ]
    order = sorted(buckets)
    for i, key in enumerate(order, 1):
        l1, l2, reg = key
        pairs = buckets[key]
        srcs = sorted({(sid2paper[s].year, sid2paper[s].problem) for _m, s in pairs})
        sids = sorted({s for _m, s in pairs})
        cnt: dict[str, int] = {}
        for m, _s in pairs:
            cnt[m] = cnt.get(m, 0) + 1
        modelcell = " · ".join(f"{_esc(m)}（{c} 篇）"
                              for m, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])))
        L.append(f"| {i} | {_esc(l1)} · {_esc(l2)} | {_esc(reg)} "
                 f"| {'/'.join(sorted(marks[key]))} "
                 f"| {'、'.join(f'{y} {p}' for y, p in srcs)} | {len(sids)} | {len(pairs)} "
                 f"| {modelcell} |")
    L += [
        "",
        "> **读法**：「论文数」= 该桶里出现过的**不同论文**数；「(模型,篇) 对」= 该桶里"
        "**不同 `(模型, 篇)` 对**的条数。后者 ≥ 前者（一篇在一个桶里可以用多个模型）；"
        "两者都由下一小节的**去重指针行**按「所属桶」列**反推**得出（判据 M-2 两向判）。",
        "",
        "### 第二节 · 指针（**按 `(模型, 篇)` 去重**，每条一行）",
        "",
        f"**这一小节就是「配对」的全集**：**{len(ptr_rows)}** 行，每行 = 一个 `(模型, 篇)` 对。"
        "同一个对**只出现一次**；它落在哪几个桶由**末列「所属桶」**给出（桶号 = 上一节表里的"
        "「桶」列，逗号分隔、升序）。**上一版把同一个对在每个桶里各抄一遍（1644 行），"
        "去重后是这一版**——判据 M-13 判的就是「去重后的对集合 ↔ `TAGS.md` 二层的对集合」"
        "两向相等，以及每行的「所属桶」与标注推出的桶集合相等。",
        "",
        "格式：末列之前与 `TAGS.md` 二层**逐字相同**，前面多一个 `篇` 字段，末尾多一个桶号列：",
        "`- <模型>; <稳定 ID>; p<页>; <md 文件（仓库相对）>; <md 整行逐字>; <桶号,桶号,…>`"
        "（`; ` 是分隔符，值内的 `;`/`|`/反斜杠/NUL/CR/LF 按 `TAGS.md` 同一套规则转义）。",
        "",
    ]
    for model, sid in ptr_rows:
        hs = [h for h in hits_by_paper.get(sid, []) if h.model == model]
        if len(hs) != 1:
            raise ValueError(f"{sid} 的 {model!r} 在 TAGS 二层有 {len(hs)} 条指针"
                             f"（应恰好 1 条——「每词首次出现」）")
        h = hs[0]
        bnos = ",".join(str(n) for n in pair_buckets[(model, sid)])
        L.append(f"- {_esc(model)}{TAGS_SEP}{_esc(sid)}{TAGS_SEP}p{h.page}"
                 f"{TAGS_SEP}{_esc(h.md_rel)}{TAGS_SEP}{_esc(h.snippet)}"
                 f"{TAGS_SEP}{bnos}")

    low = [(h.model, h.sid, h.page, h.snippet) for h in hits if h.n_occ == 1]
    low.sort()
    zero_papers = [p.sid for p in papers if not hits_by_paper.get(p.sid)]
    L += [
        "## 第三节 · 诚实栏（**不藏**）",
        "",
        f"* **`models` 栏零命中的篇**：条数={len(zero_papers)} · TAGS第三层={n_zero} · "
        f"逐篇={'、'.join(zero_papers) if zero_papers else '（无）'}",
        "  零命中**不等于**「这篇没用模型」，只等于「词表里的模型名一个都没出现」——"
        "词表外与「用了但没写名字」的模型**抓不到**（`TAGS.md` 头部的已知漏检，此处照印）。"
        "本条的两个数**都要报**（本表逐篇数 = `TAGS.md` 第三层的篇数）——只报一个数会让"
        "「本表漏列了零命中的篇」看不出来。",
        f"* **低置信条目**：条数={len(low)} · 总指针={len(hits)} · "
        f"口径=`x1`（该模型名在**该篇全篇**只出现 1 次）",
        "  **这是可机读的形式标记，不是质量判断**——单次提及不等于用得不重要；"
        "它们的片段仍逐条列在第二节。逐条（`模型; 篇; p页; 片段`）：",
        "",
    ]
    if not low:
        L.append("  （无）")
    for model, sid, page, snippet in low:
        L.append(f"  - {_esc(model)}{TAGS_SEP}{_esc(sid)}{TAGS_SEP}p{page}"
                 f"{TAGS_SEP}{_esc(snippet)}")
    L += [
        "",
        "* **本表证明不了的事**（与表同读）：① 「题型 → 模型」这条配对的**效度**"
        "（「给定题型 X，用模型 Y 合不合适」）本表回答不了——第四节量的是**匹配度**"
        "（召回 + 精确性），那是**度量**不是**效度**；"
        "② 配对的两侧都是**已有产物的读回**——题型来自人工标注、模型来自词表字面命中，"
        "本表**不新增任何判断**；③ 场景（`scenario`）不进配对，故本表**不能**回答"
        "「考古类题目该用什么模型」这类问题。",
        "",
    ]
    L.append(sec4)
    return "\n".join(L) + "\n"


def _ann_note() -> str:
    """标注文件的仓库相对路径（产物里只写相对形式）。"""
    return taxonomy.ANNOTATIONS_PATH.relative_to(io.REPO).as_posix()
