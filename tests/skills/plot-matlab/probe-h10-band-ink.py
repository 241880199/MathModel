#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`H10`（去上/右框线 · 刻度朝内）的**产物级入库探针**（计划 Task 2 / 质检记录 T5）。

用法（cwd 任意，路径一律按仓根解析）：

    python tests/skills/plot-matlab/probe-h10-band-ink.py

## 它证什么

`mcm-style.json` 的 `h10.axes_box.carriers.matlab` 在 Task 1 之前写着 `not-landable`
（措辞是「**能设、不能验**：侦察有对应 API，但产物端零回读」）。本探针把「能不能验」**真的验一遍**：
用**入库的** `mcmplot.m`（`M.apply()` 里的 H10 生成区：`box(ax,'off')` + `set(ax,'TickDir','in')`）
渲一张图，量**轴区顶边 / 右边内侧**那条带里的**非白像素数**（灰度 < 200；带宽 = 刻度长换算 px + 2 余量，
**现算**），口径与 python 侧 `tests/skills/plot-python/probe-gap1-hanging-ticks.py` **同型**：

- **落地态**（`M.apply()`：box off + TickDir in）⇒ 顶内 / 右内 / 下外三带均应为 **0**；
- **对照态**（同一条链，`apply` 之后把 `box` 打开、`TickDir` 改回 `out`）⇒ 三带都读到**墨迹**（非 0）。

对照非 0 同时证明探针**不是恒零**（不是"什么都没量到也报绿"）。

## 为什么用**入库的** `mcmplot.m`，而不是像 Task 1 那样手写 box/TickDir

Task 1 的一次性探针（`build/m3-matlab-t1/probe_h10_band_ink.m`）是**手写** `box(ax,off)` / `set(ax,'TickDir','in')`
的四态对照；本探针要证的是**交付物 `mcmplot.m` 自己**真的落了 H10 ⇒ 落地态必须走 `M.apply()`。
对照态在 `M.apply()` **之后**覆写 box/TickDir，从而**只翻转 H10 这一项**、其余（浅色主题 / 白底 / 色序 /
字体）逐项相同 ⇒ 读数差归因到 H10，不掺别的。

## 口径（与 Task 1 探针逐条同源，见那份注释）

- 折线取 `x∈[0.1,0.9]`、`y∈[0.35,0.45]`，刻意**避开**顶/右两条被测带 ⇒ 读数只反映框线/刻度，不掺数据墨迹。
- 只数**轴区严格内部**的带（排除左/下另一条轴自己的刻度与标签落点：`corner = band+4` 把角部切掉）。
- 非白阈值：灰度 `< 200`（同 Task 1 探针与 python 侧探针）。
- ⚠️ **行区间一律升序**扫（Task 1 的探针第一版把右边带写成降序 `[B, T]`，`for yy=a:b` 在 `a>b` 时
  **整段跳过** ⇒ 恒零；这正是 GC8 说的"恒真/恒零"。本探针的 `cnt` 已把这一点写进注释与断言）。
- **只写** `build/m3-matlab-t2/`（gitignored）下的产物；**临时 `.m` 驱动写在该目录的 `_probe/` 子目录，收工自清**。

## 射程（写实，别读大）

读数**绝对值**依赖 MATLAB 的刻度方向/长度与 `print` 家族像素（本机 R2025b Update 5）⇒ 换版本绝对值会变；
但"**落地态 0 / 对照态非 0**"这个**判别性**不变（那才是 H10 被处置的直接证据）。`左外带`（y 刻度**标签**
的落点）**只记不用**：标签位置随 `TickDir` 移动 ⇒ 那个数混了两件事（Task 1 已如实登记）。
"""
import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]          # tests/skills/plot-matlab → 仓根
OUT = ROOT / "build/m3-matlab-t2"                            # 产物落点（gitignored，给人看）
PROBEDIR = OUT / "_probe"                                   # 临时 .m 驱动（收工自清）
MSCRIPT = PROBEDIR / "probe_h10_band_ink.m"
MATLAB = os.environ.get("MATLAB_BIN", "D:/Software/Matlab/bin/matlab.exe")  # GC12：本机 R2025b Update 5

# 临时 .m 驱动：脚本形态（局部函数置尾）；`mfilename('fullpath')` 反推仓根（GC12 的同型做法）
DRIVER = r"""% probe_h10_band_ink.m --- M3-plot-matlab Task 2: H10 的**产物级**回读（入库探针的 MATLAB 端）
% 由 tests/skills/plot-matlab/probe-h10-band-ink.py 生成到 build/m3-matlab-t2/_probe/ 下、收工自清。
% 口径见那份 .py 的模块 docstring（与 tests/skills/plot-python/probe-gap1-hanging-ticks.py 同型）。
here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(here)));       % build/m3-matlab-t2/_probe -> ... -> 仓根
cd(root);
addpath(fullfile(root, '.claude', 'skills', 'mcm-plot-matlab', 'assets'));
OUT = fullfile(root, 'build', 'm3-matlab-t2');
if ~exist(OUT, 'dir'); mkdir(OUT); end

