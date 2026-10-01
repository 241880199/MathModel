# -*- coding: utf-8 -*-
"""mcmplot —— MCM 论文图的薄封装（底座 + 尺寸 + 保存）。

**只回答一件事**：把"这张图该怎么画"落到 matplotlib 上，并让产物过得了既有的产物判据
（`check-figure-style.py`）。**不选图型**（那是 `mcm-figure-choose`）、**不出合规判词**。

## 与规范的接口（规范正文只在 `mcm-figure-choose/references/house-style.md`，本文件不复述）

四个入口的**参数名**与判据侧**逐字同名同义**：

- `figsize_for(textwidth_in)`：`textwidth_in` = 正文栏宽（英寸），即判据侧 `--textwidth-in` 的**分母**。
  **不预设默认值** —— 它是用户论文的属性，必须由调用方传入。
- `fontsize_for(body_pt)`：给出图内字号的**允许区间**；`body_pt` 同样由调用方传（正文 pt 是论文的属性）。
- `save(fig, path, dpi)`：`dpi` 必须与调用判据时传的 `--dpi` **一致**（否则 F1 的分母对不上）。
- `apply_style()`：叠底座并注册入库字体，**并当场读回断言色序真的落上了**（`axes.prop_cycle` 的
  静默失败没有别的东西挡得住 —— 见该函数与 `_declared_prop_cycle_colors()`）。

## 两条**照实记**的操作事实（设计 §9 在系统 matplotlib 上实测）

1. **`import scienceplots` 是必需的**：它靠 **import 的副作用**把 `science` / `no-latex` 注册进
   style 库；只 `import matplotlib.style` 再 `plt.style.use(["science", ...])` 会
   `OSError: 'science' is not a valid ...`。
2. **图内元素溢出时用 `layout='constrained'`（或 `fig.tight_layout()`），不要用 `bbox_inches='tight'`**：
   前两者只在固定画布内挪坐标轴、**不改输出宽**；`bbox_inches='tight'` 才是那个**会改输出宽**的键
   —— `save()` 因此把它钉在**默认**（`None`），免得 `figsize` 与图宽比的干净映射被悄悄破掉。

## 已知缺口（不许藏）

- **不实现 `usetex` 路径**（用户裁）：底座 `science` 设 `text.usetex=True`，`no-latex` 覆盖回 `False`。
  本机 TeX Live 缺 `type1cm.sty`，走 `usetex` 保存即 `RuntimeError`。
- **数学不是论文那一套**：论文的数学是 `NewTXMI` + `txexs`，本模块用 `mathtext`（`stix`）——
  **两套实现，逐字形同一做不到**。罗马字则用**入库的同一族**（`TeX Gyre TermesX`）。
- **中文字形缺失**：默认与 `science` 底座都缺中文字形（只 warning、图上留空白框）。
- ~~**上/右悬空刻度（底座副作用）**~~ **已处置**：底座 `science` 自带 `xtick.top: True` /
  `ytick.right: True`，而本件原先只关 `axes.spines.top` / `axes.spines.right` 两条**边框线**
  ⇒ 图上/右留下过**没有边框线却仍在的悬空刻度**。现已在 `mcm.mplstyle` 显式置 `xtick.top: False` /
  `ytick.right: False`（属派生区，由 `gen-mcm-style.py` 重放产出）。
  **证据（入库探针，可复算）**：底座 `science` 的刻度**朝内**，探针量**轴区顶边 / 右边内侧**带
  （带宽 = 刻度长 3pt ≈ 12.5 px @300dpi + 余量）内的非白像素数，并同跑一条只把这两个键改回 `True`
  的对照。**复算命令（逐字可粘）**：
  `python tests/skills/plot-python/probe-gap1-hanging-ticks.py`
  ⇒ **落地态两带均 0**；**旧态（对照）顶边带 234 / 右边带 120**（探针在对照里读得到墨迹 ⇒ 不是恒零）。
  探针本身就在入库件 `tests/skills/plot-python/probe-gap1-hanging-ticks.py`（含口径与射程），
  不依赖任何 gitignored 的过程件。
- **描白边会抬高 PNG 的 F2**（**已定性，改由判据侧承重**）：条/柱描白边时抗锯齿边与白底混出浅色，
  在 PNG 上把 F2 抬高一档（**两态读数实测**：同一张图不描边 PNG=3 → 描白边 PNG=5；同图的 PDF 两态
  都 =3。四个读数由 `make-evidence.py` 当场算、落在 `tests/skills/plot-python/red-green-evidence.md`）。
  **这批混色不在 H14 集合里** ⇒ 除 F2 外它也撞上 **F5（显式色序）**：这张图描白边的 **PNG** 报
  越界主色 **2 种**（`#e2f2fb` / `#faeed4`，即混色），**同图 PDF 报 0 种**（这批混色落到 0.5% 地板
  之下）。⚠️ **该结论只在探针用 H14 配色作画时成立**：探针若按 matplotlib 默认色序（`#1f77b4`…）
  作画，那三色本就不在 H14 集合里 ⇒ 两载体都报越界主色、F5 在探针图上**不区分载体**。
  **处置**：**不改 RED 语料**（写手产出物，手改 = 造伪）；源头加一条 **skill 侧用法禁令**
  （`references/workflow.md`），并由 `check-figure-style.py` 的 **F5/F2** 与 `green/out-G*/make_figure.py`
  **通篇不设 `edgecolor`**（`grep -rn edgecolor tests/skills/plot-python/green/` 零命中）这一事实共同承重。
  **复算命令**：`python tests/skills/plot-python/make-evidence.py`（当场重画四个产物、跑检查器，
  §4 里逐字列出 F2 表与四条 F5 判词）。
  **owner** = `mcm-plot-python` 后续任何改动 F2 口径的任务。
"""
import pathlib
import re

