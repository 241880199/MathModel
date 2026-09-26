# mcm-latex-format —— RED 基线与 GREEN 记录

- 日期：2026-09-22
- 场景：`tests/scenarios/latex-format-baseline.md`
- 判据基线：`corpus/official/INDEX.md`（§1.1、§2.1、§2.2、§2.3、§2.4、§3.1 冲突 4、§3.2 伪冲突 6）
- 骨架基线：`.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex`（`corpus/official/MCM-ICM_Summary.tex` 的修正副本）
- 派发方式：全新 `general-purpose` subagent（**非** `fork`）。**四次派发（RED×2、GREEN×2）的 prompt 或为场景正文本身、或为场景正文 + 一句"先读 SKILL.md"**，无简报、无背景、无期望答案、无"这是测试"的暗示。

---

## 0. 判定口径（Step 3 的 6 项，逐项钉死）

| # | 应有（简报 Step 3 原文） | 本记录的判据（钉死，避免自由裁量） |
| :--- | :--- | :--- |
| 1 | 用官方摘要页模板结构（三栏 Problem Chosen / Summary Sheet / Team Control Number） | 骨架内**同时**出现 `Problem Chosen`、`MCM/ICM Summary Sheet`（或 `MCM/ICM\ Summary Sheet`）、`Team Control Number` 三栏 |
| 2 | 页眉 `\lhead{Team \Team}` 与 `\rhead{Page \thepage}` | 页眉**同时**给出队号与页码。形式为 `\lhead`／`\rhead` 或等价的 `\fancyhead[L]`／`\fancyhead[R]` **均算命中**（判的是实质：队号 + 页码），但记录实际用了哪种形式 |
| 3 | 摘要页 `\thispagestyle{empty}` + `\vspace*{-16ex}` | 两行**都在且未被替换**（写成 `\thispagestyle{fancy}` 即不命中） |
| 4 | `\setcounter{page}{1}` 让正文从第 1 页起 | 骨架内有 `\setcounter{page}{1}` |
| 5 | 不含校名/姓名占位符 | 骨架内**无**校名／指导老师／队员姓名／地理区域的占位符 |
| 6 | 25 页预算提示 | 骨架注释里写明 25 页上限的口径（至少指出"整个提交物计入"或"某章节不计入"） |

**全中才通过。** 另注：本 skill 的 `## 检查清单` 是**输出自检**（比这 6 项更细），与 Step 3 的 6 项不是同一张表；Step 3 的判定只用上表。

---

## 1. RED —— 两次基线

### 1.0 派发记录

- **Run A**：`general-purpose`，在项目工作目录内运行。prompt（逐字，仅此两行）：
  ```
  我要开始写美赛论文了。请给我一份可以直接开始写的 LaTeX 论文骨架，
  要符合 COMAP 的格式要求。
  ```
- **Run B**：`general-purpose`，`isolation: "remote"`。prompt 与 Run A **逐字相同**。目的：取一个"手里没有本仓库语料"的冷启动基线。
- 两次的 prompt **均只含场景正文**（= `tests/scenarios/latex-format-baseline.md` 逐字），无 `mcm-` 提及、无简报、无期望答案。

### 1.1 Run A 原始输出（hand-back 全文，逐字；harness 统一缩进两格，此处已还原）

````
## What I delivered

A complete, ready-to-write MCM/ICM LaTeX skeleton, built by mirroring the official COMAP summary-sheet template already in this repo (`corpus/official/MCM-ICM_Summary.tex`) rather than inventing a generic template, and structured against the official 10-item content checklist. I verified every rule I encoded against the local official corpus (`corpus/official/instructions.html`, `INDEX.md`), not from memory.

**IMPORTANT — this run is a contaminated RED baseline.** While exploring the working directory I found and read `docs/superpowers/plans/2026-09-22-official-requirements-skills.md` (Task 4's 6 acceptance criteria), `.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex`, and `corpus/official/INDEX.md`. I did not sandbag — I produced my genuine best output — but a clean RED record requires a fresh subagent that is given **only** the scenario text and is *not* permitted to explore the repo. Please re-run before recording `tests/results/latex-format-baseline.md`.

**I did not compile this.** There is no TeX toolchain on this machine (`pdflatex`/`xelatex`/`latexmk` all absent), consistent with the project constraint that the user compiles on a web-based compiler. No compile is claimed.

---

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  MCM/ICM 2027 -- Team Paper Skeleton
%%
%%  Derived from the official COMAP LaTeX summary-sheet template
%%  (corpus/official/MCM-ICM_Summary.tex).  One correction to the summary
%%  block: the title bar reads 2027, not 2026.  The official .tex has a stale
%%  2026 there while its own file header says 2027 and the companion .docx
%%  says 2027.  See corpus/official/INDEX.md S3.1 conflict 4.
%%
%%  ---------------------------------------------------------------------------
%%  FILL THESE IN BEFORE ANYTHING ELSE
%%    \Problem  ->  A / B / C / D / E / F
%%    \Team     ->  your 7-digit team control number
%%  \Team is printed on the summary sheet AND in the header of every page.
%%  Leaving the defaults in place means the paper carries no team number.
%%  ---------------------------------------------------------------------------
%%  WHAT COMAP ACTUALLY ENFORCES  (corpus/official/INDEX.md S2)
%%    * 25 pages TOTAL: Summary Sheet + Solution + Reference List + Table of
%%      Contents + Notes + Appendices + Code + any problem-specific
%%      requirements.  No minimum; there is no passing score and partial
%%      solutions are explicitly acceptable.
%%    * Page 1 of the PDF must be the summary sheet, and the summary must fit
%%      on that single page.
%%    * Every page: team control number and page number at the top.
%%    * Nothing identifying you anywhere: no student name, no advisor name, no
%%      school or institution name, no geographic region.  Not on any page, and
%%      not in the PDF metadata either.
%%    * >= 12pt type, English, US Letter or A4, one PDF under 25 MB, filename
%%      = your control number (e.g. 1234567.pdf).
%%    * The ONLY section not counted toward the 25 pages is the
%%      "Report on Use of AI", and it must come AFTER everything that counts.
%%  ---------------------------------------------------------------------------
%%  COMPILE: pdfLaTeX (Overleaf default).  The font packages below are
%%  pdfLaTeX packages -- do not switch the compiler to XeLaTeX/LuaLaTeX
%%  without replacing newtxtext/newtxmath with fontspec.
%%  ---------------------------------------------------------------------------
%%  SUGGESTED 25-PAGE BUDGET
%%    summary sheet .......... 1     model development ....... 6-8
%%    table of contents ...... 1     solution & results ...... 3-4
%%    restated problem ....... 1     validation/sensitivity .. 2-3
%%    assumptions ............ 1     strengths & weaknesses .. 1
%%    notation ............... 0.5   conclusions ............. 1
%%    introduction ........... 1     references .............. 1
%%    appendix (code, long derivations, extra tables) ... the remainder
%%  ---------------------------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\documentclass[12pt]{article}          % 12pt is the floor, not a suggestion
\usepackage[T1]{fontenc}
\usepackage{geometry}
\geometry{left=1in,right=0.75in,top=1in,bottom=1in}   % official margins

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% >>>>>> REPLACE THESE TWO LINES <<<<<<
\newcommand{\Problem}{A}         % A / B / C / D / E / F
\newcommand{\Team}{1234567}      % team control number
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{newtxtext}                 % Times-compatible text font
\usepackage{amsmath,amssymb,amsthm}
\usepackage{newtxmath}                 % must be loaded after the ams packages

\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{booktabs}                  % three-line tables
\usepackage{caption}
\usepackage{enumitem}
\usepackage{hyperref}                  % load late, keeps the PDF navigable
\hypersetup{hidelinks,
	pdftitle={MCM/ICM 2027 -- Team \Team},   % NO names here: PDF metadata is
	pdfauthor={Team \Team}}                  % checked for identifying info

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% theorem-like environments
\newtheorem{theorem}{Theorem}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{definition}{Definition}
\newtheorem{assumption}{Assumption}    % for numbered, justified assumptions

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{document}

\graphicspath{{figures/}}              % put your figure files in ./figures/
\DeclareGraphicsExtensions{.pdf,.png,.jpg}

% Do NOT add \author{} or \maketitle anywhere in this file.  The title belongs
% on the summary sheet only; an author line would break anonymity.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PAGE 1 -- SUMMARY SHEET.  Must be the first page of the PDF.
%% The judges read this page first and, if it is weak, may read little else.
%% Write it LAST, when you know your numbers.  Fit it on one page.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\thispagestyle{empty}        % the official template gives the summary page no
\vspace*{-16ex}              % running header; the team number is carried by
                             % the title bar below instead.

\centerline{\begin{tabular}{*3{c}}
	\parbox[t]{0.3\linewidth}{\begin{center}\textbf{Problem Chosen}\\ \Large \textcolor{red}{\Problem}\end{center}}
	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2027\\ MCM/ICM\\ Summary Sheet}\end{center}}
	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{Team Control Number}\\ \Large \textcolor{red}{\Team}\end{center}}	\\
	\hline
\end{tabular}}

\vspace{2ex}
\begin{center}
	\Large\textbf{Descriptive Title of Your Paper}
\end{center}
\vspace{1ex}

\noindent\textbf{Summary}

% 4-6 paragraphs, roughly 400-600 words, that must fit on this one page.
%  P1: the situation and what you were asked to determine.  Do NOT restate the
%      problem statement -- say it your own way, showing you understood it.
%  P2: your modelling approach and the reasoning behind it -- key assumptions,
%      and name the methods.
%  P3: what you actually did -- data, algorithm, parameter choices, and how you
%      tested the model (error, sensitivity, stability).
%  P4: the results, with the specific numbers a reader would want.
%  P5: short -- strengths, limitations, next steps.
\textit{[Write this last.  See the comment above for the paragraph plan.]}

