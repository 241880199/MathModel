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
2. 是否把 `mcm-schematic` 的输出载体从 **TikZ / Mermaid** 改为 **draw.io**？
   （~~改的理由：用户本机无 TeX~~ —— **该理由已失效**，本机 2026-09-24 已装 TeX。**但 draw.io 另两条理由仍成立**：
   全程**不需编译**、产出**可编辑矢量**。故这一问**仍待裁决**，只是论据换成这两条。）

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
