#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""★ 抢救：把 Task 6 GREEN 三个写手与一位判者的**提示词 + 自报**逐字节搬进受版本控制的仓。

为什么必须抢救：`.superpowers/` 是 gitignored，**subagent transcript 更在仓外**，
随时可能被清理。Task 6 的**公平性主张**（"GREEN 与 RED 的差别只有'能不能读 skill'这一条"）
唯一不可再生的证据就是这些原文 —— 丢了就只剩"我记得"。**本文件与 RED 的同名脚本同款同口径**。

来源：Claude Code 的 subagent transcript（仓外，`<claude-home>/projects/<slug>/<session>/subagents/`）。
本文件里的 `AGENTS` 用 **transcript 文件名**（相对名，含 agent id）定位，不含绝对路径。

用法：
  python tests/skills/figure-choose/green/rescue-transcripts.py <subagents 目录>
产物：`tests/skills/figure-choose/green/green-self-reports.md`（`write_bytes`，LF）。

摘录口径（**不加改**）：每个 agent 取两段——
  ① 首条 `user` 消息 = 派发给它的提示词（逐字节）；
  ② `SubagentHandback` 工具的 `message` 入参 = 它回给调度者的完整报告（逐字节）。
本脚本**不加任何删节**：两段引用之间没有被本脚本删掉的内容（脚本只加标题/说明/字符数行）。

⚠️ **本抢救件也含泄题风险**（写手自报里可能引用规范内容），与 `green-evidence.md` /
`green/judge-green.md` 同案看待：**不给任何"写手"agent**。
"""
import json
import pathlib
import re
import sys

GREEN = pathlib.Path(__file__).resolve().parent

# ---- 唯一的加工：绝对路径掩码（本仓规定：报告与证据不写绝对路径）----
# 原文里写手自己写了两种绝对路径：仓外临时目录、以及本仓的根。掩码只动这两类，
# 且**逐处计数**后写进文件头 —— 标签不许比事实更强，加工了几处就得说几处。
TMP_RE = re.compile(r"[A-Za-z]:[\\/][^\s`\"')\]]*?AppData[\\/]Local[\\/]Temp[\\/]m3-t6-green",
                    re.IGNORECASE)
REPO_RE = re.compile(r"[A-Za-z]:[\\/](?:[^\\/\s`\"')\]]+[\\/])*?数学建模")
MASKS = ((TMP_RE, "<TMP>/m3-t6-green"), (REPO_RE, "<REPO>"))

AGENTS = [
    # (标签, transcript 文件名, 说明)
    ("R1-writer-green", "agent-adec53c15412da08f.jsonl",
     "GREEN R1 写手（可读 skill；本 GREEN 产物的来源）"),
    ("R2-writer-green", "agent-a47052cc8583ef729.jsonl",
     "GREEN R2 写手（可读 skill；本 GREEN 产物的来源）"),
    ("R3-writer-green", "agent-a63638435c0111769.jsonl",
     "GREEN R3 写手（可读 skill；本 GREEN 产物的来源）"),
    ("judge-green", "agent-a6333dc6583bdee21.jsonl",
     "独立判者（GREEN 轮；只读产物，未参与写作，未读 skill）"),
]


def read_agent(path):
    """返回 (首条 user 消息, SubagentHandback 的 message)；都逐字节原文。

    注意：transcript 里 `content` 既可能是字符串（普通消息），也可能是 part 列表
    （带 tool_use 的消息），两条形态都要吃。
    """
    first_user, handback = None, None
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(raw)
        except Exception:                       # 个别行可能是被截断的半行，跳过
            continue
        m = o.get("message") or {}
        c = m.get("content")
        if isinstance(c, str):
            if m.get("role") == "user" and first_user is None and not c.startswith("<"):
                first_user = c
            continue
        if not isinstance(c, list):
            continue
        for part in c:
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text" and m.get("role") == "user" and first_user is None:
                t = part.get("text") or ""
                if not t.startswith("<"):       # 跳过系统注入的块
                    first_user = t
            if part.get("type") == "tool_use" and part.get("name") == "SubagentHandback":
                handback = (part.get("input") or {}).get("message")
    return first_user, handback


N_MASKED = 0


def mask(text):
    """把两类绝对路径换成 `<TMP>/m3-t6-green` / `<REPO>`，并累计处数。"""
    global N_MASKED
    for pat, rep in MASKS:
        text, n = pat.subn(rep, text)
        N_MASKED += n
    return text


def main():
    if len(sys.argv) != 2:
        print("usage: rescue-transcripts.py <subagents dir>", file=sys.stderr)
        sys.exit(2)
    src = pathlib.Path(sys.argv[1])
    out = []

    for tag, fname, note in AGENTS:
        p = src / fname
        if not p.exists():
            out.append(f"\n## {tag} —— **缺失**（transcript `{fname}` 不在给定目录里）\n")
            continue
        prompt, handback = read_agent(p)
        raw_p, raw_h = len(prompt or ""), len(handback or "")
        prompt, handback = mask(prompt or ""), mask(handback or "")
        out.append(f"\n{'=' * 78}\n## {tag}\n\n- 说明：{note}\n"
                   f"- transcript：`{fname}`（仓外文件，本行只记文件名，不记绝对路径）\n"
                   f"- 首条 user 消息：**{raw_p}** 字符（原文；掩码后 {len(prompt)}）\n"
                   f"- SubagentHandback：**{raw_h}** 字符（原文；掩码后 {len(handback)}）\n\n"
                   "### ① 派发提示词（原文）\n\n"
                   "```text\n" + prompt + "\n```\n\n"
                   "### ② 自报 / 报告（原文）\n\n```text\n"
                   + handback + "\n```\n")

    head = f"""# Task 6 GREEN 的派发提示词与写手/判者自报（抢救件）

