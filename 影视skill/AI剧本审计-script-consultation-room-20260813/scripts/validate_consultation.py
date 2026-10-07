#!/usr/bin/env python3
"""校验结构化剧本会诊记录。"""

import argparse
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
from pathlib import Path
import shlex
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - depends on the runtime environment
    Draft202012Validator = None
    JSONSCHEMA_IMPORT_ERROR = exc
else:
    JSONSCHEMA_IMPORT_ERROR = None


TRANSITIONS = {
    "detected": {"verified", "rejected", "deferred"},
    "verified": {"disputed", "accepted", "rejected", "deferred"},
    "disputed": {"accepted", "rejected", "deferred"},
    "accepted": {"fixed", "deferred"},
    "fixed": {"partially_fixed", "regressed", "closed"},
    "partially_fixed": {"fixed", "regressed", "deferred"},
    "regressed": {"accepted", "fixed", "deferred"},
    "deferred": {"accepted", "rejected"},
    "rejected": set(),
    "closed": set(),
}

REGRESSION_STATUSES = {"fixed", "partially_fixed", "regressed", "closed"}
REVIEW_REQUIRED_STATUSES = {
    "accepted",
    "fixed",
    "partially_fixed",
    "regressed",
    "closed",
}
SUPPORTED_PRIOR_STATUSES = {
    "accepted",
    "fixed",
    "partially_fixed",
    "regressed",
    "closed",
}
HEALTH_DIMENSIONS = {
    "structure",
    "character",
    "rhythm",
    "emotion",
    "visual_storytelling",
    "audience_propulsion",
    "producibility",
}


def _objects(value):
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_ids(value):
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _duplicate_values(values):
    seen = set()
    duplicates = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def allowed_status_after(prior_status, observation, has_verification):
    """返回允许的 status_after 值及其精确历史后缀。"""
    if prior_status == "accepted":
        if observation == "FIXED":
            allowed = {"fixed": ["fixed"]}
            if has_verification:
                allowed["closed"] = ["fixed", "closed"]
            return allowed
        if observation in {"PARTIALLY_FIXED", "UNFIXED", "REGRESSED"}:
            return {"accepted": []}
    elif prior_status == "fixed":
        if observation == "FIXED":
            return {"closed": ["closed"]} if has_verification else {"fixed": []}
        if observation == "PARTIALLY_FIXED":
            return {"partially_fixed": ["partially_fixed"]}
        if observation in {"UNFIXED", "REGRESSED"}:
            return {"regressed": ["regressed"]}
    elif prior_status == "partially_fixed":
        if observation == "FIXED":
            allowed = {"fixed": ["fixed"]}
            if has_verification:
                allowed["closed"] = ["fixed", "closed"]
            return allowed
        if observation in {"PARTIALLY_FIXED", "UNFIXED"}:
            return {"partially_fixed": []}
        if observation == "REGRESSED":
            return {"regressed": ["regressed"]}
    elif prior_status == "regressed":
        if observation == "FIXED":
            return {"fixed": ["fixed"]}
        if observation in {"PARTIALLY_FIXED", "UNFIXED", "REGRESSED"}:
            return {"regressed": []}
    elif prior_status == "closed":
        if observation in {"FIXED", "PARTIALLY_FIXED", "UNFIXED", "REGRESSED"}:
            return {"closed": []}
    return {}


