# 美赛 Skills 套件 — 待办清单

更新：**2026-09-26（Task 5/6/6b/7 全部完成 + 整分支终审 + 终审修复轮）**　·　设计文档 `docs/superpowers/specs/2026-09-22-mcm-skill-suite-design.md`　·　既得教训 `docs/mcm-suite-lessons.md`　·　进度台账 `.superpowers/sdd/progress.md`（git 忽略，是**恢复图**）

> **M6 试点：Task 1–7 + 6b 全部完成**（Task 3 经 8 轮、Task 4 经「实施 + 复审 + 修复」、Task 5 经 5 轮、
> Task 6 经 6 轮、Task 6b 分 2a/2b 两阶段、Task 7 经「实施 + 复审 + 修复」）。**整分支终审已做完**，
> 结论是**可以合并**（0 Critical）；终审发现的处置见 **`docs/mcm-suite-triage-2026-09-26.md`**。
> 另有两件改变既有前提的事：**官方原题语料（2016–2026）已入库**、**本机 TeX 已装** —— 见 §A.1.2、§E.1。
> **下次第一件事 = Task 9 的 recon（定全量 201 份的题号口径，任务书已起草）；扩语料前不必再做 Task 5/6/7。**

**开新模块前先读 `docs/mcm-suite-lessons.md` 的 9 条通则与 7 条流程教训，写进派发指令。**

---

## A. M6 语料流水线 —— **试点 Task 1–7 + 6b 完成**（2026-09-26）

素材已到位：`corpus/历届优秀论文/` 收进 **201 份获奖论文 PDF、9,397 页**（2022–2025 O 奖 + UMAP 2000–2019）。
设计 `docs/superpowers/specs/2026-09-23-m6-corpus-pipeline-design.md`，计划 `docs/superpowers/plans/2026-09-23-m6-corpus-pipeline-pilot.md`。

**分支 `feat/m6-corpus-pipeline`，工作树干净。** 试点 = 2025 那 43 份。
（原先这一行钉着 `HEAD a17b6f6`——那是 2026-09-24 的快照，**已过期**；钉 commit 的正文一律不写在文档里，
要现状就 `git log -1 --oneline`。）

| # | 任务 | 状态 |
| :--- | :--- | :--- |
| 1 | io 层 + 换行符闸门 + 忽略规则 | ✅ 完成（复审 clean） |
| 2 | 水印模块（内存处理）+ A1 全量基线 | ✅ 完成（复审 clean，3 轮） |
| 3 | 正文抽取 + A2/A3/B1/B2 | ✅ **完成：8 轮**（判据层 2 + 脚手架层 6）。`B2 42/42`、`B3/B4` 全通过、全量 `RESULT: PASS`。**脚手架层已冻结**，7 项残余移交终审 |
| 4 | 图表抽取 + C1–C4 | ✅ **完成**：实施 `4330eb5` → 复审 13 条（1 条阻断）→ 修复轮 `8690c73` + `a17b6f6`。全量 43 份 `RESULT: PASS`、`发布放行: 已放行` |
| 5 | 公式裁图 + D1/D2 | ✅ **完成：5 轮**（`8cf223e` 定案：0 Critical / 4 Important / 5 Minor） |
| 6 | 索引 INDEX.md + TAGS.md + 稳定 ID | ✅ **完成：6 轮**（`1491547` 定案；34 条判据） |
| 6b | 题型标注 + 配对表 + 匹配度 | ✅ **完成：阶段 1 + 2a + 2b**（67 题标注 · `MODEL_MAP.md` 召回 **0.9130**、精确性 **496/496**、未解释 **0**；`verify_types` 10 条 + `verify_map` 16 条） |
| 7 | 统一入口 + 试点汇总 + 放行评估 | ✅ **完成**（`faa3aae`）：`tools/papers/cli.py` + `tests/papers/verify_all.py`（8 个判据脚本**由磁盘派生**）。全量放行门实测 **EXIT=0**、`pilot-summary.txt` 逐字节可重放 |
| 8 | 官方题目获取 | ✅ **已完成**（范围收窄为 **2016–2026**；用户手工下载 → 已入库，见 §A.1.2） |
| 9 | UMAP 电子版 5 份纳入 | 待排；**新事实**：comap.org 的会员墙挡住 Student Papers 与 Commentary → **2018–2024 的评委点评拿不到**，可用范围须重估。**扩到全量 201 份被题号口径卡着**（`io.problem_of` 实测 **77/201** 取不到题号）⇒ 先 recon 定口径（任务书 `.superpowers/sdd/task-9-recon-brief.md`） |
| — | 最终全分支审查 | ✅ **已做（2026-09-26）**：结论 **可以合并**（0 Critical）。处置见 `docs/mcm-suite-triage-2026-09-26.md`；修复轮即本轮 |

### A.6 Task 4 的产出与遗留（2026-09-24）

**产出**：`tools/papers/report.py`（落点机制，Task 4–7 共用）、`tools/papers/figures.py`（按图注定位抽图表）、
`tests/papers/verify_c.py`（C1–C4 判据）；证据 `tests/papers/reports/c-report.txt`（放行）、`c-mutation-evidence.txt`
（**11 条变异 + 10 次对照**，驱动器自己断言"每个变异都实测判了 FAIL"）。`tools/papers/report.py` 之前**没有**落点机制，
`verify_b.py` 保持冻结、未迁移 → **§D 第 6 条的“三套落点机制并存”仍在**（该条 2026-09-26 已由“两套”改名为“**三套**”，引用文字按新名；第三套 = `tests/papers/verify_all.py` 里照 `report.py` 另写的那份复制品）。

**这轮最值钱的一条（阻断项，已修）**：C4 第二层「产出图来源」原先 `c4 = c4 and (prov is not False)`
→ `prov is None` **不改 c4 → 该篇判绿**；而**同一处文档字符串与报告都写「不记为通过」**——
代码、措辞、行为三者互相矛盾，且 **M-C4b（删掉 `strip` → 产出图张张带水印）那一跑里就实际漏过 1/7**。
修法 = `prov` 改**三态**（True 已验证 / False FAIL / **None 未验证**），`None` 既不算通过也不硬失败该篇，
但**计数 + 受新上界 `PROV_UNVERIFIED_CEILING=10%` 约束**，超界全批判 FAIL；报告**改印覆盖数、不再说"全通过"**。
**这条值得记进通则**：*「未验证」是「通过」与「失败」之间唯一诚实的位置*——并进通过就是本项目犯过六次的那一族。

**判据现状**：C1 图注 935 条 / 产出 908 张（差额 27 全登记 2.89%）；C2 最小非白 2.32%；C3 零缺；
C4 机制层 43/43、来源层**已验证 42/43、未验证 1**（`2507789`）。人工目视闸门已由用户判定（6 张送检样件无水印）。

**遗留（详见 §D 第 8 条）**：908 张产出图**"内容框对了没有"无任何判据覆盖**（无独立参照，本轮最大空白）。

### A.7 Task 5 前的下一步

**✅ 已裁决（2026-09-24，用户选 ③）**：**图注级别引文属合理引用，照推。**
即 `tests/papers/reports/c-report.txt` 与 `c-mutation-evidence.txt` 里逐字引用的图注原文
（如 `｜图注 'Figure 11 Countries with significant flu'`）**不构成推公开远端的障碍**，
这两个文件随本轮一并同步。
**✅ 同步已完成（2026-09-24 晚三）**：远端 `main` = **`600c495`**（`ba590a9..600c495`），**99 个文件、0 个 PNG**；
实测增量 = 改 `docs/mcm-suite-todo.md` + 新增 8 个自研文件；反向核确认 `ba590a9..HEAD` 之间新增了 **13 张 PNG**，
全部被排除规则挡在快照之外。走的是仓库外 worktree + 普通快进，未被拦。

**但把规则写清楚，别让它退化成"凡引文都能推"**：
- **允许**：**零散的短引文**——图注/表题的完整句、单个短语，用于说明"这一条为什么没产出"等判据依据。
- **仍禁止**：**成段的正文**、整页渲染图（`*.png` 已按目录排除）、以及任何**连续大段**的原文摘录。
  即"引用一句"可以，"转载一篇"不行。
- **判断口径**：宁可保守。若将来某个证据文件开始**成段**引用第三方正文，**回到本条重新裁决**，
  不要拿这一次的结论直接套用。
- **每次同步仍须逐项核增量**（别只信规则）；本轮实测增量 = 改 `docs/mcm-suite-todo.md` +
  新增 8 个自研文件，**PNG 一张都没进**。

**下一步**：派 **Task 5（公式裁图 + D1/D2）**——任务书尚未写，写时须沿用本轮的落点机制与四条派发要点
（`report.py` / `--limit` / 变异证明带对照 / 不得声称目视确认）。

**已产出的可用物**：`corpus/papers/md/` 43 份 md（2.5 MB，正文完整、无水印）；
`tests/papers/reports/` 的图表证据；`corpus/官方原题/` 2016–2026 官方题面 + 数据附件（含 `PROVENANCE.md`）。
**尚无公式、INDEX/TAGS。**

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

### A.3 已裁决并落地（2026-09-24 晚二）

1. **`mcm-latex-format` 的 `Mistake 11`** —— ✅ **已改**（commit `47f2335`）。保留"注释用英文"这条建议，
   **理由换成实测口径**：官方模板与修正副本都是纯 ASCII，故与官方原件同口径；
   **实测**（TeX Live 2026 / pdfLaTeX）：**注释**里混中文与全角标点**不会**报错（退出码 0、PDF 正常产出，
   原「会报编码类错误」的说法**已被实测推翻**）；**正文**里混中文才**会**
   （`! LaTeX Error: Unicode character 中 (U+4E2D)`）。
   → **第一期那条悬案随之了结**：`tests/results/latex-format-baseline.md` D3 记「Run B 断言中文注释在
   pdfLaTeX 下会编译失败，本机无 TeX 无法验证，**故不采纳为事实**」——**当时拒绝得对；现在实测确认
   那个断言是错的**。⚠️ 该 baseline 文件按"历史运行记录、非断言"的定位**未改动**（D3 那段保留原样）。