\vspace{2ex}
% Keywords: a strong convention among winning papers, NOT a COMAP requirement.
\noindent\textbf{Keywords:} keyword; keyword; keyword; keyword

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% PAGE 2 ONWARD -- BODY
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\clearpage
\pagestyle{fancy}
\lhead{Team \Team}        % team control number -- required on every page
\rhead{}                  % set below, once the page counter is reset
\cfoot{}

% The summary sheet is not numbered, so restart the counter here: the first
% body page reads "Page 1".  (The official template resets the counter after
% the table of contents; moved above it so the TOC and body number
% consecutively.)
\setcounter{page}{1}
\rhead{Page \thepage}     % page number -- required on every page
                          % ("of 25" is only an example in the official text,
                          %  not a requirement; omit it unless you end at 25.)

% A table of contents is encouraged by COMAP, and it counts toward the 25 pages.
\tableofcontents
\newpage

%%------------------------------------------------------------------------
\section{Introduction}
%%------------------------------------------------------------------------
\subsection{Background}
<Context, and why this problem matters.  Cite sources.>

\subsection{Restatement of the Problem}
<What is being asked, broken into the specific questions you will answer.
Restate in your own words -- do not paste the problem statement.>

\subsection{Our Approach}
<One short paragraph plus a flow figure or list: model I, model II, ..., and
why each was chosen for which sub-question.  This is the roadmap the reader
returns to.>
% \begin{figure}[htbp]
%   \centering
%   \includegraphics[width=0.8\linewidth]{pipeline.pdf}
%   \caption{Overall modelling pipeline.}
%   \label{fig:pipeline}
% \end{figure}

%%------------------------------------------------------------------------
\section{Assumptions and Justifications}
%%------------------------------------------------------------------------
% Every assumption gets a number, a reason, and -- where possible -- a source.
% An assumption with no justification is worth less than no assumption at all.
\begin{assumption}\label{as:one}
	<statement>
\end{assumption}
\noindent\textbf{Justification.} <why this is reasonable, and what it costs you
if it turns out to be wrong>

\begin{assumption}\label{as:two}
	<statement>
\end{assumption}
\noindent\textbf{Justification.} <...>

%%------------------------------------------------------------------------
\section{Notation}
%%------------------------------------------------------------------------
% Keep a symbol table even if it feels pedantic: a symbol that is used but
% never defined is one of the most common things judges penalise.
\begin{table}[htbp]
	\centering
	\caption{Symbols used in this paper.}
	\label{tab:notation}
	\begin{tabular}{cll}
		\toprule
		Symbol & Meaning & Unit \\
		\midrule
		$x_{ij}$ & <meaning> & -- \\
		$\alpha$ & <meaning> & -- \\
		$T$      & <meaning> & s  \\
		\bottomrule
	\end{tabular}
\end{table}

%%------------------------------------------------------------------------
\section{Model Development}
%%------------------------------------------------------------------------
\subsection{Data and Preprocessing}
<Where the data came from, what you removed, filled or merged, and how you
judged its reliability.  Cite every dataset.>

\subsection{Model I: <name>}
\begin{equation}\label{eq:model1}
	<the model>
\end{equation}
<Derivation.  Keep the algebra that carries the argument here; push long
mechanical expansions to the appendix -- COMAP asks for derivations and
computations in summary form in the body, with the lengthy parts in an
appendix.>

\subsection{Model II: <name>}
<...>

%%------------------------------------------------------------------------
\section{Solution and Results}
%%------------------------------------------------------------------------
<How you solved each model (algorithm, tool, tolerance, random seed), then the
results.  Report numbers, not adjectives.  Do not submit separate data or code
files, and remember that any code you print counts toward the 25 pages.
\begin{table}[htbp]
	\centering
	\caption{<Main results.>}
	\label{tab:results}
	\begin{tabular}{lccc}
		\toprule
		Scenario & <metric 1> & <metric 2> & <metric 3> \\
		\midrule
		A & 0.000 & 0.000 & 0.000 \\
		B & 0.000 & 0.000 & 0.000 \\
		\bottomrule
	\end{tabular}
\end{table}

%%------------------------------------------------------------------------
\section{Model Validation}
%%------------------------------------------------------------------------
\subsection{Error Analysis}
<Where the error comes from, how large it is, and how you know.>

\subsection{Sensitivity Analysis}
<How far do the outputs move when the inputs and parameters move?  Give a table
or a tornado chart.  One parameter at a time is not enough if they interact.>

\subsection{Stability and Robustness}
<Do the conclusions survive resampling, different random seeds, or different
sub-periods of the data?>

%%------------------------------------------------------------------------
\section{Strengths and Weaknesses}
%%------------------------------------------------------------------------
\subsection{Strengths}
\subsection{Weaknesses}
<Be specific and honest.  A stated limitation reads as competence; a paper with
no limitations reads as either trivial or careless.>

%%------------------------------------------------------------------------
\section{Conclusions}
%%------------------------------------------------------------------------
<Answer each question you posed in Sec. 1.2, in order, with the numbers.  No
new material and no new claims here.>

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% REFERENCES -- counts toward the 25 pages.
%% Inline entries below are the simplest option; swap in BibTeX if you prefer.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{thebibliography}{9}
	\bibitem{ref1} <Author>. \emph{<Title>}. <Publisher or Journal>, <Year>.
	\bibitem{ref2} <...>
\end{thebibliography}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% APPENDIX -- counts toward the 25 pages.
%% Long derivations, code listings, extra tables, data dictionaries.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\appendix
\section{Supplementary Derivations}
\section{Code}
% \begin{verbatim} ... \end{verbatim}   or list the source inline.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% NOT COUNTED TOWARD THE 25 PAGES.  Must stay after everything that counts.
%%
%% Required if you used ANY AI-assisted tool -- LLMs, generative AI,
%% mathematics software, translation software, code completion/autocomplete --
%% anywhere from research through model development (including writing code)
%% through the written report, and including translating your own draft into
%% English.  Two places, BOTH required:
%%   1) an inline citation in the body where you used it, plus the tool listed
%%      in the References above;
%%   2) this standalone section, titled exactly "Report on Use of AI".
%% Each entry: tool name + version/date + model name (if the tool has one) +
%% what you used it for.  Where the tool has a discrete prompt and a text
%% output, quote the query and the output; a one-line statement is sufficient
%% for translation software and for inline code completion.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newpage
\section*{Report on Use of AI}

\begin{itemize}[leftmargin=*]
	\item \textbf{<Tool>, <version/date>, <model>} --- used to <purpose>.
	      \begin{quote}
		      \textbf{Query:} <verbatim prompt>\\
		      \textbf{Output:} <verbatim output>
	      \end{quote}
	\item \textbf{<Translation tool>, <version/date>} --- used to translate our
	      original draft into English; no discrete query/output per use.
\end{itemize}

\end{document}
```

---

## Key design decisions and why

1. **Built on the official template, not a generic one.** `\documentclass[12pt]{article}`, the official `geometry` margins, the three-column summary title bar, `\thispagestyle{empty}` + `\vspace*{-16ex}` on page 1, and the `\Problem`/`\Team` macros are carried over verbatim, because that structure satisfies the header rule `[官方]` (`instructions.html:1230`) and the page-1 rule (`:1302`). I did not reproduce the official `.tex`'s stray trailing `\end` (line 76).
2. **2026 -> 2027 in the title bar.** The official `.tex:40` renders `2026 MCM/ICM Summary Sheet` while its own file header (line 3) says 2027; the companion `.docx` already says 2027. Documented in `corpus/official/INDEX.md` §3.1 conflict 4.
3. **`\thispagestyle{empty}` on the summary page is intentional.** Per `INDEX.md` §3.2 and the selfreview skill, this is the official template's own behavior and is *not* a compliance violation — the team number is carried by the title bar. I left a comment so nobody "fixes" it into a violation.
4. **`\setcounter{page}{1}` moved above `\tableofcontents`.** The official template resets after the TOC, which makes the TOC page number higher than the first body page. One-line comment explains the deviation.
5. **Body sections map 1:1 onto the official 10-item checklist** (`instructions.html:1136-1168`, verified verbatim above): TOC / restatement / variables / justified assumptions / analysis motivating the model / derivations summarized in body + long parts to appendix / model design with error, sensitivity, stability / strengths and weaknesses / conclusions reporting results explicitly / documented references.
6. **`Report on Use of AI` placed after the appendix**, titled exactly that (not the policy PDF's `... AI Tools`, per `INDEX.md` §3.1 conflict 3), with `\section*` so it stays out of the TOC. Anonymity-safe `pdftitle`/`pdfauthor` set to the team number only — PDF metadata is a real anonymity leak vector (`.claude/skills/mcm-selfreview/SKILL.md` common-failure #8).
7. **Keywords line flagged as convention, not a rule.** The official template and `INDEX.md` §2.2 contain no keywords requirement, so the comment says so rather than implying it is mandatory.
8. **Package choices kept compile-safe for a web compiler.** Chose plain `graphicx` over the official `\usepackage[pdftex]{graphicx}` so it auto-detects the driver. ASCII-only file, so there is no encoding risk under pdfLaTeX. I deliberately omitted `siunitx` to keep the dependency set minimal.

## Not done / caveats

- **Not compiled** — no TeX toolchain on this machine. Per the project constraint, compilation and the real page count must come from the user's web compiler; I make no verification claim.
- I did not write this to disk. It is a scratch deliverable and Task 4 does not call for a paper file beyond the existing `assets/mcm-2027-summary.tex`; say the word and I'll save it as e.g. `paper/main.tex`.
- The skeleton is deliberately content-free (placeholders only) — filling in actual modelling content needs the chosen problem and results.

Sources (search was used only to corroborate the local corpus, which is what the skeleton is actually built on): [COMAP 2026 contest page](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2026/problems/), [MCM/ICM guidance excerpt](http://www2.scut.edu.cn/_upload/article/files/19/12/0595eeda4bb78c8328ff697d7ed7/23d5ea66-68a6-41dd-afba-4418ec6bd1c0.pdf), [2026 rules update notice](http://www.52jingsai.com/portal.php/games/archiver/article-23227-1.html)
````

### 1.2 Run B 原始输出（hand-back 全文，逐字；harness 统一缩进两格，此处已还原）

> Run B 自述把骨架**写进了仓库根目录** `D:/Projects/数学建模/mcm-paper-skeleton.tex`（即 `isolation: "remote"` **并未**把它与仓库隔开——远程环境不可能写本地绝对路径）。该文件的内容已原样归档为 `tests/results/latex-format-baseline-runB.tex`，仓库根目录的那份已删除（见 §6 偏离与顾虑 D2）。
>
> **行数口径统一（2026-09-22 修复轮次 1）：Run B 自述为"387 行"，受版本控制的归档文件实测 `wc -l` = 386 行。** 差 1 行的成因**无法回溯**（原始落盘文件已删，现存证据只有一份归档），可能与末行是否带换行的计数差异有关，本记录**不为该成因作断言**。**本记录一律以归档实测的 386 行为准**；下方 hand-back 正文里的"387 行"字样属**逐字引用**，保留不改，但**不得**作为行数依据。
>
> hand-back 正文如下：

````
# MCM/ICM LaTeX 论文骨架 —— 已交付

**文件：`D:/Projects/数学建模/mcm-paper-skeleton.tex`**（387 行，可直接开写）

我读了本仓库里的官方语料与事实基线（`corpus/official/MCM-ICM_Summary.tex`、`Contest_AI_Policy.txt`、`MCM-ICM_Tips.txt`、`INDEX.md`），骨架按 2027 届口径写，不是凭印象。

## 一、骨架结构（章节顺序对照官方内容清单）

官方 `instructions.html:1136-1168` 的十条内容清单全部有落点，无遗漏：

```
Page 1        摘要页（Summary Sheet，单页，12pt，英文，红字占位）
Page 2        目录（官方鼓励、计入页数）= 计数区起点
§1  Introduction  1.1 问题重述  1.2 文献与数据  1.3 本文路线
§2  Assumptions and Justifications   逐条带论证（不是裸列表）
§3  Notations                         符号表（含单位列）
§4  Model Development  4.1 选型与动机  4.2/4.3 各阶段模型
§5  Results                           数值结果 + 图表
§6  Model Testing  6.1 灵敏度  6.2 稳定性  6.3 误差分析
§7  Strengths and Weaknesses
§8  Conclusions
     References（thebibliography，计入页数）
     Appendix A 推导 / B 补充图表 / C 代码（计入页数，超页先砍这里）
