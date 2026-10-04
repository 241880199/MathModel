function out = svm_regress(opts)
%SVM_REGRESS  Support-vector regression (epsilon-SVR).  Known function
%   f(x) = sin(2x) on x in [-3, 3]; observations y = f(x) + N(0, sigma^2), sigma = 0.15.
%   The KNOWN benchmark is the noise floor: predicting a NEW noisy observation, the
%   best achievable test RMSE is ~= sigma = 0.15 (the test noise is unpredictable).
%   An RBF-kernel SVR should approach it; a LINEAR SVR (wrong model for a sine)
%   should stay well above it.
%
%   M4 `mcm-model-select` 骨架 · ml #3（SVM 回归）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@svm_regress` 类目录撞名（实测 2026-10-04）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `SVR` 带锚 **1 行 / 2 篇**
%   （`P2025-C-10 P2025-C-11`；2026-10-04 当场复跑带锚形，逐条命令见 verify 记录）。
%   `corpus/algorithms/src/` 0 命中。★ **`SVR` 是**回归** tag**（与分类的 `SVM` 分行，见 `svm_classify`）。
%
%   独立参照（第 4 类：已知函数的合成数据 ⇒ 回归 RMSE）：
%     · 已知平滑函数 `sin(2x)` + 已知噪声 sigma ⇒ **预测新含噪观测的测试 RMSE 下界 ≈ sigma**（噪声底）；
%     · 线性 SVR 作对照（模型形式不对 ⇒ 明显高于噪声底）。
%   ★ **不许拿 MATLAB 内置当"独立参照"** —— `fitrsvm` 只作**实现**；参照是**已知函数 + 噪声底**。
%   ★ 固定种子 + **多次运行的分布**（不是只跑一次）。
%
%   用法：
%     svm_regress()             % 自检并打印读数
%     out = svm_regress(opts)   % opts.sigma opts.ntrain opts.ntest opts.seeds
%
%   返回 struct：sigma, ntrain, ntest, seeds,
%                rmse_rbf_seeds, rmse_rbf_mean, rmse_rbf_sd, rmse_lin_seeds, rmse_lin_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
sigma  = dflt(opts, 'sigma',  0.15);
ntrain = dflt(opts, 'ntrain', 400);
ntest  = dflt(opts, 'ntest',  1000);
seeds  = dflt(opts, 'seeds',  1:5);
f  = @(x) sin(2 * x);                          % 已知函数（参照）

rmse_rbf = zeros(1, numel(seeds));
rmse_lin = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    x  = -3 + 6 * rand(ntrain, 1);
    y  = f(x) + sigma * randn(ntrain, 1);
    xte = -3 + 6 * rand(ntest, 1);
    yte = f(xte) + sigma * randn(ntest, 1);    % 参照：**新的含噪观测**（测试噪声不可预测）

    rng(seeds(s) + 500);
    mR = fitrsvm(x, y, 'KernelFunction', 'rbf', 'KernelScale', 'auto', 'Standardize', true);
    mL = fitrsvm(x, y);                        % 默认线性核（对照）
    rmse_rbf(s) = sqrt(mean((predict(mR, xte) - yte).^2));
    rmse_lin(s) = sqrt(mean((predict(mL, xte) - yte).^2));
end

out = struct('sigma', sigma, 'ntrain', ntrain, 'ntest', ntest, 'seeds', seeds, ...
             'rmse_rbf_seeds', rmse_rbf, 'rmse_rbf_mean', mean(rmse_rbf), 'rmse_rbf_sd', std(rmse_rbf), ...
             'rmse_lin_seeds', rmse_lin, 'rmse_lin_mean', mean(rmse_lin));

fprintf('[svm_regress] epsilon-SVR on KNOWN f(x) = sin(2x) + N(0,%.2f^2), %d seeds\n', sigma, numel(seeds));
fprintf('  noise floor (ideal test RMSE = sigma) = %.4f\n', sigma);
fprintf('  RBF    SVR RMSE per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(rmse_rbf, '%.4f  '), mean(rmse_rbf), std(rmse_rbf));
fprintf('  linear SVR RMSE per seed = [%s]  mean = %.4f\n', ...
        num2str(rmse_lin, '%.4f  '), mean(rmse_lin));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
