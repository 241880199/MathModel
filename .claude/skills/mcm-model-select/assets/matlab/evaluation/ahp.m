function out = ahp(opts)
%AHP  Analytic Hierarchy Process: priority weights + consistency ratio test.
%
%   M4 `mcm-model-select` 骨架 · evaluation #1（AHP 层次分析法）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `AHP` 命中 3 篇
%   （P2025-B-03 · P2025-B-07 · P2025-E-01）；`corpus/algorithms/src/`（脚本素材面）有起点素材
%   （`corpus/algorithms/src/AHP层次分析法/`，含 `ahp.m` / `sglsortexamine.m` / `tolsortvec.m`）。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 权向量**方根法（几何平均法）**  g_i = (prod_j a_ij)^(1/n)，w_i = g_i / sum_j g_j；
%     · 最大特征值  lam_max = (1/n) * sum_i (A w)_i / w_i；
%     · 一致性指标  CI = (lam_max - n) / (n - 1)；
%     · 一致性比率  CR = CI / RI(n)，判据 CR < 0.1。
%   ★ 另算**特征向量法**（eig 主特征向量）作交叉核对（两法权重接近、排序一致）。
%   ★ 逐步算式与手算期望值见 `tests/skills/model-select/verify/ahp.md`。
%
%   RI（随机一致性指标；Saaty 表，教科书级常识 `[社区]`）：
%     n   = 1     2     3     4     5     6     7     8     9    10
%     RI  = 0     0     0.58  0.90  1.12  1.24  1.32  1.41  1.45  1.49
%   ★ n = 1,2 时 RI = 0 ⇒ 不必要做一致性检验（本骨架对 n<=2 直接 CR = 0）。
%
%   用法：
%     ahp()             % 自检并打印读数（3x3 近一致算例 + 3x3 完全一致算例）
%     out = ahp(opts)   % opts.A
%
%   返回 struct：A, n, w, lam_max, CI, RI, CR, pass, w_eig, lam_eig。

if nargin < 1 || isempty(opts); opts = struct(); end
% 主算例：3x3 近一致（CR < 0.1）；手算期望值见参照件
A = dflt(opts, 'A', [1 2 5; 1/2 1 3; 1/5 1/3 1]);

n = size(A, 1);
assert(size(A, 2) == n, 'A 必须是方阵');
assert(all(all(abs(A .* A' - 1) < 1e-9)), 'A 必须是正互反矩阵（a_ij * a_ji = 1）');

RI_TABLE = [0 0 0.58 0.90 1.12 1.24 1.32 1.41 1.45 1.49];
if n <= numel(RI_TABLE); RI = RI_TABLE(n); else; RI = RI_TABLE(end); end

% --- 方根法（几何平均法）---
g = prod(A, 2) .^ (1 / n);
w = (g / sum(g)).';                 % 行向量

% --- 最大特征值 & 一致性 ---
Aw = A * w.';
lam_max = mean(Aw ./ w.');
if n > 1; CI = (lam_max - n) / (n - 1); else; CI = 0; end
if RI > 0; CR = CI / RI; else; CR = 0; end
pass = (CR < 0.1);

% --- 交叉核对：特征向量法（主特征向量）---
[V, D] = eig(A);
ev = diag(D);
[~, imax] = max(real(ev));
w_eig = real(V(:, imax));
w_eig = (w_eig / sum(w_eig)).';
lam_eig = real(ev(imax));

out = struct('A', A, 'n', n, 'w', w, 'lam_max', lam_max, ...
             'CI', CI, 'RI', RI, 'CR', CR, 'pass', pass, ...
             'w_eig', w_eig, 'lam_eig', lam_eig);

fprintf('[ahp] n = %d，方根法（几何平均法）\n', n);
fprintf('  w       = [%s]\n', num2str(w, '%.12g  '));
fprintf('  lam_max = %.12g   CI = %.12g   RI = %.4g   CR = %.12g\n', lam_max, CI, RI, CR);
if pass; verdict = '通过'; else; verdict = '不通过'; end
fprintf('  一致性判据 CR < 0.1 : %s\n', verdict);
fprintf('[ahp] 交叉核对 · 特征向量法\n');
fprintf('  w_eig   = [%s]\n', num2str(w_eig, '%.12g  '));
fprintf('  lam_eig = %.12g   max|w - w_eig| = %.3e\n', lam_eig, max(abs(w - w_eig)));

% --- 附：完全一致算例（展示 lam_max = n、CI = 0）---
A0 = [1 2 3; 1/2 1 3/2; 1/3 2/3 1];
g0 = prod(A0, 2) .^ (1 / 3);
w0 = (g0 / sum(g0)).';
lam0 = mean((A0 * w0.') ./ w0.');
fprintf('[ahp] 附：完全一致算例 A0（权向量应为 [6 3 2]/11）\n');
fprintf('  w0      = [%s]\n', num2str(w0, '%.12g  '));
fprintf('  lam_max = %.12g   CI = %.3e\n', lam0, (lam0 - 3) / 2);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
