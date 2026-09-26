# M6 前置流水线（试点）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 2025 年 43 份 O 奖论文从原始 PDF 变成去水印的清洗版 + 可检索正文 md + 图表 PNG + 公式裁图，并产出带稳定 ID 的 `INDEX.md` 与三层 `TAGS.md`。

**Architecture:** 六个阶段各自一个独立模块（`watermark` / `textmd` / `figures` / `formulas` / `index`），共用一个字节级 IO 与路径映射层（`papers.io`）。每个阶段配一个**独立校验脚本**，把判据的逐字原文写进 `tests/papers/reports/`。校验脚本只读派生物与原件，不参与生产。

**Tech Stack:** Python 3.11.9 · PyMuPDF 1.27.2（PDF 解析）· `pdftotext`（poppler，作为 B1 的**独立第二引擎**）· 标准库 `re`/`json`/`pathlib`

## Global Constraints

以下为 spec 的项目级硬约束，**每个任务的要求都隐含包含本节**。

- 仓库 `core.autocrlf = true`。凡 `corpus/papers/` 下的产物，写入一律**字节级**（`Path.write_bytes` / `open(..., "wb")`），**禁止** `write_text` / 文本模式。根级 `.gitattributes` 须含 `corpus/papers/**   -text`。
- **原件 `corpus/历届优秀论文/` 原地不动**，任何阶段不得写入、移动或删除原件。**去水印只在内存中做，不产出清洗版 PDF**（spec §4.1）。
- **不入库的大体积派生物**：`corpus/papers/figures/` 与 `corpus/papers/formulas/`（实测 43 篇约 302 MB，全量约 1.4 GB）。它们可由 `python -m tools.papers.cli all` 确定性重生成，故写进根级 `.gitignore`。入库的是：md、INDEX.md、TAGS.md、PROVENANCE.md、`tests/papers/reports/`。
- **A1 判据要求流水线全程不改动原件**：跑之前记下全部原件的 sha256，跑完复核。这比"保证没写"强——把承诺变成可验证的事实。
- **公式一律不转 LaTeX**，不引入任何 OCR 模型。公式只做裁图 + 编号/引述句抽取。
- **32 份扫描件（UMAP 合集）本轮不碰**。试点只处理 `2025美赛O奖论文` 的 43 份。
- 判据阈值：C2 非白像素占比 `< 0.5%` 判为空图；B1 字符数差异 `> 2%` 须逐篇登记解释；A4 每篇抽 2 页（首页 + 任一含图页）做视觉比对。
- **判据证据须写进受版本控制的 `tests/papers/reports/`，逐字原文**，不得只写汇总描述（教训通则 7）。`.superpowers/` 是 git 忽略的暂存区——**证据放那里等于丢失**。
- **所有校验报告一律 `write_bytes` + LF 书写，且只写仓库相对路径**（不写 `D:\Projects\...`）。报告是逐字证据，必须与运行时产物逐字节一致，且换台机器重跑不产生假 diff。`tests/papers/reports/**` 已标 `-text`。
- **校验脚本的报告写入必须放在 `finally` 或等价保护内**：脚本崩溃时不得把上一次的 `RESULT: PASS` 留在库里冒充本次结论（与"判据不得空过"同类）。
- **凡声称某判据能抓住某类错误，须先确认它真的能**——`write_bytes`/`read_bytes` 绕过 git，抓不到行尾转换。**过度声称已验证是本项目的核心雷区。**
- **凡新增判据，必须用一次变异证明它真的会红**：改坏被测代码 → 跑一次 → 看它红不红。**改不红就是假判据。**
  本项目已出现**四次**「判据在什么都没验的情况下报绿」。在第三次之后立了"写出失败条件"这条要求，
  **仍拦不住第四次**——因为判据可以**看起来**可失败，实则被自己的前置筛选所蕴含。
  实例（Task 2）：`n_strip > 0` 在"按 `xrefs` 非空筛出的样本集"上恒真；它声称会抓的
  "水印形态不同 → `find_watermark_xrefs` 返回空"那种情况，会让样本**被排除出集合**而非失败——
  **判据声称的失败条件它根本做不到。**
  变异测试在 Task 2 修复轮已被证明有效（M1 令 `strip_in_memory` 空转 → 三闸门同时红；
  M2 放宽水印标记 → 12 份对照件掉正文被打印出来）。**只写"我认为它会因 X 失败"不算数。**

- **变异演示与发布校验是两件事，用不同样本量**（2026-09-23 加，因 Task 3 修复轮单次跑 85 分钟）：
  - **变异演示**：目的是证明判据**能**失败。跑 **2–3 份论文**即可——变异效果的机制与样本量无关。
    故每个校验脚本**必须提供 `--limit N`**（默认全量），变异演示一律 `--limit 3`。
  - **发布校验**：目的是**认证语料**。必须全量跑一次，作为该阶段的放行依据。
  - **限样本运行不得写入放行证据的路径**（2026-09-24 加）。代价实例：`verify_b.py --limit 3`
    会把**只跑 5 份**的报告覆写到 43 份全量的放行证据 `tests/papers/reports/b-report.txt` 上，
    差点被提交（靠 `git checkout` 才还原）。**验收判据：跑完一次 `--limit 3` 后，该文件的
    sha256 必须一字不变**；限样本产物写进 git 忽略的位置。**Task 4–7 每个脚本都要照此办**——
    否则这个"限样本绿覆盖全量证据"的机制会被复制四次。
  - **落点判据必须双向，且报告里关于落点的每一句文案都要按实际落点分支**（2026-09-24 加，Task 3 第五轮复审）。
    **双向**：限样本**不得**写放行证据（正向）+ 全量**必须**写放行证据（反向）——少任一方向，
    坏掉的落点逻辑都能给出"绿"（Task 3 实测：只补正向时，把 `report_path` 的 `limit==0` 分支改坏
    可让全量跑静默写进 `reports-limited/` 且 `RESULT: PASS`、无 LIMITED 后缀、退出码 0，**完全无红**）。
    **文案**：报告开头"本文件是限样本跑的……不入库、不是放行依据"属**交付物的一部分**；
    在"调用点被绕开"的配置下它会写进放行证据本体、与事实相反——**同一 `if/elif/else` 下的每一句都要
    按实际落点分支**，不得只改一处（Task 3 已出现"只改一个方向、漏掉 40 行后同块的半句"）。
  - **同一语义必须用同一个谓词**（2026-09-24 加，Task 3 第七轮复审）。代价实例：落点判据在 8 处按
    `limit > 0` 分辨，**两条反向守卫**却写成 `limit == 0`；而 `--limit` 是自由 `int`、
    `pick_sample` 把 `limit <= 0` 当全量跑——于是 `--limit -3` **是一次全量跑但不是 `== 0`**，
    两条反向守卫**静默不触发**，上一轮刚修掉的缺陷**从一个单 token 的旁路原地复活**
    （实测：`RESULT: PASS`、无 LIMITED 后缀、退出码 0、放行证据留着旧 PASS）。
    **Task 4–7 的 `--limit` 一律：要么在 argparse 拒负数，要么全文件统一按 `<= 0` 判**，
    不得两种谓词混用。**并且**：一个被登记为"Minor／语义可辩护"的歧义，可能在下一轮修复里
    变成绕过通道——**修守卫时要顺带把该类歧义收口，而不是等它长大**。
  - **代价实例**：Task 3 修复轮要求演示 4 条判据，每条都跑全量 43 份 × 约 7 分钟，
    **纯计算约 30 分钟，agent 墙钟 85 分钟**。而变异演示本该是秒级。
  - **这一条会随任务放大**：Task 4 要渲染约 860 张 PNG、Task 5 要检测公式区域，
    单次全量校验只会更慢；**Task 7 的 `verify_all.py` 会依次跑完所有校验脚本，
    单次可能 40 分钟以上**——那一次是值得的（它是最终闸门），但中间不该反复付。
- **单样本观察不得写成通则。** 凡"某特征唯一/恒定/总是"的断言，必须在**全语料**上量过才可写进设计。
  代价实例：spec 曾写「水印 span 特征唯一：`MicrosoftYaHei` 72pt」——那是从**一份**论文得出的，
  实测全 201 份有 **三种**字体（`KaiTi`/`SimHei`/`MicrosoftYaHei`），字体启发式只覆盖 **43/120**，
  会静默漏掉 77 份。**试点的 43 份恰好全在命中范围内，所以试点会绿着通过、全量才炸。**
- **不能依赖"会随输入变化的特征"做判据，优先用结构性的。** 同一件事，认字体名会随厂商更换而失效；
  认"XObject 的流是否为空"不会——流空了就画不出东西，与字体无关。
- **判据必须 fail-closed**：拿不到参照（目录不存在、结果为空）时**抛错，不得返回空结果静默通过**。两个空集合相等会让判据"零依据报绿"。
- **"不适用"必须区分两种情形**：参照**不存在**（记为不适用，不计入通过）vs 参照**存在但没解析出来**（**硬失败**）。
  代价实例：B2 把"找到 Contents 页但解析出 0 条"与"根本没有 Contents 页"用同一个 `if toc_entries:` 分支吞掉，
  **等于把一份存在的参照静默丢掉**——与 fail-closed 正好相反。实测该口径把适用面从 41/43 压到 13/43。
- **作用于交付物的判据必须是双边等式，不得是宽松单边下界。**
  代价实例：md 内容判据曾写作 `md_nons >= own_raw`，最大松量 1,315 字符（正文 2.5%）——
  **静默丢掉一整段正文仍会通过**。标记数是可记账的，应当写成等式。
- **失败路径写进证据的内容同样受"无绝对路径"约束**：`traceback.format_exc()` 含
  `File "D:\..."`，崩溃时才违反——**恰好在看门狗触发的那一刻破约束**，平时看不出来。
- **证据文件陈述的"语料事实"必须实测过。** 代价实例：B2 的证据文件称"30 份论文没有
  Contents 页"，独立实测 43 份中 **42 份都有**。**证据文件里一句不成立的语料断言，
  比没有这句话更坏**——它以权威口吻把一个假事实写进了库。
- **不得依赖 git 的二进制自动检测**（教训通则 9：曾误判上游代码，实为搬运环节写坏）。
- 水印厂商字表（用于 A2）：`校苑数模`、`校苑数模公众号`、`英伽教育`。
- 开新模块前必读 `docs/mcm-suite-lessons.md` 的 9 条通则与 7 条流程教训，写进派发指令。

## 派发指令必带（每次派 subagent 都要附）

> 1. `[官方]` 标记只用于官方原文确实如此表述的断言；自订阈值/取舍一律标 `[社区]`。
> 2. 本机**已有 TeX 工具链**（2026-09-24 装：TeX Live 2026，`D:\Software\texlive\2026\bin\windows`；`pdflatex`/`xelatex`/`latexmk` 齐）。
>    故**不得再以"本机无法编译"为由跳过验证**——凡声称编译结果，必须附真实命令与输出。
>    但用户**赛中仍以网页端编译器为准**，所以**不要**写出让用户依赖本机编译的步骤。
> 3. 验证证据须归档进 `tests/papers/reports/`，**逐字原文**。
> 4. 搬动/转换任何文件时，**先排除搬运环节**，再去解释"上游数据差"。转码一律字节级读写。
> 5. **实跑只能证明"不崩"，证明不了"算得对"。** 每个判据都要能说清"参照是什么、它为什么独立"。
> 6. 派 RED 基线的 subagent 只收场景正文，不得带简报或期望答案；隔离须**实测**，不得由 flag 推断。
> 7. 修复不是单调改进，每轮都可能引入新错——**复审不能省**。

## 实测基线（2026-09-23，供实现者校准）

| 事实 | 值 | 来源 |
| :--- | :--- | :--- |
| 2025 论文份数 | 43 | `tests/papers/recon/watermark-scan.json` |
| 全 43 份图注数 | 597 | `build/recon_probe.py` |
| 全 43 份表注数 | 212 | 同上 |
| 全 43 份 `Eq. (N)` 显式引用 | 38 | 同上 |
| 正文字号 | 12.0pt（绝对多数） | 同上 |
| 图注字号 | 10.0–10.9pt | 同上 |
| 标题字号 | 14.0–14.4pt | 同上 |
| 水印对象 | 每份 1 个，全页共用 | `scan_watermarks.py` |

---

## 文件结构

| 文件 | 职责 |
| :--- | :--- |
| `tools/papers/__init__.py` | 包标记，导出公共接口 |
| `tools/papers/io.py` | 路径映射、稳定 ID 生成、原件哈希、字节级读写 |
| `tools/papers/watermark.py` | 水印处理：**内存置空 XObject 流**（三条路径共用，不落盘） |
| `tools/papers/textmd.py` | 正文 → md |
| `tools/papers/figures.py` | 图表抽取 |
| `tools/papers/formulas.py` | 公式裁图 + 编号/引述句 |
| `tools/papers/index.py` | INDEX.md + TAGS.md |
| `tools/papers/vocab.py` | 受控词表加载与字面匹配 |
| `tools/papers/vocab/models.txt` | 受控词表数据（模型/方法名，一行一个） |
| `tools/papers/cli.py` | 统一入口 `python -m tools.papers.cli <stage>` |
| `tests/papers/verify_wm.py` | 水印模块判据 + A1 基线记录 |
| `tests/papers/verify_b.py` | A2/A3（正文侧）+ B1/B2 判据 |
| `tests/papers/verify_c.py` | C1–C4 判据（C4 = 图表无水印） |
| `tests/papers/verify_d.py` | D1–D2 判据 |
| `tests/papers/verify_ids.py` | 稳定 ID 双向解析 |
| `tests/papers/reports/` | 判据逐字原文报告（受版本控制） |

