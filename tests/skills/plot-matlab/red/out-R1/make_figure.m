%% make_figure.m - District vulnerability composition (brief R1)
%
% Regenerates Figure 1 from the fixed table of district vulnerability shares.
% Deterministic, offline, headless: no network access, no randomness, no
% manual steps. Run with, e.g.:
%
%     matlab -batch "cd('<out-R1>'); make_figure"
%
% Outputs (written next to this script):
%     figure.png   - raster export, 300 dpi, white background
%     figure.pdf   - vector export, white background
%
% The data are one row per district; within every district the three tier
% shares (low, medium, high) sum to 1.00, so a 100% stacked bar chart is the
% natural encoding: bar height is constant and the segments show composition.

clear; close all; clc;

%% ---------------------------------------------------------------- data ----
% Fixed input table (brief R1). Rows = districts A..F, columns = low/med/high.
districts = {'A', 'B', 'C', 'D', 'E', 'F'};
tiers     = {'Low', 'Medium', 'High'};

share = [0.42, 0.35, 0.23; ...
         0.31, 0.44, 0.25; ...
         0.55, 0.30, 0.15; ...
         0.28, 0.47, 0.25; ...
         0.37, 0.38, 0.25; ...
         0.50, 0.33, 0.17];

% Guard the invariant the chart relies on: each district sums to 1.00.
assert(isequal(size(share), [numel(districts), numel(tiers)]), ...
       'share must be numDistricts x numTiers.');
assert(all(abs(sum(share, 2) - 1) < 1e-12), ...
       'Every district row must sum to 1.00.');

%% ------------------------------------------------------------- closest ----
% Distance between district profiles: L1 (sum of absolute share differences).
% Used only to annotate the closest pair; the figure shows the profiles, the
% number is recomputed here so the annotation cannot drift from the data.
nD = numel(districts);
l1 = zeros(nD);
for i = 1:nD
    for j = (i + 1):nD
        l1(i, j) = sum(abs(share(i, :) - share(j, :)));
        l1(j, i) = l1(i, j);
    end
end
l1(l1 == 0) = Inf;
[minD, idx] = min(l1(:));
[pi, pj] = ind2sub(size(l1), idx);
if pi > pj          % report the pair in table order (A before F)
    tmp = pi; pi = pj; pj = tmp;
end
pairLabel = sprintf('most similar pair: %s & %s (L_1 = %.2f)', ...
                    districts{pi}, districts{pj}, minD);

%% ------------------------------------------------------------ styling ----
% Ordinal palette (low -> high severity): light blue, amber, red.
tierColors = [0.62 0.79 0.88; ...
              0.99 0.75 0.35; ...
              0.79 0.19 0.19];

set(groot, 'defaultAxesFontName',   'Times New Roman', ...
           'defaultTextFontName',   'Times New Roman', ...
           'defaultLegendFontName', 'Times New Roman');

figW = 14.0;  % cm
figH = 8.5;   % cm

fig = figure('Units', 'centimeters', ...
             'Position', [2, 2, figW, figH], ...
             'Color', 'w', ...
             'Visible', 'off', ...          % safe for headless runs
             'PaperUnits', 'centimeters', ...
             'PaperPosition', [0, 0, figW, figH]);

ax = axes('Parent', fig);
hold(ax, 'on');

% Pin the light palette explicitly: the figure must not inherit an IDE/figure
% theme (e.g. a dark MATLAB theme), and must export on a white background.
set(ax, 'Color', 'w');

%% --------------------------------------------------------------- bars ----
b = bar(ax, share, 'stacked', 'BarWidth', 0.68, ...
        'EdgeColor', 'w', 'LineWidth', 0.5);
for k = 1:numel(tiers)
    b(k).FaceColor = tierColors(k, :);
end

% Value labels centred in each segment.
cum = [zeros(nD, 1), cumsum(share, 2)];
for k = 1:numel(tiers)
    yMid = (cum(:, k) + cum(:, k + 1)) / 2;
    for i = 1:nD
        lum = 0.2126 * tierColors(k, 1) + ...
              0.7152 * tierColors(k, 2) + ...
              0.0722 * tierColors(k, 3);
        if lum > 0.6
            txtCol = [0.10 0.10 0.10];
        else
            txtCol = [1 1 1];
        end
        text(ax, b(k).XEndPoints(i), yMid(i), sprintf('%.2f', share(i, k)), ...
             'HorizontalAlignment', 'center', ...
             'VerticalAlignment', 'middle', ...
             'FontName', 'Times New Roman', 'FontSize', 8, 'Color', txtCol);
    end
end

%% --------------------------------------------- similarity annotation ----
% Headroom above 1.0 carries a bracket joining the two closest profiles, so
% the judgement is visible in the figure itself.
ylim(ax, [0, 1.14]);
bracketY = 1.045;
capY     = 1.020;
plot(ax, [pi, pi], [capY, bracketY], '-', 'Color', [0.35 0.35 0.35], ...
     'LineWidth', 0.6);
plot(ax, [pj, pj], [capY, bracketY], '-', 'Color', [0.35 0.35 0.35], ...
     'LineWidth', 0.6);
plot(ax, [pi, pj], [bracketY, bracketY], '-', 'Color', [0.35 0.35 0.35], ...
     'LineWidth', 0.6);
text(ax, (pi + pj) / 2, bracketY + 0.022, pairLabel, ...
     'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
     'FontName', 'Times New Roman', 'FontSize', 8, 'Color', [0.20 0.20 0.20]);

%% ------------------------------------------------------------- axes ----
xlim(ax, [0.4, nD + 0.6]);
set(ax, 'XTick', 1:nD, 'XTickLabel', districts, ...
        'YTick', 0:0.2:1, 'YTickLabel', {'0', '0.2', '0.4', '0.6', '0.8', '1.0'}, ...
        'FontSize', 9, 'TickDir', 'out', ...
        'Box', 'off', 'Layer', 'top', ...
        'XColor', [0.15 0.15 0.15], 'YColor', [0.15 0.15 0.15]);
grid(ax, 'on');
ax.YGrid = 'on';
ax.XGrid = 'off';
ax.GridColor = [0.75 0.75 0.75];
ax.GridAlpha = 1.0;
ax.YMinorGrid = 'off';

xlabel(ax, 'District', 'FontSize', 9.5);
ylabel(ax, 'Share of district land area', 'FontSize', 9.5);

lgd = legend(ax, b, tiers, 'Orientation', 'horizontal', ...
             'Location', 'southoutside', 'Box', 'off', 'FontSize', 9, ...
             'TextColor', [0.15 0.15 0.15], 'Color', 'none');
lgd.ItemTokenSize = [10, 8];

hold(ax, 'off');

%% ------------------------------------------------------------- export ---
outDir = fileparts(mfilename('fullpath'));
if isempty(outDir)
    outDir = pwd;
end

exportgraphics(fig, fullfile(outDir, 'figure.png'), ...
               'Resolution', 300, 'BackgroundColor', 'white');
exportgraphics(fig, fullfile(outDir, 'figure.pdf'), ...
               'ContentType', 'vector', 'BackgroundColor', 'white');

close(fig);
fprintf('Wrote figure.png and figure.pdf to %s\n', outDir);
