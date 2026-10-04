# `green/` —— GREEN 对照件（**用本 skill** 出的同一件事）

> ## !! 本目录（连同上一级证据件与 `red/**`）含泄题风险，绝不给写手 !!
>
> **点名**：上一级 `MODELSELECT-evidence.md`（对照结论）与 `../red/README.md` / `../red/writer-self-reports.md`
> **都不给写手**。**这个点名不是穷举**：`../red/out-R{n}/`（别的写手的产物）与本 `README.md` 自身**同样不给写手**。

## 1. 这是什么

Task 14 的 GREEN 侧：与 `red/` **同一件事、同一把尺**，只换一个自变量 —— **用不用本 skill**。

- **同一件事**：`tests/skills/model-select/red/brief.md`（**权威副本在 `red/`**，本目录**不重复内联**）——
  "**选模型 + 给可跑的求解代码**" ＋ 同一题面 `tests/skills/abs-cases/case-A-problem.txt`（2025 MCM Problem A）。
  RED 与 GREEN **逐字共用同一份 brief**（派发前**逐字节比对**，见 `../red/writer-self-reports.md` §0）。
- **GREEN 是**用本 skill 出的那份交付：一位干净上下文写手**多给本 skill**（`SKILL.md` + `references/` + `check-model-select.py`），
  按 skill 的入口决策树（**两跳：先选类、再选方法**）产出。
  **用 skill 出的那份产物**存于 `out-G1/selection.md`（+ 它自己写的骨架 `stair_wear_archard.m`）。
- ★ **它不造第二份权威**：skill 的权威仍在 `.claude/skills/mcm-model-select/`；本目录存的是**它的一次产出**。

## 2. 目录内容

| 路径 | 是什么 |
| :-- | :-- |
| `out-G1/selection.md` | 用本 skill 出的「选模型 + 求解代码」（**GREEN 产物**；泄题风险件） |
| `out-G1/stair_wear_archard.m` | 同一位写手写的可跑骨架（**GREEN 产物**；泄题风险件） |
| `README.md` | 本文件（泄题风险件） |

**上表不声称穷尽**：本目录内任何文件派写手时都不给。

**对照表在上一层**：`../MODELSELECT-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. GREEN 的派发口径（首条 user 消息，逐字）

```text
Read the brief at <WS>\brief.md and produce the deliverable it asks for. The problem statement it refers to is at <WS>\problem.txt.

You have access to a modeling-method skill located at <repo>\.claude\skills\mcm-model-select\ (read its SKILL.md and its references/ directory; you may also run its check-model-select.py). Use it as you see fit to produce the deliverable.

Write your deliverable into <WS>\out-G1\.

Work only from: that brief file, that problem file, the skill directory above, and (only as the skill directs) files under <repo>\corpus\. Do NOT read anything under <repo>\tests\skills\model-select\ except its verify\ subdirectory; in particular do not read tests/skills/model-select/red/, tests/skills/model-select/green/, MODELSELECT-evidence.md, make-evidence.py, or mutate-model-select.py.

Environment fact (not part of the brief): you do not need network access beyond the local repository; work offline from your own knowledge and judgement.

