% make_figure.m
% -------------------------------------------------------------------------
% Drivers of historical disaster counts across six districts (A-F).
%
% The figure answers two questions:
%   (a) which measured factor is most strongly correlated with the
%       historical disaster count, and
%   (b) how similar the six districts are to one another.
%
% Panel (a): signed Pearson correlation of each factor with the disaster
%            count, sorted by |r|.
% Panel (b): district-by-attribute heatmap of standardized (z-scored)
%            values; districts are ordered by spectral seriation of their
%            pairwise distances so that similar districts sit together.
%
% Everything is computed from the tabulated numbers below. The script is
% deterministic, needs no network and no manual steps, and runs headlessly:
%
%     matlab -batch "run('make_figure.m')"
%
% It writes figure.png and figure.pdf next to this file.
% -------------------------------------------------------------------------

clear; close all; clc;

% --- locate output directory (the folder holding this script) -------------
scriptPath = mfilename('fullpath');
if isempty(scriptPath)
    outdir = pwd;
else
    outdir = fileparts(scriptPath);
end
if ~exist(outdir, 'dir')
    mkdir(outdir);
end

% --- data -----------------------------------------------------------------
district = {'A','B','C','D','E','F'};
pop   = [ 820;  640;  610; 1210;  990; 1750];   % people / km^2
slope = [ 3.2; 11.5;  2.4; 14.8;  7.1;  5.0];   % degrees
veg   = [0.61; 0.58; 0.72; 0.41; 0.49; 0.55];   % fraction of area
dis   = [  12;   31;    8;   38;   16;   24];   % historical disaster count
infra = [  74;   72;   81;   55;   66;   70];   % index, 0-100

X = [pop, slope, veg, dis, infra];              % 6 x 5
attrNames = {'Population density', 'Mean slope', 'Vegetation cover', ...
             'Disaster count', 'Infrastructure index'};
predNames = {'Population density', 'Mean slope', 'Vegetation cover', ...
             'Infrastructure index'};
n = size(X, 1);
np = numel(predNames);

% --- Pearson correlation of every factor with the disaster count ----------
% Column layout of X: 1 population, 2 slope, 3 vegetation, 4 disaster, 5 infra
predCols = [1 2 3 5];
disCol   = 4;
xc = X(:, predCols) - mean(X(:, predCols), 1);  % 6 x 4
dc = X(:, disCol)   - mean(X(:, disCol));       % 6 x 1
r  = sum(xc .* dc, 1) ./ (sqrt(sum(xc.^2, 1)) .* sqrt(sum(dc.^2)));  % 1 x 4
r  = r(:);                                      % 4 x 1

[rSorted, ixSort] = sort(abs(r), 'descend');
rSorted = r(ixSort);
namesSorted = predNames(ixSort);

% --- standardized attribute matrix ---------------------------------------
Z = (X - mean(X, 1)) ./ std(X, 0, 1);           % 6 x 5, z-scores

% --- order districts by similarity (spectral seriation) -------------------
D = zeros(n, n);
for i = 1:n
    for j = 1:n
        D(i, j) = sqrt(sum((Z(i, :) - Z(j, :)).^2));
    end
end
A = max(D(:)) - D;                              % distance -> similarity
A(1:n+1:end) = 0;                               % zero the diagonal
Ldeg = sum(A, 2);
L = diag(Ldeg) - A;                             % graph Laplacian
[V, Ev] = eig(L);
[~, eigOrder] = sort(diag(Ev));
fiedler = V(:, eigOrder(2));                    % 2nd-smallest eigenvector
[~, serOrder] = sort(fiedler);
Zord = Z(serOrder, :);
distOrder = district(serOrder);

% =========================================================================
% figure
% =========================================================================
set(groot, 'defaultAxesFontName', 'Helvetica', ...
           'defaultTextFontName', 'Helvetica', ...
           'defaultAxesFontSize', 8, ...
           'defaultAxesTickDir', 'out', ...
           'defaultAxesColor', 'white');
set(groot, 'defaultFigureColor', 'white');

