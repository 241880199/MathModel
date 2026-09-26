function L = parity_ca(S, steps, seedIJ)
% 二维奇偶规则元胞自动机 —— 净室重写
%
%   规则：每格的下一状态 = 其 8 邻域取值之和 mod 2。
%
%   替代上游 CellularAutomata元胞向量机/初等元胞自动机/basic_CA.m。上游
%   **并未真正迭代**：它每一步只更新当前外圈（第 t 步只写半径 t-1 的那一圈），
%   所以任一格子一生只被计算一次。其注释写的是"每一时间每一点……"，实现与
%   注释不符。实测（S=121，61 层，中心单点种子）：
%       上游终态 1 的个数 = 4369
%       按规则迭代      = 416
%   两者相差 4241 格，遍布全图——不是边界效应，是根本没迭代。
%
% 用法
%   L = parity_ca()              默认 S=121，迭代到图案抵达边界
%   L = parity_ca(S, steps)      指定边长与迭代步数
%   L = parity_ca(S, steps, [i j])  指定种子位置
%
% 输出
%   L   S×S 的 0/1 矩阵，为迭代 steps 步后的状态
%
% 规则本身是教科书内容（二维 CA 的奇偶/模 2 规则），与 COMAP 无关。

    if nargin < 1 || isempty(S), S = 121; end
    if nargin < 2 || isempty(steps), steps = (S - 1) / 2; end
    if nargin < 3 || isempty(seedIJ), seedIJ = [(S+1)/2, (S+1)/2]; end

    L = zeros(S);
    L(seedIJ(1), seedIJ(2)) = 1;

    K = ones(3); K(2, 2) = 0;          % 8 邻域核，中心取 0
    for t = 1:steps
        L = mod(conv2(L, K, 'same'), 2);
    end
end
