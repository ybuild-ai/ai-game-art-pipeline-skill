#!/usr/bin/env python3
"""Provider-neutral model adapter stub.

This file intentionally contains no API keys, SDK imports, endpoints, or vendor
logic. Copy it and implement the methods for your provider of choice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Protocol


@dataclass
class ImageRequest:
    prompt: str
    output_path: Path
    reference_images: list[Path] = field(default_factory=list)
    size: str = "1024x1024"
    transparent: bool = False


@dataclass
class VideoRequest:
    prompt: str
    output_path: Path
    first_frame: Path | None = None
    reference_images: list[Path] = field(default_factory=list)
    reference_videos: list[Path] = field(default_factory=list)
    duration_seconds: int = 5
    aspect_ratio: str = "16:9"
    resolution: str = "720p"
    generate_audio: bool = False


class GameArtProvider(Protocol):
    def generate_image(self, request: ImageRequest) -> Path:
        """Generate an image and return the written output path."""

    def edit_image(self, request: ImageRequest) -> Path:
        """Generate/edit an image using reference images."""

    def generate_video(self, request: VideoRequest) -> Path:
        """Generate a short video and return the written output path."""


class NotImplementedProvider:
    """Replace this with an adapter for OpenAI, Veo, Seedance, local models, etc."""

    def generate_image(self, request: ImageRequest) -> Path:
        raise NotImplementedError("Implement generate_image() for your provider")

    def edit_image(self, request: ImageRequest) -> Path:
        raise NotImplementedError("Implement edit_image() for your provider")

    def generate_video(self, request: VideoRequest) -> Path:
        raise NotImplementedError("Implement generate_video() for your provider")


def require_paths(paths: Iterable[Path]) -> None:
    missing = [str(p) for p in paths if not p.exists()]
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))


def example_usage() -> None:
    provider = NotImplementedProvider()
    provider.generate_image(
        ImageRequest(
            prompt=(
                "2D game asset icon of a black-and-gold sword, readable "
                "silhouette, bold outline, isolated on solid magenta #FF00FF."
            ),
            output_path=Path("out/sword_icon.png"),
        )
    )


if __name__ == "__main__":
    example_usage()

