function out = euler_hamilton(opts)
%EULER_HAMILTON  Euler circuit (Hierholzer) + Hamiltonian cycle (backtracking).
%   Hand example: Euler graph (edges 1-2,2-3,3-1,3-4,4-5,5-3; all degrees even)
%   => Euler circuit 1-2-3-4-5-3-1; Hamilton graph C5 => cycle 1-2-3-4-5-1.
%
%   M4 `mcm-model-select` 骨架 · network #8（欧拉图 / Hamilton 图）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@euler_hamilton` 类目录撞名（实测 2026-10-04）。
%   ★ 归档里 `corpus/algorithms/src/GraphTheory(图论)/detailed/Euler图和Hamilton图/Fleuf1.m`
%     被 `corpus/algorithms/INDEX.md` §10.1 登记为**给出非法欧拉回路**（确证算法性缺陷）；
%     **净室重写版**在 `corpus/algorithms/fixed/euler_circuit.m`（可作**第 2 类**交叉参照的候选，
%     但本算例**首选手算**，见 verify/euler_hamilton.md）。**不拿 Fleuf1.m 当参照**。
%
%   独立参照（第 3 类：手算小图）：欧拉回路**存在性 + 合法性**（每边一次、闭合）手算；
%     Hamilton 回路在 C5 上手算为 1-2-3-4-5-1。
%
%   用法：
%     euler_hamilton()             % 自检并打印读数
%     out = euler_hamilton(opts)   % opts.AE（欧拉图邻接·可多重）· opts.AH（Hamilton 图邻接）
%
%   返回 struct：euler, hamilton。

if nargin < 1 || isempty(opts); opts = struct(); end
AE = dflt(opts, 'AE', [0 1 1 0 0; ...
                       1 0 1 0 0; ...
                       1 1 0 1 1; ...
                       0 0 1 0 1; ...
                       0 0 1 1 0]);
AH = dflt(opts, 'AH', [0 1 0 0 1; ...
                       1 0 1 0 0; ...
                       0 1 0 1 0; ...
                       0 0 1 0 1; ...
                       1 0 0 1 0]);

nE = size(AE, 1);
evenOk = all(mod(sum(AE > 0, 2), 2) == 0);
euler = [];
if evenOk
    euler = hierholzer(AE, 1);
end

nH = size(AH, 1);
path = 1; vis = false(1, nH); vis(1) = true;
[ham, found] = ham_visit(1, AH, nH, path, vis);
if ~found; ham = []; end

out = struct('euler', euler, 'hamilton', ham);

fprintf('[euler_hamilton] Euler graph (all degrees even = %d) + Hamilton graph C5\n', evenOk);
if isempty(euler)
    fprintf('  Euler circuit: (none - degrees not all even)\n');
else
    fprintf('  Euler circuit: %s\n', num2str(euler, '%d '));
end
if isempty(ham)
    fprintf('  Hamiltonian cycle: (none)\n');
else
    fprintf('  Hamiltonian cycle: %s\n', num2str(ham, '%d '));
end
fprintf('  hand-computed: Euler 1 2 3 4 5 3 1 · Hamilton 1 2 3 4 5 1   =>  %s\n', ...
        ternary(isequal(euler, [1 2 3 4 5 3 1]) && isequal(ham, [1 2 3 4 5 1]), 'MATCH', 'MISMATCH'));
end

function circ = hierholzer(A, start)
A = double(A > 0);
circ = []; stack = start;
while ~isempty(stack)
    u = stack(end);
    nbrs = find(A(u, :) > 0);
    if isempty(nbrs)
        circ(end + 1) = u;                    %#ok<AGROW>
        stack(end) = [];
    else
        v = nbrs(1);
        A(u, v) = A(u, v) - 1; A(v, u) = A(v, u) - 1;
        stack(end + 1) = v;                   %#ok<AGROW>
    end
end
circ = fliplr(circ);
end

function [path, found] = ham_visit(v, A, n, path, vis)
found = false;
if numel(path) == n
    if A(v, path(1)); path(end + 1) = path(1); found = true; end
    return;
end
for u = 1:n
    if A(v, u) && ~vis(u)
        vis(u) = true; path(end + 1) = u;                 %#ok<AGROW>
        [path, found] = ham_visit(u, A, n, path, vis);
        if found; return; end
        path(end) = []; vis(u) = false;
    end
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
