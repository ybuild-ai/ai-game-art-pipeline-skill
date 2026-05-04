# Static Assets, Icons, Props, and Canonical Characters

Use this when generating non-animated assets or deciding whether to reuse existing art.

## Best Uses

- Item icons
- FX icons
- Props
- Pickups
- Simple static monsters
- UI-adjacent game images
- Style exploration

## Prompt Pattern

Use a production-style prompt:

```text
[Asset description].
2D game asset, readable silhouette, bold outline, flat/cel-shaded color,
high contrast, isolated on a solid magenta #FF00FF background.
Designed to remain readable at [target pixel size].
```

Avoid vague quality words alone: "cool", "epic", "magical", "high quality".

Always specify:

- asset type
- runtime size or readability target
- art style
- background removal plan
- negative style constraints if needed

## Background Removal

Prefer magenta `#FF00FF` for generated transparent assets.

Why magenta:

- Green destroys foliage.
- White destroys highlights.
- Black destroys dark outlines.

Post-process with `scripts/chroma_key_magenta.py`.

## Canonical Asset Rule

If the character, brand mascot, card, relic, faction symbol, or pet already exists, reuse the canonical file first.

Only generate new art when:

- no canonical asset exists
- the requested object is new
- the user explicitly wants a redesign

Known-character consistency is usually more important than one-off novelty.

## Runtime Check

Before accepting an asset, preview it:

- at actual in-game scale
- on the intended background
- next to similar assets
- with UI overlays if applicable

Reject or regenerate if the silhouette disappears, outlines blur, colors clash, or tiny details become noise.

