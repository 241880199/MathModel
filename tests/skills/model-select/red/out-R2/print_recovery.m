function print_recovery(tt, th, cfg)
%PRINT_RECOVERY  Show true vs fitted parameters for a synthetic test.
Vt=exp(tt(1)); at=1/(1+exp(-tt(2))); bt=exp(tt(3)); sxt=exp(tt(4)); dmut=tt(5); syt=exp(tt(6));
Vh=exp(th(1)); ah=1/(1+exp(-th(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    bh = cfg.fixb;
else
    bh = exp(th(3));
end
sxh=exp(th(4)); dmuh=th(5); syh=exp(th(6));
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmuh = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), syh  = cfg.fixsigy; end

fprintf('\n----------- Parameter recovery (synthetic test) -----------\n');
fprintf('%-10s %13s %13s %10s\n','param','true','fitted','relerr');
row('V',    Vt,   Vh);
row('alpha',at,   ah);
row('b',    bt,   bh);
row('sigx', sxt,  sxh);
row('dmu',  dmut, dmuh);
row('sigy', syt,  syh);
end

function row(n,t,h)
if abs(t) > eps, e = (h-t)/t; else, e = nan; end
fprintf('%-10s %13.4g %13.4g %9.1f%%\n', n, t, h, 100*e);
end
