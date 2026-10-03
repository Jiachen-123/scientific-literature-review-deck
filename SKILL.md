---
name: scientific-literature-review-deck
description: Systematically review a folder of scientific PDFs and produce an evidence-traceable, editable literature-review presentation with source figures, speaker notes, an evidence table, and per-paper notes. Use for research synthesis decks where claims must be tied to paper pages and figures; do not use for a quick abstract-only summary or a generic slide redesign.
---

# Scientific Literature Review Deck

Turn a paper folder into a checked, editable review deck organized by scientific questions rather than one-paper-per-slide summaries.

## Required input

Resolve or ask for these values:

- `input_dir`: folder containing papers; recurse into subfolders.
- `topic`: review topic. If omitted, infer a provisional topic from the corpus and state that assumption.
- `focus_questions`: optional priorities. If omitted, derive 3–5 core scientific questions.
- `output_dir`: create a separate directory; never overwrite source papers.
- Optional: language, slide range, presentation template, figure-selection constraints, and whether XLSX is required.

Only ask the user when a missing choice would materially change the scientific scope, files are encrypted/unreadable, or output authorization is absent. Record lesser uncertainties and continue.

## Tool and dependency checks

1. Load the environment's PDF-reading/rendering capability before reading papers.
2. Load the presentation-authoring capability before creating PPTX. Use its required authoring library, finalizer, rendering, and layout checks.
3. Load the spreadsheet capability when producing XLSX; CSV is an acceptable fallback only when the user permits it.
4. Use a PDF renderer capable of 300 dpi or higher for figure crops. Use `pypdf` for deterministic inventory checks when available.
5. Do not generate or redraw literature figures with an image generator. Draw synthesis mechanisms with native editable presentation shapes and label them “Based on literature synthesis” or the requested-language equivalent.

If a named capability is unavailable, report the exact missing capability and use only a functionally equivalent installed tool. Do not claim a skill was loaded when it was not.

## Workflow

### 1. Inventory before interpretation

Run:

```bash
python scripts/inventory_pdfs.py INPUT_DIR --output WORK_DIR/inventory.json --summary WORK_DIR/inventory.md
```

Use SHA-256 to flag exact duplicates. Record page count, metadata, extraction coverage, encrypted files, errors, and relative paths. Treat near-duplicate editions as separate until bibliographic comparison confirms equivalence.

### 2. Build an evidence ledger

For every paper, capture title, authors, year, journal, DOI when present, question, object, methods, conditions, findings, mechanism interpretation, innovation, limitations, topic relevance, reading priority, and evidence locations.

Read every paper's bibliographic page, abstract, conclusion, and figure captions. For priority papers also read methods, results, and discussion. Do not summarize a full paper from its abstract alone. Distinguish PDF page numbers from printed page numbers and record both when available.

Read [references/evidence-schema.md](references/evidence-schema.md) before building the ledger.

### 3. Synthesize by scientific question

Organize the narrative as:

`background → core questions → key evidence → mechanisms → consensus and disagreement → gaps → implications`

For each important claim, label its epistemic status:

- direct observation;
- author interpretation;
- cross-paper synthesis/inference.

State supporting papers and page locations. Preserve units, conditions, comparators, and uncertainty. Do not turn correlation into causation or generalize a local experiment without its boundary conditions.

Read [references/workflow.md](references/workflow.md) for the detailed synthesis and figure-selection procedure.

### 4. Extract only decision-useful figures

Maintain a figure candidate ledger. Select figures that directly support a core claim, discriminate mechanisms, establish methods, or expose disagreement.

- Prefer embedded originals; otherwise render the page at ≥300 dpi and crop.
- Preserve axes, units, legends, scale bars, panel labels, and relevant annotations.
- Do not stretch, retouch data, or alter scientific content.
- Record author, year, title, original figure/panel, PDF page, printed page when visible, supported claim, and limitation.
- Keep the English original unchanged and add editable translated interpretation beside it.
- Put callouts and arrows in the deck as editable overlays, not baked into the source image.

### 5. Author editable deliverables

Choose slide count from evidence density; 15–25 slides is a typical range, not a quota. Use one main claim per slide. Prefer “source figure + interpretation + takeaway” for evidence slides.

Required outputs unless the user narrows scope:

- editable PPTX;
- PDF export;
- evidence ledger in XLSX or approved CSV;
- source-figure directory with index;
- per-paper Markdown notes.

Use native editable shapes, tables, arrows, and text for synthesis diagrams. Put detailed sources, evidence locations, alternative interpretations, and boundary conditions in speaker notes. Keep original screenshots as images rather than rasterizing whole slides.

Read [references/output-contract.md](references/output-contract.md) before authoring and delivery.

### 6. Validate and repair

Use the presentation finalizer required by the installed presentation capability. Render every final slide and inspect each slide at readable size; contact sheets are for overview only. Check overflow, overlap, image legibility, figure-caption consistency, units, page citations, unsupported certainty, logic, and duplication.

Render the exported PDF and compare all pages with the final PPTX. Render every spreadsheet sheet and scan formulas for errors when formulas exist.

Run the deterministic delivery check:

```bash
python scripts/validate_outputs.py \
  --pptx OUTPUT/review.pptx \
  --pdf OUTPUT/review.pdf \
  --evidence OUTPUT/evidence.xlsx \
  --notes OUTPUT/per-paper-notes.md \
  --figures OUTPUT/source-figures
```

Fix failures before delivery. Report checks that could not be performed; never claim unrun validation.

## Failure handling

- **Unreadable or scanned PDF:** try page rendering/OCR when available; record missing pages or low confidence. Never invent missing text.
- **Encrypted PDF:** ask for an unlocked copy or password; continue other papers.
- **No extractable figure:** render and crop the page; preserve scientific labels.
- **Inconsistent findings:** compare sample type, temperature, time, pressure, pH, apparatus, minerals, analytical method, and model assumptions before calling a contradiction.
- **Insufficient evidence:** lower claim strength and state what remains unanswered.
- **Missing template:** use a restrained 16:9 scientific design; do not stop unless branding is mandatory.
- **Conversion unavailable:** preserve the editable PPTX, report the missing converter, and do not claim PDF validation.

## Portable use

Never hard-code machine paths. Accept paths through CLI arguments or task parameters, resolve them at runtime, and keep temporary files outside the source folder. Scripts may require `pypdf` or Pillow and must emit a clear dependency error when missing.
