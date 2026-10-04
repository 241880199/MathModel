function out = reduce_order(opts)
%REDUCE_ORDER  Reduce a 2nd-order ODE to a first-order system; RK4 vs analytic closed form.
%
%   M4 `mcm-model-select` 骨架 · mechanism #3（降阶 / 解析解法）。文件名全 ASCII（GC5）。
%
%   起点素材（可读、不可当独立参照 —— 在 corpus/algorithms/src/ 里、不在 fixed/ 六件内，GC6 禁止）：
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/ReduceDE1.m`（形如 y^(n)=f(x) 的降阶）
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/SeparableVarsDE.m`（可分离变量）
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/HomogenDE.m`（齐次 / 可化为齐次）
%     （本骨架不照它们改写。）
%
%   本题：d2y/dx2 + y = 0，y(0) = 1，dy/dx(0) = 0
%         ⇒ 降阶为一阶组 [y1; y2]' = [y2; -y1]，初值 [1; 0]。
%   独立参照（第 1 类：解析解 + 收敛阶）：
%     闭式解 y(x) = cos(x)（由 y(0)=1、dy/dx(0)=0 定，教科书级）。
%     固定步长 RK4 ⇒ 步长减半误差比应 ~ 16（4 阶）。
%   ★ dsolve 仅作同机实现 / 符号交叉核对，不作独立参照。
%
%   用法：
%     reduce_order()             % 自检并打印读数
%     out = reduce_order(opts)   % opts.T opts.N
%
%   返回 struct：dsolve_str, y_err_N, y_err_2N, order_ratio。

if nargin < 1 || isempty(opts); opts = struct(); end
T = dflt(opts, 'T', 2*pi);
N = dflt(opts, 'N', 20);

% 降阶：d2y/dx2 + y = 0  ⇒  一阶组 z' = [z2; -z1]，初值 [y(0); dy/dx(0)] = [1; 0]
f  = @(z) [z(2); -z(1)];
y0 = [1; 0];

[xN,  YN ] = rk4_system(f, T, y0, N);
[x2N, Y2N] = rk4_system(f, T, y0, 2*N);
y_err_N  = max(abs(YN(:,1)  - cos(xN)));
y_err_2N = max(abs(Y2N(:,1) - cos(x2N)));
order_ratio = y_err_N / y_err_2N;

% dsolve（同机实现 / 符号交叉核对，非独立参照）
dsolve_str = '(dsolve unavailable)';
try
    syms y(x)
    sol = dsolve(diff(y, x, 2) + y == 0, y(0) == 1, subs(diff(y, x), x, 0) == 0);
    dsolve_str = char(sol);
catch
    dsolve_str = '(dsolve unavailable)';
end

out = struct('T', T, 'N', N, 'dsolve_str', dsolve_str, ...
             'y_err_N', y_err_N, 'y_err_2N', y_err_2N, 'order_ratio', order_ratio);

fprintf('[reduce_order] d2y/dx2 + y = 0, y(0)=1, dy/dx(0)=0 (reduced: z''=[z2; -z1])\n');
fprintf('  analytic y(x)            = cos(x)\n');
fprintf('  dsolve (cross-check)     = %s\n', dsolve_str);
fprintf('  max|y - cos(x)| (N, 2N)  = %.6e , %.6e\n', y_err_N, y_err_2N);
fprintf('  order ratio (N vs 2N)    = %.6f  (4th order ~ 16)\n', order_ratio);
end

function [x, Y] = rk4_system(f, T, y0, N)
h = T / N;
x = (0:N)' * h;
Y = zeros(N+1, 2);
Y(1, :) = y0(:).';
for k = 1:N
    z  = Y(k, :).';
    k1 = f(z);
    k2 = f(z + h/2*k1);
    k3 = f(z + h/2*k2);
    k4 = f(z + h*k3);
    Y(k+1, :) = (z + h/6*(k1 + 2*k2 + 2*k3 + k4)).';
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
