<!-- ↓↓↓ 本行以下为入库头注（由落库助手写），再往下是 `build/abs-red/quality-score.md` 的逐字全文 ↓↓↓ -->

# `mcm-abstract` 质量判分表（13 条 Q1–Q13）

**这是什么。** 本文件是 `build/abs-red/quality-score.md` 的**逐字入库**（入库时**未重排、未改写任何结论**，
一个字的原文都没动）。它的内容是对 **6 份 RED 基线产物**（`tests/skills/abs-cases/red/red-{A1,A2,A3-partial,C1,P1,P2}.md`）
逐条的 13 项打分记录（评分时间 2026-09-27）。

> ⚠️ **但本副本此后按复审结论做过 4 处勘误（正文已改动，逐字节后缀校验因此失效）** ：
> ① §2-Q2 把原标为 `P1` 的 `**The questions.**` 段更正为 `P2`（逐字在位：`red-P2.md:12-15`；
> 在 `red-P1.md` 命中 0）—— §2 的"一句话理由"栏 **与** §3-Q2 两处都改了，并补上 P1 的可用证据（边界）；② §3-Q11 删掉 6 个**口径不可复现**的字符数、
> 补上**可复现**的词数口径；③ §二 的「★ 行 8 条」更正为 **7 条**并注明两个计数量不可混；
> ④ 本节下面新增「勘误记录」。**逐条见文末「勘误记录」**，每条都带复核命令。

**冻结指纹（入库时实测）**：原文件 `build/abs-red/quality-score.md` = 172 行，
sha256 前 16 位 `ec0c82ea4bf73094`。**入库时**本文件 = 上面这段头注 + 原文件全文逐字节拼接，
拼接校验见文末「入库校验」（**该断言因下面的勘误已失效，留档而已**）。

---

## 一、这份清单的两个身份

| # | 身份 | 落地位置 |
|---|---|---|
| a | **`mcm-abstract` skill 质量层的来源** | `.claude/skills/mcm-abstract/SKILL.md` 的「质量与措辞」一节（★ 行 = 指导，末行 = 规格） |
| b | **将来 SkillOpt 用的判分表** | 13 条即 13 个判分项；打分纪律（0/1 可指认、证据不足判 N/A、页码按词数估）见原文 §0 |

## 二、13 条的两种身份：★ 6 条实测有基线失败 / 7 条全做到（规格）

| 身份 | 条数 | 条目 | 判据（来自原文 §2 的 0 分计数） |
|---|---|---|---|
| **★ 指导**（实测有基线失败） | **6** | **Q2 · Q6 · Q7 · Q9 · Q11 · Q12** | 6 份基线里真的栽过（0 分 2/5/5/3/6/4 次） |
| **规格 / 判分项**（一次都没失败） | **7** | **Q1 · Q3 · Q4 · Q5 · Q8 · Q10 · Q13** | 6 份**全部做到**（0 分 0 次）⇒ 没有基线证据支撑写成「指导」 |

**0 分次数一览**（逐字取自原文 §2 结论句与 §1 矩阵末行）：

```
Q1  0/6   Q2  2/6   Q3  0/6   Q4  0/6   Q5  0/6   Q6  5/6   Q7  5/6
Q8  0/6   Q9  3/6   Q10 0/6   Q11 6/6   Q12 4/6   Q13 0/6
其中 Q6/Q7/Q11 近乎全灭（5/6、5/6、6/6）。
```

原文 §2 的结论速览（逐字）：*"清单里真正在基线失败过的有 **6 条**（Q2、Q6、Q7、Q9、Q11、Q12），
其中 Q6/Q7/Q11 近乎全灭；**7 条一次都没失败**（Q1、Q3、Q4、Q5、Q8、Q10、Q13）→ 只当规格/判分项，
写成"指导"没有基线证据支撑。"*

**归属依据**：★ 与规格的划分见 `.claude/skills/mcm-abstract/SKILL.md`「质量与措辞」一节
（★ 行 **7** 条 = Q6/Q7/Q11/Q12/Q9 + 「结果没出来就显式标缺」[Q7 家族] + Q2；规格列 Q1/Q3/Q4/Q5/Q8/Q10/Q13。
**「7 条」为复审实测更正**：计数以 SKILL.md 的 ★ 标记行数为准，与上表「★ 6 条」（= 判分项数，Q7 家族合为一条）是**两个不同的量**，勿混。）

## 三、每条的依据指针（官方 / 官方† / 社区）

逐字取自原文 §4「逐条依据一览（可直接抄进清单）」。分级符号的含义（见 `corpus/official/INDEX.md` §0）：
`[官方]` = 官方硬性要求；`[官方]†` = 官方语料里的背景/经验陈述，**不承载硬性要求**；`[社区]` = **查不到官方原文，本项目自定口径**。

| # | 官方依据指针 | 分级 |
|---|---|---|
| Q1 | `instructions.html:1131`；`20YearsofGoodAdvice.txt:150-152`、`:310-312`；`UMAP-2003-judges-commentary.txt:6460-6461`、`:6473` | `[官方]` / `[官方]†` |
| Q2 | `instructions.html:1132`；`UMAP-2003-judges-commentary.txt:6469-6471`；`20YearsofGoodAdvice.txt:162` | `[官方]` / `[官方]†` |
| Q3 | `instructions.html:1132`；`UMAP-2003-judges-commentary.txt:6560-6563`；`20YearsofGoodAdvice.txt:157-159` | `[官方]` / `[官方]†` |
| Q4 | `20YearsofGoodAdvice.txt:160-161`、`:162` | `[官方]†`（背景/经验语料，不承载硬性要求） |
| Q5 | `20YearsofGoodAdvice.txt:164-165`、`:318-321` | `[官方]†` |
| Q6 | `20YearsofGoodAdvice.txt:160`（"the summary should not be overly technical"） | `[官方]†` |
| Q7 | `UMAP-2003-judges-commentary.txt:6565-6568`；`instructions.html:1165` | `[官方]` |
| Q8 | **无官方原文**；最近的是 `20YearsofGoodAdvice.txt:249`（sanity check） | `[社区]`（本项目口径） |
| Q9 | **无官方原文**；最近的是 `20YearsofGoodAdvice.txt:249`；`Contest_AI_Policy.txt:60-61`（仅 AI 场景） | `[社区]`（本项目口径） |
| Q10 | `UMAP-2003-judges-commentary.txt:6473`；`20YearsofGoodAdvice.txt:150-152`、`:310-312`；`instructions.html:1162` | `[官方]` / `[官方]†` |
| Q11 | `faq.html:270`；`INDEX.md §2.2.2`、`§2.2.3`（`instructions.html:955`、`1227`） | `[官方]` |
| Q12 | 空话套话：`instructions.html:1132`；`20YearsofGoodAdvice.txt:311`。**"无未验证比较级"无官方原文** | `[官方]` + `[社区]` |
| Q13 | `instructions.html:1130`；`UMAP-2003-judges-commentary.txt:6465-6468`；`20YearsofGoodAdvice.txt:152-155` | `[官方]` / `[官方]†` |

