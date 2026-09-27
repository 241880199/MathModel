#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`house-style.md` / `provenance.md` 里**每个数**的守卫——表驱动，fail-closed。

用法：
  python tests/skills/figure-choose/check-house-style.py                # 全跑
  python tests/skills/figure-choose/check-house-style.py --only G-H1-hi P-H2-a
  python tests/skills/figure-choose/check-house-style.py --list
  python tests/skills/figure-choose/check-house-style.py --no-provenance

末行恒为 `RESULT: PASS` 或 `RESULT: FAIL（...）`；退出码 0 / 1。**抽不到数即 FAIL（fail-closed）**：
被守的文档一改坏，对应守卫必须红——这正是本仓栽过六次的"判据恒绿"要防的事。

## 三类守卫

1. `GUARDS`（`G-*`）：一行 `(id, house-style.md 里的正则, 期望值来源, 容差, 说明)`。
   - 期望值**一律从文档现取**（`re.search` 的 group(1)），**不许抄进脚本**；
   - 正则必须在文档里**恰命中 1 处**（否则 FAIL——防止锚点被挤到别处）；
   - 期望值来源三种：`metric:<名>`（现算，走 `house-metrics.py` 的名册）·
     `const:<模块>.<属性>`（钉死出货检查器 / 度量模块的常量）· `text:<名>`（文本量，整串相等）。
2. `PROV`（`P-*`）：`provenance.md` 的**每一条**必须有 `数:` / `容差:` / `复跑命令:`，
   且**那次复跑确实跑出那个数**——命令按文档原样起子进程（`cwd` = 仓根），从 stdout 取回读数比对；
   取回时**名册名必须与命令里的 `--metric` 逐字相同**（只认 `name = value` 的形态时，
   「指错 metric、但数值恰好相同」的条目会静默通过）。
   写 `数: 无` 的条目**必须**写 `复跑命令: 无`（"没有数"与"没有命令"互为充要，违反即 FAIL）。
   **已知边界**：这条只证明"命令跑出来的数 = 文档写的数"，**不证明该命令就是那条口径该用的仪器**
   （entry 不声明"本数出自哪个 metric"，故 `--metric` 名与 `口径` 描述是否同指一事，本检查器判不了）。
   `provenance.md` 里**说明性散文数字**（不在 `数:` 行上的）由 `PROV_GUARDS` 单独守，见下。
3. `CENSUS`：扫 `house-style.md` 里**所有数字**，被上面两类守卫覆盖之外的每一个都必须落进
   `REASONS`（数字本体自证）或 `CONTEXT_REASONS`（按 token 前后窗口的上下文自证），
   **两张表都不含"任何整数"式的万能兜底** ⇒ 文档里新写进去的整数**也会** FAIL。
   ⇒ 射程：**`house-style.md` 的全部数字** + **`provenance.md` 的 `数:` 行与 `PROV_GUARDS` 命中的散文数**；
   `provenance.md` 里**未被 `PROV_GUARDS` 命中的**散文数字仍是本检查器的盲区（明写在案，不假装覆盖）。
4. `PROV_GUARDS`（`G-P-*`）：`provenance.md` 里**散文**里的数（不在 `数:` 行上、因而不经 `run_prov` 的）
   的守卫——与 `GUARDS` 同形，只是文本换成 `provenance.md`。**只有列进表里的才被守**。
5. `STRUCT_GUARDS`（`S1`–`S5`）：`chart-types.md` 的**结构**（那棵决策树的形状），
   与 `GUARDS` 同一表驱动结构。被验的**不是**实测读数，而是"入口齐不齐 / 四段齐不齐 / 高频标注在不在 /
   抄过去参照分布数有没有漂"。**期望值分两类，来源不同**：
   - **入口名**（`S1`）= **契约**，**硬编码在下面 `ENTRIES`**：那九个名字是任务书 Interfaces 的产物
     （Task 5 的 SKILL.md 依赖它们），**不从被验文档现取** —— 现取就等于"改文档即改期望值"，
     判据会退化成恒真。`S1` 因此只判"文档里的标题**恰好等于**契约"。
   - **数**（`S5`）= 从 `house-style.md` **现取**（**不抄进脚本**）：每个小数必须**归到它同行的 `H<n>` 引用**，
     且**值 ∈ 那个 `H<n>` 条目里的数**（跨条目搬数即红；无所属的小数也红）。
   **抽不到即 FAIL**（`S5` 抽不到任何小数也红 —— 否则把数字全删光就能让这条判据恒绿）。
   **`S4` 是「读数条」不是判据** —— 它只印"定义行数 / 不同名数 / 重名的名字"，**不进 `bad`**；
   **唯一的例外出口**是 `chart-types.md` **读不出/解析失败**时它与其余结构守卫一起记红
   （fail-closed，见 `main()` 里的那一段）。理由见 `S4` 那一行的 NOTE：计数没有可失败的谓词，
   "计数 > 0"式的断言会变成**看着能红、实则恒真**的判据——那正是本仓栽过六次的东西。
6. `SKILL_GUARDS`（`K1`–`K8`）：`SKILL.md` 的**短契约**（行数 / 指针 / **不复述任何规范数值** /
   九个入口名（含它自己那张决策树表）/ **数字的处置**（显式声明结构性计数，且声明行只许出现契约数）/
   **点名不存在的 skill 必须标〔拟建〕（双向）** / **五段标题与输出契约三件套齐全** /
   **「逐条标了验证状态」这句断言必须成立**）。
   期望值同样**分两类**：契约型硬编码（`SK_MAX_LINES` / `SK_POINTER` / `ENTRIES` /
   单位词表 `SK_CN_UNITS`），现取型是**禁止串**（`house-style.md` 里的小数字面量、`≤n` 形态，
   以及由它们推出的**中文数词写法**，**现取**、不抄进脚本）。
   ★ **射程写实（别当成"覆盖了所有复述手法"）**：`K3` 认小数 / `≤n` / `<n 词` /
   **中文数词 + 规范单位词** / **≥4 的规范整数值的中文写法**；**1–3 的中文写法、百位以上，
   以及"这句话是不是在复述规范"本身，都不在机械射程内**（那一层是判断层的事，同 `S4`）。
   逐条口径写在各自函数的 NOTE 里。
