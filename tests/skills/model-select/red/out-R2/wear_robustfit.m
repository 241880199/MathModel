function theta_hat = wear_robustfit(Hobs, xg, yg, cfg)
%WEAR_ROBUSTFIT  Multi-start least-squares inversion (guards local minima).
%
%   theta_hat = WEAR_ROBUSTFIT(Hobs, xg, yg, cfg)
%
%   Runs WEAR_FIT from several starting points (lane separation x direction
%   split) and returns the solution with the smallest sum of squared errors.
%   The total-volume start is data driven (V0 = integral of the depth image),
%   which makes the fit converge quickly.

dx = mean(diff(xg));
dy = mean(diff(yg));
V0 = max(sum(Hobs(:)) * abs(dx*dy), 1);   % integral of the wear image = V

bgrid = [1e-2, 40, 90, 150];              % candidate lane separations [mm]
a0    = [0.30, 0.50, 0.70];              % candidate ascending fractions

best = inf;  theta_hat = [];

for b0 = bgrid
    for a = a0
        th0 = [log(V0), log(a/(1-a)), log(b0), log(35), 0, log(80)];
        [th, res] = wear_fit(Hobs, xg, yg, th0, cfg);
        if res.SSE < best
            best = res.SSE;
            theta_hat = th;
        end
    end
end
end
