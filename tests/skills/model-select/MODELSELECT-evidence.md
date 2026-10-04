# Task 14 · RED × GREEN 对照证据（`mcm-model-select`）

本文件由 `tests/skills/model-select/make-evidence.py` **当场跑命令**生成（`write_bytes`、全 LF）。
**§2 / §3 / §4（原始读数）· §5（对照表）· §9（blob）是机器抽取**（逐格解析检查器 stdout、逐份扫产物、**实跑 MATLAB**）；**§6 的性质判定 · §7 的诚实边界是手写**（文里已标明）。

## §0 口径（同一件事 · **两把尺** · 可比列 vs 不可比列 · 样本量边界）

- **同一件事**：`tests/skills/model-select/red/brief.md`（**唯一一份**，RED 与 GREEN 逐字共用；§1 全文内联） ＋ 同一题面 `tests/skills/abs-cases/case-A-problem.txt`（**2025 MCM Problem A**，与 M2 的 RED 同源）。
- **两侧**：RED = **干净上下文、未用 `fork`、未给本 skill** 的写手产出的「选模型 + 求解代码」（3 位）；GREEN = **用本 skill**（`SKILL.md` + `references/` + 检查器）出的同一件事（1 位）。
- ★★ **两把尺（本支口径，与 `topic-select` **不同** —— 那支的检查器有 `--output`，本支没有）**：
  1. **产物探针**（`probe_product`）：**同一函数**逐份量**产物目录**（文件 / 类词 / 假设节 / 辨识讨论 / 代码文件 / **入口代码实跑**）。★ **这一把对两侧同尺 ⇒ 它给出的列是“可比列”。**
  2. **skill 检查器** `check-model-select.py`：**它没有 `--output`** —— 它判的是 **skill 本体**，**不是写手产物** ⇒ ★ **它只对 GREEN 侧（用本 skill）有对象；RED 侧无对象（不适用）** 
     ⇒ **它给出的列是“不可比列”，不许混进对照表当两侧同尺。**
- **判据清单现取**：本支 **6 条**（`MS1、MS2、MS3、MS4、MS5、MS6`）—— 读检查器 stdout 的 `PASS|FAIL|SKIP  <id>` 行，**不写死条数**（先例：写死条数 ⇒ 判据增减时汇总表**静默归零**）。
- **检查器自证**：工作树 blob `a1aa85207606`（**本支不动检查器**；两侧用的是同一版）。
- **题面自证**：`tests/skills/abs-cases/case-A-problem.txt` blob `2842d542e0d5`。
- **brief 自证**：`tests/skills/model-select/red/brief.md` blob `7882dc834476`（§1 全文内联）。
- **RED 是自变量**：三份写手产物**照实入库**（本轮未改）。逐件读数：

| 产物 | 侧 | 文件 | 字节 | 行数 | CR（`\r` 数） | 工作树 blob |
| :-- | :-- | :-- | --: | --: | --: | :-- |
| `R1/selection.md` | RED | selection.md | 22154 | 477 | 0 | `8b8e47660a24` |
| `R1/stairwear.m` | RED | stairwear.m | 10607 | 239 | 0 | `465c850b94b4` |
| `R2/print_recovery.m` | RED | print_recovery.m | 953 | 27 | 0 | `b0872f3c1e68` |
| `R2/selection.md` | RED | selection.md | 33543 | 691 | 0 | `781c4d1755ea` |
| `R2/wear_ci.m` | RED | wear_ci.m | 770 | 24 | 0 | `a3c1d362e2bb` |
| `R2/wear_conclusions.m` | RED | wear_conclusions.m | 3880 | 93 | 0 | `696ee3c7a27a` |
| `R2/wear_demo.m` | RED | wear_demo.m | 4446 | 93 | 0 | `ca12544422db` |
| `R2/wear_fit.m` | RED | wear_fit.m | 2892 | 83 | 0 | `7133cf0cba86` |
| `R2/wear_forward.m` | RED | wear_forward.m | 3093 | 71 | 0 | `248e177cc602` |
| `R2/wear_robustfit.m` | RED | wear_robustfit.m | 1020 | 30 | 0 | `0b10023d52e6` |
| `R3/selection.md` | RED | selection.md | 26774 | 519 | 0 | `9e3fa95b8e6c` |
| `R3/stair_wear_model.m` | RED | stair_wear_model.m | 14235 | 338 | 0 | `838627750a6d` |
| `G1/selection.md` | GREEN | selection.md | 32878 | 476 | 0 | `5a587f31b065` |
| `G1/stair_wear_archard.m` | GREEN | stair_wear_archard.m | 10645 | 233 | 233 | `af11d32b93c2` |

