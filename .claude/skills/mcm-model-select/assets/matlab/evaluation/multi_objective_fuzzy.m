function out = multi_objective_fuzzy(opts)
%MULTI_OBJECTIVE_FUZZY  Multi-objective fuzzy evaluation via relative membership.
%
%   M4 `mcm-model-select` 骨架 · evaluation #3（多目标模糊综合评价）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针（类级）** —— `corpus/papers/MODEL_MAP.md` 里
%   `fuzzy comprehensive evaluation` 命中 2 篇（P2025-D-03 · P2025-E-03）（**类级指针**，与"多层次"共用）。
%   `corpus/algorithms/src/`（脚本素材面）有起点素材
%   （`corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/多目标模糊综合评价/`，含 `main.m` + `muti_objective_fuzzy_analysis.m`）。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     方案 i（m 个）× 目标 j（n 个）的原始矩阵 X（m x n），各目标类型 benefit / cost：
%     · 相对隶属度（逐列 min-max）：
%         benefit: r_ij = (x_ij - min_i x_ij) / (max_i x_ij - min_i x_ij)
%         cost   : r_ij = (max_i x_ij - x_ij) / (max_i x_ij - min_i x_ij)
%     · 加权综合  B_i = sum_j w_j r_ij（w 归一）
%     · 排序：B 越大越优
%   ★ 与"多层次"的区别：本方法**无层级**，是**并列的多目标**；各目标量纲不同 ⇒ 用**相对隶属度**消除量纲。
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/multi_objective_fuzzy.md`。
%   ★ 常量目标列（max == min）⇒ 分母为 0；本骨架将该列相对隶属度置 0 并打印注记（常见坑）。
%
%   用法：
%     multi_objective_fuzzy()             % 自检并打印读数
%     out = multi_objective_fuzzy(opts)   % opts.X opts.w opts.benefit
%
%   返回 struct：X, w, benefit, R, B, rank, const_col。

if nargin < 1 || isempty(opts); opts = struct(); end
% 主算例：3 方案 × 3 目标（全效益型，量纲不同 ⇒ 需相对隶属度）
X = dflt(opts, 'X', [80 90 70; 70 85 95; 90 75 80]);
w = dflt(opts, 'w', [0.5 0.3 0.2]);
benefit = dflt(opts, 'benefit', [true true true]);

[m, n] = size(X);
w = w(:).' / sum(w);
benefit = logical(benefit);
assert(numel(w) == n && numel(benefit) == n, 'w / benefit 的长度必须等于目标数');

% --- 相对隶属度（逐列 min-max；常量列单独处置）---
R = zeros(m, n);
const_col = false(1, n);
for j = 1:n
    lo = min(X(:, j)); hi = max(X(:, j));
    if hi > lo
        if benefit(j)
            R(:, j) = (X(:, j) - lo) / (hi - lo);
        else
            R(:, j) = (hi - X(:, j)) / (hi - lo);
        end
    else
        const_col(j) = true;            % 常量列：max == min，分母为 0 ⇒ 置 0
    end
end

% --- 加权综合 ---
B = R * w.';
[~, rank] = sort(B, 'descend');

out = struct('X', X, 'w', w, 'benefit', benefit, 'R', R, ...
             'B', B, 'rank', rank, 'const_col', const_col);

fprintf('[multi_objective_fuzzy] 方案 m = %d, 目标 n = %d, 权重 = [%s]\n', m, n, num2str(w));
fprintf('  相对隶属度矩阵 R（逐列）：\n');
for i = 1:m
    fprintf('    方案 %d: [%s]\n', i, num2str(R(i, :), '%.12g  '));
end
fprintf('  综合隶属度 B = R * w'' = [%s]\n', num2str(B.', '%.12g  '));
fprintf('  排序 (B 降序) = [%s]\n', num2str(rank.'));
if any(const_col)
    fprintf('  ★ 注：第 [%s] 列为常量目标（max == min）⇒ 相对隶属度置 0\n', ...
            num2str(find(const_col)));
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
