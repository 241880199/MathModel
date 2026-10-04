function out = gm21_verhulst(opts)
%GM21_VERHULST  Grey Verhulst (saturated/S-curve growth) — the GM(2,1) family's saturation case.
%
%   M4 `mcm-model-select` 骨架 · prediction #2（灰色 GM(2,1) / Verhulst）。文件名全 ASCII（GC5）。
%   ★ 本骨架实现 **Verhulst（饱和/S 形）** 形态（类索引里「序列有增长上限 / S 形饱和」那一叶）；
%     GM(2,1) 的**一般二阶**形态需求解二阶微分方程（常用 Symbolic Toolbox 的 `dsolve`），
%     不在本骨架内 —— 起点素材见 `corpus/algorithms/src/GreySystem灰色系统/GM_2_1.m`（教辅级，**不作独立参照**）。
%
%   语料面（P6）：**无直接语料** —— `corpus/papers/MODEL_MAP.md` 里 `Verhulst` / `GM(2,1)` 均 **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*(Verhulst|GM\(2,1\))（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行）
%   ⇒ 标 `[社区]`（教科书级常识）。★ **素材 0 ≠ 语料 0 要分开说**：**素材面**在
%   `corpus/algorithms/src/GreySystem灰色系统/`（含 `GM_Verhulst.m`）**有**起点素材；**语料面**才是 0。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 给定**饱和序列 x1**（视作已累加的一次生成序列），令 x0(1) = x1(1)、x0(k) = x1(k) - x1(k-1)；
%     · 紧邻均值  z1(k) = 0.5 * (x1(k) + x1(k-1))；
%     · 参数估计  [a;b] = (B'B)^{-1} B'Y，B = [-z1(k), z1(k)^2]，Y = x0(k)（k = 2..n）；
%     · 白化方程  dx1/dt + a*x1 = b*x1^2 ⇒ 时间响应
%                 x1hat(k) = a*x1(1) / ( b*x1(1) + (a - b*x1(1))*exp(a*k) )，k = 0..n-1；
%     · 还原      x0hat(k) = x1hat(k) - x1hat(k-1)（x0hat(1) = x1hat(1)）。
%   ★ 逐步算式与手算期望值（含 a、b）见 `tests/skills/model-select/verify/gm21_verhulst.md`。
%
%   用法：
%     gm21_verhulst()             % 自检并打印读数（默认 = 教科书饱和序列算例）
%     out = gm21_verhulst(opts)   % opts.x1
%
%   返回 struct：x1, x0, z1, a, b, x1hat, x0hat, resid, rel, rel_mean。

if nargin < 1 || isempty(opts); opts = struct(); end
x1 = dflt(opts, 'x1', [4.93 5.33 5.87 6.35 6.63 7.15 7.37 7.39 7.81 8.35 9.39 10.59 10.94 10.44]);
x1 = x1(:).';
n = numel(x1);
assert(n >= 4, 'Verhulst 至少需要 4 个点');

x0 = [x1(1), diff(x1)];                              % 视 x1 为一次生成序列 ⇒ x0 为其差
z1 = [0, 0.5 * (x1(2:end) + x1(1:end-1))];           % z1(1) 占位（不参与估计）

B = [-z1(2:end).', z1(2:end).'.^2];                  % 数据矩阵（k = 2..n）
Y = x0(2:end).';                                     % 数据向量
ab = B \ Y;                                          % 最小二乘 [a; b]
a = ab(1); b = ab(2);

k = 0:n-1;
x1hat = a * x1(1) ./ (b * x1(1) + (a - b * x1(1)) * exp(a * k));   % 时间响应式
x0hat = [x1hat(1), diff(x1hat)];                     % 累减还原

resid = x1 - x1hat;                                  % 残差（另：对差序列也留一份）
rel = abs(resid) ./ x1;
rel_mean = mean(rel);

out = struct('x1', x1, 'x0', x0, 'z1', z1, 'a', a, 'b', b, ...
             'x1hat', x1hat, 'x0hat', x0hat, 'resid', resid, 'rel', rel, ...
             'rel_mean', rel_mean, 'n', n);

fprintf('[gm21_verhulst] n = %d，饱和序列 x1 = [%s]\n', n, num2str(x1, '%.6g '));
fprintf('  a = %.10g   b = %.10g\n', a, b);
fprintf('  x1hat = [%s]\n', num2str(x1hat, '%.8g '));
fprintf('  resid = [%s]\n', num2str(resid, '%.6g '));
fprintf('  mean rel = %.6g\n', rel_mean);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
