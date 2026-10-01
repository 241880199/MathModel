# `tests/m3-matlab-font-probe/` —— 四份 OTF 能不能被 MATLAB 用上

本目录是 **2026-09-30** 的一次性取证现场，回答一个问题：

> `mcm-plot-python` 随 skill 入库的那四份 OTF（`.claude/skills/mcm-plot-python/assets/fonts/`），
> MATLAB 到底能不能用上？怎么用上？代价是什么？

**它不是一个常跑测试。** 先例形态见 `tests/m3-matlab-recon/`（同一台机器、同一轮工作）。

## 结论速览（细节在探针输出里）

- **能用上 —— 但只走一条路**：把 4 个文件放进 `%LOCALAPPDATA%\Microsoft\Windows\Fonts`，
  并在 `HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts` 写 4 条值
  （`install-user-fonts.sh` 做的就是这件事），然后**新起一个 MATLAB 会话**。
- **注册表值的「名字」是承重的**：常规面必须写成 `TeXGyreTermesX (TrueType)`；
  写成 `TeXGyreTermesX Regular (TrueType)` 时 MATLAB **完全看不见**（静默，无任何警告）。
  因果对照：`out-control-delete-plain-name.txt`（删掉那条值 → 家族立刻消失）。
- `addpath` 指向字体目录、GDI 的 `AddFontResourceEx`（私有 / 会话级，甚至在 MATLAB 进程内调用）
  **都不能**让 `listfonts` 看见新字体。
- 不装字体时，`set(ax,'FontName','TeXGyreTermesX')` **不报错、`get` 还回声**，
  产物 PDF **内嵌 SimSun**、**零警告** —— 静默回退。

## 三类文件，纪律不同

| 类别 | 文件 | 纪律 |
| :--- | :--- | :--- |
| **探针（MATLAB）** | `probe_a.m` `probe_a2.m` `probe_a3.m` `probe_b.m` `probe_c.m` `probe_d.m` | 可运行源码，由 `gen-probe-sources.py` 生成（LF）。改它 = 改探针本身。 |
| **脚本 / 仪器（bash+python）** | `install-user-fonts.sh` · `uninstall-user-fonts.sh` · `capture-font-state.sh` · `measure_fonts.py` · `gen-evidence.py` · `gen-probe-sources.py` | 同上。`install/uninstall` 会**改本机用户级状态**，跑之前先读它们的注释。 |
| **输出的捕获** | `out-*.txt` | **逐字的 stdout 捕获，自带年代指纹**（内嵌当时的 `listfonts=249` / `FontUtils=235` 等读数）。 |

## 关于 `out-*.txt`：**手改 = 造伪**

`out-*.txt` 是某个时点的 stdout 原文。它们的价值**就是**里面那些会随机器状态变的数字
（`listfonts` 条数、内嵌字体名）。若某份捕获与今天的事实不一致，唯一正确的做法是
**重跑产出它的探针并重新捕获**，不是去改里面的字面量。

## 复跑（三步）

**第 0 步 —— 记下装之前的状态（务必先做，这是回滚的基准）：**

```
bash tests/m3-matlab-font-probe/capture-font-state.sh > build/m3-matlab-font/pre/pre_registry_and_dir.txt
```

**第 1 步 —— MATLAB 探针（每次 `-batch` 约 12–42 s）：**

```
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a.m')"  > build/m3-matlab-font/raw_probe_a.txt  2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a2.m')" > build/m3-matlab-font/raw_probe_a2.txt 2>&1
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_a3.m')" > build/m3-matlab-font/raw_probe_a3.txt 2>&1
```

**第 2 步 —— 装机 / 卸载（会改 HKCU + 用户字体目录）：**

```
bash tests/m3-matlab-font-probe/install-user-fonts.sh      # 见文件头：值名为什么这么写
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_b.m')" > build/m3-matlab-font/raw_probe_b.txt 2>&1   # 旧写法（看不见）
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_d.m')" > build/m3-matlab-font/raw_probe_d.txt 2>&1   # 本写法（看得见）
bash tests/m3-matlab-font-probe/uninstall-user-fonts.sh
d:/Software/Matlab/bin/matlab -batch "run('tests/m3-matlab-font-probe/probe_c.m')" > build/m3-matlab-font/raw_probe_c.txt 2>&1
bash tests/m3-matlab-font-probe/capture-font-state.sh > build/m3-matlab-font/afterroll/state_final.txt
```

**第 3 步 —— 归一化 + 重测内嵌字体：**

```
python tests/m3-matlab-font-probe/gen-evidence.py
```

`gen-evidence.py` 会把上一步的原始捕获**归一化为 LF**（并逐份打印原始 CR 计数），
复制 MATLAB 直接用 `fopen(...,'wb')` 写出的字体清单，并用 `measure_fonts.py` 重测
`build/m3-matlab-font/probe_*/` 里每份 PDF 的**内嵌字体**，汇总成 `out-pdf-embedded-fonts.txt`。

## 字节纪律（本目录的实测事实）

- **MATLAB `-batch` 的 stdout 在 Windows 上是 CRLF**：本轮 20 份原始捕获共 **384 个裸 CR**，
  逐份计数见 `gen-evidence.py` 的输出。所以 `out-*.txt` 由 `write_bytes` 写入并归一化为 **LF**。
- **MATLAB 用 `fopen(...,'wb')` 写出的字体清单本来就是 LF**（`out-listfonts-*.txt` 复跑自查 `CR=0`）。
- 本目录 40 个文件（含本 README）复跑自查：**`CR=0`**。

## 二进制产物

**一份都不入库。** 全部可由上面的步骤确定性重生成。产物落在
`build/m3-matlab-font/{probe_a,probe_a2,probe_a3,probe_b,probe_c,probe_d,check4,tmpfont}/`
（`build/` 已 gitignore）。

## 本目录里几个**不是** stdout 捕获的文件

- `gen-probe-sources.py` —— 生成 `probe_*.m` 与 `build/m3-matlab-font/gdi32mini.h`（LF）。
- `capture-font-state.sh` —— 逐字转储用户字体目录 + HKCU/HKLM 字体键，供装前/装后 **diff**。
- `measure_fonts.py` —— 用 PyMuPDF 读 PDF **内嵌字体**（判"到底用上了没有"的唯一真相）。
- `out-pdf-embedded-fonts.txt` —— 由 `gen-evidence.py` 组装。

## 复跑的非显然前置（踩过的坑，照实记）

1. **Git Bash 会改写 `reg.exe` 的参数**：`/v` `/t` `/d` `/f` 被当成路径 ⇒ `reg add` 报
   "Invalid syntax"。两个脚本都在头部 `export MSYS_NO_PATHCONV=1`。
2. **`run('<相对路径>.m')` 会把 cwd 切到脚本所在目录**：所有探针用
   `here=fileparts(mfilename('fullpath')); root=fileparts(fileparts(here)); cd(root);` 反推仓根。
3. **装机后必须新起 MATLAB 会话**：`listfonts` 在一个会话里是 `persistent` 缓存。
4. **注销/重登、重启 Explorer、重启机器这三种刷新都没有测**（会打断用户会话）——
   见探针报告的"未验证清单"。