★ **`CR` 列是一处如实登记**：写手产物**照实入库、本轮不改**（含**换行符**）—— 所以若某份写手件落盘时是 **CRLF**，这里就照实记它的 `CR > 0`（本支的 **G1 `stair_wear_archard.m` = 233**）。★ **本仓 `CRLF=0` 纪律管的是“我方作者件”**（本证据件与生成器都是全 LF）；**写手产物沿既有先例保留其原始字节**（先例：`tests/skills/table/red/out-R2/table.tex` 等既有写手件同样带 CR）。

- ★★ **样本量边界（**原话**）**：**`n = 1` 道题 × `3` 位 RED 写手 × `1` 位 GREEN 写手 ⇒ 任何“两侧都/都不”只是“这一次的读数”，不得写成“普遍规律”。**
- ★★ **环境旁路（照实披露）**：写手是本机 Claude Code 的 agent，会话级上下文里另有三处可见面 —— ① **skill 列表**里 `mcm-model-select` 那一行的**描述**（点了名“两跳 / 候选模型 + 判据 / 带推翻条件的推荐 / 六格详情”）；② `git status` 快照；③ **Recent commits**。★ **本轮这不是“没泄漏”**：**RED 的 R3 产物里抽到了 `六格`（1）与 `推翻`（2）** —— 那是**本 skill 描述里的词**（§2、§6）⇒ **R3 已被环境旁路污染**。★ **“未抽到” ≠ “没读到”**（只有自报，没有沙箱可证）。
- ★★ **污染面逐份给（2026-10-04 Task 14 复核发现①补探 —— 本行原写“R1/R2 未抽到同类词”，是无限定、可一秒推翻的声明，已按实测改写）**：`候选模型` R1=**0** R2=**1** R3=**1**；`判据` R1=**0** R2=**0** R3=**3**；`六格` R1=**0** R2=**0** R3=**1**；`推翻` R1=**0** R2=**0** R3=**2**；`骨架` R1=**0** R2=**0** R3=**1**。⇒ **只有 R1 全净；R2 命中 `候选模型`×1；R3 命中多处**。⇒ **不得读成“R1/R2 未抽到同类词”**（复核命令：`grep -c 候选模型 tests/skills/model-select/red/out-R2/selection.md` ⇒ **1**）。★ **强指纹（`## …六格` / `…推翻条件` 标题）仍是本件已披露的那两处** ⇒ **实质污染未隐瞒**，多出的是**通用词、信号弱**；★ 污染再宽**只会把 RED 推向“更不盲”，不动结论方向**。
- ★ **另一处旁路（2026-10-04 Task 14 复核发现②）**：`red/out-R3/selection.md` **复现了本仓的内部口号**（“判据恒真与‘声明超过事实’是同一类错误…凡列证据都写明‘不声称穷尽’”）—— 该句**不在 brief、不在题面、也不在最近提交主题行**，疑**继承自写手 agent 的 `CLAUDE.md` / 记忆文件**（**未证**）⇒ **RED 臂“不盲”的不止 skill 描述一面**。★ 如实登记，**未重跑、未换人**（与发现①同处置）。

## §1 同一件事（逐字内联；RED 与 GREEN 共用）

```text
# Brief：给这道题选模型，并给出可跑的求解代码

你是一名美赛（MCM/ICM，美国大学生数学建模竞赛）的建模顾问。一支队伍马上要开赛，手上有一道题的题面，
就放在与本文件同一目录的 `problem.txt` 里。

请你为这道题做两件事：

1. **选模型** —— 为这道题选出一个（或一组）你建议队伍使用的模型，并说明为什么选它。
2. **给可跑的求解代码** —— 给出能用 **MATLAB** 跑的求解代码，让队伍直接拿去算这道题。

把成果写成一个 markdown 文件 `selection.md`，放进给你的输出目录。代码可以直接嵌在 `selection.md` 里，
也可以另存成 `.m` 文件放进同一个输出目录（两种都行）。

其余都由你决定：怎么组织、要不要补充说明、写多长，都随你。

完成后，请简短自述：你读到了哪些文件、产出了什么、为什么这么选、有什么拿不准的地方。
```

