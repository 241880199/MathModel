function out = anova(opts)
%ANOVA  One-way / two-way analysis of variance on known-parameter synthetic data.
%
%   M4 `mcm-model-select` 骨架 · statistics #6（方差分析：单因素 / 多因素）。
%   文件名全 ASCII（GC5）—— 中文名不能作为 MATLAB 函数被调用。
%
%   语料面（P6）：**带语料指针（薄）** —— `corpus/papers/MODEL_MAP.md` 里 `analysis of variance`
%   命中 1 篇（P2025-C-18，其正文有 "Analysis of Variance, Mixed-effects Model" 一节）；
%   `corpus/algorithms/src/`（脚本素材面）0 命中。详见 `tests/skills/model-select/verify/anova.md`.
%
%   独立参照（第 4 类：已知参数的合成数据）—— 不是"跟另一段代码对"：
%     · 各组真均值相同（H0 为真）时，5% 水平下**拒绝率应 ≈ 0.05**（单因素 F 检验的名义水平）；
%     · 各组真均值有已知差（H1 为真）时，**p 值应 < alpha**、拒绝率 = 功效；
%     · **F 统计量另与手算的 SSB/SSW 分解对照**（组间/组内平方和的定义式）。
%   ★ 随机抽样固定种子；本骨架内部跑多个种子，给**多次运行的分布**。
%
%   用法：
%     anova()             % 自检并打印读数
%     out = anova(opts)   % opts.alpha opts.nrep opts.nper opts.delta opts.seeds
%
%   返回 struct：单因素 H0/H1 的 p 与拒绝率、手算 F、双因素两效应的 p。

if nargin < 1 || isempty(opts); opts = struct(); end
alpha = dflt(opts, 'alpha', 0.05);
nrep  = dflt(opts, 'nrep',  2000);
nper  = dflt(opts, 'nper',  10);      % 每组样本数
delta = dflt(opts, 'delta', 0.8);     % H1 时第三组相对第一组的均值偏移
seeds = dflt(opts, 'seeds', 0:4);

k = 3;                                % 单因素：3 组
seeds = seeds(:)';
kk = numel(seeds);
rej_h0 = zeros(1, kk); rej_h1 = zeros(1, kk);

for s = 1:kk
    rng(seeds(s));
    r0 = 0; r1 = 0;
    for i = 1:nrep
        x0 = [zeros(nper,1); zeros(nper,1); zeros(nper,1)];      % H0：三组同均值
        g  = [ones(nper,1); 2*ones(nper,1); 3*ones(nper,1)];
        x0 = x0 + randn(k*nper, 1);
        p0 = anova1(x0, g, 'off');
        r0 = r0 + (p0 < alpha);

        x1 = [zeros(nper,1); 0.5*delta*ones(nper,1); delta*ones(nper,1)];
        x1 = x1 + randn(k*nper, 1);
        p1 = anova1(x1, g, 'off');
        r1 = r1 + (p1 < alpha);
    end
    rej_h0(s) = r0/nrep; rej_h1(s) = r1/nrep;
end

% --- 手算 F 对照（确定性数据，一次）---
rng(0);
xd = [zeros(nper,1); 0.5*delta*ones(nper,1); delta*ones(nper,1)] + randn(k*nper, 1);
gd = [ones(nper,1); 2*ones(nper,1); 3*ones(nper,1)];
[pd, tbld] = anova1(xd, gd, 'off');
F_builtin  = tbld{2, 5};
grand      = mean(xd);
SSB = sum(arrayfun(@(j) sum(gd==j) * (mean(xd(gd==j)) - grand)^2, 1:k));
SSW = sum(arrayfun(@(j) sum((xd(gd==j) - mean(xd(gd==j))).^2), 1:k));
N   = numel(xd);
F_manual = (SSB/(k-1)) / (SSW/(N-k));
p_manual = 1 - fcdf(F_manual, k-1, N-k);

% --- 双因素（可加效应，2 因素各 2 水平 × 3 重复）---
% anova2 格式：X 为 (a*reps) × b，每 reps 行为因素 A 的一个水平、每列为因素 B 的一个水平
rng(1);
reps = 3; aA = 2; aB = 2;
X2 = zeros(aA*reps, aB);
for ia = 1:aA
    for ib = 1:aB
        for r = 1:reps
            X2((ia-1)*reps + r, ib) = (ia-1)*1.0 + (ib-1)*1.5 + randn;
        end
    end
end
[p2, ~] = anova2(X2, reps, 'off');
p_facB = p2(1);     % 列因素 B（已知效应 1.5）
p_facA = p2(2);     % 行因素 A（已知效应 1.0）

out = struct('alpha', alpha, 'nrep', nrep, 'nper', nper, 'delta', delta, 'seeds', seeds, ...
  'reject_h0', rej_h0, 'reject_h1', rej_h1, ...
  'reject_h0_mean', mean(rej_h0), 'reject_h0_sd', std(rej_h0), ...
  'F_builtin', F_builtin, 'F_manual', F_manual, 'p_manual', p_manual, ...
  'p_two_way_facA', p_facA, 'p_two_way_facB', p_facB);

fprintf('[anova] alpha = %.4g, nrep = %d, nper = %d, delta = %.4g, seeds = [%s]\n', ...
        alpha, nrep, nper, delta, num2str(seeds));
fprintf('  单因素 anova1 H0 真: 拒绝率 均值 = %.4f, 标准差 = %.4f (期望 ~ %.3g)\n', ...
        mean(rej_h0), std(rej_h0), alpha);
fprintf('  单因素 anova1 H1 真: 拒绝率 = %.4f (功效, 应 >> alpha)\n', mean(rej_h1));
fprintf('  手算 vs 内置 F : F_builtin = %.9g, F_manual = %.9g, 相对差 = %.3e\n', ...
        F_builtin, F_manual, abs(F_builtin-F_manual)/F_builtin);
fprintf('  双因素 anova2 : p_A = %.6g, p_B = %.6g (已知 A 效应 1.0, B 效应 1.5 ⇒ 均 < alpha)\n', ...
        p_facA, p_facB);
fprintf('  --- 多次运行分布（%d 个种子）H0 拒绝率逐种子 = [%s]\n', kk, num2str(round(rej_h0,4)));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
