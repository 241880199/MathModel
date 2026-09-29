---
name: mcm-schematic
description: 假 skill（Task 7 的变异 fixture）：只用来证明 `check-spec-pointers.py` 的家族正则 `FAMILY_RE` 里 `mcm-schematic` 这条备选**真的在射程内**（缺指针 ⇒ `K2` 判红）。不是交付物。
---

# mcm-schematic（假 skill · fixture）

**这不是一个可用的 skill**，只是 `tests/skills/figure-choose/check-spec-pointers.py` 的变异样本。
它压的是家族正则的**另一条备选**（`FAMILY_RE = ^(?:mcm-plot-.+|mcm-table|mcm-schematic)$` 里的
`mcm-schematic`）：本份**缺指针** ⇒ `K2` 应判红。
★ 删掉正则里的 `|mcm-schematic` 这条备选，本份就**掉出射程** ⇒ M43 里那条预期红随即消失 ⇒ M43 转 RED-BAD。
（这正是它存在的理由：只放一份**干净**的同名样例证不到这条腿 —— 那样删掉备选它也只是掉出射程，
M43 的交叉断言一字不变，照样 RED-OK。）

## 指针

- 规范正文见 `house-style.md`（**这正是要抓的形态**：只写了文件名，没写 skill 目录内的相对路径）。
- 本文件**不复述任何规范数值**：阈值、占比、样本读数一律回规范里去读（故 `K3` 该判绿）。
