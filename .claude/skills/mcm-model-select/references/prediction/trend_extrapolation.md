# 趋势外推（`trend_extrapolation.m`）

> **先拟合一条趋势曲线、再沿它外推**：把序列拟合成直线 / 多项式 / 指数 / logistic 曲线，然后用拟合出的曲线**向前推**未来值。核心是"趋势形态选对"。

**归属**：类索引 `references/prediction.md` · 骨架 `assets/matlab/prediction/trend_extrapolation.m` · 参照 `tests/skills/model-select/verify/trend_extrapolation.md`。

## ① 适用判据

- **用**：序列有**明确、稳定且平滑的趋势**（线性 / 多项式 / 指数 / 饱和），要**外推若干步**；趋势形态能从数据/业务判出来。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **序列无明显趋势、只有波动** ⇒ 用移动平均 / 指数平滑（`references/prediction/moving_average.md` · `references/prediction/exp_smoothing.md`）。
  2. **拟合曲线被外推到数据范围之外很远** ⇒ **多项式阶数越高外推越发散**，高次多项式**绝不可**用于远外推（数值不稳定，见 ④-2）。
  3. **趋势会拐弯 / 饱和** ⇒ 用 logistic/Gompertz 或 Verhulst（`references/prediction/gm21_verhulst.md`），别用线性硬推。
  4. **序列是随机的、没有可外推的机制** ⇒ 外推只是"把过去的斜率画出去"，须明确这是强假设。

## ② 标准建模步骤

1. **看图 / 看差分判形态**：一阶差分近常数 ⇒ 线性；二阶差分近常数 ⇒ 二次；对数近线性 ⇒ 指数；接近上下限 ⇒ logistic/Gompertz。
2. **选趋势族**并拟合参数（线性 / 多项式用最小二乘 `polyfit`；指数对 `log y` 线性拟合；logistic 对 `logit(y/K)` 线性拟合 —— `K` 是**外部给的饱和值**）。
3. **诊断拟合**：残差应无残存趋势；`R²` 仅供参考（外推不看 `R²`）。
4. **外推**：`y(t0+h) = 曲线(t0+h)`。
5. ★ **敏感性**：给趋势族 / `K` 做灵敏度分析（换一个 `K` 外推会差多少）。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | `y`（1×n）· `t`（时间轴，默认 `1:n`）· 外推步数 `h` ·（logistic）饱和值 `K` |
| **输出** | 各趋势族的参数与**外推值** |

**显式假设（必须写进论文）**：
1. **趋势形态在预测期内不变**（这是外推**最关键也最脆弱**的假设）。
2. **线性/多项式**：用**最小二乘**；**指数**：乘性误差、对 `log y` 线性；**logistic**：`K` 是**先验给定**的饱和值，**不是**从数据估的（数据估的版本更麻烦、易不稳）。
3. 外推步数 `h` 应**远小于**样本跨度（否则外推误差不可控）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **线性的手算值**：小序列 `t=1..5`、`y=[3 5 6 9 10]`，最小二乘给 `a = 1.2`、`b = 1.8`，外推 `t=6` ⇒ `y = 12.0`。**实测**（本骨架 `trend_extrapolation.m`）：`a=1.2, b=1.8, y(6)=12`。
2. ★ **高阶多项式外推发散**：**实测**（本骨架同一数据）—— 二次拟合 `coef = [3.97e-16, 1.8, 1.2]`，一步外推仍是 `12`（因为该数据本就是直线、二次项系数 ≈ 0）；但**若数据非严格线性，二阶项会显著、再往外推几步就迅速发散**。⇒ 高次多项式**只用于插值/内插**，**不用于外推**。
3. **指数外推比线性快得多**：同数据下指数外推 `y(6)=14.86` vs 线性 `12` — 趋势族选错，外推值差很大（实测）。**必须在论文里给趋势族的选取依据**。
4. **logistic 的 `K` 拍脑袋**：`K` 不同 ⇒ 曲线形状与外推都不同（本骨架默认 `K = 1.2·max(y)`，仅示例）⇒ 须做灵敏度（凭经验）。
5. **只看 `R²` 选模型**：`R²` 高不代表外推准（凭经验）。

## ⑤ 输出模板

- **趋势参数表**（各族参数）+ **外推值**（标注趋势族与 `h`）+ （logistic）`K` 的取值依据。
- 拟合-外推曲线图（含外推区标注）→ `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；参数/外推表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/prediction/trend_extrapolation.m`（**零参可跑**，含线性 / 二次 / 指数 / logistic 四族对照）。

关键片段（**不整份复制**）：
```matlab
p1 = polyfit(t, y, 1);  a = p1(2); b = p1(1);       % 线性
lin_fc  = polyval(p1, t(end) + h);
p2 = polyfit(t, y, 2);  poly_fc = polyval(p2, t(end) + h);   % 二次
pe = polyfit(t, log(y), 1);  exp_fc = exp(polyval(pe, t(end)+h));  % 指数
pl = polyfit(t, log(y./(K - y)), 1);                 % logistic（需给 K）
logi_fc = K / (1 + exp(-(pl(2) + pl(1)*(t(end)+h))));
```
**独立参照**：`tests/skills/model-select/verify/trend_extrapolation.md`（**第 3 类：手算标准算例**，线性最小二乘逐步算式）。

## 语料面（P6）

- **语料指针**：`corpus/papers/MODEL_MAP.md` 里 `trend extrapolation` **0 命中**（当场 `grep -nE "^ +- .*trend extrapolation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）⇒ **标 `[社区]` + 教科书级常识**。
- **算法素材面**：`corpus/algorithms/src/TimeSeries时间序列函数/趋势外推预测法/`（含 `predict1.m` / `logistic_curve.m` / `compertz_curve.m` / `modified_exponential_curve.m`）与 `corpus/algorithms/fixed/trend_extrapolation.m`（净室重写版）—— 教辅级**起点素材**，**不作独立参照**。
- ★ **素材 0 ≠ 语料 0**：**素材面有**（上述目录）、**语料面 0** —— 两面分开说（GC15/P6）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
