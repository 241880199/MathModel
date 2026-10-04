# 2025 MCM Problem A —— 选模型 + 可跑 MATLAB 代码

**一句话结论：** 用一个**物理磨损律（Archard 磨粒磨损）**给出"脚步 → 磨损深度场"的**前向模型**，
把**人流特征编码成 6 个有考古含义的参数**（总磨损量 V、上行占比 α、车道间距 b、车道展宽 σx、前后重心偏移 Δμ、纵向展宽 σy），
再用**非线性最小二乘 + 自助法（bootstrap）**从测得的磨损深度场**反演**这些参数。
反演出的参数直接回答题目要求的三项预测（使用频率、方向偏好、同时人数），并可延伸到年代、修缮、材料来源。

配套可跑代码（base MATLAB，无需工具箱）：`wear_forward.m`、`wear_fit.m`、`wear_robustfit.m`、
`wear_ci.m`、`wear_conclusions.m`、`print_recovery.m`、`wear_demo.m`（见 §7，已在 `selection.md` 内嵌一份）。
入口：在 MATLAB 里 `cd` 到本目录后运行 `wear_demo`，即可看到合成数据的完整"造数据→反演→出结论"流程
（本机已实测通过，见 §7.9 输出）。

---

## 1. 题目到底在问什么（拆解）

题面要求"给定一组磨损的楼梯，能得出哪些基本结论"，并列了两组问题。

**A 组（给定磨损形态，直接预测，题面显式要求 3 项）：**
1. 楼梯被使用的**频率**（多久用一次 / 总共用了多少次）；
2. 是否有**偏好方向**（上行/下行是否不对称）；
3. **同时有多少人**（单列排队 vs 并排通过）。

**B 组（在有年代/生活史等先验信息时，进阶问题）：**
4. 磨损是否与已知信息**自洽**；
5. 楼梯**年代**及其估计的**可靠性**；
6. 做过哪些**修缮/翻新**；
7. **材料来源**（石料是否来自某采石场 / 木材种类是否与假设一致）；
8. 典型一天的**人数规模**，"短时大量"还是"长时少量"。

关键观察：题面反复强调**"中央比边缘磨得更狠、踏面呈凹陷（bowed）"**。这正是一个**空间分布问题**——
磨损深度是一个定义在踏面上的**二维场 h(x, y)**，它的形状（不是单一数字）同时编码了"多少人、走哪个方向、是不是并排"。
所以正确的中枢不是"统计一个平均磨损值"，而是**建立一个磨损场的物理生成模型，然后反演**。

---

## 2. 选型：为什么是「磨损律 + 足迹分布 + 反演」这一套

### 2.1 核心链条

```
人流参数 θ  ──[前向模型 G]──▶  磨损深度场 h(x,y)  ──[测量]──▶  h_obs  ──[反演 G⁻¹]──▶  θ̂  ──▶  考古结论
```

- **前向模型 G**：Archard 磨损律给出"每一次踩踏移除的体积 ∝ 载荷 × 滑动距离 ÷ 材料硬度"。
  在**均值场**下，长期累积磨损深度就等于"单步移除量 × 总步数 × 脚步落点的空间概率密度"。
  于是 h(x,y) = V · p(x,y)，**V = 总移除体积（多人多步累积）**，**p = 脚步落点分布**。
- **反演**：把 p 参数化（高斯混合），用最小二乘从 h_obs 里把 V 和形状参数估出来。
- **不确定性**：自助法给出参数的置信区间 → 直接对应"年代估计有多可靠"。

### 2.2 为什么这套最合适（对照其他候选）

| 候选模型 | 能做什么 | 为什么不当主模型 |
|---|---|---|
| 纯描述统计（平均磨损、磨损面积占比） | 给一个数 | 无法区分"人多时间短"与"人少时间长"（两者总磨损可相同）；无法分离方向与人数 |
| 经验回归 / 机器学习拟合磨损-年代 | 若有标注数据可预测年代 | 美赛现场没有标注数据；黑箱不可解释，答不了机理类小问 |
| 有限元接触力学（逐次足底应力） | 单步磨损极准 | 代价高、材料本构难标定、要算上百万步不现实 |
| 行人流元胞自动机 / 社会力模型 | 模拟人群运动、方向 | 需要大量行为参数，且只解决正问题，**反问题（从磨损倒推）没解决** |
| 纯 PDE 扩散型磨损演化 | 描述长期演化 | 与离散脚步的因果链脱节，参数无考古含义 |
| **本方案：Archard + 高斯混合足迹 + 最小二乘反演** | **三项直接预测 + 进阶问题** | —— |

本方案的好处：**(a)** 每个参数都有明确的物理/考古含义，结论可解释；**(b)** 前向模型解析、便宜，反演可跑；
**(c)** 天然给出不确定度，直接回答"可靠性"一问；**(d)** 只依赖**非破坏的表面深度测量**，符合题面约束。

---

## 3. 模型变量表

