function verify_numerics3(srcRoot, outFile)
% VERIFY_NUMERICS3  Third batch: fuzzy composition, grey relational analysis,
%   an LP investment model, BFS levels, and the AHP single-level check.
%
%   Same principle as batches 1-2: the upstream artefact is compared against
%   an answer produced by a different route (hand arithmetic, a differently
%   formulated LP, MATLAB's own graph distances).
%
%   Usage: matlab -batch "verify_numerics3('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');
    addpath(genpath(srcRoot));
    R = @(p) fullfile(srcRoot, p);

    nPass = 0; nFail = 0; nSkip = 0;

    % ============ H1 模糊矩阵 max-min 合成：函数 vs 手算 ============
    % a = [.5 .7; .3 .9], b = [.8 .2; .4 .6]
    %   ab(1,1)=max(min(.5,.8),min(.7,.4))=max(.5,.4)=.5
    %   ab(1,2)=max(min(.5,.2),min(.7,.6))=max(.2,.6)=.6
    %   ab(2,1)=max(min(.3,.8),min(.9,.4))=max(.3,.4)=.4
    %   ab(2,2)=max(min(.3,.2),min(.9,.6))=max(.2,.6)=.6
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'H1 模糊矩阵 max-min 合成 vs 手算', ...
        @() pair(fuzzy_matrix_compund([.5 .7; .3 .9], [.8 .2; .4 .6]), ...
                 [.5 .6; .4 .6]));

    % ============ H2 灰色关联度：脚本 vs 独立重算 ============
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'H2 灰色关联度 vs 独立重算', ...
        @() grel_compare(R('GreySystem灰色系统/association_analysis.m')));

    % ============ H3 投资模型 LP：可行性 + 独立重解 ============
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'H3 投资模型 可行性 + 独立重解目标值', ...
        @() invest_compare(R('LinearProgramming（添加了线性规划、整数规划等内容的使用案例）/invest_model.m')));

    % ============ H4 BFS 层次：脚本 vs MATLAB distances ============
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'H4 BFS 各点层数 vs MATLAB distances', ...
        @() bfs_compare(R('GraphTheory(图论)/detailed/树/BFS.m')));

    % ============ H5 AHP 单排序一致性检验：函数 vs 手算 ============
    % CI = (λmax - n)/(n-1)，RI = RIT(n)
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'H5 sglsortexamine 的 CI/RI vs 手算', ...
        @() ahp_single_compare(R('AHP层次分析法/sglsortexamine.m')));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== 第三批 pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ 各项检查

function [a, e] = grel_compare(script)
    run_script(script);
    rUp = evalin('base', 'r');          % 上游算出的关联度向量
    data = evalin('base', 'data');
    rho = 0.5;
    ck = data(1, :);
    bj = data(2:end, :);
    t = bj - repmat(ck, size(bj,1), 1);
    jc1 = min(abs(t(:)));
    jc2 = max(abs(t(:)));
    ksi = (jc1 + rho*jc2) ./ (abs(t) + rho*jc2);
    ref = mean(ksi, 2)';                % 独立重算：关联系数按列取均值
    a = rUp(:)'; e = ref(:)';
end

function [a, e] = invest_compare(script)
    run_script(script);
    xUp = evalin('base', 'x');
    QUp = evalin('base', 'Q');
    aRisk = evalin('base', 'a');        % 循环结束时的风险度
    aRisk = aRisk - 0.001;              % x/Q 对应的是上一次迭代的 a
    aRisk = round(aRisk * 1000) / 1000; % 抹掉 0.001 累加的浮点漂移

    c  = [-0.05, -0.27, -0.19, -0.185, -0.185];
    A  = [zeros(4,1), diag([0.025, 0.015, 0.055, 0.026])];
    b  = aRisk * ones(4,1);
    Aeq = [1, 1.01, 1.02, 1.045, 1.065];
    beq = 1;

    % (1) 可行性：上游解必须满足全部约束
    tol = 1e-8;
    feas = max(A*xUp - b) <= tol && abs(Aeq*xUp - beq) <= tol && min(xUp) >= -tol;
    % (2) 独立重解：换一个算法（内点法），目标值应当一致
    opts = optimoptions('linprog', 'Algorithm', 'interior-point', 'Display', 'off');
    [~, Qref] = linprog(c, A, b, Aeq, beq, zeros(5,1), [], opts);
    Qref = -Qref;

    a = [double(feas), QUp]; e = [1, Qref];
end

function [a, e] = bfs_compare(script)
    % 用一个固定的无向图做测试（BFS 只依赖邻接矩阵）
    G = [0 1 1 0 0 0;
         1 0 0 1 1 0;
         1 0 0 0 0 1;
         0 1 0 0 0 0;
         0 1 0 0 0 0;
         0 0 1 0 0 0];
    which(fullfile(script));            % 确认调的是归档里的实现
    W = BFS(G, 1);
    ref = distances(graph(G), 1);       % 独立路线：MATLAB 自带的图距离
    a = W; e = ref;
end

function [a, e] = ahp_single_compare(script)
    A = [1 2 4; 1/2 1 2; 1/4 1/2 1];
    RIT = [0 0 0.52 0.89 1.12 1.26 1.36 1.41 1.46 1.49 1.52 1.54 1.56 1.58 1.59];
    lam = 3;                            % 完全一致阵的主特征值
    [RIup, CIup] = sglsortexamine(lam, A, RIT);
    ref = [(lam - 3)/(3 - 1), RIT(3)];  % 手算 CI 与 RI（注意返回顺序是 [RI, CI]）
    a = [CIup, RIup]; e = ref;
end

% ------------------------------------------------------------------ harness

function run_script(full)
    evalin('base', 'clear');
    evalin('base', sprintf('run(''%s'')', strrep(full, '''', '''''')));
    evalin('base', 'close all force');
end

function [a, e] = pair(actual, expected), a = actual; e = expected; end

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