DPI = 300;
THRESH = 200;
PAPER = [0 0 6.31 4.20];        % in —— 与 Task 1 探针同幅（**给轴区留地方**：图太矮时 x 刻度标签
                                %        会落进"下外带"、把行区间判据污染；本探针只测 H10、不测图幅）

M = mcmplot();
fprintf('### probe_h10_band_ink start ###\n');
fprintf('version = %s\n', version('-release'));
fprintf('mcmplot STYLE.width_ratio_default_hi = %g · height_in = %g\n', ...
        M.style.width_ratio_default_hi, M.style.height_in);

[a_in, a_rin, a_bout, band, bb] = measure(OUT, M, 'landed', true,  PAPER, DPI, THRESH);
[b_in, b_rin, b_bout, ~,    ~]  = measure(OUT, M, 'control', false, PAPER, DPI, THRESH);

fprintf('%-9s %-12s %8s %8s %8s\n', 'mode', 'box/tick', '顶内', '右内', '下外');
fprintf('%-9s %-12s %8d %8d %8d\n', 'landed',  'off/in',  a_in, a_rin, a_bout);
fprintf('%-9s %-12s %8d %8d %8d\n', 'control', 'on/out',  b_in, b_rin, b_bout);
fprintf('（导出像素 %d x %d · 带宽 %d px · 轴区 L%d R%d T%d B%d）\n', ...
        bb(1), bb(2), band, bb(3), bb(4), bb(5), bb(6));
ok = (a_in == 0) && (a_rin == 0) && (a_bout == 0) && ...
     (b_in > 0) && (b_rin > 0) && (b_bout > 0);
if ok
  fprintf('OK 落地态三带均 0，且对照态三带均 > 0（探针不是恒零）\n');
else
  fprintf('FAIL 读数不符预期（落地态应 0/0/0、对照态应三带全 > 0）\n');
end
fprintf('### probe_h10_band_ink done ###\n');

function [tin, rin, bout, band, bb] = measure(OUT, M, tag, doH10, PAPER, DPI, THRESH)
  fig = figure('Visible', 'off', 'Color', 'w', 'Position', [100 100 800 500], 'Theme', 'light');
  ax = axes(fig);
  plot(ax, linspace(0.1, 0.9, 50), 0.35 + 0.10*sin(linspace(0, 2*pi, 50)), '-');
  ylim(ax, [0 1]); xlim(ax, [0 1]);
  xlabel(ax, 'x'); ylabel(ax, 'y');
  set(fig, 'PaperUnits', 'inches', 'PaperPositionMode', 'manual', 'PaperPosition', PAPER);
  M.apply(fig);                                    % ← 入库件的 H10：box off + TickDir in
  if ~doH10
    box(ax, 'on'); set(ax, 'TickDir', 'out');      % 对照态：把 H10 的两项覆写回去（其余项不动）
  end
  drawnow;
  p = ax.Position; tickRel = ax.TickLength; tickRel = tickRel(1);
  axLongIn = max(p(3)*PAPER(3), p(4)*PAPER(4));
  band = ceil(tickRel * axLongIn * DPI) + 2;
  png = fullfile(OUT, sprintf('h10_%s.png', tag));
  pdf = fullfile(OUT, sprintf('h10_%s.pdf', tag));
  M.save(fig, png, DPI);                           % 导出走**入库件的** save（print 家族）
  M.save(fig, pdf);
  close(fig);

  I = imread(png);
  G = double(I(:,:,1))*0.299 + double(I(:,:,2))*0.587 + double(I(:,:,3))*0.114;
  [Hpx, Wpx] = size(G);
  left = p(1)*Wpx;  right = (p(1)+p(3))*Wpx;
  top_edge = (1 - p(2) - p(4))*Hpx;
  bot_edge = (1 - p(2))*Hpx;
  L = max(round(left), 1); R = min(round(right), Wpx);
  T = max(round(top_edge), 1); B = min(round(bot_edge), Hpx);
  corner = band + 4;
  xin = [L+corner, R-corner];
  yin = [T+corner, B-corner];              % cnt 按行号**升序**扫（降序会整段跳过 ⇒ 恒零）
  tin  = cnt(G, [T-2, T+band-1], xin, THRESH);
  rin  = cnt(G, yin, [R-2, R+band-1], THRESH);
  bout = cnt(G, [B+3, B+band+2], xin, THRESH);
  bb = [Wpx Hpx L R T B band];
