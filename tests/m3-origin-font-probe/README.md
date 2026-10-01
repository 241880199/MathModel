# `tests/m3-origin-font-probe/` — Origin **字体族**专项侦察证据（2026-09-30）

> 只回答一个问题：**有没有办法让 Origin 导出的 PDF 内嵌一个 Times 系的衬线字体？**
> 报告正文：`.superpowers/sdd/task-m3-origin-font-probe-report.md`

## 0. 前置（复跑必须）

- **本机已安装并已授权的 OriginPro**（本机 `OriginPro 2026 (教育版)`，`@V = 10.300197`）。
  ⚠️ **这是硬前置**：仓库里放什么都没有用 —— 所以"干净检出可复跑"这一项**不相容**。
- `originpro 1.1.15` + `OriginExt 1.2.5` 的 `--target` 安装，落在 **`build/m3-origin-probe/site/`**
  （**上一轮遗留、已 gitignore**，本轮**复用未重装**）。探针用
  `sys.path.insert(0, 'build/m3-origin-probe/site')` 导入。
- Python 3.11.9 · `fitz` 1.27.2.3 · `matplotlib` 3.10.7（读数与对照图用）。
- 需要**一个 Windows 桌面会话**；Origin 窗口默认隐藏，全程无交互。

## 1. 文件清单

### 探针脚本（可复跑，全部 LF）

| 文件 | 干什么 | 产物落 `build/m3-origin-font/` |
| :--- | :--- | :--- |
| `probe_mpl_control.py` | **建"已知正确"的 matplotlib 对照图**（Times / SimSun 各一份，含 CJK 版），自检读数方法能否区分 | `mpl/ctrl_*.pdf`·`mpl/glyph_*.png` |
| `probe_glyph_compare.py` | 拉丁/中文 **字形并排对照** + 逐字符墨迹宽度 | `mpl/glyph_ab.png`·`glyph_cjk_ab.png`·`glyph_metrics.json` |
| `probe_origin_font.py` | 第 1 轮：基线 + 结构 introspection 尝试 + 主题 + 点名候选 + 中文 | `origin/b0,c1,c2,d1,e1_*.pdf` |
| `probe_origin_font2.py` | 第 2 轮：**因果对照**（假主题名/真主题名）+ 索引前后 + 主题后改文本 | `origin/g1..g5_*.pdf` |
| `probe_origin_font3.py` | 第 3 轮：主题**动了哪些属性** + 不用主题照样复现 + 逐条单点 | `origin/g6,g7,g8_*.pdf` |
| `probe_origin_font4.py` | 第 4 轮：同一会话内改 `OPDF.INI`（**已按字节还原**） | `origin/h_*.pdf` |
| `probe_origin_font4b.py` | 第 4 轮 B：**每次新起 Origin 进程**改 `OPDF.INI`（**已按字节还原**） | `origin/i_*.pdf` |
| `probe_origin_font5.py` | 第 5 轮：`expGraph` 的 `theme:=` 参数（导出期换字） | `origin/j1..j4_*.pdf` |
| `probe_origin_font6.py` | 第 6 轮：`theme:=` 能不能覆盖后加的注释 | `origin/k0..k2_*.pdf` |
| `probe_pdf_fonts.py` | **统一读数器**：对目录下所有 PDF 打印 `get_fonts()`（含 `ext` 内嵌标志）+ span 层 | `pdf-readout.txt` |
| `gen-evidence.py` | 把 `build/` 的转录**归一化成 LF** 写回本目录，并自查裸 CR | 本目录 `out-*.txt` |

### 逐字转录（全部 LF，`CR=0`）

`out-mpl-control.txt` · `out-mpl-glyph-compare.txt` · `out-origin-{1,2,3,5,6}-*.txt` ·
`out-origin-4-same-session-ini.txt` · `out-origin-4b-{embed1,embed2,embed1-out1}.txt` ·
`out-pdf-font-readout.txt` + `.json`（**字体读数表**）· `out-pdf-embedding-scan.txt` ·
`out-checker-runs.txt`

### 入库的图片（唯一两份二进制，均 ≤40 KB）

- `ctrl-mpl-glyph-ab.png`（40 KB）· `ctrl-mpl-glyph-cjk-ab.png`（17 KB）
- 再生成：`python tests/m3-origin-font-probe/probe_glyph_compare.py`
- **Origin 侧的 PNG 一律不入库**（`build/m3-origin-font/origin/*.png`，gitignore），
  再生成：`python -c "import fitz; ..."`，或见各探针 json。

## 2. 一键复跑

```bash
# 0) 对照图 + 读数方法自检（不需要 Origin）
python tests/m3-origin-font-probe/probe_mpl_control.py
python tests/m3-origin-font-probe/probe_glyph_compare.py

# 1) Origin 各轮（每支都 try/finally: op.exit()；跑完请核 Origin64=0）
python tests/m3-origin-font-probe/probe_origin_font.py
python tests/m3-origin-font-probe/probe_origin_font2.py
python tests/m3-origin-font-probe/probe_origin_font3.py
python tests/m3-origin-font-probe/probe_origin_font5.py
python tests/m3-origin-font-probe/probe_origin_font6.py
# 注意：4 / 4b 会临时改用户 OPDF.INI，脚本自己按字节还原（见脚本头注释）

# 2) 读数 + 入库归一化
python tests/m3-origin-font-probe/probe_pdf_fonts.py build/m3-origin-font/origin build/m3-origin-font/mpl
python tests/m3-origin-font-probe/gen-evidence.py

# 3) 收尾
tasklist /FI "IMAGENAME eq Origin64.exe"     # 必须是 0
```

## 3. 探针自身的纪律

- **每一条"设上了"的判断都落在产物上**（导出 PDF 的 `get_fonts()` / span 字体），
  **不看** API 返回值 / `run=OK`。
  ⚠️ 但反过来**要看**：`op.lt_exec` 返回 **`False`** 是**真信号**（该属性不存在）。
  本轮实测 `page.font$=` / `layer.font$=` / `sys.font$=` 都返回 `False`，
  而 `xb.font$ = "Times New Roman";` 返回 `True` 却**什么也没做**。
- **`themeApply2g` 传入不存在的主题名不报错**（`exec_ok=True`）、产物也不变 ⇒ 又是"失败静默"。
  所以"主题应用成功"必须由**产物**证明。
- ⚠️ **不要在一个 Python 进程里起两段 Origin 会话**：`probe_origin_font7.py` 就是这么写的
  （第一段 session 退出后又 `op.set_show(False)` 起第二段），结果第二段**漏下 1 个 `Origin64.exe`**（已按 PID 清除）。
  而且 `probe_origin_font7.py` 的**读数是无效的**（对照自己也变了）——它的产物**不要当证据用**，
  脚本留在这里只为**备查失败过程**。
- 第 4 / 4b 轮**临时改过** `%USERPROFILE%\..\Documents\OriginLab\User Files\OPDF.INI`：
  改前 `sha256` 留档，改后**按字节还原**并核对（`probe_origin_font4.json` 里
  `restored_identical: true`）。**安装目录 `D:\Program Files\OriginLab\**` 一个字节没动。**
