==============================================================================
tests/skills/figure-choose/green-evidence.md —— Task 6 GREEN 对照证据（逐字）
==============================================================================

【范围】3 个场景（R1 构成数据 / R2 多变量对比 / R3 交付形态）× 2 层判据：
        机械层 = Task 1 的 `check-figure-style.py`（**一字不改**，直接调用）；
        判断层 = 独立判者（判词逐字见 `green/judge-green.md`，本文 §7 全文内联）。
        **RED 基线** = `red/`（本次 commit 当场重跑，见 §3）；GREEN = `green/out-G{1,2,3}/`。
【机器】Windows 11 / Python 3.11.9
【起始 commit】Task 6 的实现自 `e2aa240` 起；**本轮（口径收敛轮）从 `608d0e2` 起**
  （分支 `feat/m6-corpus-pipeline`）—— 本轮由复审的 Important-2 逼出，改了 F3b 一处口径（§6-2）。
【写手与判者的身份】三个 GREEN 写手 + 一位判者**全部是 `general-purpose` 全新 subagent，未用 `fork`**。
  这一条**不是自报**：`fork` 会继承主 agent 上下文，其 transcript 的**首条 user 消息**会是
  长篇上下文；而实测三个写手 + 判者的首条 user 消息就是**那一条提示词本身**（逐字见 §0.3
  与 `green/green-self-reports.md`）。

【本文件怎么来的】由同目录的 `make-evidence.py` 用 `write_bytes` 生成（LF）。
  **文中每一个数都来自本脚本当场跑过的命令**，命令与输出逐字附在文内；
  红绿表与两个汇总数（§4）由当场输出**逐格重算**，不是手写的。
  生成器与它生成的证据**同在受版本控制的目录里**。

【对捕获输出的唯一加工】
1) 命令一律以**仓库相对路径**写出（cwd = 仓根）；
2) 系统临时目录的绝对路径剥成 `<TMP>/`（本仓规定不写绝对路径）；
3) 其余**逐字未改**。每个块尾的 `[exit=..]` 是该命令的真实退出码。
   **凡有节略一律当场标明**。

【分母口径】同 Task 1/2：`--textwidth-in` 一律传 **6.31**
（= 逐篇正文行宽 p90 的全局中位，见 `tests/figures-recon/b-stats.txt`
`col_w_in: n=43 ... median=6.310`）。检查器**不预设**口径。

==============================================================================
§0 公平性：GREEN 与 RED 的差别**只允许**有"能不能读 skill"这一条（四条逐条取证）
==============================================================================

本任务是**对照实验**：唯一被操纵的自变量是"写手能不能读 `.claude/skills/mcm-figure-choose/`"。
下面四条把"只有这一条不同"落成可复核的读数。

### 0.1 场景逐字复用（三条，字节级）

场景正文取自 `red/brief-R{1,2,3}.md`（Task 2 已核过它们与 `red/README.md` §1 的内联副本
逐字节相同）。写手拿到的是**仓外**副本，做法：`read_bytes()` 原样写出，再逐条比 blob。

```
$ python - <<PY   # 逐份比 (仓内权威件) 与 (写手拿到的仓外副本) 的字节
import pathlib, subprocess
for n in (1, 2, 3):
    a = pathlib.Path('tests/skills/figure-choose/red/brief-R%d.md' % n)
    b = pathlib.Path('<TMP>/m3-t6-green/brief-R%d.md' % n)
    ga = subprocess.run(['git', 'hash-object', a.as_posix()],
                        capture_output=True, text=True).stdout.strip()
    gb = subprocess.run(['git', 'hash-object', '--no-filters', b.as_posix()],
                        capture_output=True, text=True).stdout.strip()
    print('brief-R%d.md  bytes=%d  repo_blob=%s  temp_blob=%s  identical=%s'
          % (n, b.stat().st_size, ga[:12], gb[:12], a.read_bytes() == b.read_bytes()))
PY
brief-R1.md  bytes=1122  repo_blob=c0ef25227019  temp_blob=c0ef25227019  identical=True
brief-R2.md  bytes=2029  repo_blob=4596500881bf  temp_blob=4596500881bf  identical=True
brief-R3.md  bytes=1230  repo_blob=6749ab6e9681  temp_blob=6749ab6e9681  identical=True
[exit=0]
```
⇒ 三份场景**逐字节相同**（`read_bytes()` 直接比，不靠 blob 比 —— 见 §0.5 的一处口径坑）。

### 0.2 两侧用的是**同一支**检查器（同一时刻、同一把尺）+ 本轮的**一次口径收敛**登记

**本文上一版**在这一节写的是"`check-figure-style.py` 一个字节没动：工作树 blob == `HEAD` 的 blob"。
**口径收敛轮之后它不再成立** —— 本轮改了 F3b 一处（见 §6-2）。故改成**可复核**的说法：

- **公平性的实质**是"RED 与 GREEN 用**同一支**检查器、**同一组参数**、**同一时刻**去量"，
  而不是"检查器永不改"。本文 §2–§4 的两侧读数**全部由同一支（收敛后）检查器当场跑出**。
- **收敛的唯一改动**：F3b 由 `len(cap.split())` 改成 `len(caption_body(cap).split())`
  —— **常量 `CAP_MAX=12` / `CAP_HARD=17` 与 `G-H9-*` 守卫一个没动**。
- **收敛对两侧的影响**（本文都在）：GREEN 三份 F3b **由红转绿**；RED 三份读数**一字未变**。
- 下面那条 `git status --short` 因此**非空** —— 这是**如实打印**，不是残留。

```text
$ git hash-object tests/skills/figure-choose/check-figure-style.py
7636902a868aeca105e6b75b7dc616816fce95fe
$ git rev-parse HEAD:tests/skills/figure-choose/check-figure-style.py
7636902a868aeca105e6b75b7dc616816fce95fe
$ git status --short tests/skills/figure-choose/check-figure-style.py
(无输出 = 未改动)
```

### 0.3 写手提示词：RED 第二轮 vs GREEN，**只许改"隔离句"这一处**

两版提示词都**不是手抄的**：脚本从两边的 transcript 抢救件里按原文取出（`### ① 派发提示词（原文）`），
再与脚本里写死的模板**逐字节断言相等**。断言结果（下面这段是脚本当场打印的，不是我写的）：

```
$ python - <<PY   # 模板 vs transcript 原文逐字节断言 + 抹掉临时目录名后 diff

import pathlib, re, difflib

RED_TMPL = 'Read the brief at <TMP>/m3-t2-red/brief-R{n}.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R{n}/. Work only from that brief - do not read or write any other file.'
GREEN_TMPL = 'Read the brief at <TMP>/m3-t6-green/brief-R{n}.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t6-green/out-R{n}/. Work from that brief and the skill at .claude/skills/mcm-figure-choose/ - do not read or write any other file.'

def extract(md, wanted):
    txt = md.read_bytes().decode("utf-8")
    got = {}
    for chunk in txt.split("### ① 派发提示词（原文）")[1:]:
        m = re.search(r"```text\n(.*?)\n```", chunk, re.S)
        if not m:
            continue
        tag = re.findall(r"^## (\S+)$", txt[:txt.index(chunk)], re.M)[-1]
        if tag in wanted:
            got[tag] = m.group(1)
    return got

red = extract(pathlib.Path("tests/skills/figure-choose/red/writer-self-reports.md"),
              {"R1-writer-round-2", "R2-writer-round-2", "R3-writer-round-2"})
grn = extract(pathlib.Path("tests/skills/figure-choose/green/green-self-reports.md"),
              {"R1-writer-green", "R2-writer-green", "R3-writer-green"})

print("(1) 模板 vs transcript 原文，逐字节断言（True = 文里贴的就是派发出去的那一条）")
for n in (1, 2, 3):
    r = red["R%d-writer-round-2" % n]
    g = grn["R%d-writer-green" % n]
    print("  R%d: RED-2==transcript=%s (len=%d)   GREEN==transcript=%s (len=%d)"
          % (n, r == RED_TMPL.replace("{n}", str(n)), len(r),
             g == GREEN_TMPL.replace("{n}", str(n)), len(g)))

print()
print("(2) 抹掉两版临时目录名这一个 token 后再 diff")
a2 = re.sub(r"<TMP>/m3-t[0-9a-z-]+", "<TMP>/m3-tX", red["R1-writer-round-2"])
b2 = re.sub(r"<TMP>/m3-t[0-9a-z-]+", "<TMP>/m3-tX", grn["R1-writer-green"])
ops = [o for o in difflib.SequenceMatcher(None, a2, b2, autojunk=False).get_opcodes()
       if o[0] != "equal"]
print("  difflib 的非 equal 段数 = %d" % len(ops))
for tag, i1, i2, j1, j2 in ops:
    print("    %-8s RED-2[%d:%d] = %r" % (tag, i1, i2, a2[i1:i2]))
    print("             GREEN[%d:%d] = %r" % (j1, j2, b2[j1:j2]))
P = 0
while P < min(len(a2), len(b2)) and a2[P] == b2[P]:
    P += 1
S = 0
while S < min(len(a2), len(b2)) - P and a2[-1 - S] == b2[-1 - S]:
    S += 1
print("  公共前缀 %d 字符 / 公共后缀 %d 字符" % (P, S))
print("  RED-2 改动区间 = %r" % a2[P:len(a2) - S])
print("  GREEN 改动区间 = %r" % b2[P:len(b2) - S])
print("  公共后缀 = %r" % b2[len(b2) - S:])
print("  后缀（含禁止句）逐字节未动 =", a2[len(a2) - S:] == b2[len(b2) - S:])
PY
(1) 模板 vs transcript 原文，逐字节断言（True = 文里贴的就是派发出去的那一条）
  R1: RED-2==transcript=True (len=247)   GREEN==transcript=True (len=297)
  R2: RED-2==transcript=True (len=247)   GREEN==transcript=True (len=297)
  R3: RED-2==transcript=True (len=247)   GREEN==transcript=True (len=297)

(2) 抹掉两版临时目录名这一个 token 后再 diff
  difflib 的非 equal 段数 = 2
    delete   RED-2[180:185] = 'only '
             GREEN[180:180] = ''
    insert   RED-2[200:200] = ''
             GREEN[195:246] = ' and the skill at .claude/skills/mcm-figure-choose/'
  公共前缀 180 字符 / 公共后缀 39 字符
  RED-2 改动区间 = 'only from that brief'
  GREEN 改动区间 = 'from that brief and the skill at .claude/skills/mcm-figure-choose/'
  公共后缀 = ' - do not read or write any other file.'
  后缀（含禁止句）逐字节未动 = True
[exit=0]
```
**两版原文并排（R1；R2/R3 只换文件名，见 `green/green-self-reports.md` 与 `red/writer-self-reports.md`）**：

```text
[RED-2]   Read the brief at <TMP>/m3-t2-red/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t2-red/out-R1/. Work only from that brief - do not read or write any other file.

[GREEN]   Read the brief at <TMP>/m3-t6-green/brief-R1.md and produce the figure and caption it asks for. Write the script, the exported figure and the caption text into <TMP>/m3-t6-green/out-R1/. Work from that brief and the skill at .claude/skills/mcm-figure-choose/ - do not read or write any other file.
```
⇒ 抹掉临时目录名（两版**必然**不同的那一个路径 token）之后，**改动区间只有一段**：
RED-2 是 `only from that brief`，GREEN 是 `from that brief and the skill at
.claude/skills/mcm-figure-choose/`。difflib 报的是 **2 段**（一删一插），中间那段
`from that brief` **逐字保留** —— 所以"一删一插是两段"与"改动只落在这一个从句内"**两句话都对**，
不许把前者读成"改了两处"。**从句之外（含禁止句 ` - do not read or write any other file.`）
逐字节相同** ⇒ GREEN 侧**仍然禁止**读 `red/`、`docs/`、检查器、`fixtures/` 等一切其它文件，
**新放开的只有那一个 skill 目录**。

（写手拿到的真实提示词里是**绝对路径**；本文里的 `<TMP>/m3-t6-green` 是掩码，
掩码处数与完整原文见 `green/green-self-reports.md` 文首。）

### 0.4 隔离强度：GREEN 写手不得接触 `red/` 下的任何东西（除场景本身）

- **结构上做到的**：写手拿到的是**仓外**副本（§0.1 逐字节相同），提示词里只给"那一份 brief 的
  路径 + 输出目录 + skill 目录"，**没有**给 `red/` 的任何路径。
- **只有自报、无沙箱可证**：三个写手各自的报告里都写了"只读了那一份 brief 与 skill 目录"，
  原文逐字在 `green/green-self-reports.md`。**没有**文件系统审计、**没有** syscall 记录、
  **没有**哈希链 ⇒ **"自报一致"不等于"已证"**，不许下游读过头。
- 能复核的只有一件事：**未用 `fork`**（首条 user 消息就是那条提示词本身，见本文件文首）。

### 0.5 一处口径坑（当场实测，写下来免得下游踩）

`git hash-object <仓外临时路径>` 会**对文件施加 core.autocrlf 规范化**（该路径不在
`.gitattributes` 的 `-text` 覆盖范围内），而 `git hash-object <仓内路径>` 不会
（`tests/skills/**` 有 `-text`）。实测后果：`green/out-G2/caption.txt` 含一个 CRLF，
于是**同一份字节**在两条路径上给出**两个不同的 blob**。⇒ 本文的"逐字节相同"一律用
**`read_bytes()` 直接比**判定，`git hash-object` 只在**同为仓内路径**时用于对照 `HEAD`。
这条是 Task 6 当场撞出来的，RED 那一轮没撞到（RED 的三份图注都是 LF）。

==============================================================================
§1 场景与地面真值（指向 `red/`，不重复）
==============================================================================

