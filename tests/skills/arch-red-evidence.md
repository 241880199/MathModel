# `arch-red-evidence.md` — "写论文某一节" RED 的取数记录

**本文件只写落库时在盘上实测/复算出来的东西。** 凡引用的外部结论，一律指向文件与行号；凡本机查不到的，写"**未能核实**"。
材料本体在 `tests/skills/arch-cases/`；说明见该目录的 `README.md`。

**被测目标**：`mcm-section-writer`（尚未建；`.claude/skills/` 下无此目录，落库时实测）。★ 2026-10-03 时点注：本行写于 RED 期，当时该 skill 确未建；`mcm-section-writer` 已于 2026-10-03 落地。
**案例**：2025 MCM A 题 / 获奖论文队号 `2501909`（与 `abs-cases/` 同一份案例）。

---

## 1. 入库文件身份（逐份实测）

落库命令形态：`cp -p build/arch-red/<f> tests/skills/arch-cases/<f>`（**只复制，不改一个字节**）。
「逐字节相同」= `cmp -s <源> <入库>` 的退出码为 0；下表的 `identical` 列即该判定。

| 文件 | 字节 | 行数 | identical | `git hash-object`（blob，本仓 `object-format=sha1`） | SHA-256 |
|---|---|---|---|---|---|
| `brief-S1.md` | 3953 | 28 | **True** | `8c0876f672e10242bfad8672c74cabcaab531f2b` | `8933f4b58dcb87753e8c06d8f8bf8fdc881616d063de461353e4bf44a574e571` |
| `brief-S2.md` | 2780 | 19 | **True** | `eb15117fc47e5e775818aac5bad3a9f3934bc873` | `01ae368304950297331bfed661b26d75a3d7ef3824c64bd2f0f5315c2df646b4` |
| `true-S1.md` | 6547 | 158 | **True** | `f872abffbfe661556df56a4a17ca400fbe0dd9a9` | `6566eda532cc3f9179fec55c0204101e9fe337ab162f02d14cf68a126d68fb77` |
| `true-S2.md` | 3433 | 56 | **True** | `020c47fbfec5759943f1d52517fba3d6faa43467` | `5b07752ae2514861c38d17d5568f3a5a0ef6a7b558536370314da86691e4798d` |
| `out-S1.md` | 14244 | 135 | **True** | `7b0d08fb1b97b24218fc690de263765bb2e246ea` | `802d902dcc4f04dd6a299e23422b6215de86a45ae334431dc16d3c9e449fb220` |
| `out-S2.md` | 10927 | 52 | **True** | `293b851760d6fddcd390e2e76a78bac9769532fb` | `29f43b83459bdb7e91a45169f3a9d733565b48e52660f6b1a187816cdb553e91` |
| `out-S2-p.md` | 8948 | 56 | **True** | `db0d6b20095bfc14b1ba30c96c59ff8cf2d39b8d` | `67ca0a8a4f7c299a134da7403a79748e43f5f770bdddf0e257da71747f6e47fc` |
| `README-RED.md` | 10128 | 118 | **True** | `338b9b1518487f669df1a8e4ea8e860f9a4638a2` | `24e4b146a661808bacd5e8e80db6d209fb76016b407833e550112fe782a0339d` |
| `judge.md` | 47713 | 340 | **True** | `6d1f616708eff0ed3399eedd3d9f2f5a9b743fa9` | `67fdc5c41adc72c6f329549b07075160741244fca784f1d100fa6da504d9db84` |

**两个哈希口径的说明**（免得把上面两列混为一谈）：

- `git hash-object` 在本仓给出的是 **SHA-1 的 git blob 哈希**（实测 `git rev-parse --show-object-format` = **`sha1`**，故为 40 位十六进制），**不是** SHA-256。
- `.gitattributes` 里有 `tests/skills/** -text` ⇒ 对这批文件 git **既不规范化也不转换**，
  故「工作树字节 == 入库 blob」这条恒定成立，`git hash-object` 与工作树可比。
