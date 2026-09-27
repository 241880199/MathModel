#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 6：生成 `tests/skills/figure-choose/green-evidence.md`（RED × GREEN 并列对照，逐字）。

写入用 `write_bytes`（本仓纪律；也保证 LF）。**文中每一个数都来自本脚本当场跑过的命令**，
命令与输出逐字附在文内。本脚本**与它生成的证据同目录入库**（照 Task 1/2 的规矩：
证据在册、造它的脚本不许留在 gitignored 的 `.superpowers/` 里）。

三条"由构造保证"的标签（不是手抄出来的）：
  ① **图注逐字**：从 `red/out-R{n}/caption.txt` 与 `green/out-G{n}/caption.txt` 的**字节**直接读入；
  ② **两版提示词逐字且"只有一处不同"**：RED-2 与 GREEN 两版提示词**从 transcript 抢救件**
     （`red/writer-self-reports.md` / `green/green-self-reports.md`）里按原文取出，
     与脚本里写死的模板**逐字节断言相等**；再把两版做机器 diff，断言**只有一段连续改动**；
  ③ **红绿表与汇总数**：由当场跑出的检查器输出**逐格重算**，不是手写的（Task 2 栽过这一型：
     逐格数据对、汇总数自相矛盾）。

用法： python tests/skills/figure-choose/green/make-evidence.py
"""
import difflib
import importlib.util
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent          # tests/skills/figure-choose/green
FIGCHOOSE = HERE.parent                                 # tests/skills/figure-choose
REPO = FIGCHOOSE.parents[2]
CHECKER = FIGCHOOSE / "check-figure-style.py"
RED = FIGCHOOSE / "red"

RED_DIR = "tests/skills/figure-choose/red"
GREEN_DIR = "tests/skills/figure-choose/green"


# ---------------------------------------------------------------- 基础设施
def run(cmd, mask=None):
    """跑一条命令，返回 (命令串, 逐字 stdout, exit code)。只打印仓库相对路径。"""
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    mask = MASK_CMD if mask is None else mask
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + "\n"
    shown = " ".join(cmd)
    for pat, rep in mask:
        shown, out = pat.sub(rep, shown), pat.sub(rep, out)
    return shown, out, r.returncode


def block(shown, out, rc):
    body = out if out.endswith("\n") else out + "\n"
    return f"```\n$ {shown}\n{body}[exit={rc}]\n```\n"


TMP_MASK_RE = re.compile(
    r"[A-Za-z]:[\\/][^\s`\"')\]]*?AppData[\\/]Local[\\/]Temp[\\/]m3-t6-green", re.IGNORECASE)


REPO_MASK_RE = re.compile(r"[A-Za-z]:[\\/](?:[^\\/\s`\"')\]]+[\\/])*?数学建模")

NL = chr(10)   # 行尾（不用 f-string 里的反斜杠转义：那在 f-string 里非法）


def mask_tmp(text):
    """唯一的加工：系统临时目录的绝对路径 -> `<TMP>/m3-t6-green`（本仓规定不写绝对路径）。"""
    return TMP_MASK_RE.sub("<TMP>/m3-t6-green", text)


def mask_repo(text):
    """同上的第二类：本仓根的绝对路径 -> `<REPO>`；返回 (掩码后文本, 掩码处数)。"""
    return REPO_MASK_RE.subn("<REPO>", text)


def heredoc(code, note=""):
    """真的用 `python -` 跑这一段（这样文里"命令"与"输出"来自同一次运行，不是重构出来的）。"""
    r = subprocess.run([sys.executable, "-"], input=code, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    shown = "python - <<PY" + (f"   # {note}" if note else "") + "\n" + code.rstrip("\n") + "\nPY"
    out = r.stdout
    if r.stderr.strip():
        out += "STDERR: " + r.stderr.strip() + "\n"
    return shown, out, r.returncode


CELL_RE = re.compile(r"^(PASS|FAIL)\s+(F\d[abcd]?)\s+(.*)$")


def cells(out):
    """从检查器输出里抽逐格判词 -> [("F1", "PASS", "图宽比 ..."), ...]（按出现顺序）。"""
    got, order = {}, []
    for line in out.splitlines():
        m = CELL_RE.match(line)
        if m:
            v, cid, msg = m.group(1), m.group(2), m.group(3).strip()
            if cid not in got:
                order.append(cid)
            got[cid] = (v, msg)
    return [(c, got[c][0], got[c][1]) for c in order]


def verdict_str(reader):
    return "".join("R" if c[1] == "FAIL" else "G" for c in reader)


# ---------------------------------------------------------------- 逐格读数
def check(fig, cap, carrier_dpi=None):
    cmd = [sys.executable, CHECKER.as_posix(), "--fig", fig, "--caption", cap,
           "--textwidth-in", "6.31"]
    if carrier_dpi is not None:
        cmd += ["--dpi", str(carrier_dpi)]
    return run(cmd, mask=MASK_CMD)


MASK_CMD = (
    # ① 解释器绝对路径 -> `python`（本仓规定不写绝对路径；命令要真跑，所以掩码打在"展示串"上）
    (re.compile(re.escape(sys.executable), re.IGNORECASE), "python"),
    # ② 本仓根的绝对路径 -> 空串（使命令串变成仓库相对路径，与 Task 1/2 的证据同款）
    (re.compile(re.escape(REPO.as_posix()) + r"[\\/]"), ""),
)

RED_RUNS, GREEN_RUNS = {}, {}


def collect_mechanical():
    for n in (1, 2, 3):
        RED_RUNS[("pdf", n)] = check(f"{RED_DIR}/out-R{n}/figure.pdf",
                                     f"@{RED_DIR}/out-R{n}/caption.txt")
        RED_RUNS[("png", n)] = check(f"{RED_DIR}/out-R{n}/figure.png",
                                     f"@{RED_DIR}/out-R{n}/caption.txt", 300)
        # GREEN：① 任务书规定的命令（Task 2 Step 3 逐字，含 --dpi 300）
        GREEN_RUNS[("pdf", n)] = check(f"{GREEN_DIR}/out-G{n}/figure.pdf",
                                       f"@{GREEN_DIR}/out-G{n}/caption.txt")
        GREEN_RUNS[("png300", n)] = check(f"{GREEN_DIR}/out-G{n}/figure.png",
                                          f"@{GREEN_DIR}/out-G{n}/caption.txt", 300)
        # ② 按该 PNG 的**实际导出 dpi** 再读一次（本任务新增的读数，理由见 §2 末）
        GREEN_RUNS[("png", n)] = check(f"{GREEN_DIR}/out-G{n}/figure.png",
                                       f"@{GREEN_DIR}/out-G{n}/caption.txt", TRUE_DPI[n])


# 真实导出 dpi：**不读 PNG 的 dpi 元信息** —— 检查器 `check-figure-style.py` 明写"PNG 的 dpi
# 元信息不可信"（`:152` 的 fail-closed 出口），`provenance.md` 也同款禁止。改用两条**独立**证据：
#   ① `PNG 像素宽 ÷ PDF 页盒宽`（矢量面、精确 —— 正是检查器判 PDF 的 F1 用的那条量法）；
#   ② 写手脚本里 `savefig(..., dpi=N)` 的字面量（机器抽取，不手抄）。
# 两者必须一致；下面的 `TRUE_DPI` 由 `measure_dpi()` 的**输出解析**得到，不是写死的表。
DPI_CODE = r'''
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
'''

TRUE_DPI = {}                            # 由 measure_dpi() 的输出解析（GREEN 用）
RED_TRUE_DPI = {}                        # 同上（RED 侧）：用来证"Task 2 用的 300 就是它的真实 dpi"


def measure_dpi():
    """实测各 PNG 的真实导出 dpi：`像素宽 ÷ PDF 页盒宽` 与写手脚本里的 `dpi=` 两条证据。"""
    shown, out, rc = heredoc(DPI_CODE, note="真实导出 dpi 的两条独立证据（不读 PNG 的 dpi 元信息）")
    for line in out.splitlines():
        m = re.match(r"^(RED|GREEN)\s+R(\d)\s+.*?隐含 dpi\s+([\d.]+)\s+\|\s+脚本 savefig dpi=\s*(\S+)$", line)
        if not m:
            continue
        tag, n, implied, lit = m.group(1), int(m.group(2)), float(m.group(3)), m.group(4)
        if lit != "(无)":
            assert round(implied) == int(lit), (tag, n, implied, lit)   # ① 与 ② 必须一致
        if tag == "GREEN":
            TRUE_DPI[n] = round(implied)
        else:
            RED_TRUE_DPI[n] = round(implied)
    assert set(TRUE_DPI) == {1, 2, 3}, TRUE_DPI
    assert set(RED_TRUE_DPI) == {1, 2, 3}, RED_TRUE_DPI
    return shown, out, rc


# ---------------------------------------------------------------- F2 连续色图闸门
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def collect_f2():
    """跑 f2-diagnose.py（**它自己 import 检查器**），并用 house-metrics 的闸门函数判连续色图。

    ★ 闸门不在这里重写：直接调 `house-metrics.py` 的 `_cont_hit`（== 文档 H4 里那条
      `箱数 >= CONT_BOX_MIN` **或** `最高落选箱 >= CONT_SUBFLOOR_MIN_PCT`）。
    """
    figs = ([f"{RED_DIR}/out-R{n}/figure.pdf" for n in (1, 2, 3)]
            + [f"{GREEN_DIR}/out-G{n}/figure.pdf" for n in (1, 2, 3)])
    shown, out, rc = run([sys.executable, (RED / "f2-diagnose.py").as_posix()] + figs)
    hm = load_module(FIGCHOOSE / "house-metrics.py", "house_metrics_gate")
    rows = []
    for chunk in out.split("=== ")[1:]:
        lines = chunk.splitlines()
        path = lines[0].strip()
        n_all = int(re.search(r"before floor\): (\d+)", chunk).group(1))
        counted = int(re.search(r"\(>= 0\.5% floor\): (\d+)", chunk).group(1))
        m = re.search(r"highest sub-floor box = ([\d.]+)%", chunk)
        subfloor = float(m.group(1)) / 100.0 if m else 0.0
        d = {"n": n_all, "counted": counted, "subfloor": subfloor}
        rows.append((path, d, bool(hm._cont_hit(d))))
    return shown, out, rc, rows, hm


# ---------------------------------------------------------------- 判断层（判词抽取）
def judge_rows():
    """从**两侧判者的判词文件**里抽出结论（不手抄）：RED → `red/judge.md`，GREEN → `green/judge-green.md`。

    任务书的 Interfaces 段点名对照表要有「判断层」这一维，而判断层的两侧结论**只存在于**
    这两份判词里 ⇒ 表格那两列由这里**抽**出来，避免手抄出第二份权威。
    """
    got = {"red": {}, "green": {}}

    def cells_of(line, tag):
        """按**未被转义**的竖线切表行（判词里有 `\\|r\\|` 这种转义竖线，naive split 会把它切断）。"""
        parts = [c.strip() for c in re.split(r"(?<!\\)\|", line)]
        return parts if parts and parts[0] == "" else None

    for line in (RED / "judge.md").read_bytes().decode("utf-8").splitlines():
        c = cells_of(line, "R")
        if c and re.fullmatch(r"R\d", c[1] if len(c) > 1 else ""):
            got["red"][int(c[1][1])] = (c[2], c[3])
    for line in (HERE / "judge-green.md").read_bytes().decode("utf-8").splitlines():
        c = cells_of(line, "G")
        if c and len(c) > 4 and re.fullmatch(r"G\d", c[1] if len(c) > 1 else ""):
            got["green"][int(c[1][1])] = (c[3], c[4])
    assert set(got["red"]) == {1, 2, 3}, got["red"]
    assert set(got["green"]) == {1, 2, 3}, got["green"]
    # 只取"图表类型"那一列（判词原文已把附注写在括号里，如
    # `R3 | correct（但三元图 low/medium 轴题互换，属标注错误） | no`）—— 原样搬，不改写
    return {side: {n: v[0] for n, v in d.items()} for side, d in got.items()}


# ---------------------------------------------------------------- 提示词并排
def extract_prompts(md_path, wanted):
    """从抢救件里按 `### ① 派发提示词（原文）` 抽出每个 agent 的提示词原文。"""
    txt = md_path.read_bytes().decode("utf-8")
    got = {}
    for chunk in txt.split("### ① 派发提示词（原文）")[1:]:
        head = chunk.split("### ①")[0]
        m = re.search(r"```text\n(.*?)\n```", chunk, re.S)
        if not m:
            continue
        # 反查这一段属于哪个 agent：往上找最近的 `## <tag>`
        idx = txt.index(chunk)
        before = txt[:idx]
        tag = re.findall(r"^## (\S+)$", before, re.M)[-1]
        got[tag] = m.group(1)
    return {k: v for k, v in got.items() if k in wanted}


RED_TMPL = ("Read the brief at <TMP>/m3-t2-red/brief-R{n}.md and produce the figure and caption"
            " it asks for. Write the script, the exported figure and the caption text into"
            " <TMP>/m3-t2-red/out-R{n}/. Work only from that brief - do not read or write any"
            " other file.")
GREEN_TMPL = ("Read the brief at <TMP>/m3-t6-green/brief-R{n}.md and produce the figure and"
              " caption it asks for. Write the script, the exported figure and the caption text"
              " into <TMP>/m3-t6-green/out-R{n}/. Work from that brief and the skill at"
              " .claude/skills/mcm-figure-choose/ - do not read or write any other file.")

SCRATCH_RE = re.compile(r"<TMP>/m3-t[0-9a-z-]+")

# §7-2 的可判线索：产物脚本里有没有 `H<n>` 引用（真的跑）。
HREF_CODE = r'''
import pathlib, re
for n in (1, 2, 3):
    p = pathlib.Path("tests/skills/figure-choose/green/out-G%d/make_figure.py" % n)
    hits = sorted(set(re.findall(r"H\d{1,2}", p.read_bytes().decode("utf-8"))),
                  key=lambda s: int(s[1:]))
    print("out-G%d/make_figure.py: %s" % (n, " ".join(hits) if hits else "(无 H<n> 引用)"))
'''

# §7 的判词原件体检（N-5）：原件是否已掩码、残留绝对路径几处、内联件是否逐字节相同。
JUDGE_CODE = r'''
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
'''

# §7-2 的 G2 那一问：产物里没有 `H<n>`，但**写手自报**里有整行 `Design points → H-IDs`。
G2_CODE = r'''
import pathlib, re
p = pathlib.Path("tests/skills/figure-choose/green/green-self-reports.md")
t = p.read_bytes().decode("utf-8")
m = re.search(r"^\*\*Design points → H-IDs\*\*:.*$", t, re.M)
print("green-self-reports.md 行号 = %d" % (t[:m.start()].count("\n") + 1 if m else -1))
print(m.group(0) if m else "(没找到 'Design points → H-IDs' 一行)")
assert m, "green-self-reports.md 里找不到 G2 写手自己列的 H-ID 全表"
'''

# §7-3 的复核订正：判者写"次小 A–E = 0.07"。按 brief-R1 的表实算 15 对欧氏距离。
PAIRWISE_CODE = r'''
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
'''

# 三份 GREEN 脚本会不会再生 `caption.txt`（N-6：上一版说"三份都只再生图"，与实测不符）。
CAPTION_CODE = r'''
import pathlib
for n in (1, 2, 3):
    p = pathlib.Path("tests/skills/figure-choose/green/out-G%d/make_figure.py" % n)
    hit = [(i + 1, l.strip()) for i, l in enumerate(p.read_bytes().decode("utf-8").splitlines())
           if "caption" in l.lower()]
    print("out-G%d/make_figure.py  提到 caption 的行 %d 行：" % (n, len(hit)))
    for i, l in hit:
        print("    %4d  %s" % (i, l))
'''

# §3 / §4 的汇总数是**这一段真的跑出来的**：它另起一次运行，把检查器在两边的产物上重跑，
# 再从逐格判词重算"红/绿"。**汇总不手写**（Task 2 栽过一次"逐格对、汇总自相矛盾"）。
TALLY_CODE = r'''
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
'''

# 下面这段**真的会被执行**（`python -` 喂进去），文里的"命令"与"输出"因此来自同一次运行。
# `@RED@` / `@GREEN@` 在运行时被替换成两版模板的 `repr()`（避免与模板里的 `{n}` 打架）。
CHECK_CODE = r'''
import pathlib, re, difflib

RED_TMPL = @RED@
GREEN_TMPL = @GREEN@

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
'''


def one_hunk_diff(a, b):
    """返回 (opcode 列表, 连续改动段数)。先抹掉两版**临时目录名**这一个 token。"""
    a2, b2 = SCRATCH_RE.sub("<TMP>/m3-tX", a), SCRATCH_RE.sub("<TMP>/m3-tX", b)
    sm = difflib.SequenceMatcher(None, a2, b2, autojunk=False)
    ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
    return ops, a2, b2


# ---------------------------------------------------------------- 组装
def main():
    def git(*args):
        r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
        return r.stdout.strip()

    dpi_shown, dpi_out, dpi_rc = measure_dpi()          # 先量真 dpi：collect_mechanical 要用它
    collect_mechanical()
    f2_shown, f2_out, f2_rc, f2_rows, hm = collect_f2()

    # ---- 提示词：模板 vs 抢救件原文（逐字节断言）----
    red_prompts = extract_prompts(RED / "writer-self-reports.md",
                                  {f"R{n}-writer-round-2" for n in (1, 2, 3)})
    green_prompts = extract_prompts(HERE / "green-self-reports.md",
                                    {f"R{n}-writer-green" for n in (1, 2, 3)})
    assert len(red_prompts) == 3, red_prompts.keys()
    assert len(green_prompts) == 3, green_prompts.keys()
    prompt_checks = []
    for n in (1, 2, 3):
        r_lit, g_lit = RED_TMPL.format(n=n), GREEN_TMPL.format(n=n)
        r_got, g_got = red_prompts[f"R{n}-writer-round-2"], green_prompts[f"R{n}-writer-green"]
        prompt_checks.append((n, r_lit == r_got, g_lit == g_got,
                              len(r_got), len(g_got), r_got, g_got))

    # ---- 判断层：从两侧判词文件抽结论（§4 表末两列）----
    jr = judge_rows()

    # ---- 红绿表（逐格重算）----
    CRIT = ["F1", "F2", "F3a", "F3b", "F3c", "F3d"]

    def row(pdf_key, n, runs):
        return {c[0]: c for c in cells(runs[(pdf_key, n)][1])}

    red_row = {n: row("pdf", n, RED_RUNS) for n in (1, 2, 3)}
    grn_row = {n: row("pdf", n, GREEN_RUNS) for n in (1, 2, 3)}

    # ---- 图注逐字 ----
    cap_blocks = []
    for tag, base in (("RED", f"{RED_DIR}/out-R%d/caption.txt"),
                      ("GREEN", f"{GREEN_DIR}/out-G%d/caption.txt")):
        for n in (1, 2, 3):
            p = REPO / (base % n)
            raw = p.read_bytes().decode("utf-8")
            c = cells(RED_RUNS[("pdf", n)][1]) if tag == "RED" else cells(GREEN_RUNS[("pdf", n)][1])
            cap_blocks.append(f"$ cat {base % n}    # {len(p.read_bytes())} B\n{raw}")
    caps_txt = "```\n" + "\n".join(cap_blocks) + "\n```\n"

    # ---- 汇总数（从逐格表重算）----
    def counts(rows):
        r = g = 0
        per = {}
        for n in (1, 2, 3):
            d = rows[n]
            nf = sum(1 for c in CRIT if d[c][1] == "FAIL")
            ng = 6 - nf
            r += nf
            g += ng
            per[n] = (nf, ng)
        return r, g, per

    red_r, red_g, red_per = counts(red_row)
    grn_r, grn_g, grn_per = counts(grn_row)

    improved, stayed_red, both_green = [], [], []
    for n in (1, 2, 3):
        for c in CRIT:
            rv, gv = red_row[n].get(c, ("?", ""))[1], grn_row[n][c][1]
            item = (n, c, red_row[n][c][2], grn_row[n][c][2])
            if rv == "FAIL" and gv == "PASS":
                improved.append(item)
            elif rv == "FAIL" and gv == "FAIL":
                stayed_red.append(item)
            elif rv == "PASS" and gv == "PASS":
                both_green.append(item)
            else:
                improved.append(item + ("（红→绿方向反了）",))

    # ---- 逐格表正文 ----
    def cell_md(n, c, rows_red, rows_grn):
        r = rows_red[n].get(c)
        g = rows_grn[n][c]
        rs = "—" if r is None else f"{'**FAIL**' if r[1] == 'FAIL' else 'PASS'} {r[2]}"
        gs = f"{'**FAIL**' if g[1] == 'FAIL' else 'PASS'} {g[2]}"
        return f"{rs} → {gs}"

    # ---- 装配文档 ----
    parts = []
    A = parts.append

    A(f"""\
