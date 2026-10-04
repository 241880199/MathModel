function out = sir_seir(opts)
%SIR_SEIR  SIR / SEIR compartment models via ode45 + analytic properties.
%
%   M4 `mcm-model-select` 骨架 · mechanism #6（传染病模型 SIR / SEIR）。文件名全 ASCII（GC5）。
%
%   独立参照（解析性质）—— 不是"跟另一段代码对"，而是"跟模型的不变量对"：
%     · 守恒量：S + I + R = 1（SIR）；S + E + I + R = 1（SEIR），归一化分数。
%     · 基本再生数阈值：R0 = beta / gamma（SIR/SEIR 同形）。
%     · 最终规模（final size）关系（SIR）：
%         ln( s0 / s_inf ) = R0 ( 1 - s_inf )   ⇒ 用 fzero 解出的 s_inf 应等于 ode45 末值。
%
%   用法：
%     sir_seir()             % 自检并打印读数
%     out = sir_seir(opts)   % opts.beta opts.gamma opts.I0 opts.T
%
%   返回 struct：R0, cons_sir, s_inf_num, s_inf_analytic, cons_seir。

if nargin < 1 || isempty(opts); opts = struct(); end
beta  = dflt(opts, 'beta',  0.6);
gamma = dflt(opts, 'gamma', 0.2);
I0    = dflt(opts, 'I0',    1e-3);
T     = dflt(opts, 'T',     160);
oset  = odeset('RelTol', 1e-10, 'AbsTol', 1e-12);

% --- SIR（归一化分数）---
sir   = @(t, y) [ -beta*y(1)*y(2); beta*y(1)*y(2) - gamma*y(2); gamma*y(2) ];
y0sir = [1 - I0; I0; 0];
[~, ys] = ode45(sir, [0 T], y0sir, oset);
cons_sir = max(abs(sum(ys, 2) - 1));

R0 = beta / gamma;
s0 = y0sir(1);
g  = @(s) log(s0 ./ s) - R0 * (1 - s);     % 单调，根在 (0, s0)
s_inf_analytic = fzero(g, [1e-9, s0]);
s_inf_num      = ys(end, 1);

% --- SEIR（归一化分数；sigma 潜伏率）---
sigma = 1/3;
seir   = @(t, y) [ -beta*y(1)*y(3); ...
                    beta*y(1)*y(3) - sigma*y(2); ...
                    sigma*y(2) - gamma*y(3); ...
                    gamma*y(3) ];
y0seir = [1 - I0; 0; I0; 0];
[~, ye] = ode45(seir, [0 T], y0seir, oset);
cons_seir = max(abs(sum(ye, 2) - 1));

out = struct('beta', beta, 'gamma', gamma, 'R0', R0, ...
             'cons_sir', cons_sir, 'cons_seir', cons_seir, ...
             's_inf_num', s_inf_num, 's_inf_analytic', s_inf_analytic, ...
             's_inf_abs_err', abs(s_inf_num - s_inf_analytic));

fprintf('[sir_seir] beta = %.6g, gamma = %.6g, I0 = %.6g\n', beta, gamma, I0);
fprintf('  R0 = beta/gamma                    = %.9g  (>1 => 疫情扩散)\n', R0);
fprintf('  SIR  max|S+I+R - 1|                = %.3e\n', cons_sir);
fprintf('  SEIR max|S+E+I+R - 1|              = %.3e\n', cons_seir);
fprintf('  s_inf (ode45 final S)              = %.15g\n', s_inf_num);
fprintf('  s_inf (analytic final-size root)   = %.15g\n', s_inf_analytic);
fprintf('  |s_inf_num - s_inf_analytic|       = %.3e\n', abs(s_inf_num - s_inf_analytic));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
