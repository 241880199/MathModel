function out = topsis(opts)
%TOPSIS  Technique for Order Preference by Similarity to Ideal Solution.
%
%   M4 `mcm-model-select` 骨架 · evaluation #4（TOPSIS）。文件名全 ASCII（GC5）。
%   ★ MATLAB **无内置** `topsis`（MATLAB 本无此函数）⇒ 本骨架自己写（GC6 · 设计 §7）。
%
%   语料面（P6）：**带语料指针（薄）** —— `corpus/papers/MODEL_MAP.md` 里 `TOPSIS` 命中 1 篇
%   （P2025-D-04，其正文用 `entropy-weight-TOPSIS` 组合法）；`corpus/algorithms/src/`（脚本素材面）0 命中。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 向量归一化  r_ij = x_ij / sqrt( sum_i x_ij^2 )；
%     · 加权        v_ij = w_j * r_ij；
%     · 正/负理想解 v_j^+ = max_i v_ij（效益型；成本型取 min），v_j^- 相反；
%     · 欧氏距离    D_i^+ = sqrt( sum_j (v_ij - v_j^+)^2 )，D_i^- 同理；
%     · 贴近度      C_i = D_i^- / (D_i^+ + D_i^-)，C 越大越优。
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/topsis.md`。
%
%   用法：
%     topsis()             % 自检并打印读数（三方案三指标标准算例）
%     out = topsis(opts)   % opts.X opts.w opts.benefit
%
%   返回 struct：R, V, v_pos, v_neg, D_pos, D_neg, C, rank。

if nargin < 1 || isempty(opts); opts = struct(); end
% 标准算例：三方案 × 三指标（全效益型），等权
X       = dflt(opts, 'X',       [2 3 4; 4 2 5; 3 5 3]);
w       = dflt(opts, 'w',       [1/3 1/3 1/3]);
benefit = dflt(opts, 'benefit', [true true true]);

[m, n] = size(X);
w = w(:)' ./ sum(w);        % 权重归一化
benefit = logical(benefit);

% ① 向量归一化
R = X ./ sqrt(sum(X.^2, 1));

% ② 加权
V = R .* w;

% ③ 正/负理想解（按指标类型）
v_pos = zeros(1, n); v_neg = zeros(1, n);
for j = 1:n
    if benefit(j)
        v_pos(j) = max(V(:, j)); v_neg(j) = min(V(:, j));
    else
        v_pos(j) = min(V(:, j)); v_neg(j) = max(V(:, j));
    end
end

% ④ 距离
D_pos = sqrt(sum((V - v_pos).^2, 2));
D_neg = sqrt(sum((V - v_neg).^2, 2));

% ⑤ 贴近度
C = D_neg ./ (D_pos + D_neg);
[~, rank] = sort(C, 'descend');

out = struct('X', X, 'w', w, 'benefit', benefit, 'R', R, 'V', V, ...
             'v_pos', v_pos, 'v_neg', v_neg, 'D_pos', D_pos, ...
             'D_neg', D_neg, 'C', C, 'rank', rank);

fprintf('[topsis] 方案数 m = %d, 指标数 n = %d, 权重 = [%s]\n', m, n, num2str(w));
fprintf('  C (贴近度) = [%s]\n', num2str(C', '%.10g  '));
fprintf('  排序 (C 降序) = [%s]\n', num2str(rank'));
fprintf('  D+ = [%s]\n', num2str(D_pos', '%.10g  '));
fprintf('  D- = [%s]\n', num2str(D_neg', '%.10g  '));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
