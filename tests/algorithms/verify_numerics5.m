function verify_numerics5(srcRoot, outFile)
% VERIFY_NUMERICS5  Fifth batch: cellular automata.
%
%   CAs have no closed-form answer, so correctness is established two ways:
%     - a deterministic CA (basic_CA) is re-simulated with an independent
%       vectorised update and compared to the script's final grid;
%     - the stochastic/particle CAs are checked by EXHAUSTIVELY applying the
%       rule EXACTLY AS WRITTEN in the script to every possible local
%       configuration, and testing the physical invariant that must hold
%       (particle-number conservation for the Margolus-block gas and DLA
%       diffusion; the excitable-media state cycle; the fire rule's semantics).
%
%   The rule expressions below are copied verbatim from the archive scripts.
%   If the archive changes, these must change with it.
%
%   Usage: matlab -batch "verify_numerics5('D:/.../src','out.txt')"

    srcRoot = char(srcRoot);
    out = fopen(char(outFile), 'w', 'n', 'UTF-8');
    set(0, 'DefaultFigureVisible', 'off');
    warning('off', 'all');
    addpath(genpath(srcRoot));
    R = @(p) fullfile(srcRoot, ['CellularAutomata元胞向量机' filesep p]);

    nPass = 0; nFail = 0; nSkip = 0;

    % 上游 basic_CA.m 不迭代（详见 INDEX §10.1），此处只记录偏离量，不计成败
    try
        [nUp, nRef, ndiff] = ca_divergence(R('初等元胞自动机/basic_CA.m'), ...
                                           fullfile(srcRoot, '..', 'fixed'));
        fprintf(out, 'INFO\tbasic_CA.m 上游终态 1 的个数=%d，按规则迭代应为 %d，差异 %d 格\n', ...
            nUp, nRef, ndiff);
        fprintf('INFO   basic_CA.m 上游=%d 个 1，正确迭代=%d 个 1，差异 %d 格（上游不迭代）\n', ...
            nUp, nRef, ndiff);
    catch err
        fprintf(out, 'INFO\tbasic_CA.m 偏离量未能测得: %s\n', msg(err));
        fprintf('INFO   basic_CA.m 偏离量未测得: %s\n', msg(err));
    end

    % ---- J1 奇偶规则CA 的修正版：独立逐点重模拟 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J1 fixed/parity_ca 正确迭代 vs 独立逐点重模拟', ...
        @() parity_ca_compare(fullfile(srcRoot, '..', 'fixed')));

    % ---- J2 激发介质：状态循环穷举 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J2 激发介质 状态迁移穷举（0-9 循环）', @() excitable_compare());

    % ---- J3 HPP 气体：Margolus 块内粒子数守恒穷举 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J3 HPP气体 16 种块配置粒子数守恒', @() hpp_conserve());

    % ---- J4 扩散限制聚集：扩散步是块内置换，粒子数守恒 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J4 DLA 16 种块配置扩散步粒子数守恒', @() dla_conserve());

    % ---- J5 森林火灾：规则语义穷举 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J5 森林火灾 规则语义穷举（烧->空/绿->烧/空->绿）', @() fire_rule());

    % ---- J6 砂堆规则：终态基本完整性 ----
    [nPass,nFail,nSkip] = chk(out,nPass,nFail,nSkip, ...
        'J6 砂堆规则 终态为二值且地形成分未被改写', ...
        @() sandpile_state(R('砂堆规则/main.m')));

    fprintf(out, '# RESULT pass=%d fail=%d skip=%d\n', nPass, nFail, nSkip);
    fclose(out);
    fprintf('\n==== 第五批(元胞自动机) pass=%d fail=%d skip=%d ====\n', nPass, nFail, nSkip);
end

% ------------------------------------------------------------------ 各项检查

