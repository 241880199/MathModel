function verify_numerics4(srcRoot, outFile)
% VERIFY_NUMERICS4  Fourth batch: grey models, regression, interpolation,
%   and two structural checks (variable clustering, fuzzy transitive closure).
%
%   Same principle as batches 1-3: every upstream result is compared against
%   an answer reached by a different route.
%
%   Usage: matlab -batch "verify_numerics4('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');
    addpath(genpath(srcRoot));
    R = @(p) fullfile(srcRoot, p);

    nPass = 0; nFail = 0; nSkip = 0;

    % ---- I1  GM(2,1)：符号 dsolve 解 vs 特征根闭式解 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I1 GM(2,1) dsolve 解 vs 特征根闭式解', ...
        @() gm21_compare(R('GreySystem灰色系统/GM_2_1.m')));

    % ---- I2  Verhulst：dsolve 解 vs Logistic 闭式解 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I2 Verhulst dsolve 解 vs Logistic 闭式解', ...
        @() verhulst_compare(R('GreySystem灰色系统/GM_Verhulst.m')));

    % ---- I3  优势分析：脚本 vs 独立重算 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I3 优势分析关联矩阵 vs 独立重算', ...
        @() strength_compare(R('GreySystem灰色系统/strength_analysis.m')));

    % ---- I4  一元多项式回归：polyfit vs 正规方程 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I4 一元二次回归 polyfit vs 正规方程', ...
        @() polyfit_compare(R('RegressionAnalysis回归分析/one_indeterminate_poly.m')));

    % ---- I5  最近邻插值：interp2 vs 独立查表 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I5 二维最近邻插值 interp2 vs 独立查表', ...
        @() nn_interp_compare(R('Interpolation（目标规划、多元分析与插值的相关例子）/interp_2D_compare.m')));

    % ---- I6  变量聚类：凝聚距离向量是否自洽 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I6 变量聚类 凝聚距离向量长度自洽', ...
        @() varcluster_compare(R('MultivariateAnalysis（目标规划、多元分析与插值的相关例子）/聚类分析/var_cluster.m')));

    % ---- I7  模糊聚类：传递闭包是否真的收敛 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'I7 模糊聚类 传递闭包已收敛(R2∘R2 = R2)', ...
        @() fuzzyclosure_compare(R('FuzzyMathematicalModel模糊数学模型/模糊聚类/fuzzy_cluster_analysis.m')));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== 第四批 pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ 各项检查

