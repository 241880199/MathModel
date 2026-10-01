% probe_f.m --- M3 matlab recon: palette-trigger refinement + end-to-end scenarios + RED R1/R2/R3
% re-run:  d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_f.m')"
here = fileparts(mfilename('fullpath')); root = fileparts(fileparts(here)); cd(root);
OUT = 'build/m3-matlab-recon/f';
if ~exist(OUT,'dir'); mkdir(OUT); end
fprintf('### probe_f start ###\n');

function snap(tag)
  co = get(groot,'DefaultAxesColorOrder'); L = lines(7); fc = get(groot,'defaultFigureColor');
  fprintf('[%s] co1=#%02X%02X%02X lines1=#%02X%02X%02X figColor=#%02X%02X%02X\n', tag, ...
     round(255*co(1,1)),round(255*co(1,2)),round(255*co(1,3)), ...
     round(255*L(1,1)),round(255*L(1,2)),round(255*L(1,3)), ...
     round(255*fc(1)),round(255*fc(2)),round(255*fc(3)));
end

%% ===== s1: trigger refinement -- FIRST export is `print`, not `exportgraphics` =====
disp('=== s1 first export = print (png) ===');
snap('s1-before-any-export');
f = figure('Visible','off','Position',[100 100 631 260]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(f); x=linspace(0,2*pi,200); plot(ax,x,sin(x)); xlabel(ax,'t');
print(f, fullfile(OUT,'s1_print_first.png'), '-dpng','-r200');
snap('s1-after-print-png');

%% ===== s2: end-to-end COMPLIANT figure =====
disp('=== s2 compliant figure ===');
PAL = [0 0.4470 0.7410; 0.8500 0.3250 0.0980];
f = figure('Visible','off','Position',[100 100 631 260]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 2.6]);
ax = axes(f); hold(ax,'on');
plot(ax, x, sin(x),   'Color',PAL(1,:), 'LineWidth',1.0);
plot(ax, x, cos(x),   'Color',PAL(2,:), 'LineWidth',1.0);
hold(ax,'off'); xlabel(ax,'t'); ylabel(ax,'y');
exportgraphics(f, fullfile(OUT,'s2_good.png'), 'Resolution',200);
exportgraphics(f, fullfile(OUT,'s2_good.pdf'));
print(f, fullfile(OUT,'s2_good_pr.png'), '-dpng','-r200');
print(f, fullfile(OUT,'s2_good_pr.pdf'), '-dpdf');
saveas(f, fullfile(OUT,'s2_good_sa.png'));
saveas(f, fullfile(OUT,'s2_good_sa.pdf'));
fid=fopen(fullfile(OUT,'s2_caption.txt'),'wb'); fprintf(fid,'Figure 1: Two sample series\n'); fclose(fid);
fid=fopen(fullfile(OUT,'s2_caption_bad.txt'),'wb'); fprintf(fid,'Figure 1. This figure shows the two sample series under baseline conditions for the study area.\n'); fclose(fid);
close(f);

%% ===== s3: end-to-end VIOLATING figure (6 default series, wide) =====
disp('=== s3 violating figure ===');
f = figure('Visible','off','Position',[100 100 1200 260]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 12.0 2.6]);
ax = axes(f); hold(ax,'on');
for k=1:6; plot(ax, x, sin(x*k/3), 'LineWidth',1.0); end
hold(ax,'off'); xlabel(ax,'t'); ylabel(ax,'y');
exportgraphics(f, fullfile(OUT,'s3_bad.png'), 'Resolution',200);
exportgraphics(f, fullfile(OUT,'s3_bad.pdf'));
print(f, fullfile(OUT,'s3_bad_pr.png'), '-dpng','-r200');
print(f, fullfile(OUT,'s3_bad_pr.pdf'), '-dpdf');
close(f);

