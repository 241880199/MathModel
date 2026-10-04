function out = pde_numerical(opts)
%PDE_NUMERICAL  1D heat equation u_t = D u_xx by two builtins + analytic separation-of-variables.
%
%   M4 `mcm-model-select` 骨架 · mechanism #5（PDE 数值解 · 抛物/椭圆/双曲；刚性）。
%   文件名全 ASCII（GC5）。
%
%   本题（抛物型）：
%     u_t = D u_xx,  x in (0,1),  u(0,t) = u(1,t) = 0,  u(x,0) = sin(pi x).
%   独立参照（第 1 类：解析解 + 收敛阶）—— 分离变量：
%     u(x,t) = exp(-D pi^2 t) * sin(pi x).
%   做法 ① pdepe（内置，空间二阶）: 步长减半，最大误差应约按 2 阶下降（比值 ~ 4）。
%   做法 ② 线方法（MOL）+ ode15s（内置，刚性）: 同一解析解对照。
%
%   用法：
%     pde_numerical()             % 自检并打印读数
%     out = pde_numerical(opts)   % opts.D opts.T opts.N
%
%   返回 struct：err_pdepe_N, err_pdepe_2N, order_ratio, u_num_xhalf, u_exact_xhalf, err_mol。

if nargin < 1 || isempty(opts); opts = struct(); end
D = dflt(opts, 'D', 0.1);
T = dflt(opts, 'T', 1.0);
N = dflt(opts, 'N', 20);

% --- 做法 ① pdepe：两套网格（N 与 2N），核收敛阶 ---
[errN,  xN,  uxhalfN] = pdepe_heat(D, T, N);
[err2N, ~ ,  ~      ] = pdepe_heat(D, T, 2*N);
ratio = errN / err2N;                     % 步长减半 ⇒ 误差约降 4 倍（2 阶）

% 取 x = 0.5 处读数（解析真值 = exp(-D pi^2 T) * sin(pi/2)）
u_exact_xhalf = exp(-D*pi^2*T) * sin(pi*0.5);

% --- 做法 ② MOL + ode15s：同一解析解对照 ---
[errMOL, ~] = mol_heat_ode15s(D, T, N);

out = struct('D', D, 'T', T, 'N', N, ...
             'err_pdepe_N', errN, 'err_pdepe_2N', err2N, 'order_ratio', ratio, ...
             'u_num_xhalf', uxhalfN, 'u_exact_xhalf', u_exact_xhalf, 'err_mol', errMOL);

fprintf('[pde_numerical] heat u_t = D u_xx, D = %.6g, T = %.6g\n', D, T);
fprintf('  pdepe  max|u - u_exact| on N  = %d : %.6e\n', N,    errN);
fprintf('  pdepe  max|u - u_exact| on 2N = %d : %.6e\n', 2*N,  err2N);
fprintf('  order ratio (N vs 2N)          = %.6f  (2nd order ~ 4)\n', ratio);
fprintf('  u_num  (x=0.5,t=%.3g)          = %.15g\n', T, uxhalfN);
fprintf('  u_exact(x=0.5,t=%.3g)          = %.15g\n', T, u_exact_xhalf);
fprintf('  |u_num - u_exact| at x=0.5     = %.3e\n', abs(uxhalfN - u_exact_xhalf));
fprintf('  MOL + ode15s max error (N=%d)  = %.6e\n', N, errMOL);
end

% ------------------------------------------------------------------------
function [err, xmesh, uxhalf] = pdepe_heat(D, T, N)
xmesh = linspace(0, 1, N);
tmesh = linspace(0, T, 11);
m = 0;
pdefun = @(x, t, u, DuDx) deal(1, D*DuDx, 0);      % c=1, f=D u_x, s=0
icfun  = @(x) sin(pi*x);
bcfun  = @(xl, ul, xr, ur, t) deal(ul, 0, ur, 0);  % u(0)=u(1)=0 (Dirichlet: p=u, q=0)
sol = pdepe(m, pdefun, icfun, bcfun, xmesh, tmesh, ...
            odeset('RelTol', 1e-9, 'AbsTol', 1e-11));
u   = sol(end, :);
uex = exp(-D*pi^2*T) * sin(pi*xmesh);
err = max(abs(u - uex));
uxhalf = interp1(xmesh, u, 0.5, 'pchip');
end

% ------------------------------------------------------------------------
function [err, xmesh] = mol_heat_ode15s(D, T, N)
% 线方法：内部 N-2 个节点做半离散，两端 Dirichlet 0，ode15s（内置，刚性）积分。
xmesh = linspace(0, 1, N);
dx = xmesh(2) - xmesh(1);
xi = xmesh(2:end-1);
u0 = sin(pi*xi(:));
odefun = @(t, u) D * laplacian1d(u, dx);
[tm, um] = ode15s(odefun, [0 T], u0);
u   = um(end, :)';
uex = exp(-D*pi^2*T) * sin(pi*xi(:));
err = max(abs(u - uex));
end

function lap = laplacian1d(u, dx)
% 一维 Laplacian，两端 Dirichlet 0（虚节点取 0）。
n  = numel(u);
lap = zeros(n, 1);
uL = [0; u(1:end-1)];
uR = [u(2:end); 0];
lap = (uL - 2*u + uR) / dx^2;
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
