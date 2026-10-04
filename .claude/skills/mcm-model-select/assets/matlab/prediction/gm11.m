function out = gm11(opts)
%GM11  Grey prediction GM(1,1): 1-AGO, least-squares parameter estimation, restore.
%
%   M4 `mcm-model-select` 骨架 · prediction #1（灰色预测 GM(1,1)）。文件名全 ASCII（GC5）。
%
%   语料面（P6）：**带语料指针** —— `corpus/papers/MODEL_MAP.md` 里 `grey prediction` 命中 **1 篇**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*grey prediction（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 1 行：P2025-C-11）。
%   ★ 小样本的灰色方法在**素材面**另有起点素材：`corpus/algorithms/src/GreySystem灰色系统/`
%     （含 `GM_1_1.m` / `GM_1_1_full_procession.m` / `GM_full.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照（第 3 类：手算标准算例 —— 期望值写死在参照件里、并给出算式）：
%     · 一次累加   x1(k) = sum_{i<=k} x0(i)；
%     · 紧邻均值   z1(k) = 0.5 * (x1(k) + x1(k-1))，k = 2..n；
%     · 参数估计   [a;b] = (B'B)^{-1} B'Y，B = [-z1(k), 1]，Y = x0(k)（k = 2..n）；
%     · 时间响应   x1hat(k+1) = (x0(1) - b/a) * exp(-a*k) + b/a，k = 0..n；
%     · 还原       x0hat(k)   = x1hat(k) - x1hat(k-1)。
%   ★ 逐步算式与手算期望值（含 a、b 与复原序列）见 `tests/skills/model-select/verify/gm11.md`。
%
%   用法：
%     gm11()             % 自检并打印读数（默认 = 教科书标准算例）
%     out = gm11(opts)   % opts.x0
%
%   返回 struct：x0, x1, z1, a, b, x1hat, x0hat, resid, rel, C, P, pass。

if nargin < 1 || isempty(opts); opts = struct(); end
x0 = dflt(opts, 'x0', [2.874, 3.278, 3.337, 3.390, 3.679]);   % 教科书标准算例
x0 = x0(:).';
n = numel(x0);
assert(n >= 4, 'GM(1,1) 至少需要 4 个点');

x1 = cumsum(x0);                                  % 一次累加生成（1-AGO）
z1 = 0.5 * (x1(2:end) + x1(1:end-1));             % 紧邻均值生成序列（k = 2..n）

B = [-z1(:), ones(n-1, 1)];                       % 数据矩阵
Y = x0(2:end).';                                  % 数据向量
ab = B \ Y;                                       % 最小二乘 [a; b]
a = ab(1); b = ab(2);

k = 0:n;
x1hat = (x0(1) - b/a) * exp(-a*k) + b/a;          % 时间响应式（k = 0..n）
x0hat = [x1hat(1), diff(x1hat)];                  % 累减还原（长度 n+1；末项 = 一步预测）

resid = x0 - x0hat(1:n);                          % 残差（只对观测期）
rel = abs(resid) ./ x0;                           % 相对误差

% --- 后验差检验（精度等级）---
S1 = std(x0, 1);                                  % 原始序列（总体）标准差
S2 = std(resid, 1);                               % 残差（总体）标准差
C = S2 / S1;                                      % 后验差比
P = mean(abs(resid - mean(resid)) < 0.6745 * S1); % 小误差概率
pass_C = C < 0.5;                                 % 一级（好）判据（社区常用阈值）
pass = pass_C;

out = struct('x0', x0, 'x1', x1, 'z1', z1, 'a', a, 'b', b, ...
             'x1hat', x1hat, 'x0hat', x0hat, 'resid', resid, 'rel', rel, ...
             'S1', S1, 'S2', S2, 'C', C, 'P', P, 'pass', pass, 'n', n);

fprintf('[gm11] n = %d，x0 = [%s]\n', n, num2str(x0, '%.6g '));
fprintf('  a = %.10g   b = %.10g\n', a, b);
fprintf('  x1hat = [%s]\n', num2str(x1hat, '%.8g '));
fprintf('  x0hat = [%s]\n', num2str(x0hat, '%.8g '));
fprintf('  resid = [%s]\n', num2str(resid, '%.8g '));
fprintf('  rel   = [%s]  (max = %.4g)\n', num2str(rel, '%.4g '), max(rel));
fprintf('  S1 = %.8g   S2 = %.8g   C = %.8g   P = %.4g\n', S1, S2, C, P);
if pass; v = '一级（C < 0.5）'; else; v = '未达一级'; end
fprintf('  后验差检验 C = S2/S1 : %s\n', v);
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
