function out = cellular_automata(opts)
%CELLULAR_AUTOMATA  Conway Game of Life (B3/S23, torus); standard patterns: blinker period = 2, glider period = 4.
%
%   M4 `mcm-model-select` 骨架 · simulation #1（元胞自动机 · 9 种规则族）。文件名全 ASCII（GC5）。
%   规则（B3/S23）：活细胞邻居 = 2 或 3 ⇒ 存活；死细胞邻居 = 3 ⇒ 出生；否则死亡（环面）。
%
%   语料面（P5 · P6）：`[社区]` —— `cellular automata` 在 `corpus/papers/MODEL_MAP.md` **0 命中**
%   （2026-10-04 当场复跑 `grep -nE "^ +- .*cellular automata（[0-9]+ 篇）" corpus/papers/MODEL_MAP.md` ⇒ 0 行；
%   ★ 正对照：同形态 `genetic algorithm` ⇒ 3 行，证明命令没写错）。同文件 `cellular` / `automata` / `元胞` 亦 0。
%   **算法素材面（有，起点素材）**：`corpus/algorithms/src/CellularAutomata元胞向量机/`（9 个规则子目录 · 11 件 .m，
%   含 `corpus/algorithms/src/CellularAutomata元胞向量机/生命游戏/game_of_life.m`）—— 教辅级**起点素材**，**不作独立参照**。
%
%   独立参照：★★ **人工兜底（设计 §4.1）** —— 元胞自动机无闭式解、输出是全局演化、无 ground truth。
%     ① **已知规则的标准图案**：Conway 生命游戏的 **blinker 周期 = 2**（三连直线 <-> 三连竖线）、
%        **glider 周期 = 4**（4 步后回到**位移 (+1,+1)** 的自身）；
%     ② **手算第 1 步**（blinker：水平三连 → 竖直三连，逐格可推）。
%   ★ **本项参照是人工兜底、不是"已验证"**（`MS3` 判不到"独立性"那一层；算式与读数见 verify 记录）。
%
%   用法：
%     cellular_automata()             % 自检并打印两个标准图案的周期
%     out = cellular_automata(opts)   % opts.maxsteps
%
%   返回 struct：blinker_grid, blinker_period, blinker_shift, blinker_step1,
%                glider_grid, glider_period, glider_shift, maxsteps。

if nargin < 1 || isempty(opts); opts = struct(); end
maxsteps = dflt(opts, 'maxsteps', 12);

% --- blinker：5x5 网格中央一条水平三连直线（期望周期 2）---
blinker_grid = zeros(5, 5); blinker_grid(3, 2:4) = 1;
blinker_step1 = gol_step(blinker_grid);                                   % 手算：竖直三连
[blinker_period, blinker_shift] = pattern_period(blinker_grid, maxsteps);

% --- glider：30x30 网格（远离边界），经典 glider（期望周期 4）---
glider_grid = zeros(30, 30);
glider_grid(10, 11)     = 1;    %  . O .
glider_grid(11, 12)     = 1;    %  . . O
glider_grid(12, 10:12)  = 1;    %  O O O
[glider_period, glider_shift] = pattern_period(glider_grid, maxsteps);

out = struct('blinker_grid', blinker_grid, 'blinker_period', blinker_period, ...
             'blinker_shift', blinker_shift, 'blinker_step1', blinker_step1, ...
             'glider_grid', glider_grid, 'glider_period', glider_period, ...
             'glider_shift', glider_shift, 'maxsteps', maxsteps);

fprintf('[cellular_automata] Conway Game of Life (B3/S23, torus)\n');
fprintf('  blinker: period = %d   (shift = [%d %d])   "three-in-a-line" <-> vertical\n', ...
        blinker_period, blinker_shift(1), blinker_shift(2));
fprintf('  glider : period = %d   (shift = [%d %d] per cycle)\n', ...
        glider_period, glider_shift(1), glider_shift(2));
end

% ------------------------------------------------------------------ 局部函数
function g2 = gol_step(g)
% 一步 B3/S23（**环面**：邻居用 circshift 环绕）
n = zeros(size(g));
for dr = -1:1
    for dc = -1:1
        if dr == 0 && dc == 0; continue; end
        n = n + circshift(g, [dr dc]);
    end
end
g2 = double((g == 1 & (n == 2 | n == 3)) | (g == 0 & n == 3));
end

function [p, shift] = pattern_period(grid, maxsteps)
% 求**平移周期**：最小的 p > 0，使 live(t+p) == live(t) + 常数位移（对所有 t 一致）。
subs = cell(maxsteps + 1, 1);
g = grid;
for t = 0:maxsteps
    [r, c] = find(g);
    subs{t + 1} = [r, c];
    g = gol_step(g);
end
p = NaN; shift = [0 0];
for pp = 1:maxsteps
    dr = NaN; dc = NaN; ok = true;
    for t = 0:maxsteps - pp
        a = subs{t + 1}; b = subs{t + pp + 1};
        if size(a, 1) ~= size(b, 1); ok = false; break; end
        if isempty(a); continue; end                 % 全空 ↔ 全空：位移取 [0 0]
        d = b - a;                                   % find 按列主序 ⇒ 纯平移时 d 恒定
        if any(d(:, 1) ~= d(1, 1)) || any(d(:, 2) ~= d(1, 2)); ok = false; break; end
        if isnan(dr); dr = d(1, 1); dc = d(1, 2);
        elseif d(1, 1) ~= dr || d(1, 2) ~= dc; ok = false; break; end
    end
    if ok; p = pp; shift = [dr dc]; return; end
end
end

function v = dflt(s, f, d)
if isfield(s, f) && ~isempty(s.(f)); v = s.(f); else; v = d; end
end
