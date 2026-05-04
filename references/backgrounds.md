# Level Backgrounds and Environment Art

Use this for stages, scrolling backgrounds, parallax layers, and environment tiles.

## Master-First Workflow

Independent parallax layers often look like a collage. Generate one master scene first.

1. Generate a full master scene with the desired mood.
2. Use the master as the first reference for layer generation.
3. Generate sky, midground, foreground, and ground only after the master exists.
4. If layers still feel mismatched, ship the master as a single background and fake parallax with camera speed.

Style references beat adjectives. One strong screenshot/reference is often better than paragraphs of "painterly atmospheric fantasy".

## Outpaint Chain

For long side-scrolling stages:

1. Generate a master tile.
2. Keep the right edge as locked context.
3. Extend to the right with an outpaint mask.
4. Repeat.
5. Stitch the segments.
6. Downscale/compress for runtime.

Do not generate every segment independently. The seams will drift.

## Mobile Texture Limit

For WebGL/mobile, keep large backgrounds at or below 4096px wide unless you have verified the target device.

Recommended:

- opaque background: JPG quality 85-90
- transparent layer: PNG or WebP
- avoid huge PNGs when no alpha is needed

Runtime export matters more than source resolution.

## Environment Tiles

For tile/object generation, use templates:

- diamond templates for isometric tiles
- wireframe footprint templates for buildings
- one-tile templates for small ground cover

Prompt the model to preserve projection, footprint, and background constraints.

Then remove template lines and apply alpha masks deterministically.