三份场景**就是** `red/brief-R{{1,2,3}}.md`（§0.1 已证与写手拿到的副本逐字节相同）；
场景正文与两问的**唯一确定答案**（R1 的 B–D 相似对、R2 的 mean_slope）逐字见
`red/README.md` §1 与 `red/red-evidence.md` §1（含 `truth.py` 的当场输出与命令）。
**本文不复述**，避免造第二份权威。

==============================================================================
§2 机械层逐字读数（同一把尺、同一组参数）
==============================================================================

三份 GREEN 产物各有 `figure.pdf`（矢量）与 `figure.png`（栅格）。
**下面是本脚本当场跑出来的完整输出。** 先 green，再 RED 基线（同一次运行里重跑）。

### 2.1 GREEN：`--textwidth-in 6.31`（PDF 载体；PNG 那一组按 Task 2 Step 3 的命令形状）

Task 2 Step 3 命令里的 `--dpi` 写的是**占位符** `--dpi <导出 dpi>`，**不是字面 300**
（逐字见 `.superpowers/sdd/task-m3-t2-brief.md` 的 Step 3 那一行）。字面 `300` 只出现在
`red/red-evidence.md`，因为 RED 三份**恰好**都导出 300 dpi。下面 PNG 那一组沿用 `300`，
**下一节立刻说明它为什么只对 RED 成立**。

**out-G1/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G1/figure.pdf --caption @tests/skills/figure-choose/green/out-G1/caption.txt --textwidth-in 6.31
PASS  F1  图宽比 0.951（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G2/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G2/figure.pdf --caption @tests/skills/figure-choose/green/out-G2/caption.txt --textwidth-in 6.31
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 0
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G3/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G3/figure.pdf --caption @tests/skills/figure-choose/green/out-G3/caption.txt --textwidth-in 6.31
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G1/figure.png（`--dpi 300`，= 把 RED 的取值硬套过来）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G1/figure.png --caption @tests/skills/figure-choose/green/out-G1/caption.txt --textwidth-in 6.31 --dpi 300
PASS  F1  图宽比 0.951（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G2/figure.png（`--dpi 300`，= 把 RED 的取值硬套过来）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G2/figure.png --caption @tests/skills/figure-choose/green/out-G2/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 0.667（分母 6.31 in）
PASS  F2  彩色主色数 0
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: FAIL（F1）
[exit=1]
```
**out-G3/figure.png（`--dpi 300`，= 把 RED 的取值硬套过来）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G3/figure.png --caption @tests/skills/figure-choose/green/out-G3/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 0.667（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: FAIL（F1）
[exit=1]
```

### 2.2 ★ 一处必须说清的读数：PNG 的 `--dpi` 不是载体无关的

F1 对 PNG 的算法是 `宽_in = 像素宽 / --dpi`。Task 2 Step 3 命令里的 `--dpi` 是**占位符**；
字面 `300` 是 **RED 三份的真实导出 dpi**（见下表左三行），被当年的 RED 证据沿用成了具体值。
GREEN 的写手各自选了导出 dpi ⇒ 把 `300` 当"规定值"硬套，对 200 dpi 的 PNG 就会
**量错物理尺寸**（不是图变窄了）。

**真 dpi 的取法**（**不读 PNG 的 dpi 元信息** —— 检查器 `:152` 与 `provenance.md:20` 都禁止）：
`PNG 像素宽 ÷ PDF 页盒宽`（矢量面、精确，正是检查器判 PDF 的 F1 用的那条量法）
与写手脚本里的 `savefig(..., dpi=N)` 字面量，两条独立证据交叉；两者不一致时脚本直接断言失败。
实测（下面这段是当场跑的）：

```
$ python - <<PY   # 真实导出 dpi 的两条独立证据（不读 PNG 的 dpi 元信息）

import pathlib, re
import fitz
from PIL import Image

for tag, base in (("RED", "tests/skills/figure-choose/red/out-R%d"),
                  ("GREEN", "tests/skills/figure-choose/green/out-G%d")):
    for n in (1, 2, 3):
        b = base % n
        im = Image.open(b + "/figure.png")
        with fitz.open(b + "/figure.pdf") as d:
            win, hin = d[0].rect.width / 72.0, d[0].rect.height / 72.0
        src = pathlib.Path(b + "/make_figure.py").read_bytes().decode("utf-8")
        lit = sorted(set(re.findall(r"savefig\(.*?dpi=(\d+)", src)))
        print("%-5s R%d  png %dx%d px | pdf 页盒 %.4f x %.4f in | 隐含 dpi %8.3f | 脚本 savefig dpi= %s"
              % (tag, n, im.size[0], im.size[1], win, hin, im.size[0] / win,
                 ",".join(lit) or "(无)"))
PY
RED   R1  png 2880x1350 px | pdf 页盒 9.6000 x 4.5000 in | 隐含 dpi  300.000 | 脚本 savefig dpi= (无)
RED   R2  png 3300x2520 px | pdf 页盒 11.0000 x 8.4000 in | 隐含 dpi  300.000 | 脚本 savefig dpi= 300
RED   R3  png 2280x1200 px | pdf 页盒 7.6000 x 4.0000 in | 隐含 dpi  300.000 | 脚本 savefig dpi= 300
GREEN R1  png 1800x780 px | pdf 页盒 6.0000 x 2.6000 in | 隐含 dpi  300.000 | 脚本 savefig dpi= 300
GREEN R2  png 1262x950 px | pdf 页盒 6.3100 x 4.7500 in | 隐含 dpi  200.000 | 脚本 savefig dpi= 200
GREEN R3  png 1262x580 px | pdf 页盒 6.3100 x 2.9000 in | 隐含 dpi  200.000 | 脚本 savefig dpi= 200
[exit=0]
```
⇒ GREEN 的 R2/R3 导出的是 **200 dpi**（RED 三份与 GREEN R1 都是 300 dpi；
RED 的 `make_figure.py` 里没有 `savefig dpi=` 字面量 ⇒ RED 只有"页盒"这一条证据，
与 RED 证据里用的 300 不冲突）。
故本节**再加一组读数**：按每张 PNG 的**实际导出 dpi** 读一次。这是**追加**读数，
不改判据、也不改任务书那条命令 —— `--dpi 300` 与"真实 dpi"两组都逐字列出，哪个对哪个错由读者判。

**out-G1/figure.png（`--dpi 300` = 该文件的真实导出 dpi，两条证据交叉得出）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G1/figure.png --caption @tests/skills/figure-choose/green/out-G1/caption.txt --textwidth-in 6.31 --dpi 300
PASS  F1  图宽比 0.951（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G2/figure.png（`--dpi 200` = 该文件的真实导出 dpi，两条证据交叉得出）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G2/figure.png --caption @tests/skills/figure-choose/green/out-G2/caption.txt --textwidth-in 6.31 --dpi 200
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 0
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
**out-G3/figure.png（`--dpi 200` = 该文件的真实导出 dpi，两条证据交叉得出）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/green/out-G3/figure.png --caption @tests/skills/figure-choose/green/out-G3/caption.txt --textwidth-in 6.31 --dpi 200
PASS  F1  图宽比 1.000（分母 6.31 in）
PASS  F2  彩色主色数 3
PASS  F3a  图注以 `Figure N:` 起
PASS  F3b  图注词数 11（上限 12，硬上限 17）
PASS  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 11 词）
RESULT: PASS
[exit=0]
```
### 2.3 RED 基线：**本次 commit 当场重跑**（不是从 `red-evidence.md` 抄的）

任务书要求"RED × GREEN 并列"；为了让两侧**在同一时刻、同一把尺**上比，
下面的 RED 读数是本脚本当场重跑的（`red/` 是只读的，跑检查器不改任何东西）。

**red/out-R1/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R1/figure.pdf --caption @tests/skills/figure-choose/red/out-R1/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.521（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 203 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 203 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]
```
**red/out-R2/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R2/figure.pdf --caption @tests/skills/figure-choose/red/out-R2/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.743（分母 6.31 in）
FAIL  F2  彩色主色数 7
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 285 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 285 词）
RESULT: FAIL（F1,F2,F3a,F3b,F3c）
[exit=1]
```
**red/out-R3/figure.pdf**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R3/figure.pdf --caption @tests/skills/figure-choose/red/out-R3/caption.txt --textwidth-in 6.31
FAIL  F1  图宽比 1.204（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 177 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 177 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]
```
**red/out-R1/figure.png（`--dpi 300` = 实测该 PNG 的真实导出 dpi）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R1/figure.png --caption @tests/skills/figure-choose/red/out-R1/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.521（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 203 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 203 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]
```
**red/out-R2/figure.png（`--dpi 300` = 实测该 PNG 的真实导出 dpi）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R2/figure.png --caption @tests/skills/figure-choose/red/out-R2/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.743（分母 6.31 in）
FAIL  F2  彩色主色数 7
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 285 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 285 词）
RESULT: FAIL（F1,F2,F3a,F3b,F3c）
[exit=1]
```
**red/out-R3/figure.png（`--dpi 300` = 实测该 PNG 的真实导出 dpi）**

```
$ python tests/skills/figure-choose/check-figure-style.py --fig tests/skills/figure-choose/red/out-R3/figure.png --caption @tests/skills/figure-choose/red/out-R3/caption.txt --textwidth-in 6.31 --dpi 300
FAIL  F1  图宽比 1.204（分母 6.31 in）
PASS  F2  彩色主色数 3
FAIL  F3a  图注以 `Figure N:` 起
FAIL  F3b  图注词数 177 超硬上限 17
FAIL  F3c  句末不加句号
PASS  F3d  图注正文非空（正文 177 词）
RESULT: FAIL（F1,F3a,F3b,F3c）
[exit=1]
```
### 2.4 三份图注逐字（全文、`cat`）—— F3a/b/c 的直接原因

```
$ cat tests/skills/figure-choose/red/out-R1/caption.txt    # 1215 B
Figure 1. Vulnerability composition of the six districts (A-F). (a) For every
district the land area is partitioned into three vulnerability tiers (low,
medium, high); the three shares sum to 1.00 by construction. Low-vulnerability
land ranges from 0.28 (D) to 0.55 (C), and the high tier is the smallest
component everywhere, varying only between 0.15 (C) and 0.25 (B, D, E). (b) The
same six compositions placed in the low-medium-high simplex, in which one
district is one point, so that similarity of structure is simply proximity.
Districts B and D (circled) are the closest pair: their Aitchison distance, the
Euclidean distance between centred log-ratios and the standard metric for
shares, is 0.12, smaller than for any other pair - the next closest, C-F and
A-E, stand at 0.17, and every remaining pair lies above 0.22. The plain
Euclidean distance between the share vectors selects the same pair first
(0.04), so the judgement does not hinge on the choice of metric. The two
districts are close to structurally interchangeable: each gives exactly one
quarter of its area to the high tier and they differ by only 0.03 in how the
rest is split between low and medium (0.31/0.44 in B against 0.28/0.47 in D).

$ cat tests/skills/figure-choose/red/out-R2/caption.txt    # 1775 B
Figure 1. Drivers of the historical disaster count and similarity of the six districts (A-F).
(a) Pearson r and Spearman rho between each measured factor and the historical disaster
count (n = 6), ordered by |r|. Mean slope is the factor most strongly correlated with the
disaster count (r = +0.93, rho = +0.94); the infrastructure index (r = -0.78, rho = -0.77)
and vegetation cover (r = -0.74, rho = -0.77) are moderately and negatively correlated, and
population density is only weakly correlated (r = +0.36, rho = +0.54).
(b) Disaster count against mean slope, the strongest correlate; the least-squares line
(y = 2.20x + 5.37) accounts for 87% of the variance, and the two extremes, district C
(2.4 degrees, 8 events) and district D (14.8 degrees, 38 events), are highlighted.
(c) Standardised attribute profiles (z-scores across the six districts), with rows ordered by
the clustering in (d); red marks above-average and blue below-average values.
(d) Dendrogram of the districts obtained by average-linkage clustering on the four
standardised drivers (Euclidean distance): A and C are the closest pair, B and E form the
next pair, and D is the most distinct district, combining the steepest mean slope with the
lowest vegetation cover and infrastructure index and the highest disaster count.
Two caveats apply. First, these are marginal associations rather than independent effects:
with only six districts, and with the infrastructure index and vegetation cover themselves
correlated at r = 0.98, their separate contributions cannot be disentangled, and no causal
direction is implied. Second, the ordering within the middle group (B, E, F) is only weakly
resolved, so the robust features of the similarity structure are the A-C pair and the
isolation of district D.

$ cat tests/skills/figure-choose/red/out-R3/caption.txt    # 1063 B
Figure 1. Vulnerability composition of the six districts (A-F). (a) Land-area
shares of the low, medium and high vulnerability tiers, which sum to 1.00 within
each district; districts are ordered by decreasing low-tier share. C
(0.55/0.30/0.15) and F (0.50/0.33/0.17) are the least vulnerable, A
(0.42/0.35/0.23) and E (0.37/0.38/0.25) are intermediate, and B (0.31/0.44/0.25)
and D (0.28/0.47/0.25) are the most heavily weighted towards the medium tier;
the high tier is the smallest component in every district and spans only 0.15 to
0.25. (b) The same data in the composition triangle, where each district is a
single point whose three shares are read off the three axes, so that structural
similarity is geometric proximity; B, D and E, all with a high-tier share of
0.25, lie on one horizontal line. The red segment marks the most similar pair: B
and D differ by 0.03 in total (total-variation distance), the smallest of all 15
district pairs, and the next closest pairs, A-E and C-F, differ by 0.05. B and D
are adjacent in (a) as a result of the ordering.

$ cat tests/skills/figure-choose/green/out-G1/caption.txt    # 79 B
Figure 1: Land-area vulnerability shares by district; B and D are most similar

$ cat tests/skills/figure-choose/green/out-G2/caption.txt    # 68 B
Figure 1: Scatter panels rank slope first; A and C share a profile

$ cat tests/skills/figure-choose/green/out-G3/caption.txt    # 85 B
Figure 1: Land-area vulnerability composition of six districts; B and D most similar

```
**读数**：三份 GREEN 图注**全部**是 `Figure N:` + **ASCII 冒号** + 句末**无**句号
（RED 三份是 `Figure 1.` **句点** + 句末**有**句号）。⇒ F3a、F3c 三份**全部由红转绿**。

