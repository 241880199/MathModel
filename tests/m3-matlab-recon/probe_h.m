% probe_h.m --- M3 matlab recon: THEME timeline + dark-background export (fix round)
% re-run (two sessions, one with PROBE_VISIBLE set):
%   d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_h.m')"
%   d:/Software/Matlab/bin/matlab -batch "PROBE_VISIBLE=1; run('tests/m3-matlab-recon/probe_h.m')"
% NOTE: this file must NOT be called theme.m -- a script named theme.m shadows the
%       built-in theme() ("不支持将脚本 theme 作为函数执行").
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
if exist('PROBE_VISIBLE','var') && PROBE_VISIBLE
  MODE = 'on';
else
  MODE = 'off';
end
OUT = sprintf('build/m3-matlab-recon/h_%s', MODE);
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_h start ###  MODE=Visible:%s  cwd=%s\n', MODE, pwd);

function snap(tag)
  co = get(groot,'DefaultAxesColorOrder');
  fc = get(groot,'defaultFigureColor');
  fprintf('[%s] defaultFigureColor=[%.4f %.4f %.4f] hex=#%02X%02X%02X  colorOrder1=[%.4f %.4f %.4f] hex=#%02X%02X%02X\n', ...
      tag, fc(1),fc(2),fc(3), round(255*fc(1)),round(255*fc(2)),round(255*fc(3)), ...
      co(1,1),co(1,2),co(1,3), round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)));
end

function c11 = corner1(p)
  I = imread(p);
  c11 = squeeze(I(1,1,1:3))';
end

%% ---- T: timeline of the theme flip ----
disp('=== T timeline ===');
fprintf('probe mode = Visible:%s\n', MODE);
fprintf('exist(''theme'') = %d   exist(''imread'') = %d   exist(''drawnow'') = %d\n', ...
        exist('theme'), exist('imread'), exist('drawnow'));
snap('T0-session-start-no-figure');

f = figure('Visible',MODE,'Position',[100 100 631 260]);
fprintf('T1 f.Color=[%.4f %.4f %.4f]  ', get(f,'Color'));
try; fprintf('f.Theme=%s', string(get(f,'Theme'))); catch e; fprintf('f.Theme ERR(%s)', e.message); end
fprintf('\n');
snap('T1-after-figure-created');

drawnow;
snap('T2-after-drawnow');

set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(f); x = linspace(0,2*pi,200); plot(ax, x, sin(x)); xlabel(ax,'t'); ylabel(ax,'y');
fprintf('T3 f.Color=[%.4f %.4f %.4f] ax.Color=[%.4f %.4f %.4f]\n', get(f,'Color'), get(ax,'Color'));
snap('T3-after-axes-plotted');

drawnow;
snap('T4-after-drawnow-2');

exportgraphics(f, fullfile(OUT,'T5_eg1.png'), 'Resolution', 200);
fprintf('T5 corner(eg#1)=[%d %d %d]  f.Color=[%.4f %.4f %.4f]\n', corner1(fullfile(OUT,'T5_eg1.png')), get(f,'Color'));
snap('T5-after-first-exportgraphics');

print(f, fullfile(OUT,'T6_pr1.png'), '-dpng', '-r200');
fprintf('T6 corner(print#1, SAME figure)=[%d %d %d]\n', corner1(fullfile(OUT,'T6_pr1.png')));
snap('T6-after-first-print');

f2 = figure('Visible',MODE,'Position',[100 100 631 260]);
set(f2,'PaperUnits','inches'); set(f2,'PaperPosition',[0 0 6.31 2.6]);
ax2 = axes(f2); plot(ax2, x, cos(x));
fprintf('T7 NEW figure Color=[%.4f %.4f %.4f] ax2.Color=[%.4f %.4f %.4f]\n', get(f2,'Color'), get(ax2,'Color'));
exportgraphics(f2, fullfile(OUT,'T7_newfig.png'), 'Resolution', 200);
fprintf('T7 corner=[%d %d %d]\n', corner1(fullfile(OUT,'T7_newfig.png')));
snap('T7-new-figure-after-flip');
close(f2);

