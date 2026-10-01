#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 2：生成 tests/skills/figure-choose/red/README.md。

要点：三份场景正文**逐字**内联（直接从 brief-R*.md 读字节），保证 Task 6 的 GREEN
拿到的场景与 RED **同一份**，不存在"改写过的副本"。写入用 write_bytes。
"""
import pathlib

# 锚 `__file__`，不是 cwd：本目录下另四个脚本都这么锚。用 cwd 相对路径时，
# 在别处跑 `make-readme.py` 会 FileNotFoundError（读不到 brief-R*.md）。
RED = pathlib.Path(__file__).resolve().parent

HEADER = """# `red/` - RED 基线（无 skill 场景下的产物）

> ## !! 本目录含泄题风险文件，绝不给写手 !!
>
> **点名（四份并列，没有"次要"档）**：`red-evidence.md` / `judge.md` / `README.md` /
> **`writer-self-reports.md`**。它们写明了**期望的失败形态**（图宽比、配色数、图注形态、
> 饼图那条规则）；其中 `writer-self-reports.md` 是**最完整**的一份 —— 它逐字含写手对
> 规范表（H1-H13）的引述，以及"这些阈值我都知道"的自述。任何"写手" agent 一旦读到
> 其中**任何一份**，产出的就不再是 RED 基线。
>
> **这个点名不是穷举**：第 2 节的**"证据"与"工具"两栏整体同样不给写手**，
> 派写手时提示词只给**场景 brief 的路径**与**产物输出目录**。

## 1. 三份场景正文（Task 6 的 GREEN 必须逐字复用同一份，不许改写）

下面三节是 `brief-R1.md` / `brief-R2.md` / `brief-R3.md` 的**逐字**内联副本
（脚本从这三个文件的字节直接读入，不经过改写）。**权威副本是那三个文件**；
若本文件与它们不一致，以文件为准。

"""

FOOTER = """## 2. 目录内容

**场景（只给写手的东西）**

| 路径 | 是什么 |
| :--- | :--- |
| `brief-R{1,2,3}.md` | 场景正文。**权威副本**。 |
| `out-R{1,2,3}/make_figure.py` | 写手产出的生成脚本（无参可跑、离线、可复算） |
| `out-R{1,2,3}/figure.pdf` · `figure.png` | 写手导出的图（PDF 为矢量主产物，PNG 为同源栅格） |
| `out-R{1,2,3}/caption.txt` | 写手产出的图注文本（**不由脚本再生**，见 `red-evidence.md` §7） |

**证据（⚠️ 与文首点名的泄题件同类 —— 这一栏整体不给写手，不只是被点名的那几份）**

| 路径 | 是什么 |
| :--- | :--- |
| `red-evidence.md` | 机械层逐字读数 + 红绿表 + 两条遗留风险的实测回答 + 修复记录 |
| `judge.md` | 独立判者的判断层判词（**判者未看任何规范文件**） |
| `writer-self-reports.md` | 六个写手 + 判者的**派发提示词与完整自报原文**（逐字节，抢救自仓外 transcript）。**⚠️ 本栏泄题风险最高的一份**：写手自报里逐字引了规范表（H1-H13）并写明"按这些阈值选的" |
| `f2-boxes.txt` | F2 全量色箱取证输出（341 行；由 `f2-diagnose.py --out` 用 `write_bytes` 落盘，可逐字节复现） |
| `multipage-probe.pdf` | §6"只判第 1 页"的两页探针（由 `make-multipage-probe.py` 生成，1926 B） |
| `truth.py` | 场景地面真值（R1 的 L1 相似度排序 / R2 的相关系数） |

**工具（造上面那些证据的脚本 —— 放在这里，不放 gitignored 的 `.superpowers/`）**
（⚠️ 这些脚本也**不给写手**：`f2-diagnose.py` 直接 import 检查器，等于把阈值常量摆出来）

| 路径 | 是什么 |
| :--- | :--- |
| `f2-diagnose.py` | F2 每个色箱占比的取证工具。**import** `check-figure-style.py` 的 `raster_rgb`/`color_count`（不抄），并对重写的取箱步骤做逐例一致性断言 |
| `verify-reproducible.py` | §7"逐字节重生成"：把 `make_figure.py` 单独复制到仓外跑，再与 `HEAD:` 的 blob 比 |
| `make-multipage-probe.py` | 生成 `multipage-probe.pdf`（固定 CreationDate，可重复生成） |
| `rescue-transcripts.py` | 从仓外 transcript 摘出 `writer-self-reports.md` 的那个一次性脚本 |
| `make-briefs.py` · `make-readme.py` · `make-evidence.py` | 生成 `brief-R*.md` · 本文件 · `red-evidence.md` |

## 3. 两层判据的分工（本目录要留的现场证据）

- **机械层**（`check-figure-style.py`）：F1 图宽比 · F2 彩色主色数 · F3a-d 图注形态。
  可判、可复算、**一字不改**地两边同用。
- **判断层**（独立判者）：图型选得对不对 —— **机械层抓不到这一层**。
  典型反例：饼图也常常 <=4 色，F2 会放它过去；而"构成数据不该用饼图"是判断题。
  **本目录的 `judge.md` 就是这一层的现场证据。**
- **⚠️ 两层都不管的一层**：**"图里每个几何元素都画对了没有"**。
  现场反例：`out-R1/make_figure.py:174-178` 把三族网格线里的两族算成了同一个数组
  （一族从未画出、一族画了两遍），**机械层与判断层都没有报它**（详见 `red-evidence.md` §4-3 / §8 形态 8）。
  **不许把"两层都判过了"读成"这张图没问题"。**
- **⚠️ 隔离强度的边界**：写手"只读了那一份 brief"这件事**只有自报、没有沙箱可证**；
  能复核的只有"未给它们继承的上下文"（⇒ 未用 `fork`，实测首条 user 消息就是那一条提示词）。
  详见 `red-evidence.md` §0.1 与 `writer-self-reports.md` 顶部。

## 4. 与 GREEN 的比对口径

Task 6 用**同一份场景**（第 1 节逐字复用）、**同一把尺**（`check-figure-style.py`
一字不改、同一 `--textwidth-in 6.31`）跑 GREEN，再做 RED/GREEN 并列红绿表。
**不许**因为 GREEN 没改善就调判据。
"""


def main():
    parts = [HEADER]
    for n, title in (("R1", "场景 R1（构成数据）"),
                     ("R2", "场景 R2（多变量对比 / 相关）"),
                     ("R3", "场景 R3（交付形态）")):
        body = (RED / f"brief-{n}.md").read_bytes().decode("utf-8")
        parts.append(f"### {title} —— 逐字内联自 `brief-{n}.md`\n\n")
        parts.append("````markdown\n")
        parts.append(body)
        parts.append("````\n\n")
    parts.append(FOOTER)
    out = "".join(parts).encode("utf-8")
    p = RED / "README.md"
    p.write_bytes(out)
    rel = p.relative_to(RED.parents[3]).as_posix()      # 只打印仓库相对路径（同 rescue-transcripts.py）
    print(f"{rel}  bytes={len(out)}")


if __name__ == "__main__":
    main()
