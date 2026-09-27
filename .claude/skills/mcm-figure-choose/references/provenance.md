# provenance —— `house-style.md` 里每个数的口径与复跑命令

> **本文件是 `house-style.md` 的"账本"**：规范正文只给**规则 + 数 + 来源 + 验证状态**，
> 每个数的**口径（含分母定义）、样本范围、已知偏差、复跑命令**都在这里。
>
> **纪律**：① 每个数都有一条**可直接粘进 bash** 的命令（cwd = 仓根，`python` = 本机 Python 3.11）；
> ② 命令跑出来的值与这里的 `数` 必须一致（容差见每条），**不一致就是本文件错了**；
> ③ 只写**当场跑过**的数，没跑过的写"未查"；④ 证据里不写绝对路径。

**复跑工具**：`tests/skills/figure-choose/house-metrics.py`（本任务新写，**出货检查器的数一律 import 它、绝不抄实现**）。
**机器守卫**：`tests/skills/figure-choose/check-house-style.py`（表驱动，逐条读本文件与 `house-style.md` 现取期望值，
抽不到即 FAIL —— fail-closed）。

**三支仪器（照 this 文件的口径读，别混用）**：

| 仪器 | 定义 | 前缀 |
| :--- | :--- | :--- |
| **出货仪器** | `check-figure-style.py::color_count`：320×320 **NEAREST** 采样 + `//16` 分箱 + 去近灰（<24）+ **0.5% 地板** | `color_*` |
| **侦察仪器** | `quantize(32, MEDIANCUT)` + 去近白（`max>=240`）/近黑（`max<=40`）/近灰（`<=24`）+ 0.5% 地板；tab10 另用 `quantize(64)` + 非灰 C0–C6/C8/C9 + 距离 `<=3` + 占比 `>=0.3%` + 命中 `>=2` | `recon_*` / `tab10_*` |
| **几何仪器** | PNG 像素 ÷ **200 dpi**（渲染 dpi 是构造已知，不读元信息）；宽高比 = 宽/高；比值分母 = 43 篇正文行宽 p90 的全局中位 | `h1_*` / `h2_*` / `h3_*` |

**样本范围（全表通用）**：2025 单年 **43 份** / **662 图**（`corpus/papers/figures/**/fig-*.png`）；
**246 张表**（`tab-*`）同批抽到但**不在射程**；**O 奖无对照组**；**其余 158 份未抽取**。
判断层与像素判据来自侦察台账（`tests/figures-recon/a-judgment-rand120.tsv` 等，**入库件**）。

---

## A. 几何（H1 / H2 / H3）

### P-H1-a · 图宽比 p25（= H1 的下限 0.80）
数: 0.797
容差: 0.02
口径: 662 图的（PNG 像素宽 ÷ 200 dpi）÷ **6.31 in** 的 **p25**（线性插值分位）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h1_p25
样本范围: 662 图
已知偏差: 分子是**渲染带宽**（整区渲染的内容带），**不是图自身 bbox**；未独立核对（侦察 §8.1 同）。

### P-H1-b · 图宽比中位（H1 的默认档 0.95–1.0）
数: 0.951
容差: 0.02
口径: 同 P-H1-a，统计量换成中位。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h1_med
样本范围: 662 图
已知偏差: 同 P-H1-a。

### P-H1-c · 图宽比 max（= H1 的上限 1.20）
数: 1.189
容差: 0.02
口径: 同 P-H1-a，统计量换成 max（"超 1.19 的一例都没有"）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h1_max
样本范围: 662 图
已知偏差: 同 P-H1-a。

### P-H1-d · 参照分布自身的"合规率"（H13 的反例）
数: 74.47
容差: 0.2
口径: 比值落在出货 F1 区间 **[0.80,1.20]** 内的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h1_band_pct
样本范围: 662 图
已知偏差: **这个数不是"应该达到"的合规率**——它只是"同一把尺子量回参照分布"的结果（H13）。

### P-H1-e · 低于 0.80 的占比
数: 25.53
容差: 0.2
口径: 比值 < 0.80 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h1_below_pct
样本范围: 662 图
已知偏差: 这些"窄图"多为竖排/小图（如流程图局部），本规范**不把它们当反例**（H1 的 0.80 是下限而不是目标）。

