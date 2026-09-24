function verify_fixed(fixedDir, outFile)
% VERIFY_FIXED  Numerical checks for the clean-room rewrites in fixed/.
%
%   Each rewrite is checked against an answer that is independent of the
%   implementation under test:
%     - an exactly solvable instance (perfectly consistent AHP matrix);
%     - a hand-computed short sequence (exponential smoothing);
%     - a round trip, data generated from known parameters (trend extrapolation);
%     - arithmetic done by hand in the comments (fuzzy evaluation).
%
%   Usage: matlab -batch "verify_fixed('D:/.../fixed','out.txt')"

    fixedDir = char(fixedDir);
    addpath(fixedDir);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    nPass = 0; nFail = 0;

    % ================= F1  AHP：完全一致阵，解可精确写出 =================
    % A = [1 2 4; 1/2 1 2; 1/4 1/2 1] 各行成比例 -> lambda_max = 3,
    % CI = 0, CR = 0, 权重 = [4 2 1]/7
    A = [1 2 4; 1/2 1 2; 1/4 1/2 1];
    wWant = [4 2 1] / 7;
    [nPass,nFail] = t(out,nPass,nFail,'F1a AHP 一致阵权重 = [4 2 1]/7', ...
        @() deal2(ahp(A), wWant));
    [nPass,nFail] = t(out,nPass,nFail,'F1b AHP 一致阵 lambda = 3', ...
        @() deal2(nthout(@() ahp(A), 4), 3));
    [nPass,nFail] = t(out,nPass,nFail,'F1c AHP 一致阵 CR = 0', ...
        @() deal2(nthout(@() ahp(A), 2), 0));

    % 三种近似法在同一矩阵上应当彼此接近（互为独立算法）
    [nPass,nFail] = t(out,nPass,nFail,'F1d AHP 特征值法 vs 方根法（互校）', ...
        @() deal2(ahp(A,'eig'), ahp(A,'sqrt')));
    [nPass,nFail] = t(out,nPass,nFail,'F1e AHP 方根法 vs 和积法（互校）', ...
        @() deal2(ahp(A,'sqrt'), ahp(A,'sum')));

    % 非互反矩阵必须被拒绝——上游 ahp_common.m 的示例矩阵本身就不互反
    [nPass,nFail] = t(out,nPass,nFail,'F1f AHP 拒绝非互反矩阵（应报错）', ...
        @() deal2(expect_error(@() ahp([1 2 3; 1/2 1 4; 1/6 1/4 1])), 0));

    % ================= F2  一次指数平滑：手算 =================
    % y = [10 12 14], alpha = 0.5
    %   S(1)=10, S(2)=.5*12+.5*10=11, S(3)=.5*14+.5*11=12.5
    %   拟合: yhat(2)=S(1)=10, yhat(3)=S(2)=11
    %   一步预报 = S(3) = 12.5
    [nPass,nFail] = t(out,nPass,nFail,'F2a 一次平滑 一步预报 = 12.5', ...
        @() deal2(nthout(@() exponential_smoothing([10 12 14], 0.5), 2), 12.5));
    [nPass,nFail] = t(out,nPass,nFail,'F2b 一次平滑 拟合值 [_,10,11]', ...
        @() deal2(idx(nthout(@() exponential_smoothing([10 12 14],0.5),1), 2:3), [10 11]));

    % ================= F3  趋势外推：往返 =================
    % 由已知参数生成无噪数据，估计器应能复原模型（拟合误差≈0）
    t15 = 1:15;                 % 三和法约定 t 从 1 起
    K = 200; a = -150; b = 0.7;
    ymod = K + a * b.^t15;
    [nPass,nFail] = t(out,nPass,nFail,'F3a 修正指数 往返拟合 max|误差|≈0', ...
        @() deal2(max(abs(nthout(@() trend_extrapolation(ymod,'modified'),2) - ymod)), 0));
    [nPass,nFail] = t(out,nPass,nFail,'F3b 修正指数 复原 K=200', ...
        @() deal2(getfield(nthout(@() trend_extrapolation(ymod,'modified'),1), 'K'), K));

    yK = 500; ya = 0.02; yb = 0.6;
    ycom = yK * ya.^(yb.^t15);
    [nPass,nFail] = t(out,nPass,nFail,'F3c Compertz 往返拟合 max|误差|≈0', ...
        @() deal2(max(abs(nthout(@() trend_extrapolation(ycom,'compertz'),2) - ycom)), 0));

    yLK = 100; yLa = 20; yLb = 0.8;
    ylog = yLK ./ (1 + yLa * exp(-yLb * t15));
    [nPass,nFail] = t(out,nPass,nFail,'F3d Logistic 往返拟合 max|误差|≈0', ...
        @() deal2(max(abs(nthout(@() trend_extrapolation(ylog,'logistic'),2) - ylog)), 0));

    % ================= F4  模糊综合评价：手算 =================
    % w = [.5 .5], R = [.6 .4; .2 .8]
    %   M4: B = [.5*.6+.5*.2, .5*.4+.5*.8] = [.4 .6]
    %   M1: b_j = max_i min(w_i, r_ij) = [.5 .5]
    R = [0.6 0.4; 0.2 0.8];
    [nPass,nFail] = t(out,nPass,nFail,'F4a 模糊评价 M4 = [.4 .6]', ...
        @() deal2(nthout(@() fuzzy_evaluation(R,[.5 .5],'M4'),1), [0.4 0.6]));
    [nPass,nFail] = t(out,nPass,nFail,'F4b 模糊评价 M1 = [.5 .5]', ...
        @() deal2(nthout(@() fuzzy_evaluation(R,[.5 .5],'M1'),1), [0.5 0.5]));
    % 综合得分 = B·grades' = [.4 .6]·[1;5] = 3.4（R 只有 2 个评价等级）
    [nPass,nFail] = t(out,nPass,nFail,'F4c 模糊评价 综合得分 = 3.4', ...
        @() deal2(nthout(@() fuzzy_evaluation(R,[.5 .5],'M4',[1 5]),2), 3.4));

    fprintf(out, '# RESULT pass=%d fail=%d\n', nPass, nFail);
    fclose(out);
    fprintf('\n==== fixed/ 验证: pass=%d fail=%d ====\n', nPass, nFail);
