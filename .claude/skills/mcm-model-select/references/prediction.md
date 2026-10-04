# prediction —— 类索引（**第二跳**：预测与外推）

**上位**：`SKILL.md` 的第一跳决策树把「**要预测未来值 / 外推趋势 / 补全缺失数据**」的题面指到本类。
**本文件是第二跳**：**入口 = 类内的方法特征**；**叶 = 一个方法**（→ `references/prediction/<方法>.md`）。**一方法一文件**。

**类级适用判据**：题面要**从历史 / 采样数据推出未来值、趋势、缺失点或平滑序列**（时间序列或空间网格）。
**类级反面（什么时候不该用这一类）**：要**解释变量间的因果 / 群体差异** ⇒ `statistics`；要**学出分类/回归函数**（非序列）⇒ `ml`；**有确定机理方程** ⇒ `mechanism`（本类不假设机理）。

## 类内判据树（第二跳；节点 = 一问 + 判据 + 指向的方法，叶 = 一个方法）

- **问 1：数据量 / 信息形态？**
  - **样本很少（≥4 个点）、只求趋势** ⇒ **灰色预测 GM(1,1)** → `references/prediction/gm11.md`
  - **序列有增长上限 / S 形饱和** ⇒ **灰色 GM(2,1) / Verhulst** → `references/prediction/gm21_verhulst.md`
  - **有明确的自变量-因变量关系（非纯时间）** ⇒ **回归预测** → `references/prediction/regression.md`
  - **关系强非线性、不想设解析式** ⇒ **神经网络预测** → `references/prediction/nn_forecast.md`
- **问 2：时间序列怎么处理？**
  - **要短期平滑、对新近数据加权** ⇒ **指数平滑** → `references/prediction/exp_smoothing.md`
  - **要消除随机波动、看均值走势** ⇒ **移动平均** → `references/prediction/moving_average.md`
  - **要沿明显趋势外推** ⇒ **趋势外推** → `references/prediction/trend_extrapolation.md`
  - **要自适应跟踪变化、抑制噪声** ⇒ **自适应滤波** → `references/prediction/adaptive_filtering.md`
  - **要平稳化 + 差分 + 定阶 + 预测区间** ⇒ **ARIMA / SARIMA** → `references/prediction/arima_forecast.md`
- **问 3：要的是"补点 / 加密网格"而不是"未来"？**
  - **是（数据补全 / 网格化）** ⇒ **插值** → `references/prediction/interpolation.md`

## 方法清单（**三列** · 与 `assets/matlab/MAP.md` 逐行一致）

| 中文名 | ASCII 文件名 | 六格文件路径 |
| :--- | :--- | :--- |
| 灰色预测 GM(1,1) | `gm11.m` | `references/prediction/gm11.md` |
| 灰色 GM(2,1) / Verhulst | `gm21_verhulst.m` | `references/prediction/gm21_verhulst.md` |
| 指数平滑 | `exp_smoothing.m` | `references/prediction/exp_smoothing.md` |
| 移动平均 | `moving_average.m` | `references/prediction/moving_average.md` |
| 趋势外推 | `trend_extrapolation.m` | `references/prediction/trend_extrapolation.md` |
| 自适应滤波 | `adaptive_filtering.m` | `references/prediction/adaptive_filtering.md` |
| 回归预测 | `regression.m` | `references/prediction/regression.md` |
| 神经网络预测 | `nn_forecast.m` | `references/prediction/nn_forecast.md` |
| 插值（数据补全 / 网格化） | `interpolation.m` | `references/prediction/interpolation.md` |
| ARIMA / SARIMA | `arima_forecast.m` | `references/prediction/arima_forecast.md` |

★ **行数 = 10 = 本类花名册项数**。★ **本清单不声称穷尽**。
★ **与 `ml` 的边界**：本类的**神经网络预测**管「**序列预测**」；`ml` 的**神经网络分类**管「**类别判别**」—— 两条边界在各方法文件里写明。
★ **与 `statistics` 的边界**：**回归预测**留本节（预测任务）；统计侧只把「回归诊断」当作统计方法的一部分、**不另立条目**。
★ **第二跳与第一跳同构**：入口换成**类内方法特征**，叶 = 一个方法。
