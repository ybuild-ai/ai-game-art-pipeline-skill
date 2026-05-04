#!/usr/bin/env python3
"""Remove magenta backgrounds from generated game assets.

Example:
    python scripts/chroma_key_magenta.py input.png output.png
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def chroma_key_magenta(
    image: Image.Image,
    *,
    hard_r: int = 200,
    hard_g: int = 90,
    hard_b: int = 200,
    soft: bool = True,
    erode: bool = True,
    feather: float = 0.5,
) -> Image.Image:
    arr = np.array(image.convert("RGBA"))
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    hard_mask = (r >= hard_r) & (g <= hard_g) & (b >= hard_b)

    if soft:
        soft_mask = (
            (r > 150)
            & (g < 135)
            & (b > 150)
            & (np.abs(r - b) < 65)
            & (g < r * 0.72)
            & (r <= 235)
            & (b <= 235)
        )
        mask = hard_mask | soft_mask
    else:
        mask = hard_mask

    alpha = Image.fromarray((~mask).astype(np.uint8) * 255, "L")
    if erode:
        alpha = alpha.filter(ImageFilter.MinFilter(3))
    if feather > 0:
        alpha = alpha.filter(ImageFilter.GaussianBlur(feather))

    arr[:, :, 3] = np.array(alpha)
    return Image.fromarray(arr, "RGBA")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--no-soft", action="store_true")
    parser.add_argument("--no-erode", action="store_true")
    parser.add_argument("--feather", type=float, default=0.5)
    args = parser.parse_args()

    img = Image.open(args.input)
    out = chroma_key_magenta(
        img,
        soft=not args.no_soft,
        erode=not args.no_erode,
        feather=args.feather,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.save(args.output)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()

