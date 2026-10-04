function out = regression(opts)
%REGRESSION  Multiple linear regression on synthetic data with KNOWN coefficients (parameter recovery).
%
%   M4 `mcm-model-select` 骨架 · prediction #7（回归预测）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `regression` 系列命中（带锚逐行）：
%     `linear regression`(:55 1 篇 · :90 1 篇 · :109 11 篇 · :267 2 篇)、
%     `logistic regression`(:73 2 篇 · :110 10 篇 · :232 2 篇 · :279 1 篇)、
%     `nonlinear regression`(:74 2 篇)、`ridge regression`(:175 1 篇)。
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*(linear|logistic|nonlinear|ridge) regression（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`。）
%   ★ **素材面**另有起点素材：`corpus/algorithms/src/RegressionAnalysis回归分析/`（含 `linear_regression.m` / `stepwise_regression.m` / `unlinear_regression.m`）—— 教辅级，**不作独立参照**。
%
%   独立参照（第 4 类：已知参数的合成数据 —— 参数可复原，不是"跟另一段代码对"）：
%     · 造  y = X*beta_true + 噪声（固定种子），用 `beta_hat = X \ y` 反估；
%     · 核对 `beta_hat` 是否回到 `beta_true`（有限样本下落在 ~2 个抽样标准误内）；
%     · 核对 `R^2` 与残差统计（残差均值≈0、残差标准差≈噪声 σ）。
%   ★ 逐项读数与真值对照见 `tests/skills/model-select/verify/regression.md`。
%
%   用法：
%     regression()             % 自检并打印读数
%     out = regression(opts)   % opts.beta opts.n opts.sigma opts.seed
%
%   返回 struct：beta_true, beta_hat, se, tstat, R2, R2adj, resid, sigma, n。

if nargin < 1 || isempty(opts); opts = struct(); end
beta_true = dflt(opts, 'beta',  [2.0; -3.0; 1.5; 0.5]);   % [截距; x1; x2; x3]
n     = dflt(opts, 'n',     200);
sigma = dflt(opts, 'sigma', 0.1);
seed  = dflt(opts, 'seed',  20261004);
beta_true = beta_true(:);
p = numel(beta_true);

rng(seed);
X = [ones(n, 1), randn(n, p - 1)];               % 设计矩阵（首列截距）
y = X * beta_true + sigma * randn(n, 1);         % 已知系数的合成因变量

beta_hat = X \ y;                                % 最小二乘
resid = y - X * beta_hat;
dof = n - p;
s2 = (resid.' * resid) / dof;                    % 残差方差（无偏）
Cov = s2 * inv(X.' * X);                         % 系数协方差
se = sqrt(diag(Cov));                            % 系数标准误
tstat = beta_hat ./ se;                          % t 统计量

SST = sum((y - mean(y)).^2);
SSE = sum(resid.^2);
R2 = 1 - SSE / SST;
R2adj = 1 - (1 - R2) * (n - 1) / dof;

out = struct('beta_true', beta_true, 'beta_hat', beta_hat, 'se', se, 'tstat', tstat, ...
             'resid', resid, 'sigma', sigma, 'sigma_hat', sqrt(s2), ...
             'R2', R2, 'R2adj', R2adj, 'n', n, 'p', p, ...
             'ae', abs(beta_hat - beta_true), 'startup_seed', seed);

fprintf('[regression] 合成数据：n = %d, p = %d, sigma_true = %.4g, seed = %d\n', n, p, sigma, seed);
fprintf('  beta_true = [%s]\n', num2str(beta_true.', '%.6g '));
fprintf('  beta_hat  = [%s]\n', num2str(beta_hat.', '%.8g '));
fprintf('  se        = [%s]\n', num2str(se.', '%.4g '));
fprintf('  |hat-true| = [%s]   (max = %.4g)\n', num2str(abs(beta_hat - beta_true).', '%.4g '), max(abs(beta_hat - beta_true)));
fprintf('  (hat-true)/se = [%s]  (应落在 ~ ±2)\n', num2str(((beta_hat - beta_true)./se).', '%.3f '));
fprintf('  sigma_hat = %.6g  (true %.6g)\n', sqrt(s2), sigma);
fprintf('  R^2 = %.8g   R^2_adj = %.8g   mean(resid) = %.4g\n', R2, R2adj, mean(resid));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