### P-H2-a · 分母（43 篇正文行宽 p90 的全局中位）
数: 6.3099
容差: 0.02
口径: 台账 `tests/figures-recon/b-colwidth.tsv` 第 6 列 `col_w_in`（43 篇，**逐篇正文行宽 p90**，英寸）的中位数。
  规范正文写 **6.31 in**（四舍五入）。**这就是 H2 写死的分母**——所有 `h1_*` / `h2_fork_*` 的比值都用它。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_median
样本范围: 43 篇（每篇一行）
已知偏差: 台账生成器（逐篇 p90 的取法）**不在受版本控制的目录里**；本任务核到"台账 → 6.3099"这一步，
  **没有**重跑 p90 本身（侦察 §8.3 亦承认未做 p75/p95 敏感性）。

### P-H2-b · 对照口径：同一列的**均值**（M10 用它证明"换分母就变"）
数: 6.3981
容差: 0.02
口径: 同 P-H2-a 的一列，统计量换成**均值**。**这不是 H2 的分母**，只作"口径一换、结论就变"的对照。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h2_colw_p90_mean
样本范围: 43 篇
已知偏差: 均值被右尾拉高（max 7.19 in）⇒ 与中位差 0.088 in；用作分母会把所有比值压小。

### P-H2-c · 口径分叉：全局分母下的 [0.9,1.1) 占比
数: 56.65
容差: 0.2
口径: 分母一律取 6.31 in 时，比值落在 **[0.9,1.1)** 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h2_fork_global_pct
样本范围: 662 图
已知偏差: 与 P-H2-d 是**同一批图、同一区间**，只有分母不同 ⇒ 这两条就是 H2 的立论证据。

### P-H2-d · 口径分叉：逐篇分母下的同区间占比
数: 59.37
容差: 0.2
口径: 分母换成**该篇自己的 `col_w_in`** 时，比值落在 [0.9,1.1) 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h2_fork_perpaper_pct
样本范围: 662 图（分母取自 43 篇台账）
已知偏差: 两个口径的**中位数相同（0.951）**、**百分比不同（56.65 vs 59.37）** ⇒ 只报中位数会掩盖口径歧义。

### P-H3-a · 横图占比
数: 98.04
容差: 0.2
口径: 宽高比（宽/高，均取 200 dpi 像素）≥1 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h3_land_pct
样本范围: 662 图
已知偏差: 像素比 = 渲染带比（同 P-H1-a）。

### P-H3-b · 宽高比中位
数: 2.0856
容差: 0.02
口径: 662 图宽高比的中位。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h3_aspect_med
样本范围: 662 图
已知偏差: **与设计稿的 2.42 不一致**（见 house-style H3 的差异登记），但**归因已更正**：2.42 的出处是
  `progress.md` 的「908 张 PNG；抽样 120 张 ⇒ 宽高比中位 2.42」——**样本是 908 张（含 246 张表）、
  抽样过程未落文**。复核（`--metric h3_aspect_s120_med_lo` / `_hi`）：在**同一个 908 池**里按固定种子集
  （0/1/7/42/2792/20260927）重抽 120 张，中位落在 **2.24–2.42** ⇒ **该数不可复跑**（抽样偶然，不是错）。
  **原先把它归给 `A/2500836/fig-07-p9.png` 单张图的 aspect 2.427 是错的**：那只是**巧合**，
  2.42 是**抽样中位**而非任何单张读数 ⇒ 采用 662 图口径的实测 **2.0856**。

### P-H3-c · 宽高比 ≥2 的占比
数: 53.47
容差: 0.2
口径: 宽高比 ≥2 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h3_ge2_pct
样本范围: 662 图
已知偏差: 同 P-H3-a。

### P-H3-d · 图高中位
数: 2.625
容差: 0.02
口径: 662 图（像素高 ÷ 200 dpi）的中位（英寸）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h3_h_med
样本范围: 662 图
已知偏差: 渲染带高含带边界误差（侦察 §8.1）。

### P-H3-e · 竖图（宽高比 <1）占比
数: 1.96
容差: 0.2
口径: 宽高比 <1 的图占比（%）。= 100 − 98.04。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric h3_below1_pct
样本范围: 662 图
已知偏差: 同 P-H3-a。

---

## B. 配色（H4 / H5）

