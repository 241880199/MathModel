# Task 14 RED 基线的派发口径与写手自述（`mcm-model-select`）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件写明**派发口径**与**写手读了什么**。任何「写手」agent 读过本文件，产出的就不再是 RED 基线。
> 与它同案看待的还有本目录的 `README.md` 与上一级的 `MODELSELECT-evidence.md`。

【为什么有这个文件】本任务唯一**无法靠单变量复核**的东西是「写手到底读到了什么」：它只能靠**审计写手的自报**。

【来源 —— 照实记】本文件的提示词与自述是**逐字转录自会话内 `SubagentHandback` 投递的文本**（写手回给调度者那段），
**不是**从 transcript 文件里机器摘的 ⇒ **没有**机器可复核的「逐字节」保证，只有**转录级**的忠实度声明。

【对原文的唯一加工】写手自述里写了**绝对路径** ⇒ 掩码之：`D:\Projects\_scratch\m4-red`
→ `<WS>`。除此之外**逐字未改**。

【强度声明】「写手是否真的只读了那一份 brief 与题面」**只有自报、没有沙箱可证**（另外：**未用 `fork`**——
三个写手都是新起的干净上下文 `general-purpose` agent，首条 user 消息就是下面那条提示词本身）。
**自报一致 ≠ 已证**。

---

## 0. 派发口径（三个写手逐字同一份提示词，只换输出目录）

```text
Read the brief at <WS>\brief.md and produce the deliverable it asks for. The problem statement it refers to is at <WS>\problem.txt. Write your deliverable into <WS>\out-R{n}\. Work only from that brief file and that problem file - do not read or write any other file.

Environment fact (not part of the brief): you do not need network access; work offline from your own knowledge and judgement.

When you are done, reply with a short self-report: which files you read, what you produced (file names and sizes), which model you chose and why, and any issues you hit.
```

（三个写手之间**只有 `out-R{n}` 这一个 token 不同**。）

**给写手的那份 brief 是**仓内权威件 `tests/skills/model-select/red/brief.md` 的**副本**，派发前**逐字节比对**过（当场跑过）：

```text
brief identical: True | bytes: 980
```

⇒ 写手拿到的 brief **就是我们入库的那一份**（`read_bytes()` 直接比，不经 blob）。**题面**同理
（`case-A-problem.txt` 的副本，sha256 前 16 位 `4a0cb7e074978239` 两侧一致）。

### 0.1 为什么 brief 里**没有**契约词、**没有**来源 —— 中立性抉择

- **没有契约词。** brief **只问**「选模型 + 给可跑的求解代码」——**不提**「两跳」「类索引」「六格」
  「判据」「骨架路径」这些**本 skill 契约里的词**。理由：一旦提了，写手就会**照着契约的形态**去凑，
  RED 就不再是"没受过本 skill 约束"的基线。
- **没有来源。** 不给本 skill、不给语料、不给判据、不给本任务书。
- ★ **唯一算限定的一句是**「**用 MATLAB**」—— 它**不是** skill 内容，是为了让**两侧的"代码能不能跑"
  落在同一把尺上**（GREEN 的骨架也是 MATLAB）。

---

## 1. R1 写手自述（原文，掩码后）