**F3b 与 F3d 现在**打印的是同一个词数（正文 **11** 词）⇒ F3b **转绿**。本轮之前它曾是全红，
成因是检查器 F3b 数**整条图注**（含 `Figure N:` 这一段）而 H9 的上限 12 词写的是
**去掉标签后的正文**：同一批 662 条图上两个口径**相差恰好 2 词**、不可互换（登记在
`references/provenance.md` 的 **P-D-c1**，其 `:385-386` 早在本轮之前就写明了这条分叉）。
**本轮把 F3b 收敛到规范侧**（`len(caption_body(cap).split())`，常量 12 / 17 与 `G-H9-*` 一个没动），
GREEN 三份随即转绿、RED 三份的读数**一字不变**（RED 的图注以 `Figure 1.` 起 ⇒ 切不出前缀 ⇒ 整条算正文）。
⇒ 上一版本文里那句"**新暴露的口径分歧**"是 **overclaim**（仓内三处早有记录），本轮已改正，见 §6-2。

==============================================================================
§3 RED 基线的逐格重算（核任务书给的 13 红 / 5 绿）
==============================================================================

任务书说 RED 基线是 **13 红 / 5 绿**。本文**不引用**那个数，而是**另起一次运行**，
把检查器在 RED 三份产物上重跑一遍、再从逐格判词重算汇总（下面这段真的跑过）：

```
$ python - <<PY   # RED 基线逐格重跑 + 从逐格判词重算汇总

import re, subprocess, sys

CH = "tests/skills/figure-choose/check-figure-style.py"
CRIT = ["F1", "F2", "F3a", "F3b", "F3c", "F3d"]

def verdicts(fig, cap):
    r = subprocess.run([sys.executable, CH, "--fig", fig, "--caption", "@" + cap,
                        "--textwidth-in", "6.31"], capture_output=True, text=True)
    got = {}
    for line in r.stdout.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(F\d[abcd]?)\s", line)
        if m:
            got[m.group(2)] = m.group(1)
    return got, r.returncode

for side, pat in (("RED", "tests/skills/figure-choose/red/out-R%d"),
                  ("GREEN", "tests/skills/figure-choose/green/out-G%d")):
    tot_r = tot_g = 0
    print("== %s（figure.pdf 载体，--textwidth-in 6.31）" % side)
    print("场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit")
    for n in (1, 2, 3):
        g, rc = verdicts(pat % n + "/figure.pdf", pat % n + "/caption.txt")
        v = "".join("R" if g[c] == "FAIL" else "G" for c in CRIT)
        nf = v.count("R")
        tot_r += nf
        tot_g += 6 - nf
        print("  %s%d | %s | %d | %d | %d" % (side[0], n, v, nf, 6 - nf, rc))
    print("  小计: 判红 %d 格 / 满 %d 格；绿 %d 格" % (tot_r, tot_r + tot_g, tot_g))
    print()
PY
== RED（figure.pdf 载体，--textwidth-in 6.31）
场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit
  R1 | RGRRRG | 4 | 2 | 1
  R2 | RRRRRG | 5 | 1 | 1
  R3 | RGRRRG | 4 | 2 | 1
  小计: 判红 13 格 / 满 18 格；绿 5 格

== GREEN（figure.pdf 载体，--textwidth-in 6.31）
场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit
  G1 | GGGGGG | 0 | 6 | 0
  G2 | GGGGGG | 0 | 6 | 0
  G3 | GGGGGG | 0 | 6 | 0
  小计: 判红 0 格 / 满 18 格；绿 18 格

[exit=0]
```
⇒ **13 红 / 5 绿**，与任务书给的 13 / 5 **一致**（逐格比对见 §4）。

==============================================================================
§4 RED × GREEN 并列红绿表（PDF 主载体；逐格重算）
==============================================================================

**主表用 PDF 载体**：F1 走页盒、**与 dpi 无关**，是两侧唯一口径完全一致的载体
（PNG 侧的 `--dpi` 问题见 §2.2）。每格写作 `RED → GREEN`。

**表里有两层，不是一个维度**：机械层（`check-figure-style.py` 的六格）与**判断层**
（独立判者的结论）。任务书 `task-m3-t6-brief.md` 的 Interfaces 段点名要的就是
`R1/R2/R3 × (机械层 · 判断层) × (RED · GREEN)` 这个**三维**对照 —— 判词两列在表末。

| 场景 | F1 图宽比 | F2 主色数 | F3a 前缀 | F3b 词数 | F3c 句末 | F3d 非空 | 判断层 · **RED** 判词 | 判断层 · **GREEN** 判词 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R1** | **FAIL** 图宽比 1.521（分母 6.31 in） → PASS 图宽比 0.951（分母 6.31 in） | PASS 彩色主色数 3 → PASS 彩色主色数 3 | **FAIL** 图注以 `Figure N:` 起 → PASS 图注以 `Figure N:` 起 | **FAIL** 图注词数 203 超硬上限 17 → PASS 图注词数 11（上限 12，硬上限 17） | **FAIL** 句末不加句号 → PASS 句末不加句号 | PASS 图注正文非空（正文 203 词） → PASS 图注正文非空（正文 11 词） | correct | **correct**（堆叠柱） |
| **R2** | **FAIL** 图宽比 1.743（分母 6.31 in） → PASS 图宽比 1.000（分母 6.31 in） | **FAIL** 彩色主色数 7 → PASS 彩色主色数 0 | **FAIL** 图注以 `Figure N:` 起 → PASS 图注以 `Figure N:` 起 | **FAIL** 图注词数 285 超硬上限 17 → PASS 图注词数 11（上限 12，硬上限 17） | **FAIL** 句末不加句号 → PASS 句末不加句号 | PASS 图注正文非空（正文 285 词） → PASS 图注正文非空（正文 11 词） | correct | **correct**（按 \|r\| 排序的 4 个散点面板 + 平行坐标） |
| **R3** | **FAIL** 图宽比 1.204（分母 6.31 in） → PASS 图宽比 1.000（分母 6.31 in） | PASS 彩色主色数 3 → PASS 彩色主色数 3 | **FAIL** 图注以 `Figure N:` 起 → PASS 图注以 `Figure N:` 起 | **FAIL** 图注词数 177 超硬上限 17 → PASS 图注词数 11（上限 12，硬上限 17） | **FAIL** 句末不加句号 → PASS 句末不加句号 | PASS 图注正文非空（正文 177 词） → PASS 图注正文非空（正文 11 词） | correct（但三元图 low/medium 轴题互换，属标注错误） | **correct**（堆叠柱） |

**逐格汇总**：下表不是手写的，而是**另起一次运行**把两边重跑后从逐格判词重算出来的（与上表同源同尺，用来交叉核对）：

```
$ python - <<PY   # 两边各自重跑一遍，从逐格判词重算汇总

import re, subprocess, sys

CH = "tests/skills/figure-choose/check-figure-style.py"
CRIT = ["F1", "F2", "F3a", "F3b", "F3c", "F3d"]

def verdicts(fig, cap):
    r = subprocess.run([sys.executable, CH, "--fig", fig, "--caption", "@" + cap,
                        "--textwidth-in", "6.31"], capture_output=True, text=True)
    got = {}
    for line in r.stdout.splitlines():
        m = re.match(r"^(PASS|FAIL)\s+(F\d[abcd]?)\s", line)
        if m:
            got[m.group(2)] = m.group(1)
    return got, r.returncode

for side, pat in (("RED", "tests/skills/figure-choose/red/out-R%d"),
                  ("GREEN", "tests/skills/figure-choose/green/out-G%d")):
    tot_r = tot_g = 0
    print("== %s（figure.pdf 载体，--textwidth-in 6.31）" % side)
    print("场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit")
    for n in (1, 2, 3):
        g, rc = verdicts(pat % n + "/figure.pdf", pat % n + "/caption.txt")
        v = "".join("R" if g[c] == "FAIL" else "G" for c in CRIT)
        nf = v.count("R")
        tot_r += nf
        tot_g += 6 - nf
        print("  %s%d | %s | %d | %d | %d" % (side[0], n, v, nf, 6 - nf, rc))
    print("  小计: 判红 %d 格 / 满 %d 格；绿 %d 格" % (tot_r, tot_r + tot_g, tot_g))
    print()
PY
== RED（figure.pdf 载体，--textwidth-in 6.31）
场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit
  R1 | RGRRRG | 4 | 2 | 1
  R2 | RRRRRG | 5 | 1 | 1
  R3 | RGRRRG | 4 | 2 | 1
  小计: 判红 13 格 / 满 18 格；绿 5 格

== GREEN（figure.pdf 载体，--textwidth-in 6.31）
场景 | 逐格 (F1 F2 F3a F3b F3c F3d) | FAIL | PASS | exit
  G1 | GGGGGG | 0 | 6 | 0
  G2 | GGGGGG | 0 | 6 | 0
  G3 | GGGGGG | 0 | 6 | 0
  小计: 判红 0 格 / 满 18 格；绿 18 格

[exit=0]
```
⇒ **判红从 13 格降到 0 格**（两边汇总由上面那次运行独立重算，与本文表格所用读数一致）。

**★ 判断层：两侧同判 ⇒ 本轮在判断层上「零区分力」**（这一维上一版漏了，本轮补上）

- **RED 侧判词**（`red/judge.md`，机器从判词原表抽出，见上表末列）：三份**全部 `correct`**、
  饼图规则三份 `no`。唯一抓到的实质问题是 **R3 面板 (b) 的两条轴题（Low share / Medium share）互换**
  —— 属标注错误，不是图型选错。
- **GREEN 侧判词**（`green/judge-green.md` 同款抽取）：三份**全部 `**correct**（堆叠柱）`**、饼图规则三份 `no`。
- ⇒ **判断层两侧同判 `correct`**（`correct` ↔ `**correct**（堆叠柱）`）⇒ 这一层**没有区分力**，
  它**不能**用来支持"读了规范所以选型变对了"。这正是任务书那句"不许把『没失败』算成规范的功劳"
  在**判断层**上的同款情形 —— 机械层已在 §6-3 单列，判断层这一条在本节单列。
- **唯一有区分力的收获在 RED 侧**：**三元图轴题互换**是判者抓到的、而机械层六格**一条都看不见**
  （六格里没有能看见"轴题标反"的判据）。这条**不是**规范起作用的证据，而是"判断层能看见什么"的证据。

**PNG 载体（按各自真实导出 dpi）与 PDF 载体逐格一致** —— 即两侧的载体选择不影响结论；
若按任务书规定的 `--dpi 300` 硬套，GREEN 的 R2/R3 会凭空多出两个 F1 红（§2.2）。

==============================================================================
§5 F2 的"连续色图"闸门口径（★ 任务书点名要交代的那一条）
==============================================================================

`house-style.md` 的 H4 把 F2 的**条数**限定在**离散配色图**上：
`f2-diagnose.py` 报的**彩色箱数 ≥100** **或** **最高落选箱 ≥0.4%** ⇒ 按**连续色图**处理，
**不引用 F2 条数**。本文的三份 GREEN 产物到底是哪一类，**当场测**：

