function [tour, totalW] = euler_circuit(d)
% 欧拉回路 —— 净室重写（Hierholzer 算法）
%
%   替代上游 GraphTheory(图论)/detailed/Euler图和Hamilton图/Fleuf1.m。上游实现
%   给出的是**非法结果**：在 5 点完全图 K5 上它把边 {3,4}、{2,3} 各用了两次，
%   漏掉 {1,2}、{1,4}；在简单 5 环 1-2-3-4-5-1 上它把边 {1,5} 用了两次、漏掉
%   {1,2}，且返回的边序列首尾不相接（游走本身断开）。两例均实测复现。
%
% 用法
%   [tour, totalW] = euler_circuit(d)
%
% 输入
%   d   n×n 权值矩阵，d(i,j) ≠ 0 表示存在边，其值即权（无向图应给对称矩阵）
%
% 输出
%   tour    1×(m+1) 的顶点序列，m 为边数；tour(1) == tour(end)，序列中相邻两点
%           必相邻，且**每条边恰好用一次**
%   totalW  回路总权
%
% 判据：存在欧拉回路 <=> 图连通（忽略孤立点）且所有顶点度为偶数。
% Hierholzer 算法属教科书内容，与 COMAP 无关。

    if ~ismatrix(d) || size(d,1) ~= size(d,2)
        error('euler_circuit:notSquare', 'd 必须是方阵');
    end
    n = size(d, 1);
    A = (d ~= 0);                       % 邻接（0 权视为无边）
    deg = sum(A, 2);

    if any(mod(deg, 2) ~= 0)
        error('euler_circuit:oddDegree', ...
            '存在奇度顶点，无欧拉回路：%s', mat2str(find(mod(deg,2) ~= 0)'));
    end

    live = find(deg > 0);
    if isempty(live)
        tour = []; totalW = 0; return
    end
    if ~connected(A, live)
        error('euler_circuit:disconnected', '图不连通（忽略孤立点后），无欧拉回路');
    end

    % ---- Hierholzer：沿边走直到回到起点，再把途中的环“接”回主回路 ----
    stack = live(1);
    tour = [];
    while ~isempty(stack)
        v = stack(end);
        nb = find(A(v, :), 1);
        if isempty(nb)
            tour = [v, tour];           %#ok<AGROW>  该点已无未用边，收入回路
            stack(end) = [];
        else
            A(v, nb) = false; A(nb, v) = false;     % 消耗这条边
            stack(end+1) = nb;          %#ok<AGROW>
        end
    end

    if tour(1) ~= tour(end)
        tour = [tour, tour(1)];         % 显式闭合
    end

    totalW = 0;
    for i = 1:numel(tour)-1
        totalW = totalW + d(tour(i), tour(i+1));
    end
end

function ok = connected(A, live)
    n = size(A, 1);
    seen = false(1, n);
    seen(live(1)) = true;
    q = live(1);
    while ~isempty(q)
        v = q(1); q(1) = [];
        nb = find(A(v, :) & ~seen);
        seen(nb) = true;
        q = [q, nb];                    %#ok<AGROW>
    end
    ok = all(seen(live));
end
