#!/usr/bin/env python3
"""Lightweight preflight for image/video prompts.

This catches deterministic formatting/platform conflicts and reports softer
compatibility or quality concerns as warnings. It does not emulate a platform's
online moderation system or guarantee acceptance.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

PLATFORMS = ("generic", "midjourney", "seedream", "seedance")
PROMPT_KEYS = {
    "prompt",
    "prompts",
    "prompt_zh",
    "prompt_en",
    "chinese_prompt",
    "english_prompt",
    "中文提示词",
    "英文提示词",
}
MJ_PARAM_RE = re.compile(r"(?<!\w)--([a-z][a-z0-9-]*)(?:\s+([^\s]+))?", re.I)
PLACEHOLDER_RE = re.compile(
    r"\[(?:[^\]]{0,40}(?:待补|填写|替换|placeholder|todo|subject|location|action|season|time|人物|地点|动作|季节|时段)[^\]]{0,40})\]",
    re.I,
)
AGE_AMBIGUOUS_RE = re.compile(r"(?<!成年)(?:女孩|少女)|\b(?:girl|young girl)\b", re.I)
ADULT_RE = re.compile(r"成年|二十[岁多上下出头至到以上]*|2\d\s*(?:岁|year)|young adult|adult woman|adult female", re.I)
WET_RE = re.compile(r"湿衣|湿透|浸湿|贴身|wet clothes?|soaked|drenched|clinging fabric", re.I)
BODY_FOCUS_RE = re.compile(r"身体曲线|胸|臀|大腿|透视|裸露|body curves?|breasts?|buttocks?|thighs?|see[- ]through|transparent clothes?", re.I)
NEGATIVE_RE = re.compile(r"(?<!\w)(?:no|without)\s+[a-z]|无(?:文字|水印|现代|仙侠|重妆|塑料|僵硬|人物|人群|特效|魔法|重复|漂浮)", re.I)
ACTION_HINT_RE = re.compile(r"(?:并|同时|随后|然后|接着|一边.+一边|while|then|and then|before.+after)", re.I)


def load_prompts(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return [{"id": path.name, "text": ""}]

    if path.suffix.lower() != ".json":
        return [{"id": path.name, "text": text.strip()}]

    payload = json.loads(text)
    found: list[dict[str, str]] = []

    def walk(value: Any, label: str, enabled: bool = False) -> None:
        if isinstance(value, str):
            if enabled:
                found.append({"id": label, "text": value.strip()})
            return
        if isinstance(value, list):
            for index, item in enumerate(value, 1):
                walk(item, f"{label}[{index}]", enabled)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                normalized = str(key).strip().lower()
                child_enabled = enabled or normalized in PROMPT_KEYS or "prompt" in normalized or "提示词" in normalized
                walk(item, f"{label}.{key}", child_enabled)

    if isinstance(payload, list) and all(isinstance(item, str) for item in payload):
        walk(payload, "prompts", True)
    elif isinstance(payload, str):
        found.append({"id": "prompt", "text": payload.strip()})
    else:
        walk(payload, "root")

    return found


def issue(level: str, code: str, message: str, suggestion: str = "") -> dict[str, str]:
    result = {"level": level, "code": code, "message": message}
    if suggestion:
        result["suggestion"] = suggestion
    return result


def validate_prompt(text: str, platform: str, max_chars: int) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    normalized = unicodedata.normalize("NFKC", text)

    if not normalized.strip():
        return [issue("error", "empty_prompt", "提示词为空。", "补充可独立使用的提示词正文。")]

    controls = sorted({f"U+{ord(ch):04X}" for ch in normalized if unicodedata.category(ch) == "Cc" and ch not in "\n\r\t"})
    if controls:
        issues.append(issue("error", "control_characters", f"包含不可见控制字符：{', '.join(controls)}。", "删除控制字符后再复制。"))

    if "```" in normalized or re.search(r"(?m)^\s*#{1,6}\s+|\*\*(?:中文|英文|prompt|提示词)", normalized, re.I):
        issues.append(issue("error", "markdown_wrapper", "包含 Markdown 标题、代码围栏或标签，复制时可能被当作提示词正文。", "只复制纯提示词，不包含标题、粗体标签和代码围栏。"))

    placeholders = sorted(set(PLACEHOLDER_RE.findall(normalized)))
    if placeholders:
        issues.append(issue("error", "template_placeholder", f"仍含模板占位符：{'、'.join(placeholders[:4])}。", "替换为具体人物、地点、动作或时间。"))

    params = list(MJ_PARAM_RE.finditer(normalized))
    if params and platform != "midjourney":
        issues.append(issue("error", "platform_parameter_conflict", f"{platform} 模式不接受 Midjourney 风格的 -- 参数。", "删除 --ar / --style / --stylize 等参数，尺寸和风格改在平台界面设置。"))

    if platform == "midjourney":
        allowed = {"ar", "aspect", "style", "stylize", "s", "seed", "chaos", "c", "quality", "q", "no", "iw", "weird", "w", "tile", "stop", "repeat", "r", "raw"}
        for match in params:
            name, value = match.group(1).lower(), match.group(2) or ""
            if name not in allowed:
                issues.append(issue("warning", "unknown_midjourney_parameter", f"未识别的 Midjourney 参数 --{name}。", "核对目标版本的参数名；不确定时删除。"))
            if name in {"ar", "aspect"} and value and not re.fullmatch(r"\d+(?:\.\d+)?:\d+(?:\.\d+)?", value):
                issues.append(issue("error", "invalid_aspect_ratio", f"画幅参数值 {value!r} 不是宽:高格式。", "例如使用 --ar 16:9。"))
            if name in {"stylize", "s", "chaos", "c", "quality", "q", "seed", "stop", "repeat", "r", "weird", "w", "iw"} and value and not re.fullmatch(r"-?\d+(?:\.\d+)?", value):
                issues.append(issue("error", "invalid_numeric_parameter", f"参数 --{name} 的值 {value!r} 不是数字。", "改为目标版本支持的数字值。"))

    if len(normalized) > max_chars:
        issues.append(issue("warning", "long_prompt", f"提示词共 {len(normalized)} 个字符，超过建议值 {max_chars}。", "优先删除重复风格词和重复否定词，保留主体、动作、地域、服装与光线。"))

    negative_count = len(NEGATIVE_RE.findall(normalized))
    if negative_count > 6:
        issues.append(issue("warning", "too_many_negatives", f"检测到约 {negative_count} 个否定约束，可能稀释主体或降低兼容性。", "仅保留当前镜头最必要的 2–4 个负面约束。"))

    if AGE_AMBIGUOUS_RE.search(normalized) and not ADULT_RE.search(normalized):
        issues.append(issue("warning", "ambiguous_age", "人物年龄表达可能被理解为未成年人。", "若设定为成年人，明确写“二十岁以上成年女性”或“young adult woman”。"))

    if WET_RE.search(normalized) and BODY_FOCUS_RE.search(normalized):
        issues.append(issue("warning", "wet_body_focus", "湿衣描述与身体聚焦措辞同时出现，部分平台可能误判。", "把重点改为泼水动作、布料重量、袖口湿痕、水花或环境。"))

    action_hints = len(ACTION_HINT_RE.findall(normalized))
    if action_hints >= 4:
        issues.append(issue("warning", "dense_action_sequence", "同一条提示词可能包含过多连续动作。", "保留一个主要动作和一个直接结果，其余拆成下一镜。"))

    if not re.search(r"无文字|无水印|no text|no watermark", normalized, re.I):
        issues.append(issue("info", "text_artifact_guard", "未声明避免画面文字或水印。", "若画面不需要文字，可加“无文字、无水印”。"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Lightweight prompt preflight")
    parser.add_argument("input", type=Path, help="UTF-8 .txt or .json file")
    parser.add_argument("--platform", choices=PLATFORMS, default="generic")
    parser.add_argument("--max-chars", type=int, default=1800)
    parser.add_argument("--strict", action="store_true", help="treat warnings as failure")
    args = parser.parse_args()

    try:
        prompts = load_prompts(args.input)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "errors": [f"无法读取输入：{exc}"]}, ensure_ascii=False, indent=2))
        return 1

    if not prompts:
        print(json.dumps({
            "passed": False,
            "platform": args.platform,
            "errors": ["未在 JSON 中找到提示词字段；使用 prompt/prompts/prompt_zh/prompt_en 或包含“提示词”的键。"],
        }, ensure_ascii=False, indent=2))
        return 1

    results = []
    counts = {"error": 0, "warning": 0, "info": 0}
    for item in prompts:
        issues = validate_prompt(item["text"], args.platform, args.max_chars)
        for entry in issues:
            counts[entry["level"]] += 1
        results.append({"id": item["id"], "characters": len(item["text"]), "issues": issues})

    failed = counts["error"] > 0 or (args.strict and counts["warning"] > 0)
    if counts["error"]:
        status = "未通过"
    elif counts["warning"]:
        status = "通过但有提醒"
    else:
        status = "通过"

    report = {
        "passed": not failed,
        "status": status,
        "platform": args.platform,
        "strict": args.strict,
        "prompt_count": len(prompts),
        "counts": counts,
        "note": "本地预检只检查格式、平台参数和常见兼容性风险，不保证任何平台在线审核一定通过。",
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