```
$ python tests/skills/figure-choose/red/f2-diagnose.py tests/skills/figure-choose/red/out-R1/figure.pdf tests/skills/figure-choose/red/out-R2/figure.pdf tests/skills/figure-choose/red/out-R3/figure.pdf tests/skills/figure-choose/green/out-G1/figure.pdf tests/skills/figure-choose/green/out-G2/figure.pdf tests/skills/figure-choose/green/out-G3/figure.pdf
=== tests/skills/figure-choose/red/out-R1/figure.pdf
    loaded_px=1440x675  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 3   => F2 PASS
    all chroma boxes kept (before floor): 78
      #1  bin(15, 14, 10)  share=  6.370%  >=FLOOR
      #2  bin(15, 11, 4)  share=  5.903%  >=FLOOR
      #3  bin(15, 3, 1)  share=  3.260%  >=FLOOR
      #4  bin(13, 4, 2)  share=  0.127%    below
      #5  bin(13, 12, 8)  share=  0.110%    below
      #6  bin(13, 9, 4)  share=  0.107%    below
      #7  bin(14, 10, 4)  share=  0.082%    below
      #8  bin(14, 13, 9)  share=  0.075%    below
      #9  bin(12, 9, 4)  share=  0.073%    below
      #10 bin(2, 3, 5)  share=  0.067%    below
      #11 bin(8, 7, 5)  share=  0.059%    below
      #12 bin(10, 9, 7)  share=  0.057%    below
      #13 bin(12, 4, 2)  share=  0.052%    below
      #14 bin(10, 8, 5)  share=  0.044%    below
      #15 bin(9, 8, 7)  share=  0.034%    below
      #16 bin(7, 6, 5)  share=  0.031%    below
      #17 bin(12, 11, 8)  share=  0.030%    below
      #18 bin(8, 4, 4)  share=  0.030%    below
      #19 bin(9, 4, 3)  share=  0.027%    below
      #20 bin(7, 5, 5)  share=  0.021%    below
      #21 bin(13, 3, 2)  share=  0.021%    below
      #22 bin(15, 14, 9)  share=  0.013%    below
      #23 bin(15, 4, 2)  share=  0.012%    below
      #24 bin(15, 3, 2)  share=  0.011%    below
      #25 bin(15, 10, 4)  share=  0.009%    below
      #26 bin(15, 8, 7)  share=  0.009%    below
      #27 bin(10, 7, 4)  share=  0.009%    below
      #28 bin(7, 7, 5)  share=  0.009%    below
      #29 bin(15, 10, 9)  share=  0.008%    below
      #30 bin(15, 9, 8)  share=  0.008%    below
      #31 bin(15, 6, 5)  share=  0.008%    below
      #32 bin(15, 5, 3)  share=  0.008%    below
      #33 bin(11, 8, 4)  share=  0.008%    below
      #34 bin(9, 9, 6)  share=  0.008%    below
      #35 bin(9, 4, 4)  share=  0.008%    below
      #36 bin(15, 13, 13)  share=  0.007%    below
      #37 bin(15, 7, 6)  share=  0.007%    below
      #38 bin(9, 7, 4)  share=  0.007%    below
      #39 bin(7, 6, 4)  share=  0.006%    below
      #40 bin(15, 5, 4)  share=  0.004%    below
      #41 bin(11, 10, 7)  share=  0.004%    below
      #42 bin(8, 8, 6)  share=  0.004%    below
      #43 bin(8, 6, 4)  share=  0.004%    below
      #44 bin(6, 5, 4)  share=  0.004%    below
      #45 bin(15, 13, 12)  share=  0.003%    below
      #46 bin(15, 12, 12)  share=  0.003%    below
      #47 bin(15, 11, 10)  share=  0.003%    below
      #48 bin(15, 10, 10)  share=  0.003%    below
      #49 bin(12, 12, 8)  share=  0.003%    below
      #50 bin(11, 11, 7)  share=  0.003%    below
      #51 bin(10, 10, 7)  share=  0.003%    below
      #52 bin(6, 5, 3)  share=  0.003%    below
      #53 bin(5, 6, 7)  share=  0.003%    below
      #54 bin(5, 5, 3)  share=  0.003%    below
      #55 bin(4, 5, 6)  share=  0.003%    below
      #56 bin(15, 12, 11)  share=  0.002%    below
      #57 bin(15, 7, 5)  share=  0.002%    below
      #58 bin(12, 11, 7)  share=  0.002%    below
      #59 bin(12, 8, 4)  share=  0.002%    below
      #60 bin(11, 4, 3)  share=  0.002%    below
      #61 bin(10, 8, 4)  share=  0.002%    below
      #62 bin(9, 8, 6)  share=  0.002%    below
      #63 bin(3, 4, 5)  share=  0.002%    below
      #64 bin(3, 3, 5)  share=  0.002%    below
      #65 bin(15, 13, 9)  share=  0.001%    below
      #66 bin(15, 11, 11)  share=  0.001%    below
      #67 bin(15, 6, 4)  share=  0.001%    below
      #68 bin(15, 4, 3)  share=  0.001%    below
      #69 bin(13, 13, 8)  share=  0.001%    below
      #70 bin(11, 11, 8)  share=  0.001%    below
      #71 bin(10, 9, 6)  share=  0.001%    below
      #72 bin(8, 5, 4)  share=  0.001%    below
      #73 bin(7, 5, 4)  share=  0.001%    below
      #74 bin(6, 7, 8)  share=  0.001%    below
      #75 bin(6, 6, 5)  share=  0.001%    below
      #76 bin(5, 5, 6)  share=  0.001%    below
      #77 bin(5, 4, 3)  share=  0.001%    below
      #78 bin(4, 4, 6)  share=  0.001%    below
    boundary: highest sub-floor box = 0.127%  |  lowest counted box = 3.260%  |  floor = 0.500%

=== tests/skills/figure-choose/red/out-R2/figure.pdf
    loaded_px=1650x1260  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 7   => F2 FAIL
    all chroma boxes kept (before floor): 152
      #1  bin(12, 13, 14)  share=  2.052%  >=FLOOR
      #2  bin(2, 4, 7)  share=  1.529%  >=FLOOR
      #3  bin(7, 11, 13)  share=  1.072%  >=FLOOR
      #4  bin(15, 14, 13)  share=  1.068%  >=FLOOR
      #5  bin(15, 12, 11)  share=  0.725%  >=FLOOR
      #6  bin(11, 13, 14)  share=  0.710%  >=FLOOR
      #7  bin(10, 1, 2)  share=  0.689%  >=FLOOR
      #8  bin(2, 6, 10)  share=  0.370%    below
      #9  bin(14, 9, 7)  share=  0.369%    below
      #10 bin(11, 1, 2)  share=  0.368%    below
      #11 bin(0, 4, 7)  share=  0.364%    below
      #12 bin(15, 12, 10)  share=  0.363%    below
      #13 bin(3, 8, 11)  share=  0.359%    below
      #14 bin(7, 0, 2)  share=  0.353%    below
      #15 bin(9, 12, 14)  share=  0.349%    below
      #16 bin(6, 10, 12)  share=  0.347%    below
      #17 bin(12, 3, 3)  share=  0.345%    below
      #18 bin(14, 8, 7)  share=  0.335%    below
      #19 bin(5, 9, 12)  share=  0.329%    below
      #20 bin(6, 7, 10)  share=  0.104%    below
      #21 bin(9, 10, 12)  share=  0.084%    below
      #22 bin(7, 8, 10)  share=  0.050%    below
      #23 bin(12, 14, 14)  share=  0.046%    below
      #24 bin(14, 11, 11)  share=  0.045%    below
      #25 bin(11, 4, 2)  share=  0.044%    below
      #26 bin(10, 11, 12)  share=  0.040%    below
      #27 bin(10, 11, 13)  share=  0.039%    below
      #28 bin(3, 5, 8)  share=  0.038%    below
      #29 bin(15, 13, 12)  share=  0.033%    below
      #30 bin(13, 14, 15)  share=  0.031%    below
      #31 bin(5, 7, 9)  share=  0.030%    below
      #32 bin(12, 9, 10)  share=  0.021%    below
      #33 bin(13, 9, 10)  share=  0.020%    below
      #34 bin(6, 7, 9)  share=  0.018%    below
      #35 bin(8, 9, 11)  share=  0.015%    below
      #36 bin(14, 12, 12)  share=  0.013%    below
      #37 bin(4, 6, 8)  share=  0.013%    below
      #38 bin(15, 11, 9)  share=  0.012%    below
      #39 bin(15, 10, 8)  share=  0.012%    below
      #40 bin(12, 4, 4)  share=  0.011%    below
      #41 bin(14, 8, 6)  share=  0.010%    below
      #42 bin(11, 4, 3)  share=  0.009%    below
      #43 bin(13, 6, 5)  share=  0.008%    below
      #44 bin(13, 5, 4)  share=  0.008%    below
      #45 bin(11, 2, 3)  share=  0.008%    below
      #46 bin(10, 13, 14)  share=  0.008%    below
      #47 bin(9, 12, 13)  share=  0.008%    below
      #48 bin(8, 11, 13)  share=  0.008%    below
      #49 bin(8, 0, 2)  share=  0.008%    below
      #50 bin(4, 9, 12)  share=  0.008%    below
      #51 bin(2, 7, 11)  share=  0.008%    below
      #52 bin(1, 5, 9)  share=  0.008%    below
      #53 bin(1, 4, 8)  share=  0.008%    below
      #54 bin(0, 3, 6)  share=  0.008%    below
      #55 bin(12, 7, 6)  share=  0.007%    below
      #56 bin(3, 5, 6)  share=  0.006%    below
      #57 bin(13, 10, 10)  share=  0.005%    below
      #58 bin(12, 10, 8)  share=  0.005%    below
      #59 bin(15, 14, 14)  share=  0.004%    below
      #60 bin(15, 13, 11)  share=  0.004%    below
      #61 bin(15, 9, 7)  share=  0.004%    below
      #62 bin(14, 7, 6)  share=  0.004%    below
      #63 bin(13, 12, 11)  share=  0.004%    below
      #64 bin(13, 7, 5)  share=  0.004%    below
      #65 bin(13, 6, 4)  share=  0.004%    below
      #66 bin(12, 8, 7)  share=  0.004%    below
      #67 bin(11, 3, 3)  share=  0.004%    below
      #68 bin(10, 12, 14)  share=  0.004%    below
      #69 bin(9, 1, 2)  share=  0.004%    below
      #70 bin(9, 0, 2)  share=  0.004%    below
      #71 bin(6, 10, 13)  share=  0.004%    below
      #72 bin(6, 9, 11)  share=  0.004%    below
      #73 bin(6, 0, 1)  share=  0.004%    below
      #74 bin(5, 10, 12)  share=  0.004%    below
      #75 bin(3, 7, 11)  share=  0.004%    below
      #76 bin(2, 6, 11)  share=  0.004%    below
      #77 bin(1, 6, 10)  share=  0.004%    below
      #78 bin(1, 5, 10)  share=  0.004%    below
      #79 bin(0, 3, 7)  share=  0.004%    below
      #80 bin(14, 13, 13)  share=  0.003%    below
      #81 bin(14, 13, 12)  share=  0.003%    below
      #82 bin(13, 10, 9)  share=  0.003%    below
      #83 bin(13, 9, 9)  share=  0.003%    below
      #84 bin(13, 9, 8)  share=  0.003%    below
      #85 bin(13, 8, 6)  share=  0.003%    below
      #86 bin(12, 8, 6)  share=  0.003%    below
      #87 bin(12, 6, 6)  share=  0.003%    below
      #88 bin(10, 12, 13)  share=  0.003%    below
      #89 bin(10, 6, 5)  share=  0.003%    below
      #90 bin(5, 8, 9)  share=  0.003%    below
      #91 bin(14, 11, 12)  share=  0.002%    below
      #92 bin(14, 11, 10)  share=  0.002%    below
      #93 bin(13, 11, 12)  share=  0.002%    below
      #94 bin(13, 8, 8)  share=  0.002%    below
      #95 bin(12, 8, 8)  share=  0.002%    below
      #96 bin(11, 13, 13)  share=  0.002%    below
      #97 bin(10, 8, 7)  share=  0.002%    below
      #98 bin(9, 6, 5)  share=  0.002%    below
      #99 bin(8, 10, 13)  share=  0.002%    below
      #100 bin(7, 10, 12)  share=  0.002%    below
      #101 bin(7, 10, 11)  share=  0.002%    below
      #102 bin(7, 6, 5)  share=  0.002%    below
      #103 bin(6, 8, 10)  share=  0.002%    below
      #104 bin(4, 7, 10)  share=  0.002%    below
      #105 bin(4, 7, 8)  share=  0.002%    below
      #106 bin(4, 5, 6)  share=  0.002%    below
      #107 bin(2, 3, 3)  share=  0.002%    below
      #108 bin(15, 13, 13)  share=  0.001%    below
      #109 bin(14, 12, 11)  share=  0.001%    below
      #110 bin(13, 11, 10)  share=  0.001%    below
      #111 bin(12, 9, 8)  share=  0.001%    below
      #112 bin(12, 4, 5)  share=  0.001%    below
      #113 bin(11, 12, 13)  share=  0.001%    below
      #114 bin(11, 11, 12)  share=  0.001%    below
      #115 bin(11, 9, 8)  share=  0.001%    below
      #116 bin(11, 9, 7)  share=  0.001%    below
      #117 bin(11, 8, 9)  share=  0.001%    below
      #118 bin(11, 5, 6)  share=  0.001%    below
      #119 bin(11, 5, 3)  share=  0.001%    below
      #120 bin(11, 4, 5)  share=  0.001%    below
      #121 bin(11, 3, 5)  share=  0.001%    below
      #122 bin(11, 3, 4)  share=  0.001%    below
      #123 bin(10, 11, 11)  share=  0.001%    below
      #124 bin(9, 11, 12)  share=  0.001%    below
      #125 bin(9, 10, 11)  share=  0.001%    below
      #126 bin(9, 7, 6)  share=  0.001%    below
      #127 bin(8, 10, 11)  share=  0.001%    below
      #128 bin(8, 9, 9)  share=  0.001%    below
      #129 bin(8, 7, 6)  share=  0.001%    below
      #130 bin(7, 9, 10)  share=  0.001%    below
      #131 bin(7, 9, 9)  share=  0.001%    below
      #132 bin(7, 8, 9)  share=  0.001%    below
      #133 bin(7, 5, 5)  share=  0.001%    below
      #134 bin(7, 4, 3)  share=  0.001%    below
      #135 bin(6, 10, 11)  share=  0.001%    below
      #136 bin(6, 9, 10)  share=  0.001%    below
      #137 bin(6, 7, 8)  share=  0.001%    below
      #138 bin(6, 5, 5)  share=  0.001%    below
      #139 bin(5, 8, 10)  share=  0.001%    below
      #140 bin(5, 6, 9)  share=  0.001%    below
      #141 bin(4, 9, 11)  share=  0.001%    below
      #142 bin(4, 6, 7)  share=  0.001%    below
      #143 bin(4, 5, 8)  share=  0.001%    below
      #144 bin(4, 4, 5)  share=  0.001%    below
      #145 bin(3, 7, 10)  share=  0.001%    below
      #146 bin(3, 5, 5)  share=  0.001%    below
      #147 bin(3, 4, 5)  share=  0.001%    below
      #148 bin(2, 4, 5)  share=  0.001%    below
      #149 bin(2, 4, 4)  share=  0.001%    below
      #150 bin(2, 3, 4)  share=  0.001%    below
      #151 bin(1, 2, 4)  share=  0.001%    below
      #152 bin(1, 2, 3)  share=  0.001%    below
    boundary: highest sub-floor box = 0.370%  |  lowest counted box = 0.689%  |  floor = 0.500%

=== tests/skills/figure-choose/red/out-R3/figure.pdf
    loaded_px=1140x600  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 3   => F2 PASS
    all chroma boxes kept (before floor): 93
      #1  bin(12, 13, 14)  share=  8.586%  >=FLOOR
      #2  bin(6, 10, 13)  share=  8.041%  >=FLOOR
      #3  bin(0, 5, 9)  share=  4.499%  >=FLOOR
      #4  bin(12, 3, 2)  share=  0.081%    below
      #5  bin(1, 3, 5)  share=  0.074%    below
      #6  bin(13, 14, 15)  share=  0.068%    below
      #7  bin(1, 3, 4)  share=  0.066%    below
      #8  bin(12, 14, 15)  share=  0.062%    below
      #9  bin(11, 13, 14)  share=  0.049%    below
      #10 bin(10, 12, 13)  share=  0.042%    below
      #11 bin(2, 6, 10)  share=  0.034%    below
      #12 bin(7, 11, 13)  share=  0.025%    below
      #13 bin(12, 4, 3)  share=  0.024%    below
      #14 bin(5, 8, 11)  share=  0.021%    below
      #15 bin(2, 5, 7)  share=  0.018%    below
      #16 bin(15, 13, 13)  share=  0.017%    below
      #17 bin(12, 6, 5)  share=  0.015%    below
      #18 bin(3, 6, 8)  share=  0.015%    below
      #19 bin(13, 9, 8)  share=  0.013%    below
      #20 bin(14, 11, 11)  share=  0.012%    below
      #21 bin(8, 10, 13)  share=  0.012%    below
      #22 bin(2, 4, 6)  share=  0.012%    below
      #23 bin(14, 12, 12)  share=  0.011%    below
      #24 bin(12, 5, 5)  share=  0.011%    below
      #25 bin(11, 12, 14)  share=  0.011%    below
      #26 bin(10, 11, 13)  share=  0.011%    below
      #27 bin(14, 10, 10)  share=  0.010%    below
      #28 bin(6, 8, 9)  share=  0.010%    below
      #29 bin(4, 7, 9)  share=  0.010%    below
      #30 bin(1, 5, 10)  share=  0.010%    below
      #31 bin(13, 9, 9)  share=  0.009%    below
      #32 bin(13, 8, 8)  share=  0.009%    below
      #33 bin(13, 6, 6)  share=  0.009%    below
      #34 bin(5, 7, 8)  share=  0.009%    below
      #35 bin(12, 5, 4)  share=  0.008%    below
      #36 bin(11, 12, 13)  share=  0.008%    below
      #37 bin(8, 10, 11)  share=  0.008%    below
      #38 bin(7, 9, 10)  share=  0.008%    below
      #39 bin(5, 9, 11)  share=  0.008%    below
      #40 bin(5, 6, 8)  share=  0.008%    below
      #41 bin(4, 8, 10)  share=  0.008%    below
      #42 bin(3, 5, 7)  share=  0.008%    below
      #43 bin(14, 12, 11)  share=  0.007%    below
      #44 bin(14, 11, 10)  share=  0.007%    below
      #45 bin(9, 11, 13)  share=  0.007%    below
      #46 bin(6, 9, 12)  share=  0.007%    below
      #47 bin(6, 7, 9)  share=  0.007%    below
      #48 bin(3, 5, 6)  share=  0.007%    below
      #49 bin(9, 11, 12)  share=  0.006%    below
      #50 bin(9, 10, 12)  share=  0.006%    below
      #51 bin(6, 10, 12)  share=  0.006%    below
      #52 bin(4, 6, 7)  share=  0.006%    below
      #53 bin(14, 10, 9)  share=  0.005%    below
      #54 bin(9, 12, 14)  share=  0.005%    below
      #55 bin(7, 9, 12)  share=  0.005%    below
      #56 bin(5, 9, 12)  share=  0.005%    below
      #57 bin(13, 8, 7)  share=  0.004%    below
      #58 bin(13, 7, 7)  share=  0.004%    below
      #59 bin(5, 8, 10)  share=  0.004%    below
      #60 bin(4, 7, 11)  share=  0.004%    below
      #61 bin(4, 6, 8)  share=  0.004%    below
      #62 bin(3, 7, 10)  share=  0.004%    below
      #63 bin(2, 5, 6)  share=  0.004%    below
      #64 bin(1, 6, 10)  share=  0.004%    below
      #65 bin(8, 10, 12)  share=  0.003%    below
      #66 bin(8, 9, 11)  share=  0.003%    below
      #67 bin(7, 8, 10)  share=  0.003%    below
      #68 bin(5, 7, 9)  share=  0.003%    below
      #69 bin(4, 8, 11)  share=  0.003%    below
      #70 bin(3, 4, 6)  share=  0.003%    below
      #71 bin(2, 4, 5)  share=  0.003%    below
      #72 bin(13, 7, 6)  share=  0.002%    below
      #73 bin(10, 11, 12)  share=  0.002%    below
      #74 bin(9, 10, 11)  share=  0.002%    below
      #75 bin(4, 7, 10)  share=  0.002%    below
      #76 bin(3, 7, 11)  share=  0.002%    below
      #77 bin(3, 7, 9)  share=  0.002%    below
      #78 bin(1, 4, 6)  share=  0.002%    below
      #79 bin(1, 4, 5)  share=  0.002%    below
      #80 bin(15, 14, 13)  share=  0.001%    below
      #81 bin(14, 9, 9)  share=  0.001%    below
      #82 bin(13, 14, 14)  share=  0.001%    below
      #83 bin(12, 4, 4)  share=  0.001%    below
      #84 bin(11, 7, 6)  share=  0.001%    below
      #85 bin(10, 6, 6)  share=  0.001%    below
      #86 bin(8, 11, 13)  share=  0.001%    below
      #87 bin(8, 9, 10)  share=  0.001%    below
      #88 bin(7, 8, 9)  share=  0.001%    below
      #89 bin(6, 8, 10)  share=  0.001%    below
      #90 bin(6, 7, 8)  share=  0.001%    below
      #91 bin(4, 5, 7)  share=  0.001%    below
      #92 bin(4, 5, 6)  share=  0.001%    below
      #93 bin(1, 5, 9)  share=  0.001%    below
    boundary: highest sub-floor box = 0.081%  |  lowest counted box = 4.499%  |  floor = 0.500%

=== tests/skills/figure-choose/green/out-G1/figure.pdf
    loaded_px=900x390  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 3   => F2 PASS
    all chroma boxes kept (before floor): 39
      #1  bin(13, 14, 15)  share= 10.904%  >=FLOOR
      #2  bin(9, 12, 14)  share= 10.242%  >=FLOOR
      #3  bin(3, 8, 11)  share=  5.704%  >=FLOOR
      #4  bin(10, 12, 14)  share=  0.248%    below
      #5  bin(12, 14, 14)  share=  0.159%    below
      #6  bin(12, 13, 14)  share=  0.103%    below
      #7  bin(11, 13, 14)  share=  0.074%    below
      #8  bin(3, 8, 12)  share=  0.059%    below
      #9  bin(9, 11, 13)  share=  0.058%    below
      #10 bin(10, 13, 14)  share=  0.049%    below
      #11 bin(8, 11, 13)  share=  0.041%    below
      #12 bin(5, 9, 12)  share=  0.032%    below
      #13 bin(4, 9, 12)  share=  0.032%    below
      #14 bin(9, 12, 13)  share=  0.026%    below
      #15 bin(5, 6, 7)  share=  0.022%    below
      #16 bin(7, 10, 13)  share=  0.016%    below
      #17 bin(8, 10, 11)  share=  0.014%    below
      #18 bin(8, 11, 12)  share=  0.013%    below
      #19 bin(7, 9, 10)  share=  0.013%    below
      #20 bin(6, 8, 9)  share=  0.012%    below
      #21 bin(4, 5, 6)  share=  0.011%    below
      #22 bin(9, 11, 12)  share=  0.009%    below
      #23 bin(13, 14, 14)  share=  0.008%    below
      #24 bin(6, 7, 8)  share=  0.008%    below
      #25 bin(4, 8, 12)  share=  0.008%    below
      #26 bin(6, 8, 8)  share=  0.006%    below
      #27 bin(11, 12, 14)  share=  0.004%    below
      #28 bin(8, 10, 12)  share=  0.004%    below
      #29 bin(7, 8, 9)  share=  0.004%    below
      #30 bin(6, 10, 13)  share=  0.004%    below
      #31 bin(5, 7, 8)  share=  0.004%    below
      #32 bin(5, 7, 7)  share=  0.004%    below
      #33 bin(5, 6, 6)  share=  0.004%    below
      #34 bin(6, 10, 12)  share=  0.003%    below
      #35 bin(13, 13, 14)  share=  0.002%    below
      #36 bin(7, 10, 11)  share=  0.002%    below
      #37 bin(4, 6, 6)  share=  0.002%    below
      #38 bin(7, 11, 13)  share=  0.001%    below
      #39 bin(7, 9, 11)  share=  0.001%    below
    boundary: highest sub-floor box = 0.248%  |  lowest counted box = 5.704%  |  floor = 0.500%

=== tests/skills/figure-choose/green/out-G2/figure.pdf
    loaded_px=947x713  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 0   => F2 PASS
    all chroma boxes kept (before floor): 66
      #1  bin(1, 6, 7)  share=  0.403%    below
      #2  bin(12, 4, 0)  share=  0.178%    below
      #3  bin(2, 7, 8)  share=  0.063%    below
      #4  bin(12, 4, 1)  share=  0.055%    below
      #5  bin(4, 8, 9)  share=  0.036%    below
      #6  bin(12, 5, 2)  share=  0.031%    below
      #7  bin(3, 7, 8)  share=  0.028%    below
      #8  bin(10, 12, 12)  share=  0.025%    below
      #9  bin(9, 11, 12)  share=  0.024%    below
      #10 bin(12, 6, 3)  share=  0.023%    below
      #11 bin(7, 10, 11)  share=  0.023%    below
      #12 bin(15, 14, 13)  share=  0.021%    below
      #13 bin(13, 8, 6)  share=  0.021%    below
      #14 bin(15, 13, 12)  share=  0.021%    below
      #15 bin(13, 9, 7)  share=  0.021%    below
      #16 bin(14, 12, 11)  share=  0.019%    below
      #17 bin(8, 11, 11)  share=  0.018%    below
      #18 bin(12, 13, 13)  share=  0.017%    below
      #19 bin(14, 11, 9)  share=  0.016%    below
      #20 bin(13, 7, 5)  share=  0.016%    below
      #21 bin(6, 9, 10)  share=  0.016%    below
      #22 bin(14, 11, 10)  share=  0.015%    below
      #23 bin(5, 9, 9)  share=  0.014%    below
      #24 bin(12, 6, 4)  share=  0.012%    below
      #25 bin(5, 9, 10)  share=  0.012%    below
      #26 bin(11, 12, 13)  share=  0.011%    below
      #27 bin(8, 10, 11)  share=  0.011%    below
      #28 bin(11, 13, 13)  share=  0.009%    below
      #29 bin(7, 10, 10)  share=  0.009%    below
      #30 bin(3, 8, 8)  share=  0.009%    below
      #31 bin(14, 10, 8)  share=  0.008%    below
      #32 bin(10, 12, 13)  share=  0.008%    below
      #33 bin(6, 10, 10)  share=  0.008%    below
      #34 bin(15, 13, 13)  share=  0.007%    below
      #35 bin(5, 8, 9)  share=  0.007%    below
      #36 bin(3, 8, 9)  share=  0.007%    below
      #37 bin(2, 6, 7)  share=  0.007%    below
      #38 bin(12, 5, 3)  share=  0.006%    below
      #39 bin(12, 5, 1)  share=  0.006%    below
      #40 bin(14, 10, 9)  share=  0.005%    below
      #41 bin(13, 8, 5)  share=  0.005%    below
      #42 bin(14, 13, 12)  share=  0.004%    below
      #43 bin(14, 12, 10)  share=  0.004%    below
      #44 bin(13, 7, 4)  share=  0.004%    below
      #45 bin(9, 12, 12)  share=  0.004%    below
      #46 bin(13, 9, 8)  share=  0.003%    below
      #47 bin(9, 7, 6)  share=  0.003%    below
      #48 bin(14, 12, 12)  share=  0.002%    below
      #49 bin(11, 4, 1)  share=  0.002%    below
      #50 bin(10, 8, 7)  share=  0.002%    below
      #51 bin(10, 6, 4)  share=  0.002%    below
      #52 bin(5, 8, 8)  share=  0.002%    below
      #53 bin(12, 10, 9)  share=  0.001%    below
      #54 bin(12, 7, 5)  share=  0.001%    below
      #55 bin(12, 7, 4)  share=  0.001%    below
      #56 bin(11, 6, 4)  share=  0.001%    below
      #57 bin(11, 5, 2)  share=  0.001%    below
      #58 bin(10, 7, 5)  share=  0.001%    below
      #59 bin(9, 11, 11)  share=  0.001%    below
      #60 bin(9, 8, 7)  share=  0.001%    below
      #61 bin(6, 9, 9)  share=  0.001%    below
      #62 bin(6, 8, 8)  share=  0.001%    below
      #63 bin(5, 7, 7)  share=  0.001%    below
      #64 bin(4, 7, 8)  share=  0.001%    below
      #65 bin(3, 7, 7)  share=  0.001%    below
      #66 bin(3, 6, 6)  share=  0.001%    below
    boundary: no box reached the 0.5% floor (F2 = 0)

=== tests/skills/figure-choose/green/out-G3/figure.pdf
    loaded_px=947x435  pdf_pages=1
    F2-relevant boxes (>= 0.5% floor): 3   => F2 PASS
    all chroma boxes kept (before floor): 46
      #1  bin(10, 12, 14)  share= 13.977%  >=FLOOR
      #2  bin(4, 8, 11)  share= 12.936%  >=FLOOR
      #3  bin(1, 4, 7)  share=  7.203%  >=FLOOR
      #4  bin(12, 13, 14)  share=  0.186%    below
      #5  bin(8, 10, 11)  share=  0.175%    below
      #6  bin(8, 11, 12)  share=  0.107%    below
      #7  bin(11, 12, 13)  share=  0.094%    below
      #8  bin(5, 8, 11)  share=  0.091%    below
      #9  bin(2, 5, 7)  share=  0.083%    below
      #10 bin(10, 12, 13)  share=  0.074%    below
      #11 bin(8, 10, 12)  share=  0.074%    below
      #12 bin(6, 8, 10)  share=  0.060%    below
      #13 bin(5, 8, 9)  share=  0.043%    below
      #14 bin(9, 11, 13)  share=  0.042%    below
      #15 bin(13, 14, 15)  share=  0.032%    below
      #16 bin(11, 13, 14)  share=  0.032%    below
      #17 bin(13, 14, 14)  share=  0.030%    below
      #18 bin(7, 8, 9)  share=  0.015%    below
      #19 bin(10, 11, 12)  share=  0.013%    below
      #20 bin(7, 9, 10)  share=  0.013%    below
      #21 bin(6, 9, 12)  share=  0.011%    below
      #22 bin(6, 9, 11)  share=  0.011%    below
      #23 bin(11, 12, 14)  share=  0.008%    below
      #24 bin(9, 11, 12)  share=  0.008%    below
      #25 bin(5, 7, 9)  share=  0.008%    below
      #26 bin(10, 11, 13)  share=  0.007%    below
      #27 bin(9, 10, 11)  share=  0.007%    below
      #28 bin(5, 6, 7)  share=  0.007%    below
      #29 bin(3, 6, 8)  share=  0.007%    below
      #30 bin(7, 10, 12)  share=  0.006%    below
      #31 bin(4, 6, 8)  share=  0.006%    below
      #32 bin(8, 9, 10)  share=  0.005%    below
      #33 bin(6, 7, 8)  share=  0.005%    below
      #34 bin(5, 9, 11)  share=  0.005%    below
      #35 bin(9, 10, 12)  share=  0.004%    below
      #36 bin(8, 9, 11)  share=  0.004%    below
      #37 bin(7, 8, 10)  share=  0.004%    below
      #38 bin(6, 7, 7)  share=  0.003%    below
      #39 bin(11, 12, 12)  share=  0.002%    below
      #40 bin(10, 12, 12)  share=  0.002%    below
      #41 bin(7, 9, 12)  share=  0.002%    below
      #42 bin(7, 9, 11)  share=  0.002%    below
      #43 bin(6, 8, 9)  share=  0.002%    below
      #44 bin(4, 7, 8)  share=  0.002%    below
      #45 bin(3, 5, 7)  share=  0.002%    below
      #46 bin(4, 7, 9)  share=  0.001%    below
    boundary: highest sub-floor box = 0.186%  |  lowest counted box = 7.203%  |  floor = 0.500%

[exit=0]
```
（上面是**完整输出**，没有节略。这个工具自己不判红绿，只报每个色箱的占比；它 `import` 检查器本体，并对每一个输入断言与 `color_count` 一致。）