★ **中立性抉择**：brief **只问**「选模型 + 给可跑的求解代码」，**不含**本 skill 的任何契约词（不提“两跳”“类索引”“六格”“判据”“骨架路径”）、**不含**任何来源（不给本 skill、不给语料、不给判据、不给本任务书）。**唯一**算限定的一句是 **“用 MATLAB”** —— 它**不是** skill 内容，是为了让**两侧的“代码能不能跑”落在同一把尺上**（GREEN 的骨架也是 MATLAB）。

★ **题面（权威副本在 `tests/skills/abs-cases/case-A-problem.txt`；此处不重复内联）**：2025 MCM Problem A「Testing Time: The Constant Wear On Stairs」（5683 字节）。

## §2 RED 原始读数（三位干净上下文写手 · 只给 brief + 题面）

### §2.1 机器抽取：产物特征（`probe_product`，同一函数）

| 产物 | 文件数 | 总字节 | `selection.md` 行 | 抽到的**类词** | 假设节标题 | 假设词命中（全篇） | 辨识命中 | 推翻命中 | 六格命中 | 骨架命中 | ```matlab 围栏 | `.m` 文件 |
| :-- | --: | --: | --: | :-- | :-- | --: | --: | --: | --: | --: | --: | :-- |
| R1 | 2 | 32761 | 477 | （无） | 有（2） | 8 | 1 | 0 | 0 | 0 | 2 | `stairwear.m` |
| R2 | 8 | 50597 | 691 | prediction×5、mechanism×2、statistics×2、optimization×1、ml×1 | （无） | 3 | 2 | 0 | 0 | 0 | 8 | `print_recovery.m`、`wear_ci.m`、`wear_conclusions.m`、`wear_demo.m`、`wear_fit.m`、`wear_forward.m`、`wear_robustfit.m` |
| R3 | 2 | 41009 | 519 | ml×5、mechanism×2、statistics×2、prediction×1、simulation×1 | （无） | 4 | 17 | 2 | 1 | 1 | 1 | `stair_wear_model.m` |
| G1 | 2 | 43523 | 476 | mechanism×36、statistics×10、simulation×8、optimization×5、prediction×2、evaluation×1、network×1、ml×1 | （无） | 10 | 23 | 3 | 3 | 12 | 1 | `stair_wear_archard.m` |

★ **这张表里的“类词”只是词频**（EN 名 + CN 别名在 `selection.md` 里的命中数），**它不判“选对了类没有”** —— 后者是 §6 的判断层。**本表不声称穷尽**（只抽这一组词）。

### §2.2 机器抽取：**入口代码实跑**（同一把尺 · `matlab -batch`）

**R1**（入口 = `stairwear`）

```
$ matlab -batch "addpath('<arm dir>'); stairwear"
=== STAIRWEAR self-test on SYNTHETIC data ===

-- grid 31 x 121 ; tread 1.20 m (x) by 0.30 m (y) --
RMS residual = 0.20 mm   (measurement sigma = 0.15 mm)

[1] HOW OFTEN USED
    total footfalls  N = 8.35e+05  (+/- 4.33e+03, 95%)
    rate = 2782 steps/yr  ~= 7.6 steps/day  (given age = 300 yr)

[2] TRAVEL DIRECTION
    descending fraction f_down = 0.305  (+/- 0.002, 95%)
    -> direction is BIASED toward ASCENDING

[3] SIMULTANEOUS USERS
    second-lane weight pi2 = 0.46 ; lane separation = 0.415 (+/- 0.001) m
    -> SIDE-BY-SIDE traffic likely (>= 2 people abreast)
    model choice by BIC: 1-lane = 108361.5 , 2-lane = 6860.7 -> favour 2 lanes