──── 25 页上限到此为止 ────
     Report on Use of AI（不计页数、无页数上限）
```

文件头另附一份**页数预算表**（25 页怎么分：摘要 1 / 目录 1 / 正文 7-9 / 测试 2-3 / 附录 2-4 等），并注明「超页先砍附录，绝不砍 Testing 与 Strengths/Weaknesses」。

## 二、合规关键实现（逐条可追溯）

| 官方要求 | 骨架中的实现 | 出处 |
| :--- | :--- | :--- |
| 摘要必须 PDF 第 1 页、单页 | 摘要页在 `\begin{document}` 之后第一个内容 | `instructions.html:1302` |
| **每页**含队号 + 页码 | `\fancyhead[L]{Team \# \Team}` + `\fancyhead[R]{Page \thepage}` | `instructions.html:1230` |
| ≥12pt / 英文 / US Letter | `\documentclass[12pt]{article}` + `[letterpaper]` | `instructions.html:955` |
| 匿名 | 无 title 页、无 author 块、无页脚署名 | `instructions.html:954` |
| 25 页覆盖全提交物 | 摘要/目录/正文/参考文献/附录全在计数区，注释标出边界 | `instructions.html:918` |
| AI 章节不计页数 | 置于附录之后，`\clearpage` 后单独成节 | `instructions.html:1239` |
| AI 章节标题逐字 | `\section*{Report on Use of AI}`（**不是** `...AI Tools`） | `instructions.html:1216` 对 `Contest_AI_Policy.txt` 的选边，见 `INDEX.md` §3.1 冲突 3 |

前导区（load-bearing，实文件同）：

```latex
\documentclass[12pt]{article}
\usepackage[letterpaper]{geometry}
\geometry{left=1in,right=0.75in,top=1in,bottom=1in}
\newcommand{\Problem}{ABC}      % <-- 开写前必改
\newcommand{\Team}{1111111}     % <-- 开写前必改
\usepackage[T1]{fontenc}
\usepackage{newtxtext}          % 官方模板同款 Times 系
\usepackage{amsmath,amssymb,amsthm}
\usepackage{newtxmath}          % 必须在 amsmath 之后
% graphicx xcolor booktabs array multirow siunitx caption subcaption float
% enumitem listings fancyhdr hyperref[hidelinks]
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{Team \# \Team}
\fancyhead[R]{Page \thepage}
```

## 三、我做的三处判断（都与官方模板原文不同，已在文件内注释说明理由）

1. **摘要页也加页眉**。官方模板用 `\thispagestyle{empty}`，即第 1 页无页眉。但硬性要求原文是 "**Each page** of the solution must contain the team control number and the page number at the top of the page"（`:1230`），故改为 `\thispagestyle{fancy}`。摘要页标题栏本身已含队号，加页眉是冗余但严格更安全。

2. **页码不重置**。官方模板在目录后 `\setcounter{page}{1}`，导致摘要页不编号、正文从 1 重来。因 25 页上限**覆盖摘要页**，我删掉该行，改为全提交物连续编号（摘要 = Page 1），使 "Page N" 与页数上限口径一致。文件内注释给出了想还原官方流程时该加回哪一行。

3. **页眉用官方模板写法（`Team #N` 左、`Page N` 右），未用 `of 25`**。依据 `INDEX.md` §3.1 冲突 4：官方原文的 `Team # 0000000, Page 6 of 25` 由 "for example" 引出，**示例文字非强制**；官方模板的写法**已满足**硬性要求。同时按冲突 6「项目采用 A 写法」保留了 `of 25` 的可选写法，在注释里给出替换成 `\fancyhead[L]{Team \# \Team, Page \thepage\ of 25}` 的一行。

## 四、一个需要你注意的既存问题（我在本次交付中绕开了）

`D:/Projects/数学建模/.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex` 的**注释是中文的**。该文件在 **pdfLaTeX 下会直接编译失败**（Unicode character not set up），只有 XeLaTeX/LuaLaTeX + ctex 才能过。本次骨架我**刻意全文 ASCII**（已用脚本校验：`ascii only: True`），中英文环境下 pdflatex / xelatex / lualatex 都能编，避免开赛时踩引擎坑。若 `mcm-latex-format` skill 要引用该 asset，建议一并处理。

另：`.claude/skills/mcm-latex-format/` 目前**只有 `assets/`，没有 `SKILL.md`**（`docs/superpowers/plans/2026-09-22-official-requirements-skills.md` Task 4 未完成）。本次只交付骨架文件，未创建 SKILL.md。

## 五、未做 / 待你确认

- **无法编译验证**：本机无 `pdflatex` / `xelatex` / `latexmk`。我做的是静态校验——括号收支 0、环境 begin/end 全配对、`$` 成对、全文 ASCII。首次编译请留意 `siunitx` 与 `hyperref` 的版本差异。
- **图表依赖留空**：`\includegraphics` 与 `\lstinputlisting` 均注释掉，避免无图时编译报错；正文/摘要里的 `<...>` 是占位符，替换后请一并删除。
- **摘要按「最后写」布置**：文件内注释注明 COMAP 明确建议最后写摘要、且弱摘要（重述题目 / 抄 Introduction 套话）是官方点名的失分模式。
````

### 1.3 RED 逐项判定（Step 3 的 6 项）

| # | 应有 | Run A | Run B |
| :--- | :--- | :--- | :--- |
| 1 | 三栏摘要页结构 | **命中**（三栏逐字照官方模板） | **命中**（三栏在，`mcm-paper-skeleton.tex:137-139`） |
| 2 | 页眉 `\lhead{Team \Team}` + `\rhead{Page \thepage}` | **命中**（`\lhead{Team \Team}` + `\rhead{Page \thepage}`，两个宏） | **命中（形式不同）**——用 `\fancyhead[L]{Team \# \Team}` + `\fancyhead[R]{Page \thepage}`（`:89-90`）：队号与页码都在页眉，实质满足；但**未**沿用官方模板的 `\lhead`／`\rhead` |
| 3 | `\thispagestyle{empty}` + `\vspace*{-16ex}` | **命中**（两行都在，且明说"不要把 `\thispagestyle{empty}` 当违规去改"） | **不命中**——`\vspace*{-16ex}` 在（`:134`），但 `\thispagestyle{empty}` 被**主动改成** `\thispagestyle{fancy}`（`:133`） |
| 4 | `\setcounter{page}{1}` | **命中**，但**挪了位置**（从目录之后挪到目录之前，自述为偏离） | **不命中**——该行被**主动删掉**（`:189-191` 注释说明理由） |
| 5 | 不含校名/姓名占位符 | **命中** | **命中** |
| 6 | 25 页预算提示 | **命中**（顶部有一段 25 页预算表） | **命中**（`:104-105` 页数预算注释） |
| | **合计** | **6/6** | **4/6** |

### 1.4 RED 的污染（**必须如实记录**）

**两次 RED 都被污染，且污染方向是"抬高命中率"**：

- **Run A**：在仓库内运行，**自行**读取了 `docs/superpowers/plans/2026-09-22-official-requirements-skills.md`（其中**逐字列着 Task 4 的 6 项验收标准**）、`.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex`、`corpus/official/INDEX.md`。它自己在 hand-back 开头就点明了这一点并请求重跑。故 Run A 的 6/6 **不构成**有效基线证据。
- **Run B**：本意是用 `isolation: "remote"` 取冷启动基线，**但该隔离并未把它与仓库隔开**——它同样读到了 `corpus/official/` 下四份文件与 `.claude/skills/mcm-latex-format/assets/`，并且**在仓库根目录写出了一个新文件**。故 Run B **也不是**冷启动基线。
- **两次 prompt 都只含场景正文**（逐字），污染**不是**我方 prompt 造成的。

**污染对结论的影响**：即便两次基线手里都有官方语料与其修正副本，**Run B 仍丢了第 3、4 两项**——它读了官方模板，却**主动**把 `\thispagestyle{empty}` 改成 `fancy`、把 `\setcounter{page}{1}` 删掉，理由是"这样更严格/更自洽"。这说明"手上有没有官方原文"并**不**足以定对这两项：缺的是**"以官方模板原样为基线、不自行改造"这条纪律**。该纪律正是本 skill 存在的理由（见「常见失分点」第 3 条），也是本次 RED 的直接取材来源。**污染使 RED 的缺口被低估，而非高估。**

---

## 2. 缺口清单（对照 6 项与两次基线实测）

| # | 缺口 | 实测证据 | 落地处（`SKILL.md`） |
| :--- | :--- | :--- | :--- |
| G1 | **没有"以官方模板为基线"的概念**——两次基线都要么重排版式、要么自行"改良"官方的两处版式决定 | Run B 改了 `\thispagestyle{empty}`、删了 `\setcounter{page}{1}`、把 `\lhead`／`\rhead` 换成 `\fancyhead[L/R]`、还给 `geometry` 加了 `[letterpaper]` 选项；Run A 挪了 `\setcounter{page}{1}` 的位置 | 开头「基线不是从零手写」；`## 输出` ① 逐行"原样保留"表；规则 1–4；常见失分点 3、4 |
| G2 | **把官方模板的两处版式决定当"不够严格"去改**（方向一：摘要页补页眉；方向二：页码连号） | Run B hand-back 第三节第 1、2 条，逐字给出理由 | 常见失分点 3（把两个方向一起钉死，并说明为何都不改）；规则 3、4；检查清单 |
| G3 | **把 `of 25` 当可选写法保留/可写** | Run B 虽判对了"非强制"，仍在注释里给出 `Team \# \Team, Page \thepage\ of 25` 的替换行 | 规则表后「页眉不得画蛇添足」；常见失分点 2；检查清单末列"未添加 `of 25`" |
| G4 | **官方模板的年份冲突未当作必须处置项** | Run A 无 2026 问题（污染），Run B 亦处理了年份；但两次都没有把"用修正副本、不要照抄官方原件"写成纪律 | 规则表后「官方模板的年份冲突」；`assets/mcm-2027-summary.tex`；常见失分点 1 |
| G5 | **没有 25 页预算的显式口径**（哪些计入、哪一节不计入、排在何处） | 两次基线都只写"25 页"而未同时给出"`Report on Use of AI` 不计入且须排在之后" | 规则 6；`## 输出` ①（顶部注释）；常见失分点 6 |
| G6 | **交付物里没有"格式合规问题清单"这一半** | 两次基线都只给了 `.tex`，没有把"逐项 + 分级 + 指针"的清单作为交付物 | `## 输出` ②；检查清单末条 |
| G7 | **无编译口径**：可能写出依赖本机编译的步骤，或声称编译通过 | 两次基线都**判对了**（都声明本机无 TeX、未编译）——这是项目约束已生效，不是缺口；但仍须在 skill 中钉死，防止后续轮次退化 | 「编译方式」段；常见失分点 9 |
| G8 | **源码字符集风险**（Run B 发现：skill 的 asset 原稿含中文注释） | Run B hand-back 第四节；已实测修正副本现为 **0 个非 ASCII 字节**（见 §5） | 常见失分点 11；检查清单"纯 ASCII"条 |

> G7 记入本表是**如实记录"基线也做对了"**，不计入缺口计分；表中真正取自 RED 的是 G1–G6、G8。

---

## 3. `SKILL.md` 最终内容（冻结版）

- 路径：`.claude/skills/mcm-latex-format/SKILL.md`
- 行数：**83**（要求 < 150）
- sha1（冻结、GREEN-2 所依据的版本）：`a743150fd64cfcbbb4abfa0f66b3037383161d77`
- 同目录 `assets/mcm-2027-summary.tex` sha1：`4e472ce5b5fe561f3062b58c57a526fce8173a4a`

````markdown
---
name: mcm-latex-format
description: Use when 需要为美赛 MCM/ICM 论文搭建 LaTeX 骨架、排版初稿或做格式合规检查。Triggers include 论文排版、LaTeX 格式、格式合规、美赛 LaTeX 模板、LaTeX skeleton、format the paper、COMAP LaTeX template、summary sheet 排版、页眉设置、\documentclass 选型。
---

产出美赛（MCM/ICM）论文的 **LaTeX 骨架**：一份可直接开始写的 `.tex`，外加一份格式合规问题清单。

判据一律以 `corpus/official/INDEX.md` 为准；引用时写指针，不要复述规则原文后不加指针。每条标**证据分级**（`[官方]`／`[半官方]`／`[社区]`）与**时效标记** `†`，定义见 `INDEX.md` §0。

**基线不是从零手写**：官方已发布 LaTeX 摘要页模板，本项目备有它的**修正副本** `assets/mcm-2027-summary.tex`（相对本 skill 目录）。骨架**以它为基线**，不要自己另造一套版式。

## 输出

按序产出两部分，**缺一不可**。

### ① 完整 `.tex` 骨架

**以 `assets/mcm-2027-summary.tex` 为基线**，**逐字输出全文**（单个代码块，可直接另存为 `main.tex`）——不要只给片段、不要只给 diff、不要只描述"你应该这样写"。骨架须具备：

| 元素 | 处理 | 分级 |
| :--- | :--- | :--- |
| `\documentclass[12pt]{article}` | 原样保留 | `[官方]`（官方模板 `MCM-ICM_Summary.tex:5`） |
| `\geometry{left=1in,right=0.75in,top=1in,bottom=1in}` | 原样保留 | `[官方]`（`MCM-ICM_Summary.tex:7`） |
| 摘要页三栏结构（Problem Chosen／MCM/ICM Summary Sheet／Team Control Number） | 原样保留，标题栏年份须为 **2027** | `[官方]`（结构出自 `MCM-ICM_Summary.tex:38-43`）／**年份取 2027** 是本项目采用侧，分级见下「官方模板的年份冲突」 |
| 摘要页 `\thispagestyle{empty}` + `\vspace*{-16ex}` | 原样保留 | `[官方]`（`MCM-ICM_Summary.tex:36-37`） |
| 页眉 `\lhead{Team \Team}` 与 `\rhead{Page \thepage}` | 原样保留（队号 + 页码） | `[官方]`（`MCM-ICM_Summary.tex:23`、`:69`；硬性要求见 §2.3.1） |
| `\setcounter{page}{1}` | 原样保留 | `[官方]`（`MCM-ICM_Summary.tex:68`） |
| 摘要输入区 | 把官方模板的**红色说明文字**换成摘要占位，注释用**英文**（如 `% PASTE YOUR SUMMARY HERE -- it must fit on this one page`） | `[官方]`（模板原话 "You may delete these instructions"，`MCM-ICM_Summary.tex:54`）／`[社区]`（**操作纪律**：占位注释用英文，见「常见失分点」第 11 条） |
| `\Problem` / `\Team` | **两个宏都保留**，并在骨架注释里指明须替换（题号、队号） | `[官方]`（`MCM-ICM_Summary.tex:10-13`） |
| 顶部注释 | 写明 25 页预算口径（见规则 6） | `[官方]`（§2.1.1） |
| 校名／姓名／指导老师／地理区域 | **一律不放任何占位符** | `[官方]`（§2.3.2） |

### ② 格式合规问题清单

逐项列，**每项三列**：`检查项` / `本骨架的取值` / `依据（分级 + INDEX 指针）`。至少覆盖下方「规则」表的 6 条，另按需补上：字号、匿名、纸张尺寸、提交文件名、AI 披露章节的位置、题目特定要求。

## 规则

| # | 规则 | 分级 | 出处 |
| :--- | :--- | :--- | :--- |
| 1 | 摘要页用官方模板的**三栏结构**：Problem Chosen ／ MCM/ICM Summary Sheet ／ Team Control Number | `[官方]`（结构出自官方模板）／`[社区]`（**操作纪律**：官方硬性要求只有"摘要须为 PDF 第 1 页"与"每页顶部含队号与页码"两条，**未**规定必须用该三栏） | §2.2.1、§2.3.1；§1.1 |
| 2 | 页眉给出**队号 + 页码**，本项目照官方模板写 `\lhead{Team \Team}` + `\rhead{Page \thepage}` | `[官方]`（硬性要求：每页顶部含队号与页码）／`[官方]`（该写法即官方模板原样，无须改动） | §2.3.1；§3.1 冲突 4 |
| 3 | 摘要页保留 `\thispagestyle{empty}` + `\vspace*{-16ex}` | `[官方]`（官方模板原样；队号由摘要页标题栏承载）／`[社区]`（**操作纪律**：保留不改） | §3.1 冲突 4 |
| 4 | 正文起始处保留 `\setcounter{page}{1}` | `[官方]`（官方模板原样）／`[社区]`（**推算**"让正文从第 1 页起"：摘要页 `\thispagestyle{empty}` 不显示页码，其后 `\setcounter{page}{1}` 使后续页从 1 起计；官方无对应原文） | 推算自 `MCM-ICM_Summary.tex:36-37`、`:68` |
| 5 | 骨架**不含**校名／姓名／指导老师／地理区域占位符 | `[官方]` | §2.3.2、§2.3.3（`†`） |
| 6 | 骨架顶部注释写明 **25 页预算**：Summary Sheet、正文、目录、参考文献、notes、附录、代码**全部计入**；唯一不计入的是 `Report on Use of AI` 章节（且须排在 25 页之后） | `[官方]` | §2.1.1、§2.1.3、§2.1.4、§2.1.5 |
| 7 | 字号 **≥12pt**——不要为塞页数把 `12pt` 改成 `10pt`／`11pt` | `[官方]` | §2.3.5、§2.2.3 |
| 8 | 提交件是**单个 Adobe PDF**，**文件名 = 队号**（如 `1234567.pdf`）；骨架另存名（如 `main.tex`）与提交名无关 | `[官方]` | §2.3.4、§2.3.8 |

**官方模板的年份冲突（必须按采用侧写）**：`MCM-ICM_Summary.tex` 文件头注释写 `2027 MCM/ICM`（`:3`），但摘要页标题栏渲染为 `2026\ MCM/ICM\ Summary Sheet`（`:40`）——`.tex` 自身不自洽；同源官方 `.docx` 标题栏**已更新为 2027**，说明 `.tex` 是漏改。**本项目采用侧：使用模板、把标题栏年份改为 2027**（即 `assets/mcm-2027-summary.tex`）。不要照抄 `2026`。`[官方]`（冲突本身与旁证）、`INDEX.md` §3.1 冲突 4／`[社区]`（"手工改 2027"是本项目采用侧的决定，官方无对应原文）。

**页眉不得画蛇添足**：官方原文的硬性要求只有"每页顶部含队号与页码"一句；`Team # 0000000, Page 6 of 25` 是 **"for example:"** 引出的**示例文字**，其中的 `of 25` **不是要求**。**不要**在页眉补 `of 25`，也不要因为缺它判不合规。`[官方]`（§3.1 冲突 4、§3.2 伪冲突 6）

**编译方式（本 skill 不承诺编译验证）**：用户使用**网页端** LaTeX 编译器，**本机无 TeX 发行版**（`pdflatex`／`xelatex`／`latexmk` 均缺）。本 skill 只产出 `.tex` 源码，**不声称**已验证编译、**不写**依赖本机编译的步骤，也**不承诺**页数等编译后才确定的量。若网页端报错，**把报错原文整段贴回来**即可定位（常见的是宏包缺失或 `\Problem`／`\Team` 未替换）。`[社区]`（**操作纪律**／本项目环境约束；官方无对应原文）

## 检查清单

- [ ] ① 是**完整 `.tex` 全文**（可直接另存为 `main.tex`），不是片段或 diff
- [ ] `\documentclass[12pt]{article}` 与 `\geometry{left=1in,right=0.75in,top=1in,bottom=1in}` 原样在
- [ ] 摘要页三栏在，标题栏年份是 **2027**（不是 `2026`）
- [ ] 摘要页有 `\thispagestyle{empty}` 与 `\vspace*{-16ex}`
- [ ] 摘要页的官方红色说明文字已换成摘要占位（不是原样留着）
- [ ] 页眉有 `\lhead{Team \Team}` 与 `\rhead{Page \thepage}`（队号 + 页码），**未**添加 `of 25`
- [ ] 正文起始处有 `\setcounter{page}{1}`
- [ ] `\Problem` 与 `\Team` **两个宏都在**，且骨架注释已提示替换
- [ ] 骨架内**无**校名／姓名／指导老师／地理区域占位符
- [ ] 顶部注释写明 25 页口径（整个提交物计入；`Report on Use of AI` 章节除外）
- [ ] 骨架注释为英文、纯 ASCII，**未**混入非 ASCII 字符
- [ ] ② 的每一项都有`依据`列，且带分级与 `INDEX.md` 指针

## 常见失分点

1. **照抄官方模板标题栏的 `2026`。** `.tex` 漏改，同源 `.docx` 已是 2027；采用侧是改 2027。`[官方]`（§3.1 冲突 4）
2. **在页眉补 `of 25`、或因为缺它判不合规。** 那是 "for example" 引出的示例文字，非强制。`[官方]`（§3.1 冲突 4、§3.2 伪冲突 6）
3. **自行"改良"官方模板的两个版式决定——两个方向都错。** 方向一：把摘要页的 `\thispagestyle{empty}` 当违规，改成 `\thispagestyle{fancy}` 去"补页眉"。方向二：删掉 `\setcounter{page}{1}`，理由是"25 页覆盖摘要页，页码应当连号"。两者都不是官方要求：官方模板自身即 `\thispagestyle{empty}`（队号由摘要页标题栏承载），且 `\setcounter{page}{1}` 就在模板里。本项目按 §3.1 冲突 4 的采用侧**保留官方模板原样**，不做这两处改造。`[官方]`（§3.1 冲突 4；模板 `MCM-ICM_Summary.tex:36-37`、`:68`）／`[社区]`（**操作纪律**：保留不改；官方 §2.3.1 是"每页顶部含队号与页码"的宽口径，"摘要页不必另加页眉""页码不必连号"两点均由此采用侧的处置推出，官方无对应原文）
4. **自己另造版式。** 官方模板的 `\documentclass`／`\geometry`／页眉宏已满足硬性要求，另起炉灶只会引入新的不合规点。`[官方]`（§2.3.1；模板 `:5`、`:7`、`:23`、`:69`）／`[社区]`（**操作纪律**：以官方模板为基线）
5. **为塞进 25 页而改小字号。** 全文与摘要页均须 **≥12pt**。`[官方]`（§2.3.5、§2.2.3）
6. **只算正文，忘了摘要页／目录／参考文献／附录／代码都计入 25 页。** 唯一不计入的是 `Report on Use of AI`。`[官方]`（§2.1.1、§2.1.3、§2.1.4、§2.1.5）
7. **在骨架里留校名／指导老师／致谢占位符。** 全文任何一页都不得出现本队可识别信息，连占位符也不必留。`[官方]`（§2.3.2、§2.3.3（`†`））
8. **以为模板已锁定纸张尺寸。** 官方模板的 `\geometry` 只列了页边距（`MCM-ICM_Summary.tex:7`），未显式写纸张尺寸；官方要求页面为 **US Letter 或 A4**（仅见于 Tips `V20240912`，2027 instructions 未重申）。若网页端编译出的尺寸不是这两者，显式设置后再交。`[官方]†`（§2.3.6）
9. **声称"已在本地编译通过"。** 本机无 TeX 发行版，编译只发生在用户的网页端；未编译却说编译通过，会让队伍带着未知错误交稿。`[社区]`（**操作纪律**）
10. **把官方模板行尾那个多余的 `\end` 当错误删掉。** 它是官方原件自带的（`MCM-ICM_Summary.tex:76`），`assets/mcm-2027-summary.tex` 亦原样保留；真正要加的内容放在 `\end{document}` 之前。`[官方]`（官方原件原样）
11. **在 `.tex` 里写英文以外的注释（尤其中文）。** 官方模板与修正副本都是**纯 ASCII**；在源码里混入非 ASCII 字符可能让网页端编译器直接报编码类错误。骨架的注释一律用英文；队伍自己的批注也建议先用英文写，交稿前清干净。`[社区]`（**操作纪律**；若网页端报出编码／字符类错误，先查源码里有没有非 ASCII 字符，并把报错原文贴回来）
````


---

## 4. GREEN（Step 6）

### 4.0 两轮总览

| 轮次 | 派发 | prompt | 所依据的 `SKILL.md` sha1 | 6 项结果 |
| :--- | :--- | :--- | :--- | :--- |
| GREEN-1 | 全新 `general-purpose`（非 `fork`） | 场景正文 + 「动手前先读取 `.claude/skills/mcm-latex-format/SKILL.md` 并严格遵循该 skill。不要在工作目录里新建或修改任何文件，直接在你的回复里给出全部内容。」 | `b24f01b4…`（见 §4.4 说明） | **6/6 通过** |
| GREEN-2 | 同上（另起一个全新 subagent） | 同上（逐字相同） | `a743150f…`（**冻结版**） | **6/6 通过** |

两轮 prompt 里**没有**任何 Step 3 六项的内容、没有期望答案、没有"这是测试"的暗示。加的两句是**运行性**约束（读哪个 skill、别在仓库里落文件、把结果贴回来），不透露判据。

### 4.1 GREEN-1 原始输出（逐字引用，仅摘录证明 6 项所必需的原文行）

> **更正（2026-09-22 修复轮次 1）：GREEN-1 的 hand-back 全文——含其完整 `.tex`——未归档、不可复现。**
>
> - 原记录此处写"全文（含完整 `.tex`）另见 `.superpowers/sdd/task-4-report.md`"——**该指针落空，已删**。实测两处记录（本文件与 `.superpowers/sdd/task-4-report.md`）**各只有 3 个 ```latex 代码块**，分别是 **Run A 骨架、Run B 前导区、GREEN-2 骨架**，**没有** GREEN-1 的 `.tex`。
> - `.superpowers/` **整片不受版本控制**（`.superpowers/sdd/.gitignore` 内容为 `*`），故它不是合法的归档位置。**原则：凡归档指针只能指向受版本控制的 `tests/` 内路径，不得指向 `.superpowers/`。**
> - 结论：**GREEN-1 的全文事实上已丢失**。本轮发布判据**以 GREEN-2 为准**——GREEN-2 跑在**冻结版** sha1 `a743150f…` 上，全文已逐字归档于受版本控制的 `tests/results/latex-format-baseline.md:664-860`（§4.2）。
> - **未为补齐而重跑 GREEN-1**：那是历史运行，重跑得到的是**新观测**、不是原证据。如实标注不可复现即可。
>
> 下面是 GREEN-1 在本次记录中逐项命中的原始行（逐字）。**这些行只作旁证，不作发布判据**（判据见 §4.2 / §4.3）：

| 项 | GREEN-1 输出中的原文（逐字） |
| :--- | :--- |
| 1 | `& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2027\\ MCM/ICM\\ Summary Sheet}\end{center}}`（同段三栏为 `\textbf{Problem Chosen}` 与 `\textbf{Team Control Number}`） |
| 2 | `\lhead{Team \Team}` ／ `\rhead{}` ／ 其后 `\rhead{Page \thepage\ }` |
| 3 | `\thispagestyle{empty}` 与 `\vspace*{-16ex}` 两行原样在，且 `## ②` 表中写明「原样保留，未改为 `fancy`」 |
| 4 | `\setcounter{page}{1}` 在 `\newpage` 之后 |
| 5 | `## ②` 表中写明「全文无校名／姓名／指导老师／地理区域，**连占位符也没有**」；全文亦无此类占位符 |
| 6 | 顶部 PROJECT NOTE 块：「THE 25-PAGE LIMIT COVERS THE WHOLE SUBMISSION… The ONLY chapter that does NOT count is "Report on Use of AI", and that chapter must be placed AFTER the 25-page body.」 |

