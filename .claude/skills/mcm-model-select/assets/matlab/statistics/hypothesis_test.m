function out = hypothesis_test(opts)
%HYPOTHESIS_TEST  Hypothesis tests on known-parameter synthetic data (rejection rates).
%
%   M4 `mcm-model-select` 骨架 · statistics #5（假设检验：t 检验 / 非参数检验 / 多重比较）。
%   文件名全 ASCII（GC5）—— 中文名不能作为 MATLAB 函数被调用。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `hypothesis test` 有实例
%   （P2025-A-01 · P2025-A-05 · P2025-B-05 · P2025-C-01 · P2025-C-13 · P2025-C-14 · P2025-C-15 · P2025-F-01）；
%   `corpus/algorithms/src/`（脚本素材面）0 命中。详见 `tests/skills/model-select/verify/hypothesis_test.md`.
%
%   独立参照（第 4 类：已知参数的合成数据 + 检验拒绝率）—— 不是"跟另一段代码对"：
%     · H0 为真（样本来自已知正态、真均值 = 假设值）时，5% 显著性水平下**拒绝率应 ≈ 0.05**
%       （第一类错误率 = 名义水平）；
%     · H1 为真（真均值偏离假设值、效应量 delta/sigma = 0.5）时，**拒绝率 = 检验功效**，
%       应显著高于 0.05。
%   ★ 随机抽样固定种子；本骨架内部跑多个种子，给**多次运行的分布**（不是只跑一次）。
%
%   用法：
%     hypothesis_test()             % 自检并打印读数
%     out = hypothesis_test(opts)   % opts.alpha opts.nrep opts.n opts.seeds opts.mu_h1
%
%   返回 struct：ttest_1samp / ttest_2samp / signrank 三组检验在 H0、H1 下的
%   拒绝率（逐种子向量 + 均值 + 标准差）。

if nargin < 1 || isempty(opts); opts = struct(); end
alpha = dflt(opts, 'alpha', 0.05);
nrep  = dflt(opts, 'nrep',  2000);
n     = dflt(opts, 'n',     30);
seeds = dflt(opts, 'seeds', 0:4);
mu_h1 = dflt(opts, 'mu_h1', 0.5);   % 效应量 = 0.5 / sigma(=1)

mu_h0 = 0;
k     = numel(seeds);
t1_h0 = zeros(1, k); t1_h1 = zeros(1, k);
t2_h0 = zeros(1, k); t2_h1 = zeros(1, k);
sr_h0 = zeros(1, k); sr_h1 = zeros(1, k);

for s = 1:k
    rng(seeds(s));
    a=0; b=0; c=0; d=0; e=0; f=0;
    for i = 1:nrep
        x0 = mu_h0 + randn(n, 1);          % H0 为真
        x1 = mu_h1 + randn(n, 1);          % H1 为真
        y0 = mu_h0 + randn(n, 1);
        y1 = mu_h0 + randn(n, 1);          % 双样本 H1 的对照组（均值仍为 mu_h0 ⇒ 两组真差 = mu_h1）

        [~, pa] = ttest(x0, mu_h0);       a = a + (pa < alpha);   % 单样本 t（H0）
        [~, pb] = ttest(x1, mu_h0);       b = b + (pb < alpha);   % 单样本 t（H1）
        [~, pc] = ttest2(x0, y0);         c = c + (pc < alpha);   % 双样本 t（H0）
        [~, pd] = ttest2(x1, y1);         d = d + (pd < alpha);   % 双样本 t（H1）
        [pe, ~] = signrank(x0, mu_h0);    e = e + (pe < alpha);   % Wilcoxon 符号秩（H0）
        [pf, ~] = signrank(x1, mu_h0);    f = f + (pf < alpha);   % Wilcoxon 符号秩（H1）
    end
    t1_h0(s)=a/nrep; t1_h1(s)=b/nrep; t2_h0(s)=c/nrep;
    t2_h1(s)=d/nrep; sr_h0(s)=e/nrep; sr_h1(s)=f/nrep;
end

out = struct( ...
  'alpha', alpha, 'nrep', nrep, 'n', n, 'seeds', seeds, 'mu_h1', mu_h1, ...
  'ttest_1samp_h0', t1_h0, 'ttest_1samp_h1', t1_h1, ...
  'ttest_2samp_h0', t2_h0, 'ttest_2samp_h1', t2_h1, ...
  'signrank_h0',    sr_h0, 'signrank_h1',    sr_h1, ...
  'reject_h0_mean', mean([t1_h0, t2_h0, sr_h0]), ...
  'reject_h0_sd',   std([t1_h0, t2_h0, sr_h0]) );

fprintf('[hypothesis_test] alpha = %.4g, nrep = %d, n = %d, mu_H1 = %.4g, seeds = [%s]\n', ...
        alpha, nrep, n, mu_h1, num2str(seeds));
fprintf('  单样本 t  H0 真: reject rate = %.4f  (期望 ~ %.3g)\n', mean(t1_h0), alpha);
fprintf('  单样本 t  H1 真: reject rate = %.4f  (功效, 应 >> alpha)\n', mean(t1_h1));
fprintf('  双样本 t  H0 真: reject rate = %.4f  (期望 ~ %.3g)\n', mean(t2_h0), alpha);
fprintf('  双样本 t  H1 真: reject rate = %.4f  (功效)\n', mean(t2_h1));
fprintf('  符号秩    H0 真: reject rate = %.4f  (期望 ~ %.3g)\n', mean(sr_h0), alpha);
fprintf('  符号秩    H1 真: reject rate = %.4f  (功效)\n', mean(sr_h1));
fprintf('  --- 多次运行分布（%d 个种子）---\n', k);
fprintf('    H0 拒绝率 均值 = %.4f, 标准差 = %.4f\n', ...
        mean([t1_h0, t2_h0, sr_h0]), std([t1_h0, t2_h0, sr_h0]));
fprintf('    单样本 t  H0 逐种子 = [%s]\n', num2str(t1_h0, '%.4f  '));
fprintf('    双样本 t  H0 逐种子 = [%s]\n', num2str(t2_h0, '%.4f  '));
fprintf('    符号秩    H0 逐种子 = [%s]\n', num2str(sr_h0, '%.4f  '));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
