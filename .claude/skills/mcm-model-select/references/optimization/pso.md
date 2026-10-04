# 粒子群 PSO（`pso.m`）

> **连续空间、要群体协作搜索时用**：一群"粒子"各有位置与速度，靠**个体最优 `pbest` + 群体最优 `gbest`** 相互牵引，边飞边收敛。实现短、无需梯度；代价同族：**结果随随机数变**，固定种子 + 多运行。

**归属**：类索引 `references/optimization.md` · 骨架 `assets/matlab/optimization/pso.m` · 参照 `tests/skills/model-select/verify/pso.md`。
★ **与相邻方法的边界**：要"免疫记忆 / 浓度抑制" ⇒ `references/optimization/immune.md`；要"鱼群聚群/追尾/觅食" ⇒ `references/optimization/afsa.md`。

## ① 适用判据

- **用**：**连续**变量的全局寻优（函数优化、参数标定）；目标可微但梯度难用 / 有多个局部极值；解维度中等、需要**快速实现**。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **离散 / 组合问题**（TSP、调度）⇒ 标准 PSO 的速度更新不适配排列 ⇒ 用 `references/optimization/ga.md` / `aco.md`（凭经验）。
  2. **要求精确最优** ⇒ PSO 给近似解（凭经验）。
  3. **目标可微且凸** ⇒ 用 `fmincon` 更快（凭经验）。
  4. **只跑一次就报结果** ⇒ 结果不可复现（本类纪律核心，见 ④-1）。
  5. **早熟 / 参数失配** ⇒ 惯性权重 `w` 太大不收敛、太小早熟（凭经验）。

## ② 标准建模步骤

1. **初始化**：`N` 个粒子位置 + 速度（本骨架 `pop=40`，域 `[-10,10]^2`）。
2. **评估**适应度 `f(x_i)`，更新 `pbest`、`gbest`。
3. **更新速度**：`v ← w·v + c1·r1·(pbest − x) + c2·r2·(gbest − x)`。
4. **更新位置**：`x ← clamp(x + v, 域)`。
5. **重复**至代数上限。
6. ★ **固定种子 + 多次运行**：报**逐次最优 + mean±sd + 命中率 / 相对差**。
7. **调参**：`w, c1, c2`（本骨架 `0.7 / 1.5 / 1.5`）。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 目标函数 · `pop` · `maxgen` · 惯性 `w` · 学习因子 `c1, c2` · 域 · 种子 |
| **输出** | 逐次最优 `f_best` / `x_best` · `mean ± sd` · 命中率 · 相对差 |

**显式假设（必须写进论文）**：
1. **搜索空间连续**且**有界**（否则位置会飞出，需边界处理）。
2. **适应度可比较**。
3. ★ **结果是随机变量**：报固定种子可复现值 + 多种子分布；**单次读数不能当性能**。
4. **`w, c1, c2, pop, maxgen` 是显式超参**。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★★ **只跑一次就宣称达标**：**实测**（本骨架 `pso.m`，单峰 `f(x)=3+(x1-2)²+(x2+1)²`、`f*=3`、`pop=40`、`maxgen=150`、`w=0.7, c1=c2=1.5`）：5 个种子的 `f_best` 全 = `3`，**mean ± sd = `3 ± 0`**，**命中率 `5/5`**，相对差全 `0`。
2. ★ **可复现性**：**实测**（两次独立 `matlab -batch`）：本骨架整段输出**逐字节一致**（`diff` 为空）。
3. ★ **拿工具箱 / 内置当"独立参照"**：同机同实现**不独立**（任务书 B）；参照走**已知最优算例 + 独立参照件**。
4. **速度不设上限** ⇒ 粒子飞散（凭经验——本骨架用域裁剪控制）。
5. **`w` 不当**：过大震荡不收敛、过小早熟（凭经验）。
6. **`gbest` 过早垄断** ⇒ 全群塌缩到一点、丢失多样性（凭经验）。

## ⑤ 输出模板

- **分布表**（各 `seed` 的 `f_best` + `mean ± sd` + 命中率）+ **收敛曲线** + 最优解。
- 收敛曲线 / 粒子轨迹图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；分布表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/optimization/pso.m`（**零参可跑**，5 种子分布 + 可复现）。

关键片段（**不整份复制**）：
```matlab
for s = 1:numel(seeds)
    rng(seeds(s));                                   % ★ 固定种子
    X = lo + (hi - lo) .* rand(pop, D); V = zeros(pop, D);
    pbest = X; pbestf = fit(X); [gbestf, im] = min(pbestf); gbest = pbest(im,:);
    for it = 1:maxgen
        V = w*V + c1*rand(pop,D).*(pbest - X) + c2*rand(pop,D).*(gbest - X);
        X = min(max(X + V, lo), hi);
        fx = fit(X); imp = fx < pbestf;
        pbest(imp,:) = X(imp,:); pbestf(imp) = fx(imp);
        [gbestf, im] = min(pbestf); gbest = pbest(im,:);
    end
    fbest(s) = gbestf; xbest(s,:) = gbest;           % 多次运行给分布
end
```
**独立参照**：`tests/skills/model-select/verify/pso.md`（**第 4 类：已知最优算例 + 固定种子 + 多次运行的分布**）。

## 语料面（P6）

- **语料指针（带）**：`corpus/papers/MODEL_MAP.md` 里 `particle swarm optimization` 命中 **3 行** ⇒ **去重并集 4 篇**
  （`P2025-A-01` · `P2025-A-04` · `P2025-B-01` · `P2025-C-12`；当场 `grep -nE "^ +- particle swarm optimization（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`）。
- **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch10 / ch13–ch17 PSO 系列）—— 教辅级**起点素材**，**不作独立参照**。
- ★ **口径提醒（P7）**：上式"4 篇"的常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
