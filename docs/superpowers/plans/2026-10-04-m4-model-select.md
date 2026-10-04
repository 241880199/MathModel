# `mcm-model-select`（M4）实施计划（2026-10-04）

设计：`docs/superpowers/specs/2026-10-04-m4-model-select-design.md`（**本计划的每个"为什么"都在那里**，5 轮复核 Closed）。
**先例（照抄其节奏）**：`docs/superpowers/plans/2026-10-03-m2-section-writer.md` —— 同层姊妹支，
任务级走「实现 → 独立复核 → 修复 → 定点复核」，收尾走「全分支终审 → 推送」。

**读数来源**：`corpus/official/INDEX.md`（§2.4 官方 AI 分区 · §2.5 评审导向）·
**本模块的补素材侦察**（库内权威副本 = `docs/mcm-suite-todo.md` §C「M4 开工前的补素材侦察结论」节）·
`corpus/algorithms/INDEX.md`（**★ 它的 §4 自评有错，见 GC2**）· `corpus/papers/MODEL_MAP.md`（**2025 O 奖 43 篇，常用度与"语料有无背书"的依据**）。

**用户已裁（不要再问）**：设计 §0 四条 ——
① **取材范围 = 全部实缺都补** ② **代码骨架语言 = MATLAB 优先** ③ **素材补齐 = 作为本模块的前置一批 Task** ④ **库深度 = 全深度**。

---

## Global Constraints（**每个任务的复审都要拿到这一份**）

1. ★★ **家族外 skill**：`FAMILY_RE` 不含 `mcm-model-select` ⇒ **无 `K2` 指针义务、无 `K3` 零数字约束**、**不改家族计数**（**仍 5**）。**不许**把它塞进家族正则。
2. ★★ **`corpus/algorithms/INDEX.md` §4 的自评是错的，先订正再动手**：`:66`/`:68` 写「**机理类 —— 本归档无 / 最大的空洞**」，
   而 **`《基于MATLAB的高等数学问题求解》/CH14/` 有 8 个独立 ODE 实现**（Euler/RK4/打靶/降阶/解析解）。
   该断言**已被跨件复述成"事实"共 4 处**（**本文件所在台账 2 处 + `INDEX.md` 的 §9 对照表与 §12 各 1 处** —— ★ **按节名定位，不写死行号**）。
   ⇒ **按「改时点标注 + 追加现值、不覆盖旧值」订正**；**不订正，`mechanism.md` 会照着"无素材可用"写**。
3. ★★ **`A9` 的两个数是跨 Task 的共享可变值**：`docs/mcm-writing-discipline.md` 的
   **`:3`**（`grep -rn "mcm-writing-discipline" .claude/` 命中数）与 **`:4`**（`.claude/skills/` 目录数，**现 14**）
   —— `自检件 §A 的 A9` **两个都读、两个都当场重算** ⇒ 本 skill 落地后 **目录数 14 → 15**。
   ★★★ **"哪个 Task 建目录"必须认准（本行初稿错指 Task 4，被计划收口复核实测抓出）**：
   **`A9` 数的是 `.claude/skills/` 下的【任一子目录】**（`check-writing-discipline.py` 的 `SKILLS_DIR.iterdir()`），
   而 **Task 0 的产出就直写 `.claude/skills/mcm-model-select/assets/matlab/MAP.md`** ⇒ **目录在 Task 0 就出现了**
   ⇒ **目录数必须在 `Task 0` 收工时就改成 15**（**不是 Task 4**）；**不改，A9 从 T0 一直红到 T3，而 GC16 正把它列在收工门里**。
   - **Task 0 收工**：`:4` 目录数 **14 → 15** + 名单补 `mcm-model-select`；★ `:3` 此刻**不该变**（T0 不写任何指向纪律文档的文件）⇒ **按当场 `grep` 实跑核一遍**。
   - **Task 4 收工**：`SKILL.md` 首次指向纪律文档 ⇒ **`:3` 按当场 `grep` 实跑改准**（**不许凑数加指针**）。
   ★★ **这正是 m2 姊妹计划 GC2 那条教训**（`docs/superpowers/plans/2026-10-03-m2-section-writer.md:23-31`）：
   *"每个建 skill 的 Task 都要把它改到自己那一步的终值，否则**总有一个 Task 的门必红**"* ——
   **教训我抄对了，却把"哪个 Task 建目录"认错了。**
4. ★★ **盘上素材路径一律写全路径**（设计 §2.2）：`corpus/algorithms/src/…`，**禁 `src/…` 简写**
   —— ★ 防一个**静默假绿**：`MS2` 的抽取只认 `corpus/` 与 `.claude/` 前缀，**简写等于不在抽取面上**。
   ★ 设计 §11 花名册里的 `src/…` 是**"给人读的范围定义"**，**还原为全路径归 Task 0**。
5. ★★ **MATLAB 文件名必须合法 ASCII**（设计 §2.1）：骨架用**蛇形 ASCII**（`shortest_path.m` · `topsis.m` · `sir_seir.m`），
   **不许中文名**（中文名**不能作为 MATLAB 函数被调用**）。**中文名 ↔ ASCII 名 ↔ 六格文件路径**的**三列映射表**随 skill 入库。
6. ★★ **"算得对"靠独立参照**（设计 §4）：每个骨架必须有 `tests/skills/model-select/verify/<方法>.md`，
   含**四要素**（参照类型 · 参照来源 · 运行命令 · 两边读数），**跑得出同一个数才算过**；**不许"跑通即算对"**；
   **随机算法固定种子 + 给多次运行的分布**。
   ★★ **参照类按"方法性质"分派（写死，免逐个拍脑袋）** ——
   ★★ **本表不声称穷尽**（计划定点复核指出：`mechanism` 的 **#6–#9**、`prediction` 的 `interpolation` **不落在任何一行**）——
   **它们的参照类由各自任务书定**（T6 已定 `interpolation` → **已知函数的采样点，插值回原函数**；T1/T8 已定 mechanism 的 #6–#9）。

   | 方法性质 | 参照类 | 落在哪些方法 |
   | :--- | :--- | :--- |
   | **ODE / 差分 / PDE** | **第 1 类：解析解 + 收敛阶** | mechanism 的 #1/#2/#3/#4/#5/#10（能取闭式解的参数） |
   | **确定性算法**（评价/图/规划/统计的经典式） | **第 3 类：手算标准算例** | evaluation 全部 · network 全部 · `optimization` 的 lp/ilp/nlp/goal_programming · prediction 的灰色/平滑/趋势 · statistics 的 pca/聚类/灰色关联 |
   | **随机 / 进化算法** | **第 4 类：已知最优解的小算例 + 固定种子 + 分布** | `optimization` 的 ga/sa/pso/免疫/蚁群/鱼群/ga_variants · `simulation` 的 monte_carlo |
   | **统计推断** | **第 4 类：已知参数的合成数据** | statistics 的 hypothesis_test/anova/bayesian · prediction 的 regression/nn_forecast/arima_forecast · ml 全部 |
   | **★ 三类套不上**（设计 §4.1） | **人工兜底**（见 GC6 末） | `abm` · `dim_reduction` · `cellular_automata` · `queueing`（有闭式 ⇒ 其实可用第 1 类） |
   ★★ **第 2 类（盘上实现交叉）默认不用**；**只在上面四行都不适用时**才用，**且参照件只许取 `corpus/algorithms/fixed/` 的 6 个净室重写版**
   （实测仅 6：`ahp` · `euler_circuit` · `exponential_smoothing` · `fuzzy_evaluation` · `parity_ca` · `trend_extrapolation`），
   **并须写明"参照件与骨架的算法/作者/来源不同、且骨架不是照它改写"**。**其余归档件不得当独立参照**
   （教辅级，`INDEX.md` §10 确证 20 个缺陷含 **4 算法性**）。
   ★★ **三类套不上的兜底（明列、不许假装盖住）**：`abm` = **2–3 agent 手算小例**；`dim_reduction` = **已知簇结构合成流形 + 邻域保持率（kNN 一致性）**；
   `cellular_automata` = **已知规则的标准图案**（生命游戏 glider 周期 = 4）。**且不许写成"已验证"**。
