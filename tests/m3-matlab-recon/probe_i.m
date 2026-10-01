% probe_i.m --- M3 matlab recon: isolate WHAT flips the theme, and what actually fixes it
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_i.m')"
% (do NOT name this file theme.m -- a script theme.m shadows the built-in theme())
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/i';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_i start ###\n');

function snap(tag)
  co = get(groot,'DefaultAxesColorOrder'); fc = get(groot,'defaultFigureColor');
  fprintf('[%s] defaultFigureColor=#%02X%02X%02X  colorOrder1=#%02X%02X%02X\n', tag, ...
      round(255*fc(1)),round(255*fc(2)),round(255*fc(3)), ...
      round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)));
end

function c11 = corner1(p)
  I = imread(p); c11 = squeeze(I(1,1,1:3))';
end

%% ---- S: step-by-step isolation ----
disp('=== S step-by-step ===');
snap('S0-start');
f = figure('Visible','off','Position',[100 100 631 260]);
snap('S1-figure');
ax = axes(f);
snap('S2-axes');                        % <- the suspected trigger
drawnow;
snap('S3-drawnow-after-axes');
plot(ax, linspace(0,2*pi,200), sin(linspace(0,2*pi,200)));
snap('S4-plot');
drawnow;
snap('S5-drawnow-after-plot');
xlabel(ax,'t'); ylabel(ax,'y'); title(ax,'t');
snap('S6-labels');

%% ---- W: what fixes it ----
disp('=== W fixes ===');
fprintf('exist(''theme'') = %d\n', exist('theme'));
t = get(f,'Theme'); fprintf('Theme class = %s\n', class(t));
try
  p = properties(t);
  fprintf('Theme properties: %s\n', strjoin(p', ', '));
catch e
  fprintf('properties(Theme) ERR %s\n', e.message);
end
try
  disp(struct(t));   % dump whatever it exposes
catch e
  fprintf('struct(Theme) ERR %s\n', e.message);
end

% W1: does figure('Theme','light') work at creation time?
ok1 = true; m1 = '';
try
  f2 = figure('Visible','off','Position',[100 100 631 260], 'Theme','light');
catch e
  ok1 = false; m1 = sprintf('%s: %s', e.identifier, e.message);
end
fprintf('W1 figure(...,''Theme'',''light'') ok=%d %s\n', ok1, m1);
if ok1
  fprintf('W1 f2.Color=[%.4f %.4f %.4f]\n', get(f2,'Color'));
  ax2 = axes(f2); plot(ax2, 1:3, [1 2 3]);
  exportgraphics(f2, fullfile(OUT,'W1_newlight.png'), 'Resolution', 200);
  fprintf('W1 corner=[%d %d %d]\n', corner1(fullfile(OUT,'W1_newlight.png')));
  close(f2);
end

% W2: theme(fig,'light') then set colors (re-measure)
theme(f, 'light'); set(f,'Color','w');
set(ax,'Color','w','XColor','k','YColor','k');
exportgraphics(f, fullfile(OUT,'W2_themelight.png'), 'Resolution', 200);
fprintf('W2 corner=[%d %d %d]  ax.Color=[%.4f %.4f %.4f]\n', corner1(fullfile(OUT,'W2_themelight.png')), get(ax,'Color'));
co = get(ax,'ColorOrder');
fprintf('W2 colorOrder after theme light rows=%d first=#%02X%02X%02X\n', size(co,1), round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)));
close(f);

% W3: does theme('light') with no figure handle set a session-wide default?
ok3 = true; m3 = '';
try
  theme('light');
catch e
  ok3 = false; m3 = sprintf('%s: %s', e.identifier, e.message);
end
fprintf('W3 theme(''light'') (no handle) ok=%d %s\n', ok3, m3);
snap('W3-after-theme-no-handle');
f3 = figure('Visible','off','Position',[100 100 631 260]);
ax3 = axes(f3); plot(ax3, 1:3, [1 2 3]);
fprintf('W3 new figure Color=[%.4f %.4f %.4f] ax.Color=[%.4f %.4f %.4f]\n', get(f3,'Color'), get(ax3,'Color'));
exportgraphics(f3, fullfile(OUT,'W3_newfig.png'), 'Resolution', 200);
fprintf('W3 corner=[%d %d %d]\n', corner1(fullfile(OUT,'W3_newfig.png')));
close(f3);

% W4: groot-level default for the figure colour (does a plain figure come out light?)
%     (the earlier probe showed 'Theme' has no groot default; test the Color default instead)
snap('W4-end');
disp('=== probe_i done ===');
