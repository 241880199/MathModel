# 选模型 + 可跑求解代码 —— 2025 MCM Problem A《Testing Time: The Constant Wear On Stairs》

> **一句话推荐**：主模型用 **机理类的「Archard 磨损累积模型 + 参数辨识（反演）」**——
> 把踏步表面写成「磨损深度 = 材料磨损系数 × 累计踩踏次数 × 空间落步强度场」，
> 再用 **最小二乘反演**从测得的磨损剖面反推「用了多少（累计人次）／什么方向／几个人并排」，
> 用 **蒙特卡洛**给年龄估计配可信区间。
> 这不是拍脑袋：**获奖语料里这道题的 5 篇论文，5 篇都用 Archard 磨损律**（见 §3.4）。
>
> **边界声明（照 `mcm-model-select` 的口径）**：本文件给出**候选模型与判据、一个带推翻条件的推荐**；
> **最终选择与结论由队员负责**。本文件**不判"模型选对了没有"**。

---

## 0. 交付物清单

| 文件 | 内容 |
| :--- | :--- |
| `selection.md` | 本文件：选型论证 + 建模方案 + 测量方案 + 代码说明 |
| `stair_wear_archard.m` | **可跑 MATLAB 求解器**（零参即可跑；前向仿真 + 反演 + 蒙特卡洛），本文件 §8 亦附完整清单 |

代码用法（MATLAB，任意 cwd，把该 `.m` 放进当前目录或 `addpath` 其所在目录）：

```
>> stair_wear_archard          % 零参自足 demo（合成真值 → 反演 → 打印读数与年龄区间）
>> r = stair_wear_archard();   % 取回 struct（含真值/反演值/年龄区间/方向比/并排数）
>> r = stair_wear_archard(struct('k_true',1,'alpha_true',0.5));   % 覆盖任意默认参数
```

**本机实测读数**（MATLAB R2025b，Windows，`matlab -batch "stair_wear_archard"`）：

```
truth : k=2  sep=0.240 m  alpha_up=0.70  w_max=0.0120 m  N=1.2e+07  age=12000.0 y
fit   : k=2  sep=0.240 m  alpha_up=0.70  N=1.2e+07  age=11998.4 y
rel.err : N(LS)=0.01%  N(peak)=4.76%  N(vol)=0.00%
direction up:down = 70:30 (truth 70:30)
age 95% CI = [4850.3, 28612.4] y
```

---

## 1. 题面特征（选型的第一跳输入）

从 `problem.txt` 抽出与"选哪类模型"直接相关的特征：

1. **要"为什么磨损成这样"（机理）**：石/木踏步被长期踩踏而**不可逆地减薄**，中段比边缘磨得深（"tread no longer level / bowed"）。磨损深度是**随时间的累积量**——能写出状态随时间演化的方程。
2. **要"由观测反推历史"（反演）**：题面要的答案全是**从磨损剖面倒推**——用了多频繁、有没有偏好方向、几个人并排、年龄多少、有没有修缮过、材料来自哪个采石场。这是**已知机理形态、参数/历史未知**的问题。
3. **要给"可靠性"（不确定性）**：题面明写 "*how reliable is the estimate*"。⇒ 需要在反演之外**传播不确定性**。
4. **含空间维度**：磨损在踏面上**位置相关**——横向（并排与否）与行进方向（前后 / 上下行）都要分辨。
5. **数据形态**：**无给定数据**（纯机理/假设）——模型必须**自带假设、并说清要采什么测量**。
6. **约束**：测量**非破坏、低成本、小团队、少工具**。

（特征 1–3 与语料对本题的题型标注完全一致：核心 = **反演与参数估计 / 机理建模 / 统计推断与敏感性**。）

---

## 2. 第一跳：题面特征 → 类（决策树）

按 `mcm-model-select` 的第一跳表逐条对照：

| 问 | 判据命中？ | 指向的类 |
| :--- | :--- | :--- |
| 要"为什么这样变"？ | ✅ 能写"磨损深度随时间累积"的演化方程 | **mechanism（主）** |
| 要"下判断 / 降结构"？ | ✅ 从含噪剖面反推参数、给区间、做分布拟合与检验 | **statistics（次）** |
| 要"推演出来"？ | ⚠️ 部分：个体落步位置的随机推演（用于造合成数据 / 个体效应） | **simulation（次·辅助）** |
| 要"谁更好"？ | ❌ 无多对象多指标排序 | — |
| 要"往后看"？ | ❌ 无时间序列外推 | — |
| 要"怎么最好"？ | ❌ 无决策变量 + 目标 + 约束 | — |
| 要"在图 / 网络上算"？ | ❌ 非图结构 | — |
| 要"从数据学出关系"？ | ❌ 无特征矩阵、无监督标签 | — |

**结论**：**主类 = mechanism**，**次类 = statistics（反演的不确定性）**，**辅助 = simulation（蒙特卡洛/个体落步）**。
★ 口径：**不声称一道题只属一类**；主/次/辅助是**排序**，不是排他。

