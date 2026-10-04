function out = solve(seed)
%SOLVE  样例求解脚本：入口固定随机源（MATLAB）。
% 本样例演示 CD1 的合规侧：入口一处显式 rng(...)。
if nargin < 1 || isempty(seed); seed = 2025; end
rng(seed, 'twister');
x = rand(1000, 1);
out.mean = mean(x);
outDir = fullfile('build');
if ~exist(outDir, 'dir'); mkdir(outDir); end
writetable(table(out.mean), fullfile(outDir, 'table-1-estimate.csv'));
end