2. **`corpus/algorithms/PROVENANCE.md` §6** —— ✅ **已改**（commit `279e75d`）。三张 `Final Solution.pdf`
   原登记为「疑为竞赛论文正文，属 M6 `corpus/papers/` 候选」；实测（从上游 `e15b0e9` 取到仓库外读取）：
   三份**各 1 页**、producer `Apache FOP Version 1.1: PDFDocumentGraphics2D`（MATLAB 打印 figure 的产物）、
   文本层只有坐标刻度与 `Total Distance = 15651.8` —— **是 TSP 的运行结果图，不是论文**。
   → §6 由「待定事项」改为「已结事项」：**不收录、不进 `corpus/papers/`**；§4 剔除表同句一并更正。

### A.4 已完成（2026-09-24 晚二）

- **skill 环境事实更正（(b) 方案）** —— ✅ **已落地**（commit `47f2335`），任务书 `.superpowers/sdd/task-latex-env-brief.md`。
  五处改动：`mcm-latex-format`（「编译方式」段 + 常见失分点 9）、`mcm-selfreview`（`未判定` 那节第 2、4 条）、
  `mcm-ai-disclosure`（全局约束）。**均行内改写，`mcm-selfreview` 改后 `wc -l` 仍为 149**。
  口径：**本机已有 TeX 可自检，凡声称编译结果须附真实命令与输出**；**但页数/体积的权威口径仍以用户提交的那次编译为准**，本地只作预检、不得代填。
  验证证据（本机复跑 `pdflatex` ×2）：`main.pdf` **2 页 / 71,227 字节 / Overfull·Underfull 计数 0**，
  唯一告警为官方模板自带的 `fancyhdr: \headheight too small (12.0pt)`。

### A.5 远端仓库（2026-09-24 建立）

`https://github.com/241880199/MathModel`（**公开**）。本次之前本仓**无任何远端**。

| 分支 | 内容 |
| :--- | :--- |
| `main`（**`600c495`**，2026-09-24 晚三更新） | 历史 `Initial commit → 代码快照 → 合并 → 真 README → 环境事实更正同步 → Task 4 同步`；**99 个文件**（91 + Task 4 的 8 个新文件），**0 个 PNG** |
| `code-snapshot`（`5221722`） | 内容已全在 `main` 里，**现为冗余**（要删说一声） |

**增量同步的现成配方（2026-09-24 晚二实测走通，未被拦）**——不必再造无父快照：

```bash
git worktree add "<仓库外的目录>" main          # 主工作树一个字节不动
cd "<仓库外的目录>"
git checkout feat/m6-corpus-pipeline -- <自研文件路径…>   # 只取自研文件
git commit -F -                                 # README.md 等 main 独有文件保持原样
git push origin HEAD:main                       # 普通推送；main 已存在故是快进，无须 --force
git worktree remove "<仓库外的目录>"
```

关键：**先算准增量**。两条判据——① `git ls-tree -r --name-only main` 的 91 个路径逐个看是否与 HEAD 不同
（`git diff --name-status main..HEAD -- "${F[@]}"`，用数组传路径，别用正则过滤：**非 ASCII 路径会被 git 加引号，
按 `^[AMD]\t` 写的正则匹配不到，反而误伤 `corpus/algorithms/*.md`**）；② 再确认 HEAD 没有新增的自研文件。
本次实测增量恰为 **9 个文件**，`README.md` 是 main 独有（HEAD 无）→ **保留，不得删**。

**⚠️ 远端只含自研代码与文档，不含任何第三方语料** → 那 **1.86 GB**（COMAP 获奖论文、官方赛题与数据、
官方文档 PDF、无许可证的第三方算法源码，以及论文正文抽取与整页渲染图）**本机之外没有副本**。
**"推了 = 备份了"对这部分不成立。** 远端 README 里已把这点写在明面上。

**操作注意（踩过的坑，别重犯）**

0. **排除规则改为通用式，别逐前缀列举**：既有规则是按前缀列的 `tests/papers/reports/a4-*.png` 与
   `tests/papers/recon/*.png`，**新增产物就会漏**（Task 4 起的 `c4-*.png` 正是这么长的）。
   一律按**目录**排除：`tests/papers/reports/*.png` 与 `tests/papers/recon/*.png` ——
   它们是**第三方论文页面的渲染图**，本地入库作证据可以，**推公开远端不行**。
1. **不要在主工作树里 `git checkout main`** —— git 会把那 1.86 GB 语料从工作树**删掉**
   （它们在 main 的树里不存在）。main 侧操作一律用**仓库外的独立 worktree**。
2. 本机访问 GitHub 需 `git config http.sslBackend schannel`（默认 CA 取不到证书）；
   链路有**间歇 502**，**重试即通**（同一条 URL 多试几次；`raw`/`api`/`git` 三个通道都时通时断）。
3. **两类推送被 harness 硬拦，只能由用户在自动模式之外亲自按**：
   ① 整仓（含第三方版权语料）批量推到**本次会话才添加的公开远端**；
   ② **强推**覆盖远端 `main`（= 重写远端历史、覆盖非本人提交的提交）。
   → 后者已改走**普通合并**，结果等价且什么都没丢，**以后也不需要强推**。
4. 若日后想让大语料也有远端副本：**建私有仓库**，但按实测链路速率（GitHub Releases 5–25 KB/s）
   1.86 GB 基本推不完；更现实的是**本地/网络盘裸库备份**。

## B. 不阻塞 —— 素材没到也能开工

| 模块 | skill | 依赖 |
| :--- | :--- | :--- |
| **M1 赛程编排** | `mcm-playbook`（体系入口）、`mcm-topic-select` | 只需 `INDEX.md` §2.6（赛期） |
| **M5 数据与代码** | `mcm-data`、`mcm-code` | 只需 `INDEX.md`；受 §2.4 官方 AI 边界约束（须显式声明最终判断由队员负责） |

**M1 的 `mcm-playbook` 是整套体系的入口**——目前三个已完成的 skill 是"闸门"，但没有一个告诉使用者**什么时候该干什么**。它的价值不低。

### B.1 候选：M3 的「实现半边」可提前（2026-09-23 评估外部候选后登记）

评估了 `jihe520/sci-box`（219★、**无 LICENSE**），**结论是暂不整合**，全文见 `docs/sci-box-evaluation.md`。但评估带出一条新信息：**M3 的「实现半边」不依赖语料**，理论上可不等 M6 就开工。

**两个前置决策未定，动手前先问用户**：

1. ~~是否破设计文档 §8 政策「只借方法论与结构」，取第三方代码？~~ —— ✅ **已由 §E 自动回答**：
   该政策**已于 2026-09-23 作废**（现行 = 第三方素材不因许可证排除，按价值判断收录，须留 `PROVENANCE`）。
   **故本题不再是前置决策**；`sci-box` 那次的具体结论「暂不整合」仍按 `docs/sci-box-evaluation.md` 为准。
2. ~~是否把 `mcm-schematic` 的输出载体从 **TikZ / Mermaid** 改为 **draw.io**？~~
   —— ✅ **已裁决（2026-09-27）= TikZ 单一载体**；**Mermaid 从设计里去掉**（它不是 `mcm-schematic` 的交付载体）。
   判据 = **载体选择以“agent 能否看见产物”为准**：本机已端到端实测 `pdflatex` 编译 TikZ → `fitz`(PyMuPDF) 渲 PNG → **agent 可读图**（探针 `build/m3-carrier/`）；
   **draw.io 在本机没有可执行路径**（无桌面版 / 无 CLI；装它要走 GitHub Releases，而本机实测被限速到 5–25 KB/s 并掐断）⇒ **产物看不见**。
   **draw.io 那两条理由不足以翻案**：①“不需编译”的价值被“**agent 看不见产物 ⇒ 无法自检、无法进证据链**”（通则 7）抵消——后者是**判据层**的要求，前者只是**便利**；
   ②“可编辑矢量”在 TikZ 里同样成立（源码即矢量，改的是代码），且**只有同源才能强制“共用同一份规范”**（M3 的硬约束）。
   ⚠️ **连带失效（按通则 6 全库回扫所得）**：`docs/sci-box-evaluation.md` 里以此为据的几处需一并补注——
   `:89`「取 draw.io 就要改这一行……改动本身我认为**是对的**」、`:103` 的“自写 SKILL.md 把 draw.io 的中文字宽模型/连接器语义下沉”落地方案、
   `:80`/`:127` 的“与既有 TikZ/Mermaid 决策打架 / 冲突”判定。**（待用户批后再改，见台账。）**

**并有接缝风险**：M3 若拆成"实现半边（提前）"与"设计规范半边（等 M6）"两半，两个半边各自收敛就会回到设计文档 M3 明令禁止的"各自不同视觉标准"。

## C. 等 M6 之后