7. ★★ **`MS2` 的路径判定**（设计 §5.1）：**文件**用 `git cat-file -e HEAD:<path>`（**必须 `HEAD:` 前缀**，裸路径 exit 128）；
   **目录级与 glob 用盘检 `test -d`**（**不许用 git** —— `.gitignore` 的目录在 git 里"不存在"、在盘上"存在"）。
   ★ **抽取语法**：只扫**反引号内**、以 `corpus/` 或 `.claude/` 起始的串，**剥掉尾部 `:NNN`**。**不声称穷尽**（见设计 §5.3）。
   ★★ **写作纪律（设计 §5.3 第 1 项——机械判据管不到、必须靠人守）**：
   **指向被忽略目录（`corpus/papers/figures/` · `corpus/papers/formulas/`）的内容，一律用"目录级 + 盘检"或 glob 形态，
   不许写"被忽略目录下的具名文件"**（那种写法在 git 里查不到 ⇒ `MS2` 会**假红**）。
8. ★★ **空集不许判绿**（设计 §5.2）：`MS1`/`MS2`/`MS3`/`MS4`/`MS6` 每一条**都要现取对象集合并打印它的"势"**，**势 = 0 判 `FAIL`**。
   ★★ **但门只在"已写就"的任务上算**：**"已写就" = 该任务书声明的产出文件全部落盘**。
   ⇒ **Task 4（入口与索引；方法文件还没写）不以 `MS1`–`MS4`/`MS6` 为门**，**只以 `MS5` + `MS6` 的"索引自身自洽"面为门**。
   ★★★ **`MS6` 有三个用例（★ 本行初稿一边说"必须拆成两个面"、一边在下文列了三个，名目自相矛盾 —— 末轮核验 B 抓出；以本段为准）**：
   ★★ **`Task 5–12` 的验收句里那句"`MS1`–`MS6` 全绿"，一律指 `--scope class`（类内面）** ——
   **不是** `all`（那会红，见上）；**`Task 4` 的门是 `--scope index-self`**；**`Task 13 起与 `Task 15` 是 `--scope all`**。
   （★ 末次核验 B：**各任务验收句原先无一处写 scope** ⇒ 此处一处写死，**不必逐任务重复**。）
   - **类内面**（**T5–T12 的门**）：**本类**的索引条目 ↔ **本类**的实际方法文件（**双向一致**）；
   - **全库面**（**T15 收口的门**）：**八类合起来**的索引条目 ↔ **全部 66 个**方法文件。
   ★ **理由**：索引在 **T4** 就把 **66 条全列**（那是对的 —— 索引是"两跳"的地图），而**文件要到 T12 才齐** ⇒
   **在 T5–T11 拿"全库面"当门 ⇒ 必红**（★ **收口复核精确化**：**T12 写完 66 件后全库面反可绿**，故受影响的是 **T5–T11**）。
   ⇒ **"已写就"在 `MS6` 上的落法 = 只核本类。**
   ★★ **名目对齐（收口复核 B2）**：`MS6` 实际有**三个用例**，本计划都用到，**别混**：
   ① **自洽面**（**T4 的门**）：**索引 ↔ `MAP.md`**（此刻无方法文件 ⇒ 不能核文件）；
   ② **类内面**（**T5–T12 的门**）：**本类的索引条目 ↔ 本类的实际方法文件**；
   ③ **全库面**（**T15 的门**）：**八类合计 ↔ 全部 66 件**。
   ★ **同理**：`MS2`（素材路径）是**全库面**（T4 起的索引里就有外链 ⇒ 可在 T5–T12 全绿，**不受"文件未齐"影响**）；
   `MS1`/`MS3`/`MS4` 也是**只对本类已写就的文件**判（**势 = 本类该有的件数**，不是 66）。

★★★ **`MS4` 必须加一条"遮蔽守卫"（2026-10-04 Task 3 实测发现，这是本支最值钱的一条）**：
**`MS4` 只判"`matlab -batch` 退出码 0"是不够的** —— **名字若与 MATLAB 的类构造器撞，跑的是内置类、不是我们的文件** ⇒ **假绿**。
**实测**：定名 `prediction/arima.m` 时，MATLAB 的 **`arima` 是类**（`isClass=1`，`which -all` 只给 `toolbox/econ/@arima/arima.m` 与 `@regARIMA/arima.m`）；
**class-folder 优先于同名路径函数** ⇒ 我们那个文件**既不能按名调用、也不能被 `run`**（`run('.../arima.m')` ⇒ 未找到），
而 `matlab -batch "arima"` **会成功（调用的是内置类）** ⇒ **`MS4` 判绿，而我们的骨架一次都没跑**。
⇒ **`MS4` 的判法写死为两条合取**：
1. **`which('<名字>', '-all')` 的首项指向【本仓的 `<名字>.m`】**（**不是**内置/工具箱路径）；
2. **`matlab -batch` 跑它，退出码 0**。
★ **并追加一条独立判据**：**全 66 个骨架名逐个核"是否与 MATLAB 的【顶层类目录】撞名"**。
  ★★ **判据写死为：磁盘上是否存在 `toolbox/**/@<名>`，且其【父目录不以 `+` 开头】**（有命中 ⇒ 红）。
  ★★★ **"父目录不以 `+` 开头"这一限定是本条的关键，不许省**（**计划复核实测抓出的一处假红**）：
  `toolbox/matlab/timeseries/**+tsdata**/@interpolation` **存在**，但它在**包内** ⇒ **类名是 `tsdata.interpolation`**，
  **不遮蔽顶层的 `interpolation.m`**（实测：`exist('interpolation')=0`、`~isempty(meta.class.fromName('interpolation'))=0`）
  ⇒ **照"`find -name "@<名>"` 有命中即红"写，会把 `interpolation` 误判成死文件（假红），而它正是 Task 6 要建的骨架之一。**
  ★★ **也不许用 `meta.class.fromName(<名>)` 当判据** —— **控制者实测它会误报**：
  未把本仓路径置于首位时它把 `anova` 报成"类"，**但 `which -all anova`（加上本仓路径后）把我们的文件排在首位、且跑出来的是我们自己的 struct**
  ⇒ `anova` **只是普通函数撞名**（**路径文件胜出**，已被 `toolbox/stats/hypothesis/anova.m` 与我们的 `anova.m` 并存实测证明）。
  ⇒ **正确判据 = "有没有【顶层】`@<名>` 类目录"**：**有 ⇒ 我们的文件永远不可能被调用（死文件）**；普通函数撞名 或 **包内类目录** ⇒ **都不影响**。
  ★ **实测（控制者亲跑，2026-10-04）**：**当前 18 个骨架名无顶层 `@<名>` 类目录撞名**；**唯一的原撞名是 `arima`**（`toolbox/econ/econ/@arima` —— **父目录 `econ` 非包 ⇒ 真撞名**）⇒ 已改名 `arima_forecast.m`。
  ★ **复核另实测了 48 个未落地名**（全量 66 逐个对 `@*` 目录）：**除 `interpolation` 那个包内假阳外，真实顶层撞名 = 0**。
★ **Task 5–12 的每个类任务开工前先跑这条**（**48 个骨架会再遇到同类**）。★ **判据名沿用 `MS4`**（**不新立第 7 条**——它是 `MS4` 的合取项之一）。
9. ★★ **凡自订阈值一律标 `[社区]`**，**并在输出里带该标记**；凡"提请复核"档**不判死**（退出码不受影响）；
   **不许有恒真判据** —— 每条都要能用**变异**证明它真的会红。
10. **写入一律 `write_bytes`；全 LF（CRLF=0）**。
11. **凡数字必来自当场跑过的命令**；**"我没找到" ≠ "它不存在"**（要写出搜了什么、扫描面边界）；
    全称/强弱断言词要么有实测背书、要么加限定；**凡列清单必写「不声称穷尽」**。
12. **声明了覆盖就必须有一次真的红**；**判据只能从失败方向证明**。
13. ★★★ **不许写"本文件自己命中了 N 次某串"这类自指计数** —— 它会随本文件的每次编辑失效（本仓已栽 5 次）。
    只许写**"排除本件后的读数"**，命令带 `:(exclude)<本件路径>`；讲这一型**只描述机制、不举任何行数**。
    ★ 同族：**别写死本文档的行号**（改用节名/表格行号定位）。
14. ★★ **"加订正注" ≠ "改原句"** —— 改一处错话时，**必须把原句改掉**，不能只在旁边加一句"初稿那句是错的"
    （否则 = 留一句假话 + 一句说它假的话；本仓在两支里各栽过一次）。
15. ★★ **"素材 0" ≠ "语料 0"** —— 说"某方法没有素材"时**必须点明是哪个面**：
    `corpus/algorithms/src/`（算法素材）还是 `corpus/papers/`（**获奖论文语料**）。
    ★ 实测反例：**Lotka-Volterra 算法素材 0，但语料里 4 篇 2025 论文在用**（`corpus/papers/INDEX.md` 的 P2025-B-03/E-02/E-03/E-04）。
16. **收工门（全路径，全绿）** —— ★ **本模块新增的 3 个脚本在 Task 4/13/14 之前还不存在，届时减掉**
    （`check-model-select.py` 建在 **Task 4** · `mutate-model-select.py` 建在 **Task 13** · `make-evidence.py` 建在 **Task 14**）：
    ```
    python .claude/skills/mcm-model-select/check-model-select.py --scope <面>   # ★ 见下行
    ```
    ★★ **这条命令必须带"面"（末轮核验 B 抓出：裸跑走哪个面没写清）** ——
    按 GC8：**Task 4 用 `--scope index-self`（索引↔`MAP.md` 自洽面）**· **Task 5–12 用 `--scope class`（类内面）**· **Task 13 起与 Task 15 用 `--scope all`（全库面）**。
    ★ 三个面的名字**在 Task 4 建检查器时就定死**，并**写进 `check-model-select.py --help`**。
    ```
    python tests/skills/model-select/mutate-model-select.py
    python tests/skills/model-select/make-evidence.py
    python .claude/skills/mcm-memo/check-memo.py --help
    python tests/skills/memo/mutate-memo.py
    python tests/skills/memo/make-evidence.py
    python .claude/skills/mcm-section-writer/check-section.py tests/skills/arch-cases/out-S1.md --section 模型建立 --input tests/skills/arch-cases/brief-S1.md   # 应然红
    python tests/skills/section-writer/mutate-section-writer.py
    python tests/skills/check-writing-discipline.py
    python tests/skills/mutate-writing-discipline.py
    python tests/skills/playbook/check-playbook.py
    python tests/skills/playbook/mutate-playbook.py
    python tests/check-index-pointers.py
    python tests/skills/figure-choose/check-spec-pointers.py            # ★ 家族仍 5 个
    python tests/skills/figure-choose/check-house-style.py
    python tests/skills/figure-choose/check-style-table-freshness.py
    python tests/skills/figure-choose/gen-style-table.py --check
    python tests/skills/figure-choose/fixtures/run-expected.py
    python tests/skills/figure-choose/mutate-figure-style.py
    python tests/skills/plot-python/check-style-freshness.py
    python tests/skills/plot-matlab/check-style-freshness.py
    python tests/skills/table/check-table-style.py
    python tests/skills/table/mutate-table-style.py
    python tests/skills/schematic/fixtures/make-fixtures.py --check
    python tests/skills/topic-select/check-topic-select.py
    python tests/skills/topic-select/mutate-topic-select.py
    ```
    ★★ **已知不在本表内的两个真变异驱动器**（与 `m2` 姊妹计划同披露）：`tests/skills/plot-python/mutate-plot-style.py` ·
    `tests/skills/plot-matlab/mutate-plot-style.py` —— 它们**也不在前几支的门里**（`2026-10-03-m2-section-writer.md` 已披露同一条）
    ⇒ **本支不收**（**理由写明：既有缺口，非本支引入**），**不是静默漏掉**。
    ★ 并按 m2 先例：**本表不声称穷尽全仓脚本**。
17. **不许提交脏树**；任务之间**另起提交**；**不许 `--amend`**。
18. ★ **不许**用"读-改-写写成一条表达式"的写法（先求值左边就截断 —— 清空过本仓一个 880 KB 的文件）。
19. ★★ **临时件只许落两处**：**仓内 `build/`** 或**固定容器 `D:/Projects/_scratch/…`**；**绝不许落盘根**；
    **不许 `%TEMP%`、不许 MSYS `/tmp`**。路径写 `D:/...`；`cd` 之后先 `pwd` 核一次。

## 派发指令必带（每次派 subagent 都要附）

- 任务书路径（本文件的那一节 + 该任务的 brief 文件）· 报告落点 `.superpowers/sdd/task-m4-ms-t<N>-report.md`（**必须真的落盘**）。
- Global Constraints 全文 · 基线 commit（派发前 `git log -1 --format=%H`，**不许用 `HEAD~1`**）。
- 明确：**只回报**状态 + 提交 + 一句话测试结论 + 顾虑；**不要把报告内容复制进回复**。
- ★ **控制者写的任务书本身也是候选错误** —— 执行者遇与实测矛盾，**以实测为准并当场报告**。

---

## 质检记录（**写计划时查出来的陷阱**）

### P1 ★★ 这张花名册是"首版"，**不许当既成事实**
设计 §11 的 66 项**由控制者按盘上实况列出**，**已抽验 12 条 `盘` + 6 条 `补` 均成立**，但**不声称穷尽**。
⇒ **Task 0 必须逐件核**（含**反向扫**：盘上有而册上无的，要补入）。
★ **反向扫已点出 10 项**（★ **本行初稿写"9 项"而列了 10 项，计划复核实测抓出**）：
插值 · 蚁群 ACO · 人工鱼群 · GA 变体 · PERT · TSP · SVM 分类 · SVM 回归 · ELM · **灰色关联/优势分析**（**第 10 项是"移类"而非"新增"**）。
★ 复核另在 `basic/` 扫出 **`grMaxStabSet.m`（最大独立集）· `grMinVerCover.m`（最小点覆盖）· `grMinEdgeCover.m`（最小边覆盖）**
与 `detailed/网络流/{boundnetf,fofuf,restrf}.m`、`《高等数学》/CH15/{rsolve.m,fouriern.m,dft.m,Laplace_Define.m}` ⇒ **Task 0 一并裁**。

### P2 ★★ "盘上已有实现交叉对照"**最容易造假参照**
见 GC6。★ **本仓先例**：设计件初稿把 "`grTheory` 的 `Dijkf.m`" 当例子，**实测 `Dijkf.m` 在 `detailed/最短路/`，
而 `grTheory` 是 `basic/` 下的 `gr*.m`（另一作者）** ⇒ **两个不同源的东西被写成一个**。⇒ **凡引归档件，先核它的目录与作者。**

### P3 ★★ `INDEX.md` 的自评**不能当依据**
它的 §4「机理类 —— 本归档无」**已被实测推翻**（CH14 就在盘上）。★ 另有**两处内部不一致**（**按节名定位**）：
**二级层计数 `510` vs `1,028`**（实测二级层 3 目录 = **511**、三级层 2 目录 = **465**）· **层级口径**。⇒ **Task 0 一并定口径**。

### P4 ★★ 建模不是跑通就算对
★ **本仓教训一**：*"实跑只能证明'不崩'，证明不了'算得对'"* —— **算法性缺陷只有拿独立参照才现形**。
⇒ **每个骨架都必须有参照记录**（GC6 已按方法性质**分派到类**）；★ **且参照要"能算出一个数"**。

### P5 ★★ 那 18 个"补"的项里，有 3 项**使用度极低**
（**排队论** `queueing` 语料 1 对 · **ABM** `agent-based` **0** · **降维** `t-SNE`/`UMAP` **0**）
⇒ **用户已裁"实缺全补"，照补**；★ **但不许在后来的产物里把它们写成"常用"**。

### P6 ★★ 模型形态层要**分两个面**说（**本行初稿说错，被计划复核实测推翻**）
- **算法素材面**（`corpus/algorithms/src/`）：SIR/SEIR · Lotka-Volterra · 热传导/波动/反应扩散 · 参数辨识 · 稳定性分析 **全 0**；
- ★★ **语料面**（`corpus/papers/MODEL_MAP.md`，2025 O 奖 43 篇）：**`differential equation` 25 行 · `partial differential equation` 16 行 · `Lotka-Volterra` 19 行** ⇒ **有实例可提炼**；
  ★★ **两数不许并列相加**（计划定点复核实测）：**那 16 行 `partial differential equation` 全部也含 `differential equation`**（**16/16 重叠**）⇒
  **`differential equation` 25 行里已包含 PDE 那 16 行**，**PDE 不是额外的 16 行**。
  ★ **确为 0 的是**：`SIR model` · `SEIR` · **`heat equation`** · **`wave equation`**
  （★ **注意写全 `heat equation`** —— 单独 `heat` **会误命中 `heatmap`**：`MODEL_MAP.md:515` 那 1 行就是它；**这是本仓"词表太短会误配"的又一例**）。
⇒ **能从语料提炼的（ODE/PDE/Lotka-Volterra）必须带语料指针**；**确无语料的才标 `[社区]` + 教科书级常识**。
★ **不许含混成"模型形态层没有语料背书"**（**本行初稿就是这么写的 —— 那是把"素材 0"说成了"语料 0"**，GC15 同族）。

### P7 ★★ 常用度证据**只有 2025 一年、43 篇**
（`MODEL_MAP.md:17` 自陈）⇒ **超出此范围的"美赛常用度"一律标「无依据、凭印象」**（**并进 `SKILL.md` 的口径，见 Task 4**）。

---

## 文件结构（终态）

```
.claude/skills/mcm-model-select/
├─ SKILL.md                        # 决策树（第一跳）+ 边界声明 + 八类索引 + ★ 口径（不许写什么的清单）
├─ check-model-select.py           # 判据 MS1–MS6（判据本体，全仓唯一一份；Task 4 建全六条）
├─ assets/matlab/
│   ├─ MAP.md                      # ★ 三列映射表：中文名 ↔ ASCII 文件名 ↔ 六格文件路径
│   ├─ evaluation/{ahp,topsis,entropy_weight,multi_level_fuzzy,multi_objective_fuzzy}.m
│   ├─ prediction/{gm11,gm21_verhulst,exp_smoothing,moving_average,trend_extrapolation,
│   │              adaptive_filtering,regression,nn_forecast,interpolation,arima_forecast}.m
│   ├─ optimization/{lp,ilp_assignment,nlp,goal_programming,ga,sa,pso,immune,aco,afsa,ga_variants}.m
│   ├─ mechanism/{ode_ivp,ode_bvp_shooting,reduce_order,difference_equations,pde_numerical,
│   │              sir_seir,lotka_volterra,transport,reaction_diffusion,param_id_stability}.m
│   ├─ simulation/{cellular_automata,monte_carlo,queueing,abm}.m
│   ├─ statistics/{pca,hierarchical_cluster,var_cluster,grey_relational,hypothesis_test,anova,bayesian}.m
│   ├─ network/{shortest_path,mst,maxflow_mincut,min_cost_flow,matching,coloring,tree_traversal,
│   │            euler_hamilton,connectivity_centrality,pert,tsp}.m
│   └─ ml/{nn_classify,svm_classify,svm_regress,elm,clustering,dim_reduction,factor_analysis,discriminant}.m
└─ references/
    ├─ evaluation.md … ml.md       # 八份类索引 = 第二跳（类内判据树 + 三列方法清单）
    └─ <类>/<方法>.md              # ★ 66 份六格方法文件（一方法一文件）

