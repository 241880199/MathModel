function out = ga_variants(opts)
%GA_VARIANTS  Multiple-population (island-model) GA on 2-D 凸二次 (known min f*=3 at (2,-1)); zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #11（遗传算法变体 —— 多种群 / 量子 / 混合）。文件名全 ASCII（GC5）。
%   ★ **本骨架实现"多种群（island / 并行）"这一变体**（种群分岛、定期迁移、共享最优）；
%     量子 GA / 混合 GA 属同类变体，接口与"已知最优 benchmark + 固定种子 + 分布"的参照口径相同。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里与本变体同族的命中：
%     `NSGA-II`（`:70` 2 篇）· `multi-objective optimization`（`:66` 4 篇 · `:244` 1 篇，去重 5 篇）·
%     `differential evolution`（`:241` 1 篇）· `A* and GA`（`:193` 1 篇）；
%   2026-10-04 当场复跑 `grep -nE "^ +- (NSGA-II|multi-objective optimization|differential evolution|A\* and GA)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`。
%   **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch7 多种群 · ch8 量子 · ch9 多目标 · ch11 多层编码）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     benchmark = 2-D 凸二次  f(x) = 3 + (x1-2)^2 + (x2+1)^2，域 [-10,10]^2，
%     **已知全局最优 f*=3 于 (2,-1)**（**单峰** ⇒ 收敛到该点即"算对"；人造基准，教科书级 `[社区]`）。
%     ★ 固定种子（seeds=1:5）各跑一次，报**逐次读数 + mean±sd + 命中率 + 相对差**；**绝不许"跑一次就宣称达标"**。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/ga_variants.md`。
%
%   用法：
%     ga_variants()             % 自检并打印分布读数
%     out = ga_variants(opts)   % opts.pop opts.nIsl opts.maxgen opts.migint opts.seeds opts.tol
%
%   返回 struct：fbest, xbest, fmean, fsd, hitrate, relgap, seeds, pop, nIsl, maxgen, lo, hi, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
D       = 2;
lo = -10; hi = 10;
pop     = dflt(opts, 'pop', 40);
nIsl    = dflt(opts, 'nIsl', 4);
maxgen  = dflt(opts, 'maxgen', 150);
migint  = dflt(opts, 'migint', 20);   % 迁移间隔（代）
nMig    = dflt(opts, 'nMig', 2);      % 每次迁移的个体数
pc      = dflt(opts, 'pc', 0.9);
pm      = dflt(opts, 'pm', 0.1);
seeds   = dflt(opts, 'seeds', 1:5);
tol     = dflt(opts, 'tol', 1e-4);
subpop  = max(2, round(pop / nIsl));
fit = @(x) 3 + (x(:,1) - 2).^2 + (x(:,2) + 1).^2;     % 已知最优 f*=3 于 (2,-1)

fbest = zeros(1, numel(seeds)); xbest = zeros(numel(seeds), D);
for s = 1:numel(seeds)
    rng(seeds(s));                                  % ★ 固定种子（可复现）
    P = cell(1, nIsl); fv = cell(1, nIsl);
    for isl = 1:nIsl
        P{isl} = lo + (hi - lo) .* rand(subpop, D); fv{isl} = fit(P{isl});
    end
    for gen = 1:maxgen
        for isl = 1:nIsl
            [P{isl}, fv{isl}] = evolve_island(P{isl}, fv{isl}, fit, pc, pm, gen, maxgen, lo, hi, subpop, D);
        end
        if mod(gen, migint) == 0              % 环状迁移：各岛前 nMig 优者迁往下一岛（替换其最差）
            [P, fv] = migrate(P, fv, nIsl, nMig);
        end
    end
    gall = vertcat(fv{:}); [fbest(s), im] = min(gall);   % ★ vertcat：行 cell 的列向量用 cell2mat 会拼成矩阵
    allx = vertcat(P{:});  xbest(s, :) = allx(im, :);
end

fmean = mean(fbest); fsd = std(fbest); hitrate = mean(abs(fbest - 3) <= tol);
relgap = (fbest - 3) / 3;
out = struct('fbest', fbest, 'xbest', xbest, 'fmean', fmean, 'fsd', fsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'seeds', seeds, 'pop', pop, ...
             'nIsl', nIsl, 'maxgen', maxgen, 'lo', lo, 'hi', hi, 'tol', tol);

fprintf('[ga_variants] 多种群 GA · 2-D 凸二次（已知最优 f*=3 于 (2,-1)）· pop=%d·%d 岛 · maxgen=%d · seeds=%s\n', ...
        pop, nIsl, maxgen, mat2str(seeds));
for s = 1:numel(seeds)
    fprintf('  seed=%-3d  f_best = %.8g   rel.gap = %+.3e   x = [%.6g %.6g]\n', ...
            seeds(s), fbest(s), relgap(s), xbest(s,1), xbest(s,2));
end
fprintf('  mean ± sd = %.8g ± %.8g   · 命中率(|f-f*|<=%g) = %d/%d\n', ...
        fmean, fsd, tol, sum(abs(fbest - 3) <= tol), numel(seeds));
end

% ------------------------------------------------------------------------
function [P, fv] = evolve_island(P, fv, fit, pc, pm, gen, maxgen, lo, hi, subpop, D)
% 岛内一轮：锦标赛选择 + 算术交叉 + 高斯变异 + 精英保留。
ii = randi(subpop, subpop, 2); fpair = fv(ii);
[~, win] = min(fpair, [], 2);
Q = P(ii(sub2ind(size(ii), (1:subpop).', win)), :);
for k = 1:2:subpop-1
    if rand < pc
        lam = rand; a = Q(k,:); b2 = Q(k+1,:);
        Q(k,:) = lam*a + (1-lam)*b2; Q(k+1,:) = (1-lam)*a + lam*b2;
    end
end
sigma = 0.5 * (1 - gen/maxgen) + 0.05;
Q = Q + (rand(subpop, D) < pm) .* (sigma * (hi-lo)/2) .* randn(subpop, D);
Q = min(max(Q, lo), hi);
[vs, order] = sort([fv; fit(Q)]);
P = [P; Q]; P = P(order(1:subpop), :); fv = vs(1:subpop);
end

function [P, fv] = migrate(P, fv, nIsl, nMig)
% 环状迁移：把各岛最好的 nMig 个个体传给下一岛，替换该岛最差的 nMig 个。
newP = P; newF = fv;
for isl = 1:nIsl
    nxt = mod(isl, nIsl) + 1;
    [~, ord] = sort(fv{isl});  src = ord(1:nMig);              % 本岛最优
    [~, ord2] = sort(fv{nxt}, 'descend'); dst = ord2(1:nMig);  % 下一岛最差
    newP{nxt}(dst, :) = P{isl}(src, :); newF{nxt}(dst) = fv{isl}(src);
end
P = newP; fv = newF;
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
