# Input and output contract

## Suggested task parameters

```yaml
input_dir: /path/to/papers
topic: optional review topic
focus_questions: []
output_dir: /path/to/output
language: zh-CN
slide_target: 15-25
evidence_format: xlsx
figure_dpi: 300
template: optional/path/to/template.pptx
```

Paths are examples only. Resolve supplied paths at runtime; never embed them in the skill.

## Default output layout

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

Use names requested by the user. Keep temporary renders, extraction dumps, scripts, and validation logs outside `output_dir` unless explicitly requested.

## Speaker-note minimum

For each substantive slide, notes should include:

- claim and evidence status;
- source papers and PDF/printed pages;
- figure number/panel where relevant;
- detailed interpretation;
- applicable conditions and limitations;
- alternative explanations or unresolved questions.

## Delivery report

State the paper count, duplicate count, unreadable/partial count, slide count, selected-figure count, and the validations actually run. Link all deliverables. Do not state that a visual, conversion, or scientific check passed unless it was performed.
