#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/figure-choose/check-figure-style.py` 的**变异驱动器**——一条命令复跑全部变异。

用法：  python tests/skills/figure-choose/mutate-figure-style.py

## 为什么必须落盘

本仓已栽过**六次**"判据在什么都没验的情况下报绿"。变异驱动器**入库**才能让复核员
独立复现"它真的会红"这句话；不落盘的变异等于自称。

## 每条变异做什么

1. 读检查器的**原始字节**（`rb`），在内存里做**一次**字面替换
   （替换次数必须恰为 1，否则驱动器自己报错）；
2. 用 `write_bytes` 把变异体写到 `fixtures/_mut/`（**改副本，原文件全程不碰**；
   全仓禁用 `write_text`——Windows 上会把 LF 写成 CRLF）；
3. 对**同一批 fixture**分别跑**原检查器**与**变异体**，逐条断言"该红的那条真的翻了"；
4. 跑完清空 `_mut/`，并用 **`git hash-object`** 自证检查器逐字节没变，最后复跑一遍
   逐格验收（`fixtures/run-expected.py`，exit 0）。

## 与任务书的差异（三处，均为实测逼出，逐条见输出里的 NOTE）

- **M4**：任务书写"改 0.005 → 0.0，断言 ok-02 仍绿、bad-f2 必红"——但**原 6 张 fixture 上
  这个变异一个读数都不变**（六张全等，NOTE 里逐张打印），那是个**证不了东西的变异**。
  故断言改锚在**新增的 ok-04.png**（4 主色 + 1 个 0.292% 的稀有彩色）上：地板一改，
  第 5 色被数出来 ⇒ 地板真的参与判定。
- **M5**：任务书说 `caption:2` 是 15 词、改 `CAP_MAX` 即由 FAIL 转 PASS。实测 `caption:2`
  是 **24 词**（`split()` 计数；F3b 现按正文口径数得 **22**），**超硬上限 17** ⇒ 只改
  `CAP_MAX` 时它**照样红**。
  故断言改锚在**新增的 `caption:5`（整条 15 / 正文 13 词）**上——只有它能把 `CAP_MAX` 单独证活。
- **M3**：任务书写"删掉 `sys.exit`"。实现里那条 fail-closed 走 `fail_closed()`（exit 2），
  故变异写成把 PNG 分支的守卫改成恒不成立（`if dpi is None:` → `if False:`），
  等价于删掉该守卫，且**只**动这一条路径。

## 复验补齐的三处（独立评审判定 M7/M8/P1，逐条见各行说明）

- **M7**（Important-1）：F2 的 **PDF 栅格化分支**是修完 PDF 崩溃后的新增分支，把它拆掉，
  PDF 立刻退回"`Image.open` 读 PDF"的老缺陷（rc=2、无判词）⇒ 该分支确实承重。
- **M8**（Important-3）：**F3a** 原先**没有任何"它能红"的证明**（`expected.tsv` 里 F3a 只有
  一条且是 PASS）⇒ 补一条谓词取反的变异 + 一条 `caption:6`（缺冒号）的 FAIL 行。
- **P1**（R-5）：`run-expected.py` 的 **ERROR 分支**（rc 异常/没打判词 ⇒ 记 ERROR、整轮非零退出）
  是新增分支 ⇒ 用一支"只在**期望 FAIL 的那一行** fail-closed"的变异体驱动它，证明
  **"没判成"不再被记成"判成红"**。

## 修复轮（独立评审 1 Critical + 3 Important + 4 Minor）新增的变异

- **M13–M19**：给修复轮**新写的每一个判据位**配回归位，逐条必须实测红。其中
  M13 打的是**已被证伪的 48.79**（Critical-1 的那句不实陈述在文档里的原位置）、
  M14 打的是连续色图闸门的箱数下限（Important-3 收紧的那条腿）、
  M17 打的是 H9 的宽口径条数 578（Important-4）、
  M18 打的是 `provenance.md` **散文**里的数（N-7）、
  M19 打的是 H12 的〔社区〕字号下限（N-8，原先改成 `≥6 pt` 一路全绿）。
- **C1 / C2 单独一组**：M9–M19 全走 `--only <id>`，而 `check-house-style.py` 的 **CENSUS 只在
  不带 `--only` 时才跑**（`if not want:`）⇒ 上面那些变异**一条都没验过 CENSUS**。这两条故意
  整份跑（`--no-provenance` 只为省掉 46 次子进程），断言的是 `CENSUS … 未入理由表 ≥1 个`：
  C1 往文档加一句带**整数**的话（原先整数被 `(r"\d+", …)` 兜底豁免，Important-2）、
  C2 把仪器实现常量 `quantize(32)` 改成 `quantize(99)`（证明上下文豁免表也不是万能兜底）。

## Task 4 新增的一组（`M22`–`M26` + 修复轮的 `M27`/`M28` + 读数条探针 `R1`）

这一组打的**不是** house-style / provenance，是 **`chart-types.md`**（图型决策树）的形状，
被验对象 = `check-house-style.py` 的**结构守卫** `S1`/`S2`/`S3`/`S5`。编号从 **`M22`** 起
（`M1`–`M8` 是检查器那一组、`M9`–`M19` 是规范数守卫那一组、`C1`/`C2` 是 CENSUS），
**不撞号**才引得住"哪条红了"。

- **`M22`**：入口 9 从『不确定性』**改名** ⇒ `S1` 红（八个名字对不上九个）。
  *只改标题不改块*，故 `S2` 不受影响 —— 这条专门把 `S1` **单独**证活。
- **`M23`**：删掉入口 1 的『**备选**』那一段 ⇒ `S2` 红（四段少一段），`S1` 不受影响。
- **`M24`**：删掉 **radar 定义行**上的『低频』⇒ `S3` 红。
  ⚠️ 任务书给的正则（**全文**扫 `radar` × `低频`）在本变异体上**仍然命中**（别的入口顺带提到
  radar 时也标了低频）⇒ 照任务书写法这条**不会红**。本实现把 `S3` 收紧成**只看 radar 的那条定义行**，
  逐条见该变异的 NOTE（NOTE 是**现算**的，不是抄进脚本的结论）。
- **`M25`**：把 3D 那条参照分布数 `9.2%` 改成 `9.3%` ⇒ `S5` 红（与 house-style 不同值）。
- **`M26`**：把两个小数**都**写成中文数字 ⇒ `S5` 抽不到任何小数 ⇒ 红（fail-closed：
  "把数全删光"不许成为转绿路径）。这条用**多替换**变体（`edits` 是列表）。
- **`R1`（读数条探针，不是判据变异）**：`S4` 只印计数、不进 `bad`（见检查器模块头第 5 条）。
  故它**没有"会红"可证**；这里证的是另一件事：**它真的在读数**（改坏副本上计数会动）
  **且从不改判词**（rc 恒 0、恒不出现 `PASS/FAIL  S4`）。一个"读数条"该有的两条性质都由一次运行钉住。
  （唯一例外见检查器模块头：`chart-types.md` **读不出**时它与其余结构守卫一起记红。）

## 修复轮（复审 N-2）新增的 `M27`/`M28`：`S5` 的归属口径

`S5` 原先只查"值 ∈ `house-style.md` ∪ `provenance.md` 的全局池"（123 个数，混着容差常量
`0.02/0.1/0.2` 与**别的 `H<n>` 条目**的数）——这是对任务书口径（"必须能在 `house-style.md` 找到同值"）
的**弱化**：往 3D 那条上写 `1.20`（H1 上限）或 `0.5`（H4 地板）照样绿。收紧为"**归到同行 `H<n>` 引用**
且 **∈ 该条目的数**"后，两条都要红（NOTE 里**现算**旧写法会怎么判）：

- **`M27`**：写进一个**池内但无所属**的数 `1.20`（H1 的上限）⇒ 新写法：该行没有 `H<n>` ⇒ 红。
- **`M28`**：把 `H7` 那条的数 `9.2` 换成 `0.5`（H4 的地板，池内）⇒ 新写法：`0.5 ∉ H7` ⇒ 红。

## Task 5 新增的一组（`M29`–`M41`）：`SKILL.md` 的短契约守卫 `K1`–`K8`

被验对象 = `check-house-style.py` 的 `SKILL_GUARDS`，文档 = `SKILL.md`（**短契约**）。
任务书给的 `M14`/`M15`/`M16` 与已占用的编号**撞号**，故顺延 **`M29`** 起（同 Task 3 那次顺延）。

- **`M29`**：写进一条规范数值（`0.951`）⇒ `K3`（现取禁止串）与 `K5`（数字的处置）**都**红。
  两条是**两道不同的闸**：`K3` 只认"规范里确实有的数"，`K5` 与禁止串表无关 —— 见该条的 NOTE。
- **`M30`**：**删掉指针行**、别处只留裸文件名 ⇒ `K2` 红。
  ⚠️ 任务书给的 `K2` 是 `"references/house-style.md" in txt or "house-style.md" in txt` ——
  `SKILL.md` 通篇要提规范，裸文件名**必然**还在 ⇒ **照任务书写法这条不会红**。本实现要求
  **skill 目录内的相对路径**（Task 7 的检查器要核的那个形态），逐条见该条 NOTE。
- **`M31`**：把文件撑到 151 行 ⇒ `K1` 红（短契约上限 `<150`）。
- **`M32`**：入口名『不确定性』改名 ⇒ `K4` 红（`ENTRIES` 是契约、缺一即红）。
- **`M33`**：把点名绘图 skill 的那行的 **〔拟建〕** 去掉 ⇒ `K6` 红（点名不存在的 skill 即错；
  `K6` 同时是 fail-closed：一个绘图 skill 都不点名也红 —— "不点名"不许成为转绿路径）。
