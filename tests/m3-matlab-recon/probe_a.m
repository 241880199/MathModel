% probe_a.m --- M3 matlab recon, block A/B: env / export paths / fonts / LF discipline
% re-run from repo root (the "run()" cwd gotcha is worked around by the cd prologue below):
%   d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_a.m')"
% outputs land in build/m3-matlab-recon/a/
% NOTE: version-controlled evidence. Do not edit after capture; re-run instead.

% --- prologue: pin cwd to repo root (MATLAB `run` moves cwd to the script folder; measured) ---
here = fileparts(mfilename('fullpath'));          % .../tests/m3-matlab-recon
root = fileparts(fileparts(here));                % repo root
cd(root);
fprintf('### probe_a start ###\n');
fprintf('repo root (derived) = %s\n', root);

OUT = 'build/m3-matlab-recon/a';
if ~exist(OUT, 'dir'); mkdir(OUT); end

%% ---------- P0 environment ----------
disp('=== P0 environment ===');
fprintf('version        = %s\n', version);
fprintf('release        = %s\n', version('-release'));
fprintf('matlabroot     = %s\n', matlabroot);
fprintf('arch           = %s\n', computer('arch'));
fprintf('cwd            = %s\n', pwd);

%% ---------- P1 exist() survey ----------
disp('=== P1 exist() survey ===');
names = {'exportgraphics','print','saveas','savefig','openfig','axes', ...
         'tiledlayout','nexttile','exportapp','copygraphics','getframe','listfonts'};
for k = 1:numel(names)
    fprintf('exist(%-16s) = %d\n', names{k}, exist(names{k}));
end

%% ---------- P2 default figure/axes properties ----------
disp('=== P2 default figure/axes props (factory) ===');
fprintf('defaultFigurePaperUnits    = %s\n', get(groot,'defaultFigurePaperUnits'));
fprintf('defaultFigurePaperPosition = [%s]\n', num2str(get(groot,'defaultFigurePaperPosition')));
fprintf('defaultFigurePaperSize     = [%s]\n', num2str(get(groot,'defaultFigurePaperSize')));
fprintf('defaultFigurePosition      = [%s]\n', num2str(get(groot,'defaultFigurePosition')));
fprintf('defaultAxesFontName        = %s\n', get(groot,'defaultAxesFontName'));
fprintf('defaultAxesFontSize        = %s\n', num2str(get(groot,'defaultAxesFontSize')));
fprintf('defaultAxesLineWidth       = %s\n', num2str(get(groot,'defaultAxesLineWidth')));
fprintf('defaultLineLineWidth       = %s\n', num2str(get(groot,'defaultLineLineWidth')));
fprintf('defaultFigureColor         = [%s]\n', num2str(get(groot,'defaultFigureColor')));
co = get(groot,'DefaultAxesColorOrder');
fprintf('DefaultAxesColorOrder rows = %d cols = %d\n', size(co,1), size(co,2));
fprintf('DefaultAxesColorOrder hex  = %s\n', strjoin(arrayfun(@(k) sprintf('#%02X%02X%02X', round(255*co(k,1)), round(255*co(k,2)), round(255*co(k,3))), 1:size(co,1), 'uni', 0), ' '));

%% ---------- P3 fonts census ----------
disp('=== P3 fonts census ===');
fl = listfonts;
fprintf('listfonts count = %d\n', numel(fl));
fid = fopen(fullfile(OUT,'p3_listfonts.txt'), 'wb');
for k = 1:numel(fl); fprintf(fid, '%s\n', fl{k}); end
fclose(fid);
probe = {'Arial','Times New Roman','Times','Nimbus Roman','Liberation Serif', ...
         'STIXGeneral','DejaVu Serif','Cambria','SimSun','Microsoft YaHei','SimHei', ...
         'TeXGyreTermes','TeX Gyre Termes','TeXGyreTermesX', ...
         '宋体','黑体','微软雅黑','SimSun-ExtB'};
for k = 1:numel(probe)
    fprintf('listfonts has %-18s : %d\n', probe{k}, any(strcmpi(fl, probe{k})));
end