%% ===== s4: RED R1 -- stacked composition bar =====
disp('=== s4 R1 stacked bar ===');
low  = [0.42 0.31 0.55 0.28 0.37 0.50];
med  = [0.35 0.44 0.30 0.47 0.38 0.33];
high = [0.23 0.25 0.15 0.25 0.25 0.17];
D = [low; med; high]';
f = figure('Visible','off','Position',[100 100 631 320]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 3.2]);
ax = axes(f);
b = bar(ax, D, 'stacked');
b(1).FaceColor = [0.66 0.80 0.90]; b(2).FaceColor = [0.55 0.71 0.85]; b(3).FaceColor = [0.30 0.45 0.65];
set(ax,'XTickLabel',{'A','B','C','D','E','F'});
xlabel(ax,'District'); ylabel(ax,'Share of area'); ylim(ax,[0 1]);
exportgraphics(f, fullfile(OUT,'s4_R1.png'), 'Resolution',200);
exportgraphics(f, fullfile(OUT,'s4_R1.pdf'));
fid=fopen(fullfile(OUT,'s4_R1_caption.txt'),'wb'); fprintf(fid,'Figure 1: Vulnerability composition by district\n'); fclose(fid);
close(f);

%% ===== s5: RED R2 -- |correlation| horizontal bars =====
disp('=== s5 R2 corr bars ===');
pop=[820 640 610 1210 990 1750]; slope=[3.2 11.5 2.4 14.8 7.1 5.0];
veg=[0.61 0.58 0.72 0.41 0.49 0.55]; dis=[12 31 8 38 16 24]; infra=[74 72 81 55 66 70];
names={'Pop. density','Mean slope','Vegetation','Infrastructure'};
X=[pop;slope;veg;infra]';
r=zeros(1,4); for k=1:4; C=corrcoef(X(:,k),dis); r(k)=C(1,2); end
fprintf('R2 correlations: '); fprintf('%s=%.4f ', names{:}, r); fprintf('\n');
f = figure('Visible','off','Position',[100 100 631 320]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 3.2]);
ax=axes(f); barh(ax, abs(r), 'FaceColor',[0.30 0.45 0.65]);
set(ax,'YTickLabel',names); xlabel(ax,'|Pearson r| with historical disaster count');
exportgraphics(f, fullfile(OUT,'s5_R2.png'), 'Resolution',200);
exportgraphics(f, fullfile(OUT,'s5_R2.pdf'));
fid=fopen(fullfile(OUT,'s5_R2_caption.txt'),'wb'); fprintf(fid,'Figure 1: Correlation of each factor with disaster count\n'); fclose(fid);
close(f);

%% ===== s6: RED R3 -- same as R1, delivery form (one page) =====
disp('=== s6 R3 delivery ===');
f = figure('Visible','off','Position',[100 100 631 320]);
set(f,'PaperUnits','inches'); set(f,'PaperPosition',[0 0 6.31 3.2]);
ax = axes(f); b = bar(ax, D, 'stacked');
b(1).FaceColor=[0.66 0.80 0.90]; b(2).FaceColor=[0.55 0.71 0.85]; b(3).FaceColor=[0.30 0.45 0.65];
set(ax,'XTickLabel',{'A','B','C','D','E','F'}); xlabel(ax,'District'); ylabel(ax,'Share of area'); ylim(ax,[0 1]);
exportgraphics(f, fullfile(OUT,'s6_R3.pdf'));
print(f, fullfile(OUT,'s6_R3_pr.pdf'), '-dpdf');
exportgraphics(f, fullfile(OUT,'s6_R3.png'), 'Resolution',200);
close(f);

%% ===== s7: MATLAB-readable corpus data =====
disp('=== s7 corpus data read ===');
for p = {'corpus/algorithms/src/FuzzyMathematicalModel模糊数学模型/模糊聚类/data1.mat'}
  try
    S = load(p{1});
    fn = fieldnames(S);
    fprintf('load OK: %s fields=%s\n', p{1}, strjoin(fn',','));
    for k=1:numel(fn)
      v = S.(fn{k}); fprintf('  %s size=[%s] class=%s\n', fn{k}, num2str(size(v)), class(v));
    end
  catch e
    fprintf('load RAISED %s: %s\n', p{1}, e.identifier, e.message);
  end
end
try
  T = readtable('corpus/官方原题/2026/2026_MCM_Problem_C_Data.csv');
  fprintf('readtable csv OK rows=%d vars=%d\n', height(T), width(T));
catch e
  fprintf('readtable csv RAISED: %s\n', e.message);
end
try
  T2 = readtable('corpus/官方原题/2017/2017_MCM_Problem_C_Data.xlsx');
  fprintf('readtable xlsx OK rows=%d vars=%d\n', height(T2), width(T2));
catch e
  fprintf('readtable xlsx RAISED: %s\n', e.message);
end
snap('s-end');
disp('=== probe_f done ===');
