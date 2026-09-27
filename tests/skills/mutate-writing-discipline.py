#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tests/skills/check-writing-discipline.py` 的**变异驱动器**——一条命令复跑全部变异。

用法：  python tests/skills/mutate-writing-discipline.py [--only M07] [--list]

## 为什么必须落盘（修复轮 3 · 硬要求 1）

修复轮 2 的实施报告自称跑过"9 次变异"，但那支驱动器**不在盘上**（`build/wd-check/` 里只有审计器）
⇒ 复核员**无法独立复现**它自称的那 9 次。本文件因此**入库**：一条命令、逐条变异、每条自带
"期望红"断言、每条还原后**自证逐字节还原**。

## 每条变异做什么

1. 读目标文件的**原始字节**（`rb`），在内存里做**一次**字面替换（替换次数必须恰为 1，否则驱动自己报错）；
2. 用 `write_bytes` 写回（**不用 `Path.write_text()`**——它在 Windows 上会把 LF 写成 CRLF，上一轮已栽过）；
3. 跑检查器，**要求 exit != 0**，且**输出的某条 FAIL 行必须匹配该变异登记的 `expect` 正则**；
4. 用 `write_bytes` 把原始字节写回，再用 **`git hash-object`**（不是裸 `sha256sum`）比对：
   还原后的哈希必须等于**变异前**记下的哈希；若该文件在变异前与 `HEAD` 的 blob 一致，还额外比 `HEAD`。

## 本驱动器的自陈（要与实跑一致）

- 变异条数与红/绿：由末行 `MUT:` 打印（计数命令就是本文件本身）。
- 覆盖：`§2 I-3` 要求的**九条修复每条至少一个"回退即变红"的守卫**，逐条对应见 `FIX_GUARDS`。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECKER = Path(__file__).with_name("check-writing-discipline.py")
DOC = "docs/mcm-writing-discipline.md"
EV = "tests/skills/arch-green-evidence.md"

