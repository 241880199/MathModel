#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""B5/B6/B7 探针：`K3` 的禁止串全集 + 子串命中表 + `K2` 的指针形态。

**判据一条都不在这里重写**：本脚本 import `check-house-style.py`（本仓 `_load()` 惯用法），
直接调它的 `_k3(txt)` / `_k2(txt)`，所以读数就是**出货仪器今天**的读数。

复跑（仓根）：
  python tests/m3-plot-recon/b567_k2k3_probe.py \
      --checker tests/skills/figure-choose/check-house-style.py
"""
import argparse
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# B6 的受控文本清单（逐条独立喂给 `_k3`：一条一个 txt，互不干扰）
CASES = [
    "dpi=200",
    "figsize=(6.3, 2.6)",
    "savefig(dpi=300)",
    "0.5",
    "10.0",
    "16",
    "1.8",
    "2.42",
    "0.951",
    "< 150 行",
    "SK_MAX_LINES",
    "0.7777",
    "figsize=(6.31, 2.6)",
    "6.31",
    "0.80",
    "axes.prop_cycle",
]

# B7 的指针形态
POINTER_CASES = [
    "references/house-style.md",
    ".claude/skills/mcm-figure-choose/references/house-style.md",
    "house-style.md",
    "mcm-figure-choose/references/house-style.md",
    "见 references/house-style.md §H1",
    "./references/house-style.md",
    "references\\house-style.md",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checker", default=str(ROOT / "tests/skills/figure-choose/check-house-style.py"))
    a = ap.parse_args()
    ck = pathlib.Path(a.checker)
    if not ck.is_absolute():
        ck = ROOT / ck
    mod = _load(ck.resolve(), "check_house_style")
    doc = mod.DOC.read_bytes().decode("utf-8")

    # ---- B5：按 `_k3` 的两条正则**原样现抽**（与 `_k3` 内的表达式逐字相同）
    dec = sorted(set(re.findall(r"\d+\.\d+", doc)))
    tier = sorted(set(re.findall(r"≤\s*\d+|<\s*\d+\s*词", doc)))
    banned = set(dec) | set(tier)
    print("=" * 78)
    print(f"B5  K3 禁止串全集（现抽自 {mod.DOC}）")
    print(f"    正则① = r'\\d+\\.\\d+'  → {len(dec)} 条")
    for s in dec:
        print(f"        {s!r}")
    print(f"    正则② = r'≤\\s*\\d+|<\\s*\\d+\\s*词'  → {len(tier)} 条")
    for s in tier:
        print(f"        {s!r}")
    print(f"    并集 = {len(banned)} 条")
    print(f"    （自证：`_k3` 实跑报的条数应等于上面这个并集）")
    real_ok, real_detail = mod._k3("")
    print(f"    `_k3('')` 实测：ok={real_ok} · {real_detail}")

    # ---- B6：子串命中表
    print("=" * 78)
    print("B6  子串命中实测（每个串**单独**作为一个 txt 喂 `_k3`；全绿 = ok=True）")
    print(f"{'受控文本':<44} {'_k3':<7} 命中/原因")
    print("-" * 110)
    rows = []
    for t in CASES:
        ok, detail = mod._k3(t)
        # 把 detail 里的「命中 ...」那段摘出来
        m = re.search(r"命中 (.+?)（现取）", detail) or re.search(r"命中 (.+?) ·", detail)
        hit = re.search(r"禁止串 \d+ 条（现取）· 命中 (.*?) · 中文数词臂", detail)
        why = hit.group(1) if hit else "?"
        cn = re.search(r"中文命中 (.*)$", detail)
        print(f"{t!r:<44} {'PASS' if ok else 'FAIL':<7} 命中={why} · 中文={cn.group(1) if cn else '?'}")
        rows.append((t, ok, why))

    # ---- B6b：中文数词臂（`_cn_arm`）的受控文本
    print("=" * 78)
    print("B6b 中文数词臂实测（裸值词 = ['七','二十','十七','十二','四']；"
          "`b in txt` 是**裸子串**，不要求上下文）")
    cn_cases = ["四", "四川", "第七步", "十二", "一共二十种", "四色以内", "三色", "两色",
                "子图", "四个子图", "七磅", "图例", "四种图型", "步骤四", "第四版"]
    for t in cn_cases:
        ok, detail = mod._k3(t)
        m = re.search(r"中文命中 (.*)$", detail)
        print(f"  {t!r:<16} {'PASS' if ok else 'FAIL':<5} 中文命中={m.group(1) if m else '?'}")

    # ---- B7：K2 指针形态
    print("=" * 78)
    print("B7  K2 指针形态实测（每种写法**单独**作为一个 txt 喂 `_k2`）")
    print(f"{'写法':<64} {'_k2':<7} 读数")
    print("-" * 120)
    for t in POINTER_CASES:
        ok, detail = mod._k2(t)
        print(f"{t!r:<64} {'PASS' if ok else 'FAIL':<7} {detail}")


if __name__ == "__main__":
    main()
