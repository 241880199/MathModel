function out = min_cost_flow(opts)
%MIN_COST_FLOW  Successive-shortest-path minimum-cost flow on a 4-node network.
%   Hand example: s=1, t=4, demand = 4 units; minimum cost = 13.
%
%   M4 `mcm-model-select` 骨架 · network #4（最小费用流）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@min_cost_flow` 类目录撞名（实测 2026-10-04）。
%
%   ★★ 上游缺陷（必须知道）：归档里的 `corpus/algorithms/src/GraphTheory(图论)/detailed/最小费用流/BGf.m`
%     被 `corpus/algorithms/INDEX.md` §10.1 登记为**确证算法性缺陷** —— **在 6 点 10 弧的网络上
%     传入即不终止**（>500 s，正常应毫秒级；小实例正确）。⇒ 本骨架**自写正确版**（SSP + Bellman-Ford），
%     **不拿 BGf.m 当参照**。出处：`corpus/algorithms/INDEX.md` §10.1。
%
%   独立参照（第 3 类：手算小图）：
%     4 节点有向网络（源 1、汇 4），弧 (cap, cost)：1->2:(3,1) · 1->3:(2,2) · 2->3:(2,1) · 2->4:(2,3) · 3->4:(3,1)。
%     供 4 单位 ⇒ 手算最小费用 = 13（逐项推导见 verify/min_cost_flow.md）。
%   ★ 不调用 MATLAB 内置求解器当参照。
%
%   用法：
%     min_cost_flow()             % 自检并打印读数
%     out = min_cost_flow(opts)   % opts.E（[u v cap cost]）· opts.s · opts.t · opts.demand
%
%   返回 struct：cost, flow, demand。

if nargin < 1 || isempty(opts); opts = struct(); end
E = dflt(opts, 'E', [1 2 3 1; ...
                     1 3 2 2; ...
                     2 3 2 1; ...
                     2 4 2 3; ...
                     3 4 3 1]);
s = dflt(opts, 's', 1);
t = dflt(opts, 't', 4);
demand = dflt(opts, 'demand', 4);

m = size(E, 1);
N = max(E(:, 1:2), [], 'all');
cap = [E(:, 3); zeros(m, 1)];        % 前 m 条为正向弧，后 m 条为反向（初始 0）
cst = [E(:, 4); -E(:, 4)];
uf = [E(:, 1); E(:, 2)];             % 反向弧 i+m：from=v_i
vf = [E(:, 2); E(:, 1)];             %              to  =u_i
flow = zeros(1, m);
totalCost = 0;
totalFlow = 0;
while totalFlow < demand
    [dist, pre] = bellman_ford(N, 2 * m, uf, vf, cap, cst, s);
    if isinf(dist(t)); break; end            % 无更省增广路 ⇒ 停
    b = demand - totalFlow; v = t;
    while v ~= s
        e = pre(v);
        b = min(b, cap(e));
        v = uf(e);
    end
    v = t;
    while v ~= s
        e = pre(v);
        cap(e) = cap(e) - b;
        partner = e + m; if e > m; partner = e - m; end
        cap(partner) = cap(partner) + b;
        if e <= m; flow(e) = flow(e) + b; else; flow(e - m) = flow(e - m) - b; end
        totalCost = totalCost + b * cst(e);
        v = uf(e);
    end
    totalFlow = totalFlow + b;
end

out = struct('cost', totalCost, 'flow', flow, 'demand', demand);

fprintf('[min_cost_flow] SSP (Bellman-Ford) s=%d t=%d demand=%d on a %d-node network\n', ...
        s, t, demand, N);
fprintf('  delivered flow = %g\n', totalFlow);
fprintf('  minimum cost  = %g\n', totalCost);
fprintf('  hand-computed minimum cost = 13   =>  %s\n', ...
        ternary(totalCost == 13, 'MATCH', 'MISMATCH'));
end

function [dist, pre] = bellman_ford(N, ne, uf, vf, cap, cst, s)
dist = inf(1, N);
dist(s) = 0;
pre = zeros(1, N);
for it = 1:N - 1
    changed = false;
    for e = 1:ne
        if cap(e) > 0 && dist(uf(e)) < inf && dist(uf(e)) + cst(e) < dist(vf(e))
            dist(vf(e)) = dist(uf(e)) + cst(e);
            pre(vf(e)) = e;
            changed = true;
        end
    end
    if ~changed; break; end
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
