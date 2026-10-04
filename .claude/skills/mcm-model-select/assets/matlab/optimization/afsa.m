function out = afsa(opts)
%AFSA  Artificial fish swarm algorithm on 2-D 凸二次 (known min f*=3 at (2,-1)); zero-arg.
%
%   M4 `mcm-model-select` 骨架 · optimization #10（人工鱼群）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `artificial fish` / `fish swarm` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*(artificial fish|fish swarm)（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/MATLAB智能算法30个案例分析/`（ch18 基于鱼群算法的函数寻优）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 4 类：已知最优解的小算例 + 固定种子 + 多次运行的分布）：
%     benchmark = 2-D 凸二次  f(x) = 3 + (x1-2)^2 + (x2+1)^2，域 [-10,10]^2，
%     **已知全局最优 f*=3 于 (2,-1)**（**单峰** ⇒ 收敛到该点即"算对"；人造基准，教科书级 `[社区]`）。
%     ★ 固定种子（seeds=1:5）各跑一次，报**逐次读数 + mean±sd + 命中率 + 相对差**；**绝不许"跑一次就宣称达标"**。
%   ★ 逐次读数与命中率见 `tests/skills/model-select/verify/afsa.md`。
%
%   用法：
%     afsa()             % 自检并打印分布读数
%     out = afsa(opts)   % opts.nfish opts.maxgen opts.visual opts.step opts.seeds opts.tol
%
%   返回 struct：fbest, xbest, fmean, fsd, hitrate, relgap, seeds, nfish, maxgen, lo, hi, tol。

if nargin < 1 || isempty(opts); opts = struct(); end
D      = 2;
lo = -10; hi = 10;
nfish    = dflt(opts, 'nfish', 40);
maxgen   = dflt(opts, 'maxgen', 300);
visual0  = dflt(opts, 'visual', 2.0);
step0    = dflt(opts, 'step', 0.7);
crowd    = dflt(opts, 'crowd', 0.6);
try_n    = dflt(opts, 'try_n', 8);
seeds    = dflt(opts, 'seeds', 1:5);
tol      = dflt(opts, 'tol', 1e-4);
fit = @(x) 3 + (x(:,1) - 2).^2 + (x(:,2) + 1).^2;     % 已知最优 f*=3 于 (2,-1)

fbest = zeros(1, numel(seeds)); xbest = zeros(numel(seeds), D);
for s = 1:numel(seeds)
    rng(seeds(s));                                  % ★ 固定种子（可复现）
    X = lo + (hi - lo) .* rand(nfish, D); fX = fit(X);
    [bestf, ib] = min(fX); bestx = X(ib, :);
    for it = 1:maxgen
        visual = visual0 * (1 - it/maxgen) + 0.05;   % 视野随代数收缩
        step   = step0   * (1 - it/maxgen) + 0.02;   % 步长随代数收缩
        for i = 1:nfish
            d  = sqrt(sum((X - X(i,:)).^2, 2));
            nb = find(d > 0 & d < visual);
            moved = false;
            % 1) 聚群（swarm）：向邻居中心移动（中心更优且不拥挤）——
            if ~isempty(nb)
                center = mean(X(nb,:), 1);
                if fit(center) < fX(i) && numel(nb)/nfish < crowd
                    X(i,:) = X(i,:) + step*rand*(center - X(i,:)); moved = true;
                end
            end
            % 2) 追尾（follow）：向邻居中最优者移动 ——
            if ~moved && ~isempty(nb)
                [fm, jm] = min(fX(nb));
                if fm < fX(i)
                    X(i,:) = X(i,:) + step*rand*(X(nb(jm),:) - X(i,:)); moved = true;
                end
            end
            % 3) 觅食（prey）：随机试探，有更优则前移 ——
            if ~moved
                for t = 1:try_n
                    Xj = X(i,:) + visual*randn(1, D); Xj = min(max(Xj, lo), hi);
                    if fit(Xj) < fX(i)
                        X(i,:) = X(i,:) + step*rand*(Xj - X(i,:)); moved = true; break;
                    end
                end
            end
            if ~moved; X(i,:) = X(i,:) + step*randn(1, D); end   % 随机行为
            X(i,:) = min(max(X(i,:), lo), hi);
            fX(i) = fit(X(i,:));
        end
        [fb, ib] = min(fX);
        if fb < bestf; bestf = fb; bestx = X(ib, :); end         % 全局最优记忆
    end
    fbest(s) = bestf; xbest(s, :) = bestx;
end

fmean = mean(fbest); fsd = std(fbest); hitrate = mean(abs(fbest - 3) <= tol);
relgap = (fbest - 3) / 3;
out = struct('fbest', fbest, 'xbest', xbest, 'fmean', fmean, 'fsd', fsd, ...
             'hitrate', hitrate, 'relgap', relgap, 'seeds', seeds, 'nfish', nfish, ...
             'maxgen', maxgen, 'lo', lo, 'hi', hi, 'tol', tol);

fprintf('[afsa] 2-D 凸二次（已知最优 f*=3 于 (2,-1)）· nfish=%d · maxgen=%d · seeds=%s\n', ...
        nfish, maxgen, mat2str(seeds));
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
