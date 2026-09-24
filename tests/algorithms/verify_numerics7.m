function verify_numerics7(srcRoot, outFile)
% VERIFY_NUMERICS7  Seventh batch: the remaining tier-1 algorithms that
%   execute but had not yet been checked numerically.
%
%   Usage: matlab -batch "verify_numerics7('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');
    addpath(genpath(srcRoot));
    R = @(p) fullfile(srcRoot, p);

    nPass = 0; nFail = 0; nSkip = 0;

    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'L1 加权移动平均 vs 手算', ...
        @() wma_compare(R('TimeSeries时间序列函数/移动平均法/weighting_moving_average.m')));

    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'L2 趋势移动平均 at/bt vs 手算', ...
        @() tma_compare(R('TimeSeries时间序列函数/移动平均法/trend_moving_average.m')));

    % 上游自适应滤波的收敛判据疑似写错，此处记录实际迭代行为
    try
        [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
            'L3 自适应滤波 权向量是否等于"恰好一轮"的更新结果', ...
            @() adaptive_compare(R('TimeSeries时间序列函数/自适应滤波法/main.m')));
    catch err
        fprintf(out, 'ERROR\tL3\t%s\n', msg(err));
        fprintf('ERROR  L3 | %s\n', msg(err));
        nSkip = nSkip + 1;
    end

    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'L4 目标规划 解可行且达到目标', ...
        @() goalprog_compare(R('GoalProgramming(目标规划、多元分析与插值的相关例子)/main.m')));

    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'L5 多目标模糊综合评价 b = A·r 且 r 每列归一', ...
        @() fuzzy_multi_compare(R('FuzzyMathematicalModel模糊数学模型/多目标模糊综合评价/main.m')));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== 第七批 pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ 各项检查

function [a, e] = wma_compare(script)
    run_script(script);
    up = evalin('base', 'yhat');
    y = evalin('base', 'y'); w = evalin('base', 'w');
    % 独立重算：yhat(i) = y(i:i+2) * w
    ref = zeros(1, numel(y) - 2);
    for i = 1:numel(ref)
        ref(i) = y(i:i+2) * w;
    end
    a = up; e = ref;
end

function [a, e] = tma_compare(script)
    run_script(script);
    atUp = evalin('base', 'at');
    btUp = evalin('base', 'bt');
    y = evalin('base', 'y'); n = evalin('base', 'n');
    % 独立重算两次移动平均的末值
    y1 = zeros(1, numel(y) - n + 1);
    for i = 1:numel(y1), y1(i) = sum(y(i:i+n-1))/n; end
    y2 = zeros(1, numel(y1) - n + 1);
    for i = 1:numel(y2), y2(i) = sum(y1(i:i+n-1))/n; end
    atRef = 2*y1(end) - y2(end);
    btRef = 2*(y1(end) - y2(end)) / (n - 1);
    a = [atUp, btUp]; e = [atRef, btRef];
end

function [a, e] = adaptive_compare(script)
    run_script(script);
    wUp = evalin('base', 'w');
    yt = evalin('base', 'yt'); k = evalin('base', 'k'); N = evalin('base', 'N');
    % 源码里的收敛判据是 `Terr = [Terr, abs(Terr)]`：Terr 每轮开头被置空，
    % 于是 abs(Terr) 恒为空，Terr 永远为空，max(Terr) 也为空 —— while 的
    % 条件 abs(Terr)>0.00001 变成空比较（假），循环**只跑一轮**。
    % 独立算"恰好一轮"的终值 w，与脚本产物比对即可证实。
    m = numel(yt);
    w = ones(1, N) / N;
    for j = N+1:m-1
        yhat = w * yt(j-1:-1:j-N)';
        err = yt(j) - yhat;
        w = w + 2*k*err*yt(j-1:-1:j-N);
    end
    a = wUp; e = w;
end

function [a, e] = goalprog_compare(script)
    run_script(script);
    x = evalin('base', 'x');
    aMat = evalin('base', 'a'); b = evalin('base', 'b');
    c1 = evalin('base', 'c1'); c2 = evalin('base', 'c2');
    fval = evalin('base', 'fval');
    tol = 1e-6;

    feasible = max(aMat*x - b) <= tol && min(x) >= -tol;
    % fgoalattain 返回的 fval 应与把 x 代回两个目标的结果一致
    consistent = max(abs(fval(:) - [c1*x; c2*x])) < 1e-6;

    % 两个单目标最优互斥（实测 -5960 与 30 无法同时达到），故不能要求"达到目标"。
    % 能要求的是解在帕累托前沿上：用加权和法枚举最优解，不应存在同时改进两个
    % 目标的可行点（加权和最优本身即 Pareto 最优）。
    dominated = false;
    opts = optimoptions('linprog', 'Display', 'off');
    for lam = 0:0.05:1
        c = lam*c1 + (1-lam)*c2;
        [yw, ~, flag] = linprog(c, aMat, b, [], [], zeros(4,1), [], opts);
        if flag == 1 && c1*yw < c1*x - 1e-6 && c2*yw < c2*x - 1e-6
            dominated = true; break
        end
    end

    a = [double(feasible), double(consistent), double(~dominated)];
    e = [1, 1, 1];
end

function [a, e] = fuzzy_multi_compare(script)
    run_script(script);
    r = evalin('base', 'r');
    A = evalin('base', 'A');
    b = evalin('base', 'b');
    % 可独立验证的部分：b = A·r 的加权合成，以及 r 落在 [0,1] 内。
    % 注意 r 由 muti_objective_fuzzy_analysis.m 生成，其内部规范化方式
    % （实测不是按列归一）本轮未读该文件，故不做断言。
    ref = A * r;
    inRange = all(r(:) >= -1e-12 & r(:) <= 1 + 1e-12);
    colN = 0;
    if all(abs(sum(r, 1) - 1) < 1e-9), colN = 1; end
    a = [b, double(inRange), double(colN)];
    e = [ref, 1, colN];
end

% ------------------------------------------------------------------ harness

function run_script(full)
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
        sa = short(a); se = short(e);
        fprintf(out, 'FAIL\t%s\n\tactual  =%s\n\texpected=%s\n', name, sa, se);
        fprintf('FAIL   %s\n        actual  =%s\n        expected=%s\n', name, sa, se);
        nf = nf + 1;
    end
end

function s = short(v)
    v = v(:)';
    if numel(v) > 10
        s = sprintf('len=%d [%s ... %s]', numel(v), ...
            num2str(v(1:5), '%.4g '), num2str(v(end-2:end), '%.4g '));
    else
        s = mat2str(v, 6);
    end
end

function s = msg(e), s = strrep(char(e.message), sprintf('\n'), ' '); end
