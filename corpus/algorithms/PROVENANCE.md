# PROVENANCE —— 算法归档来源与处置记录

## 1. 来源

| 项 | 值 |
| :--- | :--- |
| 仓库 | `HuangCongQing/Algorithms_MathModels` |
| URL | https://github.com/HuangCongQing/Algorithms_MathModels |
| 描述 | 【国赛】【美赛】数学建模相关算法 MATLAB 实现（2018 年初整理） |
| **取用 commit** | **`e15b0e9053b11f08b5ce1e3492c4acb444409c8b`**（2022-12-26 01:27:52 +0800，`Update README.md`，亦即最后一次提交） |
| 上游星标 / fork | 2,437 / 535（2026-09-23 记录） |
| 归档日期 | 2026-09-23 |
| 归档时全仓体量 | 127.44 MB / 3,079 条目 |

## 2. 许可状态

仓库根目录 `LICENSE` 为 **MIT License，`Copyright (c) 2014-2018 Chongqing`**。原文副本见 `LICENSE`。

**须知的限定**：仓库约 78% 的文件是**随书源码**（《MATLAB神经网络原理与实例精解》等 5 种教材的配套程序）。**上传者不是这些书的著作权人，MIT 授权覆盖不了它们。**

**本项目的处置**：2026-09-23 用户确立政策——**第三方素材不因许可证排除，按价值判断收录**（见 `docs/mcm-suite-todo.md` §E，该条取代设计文档 §8 的旧政策）。故随书源码一并收录，但**在 `INDEX.md` 里降为二级/三级并标明来源性质**，以免日后把教辅代码误当自有资产。

**引用时**：上游 `README.md` 要求 *"Fork 或借鉴请注明出处 [@双愚](https://github.com/HuangCongQing)"*，照办。上游同时自述 *"部分参考于 NarcissusHliangZhao/Algorithm_Implementation_in_MatModel"*——即上游自己也是二次来源。

### 2.1 更正：`GraphTheory(图论)/basic/` 不是仓库作者的作品

**该目录是第三方工具箱，不是本仓库作者自有代码。** 它是一套 **grTheory 图论工具箱**，作者
**Sergiy Iglin**（`siglin@yandex.ru`，http://iglin.exponenta.ru），见 `basic/readme.txt` 的文件头与
各函数的署名注释。首版 `INDEX.md` 与 `PROVENANCE.md` 把它一并算作"作者自有"，**已更正**。

该工具箱在 R2025b 上**部分失效**（详见 `INDEX.md` §10.4）：`grMaxFlows` 用了已被移除的
`linprog` 九参签名，`grTravSale` 依赖未随附的外部求解器 `miqp`；`grShortPath`、`grMinSpanTree`
经交叉验证数值正确。使用时**逐个函数验，别整包信任**。

## 3. 收录了什么

**收录 1,262 个文本文件**，落在 `src/`，保留上游原始目录名。

| 扩展名 | 数量 |
| :--- | ---: |
| `.m` | 1,200 |
| `.txt` | 57 |
| `.cpp` | 2 |
| `.md` / `LICENSE` / `README`（无扩展名工具包说明） | 3 |

上游原始体量 **2.37 MB**，转 UTF-8 后 **4.8 MB**——中文在 GBK 下 2 字节、UTF-8 下 3 字节，膨胀属预期。

## 4. 剔除了什么

上游共 2,828 个 blob，收录 1,262 个，**剔除 1,566 个 / 125.05 MB**：

| 剔除项 | 数量 | 体量 | 理由 |
| :--- | ---: | ---: | :--- |
| `.pdf` | 41 | 84.59 MB | 主要体量；含 3 个 `Final Solution.pdf`（疑为真题论文，另见 §6） |
| `.bmp` | 1,114 | 20.69 MB | 教材插图，无思考价值 |
| `.mat` | 123 | 5.04 MB | 数据 blob；TSP 用的 `china.mat` 等按需重取 |
| `.tif` / `.png` / `.gif` / `.jpg` | 183 | 8.56 MB | 同上，教材插图 |
| `.mdl` | 16 | 1.40 MB | Simulink 模型 |
| `.7z` | 1 | 1.27 MB | 压缩包 |
| 无扩展名数据 | 1 | 1.13 MB | `《MATLAB图像处理》…/chap15/datafile_name` |
| `.fig` / `.html` / `.db` / `.ps` / `.exe` / `.xls` / `.dat` / `.data` / `.data-numeric` / `.asv` / `.in` / `.out` | 85 | 2.09 MB | 演示页、MATLAB 自动备份、可执行文件与零散数据 |

