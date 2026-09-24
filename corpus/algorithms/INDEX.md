# 算法归档索引

来源：`HuangCongQing/Algorithms_MathModels`　·　见 `PROVENANCE.md`
归档日期：2026-09-23　·　上游 commit `e15b0e9053b11f08b5ce1e3492c4acb444409c8b`（2022-12-26）

---

## 边界声明（先读这段）

- **这是素材，不是 skill。** 供做题时检索与思考，不直接产出交付物、不进论文。
- **代码未经运行验证。** §6 的"已知缺陷"全部来自**静态阅读**，且只覆盖我逐字读过的 4 个文件；其余 1,255 个文件**没有任何质量判断**。本机 MATLAB R2025b 可跑（见 `docs/mcm-suite-todo.md` §E.1），验证列在 §7。
- **不套证据分级。** `[官方]/[半官方]/[社区]` 那套只用于**赛制事实断言**（设计文档 §4）。算法知识属教科书常识，与 COMAP 无关，套分级反而误导。
- 上游是 2017–2022 的中文 MATLAB 代码，**学生/教辅级**，不是生产级库。**照抄进论文有风险**，这是它没被做成 skill 的原因。

## 分层

| 层 | 内容 | 文件数 | 用法 |
| :--- | :--- | ---: | :--- |
| **一级 · 直接可用** | 作者自有的算法实现 | 282 | 做题时的主要检索对象 |
| **二级 · 参考** | 智能算法 / 神经网络随书源码 | 510 | 完整工程范例（含 GUI、数据），按需翻 |
| **三级 · 仅存档** | 图像处理 / 高等数学随书源码 | 465 | 与美赛基本无关，仅作语料 |

代码在 `src/`，保留上游原始目录名以便回溯。

---

## 1. 评价类 evaluation

| 算法 | 用途 | 路径 | 备注 |
| :--- | :--- | :--- | :--- |
| **AHP 层次分析法** | 主观赋权 + 一致性检验 | `src/AHP层次分析法/` | `ahp.m` 单层；`sglsortexamine.m` 单排序一致性；`tolsortvec.m` 层次总排序 |
| 模糊综合评价（多层次） | 多级指标的模糊评判 | `src/FuzzyMathematicalModel模糊数学模型/多层次模糊综合评价/` | |
| 模糊综合评价（多目标） | 多目标同时评判 | `src/FuzzyMathematicalModel模糊数学模型/多目标模糊综合评价/` | |
| 模糊聚类 | 按模糊关系聚类 | `src/FuzzyMathematicalModel模糊数学模型/模糊聚类/` | 含 `fuzzy_matrix_compund.m` 模糊矩阵合成、`Riemann_closeness.m` 贴近度、最大最小法 |

## 2. 预测类 prediction

| 算法 | 用途 | 路径 | 备注 |
| :--- | :--- | :--- | :--- |
| **灰色预测 GM(1,1)** | 小样本、贫信息序列预测 | `src/GreySystem灰色系统/` | `GM_1_1.m` 最简；`GM_1_1_full_procession.m` 全流程（含检验） |
| 灰色 GM(2,1) / Verhulst | 二阶 / 饱和型序列 | 同上 | |
| 灰色关联度分析 | 因素影响力排序 | 同上 | `association_analysis.m` |
| 灰色优势分析 | 优势因素识别 | 同上 | `strength_analysis.m` |
| **时间序列 · 指数平滑** | 短期预测 | `src/TimeSeries时间序列函数/指数平滑法/` | 一次 / 二次 / 三次 |
| 时间序列 · 移动平均 | 平滑与趋势 | `src/TimeSeries时间序列函数/移动平均法/` | 简单 / 趋势 / 加权 |
| 时间序列 · 趋势外推 | 长期趋势拟合 | `src/TimeSeries时间序列函数/趋势外推预测法/` | Compertz / Logistic / 修正指数曲线 |
| 自适应滤波法 | 权重自调整预测 | `src/TimeSeries时间序列函数/自适应滤波法/` | |
| 回归分析 | 因果预测 | `src/RegressionAnalysis回归分析/` | 线性 / 一元多项式 / 多元二次多项式 / 逐步回归 / 非线性回归 |
| 神经网络预测 | 非线性序列 | `src/NeuralNetwork神经网络工具箱的调用案例/` + 二级层 | |

## 3. 优化类 optimization