end

% ------------------------------------------------------------------ harness

function [np,nf] = t(out, np, nf, name, fn)
    try
        [got, want] = fn();
    catch err
        fprintf(out, 'ERROR\t%s\t%s\n', name, msg(err));
        fprintf('ERROR  %s | %s\n', name, msg(err));
        nf = nf + 1; return
    end
    if numel(got) == numel(want) && all(abs(got(:) - want(:)) < 1e-6)
        fprintf(out, 'PASS\t%s\n', name); fprintf('PASS   %s\n', name); np = np + 1;
    else
        fprintf(out, 'FAIL\t%s\tgot=%s want=%s\n', name, mat2str(got,6), mat2str(want,6));
        fprintf('FAIL   %s  got=%s want=%s\n', name, mat2str(got,6), mat2str(want,6));
        nf = nf + 1;
    end
end

function [a, b] = deal2(a, b), a = a(:)'; b = b(:)'; end
function r = idx(v, k), r = v(k); end
function r = nthout(fn, k)
% Call fn() and return its k-th output.
    outs = cell(1, k);
    [outs{1:k}] = fn();
    r = outs{k};
end
function r = expect_error(fn)
% Passes when fn() throws; returns a sentinel the harness compares to 0.
    try
        fn();
        r = NaN;                 % no error -> sentinel that never matches 0
    catch
        r = 0;
    end
end
function s = msg(e), s = strrep(char(e.message), sprintf('\n'), ' '); end