[4] AGE CONSISTENCY / RELIABILITY
    age from weathering = 215 (+/- 13, 95%) yr ; historical = 300 (+/- 50) yr
    discrepancy z = 1.69 -> CONSISTENT

[5] SHORT-BURST vs LONG-SLOW
    abrasive volume = 0.000835 m^3 ; uniform environmental depth = 0.21 mm
    abrasive/(environmental) ratio = 10.80
    (large ratio & short T -> many people, short time;
     small ratio & long T   -> few people, long time)

-- recovered parameters (m) --
    ascending foot at y = 0.180 m , descending foot at y = 0.049 m
    lanes at x = 0.397 and 0.812 m ; lateral spread tau = 0.124 m

-- per-parameter 95% confidence half-widths --
    amp    =   0.00083456  +/- 4.33e-06
    fdown  =      0.30499  +/- 0.00165
    yu     =      0.18042  +/- 0.000192
    yd     =     0.049301  +/- 0.000482
    mu1    =      0.39694  +/- 0.000656
    mu2    =      0.81172  +/- 0.000775
    pi2    =      0.46305  +/- 0.00127
    tau    =      0.12401  +/- 0.000544
    base   =   0.00021473  +/- 1.26e-05
    (sigma used for CI: 0.20 mm)
[exit=0]
```

**R2**（入口 = `wear_demo`）

```
$ matlab -batch "addpath('<arm dir>'); wear_demo"
Ground-truth field: max 8.38 mm, mean 2.39 mm

----------- Parameter recovery (synthetic test) -----------
param               true        fitted     relerr
V                2.4e+05     2.406e+05       0.2%
alpha               0.62        0.6302       1.6%
b                     90         90.37       0.4%
sigx                  30          29.9      -0.3%
dmu                   60            60       0.0%
sigy                  70            70      -0.0%

================ Archaeological conclusions ================
Total removed wear volume  V      = 2.406e+05 mm^3
Mean wear depth            h_mean = 2.673 mm
Peak wear depth            h_peak = 8.496 mm

[How often were the stairs used?]
  per-footfall removal d0 = 0.15 mm^3  =>  total footsteps N ~ 1.604e+06
  given age = 400 yr  =>  mean traffic ~ 11.0 steps/day
  given traffic = 500 steps/day  =>  implied age ~ 9 yr

[Was a direction of travel favoured?]
  ascending fraction alpha = 0.630  (+/- 0.004)
  verdict: significantly biased UP  (front/back centroid offset dmu = 60.0 mm)

[How many people used the stairs simultaneously?]
  lane separation b = 90.4 mm, lane spread sigx = 29.9 mm, b/sigx = 3.02
  verdict: two tracks -> side-by-side / parallel traffic
===========================================================

Lane-structure model selection (lower AIC wins):
  1-lane : AIC =    -76.9 , RMSE = 0.958 mm
  2-lane : AIC =  -2476.1 , RMSE = 0.275 mm
  -> data favour TWO LANES (side-by-side)
[exit=0]
```

**R3**（入口 = `stair_wear_model`）

```
$ matlab -batch "addpath('<arm dir>'); stair_wear_model"
=========== SYNTHETIC BENCHMARK ===========
ground truth : N = 8.000e+06 footfalls
ground truth : f_d = 0.62 (descent share)
ground truth : two-lane, lane sep = 0.20 m

--- INVERSE-MODEL ESTIMATES ----------------------------------
total removed volume   A   = 0.0005734 m^3
descent fraction       f_d = 0.620   (95% CI 0.618 .. 0.622)
  -> ascent fraction       = 0.380
total footfalls        N   = 8.025e+06   (95% CI 7.991e+06 .. 8.058e+06)
lateral model          : 2 lanes -> SIDE-BY-SIDE travel supported
  lane centres y = -0.101 , 0.102 m   separation = 0.203 m
BIC(1 lane , 2 lane)   = -172.9 , -190.7   (lower is better)
--------------------------------------------------------------
To convert N to a traffic rate:  rate = N / (age_days).
Example: age = 400 yr -> 54.9 foot-passages per day.

[repair detector -- synthetic per-step depth vector]
  suspect replaced/repaired step index : 6
  most likely renovation change point after step : 5
