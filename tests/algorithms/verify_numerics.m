function verify_numerics(srcRoot, outFile)
% VERIFY_NUMERICS  Numerical correctness checks for the archived algorithms.
%
%   "Runs without error" is not correctness. Each check compares the archive's
%   implementation against an INDEPENDENT reference:
%     - MATLAB built-ins (distances / minspantree / maxflow) -- separately
%       written and well tested implementations of the same problem;
%     - hand-computed textbook instance answers;
%     - brute-force enumeration over all tours (TSP).
%
%   Inf/NaN are compared semantically (Inf == Inf counts as equal), because
%   several of these routines signal "unreachable" with Inf.
%
%   Usage: matlab -batch "verify_numerics('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');

    g = fullfile(srcRoot, 'GraphTheory(图论)');
    addpath(fullfile(g, 'basic'));
    addpath(fullfile(g, 'detailed', '最短路'));
    addpath(fullfile(g, 'detailed', '树'));
    addpath(fullfile(srcRoot, 'AHP层次分析法'));
    addpath(fullfile(srcRoot, 'GreySystem灰色系统'));

    nPass = 0; nFail = 0; nSkip = 0;

    % ---- shared instance: classic 6-node directed, weighted graph ------
    W = inf(6);
    W(1,2)=7; W(1,3)=9; W(1,6)=14; W(2,3)=10; W(2,4)=15;
    W(3,4)=11; W(3,6)=2; W(4,5)=6; W(6,5)=9;
    W(1:7:36) = 0;                       % zero the diagonal
    expRow1 = [0 7 9 20 20 11];          % hand-computed from the textbook

    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N1 Floyd 全矩阵 vs MATLAB distances(G)', ...
        @() as_pair(Floyd(W), builtin_allpairs(W)));
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N2 Floyd 首行 vs 手算教科书值', @() as_pair(floyd_row1(W), expRow1));
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N3 Dijkf 单源 vs 手算教科书值', @() as_pair(Dijkf(W,1), expRow1));
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N4 Floyd 与 Dijkf 交叉一致', @() as_pair(floyd_row1(W), Dijkf(W,1)));
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N5 Huffman 最优带权路径长度 [1 2 3 4 5] = 33', ...
        @() as_pair(huffman_cost([1 2 3 4 5]), 33));

    % ---- AHP: ahp.m is the corrected routine ---------------------------
    A = [1 2 3; 1/2 1 4; 1/6 1/4 1];
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N6 ahp.m 权向量 vs 独立求主特征向量', ...
        @() as_pair(ahp_weight(A), ahp_ref(A)));

    % ---- grTheory toolbox vs MATLAB built-ins --------------------------
    Ed = [1 2 7; 1 3 9; 1 6 14; 2 3 10; 2 4 15; 3 4 11; 3 6 2; 4 5 6; 6 5 9];
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N7 grShortPath 非对角项 vs MATLAB distances', ...
        @() gr_vs_builtin_shortest(Ed));

    Eu = [1 2 2; 1 3 3; 2 3 1; 2 4 4; 3 5 5; 4 5 6];
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N8 grMinSpanTree 总权 vs MATLAB minspantree', ...
        @() as_pair(gr_mst_weight(Eu), matlab_mst_weight(Eu)));

    Ef = [1 2 16; 1 3 13; 2 3 10; 3 2 4; 2 4 12; 4 3 9; 3 5 14; 5 4 7; 4 6 20; 5 6 4];
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N9 grMaxFlows 最大流 vs MATLAB maxflow', ...
        @() as_pair(gr_maxflow(Ef,1,6), matlab_maxflow(Ef,1,6)));

    C = [ 0 16 11 20 13 15;
         16  0 12 18 14 17;
         11 12  0 15 10 19;
         20 18 15  0  9 13;
         13 14 10  9  0 11;
         15 17 19 13 11  0];
    [nPass,nFail,nSkip] = chk(out, nPass, nFail, nSkip, ...
        'N10 grTravSale vs 穷举全排列最优', ...
        @() as_pair(tsp_tour_cost(C, gr_tsp(C)), tsp_bruteforce(C)));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ harness

function r = as_pair(a, b), r = {a(:)', b(:)'}; end  % uniform compare shape

