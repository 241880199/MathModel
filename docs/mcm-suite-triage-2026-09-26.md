# M6 整分支终审：待分类清单的处置结论（2026-09-26）

> **这份文件为什么存在**：终审用的待分类清单原先只在 **`.superpowers/sdd/final-review-triage.md`**
> ——那是 **gitignored** 目录。按本项目规矩「残余一律落库区，放 `.superpowers/` 等于丢失」，
> 那份清单的**结论**必须搬进库区。本文件就是它的落点（**只此一处**）。
>
> **来源与口径**：条目标题与判定来自**终审**（判定分四类：**合并前必修 / 能便宜修就修 / 仅登记 /
> 不在本轮范围**），由 controller 转述给本轮的修复者。**终审报告原文没有落在盘上**
> （全仓 grep「合并前必修」只命中 `final-review-triage.md` 与终审自己的探针 `build/finalreview/probe_scan.py`）
> ⇒ 下表是**转述的结论 + 逐条指向仓内登记位置**，不是原文逐字。凡本文写"**实测**"的，
> 都附**可复现命令**与**当场量出的数**；**凡实测与转述口径不符，本文以实测为准并写明**（见 §4.2、§4.3）。
>
> **范围**：分支 `feat/m6-corpus-pipeline`。**注意 merge-base 不存在**——本分支与 `main` 无共同祖先
> （`main` 是快照），故终审范围按「M6 起点 `f275e91` 之后的提交」界定
> （终审当日实测：85 提交 / 90 文件 / +42672 行——**本轮的两个修复提交不在其中**，
> 要现值就重跑 `git diff --stat f275e91^ HEAD -- tools/ tests/ docs/ .gitattributes`）。

---

## 1. 总表：每条 → 判定 → 理由 → 仓内登记位置

