% probe_b.m --- M3 matlab recon, block A2: the SIZE CALIBER (single-variable experiments)
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_b.m')"
% outputs: build/m3-matlab-recon/b/
% Every case exports: exportgraphics PNG(Res 200), print -dpng -r200, exportgraphics PDF, print -dpdf.
% The python side (measure_size.py) then reads px / page-box / fonts off the artifacts.
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/b';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_b start ###  cwd=%s\n', pwd);

% ---- helper: build a figure with given pixel Position and inch PaperPosition ----
function fig = mkfig(pospx, paperin)
    fig = figure('Visible','off','Position',[100 100 pospx(1) pospx(2)]);
    set(fig,'PaperUnits','inches');
    set(fig,'PaperPosition',[0 0 paperin(1) paperin(2)]);
    ax = axes(fig);
    x = linspace(0,2*pi,200);
    plot(ax, x, sin(x)); plot(ax, x, cos(x));
    xlabel(ax,'t'); ylabel(ax,'y'); title(ax,'size probe');
end

function dumpfig(tag, fig)
    fprintf('[%s] Position      = [%s]\n', tag, num2str(get(fig,'Position')));
    fprintf('[%s] PaperUnits    = %s\n',     tag, get(fig,'PaperUnits'));
    fprintf('[%s] PaperPosition = [%s]\n',   tag, num2str(get(fig,'PaperPosition')));
    fprintf('[%s] PaperSize     = [%s]\n',   tag, num2str(get(fig,'PaperSize')));
    fprintf('[%s] PaperType     = %s\n',     tag, get(fig,'PaperType'));
    ax = findobj(fig,'Type','axes');
    fprintf('[%s] ax.Position   = [%s]\n',   tag, num2str(get(ax(1),'Position')));
    fprintf('[%s] ax.TightInset = [%s]\n',   tag, num2str(get(ax(1),'TightInset')));
end

function runcase(tag, fig, OUT)
    dumpfig(tag, fig);
    t0=tic;
    exportgraphics(fig, fullfile(OUT, sprintf('%s_eg.png', tag)), 'Resolution', 200);
    exportgraphics(fig, fullfile(OUT, sprintf('%s_eg.pdf', tag)));
    print(fig, fullfile(OUT, sprintf('%s_pr.png', tag)), '-dpng', '-r200');
    print(fig, fullfile(OUT, sprintf('%s_pr.pdf', tag)), '-dpdf');
    fprintf('[%s] 4 exports in %.2fs\n', tag, toc(t0));
    close(fig);
end

%% ---- t0 baseline: Position 631x260 px, PaperPosition 6.31x2.6 in ----
runcase('t0_base', mkfig([631 260], [6.31 2.6]), OUT);

%% ---- t1 ONLY pixel Position width changes (631 -> 800) ----
runcase('t1_pos_w800', mkfig([800 260], [6.31 2.6]), OUT);

%% ---- t2 ONLY pixel Position height changes (260 -> 400) ----
runcase('t2_pos_h400', mkfig([631 400], [6.31 2.6]), OUT);

%% ---- t3 ONLY PaperPosition width changes (6.31 -> 8.0) ----
runcase('t3_paper_w800', mkfig([631 260], [8.0 2.6]), OUT);

%% ---- t4 ONLY PaperPosition height changes (2.6 -> 3.5) ----
runcase('t4_paper_h350', mkfig([631 260], [6.31 3.5]), OUT);

%% ---- t5 PaperSize forced to 11x8.5 in (with PaperPosition untouched) ----
fig = mkfig([631 260], [6.31 2.6]);
set(fig,'PaperUnits','inches');
try
    set(fig,'PaperSize',[11 8.5]);
    fprintf('[t5] set PaperSize [11 8.5] OK\n');
catch e
    fprintf('[t5] set PaperSize RAISED %s: %s\n', e.identifier, e.message);
end
runcase('t5_paper_size', fig, OUT);

%% ---- t6 PaperType letter ----
fig = mkfig([631 260], [6.31 2.6]);
set(fig,'PaperType','<custom>');
set(fig,'PaperUnits','inches'); set(fig,'PaperSize',[8.5 11]);
runcase('t6_letter', fig, OUT);

%% ---- c1 exportgraphics Padding default vs 0 (implicit-crop test) ----
fig = mkfig([631 260], [6.31 2.6]);
dumpfig('c1_fig', fig);
exportgraphics(fig, fullfile(OUT,'c1_pad_default.pdf'));
exportgraphics(fig, fullfile(OUT,'c1_pad_default.png'), 'Resolution', 200);
try
    exportgraphics(fig, fullfile(OUT,'c1_pad0.pdf'), 'Padding', 0);
    exportgraphics(fig, fullfile(OUT,'c1_pad0.png'), 'Resolution', 200, 'Padding', 0);
    fprintf('[c1] Padding 0 exports ok\n');
catch e
    fprintf('[c1] Padding 0 RAISED %s: %s\n', e.identifier, e.message);
end
close(fig);

%% ---- c2 content variation at FIXED PaperPosition (does content move the page box?) ----
% (a) nearly empty axes
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(fig); plot(ax,1:3,[1 2 3]);
exportgraphics(fig, fullfile(OUT,'c2_sparse_eg.pdf')); exportgraphics(fig, fullfile(OUT,'c2_sparse_eg.png'),'Resolution',200);
close(fig);
% (b) long axis labels + legend, same PaperPosition
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(fig); plot(ax,linspace(0,2*pi,200),sin(linspace(0,2*pi,200)),'DisplayName','a very long legend entry indeed');
ylabel(ax,'a very long y axis label'); xlabel(ax,'a very long x axis label'); legend(ax,'show');
exportgraphics(fig, fullfile(OUT,'c2_dense_eg.pdf')); exportgraphics(fig, fullfile(OUT,'c2_dense_eg.png'),'Resolution',200);
close(fig);

%% ---- c3 default colororder vs lines() ----
disp('=== c3 default color order vs lines(7) ===');
co = get(groot,'DefaultAxesColorOrder');
fprintf('default colororder rows=%d\n', size(co,1));
for k=1:size(co,1)
    fprintf('  default %d: [%.4f %.4f %.4f]\n', k, co(k,1), co(k,2), co(k,3));
end
L = lines(7);
for k=1:7
    fprintf('  lines   %d: [%.4f %.4f %.4f]\n', k, L(k,1), L(k,2), L(k,3));
end
fprintf('max abs diff default vs lines(7) = %.6f\n', max(abs(co(1:7,:)-L(:,:)),[],'all'));
fid = fopen(fullfile(OUT,'c3_colororder.txt'),'wb');
for k=1:size(co,1); fprintf(fid,'default %d %.6f %.6f %.6f\n', k, co(k,1),co(k,2),co(k,3)); end
for k=1:7; fprintf(fid,'lines %d %.6f %.6f %.6f\n', k, L(k,1),L(k,2),L(k,3)); end
fclose(fid);

disp('=== probe_b done ===');
