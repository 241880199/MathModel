function out = difference_equations(opts)
%DIFFERENCE_EQUATIONS  Discrete dynamical systems: linear recurrence, closed form, stability.
%
%   M4 `mcm-model-select` 骨架 · mechanism #4（差分方程 / 离散动力系统 · 稳定性判据）。
%   文件名全 ASCII（GC5）—— 中文名不能作为 MATLAB 函数被调用。
%
%   起点素材（可读、不可当独立参照 —— 它在 corpus/algorithms/src/ 里、不在 fixed/ 六件内，GC6 禁止）：
%     corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH15/rsolve.m
%     （只覆盖线性定常离散系统、用符号 z 变换；本骨架不照它改写。）
%
%   独立参照（第 1 类：解析解 + 收敛阶）：
%     · 标量递推 x_{n+1} = a x_n 的闭式 x_n = a^n x_0；
%     · 稳定性条件 |a| < 1；
%     · 向量递推 x_{n+1} = A x_n 的稳定性 = 谱半径 rho(A) < 1（rho = max|eig(A)|）。
%
%   用法：
%     difference_equations()               % 自检并打印读数
%     out = difference_equations(opts)     % opts.a opts.x0 opts.N opts.A
%
%   返回 struct 字段：x_iter, x_closed, abs_err, spectral_radius, stable。

if nargin < 1 || isempty(opts); opts = struct(); end
a  = dflt(opts, 'a',  0.5);
x0 = dflt(opts, 'x0', 1.0);
N  = dflt(opts, 'N',  10);
A  = dflt(opts, 'A',  [0.8 0.1; 0.0 -0.5]);

% --- 标量递推：数值迭代 vs 闭式解 ---
x = x0;
for n = 1:N
    x = a * x;
end
x_closed = a^N * x0;

% --- 向量递推：谱半径稳定性判据 ---
rho = max(abs(eig(A)));

out = struct('a', a, 'N', N, 'x_iter', x, 'x_closed', x_closed, ...
             'abs_err', abs(x - x_closed), 'spectral_radius', rho, ...
             'stable', rho < 1);

fprintf('[difference_equations] a = %.6g, x0 = %.6g, N = %d\n', a, x0, N);
fprintf('  x_%d (numeric iteration) = %.15g\n', N, x);
fprintf('  a^N * x0 (closed form)   = %.15g\n', x_closed);
fprintf('  absolute error           = %.3e\n', abs(x - x_closed));
fprintf('  spectral radius rho(A)   = %.15g\n', rho);
fprintf('  stable (rho < 1)         = %d\n', rho < 1);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