| 条目（终审编号） | 判 | 理由（终审给的） | 仓内登记位置 |
| :--- | :--- | :--- | :--- |
| **I-5** `pilot-summary.txt` 会在"自己宣告未放行"的产物上写"可放行"（C4 目视闸门缺档时） | **合并前必修** | 同一件事两个力道，读者会把「可放行」读成覆盖了目视项 | **已修**：`verify_all.py` 【5】⑦ + 【5b】；§2 |
| **I-1** 四类实质内容只在 gitignored 目录里 | **合并前必修** | 「放那里等于丢失」 | **已修**：本文件 + `docs/mcm-suite-todo.md` §D 第 6/12/13 条；§2 |
| I-3 `report.py` 的 `ABSPATH_TRACE` 与 `_ABS_POSIX` 谓词不一致 | **能便宜修就修**（先量后改） | 只改一行谓词；量过判定翻转 0 份 | **已修**：`tools/papers/report.py`；`mcm-suite-todo.md` §D 第 13 条 |
| M-9 放行证据 `RELEASE` 自己无判据护栏 | **能便宜修就修** | 加一行 `git_tracked(RELEASE)` 即堵住 | **已修**：`verify_all.check_release_tracked`；红证据 FX-5 |
| M-1 `CRIT_RX` 支 1 锚行首 ⇒ **缩进的** `名=FAIL` 两支都不收 | **能便宜修就修** | 加一支允许前导空白；实测不产生假红 | **已修**：`verify_all.CRIT_RX`；红证据 FX-3 |
| M-2 `hits[0]` 取"先出现的以标签开头的行"（方向 fail-open） | **能便宜修就修** | 改成取该标签下**全部行并取最严** | **已修**：`verify_all.check_determinism_counts`；红证据 FX-4 |
| RT-M2 / RT-M3 的证据与编号纠葛（`M-7` 幻影红路） | **仅登记** | 补变异要连带重出 476 KB/412 KB 两份证据文件——代价不对等 | §4.3（**含一条与终审口径不符的实测**） |
| M-3 `verify_map.py:730-733` 的 `py_bad`、M-4 `verify_ids.py:569-577` 的 `path_bad` | **仅登记**（两脚本冻结 ⇒ 只更正登记文字） | 见 §4.2：**实测与终审口径不符**，以实测为准 | §4.2 + `tests/papers/recon/ids-recon.txt` 的 R3 行更正 |
| "从未被证明会红"的判据清单（含 `verify_io/wm` 的 `CRIT_RX` 覆盖、`verify_wm` §4/§6/§7/§8、`MAX_SECONDS` 与 `all-timing` 落点守卫） | **仅登记** | 补变异成本高、且多数红路在结构上难以构造 | §4.1（表） |
| I-4 9 个驱动器的清单与证据体量 | **仅登记**（不实现"驱动器入库"这个大工程） | 驱动器入库要跨目录搬迁 + 重出全部证据 | §4.4 |
| 探针覆写风险：`index.py` 的守卫可被**显式 `out_dir=io.DERIVED`** 绕过 | **仅登记**（不改 `index.py`——另一次解冻） | 终审自己踩过（三份产物被覆写，已还原） | §4.5 |
| D 项可用性缺口：`INDEX.md` 无覆盖边界块 · `PROVENANCE.md` 缺"不能让读者推出的结论" | **仅登记 + 待裁决**（**不动产物**） | 改这两份会打红 `verify_map` 的 M-1（`PROVENANCE.md` 的"逐字节不变"是判据链的一环） | §4.6 |
| `reports/README.md` 加一句 `all-timing.txt` 的说明 | **能便宜修就修** | 一句话，避免被当成 bug | **已修**：`tests/papers/reports/README.md` |
| `.gitattributes` 加 `-text`（`tools/papers/**` + `tests/papers/**`） | **用户已裁决：加，窄范围** | 实测只 2 个分叉文件、`git checkout --` 收敛后 blob 零变化 | **已做**：`.gitattributes`；`mcm-suite-todo.md` §D ⑤ 的 2026-09-26 更新 |
| `verify_io.py` / `verify_wm.py` 的两条纪律违例 | **用户已裁决：修** | 解冻两个脚本 | **已修**：`mcm-suite-todo.md` §D 第 12 条 |
| Task 9（UMAP 五卷 / 扩到 201 份） | **不在本轮范围** | 被题号口径卡着（`problem_of` 77/201 取不到） | `.superpowers/sdd/task-9-recon-brief.md`；`mcm-suite-todo.md` §A 第 9 行 |
| `INDEX.md` / `PROVENANCE.md` 的可用性补丁 · `tools/papers/index.py` 的守卫加严 | **不在本轮范围**（要用户点头的另一次解冻） | 同上两条 | §4.6 · §4.5 |

---

## 2. "合并前必修"两条的现状

### I-5（已修）：目视项被"可放行"顺带读成已判定

**事实链（终审给的，本轮逐条复核过）**：`verify_c.py:801` 的 `return not bad` **不含** `visual_ok`；
C4 人工目视闸门缺档时 `c-report.txt` 会写 `C4 人工目视闸门: FAIL（未判定）` 与 `发布放行: **未放行**`；
而汇总的 `CRIT_RX` **两式都匹配不到**那两行（一支要求 `名=状态`、另一支要求以 `: True|False` 收尾）。
**同一个名字两个力道**：`wm-visual-confirm.txt` 在 `verify_wm.py` 第 8 节是**硬判据**（缺了判该脚本 FAIL），
`c4-visual-confirm.txt` 在 `verify_c.py` **不是**；两份文件的自述却都写"缺了则判 FAIL"。

**修法（最小形态，没改任何冻结脚本）**：`verify_all.py` 的放行条件表加了 ⑦ 与 **【5b】范围声明**——
**两项人工目视闸门（C4 与 Task-2 的）不在本汇总的判定范围内**；其机读值见各产物；
C4 的 `机读值 visual_ok=` 作为**报告量（非判据）**打进汇总（**并登记它不构成判据、不参与 ok/退出码**）；
`crit_grep_idiom` 的口径行旁写明**该行是报告量**。状态行也加了「两项人工目视闸门不在本判定范围内
（见【5b】——「可放行」不覆盖 C4 目视项）」。

