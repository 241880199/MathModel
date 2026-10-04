function out = immune(opts)
%IMMUNE  Clonal-selection artificial immune algorithm on 2-D 凸二次 (known min f*=3 at (2,-1)); zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #8（免疫优化）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `immune`（词首锚定）**0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*immune.*（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch12 免疫优化算法·物流配送中心选址）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     benchmark = 2-D 凸二次  f(x) = 3 + (x1-2)^2 + (x2+1)^2，域 [-10,10]^2，
%     **已知全局最优 f*=3 于 (2,-1)**（**单峰** ⇒ 收敛到该点即"算对"；人造基准，教科书级 `[社区]`）。
%     ★ 固定种子（seeds=1:5）各跑一次，报**逐次读数 + mean±sd + 命中率 + 相对差**；**绝不许"跑一次就宣称达标"**。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/immune.md`。
%
%   用法：
%     immune()             % 自检并打印分布读数
%     out = immune(opts)   % opts.pop opts.maxgen opts.q opts.seeds opts.tol
%
%   返回 struct：fbest, xbest, fmean, fsd, hitrate, relgap, seeds, pop, maxgen, lo, hi, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
D      = 2;
lo = -10; hi = 10;
pop    = dflt(opts, 'pop', 40);
maxgen = dflt(opts, 'maxgen', 150);
q      = dflt(opts, 'q', 10);        % 每代选择的前 q 个抗体克隆
seeds  = dflt(opts, 'seeds', 1:5);
tol    = dflt(opts, 'tol', 1e-4);
fit = @(x) 3 + (x(:,1) - 2).^2 + (x(:,2) + 1).^2;     % 已知最优 f*=3 于 (2,-1)

fbest = zeros(1, numel(seeds)); xbest = zeros(numel(seeds), D);
for s = 1:numel(seeds)
    rng(seeds(s));                                  % ★ 固定种子（可复现）
    Ab = lo + (hi - lo) .* rand(pop, D);
    fAb = fit(Ab);
    for it = 1:maxgen
        [fs, order] = sort(fAb); Ab = Ab(order, :); fAb = fs;
        pool = Ab; fpool = fAb;                     % 精英保留：原始抗体全进池
        for i = 1:q
            nc = max(1, round(pop * (q - i + 1) / q));   % 排名越靠前克隆越多
            sigma = 0.05 + 0.4 * (i / q);                % 排名越靠前变异越小（亲和度成熟）
            c = repmat(Ab(i, :), nc, 1) + sigma * randn(nc, D);
            c = min(max(c, lo), hi);
            pool = [pool; c]; fpool = [fpool; fit(c)];   %#ok<AGROW>
        end
        [fs2, order2] = sort(fpool);
        Ab = pool(order2(1:pop), :); fAb = fs2(1:pop);
    end
    [fbest(s), im] = min(fAb); xbest(s, :) = Ab(im, :);
end

fmean = mean(fbest); fsd = std(fbest); hitrate = mean(abs(fbest - 3) <= tol);
relgap = (fbest - 3) / 3;
out = struct('fbest', fbest, 'xbest', xbest, 'fmean', fmean, 'fsd', fsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'seeds', seeds, 'pop', pop, ...
             'maxgen', maxgen, 'lo', lo, 'hi', hi, 'tol', tol);

fprintf('[immune] 2-D 凸二次（已知最优 f*=3 于 (2,-1)）· pop=%d · maxgen=%d · q=%d · seeds=%s\n', ...
        pop, maxgen, q, mat2str(seeds));
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