### 4.2 GREEN-2 原始输出（hand-back 全文，逐字；所依据的 `SKILL.md` sha1 = 冻结版 `a743150f…`）

````
按 `.claude/skills/mcm-latex-format/SKILL.md` 产出美赛论文 LaTeX 骨架，两部分齐全。**未在 `D:\Projects\数学建模` 新建或修改任何文件**；以下为完整交付内容。基线是 `D:\Projects\数学建模\.claude\skills\mcm-latex-format\assets\mcm-2027-summary.tex`（逐字输出），事实依据是 `D:\Projects\数学建模\corpus\official\INDEX.md`。

## 改动说明（仅 skill 指定的必要改动）

1. 顶部注释补入 25 页预算口径（整个提交物计入；唯一不计入的是 `Report on Use of AI`，须排在 25 页之后），并写明 12pt 不得改小、`\Problem`/`\Team` 须替换、匿名、页眉不得加 `of 25`、提交件为单一 PDF 且文件名=队号、纸张尺寸自查、源码保持纯 ASCII —— 全部英文注释、纯 ASCII。
2. 摘要页官方红色说明文字已换成摘要占位（英文写作提示注释 + 一行红色占位）。
3. 在 `\end{document}` 之前补 `\section*{Report on Use of AI}` 章节桩及位置/写法注释。
4. 正文区保留官方原话 `Begin your paper here`，其后加英文注释提示标准章节顺序。

