# PROVENANCE —— 随 skill 入库的第三方字体

本目录是**第三方二进制**（四档 OTF）与**两份许可原文**。规矩（本模块 Global Constraint 10）：
逐件 `git hash-object` · 记来源绝对路径 + 上游包与版本 + 许可标识 + 取件日期 · 许可原文随字体入库 ·
**只许字节级复制、不许手改**（改了哈希就变）。

## 1. 入库件与逐件 `git hash-object`

取件日期：**2026-09-29**（本机）。

| 文件 | 字节数 | `git hash-object` | 上游字体版本 |
| :--- | ---: | :--- | :--- |
| `TeXGyreTermesX-Regular.otf` | 226088 | `e80891eeb992f306596eb69a5a764b600186978b` | 2.004 |
| `TeXGyreTermesX-Italic.otf` | 217888 | `1707ff148a8f1af1ce9b5cb7382a2b8af3b28000` | 2.004 |
| `TeXGyreTermesX-Bold.otf` | 209828 | `5b5f0228b282abbb7ff9ad64e979b96c2bcaacdb` | 2.004 |
| `TeXGyreTermesX-BoldItalic.otf` | 220832 | `8ae3031ab56efd92f2340ef4ea0eba8c761e87a3` | 2.004 |
| `GFL.txt` | 1377 | `604bf7597db741c93073e937ceb2afd18458201d` | ——（许可原文） |
| `LPPL.txt` | 19102 | `1b57559a8320cc9ff85481e2bc1a0eb5e9620377` | ——（许可原文） |

复跑（仓根）：

    for f in Regular Italic Bold BoldItalic; do \
      git hash-object ".claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-$f.otf"; done

## 2. 来源（绝对路径）

字体四个文件**字节级复制**自**本机 TeX Live**：

    D:/Software/texlive/2026/texmf-dist/fonts/opentype/public/newtx/TeXGyreTermesX-{Regular,Italic,Bold,BoldItalic}.otf

- 发行版：**TeX Live 2026**（`D:/Software/texlive/2026/release-texlive.txt` 首行 "TeX Live ... version 2026"）。
- 上游包与版本：**`newtx` 1.756**（`D:/Software/texlive/2026/tlpkg/tlpobj/newtx.tlpobj` 的
  `name newtx` / `catalogue-version 1.756`）。
- ⚠️ **入库动机**：论文实际嵌的就是这一族（编译 tiny `newtxtext`+`newtxmath` 文档后 `fitz.get_fonts()`
  报 `basefont='RFQQLD+TeXGyreTermesX-Regular'`）⇒ 取它而不是上游 `tex-gyre/texgyretermes-*`。
  入库换掉的是"**依赖本机 TeX Live 路径**"这一环境耦合（设计 §11.2）。

## 3. 许可 —— **核到"这几份文件"这一级**

### 3.1 文件级（**最强证据，来自 OTF 自己的 name 表**）

四份 OTF 的 `name` 表 `nameID 0`（Copyright / 许可声明）**逐字相同**，同时声明**两套**许可：

> Copyright 2006, 2009 for TeX Gyre extensions by B. Jackowski and J.M. Nowacki (on behalf of TeX users
> groups). This work is released under the **GUST Font License** -- see
> **http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt** for details.
>
> Copyright (c) 2015--2023 Michael Sharpe, released under the **equivalent LPPL license**. (Modified all
> small cap glyphs to larger size, renamed originals as petite caps, added superior letters and figures.
> Changed positions of dots above i, j, ij, iogonek and idotbelow to match URW precursors.)

复跑：

    python -c "from fontTools.ttLib import TTFont; \
    print(TTFont('.claude/skills/mcm-plot-python/assets/fonts/TeXGyreTermesX-Regular.otf',lazy=True)['name'].getDebugName(0))"

⇒ 适用许可是**两套并存**：上游设计（TeX Gyre Termes）**GFL**，`newtx` 的修改（Michael Sharpe）
**LPPL**。**两套全文都随字体入库**（GFL 明确要求许可随字体分发）。

### 3.2 包级（佐证）

`D:/Software/texlive/2026/tlpkg/tlpobj/*.tlpobj` 的 `catalogue-license` 字段：

| tlpobj | `catalogue-license` |
| :--- | :--- |
| `newtx.tlpobj` | `lppl1.3` |
| `tex-gyre.tlpobj` | `gfl` |
| `tex-gyre-math.tlpobj` | `gfl` |

复跑：

    grep -E "^(name|catalogue-license|catalogue-version) " D:/Software/texlive/2026/tlpkg/tlpobj/{newtx,tex-gyre,tex-gyre-math}.tlpobj

## 4. 许可原文的取回（取回途径与日期）

⚠️ **本机 TeX Live 的 `doc/` 树是精简的**（`D:/Software/texlive/2026/texmf-dist/doc/` 下只有
`latex/koma-script/`），**没有任何许可文件** ⇒ 许可全文**另处取回**：

| 入库件 | 取回 URL | HTTP | 日期 |
| :--- | :--- | :--- | :--- |
| `GFL.txt` | `http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt` | 200 | 2026-09-29 |
| `LPPL.txt` | `https://www.latex-project.org/lppl/lppl-1-3c.txt` | 200 | 2026-09-29 |

- `GFL.txt` 的 URL 就是**字体 name 表里逐字给的那个 URL**（上面 §3.1）—— 取回后逐字入库
  （1377 字节，全 LF）。
- `LPPL.txt` 是 **LPPL 1.3c**（2008-05-04）全文；`newtx` 的 `catalogue-license` 是 `lppl1.3`，
  字体声明写的是"equivalent LPPL license"。1.3c 是 1.3 的现行修订版（`newtx` 的 README 指向
  `ctan.org/license/lppl1.3`，该页即指向 LPPL 1.3c）。

复跑：

    curl -sSL -o /dev/null -w "%{http_code}\n" http://tug.org/fonts/licenses/GUST-FONT-LICENSE.txt
    curl -sSL -o /dev/null -w "%{http_code}\n" https://www.latex-project.org/lppl/lppl-1-3c.txt

## 5. 这条 provenance 的**射程**（写实）

- 它证明的是"**入库的就是这几份文件**"（逐件哈希 + 字节级复制可复现）；
- **不证明**"这份字体与论文正文逐字形一致"——罗马字用的是同一族，但**数学**是另一套实现
  （`mathtext` 的 `stix` vs 论文的 `NewTXMI` + `txexs`），逐字形同一做不到（设计 §7.1 / §11.1）。
