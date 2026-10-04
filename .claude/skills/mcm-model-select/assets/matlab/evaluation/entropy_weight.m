function out = entropy_weight(opts)
%ENTROPY_WEIGHT  Objective criterion weighting via information entropy.
%
%   M4 `mcm-model-select` 骨架 · evaluation #5（熵权法）。文件名全 ASCII（GC5）。
%   ★ MATLAB **无内置**（`entropy_weight` 只是几十行）⇒ 本骨架自己写（GC6 · 设计 §7）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `entropy weight method` 命中 **5 篇**
%   （P2025-B-04 · P2025-D-02 · P2025-D-04 · P2025-E-01 · P2025-E-03）；`corpus/algorithms/src/` 0 命中。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 归一化  p_ij = x_ij / sum_i x_ij；
%     · 熵      e_j  = -(1/ln m) * sum_i p_ij ln p_ij，约定 0·ln0 = 0；
%     · 差异度  d_j  = 1 - e_j；
%     · 权重    w_j  = d_j / sum_j d_j。
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/entropy_weight.md`。
%
%   ★★ 零值/负值处置（熵权法的已知坑，本骨架显式处理并打印）：
%     · 零值：p_ij = 0 时按约定 0·ln0 = 0（MATLAB 直接算会得 NaN ⇒ 必须显式置 0）；
%     · 负值：信息熵要求取值非负 ⇒ 先做**逐列 min-max 归一化到 [0,1]**（本骨架对含负值的矩阵自动触发，
%       并打印一条注记；这一归一化会改变权重，须与直接用法区分）；
%     · 常数指标列（各方案同值）：熵 e_j = 1 ⇒ 差异度 0 ⇒ 权重 0。
%
%   用法：
%     entropy_weight()             % 自检并打印读数（含零值 / 负值两个算例）
%     out = entropy_weight(opts)   % opts.X opts.benefit
%
%   返回 struct：w, e, d, p（主算例）· w_zero, w_neg（两个边界算例）。

if nargin < 1 || isempty(opts); opts = struct(); end
X = dflt(opts, 'X', [1 2 3; 2 3 4; 3 4 5]);
benefit = dflt(opts, 'benefit', true(1, size(X, 2)));

[w, e, d, p] = ew_core(X, benefit);

% --- 边界算例一：含零值 ---
X0 = [0 1 2; 2 3 4; 4 5 6];
[w0, e0] = ew_core(X0, true(1, 3));

% --- 边界算例二：含负值（自动触发 min-max 归一化）---
Xn = [1 -1 2; 2 3 1; 3 1 3];
[wn, en] = ew_core(Xn, true(1, 3));

out = struct('X', X, 'w', w, 'e', e, 'd', d, 'p', p, ...
             'w_zero', w0, 'e_zero', e0, 'w_neg', wn, 'e_neg', en);

fprintf('[entropy_weight] 主算例 X = [1 2 3; 2 3 4; 3 4 5]（全效益型，m = 3）\n');
fprintf('  熵 e  = [%s]\n', num2str(e, '%.10g  '));
fprintf('  差异 d = [%s]\n', num2str(d, '%.10g  '));
fprintf('  权重 w = [%s]  (和 = %.12g)\n', num2str(w, '%.10g  '), sum(w));
fprintf('[entropy_weight] 零值算例 X = [0 1 2; 2 3 4; 4 5 6]\n');
fprintf('  熵 e  = [%s]  (0·ln0 = 0 约定生效)\n', num2str(e0, '%.10g  '));
fprintf('  权重 w = [%s]  (全为有限值 ⇒ 未出 NaN)\n', num2str(w0, '%.10g  '));
fprintf('[entropy_weight] 负值算例 X = [1 -1 2; 2 3 1; 3 1 3]（含负数 ⇒ 逐列 min-max 到 [0,1] 后计算）\n');
fprintf('  权重 w = [%s]  (全为有限值、且全为非负)\n', num2str(wn, '%.10g  '));
fprintf('[entropy_weight] 注：负值算例触发了 min-max 归一化（见文件头注释的零值/负值处置）\n');
end

% ------------------------------------------------------------------------
function [w, e, d, p] = ew_core(X, benefit)
[m, n] = size(X);
benefit = logical(benefit);
Xn = X;
for j = 1:n
    if ~benefit(j); Xn(:, j) = max(X(:, j)) - X(:, j); end   % 成本型 → 效益型（差值法）
end

% 负值处置：逐列 min-max 归一化到 [0,1]（信息熵要求非负）
if min(Xn(:)) < 0
    for j = 1:n
        lo = min(Xn(:, j)); hi = max(Xn(:, j));
        if hi > lo; Xn(:, j) = (Xn(:, j) - lo) / (hi - lo); else; Xn(:, j) = zeros(m, 1); end
    end
end

colsum = sum(Xn, 1);
p = zeros(m, n);
for j = 1:n
    if colsum(j) > 0; p(:, j) = Xn(:, j) / colsum(j); end
end

term = p .* log(p);
term(p == 0) = 0;                       % ★ 约定 0·ln0 = 0（否则得 NaN）
e = -sum(term, 1) / log(m);
d = 1 - e;
if sum(d) > 0; w = d / sum(d); else; w = zeros(1, n); end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
