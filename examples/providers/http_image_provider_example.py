#!/usr/bin/env python3
"""Generic HTTP image provider adapter example.

This expects a user-owned HTTP service. It is not a vendor SDK.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.provider_stub import ImageRequest  # noqa: E402


class HttpImageProvider:
    def __init__(self, endpoint: str, bearer: str | None = None) -> None:
        self.endpoint = endpoint
        self.bearer = bearer

    def generate_image(self, request: ImageRequest) -> Path:
        payload = {
            "prompt": request.prompt,
            "size": request.size,
            "transparent": request.transparent,
            "reference_images": [str(path) for path in request.reference_images],
        }
        data = self._post_json(self.endpoint, payload)
        return self._write_image_response(data, request.output_path)

    def edit_image(self, request: ImageRequest) -> Path:
        return self.generate_image(request)

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.bearer:
            headers["Authorization"] = f"Bearer {self.bearer}"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    def _write_image_response(self, data: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if "image_base64" in data:
            output_path.write_bytes(base64.b64decode(data["image_base64"]))
            return output_path
        if "image_url" in data:
            urllib.request.urlretrieve(data["image_url"], output_path)
            return output_path
        raise ValueError("Expected image_base64 or image_url in provider response")


def main() -> None:
    endpoint = os.environ["GAME_ART_IMAGE_ENDPOINT"]
    provider = HttpImageProvider(endpoint, os.environ.get("GAME_ART_BEARER"))
    output = provider.generate_image(
        ImageRequest(
            prompt=(
                "2D game asset icon of a black-and-gold sword, readable "
                "silhouette, isolated on solid magenta #FF00FF background."
            ),
            output_path=Path("out/sword-icon.png"),
        )
    )
    print(output)


if __name__ == "__main__":
    main()
