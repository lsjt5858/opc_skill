#!/usr/bin/env python3
"""Validate a rural story plan and optionally compare it with previous episodes.

Plan format:
{
  "scenes": [
    {"id":"01","location":"河埠","action":"等船","people":"1",
     "relationship":"独自等待","prop":"灯","shot":"远景",
     "time":"黎明","next":"客船出现"}
  ]
}

History format (series bible or plain list):
{"episodes":[{"number":1,"scenes":[...]}]}  or  {"scenes":[...]}  or  [ {...}, ... ]
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

REQUIRED = {"id", "location", "action", "people", "relationship", "prop", "shot", "time", "next"}
SIGNATURE_KEYS = ("location", "action", "relationship", "prop")


def load_scenes(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "episodes" in payload:
            scenes = []
            for ep in payload["episodes"]:
                scenes.extend(ep.get("scenes", []))
            return scenes
        return payload.get("scenes", [])
    return []


def signature(scene):
    return tuple(str(scene.get(k, "")).strip() for k in SIGNATURE_KEYS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--expected", type=int, default=15)
    parser.add_argument("--history", type=Path, action="append", default=[])
    args = parser.parse_args()

    scenes = load_scenes(json.loads(args.plan.read_text(encoding="utf-8")))
    errors, warnings = [], []

    if len(scenes) != args.expected:
        errors.append(f"expected {args.expected} scenes, got {len(scenes)}")

    expected_ids = [f"{i:02d}" for i in range(1, len(scenes) + 1)]
    if [str(s.get("id", "")) for s in scenes] != expected_ids:
        errors.append(f"scene ids must be sequential: {expected_ids}")

    for i, scene in enumerate(scenes, 1):
        missing = sorted(REQUIRED - set(scene))
        if missing:
            errors.append(f"scene {i:02d} missing: {', '.join(missing)}")

    for sig, count in Counter(signature(s) for s in scenes).items():
        if count > 1:
            warnings.append(f"duplicate story signature x{count}: {sig}")

    for i in range(len(scenes) - 1):
        a, b = scenes[i], scenes[i + 1]
        same = sum(a.get(k) == b.get(k) for k in ("people", "shot", "location", "time", "action"))
        if same >= 4:
            warnings.append(f"scenes {i+1:02d}-{i+2:02d} are visually too similar ({same}/5)")

    people = Counter(str(s.get("people", "")) for s in scenes)
    if len(people) < 3:
        warnings.append(f"people distribution is too uniform: {dict(people)}")
    if people.get("0", 0) == 0:
        warnings.append("no empty-scene shot; add at least one for pacing")

    shots = Counter(str(s.get("shot", "")) for s in scenes)
    if scenes and len(shots) < 4:
        warnings.append(f"shot variety is low: {dict(shots)}")

    history_scenes = []
    for path in args.history:
        history_scenes.extend(load_scenes(json.loads(path.read_text(encoding="utf-8"))))

    reused = []
    if history_scenes:
        history_sigs = {signature(s) for s in history_scenes}
        history_pairs = Counter(
            (str(s.get("location", "")).strip(), str(s.get("action", "")).strip())
            for s in history_scenes
        )
        for scene in scenes:
            sig = signature(scene)
            if sig in history_sigs:
                reused.append({"id": scene.get("id"), "reason": "identical signature", "signature": sig})
            elif history_pairs.get((sig[0], sig[1])):
                reused.append({"id": scene.get("id"), "reason": "same location+action", "signature": sig[:2]})
        if reused:
            warnings.append(f"{len(reused)} scene(s) reuse earlier episodes")

    result = {
        "passed": not errors,
        "scene_count": len(scenes),
        "people_distribution": dict(people),
        "shot_distribution": dict(shots),
        "history_scenes_checked": len(history_scenes),
        "reused_scenes": reused,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
