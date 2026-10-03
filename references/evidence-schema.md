# Evidence ledger schema

Use one row per paper for the primary ledger. Add a separate figure ledger when figures are extracted.

## Paper ledger fields

| Field | Meaning |
|---|---|
| `file` | Source filename |
| `relative_path` | Path relative to the supplied corpus root |
| `sha256` | Exact-file duplicate key |
| `title` | Article title from the paper |
| `authors` | Authors as printed |
| `year` | Publication year |
| `journal` | Journal or proceedings |
| `doi` | DOI only when present or reliably resolved |
| `pdf_pages` | PDF page count |
| `research_question` | Question addressed by the paper |
| `object_and_method` | Material, site, experiment/model and analytical method |
| `conditions` | Temperature, time, pressure, pH, composition and other boundaries |
| `key_results` | Quantitative and qualitative findings with units |
| `mechanism_interpretation` | Authors' explanation, explicitly labeled as interpretation |
| `innovation` | What the paper adds |
| `limitations` | Sample, method, scale and extrapolation limits |
| `topic_relevance` | How it informs the requested topic |
| `evidence_location` | PDF page and printed page where available |
| `reading_priority` | A = central/deep read, B = supporting, C = peripheral |
| `read_status` | OK, partial, scanned, encrypted or failed |

Do not insert guessed bibliographic values. Use `not provided` or an empty field and explain the retrieval limit.

## Claim ledger extension

For complex reviews, add one row per claim with:

- normalized claim;
- epistemic status: observation, author interpretation, or synthesis;
- source paper(s);
- evidence location(s);
- conditions and units;
- supporting/contradicting evidence;
- confidence rationale;
- unresolved question.

## Figure ledger fields

Record filename, source paper, author/year, title, original figure and panel, PDF page, printed page, crop method, what the figure shows, which claim it supports, and interpretation limits.

