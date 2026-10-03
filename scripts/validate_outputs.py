#!/usr/bin/env python3
"""Validate the presence and basic structure of literature-review deliverables."""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit("Missing dependency: install pypdf in the active Python environment.") from exc


def require_file(path: Path, label: str) -> None:
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"{label} missing or empty: {path}")


def pptx_counts(path: Path) -> tuple[int, int]:
    require_file(path, "PPTX")
    if not zipfile.is_zipfile(path):
        raise ValueError(f"PPTX is not a valid ZIP package: {path}")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
    slides = [n for n in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
    notes = [n for n in names if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", n)]
    return len(slides), len(notes)


def workbook_sheet_count(path: Path) -> int:
    require_file(path, "Evidence workbook")
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            next(csv.reader(handle), None)
        return 1
    if not zipfile.is_zipfile(path):
        raise ValueError(f"Workbook is not a valid XLSX package: {path}")
    with zipfile.ZipFile(path) as archive:
        return sum(1 for n in archive.namelist() if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", n))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pptx", type=Path, required=True)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--notes", type=Path, required=True)
    parser.add_argument("--figures", type=Path, required=True)
    args = parser.parse_args()
    issues: list[str] = []
    result: dict[str, object] = {"status": "pass"}
    try:
        slide_count, notes_count = pptx_counts(args.pptx)
        result.update(pptx_slides=slide_count, pptx_notes=notes_count)
        if slide_count == 0:
            issues.append("PPTX contains no slides")
        if notes_count < max(1, slide_count - 2):
            issues.append("Most PPTX slides do not have speaker-note parts")
    except Exception as exc:
        issues.append(str(exc))
    try:
        require_file(args.pdf, "PDF")
        pdf_pages = len(PdfReader(str(args.pdf), strict=False).pages)
        result["pdf_pages"] = pdf_pages
        if result.get("pptx_slides") != pdf_pages:
            issues.append("PPTX slide count and PDF page count differ")
    except Exception as exc:
        issues.append(str(exc))
    try:
        result["evidence_sheets"] = workbook_sheet_count(args.evidence)
    except Exception as exc:
        issues.append(str(exc))
    try:
        require_file(args.notes, "Per-paper notes")
        text = args.notes.read_text(encoding="utf-8")
        result["paper_note_sections"] = len(re.findall(r"(?m)^##\s+\d+\.", text))
        if result["paper_note_sections"] == 0:
            issues.append("No numbered per-paper note sections found")
    except Exception as exc:
        issues.append(str(exc))
    if not args.figures.is_dir():
        issues.append(f"Figure directory missing: {args.figures}")
    else:
        images = [p for p in args.figures.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}]
        result["figure_files"] = len(images)
        indexes = [p for p in args.figures.rglob("*") if p.name.lower() in {"figure-source-index.csv", "图源索引.csv"}]
        if images and not indexes:
            issues.append("Figure files exist but no figure source index was found")
    if issues:
        result.update(status="fail", issues=issues)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

