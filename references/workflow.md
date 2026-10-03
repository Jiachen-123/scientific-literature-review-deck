# Detailed review workflow

## Contents

1. Triage and reading depth
2. Scientific-question synthesis
3. Figure extraction
4. Deck construction
5. Validation

## 1. Triage and reading depth

Start from a complete recursive inventory. Exact duplicates share a SHA-256 hash; keep one canonical copy in the ledger and list all duplicate paths. Detect reviews, conference abstracts, supplemental files, and multiple versions, but do not discard them automatically.

Assign reading priority only after scanning titles, abstracts, conclusions, and captions:

- **A:** directly answers a core question, supplies quantitative constraints, tests mechanisms, or is a field-defining source.
- **B:** supplies context, a comparison, or a secondary mechanism.
- **C:** weakly related or methodologically unusable for the topic.

For A papers, inspect methods, experimental/sample conditions, results, discussion, conclusion, and relevant captions. For B papers, read the sections needed for the claim being used. C papers still receive a traceable note explaining why they are peripheral.

## 2. Scientific-question synthesis

Before slide authoring, draft 3–5 core questions. Build a claim matrix with papers as columns or source lists. For each claim, ask:

1. What was directly measured or observed?
2. What mechanism did the authors infer?
3. Under which sample, experiment, model, or site conditions does it hold?
4. Which papers independently support it?
5. Which papers disagree, and can apparatus, material, boundary conditions, scale, or analysis explain the difference?
6. What evidence would discriminate competing explanations?

Use language proportional to evidence: `shows` for direct observations, `supports/is consistent with` for interpretation, and `suggests` for cross-paper inference.

## 3. Figure extraction

Create candidates while reading, not after writing slides. A selected figure must answer all three questions:

- What does the figure show?
- Which claim does it support or challenge?
- What conditions or limitations govern interpretation?

Prefer original raster extraction when the PDF stores a clean figure image. For vector/composite pages, render at 300–450 dpi and crop without removing scientific context. Preserve the uncropped rendered page in temporary work when auditability matters.

## 4. Deck construction

A strong default sequence is:

1. Cover
2. Scope and core questions
3. Corpus distribution and research history
4. Evidence types and comparability
5. Thematic evidence sections
6. Editable synthesis mechanism diagram
7. Consensus, disagreement, and boundary conditions
8. Evidence gaps
9. Testable next steps
10. Core conclusions
11. References and appendix pointers

Do not allocate one slide per paper. Use appendix material for detailed paper notes and secondary figures.

Every evidence slide should have a declarative title, a legible source figure, editable interpretation, a short takeaway, and a compact source line. Put full evidence locations and limitations in speaker notes.

## 5. Validation

Check three levels:

- **Scientific:** claims, numbers, units, figure interpretation, causality, and boundary conditions.
- **Traceability:** every important claim and figure maps to a source and page.
- **Artifact:** editable objects remain editable; all slides render; no overflow/overlap; PDF matches PPTX; spreadsheet opens and renders.

Repair the source artifact, rerender, and recheck. A successful package validator is necessary but not sufficient for visual or scientific correctness.

