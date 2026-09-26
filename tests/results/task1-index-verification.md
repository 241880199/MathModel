# INDEX.md §5 校验记录 —— 原始 grep 输出（未滤去 `INDEX.md`）

本文件保存 `corpus/official/INDEX.md` §5「校验记录」所引用的**原始输出**。

原先该指针指向 `.superpowers/sdd/task-1-report.md`，但 `.superpowers/sdd/.gitignore` 内容为 `*`，**该目录整片不受版本控制**，导致 `INDEX.md`（全套 skill 的唯一事实基线）把一个复现入口留在了分支之外。2026-09-22 终审修复轮次把原始输出挪入受版本控制的 `tests/results/`，并把 INDEX 的指针改指本文件。

## 1. 简报指定的四字符串 grep（`grep -rl`，**未**滤去 INDEX.md）

在 `corpus/official/` 下执行：

```
$ cd "D:/Projects/数学建模/corpus/official" && for s in "25 page limit" "Team # 0000000, Page 6 of 25" "less than 25MB" "no page limit"; do printf '%s -> ' "$s"; grep -rl "$s" . 2>/dev/null | tr '\n' ' '; echo; done
25 page limit -> ./INDEX.md ./instructions.html 
Team # 0000000, Page 6 of 25 -> ./INDEX.md ./instructions.html 
less than 25MB -> ./INDEX.md ./instructions.html 
no page limit -> ./Contest_AI_Policy.txt ./INDEX.md ./instructions.html ./MCM-ICM_Tips.txt 
```

`INDEX.md` 自身命中属**预期**：本索引复述了这四个字符串，故它必然出现、无验证价值。INDEX §5 记录的是**滤去 `INDEX.md` 自身之后**的结果：

```
25 page limit -> ./instructions.html
Team # 0000000, Page 6 of 25 -> ./instructions.html
less than 25MB -> ./instructions.html
no page limit -> ./Contest_AI_Policy.txt ./instructions.html ./MCM-ICM_Tips.txt
```

**结论**：四个字符串**全部命中至少一个本地官方文件**，无需因 grep 未命中而删条目或降级。

## 2. 补充说明（摘自同轮校验记录）

- 核对期生成的临时转写文件（`_*.plain.txt`，如 `_instructions.plain.txt`、`_faq.plain.txt`、`_resources.plain.txt`）在核对完成后**已删除**，未入库，故不出现在上述结果里。
- 二进制 PDF 因文本流被压缩，`grep` 不能直接命中其内部字符串；本索引对 PDF 的引用一律以 pdftotext 转出的**同名 `.txt`** 为准（`Contest_AI_Policy.pdf` ↔ `.txt`、`MCM-ICM_Tips.pdf` ↔ `.txt`、`UMAP-2003-judges-commentary.pdf` ↔ `.txt`、`MCM-directors-overview.pdf` ↔ `.txt`）。
- 该轮另跑过「新增两份材料未引入新命中」的旁证检索，结果同上（`INDEX.md` 自身命中属预期）。