### P-H4-a · 出货仪器：主色中位
数: 2
容差: 0.5
口径: 出货仪器（`color_count`，**import 不抄**）在 662 图上的主色数中位。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric color_median
样本范围: 662 图
已知偏差: 与侦察仪器差 1 个色（见 P-H4-d）——同一张图两支仪器可以给出不同条数，**引用时必须带仪器名**。

### P-H4-b · 出货仪器：零彩色占比
数: 30.51
容差: 0.2
口径: 出货仪器读数 = 0 的图占比（%；202/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric color_zero_pct
样本范围: 662 图
已知偏差: 零彩色包含**纯灰度图与黑白线图**，也包含"彩色但都在 0.5% 地板以下"的图（后者是口径副作用）。

### P-H4-c · 出货仪器：≤4 覆盖率
数: 66.31
容差: 0.2
口径: 出货仪器读数 ≤4 的图占比（%；439/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric color_cov4_pct
样本范围: 662 图
已知偏差: **这是"闸门会放行多少张"的读数**，不是"多少张合规"——参照分布里就有 33.7% 过不了这一关。

### P-H4-d · 侦察仪器：主色中位
数: 3
容差: 0.5
口径: 侦察仪器（`quantize(32, MEDIANCUT)` + 去近白 `max>=240` / 近黑 `max<=40` / 近灰 `<=24` + 0.5% 地板）
  在**同一批 662 图**上的主色数中位。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric recon_median
样本范围: 662 图
已知偏差: 本任务把侦察仪器**重写**了一遍（其生成器**不在受版本控制的目录里**），并做了逐格核对：
  `--metric recon_ledger_match` = **662**（与入库台账 `c-color-count.tsv` 的 `n_sig_colors` 栏**逐格一致**）
  ⇒ 重写件可信；但"侦察仪器本身是否比出货仪器更对"**不是本任务能判的事**。

### P-H4-e · 侦察仪器：零彩色占比
数: 19.49
容差: 0.2
口径: 侦察仪器读数 = 0 的图占比（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric recon_zero_pct
样本范围: 662 图
已知偏差: 与出货仪器的 30.51% 差 11pp（口径分叉的第二支证据）。

### P-H4-f · 侦察仪器：≤4 覆盖率（与出货仪器同一阈值）
数: 58.61
容差: 0.2
口径: 侦察仪器读数 ≤4 的图占比（%；388/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric recon_cov4_pct
样本范围: 662 图
已知偏差: **本数就是"口径分叉把闸门放宽了"的另一半**：同一个 `≤4`，出货仪器覆盖 **66.31%**（P-H4-c）
  > 侦察仪器 **58.61%**（本数）⇒ 换仪器方向 = **放宽**（+7.7pp）。

### P-H4-g · N-2 那一对（72.9% / 57.2%）的口径与复现
数: 57.23
容差: 0.2
口径: baseline §7 的**转写口径**——`quantize(32, MEDIANCUT)` + 去近白写成 `min>=240` **且** 保留
  baseline 的 `//16` 分箱——在**同一 166 张抽样**（`FIGS[::4]`，每 4 取 1）上的 ≤4 覆盖率（%）。
  姊妹读数：同口径在 662 图上是 **51.81%**（`--metric recon_baseline_minw_cov4_pct`）、
  同口径在 166 抽样上主色中位 **4.0** / 零彩 **15.66%**（`--metric recon_baseline_minw_s166_median` /
  `..._s166_zero_pct`）、**真侦察仪器**（`max>=240`、**不分箱**）在同一 166 抽样上是 **63.86%**
  （`--metric recon_cov4_s166_pct`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric recon_baseline_minw_s166_cov4_pct
样本范围: 166 张抽样（本数）· 662 图（姊妹读数 51.81%）
已知偏差: **57.2% 是可复现的**（与 baseline §7 的 `median=4.0 / zero%=15.7 / <=4占比=57.2%` 逐格相同）。
  但它**不是真侦察仪器的读数**：转写件与真仪器有**两处**口径差——`min>=240` vs `max>=240`、
  **含 `//16` 分箱** vs **不分箱**（真仪器数的是**不同调色板项**）。⇒ 它**与 72.9% 不同源、不可对举**；
  72.9% 是出货仪器在同一 166 抽样上的读数（可复现，见 `--metric color_cov4_sample166_pct`）。