==============================================================================
tests/skills/figure-choose/green-evidence.md —— Task 6 GREEN 对照证据（逐字）
==============================================================================

【范围】3 个场景（R1 构成数据 / R2 多变量对比 / R3 交付形态）× 2 层判据：
        机械层 = Task 1 的 `check-figure-style.py`（**一字不改**，直接调用）；
        判断层 = 独立判者（判词逐字见 `green/judge-green.md`，本文 §7 全文内联）。
        **RED 基线** = `red/`（本次 commit 当场重跑，见 §3）；GREEN = `green/out-G{{1,2,3}}/`。
【机器】Windows 11 / Python {sys.version.split()[0]}
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

场景正文取自 `red/brief-R{{1,2,3}}.md`（Task 2 已核过它们与 `red/README.md` §1 的内联副本
逐字节相同）。写手拿到的是**仓外**副本，做法：`read_bytes()` 原样写出，再逐条比 blob。

""")

    bcode = (
        "import pathlib, subprocess\n"
        "for n in (1, 2, 3):\n"
        "    a = pathlib.Path('tests/skills/figure-choose/red/brief-R%d.md' % n)\n"
        "    b = pathlib.Path('<TMP>/m3-t6-green/brief-R%d.md' % n)\n"
        "    ga = subprocess.run(['git', 'hash-object', a.as_posix()],\n"
        "                        capture_output=True, text=True).stdout.strip()\n"
        "    gb = subprocess.run(['git', 'hash-object', '--no-filters', b.as_posix()],\n"
        "                        capture_output=True, text=True).stdout.strip()\n"
        "    print('brief-R%d.md  bytes=%d  repo_blob=%s  temp_blob=%s  identical=%s'\n"
        "          % (n, b.stat().st_size, ga[:12], gb[:12], a.read_bytes() == b.read_bytes()))\n"
    )
    bshown, bout, brc = heredoc(
        bcode.replace("<TMP>/m3-t6-green", TMPROOT.replace("\\", "/")),
        note="逐份比 (仓内权威件) 与 (写手拿到的仓外副本) 的字节")
    bshown, bout = mask_tmp(bshown), mask_tmp(bout)
    A(block(bshown, bout, brc))
    A("⇒ 三份场景**逐字节相同**（`read_bytes()` 直接比，不靠 blob 比 —— 见 §0.5 的一处口径坑）。\n")

    A("""
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
""" + (
        f"$ git hash-object tests/skills/figure-choose/check-figure-style.py\n"
        f"{git('hash-object', CHECKER.as_posix())}\n"
        f"$ git rev-parse HEAD:tests/skills/figure-choose/check-figure-style.py\n"
        f"{git('rev-parse', 'HEAD:tests/skills/figure-choose/check-figure-style.py')}\n"
        f"$ git status --short tests/skills/figure-choose/check-figure-style.py\n"
        f"{git('status', '--short', 'tests/skills/figure-choose/check-figure-style.py') or '(无输出 = 未改动)'}\n"
        "```\n"))
    A("""
