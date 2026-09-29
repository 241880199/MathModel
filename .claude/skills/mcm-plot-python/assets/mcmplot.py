# -*- coding: utf-8 -*-
"""mcmplot —— MCM 论文图的薄封装（底座 + 尺寸 + 保存）。

**只回答一件事**：把"这张图该怎么画"落到 matplotlib 上，并让产物过得了既有的产物判据
（`check-figure-style.py`）。**不选图型**（那是 `mcm-figure-choose`）、**不出合规判词**。

## 与规范的接口（规范正文只在 `mcm-figure-choose/references/house-style.md`，本文件不复述）

三个入口的**参数名**与判据侧**逐字同名同义**：

- `figsize_for(textwidth_in)`：`textwidth_in` = 正文栏宽（英寸），即判据侧 `--textwidth-in` 的**分母**。
  **不预设默认值** —— 它是用户论文的属性，必须由调用方传入。
- `save(fig, path, dpi)`：`dpi` 必须与调用判据时传的 `--dpi` **一致**（否则 F1 的分母对不上）。
- `apply_style()`：叠底座并注册入库字体。

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
- **上/右悬空刻度（底座副作用）**：底座 `science` 自带 `xtick.top: True` / `ytick.right: True`，
  而 `mcm.mplstyle` 只关了 `axes.spines.top` / `axes.spines.right` 两条**边框线** ⇒ 图上/右会留下
  **没有边框线却仍在的悬空刻度**。**模块自身未关** —— 当前调用方得在**轴级**用
  `tick_params(top=False, right=False)` 自己关（GREEN 生成器就是这么做的）。**修复 owner：本模块的
  后续修复任务**（落点 = `mcm.mplstyle` 的覆盖键，属派生区，须走生成器）。
- **描白边会抬高 PNG 的 F2**：给条/块描白边时，抗锯齿与白底混出的浅色在 **PNG** 栅格上占比越过
  阈值 ⇒ 同一张图 PNG 的 F2 比 PDF 高（PDF 走栅格时混色占比低于阈值）。这更偏**用法**层
  （调用方不该给条描白边），**不是**模块要改的键。**修复 owner：本模块的后续修复任务**（落点可以是
  模块文档的用法禁忌 / `workflow.md` 的禁用项，或让 `save()` 之后的产物自带这条告警）。
"""
import pathlib

_ASSETS = pathlib.Path(__file__).resolve().parent
_MPLSTYLE = _ASSETS / "mcm.mplstyle"
# 入库的字体（随 skill 分发，**不依赖 TeX Live 路径**）。四档：Regular / Italic / Bold / BoldItalic。
_FONT_STYLES = ("Regular", "Italic", "Bold", "BoldItalic")
_FONTS = tuple(_ASSETS / "fonts" / f"TeXGyreTermesX-{s}.otf" for s in _FONT_STYLES)
# 底座 = 这两个 style 叠加（顺序固定；本 skill 的 mcm.mplstyle 再叠在其后 ⇒ 覆盖前者）。
_BASE_STYLES = ("science", "no-latex")

_FONTS_REGISTERED = False

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