When you are done, reply with a short self-report: which files you read, what you produced (file names and sizes), which model you chose and why, and any issues you hit.
```

（`<WS>` = 隔离容器 `D:\Projects\_scratch\m4-green`，**用完已删**；`<repo>` = 仓根 `D:\Projects\数学建模`。
★ **未用 `fork`** —— 一位新起的干净上下文 `general-purpose` agent，首条 user 消息就是上面这条。）

★ **比 RED 多给的**：**本 skill 三件**（`SKILL.md` · `references/` · 检查器 `check-model-select.py`）。
★ **仍不给**：`corpus/**` 由 skill 指路才可读、**不给**判据结论、**不给**别的写手的产物、**不给**本任务书。

### 3.1 GREEN 写手自述（原文，掩码后）

```text
## 完成：为 2025 MCM Problem A（踏面磨损）选模型 + 可跑 MATLAB 求解器

### 读了哪些文件
- 任务输入：`<WS>\brief.md`、`<WS>\problem.txt`
- skill `mcm-model-select`：`SKILL.md`、`references/mechanism.md`、`references/mechanism/{param_id_stability,ode_ivp,pde_numerical,transport}.md`、`assets/matlab/MAP.md`、`check-model-select.py`、`assets/matlab/mechanism/param_id_stability.m`
- 语料（按 skill 指路）：`corpus/papers/MODEL_MAP.md` 的 §2025 A 节
- 未读任何被禁的 `tests/skills/model-select/` 下内容（`red/`、`green/`、evidence、脚本等一律未碰）。

### 产出了什么
写入 `<WS>\out-G1\`：
- `selection.md` — 32878 字节（主交付物）
- `stair_wear_archard.m` — 10645 字节（可跑求解器，代码亦全文嵌入 `selection.md` §8）

**实测可跑**（MATLAB R2025b，`matlab -batch "stair_wear_archard"`，零参）：
```
truth : k=2  sep=0.240 m  alpha_up=0.70  w_max=0.0120 m  N=1.2e+07  age=12000.0 y
fit   : k=2  sep=0.240 m  alpha_up=0.70  N=1.2e+07  age=11998.4 y
rel.err : N(LS)=0.01%  N(peak)=4.76%  N(vol)=0.00%
direction up:down = 70:30 (truth 70:30)
age 95% CI = [4850.3, 28612.4] y
```
反演 0.01% 复原累计人次/年龄，并复原方向比与并排数；年龄区间宽（如实反映"仅凭磨损时年龄不可精确"）。代码只依赖 base MATLAB（回避 Statistics 工具箱）。

### 选了哪个模型、为什么
- **主类 = mechanism，主方法 = Archard 磨损累积模型 + 参数辨识（反演）**；次类 = statistics（不确定性/分布拟合），辅助 = simulation（蒙特卡洛）。
- 模型：`dw/dt = κ0·φ(p)·r(t) ⇒ w(p)=κ0·N·φ(p)`，`φ(x,y)=φ_x(x)·φ_y(y)` 可分离——`φ_x` 是 k 个高斯混合（**并排人数**）、`φ_y` 是上/下行两成分（**方向偏好**）；最小二乘反演幅度 ⇒ 累计人次 `N`、年龄 `t=N/r̄`；蒙特卡洛给可信区间。
- 理由三条：(1) 一条累积律直接对上题面三个基础问题（频率/方向/并排）与四个难点（一致性/年龄可靠性/修缮/材料来源）；(2) 只需一张非破坏、低成本的踏面深度图；(3) **语料背书**——`MODEL_MAP.md` §2025 A 里该题 5 篇论文 **Archard Law 5/5 命中**，Monte Carlo 4、Bayesian 3、PDE 2、Gaussian mixture 1，与本推荐同型。
- 文件里明确写了**推翻条件 R1–R4**与"人多短时 vs 人少长时在纯磨损下不可辨识"这条诚实结论。

### 拿不准 / 踩过的坑
- 初始用 EM+BIC 选成分数会**过拟合到 k=3**（一个极宽的"假成分"吞噪声），且 `fminsearch` 有坏局部极小（K=2 曾收敛到单成分、N 偏 30%）。修法已固化进代码：给混合成分**宽度上界**、用"平滑剖面峰"做种子并做**多初值重启**、改用**残差型信息量准则**、幅度用**最小二乘投影**。这些都在 `selection.md` §7 注明。
- 合成噪声模型会影响成分数选择：加法噪声+截断到 0 会在翼部造正偏置诱发假成分；改用**乘性**深度噪声后消失——已在代码注释里说明。
- `κ0`（材料+步态磨损系数）与日均人次 `r̄` 需**独立标定**，否则年龄/材料来源问题退化（R2/R3）；本代码的 `κ0`、`sig_k`、`sig_r` 是占位假设，真实使用要换成现场标定值。
```

★ **强度声明**：GREEN 写手"只读了那几份、未读 `tests/**`"**只有自报、没有沙箱可证**（与 RED 同）。
★ **环境旁路**：与 RED 同型 —— GREEN 的会话上下文里**也**可见 `mcm-model-select` 的 skill 描述与 recent commits；
★ **对 GREEN 而言这不是旁路**（它**本来就该**看到 skill）；但 **"未读 `tests/**`" 仍只有自报**。

## 4. 与 RED 的比对口径

同一件事（`../red/brief.md`，逐字）、同一题面、**同一套产物探针**（`../make-evidence.py` 的 `probe_product` / `run_entry`，
**逐份量两侧**）。★ **一处必须写明的不同**：本支的 **skill 检查器 `check-model-select.py` 没有 `--output`** ——
它判的是 **skill 本体**，**不是写手产物** ⇒ **它只对 GREEN 侧有对象；RED 侧"无对象"**。
⇒ **不许**把 RED 在这些判据列上的"空"当成"红"或"绿"（详见 `../MODELSELECT-evidence.md` §0 / §5.2）。

★ **RED 的诚实边界**：见 `../red/README.md` §1 与 `../MODELSELECT-evidence.md` §6、§7。
**样本量 `n = 1` 道题 × 3 位 RED × 1 位 GREEN ⇒ 不许写成"普遍规律"。**