```text
Done. Both deliverables are written and the MATLAB solver was verified end-to-end.

## Files read
- <WS>\brief.md
- <WS>\problem.txt
(No other files were read or written.)

## Files produced (in <WS>\out-R1\)
- selection.md — 22,154 bytes (477 lines)
- stairwear.m — 10,607 bytes (239 lines)

## What I produced
The problem is 2025 MCM Problem A ("Testing Time: The Constant Wear On Stairs") — infer traffic frequency, direction bias, and simultaneity from a worn stair, plus age consistency, repairs, and material source.

- A measurement protocol: a non-destructive depth map h(x,y) of the tread from a straightedge + feeler gauges, caliper probe, or phone photogrammetry (cheap, small-team, minimal tools).
- A model: a separable Archard-type abrasive wear field, h(x,y) = k_m·N · p̃x(x)·p̃y(y) + b, where footfall placement is a mixture of lateral Gaussian "lanes" (single-file vs side-by-side) and a depth-direction split (descending lands on the nosing, ascending further back), plus a uniform environmental/aging term b = e·T. Key insight: the abrasive term scales with count and is spatially peaked, while the aging term scales with time and is uniform — decomposing the two separates "how many people" from "how long."
- An inverse solution: analytic seeding + constrained weighted least squares (fminsearch), a 1-lane-vs-2-lane BIC test for the simultaneity question, and a Gauss–Newton covariance for confidence intervals, propagated to every answer.
- A short mapping table from recovered parameters to all eight sub-questions (Q1–Q8), including material-source inference (compare recovered k_m = A/N against candidate materials) and repair detection (break-point in the depth profile).
- Embedded MATLAB code, base-only (no toolboxes): run `stairwear` for a self-test, or `stairwear(Hobs,xvec,yvec)` on real data.

## Model chosen and why
An inverse abrasion/wear-field model rather than a statistical or pure-biology model, because the problem is fundamentally an inverse problem (wear → traffic), and the Archard law gives a physically grounded, low-parameter, separable forward model whose parameters directly correspond to the questions asked (count, direction, lane number). Separability makes the inverse problem well-posed and fast in base MATLAB.

## Verification (I found MATLAB on the machine and smoke-tested it — validating my own deliverable, not reading a new input file)
- Fixed one real bug found by running: inline f(...)(:) indexing is illegal in MATLAB; replaced with a reshape helper.
- Self-test recovers the synthetic truth: f_down 0.305 [truth 0.30], lanes 0.397/0.812 [0.40/0.80], foot depths 0.180/0.049 [0.18/0.05], N 8.35e5 [8e5], 2-lane favoured by BIC.
- A second single-central-lane test returned f_down 0.711 [0.72], one lane at x=0.600 [0.60], and BIC favoured 1 lane — confirming the single-file vs side-by-side call is data-driven, not hard-wired.

## Caveats / uncertainty
- The aging term b is the weakest-identified parameter (only constrained by the less-worn corners), so the weathering-implied age is qualitative; the write-up recommends using the historical age as a prior. N, direction, and lanes are recovered to a few percent; b to ~30% (disclosed rather than hidden).
- N = A/k_m is only as good as the assumed material coefficient k_m (a 20% error there is a 20% error in frequency).
- The footprint spreads σ_x, σ_y are assumed (foot anatomy), not fitted; the model assumes a single "average foot."
- Files are left in the designated scratch container per the brief; I did not delete them (they are the deliverable).
```

## 2. R2 写手自述（原文，掩码后）

