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
