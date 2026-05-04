# Battle Sprite Sheets

Use this for runtime character animation: idle, walk, run, attack, hit, roll, down, die, skills, and ultimates that require transparent frames and gameplay hit timing.

## Pipeline

1. Generate one keyframe portrait to lock identity.
2. Use that keyframe as the reference for all animations.
3. Generate each animation as a 2D grid.
4. Chroma key the whole sheet.
5. Keep the main connected component.
6. Uniformly scale frames with height and width caps.
7. Anchor frames.
8. Make contact sheets and curate.
9. Export runtime sheets.

## Layouts

Do not use 1xN horizontal strips for complex combat animation.

| Frames | Layout | Typical use |
|---:|---|---|
| 4 | 2x2 | walk, hit |
| 6 | 3x2 | attacks |
| 8 | 4x2 | idle, run, roll, die |
| 10 | 5x2 | skills |
| 16 | 4x4 | ultimate sprite sheet |

## Prompt Constraints

Add these constraints to every animation prompt:

```text
The character is the EXACT SAME size, body proportion, outfit, colors,
and weapon in every frame. Only the pose/action changes.

Do NOT draw enemies, opponents, extra characters, duplicates, shadows shaped
like people, or additional figures in any frame.

Keep effects tightly contained around the weapon/body. Leave mostly empty
magenta background around the character.
```

Avoid words like "full-screen", "massive", "ground crack", "screen-filling" inside transparent sprite prompts.

## Post-Processing

### Chroma Key

Use whole-sheet chroma key before per-frame cutting. This handles anti-aliased edges more consistently.

### Connected Components

Keep the largest non-background subject. This removes hallucinated enemies, stray sparks, and isolated fragments.

Keep connected weapon trails if they touch the main body.

### Uniform Scale

Use a dual cap:

```python
ref_h = median(silhouette_heights)
max_w = max(silhouette_widths)
scale_by_h = (target_size * 0.85) / ref_h
scale_by_w = (target_size * 0.92) / max_w
uniform_scale = min(scale_by_h, scale_by_w)
```

Height-only scaling crops prone/down frames.

Width-only scaling makes upright frames too small.

### Anchors

For upright animations:

- anchor x = head x center
- anchor y = bottom / feet position

For prone animations:

- anchor x = body bbox center
- anchor y = bottom position

Do not use bbox center for walk/run. Leg motion will shift the bbox and make the character wobble.

## Curation

Generate contact sheets with `scripts/sheet_contact.py`.

Check:

- active hit frame
- silhouette readability
- weapon trail continuity
- foot sliding
- anchor wobble
- bad or duplicated frames

Drop/reorder individual frames instead of rerolling entire animations.

