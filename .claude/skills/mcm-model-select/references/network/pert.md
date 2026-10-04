# 计划评审 PERT（`pert.m`）

> **要做工期 / 关键路径分析时用**：给定工序及其历时与前后依赖，求项目总工期、各工序松弛时间、关键路径（计划评审技术）。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/pert.m` · 参照 `tests/skills/model-select/verify/pert.md`。
★ **与相邻方法的边界**：要**两点最短** ⇒ `references/network/shortest_path.md`；要**最优排程 / 资源分配** ⇒ `references/optimization/`（LP / 目标规划）。

## ① 适用判据

- **用**：题面有**工序依赖网络**，问**总工期 / 关键路径 / 松弛（浮动时间）**；可估工时（三点估计 `(o+4m+p)/6`）；要识别"哪些工序不能拖"。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. **要"最优资源分配 / 赶工代价最小"** ⇒ PERT 只做工期分析，不含优化目标 ⇒ 走 `references/optimization/`。
  2. **无依赖关系**（可并行且无先后） ⇒ 直接取最长历时即可，无须 CPM（凭经验）。
  3. **依赖关系有环** ⇒ 网络非法（工期无定义），须先消环（凭经验）。
  4. **要随机工期分布** ⇒ 经典 PERT 用三点估计近似；要精确分布须仿真（`references/simulation/monte_carlo.md`）。

## ② 标准建模步骤

1. **列工序**：活动、历时、**前驱**。
2. **建网络**：活动在点（AON）或活动在弧（AOA）。
3. **前推**：`ES = max(前驱 EF)`，`EF = ES + dur`；项目工期 = `max(EF)`。
4. **后推**：`LF = min(后继 LS)`，`LS = LF - dur`。
5. **算松弛**：`slack = LS - ES`；**关键工序 = slack 0**。
6. **数值验证**（见 ⑥）：小网络**手算**前后推。
7. **报告**：工期 + 松弛表 + 关键路径。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | `dur`（历时向量）· `pred`（前驱单元格） |
| **输出** | `ES, EF, LS, LF, slack` · `duration` · `critical` |

**显式假设（必须写进论文）**：
1. **无环依赖**：前驱关系构成 DAG。
2. **确定性历时**（经典 CPM）；随机性用三点估计 / 仿真。
3. **资源无限**：不因资源冲突而延误（若有资源约束须另建）。
4. **活动可拆分 / 不可拆分的约定**须写明（本骨架取整段不可分）。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. **依赖成环**：前推不收敛 / 结果无意义（凭经验）。
2. **关键路径不唯一**：并列 slack 0 的路径都可能关键，别只报一条（凭经验）。**实测**：本算例关键路径有 `A-C-D-E` 与 `A-C-F` 两条。
3. **把 slack 当"可随意拖"**：多条关键路径上，拖一条会把它变成关键（凭经验）。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/basic/grPERT.m`（grTheory）未净室重写，不作独立参照。参照走**手算小图**（**实测**：工期 `12`、slack `[0 2 0 0 0 0]`）。
5. **工期单位不一致**：天 / 小时混用（凭经验）。

## ⑤ 输出模板

- **工序表**（活动 · 历时 · ES · EF · LS · LF · slack）+ **总工期** + **关键路径**标注 + 可选**网络图**。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；网络图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/pert.m`（**零参可跑**，自带手算小网络：活动 A..F、历时 `[3 2 4 2 3 5]`、前驱 A:— · B:A · C:A · D:B,C · E:D · F:C）。

关键片段（**不整份复制**）：
```matlab
for i = 1:n
    if isempty(pred{i}); ES(i) = 0; else; ES(i) = max(EF(pred{i})); end
    EF(i) = ES(i) + dur(i);
end
T = max(EF);
for i = n:-1:1
    if isempty(succ{i}); LF(i) = T; else; LF(i) = min(LS(succ{i})); end
    LS(i) = LF(i) - dur(i);
end
slack = LS - ES;
```
**独立参照**：`tests/skills/model-select/verify/pert.md`（**第 3 类：手算小图** —— 手算工期 `12`、`slack = [0 2 0 0 0 0]`，与骨架逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grPERT.m`（**grTheory**）—— 教辅级**起点素材**，**不作独立参照**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `PERT` 与 `critical path` 带锚 **均 0 行**（当场 `grep -cE "^ +- (PERT|critical path)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。
- **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grPERT.m`。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