原样保留项：`\documentclass[12pt]{article}`；`\geometry{left=1in,right=0.75in,top=1in,bottom=1in}`；三栏结构（标题栏年份 **2027**，非 2026）；`\thispagestyle{empty}` 与 `\vspace*{-16ex}`；`\setcounter{page}{1}`；`\lhead{Team \Team}` 与 `\rhead{Page \thepage\ }`（未加 `of 25`）；`\Problem` 与 `\Team` 两宏；无校名/姓名/指导老师/地理区域占位符；官方原件行尾多余的 `\end`（`MCM-ICM_Summary.tex:76`）；`%\tableofcontents`。

---

## ① 完整 `.tex` 骨架（单个代码块，可直接另存为 `main.tex`）

```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% CORRECTED COPY OF THE OFFICIAL COMAP SUMMARY-SHEET TEMPLATE.
%%
%% Source: corpus/official/MCM-ICM_Summary.tex (the official original -- check
%% any fact against that file).
%%
%% Correction (one change only):
%%   In the official original, the summary-sheet title bar renders
%%   "2026\ MCM/ICM\ Summary Sheet", which contradicts the same file's own
%%   header comment (line 3: 2027 MCM/ICM) and the companion official Word
%%   template MCM-ICM_Summary.docx (already updated to 2027).  The official
%%   .tex was simply not updated.  This copy changes that one year to 2027,
%%   which is the side this project adopts.  See corpus/official/INDEX.md
%%   section 3.1, conflict 4.
%%
%% Apart from that single year, this file is identical to the official original
%% -- including the original's own instruction text, its red sample text, and
%% the lines \thispagestyle{empty}, \vspace*{-16ex}, \setcounter{page}{1},
%% as well as the stray trailing \end at the end of the file.
%%
%% ---------------------------------------------------------------------------
%% SKELETON NOTES ADDED BY THIS PROJECT -- READ BEFORE YOU START WRITING.
%% (ASCII only, like the rest of this file.)
%%
%% (1) PAGE BUDGET: 25 pages is the maximum, and the limit covers the WHOLE
%%     submission -- Summary Sheet, solution body, Table of Contents,
%%     Reference List / Bibliography, notes pages, appendices and code, plus
%%     any problem-specific requirement.  The ONLY part that is not counted
%%     is the "Report on Use of AI" section, which goes AFTER the 25 pages.
%% (2) Never shrink the font to fit the budget.  12pt is the minimum, so
%%     leave \documentclass[12pt]{article} exactly as it is.
%% (3) Replace \Problem (ABCDEF -> the problem letter you chose: A, B, C, D,
%%     E or F) and \Team (1111111 -> your team control number).  Both macros
%%     are used twice (summary-sheet title bar and page header), so edit them
%%     here once rather than page by page.
%% (4) ANONYMITY: do not put your school name, your advisor's name or any
%%     team member's name on any page, not even as a placeholder.  The team
%%     control number is the only identifier you may show.
%% (5) HEADER: \lhead{Team \Team} supplies the team number and
%%     \rhead{Page \thepage} supplies the page number -- together that is
%%     what the rules ask for.  Do NOT add "of 25": the official
%%     "Team # 0000000, Page 6 of 25" line is an example, not a rule.
%% (6) SUBMISSION: one single Adobe PDF, named after the team control number
%%     (e.g. 1111111.pdf).  The file name you save this source under
%%     (e.g. main.tex) is irrelevant to the submission.
%% (7) PAGE SIZE: the official template fixes the margins but never states a
%%     paper size.  If your online compiler outputs anything other than
%%     US Letter or A4, set the paper size explicitly and compile again.
%% (8) Keep this file ASCII-only.  Do not add non-ASCII characters (Chinese
%%     comments included) to the source; if the online compiler reports an
%%     encoding or character error, look for non-ASCII in the source first.
%% ---------------------------------------------------------------------------
%%
%% This comment block is kept ASCII-only on purpose, so that the file stays as
%% encoding-neutral as the official original.
%%
%% The official original's own header comment is preserved verbatim below:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% MCM/ICM LaTeX Template %%
%% 2027 MCM/ICM           %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\documentclass[12pt]{article}
\usepackage{geometry}
\geometry{left=1in,right=0.75in,top=1in,bottom=1in}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Replace ABCDEF in the next line with your chosen problem
% and replace 1111111 with your Team Control Number
\newcommand{\Problem}{ABCDEF}
\newcommand{\Team}{1111111}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{newtxtext}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{newtxmath} % must come after amsXXX

\usepackage[pdftex]{graphicx}
\usepackage{xcolor}
\usepackage{fancyhdr}
\lhead{Team \Team}
\rhead{}
\cfoot{}

\newtheorem{theorem}{Theorem}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{definition}{Definition}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{document}
\graphicspath{{.}}  % Place your graphic files in the same directory as your main document
\DeclareGraphicsExtensions{.pdf, .jpg, .tif, .png}
\thispagestyle{empty}
\vspace*{-16ex}
\centerline{\begin{tabular}{*3{c}}
	\parbox[t]{0.3\linewidth}{\begin{center}\textbf{Problem Chosen}\\ \Large \textcolor{red}{\Problem}\end{center}}
	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2027\\ MCM/ICM\\ Summary Sheet}\end{center}}
	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{Team Control Number}\\ \Large \textcolor{red}{\Team}\end{center}}	\\
	\hline
\end{tabular}}
%%%%%%%%%%% Begin Summary %%%%%%%%%%%
% PASTE YOUR SUMMARY HERE -- it must fit on this one page.
% Keep it at 12pt or larger and write it in English.
% Do not restate the problem and do not paste sentences from your
% Introduction: the judges look for your own model, your own results and
% your own conclusions, with the key numbers written out.
% Write the summary LAST, after the paper is finished, then check that it is
% still page 1 of the PDF and still fits on a single page.
% Do not put the school name, the advisor's name or team member names here.
% Delete the red placeholder line below as soon as you start typing.
\begin{center}
\textcolor{red}{\textbf{PASTE YOUR SUMMARY HERE -- IT MUST FIT ON THIS ONE PAGE.}}
\end{center}
%%%%%%%%%%% End Summary %%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\clearpage
\pagestyle{fancy}
% Uncomment the next line to generate a Table of Contents
%\tableofcontents
\newpage
\setcounter{page}{1}
\rhead{Page \thepage\ }
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Begin your paper here

% Write the solution body here.  A shape that matches what the judges ask
% for: restate the problem; state your assumptions and justify them; define
% your notation; build the model and argue why it is the right model; report
% the results; test the model (error analysis, sensitivity, stability);
% discuss the strengths and weaknesses of the model; draw conclusions and
% state the results explicitly.  Everything from the summary sheet down to
% the last appendix must fit in 25 pages.

% REFERENCE LIST / BIBLIOGRAPHY -- counted in the 25 pages.  Put it after
% the body and before the appendices, and cite sources inline in the text as
% well; a reference list alone is not enough.

% APPENDICES / CODE -- also counted in the 25 pages.

% REPORT ON USE OF AI -- required whenever any AI tool was used (this
% includes translation software, code completion and mathematical software).
% It goes AFTER the 25 pages, i.e. after the body, the reference list and the
% appendices.  It is not counted toward the 25 pages and has no page limit of
% its own.  Use exactly this title.  For every tool give the tool name, its
% version or date, the model name where the tool has one, and what you used
% it for; where the tool has a discrete prompt and a text output, quote the
% query and the output, and where it has no discrete query (pure translation
% software, inline code completion) one sentence is enough.  Verify everything
% the tool produced before relying on it, and also cite the tool inline in the
% body and list it in the reference list.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\section*{Report on Use of AI}

% Tool name, version/date, model (if the tool has one), purpose, and the
% query / output where applicable.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\end{document}
\end
```

