#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`mcm-model-select`（M4）机械层判据 `MS1`–`MS6`（设计 `2026-10-04-m4-model-select-design.md` §5；
实施计划 `2026-10-04-m4-model-select.md` 的 `GC7`/`GC8` 与本 Task 4）。

用法（cwd 任意，仓内路径一律按**仓根 / skill 根**解析）：

    python .claude/skills/mcm-model-select/check-model-select.py --scope index-self
    python .claude/skills/mcm-model-select/check-model-select.py --scope class [--class evaluation]
    python .claude/skills/mcm-model-select/check-model-select.py --scope all

## 三个"面"（**名字写死；必须用 `--scope` 指名**）

* `--scope index-self` —— **索引层自洽面**：**八份类索引 ↔ `MAP.md`** 的**自洽** + 索引里的盘上素材路径。
  此刻**方法文件（六格）还没写** ⇒ `MS1` 在此面**无对象、显式 `SKIP`**（**这不是"通过"**）；
  `MS3`/`MS4` 判**已就位的 18 个骨架 / 参照**（T1–T3 产出）。**本 Task 4 的门就是这个面**。
* `--scope class` —— **类内面**：**本类**的索引条目 ↔ **本类**的实际方法文件（双向一致）+ 本类的六格 / 参照 / 骨架可跑。
  `--class` 不给时，**自动取"已写就"的类**（`references/<类>/` 下有 `.md`）。
* `--scope all` —— **全库面**：**八类合计 ↔ 全部 66 件**（Task 13 起与 Task 15 用）。

## 六条判据（设计 §5）

* `MS1` **六格齐备**：每个方法文件的六格标题（适用判据 · 标准建模步骤 · 参数与假设 · 常见坑 · 输出模板 · 代码骨架）逐个在位。
* `MS2` **引用的盘上素材路径存在**（口径见下"MS2 细则"）。
* `MS3` **每个骨架有参照记录**（`verify/<方法>.md` 在场 + 四要素齐：参照类型 · 参照来源 · 运行命令 · 两边读数）。
  ★ **它只判"记录在不在、四要素齐不齐"** —— **"参照是否真的独立"是人工判**（设计 §4.1/§4.2），本器判不了。
* `MS4` **骨架可跑** + ★★ **遮蔽守卫**（见下"MS4 细则"）。
* `MS5` **边界声明在场**（§1.1 那句 + `[官方]` 标记）。
* `MS6` **类索引的方法清单 ↔ 实际方法文件**（双向一致；`index-self` 面退化为 **索引 ↔ `MAP.md`**）。

## 空集不许判绿（GC8）

`MS1`/`MS2`/`MS3`/`MS4`/`MS5`/`MS6` **每一条都现取对象集合并打印它的"势"**；**势 = 0 判 `FAIL`**（fail-closed）。
★ **唯一的 `SKIP`**：`--scope index-self` 下的 `MS1` —— 本面按定义**不含方法文件**（设计 §5.2 规定该中间态**不以 `MS1` 为门**）。
它**打印 `SKIP`（不打印 `势=0`、不计红）**，且**不当作"通过"**。

## `MS2` 细则（设计 §5.1）

* **扫描面（★ 递归收全 · F1）**：`SKILL.md` · **`references/**/*.md`（递归：8 份顶层类索引
  + 66 份 `references/<类>/<方法>.md` 六格方法文件）** · **`assets/**/*.md`（含 `MAP.md`）** ·
  `assets/**/*.m`。★ **方法文件按设计 §9 必带 `corpus/` 语料指针** ⇒ 若只收顶层 `references/<类>.md`
  与 `.m`，那 66 份方法文件**全落在扫描面之外**，`MS2` 会**静默假绿**。
* **抽取语法**：只扫**反引号内**、且以 `corpus/` 或 `.claude/` 起始的串；**剥掉尾部 `:NNN`**。
* **判定**：**文件**用 `git cat-file -e HEAD:<path>`（**必须 `HEAD:` 前缀**，裸路径 exit 128）；
  **目录级（以 `/` 结尾）与 glob（含 `*`）一律用盘检 `test -d`**（**不许用 git** —— `.gitignore` 的目录在 git 里"不存在"、在盘上"存在"）。

