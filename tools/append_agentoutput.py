#!/usr/bin/env python3
"""
Append a canonical AGENTOUTPUT entry without rewriting the file.
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Iterable

CANONICAL_REVIEWERS = ("APPROVE", "REQUEST_CHANGES", "BLOCK")


def resolve_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


DEFAULT_OUTPUT_PATH = resolve_repo_root() / "docs/301-BRIDGE/AGENTOUTPUT.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a canonical AGENTOUTPUT entry using the current execution time."
    )
    parser.add_argument("--tid", required=True, help="Target task ID, for example #TID-185-2-1")
    parser.add_argument(
        "--reviewer",
        required=True,
        choices=CANONICAL_REVIEWERS,
        help="Canonical reviewer decision",
    )
    parser.add_argument(
        "--reviewer-note",
        help="Optional note appended to the reviewer decision, for example rerun context",
    )
    parser.add_argument(
        "--file",
        dest="files",
        action="append",
        required=True,
        help="Changed file path. Repeat this option for multiple files.",
    )
    parser.add_argument(
        "--summary",
        action="append",
        required=True,
        help="Summary bullet. Repeat this option for multiple bullets.",
    )
    parser.add_argument(
        "--next-action",
        action="append",
        required=True,
        help="Next action item. Repeat this option for multiple items.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Append destination. Defaults to repo-root/docs/301-BRIDGE/AGENTOUTPUT.md",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated entry instead of appending it.",
    )
    return parser.parse_args()


def normalize_multiline(values: Iterable[str], label: str) -> list[str]:
    normalized = [value.strip() for value in values if value.strip()]
    if not normalized:
        raise SystemExit(f"{label} must include at least one non-empty value.")
    return normalized


def build_reviewer_line(reviewer: str, reviewer_note: str | None) -> str:
    if reviewer_note:
        return f"{reviewer}（{reviewer_note.strip()}）"
    return reviewer


def render_entry(args: argparse.Namespace) -> str:
    files = normalize_multiline(args.files, "--file")
    summaries = normalize_multiline(args.summary, "--summary")
    next_actions = normalize_multiline(args.next_action, "--next-action")
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    reviewer_value = build_reviewer_line(args.reviewer, args.reviewer_note)

    lines = [
        f"## {timestamp} root統合",
        f"- 対象TID: {args.tid.strip()}",
        "- 変更ファイル:",
    ]
    lines.extend(f"  - {path}" for path in files)
    lines.append(f"- reviewer判定: {reviewer_value}")
    lines.append("- 要約:")
    lines.extend(f"  - {item}" for item in summaries)
    lines.append("- 次アクション:")
    lines.extend(f"  {index}. {item}" for index, item in enumerate(next_actions, start=1))
    return "\n".join(lines) + "\n"


def append_entry(output_path: Path, entry: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    existing = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
    prefix = ""
    if existing:
        if not existing.endswith("\n"):
            prefix = "\n\n"
        elif not existing.endswith("\n\n"):
            prefix = "\n"
    output_path.write_text(existing + prefix + entry, encoding="utf-8")


def main() -> None:
    args = parse_args()
    entry = render_entry(args)
    if args.dry_run:
        print(entry, end="")
        return
    append_entry(args.output, entry)
    print(f"Appended AGENTOUTPUT entry to {args.output}")


if __name__ == "__main__":
    main()
