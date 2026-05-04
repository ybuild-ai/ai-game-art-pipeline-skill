---
name: ai-game-art-pipeline
description: Provider-neutral open-source skill for planning and producing game-runtime art assets and animation: static props/icons, canonical character sheets, combat sprites, 3D/video motion references, Veo/Seedance-style video-to-frames, cinematic ultimates, backgrounds, FX, SFX, runtime packaging, and QA. Use when building actual game assets for PixiJS/Canvas/Unity/Godot/SpriteKit/etc., not one-off marketing images.
---

# AI Game Art Pipeline

Use this skill when a user wants to generate, plan, debug, or package game art that must run in an actual game runtime.

The skill is provider-neutral. It does not assume any specific API key or vendor SDK. If a model call is needed, use the user's available provider through an adapter or ask them to implement `scripts/provider_stub.py`.

## Core Rule

Pick the pipeline by runtime job, not by model hype.

| Runtime job | Pipeline |
|---|---|
| Static props, items, FX icons | Image model + style refs + removable background |
| Existing/brand character | Reuse canonical sprite sheets before regenerating |
| Combat character animation | Keyframe-first + 2D grid + post-processing + curation |
| Walk/run/body mechanics | Prefer video motion reference; use 3D skeleton only when cleanup is acceptable |
| Ambient loops | Video model -> extracted frames |
| Cinematic ultimate / boss intro | Full-screen video-to-frames + code-driven hit logic |
| Runtime feel | Deterministic code: hit pause, shake, particles, trails, SFX |

## Default Workflow

1. Identify the runtime job and target engine.
2. Check whether canonical assets already exist.
3. Pick one scenario reference below.
4. Generate the smallest useful vertical slice, not the full asset set.
5. Post-process with deterministic scripts.
6. Preview at target size and target device.
7. Iterate surgically: rerun one animation, reprocess raw output, or repack frames.

## Scenario References

Read only the relevant file:

- `references/static-assets.md` — props, icons, items, simple monsters, canonical asset reuse.
- `references/battle-sprites.md` — keyframe-first combat sprite sheets, 2D grids, anchors, contact sheets.
- `references/motion-video.md` — 3D skeleton pitfalls, video motion references, Veo/Seedance-style video-to-frames, cinematic ultimates.
- `references/backgrounds.md` — level backgrounds, master-first parallax, outpaint chains, mobile texture limits.
- `references/runtime-shipping.md` — formats, compression, CDN layout, audio/SFX, runtime QA.

## Bundled Scripts

Scripts are local utilities only. They do not call model APIs.

- `scripts/provider_stub.py` — adapter interface the user can implement for their provider.
- `scripts/chroma_key_magenta.py` — remove magenta background from generated sheets/icons.
- `scripts/sheet_contact.py` — make numbered contact sheets for curation.
- `scripts/extract_video_frames.py` — extract/resize video frames for runtime texture sequences.

## Provider Adapters

Do not write a full vendor SDK unless the user explicitly asks for one. Prefer a thin adapter around `scripts/provider_stub.py` so credentials, endpoints, retries, billing, and model choices stay in the user's project.

If the user wants examples, point them to `examples/providers/README.md` and adapt only the minimal file they need:

- fake/local provider for testing the pipeline without model calls.
- generic image HTTP provider for a user's image-generation proxy.
- generic async video HTTP provider for a user's video-generation proxy.

## Output Standard

When using this skill, produce:

- A concise pipeline choice and why.
- The exact assets to generate or reuse.
- Prompt constraints if model generation is needed.
- Post-processing commands/scripts.
- Runtime packaging notes: dimensions, format, anchor, frame rate, texture limits.
- QA checklist for the target device.

## Hard Warnings

- Do not regenerate a known character if a canonical sheet exists.
- Do not use 1xN horizontal strips for complex combat poses; use 2D grids.
- Do not let cinematic video own gameplay semantics. Damage, hitboxes, target tracking, cooldown, and SFX belong in code.
- Do not ship giant backgrounds because they look fine on desktop. Check mobile texture limits.
- Do not treat AI output as final. The production asset is the generated image plus cleanup, anchors, timing, compression, and runtime test.
