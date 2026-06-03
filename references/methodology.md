# Methodology Notes

This skill synthesizes colorist practice into an agent workflow. It uses these ideas as guardrails:

- Separate color management, primary correction, and creative look. ACES describes Look Transforms as a way to impart an image-wide creative look in a viewing pipeline, while preserving the idea that a look is distinct from output display transforms. Source: https://docs.acescentral.com/tb/lmt/
- Store portable primary correction ideas separately from prose. ASC CDL represents primary correction through slope, offset, power, and saturation, which is useful as a mental model even when the final edit is done by an image model. Source: https://download.autodesk.com/us/systemdocs/help/2009/lustre/html/CBHGJDFE.html
- Think in tonal ranges. DaVinci Resolve exposes primary controls for contrast, saturation, hue, temperature, tint, shadows, highlights, and more; log wheels and HDR controls make narrower tonal-zone changes possible. Source: https://www.blackmagicdesign.com/products/davinciresolve/color
- Treat a stored style as a "look" plus adaptation policy, not as a fixed LUT. OCIO and ACES workflows distinguish transforms, looks, and display/output handling; this skill mirrors that separation at the prompt/workflow level. Source: https://opencolorio.readthedocs.io/

## Colorist Reasoning Dimensions

When analyzing a reference image, describe these dimensions:

1. Emotional goal: What should the viewer feel?
2. Tonal architecture: Are blacks lifted or deep? Are highlights clipped, creamy, or compressed?
3. Hue architecture: Which ranges are cooled, warmed, protected, or muted?
4. Subject protection: What colors must remain believable, such as skin, food, white clothing, brand colors, or documents?
5. Texture: Clean digital, film grain, halation, haze, softness, or sharpness?
6. Scene dependency: Which choices only work because of the source scene?
7. Transfer rule: How would a colorist make equivalent decisions for a different scene?

## Matching Questions

Ask these before applying a style:

- Does the target's story benefit from the reference mood?
- Does the target have the visual structure the grade needs: shadows, highlights, atmosphere, or a subject anchor?
- Which target elements should receive the source's color decisions?
- Which target elements must preserve local color?
- What is the worst likely failure: cold skin, dead food, crushed shadows, fake sky, damaged product color, or scene identity loss?

## Anti-Patterns

- Literal palette transfer: turning grass into sea blue because the reference has blue water.
- Single-prompt storage: saving a style only as a model prompt.
- Context-free recommendation: matching styles only by dominant color.
- Over-strength: applying a dramatic look when an `inspired_only` mode would preserve the photo better.
- Content drift: allowing a generative editor to change people, objects, weather, season, or composition during a color-only task.
