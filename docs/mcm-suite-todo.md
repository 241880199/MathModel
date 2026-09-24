# 美赛 Skills 套件 — 待办清单

更新：**2026-09-24（晚，Task 4 暂停 · 收工整理）**　·　设计文档 `docs/superpowers/specs/2026-09-22-mcm-skill-suite-design.md`　·　既得教训 `docs/mcm-suite-lessons.md`　·　进度台账 `.superpowers/sdd/progress.md`（git 忽略，是**恢复图**）

> **M6 试点：Task 1–3 完成（Task 3 经 8 轮），Task 4 已派但按用户要求暂停（零产出）。**
> 另有两件改变既有前提的事：**官方原题语料（2016–2026）已入库**、**本机 TeX 已装** —— 见 §A.1.2、§E.1。

**开新模块前先读 `docs/mcm-suite-lessons.md` 的 9 条通则与 7 条流程教训，写进派发指令。**

---

## A. M6 语料流水线 —— **试点 Task 1–3 完成，Task 4 暂停**（2026-09-24）

素材已到位：`corpus/历届优秀论文/` 收进 **201 份获奖论文 PDF、9,397 页**（2022–2025 O 奖 + UMAP 2000–2019）。
设计 `docs/superpowers/specs/2026-09-23-m6-corpus-pipeline-design.md`，计划 `docs/superpowers/plans/2026-09-23-m6-corpus-pipeline-pilot.md`。

**分支 `feat/m6-corpus-pipeline`，HEAD `189f0c9`，工作树干净。** 试点 = 2025 那 43 份。

| # | 任务 | 状态 |
| :--- | :--- | :--- |
| 1 | io 层 + 换行符闸门 + 忽略规则 | ✅ 完成（复审 clean） |
| 2 | 水印模块（内存处理）+ A1 全量基线 | ✅ 完成（复审 clean，3 轮） |
| 3 | 正文抽取 + A2/A3/B1/B2 | ✅ **完成：8 轮**（判据层 2 + 脚手架层 6）。`B2 42/42`、`B3/B4` 全通过、全量 `RESULT: PASS`。**脚手架层已冻结**，7 项残余移交终审 |
| 4 | 图表抽取 + C1–C4 | ⏸ **已派发后按用户要求暂停（零产出）**；任务书 `.superpowers/sdd/task-4-brief.md` |
| 5 | 公式裁图 + D1/D2 | 未开工 |
| 6 | 索引 INDEX.md + TAGS.md + 稳定 ID | 未开工 |
| 7 | 统一入口 + 试点汇总 + 放行评估 | 未开工 |
| 8 | 官方题目获取 | ✅ **已完成**（范围收窄为 **2016–2026**；用户手工下载 → 已入库，见 §A.1.2） |
| 9 | UMAP 电子版 5 份纳入 | 待排；**新事实**：comap.org 的会员墙挡住 Student Papers 与 Commentary → **2018–2024 的评委点评拿不到**，可用范围须重估 |
| — | 最终全分支审查 | **未做（必做）**：须 triage 冻结清单 7 项 + "两套落点机制并存"的债 |

**下次第一件事**：派 **Task 4（图表抽取 + C1–C4）**——任务书与派发要点已备好
（`.superpowers/sdd/task-4-brief.md`）。派发要点含：落点机制抽成 `tools/papers/report.py`
（**不改**已冻结的 `verify_b.py`）、`--limit` 必须提供且限样本不得写放行证据、新增判据须**变异证明会红且带对照**、
**不得声称"已目视确认"**（agent 看不了图，须用可核代理指标并如实写明）。

**已产出的可用物**：`corpus/papers/md/` 43 份 md（2.5 MB，正文完整、无水印）；
`corpus/官方原题/` 2016–2026 官方题面 + 数据附件（含 `PROVENANCE.md`）。**尚无图表、公式、INDEX/TAGS。**

### A.1 新素材源（2026-09-23 确认）

