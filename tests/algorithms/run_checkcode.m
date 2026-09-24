function run_checkcode(rootDir, outFile)
% RUN_CHECKCODE  Static analysis (mlint) of every .m file under rootDir.
%
%   Does NOT execute anything -- safe to point at untrusted trees.
%   Writes a TAB-separated report: <relpath>\t<line>\t<id>\t<message>
%   and a trailing "# scanned=N filesWithIssues=M messages=K" line.
%
%   Usage:  matlab -batch "run_checkcode('D:\path\to\src', 'out.txt')"

    rootDir = char(rootDir);
    outFile = char(outFile);

    files = dir(fullfile(rootDir, '**', '*.m'));
    fid = fopen(outFile, 'w', 'n', 'UTF-8');
    if fid < 0
        error('run_checkcode:cannotOpen', 'Cannot write %s', outFile);
    end

    nScanned = 0;
    nWithIssues = 0;
    nMessages = 0;

    for i = 1:numel(files)
        full = fullfile(files(i).folder, files(i).name);
        rel = strrep(full, [rootDir filesep], '');
        nScanned = nScanned + 1;

        msgs = [];
        try
            msgs = checkcode(full, '-id');
        catch err
            fprintf(fid, '%s\t0\trun_checkcode:error\t%s\n', rel, oneLine(err.message));
            nWithIssues = nWithIssues + 1;
            nMessages = nMessages + 1;
            continue
        end

        if ~isempty(msgs)
            nWithIssues = nWithIssues + 1;
            for k = 1:numel(msgs)
                if isfield(msgs, 'id') && ~isempty(msgs(k).id)
                    id = msgs(k).id;
                else
                    id = '(noid)';
                end
                fprintf(fid, '%s\t%d\t%s\t%s\n', rel, msgs(k).line, id, oneLine(msgs(k).message));
                nMessages = nMessages + 1;
            end
        end
    end

    fprintf(fid, '# scanned=%d filesWithIssues=%d messages=%d\n', nScanned, nWithIssues, nMessages);
    fclose(fid);

    fprintf('scanned=%d filesWithIssues=%d messages=%d\n', nScanned, nWithIssues, nMessages);
end

function s = oneLine(s)
% Flatten a message to a single TAB-free, newline-free line.
    s = char(s);
    s = strrep(s, sprintf('\r\n'), ' ');
    s = strrep(s, sprintf('\n'), ' ');
    s = strrep(s, sprintf('\t'), ' ');
    s = strtrim(s);
end