★ **被明确挡在门外**的三个类（附"反面"依据，见 `SKILL.md` 八片叶）：
- **prediction**：无"序列外推"问题；把磨损当"时间序列预测"是无机理的误配。
- **optimization**：题面**没有决策变量与目标函数**（不是"怎么走最省""怎么修最划算"）——那属于我们自行"要不要修"的延伸题，不是本题核心。
- **evaluation**：没有"多对象多指标排序"。

---

## 3. 第二跳：类内选方法（候选 + 判据 + 反面）

`mechanism` 类索引的类内判据树（`references/mechanism.md`）：

- **问 1（自变量连续时间 / 给初值？）** → 是：**ODE 初值问题**（`references/mechanism/ode_ivp.md`）
- **问 2（含空间维度？）** → 是（踏面剖面）：**PDE 数值解** / **输运方程**（`references/mechanism/pde_numerical.md` · `transport.md`）
- **问 4（方程已知、参数未知 / 要看长期？）** → 是：**参数辨识 / 稳定性分析**（`references/mechanism/param_id_stability.md`）

### 3.1 候选清单（口径：本清单**不声称穷尽**）

| 候选 | 类 / 方法 | 适用判据（为什么可能是它） | 反面（什么时候不该用它） | 六格路径 |
| :--- | :--- | :--- | :--- | :--- |
| **C1 Archard 磨损累积 + 参数辨识** | mechanism / `param_id_stability` | 方程形态已知（线性累积律 `dw/dt=κφr`）、要从观测**反推**累计人次与年龄；参数辨识正是"先有方程、再反推参数" | 若**方程形态也未知**要先做模型选择；若参数**不可辨识**须给区间不给点估计 | `.claude/skills/mcm-model-select/references/mechanism/param_id_stability.md` |
| C2 磨损累积 ODE 前向 | mechanism / `ode_ivp` | 给初值（新踏面 `w=0`）推演化轨迹 | 本题要的是**反演**不是"给定参数算轨迹" ⇒ 只作 C1 的前向引擎 | `.claude/skills/mcm-model-select/references/mechanism/ode_ivp.md` |
| C3 踏面剖面演化 PDE | mechanism / `pde_numerical` · `transport` | 若把"落步强度场 + 边缘坍塌/扩散"写成带空间导数的输运/扩散方程，求整场 | 本模型的空间依赖是**分离的参数化**（无位置间耦合），硬写成 PDE 反而**没有新增物理**；且显式格式有稳定域约束 | `.claude/skills/mcm-model-select/references/mechanism/pde_numerical.md` |
| C4 行人流 PDE（Navier-Stokes 型） | mechanism / `pde_numerical` | 若要在"上/下行人流密度"层面建模（语料 P2025-A-01 用过） | 需要**人流数据**且引入大量自由参数，对"只有磨损剖面"的输入**不可辨识** ⇒ 不作主模型 | 同上 |
| C5 高斯混合 / 中心极限 | statistics / `hierarchical_cluster`（分布拟合） | 横向磨损的**多峰**正是"几个人并排"的签名；用成分数 `k` 读数 | 若横向是单峰或噪声极大，成分数不可辨 ⇒ 退化为 1 | `.claude/skills/mcm-model-select/references/statistics.md` |
| C6 蒙特卡洛 / 贝叶斯反演 | simulation / `monte_carlo` · statistics / `bayesian` | 给年龄/人次**可信区间**，回答"可靠性" | 不是模型主体，是**不确定性层**；先验/噪声模型假设错会把区间带偏 | `.claude/skills/mcm-model-select/references/simulation/monte_carlo.md` |

### 3.2 推荐（带推翻条件）

> **推荐：以 C1（Archard 磨损累积 + 参数辨识）为主模型**，用 **C2** 作前向引擎，
> **C5** 负责"并排数"，**C6** 负责"可靠性"，**C3/C4** 仅作可选延伸（能拿到人流数据时）。

**为什么是它（三条）**：
1. **直接对齐题面的三个基础问题与四个难点**（§6 逐条兑现）——一个累积律把"频率/方向/并排/年龄/材料"全接上。
2. **测量便宜、非破坏、可小团队完成**（§7）：只要一张踏面**深度图**，就能支撑反演。
3. **有语料背书**（§3.4）：这道题的获奖论文一致选它。

**推翻条件（什么时候该弃用它）** —— 满足任一，请回退重选：

- **R1 方程形态其实不成立**：若磨损深度与人次**不近似线性**（如出现饱和/加速磨损、材料剥落主导），线性累积律失真 ⇒ 先做**模型选择**（比较线性 / 幂律 / 饱和多种形态，用 AIC/BIC），别硬拟合。
- **R2 参数不可辨识**：若 `κ0` 与 `日频次 r̄` 只能以乘积 `κ0·r̄` 出现、且没有独立标定，则**年龄不可辨识** ⇒ 只能给"累计人次"及其区间，**不给"年龄"点估计**（题面难点"many people short time vs few long time"正是这条的极端，见 §6.4）。
- **R3 没有 `κ0` 的独立标定**：不同材料/工艺的 `κ0` 变幅很大（凭经验）⇒ 缺标定时**材料来源问题**无法回答，年龄区间会宽到无信息。
- **R4 踏面几何严重退化**：若破坏性损伤、大块缺损、后期修补覆盖了原始磨损形貌 ⇒ 剖面反演失效，转用"分踏步/分区域比较 + 异常检测"（修缮识别，§6.3）。