def _health_errors(health, known_issue_ids):
    errors = []
    if not isinstance(health, dict):
        return errors

    dimensions = _objects(health.get("dimensions"))
    names = [
        dimension.get("name")
        for dimension in dimensions
        if isinstance(dimension.get("name"), str)
    ]
    if len(dimensions) != 7 or set(names) != HEALTH_DIMENSIONS:
        errors.append("health 必须且只能包含七个维度")
    for name in sorted(_duplicate_values(names)):
        errors.append(f"health 维度重复: {name}")

    overall_score = health.get("overall_score")
    applicable = []
    n_a_count = 0
    for index, dimension in enumerate(dimensions):
        name = dimension.get("name")
        label = name if isinstance(name, str) else f"dimensions[{index}]"
        applicability = dimension.get("applicability")
        score = dimension.get("score")
        weight = dimension.get("weight")

        if applicability == "N_A":
            n_a_count += 1
            if score is not None or weight is not None:
                errors.append(f"{label}: N_A 的 score 和 weight 必须为 null")
        elif applicability == "APPLICABLE":
            applicable.append(dimension)
            if score is None:
                errors.append(f"{label}: APPLICABLE 必须提供 score")
            if (
                isinstance(score, (int, float))
                and not isinstance(score, bool)
                and score >= 7
                and not _string_ids(dimension.get("linked_strengths"))
            ):
                errors.append(
                    f"{label}: 7 分及以上必须提供 linked_strengths"
                )

        for issue_id in _string_ids(dimension.get("linked_issue_ids")):
            if issue_id not in known_issue_ids:
                errors.append(f"未知 health linked_issue_id: {issue_id}")

    if n_a_count > 3 and overall_score is not None:
        errors.append("超过半数维度为 N_A 时，health.overall_score 必须为 null")

    weights = [
        dimension.get("weight")
        for dimension in applicable
        if isinstance(dimension.get("weight"), int)
        and not isinstance(dimension.get("weight"), bool)
    ]
    requires_weighted_dimensions = overall_score is not None or len(applicable) >= 3
    if requires_weighted_dimensions:
        if len(weights) != len(applicable) or sum(weights) != 100:
            errors.append("health 中适用维度的权重总和必须为 100")
    elif len(applicable) in {1, 2} and any(
        dimension.get("weight") is not None for dimension in applicable
    ):
        errors.append(
            "只有一两个 APPLICABLE 维度时，权重必须为 null"
        )

    if overall_score is not None:
        scores_and_weights = [
            (dimension.get("score"), dimension.get("weight"))
            for dimension in applicable
        ]
        if all(
            isinstance(score, (int, float))
            and not isinstance(score, bool)
            and isinstance(weight, int)
            and not isinstance(weight, bool)
            for score, weight in scores_and_weights
        ):
            try:
                calculated = (
                    sum(
                        Decimal(str(score)) * Decimal(weight)
                        for score, weight in scores_and_weights
                    )
                    / Decimal(100)
                ).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                supplied = Decimal(str(overall_score))
                if supplied != calculated:
                    errors.append(
                        f"health.overall_score 必须按加权四舍五入计算等于 {calculated}"
                    )
            except (InvalidOperation, TypeError, ValueError):
                pass

    return errors


def _cycle_errors(parent_by_issue):
    errors = []
    finished = set()
    reported_cycles = set()

    for start in sorted(parent_by_issue):
        if start in finished:
            continue

        path = []
        position = {}
        current = start
        while current in parent_by_issue and current not in finished:
            if current in position:
                cycle = path[position[current] :]
                signature = frozenset(cycle)
                if signature not in reported_cycles:
                    reported_cycles.add(signature)
                    errors.append(
                        "根因图存在循环: " + " -> ".join(cycle + [current])
                    )
                break
            position[current] = len(path)
            path.append(current)
            parent = parent_by_issue.get(current)
            if not isinstance(parent, str):
                break
            current = parent

        finished.update(path)

    return errors