_ASSETS = pathlib.Path(__file__).resolve().parent
_MPLSTYLE = _ASSETS / "mcm.mplstyle"
# 入库的字体（随 skill 分发，**不依赖 TeX Live 路径**）。四档：Regular / Italic / Bold / BoldItalic。
_FONT_STYLES = ("Regular", "Italic", "Bold", "BoldItalic")
_FONTS = tuple(_ASSETS / "fonts" / f"TeXGyreTermesX-{s}.otf" for s in _FONT_STYLES)
# 底座 = 这两个 style 叠加（顺序固定；本 skill 的 mcm.mplstyle 再叠在其后 ⇒ 覆盖前者）。
_BASE_STYLES = ("science", "no-latex")

_FONTS_REGISTERED = False

# `mcm.mplstyle` 生成区里那行 `axes.prop_cycle: cycler('color', [...])` 的声明形态。
_PROP_CYCLE_RE = re.compile(r"(?m)^axes\.prop_cycle:\s*cycler\('color',\s*\[([^\]]*)\]\s*\)")


def _declared_prop_cycle_colors():
    """读回 `mcm.mplstyle`（**派生物**）里 `axes.prop_cycle` 声明的那串色 —— 本模块**不手写第二份**。

    四段链条：`mcm-figure-choose/assets/mcm-style.json` 的 `series.color` →（`gen-mcm-style.py` 重放）
    → 本文件那一行 →（matplotlib 解析）→ `rcParams`。本函数核**后两段**（"**声明了的色有没有真的落进
    `rcParams`**"）；前两段由 `gen-mcm-style.py` 的 fail-closed 抽值与 `check-style-freshness.py` 的
    A1/A2 两条臂守；产物上色序对不对则由 `check-figure-style.py` 的 F5 **端到端**判（拿产物对表）。

    **射程（如实写窄，本机实测）**：
    - "那一行解析失败"若**其色与底座不同** ⇒ 断言咬住（实测：声明 `['#111111', '#222222']` 时断言
      报"声明 `['111111','222222']` / 实得底座八色"）；
    - **盲区**：底座 `science` 若恰好也是同一串色，解析失败会被底座值**盖住**、断言不响
      （本机装的 SciencePlots 已被改成同一串色，正属这种情形）⇒ 那时靠 F5 与上面那两段守；
    - **不在射程内**：文件**声明本身写错**（但能解析）的情形 —— 本断言按定义对不上就报，对上就过；
      那条由链条第 1–2 段（生成器 + A1/A2）与 F5 覆盖。

    找不到那行 ⇒ **抛**（fail-loud）：派生件应由 `gen-mcm-style.py` 重放产出，缺了就没有核对的依据。
    """
    m = _PROP_CYCLE_RE.search(_MPLSTYLE.read_text(encoding="utf-8"))
    if m is None:
        raise RuntimeError(
            f"{_MPLSTYLE.name} 里找不到可解析的 `axes.prop_cycle: cycler('color', […])` 行 "
            f"⇒ 色序无从核对（派生件应由 gen-mcm-style.py 重放产出）")
    return [c.lstrip("#") for c in re.findall(r"'([^']+)'", m.group(1))]


