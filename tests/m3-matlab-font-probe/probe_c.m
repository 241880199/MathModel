% probe_c.m -- RUN AFTER the rollback: is the machine back to the pre-install state?
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_c.m')" > build/m3-matlab-font/raw_probe_c.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_c');
if ~exist(OUT,'dir'); mkdir(OUT); end

fprintf('=== D1 listfonts after rollback (NEW session) ===\n');
lf = listfonts;
fprintf('listfonts count = %d\n', numel(lf));
fid = fopen(fullfile(OUT,'listfonts_probe_c_afterrollback.txt'),'wb');
for i=1:numel(lf); fprintf(fid,'%s\n', lf{i}); end
fclose(fid);
fprintf('wrote listfonts_probe_c_afterrollback.txt\n');
hit = lf(contains(lf,'Termes'));
fprintf('  contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));
fprintf('  exact TeXGyreTermesX = %d\n', sum(strcmp(lf,'TeXGyreTermesX')));

fprintf('\n=== D2 request the font anyway: where does it land? ===\n');
try
  f = figure('Visible','off','Position',[100 100 630 260]);
  ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
  set(ax,'FontName','TeXGyreTermesX','FontSize',12);
  title(ax,'after rollback TeXGyreTermesX','Interpreter','none'); xlabel(ax,'t');
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'afterrollback_texgyre.pdf'));
  [msg,id] = lastwarn;
  fprintf('D2 export lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('D2 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== D-END ===\n');
