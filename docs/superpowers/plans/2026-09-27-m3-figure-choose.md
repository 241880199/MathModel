# M3 `mcm-figure-choose` 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实施。步骤用 `- [ ]` 复选框跟踪。

**Goal:** 交付 M3 的第一份 skill `mcm-figure-choose`——语言无关的「图型决策树 + 设计规范」，并把它做成**可被机器复算**的规范（数字有守卫、指针有守卫、判据有变异证明），而不是又一份"自称权威却无人引用"的文本。

**Architecture:** 规范正文**只写一处**（`references/house-style.md`）；`provenance.md` 承载每个实测数的口径与复跑命令；`chart-types.md` 是决策树。配两支检查器（`check-figure-style.py` 管产物、`check-spec-pointers.py` 管引用完整性），判据走 **RED → GREEN → 变异证明**，证据逐字入 `tests/`。

**Tech Stack:** Python 3.11.9 · PyMuPDF 1.27.2（`fitz`，读 PDF 页盒 + 栅格化）· Pillow（像素统计）· 标准库 `re`/`json`/`argparse`。**本轮不需要 LaTeX**（TikZ 是 `mcm-schematic` 的事）。

## Global Constraints

以下为 spec 的项目级硬约束，**每个任务的要求都隐含包含本节**。

- **判据证据须写进受版本控制的 `tests/skills/figure-choose/`，逐字原文**（通则 7）。`.superpowers/` 是 git 忽略的暂存区——**证据放那里等于丢失**。**实施报告也要自己写到磁盘**（`.superpowers/sdd/task-*.md`）。
- **凡新增判据，必须用一次变异证明它真的会红**：改坏被测对象 → 跑一次 → 看它红不红。**改不红就是假判据。**
  本项目已出现**六次**「判据在什么都没验的情况下报绿」。"写出失败条件"这条要求**拦不住第四次**，故升级为**必须实测一次变异**。
- **判据必须 fail-closed**：拿不到参照（图不存在、正文宽没给、解析不出）时**抛错/非零退出**，**不得**返回空结果静默通过。
- **分母口径必须写死**：凡比值类判据，**写清分母是什么、怎么量**，并给复跑命令。
  代价实例（本轮侦察）：同一个"落在 [0.9,1.1) 的比例"，用**全局中位 6.31in** 作分母得 **56.6%**、用**逐篇 p90** 得 **59.4%**——**中位数一致、百分比不一致**。规范里一律取 **逐篇正文行宽 p90**。
- **凡实测数必须带样本范围**：`2025 单年 · 43 份 · 662 图 · O 奖无对照组 · 其余 158 份未抽取`。**单年单批不得写成通则**（通则 4.3）。
- **参照分布 ≠ 判据**：凡"获奖论文通常长什么样"的分布，只许写成参照，**不得作为判据**（"像不像获奖论文"从来不是判据）。
- **规范数值只许出现在 `house-style.md` 一处**；其余 skill（含将来的 `mcm-plot-*`）**只许给指针、不许重述**（lessons 4.8）。**重述即红**（由 Task 7 的检查器强制）。
- **量不到的项必须如实标注**：字号 / 线宽 / 字体族 = **规范性来源**，标〔社区〕，并写明**本样本量不到**。**不许把规范来源伪装成实测。**
- **`[社区]` 标记只用于自订/惯例来源**；凡官方原文确实如此表述的才可标 `[官方]`（通则 1）。
- **写入一律字节级**（`Path.write_bytes`），**禁止 `write_text`**（Windows 上会写 CRLF；`docs/**`、`tests/**`、`.claude/**` 均已由 `.gitattributes` 标 `-text`）。
- **判字节/文件身份用 `git hash-object` 比对 `HEAD` blob**，**别用裸 `sha256sum`**（本仓 `core.autocrlf = true`）。
  **也别用 `grep -c $'\r'` 数 CRLF**——本壳不展开 `$'\r'`，它会退化成"含字母 r 的行数"（controller 实测踩过，给出 168/193/535 的假警报）；用 Python 读 `rb` 数 `\r\n`。
- **报告与证据里不写绝对路径**（不写 `D:\Projects\...`），只写仓库相对路径。
- **RED 场景的 subagent 只收场景正文**，不得带简报、背景或期望答案；**不得用 `fork`**（fork 继承上下文）（通则 8）。
- **参考对象**：`docs/superpowers/specs/2026-09-27-m3-figure-choose-design.md`（spec）· `tests/figures-recon/`（侦察证据）· `docs/mcm-suite-lessons.md`（通则与流程教训，**开新模块前必读**）。

## 派发指令必带（每次派 subagent 都要附）

> 1. `[官方]` 标记只用于官方原文确实如此表述的断言；自订阈值/取舍/惯例一律标 `[社区]`。
> 2. **你写进任何文件的每一个数字，必须来自你当场跑过的命令**，并把命令与输出贴进报告。（本项目同一个坑复发过五次。）
> 3. **编辑既有文件一律先回原文件核再改**；**允许推翻派发指令**——实测与指令冲突时以实测为准，并写明冲突点。
> 4. **报告必须自己写到磁盘**（`.superpowers/sdd/task-*.md`），别只在最终消息里说（会话崩溃就丢）。
> 5. 验证证据须归档进 `tests/skills/figure-choose/`，**逐字原文**。
> 6. **凡新增判据/守卫，必须用一次变异证明它会红**；变异驱动器要**落盘**（否则"我跑过"不可独立复现）。
> 7. **不得写绝对路径**；写入用 `write_bytes` + LF。
> 8. 本机**已有 TeX 工具链**（TeX Live 2026，`D:\Software\texlive\2026\bin\windows`），故**不得以"本机无法编译"为由跳过验证**；但**本轮不需要 LaTeX**。用户赛中仍走网页端编译器。
> 9. **"我没找到" ≠ "它不存在"**（通则 4.5）：查不到就写"在本次范围内未查到 + 我怎么找的"。
> 10. **修复不是单调改进，每轮都可能引入新错——复审不能省。**