## `MS4` 细则（**遮蔽守卫** · 计划 `GC8` / 设计 §5 —— 本支最值钱的一条）

`MS4` 判**两条合取** + **一条独立判据**：
1. `which('<名>','-all')` 的**首项指向【本仓的 `<名>.m`】**（不是内置 / 工具箱路径）；
2. 跑它**成功**（逐骨架 `try/catch` 的 `RUN … OK`；MATLAB `-batch` 调用抛错即该骨架失败）；
3. **独立判据**：是否存在**顶层** `@<名>` 类目录（`matlabroot/toolbox/**/@<名>` 命中**且父目录不以 `+` 开头**）。
   ★★ **"父目录不以 `+` 开头"不许省**：`…/timeseries/+tsdata/@interpolation` 在**包内**（类名 `tsdata.interpolation`），
   **不遮蔽**顶层 `interpolation.m` ⇒ 少了它会把 `interpolation` 误判成死文件（**假红**）。
   ★ **不用 `meta.class.fromName`**（实测它会把普通函数 `anova` 误报成"类"）。
★ **`-batch` 整体退出码只当"输出是否完整"的探测**（规则 1/2 以**逐名 `RUN|` + `WHICH|` 行**为准）——
  见"已知边界"第 5 条：本机 MATLAB **退出期自崩**会在**全部输出之后**置非 0 退出码，那不是骨架报错。

## 已知边界（**不声称穷尽** · 设计 §5.3）

1. **"具名文件但落在被忽略目录下"仍会假红**：规则 2 用 `git cat-file -e HEAD:<path>`，
   而 `.gitignore` 忽略目录下的**具体文件**在 git 里同样"不存在"。★ **处置（写作纪律，非判据能兜）**：
   指向被忽略目录的内容**一律用"目录级 + 盘检"或 glob 形态**，**不要写"被忽略目录下的具名文件"**。
2. **抽取语法不覆盖**：裸路径（不带反引号）· HTML 链接 · 脚注引用 —— **不在射程内**。
3. **glob 的展开结果不判**（只判**非空前缀目录**存在）。
4. ★ **`MS4` 隐含契约：骨架必须"零参可调"** —— `_matlab_run` 用 **`feval(nm)` 无参调用**逐骨架。
   ⇒ 一个**有参**的骨架（如要求输入的 `interpolation.m`）会被判"**运行未成功（输入参数的数目不足）**"，
   **那不是守卫的错，是本器对骨架接口的一条隐含要求** —— 骨架应当**自带默认参数 / 示例数据、零参即可跑完**。
   （★ 本器**不声称**能区分"骨架本身跑不通"与"骨架只是不满足零参契约"，两者都记 `运行未成功`。）
5. ★★ **MATLAB 退出期自崩（本机已知现象）—— `MS4` 的处置与残余风险**：
   * **现象**：`matlab -batch` 偶发在**跑完全部输出之后**崩溃 —— 尾行形如
     `MATLAB is exiting because of fatal error … Exit Status: 0x00000003, abort()`，整体退出码非 0；
     也见过 `matlabroot` 探针**无任何输出**地崩。**这不是骨架报错**（复核方 24 轮实测 21 PASS / 3 FAIL，
     两失效均为退出期自崩；本修复轮自证另测：`matlab -batch "…; exit(3)"` 即便**输出完整**也仍置 rc=3
     并打印 `Exit Status: 0x00000003, abort()` ⇒ 与自崩**同一签名**）。
   * **处置（本器怎么判）**：`MS4` 的规则 1/2 **只认逐名 `RUN|<名>|OK/ERR` 行 + `WHICH|` 命中**；
     **整体退出码只当"输出是否完整"的探测**（真失败会出 `RUN|..|ERR` 或**缺行**，不会被掩蔽）。
     并配 **1 次有界重试**，**且只对崩溃特征**触发：**输出里没有任何 `RUN|` 行**，**或** rc 非 0 **且**含
     `fatal error` / `abort()` / `Exit Status:` 这类签名。★ **不做"rc 非 0 即重试"**（会掩蔽真失败）；
     ★ **不做无限重试**；★ **明确排除"重跑直到绿"** —— 本仓硬口径：那会掩蔽真失败。
   * **残余风险（如实）**：崩溃若恰好**截断在某个骨架的 `RUN|` 行之前**，该骨架会**缺行** ⇒ `MS4` 判 **FAIL**（**假红**）；
     重试 1 次可降低、**不能消除**这一概率。本器**不声称**能区分"截断式崩溃"与"骨架真失败"。
