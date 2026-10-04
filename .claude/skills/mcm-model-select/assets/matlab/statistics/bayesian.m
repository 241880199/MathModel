function out = bayesian(opts)
%BAYESIAN  Bayesian inference: normal-normal conjugate closed form + MCMC (two paths).
%
%   M4 `mcm-model-select` 骨架 · statistics #7（贝叶斯推断：先验/后验 · MCMC · 可信区间）。
%   文件名全 ASCII（GC5）—— 中文名不能作为 MATLAB 函数被调用。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `Bayesian` 命中 **14 篇**
%   （P2025-A-02/A-04/A-05 · C-01/C-02/C-09/C-10/C-13/C-14/C-16/C-17/C-18 · D-03 · F-01）；
%   ★ 这是**数得出的最高频缺口**（roster §2.6 #7）。`corpus/algorithms/src/`（脚本素材面）0 命中。
%
%   独立参照（**共轭闭式 + MCMC 双路**，本清单里参照最硬的一项）：
%     · 模型 A（正态均值、方差已知）：后验 `mu | y ~ N(mu_n, tau_n^2)` 有**闭式**
%         tau_n^2 = 1 / (1/tau0^2 + n/sigma^2)
%         mu_n    = tau_n^2 * (mu0/tau0^2 + sum(y)/sigma^2)
%       ⇒ 与**自写的随机游走 Metropolis MCMC** 的（后验均值 / 标准差 / 95% 可信区间）对照；
%       ⇒ 另用 `mvnrnd` 从闭式后验**精确抽样**，作第三条独立路径。
%     · 模型 B（贝叶斯线性回归）：用**内置 `bayeslm`**（diffuse 先验）的后验摘要，
%       与手推闭式（OLS 位置 + t 尺度，df = n-p）对照。
%   ★ 随机算法固定种子；本骨架内部跑多个种子，给**多次运行的分布**。
%
%   用法：
%     bayesian()             % 自检并打印读数
%     out = bayesian(opts)   % opts.mu0 opts.tau0 opts.sigma opts.n opts.seeds ...
%
%   返回 struct：mu_n, tau_n, ci_closed, mcmc_mean, mcmc_sd, exact_mean, exact_sd, ...
%   另有模型 B：blm_mean, blm_std, ols_beta, ols_sd。

if nargin < 1 || isempty(opts); opts = struct(); end
mu0   = dflt(opts, 'mu0',   0.0);
tau0  = dflt(opts, 'tau0',  5.0);
sigma = dflt(opts, 'sigma', 2.0);    % 已知方差
n     = dflt(opts, 'n',     20);
mu_true = dflt(opts, 'mu_true', 1.0);
nmc   = dflt(opts, 'nmc',   100000);
nburn = dflt(opts, 'nburn', 10000);
seeds = dflt(opts, 'seeds', 0:4);

% ---- 合成数据（固定种子，已知真值）----
rng(100);
y = mu_true + sigma * randn(n, 1);
ybar = mean(y);

% ---- 模型 A：正态-正态共轭闭式后验 ----
prec0  = 1/tau0^2;
precD  = n/sigma^2;
precN  = prec0 + precD;
tau_n  = 1/sqrt(precN);
mu_n   = tau_n^2 * (mu0*prec0 + sum(y)/sigma^2);
z      = norminv(0.975);
ci_closed = [mu_n - z*tau_n, mu_n + z*tau_n];

% ---- 模型 A 路径二：自写随机游走 Metropolis MCMC（多链）----
logpost = @(m) -0.5*(m-mu0)^2/tau0^2 - 0.5*(n*(ybar-m)^2 + sum((y-ybar).^2))/sigma^2;
prop_sd = 0.5*tau_n;
kk = numel(seeds);
mcmc_mean = zeros(1,kk); mcmc_sd = zeros(1,kk); acc_rate = zeros(1,kk);
for s = 1:kk
    rng(seeds(s));
    m = mu_n; lp = logpost(m); samp = zeros(nmc,1); nacc = 0;
    for it = 1:(nburn+nmc)
        mn = m + prop_sd*randn;
        lpn = logpost(mn);
        if log(rand) < (lpn - lp); m = mn; lp = lpn; nacc = nacc + 1; end
        if it > nburn; samp(it-nburn) = m; end
    end
    mcmc_mean(s) = mean(samp); mcmc_sd(s) = std(samp);
    acc_rate(s)  = nacc / (nburn+nmc);
