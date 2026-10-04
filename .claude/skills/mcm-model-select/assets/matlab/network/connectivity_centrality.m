function out = connectivity_centrality(opts)
%CONNECTIVITY_CENTRALITY  Connected components + degree centrality on a graph.
%   Hand example: edges 1-2,2-3,1-3,4-5 => 2 components;
%   degrees [2 2 2 1 1] => degree centrality [0.5 0.5 0.5 0.25 0.25].
%
%   M4 `mcm-model-select` 骨架 · network #9（连通性 / 中心性）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@connectivity_centrality` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：分量数**手算**为 2（三角形 + 一条边）；度中心性**手算**
%     为 deg/(n-1) = [2 2 2 1 1]/4（见 verify/connectivity_centrality.md）。
%
%   用法：
%     connectivity_centrality()             % 自检并打印读数
%     out = connectivity_centrality(opts)   % opts.A（邻接矩阵）
%
%   返回 struct：ncomp, comp, degree, degree_centrality。

if nargin < 1 || isempty(opts); opts = struct(); end
A = dflt(opts, 'A', [0 1 1 0 0; ...
                     1 0 1 0 0; ...
                     1 1 0 0 0; ...
                     0 0 0 0 1; ...
                     0 0 0 1 0]);
n = size(A, 1);

comp = zeros(1, n); ncomp = 0;
for u = 1:n
    if comp(u) == 0
        ncomp = ncomp + 1;
        q = u; comp(u) = ncomp;
        while ~isempty(q)
            x = q(1); q(1) = [];
            for v = find(A(x, :) > 0)
                if comp(v) == 0; comp(v) = ncomp; q(end + 1) = v; end   %#ok<AGROW>
            end
        end
    end
end

degree = sum(A > 0, 2)';
degcent = degree / (n - 1);

out = struct('ncomp', ncomp, 'comp', comp, 'degree', degree, ...
             'degree_centrality', degcent);

fprintf('[connectivity_centrality] %d-node graph (edges 1-2,2-3,1-3,4-5)\n', n);
fprintf('  connected components = %d\n', ncomp);
fprintf('  component label = [%s]\n', num2str(comp, '%d '));
fprintf('  degrees = [%s]   degree centrality = [%s]\n', ...
        num2str(degree, '%g '), num2str(degcent, '%g '));
fprintf('  hand-computed: 2 components, degree centrality [0.5 0.5 0.5 0.25 0.25]   =>  %s\n', ...
        ternary(ncomp == 2 && isequal(degcent, [0.5 0.5 0.5 0.25 0.25]), 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
