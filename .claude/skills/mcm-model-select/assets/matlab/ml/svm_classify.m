function out = svm_classify(opts)
%SVM_CLASSIFY  Support-vector classification (max-margin). Two known-boundary cases:
%   (A) two equal-covariance Gaussians (Delta = 2) => linear boundary is Bayes-optimal,
%       KNOWN error Phi(-Delta/2) = 0.1587; a LINEAR SVM should approach it;
%   (B) XOR quadrants y = sign(x1*x2) => KNOWN nonlinear boundary; a LINEAR SVM cannot
%       separate it (~0.50) while an RBF-kernel SVM can (high accuracy).
%
%   M4 `mcm-model-select` 骨架 · ml #2（SVM 分类）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@svm_classify` 类目录撞名（实测 2026-10-04）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `SVM` 带锚 **1 行 / 3 篇**
%   （`P2025-C-07 P2025-C-08 P2025-C-11`；2026-10-04 当场复跑带锚形，逐条命令见 verify 记录）。
%   `corpus/algorithms/src/` 0 命中。★ **`SVM` 是整串 tag**（非 `SVR`，后者是回归，见 `svm_regress`）。
%
%   独立参照（第 4 类：已知类别边界的合成数据 ⇒ 分类准确率）：
%     · (A) 线性可分的等协方差高斯类 ⇒ 线性 SVM 测试错误率趋近 `Phi(-Delta/2)`；
%     · (B) XOR 的**已知非线性边界** `sign(x1*x2)`（无噪声 ⇒ 贝叶斯准确率 = 1.0）⇒
%       线性 SVM 无法分离、RBF 核 SVM 可以。
%   ★ **不许拿 MATLAB 内置当"独立参照"** —— `fitcsvm` 只作**实现**；参照是**已知边界 / 闭式贝叶斯误差**。
%   ★ 固定种子 + **多次运行的分布**（不是只跑一次）。
%
%   用法：
%     svm_classify()             % 自检并打印读数
%     out = svm_classify(opts)   % opts.delta opts.ntrain opts.ntest opts.seeds opts.sigma_xor
%
%   返回 struct：bayes_err, err_linA_seeds, err_linA_mean, err_linA_sd,
%                acc_linB_seeds, acc_rbfB_seeds, acc_linB_mean, acc_rbfB_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
delta   = dflt(opts, 'delta',   2.0);
ntrain  = dflt(opts, 'ntrain',  300);
ntest   = dflt(opts, 'ntest',   2000);
seeds   = dflt(opts, 'seeds',   1:5);
sigma_x = dflt(opts, 'sigma_xor', 1.3);

% --- (A) 线性可分的等协方差高斯类：已知贝叶斯最优 ---
m1 = [0 0]; m2 = [delta 0]; Sigma = eye(2);
bayes_err = normcdf(-sqrt((m1 - m2) * (Sigma \ (m1 - m2)')) / 2);

err_A   = zeros(1, numel(seeds));    % 线性 SVM 错误率（case A）
acc_linB = zeros(1, numel(seeds));   % 线性 SVM 准确率（case B，XOR）
acc_rbfB = zeros(1, numel(seeds));   % RBF   SVM 准确率（case B，XOR）
for s = 1:numel(seeds)
    rng(seeds(s));
    % (A) 线性可分的等协方差高斯类
    Xtr = [mvnrnd(m1, Sigma, ntrain); mvnrnd(m2, Sigma, ntrain)];
    Ytr = [ones(ntrain, 1); 2 * ones(ntrain, 1)];
    Xte = [mvnrnd(m1, Sigma, ntest);  mvnrnd(m2, Sigma, ntest)];
    Yte = [ones(ntest, 1); 2 * ones(ntest, 1)];
    mdlA = fitcsvm(Xtr, Ytr);                      % 默认线性核
    err_A(s) = mean(predict(mdlA, Xte) ~= Yte);

    % (B) XOR：已知非线性边界 y = sign(x1*x2)
    XtrB = sigma_x * randn(ntrain, 2);
    YtrB = 2 - (XtrB(:, 1) .* XtrB(:, 2) >= 0);    % 一三象限 => 1；二四象限 => 2（x1·x2 ≥ 0 ⇔ 同号）
    XteB = sigma_x * randn(ntest, 2);
    YteB = 2 - (XteB(:, 1) .* XteB(:, 2) >= 0);
    mdlLin = fitcsvm(XtrB, YtrB);                  % 线性核（应失败）
    mdlRbf = fitcsvm(XtrB, YtrB, 'KernelFunction', 'rbf', 'KernelScale', 'auto');
    acc_linB(s) = mean(predict(mdlLin, XteB) == YteB);
    acc_rbfB(s) = mean(predict(mdlRbf, XteB) == YteB);
end

out = struct('delta_maha', delta, 'bayes_err', bayes_err, ...
             'ntrain', ntrain, 'ntest', ntest, 'seeds', seeds, 'sigma_xor', sigma_x, ...
             'err_linA_seeds', err_A, 'err_linA_mean', mean(err_A), 'err_linA_sd', std(err_A), ...
             'acc_linB_seeds', acc_linB, 'acc_rbfB_seeds', acc_rbfB, ...
             'acc_linB_mean', mean(acc_linB), 'acc_rbfB_mean', mean(acc_rbfB));

fprintf('[svm_classify] max-margin classification, %d seeds\n', numel(seeds));
fprintf('  (A) 2 equal-cov Gaussian classes, Delta = %.4g  (linear Bayes-optimal err = %.4f)\n', ...
        delta, bayes_err);
fprintf('      linear SVM  per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(err_A, '%.4f  '), mean(err_A), std(err_A));
fprintf('  (B) XOR  y = sign(x1*x2)  (known nonlinear boundary, Bayes accuracy = 1.0)\n');
fprintf('      linear SVM acc per seed = [%s]  mean = %.4f\n', ...
        num2str(acc_linB, '%.4f  '), mean(acc_linB));
fprintf('      RBF    SVM acc per seed = [%s]  mean = %.4f\n', ...
        num2str(acc_rbfB, '%.4f  '), mean(acc_rbfB));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
