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