- **`M34`**：打的是 **`house-style.md` 的副本**（`--doc` 指它）：把小数字面量与 `≤n` 形态全抹掉
  ⇒ `K3` 的"现取禁止串"**抽到空集** ⇒ 必须红（fail-closed）。不证这一臂，
  "抽不到即 FAIL"就只是注释里的一句话 —— 仪器取不到参照物却默认放行，正是本仓栽过的那一类。

### 修复轮（复审 1 Important + 6 Minor）新增的 `M35`–`M41`

- **`M35`**：`主色四色以内` 插进副本 ⇒ `K3` **中文数词臂**红（Important-1：主臂 `\d+(?:\.\d+)?`
  只认 ASCII/全角数字，**这四种中文写法原先整句走绿**；这条与 `M36` 各证一条臂）。
- **`M36`**：`图宽不超过一倍正文宽` 插进副本 ⇒ `K3` 红，**且由 NOTE 现算证明是"单位词臂"单独在红**
  （`一` < `SK_CN_BARE_MIN`=4 ⇒ 裸值臂不覆盖它）。
- **`M37`**：把 `4`（H4 的规范值）写进**声明行** ⇒ `K5` 红（N-2：旧写法下"声明行上的数自证"，
  写进那一行即被判"已声明"）。
- **`M38`**：删掉「输出契约」整段 ⇒ `K7` 红（N-3：这一段原先**没有任何机械存在性守卫**；
  NOTE 现算 `K1`–`K6` 在该副本上仍全绿）。
- **`M39`**：往决策树表里多加一行（= 多一个入口名）⇒ `K4` + `K5` 红（N-4：旧写法只查"九个名字
  出现过"，加一行不会红）。
- **`M40`**：`--skills-root` 指向一个**真存在** `mcm-plot-python/SKILL.md` 的临时根 ⇒ `K6` 红
  （N-5：只判单向的话，这个 skill 真建出来那天，守卫会强制保留一个已不成立的〔拟建〕）。
- **`M41`**：抹掉 `house-style.md` **副本**里 `H4` 的 `**验证**：` 行 ⇒ `K8` 红（N-7：
  `SKILL.md` 断言"逐条标了验证状态"，原先无人守）。

## Task 6 涟漪新增的一条（`M42`）

- **`M42`**：`check-figure-style.py` 的 **F3b 词数口径**由**正文**（去 `Figure N:` 标签）
  换回**整条** ⇒ 新增的口径锚 `caption:7`（整条 13 / 正文 11）由 PASS 转 FAIL。
  这是 Task 6 GREEN 对照 **Important-2** 的回归位：那一轮把 F3b 收敛到规范侧
  （`len(caption_body(cap).split())`，常量 12/17 与 `G-H9-*` 一个没动）。
  同批其余图注两口径同判 ⇒ 证不了口径，故**新增** fixture 与 expected 行，理由见 `m42` 的 docstring。
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sanitize(s):
    """证据里不写绝对路径：把本目录的绝对前缀剥掉。"""
    return s.replace(str(HERE) + os.sep, "").replace(str(HERE), "")


CHK = HERE / "check-figure-style.py"
FIX = HERE / "fixtures"
MUTD = FIX / "_mut"
CAPS = {n: t.strip() for n, t in
        (l.split("\t", 1) for l in (FIX / "captions.tsv").read_text(encoding="utf-8").splitlines() if l.strip())}
IMG_CAP = "Figure 1: A test figure caption"     # 无尾句号：图样本的判词只反映它自己要测的东西（R-7）
PDF_OK = "ok-05.pdf"                            # 4 色 PDF（F1/F2 全 PASS）
PDF_BAD = "bad-f2-five-colors.pdf"              # 6 色 PDF（F2 必红）
EXIT_FAIL_CLOSED = 2


# ---------------------------------------------------------------- 跑与读
def run_checker(checker, fig, caption, dpi="200"):
    cmd = [sys.executable, str(checker), "--fig", str(fig), "--caption", caption, "--textwidth-in", "6.31"]
    if dpi is not None:
        cmd += ["--dpi", dpi]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def verdict(out, crit):
    if f"PASS  {crit} " in out:
        return "PASS"
    if f"FAIL  {crit} " in out:
        return "FAIL"
    return "-"


def reader(checker):
    """返回 (图样本读数, 图注样本读数) 两个闭包，都绑定到同一个检查器。"""
    fig_v = lambda name, crit: verdict(run_checker(checker, FIX / name, IMG_CAP)[1], crit)
    cap_v = lambda n, crit: verdict(run_checker(checker, FIX / "ok-01.png", CAPS[n])[1], crit)
    return fig_v, cap_v


# ---------------------------------------------------------------- 断言
def m1(before, after, mp):
    """F1_HI 1.20 → 0.90：阈值真参与判定 ⇒ ok-01（0.951）也得红，ok-02（0.808）不受影响。"""
    b1, b2 = before[0]("ok-01.png", "F1"), before[0]("ok-02.png", "F1")
    a1, a2 = after[0]("ok-01.png", "F1"), after[0]("ok-02.png", "F1")
    return (b1 == "PASS" and a1 == "FAIL" and a2 == b2 == "PASS",
            f"ok-01 F1 {b1}→{a1}（比值 0.951 > 0.90）；ok-02 F1 {b2}→{a2}（0.808 ≤ 0.90，不受影响）")


def m2(before, after, mp):
    """F1_LO > F1_HI：区间判据不是恒真（原本全绿的三张合格图全红）。

    前置断言（R-6）：先要求三张合格图**变异前就是绿的**——否则"之后全 FAIL"这条断言
    在"它们本来就是红的"时也会通过，等于什么都没证。
    """
    rows = []
    for name in ("ok-01.png", "ok-02.png", "ok-03.png", "bad-f1-too-narrow.png", "bad-f1-too-wide.png"):
        b, a = before[0](name, "F1"), after[0](name, "F1")
        rows.append((name, b, a))
    ok = (all(a == "FAIL" for _n, _b, a in rows)
          and all(b == "FAIL" for n, b, _a in rows if n.startswith("bad-"))
          and all(b == "PASS" for n, b, _a in rows if n.startswith("ok-")))    # ← 前置：三张本就得是绿的
    return ok, "；".join(f"{n} {b}→{a}" for n, b, a in rows)


def m3(before, after, mp):
    """PNG 无 --dpi：必须**不判**（rc=2、无判词）；变异体把守卫换成"默认 200 硬着头皮判"。

    读法：变异体**印出了判词**（rc=1）⇒ 它不再拒绝判——这正是"拿不到参照就别判"这条
    契约被拆掉的证据。（若把守卫写成 `if False:`，变异体会被 D5 新加的通用兜底接住、
    仍退 2，只是报错变成 TypeError——那样这条变异就证不了"守卫承重"，故不取。）
    """
    rc0, out0, err0 = run_checker(CHK, FIX / "ok-01.png", IMG_CAP, dpi=None)
    rc1, out1, err1 = run_checker(mp, FIX / "ok-01.png", IMG_CAP, dpi=None)
    clean0 = rc0 == EXIT_FAIL_CLOSED and "RESULT:" not in out0 and "需要显式 --dpi" in err0
    clean1 = rc1 == EXIT_FAIL_CLOSED and "RESULT:" not in out1
    return (clean0 and not clean1,
            f"原检查器 exit={rc0} 拒绝判（'RESULT:' 未打印；stderr '{sanitize(err0).strip()[:40]}'）；"
            f"变异体 exit={rc1} 印出判词（'{out1.strip().splitlines()[-1][:40]}'）⇒ 守卫被拆掉")


def m4(before, after, mp):
    """噪声地板 0.005 → 0.0：ok-04 的稀有彩（0.292%）由"不算"变"算" ⇒ 地板真参与判定。"""
    b4, a4 = before[0]("ok-04.png", "F2"), after[0]("ok-04.png", "F2")
    b2, a2 = before[0]("ok-02.png", "F2"), after[0]("ok-02.png", "F2")
    bf, af = before[0]("bad-f2-five-colors.png", "F2"), after[0]("bad-f2-five-colors.png", "F2")
    same = "；".join(f"{n} {before[0](n,'F2')}→{after[0](n,'F2')}"
                    for n in ("ok-01.png", "ok-02.png", "ok-03.png", "bad-f1-too-narrow.png",
                              "bad-f1-too-wide.png", "bad-f2-five-colors.png"))
    return (b4 == "PASS" and a4 == "FAIL" and a2 == "PASS" and af == "FAIL",
            f"ok-04 F2 {b4}→{a4}（4 主色 + 0.292% 稀有彩：读数 4 → 5）；ok-02 F2 {b2}→{a2}；"
            f"bad-f2 F2 {bf}→{af}　NOTE/原 6 张 fixture 上此变异读数全等：{same}")


def m5(before, after, mp):
    """CAP_MAX 12 → 99：正文 13 词的 caption:5 由 FAIL 转 PASS ⇒ 词数上限真参与判定。

    注意 caption:2（正文 22 词）**不会**翻绿——它超硬上限 17，被 CAP_HARD 那条兜住（见输出 NOTE）。
    """
    b5, a5 = before[1]("5", "F3b"), after[1]("5", "F3b")
    b2, a2 = before[1]("2", "F3b"), after[1]("2", "F3b")
    return (b5 == "FAIL" and a5 == "PASS",
            f"caption:5（整条 15 / 正文 13 词）F3b {b5}→{a5}；"
            f"NOTE/caption:2（整条 24 / 正文 22 词）F3b {b2}→{a2}"
            f"（超正文硬上限 17，CAP_MAX 抬高也翻不了）")


