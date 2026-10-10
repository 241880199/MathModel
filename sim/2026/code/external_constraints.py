#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把外部关注度信号以**周级序约束**接进整季 LP，并报**ρ 曲线**（不是单一收窄数字）。

零参可跑：  python -I sim/2026/code/external_constraints.py

## 读什么 / 写什么

- 读 `sim/2026/out/table-9-external-signal.csv`（`external_signal.py` 的对齐产物；**只读缓存**）
- 写 `sim/2026/out/table-10-external-constraints.csv`（ρ 曲线）
  与 `sim/2026/out/figure-9-external-signal.json`（ρ*、外部标尺）

## 约束形式

对第 w 周、**当周在场集合**内的有序对 (i,j)：

    a_{i,w} ≥ ρ · a_{j,w}   ⇒   w_i ≥ w_j        （写成 w_j − w_i ≤ 0）

★ 用 `a_i >= rho * a_j` 判，**不要**写 `a_i / a_j >= rho`：
  后者 `0/0` 是 `nan`、`x/0` 是 `inf`，会静默丢对 / 静默排序。
★ 在这套模型里 `w_i ≥ w_j ⇔ v_{i,w} ≥ v_{j,w}`（份额 `v = w/S_w`，`S_w>0` 对当周所有人相同）
  ⇒ 对 `w` 的序约束就是对**票份额**的序约束，语义自洽。

## ★★ 为什么**不报单一"收窄了多少"**

给整季 LP 加一条**全序**（ρ→1 时序对铺满）会把可行域压成一点，而**宽度依赖"用哪个序"** ——
对抗性复核实测：同一季在 15 个可行点诱导的序下，平均宽度在 **0.05–0.18** 摆动（池化基线 0.40）。
⇒ 任何单一数字都是"审阅者用同样站得住的选择能挪 4×"的数。
**故本脚本报整条 ρ 曲线**，并把 `ρ = 1`（全序）单列出来并**标注它由模型选择驱动、不由数据驱动**。

## ★ 可证伪读数

布尔"可行/不可行"**没有分辨力**（复核实测：25/25 季都存在"随机全序里至少一个不可行"）。
故逐季报 **`ρ*_s` = 使该季仍可行的最小 ρ**（越小 = 序约束越激进仍站得住）。
★ **只报 7 个有数据的季**（pageviews 覆盖边界 2015-07-01 之后）。

## 射程（不许读大）

- 只做**有外部数据的 7 季**；其余 18 季**没有外部信号**，如实记为未覆盖。
- 多人在同周被淘汰的周**默认排除**（附件解析在该处丢约束，见 `external_signal.py` 的登记），
  另跑一版**含**它们的作敏感性对照。
