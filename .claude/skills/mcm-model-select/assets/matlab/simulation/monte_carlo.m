function out = monte_carlo(opts)
%MONTE_CARLO  Sample U(0,1), estimate mean = 0.5; standard error decays ~ 1/sqrt(n) (n x4 => error halves).
%
%   M4 `mcm-model-select` 骨架 · simulation #2（蒙特卡洛）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `Monte Carlo` 带锚命中 **4 行**
%   （`:33` 4 篇 · `:79` 1 篇 · `:113` 8 篇 · `:191` 2 篇；**去重并集 = 15 篇**）。
%   ★ 另有 **`Markov chain Monte Carlo`（MCMC）带锚 3 行 / 5 篇**（`:48` · `:137` · `:198`）——
%   **本骨架不计入**（MCMC 的角色是统计推断 / 后验抽样，本套件归 `references/statistics/bayesian.md`；
%   口径两面见 verify 记录）。2026-10-04 当场复跑
%   `grep -nE "^ +- Monte Carlo（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`（**带锚形**；裸 `grep -c` 会把 MCMC 与聚合表行混入）。
%   **算法素材面**：`corpus/algorithms/src/IntegerProgramming（线性规划、整数规划等内容的使用案例）/monte_carro.m`
%   —— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知参数的合成数据 + 收敛率）：
%     对 **U(0,1)** 抽样估计其**已知期望 `T = 0.5`** ⇒ 估计量的**标准差** = 1/sqrt(12 n)（理论）；
%     取 `n ∈ {1e3, 4e3, 1.6e4, 6.4e4}`（**每档 n×4**）⇒ 误差应**减半**（相邻档比值 ≈ 2）。
%     ★ **固定种子 + ≥5 次运行 + 逐次读数 + `mean ± sd`**；**绝不许"跑一次就宣称达标"**。
%
%   用法：
%     monte_carlo()             % 自检并打印收敛读数
%     out = monte_carlo(opts)   % opts.ns opts.seeds
%
%   返回 struct：ns, seeds, T, sd, err_mean, ratio, sd_over_theory。

if nargin < 1 || isempty(opts); opts = struct(); end
ns    = dflt(opts, 'ns',    [1000 4000 16000 64000]);
seeds = dflt(opts, 'seeds', 1:20);
T = 0.5;                                        % U(0,1) 的已知期望

K = numel(ns); sd = zeros(1, K); err_mean = zeros(1, K); est_all = zeros(numel(seeds), K);
for k = 1:K
    est = zeros(1, numel(seeds));
    for s = 1:numel(seeds)
        rng(seeds(s));                          % ★ 固定种子（可复现）
        x = rand(1, ns(k));
        est(s) = mean(x);
    end
    est_all(:, k) = est(:);
    e = est - T;
    sd(k)       = std(est);                     % 各档估计量的样本标准差
    err_mean(k) = mean(abs(e));                 % 平均绝对误差
end
ratio          = sd(1:end-1) ./ sd(2:end);      % 相邻档（n×4）比值，期望 ≈ 2
sd_over_theory = sd .* sqrt(12 .* ns);          % sd / (1/sqrt(12 n))，期望 ≈ 1

out = struct('ns', ns, 'seeds', seeds, 'T', T, 'sd', sd, 'err_mean', err_mean, ...
             'ratio', ratio, 'sd_over_theory', sd_over_theory, 'est', est_all);

fprintf('[monte_carlo] sample U(0,1), estimate mean (true T = %.1f), seeds = %s\n', ...
        T, mat2str(seeds));
fprintf('  %8s  %12s  %12s  %12s  %10s\n', 'n', 'sd(est)', 'mean|err|', 'sd/theory', 'n4-ratio');
for k = 1:K
    r = NaN; if k < K; r = ratio(k); end
    fprintf('  %8d  %12.6g  %12.6g  %12.6g  %10.4f\n', ...
            ns(k), sd(k), err_mean(k), sd_over_theory(k), r);
end
fprintf('  ratio sd(n)/sd(4n) = [%s]   (1/sqrt(n) => expected ~ 2)\n', num2str(ratio, '%.4f  '));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
