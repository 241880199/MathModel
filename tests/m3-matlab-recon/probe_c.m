% probe_c.m --- M3 matlab recon, blocks A3/A4: default palette ground truth, F2 scenarios, captions
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_c.m')"
% outputs: build/m3-matlab-recon/c/
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/c';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_c start ###  cwd=%s\n', pwd);

%% ---- q1: groot DefaultAxesColorOrder, several methods, full precision ----
disp('=== q1 colororder methods ===');
co = get(groot,'DefaultAxesColorOrder');
fprintf('size = %dx%d  class=%s\n', size(co,1), size(co,2), class(co));
for k=1:size(co,1)
  fprintf('groot-co %d = [%.6f %.6f %.6f]  hex=#%02X%02X%02X\n', k, co(k,1),co(k,2),co(k,3), ...
      round(255*co(k,1)), round(255*co(k,2)), round(255*co(k,3)));
end
L = lines(7);
for k=1:7
  fprintf('lines()  %d = [%.6f %.6f %.6f]  hex=#%02X%02X%02X\n', k, L(k,1),L(k,2),L(k,3), ...
      round(255*L(k,1)), round(255*L(k,2)), round(255*L(k,3)));
end
fprintf('max|groot-co - lines(7)| = %.8f\n', max(abs(co(1:7,:)-L),[],'all'));
co2 = get(0,'DefaultAxesColorOrder');
fprintf('get(0,...) 1 = [%.6f %.6f %.6f]  (identical to groot? %d)\n', co2(1,1),co2(1,2),co2(1,3), isequal(co,co2));

%% ---- q2: GROUND TRUTH: colors actually assigned to line objects ----
disp('=== q2 actual line colors (default axis) ===');
x = linspace(0,2*pi,200);
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(fig); hold(ax,'on');
for k=1:7; plot(ax, x, sin(x+k/3), 'LineWidth', 1.0); end
hold(ax,'off');
xlabel(ax,'t'); ylabel(ax,'y'); title(ax,'7 default series');
h = findobj(ax,'Type','line');
h = flipud(h);
for k=1:numel(h)
  c = get(h(k),'Color');
  fprintf('line %d Color = [%.6f %.6f %.6f]  hex=#%02X%02X%02X\n', k, c(1),c(2),c(3), ...
      round(255*c(1)), round(255*c(2)), round(255*c(3)));
end
exportgraphics(fig, fullfile(OUT,'c_default7.png'), 'Resolution', 200);
exportgraphics(fig, fullfile(OUT,'c_default7.pdf'));
print(fig, fullfile(OUT,'c_default7_pr.pdf'), '-dpdf');
close(fig);

%% ---- q3: N series with DEFAULT palette for N=1..7 (F2 readings) ----
disp('=== q3 default-palette N series ===');
for N=[1 2 3 4 5 6 7]
  fig = figure('Visible','off','Position',[100 100 631 260]);
  set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
  ax = axes(fig); hold(ax,'on');
  for k=1:N; plot(ax, x, sin(x*k/3), 'LineWidth', 1.0); end
  hold(ax,'off'); xlabel(ax,'t'); ylabel(ax,'y');
  exportgraphics(fig, fullfile(OUT, sprintf('c_defN%d.png',N)), 'Resolution', 200);
  exportgraphics(fig, fullfile(OUT, sprintf('c_defN%d.pdf',N)));
  close(fig);
  fprintf('exported c_defN%d\n', N);
end

%% ---- q4: MANUAL 2 / 3 / 4 colors, chromatic and well separated ----
disp('=== q4 manual 2/3/4 colors ===');
PAL = [0 0.4470 0.7410;    % classic blue
       0.8500 0.3250 0.0980;% classic orange
       0.4660 0.6740 0.1880;% classic green
       0.4940 0.1840 0.5560];% classic purple
for N=[2 3 4]
  fig = figure('Visible','off','Position',[100 100 631 260]);
  set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
  ax = axes(fig); hold(ax,'on');
  for k=1:N; plot(ax, x, sin(x*k/3), 'LineWidth', 1.0, 'Color', PAL(k,:)); end
  hold(ax,'off'); xlabel(ax,'t'); ylabel(ax,'y');
  exportgraphics(fig, fullfile(OUT, sprintf('c_manN%d.png',N)), 'Resolution', 200);
  exportgraphics(fig, fullfile(OUT, sprintf('c_manN%d.pdf',N)));
  close(fig);
  fprintf('exported c_manN%d\n', N);
end

%% ---- q5: can the default colororder be changed at all ----
disp('=== q5 settable? ===');
try
  old = get(groot,'DefaultAxesColorOrder');
  set(groot,'DefaultAxesColorOrder',[1 0 0; 0 0 1]);
  now = get(groot,'DefaultAxesColorOrder');
  fprintf('after set: size=%dx%d row1=[%.3f %.3f %.3f]\n', size(now,1), size(now,2), now(1,1),now(1,2),now(1,3));
  set(groot,'DefaultAxesColorOrder',old);
  fprintf('restored ok\n');
catch e
  fprintf('set RAISED %s: %s\n', e.identifier, e.message);
end

%% ---- q6: caption sources -- what MATLAB can emit as text ----
disp('=== q6 caption text sources ===');
fig = figure('Visible','off','Position',[100 100 631 260]);
ax = axes(fig); plot(ax,x,sin(x));
xlabel(ax,'t'); ylabel(ax,'y'); title(ax,'Series sample');
fprintf('xlabel = [%s]\n', get(get(ax,'XLabel'),'String'));
fprintf('ylabel = [%s]\n', get(get(ax,'YLabel'),'String'));
fprintf('title  = [%s]\n', get(get(ax,'Title'),'String'));
try
  exportgraphics(fig, fullfile(OUT,'c_capfig.pdf'), 'Resolution', 200);
  fprintf('capfig export ok\n');
catch e
  fprintf('capfig RAISED %s: %s\n', e.identifier, e.message);
end
close(fig);
disp('=== probe_c done ===');
