function out = ilp_assignment(opts)
%ILP_ASSIGNMENT  Integer / 0-1 programming + assignment problem; zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #2（整数规划 / 指派问题）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `integer programming` 命中 **1 篇**
%   （`P2025-F-02`；2026-10-04 当场复跑 `grep -nE "^ +- integer programming（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行）。
%   **算法素材面**：`corpus/algorithms/src/IntegerProgramming（线性规划、整数规划等内容的使用案例）/`
%   （含 `assgin_integer_prog.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例）：
%     (A) 4x4 指派问题  cost=[9 2 7 8;6 4 3 7;5 8 1 8;7 6 9 4] ⇒ 手算最优代价 = 13（行→列 = 2,1,3,4）。
%     (B) 0-1 背包  max 60*x1+100*x2+120*x3  s.t. 10*x1+20*x2+30*x3 <= 50 ⇒ 手算最优值 = 220（x=[0 1 1]）。
%   ★ 手算算式与枚举见 `tests/skills/model-select/verify/ilp_assignment.md`。
%   ★★ `intlinprog`/`perms` 只是本骨架的**实现**；**不作独立参照**（同机同实现，任务书 B）。
%
%   用法：
%     ilp_assignment()             % 自检并打印两例读数
%     out = ilp_assignment(opts)   % opts.cost opts.v opts.w opts.cap
%
%   返回 struct：assign, cost_min, knap_x, knap_val。

if nargin < 1 || isempty(opts); opts = struct(); end

% --- (A) 指派问题：n 小 ⇒ 全排列穷举（精确） ---
cost = dflt(opts, 'cost', [9 2 7 8; 6 4 3 7; 5 8 1 8; 7 6 9 4]);
n = size(cost, 1);
assert(size(cost, 2) == n, 'cost 必须是方阵');
P = perms(1:n);                              % n! 个排列
vals = zeros(size(P, 1), 1);
for k = 1:size(P, 1)
    idx = sub2ind(size(cost), (1:n).', P(k, :).');
    vals(k) = sum(cost(idx));
end
[cost_min, imin] = min(vals);
assign = P(imin, :);

% --- (B) 0-1 背包：intlinprog ---
v = dflt(opts, 'v', [60 100 120]);
w = dflt(opts, 'w', [10 20 30]);
cap = dflt(opts, 'cap', 50);
nI = numel(v);
opts_ip = optimoptions('intlinprog', 'Display', 'off');
[knap_x, fval] = intlinprog(-v(:), 1:nI, w(:).', cap, [], [], zeros(nI,1), ones(nI,1), opts_ip);
knap_val = -fval;

out = struct('assign', assign, 'cost_min', cost_min, ...
             'knap_x', knap_x(:).', 'knap_val', knap_val);

fprintf('[ilp_assignment] (A) 4x4 指派问题 · 全排列穷举（%d 个排列）\n', size(P, 1));
fprintf('  最优指派（行→列）= %s\n', mat2str(assign));
fprintf('  最小代价 = %.10g\n', cost_min);
fprintf('  （手算最优 = 13 —— 见 verify/ilp_assignment.md）\n');
fprintf('[ilp_assignment] (B) 0-1 背包 · intlinprog\n');
fprintf('  x* = %s\n', mat2str(knap_x(:).'));
fprintf('  最大价值 = %.10g\n', knap_val);
fprintf('  （手算最优 = 220（x=[0 1 1]）—— 见 verify/ilp_assignment.md）\n');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
