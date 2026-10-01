% make_figure.m
% Figure 1 - vulnerability composition of districts A-F (100% stacked bars).
%
% Deterministic, offline, headless-safe. Run with:
%   matlab -batch "run('<this folder>/make_figure.m')"
% Writes figure.png (300 dpi) and figure.pdf (vector) next to this script.

% ---------------- output location = folder holding this script ----------------
thisFile = mfilename('fullpath');
if isempty(thisFile)
    outDir = pwd;
else
    outDir = fileparts(thisFile);
end

% ---------------- data: share of district land area by tier ----------------
% Rows sum to 1.00 for every district (asserted below).
districts = {'A', 'B', 'C', 'D', 'E', 'F'};
low  = [0.42; 0.31; 0.55; 0.28; 0.37; 0.50];
med  = [0.35; 0.44; 0.30; 0.47; 0.38; 0.33];
high = [0.23; 0.25; 0.15; 0.25; 0.25; 0.17];
M = [low, med, high];

% ---------------- sanity checks ----------------
assert(all(abs(sum(M, 2) - 1) < 1e-9), ...
    'Each district''s tier shares must sum to 1.');
assert(numel(districts) == size(M, 1), ...
    'Exactly one label per district is required.');

% ---------------- style ----------------
tierNames  = {'Low', 'Medium', 'High'};
tierColors = [254 224 210; 252 146 114; 222  45  38] / 255;  % sequential, low->high
labelColor = {'k', 'k', 'w'};                                % text on each tier

fontName = 'Times New Roman';
fsAxis   = 10;
fsTick   = 9;
fsLbl    = 9;
fsLeg    = 9;

% ---------------- figure + axes ----------------
fig = figure('Color', 'w', 'Units', 'inches', ...
    'Position', [0.5 0.5 6.5 3.4], 'Visible', 'off', ...
    'InvertHardcopy', 'off');

% Force the light theme so the export does not inherit a dark session theme
% (R2025a+); the try/catch keeps this a no-op on older releases.
try
    theme(fig, 'light');
catch
end

ax = axes('Parent', fig, 'Color', 'w'); %#ok<LAXES>

h = barh(1:numel(districts), M, 0.66, 'stacked', 'Parent', ax);
for k = 1:numel(h)
    set(h(k), 'FaceColor', tierColors(k, :), 'EdgeColor', 'w', 'LineWidth', 1.0);
end

ax.YDir       = 'reverse';
ax.YTick      = 1:numel(districts);
ax.YTickLabel = districts;
ax.YLim       = [0.4, numel(districts) + 0.6];
ax.XLim       = [0, 1];
ax.XTick      = 0:0.25:1;
ax.XTickLabel = {'0', '25', '50', '75', '100'};
ax.FontName   = fontName;
ax.FontSize   = fsTick;
ax.TickDir    = 'out';
ax.LineWidth  = 0.8;
ax.XGrid      = 'off';
ax.YGrid      = 'off';
ax.Box        = 'off';
ax.XColor     = [0.15 0.15 0.15];
ax.YColor     = [0.15 0.15 0.15];

xlabel(ax, 'Share of district land area (%)', ...
    'FontName', fontName, 'FontSize', fsAxis);
ax.XLabel.Color = [0.15 0.15 0.15];

% ---------------- legend (above the axes, horizontal) ----------------
lg = legend(ax, h, tierNames, 'Orientation', 'horizontal', ...
    'Location', 'northoutside', 'Box', 'off', ...
    'FontName', fontName, 'FontSize', fsLeg);
lg.ItemTokenSize = [12 10];
lg.Color     = 'none';
lg.TextColor = [0.15 0.15 0.15];

% ---------------- value labels on each segment ----------------
for i = 1:numel(districts)
    x0 = 0;
    for k = 1:size(M, 2)
        v = M(i, k);
        if v >= 0.06
            text(x0 + v / 2, i, sprintf('%d%%', round(v * 100)), ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', ...
                'FontName', fontName, 'FontSize', fsLbl, 'Color', labelColor{k});
        end
        x0 = x0 + v;
    end
end

% ---------------- export ----------------
pngPath = fullfile(outDir, 'figure.png');
pdfPath = fullfile(outDir, 'figure.pdf');
exportgraphics(fig, pngPath, 'Resolution', 300);
exportgraphics(fig, pdfPath, 'ContentType', 'vector');

fprintf('Wrote:\n  %s\n  %s\n', pngPath, pdfPath);