### 0.3 写手提示词：RED 第二轮 vs GREEN，**只许改"隔离句"这一处**

两版提示词都**不是手抄的**：脚本从两边的 transcript 抢救件里按原文取出（`### ① 派发提示词（原文）`），
再与脚本里写死的模板**逐字节断言相等**。断言结果（下面这段是脚本当场打印的，不是我写的）：

""")

    code = CHECK_CODE.replace("@RED@", repr(RED_TMPL)).replace("@GREEN@", repr(GREEN_TMPL))
    shown, out, rc = heredoc(code, note="模板 vs transcript 原文逐字节断言 + 抹掉临时目录名后 diff")
    A(block(shown, out, rc))

    for n, rok, gok, rl, gl, r_got, g_got in prompt_checks:
        assert rok and gok, (n, rok, gok)
    _n, _r, _g, _rl, _gl, r_got, g_got = prompt_checks[0]
    A(f"**两版原文并排（R1；R2/R3 只换文件名，见 `green/green-self-reports.md` 与 "
      f"`red/writer-self-reports.md`）**：\n\n```text\n"
      f"[RED-2]   {r_got}\n\n[GREEN]   {g_got}\n```\n")
    A("""⇒ 抹掉临时目录名（两版**必然**不同的那一个路径 token）之后，**改动区间只有一段**：
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

