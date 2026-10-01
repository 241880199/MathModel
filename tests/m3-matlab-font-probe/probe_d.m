% probe_d.m -- post-install, registry value name = "<Family> (TrueType)".
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_d.m')" > build/m3-matlab-font/raw_probe_d.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_d');
if ~exist(OUT,'dir'); mkdir(OUT); end

fprintf('=== G1 listfonts with value name = <Family> (TrueType) ===\n');
lf = listfonts;
fprintf('listfonts count = %d\n', numel(lf));
fid = fopen(fullfile(OUT,'listfonts_probe_d.txt'),'wb');
for i=1:numel(lf); fprintf(fid,'%s\n', lf{i}); end
fclose(fid);
hit = lf(contains(lf,'Termes'));
fprintf('contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));
hit2 = lf(contains(lf,'Gyre'));
fprintf('contains Gyre n=%d {%s}\n', numel(hit2), strjoin(hit2,', '));
for nm = {'TeXGyreTermesX','TeXGyreTermesX Bold','TeXGyreTermesX Italic','TeXGyreTermesX Bold Italic'}
  fprintf('  exact [%s] = %d\n', nm{1}, sum(strcmp(lf,nm{1})));
end
fl = pf.fonts.getInstalledFontList(); pn = {fl.font_name};
fprintf('pf.fonts = %d ; contains Termes n=%d {%s}\n', numel(fl), ...
    sum(contains(pn,'Termes')), strjoin(pn(contains(pn,'Termes')),', '));

fprintf('\n=== G2 end-to-end embed test ===\n');
specs = {
  'texgyre_regular',    'TeXGyreTermesX',  'normal', 'normal'
  'texgyre_bold',       'TeXGyreTermesX',  'bold',   'normal'
  'texgyre_italic',     'TeXGyreTermesX',  'normal', 'italic'
  'texgyre_bolditalic', 'TeXGyreTermesX',  'bold',   'italic'
  'texgyre_spaced',     'TeX Gyre TermesX','normal', 'normal'
  'times_control',      'Times New Roman', 'normal', 'normal'
  'arial_control',      'Arial',           'normal', 'normal'
};
for i=1:size(specs,1)
  tag=specs{i,1}; fn=specs{i,2}; fw=specs{i,3}; fa=specs{i,4};
  try
    f = figure('Visible','off','Position',[100 100 630 260]);
    ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
    set(ax,'FontName',fn,'FontWeight',fw,'FontAngle',fa,'FontSize',12);
    title(ax,['FontName=' fn ' w=' fw ' a=' fa],'Interpreter','none');
    xlabel(ax,'t'); ylabel(ax,'y');
    lastwarn('');
    exportgraphics(f, fullfile(OUT,[tag '.pdf']));
    [msg,id] = lastwarn;
    fprintf('G2 %-20s FontName=%-18s w=%-6s a=%-6s lastwarn id=[%s]\n', tag, fn, fw, fa, id);
    close(f);
  catch ME
    fprintf('G2 ERR %s: %s : %s\n', tag, ME.identifier, ME.message);
  end
end

fprintf('\n=== G3 print -dpdf variant ===\n');
try
  f = figure('Visible','off','Position',[100 100 630 260]);
  ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
  set(ax,'FontName','TeXGyreTermesX','FontSize',12);
  title(ax,'TeXGyreTermesX print -dpdf','Interpreter','none'); xlabel(ax,'t');
  print(f, fullfile(OUT,'texgyre_print_dpdf.pdf'), '-dpdf');
  fprintf('G3 wrote print -dpdf\n');
  close(f);
catch ME
  fprintf('G3 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== G4 value pointing at a file OUTSIDE any font directory ===\n');
lf = listfonts;
fprintf('  listfonts has McmOutOfDirProbe = %d\n', sum(strcmp(lf,'McmOutOfDirProbe')));
hit = lf(contains(lf,'OutOfDir'));
fprintf('  listfonts contains OutOfDir n=%d {%s}\n', numel(hit), strjoin(hit,', '));
pn = {pf.fonts.getInstalledFontList().font_name};
fprintf('  pf.fonts has McmOutOfDirProbe = %d\n', sum(strcmp(pn,'McmOutOfDirProbe')));

fprintf('\n=== G-END ===\n');
