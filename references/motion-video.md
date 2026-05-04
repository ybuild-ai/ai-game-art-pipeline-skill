# Motion References, 3D Skeletons, and Video-to-Frames

Use this when animation quality depends on motion continuity, spectacle, or camera/lighting movement.

## 3D Skeleton Scaffold

Pipeline:

1. Get or create a 3D animation.
2. Render it with a clean orthographic camera.
3. Use the rendered frames as pose references.
4. Generate stylized frames from the pose references.
5. Post-process as sprite sheets.

Good for:

- grounded body mechanics
- attacks with clear pose progression
- humanoid proportions

Pitfalls:

- walk cycles may lose left/right leg readability after stylization
- coats, capes, shadows, and weapons can merge with legs
- pose transfer can create anatomically correct but visually muddy frames
- cleanup cost can exceed the benefit

If using 3D, make the reference intentionally legible:

- strong silhouette separation
- in-place animation
- plain background
- side lighting
- optional front/back leg color coding
- no capes during early tests

## Video Model as Motion Reference

Video models can be used as motion directors, not just final renderers.

Workflow:

1. Generate a short motion clip.
2. Extract frames.
3. Select strong silhouettes and timing beats.
4. Use selected frames as references for clean sprite generation, or use directly as a texture sequence.

This is often better than 3D skeletons when the move depends on:

- flow
- energy
- camera motion
- cloth / hair / particles
- transformation
- spell buildup
- readable spectacle

## Video-to-Frames Runtime Asset

Use for:

- water/lava/fog loops
- magical effects
- boss intros
- cinematic ultimates
- full-screen cut-ins

Pipeline:

1. Generate video from prompt or first frame.
2. Extract frames with `scripts/extract_video_frames.py`.
3. Resize to exact runtime dimensions.
4. Save JPG for opaque full-screen frames; PNG/WebP only when alpha is required.
5. Load as AnimatedSprite / texture sequence / frame loop.

## Cinematic Ultimate Rule

For big ultimates, let the video own the screen and let code own gameplay.

Video owns:

- light
- camera
- energy
- mood
- full-screen spectacle

Code owns:

- damage
- hitboxes
- target tracking
- cooldowns
- sword/projectile logic
- SFX
- hit pause
- screen shake

Do not try to chroma-key a full-screen light explosion unless you really need transparency.

