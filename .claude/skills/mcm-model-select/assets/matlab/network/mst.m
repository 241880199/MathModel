function out = mst(opts)
%MST  Kruskal minimum spanning tree on a 5-node undirected weighted graph.
%   Hand example: MST weight = 11; edges {3-4(1), 1-2(2), 2-3(3), 4-5(5)}.
%
%   M4 `mcm-model-select` 骨架 · network #2（最小生成树）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@mst` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：
%     5 节点、7 条边：1-2:2 · 2-3:3 · 3-4:1 · 4-5:5 · 1-3:4 · 2-4:6 · 3-5:7。
%     Kruskal 按权升序合并（避环）：取 3-4(1) · 1-2(2) · 2-3(3) · 4-5(5) ⇒ 总权 = 11
%     （手算合并序见 verify/mst.md）。★ 不调用 MATLAB `minspantree`（同机实现不作独立参照）。
%
%   用法：
%     mst()             % 自检并打印读数
%     out = mst(opts)   % opts.E（[u v w] 三列）· opts.n
%
%   返回 struct：weight, edges（[u v w]，按加入序）。

if nargin < 1 || isempty(opts); opts = struct(); end
E = dflt(opts, 'E', [1 2 2; 2 3 3; 3 4 1; 4 5 5; 1 3 4; 2 4 6; 3 5 7]);
n = dflt(opts, 'n', 5);

[~, idx] = sort(E(:, 3));
E = E(idx, :);
parent = 1:n;
sel = zeros(0, 3);
for k = 1:size(E, 1)
    a = findroot(parent, E(k, 1));
    b = findroot(parent, E(k, 2));
    if a ~= b
        parent(a) = b;                 % union
        sel(end + 1, :) = E(k, :);     %#ok<AGROW>
        if size(sel, 1) == n - 1; break; end
    end
end
weight = sum(sel(:, 3));

out = struct('weight', weight, 'edges', sel);

fprintf('[mst] Kruskal on a %d-node graph (%d edges)\n', n, size(E, 1));
fprintf('  MST edges (u-v, w): %s\n', edge_str(sel));
fprintf('  MST weight = %g\n', weight);
fprintf('  hand-computed MST weight = 11   =>  %s\n', ...
        ternary(weight == 11, 'MATCH', 'MISMATCH'));
end

function r = findroot(parent, x)
while parent(x) ~= x; x = parent(x); end
r = x;
end

function s = edge_str(sel)
parts = arrayfun(@(i) sprintf('%d-%d (%g)', sel(i, 1), sel(i, 2), sel(i, 3)), ...
                 1:size(sel, 1), 'UniformOutput', false);
s = strjoin(parts, ' · ');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