| 模块 | skill | 备注 |
| :--- | :--- | :--- |
| **M2 论文写作** | `mcm-paper-architecture`（含 25 页预算）、`mcm-abstract`、`mcm-section-writer`、`mcm-memo` | 已完成：`mcm-ai-disclosure`、`mcm-latex-format` |
| **M3 科研图表** | `mcm-figure-choose`（语言无关的设计规范，**核心**）、`mcm-plot-python`、`mcm-plot-matlab`、`mcm-plot-origin`、`mcm-table`、`mcm-schematic` | 底层用 SciencePlots；三个 plot skill 必须共用同一份规范。**2026-09-27 起 M3 已开工**：`mcm-figure-choose` 前 6/7 任务已交付（详见 **§H**）；剩余 **Task 7 引用完整性检查器**（必须用假 skill 做变异——真 `mcm-plot-*` 尚未建，否则此判据恒真），**待 `mcm-plot-*` 出现时即生效** |
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
6. **三套落点机制并存（2026-09-24 起两套，2026-09-26 更新为三套）**：
   ① `tests/papers/verify_b.py` 的限样本/落点守卫（**已冻结、不迁移**——它是那套防线的原件）；
   ② `tools/papers/report.py` 的（Task 4–7 共用；`verify_c/d/ids/map/types` 与 **2026-09-26 起**的
      `verify_io/wm` 走它）；
   ③ `tests/papers/verify_all.py` 里**照 ② 另写的一份复制品**（`limited_path` / `resolve_summary` /
      `recheck_summary`）——因为 `report.resolve_report()` 的落点名是 `f"{kind}-report.txt"`，
      **拼不出 `pilot-summary.txt`** 这个被任务书三处点名的名字。
   **敞口（终审给的结论）**：③ 有**每次运行的分支对账**（`branch_crosscheck`：两边必须走同一个分支，
   漂移即红，复核员造 4 种漂移验证 4/4 判红）——但它对账的**粒度是分支、不是文件名**，
   且**不比 `recheck_target` 的恒等化**（写前复核那道对 ③ 是另写的）。于是两类漂移对账**看不见**：
   **(a)** ③ 的落点**文件名**悄悄改成别的文件（两边仍是"同一个分支"）；
   **(b)** ③ 的写前复核被削弱成恒等函数（对账只看 `resolve_summary` 的分支）。
   处置：**登记为已知债**（本条），不并入——并入要动 ② 的落点名约定（`f"{kind}-report.txt"`），
   而那份约定是 7 个脚本共用的，改它属于另一次解冻。
7. **`corpus/papers/md/` 下 12 份含 NUL 字节**（`2504218` 16 个、`2513314` 14 个…）。git 只按**前 8KB**
   判二进制；若将来某份重生成把 NUL 排到前面，diff 会被折叠成 `Binary files differ`，
   **冲击"证据逐字可查"**。这是"不得依赖 git 的二进制自动检测"（通则 9）的另一处落点。
8. **C4 第二层（产出图来源层）的三处残渣**（2026-09-24 复核轮登记，来源：`task-4-review.md` §7）：
   `verify_c.strip_provenance` 用 A/B 差分证明"产出图来自置空后的渲染"，方向对、灵敏度是升的
   （复审给的修复前后对比是假 `True` 从 2 份 → 0 份、"适用"份数 4 → 6，即**红更多、假绿更少**；
   2026-09-24 复核轮 7 份口径重跑的可查数是：正确代码 **7/7 已验证**、M-C4a 下 **7/7 未验证**、
   M-C4b 下 **6 份 FAIL + 1 份未验证** —— 见 `tests/papers/reports/c-mutation-evidence.txt`），
   但：**(a)** B 侧归一化只是**近似**（A 侧解析全篇、B 侧只解析被探的那一页），若"解析历史"
   效应是文档级而非页级，两侧仍可能错位（后果 = 假 FAIL 或 `None`，两者都不再静默绿）；
   **(b)** 根因**机制不明**（只登记实测量）却站在**判定链**上，而机制清楚的像素代理层只在筛选
   —— 强度定位不对称；**(c)** 每篇的结论建在**最多 4 条带中的第一条**有结论的带上
   （`STRIP_PROBE_MAX` + 首次 `return`）。**全量 201 份之前须重估这三条**。
9. **五条通则候选，建议写进 `docs/mcm-suite-lessons.md`**：
   ① **同一语义必须用同一谓词** —— `limit > 0` 与 `limit == 0` 混用，`--limit -3` 就从一个**单 token**
      的旁路把两条反向守卫全绕过（实测：`RESULT: PASS`、无 LIMITED 后缀、退出码 0、放行证据留旧 PASS）；
      更值得记的是：该歧义**上一轮已被登记为 Minor**，下一轮的修复把它**升级成了绕过通道**。
      落点之二：`verify_c.py` 曾用**私有常量**重实现 `find_watermark_xrefs` 的谓词（今日逐条件等价、
      **不共享代码**）——机制一改它就静默扫错集合；2026-09-24 复核轮已改为**调机制自己的谓词 + 留副本 +
      逐篇断言两集合相等**（分叉即 FAIL）。
   ② **"存在某条消息"不能靠子串匹配来判** —— 被测文本可能**复述**该消息：R10 那句假话
      （「见本报告中的落点守卫 FAIL 消息，判 FAIL」）**冒充了守卫消息本身**，把驱动器骗成"守卫在场"，
      收紧为**行首匹配**之后旁路才现形。同一族的第三例见 ③。
   ③ **恒真的比对不是判据** —— `水印对象 == strip` 两边是同一次调用的同一个谓词
      （`strip_in_memory` 的返回值按定义就是 `len(find_watermark_xrefs(doc))`），
      变异下 strip 一个流都没清、等式照样成立；同理 `A == B` 不能当"这条带盖到水印"的证据。
      判据必须是**有区分力**的那一半（`残留流长>0 == []`）。2026-09-24 复核轮已把它改成
      **覆盖指标**并逐处注明，且加了"C1 差额登记"那类**零区分力复述**的显式标注。
   ④ **「未验证」是「通过」与「失败」之间唯一诚实的位置** —— C4 第二层曾把 `prov is None`
      （该带盖不到水印、差分无区分力）当成通过，而**同一处的文档字符串与报告都写「不记为通过」**：
      代码、措辞、行为三者互相矛盾，且 M-C4b（删掉 `strip` → 产出图张张带水印）那一跑里
      **就实际漏过 1/7**。硬失败会因非缺陷卡住放行，不计入又会重蹈"什么都没验就报绿"——
      故 `None` 必须**单列**：既不算通过也不硬失败该篇，但**计数 + 受上界约束**（超界全批判 FAIL），
      且报告**改印覆盖数、不再说"全通过"**。
   ⑤ **判"文件有没有被改"，要用能应用过滤器的工具** —— 2026-09-24 实测：`tools/papers/watermark.py`
      在盘上是 CRLF、仓库里是 LF，**`git diff` 空而裸 `sha256sum` 不同**（磁盘 3039 字节 / HEAD 2965 字节，
      74 处 CRLF）。→ 一律用 `git hash-object`（会应用 `core.autocrlf` 与 `.gitattributes`）比 blob sha。
      这与通则 9（不得依赖 git 的二进制自动检测）是同一条链上的另一半：**别拿裸字节哈希去判 git 的事**。
      **2026-09-26 更新**：那条分叉**已收敛**（`.gitattributes` 给 `tools/papers/**` 与 `tests/papers/**`
      加了 `-text`，两个分叉文件用 `git checkout --` 收敛后**工作树变 LF、blob 零变化**）⇒
      本节⑤引的那两个字节数只作**当日实测的历史记录**，**不再是现状**。
      另记一条**方法上的更正**：`git checkout -- <路径>` 在"索引 stat 认为文件干净"时**不会重写工作树**
      （`git checkout-index -f` 同样不写）——要先删掉文件再 checkout，字节才真的变。实测见本轮修复报告。

10. **908 张产出图的「内容框对了没有」无任何判据覆盖**（2026-09-24 登记，Task 4 复审确认，**本轮最大空白**）。
    现有判据全是**间接**的：C1 数图注、C2 查非白占比、C3 查配文、C4 查水印——**没有一条能回答"这张 PNG 框的是不是那张图、有没有切掉半张"**。
    要覆盖它需要一个**能看图的独立参照**（人或一个可信的视觉模型），本项目目前没有。**全量 201 份之前须先解决或明确接受。**

11. **远端排除规则只按扩展名，没覆盖"我们自己在证据里逐字引用第三方原文"**（2026-09-24 发现并裁决）。
    实测 `tests/papers/reports/c-report.txt` 的"未产出"登记行带**图注原文**（如 `｜图注 'Figure 11 Countries with significant flu'`），
    仅该文件约 **5 KB**；`c-mutation-evidence.txt`（57 KB）大概率还有。
    既有规则排的是 `tests/papers/reports/*.png` 与 `tests/papers/recon/*.png`（**页面渲染图**），**这类"文本引文"不在其列**。
    → **已裁决（用户选 ③）：零散短引文属合理引用，可推；成段正文摘录仍禁止。**
    **口径与边界见 §A.7**——这条例外的存在本身是**债**：规则从"按扩展名"退成了一个需要人判断的边界，
    将来证据文件开始成段引正文时**必须回来重裁，不得直接套用本次结论**。

12. **`verify_io.py` / `verify_wm.py` 违反项目自己的两条纪律 → 2026-09-26 已修**（Task 7 登记，终审列为
    "便宜可修"）。**两条违例**：① **没有 `--limit`**（违教训 4.6「每个校验脚本必须提供 `--limit`」）；
    ② 两者用 **`traceback.format_exc()` 落盘**（崩溃会把**绝对路径**写进入库证据，违「只写仓库相对路径」）。
    后果：汇总无法对它们收 `--limit`（`supports_limit` 对不解析 argv 的它们传 `--help` **等于真跑一次**），
    且那两份产物**自己一个都不扫**绝对路径痕迹（靠 `verify_all.check_evidence` 从外面补那一刀）。
    **修复（2026-09-26）**：两者加 `--limit`（走 `report.resolve_report` / `recheck_target` / `flush` /
    `path_audit` / `fmt_exc` 的现成机制；**`--limit` 在这两个脚本里只改落点**——它们没有"前 N 份 PDF"
    这种样本口径）；放行证据 `io-report.txt` / `wm-report.txt` 已重出。
    ⇒ `verify_all` 里对它们的**特例说明已删**（不再写"本次运行已触碰放行证据"），报告口径与其它脚本一致。
    红证据：`tests/papers/reports/finalfix-mutation-evidence.txt`（FX-1 / FX-2：把落点决策换成放行证据本体 ⇒ 判红）。
    **顺带实测出的一条**（登记，不改代码）：`verify_io/wm` 沿用的那份「跑前/跑后 sha256 自检」**测不到本脚本
    自己的覆写**——`post` 是在 `report.flush` **之前**测的（`verify_d/ids` 同形；`verify_c` 反过来，先 flush 再测）。
    真正兜住"绕过落点守卫"的是写前复核与退出码，外侧还有汇总那两道。见同一份证据的 FX-1 注。
    **措辞更正（2026-09-27）**：报告里那句「**放行证据完整性自检**（只对限样本跑做）· … ·
    两次相同 = True」**读起来像正面检查**，但要按它的真面目读——**本自检测不到本脚本自身的
    覆写**（见本条；发射点在 `tests/papers/verify_io.py` / `verify_wm.py` 的限样本分支，
    两处是**冻结脚本**，本轮只登记不改）。判红靠的是**写前复核 + 退出码**。
    **口径备忘（2026-09-27 登记，不是缺陷）**：`verify_io/wm` 的 `--limit` **只改落点、
    不改判据集**（这两个脚本没有"前 N 份 PDF"这种样本口径，`--limit` 不真的少验样本）
    ⇒ 它对教训 4.6「**成本**」那个目的**不成立**，对「**限样本不得冒充放行**」那个目的**成立**
    （限样本落点是 `reports-limited/`，且 RESULT 行明写"非放行依据"）。

