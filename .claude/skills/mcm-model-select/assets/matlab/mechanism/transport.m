function out = transport(opts)
%TRANSPORT  Linear transport: advection u_t + c u_x = 0 and diffusion u_t = D u_xx.
%
%   M4 `mcm-model-select` 骨架 · mechanism #8（输运方程：热传导 / 扩散 / 波动）。
%   文件名全 ASCII（GC5）。
%
%   周期域 (0,1)，u0(x) = sin(2 pi x)，显式有限差分。
%   独立参照（第 1 类：有闭式解的参数取值 —— 扩散 / 平流）：
%     · 平流 u_t + c u_x = 0  ⇒  u(x,t) = sin(2 pi (x - c t))；
%       ★ 取 CFL = c dt/dx = 1（dt = dx/c）时迎风格式**精确**（整格平移）。
%     · 扩散 u_t = D u_xx      ⇒  u(x,t) = exp(-D (2 pi)^2 t) sin(2 pi x)。
%
%   用法：
%     transport()             % 自检并打印读数
%     out = transport(opts)   % opts.c opts.D opts.N opts.T
%
%   返回 struct：adv_err（平流误差）, dif_err（扩散误差）, cfl, diffusion_decay_num/analytic。

if nargin < 1 || isempty(opts); opts = struct(); end
c = dflt(opts, 'c', 1.0);
D = dflt(opts, 'D', 0.1);
N = dflt(opts, 'N', 100);
T = dflt(opts, 'T', 0.5);

x  = (0:N-1)' / N;
dx = 1 / N;

% --- (a) 平流 u_t + c u_x = 0，周期，迎风 FTBS（c > 0）---
nstep = max(1, round(T / (dx/abs(c))));
dt    = T / nstep;
cfl   = c * dt / dx;
u = sin(2*pi*x);
for n = 1:nstep
    um = circshift(u, 1);            % um(j) = u(j-1)
    u  = u - cfl * (u - um);
end
uex     = sin(2*pi*(x - c*T));
adv_err = max(abs(u - uex));

% --- (b) 扩散 u_t = D u_xx，周期 ---
nstep2 = max(1, ceil(T / (0.4*dx^2/D)));
dt2    = T / nstep2;
r      = D * dt2 / dx^2;             % 稳定需 r <= 0.5
w = sin(2*pi*x);
for n = 1:nstep2
    wp = circshift(w, -1);
    wm = circshift(w,  1);
    w  = w + r * (wp - 2*w + wm);
end
wex     = exp(-D*(2*pi)^2*T) * sin(2*pi*x);
dif_err = max(abs(w - wex));

% 扩散衰减率（对数幅度）核对解析值 D (2 pi)^2
decay_num      = -log(max(abs(w))  / max(abs(sin(2*pi*x)))) / T;
decay_analytic = D * (2*pi)^2;

out = struct('c', c, 'D', D, 'N', N, 'T', T, 'cfl', cfl, ...
             'adv_err', adv_err, 'dif_err', dif_err, ...
             'decay_num', decay_num, 'decay_analytic', decay_analytic);

fprintf('[transport] advection + diffusion, c = %.6g, D = %.6g, N = %d, T = %.6g\n', c, D, N, T);
fprintf('  advection CFL                = %.15g\n', cfl);
fprintf('  advection max|u - u_exact|   = %.3e\n', adv_err);
fprintf('  diffusion max|u - u_exact|   = %.3e\n', dif_err);
fprintf('  diffusion decay (num)        = %.9g\n', decay_num);
fprintf('  diffusion decay (analytic)   = %.9g\n', decay_analytic);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
