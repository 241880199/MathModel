function out = pso(opts)
%PSO  Particle swarm optimization on 2-D 凸二次 (known min f*=3 at (2,-1)); zero-arg.
%
%   M4 `mcm-model-select` 骨架 · optimization #7（粒子群 PSO）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `particle swarm optimization` 命中 **3 行**
%   （`:42` 2 篇 · `:93` 1 篇 · `:171` 1 篇；**去重并集 = 4 篇**：P2025-A-01/A-04/B-01/C-12；
%   2026-10-04 当场复跑 `grep -nE "^ +- particle swarm optimization（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md`）。
%   **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch10/ch13–ch17 PSO 系列）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     benchmark = 2-D 凸二次  f(x) = 3 + (x1-2)^2 + (x2+1)^2，域 [-10,10]^2，
%     **已知全局最优 f*=3 于 (2,-1)**（**单峰** ⇒ 收敛到该点即"算对"；人造基准，教科书级 `[社区]`）。
%     ★ 固定种子（seeds=1:5）各跑一次，报**逐次读数 + mean±sd + 命中率 + 相对差**；**绝不许"跑一次就宣称达标"**。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/pso.md`。
%
%   用法：
%     pso()             % 自检并打印分布读数
%     out = pso(opts)   % opts.pop opts.maxgen opts.w opts.c1 opts.c2 opts.seeds opts.tol
%
%   返回 struct：fbest, xbest, fmean, fsd, hitrate, relgap, seeds, pop, maxgen, lo, hi, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
D      = 2;
lo = -10; hi = 10;
pop    = dflt(opts, 'pop', 40);
maxgen = dflt(opts, 'maxgen', 150);
w      = dflt(opts, 'w', 0.7);
c1     = dflt(opts, 'c1', 1.5);
c2     = dflt(opts, 'c2', 1.5);
seeds  = dflt(opts, 'seeds', 1:5);
tol    = dflt(opts, 'tol', 1e-4);
fit = @(x) 3 + (x(:,1) - 2).^2 + (x(:,2) + 1).^2;     % 已知最优 f*=3 于 (2,-1)

fbest = zeros(1, numel(seeds)); xbest = zeros(numel(seeds), D);
for s = 1:numel(seeds)
    rng(seeds(s));                                  % ★ 固定种子（可复现）
    X = lo + (hi - lo) .* rand(pop, D);
    V = zeros(pop, D);
    pbest = X; pbestf = fit(X);
    [gbestf, im] = min(pbestf); gbest = pbest(im, :);
    for it = 1:maxgen
        r1 = rand(pop, D); r2 = rand(pop, D);
        V = w*V + c1*r1.*(pbest - X) + c2*r2.*(gbest - X);
        X = min(max(X + V, lo), hi);
        fx = fit(X);
        imp = fx < pbestf;
        pbest(imp, :) = X(imp, :); pbestf(imp) = fx(imp);
        [gbestf, im] = min(pbestf); gbest = pbest(im, :);
    end
    fbest(s) = gbestf; xbest(s, :) = gbest;
end

fmean = mean(fbest); fsd = std(fbest); hitrate = mean(abs(fbest - 3) <= tol);
relgap = (fbest - 3) / 3;
out = struct('fbest', fbest, 'xbest', xbest, 'fmean', fmean, 'fsd', fsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'seeds', seeds, 'pop', pop, ...
             'maxgen', maxgen, 'lo', lo, 'hi', hi, 'tol', tol);

fprintf('[pso] 2-D 凸二次（已知最优 f*=3 于 (2,-1)）· pop=%d · maxgen=%d · seeds=%s\n', ...
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
