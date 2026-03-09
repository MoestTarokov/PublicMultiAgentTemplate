#!/usr/bin/env python3
"""
Commit Linter
-------------

This script validates commit messages for projects using the AgentCodingTemplateMulti
conventions. It ensures that the commit message includes a task ID (#TID-
format) and optionally checks for a valid type prefix (feat, fix, docs, refactor,
chore, test). It can be used as a pre-commit hook or manually to verify
messages before committing.

Usage examples:

```
python commit_linter.py --message "feat: implement login (#TID-2-1-2)"

# Reading from a file or standard input
git commit -m "<your message>" && python commit_linter.py --file .git/COMMIT_EDITMSG
```

If the message is valid, the script exits with code 0. If invalid, it
exits with non-zero status and prints an error message.
"""

import argparse
import re
import sys
from pathlib import Path

# Allowed commit types
ALLOWED_TYPES = {"feat", "fix", "docs", "refactor", "chore", "test"}

# Regex to extract TID pattern (#TID-X[-Y[-Z]])
TID_REGEX = re.compile(r"#TID-(\d+)(?:-(\d+))?(?:-(\d+))?")


def read_message(args: argparse.Namespace) -> str:
    """Read the commit message from --message or --file or stdin."""
    if args.message:
        return args.message.strip()
    if args.file:
        try:
            return Path(args.file).read_text(encoding="utf-8").strip()
        except Exception as e:
            raise SystemExit(f"Could not read commit message from {args.file}: {e}")
    # If no message or file provided, read from stdin
    return sys.stdin.read().strip()


def validate_commit(message: str, check_type: bool) -> None:
    """Validate the commit message. Raise SystemExit on failure."""
    lines = message.splitlines()
    if not lines:
        raise SystemExit("Commit message cannot be empty.")
    first_line = lines[0].strip()
    # Check type prefix if requested
    if check_type:
        if ":" not in first_line:
            raise SystemExit("Commit message must start with a type prefix (e.g., 'feat: ...').")
        commit_type, _ = first_line.split(":", 1)
        commit_type = commit_type.strip().lower()
        if commit_type not in ALLOWED_TYPES:
            allowed = ", ".join(sorted(ALLOWED_TYPES))
            raise SystemExit(f"Invalid commit type '{commit_type}'. Allowed types: {allowed}.")
    # Look for a TID anywhere in the message
    if not TID_REGEX.search(message):
        raise SystemExit("Commit message must include a task ID (e.g., '#TID-2-1-2').")


def main():
    parser = argparse.ArgumentParser(description="Validate commit messages for AgentCodingTemplateMulti.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message", help="Commit message string to validate")
    group.add_argument("--file", help="File containing the commit message (e.g., .git/COMMIT_EDITMSG)")
    parser.add_argument("--check-type", action="store_true", help="Enforce allowed type prefixes (feat, fix, docs, refactor, chore, test)")
    args = parser.parse_args()
    message = read_message(args)
    try:
        validate_commit(message, args.check_type)
    except SystemExit as e:
        print(f"Commit message invalid: {e}")
        sys.exit(1)
    # If no exception, commit is valid
    print("Commit message valid.")
    sys.exit(0)


if __name__ == "__main__":
    main()