> 原文附注（逐字）："Q1–Q3、Q7、Q11、Q13 的官方句同时在 `INDEX.md §2.2` 有登记
> （`instructions.html:1126-1132` 那一小节的逐条拆解），可直接引 `§2.2.6-2.2.8`。"

## 四、与 controller 的描述不符 / 请求裁量的点 —— 照抄 + 状态

> **读法提醒（重要）**：下表「已裁」一栏的判定依据是 **`SKILL.md` 已落定的措辞**（controller 的落地件，
> 即裁决的**结果**），**不是**一段独立的裁决文字——本次落库**没有**在盘上找到"逐条裁决"的独立记录。
> 若 controller 认为某条其实未裁，**以你手里的记录为准**；凡标「待裁」的，本文件保持原样、未作任何推断性改写。

原文里**明确请求裁量 / 自陈口径是本项目自定**的地方共 6 处，状态如下：

| # | 原文位置 | 原文原话（节录，逐字） | 状态 | 依据 |
|---|---|---|---|---|
| 1 | §3-Q8 末句 | "**本条的"每个数字回指正文"口径是本项目自定**，请据此决定去留。" | **已裁：保留，且加严到含"具名归属"** | `SKILL.md` 规格行："数字与**具名归属**都要能回指正文（实测有摘要写出正文未出现过的国名）" |
| 2 | §6-顾虑 1（Q3/Q4） | "**建议你确认这两条的限定语怎么写**" | **已裁：按字面口径，两条均维持"规格"** | `SKILL.md` 规格行按字面口径落定："不**逐字**搬引言——改写后能独立成立即合规"；"方法不罗列，每项附'用它做了什么'" |
| 3 | §6-顾虑 2（Q12） | "若你不接受，Q12 只剩"比较级"子项…**那么 Q12 应整条降为规格**" | **已裁：不降级**（维持 ★） | `SKILL.md` 仍以 ★ 列"措辞克制"，含"自评式套话"与"未验证比较级"**两个**子项 |
| 4 | §6-顾虑 3（Q9 是否计入 `0.359`） | "**Q9 我刻意没有把 0.359 计入**…若你要更严的口径…A1/A2 改判 0" | **已裁：维持不计入** | `SKILL.md` 第 6 条的"两步查法"只举 `RSA=0.02<0.05` 反向与 `G=700N` vs `616N` 两例，未含 `0.359` |
| 5 | §6-顾虑 4（Q11 是词数推断） | "**Q11 是词数推断，不是编译验证**…建议注明"按 12pt 单页估算"" | **已裁：口径已换成编译实测**，并新增余量要求 | `SKILL.md` ★简洁行："实测 6/6 份超页：856–1319 词 → **编译均 2 页**"+"**别刚好填满**…留几行余量" |
| 6 | §6-顾虑 5（A3/P1 正文版本不同） | "**A3 与 P1 的正文不是同一份**…若不区分正文版本，A3/P1 会被误判" | **无需裁**（评分口径说明；原文已按各自正文判） | 原文 §0 已写明三种正文的对应关系；`abs-cases/README.md` 记 `case-A-body-partial.md` 是合成输入 |

**另**：原文 §5 列了 12 条"清单外发现"（读产物时看到的真实缺陷）。它们**未被逐条裁决**；其中 3 条与 skill 落地有关，
落点如下（**未**裁的即维持原样、不作推断）：

| 原文 §5 条目 | 落点 |
|---|---|
| §5-① `[0.359, 0.996]` 下界不可复现 | **未进 skill**；与上面第 4 条同一件事（顾虑 3 已裁"不计入 Q9"） |
| §5-④ C1 的国名归属不可回指 | **已进 skill**：规格行"数字与**具名归属**都要能回指正文" |
| §5-⑦ P1 未披露 Task 2 结果不存在 | **已进 skill**：★"结果没出来就显式标缺，别用方法描述充数"（并给了句式示例） |
| §5 其余 9 条 | **未见裁决记录 → 待裁**（本文件原样保留） |
| §5-⑫、§3-Q10 的"A1 做法说明与摘要实况不符" | 属**对产物自述的采信警告**，不影响摘要本身 → **待裁**（如需） |

---

## 勘误记录（复审后按产物复核更正）

本副本在入库后按部署前复审结论做了 4 处更正。**每条都给复核命令，改的是"说法"，不是分数矩阵**：
13 条的 0 分次数与归属（★/规格）**一条都没动**。

| # | 位置 | 改了什么 | 复核命令 |
|---|---|---|---|
| ① | §2-Q2 的"一句话理由"栏 **与** §3-Q2 | 原标 `P1 = 0` 的那段 `**The questions.** …` **更正为 `P2 = 0`**（逐字在位）；**两处**都补上 P1 的可用证据并标注为边界 | `grep -c 'The questions' tests/skills/abs-cases/red/red-P1.md` → `0`；`grep -n 'The questions' tests/skills/abs-cases/red/red-P2.md` → `12` |
| ② | §3-Q11 | **删除** 6 个口径不可复现的字符数（5437/6861/7885/8215/6491/5511），**保留**词数并补上可复现口径 | 见 §3-Q11 的复现一行命令 → `856/1130/1318/1319/1031/916` |
| ③ | §二 | 「★ 行 **8** 条」更正为 **7 条** | `grep -c '^★' .claude/skills/mcm-abstract/SKILL.md` |
| ④ | 头注 | 增加本表（原头注声称"一个字都没动"，已不再成立） | — |

