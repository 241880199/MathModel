function out = clustering(opts)
%CLUSTERING  Unsupervised clustering by K-means and fuzzy C-means on synthetic
%   data with a KNOWN structure: k = 3 well-separated Gaussian clusters (fixed
%   centers, equal size).  Checks the recovery rate (up to label permutation) and
%   the centroid error.  k KNOWN vs k UNKNOWN are reported separately (unknown k
%   is chosen by silhouette over k = 1..6, which should return k = 3).
%   Fuzzy C-means additionally reports MEMBERSHIP readouts (partition coefficient).
%
%   M4 `mcm-model-select` 骨架 · ml #5（聚类：K-means / 模糊 C-means）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@clustering` 类目录撞名（实测 2026-10-04）。★ MATLAB 路径上有一个**普通文件夹**
%     `toolbox/stats/clustering`（非 `@` 类目录）⇒ 不遮蔽本文件；`which('clustering','-all')` 首项仍是本文件。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `K-means` 带锚 **2 行 / 去重 4 篇**
%   （`P2025-C-06 C-08 F-02 F-03`；2026-10-04 当场复跑带锚形，逐条命令见 verify 记录）。
%   ★ 泛指词 `cluster analysis`（11 篇，**归属存疑**）不含在"K-means/FCM 专属指针"内（见六格语料面）。
%   `corpus/algorithms/src/`（模糊聚类）有 3 件起点素材（见六格），**不作独立参照**。
%
%   独立参照（第 4 类：已知簇结构的合成数据）：
%     · k = 3 个**中心已知**、等大小的高斯簇 ⇒ 簇分配还原率（对标签置换不变）+ 质心误差；
%     · k **未知**时用轮廓系数在 k = 1..6 上选，应选回 k = 3；
%     · 模糊 C-means 给**隶属度**读数（划分系数 partition coefficient）。
%   ★ **不许拿 MATLAB 内置当"独立参照"** —— `kmeans`/`fcm` 只作**实现**；参照是**已知簇结构**。
%   ★ 固定种子 + **多次运行的分布**（不是只跑一次）。
%
%   用法：
%     clustering()             % 自检并打印读数
%     out = clustering(opts)   % opts.K opts.nper opts.sep opts.seeds
%
%   返回 struct：K, nper, sep, seeds, recover_km_seeds, recover_km_mean, recover_km_sd,
%                centroid_max_seeds, centroid_max_mean, khat_seeds, pc_seeds, pc_mean,
%                recover_fcm_seeds, recover_fcm_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
K     = dflt(opts, 'K',    3);
nper  = dflt(opts, 'nper', 200);
sep   = dflt(opts, 'sep',  5);        % 簇间尺度（中心分离量级）
seeds = dflt(opts, 'seeds', 1:5);

% --- 已知簇结构：K 个中心在半径 sep 的圆上均匀分布 ---
th0 = 2 * pi * (0:K-1)' / K;
C_true = sep * [cos(th0), sin(th0)];

rec_km  = zeros(1, numel(seeds));
cen_max = zeros(1, numel(seeds));
khat    = zeros(1, numel(seeds));
pc      = zeros(1, numel(seeds));
rec_fcm = zeros(1, numel(seeds));
for s = 1:numel(seeds)
    rng(seeds(s));
    X = []; Ytrue = [];
    for j = 1:K
        X = [X; C_true(j, :) + randn(nper, 2)];   %#ok<AGROW>
        Ytrue = [Ytrue; j * ones(nper, 1)];       %#ok<AGROW>
    end

    % --- K-means（k 已知）---
    rng(seeds(s) + 100);
    [lab, C] = kmeans(X, K, 'Replicates', 10);
    [rr, perm] = bestperm(lab, Ytrue, K);
    rec_km(s) = rr;
    Cm = zeros(K, 2); Cm(perm, :) = C;         % 按标签映射重排质心到真簇序
    cen_max(s) = max(sqrt(sum((Cm - C_true).^2, 2)));   % 匹配后各质心的最大误差

    % --- k 未知：轮廓系数选 k ---
    ev = evalclusters(X, 'kmeans', 'silhouette', 'KList', 1:6);
    khat(s) = ev.OptimalK;

    % --- 模糊 C-means（k 已知）---
    rng(seeds(s) + 200);
    [~, U] = fcm(X, K, [2, 100, 1e-5, 0]);
    [~, lab_f] = max(U, [], 1);
    rf = bestperm(lab_f(:), Ytrue, K);
    rec_fcm(s) = rf;
    pc(s) = sum(U(:).^2) / size(X, 1);           % 划分系数 PC = (1/n) sum_{i,j} u_ij^2（越接近 1 越硬）
end

out = struct('K', K, 'nper', nper, 'sep', sep, 'seeds', seeds, ...
             'C_true', C_true, ...
             'recover_km_seeds', rec_km, 'recover_km_mean', mean(rec_km), 'recover_km_sd', std(rec_km), ...
             'centroid_max_seeds', cen_max, 'centroid_max_mean', mean(cen_max), ...
             'khat_seeds', khat, ...
             'pc_seeds', pc, 'pc_mean', mean(pc), ...
             'recover_fcm_seeds', rec_fcm, 'recover_fcm_mean', mean(rec_fcm));

fprintf('[clustering] K = %d known Gaussian clusters (sep = %g), %d points, %d seeds\n', ...
        K, sep, K * nper, numel(seeds));
fprintf('  K-means   : recovery per seed = [%s]  mean = %.4f +/- %.4f\n', ...
        num2str(rec_km, '%.4f  '), mean(rec_km), std(rec_km));
fprintf('              matched centroid max err per seed = [%s]  mean = %.4f\n', ...
        num2str(cen_max, '%.4f  '), mean(cen_max));
fprintf('  k UNKNOWN : silhouette-optimal k per seed = [%s]  (true K = %d)\n', ...
        num2str(khat, '%d '), K);
fprintf('  FCM       : recovery per seed = [%s]  mean = %.4f\n', ...
        num2str(rec_fcm, '%.4f  '), mean(rec_fcm));
fprintf('              partition coefficient per seed = [%s]  mean = %.4f  (closer to 1 = crisper)\n', ...
        num2str(pc, '%.4f  '), mean(pc));
end

function [rate, perm] = bestperm(lab, truth, K)
% 簇标签可置换 ⇒ 在 K! 种映射里取还原率最高者（K 小时枚举即可）
P = perms(1:K);
best = -1; perm = 1:K;
for i = 1:size(P, 1)
    m = P(i, :);
    pred = m(lab);                 % 应用标签映射（pred 的形状随索引用 (:) 归一到列）
    r = mean(pred(:) == truth(:));
    if r > best; best = r; perm = m; end
end
rate = best;
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