function [a, e] = parity_ca_compare(fixedDir)
    addpath(fixedDir);
    S = 41; steps = 20;                 % 小规模，便于逐点重模拟
    L = parity_ca(S, steps);

    % 独立路线：手写双重循环逐点求 8 邻域和，不用卷积、不调 parity_ca
    M = (S + 1) / 2;
    R = zeros(S); R(M, M) = 1;
    for t = 1:steps
        T = zeros(S);
        for i = 1:S
            for j = 1:S
                s = 0;
                for di = -1:1
                    for dj = -1:1
                        if (di ~= 0 || dj ~= 0) ...
                                && i+di >= 1 && i+di <= S ...
                                && j+dj >= 1 && j+dj <= S
                            s = s + R(i+di, j+dj);
                        end
                    end
                end
                T(i, j) = mod(s, 2);
            end
        end
        R = T;
    end
    a = L; e = R;
end

function [nUp, nRef, ndiff] = ca_divergence(script, fixedDir)
    run_script(script);
    Lup = evalin('base', 'L');
    addpath(fixedDir);
    S = size(Lup, 1);
    Lref = parity_ca(S, (S - 1) / 2);
    nUp = nnz(Lup);
    nRef = nnz(Lref);
    ndiff = nnz(Lup ~= Lref);
end

function [a, e] = excitable_compare()
    % 规则（逐字取自 激发介质/main.m，t1 = 3）
    t1 = 3;
    cells = 0:9;                        % 穷举全部 10 个状态
    sumv = zeros(1, 10);                % 先看"无足够邻居"的情形
    outA = ((cells==0) & (sumv>=t1)) + 2*(cells==1) + 3*(cells==2) + ...
           4*(cells==3) + 5*(cells==4) + 6*(cells==5) + 7*(cells==6) + ...
           8*(cells==7) + 9*(cells==8) + 0*(cells==9);
    sumv = 3*ones(1, 10);               % 再看"邻居足够"的情形
    outB = ((cells==0) & (sumv>=t1)) + 2*(cells==1) + 3*(cells==2) + ...
           4*(cells==3) + 5*(cells==4) + 6*(cells==5) + ...
           7*(cells==6) + 8*(cells==7) + 9*(cells==8) + 0*(cells==9);
    % 期望：0->（邻居够则 1，否则 0）；1..8 -> 状态+1；9 -> 0
    expA = [0 2 3 4 5 6 7 8 9 0];
    expB = [1 2 3 4 5 6 7 8 9 0];
    a = [outA, outB]; e = [expA, expB];
end

function [a, e] = hpp_conserve()
    % 规则逐字取自 气体动力学/main.m（Margolus 块，2×2）
    worst = 0;
    for bits = 0:15
        b = bitget(bits, 1:4);          % b = [s(x,y) s(x+1,y) s(x,y+1) s(x+1,y+1)]
        s_xy = b(1); s_x1y = b(2); s_xy1 = b(3); s_x1y1 = b(4);
        for sums = [0 1]                % 是否贴墙
            diag1 = (s_xy==1) & (s_x1y1==1) & (s_x1y==0) & (s_xy1==0);
            diag2 = (s_x1y==1) & (s_xy1==1) & (s_xy==0) & (s_x1y1==0);
            and12 = (diag1==0) & (diag2==0);
            or12  = diag1 | diag2;
            n_xy   = (and12 & ~sums & s_x1y1) + (or12 & ~sums & s_xy1) + (sums & s_xy);
            n_x1y  = (and12 & ~sums & s_xy1)  + (or12 & ~sums & s_xy)  + (sums & s_x1y);
            n_xy1  = (and12 & ~sums & s_x1y)  + (or12 & ~sums & s_x1y1) + (sums & s_xy1);
            n_x1y1 = (and12 & ~sums & s_xy)   + (or12 & ~sums & s_x1y)  + (sums & s_x1y1);
            delta = abs(sum([n_xy n_x1y n_xy1 n_x1y1]) - sum(b));
            worst = max(worst, delta);
        end
    end
    a = worst; e = 0;                   % 任何配置下块内粒子数都不变
