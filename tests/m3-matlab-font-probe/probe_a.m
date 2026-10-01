% probe_a.m -- MATLAB font-source discovery. NO system fonts are installed by this probe.
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a.m')" > build/m3-matlab-font/raw_probe_a.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_a');
if ~exist(OUT,'dir'); mkdir(OUT); end
fontdir = fullfile(root,'.claude','skills','mcm-plot-python','assets','fonts');

fprintf('=== A0 env ===\n');
fprintf('version    = %s\n', version);
fprintf('matlabroot = %s\n', matlabroot);
fprintf('arch       = %s\n', computer('arch'));
fprintf('cwd        = %s\n', pwd);
fprintf('fontdir    = %s (exist=%d)\n', fontdir, exist(fontdir,'dir'));

names = {'TeXGyreTermesX','TeX Gyre TermesX','TeXGyreTermes','Times New Roman','Times','Nimbus Roman', ...
         'yyb','字语康宋体','萝莉体 第二版','Noto Sans SC','Source Han Serif SC Heavy'};

fprintf('\n=== A1 listfonts BEFORE any change ===\n');
lf = listfonts;
fprintf('listfonts count = %d\n', numel(lf));
fid = fopen(fullfile(OUT,'listfonts_probe_a_before.txt'),'wb');
for i=1:numel(lf); fprintf(fid,'%s\n', lf{i}); end
fclose(fid);
fprintf('wrote listfonts_probe_a_before.txt\n');
for k=1:numel(names)
  fprintf('  exact  [%s] = %d\n', names{k}, sum(strcmp(lf,names{k})));
end
subs = {'Termes','TeX','Gyre','yyb','萝莉','字语康'};
for k=1:numel(subs)
  hit = lf(contains(lf, subs{k}));
  fprintf('  contains [%s] : n=%d', subs{k}, numel(hit));
  if ~isempty(hit); fprintf(' -> {%s}', strjoin(hit,', ')); end
  fprintf('\n');
end

fprintf('\n=== A2 provenance of listfonts ===\n');
fprintf('exist(listfonts) = %d\n', exist('listfonts'));
wa = which('listfonts','-all');
for i=1:numel(wa); fprintf('which -all [%d] = %s\n', i, wa{i}); end

fprintf('\n=== A3 settings tree: matlab.fonts ===\n');
try
  s = settings;
  fprintf('settings root class = %s\n', class(s));
  g = s.matlab.fonts;
  fprintf('--- disp(s.matlab.fonts) ---\n');
  disp(g);
  fprintf('--- end disp ---\n');
catch ME
  fprintf('settings ERR: %s : %s\n', ME.identifier, ME.message);
end
try
  fprintf('-- probe known leaves --\n');
  s = settings;
  v = s.matlab.fonts.editor.code.Name.ActiveValue; fprintf('editor.code.Name = %s\n', v);
  v = s.matlab.fonts.editor.code.Size.ActiveValue; fprintf('editor.code.Size = %d\n', v);
  v = s.matlab.fonts.editor.normal.Name.ActiveValue; fprintf('editor.normal.Name = %s\n', v);
catch ME
  fprintf('known-leaf ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A4 environment (Java System.getenv) ===\n');
try
  env = java.lang.System.getenv();
  it = env.entrySet().iterator(); keys={}; vals={};
  while it.hasNext()
    e = it.next(); keys{end+1}=char(e.getKey()); vals{end+1}=char(e.getValue());
  end
  fprintf('env var count = %d\n', numel(keys));
  hk = keys(contains(upper(keys),'FONT'));
  fprintf('keys containing FONT: n=%d\n', numel(hk));
  for i=1:numel(hk)
    ix = find(strcmp(keys,hk{i}),1); fprintf('  %s = %s\n', hk{i}, vals{ix});
  end
  hk = keys(contains(upper(keys),'TEX'));
  fprintf('keys containing TEX: n=%d\n', numel(hk));
  for i=1:numel(hk)
    ix = find(strcmp(keys,hk{i}),1); fprintf('  %s = %s\n', hk{i}, vals{ix});
  end
  fprintf('getenv FONTCONFIG_FILE = [%s]\n', getenv('FONTCONFIG_FILE'));
  fprintf('getenv FONTCONFIG_PATH = [%s]\n', getenv('FONTCONFIG_PATH'));
catch ME
  fprintf('env ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A5 java.awt font enumeration (Java view) ===\n');