**边界说明**：`io.py` 是唯一知道"原件在哪、派生物该去哪"的模块；各阶段模块只接收输入路径、返回结果对象，不自己拼路径。这样路径映射改动只影响一处。

---

### Task 1: 骨架、字节级 IO 与换行符闸门

**Files:**
- Create: `tools/papers/__init__.py`
- Create: `tools/papers/io.py`
- Create: `tests/papers/verify_io.py`
- Modify: `.gitattributes`（追加一行）

**Interfaces:**
- Consumes: 无（起始任务）
- Produces:
  - `io.REPO: Path` — 仓库根
  - `io.ORIGIN: Path` — 原件根 `corpus/历届优秀论文`
  - `io.DERIVED: Path` — 派生物根 `corpus/papers`
  - `io.stable_id(collection: str, problem: str, seq: int) -> str`
  - `io.parse_stable_id(sid: str) -> tuple[str, str, int]` — `stable_id` 的逆运算
  - `io.md_path(collection: str, problem: str, stem: str) -> Path`
  - `io.figures_dir(collection: str, problem: str, stem: str) -> Path`
  - `io.formulas_dir(collection: str, problem: str, stem: str) -> Path`
  - `io.sha256_tree(collection: str) -> dict[str, str]` — 原件哈希表，供 A1 用
  - `io.problem_of(rel: str) -> str`
  - `io.write_bytes_checked(path: Path, data: bytes) -> None`

- [ ] **Step 1: 写失败的校验脚本**

创建 `tests/papers/verify_io.py`：

```python
"""校验 io 层的路径映射、稳定 ID 与字节级写入。"""
import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tools.papers import io  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "io-report.txt"


def _run() -> tuple[list[str], bool]:
    lines = []
    ok = True

    # 1. 原件根存在，派生物根可建
    lines.append(f"ORIGIN={io.ORIGIN} exists={io.ORIGIN.is_dir()}")
    ok &= io.ORIGIN.is_dir()

    # 2. 稳定 ID 与路径可双向解析
    sid = io.stable_id("2025美赛O奖论文", "A", 1)
    lines.append(f"stable_id('2025美赛O奖论文','A',1) = {sid!r}")
    ok &= sid == "P2025-A-01"

    got = io.parse_stable_id(sid)
    lines.append(f"parse_stable_id({sid!r}) = {got!r}")
    ok &= got == ("2025", "A", 1)

    # 3. 路径映射：题号从路径取，合集由调用方传
    src = "corpus/历届优秀论文/2025美赛O奖论文/A/2500836.pdf"
    prob = io.problem_of(src)
    lines.append(f"problem_of({src!r}) = {prob!r}")
    ok &= prob == "A"

    # 2023 合集的题目录下还有一层中文长名，题号上一层不是合集——
    # 这正是 problem_of 只返回题号、要求合集显式传入的原因
    deep = "2023美赛O奖论文/2023年美国大学生数学建模竞赛（常规赛）O奖论文/A/x.pdf"
    lines.append(f"problem_of(深层路径) = {io.problem_of(deep)!r}")
    ok &= io.problem_of(deep) == "A"

    md = io.md_path("2025美赛O奖论文", prob, "2500836")
    fdir = io.figures_dir("2025美赛O奖论文", prob, "2500836")
    qdir = io.formulas_dir("2025美赛O奖论文", prob, "2500836")
    lines.append(f"md_path   = {md}")
    lines.append(f"figures   = {fdir}")
    lines.append(f"formulas  = {qdir}")
    ok &= str(md).replace("\\", "/").endswith(
        "corpus/papers/md/2025美赛O奖论文/A/2500836.md"
    )
    ok &= "clean" not in str(md) and "clean" not in str(fdir)

    # 4. 原件哈希表：A1 判据的基础，必须非空且可复现
    h1 = io.sha256_tree("2025美赛O奖论文")
    h2 = io.sha256_tree("2025美赛O奖论文")
    lines.append(f"sha256_tree: {len(h1)} 份；两次调用一致={h1 == h2}")
    ok &= len(h1) == 43 and h1 == h2

    # 4b. **fail-closed 判据**：合集名写错必须抛错，不得返回空表。
    #     返回空表会让 A1（两张表比对）在零个哈希的情况下报绿。
    #     磁盘上的真实目录名是 `2023年美赛O奖论文`（带「年」），别处通用的是
    #     `2023美赛O奖论文`——正好差一个字，是现成的触发条件。
    try:
        io.sha256_tree("2023美赛O奖论文")
        lines.append("sha256_tree(错误合集名) 未抛错  <-- FAIL: 判据可空过")
        ok = False
    except FileNotFoundError as e:
        lines.append(f"sha256_tree(错误合集名) 抛 FileNotFoundError ✓ ({e})")

    # 4c. 目录在但没有 PDF，同样必须拒绝（否则又是空表）
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        saved = io.ORIGIN
        io.ORIGIN = Path(td)
        try:
            io.sha256_tree("空合集")
            lines.append("sha256_tree(无 PDF 的合集) 未抛错  <-- FAIL")
            ok = False
        except ValueError as e:
            lines.append(f"sha256_tree(无 PDF 的合集) 抛 ValueError ✓ ({e})")
        finally:
            io.ORIGIN = saved   # 原件树只读，测试用临时目录替换后立刻还原

    # 5. 字节级写入：内容必须逐字节相同（防 autocrlf 类事故）
    probe = io.DERIVED / "_probe" / "bytes.bin"
    payload = b"line1\nline2\r\nline3\r\r\n\x00\xff binary tail"
    io.write_bytes_checked(probe, payload)
    back = probe.read_bytes()
    lines.append(f"write_bytes_checked roundtrip identical={back == payload}")
    ok &= back == payload
    probe.unlink()
    probe.parent.rmdir()

    return lines, ok


def main() -> int:
    """报告写入受 finally 保护。

    若脚本在半途抛错（`stable_id`/`parse_stable_id`/`problem_of` 都是
    **设计上会抛错**的），不加保护就会死在写报告之前——而库里那份**已提交**的
    报告会继续保持 `RESULT: PASS`，`git status` 也看不出任何差异。
    那样一次真实回归会留下一份绿色的假证据。
    """
    lines, ok, err = [], False, None
    try:
        lines, ok = _run()
    except Exception:
        err = traceback.format_exc()
        ok = False
    if err:
        lines = lines + ["", "脚本抛异常:", err]
    lines.append("RESULT: " + ("PASS" if ok else "FAIL"))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    # 字节级 + LF：报告是逐字证据，必须与运行时产物逐字节一致。
    # 只写仓库相对路径，换台机器重跑不产生假 diff。
    REPORT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行校验，确认它失败**

Run: `python tests/papers/verify_io.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers'`

- [ ] **Step 3: 实现 io 层**

创建 `tools/papers/__init__.py`（空文件即可）：

```python
"""美赛获奖论文语料流水线。"""
```

创建 `tools/papers/io.py`：

```python
"""路径映射、稳定 ID 与字节级读写。

本模块是唯一知道"原件在哪、派生物该去哪"的地方。各阶段模块只接收
显式路径，不自己拼路径。
"""
import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ORIGIN = REPO / "corpus" / "历届优秀论文"
DERIVED = REPO / "corpus" / "papers"

# 稳定 ID：P<年份>-<题号>-<序号>，序号为该题号下的到达顺序（1 起）
# 内容无关，故条号重排不会改变已发 ID——这正是教训三.1 要的。
_ID = re.compile(r"^P(\d{4})-([A-F])-(\d{2,})$")
# 合集名形如 "2025美赛O奖论文"，取开头的 4 位年份
_YEAR = re.compile(r"^(\d{4})")


_PROBLEMS = tuple("ABCDEF")   # 与 problem_of 共用同一语义


def stable_id(collection: str, problem: str, seq: int) -> str:
    """由合集名、题号、序号生成稳定 ID。"""
    m = _YEAR.match(collection)
    if not m:
        raise ValueError(f"合集名不以 4 位年份开头: {collection!r}")
    # 必须比对 tuple 而非字符串：`problem not in "ABCDEF"` 是**子串**测试，
    # 会放过 "AB" 与 ""，而逆函数 parse_stable_id 的正则 ([A-F]) 拒绝它们——
    # 同模块两个函数对同一判据用不同语义，双向不变式就断了。
    if problem not in _PROBLEMS:
        raise ValueError(f"题号须为 A-F 单字母: {problem!r}")
    return f"P{m.group(1)}-{problem}-{seq:02d}"


def parse_stable_id(sid: str) -> tuple[str, str, int]:
    """stable_id 的逆运算，供双向解析校验用。"""
    m = _ID.match(sid)
    if not m:
        raise ValueError(f"不是合法稳定 ID: {sid!r}")
    return m.group(1), m.group(2), int(m.group(3))


def problem_of(rel: str) -> str:
    """从路径中取出 A-F 题号层。

    刻意**只返回题号、不返回合集**：合集名由调用方显式传入。
    曾试图从路径反推合集，但 2023 合集的布局是
    `2023美赛O奖论文/<中文长名>/A/xxx.pdf`，题号的上一层是子目录而非
    合集，反推会静默取错。显式传入消除这一整类歧义。
    """
    parts = [p for p in Path(rel).parts if p not in (".", "..")]
    for p in parts:
        if p in _PROBLEMS:
            return p
    raise ValueError(f"路径中找不到 A-F 题号层: {rel!r}")


def sha256_tree(collection: str) -> dict[str, str]:
    """记录某合集下全部原件的 sha256，供 A1 判据前后比对。

    这是"原件未被改动"从承诺变成事实的关键：流水线跑之前存一份，
    跑完再存一份，两份必须逐字相同。

    **必须 fail-closed。** `Path.rglob` 对不存在的目录返回空列表、不抛错，
    于是"合集名写错"会得到 `{}`；而 A1 是两张表比对，两个空表相等——
    **判据会在零个哈希的情况下报绿**。这不是假想：磁盘上的真实目录名是
    `2023年美赛O奖论文`（带「年」），而与代码别处通用的 `2023美赛O奖论文`
    正好差一个字。
    """
    root = ORIGIN / collection
    if not root.is_dir():
        raise FileNotFoundError(f"合集目录不存在: {root}")
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*.pdf")):
        out[str(p.relative_to(ORIGIN))] = hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
    if not out:
        raise ValueError(f"合集 {collection!r} 下没有 PDF，拒绝返回空哈希表")
    return out


def md_path(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "md" / collection / problem / f"{stem}.md"


def figures_dir(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "figures" / collection / problem / stem


def formulas_dir(collection: str, problem: str, stem: str) -> Path:
    return DERIVED / "formulas" / collection / problem / stem


def write_bytes_checked(path: Path, data: bytes) -> None:
    """字节级写入并回读校验。

    **这个回读能抓什么、不能抓什么，要说清**：`write_bytes` 与 `read_bytes`
    都绕过 git，所以它**抓不到行尾转换**——通则 9 的 `\\r\\r\\n` 事故不可能
    在这条路径上发生。它能抓的是文件系统层面的干扰（部分写入、磁盘满、
    同名并发写入、非字节安全的写入实现）。
    真正能抓行尾转换的是 **git 索引/blob 往返**，那由
    `tests/papers/reports/gitattributes-gate.txt` 里的对照探针负责。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    if path.read_bytes() != data:
        raise IOError(f"写入回读不一致（文件系统层面，非行尾转换）：{path}")
```

- [ ] **Step 4: 运行校验，确认通过**

Run: `python tests/papers/verify_io.py`
Expected: `RESULT: PASS`，且 `tests/papers/reports/io-report.txt` 内容与终端输出一致。

- [ ] **Step 5: 加换行符闸门**

在根级 `.gitattributes` **追加**（保留既有 `corpus/algorithms/` 两行不动）：

```
corpus/papers/**             -text
tests/papers/reports/**      -text
tests/papers/recon/**        -text
```

`tests/papers/reports/** -text` 与 `tests/papers/recon/** -text` 是**修复轮次补上的**：证据文书此前落盘 CRLF、入库 LF，不是逐字节一致；加 `-text` 后存什么取什么。

- [ ] **Step 6: 建 `.gitignore`，排除可重生成的大体积派生物**

仓库根目录当前**没有 `.gitignore`**。新建：

```gitignore
# M6 语料流水线：以下产物可由 `python -m tools.papers.cli all` 确定性重生成，
# 且体积大（实测 43 篇约 302 MB，全量约 1.4 GB），故不入库。
# 入库的是抽取出的文本、索引与判据证据。
corpus/papers/figures/
corpus/papers/formulas/
build/
__pycache__/
```