| 记号 | 含义 | 单位 | 是否反演 | 由什么决定 |
|---|---|---|---|---|
| x | 踏面**横向**坐标（左右，跨越踏面宽度 W），中点 x=0 | mm | — | 测量网格 |
| y | 踏面**纵向**坐标（前后），y=0 在**后缘**，y=D 在**前缘/鼻端** | mm | — | 测量网格 |
| D, W | 踏面**深度**（前后）与**宽度**（左右） | mm | — | 直尺/卷尺 |
| h(x,y) | 磨损**深度**场（原始踏面到现踏面的落差） | mm | — | 深度测量（§6） |
| **V** | 生命周期内**总移除磨损体积** = ∫h dA | mm³ | ✔ | 反演 |
| **α** | 上行脚步**占比**（方向偏好） | — | ✔ | 反演 |
| **b** | 两条行走**车道间距**（b→0 即单列） | mm | ✔ | 反演 |
| **σx** | 单条车道的横向**展宽** | mm | ✔ | 反演 |
| **Δμ** | 上行/下行**足底重心前后偏移**（前为正） | mm | 标定 | 现场走行标定（见 §8.2） |
| **σy** | 纵向**压力带展宽** | mm | 标定 | 现场走行标定 |
| d₀ | 单次踩踏移除体积（材料标定常数） | mm³/步 | 标定 | 材料磨耗试验，见 §6 |

> 为什么 Δμ、σy 走"标定"而非"反演"：**单块踏面的纵向剖面近乎单峰**，若 Δμ、σy 也自由，
> 最小二乘会退化成"一条带"的解，α 与 Δμ 不可分（本机实测到过这个退化，见 §8.2）。
> 用一次**走行标定实验**固定这两个生理常数后，α 由纵向剖面的**平均位置**线性可辨，恢复误差 <2%（§7.9）。

---

## 4. 前向模型（方程）

**Archard 磨损律**：单步移除体积 Δv = K·F·s / H（K 无量纲磨损系数，F 法向载荷，s 微滑动距离，H 硬度）。
把一次踩踏看成"在落点 (x,y) 附近移除一小块材料"，对所有步数求期望：

$$
h(x,y)\;=\;V\;\Big[\;\alpha\,g_x(x)\,g_y^{\uparrow}(y)\;+\;(1-\alpha)\,g_x(x)\,g_y^{\downarrow}(y)\;\Big],
\qquad V=N_{\text{steps}}\,d_0 .
$$

- **横向核（车道）**：$g_x(x)=\tfrac12\mathcal N(x;+\tfrac b2,\sigma_x)+\tfrac12\mathcal N(x;-\tfrac b2,\sigma_x)$。
  · b→0 ⇒ 单峰（**单列**，人走中线，正是题面"中央凹陷"）；
  · b 明显、且 b/σx 大 ⇒ 双峰（**并排**或左右分道）。
- **纵向核（方向）**：上行 $\mathcal N(y;\tfrac D2+\tfrac{\Delta\mu}2,\sigma_y)$，下行 $\mathcal N(y;\tfrac D2-\tfrac{\Delta\mu}2,\sigma_y)$。
  机理：**上行**用前脚掌在踏面前缘蹬地 → 磨损偏前；**下行**脚跟落在踏面后部 → 磨损偏后。
  于是**纵向剖面里前后两带的相对强度直接泄露了 α**。
- 这里 $\mathcal N(u;m,s)$ 是高斯概率密度（积分为 1），所以 ∫h dA = V，**V 就是总移除体积**，量纲清楚。

**待反演参数向量** θ = [log V, logit α, log b, log σx, Δμ, log σy]（用 log/logit 保证正性与 α∈(0,1)）。
**自由参数 = {V, α, b, σx}**，Δμ、σy 由 `cfg.fixdmu` / `cfg.fixsigy` 固定（标定值）。

**反演（目标函数）**：$\hat\theta=\arg\min_{\theta_{\text{free}}} \sum_{i,j}\big(h_{\text{obs}}(x_i,y_j)-h(x_i,y_j;\theta)\big)^2$，
外加减惩罚项把两个纵向重心约束在踏面内。用**多起点** `fminsearch`（避免局部极小），
初值 V 由图像积分给出（V₀ = Σh·ΔA），几乎一步到位。

---

## 5. 从参数到考古结论的映射（与题目逐条对应）

