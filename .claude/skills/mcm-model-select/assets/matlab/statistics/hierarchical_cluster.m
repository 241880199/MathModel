function out = hierarchical_cluster(opts)
%HIERARCHICAL_CLUSTER  Agglomerative (system) clustering of SAMPLES on synthetic data with a
%   KNOWN 2-group structure (3+3 points); single/complete/average linkage; cut@2 recovers the
%   groups. Merge order cross-checked by hand on a 4-point line (single linkage => [1 2 4]).
%
%   M4 `mcm-model-select` 骨架 · statistics #2（系统聚类 / 层次聚类）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@<名>` 类目录撞名（实测 find <matlabroot>/toolbox -name "@hierarchical_cluster" ⇒ 0）。
%
%   独立参照（第 3/4 类：合成数据 · 已知簇结构）—— 不是"跟 MATLAB 内置对"：
%     · 主例：6 个点 = **2 个已知分群**（A 三点密集、B 三点密集、两群远隔）⇒
%       `cluster(Z,2)` 割树得到的组应**还原**已知分组（对 single/complete/average 三种链接都核）；
%     · 手算核对：4 点直线 [0 1 3 7] 的 **single 链接合并次序**可**手算** = 距离 `[1 2 4]`
%       （先并近邻、再并入 3、最后并入 7）⇒ 与 `linkage(...,'single')` 的 `Z(:,3)` 逐位比。
%   ★ **链接方式（single/complete/average）显式**，并核它对结果的影响。
%   ★ MATLAB 的 `linkage` / `cluster` 只作**实现**，**不作独立参照**（同机同实现不独立）。
%
%   用法：
%     hierarchical_cluster()             % 自检并打印读数
%     out = hierarchical_cluster(opts)   % opts.X opts.truth opts.methods opts.line
%
%   返回 struct：methods, acc（各链接方式 cut@2 的分组还原率）, mergedist（各法前三层合并距离）,
%                line_md（4 点直线 single 合并距离，手算应为 [1 2 4]）。

if nargin < 1 || isempty(opts); opts = struct(); end
A = [0 0; 1 0; 0 1];
B = [10 10; 11 10; 10 11];
Xd = dflt(opts, 'X',     [A; B]);
truth = dflt(opts, 'truth', [1 1 1 2 2 2]');   % 已知（2 群）
methods = dflt(opts, 'methods', {'single', 'complete', 'average'});
line = dflt(opts, 'line', [0; 1; 3; 7]);

nm = numel(methods);
acc = zeros(1, nm);
mergedist = cell(1, nm);
for i = 1:nm
    Z = linkage(Xd, methods{i});               % 内置：**实现**，非独立参照
    lab = cluster(Z, 2);                       % 割树成 2 群
    % 簇标签可置换 ⇒ 两种标号取较大一致率
    a1 = mean(lab == truth);
    a2 = mean(lab == (3 - truth));
    acc(i) = max(a1, a2);
    mergedist{i} = Z(:, 3)';                   % 各层合并距离（末层可能 inf）
end

Zl = linkage(line, 'single');                  % 4 点直线：single 合并距离（手算 [1 2 4]）
line_md = Zl(:, 3)';

out = struct('methods', {methods}, 'acc', acc, 'mergedist', {mergedist}, ...
             'line_md', line_md, 'line_handcalc', [1 2 4]);

fprintf('[hierarchical_cluster] samples: %d points in KNOWN groups %s (2 groups: 3 + 3)\n', ...
        size(Xd, 1), mat2str(truth'));
fprintf('  %-9s  %-14s  %s\n', 'linkage', 'cut@2 recovery', 'merge distances (Z(:,3))');
for i = 1:nm
    fprintf('  %-9s  %-14s  [%s]\n', methods{i}, ...
            sprintf('%d/%d', round(acc(i) * numel(truth)), numel(truth)), ...
            num2str(mergedist{i}, '%.4g '));
end
fprintf('  hand-check (4-pt line, single linkage): merge distances = [%s]\n', ...
        num2str(line_md, '%.4g '));
fprintf('    hand-computed = [%s]   =>  %s\n', num2str([1 2 4], '%.4g '), ...
        ternary(isequal(round(line_md), [1 2 4]), 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
