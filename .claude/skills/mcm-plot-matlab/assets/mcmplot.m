function M = mcmplot()
%MCMPLOT  MCM 论文图的 MATLAB 薄封装（图幅 + 浅色主题 + 色序 + H10 + 导出）。
%
%  ★ 本文件是**派生件**：下面两处 `BEGIN/END GENERATED` 之间的内容由
%    tests/skills/plot-matlab/gen-mcm-style-matlab.py 从
%    .claude/skills/mcm-figure-choose/assets/mcm-style.json **重放**产出 —— **勿手改**。
%    要改样式值请改那张表（或其上游规范），再重放。
%
%  规范正文（图通常长什么样、每条规则的数值与验证状态）只在
%    .claude/skills/mcm-figure-choose/references/house-style.md —— 本文件**不重述**它。
%
%  用法：
%      M   = mcmplot();
%      fig = M.figure(6.31);        % 6.31 = 正文栏宽(in)，**由调用方给**（它是论文的属性）
%      ax  = axes(fig); plot(ax, x, y, 'LineWidth', M.style.line_width);
%      xlabel(ax, 'Slope (deg)');   % ← 轴标签带单位 = 调用方纪律（见下"已知缺口"）
%      M.apply(fig);                % 上 house style（浅色主题 / 白底 / 色序 / 框线刻度 / 字体）
%      M.save(fig, 'out.png', 300); % 导出（print 家族；dpi 须与判据侧的 --dpi 一致）
%      M.save(fig, 'out.pdf');      % PDF 走 PaperSize，不需要 dpi
%
%  ---- 浅色主题：**两种可用写法**（MATLAB 出厂主题是深色，必须显式上浅色）----
%    (a) 建 figure 时给：`figure('Theme','light', ...)`   ← `M.figure()` 用的就是它；
%    (b) 已有 figure 上改：`theme(fig, 'light')`          ← **必须带 figure 句柄**。
%  ⚠️ 别写 `theme('light')`（**不带句柄**）：本仓产物级实测它是**静默空操作** —— 调用 `ok=1`，
%     而 `defaultFigureColor` 仍是深色、新图仍是深色（实测新图里 84.8% 的近深像素未变）。
%     这就是"看起来设上了、实际没设"的那一类，**不许**出现在交付脚本里。
%  ⚠️ 主题翻转的触发点是"axes 内容**第一次真正渲染**"（本仓逐步隔离实测：建 figure 不翻、
%     `axes()` 单独不翻、`axes+plot+drawnow` 才翻）⇒ 别在"建 figure 之后、画图之前"去判断主题。
%
%  ---- 导出：走 `print` 家族（本模块的**权威交付载体**）----
%    `print(fig, path, '-dpng', '-r<dpi>')` **跟 `PaperPosition`**；
%    `print(fig, path, '-dpdf')` **跟 `PaperSize`** —— 两条口径**分别设**（本封装两条都设成同一图幅）。
%  ⚠️ `exportgraphics` **不作权威交付**：它的宽是**轴内容包围盒**的函数（本仓实测 F1 0.861 / 0.865，
%     出处见设计件 `docs/superpowers/specs/2026-10-01-m3-plot-matlab-design.md` §0.1，原始读数在
%     `tests/m3-matlab-recon/out-size-law.txt`；`print` 家族按构造 1.000 / 1.001）⇒ 只在需要
%     "按内容裁"时用它，且证据里要写明用的是哪条口径。
%
%  ---- 已知缺口（不许藏；**不声称穷尽**：只列本次实现时量到的那几条）----
%    · **跨版本 / 跨机未验**：本文件只在 R2025b Update 5 上验过。
%    · **点名的字体找不到就静默回退**：MATLAB 遇到不存在的字体名**不报错**、属性还回声，产物里
%      换成别的字体 ⇒ "点上了"只能由**产物内嵌字体**证明（判据读产物，不读属性）。
%    · **字体族的取值**：MATLAB 侧无入库字体，本封装从表里的候选族**取本机可用的第一档**
%      （与 python 侧 matplotlib 的 font.serif 回退链同型）；一档都不在时退回表里最后一档。
%    · **线宽**是**逐对象**属性（`plot(...,'LineWidth',v)`），没有 rcParam 式的全局开关；
%      本封装只把值放在 `M.style.line_width`，不替你套到每条线上。
%    · **字号**同理：`M.fontsize(body_pt)` 只给"允许带"，落到哪个绝对 pt 由调用方按论文正文定。
%    · **H10 的"轴标签带单位"**是**调用方纪律**：MATLAB 侧**无设置项**（见生成的 H10 区那条注释）。