[exit=0]
```

**G1**（入口 = `stair_wear_archard`）

```
$ matlab -batch "addpath('<arm dir>'); stair_wear_archard"
[stair_wear_archard] Archard wear-accumulation model
  truth : k=2  sep=0.240 m  alpha_up=0.70  w_max=0.0120 m  N=1.2e+07  age=12000.0 y
  fit   : k=2  sep=0.240 m  alpha_up=0.70  N=1.2e+07  age=11998.4 y
  rel.err : N(LS)=0.01%  N(peak)=4.76%  N(vol)=0.00%
  direction up:down = 70:30 (truth 70:30)
  age 95% CI = [4850.3, 28612.4] y  (N 95% kc=(6605192.84,21789693.25))

ans = 

  包含以下字段的 struct:

        th_true: [1×1 struct]
            fit: [1×1 struct]
         N_true: 12000000
          N_hat: 1.1998e+07
         N_peak: 1.2571e+07
          N_int: 1.1999e+07
        age_hat: 1.1998e+04
         age_ci: [2×2 double]
    age_samples: [4000×1 double]
      dir_ratio: 0.7005
          k_hat: 2
[exit=0]
```

## §3 GREEN 原始读数（用本 skill 的同一件事）

（§2.1 的特征表与 §2.2 的实跑表**已含 G1**；本节只把 GREEN 侧的**检查器**读数单列 —— 见 §4。）

## §4 检查器读数（`check-model-select.py` · **机器抽取**；★ 判的是 skill 本体，不是写手产物）

### `--scope all`

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe .claude/skills/mcm-model-select/check-model-select.py --scope all
check-model-select.py · scope=all
skill-dir = D:\Projects\数学建模\.claude\skills\mcm-model-select
PASS  MS1  势=66（方法文件）· 六格不全 0 份
PASS  MS2  势=53（盘上素材路径）· 不存在 0 条
PASS  MS3  势=66（骨架）· 参照记录/四要素不全 0 份  ★ 独立性（不同源）本器判不了，归人工/独立复核（设计 §4.1/§4.2）
PASS  MS4  势=66（骨架）· matlabroot=D:\Software\Matlab · 不合 0 项
PASS  MS5  势=1（`SKILL.md`）· 边界声明 在位
PASS  MS6  势=8（类索引，共 66 行）· 不一致 0 处
------------------------------------------------------------------------------
判据 6 条 · 红 0 条
RESULT: PASS
[exit=0]
```

### `--scope index-self`

```
$ C:\Users\Shameless\AppData\Local\Programs\Python\Python311\python.exe .claude/skills/mcm-model-select/check-model-select.py --scope index-self
check-model-select.py · scope=index-self
skill-dir = D:\Projects\数学建模\.claude\skills\mcm-model-select
SKIP  MS1  本面（index-self）按定义不含方法文件（还没写）；六格在 --scope class/all 面判 —— 这不是「通过」
PASS  MS2  势=53（盘上素材路径）· 不存在 0 条
PASS  MS3  势=66（骨架）· 参照记录/四要素不全 0 份  ★ 独立性（不同源）本器判不了，归人工/独立复核（设计 §4.1/§4.2）
PASS  MS4  势=66（骨架）· matlabroot=D:\Software\Matlab · 不合 0 项
PASS  MS5  势=1（`SKILL.md`）· 边界声明 在位
PASS  MS6  势=8（类索引，共 66 行）· 不一致 0 处
------------------------------------------------------------------------------
判据 6 条 · 红 0 条 · SKIP MS1
RESULT: PASS  [SKIP MS1]
[exit=0]
```

★ **状态图例**：`PASS` / `FAIL` / `SKIP`。★ `--scope index-self` 的 `MS1` 是 **`SKIP`**（该面按定义不含方法文件 —— **这不是“通过”**）。

## §5 对照表（机器抽取）

### §5.1 ★★ 可比的列（**产物探针**，两侧同尺）

