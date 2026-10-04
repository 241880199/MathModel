function out = queueing(opts)
%QUEUEING  M/M/1 queue: closed-form L/W/rho vs a discrete-event (Lindley) simulation.
%
%   M4 `mcm-model-select` 骨架 · simulation #3（排队论 · M/M/1 · 离散事件仿真）。文件名全 ASCII（GC5）。
%
%   语料面（P5 · P6）：★ **低使用度** —— `corpus/papers/MODEL_MAP.md` 里 `queueing theory` 仅 **1 篇**
%   （P2025-D-01）。`corpus/algorithms/src/`（脚本素材面）0 实质命中
%   （唯一 `queue` 命中是 `corpus/algorithms/src/GraphTheory(图论)/detailed/树/BFS.m` 里的 BFS 队列变量，非排队论）。
%   ★ **本项低使用度、照补是为覆盖面**（GC6 表把它列在"三类套不上"，但 M/M/1 有闭式 ⇒ 本骨架按**第 1 类**做）。
%
%   独立参照（第 1 类：解析解）—— M/M/1 闭式（教科书级）：
%     rho = lambda/mu;  L = rho/(1-rho);  Lq = rho^2/(1-rho);  W = L/lambda;  Wq = Lq/lambda。
%   ★ 与骨架对照的是**自写的离散事件（Lindley 递推 + 时间平均队长）仿真**，与解析解**不同源**。
%   ★ 随机算法：固定种子 + 给**多次运行的分布**（不是只跑一次）。
%
%   用法：
%     queueing()             % 自检并打印读数
%     out = queueing(opts)   % opts.lambda opts.mu opts.M opts.warmup opts.seeds
%
%   返回 struct：rho, L, Lq, W, Wq, L_sim_mean, L_sim_sd, W_sim_mean, W_sim_sd,
%                L_sim_seeds, W_sim_seeds。

if nargin < 1 || isempty(opts); opts = struct(); end
lambda = dflt(opts, 'lambda', 0.8);
mu     = dflt(opts, 'mu',     1.0);
M      = dflt(opts, 'M',      1000000);
warmup = dflt(opts, 'warmup', 1000);
seeds  = dflt(opts, 'seeds',  1:5);

if lambda >= mu
    error('queueing:unstable', 'M/M/1 requires lambda < mu (rho < 1); got rho = %.4g.', lambda/mu);
end

% --- 解析（闭式）---
rho = lambda / mu;
L   = rho / (1 - rho);
Lq  = rho^2 / (1 - rho);
W   = L / lambda;
Wq  = Lq / lambda;

% --- 离散事件仿真（Lindley 递推）---
Ls = zeros(1, numel(seeds)); Ws = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    A   = exprnd(1/lambda, M, 1);      % 到达间隔 ~ Exp(lambda)
    S   = exprnd(1/mu,     M, 1);      % 服务时长 ~ Exp(mu)
    arr = cumsum(A);
    start = zeros(M, 1); dep = zeros(M, 1);
    for i = 1:M
        if i == 1; start(i) = arr(i); else; start(i) = max(arr(i), dep(i-1)); end
        dep(i) = start(i) + S(i);
    end
    Wsys = dep - arr;                  % 每客在系统内时间
    t0 = arr(warmup + 1); T = dep(M);  % 丢弃预热段 [0, t0)
    area = sum(max(T - max(arr, t0), 0)) - sum(max(T - max(dep, t0), 0));
    Ls(s) = area / (T - t0);           % 时间平均队长
    Ws(s) = mean(Wsys(warmup + 1:end));
end

out = struct('lambda', lambda, 'mu', mu, 'rho', rho, 'L', L, 'Lq', Lq, 'W', W, 'Wq', Wq, ...
             'M', M, 'seeds', seeds, 'L_sim_seeds', Ls, 'W_sim_seeds', Ws, ...
             'L_sim_mean', mean(Ls), 'L_sim_sd', std(Ls), ...
             'W_sim_mean', mean(Ws), 'W_sim_sd', std(Ws));

fprintf('[queueing] M/M/1  lambda = %.4g, mu = %.4g, rho = %.4g\n', lambda, mu, rho);
fprintf('  closed-form: L = %.6f, Lq = %.6f, W = %.6f, Wq = %.6f\n', L, Lq, W, Wq);
fprintf('  --- discrete-event simulation (Lindley), M = %d, %d seeds ---\n', M, numel(seeds));
fprintf('  L_sim per seed = [%s]\n', num2str(Ls, '%.4f  '));
fprintf('  W_sim per seed = [%s]\n', num2str(Ws, '%.4f  '));
fprintf('  L_sim = %.4f +/- %.4f   (closed-form %.4f, rel.err %.2e)\n', ...
        mean(Ls), std(Ls), L, abs(mean(Ls) - L)/L);
fprintf('  W_sim = %.4f +/- %.4f   (closed-form %.4f, rel.err %.2e)\n', ...
        mean(Ws), std(Ws), W, abs(mean(Ws) - W)/W);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
