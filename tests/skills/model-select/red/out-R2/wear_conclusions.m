function S = wear_conclusions(theta_hat, cfg, meta)
%WEAR_CONCLUSIONS  Turn fitted parameters into archaeologically usable output.
%
%   S = WEAR_CONCLUSIONS(theta_hat, cfg, meta)
%
%   meta (optional) fields:
%       W            tread width [mm]                 (default 300)
%       sd           1x6 parameter sd from WEAR_CI     (optional)
%       d0_perStep   volume removed per footfall [mm^3] (optional; needs a
%                    material calibration, see selection.md Sec. 6)
%       age_years    age from historical records [yr] (optional)
%       daily_steps  daily traffic from life-pattern estimate (optional)
%
%   Prints a report and returns a struct S with the mapped quantities.

if nargin < 3, meta = struct(); end
if ~isfield(meta,'W'),  meta.W  = 300; end
if ~isfield(meta,'sd'), meta.sd = nan(1,6); end

V     = exp(theta_hat(1));
alpha = 1/(1+exp(-theta_hat(2)));
if isfield(cfg,'fixb') && ~isempty(cfg.fixb)
    b = cfg.fixb;
else
    b = exp(theta_hat(3));
end
sigx = exp(theta_hat(4));
dmu  = theta_hat(5);
sigy = exp(theta_hat(6));
if isfield(cfg,'fixdmu')  && ~isempty(cfg.fixdmu),  dmu  = cfg.fixdmu;  end
if isfield(cfg,'fixsigy') && ~isempty(cfg.fixsigy), sigy = cfg.fixsigy; end

W = meta.W;  D = cfg.D;
h_mean = V/(W*D);
xg = linspace(-W/2, W/2, 61);
yg = linspace(0, D, 61);
Hp = wear_forward(theta_hat, xg, yg, cfg);
h_peak = max(Hp(:));
laneRatio = b/max(sigx, eps);

sd_alpha = alpha*(1-alpha)*meta.sd(2);   % delta method through the logit
sd_V     = V*meta.sd(1);                 % delta method through log V

fprintf('\n================ Archaeological conclusions ================\n');
fprintf('Total removed wear volume  V      = %.4g mm^3\n', V);
fprintf('Mean wear depth            h_mean = %.3f mm\n', h_mean);
fprintf('Peak wear depth            h_peak = %.3f mm\n', h_peak);

% ---- (1) how often were the stairs used? ---------------------------------
fprintf('\n[How often were the stairs used?]\n');
if isfield(meta,'d0_perStep') && ~isempty(meta.d0_perStep)
    N = V/meta.d0_perStep;
    fprintf('  per-footfall removal d0 = %.3g mm^3  =>  total footsteps N ~ %.4g\n', ...
            meta.d0_perStep, N);
    if isfield(meta,'age_years') && ~isempty(meta.age_years)
        fprintf('  given age = %.0f yr  =>  mean traffic ~ %.1f steps/day\n', ...
                meta.age_years, N/(meta.age_years*365));
    end
    if isfield(meta,'daily_steps') && ~isempty(meta.daily_steps)
        fprintf('  given traffic = %.0f steps/day  =>  implied age ~ %.0f yr\n', ...
                meta.daily_steps, N/(meta.daily_steps*365));
    end
else
    fprintf('  (no d0 supplied: report the wear-age index V only, not absolute counts)\n');
end

% ---- (2) was a direction favoured? ---------------------------------------
fprintf('\n[Was a direction of travel favoured?]\n');
fprintf('  ascending fraction alpha = %.3f  (+/- %.3f)\n', alpha, sd_alpha);
if     alpha > 0.5 + 2*sd_alpha
    dirTxt = 'significantly biased UP';
elseif alpha < 0.5 - 2*sd_alpha
    dirTxt = 'significantly biased DOWN';
else
    dirTxt = 'roughly two-way (no significant bias)';
end
fprintf('  verdict: %s  (front/back centroid offset dmu = %.1f mm)\n', dirTxt, dmu);

% ---- (3) how many people at once? ----------------------------------------
fprintf('\n[How many people used the stairs simultaneously?]\n');
fprintf('  lane separation b = %.1f mm, lane spread sigx = %.1f mm, b/sigx = %.2f\n', ...
        b, sigx, laneRatio);
if laneRatio > 2
    fprintf('  verdict: two tracks -> side-by-side / parallel traffic\n');
else
    fprintf('  verdict: single track -> single file\n');
end
fprintf('===========================================================\n');

S = struct('V',V,'alpha',alpha,'b',b,'sigx',sigx,'dmu',dmu,'sigy',sigy, ...
           'h_mean',h_mean,'h_peak',h_peak,'laneRatio',laneRatio, ...
           'sd_alpha',sd_alpha,'sd_V',sd_V);
end