**官方题目存档**（此前我误判为"官网没有"，实有）：
`contest.comap.com/undergraduate/contests/mcm/previous-contests.php`
—— **2000–2026 共 27 年**，每年 `/contests/YYYY/problems/` 下逐题 PDF **+ 数据附件**（对 M5 亦可用）。
用户已定：**全抓 27 年**。配对已验证（2025 MCM Problem A 对应我们的 `2500836.pdf`）。

> **⚠️ 本节已被 §A.1.1 / §A.1.2 更正，勿照此执行**：① 并非"每年同一路径下逐题 PDF"（实测为**三条路由**）；
> ② 范围已收窄为 **2016–2026**（用户定）；③ **该项已完成并入库**。

**UMAP 期刊合集**的真实内容（此前被当"论文集"忽略）：每期含
**MCM·ICM Modeling Forum（竞赛主任的当届官方报告）+ Judges' Commentary（评委会点评）** + 当届 Outstanding Papers。
提供 O 奖论文给不了的视角——**"评委在看什么"**。本项目已认定其有价值
（`corpus/official/UMAP-2003-judges-commentary.pdf` 在册标 `[官方]†`），只是手里 27 年的同类材料没人看过。
5 份电子版（2017–2019）**零 OCR 可读**；32 份扫描件的 OCR 先挂起。

### A.1.1 官方题目：抓取路由的实测更正（2026-09-24）

**上面那条 A.1 的模型是错的**——我原以为"27 年**每年**都在 `/contests/YYYY/problems/` 下逐题 PDF"。
实测全 27 年后，**只有 16 年**是那个形态，题库分散在**三条路由**上：

| 路由 | 年份 | 形态 | 实测 |
| :--- | :--- | :--- | :--- |
| **A** 直链 | 2003、2004、2006–2017、2025、2026（**16 年**） | `/contests/YYYY/problems/*.pdf` + 数据附件（zip/xlsx/csv） | 2025 = 6 PDF + 2 zip；2026 = 6 PDF + 1 csv |
| **B** 内嵌 HTML | 2000、2001、2002、2005（**4 年**） | 同路径的 `mcm.php`／`icm.php`，题面**以 HTML 锚点内嵌**（`#problema`／`#problemb`），**不是 PDF** | 2000 `mcm.php` = HTTP 200 |
| **C** 会员资源站 | 2018–2024（**7 年**） | 索引页只给**题目标题** → `comap.org/membership/member-resources/item/<slug>`；题面在页内，PDF 走 ZOO 端点 | **端点免登录**：`/component/zoo/?task=callelement&format=raw&item_id=…&element=…&method=download` → 2022 MCM A = 3 页 / 199 KB / `%PDF-1.6` / `©2022 by COMAP` |

**两条要记住的边界**：
1. `http://www.mathmodels.org/Problems/YYYY/…` —— A/B/C 之外的**旧链接全是 404**（站已迁到 Joomla）。别照抄索引页里的旧链接。
2. 会员墙上挂的是 **Student Papers 与 Commentary（学生论文与评委点评）**，**题目本身不在墙内**。
   → 这对 **Task 9（UMAP／评委点评）** 是坏消息：2018–2024 那 7 年的点评拿不到。

**一条对 M4 有用的线索**（待核）：路由 C 的题面页带有 COMAP 自己的
`Mathematics Topics` 与 `Application Areas` 标签（2022 A：`Math Modeling` / `Sports & Recreation`）。
若各年都有，这就是**官方口径的题目分类**，可作 `TAGS.md` 的 `problem_type` 维度参照——但实测样本里
`Math Modeling` 这种标签**粒度很粗**，别当成"模型清单"，能不能用要全年份量过再定。

### A.1.2 范围收窄为 2016–2026（2026-09-24，**用户决定**）

> **用户原话**：`corpus\官方原题` 中已经涵盖 2016-2026 原题，2015 及以前的题目参考性不大。

**故"全抓 27 年"作废**，只做 **2016–2026 共 11 年**。这正好绕开最麻烦的部分：
**2000–2005 的 php 内嵌页（路由 B）整条不用做**，2003–2015 那些"只有 ICM、MCM 缺失"的
残缺年份也不必管。2016–2026 只落在**路由 A（2016/2017/2025/2026 直链）**与
**路由 C（2018–2024 会员资源站）**上。