下表每一个数都从**上面那次运行的输出**里抽出来；闸门那一列由 `house-metrics.py` 的 `_cont_hit` **直接判**（不在本文重写那条式子）：

| 产物 | 未设地板的彩色箱数 | 最高落选箱 | 过闸门（= 连续色图）? | F2 条数可引用? |
| :--- | ---: | ---: | :--- | :--- |
| `red/out-R1` | 78 | 0.127% | 否（离散） | 可引用 |
| `red/out-R2` | 152 | 0.370% | **是** | **不可引用** |
| `red/out-R3` | 93 | 0.081% | 否（离散） | 可引用 |
| `green/out-G1` | 39 | 0.248% | 否（离散） | 可引用 |
| `green/out-G2` | 66 | 无落选箱 | 否（离散） | 可引用 |
| `green/out-G3` | 46 | 0.186% | 否（离散） | 可引用 |

闸门常量（从 `house-metrics.py` **import** 进来打印，不是抄的）：`CONT_BOX_MIN=100`、`CONT_SUBFLOOR_MIN_PCT=0.4`
**结论**：三份 GREEN 产物**没有一份命中闸门** ⇒ **本轮的 F2 条数可以引用**，
任务书点名的那条"连续色图别拿条数去比"的警告**在本轮 GREEN 侧不触发**。
RED 侧命中闸门的只有 **1 张**
（见上表）—— 那正是 R2 的 F2=7：按 H4，**它的条数本就不该引用**，
所以 §4 里 R2 的 F2 由红转绿应当读成"**方向可信**（连续色图 → 离散配色），
RED 那个 7 不作为一个可引用的读数"。