# >>> BEGIN GENERATED: HOUSE_STYLE（gen-mcm-style.py 重放，勿手改）>>>
# 规范（.claude/skills/mcm-figure-choose/references/house-style.md）在本模块里的镜像。
# 本区由 tests/skills/plot-python/gen-mcm-style.py 从规范**逐条锚定**重放产出 ——
# **勿手改**（改了下一次重放就没了；要改请改规范里那条，再重放）。
HOUSE_STYLE = {
    'h1_width_ratio_min': 0.8,
    'h1_width_ratio_max': 1.2,
    'h1_width_ratio_default_lo': 0.95,
    'h1_width_ratio_default_hi': 1.0,
    'h3_aspect_ratio_lo': 2,
    'h3_aspect_ratio_hi': 3,
    'h3_height_in': 2.6,
    'h4_max_main_colors': 4,
    'h12_font_scale_lo': 0.8,
    'h12_font_scale_hi': 1.0,
    'h12_font_min_pt': 7,
}
# <<< END GENERATED: HOUSE_STYLE <<<


def apply_style():
    """叠上底座 `['science', 'no-latex']` + 本 skill 的 `mcm.mplstyle`，并注册入库字体。

    顺序：先 `addfont()` 把入库的四档 OTF 注册进 font manager（**不碰 TeX Live 路径**），再
    `plt.style.use`；`mcm.mplstyle` 放**最后** ⇒ 它覆盖底座里那些本模块要自管的键
    （`savefig.bbox` 等）。
    """
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    import scienceplots  # noqa: F401  —— 靠 import 的副作用注册 style 名（见模块头第 1 条）

    global _FONTS_REGISTERED
    if not _FONTS_REGISTERED:
        for f in _FONTS:
            font_manager.fontManager.addfont(str(f))
        _FONTS_REGISTERED = True
    plt.style.use([*_BASE_STYLES, str(_MPLSTYLE)])

    # ★ 硬要求：**设完之后当场读回、断言色序真的落上了** —— 因为"没设上"在这里是**静默**的：
    #   mplstyle 解析器把 `#` 当**注释起始**，所以 `mcm.mplstyle` 里那行的 hex 一旦带上 `#`，
    #   解析就失败、只往 stderr 打一条 `Bad value in file …`，`rcParams` **保持原值**（底座色序）。
    #   没有这条断言，"色序没落上"会一路没人发现。核对的基准 = 那一行**自己声明**的那串色
    #   （不在这里手写第二份，见 `_declared_prop_cycle_colors()`）。
    _got = [c.lstrip("#") for c in plt.rcParams["axes.prop_cycle"].by_key()["color"]]
    _want = _declared_prop_cycle_colors()
    assert _got == _want, (
        f"prop_cycle 没落上（静默失败）：mcm.mplstyle 声明 {_want}，rcParams 实得 {_got}")


def figsize_for(textwidth_in):
    """规范 §H2 的分母（`textwidth_in`，英寸）→ `(宽, 高)`（英寸）——`subplots(figsize=...)` 用。

    宽 = 分母 × 规范 H1 的**默认档上限**（"贴近正文宽"里最靠"占满"的那一端）；
    高 = 规范 H3 的**图高量级**。两个乘数都取自下面的生成常量区（**不手写**）。
    """
    return (textwidth_in * HOUSE_STYLE["h1_width_ratio_default_hi"],
            HOUSE_STYLE["h3_height_in"])


def fontsize_for(body_pt):
    """规范 §H12：正文 pt → 图内字号的**允许区间** `(下限, 上限)`（pt）。

    口径：图内字号 = 正文的 `[h12_font_scale_lo, h12_font_scale_hi]` 倍，且**不低于**
    `h12_font_min_pt`。调用方取一档（默认建议取上限 = 与正文同号）。`body_pt` = 用户论文的正文 pt，
    必须由调用方传入（它是论文的属性）。
    """
    lo = max(body_pt * HOUSE_STYLE["h12_font_scale_lo"], HOUSE_STYLE["h12_font_min_pt"])
    hi = max(body_pt * HOUSE_STYLE["h12_font_scale_hi"], HOUSE_STYLE["h12_font_min_pt"])
    return (lo, hi)


def save(fig, path, dpi):
    """保存：**默认 `bbox_inches`**（`None`）——绝不传 `'tight'`（见模块头第 2 条）。

    `None` 的含义是"走 `rcParams['savefig.bbox']`"，而 `mcm.mplstyle`（由 `apply_style()` 叠上）
    已把那个键钉在 `standard` ⇒ 输出宽 == `figsize` 宽。**别**在这里传 `bbox_inches='tight'`
    去"补救"溢出——那会改输出宽、毁掉与判据分母的干净映射。
    `dpi` 由调用方传入，且**必须**与该图送进 `check-figure-style.py` 时的 `--dpi` 一致。
    """
    fig.savefig(path, dpi=dpi, bbox_inches=None)