tests/skills/model-select/
├─ mutate-model-select.py · make-evidence.py · MODELSELECT-evidence.md
├─ verify/<方法>.md                # ★ 66 份参照记录（四要素）
└─ README.md
```

---

## Task 0：花名册审定 + 命名约定（**先于一切**）

**产出**：`docs/superpowers/specs/2026-10-04-m4-model-select-roster.md`（花名册终版）· `.claude/skills/mcm-model-select/assets/matlab/MAP.md`（三列映射表）· `corpus/algorithms/INDEX.md` §4 订正 + 连带 4 处。

**硬要求**：
1. **逐件核 §11 的 66 项**：`盘` 的**核路径存在**；`补` 的**核真的缺**（**词边界 `grep -w`**，防子串误配 —— 已知 `SIR` 会命中 `'good morning, Sir.'`、`agent` 会命中 `arrow.m`）。
2. ★ **反向扫**（**不声称穷尽**）：把 `src/` 一级 15 目录 + 三个三级层 + 二级层两个大目录**再扫一遍**，**盘上有而册上无的补入**（P1 的 10 项 + 复核扫出的 5 组候选，**逐条给去向**）。
3. ★ **裁三处已登记的粒度/去重瑕疵**：**模糊聚类归哪条** · **层次聚类被算两次** · **`§11.8 #5` 一行并列三种聚类的粒度**（与"SVM 分类/回归分行"不一致）。
4. ★ **定两组口径**（P3）：**二级层计数**（`510` vs `1,028`，实测 511/465，**`1,028` 复现不出**）· **层级口径**（一级 = ?）。
5. ★★ **建三列映射表**：**中文名 · ASCII 文件名 · 六格文件路径**（**全 ASCII**，GC5）；**它是 Task 4–12 的输入，也是 `MS6` 的前提**。
6. ★★ **订正 `INDEX.md` §4**（GC2）：**改时点标注 + 追加现值、不覆盖旧值**；★ **连带订正那 4 处**（**按节名定位**）。
7. ★ **把 §11 的 `src/…` 全部还原为全路径**（GC4）。
8. ★ **裁 Task 5–12 的"新做 N / 引用 M"分派**（见各任务头；**本任务核定后写进花名册终版**，供各任务照办）。
   ★★ **算式的自核（★ 控制者自己的涟漪扫描补的 —— 复核逐类验过这个算术，但**计划里原先没记**，它只活在提交信息与 gitignored 的台账里 ⇒ 执行者无从自核）**：
   **新做合计 = 3+9+11+3+2+4+11+5 = 48**（**应 == 花名册的 `盘` 48**）·
   **引用合计 = 2+1+0+7+2+3+0+3 = 18**（**应 == 花名册的 `补` 18**）·
   **48 + 18 = 66**（**应 == §11.9 的总数 66**）。
   ★★ **Task 0 要把这个算式连同"逐类之和"写进花名册终版**，**每个类任务开工前先核自己那一行**。
   ★★ **两个词的定义（本行初稿写成"引用 18−N"，那是错公式 —— 计划定点复核实测抓出）**：
   **"新做" = 本类的 `盘` 项数**（归档有素材、但**我们还没有自己的骨架**）· **"引用" = 本类的 `补` 项数**（骨架已在 T1–T3 做过）
   ⇒ **`新做 + 引用 = 本类总数`**（**不是"引用 = 18 − 新做"**：T5 新做 3 ⇒ 引用 **2**，而 18−3 = 15 ✗）。