==============================================================================
§6 改善 / 未改善 / **本次无区分力**（三类分开，不许混）
==============================================================================

### 6-1 由红转绿（逐条，附逐字读数）

- **R1 · F1**：RED **FAIL** `图宽比 1.521（分母 6.31 in）` → GREEN **PASS** `图宽比 0.951（分母 6.31 in）`
- **R1 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R1 · F3b**：RED **FAIL** `图注词数 203 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R1 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`
- **R2 · F1**：RED **FAIL** `图宽比 1.743（分母 6.31 in）` → GREEN **PASS** `图宽比 1.000（分母 6.31 in）`
- **R2 · F2**：RED **FAIL** `彩色主色数 7` → GREEN **PASS** `彩色主色数 0`
- **R2 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R2 · F3b**：RED **FAIL** `图注词数 285 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R2 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`
- **R3 · F1**：RED **FAIL** `图宽比 1.204（分母 6.31 in）` → GREEN **PASS** `图宽比 1.000（分母 6.31 in）`
- **R3 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R3 · F3b**：RED **FAIL** `图注词数 177 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R3 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`

共 **13 格**。任务书点名的两个预期（**R3 的 F1 与 F3c**）都实现了：
- R3 · F1：`图宽比 1.204（分母 6.31 in）` → `图宽比 1.000（分母 6.31 in）` ✅ 预期兑现
- R3 · F3c：`句末不加句号` → `句末不加句号` ✅ 预期兑现

### 6-2 上一版登记为「仍红」的 3 格（F3b）—— 本轮**已收敛**，逐条重述

**当前状态**：这三格现在**全部转绿**（见 §6-1）。下面是它们从"仍红"到"转绿"的完整交代，
因为上一版在这里**说错过一句话**，必须留痕。

- **（0 格）** —— 本轮没有“两侧都红”的格子。上一版的 3 格（R1/R2/R3 的 F3b）
  已由下面的口径收敛转绿。

**上一版的措辞错在哪**：它把这三格写成"**新暴露的口径分歧**"，并在报告里记成
"本轮最有价值的发现"。**这是 overclaim** —— 该口径在仓内**早有三处写死**：

1. `tests/figures-recon/c8-caption.tsv` 的分布段（小标题即"正文部分词数的分位"）：
   `FIG words(含 Figure N): … p95=14.0 max=19` 与 `FIG words(去标签后正文): … p95=12.0 max=17`
   —— **12 / 17 是正文口径的 p95 / max**；
2. `house-metrics.py` 的 `cap_words_med/p25/p75/p95/max` **全部**用 `words_body`；
3. `references/provenance.md` 的 **P-D-c1**（口径原文「去掉 `Figure N:` 前缀后的正文」），
   其 `已知偏差` 当时就登记了"出货检查器用的是含标签的整条词数 ⇒ 与本口径多 2 词 ⇒
   **两口径不可互换**"（P-D-c2 / P-D-c3 各自复述）。

⇒ 所以正确读法不是"新发现"，而是：**检查器当年取错了口径**（规范侧一直是对的）。

**本轮的收敛（照定案执行，只动一处代码）**：

- 改：`check-figure-style.py` 的 F3b 由 `len(cap.split())` 改成 `len(caption_body(cap).split())`
  （`caption_body` 就在同一个文件里，F3d 本就在用）。
- **不动**：常量 `CAP_MAX=12` / `CAP_HARD=17` 与 `G-H9-*` 守卫一族（12 / 17 本来就是**正文口径**的
  p95 / max）；也不反向改 H9 去迁就含标签口径（那要把常量重导为 14 / 19 并改 provenance 三条读数）。
- 规范侧登记同步改成"**已收敛**"：`provenance.md` 的 P-D-c1（P-D-c2/c3 的"同 P-D-c1"跟着走）
  与 `house-style.md` H9 的「违反判据」一行（标明是**正文**词数）。
- **红绿效应**：GREEN 三份 F3b 由"整条 13 词 FAIL"变成"正文 11 词 PASS"；
  RED 三份**一字不变**（`Figure 1.` 无冒号 ⇒ `caption_body` 切不出前缀 ⇒ 整条算正文）。
- **口径改动的回归位**：新增 fixture `caption:7`（整条 13 / 正文 11，卡在 `CAP_MAX=12` 的分界上）
  + 变异 `M42`（把口径换回整条 ⇒ caption:7 由 PASS 转 FAIL），见 Task 1 的证据件
  `figure-style-baseline.txt` §3.2 / §4 与 §9.2。

### 6-3 **本次无区分力的条目（两侧都通过）—— 单列，不许算成"规范的功劳"**

- R1 · F2：RED **PASS** `彩色主色数 3` → GREEN **PASS** `彩色主色数 3`（**两侧都绿**）
- R1 · F3d：RED **PASS** `图注正文非空（正文 203 词）` → GREEN **PASS** `图注正文非空（正文 11 词）`（**两侧都绿**）
- R2 · F3d：RED **PASS** `图注正文非空（正文 285 词）` → GREEN **PASS** `图注正文非空（正文 11 词）`（**两侧都绿**）
- R3 · F2：RED **PASS** `彩色主色数 3` → GREEN **PASS** `彩色主色数 3`（**两侧都绿**）
- R3 · F3d：RED **PASS** `图注正文非空（正文 177 词）` → GREEN **PASS** `图注正文非空（正文 11 词）`（**两侧都绿**）

共 **5 格**。**这些格子本轮没有区分力**：它们两侧都通过，
所以**不能**用来支持"规范起作用了"。逐条说明它们为什么没有区分力：

- **R1 · F2（3 色）与 R3 · F2（3 色）**：RED 的两个写手**恰好**都选了 3 色序数色阶
  （R1 的 `#ffeda0/#feb24c/#f03b20`），本来就 ≤4 ⇒ 两侧都绿。
  **本轮没有出现"配色爆掉"的失败形态**，所以这一格证明不了规范在配色上有用。
  真正有区分力的那一格是 **R2 · F2（RED 7 → GREEN 0）** —— RED 的 R2 用了连续发散色图。
- **F3d（三份）**：RED 三份图注都非空（203 / 285 / 177 词），GREEN 也不空 ⇒ 两侧都绿。
  RED 那份证据已登记过这条（`red/red-evidence.md` §3 末）：**不许记成"规范起作用了"**；
  本次仍是同样情形，**再次单列**。

### 6-4 预期外的确有区分力的条目（任务书没点，但实测红→绿）

**本节由数据生成**：下面逐条就是 §6-1 那份 `improved` 列表本身（同一份数据，不另抄）。
上一版这里是**手写的 5 条**，其中 `R2 · F3b` 当时**判词仍是 FAIL**，却被列进了"实测红→绿"
—— 那是**分类错**（该格当时属 §6-2）。本轮改成机器生成 + 逐条断言，杜绝再犯。

- **R1 · F1**：RED **FAIL** `图宽比 1.521（分母 6.31 in）` → GREEN **PASS** `图宽比 0.951（分母 6.31 in）`
- **R1 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R1 · F3b**：RED **FAIL** `图注词数 203 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R1 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`
- **R2 · F1**：RED **FAIL** `图宽比 1.743（分母 6.31 in）` → GREEN **PASS** `图宽比 1.000（分母 6.31 in）`
- **R2 · F2**：RED **FAIL** `彩色主色数 7` → GREEN **PASS** `彩色主色数 0`
- **R2 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R2 · F3b**：RED **FAIL** `图注词数 285 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R2 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`
- **R3 · F1**：RED **FAIL** `图宽比 1.204（分母 6.31 in）` → GREEN **PASS** `图宽比 1.000（分母 6.31 in）`
- **R3 · F3a**：RED **FAIL** `图注以 `Figure N:` 起` → GREEN **PASS** `图注以 `Figure N:` 起`
- **R3 · F3b**：RED **FAIL** `图注词数 177 超硬上限 17` → GREEN **PASS** `图注词数 11（上限 12，硬上限 17）`
- **R3 · F3c**：RED **FAIL** `句末不加句号` → GREEN **PASS** `句末不加句号`

共 **13 条**，与 §6-1 的 `13` 格**逐条相同**（本节 ⊆ §6-1，且 §6-1 ⊆ 本节 ⇒ 两节是同一集合的两处呈现）。
**口径**：本节只收"RED 判 FAIL 且 GREEN 判 PASS"的格子（上面的判定由 §4 的逐格表
同一批读数给出）。**"仍红"的格子一律不在这里** —— 上一版把 `R2 · F3b`（RED 285 词 → GREEN 13 词、
判词仍 FAIL）放进本节，是**按"词数大幅收缩"而不是按"判词红→绿"归的类**；
若按那个口径读，应当写成"词数大幅收缩但**仍红**"，并放进 §6-2。本轮该格已转绿（§6-2），
所以两个小节不再冲突。

==============================================================================
§7 判断层（独立判者）—— 判词逐字，**以及它没有背书什么**
==============================================================================

判者是**全新 `general-purpose` subagent、未用 `fork`**，**只读**三份 brief 与三个产物目录，
**没有**读 `.claude/skills/` 或任何其它仓内文件（其提示词与自报原文见
`green/green-self-reports.md`）。判词全文入库为 `green/judge-green.md`，**逐字内联如下**：

