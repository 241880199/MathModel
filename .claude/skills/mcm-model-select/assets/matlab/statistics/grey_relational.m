function out = grey_relational(opts)
%GREY_RELATIONAL  Grey relational analysis (GRA), resolution coefficient rho = 0.5;
%   hand example: reference x0 = [1 2 3 4], 3 comparison factors over 4 samples;
%   hand-computed relational grades r = [0.475000 0.916667 0.533333] (rank: f2 > f3 > f1).
%
%   M4 `mcm-model-select` 骨架 · statistics #4（灰色关联 / 优势分析 · 因素排序）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@<名>` 类目录撞名（实测 find <matlabroot>/toolbox -name "@grey_relational" ⇒ 0）。
%
%   独立参照（第 3 类：手算算例）—— 不是"跟另一段代码对"：
%     小规模算例（**1 个参考序列 x0 + 3 个比较因素**，各 **4 个样本**），`rho = 0.5`（惯例），
%     用**原始差**（不做归一化，保持手算可核）：
%       Delta_i(k) = |x0(k) - xi(k)| · min = 0 · max = 4 · xi_i(k) = (min + rho*max)/(Delta + rho*max)
%       ⇒ xi1 = 2/[3 4 5 6] = [0.666667 0.5 0.4 0.333333]  ⇒ r1 = 0.475
%          xi2 = 2/[2 2 2 3] = [1 1 1 0.666667]            ⇒ r2 = 0.916667
%          xi3 = 2/[5 3 3 5] = [0.4 0.666667 0.666667 0.4] ⇒ r3 = 0.533333
%     ⇒ **手算逐位**与骨架的 `xi` 矩阵、`r` 向量逐位比。
%   ★ **分辨系数 rho = 0.5 显式**（惯例值；rho ∈ (0,1)，越小越放大差异）。
%
%   用法：
%     grey_relational()             % 自检并打印读数
%     out = grey_relational(opts)   % opts.x0 opts.X opts.rho
%
%   返回 struct：x0, X, rho, Delta, minv, maxv, xi, r, r_sorted, order。

if nargin < 1 || isempty(opts); opts = struct(); end
x0  = dflt(opts, 'x0',  [1 2 3 4]);          % 参考序列（1×n 样本）
X   = dflt(opts, 'X',   [2 4 6 8; ...
                         1 2 3 3; ...
                         4 3 2 1]);          % 比较因素（m×n，每行一个因素）
rho = dflt(opts, 'rho', 0.5);                % ★ 分辨系数（惯例 0.5）

Delta = abs(X - x0);                         % |x0(k) - xi(k)|，m×n
minv = min(Delta(:));
maxv = max(Delta(:));
xi = (minv + rho*maxv) ./ (Delta + rho*maxv);  % 关联系数
r = mean(xi, 2);                              % 关联度（沿样本取均值）
[rs, order] = sort(r, 'descend');             % 因素影响力排序

out = struct('x0', x0, 'X', X, 'rho', rho, 'Delta', Delta, 'minv', minv, ...
             'maxv', maxv, 'xi', xi, 'r', r, 'r_sorted', rs, 'order', order);

fprintf('[grey_relational] rho = %.4g; reference x0 = [%s]; %d comparison factors, %d samples\n', ...
        rho, num2str(x0, '%.4g '), size(X, 1), size(X, 2));
fprintf('  Delta range: min = %.4g, max = %.4g\n', minv, maxv);
for i = 1:size(X, 1)
    fprintf('  factor %d: xi = [%s]   r = %.6f\n', i, num2str(xi(i, :), '%.6f '), r(i));
end
fprintf('  relational grades r = [%s]   rank (desc): factors [%s]\n', ...
        num2str(r', '%.6f '), num2str(order', '%d '));
fprintf('  hand-computed r = [0.475000 0.916667 0.533333]   =>  %s\n', ...
        ternary(max(abs(r' - [0.475 0.916667 0.533333])) < 1e-6, 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
