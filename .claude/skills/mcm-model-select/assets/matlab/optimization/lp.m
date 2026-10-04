function out = lp(opts)
%LP  Linear programming (LP) via MATLAB `linprog`; zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #1（线性规划）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无语料** —— `corpus/papers/MODEL_MAP.md` 里 `linear programming`（词首锚定）**0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- linear programming（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）。
%   ★ **注意裸模式陷阱**：裸 `linear programming` 会**误命中 `nonlinear programming`**（3 行）——
%     两者是不同方法，必须用词首锚定把 `non` 挡掉。⇒ 本方法标 `[社区]`（教科书级常识）。
%   **算法素材面**：`corpus/algorithms/src/LinearProgramming（添加了线性规划、整数规划等内容的使用案例）/`
%   （含 `solve_lp.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例）：
%     max z = 3*x1 + 5*x2  s.t. x1 <= 4, 2*x2 <= 12, 3*x1 + 2*x2 <= 18, x >= 0
%     顶点枚举： (0,0)=0 · (4,0)=12 · (4,3)=27 · (2,6)=36 · (0,6)=30 ⇒ 最优 (2,6), z=36。
%   ★ 手算算式与逐顶点读数见 `tests/skills/model-select/verify/lp.md`。
%   ★★ **本骨架用 `linprog` 只是"实现"**，**不是独立参照** —— 拿同机同实现当参照不构成独立验证（任务书 B）。
%
%   用法：
%     lp()             % 自检并打印做题读数
%     out = lp(opts)   % opts.c opts.A opts.b opts.lb
%
%   返回 struct：x, z, fval, exitflag。

if nargin < 1 || isempty(opts); opts = struct(); end
c = dflt(opts, 'c', -[3 5]);              % min c'x（max 3x1+5x2 ⇔ min -3x1-5x2）
A = dflt(opts, 'A', [1 0; 0 2; 3 2]);
b = dflt(opts, 'b', [4; 12; 18]);
lb = dflt(opts, 'lb', [0 0]);

options = optimoptions('linprog', 'Display', 'off');
[x, fval, exitflag] = linprog(c, A, b, [], [], lb, [], options);
z = -fval;                                % 回到 max 口径

out = struct('x', x, 'z', z, 'fval', fval, 'exitflag', exitflag);

fprintf('[lp] max 3*x1 + 5*x2  s.t. x1<=4, 2*x2<=12, 3*x1+2*x2<=18, x>=0\n');
fprintf('  exitflag = %d\n', exitflag);
fprintf('  x* = [%s]\n', num2str(x(:).', '%.10g  '));   % ★ x(:).' —— 列向量直接 num2str 会拼成乱序
fprintf('  z* = %.10g\n', z);
fprintf('  （手算最优 (2,6)、z=36 —— 见 verify/lp.md）\n');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
