function out = scaffold(opts)
%SCAFFOLD  mcm-code 最小可复现骨架（MATLAB · 零参可跑）。
%
%   ★ 三件事一次演示（本 skill 的可复现规范）：
%     (1) 固定随机源 —— 入口即 `rng(<固定种子>, 'twister')`，同样输入必得同样结果；
%     (2) 结果落盘   —— 用 `writetable` / `save` 把结果写到磁盘（**不是只 `disp`**）；
%     (3) 编号对齐   —— **进正文的成品**文件名带论文编号（`table-1-*` / `figure-1-*`），与正文 表 1 / 图 1 对得上。
%
%   用法（**零参可跑**）：
%     scaffold                 % 用默认参数跑一遍，产物落 build/mcm-code-scaffold/matlab/
%     out = scaffold(struct('outDir', fullfile('build','my-run'), 'nSamples', 1e5, 'seed', 2026))
%
%   ★ 不写死机器绝对路径：默认输出目录是**相对**路径（`build/...`，已入 .gitignore），可经 opts.outDir 改。
%   ★ 本骨架**不给算法** —— 例中的蒙特卡洛估 π 只是"可跑的最小例子"，整体替换为你的模型即可。
%   ★ 成品与工作转储**分目录**：带编号的成品（`table-1-*` / `figure-1-*`）落 outDir；**不进正文**的工作转储
%     （`workspace-dump.mat`）落 `outDir/work/` —— 即 `references/numbering.md`「中间产物可以不带编号，
%     但别与带编号的成品混在同一目录」的落地。
%
%   返回 struct：outDir, seed, piHat, ci95, files（落盘的三个文件路径）。

if nargin < 1 || isempty(opts); opts = struct(); end
seed     = dflt(opts, 'seed',     2025);                            % ★ (1) 固定随机源
nSamples = dflt(opts, 'nSamples', 20000);
outDir   = dflt(opts, 'outDir',   fullfile('build', 'mcm-code-scaffold', 'matlab'));
workDir  = fullfile(outDir, 'work');                                % ★ 工作转储单独落，不混成品

rng(seed, 'twister');                                              % ★ (1) 入口即固定种子

% —— 可跑的最小例子：用蒙特卡洛估 π（可整体替换为你的模型）——
x        = rand(nSamples, 1);
y        = rand(nSamples, 1);
inCircle = (x.^2 + y.^2) <= 1;
p        = mean(inCircle);
piHat    = 4 * p;

% 95% 置信区间（正态近似）
se   = 4 * sqrt(p * (1 - p) / nSamples);
ci95 = [piHat - 1.96 * se, piHat + 1.96 * se];

% —— (2) 结果落盘 + (3) 文件名带编号 ——
if ~exist(outDir, 'dir'); mkdir(outDir); end
if ~exist(workDir, 'dir'); mkdir(workDir); end

% 表 1 的结果 -> table-1-estimate.csv（对应正文 表 1）
T = table(piHat, ci95(1), ci95(2), nSamples, seed, ...
          'VariableNames', {'pi_hat', 'ci95_lo', 'ci95_hi', 'n_samples', 'seed'});
tableFile = fullfile(outDir, 'table-1-estimate.csv');              % ★ (3) table-1 ↔ 正文 表 1
writetable(T, tableFile);                                          % ★ (2) 落盘

% 图 1 的原始数据 -> figure-1-samples.csv（对应正文 图 1）
sampleFile = fullfile(outDir, 'figure-1-samples.csv');             % ★ (3) figure-1 ↔ 正文 图 1
writetable(table(x, y, inCircle), sampleFile);                     % ★ (2) 落盘

% 整包工作变量 -> work/workspace-dump.mat（`save` 之一例）
% 不进正文的工作转储：不带编号、另置 work/，别与带编号的成品混放（见 references/numbering.md）
matFile = fullfile(workDir, 'workspace-dump.mat');                 % ★ (2) save
save(matFile, 'piHat', 'ci95', 'nSamples', 'seed');

out = struct('outDir', outDir, 'seed', seed, 'piHat', piHat, 'ci95', ci95, ...
             'files', {{tableFile, sampleFile, matFile}});

fprintf('[scaffold] (1) 固定随机源 seed = %d\n', seed);
fprintf('[scaffold] (2) 结果落盘 -> %s\n', outDir);
fprintf('[scaffold] (3) 编号对齐：table-1-estimate.csv / figure-1-samples.csv\n');
fprintf('[scaffold]     不进正文的工作转储 -> %s\n', matFile);
fprintf('[scaffold] pi_hat = %.6f  (95%% CI %.6f, %.6f)\n', piHat, ci95(1), ci95(2));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
