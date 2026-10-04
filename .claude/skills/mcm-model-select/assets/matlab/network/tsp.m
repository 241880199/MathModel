function out = tsp(opts)
%TSP  Travelling salesman by brute-force permutation (small n only).
%   Hand example: 5-city symmetric distance matrix; optimal tour cost = 22
%   (route 1-2-4-3-5-1: 2+4+8+3+5 = 22).
%
%   M4 `mcm-model-select` 骨架 · network #11（旅行商 TSP）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@tsp` 类目录撞名（实测 2026-10-04）。
%   ★ 归档里 `corpus/algorithms/src/GraphTheory(图论)/basic/grTravSale.m`（grTheory）
%     被 `corpus/algorithms/INDEX.md` §10.5 记为**在 R2025b 不可用** —— **不拿它当参照**。
%
%   独立参照（第 3 类：手算小图）：n=5 时**全排列穷举**（4!/2 = 12 条不同巡回），
%     手算最优 = 22（两条对称最优巡回 1-2-4-3-5-1 与反向，见 verify/tsp.md）。**本骨架=穷举实现**。
%   ★ 穷举只适用小 n；大规模须走启发式（`references/optimization/aco.md` 等）。
%
%   用法：
%     tsp()             % 自检并打印读数
%     out = tsp(opts)   % opts.D（距离矩阵）
%
%   返回 struct：best, tour。

if nargin < 1 || isempty(opts); opts = struct(); end
D = dflt(opts, 'D', [0 2 9 10 5; ...
                     2 0 6 4 8; ...
                     9 6 0 8 3; ...
                     10 4 8 0 5; ...
                     5 8 3 5 0]);
n = size(D, 1);
P = perms(2:n);
best = inf; bestTour = [];
for i = 1:size(P, 1)
    tour = [1 P(i, :) 1];
    c = 0;
    for k = 1:n; c = c + D(tour(k), tour(k + 1)); end
    if c < best; best = c; bestTour = tour; end
end

out = struct('best', best, 'tour', bestTour);

fprintf('[tsp] brute force over %d-city tours (%d permutations)\n', n, size(P, 1));
fprintf('  optimal tour cost = %g\n', best);
fprintf('  best route: %s\n', num2str(bestTour, '%d '));
fprintf('  hand-computed optimal tour cost = 22   =>  %s\n', ...
        ternary(best == 22, 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
