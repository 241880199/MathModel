#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 `tests/skills/figure-choose/skill-verify.txt`（Task 5 的逐字证据件）。

用法：  python tests/skills/figure-choose/gen-skill-verify.py

## 为什么要落盘

与 `gen-house-style-verify.py` / `gen-chart-types-verify.py` 同一惯例：证据件要能被**复核员
自己重跑出来**，而不是只能读我贴的那几行。落盘的生成器 = 把"哪些命令、以什么顺序、输出怎么截"
这件事本身也变成可复跑的。

## 纪律

- **`write_bytes` 落盘**（Windows 上 `write_text` 会把 LF 写成 CRLF，而证据件恒 LF）；
- **不写绝对路径**（全程用 `Path(__file__)` 推仓根；命令一律用仓内相对路径）；
- 所有子进程命令的 `cwd` = **仓根**；
- §4 的几组读数**由本生成器当场算**（不经 shell）—— 手敲的带引号命令会被再切一次、
  **exit=2、什么都没证**（Task 3 §5 的教训）。这里按表达式直接算，数就是现场数。

## 五节

§0 blob 自证（含 `SKILL.md` 自身的 blob）· §1 只跑 SKILL 守卫 `K1`–`K8` · §2 全量守卫
（含 K 与 S 两族）· §3 变异驱动器（一条命令跑全部；含 `M29`–`M41`，其中 `M34`/`M41` 打的是
`house-style.md` 的副本、`M33`/`M40` 是**自造〔拟建〕场景**）· §4 生成器当场算的几组读数（两道臂的读数 /
声明到的结构性计数与白名单 / 入口表与生成性标记 / 五段与逐条验证行）· §5 自证。
"""
import importlib.util
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]                      # 仓根（本文件在 tests/skills/figure-choose/）
REF = ROOT / ".claude/skills/mcm-figure-choose/references"
SKILL = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"
OUT = HERE / "skill-verify.txt"
CHK = HERE / "check-house-style.py"
MUT = HERE / "mutate-figure-style.py"
FILES = [SKILL, CHK, MUT, HERE / "gen-skill-verify.py"]

KIDS = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8"]
ENTRIES = ["比较", "分布", "相关", "构成", "时序", "空间", "流程", "机理", "不确定性"]
ID_RE = re.compile(r"H\s*\d+")              # 与检查器 `SK_ID_RE` 同口径（现算，不抄检查器的常量）
NUM_RE = re.compile(r"\d+(?:\.\d+)?")
PLOT_RE = re.compile(r"mcm-plot-[a-z]+")
ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|")   # 决策树入口表的行标签（`K4`/`K5` 的锚）
SECTIONS = ("什么时候用", "决策树", "输出契约", "边界", "指针")
ITEMS = ("**推荐图型**", "**理由**", "**设计要点**")
VERIFY_RE = re.compile(r"\*\*验证\*\*\s*[：:]")
H_RE = re.compile(r"^### H\d+\.", re.M)

HEADER = """Task 5 证据 · SKILL.md（短契约：何时用 / 决策树九入口 / 输出契约 / 边界 / 指针）+ 守卫 K1–K8
生成者：Task 5 实施者（2026-09-27；修复轮同日追加）· 写入用 write_bytes ⇒ 本文件恒 LF · 逐字输出
本文件由 `python tests/skills/figure-choose/gen-skill-verify.py` 整份重生成；命令 cwd = 仓根。
收工时的 `git status --short` 为空见报告（本文件生成于入库之前）。

