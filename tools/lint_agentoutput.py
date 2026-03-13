#!/usr/bin/env python3
"""
Validate AGENTOUTPUT canonical structure and timestamps.
"""

import argparse
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


DEFAULT_TARGET_PATH = resolve_repo_root() / "docs/301-BRIDGE/AGENTOUTPUT.md"
HEADER_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) root統合$")
HEADER_CANDIDATE_RE = re.compile(r"^## .*root統合$")
TID_RE = re.compile(r"^- 対象TID: (#TID-\d+(?:-\d+){0,2})$")
REVIEWER_RE = re.compile(r"^- reviewer判定: (APPROVE|REQUEST_CHANGES|BLOCK)(?:[（(].+[）)])?$")


@dataclass
class Entry:
    header_line: int
    header_text: str
    timestamp_text: str | None
    lines: list[str] = field(default_factory=list)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint AGENTOUTPUT canonical root integration entries.")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_TARGET_PATH,
        help="Path to AGENTOUTPUT markdown. Defaults to repo-root/docs/301-BRIDGE/AGENTOUTPUT.md",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Lint all detected root統合 entries instead of only the latest entry candidate.",
    )
    parser.add_argument(
        "--future-tolerance-minutes",
        type=int,
        default=5,
        help="Allowed future skew for the latest entry timestamp",
    )
    return parser.parse_args()


def strip_fenced_blocks(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    in_fence = False
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        if raw_line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((line_number, raw_line.rstrip()))
    return result


def collect_entries(lines: list[tuple[int, str]]) -> list[Entry]:
    entries: list[Entry] = []
    current: Entry | None = None
    for line_number, line in lines:
        if HEADER_CANDIDATE_RE.match(line):
            if current is not None:
                entries.append(current)
            header_match = HEADER_RE.match(line)
            current = Entry(
                header_line=line_number,
                header_text=line,
                timestamp_text=header_match.group(1) if header_match else None,
            )
            current.lines.append(line)
            continue
        if current is not None:
            current.lines.append(line)
    if current is not None:
        entries.append(current)
    return entries


def validate_entry(entry: Entry) -> list[str]:
    errors: list[str] = []
    if entry.timestamp_text is None:
        errors.append(
            f"line {entry.header_line}: invalid header format '{entry.header_text}' "
            "expected '## YYYY-MM-DD HH:mm root統合'"
        )
        return errors

    tid_found = False
    reviewer_found = False
    files_section = False
    file_items = 0
    summary_section = False
    summary_items = 0
    next_action_section = False
    next_action_items = 0
    section = None

    for offset, line in enumerate(entry.lines[1:], start=1):
        line_number = entry.header_line + offset
        if line.startswith("- 対象TID: "):
            tid_found = True
            if not TID_RE.match(line):
                errors.append(f"line {line_number}: invalid 対象TID format in latest entry")
            section = None
        elif line == "- 変更ファイル:":
            files_section = True
            section = "files"
        elif line.startswith("- reviewer判定: "):
            reviewer_found = True
            if not REVIEWER_RE.match(line):
                errors.append(f"line {line_number}: invalid reviewer判定 in latest entry")
            section = None
        elif line == "- 要約:":
            summary_section = True
            section = "summary"
        elif line == "- 次アクション:":
            next_action_section = True
            section = "next_action"
        elif line.startswith("  - "):
            if section == "files":
                file_items += 1
            elif section == "summary":
                summary_items += 1
            else:
                errors.append(f"line {line_number}: unexpected bullet outside 変更ファイル/要約 in latest entry")
        elif re.match(r"^  \d+\. ", line):
            if section == "next_action":
                next_action_items += 1
            else:
                errors.append(f"line {line_number}: unexpected numbered item outside 次アクション in latest entry")
        elif line.strip():
            errors.append(f"line {line_number}: unexpected content in latest entry: '{line}'")

    if not tid_found:
        errors.append(f"line {entry.header_line}: missing 対象TID in latest entry")
    if not files_section:
        errors.append(f"line {entry.header_line}: missing 変更ファイル section in latest entry")
    if files_section and file_items == 0:
        errors.append(f"line {entry.header_line}: 変更ファイル section requires at least one item in latest entry")
    if not reviewer_found:
        errors.append(f"line {entry.header_line}: missing reviewer判定 in latest entry")
    if not summary_section:
        errors.append(f"line {entry.header_line}: missing 要約 section in latest entry")
    if summary_section and summary_items == 0:
        errors.append(f"line {entry.header_line}: 要約 section requires at least one item in latest entry")
    if not next_action_section:
        errors.append(f"line {entry.header_line}: missing 次アクション section in latest entry")
    if next_action_section and next_action_items == 0:
        errors.append(f"line {entry.header_line}: 次アクション section requires at least one item in latest entry")
    return errors


def validate_latest_timestamp(entry: Entry, tolerance_minutes: int) -> list[str]:
    if entry.timestamp_text is None:
        return []
    errors: list[str] = []
    latest_time = datetime.strptime(entry.timestamp_text, "%Y-%m-%d %H:%M")
    now = datetime.now()
    if latest_time > now + timedelta(minutes=tolerance_minutes):
        errors.append(
            f"line {entry.header_line}: latest entry timestamp {entry.timestamp_text} "
            f"is more than {tolerance_minutes} minutes in the future"
        )
    return errors


def main() -> None:
    args = parse_args()
    text = args.path.read_text(encoding="utf-8")
    visible_lines = strip_fenced_blocks(text)
    entries = collect_entries(visible_lines)
    if not entries:
        print(f"ERROR: no root統合 header candidate found in {args.path}")
        raise SystemExit(1)

    errors: list[str] = []
    targets = entries if args.all else [entries[-1]]
    for entry in targets:
        errors.extend(validate_entry(entry))
        if not errors and not args.all:
            errors.extend(validate_latest_timestamp(entry, args.future_tolerance_minutes))
        elif args.all and entry is entries[-1]:
            errors.extend(validate_latest_timestamp(entry, args.future_tolerance_minutes))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    scope = "all entries" if args.all else "latest entry"
    print(f"AGENTOUTPUT lint passed ({scope}): {args.path}")


if __name__ == "__main__":
    main()
