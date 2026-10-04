function out = solve(seed)
%SOLVE  样例求解脚本：CD5 合规侧 —— 绝对路径只出现在注释里。
% 说明（注释，不算违规）：本机曾用路径 C:\Users\alice\mcm\data.mat，现已改为相对路径。
if nargin < 1 || isempty(seed); seed = 2025; end
rng(seed, 'twister');
x = rand(1000, 1);
out.mean = mean(x);
outDir = fullfile('build');
if ~exist(outDir, 'dir'); mkdir(outDir); end
writetable(table(out.mean), fullfile(outDir, 'table-1-estimate.csv'));
end