- [ ] **Step 7: 验证闸门生效，并把证据写进受版本控制的文件**

Run:
```bash
git check-attr -a corpus/papers/md/x.md corpus/papers/figures/x/y.png
git check-ignore -v corpus/papers/figures/a.png corpus/papers/formulas/b.png
```
Expected: `check-attr` 两条都输出 `text: unset`；`check-ignore` 两条都命中 `.gitignore`。若任一未生效，**停下修正**。

**再做一次能真正失败的对照**（只跑 `check-attr` 是"证明我设了开关"，不是"证明开关有用"）：

```bash
# 同一份纯文本字节，两条路径各走一遍 git add → blob → checkout
printf 'a\r\nb\nc\r\n' > /tmp/ctrl.md
# 受保护路径 vs 未受保护路径，比对 checkout 回来的字节
```

把**原始命令输出**连同上面的对照结果写进 `tests/papers/reports/gitattributes-gate.txt`。

> **探针内容的选择有讲究**（修复轮发现的）：若探针里含**裸 CR**（如 `\r\r\n`），
> git 会把它判为二进制（`i/-text`），**无论有没有闸门都会原样保留**——那样的探针
> 是自证的，证明不了闸门起作用。**要能让闸门失效时探针也失败，必须用纯文本内容**
> （只有 CRLF/LF）。上面这条对照就是为此而设。
>
> **这条证据必须入库。** Task 1 的头号交付物是换行符闸门，而它的证据此前只写在
> `.superpowers/sdd/` 里——那是 git 忽略目录，**等于丢失**。第一期的 GREEN-1
> 证据就是这么没的。

- [ ] **Step 8: 提交**

```bash
git add .gitattributes .gitignore tools/papers/ tests/papers/verify_io.py tests/papers/reports/
git commit -m "feat(papers): io 层、换行符闸门与忽略规则——路径映射、稳定 ID、原件哈希"
```

> 提交前确认 `git status` 里没有 `__pycache__/` 或 `build/`——两者都已在 `.gitignore` 中。

---

### Task 2: 水印处理模块 + A1 基线

本任务只做**水印处理本身**，并**在任何流水线代码碰 PDF 之前**记下原件哈希基线。
正文侧的 A2/A3 判据放在 Task 3（那时才有 md 可验），图表侧的判据放在 Task 4。

**Files:**
- Create: `tools/papers/watermark.py`
- Create: `tests/papers/verify_wm.py`
- Create: `tests/papers/reports/origin-sha256-2025.txt`（基线，**库龄起点**）

**Interfaces:**
- Consumes: `io.ORIGIN`, `io.REPO`, `io.problem_of`, `io.sha256_tree`
- Produces:
  - `watermark.WM_WORDS: list[str]` — 三个已知厂商字串，供 A2/A3 判定
  - `watermark.find_watermark_xrefs(doc: fitz.Document) -> list[int]`
  - `watermark.strip_in_memory(doc: fitz.Document) -> int`
  - `watermark.content_text(doc: fitz.Document) -> str` — **置空水印流后**的全文（供 A2/A3 与正文抽取复用）
  - `watermark.spans(doc: fitz.Document) -> list[str]` — 逐 span 取文本，供 A3 的差集比对

> **不使用字体/字号启发式。** 初版有 `is_watermark_span(font, size)`，实测只覆盖 43/120
> （2023/2024 的水印是 `KaiTi`/`SimHei`），已整体废弃。详见 spec §4.1.1。

- [ ] **Step 1: 先记原件哈希基线（在做任何事之前）**

```bash
python -c "
import sys; sys.path.insert(0, '.')
from pathlib import Path
from tools.papers import io
import json
h = io.sha256_tree('2025美赛O奖论文')
out = Path('tests/papers/reports/origin-sha256-2025.txt')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(('\n'.join(f'{v}  {k}' for k, v in sorted(h.items())) + '\n').encode('utf-8'))
print(f'基线已记录 {len(h)} 份 -> {out}')
"
```
Expected: `基线已记录 43 份 -> tests/papers/reports/origin-sha256-2025.txt`

**基线必须在任何流水线代码运行前记录**，否则它会被污染、失去证明力。若此文件已存在，**不要覆盖**，先核对它与当前原件是否一致。

- [ ] **Step 2: 写失败的校验脚本**

创建 `tests/papers/verify_wm.py`：

```python
"""水印处理模块的单元级校验。

不依赖 md 或图表产物——本任务只验"水印处理本身做对了"。
A2/A3（正文侧）在 Task 3 验，图表侧在 Task 4 验。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import fitz  # noqa: E402
from tools.papers import io, watermark  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "wm-report.txt"
WM_WORDS = ["校苑数模公众号", "校苑数模", "英伽教育"]
SAMPLE = "corpus/历届优秀论文/2025美赛O奖论文/A/2500836.pdf"


def red_ratio(page, zoom=1.0):
    """偏红像素占比——水印是红色 1 0 0 rg。仅作代理指标。"""
    pm = page.get_pixmap(dpi=int(110 * zoom), alpha=False)
    s, n = pm.samples, pm.width * pm.height
    red = 0
    for i in range(0, len(s), 3):
        r, g, b = s[i], s[i + 1], s[i + 2]
        if r > 140 and r - g > 40 and r - b > 40:
            red += 1
    return red / n if n else 0.0


def main() -> int:
    lines = ["水印模块校验", "=" * 72]
    ok = True
    src = io.REPO / SAMPLE

    doc = fitz.open(src)
    xrefs = watermark.find_watermark_xrefs(doc)
    lines.append(f"find_watermark_xrefs = {xrefs}")
    ok &= len(xrefs) == 1

    # 1. 过滤水印后，正文里不含水印字
    raw = "".join(p.get_text() for p in doc)
    lines.append(f"不过滤(基线): 水印字命中 = {[w for w in WM_WORDS if w in raw]}")
    ok &= any(w in raw for w in WM_WORDS)   # 前提：不过滤确实会命中

    filt = watermark.content_text(doc)
    hit = [w for w in WM_WORDS if w in filt]
    lines.append(f"过滤后      : 水印字命中 = {hit or '无'}")
    ok &= not hit

    # 2. 过滤只去掉水印，正文长度不能塌
    lines.append(f"不过滤字数={len(raw)}  过滤后字数={len(filt)}  差={len(raw)-len(filt)}")
    ok &= len(filt) > len(raw) * 0.98

    # 3. A3 fail-closed：被移除的 span 必须**全部**是水印碎片。
    #    这是本任务最关键的一条——stripping 吃掉任何正文都会在此现形。
    doc2 = fitz.open(src)
    before = watermark.spans(doc2)
    watermark.strip_in_memory(doc2)
    after = watermark.spans(doc2)
    doc2.close()
    from collections import Counter
    removed = Counter(before) - Counter(after)
    bad_removed = [t for t in removed if not any(t in w for w in watermark.WM_WORDS)]
    lines.append(f"置空流移除 {sum(removed.values())} 个 span；"
                 f"越界（非水印碎片）={bad_removed or '无'}")
    ok &= bool(removed) and not bad_removed
    lines.append(f"   可失败的输入：若置空流吃掉任何正文，越界列表即非空 → FAIL")

    # 4. 内存去水印后，渲染的偏红像素显著下降
    with_img = None
    for i, p in enumerate(doc):
        if p.get_images(full=True):
            with_img = i
            break
    before = red_ratio(doc[with_img])
    n = watermark.strip_in_memory(doc)
    after = red_ratio(doc[with_img])
    lines.append(f"第{with_img+1}页 偏红像素: 去水印前={before*100:.3f}% 后={after*100:.3f}% "
                 f"（strip_in_memory 处理 {n} 个对象）")
    ok &= after < before * 0.5
    lines.append("注：偏红像素只是代理指标。残余值来自照片本身的暖色（石质/木质），")
    lines.append("    不是水印——结论以人工目视为准（见 Step 5）。")

    # 5. 全程未写回原件
    doc.close()
    lines.append(f"原件 sha256 复核 = {io.sha256_tree('2025美赛O奖论文')[SAMPLE]}")
    lines.append(f"基线首行          = {Path('tests/papers/reports/origin-sha256-2025.txt').read_text('utf-8').splitlines()[0]}")

    lines.append("=" * 72)
    lines.append(f"RESULT: {'PASS' if ok else 'FAIL'}")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 3: 运行校验，确认它失败**

Run: `python tests/papers/verify_wm.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers.watermark'`

- [ ] **Step 4: 实现水印模块**

创建 `tools/papers/watermark.py`：

```python
"""水印处理：**三条路径共用同一个机制**——在内存里置空水印 XObject 的流。

水印形态（2026-09-23 实测，见 tests/papers/recon/）：
  独立 Form XObject，带 /PieceInfo <</ADBE_CompoundType
  <</Private /Watermark>>>> 标记，压在正文与图表之上。

**为什么不用字体/字号启发式**（初版做法，已废弃）：
从单份论文观察到的「水印恒为 MicrosoftYaHei 72pt」被当成了通则，实测全
201 份有**三种**字体——2025 是 MicrosoftYaHei 72pt，2023/2024 是
KaiTi 74.4/76.5pt，2023 另有 SimHei 83.4pt。字体启发式只覆盖 43/120；
而试点的 43 份恰好全在命中范围内，所以**试点会绿着通过、全量才炸**。

置空 XObject 流是**结构性**的：流空了就画不出任何东西，与字体无关。
实测 120/120 命中，81 份无水印件零误伤。
"""
import fitz

WM_WORDS = ["校苑数模公众号", "校苑数模", "英伽教育"]
_WM_MARK = ("/PieceInfo", "/Watermark")


def find_watermark_xrefs(doc: fitz.Document) -> list[int]:
    """返回所有带 PieceInfo/Watermark 标记的 xref。

    必须逐 xref 加 try：这些 PDF 的对象流里有悬空引用，
    xref_object 会对部分 xref 抛 RuntimeError（实测 2025 那批有 9 处）。
    """
    hits = []
    for x in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(x, compressed=True)
        except Exception:
            continue
        if all(m in obj for m in _WM_MARK):
            hits.append(x)
    return hits


def strip_in_memory(doc: fitz.Document) -> int:
    """把水印 XObject 的流置空。**只改内存对象，不保存、不写回任何文件。**

    返回处理的对象数。水印在全部页共用同一 xref，故一次置空即全篇生效。

    返回 0 对本流水线是**异常信号**，不是无事发生：说明这份论文的水印形态
    与已知的不同，下游会静静地带水印。调用方应把 0 当失败处理。
    """
    xrefs = find_watermark_xrefs(doc)
    for x in xrefs:
        doc.update_stream(x, b"")
    return len(xrefs)


def spans(doc: fitz.Document) -> list[str]:
    """逐 span 取文本。供 A3 做差集比对（不拼接、不折叠空白）。"""
    out = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for line in b.get("lines", []):
                for s in line["spans"]:
                    if s["text"].strip():
                        out.append(s["text"])
    return out


def content_text(doc: fitz.Document) -> str:
    """置空水印流后的全文。

    **会就地修改传入的 doc**——调用方若要对照"置空前"的文本，必须
    在调用前先取好（见 verify_wm.py 的 A3 检查）。
    """
    strip_in_memory(doc)
    return "".join(doc[i].get_text() for i in range(doc.page_count))
```

- [ ] **Step 5: 运行校验，确认通过**

Run: `python tests/papers/verify_wm.py`
Expected: `RESULT: PASS`，且：
- `不过滤(基线): 水印字命中 = ['校苑数模公众号', '校苑数模']`（**前提成立**）
- `过滤后      : 水印字命中 = 无`
- `偏红像素: 去水印前=1.8xx% 后=0.4xx%`

- [ ] **Step 6: 人工目视确认**

```bash
python -c "
import sys; sys.path.insert(0,'.')
import fitz
from tools.papers import io, watermark
from pathlib import Path
src = io.REPO / 'corpus/历届优秀论文/2025美赛O奖论文/A/2500836.pdf'
out = Path('tests/papers/reports'); out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(src)
# 含图页
t = next(i for i,p in enumerate(doc) if p.get_images(full=True))
doc[t].get_pixmap(dpi=110).save(str(out / 'a4-2500836-with-wm.png'))
watermark.strip_in_memory(doc)
doc[t].get_pixmap(dpi=110).save(str(out / 'a4-2500836-no-wm.png'))
doc.close()
print('已输出两张对比图，请人工比对')
"
```
**人工打开两张 PNG 比对**：`with-wm` 应见红色「校苑数模公众号」压在照片上，`no-wm` 应完全干净。
把结论写进 `tests/papers/reports/wm-report.txt` 末尾。**未目视确认前不得进 Task 3。**

- [ ] **Step 7: 提交**

```bash
git add tools/papers/watermark.py tests/papers/verify_wm.py tests/papers/reports/
git commit -m "feat(papers): 水印模块（内存过滤，不落盘）+ A1 原件哈希基线"
```

