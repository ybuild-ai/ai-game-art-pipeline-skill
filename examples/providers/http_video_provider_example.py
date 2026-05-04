#!/usr/bin/env python3
"""Generic async HTTP video provider adapter example.

This expects a user-owned HTTP service with start and status endpoints. It is
not a vendor SDK.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.provider_stub import VideoRequest  # noqa: E402


class HttpVideoProvider:
    def __init__(
        self,
        start_endpoint: str,
        status_endpoint: str,
        bearer: str | None = None,
        poll_seconds: float = 5.0,
        max_wait_seconds: float = 600.0,
    ) -> None:
        self.start_endpoint = start_endpoint
        self.status_endpoint = status_endpoint
        self.bearer = bearer
        self.poll_seconds = poll_seconds
        self.max_wait_seconds = max_wait_seconds

    def generate_video(self, request: VideoRequest) -> Path:
        payload = {
            "prompt": request.prompt,
            "duration_seconds": request.duration_seconds,
            "aspect_ratio": request.aspect_ratio,
            "resolution": request.resolution,
            "generate_audio": request.generate_audio,
            "first_frame": str(request.first_frame) if request.first_frame else None,
            "reference_images": [str(path) for path in request.reference_images],
            "reference_videos": [str(path) for path in request.reference_videos],
        }
        start = self._post_json(self.start_endpoint, payload)
        if "video_url" in start or "video_base64" in start:
            return self._write_video_response(start, request.output_path)
        job_id = start.get("job_id")
        if not job_id:
            raise ValueError("Expected job_id, video_url, or video_base64")
        result = self._poll(job_id)
        return self._write_video_response(result, request.output_path)

    def _poll(self, job_id: str) -> dict[str, Any]:
        deadline = time.time() + self.max_wait_seconds
        while time.time() < deadline:
            status_url = self.status_endpoint.format(job_id=job_id)
            data = self._get_json(status_url)
            status = data.get("status")
            if status in {"succeeded", "completed", "done"}:
                return data
            if status in {"failed", "error", "cancelled"}:
                raise RuntimeError(f"Video generation failed: {data}")
            time.sleep(self.poll_seconds)
        raise TimeoutError(f"Video generation timed out for job {job_id}")

    def _post_json(self, url: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.bearer:
            headers["Authorization"] = f"Bearer {self.bearer}"
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    def _get_json(self, url: str) -> dict[str, Any]:
        headers = {}
        if self.bearer:
            headers["Authorization"] = f"Bearer {self.bearer}"
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    def _write_video_response(self, data: dict[str, Any], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if "video_base64" in data:
            output_path.write_bytes(base64.b64decode(data["video_base64"]))
            return output_path
        if "video_url" in data:
            urllib.request.urlretrieve(data["video_url"], output_path)
            return output_path
        raise ValueError("Expected video_base64 or video_url in provider response")


def main() -> None:
    provider = HttpVideoProvider(
        start_endpoint=os.environ["GAME_ART_VIDEO_ENDPOINT"],
        status_endpoint=os.environ["GAME_ART_VIDEO_STATUS_ENDPOINT"],
        bearer=os.environ.get("GAME_ART_BEARER"),
    )
    output = provider.generate_video(
        VideoRequest(
            prompt=(
                "Five-second cinematic ultimate animation for a 2D action RPG: "
                "charge, spectral blade burst, white flash."
            ),
            output_path=Path("out/ultimate.mp4"),
            duration_seconds=5,
            aspect_ratio="16:9",
        )
    )
    print(output)


if __name__ == "__main__":
    main()