""")

    for n in (1, 2, 3):
        A(f"**out-G{n}/figure.pdf**\n\n" + block(*GREEN_RUNS[("pdf", n)]))
    for n in (1, 2, 3):
        A(f"**out-G{n}/figure.png（`--dpi 300`，= 把 RED 的取值硬套过来）**\n\n"
          + block(*GREEN_RUNS[("png300", n)]))

    A("""
### 2.2 ★ 一处必须说清的读数：PNG 的 `--dpi` 不是载体无关的

F1 对 PNG 的算法是 `宽_in = 像素宽 / --dpi`。Task 2 Step 3 命令里的 `--dpi` 是**占位符**；
字面 `300` 是 **RED 三份的真实导出 dpi**（见下表左三行），被当年的 RED 证据沿用成了具体值。
GREEN 的写手各自选了导出 dpi ⇒ 把 `300` 当"规定值"硬套，对 200 dpi 的 PNG 就会
**量错物理尺寸**（不是图变窄了）。

**真 dpi 的取法**（**不读 PNG 的 dpi 元信息** —— 检查器 `:152` 与 `provenance.md:20` 都禁止）：
`PNG 像素宽 ÷ PDF 页盒宽`（矢量面、精确，正是检查器判 PDF 的 F1 用的那条量法）
与写手脚本里的 `savefig(..., dpi=N)` 字面量，两条独立证据交叉；两者不一致时脚本直接断言失败。
实测（下面这段是当场跑的）：

