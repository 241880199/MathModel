function out = shortest_path(opts)
%SHORTEST_PATH  Dijkstra single-source shortest paths on a 5-node undirected
%   weighted graph. Hand example: distances from node 1 = [0 3 2 8 10]
%   (shortest path to node 5 is 1-3-2-4-5, cost 2+1+5+2 = 10).
%
%   M4 `mcm-model-select` 骨架 · network #1（最短路）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@shortest_path` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：
%     5 节点无向赋权图，边：1-2:4 · 1-3:2 · 2-3:1 · 2-4:5 · 3-4:8 · 3-5:10 · 4-5:2。
%     从节点 1 出发 Dijkstra 逐点松弛 ⇒ dist = [0 3 2 8 10]（手算逐位见 verify/shortest_path.md）。
%   ★ 本骨架**自写 Dijkstra**（不调用 MATLAB `graph` / `shortestpath`）——
%     同机内置实现**不构成独立参照**（任务书 B）；参照走**手算小图**。
%
%   用法：
%     shortest_path()             % 自检并打印读数
%     out = shortest_path(opts)   % opts.W（邻接矩阵，0=无边）· opts.src
%
%   返回 struct：dist, prev, path, target。

if nargin < 1 || isempty(opts); opts = struct(); end
W = dflt(opts, 'W', [0 4 2 0 0; ...
                     4 0 1 5 0; ...
                     2 1 0 8 10; ...
                     0 5 8 0 2; ...
                     0 0 10 2 0]);
src = dflt(opts, 'src', 1);

n = size(W, 1);
dist = inf(1, n);
dist(src) = 0;
prev = zeros(1, n);
done = false(1, n);
for it = 1:n
    d = dist; d(done) = inf;
    [~, u] = min(d);
    if isinf(dist(u)); break; end
    done(u) = true;
    for v = 1:n
        if W(u, v) > 0 && ~done(v)
            nd = dist(u) + W(u, v);
            if nd < dist(v)
                dist(v) = nd;
                prev(v) = u;
            end
        end
    end
end

% 回溯到目标（默认最后一个节点）的路径
target = n;
path = target;
while path(1) ~= src && prev(path(1)) ~= 0
    path = [prev(path(1)) path];
end

out = struct('dist', dist, 'prev', prev, 'path', path, 'target', target);

fprintf('[shortest_path] Dijkstra from node %d on a %d-node undirected graph\n', src, n);
fprintf('  dist = [%s]\n', num2str(dist, '%g '));
fprintf('  path to node %d: %s  (cost %g)\n', target, num2str(path, '%d '), dist(target));
fprintf('  hand-computed dist = [0 3 2 8 10]   =>  %s\n', ...
        ternary(max(abs(dist - [0 3 2 8 10])) < 1e-9, 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
