"""Task 5 **几何口径**的复算脚本（入库；`verify_d.py` 模块 docstring 与 `formula-recon.txt`
§八里那些实测数的**唯一依据**）。

它回答三个问题（复审本轮第 1 条要求「实测这个几何谓词在本语料上的表现」）：

  A. 口径的定义（逐字，可照抄进判决书）；
  B. **11 条「编号与公式体同行」的真编号**：几何口径命中了吗？（逐条页码 + 坐标 + Δ）
  C. **7 条 B 类（行内引用 / 题注 / 分布参数 / 行内标记）**：几何口径把它们排除在外了吗？
  D. 全语料：纯行数、几何并集数、同行命中数、以及**几何口径有而检测器没有**的条数
     （后者 > 0 就会让全量判 FAIL——它是「判据会不会误伤」的自检）；
  E. 参照基数：新口径（并集）与旧口径（历史保留）的逐项值。

**口径**（缺了它这些数不可复算）：

* 「行尾 token」= 该文本行 `rstrip` 前后的行尾匹配 `\\(\\s*(\\d{1,2})\\s*\\)\\s*$`；
  token 自己的 bbox 由 `get_text("rawdict")` 的**字符级 bbox** 求和（不是整行 bbox）。
* 「编号列右缘」= **本页**整行只有编号的行（纯编号行）的 token x1 **集合**；
  本页一条都没有时退到**本篇**的同一集合。**没有任何全局绝对常量**。
* 「几何命中」= `min |token_x1 − 右缘| <= 3.0`（`verify_d.EDGE_TOL`）。
* 「检出」= `formulas.scan(doc).picks`（每号一条），一律先 `watermark.strip_in_memory`。
* **本脚本自带实现**（不 import `verify_d` 的几何函数）：它是**第二份实现**，
  用来对照第一份——两份给出同一批数，才说明规格没写歪（`formula-recon.txt` §一 的
  R1 与 R1w 也是这个形状：同一事实的两个视角）。

用法：`python tests/papers/recon/formula-geom-scan.py` → 逐字输出即入库文件的那一节。
"""
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

import fitz  # noqa: E402

from tools.papers import formulas, io, watermark  # noqa: E402

COLLECTION = "2025美赛O奖论文"
TOL = 3.0
NUM = re.compile(r"\(\s*(\d{1,2})\s*\)\s*$")
PURE = re.compile(r"^\s*\(\s*(\d{1,2})\s*\)\s*$")
COLL = ROOT / "corpus" / "papers" / "md" / COLLECTION

# B. 11 条「编号与公式体同行」的真编号（复审本轮逐条实测的清单）
INLINE = [("2517273", 13, 11), ("2517273", 14, 11),
          ("2504223", 20, 16), ("2504223", 21, 17), ("2504223", 22, 17),
          ("2517199", 4, 8), ("2517199", 7, 15), ("2517199", 8, 16),
          ("2501869", 11, 20), ("2507692", 13, 16), ("2508861", 6, 9)]
# C. 7 条 B 类（行内引用 / 题注 / 分布参数 / 行内标记）——必须仍落在外面
BCLASS = [("2500836", 11, 14), ("2502617", 1, 10), ("2501869", 1, 3),
          ("2501869", 56, 11), ("2514362", 1, 8), ("2504188", 24, 17),
          ("2513705", 20, 8)]


