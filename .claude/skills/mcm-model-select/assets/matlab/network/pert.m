function out = pert(opts)
%PERT  Critical-path method (CPM) on an activity-on-node network.
%   Hand example: activities A..F, durations [3 2 4 2 3 5];
%   project duration = 12; slack = [0 2 0 0 0 0];
%   critical activities = A C D E F (paths A-C-D-E and A-C-F).
%
%   M4 `mcm-model-select` 骨架 · network #10（计划评审 PERT）。文件名全 ASCII（GC5）。
%   ★ 本名字**无**顶层 `@pert` 类目录撞名（实测 2026-10-04）。
%
%   独立参照（第 3 类：手算小图）：前推 ES/EF、后推 LS/LF、松弛**手算**（见 verify/pert.md）。
%
%   用法：
%     pert()             % 自检并打印读数
%     out = pert(opts)   % opts.dur · opts.pred（前驱单元格）
%
%   返回 struct：ES, EF, LS, LF, slack, duration, critical。

if nargin < 1 || isempty(opts); opts = struct(); end
dur = dflt(opts, 'dur', [3 2 4 2 3 5]);
pred = dflt(opts, 'pred', {[], [1], [1], [2 3], [4], [3]});
n = numel(dur);

ES = zeros(1, n); EF = zeros(1, n);
for i = 1:n
    if isempty(pred{i}); ES(i) = 0; else; ES(i) = max(EF(pred{i})); end
    EF(i) = ES(i) + dur(i);
end
T = max(EF);

succ = cell(1, n);
for i = 1:n
    for p = pred{i}; succ{p}(end + 1) = i; end   %#ok<AGROW>
end
LS = zeros(1, n); LF = inf(1, n);
for i = n:-1:1
    if isempty(succ{i}); LF(i) = T; else; LF(i) = min(LS(succ{i})); end
    LS(i) = LF(i) - dur(i);
end
slack = LS - ES;
critical = find(slack == 0);

out = struct('ES', ES, 'EF', EF, 'LS', LS, 'LF', LF, 'slack', slack, ...
             'duration', T, 'critical', critical);

fprintf('[pert] CPM on %d activities (A..%c), durations [%s]\n', ...
        n, char(64 + n), num2str(dur, '%g '));
fprintf('  project duration = %g\n', T);
fprintf('  ES    = [%s]\n', num2str(ES, '%g '));
fprintf('  slack = [%s]\n', num2str(slack, '%g '));
fprintf('  critical activities (slack 0): %s\n', char(64 + critical));
fprintf('  hand-computed duration = 12, slack [0 2 0 0 0 0]   =>  %s\n', ...
        ternary(T == 12 && isequal(slack, [0 2 0 0 0 0]), 'MATCH', 'MISMATCH'));
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end

function v = ternary(c, a, b)
if c; v = a; else; v = b; end
end
