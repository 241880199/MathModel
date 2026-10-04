function out = matching(opts)
%MATCHING  Maximum bipartite matching via augmenting paths (Kuhn's algorithm).
%   Hand example: left {1,2,3} · right {4,5,6}; edges 1-4,1-5,2-4,3-5,3-6;
%   maximum matching size = 3 (e.g. {1-5, 2-4, 3-6}).
%
%   M4 `mcm-model-select` 骨架 · network #5（匹配与覆盖）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@matching` 类目录撞名（实测 2026-10-04）。
%   ★ `propensity score matching`（倾向得分匹配）是**统计方法**，**不是图匹配** —— 别混。
%
%   独立参照（第 3 类：手算小图）：二分图最大匹配**手算**为 3
%     （逐条增广路见 verify/matching.md）；由 Kőnig 定理，二分图最小点覆盖 = 最大匹配 = 3。
%   ★ 覆盖族的变体（最小点/边覆盖 · 最大独立集 · 团）在同一族的算法里；本骨架实现**匹配**这一支。
%
%   用法：
%     matching()             % 自检并打印读数
%     out = matching(opts)   % opts.adj（左侧 u -> 右侧邻居）· opts.nR
%
%   返回 struct：size, matchR（右侧 -> 左侧）。

if nargin < 1 || isempty(opts); opts = struct(); end
adj = dflt(opts, 'adj', {[1 2], [1], [2 3]});    % 右侧用 1..nR 编号（= 原图节点 4..6）
nR = dflt(opts, 'nR', 3);
nL = numel(adj);

matchR = zeros(1, nR);
for u = 1:nL
    seen = false(1, nR);
    [matchR, ~] = kuhn(u, adj, matchR, seen);
end
sz = sum(matchR > 0);

pairs = zeros(sz, 2);
k = 0;
for r = 1:nR
    if matchR(r) > 0; k = k + 1; pairs(k, :) = [matchR(r) r + 3]; end
end

out = struct('size', sz, 'matchR', matchR, 'pairs', pairs);

fprintf('[matching] maximum bipartite matching (left 1..3, right 4..6)\n');
fprintf('  matching size = %d\n', sz);
fprintf('  pairs (L-R): %s\n', pair_str(pairs));
fprintf('  hand-computed maximum matching = 3   =>  %s\n', ...
        ternary(sz == 3, 'MATCH', 'MISMATCH'));
end

function [matchR, ok] = kuhn(u, adj, matchR, seen)
ok = false;
for r = adj{u}
    if ~seen(r)
        seen(r) = true;
        if matchR(r) == 0
            matchR(r) = u; ok = true; return;
        else
            [matchR, ok2] = kuhn(matchR(r), adj, matchR, seen);
            if ok2; matchR(r) = u; ok = true; return; end
        end
    end
end
end

function s = pair_str(pairs)
parts = arrayfun(@(i) sprintf('%d-%d', pairs(i, 1), pairs(i, 2)), ...
                 1:size(pairs, 1), 'UniformOutput', false);
s = strjoin(parts, ' · ');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
