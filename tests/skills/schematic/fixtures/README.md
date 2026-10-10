# `tests/skills/schematic/fixtures/` —— 骨架族的**自证控制组**

本目录回答一件事：**"骨架自己就该全绿"是不是真的** —— 用机械证据回答，不用声明。

## 两组控制

| 组 | 谁 | 断言 | 产出 |
| :--- | :--- | :--- | :--- |
| **正控制** | `assets/skeletons/*.tex`（每份骨架一份） | **`pdflatex` rc=0** 且 **`F1–F6` 全绿** | `<名>.pdf` · `<名>.check.txt` · `<名>.build.txt` |
| **反控制** | `negative-control-math.tex` | 编译 rc=0，**但 `F6` 判红**（预期判词 `RESULT: FAIL（F6）`） | 同上 |

★ **反控制为什么必须有**：本仓纪律 —— **判据只能从失败方向证明**。这一条证明 `F6`（字体族）在"字体族不对"时
**真的会红**，不是恒绿；顺带它就是"**骨架里不许用数学模式**"这条规矩的机械证据
（数学模式会引入 Computer Modern / NewTX 的数学字体，它们不在 `check-figure-style.py` 的 `FONT_FAMILY_OK` 里）。

★★ **`negative-control-math.tex` 不许被"改成绿的"**：它**故意**是红的。谁把它修绿了，
就是把这条控制组废掉。要动它，先读 `README`（=本文件）与
`../references/schematic-style.md` 的「已知缺口」第 2 条。

## 复跑

```
python tests/skills/schematic/fixtures/make-fixtures.py            # 重编 + 重量 + 落盘
python tests/skills/schematic/fixtures/make-fixtures.py --check    # 只重量已入库的 PDF
python tests/skills/schematic/fixtures/probe-a-measurability.py    # A 族可测性探针（只读，见下）
```

末行恒为 `RESULT: PASS（正控制 N 份全绿…；反控制 M 份按预期红）` / `RESULT: FAIL（…）`。

## 口径（每一格都是当场跑出来的）

- **判据本体不在这里**：`F1–F6` 与 `A` 族一律由 `tests/skills/figure-choose/check-figure-style.py` 判，
  本支**只复用**。检查器带 `--schematic` 时**追加** `A` 族（`A1`/`A3`/`A4`，见下）；
  不带时只打 `F1–F6`（与上一版逐字相同）—— `make-fixtures.py` 的 `check_one` 带这个旗标。
- **`--textwidth-in` = 论文版心宽**（`mcm-latex-format` 的 `article` 12pt + `geometry`）——
  它是 `F1` 的**分母**，由调用方传入，检查器自己不预设。
- **`captions.tsv`** 里是喂给 `--caption` 的**图注字符串**：`F3a–F3d` 判的是**它**，不是图里的字。
- **`.pdf` 入库**：交付形态是"**一个图文件 = 一页**"，控制组要看的就是那一页；
  PDF **不可字节比**（每次重编带新的创建时间 / ID）⇒ 它只是**快照**，权威 = 当场重跑。
  `.check.txt` / `.build.txt` 是**逐字 stdout**与编译读数，同样**手改 = 造伪**。

## ★ 环境实测（**下面几条不声称穷尽**；它们决定了骨架怎么写）

1. **本机 TeX Live 2026 没有 `standalone.cls` / `preview.sty` / `pdfcrop`**（`kpsewhich` 逐个查过，均空）
   ⇒ 页盒**不能**靠 `standalone` 裁，改用 `geometry` 的 `paperwidth` 钉死。
   骨架**不依赖** `standalone` ⇒ 换一台装了它的机器，骨架不必改。
2. **需要 PATH 上有 `pdflatex`** ⇒ **干净检出复跑不相容**（与 Origin / 表格那两支同型）；
   **网页端未验 · 跨机未验**。
3. **临时目录落仓内 `build/m3-schematic-fixtures/`**（已 gitignore，**在 D 盘**），**不落 C 盘 / `%TEMP%`**；
   交给 `pdflatex` 的只有**文件名**（cwd 已是 build 下的 ASCII 短路径）—— 避路径含空格 / 非 ASCII 的坑。

## ★ "渲图看一眼"的记录（本骨架族出图时当场看的，机器判不了的那一层）

每份骨架都渲成 PNG 看过（渲图的那一节见 `../references/workflow.md`；**PNG 落在 `build/`（gitignore）里、不入库**，
入库的是上面那几份 `.pdf`）。逐份记下**从这张图读到了什么**：

