% probe_g.m --- M3 matlab recon: can print -dpdf be made to give a 6.31-in page box?
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_g.m')"
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/g';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_g start ###\n');
x = linspace(0,2*pi,200);

function f = fig631()
  f = figure('Visible','off','Position',[100 100 631 260]);
  set(f,'PaperUnits','inches');
  ax = axes(f); plot(ax, linspace(0,2*pi,200), sin(linspace(0,2*pi,200)));
  xlabel(ax,'t'); ylabel(ax,'y');
end

%% g1: PaperSize == paper width, PaperPosition full page, mode manual
disp('=== g1 PaperSize=[6.31 2.6] PaperPosition full page manual ===');
f = fig631();
set(f,'PaperPosition',[0 0 6.31 2.6]);
set(f,'PaperPositionMode','manual');
set(f,'PaperSize',[6.31 2.6]);
fprintf('PaperSize=[%s] PaperPosition=[%s] mode=%s\n', num2str(get(f,'PaperSize')), num2str(get(f,'PaperPosition')), get(f,'PaperPositionMode'));
print(f, fullfile(OUT,'g1_ps63_pr.pdf'), '-dpdf');
exportgraphics(f, fullfile(OUT,'g1_ps63_eg.pdf'));
exportgraphics(f, fullfile(OUT,'g1_ps63_eg.png'),'Resolution',200);
print(f, fullfile(OUT,'g1_ps63_pr.png'), '-dpng','-r200');
close(f);

%% g2: PaperSize == 6.31 wide, PaperPositionMode auto
disp('=== g2 PaperSize=[6.31 2.6] mode auto ===');
f = fig631();
set(f,'PaperSize',[6.31 2.6]);
set(f,'PaperPositionMode','auto');
fprintf('after auto: PaperPosition=[%s]\n', num2str(get(f,'PaperPosition')));
print(f, fullfile(OUT,'g2_auto_pr.pdf'), '-dpdf');
close(f);

%% g3: sane paper size but PaperPosition inset (letter page) -- control
disp('=== g3 control: A4 page, PaperPosition 6.31x2.6 ===');
f = fig631();
set(f,'PaperPosition',[0 0 6.31 2.6]);
set(f,'PaperPositionMode','manual');
print(f, fullfile(OUT,'g3_a4_pr.pdf'), '-dpdf');
close(f);

%% g4: does exportgraphics honour PaperSize at all?
disp('=== g4 exportgraphics vs PaperSize ===');
f = fig631(); set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 2.6]);
set(f,'PaperSize',[20 20]);
exportgraphics(f, fullfile(OUT,'g4_ps20_eg.pdf'));
close(f);

disp('=== probe_g done ===');
