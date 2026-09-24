function [params, yfit, ypred] = trend_extrapolation(y, model, m)
% 趋势外推预测法：修正指数曲线 / Compertz 曲线 / Logistic 曲线
%
%   净室重写。替代上游 TimeSeries时间序列函数/趋势外推预测法/ 下的三个脚本
%   （compertz_curve.m / logistic_curve.m / modified_exponential_curve.m）。
%   上游三者在 R2025b 上均报"函数或变量 'k'/'b' 无法识别"——它们依赖同目录
%   predict1.m / predict2.m / predict3.m，而那三个辅助脚本里的变量名与主脚本
%   对不上。
%
% 用法
%   [p, yfit, ypred] = trend_extrapolation(y, 'modified')        y = K + a·b^t
%   [p, yfit, ypred] = trend_extrapolation(y, 'compertz')        y = K·a^(b^t)
%   [p, yfit, ypred] = trend_extrapolation(y, 'logistic')        y = K/(1+a·e^(-bt))
%   [p, yfit, ypred] = trend_extrapolation(y, 'compertz', 5)     向前预报 5 步
%
% 输入
%   y      观测序列，长度 n 必须是 3 的倍数（三和法要求）
%   model  'modified'（默认）| 'compertz' | 'logistic'
%   m      向前预报步数，默认 1
%
% 输出
%   params 结构体：K, a, b（logistic 的 b 为 e^(-b)，已换回原参数 bLogit）
%   yfit   1×n 拟合值
%   ypred  1×m 预报值
%
% 方法为教科书的"三和法"（把序列三等分求和反解参数），与 COMAP 无关。

    if nargin < 2 || isempty(model), model = 'modified'; end
    if nargin < 3 || isempty(m), m = 1; end

    y = y(:)';
    n = numel(y);

    if mod(n, 3) ~= 0
        error('trend_extrapolation:notDivisible', ...
            '序列长度 n = %d 必须是 3 的倍数（三和法要求）', n);
    end
    if ~strcmpi(model, 'modified') && any(y <= 0)
        error('trend_extrapolation:needsPositive', ...
            '%s 模型要求序列全为正', model);
    end

    h = n / 3;

    switch lower(model)
        case 'modified'
            [K, a, b] = three_sum(y, h);
            f = @(t) K + a * b.^t;
            bLogit = b;

        case 'compertz'
            % 取对数后化为修正指数形式：ln y = ln K + (ln a)·b^t
            if any(y <= 0)
                error('trend_extrapolation:needsPositive', 'Compertz 要求 y > 0');
            end
            [lnK, lna, b] = three_sum(log(y), h);
            K = exp(lnK); a = exp(lna);
            f = @(t) K .* a.^(b.^t);
            bLogit = b;

        case 'logistic'
            % 取倒数后化为修正指数形式：1/y = 1/K + (a/K)·e^(-b t)
            if any(y <= 0)
                error('trend_extrapolation:needsPositive', 'Logistic 要求 y > 0');
            end
            [invK, inva, bb] = three_sum(1 ./ y, h);
            K = 1 / invK; a = inva * K;
            bLogit = -log(bb);
            f = @(t) K ./ (1 + a * exp(-bLogit * t));
            b = bb;

        otherwise
            error('trend_extrapolation:badModel', '未知 model: %s', model);
    end

    % 三和法的推导把第 j 个观测记为 t = j（即 t = 1..n），不是 t = 0..n-1。
    % 用错起点会让参数差一个 b 因子——上游 compertz_curve.m 正是按 t=1 写的
    % 三和公式，却在预测时按 t=0 代入，两者不自洽。
    t = 1:n;
    yfit = f(t);
    ypred = f(n + (1:m));

    params = struct('model', lower(model), 'K', K, 'a', a, 'b', bLogit);
end

% -------------------------------------------------------------------------

function [K, a, b] = three_sum(z, h)
% 三和法：z = K + a·b^t，序列按 t = 1..n 排列，n = 3h。
    S1 = sum(z(1:h));
    S2 = sum(z(h+1:2*h));
    S3 = sum(z(2*h+1:3*h));

    if abs(S2 - S1) < eps
        error('three_sum:degenerate', ...
            'S2 与 S1 相等，无法反解（序列可能不是指数型）');
    end
    if (S3 - S2) / (S2 - S1) <= 0
        error('three_sum:notExponential', ...
            '比值非正，序列不适配指数型趋势（改试线性外推）');
    end

    b = ((S3 - S2) / (S2 - S1)) ^ (1/h);
    if abs(b - 1) < 1e-12
        error('three_sum:bIsOne', 'b ≈ 1，模型退化（趋势外推不适用）');
    end

    a = (S2 - S1) * (b - 1) / (b * (b^h - 1)^2);
    K = (S1 - a * b * (b^h - 1) / (b - 1)) / h;
end
