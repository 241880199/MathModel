function out = reaction_diffusion(opts)
%REACTION_DIFFUSION  u_t = D u_xx + r u (1 - u)  (Fisher-KPP), explicit FTCS.
%
%   M4 `mcm-model-select` 骨架 · mechanism #9（反应扩散）。文件名全 ASCII（GC5）。
%
%   独立参照（第 1 类：有闭式解的参数取值）：
%     · 退化检验（r = 0，纯扩散）：u0 = sin(pi x)、两端 0 ⇒
%         u(x,t) = exp(-D pi^2 t) sin(pi x)     （分离变量，闭式）。
%   ★ 附一条解析性质（非本类的硬核，作旁证）：Fisher 行波前速 v* = 2 sqrt(D r)。
%
%   ★ 为何用显式 FTCS 而非内置 pdepe（设计取舍，非"内置不可用"）：
%     Fisher-KPP **本可用** MATLAB 内置 pdepe 直接求解（只要数值结果时）。
%     此处选显式 FTCS 是设计取舍 —— 让"反应项 + 扩散项"逐拍显现（机理可见，本
%     mechanism 类方法文件要教的正是这个），且该显式格式已过独立参照（r = 0 退
%     化到纯扩散，与闭式解同值到二阶）。
%     pdepe 复跑命令见 tests/skills/model-select/verify/reaction_diffusion.md §⑤。
%
%   用法：
%     reaction_diffusion()            % 自检并打印读数
%     out = reaction_diffusion(opts)  % opts.D opts.r opts.T opts.N
%
%   返回 struct：err_pure_diffusion, front_speed_num, front_speed_analytic。

if nargin < 1 || isempty(opts); opts = struct(); end
D = dflt(opts, 'D', 0.1);
r = dflt(opts, 'r', 1.0);
T = dflt(opts, 'T', 1.0);
N = dflt(opts, 'N', 50);

% --- (a) 退化检验：r = 0，纯扩散，对照闭式解 ---
x  = linspace(0, 1, N);
dx = x(2) - x(1);
dt = 0.4 * dx^2 / D;
nt = round(T / dt); dt = T / nt;
u  = sin(pi*x).';  u(1) = 0; u(end) = 0;
lam = D * dt / dx^2;
for n = 1:nt
    u(2:end-1) = u(2:end-1) + lam*(u(3:end) - 2*u(2:end-1) + u(1:end-2));
end
uex             = exp(-D*pi^2*T) * sin(pi*x).';
err_pure_diff   = max(abs(u - uex));

% --- (b) Fisher 行波前速（解析 v* = 2 sqrt(D r)）---
L  = 150;  Nf = 750;  xf = linspace(0, L, Nf);  dxf = xf(2) - xf(1);
dtf = 0.2 * dxf^2 / D;  ntf_total = round(100 / dtf); dtf = 100 / ntf_total;
uf = 0.5*(1 - tanh((xf - 30)/1));   % ≈1 在左、≈0 在右（阶跃）
uf(1) = 1;  uf(end) = 0;            % Dirichlet: u(0)=1, u(L)=0
rf = D * dtf / dxf^2;
t = 0; x1 = NaN; t1 = NaN; x2 = NaN; t2 = NaN;
for n = 1:ntf_total
    uf(2:end-1) = uf(2:end-1) + rf*(uf(3:end) - 2*uf(2:end-1) + uf(1:end-2)) ...
                  + dtf * r * uf(2:end-1) .* (1 - uf(2:end-1));
    t = t + dtf;
    if abs(t - 60) < dtf/2 || abs(t - 100) < dtf/2
        xfpos = crossing(xf, uf);         % u = 0.5 处
        if isnan(x1); x1 = xfpos; t1 = t; else; x2 = xfpos; t2 = t; end
    end
end
front_speed_num      = (x2 - x1) / (t2 - t1);
front_speed_analytic = 2 * sqrt(D * r);

out = struct('D', D, 'r', r, 'T', T, 'N', N, ...
             'err_pure_diffusion', err_pure_diff, ...
             'front_speed_num', front_speed_num, ...
             'front_speed_analytic', front_speed_analytic);

fprintf('[reaction_diffusion] u_t = D u_xx + r u(1-u), D = %.6g, r = %.6g\n', D, r);
fprintf('  (a) r = 0 pure-diffusion max|u - u_exact| = %.6e\n', err_pure_diff);
fprintf('  (b) Fisher front speed (num)      = %.6f\n', front_speed_num);
fprintf('      Fisher front speed (analytic) = %.6f  (2 sqrt(D r))\n', front_speed_analytic);
end

function xc = crossing(x, u)
% 找 u 从 >0.5 降到 <0.5 的第一个穿越点（线性插值）。
idx = find(u(1:end-1) >= 0.5 & u(2:end) < 0.5, 1, 'first');
if isempty(idx); xc = NaN; return; end
u1 = u(idx); u2 = u(idx+1);
xc = x(idx) + (0.5 - u1) * (x(idx+1) - x(idx)) / (u2 - u1);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