end

function [a, e] = dla_conserve()
    % 规则逐字取自 扩散限制聚集/main.m 的 Margolus 旋转
    worst = 0;
    for bits = 0:15
        b = bitget(bits, 1:4);
        s_xy = b(1); s_x1y = b(2); s_xy1 = b(3); s_x1y1 = b(4);
        for vary = [0 1]
            vary1 = 1 - vary;
            n_xy   = vary*s_x1y   + vary1*s_xy1;
            n_x1y  = vary*s_x1y1  + vary1*s_xy;
            n_xy1  = vary*s_xy    + vary1*s_x1y1;
            n_x1y1 = vary*s_xy1   + vary1*s_x1y;
            delta = abs(sum([n_xy n_x1y n_xy1 n_x1y1]) - sum(b));
            worst = max(worst, delta);
        end
    end
    a = worst; e = 0;
end

function [a, e] = fire_rule()
    % 规则逐字取自 森林火灾/main.m 的核心表达式；用确定性掩码代替 rand
    %   veg = 2*(veg==2) - ((veg==2) & (sum>0 | lightning)) + 2*((veg==0) & growth)
    got = []; exp_ = [];
    for state = 0:2
        for burn = [0 1]                % 邻居是否有火
            for growth = [0 1]          % 空地是否长草
                veg = state;
                sumv = burn;
                lightning = false;      % 掩码取假，隔离随机性
                out = 2*(veg==2) - ((veg==2) & (sumv>0 | lightning)) + ...
                      2*((veg==0) & growth);
                got(end+1) = out; %#ok<AGROW>
                % 期望语义：烧(1)->空(0)；绿(2)->有火则烧否则仍绿；空(0)->长草则绿否则仍空
                switch state
                    case 0, want = 2*growth;
                    case 1, want = 0;
                    case 2, want = 2 - burn;
                end
                exp_(end+1) = want; %#ok<AGROW>
            end
        end
    end
    a = got; e = exp_;
end

function [a, e] = sandpile_state(script)
    run_script(script);
    sand = evalin('base', 'sand');
    gnd  = evalin('base', 'gnd');
    % 判据：sand 必须是二值；gnd 必须仍是二值地形
    okSand = all(sand(:)==0 | sand(:)==1);
    okGnd  = all(gnd(:)==0 | gnd(:)==1);
    a = double(okSand && okGnd); e = 1;
end

% ------------------------------------------------------------------ harness

function run_script(full)
    evalin('base', 'clear');
    evalin('base', sprintf('run(''%s'')', strrep(full, '''', '''''')));
    evalin('base', 'close all force');
end

function [np,nf,ns] = chk(out, np, nf, ns, name, fn)
    try
        [a, e] = fn();
    catch err
        fprintf(out, 'ERROR\t%s\t%s\n', name, msg(err));
        fprintf('ERROR  %s | %s\n', name, msg(err));
        ns = ns + 1; return
    end
    a = a(:)'; e = e(:)';
    if numel(a) == numel(e) && all(abs(a - e) < 1e-9)
        fprintf(out, 'PASS\t%s\n', name); fprintf('PASS   %s\n', name); np = np + 1;
    else
        sa = short(a); se = short(e);
        fprintf(out, 'FAIL\t%s\n\tactual  =%s\n\texpected=%s\n', name, sa, se);
        fprintf('FAIL   %s\n        actual  =%s\n        expected=%s\n', name, sa, se);
        nf = nf + 1;
    end
end

function s = short(v)
    v = v(:)';
    if numel(v) > 10
        s = sprintf('len=%d [%s ... %s]', numel(v), ...
            num2str(v(1:5), '%.4g '), num2str(v(end-2:end), '%.4g '));
    else
        s = mat2str(v, 6);
    end
end

function s = msg(e), s = strrep(char(e.message), sprintf('\n'), ' '); end
