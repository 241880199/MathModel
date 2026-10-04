function out = factor_analysis(opts)
%FACTOR_ANALYSIS  Factor analysis on synthetic data with known loadings (recover loadings).
%
%   M4 `mcm-model-select` 骨架 · ml #7（因子分析）。文件名全 ASCII（GC5）。内置 `factoran`。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `factor analysis` 命中 5 篇
%   （去重：P2025-B-05 · C-14 · D-02 · F-02 · F-03；2026-10-04 当场复跑）。
%   `corpus/algorithms/src/`（脚本素材面）0 命中。逐条命令见 verify 记录。
%
%   独立参照（第 4 类：已知因子载荷的合成数据 ⇒ 载荷可复原）：
%     · 造一个**已知载荷 Λ 与唯一性 Ψ** 的正交因子模型 X = F Λ' + E（F ~ N(0, I_k)）；
%       ★ **令每个变量的方差 = ‖Λ_i‖² + Ψ_i = 1**（取 Ψ_i = 1 − ‖Λ_i‖²）——
%         因为内置 `factoran` **内部会标准化**（实测：`factoran(X,…)` 与 `factoran(zscore(X),…)`
%         结果**至 ~1e-12 量级相同**、非逐位相同），令方差 = 1 后这一标准化成为**恒等**，
%         估计出的载荷才直接对得上真值。
%     · 用内置 `factoran` 反估 ⇒ 载荷**在旋转意义下**可复原，故按两条比：
%       (a) **公因子方差（行范数 ‖Λ_i‖²）旋转不变** ⇒ 直接比；
%       (b) 载荷本身用**旋转对齐**（2×2 正交 R 由 SVD 解出）后比 —— 因子解只定到正交旋转，
%           **不假装唯一**。
%   ★ 固定种子。
%
%   用法：
%     factor_analysis()             % 自检并打印读数
%     out = factor_analysis(opts)   % opts.n opts.seed opts.k
%
%   返回 struct：Lambda_true, Lambda_hat, Lambda_aligned, Psi_true, Psi_hat,
%                comm_true, comm_hat, comm_max_ae, load_max_ae, psi_max_ae。

if nargin < 1 || isempty(opts); opts = struct(); end
n    = dflt(opts, 'n',    2000);
seed = dflt(opts, 'seed', 0);
k    = dflt(opts, 'k',    2);

% --- 已知载荷/唯一性（p = 6 变量、k 因子）---
Lambda_true = [0.9 0.0; 0.8 0.0; 0.7 0.2; 0.0 0.9; 0.0 0.8; 0.1 0.7];
Psi_true    = 1 - sum(Lambda_true.^2, 2);     % 令变量方差 = 1（factoran 内部标准化成为恒等）
p = size(Lambda_true, 1);

rng(seed);
F = randn(n, k);
E = randn(n, p) .* sqrt(Psi_true');           % 每列尺度 sqrt(Psi_i)
X = F * Lambda_true' + E;

[Lambda_hat, Psi_hat] = factoran(X, k, 'rotate', 'none');

% (a) 旋转不变的公因子方差
comm_true = sum(Lambda_true.^2, 2);
comm_hat  = sum(Lambda_hat.^2, 2);
comm_max_ae = max(abs(comm_hat - comm_true));

% (b) 载荷旋转对齐（纯正交旋转，无缩放/平移）：解 R = argmin ||Λ_t - Λ_h R||
M = Lambda_hat' * Lambda_true;
[U, ~, V] = svd(M);
R = U * V';
Lambda_aligned = Lambda_hat * R;
load_max_ae = max(abs(Lambda_aligned(:) - Lambda_true(:)));
psi_max_ae  = max(abs(Psi_hat - Psi_true));

out = struct('Lambda_true', Lambda_true, 'Lambda_hat', Lambda_hat, 'Lambda_aligned', Lambda_aligned, ...
             'Psi_true', Psi_true, 'Psi_hat', Psi_hat, ...
             'comm_true', comm_true, 'comm_hat', comm_hat, ...
             'comm_max_ae', comm_max_ae, 'load_max_ae', load_max_ae, 'psi_max_ae', psi_max_ae);

fprintf('[factor_analysis] X = F*Lambda'' + E,  p = %d vars, k = %d factors, n = %d, seed = %d\n', ...
        p, k, n, seed);
fprintf('  communalities (rotation-invariant)  true = [%s]\n', num2str(comm_true', '%.4f '));
fprintf('                                      est  = [%s]   max|diff| = %.4f\n', ...
        num2str(comm_hat', '%.4f '), comm_max_ae);
fprintf('  loadings after orthogonal align: max|diff| = %.4f\n', load_max_ae);
fprintf('  uniqueness Psi: max|diff| = %.4f\n', psi_max_ae);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
