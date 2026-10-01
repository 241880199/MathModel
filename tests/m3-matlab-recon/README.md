# `tests/m3-matlab-recon/` —— `mcm-plot-matlab` 的**侦察快照目录**

本目录是 **2026-09-30 侦察期**的一次性取证现场，不是一套常跑测试。它记录"在
`mcm-plot-matlab` 建出来之前，MATLAB 这条出图链路在本机到底是什么样"。

先例：`tests/m3-plot-recon/`（`mcm-plot-python` 的同型侦察，本目录照它的形态建）。

## 三类文件，纪律不同

| 类别 | 文件 | 纪律 |
| :--- | :--- | :--- |
| **探针（MATLAB）** | `probe_a.m` … `probe_i.m` | 可运行源码。改它 = 改探针本身（要留痕、要重跑）。**别把任何探针命名为 `theme.m`**（会遮蔽内置 `theme()`）。 |
| **探针（Python）** | `measure_artifacts.py` · `measure_pixels.py` · `probe_checks.py` · `probe_guards.py` · `probe_ripples.py` | 同上。全部**按路径调用**出货机器，**不复制、不修改** `tests/skills/**`。 |
| **输出的捕获** | `out-*.txt` | **逐字的 stdout 捕获，自带年代指纹**（内嵌当时的"扫到 N 个 skill""绘图家族 N 个""MUT: N/N"等读数）。 |

## 关于 `out-*.txt`：**手改 = 造伪**

`out-*.txt` 是某个时点的 stdout 原文。它们内嵌的数字**随家族落地而变**，
而那些数字**正是它们的价值**。若某份捕获与今天的事实不一致，唯一正确的做法是
**重跑产出它的探针并重新捕获**（让它携带今天的年代指纹），**不是**去改里面的字面量。

> ★ **例外（2026-10-02，M3-matlab Task 5 实测后加）：上面这条规则对两份捕获已不可执行** ——
> **`out-guards-k6-family-k3.txt`** 与 **`out-ripples-m33-m40.txt`** 的探针**在家族落地后跑不动了**，
> 因为**它们的前提就是"家族还没落地"**：
> - `probe_guards.py` §G2 先把真仓 `.claude/skills` 拷成 `skills2/`，再 `mkdir` 一个**假**的 `mcm-plot-matlab` ——
>   真仓现在**真的有**这个 skill ⇒ `fake.mkdir()` **`FileExistsError`**（实测崩溃原文留在
>   `build/m3-matlab-recon/raw_guards_POSTLANDING_CRASH.txt`）。
> - `probe_ripples.py` §R2 的 `assert fixed != txt` 依赖 `SKILL.md` 里那行 `` - `mcm-plot-matlab`（〔拟建〕） ``，
>   而该字面**已被 Task 1 删除** ⇒ **AssertionError**（崩溃原文留 `raw_ripples_POSTLANDING_CRASH.txt`）。
>
> ⇒ **这两份捕获现在是"冻结的历史"**：**不许手改**（老规矩），但**也不能靠重跑更新**（探针已失能）。
> **`gen-evidence.py` docstring 里那份"RE-RUN"配方因此是单向的** —— 照它整跑会把这两份捕获
> **覆盖成崩溃输出**（本任务实测过：崩溃 raw 一度覆盖上去，已由 `HEAD` 还原）。
> 要真正复活它们，得先改探针源码（**改探针 = 改仪器，另案留痕**），不属于收口工作。
>
> 它们当初问的问题（"家族一落地，`K6`/普查/`M33`/`M40` 会怎样"）**今天已由真模块自己的仪器回答**
> （`check-spec-pointers.py` 实报 `扫到 7 个 skill（绘图家族 2 个）`）⇒ **无需再跑**。

## ★ 给所有 `.m` 脚本的硬前提：`run()` 会切当前目录

`.m` 脚本被 `run('<path>')` 执行时，**当前目录在执行期间变成脚本所在目录**，跑完再切回：

```
$ d:/Software/Matlab/bin/matlab -batch "fprintf('BEFORE %s\n',pwd); run('tests/m3-matlab-recon/probe_a.m'); fprintf('AFTER %s\n',pwd)"
BEFORE D:\Projects\数学建模
### probe_a start ###   ← 脚本第一行里 pwd 已经是 D:\Projects\数学建模\tests\m3-matlab-recon
AFTER D:\Projects\数学建模
```
⇒ **脚本里任何相对路径（读数据、写产物）都会被解析到脚本所在目录**，`ENOENT` / 产物写错地方都从这来。
（本目录第一版就因此把产物写进了 `tests/m3-matlab-recon/build/…`。）

**正确写法**——在**每个脚本开头**用 `mfilename('fullpath')` 反推仓根再 `cd`：

