function out = ode_ivp(opts)
%ODE_IVP  ODE initial value problem: explicit Euler (order 1) + classical RK4 (order 4).
%
%   M4 `mcm-model-select` 骨架 · mechanism #1（ODE 初值问题 Euler / RK4）。文件名全 ASCII（GC5）。
%
%   起点素材（可读、不可当独立参照 —— 在 corpus/algorithms/src/ 里、不在 fixed/ 六件内，GC6 禁止）：
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Explicit_Euler.m`（显式欧拉）
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Classical_RK4.m`（经典 RK4）
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/Classical_RK4s.m`（RK4 变体）
%     （本骨架不照它们改写。）
%
%   算例与独立参照（第 1 类：解析解 + 收敛阶）：
%     方程 dy/dt = lambda * y，初值 y(0) = 1  ⇒  闭式解 y(t) = exp(lambda * t)。
%     步长减半：Euler 误差比应 ~ 2（1 阶）、RK4 误差比应 ~ 16（4 阶）。
%   ★ ode45 仅作同机实现 / 交叉核对，不作独立参照（同机同实现不独立）。
%
%   用法：
%     ode_ivp()             % 自检并打印读数
%     out = ode_ivp(opts)   % opts.lambda opts.T opts.h
%
%   返回 struct：y_exact, euler_err_h, euler_err_h2, euler_ratio, rk4_err_h, rk4_err_h2, rk4_ratio, ode45_err。

if nargin < 1 || isempty(opts); opts = struct(); end
lambda = dflt(opts, 'lambda', -2);
T      = dflt(opts, 'T', 1.0);
h      = dflt(opts, 'h', 0.1);

odefun  = @(t, y) lambda * y;
y0      = 1;
y_exact = exp(lambda * T);

% --- 显式欧拉：h 与 h/2 ---
y_e_h  = euler_solve(odefun, T, y0, h);
y_e_h2 = euler_solve(odefun, T, y0, h/2);
euler_err_h  = abs(y_e_h  - y_exact);
euler_err_h2 = abs(y_e_h2 - y_exact);
euler_ratio  = euler_err_h / euler_err_h2;

% --- 经典 RK4：h 与 h/2 ---
y_r_h  = rk4_solve(odefun, T, y0, h);
y_r_h2 = rk4_solve(odefun, T, y0, h/2);
rk4_err_h  = abs(y_r_h  - y_exact);
rk4_err_h2 = abs(y_r_h2 - y_exact);
rk4_ratio  = rk4_err_h / rk4_err_h2;

% --- ode45（同机实现，交叉核对，非独立参照）---
[~, yo] = ode45(odefun, [0 T], y0, odeset('RelTol', 1e-12, 'AbsTol', 1e-14));
ode45_err = abs(yo(end) - y_exact);

out = struct('lambda', lambda, 'T', T, 'h', h, 'y_exact', y_exact, ...
             'euler_err_h', euler_err_h, 'euler_err_h2', euler_err_h2, 'euler_ratio', euler_ratio, ...
             'rk4_err_h', rk4_err_h, 'rk4_err_h2', rk4_err_h2, 'rk4_ratio', rk4_ratio, ...
             'ode45_err', ode45_err);

fprintf('[ode_ivp] dy/dt = lambda*y, y(0)=1, lambda = %.6g, T = %.6g, h = %.6g\n', lambda, T, h);
fprintf('  y_exact = exp(lambda*T)   = %.15g\n', y_exact);
fprintf('  Euler err (h, h/2)        = %.6e , %.6e   ratio = %.6f  (order 1 ~ 2)\n', euler_err_h, euler_err_h2, euler_ratio);
fprintf('  RK4   err (h, h/2)        = %.6e , %.6e   ratio = %.6f  (order 4 ~ 16)\n', rk4_err_h, rk4_err_h2, rk4_ratio);
fprintf('  ode45 err (cross-check)   = %.6e  (同机实现，非独立参照)\n', ode45_err);
end

function y = euler_solve(f, T, y0, h)
n = round(T / h); h = T / n; y = y0; t = 0;
for k = 1:n
    y = y + h * f(t, y);
    t = t + h;
end
end

function y = rk4_solve(f, T, y0, h)
n = round(T / h); h = T / n; y = y0; t = 0;
for k = 1:n
    k1 = f(t,       y);
    k2 = f(t + h/2, y + h/2*k1);
    k3 = f(t + h/2, y + h/2*k2);
    k4 = f(t + h,   y + h*k3);
    y  = y + h/6 * (k1 + 2*k2 + 2*k3 + k4);
    t  = t + h;
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
