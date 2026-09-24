function verify_numerics2(srcRoot, outFile)
% VERIFY_NUMERICS2  Numerical checks for the remaining tier-1 algorithms.
%
%   Companion to verify_numerics.m. Verifies the ORIGINAL archive scripts
%   (in src/), not the rewrites in fixed/. Each check runs the upstream
%   script, captures the variable it produces, and compares it against an
%   answer derived by a different route:
%
%     GM(1,1)      symbolic dsolve  vs  numeric closed form
%     moving avg   upstream loop    vs  convolution
%     exp smooth   upstream loop    vs  my independently tested rewrite
%     assignment   intlinprog       vs  MATLAB matchpairs (exact solver)
%     regression   regress()        vs  the normal equations
%     clustering   pdist(cityblock) vs  distances summed by hand
%     PCA          pcacov           vs  eig of the covariance matrix
%
%   Usage: matlab -batch "verify_numerics2('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');

    addpath(genpath(srcRoot));

    nPass = 0; nFail = 0; nSkip = 0;
    R = @(p) fullfile(srcRoot, p);

    % ================= G1  GM(1,1)：符号解 vs 数值闭式解 =================
    % 上游用 dsolve 求符号解再代值；独立路线是直接用闭式解
    %   x1(t) = (x0(1) - b/a)·exp(-a·t) + b/a
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G1 GM(1,1) 符号解 vs 数值闭式解', ...
        @() gm_compare(R('GreySystem灰色系统/GM_1_1_full_procession.m')));

    % ================= G2  简单移动平均：循环 vs 卷积 =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G2 简单移动平均(n=4) 循环 vs 卷积', ...
        @() movavg_compare(R('TimeSeries时间序列函数/移动平均法/simple_moving_average.m')));

    % ================= G3  二次指数平滑：上游 vs 我的重写版 =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G3 二次指数平滑 上游循环 vs 独立重算 a_t/b_t', ...
        @() expsmooth2_compare(R('TimeSeries时间序列函数/指数平滑法/second_exponential_smoothing.m')));

    % ================= G4  指派问题：intlinprog vs matchpairs =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G4 指派问题 intlinprog vs matchpairs', ...
        @() assign_compare(R('IntegerProgramming（线性规划、整数规划等内容的使用案例）/assgin_integer_prog.m')));

    % ================= G5  线性回归：regress vs 正规方程 =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G5 线性回归 regress vs 正规方程 (X''X)\\(X''y)', ...
        @() regress_compare(R('RegressionAnalysis回归分析/linear_regression.m')));

    % ================= G6  系统聚类的 cityblock 距离：pdist vs 手算 =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G6 cityblock 距离 pdist vs 手算', ...
        @() cityblock_compare(R('MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/system_cluster.m')));

    % ================= G7  PCA：pcacov vs cov 的特征分解 =================
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'G7 PCA 主成分 pcacov vs eig(cov)（取绝对值比）', ...
        @() pca_compare(R('MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/主成分分析/PCA.m')));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== 第二批 pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ 各项检查

function [a, e] = gm_compare(script)
    run_script(script);
    predictUp = evalin('base', 'predict');

    % 独立路线：闭式解，不用 dsolve
    x0 = evalin('base', 'x0');
    n = numel(x0);
    x1 = cumsum(x0);
    z = 0.5 * (x1(2:n) + x1(1:n-1));
    u = [-z(:), ones(n-1,1)] \ x0(2:n)';
    aHat = u(1); bHat = u(2);
    x1h = (x0(1) - bHat/aHat) * exp(-aHat*(0:n-1)) + bHat/aHat;
    ref = [x0(1), diff(x1h)];

    a = predictUp; e = ref;
end

function [a, e] = movavg_compare(script)
    run_script(script);
    up = evalin('base', 'yhat{1}');       % n = 4 的移动平均
    y = evalin('base', 'y');
    ref = conv(y, ones(1,4)/4, 'valid');  % 独立的卷积实现
    a = up; e = ref;
end