```matlab
here = fileparts(mfilename('fullpath'));   % .../tests/m3-matlab-recon
root = fileparts(fileparts(here));         % 仓根（本目录在 tests/<x>/ 两层下）
cd(root);
```
本目录**所有** `probe_*.m` 都带这段，接着才 `fprintf('### probe_x start ### …')`。
⇒ **`mcm-plot-matlab` 出具的 `.m` 脚本必须带上它**，否则"无条件可跑"不成立。
（另一条路是让调用方传绝对路径；本目录选了自推仓根。）

## 复跑

**第一步（每次 `-batch` 约 10–42 s，探针已尽量合并；全 11 次合计 353 s）：**

```
d:/Software/Matlab/bin/matlab -batch "disp(version); disp(matlabroot); disp(computer('arch'))" > build/m3-matlab-recon/raw_version.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_a.m')" > build/m3-matlab-recon/raw_probe_a.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_b.m')" > build/m3-matlab-recon/raw_probe_b.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_c.m')" > build/m3-matlab-recon/raw_probe_c.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_d.m')" > build/m3-matlab-recon/raw_probe_d.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_e.m')" > build/m3-matlab-recon/raw_probe_e.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_f.m')" > build/m3-matlab-recon/raw_probe_f.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_g.m')" > build/m3-matlab-recon/raw_probe_g.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_h.m')" > build/m3-matlab-recon/raw_probe_h_off.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "PROBE_VISIBLE=1; run('tests/m3-matlab-recon/probe_h.m')" > build/m3-matlab-recon/raw_probe_h_on.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-recon/probe_i.m')" > build/m3-matlab-recon/raw_probe_i.txt 2>&1
```

**第二步（Python 仪器；需要第一步的产物在 `build/`）：**

```
python tests/m3-matlab-recon/measure_pixels.py build/m3-matlab-recon/h_off build/m3-matlab-recon/h_on build/m3-matlab-recon/i > build/m3-matlab-recon/raw_pixels.txt 2>&1
python tests/m3-matlab-recon/probe_guards.py   > build/m3-matlab-recon/raw_guards.txt   2>&1   # ⚠️ 已失能，别跑！见文首「例外」段
python tests/m3-matlab-recon/probe_ripples.py  > build/m3-matlab-recon/raw_ripples.txt  2>&1   # ⚠️ 已失能，别跑！见文首「例外」段
python tests/skills/figure-choose/mutate-figure-style.py > build/m3-matlab-recon/raw_mutate.txt 2>&1
python tests/skills/figure-choose/check-house-style.py   > build/m3-matlab-recon/raw_house_style.txt 2>&1
```

**第三步（归一化 + 组装证据）：**

```
python tests/m3-matlab-recon/gen-evidence.py
```

`gen-evidence.py` 会把上一步的捕获**归一化为 LF**（并逐份打印原始 CR 计数）、
重跑 `measure_artifacts.py` / `probe_checks.py` 产出 `out-artifacts-measured.txt` /
`out-checks-figure-style.txt`，并组装 `out-size-law.txt`。

## 字节纪律（本目录的实测事实，不是习惯）

- **MATLAB `-batch` 的 stdout 在 Windows 上是 CRLF**：17 份原始捕获共 **1844 个裸 CR**（逐份计数由 `gen-evidence.py` 打印），
  逐份计数见 `gen-evidence.py` 的输出。所以 `out-*.txt` 由 `write_bytes` 写入并归一化为 **LF**
  （复跑后自查：本目录 `out-*.txt` 全部 `CR=0`）。
- **MATLAB 用 `fopen` 写文件是 LF-only**：实测 `'w'` / `'W'` / `'wb'` 三种模式写出
  `line1\nline2\n` 都是 12 字节、**CR=0**；只有显式 `'wt'`（文本模式）给 14 字节、**CR=2**。
  ⇒ "MATLAB 会写 CRLF"这个说法**对 stdout 成立、对 fopen 文件不成立**，两者要分开说。
  证据：`out-a-env-export-fonts.txt` 的 P4 段。

## 二进制产物

**一份都不入库。** 全部可由入库脚本**重跑产出**（同一命令、同一输入）。
⚠️ **但不声称逐字节相同** —— 实测 **MATLAB 出图/导出非字节可复现**：同一条命令跑两次，
PNG 字节会变、PDF `MediaBox` 会有 **±1 pt** 的抖动（2026-10-02 Task 5 实测，见 `docs/mcm-suite-todo.md` §H.2 的 `M3-matlab-T5b`）。
**原句写的是"确定性重生成"，那是过度声明**，由 Task 5 独立复核 `I-1` 抓出后订正。
重生成命令 = 上面第一/二步；产物落在 `build/m3-matlab-recon/{a..g}/`（**已 gitignore**）。

## 本目录内几个**不是**"stdout 捕获"的文件

- `out-size-law.txt` —— 由 `gen-evidence.py` 从 `out-artifacts-measured.txt` **组装**的表
  （组装逻辑在脚本里，可复跑）。
- `out-listfonts.txt` —— `listfonts` 的全量转写，由 MATLAB 用 `fopen(...,'wb')` 直接写出（本身即 LF）。

**本文件不复述任何规范数值** —— 数字一律以现场命令的输出为准。
