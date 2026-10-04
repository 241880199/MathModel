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
