---
name: mcm-plot-ok
description: 假 skill（Task 7 的变异 fixture）：与 mcm-plot-nopointer / mcm-plot-restate 一起放在 tests/skills/figure-choose/fixtures/fake-skills/ 下，只用来证明引用完整性检查器的两条判据不是恒真。不是交付物。
---

# mcm-plot-ok（假 skill · fixture）

**这不是一个可用的 skill**，只是 `tests/skills/figure-choose/check-spec-pointers.py` 的变异样本。
它与 `mcm-plot-nopointer`、`mcm-plot-restate` 一起构成「一个带指针 / 一个不带 / 一个重述数值」三种形态：
本份是**合格的那一份**——含指针、不含任何规范数值 ⇒ `K2` 与 `K3` 都应判绿。

## 指针

- 规范正文：`references/house-style.md`（**这个 skill 目录内的相对路径就是被核的形态**；只写文件名不算）。
- 本文件**不复述任何规范数值**：阈值、占比、样本读数一律回上面那份文件去读。