## 入库校验

**入库时**本文件 = 头注 + `build/abs-red/quality-score.md` 全文；该逐字节后缀校验**现已失效**
（正文经上表 4 处勘误）。入库当时的校验方法与结果如下，留档：

```
python - <<'PY'
src = open('build/abs-red/quality-score.md','rb').read()
new = open('tests/skills/mcm-abstract-quality-rubric.md','rb').read()
print('逐字节后缀一致 =', new.endswith(src))
PY
```

入库当时输出 `逐字节后缀一致 = True`；**勘误后该断言不再成立，别再用它校验本文件**。
现在能校验的是**分数矩阵本身**：§1 的 0 分次数一览（Q1 0/6 … Q13 0/6）与 §2 的逐条判定，与本文任一版本一致。

---

<!-- ↑↑↑ 以上为入库头注；以下为 `build/abs-red/quality-score.md` 的逐字全文 ↑↑↑ -->

# 摘要页质量清单 —— 6 份基线产物逐条打分

评分员记录，2026-09-27。目的：判断清单 13 条**是否真的在这 6 份基线里失败过**，以决定每条写成「指导」还是只当「规格/判分项」。

## 0 口径与读物

- **产物**：`tests/skills/abs-cases/red/`（= `build/abs-red/` 同内容）下的 `red-A1.md`、`red-A2.md`、`red-C1.md`、`red-A3-partial.md`、`red-P1.md`、`red-P2.md`。每份只评 `## Summary` 正文（英文摘要），`## 我的做法说明` 只作为作者自述供参考、不计分。
- **判"数字能否回指"时用的正文**：`case-A-body.md`（A1/A2/P2）、`case-A-body-partial.md`（A3/P1，该正文**没有** §4.2 的区间数值、§4.5 的拟合式与 1.14）、`case-C-body.md`（C1）。题面：`case-A-problem.txt`、`case-C-problem.txt`。**这一点很关键**：A3/P1 不给 Task 2 数字是与其正文相符的行为，不是遗漏。
- **打分纪律**：每个 0/1 都能指到产物里的原句或"通篇未见"。证据不足或该条在这份产物上没有适用对象 → N/A 并写明原因。
- **页码**：本机无法编译，所以"一页"只能按词数估。口径：12pt 正文、常规页边距的 A4/Letter 单页约容 500–650 英文词（含标题与小标题）。实测词数见 Q11。

---

## 1 分数矩阵（列＝条目，行＝产物）

| | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Q11 | Q12 | Q13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A1** | 1 | 1 | 1 | 1 | 1 | **0** | **0** | 1 | 1 | 1 | **0** | 1 | 1 |
| **A2** | 1 | 1 | 1 | 1 | 1 | **0** | **0** | 1 | 1 | 1 | **0** | **0** | 1 |
| **C1** | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | **0** | 1 | **0** | **0** | 1 |
| **A3**（partial） | 1 | 1 | 1 | 1 | 1 | **0** | **0** | 1 | N/A | 1 | **0** | **0** | 1 |
| **P1** | 1 | **0** | 1 | 1 | 1 | **0** | **0** | 1 | **0** | 1 | **0** | **0** | 1 |
| **P2** | 1 | **0** | 1 | 1 | 1 | **0** | **0** | 1 | **0** | 1 | **0** | 1 | 1 |
| **0 分次数** | 0 | 2 | 0 | 0 | 0 | 5 | 5 | 0 | 3 | 0 | 6 | 4 | 0 |

---

## 2 逐条结论（0 分计数 → 指导 or 规格）

| # | 条目 | 0 分次数 | 判定 | 一句话理由 |
|---|---|---|---|---|
| Q1 | 最重要的结论在摘要里 | 0/6 | **规格/判分项** | 6 份全都把 Task 1 的定量结论（261 人/天、约 100 年、三峰、3:2）或 C1 的预测表摆在了显眼位置；**没有一份**只写"我们做了很多"。 |
| Q2 | 不复述题面 | 2/6 | **指导** | **P2** 有一个独立成段的 `**The questions.**`，功能就是重列题面问句（**「已按产物复核更正」：原稿此处写"P1、P2 各有一个"，但该段逐字只在 `red-P2.md:12-15`，`red-P1.md` 命中 0**）；**P1** 则把所问三件事写进首段的动机句、并以"each requested judgement"整体指代题面所问（边界，见 §3-Q2）；C1 的首段也复述了题面 Table 1 与四个 Task（判 1，见 §5 顾虑）。 |
| Q3 | 不搬引言 | 0/6 | **规格/判分项** | 按本条的限定语（"无引言原句的成段搬运"）搜引言特征句（`the stone is not impervious`、`waiting to be explored`、`molded into different shapes that tell stories of the past`），**6 份通篇未见**。但见 §5-⑩：P1/P2 的首段在功能上就是引言那两段的改写。 |
| Q4 | 方法不罗列（每项附"用它做了什么"） | 0/6 | **规格/判分项** | 6 份的每一项方法后面都跟了用途（WDM=数车道/分上下行、最小二乘=拟合 Q–σ、蒙特卡洛=不确定度区间）。**"每项附用途"这个口径下 0 失败**；官方 20YGA:160-161 真正反对的"技术清单体"另有落点，见 §5-⑬。 |
| Q5 | 不按时间顺序记流水账 | 0/6 | **规格/判分项** | 6 份摘要正文**通篇未见** "first we… / then we… / finally we…" 式时序叙述；组织方式都是按模型部件（WVM/WDM）或按 Task。 |
| Q6 | 不过度技术 | **5/6** | **指导** | 五份把主方程、Archard 式、硬度衰减式、混合分布符号直接排进第 1 页（A1/A2/A3/P1/P2）；只有 C1 没有独立公式行。 |
| Q7 | 逐问作答 | **5/6** | **指导** | 题面 Task 2 第一问（"Is the wear consistent with the information available?"）在 A1/A2/P2 里**只给了判据、没有判定**（正文 §4.1 本身也没有 P_A 的取值）；A3/P1 的整块 Task 2 五问都无结论。只有 C1 逐问有对应答案。 |
| Q8 | 每个数字都能回指正文 | 0/6 | **规格/判分项** | 逐份把摘要里出现的每个数在正文中 grep 到出处（清单见 §3-Q8），**没有一份出现"正文里没有的数"**；数字与正文最大偏差是四舍五入。唯一瑕疵是 C1 的国名归属（§5-④），但它不构成"正文里没有的数"。 |
| Q9 | 数字自洽 | **3/6** | **指导** | A1/A2 显式剔除了正文自相矛盾的 1.14 与 §4.3 的 0.02；P2 把 1.14 带进来了；P1 把 `W = 62.8 kg` 与 `G ≈ 700 N` 并入同一句（正文自己写 G=Wg）；C1 把"点估计＝自己 97.5 分位"的两列照抄。 |
| Q10 | 具体而非自评 | 0/6 | **规格/判分项** | 6 份都在用数字/区间说话，**没有一份**写"我们的模型很全面/很稳健"这类纯自评。最接近的是 A3/P2/P1 各一句"robust/在相关时间窗内稳健"的收尾，但都紧跟在数字之后，且属官方要求的优缺点陈述。 |
| Q11 | 简洁（一页能装下） | **6/6** | **指导** | 实测词数 856 / 1130 / 1318(+10 行表) / 1319 / 1031 / 916，**六份全部超过单页 12pt 的容量**；P2 自己写了"约 800 词，排成 A4 一页偏满"并给出砍法。 |
| Q12 | 措辞得当 | **4/6** | **指导** | "无未验证比较级"这一半 **0 失败**（better/faster/superior/outperform 6 份通篇未见）；失败的是"自评式套话"：A2/C1/A3/P1 各有一句把"本文写得多诚实/多克制"写进摘要。 |
| Q13 | 读者导向 | 0/6 | **规格/判分项** | 6 份都有动机句 + 亮点（A1 "Stone outlasts the people who walk on it"、C1 "only the top two are safe to forecast confidently" 等），读完都能判断该不该读正文。 |