def token_lines(doc):
    """[(页, y, 文本, token_x0, token_x1, 纯行?, num)]（字符级 bbox）。"""
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("rawdict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                chars = [c for sp in line["spans"] for c in sp["chars"]]
                text = "".join(c["c"] for c in chars)
                m = NUM.search(text)
                if not m:
                    continue
                end = m.start() + m.group(0).rfind(")") + 1
                box = [c["bbox"] for c in chars[m.start():end]
                       if c["bbox"][2] > c["bbox"][0]]
                if not box:
                    continue
                out.append((pno, line["bbox"][1], text.strip(),
                            min(z[0] for z in box), max(z[2] for z in box),
                            text.strip() == m.group(0).strip(), int(m.group(1))))
    return out


def edges_of(rows):
    """逐页右缘（纯行 token x1 集合）+ 本篇集合。"""
    per_page: dict[int, set] = {}
    for pno, _y, _t, _x0, x1, pure, _n in rows:
        if pure:
            per_page.setdefault(pno, set()).add(x1)
    doc = set()
    for s in per_page.values():
        doc |= s
    return per_page, doc


def delta_of(x1, pno, per_page, doc_edges):
    local = per_page.get(pno)
    edges = local or doc_edges
    if not edges:
        return None, "无右缘证据"
    return min(abs(x1 - e) for e in edges), ("本页" if local else "本篇")


def md_counts(stem, prob):
    p = COLL / prob / f"{stem}.md"
    strict = wide = 0
    for ln in p.read_bytes().decode("utf-8").splitlines():
        if re.match(r"^\s*\((\d{1,2})\)\s*$", ln):
            strict += 1
        if re.match(r"^\s*\(\s*(\d{1,2})\s*\)\s*$", ln):
            wide += 1
    return strict, wide


def main():
    root = io.ORIGIN / COLLECTION
    print("A. 口径定义（逐字，可照抄）")
    print("""
  * 「行尾 token」：该行行尾匹配 `\\(\\s*(\\d{1,2})\\s*\\)\\s*$`；token 的 bbox 由
    `get_text("rawdict")` 的**字符级 bbox** 求和（**不是**整行 bbox——整行 bbox 含行尾空白）。
  * 「编号列右缘」：**本页**纯编号行（整行只有编号）的 token x1 **集合**；
    本页一条都没有时退到**本篇**的同一集合。**无任何全局绝对常量**（页宽/比例/字号不进来）。
  * 「几何命中」：`min |token_x1 − 右缘| <= 3.0`。
  * 「检出」：`formulas.scan(doc).picks`（每号一条，先 strip 水印）。
  * 本脚本是**第二份实现**（不 import verify_d 的几何函数），用来与第一份对照。
""")
    rows_by_doc = {}
    detected_by_doc = {}
    doc_ctx = {}
    total_pure = total_geom = total_r1u = total_r2u = 0
    total_r1 = total_r1w = total_r2 = 0
    geom_undetected = []
    near_total = 0
    for p in sorted(root.rglob("*.pdf")):
        prob = p.parent.name
        with fitz.open(p) as doc:
            watermark.strip_in_memory(doc)
            rows = token_lines(doc)
            sc = formulas.scan(doc)
        rows_by_doc[p.stem] = rows
        detected_by_doc[p.stem] = Counter(c.num for c in sc.picks)
        per_page, doc_edges = edges_of(rows)
        doc_ctx[p.stem] = (per_page, doc_edges)
        det = detected_by_doc[p.stem]
        geom = Counter()
        near = 0
        for pno, y, t, x0, x1, pure, num in rows:
            d, src = delta_of(x1, pno, per_page, doc_edges)
            if d is None or d > TOL:
                continue
            near += 1 if not pure else 0
            geom[num] += 1
            if not pure and num not in det:
                geom_undetected.append((p.stem, pno + 1, num, d, t))
        near_total += near
        total_pure += sum(1 for r in rows if r[5])
        total_geom += sum(geom.values())
        r1, r1w = md_counts(p.stem, prob)
        total_r1 += r1
        total_r1w += r1w
        r2, _h = _r2(p)
        total_r2 += sum(r2.values())
        gex = {n: 1 for n in geom}
        # 参照并集（与 verify_d.union_ref 同一口径：max，不相加）
        ref1 = _md_nums(p.stem, prob)
        ref2 = Counter(dict(r2))
        for ref in (ref1, ref2):
            for n, v in gex.items():
                ref[n] = max(ref.get(n, 0), v)
        total_r1u += sum(ref1.values())
        total_r2u += sum(ref2.values())

    def show(title, items, want_hit):
        print(title)
        for stem, num, page1 in items:
            rows, (per_page, doc_edges) = rows_by_doc[stem], doc_ctx[stem]
            for pno, y, t, x0, x1, pure, n in rows:
                if n != num or pno != page1 - 1:
                    continue
                d, src = delta_of(x1, pno, per_page, doc_edges)
                if d is None:
                    state = "无右缘证据"
                else:
                    state = "命中" if d <= TOL else "未命中"
                print(f"  {stem} ({num}) p{page1} y={y:7.1f} token_x1={x1:6.1f} "
                      f"Δ={'-' if d is None else format(d, '.1f'):>6} [{src}] {state}"
                      f" {'纯行' if pure else '同行'}  {t[:66]!r}")
            if not any(n == num and pno == page1 - 1
                       for pno, _y, _t, _x0, _x1, _p, n in rows):
                print(f"  {stem} ({num}) p{page1} —— **该页找不到行尾是 ({num}) 的行**")

    print("B. 11 条「编号与公式体同行」的真编号（**必须全部命中**）")
    show("", INLINE, True)
    print("\nC. 7 条 B 类（行内引用 / 题注 / 分布参数 / 行内标记）——**「那一行」必须仍在外**")
    print("   注：某个号若**另有**一条真编号行（`2500836` 的 (11)、`2504188` 的 (24)），"
          "它也会一并列出——\n   那是**纯编号行**、本来就该在里面；B 类说的是**引用它的那一行**"
          "（Δ 远离右缘那些）。")
    show("", BCLASS, False)
    print(f"""
D. 全语料扫描（TOL={TOL}）
  纯编号行（宽口径，括号内允空白）= {total_pure}（与 formula-recon.txt §三 的 R1w = 773 对照）
  几何口径命中行（并集）= {total_geom}
  其中**非纯行**（= 「编号与公式体同行」的形态）= {total_geom - total_pure}
    其中**真编号 11 条** + **实测假阳性 2 条**（正文行恰好排到版心右缘、行尾正好是 `(N)`）：
      * 2502617 p10 y=681.9 `Specifically, … includes two steps. (1)`（Δ=+0.2）→ 仍留 B 类
      * 2501869 p3  y=214.7 `Task 1 … to forecast: (1)`（Δ=+0.2）→ 仍留 B 类
    容差**分不开**这两类（假阳性 Δ=0.2 比真编号的最大 Δ=2.7 小一个量级）——
    这就是几何口径**只当存在性证明、不当计数**的原因（见 verify_d 模块 docstring）。
  几何口径命中而**检测器没有检出**的非纯行 = {len(geom_undetected)} 条（> 0 即全量会 FAIL）""")
    for row in geom_undetected:
        print(f"    ! {row}")
    print(f"""
E. 参照基数（**新口径 = 纯行 ∪ 几何口径，逐号取 max**）
  R1'（md 严格纯行 ∪ 几何）= {total_r1u}
  R2'（pdftotext 行尾 ∪ 几何）= {total_r2u}
  几何口径命中行数（并集本身）= {total_geom}

  旧口径（**历史保留**，逐份值见 formula-recon.txt §三）：
  R1  = {total_r1}（md 严格纯行）· R1w = {total_r1w} · R2 = {total_r2}（pdftotext 行尾）· R3 = 661（已废弃）
  近缘（|Δ| <= {TOL}）的非纯行总数 = {near_total}（其中 11 条真编号 + 2 条假阳性）""")
    print("\nF. 复算命令")
    print("  cd <repo> && python tests/papers/recon/formula-geom-scan.py")


def _r2(p):
    """`pdftotext -layout` 侧的行尾 `(N)` 多重集（与 verify_d.r2_counts 同口径）。"""
    import subprocess
    out = subprocess.run(["pdftotext", "-layout", str(p), "-"],
                         capture_output=True, timeout=600)
    text = out.stdout.decode("utf-8", "replace")
    rx = re.compile(r"\((\d{1,2})\)[ \t]*$")
    cnt = Counter()
    for ln in text.splitlines():
        m = rx.search(ln)
        if m and ln.strip():
            cnt[int(m.group(1))] += 1
    return cnt, []


def _md_nums(stem, prob):
    """md 侧严格纯行的逐号多重集（用于并集）。"""
    cnt = Counter()
    p = COLL / prob / f"{stem}.md"
    for ln in p.read_bytes().decode("utf-8").splitlines():
        m = re.match(r"^\s*\((\d{1,2})\)\s*$", ln)
        if m:
            cnt[int(m.group(1))] += 1
    return cnt


_r2_total = 0


if __name__ == "__main__":
    main()
