function out = lotka_volterra(opts)
%LOTKA_VOLTERRA  Predator-prey (Lotka-Volterra) via ode45 + analytic invariants.
%
%   M4 `mcm-model-select` 骨架 · mechanism #7（生态动力学 Lotka-Volterra）。文件名全 ASCII（GC5）。
%
%   模型：
%     dx/dt =  alpha * x - beta  * x * y
%     dy/dt = -gamma * y + delta * x * y
%
%   独立参照（解析性质）：
%     · 平衡点：(0,0) 与 (gamma/delta, alpha/beta)（后者为中心型）。
%     · 第一积分（守恒量）：H(x,y) = delta*x - gamma*ln x + beta*y - alpha*ln y，
%       轨线应满足 H ≡ H0 ⇒ 守恒量漂移应 ~ 机器/积分容差量级（周期解存在的依据）。
%     · 周期解的时间平均 = 平衡点（x̄ → gamma/delta，ȳ → alpha/beta）。
%
%   用法：
%     lotka_volterra()             % 自检并打印读数
%     out = lotka_volterra(opts)   % opts.alpha opts.beta opts.gamma opts.delta opts.T
%
%   返回 struct：x_eq, y_eq, H0, H_drift, x_bar, y_bar。

if nargin < 1 || isempty(opts); opts = struct(); end
alpha = dflt(opts, 'alpha', 1.0);
beta  = dflt(opts, 'beta',  1.0);
gamma = dflt(opts, 'gamma', 1.0);
delta = dflt(opts, 'delta', 1.0);
T     = dflt(opts, 'T',     200);
x0    = dflt(opts, 'x0',    0.5);
y0    = dflt(opts, 'y0',    0.75);

Hfun = @(x, y) delta*x - gamma*log(x) + beta*y - alpha*log(y);

lv  = @(t, z) [ alpha*z(1) - beta*z(1)*z(2); -gamma*z(2) + delta*z(1)*z(2) ];
oset = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);
[t, z] = ode45(lv, [0 T], [x0; y0], oset);

H0     = Hfun(x0, y0);
Hvals  = Hfun(z(:,1), z(:,2));
Hdrift = max(abs(Hvals - H0));

x_eq = gamma / delta;
y_eq = alpha / beta;

% 时间平均（对全时段积分；长时段下应趋近平衡点）
x_bar = trapz(t, z(:,1)) / (t(end) - t(1));
y_bar = trapz(t, z(:,2)) / (t(end) - t(1));

out = struct('x_eq', x_eq, 'y_eq', y_eq, 'H0', H0, 'H_drift', Hdrift, ...
             'x_bar', x_bar, 'y_bar', y_bar);

fprintf('[lotka_volterra] alpha=%.4g beta=%.4g gamma=%.4g delta=%.4g\n', alpha, beta, gamma, delta);
fprintf('  equilibrium (gamma/delta, alpha/beta) = (%.12g, %.12g)\n', x_eq, y_eq);
fprintf('  first integral H0                     = %.15g\n', H0);
fprintf('  max|H(t) - H0| (conservation drift)   = %.3e\n', Hdrift);
fprintf('  time-average x_bar                    = %.9g\n', x_bar);
fprintf('  time-average y_bar                    = %.9g\n', y_bar);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
