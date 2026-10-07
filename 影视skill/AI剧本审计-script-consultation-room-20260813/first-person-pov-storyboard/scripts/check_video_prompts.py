#!/usr/bin/env python3
"""校验生产级视频提示词 Markdown。

用法：python3 check_video_prompts.py prompts.md
检查：镜头编号连续、必备字段完整、首句时长、动作时间轴覆盖到镜头尾、
参考锚定、单镜头约束、无生成字幕、反向锚定与 QC。
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = [
    "【场景】", "【运镜】", "【动作】", "【尾帧】", "【音效】", "【影像调性】",
    "【表演要求】", "【对白】", "【反向锚定】", "【后期与 QC】",
]


def parse_end_seconds(action_text: str):
    ranges = re.findall(r"(\d+(?:\.\d+)?)\s*[-–—至]\s*(\d+(?:\.\d+)?)s?\s*[：:]", action_text)
    return [float(b) for _, b in ranges]


def check(path: Path):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(V\d{2,3})｜[^｜\n]+｜(\d+(?:\.\d+)?)\s*秒\s*$", text, re.M))
    errors, warnings = [], []
    shots = []
    for i, m in enumerate(matches):
        sid, dur_s = m.group(1), float(m.group(2))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        shots.append((sid, dur_s, block))

    if not shots:
        errors.append({"scope": "document", "issue": "未找到形如 ## V01｜镜头名｜8 秒 的镜头标题"})
        return build(path, shots, errors, warnings)

    nums = [int(sid[1:]) for sid, _, _ in shots]
    expected = list(range(nums[0], nums[0] + len(nums)))
    if nums != expected:
        errors.append({"scope": "document", "issue": f"镜头编号不连续: {nums}"})

    for sid, dur, block in shots:
        missing = [f for f in FIELDS if f not in block]
        if missing:
            errors.append({"scope": sid, "issue": f"缺少字段: {', '.join(missing)}"})

        if "单镜头" not in block:
            errors.append({"scope": sid, "issue": "未明确单镜头"})
        if "vertical 9:16" not in block:
            errors.append({"scope": sid, "issue": "未明确 vertical 9:16"})
        if not re.search(r"@\[K\d{2,3}\]", block):
            errors.append({"scope": sid, "issue": "缺少 K 首帧锚定"})
        if "@[S01]" not in block:
            errors.append({"scope": sid, "issue": "缺少 S01 风格锚定"})
        if "无生成字幕" not in block:
            errors.append({"scope": sid, "issue": "未声明无生成字幕"})
        if "NOT " not in block:
            errors.append({"scope": sid, "issue": "反向锚定缺少 NOT 项"})
        if "QC：" not in block and "QC:" not in block:
            errors.append({"scope": sid, "issue": "后期与 QC 未列 QC"})

        action = block.split("【动作】", 1)[1].split("【尾帧】", 1)[0] if "【动作】" in block and "【尾帧】" in block else ""
        ends = parse_end_seconds(action)
        if len(ends) < 3:
            errors.append({"scope": sid, "issue": f"动作时间段不足 3 段，识别到 {len(ends)} 段"})
        elif abs(max(ends) - dur) > 0.01:
            errors.append({"scope": sid, "issue": f"动作时间轴终点 {max(ends)}s 与镜头时长 {dur}s 不一致"})

        if block.count("rack focus") > 1:
            warnings.append({"scope": sid, "issue": "同镜出现多次 rack focus 描述，确认是否仅一次对焦变化"})
        # 仅当出现正向“自动切镜/auto cut”且附近没有否定词时才报错。
        auto_cut_hits = list(re.finditer(r"自动切镜|auto cut", block, re.I))
        for hit in auto_cut_hits:
            window = block[max(0, hit.start() - 12):hit.start()].lower()
            if not any(n in window for n in ("不", "无", "禁止", "not", "no", "without")):
                errors.append({"scope": sid, "issue": "可能要求了自动切镜"})
                break

    return build(path, shots, errors, warnings)


def build(path, shots, errors, warnings):
    passed = not errors
    return {
        "ok": True,
        "tool": "ai-storyboard.check-video-prompts",
        "result": {
            "file": str(path), "passed": passed, "shot_count": len(shots),
            "error_count": len(errors), "warning_count": len(warnings),
            "errors": errors, "warnings": warnings,
        },
        "evidence": {"quote": f"{len(shots)} 镜：{len(errors)} error, {len(warnings)} warning"},
    }


def main():
    ap = argparse.ArgumentParser(description="生产级视频提示词校验器")
    ap.add_argument("path")
    args = ap.parse_args()
    p = Path(args.path)
    if not p.is_file():
        print(json.dumps({"ok": False, "error": {"code": "FILE_NOT_FOUND", "msg": str(p)}}, ensure_ascii=False))
        return 1
    report = check(p)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["result"]["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
