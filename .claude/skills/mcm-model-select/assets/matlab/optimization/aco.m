function out = aco(opts)
%ACO  Ant colony optimization (ant system) for the 5-city TSP (known optimum = 15); zero-arg.
%
%   M4 `mcm-model-select` 骨架 · optimization #9（蚁群 ACO）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `ant colony` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*ant colony.*（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch22 蚁群-TSP · ch23/ch24 蚁群路径规划）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     **小 TSP 5 城**  C = [0 0; 3 0; 3 4; 0 4; 1.5 2]，**已知最优巡回长度 = 15**（全排列穷举 24 条
%     独立路径得出，见 verify 件）；★ 固定种子（seeds=1:5）各跑一次 ⇒ 逐次长度 + mean±sd + 命中率/相对差。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/aco.md`。
%
%   用法：
%     aco()             % 自检并打印分布读数
%     out = aco(opts)   % opts.C opts.seeds opts.maxit opts.nAnts opts.alpha opts.beta opts.rho opts.tol
%
%   返回 struct：Lbest, tourbest, Lmean, Lsd, hitrate, relgap, Lopt, seeds, maxit, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
C      = dflt(opts, 'C', [0 0; 3 0; 3 4; 0 4; 1.5 2]);
Lopt   = dflt(opts, 'Lopt', 15);          % 已知最优（独立穷举得出）
maxit  = dflt(opts, 'maxit', 60);
nAnts  = dflt(opts, 'nAnts', 10);
alpha  = dflt(opts, 'alpha', 1);          % 信息素权重
beta   = dflt(opts, 'beta', 3);           % 启发式权重
rho    = dflt(opts, 'rho', 0.5);          % 挥发率
Qc     = dflt(opts, 'Qc', 1);
seeds  = dflt(opts, 'seeds', 1:5);
tol    = dflt(opts, 'tol', 1e-9);
n = size(C, 1); Dm = distmat(C);
Eta = 1 ./ Dm; Eta(1:n+1:end) = 0;        % 启发式 1/d（对角置 0）

Lbest = zeros(1, numel(seeds)); tourbest = zeros(numel(seeds), n);
for s = 1:numel(seeds)
    rng(seeds(s));                                % ★ 固定种子（可复现）
    Tau = ones(n);
    bL = inf; bt = 1:n;
    for it = 1:maxit
        Tours = zeros(nAnts, n); Ls = zeros(nAnts, 1);
        for a = 1:nAnts
            tabu = false(1, n);
            tour = zeros(1, n); st = randi(n); tour(1) = st; tabu(st) = true;
            for pos = 2:n
                cur = tour(pos-1);
                prob = (Tau(cur,:).^alpha) .* (Eta(cur,:).^beta);
                prob(tabu) = 0;
                if sum(prob) <= 0
                    cand = find(~tabu); nxt = cand(randi(numel(cand)));
                else
                    prob = prob / sum(prob); nxt = find(rand <= cumsum(prob), 1);
                end
                tour(pos) = nxt; tabu(nxt) = true;
            end
            Tours(a, :) = tour; Ls(a) = tourlen(tour, Dm);
            if Ls(a) < bL; bL = Ls(a); bt = tour; end
        end
        Tau = (1 - rho) * Tau;                    % 挥发
        for a = 1:nAnts                           % 按路径长度沉积信息素
            for k = 1:n
                i = Tours(a, k); j = Tours(a, mod(k, n) + 1);
                Tau(i, j) = Tau(i, j) + Qc / Ls(a);
            end
        end
    end
    Lbest(s) = bL; tourbest(s, :) = bt;
end

Lmean = mean(Lbest); Lsd = std(Lbest); hitrate = mean(abs(Lbest - Lopt) <= max(tol, 1e-6));
relgap = (Lbest - Lopt) / Lopt;
out = struct('Lbest', Lbest, 'tourbest', tourbest, 'Lmean', Lmean, 'Lsd', Lsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'Lopt', Lopt, 'seeds', seeds, ...
             'maxit', maxit, 'tol', tol);

fprintf('[aco] 5 城 TSP（已知最优 = %.6g）· maxit=%d · nAnts=%d · alpha=%g beta=%g rho=%g · seeds=%s\n', ...
        Lopt, maxit, nAnts, alpha, beta, rho, mat2str(seeds));
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