**结论速览**：清单里真正在基线失败过的有 **6 条**（Q2、Q6、Q7、Q9、Q11、Q12），其中 Q6/Q7/Q11 近乎全灭；**7 条一次都没失败**（Q1、Q3、Q4、Q5、Q8、Q10、Q13）→ 只当规格/判分项，写成"指导"没有基线证据支撑。

---

## 3 逐条依据（官方指针）+ 打分证据

### Q1 最重要的结论在摘要里 —— 依据 `[官方]`
- `instructions.html:1131`（"most prominently, your most important conclusions"）；`20YearsofGoodAdvice.txt:150-152`（"it needs to be clear and contain results"）、`:310-312`（"should state the results that you obtained, not just what you did"）；`UMAP-2003-judges-commentary.txt:6460-6461`（"contain the bottom-line answer or result"）、`:6473`。
- 证据（6 份各一句结果句）：A1 "The WVM gives an average **N_d = 261 person-passes per day**"；A2 "**N_d ≈ 261 passages per day** for a stair built roughly a century ago"；C1 预测表 "+ 4.78 new medal-winning countries"；A3 "$N_d\approx261$ people per day"；P1 "yields a usage frequency of **N_d ≈ 261 people per day**"；P2 "roughly 261 people per day if the stair is about one century old"。

### Q2 不复述题面 —— 依据 `[官方]`
- `instructions.html:1132`（"mere restatements of the contest problem … are generally considered to be weak"）；`UMAP-2003-judges-commentary.txt:6469-6471`；`20YearsofGoodAdvice.txt:162`（"Don't merely restate the problem, but indicate how it is being modeled and what was learned from the model"）。
- **P2 = 0**：`**The questions.** From a single non-destructive survey of a worn stair we are asked to recover how often it was used, which direction of travel was favoured, and how many people climbed abreast; and then, using whatever dating and documentary information exists, to say whether the wear is consistent with that information, how old the stairwell is and how reliable that age is, whether it has been repaired, where its material came from, and whether its traffic came from many people over a short time or few people over a long time.` —— **逐字命中 `red-P2.md:12-15`**（独立成段、只做重列问句）。**「已按产物复核更正」：本段原被标为 `P1`，复审实测在 `red-P1.md` 命中 0，逐字只在 `red-P2.md` 命中（复核命令见文末「勘误记录」）。**
- **P1 = 0**（边界；证据弱于 P2，如实登记）：P1 没有 `**The questions.**` 那种独立重述段，它复述题面的方式是**把所问三件事写进首段的动机句**（"The bowed centres of ancient temple steps measure something no chronicle recorded: **how many people passed, in which direction, and how many abreast**"，`red-P1.md:7`）＋ `**Guidance for the further questions.**` 段以"**each requested judgement**"整体指代题面所问（`red-P1.md:48`）。若按"必须有独立重述段"的严口径，P1 可改判 1 —— 本次维持 0，与方法论一致（复述题面即使嵌在动机句里也算），但证据强度低于 P2。
- A1/A2/A3 = 1：三份的首段都直接给"模型做什么"，没有重列题面问句；A2 那句 "we recover the frequency of use … we then extend the same model to test the wear record for consistency, to date the stairwell …, to detect past repairs …" 是把题面问句改写成**交付物清单**，不是独立的重述段（这条判 1，但属边界）。
- C1 = 1（边界）：首段 "We ask what the same data implies for Los Angeles 2028: how many medals each country will win, how precisely that can be known, how many nations will win their first-ever medal, and how much of the outcome is governed by programme design and coaching rather than by athletes alone." —— 复述了四个 Task，但压在一句里、且紧接方法与结果，未独立成段。若按逐句从严可判 0。

