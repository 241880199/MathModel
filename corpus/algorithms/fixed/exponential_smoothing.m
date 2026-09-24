function [yhat, ypred, rmse] = exponential_smoothing(y, alpha, order, m)
% 指数平滑法（一次 / 二次 / 三次）—— 时间序列短期预测
%
%   净室重写。替代上游 TimeSeries时间序列函数/指数平滑法/ 下的脚本；
%   其中 `single_exponential _smoothing.m` 文件名含空格，MATLAB 无法把它
%   当脚本执行（报"未定义函数 'single_exponential'"）。
%
% 用法
%   [yhat, ypred, rmse] = exponential_smoothing(y, alpha)
%   [yhat, ypred, rmse] = exponential_smoothing(y, alpha, 2)     二次平滑
%   [yhat, ypred, rmse] = exponential_smoothing(y, alpha, 3, 5)  三次平滑，预报 5 步
%
% 输入
%   y      1×n 或 n×1 观测序列
%   alpha  平滑系数，0 < alpha < 1（可给向量，则逐列计算）
%   order  1（默认）| 2 | 3
%   m      向前预报步数，默认 1
%
% 输出
%   yhat   n×k 拟合值（k = numel(alpha)）
%   ypred  1×k 向前 m 步的预报值
%   rmse   1×k 拟合均方根误差
%
% 初始值取 S(1) = y(1)（教科书的常见取法之一，另一取法是前两期均值）。
% 公式为教科书标准形式，与 COMAP 无关，不套证据分级。

    if nargin < 3 || isempty(order), order = 1; end
    if nargin < 4 || isempty(m), m = 1; end

    y = y(:);
    n = numel(y);
    alpha = alpha(:)';
    k = numel(alpha);

    if any(alpha <= 0 | alpha >= 1)
        error('exponential_smoothing:badAlpha', 'alpha 必须在 (0,1) 内');
    end
    if ~ismember(order, [1 2 3])
        error('exponential_smoothing:badOrder', 'order 只能是 1、2 或 3');
    end
    if n < 3
        error('exponential_smoothing:tooShort', '序列至少需要 3 个点');
    end

    S1 = zeros(n, k);
    S2 = zeros(n, k);
    S3 = zeros(n, k);
    yhat = zeros(n, k);

    for j = 1:k
        a = alpha(j);
        S1(1, j) = y(1);
        S2(1, j) = y(1);
        S3(1, j) = y(1);

        for t = 2:n
            S1(t, j) = a*y(t) + (1-a)*S1(t-1, j);
            if order >= 2
                S2(t, j) = a*S1(t, j) + (1-a)*S2(t-1, j);
            end
            if order >= 3
                S3(t, j) = a*S2(t, j) + (1-a)*S3(t-1, j);
            end
        end

        % 拟合值：用 t-1 时刻的平滑值预报 t 时刻（一步超前）
        for t = 2:n
            [A, B, C] = coeffs(S1(t-1,j), S2(t-1,j), S3(t-1,j), a, order);
            yhat(t, j) = A + B*1 + C*1^2;
        end
        yhat(1, j) = NaN;          % 首点无一步超前预报
    end

    rmse = sqrt(mean((y - yhat).^2, 1, 'omitnan'));

    ypred = zeros(1, k);
    for j = 1:k
        [A, B, C] = coeffs(S1(n,j), S2(n,j), S3(n,j), alpha(j), order);
        ypred(j) = A + B*m + C*m^2;
    end
end

% -------------------------------------------------------------------------

function [A, B, C] = coeffs(S1, S2, S3, a, order)
% 由平滑值还原 a + b·m + c·m² 预报式的三个系数。
    switch order
        case 1
            A = S1; B = 0; C = 0;
        case 2
            A = 2*S1 - S2;
            B = a/(1-a) * (S1 - S2);
            C = 0;
        case 3
            A = 3*S1 - 3*S2 + S3;
            B = a/(2*(1-a)^2) * ((6-5*a)*S1 - 2*(5-4*a)*S2 + (4-3*a)*S3);
            C = a^2/(2*(1-a)^2) * (S1 - 2*S2 + S3);
    end
end
