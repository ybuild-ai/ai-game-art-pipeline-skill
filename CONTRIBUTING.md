# Contributing

Thanks for helping improve the AI Game Art Pipeline Skill.

## What Helps Most

- Provider adapters that keep API keys and endpoints outside the repository.
- Runtime preview templates for PixiJS, Canvas, Godot, Unity, SpriteKit, or web games.
- Post-processing utilities for alpha cleanup, trimming, anchors, frame packing, and QA.
- Case studies from real game asset pipelines.
- Clearer reference notes for specific runtime jobs.

## Ground Rules

- Do not commit API keys, credentials, private URLs, private file paths, or vendor-specific secrets.
- Keep scripts provider-neutral unless the provider code is explicitly optional and documented.
- Prefer deterministic cleanup tools over prompt-only advice.
- Test scripts locally before opening a PR.
- Keep `SKILL.md` concise; put deeper material in `references/`.

## Local Checks

```bash
python3 -m py_compile scripts/*.py
rg -n "API_KEY|SECRET|TOKEN|/Users/|sk-" .
```

## Pull Request Checklist

- The change is useful for a real game-runtime workflow.
- New scripts have `--help` output if they are command-line tools.
- No generated bulk assets are included unless they are small documentation examples.
- README links still work.
- The skill still reads clearly without requiring a specific model provider.
