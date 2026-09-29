---
name: mcm-plot-restate
description: 假 skill（Task 7 的变异 fixture）：含指针，但重述了规范数值（不超过 1.20 / 比值中位 0.951）⇒ 只用来证明「复述数值」这条规则真的会红。不是交付物。
---

# mcm-plot-restate（假 skill · fixture）

**这不是一个可用的 skill**，只是 `check-spec-pointers.py` 的变异样本：
它是三种形态里**重述数值**的那一份 —— 指针在（`K2` 应绿），但把规范里的数搬了过来。

## 指针

- 规范正文：`references/house-style.md`（指针在 ⇒ `K2` 绿）。

## 设计要点（**故意犯规：重述了规范数值**）

- 图宽与正文宽之比**不超过 1.20**、**比值中位 0.951** ⇒ 这正是要抓的形态：重述 = 造第二份权威。
