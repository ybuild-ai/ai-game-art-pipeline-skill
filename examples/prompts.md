# Prompt Examples

These are starting points, not magic phrases. Always adapt dimensions, style, engine constraints, and reference images to your project.

## Static Icon

```text
A 2D game asset icon of a black-and-gold sword, bold ink outline, cel-shaded highlights, flat saturated colors, readable silhouette, isolated on a solid magenta #FF00FF background. No text. No UI frame. No extra objects.
```

Post-process:

```bash
python scripts/chroma_key_magenta.py sword_raw.png sword_alpha.png
```

## Character Keyframe

```text
A full-body 2D action RPG character keyframe, side-facing three-quarter view, readable combat silhouette, consistent outfit details, bold outline, cel-shaded fantasy style, standing pose, weapon visible, isolated on solid magenta #FF00FF background. No enemies. No duplicate characters. No text.
```

Use this keyframe as the identity reference for later animations.

## Combat Sprite Grid

```text
Create an 8-frame 2D game sprite animation sheet in a 4x2 grid. The character must be the exact same person as the reference image in every frame: same body proportion, same hairstyle, same outfit, same weapon size, same silhouette. Only the pose changes.

Animation: fast sword slash combo, side-facing action RPG combat.

Constraints:
- One character only.
- No enemy, opponent, duplicate, clone, or background object.
- Solid magenta #FF00FF background in every cell.
- Effects stay connected to the weapon or body.
- Do not paint full-screen lightning, smoke, or camera effects across the sheet.
- Leave enough margin so weapon trails are not cropped.
```

Post-process:

```bash
python scripts/chroma_key_magenta.py attack_grid_raw.png attack_grid_alpha.png
python scripts/sheet_contact.py attack_frames/ attack_contact.png --cols 4
```

## Video Motion Reference

```text
Short game animation reference video. A stylized sword fighter performs one readable forward slash, then returns to idle. Side-facing camera, stable framing, clear silhouette, no camera spin, no scene cut. Motion should emphasize timing, anticipation, contact, and recovery.
```

Use the generated video as motion reference, not necessarily final art.

## Cinematic Ultimate

```text
Five-second cinematic ultimate animation for a 2D action RPG. Start from the provided keyframe. Sequence: calm charge-up, sword energy gathers around the character, rapid burst of spectral blades, white flash at the end. Keep the character identity from the first frame. Full-screen cinematic layer is allowed. No UI text. No damage numbers.
```

Runtime rule: let the video own spectacle, but keep damage, target tracking, hit timing, camera shake, and SFX in code.
