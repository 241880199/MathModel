function out = pca(opts)
%PCA  PCA on synthetic data with a KNOWN principal direction (v1 at 30 deg) and KNOWN
%     eigenvalues [4 1] (explained variance ratio [0.8000 0.2000]); recover them from samples.
%
%   M4 `mcm-model-select` 骨架 · statistics #1（主成分分析）。文件名全 ASCII（GC5）。
%
%   ★ 撞名处置：MATLAB 有**内置函数** `pca`（本机实测 `which('pca')` =
%     D:\Software\Matlab\toolbox\stats\stats\pca.m）；`addpath` 本目录后 **路径文件胜出**
%     （同 T7 的 `ga` 先例：路径优先于同名内置函数）。本名字**没有**顶层 `@pca` 类目录撞名
%     （实测 `find <matlabroot>/toolbox -type d -name "@pca"` ⇒ 0 命中）。
%     本文件用自写的**样本协方差特征分解**实现 PCA；内置 `pca` **不作独立参照**（同机同实现不独立）。
%
%   独立参照（第 3/4 类：合成数据 · 已知结构）—— 不是"跟另一段代码对"：
%     造 d=2 维合成数据，其**总体协方差** Sigma = V * diag([4 1]) * V'，
%     V = [cos30 -sin30; sin30 cos30]（**主方向 v1 与 x 轴夹角 = 30 deg**）
%     ⇒ **已知真值**：特征值 [4 1] · 解释方差比 [0.8000 0.2000] · v1 夹角 = 30 deg。
%     从 Sigma 抽样（固定种子）⇒ 用样本协方差的特征分解估计，与真值逐位对照。
%   ★ 特征向量**符号任意**（整体取反仍是同一主方向）⇒ 方向比较用**夹角 / |内积|**（符号无关）；
%   ★ **固定种子 + 多次运行**，给**逐次读数 + mean ± sd**（不是只跑一次）。
%
%   用法：
%     pca()             % 自检并打印读数
%     out = pca(opts)   % opts.n opts.seeds opts.L_true opts.theta_deg
%
%   返回 struct：L_true, V, L_est, rat_est, ang_est, err_ang, ip1, which1。

if nargin < 1 || isempty(opts); opts = struct(); end
n       = dflt(opts, 'n',         5000);
seeds   = dflt(opts, 'seeds',     1:20);
L_true  = dflt(opts, 'L_true',    [4 1]);      % 已知（总体）特征值
theta   = dflt(opts, 'theta_deg', 30);         % 已知主方向（度）
d       = numel(L_true);

v1 = [cosd(theta); sind(theta)];
V  = [v1, [-sind(theta); cosd(theta)]];        % 已知特征向量（主方向 30 deg）
Sigma = V * diag(L_true) * V';                 % 已知总体协方差
C = chol(Sigma);                               % Sigma = C'C；X = Z*C ⇒ cov(X) = Sigma

K = numel(seeds);
L_est = zeros(K, d); rat_est = zeros(K, d); ang_est = zeros(K, 1); ip1 = zeros(K, 1);
for s = 1:K
    rng(seeds(s));                             % ★ 固定种子（可复现）
    Z = randn(n, d);
    X = Z * C;                                 % 合成样本（总体协方差 = Sigma）
    S = cov(X);                                % 样本协方差
    [Vh, D] = eig(S);
    lam = diag(D);
    [lam, ord] = sort(lam, 'descend');         % ★ 排序（特征值不确定次序）
    Vh = Vh(:, ord);
    if Vh(1,1) < 0; Vh(:,1) = -Vh(:,1); end    % ★ 符号规范化（主方向取反仍是同一方向）
    L_est(s, :)   = lam(:)';
    rat_est(s, :) = (lam / sum(lam))';
    ang_est(s)    = atan2d(Vh(2,1), Vh(1,1));  % v1 与 x 轴夹角（deg）
    ip1(s)        = abs(Vh(:,1)' * v1);        % |内积|（符号无关，应 ≈ 1）
end

w = which('pca', '-all');                       % ★ 遮蔽守卫：首项应指向本仓文件（路径文件胜出）

L_mean   = mean(L_est, 1);
rat_mean = mean(rat_est, 1);
ang_mean = mean(ang_est);
err_ang  = mean(abs(ang_est - theta));
L_relerr = mean(abs(L_est - L_true) ./ L_true, 1);
rat_ae   = mean(abs(rat_est - [L_true(1) L_true(2)] / sum(L_true)), 1);

out = struct('L_true', L_true, 'V', V, 'L_est', L_est, 'rat_est', rat_est, ...
             'ang_est', ang_est, 'err_ang', err_ang, 'ip1', ip1, 'which1', which('pca'));

fprintf('[pca] synthetic n=%d, d=%d, seeds=%s\n', n, d, mat2str(seeds));
fprintf('  TRUE  eigenvalues = [%s]   explained ratio = [%s]   v1 angle = %.1f deg\n', ...
        num2str(L_true, '%.4g '), num2str(L_true / sum(L_true), '%.4f '), theta);
fprintf('  EST   eigenvalues = [%s]   explained ratio = [%s]   v1 angle = %.4f deg\n', ...
        num2str(L_mean, '%.4f '), num2str(rat_mean, '%.4f '), ang_mean);
fprintf('  eigenvalue rel-err = [%s]   explained-ratio abs-err = [%s]\n', ...
        num2str(L_relerr, '%.4f '), num2str(rat_ae, '%.5f '));
fprintf('  v1 angle |est - true| (mean) = %.4f deg   |cos(v1_est,v1_true)| (mean) = %.6f\n', ...
        err_ang, mean(ip1));
fprintf('  per-seed v1 angle = [%s]\n', num2str(ang_est(:)', '%.3f '));
fprintf('  which(''pca'',''-all'') first = %s\n', w{1});
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
