# Scientific Literature Review Deck

A Codex skill for **systematically reviewing scientific PDFs and producing an evidence-traceable, illustrated, and editable literature-review presentation**.

Instead of creating a one-paper-per-slide summary collection, the skill organizes evidence around core scientific questions and builds a coherent narrative:

> Background → Core questions → Key evidence → Mechanistic interpretation → Consensus and disagreement → Research gaps → Implications

## Key capabilities

- Recursively inventories a paper folder, counts PDFs, detects exact duplicates, and records reading failures.
- Reads the methods, results, discussion, conclusions, and figure captions of priority papers instead of relying on abstracts alone.
- Builds a claim–evidence ledger containing DOI information, experimental conditions, quantitative results, limitations, and PDF/printed page references.
- Extracts or crops high-resolution source figures and records their figure number, panel, page, supported claim, and interpretation limits.
- Produces an editable 16:9 PPTX, a PDF preview, an evidence table, per-paper notes, and a source-figure index.
- Draws synthesis and mechanism diagrams with native PowerPoint shapes rather than using generated images to recreate published figures.
- Renders and checks every slide for layout, figure legibility, citations, units, and evidence strength.

## Installation

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/Jiachen-123/scientific-literature-review-deck.git ~/.codex/skills/scientific-literature-review-deck
```

Windows PowerShell:

```powershell
git clone https://github.com/Jiachen-123/scientific-literature-review-deck.git "$env:USERPROFILE\.codex\skills\scientific-literature-review-deck"
```

Restart Codex or open a new conversation so the skill can be discovered.

## Usage

Invoke the skill directly in Codex:

```text
Use $scientific-literature-review-deck to systematically review the papers in "/path/to/papers".
Topic: Effects of chlorite coatings on quartz cementation and feldspar dissolution.
Focus: Evidence linking coating integrity, formation timing, experimental conditions, and reservoir quality.
Save the editable presentation, PDF, evidence table, source-figure index, and per-paper notes to "/path/to/output".
```

At minimum, provide:

- `input_dir`: the folder containing the paper PDFs;
- `output_dir`: a separate folder for final deliverables.

Providing `topic` and `focus_questions` is recommended. If they are omitted, the skill derives a provisional scope and core questions from the literature, states its assumptions, and continues when doing so does not materially change the assignment.

Optional parameters:

```yaml
input_dir: /path/to/papers
topic: review topic
focus_questions: []
output_dir: /path/to/output
language: en
slide_target: 15-25
evidence_format: xlsx
figure_dpi: 300
template: /path/to/template.pptx
```

## Default deliverables

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

File names may be changed to match the user's request. Temporary renders, extraction caches, and validation logs should remain outside the final delivery folder.

## Requirements

The runtime should provide:

- PDF reading, page rendering, and screenshot capabilities;
- PowerPoint authoring, rendering, and layout inspection capabilities;
- spreadsheet support when XLSX output is requested;
- Python 3;
- the Python packages `pypdf` and `Pillow`, used for PDF inventory/delivery checks and contact-sheet generation.

Example script calls:

```bash
python scripts/inventory_pdfs.py INPUT_DIR --output WORK_DIR/inventory.json --summary WORK_DIR/inventory.md
python scripts/make_contact_sheet.py RENDERED_SLIDES --output-dir CONTACT_SHEETS
python scripts/validate_outputs.py --pptx OUTPUT/review.pptx --pdf OUTPUT/review.pdf --evidence OUTPUT/evidence.xlsx --notes OUTPUT/per-paper-notes.md --figures OUTPUT/source-figures
```

## Evidence and quality boundaries

- Every major claim should cite its source paper and page location, distinguishing PDF page numbers from printed article pages.
- Direct observations, author interpretations, and cross-paper synthesis or inference must be labeled separately.
- Quantitative results must retain their units, conditions, and comparison baseline; correlation must not be presented as causation.
- Unreadable, incomplete, encrypted, or poor-quality scanned files are recorded separately. Missing content is never invented.
- Published figures must not be stretched or scientifically altered. Highlights, arrows, and translated explanations should remain editable PowerPoint overlays.
- Automated validators check basic package structure only; they do not replace slide-by-slide visual inspection or scientific judgment.

## Privacy

This repository contains only a reusable workflow, generic scripts, and format specifications. It does not contain paper PDFs, source data, extracted figures, generated presentations, analysis results, chat records, account information, or credentials. All data paths and project parameters are supplied by the user at runtime.

## Repository structure

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

See [`SKILL.md`](SKILL.md) for the complete workflow and operating rules.