def semantic_errors(data):
    """返回 *data* 中可发现的全部语义校验错误。"""
    errors = []
    if not isinstance(data, dict):
        return errors

    issues = _objects(data.get("issues"))
    issue_ids = []
    seen_ids = set()
    duplicate_ids = set()
    for issue in issues:
        issue_id = issue.get("issue_id")
        if not isinstance(issue_id, str):
            continue
        issue_ids.append(issue_id)
        if issue_id in seen_ids:
            duplicate_ids.add(issue_id)
        seen_ids.add(issue_id)

    for issue_id in sorted(duplicate_ids):
        errors.append(f"issue_id 重复: {issue_id}")

    known_issue_ids = set(issue_ids)
    regression = data.get("regression")
    if not isinstance(regression, dict):
        regression = {}

    mode = data.get("mode")
    user_mode = mode.get("user_mode") if isinstance(mode, dict) else None

    required_values = _string_ids(regression.get("required_issue_ids"))
    checked_values = _string_ids(regression.get("checked_issue_ids"))
    issue_results = _objects(regression.get("issue_results"))
    result_values = [
        result.get("issue_id")
        for result in issue_results
        if isinstance(result.get("issue_id"), str)
    ]

    required_issue_ids = set(required_values)
    checked_issue_ids = set(checked_values)
    result_issue_ids = set(result_values)

    for issue_id in sorted(_duplicate_values(required_values)):
        errors.append(f"regression.required_issue_ids 重复: {issue_id}")
    for issue_id in sorted(_duplicate_values(checked_values)):
        errors.append(f"regression.checked_issue_ids 重复: {issue_id}")
    for issue_id in sorted(_duplicate_values(result_values)):
        errors.append(f"regression.issue_results issue_id 重复: {issue_id}")

    for issue_id in sorted(required_issue_ids - known_issue_ids):
        errors.append(
            f"regression.required_issue_ids 中存在未知 issue_id: {issue_id}"
        )
    for issue_id in sorted(checked_issue_ids - known_issue_ids):
        errors.append(
            f"regression.checked_issue_ids 中存在未知 issue_id: {issue_id}"
        )
    for issue_id in sorted(result_issue_ids - known_issue_ids):
        errors.append(
            f"regression.issue_results 中存在未知 issue_id: {issue_id}"
        )

    if not (
        required_issue_ids == checked_issue_ids == result_issue_ids
        and len(required_values) == len(checked_values) == len(result_values)
    ):
        errors.append(
            "regression.required_issue_ids, checked_issue_ids, and issue_results "
            "必须包含完全相同的 issue ID"
        )

    issue_by_id = {}
    for issue in issues:
        issue_id = issue.get("issue_id")
        if isinstance(issue_id, str) and issue_id not in issue_by_id:
            issue_by_id[issue_id] = issue

    prior_consultation = regression.get("prior_consultation")
    escalated_values = _string_ids(regression.get("escalated_dispute_ids"))
    escalated_dispute_ids = set(escalated_values)
    prior_issue_by_id = {}
    prior_required_ids = set()
    prior_creative_lock = {}

    if user_mode == "REVISION_REVIEW":
        if not isinstance(prior_consultation, dict):
            errors.append("REVISION_REVIEW 要求 prior_consultation 为对象")
        else:
            script = data.get("script")
            current_parent_version = (
                script.get("parent_version") if isinstance(script, dict) else None
            )
            prior_script_version = prior_consultation.get("script_version")
            if current_parent_version != prior_script_version:
                errors.append(
                    "script.parent_version 必须等于 prior_consultation.script_version"
                )
            current_script_version = (
                script.get("script_version") if isinstance(script, dict) else None
            )
            if current_script_version == prior_script_version:
                errors.append(
                    "script.script_version 必须不同于 prior_consultation.script_version"
                )
            if prior_consultation.get("consultation_id") == data.get(
                "consultation_id"
            ):
                errors.append(
                    "prior_consultation.consultation_id 必须不同于当前 consultation_id"
                )

            for prior_issue in _objects(prior_consultation.get("required_issues")):
                prior_issue_id = prior_issue.get("issue_id")
                if isinstance(prior_issue_id, str):
                    if prior_issue_id in prior_issue_by_id:
                        errors.append(
                            f"prior_consultation required issue_id 重复: {prior_issue_id}"
                        )
                    else:
                        prior_issue_by_id[prior_issue_id] = prior_issue
            prior_required_ids = set(prior_issue_by_id)
            if required_issue_ids != prior_required_ids:
                errors.append(
                    "regression.required_issue_ids 必须等于 prior_consultation.required_issues 的 ID 集合"
                )

            for prior_issue_id, prior_issue in prior_issue_by_id.items():
                current_issue = issue_by_id.get(prior_issue_id)
                if current_issue is None:
                    errors.append(
                        f"当前 issues 缺少基线问题: {prior_issue_id}"
                    )
                    continue
                if current_issue.get("priority") != prior_issue.get("priority"):
                    errors.append(
                        f"{prior_issue_id}: priority 必须与 prior_consultation 快照一致"
                    )

            prior_lock_value = prior_consultation.get("creative_lock")
            if isinstance(prior_lock_value, dict):
                prior_creative_lock = prior_lock_value
            current_lock = data.get("creative_lock")
            current_lock_keys = set(current_lock) if isinstance(current_lock, dict) else set()
            if current_lock_keys != set(prior_creative_lock):
                errors.append(
                    "当前 creative_lock 的键必须等于 prior_consultation creative_lock 的键"
                )
    else:
        nonempty_fields = []
        if prior_consultation is not None:
            nonempty_fields.append("prior_consultation")
        for field in (
            "required_issue_ids",
            "checked_issue_ids",
            "issue_results",
            "creative_lock_checks",
            "escalated_dispute_ids",
        ):
            value = regression.get(field)
            if isinstance(value, list) and value:
                nonempty_fields.append(field)
            elif value is not None and not isinstance(value, list):
                nonempty_fields.append(field)
        if nonempty_fields:
            errors.append(
                "非 REVISION_REVIEW 模式下，regression 字段必须为 null 或空: "
                + ", ".join(nonempty_fields)
            )

    if user_mode == "REVISION_REVIEW":
        historical_review_ids = {
            issue_id
            for issue_id, issue in issue_by_id.items()
            if not issue_id.startswith("NEW-")
            and isinstance(issue.get("status"), str)
            and issue.get("status") in REVIEW_REQUIRED_STATUSES
        }
        missing_required_ids = sorted(historical_review_ids - required_issue_ids)
        if missing_required_ids:
            errors.append(
                "regression.required_issue_ids 缺少历史复审问题: "
                + ", ".join(missing_required_ids)
            )

    for index, result in enumerate(issue_results):
        issue_id = result.get("issue_id")
        label = issue_id if isinstance(issue_id, str) else f"issue_results[{index}]"
        issue = issue_by_id.get(issue_id) if isinstance(issue_id, str) else None
        status_after = result.get("status_after")
        observation = result.get("observation")
        prior_status = result.get("prior_status")
        linked_new_issue_id = result.get("linked_new_issue_id")

        prior_issue = (
            prior_issue_by_id.get(issue_id) if isinstance(issue_id, str) else None
        )
        if isinstance(prior_issue, dict) and prior_status != prior_issue.get("status"):
            errors.append(f"{label}: prior_status 必须匹配 prior_consultation 快照")

        if isinstance(issue, dict) and status_after != issue.get("status"):
            errors.append(f"{label}: status_after 必须等于 issue status")

        if observation == "FIXED" and (
            not isinstance(status_after, str)
            or status_after not in {"fixed", "closed"}
        ):
            errors.append(
                f"{label}: FIXED 观察要求 status_after 为 fixed 或 closed"
            )
        elif (
            isinstance(observation, str)
            and observation in {"PARTIALLY_FIXED", "UNFIXED", "REGRESSED"}
            and isinstance(status_after, str)
            and status_after in {"fixed", "closed"}
            and prior_status != "closed"
        ):
            errors.append(
                f"{label}: 只有 FIXED 观察可以将 status_after 设为 fixed 或 closed"
            )

        verification_evidence = result.get("verification_evidence")
        has_verification = isinstance(verification_evidence, str) and bool(
            verification_evidence.strip()
        )
        if status_after == "closed" and not has_verification:
            errors.append(f"{label}: closed 要求提供 verification_evidence")

        changed_locations = result.get("changed_locations")
        reviewed_locations = result.get("reviewed_locations")
        change_evidence = result.get("change_evidence")
        has_changed_locations = (
            isinstance(changed_locations, list) and len(changed_locations) > 0
        )
        has_change_evidence = isinstance(change_evidence, str) and bool(
            change_evidence.strip()
        )
        unreviewed_changes = sorted(
            set(_string_ids(changed_locations))
            - set(_string_ids(reviewed_locations))
        )
        if unreviewed_changes:
            errors.append(
                f"{label}: changed_locations 未出现在 reviewed_locations 中: "
                + ", ".join(unreviewed_changes)
            )
        if observation == "UNFIXED":
            if changed_locations != [] or change_evidence is not None:
                errors.append(
                    f"{label}: UNFIXED 要求 changed_locations 为空且 change_evidence 为 null"
                )
        elif isinstance(observation, str) and observation in {
            "FIXED",
            "PARTIALLY_FIXED",
            "REGRESSED",
        }:
            if (
                has_changed_locations and not has_change_evidence
            ) or (
                not has_changed_locations and change_evidence is not None
            ):
                errors.append(
                    f"{label}: changed_locations 和 change_evidence 必须同时提供"
                )
            requires_change_evidence = (
                observation == "FIXED"
                and prior_status in {"accepted", "partially_fixed", "regressed"}
            ) or (
                observation in {"PARTIALLY_FIXED", "REGRESSED"}
                and prior_status != "closed"
            )
            if requires_change_evidence and not (
                has_changed_locations and has_change_evidence
            ):
                errors.append(
                    f"{label}: 既往状态为 {prior_status} 时，{observation} 要求提供 "
                    "changed_locations 和 change_evidence"
                )

        if has_changed_locations and isinstance(prior_consultation, dict):
            script = data.get("script")
            current_source_hash = (
                script.get("source_hash") if isinstance(script, dict) else None
            )
            if current_source_hash == prior_consultation.get("source_hash"):
                errors.append(
                    f"{label}: 存在 changed_locations 时，当前 source_hash "
                    "必须不同于既往 source_hash"
                )

        if prior_status == "closed":
            if observation == "FIXED":
                if linked_new_issue_id is not None:
                    errors.append(
                        f"{label}: closed + FIXED 要求 linked_new_issue_id 为 null"
                    )
                if not has_verification:
                    errors.append(
                        f"{label}: closed + FIXED 要求提供 verification_evidence"
                    )
            elif observation in {"PARTIALLY_FIXED", "UNFIXED", "REGRESSED"}:
                linked_issue = (
                    issue_by_id.get(linked_new_issue_id)
                    if isinstance(linked_new_issue_id, str)
                    else None
                )
                if (
                    not isinstance(linked_new_issue_id, str)
                    or linked_new_issue_id == issue_id
                    or not linked_new_issue_id.startswith("NEW-SC-")
                    or linked_issue is None
                ):
                    errors.append(
                        f"{label}: closed 回归要求 linked_new_issue_id 指向现有 NEW-SC 问题"
                    )
        elif linked_new_issue_id is not None:
            errors.append(
                f"{label}: 除非 prior_status 为 closed，否则 linked_new_issue_id 必须为 null"
            )

        if isinstance(prior_status, str):
            if prior_status not in SUPPORTED_PRIOR_STATUSES:
                errors.append(f"{label}: 不支持的 prior_status: {prior_status}")
            elif isinstance(issue, dict):
                history = issue.get("status_history")
                prior_positions = (
                    [
                        position
                        for position, state in enumerate(history)
                        if state == prior_status
                    ]
                    if isinstance(history, list)
                    else []
                )
                if not prior_positions:
                    errors.append(
                        f"{label}: status_history 中未找到 prior_status: {prior_status}"
                    )
                elif isinstance(observation, str) and isinstance(status_after, str):
                    allowed = allowed_status_after(
                        prior_status, observation, has_verification
                    )
                    expected_suffix = allowed.get(status_after)
                    if expected_suffix is None:
                        errors.append(
                            f"{label}: 不允许的观察/状态映射: "
                            f"{prior_status} + {observation} -> {status_after}"
                        )
                    else:
                        actual_suffix = history[prior_positions[-1] + 1 :]
                        if actual_suffix != expected_suffix:
                            errors.append(
                                f"{label}: prior_status {prior_status} 之后的 "
                                f"status_history 后缀必须是 {expected_suffix!r}"
                            )

    creative_lock_checks = _objects(regression.get("creative_lock_checks"))
    lock_item_values = [
        check.get("lock_item")
        for check in creative_lock_checks
        if isinstance(check.get("lock_item"), str)
    ]
    for lock_item in sorted(_duplicate_values(lock_item_values)):
        errors.append(
            f"regression.creative_lock_checks lock_item 重复: {lock_item}"
        )

    if user_mode == "REVISION_REVIEW":
        creative_lock = data.get("creative_lock")
        creative_lock_keys = (
            set(creative_lock) if isinstance(creative_lock, dict) else set()
        )
        checked_lock_items = set(lock_item_values)
        if (
            checked_lock_items != creative_lock_keys
            or len(lock_item_values) != len(checked_lock_items)
        ):
            missing_lock_items = sorted(creative_lock_keys - checked_lock_items)
            unknown_lock_items = sorted(checked_lock_items - creative_lock_keys)
            details = []
            if missing_lock_items:
                details.append("缺少 " + ", ".join(missing_lock_items))
            if unknown_lock_items:
                details.append("未知 " + ", ".join(unknown_lock_items))
            if len(lock_item_values) != len(checked_lock_items):
                details.append("lock_item 重复")
            errors.append(
                "regression.creative_lock_checks 必须精确覆盖 creative_lock 的键"
                + (": " + "; ".join(details) if details else "")
            )

    for index, check in enumerate(creative_lock_checks):
        lock_item = check.get("lock_item")
        outcome = check.get("outcome")
        current_lock = data.get("creative_lock")
        prior_value = (
            prior_creative_lock.get(lock_item)
            if isinstance(lock_item, str)
            else None
        )
        current_value = (
            current_lock.get(lock_item)
            if isinstance(current_lock, dict) and isinstance(lock_item, str)
            else None
        )
        if outcome == "PRESERVED" and current_value != prior_value:
            errors.append(
                f"creative_lock_checks[{index}]: PRESERVED 值必须等于既往值"
            )
        elif outcome == "APPROVED_CHANGE":
            for field in (
                "approval_reference",
                "old_value",
                "new_value",
                "effective_version",
            ):
                value = check.get(field)
                if not (isinstance(value, str) and value.strip()):
                    errors.append(
                        f"creative_lock_checks[{index}]: APPROVED_CHANGE 要求提供 {field}"
                    )
            expected_values = {
                "old_value": prior_value,
                "new_value": current_value,
                "effective_version": (
                    data.get("script", {}).get("script_version")
                    if isinstance(data.get("script"), dict)
                    else None
                ),
            }
            for field, expected in expected_values.items():
                if check.get(field) != expected:
                    errors.append(
                        f"creative_lock_checks[{index}]: APPROVED_CHANGE 的 {field} 必须匹配绑定版本"
                    )

    final_result = regression.get("final_result")
    if user_mode == "REVISION_REVIEW":
        if final_result is None:
            errors.append("REVISION_REVIEW 的 final_result 不得为 null")
    elif final_result is not None:
        errors.append("非 REVISION_REVIEW 模式下 final_result 必须为 null")

    parent_by_issue = {}
    for index, issue in enumerate(issues):
        issue_id = issue.get("issue_id")
        label = issue_id if isinstance(issue_id, str) else f"issues[{index}]"
        parent = issue.get("parent_issue")
        if isinstance(parent, str):
            if parent not in known_issue_ids:
                errors.append(f"{label}: parent_issue 不存在: {parent}")
            if isinstance(issue_id, str) and issue_id not in parent_by_issue:
                parent_by_issue[issue_id] = parent
        elif isinstance(issue_id, str) and issue_id not in parent_by_issue:
            parent_by_issue[issue_id] = None

        status = issue.get("status")
        history = issue.get("status_history")
        if isinstance(history, list) and history:
            if history[0] != "detected":
                errors.append(f"{label}: status_history 必须以 detected 开始")
            if status != history[-1]:
                errors.append(
                    f"{label}: status 必须等于 status_history 最后一项"
                )

            for history_index, state in enumerate(history):
                if not isinstance(state, str) or state not in TRANSITIONS:
                    errors.append(
                        f"{label}: status_history[{history_index}] 中存在未知 status: {state!r}"
                    )

            for previous, following in zip(history, history[1:]):
                if (
                    isinstance(previous, str)
                    and isinstance(following, str)
                    and previous in TRANSITIONS
                    and following in TRANSITIONS
                    and following not in TRANSITIONS[previous]
                ):
                    errors.append(
                        f"{label}: 非法状态转换: {previous} -> {following}"
                    )

        if (
            isinstance(status, str)
            and status in REGRESSION_STATUSES
            and isinstance(issue_id, str)
            and issue_id not in checked_issue_ids
        ):
            errors.append(
                f"{label}: {status} 问题必须出现在 regression.checked_issue_ids 中"
            )

    errors.extend(_cycle_errors(parent_by_issue))

    dispute_by_id = {}
    dispute_ids = []
    option_ids_by_dispute = {}
    for index, dispute in enumerate(_objects(data.get("disputes"))):
        dispute_id = dispute.get("dispute_id")
        if not isinstance(dispute_id, str):
            continue
        dispute_ids.append(dispute_id)
        if dispute_id not in dispute_by_id:
            dispute_by_id[dispute_id] = dispute
        option_ids = [
            option.get("option_id")
            for option in _objects(dispute.get("options"))
            if isinstance(option.get("option_id"), str)
        ]
        for option_id in sorted(_duplicate_values(option_ids)):
            errors.append(
                f"disputes[{index}]: option_id 重复: {option_id}"
            )
        option_ids_by_dispute[dispute_id] = set(option_ids)

    for dispute_id in sorted(_duplicate_values(dispute_ids)):
        errors.append(f"dispute_id 重复: {dispute_id}")

    decided_disputes = set()
    decision_ids = []
    for index, decision in enumerate(_objects(data.get("decisions"))):
        dispute_id = decision.get("dispute_id")
        if not isinstance(dispute_id, str):
            continue
        decision_ids.append(dispute_id)
        if dispute_id not in dispute_by_id:
            errors.append(f"decisions[{index}]: 未知 dispute_id: {dispute_id}")
            continue

        selected_option = decision.get("selected_option")
        option_ids = option_ids_by_dispute.get(dispute_id, set())
        rejected_ids = [
            item.get("option_id")
            for item in _objects(decision.get("rejected_options"))
            if isinstance(item.get("option_id"), str)
        ]
        rejected_set = set(rejected_ids)
        complete = True
        if selected_option not in option_ids:
            errors.append(
                f"decisions[{index}]: selected_option 不在争议选项中"
            )
            complete = False
        for option_id in sorted(_duplicate_values(rejected_ids)):
            errors.append(
                f"decisions[{index}]: rejected option_id 重复: {option_id}"
            )
            complete = False
        expected_rejected = option_ids - {selected_option}
        if rejected_set != expected_rejected:
            errors.append(
                f"decisions[{index}]: rejected_options 必须覆盖每个未选选项"
            )
            complete = False
        if complete:
            decided_disputes.add(dispute_id)

    for dispute_id in sorted(_duplicate_values(decision_ids)):
        errors.append(f"decision dispute_id 重复: {dispute_id}")

    unresolved_disputes = set()
    for dispute_id in dispute_by_id:
        if dispute_id not in decided_disputes:
            unresolved_disputes.add(dispute_id)
    if user_mode == "REVISION_REVIEW":
        if unresolved_disputes != escalated_dispute_ids:
            errors.append(
                "regression.escalated_dispute_ids 必须精确等于未解决争议"
            )
    else:
        for dispute_id in sorted(unresolved_disputes):
            errors.append(f"争议未解决: {dispute_id}")

    if user_mode == "REVISION_REVIEW":
        result_by_id = {
            result.get("issue_id"): result
            for result in issue_results
            if isinstance(result.get("issue_id"), str)
        }
        revision_reasons = []
        focused_reasons = []

        for issue_id in sorted(required_issue_ids):
            issue = issue_by_id.get(issue_id)
            result = result_by_id.get(issue_id)
            if not isinstance(issue, dict) or not isinstance(result, dict):
                continue
            priority = issue.get("priority")
            observation = result.get("observation")
            if (
                isinstance(priority, str)
                and priority in {"P0", "P1"}
                and observation != "FIXED"
            ):
                revision_reasons.append(f"必需 {priority} {issue_id} 为 {observation}")
            elif (
                isinstance(priority, str)
                and priority in {"P2", "P3"}
                and observation != "FIXED"
            ):
                focused_reasons.append(f"必需 {priority} {issue_id} 为 {observation}")
            if result.get("status_after") == "fixed":
                focused_reasons.append(f"{issue_id} 等待关闭验证")

        for issue_id, issue in sorted(issue_by_id.items()):
            if not issue_id.startswith("NEW-SC-"):
                continue
            priority = issue.get("priority")
            if isinstance(priority, str) and priority in {"P0", "P1"}:
                revision_reasons.append(f"新 {priority} 问题 {issue_id}")
            elif isinstance(priority, str) and priority in {"P2", "P3"}:
                focused_reasons.append(f"新 {priority} 问题 {issue_id}")

        violated_items = sorted(
            check.get("lock_item")
            for check in creative_lock_checks
            if check.get("outcome") == "VIOLATED"
            and isinstance(check.get("lock_item"), str)
        )
        for lock_item in violated_items:
            revision_reasons.append(f"创作锁被违反: {lock_item}")
        for dispute_id in sorted(escalated_dispute_ids):
            focused_reasons.append(f"升级争议 {dispute_id}")

        if revision_reasons:
            derived_result = "REVISION_REQUIRED"
            verdict_reasons = revision_reasons
        elif focused_reasons:
            derived_result = "FOCUSED_REVIEW_REQUIRED"
            verdict_reasons = focused_reasons
        else:
            derived_result = "PASS"
            verdict_reasons = ["所有机器可检查的改稿条件均已通过"]

        if final_result != derived_result:
            errors.append(
                f"final_result 不匹配: 期望 {derived_result}, 实际 {final_result}; "
                "原因: " + "; ".join(verdict_reasons)
            )

        if final_result == "PASS" and unresolved_disputes:
            errors.append("PASS 要求所有争议均已解决")

    errors.extend(_health_errors(data.get("health"), known_issue_ids))

    return errors


