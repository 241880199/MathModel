function H = wear_forward(theta, xg, yg, cfg)
%WEAR_FORWARD  Spatial wear-depth field h(x,y) for one stair tread.
%              Model for MCM/ICM 2025 Problem A ("Testing Time").
%
%   H = WEAR_FORWARD(theta, xg, yg, cfg)
%
%   Forward model (see selection.md, Sec. 4):
%       h(x,y) = V * [     alpha  * gx(x) * gy_up(y)
%                    + (1-alpha)  * gx(x) * gy_dn(y) ]
%   with the probability densities
%       gx(x)  = 0.5*N(x; +b/2, sigx) + 0.5*N(x; -b/2, sigx)   (walking lanes)
%       gy_up  = N(y; D/2 + dmu/2, sigy)                        (ascending steps)
%       gy_dn  = N(y; D/2 - dmu/2, sigy)                        (descending steps)
%   where N(u;m,s) = exp(-0.5*((u-m)/s)^2) / (s*sqrt(2*pi)) is a Gaussian pdf.
%
%   theta = [ log(V), logit(alpha), log(b), log(sigx), dmu, log(sigy) ]
%       V      total removed wear volume [mm^3]  (V = N_steps * d0)
%       alpha  fraction of footsteps that ASCEND, in (0,1)
%       b      lateral separation of the two walking lanes [mm] (b->0 = single file)
%       sigx   lateral spread of one lane [mm]
%       dmu    front(+)/back(-) offset between the ascending and descending
%              foot-pressure centroids [mm]
%       sigy   longitudinal spread of the pressure band [mm]
%
%   xg : 1xNx lateral coordinates [mm], x = 0 at the mid-width of the tread,
%        going outward to +/- W/2  (W = tread width, measured across).
%   yg : 1xNy longitudinal coordinates [mm], y = 0 at the BACK edge to
%        y = D at the FRONT edge (the nosing you face when climbing).
%   cfg: struct with fields
%        D               tread depth [mm]  (required)
%        fixb   (opt.)   if set, the lane separation b is FIXED to this value
%        fixdmu (opt.)   if set, dmu  is FIXED to this value (biomech. calib.)
%        fixsigy(opt.)   if set, sigy is FIXED to this value (biomech. calib.)
%        muy_up (opt.)   override the ascending centroid [mm]
%        muy_dn (opt.)   override the descending centroid [mm]
%
%   Returns H, size numel(yg) x numel(xg), in mm.
%
%   Base MATLAB only (no toolboxes).

g = @(u,m,s) exp(-0.5*((u-m)./s).^2) ./ (s*sqrt(2*pi));

V     = exp(theta(1));
alpha = 1/(1+exp(-theta(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    b = cfg.fixb;
else
    b = exp(theta(3));
end
sigx = exp(theta(4));
dmu  = theta(5);
sigy = exp(theta(6));

% --- calibrated (fixed) longitudinal constants, if supplied ---------------
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmu  = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), sigy = cfg.fixsigy; end

D = cfg.D;
muy_up = D/2 + dmu/2;
muy_dn = D/2 - dmu/2;
if isfield(cfg,'muy_up') && ~isempty(cfg.muy_up), muy_up = cfg.muy_up; end
if isfield(cfg,'muy_dn') && ~isempty(cfg.muy_dn), muy_dn = cfg.muy_dn; end

gx    = 0.5*g(xg,  b/2, sigx) + 0.5*g(xg, -b/2, sigx);  % 1 x Nx
gy_up = g(yg, muy_up, sigy);                            % 1 x Ny
gy_dn = g(yg, muy_dn, sigy);                            % 1 x Ny

H = V * (     alpha  * (gx(:) * gy_up(:).') + ...
         (1 - alpha)  * (gx(:) * gy_dn(:).') );
H = max(H, 0);
end
