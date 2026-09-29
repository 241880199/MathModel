#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D13 探针：`corpus/` 下有没有**可直接被 Python 读**的题目数据？

只读；不写任何东西。列清单 + 真读一次（pandas）。

复跑（仓根）：
  python tests/m3-plot-recon/d13_real_data.py
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
CORPUS = ROOT / "corpus"
EXTS = {".csv", ".xlsx", ".xls", ".json", ".dat", ".tsv"}


def main():
    print(f"扫的根 = {CORPUS.relative_to(ROOT)}（递归；跳过以 `.` 开头与 build/）")
    hits = []
    for p in CORPUS.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in EXTS:
            hits.append(p)
    print(f"直接可读候选（{'/'.join(sorted(EXTS))}）共 {len(hits)} 个：")
    for p in sorted(hits):
        print(f"  {p.relative_to(ROOT).as_posix()}   {p.stat().st_size} B")

    # 压缩包形态：需要先解压，不算"直接可读"
    zips = sorted(p for p in CORPUS.rglob("*.zip") if p.is_file())
    print(f"\n压缩包形态（需先解压，**不算直接可读**）共 {len(zips)} 个：")
    for p in zips:
        print(f"  {p.relative_to(ROOT).as_posix()}   {p.stat().st_size} B")

    print("\n" + "=" * 78)
    print("真读一次（pandas）：")
    import pandas as pd
    print(f"pandas = {pd.__version__}")
    for p in sorted(hits):
        print(f"--- {p.relative_to(ROOT).as_posix()} ---")
        try:
            if p.suffix.lower() == ".csv":
                df = pd.read_csv(p)
                print(f"    rows={len(df)} cols={len(df.columns)}")
            elif p.suffix.lower() in (".xlsx", ".xls"):
                xl = pd.ExcelFile(p)
                df = xl.parse(xl.sheet_names[0])
                print(f"    sheets={xl.sheet_names} · 首表 rows={len(df)} cols={len(df.columns)}")
            elif p.suffix.lower() == ".tsv":
                df = pd.read_csv(p, sep="\t")
                print(f"    rows={len(df)} cols={len(df.columns)}")
            else:
                continue
            print(f"    列名（前 6）: {list(df.columns)[:6]}")
        except Exception as e:                              # noqa: BLE001
            print(f"    **读不出**：{type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