def m6(before, after, mp):
    """F3c 取反：方向确实被检（合格图注转红、endswith('.') 的 caption:3 转绿）。"""
    b1, a1 = before[1]("1", "F3c"), after[1]("1", "F3c")
    b3, a3 = before[1]("3", "F3c"), after[1]("3", "F3c")
    return (b1 == "PASS" and a1 == "FAIL" and b3 == "FAIL" and a3 == "PASS",
            f"caption:1 F3c {b1}→{a1}（合格图注转红）；caption:3 F3c {b3}→{a3}（句末句号转绿）")


def m7(before, after, mp):
    """F2 的 PDF 栅格化分支（Important-1）：拆掉它 ⇒ PDF 退回"Image.open 读 PDF"的老缺陷。

    读法：原检查器对 ok-05.pdf 给出 F2 **判词**（PASS）；变异体**给不出任何判词**——
    rc=2、stdout 空。这不是"判成红"，是"根本没判成"，正是 F2 的 PDF 分支承重的证据。
    （PDF 上 F2 **真会红**另有入库样本兜着：`bad-f2-five-colors.pdf F2 FAIL`，见 expected.tsv。）
    """
    rc0, out0, _ = run_checker(CHK, FIX / PDF_OK, IMG_CAP)
    rc1, out1, err1 = run_checker(mp, FIX / PDF_OK, IMG_CAP)
    png_b, png_a = before[0]("ok-01.png", "F2"), after[0]("ok-01.png", "F2")
    ok = (rc0 == 0 and verdict(out0, "F2") == "PASS"
          and rc1 == EXIT_FAIL_CLOSED and "RESULT:" not in out1 and verdict(out1, "F2") == "-"
          and png_a == png_b == "PASS")
    return ok, (f"ok-05.pdf F2 原检查器 exit={rc0} 判词 {verdict(out0, 'F2')}；"
                f"变异体 exit={rc1} 无判词（stderr '{sanitize(err1).strip()[:44]}'）⇒ 该分支承重；"
                f"PNG 侧 ok-01 F2 {png_b}→{png_a}（不受影响）")


def m8(before, after, mp):
    """F3a 谓词取反（Important-3）：方向确实被检（合格前缀转红、缺冒号的 caption:6 转绿）。"""
    b1, a1 = before[1]("1", "F3a"), after[1]("1", "F3a")
    b6, a6 = before[1]("6", "F3a"), after[1]("6", "F3a")
    return (b1 == "PASS" and a1 == "FAIL" and b6 == "FAIL" and a6 == "PASS",
            f"caption:1 F3a {b1}→{a1}（合格前缀转红）；caption:6 F3a {b6}→{a6}"
            f"（'Figure 6 Model structure' 缺冒号，转绿）")


def m42(before, after, mp):
    """F3b 的词数口径（Task 6 的 Important-2）：换回"整条图注"口径 ⇒ caption:7 由 PASS 转 FAIL。

    背景：F3b 原先数整条图注（含 `Figure N:` 这 2 个词），而规范 H9 与它的复跑仪器
    `house-metrics.py` 的 `cap_words_*` 数的是**去掉标签后的正文**（P-D-c1）——两口径相差 2 词。
    本轮把 F3b 收敛到规范侧（`len(body.split())`），这条变异就是它的回归位。

    为什么必须**新增** fixture：同批其余图注两口径**同判**（caption:1 整条 8 / 正文 6、
    caption:5 整条 15 / 正文 13、caption:2 整条 24 / 正文 22 —— 都同红绿），
    拿它们证不了"F3b 数的到底是哪一段"。故新增 `caption:7`（整条 **13** / 正文 **11**），
    恰好卡在 `CAP_MAX=12` 的分界上：正文口径 PASS、整条口径 FAIL。
    它同时钉进 `expected.tsv` 的 `caption:7  F3b  PASS` ⇒ 口径若被改回去，逐格验收也 MISMATCH。
    """
    b7, a7 = before[1]("7", "F3b"), after[1]("7", "F3b")
    b5, a5 = before[1]("5", "F3b"), after[1]("5", "F3b")
    return (b7 == "PASS" and a7 == "FAIL" and a5 == b5 == "FAIL",
            f"caption:7（整条 13 词 / 正文 11 词）F3b {b7}→{a7}（口径换回整条 ⇒ 越线 1 词）；"
            f"NOTE/caption:5（整条 15 / 正文 13）F3b {b5}→{a5}"
            f"（两口径同判红 ⇒ 它证不了口径，故口径锚另立 caption:7）")


# (编号, 说明, 原文, 改文, 断言)
MUTATIONS = [
    ("M1", "F1_HI 1.20 → 0.90", "F1_LO, F1_HI = 0.80, 1.20", "F1_LO, F1_HI = 0.80, 0.90", m1),
    ("M2", "F1_LO/F1_HI 互换（区间空）", "F1_LO, F1_HI = 0.80, 1.20", "F1_LO, F1_HI = 1.20, 0.80", m2),
    ("M3", "PNG 无 --dpi 时不再 fail-closed，改成默认 200 硬着头皮判",
     '    if dpi is None:\n        fail_closed("FAIL F1: PNG 需要显式 --dpi（PNG 的 dpi 元信息不可信，见 provenance）")',
     '    if dpi is None:\n        dpi = 200  # 变异：守卫拆掉，默认 200 硬着头皮判', m3),
    ("M4", "F2 噪声地板 0.005 → 0.0", "c / tot >= 0.005", "c / tot >= 0.0", m4),
    ("M5", "CAP_MAX 12 → 99（CAP_HARD 17 不动）", "CAP_MAX, CAP_HARD = 12, 17", "CAP_MAX, CAP_HARD = 99, 17", m5),
    ("M6", "F3c 判定取反", 'res.append(("F3c", not cap.endswith("."), "句末不加句号"))',
     'res.append(("F3c", cap.endswith("."), "句末不加句号"))', m6),
    ("M7", "F2 的 PDF 栅格化分支整段删掉（退回 Image.open 读 PDF）",
     '''        if path.suffix.lower() == ".pdf":
            with fitz.open(path) as doc:
                if doc.page_count < 1:
                    fail_closed(f"FAIL: PDF 没有页 {path}（fail-closed）")
                pm = doc[0].get_pixmap(dpi=RASTER_DPI, colorspace=fitz.csRGB, alpha=False)
                return Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
        with Image.open(path) as im:''',
     "        with Image.open(path) as im:", m7),
    ("M8", "F3a 判定取反", 'res.append(("F3a", bool(re.match(r"^Figure\\s+\\d+\\s*:", cap)), "图注以 `Figure N:` 起"))',
     'res.append(("F3a", not bool(re.match(r"^Figure\\s+\\d+\\s*:", cap)), "图注以 `Figure N:` 起"))', m8),
    ("M42", "F3b 词数口径由**正文**换回**整条**（`len(body.split())` → `len(cap.split())`）",
     "    words = len(body.split())", "    words = len(cap.split())", m42),
]

# 探针（不是"判据变异"，是"验收脚本的 ERROR 分支变异"）：只在 **期望 FAIL 的那一行** fail-closed
PROBE = ("P1", "run-expected.py 的 ERROR 分支：rc=2/无判词 ⇒ 记 ERROR 且整轮非零退出",
         "    res = check(p, cap, a.textwidth_in, a.dpi)",
         "    if p.name == \"bad-f2-five-colors.pdf\":\n"
         "        sys.exit(EXIT_FAIL_CLOSED)  # 探针：只在期望 FAIL 的那一行 fail-closed\n"
         "    res = check(p, cap, a.textwidth_in, a.dpi)")


def p1(mp):
    """跑两遍逐格验收：干净一遍（须 MISMATCH 0 / N 且 exit 0），对变异体一遍（须记 ERROR 且 exit≠0）。

    `--checker` 就是为这条探针加的（默认值不变，收工 gate 不带该参数跑）。
    """
    clean = subprocess.run([sys.executable, str(FIX / "run-expected.py")], capture_output=True, text=True)
    mut = subprocess.run([sys.executable, str(FIX / "run-expected.py"), "--checker", str(mp)],
                         capture_output=True, text=True)
    c_last, m_last = clean.stdout.strip().splitlines()[-1], mut.stdout.strip().splitlines()[-1]
    err_rows = [l for l in mut.stdout.splitlines() if l.startswith("ERROR")]
    rc_b, out_b, _ = run_checker(CHK, FIX / PDF_BAD, IMG_CAP)
    rc_m, out_m, _ = run_checker(mp, FIX / PDF_BAD, IMG_CAP)
    # 旧版谓词（只看 "PASS  <crit>" 在不在）读同一份空 stdout 会得出什么：
    old_got = "PASS" if "PASS  F2 " in out_m else "FAIL"
    ok = (clean.returncode == 0 and c_last.startswith("MISMATCH 0 / ") and "ERROR" not in c_last
          and mut.returncode != 0 and m_last.startswith("MISMATCH 0 / ") and "ERROR 1" in m_last
          and len(err_rows) == 1
          and rc_b == 1 and verdict(out_b, "F2") == "FAIL"      # 原检查器：该行真的判成红（rc=1）
          and rc_m == EXIT_FAIL_CLOSED and out_m == "")          # 变异体：该行根本没判成（rc=2）
    return ok, (f"干净一遍 exit={clean.returncode} '{c_last}'；"
                f"对变异体一遍 exit={mut.returncode} '{m_last}'（{len(err_rows)} 行 ERROR）　"
                f"NOTE/同一行：原检查器 exit={rc_b} 判词 F2={verdict(out_b, 'F2')}；"
                f"变异体 exit={rc_m} stdout 空 ⇒ 旧版谓词会记 got={old_got}（= want ⇒ 记 OK，"
                f"整轮报 MISMATCH 0 假绿）；新版记 ERROR 且 exit≠0")