### Q3 不搬引言 —— 依据 `[官方]`
- `instructions.html:1132`（"cut-and-paste boilerplate from the Introduction"）；`UMAP-2003-judges-commentary.txt:6560-6563`（"A large number of teams simply copied and pasted their introductory paragraphs"）；`20YearsofGoodAdvice.txt:157-159`。
- 证据：在 6 份产物里 grep 引言特征句（`impervious`、`permanence`、`waiting to be explored`、`tell stories`、`molded into`、`temporal variability`）→ **通篇未见**（唯一命中 `impervious/waiting to be explored` 的是 P2 的 `## 我的做法说明` 自述，不属摘要正文）。
- 另注：题面/引言的合规措辞被 5 份近乎原样搬进摘要（A1:69 "obtained with minimal tools by a small team and without touching the fabric"、A2:20 "obtainable by a small team, with minimal tools, at low cost, and without damaging the structure"、A3:5、P1:8/37、P2:37-38），源句见 `case-A-problem.txt:12` 与 `case-A-body.md:35-36`。这是"复述题面"的变体，属 Q2 家族，不属 Q3 的原文搬运。

### Q4 方法不罗列 —— 依据 `[官方]†`（背景/经验语料）
- `20YearsofGoodAdvice.txt:160-161`（"A long list of techniques can obscure your results; it is better to provide only a quick overview of your approach"）；`:162`（"indicate how it is being modeled"）。
- 证据（每项都带用途）：A1 "The **Wear Volume Model (WVM)** links wear to time, traffic and material"；A2 "Integrating the wear field over the tread yields an average depth and closes the system in either direction"；A3 "Solving the WVM for T and N_d shows that the observed wear is a one-parameter family"；C1 "Monte Carlo resampling converts those allocations into prediction intervals"；P1 "component *count* is the number of parallel lanes, the *means* locate those lanes across the tread"；P2 "we fit the relation between traffic volume and lateral spread by least squares"。
- 边界提醒（不算 0，但值得写进指导）：P2 有独立成段的 `**The methods.**`，四样技术并列一句；C1 把四种方法压进一句。这两处最接近 20YGA 说的"技术清单体"。

### Q5 不流水账 —— 依据 `[官方]†`
- `20YearsofGoodAdvice.txt:164-165`（"not a chronological description of what you did"）、`:318-321`（时序性无人物被动叙述同样是病）。
- 证据：6 份摘要正文 **通篇未见** 时序连接词式的过程叙述；结构分别是"部件→结果→延伸→稳健→结论"（A1/A2/A3/P1/P2）或"Task1→Task2→Task3→Task4→洞见"（C1）。所有句子的主语都是 "we/our model"，不是"it was found that"式被动（20YGA:318-321 的另一半也没踩）。

### Q6 不过度技术 —— 依据 `[官方]†`
- `20YearsofGoodAdvice.txt:160`（"the summary should not be overly technical"）。
- **0 分证据**：A1 `d(x,y) = T · N_d · D(x,y) · G · k_m`、`k_m = K·d/H`、`H(t) = H₀e^(−pt)`、`D(x,y) = D_X(x)·D_Y(y)`、下标 `N_d / k_m / P_A / σ_H / H_t / H_test`；A2 `*d(x,y) = T · N_d · D(x,y) · G · k_m*`、`*T = A·d_avg /(N_d·G·k_m)*`、`*D_y ~ w_up·N(μ_up,σ_up) + w_down·N(μ_down,σ_down)*`、`ε = 1e−3`；A3 直接排 `$$d(x,y) = T\cdot N_d\cdot D(x,y)\cdot G\cdot k_m,$$` 与 `$k_m = K d / H$`、`$H(t)=H_0e^{-pt}$`；P1 `*d(x, y) = T · N_d · D(x, y) · G · k_m*`、`*k_m = K · d_s / H*`；P2 `k_m = K·d/H`、`N_pass = 0.339·e^(0.13125·σ_x) + 0.92338`。
- **C1 = 1**：无独立公式行，符号只剩 `P = P|a + P|c + ε`、`β₁`、`R²`、`ROC-AUC/PR-AUC`，且都直接挂在结果数上。

### Q7 逐问作答 —— 依据 `[官方]`
- `UMAP-2003-judges-commentary.txt:6565-6568`（"The biggest thing that caught the judges' eye was whether or not the team paid attention to the questions asked in the problem … they got cut quickly"）；`instructions.html:1165`（结论须明确报告结果）。
- **A1 = 0**：题面第二组的"一致性"问只有判据 —— "*Consistency*: we compare the wear predicted from the available record with the measured field through a log-ratio divergence P_A, whose absolute value measures disagreement." 全篇无 P_A 值、无"一致/不一致"的判定；且 `case-A-body.md` §4.1（:594-613）本身也只定义不求解，**这一问在整篇论文里就没有被回答**。
- **A2 = 0**：同问 —— "an a-priori wear matrix built from the historical record is compared with the measured one through a log-ratio agreement statistic; a larger magnitude means the two disagree."（其余 Task 2 各问都有数值。）
- **A3 = 0**：Task 2 五问全部由占位段兜住 —— `> **[PENDING — the numerical results of Task 2 have not yet been produced.]**`。
- **P1 = 0**：五条都只给 "*decision rule with an explicit threshold*"，无一条给结论；且**未披露**结果缺失（其做法说明："我没有填任何数字。"）。
- **P2 = 0**：同 A1 的一致性问 —— "Consistency of wear with the record is tested by a log-ratio measure P_A between the measured and the information-predicted wear matrices."
- **C1 = 1**：Task 1（表+"most likely to improve"）、Task 2（4.78 与候选国）、Task 3（β₁、host effect）、Task 4（三国建议）、原创洞见都有对应句子。唯一偏弱的是 "What sort of odds do you give to this estimate?" 用 Samoa 的 0.406→约 2:3 回答，整体估计只给了定性说明（C1 在做法说明里解释了为什么）。