function [a, e] = expsmooth2_compare(script, ~)
    run_script(script);
    atUp = evalin('base', 'at');
    btUp = evalin('base', 'bt');

    % 独立重算：从 yt 逐点推 s1、s2，再算 a_t、b_t（不调用上游任何函数）
    yt = evalin('base', 'yt');
    alpha = 0.3; n = numel(yt);
    s1 = zeros(1,n); s2 = zeros(1,n); s1(1) = yt(1); s2(1) = yt(1);
    for i = 2:n
        s1(i) = alpha*yt(i) + (1-alpha)*s1(i-1);
        s2(i) = alpha*s1(i) + (1-alpha)*s2(i-1);
    end
    refAt = 2*s1 - s2;
    refBt = alpha/(1-alpha) * (s1 - s2);

    a = [atUp(:)', btUp(:)']; e = [refAt, refBt];
end

function [a, e] = assign_compare(script)
    run_script(script);
    fvalUp = evalin('base', 'fval');
    C = evalin('base', 'C');
    m = matchpairs(C, 1e6);              % 独立的精确指派求解器
    ref = sum(C(sub2ind(size(C), m(:,1), m(:,2))));
    a = fvalUp; e = ref;
end

function [a, e] = regress_compare(script)
    run_script(script);
    bUp = evalin('base', 'b');
    x1 = evalin('base', 'x1');
    y  = evalin('base', 'y');
    X = [ones(numel(x1),1), x1];
    ref = X \ y;                          % 正规方程，不经 regress
    a = bUp; e = ref;
end

function [a, e] = cityblock_compare(script)
    run_script(script);
    yUp = evalin('base', 'y');            % pdist 的距离向量
    aMat = evalin('base', 'a');
    [m, ~] = size(aMat);
    D = zeros(m);
    for i = 1:m
        for j = 1:m
            D(i,j) = sum(abs(aMat(i,:) - aMat(j,:)));   % 手算 cityblock
        end
    end
    ref = squareform(D);
    a = yUp; e = ref;
end

function [a, e] = pca_compare(script)
    run_script(script);
    PCup = evalin('base', 'PC');
    b = evalin('base', 'b');
    k = size(PCup, 2);                    % PC 的列数（= 自变量个数），
                                          % 注意它不是脚本里的 n（含因变量）
    [V, D] = eig(cov(b));                 % 独立路线：对协方差阵做特征分解
    [~, ord] = sort(diag(D), 'descend');
    V = V(:, ord);
    % 主成分方向只在符号上不唯一，故比较投影的绝对值
    a = abs(b * PCup(:, 1:k));
    e = abs(b * V(:, 1:k));
end

% ------------------------------------------------------------------ harness

function run_script(full)
% Run an upstream script in the base workspace; it is expected to set its own
% data and clc/clear. Errors propagate to the caller.
    evalin('base', 'clear');
    evalin('base', sprintf('run(''%s'')', strrep(full, '''', '''''')));
    evalin('base', 'close all force');
end

function [np,nf,ns] = chk(out, np, nf, ns, name, fn)
    try
        [a, e] = fn();
    catch err
        fprintf(out, 'ERROR\t%s\t%s\n', name, msg(err));
        fprintf('ERROR  %s | %s\n', name, msg(err));
        ns = ns + 1; return
    end
    a = a(:)'; e = e(:)';
    if numel(a) == numel(e) && all(abs(a - e) < 1e-6)
        fprintf(out, 'PASS\t%s\n', name); fprintf('PASS   %s\n', name); np = np + 1;
    else
        fprintf(out, 'FAIL\t%s\n\tupstream=%s\n\tindependent=%s\n', ...
            name, mat2str(a,6), mat2str(e,6));
        fprintf('FAIL   %s\n        upstream   =%s\n        independent=%s\n', ...
            name, mat2str(a,6), mat2str(e,6));
        nf = nf + 1;
    end
end

function s = msg(e), s = strrep(char(e.message), sprintf('\n'), ' '); end