```text
## 完成

### 读了哪些文件
- `<WS>\brief.md`（任务书）
- `<WS>\problem.txt`（2025 MCM Problem A：Testing Time — 楼梯的石材磨损）
未读写任何其他文件（仅向指定输出目录写入交付物）。

### 产出了什么（均写入 `<WS>\out-R2\`）
- `selection.md` — 33,543 字节：完整选型说明 + 内嵌全部代码 + 局限交代 + 本机实测输出
- `wear_forward.m` — 3,093 B 前向磨损模型
- `wear_fit.m` — 2,892 B 最小二乘反演（带"自由参数掩码"）
- `wear_robustfit.m` — 1,020 B 多起点反演
- `wear_ci.m` — 770 B 自助法不确定度
- `wear_conclusions.m` — 3,880 B 参数→考古结论映射
- `print_recovery.m` — 953 B 合成数据恢复对照表
- `wear_demo.m` — 4,446 B 一键入口

共 8 个文件。**全部代码在本机 MATLAB（`/d/Software/Matlab/bin/matlab`）实际跑通**，`wear_demo` 端到端无报错。

### 选了什么模型、为什么
**Archard 磨粒磨损律 + 高斯混合足迹分布 + 非线性最小二乘反演。**

链条：人流参数 θ →〔前向〕磨损深度场 h(x,y)=V·p(x,y) →〔测量〕h_obs →〔反演〕θ̂ → 考古结论。

理由：题面反复强调"踏面中央被磨凹（bowed）"，这是**二维空间分布**问题；把磨损场 h(x,y) 建模为
"总移除体积 V × 脚步落点概率密度 p"后，V 回答使用频率与总量、α（上行占比）回答方向偏好、
车道间距 b 与展宽 σx 回答单列 vs 并排——三个题面显式要求的小问各有对应参数，且都带置信区间
（通过自助法），顺带回答"年代估计有多可靠"。对照表中说明了为什么不用纯统计、纯机器学习、
有限元、行人流元胞自动机、纯 PDE。基于题面约束（非破坏、低成本、小团队）只要求**踏面深度栅格测量**。

### 遇到的关键问题（已在交付物 §8.2 如实登记）
第一版把 6 个参数全部自由反演，实测发现**α 与 Δμ 不可辨识**：两块纵向压力带（真实 Δμ=60、σy=70）
重叠过大，最小二乘退化成"单条高斯"解——把 α 拟到 0、Δμ 拟到 −17，一个**自信的错答案**。
修正：把 Δμ、σy 改为**走行标定常数**（新增 `cfg.fixdmu`/`cfg.fixsigy` + 自由参数掩码），
只反演 V、α、b、σx。修正后合成数据恢复：V 误差 0.2%、α 1.6%、b 0.4%、σx −0.3%，
车道结构 AIC 选择正确（单车道 RMSE 0.958 >> 噪声 0.30 → 拒绝；双车道 RMSE 0.275 ≈ 噪声 → 接受）。
这个坑写进了论文级敏感性分析建议。

### 其余拿不准处（已在 §8 列明）
1. V 与 d₀ 只能以乘积出现，单处磨损场无法同时定出总步数与单步移除量——必须材料标定或只报"磨损-年代指数"；
2. 双峰横向磨损可能是"并排"也可能是"上下行分道"，基模型会混淆，给出未编码的消歧扩展；
3. 代码中的 d₀=0.15 mm³、Δμ=60 mm、σy=70 mm 是**可运行的占位示例值**，离线无法引用确切文献，队伍需替换；
4. 演示只做单级踏面，多级逐级反演才能分离修缮历史与整体人流。

注：交付物按要求留在 `out-R2`（即"家"；scratch 容器按约定用完即删，但这是本次交付目标，故保留）。
```

## 3. R3 写手自述（原文，掩码后）

```text
Done. Deliverable produced in <WS>\out-R3\.

FILES READ: Only <WS>\brief.md and <WS>\problem.txt (plus re-reading my own output stair_wear_model.m to embed it). No other files read or written outside out-R3.

FILES PRODUCED (both in out-R3):
- selection.md — 26,774 bytes / 519 lines. Model-selection report: TL;DR recommendation, candidate-model comparison with explicit reject criteria, six-cell model detail, identifiability analysis, non-destructive measurement protocol, sub-question→answer mapping, full embedded MATLAB code, and recorded benchmark output.
- stair_wear_model.m — 14,235 bytes / 338 lines. Self-contained, base-MATLAB (no toolbox) solver. `stair_wear_model` runs a synthetic self-test; `stair_wear_model(Z,x,y,v0)` inverts a real wear map. The embedded code in selection.md is byte-identical to this file (verified by diff).

MODEL CHOSEN AND WHY: a "wear–traffic inversion model" — Archard abrasive-wear law + normalized footfall contact kernel (forward), inverted to recover three things, each with its own independent measurable signature: total removed volume → total footfalls N (frequency); along-tread asymmetry via linear least-squares on [μa·ga, μd·gd] → descent fraction f_d (direction preference); across-tread modal structure via a BIC-scored 1-vs-2 Gaussian-model test → single-file vs side-by-side. A robust MAD/change-point layer handles repairs, and Monte-Carlo gives 95% intervals. Chosen because it is physically grounded and interpretable (defensible to judges), separates the three core questions rather than collapsing them, and lets the paper state honestly which questions wear alone CANNOT answer (notably large-brief-traffic vs small-long-traffic, which is mathematically non-identifiable from wear).

VALIDATION: ran it in MATLAB R2023b via `matlab -batch`. Two-lane benchmark: recovered f_d=0.620 (truth 0.62), N=8.025e6 (truth 8e6), detected 2 lanes at ±0.10 m (truth 0.20 m separation). Single-lane benchmark (via public data-input path): f_d=0.502, N=5.007e6, correctly reported 1 lane (no false positive). Repair detector correctly flagged the lightly-worn step 6 and change-point after step 5.

ISSUES HIT: two real bugs, both caught by running rather than by inspection, both fixed: (1) baseline estimated as the noisy map minimum biased N by ~47% and f_d toward 0.5 — fixed by estimating the reference plane as a free constant term in the fit; (2) clipping negative depths to zero inflated the low-signal tails into an artificial pedestal, which broke the BIC lane test and made EM collapse — fixed by never clipping and by replacing EM with a deterministic best-threshold split (with the clipping removed the two-lane case is detected correctly). Remaining caveats, stated in the report: v0 (per-footfall volume) is an external material+load input the model cannot derive; the footprint kernels and load factors need site calibration; and the two synthetic benchmarks only validate the inversion code, not the assumption that real stairs obey Archard's law.
```