### P-H4-h · 连续色图在 F2 下的条数（H4 的射程界定）
数: 7
容差: 0.5
口径: 连续红蓝发散热图（`red/out-R2/figure.pdf`）在出货 F2 下的条数（≥0.5% 地板的色箱数）。
  同一条命令的姊妹读数：彩色箱 **152** 个、最高落选箱 **0.370%**、入选的最低箱 **0.689%**、
  离 0.5% 地板 **0.130pp**。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric f2_r2_counted
  （姊妹：`--metric f2_r2_boxes` / `--metric f2_r2_subfloor_max_pct` / `--metric f2_r2_lowest_counted_pct` / `--metric f2_r2_margin_pp`）
样本范围: 1 张（**标定样本只有 3 张**：R2 命中闸门，R1/R3 不命中）
已知偏差: 取箱逻辑 import `red/f2-diagnose.py` 的**重写件**，并对每一例断言与出货 `color_count` 一致
  （不一致即拒绝出数）⇒ 与 F2 的定义同源。

### P-H4-h2 · 连续色图闸门的**重标定**（本任务最重要的一处自我更正）
数: 72.81
容差: 0.2
口径: 新闸门 `彩色箱数 ≥100` **或** `最高落选箱 ≥0.4%` 在**全 662 图**上的命中率（%）。
  姊妹读数（全部由 `check-house-style.py` 的 `G-H4-gate-*` / `G-H4-heat-*` / `G-H4-ex*` 守）：
  **旧闸门**（箱数 ≥20 **且** 最高落选箱 ≥0.3%）在同一批图上 **49.40%**（`--metric cont_gate_old_pct`）；
  旧闸门"箱数 ≥20"那条腿放进来的比例 **95.62%**、真正被挡住的只有 **29 张**
  （`--metric cont_box20_pass_pct` / `cont_box20_below_n`）；
  图注带 `heatmap` 的 **13 张**（正则 `heat\s*-?\s*map`）里旧闸门只命中 **5** 张、新闸门命中 **11** 张
  （`--metric cont_heat_hit_old_n` / `cont_heat_hit_n`）；其中 **F2 条数 >4** 的 **9 张**里旧闸门只命中 **4** 张、
  新闸门 **9** 张全中（`--metric cont_cite_old_n` / `cont_cite_n`）；
  那 9 张里**最低**的最高落选箱 **0.094%**（`C/2505964/fig-08-p13.png`，比离散标定件 R1 的 **0.127%** 还低，
  `--metric cont_heat_subfloor_min_pct` / `f2_r1_subfloor_max_pct`）；
  两个漏检典型：`B/2517929/fig-10-p19.png` F2=**24** / 最高落选箱 **0.123%**、
  `C/2505964/fig-08-p13.png` F2=**17** / **0.094%**（`--metric cont_ex1_f2` / `cont_ex1_sub_pct` / `cont_ex2_f2` / `cont_ex2_sub_pct`）；
  **闸门补集**（未被判为连续色图的 **180 张**）上出货仪器主色中位 **1** / 零彩 **42.78%** / ≤4 覆盖 **88.33%**
  （`--metric cont_comp_n` / `color_median_comp` / `color_zero_pct_comp` / `color_cov4_pct_comp`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cont_gate_pct
样本范围: 662 图（闸门读数）· 13 张 heatmap 图注样本 · 3 张标定件（R1/R2/R3）
已知偏差: **旧闸门的两条腿都被实测否掉**——"箱数 ≥20"形同虚设（95.62% 过），"最高落选箱 ≥0.3%"
  在真语料上**不区分连续/离散**（真热力图 0.094% < 离散标定件 0.127%）。重标定后的闸门是**手工构造的
  保守方向**，不是标定过的判别器：标定件仍只有 3 张，13 张 heatmap 是**图注点名**的旁证（不是人眼逐张
  确认的"这是连续色图"）。重标定的**代价是命中率从 49.40% 升到 72.81%** ⇒ 本样本 **72.81%** 的图
  "F2 条数不可引用"（这一条已写进规范正文，不再声称"标定样本仅 3 张、只在窄边角生效"）。
  **另**："箱数 ≫ `color_count`"这条候选判据**方向是反的**（离散件 R1 比值 **26.00** > 真热力图 **9.12**，
  `--metric cont_ratio_disc` / `cont_ratio_heat`），故不采用。

