# 传染病模型（SIR / SEIR）（`sir_seir.m`）

> **给"人群按仓室流转"的传播类题用**：把人群分成 S（易感）/ I（感染）/ R（移除）——SEIR 再加 E（潜伏）——按接触与恢复速率写出仓室间的流转方程。

**归属**：类索引 `references/mechanism.md` · 骨架 `assets/matlab/mechanism/sir_seir.m` · 参照 `tests/skills/model-select/verify/sir_seir.md`（**Task 1 已交付、已过独立复核**）。
★ **与相邻方法的边界**：**物种竞争捕食**（不是人群仓室）⇒ `references/mechanism/lotka_volterra.md`；**传播参数未知、要从数据反推** ⇒ `references/mechanism/param_id_stability.md`；**个体级接触规则**（不是仓室聚合）⇒ `simulation` 类（`references/simulation/abm.md`）。

## ① 适用判据

- **用**：题面是**传染病 / 谣言 / 信息扩散**，人群可分成"状态仓室"（S/E/I/R），要**随时间演化的感染曲线、峰值、最终规模**，或要**基本再生数 `R0` 阈值**判断扩散 / 消退。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **要刻画个体异质接触网络**（超级传播者、社区结构）⇒ 仓室模型的**均匀混合假设不成立** ⇒ 走网络 / ABM（`references/simulation/abm.md`）。
  2. **种群竞争捕食**（两类生物互相吃）⇒ 模型形态不同，走 `references/mechanism/lotka_volterra.md`。
  3. **参数不知道、只有观测数据** ⇒ 先做参数辨识（`references/mechanism/param_id_stability.md`），别凭空设 `beta/gamma`。
  4. **无"传播"机理、只有病例序列** ⇒ 走 `prediction` 类（时间序列外推）。
  5. **把仓室当"随机过程"**：确定性 SIR 给的是期望性态，小种群要随机模型（凭经验）。

## ② 标准建模步骤

1. **定仓室**：SIR（三仓）还是 SEIR（四仓，含潜伏）。
2. **写流转项**：`S→I`（接触感染，速率 `beta S I / N`）· `E→I`（潜伏，`sigma E`）· `I→R`（恢复，`gamma I`）。
3. **归一化**：取分数形式，保证 `S+I+R=1`（SIR）/ `S+E+I+R=1`（SEIR）。
4. **定初值与参数**：`beta`、`gamma`（、`sigma`）、`I0`；由文献 / 数据估。
5. **求 `R0 = beta/gamma`**，判扩散（`R0>1`）还是消退。
6. **数值求解**（`ode45`）得曲线。
7. **数值验证**（★ 见 ⑥）：守恒量守恒 + **最终规模方程**的根 vs 数值末态。
8. **报告**：感染曲线 + `R0` + 峰值 / 最终规模。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | `beta`（接触传染率）· `gamma`（恢复率）· （SEIR）`sigma`（潜伏率）· `I0` · 时间区间 `T` |
| **输出** | S/E/I/R 曲线 · `R0` · 守恒量 · 最终规模 |

**显式假设（必须写进论文）**：
1. **均匀混合**（well-mixed）：任意两人接触概率相同（无空间 / 网络结构）。
2. **封闭人口**（无出生死亡、无迁入迁出）：所以 `S+I+R ≡ const`（归一化后 ≡1）。
3. **仓室内同质**：同仓室成员传染 / 恢复率相同。
4. **参数定常**：`beta`、`gamma` 不随时间变（无干预、无季节）。
5. **恢复即免疫**（不返 S）；要"可再感染"须改 SIS / SIRS。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把守恒量当"模型用对了"的证据**：守恒量只验证**数值积分有没有漏项**，**不验证参数 / 仓室划分合适**。**实测**（Task 1）：`max|S+I+R-1|=1.554e-15`、`max|S+E+I+R-1|=1.332e-15`（机器精度）。
2. ★ **最终规模方程的口径**：`ln(s0/s_inf)=R0(1-s_inf)` 用 `fzero` 解出的 `s_inf` 应与数值末态一致。**实测**（Task 1）：数值末值 `0.0594477683271942` vs 解析根 `0.0594477683162695`，差 `1.092e-11` ⇒ 强独立佐证。
3. **`R0` 与 `beta/gamma` 混用**：`R0` 的定义依模型而异（SEIR 加潜伏时前提不同），论文里要写清本模型的 `R0` 表达式（凭经验）。
4. **初值 `I0` 取 0**：`I0=0` 系统不动（无疫情），数值上也看不到增长 ⇒ 取小正数（本骨架 `I0=1e-3`）（凭经验）。
5. ★ **拿 `ode45` 当"独立参照"**：它只是实现；真参照是**守恒律 + 最终规模解析方程**（Task 1 口径）。
6. **把仓室人数与分数混算**：`N` 归一化与不归一化两种写法别混（凭经验）。

## ⑤ 输出模板

- **感染曲线图**（S/E/I/R 同图多条线）+ **参数与阈值表**（`beta/gamma/sigma`、`R0`、峰值、最终规模）。
- 图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；参数 / 结果表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/mechanism/sir_seir.m`（**零参可跑**，自带算例 `beta=0.6, gamma=0.2, I0=1e-3`；SIR 与 SEIR 双算例）。

关键片段（**不整份复制**）：
```matlab
sir = @(t,y) [ -beta*y(1)*y(2); beta*y(1)*y(2) - gamma*y(2); gamma*y(2) ];
[~, ys] = ode45(sir, [0 T], [1-I0; I0; 0], oset);
cons_sir = max(abs(sum(ys,2) - 1));           % 守恒量
R0 = beta/gamma;                              % 基本再生数
g  = @(s) log(s0./s) - R0*(1 - s);            % 最终规模方程，fzero 解 s_inf
```
**独立参照**：`tests/skills/model-select/verify/sir_seir.md`（**解析性质** —— 守恒量 + `R0` 阈值 + 最终规模方程；**实测** `R0=3`、守恒量 `1.554e-15`/`1.332e-15`、`s_inf` 两侧差 `1.092e-11`）。
★ **起点素材**：无（Task 1 已确认 `corpus/algorithms/src/` 里 SIR/SEIR 为 0；本类为 `补`）。

## 语料面（P6）

- **语料指针（无）**：`corpus/papers/MODEL_MAP.md` 里 `SIR model` / `SEIR` **0 命中**（承接 Task 1；当场复跑 `grep -inE "SIR model|SEIR" corpus/papers/MODEL_MAP.md` ⇒ 0 行）⇒ 标 `[社区]` + **教科书级常识**。
  ★ **注**：全库 `corpus/papers/` 检索 `seir` 唯一命中是一个 PNG 的**二进制假匹配**，非文本（承接 Task 1）。
- **算法素材面**：**0**（Task 1 已确认）—— 本方法属 `补`；`ode45` **只作实现，非独立参照**。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