**实测（B-1 的验收口）**：备份 `c4-visual-confirm.txt` → 清空 → 全量跑 `verify_c.py`
（`c-report.txt` 的 `RESULT: PASS` 与「未判定 / **未放行**」同时存在 ⇒ 事实链成立）→ 跑
`verify_all.py --limit 1` ⇒ 汇总里**出现**范围声明，且 C4 报告量显示 `visual_ok = False`；
**测完逐字节还原**：`c4-visual-confirm.txt` blob `d6e0794a2474c8bdf337c58cc196ebcb104e7430`
（还原前后相同）、`c-report.txt` 重跑后 blob `b07173b0263208be7d46a1a08a5642db084180ae`（与测前相同）。

### I-1（已修）：四类实质内容只在 gitignored 目录里

四类 = 终审待分类清单本身、Task 5 的 8 条残余（**上一轮已搬进 `tests/papers/recon/formula-recon.txt`**，
commit `9431497`）、`.superpowers/sdd/` 里的驱动器/探针产物、以及本轮的处置结论。
**本轮**：处置结论 → **本文件**；§D 的两条新增（12/13）→ `docs/mcm-suite-todo.md`；
驱动器与探针的**清单与体量** → §4.4（**登记，不实现搬迁**）。

---

## 3. 本轮已修（终审判"能便宜修就修"）

| 改动 | 位置 | 红证据（实测） |
| :--- | :--- | :--- |
| 谓词统一（`_POSIX_ROOTS` 共用） | `tools/papers/report.py`（**只改那一行谓词**） | 判定翻转 0 份（先量后改）；§4.2 附命令 |
| `git_tracked(RELEASE)` 判据（M-9） | `tests/papers/verify_all.py` `check_release_tracked` | FX-5（未入库落点 ⇒ 红；真 `pilot-summary.txt` ⇒ 绿） |
| `CRIT_RX` 允许前导空白（M-1） | 同上 | FX-3（缩进的 `名=FAIL` 新收、旧不收；八份产物自报失败**仍 0 条**） |
| 确定性判数取"全部行并取最严"（M-2） | 同上 `check_determinism_counts` | FX-4（先 `变了 0` 后 `变了 17` ⇒ 红；旧 `hits[0]` ⇒ 绿即 fail-open） |
| `--limit` + `report.fmt_exc` + 全文 `path_audit`（io/wm） | `tests/papers/verify_io.py` / `verify_wm.py` | FX-1 / FX-2（落点被换成放行证据本体 ⇒ 红）。**附注（措辞更正）**：报告里那句「放行证据完整性自检…两次相同 = True」**读起来像正面检查**，但**本自检测不到本脚本自身的覆写（见 §D 第 12 条）**——`post` 是在 `report.flush` **之前**测的，那一行在本脚本结构下**不可能为 False**；真正判红靠**写前复核 + 退出码** |

**红证据的落点**：`tests/papers/reports/finalfix-mutation-evidence.txt`（驱动器
`tests/papers/recon/finalfix-mutation-driver.py`，逐字输出、含对照与还原断言）。

---

## 4. 仅登记（不改代码）—— 逐条与理由

### 4.1 "从未被证明会红"的判据（终审点名，本轮**未补变异**）

口径：**"没红过"不等于"错"**——这些判据的红路要么需要构造罕见输入、要么在结构上难以触发；
下表把「为什么没红过」与「处置」分开写，**不把"未覆盖"说成"已覆盖"**。

