function out = solve()
%SOLVE  样例求解脚本：用了随机性却未固定随机源（CD1 违规侧）。
x = rand(1000, 1);
out.mean = mean(x);
outDir = fullfile('build');
if ~exist(outDir, 'dir'); mkdir(outDir); end
writetable(table(out.mean), fullfile(outDir, 'table-1-estimate.csv'));
end
