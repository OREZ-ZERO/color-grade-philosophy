#!/usr/bin/env python3
"""Heuristically score whether a target image can carry a saved color-grade philosophy."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


DEFAULT_STYLES_ROOT = Path(
    os.environ.get(
        "COLOR_GRADE_STYLES_ROOT",
        "color-styles",
    )
).expanduser()


def contains_any(text: str, values: list[str]) -> bool:
    lowered = text.lower()
    return any(value.lower() in lowered for value in values)


def mode_from_score(score: int, reject: bool) -> str:
    if reject or score < 30:
        return "reject"
    if score >= 78:
        return "direct_apply"
    if score >= 55:
        return "semantic_adapt"
    return "inspired_only"


def score_style(style_json: Path, args: argparse.Namespace) -> dict:
    style = json.loads(style_json.read_text(encoding="utf-8"))
    compatibility = style.get("compatibility", {})
    target_text = f"{args.target_scene} {args.purpose}"

    score = 50
    reasons: list[str] = []
    reject = False

    if contains_any(target_text, compatibility.get("best_for", [])):
        score += 25
        reasons.append("target matches best_for")
    if contains_any(target_text, compatibility.get("also_works_for", [])):
        score += 15
        reasons.append("target matches also_works_for")
    if contains_any(target_text, compatibility.get("weak_for", [])):
        score -= 20
        reasons.append("target matches weak_for")
    if contains_any(target_text, compatibility.get("reject_for", [])) or args.color_critical:
        score -= 45
        reject = True
        reasons.append("target is color-critical or rejected")

    requires = compatibility.get("requires", {})
    if requires.get("has_shadow_structure") is True:
        if args.has_shadow_structure:
            score += 10
            reasons.append("target has shadow structure")
        else:
            score -= 12
            reasons.append("style expects shadow structure")
    if requires.get("benefits_from_human_anchor") is True:
        if args.has_human:
            score += 8
            reasons.append("target has human anchor")
        else:
            score -= 6
            reasons.append("style benefits from a human anchor")
    if requires.get("has_coolable_environment") is True:
        if args.has_sky or any(word in args.target_scene.lower() for word in ["mountain", "sea", "street", "forest", "landscape"]):
            score += 8
            reasons.append("target has coolable environment")
        else:
            score -= 8
            reasons.append("unclear coolable environment")

    if args.local_color_sensitivity == "high":
        score -= 15
        reasons.append("high local-color sensitivity")
    elif args.local_color_sensitivity == "low":
        score += 5
        reasons.append("low local-color sensitivity")

    score = max(0, min(100, score))
    mode = mode_from_score(score, reject)
    strength = {
        "direct_apply": "0.55-0.75",
        "semantic_adapt": "0.40-0.60",
        "inspired_only": "0.20-0.40",
        "reject": "0.00",
    }[mode]

    return {
        "style_id": style.get("id"),
        "style_name": style.get("name"),
        "style_json": str(style_json),
        "target_scene": args.target_scene,
        "score": score,
        "recommended_mode": mode,
        "recommended_strength": strength,
        "reasons": reasons,
        "risks": compatibility.get("risks", []),
    }


def styles_from_recent_index(styles_root: Path) -> list[Path]:
    index_path = styles_root / "_index" / "recent-styles.json"
    if not index_path.exists():
        return []
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    paths = []
    for item in index.get("recent", []):
        style_json = Path(item.get("style_json", ""))
        if style_json.exists():
            paths.append(style_json)
    return paths


def discover_style_jsons(styles_root: Path, recent_first: bool) -> list[Path]:
    styles_root = styles_root.expanduser()
    discovered = [path for path in styles_root.glob("*/style.json") if not path.parent.name.startswith("_")]
    discovered.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    if not recent_first:
        return discovered

    recent = styles_from_recent_index(styles_root)
    seen = {path.resolve() for path in recent}
    return recent + [path for path in discovered if path.resolve() not in seen]


def main() -> None:
    parser = argparse.ArgumentParser(description="Score target/style compatibility.")
    parser.add_argument("style_json", type=Path, nargs="?", help="Specific style.json to score. Omit to scan a style library.")
    parser.add_argument("--styles-root", type=Path, default=DEFAULT_STYLES_ROOT)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--recent-first", action="store_true", help="Prefer ordering from _index/recent-styles.json before modification time.")
    parser.add_argument("--target-scene", default="")
    parser.add_argument("--purpose", default="creative photo edit")
    parser.add_argument("--has-human", action="store_true")
    parser.add_argument("--has-sky", action="store_true")
    parser.add_argument("--has-shadow-structure", action="store_true")
    parser.add_argument("--color-critical", action="store_true")
    parser.add_argument("--local-color-sensitivity", choices=["low", "medium", "high"], default="medium")
    args = parser.parse_args()

    if args.style_json:
        print(json.dumps(score_style(args.style_json, args), ensure_ascii=False, indent=2))
        return

    candidates = discover_style_jsons(args.styles_root, args.recent_first)
    scored = [score_style(style_json, args) for style_json in candidates]
    scored.sort(key=lambda item: item["score"], reverse=True)
    print(json.dumps({
        "styles_root": str(args.styles_root.expanduser()),
        "candidate_count": len(scored),
        "top": scored[:args.top],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
