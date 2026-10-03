#!/usr/bin/env python3
"""Recursively inventory PDFs, detect exact duplicates, and measure text coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit("Missing dependency: install pypdf in the active Python environment.") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_meta(value: Any) -> str:
    return "" if value is None else str(value).strip()


def inspect_pdf(path: Path, root: Path) -> dict[str, Any]:
    record: dict[str, Any] = {
        "file": path.name,
        "relative_path": str(path.relative_to(root)),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "status": "ok",
        "error": "",
    }
    try:
        reader = PdfReader(str(path), strict=False)
        if reader.is_encrypted:
            record.update(status="encrypted", pdf_pages=len(reader.pages), text_pages=0)
            return record
        meta = reader.metadata or {}
        text_pages = 0
        for page in reader.pages:
            try:
                if (page.extract_text() or "").strip():
                    text_pages += 1
            except Exception:
                pass
        page_count = len(reader.pages)
        record.update(
            pdf_pages=page_count,
            text_pages=text_pages,
            text_coverage=(text_pages / page_count if page_count else 0.0),
            metadata={
                "title": clean_meta(meta.get("/Title")),
                "author": clean_meta(meta.get("/Author")),
                "subject": clean_meta(meta.get("/Subject")),
                "creator": clean_meta(meta.get("/Creator")),
            },
        )
    except Exception as exc:
        record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    return record


def build_summary(records: list[dict[str, Any]]) -> str:
    groups: dict[str, list[str]] = {}
    for record in records:
        groups.setdefault(record["sha256"], []).append(record["relative_path"])
    duplicate_groups = [paths for paths in groups.values() if len(paths) > 1]
    partial = [r for r in records if r.get("status") == "ok" and r.get("text_coverage", 0) < 1]
    failed = [r for r in records if r.get("status") != "ok"]
    lines = [
        "# PDF inventory summary", "",
        f"- PDFs: {len(records)}",
        f"- Exact duplicate groups: {len(duplicate_groups)}",
        f"- Partial text coverage: {len(partial)}",
        f"- Encrypted/failed: {len(failed)}", "",
        "## Exact duplicate groups", "",
    ]
    if duplicate_groups:
        for index, paths in enumerate(duplicate_groups, 1):
            lines.append(f"{index}. " + " | ".join(paths))
    else:
        lines.append("None.")
    if failed:
        lines.extend(["", "## Files requiring attention", ""])
        for record in failed:
            lines.append(f"- `{record['relative_path']}`: {record['status']} {record.get('error', '')}".rstrip())
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="JSON manifest path")
    parser.add_argument("--summary", type=Path, help="Optional Markdown summary path")
    args = parser.parse_args()
    root = args.input_dir.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"input_dir is not a directory: {root}")
    pdfs = sorted((p for p in root.rglob("*.pdf") if p.is_file()), key=lambda p: str(p).lower())
    records = [inspect_pdf(path, root) for path in pdfs]
    groups: dict[str, list[str]] = {}
    for record in records:
        groups.setdefault(record["sha256"], []).append(record["relative_path"])
    payload = {
        "input_dir": str(root),
        "pdf_count": len(records),
        "exact_duplicate_groups": [paths for paths in groups.values() if len(paths) > 1],
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.summary:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(build_summary(records), encoding="utf-8")
    print(json.dumps({"pdf_count": len(records), "duplicate_groups": len(payload["exact_duplicate_groups"]), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

