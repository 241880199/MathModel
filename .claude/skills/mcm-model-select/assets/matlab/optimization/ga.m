function out = ga(opts)
%GA  Real-coded genetic algorithm on 2-D 凸二次 (known min f*=3 at (2,-1)); zero-arg.
%
%   M4 `mcm-model-select` 骨架 · optimization #5（遗传算法）。文件名全 ASCII（GC5）。
%   ★ **撞名说明**：MATLAB Global Optimization Toolbox 有同名函数 `ga`（路径文件胜出，本骨架优先）；
%     `addpath` 本目录后，**同会话里的其它代码调 `ga` 会拿到本文件** —— 这是**函数级**撞名（可接受），
%     **不是**类目录撞名（`@ga` 顶层类目录：实测无）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `genetic algorithm` 命中 **3 行**
%   （`:72` 2 篇 · `:167` 1 篇 · `:209` 1 篇；**去重并集 = 4 篇**：P2025-B-05/B-07/C-10/D-01；
%   2026-10-04 当场复跑 `grep -nE "^ +- genetic algorithm（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`）。
%   **算法素材面**：`corpus/algorithms/src/HeuristicAlgorithm（补分启发式算法，包括神经网络、模拟退火、遗传算法）/`
%   与 `corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch1–ch9/ch11 GA 系列）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     benchmark = 2-D 凸二次  f(x) = 3 + (x1-2)^2 + (x2+1)^2，域 [-10,10]^2，
%     **已知全局最优 f*=3 于 (2,-1)**（**单峰** ⇒ 收敛到该点即"算对"；人造基准，教科书级 `[社区]`）。
%     ★ 固定种子（seeds=1:5）各跑一次，报**逐次读数 + mean±sd + 命中率（|f-f*|<=tol）+ 相对差**；
%       **绝不许"跑一次就宣称达标"**。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/ga.md`。
%
%   用法：
%     ga()             % 自检并打印分布读数
%     out = ga(opts)   % opts.pop opts.maxgen opts.pc opts.pm opts.seeds opts.tol
%
%   返回 struct：fbest, xbest, fmean, fsd, hitrate, relgap, seeds, pop, maxgen, lo, hi, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
D      = 2;
lo = -10; hi = 10;
pop    = dflt(opts, 'pop', 40);
maxgen = dflt(opts, 'maxgen', 150);
pc     = dflt(opts, 'pc', 0.9);
pm     = dflt(opts, 'pm', 0.1);
seeds  = dflt(opts, 'seeds', 1:5);
tol    = dflt(opts, 'tol', 1e-4);
fit = @(x) 3 + (x(:,1) - 2).^2 + (x(:,2) + 1).^2;     % 已知最优 f*=3 于 (2,-1)

fbest = zeros(1, numel(seeds)); xbest = zeros(numel(seeds), D);
for s = 1:numel(seeds)
    rng(seeds(s));                                  % ★ 固定种子（可复现）
    P = lo + (hi - lo) .* rand(pop, D);
    fv = fit(P);
    for gen = 1:maxgen
        % --- 锦标赛选择（规模 2）---
        ii = randi(pop, pop, 2); fpair = fv(ii);
        [~, win] = min(fpair, [], 2);
        Q = P(ii(sub2ind(size(ii), (1:pop).', win)), :);
        % --- 算术（混合）交叉 ---
        for k = 1:2:pop-1
            if rand < pc
                lam = rand; a = Q(k,:); b2 = Q(k+1,:);
                Q(k,:) = lam*a + (1-lam)*b2; Q(k+1,:) = (1-lam)*a + lam*b2;
            end
        end
        % --- 高斯变异（步长随代数收缩）---
        sigma = 0.5 * (1 - gen/maxgen) + 0.05;
        Q = Q + (rand(pop, D) < pm) .* (sigma * (hi-lo)/2) .* randn(pop, D);
        Q = min(max(Q, lo), hi);
        % --- 精英保留 ---
        [vs, order] = sort([fv; fit(Q)]);
        P = [P; Q]; P = P(order(1:pop), :); fv = vs(1:pop);
    end
    [fbest(s), im] = min(fv); xbest(s,:) = P(im,:);
end

fmean = mean(fbest); fsd = std(fbest); hitrate = mean(abs(fbest - 3) <= tol);
relgap = (fbest - 3) / 3;
out = struct('fbest', fbest, 'xbest', xbest, 'fmean', fmean, 'fsd', fsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'seeds', seeds, 'pop', pop, ...
             'maxgen', maxgen, 'lo', lo, 'hi', hi, 'tol', tol);

fprintf('[ga] 2-D 凸二次（已知最优 f*=3 于 (2,-1)）· pop=%d · maxgen=%d · seeds=%s\n', ...
        pop, maxgen, mat2str(seeds));
for s = 1:numel(seeds)
    fprintf('  seed=%-3d  f_best = %.8g   rel.gap = %+.3e   x = [%.6g %.6g]\n', ...
            seeds(s), fbest(s), relgap(s), xbest(s,1), xbest(s,2));
end
fprintf('  mean ± sd = %.8g ± %.8g   · 命中率(|f-f*|<=%g) = %d/%d\n', ...
        fmean, fsd, tol, sum(abs(fbest - 3) <= tol), numel(seeds));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
