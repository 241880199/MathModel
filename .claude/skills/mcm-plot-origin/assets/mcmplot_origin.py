# -*- coding: utf-8 -*-
"""mcmplot_origin —— MCM 论文图的 Origin 薄封装（样式 + 导出）。

**只回答一件事**：把"这张图该怎么画"落到 Origin 上，并让产物过得了既有判据
（`check-figure-style.py`）。**不选图型**（那是 `mcm-figure-choose`）、**不出合规判词**。

## 与规范的接口（签名照设计 §6，逐字）

- `apply_style(page)`：色序（**不动底色**；值从 `mcm-style.json` 读）。
- `figsize_for(textwidth_in)`：正文栏宽（英寸）→ 图宽（英寸），乘数从表里取。
- `save(page, path, dpi=300, theme="Times New Roman Font")`：导出（**宽度钉死** +
  **主题在导出那一刻施加**）；返回一个 dict，含**实测的"实际导出宽"**以自证。

★ **本文件运行时读那张表**（`.claude/skills/mcm-figure-choose/assets/mcm-style.json`）——
**唯一一份样式来源**：本文件**零规范字面量**（除"怎么调 API"本身），故**没有派生副本可漂**。
规范正文只在 `.claude/skills/mcm-figure-choose/references/house-style.md`，本文件**不重述**。

## 运行前置（**环境事实**，不是规范）

- `sys.path` 上要能找到 `originpro`（本机装在 `build/m3-origin-probe/site`）；
- 本机须**已安装且已授权** OriginPro（见 `references/workflow.md` 的前置条件一节）。

## 已知缺口（不许藏；**不声称穷尽**）

- **底色**：Origin **默认导出即白底** ⇒ `apply_style()` **不设**底色，白底由**产物**证
  （判据 `F4`）。★ 这只说明"不必设"，**不是**"设了也没用" —— 改底色**分语法**：
  **Python 属性赋值那条路是哑的**（`layer.color = …` / `page.color = …` **不抛错**，
  即对象接受任意动态属性，**却改不动产物** —— 这一步在**像素层**成立：PNG 里带时间戳块
  （`tIME`），**不许**拿"逐字节同基线"当"底色没变"的判据；连**读**它都抛 `AttributeError`）；
  **LabTalk 那条路有效**（`layer.lt_exec("layer.color=…")` 真把整层底色改掉，实测由白变橙）。
  ⇒ **不**把"Python 路无效"推广成"改底色一律无效"。
- **"设上了"只能由产物证明**：给**不存在的主题名**，两条施加路径**都静默成功**
  （`exec_ok=True`、产物毫无变化）；`xb.font$=` **静默返 True 却什么都没做**。
  ⇒ 本文件凡"设上了"的断言，**要么由产物证、要么不给**。
- **字体族：`F6` 落哪一态依产物而定**（原写"只能 `N/A`"，**2026-10-02 实测订正**）：`check-figure-style.py` 的 `F6`
  读产物**内嵌字体**的族名。产物里含一个**内嵌的 `Type3` 过程字形件**时 ⇒ 按族名判（施加了正确主题 ⇒ `PASS`，实测内嵌 `TimesNewRomanPSMT`；
  **不施加主题 / 主题名不存在** ⇒ `FAIL`，内嵌 `SimSun`）；**没有**那个件时 ⇒ 字体只被引用、未内嵌 ⇒ **`N/A`**。
  ⚠️ **`/FontFile* = 0` 不等于"没内嵌字体"** —— **`Type3` 字体没有 `/FontFile` 条目**（早期据此推"Origin 不内嵌"是错的）。
  ★ **别去猜"什么会让它内嵌"**：这条触发条件改过几版、每版都被下一轮推翻或复现不出（控制者最近一次复现尝试
  **没成功**，但那个探针**没把文字渲染上去** ⇒ **不构成反证**）⇒ **直接量产物**（读 `F6` 判词，或数那个过程字形件）。
  ⚠️ 所以 `save()` 的 `theme=` **不是装饰** —— 它有 `Type3` 件时**正是 `F6` 判的那个东西**；只有**字形观感**仍只靠人看图。
- **`H10`（去上/右框线 · 刻度朝内）今天落不了地**：侦察未找到可用属性 ⇒ 本文件不设它。
"""
import json
import os
import pathlib
import re
import struct

