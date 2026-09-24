function run_scripts(manifestFile, srcRoot, outFile)
% RUN_SCRIPTS  Execute every script listed in manifestFile, capture failures.
%
%   manifestFile : UTF-8 text, one path per line, relative to srcRoot.
%   srcRoot      : archive root (all of its subdirs are added to the path so
%                  sibling helper functions resolve).
%   outFile      : TSV report  <relpath>\t<status>\t<seconds>\t<message>
%                  status in {ok, fail, error}
%
%   Writes+flushes one line per script, so a hang still leaves partial evidence.
%
%   Usage: matlab -batch "run_scripts('manifest.txt','D:/.../src','out.txt')"

    manifestFile = char(manifestFile);
    srcRoot      = char(srcRoot);
    outFile      = char(outFile);

    % --- environment: no windows, no interactive pauses ----------------
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');

    % Everything on the path so main.m can call its sibling helpers.
    addpath(genpath(srcRoot));

    fid = fopen(manifestFile, 'r', 'n', 'UTF-8');
    if fid < 0, error('run_scripts:noManifest', 'cannot read %s', manifestFile); end
    raw = fread(fid, '*char')';
    fclose(fid);
    rels = regexp(raw, '\r\n|\n|\r', 'split');
    rels = rels(~cellfun(@isempty, strtrim(rels)));

    out = fopen(outFile, 'w', 'n', 'UTF-8');
    if out < 0, error('run_scripts:noReport', 'cannot write %s', outFile); end
    fprintf(out, '# status\tscript\tseconds\tmessage\n');

    startDir = pwd;
    nOk = 0; nFail = 0;

    for i = 1:numel(rels)
        rel  = strtrim(rels{i});
        full = fullfile(srcRoot, rel);
        [d, ~, ~] = fileparts(full);

        status = 'ok';
        msg    = '';
        t0 = tic;

        cleanup = onCleanup(@() cd(startDir));   %#ok<NASGU>
        try
            % Prepend the script's own dir so its local helpers win over
            % same-named ones elsewhere in the archive (there are many
            % main.m / func.m / fun.m). addpath prepends, so this takes
            % precedence over the genpath(srcRoot) fallback.
            addpath(d);
            cd(d);
            evalin('base', 'clear');             % isolate scripts from each other
            evalin('base', sprintf('run(''%s'')', strrep(full, '''', '''''')));
        catch err
            status = 'fail';
            if isfield(err, 'identifier') && ~isempty(err.identifier)
                msg = sprintf('%s: %s', err.identifier, err.message);
            else
                msg = err.message;
            end
        end
        clear cleanup;
        rmpath(d);
        cd(startDir);
        close all force;

        el = toc(t0);
        msg = flatten(msg);
        if strcmp(status, 'ok'), nOk = nOk + 1; else, nFail = nFail + 1; end
        fprintf(out, '%s\t%s\t%.2f\t%s\n', status, rel, el, msg);
        fseek(out, 0, 'cof');                     % flush; MATLAB has no fflush
        fprintf('%3d/%3d  %-6s %6.1fs  %s\n', i, numel(rels), status, el, rel);
    end

    fprintf(out, '# done ok=%d fail=%d total=%d\n', nOk, nFail, numel(rels));
    fclose(out);
    fprintf('\n完成: ok=%d fail=%d total=%d\n', nOk, nFail, numel(rels));
end

function s = flatten(s)
    s = char(s);
    s = strrep(s, sprintf('\r\n'), ' ');
    s = strrep(s, sprintf('\n'), ' ');
    s = strrep(s, sprintf('\t'), ' ');
    s = strtrim(s);
    if numel(s) > 300, s = [s(1:300) '...']; end
end