%% ---------- P4 LF discipline: which fopen mode yields LF-only ----------
disp('=== P4 LF discipline (byte-level) ===');
modes = {'w','W','wb','wt'};
for k = 1:numel(modes)
    fn = fullfile(OUT, sprintf('_lf_%s.txt', modes{k}));
    fid = fopen(fn, modes{k});
    fprintf(fid, 'line1\nline2\n');
    fclose(fid);
    fid = fopen(fn, 'rb'); raw = fread(fid, Inf, '*uint8'); fclose(fid);
    fprintf('fopen mode %-3s -> bytes=%d  CR(13)=%d  LF(10)=%d\n', ...
            modes{k}, numel(raw), sum(raw==13), sum(raw==10));
end
% same for a claim written via dlmwrite-free path: check fid=1 (stdout) cannot be byte-read here
fprintf('NOTE: MATLAB -batch stdout is captured by the shell, not by this probe.\n');

%% ---------- P5 headless figure + 6 export paths ----------
disp('=== P5 six export paths ===');
x = linspace(0, 2*pi, 200);
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches');
set(fig,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(fig);
hold(ax,'on');
plot(ax, x, sin(x),   'DisplayName','alpha');
plot(ax, x, sin(2*x), 'DisplayName','beta');
plot(ax, x, sin(3*x), 'DisplayName','gamma');
hold(ax,'off');
xlabel(ax,'t'); ylabel(ax,'y'); title(ax,'Six export paths'); legend(ax,'show');
fprintf('P5 figure Position      = [%s]\n', num2str(get(fig,'Position')));
fprintf('P5 figure PaperUnits    = %s\n', get(fig,'PaperUnits'));
fprintf('P5 figure PaperPosition = [%s]\n', num2str(get(fig,'PaperPosition')));
fprintf('P5 figure PaperSize     = [%s]\n', num2str(get(fig,'PaperSize')));
fprintf('P5 figure PaperType     = %s\n', get(fig,'PaperType'));
fprintf('P5 ax Position          = [%s]\n', num2str(get(ax,'Position')));
fprintf('P5 ax OuterPosition     = [%s]\n', num2str(get(ax,'OuterPosition')));
fprintf('P5 ax TightInset        = [%s]\n', num2str(get(ax,'TightInset')));

paths = {};
paths{end+1} = {'exportgraphics_png', @(f,p) exportgraphics(f, p, 'Resolution', 200)};
paths{end+1} = {'exportgraphics_pdf', @(f,p) exportgraphics(f, p)};
paths{end+1} = {'exportgraphics_pdf_vector', @(f,p) exportgraphics(f, p, 'ContentType','vector')};
paths{end+1} = {'exportgraphics_pdf_image',  @(f,p) exportgraphics(f, p, 'ContentType','image','Resolution',200)};
paths{end+1} = {'print_dpng',  @(f,p) print(f, p, '-dpng', '-r200')};
paths{end+1} = {'print_dpdf',  @(f,p) print(f, p, '-dpdf')};
paths{end+1} = {'saveas_png',  @(f,p) saveas(f, p)};
paths{end+1} = {'saveas_pdf',  @(f,p) saveas(f, p)};

for k = 1:numel(paths)
    tag = paths{k}{1}; fn = paths{k}{2};
    if contains(tag,'pdf'); ext = '.pdf'; else; ext = '.png'; end
    p = fullfile(OUT, sprintf('p5_%s%s', tag, ext));
    t0 = tic; ok = true; msg = '';
    try
        fn(fig, p);
    catch e
        ok = false; msg = sprintf('%s: %s', e.identifier, e.message);
    end
    el = toc(t0);
    if exist(p,'file'); nb = dir(p).bytes; else; nb = -1; end
    fprintf('%-26s ok=%d  %.2fs  bytes=%d\n', tag, ok, el, nb);
    if ~ok; fprintf('    ERROR %s\n', msg); end
end

%% ---------- P6 default font on the figure + Chinese ----------
disp('=== P6 default font + Chinese ===');
fprintf('gca FontName = %s\n', get(ax,'FontName'));
fprintf('gca FontSize = %s\n', num2str(get(ax,'FontSize')));
lastwarn('');
fig2 = figure('Visible','off','Position',[100 100 631 260]);
ax2 = axes(fig2);
plot(ax2, x, sin(x));
try
    xlabel(ax2, '时间 (秒)'); ylabel(ax2, '振幅'); title(ax2, '中文标题');
    p = fullfile(OUT,'p6_chinese_default.pdf'); exportgraphics(fig2, p);
    fprintf('chinese(default font) export ok, bytes=%d\n', dir(p).bytes);
    p2 = fullfile(OUT,'p6_chinese_default.png'); exportgraphics(fig2, p2, 'Resolution', 200);
    fprintf('chinese(default font) png ok, bytes=%d\n', dir(p2).bytes);
catch e
    fprintf('chinese export RAISED %s: %s\n', e.identifier, e.message);
end
[wmsg, wid] = lastwarn;
fprintf('chinese lastwarn id=[%s] msg=[%s]\n', wid, wmsg);
% with SimHei / SimSun explicitly requested
for fname = {'SimHei','SimSun','Microsoft YaHei'}
    fig3 = figure('Visible','off','Position',[100 100 631 260]);
    ax3 = axes(fig3); plot(ax3, x, sin(x));
    set(ax3,'FontName', fname{1});
    fprintf('requested FontName=%s -> get(ax,FontName)=%s\n', fname{1}, get(ax3,'FontName'));
    p = fullfile(OUT, sprintf('p6_chinese_%s.pdf', fname{1}));
    try
        exportgraphics(fig3, p); fprintf('   export ok bytes=%d\n', dir(p).bytes);
    catch e
        fprintf('   RAISED %s: %s\n', e.identifier, e.message);
    end
    close(fig3);
end

%% ---------- P7 Times New Roman + bundled OTF font availability ----------
disp('=== P7 Times family + bundled OTF ===');
fig4 = figure('Visible','off','Position',[100 100 631 260]);
ax4 = axes(fig4);
plot(ax4, x, sin(x)); xlabel(ax4,'t'); ylabel(ax4,'y'); title(ax4,'Times face');
set(ax4, 'FontName', 'Times New Roman');
fprintf('after set, gca FontName = %s\n', get(ax4,'FontName'));
try
    p = fullfile(OUT,'p7_times.pdf'); exportgraphics(fig4, p);
    fprintf('times pdf ok, bytes=%d\n', dir(p).bytes);
catch e
    fprintf('times pdf RAISED %s: %s\n', e.identifier, e.message);
end

fontdir = '.claude/skills/mcm-plot-python/assets/fonts';
fprintf('fontdir (%s) exists = %d\n', fontdir, exist(fontdir,'dir'));
if exist(fontdir,'dir')
    d = dir(fullfile(fontdir,'*.otf'));
    for k=1:numel(d); fprintf('  otf: %s (%d B)\n', d(k).name, d(k).bytes); end
    addpath(fontdir);
    fl2 = listfonts;
    fprintf('after addpath, listfonts count = %d\n', numel(fl2));
    fprintf('after addpath, has TeXGyreTermesX : %d\n', any(strcmpi(fl2,'TeXGyreTermesX')));
    fprintf('after addpath, has TeX Gyre Termes : %d\n', any(strcmpi(fl2,'TeX Gyre Termes')));
    % Java-level parse test (MATLAB's r2025b -batch has no JVM here -> expect failure, record it)
    try
        jf = java.awt.Font.createFont(java.awt.Font.TRUETYPE_FONT, java.io.File(fullfile(fontdir,'TeXGyreTermesX-Regular.otf')));
        fprintf('Java Font.createFont OK: family=%s name=%s\n', char(jf.getFamily()), char(jf.getFontName()));
    catch e
        fprintf('Java Font.createFont RAISED: %s: %s\n', e.identifier, e.message);
    end
    % try to actually use it as a MATLAB font name
    try
        set(ax4, 'FontName', 'TeXGyreTermesX');
        fprintf('set FontName=TeXGyreTermesX -> gca FontName = %s\n', get(ax4,'FontName'));
        p = fullfile(OUT,'p7_otfname.pdf'); exportgraphics(fig4, p);
        fprintf('otf-name pdf ok, bytes=%d\n', dir(p).bytes);
    catch e
        fprintf('otf-name RAISED %s: %s\n', e.identifier, e.message);
    end
    rmpath(fontdir);
end

close all;
disp('=== probe_a done ===');