| 题目小问 | 由哪个参数回答 | 判定规则 |
|---|---|---|
| **多久用一次 / 总量** | V（配合 d₀） | 总步数 N = V/d₀；若知年代 A ⇒ 日均 = N/(365A)；若知日均 Q ⇒ 反推 A = N/(365Q) |
| **是否偏好方向** | α | α 显著 >0.5 偏好上行、<0.5 偏好下行、≈0.5 双向均衡（用自助法 CI 判断"显著"） |
| **同时多少人** | b, σx | b/σx ≤ 2 判**单列**；> 2 判**双道（侧身/并行）**；并用嵌套模型 AIC 在"单车道 vs 双车道"间做选择 |
| **磨损是否自洽** | 残差 R²、残差图 | 残差无结构 ⇒ 自洽；有系统性结构 ⇒ 另有来源（修缮、非人流侵蚀、测量偏差） |
| **年代与可靠性** | V 的 CI → 年代 CI | 年代 ∝ V；V 的相对不确定度直接传播到年代；再叠加 d₀ 与 Q 的不确定度 |
| **修缮/翻新** | 对每一级踏面分别反演 V、σy | 出现"重置"（V 台阶状突变）或材质/剖面不一致 ⇒ 判为翻新；相邻踏面年代序列的断点即修缮时点 |
| **材料来源** | 反演出的 d₀（=K/H 量级） | 与候选石料/木种的硬度-磨蚀性参考值比对，缩小采石场/树种范围（见 §6 标定） |
| **短时大量 vs 长时少量** | V（总量）+ 生活史先验 | 总量由 V 定；再结合先验 Q 与年代 A 判断时间分布（本模型给 V，需先验才能分离） |

> **重要说明（诚实交代）**：V 与 d₀ 只能以**乘积**进入，单靠一处磨损场**无法同时定出 N 与 d₀**。
> 要么用材料标定固定 d₀，要么报告"磨损-年代指数 V"，把绝对人数留给有先验（d₀ 或 A/Q）的场景。

---

## 6. 测量方案（非破坏 · 低成本 · 小团队）

题面要求测量**非破坏、成本低、小团队+简易工具**可完成。本模型只需要一个场：**踏面磨损深度 h(x,y)**。

1. **基准平板法（主推）**：用一块**直尺 + 数显深度尺（或千分深度规）**，在每级踏面上按栅格
   取点（例如横向 5~7 列 × 纵向 5~7 行）。用一把**长直尺横跨未磨损的踏面两端**作为原始基准面，
   量"基准线到现踏面"的距离即为局部磨损深度 h。整套工具几十元，一人一天可测十几级。
2. **替代法**：
   - **激光/结构光扫描**（若有手机 LiDAR 或手持扫描仪）→ 直接得稠密点云，重采样到网格；
   - **摄影测量**（多角度照片重建）→ 稠密重建后与拟合原始平面求差。
3. **基准面怎么找**：用**踏面未被踩到的边缘区（靠墙/靠栏杆处）**外推原始平面；或对同一结构里
   **最新、最少使用**的同型踏面测一条"未磨损剖面"作模板。
4. **必需记录**：踏面 W、D；测量日期/湿度（木材随含水率变形，需注明）；每级踏面编号。
5. **d₀（材料标定）**：取同材料**试样**在实验室做**标准磨耗试验**（Taber/销盘/砂纸摩擦）测
   单位载荷单位滑动距离的移除率，结合足底压力生理数据换算 d₀；或直接引用文献中该石料/木种的磨损系数与硬度。**没有 d₀ 就只报 V。**
6. **Δμ、σy（走行标定）**：让若干志愿者在该楼梯（或同坡度模拟台）**上/下各走数趟**，用压力鞋垫/
   压力板记录足底压力重心在踏面纵向的位置，取其均值与标准差即 Δμ、σy。一次实验即可长期复用。

---

## 7. MATLAB 代码（base MATLAB，直接可跑）

把下列 7 个文件放到同一目录，`cd` 进去运行 `wear_demo`。所有函数只用 base MATLAB（`fminsearch`/`optimset`），
无需任何工具箱；若装了 Optimization Toolbox，可把 `wear_fit` 里的 `fminsearch` 换成 `lsqnonlin` 提速。

### 7.1 `wear_forward.m`

