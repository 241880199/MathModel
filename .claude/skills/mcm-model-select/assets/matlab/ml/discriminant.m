function out = discriminant(opts)
%DISCRIMINANT  Linear/quadratic discriminant vs Bayes-optimal error (synthetic Gaussian classes).
%
%   M4 `mcm-model-select` 骨架 · ml #8（判别分析）。文件名全 ASCII（GC5）。内置 `classify`。
%
%   语料面（P6）：`[社区]` —— `discriminant` / `判别分析` 在 `corpus/papers/MODEL_MAP.md` **0 命中**
%   （2026-10-04 当场复跑）；`corpus/algorithms/src/` 0 命中
%   （受控词表 `tools/papers/vocab/models.txt` 有 `discriminant analysis` 词条，但 2025 O 奖语料**无实例**）。
%   ★ **教科书级常识**。
%
%   独立参照（第 4 类：已知类别的合成数据 ⇒ 错误率对得上贝叶斯最优）：
%     · 两高斯类、**等协方差** ⇒ 线性判别（LDA）是**贝叶斯最优**；理论错误率
%       `err_bayes = Phi(-Delta/2)`，`Delta = sqrt((m1-m2)' Sigma^{-1} (m1-m2))`（教科书级闭式）；
%     · 用内置 `classify(...,'linear')` 在**独立测试集**上估错误率 ⇒ 应趋近 `err_bayes`
%       （有限训练集 ⇒ 略高于理论，因参数估计误差）；
%     · 另给一个**不等协方差**的二次判别（`'quadratic'`）作对照。
%   ★ 固定种子 + **多组重复的分布**（不是只跑一次）。
%
%   用法：
%     discriminant()             % 自检并打印读数
%     out = discriminant(opts)   % opts.d opts.delta opts.ntrain opts.ntest opts.seeds
%
%   返回 struct：delta_maha, bayes_err, err_lin_seeds, err_lin_mean, err_lin_sd,
%                err_quad_seeds, err_quad_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
d      = dflt(opts, 'd',      2);
delta  = dflt(opts, 'delta',  2.0);      % 类均值间的马氏距离（Sigma = I ⇒ 欧氏距离）
ntrain = dflt(opts, 'ntrain', 200);
ntest  = dflt(opts, 'ntest',  2000);
seeds  = dflt(opts, 'seeds',  1:5);

m1 = zeros(1, d);
m2 = zeros(1, d); m2(1) = delta;
Sigma = eye(d);                          % 共同协方差（等协方差 ⇒ LDA 最优）

% 贝叶斯最优（闭式，教科书级）：两等协方差高斯类、等先验
delta_maha = sqrt((m1 - m2) * (Sigma \ (m1 - m2)'));
bayes_err  = normcdf(-delta_maha / 2);

err_lin  = zeros(1, numel(seeds));
err_quad = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    Xtr = [mvnrnd(m1, Sigma, ntrain); mvnrnd(m2, Sigma, ntrain)];
    Ytr = [ones(ntrain, 1); 2 * ones(ntrain, 1)];
    Xte = [mvnrnd(m1, Sigma, ntest);  mvnrnd(m2, Sigma, ntest)];
    Yte = [ones(ntest, 1); 2 * ones(ntest, 1)];
    plin  = classify(Xte, Xtr, Ytr, 'linear');
    pquad = classify(Xte, Xtr, Ytr, 'quadratic');
    err_lin(s)  = mean(plin  ~= Yte);
    err_quad(s) = mean(pquad ~= Yte);
end

out = struct('d', d, 'delta_maha', delta_maha, 'bayes_err', bayes_err, ...
             'ntrain', ntrain, 'ntest', ntest, 'seeds', seeds, ...
             'err_lin_seeds', err_lin, 'err_lin_mean', mean(err_lin), 'err_lin_sd', std(err_lin), ...
             'err_quad_seeds', err_quad, 'err_quad_mean', mean(err_quad));

fprintf('[discriminant] 2 Gaussian classes, d = %d, Delta(Mahalanobis) = %.4g\n', d, delta_maha);
fprintf('  Bayes-optimal error  = Phi(-Delta/2) = %.4f\n', bayes_err);
fprintf('  --- test-set error, ntrain = %d/class, ntest = %d/class, %d seeds ---\n', ...
        ntrain, ntest, numel(seeds));
fprintf('  linear    per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(err_lin, '%.4f  '), mean(err_lin), std(err_lin));
fprintf('  quadratic per seed = [%s]  mean = %.4f\n', ...
        num2str(err_quad, '%.4f  '), mean(err_quad));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