| 判据 id | 位置 | 现状 | 为什么没红过 | 处置 |
| :--- | :--- | :--- | :--- | :--- |
| `I1-c` `I2-b` `I3-b` `I4-b` `I5-b` `I10-h` `I10-i` `I12` `I13` | `tests/papers/verify_ids.py` | 全量跑 `=OK` | 它们的红路要求**语料自身**出问题（年份/词干不一致、栏位缺失、零区分力集合变化…），43 份上 0 例 | 永久登记（补变异要造语料，代价不对等） |
| `D3-b` | `tests/papers/verify_d.py` | `=OK` | **它的 id 从不作为独立行发射**（`d3b_rows` 只在有结论时进消息），既没法 grep、红路也没演练 | 永久登记（终审点名） |
| `verify_io` / `verify_wm` 的**全部** `CRIT_RX` 覆盖 | 两份产物 | 判据行计数 **0** | 两份产物**不使用** `名=状态`/`…: True\|False` 两种形态 ⇒ 计数不适用（汇总里逐份写着"计数不适用"） | **2026-09-26 后仍有此性质**（A-2 只补了 `--limit`，没改报告形态）；登记 |
| `verify_wm.py` §4 / §6 / §7 / §8 与**空样本组守卫** | `tests/papers/verify_wm.py` | `=OK` | §4 要对照件被误伤、§6 要原件被改、§7 要有人落盘清洗版、§8 要目视存档缺失、空样本组要 `watermark-scan.json` 分组为空——都要**改语料或改产物** | 永久登记（§4 的红路最贵：要真把对照件改坏） |
| `verify_all.py` 的 `MAX_SECONDS`（`7200`）与 `all-timing` 落点守卫 | `tests/papers/verify_all.py` | 未红 | 17 条变异里 **`7200` 命中 0 次、`all-timing` 命中 0 次**（终审实测） | 永久登记：前者要真跑出 2 小时超时；后者要有人在限样本跑里写 `all-timing.txt`（可构造，但代价 = 重出一份入库证据） |

复现（**只读**）：
```bash
grep -nE '^(I1-c|I2-b|I3-b|I4-b|I5-b|I10-h|I10-i|I12|I13)=' tests/papers/reports/ids-report.txt
grep -nE '\b7200\b|all-timing' tests/papers/reports/all-mutation-evidence.txt   # 0 命中
grep -n '判据行计数' tests/papers/reports/pilot-summary.txt | grep -E 'io-report|wm-report'
# 两行都是 **0**，且括注写着「本脚本的报告两种形态都不用，计数不适用」
```

### 4.2 两条"疑似恒真"的判据 —— **实测与终审口径不符，以实测为准**

终审口径：「M-3 `verify_map.py:730-733` 的 `py_bad`（四条路径全在 `-text` 面上 ⇒ **两个算法同式**
⇒ 恒空）；M-4 `verify_ids.py:569-577` 的 `path_bad`（**两种模式都恒真**，而 `ids-recon.txt:230`
登记说"只有限样本跑才可能红"——**那句不实**）。」

**实测（命令与输出见 `tests/papers/recon/truism-checks-probe.py`，只量不改）**：