| 算法 | 用途 | 路径 | 备注 |
| :--- | :--- | :--- | :--- |
| 线性规划 | LP 标准型求解 | `src/LinearProgramming（…）/` | `solve_lp.m`、`invest_model.m`（投资组合范例）|
| 整数规划 / 指派问题 | 离散决策 | `src/IntegerProgramming（…）/` | `assgin_integer_prog.m` 指派问题 |
| 非线性规划 | 目标或约束非线性 | `src/NonLinearProgramming非线性规划/` | |
| 目标规划 | 多目标折中 | `src/GoalProgramming(…)/` | |
| **遗传算法** | 全局搜索 / 组合优化 | `src/HeuristicAlgorithm（…）/遗传算法/` | 含 TSP(GA) 完整案例 |
| **模拟退火** | 全局搜索 | `src/HeuristicAlgorithm（…）/模拟退火算法/` | 含 TSP(SA) 完整案例 |
| 粒子群 PSO | 连续寻优 | 二级层 `MATLAB智能算法30个案例分析/chapter10,13,14,15,16` | 含多目标 PSO、混合 PSO 解 TSP、动态环境寻优 |
| 免疫优化 | 选址类离散问题 | 二级层 `…/chapter12` | |
| 蒙特卡洛 | 随机模拟求解 | `src/IntegerProgramming（…）/monte_carro.m` | |
| **GAOT 遗传算法工具箱** | 成熟第三方 GA 工具箱 | 二级层 `《MATLAB 神经网络30个案例分析》…/chapter27/gaot/` | 比一级层的自写 GA 更完整，优先用这个 |

## 4. 机理类 mechanism —— ⚠️ **本归档无**

**这是最大的空洞。** 上游 README 声称覆盖常微分方程与偏微分方程，但**归档里没有任何 ODE/PDE/差分方程的独立实现**（可能散在三级层的《高等数学问题求解》里，未逐查）。M4 的 `mechanism.md` 一类**不能指望本归档**，须另行准备。

## 5. 仿真类 simulation

| 算法 | 用途 | 路径 | 备注 |
| :--- | :--- | :--- | :--- |
| **元胞自动机（9 种规则）** | 空间演化 / 扩散 / 相变 | `src/CellularAutomata元胞向量机/` | 初等 CA、扩散限制聚集(DLA)、森林火灾、气体动力学、渗流集群、激发介质、生命游戏、砂堆规则、表面张力 |
| 蒙特卡洛 | 随机模拟 | 同优化类 | |

## 6. 统计类 statistics

| 算法 | 用途 | 路径 | 备注 |
| :--- | :--- | :--- | :--- |
| 主成分分析 PCA | 降维 / 指标合成 | `src/MultivariateAnalysis（…）/主成分分析/` | |
| 系统聚类 | 样本分类 | `src/MultivariateAnalysis（…）/聚类分析/` | `system_cluster.m` |
| 变量聚类 | 指标归类 | 同上 | `var_cluster.m` |
| 灰色关联 / 优势分析 | 因素排序 | 见 §2 | |

## 7. 网络与图论 network —— **本归档最厚的一块**

`src/GraphTheory(图论)/basic/` 是一套完整的 **grTheory 工具箱**（约 28 个函数 + `readme.txt`），`detailed/` 是分类详解。

| 主题 | 函数 | 路径 |
| :--- | :--- | :--- |
| 最短路 | `Dijkf.m` / `Floyd.m` / `grShortPath.m` | `basic/`、`detailed/最短路/` |
| 最小生成树 | `grMinSpanTree.m` | `basic/` |
| 最大流 / 最小割 | `grMaxFlows.m` / `grMinCutSet.m` | `basic/` |
| 最小费用流 | `BGf.m` | `detailed/最小费用流/` |
| 网络流（上下界 / 可行流） | `boundnetf.m` / `fofuf.m` / `restrf.m` | `detailed/网络流/` |
| 匹配 | `grMaxMatch.m` / `fc01-03.m` | `basic/`、`detailed/匹配问题/` |
| 染色（边 / 点 / 图） | `grColEdge.m` / `grColVer.m` / `colorcodf.m` 等 | `basic/`、`detailed/图的染色/` |
| 树 / 遍历 / Huffman | `BFS.m` / `DFS.m` / `Huffman.m` | `detailed/树/` |
| 欧拉图 / Hamilton 图 | `Fleuf1.m` / `flecvexf.m` / `glf.m` | `detailed/Euler图和Hamilton图/` |
| 连通性 / 中心性 | `grComp.m` / `ucengraf.m` / `centgraf.m` | `basic/`、`detailed/连通图/` |
| **计划评审 PERT** | `grPERT.m` | `basic/` |
| **旅行商 TSP** | `grTravSale.m` | `basic/` |
| 绘图 | `grPlot.m` | `basic/` |

