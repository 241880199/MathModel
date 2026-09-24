"""水印处理模块的校验（返工版：判据围着**结构性机制**重写）。

初版把「水印恒为 MicrosoftYaHei 72pt」这一个样本的特征当成了通则，正文侧
另走了一条**字体启发式**。实测全语料 201 份里水印有三套字体（2025 是
MicrosoftYaHei 72pt、2023/2024 是 KaiTi 74.4/76.5pt、2023 另有 SimHei
83.4pt），启发式只覆盖 43/120——而试点的 43 份恰好全在命中范围内，于是
**试点绿着通过、全量才炸**。

本脚本按「怎么让这个错下次一定会被抓到」重排判据：

  * 第 1 节把缺陷本身写成证据：两种方法的判别力在报告里并排摆着，并且
    **每次运行都在全语料 201 份上重算**（不是抄 recon 的结论）。
  * 第 3 节（A3）是 fail-closed 的那条：置空前后逐 span 做多重集差，
    **被移除的每一个 span 都必须是 WM_WORDS 里某串的子串**。抽错流会把
    正文一起吃进去，那时它当场打印肇事 span 并转红，而不会「字数少了点、
    看着还行」地滑过去。
  * 第 5 节把「水印件上 strip 返回 0」显式判死：0 不是无事发生，是
    「这篇的水印形态不认识」，下游会静默带着水印走完全流程。
  * 样本按 **recon 的 ground truth**（`watermark-scan.json` 的 `wm_texts` 非空）
    分成「水印件 / 对照件」两组。**不按模块自己的 `find_watermark_xrefs` 分组**：
    那样分组等于让判据自己证自己——模块一旦认不出水印，那份样本就被挪出检查集，
    2/3/5 节的断言整段被架空，永远不会红。

报告是入库的判据证据，所以：
  * 内容一律 write_bytes + LF 落盘，路径按仓库相对形式打印（绝对路径只在
    这台机器上成立，换台机器重跑就整篇变红，等于噪音）；
  * 报告写入无条件执行（main 的结尾，不在 try 内）：脚本崩了也不能把上一次
    的 RESULT: PASS 留在库里冒充本次结论；
  * 各 import 放在 checks() 体内：模块被改坏时 import 当场抛，那是 main()
    的 try 保护得到的路径，能拿到「崩溃 → 写成 FAIL」的证据。
  * 人工目视结论**不由本脚本生成**：本脚本每次运行都会重写 wm-report.txt，
    结论若写在那份报告里，任何一次重跑都会抹掉它。改为读一份独立的、
    只写一次的存档并抄进报告：重跑不丢，缺了则 FAIL。
"""
import json
import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
REPORTS = HERE / "reports"
REPORT = REPORTS / "wm-report.txt"
# A1 基线。全量那份是本次返工新加的（201 份 / 6 个合集）。2025 那份**保留**
# 原样：Task 7 的汇总要读它，本脚本顺带验它仍是全量基线的逐条子集。
BASELINE_ALL = REPORTS / "origin-sha256-all.txt"
BASELINE_2025 = REPORTS / "origin-sha256-2025.txt"
VISUAL = REPORTS / "wm-visual-confirm.txt"
SCAN = HERE / "recon" / "watermark-scan.json"
PNGS = ["a4-2500836-with-wm.png", "a4-2500836-no-wm.png"]

# 全语料扫描时每份最多看几页。与 recon 的 wm_font_probe.py 同口径——两处的
# 覆盖数要能直接对上，口径不同的话「43/120」这个数字就变成两套含义。
# 全文档口径的 A3 在第 3 节按样本验；全文档的 A3 全量实测见 task-2 报告。
CORPUS_PAGES = 4

# 初版正文侧用的字体启发式，**已废弃**。留在这里不是「还能用」，而是为了把
# 缺陷本身写成可复算的证据：43/120 这个数字由它每次运行当场算出来，
# 而不是抄一句「已知有缺陷」。
_OLD_FONT, _OLD_MIN_SIZE = "MicrosoftYaHei", 60.0


