# Runtime Shipping, QA, and Audio

Use this after generation. This is where assets become game-ready.

## Asset Contract

For each asset, record:

- path
- dimensions
- frame count
- layout
- frame rate
- loop or one-shot
- anchor point
- collision/hit timing if applicable
- file format
- compression settings
- source prompt / reference list

## Format Rules

Use JPG for opaque backgrounds.

Use PNG/WebP for alpha sprites.

Use sprite sheets for small/medium runtime animation.

Use frame sequences for full-screen video-derived animation.

Avoid per-frame GPU texture creation from canvas. Preload textures and reuse them.

## QA Checklist

Check assets in runtime, not just in the file browser.

- target device
- target resolution
- target background
- actual scale
- animation speed
- anchor stability
- active hit frame
- SFX sync
- texture upload stutter
- memory pressure
- CDN/cache behavior

## Audio

Visuals need sound and hit feel.

Minimum action-game SFX set:

- light slash
- heavy slash
- light hit
- heavy hit
- dash / roll
- shockwave
- pickup
- boss roar
- victory
- defeat

Use an audio pool. Do not create audio objects on every hit.

Pair visual impact with:

- hit pause
- screen shake
- SFX
- particle burst
- floating damage number

The animation can be beautiful and still feel weak without these.

