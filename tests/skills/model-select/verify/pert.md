# 参照记录 · `pert`（计划评审 PERT / CPM）

**骨架**：`.claude/skills/mcm-model-select/assets/matlab/network/pert.m`
**语料面（P6）**：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `PERT` 与 `critical path` 带锚 **均 0 行**（2026-10-04 当场复跑 `grep -cE "^ +- (PERT|critical path)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0）⇒ 标 `[社区]`（教科书级常识）。
★ **正对照**：同形态 `centrality` 带锚 ⇒ `3 行`。
★ **算法素材面**：`corpus/algorithms/src/GraphTheory(图论)/basic/grPERT.m`（grTheory）—— 教辅级**起点素材**，**不作独立参照**。

## ① 参照类型
**第 3 类：手算小图**（GC6）—— 6 活动网络，**手算前推 / 后推 / 松弛**，与骨架的 `duration`、`slack`**逐位比**。

## ② 参照来源（算式 + 手算）
- **活动**：A..F，历时 `[3 2 4 2 3 5]`；前驱：A:— · B:A · C:A · D:B,C · E:D · F:C。
- **前推手算**（`ES = max(前驱 EF)`, `EF = ES + dur`）：
  - A: `ES=0, EF=3`
  - B: `ES=3, EF=5`
  - C: `ES=3, EF=7`
  - D: `ES=max(5,7)=7, EF=9`
  - E: `ES=9, EF=12`
  - F: `ES=7, EF=12`
  ⇒ 项目工期 `T = max(EF) = 12`。
- **后推手算**（`LF = min(后继 LS)`, `LS = LF − dur`）：
  - F: `LF=12, LS=7` · E: `LF=12, LS=9`
  - D: `LF=LS(E)=9, LS=7` · C: `LF=min(LS(D),LS(F))=min(7,7)=7, LS=3`
  - B: `LF=LS(D)=7, LS=5` · A: `LF=min(LS(B),LS(C))=min(5,3)=3, LS=0`
- **松弛手算** `slack = LS − ES = [0 2 0 0 0 0]`；关键活动 = `{A, C, D, E, F}`（**两条关键路径** `A-C-D-E` 与 `A-C-F`，均 12）。
- **参照与骨架不同源**：手算走**表格式前后推**；骨架是同一 CPM 的实现。
  ★ **诚实说明**：手算与骨架同一算法 ⇒ **符号核对 + 逐位数值核对**；独立性来自"手算是人按前后推定义逐活动算、与代码无关"。

## ③ 运行命令
```
matlab -batch "addpath('D:/Projects/数学建模/.claude/skills/mcm-model-select/assets/matlab/network'); pert"
```

## ④ 两边读数
| 量 | 骨架 | 参照（手算） | 是否一致 |
| :--- | :--- | :--- | :--- |
| 项目工期 | `12` | `12` | **相同** |
| `ES` | `[0 3 3 7 9 7]` | `[0 3 3 7 9 7]` | **逐位相同** |
| `slack` | `[0 2 0 0 0 0]` | `[0 2 0 0 0 0]` | **逐位相同** |
| 关键活动 | `A C D E F` | `{A,C,D,E,F}` | 一致 |

（骨架内置 `hand-computed ... => MATCH` 自检行；本方法**确定性**，故无需多运行分布。）

**结论**：工期 `12`、`ES = [0 3 3 7 9 7]`、`slack = [0 2 0 0 0 0]`、关键活动 `A C D E F`，与**手算前后推逐位相同**。
★ **本记录验证**"工期与关键路径算得对"；**不验证**"依赖网络建得对"（建模判断）。
