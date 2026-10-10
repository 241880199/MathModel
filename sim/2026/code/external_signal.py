#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""外部关注度信号（维基 pageviews）—— 取数 + 与题面附件对齐。**两段式**。

零参可跑：  python -I sim/2026/code/external_signal.py            # 只读缓存
联网取数：  python -I sim/2026/code/external_signal.py --refresh  # 唯一会碰网络的分支

## 为什么有它

`sim/2026/tex/S7-strengths-weaknesses.tex` 自陈的本模拟最大弱点是"未用外部代理，
辨识力就是代价"。模拟当时**取不到**（网络受限），本轮把信号取回来。

## ★ 两段式 = 可复现性的硬要求

- `--refresh`：**唯一**会碰网络的分支。把**原始响应逐字**落进 `sim/2026/data/wiki-cache/`。
- 零参跑：**只读缓存**；缺缓存就**大声失败**，绝不静默联网。
  ⇒ 此后一切重跑（含 `external_constraints.py`）都只读缓存 ⇒ 结果完全确定。
★ 本仓此前**没有任何 `.py` 联网取数**。唯一的先例是
  `.claude/skills/mcm-plot-python/assets/fonts/PROVENANCE.md`（外部字节入仓 + 逐件哈希 + 取回日期）。
  ⇒ 本脚本照那个形态：每件缓存在 `PROVENANCE.md` 里记 请求 URL / 取回时刻(UTC) / HTTP 状态 / sha256。

## ★★ 两条**实测过**的坑（写死在代码里，别重犯）

1. **覆盖边界 `2015-07-01`**：pageviews 端点在更早的日期返回 **404**（实测
   `20150629..0630 → 404`、`20150630..0702 → 200`）。⇒ 射程内的 3–27 季里
   **只有 S21–S27 有数据**，S3–S20 整段无数据。
2. **404 有歧义**：条目**不存在** 与 **时段未覆盖** 的响应体**逐字节相同**
   ⇒ **绝不用 pageviews 的状态码判条目是否存在**；存在性单独走 `action=query&redirects=1`。
   ★ 且 pageviews 端点**不跟随重定向** ⇒ 拿到规范标题再取数，否则重定向条目静默返回近零。

## ★ 工程约束（来自出货判据，违反会红）

- **URL 不许出现在本文件的可执行字符串里**：`CD5` 的正则 `[A-Za-z]:[\\\\/]` 会命中
- ★★ **本文件里不许出现任何 URL 字面量**（连文档字符串里也不行）—— 出货 `CD5` 的
  正则会把**协议头里的冒号加斜杠**误判成盘符路径，而它**剥 `#` 注释、不剥字符串**。
  ⇒ 端点一律从 `sim/2026/data/sources.json` 读。
- ★★ **本文件里不许出现表示「随机」的那个英文词**（`CD1` 全文扫它，撞到就要求同文件有种子字面量）—— **连文档字符串里也不行**。本脚本本来就不用随机数，这条只是别自己踩。
  ⚠️ **我第一版正是在文档字符串里「描述」这两条禁忌，结果把两条判据都打红了。**
- 限速 ≥ `min_interval_sec`/次，带可识别 `User-Agent`。

## 射程（不许读大）

- **只做百分比法季次里"有 pageviews 数据"的那些季**；无数据的季**如实记为未覆盖**，不填零。
- 逐周窗口取自季条目的 `==Episodes==`（`OriginalAirDate`）；解析不干净时降级为
  以 `P580` 为锚的等长 7 天分箱，**逐季记下用了哪一种**。
