---
name: color-grade-philosophy
description: Analyze photographic color grading styles, save them as reusable style packages, recommend which saved style fits a target photo, and apply a saved style through conceptual color-grade transfer rather than literal palette copying. Use when the user uploads or references photos and asks to parse a color style, name/save a color grade, choose a suitable grade for another image, adapt a reference grade to a different scene, generate prompts for GPT Image or another image editing model, or produce color-graded outputs including a model reference grade and a preservation-first full-resolution local grade when feasible.
---

# Color Grade Philosophy

## Core Principle

Transfer the colorist's decision logic, not the source image's surface colors.

Treat a reference photo as evidence of a grading philosophy: emotional goal, tonal strategy, color contrast, subject protection, texture, and scene-specific choices. When applying the style to a new photo, preserve the target scene's identity and rebuild the grade for that scene.

## Workflow

1. Classify the user request:
   - **Analyze/save**: build a reusable style package from a reference photo.
   - **Recommend/match**: decide which saved style fits a target photo.
   - **Apply**: edit a target photo using a saved style. If the user does not name a style, first recommend from the saved style library, then apply the best compatible style.
   - **Prompt only**: produce a model prompt without generating an image.

2. Resolve the saved style library before work:
   - Use `COLOR_GRADE_STYLES_ROOT` when set.
   - Otherwise use `./color-styles` in the current project.
   - Treat the resolved style library as the source of truth for saved styles unless the user requests another destination.

3. For image files on disk, inspect them visually first. Also run `scripts/extract_image_profile.py` when objective color statistics would help.

4. For a new style, run `scripts/create_style_package.py` to create the package in the saved style library, then fill the human/visual fields in `style.json`. Every parsed style package should remain in the default library unless the user requests another destination. If importing or manually moving existing packages, run `scripts/index_style_library.py` to refresh the recent index.

5. For style selection, score the target against saved candidates with the compatibility rules below. Use `scripts/score_style_fit.py --styles-root <library>` as a quick heuristic, then override it with visual judgment when needed.

6. For image editing, use the dual-track output workflow by default when the target is a local image file: first create a model-generated reference grade for creative direction, then create a deterministic full-resolution local grade from the same adaptation plan. If the target is a local file, view it first so the image is in conversation context. Save both outputs into the current project or user-requested destination, and treat the local full-resolution grade as the delivery asset unless the user explicitly chooses the model output.

## Saved Style Library

Default style library:

```text
color-styles/
  <style-id>/
    style.json
    reference.<ext>
    thumbnail.jpg
    swatches.png
    examples/
  _index/
    recent-styles.json
```

Use this library as the source of truth for saved styles across projects. `scripts/create_style_package.py` writes there by default and updates `_index/recent-styles.json` so phrases like "刚才解析的风格包", "最近的风格", or "从之前解析的风格里选" can be resolved without relying on conversation memory.

When recommending a style for a target image:

1. Load candidate `style.json` files from the saved style library.
2. If the user references recent work, prefer the newest entries in `_index/recent-styles.json`; if the index is missing, fall back to style package modification time.
3. Inspect the target image and infer scene, subject, purpose, protected colors, and risks.
4. Run the heuristic scorer for a first pass, then choose with visual judgment using the compatibility dimensions below.
5. If the user asked to color grade rather than only recommend, write the semantic adaptation plan and apply the top compatible style. If all candidates are `reject`, explain why and do not edit.

## Style Package

Package layout:

```text
color-styles/<style-id>/
  style.json
  reference.<ext>
  thumbnail.jpg
  swatches.png
  examples/
```

Read `references/style-package-schema.md` before creating or modifying a style package. A useful package must include:

- `style_philosophy`: why the grade works.
- `semantic_transfer_rules`: how the philosophy maps to skies, grass, skin, forests, interiors, products, shadows, highlights, etc.
- `compatibility`: best scenes, weak scenes, rejection cases, required visual structures, and risks.
- `model_prompt`: positive and negative edit instructions.
- `technical_profile`: palette, luminance, saturation, hue bias, grain, and sharpness notes.

Do not store only a prompt. A prompt is an execution artifact, not the style.

## Compatibility Modes

Choose one mode for each target image:

- `direct_apply`: source and target share scene, light, subject, and purpose. Apply the style with minimal rewriting.
- `semantic_adapt`: scene differs but the philosophy can transfer. Re-map the decisions to target semantics.
- `inspired_only`: only borrow a few ideas, such as lower saturation, soft rolloff, or film grain.
- `reject`: the style conflicts with the image purpose or would damage essential subject/color truth.