## 8. 机器学习 ml

| 算法 | 路径 | 备注 |
| :--- | :--- | :--- |
| BP 分类 / LVQ 分类 | `src/NeuralNetwork神经网络工具箱的调用案例/` | 一级层，仅 2 个文件 |
| 神经网络 30 案例 | 二级层 `《MATLAB 神经网络30个案例分析》源程序 数据/` | BP、RBF、GRNN、SVM、Hopfield、SOM、Elman、PNN、小波、模糊神经… |
| 神经网络原理实例 | 二级层 `《MATLAB神经网络原理与实例精解》随书附带源程序/` | 单层感知器 → 随机神经网络，按章组织 |

---

## 9. 覆盖度对照（对 M4 的 8 大类）

| M4 计划的一类 | 本归档 | 判决 |
| :--- | :--- | :--- |
| evaluation 评价类 | AHP、模糊综合、模糊聚类 | ✅ 够 |
| prediction 预测类 | 灰色、时间序列、回归、神经网络 | ✅ 够 |
| optimization 优化类 | LP/ILP/NLP/目标规划、GA、SA、PSO | ✅ 最全 |
| mechanism 机理类 | — | ❌ **空** |
| simulation 仿真类 | 元胞自动机 9 种、蒙特卡洛 | ✅ 够 |
| statistics 统计类 | PCA、聚类、灰色关联 | ⚠️ 偏薄（无假设检验、无方差分析、无贝叶斯） |
| network 网络与图论 | grTheory 工具箱 + 8 个专题 | ✅✅ 最厚 |
| ml 机器学习 | BP/LVQ 一级；30 案例二级 | ✅ 够（但多为工具箱调用，非原理实现） |

## 10. 已知代码缺陷 —— **实跑验证结果**（2026-09-23，MATLAB R2025b）

**方法**：MATLAB `-batch` 逐脚本执行一级层 68 个脚本（`tests/algorithms/run_scripts.m`），
另对核心算法做**独立参照的数值验证**（`tests/algorithms/verify_numerics.m`）。
逐字证据在 `tests/algorithms/run-report.txt`、`numerics-report.txt`。

**结果**：60 个可无人值守脚本中 **44 通过 / 16 失败**；另 2 个交互式脚本实测通过，6 个因 GUI 死循环无法无人值守。

### 10.1 确证的**算法性**缺陷（4 个）—— 这些"能跑通"，但算的不是它声称的东西

**最重要的一类。** 它们不报错、不崩溃，照抄进论文会得到看似合理的错误结果。

| 文件 | 缺陷 | 怎么发现的 |
| :--- | :--- | :--- |
| `CellularAutomata元胞向量机/初等元胞自动机/basic_CA.m` | **从未真正迭代**。它让外圈随时间扩张，但每格一生只被计算一次（第 t 步只写半径 t−1 的那一圈），所以算出来的是"光锥填充"而非 CA 演化。其注释写的是"每一时间每一点"。实测（S=121、61 层、中心单点种子）：上游终态 **4369** 个 1，按规则迭代应为 **416** 个，**4241 格不同**，遍布全图 | 独立向量化重模拟逐格比对 |
| `GraphTheory(图论)/detailed/Euler图和Hamilton图/Fleuf1.m` | **给出非法欧拉回路**。5 点完全图 K5 上把边 {3,4}、{2,3} 各用两次、漏掉 {1,2}、{1,4}；简单 5 环上把 {1,5} 用两次、漏掉 {1,2}，且返回的边序列首尾不相接（游走本身断开） | 与图应有的边集直接比对 |
| `GraphTheory(图论)/detailed/最小费用流/BGf.m` | **在 6 点 10 弧的网络上传入即不终止**（>500 s，正常应毫秒级）。小实例上正确（3 点、含反向平行弧的实例均手算吻合），故非全盘失效，但**不可无超时保护地使用** | 批量运行超时 + 单独复现 |
| `TimeSeries时间序列函数/自适应滤波法/main.m` | **收敛循环只跑一轮**。判据写作 `Terr = [Terr, abs(Terr)]`，而 `Terr` 每轮开头被置空，`abs(Terr)` 恒为空 → `Terr` 永远是空 → `while abs(Terr)>0.00001` 是空比较（假）→ 循环只执行一次，权向量停在单轮更新值上，学习根本没收敛 | 独立计算"恰好一轮"的终值与脚本产物完全相等 |

