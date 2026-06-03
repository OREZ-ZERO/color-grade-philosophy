# Style Package Schema

Use this schema for `color-styles/<style-id>/style.json`. Keep stable fields even when some values are empty; this makes stored styles searchable and reusable across image models, LUT tools, and future workflows.

## Required Top-Level Fields

```json
{
  "id": "blue-hour-seaside-film",
  "name": "Blue Hour Seaside Film",
  "version": "1.0.0",
  "created_at": "2026-06-01",
  "source_image": "reference.jpg",
  "source_image_sha256": "sha256:...",
  "description": "One concise paragraph.",
  "tags": ["film", "blue-hour", "portrait"],
  "mood": ["quiet", "nostalgic"],
  "scene_fit": ["seaside portrait", "travel portrait"],
  "avoid_scenes": ["product color accuracy", "document scan"],
  "technical_profile": {},
  "style_philosophy": {},
  "semantic_transfer_rules": {},
  "compatibility": {},
  "palette": [],
  "model_prompt": {},
  "retrieval": {}
}
```

## `technical_profile`

Store objective observations and measurable image properties:

```json
{
  "image_size": { "width": 1913, "height": 2560, "aspect_ratio": 0.747 },
  "luminance": { "mean": 0.564, "p01": 0.098, "p10": 0.129, "p50": 0.697, "p90": 0.895, "p99": 0.927 },
  "saturation": { "mean": 0.251, "median": 0.266, "p90": 0.441 },
  "dominant_hue_bias": "cyan-blue dominant with small warm skin accent",
  "grain": "visible fine grain in sky and shadows",
  "sharpness": "soft focus / slight motion blur"
}
```

## `style_philosophy`

Store the reasoned colorist logic:

```json
{
  "emotional_goal": "quiet, nostalgic, slightly distant",
  "contrast_strategy": "deep emotional shadows with soft highlight rolloff",
  "color_strategy": "cool environment with small protected warm human anchor",
  "subject_strategy": "preserve the person as the emotional/brightness center",
  "texture_strategy": "subtle analog grain and mild softness instead of digital sharpness",
  "do_not_literalize": "Do not copy source scene colors into incompatible target objects."
}
```

## `semantic_transfer_rules`

Rules should describe how the philosophy maps to scene elements. Include rules for source-relevant elements and common target elements:

```json
{
  "sky": "pale cyan-blue, restrained saturation",
  "water": "cool cyan-blue with soft contrast",
  "grass": "muted sage or cool olive; preserve green identity",
  "forest": "deep blue-green or pine-black shadows with visible texture",
  "mountain": "cool slate grey, natural rock texture",
  "skin": "preserve slight warm peach accent",
  "white_clothing": "pearl white, luminous but not clipped",
  "shadow": "deep navy or blue-green, not neutral black",
  "highlight": "soft rolloff, pearl or cream-white"
}
```

## `compatibility`

Use this to choose `direct_apply`, `semantic_adapt`, `inspired_only`, or `reject`.

```json
{
  "best_for": ["seaside portrait", "blue hour portrait"],
  "also_works_for": ["mountain travel portrait", "street portrait", "overcast landscape"],
  "weak_for": ["bright food", "clean commercial portrait", "wedding"],
  "reject_for": ["document", "ID photo", "medical image", "color-critical product"],
  "requires": {
    "has_shadow_structure": true,
    "has_coolable_environment": true,
    "benefits_from_human_anchor": true,
    "needs_highlight_anchor": "white clothing, sky, clouds, window light"
  },
  "risks": [
    "may make grass too grey if applied literally",
    "may make skin too cold",
    "may crush forest detail",
    "may over-blue non-seaside scenes"
  ]
}
```

## `model_prompt`

Keep model execution prompts separate from the philosophy:

```json
{
  "positive": "Apply a nostalgic cool film grade...",
  "negative": "Do not change composition, identity, objects...",
  "strength_default": 0.55,
  "strength_range": [0.35, 0.75],
  "preserve_content_priority": "very high"
}
```

## `retrieval`

Use this for search and recommendations:

```json
{
  "keywords": ["cool film", "deep shadows", "warm skin", "soft highlights"],
  "embedding_text": "Quiet nostalgic cool environment grade with deep navy shadows, soft rolloff, protected warm skin, and subtle film grain."
}
```

## Quality Rules

- Store both objective metrics and subjective philosophy.
- Name risks explicitly. They are needed for scene-aware adaptation.
- Never let `model_prompt.positive` be the only source of truth.
- Preserve target local color identity unless the user asks for heavy stylization.
- Add examples over time: `examples/before.*`, `examples/after.*`, and notes about what worked.