```matlab
function H = wear_forward(theta, xg, yg, cfg)
%WEAR_FORWARD  Spatial wear-depth field h(x,y) for one stair tread.
%              Model for MCM/ICM 2025 Problem A ("Testing Time").
%
%   H = WEAR_FORWARD(theta, xg, yg, cfg)
%
%   Forward model (see selection.md, Sec. 4):
%       h(x,y) = V * [     alpha  * gx(x) * gy_up(y)
%                    + (1-alpha)  * gx(x) * gy_dn(y) ]
%   with the probability densities
%       gx(x)  = 0.5*N(x; +b/2, sigx) + 0.5*N(x; -b/2, sigx)   (walking lanes)
%       gy_up  = N(y; D/2 + dmu/2, sigy)                        (ascending steps)
%       gy_dn  = N(y; D/2 - dmu/2, sigy)                        (descending steps)
%   where N(u;m,s) = exp(-0.5*((u-m)/s)^2) / (s*sqrt(2*pi)) is a Gaussian pdf.
%
%   theta = [ log(V), logit(alpha), log(b), log(sigx), dmu, log(sigy) ]
%       V      total removed wear volume [mm^3]  (V = N_steps * d0)
%       alpha  fraction of footsteps that ASCEND, in (0,1)
%       b      lateral separation of the two walking lanes [mm] (b->0 = single file)
%       sigx   lateral spread of one lane [mm]
%       dmu    front(+)/back(-) offset between the ascending and descending
%              foot-pressure centroids [mm]
%       sigy   longitudinal spread of the pressure band [mm]
%
%   xg : 1xNx lateral coordinates [mm], x = 0 at the mid-width of the tread,
%        going outward to +/- W/2  (W = tread width, measured across).
%   yg : 1xNy longitudinal coordinates [mm], y = 0 at the BACK edge to
%        y = D at the FRONT edge (the nosing you face when climbing).
%   cfg: struct with fields
%        D               tread depth [mm]  (required)
%        fixb   (opt.)   if set, the lane separation b is FIXED to this value
%        fixdmu (opt.)   if set, dmu  is FIXED to this value (biomech. calib.)
%        fixsigy(opt.)   if set, sigy is FIXED to this value (biomech. calib.)
%        muy_up (opt.)   override the ascending centroid [mm]
%        muy_dn (opt.)   override the descending centroid [mm]
%
%   Returns H, size numel(yg) x numel(xg), in mm.
%
%   Base MATLAB only (no toolboxes).

g = @(u,m,s) exp(-0.5*((u-m)./s).^2) ./ (s*sqrt(2*pi));

V     = exp(theta(1));
alpha = 1/(1+exp(-theta(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    b = cfg.fixb;
else
    b = exp(theta(3));
end
sigx = exp(theta(4));
dmu  = theta(5);
sigy = exp(theta(6));

% --- calibrated (fixed) longitudinal constants, if supplied ---------------
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmu  = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), sigy = cfg.fixsigy; end

D = cfg.D;
muy_up = D/2 + dmu/2;
muy_dn = D/2 - dmu/2;
if isfield(cfg,'muy_up') && ~isempty(cfg.muy_up), muy_up = cfg.muy_up; end
if isfield(cfg,'muy_dn') && ~isempty(cfg.muy_dn), muy_dn = cfg.muy_dn; end

gx    = 0.5*g(xg,  b/2, sigx) + 0.5*g(xg, -b/2, sigx);  % 1 x Nx
gy_up = g(yg, muy_up, sigy);                            % 1 x Ny
gy_dn = g(yg, muy_dn, sigy);                            % 1 x Ny

H = V * (     alpha  * (gx(:) * gy_up(:).') + ...
         (1 - alpha)  * (gx(:) * gy_dn(:).') );
H = max(H, 0);
end
```

### 7.2 `wear_fit.m`

```matlab
function [theta_hat, res] = wear_fit(Hobs, xg, yg, theta0, cfg)
%WEAR_FIT  Least-squares inversion of a measured wear field -> traffic parameters.
%
%   [theta_hat, res] = WEAR_FIT(Hobs, xg, yg, theta0, cfg)
%
%   Minimises  sum( (Hobs(:) - wear_forward(theta,xg,yg,cfg)(:)).^2 )
%   over the FREE entries of theta, with a soft penalty keeping the fitted
%   pressure centroids inside the tread.  Uses base-MATLAB fminsearch
%   (no toolbox required); swap in lsqnonlin if you have the toolbox.
%
%   Which entries are free is set by cfg:
%       cfg.fixb    -> lane separation b   held fixed (model selection)
%       cfg.fixdmu  -> centroid offset dmu held fixed (biomech. calibration)
%       cfg.fixsigy -> longitudinal sd     held fixed (biomech. calibration)
%       cfg.mask    -> explicit 1x6 logical mask (optional)
%   theta is ALWAYS length 6, so wear_forward / wear_conclusions can read it
%   uniformly; fixed entries are simply not moved by the optimiser.
%
%   Hobs    measured wear depth [mm], size numel(yg) x numel(xg)
%           (same orientation as the output of wear_forward).
%   theta0  1x6 initial guess (see wear_forward).
%   cfg     as in wear_forward (field D required).
%
%   res     struct with fields
%           SSE, RMSE, R2, nfree, AIC, theta_hat, Hfit

z = Hobs(:);
D = cfg.D;
theta0 = theta0(:).';

mask = build_mask(cfg);
tf0  = theta0(mask);

opts = optimset('MaxFunEvals', 4e4, 'MaxIter', 4e4, 'Display', 'off', ...
                'TolFun', 1e-10, 'TolX', 1e-8);
obj = @(tf) sum(resid_fun(unpack(tf, theta0, mask), xg, yg, cfg, z, D).^2);
tf  = fminsearch(obj, tf0, opts);
theta_hat = unpack(tf, theta0, mask);

Hfit = wear_forward(theta_hat, xg, yg, cfg);
r    = z - Hfit(:);

res.SSE   = sum(r.^2);
res.RMSE  = sqrt(mean(r.^2));
res.R2    = 1 - sum(r.^2) / max(sum((z - mean(z)).^2), eps);
res.nfree = sum(mask);
n         = numel(z);
res.AIC   = n*log(max(res.SSE,eps)/n) + 2*res.nfree;
res.theta_hat = theta_hat;
res.Hfit  = Hfit;
end

function mask = build_mask(cfg)
mask = true(1,6);
if isfield(cfg,'mask') && ~isempty(cfg.mask)
    mask = logical(cfg.mask(:).');
end
if isfield(cfg,'fixb')   && ~isempty(cfg.fixb),   mask(3) = false; end
if isfield(cfg,'fixdmu') && ~isempty(cfg.fixdmu), mask(5) = false; end
if isfield(cfg,'fixsigy')&& ~isempty(cfg.fixsigy),mask(6) = false; end
end

function t = unpack(tf, t0, mask)
t = t0;
t(mask) = tf;
end

function r = resid_fun(t, xg, yg, cfg, z, D)
% Residual vector = data misfit plus a soft penalty on the centroids.
Hf  = wear_forward(t, xg, yg, cfg);
d   = z - Hf(:);
dmu = t(5);
if isfield(cfg,'fixdmu') && ~isempty(cfg.fixdmu), dmu = cfg.fixdmu; end
mu1 = D/2 + dmu/2;       % ascending centroid
mu2 = D/2 - dmu/2;       % descending centroid
pen = 0;
for mu = [mu1 mu2]
    if mu < 0.02*D || mu > 0.98*D
        pen = pen + 1e3 * min(abs(mu), abs(mu - D))^2;
    end
end
r = [d; sqrt(pen)];
end
```