def rel(p) -> str:
    """仓库相对路径。"""
    try:
        return Path(p).relative_to(ROOT).as_posix()
    except ValueError:
        return Path(p).as_posix()


def parse_baseline(text: str) -> dict[str, str]:
    """解析基线清单为 {仓库相对路径(posix): sha256}。

    基线由 io.sha256_tree 生成，其键在 Windows 上是 `2025美赛O奖论文\\A\\x.pdf`
    这种反斜杠形态；统一换成 posix 再比对，免得分隔符差异变成假 diff。
    解析不出分隔符就抛——绝不让一条坏行静默变成"少了一条、其余都对"。
    """
    out: dict[str, str] = {}
    for ln in text.splitlines():
        if not ln.strip():
            continue
        digest, sep, path = ln.partition("  ")
        if not sep or not digest or not path:
            raise ValueError(f"基线行格式不对（缺两空格分隔符）: {ln!r}")
        out[path.replace("\\", "/")] = digest
    return out


def font_heuristic(font: str, size: float) -> bool:
    """**已废弃**的初版判据：字体是微软雅黑且字号 >= 60。

    它只在 2025 那 43 份上成立。保留是为了让「它覆盖不到全语料」这件事
    在报告里每次都被当场量出来，而不是靠一句注释自我声明。
    """
    return _OLD_FONT in font and size >= _OLD_MIN_SIZE


def spans_font(doc, npages: int | None = None) -> list[tuple[str, float, str]]:
    """逐 span 取 (字体, 字号, 文本)。

    `npages` 只用于全语料扫描的**成本控制**：全文档的 dict 层抽取在 201 份
    上要 10 分钟量级，前 4 页则 20 秒。全文档口径由样本那条路径覆盖
    （样本不传 npages，与 watermark.spans 逐字对齐，见 measure_sample 里
    的一致性复核）。
    """
    n = doc.page_count if npages is None else min(npages, doc.page_count)
    out = []
    for pno in range(n):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for s in line["spans"]:
                    if s["text"].strip():
                        out.append((s["font"], round(s["size"], 1), s["text"]))
    return out


def pick_samples(scan: list[dict]) -> list[tuple[str, str, tuple[str, ...]]]:
    """从扫描清单按 `wm_texts` 分组取样本，返回 [(标签, 仓库相对路径, recon 水印字)]。

    **不硬编码路径**。第三个元素就是 recon 的 ground truth：非空 = 这份论文
    「已知有水印」。后面各节按它分组，而不是按模块自己的判断分组——否则
    「模块没认出水印」这件事会把样本从检查集中挪走，判据变成自己证自己。

    2023 合集的磁盘目录名带「年」（`2023年美赛O奖论文`），题号层之上还多一层
    中文子目录，路径形态与 2024/2025 都不同；硬编码在换批次时只会静默取错文件。
    这里只按 (水印字, 合集) 分组、各取路径序首个，路径一律来自 recon 的实测记录。
    分组到合集而不是只到水印字，是因为同一厂商的 2023 与 2024 是两棵目录树、
    两套字号（KaiTi 76.5 与 74.4），少验一棵就等于把「试点 vs 全量」的教训
    再犯一次。
    """
    groups: dict[tuple, list[str]] = {}
    for r in scan:
        p = r["file"].replace("\\", "/")
        collection = p.split("/")[2]
        words = tuple(sorted(set(r.get("wm_texts") or [])))
        groups.setdefault((words, collection), []).append(p)
    watermarked, controls = [], []
    for words, collection in sorted(groups, key=lambda k: (k[0], k[1])):
        path = sorted(groups[(words, collection)])[0]
        if words:
            watermarked.append((f"{collection} / {'+'.join(words)}", path, words))
        else:
            controls.append((f"{collection} / 无水印对照", path, words))
    # 对照件取一份做全文档精验即可；全语料 81 份由第 1 节的扫描覆盖。
    return watermarked + controls[:1]


