function out = var_cluster(opts)
%VAR_CLUSTER  Variable clustering: cluster the VARIABLES of synthetic data built from 2 known
%   latent factors (3 variables each); distance = 1 - |corr|; complete/average linkage; cut@2
%   recovers the 2 known variable groups {v1,v2,v3} and {v4,v5,v6}.
%
%   M4 `mcm-model-select` 骨架 · statistics #3（变量聚类 / R 型聚类）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@<名>` 类目录撞名（实测 find <matlabroot>/toolbox -name "@var_cluster" ⇒ 0）。
%   ★ **与 `hierarchical_cluster` 的边界**：本方法聚的是**变量**（corr 矩阵的行列，R 型聚类）；
%     `hierarchical_cluster` 聚的是**样本**（Q 型聚类）。两者共用 `linkage`/`cluster`，但**输入对象不同**。
%
%   独立参照（第 3/4 类：合成数据 · 已知变量结构）—— 不是"跟 MATLAB 内置对"：
%     · 变量 v1..v6 由**已知隐因子**生成：v1,v2,v3 = f1 + 小噪声；v4,v5,v6 = f2 + 小噪声（f1 ⟂ f2）
%       ⇒ **已知真值**：变量分群 = {1,2,3} / {4,5,6}；且**组内 |corr| 高、组间 |corr| 低**；
%     · 距离 = `1 - |corr|`，割树成 2 群 ⇒ 应**还原**已知变量分组。
%   ★ 链接方式（complete/average）显式；★ 固定种子，给**逐种子还原率 + 组内/组间平均 |corr|**。
%   ★ MATLAB 的 `corr`/`linkage`/`cluster` 只作**实现**，**不作独立参照**（同机同实现不独立）。
%
%   用法：
%     var_cluster()             % 自检并打印读数
%     out = var_cluster(opts)   % opts.n opts.seeds opts.noise opts.vtruth opts.methods
%
%   返回 struct：vtruth, R（代表相关阵）, within, between, acc（各法 cut@2 还原率）, groups。

if nargin < 1 || isempty(opts); opts = struct(); end
n       = dflt(opts, 'n',      500);
seeds   = dflt(opts, 'seeds',  1:20);
noise   = dflt(opts, 'noise',  0.30);
vtruth  = dflt(opts, 'vtruth', [1 1 1 2 2 2]');   % 已知变量分群（2 群，各 3）
methods = dflt(opts, 'methods', {'complete', 'average'});
p = numel(vtruth);

nm = numel(methods);
acc = zeros(1, nm); groups = cell(1, nm);
for i = 1:nm
    acc_i = zeros(1, numel(seeds));
    for s = 1:numel(seeds)
        rng(seeds(s));
        f1 = randn(n, 1); f2 = randn(n, 1);
        Xv = [f1 + noise*randn(n,1), f1 + noise*randn(n,1), f1 + noise*randn(n,1), ...
              f2 + noise*randn(n,1), f2 + noise*randn(n,1), f2 + noise*randn(n,1)];
        R = corr(Xv);
        D = 1 - abs(R); D(1:p+1:end) = 0;         % 距离 = 1 - |corr|，对角 0
        Z = linkage(squareform(D), methods{i});
        lab = cluster(Z, 2);
        a1 = mean(lab == vtruth); a2 = mean(lab == (3 - vtruth));
        acc_i(s) = max(a1, a2);
    end
    acc(i) = mean(acc_i);
    rng(seeds(1));
    f1 = randn(n, 1); f2 = randn(n, 1);
    Xv = [f1 + noise*randn(n,1), f1 + noise*randn(n,1), f1 + noise*randn(n,1), ...
          f2 + noise*randn(n,1), f2 + noise*randn(n,1), f2 + noise*randn(n,1)];
    R = corr(Xv);
    D = 1 - abs(R); D(1:p+1:end) = 0;
    Z = linkage(squareform(D), methods{i});
    lab = cluster(Z, 2);
    if mean(lab == vtruth) < mean(lab == (3 - vtruth)); lab = 3 - lab; end
    groups{i} = lab(:)';
end

rng(seeds(1));
f1 = randn(n, 1); f2 = randn(n, 1);
Xv = [f1 + noise*randn(n,1), f1 + noise*randn(n,1), f1 + noise*randn(n,1), ...
      f2 + noise*randn(n,1), f2 + noise*randn(n,1), f2 + noise*randn(n,1)];
R = corr(Xv);
up = triu(true(p), 1);                                   % 上三角成对
same = (vtruth == vtruth') & up;                         % 组内对
diffp = (vtruth ~= vtruth') & up;                        % 组间对
within  = mean(abs(R(same)));
between = mean(abs(R(diffp)));

out = struct('vtruth', vtruth, 'R', R, 'within', within, 'between', between, ...
             'acc', acc, 'groups', {groups});

fprintf('[var_cluster] variables: %d in KNOWN groups %s (2 latent factors, 3 vars each, noise=%.2f)\n', ...
        p, mat2str(vtruth'), noise);
fprintf('  mean |corr|  within-group = %.4f   between-group = %.4f\n', within, between);
fprintf('  %-9s  %-14s  %s\n', 'linkage', 'cut@2 recovery', 'recovered groups');
for i = 1:nm
    fprintf('  %-9s  %-14s  [%s]\n', methods{i}, ...
            sprintf('%.3f', acc(i)), num2str(groups{i}, '%d '));
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