%% ---- C: does setting Color explicitly work? ----
disp('=== C: explicit Color ===');
f3 = figure('Visible',MODE,'Color','w','Position',[100 100 631 260]);
set(f3,'PaperUnits','inches'); set(f3,'PaperPosition',[0 0 6.31 2.6]);
ax3 = axes(f3,'Color','w'); plot(ax3, x, sin(x)); xlabel(ax3,'t'); ylabel(ax3,'y');
fprintf('C1 requested figure Color=w  -> get(f3,Color)=[%.4f %.4f %.4f]\n', get(f3,'Color'));
fprintf('C1 requested axes   Color=w  -> get(ax3,Color)=[%.4f %.4f %.4f]\n', get(ax3,'Color'));
fprintf('C1 ax3 XColor=[%.4f %.4f %.4f] YColor=[%.4f %.4f %.4f]\n', get(ax3,'XColor'), get(ax3,'YColor'));
exportgraphics(f3, fullfile(OUT,'C1_colorw.png'), 'Resolution', 200);
fprintf('C1 corner=[%d %d %d]\n', corner1(fullfile(OUT,'C1_colorw.png')));

%% ---- L: theme(fig,'light') recipe ----
disp('=== L: theme light recipe ===');
f4 = figure('Visible',MODE,'Position',[100 100 631 260]);
set(f4,'PaperUnits','inches'); set(f4,'PaperPosition',[0 0 6.31 2.6]);
ax4 = axes(f4); plot(ax4, x, sin(x)); xlabel(ax4,'t'); ylabel(ax4,'y');
ok = true; msg = '';
try
  theme(f4,'light');
catch e
  ok = false; msg = sprintf('%s: %s', e.identifier, e.message);
end
fprintf('L1 theme(f4,''light'') ok=%d %s\n', ok, msg);
set(f4,'Color','w');
set(ax4,'Color','w','XColor','k','YColor','k');
fprintf('L1 after recipe: f4.Color=[%.4f %.4f %.4f] ax4.Color=[%.4f %.4f %.4f] XColor=[%.4f %.4f %.4f]\n', ...
    get(f4,'Color'), get(ax4,'Color'), get(ax4,'XColor'));
try; fprintf('L1 f4.Theme=%s\n', string(get(f4,'Theme'))); catch e; fprintf('L1 f4.Theme ERR %s\n', e.message); end
exportgraphics(f4, fullfile(OUT,'L1_light_eg.png'), 'Resolution', 200);
exportgraphics(f4, fullfile(OUT,'L1_light_eg.pdf'));
print(f4, fullfile(OUT,'L1_light_pr.png'), '-dpng', '-r200');
print(f4, fullfile(OUT,'L1_light_pr.pdf'), '-dpdf');
fprintf('L1 corner(eg png)=[%d %d %d]\n', corner1(fullfile(OUT,'L1_light_eg.png')));
fprintf('L1 corner(print png)=[%d %d %d]\n', corner1(fullfile(OUT,'L1_light_pr.png')));
snap('L1-after-light-recipe');
close all;

%% ---- P: presentation comparison, print vs exportgraphics (label-heavy) ----
disp('=== P: print vs exportgraphics, label-heavy figure ===');
f5 = figure('Visible',MODE,'Position',[100 100 631 260]);
set(f5,'PaperUnits','inches'); set(f5,'PaperPosition',[0 0 6.31 2.6]); set(f5,'PaperPositionMode','manual');
set(f5,'PaperSize',[6.31 2.6]);
ax5 = axes(f5); plot(ax5, x, sin(x));
xlabel(ax5,'time (s)'); ylabel(ax5,'amplitude (a.u.)'); title(ax5,'A fairly long figure title');
exportgraphics(f5, fullfile(OUT,'P_eg.png'), 'Resolution', 200);
exportgraphics(f5, fullfile(OUT,'P_eg.pdf'));
print(f5, fullfile(OUT,'P_pr.png'), '-dpng', '-r200');
print(f5, fullfile(OUT,'P_pr.pdf'), '-dpdf');
fprintf('P exportgraphics png corner=[%d %d %d]\n', corner1(fullfile(OUT,'P_eg.png')));
fprintf('P print         png corner=[%d %d %d]\n', corner1(fullfile(OUT,'P_pr.png')));
close all;

disp('=== probe_h done ===');