---

### Task 3: 正文抽取 + B1/B2 与 A2/A3 判据

**Files:**
- Create: `tools/papers/textmd.py`
- Create: `tests/papers/verify_b.py`

**Interfaces:**
- Consumes: `io.ORIGIN`（**读原件**——去水印在抽取时内存完成，不读任何清洗版）、`io.md_path`, `io.problem_of`, `watermark.strip_in_memory`, `watermark.spans`, `watermark.WM_WORDS`
- Produces:
  - `textmd.is_heading(size: float, body_size: float) -> bool`
    （**2026-09-24 改签**：原为全局常量 `HEADING_MIN_SIZE = 13.5` 的单参判据，实测对 42/43 成立、
    但 `2522820` 正文 10.9pt／小节 12.0pt 时把小节降级，故改为**逐篇相对**。
    参数为**原始字号**（未取整），判据是 `size >= round(body_raw, 1) + HEADING_DELTA`，
    `HEADING_DELTA = 1.0` 由全 43 份逐篇约束的**交集 (0.9100, 1.0600]** 定，见
    `tests/papers/reports/b2-size-histogram.txt`）
  - `textmd.body_size(doc: fitz.Document) -> float`（该篇基准字号＝承载字符最多的字号；文本层为空时**抛错**）
  - `textmd.is_title(text: str) -> bool`（按**形态**剔除假标题，见 `BULLET_CHARS`）
  - 常量：`HEADING_DELTA`、`BULLET_CHARS`；**`HEADING_MIN_SIZE` 已删除**
  - `textmd.to_markdown(doc: fitz.Document) -> tuple[str, MdResult]`
  - `textmd.extract(src: Path, out_md: Path) -> MdResult`
  - `textmd.MdResult` —— dataclass，字段 `n_headings: int, n_chars: int, n_captions: int`

**关键实测值**：正文 12.0pt、图注 10.0–10.9pt、标题 14.0–14.4pt。标题判据取 `size >= 13.5`。

**判据分工**：B1/B2 验正文抽取质量；**A2/A3 在本任务首次可验**（verifier 里一并做），因为它们要拿 md 与原件文本对照。

- [ ] **Step 1: 写失败的校验脚本**

创建 `tests/papers/verify_b.py`：

```python
"""正文抽取判据 B1/B2 + 正文侧水印判据 A2/A3。

B1 非空且与 pdftotext（另一引擎）字数差 <= 2%
B2 识别出的标题数 >= 论文自己 Contents 页的条目数
A2 产出的 md 里水印字 0 命中
A3 原件文本剔除水印字串后 == md 正文（逐字）
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import fitz  # noqa: E402
from tools.papers import io, textmd, watermark  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "b-report.txt"
WS = re.compile(r"\s+")
WM_WORDS = watermark.WM_WORDS


def pdftotext_len(p: Path) -> int:
    """第二引擎字数。stderr 里的字体告警属预期，不视为失败。"""
    r = subprocess.run(
        ["pdftotext", "-q", str(p), "-"], capture_output=True, timeout=120
    )
    return len(WS.sub("", r.stdout.decode("utf-8", "replace")))


def main() -> int:
    root = io.ORIGIN / "2025美赛O奖论文"
    pdfs = sorted(root.rglob("*.pdf"))
    lines = [f"B 组 + A2/A3 判据 · 试点 {len(pdfs)} 份", "=" * 72]
    bad = []
    for src in pdfs:
        prob = src.parent.name
        md = io.md_path("2025美赛O奖论文", prob, src.stem)
        res = textmd.extract(src, md)

        mdtext = md.read_text("utf-8")

        # A2 产出物里水印字 0 命中
        hit = [w for w in WM_WORDS if w in mdtext]
        a2 = not hit

        # A3 **fail-closed**：被置空流移除的 span 必须**全部**是水印碎片。
        # 只要有一个非水印片段消失，就说明 stripping 吃掉了正文 → FAIL。
        # 2023 那批把水印拆成每页 8 个片段（校/苑/数/模/…），所以必须逐 span
        # 做差集，不能靠整段字符串替换——那种做法多替少替都不易察觉。
        with fitz.open(src) as doc:
            before = watermark.spans(doc)
            watermark.strip_in_memory(doc)
            after = watermark.spans(doc)
            filt = "".join(doc[i].get_text() for i in range(doc.page_count))

        removed = Counter(before) - Counter(after)
        bad_removed = [t for t in removed if not any(t in w for w in WM_WORDS)]
        a3 = not bad_removed

        # B1 与第二引擎对照（用置空后的文本，两边都不含水印）
        own = len(WS.sub("", filt))
        other = pdftotext_len(src)
        diff = abs(own - other) / max(other, 1)
        b1 = diff <= 0.02

        # B2 论文自己的 Contents 页条目数
        with fitz.open(src) as doc:
            toc_entries = 0
            for p in doc:
                t = p.get_text()
                if "Contents" in t:
                    toc_entries = len(re.findall(r"\.{3,}\s*\d+\s*$", t, re.M))
                    break
        # 未检出目录 → 记为"不适用"，**不记为通过**（判据凡"不适用"一律如此处置）
        if toc_entries:
            b2, b2_label = res.n_headings >= toc_entries, str(toc_entries)
        else:
            b2, b2_label = None, "不适用(未检出目录)"

        lines.append(
            f"{src.stem:<10} A2水印字={hit or '无'} "
            f"A3移除{sum(removed.values())}span/越界={bad_removed or '无'} "
            f"B1 我方={own:<7} pdftotext={other:<7} 差={diff*100:5.2f}% "
            f"B2 标题={res.n_headings:<3} 目录={b2_label:<20}"
        )
        if bad_removed:
            lines.append(f"{'':10} ^ A3 FAIL：以下被移除的 span 不是水印碎片 "
                         f"{bad_removed[:5]}")
        if not b1:
            lines.append(f"{'':10} ^ B1 超阈，须解释差异来源（换行/连字符）")
        if not (a2 and a3 and b1) or b2 is False:
            bad.append((src.stem, a2, a3, b1, b2, bad_removed))

    lines.append("=" * 72)
    lines.append(f"A2/A3/B1/B2 全通过: {not bad}")
    if bad:
        lines.append("失败明细（每一条都必须给出解释，不得静默）:")
        for stem, a2, a3, b1, b2, bad_removed in bad:
            lines.append(f"  {stem}: A2={a2} A3={a3} B1={b1} B2={b2} "
                         f"越界移除={bad_removed[:3]}")
    lines.append(f"RESULT: {'PASS' if not bad else 'FAIL'}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行校验，确认它失败**

Run: `python tests/papers/verify_b.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers.textmd'`

- [ ] **Step 3: 实现正文抽取**

创建 `tools/papers/textmd.py`：

```python
"""正文抽取：字形层 → markdown。全程无 OCR、无推断。

水印在抽取时**置空其 XObject 的流**（`watermark.strip_in_memory`），
与图表/公式路径同源。**不用字体/字号启发式**——实测水印字体有三种，
启发式只覆盖 43/120，且试点的 43 份恰在命中范围内，会绿着通过。
详见 spec §4.1.1。

**不读任何清洗版 PDF**——原件是唯一输入，且全程只读。

标题判据取自实测字号分层：正文 12.0pt、图注 10.0-10.9pt、标题 14.0-14.4pt。
取 >= 13.5 为标题阈值，是实测分布之间的空档，不落在任一簇内。
"""
import re
from dataclasses import dataclass
from pathlib import Path

import fitz

from . import watermark

HEADING_MIN_SIZE = 13.5
CAPTION = re.compile(r"^\s*(Figure|Fig\.|Table)\s*\d+\s*[:.]", re.I)


@dataclass
class MdResult:
    n_headings: int
    n_chars: int
    n_captions: int


def is_heading(size: float) -> bool:
    return size >= HEADING_MIN_SIZE


def to_markdown(doc: fitz.Document) -> tuple[str, MdResult]:
    """把文档转成 markdown。

    **调用方必须已经 `strip_in_memory` 过**——本函数不做水印判断，
    因为那需要认字体，而字体判据是错的（见模块 docstring）。
    """
    out: list[str] = []
    n_headings = n_captions = 0

    for pno in range(doc.page_count):
        page = doc[pno]
        out.append(f"\n<!-- page {pno + 1} -->\n")
        for block in page.get_text("dict")["blocks"]:
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
                bold = any("Bold" in s["font"] for s in spans)
                if CAPTION.match(text):
                    n_captions += 1
                    out.append(f"\n*{text.strip()}*\n")
                elif is_heading(size):
                    n_headings += 1
                    out.append(f"\n{'#' * 2} {text.strip()}\n")
                elif bold and len(text.strip()) < 80 and not text.strip().endswith("."):
                    out.append(f"\n**{text.strip()}**\n")
                else:
                    out.append(text)

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body, MdResult(
        n_headings=n_headings,
        n_chars=len(re.sub(r"\s+", "", body)),
        n_captions=n_captions,
    )


def extract(src: Path, out_md: Path) -> MdResult:
    """从**原件**抽正文。原件只读，水印在内存中置空。

    **fail-closed 判据**：若文本层本来就带着水印字，却找不到水印 XObject
    （`strip_in_memory` 返回 0），说明这份论文的水印形态与已知的不同——
    继续下去会把水印字静静写进 md。此时**抛错**，不静默产出。
    反过来，文本层本来没有水印字的（2022 与 UMAP 那 81 份），返回 0 是正常的。
    """
    doc = fitz.open(src)
    try:
        raw = "".join(doc[i].get_text() for i in range(doc.page_count))
        had_wm_text = any(w in raw for w in watermark.WM_WORDS)
        n = watermark.strip_in_memory(doc)
        if had_wm_text and n == 0:
            raise RuntimeError(
                f"文本层带水印字，却找不到水印 XObject（形态未知）: {src.name}"
            )
        body, res = to_markdown(doc)
    finally:
        doc.close()
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_bytes(body.encode("utf-8"))  # 字节级，勿用 write_text
    return res
```

- [ ] **Step 4: 运行校验，确认 A2/A3/B1/B2 通过**

Run: `python tests/papers/verify_b.py`
Expected: `A2/A3/B1/B2 全通过: True`，`RESULT: PASS`。

**失败时的处理纪律**：
- **A3 不一致** → 打印第一处差异的上下文（两个字符串各自的差异位置前后 60 字），看清是滤多了还是滤少了。**不得放宽判据**。
- **B1 超阈** → 逐篇看差异来源写进报告。**不得直接把 2% 调大**——教训二.6：测试失败时默认假设选错方向会把判据越改越松。

- [ ] **Step 5: 提交**

```bash
git add tools/papers/textmd.py tests/papers/verify_b.py tests/papers/reports/b-report.txt corpus/papers/md/
git commit -m "feat(papers): 正文抽取，A2/A3/B1/B2 判据全通过"
```

---

### Task 4: 阶段 3 —— 图表抽取 + C1/C2/C3 判据

**Files:**
- Create: `tools/papers/figures.py`
- Create: `tests/papers/verify_c.py`

**Interfaces:**
- Consumes: `io.ORIGIN`（**读原件**）、`io.figures_dir`, `io.problem_of`, `watermark.strip_in_memory`
- Produces:
  - `figures.caption_blocks(doc) -> list[Caption]`
  - `figures.Caption` —— dataclass，字段 `kind: str, num: int, page: int, y0: float, text: str`
  - `figures.extract_all(src: Path, out_dir: Path, dpi: int = 200) -> FigResult`
  - `figures.FigResult` —— dataclass，字段 `n_fig: int, n_tab: int`

**方法**：按图注定位——找到 `Figure N:` / `Table N:` 文本块，取其**上方**内容区整区渲染。矢量图与位图统一处理，不逐图判断类型（逐图判断会漏）。

**渲染前必须 `strip_in_memory(doc)`**，否则水印会被烤进产出的 PNG。这一步只改内存对象，不写回原件。

- [ ] **Step 1: 写失败的校验脚本**

创建 `tests/papers/verify_c.py`：