def _reject_non_finite(value):
    raise ValueError(f"非有限 JSON 数字: {value}")


def _reject_duplicate_object_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON 对象键重复: {key}")
        result[key] = value
    return result


def _load_json(path, description):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(
                handle,
                parse_constant=_reject_non_finite,
                object_pairs_hook=_reject_duplicate_object_keys,
            )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"无法从 {path} 读取 {description} JSON: {exc}") from exc


def _json_path(error):
    path = "$"
    for part in error.absolute_path:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f"[{json.dumps(part, ensure_ascii=False)}]"
    return path


def _parser():
    default_schema = Path(__file__).resolve().parent.parent / "references" / "consultation.schema.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("consultation", type=Path)
    parser.add_argument("--schema", type=Path, default=default_schema)
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)

    if Draft202012Validator is None:
        requirements = Path(__file__).resolve().parent.parent / "requirements.txt"
        install_command = (
            f"{shlex.quote(sys.executable)} -m pip install -r "
            f"{shlex.quote(str(requirements))}"
        )
        print(
            f"jsonschema 依赖错误: {JSONSCHEMA_IMPORT_ERROR}. "
            f"请安装: {install_command}",
            file=sys.stderr,
        )
        return 2

    try:
        consultation = _load_json(args.consultation, "consultation")
        schema = _load_json(args.schema, "schema")
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        schema_error_objects = list(validator.iter_errors(consultation))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2

    schema_errors = sorted(
        (
            f"schema 错误位于 {_json_path(error)}: {error.message}"
            for error in schema_error_objects
        )
    )
    all_errors = schema_errors + semantic_errors(consultation)
    if all_errors:
        for error in all_errors:
            print(error, file=sys.stderr)
        return 1

    print("会诊记录有效。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
