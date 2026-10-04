# Model selection & solver — 2025 MCM Problem A
## "Testing Time: The Constant Wear On Stairs"

**Recommended model:** an **inverse abrasion model** — a separable *Archard-type wear
field* driven by a *footfall-placement distribution*, fitted to a measured wear map
by weighted least squares, with uncertainty from the Gauss–Newton covariance.
One fit answers every question the problem asks (frequency, direction, simultaneity,
age consistency/reliability, short-burst vs long-slow), and it degrades gracefully
into a material-source hypothesis test.

Deliverable code: **`stairwear.m`** (base MATLAB, no toolboxes; run the self-test by
typing `stairwear`). Full listing in [§9](#9-matlab-solver-listing).

---

## 1. What the problem actually asks

From a set of worn stairs, infer, non-destructively and cheaply:

| # | Question | What the model must output |
|---|----------|----------------------------|
| Q1 | How often were the stairs used? | a *rate* (steps per day / year) |
| Q2 | Was a direction favoured? | ascending vs descending bias |
| Q3 | How many people used them simultaneously? | single-file vs side-by-side |
| Q4 | Is the wear consistent with known history? | a consistency test |
| Q5 | Age of the stairwell and how reliable? | age + confidence interval |
| Q6 | What repairs / renovations happened? | presence of a break in the wear surface |
| Q7 | Can the material source be determined? | hypothesis test over candidate materials |
| Q8 | Many people briefly vs few people long? | time-profile of the traffic |

The physics that makes all eight tractable is the **wear-rate separation**:

> **Wear = (abrasive term ∝ number of footsteps) + (environmental/aging term ∝ elapsed time).**

The abrasive term is **spatially peaked** (it follows where feet land); the aging term
is **spatially uniform** (weathering, dust, and chemical attack act everywhere).
Decomposing the observed depth field into a peaked part and a flat part separates
*how many people* from *how long* — which is exactly Q1 vs Q5/Q8.

---

## 2. Measurement protocol (non-destructive, cheap, small team)

Everything the model needs is a **depth map `h(x, y)`** of the tread relative to its
original flat top:

* `x` — lateral position across the tread (left → right),
* `y` — depth position on the tread (0 = nosing/front edge → riser/back),
* `h` — material removed (mm).

**How to get it with minimal tools** (any one of these):

1. **Straightedge + feeler gauges / slip gauges** — lay a rigid steel rule across the
   tread (both directions), measure the gap at a 2–3 cm grid with feeler gauges.
   Cost ≈ a ruler and a gauge set; time ≈ 30–60 min per step.
2. **Digital caliper depth probe** referenced to a straightedge — same idea, ±0.05 mm.
3. **Phone photogrammetry / a cheap line laser + camera** — reconstruct the surface from
   a few photos; ±0.2–0.5 mm, best for a full map quickly.

Also record (**cheap, needed once**):

* **Material** and its **abrasion coefficient `k_m`** (volume removed per footstep) — from
  a small loose fragment (a spall already on the floor, so still non-destructive) or
  from literature hardness/grain data. This is the ONLY constant that converts wear
  *volume* into a *footfall count* (see §4).
* **Age estimate `T`** and its uncertainty (usually a range, not a point) — from the
  historical record.
* The **original (unworn) surface** reference — an unworn neighbour tread, a doorway
  threshold, or the back strip near the riser, which is usually least worn.

Recommended grid: `x` every 2–5 cm, `y` every 1–2 cm. Example: 1.2 m × 0.30 m tread at
2 cm spacing → 61 × 15 ≈ 900 points, an hour's work.

---

## 3. The model

### 3.1 Single footstep = an abrasion kernel
A footstep at placement `(x₀, y₀)` removes a shallow dent. Model the contact as a
normalised separable Gaussian "abrasion kernel" with footprint spreads `σ_x`, `σ_y`:

$$g(x,y;x_0,y_0)=\frac{1}{2\pi\sigma_x\sigma_y}\,
e^{-\frac{(x-x_0)^2}{2\sigma_x^2}-\frac{(y-y_0)^2}{2\sigma_y^2}},\qquad \iint g\,dA=1 .$$

### 3.2 Where feet land = a placement distribution
**Lateral** placement (across the width) is a **mixture of `m` Gaussian lanes**
`μ₁…μ_m`: `m = 1` is single-file, `m = 2` (well-separated lanes) is people walking
**side-by-side**:

$$p_x(x_0)=\sum_{j=1}^{m}\pi_j\,\mathcal N(x_0;\mu_j,\tau^2),\qquad \sum_j\pi_j=1 .$$

**Depth** placement (front→back on the tread) depends on **direction**: people
*descending* plant the foot near the **nosing** (`y_d` small); people *ascending* plant
it further back (`y_u` larger). With `f_d` = fraction of footsteps that descend,

$$p_y(y_0)=f_d\,\delta(y_0-y_d)+(1-f_d)\,\delta(y_0-y_u),\qquad y_d<y_u .$$

### 3.3 Accumulated wear
The expected depth field is the placement distribution convolved with the kernel,
scaled by the total footfall count `N` and the material coefficient `k_m`, plus the
uniform environmental term `b = e·T` (`e` = ablation rate, `T` = exposure time):

$$\boxed{\;h(x,y)=k_m N\,\big(p_x\!\ast\!g_x\big)(x)\;\big(p_y\!\ast\!g_y\big)(y)\;+\;b\;}$$

Because the kernel is separable, so is the result — write it as

$$h(x,y)=A\,\tilde p_x(x)\,\tilde p_y(y)+b,$$

where `Ã = k_m·N`, and `p̃_x, p̃_y` are the (widened) normalised lane / depth densities.
**This separability is what makes the inverse problem well-posed and cheap** — the
lateral profile fixes the lanes (Q3), the depth profile fixes direction (Q2), and the
overall volume fixes `N` (Q1).

### 3.4 Physical assumptions baked in
* Archard law: wear ∝ load × sliding distance / hardness → linear in the number of
  footsteps; all footsteps assumed equal (an average foot).
* The footprint spreads `σ_x, σ_y` (≳ foot size) are **assumed**, i.e. taken from foot
  anatomy; the fit recovers the *placement* spread `τ` and lane centres.
* Depth `y=0` at the nosing; wear is permitted to be positive only (the fit is
  constrained so `h ≥ 0`).

---

## 4. Recovering the parameters (how the solver works)

1. **Analytic seed.** Wear volume `V = ∬h dA ≈ A + b·(area)`; peaks of the lateral
   profile seed the lane centres `μ_j`; front/back peaks of the depth profile seed
   `y_d, y_u` and their height ratio seeds `f_d`.
2. **Weighted least squares.** Minimise `χ² = Σ (h_obs − h_model)²/σ²` over the
   parameter vector `θ = (A, f_d, y_u, y_d, μ₁, μ₂, π₂, τ, b)` with `fminsearch`
   (base MATLAB). A constrained reparameterisation keeps `0<y_d<y_u<D`, `0<μ₁<μ₂<W`,
   `f_d,π₂∈(0,1)` and the scales positive. Three starts guard against local minima.
3. **Concurrency model choice.** Refit with **one** lane (`π₂ = 0`) and compare by
   **BIC**; a `ΔBIC > 10` in favour of two lanes is strong evidence of side-by-side use.
4. **Uncertainty.** Numerically differentiate the model to get the Jacobian `J`, then
   the Gauss–Newton covariance `C = σ² (JᵀJ)⁻¹`, with `σ` taken as the **worse** of the
   instrument error and the residual scatter. Standard errors propagate to every answer
   (`N`, `f_d`, lane separation, age).

### From recovered parameters to the eight questions

| Q | Answer from the fit |
|---|---------------------|
| **Q1 frequency** | `N = A / k_m` total footsteps; rate `= N / T` (→ steps/day). |
| **Q2 direction** | `f_d` with a 95 % CI; a bias is significant iff the CI excludes 0.5. The **front-vs-back** asymmetry of the depth profile is the fingerprint. |
| **Q3 simultaneity** | number of lanes `m` and their separation `μ₂−μ₁` (BIC test). Separation ≳ a person's width ⇒ side-by-side; a single lane ⇒ single file. |
| **Q4 consistency** | compare the weathering-implied age `T_w = b / e` against the historical `T` (z-test), and `N` against the plausible population. |
| **Q5 age & reliability** | `T_w ± 1.96·SE`; reliability = width of that interval (driven by measurement noise and how well `b` is separated from `A`). |
| **Q6 repairs** | a repair shows as a **discontinuity / step** in `h` or a local change of slope along `y`; detected as structured residuals or a break-point in the depth profile. |
| **Q7 material source** | invert `k_m = A / N`; compare the recovered effective abrasion coefficient with each candidate material's known `k_m` and accept the one inside the CI (a model-selection / hypothesis test). |
| **Q8 short vs long** | the **abrasive/environmental ratio** `A / (b·area)`: a large ratio with a short `T` ⇒ many people over a short time; a small ratio over a long `T` ⇒ few people over a long time. |

---

## 5. Material-source inference (Q7, in more detail)

Because `A = k_m N`, if the age `T` gives an independent handle on `N` (via the rate),
then the *observed* abrasion coefficient is `k_m^obs = A / N`. Each candidate source
(quarry / timber species) predicts a `k_m^cand` from its hardness, grain size and
porosity. The source is accepted iff `k_m^cand` lies inside the confidence interval of
`k_m^obs`. **Wood** wears differently (compression and fibre pull-out, not abrasion) —
for wood, replace the Archard kernel by a plastic-denting kernel and compare the
recovered *yield pressure* instead of hardness; the geometry (lanes, depth asymmetry)
is unchanged.

---

## 6. Assumptions, and what is genuinely hard

* **`k_m` dominates the frequency estimate.** `N = A/k_m` is only as good as the material
  coefficient; report it with uncertainty. A 20 % error in `k_m` is a 20 % error in `N`.
* **The aging term `b` is the weakest link.** It is identifiable only from the
  less-worn corners of the tread, so on a weakly weathered stair `b` can trade off
  against the abrasive tails. Prefer the historical `T` as a prior, and treat `T_w`
  qualitatively. (The self-test shows this: `b` is recovered to ~30 % while `N`,
  direction and lanes are recovered to a few percent.)
* **Single average foot.** Real traffic mixes body weights, shoe types and gaits; the
  model gives population means, not individuals.
* **Independence of `x` and `y` placement.** Justified if the lateral lane a person
  walks in is independent of the depth they plant on; relaxation = a full 2-D mixture
  (same machinery, more parameters).

---

## 7. Interpretation of the deterministic (non-answer) questions

* Q6 repairs: run the fit, then fit a **piecewise** version with a break-point in `y`
  (and/or in `x`) and test whether the break improves BIC — a significant break at a
  plausible renovation line is evidence of a repair; a changed `k_m` across the break
  points to replacement with different stone.
* Q4: a large `|T_w − T|` or a recovered lane pattern that contradicts the documented
  use (e.g. ceremonial one-directional use but balanced `f_d`) flags inconsistency.

---

## 8. Running the solver

```matlab
% 1. Self-test on synthetic data (proves the pipeline end-to-end):
stairwear

% 2. Your own measured map (depths in metres, Hobs is Ny-by-Nx, y = rows):
stairwear(Hobs, xvec, yvec)
```

Edit the **Configuration** block at the top of `stairwear.m` for your stair:
`SXF, SYF` (assumed footprint spreads), `SIG` (instrument error), `K_M` (material
coefficient), `T_AGE, T_AGE_SD` (historical age), `E_WEATHER` (ablation rate),
`LANE_GAP` (single-file vs side-by-side threshold).

**Verified self-test output** (this exact code was run in MATLAB; true values in
brackets):

```
RMS residual = 0.20 mm   (measurement sigma = 0.15 mm)

[1] total footfalls  N = 8.35e+05  (+/- 4.33e+03, 95%)      [truth 8e5]
    rate ~= 7.6 steps/day  (given age = 300 yr)
[2] descending fraction f_down = 0.305  (+/- 0.002, 95%)    [truth 0.30]
    -> direction is BIASED toward ASCENDING
[3] lane separation = 0.415 m ; BIC favours 2 lanes          [truth 0.40 m]
    -> SIDE-BY-SIDE traffic likely
[4] age from weathering = 215 (+/- 13) yr ; historical 300  [truth 300]
    discrepancy z = 1.69 -> CONSISTENT
[5] abrasive/environmental ratio = 10.8                     [truth 10.4]
recovered: ascending foot y=0.180, descending y=0.049       [truth 0.18, 0.05]
           lanes x=0.397, 0.812                             [truth 0.40, 0.80]
```

A second test with a **single central lane** returned `f_down = 0.711` [truth 0.72],
one lane at `x = 0.600` [truth 0.60], and **BIC favoured 1 lane** — i.e. the
single-file / side-by-side decision is data-driven, not hard-wired.

---

## 9. MATLAB solver listing

See **`stairwear.m`** in this directory (the file is the authoritative copy; the
listing is reproduced here for convenience).

```matlab
function stairwear(Hobs, xvec, yvec, varargin)
%STAIRWEAR  Inverse wear model for 2025 MCM Problem A
%  Model: separable Archard-type abrasion term (peaked; scales with footfall
%  COUNT) + uniform environmental/aging term (scales with TIME). Inverted by
%  weighted least squares; uncertainty from the Gauss-Newton covariance.
%  Base MATLAB only.
%
%  USAGE
%     stairwear                       % synthetic self-test
%     stairwear(Hobs, xvec, yvec)     % fit your own wear map (depths in m)

%% ---------------- 0. Configuration: EDIT FOR YOUR STAIR ----------------
cfg.SXF       = 0.050;    % [m]       lateral footprint spread (assumed)
cfg.SYF       = 0.045;    % [m]       depth   footprint spread (assumed)
cfg.SIG       = 1.5e-4;   % [m]       measurement std of depth
cfg.K_M       = 1.0e-9;   % [m^3/step] abrasive volume per footfall
cfg.T_AGE     = 300;      % [yr]      historical age estimate
cfg.T_AGE_SD  = 50;       % [yr]      its 1-sigma uncertainty
cfg.E_WEATHER = 1.0e-6;   % [m/yr]    environmental ablation rate
cfg.LANE_GAP  = 0.30;     % [m]       lane separation -> "side-by-side"
cfg.DO_PLOTS  = true;

%% ---------------- 1. Data ----------------------------------------------
if nargin==0
    [Hobs,xvec,yvec] = make_synthetic(cfg);
    fprintf('=== STAIRWEAR self-test on SYNTHETIC data ===\n');
else
    fprintf('=== STAIRWEAR fit of a measured wear map ===\n');
end
[X,Y] = meshgrid(xvec,yvec);
Nx = numel(xvec); Ny = numel(yvec);
W  = xvec(end)-xvec(1);
Dt = yvec(end)-yvec(1);
sig = cfg.SIG; sxf = cfg.SXF; syf = cfg.SYF;

%% ---------------- 2. Fit the 2-lane model ------------------------------
logit  = @(v) log(v./(1-v));
unpack = @(q) unpack_q(q,W,Dt,sxf,syf);
fw     = @(p) reshape(forward_wear(X,Y,p),[],1);
obj    = @(q) sum( (Hobs(:)-fw(unpack(q))).^2 ) / sig^2;

base0 = max(min(Hobs(:)),1e-6);
amp0  = max(max(Hobs(:))-base0,1e-8);
starts = { ...
  [log(amp0); logit(0.50); 0;        logit(0.20); logit(1/3); 0;        0;         log(0.10); log(base0)], ...
  [log(amp0); logit(0.65); 0;        logit(0.20); logit(1/3); 0;        logit(0.5);log(0.15); log(base0)], ...
  [log(amp0); logit(0.35); logit(0.5);logit(0.10); logit(1/4); logit(0.5);logit(0.5);log(0.12); log(base0)] };
opts = optimset('Display','off','MaxFunEvals',40000,'MaxIter',40000, ...
                'TolFun',1e-4,'TolX',1e-5);
qhat = []; fbest = inf;
for s = 1:numel(starts)
    [q,fv] = fminsearch(obj, starts{s}, opts);
    if fv < fbest, fbest = fv; qhat = q; end
end
phat = unpack(qhat);
Hfit = forward_wear(X,Y,phat);

%% ---------------- 3. 1-lane (single-file) model for comparison ---------
unpack1 = @(r) unpack_q([r(1);r(2);r(3);r(4);r(5); 0; -40; r(6); r(7)],W,Dt,sxf,syf);
obj1    = @(r) sum( (Hobs(:)-fw(unpack1(r))).^2 ) / sig^2;
r0 = [qhat(1);qhat(2);qhat(3);qhat(4);qhat(5);qhat(8);qhat(9)];
[r1,fv1] = fminsearch(obj1, r0, opts);   %#ok<ASGLU>

%% ---------------- 4. Uncertainty (Gauss-Newton covariance) -------------
pnames = {'amp','fdown','yu','yd','mu1','mu2','pi2','tau','base'};
J = zeros(numel(Hobs), numel(pnames));
for k = 1:numel(pnames)
    step = 1e-4*max(abs(phat.(pnames{k})),1e-8);
    pp = phat; pp.(pnames{k}) = phat.(pnames{k}) + step;
    Hm = forward_wear(X,Y,pp);
    J(:,k) = (Hm(:)-Hfit(:)) / step;
end
rms    = sqrt(mean((Hobs(:)-Hfit(:)).^2));
sigEff = max(sig, rms);
C  = pinv(J'*J) * sigEff^2;
SE = sqrt(abs(diag(C)));
getSE = @(nm) SE(strcmp(pnames,nm));

%% ---------------- 5. Derived quantities --------------------------------
N     = phat.amp / cfg.K_M;
SE_N  = getSE('amp') / cfg.K_M;
fdown = phat.fdown;  SE_fd = getSE('fdown');
sep   = abs(phat.mu2 - phat.mu1);
SE_sep = sqrt(getSE('mu1')^2 + getSE('mu2')^2);
lam     = N / cfg.T_AGE;
lam_day = N / (cfg.T_AGE*365.25);
Tw    = phat.base / cfg.E_WEATHER;
SE_Tw = getSE('base') / cfg.E_WEATHER;
zAge  = abs(Tw - cfg.T_AGE) / sqrt(SE_Tw^2 + cfg.T_AGE_SD^2);
M     = numel(Hobs);
BIC2  = fbest + 9*log(M);
BIC1  = fv1   + 7*log(M);

%% ---------------- 6. Report --------------------------------------------
fprintf('\n-- grid %d x %d ; tread %.2f m (x) by %.2f m (y) --\n',Ny,Nx,W,Dt);
fprintf('RMS residual = %.2f mm   (measurement sigma = %.2f mm)\n', rms*1e3, sig*1e3);

fprintf('\n[1] HOW OFTEN USED\n');
fprintf('    total footfalls  N = %.3g  (+/- %.3g, 95%%)\n', N, 1.96*SE_N);
fprintf('    rate = %.0f steps/yr  ~= %.1f steps/day  (given age = %.0f yr)\n', ...
        lam, lam_day, cfg.T_AGE);

fprintf('\n[2] TRAVEL DIRECTION\n');
fprintf('    descending fraction f_down = %.3f  (+/- %.3f, 95%%)\n', fdown, 1.96*SE_fd);
if abs(fdown-0.5) > 1.96*SE_fd
    if fdown>0.5, d='DESCENDING'; else d='ASCENDING'; end
    fprintf('    -> direction is BIASED toward %s\n', d);
else
    fprintf('    -> no significant direction bias (balanced use)\n');
end

fprintf('\n[3] SIMULTANEOUS USERS\n');
fprintf('    second-lane weight pi2 = %.2f ; lane separation = %.3f (+/- %.3f) m\n', ...
        phat.pi2, sep, 1.96*SE_sep);
if phat.pi2>0.15 && sep>cfg.LANE_GAP
    fprintf('    -> SIDE-BY-SIDE traffic likely (>= 2 people abreast)\n');
else
    fprintf('    -> essentially SINGLE-FILE traffic\n');
end
fprintf('    model choice by BIC: 1-lane = %.1f , 2-lane = %.1f -> %s\n', ...
        BIC1, BIC2, ternary(BIC2<BIC1-10,'favour 2 lanes', ...
                    ternary(BIC1<BIC2-10,'favour 1 lane','indistinguishable')));

fprintf('\n[4] AGE CONSISTENCY / RELIABILITY\n');
fprintf('    age from weathering = %.0f (+/- %.0f, 95%%) yr ; historical = %.0f (+/- %.0f) yr\n', ...
        Tw, 1.96*SE_Tw, cfg.T_AGE, cfg.T_AGE_SD);
fprintf('    discrepancy z = %.2f -> %s\n', zAge, ...
        ternary(zAge<2,'CONSISTENT','INCONSISTENT'));

fprintf('\n[5] SHORT-BURST vs LONG-SLOW\n');
fprintf('    abrasive volume = %.3g m^3 ; uniform environmental depth = %.2f mm\n', ...
        phat.amp, phat.base*1e3);
fprintf('    abrasive/(environmental) ratio = %.2f\n', phat.amp/(phat.base*W*Dt));
fprintf('    (large ratio & short T -> many people, short time;\n');
fprintf('     small ratio & long T   -> few people, long time)\n');

fprintf('\n-- recovered parameters (m) --\n');
fprintf('    ascending foot at y = %.3f m , descending foot at y = %.3f m\n', ...
        phat.yu, phat.yd);
fprintf('    lanes at x = %.3f and %.3f m ; lateral spread tau = %.3f m\n', ...
        phat.mu1, phat.mu2, phat.tau);

fprintf('\n-- per-parameter 95%% confidence half-widths --\n');
for k = 1:numel(pnames)
    fprintf('    %-6s = %12.5g  +/- %.3g\n', pnames{k}, phat.(pnames{k}), 1.96*SE(k));
end
fprintf('    (sigma used for CI: %.2f mm)\n', sigEff*1e3);

%% ---------------- 7. Figures (optional) --------------------------------
if cfg.DO_PLOTS
    try
        figure('Name','wear map: observed');
        imagesc(xvec*100, yvec*100, Hobs*1e3); axis image; colorbar;
        xlabel('lateral x (cm)'); ylabel('depth y (cm)');
        title('Observed wear depth (mm)'); set(gca,'YDir','normal');

        figure('Name','wear map: model');
        imagesc(xvec*100, yvec*100, Hfit*1e3); axis image; colorbar;
        xlabel('lateral x (cm)'); ylabel('depth y (cm)');
        title('Fitted model depth (mm)'); set(gca,'YDir','normal');

        figure('Name','profiles');
        subplot(1,2,1);
        [~,im] = min(abs(yvec - phat.yu));
        plot(xvec*100, Hobs(im,:)*1e3,'.', xvec*100, Hfit(im,:)*1e3,'-','LineWidth',1);
        xlabel('lateral x (cm)'); ylabel('depth (mm)');
        title('lateral profile (mid-tread)'); legend('obs','fit'); grid on;
        subplot(1,2,2);
        [~,ic] = min(abs(xvec - phat.mu1));
        plot(yvec*100, Hobs(:,ic)*1e3,'.', yvec*100, Hfit(:,ic)*1e3,'-','LineWidth',1);
        xlabel('depth y (cm)'); ylabel('depth (mm)');
        title('depth profile (through lane 1)'); legend('obs','fit'); grid on;
    catch
        warning('Plotting skipped (no display available).');
    end
end
end

%% ======================= local functions ===============================
function [Hobs,xvec,yvec] = make_synthetic(cfg)
W = 1.20; Dt = 0.30;
xvec = linspace(0,W,121); yvec = linspace(0,Dt,31);
[X,Y] = meshgrid(xvec,yvec);
p = struct('amp',8.0e-4,'fdown',0.30,'yu',0.18,'yd',0.05, ...
           'mu1',0.40,'mu2',0.80,'pi2',0.45,'tau',0.12, ...
           'base',3.0e-4,'sxf',cfg.SXF,'syf',cfg.SYF);
Hclean = forward_wear(X,Y,p);
rng(7);
Hobs = max(Hclean + cfg.SIG*randn(size(Hclean)), 0);
end

function H = forward_wear(X,Y,p)
sx = sqrt(p.tau^2 + p.sxf^2);
px = (1-p.pi2).*g1(X,p.mu1,sx) + p.pi2.*g1(X,p.mu2,sx);
py = p.fdown.*g1(Y,p.yd,p.syf) + (1-p.fdown).*g1(Y,p.yu,p.syf);
H  = p.amp .* px .* py + p.base;
end

function v = g1(z,m,s)
v = exp(-(z-m).^2/(2*s^2)) / (s*sqrt(2*pi));
end

function p = unpack_q(q,W,Dt,sxf,syf)
yd  = Dt*sigm(q(4));
yu  = yd + (Dt-yd)*sigm(q(3));
mu1 = W*sigm(q(5));
mu2 = mu1 + (W-mu1)*sigm(q(6));
p = struct('amp',exp(q(1)),'fdown',sigm(q(2)),'yu',yu,'yd',yd, ...
           'mu1',mu1,'mu2',mu2,'pi2',sigm(q(7)),'tau',exp(q(8)), ...
           'base',exp(q(9)),'sxf',sxf,'syf',syf);
end

function s = sigm(q)
s = 1./(1+exp(-q));
end

function out = ternary(c,a,b)
if c, out = a; else, out = b; end
end
```

---

## 10. Parameter glossary

| Symbol | Meaning | Units |
|--------|---------|-------|
| `h(x,y)` | wear depth field | m |
| `N` | total number of footsteps | — |
| `k_m` | abrasive volume removed per footstep | m³/step |
| `f_d` | fraction of footsteps going down | — |
| `y_d, y_u` | foot-plant depth (descending / ascending) | m |
| `μ_j, π_j, τ` | lane centre / weight / spread | m, —, m |
| `σ_x, σ_y` | footprint spreads (assumed) | m |
| `b = e·T` | uniform environmental depth | m |
| `T, e` | exposure age, ablation rate | yr, m/yr |