```python
"""图表判据 C1-C4。

C1 图注计数 = 产出图片数，差额为 0（非 0 须逐条登记解释）
C2 非白像素占比 >= 0.5%，否则判空图
C3 每张图配 .caption.txt
C4 产出图不含水印（偏红像素代理指标 + 人工目视抽查）
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import fitz  # noqa: E402
from PIL import Image  # noqa: E402
from tools.papers import figures, io, watermark  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "c-report.txt"
CAP = re.compile(r"^\s*(Figure|Fig\.|Table)\s*(\d+)\s*[:.]", re.I)


def red_ratio(png: Path) -> float:
    """偏红像素占比——水印是红色 1 0 0 rg。仅作代理指标。"""
    im = Image.open(png).convert("RGB")
    px = im.getdata()
    n = im.width * im.height
    red = sum(1 for r, g, b in px if r > 140 and r - g > 40 and r - b > 40)
    return red / n if n else 0.0


def main() -> int:
    root = io.ORIGIN / "2025美赛O奖论文"
    pdfs = sorted(root.rglob("*.pdf"))
    lines = [f"C 组判据 · 试点 {len(pdfs)} 份", "=" * 72]
    bad = []
    for src in pdfs:
        prob = src.parent.name
        out = io.figures_dir("2025美赛O奖论文", prob, src.stem)
        res = figures.extract_all(src, out)

        doc = fitz.open(src)
        expected = sum(
            1
            for p in doc
            for b in p.get_text("dict")["blocks"] if b.get("type") == 0
            for l in b.get("lines", [])
            if CAP.match("".join(s["text"] for s in l["spans"]))
        )
        doc.close()

        produced = sorted(out.glob("*.png")) if out.is_dir() else []
        # C1：只比图（Figure），表单独统计
        figs = [p for p in produced if p.name.startswith("fig-")]
        c1 = abs(len(figs) - res.n_fig) == 0

        blank = []
        ratios = []
        for p in produced:
            im = Image.open(p).convert("L")
            hist = im.histogram()
            nonwhite = sum(hist[:245])          # 灰度 < 245 计为非白
            total = im.width * im.height
            ratio = nonwhite / total if total else 0.0
            ratios.append(ratio)
            if ratio < 0.005:
                blank.append(f"{p.name}({ratio*100:.2f}%)")
        c2 = not blank
        min_ratio = min(ratios) if ratios else float("nan")

        c3 = all((p.with_suffix(".caption.txt")).exists() for p in produced)

        # C4 产出图无水印。分两层：
        #   (a) 结构化——权威证据：strip 后所有水印 XObject 的流长必须为 0。
        #       这是确定性的：流为空则画不出任何东西。同时要求带水印的论文
        #       strip 返回 > 0，否则说明 find_watermark_xrefs 漏掉了它
        #       （水印形态变了），产出图会静静地带水印。
        #   (b) 像素代理——只用来筛出可疑页送人工，**不单独作为结论**。
        with fitz.open(src) as doc:
            n_marked = len(watermark.find_watermark_xrefs(doc))
            n_stripped = watermark.strip_in_memory(doc)
            leftover = []
            for x in range(1, doc.xref_length()):
                try:
                    o = doc.xref_object(x, compressed=True)
                except Exception:
                    continue
                if "/PieceInfo" in o and "/Watermark" in o:
                    if len(doc.xref_stream(x) or b"") > 0:
                        leftover.append(x)
        c4_struct = (n_stripped > 0 and not leftover) if n_marked else (not leftover)

        by_size = sorted(produced, key=lambda p: p.stat().st_size, reverse=True)[:3]
        reds = [(p.name, red_ratio(p)) for p in by_size]
        suspicious = [(n, r) for n, r in reds if r >= 0.01]

        lines.append(
            f"{src.stem:<10} C1 期望图注={res.n_fig:<3} 产出图={len(figs):<3} "
            f"（全图注含表={expected}）C2 最小非白={min_ratio*100:5.2f}% 空图={blank or '无'} "
            f"C3 图注文件={'齐' if c3 else '缺'}"
        )
        lines.append(
            f"{'':10} C4 水印对象={n_marked} strip={n_stripped} 残留流长>0={leftover or '无'} "
            f"| 抽最大3张偏红: "
            + " ".join(f"{n}={r*100:.2f}%" for n, r in reds)
            + (f"  <- 待人工确认 {[n for n,_ in suspicious]}" if suspicious else "")
        )
        if not (c1 and c2 and c3 and c4_struct):
            bad.append((src.stem, c1, c2, c3, c4_struct, blank, leftover))

    lines.append("=" * 72)
    lines.append(f"C1/C2/C3/C4 全通过: {not bad}")
    if bad:
        lines.append("失败明细（C1 差额须逐条解释，预期来源：无图注的装饰图）:")
        for stem, c1, c2, c3, c4, blank, leftover in bad:
            lines.append(f"  {stem}: C1={c1} C2={c2} C3={c3} C4={c4} "
                         f"空图={blank} 残留水印流={leftover}")
    lines.append("提示：C4 的偏红占比只是筛选器。结论以人工目视为准——")
    lines.append("      残余偏红来自照片本身的暖色（石质/木质），不是水印。")
    lines.append(f"RESULT: {'PASS' if not bad else 'FAIL'}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行校验，确认它失败**

Run: `python tests/papers/verify_c.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers.figures'`

- [ ] **Step 3: 实现图表抽取**

创建 `tools/papers/figures.py`：

```python
"""按图注定位抽取图表。

策略：找 "Figure N:" / "Table N:" 文本块，取其上方的内容区整区渲染。
不逐图判断矢量/位图——实测两种都有，逐图判断会漏。
整区渲染对两种一视同仁。

水印是覆盖层，渲染前必须在内存里摘掉，否则会烤进产出的 PNG。
"""
import re
from dataclasses import dataclass
from pathlib import Path

import fitz

from . import watermark

CAP = re.compile(r"^\s*(Figure|Fig\.|Table)\s*(\d+)\s*[:.]", re.I)
# 图注上方取多高：图注本身的 y0 往上找版面空白，最多回退到页顶
MIN_BAND = 60.0   # 至少这么高，避免抓到一条线
MAX_BAND = 420.0  # 不超过这么高，避免抓进上一段正文


@dataclass
class Caption:
    kind: str      # "fig" | "tab"
    num: int
    page: int      # 0 起
    y0: float
    text: str


@dataclass
class FigResult:
    n_fig: int
    n_tab: int


def caption_blocks(doc: fitz.Document) -> list[Caption]:
    out: list[Caption] = []
    for pno in range(doc.page_count):
        for b in doc[pno].get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                txt = "".join(s["text"] for s in l["spans"]).strip()
                m = CAP.match(txt)
                if m:
                    kind = "tab" if m.group(1).lower().startswith("tab") else "fig"
                    out.append(Caption(kind, int(m.group(2)), pno,
                                       l["bbox"][1], txt))
    return out


def _band_above(page: fitz.Page, cap: Caption) -> fitz.Rect | None:
    """图注上方的内容带。用 drawings/images 的实际范围约束高度，
    拿不到就回退到固定高度。"""
    pr = page.rect
    top = max(pr.y0, cap.y0 - MAX_BAND)
    band = fitz.Rect(pr.x0 + 20, top, pr.x1 - 20, cap.y0 - 4)
    if band.height < MIN_BAND:
        return None
    return band


def extract_all(src: Path, out_dir: Path, dpi: int = 200) -> FigResult:
    """从**原件**抽图表。原件只读。

    渲染前先 strip_in_memory —— 水印是覆盖层，不摘掉会烤进产出的 PNG。
    """
    doc = fitz.open(src)
    n_fig = n_tab = 0
    try:
        watermark.strip_in_memory(doc)   # 关键：必须在任何 get_pixmap 之前
        caps = caption_blocks(doc)
        for cap in caps:
            page = doc[cap.page]
            band = _band_above(page, cap)
            if band is None:
                continue
            pix = page.get_pixmap(dpi=dpi, clip=band)
            name = f"{cap.kind}-{cap.num:02d}-p{cap.page + 1}"
            out_dir.mkdir(parents=True, exist_ok=True)
            png = out_dir / f"{name}.png"
            png.write_bytes(pix.tobytes("png"))
            (out_dir / f"{name}.caption.txt").write_bytes(cap.text.encode("utf-8"))
            if cap.kind == "fig":
                n_fig += 1
            else:
                n_tab += 1
    finally:
        doc.close()
    return FigResult(n_fig=n_fig, n_tab=n_tab)
```

- [ ] **Step 4: 运行校验，确认 C1–C4 通过**

Run: `python tests/papers/verify_c.py`
Expected: `C1/C2/C3/C4 全通过: True`，`RESULT: PASS`，且每份 `C4 水印对象=1 strip=1 残留流长>0=无`。

**C1 差额非 0 时**：逐条登记是哪一页、哪张图，对照 §8 风险 2（无图注的装饰图）。**不得把差额悄悄抹平**。
**C4 结构化判据失败（`水印对象=0`）时**：说明这份论文的水印形态与已知不同，`find_watermark_xrefs` 漏了它，产出图会静静地带水印。**停下调查该份的水印形态**，不要跳过。

- [ ] **Step 5: 人工目视确认图表无水印**

```bash
python -c "
import sys; sys.path.insert(0,'.')
from pathlib import Path
from tools.papers import io
# 取三份的不同图，输出前 6 张到 reports 供人工看
out = Path('tests/papers/reports'); out.mkdir(parents=True, exist_ok=True)
n = 0
for d in sorted((io.DERIVED / 'figures' / '2025美赛O奖论文').rglob('fig-*.png')):
    if n >= 6: break
    (out / ('c4-' + d.parent.name + '-' + d.name)).write_bytes(d.read_bytes())
    n += 1
print(f'已输出 {n} 张供人工阅看')
"
```
**人工打开这 6 张**，确认无红色「校苑数模公众号」字样。把结论写进 `tests/papers/reports/c-report.txt` 末尾。**未目视确认前不得进 Task 5。**

- [ ] **Step 6: 提交**

```bash
git add tools/papers/figures.py tests/papers/verify_c.py tests/papers/reports/c-report.txt
git commit -m "feat(papers): 图表抽取，C1-C4 判据全通过"
```

> `corpus/papers/figures/` 已在 `.gitignore` 中（约 302 MB，可重生成），**不进 git**。入库的是 `tests/papers/reports/` 里的证据与抽样图。

---

### Task 5: 阶段 4 —— 公式裁图 + 编号/引述句（无 OCR）

**Files:**
- Create: `tools/papers/formulas.py`
- Create: `tests/papers/verify_d.py`

**Interfaces:**
- Consumes: `io.ORIGIN`（**读原件**）、`io.formulas_dir`, `watermark.strip_in_memory`
- Produces:
  - `formulas.equation_numbers(doc) -> list[EqNum]`
  - `formulas.EqNum` —— dataclass，字段 `num: int, page: int, x0: float, y0: float, y1: float`
  - `formulas.extract_all(src: Path, out_dir: Path, dpi: int = 200) -> EqResult`
  - `formulas.EqResult` —— dataclass，字段 `n_eq: int, n_refs: int`

**编号识别**：方程编号是**右对齐的 `(N)`**，且 N 在篇内单调递增。实测 2025 全 43 份括号编号 1058 处、显式 `Eq. (N)` 引用 38 处——1058 含大量非编号的括号数字，故必须加"靠右 + 递增"两个约束才可靠。

- [ ] **Step 1: 写失败的校验脚本**

创建 `tests/papers/verify_d.py`：

```python
"""阶段 4 判据 D1-D2。

D1 公式裁图数 = 编号出现次数（计数型判据，同 C1）
D2 引述句在 md 中能字面定位
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import fitz  # noqa: E402
from tools.papers import formulas, io  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "d-report.txt"


def main() -> int:
    root = io.ORIGIN / "2025美赛O奖论文"
    pdfs = sorted(root.rglob("*.pdf"))
    lines = [f"D 组判据 · 试点 {len(pdfs)} 份", "=" * 72]
    bad = []
    for src in pdfs:
        prob = src.parent.name
        out = io.formulas_dir("2025美赛O奖论文", prob, src.stem)
        res = formulas.extract_all(src, out)

        doc = fitz.open(src)
        detected = len(formulas.equation_numbers(doc))
        doc.close()

        produced = sorted(out.glob("eq-*.png")) if out.is_dir() else []
        d1 = len(produced) == detected

        # D2：每个 .context 里的引述句能在 md 中字面找到
        md = io.md_path("2025美赛O奖论文", prob, src.stem)
        mdtext = md.read_text("utf-8") if md.exists() else ""
        missing = []
        for ctx in sorted(out.glob("eq-*.context")) if out.is_dir() else []:
            for line in ctx.read_text("utf-8").splitlines():
                if line.startswith("REF: "):
                    frag = line[5:].strip()
                    if frag and frag not in mdtext:
                        missing.append(f"{ctx.name}:{frag[:40]}")
        d2 = not missing

        lines.append(
            f"{src.stem:<10} D1 检出编号={detected:<3} 产出裁图={len(produced):<3} "
            f"D2 引用句={res.n_refs:<3} 定位失败={missing or '无'}"
        )
        if not (d1 and d2):
            bad.append((src.stem, d1, d2, missing))

    lines.append("=" * 72)
    lines.append(f"D1/D2 全通过: {not bad}")
    if bad:
        lines.append("失败明细:")
        for row in bad:
            lines.append(f"  {row[0]}: D1={row[1]} D2={row[2]} 缺={row[3]}")
    lines.append("注：本阶段无 OCR、无 .tex 产出——公式一律不转 LaTeX（spec §1）")
    lines.append(f"RESULT: {'PASS' if not bad else 'FAIL'}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行校验，确认它失败**

Run: `python tests/papers/verify_d.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers.formulas'`

- [ ] **Step 3: 实现公式抽取**

创建 `tools/papers/formulas.py`：

