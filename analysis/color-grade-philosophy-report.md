# Photography Color Reference Library - Color Grade Philosophy Analysis

Generated: 2026-06-02

This analysis follows the `color-grade-philosophy` skill: each reference is treated as evidence of a transferable colorist logic, not as a literal palette to copy. When a photographer has two references, both are merged into one style philosophy.

## Style Index

| Photographer | Style package | Core philosophy | Best use |
| --- | --- | --- | --- |
| Deniz Sabuncu | `deniz-sabuncu-sunlit-cobalt-portrait` | Saturated cobalt environment + warm human/linen anchor + crisp daylight graphic contrast. | Sunny outdoor portraits with sky or clean color fields. |
| 唐植炫 | `tang-zhixuan-botanical-soft-green` | Lush foliage as intimate enclosure + creamy protected skin + leaf-filtered softness. | Garden, park, and summer foliage portraits. |
| Jade Stephens | `jade-stephens-pastel-alpine-memory` | Pastel travel-film memory + muted meadow greens + pale cyan sky + blue/lavender mountain distance. | Mountain, countryside, and pastoral daylight travel photos. |
| 陈咏华 | `chen-yonghua-amber-shadow-film` | Amber subject light carved out of deep black-brown shadow + raw grainy intimacy. | Close, low-key, direct-light portraits. |
| avdidit | `avdidit-sunlit-pastoral-postcard` | High-key pastoral daylight + yellow-green fields + pale cyan sky + clean postcard calm. | Open grassland, pasture, mountain valley daylight. |
| 上田义彦 | `ueda-yoshihiko-cool-green-quiet-portrait` | Low-saturation cool green air + open shadows + soft whites + restrained psychological portrait. | Quiet natural-light portraits in foliage or soft interiors. |

## Matching Logic

Use these modes when applying a style:

- `direct_apply`: target shares scene, light, subject, and purpose.
- `semantic_adapt`: target differs but can carry the same philosophy.
- `inspired_only`: borrow only a few ideas, such as soft rolloff, lower saturation, or grain.
- `reject`: the style would damage subject truth, color accuracy, or scene identity.

## Practical Selection Notes

- For blue-sky fashion/travel portraits, start with `deniz-sabuncu-sunlit-cobalt-portrait`.
- For leafy portraits where the subject is surrounded by plants, start with `tang-zhixuan-botanical-soft-green`.
- For open mountain or countryside photos that need nostalgia, start with `jade-stephens-pastel-alpine-memory`.
- For intimate portraits with strong warm light and darkness, start with `chen-yonghua-amber-shadow-film`.
- For broad grassland daylight photos, start with `avdidit-sunlit-pastoral-postcard`.
- For restrained, quiet portraits in soft green environments, start with `ueda-yoshihiko-cool-green-quiet-portrait`.

## Anti-Literal Transfer Rules

- Do not turn grass blue just because the reference contains strong blue sky.
- Do not apply botanical green globally; protect skin and white fabric.
- Do not make every landscape pastel; only use the memory-film approach when the scene benefits from gentleness.
- Do not apply amber-shadow portrait logic to open daylight landscapes except as a very light inspiration.
- Do not over-desaturate quiet green portraits until skin loses life.

See `analysis/style-index.json` for machine-readable retrieval metadata and each `color-styles/<style-id>/style.json` for the full style package.