13. **`tools/papers/report.py` 的 `ABSPATH_TRACE` 与 `_ABS_POSIX` 谓词不一致 → 2026-09-26 已统一**。
    原先"审计"那条的 POSIX 支只有 `Users|home|root`，而"消毒"那条还认 `tmp|var|opt|mnt|Volumes`
    ⇒ `/tmp/x`、`/opt/x` 一类路径**对审计不可见、对消毒可见**：一条真痕迹可以整篇写进入库报告而审计一声不吭。
    **触发条件（终审给的，照实读）**：要咬到人需 ① 报告里真的出现 `/tmp/`、`/opt/`、`/var/` 这类仓库外路径，
    **且 ② 那台机器上仓库不在 `/home`（或 `/Users`、`/root`）之下**——在 Linux 上把仓库放在
    `/srv`、`/data`、`/mnt` 之类的位置即满足第二条；此时"审计说干净"推不出"报告干净"。
    **先量后改（顺序要紧）**：换成同一交替式后扫**全部入库证据**
    （`tests/papers/reports/**` + `tests/papers/recon/**` + 产出的 md + 词表 + docs）= **判定翻转 0 份**
    （旧谓词已红的那些仍是红，新的没有把任何一份从干净变红；**逐份清单与计数由那支探针当场打印**，
    不在这里抄成会随编辑过期的计数）。**那支探针 = `tests/papers/recon/audit-predicate-probe.py`**
    （复现：`PYTHONDONTWRITEBYTECODE=1 python tests/papers/recon/audit-predicate-probe.py`）。
    **2026-09-27 更正**：它原先拿 `report.ABSPATH_TRACE` 当"旧谓词"⇒ 统一之后是**自己跟自己比**、
    必然打印"翻转 0 份"，**复现不了**这个结论（教训 4.8 的形态）。现在**旧谓词已硬编码**
    （`git show fad9384^:tools/papers/report.py` 的那一行），探针自己断言两条谓词**逐字不同**。
    仓内那条 `/tmp/` 实例在
    `docs/superpowers/plans/2026-09-23-m6-corpus-pipeline-pilot.md:464`（`printf ... > /tmp/ctrl.md`），
    **没有任何 `path_audit` 调用会扫它**。⇒ 两处现在共用同一个 `_POSIX_ROOTS` 交替式；
    **`report.py` 是冻结件，本次只改那一行谓词**（并写清"同一语义必须用同一谓词"）。

14. **`verify_all.py` 的 `--limit` 跑里，【5b】读到的 C4 `visual_ok` 来自放行版 `c-report.txt`**
    （2026-09-27 登记，**只登记不改**）。机制：`stage_evidence()`（`verify_all.py:405-414`）
    返回的**恒是** `tests/papers/reports/<名>-report.txt`——它**不随 `--limit` 换落点**，
    而 `--limit` 跑里真正被这次运行更新的是 `reports-limited/c-report-limited-N.txt`。
    ⇒ 于是汇总里那个 `机读值 visual_ok = …` **可能给出与"此刻"相反的读数**
    （**全量跑读的是本次值、正确**；只有 `--limit` 跑会读到上一次全量跑留下的存档值）。
    **为什么不算缺陷**：那一行**显式自称"报告量（不是判据）"**、**不参与 `ok` / 退出码**
    （`verify_all.py:1082-1088` 逐字写着）；它只是把"目视项是不是判定过"摆到读者眼前。
    **红路不进放行**：放行判定用的是全量跑，那时读的就是本次值。

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


## H. M3 图表层 —— 已开工（2026-09-27）

**已完成**：`mcm-figure-choose`（M3 第一份，也是本套件第一份**可被机器复算**的规范型 skill）——
`.claude/skills/mcm-figure-choose/`：`SKILL.md`（82 行短契约）+ `references/{house-style.md（H1–H13，规范唯一权威）, provenance.md（45 条，每数带口径与复跑命令）, chart-types.md（9 个数据关系入口 + 题型索引 + 42 个图型名）}`。
配套机器在 `tests/skills/figure-choose/`：`check-figure-style.py`（**产物判据** F1 图宽比 / F2 彩色主色数 / F3a-d 图注形态，fail-closed）· `check-house-style.py`（**162 条守卫**）· `mutate-figure-style.py`（**53 条变异达预期全红**——2026-09-29 M3-plot Task 1 后由 46 增到 53；含 1 条"必须仍绿"的射程边界对照）· `check-spec-pointers.py`（**引用完整性全扫器**：判据**复用** `K2`/`K3` 不另写、射程 = 绘图家族、fail-closed 锚在**扫到的 skill 总数**）· `house-metrics.py`（**129 个**具名读数——2026-09-29 复核订正：此处原写「95 个」，实测 `python tests/skills/figure-choose/house-metrics.py --list | wc -l` = **129**）。
对照实验：**RED 基线 13 红 / 5 绿 ⇒ GREEN 0 红**（同场景、同判据、一字不改）。**逐轮任务级证据与复审结论在 `.superpowers/sdd/progress.md`（恢复图）。**

**Task 7 已交付（2026-09-29，提交 `1478463` → `6926e34` → `acfbc75`，两轮独立复审均 Approved）**：引用完整性检查器 = `check-spec-pointers.py`——三条规则里**只新增"全扫"这一层**，规则①（必须有指向 `references/house-style.md` 的指针）与规则②（不许复述规范数值）**复用** `check-house-style.py` 的 `K2`/`K3`、**不另写判据**（抄件会随检查器漂移）；配三份假 skill 防恒真 + `M43`–`M46`（**当时**合计 **46/46 红**；该总数随后由 M3-plot Task 1 增至 **53/53**，见 §H.1）。**射程 = 绘图家族**（`mcm-plot-*` / `mcm-table` / `mcm-schematic`）——原写法"任何 skill"实测**会在当时的 4/5 份 skill 上假红**（house-style.md 现抽 87 条禁止串，命中的 11 条**全是 `§7.2` 这类章节引用**，属口径偶合不是重述）。**当时读数（2026-09-29）**：`RESULT: PASS (无对象：扫到 5 个 skill，绘图家族 0 个)`——**无对象也打印普查**，故它既非恒真也非恒红。⚠️ 该检查器**"待 `mcm-plot-*` 出现时即生效"**（§C 已记）。**今日现状（2026-09-30，M3-plot Task 6 当场跑）**：`mcm-plot-python` 已建 ⇒ 普查 **扫到 6 个 skill、绘图家族 1 个**，末行 **`RESULT: PASS (绘图家族 1 个，K2/K3 全绿)`**（复跑命令见 §H.1.1）。

**两条结构性局限（已写在规范里，下游不许当结论引用）**：
① **H4 的连续色图闸门会把 72.81% 的图标为"条数不可引用"**——那是**闸门的性质**、不是"72.81% 的图有问题"；**H4 的证据基础因此只覆盖约 27% 语料**。
② **判断层实际射程只有单规则**（判者提示词只逐字内嵌了饼图那条）⇒ **判者通过 ≠ 规范得到背书**。

### H.1 M3 剩余

| # | 事项 | 说明 |
| :--- | :--- | :--- |
| 1 | **`mcm-plot-python`（建议先行）** | ✅ **已收口，含全分支终审**（Task 1–6 每个都走满「实现 → 独立复审 → 修复 → 聚焦复核」；**终审判 `Ready to merge: With fixes`**，2 Important + 7 Minor 全部处置，并有一条由**控制者亲跑**的定点复验）· **下一步 = `mcm-plot-matlab`**；本模块残留见 §H.2 |
| 2 | `mcm-plot-matlab` | 本机 R2025b `-batch` 可跑 |
| 3 | `mcm-plot-origin` | GUI，只给操作步骤；**导出物照样能过机械层**（F1/F2 都吃 PNG/PDF） |
| 4 | `mcm-table` | 三线表 LaTeX 代码 |
| 5 | `mcm-schematic` | **TikZ 源码**（载体已裁决，判据 = agent 能否看见产物） |
| 6 | **最终全分支审查 + Minor 批量清**（见 H.2） | 一次做掉 |

**M3 绘图实现层第一份 `mcm-plot-python`——在建（2026-09-29 开工）**

