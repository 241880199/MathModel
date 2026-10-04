function wear_demo()
%WEAR_DEMO  End-to-end demonstration of the wear inversion (MCM/ICM 2025 A).
%
%   Runs three things:
%     (A) synthetic ground truth -> noisy "measurement" -> inversion,
%     (B) a parameter-recovery table,
%     (C) archaeological conclusions + a single-file vs side-by-side test.
%
%   Note: free parameters are V, alpha, b, sigx (4).  dmu and sigy are held
%   at their calibrated values, because a single tread's near-unimodal
%   longitudinal profile cannot separate a two-band mixture from one band --
%   see selection.md Sec. 8.2.
%
%   To use REAL data instead: save your measured depth grid as a text file
%   (columns x, y, h OR a matrix of h with matching x/y vectors) and call
%   wear_robustfit / wear_conclusions directly (see selection.md Sec. 7).

rng(20250101);                                  % reproducible

%% 1. Tread geometry and measurement grid --------------------------------
cfg.W = 300;                                    % tread width  [mm] (lateral)
cfg.D = 300;                                    % tread depth  [mm] (longitudinal)
xg = linspace(-cfg.W/2, cfg.W/2, 31);           % lateral coordinate  [mm]
yg = linspace(0, cfg.D, 31);                    % 0 = back edge, D = nosing

% Biomechanical CALIBRATION constants (measure once, keep fixed: they make
% alpha identifiable).  Replace with your own controlled-walk measurements.
cfg.fixdmu  = 60;    % ascending/descending pressure-centroid offset [mm]
cfg.fixsigy = 70;    % longitudinal pressure-band sd [mm]

%% 2. "Ground truth" for the test case -----------------------------------
theta_true = [ log(2.4e5), ...   % V    = 2.4e5 mm^3 removed over its life
               logit(0.62), ...  % 62% of steps ascend
               log(90),   ...    % lanes 90 mm apart (side-by-side)
               log(30),   ...    % lane spread 30 mm
               60,        ...    % front/back centroid offset 60 mm
               log(70) ];        % longitudinal spread 70 mm

H_true = wear_forward(theta_true, xg, yg, cfg);
fprintf('Ground-truth field: max %.2f mm, mean %.2f mm\n', ...
        max(H_true(:)), mean(H_true(:)));

%% 3. Synthetic measurement: white noise + non-negativity ----------------
noise_sd = 0.30;                                % [mm] gauge repeatability
H_obs = max(H_true + noise_sd*randn(size(H_true)), 0);

%% 4. Inversion (multi-start) --------------------------------------------
theta_hat = wear_robustfit(H_obs, xg, yg, cfg);

%% 5. Parameter recovery table -------------------------------------------
print_recovery(theta_true, theta_hat, cfg);

%% 6. Bootstrap uncertainty ----------------------------------------------
[~, sd] = wear_ci(H_obs, xg, yg, theta_hat, cfg, 50);

%% 7. Archaeological conclusions -----------------------------------------
meta = struct('W', cfg.W, 'sd', sd, ...
              'd0_perStep', 0.15, ...   % mm^3 stone per footfall (CALIBRATE!)
              'age_years', 400, ...     % from historical records (if available)
              'daily_steps', 500);      % from daily-life estimate (if available)
S = wear_conclusions(theta_hat, cfg, meta);  %#ok<NASGU>

%% 8. Single-file vs side-by-side: nested model selection by AIC ----------
cfg1 = cfg;  cfg1.fixb = 1e-3;                  % nested "single lane" model
th1  = wear_robustfit(H_obs, xg, yg, cfg1);
[~, res1] = wear_fit(H_obs, xg, yg, th1,       cfg1);
[~, res2] = wear_fit(H_obs, xg, yg, theta_hat, cfg);
fprintf('\nLane-structure model selection (lower AIC wins):\n');
fprintf('  1-lane : AIC = %8.1f , RMSE = %.3f mm\n', res1.AIC, res1.RMSE);
fprintf('  2-lane : AIC = %8.1f , RMSE = %.3f mm\n', res2.AIC, res2.RMSE);
if res1.AIC < res2.AIC
    fprintf('  -> data favour SINGLE FILE\n');
else
    fprintf('  -> data favour TWO LANES (side-by-side)\n');
end

%% 9. Figures (safe to skip in a headless run) ---------------------------
try
    figure('Name','Wear inversion');
    subplot(1,3,1); imagesc(xg, yg, H_obs); axis xy; colorbar;
    xlabel('x [mm]'); ylabel('y [mm]'); title('measured');
    subplot(1,3,2); imagesc(xg, yg, wear_forward(theta_hat,xg,yg,cfg));
    axis xy; colorbar; xlabel('x [mm]'); ylabel('y [mm]'); title('fitted');
    subplot(1,3,3); imagesc(xg, yg, H_obs - wear_forward(theta_hat,xg,yg,cfg));
    axis xy; colorbar; xlabel('x [mm]'); ylabel('y [mm]'); title('residual');
catch ME
    fprintf('(figure skipped: %s)\n', ME.message);
end
end

function y = logit(p)
y = log(p/(1-p));
end