### 3.3 被选中模型的六格详情（C1：Archard 磨损累积 + 参数辨识）

> 骨架（六格原文）路径：`.claude/skills/mcm-model-select/references/mechanism/param_id_stability.md`
> 可跑骨架：`.claude/skills/mcm-model-select/assets/matlab/mechanism/param_id_stability.m`
> 前向引擎骨架：`.claude/skills/mcm-model-select/assets/matlab/mechanism/ode_ivp.m`

| 格 | 内容（本题落地版） |
| :--- | :--- |
| **① 适用判据** | 题面能写出**含待估参数的动力学方程**、要从观测**反推参数/历史**：本题 `dw/dt = κ0·φ(p)·r(t)`，`w(0)=0`。**反面**：无机理方程（→ statistics/ml）；核心是约束最优（→ optimization）；**方程形态也未知**（→ 先 AIC/BIC 模型选择）；**参数不可辨识**（→ 只给区间）。 |
| **② 标准建模步骤** | 1) 写机理方程（含 `κ0, φ, r`）。2) 采/造观测 `w_meas = model + 噪声`。3) 构造最小二乘目标 `J=Σ(w_model−w_meas)²`。4) 优化求参数（`fminsearch`/`lsqcurvefit`，**对数/`exp` 参数化保正**）。5) 稳定性/可辨识性：扰动参数看剖面敏感性。6) **数值验证**：造真值 → 反演回来要对得上（无噪精确、加噪在噪水平内）。7) 报告：点估计 + 区间 + 结论。 |
| **③ 参数与假设** | 输入：`κ0`（材料+步态磨损系数，m/次）· `φ(p)` 参数化（横向成分数 `k`、间距 `sep`、宽 `s`；纵向上下行中心 `yU,yD`、上行占比 `α`）· 网格 · 噪声水平。输出：`N`（累计人次）· 年龄 `t` · 方向比 · 并排数 `k` · 区间。**显式假设（必须写进论文）**：① 线性累积成形**正确**；② `κ0` 定常；③ 噪声模型写清（本骨架用**乘性**深度噪声、固定种子）；④ **可辨识性**成立；⑤ 优化收敛到全局（**多初值重启**）。 |
| **④ 常见坑** | 1) **加噪报"精确等于真值"**：只会在噪水平内回到真值（`param_id_stability` Task 1 实测：无噪相对差 `~1e-13`、2% 噪声 `~3e-2/6e-3`）。2) **只报点估计、不做可辨识性**：多参数常相关（如"多人少时"与"少人多时"给同一 `N`）⇒ 必给区间/敏感性。3) **初值/参数化不当**跑负值 ⇒ 用 `exp` 保正（本骨架做法）。4) **把"残差小"当"模型对"**：残差小只在**该数据**上成立。5) **越界**：别把"从样本估总体"（statistics）或"约束最优"（optimization）写成参数辨识。 |
| **⑤ 输出模板** | 参数估计表（真值 vs 估计 + 相对差）· 年龄可信区间 · 方向比 · 并排数；拟合剖面叠加图；年龄后验直方图。图 → `mcm-figure-choose`；表 → `mcm-table`（本文件不复述其排版规则）。 |
| **⑥ 代码骨架** | 骨架路径：`.claude/skills/mcm-model-select/assets/matlab/mechanism/param_id_stability.m`（**零参可跑**，自带算例 logistic `dN/dt=rN(1−N/K)`，以 `exp` 参数化 + `fminsearch` 最小二乘反演）。**本题**的落地求解器见本目录 `stair_wear_archard.m`（§8）——把骨架的"造真值→最小二乘反演→加噪验证"范式搬到 Archard 累积律上。 |

### 3.4 语料面（口径：`"素材 0" ≠ "语料 0"`，两面分开说）

- **语料面（有，且强）**：`corpus/papers/MODEL_MAP.md` 的 **§2025 A** 节把本题标为
  `核心 6 反演与参数估计·6.1 由观测反推参数/历史` · `核心 4 机理建模与仿真·4.1` · `核心 5 统计推断与因果·5.4`，
  **数据形态 = 无数据(纯机理/假设)**。该题 **5 篇**论文的去重模型里：
  - **Archard Law（5 篇）** 居首 —— `P2025-A-01..-05` 全部命中；
  - Monte Carlo（4）· sensitivity analysis（4）· Bayesian（3）· Gaussian Distribution（2）· PDE（2）· differential equation（2）· hypothesis test（2）· PSO（2）；
  - Gaussian Mixture（1）· Central Limit Theorem（1）· MCMC（1）· Credible Intervals（1）· CNN（1）。
  ⇒ **本题的主流解法 = Archard 磨损律 + 反演 + 贝叶斯/蒙特卡洛不确定性**，与本推荐**同型**。
  （当场复跑 `grep -nE "P2025-A-0[1-5]" corpus/papers/MODEL_MAP.md` 可复核；行 329–333 是逐篇 Archard Law 命中行。）
