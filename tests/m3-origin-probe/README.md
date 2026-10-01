# `tests/m3-origin-probe/` —— `mcm-plot-origin` 的**侦察快照目录**

本目录是 **2026-09-30 侦察期**的一次性取证现场，不是一套常跑测试。它记录"在
`mcm-plot-origin` 建出来之前，Origin 这条出图链路在本机到底是什么样"。

先例：`tests/m3-plot-recon/`（`mcm-plot-python`）、`tests/m3-matlab-recon/` 与
`tests/m3-matlab-font-probe/`（`mcm-plot-matlab`），本目录照它们的形态建。

**本目录不复述任何规范数值** —— 数字一律以现场命令的输出为准。

## ★ 头号结论（先看这个）

**Origin 导出物的图宽是可以设定的**（与 MATLAB 相反）。核心 API：
`GPage.save_fig(path, width=N)`（originpro 侧）→ 实际发出
`expgraph ... tr1.Unit:=2 tr1.Width:=N`（`tr1` 是导出尺寸子树的节点名）。

## 三类文件，纪律不同

| 类别 | 文件 | 纪律 |
| :--- | :--- | :--- |
| **探针（Python）** | `probe_a_connect.py` · `probe_a2_edition.py` · `probe_b_size.py` · `probe_c_export.py` · `probe_d_appearance.py` · `probe_e_font_axis.py` · `probe_f_axis.py` · `probe_g_e2e.py` · `probe_h_f2.py` · `probe_i_dpi_pagesize.py` | 可运行源码。改它 = 改探针本身（要留痕、要重跑）。**每个都用 `op.exit()` 收尾**。 |
| **装配器** | `gen-evidence.py` | 把 `build/` 里的 CRLF 捕获归一化为 LF 并装配 `out-*.txt`。 |
| **输出的捕获** | `out-*.txt` | **逐字的 stdout 捕获，自带年代指纹**。 |

## 关于 `out-*.txt`：**手改 = 造伪**

`out-*.txt` 是某个时点的 stdout 原文。若某份捕获与今天的事实不一致，唯一正确的做法是
**重跑产出它的探针并重新捕获**，**不是**去改里面的字面量。

## ★ 硬前提：`originpro` 必须按 `--target` 装到 `build/`

探针把 `build/m3-origin-probe/site` 插到 `sys.path[0]`，**不碰全局 site-packages**：

```
python -m pip install --target build/m3-origin-probe/site --no-deps originpro
python -m pip download --no-deps -d build/m3-origin-probe/wheels OriginExt
python -m pip install --target build/m3-origin-probe/site --no-deps \
    build/m3-origin-probe/wheels/originext-1.2.5-cp311-none-win_amd64.whl
```

- 为什么拆两步：`originpro` 的唯一依赖是 `OriginExt`（编译扩展，`cp311-win_amd64`）。
  `OriginExt` 自己**无 Requires-Dist**，所以 `--no-deps` 不会触发 `pywin32` 的 post-install
  写系统位置 —— `--target` 因此**可行**（见 `out-j-…txt`）。
- **另一条硬前提**：本机必须**装了并已授权** Origin（本例 = `OriginPro 2026 (教育版)`，
  `D:\Program Files\OriginLab\Origin2026\Origin64.exe`）。这不是 pip 能解决的。

## 复跑

**第一步（每条都要等它起/退 Origin 一个实例，单条约 15–60 s）：**

```
python tests/m3-origin-probe/probe_a_connect.py    > build/m3-origin-probe/raw_probe_a.txt  2>&1
python tests/m3-origin-probe/probe_a2_edition.py   > build/m3-origin-probe/raw_probe_a2.txt 2>&1
python tests/m3-origin-probe/probe_b_size.py       > build/m3-origin-probe/raw_probe_b.txt  2>&1
python tests/m3-origin-probe/probe_c_export.py     > build/m3-origin-probe/raw_probe_c.txt  2>&1
python tests/m3-origin-probe/probe_d_appearance.py > build/m3-origin-probe/raw_probe_d.txt  2>&1
python tests/m3-origin-probe/probe_e_font_axis.py  > build/m3-origin-probe/raw_probe_e.txt  2>&1
python tests/m3-origin-probe/probe_f_axis.py       > build/m3-origin-probe/raw_probe_f.txt  2>&1
python tests/m3-origin-probe/probe_g_e2e.py        > build/m3-origin-probe/raw_probe_g.txt  2>&1
python tests/m3-origin-probe/probe_h_f2.py         > build/m3-origin-probe/raw_probe_h.txt  2>&1
python tests/m3-origin-probe/probe_i_dpi_pagesize.py > build/m3-origin-probe/raw_probe_i.txt 2>&1
```

**第二步（判词；需要第一步的产物在 `build/m3-origin-probe/{g,h}/`）：**
见 `out-checks-figure-style.txt` 顶部逐条列出的 7 条命令（绿色 2 条 + 违规 5 条）。

**第三步（归一化 + 组装）：**

```
python tests/m3-origin-probe/gen-evidence.py
```

## ★ 进程卫生：**崩溃会漏 Origin 进程**

`originpro` 的 `atexit` 在**没走到 `op.exit()`** 时只做 `Detach(releaseonly=True)`，
**Origin 进程会残留**。本目录的探针一律 `op.exit()` 收尾；侦察期有 3 次**首轮崩溃**
（`probe_c` / `probe_e` / `probe_g`）各漏 1 个 `Origin64.exe`，已按 PID 清除。
⇒ **给 skill 的输入：跑 Origin 的包装必须 `try/finally: op.exit()`**。

## 字节纪律（本目录的实测事实）

- Python 的 stdout 在 Windows 上是 **CRLF**。本次 **12 份**原始捕获共
  **476 个裸 CR**（逐份计数由 `gen-evidence.py` 打印），`out-*.txt` 由 `write_bytes`
  写入并归一化为 **LF**（自查：本目录 `out-*.txt` 全部 `CR=0`）。

## 二进制产物

**一份都不入库。** 全部可由入库脚本**重跑产出**（同一命令、同一输入）。
⚠️ **但不声称逐字节相同** —— 本目录的 PNG/PDF 是 **Origin 本体**导出（经 `originpro` → `OriginExt` 驱动），
**可复现性本目录未测**；而**同类断言在 MATLAB 侧已被实测证伪**（同命令两次：PNG 字节变、PDF `MediaBox` ±1 pt，
见 `docs/mcm-suite-todo.md` §H.2 的 `M3-matlab-T5b`）⇒ 这里**不再声称**"确定性重生成"。
产物落 `build/m3-origin-probe/{b,c,d,e,f,g,h,i}/`（**已 gitignore**）。
重生成命令 = 上面第一/二步。
