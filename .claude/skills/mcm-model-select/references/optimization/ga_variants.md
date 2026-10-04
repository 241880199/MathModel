# 遗传算法变体（`ga_variants.m`）

> **基础 GA 不够用时用**：把种群**分成若干"岛"（多种群 / 并行 GA）**，各岛独立进化、**定期迁移**交换最优个体 ⇒ 在保持多样性的同时共享好解。同类变体还包括**量子 GA**（量子比特编码）与**混合 GA**（GA + 局部搜索）。代价同族：**结果随随机数变**，固定种子 + 多运行。

**归属**：类索引 `references/optimization.md` · 骨架 `assets/matlab/optimization/ga_variants.m` · 参照 `tests/skills/model-select/verify/ga_variants.md`。
★ **与 `ga` 的边界**：基础实数/二进制 GA ⇒ `references/optimization/ga.md`；本文件专收**多种群 / 量子 / 混合**等增强结构（本骨架实现**多种群（island）**）。

## ① 适用判据

- **用**：基础 GA **早熟 / 多样性丢失**时；问题**多峰**、需要"分头探索 + 共享好解"；想借**并行 / 多种群**结构提升鲁棒性；或题目明确要求**多目标（NSGA-II 一族）**、量子编码、混合局部搜索。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **基础 GA 已够** ⇒ 上变体只增复杂度与调参面（凭经验）。
  2. **目标可微且凸** ⇒ 梯度法更快更准（凭经验）。
  3. **要求精确最优** ⇒ 仍是启发式、给近似解（凭经验）。
  4. **只跑一次就报结果** ⇒ 结果不可复现（本类纪律核心，见 ④-1）。
  5. **误把"变体"当"必更好"** ⇒ 多种群/量子不一定强于调好参的基础 GA（凭经验——不要迷信名字）。

## ② 标准建模步骤

1. **编码 + 适应度**（同 `ga`）。
2. **分岛**：种群切成 `nIsl` 个子种群（本骨架 `pop=40` → 4 岛 × 10）。
3. **各岛独立进化**：选择 / 交叉 / 变异 / 精英（同基础 GA）。
4. **定期迁移**：每隔 `migint` 代，把各岛最优的 `nMig` 个个体**环状**传给下一岛、替换其最差（本骨架 `migint=20`、`nMig=2`）。
5. **共享全局最优**（可选布告板）。
6. ★ **固定种子 + 多次运行**：报**逐次最优 + mean±sd + 命中率 / 相对差**。
7. **（多目标变体）**：NSGA-II 走非支配排序 + 拥挤距离，输出**Pareto 前沿**（而非单点）。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 目标函数 · `pop` · `nIsl` · `maxgen` · `migint` / `nMig` · `pc` / `pm` · 种子 |
| **输出** | 逐次最优 `f_best` / `x_best` · `mean ± sd` · 命中率 · 相对差 |

**显式假设（必须写进论文）**：
1. **岛内交叉/变异算子保持可行性**（同 `ga`）。
2. **迁移拓扑与频率**会影响收敛（本骨架用环状 + 固定间隔）—— 是**显式设计选择**。
3. ★ **结果是随机变量**：报固定种子可复现值 + 多种子分布；**单次读数不能当性能**。
4. **（多目标）Pareto 前沿的**"最优"是**集合**，不是单点 —— 评价口径不同（超体积 / 覆盖度）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★★ **只跑一次就宣称达标**：**实测**（本骨架 `ga_variants.m`，多种群 GA、单峰 `f(x)=3+(x1-2)²+(x2+1)²`、`f*=3`、`pop=40·4 岛`、`maxgen=150`）：5 个种子的 `f_best` = `3 / 3 / 3 / 3 / 3.0000022`，**mean ± sd = `3.0000005 ± 9.9019957e-07`**，**命中率 `5/5`**。
2. ★ **可复现性**：**实测**（两次独立 `matlab -batch`）：本骨架整段输出**逐字节一致**（`diff` 为空）。
3. ★ **迁移一个坑（实测）**：迁移代码里把 4 个岛的**列向量** `fv` 用 `cell2mat` 合并会拼成**矩阵**（不是 40×1 向量），让 `min` 返回**两个向量**、赋值报错 —— 改用 `vertcat(fv{:})` 才拿到正确的 40×1。★ 这是"合并 cell 数组"的通用陷阱。
4. **迁移太频繁 / 太多** ⇒ 各岛趋同、退化成单种群（凭经验）。
5. **误把多目标当单目标** ⇒ 若真是多目标，须给**前沿**而非单点（凭经验）。
6. **拿工具箱 / 内置当"独立参照"**：同机同实现**不独立**（任务书 B）；参照走**已知最优算例 + 独立参照件**。

## ⑤ 输出模板

- **分布表**（各 `seed` 的 `f_best` + `mean ± sd` + 命中率）+ **收敛曲线** + 最优解；（多目标）**Pareto 前沿图**。
- 收敛曲线 / Pareto 前沿图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）；分布表 → `mcm-table`（`.claude/skills/mcm-table/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/optimization/ga_variants.m`（**零参可跑**，多种群 GA，5 种子分布 + 可复现）。

关键片段（**不整份复制**）：
```matlab
for s = 1:numel(seeds)
    rng(seeds(s));                                   % ★ 固定种子
    P = cell(1,nIsl); fv = cell(1,nIsl);
    for isl = 1:nIsl; P{isl} = lo + (hi-lo)*rand(subpop,D); fv{isl} = fit(P{isl}); end
    for gen = 1:maxgen
        for isl = 1:nIsl
            [P{isl}, fv{isl}] = evolve_island(P{isl}, fv{isl}, fit, pc, pm, gen, maxgen, ...);
        end
        if mod(gen, migint) == 0; [P, fv] = migrate(P, fv, nIsl, nMig); end   % 环状迁移
    end
    gall = vertcat(fv{:}); [fbest(s), im] = min(gall);   % ★ vertcat（不是 cell2mat）
end
```
**独立参照**：`tests/skills/model-select/verify/ga_variants.md`（**第 4 类：已知最优算例 + 固定种子 + 多次运行的分布**）。

## 语料面（P6）

- **语料指针（带）**：`corpus/papers/MODEL_MAP.md` 里与本变体**同族**的命中（当场
  `grep -nE "^ +- (NSGA-II|multi-objective optimization|differential evolution|A\* and GA)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`）：
  `NSGA-II`（1 行 · 2 篇）· `multi-objective optimization`（2 行 · **去重并集 5 篇**）·
  `differential evolution`（1 行 · 1 篇）· `A* and GA`（1 行 · 1 篇）。
  ★ **同族不等于同一方法**——上面是"GA 变体族"的**共同证据**，不是"多种群 GA 本身"的逐字命中。
- **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch7 多种群 · ch8 量子 · ch9 多目标 · ch11 多层编码）—— 教辅级**起点素材**，**不作独立参照**。
- ★ **口径提醒（P7）**：上式常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
