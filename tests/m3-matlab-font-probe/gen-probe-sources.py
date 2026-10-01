#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Write the MATLAB/header probe sources with LF endings.

Why a generator: this repo requires the probe sources to be byte-exact LF
(see tests/m3-matlab-recon/README.md "byte discipline").  Writing them from
Python with Path.write_bytes guarantees no CR is introduced by an editor or by
the shell on Windows.

Run:
    python tests/m3-matlab-font-probe/gen-probe-sources.py

It writes, relative to the repo root discovered from this file:
    build/m3-matlab-font/gdi32mini.h
    tests/m3-matlab-font-probe/probe_a.m   (font-source discovery; NO system change)
    tests/m3-matlab-font-probe/probe_a2.m  (pre-install baselines; NO system change)
    tests/m3-matlab-font-probe/probe_b.m   (run AFTER the user-level font install)
    tests/m3-matlab-font-probe/probe_c.m   (run AFTER the rollback))
and prints the byte size + CR count of each.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BUILD = ROOT / "build" / "m3-matlab-font"

GDI32MINI_H = """/* gdi32mini.h -- minimal gdi32 prototypes for MATLAB loadlibrary (probe only).
   Regenerate: python tests/m3-matlab-font-probe/gen-probe-sources.py (LF). */
#define FR_PRIVATE 0x10
int AddFontResourceExA(char *name, unsigned long fl, void *res);
int RemoveFontResourceExA(char *name, unsigned long fl, void *res);
unsigned long AddFontMemResourceEx(void *pb, unsigned long cb, void *pv, unsigned long *pc);
int RemoveFontMemResourceEx(void *h);
"""

PROBE_A = r"""% probe_a.m -- MATLAB font-source discovery. NO system fonts are installed by this probe.
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
"""


PROBE_A2 = r"""% probe_a2.m -- PRE-install baselines. NO system fonts are installed by this probe.
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
"""

PROBE_B = r"""% probe_b.m -- RUN AFTER the user-level font install. Reads state, exports PDFs.
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
"""

PROBE_C = r"""% probe_c.m -- RUN AFTER the rollback: is the machine back to the pre-install state?
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
"""


PROBE_A3 = r"""% probe_a3.m -- no-install route exploration: the pf.fonts API surface. NO system change.
% Recreate sources: python tests/m3-matlab-font-probe/gen-probe-sources.py
% Regenerate evidence: d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a3.m')" > build/m3-matlab-font/raw_probe_a3.txt 2>&1
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
cd(root);
OUT = fullfile(root,'build','m3-matlab-font','probe_a3');
if ~exist(OUT,'dir'); mkdir(OUT); end

fprintf('=== E1 decaf flag (decides which branch listfonts takes) ===\n');
fprintf('DialogUtils.checkDecaf = %d\n', matlab.ui.internal.dialog.DialogUtils.checkDecaf);
fprintf('usejava awt = %d\n', usejava('awt'));

fprintf('\n=== E2 pf namespace: is it a MATLAB class? ===\n');
try
  wa = which('pf','-all');
  fprintf('which pf -all n=%d\n', numel(wa));
  for i=1:numel(wa); fprintf('  [%d] %s\n', i, wa{i}); end
catch ME
  fprintf('which pf ERR: %s\n', ME.message);
end
try
  mm = methods('pf.fonts');
  fprintf('methods(pf.fonts) n=%d\n', numel(mm));
  for i=1:numel(mm); fprintf('  %s\n', mm{i}); end
catch ME
  fprintf('methods(pf.fonts) ERR: %s : %s\n', ME.identifier, ME.message);
end
try
  mc = meta.class.fromName('pf.fonts');
  if isempty(mc)
    fprintf('meta.class pf.fonts = EMPTY\n');
  else
    fprintf('meta.class pf.fonts name = %s, methods n=%d\n', mc.Name, numel(mc.MethodList));
    for i=1:numel(mc.MethodList); fprintf('  m: %s\n', mc.MethodList(i).Name); end
  end
catch ME
  fprintf('meta ERR: %s\n', ME.message);
end

fprintf('\n=== E3 pf.fonts.getInstalledFontList payload ===\n');
try
  fl = pf.fonts.getInstalledFontList();
  fprintf('class = %s  numel = %d\n', class(fl), numel(fl));
  fprintf('fields = %s\n', strjoin(fieldnames(fl), ','));
  for i=1:min(3,numel(fl))
    fprintf('  [%d].font_name = %s\n', i, fl(i).font_name);
  end
  nm = {fl.font_name};
  fprintf('contains Termes n=%d\n', sum(contains(nm,'Termes')));
  fprintf('has yyb=%d  萝莉体 第二版=%d  字语康宋体=%d\n', ...
      sum(strcmp(nm,'yyb')), sum(strcmp(nm,'萝莉体 第二版')), sum(strcmp(nm,'字语康宋体')));
catch ME
  fprintf('E3 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== E4 try any add/install/refresh entry points that exist ===\n');
cands = {'addFont','addFonts','addFontFile','installFont','installFonts','registerFont', ...
         'setFontPath','addFontFolder','addFontDir','loadFont','refresh','rehash','reset'};
for i=1:numel(cands)
  fn = ['pf.fonts.' cands{i}];
  try
    ex = exist(fn);
    ex2 = exist(fn,'file');
    fprintf('  exist(%s) = %d (file=%d)\n', fn, ex, ex2);
  catch ME
    fprintf('  exist(%s) ERR: %s\n', fn, ME.message);
  end
end

fprintf('\n=== E5 java properties whose key mentions font ===\n');
try
  p = java.lang.System.getProperties();
  en = p.propertyNames(); nm = {};
  while en.hasMoreElements()
    x = en.nextElement(); nm{end+1} = char(x.toString());
  end
  hit = nm(contains(lower(nm),'font'));
  fprintf('java props containing font: n=%d {%s}\n', numel(hit), strjoin(hit,','));
  for i=1:numel(hit); fprintf('  %s = %s\n', hit{i}, char(p.getProperty(hit{i}))); end
catch ME
  fprintf('E5 ERR: %s : %s\n', ME.identifier, ME.message);
end

fprintf('\n=== E6 other font-ish namespaces on the path ===\n');
for pkg = {'matlab.fonts','matlab.internal.font','matlab.internal.fonts','matlab.ui.internal.font'}
  try
    mm = methods(pkg{1});
    fprintf('  methods(%s) n=%d {%s}\n', pkg{1}, numel(mm), strjoin(mm,','));
  catch ME
    fprintf('  methods(%s) ERR: %s\n', pkg{1}, ME.message);
  end
end

fprintf('\n=== E-END ===\n');
"""


PROBE_D = r"""% probe_d.m -- post-install, registry value name = "<Family> (TrueType)".
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
"""


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def main() -> None:
    targets = [
        (BUILD / "gdi32mini.h", GDI32MINI_H),
        (HERE / "probe_a.m", PROBE_A),
        (HERE / "probe_a2.m", PROBE_A2),
        (HERE / "probe_a3.m", PROBE_A3),
        (HERE / "probe_b.m", PROBE_B),
        (HERE / "probe_c.m", PROBE_C),
        (HERE / "probe_d.m", PROBE_D),
    ]
    for path, text in targets:
        write_lf(path, text)
        raw = path.read_bytes()
        print("wrote %s  %d B  CR=%d" % (path, len(raw), raw.count(b"\r")))


if __name__ == "__main__":
    main()
