function [B, score] = fuzzy_evaluation(R, w, operator, grades)
% 模糊综合评价（单层）—— B = w ∘ R
%
%   净室重写。替代上游 FuzzyMathematicalModel模糊数学模型/多层次模糊综合评价/
%   main.m（R2025b 上报"数组索引必须为正整数或逻辑值"）。
%
% 用法
%   B = fuzzy_evaluation(R, w)                       默认加权平均型 M4
%   B = fuzzy_evaluation(R, w, 'M1')                 主因素决定型 (∧,∨)
%   B = fuzzy_evaluation(R, w, 'M2')                 主因素突出型 (·,∨)
%   B = fuzzy_evaluation(R, w, 'M3')                 不均衡平均型 (∧,⊕)
%   [B, score] = fuzzy_evaluation(R, w, 'M4', [1 2 3 4 5])   加权综合得分
%
% 输入
%   R        m×n 隶属度矩阵：m 个因素对 n 个评价等级的隶属度，元素 ∈ [0,1]
%   w        1×m（或 m×1）因素权重，自动归一化
%   operator 'M1' | 'M2' | 'M3' | 'M4'（默认 'M4'，数模最常用）
%   grades   1×n 各评价等级的量化取值（如 [1 2 3 4 5]），用于算综合得分
%
% 输出
%   B       1×n 综合评价向量（已归一化，sum(B) = 1）
%   score   加权综合得分 = B · grades'（需给 grades）
%
% 四种算子的定义为教科书标准形式，与 COMAP 无关。

    if nargin < 3 || isempty(operator), operator = 'M4'; end

    if ~ismatrix(R) || any(R(:) < 0 | R(:) > 1)
        error('fuzzy_evaluation:badR', 'R 的元素必须在 [0,1] 内');
    end

    w = w(:)';
    if numel(w) ~= size(R, 1)
        error('fuzzy_evaluation:sizeMismatch', ...
            'w 的长度 %d 与 R 的行数 %d 不一致', numel(w), size(R, 1));
    end
    w = w / sum(w);

    switch upper(operator)
        case 'M1'   % 主因素决定型：b_j = max_i min(w_i, r_ij)
            B = max(min(w(:), R), [], 1);

        case 'M2'   % 主因素突出型：b_j = max_i (w_i · r_ij)
            B = max(w(:) .* R, [], 1);

        case 'M3'   % 不均衡平均型：b_j = min(1, Σ_i min(w_i, r_ij))
            B = min(1, sum(min(w(:), R), 1));

        case 'M4'   % 加权平均型：b_j = Σ_i w_i · r_ij
            B = w * R;

        otherwise
            error('fuzzy_evaluation:badOperator', '未知 operator: %s', operator);
    end

    if sum(B) <= 0
        error('fuzzy_evaluation:zeroResult', '评价结果全为零，检查 R 与权重');
    end
    B = B / sum(B);          % 归一化

    if nargin >= 4 && ~isempty(grades)
        grades = grades(:)';
        if numel(grades) ~= numel(B)
            error('fuzzy_evaluation:gradesSize', ...
                'grades 的长度 %d 与评价等级数 %d 不一致', numel(grades), numel(B));
        end
        score = B * grades';
    else
        score = [];
    end
end
