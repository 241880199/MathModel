# -*- coding: utf-8 -*-
"""把同目录的 `figure-style-baseline.txt` 里登记的每条命令**逐条重跑**，用当场输出就地
替换旧输出。散文（含 §9 差异表）不在此脚本里改。

**本脚本与它生成的证据同目录入库**（照本仓规矩：证据在册，造它的脚本不许留在 gitignored 的
`.superpowers/` 里 —— `.superpowers/sdd/.gitignore` 是 `*`，那里的 `m3-t1-mk-baseline.py`
从来没入过库，而且它已过期：只能重放出修复轮之前那一版，见下）。

## 为什么是"重放"而不是"重生成"

旧任务书与旧报告里点名的生成器 `.superpowers/sdd/m3-t1-mk-baseline.py`（**其实从未入库** ——
那个目录被它自己的 `.gitignore`（`*`）全挡掉）只能重放出**修复轮之前**那一版
（实测：它写出 594 行，而在库件是 774 行；§1/§2/§4/§5/§8.5 全不同）⇒ 那一版生成器
**已不覆盖在库件**（在库件是修复轮里手装出来的）。本脚本改成**重放**：把在库件当成
「命令 + 散文」的清单 —— 命令原地重跑、散文原样保留。好处是**每个数都来自当场跑过的
命令**，且不必重抄散文；它自己**入库**（同目录），所以复核员拿得到造证据的那支笔。

## 用法（cwd = 仓根）

    python tests/skills/figure-choose/gen-figure-style-baseline.py 1    # 提交前：重放 §2–§8.4
    python tests/skills/figure-choose/gen-figure-style-baseline.py 2    # 提交后：重放 §8.5

## 显示格式（按旧块**自己**的形态推断，不另立一套）

| 旧块首行 | 模式 | 新块内容 |
| :--- | :--- | :--- |
| `[stdout 末行] ...` | lastline | stdout 的末行 |
| `[stdout 中匹配 /re/ 的行]` | filter | stdout 里匹配 `re` 的行 |
| `[stdout] ...` | split | `[stdout]`（空则 `[stdout] （空）`）+ 逐行；stderr 非空再加 `[stderr] ...` |
| `（空）` | empty | 空则 `（空）`，否则逐行如实 |
| 其它 | normal | stdout+stderr 逐字 |

## 三处 `$TEMP` 资产的补货（文件里只以散文/注释提到，不是可跑的命令）

1. `$TEMP/m3t1/fake.pdf`（§3.5 的坏 PDF）—— 本脚本预置 `b"not a pdf\\n"`；
2. `$TEMP/m3t1/instrument.py`（§7 的仪器探针）—— 从文件里紧跟其后的「命令体（逐字，
   cwd = 仓根）：」块**逐字**取出后落盘；
3. `$TEMP/m3t1/p1/figure-choose/check-figure-style.py`（§5 的 P1 变异体）—— 在 §5 的
   `cp -r` 那一块之后，用**与驱动器 P1 逐字相同**的那次字面替换现做一份。

写入一律 `write_bytes`（全仓禁用 `write_text`：Windows 上会写 CRLF）。
"""
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]   # tests/skills/figure-choose → 仓根
EV = ROOT / "tests/skills/figure-choose/figure-style-baseline.txt"
CHK = ROOT / "tests/skills/figure-choose/check-figure-style.py"
PHASE = sys.argv[1] if len(sys.argv) > 1 else "1"
if PHASE not in ("1", "2"):
    sys.exit("用法：python tests/skills/figure-choose/gen-figure-style-baseline.py [1|2]（cwd = 仓根）")

# ------------------------------------------------------------------ $TEMP 资产
TMP = pathlib.Path(tempfile.mkdtemp(prefix="m3t1r-"))
M3T1 = TMP / "m3t1"
P1DIR = M3T1 / "p1" / "figure-choose"
for d in (M3T1, P1DIR / "fixtures"):
    d.mkdir(parents=True, exist_ok=True)
(M3T1 / "fake.pdf").write_bytes(b"not a pdf\n")
TEMP_S = str(TMP).replace("\\", "/")
PYDIR = str(pathlib.Path(sys.executable).parent)