- 右列 SHA-256 是用 `sha256sum` 对**工作树字节**直接算的，与本目录的源文件相同（因 identical=True）。

**行尾**：9 份全部是 **LF**（实测每份的 **CR 字节数 = 0**、LF 字节数 = 行数；`file(1)` 报 `UTF-8 text`），末字节均为 `0x0a`。

**未入库、仍留在 `build/arch-red/` 的三份**（**另一次** RED：`mcm-paper-architecture`，本轮按指示不搬、只登记）：

| 文件 | 字节 | 行数 | `git hash-object` |
|---|---|---|---|
| `build/arch-red/red-arch-A.md` | 22276 | 213 | `05219d0bb9cc1345e70ad8fc3fad9cb6a7b55f03` |
| `build/arch-red/red-arch-C.md` | 27423 | 316 | `6abe4eebfb9160a5ec3a88b59eb820f94782f837` |
| `build/arch-red/red-arch-P1.md` | 9782 | 144 | `f1610910a1199fda5107139814d142f4f66c6f6a` |

> ⚠️ `build/` 是 gitignored（`.gitignore:6`；实测 `git check-ignore -v build/arch-red/judge.md` → `.gitignore:6:build/`）⇒ 这三份**目前无版本**。

---

## 2. `judge.md` 的"量出来的标记表"（**原样引用**）

**出处**：`tests/skills/arch-cases/judge.md` 的 **§1「标记清单（**量出来的**；未出现的全部删掉）」→ §1.1「保留的标记（产物里确实出现）」**，
即该文件的**第 31–44 行**。以下为**逐字引用，未改一个字符、未加一句解释**（含源文件里原本就有的 `\|` 转义）：

````text
### 1.1 保留的标记（产物里确实出现）

