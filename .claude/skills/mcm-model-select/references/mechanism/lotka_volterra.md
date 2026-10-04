# 生态动力学（Lotka-Volterra）（`lotka_volterra.m`）

> **给"捕食-被捕食 / 竞争"的种群题用**：两类（或多类）种群互相作用，增长与相遇项写出 `dx/dt = alpha x - beta x y`、`dy/dt = -gamma y + delta x y`，求轨线、平衡点与周期性。

**归属**：类索引 `references/mechanism.md` · 骨架 `assets/matlab/mechanism/lotka_volterra.m` · 参照 `tests/skills/model-select/verify/lotka_volterra.md`（**Task 1 已交付、已过独立复核**）。
★ **与相邻方法的边界**：**人群仓室传播**（SIR/SEIR）⇒ `references/mechanism/sir_seir.md`；**竞争 / 捕食参数未知、从数据反推** ⇒ `references/mechanism/param_id_stability.md`；**含空间扩散**（反应扩散 / 空间生态）⇒ `references/mechanism/reaction_diffusion.md`。

## ① 适用判据

- **用**：题面是**多物种相互作用**（捕食-被捕食、竞争、共生），要**长期轨线、周期、平衡点**，或要**守恒量 / 时间平均**这类解析性质；数据面常见于生态、渔业、资源管理。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **单种群 logistic 增长**（无相互作用）⇒ 用 logistic（见 `references/mechanism/param_id_stability.md` 的算例），不必上 LV。
  2. **要刻画空间分布 / 扩散**⇒ 加扩散项，走 `references/mechanism/reaction_diffusion.md`。
  3. **参数未知、要从观测反推** ⇒ 先做参数辨识（`references/mechanism/param_id_stability.md`）。
  4. **随机环境 / 小种群灭绝** ⇒ 确定性 LV 给不了灭绝概率，走随机 / 仿真（`references/simulation/monte_carlo.md`）。
  5. **"竞争"其实是无相互作用的资源分配** ⇒ 可能是 optimization，不是动力学。

## ② 标准建模步骤

1. **定种类与作用**：捕食者 `y`、被捕食者 `x`（竞争则都取正相互作用符号）。
2. **写方程**：`dx/dt = alpha x - beta x y`，`dy/dt = -gamma y + delta x y`（符号见物理含义）。
3. **定参数与初值**：`alpha/beta/gamma/delta`、`(x0,y0)`。
4. **求平衡点**：解右端 = 0，得 `(0,0)` 与 `(gamma/delta, alpha/beta)`。
5. **判类型**：经典 LV 的共存平衡点是**中心型**（线性化特征值为纯虚数）⇒ 周期解族。
6. **数值积分**（`ode45`）得轨线。
7. **数值验证**（★ 见 ⑥）：**第一积分（守恒量）** 应守恒；**周期解时间平均** 应趋近平衡点。
8. **报告**：相图（`y vs x`）+ 时间序列 + 平衡点 + 守恒量漂移。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | `alpha`（被捕食内禀增长）· `beta`（被捕食率）· `gamma`（捕食者死亡）· `delta`（捕食转化）· 初值 `(x0,y0)` · 时间区间 `T` |
| **输出** | 轨线 `x(t),y(t)` · 平衡点 · 守恒量漂移 · 时间平均 |

**显式假设（必须写进论文）**：
1. **连续、确定性**：种群连续变化、无随机（大种群近似）。
2. **均匀混合**：捕食者与被捕食者相遇率正比于两者密度之积（`x y` 项）。
3. **参数定常、无环境容量上限**（无 logistic 饱和项；有容量则改方程）。
4. **无空间结构**（空间均匀，无迁移 / 扩散）。
5. **时间尺度足够长**时周期解的时间平均趋近平衡点（本骨架 `T=200`）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **守恒量漂移被当成"模型对"**：第一积分守恒只验证**数值积分质量**，不验证**参数 / 方程是否合适**。**实测**（Task 1）：`max|H(t)-H0|=2.813e-10`（`H0=2.23082925301173`）⇒ **周期解存在性成立**。
2. ★ **时间平均不是精确等于平衡点**：有限时窗下有残差。**实测**（Task 1）：`x_bar=1.00441452`（平衡点 1，差 `4.4e-03`）、`y_bar=0.995757613`（差 `4.2e-03`）⇒ **不声称精确相等**。
3. **把"平衡点是中心型"误判成渐近稳定**：中心型的轨线**环绕**平衡点、不收敛 ⇒ 用"特征值实部 <0"判稳定会判错（凭经验 + 线性化分析）。
4. **长期积分误差累积**：LV 无耗散，数值格式的假耗散 / 假增能会让轨线螺旋进 / 出 ⇒ 长时窗要收紧容差并盯守恒量（凭经验）。
5. ★ **拿 `ode45` 当"独立参照"**：真参照是**守恒量 / 时间平均**这类**解析性质**（Task 1 口径）。
6. **符号写反**：`-gamma y` 与 `+delta x y` 的符号决定谁是捕食者；写反会得到非物理轨线（凭经验）。

## ⑤ 输出模板

- **相图**（`y vs x` 闭合轨线）+ **时间序列图** + **平衡点 / 守恒量表**。
- 图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；读数表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/mechanism/lotka_volterra.m`（**零参可跑**，自带算例 `alpha=beta=gamma=delta=1, (x0,y0)=(0.5,0.75), T=200`）。

关键片段（**不整份复制**）：
```matlab
lv = @(t,z) [ alpha*z(1) - beta*z(1)*z(2); -gamma*z(2) + delta*z(1)*z(2) ];
[t, z] = ode45(lv, [0 T], [x0; y0], oset);
Hfun = @(x,y) delta*x - gamma*log(x) + beta*y - alpha*log(y);  % 第一积分
Hdrift = max(abs(Hfun(z(:,1),z(:,2)) - H0));                   % 应 ~ 容差量级
```
**独立参照**：`tests/skills/model-select/verify/lotka_volterra.md`（**解析性质** —— 守恒量 + 平衡点 + 时间平均；**实测** `H` 漂移 `2.813e-10`、`x_bar` 差 `4.4e-03`、`y_bar` 差 `4.2e-03`）。
★ **起点素材**：无（Task 1 已确认 `corpus/algorithms/src/` 里 LV 为 0；本类为 `补`）。

## 语料面（P6）

- **语料指针（带）**：`corpus/papers/INDEX.md` 的 **P2025-B-03 / E-02 / E-03 / E-04 四篇**在用 Lotka-Volterra（`MODEL_MAP.md` 里 `Lotka-Volterra` 命中 **4 篇**；当场 `grep -nE "^ +- .*Lotka-Volterra（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ **2 行**，篇数 `1 + 3 = 4`）。★ **订正（2026-10-04 M4 终审 W-2）**：本处**原写** `grep -nE "^ +- .*Lotka"`（**少了 `（[0-9]+ 篇）` 锚**）⇒ 实测 **3 行**（`:840` 是关键词明细行也命中）⇒ **命令已补锚**（篇数 `4` 不变）。
  ★ **口径订正（2026-10-04 Task 8 复核 Q3）**：本行**原写** `grep -c "Lotka"` 的"**19 行**"（承接 Task 1）—— 那是**裸模式**，含聚合表行与关键词行。**已改带锚形**（全库唯一两处裸 `grep -c` 之一）。
  ★ **口径（GC15）**：**"素材 0" ≠ "语料 0"** —— `corpus/algorithms/src/` 里 LV 素材确为 0，但**获奖论文语料里 4 篇在用**。
- **算法素材面**：**0**（`corpus/algorithms/src/` 里 LV 素材确为 0）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
