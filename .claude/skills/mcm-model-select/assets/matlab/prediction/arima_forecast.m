function out = arima_forecast(opts)
%ARIMA_FORECAST  ARIMA: order selection, estimation, and forecast intervals (synthetic AR check).
%
%   M4 `mcm-model-select` 骨架 · prediction #10（ARIMA / SARIMA）。文件名全 ASCII（GC5）。
%
%   ★ 为什么文件名是 `arima_forecast.m`、不是 `arima.m`（实测，非推断）：
%     MATLAB 的 `arima` 是**类文件夹里的构造器**（`...\toolbox\econ\econ\@arima\arima.m`），
%     在 R2025b 上 **class-folder 优先于 MATLAB 路径里的同名函数**（MATLAB 会打印该警告）。
%     ⇒ 一个名为 `arima.m` 的骨架文件**既不能被按名调用**（`arima` 解析到类构造器），
%       **也不能被 `run` 执行**（实测：`run('.../arima.m')` ⇒ 未找到）⇒ 那个文件成了**死文件**，
%       会让 `MS4`（骨架可跑）判出**假绿**。故本骨架改名为 `arima_forecast.m`，
%       从而**能正常调用内置 `arima` 类构造器**。详见 `tests/skills/model-select/verify/arima_forecast.md`。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `ARIMA` 命中 6 篇、`SARIMA` 2 篇
%   （合并去重 7 篇：P2025-B-01 · C-04 · C-05 · C-06 · C-11 · C-12 · C-16）。
%   `corpus/algorithms/src/`（脚本素材面）0 命中。逐条命令见 verify 记录。
%
%   独立参照（第 4 类：已知参数的合成数据）—— 不是"跟另一段代码对"：
%     · 造一个**已知系数**的平稳 AR(2)  过程（固定种子），用内置 `arima`+`estimate` 反估系数
%       ⇒ 估计出的 `Constant`/`AR{1}`/`AR{2}` 应回到真值；
%     · 用同一模型做**预测区间覆盖率**检验：名义 95% 区间应覆盖约 95%（多次重复）。
%   ★ 随机过程固定种子；覆盖率给**多次运行的分布**（每个种子一组，不是只跑一次）。
%
%   用法：
%     arima_forecast()             % 自检并打印读数
%     out = arima_forecast(opts)   % opts.a_true opts.c_true opts.n opts.h opts.nrep opts.seeds
%
%   返回 struct：a_true, c_true, a_hat, c_hat, coeff_ae, sig_hat, ...
%                coverage_mean, coverage_sd, coverage_seeds。

if nargin < 1 || isempty(opts); opts = struct(); end
a_true = dflt(opts, 'a_true', [0.5 0.2]);   % 真 AR(2) 系数
c_true = dflt(opts, 'c_true', 0.1);         % 真常数项
n      = dflt(opts, 'n',      300);         % 覆盖率检验里每条序列长度
nlong  = dflt(opts, 'nlong',  4000);        % 系数反估用的长序列
h      = dflt(opts, 'h',      1);
nrep   = dflt(opts, 'nrep',   300);
seeds  = dflt(opts, 'seeds',  0:4);
alpha  = dflt(opts, 'alpha',  0.05);
zc     = -norminv(alpha/2);                 % 95% ⇒ 1.95996

% --- ① 系数反估：一条长序列 ---
rng(0);
yl = sim_ar2(a_true, c_true, nlong, 500);   % 500 步预热丢弃
Mdl = arima(2, 0, 0);
Est = estimate(Mdl, yl, 'Display', 'off');
a_hat = [Est.AR{1}, Est.AR{2}];
c_hat = Est.Constant;
sig_hat = sqrt(Est.Variance);

% --- ② 预测区间覆盖率：多次重复 ---
cov_vec = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    hit = 0;
    for r = 1:nrep
        y = sim_ar2(a_true, c_true, n + h, 0);
        ytr = y(1:n);
        E = estimate(arima(2, 0, 0), ytr, 'Display', 'off');
        [yf, yMSE] = forecast(E, h, 'Y0', ytr);
        lo = yf(end) - zc * sqrt(yMSE(end));
        hi = yf(end) + zc * sqrt(yMSE(end));
        hit = hit + (y(n + h) >= lo && y(n + h) <= hi);
    end
    cov_vec(s) = hit / nrep;
end

out = struct('a_true', a_true, 'c_true', c_true, 'a_hat', a_hat, 'c_hat', c_hat, ...
             'coeff_ae', max(abs(a_hat - a_true)), 'const_ae', abs(c_hat - c_true), ...
             'sig_hat', sig_hat, 'n', n, 'nrep', nrep, 'h', h, 'seeds', seeds, ...
             'coverage_seeds', cov_vec, 'coverage_mean', mean(cov_vec), ...
             'coverage_sd', std(cov_vec), 'nominal', 1 - alpha);

fprintf('[arima_forecast] AR(2): y_t = c + a1 y_{t-1} + a2 y_{t-2} + e_t\n');
fprintf('  true    c = %.6g,  a = [%s]\n', c_true, num2str(a_true, '%.6g '));
fprintf('  est     c = %.6g,  a = [%s]\n', c_hat, num2str(a_hat, '%.6g '));
fprintf('  |est-true|  c = %.3e,  max|a_hat-a_true| = %.3e\n', abs(c_hat - c_true), max(abs(a_hat - a_true)));
fprintf('  sigma_hat = %.6g  (true 1.0)\n', sig_hat);
fprintf('  --- forecast-interval coverage (nominal %.2f) ---\n', 1 - alpha);
fprintf('  per-seed coverage = [%s]\n', num2str(cov_vec, '%.4f  '));
fprintf('  mean +/- sd = %.4f +/- %.4f  (n=%.0f per seed, %d seeds)\n', ...
        mean(cov_vec), std(cov_vec), nrep, numel(seeds));
end

% ------------------------------------------------------------------------
function y = sim_ar2(a, c, ntot, burn)
y = zeros(ntot + burn, 1);
e = randn(ntot + burn, 1);
for t = 3:numel(y)
    y(t) = c + a(1)*y(t-1) + a(2)*y(t-2) + e(t);
end
y = y(burn + 1:end);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