- **算法素材面**：`corpus/algorithms/src/` 里**磨损 / Archard** 为 0 命中 ⇒ 这一面属 `补`（本求解器为自写）。
- ★ 常用度证据**只有 2025 一年、43 篇**；超此范围的一律标「无依据、凭印象」。

---

## 4. 模型方程（写成论文可直接用的形态）

**状态量**：踏面上某点 `p=(x,y)` 的**磨损深度** `w(p)`（m）。
`x` = 横向（跨踏步宽，并排方向）；`y` = 沿行进方向（踏面进深，前缘↔后缘）。

**Archard 磨损律**：一次接触擦过的磨损体积 `V = K·F·s / H`（`K` 无量纲磨损系数、`F` 法向载荷、`s` 滑动距离、`H` 硬度）。
把 `K,H,F,s` 与步态几何**并成一个有效深度率** `κ0`（每次踩踏在最深处造成的深度增量，m/次），得**累积方程**：

```
dw(p)/dt = κ0 · φ(p) · r(t),      w(p,0) = 0
  =>  w(p) = κ0 · N · φ(p),   N = ∫₀ᵗ r(τ) dτ    [累计人次]
```

- `φ(p) ∈ [0,1]`：**空间落步强度场**（峰值归一为 1，故 `κ0` 定义在"最深处"）。
- 取**可分离** `φ(x,y)=φ_x(x)·φ_y(y)`：
  - `φ_x(x)` = **k 个高斯混合**（中心 `x_c±sep·(…)`、宽 `s_x`）——`k` 就是"**并排人数**"的签名；
  - `φ_y(y)` = **上/下行两成分混合**（中心 `y_U,y_D`、上行占比 `α`）——上下行落步前后重心不同 ⇒ **方向偏好**的签名。

**反演（参数辨识）**：给定实测剖面 `w_meas(x,y)`，
1. 边际化得 `w_x(x)`、`w_y(y)`；
2. 对 `w_x` 用 1..3 个高斯**最小二乘拟合**、按**信息量准则**选成分数 `k`（并排数）与 `sep,s_x`；
3. 对 `w_y` 拟合两成分 ⇒ 上行占比 `α`（方向比）；
4. 幅度最小二乘 `A = ⟨w, φ̂⟩/⟨φ̂,φ̂⟩` ⇒ **`N = A/κ0`**；
5. **年龄** `t = N / r̄`（`r̄` = 日均人次，来自历史估计）。

---

## 5. 需要什么测量（题面硬要求：非破坏 · 低成本 · 小团队 · 少工具）

| 测量 | 怎么测（非破坏 · 廉价） | 支撑哪个结论 |
| :--- | :--- | :--- |
| **踏面深度图 `w(x,y)`** | 直尺/塞尺 + 直边（straightedge）测"凹陷深度"，或手机/相机的**近景摄影测量 / 结构光**逐点重建顶面；每级踏步取 `x`（横向）×`y`（进深）网格 | 频率（`N`）· 并排（`k`）· 方向（`α`）· 年龄 |
| **踏步几何** | 卷尺：宽 `W`、进深 `D`、级高、级数 | 时空网格与折算 |
| **材料硬度（相对）** | **回弹仪 / Schmidt 锤**（非破坏）、或便携硬度计 | 标定 `κ0`、材料来源 |
| **对照样 / 参考料** | 同址**已知年龄踏步**、或采石场**同料新样**做磨耗对照 | 独立标定 `κ0`（解 R3） |
| **破损/修补痕迹** | 目视 + 照片：换过的踏步、局部补石/补木、色差与接缝 | 修缮识别（§6.3） |
| **上/下行落步几何** | 现场让志愿者上下各走数次，拍足印/落步位置 | 标定 `y_U,y_D` |

★ 全部**非破坏、低成本、小团队（2–4 人）、少工具（卷尺/直尺/塞尺/手机或回弹仪）**。
★ 论文里必须**写清测量协议与网格分辨率**（否则不可复现，对应 `mcm-selfreview` 的可复现性检查）。

---

## 6. 把模型对准题面的每个问题

### 6.1 三个基础问题