# (编号, 说明, 文件, 原文, 改文, 期望红的 FAIL 行正则, 期望**不**出现的正则)
MUTATIONS = [
    # ---- 九条修复（F-1..F-9）的"回退即变红"
    ("M01", "F-1：把带 -i 口径的五个数改回大小写敏感那一组", DOC,
     "`out-S1` **7.96‰**、`out-S2` **13.27‰**、`out-S2-p` **13.72‰**、真值 **7.80‰ / 2.82‰**（命中 14 / 16 / 11 / 8 / 1 次）",
     "`out-S1` **4.55‰**、`out-S2` **8.29‰**、`out-S2-p` **7.48‰**、真值 **2.93‰ / 0.00‰**（命中 8 / 10 / 6 / 3 / 0 次）",
     r"A5 F-1 旧口径五个数", None),
    ("M02", "F-2：把“别拿 judge.md:103 当出处”改回“出处见 judge.md:103”", DOC,
     "⚠️ **别拿 `judge.md:103` 当这条的出处**：", "⚠️ **出处见 `judge.md:103`**：",
     r"C2 F-2", None),
    ("M03", "F-3：删掉 root-TTR 的“GREEN 落在真值一带”读法", DOC,
     "，**GREEN 两份是 10.55 / 11.11——就落在真值那一带里**", "，**GREEN 两份也偏高**",
     r"C3 F-3", None),
    ("M04", "F-4：把入站指针 doc:135 改回上一轮的 doc:130", EV,
     "（2026-09-27 由 GREEN 轮复量）\"，`:135`）", "（2026-09-27 由 GREEN 轮复量）\"，`:130`）",
     r"B3 入站指针锚", None),
    ("M05", "F-5：口径从 6 个 alternation 改回 4 个（去掉 not only/not just）", DOC,
     "|not merely|not only|not just|precisely|exactly`（`grep -o -i -E`，大小写不敏感",
     "|not merely|precisely|exactly`（`grep -o -i -E`，大小写不敏感",
     r"C5 F-5", None),
    ("M05b", "F-5b：口径从 6 个改成 7 个（多并一个 alternation）", DOC,
     "|precisely|exactly`（`grep -o -i -E`，大小写不敏感", "|precisely|exactly|moreover`（`grep -o -i -E`，大小写不敏感",
     r"C5 F-5", None),
    ("M06", "F-5c：代码块里的口径从 6 个改回 4 个", DOC,
     "grep -o -i -E 'rather than|not merely|not only|not just|precisely|exactly' | wc -l",
     "grep -o -i -E 'rather than|not merely|precisely|exactly' | wc -l",
     r"C5 F-5", None),
    ("M07", "F-6：删掉“两个来源别混”的分列句", DOC,
     "⚠️ **两个来源别混**：3 与 5 是", "3 与 5 是", r"C6 F-6", None),
    ("M08", "F-7：把 §6.2 改回 §5", DOC,
     "**§6.2**——`### 6.2", "**§5**——`### 6.2", r"C7 F-7", None),
    ("M09", "F-8：把 B5 的落点改回 138-140 那一版", DOC,
     "- **最小可执行读法**（落点 = `judge-green.md:138-141`；",
     "- **最小可执行读法（判词自己用的那条，`judge-green.md:138-140`）**：",
     r"C8 F-8", None),
    ("M10", "F-9：把 λ 定义句的行号改回判词那处错值 :48", DOC,
     "（定义句在 `out-S1-g.md:50`）", "（定义句在 `out-S1-g.md:48`）", r"C9 F-9", None),
    # ---- 本轮（修复轮 3）的三条 Important
    ("M11", "I-1：把那半句改回“只多 This X 这一个变量”", DOC,
     "**相对当时那条 canonical 四 alternation（`rather than|not merely|precisely|exactly`）是两处改动**——"
     "**① 去掉 `exactly`、② 加上 `This \\w+`**——实测得",
     "**只多 `This X` 这一个变量**，实测得", r"C10 I-1", None),
    ("M12", "I-2(b)：把一个落点换成指向**空行**（复核的 M7 同型）", DOC,
     "RED 实测：`out-S1.md:28` 残留一条", "RED 实测：`out-S2.md:28` 残留一条",
     r"B2", None),
    ("M13", "I-2(b)：把 out-S2-g.md:15 换成 :16（该行是空行；复核 M16 同型）", DOC,
     "**而 S2 仍在用 `p`**（`out-S2-g.md:15`）", "**而 S2 仍在用 `p`**（`out-S2-g.md:16`）",
     r"B2", None),
    ("M14", "I-2(c)：把一个落点的行号改成越界值", DOC,
     "`corpus/official/instructions.html:952`", "`corpus/official/instructions.html:999999`",
     r"B2", None),
    ("M15", "I-2(e)：把落点换成另一个**已登记**的落点（文档侧上下文不符）", DOC,
     "`judge-green.md:257` 记作", "`judge-green.md:189` 记作",
     r"B2", None),
    ("M16", "I-2：删掉一个指针，让登记的落点变成孤儿", DOC,
     "§8 第 8 条（`judge-green.md:270`）", "§8 第 8 条（`judge-green.md` §8）",
     r"B2", None),
    ("M17", "M-5：把一个指针改回**裸 `:NN`**（不写文件名）", DOC,
     "`judge-green.md:257` 记作\"**修一条、退一条**\"", "`:257` 记作\"**修一条、退一条**\"",
     r"B1 裸指针零容忍", None),
    ("M18", "M-4：把 A5 口径里的 `-i` 删掉——要**诊断**，不许崩溃（同时演示 E5 口径同宽）", DOC,
     "（模式 `rather than|not merely|precisely|This \\w+`，`grep -o -i -E`",
     "（模式 `rather than|not merely|precisely|This \\w+`，`grep -o -E`",
     r"A5 F-1 旧口径五个数", r"检查器异常"),
    ("M19", "M-2：把未舍入增幅 +5.65% 改掉", DOC,
     "算得 **+5.65%**", "算得 **+5.00%**", r"A4 剔表格行实验", None),
    ("M20", "I-2.4：删掉一个已有〔本文件复算〕标记（修复轮 2 实测“删了它仍绿”）", DOC,
     "**RED 轮的重锤**〔本文件复算〕", "**RED 轮的重锤**", r"D2 覆盖守卫·反向", None),
    ("M21", "I-2.4/§D 反向：把一条 §A 认领正则的锚点整句改掉（认领失效）", DOC,
     "**为什么含表格行**〔本文件复算〕", "**为什么把表格行也算进去**〔本文件复算〕",
     r"D1 覆盖守卫·正向|D3 覆盖守卫·认领存活", None),
    # ---- 修复轮 4：X7 / M-1 / I-2 机器断言 / X1 极性 / X4 挂牌
    ("M22", "X7：把区间落点的**止行**改小（`183-186`→`183-185`，半角）", DOC,
     "`judge-green.md:183-186`", "`judge-green.md:183-185`", r"B2 出站指针全扫", None),
    ("M23", "X7：同一处改成**全角破折号**并同时改小止行（`183-186`→`183–185`）", DOC,
     "`judge-green.md:183-186`", "`judge-green.md:183–185`", r"B2 出站指针全扫", None),
    ("M24", "M-1：删掉自检件里的**一个 `guard(...)` 调用**（分母钉死 ⇒ 应立刻红）",
     "tests/skills/check-writing-discipline.py",
     '    guard("E4 容差自述", not bad, "; ".join(bad))\n', "",
     r"E0 守卫名册", None),
    ("M25", "I-2：把头部自陈的**指针条数**改错（107→108）", DOC,
     "本文件共 **107 条**出站指针", "本文件共 **108 条**出站指针", r"E1 头部自陈", None),
    ("M26", "容差：把文档的 `±1pp` 改成 `±3pp`（脚本常量没动）", DOC,
     "**±1pp** 容差", "**±3pp** 容差", r"E4 容差自述", None),
    ("M28", "口径前提：给 canonical 口径多并一个**真值侧命中**的 alternation", DOC,
     "precisely|exactly' | wc -l", "precisely|exactly|Moreover' | wc -l", r"E6 基线非零", None),
    ("M29", "自查清单条数：把 `15 条` 改成 `14 条`", DOC,
     "**15 条**〔机器守卫：E7", "**14 条**〔机器守卫：E7", r"E7 自查清单条数", None),
    ("M30", "This-X 五份：把 `+1` 改成 `+2`", DOC,
     "五份各 **+7 / +9 / +7 / +8 / +1**", "五份各 **+7 / +9 / +7 / +8 / +2**",
     r"E8 This-X 复算", None),
    ("M31", "缺项基数：`还缺两样` → `还缺三样`", DOC,
     "还缺两样", "还缺三样", r"E10 缺项基数", None),
    ("M32", "X1：保留 hint 关键词，把**方向**写反（反证→支撑）", DOC,
     "引它反而**反证**本条", "引它即可**支撑**本条", r"E9 方向性断言极性", None),
    ("M33", "X1：把该处引的**判词列值**改错（S1 列 0→1）", DOC,
     "其 S1 列记 **0**", "其 S1 列记 **1**", r"E9 方向性断言极性", None),
    ("M34", "X4：删掉一个已有的〔判词读数〕标记", DOC,
     "〔判词读数〕两侧都是", "两侧都是", r"E3 判词读数挂牌", None),
    ("M35", "无守卫面：把文档声明的数改错（`1` 条→`0` 条）", DOC,
     "机器守卫覆盖不到的：`1` 条", "机器守卫覆盖不到的：`0` 条", r"E2 无守卫面计数", None),
    ("M36", "X4 反向：给一个**没登记**的行挂上〔判词读数〕", DOC,
     "判据原文见 `judge.md:224`", "〔判词读数〕判据原文见 `judge.md:224`", r"E3 判词读数挂牌", None),
    ("M37", "X7：把已登记的**单点**写成**未登记的区间**（`136-142`→`136-143`）", DOC,
     "`judge-green.md:136-142`", "`judge-green.md:136-143`", r"B2 出站指针全扫", None),
    # ---- 修复轮 5（收口轮）：I-1 / I-2 / M-4b / M-1 残余
    ("M38", "M-1 残余：**掏空守卫体**（期望值字面 True + detail 空；复核 G5d 的那一手）⇒ E12 必须红",
     "tests/skills/check-writing-discipline.py",
     '    guard("E4 容差自述", not bad, "; ".join(bad))\n', '    guard("E4 容差自述", True, "")\n',
     r"E12 守卫体完整性", None),
    ("M39", "I-1：把本节自陈数《降掉的 13 条》改回上一轮的错值 9（修复轮 4 复核实测：三种改法全绿）", DOC,
     "**降掉的 13 条**", "**降掉的 9 条**", r"E2 无守卫面计数", None),
    ("M40", "I-1：把本节另一个自陈数《剩下的 1 条》改错（1→7）", DOC,
     "**剩下的 1 条**", "**剩下的 7 条**", r"E2 无守卫面计数", None),
    ("M41", "I-2：往文档里塞一行**带读数形态数字、又没被任何名册登记的行** ⇒ 普查必须红（E2）", DOC,
     "**那是对已交付 skill 的改动，须单独走一遍流程**。",
     "**那是对已交付 skill 的改动，须单独走一遍流程**（本节共 **99 条**）。",
     r"E2 无守卫面计数", None),
    ("M42", "M-4b：只改**文档代码块**里的正文区间（`1,109`→`1,50`，A1 的 `# 1759` 不动）"
             " ⇒ 正文区间不再有两份，A1 立刻红", DOC,
     "sed -n '1,109p' tests/skills/arch-cases/out-S1.md   | wc -w   # 1759",
     "sed -n '1,50p' tests/skills/arch-cases/out-S1.md   | wc -w   # 1759",
     r"A1 C2 词数", None),
    ("M43", "I-2：把**第二处**《Q1–Q13 共 13 条》改错（13→14）——E11 要核**每一处**", DOC,
     "**Q1–Q13 共 13 条**〔机器守卫：E11", "**Q1–Q13 共 14 条**〔机器守卫：E11",
     r"E11 判分表条数", None),
]