### 10.2 确证的**工程性**缺陷（16 个脚本）

| 文件 | 缺陷 | 类别 |
| :--- | :--- | :--- |
| `AHP层次分析法/ahp_common.m` | 第 30 行 `str2num(CI)` 应为 `num2str` → **解析错误**；`r=d(1,1)`、`w=v(:,1)` 假设 `eig` 把最大特征值排第一，**不成立** | 语法 + 算法 |
| `TimeSeries…/指数平滑法/single_exponential _smoothing.m` | **文件名含空格**，MATLAB 无法当脚本执行 | 命名 |
| `TimeSeries…/趋势外推预测法/compertz_curve.m`、`logistic_curve.m`、`modified_exponential_curve.m` | 依赖的 `predict1/2/3.m` 变量名与主脚本对不上 → "函数或变量 'k'/'b' 无法识别"；且三和法按 t=1 推导却按 t=0 预测 | 接口 + 算法 |
| `FuzzyMathematicalModel…/多层次模糊综合评价/main.m` | 数组索引必须为正整数 | 索引 |
| `HeuristicAlgorithm…/遗传算法/genetic_algorithms.m` | 索引超出边界（代码假定 100 个目标，数据文件只有约 30 行）；另用 `rand('state',…)` 旧随机数生成器 | 数据错配 |
| `LinearProgramming…/solve_lp.m` | 矩阵乘法维度不匹配 | 维度 |
| `IntegerProgramming…/monte_carro.m`、`NonLinearProgramming…/non_linear_prog.m` | 用 `rand('state',0)` 旧生成器，与 `rng` 冲突 | 废弃 API |
| `TimeSeries…/指数平滑法/third_exponential_smoothing.m` | `legend` 参数无效 | 废弃 API |
| `CellularAutomata…/表面张力/main.m` | 变量 `n` 未定义 | 未定义变量 |
| `MultivariateAnalysis…/聚类分析/main.m` | 输入类型不符（'P 应为 double'） | 类型 |
| `AHP层次分析法/test1.m`、`GreySystem…/GM_full.m` | 需要交互输入，`-batch` 下不可执行 | 环境 |

### 10.3 需注意的遮蔽陷阱

`HeuristicAlgorithm…/遗传算法/遗传算法求解函数优化问题/ga.m` 是**脚本**，与 Global Optimization
Toolbox 的内置函数 **`ga` 重名**。一旦该目录进入路径，内置 `ga` 即被遮蔽——同层的
`求解函数最小值/find_function_min.m` 正因此报"不支持将脚本 ga 作为函数执行"。
**用该目录前先 `rmpath` 或改名。**

### 10.4 因本归档剔除数据而失败的（非代码问题）

`遗传算法/TSP(GA)/main.m`、`模拟退火算法/TSP(SA)/main.m` 需要 **`china.mat`**（0.87 MB，
作为大二进制被剔除）。按 `PROVENANCE.md` §4 的方法可重新取回。

### 10.5 数值正确性验证（**7 批，50+ 项检查，对独立参照**）

不是"能跑就算对"。每一项都把归档实现与**另一条路线**产出的答案对比：手算、MATLAB 内置的
另一实现、不同的数学表述、或穷举局部状态。逐字证据见 `numerics-report.txt` …
`numerics7-report.txt`。

| 批次 | 覆盖 | 结果 |
| :--- | :--- | :--- |
| 1 | Floyd、Dijkf、Huffman、ahp、sglsortexamine、grShortPath、grMinSpanTree | 8 项全一致；grMaxFlows / grTravSale **确证在 R2025b 不可用** |
| 2 | GM(1,1)、简单移动平均、二次指数平滑、指派问题、线性回归、cityblock 距离、PCA | 7/7 ✅ |
| 3 | 模糊矩阵 max-min 合成、灰色关联度、投资 LP、BFS 层数、AHP 单排序检验 | 5/5 ✅ |
| 4 | GM(2,1)、Verhulst、优势分析、一元二次回归、二维最近邻插值、变量聚类、模糊传递闭包 | 7/7 ✅ |
| 5 | 元胞自动机：奇偶规则、激发介质、HPP 气体、DLA、森林火灾、砂堆 | 6/6 ✅（奇偶规则比的是**修正版**，上游缺陷见 §10.1） |
| 6 | n2shortf、fofuf、BGf、concom、fc01、欧拉回路、DFS | 7/7 ✅（欧拉回路比的是**修正版**，上游缺陷见 §10.1） |
| 7 | 加权/趋势移动平均、自适应滤波、目标规划、多目标模糊综合评价 | 5/5 ✅（自适应滤波比的是"是否只跑一轮"） |