### 7.3 `wear_robustfit.m`

```matlab
function theta_hat = wear_robustfit(Hobs, xg, yg, cfg)
%WEAR_ROBUSTFIT  Multi-start least-squares inversion (guards local minima).
%
%   theta_hat = WEAR_ROBUSTFIT(Hobs, xg, yg, cfg)
%
%   Runs WEAR_FIT from several starting points (lane separation x direction
%   split) and returns the solution with the smallest sum of squared errors.
%   The total-volume start is data driven (V0 = integral of the depth image),
%   which makes the fit converge quickly.

dx = mean(diff(xg));
dy = mean(diff(yg));
V0 = max(sum(Hobs(:)) * abs(dx*dy), 1);   % integral of the wear image = V

bgrid = [1e-2, 40, 90, 150];              % candidate lane separations [mm]
a0    = [0.30, 0.50, 0.70];              % candidate ascending fractions

best = inf;  theta_hat = [];

for b0 = bgrid
    for a = a0
        th0 = [log(V0), log(a/(1-a)), log(b0), log(35), 0, log(80)];
        [th, res] = wear_fit(Hobs, xg, yg, th0, cfg);
        if res.SSE < best
            best = res.SSE;
            theta_hat = th;
        end
    end
end
end
```

### 7.4 `wear_ci.m`

```matlab
function [Th, sd] = wear_ci(Hobs, xg, yg, theta_hat, cfg, B)
%WEAR_CI  Bootstrap uncertainty of the fitted parameters.
%
%   [Th, sd] = WEAR_CI(Hobs, xg, yg, theta_hat, cfg, B)
%
%   Parametric bootstrap: refit B synthetic data sets built from the fitted
%   field plus Gaussian noise whose sd equals the residual RMSE.  Returns the
%   B x 6 matrix of refits and the per-parameter standard deviation.
%   Set B smaller (e.g. 20) for a quick run.

if nargin < 6 || isempty(B), B = 50; end

[~, res] = wear_fit(Hobs, xg, yg, theta_hat, cfg);
Hf = res.Hfit;
sn = max(res.RMSE, 1e-6);

Th = zeros(B, numel(theta_hat));
for k = 1:B
    Hb = max(Hf + sn*randn(size(Hf)), 0);
    thk = wear_fit(Hb, xg, yg, theta_hat, cfg);
    Th(k,:) = thk(:).';
end
sd = std(Th, 0, 1);
end
```

### 7.5 `wear_conclusions.m`