# 九条修复 × 守卫：修复编号 -> 演示它"回退即变红"的变异编号
FIX_GUARDS = {
    "F-1": ("M01", "A5 F-1 旧口径五个数"),
    "F-2": ("M02", "C2 F-2"),
    "F-3": ("M03", "C3 F-3"),
    "F-4": ("M04", "B3 入站指针锚（F-4 回归守卫）"),
    "F-5": ("M05 + M05b + M06（双向：6→4、6→7、代码块 6→4）", "C5 F-5 / A2 / A3"),
    "F-6": ("M07", "C6 F-6"),
    "F-7": ("M08", "C7 F-7"),
    "F-8": ("M09", "C8 F-8"),
    "F-9": ("M10", "C9 F-9"),
}
EXTRA_GUARDS = {
    "I-1（修复轮 3）": ("M11", "C10 I-1"),
    "I-2(a)(b)(c)(e) 指针面": ("M12 / M13 / M14 / M15 / M16", "B2 出站指针全扫"),
    "M-5 裸指针": ("M17", "B1 裸指针零容忍"),
    "M-4 诊断不崩溃": ("M18", "A5（且不含“检查器异常”）"),
    "M-2 容差/口径": ("M19", "A4 剔表格行实验"),
    "§D 覆盖守卫可自擦": ("M20 / M21", "D1 / D2 / D3"),
    # ---- 修复轮 4 ----
    "I-2 头部自陈（E1）": ("M25", "E1 头部自陈"),
    "E2 无守卫面计数": ("M35", "E2 无守卫面计数"),
    "X4 判词读数挂牌（E3）": ("M34 / M36", "E3 判词读数挂牌"),
    "E4 容差自述": ("M26", "E4 容差自述"),
    "E5 口径同宽": ("M18", "A5 + E5 口径同宽"),
    "E6 基线非零": ("M28", "E6 基线非零"),
    "E7 自查清单条数": ("M29", "E7 自查清单条数"),
    "E8 This-X 复算": ("M30", "E8 This-X 复算"),
    "X1 方向性断言极性（E9）": ("M32 / M33", "E9 方向性断言极性"),
    "E10 缺项基数": ("M31", "E10 缺项基数"),
    "M-1 分母钉死（E0）": ("M24", "E0 守卫名册"),
    "X7 区间两端都核": ("M22 / M23 / M37", "B2 出站指针全扫（区间止行）"),
    # ---- 修复轮 5（收口轮） ----
    "I-2 判分表条数（E11）": ("M43", "E11 判分表条数（核**每一处**）"),
    "M-1 残余·守卫体掏空（E12）": ("M38", "E12 守卫体完整性"),
    "I-1 本节两个自陈数（E2）": ("M39 / M40", "E2 无守卫面计数"),
    "I-2 普查未归类行（E2）": ("M41", "E2 无守卫面计数（第二口径）"),
    "M-4b 正文区间单一来源": ("M42", "A1 C2 词数（BODY 现取自文档代码块）"),
}