end

% ---- 模型 A 路径三：mvnrnd 从闭式后验精确抽样 ----
rng(202);
exact = mvnrnd(mu_n, tau_n^2, 50000);
exact_mean = mean(exact); exact_sd = std(exact);
ci_exact = quantile(exact, [0.025 0.975]);

% ---- 模型 B：bayeslm（diffuse）vs 手推闭式 ----
rng(7);
nB = 40; xB = linspace(0,1,nB)'; yB = 1 + 3*xB + 0.5*randn(nB,1);
XB = [ones(nB,1), xB];
pB = 2; dfB = nB - pB;
PriorMdl     = bayeslm(1, ModelType="diffuse");
PosteriorMdl = estimate(PriorMdl, XB, yB, Display=false);
Tsum = summarize(PosteriorMdl);
Marg = Tsum.MarginalDistributions;
blm_mean = [Marg.Mean(1), Marg.Mean(2)];
blm_std  = [Marg.Std(1),  Marg.Std(2)];

bh   = XB \ yB;
RSS  = sum((yB - XB*bh).^2);
s2   = RSS / dfB;
se_scale = sqrt(diag(s2 * inv(XB'*XB)))';        % t 尺度
ols_beta = bh';
ols_sd   = se_scale * sqrt(dfB/(dfB-2));          % t 分布的标准差

out = struct('mu_n', mu_n, 'tau_n', tau_n, 'ci_closed', ci_closed, ...
  'mcmc_mean', mcmc_mean, 'mcmc_sd', mcmc_sd, 'acc_rate', acc_rate, ...
  'mcmc_mean_avg', mean(mcmc_mean), 'mcmc_sd_avg', mean(mcmc_sd), ...
  'mcmc_sd_spread', std(mcmc_sd), ...
  'exact_mean', exact_mean, 'exact_sd', exact_sd, 'ci_exact', ci_exact, ...
  'blm_mean', blm_mean, 'blm_std', blm_std, 'ols_beta', ols_beta, 'ols_sd', ols_sd);

fprintf('[bayesian] 模型 A: 正态均值, sigma = %.4g (已知), n = %d, 先验 N(%.3g, %.3g^2)\n', ...
        sigma, n, mu0, tau0);
fprintf('  后验闭式   : mu_n = %.12g, tau_n = %.12g, 95%%CI = [%.9g, %.9g]\n', ...
        mu_n, tau_n, ci_closed(1), ci_closed(2));
fprintf('  MCMC 均值  : %.9g  (闭式 mu_n 之差 = %.3e)\n', mean(mcmc_mean), ...
        abs(mean(mcmc_mean)-mu_n));
fprintf('  MCMC 标准差: %.9g  (闭式 tau_n 之差 = %.3e)\n', mean(mcmc_sd), ...
        abs(mean(mcmc_sd)-tau_n));
fprintf('  mvnrnd 精确抽样: 均值 = %.9g, 标准差 = %.9g, 95%%CI = [%.9g, %.9g]\n', ...
        exact_mean, exact_sd, ci_exact(1), ci_exact(2));
fprintf('  多次运行分布(%d 链): MCMC 后验均值 = [%s], 接收率 = [%s]\n', ...
        kk, num2str(round(mcmc_mean, 5)), num2str(round(acc_rate, 2)));

fprintf('[bayesian] 模型 B: 贝叶斯线性回归 (bayeslm, diffuse) vs 手推闭式\n');
fprintf('  bayeslm 后验均值 = [%.10g %.10g], 闭式 OLS = [%.10g %.10g]\n', ...
        blm_mean, ols_beta);
fprintf('  bayeslm 后验标准差 = [%.10g %.10g], 闭式 t 尺度 = [%.10g %.10g]\n', ...
        blm_std, ols_sd);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
