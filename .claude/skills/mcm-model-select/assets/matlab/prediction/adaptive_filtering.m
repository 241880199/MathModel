function out = adaptive_filtering(opts)
%ADAPTIVE_FILTERING  Adaptive (self-tuning) linear predictor by normalised LMS weight updates.
%
%   M4 `mcm-model-select` 骨架 · prediction #6（自适应滤波）。文件名全 ASCII（GC5）。
%
%   ★ 方法口径（与 `corpus/algorithms/src/TimeSeries时间序列函数/自适应滤波法/main.m` 同源、但**加了一步归一化**）：
%     预测  yhat(t) = sum_{i=1..k} w_i * y(t-i)；误差 e(t) = y(t) - yhat(t)；
%     权重更新（**归一化 LMS，NLMS**）  w_i <- w_i + mu * e(t) * y(t-i) / (||y(t-1..t-k)||^2 + eps)。
%     ★ 为什么归一化：教科书原始的未归一版本 `w = w + 2*k*err*y(..)` 对**数据尺度**极敏感、
%       在中等尺度序列上会**发散**（见 ④-1 的实测依据）⇒ 本骨架用 NLMS 兜住尺度。
%
%   语料面（P6）：**无直接语料** —— `corpus/papers/MODEL_MAP.md` 里 `adaptive filter` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*adaptive filter（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。★ **素材 0 ≠ 语料 0 要分开说**：**素材面**在
%   `corpus/algorithms/src/TimeSeries时间序列函数/自适应滤波法/`（含 `main.m`）**有**起点素材；**语料面**才是 0。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 逐步手算前 3 次权重迭代（含 yhat、e、新 w），与骨架逐位比；
%     · 收敛性：训练 MSE 随 pass 单调下降（NLMS 的分布性质）。
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/adaptive_filtering.md`。
%
%   用法：
%     adaptive_filtering()             % 自检并打印读数
%     out = adaptive_filtering(opts)   % opts.y opts.k opts.mu opts.w0 opts.passes
%
%   返回 struct：y, k, mu, w0, w, mse, trace, fc。

if nargin < 1 || isempty(opts); opts = struct(); end
y = dflt(opts, 'y', [10 12 13 15 14 16 17]);
y = y(:).';
n = numel(y);
k = dflt(opts, 'k', 2);
mu = dflt(opts, 'mu', 0.5);
w0 = dflt(opts, 'w0', ones(1, k) / k);
passes = dflt(opts, 'passes', 10);
epsn = 1e-12;
assert(numel(w0) == k, 'w0 的长度必须等于 k');

w = w0(:).';
mse = zeros(1, passes);
trace = [];                                       % 首次 pass 的前 3 次迭代

for p = 1:passes
    se = 0; cnt = 0;
    for t = k+1:n
        xs = y(t-1:-1:t-k);                       % [y(t-1), ..., y(t-k)]
        yhat = w * xs.';
        e = y(t) - yhat;
        w = w + mu * e * xs / (sum(xs.^2) + epsn);
        se = se + e^2; cnt = cnt + 1;
        if p == 1 && t <= k + 3
            trace = [trace; t, xs, yhat, e, w];   %#ok<AGROW>  只记前 3 次
        end
    end
    mse(p) = se / cnt;
end

% 一步预测（用序列末端的 k 个值）
fc = w * y(end:-1:end-k+1).';

out = struct('y', y, 'k', k, 'mu', mu, 'w0', w0, 'w', w, ...
             'mse', mse, 'trace', trace, 'fc', fc, 'n', n, 'passes', passes);

fprintf('[adaptive_filtering] NLMS · n = %d, k = %d, mu = %.6g, passes = %d\n', n, k, mu, passes);
fprintf('  y = [%s]\n', num2str(y, '%.6g '));
fprintf('  w0 = [%s]  ⇒  w = [%s]\n', num2str(w0, '%.6g '), num2str(w, '%.8g '));
fprintf('  首次 pass 前 3 次迭代（t | yhat | e | w）：\n');
for i = 1:size(trace, 1)
    fprintf('    t=%d  yhat=%.8g  e=%.8g  w=[%s]\n', trace(i, 1), trace(i, k+2), trace(i, k+3), ...
            num2str(trace(i, k+4:k+3+k), '%.8g '));
end
fprintf('  训练 MSE（每 pass）：[%s]\n', num2str(mse, '%.8g '));
fprintf('  MSE 是否随 pass 单调不增 : %s\n', bool2str(all(diff(mse) <= 1e-12)));
fprintf('  一步预测 = %.8g\n', fc);
end

function s = bool2str(tf)
if tf; s = '是'; else; s = '否'; end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