| 列（机器抽取） | R1 | R2 | R3 | G1 | 两侧同尺？ |
| :-- | :-- | :-- | :-- | :-- | :-- |
| 产物文件数 | 2 | 8 | 2 | 2 | **是** |
| 入口 `.m` | `stairwear` | `wear_demo` | `stair_wear_model` | `stair_wear_archard` | **是** |
| 入口实跑 exit | 0 | 0 | 0 | 0 | **是** |
| 入口实跑有输出 | 是 | 是 | 是 | 是 | **是** |
| 抽到的类词（个） | 0 | 5 | 5 | 8 | **是** |
| 假设节标题 | 有 | 无 | 无 | 无 | **是** |
| 假设词命中（全篇） | 8 | 3 | 4 | 10 | **是** |
| 辨识讨论命中 | 1 | 2 | 17 | 23 | **是** |
| 推翻条件命中 | 0 | 0 | 2 | 3 | **是** |
| `.m` 文件数 | 1 | 7 | 1 | 1 | **是** |

★ **上表每一列都两侧同尺**（同一个 `probe_product` / 同一个 `run_entry` 跑的）⇒ 它是对照表的**主体**。

### §5.2 ★★ 不可比的列（**skill 检查器** —— **只有 GREEN 侧有对象**）

| 判据 | 打的是（机制） | `--scope all` | `--scope index-self` | RED 侧 |
| :-- | :-- | :-- | :-- | :-- |
| `MS1` | 六格齐备（每个方法文件） | PASS | SKIP | **不适用（无对象）** |
| `MS2` | 引用的盘上素材路径存在 | PASS | PASS | **不适用（无对象）** |
| `MS3` | 每个骨架有参照记录（四要素齐） | PASS | PASS | **不适用（无对象）** |
| `MS4` | 骨架可跑 + 遮蔽守卫 | PASS | PASS | **不适用（无对象）** |
| `MS5` | 边界声明在场 | PASS | PASS | **不适用（无对象）** |
| `MS6` | 类索引 ↔ 实际方法文件（双向一致） | PASS | PASS | **不适用（无对象）** |

★ **这两列不可比**：`check-model-select.py` **没有 `--output`**（与 `check-topic-select.py` 不同）——它判的是 **skill 本体**（索引 / 骨架 / 参照 / 边界声明），**不是写手产物**。
  ⇒ ★★ **RED 侧没有 skill 本体可以喂给它** ⇒ **RED 在这几列上“无对象”**，**不许把 RED 的“空”当成“红”或“绿”**。
  ★ **同族**：**GREEN 的产物 `selection.md` 也没有任何一条 `MS` 判据去量它** —— `MS1`–`MS6` 全绿只说明 **skill 本体**齐备，**不说明这份产物写得好**（§7.4）。

### §5.3 检查器逐判词（机器抽取；判词原文，不手抄）

| 面 | 判据 | 状态 | 判词 |
| :-- | :-- | :-- | :-- |
| `all` | MS1 | PASS | 势=66（方法文件）· 六格不全 0 份 |
| `all` | MS2 | PASS | 势=53（盘上素材路径）· 不存在 0 条 |
| `all` | MS3 | PASS | 势=66（骨架）· 参照记录/四要素不全 0 份  ★ 独立性（不同源）本器判不了，归人工/独立复核（设计 §4.1/§4.2） |
| `all` | MS4 | PASS | 势=66（骨架）· matlabroot=D:\Software\Matlab · 不合 0 项 |
| `all` | MS5 | PASS | 势=1（`SKILL.md`）· 边界声明 在位 |
| `all` | MS6 | PASS | 势=8（类索引，共 66 行）· 不一致 0 处 |
| `index-self` | MS1 | SKIP | 本面（index-self）按定义不含方法文件（还没写）；六格在 --scope class/all 面判 —— 这不是「通过」 |
| `index-self` | MS2 | PASS | 势=53（盘上素材路径）· 不存在 0 条 |
| `index-self` | MS3 | PASS | 势=66（骨架）· 参照记录/四要素不全 0 份  ★ 独立性（不同源）本器判不了，归人工/独立复核（设计 §4.1/§4.2） |
| `index-self` | MS4 | PASS | 势=66（骨架）· matlabroot=D:\Software\Matlab · 不合 0 项 |
| `index-self` | MS5 | PASS | 势=1（`SKILL.md`）· 边界声明 在位 |
| `index-self` | MS6 | PASS | 势=8（类索引，共 66 行）· 不一致 0 处 |

