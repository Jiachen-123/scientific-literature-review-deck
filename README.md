# Scientific Literature Review Deck

一个用于 **系统阅读科学论文 PDF，并生成证据可追溯、图文并茂、可编辑文献调研 PPT** 的 Codex skill。

它不会把结果做成“一篇论文一页”的摘要集合，而是围绕核心科学问题组织证据，形成：

> 研究背景 → 核心问题 → 关键证据 → 机制解释 → 共识与分歧 → 研究不足 → 后续启示

## 主要能力

- 递归扫描论文文件夹，统计 PDF、识别完全重复文件并记录读取异常。
- 对重点论文联合阅读方法、结果、讨论、结论和图注，而非只依赖摘要。
- 建立观点—证据台账，记录 DOI、实验条件、定量结果、局限及 PDF/印刷页码。
- 从原文提取或高分辨率裁取关键图，并保存图号、分图、页码和适用限制。
- 生成 16:9 可编辑 PPT、浏览版 PDF、证据表、逐篇笔记和原图索引。
- 使用 PPT 原生形状绘制综合机制图，不用生成式图像重绘论文原图。
- 渲染并逐页检查排版、图像清晰度、引用、单位和证据强度。

## 安装

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/Jiachen-123/scientific-literature-review-deck.git ~/.codex/skills/scientific-literature-review-deck
```

Windows PowerShell：

```powershell
git clone https://github.com/Jiachen-123/scientific-literature-review-deck.git "$env:USERPROFILE\.codex\skills\scientific-literature-review-deck"
```

重新启动 Codex 或开启新对话，使 skill 被发现。

## 使用方式

在 Codex 中直接调用：

```text
使用 $scientific-literature-review-deck，对“/path/to/papers”中的文献开展系统调研。
主题：绿泥石包膜对石英胶结和长石溶蚀的影响。
重点关注：包膜完整性、形成时序、实验条件与储层质量之间的证据链。
请将中文可编辑 PPT、PDF、证据表、原图索引和逐篇笔记保存到“/path/to/output”。
```

至少应提供：

- `input_dir`：论文 PDF 文件夹；
- `output_dir`：独立输出文件夹。

建议同时提供 `topic` 和 `focus_questions`。若未提供主题或重点问题，skill 会基于文献提出暂定范围，并在不影响推进时继续执行。

可选参数示例：

```yaml
input_dir: /path/to/papers
topic: review topic
focus_questions: []
output_dir: /path/to/output
language: zh-CN
slide_target: 15-25
evidence_format: xlsx
figure_dpi: 300
template: /path/to/template.pptx
```

## 默认交付物

```text
output_dir/
├── literature-review.pptx
├── literature-review.pdf
├── evidence-ledger.xlsx
├── per-paper-notes.md
└── source-figures/
    ├── figure-source-index.csv
    └── selected-figures...
```

文件名可按用户要求调整。临时渲染、提取缓存和检查日志不应混入最终交付目录。

## 依赖与配套能力

运行环境需要具备：

- PDF 阅读、页面渲染与截图能力；
- PowerPoint 创建、渲染和布局检查能力；
- 生成 XLSX 时所需的电子表格能力；
- Python 3；
- Python 包 `pypdf` 和 `Pillow`（分别用于 PDF 清单/交付检查与联系表生成）。

脚本示例：

```bash
python scripts/inventory_pdfs.py INPUT_DIR --output WORK_DIR/inventory.json --summary WORK_DIR/inventory.md
python scripts/make_contact_sheet.py RENDERED_SLIDES --output-dir CONTACT_SHEETS
python scripts/validate_outputs.py --pptx OUTPUT/review.pptx --pdf OUTPUT/review.pdf --evidence OUTPUT/evidence.xlsx --notes OUTPUT/per-paper-notes.md --figures OUTPUT/source-figures
```

## 质量与证据边界

- 每个关键结论都应关联来源文献及页码，并区分 PDF 页码与文章印刷页码。
- 明确区分直接观察、作者解释和跨文献综合推断。
- 定量结果必须保留单位、条件和比较基准；相关性不得直接表述为因果性。
- 无法读取、缺页、加密或扫描质量差的文件会单独记录，不补写缺失内容。
- 原文图不拉伸、不篡改数据；圈选、箭头和中文解释使用 PPT 可编辑叠加对象。
- 自动检查脚本只能验证交付包的基本结构，不能替代逐页视觉检查和科学判断。

## 隐私说明

本仓库只包含可复用的工作流程、通用脚本和格式规范，不包含论文 PDF、原始数据、提取图片、PPT 成果、分析报告、聊天记录、账号信息或密钥。实际数据路径和项目参数均由用户在运行时提供。

## 仓库结构

```text
scientific-literature-review-deck/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── evidence-schema.md
│   ├── output-contract.md
│   └── workflow.md
└── scripts/
    ├── inventory_pdfs.py
    ├── make_contact_sheet.py
    └── validate_outputs.py
```

详细执行规则见 [`SKILL.md`](SKILL.md)。