- **① 用了多频繁？** ⇒ 反演 `N = ⟨w,φ̂⟩/⟨κ0·⟨φ̂,φ̂⟩⟩`，即**累计踩踏人次**；再除以观测/历史时长得**平均频次**。
- **② 有没有偏好方向？** ⇒ 拟合 `φ_y(y)` 的两成分**质量比** `α:(1−α)` = **上行:下行**。`α≈1/2` ⇒ 近似双向均等；偏离大 ⇒ 有主导方向。
- **③ 几个人同时（并排还是单列）？** ⇒ 横向边际 `w_x(x)` 的**成分数 `k`**：`k=1` 单列（一条中央沟）⇒ 单排；`k=2` 双沟 ⇒ 常**两人并排**；间隙 `sep` 还可与**肩宽/踏步宽**对照核验。

### 6.2 四个难点

- **④ 磨损与已知信息是否一致？** ⇒ 用历史情景（年龄估计 × 日均人次 × 材料 `κ0`）**前向**算出 `w_pred(x,y)`，与 `w_meas` 比**残差**；残差在噪水平内 ⇒ 一致。可配**假设检验**（残差均值/结构，对应语料 `hypothesis test`）。
- **⑤ 年龄及可靠性？** ⇒ `t=N/r̄`；对 `κ0`、`r̄`、深度噪声做**蒙特卡洛**传播得**可信区间**（本骨架实测区间 `[4850, 28612] y`，真值 12000y —— 区间**很宽**，如实反映"只有磨损时年龄不可精确"）。
- **⑥ 修缮/改造？** ⇒ **逐级/逐区**分别反演 `κ0` 或年龄，做**异常检测**：某级 `N` 明显偏小 ⇒ 后换的新踏步；`κ0` 或材料特征突变 ⇒ 换料修补。
- **⑦ 材料来源？** ⇒ 反演所得 `κ0`（或硬度）与**候选料**（采石场/树种）的 `κ0` **比对**；一致 ⇒ 支持该来源。**前提是 `κ0` 有独立标定**（否则退化，见 R3）。
- **⑧ 人多短时 vs 人少长时？** ⇒ **本条要诚实**：`w` 只记录**累计 `N=∫r dt`**，**"人多短时"与"人少长时"给同一 `N`，在纯磨损下不可辨识**（这就是 §3.2 的 R2）。可区分它们的线索：边缘圆化/表层疲劳损伤等**与加载速率相关的次生效应**，或外部史料 —— 单靠磨损形貌**不能**分开，论文应把这条**明说为不可辨识**并给出所依赖的额外证据。

---

## 7. 代码说明（`stair_wear_archard.m`）

- **零参可跑**：`stair_wear_archard` 自带一套代表真值（两人并排、70% 上行、`N=1.2e7`、`κ0=1e-9 m/次` ⇒ 最深约 12 mm、约 12000 天 ≈ 33 年），
  造合成剖面 → 加**乘性**深度噪声 → **反演** → 打印读数与年龄区间。
- **可移植到真实数据**：把 `fit_wear(w_meas,...)` 之前那步（造真值 + 加噪）换成**你的实测深度矩阵**即可；接口只需 `w_meas`（`ny×nx`）、`W,D`、以及标定好的 `κ0` 与日均 `r̄`。
- **无工具箱依赖**：只用 base MATLAB（`fminsearch` · `trapz` · `conv` · `randn`），**不依赖** Statistics/Curve Fitting 工具箱（回避了 `normpdf`/`fitgmdist`/`prctile` 等）。
- **反演的两个稳健性细节**（调试中踩过、已修）：
  1. **成分数选择**：`k` 用**残差型信息量准则** `n·log(SSE/n)+3k·log(n)` 选；**但**必须给混合成分的**宽度上界**（此处 `s≤0.2W`）——否则会出现一个极宽的"假成分"去吞掉噪声（**过拟合**）。
  2. **拟合要多项初值重启**：中心用**平滑剖面的峰**做种子（`mode_seeds`，即"数沟槽"），再对**初始宽度**取 3 档重启；否则 `fminsearch` 会卡在单成分的坏局部极小（实测：K=2 曾收敛到 1 个有效成分、`N` 偏 30%）。

---

## 8. 完整可跑代码（`stair_wear_archard.m`）