def git_hash_object(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True, text=True).stdout.strip()


# ================================================================ 规范数守卫的变异（Task 3）
# 为什么**不叫** M7/M8：任务书给的编号 M7–M10 与 `check-figure-style.py` 那一组已占用的
# M7（F2 的 PDF 分支）/ M8（F3a 取反）**撞号**；撞号的变异表会让"哪条红了"没法引用，
# 故本组顺延为 **M9–M12**（逐条对应任务书 M7/M8/M9/M10 的四种手法）。
#
# 这一组打的**不是检查器**，是 `house-style.md` / `provenance.md` ——
# 被验对象 = `check-house-style.py` 的规范数守卫（抽不到数即 fail-closed）。
ROOT = HERE.resolve().parents[2]
HOUSE_DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
HOUSE_PROV = ROOT / ".claude/skills/mcm-figure-choose/references/provenance.md"
HOUSE_SKILLS = ROOT / ".claude/skills"           # `K6` 判"这个 skill 存不存在"的真根
HOUSE_CHK = HERE / "check-house-style.py"
HMUTD = FIX / "_mut-house"


def house_run(checker, doc, prov, only):
    """跑规范数守卫：`--only` 限定被验的那几条，返回 (rc, stdout)。"""
    cmd = [sys.executable, str(checker), "--doc", str(doc), "--prov", str(prov), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def house_assert(desc, doc_src, prov_src, old, new, target, ids):
    """一次字面替换 + 前置/后置两跑。

    前置（`before`）：**原件**上这几条守卫必须全绿 —— 否则"改坏了才红"这条断言在
    "它本来就是红的"时也会通过（与 M2 的 R-6 同一条教训）。
    后置（`after`）：改坏副本上必须 **exit≠0** 且被点名的守卫**逐条**报 FAIL。
    """
    src = (HOUSE_DOC if target == "doc" else HOUSE_PROV).read_bytes()
    n_hit = src.decode("utf-8").count(old)
    if n_hit != 1:
        raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）")
    mutated = src.decode("utf-8").replace(old, new, 1).encode("utf-8")
    assert mutated != src, "变异体与原文相同"
    mp = HMUTD / ("house-style.md" if target == "doc" else "provenance.md")
    mp.write_bytes(mutated)                                  # write_bytes：不用 write_text
    rc_b, out_b = house_run(HOUSE_CHK, doc_src, prov_src, ids)
    rc_a, out_a = house_run(HOUSE_CHK, doc_src if target != "doc" else mp,
                            prov_src if target != "prov" else mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    return pre_ok and post_ok, f"{desc}　{detail}"


def house_mutations():
    """任务书 Step 4 的四种手法（M9–M12）+ 修复轮新增的七条（M13–M19），逐条必须实测红。"""
    return [
        ("M9", "house-style.md 里 H1 的上限 1.20 → 9.99", "doc",
         "**不超过 1.20×**", "**不超过 9.99×**", ["G-H1-hi"]),
        ("M10", "house-style.md 里 H9 的词数上限 12 → 3", "doc",
         "**上限 12 词**（p95）", "**上限 3 词**（p95）", ["G-H9-wmax", "G-H9-const-max"]),
        ("M11", "删掉 H4 那一行（主色中位那条依据）", "doc",
         "出货：主色中位 **2**、出货：零彩色 **30.5%**（202/662）、出货：≤4 覆盖率 **66.3%**（439/662）。\n",
         "", ["G-H4-med", "G-H4-zero", "G-H4-cov"]),
        ("M12", "provenance.md 里 P-H2-a 的复跑命令把分母口径从 p90 改成 mean", "prov",
         "python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_median",
         "python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_mean",
         ["P-H2-a"]),
        # ---- 修复轮（独立评审 Critical-1 / Important-3 / Important-4 / Minor N-7）新增
        ("M13", "H4 把 662 图上的转写口径读数 51.81 改回**已被证伪的 48.79**（Critical-1 的回归位）", "doc",
         "上是 **51.81%** ⇒ **57.2% 与 72.9% 不同源", "上是 **48.79%** ⇒ **57.2% 与 72.9% 不同源",
         ["G-H4-n2lo"]),
        ("M14", "H4 连续色图闸门的箱数下限 ≥100 → ≥20（退回形同虚设的那条腿）", "doc",
         "**彩色箱数 ≥100** **或**", "**彩色箱数 ≥20** **或**", ["G-H4-gate-box"]),
        ("M15", "H4 旧闸门在 heatmap 样本上的命中数 5/13 → 9/13（漏检证据被改坏）", "doc",
         "旧闸门只命中 **5/13**", "旧闸门只命中 **9/13**", ["G-H4-heat-old"]),
        ("M16", "H3 的 120 抽样中位区间 2.24–2.42 → 2.14–2.42（N-5 的回归位）", "doc",
         "中位落在 **2.24–2.42**", "中位落在 **2.14–2.42**", ["G-H3-s120-lo"]),
        ("M17", "H9 的宽口径条数 578 → 572（Important-4 的回归位）", "doc",
         "（**578**/662 = 87.31%", "（**572**/662 = 87.31%", ["G-H9-578"]),
        ("M18", "provenance.md P-H2-b 散文里的右尾 max 7.19 → 8.19（N-7：散文数也要守）", "prov",
         "（max 7.19 in）", "（max 8.19 in）", ["G-P-H2b-max"]),
        ("M19", "H12 的〔社区〕字号下限 ≥7 pt → ≥6 pt（N-8：社区值也不能被静默改掉）", "doc",
         "最小 **≥7 pt**", "最小 **≥6 pt**", ["G-H12-minpt"]),
    ]


# ============================================== `chart-types.md` 的结构守卫变异（Task 4）
# 打的是 `check-house-style.py` 的 `S1`/`S2`/`S3`/`S5`（被验对象 = 那棵决策树的形状）。
# 期望值**分两类**（修复轮 N-2 后）：**入口名 = 契约**（硬编码在检查器的 `ENTRIES`，不从文档现取）；
# **数 = 现取**（该小数所属 `H<n>` 条目里的小数字面量），故这里只写"改哪一处"，不写"应该等于几"。
# `S4` 是读数条（无谓词 ⇒ 无红可证），由探针 `R1` 另证（见 `s4_readout_probe`）。
CT_DOC = ROOT / ".claude/skills/mcm-figure-choose/references/chart-types.md"


def struct_run(checker, ct, only):
    """跑结构守卫：只换 `--ct`（被验的决策树），`house-style.md` / `provenance.md` 用真件。"""
    cmd = [sys.executable, str(checker), "--ct", str(ct), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def ct_assert(desc, edits, ids, probe=None):
    """对 `chart-types.md` 做**一次或多次**字面替换 + 前置/后置两跑。

    `edits` 是 `[(原文, 改文), …]`，每条的命中数必须恰为 1（否则驱动器自己报错）；
    多替换是给 `M26`（要把**两个**小数一起抹掉）用的。
    `probe`：可选，收变异体全文、返回一行**现算**的补充说明（`M24` 用它记"任务书的宽松写法
    在这种改法下不会红"）。
    """
    text = CT_DOC.read_bytes().decode("utf-8")
    for old, new in edits:
        n_hit = text.count(old)
        if n_hit != 1:
            raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）：{old[:48]!r}")
        text = text.replace(old, new, 1)
    if text == CT_DOC.read_bytes().decode("utf-8"):
        raise AssertionError("变异体与原文相同")
    mp = HMUTD / "chart-types.md"
    mp.write_bytes(text.encode("utf-8"))                      # write_bytes：不用 write_text
    rc_b, out_b = struct_run(HOUSE_CHK, CT_DOC, ids)
    rc_a, out_a = struct_run(HOUSE_CHK, mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    if probe:
        detail += "　" + probe(text)
    return pre_ok and post_ok, f"{desc}　{detail}"


def _m24_probe(txt):
    """`M24` 的现算 NOTE：任务书那条正则（**全文**扫 radar×低频）在这个变异体上到底还红不红。"""
    lax = bool(re.search(r"radar[^\n]*低频|低频[^\n]*radar", txt, re.I))
    return (f"NOTE/任务书给的正则（**全文**扫 `radar` × `低频`）在本变异体上仍"
            f"{'**命中** ⇒ 那个写法会漏掉这次改坏' if lax else '不命中'}"
            f"；本实现只扫 **radar 定义行** ⇒ 红")


def _old_pool():
    """**修复前**的 `S5` 同值池：`house-style.md` ∪ `provenance.md` 的小数字面量全集（现取）。"""
    return set(re.findall(r"\d+\.\d+", HOUSE_DOC.read_bytes().decode("utf-8"))) | \
        set(re.findall(r"\d+\.\d+", HOUSE_PROV.read_bytes().decode("utf-8")))


def _house_h_nums(hid):
    """`house-style.md` 的 `### H<hid>.` 条目里的小数字面量（与检查器 `_h_entries` 同口径，现取）。"""
    txt = HOUSE_DOC.read_bytes().decode("utf-8")
    m = re.search(rf"^### H{hid}\..*?$(.*?)(?=^### H\d+\.|\Z)", txt, re.M | re.S)
    return set(re.findall(r"\d+\.\d+", m.group(1))) if m else set()


def _s5_scope_probe(num, hid=None):
    """`M27`/`M28` 的现算 NOTE：这个数**旧写法怎么会绿**、**新写法为什么红**。

    旧写法（`S5` 修复前）= "值 ∈ house-style ∪ provenance 的全局池"（池里混着容差常量与
    别的 `H<n>` 条目的数）⇒ 池内一律绿。新写法 = **归到同行 `H<n>` 引用**且 **∈ 该条目的数**。
    """
    def probe(_txt):
        pool = _old_pool()
        if hid is None:
            return (f"NOTE/`{num}` 在**旧池子**（{len(pool)} 个数）里: {num in pool}"
                    f" ⇒ 旧写法**判绿、漏掉这次改坏**；新写法：该行**没有任何 `H<n>` 引用**"
                    f" ⇒ 无所属 ⇒ 红（fail-closed）")
        ent = _house_h_nums(hid)
        return (f"NOTE/`{num}` 在**旧池子**（{len(pool)} 个数）里: {num in pool}"
                f" ⇒ 旧写法**判绿、漏掉这次改坏**；`H{hid}` 条目的数 {sorted(ent)} 里"
                f"{'有它' if num in ent else '**没有它**'} ⇒ 新写法红（跨条目搬数）")
    return probe


def struct_mutations():
    """`M22`–`M28`：`chart-types.md` 的七种改坏手法，逐条必须实测红。"""
    return [
        ("M22", "chart-types.md：入口 9 由『不确定性』**改名**（九个入口少一个）",
         [("### 入口 9 · 不确定性", "### 入口 9 · 时变")], ["S1"], None),
        ("M23", "chart-types.md：删掉入口 1 的『**备选**』那一段（四段少一段）",
         [("**备选**：`dot plot`", "**可替代方案**：`dot plot`")], ["S2"], None),
        ("M24", "chart-types.md：删掉 **radar 定义行**上的『低频』标注",
         [("连成多边形 —— **低频**：获奖样本里属罕见选择", "连成多边形 —— 获奖样本里属罕见选择")],
         ["S3"], _m24_probe),
        ("M25", "chart-types.md：3D 那条参照分布数 9.2% → 9.3%（与 house-style 不同值）",
         [("**9.2%**", "**9.3%**")], ["S5"], None),
        ("M26", "chart-types.md：两个小数**都**写成中文数字 ⇒ 一个实测数都抽不到（fail-closed 该红）",
         [("**0.0%**", "**零**"), ("**9.2%**", "**九点二**")], ["S5"], None),
        # ---- 修复轮（复审 N-2）：`S5` 的归属口径从"全局池"收紧到"该 `H<n>` 条目"
        ("M27", "chart-types.md：写进一个**池内但无所属**的数 `1.20`（H1 的上限，旧池子里有它）",
         [('   机械守卫 `S5` 管的是**抄过来之后有没有漂**，不是"这个数本身对不对"。',
           '   机械守卫 `S5` 管的是**抄过来之后有没有漂**，不是"这个数本身对不对"。'
           '图宽与正文宽之比**不超过 1.20**。')], ["S5"], _s5_scope_probe("1.20")),
        ("M28", "chart-types.md：H7 那条的数 `9.2` 换成 `0.5`（H4 的地板，**池内但语义不同**）",
         [("**9.2%**", "**0.5%**")], ["S5"], _s5_scope_probe("0.5", "7")),
    ]


# ============================================== `SKILL.md` 的短契约守卫变异（Task 5）
# 打的是 `check-house-style.py` 的 `K1`–`K6`（被验对象 = `SKILL.md` 这份**短契约**）。
# 为什么从 **`M29`** 起：`M1`–`M8`（检查器）· `M9`–`M19`（规范数）· `C1`/`C2`（CENSUS）·
# `M22`–`M28`（`chart-types.md` 的结构）已占号；任务书给的 `M14`/`M15`/`M16` 与上面**撞号**，
# 撞号的变异表会让"哪条红了"没法引用（同 Task 3 顺延 `M9`–`M12` 的那次），故顺延 `M29` 起。
# 期望值分两类（与结构守卫同）：**契约型硬编码**（行数上限 / 指针路径 / 九个入口名）·
# **现取型**（禁止串从 `house-style.md` 现取）—— 故这里只写"改哪一处"，不写"应该等于几"。
SKILL_MD = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"


def sub_once(text, old, new):
    """一次字面替换：命中数必须恰为 1（否则驱动器自己报错）。"""
    n = text.count(old)
    if n != 1:
        raise AssertionError(f"原文串命中 {n} 次（必须恰为 1）：{old[:44]!r}")
    return text.replace(old, new, 1)


def sub_all(text, old, new):
    """替换**全部**出现处（用于"把某个名字从全文拿掉"这类改法；命中数必须 ≥1）。"""
    n = text.count(old)
    if n < 1:
        raise AssertionError(f"原文串一次都没命中：{old[:44]!r}")
    return text.replace(old, new)


def pad_to(text, n):
    """在文末补空行，把行数**恰**撑到 `n`（`M31` 用）。"""
    cur = len(text.splitlines())
    if cur >= n:
        raise AssertionError(f"原文已有 {cur} 行 ≥ {n}")
    return text + "\n" * (n - cur)


def skill_run(checker, skill, only):
    """跑 SKILL 守卫：只换 `--skill`（被验的短契约），其余文档用真件。"""
    cmd = [sys.executable, str(checker), "--skill", str(skill), "--only", *only]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, p.stdout


def skill_assert(desc, transform, ids, probe=None):
    """对 `SKILL.md` 做一次（或一串）字面替换 + 前置/后置两跑。

    前置（原件）必须全绿、后置（改坏副本）必须 exit≠0 **且**被点名的守卫逐条报 FAIL ——
    与 `house_assert` / `ct_assert` 同一条纪律（"它本来就是红的"不算证据）。
    `probe`：可选，收**变异体全文**、返回一行**现算**的补充说明（`M30` 用它记"任务书那条宽松
    谓词（`references/house-style.md` 或裸 `house-style.md` 任一命中即可）在这种改法下不会红"）。
    """
    text0 = SKILL_MD.read_bytes().decode("utf-8")
    text = transform(text0)
    if text == text0:
        raise AssertionError("变异体与原文相同")
    mp = HMUTD / "SKILL.md"
    mp.write_bytes(text.encode("utf-8"))                      # write_bytes：不用 write_text
    rc_b, out_b = skill_run(HOUSE_CHK, SKILL_MD, ids)
    rc_a, out_a = skill_run(HOUSE_CHK, mp, ids)
    pre_ok = rc_b == 0 and all(f"PASS  {i} " in out_b for i in ids)
    post_ok = rc_a != 0 and all(f"FAIL  {i} " in out_a for i in ids)
    detail = (f"前置(原件) exit={rc_b} {'全绿' if pre_ok else '未全绿 <<<'}；"
              f"后置(改坏) exit={rc_a} 被点名守卫 "
              + "、".join(f"{i}={'FAIL' if f'FAIL  {i} ' in out_a else '未红 <<<'}" for i in ids))
    if probe:
        detail += "　" + probe(text)
    return pre_ok and post_ok, f"{desc}　{detail}"


def _m30_probe(_txt):
    """`M30` 的现算 NOTE：**任务书那条宽松谓词**在这个变异体上会不会红。

    任务书的 `K2` 写的是 `"references/house-style.md" in txt or "house-style.md" in txt` ——
    `SKILL.md` 通篇要提规范，裸文件名**必然**还在 ⇒ 那个写法**判绿**、漏掉这次改坏
    （"指针还在不在"会被一句"见 house-style.md"顶包）。本实现要求**skill 目录内的相对路径**，
    即 Task 7 的检查器要核的那个形态。
    """
    hit_bare = "house-style.md" in _txt
    return (f"NOTE/任务书那条宽松谓词（路径**或**裸文件名任一即可）在本变异体上仍"
            f"{'**命中** ⇒ 那个写法会漏掉这次改坏' if hit_bare else '不命中'}；"
            f"本实现要求 `references/house-style.md` 这个**相对路径** ⇒ 红")


def _k5_scope_probe(num):
    """`M29` 的现算 NOTE：这个数为什么**两条守卫都该红**（K3 与 K5 是两道不同的闸）。"""
    def probe(_txt):
        doc = HOUSE_DOC.read_bytes().decode("utf-8")
        banned = bool(re.search(rf"(?<![\d.]){re.escape(num)}(?![\d])", doc))
        return (f"NOTE/`{num}` 在 `house-style.md` 里出现: {banned} ⇒ `K3`（现取禁止串）"
                f"{'红' if banned else '**不会红（不在禁止串表里）**'}；`K5`（除 `H<n>` 外每个数"
                f"都要被声明为结构性计数）与禁止串表无关 —— 这个数没被声明就红（本次即红，"
                f"故两条是**两道不同的闸**，不是同一条判两遍）")
    return probe


def drop_section(text, start, end):
    """把 `## <start>` 那一节**整段**删掉（删到下一个 `## <end>` 之前）。"""
    lines = text.splitlines(keepends=True)
    i = next(k for k, l in enumerate(lines) if l.startswith(start))
    j = next(k for k, l in enumerate(lines) if k > i and l.startswith(end))
    return "".join(lines[:i] + lines[j:])


TOP_ITEM = "- **推荐图型**：给**一个首选**；"


def _m36_probe(_txt):
    """`M36` 的现算 NOTE：为什么这条**只能**由单位词臂红 —— 直接读 `K3` 在同一副本上印出的读数。"""
    _rc, out = skill_run(HOUSE_CHK, HMUTD / "SKILL.md", ["K3"])
    line = next((l for l in out.splitlines() if l.startswith(("PASS  K3", "FAIL  K3"))), "")
    mb = re.search(r"裸值词 \[([^\]]*)\]", line)
    mu = re.search(r"≥(\d+)", line)
    mh = re.search(r"中文命中 (\[[^\]]*\]|无)", line)
    return (f"NOTE/同一副本上 `K3` 印出的『裸值词』= [{mb.group(1) if mb else '?'}]"
            f"（下界 ≥{mu.group(1) if mu else '?'}）、『中文命中』= {mh.group(1) if mh else '?'}"
            f" ⇒ 插入串里的 `一` **不在裸值词里**（1 < 下界），这条红的是**单位词臂**"
            f"（`倍` 是 `×` 的中文写法）—— 两条臂各管一段，只留一条就会漏掉这一半")


def _m38_probe(_txt):
    """`M38` 的现算 NOTE：这段被删掉时 `K1`–`K6` 会不会红 —— 现跑一遍给结论。"""
    rc, out = skill_run(HOUSE_CHK, HMUTD / "SKILL.md", ["K1", "K2", "K3", "K4", "K5", "K6"])
    res = next((l for l in out.splitlines() if l.startswith("RESULT")), "(无 RESULT 行)")
    return (f"NOTE/同一副本上 `K1`–`K6` 现跑 exit={rc}『{res}』 ⇒ 这六条**一条都不红**"
            f"（删掉整段不违反它们中的任何一条）—— `K7` 是这段唯一的机械守卫")


def skill_mutations():
    """`M29`–`M39`：`SKILL.md` 的十种改坏手法，逐条必须实测红。"""
    return [
        ("M29", "SKILL.md：写进一条规范数值『图宽用满 0.951×正文宽』⇒ 重述规范（`K3` 与 `K5` 都红）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（图宽用满 0.951×正文宽）；"),
         ["K3", "K5"], _k5_scope_probe("0.951")),
        ("M30", "SKILL.md：指针行删掉、别处只留裸文件名 ⇒ `K2` 红（宽松谓词会漏，见 NOTE）",
         lambda t: sub_once(sub_once(t, "- **规范正文**（图通常长什么样、每条规则的数值与验证状态）："
                                       "`references/house-style.md`\n", ""),
                            "（规范在 `references/house-style.md`）", "（规范在 `house-style.md`）"),
         ["K2"], _m30_probe),
        ("M31", "SKILL.md：把文件撑到 151 行 ⇒ `K1` 红（短契约上限 <150）",
         lambda t: pad_to(t, 151), ["K1"], None),
        ("M32", "SKILL.md：入口 9 由『不确定性』改名 ⇒ `K4` 红（九个入口少一个）",
         lambda t: sub_all(t, "不确定性", "时变"), ["K4"], None),
        ("M33", "SKILL.md：把点名绘图 skill 的那行的〔拟建〕去掉 ⇒ `K6` 红（点名即错）",
         lambda t: sub_once(t, "  - `mcm-plot-python`（〔拟建〕）", "  - `mcm-plot-python`"),
         ["K6"], None),
        # ---- 修复轮（复审 1 Important + N-2/N-3/N-4）
        ("M35", "SKILL.md：写进『主色四色以内』（中文数词 + 规范单位词）⇒ `K3` 的中文数词臂红"
                "（原先整句走绿，见 Important-1）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（主色四色以内）；"),
         ["K3"], None),
        ("M36", "SKILL.md：写进『图宽不超过一倍正文宽』⇒ `K3` 红（**单位词臂**单独在红，见 NOTE）",
         lambda t: sub_once(t, TOP_ITEM, "- **推荐图型**：给**一个首选**（图宽不超过一倍正文宽）；"),
         ["K3"], _m36_probe),
        ("M37", "SKILL.md：把 `4`（H4 的规范值）写进**声明行** ⇒ `K5` 红（声明行只许出现契约数）",
         lambda t: sub_once(t, "② **结构性计数**——全文只有一处，就是决策树的入口数 **9**",
                            "② **结构性计数**——入口数 **9** 与主色上限 **4**"),
         ["K5"], None),
        ("M38", "SKILL.md：删掉「输出契约」整段 ⇒ `K7` 红（该段原先没有任何机械存在性守卫）",
         lambda t: drop_section(t, "## 输出契约", "## 边界"), ["K7"], _m38_probe),
        ("M39", "SKILL.md：决策树表多加一行（= 多一个入口名）⇒ `K4` + `K5` 红（旧写法不会红）",
         lambda t: sub_once(t, "| **不确定性** | 结论有多稳 / 最坏能坏到哪 |",
                            "| **不确定性** | 结论有多稳 / 最坏能坏到哪 |\n| **雷达** | 谁跟谁像 |"),
         ["K4", "K5"], None),
    ]


def k6_exists_mut():
    """`M40`：`K6` 的**反向臂** —— 标了〔拟建〕的 skill **真的存在**时必须红（复审 N-5）。

    做法：把 `--skills-root` 指到一个**临时根**（真件不碰），里面建一个 `mcm-plot-python/SKILL.md`
    ⇒ "标了〔拟建〕"与"事实存在"矛盾 ⇒ 必须红；前置（真根）必须绿。
    """
    if (HOUSE_SKILLS / "mcm-plot-python").exists():
        raise AssertionError("真仓里已经有 mcm-plot-python 了 —— 这条变异的前提不成立")

    def run(sroot):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--skill", str(SKILL_MD),
                            "--skills-root", str(sroot), "--only", "K6"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "mcm-plot-python").mkdir()
        (tmp / "mcm-plot-python" / "SKILL.md").write_bytes(b"---\nname: mcm-plot-python\n---\n")
        rc_b, out_b = run(HOUSE_SKILLS)
        rc_a, out_a = run(tmp)
    pre_ok = rc_b == 0 and "PASS  K6 " in out_b
    post_ok = rc_a != 0 and "FAIL  K6 " in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K6")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (f"前置(真 skills 根) exit={rc_b} {'K6 绿' if pre_ok else '未绿 <<<'}；"
                                f"后置(临时根里真有 mcm-plot-python) exit={rc_a} 『{line}』")