### Q8 每个数字都能回指正文 —— 依据 `[社区]`（**查不到直接的官方原文**）
- 最接近的官方表述只有 `20YearsofGoodAdvice.txt:249`（"Verify as much as you can. Make sanity checks"）与 `Contest_AI_Policy.txt:60-61`（队须核验并改正错误与不一致，但那是 AI 使用政策下的义务，不是摘要写作要求）。**本条的"每个数字回指正文"口径是本项目自定**，请据此决定去留。
- 证据（逐份核过，全部命中）：A1 `261 / 36492 / 0.30,1.10,1.76 / 3:2 / 0.08,0.15 / 0.359,0.996 / RS=0.03 / σ_H=1.8 / 89.45 / 90.44 / 93.18 / η=3.0% / R²=0.9999 / <0.01% / 10⁸ footfalls over a century`（"Each stair is stepped 100 million times in 100 years"，`case-A-body.md:796`）；A2 `36,500 天 / ~48% / 64% / <0.01% / 25% / ε=1e−3 / T=A·d_avg/(N_d·G·k_m)`（式 3.9/3.10，`:290-295`）；A3 `H=95 / 261 / 36 500 / 0.30,1.10,1.76 / 3:2 / 0.08,0.15 / 64.2% / 0.0025→0.005 / <0.01% / 18,24,95,175`；C1 `142/113/69… / 4.78 / 4–7 / 0.1912 / 21.1% / 1.91–3.82 / 0.2378 / 0.1626 / 92.33 / 0.18–0.20 / 0.2305 / 0.1273 / +74.8 / +24.7 / 0.539 / 0.854 / 0.974,0.983 / 0.926,0.639 / 1.16 / 1.33 / 1.67` 全部在 `case-C-body.md` 命中；P1 `261 / 36,492 / 0.30,1.10,1.76 / 3:2 / 0.08,0.15 / W=62.8 / G≈700 / granite H_0=175`（partial 正文 `:264`、`:496`、`:891`）；P2 `261 / 36492 / 三峰 / 3:2 / 0.08,0.15 / σ_H=1.8 / 89.45 / 90.44 / 93.18 / η=3.0% / R²=0.9999 / N_pass=0.339e^{0.13125σ_x}+0.92338 / 1.14 / 48.1%,43.6%,64.2% / 0.001–0.006%`。
- 瑕疵（不构成"正文里没有的数"，但见 §5-④）：C1 的候选国名 `Samoa / Mali / Guam / Papua New Guinea / Vanuatu` 在 `case-C-body.md` **通篇未见**；正文只有一串裸概率值（`:488-500` 的 `0.406 / 0.266 / 0.254 / 0.242 / 0.242`）。若你要的口径是"数字**及其归属**都能回指"，C1 应判 0。

### Q9 数字自洽 —— 依据 `[社区]`（**查不到直接的官方原文**）
- 只能挂到 `20YearsofGoodAdvice.txt:249`（sanity check）与 `Contest_AI_Policy.txt:60-61`（改正文里的错误与不一致）。**本条的"不许把正文里那个自相矛盾的数带进摘要"是本项目口径**。
- A1 = 1：显式剔除 —— "**§4.5 的'1.14 people walking side by side'** … 第 1 页上摆一个自相矛盾的数字，等于把最大的把柄递给评委，所以我只保留三峰"；"**§4.3 结论里的 "RSA = 0.02 < 0.05"** … 因此摘要里只写定性结论 + 两组自洽的数字"。
- A2 = 1：显式剔除同类项 —— "我保留了回归形式和 `R² = 0.9999`，但**没有**写 1.14 这个数"；"只写结论'判定未修缮'，不重述阈值"。
- C1 = **0**：表格里 `| USA | 126 | 142 | 113 – 142 | 37 – 53 |` —— 点估计 142 恰为自己的 95% 区间上界；C1 自己写了"点估计落在自己的 97.5 分位上不正常"，但"两列都照抄了"。
- A3 = **N/A**：其正文（`case-A-body-partial.md`）里既没有 1.14，也没有 §4.2 的区间数值（grep `1.14`/`0.9999`/`0.359` 均无命中），本条在这份产物上没有适用对象。
- P1 = **0**："The loading term *G* is not a guess: it is the population-weighted expectation of body weight over six demographic groups using WHO weight data, giving *W = 62.8 kg* and *G ≈ 700 N*." —— 其正文自己写 `G = W ·g`、`g = 9.81`（partial 正文 `:272-274`）且 `W = 62.8 kg`（`:264`），700 N 只孤立出现在 Table 4（`:496`）。P1 把这一对互斥的数并进同一句，做法说明里也没察觉（A2/P2/A3 都察觉了）。
- P2 = **0**：同一页上 `people walked three abreast` 与 `gives about 1.14 people abreast on the Edinburgh step` 并列；P2 自己的做法说明承认"并排人数自相矛盾"。

### Q10 具体而非自评 —— 依据 `[官方]`+`[官方]†`
- `UMAP-2003-judges-commentary.txt:6473`（"Put the 'bottom line results and managerial recommendations' in the summary"）；`20YearsofGoodAdvice.txt:150-152`、`:310-312`；`instructions.html:1162`（优缺点须讨论，故 A2/P2 的"strength/weakness"一句不算自评）。
- 证据：6 份的结论段都带数（A1 `[0.359,0.996]`、A2 `R²=0.9999`、A3 `64.2%`、C1 `+74.8`、P1 `N_d≈261`、P2 `η=3.0%`）；**通篇未见**"我们的模型很全面/很稳健/很精确"式纯自评。
- 两处可写进指导的弱化（不判 0）：A1 的硬度敏感性句无数字（"Wear accumulation is sensitive to material hardness, as it must be for hardness to be usable as a provenance discriminant"，正文有 48.1%），而 A1 的做法说明却自称这一节是"**带数字的**陈述"——自述与摘要不符；P1 的 Validation 段整段无数字。