def measure_sample(path: str) -> dict:
    """一份论文的全文档实测：两种方法的判别力 + A3 差集。"""
    import fitz

    from tools.papers import watermark

    doc = fitz.open(ROOT / path)
    try:
        xrefs = watermark.find_watermark_xrefs(doc)
        raw = "".join(doc[i].get_text() for i in range(doc.page_count))
        swf = spans_font(doc)
        before = Counter(t for _, _, t in swf)
        # 旧判据的产物。与结构性那条**同底**（都从 span 层取），只是按字体剔除，
        # 这样两条路径的对比是同一口径，不是拿两种抽取方式的长短去比。
        fkeep = "".join(t for f, sz, t in swf if not font_heuristic(f, sz))
        # 口径复核：**必须在置空之前**取，否则拿到的是「置空前 vs 置空后」，
        # 差的正是水印那几段，恒不相等。它要证的是本脚本自己那份 span 抽取
        # （spans_font，为了给全语料扫描限页而重写）与模块 spans() 逐字一致，
        # 免得第 1 节的扫描量的是另一个东西。
        same_basis = [t for _, _, t in swf] == watermark.spans(doc)
        n_strip = watermark.strip_in_memory(doc)
        after = Counter(watermark.spans(doc))
        text = "".join(doc[i].get_text() for i in range(doc.page_count))
    finally:
        doc.close()

    removed, added = before - after, after - before
    bad = sorted(s for s in removed if not any(s in w for w in watermark.WM_WORDS))
    fonts = Counter(f"{f} {sz}" for f, sz, t in swf if t in removed)
    return {
        "path": path,
        "xrefs": xrefs,
        "n_strip": n_strip,
        "raw_hits": [w for w in watermark.WM_WORDS if w in raw],
        "font_hits": [w for w in watermark.WM_WORDS if w in fkeep],
        "struct_hits": [w for w in watermark.WM_WORDS if w in text],
        "removed": removed,
        "added": added,
        "bad": bad,
        "fonts": fonts,
        "n_before": sum(before.values()),
        "n_after": sum(after.values()),
        "same_basis": same_basis,
    }


def sweep_corpus(scan: list[dict]) -> dict:
    """全语料扫描：两种方法在 201 份上的判别力。

    每份只看前 CORPUS_PAGES 页（与 recon 同口径）。这一节的意义在于
    **不拿试点当全量**：初版的错就是拿 2025 那 43 份的观察当通则，
    而 2025 恰好全在字体启发式的命中范围内。
    """
    import fitz

    from tools.papers import watermark

    fitz.TOOLS.reset_mupdf_warnings()
    acc = {
        "n": 0, "n_wm": 0, "n_ctl": 0,
        "font_cov": 0, "struct_cov": 0,
        "ctl_damaged": 0, "ctl_strip_nonzero": 0, "ctl_font_removed": 0,
        "bad_frag": [], "open_fail": [], "added": 0,
    }
    for r in scan:
        try:
            doc = fitz.open(ROOT / r["file"].replace("\\", "/"))
        except Exception as e:  # 打开失败=这份没验到，必须显式记，不能算通过
            acc["open_fail"].append(f"{r['file']}: {e!r}")
            continue
        try:
            swf = spans_font(doc, CORPUS_PAGES)
            before = Counter(t for _, _, t in swf)
            fkeep = "".join(t for f, sz, t in swf if not font_heuristic(f, sz))
            n_strip = watermark.strip_in_memory(doc)
            # 置空后**只取前 CORPUS_PAGES 页**：全文档的 dict 层抽取在 201 份上
            # 要 10 分钟量级，前 4 页 20 秒。全文档口径由样本那条路径覆盖。
            after_texts = [t for _, _, t in spans_font(doc, CORPUS_PAGES)]
            after = Counter(after_texts)
            stext = "".join(after_texts)
        finally:
            doc.close()

        acc["n"] += 1
        removed, added = before - after, after - before
        bad = sorted(s for s in removed if not any(s in w for w in watermark.WM_WORDS))
        if bad:
            acc["bad_frag"].append((r["file"], bad[:5]))
        if added:
            acc["added"] += 1
        if r["wm_texts"]:
            acc["n_wm"] += 1
            if not [w for w in watermark.WM_WORDS if w in fkeep]:
                acc["font_cov"] += 1
            if not [w for w in watermark.WM_WORDS if w in stext]:
                acc["struct_cov"] += 1
        else:
            acc["n_ctl"] += 1
            if removed or added:
                acc["ctl_damaged"] += 1
            if n_strip:
                acc["ctl_strip_nonzero"] += 1
            if any(font_heuristic(f, sz) for f, sz, _ in swf):
                acc["ctl_font_removed"] += 1
    acc["warnings"] = fitz.TOOLS.mupdf_warnings()
    return acc