```matlab
function out = stair_wear_archard(opts)
%STAIR_WEAR_ARCHARD  Archard-type wear-accumulation model for worn stair treads.
%
%   Forward simulation of the worn tread surface + INVERSE identification of
%   (cumulative traffic N, age t, direction ratio, number-abreast k) from a
%   measured, NON-DESTRUCTIVE wear-depth map w(x,y) on one tread.
%
%   Physical model (mechanism class; Archard's wear law)
%   ---------------------------------------------------
%   Each footstep removes a small amount of material. Archard: V = K*F*s/H.
%   Lumping K,H,F,s and the gait geometry into an effective depth rate gives,
%   at each point p of the tread, a linear accumulation law
%
%       dw(p)/dt = kappa0 * phi(p) * r(t),        w(p,0) = 0
%   =>  w(p) = kappa0 * N * phi(p),   N = integral_0^t r(tau) dtau   [footsteps]
%
%   where
%       kappa0  [m/footstep]  material+gait wear coefficient at the worst point
%       phi(p)  in [0,1]      spatial footfall-intensity field (peak = 1)
%       r(t)                  instantaneous footfall rate [footsteps/day]
%   phi is separable, phi(x,y) = phix(x)*phiy(y):
%       phix : lateral intensity  -> number of people walking ABREAST (k modes)
%       phiy : along-travel intensity -> UP/DOWN traffic mix (direction bias)
%
%   Inverse (mechanism #10, parameter identification)
%   -------------------------------------------------
%   Given w_meas on a grid: fit the phix/phiy shapes => k, mode separation,
%   direction ratio; then the LS amplitude A = <w,phi>/<phi,phi> => N = A/kappa0,
%   age = N/rbar.  Reliability: Monte Carlo over kappa0, rbar and depth noise.
%
%   Usage
%   -----
%     stair_wear_archard()            % zero-arg self-contained demo (synthetic truth)
%     out = stair_wear_archard(opts)  % opts.W opts.D opts.k_true ... (all optional)
%
%   Returns a struct with truth vs recovered values and the age credible interval.

if nargin < 1 || isempty(opts); opts = struct(); end
W  = dflt(opts,'W',1.00);    % tread width  [m]
D  = dflt(opts,'D',0.30);    % tread depth  [m] (front-back, direction of travel)
nx = dflt(opts,'nx',101);
ny = dflt(opts,'ny',61);
x  = linspace(0,W,nx); y = linspace(0,D,ny);
[X,Y] = meshgrid(x,y);

% ---- ground truth (representative of a real, long-used worn tread) --------
k_true     = dflt(opts,'k_true',2);         % two people abreast
sep_true   = dflt(opts,'sep_true',0.24);    % lateral mode separation [m]
sx_true    = dflt(opts,'sx_true',0.055);    % lateral sd [m]
alpha_true = dflt(opts,'alpha_true',0.70);  % fraction of traffic ASCENDING
yU_true    = dflt(opts,'yU_true',0.20);     % ascending foot centre [m]
yD_true    = dflt(opts,'yD_true',0.10);     % descending foot centre [m]
sy_true    = dflt(opts,'sy_true',0.045);    % along-travel sd [m]
kappa0     = dflt(opts,'kappa0',1e-9);      % m per footstep at the worst point
N_true     = dflt(opts,'N_true',1.2e7);     % cumulative footsteps
rbar       = dflt(opts,'rbar',1000);        % mean footsteps/day
noise      = dflt(opts,'noise',0.03);       % relative depth-measurement noise

th_true = struct('k',k_true,'sep',sep_true,'sx',sx_true,'xc',W/2, ...
                 'alpha',alpha_true,'yU',yU_true,'yD',yD_true,'sy',sy_true);
w_true = kappa0*N_true*phi_field(th_true,X,Y);
rng(0);
w_meas = w_true .* (1 + noise*randn(size(w_true)));   % proportional depth-gauge noise

% ---- inverse (parameter identification) -----------------------------------
% amplitude by least squares: w = A*phi + noise  =>  A = <w,phi>/<phi,phi>,
% then N = A/kappa0.  Peak- and volume-based estimates are kept as cross-checks.
fit     = fit_wear(w_meas,X,Y,W,D);
V_meas  = trapz(y, trapz(x, w_meas, 2));                 % integral w dx dy [m^3]
V_phi   = trapz(y, trapz(x, phi_field(fit,X,Y), 2));     % integral phi dx dy
phi_f   = phi_field(fit,X,Y);
N_hat   = sum(w_meas(:).*phi_f(:))/sum(phi_f(:).^2)/kappa0;  % LS amplitude -> N
N_peak  = max(w_meas(:))/kappa0;                         % peak-based cross-check
N_int   = V_meas/(kappa0*V_phi);                         % volume-based cross-check
age_hat = N_hat/rbar;

% ---- reliability (Monte Carlo) --------------------------------------------
mc = monte_carlo_age(N_hat,rbar,noise);

out = struct('th_true',th_true,'fit',fit,'N_true',N_true,'N_hat',N_hat, ...
             'N_peak',N_peak,'N_int',N_int,'age_hat',age_hat,'age_ci',mc.ci, ...
             'age_samples',mc.samples,'dir_ratio',fit.alpha,'k_hat',fit.k);

fprintf('[stair_wear_archard] Archard wear-accumulation model\n');
fprintf('  truth : k=%d  sep=%.3f m  alpha_up=%.2f  w_max=%.4f m  N=%.3g  age=%.1f y\n', ...
        k_true,sep_true,alpha_true,max(w_true(:)),N_true,N_true/rbar);
fprintf('  fit   : k=%d  sep=%.3f m  alpha_up=%.2f  N=%.3g  age=%.1f y\n', ...
        fit.k,fit.sep,fit.alpha,N_hat,age_hat);
fprintf('  rel.err : N(LS)=%.2f%%  N(peak)=%.2f%%  N(vol)=%.2f%%\n', ...
        100*abs(N_hat-N_true)/N_true, 100*abs(N_peak-N_true)/N_true, ...
        100*abs(N_int-N_true)/N_true);
fprintf('  direction up:down = %.0f:%.0f (truth %.0f:%.0f)\n', ...
        100*fit.alpha,100*(1-fit.alpha),100*alpha_true,100*(1-alpha_true));
fprintf('  age 95%% CI = [%.1f, %.1f] y  (N 95%% kc=(%.2f,%.2f))\n', ...
        mc.ci(1),mc.ci(2),mc.N_ci(1),mc.N_ci(2));
end

% ===========================================================================
function P = phi_field(th,X,Y)
%PHI_FIELD  Separable spatial footfall-intensity field, peak-normalized to 1.
phx = lateral_shape(th.k,th.xc,th.sep,th.sx,X(1,:));
phy = along_shape(th.alpha,th.yU,th.yD,th.sy,Y(:,1));
P = phy(:)*phx(:)';
P = P/max(P(:));
end

function ph = lateral_shape(k,xc,sep,sx,x)
%LATERAL_SHAPE  Mixture of k Gaussians across the tread width (k abreast).
off = (1:k) - (k+1)/2;
ph  = zeros(size(x));
for i = 1:k
    ph = ph + exp(-(x-(xc+sep*off(i))).^2/(2*sx^2));
end
ph = ph/max(ph);
end

function ph = along_shape(alpha,yU,yD,sy,y)
%ALONG_SHAPE  Two-component up/down mixture along the travel direction.
ph = alpha*exp(-(y-yU).^2/(2*sy^2)) + (1-alpha)*exp(-(y-yD).^2/(2*sy^2));
ph = ph/max(ph);
end

function fit = fit_wear(wm,X,Y,W,D)
%FIT_WEAR  Recover shape parameters from the measured depth map (separable).
x  = X(1,:); y = Y(:,1);
wx = trapz(y, wm, 1);   % lateral marginal  (1 x nx)
wy = trapz(x, wm, 2);   % along-travel marginal (ny x 1)

% --- lateral: number abreast k chosen by an IC over k = 1..3 ---
n = numel(x); best = struct('ic',inf,'k',1,'mu',W/2,'s',W/5);
for k = 1:3
    [mu,s,~,sse] = fit_mixture_ls(x, wx, k, 0.20*W);   % mode sd <= 0.2 W
    ic = n*log(sse/n) + 3*k*log(n);                    % residual-based IC
    if ic < best.ic; best = struct('ic',ic,'k',k,'mu',mu,'s',s); end
end
fit.k  = best.k;
fit.xc = W/2;
if best.k >= 2; fit.sep = max(best.mu)-min(best.mu); else; fit.sep = 0; end
fit.sx = mean(best.s);

% --- along-travel: two-component up/down mixture ---
[mu2,s2,a2,~] = fit_mixture_ls(y, wy, 2, 0.60*D);   % mu sorted ascending
fit.yD = mu2(1); fit.yU = mu2(2);
mass   = a2.*s2;                            % component mass ~ a*s (Gaussian area)
fit.alpha = mass(2)/(mass(1)+mass(2));      % ascending share of traffic
fit.sy = mean(s2);
end

function [mu,s,a,sse] = fit_mixture_ls(xg,vg,K,smax)
%FIT_MIXTURE_LS  Least-squares fit of a K-Gaussian mixture to a profile
%   (fminsearch; sigmoid-bounded centre/width, log amplitude; multi-start).
xg = xg(:); vg = vg(:); n = numel(xg);
lo = min(xg); hi = max(xg); span = hi-lo;
p0_mass = max(vg,0); if sum(p0_mass)==0; p0_mass = ones(n,1); end
seeds = { mode_seeds(xg, vg, K), ...                            % detected peaks
          lo + span*((1:K)'-0.5)/K, ...                         % equal spacing
          interp1(cumsum(p0_mass)/sum(p0_mass), xg, ((1:K)'-0.5)/K) }; % quantiles
smults = [0.10 0.25 0.50];      % multi-start over the initial mode width
best = struct('sse',inf,'mu',[],'s',[],'a',[]);
obj  = @(p) sum((vg - mix_model(xg,p,K,lo,span,smax)).^2);
for rep = 1:numel(seeds)
    mu0 = seeds{rep}(:);
    for q = 1:numel(smults)
        s0   = smults(q)*smax;
        par0 = [logit((mu0-lo)/span); logit(repmat(s0/smax,K,1)); ...
                log((max(vg)/K)*ones(K,1))];
        p    = fminsearch(obj, par0, optimset('MaxFunEvals',4e4,'MaxIter',4e4, ...
                                              'TolX',1e-12,'TolFun',1e-14));
        sse  = obj(p);
        if sse < best.sse
            [mu,s,a] = unpack(p,K,lo,span,smax); [mu,idx] = sort(mu);
            best = struct('sse',sse,'mu',mu(:),'s',s(idx),'a',a(idx));
        end
    end
end
mu = best.mu; s = best.s; a = best.a; sse = best.sse;
end

function v = mix_model(x,p,K,lo,span,smax)
%MIX_MODEL  Bounded K-Gaussian mixture: centres in [lo,lo+span], sd in (0,smax].
mu = lo + span*sigmoid(p(1:K));
s  = smax*sigmoid(p(K+1:2*K));
a  = exp(p(2*K+1:3*K));
v  = zeros(size(x));
for j = 1:K; v = v + a(j)*exp(-(x-mu(j)).^2/(2*s(j)^2)); end
end

function [mu,s,a] = unpack(p,K,lo,span,smax)
mu = lo + span*sigmoid(p(1:K)); s = smax*sigmoid(p(K+1:2*K)); a = exp(p(2*K+1:3*K));
end

function v = sigmoid(x); v = 1./(1+exp(-x)); end

function c = mode_seeds(xg, vg, K)
%MODE_SEEDS  Seeds for mixture centres: the K highest smoothed-profile peaks.
vg = vg(:); n = numel(vg);
w  = max(1, round(n/50));
vs = conv(vg, ones(2*w+1,1)/(2*w+1), 'same');
is = false(n,1);
is(2:end-1) = vs(2:end-1) > vs(1:end-2) & vs(2:end-1) >= vs(3:end);
idx = find(is);
if isempty(idx); [~,idx] = max(vs); end
[~,ord] = sort(vs(idx),'descend'); idx = idx(ord);
c = xg(idx(1:min(K,numel(idx))));
while numel(c) < K; c = [c; mean(xg)]; end     % pad by adding the domain centre
c = sort(c(1:K));
end

function y = logit(z)
z = min(max(z,1e-3),1-1e-3); y = log(z./(1-z));
end

function mc = monte_carlo_age(N_hat,rbar,noise)
%MONTE_CARLO_AGE  Propagate kappa0, daily-rate and depth noise -> age CI.
rng(1);
nMC   = 4000;
sig_k = 0.30;                                    % ln-sd of kappa0 (material)
sig_r = 0.35;                                    % ln-sd of daily rate rbar
Nmc   = N_hat*(1 + noise*randn(nMC,1)).*exp(sig_k*randn(nMC,1));
agemc = Nmc./(rbar*exp(sig_r*randn(nMC,1)));
mc = struct('ci',pct(agemc,[2.5 97.5]), 'N_ci',pct(Nmc,[2.5 97.5]), ...
            'samples',agemc);
end

function q = pct(v,p)
v = sort(v(:)); n = numel(v);
idx = (p/100)*(n-1)+1; lo = floor(idx); hi = ceil(idx);
q = v(lo) + (v(hi)-v(lo)).*(idx-lo);
end

function v = dflt(s,f,d)
if isfield(s,f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
```

