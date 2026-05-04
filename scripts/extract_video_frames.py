#!/usr/bin/env python3
"""Extract and optionally resize frames from a video.

Requires ffmpeg on PATH.

Examples:
    python scripts/extract_video_frames.py clip.mp4 frames --fps 14 --start 0.6 --duration 3.6 --width 1280 --format jpg
    python scripts/extract_video_frames.py water.mp4 water_frames --fps 12 --format png
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
        raise SystemExit(proc.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--fps", type=float, default=12)
    parser.add_argument("--start", type=float, default=0.0)
    parser.add_argument("--duration", type=float, default=0.0, help="0 means until end")
    parser.add_argument("--width", type=int, default=0, help="resize to width, preserving aspect")
    parser.add_argument("--format", choices=("png", "jpg"), default="png")
    parser.add_argument("--quality", type=int, default=86)
    parser.add_argument("--keep-temp", action="store_true")
    args = parser.parse_args()

    if not args.video.exists():
        raise SystemExit(f"missing video: {args.video}")
    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg not found on PATH")

    tmp = args.output_dir / "_tmp_png"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True, exist_ok=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["ffmpeg", "-y"]
    if args.start > 0:
        cmd += ["-ss", str(args.start)]
    cmd += ["-i", str(args.video)]
    if args.duration > 0:
        cmd += ["-t", str(args.duration)]
    cmd += ["-vf", f"fps={args.fps}", str(tmp / "frame_%04d.png")]
    run(cmd)

    frames = sorted(tmp.glob("frame_*.png"))
    if not frames:
        raise SystemExit("no frames extracted")

    for i, src in enumerate(frames):
        img = Image.open(src).convert("RGB" if args.format == "jpg" else "RGBA")
        if args.width > 0 and img.width != args.width:
            h = round(img.height * (args.width / img.width))
            img = img.resize((args.width, h), Image.Resampling.LANCZOS)
        dest = args.output_dir / f"frame_{i:04d}.{args.format}"
        if args.format == "jpg":
            img.save(dest, "JPEG", quality=args.quality, optimize=True, progressive=True)
        else:
            img.save(dest)

    if not args.keep_temp:
        shutil.rmtree(tmp)
    print(f"wrote {len(frames)} frames to {args.output_dir}")


if __name__ == "__main__":
    main()

