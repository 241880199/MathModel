# M6 前置流水线 — 开工前侦察证据

日期：2026-09-23（2026-09-24 补字号直方图一条，见下）
对应设计：`docs/superpowers/specs/2026-09-23-m6-corpus-pipeline-design.md` §2

本目录是设计文档 §2「素材实况」的**逐字证据**。归档在此而非 `build/` 下的理由：教训通则 7——`mcm-latex-format` 的 GREEN-1 证据只写进 gitignore 目录，**已永久丢失**。

## 可复现命令

```bash
cd "D:/Projects/数学建模"
python tools/scan_watermarks.py                     # 重新生成 watermark-scan.json
python tests/papers/recon/heading_size_hist.py      # 重新生成 reports/b2-size-histogram.txt
```

两者都是纯读操作，不改动任何原件；输出一律字节级 + LF。

## 文件说明

| 文件 | 证明什么 |
| :--- | :--- |
| `watermark-scan.json` | 201 份 PDF 的逐份扫描结果：页数、水印厂商、水印对象数、是否扫描件 |
| `before_p1.png` / `after_p1.png` | 2025 A 题 `2500836.pdf` 第 1 页去水印前后对比 |
| `before_p3.png` / `after_p3.png` | 同上第 3 页（含图页）——证明**水印是覆盖层，摘除后图表同时变干净** |
| `y2022_p2.png` | 2022 年 `2200289.pdf` 第 2 页——证明 **2022 那 44 份确实无水印** |
| `wm-font-coverage.txt` | **水印 span 字体并非全语料一致**：2025 是 `MicrosoftYaHei` 72pt，2023/2024 是 `KaiTi`/`SimHei` 74.4–83.4pt；`is_watermark_span` 命中 43/120 |
| `wm_font_probe.py` | 上一行的复现脚本（只读）；同时实测 `find_watermark_xrefs` 在 201 份上的判别力 |
| `heading_size_hist.py` | 复现 `tools/papers/textmd.py` 标题阈值的依据：43 份的字号→字符数直方图，以及 `HEADING_DELTA` 的可行区间交集 `(0.9100, 1.0600]`（`1.0` 是其中唯一的 0.1 倍数）。输出落在 `tests/papers/reports/b2-size-histogram.txt`（2026-09-24 补） |

**为什么生成脚本本身也入库**：上面那张表的每一条都是"某份证据证明某条结论"。生成器只留在
`build/`（被 gitignore）时，结论可读、生成过程不可复现——而本项目已在通则 7 上付过一次
代价。一次性演示脚本（`build/mutation_runner*.py`、`build/crash_probe.py`）不在此列：
它们不产出被引用的证据文件。

## 关键结论（与设计文档 §2 对应）

- 总数 **201 份 / 9,397 页**；有水印 **120**、无水印 **81**、扫描件 **32**
- 水印三个厂商：`校苑数模`（2023/2024，72 份）、`校苑数模公众号`（2025，43 份）、`英伽教育`（2023，5 份）
- 水印形态：Adobe 标准水印 Form XObject（`/PieceInfo` + `/Private /Watermark`）+ 独立 `/OC` 图层，红色 72pt 微软雅黑，**压在正文与图表之上**
- **2022 的 44 份无水印**——`y2022_p2.png` 为证
- **水印的 span 字体按年份换过**：2025 那 43 份是 `MicrosoftYaHei` 72pt，
  2023/2024 那 77 份是 `KaiTi` 74.4/76.5pt 与 `SimHei` 83.4pt。
  「按字体+字号过滤水印字」对 2025 成立，对 2023/2024 **不成立**——
  实测 `is_watermark_span` 命中 43/120。详见 `wm-font-coverage.txt`（2026-09-23 补）
- 抽样 2025 十篇：**4 篇矢量数学 / 6 篇文本数学**——矢量数学的符号不在文本层，此项已否决"字形层交叉校验公式 OCR"的技术路线

## 未归档的中间产物

`build/` 下留有 `wmtest/clean.pdf`（去水印测试版，2.4MB）与 `pipprobe/`（pip dry-run 报告）。二者**均为临时产物**，不属于证据，未纳入版本控制。仓库根目录当前**无 `.gitignore`**。
