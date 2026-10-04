function out = trend_extrapolation(opts)
%TREND_EXTRAPOLATION  Fit a trend curve (linear / polynomial / exponential / logistic) and extrapolate.
%
%   M4 `mcm-model-select` 骨架 · prediction #5（趋势外推）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**无直接语料** —— `corpus/papers/MODEL_MAP.md` 里 `trend extrapolation` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*trend extrapolation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。★ **素材 0 ≠ 语料 0 要分开说**：**素材面**在
%   `corpus/algorithms/src/TimeSeries时间序列函数/趋势外推预测法/`（含 `predict1.m` / `logistic_curve.m` / `compertz_curve.m` / `modified_exponential_curve.m`）
%   与 `corpus/algorithms/fixed/trend_extrapolation.m`（净室重写版）**有**起点素材；**语料面**才是 0。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 线性趋势  y = a + b*t，最小二乘
%                 b = sum((t-tbar)(y-ybar)) / sum((t-tbar)^2)，a = ybar - b*tbar；
%                 外推 y(t0) = a + b*t0。**手算在 t = 1..5 的小序列 + 外推 t = 6 上做**。
%     · 多项式    `polyfit(t, y, p)` + `polyval`（p 阶）；
%     · 指数      log(y) 对 t 线性拟合 ⇒ y = exp(c + d*t)；
%     · logistic  logit(y/K) 对 t 线性拟合（需给饱和值 K）。
%   ★ 逐步算式与手算期望值（线性）见 `tests/skills/model-select/verify/trend_extrapolation.md`。
%
%   用法：
%     trend_extrapolation()             % 自检并打印读数（默认线性，外推 1 步）
%     out = trend_extrapolation(opts)   % opts.y opts.t opts.h opts.K
%
%   返回 struct：t, y, lin(a,b), lin_fc, poly(coef,fc), exp(c,d,fc), logi(c,d,fc)。

if nargin < 1 || isempty(opts); opts = struct(); end
y = dflt(opts, 'y', [3 5 6 9 10]);
y = y(:).';
n = numel(y);
t = dflt(opts, 't', 1:n);
h = dflt(opts, 'h', 1);
K = dflt(opts, 'K', max(y) * 1.2);                % logistic 的饱和值（需外部给，本骨架给默认）
t = t(:).';

% --- 线性趋势（最小二乘，等价 polyfit(t,y,1)）---
p1 = polyfit(t, y, 1);
b = p1(1); a = p1(2);
lin_fc = polyval(p1, t(end) + h);

% --- 多项式（2 阶）---
p2 = polyfit(t, y, 2);
poly_fc = polyval(p2, t(end) + h);

% --- 指数趋势 y = exp(c + d t) ---
pe = polyfit(t, log(y), 1);
d = pe(1); c = pe(2);
exp_fc = exp(polyval(pe, t(end) + h));

% --- logistic 趋势 logit(y/K) = c + d t ---
pl = polyfit(t, log(y ./ (K - y)), 1);
dL = pl(1); cL = pl(2);
logi_fc = K / (1 + exp(-(cL + dL * (t(end) + h))));

out = struct('t', t, 'y', y, 'h', h, 'K', K, ...
             'lin_a', a, 'lin_b', b, 'lin_fc', lin_fc, ...
             'poly_coef', p2, 'poly_fc', poly_fc, ...
             'exp_c', c, 'exp_d', d, 'exp_fc', exp_fc, ...
             'logi_c', cL, 'logi_d', dL, 'logi_fc', logi_fc);

fprintf('[trend_extrapolation] n = %d，y = [%s]，逐步外推 h = %d\n', n, num2str(y, '%.6g '), h);
fprintf('  线性   a = %.8g, b = %.8g  ⇒ y(%g) = %.8g\n', a, b, t(end) + h, lin_fc);
fprintf('  二次   coef = [%s]  ⇒ y(%g) = %.8g\n', num2str(p2, '%.6g '), t(end) + h, poly_fc);
fprintf('  指数   c = %.8g, d = %.8g  ⇒ y(%g) = %.8g\n', c, d, t(end) + h, exp_fc);
fprintf('  logistic (K = %.6g) c = %.8g, d = %.8g  ⇒ y(%g) = %.8g\n', K, cL, dL, t(end) + h, logi_fc);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