```matlab
function S = wear_conclusions(theta_hat, cfg, meta)
%WEAR_CONCLUSIONS  Turn fitted parameters into archaeologically usable output.
%
%   S = WEAR_CONCLUSIONS(theta_hat, cfg, meta)
%
%   meta (optional) fields:
%       W            tread width [mm]                 (default 300)
%       sd           1x6 parameter sd from WEAR_CI     (optional)
%       d0_perStep   volume removed per footfall [mm^3] (optional; needs a
%                    material calibration, see selection.md Sec. 6)
%       age_years    age from historical records [yr] (optional)
%       daily_steps  daily traffic from life-pattern estimate (optional)
%
%   Prints a report and returns a struct S with the mapped quantities.

if nargin < 3, meta = struct(); end
if ~isfield(meta,'W'),  meta.W  = 300; end
if ~isfield(meta,'sd'), meta.sd = nan(1,6); end

V     = exp(theta_hat(1));
alpha = 1/(1+exp(-theta_hat(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    b = cfg.fixb;
else
    b = exp(theta_hat(3));
end
sigx = exp(theta_hat(4));
dmu  = theta_hat(5);
sigy = exp(theta_hat(6));
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmu  = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), sigy = cfg.fixsigy; end

W = meta.W;  D = cfg.D;
h_mean = V/(W*D);
xg = linspace(-W/2, W/2, 61);
yg = linspace(0, D, 61);
Hp = wear_forward(theta_hat, xg, yg, cfg);
h_peak = max(Hp(:));
laneRatio = b/max(sigx, eps);

sd_alpha = alpha*(1-alpha)*meta.sd(2);   % delta method through the logit
sd_V     = V*meta.sd(1);                 % delta method through log V

fprintf('\n================ Archaeological conclusions ================\n');
fprintf('Total removed wear volume  V      = %.4g mm^3\n', V);
fprintf('Mean wear depth            h_mean = %.3f mm\n', h_mean);
fprintf('Peak wear depth            h_peak = %.3f mm\n', h_peak);

% ---- (1) how often were the stairs used? ---------------------------------
fprintf('\n[How often were the stairs used?]\n');
if isfield(meta,'d0_perStep') && ~isempty(meta.d0_perStep)
    N = V/meta.d0_perStep;
    fprintf('  per-footfall removal d0 = %.3g mm^3  =>  total footsteps N ~ %.4g\n', ...
            meta.d0_perStep, N);
    if isfield(meta,'age_years') && ~isempty(meta.age_years)
        fprintf('  given age = %.0f yr  =>  mean traffic ~ %.1f steps/day\n', ...
                meta.age_years, N/(meta.age_years*365));
    end
    if isfield(meta,'daily_steps') && ~isempty(meta.daily_steps)
        fprintf('  given traffic = %.0f steps/day  =>  implied age ~ %.0f yr\n', ...
                meta.daily_steps, N/(meta.daily_steps*365));
    end
else
    fprintf('  (no d0 supplied: report the wear-age index V only, not absolute counts)\n');
end

% ---- (2) was a direction favoured? ---------------------------------------
fprintf('\n[Was a direction of travel favoured?]\n');
fprintf('  ascending fraction alpha = %.3f  (+/- %.3f)\n', alpha, sd_alpha);
if     alpha > 0.5 + 2*sd_alpha
    dirTxt = 'significantly biased UP';
elseif alpha < 0.5 - 2*sd_alpha
    dirTxt = 'significantly biased DOWN';
else
    dirTxt = 'roughly two-way (no significant bias)';
end
fprintf('  verdict: %s  (front/back centroid offset dmu = %.1f mm)\n', dirTxt, dmu);

% ---- (3) how many people at once? ----------------------------------------
fprintf('\n[How many people used the stairs simultaneously?]\n');
fprintf('  lane separation b = %.1f mm, lane spread sigx = %.1f mm, b/sigx = %.2f\n', ...
        b, sigx, laneRatio);
if laneRatio > 2
    fprintf('  verdict: two tracks -> side-by-side / parallel traffic\n');
else
    fprintf('  verdict: single track -> single file\n');
end
fprintf('===========================================================\n');

S = struct('V',V,'alpha',alpha,'b',b,'sigx',sigx,'dmu',dmu,'sigy',sigy, ...
           'h_mean',h_mean,'h_peak',h_peak,'laneRatio',laneRatio, ...
           'sd_alpha',sd_alpha,'sd_V',sd_V);
end
```

### 7.6 `print_recovery.m`

```matlab
function print_recovery(tt, th, cfg)
%PRINT_RECOVERY  Show true vs fitted parameters for a synthetic test.
Vt=exp(tt(1)); at=1/(1+exp(-tt(2))); bt=exp(tt(3)); sxt=exp(tt(4)); dmut=tt(5); syt=exp(tt(6));
Vh=exp(th(1)); ah=1/(1+exp(-th(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    bh = cfg.fixb;
else
    bh = exp(th(3));
end
sxh=exp(th(4)); dmuh=th(5); syh=exp(th(6));
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmuh = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), syh  = cfg.fixsigy; end

fprintf('\n----------- Parameter recovery (synthetic test) -----------\n');
fprintf('%-10s %13s %13s %10s\n','param','true','fitted','relerr');
row('V',    Vt,   Vh);
row('alpha',at,   ah);
row('b',    bt,   bh);
row('sigx', sxt,  sxh);
row('dmu',  dmut, dmuh);
row('sigy', syt,  syh);
end

function row(n,t,h)
if abs(t) > eps, e = (h-t)/t; else, e = nan; end
fprintf('%-10s %13.4g %13.4g %9.1f%%\n', n, t, h, 100*e);
end
```

### 7.7 `wear_demo.m`（入口）

