#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 2 Step 1：落三份 RED 场景 brief（只给场景，不给期望）。

本仓纪律：写入一律 write_bytes（禁 write_text）。本脚本是**一次性备料工具**，不是证据；
证据是它落下的三份 brief 本身（逐字入受版本控制的 tests/skills/figure-choose/red/）。
"""
import pathlib

# 锚 `__file__`，不是 cwd：旧版用 cwd 相对路径，在别处跑会把三份 brief **静默写进
# `<cwd>/tests/...`**（`mkdir(parents=True, exist_ok=True)` 让这失败不报错）。
RED = pathlib.Path(__file__).resolve().parent

R1 = """# Brief R1 - district vulnerability composition

A regional risk assessment divides a study area into six districts (A-F). For each
district, the share of its land area falling into each of three vulnerability tiers
(low, medium, high) has been measured. Within every district the three shares sum to
1.00.

| District | low  | medium | high |
|----------|------|--------|------|
| A        | 0.42 | 0.35   | 0.23 |
| B        | 0.31 | 0.44   | 0.25 |
| C        | 0.55 | 0.30   | 0.15 |
| D        | 0.28 | 0.47   | 0.25 |
| E        | 0.37 | 0.38   | 0.25 |
| F        | 0.50 | 0.33   | 0.17 |

Question to answer with the figure: describe the vulnerability composition of each
district, and support a judgement about which two districts have the most similar
structure.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
"""

R2 = """# Brief R2 - drivers of historical disaster counts

A regional risk assessment divides a study area into six districts (A-F). Five
attributes have been measured for each district.

| District | Population density (people/km2) | Mean slope (degrees) | Vegetation cover (fraction of area) | Historical disaster count | Infrastructure index (0-100) |
|----------|--------------------------------|----------------------|-------------------------------------|---------------------------|------------------------------|
| A        | 820                            | 3.2                  | 0.61                                | 12                        | 74                           |
| B        | 640                            | 11.5                 | 0.58                                | 31                        | 72                           |
| C        | 610                            | 2.4                  | 0.72                                | 8                         | 81                           |
| D        | 1210                           | 14.8                 | 0.41                                | 38                        | 55                           |
| E        | 990                            | 7.1                  | 0.49                                | 16                        | 66                           |
| F        | 1750                           | 5.0                  | 0.55                                | 24                        | 70                           |

Question to answer with the figure: identify which factor is most strongly correlated
with the historical disaster count, and describe the similarity between districts.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
"""

R3 = """# Brief R3 - district vulnerability composition, paper-ready

A regional risk assessment divides a study area into six districts (A-F). For each
district, the share of its land area falling into each of three vulnerability tiers
(low, medium, high) has been measured. Within every district the three shares sum to
1.00.

| District | low  | medium | high |
|----------|------|--------|------|
| A        | 0.42 | 0.35   | 0.23 |
| B        | 0.31 | 0.44   | 0.25 |
| C        | 0.55 | 0.30   | 0.15 |
| D        | 0.28 | 0.47   | 0.25 |
| E        | 0.37 | 0.38   | 0.25 |
| F        | 0.50 | 0.33   | 0.17 |

Question to answer with the figure: describe the vulnerability composition of each
district, and support a judgement about which two districts have the most similar
structure. I need one figure (with its caption) that I can paste straight into the
body text of my paper.

Deliverables - write all of these into the output directory:

1. `make_figure.py` - a Python script that regenerates the figure from the numbers
   above, deterministically, with no network access and no manual steps.
2. the exported figure itself, as `figure.pdf` or `figure.png`.
3. `caption.txt` - the figure caption, in English, as plain text.
"""


def main():
    RED.mkdir(parents=True, exist_ok=True)
    for name, body in (("brief-R1.md", R1), ("brief-R2.md", R2), ("brief-R3.md", R3)):
        p = RED / name
        p.write_bytes(body.encode("utf-8"))
        rel = p.relative_to(RED.parents[3]).as_posix()  # 只打印仓库相对路径
        print(f"{rel}  bytes={len(p.read_bytes())}")
    for d in ("out-R1", "out-R2", "out-R3"):
        (RED / d).mkdir(parents=True, exist_ok=True)
        rel = (RED / d).relative_to(RED.parents[3]).as_posix()
        print(f"{rel}/  (empty, awaiting writer)")


if __name__ == "__main__":
    main()
