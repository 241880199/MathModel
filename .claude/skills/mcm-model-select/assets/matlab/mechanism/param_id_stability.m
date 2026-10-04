function out = param_id_stability(opts)
%PARAM_ID_STABILITY  Parameter identification (synthetic data) + equilibrium stability.
%
%   M4 `mcm-model-select` 骨架 · mechanism #10（参数辨识 / 稳定性分析）。文件名全 ASCII（GC5）。
%
%   模型：logistic  dN/dt = r N (1 - N/K)。
%   独立参照（第 4 类：已知参数的合成数据 ⇒ 反演回来要对得上）：
%     · 由已知真值 (r, K) 生成合成数据（固定种子 rng(0) 加噪），
%       以最小二乘反演 (r̂, K̂)，应回到真值（无噪数据精确、加噪数据在噪水平内）。
%   附解析性质：平衡点稳定性由线性化的特征值给 ——
%     N* = 0 ⇒ f'(0) = +r > 0（不稳定）；N* = K ⇒ f'(K) = -r < 0（稳定）。
%
%   用法：
%     param_id_stability()             % 自检并打印读数
%     out = param_id_stability(opts)   % opts.r_true opts.K_true opts.N0 opts.noise_frac
%
%   返回 struct：r_hat_clean, K_hat_clean, r_hat_noisy, K_hat_noisy, eig0, eigK。

if nargin < 1 || isempty(opts); opts = struct(); end
r_true     = dflt(opts, 'r_true',     0.5);
K_true     = dflt(opts, 'K_true',     10);
N0         = dflt(opts, 'N0',         0.5);
noise_frac = dflt(opts, 'noise_frac', 0.02);

tt = (0:0.5:20)';
sim = @(r, K) logistic(r, K, N0, tt);

data_clean = sim(r_true, K_true);
rng(0);
data_noisy = data_clean + noise_frac * max(data_clean) * randn(size(data_clean));

p_clean = fit_params(sim, tt, data_clean);
p_noisy = fit_params(sim, tt, data_noisy);
r_hat_clean = exp(p_clean(1)); K_hat_clean = exp(p_clean(2));
r_hat_noisy = exp(p_noisy(1)); K_hat_noisy = exp(p_noisy(2));

% 平衡点稳定性（解析线性化特征值）
eig0 = r_true * (1 - 2*0   / K_true);   %  = +r_true
eigK = r_true * (1 - 2*K_true / K_true); % = -r_true

out = struct('r_true', r_true, 'K_true', K_true, ...
             'r_hat_clean', r_hat_clean, 'K_hat_clean', K_hat_clean, ...
             'r_hat_noisy', r_hat_noisy, 'K_hat_noisy', K_hat_noisy, ...
             'eig0', eig0, 'eigK', eigK);

fprintf('[param_id_stability] logistic dN/dt = r N (1 - N/K)\n');
fprintf('  true (r, K)                   = (%.12g, %.12g)\n', r_true, K_true);
fprintf('  recovered (clean data)        = (%.12g, %.12g)\n', r_hat_clean, K_hat_clean);
fprintf('  rel err (clean)               = (%.3e, %.3e)\n', ...
        abs(r_hat_clean - r_true)/r_true, abs(K_hat_clean - K_true)/K_true);
fprintf('  recovered (%.2g%% noise)        = (%.12g, %.12g)\n', 100*noise_frac, r_hat_noisy, K_hat_noisy);
fprintf('  rel err (noisy)               = (%.3e, %.3e)\n', ...
        abs(r_hat_noisy - r_true)/r_true, abs(K_hat_noisy - K_true)/K_true);
fprintf('  eigenvalue at N*=0  f''(0) = +r = %.6g  (unstable)\n', eig0);
fprintf('  eigenvalue at N*=K  f''(K) = -r = %.6g  (stable)\n', eigK);
end

% ------------------------------------------------------------------------
function N = logistic(r, K, N0, tt)
[~, N] = ode45(@(t, n) r*n*(1 - n/K), tt, N0);
end

function p = fit_params(sim, tt, data)
obj = @(p) sum((sim(exp(p(1)), exp(p(2))) - data).^2);
p0  = [log(0.3), log(5)];
p   = fminsearch(obj, p0, optimset('TolX', 1e-12, 'TolFun', 1e-14, ...
                                   'MaxFunEvals', 20000, 'MaxIter', 20000));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
