function out = coloring(opts)
%COLORING  Greedy vertex coloring (Welsh-Powell order) on a small graph.
%   Hand example: 5-cycle C5 (1-2-3-4-5-1); greedy uses 3 colors,
%   colors = [1 2 1 2 3]; chi(C5) = 3 (odd cycle).
%
%   M4 `mcm-model-select` 骨架 · network #6（染色）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@coloring` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：C5 是奇环 ⇒ 色数 chi = 3（手算见 verify/coloring.md）。
%   ★ 贪心只给**上界**；本算例上界恰达到最优（3）。一般图贪心可能多于 chi。
%
%   用法：
%     coloring()             % 自检并打印读数
%     out = coloring(opts)   % opts.A（邻接矩阵）
%
%   返回 struct：colors, ncolors。

if nargin < 1 || isempty(opts); opts = struct(); end
A = dflt(opts, 'A', [0 1 0 0 1; ...
                     1 0 1 0 0; ...
                     0 1 0 1 0; ...
                     0 0 1 0 1; ...
                     1 0 0 1 0]);
n = size(A, 1);

deg = sum(A > 0, 2);
[~, order] = sort(deg, 'descend');       % Welsh-Powell：按度降序（并列按原序）
colors = zeros(1, n);
for u = order(:)'
    used = colors(A(u, :) > 0);
    c = 1;
    while any(used == c); c = c + 1; end
    colors(u) = c;
end
ncolors = max(colors);

out = struct('colors', colors, 'ncolors', ncolors);

fprintf('[coloring] greedy (Welsh-Powell) on a %d-node graph\n', n);
fprintf('  colors = [%s]\n', num2str(colors, '%d '));
fprintf('  number of colors = %d\n', ncolors);
fprintf('  hand-computed chi(C5) = 3, colors [1 2 1 2 3]   =>  %s\n', ...
        ternary(ncolors == 3 && isequal(colors, [1 2 1 2 3]), 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