| # | 标记 | S1 | S2 | S2-p | 逐字例证（行号） |
|---|---|---|---|---|---|
| **M1** | **段末总结/升华句**（段落最后一句不是收束事实，而是给一个判断/评价/格言） | **8 / 21**（38%） | **10 / 10**（100%） | **6 / 9**（67%） | S2 最密，每条论据段末尾都是。逐条见 §1.3 |
| **M2** | **对比式论断** `rather than` / `not merely\|only\|just` | **5**（4+1） | **6**（5+1） | **3**（3+0） | S1:20 `would add noise rather than information`；S1:43 `go bowed in the middle rather than flat`；S1:41 `does not merely add more footsteps`；S2:11 `We consider this a requirement rather than a convenience`；S2:9 `not merely about total volume of traffic`；S2-p:5 `rather than as a collection of independent effects` |
| **M3** | **强调副词** `precisely` / `exactly` | **5** | **1** | **1** | S1:36 `is precisely the cumulative number of traversals`；S1:45 `These are precisely the conditions under which Archard's wear law applies`；S1:26 `which is exactly the local wear depth`；S1:43 `which is exactly why real treads go bowed`；S1:107 `trade off against each other exactly as intuition suggests`；S2:25 `difficult precisely because so many influences are folded`；S2-p:7 `It is precisely what allows the model to reflect` |
| **M4** | **对偶破折号插入语**（`— …, … —` 包夹式同位语） | **7** / 4.0‰ | **4** / 3.3‰ | **5** / **6.2‰** | S2-p:7 `described by a normal — and, in the two-directional case, a multivariate normal — distribution`；S2-p:9 `The quantities it requires — the depth of wear on a tread, the initial hardness …, and comparable properties of the stone — are obtainable`；S2:17 `— most notably the reliability of an age estimate, and the comparison of a stone's wear against the wear expected of a particular quarry —`；S1:26、36、41、43、49、107 |
| **M5** | **格言式收尾** | 2 | 2 | 1 | S1:5 `**wear is the accumulated residue of behaviour**`；S1:107 `a heavily worn tread is either very old and lightly used, or young and heavily used`；S2:19 `a simple rule for the reader: …`；S2:25 整段 `Wear on a staircase is unavoidable. Any surface that people cross often enough will yield to them …`；S2-p:25 `The wear of a stairway is unavoidable. It is, in effect, a trace left behind by the people who passed over it` |
| **M6** | **自评式套话**（对本文/本节的自我评价，非内容） | 2 | 3 | 2 | S1:38 `The physical reasoning behind (3.3) is worth stating explicitly`；S1:107 `Equations (3.11) and (3.12) are the payoff of this section.`；S2:3 `The purpose of this section is not to defend what we have built, but to state plainly what it does well`；S2:11 `We consider this a requirement rather than a convenience.`；S2:23 `our aim here is to state what has been delivered.`；S2-p:7 `This randomness is not a technical refinement.`；S2-p:17 `These are limitations of scope rather than of construction.` |
| **M7** | **篇幅膨胀比**（同一内容，产物字数 ÷ 源文对应字数） | **1.7×**（1759 / 1025，源含公式碎片；按纯散文约 2.1×） | **3.3×**（1206 / 366） | **2.2×**（802 / 366） | 源文 3 条优点共 ~90 词、2 条缺点共 ~55 词；out-S2 对应约 330 / 185 词 |
| **M8** | **强调句 / 指示代词起句复用**（`is what`·`it is what`·`it is this` 强调句 + `This <名词>` 起句） | **1**（强调 1 + 起句 0） | **7**（强调 4 + 起句 3） | **2**（强调 1 + 起句 1） | 强调句 S1:109 `is what decides where the wear concentrates`；S2:7 `is what allows … and it is what makes`（同句 2 次）、S2:7 `it is what makes`、S2:23 `it is this component that lets us ask`；S2-p:5 `is what makes the central inference possible at all`。起句 S2:7 `This integration`、S2:9 `This choice`、S2:17 `This is a substantial simplification`；S2-p:7 `This randomness`。**基线 = 0**（`true-S1/S2` 各 0） |
| **M9** | **模板化元话语路标** | 3 | 3 | 1 | S1:7 `This section makes that idea quantitative.`；S1:109 `What remains is to determine … That is the subject of Section 3.2.`；S2:3 `We now step back and assess the model as a whole.`；S2:19 `Taken together, these strengths and weaknesses suggest …`；S2:25 `We close with a reflection that the problem itself invites.`；S2-p:17 `— a direction we take up in the conclusion.` |
| **M10** | 三项/四项排比 | 有 | 有 | 有 | S2:7 `how hard the material is, how many feet cross it, and where those feet land`；S2:19 `to compare, to rank, and to characterize`；S2-p:13 `The number of people using the stairs, their direction of travel, the loads they carried, and the frequency of their passage`；S1:20 `stored, plotted, differenced and integrated` |
````

**同一节里另有两张表，位置登记在此（本文件不重复引用）**：

| 位置 | 是什么 |
|---|---|
| `judge.md` §0（第 14–26 行） | 「我实际用到的量（先把口径写死）」——正文字数 / 段数 / 数字字符数 / 破折号数 |
| `judge.md` §1.2（第 46–57 行） | ★「我提过的、**产物里根本没出现 → 全部删掉**」——候选标记的实测与处置 |
| `judge.md` §1.3（第 59–70 行） | M1 的逐段落点（"这是我要复核的死数，故全列"） |
| `judge.md` §6.2（第 283–297 行） | 第三层文风：七个候选代理量 + 自补 2 个的实测分布 |

---

## 3. 独立复算：两张六组体重表（`out-S1.md` vs `true-S1.md`）

落库时按盘上文件逐格复算，**不引任何转述**。

- **产物表** `out-S1.md:71–76`：`mm 35/10`、`fm 33/10`、`am 78/28`、`af 65/28`、`om 70/12`、`ow 63/12`。
- **真实论文表** `true-S1.md:108–125`：`mm 40/10`、`fm 38/10`、`am 75/30`、`af 65/30`、`om 70/10`、`ow 60/10`。
- **逐格比对（6 体重 + 6 占比 = 12 格）**：**8 格不同、4 格相同**。
  相同的 4 格为：体重 `af` = 65、`om` = 70；占比 `mm` = 10、`fm` = 10。