## 实测基线（2026-09-27 侦察，供实现者校准）

来源：`tests/figures-recon/`（已入库）· 报告 `.superpowers/sdd/task-m3-figure-recon-report.md`。
**范围**：`corpus/papers/figures/` 的 **662 张图 + 246 张表**，来自 **2025 单年 43 份 O 奖论文**；O 奖**无对照组**；C 题占 42%；其余 158 份未抽取。

| 事实 | 值 | 口径 |
| :--- | :--- | :--- |
| 图宽 / 正文宽 比值 | 中位 **0.951** · p25 **0.80** · p75 **1.00** · p95 1.08 · **max 1.19** | 物理宽 = `w_px / 200`；正文宽 = 逐篇正文行宽 p90（全局中位 **6.31 in**） |
| 页面 | **A4**（595.32 × 841.92 pt），**不是 US Letter** | 43 篇正文页 |
| 横图占比 / 宽高比 | **98.0%** / 中位 **2.42**，`aspect≥2` 53.5% | n=662 |
| 图宽 / 图高 | 中位 **6.00 in** / **2.63 in** | n=662 |
| 彩色主色数（去掉黑/白/灰、占比 ≥0.5%） | 图**中位 3**；**19.5% 零彩色**；**表 83.3% 零彩色** | n=662 / 246 |
| matplotlib 默认色序（tab10） | **已证实下界 0.9%**（人眼复核 6/6）；**松判据那版 17.8% 已证伪，不得引用** | n=662 |
| 多面板 / 内嵌 3D / 饼图 / 图例 | 50.8%（**只能当上界**）/ 9.2% / **0%** / 10.8%（**判据已证废**） | 判断层 n=120 |
| 图注可切出 `Figure N` | **662/662** | n=662 |
| 图注冒号形态 | **87.3% ASCII `:`** | n=662 |
| 图注词数 | 中位 **5** · p95 **12** · **无一条超 17** | n=662 |
| 图注句末标点 | **94.6% 不以句号结尾** | n=662 |
| 空图注 | **17/662**（只有 `Figure 13:` 没正文）——**当反例** | n=662 |
| dpi 元信息 | **不可信**（908/908 相同 = 200 dpi 渲染常量） | 全样本 |
| 字号 / 线宽 / 字体族 | **量不到**（PNG 反推得 1.54–11.31 pt 乱值） | 见 spec §4 #11 |

---

## 文件结构

```
.claude/skills/mcm-figure-choose/
├─ SKILL.md                     # 短契约（<150 行，硬上限由校验强制）
└─ references/
   ├─ house-style.md            # ★ 唯一权威：13 条规范条目，逐条带来源标记 + 违反判据
   ├─ chart-types.md            # 决策树：9 个数据关系入口 + 题型索引 + radar 低频标注
   └─ provenance.md             # 每个数的口径 / 复跑命令 / 样本范围
tests/skills/figure-choose/
├─ check-figure-style.py        # 产物判据：图宽比 / 主色数 / 图注形态（fail-closed）
├─ check-spec-pointers.py       # 引用完整性：plot skill 必须指向规范、且不许重述规范数值
├─ mutate-figure-style.py       # 变异驱动器（落盘，一条命令全跑）
├─ fixtures/                    # 合格/违规样本 + expected.tsv
├─ red/                         # RED 场景（brief + 产物 + 判词 + README）
├─ green/                       # GREEN 场景（同一场景 + skill）
└─ *.txt                        # 放行证据（逐字）
```
**边界说明**：`check-figure-style.py` 只判"产出的图+图注"（实现层产物）；`check-spec-pointers.py` 只判"仓库里各 skill 是否守了指针纪律"（交付物层）。二者不互相调用、不共享状态。

---

### Task 1: 产物判据检查器 + 变异证明

**Files:**
- Create: `tests/skills/figure-choose/check-figure-style.py`
- Create: `tests/skills/figure-choose/fixtures/`（`ok-*.png` ×3、`bad-*.png` ×3、`expected.tsv`、`make-fixtures.py`）
- Create: `tests/skills/figure-choose/mutate-figure-style.py`
- Create: `tests/skills/figure-choose/figure-style-baseline.txt`（放行证据）

**Interfaces:**
- Consumes: 无（本任务是尺子本身）
- Produces（后续任务要照此调用）：
  `python tests/skills/figure-choose/check-figure-style.py --fig <path> --caption <text|@file> --textwidth-in <float> [--dpi <int>] [--json]`
  · 退出码：`0` 全 PASS · `1` 有 FAIL · `2` 参数/参照缺失（**fail-closed**）
  · 判据 ID：`F1` 图宽比 ∈[0.80,1.20] · `F2` 彩色主色数 ≤4 · `F3a` 图注以 `Figure <n>:` 起 · `F3b` 词数 ≤12（>17 硬失败）· `F3c` 句末无句号 · `F3d` 图注非空
  · 末行固定为 `RESULT: PASS` 或 `RESULT: FAIL`

- [ ] **Step 1: 先做 fixtures（含"预期违规"的样本）与期望表**

`make-fixtures.py` 生成 6 张图 + `expected.tsv`（Python + Pillow，尺寸直接写 px，dpi 钉死 200）：