**用户已自行下载到 `corpus/官方原题/<年>/`。实测盘点（2026-09-24）**：

| 项 | 实况 |
| :--- | :--- |
| 六份题面 PDF（MCM A–C + ICM D–F） | **11 年全部齐** |
| 2023 额外一份 | `2023_ICM_Problem_Z.pdf` = 官方「2023 ICM Problem Z: The Future of the Olympics」（©2023 COMAP，1 页），**真件**，非错文件 |
| 2018–2024 | 每篇 6 份 PDF 齐，另含各年数据附件 |

**真实缺口只有 3 个数据附件**（题面一份不缺）：

| 年 | 缺 | 官方位置 |
| :--- | :--- | :--- |
| 2016 | `ProblemCDATA.zip` | `.../contests/2016/problems/` |
| 2017 | `2017_MCM_Problem_C_Data.xlsx`、`2017_ICM_Problem_D_Data.xlsx` | 同上 |
| 2025 | `2025_Problem_D_Data.zip` | 同上 |

**两处文件名/编码待处置**：
1. `2025_ICM_Problem_E .pdf` —— **文件名里多一个空格**（`.pdf` 前），须改名。
2. `2026_MCM_Problem_C_Data.csv` —— **文本文件**，在 `core.autocrlf = true` 下 git 会改写其行尾。
   → 入库前必须给 `corpus/官方原题/**` 加根级 `.gitattributes` 的 `-text`（**不得依赖 git 的二进制自动检测**，通则 9）。

### A.2 用户已定的分析方向

> **"分析时可结合官方题目和优秀论文"**

模型选择知识 = **官方题目（输入）× 获奖论文（选用的模型）** → `TAGS.md` 需 `problem_type → models` 配对维度。
**官方题目因此是必需输入，不是可选素材。**

### A.3 待用户裁决（2026-09-24，两件一直欠着）

1. **`mcm-latex-format` 的 `Mistake 11`**：现写「在 `.tex` 里写英文以外的注释（尤其中文）……**可能**让网页端
   编译器直接报编码类错误」。**实测**（TeX Live 2026 / pdfLaTeX，2026-09-24）：含中文注释与全角标点的
   前导区**编译通过**（退出码 0、PDF 正常产出）；**正文**里混中文才失败
   （`! LaTeX Error: Unicode character 中 (U+4E2D)`）。
   → 建议**保留**"注释用英文"这条建议，但**理由换成实测口径**（与官方原件保持纯 ASCII 一致），
   并把"正文里混中文会直接失败"写成实测事实。
   此条同时**了结第一期一条悬案**：`tests/results/latex-format-baseline.md` 记着「Run B 断言中文注释在
   pdfLaTeX 下会编译失败，因本机无 TeX 无法验证，**故不采纳为事实**」——**当时拒绝得对；现在实测确认
   那个断言是错的**。

2. **`corpus/algorithms/PROVENANCE.md` §6**：把三张 `Final Solution.pdf` 登记成「从命名看**疑为竞赛论文正文**，
   属 M6 `corpus/papers/` 的候选」。**实测**（2026-09-24，从上游 `e15b0e9` 取到仓库外读取）：三份**各 1 页**、
   producer `Apache FOP Version 1.1: PDFDocumentGraphics2D`（MATLAB 打印 figure 的产物）、
   文本层只有坐标刻度与 `Total Distance = 15651.8` —— **是 TSP 的运行结果图，不是论文**。
   → 建议更正（它是"证据文件里一句不成立的语料断言"，本项目最重的那类）。**不收录**。

### A.4 已批准、待派（等仓库空下来）

- **skill 环境事实更正（用户已选 (b) 方案）**：任务书已备好 `.superpowers/sdd/task-latex-env-brief.md`。
  改动面 = **3 个已过 15 轮复审的 skill** 各 1–2 句：`mcm-latex-format`（「编译方式」段 + 常见失分点 9）、
  `mcm-selfreview`（`未判定` 那节 §4/§5）、`mcm-ai-disclosure`（全局约束）。**均须行内改写**
  （`mcm-selfreview` 上限 150 行，现 **149 行**）。
  口径：**本机已有 TeX 可自检**；**但页数/体积的权威口径仍以用户提交的那次编译为准**，本地只作预检。