1. **`py_bad` 的两个算法不是同式** ⇒ **该判据有红路，不是恒真**；但**机理原先说错了，
   2026-09-27 按实测更正**。`v_blob_bytes` 直接量工作树字节 + git blob 头；`v_git_blob` 走
   `git hash-object`——**而它看得到什么，取决于两件事**：`git hash-object` 收到的是**哪种路径形态**，
   以及工作树是不是 CRLF。**探针 `tests/papers/recon/truism-checks-probe.py` 的用例矩阵**
   （行尾 × `-text` 面 × 路径形态，逐格读数当场打印）实测：

   * **`-text` 面 + CRLF + 仓库相对路径（或 POSIX 绝对 `/` 路径）** ⇒ 报**原始字节**
     ⇒ 两个算法**不分叉**（`-text` 生效：`git check-attr` 说 `text: unset`）。
   * **`-text` 面 + CRLF + Windows 反斜杠绝对路径** ⇒ 报**归一化**值（`c0d0fb45…` ≠ 原始字节
     `8561d5d6…`）⇒ **分叉**——**尽管 `git check-attr` 仍说 `text: unset`**：属性在这一格
     **被绕过**。**这正是 `verify_map.py` 的实际调用形态**（`v_git_blob(ROOT / p)`、无 `cwd`）。
   * **LF 工作树** ⇒ 归一化是恒等变换，三种路径形态**都不分叉**。
   * 无 `-text` 面 + CRLF ⇒ 三种路径形态**都分叉**。

   ⇒ **真触发条件**（就入库的四条路径而言）= 「**工作树里有 CRLF**」+「传的是 **Windows 反斜杠
   绝对路径**」；**`-text` 有没有不是条件**（反斜杠路径下它不生效）。⇒ 那四条路径上它们相等，
   **因为工作树是 LF**，**不是**因为 `-text` 被尊重。
   ⇒ 该判据的红路仍在（红路 = 工作树出 CRLF），且**它今天之所以还有红路，恰恰是靠这个绕过**：
   若属性真被应用，`v_git_blob` 与 `v_blob_bytes` 在 `-text` 面上将**恒等**、`py_bad` 结构上恒空。
   唯一没做到的仍是：**没有一条入库变异证明过它会红**（进 §4.1 类）。
   **登记（冻结件，只登记不改）**：`tests/papers/verify_map.py:159-173` 的 `v_git_blob` docstring
   自称口径是"**按 `.gitattributes` 的过滤器口径**"——与上面的实测**不符**（实际传进去的是
   Windows 反斜杠绝对路径 ⇒ 属性被绕过，量到的是 `core.autocrlf` 归一化值）。同一句里的
   "两条算法**都要**跑：结果不等 ⇒ 红——那说明 `corpus/papers/**` 的 `-text` 约定被破坏了"
   也因此**归因不准**（真正的红条件是"工作树出 CRLF"）。`verify_map.py` 是**冻结件**（M15/M18
   两条变异锚在它身上）⇒ **本轮不改代码、不造反例**，只在此登记。
2. **`path_bad` 与"全量/限样本"无关**：`index.build` 里 `dest = out_dir or io.DERIVED`，
   三个落点都写成 `dest / "<名>"`；`verify_ids` 那侧比的是 `prod_dir / "<名>"`，而 `prod_dir`
   **就是**传进去的 `out_dir` ⇒ **只要 `out_dir` 非空就两边同值**，两种模式都恒空
   （实测：`out_dir=<tmp>` 时报告的 `index_path` / `tags_path` / `prov_path` **三者全等**于 `<tmp>/<名>`）。
   ⇒ 与终审「两种模式都恒真」**一致**（就"未施加代码变异时"这一层），但与 `ids-recon.txt:230` 那句
   「**只有限样本跑（M13）才可能红**」**不一致**：M13（把返回值里 `index_path` 写成 `io.DERIVED/"INDEX.md"`）
   在**限样本**模式下才分叉（`prod_dir ≠ io.DERIVED`），在**全量**模式下恰好同值、测不到。
   ⇒ **准确的登记**：该判据（未加代码变异时）在**两种模式下都恒空**；它唯一被证明过的红路是
   **限样本 + M13**（`tests/papers/reports/ids-mutation-evidence.txt` §M13：`I2=FAIL`、`--limit 3`）；
   全量模式下要它变红，必须把 `dest = out_dir or io.DERIVED` 改成**与 `out_dir` 无关**的值。

**处置**：两个脚本都冻结 ⇒ **不改代码**。`tests/papers/recon/ids-recon.txt` 的 R3 行**已加日期落款的更正**。
**要更正的那句不是终审指的那句**：R3 的第一格（"全量放行跑里结构上恒真"）**不完整**（限样本也恒空），
第三格（"只有限样本跑（M13）才可能红"）**在"M13 这一条变异"上是准确的**——故更正写的是"两种模式都恒空"
而不是"那句不实"。

### 4.3 `RT-M3`：终审称"2b 轮已覆盖" —— **实测不成立**

