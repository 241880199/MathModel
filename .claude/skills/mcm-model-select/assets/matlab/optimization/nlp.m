function out = nlp(opts)
%NLP  Nonlinear programming (NLP) via MATLAB `fmincon`; zero-arg self-test.
%
%   M4 `mcm-model-select` 骨架 · optimization #3（非线性规划）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `nonlinear programming` 命中 **3 篇**
%   （`P2025-B-01` · `P2025-D-01` · `P2025-E-02`；2026-10-04 当场复跑
%   `grep -nE "^ +- nonlinear programming（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 3 行，去重并集 3 篇）。
%   **算法素材面**：`corpus/algorithms/src/NonLinearProgramming非线性规划/`（含 `non_linear_prog.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例）：
%     min f = (x1-1)^2 + (x2-2)^2  s.t. x1 + x2 <= 2, x1,x2 >= 0
%     无约束极小 (1,2) 越界（3>2）⇒ 取边界 x1+x2=2：代 y=2-x1 ⇒ f = 2*x1^2-2*x1+1，df/dx1=0 ⇒ x1=0.5, x2=1.5, f=0.5。
%   ★ 手算算式见 `tests/skills/model-select/verify/nlp.md`。
%   ★★ `fmincon` 只是本骨架的**实现**；**不作独立参照**（同机同实现，任务书 B）。
%
%   用法：
%     nlp()             % 自检并打印读数
%     out = nlp(opts)   % opts.x0 opts.A opts.b opts.lb
%
%   返回 struct：x, fval, exitflag。

if nargin < 1 || isempty(opts); opts = struct(); end
fun = @(x) (x(1) - 1)^2 + (x(2) - 2)^2;
x0  = dflt(opts, 'x0', [0 0]);
A   = dflt(opts, 'A', [1 1]);
b   = dflt(opts, 'b', 2);
lb  = dflt(opts, 'lb', [0 0]);

opts_fmin = optimoptions('fmincon', 'Display', 'off', 'Algorithm', 'sqp');
[x, fval, exitflag] = fmincon(fun, x0, A, b, [], [], lb, [], [], opts_fmin);

out = struct('x', x, 'fval', fval, 'exitflag', exitflag);

fprintf('[nlp] min (x1-1)^2 + (x2-2)^2  s.t. x1+x2 <= 2, x>=0\n');
fprintf('  exitflag = %d\n', exitflag);
fprintf('  x* = [%s]\n', num2str(x(:).', '%.10g  '));   % ★ x(:).' —— 列向量直接 num2str 会拼成乱序
fprintf('  f* = %.10g\n', fval);
fprintf('  （手算最优 (0.5,1.5)、f=0.5 —— 见 verify/nlp.md）\n');
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
