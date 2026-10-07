#!/usr/bin/env python3
"""根据 JSON 输入生成稳定的剧本位置索引。"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile


class ValidationError(ValueError):
    """当索引输入不满足必需结构时抛出。"""


class AtomicWriteCleanupError(OSError):
    """同时保留原子写入错误及其清理错误。"""

    def __init__(self, original_error, cleanup_error):
        self.original_error = original_error
        self.cleanup_error = cleanup_error
        super().__init__(
            f"{original_error}; 清理失败: {cleanup_error}"
        )


class CliArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValidationError(message)


def _positive_int(segment, field):
    value = segment.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{field} 必须是正整数")
    return value


def segment_id(segment):
    """返回场景或节拍片段的稳定位置标识。"""
    if not isinstance(segment, dict):
        raise ValidationError("segment 必须是对象")

    level = segment.get("level")
    if level not in ("scene", "beat"):
        raise ValidationError(f"不支持的 segment level: {level!r}")

    episode = _positive_int(segment, "episode")
    scene = _positive_int(segment, "scene")
    identifier = f"E{episode:03d}-S{scene:03d}"
    if level == "beat":
        beat = _positive_int(segment, "beat")
        identifier += f"-B{beat:03d}"
    return identifier


def _required_string(payload, field, *, allow_empty=False):
    value = payload.get(field)
    if not isinstance(value, str) or (not allow_empty and not value):
        qualifier = "" if allow_empty else "非空"
        raise ValidationError(f"{field} 必须是{qualifier}字符串")
    return value


def _reject_json_constant(constant):
    raise ValidationError(f"非法 JSON 常量: {constant}")


def stabilize(payload):
    """校验剧本载荷并返回确定性索引。"""
    if not isinstance(payload, dict):
        raise ValidationError("payload 必须是对象")

    script_id = _required_string(payload, "script_id")
    source_text = _required_string(payload, "source_text", allow_empty=True)
    segments = payload.get("segments")
    if not isinstance(segments, list):
        raise ValidationError("segments 必须是数组")

    stable_segments = []
    seen_ids = set()
    for position, segment in enumerate(segments):
        location = f"segments[{position}]"
        if not isinstance(segment, dict):
            raise ValidationError(f"{location}: segment 必须是对象")

        anchor = segment.get("anchor")
        if not isinstance(anchor, str) or not anchor or anchor not in source_text:
            raise ValidationError(f"{location}: 未找到 anchor")

        try:
            identifier = segment_id(segment)
        except ValueError as error:
            raise ValidationError(f"{location}: {error}") from None
        if identifier in seen_ids:
            raise ValidationError(
                f"{location}: segment_id 重复: {identifier}"
            )
        seen_ids.add(identifier)

        stable_segment = {**segment, "segment_id": identifier}
        stable_segments.append(stable_segment)

    return {
        "script_id": script_id,
        "source_hash": hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        "segments": stable_segments,
    }


def _parse_args(argv):
    parser = CliArgumentParser(
        description="根据 JSON 生成稳定的剧本位置索引。"
    )
    parser.add_argument("input", nargs="?", type=Path, help="输入 JSON 文件")
    parser.add_argument("-o", "--output", type=Path, help="输出 JSON 文件")
    return parser.parse_args(argv)


def _current_umask():
    # CLI 在单线程中同步写入，因此这里会立即恢复。
    previous_umask = os.umask(0)
    try:
        return previous_umask
    finally:
        os.umask(previous_umask)


def _write_atomic(output_path, contents):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_mode = stat.S_IMODE(output_path.stat().st_mode)
    except FileNotFoundError:
        output_mode = 0o666 & ~_current_umask()

    temporary_file = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary_path = Path(temporary_file.name)
    try:
        with temporary_file:
            temporary_file.write(contents)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.chmod(temporary_path, output_mode)
        os.replace(temporary_path, output_path)
    except BaseException as original_error:
        cleanup_error = None
        try:
            temporary_path.unlink(missing_ok=True)
        except BaseException as error:
            cleanup_error = error
        if isinstance(original_error, Exception) and isinstance(
            cleanup_error, Exception
        ):
            raise AtomicWriteCleanupError(
                original_error, cleanup_error
            ) from original_error
        raise


def main(argv=None):
    try:
        args = _parse_args(argv)
        if args.input is None or args.input == Path("-"):
            raw_input = sys.stdin.read()
        else:
            raw_input = args.input.read_text(encoding="utf-8")

        result = stabilize(json.loads(raw_input, parse_constant=_reject_json_constant))
        rendered = json.dumps(
            result, ensure_ascii=False, indent=2, allow_nan=False
        ) + "\n"
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            _write_atomic(args.output, rendered)
        return 0
    except (ValueError, OSError, UnicodeError) as error:
        print(f"错误: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