def k8_verify_line_mut():
    """`M41`：`K8` —— `house-style.md` 的每个 `H<n>` 条目都要有**恰一行** `**验证**：`（复审 N-7）。

    做法：在**副本**上把**第一个**带验证行的 `H<n>` 条目里那行抹掉（真件不碰）⇒ 必须红；前置必须绿。
    哪一条被抹掉是**现算**的（不写死 `H4`）—— `H<n>` 的名字与位置都不许抄进脚本。
    """
    src = HOUSE_DOC.read_bytes().decode("utf-8")
    sec = next((m for m in re.finditer(r"^### (H\d+)\..*?$(.*?)(?=^### H\d+\.|\Z)", src, re.M | re.S)
                if "**验证**：" in m.group(2)), None)
    if sec is None:
        raise AssertionError("house-style.md 里找不到带 `**验证**：` 的 `H<n>` 条目（前提不成立）")
    new_blk = re.sub(r"\n\*\*验证\*\*：.*?(?=\n\n)", "\n", sec.group(0), count=1, flags=re.S)
    if new_blk == sec.group(0):
        raise AssertionError("副本没改到（那行没命中？）")
    mut = src[:sec.start()] + new_blk + src[sec.end():]
    mp = HMUTD / "k8.house-style.md"
    mp.write_bytes(mut.encode("utf-8"))                      # write_bytes：不用 write_text

    def run(doc):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--doc", str(doc),
                            "--skill", str(SKILL_MD), "--only", "K8"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    rc_b, out_b = run(HOUSE_DOC)
    rc_a, out_a = run(mp)
    mp.unlink()
    pre_ok = rc_b == 0 and "PASS  K8 " in out_b
    post_ok = rc_a != 0 and "FAIL  K8 " in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K8")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (f"前置(真件) exit={rc_b} {'K8 绿' if pre_ok else '未绿 <<<'}；"
                                f"后置(副本抹掉 `{sec.group(1)}` 的验证行) exit={rc_a} 『{line}』")