| 骨架 | 从这张图读到了什么 |
| :--- | :--- |
| `pipeline-linear` | 五个阶段的先后一眼可读；**回环虚线与主流程实线分得开**；回环文字在走线下方、没压线 |
| `pipeline-branch` | 判定菱形居中，两条支路**夹角对称**；`Yes` / `No` 标签落在各自边上、没压住箭头；汇合点是一个小实心点，**方向可读** |
| `model-layered` | 三层分组框 + 列对齐的跨层连线；**强调色只用在 `Unit 2` 一处**，一眼看得出"这张图要我先看它" |
| `loop-feedback` | 上环（强调色实线）与下环（虚线）**一眼分得开**；两条环的出入点各在节点上下，**互不压线**；极性标签不压走线 |
| `mechanism-block` | 储罐 + 液面 + 粗细两条流（`Q_in` 细 / `Q_out` 粗）**可读**；控制信号那条虚线**绕到全图下方**，没穿过储罐；三个标注（`Q_in` / `Q_out` / `h(t)`）**都没有落到画外** |
| `banded-flow` | ★ **2026-10-10 视觉语言改版后新增**（不在 Task 0 那批）。三层由**背景带**分开、**不靠框**；方块条的"重复"与柱条的"高低"**各自编码了一个量**（不是装饰）；比例条一眼看出两段权重不等；`Solve for u` 那处强调色**在整片白底里跳得出来** —— 改版前所有节点填灰，强调色淹在里面 |

★ **订正（2026-10-03 · Task 2 落地 `A` 族之后）**：上表是**骨架入库时**记的"看一眼"读数，
当时只有 `F1–F6` ⇒ 那几行**全是人看出来的**。现在机械层多出 `A1`/`A3`/`A4` 三条
（`--schematic` 触发，见下节），但**上表这一层仍有两条没机械判据**：
**"箭头有没有戳进框里"（`A2` 已降级）** 与 **"两条线分不分得清主次 / 图例丢没丢 / 文字被压成不成几行"**
（没有可稳定量化的口径）⇒ 那几条**依然只能靠眼睛**。**不声称覆盖全部失败模式。**

---

## ★ `A` 族（示意图专属判据）与它的**可测性探针**

检查器 `check-figure-style.py` 在 `--schematic` 下追加三条（`F1–F6` 一字未动）：

| id | 判什么 | 量法 | 边界（**如实登记**） |
| :--- | :--- | :--- | :--- |
| `A1` | **节点框两两不重叠** | `get_drawings()` 取"既填充又描边 + 闭合 + 尺寸过线 + **含文字** + **不被同类框包住**"的块，做 bbox 相交 | `fill=none`（`mcmio`）与**不含文字**的节点框**不入集合** ⇒ 对它们**视而不见** |
| `A3` | **图内文字不越出页框** | `get_text("words")` 的词框 vs 页框，容差 `0.5pt` | 量的是"**越出页框**"（TikZ 里页框 = 图框 ⇒ 越出即被裁）；**"贴边"那半句降级**（没有稳定的安全边距阈值） |
| `A4` | **描边线宽在允许集合内** | `get_drawings()` 的 `width`，**只取 `type=='s'` 的纯描边** | 允许集合 `(0.5, 0.7, 0.9, 0.5mm, 1.4mm)→pt` 是**转写自 `assets/schematic-style.tex`**（改样式层要同批改这里）；**不含** `fs`（既填充又描边）：**箭头尖**的 `fs` 线宽是 **pgf 的产物**、不是设计线宽；**节点框**的 `fs` 线宽**就是设计线宽**，但 `A4` 一并不量 ⇒ **节点框线宽没有判据**（权威口径与实测见 `../references/schematic-style.md` §3.1「残余（不许藏）」） |
| `A2` | ~~箭头端点不落在节点框内部~~ | **降级到「看一眼」层，不在脚本里** | 见下 |

**`A2` 为什么降级**（探针实测，两列读数见 `a-measurability.txt` 段 1 表的 `A2假红(bbox/点-多边形)`）：
- **`bbox` 列**（拿**矩形 bbox** 判"框内"）⇒ 对**菱形**节点放得太大：`pipeline-branch` 的判定菱形实测 **2** 处假红，
  `mechanism-block` 实测 **1** 处；
- **`点-多边形` 列**（拿**线段端点**判）⇒ pgf 会把箭头线端**按箭头尖长度截短**、停在框**内侧**：
  `mechanism-block` 实测 **4** 处假红（`pipeline-branch` 为 **0**），而真正的箭头尖在框边上 ⇒ 这一列也假红。
两列全表合计 `1 + 4 + 2 + 0 = 7` 处。做对需要"箭头尖朝向 + 节点真实轮廓"两块几何，`get_drawings()` 给不出稳定形态 ⇒ **降级**。

**为什么是 `--schematic` 门控而不是无条件判**（探针段 3 / 段 4 是它的实测背书）：
`A4` 的允许集合是**示意样式**的 ⇒ 数据图产物上读到别的线宽（实测 `plot-python/green/out-G2` 的
纯描边宽 `0.6` 越界）⇒ 无条件跑会把一张**该全绿的数据图判红**；`A1` 的"节点框"想靠几何**推断**
也不可靠（探针段 4 把口径放宽一格 ⇒ MATLAB 数据图的图框成批入集合、当场报 38 处"重叠"）。
⇒ **射手声明目标**（`--schematic`），不靠几何猜。

**探针**（`probe-a-measurability.py`，**只读**、幂等、不写文件）：把上面每条边界**当场量出来**，
原始 stdout 逐字入库 `a-measurability.txt`（**手改 = 造伪**，要更新就重跑探针再捕获）：

```
python tests/skills/schematic/fixtures/probe-a-measurability.py > build/m3-schematic-fixtures/a-measurability.txt 2>&1
# 再把 build 下的 CRLF 捕获归一化为 LF 落到本目录（同 recon 目录的装配器口径）
```