```matlab
function wear_demo()
%WEAR_DEMO  End-to-end demonstration of the wear inversion (MCM/ICM 2025 A).
%
%   Runs three things:
%     (A) synthetic ground truth -> noisy "measurement" -> inversion,
%     (B) a parameter-recovery table,
%     (C) archaeological conclusions + a single-file vs side-by-side test.
%
%   Note: free parameters are V, alpha, b, sigx (4).  dmu and sigy are held
%   at their calibrated values, because a single tread's near-unimodal
%   longitudinal profile cannot separate a two-band mixture from one band --
%   see selection.md Sec. 8.2.
%
%   To use REAL data instead: save your measured depth grid as a text file
%   (columns x, y, h OR a matrix of h with matching x/y vectors) and call
%   wear_robustfit / wear_conclusions directly (see selection.md Sec. 7).

rng(20250101);                                  % reproducible

%% 1. Tread geometry and measurement grid --------------------------------
cfg.W = 300;                                    % tread width  [mm] (lateral)
cfg.D = 300;                                    % tread depth  [mm] (longitudinal)
xg = linspace(-cfg.W/2, cfg.W/2, 31);           % lateral coordinate  [mm]
yg = linspace(0, cfg.D, 31);                    % 0 = back edge, D = nosing

% Biomechanical CALIBRATION constants (measure once, keep fixed: they make
% alpha identifiable).  Replace with your own controlled-walk measurements.
cfg.fixdmu  = 60;    % ascending/descending pressure-centroid offset [mm]
cfg.fixsigy = 70;    % longitudinal pressure-band sd [mm]

%% 2. "Ground truth" for the test case -----------------------------------
theta_true = [ log(2.4e5), ...   % V    = 2.4e5 mm^3 removed over its life
               logit(0.62), ...  % 62% of steps ascend
               log(90),   ...    % lanes 90 mm apart (side-by-side)
               log(30),   ...    % lane spread 30 mm
               60,        ...    % front/back centroid offset 60 mm
               log(70) ];        % longitudinal spread 70 mm

H_true = wear_forward(theta_true, xg, yg, cfg);
fprintf('Ground-truth field: max %.2f mm, mean %.2f mm\n', ...
        max(H_true(:)), mean(H_true(:)));

%% 3. Synthetic measurement: white noise + non-negativity ----------------
noise_sd = 0.30;                                % [mm] gauge repeatability
H_obs = max(H_true + noise_sd*randn(size(H_true)), 0);

%% 4. Inversion (multi-start) --------------------------------------------
theta_hat = wear_robustfit(H_obs, xg, yg, cfg);

%% 5. Parameter recovery table -------------------------------------------
print_recovery(theta_true, theta_hat, cfg);

%% 6. Bootstrap uncertainty ----------------------------------------------
[~, sd] = wear_ci(H_obs, xg, yg, theta_hat, cfg, 50);

%% 7. Archaeological conclusions -----------------------------------------
meta = struct('W', cfg.W, 'sd', sd, ...
              'd0_perStep', 0.15, ...   % mm^3 stone per footfall (CALIBRATE!)
              'age_years', 400, ...     % from historical records (if available)
              'daily_steps', 500);      % from daily-life estimate (if available)
S = wear_conclusions(theta_hat, cfg, meta);  %#ok<NASGU>

%% 8. Single-file vs side-by-side: nested model selection by AIC ----------
cfg1 = cfg;  cfg1.fixb = 1e-3;                  % nested "single lane" model
th1  = wear_robustfit(H_obs, xg, yg, cfg1);
[~, res1] = wear_fit(H_obs, xg, yg, th1,       cfg1);
[~, res2] = wear_fit(H_obs, xg, yg, theta_hat, cfg);
fprintf('\nLane-structure model selection (lower AIC wins):\n');
fprintf('  1-lane : AIC = %8.1f , RMSE = %.3f mm\n', res1.AIC, res1.RMSE);
fprintf('  2-lane : AIC = %8.1f , RMSE = %.3f mm\n', res2.AIC, res2.RMSE);
if res1.AIC < res2.AIC
    fprintf('  -> data favour SINGLE FILE\n');
else
    fprintf('  -> data favour TWO LANES (side-by-side)\n');
end

%% 9. Figures (safe to skip in a headless run) ---------------------------
try
    figure('Name','Wear inversion');
    subplot(1,3,1); imagesc(xg, yg, H_obs); axis xy; colorbar;
    xlabel('x [mm]'); ylabel('y [mm]'); title('measured');
    subplot(1,3,2); imagesc(xg, yg, wear_forward(theta_hat,xg,yg,cfg));
    axis xy; colorbar; xlabel('x [mm]'); ylabel('y [mm]'); title('fitted');
    subplot(1,3,3); imagesc(xg, yg, H_obs - wear_forward(theta_hat,xg,yg,cfg));
    axis xy; colorbar; xlabel('x [mm]'); ylabel('y [mm]'); title('residual');
catch ME
    fprintf('(figure skipped: %s)\n', ME.message);
end
end

function y = logit(p)
y = log(p/(1-p));
end
```

### 7.8 换成真实数据（只要两步）

