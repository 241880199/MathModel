function out = solve(seed)
%SOLVE  样例求解脚本：只打印不落盘（CD2 违规侧）。
if nargin < 1 || isempty(seed); seed = 2025; end
rng(seed, 'twister');
x = rand(1000, 1);
out.mean = mean(x);
disp(out.mean);
end