### P-H5-a · 严判据 tab10 命中数
数: 6
容差: 0.5
口径: `quantize(64, MEDIANCUT)` + 非灰 tab10 色（C0–C6/C8/C9）+ RGB 欧氏距离 `<=3` + 该色占比 `>=0.3%`，
  命中的 tab10 **色序号集合**大小 ≥2 即记命中（与 `probe_c6_tab10_v2.py` 同法）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric tab10_strict_n
样本范围: 662 图
已知偏差: 重写件与入库台账 `c6-tab10-v2.tsv` 的 `n_hits` 栏**逐格一致 662**（`--metric tab10_v2_ledger_match`）。
  **6 张里 6/6 经人眼复核为真命中**（侦察 C.6 节）。

### P-H5-b · 严判据读数（下界）
数: 0.91
容差: 0.02
口径: P-H5-a 的命中数 ÷ 662（%）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric tab10_strict_pct
样本范围: 662 图
已知偏差: **这是下界**：判据只能证明"没观察到广泛使用"，不能证明"没人用"。

### P-H5-c · 松判据读数（已证伪，不得引用）
数: 17.82
容差: 0.1
口径: 容差 40（`probe_c_color.py` 的判据）+ 命中 ≥2 的命中率（%）；重写件与台账
  `c-color-count.tsv` 的 `tab10_verdict` 栏**逐格一致 662**（`--metric tab10_loose_ledger_match`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric tab10_loose_pct
样本范围: 662 图
已知偏差: **人眼已证伪**（12 张抽查 7 张是照片）⇒ 只作"判据面为什么被换掉"的留痕，**不得作结论**。

---

## C. 判断层与像素判据（H6 / H7 / H8 / H11）

### P-C-a · 饼图（判断层）
数: 0
容差: 0.5
口径: 判断层抽样 `a-judgment-rand120.tsv`（**种子 20260927 随机 120 张**，缩略图判读）里 `pie == "y"` 的张数。
  占比 = **0.0%**（`--metric judge_pie_pct`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric judge_pie_n
样本范围: 判断层 120 张（不是 662 全量）
已知偏差: 缩略图判读（340×260/格）⇒ 极小尺寸的饼图可能漏判；**0 张 ≠ 不存在**（下界）。

### P-C-b1 · 3D（判断层）
数: 9.17
容差: 0.1
口径: 判断层 120 张里 `three_d == "y"` 的占比（%；11/120）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric judge_3d_pct
样本范围: 判断层 120 张
已知偏差: 缩略图判读；与图注口径（P-C-b2）差约 4 倍 ⇒ 只作"少用"的方向性旁证。

### P-C-b2 · 3D（图注口径，本任务自定判据面）
数: 2.11
容差: 0.1
口径: 图注里出现 `3-D` / `3D` / `three-dimensional` 的图占比（%；14/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric caption_3d_pct
样本范围: 662 条图注
已知偏差: 侦察 §7.2 #4 记的另一口径是 1.8%，但**其口径未落文** ⇒ 本任务只引自己这条可复跑的读数。

### P-C-c1 · 多面板（判断层）
数: 50.83
容差: 0.1
口径: 判断层 `multi_panel == "y"` 占比（%；61/120）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric judge_mp_pct

### P-C-c2 · 多面板（像素判据读数）
数: 92.3
容差: 0.2
口径: 像素判据 `c7-pixel-criteria.tsv` 的 `multi_panel == 1` 在 662 图上的占比（%；611/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric pixel_mp_pct

### P-C-c3 · 多面板：判断层 vs 像素判据的一致率
数: 55.83
容差: 0.1
口径: P-C-c1 与 P-C-c2 在**同一 120 张**上的逐张一致率（%；67/120）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric mp_agree_pct
样本范围: 判断层 120 张 / 662 图
已知偏差: 像素判据（白带 + 网格结构）**系统性多判**（92.3% vs 50.8%）⇒ 只能当**上界**（H8 的措辞下限）。

### P-C-d · 图例判据（已证废）
数: 15.83
容差: 0.1
口径: 判断层 `legend` 与像素判据 `legend_frame` 在同一 120 张上的一致率（%；19/120）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric legend_agree_pct
样本范围: 判断层 120 张
已知偏差: 一致率 15.83% ≈ 抛硬币 ⇒ **判据已证废**（侦察 §8.6 同）；像素判据报的 81.0% 不得引用。