def git_hash_object(path):
    """用 **git 自己的**哈希（不是裸 sha256sum）。"""
    p = subprocess.run(["git", "hash-object", str(path)], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout.strip()


def head_blob_hash(rel):
    p = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], cwd=ROOT,
                       capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def run_checker():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT,
                       capture_output=True, text=True, encoding="utf-8", env=env)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    if "--list" in sys.argv:
        for mid, desc, *_ in MUTATIONS:
            print(f"{mid:<6} {desc}")
        return 0

    files = sorted({m[2] for m in MUTATIONS})
    base = {}
    for rel in files:
        p = ROOT / rel
        base[rel] = {"bytes": p.read_bytes(), "hash": git_hash_object(p),
                     "head": head_blob_hash(rel)}

    print("=" * 78)
    print("变异驱动器：tests/skills/mutate-writing-discipline.py")
    print("=" * 78)
    for rel in files:
        b = base[rel]
        same = "== HEAD blob" if b["head"] == b["hash"] else f"!= HEAD blob（{b['head']}）——工作树有未提交改动"
        print(f"  基线 {rel:<40} git hash-object = {b['hash']}  {same}")

    code, out = run_checker()
    print(f"\n[基线] 检查器 exit={code}  {'（应为 0）' if code == 0 else '<<< 基线不是绿的，后面的变异没有意义'}")
    if code != 0:
        print(out[-2000:])
        return 2

    rows, failed = [], []
    for mid, desc, rel, old, new, expect, notexpect in MUTATIONS:
        if only and mid != only:
            continue
        path = ROOT / rel
        raw = base[rel]["bytes"]
        text = raw.decode("utf-8")
        n = text.count(old)
        if n != 1:
            rows.append((mid, "DRIVER-ERR", f"原文命中 {n} 次（应恰为 1）：{old[:50]!r}"))
            failed.append(mid)
            continue
        path.write_bytes(text.replace(old, new, 1).encode("utf-8"))
        code, out = run_checker()
        fails = [l for l in out.splitlines() if l.startswith("FAIL")]
        hit = [l for l in fails if re.search(expect, l)]
        bad = [l for l in fails if notexpect and re.search(notexpect, l)]
        red_ok = code != 0 and bool(hit) and not bad
        # 还原：write_bytes（**不用 write_text**），再用 git hash-object 自证
        path.write_bytes(raw)
        restored = git_hash_object(path)
        byte_ok = restored == base[rel]["hash"]
        status = "RED-OK" if (red_ok and byte_ok) else "!! 不达预期"
        rows.append((mid, status,
                     f"exit={code} · {('命中 ' + hit[0][:118]) if hit else '（无匹配 FAIL 行）'}"
                     f" · 还原 {restored[:12]} {'==' if byte_ok else '!='} {base[rel]['hash'][:12]}"
                     + ("  ⚠️ 含禁止出现的文本" if bad else "")
                     + ("" if byte_ok else "  ⚠️ 还原不一致")))
        if not (red_ok and byte_ok):
            failed.append(mid)
        print(f"  {mid:<6} {desc}")
        print(f"         {rows[-1][2]}")

    print("\n" + "=" * 78)
    print("逐条结果")
    print("=" * 78)
    for mid, st, det in rows:
        print(f"{st:<12} {mid:<6} {det}")

    print("\n" + "=" * 78)
    print("九条修复 × 守卫（I-3 要求）")
    print("=" * 78)
    for fix, (mut, guard_name) in FIX_GUARDS.items():
        print(f"  {fix:<5} 守卫 {guard_name:<34} 演示红：{mut}")
    for what, (mut, guard_name) in EXTRA_GUARDS.items():
        print(f"  {what:<24} 守卫 {guard_name:<30} 演示红：{mut}")

    code2, out2 = run_checker()
    print(f"\n[还原后复跑] 检查器 exit={code2}  {'（应为 0）' if code2 == 0 else '<<< 还原失败'}")
    # 全部文件再自证一次
    print("\n[还原自证 · git hash-object]")
    allok = True
    for rel in files:
        h = git_hash_object(ROOT / rel)
        ok = h == base[rel]["hash"]
        allok &= ok
        print(f"  {rel:<40} {h}  {'== 变异前' if ok else '!= 变异前 <<<'}")
    print(f"\nMUT: {'全红' if not failed and code2 == 0 and allok else '有绿或不达预期（' + ', '.join(failed) + '）'}"
          f"（{len(rows)} 条变异；还原 {len(files)}/{len(files)} 逐字节）")
    return 0 if (not failed and code2 == 0 and allok) else 1


if __name__ == "__main__":
    sys.exit(main())
