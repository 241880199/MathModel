% probe_e.m --- M3 matlab recon: isolate WHAT flips the default palette between sessions
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_e.m')"
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/e';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_e start ###\n');

function p = snap(tag)
  co = get(groot,'DefaultAxesColorOrder');
  L  = lines(7);
  fc = get(groot,'defaultFigureColor');
  p = sprintf('[%s] groot-co1=#%02X%02X%02X  lines1=#%02X%02X%02X  nRows=%d  figColor=#%02X%02X%02X', ...
     tag, round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)), ...
          round(255*L(1,1)),round(255*L(1,2)),round(255*L(1,3)), size(co,1), ...
          round(255*fc(1)),round(255*fc(2)),round(255*fc(3)));
  fprintf('%s\n', p);
end

snap('t0-noop');
f = figure('Visible','off','Position',[100 100 631 260]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(f); x=linspace(0,2*pi,200); plot(ax,x,sin(x)); xlabel(ax,'t');
snap('t1-fig-created');
exportgraphics(f, fullfile(OUT,'e_eg.pdf'));
snap('t2-after-exportgraphics-pdf');
exportgraphics(f, fullfile(OUT,'e_eg.png'),'Resolution',200);
snap('t3-after-exportgraphics-png');
print(f, fullfile(OUT,'e_pr.pdf'),'-dpdf');
snap('t4-after-print-pdf');
print(f, fullfile(OUT,'e_pr.png'),'-dpng','-r200');
snap('t5-after-print-png');
saveas(f, fullfile(OUT,'e_sa.png'));
snap('t6-after-saveas');
close(f);
snap('t7-after-close');

% does a fresh figure after all that use the same palette?
f2 = figure('Visible','off'); a2=axes(f2); plot(a2,1:3,[1 2 3]);
h = findobj(a2,'Type','line'); c = get(h(1),'Color');
fprintf('[t8] NEW figure line color = #%02X%02X%02X\n', round(255*c(1)),round(255*c(2)),round(255*c(3)));
snap('t8-new-fig');
close(f2);

% probe theme-ish internals
disp('--- theme-ish probes ---');
try
  disp(get(groot,'defaultFigureTheme'));
catch e; fprintf('groot defaultFigureTheme: %s\n', e.message); end
try
  t = matlab.lang.Theme.getCurrent(); fprintf('matlab.lang.Theme.getCurrent = %s\n', string(t));
catch e; fprintf('Theme.getCurrent: %s\n', e.message); end
try
  fprintf('defaultAxesColorOrder is factory: ');
  co = get(groot,'DefaultAxesColorOrder');
  fprintf('factory=%d\n', isequal(co, get(groot,'factoryAxesColorOrder')));
catch e; fprintf('%s\n', e.message); end
disp('=== probe_e done ===');
