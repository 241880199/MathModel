function out = interpolation(opts)
%INTERPOLATION  Interpolate a KNOWN function from its samples; error decreases as the grid refines.
%
%   M4 `mcm-model-select` 骨架 · prediction #9（插值 · 数据补全 / 网格化）。文件名全 ASCII（GC5）。
%   ★ **零参可跑**：本骨架自带默认函数与网格，`feval('interpolation')` 无需输入即跑完（`MS4` 隐含契约）。
%
%   语料面（P6）：**无直接语料** —— `corpus/papers/MODEL_MAP.md` 里 `interpolation` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*interpolation（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。★ **素材 0 ≠ 语料 0 要分开说**：**素材面**在
%   `corpus/algorithms/src/Interpolation（目标规划、多元分析与插值的相关例子）/`
%   （含 `interp_1D.m` / `interp_2D.m` / `interp_grid.m`）**有**起点素材；**语料面**才是 0。
%
%   独立参照（第 4 类：已知函数的采样点 —— 插值回原函数，误差随网格加密下降）：
%     · 已知 f(x) = sin(2*pi*x)，在 [0,1] 上取 n 个等距节点采样；
%     · 用 `interp1(xt, f(xt), xq, method)` 回原函数，method ∈ {linear, spline, pchip}；
%     · 在**细测试网格**上算最大绝对误差 ⇒ **误差应随 n 增大而下降**（spline/pchip 快于 linear）。
%   ★ 逐项读数（各 n × 各 method 的误差表）见 `tests/skills/model-select/verify/interpolation.md`。
%
%   用法：
%     interpolation()             % 自检并打印读数（默认 sin 函数 + 逐级加密网格）
%     out = interpolation(opts)   % opts.f opts.grids opts.ntest
%
%   返回 struct：grids, err（3 × numel(grids)，行序 {linear, spline, pchip}）。

if nargin < 1 || isempty(opts); opts = struct(); end
f     = dflt(opts, 'f',     @(x) sin(2 * pi * x));
grids = dflt(opts, 'grids', [5 9 17 33 65]);
ntest = dflt(opts, 'ntest', 4001);
methods = {'linear', 'spline', 'pchip'};
xf = linspace(0, 1, ntest);
yf = f(xf);

err = zeros(numel(methods), numel(grids));
for gi = 1:numel(grids)
    xt = linspace(0, 1, grids(gi));
    yt = f(xt);
    for mi = 1:numel(methods)
        yq = interp1(xt, yt, xf, methods{mi});
        err(mi, gi) = max(abs(yq - yf));
    end
end

out = struct('grids', grids, 'err', err, 'methods', {methods}, 'ntest', ntest);

fprintf('[interpolation] f(x) = sin(2*pi*x)，测试点 %d 个\n', ntest);
fprintf('  %-8s', 'n');
for gi = 1:numel(grids); fprintf('%12d', grids(gi)); end
fprintf('\n');
for mi = 1:numel(methods)
    fprintf('  %-8s', methods{mi});
    for gi = 1:numel(grids); fprintf('%12.4g', err(mi, gi)); end
    fprintf('\n');
end
for mi = 1:numel(methods)
    fprintf('  %-8s 误差随 n 单调不增 : %s\n', methods{mi}, bool2str(all(diff(err(mi, :)) <= 0)));
end
end

function s = bool2str(tf)
if tf; s = '是'; else; s = '否'; end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