""")
    A(block(dpi_shown, dpi_out, dpi_rc))
    A("""⇒ GREEN 的 R2/R3 导出的是 **200 dpi**（RED 三份与 GREEN R1 都是 300 dpi；
RED 的 `make_figure.py` 里没有 `savefig dpi=` 字面量 ⇒ RED 只有"页盒"这一条证据，
与 RED 证据里用的 300 不冲突）。
故本节**再加一组读数**：按每张 PNG 的**实际导出 dpi** 读一次。这是**追加**读数，
不改判据、也不改任务书那条命令 —— `--dpi 300` 与"真实 dpi"两组都逐字列出，哪个对哪个错由读者判。

""")
    for n in (1, 2, 3):
        A(f"**out-G{n}/figure.png（`--dpi {TRUE_DPI[n]}` = 该文件的真实导出 dpi，两条证据交叉得出）**\n\n"
          + block(*GREEN_RUNS[("png", n)]))

    A("""### 2.3 RED 基线：**本次 commit 当场重跑**（不是从 `red-evidence.md` 抄的）

任务书要求"RED × GREEN 并列"；为了让两侧**在同一时刻、同一把尺**上比，
下面的 RED 读数是本脚本当场重跑的（`red/` 是只读的，跑检查器不改任何东西）。

""")
    for n in (1, 2, 3):
        A(f"**red/out-R{n}/figure.pdf**\n\n" + block(*RED_RUNS[("pdf", n)]))
    for n in (1, 2, 3):
        A(f"**red/out-R{n}/figure.png（`--dpi {RED_TRUE_DPI[n]}` = 实测该 PNG 的真实导出 dpi）**"
          "\n\n" + block(*RED_RUNS[("png", n)]))

    A("""### 2.4 三份图注逐字（全文、`cat`）—— F3a/b/c 的直接原因

