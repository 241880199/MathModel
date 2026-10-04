function out = nn_forecast(opts)
%NN_FORECAST  Neural-network regression on a KNOWN function; multi-seed distribution + error-vs-training.
%
%   M4 `mcm-model-select` 骨架 · prediction #8（神经网络预测）。文件名全 ASCII（GC5）。
%   ★ **边界（与 `ml` 的 `nn_classify` 分清）**：本骨架管**序列/函数预测**（输出是连续值），
%     不是"类别判别"（那是 `ml` 的神经网络分类）。类索引与本节均写明这条边界。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `neural network` 命中 **8 篇**（:115）、
%   `BP neural network`（:145 · :195 各 1 篇）、`LSTM`（:124 4 篇）、`RNN`（:156 1 篇）。
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*(neural network|BP neural network|LSTM|RNN)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 5 行。）
%   ★ **素材面**另有起点素材：`corpus/algorithms/src/NeuralNetwork神经网络工具箱的调用案例/` 与 `corpus/algorithms/src/《MATLAB 神经网络30个案例分析》源程序 数据/` —— 教辅级，**不作独立参照**。
%
%   独立参照（第 4 类：已知函数的合成数据 —— 拟合误差随训练下降，且给**多次运行的分布**）：
%     · 已知函数 f(x) = sin(2*pi*x)，在 [0,1] 上采样训练；
%     · 用 `fitnet`（trainlm）拟合 ⇒ 测试 MSE 应随**训练轮数**下降、且远小于 1；
%     · **随机量**：网络初值随 RNG ⇒ **固定种子 + 多次运行给分布**（不是跑一次就宣称达标）。
%   ★ 逐项读数（每次运行的 MSE 分布 + 误差-轮数表）见 `tests/skills/model-select/verify/nn_forecast.md`。
%
%   用法：
%     nn_forecast()             % 自检并打印读数
%     out = nn_forecast(opts)   % opts.H opts.ntr opts.epochs opts.seeds opts.reseed_each
%
%   返回 struct：mse_seeds, mse_mean, mse_sd, epochs_grid, mse_grid, epochs, H, ntr。

if nargin < 1 || isempty(opts); opts = struct(); end
H      = dflt(opts, 'H',      10);
ntr    = dflt(opts, 'ntr',    40);
epochs = dflt(opts, 'epochs', 200);
seeds  = dflt(opts, 'seeds',  1:5);
f = @(x) sin(2 * pi * x);
xtr = linspace(0, 1, ntr);  ytr = f(xtr);
xte = linspace(0, 1, 200);  yte = f(xte);

% --- ① 多次运行的分布（固定种子）---
mse_seeds = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    yp = train_predict(xtr, ytr, xte, H, epochs, seeds(s));
    mse_seeds(s) = mean((yp - yte).^2);
end
mse_mean = mean(mse_seeds);
mse_sd = std(mse_seeds);

% --- ② 误差随训练轮数下降（单一种子）---
epochs_grid = [5 20 60 200];
mse_grid = zeros(1, numel(epochs_grid));
for i = 1:numel(epochs_grid)
    yp = train_predict(xtr, ytr, xte, H, epochs_grid(i), seeds(1));
    mse_grid(i) = mean((yp - yte).^2);
end

out = struct('mse_seeds', mse_seeds, 'mse_mean', mse_mean, 'mse_sd', mse_sd, ...
             'epochs_grid', epochs_grid, 'mse_grid', mse_grid, ...
             'epochs', epochs, 'H', H, 'ntr', ntr, 'seeds', seeds);

fprintf('[nn_forecast] fitnet(H=%d), trainlm, divideFcn=dividetrain, ntr = %d, 目标 f(x)=sin(2*pi*x)\n', H, ntr);
fprintf('  多次运行（固定种子）测试 MSE：\n');
for s = 1:numel(seeds)
    fprintf('    seed=%-3d  MSE = %.8g\n', seeds(s), mse_seeds(s));
end
fprintf('  mean +/- sd = %.8g +/- %.8g  （%d 次运行）\n', mse_mean, mse_sd, numel(seeds));
fprintf('  误差随训练轮数（seed=%d）：\n', seeds(1));
for i = 1:numel(epochs_grid)
    fprintf('    epochs=%-4d  MSE = %.8g\n', epochs_grid(i), mse_grid(i));
end
fprintf('  MSE 是否随 epochs 单调不增 : %s\n', bool2str(all(diff(mse_grid) <= 0)));
end

% ------------------------------------------------------------------------
function yp = train_predict(xtr, ytr, xte, H, epochs, seed)
% 固定种子训练一个前馈网并预测。可复现：rng(seed) 后建网 + 全量训练（dividetrain）。
rng(seed);
net = fitnet(H);
net.trainFcn = 'trainlm';
net.divideFcn = 'dividetrain';                    % 全部用于训练（无随机划分）
net.trainParam.epochs = epochs;
net.trainParam.showWindow = false;
net.trainParam.showCommandLine = false;
net = train(net, xtr, ytr);
yp = net(xte);
end

function s = bool2str(tf)
if tf; s = '是'; else; s = '否'; end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