## B. 不阻塞 —— 素材没到也能开工

| 模块 | skill | 依赖 |
| :--- | :--- | :--- |
| **M1 赛程编排** | `mcm-playbook`（体系入口）、`mcm-topic-select` | 只需 `INDEX.md` §2.6（赛期） |
| **M5 数据与代码** | `mcm-data`、`mcm-code` | 只需 `INDEX.md`；受 §2.4 官方 AI 边界约束（须显式声明最终判断由队员负责） |

**M1 的 `mcm-playbook` 是整套体系的入口**——目前三个已完成的 skill 是"闸门"，但没有一个告诉使用者**什么时候该干什么**。它的价值不低。

### B.1 候选：M3 的「实现半边」可提前（2026-09-23 评估外部候选后登记）

评估了 `jihe520/sci-box`（219★、**无 LICENSE**），**结论是暂不整合**，全文见 `docs/sci-box-evaluation.md`。但评估带出一条新信息：**M3 的「实现半边」不依赖语料**，理论上可不等 M6 就开工。

**两个前置决策未定，动手前先问用户**：

1. 是否破设计文档 §8 政策「只借方法论与结构」，取第三方代码？（或者只取方法、自写实现）
2. 是否把 `mcm-schematic` 的输出载体从 **TikZ / Mermaid** 改为 **draw.io**？（改的理由：用户本机无 TeX，draw.io 全程不需编译且产出可编辑矢量）

**并有接缝风险**：M3 若拆成"实现半边（提前）"与"设计规范半边（等 M6）"两半，两个半边各自收敛就会回到设计文档 M3 明令禁止的"各自不同视觉标准"。

## C. 等 M6 之后

| 模块 | skill | 备注 |
| :--- | :--- | :--- |
| **M2 论文写作** | `mcm-paper-architecture`（含 25 页预算）、`mcm-abstract`、`mcm-section-writer`、`mcm-memo` | 已完成：`mcm-ai-disclosure`、`mcm-latex-format` |
| **M3 科研图表** | `mcm-figure-choose`（语言无关的设计规范，**核心**）、`mcm-plot-python`、`mcm-plot-matlab`、`mcm-plot-origin`、`mcm-table`、`mcm-schematic` | 底层用 SciencePlots；三个 plot skill 必须共用同一份规范 |
| **M4 数学模型** | `mcm-model-select` + `references/` 8 个大类 | 架构已定：入口决策树 + 参考文献库。**注意**：官方把"模型选择与构建"列在建议谨慎用 AI 的一侧，入口须显式声明边界 |

> **M4 的素材已就位并已验证**（2026-09-23）：`corpus/algorithms/` 归档 1,262 个算法文件 + `INDEX.md`（按 8 大类组织），已做完**实跑 + 7 批数值验证**（`tests/algorithms/`）。
> **两处已知缺口**：① **mechanism 机理类完全没有**（上游无任何 ODE/PDE 实现），须另找材料；② statistics 偏薄（无假设检验/方差分析/贝叶斯）。
> 开工时用 `INDEX.md` 做**覆盖度对照**（§9），**取代码优先用 `fixed/`**（6 个净室重写版）；`src/` 里已确证的 20 个缺陷见 §10。**别把上游代码当质量资产**——它是教辅级，且"通过执行"不等于"算得对"（教训二.7）。

## D. 已知技术债

