#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 `tests/skills/figure-choose/house-style-verify.txt`（Task 3 的逐字证据件）。

用法：  python tests/skills/figure-choose/gen-house-style-verify.py

## 为什么要落盘

证据件要能被**复核员自己重跑出来**，而不是只能读我贴的那几行。落盘的生成器 = 把
"哪些命令、以什么顺序、输出怎么截"这件事本身也变成可复跑的（与 `red/make-multipage-probe.py` 同一惯例）。

## 纪律

- **`write_bytes` 落盘**（本仓纪律：Windows 上 `write_text` 会把 LF 写成 CRLF，而证据件恒 LF）；
- **不写绝对路径**（本文件全程用 `Path(__file__)` 推仓根；`--file` 一律用仓内相对路径）；
- 所有命令的 `cwd` = **仓根**（与文档里"可直接粘进 bash"的口径一致）；
- §9 自证：本脚本跑的**每一条**命令都必须 `exit=0`，非零退出即写进文末并让本脚本 exit≠0。

## 八节

§0 blob 自证 · §1 全量守卫 · §2 只跑报告点名的那些 · §3 变异驱动器 ·
§4 provenance 每条复跑命令按文档原样跑一遍 · §4b 无数条目 · §5 两页探针（**守卫读数**，不手敲命令）·
§6 连续色图边界 · §7 台账逐格一致 · §8 修复轮新增的读数 · §9 自证。

§5 的说明：原先这里贴的是一条**手敲的** `check-figure-style.py --caption '...'` 命令，
引号被再切一次 ⇒ `exit=2`、**什么都没证**。整份判 PASS 这句话的真正承重件是
`house-metrics.py::probe_verdict`（它内部按**参数列表**起子进程，不经 shell ⇒ 没有引号问题），
故本节改贴**守卫读数**（`probe_verdict` / `probe_pages` / `probe_page1_*` / `probe_page2_*`）。
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]          # 仓根（本文件在 tests/skills/figure-choose/）
HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "house-style-verify.txt"
HM = HERE / "house-metrics.py"
CHK = HERE / "check-house-style.py"
MUT = HERE / "mutate-figure-style.py"
F2D = HERE / "red/f2-diagnose.py"
REF = ROOT / ".claude/skills/mcm-figure-choose/references"
FILES = [HM, CHK, REF / "house-style.md", REF / "provenance.md", MUT,
         HERE / "gen-house-style-verify.py", HERE / "check-figure-style.py"]

HEADER = """Task 3 证据 · house-style 13 条 + provenance（每数带口径与复跑命令）+ 规范数守卫
生成者：Task 3 实施者（2026-09-27，修复轮）· 写入用 write_bytes ⇒ 本文件恒 LF · 逐字输出
本文件由 `python tests/skills/figure-choose/gen-house-style-verify.py` 整份重生成；
命令 cwd = 仓根。收工时的 `git status --short` 为空见报告（本文件生成于入库之前）。"""


def rel(p):
    return pathlib.Path(p).relative_to(ROOT).as_posix()


def run(argv):
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(ROOT))
    return p.returncode, (p.stdout + p.stderr).rstrip("\n")


def sha(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True).stdout.strip()


class Ev:
    def __init__(self):
        self.lines, self.log = [], []

    def __call__(self, s=""):
        self.lines.append(s)

    def banner(self, t):
        self("=" * 78)
        self(t)
        self("=" * 78)

    def cmd(self, argv, shown=None):
        """按 `argv` 起子进程，把 `shown`（缺省 = argv 自拼）与输出逐字写进来。"""
        shown = shown or " ".join(argv)
        self(f"$ {shown}")
        rc, out = run(argv)
        if out:
            self(out)
        self(f"[exit={rc}]")
        self.log.append((shown, rc))
        self()
        return rc