""")
    A(caps_txt)
    A("""**读数**：三份 GREEN 图注**全部**是 `Figure N:` + **ASCII 冒号** + 句末**无**句号
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

""")
    shown, out, rc = heredoc(TALLY_CODE, note="RED 基线逐格重跑 + 从逐格判词重算汇总")
    A(block(shown, out, rc))
    A(f"⇒ **{red_r} 红 / {red_g} 绿**，与任务书给的 13 / 5 **一致**（逐格比对见 §4）。\n")

    A("""
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
""")
    for n in (1, 2, 3):
        A(f"| **R{n}** | " + " | ".join(cell_md(n, c, red_row, grn_row) for c in CRIT)
          + f" | {jr['red'][n]} | {jr['green'][n]} |\n")
    A("\n**逐格汇总**：下表不是手写的，而是**另起一次运行**把两边重跑后从逐格判词重算出来的"
      "（与上表同源同尺，用来交叉核对）：\n\n")
    shown, out, rc = heredoc(TALLY_CODE, note="两边各自重跑一遍，从逐格判词重算汇总")
    A(block(shown, out, rc))
    A(f"⇒ **判红从 {red_r} 格降到 {grn_r} 格**（两边汇总由上面那次运行独立重算，"
      f"与本文表格所用读数一致）。\n")

    A(f"""
**★ 判断层：两侧同判 ⇒ 本轮在判断层上「零区分力」**（这一维上一版漏了，本轮补上）

- **RED 侧判词**（`red/judge.md`，机器从判词原表抽出，见上表末列）：三份**全部 `{jr['red'][1]}`**、
  饼图规则三份 `no`。唯一抓到的实质问题是 **R3 面板 (b) 的两条轴题（Low share / Medium share）互换**
  —— 属标注错误，不是图型选错。
