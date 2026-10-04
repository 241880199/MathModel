# 选型报告：磨损阶石的人流反演模型

**题目**：2025 MCM Problem A — *Testing Time: The Constant Wear On Stairs*
**产出**：一个建议模型 + 一份可在 MATLAB 直接运行的求解代码。

---

## 0. TL;DR —— 推荐与一句话理由

**推荐模型：Archard 磨损律 × 足迹核 × 反演的「磨损—人流反演模型」**
（a mechanistic wear–traffic inversion model, with a BIC-based lateral-structure test and a robust repair detector）。

一句话：把每级踏步看成一个**已知形状的接触核**在**未知人流史**下的累积磨损场 —— 磨损图沿踏深方向的**一阶矩**给出上/下行比例，**总体积**给出总人次，跨踏宽方向的**模态结构**给出单列还是并排；由于"总磨损量只记得总人次"，模型必须**显式声明哪些问题可辨识、哪些不可辨识**，这才是本题真正的建模难点。

代码文件：`out-R3/stair_wear_model.m`（正文 `§7` 全文附上，已在本机 MATLAB 跑通，见 `§8`）。

---

## 1. 题目到底要估什么（拆成可辨识量）

题面问了一长串问题，但从"能测到的量"角度它们其实分成两族：

| 族 | 问题 | 对应的可测特征 |
|---|---|---|
| **A. 可用磨损图直接反演** | 多久用一次？方向偏好？多少人同时上？ | 磨损的**总量/尺度**、沿踏深的**不对称度**、跨踏宽的**模态数** |
| **B. 需外部信息才能定，或根本不可辨识** | 磨损是否与史料一致？年龄及其可靠度？修过没有？石料来源？"大流短时"还是"小流长时"？ | 残差、异常步、材料常数、**退化性（identifiability）** |

**关键建模洞察（也是本模型的核心论点）**：题目最后那个问题——"是短时间大量人，还是长时间少量人"——**光靠磨损图在数学上不可辨识**：两者产生**同样的累计磨损**。诚实地把它写出来、并给出"需要哪些外部证据才能拆分"，比假装能算出来分数更高。这是 A 族（可反演）与 B 族（需外部信息）的分界线。

---

## 2. 候选模型与判据

| 候选 | 能答什么 | 判据：为什么选 / 不选 |
|---|---|---|
| ① **纯统计/机器学习回归**（用磨损特征直接回归人流） | 若有大量标注数据，预测力强 | ✗ 本题**没有训练数据**、**没有真值标签**；黑箱、不可外推、无法回答方向/同时性的**物理机理**。评委一眼看穿。 |
| ② **纯经验磨耗律拟合**（只拟合深度随时间） | 给个衰减曲线 | ✗ 无法分离方向与同时性；不停留于"描述"。 |
| ③ **行人流元胞自动机/agent 仿真** | 正向模拟人流→磨损，很直观 | △ 作为**正向验证器**很好，但反演时需大量标定、计算重；不必要。可作为后续增强。 |
| ④ **Archard 磨损律 + 足迹核 + 反演（推荐）** | 频率、方向、同时性三者**各有独立特征**；可外推；可写可辨识性 | ✓ **物理有据、可解释、对评委友好、把"能/不能答"讲清楚**。 |
| ⑤ **贝叶斯分层模型** | 给出后验与不确定度 | ✓ **不是替代，是本模型的包裹层**：把 ④ 的参数反演放进贝叶斯框架，天然给出年龄/材料的可信区间。我们采纳其精神（§4 用 Monte-Carlo 出区间）。 |

**结论**：以 ④ 为骨架，吸收 ⑤ 的不确定度处理，保留 ③ 作为将来正向验证。

**推翻条件（什么时候别用它）**：如果考古队只有"每级一个深度读数"而没有 2D 表面图 → 退化成 1D 版本（只能给总量，方向/同时性降级为假设）；如果材料高度非均质（多孔石料、木纹各向异性）→ Archard 的线性假设失效，应改用经验/半经验磨耗律；如果现场测量精度低于 ~1 mm → 噪声淹没特征，模型退化为上下界估计。