1. **`INDEX.md` 需要稳定 ID。** `tests/check-index-pointers.py` 只能抓**悬空**指针，抓不到"条号重排后仍存在、但指向了另一条事实"的**静默失效**。彻底覆盖需给每条加稳定 ID——建议与 M6 一并做。
2. **`mcm-selfreview` 已 149/150 行。** 该文件是"一段一行"的长行体，增写句子不增行、新增段落才增行。下轮若加新段落，须先压长行或下沉 `references/`。
3. **Word 用户未覆盖。** 官方同时提供 Word 模板（`INDEX.md` §1.1 收录 `.docx`），而三个 skill 均假定 LaTeX；`mcm-selfreview` 的 A3/A15 判据含 `\Team`/`\Problem` 宏这类 LaTeX 专有表述。设计文档已声明"论文载体 LaTeX"，属**已声明的取舍**；如要用 Word 需另议。
4. **`mcm-latex-format` 的 GREEN-1 证据已不可复现**（只写进了 gitignore 目录），现以 GREEN-2 为发布判据。
5. **`corpus/历届优秀论文/` 原先缺 `-text` 保护**（2026-09-24 发现，已加）。201 份 PDF 里
   **10 份的前 8KB 不含 NUL** —— 按 git 的二进制判定规则（只看前 8KB）它们会被当成**文本**，
   而本仓 `core.autocrlf = true` 会对文本做行尾转换。逐份比对后**隐患未实现**：这 10 份的
   blob 与工作树**逐字节相同**，`tests/papers/reports/origin-sha256-2025.txt` 的 43 条也 0 条不符。
   但"没被改写"当时依赖的**正是 git 的自动判定**——通则 9 明令不得依赖它，故已在 `.gitattributes`
   固化 `corpus/历届优秀论文/** -text`（对已入库 blob 无影响，它们本就是原样存储）。
   **留此条目是为了记住：这份语料的安全性原先建立在一条不该依赖的机制上。**
6. **两套落点机制并存（2026-09-24 起）**：`tests/papers/verify_b.py` 的限样本/落点守卫**已冻结、不迁移**；
   Task 4 起改用 `tools/papers/report.py`。两者并存 → **divergence 风险**，终审须裁
   （要么把 verify_b 迁过去、要么明确以 `report.py` 为准并登记 verify_b 的例外）。
7. **`corpus/papers/md/` 下 12 份含 NUL 字节**（`2504218` 16 个、`2513314` 14 个…）。git 只按**前 8KB**
   判二进制；若将来某份重生成把 NUL 排到前面，diff 会被折叠成 `Binary files differ`，
   **冲击"证据逐字可查"**。这是"不得依赖 git 的二进制自动检测"（通则 9）的另一处落点。
8. **两条通则候选，建议写进 `docs/mcm-suite-lessons.md`**：
   ① **同一语义必须用同一谓词** —— `limit > 0` 与 `limit == 0` 混用，`--limit -3` 就从一个**单 token**
      的旁路把两条反向守卫全绕过（实测：`RESULT: PASS`、无 LIMITED 后缀、退出码 0、放行证据留旧 PASS）；
      更值得记的是：该歧义**上一轮已被登记为 Minor**，下一轮的修复把它**升级成了绕过通道**。
   ② **"存在某条消息"不能靠子串匹配来判** —— 被测文本可能**复述**该消息：R10 那句假话
      （「见本报告中的落点守卫 FAIL 消息，判 FAIL」）**冒充了守卫消息本身**，把驱动器骗成"守卫在场"，
      收紧为**行首匹配**之后旁路才现形。

## E. 已定的决策 —— 不要再问

- 使用阶段：**赛中执行优先，兼顾备赛**
- 论文载体：**LaTeX**（网页端编译）；建模绘图：**Python / MATLAB / Origin 混合**
- 语料策略：**提炼内嵌 + 保留可检索语料库**（不是只提炼，也不是只检索）
- M4 架构：**入口决策树 + `references/` 模型库**（不是每模型一个 skill，也不是按大类拆多个）
- skill 归属：**项目级 `.claude/skills/`**，非全局
- 建设顺序：**M6 → M2 → M3 → M1 → M4 → M5**
- **第三方素材：不因许可证排除，按价值判断收录**（2026-09-23 定）。**此条取代设计文档 §8 的「只借方法论与结构，内容从自己提供的语料重新提炼」政策**——那一条是当时因多数仓库无 License 而立的，现作废。仍须逐份留 `PROVENANCE`（来源、commit、许可状态），以便日后追溯。

### E.1 环境（2026-09-23 实测）