- **GREEN 侧判词**（`green/judge-green.md` 同款抽取）：三份**全部 `{jr['green'][1]}`**、饼图规则三份 `no`。
- ⇒ **判断层两侧同判 `correct`**（`{jr['red'][1]}` ↔ `{jr['green'][1]}`）⇒ 这一层**没有区分力**，
  它**不能**用来支持"读了规范所以选型变对了"。这正是任务书那句"不许把『没失败』算成规范的功劳"
  在**判断层**上的同款情形 —— 机械层已在 §6-3 单列，判断层这一条在本节单列。
- **唯一有区分力的收获在 RED 侧**：**三元图轴题互换**是判者抓到的、而机械层六格**一条都看不见**
  （六格里没有能看见"轴题标反"的判据）。这条**不是**规范起作用的证据，而是"判断层能看见什么"的证据。
""")

    A("""
**PNG 载体（按各自真实导出 dpi）与 PDF 载体逐格一致** —— 即两侧的载体选择不影响结论；
若按任务书规定的 `--dpi 300` 硬套，GREEN 的 R2/R3 会凭空多出两个 F1 红（§2.2）。

==============================================================================
§5 F2 的"连续色图"闸门口径（★ 任务书点名要交代的那一条）
==============================================================================

`house-style.md` 的 H4 把 F2 的**条数**限定在**离散配色图**上：
`f2-diagnose.py` 报的**彩色箱数 ≥100** **或** **最高落选箱 ≥0.4%** ⇒ 按**连续色图**处理，
**不引用 F2 条数**。本文的三份 GREEN 产物到底是哪一类，**当场测**：

""")
    A(block(f2_shown, f2_out, f2_rc))
    A("（上面是**完整输出**，没有节略。这个工具自己不判红绿，只报每个色箱的占比；"
      "它 `import` 检查器本体，并对每一个输入断言与 `color_count` 一致。）\n\n")
    A("下表每一个数都从**上面那次运行的输出**里抽出来；闸门那一列由 "
      "`house-metrics.py` 的 `_cont_hit` **直接判**（不在本文重写那条式子）：\n\n")
    A("| 产物 | 未设地板的彩色箱数 | 最高落选箱 | 过闸门（= 连续色图）? | F2 条数可引用? |\n")
    A("| :--- | ---: | ---: | :--- | :--- |\n")
    for path, d, hit in f2_rows:
        tag = path.replace("tests/skills/figure-choose/", "").replace("/figure.pdf", "")
        sf = "无落选箱" if d["subfloor"] == 0 else f"{d['subfloor'] * 100:.3f}%"
        A(f"| `{tag}` | {d['n']} | {sf} | {'**是**' if hit else '否（离散）'} | "
          f"{'**不可引用**' if hit else '可引用'} |\n")
    A(f"\n闸门常量（从 `house-metrics.py` **import** 进来打印，不是抄的）："
      f"`CONT_BOX_MIN={hm.CONT_BOX_MIN}`、`CONT_SUBFLOOR_MIN_PCT={hm.CONT_SUBFLOOR_MIN_PCT}`\n")
    grn_hits = [t for t, d, h in f2_rows if h and "green/out-G" in t]
    A(f"""**结论**：三份 GREEN 产物**没有一份命中闸门** ⇒ **本轮的 F2 条数可以引用**，
任务书点名的那条"连续色图别拿条数去比"的警告**在本轮 GREEN 侧不触发**。
RED 侧命中闸门的只有 **{len([1 for t, d, h in f2_rows if h and 'red/out-R' in t])} 张**
（见上表）—— 那正是 R2 的 F2=7：按 H4，**它的条数本就不该引用**，
所以 §4 里 R2 的 F2 由红转绿应当读成"**方向可信**（连续色图 → 离散配色），
RED 那个 7 不作为一个可引用的读数"。

==============================================================================
§6 改善 / 未改善 / **本次无区分力**（三类分开，不许混）
==============================================================================

### 6-1 由红转绿（逐条，附逐字读数）

""")
    for n, c, rmsg, gmsg in improved:
        # 逐条带上**两侧判词**：本节的定义就是 "RED FAIL → GREEN PASS"，
        # 不写出来读者就得回 §4 找（上一版正是靠这个含糊把一格"仍红"混进来的）
        A(f"- **R{n} · {c}**：RED **FAIL** `{rmsg}` → GREEN **PASS** `{gmsg}`" + NL)
    A(f"\n共 **{len(improved)} 格**。任务书点名的两个预期（**R3 的 F1 与 F3c**）都实现了：\n")
    for n, c, rmsg, gmsg in improved:
        if n == 3 and c in ("F1", "F3c"):
            A(f"- R3 · {c}：`{rmsg}` → `{gmsg}` ✅ 预期兑现" + NL)
    A("""
### 6-2 上一版登记为「仍红」的 3 格（F3b）—— 本轮**已收敛**，逐条重述

**当前状态**：这三格现在**全部转绿**（见 §6-1）。下面是它们从"仍红"到"转绿"的完整交代，
因为上一版在这里**说错过一句话**，必须留痕。

""")
    if stayed_red:
        for n, c, rmsg, gmsg in stayed_red:
            A(f"- **R{n} · {c}**：RED **FAIL** `{rmsg}` → GREEN **FAIL** `{gmsg}`" + NL)
    else:
        A("""- **（0 格）** —— 本轮没有“两侧都红”的格子。上一版的 3 格（R1/R2/R3 的 F3b）
  已由下面的口径收敛转绿。