def k3_fail_closed_mut():
    """`M34`：`K3` 的 **fail-closed 臂** —— 禁止串**一条都抽不到**时，这条判据必须红。

    做法：把**副本** `house-style.md` 里的小数字面量与 `≤n` 形态全抹掉（真件不碰），
    于是 `K3` 的"现取禁止串"抽到空集 —— 前置（真件）必须绿、后置必须红。
    不证这一臂的话，"抽不到即 FAIL"就只是注释里的一句话（本仓栽过的"判据恒绿"里，
    最常见的一类就是**仪器取不到参照物时默认放行**）。
    """
    src = HOUSE_DOC.read_bytes().decode("utf-8")
    mut = re.sub(r"\d+\.\d+", "□", src)
    mut = re.sub(r"≤\s*\d+", "□", mut)
    mut = re.sub(r"<\s*\d+\s*词", "□", mut)
    if mut == src:
        raise AssertionError("变异体与原文相同（一条都改不动？）")
    mp = HMUTD / "house-style.md"
    mp.write_bytes(mut.encode("utf-8"))                      # write_bytes：不用 write_text

    def run(doc):
        p = subprocess.run([sys.executable, str(HOUSE_CHK), "--doc", str(doc),
                            "--skill", str(SKILL_MD), "--only", "K3"],
                           capture_output=True, text=True, cwd=str(ROOT))
        return p.returncode, p.stdout

    rc_b, out_b = run(HOUSE_DOC)
    rc_a, out_a = run(mp)
    left = len(set(re.findall(r"\d+\.\d+", mut)) | set(re.findall(r"≤\s*\d+", mut)))
    pre_ok = rc_b == 0 and "PASS  K3 " in out_b
    post_ok = rc_a != 0 and "FAIL  K3 " in out_a and "fail-closed" in out_a
    line = next((l.split(None, 2)[-1] for l in out_a.splitlines() if l.startswith("FAIL  K3")), "（缺 FAIL 行）")
    return pre_ok and post_ok, (f"前置(真件) exit={rc_b} {'K3 绿' if pre_ok else '未绿 <<<'}；"
                                f"后置(副本抹掉小数与 `≤n`) exit={rc_a} 『{line}』"
                                f"（副本里剩下的禁止串 {left} 条）")


