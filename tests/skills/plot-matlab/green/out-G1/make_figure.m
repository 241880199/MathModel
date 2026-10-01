function make_figure()
% GREEN G1 - R1 district vulnerability composition (stacked bars), produced WITH the module.
% Style comes from .claude/skills/mcm-plot-matlab/assets/mcmplot.m (addpath below);
% the script itself contains NO style numbers -- only scene data and the caller-supplied
% textwidth denominator (an attribute of the paper, per the module contract).
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(fileparts(fileparts(here)))));   % .../tests/skills/plot-matlab/green/out-G1 -> repo root
addpath(fullfile(root, '.claude', 'skills', 'mcm-plot-matlab', 'assets'));
OUT = here;

TEXTWIDTH_IN = 6.31;   % paper column width (inches) -- same value passed to the checker
DPI = 300;             % PNG export dpi -- must match the checker's --dpi

M = mcmplot();
D      = {'A','B','C','D','E','F'};
low    = [0.42 0.31 0.55 0.28 0.37 0.50];
medium = [0.35 0.44 0.30 0.47 0.38 0.33];
high   = [0.23 0.25 0.15 0.25 0.25 0.17];

fig = M.figure(TEXTWIDTH_IN);     % light theme + paper size
ax  = axes(fig);
b   = bar(ax, [low(:) medium(:) high(:)], 'stacked');
co  = M.style.series_color;       % H14 series colors, read from the module (no second source)
for k = 1:3
    b(k).FaceColor = co(k, :);
    b(k).EdgeColor = 'none';
end
set(ax, 'XTickLabel', D);
ylabel(ax, 'Share of district area (fraction)');
ylim(ax, [0 1]);
legend(ax, {'low','medium','high'}, 'Location', 'eastoutside');
M.apply(fig);                     % white bg / color order / font / H10 (box off, ticks in)
M.save(fig, fullfile(OUT, 'figure.png'), DPI);
M.save(fig, fullfile(OUT, 'figure.pdf'));
close(fig);
end