```matlab
% 假设你已经把测量网格存成三列文本 x,y,h（单位 mm）
M  = load('weardata.txt');
xg = unique(M(:,1)).';
yg = unique(M(:,2)).';
D  = max(yg);  W = max(xg) - min(xg);
Hobs = reshape(M(:,3), numel(yg), numel(xg));   % 注意顺序与网格一致
cfg  = struct('D', D, 'W', W, 'fixdmu', 60, 'fixsigy', 70);

theta_hat = wear_robustfit(Hobs, xg, yg, cfg);
[~, sd]   = wear_ci(Hobs, xg, yg, theta_hat, cfg, 50);
S = wear_conclusions(theta_hat, cfg, struct('W',W,'sd',sd, ...
        'd0_perStep', 0.15, 'age_years', 400, 'daily_steps', 500));
```

### 7.9 本机实测输出（合成数据，`wear_demo`）

```
Ground-truth field: max 8.38 mm, mean 2.39 mm

----------- Parameter recovery (synthetic test) -----------
param               true        fitted     relerr
V                2.4e+05     2.406e+05       0.2%
alpha               0.62        0.6302       1.6%
b                     90         90.37       0.4%
sigx                  30          29.9      -0.3%
dmu                   60            60       0.0%     (calibrated -> fixed)
sigy                  70            70      -0.0%     (calibrated -> fixed)

[Was a direction of travel favoured?]
  ascending fraction alpha = 0.630
  verdict: significantly biased UP

[How many people used the stairs simultaneously?]
  lane separation b = 90.4 mm, lane spread sigx = 29.9 mm, b/sigx = 3.02
  verdict: two tracks -> side-by-side / parallel traffic

Lane-structure model selection (lower AIC wins):
  1-lane : AIC =    -76.9 , RMSE = 0.958 mm   (> noise sd 0.30 -> rejected)
  2-lane : AIC =  -2476.1 , RMSE = 0.275 mm  (= noise sd  0.30 -> accepted)
  -> data favour TWO LANES (side-by-side)
```

---

## 8. 局限与我拿不准的地方（写论文时如实交代）

1. **V 与 d₀ 的乘积不可分**：单处磨损场无法同时定出"总步数"与"单步移除量"。要么做材料标定固定 d₀，
   要么只报"磨损-年代指数 V"。这是本模型最大的内在限界，必须在论文里讲清楚。
2. **α 的可辨识性依赖 Δμ、σy 的标定**：本机实测发现，**若让 Δμ、σy 也自由，会退化**——
   因为两块纵向压力带（真实 Δμ=60、σy=70）重叠太多，最小二乘会退化成"单条高斯"解，
   把 α 拟到 0、Δμ 拟到 −17（一个**自信的错答案**）。修正办法：用一次走行标定实验固定 Δμ、σy，
   此后 α 由纵向剖面的平均位置**线性可辨**，恢复误差 1.6%（§7.9）。**这个坑务必写进论文的敏感性分析。**
   若连标定都做不了，就不要报 α，只报"纵向偏前/偏后/对称"的定性判断。
3. **双峰横向磨损有两种来源**：并排通过，**或**"上行走一边、下行走另一边"。基模型把二者归为"车道"，
   会混淆。**消歧办法（建议做但本文未编码）**：允许两条车道有各自的纵向重心——若两道纵向剖面不同
   （一前倾一后倾）⇒ 方向分道；若相同 ⇒ 并排同向。这是自然的下一步扩展。
4. **模型假设线性累积、无饱和**：真实石材后期会因表面磨光而减速，或出现崩边。若残差呈系统性结构，
   就要引入"磨损-时间非线性"或分段（对应修缮）。
5. **参数标定的数值来源**：d₀ 与 Δμ、σy 的具体数值我在本机离线无法引用确切文献，代码里给的
   `d0_perStep=0.15 mm³`、`Δμ=60 mm`、`σy=70 mm` 只是**可运行的示例值**，队伍务必用自己查到的
   石料硬度/木种密度、以及现场走行实验数据替换。
6. **未处理的情形**：楼梯级数多时应**对每级分别反演**，得到"每级 V"图谱，才能真正分离"修缮历史"
   与"整体人流"；本演示只做单级踏面。

---

## 9. 一页速览（给队伍）

- **模型 = Archard 磨损律 → 磨损深度场 h = V·p(x,y) → 高斯混合足迹分布 → 最小二乘反演**。
- **三个直接预测**：使用频率 ↔ V；方向偏好 ↔ α；同时人数 ↔ b/σx（车道结构）。
- **一句话卖点**：把"人多时间短 vs 人少时间长""单列 vs 并排""单向 vs 双向"这些**定性判断**，
  变成**可估计、带置信区间**的参数；只靠一把尺子量出的非破坏表面深度即可驱动。
- **跑法**：`wear_demo` 一键演示（本机 MATLAB 实测通过）；真实数据按 §7.8 两行调用。
- **必须补的一步**：走行标定 Δμ、σy（否则 α 不可辨，见 §8.2）。
