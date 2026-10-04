function out = sa(opts)
%SA  Simulated annealing for the 5-city TSP (known-optimal tour = 15); zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #6（模拟退火）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `simulated annealing` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*simulated annealing.*（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/HeuristicAlgorithm（补分启发式算法，包括神经网络、模拟退火、遗传算法）/模拟退火算法/`
%   与 `corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch19 SA-TSP · ch21 SA 工具箱）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     **小 TSP 5 城**  C = [0 0; 3 0; 3 4; 0 4; 1.5 2]，**已知最优巡回长度 = 15**（全排列穷举 24 条
%     独立路径得出，见 verify 件）；★ 固定种子（seeds=1:5）各跑一次 ⇒ 逐次长度 + mean±sd + 命中率/相对差。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/sa.md`。
%
%   用法：
%     sa()             % 自检并打印分布读数
%     out = sa(opts)   % opts.C opts.seeds opts.maxit opts.T0 opts.alpha opts.tol
%
%   返回 struct：Lbest, tourbest, Lmean, Lsd, hitrate, relgap, Lopt, seeds, maxit, T0, alpha, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
C      = dflt(opts, 'C', [0 0; 3 0; 3 4; 0 4; 1.5 2]);
Lopt   = dflt(opts, 'Lopt', 15);          % 已知最优（独立穷举得出）
maxit  = dflt(opts, 'maxit', 3000);
T0     = dflt(opts, 'T0', 5.0);
alpha  = dflt(opts, 'alpha', 0.995);
seeds  = dflt(opts, 'seeds', 1:5);
tol    = dflt(opts, 'tol', 1e-9);
n = size(C, 1);
Dm = distmat(C);

Lbest = zeros(1, numel(seeds)); tourbest = zeros(numel(seeds), n);
for s = 1:numel(seeds)
    rng(seeds(s));                                % ★ 固定种子（可复现）
    tour = randperm(n); L = tourlen(tour, Dm);
    bt = tour; bL = L; T = T0;
    for k = 1:maxit
        ij = sort(randi(n, 1, 2)); i = ij(1); j = ij(2);
        if i == j; continue; end
        cand = [tour(1:i-1), fliplr(tour(i:j)), tour(j+1:end)];   % 2-opt 反转
        Lc = tourlen(cand, Dm);
        if Lc < L || rand < exp(-(Lc - L)/max(T, eps))            % Metropolis 接受
            tour = cand; L = Lc;
            if L < bL; bt = tour; bL = L; end
        end
        T = max(T * alpha, 1e-6);
    end
    Lbest(s) = bL; tourbest(s, :) = bt;
end

Lmean = mean(Lbest); Lsd = std(Lbest); hitrate = mean(abs(Lbest - Lopt) <= max(tol, 1e-6));
relgap = (Lbest - Lopt) / Lopt;
out = struct('Lbest', Lbest, 'tourbest', tourbest, 'Lmean', Lmean, 'Lsd', Lsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'Lopt', Lopt, 'seeds', seeds, ...
             'maxit', maxit, 'T0', T0, 'alpha', alpha, 'tol', tol);

fprintf('[sa] 5 城 TSP（已知最优 = %.6g）· maxit=%d · T0=%.3g · alpha=%.4g · seeds=%s\n', ...
        Lopt, maxit, T0, alpha, mat2str(seeds));
for s = 1:numel(seeds)
    fprintf('  seed=%-3d  L_best = %.8g   rel.gap = %+.3e\n', seeds(s), Lbest(s), relgap(s));
end
fprintf('  mean ± sd = %.8g ± %.8g   · 命中率(L==Lopt) = %d/%d\n', ...
        Lmean, Lsd, sum(abs(Lbest - Lopt) <= max(tol, 1e-6)), numel(seeds));
end

% ------------------------------------------------------------------------
function Dm = distmat(C)
n = size(C, 1); Dm = zeros(n);
for a = 1:n
    for b = 1:n
        Dm(a, b) = hypot(C(a,1) - C(b,1), C(a,2) - C(b,2));
    end
end
end

function L = tourlen(tour, Dm)
n = numel(tour);
L = 0;
for k = 1:n
    L = L + Dm(tour(k), tour(mod(k, n) + 1));
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
