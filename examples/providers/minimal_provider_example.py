#!/usr/bin/env python3
"""Minimal local provider example.

This does not call any model API. It writes a tiny placeholder PNG so you can
test downstream file flow before wiring a real provider.
"""

from __future__ import annotations

import base64
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.provider_stub import ImageRequest, VideoRequest  # noqa: E402


PLACEHOLDER_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAF"
    "gwJ/lOp9WQAAAABJRU5ErkJggg=="
)


class MinimalProvider:
    def generate_image(self, request: ImageRequest) -> Path:
        request.output_path.parent.mkdir(parents=True, exist_ok=True)
        request.output_path.write_bytes(base64.b64decode(PLACEHOLDER_PNG))
        return request.output_path

    def edit_image(self, request: ImageRequest) -> Path:
        return self.generate_image(request)

    def generate_video(self, request: VideoRequest) -> Path:
        raise NotImplementedError("Wire your video provider here")


def main() -> None:
    provider = MinimalProvider()
    output = provider.generate_image(
        ImageRequest(
            prompt="Placeholder 2D game asset icon on solid magenta background.",
            output_path=Path("out/provider-test.png"),
        )
    )
    print(output)


if __name__ == "__main__":
    main()