终审口径：「`map-mutation-evidence-2b.txt:555` **就是**幻影红路原文（`M-7=FAIL` + 具名）
⇒ 2b 轮**已覆盖**，那条『无变异覆盖』的登记**已过期**」。

**实测**：`:555` 的 `M-7=FAIL` 是 **M-7 的另一支** —— 消息是
`桶 2：来源题列 [('2025','B'),('2025','E')] ≠ 指针行反推的题 [('2025','A'),('2025','B'),('2025','E')]`
（那是变异 V-5「改错一行『所属桶』列」打出来的，走 `verify_map.py:1106` 那条）。
**幻影支的具名消息是另一串**：`配对表里出现了 TAGS 一层没有的稳定 ID：…`（`verify_map.py:1090`）。
命令（**全库 grep**）：
```bash
grep -rn "一层没有的稳定 ID" tests/papers/ docs/ corpus/papers/*.md
# 只有 verify_map.py:1090 那一行（源码），**入库证据里 0 命中**
```
⇒ **幻影红路仍然没有入库红证据**，`map-recon.txt` §13 的 `RT-M3`（含 §14 的"这条缺口仍在"）
**不需要更正**；它的证据原本只有**手工探针** `build/t6b2a_probe_phantom.py`——而那份探针**在 gitignored 目录里**，
按本项目规矩**等于丢失**。⇒ **本条登记升级**：真正的缺口是"幻影红路的**唯一**证据不入库"，
补法要么把它做成一条变异（连带重出 412 KB 的 2b 证据），要么把探针搬进 `tests/papers/recon/`。

**收尾（2026-09-27，用户裁决：搬探针）**：

1. **缺口仍在**（**入库红证据 0 命中**）。口径要收紧——"证据里 0 命中"指的是**捕获到的输出**：
   ```bash
   grep -rn "一层没有的稳定 ID" tests/papers/reports/     # 0 命中（入库证据面）
   ```
   上面那条全库 grep（`tests/papers/ docs/ …`）**不能这样用**：它连**本文件与 `map-recon.txt`
   对这句话的复述**一起命中——复述不是证据（`mcm-suite-todo.md` §D 第 9 条 ②）。
2. **入库了一份能跑过的探针**：`tests/papers/recon/map-phantom-probe.py`。它只把 `MODEL_MAP.md` 的
   **一行**桶指针改成幻影 ID、跑 `verify_map.py --limit 3`（落点 gitignored、不碰放行证据）、
   断"退出码非 0 + 红 id 集合非空且含 `M-13` + `M-7` 块里有具名说明 + 无 traceback + 按原始字节还原"。
   **旧的 `build/t6b2a_probe_phantom.py` 期望 id 已过期**（它断言 `M-3=FAIL`，而 2b 已把配对判据
   改名 `M-13`，`M-3` 这个编号不再存在）⇒ 它**今天自己跑不过**，**别再引用它**。
3. **实测红 id 清单**（口径：该探针 stdout 当场打印）：`M-2 / M-13 / M-4 / M-7 / M-8`（`M-3` 不打印）。

### 4.4 驱动器清单与证据体量（I-4，**登记，不实现"驱动器入库"**）

2026-09-26 实测（`ls` + `wc -c`，命令见下）：

**入库的驱动器（`tests/papers/recon/*.py`，9 个）**：`all-determinism-scan.py` 10792 B ·
`all-mutation-driver.py` 39249 B · `finalfix-mutation-driver.py` 16015 B（本轮新增）·
`formula-band-scan.py` 13155 B · `formula-geom-scan.py` 11590 B · `heading_size_hist.py` 11417 B ·
`ids-recon-scan.py` 26446 B · `types-recon-scan.py` 18323 B · `wm_font_probe.py` 6461 B

**仍在 gitignored `build/` 的驱动器（不入库 ⇒ 按规矩等于丢失）**：`ids_mutdrive.py` 32340 B ·
`map_mutdrive.py` 33302 B · `map_mutdrive2.py` 29401 B · `mutdrive.py` 50638 B ·
`mutation_runner.py` 11489 B · `mutation_runner_r2.py` 10893 B · `types_mutdrive.py` 14320 B ·
`t6b2a_probe_phantom.py` 4835 B …

