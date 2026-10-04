function stairwear(Hobs, xvec, yvec, varargin)
%STAIRWEAR  Inverse wear model for 2025 MCM Problem A
%           ("Testing Time: The Constant Wear On Stairs").
%
%  Model: a separable Archard-type abrasion term (spatially peaked; scales
%  with the footfall COUNT) plus a uniform environmental/aging term (scales
%  with EXPOSURE TIME).  Inverted by weighted least squares; uncertainty from
%  the Gauss-Newton covariance.  The same fit answers:
%     [1] how often the stair was used      (total footfalls N, rate)
%     [2] favoured travel direction         (descending fraction f_down)
%     [3] how many people at once           (# lateral wear lanes)
%     [4] is the wear consistent / age & reliability (weathering time vs history)
%     [5] short-burst vs long-slow traffic  (abrasive/weathering ratio)
%
%  USAGE
%     stairwear                       % self-contained synthetic self-test
%     stairwear(Hobs, xvec, yvec)     % fit your own measured wear map
%        Hobs : Ny-by-Nx matrix of wear DEPTH in metres (>=0)
%        xvec : 1-by-Nx lateral coordinates (m)   [left -> right]
%        yvec : Ny-by-1 depth  coordinates (m)    [nosing(0) -> riser]
%
%  Base MATLAB only (no toolboxes).  See selection.md for the protocol and
%  the equations this code implements.

%% ---------------- 0. Configuration: EDIT FOR YOUR STAIR ----------------
cfg.SXF       = 0.050;    % [m]       lateral footprint spread (assumed)
cfg.SYF       = 0.045;    % [m]       depth   footprint spread (assumed)
cfg.SIG       = 1.5e-4;   % [m]       measurement std of depth
cfg.K_M       = 1.0e-9;   % [m^3/step] abrasive volume per footfall (lab/lit)
cfg.T_AGE     = 300;      % [yr]      historical age estimate
cfg.T_AGE_SD  = 50;       % [yr]      its 1-sigma uncertainty
cfg.E_WEATHER = 1.0e-6;   % [m/yr]    environmental ablation rate (uniform term)
cfg.LANE_GAP  = 0.30;     % [m]       lane separation -> "side-by-side" if above
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
rms   = sqrt(mean((Hobs(:)-Hfit(:)).^2));
sigEff = max(sig, rms);              % honest: trust the WORSE of instrument/ residual
C  = pinv(J'*J) * sigEff^2;
SE = sqrt(abs(diag(C)));
getSE = @(nm) SE(strcmp(pnames,nm));

%% ---------------- 5. Derived quantities --------------------------------
N     = phat.amp / cfg.K_M;                 % total footfalls
SE_N  = getSE('amp') / cfg.K_M;
fdown = phat.fdown;  SE_fd = getSE('fdown');
sep   = abs(phat.mu2 - phat.mu1);
SE_sep = sqrt(getSE('mu1')^2 + getSE('mu2')^2);   % (ignores mu1-mu2 corr.)
lam     = N / cfg.T_AGE;                     % footfalls / year
lam_day = N / (cfg.T_AGE*365.25);            % footfalls / day
Tw    = phat.base / cfg.E_WEATHER;           % age implied by weathering
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
% Synthetic worn tread used by the self-test (replace with real data).
W = 1.20; Dt = 0.30;
xvec = linspace(0,W,121); yvec = linspace(0,Dt,31);
[X,Y] = meshgrid(xvec,yvec);
p = struct('amp',8.0e-4,'fdown',0.30,'yu',0.18,'yd',0.05, ...
           'mu1',0.40,'mu2',0.80,'pi2',0.45,'tau',0.12, ...
           'base',3.0e-4,'sxf',cfg.SXF,'syf',cfg.SYF);
Hclean = forward_wear(X,Y,p);
rng(7);                                   % reproducible noise
Hobs = max(Hclean + cfg.SIG*randn(size(Hclean)), 0);
end

function H = forward_wear(X,Y,p)
% Separable forward model:  h(x,y) = amp*px(x)*py(y) + base
%   px : lateral placement mix of 2 Gaussians, widened by footprint spread
%   py : depth  placement mix of up/down deltas, widened by footprint spread
sx = sqrt(p.tau^2 + p.sxf^2);
px = (1-p.pi2).*g1(X,p.mu1,sx) + p.pi2.*g1(X,p.mu2,sx);
py = p.fdown.*g1(Y,p.yd,p.syf) + (1-p.fdown).*g1(Y,p.yu,p.syf);
H  = p.amp .* px .* py + p.base;
end

function v = g1(z,m,s)
% normalised 1-D Gaussian density
v = exp(-(z-m).^2/(2*s^2)) / (s*sqrt(2*pi));
end

function p = unpack_q(q,W,Dt,sxf,syf)
% constrained reparameterisation:  yu>yd in (0,Dt), mu2>mu1 in (0,W),
% fdown,pi2 in (0,1), amp,tau,base > 0
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
