# AI Game Art Pipeline Skill

An open-source Codex skill for planning, generating, cleaning, and shipping game-runtime art assets.

This is not a prompt pack or a model leaderboard. It is a production workflow for turning AI-generated visuals into assets that can survive an actual runtime: sprites, icons, backgrounds, video-to-frames animation, cinematic ultimates, compression, anchors, and QA.

## What It Covers

- Static game assets: icons, props, items, FX, simple monsters
- Combat sprites: keyframe-first identity lock, 2D grids, chroma key, connected components, anchors
- Motion references: 3D skeleton tradeoffs, video generation as motion reference, frame extraction
- Backgrounds: master-first style control, parallax decisions, mobile texture limits
- Cinematic ultimates: full-screen video layers with deterministic gameplay logic
- Shipping: formats, compression, CDN layout, audio, runtime preview checks

## Install

Clone this repository into your Codex skills directory:

```bash
git clone https://github.com/ybuild-ai/ai-game-art-pipeline-skill.git ~/.codex/skills/ai-game-art-pipeline
```

Then ask Codex to use the skill for game art or animation production tasks.

## Repository Layout

```text
SKILL.md
references/
  static-assets.md
  battle-sprites.md
  motion-video.md
  backgrounds.md
  runtime-shipping.md
scripts/
  provider_stub.py
  chroma_key_magenta.py
  sheet_contact.py
  extract_video_frames.py
```

## Scripts

The scripts are intentionally provider-neutral. They do not contain API keys, endpoints, private paths, or vendor SDK code.

- `provider_stub.py`: interface for users to implement with their own image/video provider.
- `chroma_key_magenta.py`: remove solid magenta backgrounds from generated assets.
- `sheet_contact.py`: build numbered contact sheets for sprite curation.
- `extract_video_frames.py`: extract and resize video frames for runtime texture sequences.

Example:

```bash
python scripts/chroma_key_magenta.py input.png output.png
python scripts/sheet_contact.py frames/ contact.png --cols 6
python scripts/extract_video_frames.py ultimate.mp4 frames/ --fps 14 --start 0.6 --duration 3.6 --width 1280
```

## Design Philosophy

Pick the pipeline by runtime job, not by model hype.

Use generative models for visual richness, pose ideas, atmosphere, texture, light, and spectacle. Use deterministic code for transparency, anchors, hit timing, compression, frame selection, hitboxes, damage, SFX, and runtime behavior.

The useful output is not a pretty image. It is a playable asset.

## License

MIT.