function [np,nf,ns] = chk(out, np, nf, ns, name, fn)
    try
        pair = fn();
    catch err
        fprintf(out, 'ERROR\t%s\t%s\n', name, one_line(err.message));
        fprintf('ERROR  %s | %s\n', name, one_line(err.message));
        ns = ns + 1; return
    end
    a = pair{1}; e = pair{2};
    if same_vec(a, e)
        fprintf(out, 'PASS\t%s\n', name);
        fprintf('PASS   %s\n', name);
        np = np + 1;
    else
        fprintf(out, 'FAIL\t%s\tactual=%s expected=%s\n', name, ...
            mat2str(a, 6), mat2str(e, 6));
        fprintf('FAIL   %s\n        actual  =%s\n        expected=%s\n', ...
            name, mat2str(a, 6), mat2str(e, 6));
        nf = nf + 1;
    end
end

function ok = same_vec(a, e)
% Numeric equality where Inf==Inf and NaN==NaN count as equal.
    if numel(a) ~= numel(e), ok = false; return; end
    d = abs(a(:) - e(:));
    bothInf = isinf(a(:)) & isinf(e(:)) & (sign(a(:)) == sign(e(:)));
    bothNaN = isnan(a(:)) & isnan(e(:));
    d(bothInf | bothNaN) = 0;
    ok = all(d < 1e-6);
end

% ---- Floyd / Dijkstra --------------------------------------------------

function r = floyd_row1(W)
    U = Floyd(W);
    r = U(1, :);
end

function D = builtin_allpairs(W)
% All-pairs shortest distances from MATLAB's own digraph, for cross-checking.
    n = size(W, 1);
    s = []; t = []; wt = [];
    for i = 1:n
        for j = 1:n
            if i ~= j && isfinite(W(i,j))
                s(end+1) = i; t(end+1) = j; wt(end+1) = W(i,j); %#ok<AGROW>
            end
        end
    end
    D = distances(digraph(s, t, wt));
end

function c = huffman_cost(A)
    H = Huffman(A);
    c = sum(H(:, 3));       % each row's 3rd column is one merge cost
end

% ---- AHP ---------------------------------------------------------------

function w = ahp_weight(A)
    [~, w] = ahp(A);
    w = w(:)' / sum(w);     % eigvector sign is arbitrary; normalise
end

function w = ahp_ref(A)
    [V, D] = eig(A);
    d = real(diag(D));
    [~, k] = max(d);        % the CORRECT way: take the max, not d(1,1)
    v = real(V(:, k));
    w = v / sum(v);
    w = w(:)' / sum(w);
end

% ---- grTheory ----------------------------------------------------------

function r = gr_vs_builtin_shortest(Ed)
    % grShortPath leaves the diagonal as Inf (MATLAB's distances uses 0);
    % the diagonal is a convention difference, so compare off-diagonal only.
    dSP = grShortPath(Ed);
    D = distances(digraph(Ed(:,1), Ed(:,2), Ed(:,3)));
    n = size(dSP, 1);
    offDiag = setdiff(1:n*n, 1:n+1:n*n);      % linear indices, diagonal removed
    r = {dSP(offDiag), D(offDiag)};
end

function w = gr_mst_weight(Eu)
    % grMinSpanTree returns a COLUMN VECTOR OF EDGE INDICES into Eu,
    % not an edge list -- see basic/readme.txt and the function tail.
    idx = grMinSpanTree(Eu);
    w = sum(Eu(idx(:), 3));
end

function w = matlab_mst_weight(Eu)
    G = graph(Eu(:,1), Eu(:,2), Eu(:,3));
    T = minspantree(G);
    w = sum(T.Edges.Weight);
end

function v = gr_maxflow(Ef, s, t), v = grMaxFlows(Ef, s, t); end
function v = matlab_maxflow(Ef, s, t)
    G = digraph(Ef(:,1), Ef(:,2), Ef(:,3));
    v = maxflow(G, s, t);
end

function p = gr_tsp(C)
    [p, ~] = grTravSale(C);
    p = p(:)';
end

function c = tsp_tour_cost(C, p)
    p = p(:)';
    if numel(p) > 1 && p(1) == p(end), p(end) = []; end
    c = 0;
    for i = 1:numel(p)-1, c = c + C(p(i), p(i+1)); end
    c = c + C(p(end), p(1));
end

function best = tsp_bruteforce(C)
    n = size(C, 1);
    best = inf;
    for p = perms(2:n)                  % fix city 1 as the start
        c = tsp_tour_cost(C, [1, p]);
        if c < best, best = c; end
    end
end

function s = one_line(s)
    s = strrep(char(s), sprintf('\n'), ' ');
    s = strtrim(s);
end
