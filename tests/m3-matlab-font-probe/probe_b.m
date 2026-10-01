% probe_b.m -- RUN AFTER the user-level font install. Reads state, exports PDFs.
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_b.m')" > build/m3-matlab-font/raw_probe_b.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_b');
if ~exist(OUT,'dir'); mkdir(OUT); end

fprintf('=== C0 env ===\n');
fprintf('version = %s\n', version);

fprintf('\n=== C1 listfonts after user-level install (NEW session) ===\n');
lf = listfonts;
fprintf('listfonts count = %d\n', numel(lf));
fid = fopen(fullfile(OUT,'listfonts_probe_b_after.txt'),'wb');
for i=1:numel(lf); fprintf(fid,'%s\n', lf{i}); end
fclose(fid);
fprintf('wrote listfonts_probe_b_after.txt\n');
for nm = {'TeXGyreTermesX','TeX Gyre TermesX','TeXGyreTermes','TeXGyreTermesX Bold','Times New Roman'}
  fprintf('  exact [%s] = %d\n', nm{1}, sum(strcmp(lf,nm{1})));
end
hit = lf(contains(lf,'Termes'));
fprintf('  contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));

fprintf('\n=== C2 the Java source listfonts.m uses ===\n');
try
  fl = com.mathworks.mwswing.FontUtils.getFontNames;
  fprintf('FontUtils.getFontNames size = %d\n', fl.size());
  arr = cell(fl.toArray());
  fprintf('  has TeXGyreTermesX = %d ; has TeX Gyre TermesX = %d\n', ...
      sum(strcmp(arr,'TeXGyreTermesX')), sum(strcmp(arr,'TeX Gyre TermesX')));
  hit = arr(contains(arr,'Termes'));
  fprintf('  contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));
catch ME
  fprintf('C2 ERR: %s : %s\n', ME.identifier, ME.message);
end
try
  ge = java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment();
  fam = cell(ge.getAvailableFontFamilyNames());
  fprintf('java.awt families count = %d ; has TeXGyreTermesX = %d ; has TeX Gyre TermesX = %d\n', ...
      numel(fam), sum(strcmp(fam,'TeXGyreTermesX')), sum(strcmp(fam,'TeX Gyre TermesX')));
catch ME
  fprintf('C2 java ERR: %s\n', ME.message);
end

fprintf('\n=== C3 end-to-end: does HG actually embed it? ===\n');
specs = {
  'texgyre_regular',    'TeXGyreTermesX',  'normal', 'normal'
  'texgyre_bold',       'TeXGyreTermesX',  'bold',   'normal'
  'texgyre_italic',     'TeXGyreTermesX',  'normal', 'italic'
  'texgyre_bolditalic', 'TeXGyreTermesX',  'bold',   'italic'
  'texgyre_spaced',     'TeX Gyre TermesX','normal', 'normal'
  'times_control',      'Times New Roman', 'normal', 'normal'
};
for i=1:size(specs,1)
  tag=specs{i,1}; fn=specs{i,2}; fw=specs{i,3}; fa=specs{i,4};
  try
    f = figure('Visible','off','Position',[100 100 630 260]);
    ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
    set(ax,'FontName',fn,'FontWeight',fw,'FontAngle',fa,'FontSize',12);
    title(ax,['FontName=' fn ' weight=' fw ' angle=' fa],'Interpreter','none');
    xlabel(ax,'t'); ylabel(ax,'y');
    lastwarn('');
    exportgraphics(f, fullfile(OUT,[tag '.pdf']));
    [msg,id] = lastwarn;
    fprintf('C3 %-20s FontName=%-18s w=%-6s a=%-6s lastwarn id=[%s]\n', tag, fn, fw, fa, id);
    close(f);
  catch ME
    fprintf('C3 ERR %s: %s : %s\n', tag, ME.identifier, ME.message);
  end
end

fprintf('\n=== C4 same font via print -dpdf and exportgraphics PNG ===\n');
try
  f = figure('Visible','off','Position',[100 100 630 260]);
  ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
  set(ax,'FontName','TeXGyreTermesX','FontSize',12);
  title(ax,'TeXGyreTermesX print -dpdf'); xlabel(ax,'t');
  print(f, fullfile(OUT,'texgyre_print_dpdf.pdf'), '-dpdf');
  exportgraphics(f, fullfile(OUT,'texgyre_eg.png'), 'Resolution', 200);
  fprintf('C4 wrote print -dpdf and PNG\n');
  close(f);
catch ME
  fprintf('C4 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== C-END ===\n');