- **设计与计划（已入库）**：`docs/superpowers/specs/2026-09-29-m3-plot-python-design.md`（含 §9 系统 3.10.7 实测补充、§11 字体）· `docs/superpowers/plans/2026-09-29-m3-plot-python.md`（**6 个任务** + Global Constraints）。
- **用户已裁六条**：① 底座 = `matplotlib` + `SciencePlots`，style 取 **`science` + `no-latex` 叠加**并**自己覆盖 `savefig.bbox`**
  （实测 `science` 设 `text.usetex=True` 而本机 TeX Live 2026 **缺 `type1cm.sty`** ⇒ 保存即 `RuntimeError`；且它自带 `bbox='tight'`
  会把输出宽从 6.31 in 裁到 5.500 in ⇒ F1 只剩 **0.870**；覆盖回 `standard` 后 **1.000/1.000，PNG 与 PDF 逐位一致**）
  ② 样式数值走 **派生件 + 新鲜度守卫**（实测非 `SKILL.md` 载体今天**没有任何守卫会扫**）
  ③ `K3` 的 ASCII 标记集与中文臂 `SK_CN_TIER_RES` 对齐、**与家族落地同一次重生成**
  ④ `house-metrics.py` 的「95 个具名读数」订正为 **129**
  ⑤ **字体随 skill 入库**（`TeXGyreTermesX-{Regular,Italic,Bold,BoldItalic}.otf`；`newtx` README 原文
  "All text fonts are now based on TeXGyre Termes"，许可 **LPPL 1.3**，上游 Termes 是 **GFL** ⇒ **两套许可原文都须随字体入库**）
  ⑥ **加一条字体判据**：渲染后核"实际用的是入库那一份"，被移走即红——**今天 `F1`/`F2`/`F3` 一个字都不判字体，回退是完全静默的**。
- **环境动作**：`pip install --no-deps SciencePlots`（**2.2.2**）**已装**；**matplotlib 仍 3.10.7**（`--no-deps` 保证没被顺带升级）。
- **Task 1 已收口**（`8d56769`→`145e807`→`ddfe7fb`，修复 `5cfd47a`→`d0249b1`）：`K3` 主臂的 ASCII 阈值标记集与中文臂对齐
  （六个标记 · 两族值池），变异 **46 → 53**（含 1 条"必须仍绿"的射程边界对照）。**两轮独立复审**（Spec ✅ / Needs work
  → 修复 → 聚焦复核：**I-1 真收口**、M-1..M-4 全 ✅、无阻断）。
- **Task 2–5 已收口（2026-09-29，每个任务都「实现 → 独立复审 → 修复 → 聚焦复核」走满）**：
  - **Task 2 生成器与派生件 + 字体入库**（`2ff1291` → `bc01515` → 修复 `85cddc0`）：`gen-mcm-style.py`（重放式，11 条锚点**逐条恰命中 1 处**的 fail-closed 抽取）产出
    `assets/mcm.mplstyle` 与 `assets/mcmplot.py`；**底座 = `science` + `no-latex` 叠加 + 自己覆盖 `savefig.bbox`**（不覆盖则 6.31 in 被裁到 5.500 in、F1 掉到 0.870）；
    **字体随 skill 入库**（四份 `TeXGyreTermesX-*.otf` 字节级复制 + `PROVENANCE.md` 逐件 `git hash-object` + **GFL 与 LPPL 两套许可原文**，许可核到**文件级**即 OTF name 表 nameID 0 逐字声明）。
    复审抓到**唯一一条 Important**：两个 H12 锚点把规范端点 `0.8`/`1.0` 当**正则字面量手写**（违反非 `SKILL.md` 载体零手写数值）⇒ 已改成字符类，**派生件逐字节未变**。
  - **Task 3 判据：新鲜度守卫 + 字体守卫 + 变异**（`86278c2` → `f208f11` → `72ad5b8` → 修复 `0f77293` → `341c28d`）：
    ★ **计划原文那条验收照字面实现是恒真的**（生成器原地写 ⇒ 一份**过期**派生件被原地重跑就被改对，再比必然相等）⇒ 改为**两份参考都取在重跑之前**（`git show HEAD:<path>` + 检查前工作树字节），
    且实测**两臂互补、各有专属真红**（`M55` 改标记**之间**的常量只 `A2` 红；`M58` 改标记**之外** `A1` 与 `FON` 同时红 —— 实测 `RESULT: FAIL（A1:mcmplot.py,FON）`，见 `tests/skills/plot-python/plot-style-verify.txt:207`）；`M61` 机械证伪了计划那条字面形态。
    **字体守卫取「核产物本身」**（探针 PDF 的 `fitz` 实报 basefont ⊆ 入库集合、含罗马正体档），`M58` 拆掉 `addfont` ⇒ 渲染**照常成功**但实报 **`DejaVuSerif`** ⇒ 红（设计 §11.3「静默回退无人红」的实测复现）。
    驱动器的收尾自证**真的并进退出条件**（脏树 ⇒ `exit 1`），证据件**可从干净 HEAD 逐字节复跑**（复审在一次性克隆上真跑了脏/净两态，并把 223 行驱动器 stdout 与重跑输出 diff 为 0）。
  - **Task 4 `SKILL.md` + `references/workflow.md` + 家族落地最小同步**（`11728eb` → `b23e870` → 修复 `727bd5f` → `0a77319` → `a760592`）：
    `mcm-plot-python` **成为第一个绘图家族 skill**，`check-spec-pointers.py` 报 **`RESULT: PASS (绘图家族 1 个，K2/K3 全绿)`**；`mutate-figure-style.py` 在**真仓 6 skill / 家族 1 个**下仍 53/53、`exit 0`（侦察没跑过的那一步）。
    涟漪按**性质分档**处置（真·声明语义改写 / 字面转录按各自生成器重生成 / **历史快照手改 = 造伪不许手改**）。复审抓到三条「声明与事实不符」：两件散文写「一个数字都不出现（含中文数词形态）」而里面明明有 `一/两/三`（约束本体满足了，假的是那句声明）；
    `mutate-figure-style.py` 硬编码「真仓 0 个家族」而实测 1 个家族 2 条红 ⇒ **改成运行时现算**。**顺带冲销了 Task 2 留下的一处证据漂移**（Task 2 改了驱动器却没重生成那 5 份转录，Task 2 的复审漏了）。
  - **Task 5 RED/GREEN 对照与证据**（`bff9e73` → 修复 `d9a594a` → `dd24ce4`）：**RED 由三个新起、未见过规范的写手产出**（先例纪律：只给场景 brief 路径 + 输出目录），
    三场景 × 两载体**全判红**（R1 四条 `F1/F3a/F3b/F3c`；R2/R3 各五条，多一条 `F2`）；**GREEN 用模块三场景 × 两载体全 `PASS`**；同一把尺、同分母 `6.31`、两侧同源同数。
    复审**重判了全部 12 张图**，读数逐字重现；**亲眼看图逼出两条模块级缺口**（`science` 自带 `xtick.top/ytick.right` 而 `mcm.mplstyle` 只关 spines ⇒ **悬空刻度**；条描白边抬 PNG 的 F2）⇒ **只登记不修**（修了 GREEN 图会变、对照全废）。
  - **本模块内新起的两条耐久纪律**（下文 H.2 有对应待办）：① **计划里写死的行为口径，落地前必须实测复算**（计划那条新鲜度验收恒真；计划引的 F2 例子 `PNG=2 / PDF=0` **未带图名**——`science+no-latex` 图复现为 `2/0`、侦察朴素线图 `out-d11-red-loop.txt` 为 `2/1` ⇒ **F2 跨载体引用必须带图名**。★ 这句是**本任务新立**的常驻规矩（**不是订正过期句**），事实依据 = 设计件 `specs/2026-09-29-m3-plot-python-design.md:132` 记的 `science+no-latex` 图 **`2/0`** vs 侦察朴素线图 `out-d11-red-loop.txt` 的 **`2/1`** —— **两个数属于两张不同的图**（各是同一张图的 PNG/PDF 对数），不带图名就无从判真假。Task 6 见 §H.1.1）；
    ② **凡"声明"必须能被机械复算**——本模块 Task 2/3/4/5 **四个任务**的复审都各抓到至少一条「声明比事实大」，**没有一条是自己发现的**。
- **Task 6 真家族 ≥1 下的驱动器整跑与全库收口**（**已收口**，`50c7230` → `dc03dca` → 修复 `55da664` → 定点修复 `5831a8d`）：八个驱动器在收口态 HEAD 上**串行整跑全绿**（三件套：`RESULT: PASS` / `MUT: 53/53 达预期` / `MISMATCH 0/21`）；`docs/**` 过期散文订正；全库残留**逐件分类**并落 §H.1.1。
  ★ 计划的验收已按 H.2 `M3-plot-T6` 从「残留 = 0」（恒不可达）重写成**可判真假**的两条，并**分层**：机械层（命中集去重并集 == 表行数，**B 钥匙一条命令、A 钥匙四条**）+ 判断层（每行的类别与理由，须人读，已如实标层）。
  独立复审**独立重算**了双钥匙等式：A 四模式 12/12/7/0、**去重并集 22 == A 表 22 行**（逐行映射双向无剩余）；**B 命中 8 == B 表 8 行**。
  ★ **本任务内控制者出自己的错**：任务书断言计划那句「同一张图 `PNG=2 / PDF=0`」是错数 —— **实测证伪，那是两张不同的图**（设计件 `:132` 的 `science+no-latex` 图；侦察 `out-d11-red-loop.txt` 是朴素图 `2/1`）⇒ 设计件原读数**保留**，计划改成**带图名**的例子。