读法提示（六处最容易看错的地方）：
  1. **`K3` 是两道并列的臂，都要绿**：① **主臂（禁止串）** 从
     `house-style.md` 现抽**三族参照物**（小数字面量 + **六个阈值标记**后面那个整数值，后者按
     **方向**分成上界 / 下界两族值池；本次 §4a 印出三族读数），**不抄进脚本**；
     ② **中文数词臂** —— 规范值用
     **中文数词**写出来同样是重述（`主色四色以内` / `一倍正文宽` / `七磅` / `不超过四`）。
     ★ **主臂的阈值族是"同一方向内标记可互换"**：规范写 `≤4 色`、skill 写 `上限 4 色` /
     `不超过 4` 都算同一个阈值的重述；**跨方向不算**（`≥4` 与 `≤4` 是两个不同的阈值）——
     不分方向就会在**别人的规则**上假红（实测 `mcm-abstract/SKILL.md:16` 的 `字体 ≥12pt`）。
     中文臂的口径（**写实，不是"全覆盖"**）：只认"规范单位词紧跟中文数词"与"≥4 的规范整数值的
     中文写法"（阈值由 `≤`/`≥`/`上限`/`下限`/`不超过`/`<n 词` 现取，**不分方向** ——
     它在 skill 那边只看得到数词）；**1–3 的中文写法、百位以上、无标记裸整数（`主色 4 个`）、
     以及"这句话是不是在复述规范"本身都不在机械射程内**。两道臂的实测读数见 §4a。
  2. **`K5` 卡的是数字的处置**：除 `H<n>` 编号外，**全文每个数都必须被显式声明为结构性计数**
     （声明行含『结构性计数』）；且**声明行上只许出现契约数**（白名单恰 `[入口数]`），
     **入口数必须等于 SKILL.md 自己那张决策树表的行数**。§4b 印出声明到了哪几个数、白名单、
     表行数。**已知边界（写实）**：白名单只有"入口数"这一个锚，本文件之外判不了"输出契约有几项"。
  3. **`K6` 是双向的**：① **不存在**的绘图 skill 必须标〔拟建〕（一个都不点名也红，fail-closed）；
     ② **存在**的 skill **不许**标〔拟建〕（否则 skill 真建出来那天会强制保留一个不成立的标记）。
     §4c 印出点名了哪几个、各自的存在性与标记。
  4. **`M30` 的 NOTE 是现算的**：任务书那条宽松谓词（相对路径**或**裸文件名任一命中即可）
     在那种改法下**不会红**（SKILL.md 通篇要提规范，裸文件名必然还在）⇒ `K2` 被收紧成
     **skill 目录内的相对路径**，即 Task 7 的检查器要核的那个形态。
  5. **`K3` 的 fail-closed 臂由 `M34` 证**：把 `house-style.md` 的**副本**里的小数与 `≤n`
     抹光 ⇒ 参照物抽不齐 ⇒ `K3` 必须红。"抽不到即 FAIL"不是注释里的一句话。
  6. **`K7`/`K8` 是修复轮补的两条**：`K7` = 五段标题齐全 + 输出契约三件套**落在该段里**
     （`M38` 证：整段删掉时 `K1`–`K6` **一条都不红**）；`K8` = `house-style.md` 每个 `H<n>`
     条目**恰有一行**『**验证**：』—— `SKILL.md` 那句"逐条标了验证状态"所以要成立（`M41` 证）。