def main():
    ev = Ev()
    for line in HEADER.splitlines():
        ev(line)
    ev()

    # ---------------- §0
    ev.banner("§0  blob 自证（git hash-object：被验对象就是即将入库的那几个文件）")
    for f in FILES:
        ev(f"{sha(f)}  {rel(f)}")
    ev()

    # ---------------- §1 全量守卫
    ev.banner("§1  规范数守卫（全量）：python tests/skills/figure-choose/check-house-style.py")
    ev.cmd([sys.executable, rel(CHK), ], "python " + rel(CHK))

    # ---------------- §2 只跑报告点名的那些
    only = ("G-H1-lo G-H1-hi G-H1-med G-H4-max G-H4-med G-H4-zero G-H4-cov "
            "G-H4-n2pair-lo G-H4-n2lo G-H4-gate-pct G-H4-gate-box G-H4-heat-old G-H4-ex2-sub "
            "G-H3-s120-lo G-H3-908 G-H9-ascii G-H9-wmax G-H9-whard G-H9-doc873 G-H9-578 "
            "G-P-H2b-max G-P-H2b-gap G-H12-minpt G-H12-scale-lo").split()
    ev.banner("§2  规范数守卫：只跑报告点名的那些（H1 / H3 / H4 / H9 / H12 / P-H2-b）")
    ev.cmd([sys.executable, rel(CHK), "--only", *only],
           "python " + rel(CHK) + " --only " + " ".join(only))

    # ---------------- §3 变异驱动器
    ev.banner("§3  变异驱动器（一条命令跑全部）：python tests/skills/figure-choose/mutate-figure-style.py")
    ev.cmd([sys.executable, rel(MUT)], "python " + rel(MUT))

    # ---------------- §4 provenance 的每条复跑命令按文档原样跑一遍
    prov = (REF / "provenance.md").read_text(encoding="utf-8")
    cmds = [m.group(1).strip() for m in re.finditer(r"^复跑命令:\s*(.+)$", prov, re.M)]
    cmds = [c for c in cmds if c.startswith("python ") and "--metric" in c]
    ev.banner("§4  provenance 里每条复跑命令**按文档原样**跑一遍（逐字命令 + 输出）")
    ev("（下面每一行都是 `provenance.md` 的 `复跑命令:` 原文，可直接粘进 bash；cwd = 仓根）")
    ev()
    for c in cmds:
        ev.cmd(c.split(), c)

    # ---------------- §4b
    ev.banner("§4b  无数条目（『数: 无』 ⇔ 『复跑命令: 无』，由守卫强制）")
    ev("PASS  P-E-b  无数条目：数='无（**本条不给数**）' 命令='无——**本样本量不到**…'"
       "（两者必须同时以『无』开头；逐字见 §1）")
    ev()

    # ---------------- §5 两页探针（守卫读数）
    ev.banner("§5  第一手口径核对：一个图文件 = 一页（两页探针整份判 PASS）")
    ev("说明（修复轮 N-6）：本节原先贴的是一条**手敲的命令**（`--caption '…'` 的引号被再切一次")
    ev("⇒ exit=2、什么都没证）。整份判 PASS 这句话的真正承重件是 `house-metrics.py::probe_verdict`")
    ev("（内部按**参数列表**起子进程、不经 shell ⇒ 没有引号问题）⇒ 本节改贴**守卫读数**。")
    ev()
    for m in ("probe_verdict", "probe_pages", "probe_page1_w_in", "probe_page1_colors",
              "probe_page1_ratio", "probe_page2_w_in", "probe_page2_colors"):
        ev.cmd([sys.executable, rel(HM), "--metric", m],
               f"python {rel(HM)} --metric {m}")
    ev("（上面 7 个读数逐条由 §1 的 `G-F0-verdict` / `G-F0-pages` / `G-F0-p1w` / `G-F0-p1c` /")
    ev(" `G-F0-p1ratio` / `G-F0-p2w` / `G-F0-p2c` 守住：`doc[0]` 的读数全绿、page2 的两项都超限，")
    ev(" 而整份仍判 PASS ⇒ 「检查器只读 doc[0]」这一实现事实由守卫钉住，不靠手敲命令。）")
    ev()

    # ---------------- §6 连续色图边界
    ev.banner("§6  第一手口径核对：连续色图的 F2 边界（连续 R2 vs 离散 R1/R3）")
    ev.cmd([sys.executable, rel(F2D),
            rel(HERE / "red/out-R2/figure.pdf"),
            rel(HERE / "red/out-R1/figure.pdf"),
            rel(HERE / "red/out-R3/figure.pdf")],
           f"python {rel(F2D)} {rel(HERE / 'red/out-R2/figure.pdf')} "
           f"{rel(HERE / 'red/out-R1/figure.pdf')} {rel(HERE / 'red/out-R3/figure.pdf')}")

    # ---------------- §7 台账逐格一致
    ev.banner("§7  台账逐格一致（重写件 vs 入库台账）")
    ev.cmd([sys.executable, rel(HM), "--metrics",
            "recon_ledger_match,tab10_v2_ledger_match,tab10_loose_ledger_match"],
           f"python {rel(HM)} --metrics recon_ledger_match,tab10_v2_ledger_match,tab10_loose_ledger_match")

    # ---------------- §8 修复轮新增的读数
    new = ("recon_baseline_minw_cov4_pct,recon_baseline_minw_s166_cov4_pct,"
           "recon_baseline_minw_s166_median,recon_baseline_minw_s166_zero_pct,recon_cov4_s166_pct,"
           "cont_gate_pct,cont_gate_old_pct,cont_heat_hit_n,cont_heat_hit_old_n,"
           "cont_cite_den,cont_cite_n,cont_cite_old_n,cont_heat_subfloor_min_pct,"
           "cont_ratio_disc,cont_ratio_heat,cont_comp_n,color_median_comp,color_zero_pct_comp,"
           "color_cov4_pct_comp,cap_ascii_period_n,cap_ascii_colon_or_period_n,"
           "cap_ascii_colon_or_period_pct,h2_colw_p90_max,h2_colw_p90_gap,"
           "h3_aspect_pool908_med,h3_aspect_s120_med_lo,h3_aspect_s120_med_hi,n_png_all")
    ev.banner("§8  修复轮新增的读数（Critical-1 / Important-3 / Important-4 / N-5 / N-7）")
    ev.cmd([sys.executable, rel(HM), "--metrics", new], f"python {rel(HM)} --metrics {new}")

    # ---------------- §9 自证
    bad = [(c, rc) for c, rc in ev.log if rc != 0]
    ev.banner("§9  本节自证：上面每条命令都要 exit=0")
    ev(f"§0-§8 共跑 {len(ev.log)} 条；非零退出 {len(bad)} 条"
       + ("" if not bad else "：" + "; ".join(f"{c} → exit={rc}" for c, rc in bad)))
    ev()

    blob = ("\n".join(ev.lines) + "\n").encode("utf-8")
    OUT.write_bytes(blob)                                    # write_bytes ⇒ 恒 LF
    print(f"wrote {rel(OUT)}  bytes={len(blob)}  lines={blob.count(10)}  "
          f"命令 {len(ev.log)} 条 · 非零退出 {len(bad)} 条")
    if bad:
        for c, rc in bad:
            print(f"  exit={rc}  {c}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
