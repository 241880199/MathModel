function out = tree_traversal(opts)
%TREE_TRAVERSAL  BFS / DFS order on a rooted tree + Huffman code lengths.
%   Hand example: tree edges 1-2,1-3,2-4,2-5,3-6 (root 1);
%   BFS order = [1 2 3 4 5 6]; DFS order = [1 2 4 5 3 6];
%   Huffman weights [5 9 12 13 16 45] => code lengths [4 4 3 3 3 1], weighted path length = 224.
%
%   M4 `mcm-model-select` 骨架 · network #7（树 / 遍历 / Huffman）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@tree_traversal` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：BFS / DFS 序**手算**；Huffman 码长**手算**（合并序见 verify/tree_traversal.md）。
%
%   用法：
%     tree_traversal()             % 自检并打印读数
%     out = tree_traversal(opts)   % opts.adj · opts.root · opts.w
%
%   返回 struct：bfs, dfs, lens, wpl。

if nargin < 1 || isempty(opts); opts = struct(); end
adj = dflt(opts, 'adj', {[2 3], [1 4 5], [1 6], [2], [2], [3]});
root = dflt(opts, 'root', 1);
w = dflt(opts, 'w', [5 9 12 13 16 45]);
n = numel(adj);

% BFS
bfs = zeros(1, 0); visited = false(1, n); visited(root) = true;
q = root;
while ~isempty(q)
    u = q(1); q(1) = [];
    bfs(end + 1) = u;                       %#ok<AGROW>
    for v = adj{u}
        if ~visited(v); visited(v) = true; q(end + 1) = v; end   %#ok<AGROW>
    end
end

% DFS（升序邻接、递归）
dfs = zeros(1, 0); seen = false(1, n);
dfs = dfs_visit(root, adj, seen, dfs);

% Huffman
[lens, wpl] = huffman(w);

out = struct('bfs', bfs, 'dfs', dfs, 'lens', lens, 'wpl', wpl);

fprintf('[tree_traversal] rooted tree (root %d): 1-2,1-3,2-4,2-5,3-6\n', root);
fprintf('  BFS order: %s\n', num2str(bfs, '%d '));
fprintf('  DFS order: %s\n', num2str(dfs, '%d '));
fprintf('  Huffman weights [%s] => code lengths [%s], weighted path length = %g\n', ...
        num2str(w, '%g '), num2str(lens, '%d '), wpl);
fprintf('  hand-computed: BFS [1 2 3 4 5 6] · DFS [1 2 4 5 3 6] · WPL 224   =>  %s\n', ...
        ternary(isequal(bfs, [1 2 3 4 5 6]) && isequal(dfs, [1 2 4 5 3 6]) && wpl == 224, ...
                'MATCH', 'MISMATCH'));
end

function dfs = dfs_visit(u, adj, seen, dfs)
seen(u) = true;
dfs(end + 1) = u;
for v = adj{u}
    if ~seen(v); dfs = dfs_visit(v, adj, seen, dfs); end
end
end

function [lens, wpl] = huffman(w)
n = numel(w);
wt = zeros(1, 2 * n - 1); wt(1:n) = w;
left = zeros(1, 2 * n - 1); right = zeros(1, 2 * n - 1);
activeIdx = 1:n; activeW = w; next = n + 1;
while numel(activeIdx) > 1
    [~, o] = sort(activeW);
    a = activeIdx(o(1)); b = activeIdx(o(2));
    wt(next) = wt(a) + wt(b); left(next) = a; right(next) = b;
    rm = [o(1) o(2)];
    activeIdx(rm) = []; activeW(rm) = [];
    activeIdx(end + 1) = next; activeW(end + 1) = wt(next);    %#ok<AGROW>
    next = next + 1;
end
root = activeIdx(1);
lens = zeros(1, n);
stack = root; dstack = 0;
while ~isempty(stack)
    node = stack(end); d = dstack(end); stack(end) = []; dstack(end) = [];
    if node <= n
        lens(node) = d;
    else
        stack(end + 1) = left(node); dstack(end + 1) = d + 1;     %#ok<AGROW>
        stack(end + 1) = right(node); dstack(end + 1) = d + 1;    %#ok<AGROW>
    end
end
wpl = sum(w(:)' .* lens);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
