# reproducibility —— 随机源 / 环境 / 落盘 / 路径

**上位**：`SKILL.md` 的指针（① 写代码）。本文件写三件事：**固定随机源** · **结果落盘** · **不写死机器绝对路径**。
**依据标注**：本文件全体 `[社区]` —— 是本套件自订的**工程口径**，官方（`corpus/official/`）**没有任何明文**。
**不声称穷尽**：下列惯用法是常见形态，不是全部；只要求"入口固定随机源 + 结果真的落盘"，不强求你用某一种写法。

---

## ① 固定随机源（可复现的入口）

**要求**：**求解入口**（顶层脚本 / 主函数）一处**显式**设定随机源，且种子是**写死的字面量或配置项**，不是 `time()` / 系统时钟一类不可复现的源。

| 语言 | 惯用法 | 说明 |
| :--- | :--- | :--- |
| MATLAB | `rng(2025, 'twister')` | 顶层入口设一次；子函数**不要**再 `rng`（否则重跑不复现）。 |
| Python | `rng = numpy.random.default_rng(2025)` | 现代推荐：把 `rng` 显式传下去，别用全局 `numpy.random` 隐式状态。 |
| Python | `random.seed(2025)` / `numpy.random.seed(2025)` | 旧式全局种子；能用 `default_rng` 就用它（不受其它库调用全局状态影响）。 |

★ **两条常见坑**：
- **并行 / 多线程**下"每个 worker 各自再播种"会让结果随调度变化 ⇒ 用**可派生的子种子**（`default_rng.spawn(...)` 一类），不要每个 worker 都用同一个常数。
- **不要**在循环里重播同一个种子 —— 那会把独立的随机试验变成同一个。

---

## ② 结果落盘（不许只有打印）

**要求**：凡要进论文数字 / 图 / 表的结果，**必须写到磁盘文件**；`disp` / `print` / `fprintf` 只作**运行时观察**，**不能替代落盘**。

| 语言 | 落盘惯用法 | 典型用途 |
| :--- | :--- | :--- |
| MATLAB | `save('work/workspace-dump.mat', 'X', 'Y')` | 整包工作变量（**非正文转储** ⇒ 不带编号、另置 `work/`） |
| MATLAB | `writetable(T, 'table-1-estimate.csv')` | 表格结果（可直接进论文表） |
| MATLAB | `writematrix(M, 'figure-1-data.csv')` | 数值矩阵（喂给绘图） |
| MATLAB | `exportgraphics(gcf, 'figure-1.png')` / `print(gcf, 'figure-1', '-dpng')` | 图（**排版归 M3**，这里只管落盘） |
| Python | `df.to_csv('table-1-estimate.csv', index=False)` | 表格结果（pandas） |
| Python | `numpy.save('work/workspace-dump.npy', arr)` / `numpy.savetxt(...)` | 数值数组（**非正文转储** ⇒ 不带编号、另置 `work/`） |
| Python | `fig.savefig('figure-1.png', dpi=300)` | 图（matplotlib；**排版归 M3**） |
| Python | `json.dump(payload, f)` | 标量 / 结构化读数 |

★ **落盘的最小形态**见 `assets/scaffold.m` · `assets/scaffold.py`（零参可跑，两侧各演示一遍）。
★ **进正文的成品**文件名带编号，是落盘时的**同一步动作** —— 见 `references/numbering.md`。

---

## ③ 路径处置（不写死机器绝对路径）

**要求**：**可执行语句内**不得出现写死的**机器绝对路径**（`C:\` / `D:\` / `/Users/` 一类）。
**理由**：自己的机器路径**换台机器就跑不了**，也不可复现。

| 反面（写死，换机即废） | 正面（相对 / 可配置） |
| :--- | :--- |
| `load('D:\Projects\数学建模\build\data.mat')` | `load(fullfile('build', 'data.mat'))` |
| `open('/Users/alice/mcm/table1.csv')` | `open(Path('build') / 'table1.csv')`（Python） |
| 绝对路径散落各处 | 顶层设一个 `ROOT` / `OUT_DIR` 变量，其余相对它拼 |

★ **判定边界**：
- 只判**可执行语句内**的路径字面量 —— **注释里出现路径不算**（如一行注释写着本机真实路径，是**文档性说明**，不判违规）。
- 判定是**启发式**（按 `C:\` / `D:\` / `/Users/` 形态找），**有假阳性空间** —— 匹配到不一定是违规，没匹配到也不保证没有别的写死形态。
- **只读输入**（如题面给的绝对路径附件）确需写死时，**挪到配置项**并写进论文的复现说明，别埋在算法里。

★ **本文件不判"跑出来的数对不对"** —— 只要求"入口固定随机源 + 结果落盘 + 路径不写死"这三件工程规范。
