function out = solve(seed)
%SOLVE  样例求解脚本：CD5 违规侧 —— 可执行语句里写死了机器绝对路径。
if nargin < 1 || isempty(seed); seed = 2025; end
rng(seed, 'twister');
data = load('D:\Projects\数学建模\build\data.mat');
out.mean = mean(data.x);
outDir = fullfile('build');
if ~exist(outDir, 'dir'); mkdir(outDir); end
writetable(table(out.mean), fullfile(outDir, 'table-1-estimate.csv'));
end
