#!/usr/bin/env python3
"""Create a numbered contact sheet from a sprite sheet.

Examples:
    python scripts/sheet_contact.py walk.png walk_contact.png --cols 2 --rows 2 --frames 4
    python scripts/sheet_contact.py ultimate.png ultimate_contact.png --cols 4 --rows 4 --frames 16
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def get_font(size: int) -> ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def make_contact(
    sheet: Image.Image,
    *,
    cols: int,
    rows: int,
    frames: int,
    label_color: tuple[int, int, int] = (255, 255, 0),
) -> Image.Image:
    sheet = sheet.convert("RGBA")
    cell_w = sheet.width // cols
    cell_h = sheet.height // rows
    out = Image.new("RGB", sheet.size, (12, 12, 14))
    font = get_font(max(14, min(cell_w, cell_h) // 8))
    draw = ImageDraw.Draw(out)

    for idx in range(frames):
        c = idx % cols
        r = idx // cols
        x0 = c * cell_w
        y0 = r * cell_h
        frame = sheet.crop((x0, y0, x0 + cell_w, y0 + cell_h))
        bg = Image.new("RGBA", frame.size, (0, 0, 0, 255))
        bg.alpha_composite(frame)
        out.paste(bg.convert("RGB"), (x0, y0))

        label = f"F{idx + 1:02d}"
        tw = int(draw.textlength(label, font=font))
        draw.rectangle((x0 + 6, y0 + 6, x0 + tw + 14, y0 + font.size + 12), fill=label_color)
        draw.text((x0 + 10, y0 + 7), label, font=font, fill=(0, 0, 0))

    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--cols", type=int, required=True)
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--frames", type=int, required=True)
    args = parser.parse_args()

    sheet = Image.open(args.input)
    out = make_contact(sheet, cols=args.cols, rows=args.rows, frames=args.frames)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