---

## 3. 推荐模型（六格）

**① 模型名**：磨损—人流反演模型（wear–traffic inversion model）。

**② 核心机理（Archard 磨料磨损律）**
每一步脚印造成的局部磨耗深度正比于该处接触压强与滑动距离：

$$ \delta z(x,y) \;=\; \kappa\,\frac{p(x,y)\,s}{H} $$

- $p$ 局部接触压强，$s$ 每次接触的磨料滑动距离，$H$ 材料硬度，$\kappa$ 无量纲磨耗系数。
- 把 $\kappa s/H$ 折成一个**每次踩踏去除的体积** $v_0$（这是材料+载荷的联合常数，**唯一不能从磨损图本身得到**的量，需材料试样或已知产地样品标定）。所有脚印的成本 $v_k = \mu_k v_0$ 里，$\mu_k$ 是上/下行各自的相对载荷因子。

**③ 接触/足迹核（把物理落成形状）**
设踏步沿踏深坐标 $x\in[0,L]$（$x=0$ 是**前缘/鼻端 nosing**，$x=L$ 抵竖板），沿踏宽 $y\in[-W/2,W/2]$。
每一步踩踏在面上撒一个**归一化足迹核** $k(x,y)$；对 $N$ 次踩踏求和得到深度场

$$ z(x,y) \;=\; A\cdot\big[\,f_d\,g_d(x)+(1-f_d)\,g_a(x)\,\big]\cdot h(y), \qquad \iint k\,dA = 1 $$

- $g_d,g_a$：**下行 / 上行**脚印沿踏深的分布（高斯核，$g_d$ 更靠前缘、更集中；$g_a$ 更居中、更弥散）；
- $f_d$：下行占比（**方向偏好**）；
- $h(y)$：跨踏宽的 **walk-line 密度**（单列 = 单峰；并排 = 双峰）；
- $A=\sum\mu_k v_0 N_k$：**总去除体积**（**频率**）。

**④ 反演（三个问题 → 三个独立特征）**

| 问题 | 特征 | 估计子 |
|---|---|---|
| 多久用一次 | 体积 $A$ | $N=A/(\bar\mu\,v_0)$，$\bar\mu=f_d\mu_d+(1-f_d)\mu_a$ |
| 方向偏好 | 沿踏深**不对称** | 把 $z$ 对 $y$ 积分得 $z_x(x)$，对 $[\mu_a g_a,\ \mu_d g_d]$ 做**线性最小二乘**，系数比即 $f_d/(1-f_d)$ |
| 多少人同时上 | 跨踏宽**模态数** | 对 $z_y(y)$ 做 1 核 vs 2 核高斯拟合，用 **BIC** 选模态数（2 峰 ⇒ 并排） |

**⑤ 统计/甄别层（回答 B 族）**
- **修复/翻建**：按级取深度向量，用 **MAD 稳健 z 分数**挑异常级（换过/补过的踏步），再用**单变点扫描**定位翻建边界。
- **材料来源**：反演得到的 $v_0$ 本质是"磨耗难易度"；与候选产地石料的实测 $v_0$ 做**似然比较**，即选最可能的来源。
- **一致性/年龄可靠度**：用残差卡方判"磨损是否与史料相符"；对 $v_0$ 与 $N$ 的不确定度做传播，得到年龄的可信区间。

**⑥ 数据/测量需求**：见 `§5`。核心只需**一次非破坏的 3D 表面扫描**（或直尺+塞尺的降级版）。

---

## 4. 可辨识性分析（本模型的"诚实核心"）

