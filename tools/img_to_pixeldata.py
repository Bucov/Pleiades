"""
One-off helper: convert an image into the pixelData format used by
static/js/frontpage-art.js, and write it to static/js/pixel-data.js.

Usage:
    pip install pillow
    python tools/img_to_pixeldata.py path/to/miku.jpg
    python tools/img_to_pixeldata.py path/to/miku.jpg --width 120 --height 90

Notes:
- width/height are the character-grid size (columns/rows), not real
  pixels -- each cell becomes one letter drawn in that cell's color.
  Keep these modest (the reference art was 120x33); a photo-realistic
  jpg will look best resized to a similar small grid.
- This script does not touch app.py or any Flask code.
"""

import argparse
import json
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="path to the source image (jpg/png/etc.)")
    parser.add_argument("--width", type=int, default=120, help="grid columns")
    parser.add_argument("--height", type=int, default=33, help="grid rows")
    parser.add_argument(
        "--out",
        default="static/js/pixel-data.js",
        help="output JS file (default: static/js/pixel-data.js)",
    )
    args = parser.parse_args()

    img = Image.open(args.image).convert("RGB")
    img = img.resize((args.width, args.height), Image.LANCZOS)

    rows = []
    for y in range(args.height):
        row = [list(img.getpixel((x, y))) for x in range(args.width)]
        rows.append(row)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("const pixelData = ")
        json.dump(rows, f)
        f.write(";\n")

    print(f"wrote {args.width}x{args.height} grid to {out_path}")


if __name__ == "__main__":
    main()
