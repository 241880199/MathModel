function out = moving_average(opts)
%MOVING_AVERAGE  Moving average: simple MA, weighted MA, and MA-based forecast.
%
%   M4 `mcm-model-select` 骨架 · prediction #4（移动平均）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `moving average` 命中 **4 篇**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*moving average（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行：
%   :131 `moving average（4 篇）`：P2025-C-05 · C-06 · C-16 · C-17）。
%   ★ **素材面**（另有起点素材）：`corpus/algorithms/src/TimeSeries时间序列函数/移动平均法/`
%     （含 `simple_moving_average.m` / `weighting_moving_average.m` / `trend_moving_average.m`）—— 教辅级，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 简单移动平均  MA_m(t) = (1/m) * sum_{i=0}^{m-1} x(t-i)，t = m..n；
%     · 加权移动平均  WMA(t)  = sum_i w(i)*x(t-m+i) / sum_i w(i)（本骨架 w = 1:m 递增）；
%     · 预测          用最后一个 MA 值作一步预测（趋势不明时用 MA、不用趋势外推）。
%   ★ 逐步算式与手算期望值（m = 3 的 MA 与 WMA）见 `tests/skills/model-select/verify/moving_average.md`。
%
%   用法：
%     moving_average()             % 自检并打印读数（默认小序列 + m = 3）
%     out = moving_average(opts)   % opts.x opts.m opts.w
%
%   返回 struct：x, m, ma, w, wma, ma_fc, wma_fc。

if nargin < 1 || isempty(opts); opts = struct(); end
x = dflt(opts, 'x', [10 12 13 15 14]);
x = x(:).';
n = numel(x);
m = dflt(opts, 'm', 3);
w = dflt(opts, 'w', 1:m);
assert(m >= 1 && m < n, '窗口 m 必须满足 1 <= m < n');
assert(numel(w) == m, '权重 w 的长度必须等于 m');

% --- 简单移动平均 ---
ma = zeros(1, n - m + 1);
for t = m:n
    ma(t - m + 1) = mean(x(t - m + 1 : t));
end

% --- 加权移动平均（w 递增，最近的观测权重最大）---
wma = zeros(1, n - m + 1);
for t = m:n
    wma(t - m + 1) = sum(w .* x(t - m + 1 : t)) / sum(w);
end

ma_fc  = ma(end);                                 % 一步预测
wma_fc = wma(end);

out = struct('x', x, 'm', m, 'ma', ma, 'w', w, 'wma', wma, ...
             'ma_fc', ma_fc, 'wma_fc', wma_fc, 'n', n);

fprintf('[moving_average] n = %d, m = %d, x = [%s]\n', n, m, num2str(x, '%.6g '));
fprintf('  MA  = [%s]  ⇒ 1 步预测 = %.8g\n', num2str(ma, '%.8g '), ma_fc);
fprintf('  w   = [%s]  (和 = %g)\n', num2str(w, '%.6g '), sum(w));
fprintf('  WMA = [%s]  ⇒ 1 步预测 = %.8g\n', num2str(wma, '%.8g '), wma_fc);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