9. ★★★ **`A9` 的目录数（`:4`）在本 Task 收工前必须改到 15**（**GC3**）——
   **理由**：本 Task 的产出**直写 `.claude/skills/mcm-model-select/assets/matlab/MAP.md`** ⇒ **目录在 T0 就出现**；
   而 `A9` 数的是 `.claude/skills/` 下的**任一子目录** ⇒ **不改，`check-writing-discipline.py` 从 T0 一路红到 T3**
   （★ 收工门 `GC16` 正列着它、且**它不在"届时减掉"的减免名单里**）。
   - **`:4` 目录数 14 → 15** + 名单补 `mcm-model-select`（**改时点标注 + 追加现值、不覆盖旧值**）；
   - ★ **`:3` 此刻不该变**（本 Task 不写任何指向纪律文档的文件）⇒ **按当场 `grep` 实跑核一遍**（应为 **19**）。
   ★★ **本条是控制者自己的"验收 vs 硬要求"全任务扫描补的** —— **改 `GC3` 时漏了本 Task 的硬要求与验收**（本支第 6 次同型）。

**验收**：花名册每一项**能按给出的命令复跑** · 反向扫候选**逐条有去向** · 映射表**三列齐**且**文件名全 ASCII** · `INDEX.md` 那 4 处**全部改准** ·
★ **`check-writing-discipline.py` 实跑绿**（`:4` = **15**、`:3` 按当场实跑写）。

