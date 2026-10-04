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