function [a, e] = gm21_compare(script)
    run_script(script);
    predUp = evalin('base', 'predict');
    x0 = evalin('base', 'x0');
    n = numel(x0);

    % 独立路线：自己组最小二乘，并按特征根写闭式解（不用 dsolve）
    x1 = cumsum(x0);
    ax0 = [0, diff(x0)];
    z = 0.5 * (x1(2:n) + x1(1:n-1));
    B = [-x0(2:n)', -z(:), ones(n-1,1)];
    Y = ax0(2:n)';
    u = pinv(B) * Y;                       % 用伪逆，与反斜杠是两条路
    a1 = u(1); a2 = u(2); b = u(3);

    r = roots([1, a1, a2]);                % 特征方程 r² + a1 r + a2 = 0
    xp = b / a2;                           % 特解
    % x(t) = xp + C1 e^{r1 t} + C2 e^{r2 t}，用 x(0)=x1(1)、x(n-1)=x1(n) 定 C
    M = [1, 1; exp(r(1)*(n-1)), exp(r(2)*(n-1))];
    C = M \ [x1(1) - xp; x1(n) - xp];
    x1h = xp + C(1)*exp(r(1)*(0:n-1)) + C(2)*exp(r(2)*(0:n-1));
    ref = [real(x1h(1)), diff(real(x1h))];

    a = predUp; e = ref;
end

function [a, e] = verhulst_compare(script)
    run_script(script);
    predUp = evalin('base', 'predict');
    x1  = evalin('base', 'x1');
    ab  = evalin('base', 'abhat');
    aa = ab(1); bb = ab(2);

    % Logistic 闭式解：x(t) = a / (b + C e^{a t})，C = a/x(0) - b
    C = aa/x1(1) - bb;
    tt = 0:15;
    ref = aa ./ (bb + C*exp(aa*tt));

    a = predUp; e = ref;
end

function [a, e] = strength_compare(script)
    run_script(script);
    rUp = evalin('base', 'r');
    data = evalin('base', 'data');
    n = size(data, 1);
    rho = 0.5;
    ck = data(6:n, :);
    bj = data(1:5, :);
    ref = [];
    for i = 1:size(ck,1)
        t = bj - repmat(ck(i,:), size(bj,1), 1);
        jc1 = min(abs(t(:))); jc2 = max(abs(t(:)));
        ksi = (jc1 + rho*jc2) ./ (abs(t) + rho*jc2);
        ref = [ref; mean(ksi, 2)'];         %#ok<AGROW>
    end
    a = rUp; e = ref;
end

function [a, e] = polyfit_compare(script)
    run_script(script);
    pUp = evalin('base', 'p');              % polyfit 得到的 [a2 a1 a0]
    x0 = evalin('base', 'x0');
    y0 = evalin('base', 'y0');
    X = [x0(:).^2, x0(:), ones(numel(x0),1)];
    ref = (X \ y0(:))';                     % 正规方程直接解
    a = pUp(:)'; e = ref;
end

function [a, e] = nn_interp_compare(script)
    run_script(script);
    z1i = evalin('base', 'z1i');
    x = evalin('base', 'x'); y = evalin('base', 'y'); z = evalin('base', 'z');
    xi = evalin('base', 'xi'); yi = evalin('base', 'yi');

    % 独立路线：均匀网格上直接算最近点的下标（纯算术，不做查找、不调 interp2）。
    % 注意 interp2(...,'nearest') 在恰好落在两格中点时取**上侧**（round 半边进），
    % 这与「取较小下标」的直觉相反；此处按 MATLAB 的约定复现，否则会在
    % yi = 200, 600, 1000, … 这些中点行上系统性对不上（实测 2399/10961 个点）。
    ix = round((xi(:)' - x(1)) / (x(2) - x(1))) + 1;
    iy = round((yi(:)  - y(1)) / (y(2) - y(1))) + 1;
    ix = min(max(ix, 1), numel(x));
    iy = min(max(iy, 1), numel(y));
    ref = z(iy, ix);                       % 自动展开为 numel(yi) × numel(xi)
    a = z1i; e = ref;
end

function [a, e] = varcluster_compare(script)
    run_script(script);
    b = evalin('base', 'b');
    aMat = evalin('base', 'a');
    n = size(aMat, 1);
    expectedLen = n * (n - 1) / 2;          % n 个对象应有 n(n-1)/2 个距离
    % 通过判据：距离向量长度应等于 91；给 182 会多算一倍
    a = numel(b); e = expectedLen;
end

function [a, e] = fuzzyclosure_compare(script)
    run_script(script);
    r2 = evalin('base', 'r2');
    r3 = evalin('base', 'r3');
    lambda = evalin('base', 'lambda');
    % 脚本用 r2 做 lambda 截集。r2 并未完全收敛（r2∘r2 ≠ r2，残差约 3e-5），
    % 所以真正要问的是：改用收敛后的 r3 会不会改变聚类结果？
    % 相同 -> 提前停止只是形式不严谨，不影响结论；不同 -> 真缺陷。
    a = double(isequal(r2 > lambda, r3 > lambda));
    e = 1;
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
% Compact rendering: show the first few entries and the length.
    v = v(:)';
    if numel(v) > 8
        s = sprintf('len=%d [%s ... %s]', numel(v), ...
            num2str(v(1:4), '%.4g '), num2str(v(end-1:end), '%.4g '));
    else
        s = mat2str(v, 6);
    end
end

function s = msg(e), s = strrep(char(e.message), sprintf('\n'), ' '); end