```
$ python - <<PY   # 判词原件的合规体检 + 内联件逐字节相同

import hashlib, pathlib, re, string
p = pathlib.Path("tests/skills/figure-choose/green/judge-green.md")
b = p.read_bytes()
t = b.decode("utf-8")
body = t.split("\n---\n", 1)[1] if "\n---\n" in t else t
print("judge-green.md  bytes=%d  <REPO> 掩码处数（正文里）= %d" % (len(b), body.count("<REPO>")))
# 残留绝对路径：不把盘符形态与仓根名写成字面量（否则本文件的体检会命中体检代码自己）
proj = pathlib.Path(".").resolve().name                      # 仓根目录名（cwd = 仓根）
print("残留绝对路径（`X:\\` 形态 + 仓根名）= %d 处"
      % (sum(t.count(c + ":" + "\\") for c in string.ascii_letters) + t.count(proj)))
print("SHA-256（前 16 位）= %s" % hashlib.sha256(b).hexdigest()[:16])
PY
judge-green.md  bytes=13556  <REPO> 掩码处数（正文里）= 3
残留绝对路径（`X:\` 形态 + 仓根名）= 0 处
SHA-256（前 16 位）= ccd0ff3f0493901f
[exit=0]
```
⇒ `green/judge-green.md` 的**原件**已按本仓"不写绝对路径"的规定把本仓根掩码成 `<REPO>`
（**3 处**，都在正文里），脚本当场复扫**残留 0 处** ⇒ 下面内联的判词与原件**逐字节相同**，
不再是"本文又掩一次、原件仍然带绝对路径"。
**对判词原件的两处编辑逐条登记在 §7-3**（掩码 3 处 + 一处数字订正），不藏。

**判词全文（`green/judge-green.md`，逐字节内联）**：

`````text
# judge-green.md — 三份 GREEN 产物判读（G1 / G2 / G3）

〔原件登记〕本件是判者写的判词。入库前做过**两处**编辑（逐条见 `green-evidence.md` §7-3）：
① 3 处本仓绝对路径掩码为 `<REPO>`（本仓规定不写绝对路径）；② 第 131 行（掩码前行号）的
"次小 A–E = 0.07" 订正为 **0.0616**。除此之外逐字未改；判者的结论不受影响。

判读范围：题面 `tests/skills/figure-choose/red/brief-R{1,2,3}.md`，产物目录
`tests/skills/figure-choose/green/out-G{1,2,3}/`（`make_figure.py` / `figure.pdf` / `figure.png` / `caption.txt`），
三张 PNG 均已打开逐张看图。下面按 G1 → G2 → G3 依次回答四问；每条结论后面附我把数字自己重算一遍的结果，
以免只凭产物自述下判断。

---

## G1 — 来源 brief R1（六个区的脆弱度构成）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R1 的数据关系是"构成"：每个区的 low/medium/high 三份占比相加恒为 1.00（我逐区验算，
六区三份之和都是 1.00，与题面一致）。问的是两件事——逐区描述构成、并支撑"哪两个区结构最像"的判断。
G1 画的是**堆叠柱状图**：横轴六个区，纵轴 0.00–1.00，每根柱按三个 tier 分段。

这是构成数据"比较多个组的构成"的标准正解，理由具体到这张图上：

- 每一段长度都落在同一条共同基线（0–1 轴）上，区与区之间可以直接比长短——这正是饼图做不到的
  （饼图每个扇区各有一条自己的弧，跨饼比较角度要靠眼睛估，六个饼就是六套参照系）。
- 段内直接标了数值（0.15 / 0.30 / 0.55 …），读者不用靠量长度去猜，"描述构成"这一层是硬信息落图的。
- 对"哪两个区最像"这一层，图做了两件实事：柱序按 low 降序排（C, F, A, E, B, D），把最像的一对排成相邻；
  并在 B、D 两根柱下方画了括号 + 注记 "B and D: closest pair"。我自己按三份占比的 L1 距离重算了 15 对：
  B–D = |0.31−0.28| + |0.44−0.47| + |0.25−0.25| = **0.06**，是全表最小（次小 A–E = 0.10、A–F = 0.10），
  和 `caption.txt` 的 "B and D are most similar" 以及图上括号的位置一致。图没有替读者编结论。

配色是同色系三段递进（`#deebf7`/`#9ecae1`/`#3182bd`），有序 tier 用有序明度，属于正确的编码；
没有任何一条编码通道在这张图上会误导。唯一可挑的是"最像的一对"是靠图外的计算（L1）选出来的，
图上只给了括号没给距离值——但这不影响图型选得对不对。**图型对问题是合适的。**

**问题 3（是否违反"构成数据不得画成饼图"）：no**
三张 PNG、三份脚本里都没有 pie / donut 的任何调用（`make_figure.py` 全文只有 `ax.bar`）。

**问题 4（是否引用编号设计规则）：有**

引用文件：`<REPO>\tests\skills\figure-choose\green\out-G1\make_figure.py`，
集中在模块 docstring 第 11–22 行。第 11 行写明出处：

> 第 11 行：`Delivery-form targets come from ``house-style.md`` and are cited by H-ID only:`

其下逐条列出（第 13–21 行，原文照抄）：

> 第 13 行：`H1  width close to the body text width (0.95-1.0 x 6.31 in -> 6.0 in)`
> 第 14 行：`H3  landscape, aspect ratio in the usual 2-3 band, height ~2.6 in`
> 第 15 行：`H4  at most 4 main colours (three tiers -> three ordered shades)`
> 第 16 行：`H5  no matplotlib default colour cycle (tab10)`
> 第 17 行：`H6  no pie / donut chart for composition data`
> 第 18 行：`H7  no 3-D`
> 第 19 行：`H9  caption is "Figure N:" + ASCII colon, <= 12 words, no trailing period`
> 第 20 行：`H10 no top/right spines, ticks pointing in, axis labels carry units`
> 第 21 行：`H12 in-figure text 9 pt (>= 7 pt, ~0.8-1.0 x body size)`

正文里还有带 H 编号的落地注解：第 37 行 `(H4, H5: not the tab10 cycle)`、第 79 行 `# 4. Figure (H1 / H3 / H12)`、
第 100 行 `# H1: 6.0 / 6.31 = 0.95; H3: aspect 2.31`、第 125 行 `# 5. Axes (H10)`、
第 158 行 `# x-axis title, written on the same row as the pair note (H10)`、第 174 行 `# 8. Export (H1: no tight bbox, ...)`。

即：作者确实是从一份**有成文编号的规范**（H 编号，另有对应文件 `house-style.md`）出发工作的；
H2/H8/H11 未被提及。另外注意 H6 被显式抄在 docstring 里，而图并没有踩它（见问题 3）——
抄了规则又没违反，属于"规则被读到并遵守"，不是"抄了却在图里违掉"。

---

## G2 — 来源 brief R2（灾害次数的驱动因子）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R2 的问题有两层：(a) 哪个因子与历史灾害次数相关性最强；(b) 各区之间有多相似。
数据是同一批 6 个区上的 5 个连续属性。G2 的图是两块：

- 上半：**4 个散点面板**，每个面板是一个预测因子（横轴）对灾害次数（共享同一根纵轴 0–42），
  按 |r| 从大到小从左到右排（Mean slope → Infrastructure index → Vegetation cover → Population density），
  每个面板角上直接印出相关系数。
- 下半：**平行坐标图**，6 个区在 5 根标准化轴上的折线，用来读"区与区的相似"。

我按定义把四个 Pearson r 全算了一遍：slope **+0.934**、infra **−0.777**、veg **−0.744**、pop **+0.360**，
与图上标注的 +0.93 / −0.78 / −0.74 / +0.36 逐位吻合，排序也对（slope 最左且加粗）。
也就是说，第一层问题——"哪个因子与灾害次数关联最强"——是**被图直接回答的**：读者不看正文也能从
左起第一个面板读出答案。这正是散点面板该干的活（相关关系用 x–y 平面上的位置编码，而不是用长度或角度去编码）。

第二层"区与区的相似"用平行坐标承载，是把同一批个体跨全部 5 个属性一次连起来看，属于这一层的标准做法之一，
比"两两散点矩阵"更省版面，也和多面板散点的关系是互补而非重复。注意它也**没有**用雷达图——
雷达图在跨轴比较时角度/面积都会失真，这里没踩。

图外我还验了它自报的结论：把 5 个属性各自 z 标准化后算区与区的欧氏距离，
最小的一对是 A–C（≈1.45），次小 A–E（≈1.74），所以 `caption.txt` 的 "A and C share a profile" 站得住；
图上 A、C 也确实用同一种强调色（青）画出，D 单独用橙色标为离群点。"Vegetation cover 与 Infrastructure index
共变 (r = +0.98)"这句也复核过，r = +0.980，属实。

一点保留（不影响结论）：下半的平行坐标对每根轴做了各自 min–max 缩放，各轴可视跨度被拉平，
因此"两条线交叉"只能读相对次序、不能读绝对差距；6 条线 5 根轴对肉眼仍偏密。
但它承担的只是辅助性的第二问，主问题（相关性排序）由上半的 r 读数硬性给出，所以整体仍是
**图型对问题是合适的**。

**问题 3（是否违反"构成数据不得画成饼图"）：no**
这份数据根本不是构成数据（5 个属性不是同一个整体的互补份额，不要求和为 1），
而且图中也没有 pie / donut：脚本里只有 `ax.scatter` 与 `axp.plot`。

**问题 4（是否引用编号设计规则）：没有**

我把 `<REPO>\tests\skills\figure-choose\green\out-G2\make_figure.py` 全文找过，
**没有任何 H 编号**（也没有 K/S/R 之类的编号规则）。作者提到过规范，但只以散文形式，例如第 77–78 行：

> 第 77–78 行：`# House style: <=4 main colours, no matplotlib default colour order, grey is`
> `# a normal choice, no top/right spines, ticks inward, unit-bearing labels.`

另外第 5 行提到决策树的条目号 `figure-choose decision tree, entry 3 "correlation"`、
第 16 行 `the alternative listed for this entry`——那是**树里的条目号**，不是 `H1, H2, ...` 形式的编号规则。

结论：G2 的作者**没有**在产物里引用编号规则；从注释看它工作在一套"散文写成的风格说明 + 决策树条目号"上，
而不是 H 编号那份规范。这一点与 G1、G3 形成明显对照。

---

## G3 — 来源 brief R3（同 R1 的数据，论文可直接粘贴版）

**问题 1（图型是否合适）：correct**

**问题 2（理由）**

R3 与 R1 是**同一张表、同一个问题**，差别只在交付形态（"one figure I can paste straight into the body text"）。
因此正解应与 R1 相同——G3 也选了**堆叠柱状图**，两者一致，没有被"论文版"这个限定带偏成别的图型。

图的表现：纵轴换成百分比 0–100%，段内印整数（25 / 47 / 28 …），柱序按 high 降序（B/D/E 三个 0.25 并列时
再按 low 升序）得到 D, B, E, A, F, C——把最像的一对排成相邻；最像的一对用一块近灰底纹带 + 上方括号标出，
注记 "most similar pair (B, D)"。我按三份占比的欧氏距离重算了 15 对，最小仍是 **B–D**
（√(0.03²+0.03²+0²) = 0.0424，次小 A–E = 0.0616〔复核订正：原文写 0.07，实算 0.0616，见 green-evidence.md §7-3〕），和 `caption.txt` 的 "B and D most similar" 一致，
底纹与括号也压在 D、B 两根柱上，没有标错位置。

值得记一笔的是：脚本 docstring 第 18–22 行**主动记下了候选图型被否掉的理由**——
它考虑过三元图（ternary plot），因为六个构成点只占单纯形中间一小块（low 0.28–0.55、high 0.15–0.25），
三对最像的点会挤在 ~0.04 单纯形单位内、任何可读尺寸下标记都会重叠，于是回到堆叠柱。
候选图型被逐一比较后落选，而不是随手抓一个——这正说明图型是选出来的。

**问题 3（是否违反"构成数据不得画成饼图"）：no**
这张图就是 R1 那类构成数据，但画的是堆叠柱；脚本里除 `ax.bar` 之外没有任何饼/环调用。
docstring 第 45 行还自己把这条规则抄了出来（见下），是"知道有这条禁令并且绕开了"。

**问题 4（是否引用编号设计规则）：有**

引用文件：`<REPO>\tests\skills\figure-choose\green\out-G3\make_figure.py`，
集中在模块 docstring 第 39–51 行。第 39 行写明出处：

> 第 39 行：`Design points, mapped to the house style by ID (references/house-style.md):`

其下逐条（第 40–51 行，原文照抄）：

> 第 40 行：`H1  figure width == text-width default (6.31 in)      -> not narrower/wider`
> 第 41 行：`H3  landscape, aspect in the 2-3 band, height ~2.6 in`
> 第 42 行：`H4  three chromatic colours (<= 4); the highlight band is near-grey`
> 第 43 行：`H5  explicit palette, not the matplotlib default colour cycle`
> 第 44 行：`H6  composition data is NOT drawn as a pie/donut`
> 第 45 行：`H7  no 3-D`
> 第 46 行：`H9  caption (caption.txt) is `Figure 1:` + ASCII colon, <= 12 words, no`
> `      closing period`
> 第 48 行：`H10 no top/right spines, inward major ticks only, axis label carries the unit`
> 第 49 行：`H12 in-figure type 7.5-9 pt, no line/font clash with the body text`
> 第 50 行：`(H11 is not covered by the style: no gridlines are drawn; the legend is kept,`

正文里同样有带 H 编号的落地注解：第 68 行 `never below 7.5 pt (H12)`、第 94 行 `(H5)`、
第 98 行 `# near-grey highlight band (not a chromatic colour, H4)`、第 101 行 `# H1 width = text-width default, H3 aspect 2.18`、
第 159 行 `# axes (H10)`、第 178 行 `# legend: tier key, to the right of the plot (H11 not covered by the style)`。

即：G3 与 G1 一样，是从同一份 H 编号规范出发工作的（且比 G1 多处理了一条 H11，并明确说明 H11 未被规范覆盖——
不装懂）。H2/H8 未提及。

---

## 汇总

