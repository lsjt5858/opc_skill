#!/usr/bin/env python3
"""Validate a collected image→Seedance 2.5→publishing text package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def issue(level: str, code: str, message: str) -> dict[str, str]:
    return {"level": level, "code": code, "message": message}


def text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a pastoral story delivery package")
    parser.add_argument("input", type=Path, help="UTF-8 JSON delivery package")
    args = parser.parse_args()

    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "errors": [f"无法读取输入：{exc}"]}, ensure_ascii=False, indent=2))
        return 1

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    images = payload.get("image_prompts", [])
    cover = payload.get("cover", {})
    videos = payload.get("video_prompts", [])
    publishing = payload.get("publishing", {})

    if not isinstance(images, list) or not images:
        errors.append(issue("error", "missing_image_prompts", "缺少已收纳的正片图片提示词。"))
    if not isinstance(cover, dict):
        errors.append(issue("error", "invalid_cover", "cover必须是对象。"))
        cover = {}
    required_cover = {
        "source_scene_id": "封面来源镜头ID",
        "story_title": "封面故事名称",
        "prompt": "净底封面提示词",
        "title_layout": "封面叠字规范",
    }
    for key, label in required_cover.items():
        if not text(cover.get(key)):
            errors.append(issue("error", "missing_cover_field", f"缺少{label}。"))
    cover_prompt = text(cover.get("prompt"))
    if cover_prompt and not re.search(r"无文字|no text", cover_prompt, re.I):
        warnings.append(issue("warning", "cover_prompt_text_guard", "净底封面提示词未声明无文字，可能导致模型直接生成错字。"))
    if not isinstance(videos, list) or not videos:
        errors.append(issue("error", "missing_video_prompts", "缺少Seedance 2.5视频分镜提示词。"))

    if isinstance(images, list) and isinstance(videos, list) and len(images) != len(videos):
        errors.append(issue("error", "count_mismatch", f"图片提示词{len(images)}条，视频分镜{len(videos)}条，未一一对应。"))

    image_ids = [str(item.get("id", "")) for item in images if isinstance(item, dict)]
    video_ids = [str(item.get("id", "")) for item in videos if isinstance(item, dict)]
    if image_ids and video_ids and image_ids != video_ids:
        errors.append(issue("error", "id_mismatch", "图片提示词与视频分镜的镜头ID或顺序不一致。"))

    required_timecodes = ("0-1秒", "1-3.2秒", "3.2-4.5秒", "4.5-5秒")
    for index, item in enumerate(videos, 1):
        if not isinstance(item, dict):
            errors.append(issue("error", "invalid_video_item", f"第{index}条视频分镜不是对象。"))
            continue
        prompt = text(item.get("prompt"))
        if not prompt:
            errors.append(issue("error", "empty_video_prompt", f"第{index}条视频分镜为空。"))
            continue
        if "Seedance 2.5" not in prompt and "首帧与唯一视觉锚点" not in prompt:
            errors.append(issue("error", "missing_seedance_anchor", f"第{index}条未声明Seedance 2.5首帧锚点。"))
        missing = [part for part in required_timecodes if part not in prompt]
        if missing:
            errors.append(issue("error", "missing_timecode", f"第{index}条缺少时间段：{'、'.join(missing)}。"))
        if not re.search(r"无字幕|无文字|no text", prompt, re.I):
            warnings.append(issue("warning", "missing_text_guard", f"第{index}条未声明避免画面文字。"))
        if not re.search(r"声音|环境声|sound", prompt, re.I):
            warnings.append(issue("warning", "missing_sound", f"第{index}条未写声音设计。"))

    required_publish = {
        "cover_title": "共用封面标题",
        "cover_subtitle": "共用封面副标题",
        "cover_scene": "共用封面建议",
        "music_direction": "音乐方向",
        "ai_disclosure": "统一AI内容声明",
        "rules_checked_at": "规则核验日期",
        "rule_sources": "规则来源",
        "platforms": "多平台发布包",
    }
    if not isinstance(publishing, dict):
        errors.append(issue("error", "invalid_publishing", "publishing必须是对象。"))
        publishing = {}
    for key, label in required_publish.items():
        value = publishing.get(key)
        if key == "rule_sources":
            if not isinstance(value, list) or not all(text(url) for url in value):
                errors.append(issue("error", "missing_publish_field", f"缺少有效的{label}。"))
        elif key == "platforms":
            if not isinstance(value, dict):
                errors.append(issue("error", "missing_publish_field", f"缺少有效的{label}。"))
        elif not text(value):
            errors.append(issue("error", "missing_publish_field", f"缺少{label}。"))

    ai_disclosure = text(publishing.get("ai_disclosure"))
    if ai_disclosure and not re.search(r"AI|人工智能", ai_disclosure, re.I):
        errors.append(issue("error", "invalid_ai_disclosure", "统一AI内容声明未明确写出AI或人工智能。"))
    if ai_disclosure and not re.search(r"虚构|非真实", ai_disclosure):
        warnings.append(issue("warning", "missing_fiction_disclosure", "AI声明未明确故事或人物为虚构／非真实。"))

    platforms = publishing.get("platforms", {})
    if not isinstance(platforms, dict):
        platforms = {}
    required_platforms = {
        "douyin": "抖音",
        "kuaishou": "快手",
        "xiaohongshu": "小红书",
        "wechat_channels": "微信视频号",
        "bilibili": "B站",
    }
    required_platform_fields = {
        "title": "标题",
        "caption": "正文／简介",
        "tags": "标签",
        "pinned_comment": "置顶评论／首评",
        "ai_disclosure": "AI内容声明",
        "pre_publish_checks": "发布前勾选项",
    }
    for platform_key, platform_label in required_platforms.items():
        package = platforms.get(platform_key)
        if not isinstance(package, dict):
            errors.append(issue("error", "missing_platform", f"缺少{platform_label}发布包。"))
            continue
        for key, label in required_platform_fields.items():
            value = package.get(key)
            if key in {"tags", "pre_publish_checks"}:
                if not isinstance(value, list) or not all(text(item) for item in value):
                    errors.append(issue("error", "missing_platform_field", f"{platform_label}缺少有效的{label}。"))
            elif not text(value):
                errors.append(issue("error", "missing_platform_field", f"{platform_label}缺少{label}。"))
        disclosure = text(package.get("ai_disclosure"))
        if disclosure and not re.search(r"AI|人工智能", disclosure, re.I):
            errors.append(issue("error", "platform_ai_disclosure", f"{platform_label}的AI声明不明确。"))
        tags = package.get("tags", [])
        if isinstance(tags, list) and not 3 <= len(tags) <= 8:
            warnings.append(issue("warning", "tag_count", f"{platform_label}标签数量为{len(tags)}，建议按平台保持3–8个。"))

    captions = {
        key: text(value.get("caption"))
        for key, value in platforms.items()
        if isinstance(value, dict) and text(value.get("caption"))
    }
    if len(captions) > 1 and len(set(captions.values())) == 1:
        errors.append(issue("error", "duplicated_platform_captions", "各平台正文完全相同，未做平台化改写。"))

    if text(cover.get("story_title")) and text(publishing.get("cover_title")):
        if text(cover.get("story_title")) != text(publishing.get("cover_title")):
            errors.append(issue("error", "cover_title_mismatch", "图片阶段的封面故事名称与发布包封面标题不一致。"))
    if text(cover.get("source_scene_id")) and text(publishing.get("cover_scene")):
        if text(cover.get("source_scene_id")) not in text(publishing.get("cover_scene")):
            warnings.append(issue("warning", "cover_scene_mismatch", "发布包封面建议未明确复用图片阶段的封面来源镜头。"))

    result = {
        "passed": not errors,
        "image_prompt_count": len(images) if isinstance(images, list) else 0,
        "cover_fields": sorted(cover.keys()),
        "video_prompt_count": len(videos) if isinstance(videos, list) else 0,
        "publishing_fields": sorted(publishing.keys()),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