# --------------------------------------------------------------------------- 样式表
_HERE = pathlib.Path(__file__).resolve()                       # …/assets/mcmplot_origin.py
# 仓根 = .claude/skills/mcm-plot-origin/assets/<本文件> 上溯四层。
_ROOT = _HERE.parents[4]
_STYLE_TABLE = _ROOT / ".claude/skills/mcm-figure-choose/assets/mcm-style.json"

_TABLE_CACHE = None


def _entries():
    """读那张表（**运行时**读，缓存于进程内）。表缺失 ⇒ fail-loud（不许静默给默认值）。"""
    global _TABLE_CACHE
    if _TABLE_CACHE is None:
        if not _STYLE_TABLE.is_file():
            raise FileNotFoundError(
                f"样式表不在位：{_STYLE_TABLE}（本模块的样式值**只从这张表读**）")
        _TABLE_CACHE = json.loads(_STYLE_TABLE.read_bytes().decode("utf-8"))["entries"]
    return _TABLE_CACHE


def _value(entry_id):
    """按 id 取某条目在**本载体**上的规范值（唯一来源 = 表）。"""
    for e in _entries():
        if e["id"] == entry_id:
            return e["value"]
    raise KeyError(f"样式表里没有条目 {entry_id!r}")


# --------------------------------------------------------------------------- 公开接口
def apply_style(page):
    """给图页上 house style：**色序**（**不动底色**；值从 `mcm-style.json` 读）。

    - **底色**：本函数对底色**不做动作**。理由 = **Origin 默认导出即白底**，白底由**产物**证
      （判据 `F4`）——**不是**"设了也没用"。★ 改底色**分语法**：Python 属性赋值
      （`layer.color = …` / `page.color = …`）是**哑的**（不抛错、也改不动产物 —— **像素层**
      成立：PNG 带时间戳块 `tIME`，别拿逐字节比对当判据；读它反而 `AttributeError`）；
      LabTalk（`layer.lt_exec("layer.color=…")`）**真能改产物**。
      ⇒ **不**从"Python 路无效"推出"改底色一律无效"。
    - **色序**：把 `series.color`（H14 的八色序列）**逐 plot** 设到页面里的每个层上；
      plot 数超过色数时按模回绕（调用方纪律：主色不宜超过规范那条上限，见规范正文）。

    参数 `page` = 一个 `originpro` 的 `GPage`（`op.new_graph()` 的返回值）。
    """
    colors = list(_value("series.color"))
    for layer in page:
        for i, plot in enumerate(layer.plot_list()):
            plot.color = colors[i % len(colors)]


def figsize_for(textwidth_in):
    """正文栏宽（英寸）→ **图宽**（英寸）。乘数 = 表里 H1 的**默认档上限**。

    `textwidth_in` = 判据侧 `--textwidth-in` 的**分母**：它是**用户论文的属性**，
    **不预设默认值**（本函数与检查器都不设），必须由调用方传入。
    """
    return float(textwidth_in) * float(_value("h1.width_ratio.default_hi"))