### Q11 简洁 —— 依据 `[官方]`
- `faq.html:270`（"it must be on a single page with a readable font (12)"）、`INDEX.md §2.2.2`；字号见 `INDEX.md §2.2.3`（`instructions.html:955`、`1227`）。
- 证据（词数）：A1 **856**；A2 **1130**；C1 **1318**（另加一张 10 行 × 5 列表）；A3 **1319**；P1 **1031**；P2 **916**，且 P2 自己写"**这版约 800 词，排成 A4 一页偏满**"，并给出"要压到一页就砍这两处"的清单。→ 六份都不止一页。
- **口径（复审补记，可复现）**：从文件**第一行**到 `## 我的做法说明` **之前**（不剥 `---` 分隔线）的 `wc -w`。复现：`python -c "import sys;t=open(sys.argv[1],encoding='utf-8').read();print(len(t[:t.find('## 我的做法说明')].split()))" tests/skills/abs-cases/red/red-A1.md` → `856`。六份依次 **856 / 1130 / 1318 / 1319 / 1031 / 916**（与上表逐位相符）。
- **字符数已删**：原稿另给了 6 个字符数（5437 / 6861 / 7885 / 8215 / 6491 / 5511）。复审穷举 14 种切片定义、本次又试多种（含 `len()` / `strip()` / `\s+` 归一 / 逐对 CRLF 假设）**无一命中**，**口径不可复现** ⇒ 按"不许把说不出口径的数留在那里"**删除**，只留可复现的词数。（供参照：按上面同一口径的 `len()` 分别是 5471 / 6871 / 7832 / 8228 / 6530 / 5549 —— 与原数不是同一个量，勿混用。）

### Q12 措辞得当 —— 依据：空话套话 `[官方]`；"无未验证比较级" `[社区]`
- 官方依据：`instructions.html:1132`（弱摘要 = 重述题面或套话）；`20YearsofGoodAdvice.txt:311`（"state the results that you obtained, not just what you did"）。**"无未验证的比较级（better/faster/superior）"查不到官方原文，是本项目口径**。
- 子项一（比较级）：6 份 **通篇未见** `better/faster/superior/outperform/more accurate` 这类词 → 0 次失败。
- 子项二（自评式套话）0 分证据：A2 "with an explicit and **honest** statement of how far the dating can be trusted" / "we report it as such rather than as a point estimate"；C1 "Monte Carlo resampling turns them into **honest** intervals"；A3 "The model is therefore robust in the regime where it is meant to be used, and **honest about where it is not**"；P1 "we report the model's reliability as a function of the time horizon rather than as a single number"（摘要里既没给这个函数、也没给数字）、"instead of an unqualified opinion"、"The loading term *G* is not a guess"。
- A1 = 1、P2 = 1：A1 无自评句；P2 的 "Its strength is that … its principal weakness is that …" 对应 `instructions.html:1162` 要求的优缺点陈述，不算套话。

### Q13 读者导向 —— 依据 `[官方]`
- `instructions.html:1130`（"imagine that a reader will choose whether to read the body of the paper based on your summary"）；`UMAP-2003-judges-commentary.txt:6465-6468`；`20YearsofGoodAdvice.txt:152-155`。
- 证据：6 份都有动机句 + 亮点句（A1 "Stone outlasts the people who walk on it, but not without record."；A2 "A staircase is an instrument that has already been running for centuries."；C1 "only the top two are safe to forecast confidently"；A3 "Historical records can tell an archaeologist roughly when a staircase was built, but they rarely say how it was used"；P1 "Worn stairs are one of the few archaeological records that is written by ordinary people rather than by their rulers."；P2 "Even stone yields to feet."）。读完都能判断该不该读正文。

---

## 4 逐条依据一览（可直接抄进清单）

| # | 官方依据指针 | 分级 |
|---|---|---|
| Q1 | `instructions.html:1131`；`20YearsofGoodAdvice.txt:150-152`、`:310-312`；`UMAP-2003-judges-commentary.txt:6460-6461`、`:6473` | `[官方]` / `[官方]†` |
| Q2 | `instructions.html:1132`；`UMAP-2003-judges-commentary.txt:6469-6471`；`20YearsofGoodAdvice.txt:162` | `[官方]` / `[官方]†` |
| Q3 | `instructions.html:1132`；`UMAP-2003-judges-commentary.txt:6560-6563`；`20YearsofGoodAdvice.txt:157-159` | `[官方]` / `[官方]†` |
| Q4 | `20YearsofGoodAdvice.txt:160-161`、`:162` | `[官方]†`（背景/经验语料，不承载硬性要求） |
| Q5 | `20YearsofGoodAdvice.txt:164-165`、`:318-321` | `[官方]†` |
| Q6 | `20YearsofGoodAdvice.txt:160`（"the summary should not be overly technical"） | `[官方]†` |
| Q7 | `UMAP-2003-judges-commentary.txt:6565-6568`；`instructions.html:1165` | `[官方]` |
| Q8 | **无官方原文**；最近的是 `20YearsofGoodAdvice.txt:249`（sanity check） | `[社区]`（本项目口径） |
| Q9 | **无官方原文**；最近的是 `20YearsofGoodAdvice.txt:249`；`Contest_AI_Policy.txt:60-61`（仅 AI 场景） | `[社区]`（本项目口径） |
| Q10 | `UMAP-2003-judges-commentary.txt:6473`；`20YearsofGoodAdvice.txt:150-152`、`:310-312`；`instructions.html:1162` | `[官方]` / `[官方]†` |
| Q11 | `faq.html:270`；`INDEX.md §2.2.2`、`§2.2.3`（`instructions.html:955`、`1227`） | `[官方]` |
| Q12 | 空话套话：`instructions.html:1132`；`20YearsofGoodAdvice.txt:311`。**"无未验证比较级"无官方原文** | `[官方]` + `[社区]` |
| Q13 | `instructions.html:1130`；`UMAP-2003-judges-commentary.txt:6465-6468`；`20YearsofGoodAdvice.txt:152-155` | `[官方]` / `[官方]†` |

> Q1–Q3、Q7、Q11、Q13 的官方句同时在 `INDEX.md §2.2` 有登记（`instructions.html:1126-1132` 那一小节的逐条拆解），可直接引 `§2.2.6-2.2.8`。

---

## 5 清单外发现的质量问题（读产物时看到的真实缺陷）

1. **区间下界 0.359 与正文自己的公式对不上，且 A1/A2/P2 三份都带进了摘要。**
   `case-A-body.md:640-654` 给 `CIinf = [1 + (RC+1)/(RA·F_{1−α/2}(2RA, 2(RC+1)))]^{-1}`，同页给 `α=0.05`、6 级台阶中 5 级合格（RA=5, RC=1）。代入得 `[1 + 2/(5·F_{0.975}(10,4))]^{-1} ≈ [1+2/(5×8.84)]^{-1} ≈ 0.957`；要得到 0.359 需 `F ≈ 0.22`，不可能。同页 `CIsup = [1+1/(6·F_{0.975}(12,2))]^{-1} ≈ 0.996` 反而对得上。P2 的独立结论一致（"代入约得 0.96"）。→ 摘要里的 `[0.359, 0.996]` 含一个不可复现的数。（本项我**未**据此扣 Q9，理由见"顾虑"。）