def s4_readout_probe():
    """`R1`：证 `S4` 是**读数条**（不是判据）—— 改坏副本上**读数会动**、**判词不动**。

    两条断言（缺一条这个"读数条"就是坏的）：
      ① 原件 `--only S4`：rc=0、出现 `READ  S4`、**不出现** `PASS  S4` / `FAIL  S4`；
      ② 把 `bar chart` 的定义**复制成两份**（真的制造一次重名）后：rc **仍为 0**（它不判红），
         而读数里的 `重名` 字段**必须变**（它真在读那份文档）。
    """
    rc0, out0 = struct_run(HOUSE_CHK, CT_DOC, ["S4"])
    read_line = next((l for l in out0.splitlines() if l.startswith("READ  S4")), "")
    n0 = re.search(r"定义行 (\d+)", read_line)
    dup0 = re.search(r"重名 ([^（]*)（", read_line)
    text = CT_DOC.read_bytes().decode("utf-8")
    line = next(l for l in text.splitlines() if l.startswith("**bar chart**:"))
    mp = HMUTD / "chart-types.md"
    mp.write_bytes((text.replace(line, line + "\n" + line, 1)).encode("utf-8"))
    rc1, out1 = struct_run(HOUSE_CHK, mp, ["S4"])
    read_line1 = next((l for l in out1.splitlines() if l.startswith("READ  S4")), "")
    n1 = re.search(r"定义行 (\d+)", read_line1)
    dup1 = re.search(r"重名 ([^（]*)（", read_line1)
    clean = (rc0 == 0 and bool(read_line) and "PASS  S4" not in out0 and "FAIL  S4" not in out0)
    moved = (rc1 == 0 and n0 and n1 and int(n1.group(1)) == int(n0.group(1)) + 1
             and dup1 and "bar chart" in dup1.group(1))
    def _body(l):
        return l.split(None, 2)[-1] if len(l.split(None, 2)) == 3 else l

    return clean and moved, (
        f"原件 `--only S4` exit={rc0} 『{_body(read_line) if read_line else '(缺 READ 行) <<<'}』"
        f"（无 PASS/FAIL 判词）　"
        f"把 `bar chart` 定义复制一份后 exit={rc1} 『{(dup1.group(1).strip() if dup1 else '?')}』"
        f"⇒ 读数从 {n0.group(1) if n0 else '?'} 行涨到 {n1.group(1) if n1 else '?'} 行、"
        f"重名被点出，而 **rc 仍为 0**（读数条只读不判；一个判据做不到这点）")


# ---------------------------------------------------------------- CENSUS 的变异（Important-2）
# 为什么单列一组：M9–M19 全走 `--only <id>`，而 CENSUS 只在**不带 `--only`** 时才跑
# （`if not want:`）⇒ 上面那些变异**一条都没验过 CENSUS**。这组故意不带 `--only`。
CENSUS_MUTATIONS = [
    ("C1", "往 house-style.md 末尾**加一句带整数的话**（『共 37 条断言，其中 6 条为社区条目。』）",
     "doc", "数 ①（`G-H13-band`）\n", "数 ①（`G-H13-band`）\n\n共 37 条断言，其中 6 条为社区条目。\n"),
    ("C2", "把仪器实现常量 `quantize(32, MEDIANCUT)` 改成 `quantize(99, MEDIANCUT)`"
            "（上下文豁免表不能是万能兜底）",
     "doc", "quantize(32, MEDIANCUT)", "quantize(99, MEDIANCUT)"),
]


def house_census_run(doc, prov):
    """**不带 `--only`** 跑一遍（CENSUS 才会参与）；`--no-provenance` 只为省掉 46 次子进程。"""
    cmd = [sys.executable, str(HOUSE_CHK), "--doc", str(doc), "--prov", str(prov), "--no-provenance"]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    census = [l for l in p.stdout.splitlines() if l.startswith("CENSUS")]
    return p.returncode, p.stdout, (census[0] if census else "(没有 CENSUS 行)")


def run_census_mutations():
    """`C1`/`C2` 两条：改坏副本必须让 rc≠0 **且** CENSUS 报『未入理由表』≥1。"""
    rows, failed = [], []
    for mid, desc, target, old, new in CENSUS_MUTATIONS:
        src = (HOUSE_DOC if target == "doc" else HOUSE_PROV).read_bytes()
        if src.decode("utf-8").count(old) != 1:
            print(f"RED-BAD  {mid}  原文串命中 != 1——驱动器自己报错")
            failed.append(mid)
            continue
        mp = HMUTD / ("census.house-style.md" if target == "doc" else "census.provenance.md")
        mp.write_bytes(src.decode("utf-8").replace(old, new, 1).encode("utf-8"))
        rc_b, out_b, cen_b = house_census_run(HOUSE_DOC, HOUSE_PROV)
        rc_a, out_a, cen_a = house_census_run(mp if target == "doc" else HOUSE_DOC,
                                              mp if target == "prov" else HOUSE_PROV)
        m = re.search(r"未入理由表 (\d+) 个", cen_a)
        n_unlisted = int(m.group(1)) if m else -1
        pre_ok = rc_b == 0 and "未入理由表 0 个" in cen_b
        post_ok = rc_a != 0 and n_unlisted >= 1
        detail = (f"前置(原件) exit={rc_b} 『{(cens := cen_b.split('·')[-1].strip())}』；"
                  f"后置(改坏) exit={rc_a} 未入理由表 {n_unlisted} 个 ⇒ "
                  f"{'CENSUS 当场点了出来' if post_ok else '未达预期 <<<'}")
        rows.append(("RED-OK" if (pre_ok and post_ok) else "RED-BAD", mid, desc, detail))
        if not (pre_ok and post_ok):
            failed.append(mid)
    for f in HMUTD.glob("census.*"):
        f.unlink()
    return rows, failed


def run_house():
    """跑完整组（规范数守卫 M9–M19 + CENSUS C1/C2 + 结构守卫 M22–M26 + 读数条探针 R1）。

    返回 `(rows, failed, 自证 ok, 分组条数)`；`rows` 里 `mid == "R1"` 的那条是**探针**不是判据变异。
    """
    doc_hash, prov_hash = git_hash_object(HOUSE_DOC), git_hash_object(HOUSE_PROV)
    ct_hash = git_hash_object(CT_DOC)
    skill_hash = git_hash_object(SKILL_MD)
    HMUTD.mkdir(exist_ok=True)
    rows, failed = [], []
    f_house, f_census, f_struct = [], [], []
    n_house = 0
    for mid, desc, target, old, new, ids in house_mutations():
        n_house += 1
        try:
            ok, detail = house_assert(desc, HOUSE_DOC, HOUSE_PROV, old, new, target, ids)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            f_house.append(mid)
            continue
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            f_house.append(mid)
    # CENSUS 那两条**必须**在清空 `_mut-house/` 之前跑（它们要写自己的变异副本）
    crows, cfailed = run_census_mutations()
    rows += crows
    failed += cfailed
    f_census += cfailed
    n_census = len(crows)

    # ---- 结构守卫（Task 4）：`chart-types.md`
    srows, sfailed = [], []
    for mid, desc, edits, ids, probe in struct_mutations():
        try:
            ok, detail = ct_assert(desc, edits, ids, probe)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            f_struct.append(mid)
            continue
        srows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            f_struct.append(mid)

    # ---- 读数条探针（不是判据变异）：`S4` 只读不判
    try:
        r_ok, r_detail = s4_readout_probe()
    except (AssertionError, StopIteration) as e:                 # noqa: BLE001（驱动器自己的出口）
        r_ok, r_detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    probe_row = ("RED-OK" if r_ok else "RED-BAD", "R1",
                 "读数条 `S4`：该动的时候动、该判的时候不判", r_detail)
    if not r_ok:
        failed.append("R1")

    # ---- SKILL 守卫（Task 5）：`SKILL.md` 的短契约
    krows, kfailed = [], []
    for mid, desc, transform, ids, probe in skill_mutations():
        try:
            ok, detail = skill_assert(desc, transform, ids, probe)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            kfailed.append(mid)
            continue
        krows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)
            kfailed.append(mid)

    # ---- `M34`：`K3` 的 fail-closed 臂（打的是 `house-style.md` 的副本，不是 SKILL.md）
    try:
        k34_ok, k34_detail = k3_fail_closed_mut()
    except AssertionError as e:
        k34_ok, k34_detail = False, f"驱动器自己报错：{type(e).__name__}: {e}"
    krows.append(("RED-OK" if k34_ok else "RED-BAD", "M34",
                  "house-style.md：小数字面量与 `≤n` 全抹掉 ⇒ `K3` 抽不到禁止串 ⇒ fail-closed 红",
                  k34_detail))
    if not k34_ok:
        failed.append("M34")
        kfailed.append("M34")

    # ---- `M40`：`K6` 的反向臂（换 skills 根，真件不碰）
    # ---- `M41`：`K8`（打的是 `house-style.md` 的副本，真件不碰）
    for mid, desc, fn in (
        ("M40", "SKILL.md：`--skills-root` 指到**真有** `mcm-plot-python` 的临时根 ⇒ "
                "`K6` 红（标了〔拟建〕就必须真的不存在 —— 反向臂）", k6_exists_mut),
        ("M41", "house-style.md：副本里抹掉某个 `H<n>` 的『**验证**：』行 ⇒ `K8` 红"
                "（`SKILL.md` 那句『逐条标了验证状态』要成立）", k8_verify_line_mut),
    ):
        try:
            ok_m, detail_m = fn()
        except AssertionError as e:
            ok_m, detail_m = False, f"驱动器自己报错：{type(e).__name__}: {e}"
        krows.append(("RED-OK" if ok_m else "RED-BAD", mid, desc, detail_m))
        if not ok_m:
            failed.append(mid)
            kfailed.append(mid)

    rows += srows
    for f in HMUTD.glob("*"):
        f.unlink()
    HMUTD.rmdir()
    clean = not HMUTD.exists()
    byte_ok = (HOUSE_DOC.read_bytes().decode("utf-8").count("**不超过 1.20×**") == 1
               and HOUSE_PROV.read_bytes().decode("utf-8").count("--metric h2_colw_p90_median") == 1
               and CT_DOC.read_bytes().decode("utf-8").count("### 入口 9 · 不确定性") == 1
               and SKILL_MD.read_bytes().decode("utf-8").count("- **推荐图型**：给**一个首选**；") == 1
               # `M40` 换的是 `--skills-root`，真 skills 根不该被碰：这里核它没多出那个 skill
               and not (HOUSE_SKILLS / "mcm-plot-python").exists())
    same = (git_hash_object(HOUSE_DOC) == doc_hash and git_hash_object(HOUSE_PROV) == prov_hash
            and git_hash_object(CT_DOC) == ct_hash and git_hash_object(SKILL_MD) == skill_hash)
    print("\n" + "=" * 78)
    print(f"规范数守卫的变异（M9–M19 + C1/C2 · 打的是 house-style.md / provenance.md，共 {n_house + n_census} 条）")
    print("=" * 78)
    for st, mid, desc, detail in rows[:n_house + n_census]:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("\n" + "=" * 78)
    print(f"结构守卫的变异（M22–M28 · 打的是 chart-types.md，共 {len(srows)} 条）"
          f" + 读数条探针 R1")
    print("=" * 78)
    for st, mid, desc, detail in srows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print("-" * 78)
    print(f"{probe_row[0]:<8} {probe_row[1]:<4} {probe_row[2]}")
    print(f"         {probe_row[3]}")
    print("\n" + "=" * 78)
    print(f"SKILL 守卫的变异（M29–M41 · 打的是 SKILL.md 的副本；M34/M41 打的是 house-style.md 的"
          f"副本、M40 换 skills 根，共 {len(krows)} 条）")
    print("=" * 78)
    for st, mid, desc, detail in krows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    print(f"还原自证  house-style.md blob {doc_hash} {'== 变异前' if same else '!= 变异前 <<<'}"
          f" · provenance.md blob {prov_hash} · chart-types.md blob {ct_hash}"
          f" · SKILL.md blob {skill_hash}"
          f" · 原件字面仍在: {byte_ok} · _mut-house/ 已清空: {clean}")
    return rows, failed, (clean and byte_ok and same), {
        "house": n_house, "census": n_census, "struct": len(srows), "skill": len(krows),
        "f_house": f_house, "f_census": f_census, "f_struct": f_struct, "f_skill": kfailed,
        "probe_row": probe_row}