- **✅ 全分支终审已完成（2026-09-30，范围 `e98662d..0ce008d`，32 提交 / 92 文件 / +8525 −220，复审者 = 最强档）**：判 **`Ready to merge: With fixes`**，**0 Critical · 2 Important · 7 Minor**。
  复审**自己复现**了本模块的核心主张（不采信报告）：`PROVENANCE.md` 六个哈希与 `HEAD` 逐个相符；在 `mktemp -d` 里**重放生成器** ⇒ `mcm.mplstyle` 与 `mcmplot.py` **逐字节等于入库件**；双钥匙等式 22↔22 / 8↔8 逐行一对一；六份证据件的 BOUND blob 全等于 `HEAD`。
  - **I-1（真 bug）**：`K3` 主臂两条整数捕获未锚定 ⇒ 规范 `**不超过 1.20×**` 的**整数部 `1`** 混进上界值池 ⇒ 写 `上限 1` 的 skill 会假红。**已修**（只锚 `上限`/`不超过`；值池 `[1,3,4,12,17]`→`[3,4,12,17]`）。
  - **I-2（真·声明比事实大）**：`gen-pointer-verify.py` §5b 印着"现算，不是抄它的输出"而它**逐字抄了**检查器的 `FAMILY_RE` ⇒ **已修成 import 取用**（§5a 早已修过同型，这是那一次该带上的邻行）。
  - ★ **终审后追加抓到一条（两次都没自现）**：修复轮把 `plot-style-verify.txt` 在**该文件自己还脏着**的时候重生成 ⇒ 入库证据里印着 `exit=1`、脏树、`非零退出 1 条`，**从干净 HEAD 复现不出来**。
    **根因 = 节奏**：这类"证据件记录自身所在工作树状态"的生成器必须 **先干净 → 再捕获 → 再提交 → 再跑一次证不动点**。**已修（`0ce008d`），且由控制者亲跑生成器复验不动点**（`exit=0`、`git status` 空、`git diff` 空、blob 不变）。
    **新增口径（拟入 lessons）**：**"核了"的范围必须覆盖被改动物的语义** —— 控制者当轮核了范围/提交数/树干净/值池 delta，**独独没读那份重生成件的内容**，于是漏掉了这条。
- **余 0 个实现任务** ⇒ 本模块**已收口**。**下一步 = `mcm-plot-matlab`**（§H.1 第 2 项）。
  ⚠️ **另有两个独立后续任务**（**都不许塞进已完成的任务里**）：① **模块缺口修复**（`M3-plot-gap`：底座 `science` 自带 `xtick.top`/`ytick.right` 而 `mcm.mplstyle` 只关 spines ⇒ **悬空刻度**；条描白边抬高 PNG 的 `F2`）—— 修它必须重生成 Task 5 的 12 张对照证据；② **H.2 的 Minor 批量清**（含 `M3-plot-font` 的字体哈希臂、`M3-plot-M2` 的 `workflow.md` 无守卫缺口、**新记的 `M3-plot-T7b`** 等）。

### H.1.1 Task 6 全库残留**逐件分类表**（2026-09-30 收口 · 入库副本）

**为什么有这一节**：Task 6 报告落 `.superpowers/sdd/**`（**gitignored**）⇒ 分类表必须**在 docs 侧留一份**，否则只活在会话里。

**两把钥匙**：本表按**两组模式**各建一张子表，**每张各自声明自己的键与计数**——**两半各自一条命令可推翻**，谁都不靠另一张的计数。

**A 钥匙：四条残留模式（22 行）**

**四条残留模式**（均来自任务书 §2）：① 旧的 skill 普查数（"…个 skill"形态）② 绘图家族计数为 **0** 的形态 ③ 旧变异总数（分子分母同为 46 的形态）④ 作废的 52 形态。
**A 的两个数**：逐模式命中 = **12 / 12 / 7 / 0 行**（合计 31，含跨模式重复）；**去重后唯一 (文件:行) = 22 处** ⇒ **A 表 22 行**。

**复核命令**（一条命令一秒推翻本表）；**刻意用 `[ ]?` 拆分模式串，免得这一行自己变成新的命中**：
```bash
git grep -nE "扫到 5 个[ ]?skill" -- .     # 12 行
git grep -nE "绘图家族[ ]0[ ]个" -- .       # 12 行
git grep -nE "4[6]/4[6]" -- .              # 7 行
git grep -nE "5[2]/5[2]" -- .              # 0 行
```

| # | 位置 | 类别 | 今天读它不是假的，因为… | 复核命令 |
| :-- | :--- | :--- | :--- | :--- |
| 1 | `docs/mcm-suite-todo.md:471` | 历史（**已加时点**） | 原"真仓现状"句已改写成"**当时读数（2026-09-29）**"，同段补"**今日现状（2026-09-30）**"；段内旧变异总数标"**当时**合计"、`4/5 份` 标"**当时的**" | `sed -n '471p' docs/mcm-suite-todo.md` |
| 2 | `docs/superpowers/plans/2026-09-29-m3-plot-python.md:73` | 历史（计划内推理） | 说"只有 Task 4 才让它过期"——Task 4 确实这么做了，**该推理今天仍为真** | `sed -n '73p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| 3 | 同上 `:194` | 历史（**已执行**的硬要求原文） | Task 4 的指令（普查数 5 → 6）**已执行**（今天真仓正是 6 个）| `sed -n '194p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| 4 | 同上 `:228` | 历史（Task 6 硬要求原文） | "改成与 Task 1 之后的总数一致"——本任务**已执行** | `sed -n '228p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| 5 | 同上 `:232` | **判据模式串**（本任务新写） | 是重写后验收条款里**列出要搜的字面量**，非述说现状 | `sed -n '232,236p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| 6 | 同上 `:236` | 判据模式串（本任务新写） | 同上（机械层复核命令里引的模式） | `sed -n '232,236p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| 7 | `docs/superpowers/specs/2026-09-29-m3-plot-python-design.md:144` | 设计期**侦察记录** | 以"侦察逐条 grep 取证"起头 ⇒ 是**那天的发现记录** | `sed -n '140,145p' docs/superpowers/specs/2026-09-29-m3-plot-python-design.md` |
| 8 | 同上 `:150` | 设计期**涟漪记录** | "总数现算、散文要订正"——已被 Task 1（46→53）与本任务执行 | `sed -n '150p' docs/superpowers/specs/2026-09-29-m3-plot-python-design.md` |
| 9 | `tests/m3-plot-recon/out-m43-m46-today.txt:4` | **逐字 stdout 捕获** | 探针当天的 stdout 原文、自带年代指纹；见 `tests/m3-plot-recon/README.md` | `sed -n '4p' tests/m3-plot-recon/out-m43-m46-today.txt` |
| 10 | 同上 `:18` | 逐字捕获 | 同 #9：那是**那天**的变异合计（`MUT: … 红（合计）`），手改 = 造伪 | `sed -n '18p' tests/m3-plot-recon/out-m43-m46-today.txt` |
| 11 | `tests/m3-plot-recon/out-e15-m43-prealchor.txt:17` | 逐字捕获 | 同 #9：探针当天 stdout 原文 | `sed -n '17p' tests/m3-plot-recon/out-e15-m43-prealchor.txt` |
| 12 | `tests/skills/figure-choose/mutate-figure-style.py:956` | **历史叙述** | 明写"那是**真仓那天的读数**" | `sed -n '956p' tests/skills/figure-choose/mutate-figure-style.py` |
| 13 | `tests/skills/figure-choose/pointer-verify.txt:76` | **fixture 读数** | 普查对象是 `fixtures/fake-skills/*`（**假** skill 根），**不是真仓** | `sed -n '76p;94p;314p' tests/skills/figure-choose/pointer-verify.txt` |
| 14 | 同上 `:94` | fixture 读数 | 同上 | 同上 |
| 15 | 同上 `:314` | fixture 读数 | 同上（fixture 普查）| 同上 |
| 16 | 同上 `:116` | **空目录分支**读数 | 扫的是 `fixtures/*/SKILL.md`（该行读数 **0**），非真仓 | `sed -n '116p;120p' tests/skills/figure-choose/pointer-verify.txt` |
| 17 | 同上 `:120` | 空目录分支读数 | 同上 | 同上 |
| 18 | `tests/skills/figure-choose/check-spec-pointers.py:42` | **代码**（docstring 通用例）| 用占位 `N`，讲"家族还没建出来"时的形态 | `sed -n '42,44p' tests/skills/figure-choose/check-spec-pointers.py` |
| 19 | 同上 `:43` | 代码（docstring 通用例）| 同上 | 同上 |
| 20 | 同上 `:166` | **代码**（无家族分支）| `elif not fam:` 分支，家族 ≥1 后**不执行** | `sed -n '160,167p' tests/skills/figure-choose/check-spec-pointers.py` |
| 21 | `docs/mcm-suite-todo.md` §H.2 的 **`M3-plot-T4`** 行（**定位见本行复核命令**，不写死行号）| 已处置（**复核命令自身**）| 旧总数只出现在本任务写的复核命令里；待办里的行号已订正 `:67` → `:75` | `git grep -n "^| M3-plot-T4" docs/mcm-suite-todo.md` |
| 22 | 同上 §H.2 的 **`M3-plot-N2`** 行（**定位见本行复核命令**，不写死行号）| 已处置（**类别标签**）| "3 处旧总数已分档落定"是**待办台账文字** | `git grep -n "^| M3-plot-N2" docs/mcm-suite-todo.md` |

**B 钥匙：任务书 §3.6 的"skill 尚未建成"一类（8 行；7 行属 skill 尚未建成，1 行属同串他义——见 B6）**

**为什么单列 B**：这一类条目**不含** A 的四条模式串 ⇒ **A 表一行都不覆盖它**；任务书 §3.6 明令它**要在分类表里有行**
（复审点名的三处：`plans/2026-09-27-m3-figure-choose.md:160` · `plans/2026-09-29-m3-plot-python.md:184` · `specs/2026-09-29-m3-plot-python-design.md:148`）。
模式串同样用括号拆分，免得本行自己变成新的命中：

```bash
git grep -nE "还不存[在]" -- .     # 8 行
```

**B 的两个数**：模式命中 **8 行**；去重后唯一 (文件:行) **8 处** ⇒ **B 表 8 行**；**二者相等**（本模式无跨行重复）。