## §6 ★ 预测（**写在前**）vs 实际（逐条，含没发生的）

**这一节是判断层，机械读数判不了它。** 上表（§5）的读数是**机器抽取**；下表的**结论是人工**，
逐条写、**含"没发生的"**。★ 逐条**以 §2/§3 的机器读数为据**（不另编数字）。

| # | 预测（**写在前**，`red/README.md` §1） | RED 实际（R1/R2/R3） | GREEN 实际（G1） | 判定 |
| :-- | :-- | :-- | :-- | :-- |
| `P1` | **选错类**：不按"类"的框架组织、直接跳到具体方法；把**反问题**当**正向**建模 | ★ **没发生（3/3）**：三位**都选了"磨损累积律 + 反演"**这一**机理（mechanism）**族模型；**都把"从磨损反推人流"当反问题**处理 | 选 **mechanism**（主类）+ 参数辨识（反演） | ★ **预测被推翻**（两侧**选到同一类**：mechanism） |
| `P1b` | （§1 表未单列，**落地时补记**）**说不说得出"类"** | **R1：类词命中 0**；**R2/R3：命中 5 个类词**（§2） | **G1：8 个类词都在、且点名主类 `mechanism`×36**（§2） | ★ **拆开的现象**：**选对了类 ≠ 说得出类名**（R1 与 GREEN 同族模型，却一个类词也不给） |
| `P2` | **用不存在的函数**：MATLAB 里出现幻觉 / 拼错的函数名 ⇒ 运行报 `Undefined function` | ★ **没发生（3/3）**：三份入口代码**都 rc=0、实跑通过**（§2 的实跑读数） | ★ **没发生**：入口代码 rc=0（§3） | ★ **预测被推翻**（这一条本轮**两个预测位**都指向"会发生"，实测"没发生"）—— 见 §7 的"边界" |
| `P3` | **骨架跑不通**：代码跑不起来 / 跑不完 | ★ **没发生（3/3）**：三份入口代码**都 rc=0**、有输出（§2） | ★ **没发生**：入口代码 rc=0（§3） | ★ **预测被推翻** |
| `P4` | **把假设当已知**：把一批数值 / 关系当既成事实、**不单列假设** | ★ **没发生（3/3）**：三份产物**都有显式假设 / 局限节**（§2 的 `assum_head` 非空） | ★ 有显式假设节（§3） | ★ **预测被推翻** |
| `P5` | **无参数辨识**：不提"哪些参数从题面给不出来" | ★ **没发生（3/3）**：三份**都点了辨识问题**（R1「`b` 是辨识最弱的参数」；R2「`α/Δμ` 不可辨识 ⇒ 自信的错答案」；R3「纯磨损下人多人少不可辨识」） | ★ 点了（§3） | ★ **预测被推翻** |

★★ **一条必须写死的读法**（别把"预测被推翻"读成"本 skill 没用"）：**这五条预测是设计 §6 写死的"预期失败模式"，
本轮在这道题上"没发生"** —— 原因见 §7：**这道题（2025 A）的类与法几乎是"题面直接指出来"的**
（"踏面被磨凹" + "随时间累积" ⇒ 累积律 + 反演），**不够刁**，**不足以把本 skill 的价值区分出来**。
⇒ **本节结论的射程 = 这一道题、这一批写手；不许外推**（§7 的样本量边界）。

★ **另记一条 RED 侧的差异（机器读数，不是预测）**：**R1 产物里"类词"命中 0**（§2）——
它**给出的模型与 GREEN 同族，却没有用"类"这个词** ⇒ 说明**"能否明确点出类"在本轮 RED 里不稳**
（3 位里 1 位 0 命中、2 位有命中）。**本行不声称穷尽**：只报**实际抽到**的。

## §7 诚实边界

**这一节照 `TOPICSELECT-evidence.md` 的写法，逐条写清本轮测不到的东西。**

### 7.1 ★★ 本轮的"尺"只量机械层（`MS3` 那型的同族）

