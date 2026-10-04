function out = elm(opts)
%ELM  Extreme learning machine: a single hidden layer with RANDOM weights and
%   output weights solved in closed form (ridge), so "training" is one linear solve.
%   Example below = two equal-covariance Gaussian classes (Delta = 2) => KNOWN
%   Bayes-optimal error Phi(-Delta/2) = 0.1587; ELM test error should approach it.
%
%   M4 `mcm-model-select` 骨架 · ml #4（极限学习机 ELM）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@elm` 类目录撞名（实测 2026-10-04）；MATLAB 也**无内置 `elm`**
%     （`exist('elm')` 实测 = 0）⇒ 本骨架**自写 ELM**（随机隐层 + 岭回归输出权重）。
%
%   语料面（P6）：`[社区]` —— `ELM` / `extreme learning machine` 在 `corpus/papers/MODEL_MAP.md`
%   **0 命中**（2026-10-04 当场复跑带锚形；正对照见 verify 记录：同形 `SVM` 带锚 3 篇 ⇒ 命令没写错）；
%   `corpus/algorithms/src/` 0 命中。★ **教科书级常识**。
%
%   独立参照（第 4 类：已知参数的合成数据）：
%     · 两高斯类、**等协方差** `Sigma = I`、等先验、类均值距 Delta = 2（马氏距离）⇒
%       **线性边界是贝叶斯最优**，理论错误率 `err_bayes = Phi(-Delta/2) = 0.1587`（教科书级闭式）；
%     · ELM 在**独立测试集**上估错误率 ⇒ 应趋近 `err_bayes`（有限训练集 ⇒ 略高）；
%     · 一个**线性最小二乘分类器**（同一 ELM 去掉隐层 = 直接对线性模型解）作对照，应同样 ≈ 贝叶斯。
%   ★ 固定随机种子（隐层权重随机）+ **多次运行的分布**（不是只跑一次）。
%
%   用法：
%     elm()             % 自检并打印读数
%     out = elm(opts)   % opts.L opts.lambda opts.ntrain opts.ntest opts.seeds opts.delta opts.hidden
%
%   返回 struct：L, lambda, delta_maha, bayes_err, err_seeds, err_mean, err_sd,
%                err_lin_seeds, err_lin_mean, hidden。

if nargin < 1 || isempty(opts); opts = struct(); end
L      = dflt(opts, 'L',      60);
lambda = dflt(opts, 'lambda', 1e-6);
ntrain = dflt(opts, 'ntrain', 600);
ntest  = dflt(opts, 'ntest',  4000);
seeds  = dflt(opts, 'seeds',  0:4);
delta  = dflt(opts, 'delta',  2.0);
hidden = dflt(opts, 'hidden', 'sig');      % 'sig' = sigmoid 隐层（ELM 常用）

m1 = [0 0]; m2 = [delta 0];
Sigma = eye(2);                             % 等协方差 ⇒ 线性贝叶斯边界
delta_maha = sqrt((m1 - m2) * (Sigma \ (m1 - m2)'));
bayes_err  = normcdf(-delta_maha / 2);      % Phi(-Delta/2)，教科书级闭式

err_elm = zeros(1, numel(seeds));
err_lin = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    Xtr = [mvnrnd(m1, Sigma, ntrain); mvnrnd(m2, Sigma, ntrain)];
    Ytr = [ones(ntrain, 1); 2 * ones(ntrain, 1)];
    Xte = [mvnrnd(m1, Sigma, ntest);  mvnrnd(m2, Sigma, ntest)];
    Yte = [ones(ntest, 1); 2 * ones(ntest, 1)];

    Ttr = full(ind2vec(Ytr', 2))';          % 2 列 one-hot（2*ntrain x 2）

    % --- ELM：随机隐层 + 岭回归输出权重 ---
    rng(seeds(s) + 1000);                    % 隐层随机权重独立流（固定种子）
    W = randn(size(Xtr, 2), L);
    b = randn(1, L);
    Htr = act(Xtr * W + repmat(b, size(Xtr, 1), 1), hidden);
    beta = (Htr' * Htr + lambda * eye(L)) \ (Htr' * Ttr);
    Hte = act(Xte * W + repmat(b, size(Xte, 1), 1), hidden);
    [~, yp] = max(Hte * beta, [], 2);
    err_elm(s) = mean(yp ~= Yte);

    % --- 对照：线性最小二乘分类器（等价于 ELM 去掉隐层）---
    Xtr1 = [ones(size(Xtr, 1), 1) Xtr];
    Xte1 = [ones(size(Xte, 1), 1) Xte];
    B = Xtr1 \ Ttr;
    [~, yl] = max(Xte1 * B, [], 2);
    err_lin(s) = mean(yl ~= Yte);
end

out = struct('L', L, 'lambda', lambda, 'hidden', hidden, 'delta_maha', delta_maha, ...
             'bayes_err', bayes_err, 'ntrain', ntrain, 'ntest', ntest, 'seeds', seeds, ...
             'err_seeds', err_elm, 'err_mean', mean(err_elm), 'err_sd', std(err_elm), ...
             'err_lin_seeds', err_lin, 'err_lin_mean', mean(err_lin));

fprintf('[elm] ELM (%d hidden units, %s), 2 equal-cov Gaussian classes, Delta = %.4g\n', ...
        L, hidden, delta_maha);
fprintf('  Bayes-optimal error = Phi(-Delta/2) = %.4f\n', bayes_err);
fprintf('  --- test-set error, ntrain = %d/class, ntest = %d/class, %d seeds ---\n', ...
        ntrain, ntest, numel(seeds));
fprintf('  ELM       per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(err_elm, '%.4f  '), mean(err_elm), std(err_elm));
fprintf('  linear LS per seed = [%s]  mean = %.4f\n', ...
        num2str(err_lin, '%.4f  '), mean(err_lin));
end

function H = act(Z, kind)
if strcmp(kind, 'relu')
    H = max(Z, 0);
else
    H = 1 ./ (1 + exp(-Z));
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