- **加权和**：产物表 = `0.10·35 + 0.10·33 + 0.28·78 + 0.28·65 + 0.12·70 + 0.12·63` = **62.8**；
  真实表 = `0.10·40 + 0.10·38 + 0.30·75 + 0.30·65 + 0.10·70 + 0.10·60` = **62.8**。**两表都恰好等于 62.8。**
- **与 `judge.md` 的记法有一处出入**：`judge.md:177` 写作"**十二格里九格不同**"，复算得 **8 格不同**。
  本节只登记这一处按文件复算的结果与差异，**不对哪一方下判定**。

**产物表在正文里的"署名"（逐字例证）**：`out-S1.md:65` `In the absence of local demographic data, we adopt the WHO global body-weight references as the default calibration, reproduced in Table 3.1.`；
`out-S1.md:67` 表题 `**Table 3.1** Reference mean body weights and population shares for the six pedestrian groups.`。
真实论文同位置的出处标注（逐字）：`true-S1.md:100–101` `based on the global weight data provided by the World Health Organization (WHO)[6][7]`。

---

## 4. 来源交代：`true-*.md` 是获奖论文的逐字节选（第三方文本）

**独立复验（落库时实测，非引用）**：把 `true-*.md` 从标记行 `===== BEGIN VERBATIM 以下为逐字原文 =====` 之后的部分取出，
与 `tests/skills/abs-cases/case-A-body.md` 的对应区间逐字节比对：

| 文件 | 取值区间（`true-*.md`） | 对应源区间（`case-A-body.md`） | 字节 | `cmp` 结果 |
|---|---|---|---|---|
| `true-S1.md` | 第 9–158 行（标记行在第 8 行） | **第 147–296 行** | 5910 = 5910 | **逐字节相同** |
| `true-S2.md` | 第 12–56 行（标记行在第 11 行） | **第 929–973 行** | 2375 = 2375 | **逐字节相同** |

**⇒ `true-*.md` 与 `abs-cases/` 里的 `case-A-body.md` 同源**（`case-A-body.md` 自身派生自
`corpus/papers/md/2025美赛O奖论文/A/2501909.md`，见 `tests/skills/abs-cases/README.md` §一）。
即：`true-S1.md` / `true-S2.md` 是**同一份第三方文本的两个更短切法**。

**用户已就"md 是否上公开远端"做过裁决（保留）**：口径记在 `.superpowers/sdd/progress.md:2265–2276`
（标题「★★ 推送完成 + 一处 controller 的口径疏漏（用户裁决：保留）」；裁决原文：*"**用户裁决：保留 md**（理由：① 当初把 1.86 GB 挡在远端**主要是推不动**，不是版权红线；② **产物要靠它才可核** …③ 43 份 md 只有几百 KB）。**未做任何回退**。"*）。
**本目录的入库形态与该裁决一致**：本目录装的是同一份 md 的**更短节选**，而**更长的 `case-A-body.md` 早已在 `tests/skills/` 下入库**。
（注：`.superpowers/**` **不在仓库里**——`progress.md` 只在本机，该文件不是本次入库物。）

---

## 5. 复现路径（怎么再跑一遍这次对照）

**材料**（全部在 `tests/skills/` 下）：写给写手的两份 `arch-cases/brief-S{1,2}.md` + 题面 `abs-cases/case-A-problem.txt`；
对照的两份 `arch-cases/true-S{1,2}.md`；口径 `arch-cases/README-RED.md`；量判方法 `arch-cases/judge.md`。

1. **取样**：只给写手 `brief-S1.md`（或 `brief-S2.md`）**+** `case-A-problem.txt`，让它写出那一节。
   **不得**给它 `true-*.md` / `README-RED.md` / `judge.md`（前两者是对照，后两者是泄题）。
2. **切正文**：产物末尾那段 `## 我的做法说明` 是 agent 自述，**不是论文的一部分**，量措辞前先切掉
   （`judge.md` 的口径：说明段不计入统计，凡引用单独标「说明段」）。