"""
import csv
import json
import pathlib
import sys
import collections

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import numpy as np                                          # noqa: E402
from scipy.optimize import linprog                          # noqa: E402
from scipy.stats import spearmanr                           # noqa: E402

from fan_vote_bounds import (ROOT, OUT, load, build_panel, judge_pct,  # noqa: E402
                             PERCENT_SEASONS, csv_name)
from fan_vote_season import season_people                   # noqa: E402

SEED = 2025                       # ★ 入口一处固定随机源（本脚本确定性，留着以防日后加抽样）
TABLE9 = OUT / "table-9-external-signal.csv"
RHO_GRID = [None, 20.0, 10.0, 5.0, 3.0, 2.0, 1.5, 1.2, 1.05, 1.0]   # None = 基线（不加序约束）


def multi_elim_weeks():
    """附件里"多人同周淘汰"的 (季, 周) 集合。

    ★ 为什么单独算：`fan_vote_bounds.build_panel` 的 `elim` 以 `(season,week)` 为键，
      多人同周时**后一行覆盖前一行** ⇒ 该周**少一条约束**且语义也不对
      （正确形态是"最低的 k 个被淘汰"，那是另一个模型）⇒ 默认把这些周排除，
      另跑一版含它们的作对照。
    """
    _hdr, body = load(csv_name)
    hdr, _ = load(csv_name)
    i_s, i_res = hdr.index("season"), hdr.index("results")
    cnt = collections.Counter()
    for r in body:
        res = (r[i_res] or "").strip()
        if res.lower().startswith("eliminated week"):
            cnt[(int(r[i_s]), int(res.split()[-1]))] += 1
    return {k for k, v in cnt.items() if v > 1}


def season_lp(panel, elim, s, attn, rho, skip):
    """整季 LP（与本仓 `fan_vote_season.season_bounds` 同一组不等式）+ 可选周级序约束。"""
    people, weeks = season_people(panel, elim, s)
    n = len(people)
    if n < 3 or not weeks:
        return None
    idx = {p: k for k, p in enumerate(people)}
    A_ub, b_ub, npairs = [], [], 0
    for w, present in weeks:
        if (s, w) in skip:
            continue
        e = elim[(s, w)]
        if e not in present or len(present) < 2:
            continue
        jp = judge_pct(panel[(s, w)])
        srow = np.zeros(n)
        for p in present:
            srow[idx[p]] = 1.0
        for j in present:
            if j == e:
                continue
            row = np.zeros(n)
            row[idx[e]] += 1.0
            row[idx[j]] -= 1.0
            row -= (jp[j] - jp[e]) * srow
            A_ub.append(row)
            b_ub.append(0.0)
        # ---- ★ 周级序约束：a_i >= rho * a_j  ⇒  w_j - w_i <= 0 ----
        if rho is not None:
            av = attn.get(w, {})
            ps = [p for p in present if av.get(p)]
            for a in ps:
                for b in ps:
                    if a is b:
                        continue
                    if av[a] >= rho * av[b]:
                        row = np.zeros(n)
                        row[idx[b]] += 1.0
                        row[idx[a]] -= 1.0
                        A_ub.append(row)
                        b_ub.append(0.0)
                        npairs += 1
    if not A_ub:
        return None
    A_eq, b_eq, bnds = np.ones((1, n)), np.array([1.0]), [(0.0, 1.0)] * n
    lo, hi = {}, {}
    for p in people:
        c = np.zeros(n)
        c[idx[p]] = 1.0
        r_lo = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bnds, method="highs")
        r_hi = linprog(-c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bnds, method="highs")
        # ★ 只认 status==2（真不可行）；1=迭代上限 / 3=无界 / 4=数值困难**不是**不可行
        if r_lo.status == 2 or r_hi.status == 2:
            return {"status": "infeasible", "people": people, "npairs": npairs}
        if not (r_lo.success and r_hi.success):
            return {"status": f"solver-{r_lo.status}/{r_hi.status}", "people": people,
                    "npairs": npairs}
        lo[p], hi[p] = float(r_lo.fun), float(-r_hi.fun)
    widths = [hi[p] - lo[p] for p in people]
    return {"status": "ok", "people": people, "npairs": npairs, "ncon": len(A_ub),
            "lo": lo, "hi": hi,
            "w_mid": {p: 0.5 * (lo[p] + hi[p]) for p in people},
            "w_mean": float(np.mean(widths)),
            "w_median": float(np.median(widths)),
            "w_p90": float(np.percentile(widths, 90))}


def sweep(panel, elim, attn, seasons, skip):
    """对给定"排除集"跑一遍 ρ 扫描。返回 (curve, rho_star, rows)。"""
    curve, rows = collections.defaultdict(dict), []
    for s in seasons:
        for rho in RHO_GRID:
            r = season_lp(panel, elim, s, attn.get(s, {}), rho, skip=skip)
            tag = "baseline" if rho is None else f"{rho:g}"
            if r is None or r["status"] != "ok":
                curve[s][tag] = {"status": (r or {}).get("status", "none"),
                                 "npairs": (r or {}).get("npairs")}
                rows.append({"season": s, "rho": tag, "status": curve[s][tag]["status"],
                             "npairs": curve[s][tag]["npairs"]})
                continue
            curve[s][tag] = {"status": "ok", "npairs": r["npairs"], "ncon": r["ncon"],
                             "w_mean": r["w_mean"], "w_median": r["w_median"],
                             "w_p90": r["w_p90"]}
            rows.append({"season": s, "rho": tag, "status": "ok", "npairs": r["npairs"],
                         "ncon": r["ncon"], "w_mean": r["w_mean"],
                         "w_median": r["w_median"], "w_p90": r["w_p90"]})
    star = {}
    for s in seasons:
        feas = [x for x in RHO_GRID if x is not None
                and curve[s].get(f"{x:g}", {}).get("status") == "ok"]
        star[s] = min(feas) if feas else None
    return curve, star, rows


def lagged(attn):
    """把关注度整体**滞后一周**：第 w 周用第 w−1 周的关注度。

    ★ 为什么要这个对照：第 w 周的浏览量里含**当周被淘汰者的淘汰后暴涨** ⇒ 用**当周**关注度
      排序，会把被淘汰者排高，再被淘汰记录否掉 —— 这是一种**反因果污染**。
      滞后一周（用**上**一周的关注度去约束**本**周的票）就把当周的结果从信号里摘出去了。
    """
    out = collections.defaultdict(lambda: collections.defaultdict(dict))
    for s, wk in attn.items():
        for w in sorted(wk):
            if (w - 1) in wk:                       # 第 w 周 ← 第 w−1 周
                out[s][w] = wk[w - 1]
    return out


def load_attention():
    """从 table-9 读回：{season: {week: {contestant: views}}}。"""
    attn = collections.defaultdict(lambda: collections.defaultdict(dict))
    with TABLE9.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            attn[int(r["season"])][int(r["week"])][r["contestant"]] = int(r["views"])
    return attn


def main():
    if not TABLE9.exists():
        raise SystemExit(f"缺 {TABLE9} —— 先跑 `python -I sim/2026/code/external_signal.py`。")
    attn = load_attention()
    seasons = sorted(attn)
    hdr, body = load(csv_name)
    panel, elim, _ = build_panel(hdr, body)
    multi = multi_elim_weeks()
    print(f"外部数据覆盖的季：{seasons}（共 {len(seasons)} 季）")
    print(f"多人同周淘汰的周（默认排除）：{len([k for k in multi if k[0] in seasons])} 个落在这些季里")

    # ★★ 基线自证：**不排除任何周**、**不加序约束** ⇒ 必须与已入库的 figure-2 逐值相同。
    #    这是"我没把原模型改坏"的唯一硬判据（本脚本自己重建了约束构造，必须证明等价）。
    print("\n=== 基线自证（ρ=∞ · 不排除任何周 ⇒ 应与入库 figure-2 逐值相同）===")
    committed = {q["season"]: q for q in json.loads(
        (OUT / "figure-2-season-width-summary.json").read_text(encoding="utf-8"))["seasons"]}
    proof_ok = True
    for s in seasons:
        r = season_lp(panel, elim, s, attn[s], None, skip=set())
        got = r["w_mean"] if r and r["status"] == "ok" else None
        exp = committed.get(s, {}).get("width_mean")
        # ★ 入库 JSON 把 width_mean 存成**四舍五入到 6 位**的值 ⇒ 按**存储精度**比，
        #   拿 1e-12 去比会把"一致"误判成"不一致"（我第一版就是这么误报的）。
        same = (got is not None and exp is not None
                and round(got, 6) == round(exp, 6))
        proof_ok &= same
        print(f"  S{s}: 亲跑 {got} · 入库 {exp} · "
              f"约束数 亲跑 {r['ncon'] if r else '-'} / 入库 {committed.get(s,{}).get('constraints')} · "
              f"{'一致' if same else '★★ 不一致 ★★'}")
    print(f"  ⇒ 基线自证：{'通过' if proof_ok else '★★ 未通过 ★★'}")
    if not proof_ok:
        raise SystemExit("基线自证未通过 ⇒ 本脚本的约束构造与入库版不等价，先修这个再往下走。")

    # ★ 四种口径一并跑，把两处**口径选择**的影响量出来：
    #   ① 排不排除"多人同周淘汰"的周；② 关注度用**当周**还是**滞后一周**。
    curve, rho_star, rows = sweep(panel, elim, attn, seasons, skip=multi)
    curve_all, rho_star_all, _ = sweep(panel, elim, attn, seasons, skip=set())
    curve_lag, rho_star_lag, _ = sweep(panel, elim, lagged(attn), seasons, skip=multi)
    curve_lag_all, rho_star_lag_all, _ = sweep(panel, elim, lagged(attn), seasons, skip=set())

    yard = {}
    for s in seasons:
        # 外部标尺：周级（主口径）与季级（对照）
        base = season_lp(panel, elim, s, attn[s], None, skip=multi)
        if base and base["status"] == "ok":
            wk_rhos = []
            for w, d in sorted(attn[s].items()):
                pr = [p for p in d if p in base["w_mid"]]
                if len(pr) >= 3:
                    a = [d[p] for p in pr]
                    b = [base["w_mid"][p] for p in pr]
                    if len(set(a)) > 1 and len(set(b)) > 1:
                        wk_rhos.append(float(spearmanr(a, b).statistic))
            tot = {p: sum(d.get(p, 0) for d in attn[s].values()) for p in base["w_mid"]}
            ps = [p for p in base["w_mid"] if tot.get(p)]
            se = float(spearmanr([tot[p] for p in ps], [base["w_mid"][p] for p in ps]).statistic) \
                if len(ps) >= 3 else None
            yard[s] = {"weekly_n": len(wk_rhos),
                       "weekly_median": float(np.median(wk_rhos)) if wk_rhos else None,
                       "weekly_mean": float(np.mean(wk_rhos)) if wk_rhos else None,
                       "season_level": se}

    with (OUT / "table-10-external-constraints.csv").open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["season", "rho", "status", "npairs", "ncon",
                                           "w_mean", "w_median", "w_p90"])
        wr.writeheader()
        wr.writerows(rows)
    (OUT / "figure-9-external-signal.json").write_text(json.dumps(
        {"coverage_seasons": seasons, "rho_grid": [str(x) if x else "baseline" for x in RHO_GRID],
         # 四种口径：{curve,rho_star} 主口径 = 排除多人同周淘汰周 + **当周**关注度
         "curve_excl_contemp": curve, "rho_star_excl_contemp": rho_star,
         "curve_incl_contemp": curve_all, "rho_star_incl_contemp": rho_star_all,
         "curve_excl_lag1": curve_lag, "rho_star_excl_lag1": rho_star_lag,
         "curve_incl_lag1": curve_lag_all, "rho_star_incl_lag1": rho_star_lag_all,
         "yardstick": yard,
         "excluded_multi_elim_weeks": sorted(f"S{a}W{b}" for a, b in multi if a in seasons),
         "seed": SEED}, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n★★ ρ*_s = 使该季仍可行的**最小** ρ（越小＝序约束越激进仍站得住；None＝ρ=20 都不可行）")
    print("季 | 排除·当周 | 全含·当周 | 排除·滞后1 | 全含·滞后1 | 基线宽中位 | 周级标尺中位")
    for s in seasons:
        y = yard.get(s, {})
        print(f" {s} | {rho_star[s]!s:>9} | {rho_star_all[s]!s:>9} | {rho_star_lag[s]!s:>9}"
              f" | {rho_star_lag_all[s]!s:>10} | {curve[s].get('baseline', {}).get('w_median')}"
              f" | {y.get('weekly_median')}")
    print("\n落盘：sim/2026/out/table-10-external-constraints.csv · figure-9-external-signal.json")


if __name__ == "__main__":
    main()