def scrub(s):
    """本文件对捕获输出唯一的加工：仓根 → 相对、`$TEMP` → 占位符、解释器前缀 → 去掉。

    三种写法（原样 / repr 里的双反斜杠 / 正斜杠）都要认；**带分隔符的形态连分隔符一起**换，
    否则会留下一个秃 `\\` 或 `/`。
    """
    for raw, repl in ((str(TMP), "$TEMP"), (str(ROOT), "."), (PYDIR, ""), (sys.executable, "python")):
        bases = (raw, raw.replace("\\", "\\\\"), raw.replace("\\", "/"))
        for b in bases:
            for sep in ("\\\\", "\\", "/"):
                s = s.replace(b + sep, repl + sep)
        for b in bases:
            s = s.replace(b, repl)
    return s


def run_cmd(cmd_text):
    """跑一行登记的命令，返回 (rc, stdout, stderr)。只支持本文件出现过的那几种：
    `python ...` / `git ...` / `cp -r a b` / `... > file`（重定向）。"""
    s = cmd_text.replace("$TEMP", TEMP_S).replace("$TMP", TEMP_S)
    redir = None
    m = re.match(r"^(.*?)\s+>\s+(\S+)$", s)
    if m:
        s, redir = m.group(1).strip(), m.group(2).strip().strip('"')
    argv = shlex.split(s, posix=True)
    if argv and argv[0] == "python":
        argv[0] = sys.executable
    if argv and argv[0] == "cp" and argv[1] == "-r":
        src, dst = pathlib.Path(argv[2]), pathlib.Path(argv[3])
        if dst.is_dir():                       # 与 `cp -r` 同义：拷**进**目录而不是覆盖它
            dst = dst / src.name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return 0, "", ""
    p = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if redir:
        pathlib.Path(redir).write_bytes((p.stdout or "").encode("utf-8"))
        return p.returncode, "", p.stderr
    return p.returncode, p.stdout, p.stderr


# ------------------------------------------------------------------ 块解析 / 渲染
CMD = re.compile(r"^\$ ")
EXIT = re.compile(r"^\[exit=(\d+)\]$")


def mode_of(first):
    if first.startswith("[stdout 末行]"):
        return "lastline"
    if first.startswith("[stdout 中匹配"):
        return "filter"
    if first.startswith("[stdout]"):
        return "split"
    if first.strip() == "（空）":
        return "empty"
    return "normal"


def render(rc, out, err, mode, old_first):
    out, err = scrub(out or ""), scrub(err or "")
    ol = out.rstrip("\n").split("\n") if out.strip() else []
    el = err.rstrip("\n").split("\n") if err.strip() else []
    if mode == "lastline":
        body = ["[stdout 末行] " + (ol[-1] if ol else "（空）")]
    elif mode == "filter":
        m = re.search(r"中匹配 /(.*)/ 的行", old_first)
        rx = m.group(1) if m else ".^"
        body = ["[stdout 中匹配 /%s/ 的行]" % rx] + [l for l in out.split("\n") if re.search(rx, l)]
    elif mode == "split":
        body = (["[stdout]"] + ol) if ol else ["[stdout] （空）"]
        if el:
            body += ["[stderr] " + el[0]] + el[1:]
    elif mode == "empty":
        body = ["（空）"] if not out.strip() else ol
    else:
        body = (out + err).rstrip("\n").split("\n") if (out + err).strip() else []
    return body + ["[exit=%d]" % rc]


def code_block(text, marker, stop):
    """取 `marker` 之后、`stop` 之前的那段**逐字**代码（去掉首尾空行）。"""
    i = text.index(marker) + len(marker)
    j = text.index(stop, i)
    seg = text[i:j]
    lines = seg.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise AssertionError("空代码块：%r" % marker)
    return "\n".join(lines)


text = EV.read_bytes().decode("utf-8")
INSTRUMENT = code_block(text, "命令体（逐字，cwd = 仓根）：", "\n\n⇒ A 与 B 的差")
BYTECHECK = code_block(text, "命令体：\n", "\n$ python -c ")
(M3T1 / "instrument.py").write_bytes((INSTRUMENT + "\n").encode("utf-8"))