"""


def rel(p):
    return pathlib.Path(p).relative_to(ROOT).as_posix()


def _load(path, name):
    """本仓既有惯用法（带连字符的脚本名不能 `import`）—— 用于**复用**检查器的 `k3_main_hits()`。"""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, (p.stdout + p.stderr).rstrip("\n")


def sha(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True).stdout.strip()


class Ev:
    def __init__(self):
        self.lines, self.log = [], []

    def __call__(self, s=""):
        self.lines.append(s)

    def banner(self, t):
        self("=" * 78)
        self(t)
        self("=" * 78)

    def cmd(self, argv, shown=None):
        shown = shown or " ".join(argv)
        self(f"$ {shown}")
        rc, out = run(argv)
        if out:
            self(out)
        self(f"[exit={rc}]")
        self.log.append((shown, rc))
        self()
        return rc


def main():
    ev = Ev()
    for line in HEADER.splitlines():
        ev(line)
    ev()

    ev.banner("§0  blob 自证（git hash-object：被验对象就是即将入库的那几个文件）")
    for f in FILES:
        ev(f"{sha(f)}  {rel(f)}")
    ev()

    ev.banner("§1  只跑 SKILL 守卫：python tests/skills/figure-choose/check-house-style.py "
              "--only " + " ".join(KIDS))
    ev.cmd([sys.executable, rel(CHK), "--only", *KIDS],
           "python " + rel(CHK) + " --only " + " ".join(KIDS))

    ev.banner(f"§2  全量守卫（规范数守卫 + CENSUS + 结构守卫 S1–S5 + SKILL 守卫 "
              f"K1–K{len(KIDS)}，含 provenance 复跑 46 条）："
              f"python tests/skills/figure-choose/check-house-style.py")
    ev.cmd([sys.executable, rel(CHK)], "python " + rel(CHK))

    ev.banner("§3  变异驱动器（一条命令跑全部）：python tests/skills/figure-choose/mutate-figure-style.py")
    ev.cmd([sys.executable, rel(MUT)], "python " + rel(MUT))

    # ---------------- §4
    ev.banner("§4  生成器当场算的四组读数（**不经 shell** ⇒ 没有引号可切）")
    ev("说明（与 Task 3 §5 同一条教训）：手敲的带引号命令会被再切一次、exit=2、什么都没证。")
    ev("下面四组数由本生成器**直接算**并打印（只有 §4a 那一行读数是从检查器的输出里引的，"
       "引的就是上面 §1/§2 会印的那一行）；命令就是上面那一行 `python …/gen-skill-verify.py`。")
    ev()

    skill_text = SKILL.read_bytes().decode("utf-8")
    doc_text = (REF / "house-style.md").read_bytes().decode("utf-8")

    ev("§4a  `K3` 的两道臂（**逐字引用检查器自己印的那一行** —— 读数只有一份，不另抄一份常数）")
    ev.cmd([sys.executable, rel(CHK), "--only", "K3"], "python " + rel(CHK) + " --only K3")
    # M3-T1 起：这一行不再**抄**一条正则（抄件会随检查器漂移，本仓明令"绝不抄实现"），
    # 改为 import 复用检查器自己的 `k3_main_hits()` —— 口径与检查器**逐位同一份代码**。
    hs = _load(CHK.resolve(), "check_house_style")
    hits, (dec, up, lo) = hs.k3_main_hits(doc_text, skill_text)
    ev("     主臂的参照物（生成器旁证，**import 复用检查器的 `k3_main_hits()`**，不是抄一条正则）：")
    ev(f"       小数 {len(dec)} 条 · 阈值值池 上界 {sorted(up)} / 下界 {sorted(lo)}"
       f" · SKILL.md 命中 {hits or '无'}")
    ev("     阈值族的方向纪律：**同一方向内标记可互换**（规范 `≤4` ↔ skill `上限 4` 是同一个阈值）、"
       "**跨方向不算**（`≥4` 与 `≤4` 是两个不同的阈值）—— 不分方向会在别人的规则上假红。")
    ev("     中文数词臂的**射程写实**：只认 ① 规范单位词紧跟中文数词 ② ≥4 的规范整数值的中文写法；"
       "**1–3 的中文写法 / 百位以上 / 无标记裸整数 / 『是不是在复述规范』本身，都不在机械射程内**。")
    ev("     （四种中文写法各自会红：`M35` 证『四色』、`M36` 证『一倍』；"
       "『七磅』与『四个主色』走的是同两条臂 —— 见 §3 的 `M35`/`M36`。）")
    ev()

    ev("§4b  `K5` 的声明（声明行只许出现契约数；入口数须 == SKILL.md 自己那张表的行数）")
    decl = [l for l in skill_text.splitlines() if "结构性计数" in l]
    declared = {n for l in decl for n in NUM_RE.findall(ID_RE.sub("", l))}
    undeclared = sorted(set(NUM_RE.findall(ID_RE.sub("", skill_text))) - declared)
    ev(f"     声明行 {len(decl)} 行：")
    for l in decl:
        ev(f"       『{l.strip()}』")
    ev(f"     声明到的数 {sorted(declared) or '无'} · 白名单恰 [{len(ENTRIES)}]"
       f" · 多出 {sorted(declared - {str(len(ENTRIES))}) or '无'}"
       f" · 入口数 {len(ENTRIES)} {'在声明里' if str(len(ENTRIES)) in declared else '**不在声明里 ⇒ 红**'}")
    rows = [m.group(1).strip() for l in skill_text.splitlines() if (m := ROW_RE.match(l))]
    ev(f"     决策树表 {len(rows)} 行（应 {len(ENTRIES)}）· 行标签 "
       f"{'== 契约：' + str(rows) if rows == ENTRIES else '**≠ 契约**：' + str(rows)}")
    ev(f"     全文去掉 `H<n>` 编号后的数 {sorted(set(NUM_RE.findall(ID_RE.sub('', skill_text))))}"
       f" · 其中未声明的 {undeclared or '无'}")
    ev(f"     行数 {len(skill_text.splitlines())}（`K1` 上限：<150）")
    ev()

    ev("§4c  `K4`/`K6`：九个入口名（含表标签）与『标记必须与事实一致』")
    ev(f"     入口名逐个在 SKILL.md 里："
       + "、".join(f"{e}={'在' if e in skill_text else '**缺**'}" for e in ENTRIES))
    names = sorted(set(PLOT_RE.findall(skill_text)))
    for n in names:
        exists = (ROOT / ".claude/skills" / n).exists()
        lines = [l for l in skill_text.splitlines() if PLOT_RE.search(l) and n in l]
        marked = all("〔拟建〕" in l for l in lines)
        ev(f"     {n}：存在={exists} · 标了〔拟建〕={marked}"
           f" ⇒ {'**标记与事实不符 ⇒ 红**' if exists == marked else '一致'}")
    ev("     边界段里点名的每一行：")
    for l in skill_text.splitlines():
        if PLOT_RE.search(l):
            ev(f"       『{l.strip()}』")
    ev()

    ev("§4d  `K7`/`K8`：五段与三件套 / 逐条验证行")
    heads = [l[3:].strip() for l in skill_text.splitlines() if l.startswith("## ")]
    ev(f"     `## ` 标题 {len(heads)} 个：{heads}")
    ev(f"     五段逐个："
       + "、".join(f"{s}={'在' if any(s in h for h in heads) else '**缺**'}" for s in SECTIONS))
    body = []
    cur = None
    for l in skill_text.splitlines():
        if l.startswith("## "):
            cur = l[3:].strip()
        elif cur is not None and "输出契约" in cur:
            body.append(l)
    ev(f"     输出契约段内三件套："
       + "、".join(f"{i.strip('*')}={'在' if i in chr(10).join(body) else '**缺**'}" for i in ITEMS))
    ev(f"     `house-style.md`：`### H<n>.` 条目 {len(H_RE.findall(doc_text))} 个 · "
       f"`**验证**：` 行 {len(VERIFY_RE.findall(doc_text))} 行"
       f"（`K8` 是**逐条**核『恰一行』，不是只比总数）")
    ev()

    # ---------------- §5
    bad = [(c, rc) for c, rc in ev.log if rc != 0]
    ev.banner("§5  本节自证：上面每条命令都要 exit=0")
    ev(f"§0-§4 共跑 {len(ev.log)} 条；非零退出 {len(bad)} 条"
       + ("" if not bad else "：" + "; ".join(f"{c} → exit={rc}" for c, rc in bad)))
    ev()

    blob = ("\n".join(ev.lines) + "\n").encode("utf-8")
    OUT.write_bytes(blob)                                    # write_bytes ⇒ 恒 LF
    print(f"wrote {rel(OUT)}  bytes={len(blob)}  lines={blob.count(10)}  "
          f"命令 {len(ev.log)} 条 · 非零退出 {len(bad)} 条")
    if bad:
        for c, rc in bad:
            print(f"  exit={rc}  {c}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