### P-C-e · 网格判据（只是读数）
数: 27.34
容差: 0.2
口径: 像素判据 `grid == 1` 在 662 图上的占比（%；181/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric grid_reading_pct
样本范围: 662 图
已知偏差: **没有独立人判对照** ⇒ 它只是"判据读数"，不是"获奖论文里 27.34% 有网格线"这个结论（侦察 §8.5）。

---

## D. 图注（H9）

### P-D-a · 标签可机械切出 / 附图注条数
数: 100.0
容差: 0.1
口径: 662 条 `fig-*.caption.txt` 里能被宽松前缀 `^\s*(Figure|Fig\.|Table)\s*\d+\s*[:.：．。]?` 切出标签的占比（%）。
  附图注条数 `cap_n` = **662**。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_cut_pct
样本范围: 662 条图注
已知偏差: 宽松口径**含**仅带句点的形态；出货 F3a 是严格口径（见 P-D-b）。

### P-D-b · ASCII 冒号占比 / 出货 F3a 严格匹配率
数: 86.4
容差: 0.2
口径: 662 条图注里前缀标点为 **ASCII 冒号** `:` 的占比（%；572/662）。姊妹读数：出货 F3a
  （`^Figure\s+\d+\s*:`，在 strip 后匹配）的匹配率 = **86.25%**（571/662；1 条差异来自前导空白）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_ascii_colon_pct
样本范围: 662 条图注
已知偏差: **与设计稿的 87.3% 不一致**（差异登记在 house-style H9），但**这是口径收窄、不是设计稿错**：
  87.3% 是**同一 662 条图注**上更宽口径（ASCII 冒号**或** ASCII **句点**）的读数 —— 姊妹读数
  `cap_ascii_colon_or_period_n` = **578**（= 572 冒号 + **6** 句点，即侦察报告 §4.4 的「合计用
  ASCII `:`/`.` | 578/662 = 87.3%」一行）⇒ 578/662 = **87.31%**；本规范**只算冒号**（572/662 = 86.4%）。
  差的 6 条正是写成 `Figure N.` 的那批（它们缺冒号，出货 F3a 会抓）。**原先记的"87.3% 疑为全 908 条
  （含表）的读数、777/908 = 85.57%"是错的**：表中 ASCII 冒号只有 205 条，与 87.3% 无关。

### P-D-c1 · 正文词数中位
数: 5
容差: 0.5
口径: 词数 = **去掉 `Figure N:` 前缀后的正文**按 `\S+` 计数（"图注正文该怎么写"要的是正文部分）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_words_med
样本范围: 662 条图注
已知偏差: **已收敛**（Task 6 GREEN 对照 Important-2 定案）：出货检查器的 `CAP_MAX=12` / `CAP_HARD=17` 原先
  数的是**含标签的整条**词数（比本口径多 `Figure N:` 这 2 个词）⇒ 当时**两个口径不可互换**。
  现已把 F3b 改成 `len(caption_body(cap).split())`（去标签后的正文），与本口径、与 `cap_words_*` 三者同源；
  **常量与 `G-H9-*` 守卫一个没动** —— 12 / 17 本就是**本口径**（正文）的 p95 / max
  （`tests/figures-recon/c8-caption.tsv`：`FIG words(去标签后正文) … p95=12.0 max=17`；
  含标签那行是 `p95=14.0 max=19`）。反向改（把常量重导为含标签口径的 14 / 19 并改本文件三条读数）
  与现口径冲突，故不取。

### P-D-c2 · 正文词数上限（p95）
数: 12
容差: 0.5
口径: P-D-c1 的口径下的 p95（线性插值分位）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_words_p95
样本范围: 662 条图注
已知偏差: 同 P-D-c1（**已收敛**；含标签口径的 p95 比它长）。

### P-D-c3 · 正文词数上界（max）
数: 17
容差: 0.5
口径: P-D-c1 的口径下的 max（= 全样本上界，出货常量 `CAP_HARD=17` 的来源）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_words_max
样本范围: 662 条图注
已知偏差: 同 P-D-c1（**已收敛**）。本读数是**正文口径**的 max，与出货常量 `CAP_HARD` 同源同值；
  含标签口径的 max 比它长（`tests/figures-recon/c8-caption.tsv` 的两行可逐字对账）。