% >>> BEGIN GENERATED: STYLE（gen-mcm-style-matlab.py 重放，勿手改）>>>
% 唯一样式来源：.claude/skills/mcm-figure-choose/assets/mcm-style.json（由生成器**按 id 逐条锚定**重放）。
% 下列 id **不声称穷尽**：只列本模块读到的那些行；表里别的行本模块不消费。
STYLE.width_ratio_min = 0.8;                % h1.width_ratio.min · status=same-value
STYLE.width_ratio_max = 1.2;                % h1.width_ratio.max · status=same-value
STYLE.width_ratio_default_hi = 1.0;         % h1.width_ratio.default_hi · status=same-value
% h1.width_ratio.default_lo      status=same-value  （本模块不落活常量）
STYLE.height_in = 2.6;                      % h3.height_in · status=same-value
STYLE.max_main_colors = 4;                  % h4.max_main_colors · status=not-landable
STYLE.font_scale_lo = 0.8;                  % h12.font_scale_lo · status=not-landable
STYLE.font_scale_hi = 1.0;                  % h12.font_scale_hi · status=not-landable
STYLE.font_min_pt = 7;                      % h12.font_min_pt · status=not-landable
STYLE.line_width = 1.0;                     % lines.linewidth · status=same-value
STYLE.bg = [255 255 255]/255;               % bg · status=same-value
STYLE.series_color = [[230 159 0]; [86 180 233]; [0 158 115]; [204 121 167]; [0 114 178]; [213 94 0]; [117 112 179]; [77 77 77]]/255; % series.color · status=same-value
% font.family                    status=family-equivalent  （本模块不落活常量）
STYLE.font_serif = {'TeXGyreTermesX', 'Times New Roman'}; % font.serif · status=family-equivalent
% h10.axes_box                   status=not-landable  （本模块不落活常量）
%
% ---- status=not-landable 的行（**不静默跳过**：下面逐行给『为何落不了地』，原句取自表）----
% [h4.max_main_colors] status=not-landable
%     **数值判据，无设置项**：同上；F2 本就按像素占比数色、不数系列（只数占比 ≥0.5% 的颜色 ⇐ check-figure-style.py）—— 实测 MATLAB 侧同一张 7 系列默认图读 3（png）/ 0（pdf）（⇐ out-checks-figure-style.txt 的 `C default-N7` 段），更无『主色数上限』设置
% [h12.font_scale_lo] status=not-landable
%     **数值判据，无设置项**：同上；MATLAB 侧可设绝对 `FontSize`，但判据是比值/下限、无对应设置；且 H12 **无机械判据**（⇐ task-m3-matlab-recon-report.md『H12 落不了地』）
% [h12.font_scale_hi] status=not-landable
%     **数值判据，无设置项**：同上；MATLAB 侧可设绝对 `FontSize`，但无『倍数』设置项；且 H12 无机械判据（⇐ task-m3-matlab-recon-report.md）
% [h12.font_min_pt] status=not-landable
%     **数值判据，无设置项**：同上；无对应设置项；且 H12 无机械判据（⇐ task-m3-matlab-recon-report.md）
% [h10.axes_box] status=not-landable
%     **今天无产物级实测**：侦察记录 MATLAB 侧有对应 API（`box(ax,'off')` 去框线 / `set(ax,'TickDir','in')` 刻度朝内 —— 两者都在 K3 采样行里出现过），但**产物端零回读**：侦察判定为「**能设、不能验**」（`box off` / `TickDir 'in'` 可设，**三支机器都没有 spine/tick 判据** ⇐ `.superpowers/sdd/task-m3-matlab-recon-report.md` §G19 /「落不了地」表）⇒ 如实记 `not-landable`，不编造落地方式。
% <<< END GENERATED: STYLE <<<

M = struct();
M.style    = STYLE;
M.figure   = @(tw_in)   new_figure(tw_in, STYLE);
M.apply    = @(fig)     apply_style(fig, STYLE);
M.size     = @(tw_in)   figsize_for(tw_in, STYLE);
M.fontsize = @(body_pt) fontsize_for(body_pt, STYLE);
M.save     = @(fig, path, varargin) save_fig(fig, path, varargin{:}, STYLE);
end