colPos = [0.79 0.19 0.21];      % warm  (positive correlation)
colNeg = [0.13 0.40 0.67];      % cool  (negative correlation)
colEdge = [0.25 0.25 0.25];

fig = figure('Units', 'centimeters', 'Position', [2 2 17 7.6], ...
             'Color', 'white', 'PaperPositionMode', 'auto');

% --------------------------------------------------------------- panel (a)
ax1 = subplot(1, 2, 1);
b = barh(1:np, rSorted, 0.62, 'EdgeColor', colEdge, 'LineWidth', 0.5);
b.FaceColor = 'flat';
for k = 1:np
    if rSorted(k) >= 0
        b.CData(k, :) = colPos;
    else
        b.CData(k, :) = colNeg;
    end
end
set(ax1, 'YDir', 'reverse', 'YTick', 1:np, 'YTickLabel', namesSorted, ...
    'YLim', [0.4, np + 0.6], 'XLim', [-1 1], 'Box', 'off', ...
    'XGrid', 'on', 'GridColor', [0.85 0.85 0.85], 'GridAlpha', 1);
xline(0, 'Color', [0.35 0.35 0.35], 'LineWidth', 0.6);
for k = 1:np
    if rSorted(k) >= 0
        tx = rSorted(k) + 0.03; ha = 'left';
    else
        tx = rSorted(k) - 0.03; ha = 'right';
    end
    text(tx, k, sprintf('%+0.2f', rSorted(k)), ...
        'HorizontalAlignment', ha, 'VerticalAlignment', 'middle', ...
        'FontSize', 8, 'Color', [0.15 0.15 0.15]);
end
xlabel('Pearson correlation with disaster count, r');
title('(a) Factor correlation with disaster count', 'FontWeight', 'normal');

% --------------------------------------------------------------- panel (b)
ax2 = subplot(1, 2, 2);
lim = max(abs(Zord(:))) * 1.02;
imagesc(ax2, Zord);
set(ax2, 'XTick', 1:numel(attrNames), 'XTickLabel', attrNames, ...
    'YTick', 1:n, 'YTickLabel', distOrder, 'Box', 'on', ...
    'LineWidth', 0.5, 'TickLength', [0 0], 'XColor', colEdge, ...
    'YColor', colEdge);
xtickangle(ax2, 30);
caxis(ax2, [-lim, lim]);

% diverging blue-white-red colormap
ncol = 256;
ctrl = [colNeg; 1 1 1; colPos];
cmap = interp1([0 0.5 1], ctrl, linspace(0, 1, ncol));
colormap(ax2, cmap);
cb = colorbar(ax2);
cb.Label.String = 'standardized value (z-score)';
cb.Label.FontSize = 8;
cb.TickDirection = 'out';

% annotate cell values
for i = 1:n
    for j = 1:numel(attrNames)
        v = Zord(i, j);
        if abs(v) > 0.58 * lim
            tc = [1 1 1];
        else
            tc = [0.15 0.15 0.15];
        end
        text(ax2, j, i, sprintf('%0.2f', v), 'HorizontalAlignment', 'center', ...
            'VerticalAlignment', 'middle', 'FontSize', 7.5, 'Color', tc);
    end
end
title('(b) District similarity: standardized attribute profiles', ...
    'FontWeight', 'normal');

% --------------------------------------------------------------- export
pngPath = fullfile(outdir, 'figure.png');
pdfPath = fullfile(outdir, 'figure.pdf');
set(fig, 'InvertHardcopy', 'off');
if exist('exportgraphics', 'file') == 2
    exportgraphics(fig, pngPath, 'Resolution', 600);
    exportgraphics(fig, pdfPath, 'ContentType', 'vector');
else
    print(fig, pngPath, '-dpng', '-r600');
    print(fig, pdfPath, '-dpdf', '-painters');
end

% --- console summary (useful for the caption / for verification) ----------
fprintf('Correlation with disaster count (sorted by |r|):\n');
for k = 1:np
    fprintf('  %-22s r = %+0.3f\n', namesSorted{k}, rSorted(k));
end
fprintf(['District similarity order: %s\n'], strjoin(distOrder, ', '));
fprintf('Wrote %s and %s\n', pngPath, pdfPath);
