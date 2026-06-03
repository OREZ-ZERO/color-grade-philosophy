#!/usr/bin/env python3
"""Refresh the recent-style index for a color-grade style library."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_STYLES_ROOT = Path(
    os.environ.get(
        "COLOR_GRADE_STYLES_ROOT",
        "color-styles",
    )
).expanduser()


def iso_from_mtime(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_style(style_json: Path) -> dict:
    try:
        return json.loads(style_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def build_entry(style_json: Path) -> dict:
    style = read_style(style_json)
    package_dir = style_json.parent
    return {
        "id": style.get("id") or package_dir.name,
        "name": style.get("name") or package_dir.name,
        "path": str(package_dir),
        "style_json": str(style_json),
        "updated_at": iso_from_mtime(style_json),
        "source_image_sha256": style.get("source_image_sha256"),
    }


def discover(styles_root: Path) -> list[Path]:
    paths = [path for path in styles_root.glob("*/style.json") if not path.parent.name.startswith("_")]
    return sorted(paths, key=lambda path: path.stat().st_mtime, reverse=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Refresh _index/recent-styles.json for a color style library.")
    parser.add_argument("--styles-root", type=Path, default=DEFAULT_STYLES_ROOT)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    styles_root = args.styles_root.expanduser()
    recent = [build_entry(path) for path in discover(styles_root)[: args.limit]]
    index = {
        "styles_root": str(styles_root),
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "recent": recent,
    }
    index_dir = styles_root / "_index"
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "recent-styles.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "styles_root": str(styles_root),
        "style_count": len(recent),
        "recent_index": str(index_path),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
