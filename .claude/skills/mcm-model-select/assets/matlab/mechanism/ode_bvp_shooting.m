function out = ode_bvp_shooting(opts)
%ODE_BVP_SHOOTING  Linear BVP "d2y/dx2 = -y" by single shooting (fzero + fixed-step RK4).
%
%   M4 `mcm-model-select` 骨架 · mechanism #2（ODE 边值问题 · 打靶法）。文件名全 ASCII（GC5）。
%
%   起点素材（可读、不可当独立参照 —— 在 corpus/algorithms/src/ 里、不在 fixed/ 六件内，GC6 禁止）：
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/lineshoot.m`（线性 BVP 打靶）
%     `corpus/algorithms/src/《基于MATLAB的高等数学问题求解》 随书附带源程序/CH14/nlshoot.m`（非线性 BVP 打靶）
%     （本骨架不照它们改写。）
%
%   本题：d2y/dx2 = -y，x ∈ [0, pi/2]，y(0) = 0，y(pi/2) = 1。
%   独立参照（第 1 类：解析解 + 收敛阶）：
%     闭式解 y(x) = sin(x)（教科书级）；打靶未知量 s = dy/dx(0) 的解析值 s* = 1。
%     固定步长 RK4 积分 ⇒ 步长减半误差比应 ~ 16（4 阶）。
%   ★ fzero / ode45 仅作同机实现，不作独立参照。
%
%   用法：
%     ode_bvp_shooting()             % 自检并打印读数
%     out = ode_bvp_shooting(opts)   % opts.N
%
%   返回 struct：s_star, s_hat, y_err_N, y_err_2N, order_ratio。

if nargin < 1 || isempty(opts); opts = struct(); end
N = dflt(opts, 'N', 10);

xr = pi/2;                      % 右端点
yl = 0;                         % 左边界 y(0) = 0
yr = 1;                         % 右边界 y(pi/2) = 1
s_star = cos(0);                % 解析打靶参数 dy/dx(0) = 1

% 打靶：解 phi(s) = y_end(s) - yr = 0，s = dy/dx(0)；初值取 1（解析 s* = 1）
% ★ 收敛阶研究必须在【每一档网格上各自重新解 s】—— 否则把 N 档的 s 固定拿去跑 2N 档，
%   误差被"s 的截断误差"支配，比值会退化成 ~2（不是积分格式的 4 阶）。本骨架按档重解。
fzopt = optimset('TolX', 1e-14);
s_N  = fzero(@(s) shoot_final(s, xr, yl, N)   - yr, 1.0, fzopt);
s_2N = fzero(@(s) shoot_final(s, xr, yl, 2*N) - yr, 1.0, fzopt);
s_hat = s_N;

% 网格上逐点比（N 与 2N，各用自己那档解出的 s）
[yN,  xN ] = shoot_profile(s_N,  xr, yl, N);
[y2N, x2N] = shoot_profile(s_2N, xr, yl, 2*N);
y_err_N  = max(abs(yN  - sin(xN)));
y_err_2N = max(abs(y2N - sin(x2N)));
order_ratio = y_err_N / y_err_2N;

out = struct('s_star', s_star, 's_hat', s_hat, ...
             'y_err_N', y_err_N, 'y_err_2N', y_err_2N, 'order_ratio', order_ratio);

fprintf('[ode_bvp_shooting] d2y/dx2 = -y, y(0)=0, y(pi/2)=1, N = %d\n', N);
fprintf('  s = dy/dx(0):  analytic = %.15g ,  shooting = %.15g\n', s_star, s_hat);
fprintf('  max|y - sin(x)| (N, 2N) = %.6e , %.6e\n', y_err_N, y_err_2N);
fprintf('  order ratio (N vs 2N)   = %.6f  (4th order ~ 16)\n', order_ratio);
end

function yend = shoot_final(s, xr, yl, N)
[~, Y] = rk4_system(xr, [yl; s], N);
yend = Y(end, 1);
end

function [ys, xs] = shoot_profile(s, xr, yl, N)
[xs, Y] = rk4_system(xr, [yl; s], N);
ys = Y(:, 1);
end

function [x, Y] = rk4_system(xr, y0, N)
% 固定步长 RK4 积分一阶组 z' = [z2; -z1]（即 d2y/dx2 = -y），x ∈ [0, xr]
h = xr / N;
x = (0:N)' * h;
Y = zeros(N+1, 2);
Y(1, :) = y0(:).';
f = @(z) [z(2); -z(1)];
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
