# Provider Adapter Examples

These examples show how to connect the skill's provider-neutral request objects to a user's own image or video generation service.

They are not official SDKs. They intentionally avoid vendor SDK imports, real endpoints, credentials, retry policy, billing behavior, and model-specific parameters.

## Design

Keep the split clean:

- `scripts/provider_stub.py` defines the interface.
- provider adapters live in the user's project.
- deterministic cleanup stays in `scripts/`.
- generated raw assets stay outside git unless they are small docs examples.

## Environment

The generic HTTP examples use placeholder environment variables:

```bash
export GAME_ART_IMAGE_ENDPOINT="https://your-service.example/image"
export GAME_ART_VIDEO_ENDPOINT="https://your-service.example/video"
export GAME_ART_VIDEO_STATUS_ENDPOINT="https://your-service.example/video/{job_id}"
export GAME_ART_BEARER="optional bearer credential"
```

Do not commit real credentials.

## Examples

### Minimal local provider

Writes a placeholder PNG so you can test downstream file flow without any model call:

```bash
python examples/providers/minimal_provider_example.py
```

### Generic image HTTP provider

Sends an `ImageRequest` as JSON to `GAME_ART_IMAGE_ENDPOINT`.

Expected service response:

```json
{"image_url": "https://example.com/generated.png"}
```

or:

```json
{"image_base64": "iVBORw0KGgo..."}
```

Run:

```bash
python examples/providers/http_image_provider_example.py
```

### Generic async video HTTP provider

Sends a `VideoRequest` as JSON to `GAME_ART_VIDEO_ENDPOINT`.

Expected start response:

```json
{"job_id": "abc123"}
```

Expected status response:

```json
{"status": "succeeded", "video_url": "https://example.com/clip.mp4"}
```

or:

```json
{"status": "succeeded", "video_base64": "AAAA..."}
```

Run:

```bash
python examples/providers/http_video_provider_example.py
```

## Real Provider Checklist

- Read credentials from environment variables or a secret manager.
- Keep raw generation outputs in `out/`, `raw/`, or another ignored directory.
- Save the original prompt and provider metadata next to generated assets.
- Never let provider output directly define gameplay logic.
- Run post-processing and runtime preview after generation.