end

function n = cnt(G, rows, cols, THRESH)
  [Hpx, Wpx] = size(G);
  n = 0;
  for yy = max(rows(1),1):min(rows(2),Hpx)        % ← 若 rows(1) > rows(2) 则整段跳过（本探针禁止降序）
    for xx = max(cols(1),1):min(cols(2),Wpx)
      if G(yy, xx) < THRESH; n = n + 1; end
    end
  end
end
"""


def run_matlab() -> tuple[int, str, str]:
    """跑 MATLAB `-batch run('<仓相对 .m 路径>')`（cwd = 仓根）。返回 `(rc, stdout, stderr)`。"""
    rel = MSCRIPT.relative_to(ROOT).as_posix()
    cmd = [MATLAB, "-batch", f"run('{rel}')"]
    try:
        pr = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    except OSError as e:                                     # 起不动 MATLAB（未装 / 路径变）
        return 127, "", f"{type(e).__name__}: {e}"
    return pr.returncode, pr.stdout, pr.stderr


def parse(out: str) -> dict:
    """从 MATLAB stdout 里取 `landed` / `control` 行的三个读数（顶内 / 右内 / 下外）。"""
    res = {}
    for line in out.splitlines():
        m = re.match(r"^(landed|control)\s+\S+\s+(\d+)\s+(\d+)\s+(\d+)\s*$", line)
        if m:
            res[m.group(1)] = tuple(int(m.group(i)) for i in (2, 3, 4))
    return res


def main():
    ap = argparse.ArgumentParser(description="H10 产物级回读（顶/右带内墨迹；与 python 侧同型口径）")
    ap.add_argument("--keep-driver", action="store_true", help="保留临时 .m 驱动（默认收工自清）")
    a = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    PROBEDIR.mkdir(parents=True, exist_ok=True)
    MSCRIPT.write_bytes(DRIVER.encode("utf-8"))              # 全 LF；write_bytes（GC4）

    print("H10 产物级回读探针（顶内 / 右内 / 下外带内非白像素）· 口径同 python 侧 probe-gap1-hanging-ticks.py")
    print(f"驱动 = {MSCRIPT.relative_to(ROOT).as_posix()}（临时；收工自清）")
    print(f"MATLAB = {MATLAB}")
    try:
        rc, out, err = run_matlab()
    finally:
        if not a.keep_driver:
            shutil.rmtree(PROBEDIR, ignore_errors=True)
    for line in out.splitlines():
        print("  | " + line)
    if err.strip():
        print("  stderr:")
        for line in err.strip().splitlines():
            print("  ! " + line)

    if rc != 0:
        print(f"RESULT: FAIL（MATLAB 退出 {rc} ⇒ 探针没跑成，fail-closed）")
        return 1
    r = parse(out)
    if set(r) != {"landed", "control"}:
        print(f"RESULT: FAIL（读不出 landed/control 两态读数：{r} ⇒ fail-closed）")
        return 1
    landed, control = r["landed"], r["control"]
    ok = landed == (0, 0, 0) and all(v > 0 for v in control)
    print("-" * 78)
    print(f"落地态（M.apply 的 H10：box off + TickDir in） 顶内/右内/下外 = {landed}")
    print(f"对照态（apply 后覆写 box on + TickDir out）    顶内/右内/下外 = {control}")
    print(f"产物（给人看） = {OUT.relative_to(ROOT).as_posix()}/h10_{{'landed','control'}}.{{png,pdf}}")
    print("RESULT: PASS" if ok else
          "RESULT: FAIL（落地态应 0/0/0、对照态应三带全 > 0）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