1. **总人次 vs 每人次磨耗**：$z \propto N\cdot v_0$，二者只能定乘积。⇒ 需要材料常数 $v_0$ 才能把 $N$ 单独拆出。模型里用 $v_0$ 显式承载这个外部信息。
2. **方向比例**：可从 $z_x(x)$ 的不对称稳定辨识 —— **前提**是 $(\mu_d,g_d)$、$(\mu_a,g_a)$ 已标定到现场（否则只能辨识"方向加权载荷"这个合成量，而非纯比例）。代码里把这四个量做成可调参数。
3. **"大流短时" vs "小流长时"**：**数学上不可辨识**（同一累计磨损）。必须借外部锚点：史料日期区间、结构可容纳人数、其他磨损证据。模型给出的指导是：**报告 $N$ 及其区间，并说明它只约束"总人次 = 日均 × 天数"，再叠加日期区间给出日均人次的可行三角**。
4. **同时性**：可从跨踏宽模态辨识，但要求扫描横向分辨率 < 足宽（~10 cm）；否则退化。

> 我们把这四条单独成节、写进论文，正是为了不犯"把声明写得比事实大"的错 —— 判据恒真与"声明超过事实"是同一类错误。凡列证据都写明"不声称穷尽"。

---

## 5. 测量协议（非破坏 · 低成本 · 小队伍可做）

| 测量 | 工具 | 产出 | 为什么需要 |
|---|---|---|---|
| **每级踏步 2D 表面图** | 手持结构光/摄影测量，或**直尺 + 塞尺/深度规**沿中心线与横向多条测线 | 深度场 $z(x,y)$，分辨率 ~5 mm | 模型的唯一核心输入 |
| 踏步几何 | 卷尺 | $L$（踏深）、$W$（踏宽）、级数 | 定标核函数 |
| 材料硬度 | 里氏/施密特回弹仪（非破坏） | $H$，辅助定 $v_0$ | 拆 $N$ 与 $v_0$ |
| 每级深度汇总 | 由扫描导出 | 深度向量 $D$（供修复检测） | 甄别翻建 |
| 参考平面 | 靠后缘/边角**未磨区**读数 | 基准 $b$ | 定零点（代码自动估） |

**待测清单要写进论文**，因为题面明确要求"说清需要哪些测量"。上述全部非破坏、可由 2–3 人一天内完成。

---

## 6. 子问题 → 模型答案映射

| 题面问题 | 本模型怎么答 |
|---|---|
| 多久用一次 | $N=A/(\bar\mu v_0)$；除以天数得日均通过量 |
| 是否方向偏好 | $f_d$（及其 95% 区间），偏离 0.5 即偏好 |
| 多少人同时上 | 跨踏宽模态数：1 ⇒ 单列，2 ⇒ 并排；并报车道间距 |
| 磨损是否与史料一致 | 残差卡方 + 与假设人流史的正向模拟对比 |
| 年龄及可靠度 | 由 $N$ 与观测到的历史人流率反推；用 $v_0$、$N$ 的不确定度给可信区间 |
| 是否翻建 | 每级深度向量的稳健异常级 + 变点 |
| 材料来源 | 反演 $v_0$ 与候选产地样品做似然比较 |
| 大流短时 vs 小流长时 | **不可辨识** —— 报告退化性并给出拆解所需的外部证据 |
| 组合结论 | 三特征（体积/不对称/模态）互相独立 ⇒ 可分别下结论、分别给不确定度 |

---

## 7. 可直接运行的 MATLAB 代码

> 单文件、无工具箱依赖。运行 `stair_wear_model` 跑**合成自检**（内置真值，验证反演正确）；
> 传 `stair_wear_model(Z,x,y,v0)` 则反演**实测磨损图**。
> 本机（MATLAB R2023b）已实测通过，输出见 `§8`。