```python
# tests/skills/figure-choose/fixtures/make-fixtures.py
"""生成判据 fixtures。用途：让检查器的每条判据都有一个'必须红'的样本。"""
import io, pathlib
from PIL import Image, ImageDraw
D = pathlib.Path(__file__).parent

def fig(name, w_in, h_in, colors):
    """按 200 dpi 出图：w_in*200 px 宽。colors=彩色主色列表（外加大片白底）。"""
    px, py = int(w_in*200), int(h_in*200)
    im = Image.new("RGB", (px, py), "white"); d = ImageDraw.Draw(im)
    band = py // (len(colors) + 1)
    for i, c in enumerate(colors):
        d.rectangle([0, band*(i+1), px, band*(i+2)], fill=c)   # 每色占 ~1/(n+1) 面积
    im.save(D/name, dpi=(200, 200))

# 合格：6.0in 宽（正文 6.31in ⇒ 比值 0.951），3 色
fig("ok-01.png", 6.0, 2.6, ["#4477AA", "#EE6677", "#228833"])
fig("ok-02.png", 5.1, 2.6, ["#4477AA"])                       # 0.808，单色
fig("ok-03.png", 6.3, 3.0, ["#4477AA", "#EE6677", "#228833", "#CCBB44"])  # 0.999，4 色
# 违规：各只踩一条
fig("bad-f1-too-narrow.png", 4.4, 2.6, ["#4477AA"])           # 0.697 < 0.80
fig("bad-f1-too-wide.png",   7.8, 3.0, ["#4477AA"])           # 1.236 > 1.20
fig("bad-f2-five-colors.png", 6.0, 2.6,
    ["#4477AA", "#EE6677", "#228833", "#CCBB44", "#66CCEE", "#AA3377"])  # 6 色
```

`expected.tsv`（**判据 → 期望**，逐格写死；`--` 表示该样本该条不适用于本任务）：

```
sample	criterion	expected
ok-01.png	F1	PASS
ok-01.png	F2	PASS
ok-02.png	F1	PASS
ok-03.png	F2	PASS
bad-f1-too-narrow.png	F1	FAIL
bad-f1-too-wide.png	F1	FAIL
bad-f2-five-colors.png	F2	FAIL
```
图注类判据（F3a–F3d）用**文本 fixture**，写进 `expected.tsv` 同表，`sample` 列写 `caption:<n>`：
`caption:1` = `Figure 1: Calibrated wear depth versus sliding distance.`（→ 4 条全 PASS）·
`caption:2` = `Figure 2: We show the calibrated wear depth versus sliding distance for all six groups, including the sensitivity band at the 95 percent level.`（15 词 >12 **且** >17 ⇒ F3b FAIL）·
`caption:3` = `Figure 3: Model structure.`（末字符 `.` ⇒ F3c FAIL）·
`caption:4` = `Figure 4:`（空 ⇒ F3d FAIL）。

- [ ] **Step 2: 写检查器，先让它跑起来就红（fixtures 已在，实现未写）**

先跑：`python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/fixtures/ok-01.png --caption "Figure 1: A test." --textwidth-in 6.31`
Expected: 报 `FileNotFoundError`/`NotImplementedError` 之类 ⇒ **这一步只是确认"它还不存在"**。

- [ ] **Step 3: 实现检查器（完整代码）**

