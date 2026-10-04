function out = nn_classify(opts)
%NN_CLASSIFY  Feedforward neural-network CLASSIFIER (built-in `fitcnet`) on two
%   concentric classes with a KNOWN radial boundary: class 1 = disk  r <= 1.5,
%   class 2 = annulus 2.0 <= r <= 3.2 (noiseless => Bayes accuracy = 1.0).
%   A LINEAR classifier cannot separate a disk from a surrounding ring (accuracy ~= majority-class rate 0.6113, not chance);
%   the network can.  ★ This is CLASSIFICATION (class labels); sequence/future
%   PREDICTION is a different method (`prediction/nn_forecast`) — see six-grid.
%
%   M4 `mcm-model-select` 骨架 · ml #1（神经网络分类）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@nn_classify` 类目录撞名（实测 2026-10-04）。
%   ★ 本骨架用**内置 `fitcnet`**（前馈网络，BP 类）作实现；内置**只作实现、不作独立参照**。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `BP neural network`
%   带锚 **2 行 / 去重 2 篇**（`P2025-C-07 P2025-D-01`）· `neural network` 带锚 **1 行 / 8 篇**
%   （2026-10-04 当场复跑带锚形，逐条命令见 verify 记录）。`corpus/algorithms/src/` 0 命中。
%
%   独立参照（第 4 类：已知类别边界的合成数据 ⇒ 分类准确率）：
%     · 已知**径向边界**（disk / annulus，无噪声 ⇒ 贝叶斯准确率 = 1.0）；
%     · 一个**线性分类器**（`fitclinear`）作对照 —— 对这种径向边界它只能到随机水平。
%   ★ 固定随机种子（网络权重随机初始化）+ **多次运行的分布**（不是只跑一次）。
%
%   用法：
%     nn_classify()             % 自检并打印读数
%     out = nn_classify(opts)   % opts.layers opts.ntrain opts.ntest opts.seeds opts.r_in opts.r_out
%
%   返回 struct：layers, r_in, r_out, ntrain, ntest, seeds,
%                acc_nn_seeds, acc_nn_mean, acc_nn_sd, acc_lin_seeds, acc_lin_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
layers = dflt(opts, 'layers', [16 8]);     % 两个隐层
ntrain = dflt(opts, 'ntrain', 400);
ntest  = dflt(opts, 'ntest',  2000);
seeds  = dflt(opts, 'seeds',  1:5);
r_in   = dflt(opts, 'r_in',   1.5);         % class 1: disk  r <= r_in
r_out  = dflt(opts, 'r_out',  3.2);         % class 2: annulus 2.0 <= r <= r_out
r_gap  = 2.0;

acc_nn  = zeros(1, numel(seeds));
acc_lin = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    [Xtr, Ytr] = circles(ntrain, r_in, r_gap, r_out);
    [Xte, Yte] = circles(ntest,  r_in, r_gap, r_out);

    rng(seeds(s) + 500);                    % 网络权重随机初始化（固定种子）
    mdl = fitcnet(Xtr, Ytr, 'LayerSizes', layers, 'Standardize', true, ...
                  'IterationLimit', 500, 'Verbose', 0);
    acc_nn(s) = mean(predict(mdl, Xte) == Yte);

    lin = fitclinear(Xtr, Ytr);             % 线性对照
    acc_lin(s) = mean(predict(lin, Xte) == Yte);
end

out = struct('layers', layers, 'r_in', r_in, 'r_out', r_out, 'r_gap', r_gap, ...
             'ntrain', ntrain, 'ntest', ntest, 'seeds', seeds, ...
             'acc_nn_seeds', acc_nn, 'acc_nn_mean', mean(acc_nn), 'acc_nn_sd', std(acc_nn), ...
             'acc_lin_seeds', acc_lin, 'acc_lin_mean', mean(acc_lin));

fprintf('[nn_classify] feedforward net (fitcnet) layers = [%s], %d seeds\n', ...
        num2str(layers, '%d '), numel(seeds));
fprintf('  known radial boundary: class 1 = disk r <= %.2f, class 2 = annulus %.2f..%.2f', ...
        r_in, r_gap, r_out);
fprintf('  (Bayes accuracy = 1.0)\n');
fprintf('  NN     acc per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(acc_nn, '%.4f  '), mean(acc_nn), std(acc_nn));
fprintf('  linear acc per seed = [%s]  mean = %.4f\n', ...
        num2str(acc_lin, '%.4f  '), mean(acc_lin));
end

function [X, Y] = circles(n, r_in, r_gap, r_out)
% 半径环状采样（等点数）：内 disk n/2 点（按面积均匀），外 annulus n/2 点（按面积均匀）
n1 = floor(n / 2); n2 = n - n1;
r1 = r_in  * sqrt(rand(n1, 1));                          % 内 disk：面积均匀
r2 = sqrt(rand(n2, 1) * (r_out^2 - r_gap^2) + r_gap^2);  % 外 annulus：面积均匀
r  = [r1; r2];
th = 2 * pi * rand(n, 1);
X  = [r .* cos(th), r .* sin(th)];
Y  = [ones(n1, 1); 2 * ones(n2, 1)];
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