3. **判什么量**：按 `judge.md` §1 的标记清单（本文件 §2 已原样引用）逐条去**产物里量**——
   **出现才留、没出现一律删**（§1.2 的做法）；再用 §2 的三条尺子逐条判 0/1 并附逐字例证。
4. **对照**：`true-*.md` **只用于内容覆盖**（`judge.md` §3），**不评风格**。
   理由写在 `judge.md` §5.3 第 3 条与 §6.1 的「★ 限制」：`true-*.md` 是 PDF 转换件，
   公式被打散成 2–10 行、含页码残留行、行尾软连字符断词、破折号与连字丢失 ⇒ **标点密度与句法表面不可比**。
5. **算第三层文风读数**：按 `judge.md` §6.1 的方法与 §6.2 的九个代理量算，真值一侧一律标 `(approx)`；
   **先给分布、后说"偏离到多少值得改"**，**不设魔法阈值**（§6.2 的硬要求）。
6. **两条必须一起读的口径**：
   - `README-RED.md` §3「★ 不得判成写手之错的清单」（源 md 排版破碎 / 原文字面错误 / 页码残留行 / 交叉引用）；
   - `README-RED.md` §5「★ 已知的结构性损失」（Archard 适用性论证被压成半句 ⇒ **不得污染其余 11 条要点的判定**）。

**要判的量（一句话版）**：`judge.md` §0 的四项基量 → §1 的 M1–M10 标记 → §2 的三条尺子逐条 0/1 → §3 内容覆盖 → §6 的九个文风代理量。

---

## 6. 未能核实 / 本文件未做的事

- **`.superpowers/sdd/progress.md` 的内容**只在本机（该目录 `0 tracked`、`*` gitignore），**本次入库未包含它**；
  本文件对它只作**指认**（给出行号区间），未复制其内容。
- **`build/arch-red/` 里另一次 RED 的三份产物**（`red-arch-A/C/P1.md`）**本轮未入库**（按落库指示），
  只登记了身份（§1 末表）⇒ **它们仍无版本**。
- **`judge.md` 内部各项读数（词数、CV、Flesch、TTR 等）未在本文件复算**——
  它们的分词/分句脚本没有随材料落库，**本机没有可重跑的脚本**；本节只复算了 §3 的 12 格表与 §4 的逐字节切分。
  若要复算 `judge.md` §6 的九个代理量，**需按 §6.1 的口径另写脚本**（口径已写在那里，脚本本身**未能核实其存在**）。
- **`out-*.md` 的采样过程（几次采样、什么模型、什么温度）未能核实**——材料里没有记录，本文件不猜。

---

## ★ 编者按（2026-09-27，controller 复算后追加）

**一处登记在案的出入：`judge.md:177` 的"十二格里九格不同"应为 8。**

- **起因**：落库助手逐格复算得 **8 格不同 / 4 格相同**，与 `judge.md` 记的 9 不符；它**两处都如实登记、不下判定**（正确做法）。
- **controller 亲自复核**（不采信任何一方）：
  - 真值表 `tests/skills/arch-cases/true-S1.md:103-125`：体重 `40/38/75/65/70/60`、占比 `10/10/30/30/10/10`
  - 产物表 `tests/skills/arch-cases/out-S1.md:69-77`：体重 `35/33/78/65/70/63`、占比 `10/10/28/28/12/12`
  - **逐格比对**：体重 4 处不同（`af` 65、`om` 70 相同）；占比 4 处不同 ⇒ **合计 8 格不同 / 4 格相同**。
- **两表都恰好得 62.8**，且**占比也被改过**：真值 `40×.1+38×.1+75×.3+65×.3+70×.1+60×.1 = 62.8`；产物 `35×.1+33×.1+78×.28+65×.28+70×.12+63×.12 = 62.8` ⇒ **反推凑数**的结论不受影响、反而更清楚。
- **处置**：`judge.md` 是**逐字入库的对照件**（第三方/当时形态），按本项目体例**不静默改**；出入在此登记，
  已按复查结果更正的是 `docs/mcm-writing-discipline.md` 的对应行（并在该行注明此处出入）。