**它们产出的入库证据体量**：`ids-mutation-evidence.txt` **476210 B** ·
`map-mutation-evidence-2b.txt` **411984 B** · `map-mutation-evidence.txt` 329172 B ·
`d-mutation-evidence.txt` **2074214 B** · `types-mutation-evidence.txt` 185797 B ·
`b-mutation-evidence.txt` 92453 B · `c-mutation-evidence.txt` 57164 B ·
`all-mutation-evidence.txt` 36958 B · `finalfix-mutation-evidence.txt` 26462 B ·
`wm-mutation-evidence.txt` 4137 B
```bash
ls -1 tests/papers/recon/*.py | while read f; do printf "%-52s %8s\n" "$f" "$(wc -c < "$f")"; done
ls -1 tests/papers/reports/*mutation*.txt | while read f; do printf "%-56s %9s\n" "$f" "$(wc -c < "$f")"; done
```
**为什么只登记不实现**：驱动器入库要跨目录搬迁（脚本按 `parents[3]` 定位仓库根，**换目录就跑不起来**）
+ 重出全部证据（合计约 **3.8 MB**），而驱动器本身**可以从证据逐字重建**（证据里有变异的锚点原文与命令）。
⇒ 代价不对等；**终审也判"仅登记"**。

### 4.5 探针覆写风险：`index.py` 的守卫可被**显式 `out_dir`** 绕过（**不改 `index.py`**）

**终审自曝的事故**：它的探针用 `index.build(out_dir=io.DERIVED, sample=[1 篇])`
**覆写**了 `corpus/papers/{INDEX,TAGS,PROVENANCE}.md` 三份入库产物（事后已还原）。
**根因**：`index.py` 新增的守卫只在「**限样本 + 未显式给 out_dir**」时抛
（`sample is not None and out_dir is None`）⇒ **显式传 `io.DERIVED` 就绕过**。
**为什么本轮不改**：改 `tools/papers/index.py` 属于**另一次解冻**（它是 Task 6 的冻结交付物，
且 M15/M18 两条变异锚在它身上）。⇒ 登记；**待裁决**：是否把守卫加严成
「**限样本跑一律不许把落点算到入库产物目录**（不论 out_dir 是不是显式给的）」。

### 4.6 D 项可用性缺口（**不动产物**，登记 + 待裁决）

* **`INDEX.md` 是五份产物里唯一没有覆盖边界块的**（`TAGS.md` / `PROVENANCE.md` / `MODEL_MAP.md` /
  `PROBLEM_TYPES.md` 都有）——而它最可能是用户**先打开**的那一份。
* **`PROVENANCE.md` 缺"不能让读者推出的结论"一节**（其余几份有）。
* **为什么不动**：改这两份会打红 `verify_map` 的 **M-1**（`PROVENANCE.md` 的"逐字节不变"与
  `INDEX.md` 的"只许差第 10 栏"**都是判据链的一环**）⇒ 属**需要用户点头的另一次解冻**。

---

## 5. 待用户裁决（不在本轮范围）

1. **`INDEX.md` / `PROVENANCE.md` 的可用性补丁**（§4.6）——要动产物 + 改 `verify_map` 的 M-1 基准。
2. **`tools/papers/index.py` 的守卫加严**（§4.5）——限样本跑一律不许落进入库产物目录。
3. **`RT-M3` 的幻影红路证据**（§4.3）——**已按用户裁决做掉**（搬探针，非做变异）：
   探针 `tests/papers/recon/map-phantom-probe.py` 已入库且可重跑（**入库红证据仍 0 命中**，
   那一条缺口按原样保留）。
4. **Task 9 的题号口径**（`io.problem_of` 77/201 取不到题号）——**先定口径再扩语料**。