**全部可依 §1 的 commit 重新取回。**

取用方式：`--filter=blob:none` + 稀疏检出，只拉 `*.m` / `*.txt` / `*.md`，故 1,114 个 `.bmp` **从未下载**。
2 个 `.cpp`（`dijkstra.cpp` / `floyd.cpp`）与 `gaot/README` 因不在稀疏模式内，由 `raw.githubusercontent.com` 按 commit 单独补取。

## 5. 处置动作（可复现）

1. `git clone --depth 1 --filter=blob:none --sparse`（须 `-c http.sslBackend=schannel`——本机默认 CA 取不到 GitHub 证书）
2. `git sparse-checkout set --no-cone '*.m' '*.txt' '*.md' '/LICENSE'`
3. **编码转码**：883 / 1,259 个文件原为 **GBK**（`gb18030` 解码），转为 UTF-8；其余 376 个 UTF-8 文件**逐字节原样复制**。逐文件对照表见 `.transcode-map.txt`。
4. `LICENSE` 因稀疏模式未命中，由 `raw.githubusercontent.com` 单独取回。

### 5.1 ⚠️ 一次已修正的转码事故（**务必读，别再犯**）

**首版归档有 883 个文件被写坏成 `\r\r\n`（双 CR），全部是我造成的。** 成因是两步叠加：

1. `git sparse-checkout` 在 `core.autocrlf` 生效下把工作树写成 **CRLF**；
2. 我用 Python 的**文本模式**写入（`Path.write_text`），它把每个 `\n` 再翻成 `\r\n` → 原本的 `\r\n` 变成 `\r\r\n`。

后果：MATLAB 在每行行首读到游离的 `\r`，报"解析错误：使用的 MATLAB 语法可能无效"。**我一度据此认定上游有 47 个文件语法错误——其中 46 个是我的锅**，只有 `ahp_common.m` 是真的。

**正确做法**（首版归档已按此重做）：

```bash
cd <clone> && git config core.autocrlf false && git checkout -f .   # 工作树回到 LF
```
```python
# 转码一律用字节级写入，杜绝任何换行翻译
out.write_bytes(src_bytes.decode('gb18030').encode('utf-8'))
```

**教训**：把第三方文件搬进自己的仓库时，**换行符是转码链上最容易被静默改坏的一环**；事后一定要有一条独立校验（本次是 `b'\r\r\n' in bytes` 计数 + MATLAB `checkcode` 复跑）。**跨过这一层去解释"上游代码很差"之前，先排除自己的搬运环节。**

## 6. 待定事项（未处置）

- **3 个 `Final Solution.pdf`**（根目录 0.60 MB + `HeuristicAlgorithm/…/TSP(SA)/` 5.73 MB + `…/TSP(GA)/` 0.61 MB）从命名看**疑为竞赛论文正文**，属 M6 `corpus/papers/` 的候选。**作者与授权均不明，本次未收录、未打开**，仅登记在此，等用户决定是否单独审阅。

## 7. 质量声明

**已于 2026-09-23 做运行验证**（MATLAB R2025b）：一级层 68 个脚本实跑，**44 通过 / 16 失败**，另有 2 个交互式脚本通过、6 个因 GUI 死循环无法无人值守。核心算法另做独立参照的数值验证。**逐字证据在 `tests/algorithms/`**（`run-report.txt`、`numerics-report.txt`、`fixed-report.txt`），结论汇总在 `INDEX.md` §10。

**仍未覆盖的**：上游其余 1,200+ 文件未做质量判断；一级层中"能跑通"的脚本其**数值仍属未验证**（只测了 Floyd、Dijkstra、Huffman、ahp、grShortPath、grMinSpanTree 六项的数值）。

上游代码为 2017–2022 年的中文 MATLAB 教辅/学生级代码，非生产级库。**这是它未被做成 skill 的原因**。已确证的缺陷其净室重写版见 `fixed/`。