★ 末行恒为 `RESULT: …`；退出码 **0 / 1**（判红 = exit 1；用法错 = exit 2）。每条判词一行，形态 `PASS|FAIL|SKIP  <id>  <读数>`。
★ `SKIP` 会在末行附带回显（如 `RESULT: PASS  [SKIP MS1]`）—— **`RESULT: PASS` 的语义不变**，只把 `SKIP` 一并标出，
  **免得裸看 `RESULT:` 的人把"有 `SKIP` 的面"读成"全过"**。
"""
import argparse
import os
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]               # …/mcm-model-select/x.py → 仓根
SKILL_DIR = ROOT / ".claude/skills/mcm-model-select"
DEF_REFERENCES = SKILL_DIR / "references"
DEF_ASSETS = SKILL_DIR / "assets/matlab"
DEF_SKILL_MD = SKILL_DIR / "SKILL.md"
DEF_MAP = SKILL_DIR / "assets/matlab/MAP.md"
DEF_VERIFY = ROOT / "tests/skills/model-select/verify"

CLASSES = ["evaluation", "prediction", "optimization", "mechanism",
           "simulation", "statistics", "network", "ml"]

BOUNDARY = "本 skill 给出候选模型与判据；最终选择与结论由队员负责"
OFFICIAL_MARK = "[官方]"
SIX = ["适用判据", "标准建模步骤", "参数与假设", "常见坑", "输出模板", "代码骨架"]
FOUR = ["参照类型", "参照来源", "运行命令", "两边读数"]

HEAD_RE = re.compile(r"^\s{0,3}#{2,6}\s*(.+?)\s*$")
PATH_RE = re.compile(r"`([^`]+)`")
LINENO_RE = re.compile(r":\d+$")
COLS = ["中文名", "ASCII 文件名", "六格文件路径"]


# ---------------------------------------------------------------- 基础 IO / 解析
def read_text(path):
    """读一个文本文件；读不出 ⇒ `None`（**fail-closed 的入口**）。"""
    try:
        return pathlib.Path(path).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _norm(cell):
    return cell.strip().strip("`").strip()


def _rel_label(path, base):
    """给 `MS2` 的命中项一个**可读标签**（相对 skill 根的 posix 路径）；不在其下则退回文件名。"""
    try:
        return pathlib.Path(path).relative_to(base).as_posix()
    except ValueError:
        return pathlib.Path(path).name


def _is_sep(cells):
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells)


def _tables(text):
    """把一份 markdown 切成若干表；每表 = `[[cell,...], ...]`（去掉分隔行）。"""
    out, cur = [], []
    for ln in text.splitlines():
        if ln.lstrip().startswith("|"):
            cur.append(ln)
        else:
            if cur:
                out.append(cur)
                cur = []
    if cur:
        out.append(cur)
    res = []
    for b in out:
        rows = [[_norm(c) for c in l.strip().strip("|").split("|")] for l in b]
        rows = [r for r in rows if not _is_sep(r)]
        if rows:
            res.append(rows)
    return res


def _three_col(rows):
    """若某表的表头三列 == `COLS` ⇒ 返回其数据行（`[(中文名,ascii,path)]`），否则 `None`。"""
    if rows and rows[0][:3] == COLS:
        return [tuple(r[:3]) for r in rows[1:] if len(r) >= 3]
    return None


def parse_map(text):
    """`MAP.md` ⇒ `{类: [(中文名, ascii, path)]}`（按 `## <类>（N）` 分节）。"""
    out, cur = {}, None
    for ln in text.splitlines():
        m = re.match(r"^##\s+([a-z_]+)\s*[（(]?", ln)
        if m and m.group(1) in CLASSES:
            cur = m.group(1)
            out.setdefault(cur, [])
            continue
        if cur is not None and ln.lstrip().startswith("|"):
            cells = [_norm(c) for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 3 and not _is_sep(cells) and cells[:3] != COLS and cells[0]:
                out[cur].append(tuple(cells[:3]))
    return out


def parse_index(text):
    """一份类索引 ⇒ `[(中文名, ascii, path)]`（其"三列方法清单"表的数据行），找不到 ⇒ `[]`。"""
    for rows in _tables(text):
        got = _three_col(rows)
        if got is not None:
            return got
    return []


def _headings(text):
    hs = []
    for ln in text.splitlines():
        m = HEAD_RE.match(ln)
        if m:
            hs.append(m.group(1))
    return hs


def _has_keys(text, keys):
    """返回**命中不了的 key** 列表（keys 都出现在某个标题里 ⇒ 返回空）。"""
    hs = _headings(text)
    return [k for k in keys if not any(k in h for h in hs)]


# ---------------------------------------------------------------- MS1
def ms1(method_files):
    """六格齐备。`method_files` = `[(类, path)]`。"""
    if not method_files:
        return "FAIL", "势=0：本面无方法文件（`references/<类>/*.md`）⇒ 无可检对象"
    bad = []
    for _cls, p in method_files:
        txt = read_text(p)
        if txt is None:
            bad.append(f"{p.name}：读不出")
            continue
        miss = _has_keys(txt, SIX)
        if miss:
            bad.append(f"{p.name}：缺 {'/'.join(miss)}")
    detail = f"势={len(method_files)}（方法文件）· 六格不全 {len(bad)} 份"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- MS2
def extract_paths(text):
    """只扫反引号内、以 `corpus/` 或 `.claude/` 起始的串；剥掉尾部 `:NNN`。"""
    out = []
    for m in PATH_RE.finditer(text):
        s = m.group(1).strip()
        if s.startswith("corpus/") or s.startswith(".claude/"):
            out.append(LINENO_RE.sub("", s))
    return out


def _git_has(path):
    r = subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", "HEAD:" + path],
                       capture_output=True)
    return r.returncode == 0


def ms2(texts):
    """引用的盘上素材路径存在。`texts` = `[(标签, 文本)]`。"""
    seen = {}
    for label, txt in texts:
        if txt is None:
            continue
        for p in extract_paths(txt):
            seen.setdefault(p, label)
    if not seen:
        return "FAIL", "势=0：抽取面上没有以 `corpus/` 或 `.claude/` 起始的反引号路径 ⇒ 无可检对象"
    bad = []
    for p, label in sorted(seen.items()):
        if p.endswith("/"):
            if not (ROOT / p.rstrip("/")).is_dir():
                bad.append(f"目录不存在〔盘检〕{p}  (于 {label})")
        elif "*" in p:
            pre = p.split("*", 1)[0]
            d = pre.rsplit("/", 1)[0] if "/" in pre else ""
            if not d or not (ROOT / d).is_dir():
                bad.append(f"glob 前缀目录不存在〔盘检〕{p}  (于 {label})")
        else:
            if not _git_has(p):
                bad.append(f"文件不在 HEAD〔git cat-file〕{p}  (于 {label})")
    detail = f"势={len(seen)}（盘上素材路径）· 不存在 {len(bad)} 条"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- MS3
def ms3(skeletons, verify_dir):
    """每个骨架有参照记录（四要素齐）。★ 只判记录在场 + 四要素齐；**独立性是人工判**。"""
    if not skeletons:
        return "FAIL", "势=0：本面无骨架 ⇒ 无可检对象"
    bad = []
    for _cls, name, _mp in skeletons:
        rec = pathlib.Path(verify_dir) / (name + ".md")
        txt = read_text(rec)
        if txt is None:
            bad.append(f"{name}：缺参照记录 {rec.name}")
            continue
        miss = _has_keys(txt, FOUR)
        if miss:
            bad.append(f"{name}：四要素缺 {'/'.join(miss)}")
    detail = (f"势={len(skeletons)}（骨架）· 参照记录/四要素不全 {len(bad)} 份"
              "  ★ 独立性（不同源）本器判不了，归人工/独立复核（设计 §4.1/§4.2）")
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- MS4
# ★ MATLAB **退出期自崩**（本机已知现象，见"已知边界"第 5 条）：`-batch` 偶发在**跑完全部输出之后**
#   崩溃（尾行 `MATLAB is exiting because of fatal error … Exit Status: 0x00000003, abort()`）、整体退出码非 0。
#   这**不是**骨架报错 ⇒ `MS4` **只认逐名 `RUN|`/`WHICH|` 行**，退出码只当"输出是否完整"的探测，并配**有界重试**。
CRASH_SIGNS = ("fatal error", "abort()", "Exit Status:", "MATLAB is exiting")


def _run_matlab(argv, timeout):
    """跑一条 `matlab` 命令；返回 `(rc, stdout, stderr)`。**起不来**（无 matlab / 超时）⇒ `rc=None`。"""
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as e:
        return None, "", f"{type(e).__name__}: {e}"
    return r.returncode, r.stdout or "", r.stderr or ""


def _crash_signature(stdout, stderr):
    """命中 **MATLAB 退出期自崩**的崩溃特征串；无 ⇒ `""`。
    ★ **判"是否重试"只看崩溃特征**，**绝不是"rc 非 0 即重试"** —— 后者会掩蔽真失败。"""
    blob = (stdout or "") + "\n" + (stderr or "")
    return next((s for s in CRASH_SIGNS if s in blob), "")


def _parse_matlabroot(stdout):
    """从 `disp(matlabroot)` 的输出里取第一个像路径的行。"""
    for ln in (stdout or "").splitlines():
        s = ln.strip()
        if s and (re.match(r"^[A-Za-z]:[\\/]", s) or s.startswith("/")):
            return s
    return None


def _matlabroot():
    """取 `matlabroot`。★ **有界重试 1 次**：**仅当**上一跑落入"崩溃特征"（**无任何输出**，或 rc 非 0 且含崩溃签名）。
    正常路径（rc=0，或**输出完整、只是退出码非 0**）**不重试**。"""
    for _attempt in (1, 2):
        rc, out, err = _run_matlab(["matlab", "-batch", "disp(matlabroot)"], 300)
        if rc is None:
            return None
        root = _parse_matlabroot(out)
        if root:
            return root
        if not (_crash_signature(out, err) or not out.strip()):
            return None                     # 非崩溃特征 ⇒ 不重试
    return None


def _top_class_dir_hits(matlabroot, names):
    """`name ⇒ [类目录…]`：**顶层** `@<名>` 类目录（父目录不以 `+` 开头）。"""
    hits = {}
    tb = os.path.join(matlabroot, "toolbox")
    for dpath, dnames, _ in os.walk(tb):
        for dn in dnames:
            if dn.startswith("@") and dn[1:] in names:
                if not os.path.basename(dpath).startswith("+"):
                    hits.setdefault(dn[1:], []).append(os.path.join(dpath, dn))
    return hits


def _parse_run(stdout):
    """解析逐名 `WHICH|`/`RUN|` 行 ⇒ `{name: {which, ok, msg}}`。"""
    res = {}
    for ln in (stdout or "").splitlines():
        parts = ln.strip().split("|")
        if not parts:
            continue
        if parts[0] == "WHICH" and len(parts) >= 3:
            res.setdefault(parts[1], {})["which"] = parts[2]
        elif parts[0] == "RUN" and len(parts) >= 3:
            d = res.setdefault(parts[1], {})
            d["ok"] = parts[2] == "OK"
            d["msg"] = parts[3] if len(parts) > 3 else ""
    return res


def _matlab_run(skeletons):
    """一条 `matlab -batch` 跑全部目标骨架：逐名打印 `WHICH|` 与 `RUN|`。
    ★ **判定以逐名 `RUN|`/`WHICH|` 行为准**；整体退出码只当"输出是否完整"的探测（真失败会出 `RUN|..|ERR` 或**缺行**）。
    ★ **有界重试 1 次**：**仅当**输出里**没有任何 `RUN|` 行**，**或** rc 非 0 **且**含崩溃签名（本机退出期自崩）。
      ★ **不**把"rc 非 0"当重试条件；★ **不**做无限重试。
    返回 `(res, note)`：`res=None` ⇒ MATLAB 起不来（fail-closed）；`note` 为回显（重试 / 崩溃说明）。"""
    dirs = sorted({str(pathlib.Path(mp).parent) for _c, _n, mp in skeletons})
    names = [n for _c, n, _mp in skeletons]
    addp = "".join("addpath('%s');" % d.replace("\\", "/") for d in dirs)
    lit = "{" + ",".join("'%s'" % n for n in names) + "}"
    script = (f"{addp} ns={lit};"
              "for k=1:numel(ns); nm=ns{k};"
              " w=which(nm,'-all'); if ischar(w); w={w}; end;"
              " fprintf('WHICH|%s|%s\\n', nm, w{1});"
              " try; feval(nm); fprintf('RUN|%s|OK\\n', nm);"
              " catch e; fprintf('RUN|%s|ERR|%s\\n', nm, e.message); end;"
              " end")
    res, note = {}, ""
    n_run, rc, crash, retried = 0, 0, "", False
    for attempt in (1, 2):
        rc, out, err = _run_matlab(["matlab", "-batch", script], 1800)
        if rc is None:
            return None, f"MATLAB 起不来：{err}"
        res = _parse_run(out)
        n_run = sum(1 for ln in out.splitlines() if ln.strip().startswith("RUN|"))
        crash = _crash_signature(out, err)
        # 崩溃特征 = 没有任何 `RUN|` 行，或（rc 非 0 且含崩溃签名）⇒ 至多重试 1 次
        if not (n_run == 0 or (rc != 0 and crash)):
            break                                    # 无崩溃特征 ⇒ 采用本轮结果
        if attempt == 1:
            retried = True
            continue                                 # 命中崩溃特征 ⇒ 至多重试 1 次
        break                                        # 重试后仍命中 ⇒ 采用本轮结果（交判词处理）
    # ★ 诚实回显：区分"输出完整但退出码非 0"与"输出不完整（缺行 / 无输出）"
    tag = "，已重试 1 次" if retried else ""
    if n_run >= len(names):
        if rc != 0:
            note = (f"（rc={rc} 非 0" + (f"·含崩溃签名「{crash}」" if crash else "")
                    + f"，但逐名 RUN| 行齐全（{n_run}/{len(names)}）⇒ 按逐名读数判{tag}）")
    else:
        note = (f"（输出不完整：RUN| 行 {n_run}/{len(names)}"
                + (f"·崩溃签名「{crash}」" if crash else "")
                + (f"·rc={rc}" if rc != 0 else "") + tag + "）")
    return res, note


def ms4(skeletons):
    """骨架可跑 + 遮蔽守卫（两条合取 + 一条独立判据）。"""
    if not skeletons:
        return "FAIL", "势=0：本面无骨架 ⇒ 无可检对象"
    mr = _matlabroot()
    if not mr:
        return "FAIL", "MATLAB 不可用（`matlab -batch disp(matlabroot)` 取不到）⇒ 无法判骨架可跑（fail-closed）"
    names = {n for _c, n, _mp in skeletons}
    top_hits = _top_class_dir_hits(mr, names)
    got, note = _matlab_run(skeletons)
    if got is None:
        return "FAIL", f"骨架运行失败：{note}（fail-closed）"
    bad = []
    for _cls, name, mp in skeletons:
        real = os.path.normcase(os.path.normpath(str(pathlib.Path(mp).resolve())))
        w = (got.get(name) or {}).get("which", "")
        ok_run = (got.get(name) or {}).get("ok", False)
        if not w or os.path.normcase(os.path.normpath(w)) != real:
            bad.append(f"{name}：which 首项 {w or '（无）'} ≠ 本仓文件")
        if not ok_run:
            bad.append(f"{name}：运行未成功（{((got.get(name) or {}).get('msg') or '')[:40]}）")
        if name in top_hits:
            bad.append(f"{name}：撞【顶层】@类目录 {top_hits[name][0]}")
    detail = f"势={len(skeletons)}（骨架）· matlabroot={mr} · 不合 {len(bad)} 项"
    if note:
        detail += " · " + note
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- MS5
def ms5(skill_md_text):
    """边界声明在场（§1.1 那句 + `[官方]` 标记）。"""
    if skill_md_text is None:
        return "FAIL", "势=0：`SKILL.md` 读不出 ⇒ 无可检对象（fail-closed）"
    norm = re.sub(r"\s+", " ", re.sub(r"[*>`]", "", skill_md_text))
    bad = []
    if BOUNDARY not in norm:
        bad.append("缺 §1.1 边界句「%s」" % BOUNDARY)
    if OFFICIAL_MARK not in skill_md_text:
        bad.append("缺 `[官方]` 标记")
    detail = "势=1（`SKILL.md`）· 边界声明 %s" % ("在位" if not bad else "缺")
    if bad:
        detail += "  <<< " + " ; ".join(bad)
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- MS6
def _rowwise_mismatch(idx, mp):
    """**逐行（按位置）**比对两表的三元组；一致 ⇒ `None`，否则一句读数。
    ★ 位置/顺序也算不一致：同一方法的「中文名 / ASCII 名 / 路径」三元组必须在两表里**同行**（设计 §2.1）。"""
    n = min(len(idx), len(mp))
    off = [i for i in range(n) if idx[i] != mp[i]]
    if not off and len(idx) == len(mp):
        return None
    parts = []
    if off:
        i = off[0]
        parts.append(f"第 {i + 1} 行不同（索引 {idx[i]} ↔ MAP {mp[i]}）· 位置不符 {len(off)} 处")
    if len(idx) != len(mp):
        di = {x for x in idx if x not in mp}
        dm = {x for x in mp if x not in idx}
        parts.append(f"行数 {len(idx)}/{len(mp)}（索引独有 {len(di)} · MAP 独有 {len(dm)}）")
    return "；".join(parts)


def ms6(map_rows, index_rows, references, scope, target):
    """类索引 ↔ `MAP.md`（自洽面 · **逐行**）+（`class`/`all`）索引 ↔ 实际方法文件（类内面）。"""
    judged = [c for c in CLASSES if c in index_rows]
    if not judged:
        return "FAIL", "势=0：一份类索引都读不出 ⇒ 无可检对象"
    bad = []
    for c in judged:
        idx = index_rows[c]
        mp = map_rows.get(c, [])
        mis = _rowwise_mismatch(idx, mp)                           # 自洽面（逐行 · 全类）
        if mis:
            bad.append(f"{c}：索引↔MAP 不一致（{mis}）")
        if scope != "index-self" and c in target:                  # 类内面（**只对本类**，双向）
            listed = {p for _a, _b, p in idx}
            present = {f"references/{c}/{f.name}" for f in references.joinpath(c).glob("*.md")} \
                if references.joinpath(c).is_dir() else set()
            miss = sorted(listed - present)
            extra = sorted(present - listed)
            if miss:
                bad.append(f"{c}：索引列了但文件不在 {len(miss)} 个（如 {miss[0]}）")
            if extra:
                bad.append(f"{c}：文件在但索引没列 {len(extra)} 个（如 {extra[0]}）")
    nrows = sum(len(index_rows[c]) for c in judged)
    detail = f"势={len(judged)}（类索引，共 {nrows} 行）· 不一致 {len(bad)} 处"
    if bad:
        detail += "  <<< " + " ; ".join(bad[:6]) + (" …" if len(bad) > 6 else "")
    return ("PASS" if not bad else "FAIL"), detail


# ---------------------------------------------------------------- main
def _target_classes(scope, class_arg, references):
    if scope == "all":
        return list(CLASSES)
    if scope == "class":
        if class_arg:
            return [class_arg]
        return [c for c in CLASSES if references.joinpath(c).is_dir()
                and any(references.joinpath(c).glob("*.md"))]
    return [c for c in CLASSES if references.joinpath(c + ".md").exists() or references.joinpath(c).is_dir()]


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="`mcm-model-select`（M4）机械层判据 MS1–MS6。"
                    "三个面用 --scope 指名：index-self（索引↔MAP 自洽）· class（类内）· all（全库）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python .claude/skills/mcm-model-select/check-model-select.py --scope index-self\n"
               "  python .claude/skills/mcm-model-select/check-model-select.py --scope class --class evaluation\n"
               "  python .claude/skills/mcm-model-select/check-model-select.py --scope all\n")
    ap.add_argument("--scope", required=True, choices=["index-self", "class", "all"],
                    help="面：index-self = 索引↔MAP 自洽（Task 4 的门）· class = 本类索引↔本类文件（Task 5–12）· all = 全库（Task 13 起 / Task 15）")
    ap.add_argument("--class", dest="class_name", default=None, choices=CLASSES,
                    help="--scope class 时指定一个类；不给则自动取「已写就」的类")
    ap.add_argument("--skill-dir", default=None, help="skill 根（默认仓内；变异探针可指到副本）")
    ap.add_argument("--verify-dir", default=None, help="参照记录目录（默认 tests/skills/model-select/verify）")
    a = ap.parse_args(argv)

    skill_dir = pathlib.Path(a.skill_dir) if a.skill_dir else SKILL_DIR
    references = skill_dir / "references"
    assets = skill_dir / "assets/matlab"
    skill_md = skill_dir / "SKILL.md"
    map_md = assets / "MAP.md"
    verify_dir = pathlib.Path(a.verify_dir) if a.verify_dir else DEF_VERIFY

    print(f"check-model-select.py · scope={a.scope}" + (f" · class={a.class_name}" if a.class_name else ""))
    print(f"skill-dir = {skill_dir}")

    tclasses = _target_classes(a.scope, a.class_name, references)

    # 对象集合（每条现取 + 打印势）
    method_files = []
    skeletons = []
    for c in tclasses:
        d = references.joinpath(c)
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                method_files.append((c, f))
        sa = assets.joinpath(c)
        if sa.is_dir():
            for f in sorted(sa.glob("*.m")):
                skeletons.append((c, f.stem, f))

    index_rows, scan_texts = {}, []
    smd = read_text(skill_md)
    if smd is not None:
        scan_texts.append(("SKILL.md", smd))

    # ★ F1：扫描面**递归收全** —— 否则 `MS2` 对方法文件（六格）与 `assets/**/*.md` 静默假绿：
    #   · `SKILL.md`；
    #   · `references/**/*.md`（递归：8 份顶层类索引 + 66 份 `references/<类>/<方法>.md`）；
    #   · `assets/**/*.md`（含 `assets/matlab/MAP.md`）；
    #   · `assets/**/*.m`（骨架）。
    assets_root = skill_dir / "assets"
    for f in sorted(references.rglob("*.md")):
        txt = read_text(f)
        if txt is not None:
            scan_texts.append((_rel_label(f, skill_dir), txt))
    for f in sorted(assets_root.rglob("*.md")):
        txt = read_text(f)
        if txt is not None:
            scan_texts.append((_rel_label(f, skill_dir), txt))
    for f in sorted(assets_root.rglob("*.m")):
        txt = read_text(f)
        if txt is not None:
            scan_texts.append((_rel_label(f, skill_dir), txt))

    # 8 份顶层类索引另行解析（`MS6` 用）；数据来源与上面的扫描面同源、互不替代
    for c in CLASSES:
        f = references.joinpath(c + ".md")
        txt = read_text(f)
        if txt is not None:
            index_rows[c] = parse_index(txt)
    map_txt = read_text(map_md)
    map_rows = parse_map(map_txt) if map_txt else {}

    # 判据
    rows = []
    if a.scope == "index-self":
        rows.append(("MS1", ("SKIP", "本面（index-self）按定义不含方法文件（还没写）；六格在 --scope class/all 面判 —— 这不是「通过」")))
    else:
        rows.append(("MS1", ms1(method_files)))
    rows.append(("MS2", ms2(scan_texts)))
    rows.append(("MS3", ms3(skeletons, verify_dir)))
    rows.append(("MS4", ms4(skeletons)))
    rows.append(("MS5", ms5(smd)))
    rows.append(("MS6", ms6(map_rows, index_rows, references, a.scope, tclasses)))

    for rid, (st, detail) in rows:
        print(f"{st:<4}  {rid}  {detail}")

    fails = [rid for rid, (st, _d) in rows if st == "FAIL"]
    skips = [rid for rid, (st, _d) in rows if st == "SKIP"]
    print("-" * 78)
    print(f"判据 {len(rows)} 条 · 红 {len(fails)} 条" + (f" · SKIP {','.join(skips)}" if skips else ""))
    # ★ F4.2：`RESULT: PASS` 语义不变；`SKIP` 附在其后回显，免得裸看 `RESULT:` 的人读成"全过"。
    if not fails:
        print("RESULT: PASS" + (f"  [SKIP {','.join(skips)}]" if skips else ""))
    else:
        print(f"RESULT: FAIL（{','.join(fails)}）")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