---

## Task 1：前置批次①——机理（7 个方法的骨架 + 参照）

**产出**：`assets/matlab/mechanism/{difference_equations,pde_numerical,sir_seir,lotka_volterra,transport,reaction_diffusion,param_id_stability}.m` + `verify/` 里对应 7 份参照记录。

**硬要求**：
1. **骨架一律 MATLAB**（GC5 命名），**能用内置就用内置**（`pdepe` · `ode15s` · `ode45` **实测全在**）。
2. ★★ **参照照 GC6 的表分派**：`difference_equations`/`pde_numerical`/`transport`/`reaction_diffusion`/`param_id_stability` → **解析解 + 收敛阶**；
   `sir_seir`/`lotka_volterra` → **解析性质**（守恒量 / 平衡点 / 周期解）。
   ★ `param_id_stability` → 也可用**第 4 类**（造真值参数 ⇒ 反演回来要对得上）。
3. ★★ **P6 的两面分派（本任务最要紧的一条）** —— ★★ **逐项定，不许按"一类"打包**
   （**初稿把 `transport` 整项列进"必须带语料指针"，与设计 §9 的"热传导·波动无语料"打架 —— 计划定点复核抓出；根因是 `transport` 一项里含多个子形态**）：
   | 方法 | 语料面 | 依据 |
   | :--- | :--- | :--- |
   | `lotka_volterra` | ★ **有** ⇒ **带语料指针** | `INDEX.md` 的 **P2025-B-03 / E-02 / E-03 / E-04 四篇**在用 |
   | `pde_numerical` | ★ **有** ⇒ **带语料指针** | `MODEL_MAP.md` 里含 PDE 的 **16 行** |
   | `difference_equations` | ★★ **证据偏弱，按"无"处置更稳** ⇒ **标 `[社区]`**（计划定点复核指出：我原写"同属 `differential equation` 的 25 行"，**但离散 ≠ 连续**，那 25 行是**微分方程**、不能直接给差分方程背书）—— ★ **若在写六格时找到 `difference equation` 的确切实例，可改为"有"并补指针** | 自己 grep（`difference equation` **0 命中**） |
   | `transport` | ★★ **拆开**：**扩散**语料 **仅 1 行（薄）** ⇒ **带指针但注明"薄"**；**`heat equation` / `wave equation` 确为 0** ⇒ **标 `[社区]`** | 逐子形态 grep（`diffusion` **1** · `heat equation` **0** · `wave equation` **0**） |
   | `reaction_diffusion` | ★ **无**（`reaction diffusion` / `reaction-diffusion` **0 命中**）⇒ **标 `[社区]`** | 自己 grep 核 |
   | `sir_seir` | ★ **无**（`SIR model` / `SEIR` **0 命中**）⇒ **标 `[社区]` + "教科书级常识"** | 自己 grep 核 |
   | `param_id_stability` | ★★ **无**（`parameter identification` / `identifiability` **0 命中**）⇒ **标 `[社区]`** | 自己 grep 核 |
   ★ **口径**：**有语料的必须带指针、无语料的才标 `[社区]`**；**不许一律**（**两个方向都不许**）。
   ★★ **本表不声称穷尽**（★ **初稿只列 6 行、漏了本任务的第 7 个方法 `param_id_stability`** —— 收口复核 B3 抓出，**已补**）。
4. ★ **不许**把"跑通"当"算对"（P4）。