| 产物 | 对应 brief | 1. 图型 | 2. 饼图违规 | 4. 引用编号规则 |
|---|---|---|---|---|
| G1 | R1（构成，六区三档） | **correct**（堆叠柱） | **no** | **有** — `out-G1/make_figure.py` 第 11–22 行，H1/H3/H4/H5/H6/H7/H9/H10/H12（及第 37/79/100/125/158/174 行内联） |
| G2 | R2（相关 + 相似） | **correct**（按 \|r\| 排序的 4 个散点面板 + 平行坐标） | **no** | **无** — 全文无 H 编号；只有散文式 house-style 注释（第 77–78 行）和决策树条目号（第 5、16 行 "entry 3"） |
| G3 | R3（同 R1 的构成，论文版） | **correct**（堆叠柱） | **no** | **有** — `out-G3/make_figure.py` 第 39–51 行，H1/H3/H4/H5/H6/H7/H9/H10/H11/H12（及第 68/94/98/101/159/178 行内联） |

三点跨产物观察：

1. **三张图型都对**，没有一张把构成数据画成饼图，也没有一张把相关问题画成饼图/雷达图/3-D。
   R1 与 R3 同表同问，两份产物选了同一种图型（堆叠柱），是自洽的——"论文版"没有成为换图型的理由。
2. **三份产物自报的结论我都独立复算过，全部属实**：G1/G3 的最相似对 B–D、G2 的 slope r = +0.93 排第一
   以及 A–C 最相似，都能被数据本身验证。产物没有"图看起来对但结论编出来"的情况。
3. **规范引用不齐**：G1、G3 引 H 编号，G2 不引（它引的是决策树条目号）。这只是一条"作者是否在被写下来的
   规范下工作"的证据，**不进入**前三问的判分——G2 图型选得对、没违规，不因为没抄 H 编号而扣分。

`````

### 7-1 判断层的**射程**（不许读过头）

判者提示词里**逐字内嵌的规范规则只有一条**：`composition data must not be drawn as a pie chart`
（= `house-style.md` 的 **H6**；该文件的「验证状态三级」一段自己写明"判断层的实际射程只有
单规则"）。⇒ **判者判"correct"不等于规范得到背书**：除 H6 以外，判者的任何结论都是
**判者自己的判断力**，不是规范条文被验证。本文凡引用判者结论处，一律按此口径读。

### 7-2 任务书点名要回答的那一问：GREEN 的图型选择**是不是因为读了规范才对的**？

**可判线索（本文当场实测）**：产物里是否引用了 `H<n>`。三份 `make_figure.py` 的实测结果：

```
$ python - <<PY   # 三份 GREEN 产物脚本里出现的 H<n> 编号

import pathlib, re
for n in (1, 2, 3):
    p = pathlib.Path("tests/skills/figure-choose/green/out-G%d/make_figure.py" % n)
    hits = sorted(set(re.findall(r"H\d{1,2}", p.read_bytes().decode("utf-8"))),
                  key=lambda s: int(s[1:]))
    print("out-G%d/make_figure.py: %s" % (n, " ".join(hits) if hits else "(无 H<n> 引用)"))
PY
out-G1/make_figure.py: H1 H3 H4 H5 H6 H7 H9 H10 H12
out-G2/make_figure.py: (无 H<n> 引用)
out-G3/make_figure.py: H1 H3 H4 H5 H6 H7 H9 H10 H11 H12
[exit=0]
```
**结论（分两半说，不许含糊）**：

- **G1 与 G3：是（可判）。** 两份 `make_figure.py` 里**逐条**引用了 `H1 H3 H4 H5 H6 H7 H9 H10 H12`
  等编号，写手自己的报告也逐条写成 `要点 → H<n>`（`green/green-self-reports.md` 里是原文）。
  H 编号**只存在于** `.claude/skills/mcm-figure-choose/references/house-style.md` 与
  `chart-types.md`，且 GREEN 侧**唯一新开的那一条通道**就是那个 skill 目录 ⇒
  这两份产物的设计**确实取自规范**。
- **G2：分两个口径答（如实写，不合并成一个）。**
  - **只看产物 ⇒ 判不出。** 它的 `make_figure.py` 里**一个 `H<n>` 都没有**；
    从产物本身只能说"与规范不矛盾"。
  - **产物之外的同类证据（写手自报）⇒ 可判，而且更直接。** `green/green-self-reports.md` 里
    G2 的写手**自己列了一整行 `Design points → H-IDs`**（`H1·H2·H3 … H13` 逐条点名），
    本节末的取证命令把它当场抓出来。写手报告**不是产物**，但它与产物一样是 GREEN 侧新开的
    那条通道的产物 ⇒ 从这个口径看，G2 的设计**也是**取自规范的（`H<n>` 只存在于那个 skill 目录）。
  - **不许把两个口径混成一个**：任务书允许的"判不出"**只对产物本身成立**；
    "写手报告里有全表"是**比产物更强的证据**，不能因为产物里没痕迹就把它一起否掉。

```
$ python - <<PY   # G2 写手自报里的 `Design points → H-IDs` 全表（机器抓）

import pathlib, re
p = pathlib.Path("tests/skills/figure-choose/green/green-self-reports.md")
t = p.read_bytes().decode("utf-8")
m = re.search(r"^\*\*Design points → H-IDs\*\*:.*$", t, re.M)
print("green-self-reports.md 行号 = %d" % (t[:m.start()].count("\n") + 1 if m else -1))
print(m.group(0) if m else "(没找到 'Design points → H-IDs' 一行)")
assert m, "green-self-reports.md 里找不到 G2 写手自己列的 H-ID 全表"
PY
green-self-reports.md 行号 = 116
**Design points → H-IDs**: canvas/orientation H1·H2·H3; colour density H4 (two accent hues #C1440E / #16697A + greys); no matplotlib default colour order H5; no pie H6; no 3-D H7; multi-panel on one page H8; caption template H9; spines removed / ticks inward / units on axis labels H10; one scale per panel, no dual axis H11; in-figure text 8 pt (7.5 pt for the profile axis names and the note) H12; no distribution figure used as a threshold H13.
[exit=0]
```

- **★ 但"照规范做"≠"选择正确是规范的功劳"**：规范在**图型选择**上给的是决策树
  （`chart-types.md`），而**判者没有读规范**、判者也不知道写手读没读 ⇒ 判者判"correct"
  这件事本身**不能**归因给规范。能归因的只有："GREEN 产物（或写手自报）里留下了引用规范的痕迹" +
  "判者独立地认为选型合适" 这两件事**同时**成立。

### 7-3 对判词原件做过的**两处**编辑（登记，不藏）

`green/judge-green.md` 是判者写的判词。本轮为了本仓纪律与准确性做了**两处**编辑
（本件文首也留了同样的登记句），逐条如下：

| # | 改了什么 | 为什么 | 复核依据 |
| :- | :--- | :--- | :--- |
| 1 | **3 处**本仓绝对路径 → `<REPO>` | 本仓规定"报告与证据里不写绝对路径" | §7 开头那次体检：残留绝对路径 0 处 |
| 2 | 判者写"次小 A–E = **0.07**" → **0.0616** | 按 `red/brief-R1.md` 的构成表实算 15 对欧氏距离，最小 B–D=0.0424、**次小 0.0616**（A–E 与 C–F 并列）；0.07 是目测值 | 下面这次复算 |

两处都**不改变判者的结论**：0.0616 与 0.0424 的大小关系，与 0.07 与 0.0424 的大小关系相同
（"B–D 是最相似的一对"仍成立）。

```
$ python - <<PY   # 按 brief-R1.md 的构成表复算 15 对欧氏距离

import itertools, math, pathlib, re
t = pathlib.Path("tests/skills/figure-choose/red/brief-R1.md").read_bytes().decode("utf-8")
rows = {m.group(1): tuple(float(m.group(i)) for i in (2, 3, 4))
        for m in re.finditer(r"^\|\s*([A-F])\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|", t, re.M)}
print("从 brief-R1.md 抽到的区数 =", len(rows), sorted(rows))
ds = sorted((math.dist(rows[a], rows[b]), a, b) for a, b in itertools.combinations(sorted(rows), 2))
print("15 对欧氏距离，最小三对：")
for d, a, b in ds[:3]:
    print("  %s-%s  %.4f" % (a, b, d))
print("最小 = %.4f（%s-%s）；次小 = %.4f（%s-%s）%s"
      % (ds[0][0], ds[0][1], ds[0][2], ds[1][0], ds[1][1], ds[1][2],
         ("（与 %s-%s 并列）" % (ds[2][1], ds[2][2])) if abs(ds[1][0] - ds[2][0]) < 1e-12 else ""))
PY
从 brief-R1.md 抽到的区数 = 6 ['A', 'B', 'C', 'D', 'E', 'F']
15 对欧氏距离，最小三对：
  B-D  0.0424
  A-E  0.0616
  C-F  0.0616
最小 = 0.0424（B-D）；次小 = 0.0616（A-E）（与 C-F 并列）
[exit=0]
```

==============================================================================
§8 与任务书/协议的偏离登记（逐条）
==============================================================================

| # | 偏离 | 为什么 | 落在哪 |
| :- | :--- | :--- | :--- |
| A | 产物目录用 `green/out-G{n}/` 子目录，而非任务书 Files 段的前缀式 `out-G1.*` | 与 RED 侧同款（`red/red-evidence.md` §9-C 已登记同一偏离），使两侧产物单元同形、下游命令不随写手命名漂移 | `green/out-G{n}/` |
| B | PNG 载体**追加**了一组按真实导出 dpi 的读数 | Task 2 Step 3 命令里的 `--dpi` 是**占位符**（`--dpi <导出 dpi>`，见 `.superpowers/sdd/task-m3-t2-brief.md`）；字面 `300` 只出现在 `red/red-evidence.md`，因为 RED 三份**恰好**都导出 300 dpi。GREEN 的 R2/R3 是 200 dpi ⇒ 硬套 300 会量错物理尺寸（F1 假红）。**两组读数都逐字列出**，`300` 那组没有删 | §2.2 |
| C | 判者提示词比 RED 版**多了一问**（第 4 问：产物里有没有 `H<n>` 引用） | 任务书 §Step 3 点名要回答"是不是因为读了规范才对的"；不给这一问就无从回答。**它不改变前三问**，也不向判者泄露任何规范内容 | §7-2 |
| D | 抢救件 `green/green-self-reports.md` + `rescue-transcripts.py` 入库（任务书未列） | 与 RED 同款。这是"写手只读了那一份 brief + skill"的**唯一不可再生**证据（transcript 在仓外、`.superpowers/` 是 gitignored） | 本目录 |
| E | 新增 `green/README.md` | 本目录的入口说明（与 `red/README.md` 对称），并登记"本目录也是泄题风险件" | 本目录 |
| F | **改了 `green/judge-green.md` 原件两处**：3 处绝对路径 → `<REPO>`；"次小 A–E = 0.07" → 0.0616 | 前者是本仓"不写绝对路径"的硬规定（上一版只掩了内联副本、原件仍带绝对路径，属**漏登记**）；后者是判者的目测值与实算不符（实算 0.0616）。两处都在本件文首留了登记句 | §7-3 |

**一处如实说明（措辞不许强过实测）**：§0.3 的"只改隔离句"是**机器 diff 的结论**，口径是
"先抹掉两版**临时目录名**这一个 token 再 diff"（临时目录名两侧必然不同 —— RED-2 那次搬家
同样变过）。抹掉之后，机器报的是：**公共前缀 180 字符 / 公共后缀 39 字符**，
中间那段改动区间 RED-2 是 `only from that brief`、GREEN 是 `from that brief and the skill at
.claude/skills/mcm-figure-choose/`；difflib 把它切成 **2 段（一删一插）**，
因为中间的 `from that brief` 逐字保留。⇒ 准确说法是"**改动全部落在这一个从句内，从句之外
逐字节相同**"，**不是**"逐字符只有一个 hunk"。

**一处没做的（措辞按实测改准）**：`caption.txt` **不保证**由 `make_figure.py` 再生 ——
上一版写成"**三份** GREEN 的脚本都只再生图"，**不实**：当场扫三份脚本，`out-G2/make_figure.py`
确实写了 `caption.txt`。**准确说法是"G1 与 G3 的图注不由各自的脚本再生"**；
与 RED 同款的那条已知缺口（`red/red-evidence.md` §7 末条）**只覆盖 G1 / G3**。
若要让 G1/G3 的图注也可复算，得在 brief 里加要求；本轮**没有**加，
免得与 RED 侧的 brief 不再逐字相同（那会破坏 §0.1）。

```
$ python - <<PY   # 三份 GREEN 脚本里与 caption 有关的行（机器扫，不靠自报）

import pathlib
for n in (1, 2, 3):
    p = pathlib.Path("tests/skills/figure-choose/green/out-G%d/make_figure.py" % n)
    hit = [(i + 1, l.strip()) for i, l in enumerate(p.read_bytes().decode("utf-8").splitlines())
           if "caption" in l.lower()]
    print("out-G%d/make_figure.py  提到 caption 的行 %d 行：" % (n, len(hit)))
    for i, l in hit:
        print("    %4d  %s" % (i, l))
PY
out-G1/make_figure.py  提到 caption 的行 1 行：
      19  H9  caption is "Figure N:" + ASCII colon, <= 12 words, no trailing period
out-G2/make_figure.py  提到 caption 的行 4 行：
      20  figure.pdf and caption.txt next to this file.
      36  OUT_TXT = os.path.join(HERE, "caption.txt")
      74  CAPTION = "Figure 1: Scatter panels rank slope first; A and C share a profile"
     424  fh.write(CAPTION + "\n")
out-G3/make_figure.py  提到 caption 的行 1 行：
      46  H9  caption (caption.txt) is `Figure 1:` + ASCII colon, <= 12 words, no
[exit=0]
```
⇒ **G2 写了 `caption.txt`（`OUT_TXT` → `open(..., "w")`），G1 / G3 没有** ——
上一版那句"三份都只再生图"在下一次报告里不许再出现。
