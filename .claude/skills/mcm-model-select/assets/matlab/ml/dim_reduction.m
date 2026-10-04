function out = dim_reduction(opts)
%DIM_REDUCTION  t-SNE on synthetic clusters + neighbourhood-preservation (kNN consistency).
%
%   M4 `mcm-model-select` 骨架 · ml #6（降维：t-SNE / UMAP）。文件名全 ASCII（GC5）。
%
%   ★ 内置只有 `tsne`；**`umap` MATLAB 无内置**（`which umap` 实测为空）⇒ 本骨架**只给 t-SNE**，
%     并把"**UMAP 需外部包**（如第三方 `umap` / `run_umap`）"登记为**已知边界**（不假装有）。
%
%   语料面（P5 · P6）：`[社区]` —— `t-SNE` / `UMAP` 在 `corpus/papers/MODEL_MAP.md` **0 命中**
%   （2026-10-04 当场复跑）；`corpus/algorithms/src/` 0 命中。★ **低使用度、照补是为覆盖面**。
%   ★ 披露（**不声称穷尽**）：原始语料 md 里 `t-SNE` 有 1 处
%   （`corpus/papers/md/2025美赛O奖论文/F/2507789.md` §6.4，用作可视化），因该词不在受控词表内故未进 `MODEL_MAP.md`。
%
%   独立参照：★★ **人工兜底（设计 §4.1）** —— t-SNE 非确定性、**没有 ground-truth 输出**
%     （"看上去分开了"不是判据）。兜底：
%     · **已知簇结构的合成流形**（3 个高斯簇，在 R^d 里中心已知）；
%     · **邻域保持率（kNN 一致性）**：原空间 k 近邻里有多少在对偶嵌入里仍是 k 近邻（**可算的量**）；
%     · 固定随机种子（实测 `rng(seed)` 后 `tsne` **逐位可复现**）。
%   ★ **本项参照是人工兜底、不是可机械核的参照**（见 verify 记录）。
%
%   用法：
%     dim_reduction()             % 自检并打印读数
%     out = dim_reduction(opts)   % opts.k opts.nper opts.seeds opts.perp opts.d
%
%   返回 struct：knn_consistency（逐种子向量）, knn_mean, knn_sd, silhouette, purity,
%                umap_available, Y, labels, X, k, seeds。

if nargin < 1 || isempty(opts); opts = struct(); end
k     = dflt(opts, 'k',     10);
nper  = dflt(opts, 'nper',  90);
seeds = dflt(opts, 'seeds', 0:4);
perp  = dflt(opts, 'perp',  30);
d     = dflt(opts, 'd',     10);
K     = 3;

% --- 已知簇结构的合成流形 ---
rng(0);                                  % 合成数据本身固定（不随 t-SNE 的种子变）
centers = zeros(K, d);
for j = 1:K; centers(j, j) = 6; end
X = []; labels = [];
for j = 1:K
    X = [X; centers(j, :) + randn(nper, d)];      %#ok<AGROW>
    labels = [labels; j * ones(nper, 1)];         %#ok<AGROW>
end
idxX = knnsearch(X, X, 'K', k + 1); idxX(:, 1) = [];   % 原空间 k 近邻（与 t-SNE 种子无关）

% --- 逐种子：t-SNE 嵌入 + 邻域保持率（kNN 一致性） + 簇纯度 ---
ks = numel(seeds);
knn = zeros(1, ks); sil_v = zeros(1, ks); pur = zeros(1, ks);
for s = 1:ks
    rng(seeds(s));                       % ★ 固定种子（t-SNE 非确定性；实测给定 rng 后逐位可复现）
    Y = tsne(X, 'NumDimensions', 2, 'Perplexity', perp, 'Verbose', 0);
    idxY = knnsearch(Y, Y, 'K', k + 1); idxY(:, 1) = [];
    c = 0;
    for i = 1:size(X, 1)
        c = c + numel(intersect(idxX(i, :), idxY(i, :))) / k;
    end
    knn(s) = c / size(X, 1);
    sil_v(s) = mean(silhouette(Y, labels));
    kidx = kmeans(Y, K, 'Replicates', 5);
    p = 0;
    for cc = 1:K
        m = mode(labels(kidx == cc));
        p = p + sum(kidx == cc & labels == m);
    end
    pur(s) = p / numel(labels);
    if s == 1; Y1 = Y; end
end
umap_available = ~isempty(which('umap'));

out = struct('knn_consistency', knn, 'silhouette', sil_v, 'purity', pur, ...
             'knn_mean', mean(knn), 'knn_sd', std(knn), 'purity_mean', mean(pur), ...
             'umap_available', umap_available, 'Y', Y1, 'labels', labels, 'X', X, ...
             'k', k, 'seeds', seeds);

fprintf('[dim_reduction] t-SNE on %d points (3 Gaussian clusters, d = %d, k = %d, %d seeds)\n', ...
        size(X, 1), d, k, ks);
fprintf('  kNN consistency per seed = [%s]\n', num2str(knn, '%.4f  '));
fprintf('  kNN consistency          = %.4f +/- %.4f  (local-order preserved; a RELATIVE number)\n', ...
        mean(knn), std(knn));
fprintf('  silhouette  per seed     = [%s]\n', num2str(sil_v, '%.4f  '));
fprintf('  cluster purity per seed  = [%s]  (known cluster structure recovered)\n', num2str(pur, '%.4f  '));
fprintf('  umap available on path   = %d   (MATLAB has no built-in UMAP)\n', umap_available);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
