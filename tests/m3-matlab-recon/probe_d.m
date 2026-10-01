% probe_d.m --- M3 matlab recon: palette identity (theme?), ScreenPixelsPerInch, size law, padding
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_d.m')"
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/d';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_d start ###  cwd=%s\n', pwd);

function showco(tag)
  co = get(groot,'DefaultAxesColorOrder');
  L = lines(7);
  fprintf('[%s] groot-co row1=[%.4f %.4f %.4f] hex=#%02X%02X%02X\n', tag, co(1,1),co(1,2),co(1,3), ...
     round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)));
  fprintf('[%s] lines(7) row1=[%.4f %.4f %.4f] hex=#%02X%02X%02X\n', tag, L(1,1),L(1,2),L(1,3), ...
     round(255*L(1,1)),round(255*L(1,2)),round(255*L(1,3)));
  fprintf('[%s] max|groot-lines| = %.8f\n', tag, max(abs(co(1:7,:)-L),[],'all'));
end

disp('=== r1 palette: before any figure ===');
showco('no-fig');

disp('=== r2 palette: with a figure open ===');
f0 = figure('Visible','off');
showco('fig-open');
ax0 = axes(f0); plot(ax0,1:3,[1 2 3]); h0 = findobj(ax0,'Type','line'); c0 = get(h0(1),'Color');
fprintf('line color with fig open = [%.4f %.4f %.4f] hex=#%02X%02X%02X\n', c0(1),c0(2),c0(3), ...
    round(255*c0(1)),round(255*c0(2)),round(255*c0(3)));
% try to read a theme-ish property
for p = {'Theme','ThemeName','SystemTheme'}
  try; v = get(f0, p{1}); fprintf('figure.%s = %s\n', p{1}, string(v)); catch; end
  try; v = get(groot, p{1}); fprintf('groot.%s = %s\n', p{1}, string(v)); catch; end
end
close(f0);
disp('=== r3 palette: after closing the figure ===');
showco('fig-closed');

disp('=== r4 screen pixels per inch ===');
fprintf('groot ScreenPixelsPerInch = %s\n', num2str(get(groot,'ScreenPixelsPerInch')));
try
  fprintf('groot ScreenSize = [%s]\n', num2str(get(groot,'ScreenSize')));
catch e
  fprintf('ScreenSize RAISED: %s\n', e.message);
end

%% ---- r5 SIZE LAW: pixel Position width sweep, identical content ----
disp('=== r5 size law (Position width sweep) ===');
widths = [400 600 631 800 1000 1200];
fid = fopen(fullfile(OUT,'r5_sizelaw.txt'),'wb');
fprintf(fid,'# PositionW  PaperPosW  egPdfW_pt  egPdfW_in  egPngW_px  prPngW_px  prPdfW_pt  contentNormW\n');
for W = widths
  fig = figure('Visible','off','Position',[100 100 W 260]);
  set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
  ax = axes(fig);
  x=linspace(0,2*pi,200); plot(ax,x,sin(x)); xlabel(ax,'t'); ylabel(ax,'y');
  P = get(ax,'Position'); TI = get(ax,'TightInset');
  cw = (P(1)-TI(1)) + P(3) + TI(3);
  exportgraphics(fig, fullfile(OUT,sprintf('r5_w%d_eg.pdf',W)));
  exportgraphics(fig, fullfile(OUT,sprintf('r5_w%d_eg.png',W)),'Resolution',200);
  print(fig, fullfile(OUT,sprintf('r5_w%d_pr.png',W)),'-dpng','-r200');
  print(fig, fullfile(OUT,sprintf('r5_w%d_pr.pdf',W)),'-dpdf');
  fprintf(fid,'%d 6.31 %.0f %.4f %.0f %.0f %.0f %.6f\n', W, 0,0,0,0,0,cw);
  fprintf('%d done (contentNormW=%.6f)\n', W, cw);
  close(fig);
end
fclose(fid);

%% ---- r6 Padding sweep on exportgraphics (implicit-crop knob) ----
disp('=== r6 Padding sweep ===');
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches'); set(fig,'PaperPosition',[0 0 6.31 2.6]);
ax=axes(fig); x=linspace(0,2*pi,200); plot(ax,x,sin(x)); xlabel(ax,'t'); ylabel(ax,'y');
for pad = [0 1 2 5 10]
  try
    exportgraphics(fig, fullfile(OUT,sprintf('r6_pad%d.pdf',pad)), 'Padding', pad);
    exportgraphics(fig, fullfile(OUT,sprintf('r6_pad%d.png',pad)), 'Resolution',200,'Padding',pad);
    fprintf('Padding %d ok\n', pad);
  catch e
    fprintf('Padding %d RAISED %s: %s\n', pad, e.identifier, e.message);
  end
end
close(fig);

%% ---- r7 PaperPositionMode auto vs manual ----
disp('=== r7 PaperPositionMode ===');
fig = figure('Visible','off','Position',[100 100 631 260]);
set(fig,'PaperUnits','inches');
fprintf('initial PaperPositionMode = %s\n', get(fig,'PaperPositionMode'));
set(fig,'PaperPosition',[0 0 6.31 2.6]);
fprintf('after set PaperPosition, mode = %s\n', get(fig,'PaperPositionMode'));
ax=axes(fig); plot(ax,1:3,[1 2 3]);
set(fig,'PaperPositionMode','auto');
fprintf('after auto, PaperPosition = [%s]\n', num2str(get(fig,'PaperPosition')));
print(fig, fullfile(OUT,'r7_auto_pr.pdf'), '-dpdf');
print(fig, fullfile(OUT,'r7_auto_pr.png'), '-dpng','-r200');
close(fig);
disp('=== probe_d done ===');