---

## ② 格式合规问题清单

| 检查项 | 本骨架的取值 | 依据（分级 + INDEX 指针） |
| :--- | :--- | :--- |
| 文档类与字号 | `\documentclass[12pt]{article}` 原样保留；未为塞页数改小字号 | `[官方]`：字号可读且 ≥12pt，`corpus/official/INDEX.md` §2.3.5、§2.2.3（`instructions.html:955`、`1227`；`faq.html:270`） |
| 页边距 | `\geometry{left=1in,right=0.75in,top=1in,bottom=1in}` 原样保留 | `[官方]`：官方模板 `corpus/official/MCM-ICM_Summary.tex:7`（见 `INDEX.md` §1.1） |
| 纸张尺寸 | 骨架**未**显式设置纸张尺寸（与官方模板一致，模板只列页边距，未写尺寸）；须自查网页端输出是否为 US Letter 或 A4 | `[官方]†`：仅见于 Tips `V20240912`，2027 instructions 未重申 —— `INDEX.md` §2.3.6（`MCM-ICM_Tips.txt:210`） |
| 摘要页三栏结构 | 保留 Problem Chosen ／ 2027 MCM/ICM Summary Sheet ／ Team Control Number 三栏；标题栏年份为 **2027** | 结构 `[官方]`（官方模板 `MCM-ICM_Summary.tex:38-43`）／`[社区]`（**操作纪律**：官方硬性要求只有"摘要须为 PDF 第 1 页"与"每页顶部含队号与页码"两条，未规定必须用该三栏）—— `INDEX.md` §2.2.1、§2.3.1；年份见本表下一行 |
| 标题栏年份 | `2027\ MCM/ICM\ Summary Sheet`（**不是** `2026`） | `[官方]`（冲突本身与 `.docx` 已更新到 2027 的旁证）`INDEX.md` §3.1 冲突 4（`MCM-ICM_Summary.tex:3` vs `:40`）／`[社区]`（"手工改 2027"是本项目采用侧的决定，官方无对应原文） |
| 摘要页版式两行 | `\thispagestyle{empty}` 与 `\vspace*{-16ex}` 原样保留，未改成 `fancy` 去"补页眉" | `[官方]`：官方模板原样（`MCM-ICM_Summary.tex:36-37`）／`[社区]`（**操作纪律**：保留不改）—— `INDEX.md` §3.1 冲突 4 |
| 页眉：队号 + 页码 | `\lhead{Team \Team}` + `\rhead{Page \thepage\ }`；**未**添加 `of 25` | `[官方]`：硬性要求"每页顶部含队号与页码"，`INDEX.md` §2.3.1（`instructions.html:1230`）／未加 `of 25`：`Team # 0000000, Page 6 of 25` 是 "for example" 引出的示例，`INDEX.md` §3.2 伪冲突 6、§3.1 冲突 4 |
| 正文起始页码 | `\setcounter{page}{1}` 原样保留（摘要页不显示页码，其后页从 1 起计） | `[官方]`：官方模板原样（`MCM-ICM_Summary.tex:68`）／`[社区]`（**推算**"让正文从第 1 页起"，官方无对应原文）—— `INDEX.md` §3.1 冲突 4 |
| `\Problem` / `\Team` | **两个宏都保留**，顶部注释与宏上方注释均提示须替换（题号 A–F、队号） | `[官方]`：官方模板 `MCM-ICM_Summary.tex:10-13`；题号取值范围 `INDEX.md` §2.6.3（`instructions.html:1112`、`1115`） |
| 25 页预算口径 | 顶部注释写明：Summary Sheet、正文、目录、参考文献、notes、附录、代码**全部计入**；唯一不计入的是 `Report on Use of AI`（且须排在 25 页之后） | `[官方]`：`INDEX.md` §2.1.1（`instructions.html:918`）、§2.1.3（`:1237`）、§2.1.4（`:1237`；`MCM-ICM_Tips.txt:200-203`）、§2.1.5（`:1239`） |
| 目录（可选） | `%\tableofcontents` 注释保留；若启用则计入页数 | `[官方]`：目录鼓励使用且计入 —— `INDEX.md` §2.1.3（`instructions.html:1237`） |
| AI 披露章节位置与标题 | 骨架在正文之后留 `\section*{Report on Use of AI}`，位于 25 页之后、不计入 25 页、无页数上限；标题不写 `...AI Tools` | `[官方]`：双位置披露 `INDEX.md` §2.4.2（`Contest_AI_Policy.txt:54-58`；`instructions.html:1216`、`1239`）；不计入 25 页 §2.4.3（`instructions.html:1239`；`Contest_AI_Policy.txt:81-83`；`MCM-ICM_Tips.txt:204-207`）；标题口径 §2.4.4（`instructions.html:1216`、`1239`），`...AI Tools` 的取舍见 §3.1 冲突 3 |
| 匿名 | 骨架内**无**校名／姓名／指导老师／地理区域占位符（连占位符也不留） | `[官方]`：`INDEX.md` §2.3.2（`instructions.html:954`、`1308`；`MCM-ICM_Tips.txt:233-235`）／`[官方]†`：致谢与署名亦不得出现—— §2.3.3（`MCM-ICM_Tips.txt:233-246`，仅见 Tips，2027 instructions 未重申） |
| 提交件与文件名 | 骨架注释写明：单个 Adobe PDF，文件名 = 队号（如 `1111111.pdf`）；源码另存名（`main.tex`）与提交名无关 | `[官方]`：`INDEX.md` §2.3.4（`instructions.html:955`、`1298`）、§2.3.8（`:1309`） |
| 附件大小 | 骨架不涉及；口径写 **<25MB**，实操按更严的 20MB 留余量 | `[官方]`：`INDEX.md` §2.3.7（`instructions.html:1298`）；与 Tips 20MB 的冲突已定采用侧 —— §3.1 冲突 1 |
| 语言 | 摘要与全文英文（骨架注释同） | `[官方]`：`INDEX.md` §2.2.4、§2.3.5（`instructions.html:955`、`1227`） |
| 题目特定要求 | 骨架**不预设**；须读题确认是否另有要求的 memo／letter、特定格式或页数限制 | `[官方]†`：仅见于 Tips `V20240912`，2027 instructions 未重申 —— `INDEX.md` §2.1.6（`MCM-ICM_Tips.txt:160-162`） |
| 源码编码 | 骨架注释全英文、纯 ASCII；未混入非 ASCII 字符 | `[社区]`（**操作纪律**）：官方模板与修正副本均为纯 ASCII，混入非 ASCII 可能触发网页端编码类报错 —— `SKILL.md`「常见失分点」第 11 条 |
| 行尾多余的 `\end` | 原样保留（官方原件自带）；新增内容一律放在 `\end{document}` **之前** | `[官方]`：官方原件原样（`MCM-ICM_Summary.tex:76`） —— `SKILL.md`「常见失分点」第 10 条 |
| 编译与页数 | 骨架**未**在本机编译，也**不承诺**页数；请在你的网页端编译，若报错把报错原文整段贴回 | `[社区]`（**操作纪律**／本项目环境约束：本机无 TeX 发行版，`pdflatex`／`xelatex`／`latexmk` 均缺） —— `SKILL.md`「编译方式」 |