**具体参照举例**（说明"独立"到什么程度）：

- **GM(1,1)**：上游用符号 `dsolve` 求解，我用**特征根闭式解**独立算，两者逐值一致。
- **指派问题**：上游 `intlinprog`，我用 `matchpairs`（另一套精确求解器）。
- **回归**：上游 `regress`，我用正规方程 `(X'X)\(X'y)`。
- **PCA**：上游 `pcacov`，我对 `cov` 做特征分解。
- **HPP 气体 / DLA**：**穷举全部 16 种块配置**，验证 Margolus 更新是块内置换、粒子数守恒。
- **灰色关联度 / 优势分析 / 二次平滑**：从原始数据独立重算，不经上游任何函数。

> **结论（含一处自我更正）**：我一度写过"能跑通的核算法数值都对，未发现静默算错"。
> **这句是错的**，当时只覆盖了 20 个算法。补完第 5–7 批后，在"能跑通"的脚本里又挖出
> **4 个算法性缺陷**（§10.1）：`basic_CA.m` 根本不迭代、`Fleuf1.m` 给出非法欧拉回路、
> `BGf.m` 在中等规模网络上不终止、自适应滤波的收敛循环只跑一轮。
>
> **正确结论**：工程性缺陷（解析错误、接口错配、废弃 API、数据错配）容易在实跑中暴露；
> **算法性缺陷不会**——它们不报错，只有拿独立参照逐个对照才会现形。这正是本套验证存在的理由。

### 10.6 修正版

已确证的缺陷，其**净室重写版**放在 `fixed/`（6 个：AHP、指数平滑、趋势外推、模糊综合评价、
奇偶规则元胞自动机、欧拉回路），附独立对照测试。**上游原文一字未改**，仍在本目录 `src/` 内。
详见 `fixed/README.md`。

> **其余文件未做质量判断。** 二级层 1,028 个文件完全未验证；一级层中"通过执行"但未列入
> §10.5 的脚本，其数值也仍未验证。使用前必须实跑，且**必须拿独立参照比对**——实跑只能
> 抓工程性缺陷，抓不到算法性缺陷。

## 11. 编码与换行说明

上游 1,258 个稀疏检出文件中 **883 个原为 GBK**（按 UTF-8 读是乱码），已统一转 UTF-8；其余 375 个 UTF-8 文件为**逐字节原样复制**。逐文件对照表见 `.transcode-map.txt`。

另有 3 个文件（`dijkstra.cpp`、`floyd.cpp`、`gaot/README`）不在稀疏模式内，按 commit 单独补取。

> ⚠️ **首版归档曾把 883 个文件写坏成 `\r\r\n`（双 CR），成因与修法见 `PROVENANCE.md` §5.1。**
> 这批"语法错误"里有 46 个是我造成的，只有 `ahp_common.m` 是真的。现已字节级重做并复验。

## 12. 下一步

1. ~~实跑验证~~ **已完成**（2026-09-23）：7 批数值验证，证据在 `tests/algorithms/`，结论在 §10。
2. **仍未验的**：① 一级层**执行通过但未列入 §10.5 的**脚本（模糊模式识别、`interp_grid`、`af_classify_BP/LVQ`、SA/GA 的 TSP 与函数优化、`stepwise_regression`、`unlinear_regression`、`var_cluster` 的聚类结果等）；② **二级层 1,028 个文件完全未验证**；③ 6 个 GUI 死循环脚本无法无人值守；④ 多目标模糊综合评价里 `muti_objective_fuzzy_analysis.m` 的内部规范化方式未读未验。
3. **M4 开工时**：用本目录做**覆盖度对照**（§9），而非代码来源；§4 的 mechanism 空洞要另找材料。取代码时**优先用 `fixed/`**。
4. 上游 `README.md` 要求"Fork 或借鉴请注明出处 @双愚"，引用时照办；`GraphTheory(图论)/basic/` 另需注明 Sergiy Iglin。