### P-D-d · 句末无句号占比
数: 94.56
容差: 0.2
口径: 662 条图注里**末尾不是 ASCII 句点**的占比（%；626/662）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_noperiod_pct
样本范围: 662 条图注
已知偏差: 侦察 §8.8：这 5.44% 的成因未区分（原文风格 vs 抽取截断）——本规范只说"多数不加句号"。

### P-D-e · 空图注张数 / F3d 的射程
数: 17
容差: 0.5
口径: 整条图注只有 `Figure N:` + 标点、无正文的条数（= 整条词数恰为 2；**17/662**）。
  其中**被出货 F3d 抓到 15 张**（`--metric cap_empty_f3d_n`）；另 **2 张**写成 `Figure N.`（ASCII 句点、缺冒号），
  F3d 抓不到但**出货 F3a 会抓**（缺 `Figure N:` 的冒号形态）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_empty_n
样本范围: 662 条图注
已知偏差: F3d 只覆盖 15/17 ⇒ **空图注的完整覆盖靠 F3a + F3d 两条合起来**，单独引用 F3d 会漏 2 张。

---

## E. 〔社区〕条目与未覆盖条目的"依据"数（H10 / H12）

### P-E-a1 · PNG 连通域反推的字号乱值（min）
数: 1.54
容差: 0.02
口径: 入库台账 `tests/figures-recon/d9-fontsize-experiment.tsv` 的 `est_pt_mode` 栏（**n=40 抽样**）的 min（pt）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric font_est_pt_min
样本范围: d9 台账 40 张（不是 662）

### P-E-a2 · PNG 连通域反推的字号乱值（max）
数: 11.31
容差: 0.02
口径: 同 P-E-a1 的 max（pt）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric font_est_pt_max
样本范围: d9 台账 40 张（不是 662）
已知偏差: **这两个数不是"字号读数"**，是"这条路走不通"的证据（1.54–11.31 pt 跨了 7 倍）；
  H12 的字号规则来自〔社区〕，**不是**从这两个数推出来的。

### P-E-b · H10 / H11 的"量不到/未覆盖"依据
数: 无（**本条不给数**）
容差: —
口径: H10（刻度朝向）与 H11（网格/图例/双 Y 轴）**不给读数**：前者 PNG 路径未打通（侦察 §7.3），
  后者的判据已证废（P-C-d）或只是读数（P-C-e）。
复跑命令: 无——**本样本量不到**，故没有可复跑的数（这正是这两条被标 ③ 的原因）。
样本范围: —
已知偏差: 本文件不含任何 H10/H11 的"测量值"；若将来要写，须先有**通过人判对照**的新判据面。

---

## F. 交付形态（"一个图文件 = 一页"）

### P-F-a · 两页探针的读数
数: 2
容差: 0.5
口径: `red/multipage-probe.pdf` 的页数（**2**）；page1 页盒 **6.31 in** / **1 色**（F1 比值恰 1.000）；
  page2 页盒 **12.00 in** / **6 色**；**整份在出货检查器下判 PASS**（`probe_verdict`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric probe_pages
  （姊妹：`--metric probe_page2_w_in` / `probe_page2_colors` / `probe_verdict`）
样本范围: 1 份两页 PDF（生成器 `red/make-multipage-probe.py`，固定 CreationDate、可重复生成）
已知偏差: 探针是**手工构造**的两页 PDF（不是真实论文）；它证明的是"检查器只读 `doc[0]`"这一实现事实，
  **不证明**真实论文里有几份多页图。

---

## G. 样本框架（结构性常量）

### P-G-a · 样本量
数: 662
容差: 0.5
口径: `corpus/papers/figures/**/fig-*.png` 的文件数；样本份数 = **43**（`b-colwidth.tsv` 行数）；
  判断层抽样 = **120**（`a-judgment-rand120.tsv`）。
复跑命令: python tests/skills/figure-choose/house-metrics.py --metric cap_n
  （= 662；姊妹：`--metric judge_n` = 120）
样本范围: —
已知偏差: 662 张来自 **2025 单年**；**O 奖无对照组**；**其余 158 份未抽取** ⇒ 不能外推成"美赛通行规律"。
