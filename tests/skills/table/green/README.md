# `green/` —— GREEN 对照件（**用本 skill 规范 + 判据**产的表）

> ## !! 本目录同样含泄题风险文件，绝不给写手 !!
>
> 上一层 `red-green-evidence.md`（对照结论）与 `../red/README.md` / `../red/writer-self-reports.md`
> **都不给写手**。**这个点名不是穷举**：§2 列出的产物件（`out-G{n}/` 下的 `table.tex` /
> `caption.txt` / `table.png`）与本 `README.md` 自身**同样不给写手**。

## 1. 这是什么

Task 3 的 GREEN 侧：与 `red/` **同场景、同数据、同一把尺**，
只换一个自变量 —— **用不用本 skill 的规范**（`.claude/skills/mcm-table/references/table-style.md`
的 `T1`–`T3` / `D4`–`D8` + 判据 `C1`–`C8`）。

- **场景**：数据逐字取 `figure-choose/red/brief-R{1,2,3}.md`（**权威副本在 `red/`**，本目录
  **不重复内联**）。G1↔R1、G2↔R2、G3↔R3 一一对应。
- **判据**：`check-table-style.py` 一字未改；工作树 blob == `HEAD` blob（见 `../red-green-evidence.md` §0）。
- **GREEN 不由干净写手产出**：由本任务用规范产出（`T`/`D` + 8 条判据都要过）。
- **表题是判断层动作**：由本任务写（场景 brief 只要求"英文表题"，没给合规形态）。

## 2. 目录内容

| 路径 | 是什么 |
| :--- | :--- |
| `out-G{n}/table.tex` | 规范产出的表片段（含**来源回显注释**；泄题风险件） |
| `out-G{n}/caption.txt` | 表题（英文） |
| `out-G{n}/table.png` | **判据渲染**的证据件（`--png` · 150dpi 第 1 页）；非字节可复现（每次重编带新时间戳） |

**上表不声称穷尽**：本目录还有本 `README.md` 自身（泄题风险件）；派写手时本目录内任何文件都不给。

**对照表在上一层**：`../red-green-evidence.md`。**生成器**：`../make-evidence.py`。

## 3. 本支产物在机械判据上的读数

- **G1 / G2 / G3 三条全绿**（`C1`–`C8` 逐条 `PASS`）—— 读数见 `../red-green-evidence.md` §3。
- **设计覆盖**：G1 = 两级表头（**前导 `&`** 形态）+ 表注 + 相似度列；G2 = **负数** S 列
  （`table-format=-1.3`）+ 相关系数表；G3 = 紧凑单级四列（`District` + Low/Medium/High；
  检查器实测 `7 行 × 4 列`）（"paper-ready"）。

## 4. 亲眼看表逼出来的（照实，本任务**不改**判据）

- **G1 的 caption 比表宽**（caption 满版心、表 4.12in 居中）—— 正常排版，非缺陷（判据不报）。
- **G3 的表本身不含"最相似的一对"**（该判断在 caption 里）—— "paper-ready 单表"的设计选择。
- **`D6` / `C7`（缺失值形态）未被本支 GREEN 的数据触发**（本支数据无缺失值）—— 该判据的真红
  作证在变异驱动器 `MUT-C7a` / `MUT-C7b`，见 `../red-green-evidence.md` §7。

## 5. 与 RED 的比对口径

同场景、同数据（逐字）、同一把尺（判据一字不改）。**不许**因为某场景过不了就调判据或换数据。