```python
"""阶段 4：公式裁图 + 编号/引述句抽取。无 OCR、无 .tex。

公式编号靠三个约束识别（缺一不可，实测单靠括号数字会有 1058 处噪声）：
  1. 文本形态为 (N)
  2. x 位置靠右（距右边距 15% 以内）
  3. N 在篇内单调递增
"""
import re
from dataclasses import dataclass
from pathlib import Path

import fitz

from . import watermark

PAREN = re.compile(r"^\s*\((\d{1,2})\)\s*$")
REF = re.compile(r"\b(?:Eq\.?|Equation)\s*\((\d{1,2})\)", re.I)
RIGHT_BAND = 0.15   # 右边距 15% 内算"靠右"
MAX_EQ_NUM = 99


@dataclass
class EqNum:
    num: int
    page: int
    x0: float
    y0: float
    y1: float


@dataclass
class EqResult:
    n_eq: int
    n_refs: int


def equation_numbers(doc: fitz.Document) -> list[EqNum]:
    """按 形态+靠右+递增 三约束识别公式编号。"""
    cands: list[EqNum] = []
    for pno in range(doc.page_count):
        page = doc[pno]
        cutoff = page.rect.x1 - page.rect.width * RIGHT_BAND
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                txt = "".join(s["text"] for s in l["spans"])
                m = PAREN.match(txt)
                if not m:
                    continue
                if l["bbox"][2] < cutoff:
                    continue
                cands.append(EqNum(int(m.group(1)), pno,
                                   l["bbox"][0], l["bbox"][1], l["bbox"][3]))

    # 递增过滤：贪心保留能构成递增序列的元素
    out: list[EqNum] = []
    last = 0
    for c in sorted(cands, key=lambda e: (e.page, e.y0)):
        if c.num == last + 1:
            out.append(c)
            last = c.num
    return out


def _context(doc: fitz.Document, eq: EqNum) -> str:
    """该公式所在页的编号行 + 页内 where/Eq. 引述句。"""
    page = doc[eq.page]
    lines = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b.get("lines", []):
            txt = "".join(s["text"] for s in l["spans"]).strip()
            if not txt:
                continue
            if PAREN.match(txt) or txt.lower().startswith("where") or REF.search(txt):
                lines.append(f"REF: {txt}")
    return "\n".join(lines)


def extract_all(src: Path, out_dir: Path, dpi: int = 200) -> EqResult:
    """从**原件**抽公式裁图。原件只读。

    渲染前先 strip_in_memory —— 水印是覆盖层，不摘掉会烤进裁图。
    """
    doc = fitz.open(src)
    n_refs = 0
    try:
        watermark.strip_in_memory(doc)   # 必须在任何 get_pixmap 之前
        eqs = equation_numbers(doc)
        for eq in eqs:
            page = doc[eq.page]
            # 公式区：编号行同高，向左取到页左边距
            band = fitz.Rect(page.rect.x0 + 60, eq.y0 - 6,
                             page.rect.x1 - 20, eq.y1 + 6)
            pix = page.get_pixmap(dpi=dpi, clip=band)
            out_dir.mkdir(parents=True, exist_ok=True)
            stem = f"eq-{eq.num:02d}-p{eq.page + 1}"
            (out_dir / f"{stem}.png").write_bytes(pix.tobytes("png"))
            ctx = _context(doc, eq)
            (out_dir / f"{stem}.context").write_bytes(ctx.encode("utf-8"))
            n_refs += len(REF.findall(ctx))
    finally:
        doc.close()
    return EqResult(n_eq=len(eqs), n_refs=n_refs)
```

- [ ] **Step 4: 运行校验，确认 D1/D2 通过**

Run: `python tests/papers/verify_d.py`
Expected: `D1/D2 全通过: True`，`RESULT: PASS`。

**D1 若差额非 0**：逐篇看检出序列断在哪、是漏编号还是多认了括号数字。**不得放宽"递增"约束来凑数**。

- [ ] **Step 5: 提交**

```bash
git add tools/papers/formulas.py tests/papers/verify_d.py tests/papers/reports/d-report.txt
git commit -m "feat(papers): 公式裁图与编号引述句，D1/D2 判据全通过"
```

> `corpus/papers/formulas/` 同样在 `.gitignore` 中，**不进 git**。

---

### Task 6: 阶段 5 —— 索引与稳定 ID

**Files:**
- Create: `tools/papers/vocab.py`
- Create: `tools/papers/vocab/models.txt`
- Create: `tools/papers/index.py`
- Create: `tests/papers/verify_ids.py`

**Interfaces:**
- Consumes: `io.*`、阶段 1–4 的产物、`tests/papers/recon/watermark-scan.json`
- Produces:
  - `vocab.load(path: Path) -> list[str]`
  - `vocab.match(text: str, terms: list[str]) -> list[tuple[str, int]]` —— 返回 (词, 首次出现位置)
  - `index.build(collection: str) -> IndexResult`
  - `index.IndexResult` —— dataclass，字段 `n_entries: int, n_zero_hit: int, index_path: Path, tags_path: Path`

**标级纪律**（spec §5 阶段 5）：`INDEX.md` 每栏来源与标级写死在表头；「亮点」是判断栏，标 `[社区]`，**给不出可指回原文的就留空，不填推测**。

- [ ] **Step 1: 写失败的校验脚本**

创建 `tests/papers/verify_ids.py`：

```python
"""稳定 ID 双向解析校验（教训三.1）。

现有 tests/check-index-pointers.py 只能抓悬空指针，抓不到"条号重排后
仍存在、却指向了另一条事实"的静默失效。稳定 ID 与之互补。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from tools.papers import index, io  # noqa: E402

REPORT = Path(__file__).resolve().parent / "reports" / "ids-report.txt"
ROW = re.compile(r"^\|\s*(P\d{4}-[A-F]-\d{2,})\s*\|")


def main() -> int:
    res = index.build("2025美赛O奖论文")
    lines = ["稳定 ID 双向解析", "=" * 72]

    seen = set()
    dup = []
    bad_parse = []
    for line in res.index_path.read_text("utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        sid = m.group(1)
        if sid in seen:
            dup.append(sid)
        seen.add(sid)
        try:
            io.parse_stable_id(sid)
        except ValueError:
            bad_parse.append(sid)

    lines.append(f"条目数={res.n_entries} 唯一 ID={len(seen)} 重复={dup or '无'}")
    lines.append(f"ID 可解析失败={bad_parse or '无'}")
    lines.append(f"词表零命中篇目数={res.n_zero_hit}")

    # 反向：每个 ID 必须能唯一解析回 (年,题,序)
    roundtrip_ok = True
    for sid in sorted(seen):
        y, p, s = io.parse_stable_id(sid)
        if io.stable_id(f"{y}美赛O奖论文", p, s) != sid:
            roundtrip_ok = False
            lines.append(f"  往返失败: {sid}")

    lines.append(f"双向往返一致={roundtrip_ok}")
    ok = not dup and not bad_parse and roundtrip_ok
    lines.append(f"RESULT: {'PASS' if ok else 'FAIL'}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行校验，确认它失败**

Run: `python tests/papers/verify_ids.py`
Expected: FAIL —— `ModuleNotFoundError: No module named 'tools.papers.index'`

- [ ] **Step 3: 建受控词表**

创建 `tools/papers/vocab/models.txt`（一行一个；**先建种子表，试点后按第三层缺口补**）：

```
AHP
层次分析法
TOPSIS
熵权法
灰色预测
GM(1,1)
ARIMA
指数平滑
线性回归
岭回归
LASSO
主成分分析
PCA
因子分析
聚类分析
K-means
判别分析
支持向量机
随机森林
神经网络
BP神经网络
LSTM
遗传算法
粒子群
模拟退火
蚁群算法
蒙特卡洛
马尔可夫链
元胞自动机
有限差分
有限元
微分方程
Navier-Stokes
SIR
logistic
多目标优化
线性规划
整数规划
动态规划
排队论
图论
最短路
网络流
时间序列
敏感性分析
```

- [ ] **Step 4: 实现词表匹配与索引生成**

创建 `tools/papers/vocab.py`：

```python
"""受控词表的字面匹配。

刻意不做自由生成：字面匹配能指出命中位置，可复核、不虚构。
由模型自由生成的标签是判断而非事实——第一期反复踩过这个坑。
"""
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent / "vocab" / "models.txt"


def load(path: Path | None = None) -> list[str]:
    p = path or DEFAULT
    terms = [
        ln.strip()
        for ln in p.read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.strip().startswith("#")
    ]
    # 长词优先，避免 "PCA" 抢先于 "主成分分析" 造成重复计数
    return sorted(set(terms), key=len, reverse=True)


def match(text: str, terms: list[str]) -> list[tuple[str, int]]:
    """返回 (词, 首次出现位置)，按位置排序。"""
    hits = []
    for t in terms:
        i = text.find(t)
        if i >= 0:
            hits.append((t, i))
    return sorted(hits, key=lambda kv: kv[1])
```

创建 `tools/papers/index.py`：

```python
"""阶段 5：INDEX.md（人读）+ TAGS.md（机读三层）。

标级纪律：客观栏与判断栏分开标级。「亮点」是判断栏，标 [社区]，
给不出可指回原文的就留空——不填推测性内容。
"""
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import fitz

from . import io, vocab, watermark

CAP_FIG = re.compile(r"^\s*(Figure|Fig\.)\s*\d+\s*[:.]", re.I)
CAP_TAB = re.compile(r"^\s*Table\s*\d+\s*[:.]", re.I)
KEYWORDS = re.compile(r"^\s*(Key\s*words?|关键词)\s*[:：]\s*(.+)$", re.I)
SECT = re.compile(r"^\s*(\d+\.?\s+)?([A-Z][A-Za-z ]{2,60})$")

HAS_PROBES = {
    "has_contents": ["Contents"],
    "has_assumptions": ["Assumptions", "Assumption"],
    "has_notations": ["Notations", "Notation"],
    "has_sensitivity": ["Sensitivity"],
    "has_extension": ["Extension", "Extend"],
}


@dataclass
class Entry:
    sid: str
    collection: str
    problem: str
    stem: str
    n_pages: int = 0
    n_figures: int = 0
    n_tables: int = 0
    n_equations: int = 0
    keywords: str = ""
    sections: list[str] = field(default_factory=list)
    has: dict = field(default_factory=dict)
    model_hits: list[tuple[str, int]] = field(default_factory=list)


@dataclass
class IndexResult:
    n_entries: int
    n_zero_hit: int
    index_path: Path
    tags_path: Path


def _scan_pdf(p: Path) -> dict:
    doc = fitz.open(p)
    d = {"n_pages": doc.page_count, "n_figures": 0, "n_tables": 0,
         "n_equations": 0, "sections": [], "keywords": "", "has": {}}
    # 水印必须先去：它也在文本层里，不摘会污染 keywords 与 sections。
    # 用结构化方式（置空 XObject 流），不用字体启发式——理由见 spec §4.1.1。
    watermark.strip_in_memory(doc)
    full = []
    for pno in range(doc.page_count):
        page = doc[pno]
        for b in page.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for l in b.get("lines", []):
                spans = l["spans"]
                if not spans:
                    continue
                txt = "".join(s["text"] for s in spans).strip()
                if not txt:
                    continue
                full.append(txt)
                size = max(s["size"] for s in spans)
                if CAP_FIG.match(txt):
                    d["n_figures"] += 1
                elif CAP_TAB.match(txt):
                    d["n_tables"] += 1
                elif size >= 13.5 and 2 < len(txt) < 60 and not txt.endswith("."):
                    d["sections"].append(txt)
    doc.close()
    text = "\n".join(full)
    m = KEYWORDS.search(text)
    if m:
        d["keywords"] = m.group(2).strip()
    for k, probes in HAS_PROBES.items():
        d["has"][k] = any(x.lower() in text.lower() for x in probes)
    d["_full"] = text
    return d