```python
# tests/skills/figure-choose/check-figure-style.py
"""mcm-figure-choose 产物判据。只读被测图，不改任何东西。fail-closed。"""
import argparse, json, re, sys, pathlib
import fitz                      # PyMuPDF
from PIL import Image

F1_LO, F1_HI = 0.80, 1.20        # spec house-style #1（实测 p25 / max）
F2_MAX = 4                       # spec #4（实测中位 3）
CAP_MAX, CAP_HARD = 12, 17       # spec #9（实测 p95 / 全样本上界）

def color_count(im):
    """彩色主色数：去掉近黑/近白/近灰，只数占比 >=0.5% 的颜色。"""
    im = im.convert("RGB").resize((320, 320))          # 与分辨率无关
    tot, keep = 320*320, {}
    for cnt, (r, g, b) in im.getcolors(tot):
        if max(r, g, b) - min(r, g, b) < 24:           # 近灰（含黑/白）
            continue
        keep[(r//16, g//16, b//16)] = keep.get((r//16, g//16, b//16), 0) + cnt
    return sum(1 for c in keep.values() if c/tot >= 0.005)

def fig_width_in(path, dpi):
    """图宽（英寸）。优先用 PDF 页盒（矢量、精确）；PNG 走 --dpi（必须显式给）。"""
    if path.suffix.lower() == ".pdf":
        p = fitz.open(path)[0]
        return p.rect.width / 72.0
    if dpi is None:
        sys.exit("FAIL F1: PNG 需要显式 --dpi（PNG 的 dpi 元信息不可信，见 provenance）")
    with Image.open(path) as im:
        return im.size[0] / dpi

def check(fig, caption, textwidth_in, dpi):
    res = []
    if textwidth_in <= 0:
        sys.exit("FAIL: --textwidth-in 必须为正（fail-closed）")
    ratio = fig_width_in(fig, dpi) / textwidth_in
    res.append(("F1", F1_LO <= ratio <= F1_HI, f"图宽比 {ratio:.3f}（分母 {textwidth_in:.2f} in）"))
    with Image.open(fig) as im:
        n = color_count(im)
    res.append(("F2", n <= F2_MAX, f"彩色主色数 {n}"))
    cap = caption.strip()
    res.append(("F3a", bool(re.match(r"^Figure\s+\d+\s*:", cap)), "图注以 `Figure N:` 起"))
    words = len(cap.split())
    res.append(("F3b", words <= CAP_MAX, f"图注词数 {words}（上限 {CAP_MAX}，硬上限 {CAP_HARD}）"))
    if words > CAP_HARD:
        res[-1] = ("F3b", False, f"图注词数 {words} 超硬上限 {CAP_HARD}")
    res.append(("F3c", not cap.endswith("."), "句末不加句号"))
    res.append(("F3d", words > 0, "图注非空"))
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fig", required=True); ap.add_argument("--caption", required=True)
    ap.add_argument("--textwidth-in", type=float, required=True); ap.add_argument("--dpi", type=int)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    p = pathlib.Path(a.fig)
    if not p.exists():
        sys.exit(f"FAIL: 图不存在 {a.fig}（fail-closed）")
    cap = pathlib.Path(a.caption[1:]).read_text(encoding="utf-8") if a.caption.startswith("@") else a.caption
    res = check(p, cap, a.textwidth_in, a.dpi)
    for cid, ok, why in res:
        print(f"{'PASS' if ok else 'FAIL'}  {cid}  {why}")
    bad = [c for c, ok, _ in res if not ok]
    print(f"RESULT: {'PASS' if not bad else 'FAIL'}" + ("" if not bad else f"（{','.join(bad)}）"))
    if a.json:
        print(json.dumps({c: ok for c, ok, _ in res}, ensure_ascii=False))
    sys.exit(0 if not bad else 1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 用 fixtures 逐条验收（合格组全绿、违规组指定条红）**

`tests/skills/figure-choose/fixtures/run-expected.py`（**逐格比对**，读 `expected.tsv`）：

```python
# tests/skills/figure-choose/fixtures/run-expected.py
"""逐格验收：对 expected.tsv 的每一行跑一次检查器，比对期望。
captions.tsv 存图注文本 fixture（sample 列写 caption:<n>）。"""
import pathlib, subprocess, sys
D = pathlib.Path(__file__).parent
CHK = D.parent / "check-figure-style.py"
CAPS = {n: t.strip() for n, t in
        (l.split("\t", 1) for l in (D/"captions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())}
bad = total = 0
for line in (D/"expected.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    if not line.strip():
        continue
    sample, crit, want = line.split("\t")
    total += 1
    if sample.startswith("caption:"):
        cmd = [sys.executable, str(CHK), "--fig", str(D/"ok-01.png"),
               "--caption", CAPS[sample.split(":")[1]], "--textwidth-in", "6.31", "--dpi", "200"]
    else:
        cmd = [sys.executable, str(CHK), "--fig", str(D/sample),
               "--caption", "Figure 1: A test figure caption.", "--textwidth-in", "6.31", "--dpi", "200"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    got = "PASS" if f"PASS  {crit} " in out else "FAIL"
    # 图注 fixture 的 F1/F2 不适用（借用 ok-01），只核它们自己那条判据
    if sample.startswith("caption:") and crit not in ("F3a", "F3b", "F3c", "F3d"):
        total -= 1; continue
    flag = "OK" if got == want else "MISMATCH"
    bad += flag == "MISMATCH"
    print(f"{flag:9} {sample:24} {crit:4} want={want:4} got={got}")
print(f"MISMATCH {bad} / {total}")
sys.exit(0 if bad == 0 else 1)
```

Run: `python tests/skills/figure-choose/fixtures/run-expected.py`
Expected: `MISMATCH 0 / 12`（12 = 图中 7 + 图注 5；若条数不同，以 `expected.tsv` 实际行数为准并打印）。**`MISMATCH 0` 才算过。**

- [ ] **Step 5: 变异证明（每条判据都要有"必须红"的变异）**

`mutate-figure-style.py` 用 `write_bytes` 改**副本**（fixtures 目录下 `_mut/`），执行以下 6 条并断言每条都使对应判据转 FAIL，跑完**逐字节还原**并以 `git hash-object` 自证：

| 变异 | 手法 | 必须变红的判据 |
| :--- | :--- | :--- |
| M1 | 把 `F1_HI` 从 1.20 改成 0.90 | `bad-f1-too-wide` 之外的 **`ok-01` 也红**（证阈值真参与判定） |
| M2 | 把 `F1_LO/F1_HI` 互换写成 `F1_LO > F1_HI` | 所有 F1 全红（证区间判据不是恒真） |
| M3 | 删掉 `--dpi` 时走 PNG 分支的 `sys.exit` | PNG 无 dpi 时**不再 fail-closed** ⇒ 该条自检红 |
| M4 | 把 `color_count` 的 `>= 0.005` 改成 `>= 0.0` | `ok-02` 单色图仍绿、但 `bad-f2-five-colors` 必红（证它不是恒 FAIL） |
| M5 | 把 `CAP_MAX` 从 12 改成 99 | `caption:2`（15 词）由 FAIL 转 PASS ⇒ 对照显示该判据有效 |
| M6 | 把 `F3c` 的 `not cap.endswith(".")` 取反 | `ok` 组图注转红、`caption:3` 转绿 ⇒ 方向确实被检 |

Run: `python tests/skills/figure-choose/mutate-figure-style.py`
Expected: 每条打印 `RED-OK <Mi>`，末行 `MUT: 6/6 红`，并打印 `git hash-object` 还原自证。

- [ ] **Step 6: 写放行证据并提交**

`figure-style-baseline.txt`：贴入 Step 4 与 Step 5 的**逐字输出** + `git status --short`（须空）+ 三个文件的 `hash-object`。

```bash
git add tests/skills/figure-choose/
git commit -m "test(figure-choose): 产物判据检查器（F1/F2/F3a-d）+ fixtures 逐格验收 + 6 条变异证明"
```

---

### Task 2: RED 场景备料与 RED 基线

**Files:**
- Create: `tests/skills/figure-choose/red/{brief-R1.md,brief-R2.md,brief-R3.md}`（**只给场景正文**）
- Create: `tests/skills/figure-choose/red/{out-R1.,out-R2.,out-R3.}*`（RED 产物：脚本 + 图 + 图注）
- Create: `tests/skills/figure-choose/red/judge.md`（判者的判断题记录）
- Create: `tests/skills/figure-choose/red/README.md`（含"**本目录含泄题风险文件，绝不给写手**"警示）
- Create: `tests/skills/figure-choose/red/red-evidence.md`（机械层读数，逐字）

**Interfaces:**
- Consumes: Task 1 的 `check-figure-style.py`（**RED 的机械层读数就用它**）
- Produces: `red/README.md` 里固定的 RED 场景正文（Task 6 的 GREEN 必须**逐字复用**同一份场景）

- [ ] **Step 1: 写三份场景 brief（只给场景，不给期望）**

三份都要**只有数据与问题**，不得出现"你应该画什么图""注意图宽"这类提示（通则 8）。

- **R1（构成数据）**：`六个分区在三档脆弱性下的面积占比：A 区 0.42/0.35/0.23，B 区 0.31/0.44/0.25，C 区 0.55/0.30/0.15，D 区 0.28/0.47/0.25，E 区 0.37/0.38/0.25，F 区 0.50/0.33/0.17`；问题："说明各区脆弱性构成，并支持'哪两个区结构最接近'的判断"。（压**饼图**这条：实测 n=120 里 0 张）
- **R2（多变量对比/相关）**：`六个分区的人口密度、平均坡度、植被覆盖率、历史受灾次数、基础设施指数（5 列 × 6 行，数值给出）`；问题："找出与受灾次数最相关的因子，并说明分区之间的相似性"。（压**图型选择与多面板**）
- **R3（交付形态）**：`承 R1 的数据`，题面只加一句："产出一张可直接放进论文的图（含图注），我需要能直接贴进正文。"（压**图宽 / 配色 / 图注形态**）

- [ ] **Step 2: 派 RED subagent（不带任何提示）**

对每份 brief 派一个独立 subagent，提示词**只有**：`按这份 brief 产出图与图注，脚本与产物写到 <路径>。` **不得**提到 skill、规范、图宽、配色、饼图。
要求产物**可复算**：脚本 + 导出的 PNG/PDF + 图注文本，三者都入库。

- [ ] **Step 3: 跑机械层判据（同一把尺）**

对每份产物：`python tests/skills/figure-choose/check-figure-style.py --fig <产物> --caption @<图注文件> --textwidth-in 6.31 --dpi <导出 dpi>`
把**逐字输出**贴进 `red/red-evidence.md`，并给一张 `R1/R2/R3 × F1/F2/F3a-d` 的红绿表。
Expected（RED 的**典型**失败形态）：至少 R3 的 F1 与 F3c 红、R1 可能选饼图（F2 未必红，因为饼图也常 ≤4 色 ⇒ **这正是"机械层抓不到判断题"的现场证据**）。

- [ ] **Step 4: 判断层判读（独立判者，不看 skill）**

派一位**独立判者**读三份产物（**只读产物**），逐份回答：图型选得对不对（对/部分对/错）+ 理由 + 是否违反"构成数据不用饼图"这条。
判词写 `red/judge.md`（逐字），**不许**让判者看 `house-style.md`。

- [ ] **Step 5: 提交 RED 基线**

```bash
git add tests/skills/figure-choose/red/
git commit -m "test(figure-choose): RED 基线（3 场景 × 机械层/判断层两层判据）"
```

---

### Task 3: `house-style.md` + `provenance.md`（规范正文与出处）

**Files:**
- Create: `.claude/skills/mcm-figure-choose/references/house-style.md`
- Create: `.claude/skills/mcm-figure-choose/references/provenance.md`
- Create: `tests/skills/figure-choose/check-house-style.py`（**规范里每个数的守卫**）
- Modify: `tests/skills/figure-choose/mutate-figure-style.py`（追加规范数守卫的变异）

**Interfaces:**
- Consumes: Task 1 的 `check-figure-style.py` 的常量（`F1_LO/F1_HI/F2_MAX/CAP_MAX/CAP_HARD`）
- Produces: `house-style.md` 的 **13 条条目 ID**（`H1..H13`），Task 5 的 SKILL.md 与 Task 7 的指针检查器都引用这些 ID

- [ ] **Step 1: 写 `house-style.md`，13 条逐条落文**

**文件头必须写**：样本范围（2025 单年 43 份 / 662 图 / O 奖无对照组 / 其余 158 份未抽取）· 三条"不许吹"的措辞下限 · 与 `provenance.md` 的分工。
每条格式固定：`### H<n>. <标题>` + `规则` + `来源`（**实测** / **规范性〔社区〕** / **量不到**）+ `依据` + `违反判据` + `复跑命令`。
内容**照 spec §4 的 13 条落地**（逐条复制，不得改写数值）：

| ID | 标题 | 来源 |
| :--- | :--- | :--- |
| H1 | 图宽：0.95–1.0× 正文宽，不窄于 0.80×，不超过 1.2× | 实测 |
| H2 | 分母口径：正文栏宽 = 该篇正文行宽 p90（明确写死） | 实测 |
| H3 | 横向、宽高比 2–3；图高 2.6 in 量级 | 实测 |
| H4 | 彩色主色 ≤4；单色/灰度是正常选择 | 实测 |
| H5 | 不用默认色序（措辞上限：**"未观察到广泛使用"**） | 实测定下界 |
| H6 | 不用饼图 | 实测（n=120 里 0 张） |
| H7 | 3D 图可用但少用 | 实测（判据读数 9.2%） |
| H8 | 多面板是常态（**只能当上界**） | 实测（上界） |
| H9 | 图注模板：`Figure N:` + ASCII 冒号 · ≤12 词（硬上限 17）· 句末无句号 · 必须自足 | 实测 |
| H10 | 坐标轴：去顶右框线、刻度方向、轴标签带单位 | **规范性〔社区〕** |
| H11 | 网格线/图例/双 Y 轴：**本规范暂不覆盖**（写明理由） | 未覆盖 |
| H12 | 字号 = 正文 0.8–1.0×、最小 ≥7 pt；线宽与字体族随正文 | **规范性〔社区〕，非实测** |
| H13 | 参照分布 ≠ 判据（"像不像获奖论文"从来不是判据） | 口径纪律 |

- [ ] **Step 2: 写 `provenance.md`（每个数的口径与复跑命令）**

逐条给：`数` · `口径`（含**分母定义**）· `复跑命令`（可直接粘进 bash 的完整命令，含 `PYTHONPATH` 或相对路径）· `样本范围` · `已知偏差`（如"算的是渲染带宽，非图 bbox"）。

- [ ] **Step 3: 写 `check-house-style.py`——**规范里每个数的守卫**（**表驱动**，故可在 Step 1 之后一次写成）**

设计：一张 `GUARDS` 表，每行 `(条目 ID, 文档里那个数的正则, 复算函数, 容差)`。**期望值一律从文档现取，不许抄进脚本**；抽不到 ⇒ FAIL（fail-closed）。

```python
# tests/skills/figure-choose/check-house-style.py  （骨架：runner 完整，条目按 H1..H12 逐条补）
import re, pathlib, statistics as st, sys, glob
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parents[3]
DOC  = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
FIGS = sorted(glob.glob(str(ROOT / "corpus/papers/figures/**/fig-*.png"), recursive=True))

def doc_num(pattern):
    """从 house-style.md 现取一个数；抽不到就抛（fail-closed）。"""
    m = re.search(pattern, DOC.read_text(encoding="utf-8"))
    if not m:
        raise LookupError(f"house-style.md 里抽不到：{pattern}")
    return float(m.group(1))

def ratios():
    vals = [Image.open(f).size[0] / 200.0 / 6.31 for f in FIGS]      # 分母：逐篇 p90 的全局中位（H2 写死）
    return sorted(vals)

def colors():
    out = []
    for f in FIGS:
        im = Image.open(f).convert("RGB").resize((320, 320))
        tot = 320*320; keep = {}
        for cnt, (r, g, b) in im.getcolors(tot):
            if max(r, g, b) - min(r, g, b) < 24: continue
            k = (r//16, g//16, b//16); keep[k] = keep.get(k, 0) + cnt
        out.append(sum(1 for c in keep.values() if c/tot >= 0.005))
    return out

TOL = 0.02      # 比值类容差（两位小数）
GUARDS = [
    ("H1-hi",  r"不超过\s*\*\*([\d.]+)×\*\*", lambda: max(ratios()),   TOL),
    ("H1-lo",  r"不窄于\s*\*\*([\d.]+)×\*\*", lambda: min(ratios()),   TOL),
    ("H1-med", r"比值中位\s*([\d.]+)",        lambda: st.median(ratios()), TOL),
    ("H4-med", r"主色\s*≤\s*(\d+)",           lambda: st.median(colors()), 0.5),
    # ↑ H2/H3/H6/H8/H9 照此逐条补；每条都要有一个"文档改坏即红"的变异（见 Step 4）
]

bad = 0
for gid, pat, recompute, tol in GUARDS:
    want, got = doc_num(pat), recompute()
    ok = abs(want - got) <= tol
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'}  {gid}  文档={want:g}  实测={got:g}  容差={tol:g}")
print(f"RESULT: {'PASS' if not bad else 'FAIL'}")
sys.exit(0 if not bad else 1)
```

**必须覆盖**：H1 的三个比值端点 · H3 的宽高比与图高 · H4 的主色中位数与零彩色占比 · H6 的饼图 0 · H9 的词数三点与 ASCII 冒号占比 · H7/H8 的读数。
正则对不上就先改**正则**（不是改数）——**文档是权威，脚本是尺子**。

- [ ] **Step 4: 变异证明（4 条）**

| 变异 | 手法 | 必须红 |
| :--- | :--- | :--- |
| M7 | 把 `house-style.md` 里 H1 的 `1.20` 改成 `9.99` | `check-house-style.py` 红 |
| M8 | 把 H9 的 `12` 改成 `3` | 红 |
| M9 | 删掉 H4 那一行 | 红（抽不到数 ⇒ fail-closed） |
| M10 | 把 `provenance.md` 里某条命令的分母从 `p90` 改成 `mean` | 该条重算值与文档不符 ⇒ 红 |

Run: `python tests/skills/figure-choose/mutate-figure-style.py`（追加后一条命令跑全部）
Expected: `MUT: 10/10 红`

- [ ] **Step 5: 证据与提交**

把 Step 3/4 的逐字输出写进 `tests/skills/figure-choose/house-style-verify.txt`。

```bash
git add .claude/skills/mcm-figure-choose/references/ tests/skills/figure-choose/
git commit -m "feat(figure-choose): house-style 13 条 + provenance（每数带口径与复跑命令）+ 规范数守卫 10/10 变异红"
```

---

### Task 4: `chart-types.md`（决策树）

**Files:**
- Create: `.claude/skills/mcm-figure-choose/references/chart-types.md`
- Modify: `tests/skills/figure-choose/check-house-style.py`（追加结构守卫）
- Create: `tests/skills/figure-choose/chart-types-verify.txt`（证据）

**Interfaces:**
- Consumes: `house-style.md` 的 `H1..H13` ID；`corpus/papers/PROBLEM_TYPES.md`（67 题题型标注，**只读**）
- Produces: 决策树的 **9 个入口名**（`比较 / 分布 / 相关 / 构成 / 时序 / 空间 / 流程 / 机理 / 不确定性`），Task 5 的 SKILL.md 依赖这些入口名

- [ ] **Step 1: 写决策树**

按 9 个**数据关系**入口组织，每题固定四段：`你手上是什么数据` → `首选图型` → `备选` → `禁忌（含理由）`。
**不按题型组织**；末尾加一条**题型索引**：指向 `corpus/papers/PROBLEM_TYPES.md`，说明"题型→通常给什么数据"的反查路径。
**radar 立类但标低频**（规则层 5 次 `Radar chart` 全被 `line` 兜住；判断层 1/120）。
**每个图型名必须出现且只出现一次定义**（守卫要能数出来）。

- [ ] **Step 2: 结构守卫（机械可判的部分）**

追加到 `check-house-style.py`，用**同一表驱动结构**（`STRUCT_GUARDS = [(id, 断言函数, 说明), ...]`）：

```python
CT = ROOT / ".claude/skills/mcm-figure-choose/references/chart-types.md"
ENTRIES = ["比较", "分布", "相关", "构成", "时序", "空间", "流程", "机理", "不确定性"]

def struct_guards():
    txt = CT.read_text(encoding="utf-8")
    nums_doc = set(re.findall(r"\d+\.\d+", DOC.read_text(encoding="utf-8")))   # 规范里的实测数（现取）
    out = []
    out.append(("S1 入口齐全", all(f"### {e}" in txt or f"「{e}」" in txt for e in ENTRIES),
                "九个入口名缺一即红"))
    out.append(("S2 四段齐全", txt.count("首选图型") >= len(ENTRIES) and txt.count("禁忌") >= len(ENTRIES),
                "每个入口都要有 首选/备选/禁忌"))
    out.append(("S3 radar 低频", bool(re.search(r"radar[^\n]*低频|低频[^\n]*radar", txt, re.I)),
                "radar 必须带低频标注"))
    out.append(("S4 无重复定义", len(re.findall(r"^\s*\|?\s*\*\*([A-Za-z0-9\- ]+)\*\*\s*[:：]", txt, re.M)),
                "图型名重复定义要人看一眼——此条先印计数，>0 时由人判"))
    out.append(("S5 数值不漂", all(n in nums_doc for n in re.findall(r"\d+\.\d+", txt)),
                "chart-types 里的实测数必须与 house-style 同值"))
    return out
```

① 9 个入口名**全部存在**（缺一即 FAIL）；② 每个入口下**四段齐全**；③ `radar` 条目**带"低频"标注**；④ 图型名**重复定义**先印计数（S4 是"读数条"，**不得**充当判据——本项目"判据看起来可失败实则恒真"的教训）；⑤ **文件里凡出现实测数字，必须能在 `house-style.md` 找到同值**（防重述时改数）。

- [ ] **Step 3: 变异证明（3 条）**

| 变异 | 手法 | 必须红 |
| :--- | :--- | :--- |
| M11 | 删掉一个入口（如"不确定性"） | 红 |
| M12 | 删掉 `radar` 的"低频"标注 | 红 |
| M13 | 把某条参照分布的数改成与 `house-style.md` 不同 | 红 |

Run: `python tests/skills/figure-choose/mutate-figure-style.py`  → Expected `MUT: 13/13 红`

- [ ] **Step 4: 提交**

```bash
git add .claude/skills/mcm-figure-choose/references/chart-types.md tests/skills/figure-choose/
git commit -m "feat(figure-choose): 图型决策树（9 入口 + 题型索引 + radar 低频）+ 结构守卫 13/13 红"
```

---

### Task 5: `SKILL.md`（短契约）

**Files:**
- Create: `.claude/skills/mcm-figure-choose/SKILL.md`
- Modify: `tests/skills/figure-choose/check-house-style.py`（追加 SKILL.md 守卫）
- Create: `tests/skills/figure-choose/skill-verify.txt`（证据）

**Interfaces:**
- Consumes: `H1..H13`、9 个入口名
- Produces: SKILL.md 里的**指针行**（Task 7 的检查器要核它存在且指向 `references/house-style.md`）

- [ ] **Step 1: 写 SKILL.md（<150 行）**

必须含：**何时用**（触发词：选图型/画什么图/这个数据该用什么图/图被评委说看不明白）· **决策树入口**（9 个入口名 + 怎么问用户）· **输出契约**（推荐图型 + 理由 + 落到 `H<n>` 的设计要点）· **边界**（不产代码 → 指向 `mcm-plot-*`；不做全自动合规检查）· **指针**（规范在 `references/house-style.md`，**本文件不重述任何规范数值**）。
**不得**在 SKILL.md 里出现 `0.951`/`1.20`/`≤4`/`12 词` 这类规范数值——**重述即违反 H13 的同族纪律**。

- [ ] **Step 2: 守卫**

```python
SK = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"

def skill_guards():
    txt = SK.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    banned = set(re.findall(r"\d+\.\d+", doc)) | set(re.findall(r"≤\s*\d+|<\s*\d+\s*词", doc))  # 规范里的数现取
    hits = sorted(b for b in banned if b in txt)
    return [
        ("K1 行数<150", len(txt.splitlines()) < 150, f"实际 {len(txt.splitlines())} 行"),
        ("K2 指针存在", "references/house-style.md" in txt or "house-style.md" in txt, "必须指向规范"),
        ("K3 不重述规范数值", not hits, f"命中禁用串 {hits}"),
        ("K4 九入口齐全", all(e in txt for e in ENTRIES), "九个入口名都要出现"),
    ]
```

① 行数 **<150**；② 含指向 `references/house-style.md` 的指针（**必须**）；③ **不含任何规范数值**（禁用串从 `house-style.md` **现取**，命中即 FAIL）；④ 9 个入口名全部出现。

- [ ] **Step 3: 变异证明（3 条）**

| 变异 | 手法 | 必须红 |
| :--- | :--- | :--- |
| M14 | 在 SKILL.md 里插入 `图宽用满 0.951×正文宽` | 红（重述规范数值） |
| M15 | 删掉指向 `house-style.md` 的指针行 | 红 |
| M16 | 把 SKILL.md 撑到 151 行 | 红 |

Run: `python tests/skills/figure-choose/mutate-figure-style.py` → Expected `MUT: 16/16 红`

- [ ] **Step 4: 提交**

```bash
git add .claude/skills/mcm-figure-choose/SKILL.md tests/skills/figure-choose/
git commit -m "feat(figure-choose): SKILL.md 短契约（不重述规范数值，指针唯一）+ 守卫 16/16 红"
```

---

### Task 6: GREEN 对照 + 独立复审

**Files:**
- Create: `tests/skills/figure-choose/green/{out-G1.,out-G2.,out-G3.}*`
- Create: `tests/skills/figure-choose/green/judge-green.md`
- Create: `tests/skills/figure-choose/green-evidence.md`（RED/GREEN 对照表，逐字）

**Interfaces:**
- Consumes: `red/README.md` 里那三份**逐字场景**（不许改写）；`check-figure-style.py`（**同一把尺，一字不改**）
- Produces: 对照表 `R1/R2/R3 × (机械层 · 判断层) × (RED · GREEN)`

- [ ] **Step 1: 派 GREEN subagent（同一场景 + 允许读 skill）**

对三份场景**逐字复用** brief，允许 agent 读 `.claude/skills/mcm-figure-choose/`（含 references）。
产物（脚本 + 图 + 图注）入 `green/`。**判者不得参与 GREEN 的写作**。

- [ ] **Step 2: 跑机械层（同一脚本、同一参数）**

命令与 Task 2 Step 3 **逐字相同**（只换被测产物路径）。逐字输出入 `green-evidence.md`，并给 RED/GREEN 并列红绿表。
**预期（GREEN 应改善）**：R3 的 F1 与 F3c 由红转绿；**若某条没改善，如实登记，不许调判据**。

- [ ] **Step 3: 判断层复审（独立判者，仍不看 skill）**

同一判者口径，重判 GREEN 三份；写 `green/judge-green.md`。
**并回答一个问题**：GREEN 的图型选择是不是**因为读了规范才对的**？（可判线索：产物里是否引用了 `H<n>`；若判不出，如实写"判不出"。）

- [ ] **Step 4: 对照结论与残余**

`green-evidence.md` 末尾写：改善了哪几条（逐字证据）· **没改善的逐条登记** · **不许把"没失败"算成"规范的功劳"**（两侧都通过、本次无区分力的条目要**单列**）。

- [ ] **Step 5: 提交**

```bash
git add tests/skills/figure-choose/green/ tests/skills/figure-choose/green-evidence.md
git commit -m "test(figure-choose): GREEN 对照（同场景/同判据）+ 独立复审，残余逐条登记"
```

---

### Task 7: 引用完整性检查器（机制先行）

**Files:**
- Create: `tests/skills/figure-choose/check-spec-pointers.py`
- Create: `tests/skills/figure-choose/fixtures/fake-skills/`（**假 plot skill**：一个带指针、一个不带、一个重述数值）
- Modify: `tests/skills/figure-choose/mutate-figure-style.py`
- Create: `tests/skills/figure-choose/pointer-verify.txt`

**Interfaces:**
- Consumes: `.claude/skills/*/SKILL.md` 的实际状态；`house-style.md` 现抽的规范数值表
- Produces: `python tests/skills/figure-choose/check-spec-pointers.py [--skills-dir <dir>]`，退出码 `0/1`，末行 `RESULT: PASS|FAIL`

- [ ] **Step 1: 写检查器（三条规则）**

① **凡存在 `mcm-plot-*` / `mcm-table` / `mcm-schematic`，其 SKILL.md 必须含指向 `mcm-figure-choose/references/house-style.md` 的指针**（缺则 FAIL）；
② **任何 skill（除 `mcm-figure-choose` 自身）不得出现 `house-style.md` 的规范数值**（重述即 FAIL）；
③ **fail-closed**：`--skills-dir` 不存在 ⇒ FAIL；`house-style.md` 抽不出数 ⇒ FAIL。
**必须支持 `--skills-dir`**，以便用假 skill 做变异（真 plot skill 尚未建，**否则此检查器恒真**）。

- [ ] **Step 2: 用假 skill 做变异证明（4 条）**

`fixtures/fake-skills/` 下建三份最小 SKILL.md：`fake-ok/SKILL.md`（含指针、无数值）· `fake-nopointer/SKILL.md`（缺指针）· `fake-restate/SKILL.md`（含 `1.20` 与 `0.951`）。
| 变异 | 手法 | 必须红 |
| :--- | :--- | :--- |
| M17 | `--skills-dir fixtures/fake-skills` 整体跑（应含 `fake-nopointer` 与 `fake-restate`） | 红，且**分别点名两条规则** |
| M18 | 只留 `fake-ok` 再跑 | **绿**（证它不是恒 FAIL） |
| M19 | 把 `house-style.md` 抽数的正则改坏 | 红（fail-closed） |
| M20 | `--skills-dir` 指向不存在目录 | 红（非零退出） |

Run: `python tests/skills/figure-choose/mutate-figure-style.py` → Expected `MUT: 20/20 红`

- [ ] **Step 3: 对真实仓库跑一次并登记现状**

Run: `python tests/skills/figure-choose/check-spec-pointers.py`
Expected: 现存的 4 个 skill 里**没有** `mcm-plot-*` ⇒ 规则①无对象；但**必须实测确认**并把这个"当前无对象"**写进证据**（否则它就是"恒真判据"）。
**并把"待 `mcm-plot-*` 出现时本检查器即生效"这条登记进 `docs/mcm-suite-todo.md` §C 的 M3 行**（改冻结区需先报用户）。

- [ ] **Step 4: 提交**

```bash
git add tests/skills/figure-choose/
git commit -m "test(figure-choose): 引用完整性检查器（假 skill 变异 20/20 红，防恒真）"
```

---

## 自查（写完后对 spec 逐节核）

- spec §1 已裁决策 → Global Constraints 与任务落点全覆盖 ✔
- spec §2 职责与边界 → Task 5 Step 1 的 SKILL.md 边界段 ✔
- spec §3 交付形态 → 文件结构 ✔；**引用完整性机制 → Task 7** ✔
- spec §4 的 13 条 → Task 3 Step 1 的表逐条对齐 ✔；**决策树与 radar → Task 4** ✔
- spec §5 判据与 RED/GREEN → Task 1/2/6 ✔（机械层 + 判断层两层都在）
- spec §6 已知缺口 → Task 3 Step 1 的文件头要求 ✔
- 无占位符：每个 Step 都给了命令/代码/期望输出 ✔
- 命名一致：`F1/F2/F3a-d`（产物判据）· `H1..H13`（规范条目）· 9 个入口名（决策树）· `M1..M20`（变异）✔

## 未决（需用户裁决后才可动）

1. **Task 7 Step 3 要改 `docs/mcm-suite-todo.md`**（冻结区）——派发前先报批。
2. **RED 场景的数据是合成还是取自 `corpus/官方原题/`** —— 默认用合成（brief 里那几组数），若你要求用真题数据，派发前改 brief。