> ## !! 泄题风险件：绝不给写手 !!
>
> 本文件逐字收录 **GREEN 写手的自报**与**派发提示词**；自报里可能引用 skill 的规则编号或
> 数值，且**提示词本身就是 Task 6 派发 GREEN 的口径**。任何"写手" agent 读过本文件，
> 产出的就不再是干净的对照件。**与它同案看待的还有** `green-evidence.md` /
> `green/judge-green.md` 与整个 `red/`（点名清单见 `red/README.md` 文首警示头）。

【为什么有这个文件】Task 6 唯一**无法靠单变量复核**的东西是"GREEN 写手到底读到了什么"：
  它只能靠**审计原文**。而这些原文（subagent transcript）在仓外、且 `.superpowers/` 是
  gitignored ⇒ 不搬进受版本控制的目录就随时会丢。本文件由
  `rescue-transcripts.py` 从 transcript 一次性摘录。

【摘录口径】每个 agent 两段，均为原文，**本脚本不加删节**：
  ① 首条 `user` 消息 = 派发的提示词（对本轮，它就是**单独一行**提示词本身 ——
     这一点同时**可复核"未用 fork"**：`fork` 会继承主 agent 上下文，首条消息会是长篇上下文）；
  ② `SubagentHandback` 的 `message` = 它回给调度者的完整报告。
  **不等于"文件里没有省略号"**：文件里出现的省略号（三个句点）**全部**在两段引用
  **内部** —— 是原文作者自己写的简写；**本脚本一处未删**。

【对原文的加工 —— **只有一种**，且逐处计数】写手自己写了**绝对路径**（含 Windows 用户名与
  系统临时目录），本仓规定报告与证据不写绝对路径，故掩码之：仓外临时目录 → `<TMP>/m3-t6-green`，
  仓内根 → `<REPO>`。**本文件共掩码 {N_MASKED} 处**，除此之外两段引用**逐字节未改、未软换行**。
  （本文件里**不是原文**的只有脚本写的那几行：文首这几段【】说明与警示块、每个 agent 的
  标题/说明/`transcript`/`字符数` 行。）

【强度声明（不许下游读过头）】①②是**原文**，但"GREEN 写手是否真的**没有**去读 `red/`"
**只有自报、没有沙箱可证**（没有文件系统审计、没有 syscall 记录）。
自报一致 ≠ 已证；本文件能做的是：把自报存下来，让下游能自己判断。

---
"""
    blob = (head + "".join(out)).encode("utf-8")

    dst = GREEN / "green-self-reports.md"
    dst.write_bytes(blob)
    rel = dst.relative_to(GREEN.parents[3]).as_posix()        # 只打印仓库相对路径
    print(f"wrote {rel}  bytes={len(blob)}  lines={blob.count(chr(10).encode())}"
          f"  masked_paths={N_MASKED}")


if __name__ == "__main__":
    main()