function wh = figsize_for(tw_in, S)
%FIGSIZE_FOR  正文栏宽(in) -> [宽 高](in)。宽 = 栏宽 × H1 的**默认档上限**；高 = H3 的图高量级。
%  两个乘数都取自 S（由生成器从表重放），此处不写死。
wh = [tw_in * S.width_ratio_default_hi, S.height_in];
end


function band = fontsize_for(body_pt, S)
%FONTSIZE_FOR  正文 pt -> 图内字号的**允许带** [下限 上限](pt)。
%  H12：图内字号 = 正文的 [lo, hi] 倍，且不低于 min_pt。body_pt 是论文的属性，由调用方传。
band = [max(body_pt * S.font_scale_lo, S.font_min_pt), ...
        max(body_pt * S.font_scale_hi, S.font_min_pt)];
end


function fig = new_figure(tw_in, S)
%NEW_FIGURE  建一张**浅色主题**的 figure，并把图幅钉进 PaperPosition / PaperSize。
wh = figsize_for(tw_in, S);
fig = figure('Visible', 'on', 'Color', S.bg, 'Theme', 'light');   % ← (a) 建时上浅色主题
set(fig, 'Units', 'inches', 'Position', [1 1 wh(1) wh(2)]);
set(fig, 'PaperUnits', 'inches', 'PaperPositionMode', 'manual', ...
         'PaperPosition', [0 0 wh(1) wh(2)], 'PaperSize', [wh(1) wh(2)]);
end


function apply_style(fig, S)
%APPLY_STYLE  给 fig（及其下每个 axes）上 house style：白底 / 色序 / 字体 / H10。
set(fig, 'Color', S.bg);
axs = findall(fig, 'Type', 'axes');
for k = 1:numel(axs)
    ax = axs(k);
    set(ax, 'Color', S.bg, 'XColor', 'k', 'YColor', 'k');
    set(ax, 'ColorOrder', S.series_color);
    set(ax, 'FontName', pick_font(S));
% >>> BEGIN GENERATED: H10（gen-mcm-style-matlab.py 重放，勿手改）>>>
% 表 status（今天）= 'not-landable'；Task 1 产物级实测 = landed（顶内 0 / 右内 0 / 下外 0（落地态） vs 顶内 2900 / 右内 2337 / 下外 336（对照态））。
% ⇒ 按**实测**把这些行落进产物；表 status 的同步（not-landable → 实测口径）归 Task 2。
box(ax, 'off');                        % H10: 去上/右边框线（MATLAB 的 box 一并管顶与右）
% H10: 右框线同上（MATLAB 无单独关右框线的设置项，由 box off 一并管）
set(ax, 'TickDir', 'in');              % H10: 刻度朝内
set(ax, 'XMinorTick', 'off', 'YMinorTick', 'off');   % H10: 只留主刻度
% H10: 轴标签带单位 = **调用方纪律**（MATLAB 侧**无设置项**）：写 xlabel/ylabel 时把单位写进去
% <<< END GENERATED: H10 <<<
end
end


function name = pick_font(S)
%PICK_FONT  从表里的候选族取**本机可用的第一档**；一档都不在则退回最后一档。
%  与 python 侧 matplotlib 的 font.serif 回退链同型（取"本机可用的 Times 系实现"）。
avail = listfonts;
name = S.font_serif{numel(S.font_serif)};
for k = 1:numel(S.font_serif)
    if any(strcmpi(avail, S.font_serif{k}))
        name = S.font_serif{k};
        return;
    end
end
end


function save_fig(fig, path, varargin)
%SAVE_FIG  按扩展名走 print 家族：PNG 跟 PaperPosition、PDF 跟 PaperSize（两条在 new_figure 里同幅）。
%  参数：`save_fig(fig, path, [dpi], S)` —— dpi 只对 PNG 有意义，缺省取 300；PDF 不需要它。
S = varargin{end};                                    %#ok<NASGU>（保留 S 便于日后按载体分派）
dpi = 300;
if numel(varargin) >= 2
    dpi = varargin{1};
end
[~, ~, ext] = fileparts(path);
switch lower(ext)
    case '.png'
        print(fig, path, '-dpng', sprintf('-r%d', dpi));
    case '.pdf'
        print(fig, path, '-dpdf');
    otherwise
        error('mcmplot:ext', 'save() 只支持 .png / .pdf，收到 %s', ext);
end
end