---

## 4. ★★ 环境旁路披露（**照实记**）—— 本轮 RED **不是**"完全没见过本 skill"的基线

写手是本机 Claude Code 的 agent，会话级共享上下文里**另有三处可见面**：

1. **skill 列表**里 `mcm-model-select` 那一行的**描述** —— 它点了名 **"两跳（先选类、再选方法）" / "候选模型 + 判据 /
   带推翻条件的推荐" / "六格详情与可跑骨架路径"**。
2. `git status` 快照（含 `.claude/skills/mcm-model-select/...` 之类的路径）。
3. **Recent commits**（含本 Task 14 的起手提交 `test(m4): Task 14 RED brief + 写在先的预测（RED/GREEN 对照与证据 · 起手）`）。

### 4.1 ★★ 本轮**实打实漏了**：**R3 的产物里出现了本 skill 描述里的词**

**机器抽取**（`MODELSELECT-evidence.md` §2.1）：**R3 的 `selection.md` 里 `六格` 命中 1 次、`推翻` 命中 2 次**
（R3 的标题里有 `## 3. 推荐模型（六格）`、`## 9. 拿不准的地方 / 推翻条件`）——
**那两个词正是本 skill `description` 里的词**。⇒ ★ **R3 已被环境旁路污染**。

- ★★ **订正（2026-10-04 Task 14 复核发现①）**：本行**原写**"**R1 / R2 未抽到同类词**（`六格` / `推翻` 命中 0）"——
  **那是一句无限定、可被一秒推翻的声明**：复核**补探两个本 skill 描述词**后实测
  **`候选模型` R1=0 · R2=1 · R3=1**；**`判据` R1=0 · R2=0 · R3=3**；**`骨架` R1=0 · R2=0 · R3=1**
  ⇒ **只有 R1 全净**（探针面：`grep -c 候选模型 tests/skills/model-select/red/out-R2/selection.md` ⇒ **1**）。
  ⇒ **正确读法 = "R1 全净；R2 命中 1 处 `候选模型`；R3 命中多处"**，**不是**"R1/R2 未抽到同类词"。
  ★ **强指纹（`## …六格` / `…推翻条件` 标题）仍是已披露的那两处** ⇒ **实质污染未隐瞒**，多出的是通用词、信号弱。
- ★ **但"未抽到" ≠ "没读到"**：探针只抽了**写着的一组词**，**不声称穷尽**；
  写手"只读了 brief + 题面"**只有自报、没有沙箱可证**。
- ★ **另一处旁路（2026-10-04 Task 14 复核发现②）**：`out-R3/selection.md` **复现了本仓的内部口号**
  （"判据恒真与'声明超过事实'是同一类错误…凡列证据都写明'不声称穷尽'"）—— 该句**不在 brief、不在题面、
  也不在最近提交主题行**，疑**继承自写手 agent 的 `CLAUDE.md` / 记忆文件**（**未证**）⇒
  **RED 臂"不盲"的不止 skill 描述一面**。★ 如实登记，**未重跑、未换人**。
- ★ **处置（照 P8 / 既有先例）**：**不为此重跑 R3、不换写手、不凑数** —— **照实记**。
  **本轮的 RED 一律读作"环境里可见本 skill 描述（及仓库文化）"的基线，不是"纯盲"基线。**

### 4.2 派发口径里**没有**放进提示词的（避免泄漏）

提示词里**没有**：本 skill 的**正文**（`SKILL.md` / `references/`）、`corpus/**`、判据、本任务书、
上一级 `MODELSELECT-evidence.md`、别的写手的产物。**R1/R2/R3 的提示词逐字相同，只换输出目录。**