try
  ge = java.awt.GraphicsEnvironment.getLocalGraphicsEnvironment();
  fam = cell(ge.getAvailableFontFamilyNames());
  fprintf('java families count = %d\n', numel(fam));
  for k=1:numel(names)
    fprintf('  java exact [%s] = %d\n', names{k}, sum(strcmp(fam,names{k})));
  end
  hit = fam(contains(fam,'Termes'));
  fprintf('  java contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));
catch ME
  fprintf('java ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A6 GDI AddFontResourceExA(FR_PRIVATE) -- no-install route 3c ===\n');
hdr = fullfile(root,'build','m3-matlab-font','gdi32mini.h');
otf = fullfile(fontdir,'TeXGyreTermesX-Regular.otf');
tmpd = fullfile(root,'build','m3-matlab-font','tmpfont');
if ~exist(tmpd,'dir'); mkdir(tmpd); end
otfA = fullfile(tmpd,'TeXGyreTermesX-Regular.otf');
copyfile(otf, otfA);
fprintf('hdr exist=%d  ascii otf copy exist=%d\n', exist(hdr,'file'), exist(otfA,'file'));
try
  if libisloaded('gdi32'); unloadlibrary('gdi32'); end
  loadlibrary('gdi32', hdr, 'alias', 'gdi32');
  fprintf('loadlibrary(gdi32) ok\n');
  n1 = calllib('gdi32','AddFontResourceExA', otfA, 16, 0);
  fprintf('AddFontResourceExA(FR_PRIVATE) returned %d\n', n1);
catch ME
  fprintf('A6 ERR: %s : %s\n', ME.identifier, ME.message);
end
lf2 = listfonts;
fprintf('listfonts count after private-add = %d (before = %d)\n', numel(lf2), numel(lf));
fprintf('  after: exact TeXGyreTermesX = %d\n', sum(strcmp(lf2,'TeXGyreTermesX')));
fprintf('  after: exact TeX Gyre TermesX = %d\n', sum(strcmp(lf2,'TeX Gyre TermesX')));
hit = lf2(contains(lf2,'Termes'));
fprintf('  after: contains Termes n=%d {%s}\n', numel(hit), strjoin(hit,', '));
try
  f = figure('Visible','off','Position',[100 100 630 260]);
  ax = axes(f); plot(ax,1:10,(1:10).^2,'LineWidth',1.2);
  set(ax,'FontName','TeXGyreTermesX','FontSize',11);
  title(ax,'private-add TeXGyreTermesX'); xlim(ax,[0 10]);
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'A6_private_add.pdf'));
  [msg,id] = lastwarn;
  fprintf('A6 export lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('A6 export ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A7 latex text interpreter (no-install route 1) ===\n');
try
  f = figure('Visible','off','Position',[100 100 630 320]);
  ax = axes(f); axis(ax,[0 1 0 1]); axis(ax,'off');
  text(ax,0.02,0.88,'$\alpha\beta\gamma=\int_0^1 x\,dx$','Interpreter','latex','FontSize',13);
  text(ax,0.02,0.62,'$\mathrm{ABCdef}\ \mathsf{ABC}\ \mathtt{ABC}$','Interpreter','latex','FontSize',13);
  text(ax,0.02,0.36,'$\mathbf{ABC}$ plain ABCdef','Interpreter','latex','FontSize',13);
  text(ax,0.02,0.10,'$\Phi\Psi$ and roman','Interpreter','latex','FontSize',13, ...
       'FontName','TeXGyreTermesX');
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'A7_latex_interp.pdf'));
  [msg,id] = lastwarn;
  fprintf('A7 latex export lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('A7 ERR: %s : %s\n', ME.identifier, ME.message);
end
try
  f = figure('Visible','off','Position',[100 100 630 200]);
  ax = axes(f); axis(ax,[0 1 0 1]); axis(ax,'off');
  text(ax,0.02,0.5,'$\usepackage{newtxtext}\mathrm{ABC}$','Interpreter','latex','FontSize',13);
  lastwarn('');
  try
    exportgraphics(f, fullfile(OUT,'A7_latex_pkg.pdf'));
    fprintf('A7 usepackage: export ran\n');
  catch ME2
    fprintf('A7 usepackage export ERR: %s : %s\n', ME2.identifier, ME2.message);
  end
  [msg,id] = lastwarn;
  fprintf('A7 usepackage lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('A7 usepackage build ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A8 matlabroot/sys/fonts (read-only listing) ===\n');
try
  d = dir(fullfile(matlabroot,'sys','fonts'));
  fprintf('entries = %d\n', numel(d));
  for i=1:numel(d)
    if d(i).isdir
      fprintf('  [dir] %s\n', d(i).name);
    else
      fprintf('  %s  %d B\n', d(i).name, d(i).bytes);
    end
  end
  d2 = dir(fullfile(matlabroot,'sys','fonts','ttf'));
  fprintf('ttf entries = %d\n', numel(d2));
  for i=1:numel(d2); fprintf('  ttf/%s  %d B\n', d2(i).name, d2(i).bytes); end
catch ME
  fprintf('A8 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A9 control: set a nonexistent FontName silently? ===\n');
try
  f = figure('Visible','off','Position',[100 100 500 300]);
  ax = axes(f); plot(ax,1:10,1:10);
  set(ax,'FontName','NoSuchFontXYZ123');
  fprintf('get after set = [%s]\n', get(ax,'FontName'));
  lastwarn('');
  exportgraphics(f, fullfile(OUT,'A9_nosuchfont.pdf'));
  [msg,id] = lastwarn;
  fprintf('A9 lastwarn id=[%s] msg=[%s]\n', id, msg);
  close(f);
catch ME
  fprintf('A9 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== A10 addpath(fontdir) -- re-test of the recon claim ===\n');
n_before = numel(listfonts);
addpath(fontdir);
lf3 = listfonts;
fprintf('listfonts before addpath = %d ; after addpath = %d\n', n_before, numel(lf3));
fprintf('  after addpath: exact TeXGyreTermesX = %d ; contains Termes = %d\n', ...
    sum(strcmp(lf3,'TeXGyreTermesX')), sum(contains(lf3,'Termes')));
pp = strsplit(path, pathsep);
fprintf('  fontdir is on the MATLAB path now = %d\n', any(strcmp(pp, fontdir)));

fprintf('\n=== A-END ===\n');
