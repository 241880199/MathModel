# 排队论（`queueing.m` · M/M/1）

> **题面有"随机到达 + 排队 + 服务"结构时用**：到达是随机的、服务要花时间、超出容量就等 ⇒ 用排队模型算队长 / 等待 / 利用率。
> ★ **本项属低使用度**（`corpus/papers/MODEL_MAP.md` 里 `queueing theory` 仅 **1 篇**）—— **照补是为覆盖面，不是"常用"**。

**归属**：类索引 `references/simulation.md` · 骨架 `assets/matlab/simulation/queueing.m`（**Task 3 已交付**）· 参照 `tests/skills/model-select/verify/queueing.md`（**Task 3 已交付、已过独立复核**）。
★ **与相邻方法的边界**：要"按局部规则推演空间 / 时间演化" ⇒ `references/simulation/cellular_automata.md`；对随机量做大量抽样估计 ⇒ `references/simulation/monte_carlo.md`；个体各自规则互动、涌现宏观行为 ⇒ `references/simulation/abm.md`。

## ① 适用判据

- **用**：有**到达过程** + **服务过程** + **排队规则**；关心 `L`（系统内队长）/ `Lq`（排队队长）/ `W`（逗留时间）/ `Wq`（等待时间）/ `ρ`（利用率）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **有确定的闭式动力学**（方程可解）⇒ 走 `mechanism`，别用排队论硬套。
  2. **只需对随机量抽样估一个期望**⇒ 走 `monte_carlo`。
  3. **服务台异构、个体有各自策略**（互动、涌现）⇒ 走 `abm`。
  4. **到达 / 服务非 Poisson / 指数而硬套 M/M/1 公式** ⇒ 结论错（凭经验）。
  5. **系统不稳定**（`λ ≥ μ`）仍套 `ρ < 1` 的闭式 ⇒ 无意义（等式里的分母失灵）。

## ② 标准建模步骤

1. **定到达过程**（通常 Poisson，率 `λ`）、**服务过程**（通常指数，率 `μ`）、**服务台数** `c`、队列容量、排队规则（FCFS…）。
2. **算利用率** `ρ = λ/(cμ)`；核 `ρ < 1`（稳定前提）。
3. **选模型**：M/M/1 / M/M/c / M/G/1 —— 取闭式，或写**离散事件仿真**。
4. **求指标**：`L` / `Lq` / `W` / `Wq` / `ρ`。
5. **数值验证**（★ 见 ⑥）：仿真 vs **闭式解析**。
6. **报告**：指标表（闭式 vs 仿真）+ 分布图 + 参数与稳定条件。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | `λ` · `μ` · 服务台数 `c` · 队列容量 · 排队规则 · 仿真长度 · 预热段 · 种子 |
| **输出** | `ρ` · `L` · `Lq` · `W` · `Wq`（+ 仿真的多次运行分布） |

**显式假设（必须写进论文）**：
1. **Poisson 到达 / 指数服务**（M/M/* 的 `M` 就是 Markov）；否则换 M/G/1 或纯仿真。
2. **FCFS** 排队、容量无限（或写明有限 + 丢包 / 阻塞规则）。
3. **稳态**：`ρ < 1`；分析的是一段稳态区间（有预热段）。
4. **到达间隔与服务时长独立同分布**（且相互独立）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把低使用度写成"常用"**：**实测**（2026-10-04 带锚复跑）`corpus/papers/MODEL_MAP.md` 里 `queueing theory` 仅 **1 篇**（`P2025-D-01`）⇒ **不许写成"常用"**（P5，见 `SKILL.md` 口径与不做表）。
2. ★ **拿单次仿真当结论**：必须**固定种子 + 多次运行给分布**（本骨架 5 个种子）。
3. ★ **忽略预热段**：有限样本偏差会让 `L` 偏低。**实测**（Task 3）：初版 `M = 2e5` 时 `L` 偏低约 `2.3%`，`M = 1e6` 后降到 `1.3e-3`。
4. ★ **系统不稳定仍套闭式**（`λ ≥ μ`）：本骨架会**报错拦截**（`queueing:unstable`），不要绕过。
5. **有限队列容量 / 排队规则未写明** ⇒ 结论不可用（凭经验）。

## ⑤ 输出模板

- **指标表**（`ρ` / `L` / `Lq` / `W` / `Wq`，**闭式 vs 仿真**两列）+ 队长分布图 / 等待时间分布图。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/simulation/queueing.m`（**零参可跑**；★ **Task 3 已交付**，本文件只补六格，**不重做骨架**）。

关键片段（**不整份复制**）：
```matlab
rho = lambda / mu;  L = rho/(1-rho);  Lq = rho^2/(1-rho);   % 闭式
W = L/lambda;  Wq = Lq/lambda;
% 离散事件（Lindley 递推）：start(i) = max(arr(i), dep(i-1)); dep(i) = start(i)+S(i);
```
**独立参照**：`tests/skills/model-select/verify/queueing.md`（**第 1 类：M/M/1 闭式 `L/W/ρ`**；★ **承 Task 3、读数一致** —— `L_sim = 4.0053 ± 0.0718` vs 闭式 `4.0`；`W_sim = 5.0042 ± 0.0817` vs `5.0`）。
★ **起点素材**：无（`corpus/algorithms/src/` 排队论 **0 实质命中**）。

## 语料面（P6）

- **带语料指针（薄）**：`corpus/papers/MODEL_MAP.md` 里 `queueing` 带锚 **1 行 / 1 篇**（`:216` `queueing theory（1 篇）：P2025-D-01`）。
  ★ **承 Task 3（`tests/skills/model-select/verify/queueing.md`）、读数一致**；Task 3 用的**就是带锚形**（`grep -nE "^ +- .*queueing.*（[0-9]+ 篇）"`）⇒ **无需改口径**。
- **算法素材面**：`corpus/algorithms/src/` 排队论 **0 实质命中**（唯一 `queue` 命中是 `corpus/algorithms/src/GraphTheory(图论)/detailed/树/BFS.m` 里的 BFS 队列变量，非排队论）。
- ★ **低使用度**（P5）：照补是为覆盖面，**不是"常用"**。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**："queueing 还有哪些写法"不声称覆盖。
