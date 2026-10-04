function out = goal_programming(opts)
%GOAL_PROGRAMMING  Weighted goal programming (GP) via MATLAB `linprog`; zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #4（目标规划）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `goal programming` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- goal programming（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/GoalProgramming(目标规划、多元分析与插值的相关例子)/`
%   （含 `main.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例）：
%     min 2*d1^- + 1*d2^-  （硬约束 x1+x2 <= 10, x >= 0）
%     目标1  x1 + 2*x2 + d1^- - d1^+ = 16
%     目标2  2*x1 + x2 + d2^- - d2^+ = 16
%     手算：两目标同时满足需 x1+x2 >= 32/3 > 10 ⇒ 不可行；令硬约束取等 x1+x2=10 ⇒ 代价 = 2*max(0,x1-4)+max(0,6-x1)，
%           在 x1=4 处最小 = 2 ⇒ 最优 (x1,x2)=(4,6)、总偏差代价 = 2。
%   ★ 手算算式见 `tests/skills/model-select/verify/goal_programming.md`。
%   ★★ `linprog` 只是本骨架的**实现**；**不作独立参照**（同机同实现，任务书 B）。
%   ★ 目标规划含**加权式**（本骨架）与**分层（lexicographic）式**两种；分层式靠"按优先级分轮求解、后轮不得恶化前轮"实现。
%
%   用法：
%     goal_programming()             % 自检并打印读数
%     out = goal_programming(opts)   % opts.w1 opts.w2（目标权重）· opts.t1 opts.t2（目标值）
%
%   返回 struct：x, dev, cost, exitflag。

if nargin < 1 || isempty(opts); opts = struct(); end
w1 = dflt(opts, 'w1', 2);    % 目标1 欠量权重
w2 = dflt(opts, 'w2', 1);    % 目标2 欠量权重
t1 = dflt(opts, 't1', 16);   % 目标1 目标值
t2 = dflt(opts, 't2', 16);   % 目标2 目标值

% 变量 z = [x1 x2 d1- d1+ d2- d2+]
c      = [0 0 w1 0 w2 0];
A_ub   = [1 1 0 0 0 0];   b_ub = dflt(opts, 'cap', 10);   % 硬约束 x1+x2 <= 10
A_eq   = [1 2 1 -1 0 0; 2 1 0 0 1 -1];
b_eq   = [t1; t2];
lb     = zeros(1, 6);
options = optimoptions('linprog', 'Display', 'off');
[z, cost, exitflag] = linprog(c, A_ub, b_ub, A_eq, b_eq, lb, [], options);

x   = z(1:2);
dev = struct('d1m', z(3), 'd1p', z(4), 'd2m', z(5), 'd2p', z(6));
out = struct('x', x, 'dev', dev, 'cost', cost, 'exitflag', exitflag);

fprintf('[goal_programming] 加权目标规划 min %.4g*d1^- + %.4g*d2^-（硬约束 x1+x2<=10）\n', w1, w2);
fprintf('  exitflag = %d\n', exitflag);
fprintf('  x* = [%s]\n', num2str(x(:).', '%.10g  '));   % ★ x(:).' —— 列向量直接 num2str 会拼成乱序
fprintf('  偏差 = d1^- %.6g · d1^+ %.6g · d2^- %.6g · d2^+ %.6g\n', z(3), z(4), z(5), z(6));
fprintf('  总偏差代价 = %.10g\n', cost);
fprintf('  （手算最优 (4,6)、代价 = 2 —— 见 verify/goal_programming.md）\n');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