def mutate(src, old, new, out_path):
    """一次字面替换 → 写副本。命中数必须恰为 1，否则驱动器自己报错。"""
    n_hit = src.decode("utf-8").count(old)
    if n_hit != 1:
        raise AssertionError(f"原文串命中 {n_hit} 次（必须恰为 1）")
    mutated = src.decode("utf-8").replace(old, new, 1).encode("utf-8")
    assert mutated != src, "变异体与原文相同"
    out_path.write_bytes(mutated)               # write_bytes：不用 write_text（Windows CRLF）
    return mutated


def main():
    src = CHK.read_bytes()                      # 原始字节（全程不写回原文件）
    base_hash = git_hash_object(CHK)
    print("=" * 78)
    print("变异驱动器 · check-figure-style.py")
    print("=" * 78)
    print(f"原检查器 blob  {base_hash}")
    print(f"逐格验收基线  python fixtures/run-expected.py → exit ", end="")
    print(subprocess.run([sys.executable, str(FIX / "run-expected.py")],
                         capture_output=True, text=True).returncode)

    MUTD.mkdir(exist_ok=True)
    before = reader(CHK)
    failed, rows = [], []
    for mid, desc, old, new, fn in MUTATIONS:
        mp = MUTD / f"check-figure-style.{mid}.py"
        try:
            mutate(src, old, new, mp)
        except AssertionError as e:
            print(f"RED-BAD  {mid}  {e}——驱动器自己报错")
            failed.append(mid)
            continue
        after = reader(mp)
        ok, detail = fn(before, after, mp)
        rows.append(("RED-OK" if ok else "RED-BAD", mid, desc, detail))
        if not ok:
            failed.append(mid)

    # ------------------------------------------------------------ 探针 P1
    pmid, pdesc, pold, pnew = PROBE
    pmp = MUTD / f"check-figure-style.{pmid}.py"
    probe_row = None
    try:
        mutate(src, pold, pnew, pmp)
        ok, detail = p1(pmp)
        probe_row = ("RED-OK" if ok else "RED-BAD", pmid, pdesc, detail)
        if not ok:
            failed.append(pmid)
    except AssertionError as e:
        print(f"RED-BAD  {pmid}  {e}——驱动器自己报错")
        failed.append(pmid)

    print("\n" + "=" * 78)
    print("逐条结果")
    print("=" * 78)
    for st, mid, desc, detail in rows:
        print(f"{st:<8} {mid:<4} {desc}")
        print(f"         {detail}")
    if probe_row:
        print("-" * 78)
        print("变异探针（被打的不是判据，是验收脚本的 ERROR 分支）")
        print(f"{probe_row[0]:<8} {probe_row[1]:<4} {probe_row[2]}")
        print(f"         {probe_row[3]}")

    # ------------------------------------------------------------ 还原自证
    now_hash = git_hash_object(CHK)
    byte_ok = CHK.read_bytes() == src
    for f in MUTD.glob("*"):
        f.unlink()
    MUTD.rmdir()
    clean = not MUTD.exists()
    rerun = subprocess.run([sys.executable, str(FIX / "run-expected.py")], capture_output=True, text=True)

    print("\n" + "=" * 78)
    print("还原自证")
    print("=" * 78)
    print(f"  check-figure-style.py  blob  {now_hash}  {'== 变异前' if now_hash == base_hash else '!= 变异前 <<<'}")
    print(f"  工作树字节 == 变异前字节: {byte_ok}")
    print(f"  fixtures/_mut/ 已清空: {clean}")
    print(f"  还原后复跑逐格验收: exit={rerun.returncode}  {rerun.stdout.strip().splitlines()[-1]}")
    n_probe = 1 if probe_row else 0
    mut_failed = [m for m in failed if m != pmid]
    probe_ok = bool(probe_row) and probe_row[0] == "RED-OK"

    rows_h, failed_h, selfok_h, grp = run_house()

    # `rows_h` 里含探针 R1 那条（不是判据变异）⇒ 统计时单列
    n_spec = grp["house"] + grp["census"]                 # M9–M19 + C1/C2
    n_struct = grp["struct"]                              # M22–M28
    n_skill = grp["skill"]                                # M29–M39（+ M34/M40/M41）
    n_spec_ok = n_spec - len(grp["f_house"]) - len(grp["f_census"])
    n_struct_ok = n_struct - len(grp["f_struct"])
    n_skill_ok = n_skill - len(grp["f_skill"])
    r1_ok = grp["probe_row"][0] == "RED-OK"

    print("\n" + "=" * 78)
    print("合计")
    print("=" * 78)
    print(f"MUT: {len(rows) - len(mut_failed)}/{len(MUTATIONS)} 红（check-figure-style.py）"
          + ("" if not mut_failed else f"（未达预期：{', '.join(mut_failed)}）"))
    print(f"MUT: {n_spec_ok}/{n_spec} 红（house-style.md / provenance.md 的规范数守卫："
          f"{grp['house']} 条 `--only` + {grp['census']} 条 CENSUS 全跑）"
          + ("" if not (grp["f_house"] + grp["f_census"])
             else f"（未达预期：{', '.join(grp['f_house'] + grp['f_census'])}）"))
    print(f"MUT: {n_struct_ok}/{n_struct} 红（chart-types.md 的结构守卫 S1/S2/S3/S5：{n_struct} 条 `--only`）"
          + ("" if not grp["f_struct"] else f"（未达预期：{', '.join(grp['f_struct'])}）"))
    n_skill_copy = len(skill_mutations())                 # 打 SKILL.md 副本的那几条
    print(f"MUT: {n_skill_ok}/{n_skill} 红（SKILL.md 的短契约守卫 K1–K8：{n_skill} 条"
          f"（{n_skill_copy} 条打 SKILL.md 副本 + {n_skill - n_skill_copy} 条打别的："
          f"`K3` fail-closed 臂 / `K6` 反向臂 / `K8`））"
          + ("" if not grp["f_skill"] else f"（未达预期：{', '.join(grp['f_skill'])}）"))
    print(f"MUT: {len(rows) - len(mut_failed) + n_spec_ok + n_struct_ok + n_skill_ok}/"
          f"{len(MUTATIONS) + n_spec + n_struct + n_skill} 红（合计）")
    print(f"探针 P1: {'红' if probe_ok else '未红'}（check-figure-style.py 的脚本探针）")
    print(f"探针 R1: {'红' if r1_ok else '未红'}（读数条 S4 的『该动的时候动、该判的时候不判』）")
    print(f"（本驱动器共 {len(MUTATIONS)} 条检查器判据变异 + {n_probe} 条脚本探针"
          f" + {n_spec} 条规范数变异 + {n_struct} 条结构变异 + {n_skill} 条 SKILL.md 变异"
          f" + 1 条读数条探针）")
    return 0 if (not failed and not failed_h and byte_ok and clean and selfok_h
                 and rerun.returncode == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
