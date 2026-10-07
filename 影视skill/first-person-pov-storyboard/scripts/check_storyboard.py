#!/usr/bin/env python3
"""AI 影像分镜校验器。
用法:
    python3 check_storyboard.py storyboard.json
    python3 check_storyboard.py storyboard.json --strict   # 把 warning 也当失败
    python3 check_storyboard.py storyboard.json --pov      # 强制纯 POV 模式

默认模式为情感叙事（第三人称为主），背影/越肩/侧脸不报错。
--pov 切换为纯 POV 模式，恢复严格的第三人称越界检测和 POV 证据要求。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

# POV 证据类别
EVIDENCE_ALIASES = {
    "身体": "body", "body": "body", "hands": "body",
    "视线": "gaze", "gaze": "gaze", "look": "gaze",
    "互动": "interaction", "interaction": "interaction",
    "动作": "action", "action": "action", "motion": "action",
    "锚点": "anchor", "anchor": "anchor", "prop": "anchor",
}

# 纯 POV 模式下视为越界的第三人称表达
THIRD_PERSON_PATTERNS = [
    r"第三人称", r"背影", r"全身(出现|入画|站在|走)", r"航拍", r"无人机", r"上帝视角",
    r"俯瞰全景", r"越肩", r"过肩镜头", r"监控视角", r"环绕(镜头|拍摄)", r"绕拍",
    r"镜头(拉远|后拉)(到|至)?(远处|户外)?[^。；]*(叙事者|主角|镜头主人)",
    r"(叙事者|主角|镜头主人)(的)?(整个)?身体(出现|可见|入画)",
    r"third[- ]person", r"over[- ]the[- ]shoulder", r"drone shot", r"bird'?s[- ]eye",
    r"wide shot of (the )?(narrator|protagonist)", r"full body of (the )?(narrator|protagonist)",
]

# 需要独立后期文字资产的内容
TEXT_RISK_PATTERNS = [
    r"寻人启事", r"海报", r"公告", r"短信", r"聊天(记录|界面)", r"证件", r"身份证",
    r"名片", r"报纸", r"信件", r"合同", r"标语", r"横幅", r"招牌上的字",
    r"手机(屏幕|界面)", r"电脑(屏幕|界面)", r"文件上的字", r"清晰(可读)?的(中文|文字)",
]

# 隐私与版权风险
PRIVACY_PATTERNS = [
    r"真实(电话|手机号|号码|姓名|身份证|证件号|地址)",
    r"1[3-9]\d{9}",
    r"\b\d{17}[\dXx]\b",
    r"(真人|名人|明星|艺人)(肖像|照片|形象)",
    r"(可识别|真实)的(失踪|受害|患者|儿童)(儿童|人员|信息|资料)",
]

# 单镜动作过载信号
OVERLOAD_PATTERNS = [r"同时", r"接着又", r"然后又", r"一边.*一边", r"边.*边"]

# 情感叙事模式下的合法视角类型（不报第三人称越界）
EMOTIONAL_PERSPECTIVES = {
    "背影跟随", "背跟", "follow-from-behind",
    "侧脸旁观", "侧面旁观", "side-profile",
    "情绪特写", "emotional-closeup",
    "越肩旁观", "越肩", "over-shoulder",
    "静物空镜", "空镜", "establishing-empty",
    "环境空镜", "跨年蒙太奇", "low-angle", "high-angle",
    "第三人称", "third-person",
    "POV", "pov", "第一人称",  # 情感叙事中也可穿插 POV
}

# 情绪特写上限
EMOTIONAL_CLOSEUP_MAX_COUNT = 3
EMOTIONAL_CLOSEUP_MAX_DURATION = 2.0
# 背影跟拍占比下限（情感叙事模式）
BACKSHOT_MIN_RATIO = 0.20
# 切出镜头时长上限（混合/POV 模式下）
CUTOUT_MAX_DURATION = 3.0
CUTOUT_MAX_RATIO = 0.20

# 动态提示词起止
START_PATTERNS = [r"起始", r"开始时", r"画面开始", r"首帧", r"起手", r"最初"]
END_PATTERNS = [r"最后", r"结束(时|于|在)", r"最终(停在|落在)", r"收尾", r"末帧", r"停在"]

REQUIRED_SHOT_FIELDS = [
    "id", "duration_sec", "pov_evidence", "assets",
    "keyframe_prompt", "motion_prompt", "start_state", "end_state",
]

# 否定语境
NEGATION_WINDOW = 12
NEGATION_WORDS = [
    "不", "无", "没有", "禁止", "避免", "切勿", "勿", "非", "杜绝", "排除",
    "not", "no", "never", "avoid", "without",
]


def _is_negated(text, start):
    window = text[max(0, start - NEGATION_WINDOW):start]
    return any(w in window.lower() for w in NEGATION_WORDS)


MAX_HIT_LEN = 24


def _clip(s):
    s = " ".join(str(s).split())
    return s if len(s) <= MAX_HIT_LEN else s[:MAX_HIT_LEN] + "…"


def hits(patterns, text, respect_negation=False):
    found = []
    for pat in patterns:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            if respect_negation and _is_negated(text, m.start()):
                continue
            found.append(_clip(m.group(0)))
            break
    return found


def norm_evidence(item):
    if not isinstance(item, str):
        return None
    key = item.split(":", 1)[0].split("：", 1)[0].strip().lower()
    return EVIDENCE_ALIASES.get(key)


def _get_perspective(shot):
    return str(shot.get("perspective") or shot.get("view_type") or "").strip().lower()


def _is_emotional_perspective(persp):
    """识别情感叙事视角，兼容“中景背影跟随”等带修饰语的变体。"""
    if not persp:
        return False
    exact = {p.lower() for p in EMOTIONAL_PERSPECTIVES}
    keywords = (
        "背影", "背跟", "侧脸", "侧面旁观", "情绪特写", "越肩", "过肩",
        "空镜", "手部特写", "跨年蒙太奇", "低角度", "高角度", "第三人称",
        "follow-from-behind", "side-profile", "emotional-closeup", "over-shoulder",
        "establishing-empty", "third-person",
    )
    return persp in exact or any(k in persp for k in keywords)


def check(data, strict=False, pov_mode=False):
    errors, warnings, notes = [], [], []
    project = data.get("project") or {}
    assets = data.get("assets") or []
    shots = data.get("shots") or []

    if not shots:
        errors.append({"scope": "storyboard", "issue": "shots 为空，没有任何镜头可校验"})
        return build_report(project, assets, shots, errors, warnings, notes, strict, pov_mode)

    # 资产表
    asset_ids = []
    for a in assets:
        aid = str(a.get("id", "")).strip()
        if not aid:
            errors.append({"scope": "assets", "issue": "存在缺少 id 的资产条目"})
            continue
        asset_ids.append(aid)
    dup_assets = [k for k, v in Counter(asset_ids).items() if v > 1]
    if dup_assets:
        errors.append({"scope": "assets", "issue": f"资产编号重复: {', '.join(sorted(dup_assets))}"})

    text_asset_ids = {
        str(a.get("id")) for a in assets
        if str(a.get("type", "")).lower() in {"text", "overlay", "t", "graphic"}
        or str(a.get("id", "")).upper().startswith("T")
    }

    # 镜号唯一性
    shot_ids = [str(s.get("id", "")).strip() for s in shots]
    dup_shots = [k for k, v in Counter(shot_ids).items() if v > 1 and k]
    if dup_shots:
        errors.append({"scope": "shots", "issue": f"镜号重复: {', '.join(sorted(dup_shots))}"})

    total = 0.0
    cutout_total = 0.0
    cutout_count = 0
    emotional_closeup_count = 0
    backshot_total = 0.0
    prev_perspectives = []  # 用于检测连续切出

    for idx, shot in enumerate(shots):
        sid = str(shot.get("id") or f"#{idx + 1}")
        persp = _get_perspective(shot)

        # 判断镜头类型
        is_emotional_perspective = _is_emotional_perspective(persp)
        is_backshot = any(k in persp for k in ("背影", "背跟", "follow-from-behind"))
        is_closeup = persp in {"情绪特写", "emotional-closeup"}
        is_pov = persp in {"pov", "第一人称"}
        is_cutout = is_emotional_perspective and not is_pov if pov_mode else False

        # 情感叙事模式：统计情绪特写和背影跟拍
        if is_closeup:
            emotional_closeup_count += 1
        if is_backshot and isinstance(shot.get("duration_sec"), (int, float)):
            backshot_total += float(shot["duration_sec"])

        # 必填字段
        required = REQUIRED_SHOT_FIELDS
        if is_cutout or (is_emotional_perspective and not pov_mode):
            required = [f for f in REQUIRED_SHOT_FIELDS if f != "pov_evidence"]
        missing = []
        for f in required:
            if f not in shot or shot.get(f) is None or shot.get(f) == "":
                missing.append(f)
        if missing:
            errors.append({"scope": sid, "issue": f"缺少必填字段: {', '.join(missing)}"})

        # 时长
        dur = shot.get("duration_sec")
        if isinstance(dur, (int, float)):
            total += float(dur)
            if dur < 2:
                warnings.append({"scope": sid, "issue": f"单镜 {dur}s 过短"})
            elif dur > 8:
                warnings.append({"scope": sid, "issue": f"单镜 {dur}s 过长，建议拆镜"})
        elif dur is not None:
            errors.append({"scope": sid, "issue": f"duration_sec 必须是数字，当前为 {dur!r}"})

        # POV 证据检查（仅纯 POV 模式下的非切出镜头）
        ev = shot.get("pov_evidence") or []
        if isinstance(ev, str):
            ev = [ev]
        if pov_mode and not is_cutout:
            cats, bad = set(), []
            for item in ev:
                c = norm_evidence(item)
                if c:
                    cats.add(c)
                else:
                    bad.append(item)
            if len(cats) < 2:
                errors.append({
                    "scope": sid,
                    "issue": f"POV 证据类别不足（{len(cats)}/2），已识别: {sorted(cats) or '无'}",
                })
            if bad:
                warnings.append({"scope": sid, "issue": f"无法识别的证据条目: {bad}"})
            for item in ev:
                if isinstance(item, str) and len(item.split(":", 1)[-1].split("：", 1)[-1].strip()) < 4:
                    warnings.append({"scope": sid, "issue": f"证据描述过于笼统: {item!r}"})

        # 情绪特写时长检查
        if is_closeup and isinstance(dur, (int, float)) and dur > EMOTIONAL_CLOSEUP_MAX_DURATION:
            errors.append({
                "scope": sid,
                "issue": f"情绪特写 {dur}s 超过上限 {EMOTIONAL_CLOSEUP_MAX_DURATION}s",
            })

        kf = str(shot.get("keyframe_prompt") or "")
        mp = str(shot.get("motion_prompt") or "")
        blob = f"{kf}\n{mp}"

        # 第三人称越界（仅纯 POV 模式下的非切出镜头）
        if pov_mode and not is_cutout:
            tp = hits(THIRD_PERSON_PATTERNS, blob, respect_negation=True)
            if tp:
                errors.append({"scope": sid, "issue": f"提示词包含第三人称/旁观表达: {tp}"})

        # 动态提示词起止
        if mp:
            if not hits(START_PATTERNS, mp):
                warnings.append({"scope": sid, "issue": "动态提示词缺少明确起始状态"})
            if not hits(END_PATTERNS, mp):
                warnings.append({"scope": sid, "issue": "动态提示词缺少明确结束状态"})

        # 动作过载
        ol = hits(OVERLOAD_PATTERNS, mp)
        if ol:
            warnings.append({"scope": sid, "issue": f"单镜动作可能过载: {ol}，建议拆镜"})

        # 资产引用闭环
        refs = shot.get("assets") or []
        if isinstance(refs, str):
            refs = [refs]
        unknown = [r for r in map(str, refs) if r not in asset_ids]
        if unknown:
            errors.append({"scope": sid, "issue": f"引用了未声明的资产: {unknown}"})

        # 文字资产拆分
        trisk = hits(TEXT_RISK_PATTERNS, kf)
        if trisk and not (set(map(str, refs)) & text_asset_ids):
            warnings.append({"scope": sid, "issue": f"画面含需可读文字 {trisk}，但未引用 T 类后期文字资产"})

        # 隐私与版权
        priv = hits(PRIVACY_PATTERNS, blob, respect_negation=True)
        if priv:
            errors.append({"scope": sid, "issue": f"存在隐私/版权风险内容: {priv}"})

        # 负面词
        if not shot.get("negative_extra") and not data.get("global_negative"):
            notes.append({"scope": sid, "issue": "既无全局负面词也无本镜负面词"})

        # 接镜连续性：缺字段报 warning；状态相同表示已闭环，不另报提示。
        if idx + 1 < len(shots):
            nxt = shots[idx + 1]
            if not (shot.get("end_state") and nxt.get("start_state")):
                warnings.append({"scope": sid, "issue": "缺少接镜所需的 end_state 或下一镜 start_state"})

        # 声音
        if not shot.get("sound"):
            notes.append({"scope": sid, "issue": "未标注声音层"})

    # 情绪特写次数检查（情感叙事模式）
    if not pov_mode and emotional_closeup_count > EMOTIONAL_CLOSEUP_MAX_COUNT:
        errors.append({
            "scope": "project",
            "issue": f"情绪特写共 {emotional_closeup_count} 次，超过上限 {EMOTIONAL_CLOSEUP_MAX_COUNT} 次",
        })

    # 背影跟拍占比检查（情感叙事模式）
    if not pov_mode and total > 0 and backshot_total / total < BACKSHOT_MIN_RATIO:
        warnings.append({
            "scope": "project",
            "issue": f"背影跟拍占比 {backshot_total / total:.0%}，低于建议下限 {BACKSHOT_MIN_RATIO:.0%}",
        })

    # 切出占比检查（纯 POV 模式）
    if pov_mode and total > 0 and cutout_total / total > CUTOUT_MAX_RATIO:
        errors.append({
            "scope": "project",
            "issue": f"切出镜头总时长 {cutout_total:.1f}s 占比 {cutout_total / total:.0%}，超过上限 {CUTOUT_MAX_RATIO:.0%}",
        })

    # 时长核算
    target = project.get("target_duration_sec")
    duration_report = {"sum_sec": round(total, 2), "target_sec": target, "shot_count": len(shots)}
    if isinstance(target, (int, float)) and target > 0:
        delta = total - float(target)
        duration_report["delta_sec"] = round(delta, 2)
        tol = max(2.0, float(target) * 0.1)
        if abs(delta) > tol:
            errors.append({
                "scope": "project",
                "issue": f"时长合计 {total:.1f}s 与目标 {target}s 相差 {delta:+.1f}s，超出容差 {tol:.1f}s",
            })

    return build_report(project, assets, shots, errors, warnings, notes, strict, pov_mode, duration_report)


def build_report(project, assets, shots, errors, warnings, notes, strict, pov_mode, duration=None):
    passed = not errors and (not warnings if strict else True)
    return {
        "ok": True,
        "tool": "ai-storyboard.check",
        "result": {
            "title": project.get("title"),
            "passed": passed,
            "strict": strict,
            "mode": "pov" if pov_mode else "emotional-narrative",
            "duration": duration or {"shot_count": len(shots)},
            "asset_count": len(assets),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "note_count": len(notes),
            "errors": errors,
            "warnings": warnings,
            "notes": notes,
        },
        "evidence": {
            "quote": (
                f"{len(shots)} 镜 / {len(assets)} 资产：{len(errors)} error, "
                f"{len(warnings)} warning, {len(notes)} note"
            )
        },
    }


def main():
    ap = argparse.ArgumentParser(description="AI 影像分镜校验器")
    ap.add_argument("path", help="分镜 JSON 路径")
    ap.add_argument("--strict", action="store_true", help="把 warning 也视为失败")
    ap.add_argument("--pov", action="store_true", help="强制纯 POV 模式")
    args = ap.parse_args()

    try:
        with open(args.path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(json.dumps({"ok": False, "error": {"code": "FILE_NOT_FOUND", "msg": args.path}},
                         ensure_ascii=False))
        return 1
    except json.JSONDecodeError as e:
        print(json.dumps({"ok": False, "error": {"code": "PARSE_ERROR", "msg": str(e)}},
                         ensure_ascii=False))
        return 1

    report = check(data, strict=args.strict, pov_mode=args.pov)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["result"]["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