"""
import argparse
import collections
import importlib.util
import pathlib
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parents[3]
DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"
PROV = ROOT / ".claude/skills/mcm-figure-choose/references/provenance.md"
CT = ROOT / ".claude/skills/mcm-figure-choose/references/chart-types.md"
SK = ROOT / ".claude/skills/mcm-figure-choose/SKILL.md"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


HM = _load(pathlib.Path(__file__).resolve().parent / "house-metrics.py", "house_metrics")
CS = _load(pathlib.Path(__file__).resolve().parent / "check-figure-style.py", "check_figure_style")
CONSTS = {"CS": CS, "HM": HM}


# ------------------------------------------------------------------ 守卫表
# (id, 文档正则, 期望值来源, 容差, 说明)
GUARDS = [
    # ---- §0 样本框架与交付形态
    ("G-F0-papers", r"\*\*(\d+) 份\*\*论文", "metric:n_papers", 0.5, "样本份数"),
    ("G-F0-figs", r"\*\*(\d+) 张图\*\*", "metric:n_figs", 0.5, "样本图数"),
    ("G-F0-tabs", r"\*\*(\d+) 张表\*\*", "metric:n_tabs", 0.5, "同批抽到的表数"),
    ("G-F0-other", r"其余 (\d+) 份未抽取", "metric:n_other_papers", 0.5, "未建索引的其余合集份数"),
    ("G-F0-dpi", r"\*\*(\d+) dpi\*\* 渲染带", "const:HM.DPI", 0, "渲染 dpi（几何仪器的构造已知量）"),
    ("G-F0-judge", r"判断层随机 (\d+) 张", "metric:judge_n", 0.5, "判断层抽样量"),
    ("G-F0-pages", r"实测\*\*页数 (\d+)\*\*", "metric:probe_pages", 0.5, "两页探针的页数"),
    ("G-F0-p1w", r"page1 = \*\*([\d.]+) in\*\*", "metric:probe_page1_w_in", 0.02, "探针 page1 宽（应=分母 6.31）"),
    ("G-F0-p1c", r"page1 = \*\*[\d.]+ in\*\* / \*\*(\d+) 色\*\*", "metric:probe_page1_colors", 0.5, "探针 page1 的 F2 读数"),
    ("G-F0-p2w", r"page2 = \*\*([\d.]+) in\*\*", "metric:probe_page2_w_in", 0.02, "探针 page2 宽（应超 1.20×）"),
    ("G-F0-p2c", r"page2 = \*\*[\d.]+ in\*\* / \*\*(\d+) 色\*\*", "metric:probe_page2_colors", 0.5, "探针 page2 的 F2 读数"),
    ("G-F0-p1ratio", r"（F1 比值恰 ([\d.]+)）", "metric:probe_page1_ratio", 0.002, "探针 page1 的 F1 比值（=1.000）"),
    ("G-F0-verdict", r"整份仍判 (PASS|FAIL)\*\*", "text:probe_verdict", 0, "整份探针的判词（只读 doc[0] 的证据）"),
    # ---- H1
    ("G-H1-p25b", r"p25 \*\*([\d.]+)\*\*（= 下限", "metric:h1_p25", 0.02, "比值 p25 的未舍入读数"),
    ("G-H1-maxb", r"max \*\*([\d.]+)\*\*（= 上限", "metric:h1_max", 0.02, "比值 max 的未舍入读数"),
    ("G-H1-band-lo", r"（\*\*([\d.]+)–[\d.]+×\*\*）", "metric:h1_med", 0.02, "默认档左端 = 中位"),
    ("G-H1-band-hi", r"（\*\*[\d.]+–([\d.]+)×\*\*）", "metric:h1_p75", 0.02, "默认档右端 = p75"),
    ("G-H1-lo", r"\*\*不窄于 ([\d.]+)×\*\*", "metric:h1_p25", 0.02, "下限 = p25"),
    ("G-H1-hi", r"\*\*不超过 ([\d.]+)×\*\*", "metric:h1_max", 0.02, "上限 = max"),
    ("G-H1-med", r"\*\*比值中位 ([\d.]+)\*\*", "metric:h1_med", 0.02, "比值中位"),
    ("G-H1-p75", r"p75 ([\d.]+)、max", "metric:h1_p75", 0.02, "比值 p75"),
    ("G-H1-band", r"只有 \*\*([\d.]+)%\*\* 落在", "metric:h1_band_pct", 0.2, "参照分布自身的 F1 合规率（H13 的反例）"),
    ("G-H1-below", r"低于 0\.80 的占 \*\*([\d.]+)%\*\*", "metric:h1_below_pct", 0.2, "低于下限的占比"),
    ("G-H1-above", r"高于 1\.20 的 \*\*([\d.]+)%\*\*", "metric:h1_above_pct", 0.2, "高于上限的占比"),
    ("G-H1-const-lo", r"\*\*不窄于 ([\d.]+)×\*\*", "const:CS.F1_LO", 0, "文档的 0.80 必须 == 出货常量 F1_LO"),
    ("G-H1-const-hi", r"\*\*不超过 ([\d.]+)×\*\*", "const:CS.F1_HI", 0, "文档的 1.20 必须 == 出货常量 F1_HI"),
    # ---- H2
    ("G-H2-den", r"p90 的\*\*全局中位 ([\d.]+) in\*\*", "metric:h2_colw_p90_median", 0.02, "分母 = 43 篇 p90 的全局中位"),
    ("G-H2-den-raw", r"（未舍入 ([\d.]+)）", "metric:h2_colw_p90_median", 0.0001, "分母的未舍入值"),
    ("G-H2-fork-global", r"\*\*全局分母 ([\d.]+)%\*\*", "metric:h2_fork_global_pct", 0.2, "口径分叉：全局分母"),
    ("G-H2-fork-perpaper", r"\*\*逐篇分母 ([\d.]+)%\*\*", "metric:h2_fork_perpaper_pct", 0.2, "口径分叉：逐篇分母"),
    # ---- H3
    ("G-H3-vert", r"竖向图只占 ([\d.]+)%", "metric:h3_below1_pct", 0.2, "竖向图占比（违反判据里的说法）"),
    ("G-H3-band", r"样本内 \*\*([\d.]+)%\*\* 落在带内", "metric:h3_in_band_pct", 0.2, "常见带 [2,3] 的样本权重"),
    ("G-H3-hrule", r"图高按 \*\*([\d.]+) in 量级\*\*", "metric:h3_h_med", 0.05, "图高量级 = 实测中位"),
    ("G-H3-land", r"\*\*横向占 ([\d.]+)%\*\*", "metric:h3_land_pct", 0.2, "横图占比"),
    ("G-H3-below1", r"竖向只有 ([\d.]+)%", "metric:h3_below1_pct", 0.2, "竖图占比"),
    ("G-H3-aspect", r"\*\*宽高比中位 ([\d.]+)\*\*", "metric:h3_aspect_med", 0.02, "宽高比中位"),
    ("G-H3-ge2", r"\*\*宽高比 ≥2 占 ([\d.]+)%\*\*", "metric:h3_ge2_pct", 0.2, "宽高比 ≥2 占比"),
    ("G-H3-hmed", r"\*\*图高中位 ([\d.]+) in\*\*", "metric:h3_h_med", 0.02, "图高中位"),
    ("G-H3-h25", r"in\*\*（p25 ([\d.]+) / p75 [\d.]+）", "metric:h3_h_p25", 0.02, "图高 p25"),
    ("G-H3-h75", r"in\*\*（p25 [\d.]+ / p75 ([\d.]+)）", "metric:h3_h_p75", 0.02, "图高 p75"),
    ("G-H3-a25", r"（p25 ([\d.]+) / p75 [\d.]+ 都在带外）", "metric:h3_aspect_p25", 0.02, "宽高比 p25"),
    ("G-H3-a75", r"（p25 [\d.]+ / p75 ([\d.]+) 都在带外）", "metric:h3_aspect_p75", 0.02, "宽高比 p75"),
    ("G-H3-legacy", r"aspect = ([\d.]+)", "metric:h3_legacy_2427", 0.001,
     "2.427 —— 入库证据里**唯一等于 2.427 的单张读数**（**不是**设计稿 2.42 的来源，只是巧合）"),
    ("G-H3-s120-lo", r"中位落在 \*\*([\d.]+)–[\d.]+\*\*", "metric:h3_aspect_s120_med_lo", 0.01,
     "908 池里 120 张抽样的宽高比中位**下界**（2.42 不可复跑的证据）"),
    ("G-H3-s120-hi", r"中位落在 \*\*[\d.]+–([\d.]+)\*\*", "metric:h3_aspect_s120_med_hi", 0.01,
     "同上**上界**（设计稿 2.42 落在这一段里）"),
    ("G-H3-908", r"「(\d+) 张 PNG；抽样", "metric:n_png_all", 0.5,
     "2.42 那次抽样的池子 = 908 张（662 图 + 246 表）"),
    # ---- H4
    ("G-H4-r1sub", r"离散标定件 R1 的 ([\d.]+)%", "metric:f2_r1_subfloor_max_pct", 0.002,
     "R1（离散配色）的最高落选箱——**比真热力图还高** ⇒ 这条线不区分连续/离散"),
    ("G-H4-r3sub", r"（R3 的最高落选箱 \*\*([\d.]+)%\*\*", "metric:f2_r3_subfloor_max_pct", 0.002,
     "R3（离散配色）的最高落选箱（同样低于新线）"),

    # ---- H4：N-2 那一对的口径（Critical-1 修复）
    ("G-H4-n2pair-hi", r"引的那一对 \*\*([\d.]+)% / ", "metric:color_cov4_sample166_pct", 0.2,
     "N-2 那一对的 72.9%（出货仪器在 166 抽样上）"),
    ("G-H4-n2pair-lo", r"引的那一对 \*\*[\d.]+% / ([\d.]+)%\*\*", "metric:recon_baseline_minw_s166_cov4_pct", 0.2,
     "N-2 那一对的 57.2%——baseline §7 转写口径在 166 抽样上，**可复现**"),
    ("G-H4-n2med", r"分箱；中位 \*\*([\d.]+)\*\*、零彩", "metric:recon_baseline_minw_s166_median", 0.05,
     "转写口径在 166 抽样上的主色中位（baseline 报 4.0）"),
    ("G-H4-n2zero", r"零彩 \*\*([\d.]+)%\*\* 与 baseline", "metric:recon_baseline_minw_s166_zero_pct", 0.05,
     "转写口径在 166 抽样上的零彩占比（baseline 报 15.7）"),
    ("G-H4-n2real", r"在同一 166 抽样上给 \*\*([\d.]+)%\*\*", "metric:recon_cov4_s166_pct", 0.2,
     "**真侦察仪器**在同一 166 抽样上的 ≤4 覆盖率（≠ 57.2% ⇒ 两者不同源）"),
    ("G-H4-n2lo", r"在 \*\*662\*\* 上是 \*\*([\d.]+)%\*\*", "metric:recon_baseline_minw_cov4_pct", 0.2,
     "转写口径在 **662** 图上的 ≤4 覆盖率（原记的 48.79 不实，真值在此）"),
    # ---- H4：连续色图闸门（Important-3 修复）
    ("G-H4-gate-warn", r"而其中 \*\*([\d.]+)%\*\* 被下面那道", "metric:cont_gate_pct", 0.2,
     "全 662 里被连续色图闸门判为『条数不可引用』的比例（依据里的自相矛盾点）"),
    ("G-H4-comp-n", r"连续色图的 \*\*(\d+) 张\*\*", "metric:cont_comp_n", 0.5, "闸门补集（未被判为连续色图）张数"),
    ("G-H4-comp-med", r"张\*\*）：主色中位 \*\*(\d+)\*\*", "metric:color_median_comp", 0.5,
     "补集上的出货仪器主色中位（与全 662 的 2 对照）"),
    ("G-H4-comp-zero", r"主色中位 \*\*\d+\*\*、零彩色 \*\*([\d.]+)%\*\*", "metric:color_zero_pct_comp", 0.2,
     "补集上的零彩色占比"),
    ("G-H4-comp-cov", r"零彩色 \*\*[\d.]+%\*\*、≤4 覆盖率 \*\*([\d.]+)%\*\*", "metric:color_cov4_pct_comp", 0.2,
     "补集上的 ≤4 覆盖率"),
    ("G-H4-gate-box", r"彩色箱数 ≥(\d+)\*\* \*\*或\*\*", "const:HM.CONT_BOX_MIN", 0,
     "新闸门：箱数下限（== CONT_BOX_MIN）"),
    ("G-H4-gate-sub", r"最高落选箱 ≥([\d.]+)%\*\* ⇒", "const:HM.CONT_SUBFLOOR_MIN_PCT", 0,
     "新闸门：最高落选箱下限（== CONT_SUBFLOOR_MIN_PCT）"),
    ("G-H4-gate-old-box", r"旧闸门（彩色箱数 \*\*≥(\d+)\*\*", "const:HM.CONT_BOX_VACUOUS_MAX", 0,
     "旧闸门箱数下限（== CONT_BOX_VACUOUS_MAX，形同虚设的那条腿）"),
    ("G-H4-gate-old-sub", r"最高落选箱 \*\*≥([\d.]+)%\*\*）", "const:HM.CONT_SUBFLOOR_OLD_PCT", 0,
     "旧闸门最高落选箱下限（== CONT_SUBFLOOR_OLD_PCT，漏真热力图的那条腿）"),
    ("G-H4-boxvac", r"全 662 里 \*\*([\d.]+)%\*\* 过这一关", "metric:cont_box20_pass_pct", 0.1,
     "旧闸门箱数腿放进来的比例（形同虚设的读数）"),
    ("G-H4-boxvac-n", r"（<20 箱的只有 \*\*(\d+) 张\*\*）", "metric:cont_box20_below_n", 0.5,
     "旧闸门箱数腿真正挡住的张数"),
    ("G-H4-heat-den", r"\*\*图注带 `heatmap` 的 (\d+) 张\*\*", "metric:cont_heat_den", 0.5,
     "heatmap 图注样本量（正则 heat\\s*-?\\s*map）"),
    ("G-H4-heat-old", r"旧闸门只命中 \*\*(\d+)/13\*\*", "metric:cont_heat_hit_old_n", 0.5,
     "旧闸门在 heatmap 样本上的命中数"),
    ("G-H4-cite-den", r"\*\*(\d+) 张里旧闸门只命中 \d+ 张\*\*", "metric:cont_cite_den", 0.5,
     "heatmap 样本里 F2 条数 >4（会被引用）的张数"),
    ("G-H4-cite-old", r"\*\*\d+ 张里旧闸门只命中 (\d+) 张\*\*", "metric:cont_cite_old_n", 0.5,
     "旧闸门在那批『条数会被引用』的图里的命中数（漏检证据）"),
    ("G-H4-ex1-f2", r"fig-10-p19\.png` \| (\d+) \|", "metric:cont_ex1_f2", 0.5, "漏检典型 #1 的 F2 条数"),
    ("G-H4-ex1-sub", r"fig-10-p19\.png` \| \d+ \| ([\d.]+)%", "metric:cont_ex1_sub_pct", 0.002,
     "漏检典型 #1 的最高落选箱"),
    ("G-H4-ex2-f2", r"fig-08-p13\.png` \| (\d+) \|", "metric:cont_ex2_f2", 0.5, "漏检典型 #2 的 F2 条数"),
    ("G-H4-ex2-sub", r"fig-08-p13\.png` \| \d+ \| ([\d.]+)%", "metric:cont_ex2_sub_pct", 0.002,
     "漏检典型 #2 的最高落选箱（< R1 的 0.127%）"),
    ("G-H4-heat-new", r"新闸门（\*\*或\*\*）在同一 13 张上命中 \*\*(\d+)/13\*\*", "metric:cont_heat_hit_n", 0.5,
     "新闸门在 heatmap 样本上的命中数"),
    ("G-H4-cite-new", r"在同一 13 张上命中 \*\*11/\d+\*\*、\*\*那 (\d+) 张全部", "metric:cont_cite_n", 0.5,
     "新闸门在『条数会被引用』的 heatmap 图上的命中数"),
    ("G-H4-gate-new", r"命中率由 \*\*[\d.]+%\*\* 升到 \*\*([\d.]+)%\*\*", "metric:cont_gate_pct", 0.2,
     "新闸门在全 662 上的命中率"),
    ("G-H4-gate-old", r"命中率由 \*\*([\d.]+)%\*\* 升到", "metric:cont_gate_old_pct", 0.2,
     "旧闸门在全 662 上的命中率"),
    ("G-H4-ratio-disc", r"箱数/条数 = \*\*([\d.]+)\*\*", "metric:cont_ratio_disc", 0.05,
     "离散标定件 R1 的 箱数÷条数（比真热力图还高）"),
    ("G-H4-ratio-heat", r"fig-10-p19\.png` 只有 \*\*([\d.]+)\*\*", "metric:cont_ratio_heat", 0.05,
     "真热力图的同一条比值（< 离散件 ⇒ 该判据方向反了）"),
    ("G-H4-max", r"彩色\*\*主色 ≤(\d+)\*\*", "const:CS.F2_MAX", 0, "文档的 ≤4 必须 == 出货常量 F2_MAX"),
    ("G-H4-med", r"出货：主色中位 \*\*(\d+)\*\*", "metric:color_median", 0.5, "出货仪器主色中位"),
    ("G-H4-zero", r"出货：零彩色 \*\*([\d.]+)%\*\*", "metric:color_zero_pct", 0.2, "出货仪器零彩色占比"),
    ("G-H4-zeron", r"出货：零彩色 \*\*[\d.]+%\*\*（(\d+)/662）", "metric:color_zero_n", 0.5, "零彩色张数"),
    ("G-H4-cov", r"出货：≤4 覆盖率 \*\*([\d.]+)%\*\*", "metric:color_cov4_pct", 0.2, "出货仪器 ≤4 覆盖率"),
    ("G-H4-covn", r"出货：≤4 覆盖率 \*\*[\d.]+%\*\*（(\d+)/662）", "metric:color_cov4_n", 0.5, "≤4 覆盖张数"),
    ("G-H4-rmed", r"侦察：主色中位 \*\*(\d+)\*\*", "metric:recon_median", 0.5, "侦察仪器主色中位"),
    ("G-H4-rzero", r"侦察：零彩色 \*\*([\d.]+)%\*\*", "metric:recon_zero_pct", 0.2, "侦察仪器零彩色占比"),
    ("G-H4-rcov", r"侦察：≤4 覆盖率 \*\*([\d.]+)%\*\*", "metric:recon_cov4_pct", 0.2, "侦察仪器 ≤4 覆盖率"),
    ("G-H4-rcovn", r"侦察：≤4 覆盖率 \*\*[\d.]+%\*\*（(\d+)/662）", "metric:recon_cov4_n", 0.5, "侦察仪器 ≤4 覆盖张数"),
    ("G-H4-ledger", r"\*\*台账逐格一致 (\d+)\*\*", "metric:recon_ledger_match", 0.5, "重写件 vs 入库台账逐格一致数"),
    ("G-H4-n2-n", r"是 \*\*(\d+) 张抽样\*\*上的数", "metric:n_sample166", 0.5, "N-2 那一对的抽样量"),
    ("G-H4-cont-n", r"连续色图按 F2 计到 (\d+) 条\*\*", "metric:f2_r2_counted", 0.5, "连续色图的 F2 条数"),
    ("G-H4-cont-box", r"彩色箱有 \*\*(\d+)\*\* 个", "metric:f2_r2_boxes", 0.5, "连续色图的彩色箱数"),
    ("G-H4-cont-sub", r"\*\*最高落选箱 ([\d.]+)%\*\*", "metric:f2_r2_subfloor_max_pct", 0.02, "最高落选箱"),
    ("G-H4-cont-low", r"\*\*入选的最低箱 ([\d.]+)%\*\*", "metric:f2_r2_lowest_counted_pct", 0.02, "入选的最低箱"),
    ("G-H4-cont-mgn", r"离 0\.5% 地板仅 ([\d.]+)pp\*\*", "metric:f2_r2_margin_pp", 0.02, "离地板的富余"),
    ("G-H4-floor", r"离 ([\d.]+)% 地板仅", "metric:f2_floor_pct", 0.001, "0.5% 地板 = f2-diagnose.py 的 FLOOR"),
    # ---- H5
    ("G-H5-strict-n", r"严判据命中 (\d+) 张 / 662\*\*", "metric:tab10_strict_n", 0.5, "严判据命中张数"),
    ("G-H5-eye", r"人眼复核 (\d+)/", "metric:tab10_strict_n", 0.5, "人眼复核张数 = 命中张数（6/6）"),
    ("G-H5-strict", r"\*\*严判据读数 ([\d.]+)%\*\*", "metric:tab10_strict_pct", 0.02, "严判据读数（下界）"),
    ("G-H5-strict-raw", r"未舍入 ([\d.]+)%", "metric:tab10_strict_pct", 0.02, "严判据读数的未舍入值"),
    ("G-H5-loose", r"\*\*松判据读数 ([\d.]+)%\*\*", "metric:tab10_loose_pct", 0.1, "松判据读数（已证伪）"),
    ("G-H5-loosen", r"（(\d+)/662）\*\*已被人眼证伪\*\*", "metric:tab10_loose_n", 0.5,
     "松判据命中的张数（原被整数兜底豁免，Important-2 后必须入表）"),
    # ---- H6
    ("G-H6-pie-n", r"\*\*饼图 (\d+) 张\*\*", "metric:judge_pie_n", 0.5, "判断层饼图张数"),
    ("G-H6-pie-pct", r"\*\*饼图占比 ([\d.]+)%\*\*", "metric:judge_pie_pct", 0.2, "判断层饼图占比"),
    # ---- H7
    ("G-H7-3d", r"\*\*3D 判断层读数 ([\d.]+)%\*\*", "metric:judge_3d_pct", 0.1, "判断层 3D 读数"),
    ("G-H7-3dn", r"3D 判断层读数 [\d.]+%\*\*（(\d+)/120）", "metric:judge_3d_n", 0.5, "判断层 3D 张数"),
    ("G-H7-cap", r"\*\*图注口径 ([\d.]+)%\*\*", "metric:caption_3d_pct", 0.1, "图注口径 3D 读数"),
    ("G-H7-capn", r"three-dimensional`，(\d+)/662", "metric:caption_3d_n", 0.5, "图注口径 3D 张数"),
    # ---- H8
    ("G-H8-mp", r"\*\*多面板判断层 ([\d.]+)%\*\*", "metric:judge_mp_pct", 0.1, "判断层多面板占比"),
    ("G-H8-mp-n", r"多面板判断层 [\d.]+%\*\*（(\d+)/120）", "metric:judge_mp_n", 0.5, "判断层多面板张数"),
    ("G-H8-pixel", r"\*\*像素判据读数 ([\d.]+)%\*\*", "metric:pixel_mp_pct", 0.2, "像素判据多面板读数"),
    ("G-H8-pixel-n", r"像素判据读数 [\d.]+%\*\*（(\d+)/662）", "metric:pixel_mp_n", 0.5, "像素判据多面板张数"),
    ("G-H8-agree", r"\*\*与像素判据一致率 ([\d.]+)%\*\*", "metric:mp_agree_pct", 0.1, "两判据一致率"),
    ("G-H8-agree-n", r"与像素判据一致率 [\d.]+%\*\*（(\d+)/120）", "metric:mp_agree_n", 0.5, "两判据一致张数"),
    # ---- H9
    ("G-H9-lv1", r"\*\*>(\d+) 词 = 违反\*\*", "const:CS.CAP_MAX", 0, "两级词数：>12 = 违反（== CAP_MAX）"),
    ("G-H9-lv2", r"\*\*>(\d+) 词 = 严重违反\*\*", "const:CS.CAP_HARD", 0, "两级词数：>17 = 严重违反（== CAP_HARD）"),
    ("G-H9-cutp", r"\*\*可切出标签 ([\d.]+)%\*\*", "metric:cap_cut_pct", 0.1, "标签可切出占比"),
    ("G-H9-cutn", r"可切出标签 [\d.]+%\*\*（(\d+)/662", "metric:cap_n", 0.5, "可切出条数"),
    ("G-H9-ascii", r"\*\*ASCII 冒号 ([\d.]+)%\*\*", "metric:cap_ascii_colon_pct", 0.2, "ASCII 冒号占比"),
    ("G-H9-asciin", r"ASCII 冒号 [\d.]+%\*\*（(\d+)/662", "metric:cap_ascii_colon_n", 0.5, "ASCII 冒号条数"),
    ("G-H9-f3a", r"严格匹配率 \*\*([\d.]+)%\*\*", "metric:cap_f3a_pct", 0.2, "出货 F3a 严格匹配率"),
    ("G-H9-f3an", r"严格匹配率 \*\*[\d.]+%\*\*（(\d+)/662", "metric:cap_f3a_n", 0.5, "出货 F3a 匹配条数"),
    ("G-H9-wmed", r"正文词数中位 (\d+) 词\*\*（p25", "metric:cap_words_med", 0.5, "正文词数中位"),
    ("G-H9-w25", r"词\*\*（p25 (\d+) / p75 \d+）", "metric:cap_words_p25", 0.5, "正文词数 p25"),
    ("G-H9-w75", r"词\*\*（p25 \d+ / p75 (\d+)）", "metric:cap_words_p75", 0.5, "正文词数 p75"),
    ("G-H9-wmax", r"上限 (\d+) 词\*\*（p95）", "metric:cap_words_p95", 0.5, "词数上限 = p95"),
    ("G-H9-whard", r"不超过 (\d+) 词\*\*（max", "metric:cap_words_max", 0.5, "词数上界 = max"),
    ("G-H9-const-max", r"上限 (\d+) 词\*\*（p95）", "const:CS.CAP_MAX", 0, "文档的 12 必须 == 出货常量 CAP_MAX"),
    ("G-H9-const-hard", r"不超过 (\d+) 词\*\*（max", "const:CS.CAP_HARD", 0, "文档的 17 必须 == 出货常量 CAP_HARD"),
    ("G-H9-noper", r"\*\*句末无句号 ([\d.]+)%\*\*", "metric:cap_noperiod_pct", 0.2, "句末无句号占比"),
    ("G-H9-nopern", r"句末无句号 [\d.]+%\*\*（(\d+)/662）", "metric:cap_noperiod_n", 0.5, "句末无句号条数"),
    ("G-H9-empty", r"\*\*空图注 (\d+)/662\*\*", "metric:cap_empty_n", 0.5, "空图注张数"),
    ("G-H9-emptyf3d", r"其中 \*\*(\d+) 张\*\*被 F3d 抓到", "metric:cap_empty_f3d_n", 0.5, "空图注里被 F3d 抓到的张数"),
    ("G-H9-doc873", r"设计稿写 ASCII 冒号 \*\*([\d.]+)%\*\*", "metric:cap_ascii_colon_or_period_pct", 0.2,
     "设计稿 87.3% 的真口径 = 「ASCII 冒号**或**句点」（Important-4 修复）"),
    ("G-H9-578", r"（\*\*(\d+)\*\*/662 = 87\.31%", "metric:cap_ascii_colon_or_period_n", 0.5,
     "更宽口径的条数（572 冒号 + 6 句点）"),
    ("G-H9-6", r"差的 \*\*(\d+) 条\*\*", "metric:cap_ascii_period_n", 0.5,
     "差出来的那几条 = 写成 `Figure N.` 的（正是 F3a 会抓的）"),
    # ---- H11
    ("G-H11-legend", r"\*\*图例判据一致率 ([\d.]+)%\*\*", "metric:legend_agree_pct", 0.1, "图例判据一致率（已证废）"),
    ("G-H11-legendn", r"图例判据一致率 [\d.]+%\*\*（(\d+)/120", "metric:legend_agree_n", 0.5, "图例一致张数"),
    ("G-H11-grid", r"\*\*网格 ([\d.]+)%\*\*", "metric:grid_reading_pct", 0.2, "网格判据读数"),
    ("G-H11-gridn", r"网格 [\d.]+%\*\*（(\d+)/662）", "metric:grid_reading_n", 0.5, "网格判据命中张数"),
    # ---- H12
    ("G-H12-scale-lo", r"正文的 \*\*([\d.]+)–1\.0×\*\*", "const:HM.H12_FONT_SCALE_LO", 0,
     "〔社区〕字号下限 0.8×——**无实测可依**，这里只钉'文档 == 登记常量'（复审 N-8）"),
    ("G-H12-scale-hi", r"正文的 \*\*0\.8–([\d.]+)×\*\*", "const:HM.H12_FONT_SCALE_HI", 0,
     "〔社区〕字号上限 1.0×——同上"),
    ("G-H12-minpt", r"最小 \*\*≥(\d+) pt\*\*", "const:HM.H12_FONT_MIN_PT", 0,
     "〔社区〕字号下限 ≥7 pt——同上（原被整数兜底豁免，Important-2 后必须入表）"),
    ("G-H12-min", r"\*\*最小 ([\d.]+) pt\*\*", "metric:font_est_pt_min", 0.02, "连通域反推字号 min"),
    ("G-H12-max", r"\*\*最大 ([\d.]+) pt\*\*", "metric:font_est_pt_max", 0.02, "连通域反推字号 max"),
    ("G-H12-n", r"（n=(\d+) 抽样", "metric:font_est_n", 0.5, "d9 台账可用张数"),
    # ---- H13
    ("G-H13-band", r"内的只有 \*\*([\d.]+)%\*\*", "metric:h1_band_pct", 0.2, "参照分布自身的合规率（H13 的反例）"),
]

# `provenance.md` 里**散文**中的数的守卫（形态同 GUARDS，文本换成 PROV）。复审 N-7：
# `数:` 行经 `run_prov` 复跑，但**说明性散文数字**（如 P-H2-b 的"差 0.088 in / max 7.19 in"）
# 原先无守卫、也无变异。凡能给出复算仪器的散文数都登记在这里；给不出的必须在条目里写明"无守卫"。
PROV_GUARDS = [
    ("G-P-H2b-max", r"右尾拉高（max ([\d.]+) in）", "metric:h2_colw_p90_max", 0.01,
     "P-H2-b 散文里的右尾 max（均值被它拉高）"),
    ("G-P-H2b-gap", r"⇒ 与中位差 ([\d.]+) in", "metric:h2_colw_p90_gap", 0.001,
     "P-H2-b 散文里的『均值 − 中位』差"),
]

# 未被守卫覆盖的数字必须落在下面**两张**表之一的理由里（否则 CENSUS FAIL）。
#
# 分两张的理由（Important-2 修复）：CENSUS 原先把裸 token 对一张 `(正则, 理由)` 表做 fullmatch，
# 末行曾是一条 `(r"\d+", "@TODO-整数兜底")` —— 它对**任何整数**恒真 ⇒ 文档里新写的整数自动豁免，
# "规范里每个数都有守卫"就退化成自称。现在：
#   · `REASONS`：数字**本体**就无可复算来源的（章节号 / 年份 / 引文读物 / 规则带端点）；
#   · `CONTEXT_REASONS`：数字本体说不清、但**上下文**能说清的（语料路径里的论文号与图号、
#     证据文件的行号引用、侦察报告节号、〔社区〕规则值）——按 token 前后 ±80 字符的窗口匹配。
# 两张表都**不含**万能兜底：写不进去的新整数一律 FAIL。这是本文件"当场点数"承诺的地基。
REASONS = [
    (r"^§\d+$", "章节号（§n）"),
    (r"2025", "样本年份（文件头，样本框架）"),
    (r"1\.19", "比值 max 的**舍入说法**（G-H1-maxb 守 1.189、G-H1-hi 守 1.20）"),
    (r"0\.9|1\.1", "H2 口径分叉用的区间端点 [0.9,1.1)（两个占比由 G-H2-fork-* 守）"),
    (r"2–3", "H3 的规则带本体（样本权重 37.2% 由 G-H3-band 守）"),
    (r"0\.95", "H1 默认档左端（由 G-H1-band-lo 守 0.951）"),
    (r"1\.8", "**引文**：侦察报告记的另一口径读数（**口径未落文**，本任务不引用）"),
]

# 按**上下文**豁免（token 说不清、上下文能说清的）。匹配窗口见末行常量。
CONTEXT_REASONS = [
    (r"项目/", "文档示例里的占位路径"),
    (r"[A-Z]/\d{6,7}/", "语料路径里的**论文号**（如 `C/2505964/…`）"),
    (r"fig-\d+-p\d+\.", "语料文件名里的**图号**（`fig-N-pM`）"),
    (r"baseline `:\d+`", "baseline 证据文件里的**行号引用**（如 `:568`）"),
    (r"侦察报告 §\d+\.\d+", "侦察报告的**节号**（§3.1 / §4.4 / §7.2 / §7.3）"),
    (r"§7\.2 #\d", "侦察报告的小节编号（#3 / #4）"),
    # 三支仪器的**实现常量**（写进文档是为了让人能照着重跑，不是本任务量出来的读数）
    (r"320×320", "出货仪器 `color_count` 的采样尺寸（实现常量，见 `check-figure-style.py`）"),
    (r"//16", "出货仪器 `color_count` 的分箱步长（实现常量）"),
    (r"quantize\((32|64)", "侦察/严判据仪器的量化色数（实现常量，见 `probe_c_color.py`）"),
    (r"(min|max)>=240", "近白判据阈值（实现常量：真侦察仪器用 `max>=240`，baseline 转写用 `min>=240`）"),
]
CONTEXT_WINDOW = 80                              # 上下文豁免的回看/前瞻窗口（字符）


# ------------------------------------------------------- 结构守卫（`chart-types.md`）
# 被验对象是**决策树的形状**，不是实测读数。期望值**分两类，来源不同**：
#   · 入口名（`S1`）= **契约**：九个名字**硬编码在 `ENTRIES`**，是任务书 Interfaces 的产物
#     （Task 5 的 SKILL.md 依赖它）。**不从被验文档现取** —— 现取就等于"改文档即改期望值"，
#     这条判据会退化成恒真（文档写几个就是几个）。
#   · 参照分布数（`S5`）= 从 `house-style.md` **现取**（不抄进脚本）：每个小数必须**归到它同行的
#     `H<n>` 引用**，且**值 ∈ 那个 `H<n>` 条目里的数**。旧写法只查"值 ∈ house-style ∪ provenance 的
#     全局池"（123 个数、含容差常量与别的 H 条目的数）⇒ 把 `1.20`（H1 上限）或 `0.5`（H4 地板）
#     搬到 3D 那条上照样绿。收紧了（变异 `M27`/`M28`）。
# 抽不到即 FAIL（fail-closed）：入口标题抽不到、四段抽不到、radar 那条找不到、小数一个都抽不到
# —— 全都记红。否则"把被守的文本删光"就成了让判据转绿的最短路径。
ENTRIES = ["比较", "分布", "相关", "构成", "时序", "空间", "流程", "机理", "不确定性"]
SEGMENTS = ["你手上是什么数据", "首选图型", "备选", "禁忌"]
ENTRY_RE = re.compile(r"^#{2,}\s*入口\s*\d+\s*·\s*(\S+)\s*$", re.M)
DEF_RE = re.compile(r"^\s*\|?\s*\*\*([A-Za-z0-9\- ]+)\*\*\s*[:：]", re.M)
NUM_RE = re.compile(r"\d+\.\d+")
RADAR_LO = re.compile(r"radar[^\n]*低频|低频[^\n]*radar", re.I)


H_SEC_RE = re.compile(r"^### H(\d+)\..*?$(.*?)(?=^### H\d+\.|\Z)", re.M | re.S)
H_REF_RE = re.compile(r"H(\d+)")


def _h_entries(path):
    """`house-style.md` 的每个 `H<n>` 条目 → 该条目正文里的小数字面量集合（**现取**，不抄写）。"""
    text = path.read_bytes().decode("utf-8")
    return {m.group(1): set(NUM_RE.findall(m.group(2))) for m in H_SEC_RE.finditer(text)}


def _ct_ctx(path):
    """把 `chart-types.md` 解析成各条守卫要的形状（数字与标题全部现取，无一处抄写）。"""
    txt = path.read_bytes().decode("utf-8")
    marks = list(ENTRY_RE.finditer(txt))
    blocks = [(m.group(1),
               txt[m.start():marks[i + 1].start() if i + 1 < len(marks) else len(txt)])
              for i, m in enumerate(marks)]
    nums = sorted(set(NUM_RE.findall(txt)))
    ents = _h_entries(DOC)          # `house-style.md` 的 `H<n>` → 该条目的数（现取）
    return txt, [m.group(1) for m in marks], blocks, nums, ents


def _s1(cx):
    """九个入口名齐全：标题恰九条、名字恰是**契约**里那九个（缺一、多一、重名都红）。

    **期望值不是从被验文档现取的** —— 是任务书 Interfaces 定的那九个（`ENTRIES`）。若改成
    "从文档现取"，这条判据就退化成恒真（文档写几个就是几个）；见模块头第 5 条。
    """
    _txt, heads, _blocks, _nums, _ents = cx
    missing = [e for e in ENTRIES if e not in heads]
    dup = len(heads) - len(set(heads))
    return (len(heads) == len(ENTRIES) and not missing and dup == 0,
            f"入口标题 {len(heads)} 个（应 {len(ENTRIES)}）· 缺 {missing or '无'} · 重名 {dup}")


def _s2(cx):
    """每入口四段齐全：`你手上是什么数据` / `首选图型` / `备选` / `禁忌` 逐段在**该入口的块内**。"""
    _txt, _heads, blocks, _nums, _ents = cx
    short = []
    for name, blk in blocks:
        miss = [s for s in SEGMENTS if f"**{s}**" not in blk]
        if miss:
            short.append(f"{name} 缺 {'/'.join(miss)}")
    ok = len(blocks) == len(ENTRIES) and not short
    return (ok, f"四段齐全的入口 {len(blocks) - len(short)}/{len(ENTRIES)}"
                + ("" if not short else " · " + "；".join(short)))


def _s3(cx):
    """radar 立类但**标低频** —— 且要标在 **radar 的那条定义行**（名册里的 `**radar chart**: …`）上。

    为什么不扫"随便哪一行"：只扫全文会让**顺带提到** radar 的行（如某个入口的备选里
    "`radar chart`（**低频**，见名册）"）替定义行顶包 —— 定义行上的标注被删掉，判据照样绿。
    （任务书给的正则正是全文扫的那种；驱动器 `M24` 的 NOTE 记了这次收紧。）
    """
    txt = cx[0]
    hit = ""
    for line in txt.splitlines():
        m = DEF_RE.match(line)
        if m and m.group(1).strip().lower() == "radar chart":
            hit = line.strip()
            break
    ok = bool(hit) and bool(RADAR_LO.search(hit))
    return (ok, "radar 定义行：" + (f"『{hit[:52]}…』{'带' if RADAR_LO.search(hit) else '**不带**'}『低频』"
                                   if hit else "**找不到**（fail-closed）"))


def _s4(cx):
    """★ **读数条，不是判据**：只印定义行数 / 不同名数 / 重名的名字，**不进 `bad`**。

    例外出口（写实，别当成"永不可能红"）：`chart-types.md` **读不出/解析失败**时（`_ct_ctx` 抛），
    `main()` 的 fail-closed 段会把 `S4` 与其余结构守卫**一起**记红并计入 `n_guard` —— 读不出就该全红。

    为什么不做成判据：这一条**没有可失败的谓词**——"计数 > 0"对任何有定义的文档都真，
    而"计数 == 期望值"得把一个**没有外部契约、只属于本文档**的计数抄进脚本（`S1` 的入口名不同：
    那是任务书 Interfaces 的契约，见模块头第 5 条）⇒ 只能由人看一眼。
    把它写成判据，就又是一条"看着能红、实则恒真"的判据（见模块头第 5 条）。
    """
    names = DEF_RE.findall(cx[0])
    dup = sorted({n for n in names if names.count(n) > 1})
    return (None, f"定义行 {len(names)} · 不同名 {len(set(names))} · 重名 {dup or '无'}"
                  "（读数条：不参与 PASS/FAIL，重名由人看一眼）")


def _s5(cx):
    """参照分布数不许漂：`chart-types.md` 里**每个**小数都要**归到它同行的 `H<n>` 引用**，
    且**值 ∈ 那个 `H<n>` 条目里的数**（`house-style.md` 的那一条，现取）。

    两条红法：
      · **跨条目搬数**：`1.20` 是 H1 的数、`0.5` 是 H4 的地板 —— 写成 H7 那条上的数即红
        （旧写法只查"值 ∈ house-style ∪ provenance 的全局池"=123 个数，这两条**都会漏**）；
      · **无所属的小数**：同行找不到 `H<n>` ⇒ 红（fail-closed：没人能复核它抄自哪一条）。

    **一个数都没有也红**——否则"把数全删掉"是最省事的转绿路径（fail-closed）。
    这条**不判"这个数本身对不对"**（那由 `G-*` 管），只判"**抄过去之后有没有被改 / 有没有搬错条目**"。
    **射程**：只管小数（`\\d+\\.\\d+`）；`chart-types.md` 里的**整数**没有机械守卫（明写在案，
    见该文件 §0 第 2 条与 Task 4 报告 §5.5）。
    """
    txt, _heads, _blocks, nums, ents = cx
    drift, unref, n_occ = [], [], 0
    for line in txt.splitlines():
        refs = list(H_REF_RE.finditer(line))
        for m in NUM_RE.finditer(line):
            n_occ += 1
            before = [r for r in refs if r.start() < m.start()]
            ref = before[-1] if before else (refs[0] if refs else None)
            if ref is None:
                unref.append(m.group(0))
                continue
            hid = ref.group(1)
            if m.group(0) not in ents.get(hid, set()):
                drift.append(f"{m.group(0)}∉H{hid}")
    ok = bool(n_occ) and not drift and not unref
    return (ok,
            f"小数出现 {n_occ} 处（不同值 {nums or '**一个都没有 ⇒ fail-closed 记红**'}）· "
            f"与所属 H 条目不同值者 {drift or '无'} · 无所属 `H<n>` 者 {unref or '无'}")


# (id, 断言函数, 说明) —— 与 `GUARDS` 同一表驱动结构；`S4` 的断言函数恒返回 `ok=None`（读数条）
STRUCT_GUARDS = [
    ("S1", _s1, "九个入口名齐全（题名**恰等于契约 `ENTRIES`**；缺一 / 多一 / 重名即红）"),
    ("S2", _s2, "每个入口下四段齐全（你手上是什么数据 / 首选图型 / 备选 / 禁忌）"),
    ("S3", _s3, "radar 条目带『低频』标注（同行找不到即红）"),
    ("S4", _s4, "图型名重复定义 —— **读数条，不是判据**（只印计数；唯一红法是该文件读不出）"),
    ("S5", _s5, "参照分布数不漂（每个小数**归到同行 `H<n>`** 且 ∈ 该条目的数；无所属 / 一个数都没有也红）"),
]


# ------------------------------------------------------- SKILL.md 守卫（Task 5）
# 被验对象 = `.claude/skills/mcm-figure-choose/SKILL.md`（**短契约**）。与结构守卫同一形状，
# 期望值来源**分两类**，别把它们搞混：
#   · **契约型（硬编码）**：行数上限 `SK_MAX_LINES`、指针路径 `SK_POINTER`、入口名 `ENTRIES`
#     （九个名字是任务书 Interfaces 的契约，**不从被验文档现取** —— 现取即"改文档即改期望值"，
#     判据退化成恒真，同模块头第 5 条）；
#   · **现取型**：禁止串（`house-style.md` 里的小数与 `≤n` 形态，**现取**，不抄进脚本）——
#     这正是本文件存在的理由：SKILL.md **不许重述任何规范数值**（重述即造第二份权威）。
# 抽不到即 FAIL（fail-closed）：SKILL.md 读不出 / 禁止串一条都抽不到 / 全文一个数都没有 →
# 全都记红，否则"把被守的文本删光"或"把规范数值删光"就成了让判据转绿的路径。
SK_MAX_LINES = 150
SK_POINTER = "references/house-style.md"
SK_STRUCT_MARK = "结构性计数"          # 声明行标记：**显式声明哪些是结构性计数**（Task 5 controller 第 4 条）
SK_NUM_RE = re.compile(r"\d+(?:\.\d+)?")
SK_ID_RE = re.compile(r"H\s*\d+")      # 规则编号（`H1`…`H13`）—— 指针型 ID，不算"数"
SK_PLOT_RE = re.compile(r"mcm-plot-[a-z]+")
SK_BUILD_MARK = "〔拟建〕"              # 点名**不存在**的 skill 必须带这个标记（Task 5 controller 第 1 条）
SKILLS_ROOT = ROOT / ".claude/skills"  # `K6` 判"这个 skill 到底存不存在"的根（`--skills-root` 可换）

# ---- `K3` 的中文数词臂（复审 Important-1：主臂只认 ASCII/全角数字，"主色四色以内"能整句走绿）
SK_CN_DIGITS = "零一二三四五六七八九"
SK_CN_NUM_RE = re.compile(r"[一二三四五六七八九十百两]+")
# **规范单位词表**：`(中文写法, 它在 house-style.md 里的出处串)`。硬编码，但逐条**锚验** ——
# 每个出处串都必须在 `house-style.md` 里找得到，缺一即红（fail-closed：词表是抄的，出处都没了
# 就是在守空气）。为什么不把单位词也现取：现取只能取到"紧跟在数字后面的那个字"，而规范里
# `≤4 色` 常常写成 `≤4，单色…`（单位词不紧邻）⇒ 现取会**抽空**；数值那一侧才是现取的。
SK_CN_UNITS = (("色", "色"), ("词", "词"), ("磅", "pt"), ("倍", "×"), ("英寸", "in"),
               ("像素", "像素"), ("分箱", "分箱"), ("面板", "面板"), ("子图", "子图"))
SK_CN_BARE_MIN = 4                     # 裸值臂的**下界**：中文的 一/两/二/三 兼作泛量词（写实口径）
# 裸值臂的**阈值标记**（"规范阈值"在这份文档里的几种写法，全部现取）：
SK_CN_TIER_RES = (r"≤\s*(\d+)", r"≥\s*(\d+)", r"上限\s*\*{0,2}\s*(\d+)",
                  r"下限\s*\*{0,2}\s*(\d+)", r"不超过\s*\*{0,2}\s*(\d+)", r"<\s*(\d+)\s*词")

# ---- `K4`/`K5`：`SKILL.md` 自己那张**决策树入口表**（入口数与标签的锚）
SK_TABLE_ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|")
# ---- `K7`：五段标题与输出契约三件套（复审 N-3）
SK_SECTIONS = ("什么时候用", "决策树", "输出契约", "边界", "指针")
SK_CONTRACT_ITEMS = ("**推荐图型**", "**理由**", "**设计要点**")
# ---- `K8`：`SKILL.md` 的断言「`house-style.md` 逐条标了验证状态」要成立（复审 N-7）
SK_VERIFY_RE = re.compile(r"\*\*验证\*\*\s*[：:]")


def _strip_ids(txt):
    """去掉 `H<n>` 形式的规则编号：它们是指针型 ID，不是"数"。"""
    return SK_ID_RE.sub("", txt)


def _cn_int(n):
    """整数 → 中文数词（0–99；超出返回 `None`：**百位以上的中文写法本层不判**，写实口径）。"""
    if not 0 <= n <= 99:
        return None
    if n < 10:
        return SK_CN_DIGITS[n]
    if n < 20:
        return "十" + (SK_CN_DIGITS[n % 10] if n % 10 else "")
    return SK_CN_DIGITS[n // 10] + "十" + (SK_CN_DIGITS[n % 10] if n % 10 else "")


def _sk_table_entries(txt):
    """`SKILL.md` 那张**决策树入口表**的行标签（全文唯一一张表：`| **入口** | 用户的那句话 |`）。"""
    return [m.group(1).strip() for l in txt.splitlines() if (m := SK_TABLE_ROW_RE.match(l))]


def _sk_sections(txt):
    """按 `## ` 分节 → `{标题: 正文}`（同一标题出现多次时正文合并）。"""
    out = {}
    cur = None
    for l in txt.splitlines():
        if l.startswith("## "):
            cur = l[3:].strip()
            out.setdefault(cur, [])
        elif cur is not None:
            out[cur].append(l)
    return {h: "\n".join(b) for h, b in out.items()}


def _k1(txt):
    """短契约的硬上限：**行数 < 150**（含 frontmatter 与空行，按 `splitlines()` 数）。"""
    n = len(txt.splitlines())
    return (n < SK_MAX_LINES, f"行数 {n}（上限：<{SK_MAX_LINES}）")


def _k2(txt):
    """指向 `house-style.md` 的指针**必须**存在，且要写成 **skill 目录内的相对路径**
    `references/house-style.md`（Task 7 的检查器核的就是这个形态；只写文件名不算）。"""
    ok = SK_POINTER in txt
    n = txt.count(SK_POINTER)
    return (ok, f"指针 `{SK_POINTER}` 出现 {n} 处（必须 ≥1；只写 `house-style.md` 不算）")


def _cn_arm(doc, txt):
    """`K3` 的**中文数词臂**：规范值**用中文数词写出来**同样是重述。

    两臂（数值都**现取**自同一份 `house-style.md`）：
      · **裸值臂**：**阈值标记**（`≤` / `≥` / `上限` / `下限` / `不超过` / `<n 词`）后面那个整数值
        （**现取**）中 ≥ `SK_CN_BARE_MIN` 者的**中文写法** —— "**四**"（`≤4 色` ⇒ "主色不超过四"）·
        "**七**"（`≥7 pt`）· "**十二**" / "**十七**"（词数上限）。
        为什么从 4 起：中文里 一 / 两 / 二 / 三 兼作泛量词（"一个首选" / "走三步"），不携带阈值信息。
        **写实口径（不是已覆盖）**：这条臂只到 99，且"不超过三个主色"这类 **1–3 的中文写法不在射程内**。
      · **单位词臂**：中文数词**紧跟**一个规范单位词（`SK_CN_UNITS`，含同义写法 磅←`pt`、倍←`×`、
        英寸←`in`）—— "四色以内" / "一倍正文宽" / "七磅"。词表硬编码，故逐条**锚验出处**：
        `house-style.md` 里找不到那条出处 ⇒ 这条臂记红（fail-closed）。
    裸值一条都抽不到（阈值标记全没了）也记红 —— 与主臂同一口径（`M34` 那类）。

    ★ 两臂**都只认字面**：判不了"这句话是不是在复述规范"——措辞层仍是判断层的事（同 `S4`）。
    """
    units_ok = [cn for cn, src in SK_CN_UNITS if src in doc]
    units_missing = [f"{cn}（出处 {src!r}）" for cn, src in SK_CN_UNITS if src not in doc]
    tiers = {int(v) for p in SK_CN_TIER_RES for v in re.findall(p, doc)}
    bare = sorted({w for w in (_cn_int(v) for v in tiers if v >= SK_CN_BARE_MIN) if w})
    bare_hits = sorted(b for b in bare if b in txt)
    unit_hits = []
    if units_ok:
        ure = re.compile("|".join(sorted(units_ok, key=len, reverse=True)))
        for m in SK_CN_NUM_RE.finditer(txt):
            um = ure.match(txt, m.end())            # 紧跟（不许中间夹字）
            if um:
                unit_hits.append(m.group(0) + um.group(0))
    unit_hits = sorted(set(unit_hits))
    ok = bool(bare) and not units_missing and not bare_hits and not unit_hits
    return ok, (f"中文数词臂：裸值词 {bare or '**一条都抽不到 ⇒ fail-closed 记红**'}"
                f"（由阈值标记现取，≥{SK_CN_BARE_MIN}）· "
                f"单位词 {len(units_ok)}/{len(SK_CN_UNITS)} 条出处都在"
                + ("" if not units_missing else f"（**缺 {units_missing} ⇒ 红**）")
                + f" · 中文命中 {sorted(set(bare_hits + unit_hits)) or '无'}")


def _k3(txt):
    """**不许重述任何规范数值** —— 两道**并行**的臂，都要绿：

    ① **主臂（现取禁止串）**：从 `house-style.md` 现抽小数字面量与 `≤n` / `<n 词` 形态，
       命中即 FAIL；**抽不到任何禁止串也 FAIL**（fail-closed：规范里一个数都没有 ⇒ 判据无从谈起）。
    ② **中文数词臂**（`_cn_arm`）：规范值用中文数词写出来同样是重述 —— 口径见那个函数的 NOTE。

    ★ **射程写实（别把两臂读成"覆盖了所有复述手法"）**：主臂只认小数与 `≤n` / `<n 词`；中文臂只认
    "规范单位词紧跟中文数词"与"≥4 的规范整数值的中文写法"。**1–3 的中文写法、百位以上、以及
    "这句话是不是在复述规范"本身，都不在本条的机械射程内**（不是"另有某条兜住"，是**判断层的事**，
    同 `S4`：机械判不了，就只能由人看一眼）。
    """
    doc = DOC.read_bytes().decode("utf-8")
    banned = set(re.findall(r"\d+\.\d+", doc)) | set(re.findall(r"≤\s*\d+|<\s*\d+\s*词", doc))
    hits = sorted(b for b in banned if b in txt)
    ok1 = bool(banned) and not hits
    ok2, d2 = _cn_arm(doc, txt)
    return (ok1 and ok2,
            f"禁止串 {len(banned)} 条（现取）· 命中 {hits or '无'}"
            + ("" if banned else " ⇒ **一条都抽不到 ⇒ fail-closed 记红**")
            + " · " + d2)


def _k4(txt):
    """九个入口名**全部**出现，**且** `SKILL.md` 自己那张决策树表的行标签**恰等于**契约 `ENTRIES`
    （缺一 / 多一 / 改名 / 次序不符都红）。期望值是契约，**不从 `chart-types.md` 现取**。

    为什么连那张表一起判（复审 N-4）：只查"九个名字在全文某处出现过"时，**往表里多加一行**
    （等于多一个入口）照样绿 —— 而那张表就是 SKILL.md 自己的入口契约。
    """
    missing = [e for e in ENTRIES if e not in txt]
    rows = _sk_table_entries(txt)
    extra = [r for r in rows if r not in ENTRIES]
    ok = not missing and rows == ENTRIES
    detail = (f"入口名缺 {missing or '无'}（契约 {len(ENTRIES)} 个，全部出现）· "
              f"决策树表 {len(rows)} 行")
    if rows != ENTRIES:
        detail += f" ⇒ **表行标签 ≠ 契约**（多出/改名/次序 {extra or '无'}；契约 {ENTRIES}）"
    return ok, detail


def _k5(txt):
    """**数字的处置**：除 `H<n>` 编号外，全文每个数都必须**已被显式声明为结构性计数**。

    四条一起判（缺一条这条守卫就漏）：
      ① 声明行（含 `结构性计数`）必须存在 —— fail-closed；
      ② 声明行上抽到的数集 = 全文被许可的数集（**按值许可**，故声明一次即全文通用）；
      ③ **入口数（`len(ENTRIES)`，契约值）必须在声明里**；
      ④ **声明行上不许出现别的数**（白名单**恰** `{len(ENTRIES)}`，契约值）—— 旧写法下
         "把数写进声明那一行"就是洗白任意整数的路径（复审 N-2：把 `4`（H4 的规范值）写进
         声明行，`K3` 与 `K5` 都判绿）；白名单钉到契约上，声明就不再是自证的；
      ⑤ 声明的入口数必须 **== `SKILL.md` 自己那张决策树表的行数**（复审 N-4）—— 声明里的
         "入口数"不许只对契约、不对文档；往表里加一行而声明不改，直接红。
    """
    decl = [l for l in txt.splitlines() if SK_STRUCT_MARK in l]
    declared = {n for l in decl for n in SK_NUM_RE.findall(_strip_ids(l))}
    undeclared = sorted(set(SK_NUM_RE.findall(_strip_ids(txt))) - declared)
    need = str(len(ENTRIES))
    extra = sorted(declared - {need})
    rows = _sk_table_entries(txt)
    ok = (bool(decl) and need in declared and not extra and not undeclared
          and len(rows) == len(ENTRIES))
    return (ok, f"声明行 {len(decl)} 行（含『{SK_STRUCT_MARK}』）· 声明到的数 {sorted(declared) or '**无**'}"
                f"（白名单只许 [{need}]，多出 {extra or '无'}）· "
                f"入口数 {need} {'已在声明里' if need in declared else '**不在声明里**'} · "
                f"决策树表 {len(rows)} 行（应 {len(ENTRIES)}）· 未声明的数 {undeclared or '无'}"
                + ("" if decl else " ⇒ **没有声明行 ⇒ fail-closed 记红**"))


def _k6(txt):
    """**点名不存在的 skill 必须标〔拟建〕** —— 判的是**双向**（复审 N-5）：

    ① 边界段**真的点了名**（一个绘图 skill 都不点名 = 边界没交接出去 ⇒ 红，
       否则"不点名"就成了这条判据的转绿路径）；
    ② **不存在**的 skill：每一处点名所在行都要带〔拟建〕；
    ③ **存在**的 skill：**不许**带〔拟建〕—— 只判单向的话，等 `mcm-plot-python` 真建出来那天，
       这条守卫会**强制保留一个已不成立的〔拟建〕**。
    存在性判的是 `SKILLS_ROOT / <名字>`（`--skills-root` 可换，变异 `M40` 用它证反向臂会红）。
    """
    names = sorted(set(SK_PLOT_RE.findall(txt)))
    rows = []
    for n in names:
        lines = [l for l in txt.splitlines() if SK_PLOT_RE.search(l) and n in l]
        rows.append((n, (SKILLS_ROOT / n).exists(), all(SK_BUILD_MARK in l for l in lines)))
    fake = [n for n, exists, marked in rows if exists == marked]   # 标记与事实不符（含"不存在却没标"）
    ok = bool(names) and not fake
    return (ok, "点名的绘图 skill "
                + ("、".join(f"{n}（{'存在' if e else '不存在'}·{'标了〔拟建〕' if m else '未标〔拟建〕'}"
                             f"{'⇒**标记与事实不符**' if e == m else ''}）" for n, e, m in rows)
                   or "**一个都没有 ⇒ fail-closed 记红**")
                + f" · 标记与事实不符的 {fake or '无'}")


def _k7(txt):
    """**五段标题齐全 + 输出契约三件套落在该段里**（复审 N-3）。

    任务书 Step 1 的五段必含项里，「什么时候用」与「输出契约」**没有任何别的机械守卫**
    —— 把这两段整段删掉，`K1`–`K6` 照样全绿（实测），而**输出契约正是本 skill 的核心交付面**
    （推荐图型 / 理由 / 设计要点 ⇒ 逐条写成 `要点 → H<n>`）。
    """
    secs = _sk_sections(txt)
    missing = [s for s in SK_SECTIONS if not any(s in h for h in secs)]
    body = "\n".join(b for h, b in secs.items() if "输出契约" in h)
    noitem = [i.strip("*") for i in SK_CONTRACT_ITEMS if i not in body]
    ok = not missing and not noitem
    return (ok, f"五段标题缺 {missing or '无'}（共 {len(SK_SECTIONS)} 段）· "
                f"输出契约段内三件套缺 {noitem or '无'}")


def _k8(_txt):
    """`SKILL.md` 的断言「`house-style.md` **逐条**标了验证状态」必须成立 ⇒ **逐条核**（复审 N-7）：
    `house-style.md` 每个 `### H<n>.` 条目里**恰有一行** `**验证**：`（缺 / 多都红）。
    一个 `H` 条目都抽不到也红（fail-closed）——否则"把被断言的文本删光"就成了转绿路径。
    """
    doc = DOC.read_bytes().decode("utf-8")
    blocks = list(H_SEC_RE.finditer(doc))
    miss = [f"H{m.group(1)}（{len(SK_VERIFY_RE.findall(m.group(2)))} 行）" for m in blocks
            if len(SK_VERIFY_RE.findall(m.group(2))) != 1]
    ok = bool(blocks) and not miss
    return (ok, f"`### H<n>.` 条目 {len(blocks)} 个 · 没有恰一行『**验证**：』的 {miss or '无'}"
                + ("" if blocks else " ⇒ **一个条目都抽不到 ⇒ fail-closed 记红**"))


# (id, 断言函数, 说明) —— 与 `STRUCT_GUARDS` 同一表驱动结构
SKILL_GUARDS = [
    ("K1", _k1, f"短契约行数 <{SK_MAX_LINES}（硬上限，按 `splitlines()` 数）"),
    ("K2", _k2, f"指针 `{SK_POINTER}` 必须存在（skill 目录内相对路径）"),
    ("K3", _k3, "不重述规范数值（ASCII 禁止串**现取** + **中文数词臂**；命中 / 抽不到都红）"),
    ("K4", _k4, "九个入口名齐 + 决策树表的行标签**恰等于**契约 `ENTRIES`"),
    ("K5", _k5, "数字必须声明为结构性计数，且声明行只许出现契约数、入口数须 == 表行数"),
    ("K6", _k6, "点名的绘图 skill：存在性与〔拟建〕标记必须**一致**（双向）"),
    ("K7", _k7, "五段标题齐全 + 输出契约三件套落在该段里"),
    ("K8", _k8, "`house-style.md` 每个 `H<n>` 条目恰有一行『**验证**：』（SKILL.md 的断言要成立）"),
]


def prov_blocks(text):
    out = []
    for m in re.finditer(r"^### (P-[\w-]+) · ([^\n]*)\n(.*?)(?=^### |\Z)", text, re.M | re.S):
        out.append((m.group(1), m.group(2), m.group(3)))
    return out


def field(block, name):
    m = re.search(rf"^{name}:\s*(.+)$", block, re.M)
    return m.group(1).strip() if m else None


def run_prov(pid, block):
    """按 provenance 里那条命令**原样跑一遍**，取回它打出的读数。"""
    num, tol, cmd = field(block, "数"), field(block, "容差"), field(block, "复跑命令")
    if num is None or tol is None or cmd is None:
        return False, "缺 数/容差/复跑命令 三者之一（fail-closed）"
    if num.startswith("无") or cmd.startswith("无"):
        ok = num.startswith("无") and cmd.startswith("无")
        return ok, f"无数条目：数={num[:12]!r} 命令={cmd[:12]!r}（两者必须同时以『无』开头）"
    met = re.findall(r"--metric\s+([A-Za-z_]\w*)", cmd)
    if len(met) != 1:
        return False, f"命令里 `--metric` 命中 {len(met)} 次（必须恰 1，fail-closed）：{cmd}"
    toks = cmd.split()
    if not (toks[0] == "python" and toks[1].endswith("house-metrics.py")):
        return False, f"命令不是 `python …/house-metrics.py` 形态（fail-closed）：{cmd}"
    p = subprocess.run([sys.executable, cmd.split()[1], *cmd.split()[2:]],
                       capture_output=True, text=True, cwd=str(ROOT))
    line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    m = re.match(r"^([A-Za-z_]\w*) = (.+)$", line)
    if p.returncode != 0 or not m:
        return False, f"命令失败 rc={p.returncode} out={line[:60]!r}"
    # 打出来的**名册名必须与命令里那条 `--metric` 一致**：只认 `name = value` 的形态时，
    # 「指错 metric、但数值恰好相同」的条目会静默通过（复审 N-7）。
    if m.group(1) != met[0]:
        return False, (f"输出名册名 {m.group(1)!r} ≠ 命令里的 --metric {met[0]!r}"
                       f"（fail-closed：防止『指错 metric 而数值巧合相同』）")
    got = m.group(2).strip()
    try:
        ok = abs(float(got) - float(num)) <= float(tol)
    except ValueError:
        ok = (got == num)
    return ok, f"文档={num} 命令={got} 容差={tol}（{met[0]}）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--no-provenance", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--doc", default=None)          # 变异驱动器用：指向被改坏的副本（默认 = 真件）
    ap.add_argument("--prov", default=None)
    ap.add_argument("--ct", default=None)           # 同上：指向被改坏的 `chart-types.md` 副本
    ap.add_argument("--skill", default=None)        # 同上：指向被改坏的 `SKILL.md` 副本
    ap.add_argument("--skills-root", default=None)  # `K6` 的存在性根（默认 = 仓内 `.claude/skills`）
    a = ap.parse_args()
    global DOC, PROV, CT, SK, SKILLS_ROOT
    if a.doc:
        DOC = pathlib.Path(a.doc)
    if a.prov:
        PROV = pathlib.Path(a.prov)
    if a.ct:
        CT = pathlib.Path(a.ct)
    if a.skill:
        SK = pathlib.Path(a.skill)
    if a.skills_root:
        SKILLS_ROOT = pathlib.Path(a.skills_root)
    if a.list:
        for gid, pat, src, tol, note in GUARDS + PROV_GUARDS:
            print(f"{gid}\t{src}\t{note}")
        print("--- 结构守卫（chart-types.md）---")
        for sid, _fn, note in STRUCT_GUARDS:
            print(f"{sid}\t(struct)\t{note}")
        print("--- SKILL.md 守卫（短契约）---")
        for kid, _fn, note in SKILL_GUARDS:
            print(f"{kid}\t(skill)\t{note}")
        print("--- provenance ---")
        for pid, title, _b in prov_blocks(PROV.read_bytes().decode("utf-8")):
            print(f"{pid}\t{title}")
        return 0

    dup = [k for k, v in collections.Counter(
        [g[0] for g in GUARDS + PROV_GUARDS] + [g[0] for g in STRUCT_GUARDS]
        + [g[0] for g in SKILL_GUARDS]).items() if v > 1]
    if dup:
        print(f"FAIL  IDUNIQ  守卫 id 重名：{dup}（变异断言会打错目标 ⇒ fail-closed）")
        return 1

    text = DOC.read_bytes().decode("utf-8")
    reg = HM._reg()
    want = set(a.only) if a.only else None
    bad, spans, rows = [], [], []
    guard_vals = set()
    n_guard = n_prov = 0

    for gid, pat, src, tol, note in GUARDS:
        if want and gid not in want:
            continue
        n_guard += 1
        hits = list(re.finditer(pat, text))
        if len(hits) != 1:
            bad.append(gid)
            print(f"FAIL  {gid:<18} 文档正则命中 {len(hits)} 处（必须恰 1）：{pat}")
            continue
        spans.append(hits[0].span())
        docval = hits[0].group(1)
        try:
            guard_vals.add(float(docval))
        except ValueError:
            guard_vals.add(docval)
        kind, arg = src.split(":", 1)
        try:
            if kind == "metric":
                got = reg[arg][0]()
            elif kind == "const":
                mod, attr = arg.split(".")
                got = getattr(CONSTS[mod], attr)
            else:
                got = reg[arg][0]()
        except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
            bad.append(gid)
            print(f"FAIL  {gid:<18} 现算失败：{type(e).__name__}: {e}")
            continue
        ok = (docval == str(got)) if isinstance(got, str) else (abs(float(docval) - float(got)) <= tol)
        bad += [] if ok else [gid]
        shown = got if isinstance(got, str) else f"{float(got):g}"
        rows.append((ok, f"{'PASS' if ok else 'FAIL'}  {gid:<18} 文档={docval:<8} 实测={shown:<9} "
                         f"容差={tol:<7g} {note}"))

    prov_rows = []
    if not a.no_provenance:
        # ---------------- PROV_GUARDS：provenance.md **散文**里的数（不经 run_prov 的那些）
        pv_text = PROV.read_bytes().decode("utf-8")
        for pvid, pvpat, pvsrc, pvtol, pvnote in PROV_GUARDS:
            if want and pvid not in want:
                continue
            n_guard += 1
            ph = list(re.finditer(pvpat, pv_text))
            if len(ph) != 1:
                bad.append(pvid)
                rows.append((False, f"FAIL  {pvid:<18} provenance.md 正则命中 {len(ph)} 处"
                                    f"（必须恰 1）：{pvpat}"))
                continue
            pdocval = ph[0].group(1)
            pk, parg = pvsrc.split(":", 1)
            try:
                pgot = getattr(CONSTS[parg.split(".")[0]], parg.split(".")[1]) if pk == "const" \
                    else reg[parg][0]()
            except Exception as e:                                 # noqa: BLE001（fail-closed 出口）
                bad.append(pvid)
                rows.append((False, f"FAIL  {pvid:<18} 现算失败：{type(e).__name__}: {e}"))
                continue
            pok = (pdocval == str(pgot)) if isinstance(pgot, str) \
                else (abs(float(pdocval) - float(pgot)) <= pvtol)
            bad += [] if pok else [pvid]
            pshown = pgot if isinstance(pgot, str) else f"{float(pgot):g}"
            rows.append((pok, f"{'PASS' if pok else 'FAIL'}  {pvid:<18} 文档={pdocval:<8} "
                              f"实测={pshown:<9} 容差={pvtol:<7g} {pvnote}"))

        blocks = [b for b in prov_blocks(PROV.read_bytes().decode("utf-8"))
                  if want is None or b[0] in want]
        with ThreadPoolExecutor(6) as ex:
            res = list(ex.map(lambda b: run_prov(b[0], b[2]), blocks))
        for (pid, title, _b), (ok, detail) in zip(blocks, res):
            n_prov += 1
            prov_rows.append(f"{'PASS' if ok else 'FAIL'}  {pid:<12} {detail}")
            bad += [] if ok else [pid]

    for ok, line in rows:
        print(line)

    # ---------------- 结构守卫（Task 4）：`chart-types.md` 的形状
    n_struct = 0
    struct_rows = []
    if want is None or any(sid in want for sid, _f, _n in STRUCT_GUARDS):
        try:
            scx = _ct_ctx(CT)
        except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
            # 读不出 ⇒ **连读数条 `S4` 一起记红**（与"`S4` 不进 bad"不矛盾：读不出就没有读数可言，
            # 且此时 `S4` 无法印出任何东西，放它过去等于把"文件挂了"读成"没有重名"）。
            scx = None
            for sid, _fn, _note in STRUCT_GUARDS:
                if want and sid not in want:
                    continue
                n_guard += 1
                n_struct += 1
                bad.append(sid)
                struct_rows.append(f"FAIL  {sid:<18} chart-types.md 读不出/解析失败："
                                   f"{type(e).__name__}: {e}（fail-closed）")
        if scx is not None:
            for sid, fn, _note in STRUCT_GUARDS:
                if want and sid not in want:
                    continue
                sok, sdetail = fn(scx)
                if sok is None:                     # 读数条（`S4`）：只印，恒不进 bad
                    struct_rows.append(f"READ  {sid:<18} {sdetail}")
                    continue
                n_guard += 1
                n_struct += 1
                bad += [] if sok else [sid]
                struct_rows.append(f"{'PASS' if sok else 'FAIL'}  {sid:<18} {sdetail}")
        print("-" * 78)
        print("结构守卫（chart-types.md 的形状；S4 是**读数条**，不参与判词"
              "——除非 chart-types.md 读不出，那时它随其余结构守卫一起记红）")
        for r in struct_rows:
            print(r)

    # ---------------- SKILL 守卫（Task 5）：`SKILL.md` 的短契约
    n_skill = 0
    skill_rows = []
    if want is None or any(kid in want for kid, _f, _n in SKILL_GUARDS):
        try:
            ktxt = SK.read_bytes().decode("utf-8")
        except Exception as e:                                     # noqa: BLE001（fail-closed 出口）
            # 读不出 ⇒ 全部记红（与结构守卫同一出口：没有文件就没有"契约守住了"可言）
            ktxt = None
            for kid, _fn, _note in SKILL_GUARDS:
                if want and kid not in want:
                    continue
                n_guard += 1
                n_skill += 1
                bad.append(kid)
                skill_rows.append(f"FAIL  {kid:<18} SKILL.md 读不出/解析失败："
                                  f"{type(e).__name__}: {e}（fail-closed）")
        if ktxt is not None:
            for kid, fn, _note in SKILL_GUARDS:
                if want and kid not in want:
                    continue
                kok, kdetail = fn(ktxt)
                n_guard += 1
                n_skill += 1
                bad += [] if kok else [kid]
                skill_rows.append(f"{'PASS' if kok else 'FAIL'}  {kid:<18} {kdetail}")
        print("-" * 78)
        print("SKILL.md 守卫（短契约：行数 < 上界 / 指针 / 不复述规范数值（ASCII + 中文数词） / "
              "九入口（含决策树表） / 数字声明 / 点名拟建的存否 / 五段+输出契约三件套 / "
              "逐条验证行）")
        for r in skill_rows:
            print(r)

    if prov_rows:
        print("-" * 78)
        print("provenance 复跑（命令按文档原样起子进程，cwd = 仓根）")
        for r in prov_rows:
            print(r)

    # ---------------- IDCHECK：文档里点名的守卫/P 条目必须真的存在
    ids = {g[0] for g in GUARDS + PROV_GUARDS} | {b0[0] for b0 in
                                                  prov_blocks(PROV.read_bytes().decode("utf-8"))}
    bad_ids = []
    for m in re.finditer(r"([GP]-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)", text):
        tok = m.group(1)
        if tok in ids or any(i.startswith(tok + "-") for i in ids):
            continue
        bad_ids.append(tok)
    if bad_ids:
        bad += bad_ids
        print(f"FAIL  IDCHECK  文档点名了不存在的守卫/条目：{','.join(sorted(set(bad_ids)))}")
    else:
        print(f"PASS  IDCHECK  文档点名的守卫/P 条目全部存在（族前缀 {len(ids)} 条）")

    # ---------------- CENSUS：文档里每个数字都得有守卫或理由
    census_bad, unlisted = [], []
    if not want:
        covered = set()
        for s, e in spans:
            covered.update(range(s, e))
        hits = list(re.finditer(r"(?<![\w.])\d+(?:\.\d+)?(?![\w])", text))
        n_dup = n_ctx = 0
        for m in hits:
            if any(i in covered for i in range(*m.span())):
                continue
            tok = m.group(0)
            if any(re.fullmatch(p, tok) for p, _r in REASONS):
                continue
            win = text[max(0, m.start() - CONTEXT_WINDOW):m.end() + CONTEXT_WINDOW]
            if any(re.search(p, win) for p, _r in CONTEXT_REASONS):
                n_ctx += 1
                continue
            try:                       # 同一读数/常量的第二次出现：首次出现处已被某条守卫捕获
                if float(tok) in {v for v in guard_vals if isinstance(v, float)}:
                    n_dup += 1
                    continue
            except ValueError:
                pass
            unlisted.append(tok)
            census_bad.append(tok)
        print("-" * 78)
        print(f"CENSUS  house-style.md 数字 {len(hits)} 个 · 守卫覆盖片段 {len(spans)} 段 · "
              f"重复读数 {n_dup} 个 · 上下文豁免 {n_ctx} 个 · 未入理由表 {len(unlisted)} 个"
              f"{'' if not unlisted else '：' + ','.join(unlisted)}")
        bad += census_bad

    print(f"\n守卫 {n_guard} 条（其中结构守卫 {n_struct} 条 · SKILL 守卫 {n_skill} 条）"
          f" · provenance {n_prov} 条 · 总 {n_guard + n_prov} 条")
    print(f"RESULT: {'PASS' if not bad else 'FAIL（' + ','.join(sorted(set(bad))) + '）'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