P1_OLD = "    res = check(p, cap, a.textwidth_in, a.dpi)"
P1_NEW = ('    if p.name == "bad-f2-five-colors.pdf":\n'
          "        sys.exit(EXIT_FAIL_CLOSED)  # 探针：只在期望 FAIL 的那一行 fail-closed\n"
          + P1_OLD)

lines = text.split("\n")
out, i, section, stats = [], 0, None, {"blocks": 0, "skipped": 0}
while i < len(lines):
    ln = lines[i]
    ms = re.match(r"^§([\d.]+)", ln)
    if ms:
        section = ms.group(1)
    want = (section is not None) and ((PHASE == "1" and section != "8.5") or
                                     (PHASE == "2" and section == "8.5"))
    if ln.startswith("$ ") and want:
        cmds, i = [], i
        while i < len(lines) and lines[i].startswith("$ "):
            cmds.append(lines[i][2:])
            out.append(lines[i])
            i += 1
        disp, j = [], i
        while j < len(lines) and not EXIT.match(lines[j]):
            disp.append(lines[j])
            j += 1
        rc_last, outs = 0, []
        for c in cmds:
            body = re.sub(r"\s{2,}#\s.*$", "", c).strip()
            if not body or body.startswith("#"):
                continue
            if "<上面的命令体>" in body:
                argv = [sys.executable, "-c", BYTECHECK]
                p = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True,
                                   encoding="utf-8", errors="replace")
                rc_last, outs = p.returncode, [(p.stdout or "", p.stderr or "")]
                continue
            if "instrument.py" in body:
                (M3T1 / "instrument.py").write_bytes((INSTRUMENT + "\n").encode("utf-8"))
            rc_last, so, se = run_cmd(body)
            outs.append((so, se))
            if "cp -r tests/skills/figure-choose/fixtures" in body:
                src = CHK.read_bytes().decode("utf-8")
                assert src.count(P1_OLD) == 1, "P1 字面替换命中数 ≠ 1"
                (P1DIR / "check-figure-style.py").write_bytes(
                    src.replace(P1_OLD, P1_NEW).encode("utf-8"))
        so = "".join(o for o, _ in outs)
        se = "".join(e for _, e in outs)
        mode = mode_of(disp[0] if disp else "")
        block = render(rc_last, so, se, mode, disp[0] if disp else "")
        out.extend(block)
        i = j + 1
        stats["blocks"] += 1
        continue
    out.append(ln)
    i += 1

if PHASE == "2":
    # §8.5 的「逐个比对」表不是 `$` 块（是脚本现算的表）⇒ 单独重算
    m = re.search(r"^\$ git hash-object (.+?)\s+# 工作树$", text, re.M)
    files = shlex.split(m.group(1))
    rows, all_eq = [], True
    for f in files:
        w = subprocess.run(["git", "hash-object", f], cwd=str(ROOT),
                           capture_output=True, text=True).stdout.strip()
        h = subprocess.run(["git", "rev-parse", "HEAD:" + f], cwd=str(ROOT),
                           capture_output=True, text=True).stdout.strip()
        eq = w == h
        all_eq = all_eq and eq
        rows.append("  %-62s 工作树=%s  HEAD=%s  %s"
                    % (f, w[:12], h[:12], "相等" if eq else "不等 <<<"))
    k = out.index("逐个比对：")
    l = next(n for n in range(k, len(out)) if out[n].startswith("  全部相等"))
    out[k + 1:l + 1] = rows + ["  全部相等: %s  （%d/%d）"
                               % (all_eq, len(files), len(files))]
    print("phase 2：逐个比对表 %d 行 · 全部相等=%s" % (len(files), all_eq))

new = "\n".join(out)
EV.write_bytes(new.encode("utf-8"))
print("phase %s：重放 %d 块 → %s  %d bytes  %d lines"
      % (PHASE, stats["blocks"], EV, len(EV.read_bytes()), new.count("\n")))
