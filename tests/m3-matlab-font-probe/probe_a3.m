% probe_a3.m -- no-install route exploration: the pf.fonts API surface. NO system change.
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