| # | 位置 | 类别 | 今天读它不是假的，因为… | 复核命令 |
| :-- | :--- | :--- | :--- | :--- |
| B1 | `docs/mcm-suite-lessons.md:259` | 历史**事件**记录 | §7.4 记的是过去那轮派发里写过的断言（后经实测证伪）——是**事件叙述**，非述说现状 | `sed -n '259p' docs/mcm-suite-lessons.md` |
| B2 | `docs/superpowers/plans/2026-09-27-m3-figure-choose.md:160` | 计划的**历史步骤** | 那是 M3-figure-choose 计划里的 TDD 步骤（预期报 `FileNotFoundError`）——**早已执行** | `sed -n '160p' docs/superpowers/plans/2026-09-27-m3-figure-choose.md` |
| B3 | `docs/superpowers/plans/2026-09-29-m3-plot-python.md:184` | 历史（Task 4 硬要求原文） | Task 4 的指令：点名要改 `mcm-figure-choose/SKILL.md:70` 那句过期散文——**已执行**（今天那句已不存在） | `sed -n '184p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| B4 | 同上 `:233` | **判据模式串**（本任务重写） | 验收条款里**列出要搜的字面量**，非述说现状 | `sed -n '233p' docs/superpowers/plans/2026-09-29-m3-plot-python.md` |
| B5 | `docs/superpowers/specs/2026-09-29-m3-plot-python-design.md:148` | 设计期**侦察记录** | 记的是设计期"`K6` 抓不到那行"的发现——是**那天的记录** | `sed -n '148p' docs/superpowers/specs/2026-09-29-m3-plot-python-design.md` |
| B6 | `tests/skills/abs-cases/red/red-P1.md:127` | M2 摘要 **RED 语料** | 讲的是**摘要里那一格数字**没有——与 skill 计数无关（同模式串的另一义） | `sed -n '127p' tests/skills/abs-cases/red/red-P1.md` |
| B7 | `tests/skills/figure-choose/red/make-evidence.py:51` | **生成器引文** | 引的是任务书当年的断言（该断言经实测为假）——是**历史** | `sed -n '51p' tests/skills/figure-choose/red/make-evidence.py` |
| B8 | `tests/skills/figure-choose/red/red-evidence.md:35` | 生成证据件**转录** | 同 B7（该生成器产出的转录，内容一致） | `sed -n '35p' tests/skills/figure-choose/red/red-evidence.md` |

**近邻不收（说理）**：`docs/mcm-suite-todo.md` 的 **T7-5** 行（`git grep -n "^| T7-5" docs/mcm-suite-todo.md` 定位）含的是「**尚**不存在」——讲的是**第二个提交**尚不存在（对一条测量声明的记述），与 B 钥匙那一类（**skill 尚未建成**）**不同类** ⇒ **不收**（它也不在 B 钥匙的命中集里）。

**本任务归零的两处**：① `tests/m3-plot-recon/e15_m43_preanchor.py:75` 的**裸总数**——走**乙**（去掉裸总数、改不写死计数的措辞）；② ④ 那条模式（作废的 52）的**唯一一处**（原 M3-plot-N1 待办行）已随该行改写消失 ⇒ 全库 **0 行**（见上表 `5[2]/5[2]` 那条命令）。

**现取值（非残留）**：变异合计的**当前**数全库 **10 处**——`docs/mcm-suite-todo.md:{471,515,523}` 的 **3 处** + **6 份入库验证件里的 7 处**（`chart-types-verify.txt:436` · `figure-style-baseline.txt:438,604`（**同一份件贡献 2 处**）· `house-style-verify.txt:442` · `pointer-verify.txt:289` · `skill-verify.txt:455` · `plot-style-verify.txt:669`）= **3 + 7 = 10 处**。**这条计数有自己的命令**（不属于 A 的四条模式，故 A/B 两把钥匙都不含它）：`git grep -nE "5[3]/5[3]" -- . | wc -l` → **10**。**7 处全部等于当场跑出的总数**：`python tests/skills/figure-choose/mutate-figure-style.py | tail -1`。

### H.2 待批量清的 Minor（同批文件，适合一次做掉）

| ID | 位置 | 一句话 |
| :--- | :--- | :--- |
| T2-M1 | `red/red-evidence.md:829` + `red/make-evidence.py:786` | `<<ROUND2>>` **残留占位符**（机制只接了一半；对照 `<<CAPTIONS>>` 有 replace+assert） |
| T3-R1 | `check-house-style.py:274-275` | 推论"写不进去的新整数一律 FAIL"在**豁免窗口内不成立** ⇒ 改成"不在豁免窗口内的…" |
| T3-R2 | `.superpowers/sdd/task-m3-t3-report.md:48`（gitignored） | **仍留假陈述**"57.2% 未能复现…48.79%"（受控文件已清、仓外件没清） |
| T3-R3 | `house-style.md:134` | "本样本 72.81% 的图『条数不可引用』"把**闸门性质**写成了**图的属性** |
| T4-m1/m2 | `chart-types.md` §0.2 | 补两句：参照分布数**必须与 `H<n>` 引用同行**；`S5` **只判漂/归属**、池子 = 该 H 条目里出现过的**所有**小数 |
| T5-1 | `check-house-style.py:529` | 中文数词臂的**射程写法**与实测不符（实测边界更宽）；可选加阈值锚定臂（已验证 0 误伤） |
| T5-2 | `check-house-style.py:620` | `_k5` docstring 说"四条"、下列的是 ①–⑤ **五条** |
| T6-1 | `red/red-evidence.md:527/:642` | 两条**探针**的 F3b 打印词数按新口径应为 3/2（**判词仍 PASS、结论不变**，显示性过期） |
| T6-4 | `green-evidence.md` §8 · `check-figure-style.py` D7 | **两处跨任务涟漪的说明只活在 gitignored 报告里** ⇒ 仓内补 2 行（否则复算者会以为证据件造假）——**恰好重演了本轮自己识破的毛病**（"解释留在 `.superpowers/` 就走不掉"） |
| T6-5 | 提交 `35133ec` 的信息 | 只写了 F3b 收敛 + 判断层列 + 6 Minor，**没提** Task 1 生成器/基线重发与三份证据件重生成（`--amend` 把跨任务活并进一个提交，信息留白） |
| T6-6 | `.superpowers/sdd/task-m3-t6-report.md` | 报告上半部分（§0/§2/§3）仍是修复前的数（3 红 / 10 格），与 §R0（0 红 / 13）并存 ⇒ 只看 §0 会拿到过期结论 |
| T7-1 | `mutate-figure-style.py:956-957`（`m46_ptr`） | 只断言 `rc != 0` **且无** `RESULT: PASS` ⇒ 无关崩溃也算过；建议改成要求 `FAIL  DIR` / `FAIL  CENSUS` |
| T7-2 | `check-spec-pointers.py:118` | `_load()` 外无 `try` ⇒ `--checker` 指向坏文件时 traceback 且**不打印 `RESULT:`**，破了"末行恒为 RESULT"的契约（**仍非零退出 = fail-closed**） |
| T7-3 | `gen-pointer-verify.py:47` | ✅ **已处置（2026-09-30，终审修复轮）**：`FAMILY_RE` 是**抄件不是派生**而 §5b 标题写"现算，不是抄它的输出" —— **终审把它列为 I-2 并修成 import 取检查器对象**（与 §5a 同法），`pointer-verify.txt` 已重生成。★ 它是**那一次该带上的邻行**（§5a 早已修过同型） |
| T7-4 | `gen-pointer-verify.py` §5a | 只**披露**「本器自己定义的 `_k2`/`_k3`：零个」却不因它非零而红 ⇒ 两行可硬化成 `raise` |
| T7-5 | `figure-style-baseline.txt:923-925` | 断言"另起提交只动本文件"是**声明而非测量**（16 条比对取自提交①，②尚不存在）⇒ 改成可核写法（`git show --stat <hash>`） |
| T7-6 | `.superpowers/sdd/task-m3-t7-report.md:528`（gitignored） | 记 73379 B「phase 2 后」，提交件实为 73594 B ⇒ §8.5 的改写发生在 phase 2 **之后**，叙述该说清（同 T6-6 那一型） |
| T7-7 | `mutate-figure-style.py`（`M45`） | 在 `__pycache__/` 留 `.pyc`（已核 `.gitignore:9` ⇒ **不脏树**）⇒ `finally` 里加 `cache_from_source(...).unlink(missing_ok=True)` |
| T7-8 | 仪器探针 | 只打 `K3` 且以"空串"为代理 ⇒ `SK_POINTER` 坏在真仓**不可见**（0 家族 ⇒ 逐份循环不跑）；对称加一条 `K2@空串` 探针 |
| T7-9 | `figure-style-baseline.txt` §8 | 记的自己那行字节数**天生追不上自己**（phase 1 跑时文件还是重放前版本；基线 `1478463` 上同一现象，**非本轮引入**） |
| — | **任务书侧待订正 + 通则候选** | Task 7 两份任务书把假 skill 写成 `fake-ok`/`fake-nopointer`/`fake-restate`，与同一份文件里刚定的"射程 = 绘图家族"**互相矛盾**（`fake-*` 不在射程内 ⇒ M43 不可能红）——实现者当场按家族前缀改名（**角色与内容未改**），复审判"成立且被逼"。**未造成返工，但属派发缺陷。** ⇒ **通则候选：改一条差异后必须回头扫同一份任务书里与它耦合的其他行**（与通则 10 同族，都是"派发前的自核"）。**→ 用户 2026-09-29 批准，已入 `mcm-suite-lessons.md` §一 通则 11。** |
| M3-plot-T4 | `tests/m3-plot-recon/out-m43-m46-today.txt:18` · `out-e15-m43-prealchor.txt:17` · `e15_m43_preanchor.py:75` | **已处置（2026-09-30，Task 6）**：① `out-m43-m46-today.txt:18` 与 `out-e15-m43-prealchor.txt:17` 是**逐字 stdout 捕获、自带年代指纹 ⇒ 手改 = 造伪**，依同批新增的 `tests/m3-plot-recon/README.md` 判为**不许手改**（差异只能靠"重跑 `*.py` 并同批重新捕获"更新）；② `e15_m43_preanchor.py` 那处裸总数走**乙**（去掉裸总数、改不写死计数的措辞）；★ **行号订正**：本条原先写的 `:67` **实测是 `:75`**（`git grep -n "46/46" tests/m3-plot-recon/e15_m43_preanchor.py`）|
| M3-plot-N1 | `.superpowers/sdd/task-m3-plot-t1-report.md`（gitignored） | **已处置（Task 6 复核）**：那份报告只活在 **gitignore 的 `.superpowers/sdd/**`** 里、**不入库** ⇒ 依 §3.5 规则**不改仓内任何件**；要清须在被忽略件自身订正，**不在本任务射程** |
| M3-plot-N2 | 同上 §8.5 | **已处置（Task 6）**：3 处 `46/46` 已分档落定——2 处**逐字 stdout 捕获**（判"不许手改"，见 `tests/m3-plot-recon/README.md`）、1 处**源码字面量**（去裸总数，见 M3-plot-T4）|
| — | **通则候选（2026-09-29 新增）** | **凡"按槽位默认落盘"的工具，调用时必须显式给输出路径。** 实测：`task-brief` 漏第三个参数时会默认写到 `.superpowers/sdd/task-<N>-brief.md`，**覆盖了 M6 试点同名旧件**（9138 B；该目录被 gitignore ⇒ **git 无从恢复**，只能从受版本控制的计划重建并标注"重建件"）；同型的还有"任务书把报告落点写成被旧件占用的槽位"（那次实现者识别出来并让路了）。**待用户批准后入 `lessons`。** |
| — | **通则候选（2026-09-30 新增，两条同族）** | ① **拿两个数比对（判"不符/有出入/是错的"）之前，必须先确认它们说的是同一个对象。** 实测：任务书断言计划那句「同一张图 `PNG=2 / PDF=0`」是**错数**，依据是侦察实测 `2/1` —— 而那**是两张不同的图**（设计件的 `science+no-latex` 图 vs 侦察的朴素图）。**根因**：台账条目当初就没核过两个数说的是不是同一张图，控制者**照抄了台账**并升级成一条"订正指令"。 ② **"核了"的范围必须覆盖被改动物的语义。** 实测：控制者自核了范围/提交数/树干净/值池 delta，**独独没读那份重生成件的内容** ⇒ 漏掉了"入库证据自报 `exit=1` 与脏树、且从干净 HEAD 复现不出来"这条 Important。两条与既有「计划里写死的口径落地前必须实测复算」同族，都属"**核了，但核的不是那件事**"。**待用户批准后入 `lessons`。** |

| M3-plot-T6 | `docs/superpowers/plans/2026-09-29-m3-plot-python.md`（原 `:227`） | **已处置（2026-09-30，Task 6）**：那条「全库 `git grep` 残留 = **0**」已按新口径重写成两条**可被判真假**的判据（①不得残留述说现状的过期陈述 ②其余字面量逐件登记，行数与命中数对得上）；逐件分类表见 §H.1.1 |
| M3-plot-T6b | 同上 `:101` | **已处置（2026-09-30，Task 6）**：原写的失效引用 `:821-824`（实测是 `_run`/`_skills_tree` 的代码）已换成**可核落点**——`mutate-figure-style.py:145-146`（`M43` 顺延）/`:172-173`（`M47` 顺延）/`:1134-1135`（`M53` 顺延），更早同型见 `:95`/`:441-443`/`:634`。★ 本条原先列的 `:1107` 是 `except AssertionError`（**对不上**），一并订正 |
| M3-plot-T6c | 同上（Task 5 硬要求 3） | **已处置且已实测复核（2026-09-30，Task 6）**：原「同一张图 PNG=2 / **PDF=0**」**未带图名** ⇒ 已改成带图名的例子（`out-d11-red-loop.txt` 的朴素线图 **PNG=2 / PDF=1**，Task 6 当场复跑证实）；**未**改口径/判据/换图。★ 复核中发现：`PNG=2 / PDF=0` 本身对**另一张图**为真（`science+no-latex` 三线图，Task 6 复现），故设计件 `2026-09-29-m3-plot-python-design.md:132` 的 `2/0` **保持不变** —— 详见 §H.1.1 与 Task 6 报告 |
| M3-plot-font | `tests/skills/plot-python/check-style-freshness.py:42-48` · `.claude/skills/mcm-plot-python/assets/fonts/PROVENANCE.md:11-18` | **字体字节完整性无判据归属**：全 `tests/` **无任何判据**把 `.otf` 的 blob 与 `PROVENANCE.md` 对账 ⇒ Global Constraint 10 括注「改了哈希就变，判据会红」**目前无人兑现**（射程段已如实声明该缺口）。`PROVENANCE.md` 已有逐件 blob ⇒ 补一条哈希臂成本很低。**未排** |
| M3-plot-gap | `.claude/skills/mcm-plot-python/assets/mcmplot.py`（『已知缺口（不许藏）』段） | **两条模块级缺口已登记、已指派 owner，但本身未修**：① 底座 `science` 自带 `xtick.top: True / ytick.right: True`，而 `mcm.mplstyle` 只关 `axes.spines.top/right` ⇒ **悬空刻度**；② **条描白边把 PNG 的 F2 抬高一档**。**修它必须重生成 Task 5 的对照证据** ⇒ 需要一个**独立的后续修复任务**，**别塞进 Task 6** |
| M3-plot-M1 | `tests/skills/plot-python/check-style-freshness.py:261` | 行内注释仍写 `# 还原：本器非侵入` **无限定**，而 `:31-32` 已声明非侵入是**有条件的**（非原子）⇒ 同一处措辞的最后一件 |
| M3-plot-M2 | `.claude/skills/mcm-plot-python/references/workflow.md` | 该件零数字是**纪律不是判据保证**（`K1`–`K8` 只看 `SKILL.md`；`census()` 只 `glob("*/SKILL.md")`）⇒ 将来往里写规范数值**不会有任何东西变红**。缺口既有、已自我披露（报告 §6.6/§9.8.3） |
| M3-plot-M3 | `tests/skills/figure-choose/figure-style-baseline.txt:939-940` | 样板文字说末哈希登记在 `task-m3-t7-report.md`/`task-m3-t1-report.md`，本轮实际登记在 `task-m3-plot-t4-report.md`（**既有生成文本、不在任何本轮 diff、射程外**） |
| M3-plot-M4 | `tests/skills/figure-choose/check-house-style.py`（`GUARDS` 的 `G-H12-scale-lo/hi`） | 守卫正则**手写了**规范端点 `1\.0` / `0\.8` —— 与 Task 2 那条 Important **同形**（那条已修成字符类）。**终审已裁：非合并阻断**（runner 对"守卫不命中"是 **fail-closed** ⇒ 不是健全性漏洞），但**应与模块自己的裁断保持一致**，批量清时一并改 |
| **M3-plot-T7b**（新，终审残留） | `tests/skills/figure-choose/check-house-style.py` 的 `SK_CN_TIER_RES`（`≥` / `下限` 两条） | **同一 bug 的**下半臂**未修**：`≥` / `下限` 与 `上限` / `不超过` **同形未锚** ⇒ `≥0.4%`（`house-style.md:115`）/`≥0.3%`（`:116,120,150`）/「**下限 0.80**」（`:49`）的**整数部 `0`** 仍在下界值池里 ⇒ 写 `≥0` / `下限 0` 的 skill 会**假红**。★ **终审已复核确认**：`house-style.md` 里**没有真正的整数 0 阈值**（真下界整数阈值是 `2`/`7`/`20`/`100`），且 **`M50` 并不依赖 `0`**（其 `TIER_GREEN` 三例是 `主色 4 个`/`下限 4`/`< 25 词`，只断言 `K3` 仍绿）⇒ 锚定下半臂**不会破 `M50`**。**这是一行即可修**（加 `(?![\d.])` + 把 `0` 从 `_k3` docstring 的枚举句里去掉），**不是**需要"规范值裁决"的硬问题。 ⚠️ 需同批重生成绑定 `check-house-style.py` blob 的证据件 |
| **M3-plot-RED（新，终审 Minor）** | `docs/superpowers/specs/2026-09-29-m3-plot-python-design.md` §5（约 `:122-123`） | 设计件说 RED = "一份**朴素 matplotlib** 脚本…判红 **4 条**（F1 1.426 · F3a · F3b 21 词 · F3c）"，而**交付的 RED 是三张写手图**（F1 1.213/1.385/1.514、168/208/237 词）。`1.426/21 词` 那对**是真的**（属**侦察**那张朴素图 `out-d11-red-loop.txt`）⇒ 该条**未标 superseded**，读起来像交付物的描述。**归 H.2 批量清** |
| **M3-plot-INIT（新，终审 Minor）** | `tests/skills/plot-python/make-evidence.py:276` | 把 **"初版"读数**（"G3 初版 PNG=5 / PDF=3；G1 初版加 constrained 后 PNG=4/PDF=3"）**硬编码进生成的证据件** `red-green-evidence.md` §4 ⇒ 那几条**无法从入库树复导**。同段的**当场探针是真的**。⇒ 应**标为历史叙述**或删掉。**归 H.2 批量清** |

### H.3 M2 欠账

- **写作纪律的去重**：`mcm-abstract` 的 **Q7/Q8/Q9/Q12 四格改成指针**（**要改已交付的冻结 skill** ⇒ 需单独走一遍流程）。
- **`mcm-section-writer`**（薄 skill：只在"该写的时刻"被触发 + 交付那份权威纪律）。
- 写作纪律文档**残余 R1–R12** 里仍该动的；其中 **R6：`grep -rn "mcm-writing-discipline" .claude/` = 0 ⇒ "唯一权威"至今仍只是约定**。

### H.4 更早的待裁决

- **Task 9 的 UMAP 题号口径 recon**（用户已裁"先 recon 定口径"）。
- `.gitattributes` 自身不在 `-text` 规则内（全新检出一致性上仍会分叉，不影响任何判据）。