Scoring dimensions:

- Emotional fit: Does the target story benefit from the style mood?
- Light structure: Does the target have shadows, highlights, depth, or atmosphere that can carry the grade?
- Semantic fit: Are there target elements that can receive the source decisions?
- Color conversion cost: Would local colors be damaged by literal transfer?
- Risk: Would skin, food, product color, documents, or identity be harmed?

## Semantic Adaptation

Before editing, write a short adaptation plan:

```text
Target scene: <scene and subject>
Style philosophy: <mood, contrast, color strategy, texture>
Application mode: <direct_apply | semantic_adapt | inspired_only | reject>
Semantic mappings:
- sky -> <target-specific treatment>
- grass/foliage -> <target-specific treatment>
- forest/shadows -> <target-specific treatment>
- skin/person -> <target-specific treatment>
- highlights/white objects -> <target-specific treatment>
Risks: <what must not be damaged>
Strength: <0.0-1.0 or natural language>
```

Example: if a seaside reference uses cyan water and navy shadows, and the target is a mountain grassland, do not turn grass into ocean blue. Keep grass green but lower and cool it into sage/olive, move forest shadows toward blue-green/navy, keep rocks as cool slate grey, preserve skin warmth, and protect white clothing.

## Editing Prompt Pattern

Use this structure for GPT Image or another image editing model:

```text
Use case: style-transfer
Asset type: edited photograph / conceptual color-grade transfer

Input images:
- Image 1 is the edit target: <target description>.
- Image 2 is the style reference, if available: <style name>.

Primary request:
Apply the color philosophy of <style name> to Image 1. Do not literally copy the source scene palette. Preserve the target scene identity.

Core philosophy:
<emotional goal, contrast strategy, color strategy, subject strategy, texture strategy>

Semantic adaptation:
<scene-specific mapping rules>

Strength:
<subtle/moderate/strong; numeric if useful>

Strict preservation constraints:
Do not change composition, identity, pose, objects, camera angle, scene, weather, season, or add/remove elements. Color grade only.

Avoid:
<style-specific failure modes>
```

## Dual-Track Final Output

For final color grading of a local target image, produce two outputs when feasible:

1. **Model reference grade**: use GPT Image or another image editing model to interpret the style philosophy and show the intended creative direction. This output is useful for taste, mood, and semantic adaptation review, but it may change pixels, details, or dimensions.
2. **Full-resolution local grade**: apply a deterministic local color grade to the original target file using the same semantic adaptation plan. Preserve original dimensions, composition, identity, objects, and local color truth. This is the preservation-first delivery version.

If the user asks for `prompt only`, do not generate images. If the user explicitly asks for model-only or local-only output, follow that request. If the target is not available as a local file, cannot be opened, or local processing would require unavailable tools, explain the limitation and produce the best feasible output.

When creating the local grade:

- Use the model reference only as a visual guide, not as a pixel source.
- Prefer conservative curves, white balance, HSL, selective saturation, highlight rolloff, shadow tint, grain, and sharpening adjustments over generative edits.
- Use masks or region-specific adjustments only when they can be applied reliably; otherwise keep the local grade global and subtle.
- Do not resize, crop, upscale, inpaint, replace texture, or alter scene content.
- Preserve metadata when practical, but never at the cost of corrupting the image.

## Quality Check

After generating or editing an image:

- Verify content preservation before judging color.
- Compare target scene identity before and after.
- Confirm the full-resolution local grade matches the original pixel dimensions.
- Check protected subjects: skin, white clothing, food, product color, logos, documents.
- Check whether the grade is literal or philosophical. If it copied source colors into incompatible objects, redo with stronger semantic instructions.
- Prefer a weaker, scene-aware grade over a dramatic but scene-breaking grade.
- Deliver both the model reference grade and the local full-resolution grade when both were created, clearly labeling which is the reference and which is the preservation-first delivery asset.

## Resources

- `scripts/extract_image_profile.py`: compute palette, luminance, saturation, hue bias, region stats, and grain estimate for a photo.
- `scripts/create_style_package.py`: create a style package skeleton with `style.json`, reference image, thumbnail, and swatches.
- `scripts/index_style_library.py`: refresh `_index/recent-styles.json` after importing, moving, or bulk editing saved style packages.
- `scripts/score_style_fit.py`: quick compatibility heuristic for a style and target profile.
- `references/style-package-schema.md`: JSON schema and field guidance.
- `references/methodology.md`: color grading methodology notes and source links.