def build(collection: str) -> IndexResult:
    root = io.ORIGIN / collection          # 索引读原件，水印在扫描时已滤除
    pdfs = sorted(root.rglob("*.pdf"))
    terms = vocab.load()
    entries: list[Entry] = []
    per_problem: dict[str, int] = {}

    for p in pdfs:
        prob = p.parent.name
        per_problem[prob] = per_problem.get(prob, 0) + 1
        sid = io.stable_id(collection, prob, per_problem[prob])
        d = _scan_pdf(p)
        full = d.pop("_full")
        e = Entry(sid=sid, collection=collection, problem=prob,
                  stem=p.stem, **d)
        e.model_hits = vocab.match(full, terms)
        # n_equations 取自阶段 4 的产出，不在此处另算一遍
        # （同一份事实不在两处各算一次——spec §6）
        fdir = io.formulas_dir(collection, prob, p.stem)
        e.n_equations = len(list(fdir.glob("eq-*.png"))) if fdir.is_dir() else 0
        entries.append(e)

    n_zero = sum(1 for e in entries if not e.model_hits)

    # ---- INDEX.md ----
    L = [
        "# 获奖论文索引（试点 · 2025）",
        "",
        "日期：2026-09-23　·　来源：`corpus/历届优秀论文/2025美赛O奖论文/`",
        "",
        "**栏目标级**：`[客观]` 可由文本层直接确定 · `[社区]` 含判断，须附页/行指针",
        "",
        "| 稳定 ID `[客观]` | 题号 `[客观]` | 页数 `[客观]` | 图 `[客观]` | 表 `[客观]` | 主题 `[客观]` | 亮点 `[社区]` |",
        "| :--- | :--- | ---: | ---: | ---: | :--- | :--- |",
    ]
    for e in entries:
        L.append(
            f"| {e.sid} | {e.problem} | {e.n_pages} | {e.n_figures} | "
            f"{e.n_tables} | {e.keywords[:60]} | |"
        )
    L += ["", "> 「亮点」栏本轮一律留空：未逐篇精读到能给出可指回原文的判断。",
          "> 留空而非填推测——见 spec §5 阶段 5。", ""]
    idx = io.DERIVED / "INDEX.md"
    idx.write_bytes("\n".join(L).encode("utf-8"))

    # ---- TAGS.md ----
    T = [
        "# TAGS 机读索引（试点 · 2025）",
        "",
        "## 局限（必读）",
        "",
        "词表匹配抓不到「用了但没写名字」的模型，也抓不到词表外的模型。",
        "**本文件是检索入口，不是完备清单**——先据此定位候选，再读全文。",
        "",
        "## 第一层 · 客观",
        "",
        "| ID | 题号 | 页 | 图 | 表 | 公式 | Contents | Assumptions | Notations | Sensitivity | Extension |",
        "| :--- | :--- | ---: | ---: | ---: | ---: | :-: | :-: | :-: | :-: | :-: |",
    ]
    for e in entries:
        h = e.has
        mk = lambda k: "✓" if h.get(k) else ""  # noqa: E731
        T.append(
            f"| {e.sid} | {e.problem} | {e.n_pages} | {e.n_figures} | "
            f"{e.n_tables} | {e.n_equations} | {mk('has_contents')} | "
            f"{mk('has_assumptions')} | {mk('has_notations')} | "
            f"{mk('has_sensitivity')} | {mk('has_extension')} |"
        )

    T += ["", "> `Contents/Assumptions/…` 各栏是**标题里字面出现了该词**这个事实，",
          "> 不等于「论文确实做了敏感性分析」。", "",
          "## 第二层 · 判断 `[社区]`（受控词表字面命中，附出处指针）", ""]
    for e in entries:
        if not e.model_hits:
            continue
        tagstr = " · ".join(f"`{w}`@{i}" for w, i in e.model_hits)
        T.append(f"- **{e.sid}**（题 {e.problem}）：{tagstr}")
    T += ["", "> `@N` 为该词在全文文本中的字符位置，可据此复核。", "",
          "## 第三层 · 词表缺口自曝", "",
          f"以下 {n_zero} 篇在受控词表中**零命中**——要么真未用词表内模型，",
          "要么用了词表外的模型。**这是已知漏检，登记而非掩盖。**", ""]
    for e in entries:
        if not e.model_hits:
            T.append(f"- {e.sid}（题 {e.problem}）")

    tags = io.DERIVED / "TAGS.md"
    tags.write_bytes("\n".join(T).encode("utf-8"))

    return IndexResult(n_entries=len(entries), n_zero_hit=n_zero,
                       index_path=idx, tags_path=tags)
```

- [ ] **Step 5: 运行校验，确认通过**

Run: `python tests/papers/verify_ids.py`
Expected: `RESULT: PASS`，`重复=无`，`双向往返一致=True`。

- [ ] **Step 6: 提交**

```bash
git add tools/papers/vocab.py tools/papers/vocab/ tools/papers/index.py tests/papers/verify_ids.py tests/papers/reports/ids-report.txt corpus/papers/INDEX.md corpus/papers/TAGS.md
git commit -m "feat(papers): 阶段5 索引与稳定 ID，含 TAGS 三层与词表缺口自曝"
```

---

### Task 7: 阶段 6 —— 试点汇总、证据归档与放行评估

**Files:**
- Create: `tools/papers/cli.py`
- Create: `tests/papers/verify_all.py`
- Create: `corpus/papers/PROVENANCE.md`

**Interfaces:**
- Consumes: 全部前置任务的产物与报告
- Produces:
  - `cli.main(argv: list[str]) -> int` —— 子命令 `watermark` / `text` / `figures` / `formulas` / `index` / `all`
  - `verify_all` 的汇总结论与**放行评估**写入 `tests/papers/reports/pilot-summary.txt`

- [ ] **Step 1: 写失败的汇总校验**

创建 `tests/papers/verify_all.py`：

```python
"""试点汇总：跑齐各组判据 + A1 原件哈希复核，输出放行评估。"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = HERE / "reports" / "pilot-summary.txt"
STAGES = ["verify_io.py", "verify_wm.py", "verify_b.py", "verify_c.py",
          "verify_d.py", "verify_ids.py"]
BASELINE = HERE / "reports" / "origin-sha256-2025.txt"


def check_a1(lines) -> bool:
    """A1：原件 sha256 与基线逐字相同。流水线全程不得改动原件。"""
    sys.path.insert(0, str(HERE.parent.parent))
    from tools.papers import io

    base = {}
    for ln in BASELINE.read_text("utf-8").splitlines():
        if ln.strip():
            h, k = ln.split("  ", 1)
            base[k] = h
    now = io.sha256_tree("2025美赛O奖论文")

    missing = sorted(set(base) - set(now))
    added = sorted(set(now) - set(base))
    changed = sorted(k for k in set(base) & set(now) if base[k] != now[k])

    lines.append(f"A1 原件哈希: 基线 {len(base)} 份 / 现在 {len(now)} 份")
    lines.append(f"   改动={changed or '无'}  缺失={missing or '无'}  新增={added or '无'}")
    ok = not changed and not missing and not added
    lines.append(f"   A1 结论: {'原件一字未动' if ok else '原件被改动！'}")
    return ok


def main() -> int:
    lines = ["M6 前置流水线 · 试点汇总（2025 · 43 份）", "=" * 72]
    failed = []

    if not BASELINE.exists():
        lines.append(f"A1 基线缺失: {BASELINE} —— 无法复核原件完整性")
        failed.append("A1-baseline")
    elif not check_a1(lines):
        failed.append("A1-origin-modified")

    lines.append("=" * 72)
    for s in STAGES:
        r = subprocess.run([sys.executable, str(HERE / s)],
                           capture_output=True, text=True, timeout=7200)
        status = "PASS" if r.returncode == 0 else "FAIL"
        lines.append(f"{s:<18} {status}")
        if r.returncode != 0:
            failed.append(s)

    lines += ["=" * 72,
              "证据清单（逐字原文，受版本控制）:"]
    for p in sorted((HERE / "reports").glob("*.txt")):
        lines.append(f"  {p.name}  {p.stat().st_size} 字节")

    lines += ["", "放行全量（201 份）的条件:",
              "  1. 上述六项全部 PASS",
              "  2. A1 原件哈希复核通过（原件一字未动）",
              "  3. 各阶段耗时实测已记录",
              "  4. 图表/公式的人工目视抽查结论已写入对应报告",
              "",
              f"当前状态: {'可放行' if not failed else '未放行 —— ' + ', '.join(failed)}",
              f"RESULT: {'PASS' if not failed else 'FAIL'}"]

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print("\n".join(lines))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 运行汇总，确认它失败**

Run: `python tests/papers/verify_all.py`
Expected: FAIL —— `cli.py` 尚未创建（若其它脚本已就绪，此处会显示各阶段状态）。

- [ ] **Step 3: 实现统一入口**

创建 `tools/papers/cli.py`：

```python
"""统一入口：python -m tools.papers.cli <stage> [--collection 名]

stage ∈ text | figures | formulas | index | all

**没有 watermark 阶段**：去水印不是一个独立产出步骤，它在 text/figures/
formulas 各自读取时于内存中完成，不产生任何文件（spec §4.1）。