- `MS3` **判不了"参照是否真的独立"**（设计 §5 末写死）—— 它只判"参照记录在场 + 四要素齐"。
  ★ **本轮的 GREEN 用到了 `MS3` 覆盖的骨架**（它的推荐骨架 `param_id_stability.m`）；
  **GREEN 的 `MS3` 绿**只说明**那份参照记录在、四要素齐**，**不说明参照真的与骨架不同源**。
- ★ **同族**：**本轮的 GREEN 不代表真实赛期表现** —— 它只是**一份干净上下文写手用本 skill 产出的一次结果**。

### 7.2 ★★ 本轮测不到的真实赛期情形（M4 的对应物）

- **真实赛期是"题面刚放出、你手上还没有任何建模素材"**；而**本轮双方（RED/GREEN）都拿到了同一仓库**
  （写手是本机 Claude Code 的 agent，能看到 `corpus/**`、别的 skill、本仓的 git 历史）。
  ⇒ **本轮复现不了"零素材"那一情形**。**不声称覆盖真实赛期。**
- ★ **加剧这一条的**：**2025 A 的题面本身把"类"与"法"点得很明**（"踏面被磨凹" + "常年的磨损" ⇒ 累积律 + 反演）
  ⇒ **n = 1 道题的 RED，区分力天然弱**（见 §6）。

### 7.3 ★★ 样本量边界（**原话**）

> **本轮样本量：`n = 1` 道题（2025 MCM Problem A）× `3` 位 RED 写手 × `1` 位 GREEN 写手。**
> **n 小 ⇒ 本证据件里的任何"两侧都/都不"一律只是"这一次的读数"，不得写成"普遍规律"。**

### 7.4 ★★ 一条**不许**做的读法

- **不许**把本轮的"预测被推翻"读成**"写手不看 skill 也做得一样好"**：
  **3 位 RED 也都实跑了代码、都写了假设与辨识**是**这一道题**上的读数；**换一道更刁的题未必如此**（§7.2）。
- **不许**把 **GREEN 的 `MS1`–`MS6` 全绿**读成"GREEN 的产物质量被 `MS` 判据背书"：
  `MS` 判的是**skill 本体**（索引 / 骨架 / 参照 / 边界声明），**不判这份 `selection.md` 写得好不好**。
  ★ **GREEN 的产物没有任何一条 `MS` 判据去量它**（§5 的"不可比列"）。

## §8 可重放性（通则 14）—— 先干净 → 捕获 → 提交 → 再跑一次证不动点

- **本文件完全由生成器当场产出**：`python tests/skills/model-select/make-evidence.py`。
  ★ 它**实跑**：`check-model-select.py`（两次 · 含 `MS4` 的 MATLAB）＋ **四份入口代码各一次**（MATLAB）。
- **不动点的证法**：在**已提交的树上**重跑本生成器 ⇒ **本文件逐字节不变**（证法：跑后 `git status --short` 仍为空）。
  ★★ **边界（照实说）**：不动点依赖两件**不完全由本器控制**的事 ——（i）检查器的 `MS4` 每跑一次会**实调 MATLAB**（本机已知**退出期自崩**现象，见检查器“已知边界”第 5 条）：若某次自崩触发**有界重试**，该次 `MS4` 判词会**多一段重试回显** ⇒ 本文件**不再逐字节相等**；（ii）四份写手代码**实跑**：本轮**实测两跑逐字节相同**（§8 末的读数），但这是一个**观测事实、不是保证**。
- **判据非空泛（失败方向的另一条臂）**：`tests/skills/model-select/mutate-model-select.py` 的读数（**本生成器不执行该驱动器**，故**不声称当场跑过**；复跑命令见收工门）。它证明 `MS1`–`MS6` **逐条真红**、两条空集反证、四条“必须仍绿”对照。

## §9 生成器口径与数据来源（机器抽取）

- 生成器 `tests/skills/model-select/make-evidence.py` blob `6bfd25ade001`。
- 检查器 `.claude/skills/mcm-model-select/check-model-select.py` blob `a1aa85207606`（**本支不动它**）。
- brief blob `7882dc834476` · 题面 blob `2842d542e0d5`。
- 四臂产物的逐件 blob 见 §0 的表（`git hash-object`，**当场跑**）。
- ★ **本文件不声称穷尽**：机器抽取只覆盖 `probe_product` 抽的那几列 + 检查器判的那几条判据。