---

### 交付说明

- **未新建或修改任何文件**，`D:\Projects\数学建模` 目录状态未变。
- 未声称"已编译通过"：本机无 TeX 发行版，编译发生在用户的网页端。若报错，最常见两类是宏包缺失与 `\Problem`／`\Team` 未替换；把报错原文整段贴回来即可定位。
- 上手第一步：改 `\Problem`（A–F 之一）与 `\Team`（队号），删掉摘要页那行红色占位，然后从 `Begin your paper here` 处开始写。

### 相关文件路径（绝对路径）

- 读取并遵循的 skill：`D:\Projects\数学建模\.claude\skills\mcm-latex-format\SKILL.md`
- 骨架基线（本骨架的逐字来源）：`D:\Projects\数学建模\.claude\skills\mcm-latex-format\assets\mcm-2027-summary.tex`
- 官方原件（事实核对用）：`D:\Projects\数学建模\corpus\official\MCM-ICM_Summary.tex`
- 事实基线（全部指针指向它）：`D:\Projects\数学建模\corpus\official\INDEX.md`
````

### 4.3 GREEN-2 逐项判定（Step 8，**全中才通过**）

判据见 §0。逐项在 GREEN-2 的 `.tex` 全文里核对：

| # | 应有 | GREEN-2 的原文（逐字） | 判定 |
| :--- | :--- | :--- | :--- |
| 1 | 三栏摘要页结构 | `\parbox[t]{0.3\linewidth}{\begin{center}\textbf{Problem Chosen}\\ ...}` ／ `& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2027\\ MCM/ICM\\ Summary Sheet}\end{center}}` ／ `& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{Team Control Number}\\ ...}` | **命中** |
| 2 | 页眉 `\lhead{Team \Team}` + `\rhead{Page \thepage}` | `\lhead{Team \Team}`、`\rhead{}`（前置区）；其后 `\rhead{Page \thepage\ }` | **命中**（且沿用官方模板的 `\lhead`／`\rhead` 形式，未改用 `\fancyhead`） |
| 3 | `\thispagestyle{empty}` + `\vspace*{-16ex}` | `\thispagestyle{empty}` 与 `\vspace*{-16ex}` 相邻两行，原样未被替换 | **命中** |
| 4 | `\setcounter{page}{1}` | `\newpage` 之后 `\setcounter{page}{1}` | **命中** |
| 5 | 不含校名/姓名占位符 | 全文无校名／指导老师／队员姓名／地理区域占位符；`## ②` 表内亦记明「连占位符也不留」 | **命中** |
| 6 | 25 页预算提示 | 顶部注释 `(1) PAGE BUDGET: 25 pages is the maximum, and the limit covers the WHOLE submission -- Summary Sheet, solution body, Table of Contents, Reference List / Bibliography, notes pages, appendices and code... The ONLY part that is not counted is the "Report on Use of AI" section, which goes AFTER the 25 pages.` | **命中** |
| | | | **6/6 → 通过** |