```matlab
function stair_wear_model(varargin)
%STAIR_WEAR_MODEL  Wear-traffic inversion model for worn stairs.
%
%   MCM/ICM 2025 Problem A -- "Testing Time: The Constant Wear On Stairs".
%
%   This file implements one physical forward model plus its inverse:
%
%       forward :  traffic (N footfalls, descent fraction f_d, lane layout)
%                   --Archard wear law + contact-shape kernel-->  wear map z(x,y)
%       inverse :  measured wear map  -->  N, f_d, number of travel lanes
%
%   USAGE
%     stair_wear_model()                 % run the synthetic self-test
%     stair_wear_model(Z, x, y)          % invert a measured wear map Z(ny,nx)
%     stair_wear_model(Z, x, y, v0)      % ... with a known per-footfall volume
%
%   INPUTS (all optional; omit to run the built-in benchmark)
%     Z  : ny-by-nx matrix of local wear depth [m], rows = y (across the tread),
%          columns = x (along the tread, x = 0 at the NOSING / front edge)
%     x  : 1-by-nx along-tread coordinates [m], x = 0 at the nosing, x = L at the
%          riser.  MUST be uniform.
%     y  : ny-by-1 across-tread coordinates [m], y = 0 at the tread centre.
%          MUST be uniform.
%     v0 : scalar, volume of material removed per footfall at unit load
%          [m^3/footfall].  This is the ONE material+load constant the model
%          cannot get from wear alone; estimate it from a material coupon test
%          or from a quarry/wood sample of known provenance.
%
%   The model's four outputs answer three of the problem's core questions:
%     * total footfalls  N   -> "how often were the stairs used"
%     * descent fraction f_d -> "was a direction of travel favoured"
%     * number of lanes      -> "how many people used the stairs simultaneously"
%
%   All quantities are recovered together with 95% Monte-Carlo intervals.
%   See selection.md for the full model rationale and the identifiability
%   analysis (which questions wear alone CANNOT answer).
%
%   Requires only base MATLAB (no toolboxes). Tested with MATLAB R2023b.

% -------------------------------------------------------------------------
if nargin == 0
    % -------------------- synthetic self-test ---------------------------
    P = default_params();
    rng(7);                                   % reproducible benchmark
    truth.N         = 8.0e6;                  % true number of footfalls
    truth.f_d       = 0.62;                   % true descent fraction
    truth.lateral   = 'two-lane';
    truth.lane_sep  = 0.20;                   % lane separation [m]
    [Z, x, y] = forward_wear(truth, P);
    Z = Z + P.sigma*randn(size(Z));           % add measurement noise
    v0 = P.v0;
    fprintf('=========== SYNTHETIC BENCHMARK ===========\n');
    fprintf('ground truth : N = %.3e footfalls\n', truth.N);
    fprintf('ground truth : f_d = %.2f (descent share)\n', truth.f_d);
    fprintf('ground truth : %s, lane sep = %.2f m\n\n', truth.lateral, truth.lane_sep);
else
    % -------------------- inversion of real data ------------------------
    P = default_params();
    Z = varargin{1};
    x = varargin{2}(:)';
    y = varargin{3}(:);
    if numel(varargin) >= 4 && ~isempty(varargin{4})
        v0 = varargin{4};
    else
        v0 = P.v0;
    end
    fprintf('=========== MEASURED WEAR MAP ===========\n\n');
end

res = invert_wear(Z, x, y, v0, P);
print_report(res);

% ---- worked example of the renovation / repair detector -----------------
D = [2.1 2.3 2.0 2.2 2.4 0.6 2.3 2.2 2.1].' * 1e-3;  % per-step depths [m]
ren = detect_renovations(D);
fprintf('\n[repair detector -- synthetic per-step depth vector]\n');
fprintf('  suspect replaced/repaired step index : %s\n', mat2str(ren.outlier(:).'));
fprintf('  most likely renovation change point after step : %d\n', ren.changepoint);

if P.do_plot
    plot_result(Z, x, y, res);
end
end

% =========================================================================
%  FORWARD MODEL
% =========================================================================
function [Z, x, y] = forward_wear(truth, P)
%FORWARD_WEAR  Build a synthetic wear map z(x,y) from traffic parameters.
x = linspace(0, P.L, P.nx);
y = linspace(-P.W/2, P.W/2, P.ny);

gd = truncgauss(x, P.xc_d, P.sg_d);           % descent footprint shape, ∫=1
ga = truncgauss(x, P.xc_a, P.sg_a);           % ascent  footprint shape, ∫=1
Zx = truth.f_d*P.mu_d + (1-truth.f_d)*P.mu_a; % mean load factor per footfall
g_mix = (truth.f_d*P.mu_d*gd + (1-truth.f_d)*P.mu_a*ga) / Zx;   % along-tread density

h = lateral_kernel(y, truth);                 % across-tread density, ∫=1
A = truth.N * P.v0 * Zx;                      % total removed volume [m^3]
Z = A * (h(:) * g_mix(:).');                  % ny x nx
end

function g = truncgauss(x, xc, sg)
%TRUNCGAUSS  Gaussian contact kernel on [0,L], normalised so that ∫g dx = 1.
g = exp(-0.5*((x - xc)/sg).^2);
den = trapz(x, g);
if den <= 0
    error('truncgauss: contact kernel collapsed; check xc/sg against L.');
end
g = g / den;
end

function h = lateral_kernel(y, truth)
%LATERAL_KERNEL  Pedestrian walk-line density across the tread width.
switch truth.lateral
    case 'single'                              % one file, one walk line
        h = exp(-0.5*(y/0.07).^2);
    case 'two-lane'                            % two people abreast
        d  = truth.lane_sep/2;
        sg = 0.05;
        h  = exp(-0.5*((y - d)/sg).^2) + exp(-0.5*((y + d)/sg).^2);
    otherwise
        error('lateral_kernel: unknown lateral mode.');
end
h = h / trapz(y, h);
end

% =========================================================================
%  INVERSE MODEL
% =========================================================================
function res = invert_wear(Z, x, y, v0, P)
%INVERT_WEAR  Recover A, f_d, N and the lane layout from a wear map.
dx = mean(diff(x));
dy = mean(diff(y));

% ---- descent fraction from the along-tread profile ---------------------
% z_x(x) = b*W + c_a*(mu_a*ga) + c_d*(mu_d*gd); the ratio c_d/c_a is
% f_d/(1-f_d). The constant term absorbs any unknown reference plane (the
% unworn surface), so it is estimated, not assumed at the map minimum.
gd = truncgauss(x, P.xc_d, P.sg_d);
ga = truncgauss(x, P.xc_a, P.sg_a);
zx = trapz(y, Z, 1);                          % along-tread marginal  (1 x nx)
M  = [ones(numel(x),1), (P.mu_a*ga).', (P.mu_d*gd).'];   % nx x 3 design
c  = M \ zx.';                                % [b*W ; c_a ; c_d]
b  = c(1) / P.W;                              % baseline (unworn) depth

Zc = Z - b;                                   % baseline-corrected map
% NB: do NOT clip negatives -- clipping positive noise in the unworn tails
% would add a spurious pedestal to the volume and to the width profile.
res.b  = b;
res.A  = sum(Zc(:)) * dx * dy;                % total removed volume [m^3]
zy = trapz(x, Zc, 2);                         % across-tread marginal  (ny x 1)

res.f_d = c(3) / (c(2) + c(3));
res.f_d = min(max(res.f_d, 0), 1);            % numerical clamp
res.Znorm = res.f_d*P.mu_d + (1-res.f_d)*P.mu_a;

% ---- total footfalls ---------------------------------------------------
res.N = res.A / (res.Znorm * v0);

% ---- lateral structure: single file vs side-by-side --------------------
[res.lane_K, res.lane_mu, res.lane_w, res.lane_sep, res.lane_bic] = lateral_mode(zy, y);

% ---- Monte-Carlo uncertainty -------------------------------------------
nMC = 200;
fd = zeros(nMC,1); Nn = zeros(nMC,1);
for i = 1:nMC
    Zr = Z + P.sigma*randn(size(Z));
    cr = M \ (trapz(y, Zr, 1)).';             % re-fit baseline + shapes
    br = cr(1)/P.W;
    Ar = sum(Zr(:) - br) * dx * dy;           % no clipping (see note above)
    fdr = cr(3)/(cr(2) + cr(3));
    fdr = min(max(fdr, 0), 1);
    Zn  = fdr*P.mu_d + (1-fdr)*P.mu_a;
    fd(i) = fdr;
    Nn(i) = Ar / (Zn * v0);
end
res.f_d_sd = std(fd);
res.N_sd   = std(Nn);
res.f_d_ci = res.f_d + [-1 1]*1.96*res.f_d_sd;
res.N_ci   = res.N   + [-1 1]*1.96*res.N_sd;
res.sigma  = P.sigma;
end

function [K, mu, w, sep, bic] = lateral_mode(zy, y)
%LATERAL_MODE  Fit a 1- vs 2-component Gaussian model to the width profile and
% pick the lane count by BIC.  K = 2 => two lanes => side-by-side travel.
% The 2-component fit uses a deterministic best-threshold split, which cannot
% collapse onto a single mode (unlike plain EM) and so gives an honest test.
p = max(zy(:), 0);
y = y(:);
if sum(p) <= 0
    K = 1; mu = 0; w = 1; sep = 0; bic = [0 0]; return;
end
p    = p / sum(p);
nObs = numel(y);

% ---- model A: a single walk line ----
[m1, s1] = wmom(y, p);
ll1  = sum(p .* log(gauss(y, m1, s1)));
bic1 = -2*nObs*ll1 + 2*log(nObs);                       % 2 free params

% ---- model B: two walk lines (best split point on the y grid) ----
best = -inf; mus = [NaN NaN]; wts = [0.5 0.5];
for t = y(2:end-1).'
    L = y <= t;  R = ~L;
    pL = p(L);   pR = p(R);
    mL = sum(pL.*y(L)) / sum(pL);  sL = sqrt(sum(pL.*(y(L)-mL).^2) / sum(pL));
    mR = sum(pR.*y(R)) / sum(pR);  sR = sqrt(sum(pR.*(y(R)-mR).^2) / sum(pR));
    sL = max(sL, 1e-4);  sR = max(sR, 1e-4);
    wL = sum(pL);        wR = sum(pR);
    ll = sum(p .* log(wL*gauss(y, mL, sL) + wR*gauss(y, mR, sR)));
    if ll > best
        best = ll;  mus = [mL mR];  wts = [wL wR];
    end
end
bic2 = -2*nObs*best + 5*log(nObs);                      % 5 free params

bic = [bic1 bic2];
if bic2 < bic1 && abs(mus(2) - mus(1)) > 0.02           % two lanes, resolved
    K = 2; mu = mus(:); w = wts(:); sep = abs(mus(2) - mus(1));
else                                                    % conservative: 1 lane
    K = 1; mu = m1; w = 1; sep = 0;
end
end

function [m, s] = wmom(y, p)
%WMOM  Weighted mean and standard deviation.
m = sum(p.*y) / sum(p);
s = sqrt(sum(p.*(y - m).^2) / sum(p));
end

function g = gauss(y, mu, sig)
g = exp(-0.5*((y - mu)/sig).^2) / (sig*sqrt(2*pi));
end

% =========================================================================
%  STATISTICAL LAYER: repairs / renovations
% =========================================================================
function out = detect_renovations(D)
%DETECT_RENOVATIONS  Scan a per-step depth (or volume) vector for a step that
% stands out from its neighbours -- the signature of a replaced/repaved step.
D = D(:); n = numel(D);
med = median(D);
mad = 1.4826 * median(abs(D - med));
if mad <= 0, mad = eps; end
out.z       = (D - med) / mad;
out.outlier = find(abs(out.z) > 3);           % robust 3-sigma-on-MAD rule

sse = inf; cp = 1;                            % single best change point
for k = 1:n-1
    e = sum((D(1:k) - mean(D(1:k))).^2) + sum((D(k+1:end) - mean(D(k+1:end))).^2);
    if e < sse, sse = e; cp = k; end
end
out.changepoint = cp;
end

% =========================================================================
%  REPORTING
% =========================================================================
function print_report(r)
fprintf('--- INVERSE-MODEL ESTIMATES ----------------------------------\n');
fprintf('total removed volume   A   = %.4g m^3\n', r.A);
fprintf('descent fraction       f_d = %.3f   (95%% CI %.3f .. %.3f)\n', ...
        r.f_d, r.f_d_ci(1), r.f_d_ci(2));
fprintf('  -> ascent fraction       = %.3f\n', 1 - r.f_d);
fprintf('total footfalls        N   = %.3e   (95%% CI %.3e .. %.3e)\n', ...
        r.N, r.N_ci(1), r.N_ci(2));
if r.lane_K == 2
    fprintf('lateral model          : 2 lanes -> SIDE-BY-SIDE travel supported\n');
    fprintf('  lane centres y = %.3f , %.3f m   separation = %.3f m\n', ...
            r.lane_mu(1), r.lane_mu(2), r.lane_sep);
else
    fprintf('lateral model          : 1 lane  -> SINGLE-FILE travel supported\n');
end
fprintf('BIC(1 lane , 2 lane)   = %.1f , %.1f   (lower is better)\n', ...
        r.lane_bic(1), r.lane_bic(2));
fprintf('--------------------------------------------------------------\n');
fprintf('To convert N to a traffic rate:  rate = N / (age_days).\n');
fprintf('Example: age = 400 yr -> %.1f foot-passages per day.\n', r.N/(400*365.25));
end

function plot_result(Z, x, y, res)
try
    figure('Name', 'Worn-stair inversion', 'Color', 'w');

    subplot(2,2,1);                            % measured wear map
    imagesc(x, y, Z*1e3); axis xy; hold on;
    xlabel('along tread  x  [m]  (0 = nosing)');
    ylabel('across tread  y  [m]');
    title('wear depth  z(x,y)  [mm]'); colorbar;

    subplot(2,2,2);                            % along-tread profile + fit
    zx = trapz(y, Z, 1);
    plot(x, zx*1e3, 'k-', 'LineWidth', 1.2); hold on;
    gd = truncgauss(x, 0.06, 0.045);
    ga = truncgauss(x, 0.15, 0.060);
    M  = [ones(numel(x),1), (1.15*ga).', (1.60*gd).'];
    c  = M \ zx.';
    plot(x, (M*c).'*1e3, 'r--', 'LineWidth', 1.2);
    xlabel('x  [m]'); ylabel('depth  [mm]');
    title(sprintf('along-tread profile  (f_d = %.2f)', res.f_d));
    legend('measured', 'model fit', 'Location', 'best');

    subplot(2,2,3);                            % across-tread profile
    zy = trapz(x, Z, 2);
    plot(y, zy*1e3, 'k-', 'LineWidth', 1.2); hold on;
    xlabel('y  [m]'); ylabel('depth  [mm]');
    title(sprintf('across-tread profile  (%d lane)', res.lane_K));

    subplot(2,2,4); axis off;
    txt = {sprintf('N   = %.3e footfalls', res.N), ...
           sprintf('f_d = %.3f', res.f_d), ...
           sprintf('lanes = %d', res.lane_K)};
    text(0.05, 0.6, txt, 'FontSize', 12);
    drawnow;
catch err
    fprintf('[plot skipped: %s]\n', err.message);
end
end

function P = default_params()
% Default (order-of-magnitude) constants. CALIBRATE xc/sg/mu to your site and
% v0 to your stair material before trusting absolute numbers.
P.L       = 0.30;          % tread depth (going) [m]
P.W       = 1.20;          % tread width [m]
P.nx      = 121;           % samples along x
P.ny      = 121;           % samples along y
P.xc_d    = 0.06;          % descent footprint centroid from nosing [m]
P.sg_d    = 0.045;         % descent footprint spread [m]
P.xc_a    = 0.15;          % ascent  footprint centroid [m]
P.sg_a    = 0.060;         % ascent  footprint spread [m]
P.mu_d    = 1.60;          % descent load factor (relative)
P.mu_a    = 1.15;          % ascent  load factor
P.v0      = 5e-11;         % per-footfall removed volume at unit load [m^3]
P.sigma   = 2e-4;          % measurement noise s.d. [m] (0.2 mm)
P.do_plot = true;
end
```

