# ARIMA / SARIMA（`arima_forecast.m`）

> **把非平稳序列"平稳化"后再建模型**：差分去掉趋势/季节，用 AR（自回归）+ MA（移动平均）刻画剩余相关结构，定阶、估计、给出**带预测区间**的预测。是时间序列预测的**标准统计框架**。

**归属**：类索引 `references/prediction.md` · 骨架 `assets/matlab/prediction/arima_forecast.m` · 参照 `tests/skills/model-select/verify/arima_forecast.md`。
★ **骨架与参照由本模块 Task 3 产出** —— **本文件只写六格，不重做骨架 / 参照**。

## ① 适用判据

- **用**：**单变量时间序列**、要**平稳化 + 差分 + 定阶**、要**短期预测与预测区间**；序列有自相关（不是白噪声）；样本量**中等以上**（阶数要能估出来）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **样本极少**（< ~30）⇒ 阶数与参数估不准 ⇒ 用灰模型 / 平滑（`references/prediction/gm11.md` · `references/prediction/exp_smoothing.md`）。
  2. **有外生自变量** ⇒ 用回归 / ARIMAX（`references/prediction/regression.md`）；纯 ARIMA 不含外生变量。
  3. **序列是纯白噪声** ⇒ 无自相关可建模，ARIMA 退化为常数。
  4. **关系强非线性** ⇒ ARIMA 是线性的 ⇒ 考虑神经网络预测（`references/prediction/nn_forecast.md`）。
  5. **不检验平稳性就定阶** ⇒ 差分阶数 `d` 选错、模型无意义（凭经验）。

## ② 标准建模步骤

1. **看图 / 检验平稳性**（ADF 检验、ACF 衰减）；不平稳 ⇒ **差分**，得 `d`（季节序列再用季节差分，得 SARIMA 的 `D`）。
2. **定阶**：看 ACF / PACF 或按信息准则（AIC/BIC）搜 `(p,d,q)`（季节版 `(p,d,q)(P,D,Q)_s`）。
3. **估计**参数（本骨架用内置 `arima` 类 + `estimate`）。
4. **诊断**：残差应为白噪声（Ljung-Box）。
5. **预测** `h` 步 + **预测区间**（用 `MSE` ⇒ 区间半宽）。
6. **滚动/样本外**评估覆盖率。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 序列 `y` · 阶数 `(p,d,q)`（· 季节 `(P,D,Q,s)`）· 预测步数 `h` |
| **输出** | 参数估计 · 预测值 `yf` · 预测 `MSE` ⇒ 预测区间 |

**显式假设（必须写进论文）**：
1. 差分后序列**平稳**（均值/方差/自相关结构不随时间变）。
2. 序列可被 **ARMA（线性、有限阶）** 近似。
3. 误差为**白噪声**（诊断可验）。
4. ★ **阶数 `(p,d,q)` 是显式选择**；不同准则（AIC vs BIC）可能给不同阶数。
5. **预测区间依赖"误差正态 + 参数已知"** 的近似（小样本下偏乐观）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **文件名是 `arima_forecast.m`、不是 `arima.m`**（**实测，非推断**）：MATLAB 的 `arima` 是**类文件夹里的构造器**（`...\toolbox\econ\econ\@arima\arima.m`），R2025b 上 **class-folder 优先于路径函数** ⇒ 名为 `arima.m` 的骨架文件**既不能按名调用、也不能 `run`**（会变成死文件、让 `MS4` 判**假绿**）⇒ 改名 `arima_forecast.m` 以正常调用内置 `arima` 类。（详见 `MAP.md` 的订正段与参照记录。）
2. ★ **不检验平稳性、乱差分**：`d` 过大 ⇒ 过度差分、方差膨胀（凭经验）。
3. ★ **预测区间覆盖率不核**：名义 95% 的区间应覆盖约 95%。**实测**（骨架参照件 `tests/skills/model-select/verify/arima_forecast.md`）：一步 95% 区间覆盖率 `0.9453`（5 种子均值），落在名义 `0.95` 的 1 个二项标准误内。
4. **系数不核反估**：**实测**（同参照件）：已知 AR(2) 真值 `c=0.1, a=[0.5,0.2]`，估计回到 `c=0.1181, a=[0.5287,0.1826]`（差 ≲ 2 个抽样标准误）。
5. **阶数靠"跑很多组合挑 AIC 最小"而不报搜索范围** ⇒ 不可复现（凭经验）。

## ⑤ 输出模板

- **模型阶数 + 参数表** + **残差诊断**（自相关/Ljung-Box）+ **预测值 + 预测区间** + （如做）覆盖率。
- 预测曲线（含区间带）→ `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；参数表 / 预测表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/prediction/arima_forecast.m`（**零参可跑**，已知 AR(2) 合成数据 + 系数反估 + 区间覆盖率；由 **Task 3** 产出）。

关键片段（**不整份复制**；完整实现见上述路径）：
```matlab
Mdl = arima(2, 0, 0);                    % (p,d,q) = (2,0,0)
Est = estimate(Mdl, y, 'Display', 'off');
[yf, yMSE] = forecast(Est, h, 'Y0', ytr);
lo = yf(end) - zc*sqrt(yMSE(end));       % zc = -norminv(alpha/2) = 1.95996
hi = yf(end) + zc*sqrt(yMSE(end));
```
**独立参照**：`tests/skills/model-select/verify/arima_forecast.md`（**第 4 类：已知参数的合成数据**；**由 Task 3 产出**）。

## 语料面（P6）

- **语料指针（带）**：`corpus/papers/MODEL_MAP.md` 里 3 行 —— `ARIMA`（`:75` 1 篇 · `:122` 5 篇）、`SARIMA`（`:141` 2 篇）；**去重后 7 篇**（`P2025-B-01` · `C-04` · `C-05` · `C-06` · `C-11` · `C-12` · `C-16`）。
  （当场 `grep -nE "^ +- .*(ARIMA|SARIMA)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 3 行，篇数 `1 + 5 + 2 = 8`、按题目去重为 `7`。）
- **算法素材面**：`corpus/algorithms/src/`（脚本素材面）`ARIMA` / `arima` **0 命中**（当场 `grep -rliE "arima" corpus/algorithms/src/ | wc -l` ⇒ `0`）—— ★ **素材 0 ≠ 语料 0**（GC15/P6）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
