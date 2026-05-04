#!/usr/bin/env python3
"""Turn a small art plan into provider requests.

This uses the minimal local provider by default. Replace it with your own
adapter from examples/providers/ when you are ready to call a real service.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "examples" / "providers"))

from minimal_provider_example import MinimalProvider  # noqa: E402
from scripts.provider_stub import ImageRequest  # noqa: E402


ASSETS = [
    (
        "sword-icon",
        "2D game asset icon of a black-and-gold sword, readable silhouette, "
        "isolated on solid magenta #FF00FF background. No text.",
    ),
    (
        "hero-keyframe",
        "Full-body 2D action RPG hero keyframe, side-facing three-quarter view, "
        "bold outline, readable combat silhouette, solid magenta background.",
    ),
    (
        "enemy-keyframe",
        "Full-body 2D action RPG enemy keyframe, readable silhouette, solid "
        "magenta background, no duplicate characters.",
    ),
]


def main() -> None:
    provider = MinimalProvider()
    for slug, prompt in ASSETS:
        output = provider.generate_image(
            ImageRequest(prompt=prompt, output_path=Path("out") / f"{slug}.png")
        )
        print(output)


if __name__ == "__main__":
    main()
