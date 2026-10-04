function out = abm(opts)
%ABM  Agent-based model (DeGroot consensus): deterministic 3-agent update + property checks.
%
%   M4 `mcm-model-select` 骨架 · simulation #4（ABM · 多智能体仿真）。文件名全 ASCII（GC5）。
%
%   语料面（P5 · P6）：`[社区]` —— `agent-based` / `ABM` 在 `corpus/papers/MODEL_MAP.md` **0 命中**
%   （2026-10-04 当场复跑）；`corpus/algorithms/src/` 0 命中。★ **低使用度、照补是为覆盖面**。
%   ★ 披露（**不声称穷尽**）：原始语料 md 里 `multi-agent` 有 1 处
%   （`corpus/papers/md/2025美赛O奖论文/D/2516219.md` §7.5，是 "multi-agent welfare framework" 的
%   stakeholder 框定、非 ABM 仿真），因该词不在受控词表内故未进 `MODEL_MAP.md`（词表漏配）。
%
%   独立参照：★★ **人工兜底（设计 §4.1）** —— ABM 无解析解、输出是涌现行为、无 ground truth。
%     ① **2–3 agent 的确定性手算小例**（DeGroot 意见更新，逐步可手推，算式见 verify 记录）；
%     ② **性质检查**：和守恒（W 双随机）/ 边界行为 / 收敛到均值。
%   ★ **本项参照是人工兜底、不是可机械核的参照**（见 verify 记录；`MS3` 判不到"独立性"那一层）。
%
%   模型：3 个 agent 在一维线上，状态 x 连续，按**行/列双随机**权重矩阵 W 更新 x' = W x
%   （每个 agent 的新状态 = 自己与邻居的加权平均；W 双随机 ⇒ 总和守恒）。
%
%   用法：
%     abm()             % 自检并打印读数
%     out = abm(opts)   % opts.W opts.x0 opts.steps
%
%   返回 struct：W, x0, X, step1_expected, step1_max_ae, sum_conserved, consensus, mean_x0。

if nargin < 1 || isempty(opts); opts = struct(); end
W     = dflt(opts, 'W', [0.5 0.5 0; 0.5 0.0 0.5; 0 0.5 0.5]);   % 对称、双随机
x0    = dflt(opts, 'x0', [1; 0; 3]);
steps = dflt(opts, 'steps', 30);

X = zeros(steps + 1, numel(x0));
X(1, :) = x0(:)';
for t = 1:steps
    X(t + 1, :) = (W * X(t, :)')';
end

% --- 性质检查 ---
step1_expected = [0.5; 2.0; 1.5];                 % 手算：W*x0（见 verify 记录）
step1_max_ae   = max(abs(X(2, :)' - step1_expected));
sum_conserved  = all(abs(sum(X, 2) - sum(x0)) < 1e-12);
mean_x0        = mean(x0);
consensus      = max(abs(X(end, :)' - mean_x0));

out = struct('W', W, 'x0', x0, 'X', X, ...
             'step1_expected', step1_expected, 'step1_max_ae', step1_max_ae, ...
             'sum_conserved', sum_conserved, 'consensus', consensus, 'mean_x0', mean_x0);

fprintf('[abm] DeGroot consensus: 3 agents, x'' = W x (W doubly stochastic)\n');
fprintf('  x0      = [%s]\n', num2str(x0(:)', '%.4g '));
fprintf('  step 1  = [%s]   (hand: [%s], max|diff| = %.3e)\n', ...
        num2str(X(2, :), '%.4g '), num2str(step1_expected', '%.4g '), step1_max_ae);
fprintf('  after %d steps = [%s]\n', steps, num2str(X(end, :), '%.6f '));
fprintf('  sum conserved every step (W doubly stochastic) = %d\n', sum_conserved);
fprintf('  |x_end - mean(x0)| = %.3e  (consensus to the mean %.6f)\n', consensus, mean_x0);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