**验收**：7 个骨架**逐个 `-batch` 跑通（exit 0）** · 7 份参照**四要素齐且跑得出同一个数** · ★ **带语料指针的是【三份】**（`lotka_volterra` · `pde_numerical` · `transport`〔**薄**〕），
**其余四份**（`difference_equations` · `reaction_diffusion` · `sir_seir` · `param_id_stability`）**标 `[社区]`**。
★ **本句初稿写"四份"** —— 那是 `difference_equations` **改判"无"之前**的读数，**改表时漏改了验收句**（末轮核验 A① 抓出）。**以本节那张逐项表为准。**

---

## Task 2：前置批次②——统计 3 + 评价 2

**产出**：`assets/matlab/statistics/{hypothesis_test,anova,bayesian}.m` + `assets/matlab/evaluation/{topsis,entropy_weight}.m` + 5 份参照。

**硬要求**：
1. **内置**：`ttest`/`anova1`/`mle`/`fitdist` · `bayeslm`/`mvnrnd` · ★ **`topsis` 不存在 ⇒ 自己写**。
2. ★★ **参照照 GC6**：`hypothesis_test`/`anova` → **合成数据 + 检验拒绝率**（H0 为真时 5% 水平下拒绝率 ≈ 5%）；
   `bayesian` → **正态-正态共轭的闭式后验 + MCMC 对照**；`topsis`/`entropy_weight` → **手算标准算例（给出算式）**。
3. ★ **贝叶斯**是**数得出的最高频缺口**（`Bayesian` 14 篇）⇒ 参照**要比别项更硬**。
4. ★ **`entropy_weight` 的零值/负值处置**写进骨架注释。

**验收**：5 个骨架跑通 · 5 份参照四要素齐且**跑得出同一个数** · **`topsis` 给出算式**。

---

## Task 3：前置批次③——预测 1 + 仿真 2 + ML 3

**产出**：`assets/matlab/prediction/arima_forecast.m` · `assets/matlab/simulation/{queueing,abm}.m` · `assets/matlab/ml/{dim_reduction,factor_analysis,discriminant}.m` + 6 份参照。
★ **订正（2026-10-04 Task 3 实测）**：原定 `prediction/arima.m` —— **实测不可用**：MATLAB 的 `arima` 是**类构造器**，
class-folder 优先于同名路径函数 ⇒ `arima.m` 既不可按名调用、也不可 `run`（会让 `MS4` 假绿）⇒ 改名 `arima_forecast.m`。
连带已改：`MAP.md` 该行、花名册 §2.2 #10、本文件 §52/§202/§367/§369。

**硬要求**：
1. **内置**：`arima` · `factoran` · `classify` · **`tsne`**（★ **`umap` MATLAB 无内置** ⇒ 骨架只给 t-SNE，**并把"UMAP 需外部包"登记为已知边界**）。
2. ★★ **参照照 GC6**：`arima` → **已知 AR 过程的合成数据**；`queueing` → **第 1 类：M/M/1 的闭式 L/W/ρ**（★ **它其实套得上，不属"三类套不上"**）；
   `abm` · `dim_reduction` → **人工兜底**（2–3 agent 手算小例 / 合成流形 + 邻域保持率）；
   `factor_analysis` · `discriminant` → **已知载荷 / 已知类别的合成数据**。
3. ★ **P5 措辞纪律**：`queueing` / `abm` / `dim_reduction` **使用度极低** ⇒ 文档里**写明"低使用度、照补是为覆盖面"**，**不许写成"常用"**。
4. ★ **`abm` / `dim_reduction` 的参照记录必须写"本项参照是人工兜底、不是可机械核的参照"**。

**验收**：6 个骨架跑通 · 6 份参照四要素齐 · ★ **`abm`/`dim_reduction` 两份明写人工兜底**。

---

## Task 4：入口 `SKILL.md` + 八份类索引 + **完整版判据**

**产出**：`.claude/skills/mcm-model-select/{SKILL.md, check-model-select.py, references/{evaluation,…,ml}.md}`。

**硬要求**：
1. ★★ **第一跳照设计 §2.3 的表**：节点 = **一问 + 判据 + 指向的类**；叶 = **一个类**；
   每叶必带 **① 适用判据 · ② 反面（什么时候不该用它）· ③ 指向该类索引的路径**。
2. ★★ **§1.1 的官方边界必须在 `SKILL.md` 里显式成句**（`MS5` 判）：*"本 skill 给出候选模型与判据；最终选择与结论由队员负责"*，并写清"推荐是候选排序，不是替你拍板"。
3. ★ **`< 150 行`**；**不许复述方法细节**（那是 `references/**` 的活）。
4. ★★ **第二跳（八份类索引）照同一决策树形态写**（§2.3 末）：入口 = **类内方法特征**；叶 = **一个方法**（→ 指向 `references/<类>/<方法>.md`）。
5. ★★ **每份类索引带三列方法清单**，**与 `MAP.md` 一致**（`MS6` 核这个）。
6. ★★ **`SKILL.md` 必须带一张"口径与不做"表**（**本轮补的落点，见设计 §9 与 P5/P6/P7**，四条）：
   ① **常用度证据只有 2025 年、43 篇** ⇒ **超出范围的"常用度"一律标「无依据、凭印象」**（P7）；
   ② **"素材 0" ≠ "语料 0"**（GC15/P6）；
   ③ **P5 的三项低使用度方法不许写成"常用"**；
   ④ **本 skill 不做**：不替你拍板 · 不跑你的数据（M5）· 不出图（M3）· 不做全稿合规（`mcm-selfreview`）· **不判"模型选对了没有"**。
7. ★★ **`check-model-select.py` 建【完整版 `MS1`–`MS6`】**（**不是骨架**）——
   ★ **理由（计划复核 High 1 的修复）**：Task 5–12 的验收要用 `MS1`–`MS4`/`MS6` 当门，**它们必须在这之前就存在**；
   而 **Task 4 自己不以这几条为门**（GC8：方法文件还没写 ⇒ 势 = 0 ⇒ 会红）⇒ **只以 `MS5` + `MS6` 的"索引自身自洽"面为门**。
8. ★★ **`A9` 的两个数——本 Task 只改后者**（★ **本行初稿写"两数同批（目录数 14 → 15）"，与 GC3 矛盾，末轮核验 A② 抓出**）：
   - **目录数（`:4`）已在 `Task 0` 改毕**（**GC3**）⇒ 本 Task **只需核它仍是 15**；
   - ★ **本 Task 要改的是 `:3`** —— `SKILL.md` **首次指向纪律文档** ⇒ **按当场 `grep -rn "mcm-writing-discipline" .claude/ | wc -l` 实跑写**（**不许凑数加指针**）。

**验收**：`SKILL.md` < 150 行且**边界声明 + 口径与不做表**在位 · 八份索引**各有三列清单** · **Task 4 的门（`MS5` + `MS6` 自洽面）绿** ·
★ **`A9` 的两个数分别核**（**本句初稿写"两数跟到 15"，与上面硬要求 8 自相矛盾、且事实也不对** —— 末次核验抓出）：
**`:4` 目录数 = 15**（**T0 已改**）· **`:3` 按当场 `grep -rn "mcm-writing-discipline" .claude/ | wc -l` 实跑写**
（**现值 19**；**M4 的 `SKILL.md` 再添一条 ⇒ 会是 20 上下，绝不会是 15**）⇒ **实跑 `check-writing-discipline.py` 绿**。

