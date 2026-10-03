#!/usr/bin/env python3
"""Create numbered contact sheets from rendered slide or PDF-page PNGs."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as exc:
    raise SystemExit("Missing dependency: install Pillow in the active Python environment.") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--pattern", default="*.png")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--rows", type=int, default=3)
    args = parser.parse_args()
    if args.columns < 1 or args.rows < 1:
        parser.error("columns and rows must be positive")
    files = sorted(args.input_dir.glob(args.pattern))
    if not files:
        parser.error("no matching images found")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    cell_w, cell_h, label_h = 1280, 720, 28
    page_size = args.columns * args.rows
    for offset in range(0, len(files), page_size):
        group = files[offset : offset + page_size]
        canvas = Image.new("RGB", (cell_w * args.columns, (cell_h + label_h) * args.rows), "#dfe4e7")
        draw = ImageDraw.Draw(canvas)
        for index, file in enumerate(group):
            image = Image.open(file).convert("RGB")
            image.thumbnail((cell_w - 20, cell_h - 20))
            x = (index % args.columns) * cell_w + 10
            y = (index // args.columns) * (cell_h + label_h) + 10
            canvas.paste(image, (x, y))
            draw.text((x, y + cell_h - 6), file.stem, fill="#17324d", anchor="ls")
        number = offset // page_size + 1
        canvas.save(args.output_dir / f"contact-{number:02d}.png")
    print(f"images={len(files)} sheets={math.ceil(len(files) / page_size)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