所有阶段都直接读**原件**，原件全程只读。
"""
import argparse
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.papers import figures, formulas, index, io, textmd  # noqa: E402

DEFAULT_COLLECTION = "2025美赛O奖论文"


def _originals(collection: str) -> list[Path]:
    root = io.ORIGIN / collection
    return sorted(root.rglob("*.pdf"))


def run_stage(stage: str, collection: str) -> int:
    paths = _originals(collection)
    if not paths:
        print(f"[!] {collection} 下没有 PDF", file=sys.stderr)
        return 1
    t0 = time.time()
    n = 0
    for src in paths:
        rel = str(src.relative_to(io.ORIGIN))
        prob = io.problem_of(rel)   # 合集由调用方显式传入，不从路径反推
        stem = src.stem

        if stage in ("text", "all"):
            textmd.extract(src, io.md_path(collection, prob, stem))
        if stage in ("figures", "all"):
            figures.extract_all(src, io.figures_dir(collection, prob, stem))
        if stage in ("formulas", "all"):
            formulas.extract_all(src, io.formulas_dir(collection, prob, stem))

        n += 1
        if n % 10 == 0:
            print(f"  ... {n}/{len(paths)}  {time.time() - t0:.1f}s")

    if stage in ("index", "all"):
        index.build(collection)

    dt = time.time() - t0
    print(f"[{stage}] {collection}: {n} 份，耗时 {dt:.1f}s（{dt / max(n,1):.2f}s/份）")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["text", "figures", "formulas", "index", "all"])
    ap.add_argument("--collection", default=DEFAULT_COLLECTION)
    args = ap.parse_args(argv)
    return run_stage(args.stage, args.collection)


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: 跑通全链路并记录耗时**

Run:
```bash
python -m tools.papers.cli all --collection 2025美赛O奖论文
```
Expected: 末行形如 `[all] 2025美赛O奖论文: 43 份，耗时 <N>s（<x>s/份）`。
**把这一行原样抄进 `tests/papers/reports/pilot-summary.txt` 的耗时表** —— 这是放行条件 2 的证据。

- [ ] **Step 5: 运行全部判据与汇总**

Run:
```bash
python tests/papers/verify_all.py
```
Expected: 六项全 PASS，末行 `当前状态: 可放行`

- [ ] **Step 6: 写 PROVENANCE**

创建 `corpus/papers/PROVENANCE.md`，内容须含：

```markdown
# 语料来源与处理台账

## 来源

| 项 | 值 |
| :--- | :--- |
| 原件位置 | `corpus/历届优秀论文/`（**原地未动，全程只读**） |
| 派生物位置 | `corpus/papers/` |
| 试点范围 | `2025美赛O奖论文` 43 份 |
| 侦察日期 | 2026-09-23 |

## 水印

| 合集 | 厂商 | 形态 |
| :--- | :--- | :--- |
| 2023/2024 | 校苑数模 | Adobe 标准水印 Form XObject + `/OC` 图层 |
| 2025 | 校苑数模公众号 | 同上 |
| 2023（5 份） | 英伽教育 | 同上 |
| 2022 / UMAP | 无 | —— |

**不产出清洗版 PDF**。水印在抽取时于内存中处理：
- 正文：按 span 特征（`MicrosoftYaHei` 72pt）滤除
- 图表/公式：渲染前在内存里置空水印 XObject 的流

**原件保留且未被改动**——A1 判据以 sha256 前后比对证明，
基线见 `tests/papers/reports/origin-sha256-2025.txt`。

## 可复现命令

```bash
python tools/scan_watermarks.py                              # 侦察
python -m tools.papers.cli all --collection 2025美赛O奖论文    # 抽取（原件只读）
python tests/papers/verify_all.py                             # 全部判据
```

## 不入库的大体积产物

`corpus/papers/figures/` 与 `corpus/papers/formulas/`（实测 43 篇约 302 MB，
全量约 1.4 GB）**可由上面的 cli 命令确定性重生成**，故写在 `.gitignore` 中。
入库的是抽取出的文本、索引与判据证据。

## 字节保真

仓库 `core.autocrlf = true`。`corpus/papers/**` 已在根级 `.gitattributes`
标 `-text`；所有产物走字节级写入并回读校验（`io.write_bytes_checked`）。
起因见 `corpus/algorithms/PROVENANCE.md` §5.1（883 个文件曾被写坏为 `\r\r\n`）。

## 已知缺口

- 32 份扫描件（UMAP 合集）**未处理**，正文不可检索
- 公式一律未转 LaTeX（spec §1），只提供裁图与编号/引述句
- `TAGS.md` 第二层的关键词来自受控词表字面匹配，**是检索入口不是完备清单**
```

- [ ] **Step 7: 提交**

```bash
git add tools/papers/cli.py tests/papers/verify_all.py tests/papers/reports/pilot-summary.txt corpus/papers/PROVENANCE.md
git commit -m "feat(papers): 阶段6 统一入口、试点汇总与放行评估，台账归档"
```

---

## 收尾

全部七个任务完成后：

- 试点产物在 `corpus/papers/`（md + INDEX + TAGS + PROVENANCE 入库；figures/formulas 在本地磁盘但不入库），可直接供 M2/M3 检索
- 判据证据在 `tests/papers/reports/`，逐字原文受版本控制
- **全量放行的前提**：`tests/papers/reports/pilot-summary.txt` 显示"可放行"。若未放行，**先解决失败项，不得先跑全量**
- **原件自始至终只读**：任何阶段都不得写回 `corpus/历届优秀论文/`。全量时 A1 的基线要扩到全部 201 份

## Self-Review 记录

写完后对照 spec 逐节核对：

| spec 节 | 对应任务 | 状态 |
| :--- | :--- | :--- |
| §4 目录布局（无 `clean/`） | Task 1（`io.py` 全权负责路径映射） | ✅ |
| §4.1 不产出清洗版 PDF | Task 2（内存处理）、Task 3/4/5 全部读原件 | ✅ |
| §4.2 换行符闸门 | Task 1 Step 5/7（含 `git check-attr` 验证） | ✅ |
| §4.1 大体积产物不入库 | Task 1 Step 6（`.gitignore`）+ Task 4/5 提交说明 | ✅ |
| §5 A1 原件 sha256 不变 | Task 2 Step 1 记基线 + Task 7 `check_a1()` 复核 | ✅ |
| §5 A2/A3 正文侧 | Task 3（有 md 可验时才做） | ✅ |
| §5 A4（图表无水印，计划中改称 C4） | Task 4 结构化断言 + 人工目视 | ✅ |
| §5 阶段2 B1–B2 | Task 3 | ✅ |
| §5 阶段3 C1–C3 | Task 4 | ✅ |
| §5 阶段4 D1–D2 | Task 5 | ✅ |
| §5 阶段5 稳定 ID | Task 6 | ✅ |
| §6 TAGS 三层 | Task 6 | ✅ |
| §6 局限写死文件头 | Task 6 Step 4（TAGS.md「局限（必读）」节） | ✅ |
| §5 阶段6 证据归档 | Task 7 | ✅ |
| §7 放行条件 | Task 7 Step 1（四条条件写进汇总） | ✅ |
| §8 风险 2（无图注的图） | Task 4 C1 差额登记 | ✅ |
| §8 风险 3（TAGS 含判断） | Task 6 标级 | ✅ |

> **一处命名漂移**：spec §5 把"图表无水印"编在 A 组（A4），因它的产物来自图表任务，
> 计划里改称 **C4**，与 C 组同处。判据本身未变，只是归组调整。spec 与计划以本节为准。

**类型一致性核对**：`io.stable_id` / `parse_stable_id` 签名在 Task 1 定义，Task 6 的 `index.build` 与 `verify_ids.py` 沿用同名同参；`StripResult` / `MdResult` / `FigResult` / `EqResult` / `IndexResult` 各自在定义任务中被消费方按同名字段访问。

### 自查中改掉的实质缺陷

| # | 缺陷 | 性质 | 处置 |
| :--- | :--- | :--- | :--- |
| 1 | **A1 判据是同义反复**——原写成 `strip.pages == fitz.open(src).page_count`，两边是同一个文档，恒为真，证明不了任何事 | **假判据**（比占位符更危险：它看着像在验，其实永远通过） | 改为比较**原件与清洗版两个文件**的页数，并同时打印两侧页数 |
| 2 | `collection_problem` 从路径反推合集——2023 合集的题号上层是中文长子目录而非合集，会**静默取错** | 设计缺陷 | 改为 `problem_of` 只返回题号，**合集由调用方显式传入**；加了两层深路径的测试用例 |
| 3 | `verify_a.py` 里残留 `... if False else ...` 的垃圾表达式 | 占位符残留 | 删除，改为显式路径 |
| 4 | `io._sub()` 定义后无任何调用 | 死代码 | 删除 |
| 5 | C2 用 `fitz.Pixmap` 手挑通道算非白像素，可读性差且易错 | 实现脆弱 | 改用 PIL 的 `histogram()`，并在报告里打印实际非白占比 |
| 6 | B2 在"未检出目录"时静默记为通过 | **判据被架空**（与 A5 同类错误） | 改为记为"不适用"，**不得记为通过**；同时报告实际目录条目数 |
| 7 | `index.py` 的 `n_equations` 恒为 0，与 spec §6「取自阶段 4 的 D1 计数」不符 | spec 覆盖缺口 | 改为读 `formulas_dir` 下 `eq-*.png` 的实际数量 |

### 第二轮修订：取消清洗版 PDF（2026-09-23，用户提出后实测确认）

用户问「能否在不清洗的条件下准确读取所需内容」。实测（`build/probe_noclean.py`）证明**可以**，于是：

| # | 原设计 | 实测结论 | 处置 |
| :--- | :--- | :--- | :--- |
| 8 | 去水印后**另存清洗版 PDF**，下游读它 | 正文靠 span 特征过滤即可（过滤后水印字 0 命中）；图表靠**内存**置空后渲染（目视确认干净） | **取消 `clean/` 目录**。去水印在内存完成，不落盘。省掉约 270 MB/试点、约 1.7 GB/全量的派生 PDF |
| 9 | 判据 A1「页数不变」、A5「无水印件零改动」锚在清洗版 PDF 上 | 没有清洗版可锚 | 判据重定义为 **A1 原件 sha256 前后不变**——从"我保证没写"变成**可验证的事实**，比原 A5 强 |
| 10 | 计划要提交 figures/ 与 formulas/ 全部 PNG | 实测 43 篇约 **302 MB**（全量约 1.4 GB），且可由 cli 命令确定性重生成 | 写进 `.gitignore`，**不入库**。入库的是 md、索引与判据证据 |

> 修订后**去水印仍是唯一的高危环节**，但被 A1（没碰原件）+ A3（正文逐字相同）双向锁住：
> A1 锁"没多改"，A3 锁"滤干净了但没伤正文"。

### 第三轮修订：Task 1 审查驱动的修正（2026-09-23）

Task 1 实现后的独立审查（Approved）又挑出 2 Important + 6 Minor，已全部修复并同步进本计划：

| # | 缺陷 | 性质 | 处置 |
| :--- | :--- | :--- | :--- |
| 11 | `sha256_tree` 对错误合集名**静默返回 `{}`**，而 A1 是两张表比对——**两个空表相等，零哈希也报绿** | **判据可空过**（与 #1 同一类，第三例） | 加 fail-closed：目录不存在抛 `FileNotFoundError`，结果为空抛 `ValueError` |
| 12 | 闸门证据只存在于 `.superpowers/`（git 忽略） | **证据丢失**（第一期 GREEN-1 同类错误重犯） | 原始命令输出入库为 `tests/papers/reports/gitattributes-gate.txt` |
| 13 | `stable_id` 的 `problem not in "ABCDEF"` 是**子串**测试，放过 `"AB"`/`""`，与逆函数正则矛盾 | 双向不变式断裂 | 改用共享的 `_PROBLEMS = tuple("ABCDEF")` |
| 14 | 校验脚本崩溃时留下已提交的 `RESULT: PASS` | 假绿证据（同 #11 类） | 报告写入移入受保护路径，异常时写 `RESULT: FAIL` + traceback |
| 15 | docstring 声称 `write_bytes`/`read_bytes` 回读能抓 autocrlf——**它绕过 git，抓不到** | **过度声称已验证** | 改正措辞并写清它到底能抓什么；行尾转换的验证改由 git 索引往返对照承担 |
| 16 | 报告 CRLF 落盘 / LF 入库，非逐字节一致；嵌入机器专属绝对路径 | 证据保真 | `write_bytes`+LF、只写仓库相对路径、`tests/papers/reports/** -text` |

> **第三例了。** #1（我自查）、#11、#14 是同一类：**判据或证据会在什么都没验的情况下呈现绿色**。
> 这类缺陷实跑抓不到（脚本退出码是 0），必须靠"这条判据在什么情况下会失败"的反问才现形。
> 实施后续任务时，凡是新增判据，都要能回答这个问题。

### 第四轮修订：Task 2 实现暴露的**设计**缺陷（2026-09-23）

Task 2 的实现者报出一条 concern，独立测量后确认为**我 spec 里的设计错误**：

| # | 缺陷 | 性质 | 处置 |
| :--- | :--- | :--- | :--- |
| 17 | spec 写「水印 span 特征唯一：`MicrosoftYaHei` 72pt」——**那是从单份论文得出的，被写成了通则**。实测全 201 份有**三种**字体（`KaiTi` 74.4/76.5、`SimHei` 83.4、`MicrosoftYaHei` 72），字体启发式只覆盖 **43/120**，静默漏 77 份 | **单样本当通则**（"过度声称已验证"的另一种形态） | 正文侧改用与图表/公式**同一个结构性机制**（置空 XObject 流），实测 120/120、81 份无水印零误伤。字体启发式整体废弃 |
| 18 | 更阴险的一点：**试点那 43 份恰好全在字体命中范围内** | 试点会绿着通过、全量才炸 | 已写进全局约束：「不能依赖会随输入变化的特征做判据，优先用结构性的」 |
| 19 | A3 原定义是"剔除水印字串后逐字相同"——整段字符串替换，**多替少替都不易察觉**（2023 每页把水印拆成 8 个片段） | 判据不够锐利 | 重定义为 **fail-closed**：逐 span 取差集，**被移除的每一个 span 都必须是水印字串的子串**，出现任何非水印片段即 FAIL。实测 2023 样本移除 1,150 字全部是碎片、零正文损失 |

> **这一轮的教训值得单记**：把一次观察写成通则，和"跑通了就说算对了"是同一个毛病的两种形态。
> #17 的危险之处不在错误本身，而在**它会让试点通过**——一个只在全量时才暴露的缺陷，
> 恰恰是最容易被"试点绿了"这句话掩盖的。

### 第五轮修订：判据「看起来可失败」但被自身筛选蕴含（2026-09-23）

Task 2 复审又抓出一条同类缺陷，**这已是第四例**：

| # | 缺陷 | 性质 | 处置 |
| :--- | :--- | :--- | :--- |
| 20 | `verify_wm.py:373` 的 `n_strip > 0` 在"按 `xrefs` 非空筛出的样本集"上**恒真**；它声称会抓的"水印形态不同 → `find_watermark_xrefs` 返回空"那种情况，会让样本**被排除出集合**而非失败 | **判据声称的失败条件它做不到** | 样本改按 **recon 真值**（`wm_texts` 非空）筛选，再要求 `n_strip > 0`；§2/§3 的强断言同样继承此修正 |
| 21 | 修复提交删掉 `is_watermark_span` 后，**弄坏了两个已入库文件所引用的复现脚本**（`wm_font_probe.py:78` 一跑即 `AttributeError`），且修复报告未披露 | 证据链断裂 | 该探针自带旧启发式的本地副本（它是"为何废弃"的证据），并断言输出仍为 `命中 43/120` |

> **为什么前三次的"写出失败条件"要求没拦住第四次**：因为判据可以**看起来**可失败。
> 这次要求升级为**可操作的形式**——**改坏被测代码，看它红不红**。
> 变异测试在本轮已证明有效（M1/M2 都真红了），而"我认为它会因 X 失败"这种自述不算数。

### 第六轮修订：Task 3 复审（2026-09-23）

| # | 缺陷 | 性质 | 处置 |
| :--- | :--- | :--- | :--- |
| 22 | **A3 原写法（我写在计划里的）是恒真判据**：`not bad_removed` 在"零移除"时差集为空、空集不含越界片段 → **strip 完全失效也绿** | **判据不能失败（第五例）——且是**我在立下"必须变异证明"之后**写下的 | 补伴随判据"带水印字却零移除 → FAIL"，变异证明会红 |
| 23 | **交付物本身没有任何判据**：`to_markdown` 静默丢正文时 A2/A3/B1 全绿、B2 在 30/43 上"不适用"——整条链没有一条会红 | 验了过程，没验产物 | 补 md 内容判据（本轮进一步要求改为双边等式） |
| 24 | **变异验证自身差点产出假绿**：`watermark.py` 磁盘 CRLF vs `textmd.py` LF，三个变异锚点没匹配上 → 会报"3 条已验证"而实际没跑 | 元层面的假绿 | 实现者发现并重跑；要求把锚点匹配记录一并入库（Minor 4） |
| 25 | **B2 的证据文件陈述了关于语料的错误事实**：称"30 份没有 Contents 页"，实测 **42/43 都有**；真实适用面 41/43 而非 13/43 | **证据文件里的假事实**（比没有更坏） | 放宽点引线口径；三态拆分；"找到但解析 0 条"改硬失败 |
| 26 | 唯一作用于交付物的判据是**宽松单边下界**（松量最大 1,315 字符＝正文 2.5%），**静默丢一段正文仍通过** | 判据过宽 | 改为双边等式（标记数可记账） |
| 27 | 失败路径写入的 traceback 含绝对路径，**崩溃时才破约束** | 约束在看门狗触发那刻失效 | 消毒 traceback 或只记类型 + 仓库相对帧 |
| 28 | `n_boundary`（置空后仍是 WM_WORDS 子串的 span）**只打印不设门** | 量了但不判 | 改为设门——**2023 那 77 份按单字片段绘制水印**，A2 按整串短语匹配可能不触发，这是唯一盯它的判据 |