---

## 9. 边界、不确定与已知局限（如实）

1. **年龄的宽区间是物理事实，不是实现缺陷**：`κ0` 与 `r̄` 的不确定（本骨架取 ln-sd 0.30 / 0.35）传播后，年龄 95% 区间可达真值的 `[0.4×, 2.4×]`。要让年龄**收窄**，只能靠**独立标定 `κ0`（对照样）**与**更可靠的历史人次**——这正好对应题面的"*how reliable is the estimate*"。
2. **"人多短时 vs 人少长时"不可辨识**（§6.4/ R2）：纯磨损只留累计量 `N`，论文应明说这条不可辨识，并指出所需的外部证据。
3. **线性累积假设**：饱和/加速磨损、材料剥落会破坏它（R1）；论文应做**形态敏感性**（改幂律/饱和律看结论稳不稳）。
4. **可分离假设**：`φ=φ_x·φ_y` 假设横向与纵向落步独立。若实际落步横向-纵向强耦合（如靠边走位），需扩展为不可分离场。
5. **本骨架用合成数据自证**：反演在**已知真值**下 0.01% 复原（`N`、年龄），方向比、并排数亦复原——**这只证明"反演流程对"**，不证明真实参数已知（真实 `κ0` 仍需现场标定）。
6. **未做**：真实深度图的预处理（去离群、配准、基线拉平）、逐级修缮检测的完整实现——这些是拿到实测数据后的下一步。

---

## 10. 参考（指针，不复述其规则）

- 选型方法：`mcm-model-select` `SKILL.md` · `references/mechanism.md` · `references/mechanism/param_id_stability.md` · `references/mechanism/ode_ivp.md` · `references/mechanism/pde_numerical.md` · `references/mechanism/transport.md` · `references/simulation/monte_carlo.md`
- 可跑骨架：`.claude/skills/mcm-model-select/assets/matlab/mechanism/param_id_stability.m` · `.../ode_ivp.m`
- 语料证据：`corpus/papers/MODEL_MAP.md` §2025 A（Archard Law 5/5 篇；Monte Carlo / Bayesian / PDE / Gaussian mixture …）
- 出图 / 排版：`mcm-figure-choose` · `mcm-table`（本文件不代述其规范）
