function out = multi_level_fuzzy(opts)
%MULTI_LEVEL_FUZZY  Two-level fuzzy comprehensive evaluation (多层次模糊综合评价).
%
%   M4 `mcm-model-select` 骨架 · evaluation #2。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针（类级）** —— `corpus/papers/MODEL_MAP.md` 里
%   `fuzzy comprehensive evaluation` 命中 2 篇（P2025-D-03 · P2025-E-03）；
%   ★ 该 tag **不区分"多层次"与"多目标"两种形态** ⇒ 本条指针是**类级**的、两方法共用。
%   `corpus/algorithms/src/`（脚本素材面）有起点素材
%   （`corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/多层次模糊综合评价/`，含 `main.m`）。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     两级：准则层权重 W（1xK）；准则 k 有子权重 Wk（1 x n_k）与隶属度矩阵 Rk（n_k x p，行=子指标、列=评语等级）。
%     · 一级（子准则）B_k = Wk * Rk              （**加权平均算子** M(·,+)）
%     · 二级（准则层）R_top = [B_1; ...; B_K]；B = W * R_top
%     · 综合得分      S = B * V.'，V = 评语等级分值向量（如 [100 80 60]）
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/multi_level_fuzzy.md`。
%
%   ★ 算子对照（常见坑）：M(·,+)（加权平均，保留全部信息、B 归一）与
%     M(∧,∨)（最大最小合成，会丢信息且 B 常不归一）结果不同 ⇒ 论文里**必须写明用了哪个算子**。
%     本骨架两种都算（`op` 选项：'weighted' | 'maxmin'）；**参照只核 M(·,+)**。
%
%   用法：
%     multi_level_fuzzy()             % 自检并打印读数
%     out = multi_level_fuzzy(opts)   % opts.W opts.Wk opts.Rk opts.V
%
%   返回 struct：W, Wk, Rk, B_k, B, score, best_grade, B_maxmin。

if nargin < 1 || isempty(opts); opts = struct(); end
% 主算例：2 准则 × 各 2 子指标 × 3 评语等级
W  = dflt(opts, 'W',  [0.6 0.4]);
Wk = dflt(opts, 'Wk', {[0.5 0.5], [0.7 0.3]});
Rk = dflt(opts, 'Rk', {[0.3 0.6 0.1; 0.4 0.4 0.2], [0.5 0.4 0.1; 0.2 0.5 0.3]});
V  = dflt(opts, 'V',  [100 80 60]);
op = dflt(opts, 'op', 'weighted');

K = numel(Wk);
p = numel(V);
assert(numel(W) == K, 'W 的长度必须等于准则数 numel(Wk)');
for k = 1:K
    assert(size(Rk{k}, 2) == p, 'Rk{%d} 的列数必须等于评语等级数 %d', k, p);
    assert(numel(Wk{k}) == size(Rk{k}, 1), 'Wk{%d} 的长度必须等于 Rk{%d} 的行数', k, k);
end

% --- 一级：子准则 ---
B_k = zeros(K, p);
for k = 1:K
    B_k(k, :) = Wk{k} * Rk{k};           % M(·,+)：加权平均
end
% --- 二级：准则层 ---
R_top = B_k;
B = W * R_top;
score = B * V.';
[~, best_grade] = max(B);

% --- 算子对照：M(∧,∨) 最大最小合成 ---
B_k_mm = zeros(K, p);
for k = 1:K
    B_k_mm(k, :) = max(min(repmat(Wk{k}.', 1, p), Rk{k}), [], 1);   % M(∧,∨)
end
B_maxmin = max(min(repmat(W.', 1, p), B_k_mm), [], 1);

out = struct('W', W, 'Wk', {Wk}, 'Rk', {Rk}, 'B_k', B_k, 'B', B, ...
             'score', score, 'best_grade', best_grade, 'B_maxmin', B_maxmin, 'op', op);

fprintf('[multi_level_fuzzy] 两级 · %d 准则 × 各子指标 × %d 评语等级\n', K, p);
for k = 1:K
    fprintf('  B_%d (M(·,+)) = [%s]  (和 = %.12g)\n', k, num2str(B_k(k, :), '%.12g  '), sum(B_k(k, :)));
end
fprintf('  B (综合隶属度) = [%s]  (和 = %.12g)\n', num2str(B, '%.12g  '), sum(B));
fprintf('  综合得分 S = B * V'' = %.12g   （最优等级 = 第 %d 级）\n', score, best_grade);
fprintf('  ★ 算子对照 M(∧,∨) B = [%s]  （未归一、与 M(·,+) 不同 ⇒ 论文须写明算子）\n', ...
        num2str(B_maxmin, '%.12g  '));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
