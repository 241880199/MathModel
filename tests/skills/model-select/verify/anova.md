# 参照记录 · `anova`（方差分析）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/statistics/anova.m`
**语料面（P6）**：**带语料指针（薄）** —— `corpus/papers/MODEL_MAP.md` 里 `analysis of variance` 命中 **1 篇**
（P2025-C-18；其正文有 `## Analysis of Variance, Mixed-effects Model` 一节，2026-10-04 当场复跑
`grep -nE "^ +- .*analysis of variance（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行）。
★ **薄**：仅 1 篇。`corpus/algorithms/src/`（**脚本素材面**）0 命中
（`grep -rliE "ANOVA|方差分析|analysis of variance" corpus/algorithms/src/ | wc -l` ⇒ `0`）。

## ① 参照类型
**第 4 类：已知参数的合成数据**（GC6）；`F` 统计量另与**手算的平方和分解**逐一对照。

## ② 参照来源
- **各组真均值相同**（H0 为真）：5% 水平下**拒绝率应 ≈ 0.05**（单因素 F 检验的名义水平）。
- **各组真均值有已知差**（H1 为真，组均值偏移 `[0, 0.4, 0.8]`）：`p` 应 `< alpha`、拒绝率 = 功效。
- **`F` 的手算式**（单因素，`k` 组、`N` 总样本）：`SSB = Σ_i n_i (x̄_i - x̄)^2`，
  `SSW = Σ_i Σ_j (x_ij - x̄_i)^2`，`F = (SSB/(k-1)) / (SSW/(N-k))`，`p = 1 - F_cdf(F; k-1, N-k)`。
- 参照与骨架**不同源**：理论拒绝率与平方和定义式都独立于 `anova1` 的内部实现。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/statistics'); anova"
```

## ④ 两边读数（`alpha=0.05`, `nrep=2000`, `nper=10`, `delta=0.8`, `seeds=0:4`）
| 量 | 骨架 | 参照 | 差 |
| :--- | :--- | :--- | :--- |
| H0 单因素 anova1 拒绝率（5 种子均值 ± 标准差） | `0.0499 ± 0.0066` | `0.05` | `0.0001` |
| H1 单因素 anova1 拒绝率（功效，组均值 `[0,0.4,0.8]`） | `0.3071` | `>> 0.05` | — |
| `F`（`anova1` 返回） | `0.451395878` | `F`（手算 SSB/SSW 分解）`0.451395878` | `0`（逐位相同） |
| 双因素 anova2 行因素 `p_A`（已知效应 1.0） | `0.00951269` | `< alpha` | — |
| 双因素 anova2 列因素 `p_B`（已知效应 1.5） | `0.016101` | `< alpha` | — |

**多次运行的分布（5 个种子）H0 拒绝率逐种子** = `[0.0460, 0.0465, 0.0440, 0.0530, 0.0600]`（均值 `0.0499`，标准差 `0.0066`）。

**结论**：H0 为真时单因素检验的经验拒绝率落在名义水平 `0.05` 附近；
`anova1` 返回的 `F` 与手算的平方和分解式**逐位相同**（差 `0`）⇒ 统计量算得对；
H1 为真时功效显著高于 `0.05`；双因素两主效应 `p` 均 `< alpha`。
