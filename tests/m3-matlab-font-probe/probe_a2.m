% probe_a2.m -- PRE-install baselines. NO system fonts are installed by this probe.
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a2.m')" > build/m3-matlab-font/raw_probe_a2.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_a2');
if ~exist(OUT,'dir'); mkdir(OUT); end

fprintf('=== B0 env ===\n');
fprintf('version    = %s\n', version);
fprintf('matlabroot = %s\n', matlabroot);

fprintf('\n=== B1 the exact Java call listfonts.m makes ===\n');
try
  fl = com.mathworks.mwswing.FontUtils.getFontNames;
  fprintf('FontUtils.getFontNames size = %d\n', fl.size());
  arr = cell(fl.toArray());
  fprintf('  has TeXGyreTermesX = %d\n', sum(strcmp(arr,'TeXGyreTermesX')));
  fprintf('  has TeX Gyre TermesX = %d\n', sum(strcmp(arr,'TeX Gyre TermesX')));
  fprintf('  has yyb = %d ; has 萝莉体 第二版 = %d ; has 字语康宋体 = %d\n', ...
      sum(strcmp(arr,'yyb')), sum(strcmp(arr,'萝莉体 第二版')), sum(strcmp(arr,'字语康宋体')));
  fid = fopen(fullfile(OUT,'FontUtils_getFontNames.txt'),'wb');
  for i=1:numel(arr); fprintf(fid,'%s\n', arr{i}); end
  fclose(fid);
  fprintf('  wrote FontUtils_getFontNames.txt\n');
catch ME
  fprintf('B1 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== B1b decaf / java properties / prefs ===\n');
try
  fprintf('DialogUtils.checkDecaf = %d\n', matlab.ui.internal.dialog.DialogUtils.checkDecaf);
catch ME
  fprintf('decaf ERR: %s\n', ME.message);
end
try
  p = java.lang.System.getProperties();
  nm = cell(p.stringPropertyNames());
  hit = nm(contains(lower(nm),'font'));
  fprintf('java properties whose key contains font: n=%d {%s}\n', numel(hit), strjoin(hit,','));
  for i=1:numel(hit); fprintf('  %s = %s\n', hit{i}, char(p.getProperty(hit{i}))); end
catch ME
  fprintf('props ERR: %s\n', ME.message);
end
try
  g = getpref('MathWorks_MATLAB');
  fprintf('getpref(MathWorks_MATLAB) = %s\n', class(g));
catch ME
  fprintf('getpref(MathWorks_MATLAB) ERR: %s\n', ME.message);
end

fprintf('\n=== B2 latex interpreter, clean (no \mathsf) ===\n');
try
  f = figure('Visible','off','Position',[100 100 630 200]);
  ax = axes(f); axis(ax,[0 1 0 1]); axis(ax,'off');
  text(ax,0.02,0.62,'$\alpha\beta\gamma=\int_0^1 x\,dx$','Interpreter','latex','FontSize',13);
  text(ax,0.02,0.22,'$\Phi\Psi\Omega$ plain Arial','Interpreter','latex','FontSize',13);
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'B2_latex_clean.pdf'));
  [msg,id] = lastwarn;
  fprintf('B2 latex-clean lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('B2 ERR: %s : %s\n', ME.identifier, ME.message);
end
try
  f = figure('Visible','off','Position',[100 100 630 260]);
  ax = axes(f); plot(ax,1:5,(1:5).^2,'LineWidth',1.2);
  set(ax,'TickLabelInterpreter','latex'); xlabel(ax,'$t$','Interpreter','latex');
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'B2_ticklatex.pdf'));
  [msg,id] = lastwarn;
  fprintf('B2 ticklatex lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('B2 tick ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== B3 PRE-EXISTING per-user fonts: end-to-end embed test ===\n');
pu = {'yyb','字语康宋体','萝莉体 第二版'};
for k=1:numel(pu)
  try
    f = figure('Visible','off','Position',[100 100 560 220]);
    ax = axes(f); plot(ax,1:6,(1:6).^2,'LineWidth',1.2);
    set(ax,'FontName',pu{k},'FontSize',12);
    title(ax,sprintf('puser %d',k),'Interpreter','none');
    lastwarn('');
    exportgraphics(f, fullfile(OUT,sprintf('B3_puser_%d.pdf',k)));
    [msg,id] = lastwarn;
    fprintf('B3 puser_%d name=[%s] lastwarn id=[%s]\n', k, pu{k}, id);
    close(f);
  catch ME
    fprintf('B3 ERR k=%d: %s : %s\n', k, ME.identifier, ME.message);
  end
end

fprintf('\n=== B-END ===\n');