---

## Task 5：方法库① —— evaluation（5；**新做 3 · 引用 2**）

**产出**：`references/evaluation/**.md` 5 份 + `assets/matlab/evaluation/` 5 个骨架 + 5 份参照。
★ **本任务新做 3 个骨架**（`ahp` · `multi_level_fuzzy` · `multi_objective_fuzzy`，均 `盘` 上已有素材）；
★ **引用 Task 2 已做的 2 个**（`topsis` · `entropy_weight`）—— **不重做**。

**硬要求**：
1. ★★ **每份六格齐**（`MS1` 判）：适用判据（**含反面**）· 标准建模步骤 · 参数与假设 · 常见坑 · 输出模板 · 代码骨架（**指向 `assets/` 的路径 + 关键片段**）。
2. ★★ **参照照 GC6**：evaluation 全 5 项 → **第 3 类：手算标准算例**（`盘` 上的 AHP/模糊综合**也用手算**，**不许用归档件当参照** —— 它们不在 `fixed/` 六件里）。
3. ★ **盘上素材路径一律全路径**（GC4）。
4. ★ **⑤ 输出模板**指向 M3 的 skill（表 → `mcm-table`；图 → `mcm-figure-choose`），**不重复它们的规则**。

**验收**：5 份六格齐 · 3 个新做骨架跑通 · 5 份参照四要素齐且**跑得出同一个数** · ★ **`MS1`–`MS6` 全绿**（此时方法文件"已写就"，GC8）。

---

## Task 6：方法库② —— prediction（10；**新做 9 · 引用 1**）

**产出**：`references/prediction/**.md` 10 份 + 9 个新骨架（`prediction/` 除 `arima_forecast` 外）+ 10 份参照。
★ **新做 9**（`gm11` · `gm21_verhulst` · `exp_smoothing` · `moving_average` · `trend_extrapolation` · `adaptive_filtering` · `regression` · `nn_forecast` · `interpolation`）；
★ **引用 Task 3 的 `arima_forecast`** —— **不重做**。

**硬要求**：同 Task 5 的 1/3/4 条；★ **参照照 GC6**：灰色/平滑/趋势 → **手算算例**；`regression`/`nn_forecast` → **合成数据**；`interpolation` → **已知函数的采样点**（插值回原函数）。

**验收**：10 份六格齐 · 9 个新骨架跑通 · 10 份参照四要素齐 · `MS1`–`MS6` 全绿。

---

## Task 7：方法库③ —— optimization（11；**新做 11**）

**产出**：`references/optimization/**.md` 11 份 + 11 个骨架 + 11 份参照。

**硬要求**：
1. 同 Task 5 的 1/3/4 条。
2. ★★ **参照照 GC6**：`lp`/`ilp_assignment`/`nlp`/`goal_programming` → **手算算例**（**不许拿 MATLAB 内置当"独立"参照** —— 那是同一台机器的同一套实现）；
   `ga`/`sa`/`pso`/`immune`/`aco`/`afsa`/`ga_variants` → **第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布**。

**验收**：11 份六格齐 · 11 骨架跑通（**随机算法给种子与分布**）· 11 份参照四要素齐 · `MS1`–`MS6` 全绿。

---

## Task 8：方法库④ —— mechanism（10；**新做 3 · 引用 7**）

**产出**：`references/mechanism/**.md` 10 份 + 3 个新骨架（`mechanism/{ode_ivp,ode_bvp_shooting,reduce_order}.m`）+ 10 份参照。
★ **新做 3**（`盘` 上 CH14 有起点素材）；★ **引用 Task 1 的 7 个** —— **不重做**。

**硬要求**：
1. 同 Task 5 的 1/3/4 条。
2. ★★ **参照照 GC6**：3 个新做的 → **第 1 类（解析解 + 收敛阶）**；★ **`盘` 上 CH14 那 8 个 `.m` 可作"起点素材"，但不许当独立参照**（未经净室重写，GC6）。
3. ★★ **P6 的两面分派**（同 Task 1 硬要求 3）：**ODE/PDE/Lotka-Volterra 类的必须带语料指针**；**SIR/SEIR · 热传导 · 波动 标 `[社区]`**。

**验收**：10 份六格齐 · 3 个新骨架跑通 · 10 份参照四要素齐 · ★ **两面的来源分派逐份落实** · `MS1`–`MS6` 全绿。

---

## Task 9：方法库⑤ —— simulation（4；**新做 2 · 引用 2**）

**产出**：`references/simulation/**.md` 4 份 + 2 个新骨架（`simulation/{cellular_automata,monte_carlo}.m`）+ 4 份参照。
★ **引用 Task 3 的 `queueing` · `abm`** —— **不重做**（★ **计划复核 High 2 抓出的漏项：初稿只提了 `abm`、漏了 `queueing`**）。

**硬要求**：同 Task 5 的 1/3/4 条；★ **参照照 GC6**：`cellular_automata` → **人工兜底（已知规则的标准图案，glider 周期 = 4）**；
`monte_carlo` → **合成分布 + 收敛率**（误差按 1/√n 下降）；`queueing`/`abm` 已在 Task 3 定。

**验收**：4 份六格齐 · 2 个新骨架跑通 · 4 份参照四要素齐 · `MS1`–`MS6` 全绿。

---

## Task 10：方法库⑥ —— statistics（7；**新做 4 · 引用 3**）

**产出**：`references/statistics/**.md` 7 份 + 4 个新骨架（`statistics/{pca,hierarchical_cluster,var_cluster,grey_relational}.m`）+ 7 份参照。
★ **引用 Task 2 的 3 个**（`hypothesis_test` · `anova` · `bayesian`）—— **不重做**。

**硬要求**：同 Task 5 的 1/3/4 条；★ **参照照 GC6**：`pca`/聚类 → **合成数据（已知簇结构 + 解释方差）**；`grey_relational` → **手算算例**。

**验收**：7 份六格齐 · 4 个新骨架跑通 · 7 份参照四要素齐 · `MS1`–`MS6` 全绿。

---

## Task 11：方法库⑦ —— network（11；**新做 11**）

**产出**：`references/network/**.md` 11 份 + 11 个骨架 + 11 份参照。

**硬要求**：
1. 同 Task 5 的 1/3/4 条。
2. ★★ **参照照 GC6 = 手算小图**（5 节点可手算最短路/最大流/最小生成树）。
   ★ **`grTheory`（`basic/gr*.m`，作者 Sergiy Iglin）与 `detailed/` 下另一作者的中文实现不是一套，不许混写**（P2）。
   ★ **第 2 类只在必要时用**，且参照件**只许取 `fixed/` 的 `euler_circuit`**（11 项里唯一对得上的）。
3. ★ **`min_cost_flow`（`BGf.m`）在 `INDEX.md` §10.1 登记了算法性缺陷（不终止）** ⇒ **骨架自己写正确版本**，**并在"常见坑"里写明上游那个缺陷**。

**验收**：11 份六格齐 · 11 骨架跑通 · 11 份参照四要素齐 · **`min_cost_flow` 的坑写明** · `MS1`–`MS6` 全绿。