2. **A2 把 20 年时程写成 "long-run"**：正文是"wood hardness 下降 25%，**20 年后**再增 48.1%"（`case-A-body.md:881-882`），A2 写成 "a 25% loss of initial hardness changes **long-run** wear by ~48%"。同一份产物在做法说明里恰好把"数字要能回指正文"列为自己的筛子，此处是时程标签抄错（P2 写成 "raises **twenty-year** wear by 48.1%" 才对）。
3. **A2 加了一处正文没有的方法细节**："（obtained, for example, by 3D reconstruction from **photographs plus a depth reference**）"；正文只说 "Based on the 3D reconstruction of the image"（`:486-487`），没有照片与深度基准。
4. **C1 的国名归属不可回指**：`Samoa / Mali / Guam / Papua New Guinea / Vanuatu` 在 `case-C-body.md` 通篇未见（该文件通篇 grep 无命中），正文只有一串裸概率 `0.406 / 0.266 / 0.254 / 0.242 / 0.242`。摘要把一个无法在正文文本里核对的"国名↔概率"对应关系当成结论写了出来。
5. **C1 的"区间宽度随国力变宽"与自己那张表冲突**：摘要写 "The intervals are tight for the established powers (USA, CHN, GBR) and progressively wider for mid-sized programmes"。按绝对宽度算：NED 16 < GER/JPN 18 < FRA/AUS/ITA/CHN 20 < GBR 23 < **USA 29**；即美国最宽、多个中小国比英/美都窄。只有按**相对**宽度（PI 宽度÷点估计）才勉强成立，且 GBR（33%）与 FRA（34%）几乎无差别。
6. **P1 把 σ 的方向说错**：正文的"人数–离散度"拟合对象是 **X 向（横向）**边缘分布的 σ（`case-A-body-partial.md:802-804` "a normal distribution with a small variance is likely to emerge in the X-direction"、`:840` "from the edge distribution of the measurement matrix D_x^measure"），P1 写成 "the **longitudinal** spread σ of the wear field"。这与 P1 同一段里"X 向峰数＝并行人数"的用法自相矛盾。
7. **P1 未披露 Task 2 结果不存在**：同类情形的 A3 用 `[PENDING …]` 显式标出，P1 没有；其结论段还写 "for the harder questions of age, reliability, renovation and provenance, it returns **a ruled judgement** with stated thresholds instead of an unqualified opinion"，读者会以为这些追问已经有判定。P1 的做法说明里则明确承认"我没有填任何数字……正文里也没有"。
8. **P2 把 0.996 写成 1.00**："giving a 95% interval of [0.36, 1.00] … wide, chiefly because six stairs is a small sample" —— 上界写成 1.00 与同一句"区间宽"的表述互相拆台（正文是 0.996）。
9. **P2 结果段的措辞自相打架**："people walked **three abreast**, and the central mode carries both the most traffic and the smallest spread, so the middle of the stair was the **habitual single-file path**" —— 三人并行与"习惯单列"同句并存，读者无从判断结论是哪个。
10. **五份把题面的合规套话搬进摘要**（A1:69、A2:20、A3:5、P1:8/37、P2:37-38）："non-destructive / low cost / small team with minimal tools" 几乎原样复现 `case-A-problem.txt:12`。占篇幅、不换分（20YGA:160-161 的精神）。
11. **A2 的摘要页文本里留着未填占位**：第 4 行 `Team Control Number: [fill from submission page] · Summary Sheet (page 1 of 25)`。与 `INDEX.md §2.2.9` 记的"保留占位符＝题号未填"同性质（虽然队号属排版层）。A1/P1/P2/A3/C1 都没有这一行。
12. **A1 的做法说明与摘要实况不符**（不影响摘要本身，但影响你采信其自述）：自述称"把 Strengths/Weaknesses 那一节压缩成'敏感性 + 稳健性'的**带数字的**陈述"，但摘要里硬度敏感性那一句没有任何数字。

---

## 6 打分员的顾虑（供你裁量）

1. **Q3 与 Q4 我按字面口径判，结果是 0 失败**。若你本意是"不许复用引言的**素材/功能**"（P1/P2 的首段就是引言那两段的改写）或"不许出现技术清单体"（P2 的 `The methods` 段、C1 的四方法一句），这两条会从"规格"翻成"指导"。Q3/Q4 的官方句子（`instructions.html:1132`、`20YGA:160-161`）其实更偏后者——**建议你确认这两条的限定语怎么写**。
2. **Q12 的 4 个 0 分是我判读的结果**：官方只反对"套话/boilerplate"，"自称诚实"算不算套话可以争。若你不接受，Q12 只剩"比较级"子项，而那个子项是 0 失败——那么 Q12 应整条降为规格。
3. **Q9 我刻意没有把 0.359 计入**（§5-①），否则 A1/A2 也会变 0、Q9 变成 5/6 失败。理由是 0.359 的不可复现需要自己拿 F 分布算一遍才看得出来，与"1.14 与三峰直接打架"不是一个可发现性等级。若你要更严的口径（"正文自相矛盾处的数一律不得进摘要"），A1/A2 改判 0。
4. **Q11 是词数推断，不是编译验证**：本机没编译这 6 份摘要，500–650 词/页是我的通用估计。六份词数从 856 到 1319，即便按宽松口径（700 词/页）也全部超标，所以结论方向不会翻转；但若你要写进 skill，建议注明"按 12pt 单页估算"。
5. **A3 与 P1 的正文不是同一份**：A3/P1 用的是 `case-A-body-partial.md`（无 Task 2 数值），A1/A2/P2 用的是 `case-A-body.md`。评 Q7/Q8/Q9 时我按各自正文判——若不区分正文版本，A3/P1 会被误判成"该给数却不给"。