def checks(lines: list[str]) -> bool:
    from tools.papers import io, watermark

    ok = True
    scan = json.loads(SCAN.read_bytes().decode("utf-8"))
    samples = pick_samples(scan)

    # ---- 1. 缺陷存档：两种方法并排量 ----------------------------------
    lines.append("1. 缺陷存档：字体启发式 vs 结构性机制")
    lines.append("-" * 72)
    lines.append(f"1a. 样本 {len(samples)} 份（取自 {rel(SCAN)}，按 wm_texts+合集 分组取路径序首个，不硬编码路径）")
    measured = []
    for label, path, words in samples:
        m = measure_sample(path)
        m["label"] = label
        # recon 的 ground truth：后面 2/3/5 节按**它**分组，不按模块自己的判断。
        m["recon_wm"] = bool(words)
        m["recon_words"] = words
        measured.append(m)
        lines.append(f"  [{label}]")
        lines.append(f"      {rel(ROOT / path)}")
        lines.append(f"      recon ground truth = "
                     f"{'有水印，wm_texts=' + str(list(words)) if words else '无水印（对照件）'}")
        lines.append(f"      裸 get_text       命中 = {m['raw_hits'] or '无'}")
        lines.append(f"      字体启发式后       命中 = {m['font_hits'] or '无'}")
        lines.append(f"      置空 XObject 流后  命中 = {m['struct_hits'] or '无'}")
        fonts = "、".join(f"{k} ×{v}" for k, v in m["fonts"].most_common())
        lines.append(f"      strip_in_memory 返回 = {m['n_strip']}；被移除 span 的字体/字号 = {fonts or '（无）'}")
        lines.append(f"      本脚本的 span 抽取与模块 spans() 逐字一致（全文档，置空前）= {m['same_basis']}")
        ok &= m["same_basis"]

    # 全语料重算覆盖：不把 recon 的结论抄一遍，而是每次运行当场量。
    sw = sweep_corpus(scan)
    lines.append("")
    lines.append(f"1b. 全语料覆盖（{sw['n']} 份；每份前 {CORPUS_PAGES} 页，与 recon 的 wm_font_probe.py 同口径）")
    lines.append(f"      有水印 {sw['n_wm']} 份 / 无水印 {sw['n_ctl']} 份；打开失败 {len(sw['open_fail'])} 份")
    lines.append(f"      字体启发式（已废弃） 覆盖 = {sw['font_cov']}/{sw['n_wm']}")
    lines.append(f"      结构性（置空流）     覆盖 = {sw['struct_cov']}/{sw['n_wm']}")
    lines.append(f"      对照件被结构性误伤（span 有增删 / strip 返回非 0）= {sw['ctl_damaged']} / {sw['ctl_strip_nonzero']} 份")
    lines.append(f"      对照件被字体启发式误删 span 的份数 = {sw['ctl_font_removed']}（启发式的问题在漏，不在误伤）")
    lines.append(f"      被移除片段含非水印文本的份数 = {len(sw['bad_frag'])}；置空后凭空多出 span 的份数 = {sw['added']}")
    for f, b in sw["bad_frag"][:3]:
        lines.append(f"        ! {f}: {b}")
    for f in sw["open_fail"][:3]:
        lines.append(f"        ! 打开失败 {f}")
    if sw["warnings"]:
        # 只印第一类时，「12 行均来自语料 PDF 自身缺陷」这句话里 11 行没有出处。
        # 这里把**每一个不同的行连计数全印**，分类计数之和 == 总行数，读者能自己核。
        # `... repeated N times...` 是 MuPDF 把重复告警折叠后的计数行（不是本模块
        # 或本脚本产生的），照样列出并标注，免得又变成一段没有出处的断言。
        wl = [w for w in sw["warnings"].splitlines() if w.strip()]
        lines.append(f"      MuPDF 告警 {len(wl)} 行，逐行如下（本模块不自造告警：不走渲染、"
                     f"不落盘；以下均为 fitz 打开这批语料 PDF 时记下的）：")
        for k, c in Counter(wl).most_common():
            tag = "  ← MuPDF 的重复折叠计数行" if k.startswith("...") else ""
            lines.append(f"        ×{c:<4}{k}{tag}")
    lines.append("  判据失败条件：")
    lines.append("    * 结构性覆盖不再是 100%——某份水印件的水印不是带标记的 XObject（换批次/"
    "重新导出）时当场红，而不是让它静默带着水印流下去；")
    lines.append("    * 字体启发式的覆盖追平了结构性机制——说明有人按字体补了启发式，"
    "本模块「不依赖字体」这个前提已被推翻，需要重新裁决而不是默默通过；")
    lines.append("    * 打开失败 > 0，或对照件出现 span 增删 / strip 返回非 0——标记被改松（例如"
    "只匹配 /PieceInfo）会命中正常内容流。")
    ok &= not sw["open_fail"]
    ok &= sw["struct_cov"] == sw["n_wm"] and sw["n_wm"] > 0
    ok &= sw["font_cov"] < sw["struct_cov"]
    ok &= sw["ctl_damaged"] == 0 and sw["ctl_strip_nonzero"] == 0
    ok &= not sw["bad_frag"] and sw["added"] == 0

    # 样本分组一律按 **recon 的 ground truth**（wm_texts 非空），不按模块自己的
    # xrefs 判断。按 xrefs 分组的旧写法是自证：`find_watermark_xrefs` 返回 []
    # 时那份样本被挪出检查集，2/3/5 节的断言整段被架空——判据永远不可能红。
    # 按 recon 分组后，「模块没认出这篇的水印」正是让 2/3/5 节变红的那类输入。
    wm_samples = [m for m in measured if m["recon_wm"]]
    ctl_samples = [m for m in measured if not m["recon_wm"]]
    # 空集必须判死而不是空转：本轮修的正是「检查集为空 → 判据恒真」这一类。
    # 用显式判据而不是 assert——assert 在 -O 下会被摘掉，那又变成一条不会失败的规则。
    lines.append("")
    lines.append(f"  样本分组（按 recon 的 wm_texts）：水印件 {len(wm_samples)} 份 / "
                 f"对照件 {len(ctl_samples)} 份")
    if not wm_samples or not ctl_samples:
        lines.append("    ! 有一组为空，对应各节的断言会空转通过 ← FAIL")
        ok = False

    # ---- 2. A2：置空后水印字不再出现 ----------------------------------
    lines.append("")
    lines.append("2. A2 置空水印流后，WM_WORDS 零命中")
    lines.append("-" * 72)
    for m in measured:
        lines.append(f"  [{m['label']}] 置空后命中 = {m['struct_hits'] or '无'}"
                     + ("  ← 对照件，本来就无水印字" if not m["recon_wm"] else ""))
    for m in wm_samples:
        ok &= not m["struct_hits"]
    lines.append("  判据失败条件：若置空没有真正去掉水印（标记匹配失配、水印改成"
                 "非 XObject 形态、或 doc 被换成了清洗前的另一份），水印字会留在文本里。")

    # ---- 3. A3：fail-closed 的差集判据 --------------------------------
    lines.append("")
    lines.append("3. A3（关键）置空前后逐 span 做多重集差，移除的必须**全是水印片段**")
    lines.append("-" * 72)
    for m in measured:
        frags = "、".join(sorted(m["removed"])[:8])
        lines.append(f"  [{m['label']}]")
        lines.append(f"      span {m['n_before']} → {m['n_after']}；"
                     f"移除 {len(m['removed'])} 种 / {sum(m['removed'].values())} 次；"
                     f"多出 {sum(m['added'].values())} 次")
        lines.append(f"      移除的片段 = {frags or '（无）'}")
        lines.append(f"      其中不是 WM_WORDS 子串的 = {m['bad'] or '无'}")
        if m["bad"]:
            for s in m["bad"]:
                lines.append(f"        ! 肇事 span: {s!r}")
    for m in wm_samples:
        ok &= not m["bad"]          # 吃进正文 = 当场红
        ok &= not m["added"]        # 置空只能删，不能凭空造 span
        ok &= bool(m["removed"])    # 水印件上一个片段都没少 = 没真去掉
    # 原先这里还有一条 `all(not bad and not added for m in measured)`，覆盖的是
    # 对照件那一条——与第 4 节重复（且 `not removed` 已蕴含 `not bad`）。删掉，
    # 对照件由第 4 节在 **recon 分组的** 对照集上判，比原来的 xrefs 分组更强：
    # 「recon 说无水印、模块却认出水印并删了东西」那份也落在第 4 节里当场红。
    lines.append("  判据失败条件：只要有一个被移除的 span 不是 WM_WORDS 里某串的子串"
                 "（例如正文段落、图题、公式），就 FAIL 并打印肇事 span。"
                 "真实触发路径：把 _WM_MARK 放宽成只匹配 /PieceInfo——实测全语料有 14 份"
                 "只有 /PieceInfo 没有 /Watermark，它们的正常内容流会被置空。")
    lines.append("  已知边界（不声称更强的东西）：这是**必要**条件，不是充分条件。正文里若恰好有"
                 "与 WM_WORDS 同字符的孤立 span（例如正文单独出现一个「校」字），规则会放行它。"
                 "本语料的实测差集里没有这种误伤（全语料前 4 页 0 例、样本全文档 0 例），"
                 "但不能因此说它不可能。")

    # ---- 4. 对照件零改动 ---------------------------------------------
    lines.append("")
    lines.append("4. 无水印对照件必须分毫未动")
    lines.append("-" * 72)
    for m in ctl_samples:
        clean = m["n_strip"] == 0 and not m["removed"] and not m["added"]
        lines.append(f"  [{m['label']}] recon 记录 wm_texts 为空；"
                     f"find_watermark_xrefs = {m['xrefs']}；strip_in_memory = {m['n_strip']}；"
                     f"span {m['n_before']} → {m['n_after']}；逐字节相同 = {clean}")
        ok &= clean
    lines.append("  判据失败条件：对照件上 strip 返回非 0 或 span 列表有增减"
                 "（标记被改松、或水印对象的标记出现在了正常内容流里）。"
                 "对照集按 recon 的 wm_texts 分组，故它也覆盖反向分歧："
                 "recon 说无水印、模块却认出水印并删了内容。")

    # ---- 5. 水印件上 strip 返回 0 = FAIL ------------------------------
    lines.append("")
    lines.append("5. 水印件上 strip_in_memory 返回 0 = FAIL（不是无事发生）")
    lines.append("-" * 72)
    for m in wm_samples:
        lines.append(f"  [{m['label']}] 已知有水印（recon 记录 wm_texts 非空）；")
        lines.append(f"      recon wm_texts = {list(m['recon_words'])}；裸文本实测命中 {m['raw_hits']}；"
                     f"find_watermark_xrefs = {m['xrefs']}；strip_in_memory = {m['n_strip']}")
        ok &= m["n_strip"] > 0
    lines.append("  判据失败条件：任何一份已知有水印的论文上返回 0。那说明这篇的水印形态"
                 "与已知形态不同（模块的认知与 recon 的实测对不上），下游（Task 3 正文/"
                 "Task 4 图表/Task 5 公式）会静默带着水印走完。"
                 "具体输入：让 find_watermark_xrefs 对 4 份水印件返回 []（标记失配 / 水印"
                 "不再是带标记的 XObject），本节当场红——实测见 task-2 报告「Fix round 2」。")

    # ---- 6. A1：原件未改动 -------------------------------------------
    lines.append("")
    lines.append("6. A1 原件未改动（全量基线 201 份 / 6 个合集）")
    lines.append("-" * 72)
    collections = sorted(p.name for p in io.ORIGIN.iterdir() if p.is_dir())
    live: dict[str, str] = {}
    for c in collections:
        for k, v in io.sha256_tree(c).items():
            live[k.replace("\\", "/")] = v
    base_all = parse_baseline(BASELINE_ALL.read_bytes().decode("utf-8"))
    base_2025 = parse_baseline(BASELINE_2025.read_bytes().decode("utf-8"))
    lines.append(f"  合集（从磁盘读取，不硬编码）= {collections}")
    lines.append(f"{rel(BASELINE_ALL)}：基线 {len(base_all)} 条 / 当前原件 {len(live)} 份；逐条一致 = {base_all == live}")
    sub2025 = {k: v for k, v in base_all.items() if k.startswith("2025美赛O奖论文/")}
    lines.append(f"{rel(BASELINE_2025)}：{len(base_2025)} 条；与全量基线的 2025 子集逐条一致 = {sub2025 == base_2025}")
    ok &= base_all == live and len(live) > 0
    ok &= sub2025 == base_2025 and len(base_2025) > 0
    lines.append("  判据失败条件：流水线里任何一次 doc.save() 写回原件、或有人手工改了语料 PDF，"
                 "都会让某条哈希当场对不上。")

    # ---- 7. 不产出清洗版 PDF -----------------------------------------
    lines.append("")
    lines.append("7. 不产出清洗版 PDF")
    lines.append("-" * 72)
    clean = io.DERIVED / "clean"
    lines.append(f"  {rel(clean)} 存在 = {clean.exists()}（应为 False）")
    ok &= not clean.exists()
    lines.append("  判据失败条件：设计里没有这一层，它一旦出现就说明有人把置空后的 doc 落盘了。")

    # ---- 8. 人工目视确认（存档 + 对比图） -----------------------------
    lines.append("")
    lines.append("8. 人工目视确认")
    lines.append("-" * 72)
    if VISUAL.is_file() and VISUAL.read_bytes().strip():
        lines.append(VISUAL.read_bytes().decode("utf-8").rstrip())
        lines.append(f"  （逐字存档于 {rel(VISUAL)}；刻意不由本脚本生成——本报告每次重跑都会被重写）")
    else:
        lines.append(f"  缺 {rel(VISUAL)} ← 未做人工目视确认")
        ok = False
    for png in PNGS:
        p = REPORTS / png
        size = p.stat().st_size if p.is_file() else 0
        lines.append(f"  对比图 {rel(p)} exists={p.is_file()} bytes={size}")
        ok &= p.is_file() and size > 0
    lines.append("  判据失败条件：存档缺失/为空、任一张对比图缺失或为空。")

    return ok


def main() -> int:
    lines = ["水印模块校验（返工 1：结构性机制，无字体启发式）", "=" * 72]
    try:
        ok = checks(lines)
    except BaseException:
        # io / watermark 的函数与 import 都可能抛。崩了也绝不能带着上一次的
        # PASS 死掉：这份报告是入库的判据证据，留在仓库里的绿色结论会被当成
        # 事实，而 git status 上看不出任何异常。
        lines.append("校验过程中抛出异常：")
        lines.append(traceback.format_exc())
        ok = False

    text = "\n".join(lines) + f"\n\nRESULT: {'PASS' if ok else 'FAIL'}\n"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_bytes(text.encode("utf-8"))
    print(text, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
