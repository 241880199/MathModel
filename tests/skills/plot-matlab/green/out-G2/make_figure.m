function make_figure()
% GREEN G2 - R2 drivers of historical disaster counts, produced WITH the module.
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(fileparts(fileparts(here)))));
addpath(fullfile(root, '.claude', 'skills', 'mcm-plot-matlab', 'assets'));
OUT = here;

TEXTWIDTH_IN = 6.31;
DPI = 300;

M = mcmplot();

% scene data (verbatim from the brief table)
popdensity = [820 640 610 1210 990 1750];
slope      = [3.2 11.5 2.4 14.8 7.1 5.0];
vegcover   = [0.61 0.58 0.72 0.41 0.49 0.55];
count      = [12 31 8 38 16 24];
infra      = [74 72 81 55 66 70];

preds  = {'Population density', 'Mean slope', 'Vegetation cover', 'Infrastructure index'};
P      = [popdensity(:) slope(:) vegcover(:) infra(:)];
r      = zeros(1, size(P, 2));
for j = 1:size(P, 2)
    c = corrcoef(P(:, j), count);
    r(j) = c(1, 2);
end
[~, ord] = sort(abs(r), 'descend');

fig = M.figure(TEXTWIDTH_IN);
ax  = axes(fig);
b   = bar(ax, r(ord));
b.FaceColor = M.style.series_color(1, :);
b.EdgeColor = 'none';
set(ax, 'XTickLabel', preds(ord));
xtickangle(ax, 20);               % 看图层修图：四个类目名默认平排会互相压住（读不出哪根是哪根）
ylabel(ax, 'Pearson r (dimensionless)');
ylim(ax, [-1 1]);
yline(ax, 0, 'Color', [0 0 0]);
M.apply(fig);
M.save(fig, fullfile(OUT, 'figure.png'), DPI);
M.save(fig, fullfile(OUT, 'figure.pdf'));
close(fig);
end
