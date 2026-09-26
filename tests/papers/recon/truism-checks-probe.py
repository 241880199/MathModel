"""量 C-3 里两条"疑似恒真"的判据到底能不能红——**只量，不改判据**。

① `verify_ids.py:569-577` 的 `path_bad`（比较 `IndexResult` 报告的落点 vs 判据读的落点）
   ⇒ 量：`index.build(..., out_dir=X)` 报告的三个落点是否**构造性地**等于 `X/<名>`。
   若等于，则「落点等式」只在 `dest = out_dir or io.DERIVED` 这条链被改坏时才可能不等，
   与"全量/限样本"无关（两种模式都恒空）。
② `verify_map.py:730-733` 的 `py_bad`（`v_blob_bytes` vs `v_git_blob`）
   ⇒ 量：两个算法在**用例矩阵**上何时分叉。矩阵三轴：
      **行尾**（LF / CRLF）× **`.gitattributes`**（`-text` 面 / 无 `-text`）×
      **传给 `git hash-object` 的路径形态**（仓库相对 / POSIX 绝对 `/` / Windows 反斜杠绝对 `\`）。

**为什么矩阵要带第三轴（2026-09-26 更正，本轮实测）**：本探针早先只放了"无 `-text` 的
LF / CRLF"两格，并据此把分叉归因于"**少了 `-text`**"。**实测不是**：真正的触发条件是
「**工作树里有 CRLF**」+「**传给 `git hash-object` 的是 Windows 反斜杠绝对路径**」——
反斜杠绝对路径下 `.gitattributes` 的 `-text` **根本不生效**（`git check-attr` 说
`text: unset`，但 `hash-object` 仍按 `core.autocrlf` 归一化），而**同一份文件**换相对路径
或 `/` 绝对路径就回到原始字节。**先前的矩阵恰好缺了能否证它的那一格**（`-text` + CRLF + 相对路径）。
⇒ 2b 判据那条的 docstring（"按 `.gitattributes` 的过滤器口径"）与本探针旧结论**都按实测更正**；
`verify_map.py` 是冻结件 ⇒ **只登记不改**（见 `docs/mcm-suite-triage-2026-09-26.md` §4.2）。
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]   # tests/papers/recon/（比判据脚本深一层）
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests" / "papers"))

from tools.papers import index, io  # noqa: E402

print("=" * 74)
print("① path_bad：`IndexResult` 报告的落点是否构造性地 == `out_dir/<名>`")
print("=" * 74)
COLLECTION = "2025美赛O奖论文"
one = sorted((io.ORIGIN / COLLECTION).rglob("*.pdf"))[:1]
with tempfile.TemporaryDirectory() as td:
    dest = Path(td) / "some-other-place"
    res = index.build(COLLECTION, sample=one, out_dir=dest)
    got = {res.index_path: dest / "INDEX.md", res.tags_path: dest / "TAGS.md",
           res.prov_path: dest / "PROVENANCE.md"}
    for k, v in got.items():
        print(f"  报告 {k.name:16s} == out_dir/{v.name:16s} ? {k == v}   （报告值 {k}）")
    print(f"  ⇒ 三者全等 = {all(k == v for k, v in got.items())}")
    print("  口径：`index.build` 里 `dest = out_dir or io.DERIVED`，三个落点都写成")
    print("        `dest / \"<名>\"`；判据那侧比的是 `prod_dir / \"<名>\"`，而 prod_dir")
    print("        就是传进去的 out_dir ⇒ **只要 out_dir 非空，两边同值**——")
    print("        **与全量/限样本无关**（两种模式下 prod_dir 都直接传下去）。")
    print(f"  out_dir 是 Path（恒真） = {bool(dest)}")

print()
print("=" * 74)
print("② py_bad：`v_blob_bytes`（裸字节 + blob 头） vs `v_git_blob`（git hash-object）")
print("=" * 74)


def v_blob_bytes(data: bytes) -> str:
    h = hashlib.sha1()
    h.update(b"blob %d\0" % len(data))
    h.update(data)
    return h.hexdigest()


def git_blob(arg: str, cwd: Path = ROOT) -> str:
    """`git hash-object -- <arg>`（**路径形态是自变量**，见下）。"""
    r = subprocess.run(["git", "hash-object", "--", arg],
                       capture_output=True, cwd=str(cwd))
    return r.stdout.decode().strip() if r.returncode == 0 else f"<rc={r.returncode}>"


def check_attr(p: Path) -> str:
    """`git check-attr` 的独立读数（谁在管这个路径的 `text`）。"""
    r = subprocess.run(["git", "check-attr", "text", "--", str(p)],
                       capture_output=True, cwd=str(ROOT))
    return r.stdout.decode("utf-8", "replace").strip().rsplit(": ", 1)[-1]


# **两块试验面**（`-text` 是自变量，必须由路径所在目录决定，不能靠想象）：
#   `-text` 面 ⇒ `tests/papers/** -text`（该目录 gitignored ⇒ 试件不留痕）；
#   无 `-text` ⇒ `build/finalfix/`（不在任何 `-text` 规则下）。
SPECIMENS = {
    "-text 面（tests/papers/reports-limited/，gitignored）":
        ROOT / "tests" / "papers" / "reports-limited" / "zz-truism-probe.txt",
    "无 -text（build/finalfix/）":
        ROOT / "build" / "finalfix" / "zz-truism-probe.txt",
}
PAYLOADS = {"LF": b"line1\nline2\n", "CRLF": b"line1\r\nline2\r\n"}

for face, p in SPECIMENS.items():
    p.parent.mkdir(parents=True, exist_ok=True)
    attr = check_attr(p)
    print(f"\n--- {face}")
    print(f"    `git check-attr text` = {attr}")
    for eol, payload in PAYLOADS.items():
        p.write_bytes(payload)
        raw = v_blob_bytes(payload)
        rel = git_blob(p.relative_to(ROOT).as_posix())
        posix = git_blob(p.as_posix())
        win = git_blob(str(p))
        print(f"    [{eol}] 试件 = {p.relative_to(ROOT).as_posix()}")
        print(f"      v_blob_bytes（裸字节）        = {raw}")
        print(f"      相对路径  {p.name:20s} = {rel}   == 裸字节? {rel == raw}")
        print(f"      POSIX 绝对（/）               = {posix}   == 裸字节? {posix == raw}")
        print(f"      Win 反斜杠绝对（backslash）    = {win}   == 裸字节? {win == raw}")
        print(f"      ⇒ 三者一致 = {rel == posix == win}")
    p.unlink()

print()
print("  ⇒ 实测结论（**按上表读，别照抄旧说**）：")
print("     · **有 CRLF 且传 Windows 反斜杠绝对路径** ⇒ `git hash-object` 报**归一化**值")
print("       （≠ 裸字节）——**即便 `check-attr` 说 `text: unset`**，属性在这一格被绕过。")
print("     · **同一份 CRLF 文件**换相对路径或 POSIX 绝对路径 ⇒ 报**原始字节**（`-text` 生效）。")
print("     · LF 文件三种路径形态**都不分叉**（归一化是恒等变换）——所以入库的四条路径")
print("       上 `py_bad` 恒空，**因为工作树是 LF**，不是因为 `-text` 被尊重。")
print("     · 真触发条件 = 「工作树里有 CRLF」+「传的是 Windows 反斜杠绝对路径」；")
print("       `-text` 有没有**不是**条件（反斜杠路径下它不生效）。")
print("     ⇒ `py_bad` 仍有红路（红路 = 工作树出 CRLF），但它 docstring 把机制归给")
print("       「`.gitattributes` 过滤器口径」**与实测不符**——`verify_map.py` 冻结，只登记。")