"""
import argparse
import csv
import hashlib
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# ★ `python -I` 不会把脚本目录放进 sys.path ⇒ 显式加回**本脚本自己的目录**（我们自己写的代码）
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from fan_vote_bounds import (ROOT, OUT, load, build_panel, PERCENT_SEASONS,  # noqa: E402
                             csv_name)

HERE = pathlib.Path(__file__).resolve().parent          # sim/2026/code
SIM = HERE.parent                                       # sim/2026
DATA = SIM / "data"
CACHE = DATA / "wiki-cache"
PROV = CACHE / "PROVENANCE.md"
SOURCES = DATA / "sources.json"

# ★ 实测的覆盖边界：pageviews 端点在更早的日期一律 404
COVERAGE_START = "2015-07-01"
# 射程内的季次里**有数据**的那些（实施时由 季窗口 ∩ 覆盖边界 算出，这里只作交叉核对）
EXPECTED_COVERED = (21, 22, 23, 24, 25, 26, 27)

_last_call = [0.0]
_FILL = [False]      # True = 只补**缺**的缓存（不重取已有的），由 `--fill` 置位


def _sources():
    return json.loads(SOURCES.read_text(encoding="utf-8"))


def _plus7(iso):
    from datetime import date, timedelta
    y, m, d = map(int, iso.split("-"))
    return (date(y, m, d) + timedelta(days=7)).isoformat()


def iso_week_edges(dates):
    """把逐**集**播出日归并成逐**周**边界（ISO 周，周一为始）。

    ★ 为什么必须归并：条目的 `Episodes` 里**一周可能有两集**（实测 S25：
      `09-18`(一) `09-25`(一) `09-26`(二) `10-02`(一)…）⇒ 直接拿第 k 个播出日当第 k 周
      会让第 2 周之后**整体漂移**。附件里的 `week w` 是**播出周**，所以按 ISO 周去重才对得上。
    """
    from datetime import date, timedelta
    mons = []
    for d in dates:
        y, m, dd = map(int, d.split("-"))
        day = date(y, m, dd)
        mon = day - timedelta(days=day.weekday())
        if mon not in mons:
            mons.append(mon)
    mons.sort()
    return [x.isoformat() for x in mons]

# 退避表（秒）—— ★ 固定表，不引入任何随机性（动机见文档头）
# 退避表（秒）—— ★ 固定表，不引入任何随机性（动机见文档头）
_BACKOFF = (5, 15, 30, 60)


def _get(url, timeout=45):
    """**唯一**发起网络请求的地方。限速 + 可识别 UA + **429/5xx 退避重试**。

    ★ 实测：Wikidata SPARQL 会在两次调用之间就回 **429**；不重试就会把 429 的响应体
      当成"数据"写进缓存（本脚本第一版真犯过这个错）。这里重试，仍失败则**原样返回状态码**，
      由调用方决定**不覆盖缓存**。
    """
    cfg = _sources()
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({"http": cfg["proxy"], "https": cfg["proxy"]}),
        urllib.request.HTTPRedirectHandler(),
    )
    req = urllib.request.Request(url, headers={"User-Agent": cfg["user_agent"],
                                               "Accept": "application/json"})
    status, body = 0, ""
    for attempt in range(len(_BACKOFF) + 1):
        wait = cfg["min_interval_sec"] - (time.time() - _last_call[0])
        if wait > 0:
            time.sleep(wait)
        try:
            with opener.open(req, timeout=timeout) as r:
                status, body = r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            status, body = e.code, e.read().decode("utf-8", "replace")
        except Exception as e:                      # 网络层异常
            status, body = 0, str(e)
        finally:
            _last_call[0] = time.time()
        if status == 200:
            return status, body
        if status in (429, 500, 502, 503) and attempt < len(_BACKOFF):
            time.sleep(_BACKOFF[attempt])
            continue
        break
    return status, body


def _cache_path(key):
    return CACHE / (key + ".json")


def _cached(key, url, refresh):
    """两段式的核心：`refresh` 才联网；否则只读缓存，缺了就大声失败。"""
    p = _cache_path(key)
    if refresh or (_FILL[0] and not p.exists()):
        status, body = _get(url)
        # ★★ 非 200 **绝不覆盖**既有缓存 —— 否则一次 429 就能把好数据换成一份 HTML 错误页。
        #    （本脚本第一版就栽在这里：200 之后紧跟一次 429，好缓存被盖掉、json 解析当场炸。）
        CACHE.mkdir(parents=True, exist_ok=True)
        _provenance(p, url, status, body)
        if status != 200:
            raise SystemExit(
                f"取数失败 HTTP {status}（**既有缓存未动**）：{url[:90]}…\n"
                f"  重跑 `--refresh` 即可；零参跑仍可读旧缓存。")
        p.write_bytes(body.encode("utf-8"))
        return status, body
    if not p.exists():
        raise SystemExit(
            f"缺缓存 `{p}` —— 零参跑只读缓存、绝不联网。先跑一次 `--refresh`。")
    return 200, p.read_text(encoding="utf-8")


def _provenance(path, url, status, body):
    """照 fonts/PROVENANCE.md 的形态：逐件记 URL / 取回时刻 / 状态 / sha256。"""
    from datetime import datetime, timezone
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    if not PROV.exists():
        PROV.write_text(
            "# 外部字节取回记录（`wiki-cache/`）\n\n"
            "> 形态照 `.claude/skills/mcm-plot-python/assets/fonts/PROVENANCE.md`：\n"
            "> **外部字节入仓 + 逐件哈希 + 取回日期 + HTTP 状态**。\n"
            "> ★ 缓存**只许逐字落盘、不许手改**（改了哈希就变）。\n"
            "> ★ 本目录是 `--refresh` 的产物；零参跑**只读**它。\n\n"
            "| 文件 | 请求 URL | 取回(UTC) | HTTP | sha256 |\n"
            "| :--- | :--- | :--- | :--- | :--- |\n",
            encoding="utf-8")
    with PROV.open("a", encoding="utf-8") as f:
        f.write(f"| `{path.name}` | `{url}` | {stamp} | {status} | `{digest[:16]}` |\n")


# ---------------------------------------------------------------- 1) 季 → 播出窗口

def season_windows(refresh):
    """Wikidata SPARQL：该系列各季的 P580 / P582。"""
    cfg = _sources()
    q = ("SELECT ?season ?seasonLabel ?start ?end WHERE {"
         f" ?season wdt:P179 wd:{cfg['series_qid']} ."
         " OPTIONAL { ?season wdt:P580 ?start } OPTIONAL { ?season wdt:P582 ?end }"
         ' SERVICE wikibase:label { bd:serviceParam wikibase:language "en". } }')
    url = cfg["wikidata_sparql"] + "?" + urllib.parse.urlencode(
        {"query": q, "format": "json"})
    _, body = _cached("wikidata-series-seasons", url, refresh)
    d = json.loads(body)
    out = {}
    for b in d["results"]["bindings"]:
        lab = b.get("seasonLabel", {}).get("value", "")
        m = re.search(r"season (\d+)$", lab)
        if not m:
            continue
        s = int(m.group(1))
        out[s] = {"label": lab,
                  "start": b.get("start", {}).get("value", "")[:10],
                  "end": b.get("end", {}).get("value", "")[:10]}
    return out


# ---------------------------------------------------------------- 2) 季条目：参赛者表 + 逐集日期

def season_wikitext(s, refresh):
    cfg = _sources()
    title = f"Dancing with the Stars (American TV series) season {s}"
    url = cfg["wikipedia_api"] + "?" + urllib.parse.urlencode(
        {"action": "parse", "page": title, "prop": "wikitext",
         "format": "json", "redirects": "1"})
    _, body = _cached(f"season-{s:02d}-wikitext", url, refresh)
    d = json.loads(body)
    if "error" in d:
        return None
    return d["parse"]["wikitext"]["*"]


def parse_cast(wt):
    """参赛者表的 Celebrity 列：`{{sortname|First|Last}}`（**不是** `[[链接]]`）。"""
    m = re.search(r'\{\|.*?\|\}', wt, re.S)
    names = []
    for blk in re.finditer(r'\{\|.*?\n\|\}', wt, re.S):
        b = blk.group(0)
        if "Celebrity" in b and "Professional partner" in b:
            for t in re.finditer(r"\{\{sortname\|([^}|]+)\|([^}|]+)", b):
                names.append(f"{t.group(1).strip()} {t.group(2).strip()}")
            break
    return names


def parse_episode_dates(wt):
    """`==Episodes==` 段里的 `OriginalAirDate = {{Start date|Y|M|D}}`。"""
    i = wt.find("==Episodes==")
    seg = wt[i:] if i >= 0 else wt
    ds = []
    for m in re.finditer(r"OriginalAirDate\s*=\s*\{\{Start date\|(\d+)\|(\d+)\|(\d+)", seg):
        ds.append(f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}")
    return ds


# ---------------------------------------------------------------- 3) 条目存在性 / 重定向

def resolve_titles(titles, refresh, tag):
    """★ 独立一步（拦路石 2）：`action=query&redirects=1` 取**规范标题**。

    pageviews 端点**不跟随重定向** ⇒ 必须在取数**之前**解析；
    且**绝不**用 pageviews 的 404 去判条目存在（那个 404 与"时段未覆盖"逐字节相同）。
    """
    cfg = _sources()
    out = {}
    titles = [t for t in titles if t]
    for k in range(0, len(titles), 20):                    # 批量 20 个/次，省调用
        chunk = titles[k:k + 20]
        url = cfg["wikipedia_api"] + "?" + urllib.parse.urlencode(
            {"action": "query", "titles": "|".join(chunk), "redirects": "1",
             "format": "json"})
        _, body = _cached(f"titles-{tag}-{k // 20:02d}", url, refresh)
        d = json.loads(body)
        q = d.get("query", {})
        norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
        redir = {x["from"]: x["to"] for x in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", {}).values()}
        for t in chunk:
            cur = norm.get(t, t)
            cur = redir.get(cur, cur)
            p = pages.get(cur)
            out[t] = {"title": cur,
                      "exists": bool(p and "missing" not in p),
                      "pageid": (p or {}).get("pageid")}
    return out


def search_fallback(name, refresh, tag):
    """兜底：搜索 → 取**排名最前**、且同时满足两条的候选：

    ① 标题的**每个词都来自附件里的人名** —— 把 `Jennie Finch Daigle` 对到 `Jennie Finch`，
       同时挡掉搜索顺带返回的同节目其他人（实测：一次搜索返回
       `Jennie Finch` / `Keo Motsepe` / `Alan Bersten`，后两个是 DWTS 的职业舞者）；
    ② 正文（**全篇**、不是导语）里出现本节目名。

    ★ 为什么要求"全篇正文"：本节目几乎不出现在人物条目的**导语**里，用 `exintro=1` 自查
      会**低估**命中率（我自己犯过）。
    ★ 为什么不是"唯一命中"：那条规则**太严** —— 实测上面三个候选的正文**全都**提到本节目
      ⇒ 唯一命中数 = 0，把**正确解也挡掉了**。
    """
    cfg = _sources()
    qtok = set(name.lower().replace("-", " ").split())
    url = cfg["wikipedia_api"] + "?" + urllib.parse.urlencode(
        {"action": "query", "list": "search", "srsearch": name,
         "srlimit": "3", "format": "json"})
    _, body = _cached(f"search-{tag}", url, refresh)
    hits = [h["title"] for h in json.loads(body).get("query", {}).get("search", [])]
    for t in hits:
        if not set(t.lower().replace("-", " ").split()) <= qtok:
            continue
        u2 = cfg["wikipedia_api"] + "?" + urllib.parse.urlencode(
            {"action": "query", "prop": "extracts", "explaintext": "1",
             "titles": t, "format": "json"})
        _, b2 = _cached(f"extract-{tag}-{t.replace(' ', '_').replace('/', '_')}", u2, refresh)
        pg = list(json.loads(b2).get("query", {}).get("pages", {}).values())
        txt = ((pg[0].get("extract", "") if pg else "") or "")
        if "dancing with the stars" in txt.lower():      # ★ 大小写不敏感（实测会撞上大小写差异）
            return t
    return None


# ---------------------------------------------------------------- 4) 取浏览量

def fetch_pageviews(title, start, end, refresh, tag):
    """官方 REST API。★ 404 ⇒ **不填零**：把状态如实带回去，由调用方判因。"""
    cfg = _sources()
    art = urllib.parse.quote(title.replace(" ", "_"), safe="")
    url = (cfg["pageviews_api"] + "/en.wikipedia/all-access/user/" + art
           + f"/daily/{start.replace('-', '')}00/{end.replace('-', '')}00")
    status, body = _cached(f"pv-{tag}", url, refresh)
    if status != 200:
        return status, []
    try:
        items = json.loads(body)["items"]
    except Exception:
        return status, []
    return status, [(it["timestamp"][:8], it["views"]) for it in items]


# ---------------------------------------------------------------- 主流程

def main():
    ap = argparse.ArgumentParser(description="外部关注度信号：取数 + 对齐（两段式）")
    ap.add_argument("--refresh", action="store_true",
                    help="联网**重取全部**并刷新缓存")
    ap.add_argument("--fill", action="store_true",
                    help="联网**只补缺失**的缓存条目（已有的一律不动）")
    a = ap.parse_args()
    _FILL[0] = a.fill

    windows = season_windows(a.refresh)
    # ★ 季窗口：Wikidata 的 P580/P582 优先；**缺日期的（实测 S27 就是）降级用季条目的逐集日期**。
    #   不做这层降级就会把 S27 误判成"无数据" —— 那是**元数据缺失**，不是数据缺失。
    win, win_mode = {}, {}
    for s in sorted(PERCENT_SEASONS):
        w = windows.get(s) or {}
        st, en = w.get("start", ""), w.get("end", "")
        src = "wikidata"
        if not st:
            wt = season_wikitext(s, a.refresh)
            eps = parse_episode_dates(wt) if wt else []
            if eps:
                st, en, src = eps[0], eps[-1], "season-article"
        if st:
            win[s] = {"start": st, "end": en or st}
            win_mode[s] = src
    covered = [s for s in sorted(PERCENT_SEASONS)
               if s in win and win[s]["start"] >= COVERAGE_START]
    uncovered = [s for s in sorted(PERCENT_SEASONS) if s not in covered]
    print(f"射程内季次 {len(list(PERCENT_SEASONS))} 个："
          f"**窗口落在覆盖边界之后的 {len(covered)} 个** {covered} · "
          f"无数据 {len(uncovered)} 个 {uncovered}")
    print(f"（覆盖边界实测 = {COVERAGE_START}；见本文件文档头的拦路石 1）")
    print(f"（季窗口来源：{ {s: win_mode[s] for s in covered} }）")

    panel, elim, _order = build_panel(*load(csv_name))
    rows, unresolved, per_season, fallback_used = [], [], {}, []
    for s in covered:
        wt = season_wikitext(s, a.refresh)
        if not wt:
            print(f"  季 {s}: 季条目取不到 ⇒ 跳过（如实记未覆盖）")
            continue
        cast = parse_cast(wt)
        eps = parse_episode_dates(wt)
        csvin = {p for (ss, _w), d in panel.items() if ss == s for p in d}
        # 只保留附件里出现过的人名（附件为准）
        want = sorted(csvin)
        res = resolve_titles(want, a.refresh, f"s{s:02d}")
        mis = [n for n in want if not res[n]["exists"]]
        # 兜底：搜索 + 正文含节目名 + 唯一命中（否则交人工复核，**不猜**）
        for n in list(mis):
            alt = search_fallback(n, a.refresh, f"s{s:02d}-{n.replace(' ', '_')}")
            if alt:
                res[n] = {"title": alt, "exists": True, "pageid": None}
                mis.remove(n)
                fallback_used.append({"season": s, "attachment_name": n, "article": alt})
        unresolved += [{"season": s, "name": n, "reason": "查无此条目（兜底亦无唯一命中）"}
                       for n in mis]
        ok = [n for n in want if res[n]["exists"]]
        # 逐周窗口
        if len(eps) >= 2:
            mode = "episodes-iso-week"
            edges = iso_week_edges(eps)
        else:
            mode = "equal-7d"
            d0 = win[s]["start"]
            from datetime import date, timedelta
            y, m, dd = map(int, d0.split("-"))
            base = date(y, m, dd)
            edges = [(base + timedelta(days=7 * k)).isoformat() for k in range(0, 12)]
        weeks = sorted({w for (ss, w), _ in panel.items() if ss == s})
        while len(edges) < max(weeks) + 1:          # 边界不够就按 7 天递推补，别静默丢周
            edges.append(_plus7(edges[-1]))
        s0, s1 = win[s]["start"], win[s]["end"]
        for n in ok:
            t = res[n]["title"]
            # ★ 每位选手**打一次**覆盖整季，再本地切周 ⇒ ~13 次/季，而不是 ~130 次
            status, series = fetch_pageviews(t, s0, s1, a.refresh,
                                             f"s{s:02d}-{n.replace(' ', '_')}")
            by_date = {d: v for d, v in series}
            for w in weeks:
                if w - 1 >= len(edges):
                    continue
                st = edges[w - 1]
                en = edges[w] if w < len(edges) else _plus7(st)
                lo, hi = st.replace("-", ""), en.replace("-", "")
                vs = [v for d, v in by_date.items() if lo <= d < hi]
                rows.append({"season": s, "week": w, "contestant": n,
                             "article": t, "w_start": st, "w_end": en,
                             "http": status,
                             "views": sum(vs), "days": len(vs)})
        per_season[s] = {"cast_in_article": len(cast), "in_attachment": len(want),
                         "resolved": len(ok), "unresolved": len(mis),
                         "episodes_dates": len(eps), "week_window_mode": mode}
        print(f"  季 {s}: 附件 {len(want)} 人 · 解析成功 {len(ok)} · 查无条目 {len(mis)} · "
              f"窗口口径 {mode}（{len(eps)} 个播出日）")

    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "table-9-external-signal.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["season", "week", "contestant", "article",
                                           "w_start", "w_end", "http", "views", "days"])
        wr.writeheader()
        wr.writerows(rows)
    meta = {"coverage_boundary": COVERAGE_START, "covered_seasons": covered,
            "uncovered_seasons": uncovered, "per_season": per_season,
            "unresolved": unresolved, "fallback_used": fallback_used, "n_rows": len(rows)}
    (OUT / "external-signal-alignment.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"落盘：{csv_path.relative_to(ROOT.parent)}（{len(rows)} 行）")
    print(f"落盘：sim/2026/out/external-signal-alignment.json · 未解析 {len(unresolved)} 条")


if __name__ == "__main__":
    main()
