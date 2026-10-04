# 匹配与覆盖（`matching.m`）

> **要在图里选"两两配对 / 点边子集"满足约束时用**：最大匹配、最小点覆盖、最小边覆盖、最大独立集、团 —— 同属"点 / 边子集的优化选择"一族。

**归属**：类索引 `references/network.md` · 骨架 `assets/matlab/network/matching.m` · 参照 `tests/skills/model-select/verify/matching.md`。
★ **与相邻方法的边界**：要给**边着色 / 点着色** ⇒ `references/network/coloring.md`；要**指派到具体成本**（带费用）⇒ `references/optimization/ilp_assignment.md`；要求**最大流** ⇒ `references/network/maxflow_mincut.md`（二分匹配可归约为流）。

## ① 适用判据

- **用**：题面是**配对 / 覆盖 / 选择子集**问题（任务分配、人员-岗位配对、最小监控点覆盖、最大无冲突集合）；**二分结构**时匹配有强定理（Kőnig：最小点覆盖 = 最大匹配）。
- **反面（什么时候不该用 · 会误用的场合）**：
  1. ★ **`propensity score matching`（倾向得分匹配）不是图匹配** —— 那是**统计因果推断**方法，别混（`corpus/papers/MODEL_MAP.md` 里是独立 tag）。
  2. **配对上还带具体成本、要最小总成本** ⇒ 用**指派问题**（`references/optimization/ilp_assignment.md`），纯匹配只最大化"配对数"。
  3. **要着色** ⇒ 走 `references/network/coloring.md`。
  4. **一般图**（非二分）的最大匹配虽存在（Blossom 算法），但复杂度高；本骨架实现**二分**这一支（凭经验，实战图多为二分）。

## ② 标准建模步骤

1. **判定结构**：能否分成两侧（二分）？左侧 = 任务 / 人，右侧 = 岗位 / 资源。
2. **建图**：可行配对连边（无权 = 只要配得上）。
3. **求最大匹配**：**增广路**法（本骨架 Kuhn / 匈牙利 DFS 版）。
4. **取覆盖**：二分图由 **Kőnig 定理**，最小点覆盖 = 最大匹配（可由匹配直接给）。
5. **数值验证**（见 ⑥）：小二分图**手算**最大匹配。
6. **报告**：匹配对 + 匹配数 + 关联覆盖/独立集。

## ③ 参数与假设

| 项 | 说明 |
| :--- | :--- |
| **输入** | 邻接表 `adj`（左侧 u → 右侧邻居）· 右侧规模 `nR` |
| **输出** | `size`（最大匹配数）· `matchR`（右侧 → 左侧）· `pairs` |

**显式假设（必须写进论文）**：
1. **二分结构**：两侧内部无冲突边（若有 ⇒ 须先转化或转一般图算法）。
2. **无权 / 等权**：只最大化配对数；带成本须换指派模型。
3. **一对一并发**：每个顶点至多匹配一条边。
4. **静态可行性**：可行配对集合固定。

## ④ 常见坑（每条：实测依据 / 或标明"凭经验"）

1. ★ **把倾向得分匹配当图匹配**：同名不同义，`MODEL_MAP.md` 里是独立 tag（凭经验 + 语料实查）。
2. **非二分图直接套增广路**：一般图需 Blossom 收缩奇环，简单增广会错（凭经验）。
3. **只求"最大匹配数"却要"最小覆盖"**：二者在二分图**数值相等但集合不同**，别混给（凭经验）。
4. ★ **拿归档实现当"独立参照"**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMaxMatch.m`（grTheory）等是**未净室重写**的教辅级代码，不作独立参照。参照走**手算小图**（**实测**：最大匹配 = 3）。
5. **右侧编号错位**：左侧 / 右侧必须各自连续编号，否则增广路索引越界（凭经验）。

## ⑤ 输出模板

- **匹配对表**（左-右）+ **最大匹配数** + 可选**二分图**（标匹配边）。
- 表 → `mcm-table`（`.claude/skills/mcm-table/`）；二分图 → `mcm-figure-choose`（`.claude/skills/mcm-figure-choose/`）。
- ★ **本文件不复述这两个 skill 的排版规则**。

## ⑥ 代码骨架

**路径**：`assets/matlab/network/matching.m`（**零参可跑**，自带手算小二分图：左 {1,2,3} · 右 {4,5,6}；边 1-4,1-5,2-4,3-5,3-6）。

关键片段（**不整份复制**）：
```matlab
for u = 1:nL
    seen = false(1, nR);
    [matchR, ~] = kuhn(u, adj, matchR, seen);   % 增广路
end
sz = sum(matchR > 0);
```
**独立参照**：`tests/skills/model-select/verify/matching.md`（**第 3 类：手算小图** —— 手算最大匹配 = `3`，与骨架逐位相同）。
★ **起点素材**：`corpus/algorithms/src/GraphTheory(图论)/basic/grMaxMatch.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinVerCover.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinEdgeCover.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMaxStabSet.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMaxComSu.m` · `corpus/algorithms/src/GraphTheory(图论)/basic/grMinAbsVerSet.m`（**grTheory**，作者 Sergiy Iglin）· `corpus/algorithms/src/GraphTheory(图论)/detailed/匹配问题/`（**另一作者**的中文实现）—— 教辅级**起点素材**，**不作独立参照**。
★★ **两条线不许混写（P2）**：`basic/gr*.m`（`grTheory`，Sergiy Iglin）与 `detailed/` 下另一作者的实现**不是一套**，本文件只把二者**并列标源**，**不合成一个**。

## 语料面（P6）

- **无语料**：`corpus/papers/MODEL_MAP.md` 里 `matching` 带锚 **0 行**（当场 `grep -cE "^ +- matching（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
  ★ **正对照**：同形态 `centrality` 带锚 ⇒ 3 行，证明命令没写错。★ **陷阱**：`propensity score matching` 带锚 **1 行（2 篇）**（P2025-C-08/C-12）—— 那是**统计方法**、**不是本类图匹配**，**不并入**（★ **订正**：原写"带锚 2 行"，**把篇数当成了行数**；实测 ⇒ **1 行**、2 是篇数 —— 同 Task 11 复核 M3）。
- **算法素材面**：见上（`grMaxMatch.m` 等 6 件〔**grTheory**〕 + `detailed/匹配问题/`〔**另一作者**〕）。
- ★ **口径提醒（P7）**：常用度证据**只有 2025 一年、43 篇**；超范围的一律标「无依据、凭印象」。
- ★ **本行不声称穷尽**。