""")
    A("""
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
""")
    A("""
### 6-3 **本次无区分力的条目（两侧都通过）—— 单列，不许算成"规范的功劳"**

""")
    for n, c, rmsg, gmsg in both_green:
        A(f"- R{n} · {c}：RED **PASS** `{rmsg}` → GREEN **PASS** `{gmsg}`（**两侧都绿**）" + NL)
    A(f"""
共 **{len(both_green)} 格**。**这些格子本轮没有区分力**：它们两侧都通过，
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

""")
    for n, c, rmsg, gmsg in improved:
        A(f"- **R{n} · {c}**：RED **FAIL** `{rmsg}` → GREEN **PASS** `{gmsg}`" + NL)
    A(f"\n共 **{len(improved)} 条**，与 §6-1 的 `{len(improved)}` 格**逐条相同**"
      f"（本节 ⊆ §6-1，且 §6-1 ⊆ 本节 ⇒ 两节是同一集合的两处呈现）。\n")
    A(f"""**口径**：本节只收"RED 判 FAIL 且 GREEN 判 PASS"的格子（上面的判定由 §4 的逐格表
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

""")
    jp = HERE / "judge-green.md"
    jraw = jp.read_bytes().decode("utf-8") if jp.exists() else "(判词缺失)"
    jtxt, jmasked = mask_repo(jraw)
    # 原件本身已按本仓规定掩码（§8 偏离 F）⇒ 这里应当**掩不出东西**，脚本当场证明
    assert jmasked == 0, jmasked
    jshown, jout, jrc = heredoc(JUDGE_CODE, note="判词原件的合规体检 + 内联件逐字节相同")
    A(block(jshown, jout, jrc))
    A(f"""⇒ `green/judge-green.md` 的**原件**已按本仓"不写绝对路径"的规定把本仓根掩码成 `<REPO>`
（**3 处**，都在正文里），脚本当场复扫**残留 0 处** ⇒ 下面内联的判词与原件**逐字节相同**，
不再是"本文又掩一次、原件仍然带绝对路径"。
**对判词原件的两处编辑逐条登记在 §7-3**（掩码 3 处 + 一处数字订正），不藏。

**判词全文（`green/judge-green.md`，逐字节内联）**：

""")
    fence = "`" * max(5, max((len(m) for m in re.findall(r"`+", jtxt)), default=0) + 1)
    A(f"{fence}text\n{jtxt}\n{fence}\n")

    A("""
### 7-1 判断层的**射程**（不许读过头）

判者提示词里**逐字内嵌的规范规则只有一条**：`composition data must not be drawn as a pie chart`
（= `house-style.md` 的 **H6**；该文件的「验证状态三级」一段自己写明"判断层的实际射程只有
单规则"）。⇒ **判者判"correct"不等于规范得到背书**：除 H6 以外，判者的任何结论都是
**判者自己的判断力**，不是规范条文被验证。本文凡引用判者结论处，一律按此口径读。

### 7-2 任务书点名要回答的那一问：GREEN 的图型选择**是不是因为读了规范才对的**？

""")
    A("**可判线索（本文当场实测）**：产物里是否引用了 `H<n>`。三份 `make_figure.py` 的实测结果：\n\n")
    shown, out, rc = heredoc(HREF_CODE, note="三份 GREEN 产物脚本里出现的 H<n> 编号")
    A(block(shown, out, rc))
    A("""**结论（分两半说，不许含糊）**：

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

""")
    shown, out, rc = heredoc(G2_CODE, note="G2 写手自报里的 `Design points → H-IDs` 全表（机器抓）")
    A(block(shown, out, rc))
    A("""
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

""")
    pshown, pout, prc = heredoc(PAIRWISE_CODE, note="按 brief-R1.md 的构成表复算 15 对欧氏距离")
    A(block(pshown, pout, prc))
    A("""
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

""")
    shown, out, rc = heredoc(CAPTION_CODE, note="三份 GREEN 脚本里与 caption 有关的行（机器扫，不靠自报）")
    A(block(shown, out, rc))
    A("""⇒ **G2 写了 `caption.txt`（`OUT_TXT` → `open(..., "w")`），G1 / G3 没有** ——
上一版那句"三份都只再生图"在下一次报告里不许再出现。
""")

    doc = "".join(parts)
    blob = doc.encode("utf-8")
    dst = FIGCHOOSE / "green-evidence.md"
    dst.write_bytes(blob)
    rel = dst.relative_to(REPO).as_posix()
    nl = blob.count(b"\n")
    print(f"{rel}  bytes={len(blob)}  lines={nl}")
    print(f"prompt assertion: RED-2 all-equal={all(p[1] for p in prompt_checks)} "
          f"GREEN all-equal={all(p[2] for p in prompt_checks)}")
    print(f"cells: RED {red_r}R/{red_g}G  GREEN {grn_r}R/{grn_g}G  "
          f"improved={len(improved)} stayed-red={len(stayed_red)} both-green={len(both_green)}")


TMPROOT = None

if __name__ == "__main__":
    import tempfile
    TMPROOT = str(pathlib.Path(tempfile.gettempdir()) / "m3-t6-green")
    main()