| 工具 | 状态 | 影响 |
| :--- | :--- | :--- |
| **MATLAB R2025b** | ✅ `/d/Software/Matlab/bin/matlab`，`-batch` 可跑 | **MATLAB 代码骨架本机可验证**（教训 7 可满足，不像 LaTeX 那边什么都验不了） |
| TeX | ✅ **已装（2026-09-24）**：TeX Live 2026 `scheme-small`+美赛包集，`D:\Software\texlive\2026`，986 MB，免管理员、**不占 C 盘**，已入用户 PATH（winreg 保 `REG_EXPAND_SZ`，未用 `setx`）。`pdflatex`/`xelatex`/`lualatex`/`latexmk`/`tlmgr`/`kpsewhich` 齐，源指向 USTC 镜像 | **教训 6 已可退休**：已实测编译 `mcm-2027-summary.tex` 成功（2 页/71 KB/零 overfull）。⚠️ GitHub Releases 本机被限速掐断（~5–25 KB/s），装 TeX 类一律走国内 CTAN 镜像 |
| `pdfinfo`/`pandoc` | ❌ 仍缺 | 页数用 `PyPDF2` 读（`mcm-selfreview` 已是此法），无碍 |
| Python 3.11.9 | matplotlib 3.10.7 / numpy / scipy / pandas / sklearn / **networkx** 有 | — |
| Python 缺 | **`statsmodels` / `cvxpy` / `pulp` / `scienceplots`** | M4 若给 Python 代码骨架，这几类（统计、优化）要么先装依赖，要么改走 MATLAB |

## F. 关键日期

| 日期 | 事项 |
| :--- | :--- |
| **2027-01-28 15:00 EST** | 报名与缴费截止 |
| **2027-01-28 17:00 EST** | 开赛（赛期 99 小时） |
| **2027-02-01 20:00 EST** | 停止修改 |
| **2027-02-01 21:00 EST** | 提交截止 |
| 2027-05-08 | 结果公布 |

---

## G. 算法归档 `corpus/algorithms/` —— 主体已完成（2026-09-23）

来源 `HuangCongQing/Algorithms_MathModels` @ `e15b0e9`。台账：`INDEX.md`（八大类索引 + 缺陷表 + 验证结果）、`PROVENANCE.md`（来源/许可/可复现步骤）、`fixed/`（净室重写版）。

### G.1 已完成

| 项 | 结果 |
| :--- | :--- |
| 归档 | 1,262 个文本文件（GBK→UTF-8），剔除 1,566 个二进制/PDF |
| 实跑 | 一级层 68 脚本：**44 通过 / 16 失败 / 6 个 GUI 死循环** |
| 数值验证 | **7 批、50+ 项**，每项对独立参照（`tests/algorithms/numerics*-report.txt`） |
| 缺陷登记 | **20 个**：16 个工程性 + **4 个算法性**（§10.1，最要紧） |
| 净室重写 | **6 个**：AHP、指数平滑、趋势外推、模糊综合评价、奇偶规则元胞自动机、欧拉回路 |

### G.2 未做 —— 按优先级

| # | 事项 | 说明 |
| :--- | :--- | :--- |
| 1 | **两个已登记未重写的缺陷** | `BGf.m`（最小费用流不终止）、自适应滤波（收敛循环只跑一轮）。用户已授权"按算法名自行编写正确版本" |
| 2 | 一级层**执行通过但未验数值**的脚本 | 模糊模式识别、`interp_grid`、`af_classify_BP/LVQ`、SA/GA 的 TSP 与函数优化、`stepwise_regression`、`unlinear_regression`、`var_cluster` 的聚类结果 |
| 3 | **二级层 1,028 个文件** | 完全未验证 |
| 4 | **mechanism 机理类缺口** | 上游无任何 ODE/PDE 实现，M4 的这一类要另找材料 |
| 5 | 6 个 GUI 死循环脚本 | 无法无人值守，其正确性未评估 |

> **动手前先读教训二.7**：实跑只能抓工程性缺陷，**算法性缺陷必须拿独立参照才现形**。加新验证时，每项都要能说清"参照是什么、它为什么独立"。