def save(page, path, dpi=300, theme="Times New Roman Font"):
    """把 `page` 导出到 `path`（`.png` / `.pdf`）：**宽度钉死** + **主题在导出那一刻施加**。

    - **宽度钉死**：导出宽 = **页面的物理宽**（`page.get_float('width') / page.get_float('resx')`，
      英寸）。调用方须先把页面物理宽设成 `figsize_for(textwidth_in)`（见 `references/workflow.md`）；
      这样导出宽就**不取决于 Origin"上次用的导出设置"**（那是个会跨图残留的旋钮）。
    - **PNG**：宽按 `dpi` 换算成像素（`tr1.Unit:=2`）——送判据时的 `--dpi` **必须与这里逐字一致**。
    - **PDF**：宽按英寸（`tr1.Unit:=0`）——页盒由 Origin 量化到 1/72 in；送判据时**不给** `--dpi`。
    - **主题**：`theme` 在**导出命令那一刻**施加（`expGraph … theme:=…`）。**不许**改用
      `themeApply2g` 提前施加：它只作用于施加那一刻**已存在**的对象，之后新建的文本注释会
      **回到 SimSun**（实测半张图两种字体）。
    - **返回**：`{"path", "requested_width_in", "actual_width_in", "kind"}` ——
      `actual_width_in` 是**从产物实测**回来的实际导出宽（PNG 读 IHDR、PDF 读 `/MediaBox`），
      供调用方自证"宽度真的钉上了"（Origin 的**返回值不算数**，只有产物算）。

    ## 进程卫生（本函数与调用方的分工）
    本函数用 `try/finally` 包住导出：**失败路径当场 `op.exit()`**（`originpro` 的 `atexit`
    在没走到 `op.exit()` 时只做 `Detach(releaseonly=True)` ⇒ Origin 进程会残留）；
    **成功路径不退**（会话内还要出第二个载体 —— 实测 `op.exit()` 之后页面对象即失效）。
    ⇒ **成功路径收尾的 `op.exit()` 归调用方**（场景脚本纪律，见 `references/workflow.md`）。
    """
    import originpro as op                                    # 只为失败路径的 op.exit()

    path = os.path.abspath(str(path))
    outdir, name = os.path.split(path)
    ext = os.path.splitext(name)[1].lower()
    if ext not in (".png", ".pdf"):
        raise ValueError(f"save() 只支持 .png / .pdf，收到 {ext!r}")

    width_in = _page_width_in(page)
    if ext == ".png":
        tr = f"tr1.Unit:=2 tr1.Width:={round(width_in * dpi)}"
    else:
        tr = f"tr1.Unit:=0 tr1.Width:={width_in}"
    cmd = (f'expgraph type:={ext[1:]} path:="{outdir}" filename:="{name}" '
           f'overwrite:=replace {tr} theme:="{theme}"')

    ok = False
    try:
        page.activate()                                       # expgraph 作用于活动窗口
        page.lt_exec(cmd)
        if not os.path.isfile(path):
            raise RuntimeError(f"导出后产物不存在 ⇒ Origin 静默失败了：{path}")
        actual = _measured_width_in(path, dpi)
        ok = True
        return {"path": path, "requested_width_in": width_in,
                "actual_width_in": actual, "kind": ext[1:]}
    finally:
        if not ok:
            op.exit()                                         # 失败 ⇒ 当场退，别留给 atexit 的 Detach


# --------------------------------------------------------------------------- 内部工具
def _page_width_in(page):
    """页面的物理宽（英寸）= `width` / `resx`（两者都是页面自身的量，不依赖"当前活动窗"）。"""
    return float(page.get_float("width")) / float(page.get_float("resx"))


def _measured_width_in(path, dpi):
    """**从产物实测**导出宽（英寸）——这是唯一算数的口径（Origin 的返回值不算数）。"""
    raw = pathlib.Path(path).read_bytes()
    if path.lower().endswith(".png"):
        # PNG：IHDR 的宽在高 4 字节之后，big-endian（纯 stdlib，不引 Pillow）。
        if raw[:8] != b"\x89PNG\r\n\x1a\n":
            raise ValueError(f"不是 PNG：{path}")
        px = struct.unpack(">I", raw[16:20])[0]
        return px / float(dpi)
    # PDF：第一处 /MediaBox 的宽（单位 1/72 in）。
    m = re.search(rb"/MediaBox\s*\[\s*[\d.+-]+\s+[\d.+-]+\s+([\d.+-]+)", raw)
    if m is None:
        raise ValueError(f"PDF 里找不到 /MediaBox：{path}")
    return float(m.group(1)) / 72.0
