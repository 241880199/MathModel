function [w, CR, CI, lambda] = ahp(A, method)
% AHP 层次分析法 —— 判断矩阵的权重向量与一致性检验
%
%   净室重写。替代上游 AHP层次分析法/ahp_common.m，该文件在 MATLAB R2025b
%   上直接报解析错误（第 30 行 `str2num(CI)` 应为 `num2str`），且 `r = d(1,1)`
%   假设 eig 把最大特征值排在首位——该假设不成立。
%
% 用法
%   [w, CR, CI, lambda] = ahp(A)              特征值法（默认）
%   [w, CR, CI, lambda] = ahp(A, 'sqrt')      方根法（几何平均）
%   [w, CR, CI, lambda] = ahp(A, 'sum')       和积法（算术平均）
%
% 输入
%   A       n×n 正互反判断矩阵，A(i,j) = 1/A(j,i)，A(i,i) = 1
%   method  'eig'（默认）| 'sqrt' | 'sum'
%
% 输出
%   w       1×n 归一化权重向量，sum(w) = 1
%   CR      一致性比例；CR < 0.10 视为通过
%   CI      一致性指标 (lambda - n)/(n-1)
%   lambda  最大特征值（特征值法）或 n（近似法，此时 CI 由特征值另算）
%
% 判据来源：Saaty 的 AHP 通行判据，RI 表为教科书标准取值。
% 这是教科书常识，与 COMAP 无关，故不套 [官方]/[半官方]/[社区] 分级。

    if nargin < 2 || isempty(method), method = 'eig'; end

    validate(A);

    n = size(A, 1);

    switch lower(method)
        case 'eig'
            % 正确取主特征值：先滤出实特征值，再取最大——而不是假定 eig
            % 把最大特征值排在第 1 位（上游 ahp_common.m 正因此取错）。
            [V, D] = eig(A);
            d = diag(D);
            keep = abs(imag(d)) < 1e-10;   % 正互反阵的主特征值为实
            d = real(d(keep));
            V = real(V(:, keep));
            [lambda, k] = max(d);
            w = V(:, k);
        case 'sqrt'
            w = prod(A, 2) .^ (1/n);                   % 行几何平均
            lambda = mean((A * w) ./ w);               % 由 w 反推主特征值
        case 'sum'
            B = A ./ sum(A, 1);                        % 列归一化
            w = mean(B, 2);
            lambda = mean((A * w) ./ w);
        otherwise
            error('ahp:badMethod', '未知 method: %s', method);
    end

    w = w(:)' / sum(w);                                % 归一化

    CI = (lambda - n) / (n - 1);
    ri = ri_table(n);

    if ri == 0
        % n = 1 或 2 时判断矩阵必然一致，CR 无定义
        CR = 0;
    else
        CR = CI / ri;
    end
end

% -------------------------------------------------------------------------

function validate(A)
    if ~ismatrix(A) || size(A,1) ~= size(A,2)
        error('ahp:notSquare', 'A 必须是方阵');
    end
    if any(~isfinite(A), 'all') || any(A(:) <= 0)
        error('ahp:notPositive', 'A 的所有元素必须为正的有限值');
    end
    n = size(A, 1);
    if max(abs(diag(A) - 1)) > 1e-10
        error('ahp:diagNotOne', 'A 的对角线元素必须为 1');
    end
    if max(abs(A - 1./A.'), [], 'all') > 1e-8
        error('ahp:notReciprocal', 'A 必须是正互反矩阵：A(i,j) = 1/A(j,i)');
    end
    if n > 15
        warning('ahp:largeN', 'n = %d 超出常用 RI 表范围(≤15)，CR 仅供参考', n);
    end
end

function ri = ri_table(n)
% 随机一致性指标 RI（Saaty）。n > 15 时按 1.59 外推，仅作提示。
    table = [0 0 0.52 0.89 1.12 1.26 1.36 1.41 1.46 1.49 ...
             1.52 1.54 1.56 1.58 1.59];
    if n <= numel(table)
        ri = table(n);
    else
        ri = 1.59;
    end
end
