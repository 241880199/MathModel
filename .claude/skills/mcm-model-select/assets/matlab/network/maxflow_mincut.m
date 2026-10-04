function out = maxflow_mincut(opts)
%MAXFLOW_MINCUT  Edmonds-Karp maximum flow / minimum cut on a 5-node directed
%   network. Hand example: s=1, t=4; max flow = 5 = min cut capacity.
%
%   M4 `mcm-model-select` 骨架 · network #3（最大流 / 最小割）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@maxflow_mincut` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：
%     5 节点有向网络（源 1、汇 4），容量：1->2:3 · 1->3:2 · 2->3:1 · 2->4:2 · 3->4:4。
%     手算最小割 S={1,2} ⇒ 割容量 1->3(2)+2->3(1)+2->4(2) = 5 ⇒ 最大流 = 5
%     （手算见 verify/maxflow_mincut.md）。★ 不调用 MATLAB `maxflow`（同机实现不作独立参照）。
%
%   用法：
%     maxflow_mincut()             % 自检并打印读数
%     out = maxflow_mincut(opts)   % opts.C（容量矩阵）· opts.s · opts.t
%
%   返回 struct：maxflow, mincut, flow（流量矩阵）。

if nargin < 1 || isempty(opts); opts = struct(); end
C = dflt(opts, 'C', [0 3 2 0 0; ...
                     0 0 1 2 0; ...
                     0 0 0 4 0; ...
                     0 0 0 0 0; ...
                     0 0 0 0 0]);
s = dflt(opts, 's', 1);
t = dflt(opts, 't', 4);

n = size(C, 1);
F = zeros(n, n);                 % 流量
maxflow = 0;
while true
    [parent, ok] = bfs_path(C - F, s, t, n);   % 残量网络 BFS 增广路
    if ~ok; break; end
    % 沿路径找瓶颈
    bottleneck = inf; v = t;
    while v ~= s
        u = parent(v);
        bottleneck = min(bottleneck, C(u, v) - F(u, v));
        v = u;
    end
    v = t;
    while v ~= s
        u = parent(v);
        F(u, v) = F(u, v) + bottleneck;
        F(v, u) = F(v, u) - bottleneck;
        v = u;
    end
    maxflow = maxflow + bottleneck;
end

% 由残量网络取最小割：从 s 可达的节点集为 S
[~, ~, reach] = bfs_path(C - F, s, [], n);
mincut = 0;
for u = 1:n
    for v = 1:n
        if reach(u) && ~reach(v) && C(u, v) > 0
            mincut = mincut + C(u, v);
        end
    end
end

out = struct('maxflow', maxflow, 'mincut', mincut, 'flow', F);

fprintf('[maxflow_mincut] Edmonds-Karp, s=%d t=%d on a %d-node network\n', s, t, n);
fprintf('  max flow = %g\n', maxflow);
fprintf('  min cut  = %g\n', mincut);
fprintf('  hand-computed max flow = 5 = min cut   =>  %s\n', ...
        ternary(maxflow == 5 && mincut == 5, 'MATCH', 'MISMATCH'));
end

function [parent, ok, reach] = bfs_path(res, s, t, n)
parent = zeros(1, n);
reach = false(1, n);
reach(s) = true;
q = s;
ok = false;
while ~isempty(q)
    u = q(1); q(1) = [];
    if ~isempty(t) && u == t; ok = true; return; end
    for v = 1:n
        if res(u, v) > 0 && ~reach(v)
            reach(v) = true;
            parent(v) = u;
            q(end + 1) = v;        %#ok<AGROW>
        end
    end
end
if isempty(t)
    ok = true;                     % 只要可达集（最小割用）
else
    ok = reach(t);
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
