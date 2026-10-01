function make_figure()
% GREEN G3 - R3 district vulnerability composition, paper-ready (horizontal stacked bars).
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(fileparts(fileparts(here)))));
addpath(fullfile(root, '.claude', 'skills', 'mcm-plot-matlab', 'assets'));
OUT = here;

TEXTWIDTH_IN = 6.31;
DPI = 300;

M = mcmplot();
D      = {'A','B','C','D','E','F'};
low    = [0.42 0.31 0.55 0.28 0.37 0.50];
medium = [0.35 0.44 0.30 0.47 0.38 0.33];
high   = [0.23 0.25 0.15 0.25 0.25 0.17];

fig = M.figure(TEXTWIDTH_IN);
ax  = axes(fig);
b   = barh(ax, [low(:) medium(:) high(:)], 'stacked');
co  = M.style.series_color;
for k = 1:3
    b(k).FaceColor = co(k, :);
    b(k).EdgeColor = 'none';
end
set(ax, 'YTickLabel', D);
xlabel(ax, 'Share of district area (fraction)');
xlim(ax, [0 1]);
legend(ax, {'low','medium','high'}, 'Location', 'southoutside', 'Orientation', 'horizontal');
M.apply(fig);
M.save(fig, fullfile(OUT, 'figure.png'), DPI);
M.save(fig, fullfile(OUT, 'figure.pdf'));
close(fig);
end
