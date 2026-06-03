#!/usr/bin/env python3
"""Extract objective color/style statistics from an image."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
import statistics
from collections import Counter
from pathlib import Path

try:
    from PIL import Image, ImageFilter
except Exception as exc:  # pragma: no cover - environment helper
    raise SystemExit(
        "Pillow is required. Install it with `pip install pillow` or use a Python runtime that already includes Pillow."
    ) from exc


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = round((len(ordered) - 1) * p / 100)
    return ordered[max(0, min(len(ordered) - 1, index))]


def rgb_to_luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (channel / 255 for channel in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pixels_from(image: Image.Image) -> list:
    getter = getattr(image, "get_flattened_data", None)
    if getter:
        return list(getter())
    return list(image.getdata())


def color_meta(rgb: tuple[int, int, int], weight: float | None = None) -> dict:
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    item = {
        "hex": f"#{r:02x}{g:02x}{b:02x}",
        "rgb": [r, g, b],
        "hue": round(h * 360, 1),
        "saturation": round(s, 3),
        "value": round(v, 3),
        "luminance": round(rgb_to_luminance(rgb), 3),
    }
    if weight is not None:
        item["weight"] = round(weight, 4)
    return item


def build_palette(image: Image.Image, colors: int) -> list[dict]:
    quantized = image.quantize(colors=colors, method=2).convert("RGB")
    counts = Counter(pixels_from(quantized))
    total = sum(counts.values()) or 1
    return [color_meta(rgb, count / total) for rgb, count in counts.most_common(colors)]


def region_stats(image: Image.Image, box: tuple[int, int, int, int]) -> dict:
    crop = image.crop(box).resize((160, 160)).convert("RGB")
    pixels = pixels_from(crop)
    luminance = [rgb_to_luminance(pixel) for pixel in pixels]
    saturation = []
    avg = [0, 0, 0]
    for r, g, b in pixels:
        _, s, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        saturation.append(s)
        avg[0] += r
        avg[1] += g
        avg[2] += b
    count = len(pixels) or 1
    avg_rgb = tuple(round(channel / count) for channel in avg)
    palette = build_palette(crop, 5)
    return {
        "avg_hex": f"#{avg_rgb[0]:02x}{avg_rgb[1]:02x}{avg_rgb[2]:02x}",
        "luminance_mean": round(statistics.mean(luminance), 3),
        "luminance_p10": round(percentile(luminance, 10), 3),
        "luminance_p90": round(percentile(luminance, 90), 3),
        "saturation_mean": round(statistics.mean(saturation), 3),
        "dominants": palette,
    }


def hue_bias(pixels: list[tuple[int, int, int]]) -> dict:
    buckets = {
        "red_orange": 0.0,
        "yellow": 0.0,
        "green": 0.0,
        "cyan_blue": 0.0,
        "magenta": 0.0,
    }
    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        hue = h * 360
        if s < 0.08 or v < 0.08:
            continue
        weight = s * v
        if hue < 35 or hue >= 340:
            buckets["red_orange"] += weight
        elif hue < 70:
            buckets["yellow"] += weight
        elif hue < 165:
            buckets["green"] += weight
        elif hue < 255:
            buckets["cyan_blue"] += weight
        else:
            buckets["magenta"] += weight
    total = sum(buckets.values()) or 1
    return {key: round(value / total, 3) for key, value in buckets.items()}


def estimate_grain(image: Image.Image) -> dict:
    width, height = image.size
    crop = image.crop((0, 0, width, max(1, int(height * 0.36))))
    resized_height = max(1, round(512 * crop.size[1] / max(1, crop.size[0])))
    gray = crop.resize((512, resized_height)).convert("L")
    blur = gray.filter(ImageFilter.GaussianBlur(radius=2))
    residuals = [abs(a - b) / 255 for a, b in zip(pixels_from(gray), pixels_from(blur))]
    return {
        "high_frequency_mean": round(statistics.mean(residuals), 4),
        "high_frequency_p95": round(percentile(residuals, 95), 4),
    }


def build_profile(image_path: Path, palette_colors: int = 12) -> dict:
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    scale = min(1.0, 1000 / max(width, height))
    small = image.resize((max(1, int(width * scale)), max(1, int(height * scale))))
    pixels = pixels_from(small)

    luminance = [rgb_to_luminance(pixel) for pixel in pixels]
    saturation = []
    value = []
    for r, g, b in pixels:
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        saturation.append(s)
        value.append(v)

    regions = {
        "top": (0, 0, width, int(height * 0.33)),
        "middle": (0, int(height * 0.33), width, int(height * 0.66)),
        "bottom": (0, int(height * 0.66), width, height),
        "center": (int(width * 0.25), int(height * 0.2), int(width * 0.75), int(height * 0.85)),
    }

    return {
        "image": {
            "path": str(image_path),
            "sha256": "sha256:" + hashlib.sha256(image_path.read_bytes()).hexdigest(),
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 3),
        },
        "luminance": {
            "mean": round(statistics.mean(luminance), 3),
            "p01": round(percentile(luminance, 1), 3),
            "p10": round(percentile(luminance, 10), 3),
            "p50": round(percentile(luminance, 50), 3),
            "p90": round(percentile(luminance, 90), 3),
            "p99": round(percentile(luminance, 99), 3),
        },
        "saturation": {
            "mean": round(statistics.mean(saturation), 3),
            "median": round(percentile(saturation, 50), 3),
            "p90": round(percentile(saturation, 90), 3),
        },
        "hue_bias": hue_bias(pixels),
        "palette": build_palette(small, palette_colors),
        "regions": {name: region_stats(image, box) for name, box in regions.items()},
        "grain_estimate": estimate_grain(image),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract color/style statistics from an image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--out", type=Path, help="Optional JSON output path.")
    parser.add_argument("--palette-colors", type=int, default=12)
    args = parser.parse_args()

    profile = build_profile(args.image, args.palette_colors)
    payload = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
