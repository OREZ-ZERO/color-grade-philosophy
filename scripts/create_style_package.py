#!/usr/bin/env python3
"""Create a reusable color-grade style package from a reference image."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except Exception as exc:  # pragma: no cover - environment helper
    raise SystemExit(
        "Pillow is required. Install it with `pip install pillow` or use a Python runtime that already includes Pillow."
    ) from exc

from extract_image_profile import build_profile


DEFAULT_STYLES_ROOT = Path(
    os.environ.get(
        "COLOR_GRADE_STYLES_ROOT",
        "color-styles",
    )
).expanduser()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug or "color-style"


def make_swatches(palette: list[dict], output: Path) -> None:
    width, height = 1200, 260
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    top = palette[:8]
    total = sum(item.get("weight", 0) for item in top) or 1
    x = 0
    for index, item in enumerate(top):
        segment_width = width - x if index == len(top) - 1 else int(width * item.get("weight", 0) / total)
        rgb = tuple(item["rgb"])
        draw.rectangle([x, 0, x + segment_width, height], fill=rgb)
        label_color = "white" if item.get("luminance", 0) < 0.42 else "black"
        draw.text((x + 10, height - 32), item["hex"], fill=label_color)
        x += segment_width
    image.save(output)


def default_style_json(style_id: str, name: str, source_name: str, profile: dict, description: str) -> dict:
    return {
        "id": style_id,
        "name": name,
        "version": "1.0.0",
        "created_at": str(date.today()),
        "source_image": source_name,
        "source_image_sha256": profile["image"]["sha256"],
        "description": description,
        "tags": [],
        "mood": [],
        "scene_fit": [],
        "avoid_scenes": [],
        "technical_profile": {
            "image_size": {
                "width": profile["image"]["width"],
                "height": profile["image"]["height"],
                "aspect_ratio": profile["image"]["aspect_ratio"],
            },
            "luminance": profile["luminance"],
            "saturation": profile["saturation"],
            "hue_bias": profile["hue_bias"],
            "grain_estimate": profile["grain_estimate"],
            "regions": profile["regions"],
        },
        "style_philosophy": {
            "emotional_goal": "",
            "contrast_strategy": "",
            "color_strategy": "",
            "subject_strategy": "",
            "texture_strategy": "",
            "do_not_literalize": "Do not copy source scene colors into incompatible target objects.",
        },
        "semantic_transfer_rules": {
            "sky": "",
            "water": "",
            "grass": "",
            "forest": "",
            "mountain": "",
            "skin": "",
            "white_clothing": "",
            "shadow": "",
            "highlight": "",
        },
        "compatibility": {
            "best_for": [],
            "also_works_for": [],
            "weak_for": [],
            "reject_for": ["document", "ID photo", "medical image", "color-critical product"],
            "requires": {
                "has_shadow_structure": None,
                "has_coolable_environment": None,
                "benefits_from_human_anchor": None,
                "needs_highlight_anchor": "",
            },
            "risks": [],
        },
        "palette": profile["palette"],
        "model_prompt": {
            "positive": "",
            "negative": "Do not change composition, identity, objects, pose, weather, season, camera angle, or add/remove elements. Color grade only.",
            "strength_default": 0.55,
            "strength_range": [0.35, 0.75],
            "preserve_content_priority": "very high",
        },
        "retrieval": {
            "keywords": [],
            "embedding_text": "",
        },
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def update_recent_index(styles_root: Path, package_dir: Path, style: dict) -> Path:
    index_dir = styles_root / "_index"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "recent-styles.json"
    if index_path.exists():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            index = {}
    else:
        index = {}

    style_json = package_dir / "style.json"
    entry = {
        "id": style.get("id"),
        "name": style.get("name"),
        "path": str(package_dir),
        "style_json": str(style_json),
        "updated_at": utc_now(),
        "source_image_sha256": style.get("source_image_sha256"),
    }
    recent = [
        item
        for item in index.get("recent", [])
        if item.get("id") != style.get("id") and item.get("style_json") != str(style_json)
    ]
    recent.insert(0, entry)
    index = {
        "styles_root": str(styles_root),
        "updated_at": utc_now(),
        "recent": recent[:100],
    }
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a color grade style package.")
    parser.add_argument("image", type=Path)
    parser.add_argument(
        "--styles-root",
        type=Path,
        default=DEFAULT_STYLES_ROOT,
        help="Root directory for saved style packages. Defaults to COLOR_GRADE_STYLES_ROOT or the shared style library.",
    )
    parser.add_argument("--id", dest="style_id")
    parser.add_argument("--name")
    parser.add_argument("--description", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    image_path = args.image
    name = args.name or image_path.stem
    style_id = args.style_id or slugify(name)
    styles_root = args.styles_root.expanduser()
    package_dir = styles_root / style_id
    if package_dir.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing package: {package_dir}")
    package_dir.mkdir(parents=True, exist_ok=True)

    profile = build_profile(image_path)
    suffix = image_path.suffix.lower() or ".jpg"
    reference_name = f"reference{suffix}"
    shutil.copyfile(image_path, package_dir / reference_name)

    source = Image.open(image_path).convert("RGB")
    thumb = source.copy()
    thumb.thumbnail((900, 1200))
    thumb.save(package_dir / "thumbnail.jpg", quality=90)
    make_swatches(profile["palette"], package_dir / "swatches.png")

    style = default_style_json(style_id, name, reference_name, profile, args.description)
    (package_dir / "style.json").write_text(json.dumps(style, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    index_path = update_recent_index(styles_root, package_dir, style)

    print(json.dumps({
        "styles_root": str(styles_root),
        "package_dir": str(package_dir),
        "style_json": str(package_dir / "style.json"),
        "recent_index": str(index_path),
        "next_step": "Fill style_philosophy, semantic_transfer_rules, compatibility, tags, mood, and model_prompt from visual analysis.",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
