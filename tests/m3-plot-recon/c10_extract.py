#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C10 探针：能不能从 `house-style.md` **机械抽数** —— 对 H1–H13 逐条试一组正则，
打印**命中文本**（抽不到的就明确列出来）。

只读规范，不改任何文件。正则集是"探路"用的最小集，不是设计。

复跑（仓根）：
  python tests/m3-plot-recon/c10_extract.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOC = ROOT / ".claude/skills/mcm-figure-choose/references/house-style.md"

RES = {
    "小数 \\d+\\.\\d+": r"\d+\.\d+",
    "百分数 \\d+(\\.\\d+)?%": r"\d+(?:\.\d+)?%",
    "带单位 \\d+\\s*(in|pt|词|色|倍|×|dpi)": r"\d+\s*(?:in|pt|词|色|倍|×|dpi)",
    "带界 ≤n / ≥n / <n / >n": r"[≤≥<>]\s*\d+(?:\.\d+)?",
    "区间 a–b / a-b": r"\d+(?:\.\d+)?\s*[–-]\s*\d+(?:\.\d+)?",
    "冒号数值 AX: nn": r"[A-Z]{1,3}\d*:\s*\d+",
    "行内代码 `…`": r"`[^`]+`",
}


def main():
    txt = DOC.read_bytes().decode("utf-8")
    blocks = list(re.finditer(r"^### (H\d+)\. ([^\n]*)\n(.*?)(?=^### |\Z)", txt, re.M | re.S))
    print(f"规范 = {DOC}")
    print(f"`### H<n>.` 条目 {len(blocks)} 个")
    for m in blocks:
        hid, title, body = m.group(1), m.group(2), m.group(3)
        # 「规则」那一行 = 可操作层；「依据」= 分布读数层
        rule = re.search(r"^\*\*规则\*\*[：:](.*)$", body, re.M)
        rule_txt = rule.group(1) if rule else "（没有『**规则**：』行）"
        print("=" * 78)
        print(f"{hid}. {title}")
        print(f"  规则行：{rule_txt.strip()}")
        for name, pat in RES.items():
            hits = re.findall(pat, body)
            hits = [h if isinstance(h, str) else h for h in hits]
            uniq = sorted(set(hits))
            shown = "、".join(repr(h) for h in uniq[:8]) + (f" …共{len(hits)}" if len(hits) > 8 else "")
            print(f"    {name:<28} {'命中 ' + str(len(hits)) + ' 处：' + shown if hits else '**抽不到**'}")
        # 规则行里有没有"数"
        rule_nums = re.findall(r"\d+(?:\.\d+)?", rule_txt)
        print(f"  ⇒ 规则行里的数：{rule_nums or '**一个都没有**（没有数的规则）'}")


if __name__ == "__main__":
    main()