**GREEN-2 同时满足 `SKILL.md` 的 `## 检查清单` 全部 12 条**（逐条核过）：① 完整全文单代码块；documentclass／geometry 原样；三栏年份 2027；`\thispagestyle{empty}` + `\vspace*{-16ex}`；红色说明已换占位（`% Delete the red placeholder line below...` + 红色占位行）；页眉队号+页码且无 `of 25`（顶部注释 (5) 还明写 "Do NOT add 'of 25'"）；`\setcounter{page}{1}`；两宏都在且注释提示替换（注释 (3)）；无身份标识占位符（注释 (4)）；25 页口径（注释 (1)）；纯 ASCII（注释 (8)）；② 为三列 20 项，每项带分级与 `INDEX.md` 指针。

**检查清单未否证输出**（通则第 5 条）：GREEN-2 的交付物**同时**通过 6 项判据与 12 条自检——不存在"按其自检，skill 自己的参考输出不合格"的情形。

### 4.4 关于 GREEN 两轮与中途改动

- GREEN-1 跑在 sha1 `b24f01b4…`；随后我把 `## 输出` ① 表内"摘要占位"一行的**举例文字**从中文 `% 在此粘贴摘要（须容于单页）` 改成英文 `% PASTE YOUR SUMMARY HERE -- it must fit on this one page`。改动理由：那一行与「常见失分点」第 11 条（骨架须纯 ASCII）**自相矛盾**，属通则第 5 条禁止的"清单否证契约自身的输出"。GREEN-1 自己就发现了这个矛盾（其 hand-back 写「摘要占位用英文，不用 skill 里举例的中文注释」）。
- 改完冻结（sha1 `a743150f…`）后**重跑** GREEN-2，跑在冻结版上，仍 6/6。故该改动**不影响**任何一条判据，两轮结果一致。
- 另有一处**派发后**追加：检查清单加了「摘要页的官方红色说明文字已换成摘要占位（不是原样留着）」一条（对应 `## 输出` ① 早已要求的动作）。该条**不属于** Step 3 的 6 项判据；GREEN-2 恰好满足它。

---

## 5. 实际命令输出

### 5.1 工具链探测（`pdflatex` / `xelatex` / `latexmk` / `pdfinfo` / `pandoc`）

```
=== toolchain probe ===
pdflatex: MISSING
xelatex: MISSING
latexmk: MISSING
pdfinfo: MISSING
pandoc: MISSING
```

### 5.2 官方模板行号核对（10 处，全部命中）

```
cd "D:/Projects/数学建模" && F=corpus/official/MCM-ICM_Summary.tex && for spec in "5:documentclass" "7:geometry" "23:lhead" "36:thispagestyle" "37:vspace" "40:Summary Sheet" "54:delete these instructions" "68:setcounter" "69:rhead" "76:end"; do n="${spec%%:*}"; pat="${spec#*:}"; line=$(sed -n "${n}p" "$F"); case "$line" in *"$pat"*) echo "OK   :$n  $pat";; *) echo "FAIL :$n  want=$pat  got=$line";; esac; done
```
```
OK   :5  documentclass
OK   :7  geometry
OK   :23  lhead
OK   :36  thispagestyle
OK   :37  vspace
OK   :40  Summary Sheet
OK   :54  delete these instructions
OK   :68  setcounter
OK   :69  rhead
OK   :76  end
```

### 5.3 修正副本与官方原件的差异（代码层面只差年份一处）

```
cd "D:/Projects/数学建模" && diff <(grep -v "^%%" corpus/official/MCM-ICM_Summary.tex) <(grep -v "^%%" .claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex)
```
```
33c33
< 	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2026\\ MCM/ICM\\ Summary Sheet}\end{center}}
---
> 	& \parbox[t]{0.3\linewidth}{\begin{center}\textbf{2027\\ MCM/ICM\\ Summary Sheet}\end{center}}
```

### 5.4 编码与行数（修正副本 0 个非 ASCII 字节）

```
.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex | bytes: 4111 | non-ascii bytes: 0
corpus/official/MCM-ICM_Summary.tex | bytes: 2733 | non-ascii bytes: 0
```

```
$ wc -l .claude/skills/mcm-latex-format/SKILL.md
83 .claude/skills/mcm-latex-format/SKILL.md
```

### 5.5 官方 `.docx` 的标题栏旁证（INDEX §3.1 冲突 4 的旁证，实测）

```
cd "D:/Projects/数学建模" && python -c "
import zipfile,re
z=zipfile.ZipFile('corpus/official/MCM-ICM_Summary.docx')
d=z.read('word/document.xml').decode('utf-8',errors='replace')
txt=re.sub(r'<[^>]+>','',d)
print('2026 count:', txt.count('2026'), '| 2027 count:', txt.count('2027'))
i=txt.find('2027')
print(repr(txt[max(0,i-200):i+120]))
"
```
```
2026 count: 0 | 2027 count: 1
'\r\nProblem ChosenABCDEF2027MCM/ICMSummary SheetTeam Control Number1111111Use this template to begin typing the first page (summary page) of you'
```

### 5.6 frontmatter 校验

```
fm keys: ['name', 'description']
description length: 191
starts with Use when: True
```

（`description` < 500 字符；只含触发条件，不概括流程；含 `论文排版`、`LaTeX 格式`、`格式合规`、`LaTeX skeleton`、`format the paper` 五个要求的中英触发词。）

### 5.7 冻结哈希

```
b24f01b40ef68422836b6aa1834460864b177dd1 *.claude/skills/mcm-latex-format/SKILL.md   # GREEN-1 所依据
a743150fd64cfcbbb4abfa0f66b3037383161d77 *.claude/skills/mcm-latex-format/SKILL.md   # 冻结版，GREEN-2 所依据
4e472ce5b5fe561f3062b58c57a526fce8173a4a *.claude/skills/mcm-latex-format/assets/mcm-2027-summary.tex
```

---

## 6. 偏离与顾虑

- **D1（重要）：两次 RED 都被污染，且"remote"隔离没有生效。** Run A 自行读取了含 Task 4 验收标准的计划文档与官方语料；Run B 虽用 `isolation: "remote"` 派发，但**同样读到了仓库里的语料**，并且**在仓库根目录写出了文件**——说明该隔离在本环境下并未把它与工作目录隔开。两次 prompt 都只有场景正文，污染非我方 prompt 所致。**我未能取得冷启动 RED**：本任务没有可"复制到仓库外"的 fixture（场景是纯生成，无输入文件），而移动仓库内既有文件在上一轮已被权限系统拒绝、本轮我没有重试。**结论的稳健性**：污染方向是**抬高**命中率，故 RED 实测的缺口只会**少**不会多；且 Run B 在**手握官方模板**的情况下仍丢了第 3、4 两项，这恰恰证明缺的不是"官方原文"而是"以官方模板原样为基线"这条纪律——即本 skill 的核心。**请裁定**是否需要补一次真正冷启动的 RED。
- **D2：Run B 在仓库根目录留下了一个新文件** `mcm-paper-skeleton.tex`（其自己写的交付物）。我已把它的内容**原样复制**到 `tests/results/latex-format-baseline-runB.tex` 归档（受版本控制），然后删除了仓库根目录那份。仓库根目录的干净状态已由 `git status` 复核。**未触碰任何既有文件。**
- **D3：Run B 指出修正副本的注释是中文，并断言其在 pdfLaTeX 下会编译失败。** 该断言**我无法在本机验证**（无 TeX 工具链），且属 `corpus/official/` 之外的机制性断言，**不采纳为事实**。但它指向的风险是实的，处理办法**不需要**采纳该断言：我已把修正副本的注释块改为**纯 ASCII 英文**（实测 0 个非 ASCII 字节，与官方原件一致），并在 skill 里以**操作纪律**（`[社区]`）+ 错误排查提示的形式写入「常见失分点」第 11 条，**未**写成官方要求、也未声称已验证编译。
- **D4：GREEN-1 与 GREEN-2 之间有一次 skill 改动**（把 `## 输出` ① 的中文示例注释改为英文）。理由与影响见 §4.4；改后重跑 GREEN-2，结论不变。冻结 sha1 已记录。
- **D5：`isolation: "remote"` 的实际行为与预期不符**（见 D1），这会影响本项目后续任何想靠它取冷启动基线的任务；建议在计划层面记录。
- **D6：`SKILL.md` 里保留了"官方模板行尾多余的 `\end`"这一条**（常见失分点 10）。我**没有**断言"`\end{document}` 之后的内容不被处理"这类 LaTeX 行为（无本地工具链可验证、也非 `corpus/official/` 内出处），只陈述"它是官方原件自带的、修正副本原样保留、新内容加在 `\end{document}` 之前"。
- **D7：本 skill 不承诺编译验证**（通则第 6 条）。它只产出 `.tex`，并提示网页端报错时把报错原文贴回。本记录中**没有**任何"已编译通过"或页数实测的断言。

