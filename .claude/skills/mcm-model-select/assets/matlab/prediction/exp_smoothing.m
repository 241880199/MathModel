function out = exp_smoothing(opts)
%EXP_SMOOTHING  Exponential smoothing: single (SES), double (Holt), triple (Holt-Winters additive).
%
%   M4 `mcm-model-select` 骨架 · prediction #3（指数平滑）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `exponential smoothing` 命中 **1 篇**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*exponential smoothing（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行：P2025-C-04）。
%   ★ **素材面**（另有起点素材）：`corpus/algorithms/src/TimeSeries时间序列函数/指数平滑法/`
%     （含 `single_exponential _smoothing.m` / `second_exponential_smoothing.m` / `third_exponential_smoothing.m`）—— 教辅级，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 一次（SES）  S(1) = x(1)；S(t) = alpha*x(t) + (1-alpha)*S(t-1)；预测 = S(n)；
%     · 二次（Holt） l(1) = x(1), b(1) = x(2) - x(1)；
%                    l(t) = alpha*x(t) + (1-alpha)*(l(t-1) + b(t-1))；
%                    b(t) = beta*(l(t) - l(t-1)) + (1-beta)*b(t-1)；h 步预测 = l(n) + h*b(n)；
%     · 三次（HW 加法） 见 `hw_additive` 子函数。
%   ★ 逐步算式与手算期望值（SES 与 Holt 各一组）见 `tests/skills/model-select/verify/exp_smoothing.md`。
%
%   用法：
%     exp_smoothing()             % 自检并打印读数（SES + Holt 于小序列；HW 于自带季节序列）
%     out = exp_smoothing(opts)   % opts.x opts.alpha opts.beta opts.gamma opts.L opts.h
%
%   返回 struct：S (SES) · l, b (Holt) · lw, bw, sw, hw_fc (HW)。

if nargin < 1 || isempty(opts); opts = struct(); end
x     = dflt(opts, 'x',     [10 12 13 15 14]);
alpha = dflt(opts, 'alpha', 0.5);
beta  = dflt(opts, 'beta',  0.3);
gamma = dflt(opts, 'gamma', 0.2);
h     = dflt(opts, 'h',     1);
x = x(:).';
n = numel(x);

% --- 一次指数平滑（SES）---
S = zeros(1, n);
S(1) = x(1);
for t = 2:n
    S(t) = alpha * x(t) + (1 - alpha) * S(t-1);
end
ses_fc = S(end);                                  % 一步预测

% --- 二次指数平滑（Holt）---
l = zeros(1, n); b = zeros(1, n);
l(1) = x(1); b(1) = x(2) - x(1);
for t = 2:n
    l(t) = alpha * x(t) + (1 - alpha) * (l(t-1) + b(t-1));
    b(t) = beta * (l(t) - l(t-1)) + (1 - beta) * b(t-1);
end
holt_fc = l(end) + h * b(end);

% --- 三次指数平滑（Holt-Winters 加法；自带季节序列）---
ys = dflt(opts, 'x_seasonal', [10 14 18 22, 12 16 20 24, 14 18 22 26]);
L  = dflt(opts, 'L', 4);
[lw, bw, sw, hw_fc] = hw_additive(ys, L, alpha, beta, gamma, h);

out = struct('x', x, 'alpha', alpha, 'beta', beta, 'S', S, 'ses_fc', ses_fc, ...
             'l', l, 'b', b, 'holt_fc', holt_fc, 'h', h, ...
             'ys', ys, 'L', L, 'gamma', gamma, 'lw', lw, 'bw', bw, 'sw', sw, 'hw_fc', hw_fc);

fprintf('[exp_smoothing] SES · x = [%s], alpha = %.4g\n', num2str(x, '%.6g '), alpha);
fprintf('  S = [%s]  ⇒ 1 步预测 = %.8g\n', num2str(S, '%.8g '), ses_fc);
fprintf('[exp_smoothing] Holt · alpha = %.4g, beta = %.4g\n', alpha, beta);
fprintf('  level l = [%s]\n', num2str(l, '%.8g '));
fprintf('  trend b = [%s]  ⇒ %d 步预测 = %.8g\n', num2str(b, '%.8g '), h, holt_fc);
fprintf('[exp_smoothing] Holt-Winters（加法）· L = %d, alpha = %.4g, beta = %.4g, gamma = %.4g\n', L, alpha, beta, gamma);
fprintf('  hw level = [%s]\n', num2str(lw, '%.6g '));
fprintf('  hw trend = [%s]\n', num2str(bw, '%.6g '));
fprintf('  hw seas  = [%s]  ⇒ %d 步预测 = %.8g\n', num2str(sw(1:L), '%.6g '), h, hw_fc);
end

% ------------------------------------------------------------------------
function [l, b, s, fc] = hw_additive(y, L, alpha, beta, gamma, h)
% 加法 Holt-Winters：初值取第一个季节的均值作水平、相邻季节均值差 / L 作趋势、季节项 = y - 水平。
y = y(:).';
n = numel(y);
assert(n >= 2*L, 'Holt-Winters 需要至少两个季节的数据');
l = zeros(1, n); b = zeros(1, n); s = zeros(1, n);
l(L) = mean(y(1:L));
b(L) = (mean(y(L+1:2*L)) - mean(y(1:L))) / L;
s(1:L) = y(1:L) - l(L);
for t = L+1:n
    l(t) = alpha * (y(t) - s(t-L)) + (1 - alpha) * (l(t-1) + b(t-1));
    b(t) = beta * (l(t) - l(t-1)) + (1 - beta) * b(t-1);
    s(t) = gamma * (y(t) - l(t)) + (1 - gamma) * s(t-L);
end
% h 步预测：水平 + 趋势 + 季节（季节索引按 mod L 回绕）
idx = n - L + mod(h - 1, L) + 1;
fc = l(n) + h * b(n) + s(idx);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