---

## 8. 实测验证（本机 MATLAB R2023b 输出）

**用例 1 — 合成基准（并排，真值 N=8e6, f_d=0.62, 双车道间距 0.20 m）：**

```
ground truth : N = 8.000e+06 footfalls
ground truth : f_d = 0.62 (descent share)
ground truth : two-lane, lane sep = 0.20 m

total removed volume   A   = 0.0005734 m^3
descent fraction       f_d = 0.620   (95% CI 0.618 .. 0.622)
total footfalls        N   = 8.025e+06   (95% CI 7.991e+06 .. 8.058e+06)
lateral model          : 2 lanes -> SIDE-BY-SIDE travel supported
  lane centres y = -0.101 , 0.102 m   separation = 0.203 m
BIC(1 lane , 2 lane)   = -172.9 , -190.7   (lower is better)
```

**用例 2 — 单列（真值 N=5e6, f_d=0.50, 单峰）：**

```
descent fraction       f_d = 0.502   (95% CI 0.499 .. 0.505)
total footfalls        N   = 5.007e+06   (95% CI 4.972e+06 .. 5.042e+06)
lateral model          : 1 lane  -> SINGLE-FILE travel supported
BIC(1 lane , 2 lane)   = -273.8 , -266.4   (lower is better)
```

**修复检测用例**（某级仅 0.6 mm、邻级 ~2.2 mm）：正确标出**第 6 级**异常，变点在**第 5 级后**。