---

## Task 12：方法库⑧ —— ml（8；**新做 5 · 引用 3**）

**产出**：`references/ml/**.md` 8 份 + 5 个新骨架（`ml/{nn_classify,svm_classify,svm_regress,elm,clustering}.m`）+ 8 份参照。
★ **引用 Task 3 的 3 个**（`dim_reduction` · `factor_analysis` · `discriminant`）—— **不重做**。

**硬要求**：同 Task 5 的 1/3/4 条；★ **参照照 GC6 = 合成数据**（已知类别 / 已知因子载荷 / 已知簇结构 + 邻域保持率）；
★ **`dim_reduction` 的"人工兜底"性质要在六格里写明**（Task 3 已在参照记录里写）。

**验收**：8 份六格齐 · 5 个新骨架跑通 · 8 份参照四要素齐 · `MS1`–`MS6` 全绿。

---

## Task 13：变异驱动器 + 判据的变异证明

**产出**：`tests/skills/model-select/mutate-model-select.py` · `tests/skills/model-select/README.md`。

**硬要求**：
1. ★★ **必查项照设计 §5 末**：删一格 · 改错一个素材路径 · 删一份参照 / 删四要素任一项 · 骨架改跑不通 ·
   删边界声明 · 索引里加不存在的方法 · ★ **把某条全路径改回 `src/…` 简写 ⇒ 该条必须从"被 `MS2` 覆盖"变成"不在抽取面上"** ·
   ★ **把方法目录清空 ⇒ `MS1`/`MS2`/`MS3`/`MS4`/`MS6` 必须全红**（空集反证）。
   ★ **订正（2026-10-04 Task 13 实测 —— 本句"把方法目录清空"太宽，以实测为准）**：**只清方法库**（`references/` + `assets/`、**留 `SKILL.md`**）⇒ 红集 = `{MS1,MS3,MS4,MS6}`、**`MS2` 仍绿**（势=3 —— `SKILL.md` 自身带 3 条 `corpus/` 反引号路径 ⇒ **抽取面非空**）。**只有整棵 skill-dir 清空**（连 `SKILL.md` 也没了）才 **六条全红**。⇒ 本句的"`MS2` 必须红"**只有在"整树空"这层成立** —— 与设计 §5.2 原话"**空树**（零文件 / 零路径 / 零参照 / 零骨架）"一致；本句把"空树"写成了"方法目录"，是**转述时的收紧**。**驱动器两种切法都跑了**（`MUT-EMPTY-TREE` 满足"`MS2` 必须红"；`MUT-EMPTY-LIB` 登记"`MS2` 仍绿"这一真读数），见 `tests/skills/model-select/README.md`「空集反证」节。
2. ★ **每条配"必须仍绿"的对照**（干净仓 · 真值 · 假 skill）；**合计行不是末行**。
3. ★ **不许**为凑数写恒真判据；**本支不动**任何既有 `check-*.py` / `mutate-*.py`。

**验收**：`MS1`–`MS6` 在**变异体上逐条真红**、在**真仓全绿** · 变异**全部达预期** · **既有各支的门一个都没动且仍全绿**。

---

## Task 14：RED / GREEN 对照与证据

**产出**：`tests/skills/model-select/{make-evidence.py, MODELSELECT-evidence.md, red/, green/}`。

**硬要求**：
1. ★★ **RED**：新起、无上下文的写手 agent（**不许 `fork`**），**只给场景 brief 路径 + 输出目录**；
   题面用 `tests/skills/abs-cases/case-A-problem.txt`；要求"**选模型 + 给可跑的求解代码**"。
   ★ **预测写在先**（选错类 / 用不存在的函数 / 骨架跑不通 / 把假设当已知 / 无参数辨识），**落地后照实记（含"没发生"的）**。
   ★ **隔离**：复制到仓外固定容器 `D:/Projects/_scratch/m4-red/`（GC19）。
2. ★★ **GREEN**：同一 brief 同一题面，**唯一多给**本 skill。**对照口径**：**只评"选对了类没有 / 骨架能不能跑 / 有没有把假设写明"，不评写法**。
3. ★ **样本量边界必须写在证据件里**（n 小 ⇒ **不得**写成"普遍规律"）。
4. ★ **可重放性**：**先干净 → 捕获 → 提交 → 再跑一次证不动点**（通则 14）。

**验收**：两臂产物入库 · 对照表**标出可比的列** · 证据件**可由生成器重放** · **RED 的预测逐条有结论**。

---

## Task 15：全库收口

**产出**：`docs/mcm-suite-todo.md` 的 §C（M4 行）· **§H.5.8j（新增交付节）** · 进度台账追加。

**硬要求**：
1. **计数**：`.claude/skills/` **14 → 15**（★ **本行的"14 → 15"是回溯口径 —— 目录数已在 `Task 0` 改成 15（GC3），本 Task 只核它仍是 15**；**先当场 `ls -d | wc -l` 核**）；
   **绘图家族仍 5**（**先当场跑 `check-spec-pointers.py` 核**）；★ **`A9` 两个数都要核**（`:3` 在 T4 改过、`:4` 在 T0 改过 —— 本 Task 复跑 `check-writing-discipline.py` 确认绿）。
2. **全库回扫陈旧断言**（**扫描面 = 全仓**，不用 `.claude/` 收窄）：`git grep -n "mcm-model-select" -- .` 逐处看有无残留「未建」；
   ★ **量词写准**（只覆盖"同一行同时含新 skill 名与「未建」"，**不声称覆盖其它**）。
3. ★ **`§H.2.2` 那两类**（"捕获件里印着总 skill 数"**再假一次** · "家族成员计数"**不变、要当场实跑证明**）⇒ 依已定口径**只登记、不重跑**。
4. ★ **登记 B 类残留**：实现中产生的"已披露的局限"（`umap` 无内置 · `abm`/`dim_reduction`/`cellular_automata` 的参照是人工兜底 ·
   §5.3 的写作纪律）**逐条入 §H.5.8j**。
5. **收工门全绿**（GC16 全表）。

**验收**：§C/§H.5.8j 无过期断言 · 收工门全绿 · 台账已追加 · **工作树干净**。

---

## 结束条件

1. Task 0–15 **全部收口**（每个任务走满「实现 → 独立复核 → 修复 → 定点复核」）。
2. **全分支终审**（独立 agent）⇒ 判 `Ready to merge`（或 `With fixes` 后修完）。
3. ★ **终审要专门核两件本模块特有的事**：
   ① **66 份参照记录里"独立性"（不同源）是人工判的** ⇒ 让终审**抽 10 份逐条读**（**这是 `MS3` 判不到的那一层**）；
   ② **语料指针与 `[社区]` 的分派**（P6）⇒ 抽 10 份核"该带语料的带了没有、该标 `[社区]` 的标了没有"。
4. **推送**（§A.5 配方：仓外 worktree + 普通快进 + 两条硬检查；**用户已授「默认推送」**）——
   ★ **同步集必须显式剔除** `corpus/**`、`tests/papers/{recon,reports}/*.png`、**6 件 COMAP 题面**（`tests/skills/topic-select/red/problems/{A–F}.md`）、**`README.md`（差集里的删除项）**。
5. 台账与记忆更新；`agents-busy.py clear`。