- **教训（与 lessons 4.8 同族）**：**"9"这个数是从 `judge.md` 转抄进纪律文档的，而我没复算**——转抄即风险；凡数字进权威文档前必须当场复算。

**另登记一处同型出入：`judge.md:101` 的"与真值表逐格不同"应为"12 格里 8 格不同 / 4 格相同"。**

- **出处（逐字）**：`tests/skills/arch-cases/judge.md:101`（§2.2「尺子② 表达准确」表首行）写作
  *"表内数（35/33/78/65/70/63；10/10/28/28/12/12）**与真实获奖论文的表（`true-S1.md:109–124`：40/38/75/65/70/60；10/10/30/30/10/10）逐格不同**，而两张表都恰好得 62.8"*。
  "**逐格不同**"的字面含义是 12 格全不同。
- **复算（与上一条用同一组两张表，口径见本文件 §3）**：真值 `40/38/75/65/70/60`、`10/10/30/30/10/10`；产物 `35/33/78/65/70/63`、`10/10/28/28/12/12`。
  **逐格比对：体重 4 处不同（`af` 65、`om` 70 相同）、占比 4 处不同 ⇒ 合计 8 格不同 / 4 格相同**。
  命令（`tests/skills/arch-cases/` 下）：`sed -n '69,77p' out-S1.md` 与 `sed -n '103,125p' true-S1.md` 逐行取数后人工比对。
- **性质**：与 `:177` 的"十二格里九格不同"是**同型错**——同一组 **4 格相同**被漏数，而"两表都恰好得 62.8"的结论**不受影响、反而更清楚**（差异越少、越说明是在凑那个数）。
  两处**互相独立、不在同一节**（`:177` 在 §4.1，`:101` 在 §2.2）。
- **处置**：与 `:177` 同 —— `judge.md` 是**逐字入库的对照件**（第三方/当时形态），按本项目体例**不静默改**；出入在此登记，
  已按复算结果更正的是 `docs/mcm-writing-discipline.md` 的 A1 行（并在该行注明这两处出入）。
- **与上一条的关系（如实分开，不合并因果）**：上一条（`judge.md:177` 的"九格"）确实**被转抄进了纪律文档**，是本轮已修的错；
  这**一条（`:101` 的"逐格不同"）从未进过纪律文档**——它只是 `judge.md` 内部的两句同型粗算，**修正它的唯一后果**是让"12 格里 8 格不同 / 4 格相同"这句话在证据链里**只有一个版本**。

**另登记**：`build/arch-red/` 里另有**三份**属于**另一次 RED**（`mcm-paper-architecture` 的骨架测试）的产物
（`red-arch-A.md` / `red-arch-C.md` / `red-arch-P1.md`），**本轮未入库**（该 skill 已决定不单做），
其路径/字节/行数/hash 在 `tests/skills/arch-cases/README.md` §五 登记；**它们目前仍只在 gitignored 目录里 ⇒ 若要留档需另开一轮**。

---

## ★ 编者按 ②（2026-09-27，修复轮发现后追加）

**`judge.md:314` 有一处"归错词"（数对、词错）**：该处把"模板化过渡词表"的唯一命中说成**真值 `In addition` 那一处**；
实测那一处的命中的是 **`true-S1.md:80` 的 `Moreover`**（`In addition` 出现在 `true-S1.md:44`，属**宽表**，不在本次窄表内）。
- **影响面**：**"五份合计只命中 1 次"这个数是对的**（我按窄表复算仍为 1）；错的只是**它把这个命中的词说成了哪个**。
- **处置**：`judge.md` 是入库的判词原件，**按体例不静默改**；出入在此登记（与 `:101`/`:177` 两处同型错的编者按同一体例）。
- **口径**：窄表 = `Moreover|Furthermore|Additionally|In conclusion`；宽表另含 `In addition`。**引用这一条时必须写明用哪张表**。