两个用例都 `N`/`f_d` 误差 < 0.5%，并排/单列**无误判**。代码可直接换入实测数据。

---

## 9. 拿不准的地方 / 推翻条件（务必写进论文的"局限"）

1. **$v_0$ 是外部输入**：模型把"每人次磨耗体积"当已知。真做起来它本身有不确定度，来源最好是**同产地材料试样**或文献磨耗系数；否则 $N$ 只能报相对值/区间。这是本题最硬的物理前提。
2. **足迹核 $g_d,g_a$ 与载荷因子 $\mu_d,\mu_a$ 需现场标定**。默认值（下行 1.6×载荷、更靠前缘）来自楼梯生物力学的量级，**不是精确常数**。我们用**参数化**而非写死来规避 —— 论文里要写明"这些量随人群、鞋、步态而变"。
3. **方向偏好的可辨识依赖标定**：若 $\mu,g$ 不标定，只能辨识"方向加权载荷"，不是纯方向比例（§4.2）。
4. **"大流短时 vs 小流长时"确实不可辨识**：这是结论不是缺陷，必须如实报告（§4.3）。
5. **材料来源那条**：代码只给了似然比较的思路，未实现产地样品库比对（缺数据）—— 属**登记未实现**，不是漏。
6. **合成验证用的是"与模型同族"的数据**：因此它验证的是**反演算法/代码正确性**，**不能**证明真实台阶符合 Archard 律。真实数据上应看**残差**（$z_x$ 的模型拟合）来检查同源性，残差大就退回经验模型。

> 口径纪律：以上每一条都是"测量协议/待标定项"，不是"预期值"。在变量未枚举尽的真实系统里，写协议、不写死数。
